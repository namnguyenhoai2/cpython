.. highlight:: c


.. _memory:

**************
Quản lý bộ nhớ
**************

.. sectionauthor:: Vladimir Marangozov <Vladimir.Marangozov@inrialpes.fr>



.. _memoryoverview:

Tổng quan
=========

Quản lý bộ nhớ trong Python bao gồm một heap riêng chứa tất cả đối tượng và cấu trúc dữ liệu Python. Việc quản lý heap riêng này được đảm bảo nội bộ bởi *trình quản lý bộ nhớ Python*. Trình quản lý bộ nhớ Python có các thành phần khác nhau đảm nhiệm nhiều khía cạnh của việc quản lý lưu trữ động, chẳng hạn như chia sẻ, phân đoạn, cấp phát trước hoặc caching.

Ở cấp thấp nhất, một bộ cấp phát bộ nhớ thô đảm bảo có đủ chỗ trong heap riêng để lưu trữ tất cả dữ liệu liên quan đến Python bằng cách tương tác với trình quản lý bộ nhớ của hệ điều hành. Bên trên bộ cấp phát bộ nhớ thô, một số bộ cấp phát dành riêng cho từng loại đối tượng hoạt động trên cùng heap và triển khai các chính sách quản lý bộ nhớ riêng, phù hợp với đặc điểm của từng loại đối tượng. Ví dụ, các đối tượng số nguyên được quản lý trong heap khác với chuỗi, tuple hoặc dictionary vì số nguyên có yêu cầu lưu trữ cũng như sự đánh đổi khác nhau giữa tốc độ và không gian. Do đó, trình quản lý bộ nhớ Python ủy thác một phần công việc cho các bộ cấp phát dành riêng cho từng loại đối tượng, đồng thời đảm bảo các bộ cấp phát này hoạt động trong phạm vi của heap riêng.

Điều quan trọng là phải hiểu rằng việc quản lý heap Python được thực hiện bởi chính trình thông dịch và người dùng không thể kiểm soát việc này, ngay cả khi họ thường xuyên thao tác với các con trỏ đối tượng tới các khối bộ nhớ bên trong heap đó. Việc cấp phát không gian heap cho các đối tượng Python và những buffer nội bộ khác được trình quản lý bộ nhớ Python thực hiện theo nhu cầu thông qua các hàm Python/C API được liệt kê trong tài liệu này.

.. index::
   single: malloc (C function)
   single: calloc (C function)
   single: realloc (C function)
   single: free (C function)

Để tránh hỏng bộ nhớ, người viết extension không bao giờ được cố gắng thao tác với các đối tượng Python bằng những hàm do thư viện C xuất ra: :c:func:`malloc`,
:c:func:`calloc`, :c:func:`realloc` và :c:func:`free`. Điều này sẽ dẫn đến việc gọi lẫn lộn giữa bộ cấp phát C và trình quản lý bộ nhớ Python, với hậu quả nghiêm trọng, vì chúng triển khai các thuật toán khác nhau và hoạt động trên các heap khác nhau. Tuy nhiên, bạn có thể an toàn cấp phát và giải phóng các khối bộ nhớ bằng bộ cấp phát của thư viện C cho những mục đích riêng lẻ, như trong ví dụ sau::

   PyObject *res;
   char *buf = (char *) malloc(BUFSIZ); /* cho I/O */

   if (buf == NULL)
       return PyErr_NoMemory();
   ...Do some I/O operation involving buf...
   res = PyBytes_FromString(buf);
   free(buf); /* được cấp phát bằng malloc */
   return res;

Trong ví dụ này, yêu cầu bộ nhớ cho bộ đệm I/O được trình cấp phát của thư viện C xử lý. Trình quản lý bộ nhớ Python chỉ tham gia vào việc cấp phát đối tượng bytes được trả về làm kết quả.

Tuy nhiên, trong hầu hết các trường hợp, bạn nên cấp phát bộ nhớ từ heap Python, cụ thể là vì heap này nằm dưới sự kiểm soát của trình quản lý bộ nhớ Python. Ví dụ, điều này là bắt buộc khi mở rộng trình thông dịch bằng các kiểu đối tượng mới được viết bằng C. Một lý do khác để sử dụng heap Python là mong muốn *thông báo* cho trình quản lý bộ nhớ Python về nhu cầu bộ nhớ của mô-đun mở rộng. Ngay cả khi bộ nhớ được yêu cầu chỉ được sử dụng cho các mục đích nội bộ, rất đặc thù, việc ủy quyền tất cả yêu cầu bộ nhớ cho trình quản lý bộ nhớ Python giúp trình thông dịch có hình dung chính xác hơn về tổng thể lượng bộ nhớ mà nó sử dụng. Do đó, trong một số trường hợp nhất định, trình quản lý bộ nhớ Python có thể kích hoạt hoặc không kích hoạt các hành động phù hợp, chẳng hạn như thu gom rác, nén bộ nhớ hoặc các quy trình phòng ngừa khác. Lưu ý rằng khi sử dụng trình cấp phát của thư viện C như trong ví dụ trước, bộ nhớ được cấp phát cho bộ đệm I/O hoàn toàn nằm ngoài sự quản lý của trình quản lý bộ nhớ Python.

.. seealso::

   Biến môi trường :envvar:`PYTHONMALLOC` có thể được sử dụng để cấu hình các trình cấp phát bộ nhớ mà Python sử dụng.

   Biến môi trường :envvar:`PYTHONMALLOCSTATS` có thể được sử dụng để in thống kê của trình cấp phát bộ nhớ :ref:`pymalloc memory allocator <pymalloc>` mỗi khi một arena đối tượng pymalloc mới được tạo và khi tắt.

Các miền trình cấp phát
=======================

.. _allocator-domains:

Tất cả các hàm cấp phát thuộc về một trong ba "domain" khác nhau (xem thêm
:c:type:`PyMemAllocatorDomain`). Các domain này đại diện cho những chiến lược cấp phát khác nhau và được tối ưu hóa cho các mục đích khác nhau. Chi tiết cụ thể về cách mỗi domain cấp phát bộ nhớ hoặc các hàm nội bộ mà mỗi domain gọi được xem là chi tiết triển khai, nhưng để phục vụ việc gỡ lỗi, có thể xem bảng đơn giản hóa tại :ref:`default-memory-allocators`. Các API được dùng để cấp phát và giải phóng một khối bộ nhớ phải thuộc cùng một domain. Ví dụ: phải dùng :c:func:`PyMem_Free` để giải phóng bộ nhớ được cấp phát bằng :c:func:`PyMem_Malloc`.

Ba domain cấp phát là:

* Domain Raw: dùng để cấp phát bộ nhớ cho các bộ đệm bộ nhớ đa dụng, trong đó việc cấp phát *must* chuyển đến system allocator hoặc allocator có thể hoạt động mà không cần :term:`attached thread state`. Bộ nhớ được yêu cầu trực tiếp từ hệ thống. Xem :ref:`Raw Memory Interface <raw-memoryinterface>`.

* Domain "Mem": dùng để cấp phát bộ nhớ cho các bộ đệm Python và các bộ đệm bộ nhớ đa dụng, trong đó việc cấp phát phải được thực hiện bằng :term:`attached thread state`. Bộ nhớ được lấy từ private heap của Python. Xem :ref:`Memory Interface <memoryinterface>`.

* Domain Object: dùng để cấp phát bộ nhớ cho các đối tượng Python. Bộ nhớ được lấy từ private heap của Python. Xem :ref:`Object allocators <objectinterface>`.

.. note::

  Bản build :term:`free-threaded <free threading>` yêu cầu chỉ các đối tượng Python được cấp phát bằng domain "object" và tất cả đối tượng Python đều được cấp phát bằng domain đó. Điều này khác với các phiên bản Python trước đây, trong đó đây chỉ là một best practice chứ không phải yêu cầu bắt buộc.

  Ví dụ: các buffer (đối tượng không phải Python) nên được cấp phát bằng :c:func:`PyMem_Malloc`,
  :c:func:`PyMem_RawMalloc`, hoặc :c:func:`malloc`, nhưng không phải :c:func:`PyObject_Malloc`.

  Xem :ref:`Các API cấp phát bộ nhớ <free-threaded-memory-allocation>`.


.. _raw-memoryinterface:

Giao diện bộ nhớ thô
====================

Các tập hợp hàm sau đây là wrapper cho allocator của hệ thống. Các hàm này an toàn với thread, vì vậy một :term:`thread state` không cần phải được :term:`gắn <attached thread state>`.

:ref:`Allocator bộ nhớ thô mặc định <default-memory-allocators>` sử dụng các hàm sau: :c:func:`malloc`, :c:func:`calloc`, :c:func:`realloc` và :c:func:`!free`; gọi ``malloc(1)`` (hoặc ``calloc(1, 1)``) khi yêu cầu zero byte.

.. versionadded:: 3.4

.. c:function:: void* PyMem_RawMalloc(size_t n)

   Cấp phát *n* byte và trả về một con trỏ kiểu :c:expr:`void*` trỏ đến vùng nhớ đã cấp phát, hoặc ``NULL`` nếu yêu cầu không thành công.

   Việc yêu cầu số byte bằng không sẽ trả về một con trỏ không phải ``NULL`` nếu có thể, như thể ``PyMem_RawMalloc(1)`` đã được gọi thay thế. Bộ nhớ sẽ không được khởi tạo theo bất kỳ cách nào.


.. c:function:: void* PyMem_RawCalloc(size_t nelem, size_t elsize)

   Cấp phát *nelem* phần tử, mỗi phần tử có kích thước *elsize* byte, và trả về một con trỏ kiểu :c:expr:`void*` trỏ đến vùng nhớ đã cấp phát, hoặc ``NULL`` nếu yêu cầu thất bại. Bộ nhớ được khởi tạo bằng các giá trị zero.

   Yêu cầu cấp phát zero phần tử hoặc phần tử có kích thước zero byte sẽ trả về một con trỏ khác ``NULL`` nếu có thể, như thể ``PyMem_RawCalloc(1, 1)`` đã được gọi thay thế.

   .. versionadded:: 3.5


.. c:function:: void* PyMem_RawRealloc(void *p, size_t n)

   Thay đổi kích thước khối bộ nhớ được trỏ đến bởi *p* thành *n* byte. Nội dung sẽ không thay đổi trong phạm vi kích thước nhỏ hơn giữa kích thước cũ và mới.

   Nếu *p* là ``NULL``, lệnh gọi tương đương với ``PyMem_RawMalloc(n)``; nếu không, nếu *n* bằng zero, khối bộ nhớ sẽ được thay đổi kích thước nhưng không được giải phóng, và con trỏ được trả về là khác ``NULL``.

   Trừ khi *p* là ``NULL``, nó phải được trả về bởi một lần gọi trước đó đến
   :c:func:`PyMem_RawMalloc`, :c:func:`PyMem_RawRealloc` hoặc
   :c:func:`PyMem_RawCalloc`.

   Nếu yêu cầu không thành công, :c:func:`PyMem_RawRealloc` trả về ``NULL`` và *p* vẫn là một con trỏ hợp lệ tới vùng bộ nhớ trước đó.


.. c:function:: void PyMem_RawFree(void *p)

   Giải phóng khối bộ nhớ được *p* trỏ tới; khối này phải đã được trả về bởi một lần gọi trước đó tới :c:func:`PyMem_RawMalloc`, :c:func:`PyMem_RawRealloc` hoặc
   :c:func:`PyMem_RawCalloc`. Nếu không, hoặc nếu ``PyMem_RawFree(p)`` đã được gọi trước đó, hành vi không xác định sẽ xảy ra.

   Nếu *p* là ``NULL``, không thực hiện thao tác nào.


.. _memoryinterface:

Giao diện bộ nhớ
================

Các tập hợp hàm sau đây, được mô phỏng theo tiêu chuẩn ANSI C nhưng quy định hành vi khi yêu cầu số byte bằng không, có sẵn để cấp phát và giải phóng bộ nhớ từ heap Python.

Trong bản build bật GIL (bản build mặc định), các
:ref:`bộ cấp phát bộ nhớ mặc định <default-memory-allocators>` sử dụng
:ref:`bộ cấp phát bộ nhớ pymalloc <pymalloc>`, trong khi ở
:term:`free-threaded build`, mặc định là
:ref:`bộ cấp phát bộ nhớ mimalloc <mimalloc>` thay vào đó.

.. warning::

   Phải có một :term:`attached thread state` khi sử dụng các hàm này.

.. versionchanged:: 3.6

   Bộ cấp phát mặc định hiện là pymalloc thay vì :c:func:`malloc` hệ thống.

.. versionchanged:: 3.13

   Trong bản build :term:`free-threaded <free threading>`, bộ cấp phát mặc định hiện là :ref:`mimalloc <mimalloc>`.

.. c:function:: void* PyMem_Malloc(size_t n)

   Cấp phát *n* byte và trả về một con trỏ kiểu :c:expr:`void*` trỏ đến vùng nhớ đã cấp phát, hoặc ``NULL`` nếu yêu cầu thất bại.

   Việc yêu cầu 0 byte sẽ trả về một con trỏ khác ``NULL`` nếu có thể, như thể ``PyMem_Malloc(1)`` đã được gọi thay thế. Vùng nhớ sẽ không được khởi tạo theo bất kỳ cách nào.


.. c:function:: void* PyMem_Calloc(size_t nelem, size_t elsize)

   Cấp phát *nelem* phần tử, mỗi phần tử có kích thước *elsize* byte, và trả về một con trỏ kiểu :c:expr:`void*` trỏ đến vùng nhớ đã cấp phát, hoặc ``NULL`` nếu yêu cầu thất bại. Vùng nhớ được khởi tạo bằng các giá trị 0.

   Việc yêu cầu 0 phần tử hoặc các phần tử có kích thước 0 byte sẽ trả về một con trỏ khác ``NULL`` nếu có thể, như thể ``PyMem_Calloc(1, 1)`` đã được gọi thay thế.

   .. versionadded:: 3.5


.. c:function:: void* PyMem_Realloc(void *p, size_t n)

   Thay đổi kích thước khối nhớ được con trỏ *p* trỏ đến thành *n* byte. Nội dung sẽ không thay đổi trong phạm vi kích thước nhỏ hơn giữa kích thước cũ và mới.

   Nếu *p* là ``NULL``, lệnh gọi này tương đương với ``PyMem_Malloc(n)``; nếu không, nếu *n* bằng 0, khối nhớ sẽ được thay đổi kích thước nhưng không được giải phóng, và con trỏ được trả về sẽ khác ``NULL``.

   Trừ khi *p* là ``NULL``, nó phải được trả về từ một lần gọi trước đó tới
   :c:func:`PyMem_Malloc`, :c:func:`PyMem_Realloc` hoặc :c:func:`PyMem_Calloc`.

   Nếu yêu cầu thất bại, :c:func:`PyMem_Realloc` trả về ``NULL`` và *p* vẫn là một con trỏ hợp lệ đến vùng bộ nhớ trước đó.


.. c:function:: void PyMem_Free(void *p)

   Giải phóng khối bộ nhớ được *p* trỏ tới; khối này phải được trả về bởi một lần gọi trước đó đến :c:func:`PyMem_Malloc`, :c:func:`PyMem_Realloc` hoặc
   :c:func:`PyMem_Calloc`. Nếu không, hoặc nếu ``PyMem_Free(p)`` đã được gọi trước đó, hành vi không xác định sẽ xảy ra.

   Nếu *p* là ``NULL``, không có thao tác nào được thực hiện.

Các macro định hướng theo kiểu sau đây được cung cấp để thuận tiện. Lưu ý rằng *TYPE* đề cập đến bất kỳ kiểu C nào.


.. c:macro:: PyMem_New(TYPE, n)

   Tương tự như :c:func:`PyMem_Malloc`, nhưng cấp phát ``(n * sizeof(TYPE))`` byte bộ nhớ. Trả về một con trỏ được ép kiểu thành ``TYPE*``. Bộ nhớ sẽ không được khởi tạo theo bất kỳ cách nào.


.. c:macro:: PyMem_Resize(p, TYPE, n)

   Giống như :c:func:`PyMem_Realloc`, nhưng khối bộ nhớ được thay đổi kích thước thành ``(n * sizeof(TYPE))`` byte. Trả về một con trỏ được ép kiểu thành ``TYPE*``. Khi trả về, *p* sẽ là con trỏ tới vùng nhớ mới hoặc ``NULL`` nếu xảy ra lỗi.

   Đây là một macro tiền xử lý C; *p* luôn được gán lại. Hãy lưu giá trị ban đầu của *p* để tránh làm mất vùng nhớ khi xử lý lỗi.


.. c:function:: void PyMem_Del(void *p)

   Giống như :c:func:`PyMem_Free`.


Bí danh đã lỗi thời
-------------------

Đây là các bí danh :term:`soft deprecated` của những hàm và macro hiện có. Chúng chỉ tồn tại để duy trì khả năng tương thích ngược.

.. list-table::
   :widths: auto
   :header-rows: 1

   * * Bí danh đã lỗi thời
     * Hàm hoặc macro tương ứng
   * * .. c:macro:: PyMem_MALLOC(size)
     * :c:func:`PyMem_Malloc`
   * * .. c:macro:: PyMem_NEW(type, size)
     * :c:macro:`PyMem_New`
   * * .. c:macro:: PyMem_REALLOC(ptr, size)
     * :c:func:`PyMem_Realloc`
   * * .. c:macro:: PyMem_RESIZE(ptr, type, size)
     * :c:macro:`PyMem_Resize`
   * * .. c:macro:: PyMem_FREE(ptr)
     * :c:func:`PyMem_Free`
   * * .. c:macro:: PyMem_DEL(ptr)
     * :c:func:`PyMem_Free`

.. versionchanged:: 3.4

   Các macro hiện là bí danh của các hàm và macro tương ứng. Trước đây, hành vi của chúng giống nhau, nhưng việc sử dụng chúng không nhất thiết vẫn duy trì khả năng tương thích nhị phân giữa các phiên bản Python.

.. deprecated:: 2.0


.. _objectinterface:

Bộ cấp phát đối tượng
=====================

Các nhóm hàm sau đây, được xây dựng theo tiêu chuẩn ANSI C nhưng quy định hành vi khi yêu cầu số byte bằng không, có sẵn để cấp phát và giải phóng bộ nhớ từ heap Python.

.. note::
    Không có gì đảm bảo rằng bộ nhớ được các bộ cấp phát này trả về có thể được ép kiểu thành công thành một đối tượng Python khi can thiệp vào các hàm cấp phát trong miền này bằng các phương thức được mô tả trong phần :ref:`Customize Memory Allocators <customize-memory-allocators>`.

:ref:`Bộ cấp phát đối tượng mặc định <default-memory-allocators>` sử dụng
:ref:`bộ cấp phát bộ nhớ pymalloc <pymalloc>`.  Trong bản dựng
:term:`không có GIL <free threading>`, mặc định là
thay vào đó là :ref:`mimalloc memory allocator <mimalloc>`.

.. warning::

   Phải có một :term:`attached thread state` khi sử dụng các hàm này.

.. c:function:: void* PyObject_Malloc(size_t n)

   Cấp phát *n* byte và trả về một con trỏ kiểu :c:expr:`void*` trỏ đến vùng nhớ đã cấp phát, hoặc ``NULL`` nếu yêu cầu thất bại.

   Yêu cầu cấp phát 0 byte sẽ trả về một con trỏ khác biệt và không phải ``NULL``, nếu có thể, như thể ``PyObject_Malloc(1)`` đã được gọi thay thế. Vùng nhớ sẽ không được khởi tạo theo bất kỳ cách nào.


.. c:function:: void* PyObject_Calloc(size_t nelem, size_t elsize)

   Cấp phát *nelem* phần tử, mỗi phần tử có kích thước *elsize* byte, và trả về một con trỏ kiểu :c:expr:`void*` trỏ đến vùng nhớ đã cấp phát, hoặc ``NULL`` nếu yêu cầu thất bại. Vùng nhớ được khởi tạo bằng các số 0.

   Yêu cầu cấp phát 0 phần tử hoặc phần tử có kích thước 0 byte sẽ trả về một con trỏ khác biệt và không phải ``NULL``, nếu có thể, như thể ``PyObject_Calloc(1, 1)`` đã được gọi thay thế.

   .. versionadded:: 3.5


.. c:function:: void* PyObject_Realloc(void *p, size_t n)

   Thay đổi kích thước khối nhớ được *p* trỏ đến thành *n* byte. Nội dung sẽ không thay đổi trong phạm vi kích thước nhỏ hơn giữa kích thước cũ và mới.

   Nếu *p* là ``NULL``, lời gọi tương đương với ``PyObject_Malloc(n)``; nếu không, nếu *n* bằng không, khối bộ nhớ được thay đổi kích thước nhưng không được giải phóng, và con trỏ được trả về không phải là ``NULL``.

   Trừ khi *p* là ``NULL``, nó phải được trả về bởi một lời gọi trước đó đến
   :c:func:`PyObject_Malloc`, :c:func:`PyObject_Realloc` hoặc :c:func:`PyObject_Calloc`.

   Nếu yêu cầu không thành công, :c:func:`PyObject_Realloc` trả về ``NULL`` và *p* vẫn là một con trỏ hợp lệ đến vùng bộ nhớ trước đó.


.. c:function:: void PyObject_Free(void *p)

   Giải phóng khối bộ nhớ được *p* trỏ tới; khối này phải được trả về bởi một lời gọi trước đó đến :c:func:`PyObject_Malloc`, :c:func:`PyObject_Realloc` hoặc
   :c:func:`PyObject_Calloc`. Nếu không, hoặc nếu ``PyObject_Free(p)`` đã được gọi trước đó, hành vi không xác định sẽ xảy ra.

   Nếu *p* là ``NULL``, không có thao tác nào được thực hiện.

   Đừng gọi trực tiếp hàm này để giải phóng bộ nhớ của một đối tượng; hãy gọi thành phần của type
   :c:member:`~PyTypeObject.tp_free` slot thay vào đó.

   Không sử dụng hàm này cho bộ nhớ được cấp phát bởi :c:macro:`PyObject_GC_New` hoặc
   :c:macro:`PyObject_GC_NewVar`; hãy sử dụng :c:func:`PyObject_GC_Del` thay vào đó.

   .. seealso::

      * :c:func:`PyObject_GC_Del` tương đương với hàm này đối với bộ nhớ được cấp phát bởi các type hỗ trợ garbage collection.
      * :c:func:`PyObject_Malloc`
      * :c:func:`PyObject_Realloc`
      * :c:func:`PyObject_Calloc`
      * :c:macro:`PyObject_New`
      * :c:macro:`PyObject_NewVar`
      * :c:func:`PyType_GenericAlloc`
      * :c:member:`~PyTypeObject.tp_free`


.. _default-memory-allocators:

Các bộ cấp phát bộ nhớ mặc định
===============================

Các bộ cấp phát bộ nhớ mặc định:

+----------------------------------------+----------------------+----------------------+----------------------+----------------------+
| Cấu hình                               | Tên                  | PyMem_RawMalloc      | PyMem_Malloc         | PyObject_Malloc      |
+========================================+======================+======================+======================+======================+
| Bản dựng Release                       | ``"pymalloc"``       | ``malloc``           | ``pymalloc``         | ``pymalloc``         |
+----------------------------------------+----------------------+----------------------+----------------------+----------------------+
| Bản dựng Debug                         | ``"pymalloc_debug"`` | ``malloc`` + debug   | ``pymalloc`` + debug | ``pymalloc`` + debug |
+----------------------------------------+----------------------+----------------------+----------------------+----------------------+
| Bản build phát hành, không có pymalloc | ``"malloc"``         | ``malloc``           | ``malloc``           | ``malloc``           |
+----------------------------------------+----------------------+----------------------+----------------------+----------------------+
| Bản build debug, không có pymalloc     | ``"malloc_debug"``   | ``malloc`` + debug   | ``malloc`` + debug   | ``malloc`` + debug   |
+----------------------------------------+----------------------+----------------------+----------------------+----------------------+
| Bản dựng free-threaded                 | ``"mimalloc"``       | ``mimalloc``         | ``mimalloc``         | ``mimalloc``         |
+----------------------------------------+----------------------+----------------------+----------------------+----------------------+
| Bản dựng debug free-threaded           | ``"mimalloc_debug"`` | ``mimalloc`` + debug | ``mimalloc`` + debug | ``mimalloc`` + debug |
+----------------------------------------+----------------------+----------------------+----------------------+----------------------+

Chú giải:

* Tên: giá trị của biến môi trường :envvar:`PYTHONMALLOC`.
* ``malloc``: các bộ cấp phát của hệ thống từ thư viện C chuẩn, các hàm C:
  :c:func:`malloc`, :c:func:`calloc`, :c:func:`realloc` và :c:func:`free`.
* ``pymalloc``: :ref:`bộ cấp phát bộ nhớ pymalloc <pymalloc>`.
* ``mimalloc``: :ref:`bộ cấp phát bộ nhớ mimalloc <mimalloc>`.
* "+ debug": với :ref:`các hook gỡ lỗi trên các bộ cấp phát bộ nhớ Python <pymem-debug-hooks>`.
* "Bản dựng Debug": :ref:`bản dựng Python ở chế độ gỡ lỗi <debug-build>`.

.. _customize-memory-allocators:

Tùy chỉnh bộ cấp phát bộ nhớ
============================

.. versionadded:: 3.4

.. c:type:: PyMemAllocatorEx

   Cấu trúc dùng để mô tả bộ cấp phát khối bộ nhớ. Cấu trúc có các trường sau:

   +----------------------------------------------------------+-----------------------------------------------------------+
   | Trường                                                   | Ý nghĩa                                                   |
   +==========================================================+===========================================================+
   | ``void *ctx``                                            | ngữ cảnh người dùng được truyền dưới dạng đối số đầu tiên |
   +----------------------------------------------------------+-----------------------------------------------------------+
   | ``void* malloc(void *ctx, size_t size)``                 | cấp phát một khối bộ nhớ                                  |
   +----------------------------------------------------------+-----------------------------------------------------------+
   | ``void* calloc(void *ctx, size_t nelem, size_t elsize)`` | cấp phát một khối bộ nhớ được khởi tạo bằng các số 0      |
   +----------------------------------------------------------+-----------------------------------------------------------+
   | ``void* realloc(void *ctx, void *ptr, size_t new_size)`` | cấp phát hoặc thay đổi kích thước một khối bộ nhớ         |
   +----------------------------------------------------------+-----------------------------------------------------------+
   | ``void free(void *ctx, void *ptr)``                      | giải phóng một khối bộ nhớ                                |
   +----------------------------------------------------------+-----------------------------------------------------------+

   .. versionchanged:: 3.5
      Cấu trúc :c:type:`!PyMemAllocator` đã được đổi tên thành
      :c:type:`PyMemAllocatorEx` và một trường ``calloc`` mới đã được thêm vào.


.. c:type:: PyMemAllocatorDomain

   Enum dùng để xác định miền của allocator. Các miền:

   .. c:namespace:: NULL

   .. c:macro:: PYMEM_DOMAIN_RAW

      Các hàm:

      * :c:func:`PyMem_RawMalloc`
      * :c:func:`PyMem_RawRealloc`
      * :c:func:`PyMem_RawCalloc`
      * :c:func:`PyMem_RawFree`

   .. c:macro:: PYMEM_DOMAIN_MEM

      Các hàm:

      * :c:func:`PyMem_Malloc`,
      * :c:func:`PyMem_Realloc`
      * :c:func:`PyMem_Calloc`
      * :c:func:`PyMem_Free`

   .. c:macro:: PYMEM_DOMAIN_OBJ

      Các hàm:

      * :c:func:`PyObject_Malloc`
      * :c:func:`PyObject_Realloc`
      * :c:func:`PyObject_Calloc`
      * :c:func:`PyObject_Free`

.. c:function:: void PyMem_GetAllocator(PyMemAllocatorDomain domain, PyMemAllocatorEx *allocator)

   Lấy bộ cấp phát khối bộ nhớ của miền được chỉ định.


.. c:function:: void PyMem_SetAllocator(PyMemAllocatorDomain domain, PyMemAllocatorEx *allocator)

   Thiết lập bộ cấp phát khối bộ nhớ của miền được chỉ định.

   Bộ cấp phát mới phải trả về một con trỏ khác biệt không phải ``NULL`` khi yêu cầu 0 byte.

   Đối với miền :c:macro:`PYMEM_DOMAIN_RAW`, bộ cấp phát phải an toàn với thread: một :term:`thread state` không :term:`attached <attached thread state>` khi bộ cấp phát được gọi.

   Đối với các miền còn lại, bộ cấp phát cũng phải an toàn với thread: bộ cấp phát có thể được gọi trong các interpreter khác nhau không dùng chung một :term:`GIL`.

   Nếu bộ cấp phát mới không phải là một hook (không gọi bộ cấp phát trước đó), phải gọi hàm :c:func:`PyMem_SetupDebugHooks` để cài đặt lại các debug hook trên bộ cấp phát mới.

   Xem thêm :c:member:`PyPreConfig.allocator` và :ref:`Khởi tạo trước Python bằng PyPreConfig <c-preinit>`.

   .. warning::

       :c:func:`PyMem_SetAllocator` tuân theo hợp đồng sau đây:

       * Có thể gọi nó sau :c:func:`Py_PreInitialize` và trước
         :c:func:`Py_InitializeFromConfig` để cài đặt một memory allocator tùy chỉnh. Không có hạn chế nào đối với allocator đã cài đặt ngoài những hạn chế do domain áp đặt (chẳng hạn, Raw Domain cho phép gọi allocator mà không cần :term:`attached thread state`). Xem :ref:`phần về các domain của allocator <allocator-domains>` để biết thêm thông tin.

       * Nếu được gọi sau khi Python hoàn tất việc khởi tạo (sau khi
         :c:func:`Py_InitializeFromConfig` đã được gọi), allocator **phải** bao bọc allocator hiện có. Việc thay thế allocator hiện tại bằng một allocator tùy ý khác **không được hỗ trợ**.

   .. versionchanged:: 3.12
      Tất cả allocator phải an toàn với thread.


.. c:function:: void PyMem_SetupDebugHooks(void)

   Thiết lập :ref:`các hook debug trong bộ cấp phát bộ nhớ Python <pymem-debug-hooks>` để phát hiện lỗi bộ nhớ.


.. _pymem-debug-hooks:

Các hook debug trên bộ cấp phát bộ nhớ Python
=============================================

Khi :ref:`Python được xây dựng ở chế độ debug <debug-build>`, phần này
hàm :c:func:`PyMem_SetupDebugHooks` được gọi trong :ref:`giai đoạn khởi tạo trước Python <c-preinit>` để thiết lập các hook debug trên bộ cấp phát bộ nhớ Python nhằm phát hiện lỗi bộ nhớ.

Có thể sử dụng biến môi trường :envvar:`PYTHONMALLOC` để cài đặt các hook debug trên Python được biên dịch ở chế độ release (ví dụ: ``PYTHONMALLOC=debug``).

Có thể sử dụng hàm :c:func:`PyMem_SetupDebugHooks` để thiết lập các hook debug sau khi gọi :c:func:`PyMem_SetAllocator`.

Các hook debug này lấp đầy các khối bộ nhớ được cấp phát động bằng những mẫu bit đặc biệt, dễ nhận biết. Bộ nhớ mới được cấp phát được lấp đầy bằng byte ``0xCD`` (``PYMEM_CLEANBYTE``), còn bộ nhớ đã giải phóng được lấp đầy bằng byte ``0xDD`` (``PYMEM_DEADBYTE``). Các khối bộ nhớ được bao quanh bởi các "byte bị cấm", được lấp đầy bằng byte ``0xFD`` (``PYMEM_FORBIDDENBYTE``). Các chuỗi byte này khó có khả năng là địa chỉ hợp lệ, số thực hoặc chuỗi ASCII.

Kiểm tra runtime:

- Phát hiện các vi phạm API. Ví dụ: phát hiện trường hợp gọi :c:func:`PyObject_Free` trên một khối bộ nhớ được cấp phát bởi :c:func:`PyMem_Malloc`.
- Phát hiện việc ghi trước phần đầu của bộ đệm (buffer underflow).
- Phát hiện việc ghi sau phần cuối của bộ đệm (buffer overflow).
- Kiểm tra rằng có một :term:`attached thread state` khi các hàm allocator của :c:macro:`PYMEM_DOMAIN_OBJ` (ví dụ:
  :c:func:`PyObject_Malloc`) và các miền :c:macro:`PYMEM_DOMAIN_MEM` (ví dụ:
  :c:func:`PyMem_Malloc`) được gọi.

Khi xảy ra lỗi, các debug hook sử dụng module :mod:`tracemalloc` để lấy traceback tại nơi một khối bộ nhớ được cấp phát. Traceback chỉ được hiển thị nếu :mod:`tracemalloc` đang trace các lần cấp phát bộ nhớ của Python và khối bộ nhớ đó đã được trace.

Gọi *S* = ``sizeof(size_t)``. Có ``2*S`` byte được thêm vào mỗi đầu của từng khối gồm *N* byte được yêu cầu. Bố cục bộ nhớ như sau, trong đó p biểu thị địa chỉ được trả về bởi một hàm giống malloc hoặc realloc (``p[i:j]`` có nghĩa là lát byte từ ``*(p+i)`` bao gồm đến ``*(p+j)`` không bao gồm; lưu ý rằng cách xử lý các chỉ mục âm khác với lát trong Python):

``p[-2*S:-S]``
    Số byte được yêu cầu ban đầu. Đây là một size_t, theo thứ tự big-endian (dễ đọc hơn trong bản kết xuất bộ nhớ).
``p[-S]``
    Mã định danh API (ký tự ASCII):

    * ``'r'`` cho :c:macro:`PYMEM_DOMAIN_RAW`.
    * ``'m'`` cho :c:macro:`PYMEM_DOMAIN_MEM`.
    * ``'o'`` cho :c:macro:`PYMEM_DOMAIN_OBJ`.

``p[-S+1:0]``
    Các bản sao của PYMEM_FORBIDDENBYTE. Được dùng để phát hiện việc ghi và đọc vượt quá giới hạn.

``p[0:N]``
    Vùng bộ nhớ được yêu cầu, chứa các bản sao của PYMEM_CLEANBYTE, được dùng để phát hiện việc tham chiếu đến bộ nhớ chưa được khởi tạo. Khi một hàm dạng realloc được gọi để yêu cầu một khối bộ nhớ lớn hơn, các byte dư mới cũng được điền bằng PYMEM_CLEANBYTE. Khi một hàm dạng free được gọi, chúng sẽ bị ghi đè bằng PYMEM_DEADBYTE để phát hiện việc tham chiếu đến bộ nhớ đã được giải phóng. Khi một hàm dạng realloc được gọi để yêu cầu một khối bộ nhớ nhỏ hơn, các byte cũ dư ra cũng được điền bằng PYMEM_DEADBYTE.

``p[N:N+S]``
    Các bản sao của PYMEM_FORBIDDENBYTE. Được dùng để phát hiện việc ghi và đọc vượt quá giới hạn.

``p[N+S:N+2*S]``
    Chỉ được sử dụng nếu macro ``PYMEM_DEBUG_SERIALNO`` được định nghĩa (theo mặc định thì không được định nghĩa).

    Một số sê-ri, được tăng thêm 1 sau mỗi lần gọi một hàm dạng malloc hoặc realloc. :c:type:`size_t` big-endian. Nếu phát hiện "bộ nhớ không hợp lệ" sau đó, số sê-ri cung cấp một cách rất hiệu quả để đặt breakpoint trong lần chạy tiếp theo, nhằm ghi lại thời điểm khối này được cấp phát. Hàm tĩnh bumpserialno() trong obmalloc.c là nơi duy nhất số sê-ri được tăng, và tồn tại để bạn có thể dễ dàng đặt breakpoint như vậy.

Một hàm dạng realloc hoặc free trước tiên sẽ kiểm tra xem các byte PYMEM_FORBIDDENBYTE ở mỗi đầu có còn nguyên vẹn hay không. Nếu chúng đã bị thay đổi, thông tin chẩn đoán sẽ được ghi vào stderr và chương trình bị hủy thông qua Py_FatalError(). Một dạng lỗi chính khác là gây ra lỗi bộ nhớ khi chương trình đọc một trong các mẫu bit đặc biệt rồi cố sử dụng nó làm địa chỉ. Nếu khi đó bạn vào trình debugger và xem đối tượng, rất có thể bạn sẽ thấy nó được điền hoàn toàn bằng PYMEM_DEADBYTE (nghĩa là bộ nhớ đã được giải phóng đang bị sử dụng) hoặc PYMEM_CLEANBYTE (nghĩa là bộ nhớ chưa được khởi tạo đang bị sử dụng).

.. versionchanged:: 3.6
   Hàm :c:func:`PyMem_SetupDebugHooks` hiện cũng hoạt động trên Python được biên dịch ở chế độ release. Khi có lỗi, các debug hook hiện sử dụng
   :mod:`tracemalloc` để lấy traceback tại nơi một khối bộ nhớ được cấp phát. Các debug hook hiện cũng kiểm tra xem có :term:`attached thread state` khi các hàm thuộc các miền :c:macro:`PYMEM_DOMAIN_OBJ` và :c:macro:`PYMEM_DOMAIN_MEM` được gọi hay không.

.. versionchanged:: 3.8
   Các mẫu byte ``0xCB`` (``PYMEM_CLEANBYTE``), ``0xDB`` (``PYMEM_DEADBYTE``) và ``0xFB`` (``PYMEM_FORBIDDENBYTE``) đã được thay thế bằng ``0xCD``, ``0xDD`` và ``0xFD`` để sử dụng cùng các giá trị với ``malloc()`` và ``free()`` debug của Windows CRT.


.. _pymalloc:

Bộ cấp phát pymalloc
====================

Python có bộ cấp phát *pymalloc* được tối ưu hóa cho các đối tượng nhỏ (nhỏ hơn hoặc bằng 512 byte) có thời gian tồn tại ngắn. Bộ cấp phát này sử dụng các ánh xạ bộ nhớ được gọi là "arena", với kích thước cố định là 256 KiB trên nền tảng 32-bit hoặc 1 MiB trên nền tảng 64-bit. Bộ cấp phát này chuyển sang :c:func:`PyMem_RawMalloc` và
:c:func:`PyMem_RawRealloc` cho các lần cấp phát lớn hơn 512 byte.

*pymalloc* là :ref:`bộ cấp phát mặc định <default-memory-allocators>` của
:c:macro:`PYMEM_DOMAIN_MEM` (ví dụ: :c:func:`PyMem_Malloc`) và
:c:macro:`PYMEM_DOMAIN_OBJ` (ví dụ: :c:func:`PyObject_Malloc`) miền.

Bộ cấp phát arena sử dụng các hàm sau:

* :c:func:`!VirtualAlloc` và :c:func:`!VirtualFree` trên Windows,
* :c:func:`!mmap` và :c:func:`!munmap` nếu khả dụng,
* :c:func:`malloc` và :c:func:`free` trong các trường hợp khác.

Bộ cấp phát này bị vô hiệu hóa nếu Python được cấu hình với tùy chọn
:option:`--without-pymalloc`. Bạn cũng có thể vô hiệu hóa bộ cấp phát này trong runtime bằng biến môi trường :envvar:`PYTHONMALLOC` (ví dụ: ``PYTHONMALLOC=malloc``).

Thông thường, nên vô hiệu hóa bộ cấp phát pymalloc khi xây dựng Python với AddressSanitizer (:option:`--with-address-sanitizer`), công cụ này giúp phát hiện các lỗi cấp thấp trong mã C.

Tùy chỉnh bộ cấp phát Arena của pymalloc
----------------------------------------

.. versionadded:: 3.4

.. c:type:: PyObjectArenaAllocator

   Cấu trúc dùng để mô tả một bộ cấp phát arena. Cấu trúc này có ba trường:

   +--------------------------------------------------+-----------------------------------------------------+
   | Trường                                           | Ý nghĩa                                             |
   +==================================================+=====================================================+
   | ``void *ctx``                                    | ngữ cảnh người dùng được truyền làm đối số đầu tiên |
   +--------------------------------------------------+-----------------------------------------------------+
   | ``void* alloc(void *ctx, size_t size)``          | cấp phát một arena có kích thước tính bằng byte     |
   +--------------------------------------------------+-----------------------------------------------------+
   | ``void free(void *ctx, void *ptr, size_t size)`` | giải phóng một arena                                |
   +--------------------------------------------------+-----------------------------------------------------+

.. c:function:: void PyObject_GetArenaAllocator(PyObjectArenaAllocator *allocator)

   Lấy arena allocator.

.. c:function:: void PyObject_SetArenaAllocator(PyObjectArenaAllocator *allocator)

   Thiết lập arena allocator.

.. _mimalloc:

mimalloc allocator
==================

.. versionadded:: 3.13

Python hỗ trợ allocator `mimalloc <https://github.com/microsoft/mimalloc/>`__ khi nền tảng bên dưới có hỗ trợ tương ứng. mimalloc là một allocator đa mục đích có hiệu năng rất tốt, ban đầu được Daan Leijen phát triển cho các hệ thống runtime của các ngôn ngữ Koka và Lean.

Không giống :ref:`pymalloc <pymalloc>`, vốn được tối ưu cho các đối tượng nhỏ (512 byte trở xuống), mimalloc xử lý các allocation với mọi kích thước.

Trong bản build :term:`free-threaded <free threading>`, mimalloc là allocator mặc định và **bắt buộc** cho :c:macro:`PYMEM_DOMAIN_MEM` và
:c:macro:`PYMEM_DOMAIN_OBJ` các domain. Không thể vô hiệu hóa trong các bản build free-threaded. Bản build free-threaded sử dụng các heap mimalloc riêng cho từng thread, nhờ đó việc cấp phát và giải phóng có thể tiến hành mà không cần khóa trong hầu hết các trường hợp.

Trong bản build mặc định (không free-threaded), mimalloc khả dụng nhưng không phải allocator mặc định. Có thể chọn nó trong runtime bằng
:envvar:`PYTHONMALLOC`\ ``=mimalloc`` (hoặc ``mimalloc_debug`` để bao gồm
:ref:`debug hooks <pymem-debug-hooks>`). Có thể vô hiệu hóa nó tại thời điểm build bằng tùy chọn configure :option:`--without-mimalloc`, nhưng không thể kết hợp tùy chọn này với :option:`--disable-gil`.

C API của tracemalloc
=====================

.. versionadded:: 3.7

.. c:function:: int PyTraceMalloc_Track(unsigned int domain, uintptr_t ptr, size_t size)

   Theo dõi một khối bộ nhớ đã cấp phát trong mô-đun :mod:`tracemalloc`.

   Trả về ``0`` khi thành công, trả về ``-1`` khi có lỗi (không thể cấp phát bộ nhớ để lưu trace). Trả về ``-2`` nếu tracemalloc bị vô hiệu hóa.

   Nếu khối bộ nhớ đã được theo dõi, hãy cập nhật dấu vết hiện có.

.. c:function:: int PyTraceMalloc_Untrack(unsigned int domain, uintptr_t ptr)

   Hủy theo dõi một khối bộ nhớ đã được cấp phát trong mô-đun :mod:`tracemalloc`. Không thực hiện thao tác nào nếu khối này chưa được theo dõi.

   Trả về ``-2`` nếu tracemalloc bị tắt, nếu không thì trả về ``0``.


.. _memoryexamples:

Ví dụ
=====

Dưới đây là ví dụ từ phần :ref:`memoryoverview`, được viết lại để bộ đệm I/O được cấp phát từ heap Python bằng cách sử dụng bộ hàm đầu tiên::

   PyObject *res;
   char *buf = (char *) PyMem_Malloc(BUFSIZ); /* cho I/O */

   if (buf == NULL)
       return PyErr_NoMemory();
   /* ...Thực hiện một thao tác I/O liên quan đến buf... */
   res = PyBytes_FromString(buf);
   PyMem_Free(buf); /* được cấp phát bằng PyMem_Malloc */
   return res;

Cùng đoạn mã đó khi sử dụng bộ hàm hướng theo kiểu::

   PyObject *res;
   char *buf = PyMem_New(char, BUFSIZ); /* cho I/O */

   if (buf == NULL)
       return PyErr_NoMemory();
   /* ...Thực hiện một thao tác I/O liên quan đến buf... */
   res = PyBytes_FromString(buf);
   PyMem_Free(buf); /* được cấp phát bằng PyMem_New */
   return res;

Lưu ý rằng trong hai ví dụ trên, buffer luôn được thao tác thông qua các hàm thuộc cùng một bộ. Thật vậy, bắt buộc phải sử dụng cùng một họ memory API cho một khối bộ nhớ nhất định, để giảm thiểu nguy cơ trộn lẫn các bộ cấp phát khác nhau. Chuỗi mã sau đây chứa hai lỗi, một trong số đó được đánh dấu là *nghiêm trọng* vì nó trộn lẫn hai bộ cấp phát khác nhau hoạt động trên các heap khác nhau.::

   char *buf1 = PyMem_New(char, BUFSIZ);
   char *buf2 = (char *) malloc(BUFSIZ);
   char *buf3 = (char *) PyMem_Malloc(BUFSIZ);
   ...
   PyMem_Del(buf3);  /* Sai -- phải là PyMem_Free() */
   free(buf2);       /* Đúng -- được cấp phát bằng malloc() */
   free(buf1);       /* Nghiêm trọng -- phải dùng PyMem_Free()  */

Ngoài các hàm dùng để xử lý các khối bộ nhớ thô từ heap của Python, các đối tượng trong Python được cấp phát và giải phóng bằng :c:macro:`PyObject_New`,
:c:macro:`PyObject_NewVar` và :c:func:`PyObject_Free`.

Những nội dung này sẽ được giải thích trong chương tiếp theo về cách định nghĩa và triển khai các kiểu đối tượng mới trong C.
