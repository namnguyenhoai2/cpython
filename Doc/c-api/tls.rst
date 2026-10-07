.. highlight:: c

.. _thread-local-storage:

Hỗ trợ lưu trữ cục bộ theo thread
=================================

Trình thông dịch Python cung cấp hỗ trợ cấp thấp cho lưu trữ cục bộ theo thread (TLS), bao bọc triển khai TLS gốc bên dưới để hỗ trợ API lưu trữ cục bộ theo thread ở cấp Python (:class:`threading.local`). Các API cấp C của CPython tương tự những API do pthreads và Windows cung cấp: sử dụng một khóa thread và các hàm để liên kết một giá trị :c:expr:`void*` cho mỗi thread.

Một :term:`thread state` không cần được *không* gắn :term:`attached <attached thread state>` khi gọi các hàm này; chúng tự thực hiện việc khóa.

Lưu ý rằng :file:`Python.h` không bao gồm khai báo của các API TLS; bạn cần include :file:`pythread.h` để sử dụng lưu trữ cục bộ theo thread.

.. note::
   Không hàm API nào trong số này quản lý bộ nhớ thay cho các
   giá trị :c:expr:`void*`. Bạn cần tự cấp phát và giải phóng chúng. Nếu các giá trị :c:expr:`void*` tình cờ là :c:expr:`PyObject*`, các hàm này cũng không thực hiện thao tác refcount trên chúng.

.. _thread-specific-storage-api:

API lưu trữ dành riêng cho thread
---------------------------------

API bộ nhớ lưu trữ dành riêng cho luồng (TSS) được giới thiệu để thay thế việc sử dụng API TLS hiện có trong trình thông dịch CPython. API này sử dụng một kiểu mới :c:type:`Py_tss_t` thay vì
:c:expr:`int` để biểu diễn các khóa luồng.

.. versionadded:: 3.7

.. seealso:: "Một C-API mới cho Thread-Local Storage trong CPython" (:pep:`539`)


.. c:type:: Py_tss_t

   Cấu trúc dữ liệu này biểu diễn trạng thái của một khóa luồng, với định nghĩa có thể phụ thuộc vào triển khai TLS bên dưới, đồng thời có một trường nội bộ biểu diễn trạng thái khởi tạo của khóa. Cấu trúc này không có thành viên công khai.

   Khi :ref:`Py_LIMITED_API <stable>` chưa được định nghĩa, có thể cấp phát tĩnh kiểu này bằng :c:macro:`Py_tss_NEEDS_INIT`.


.. c:macro:: Py_tss_NEEDS_INIT

   Macro này mở rộng thành trình khởi tạo cho các biến :c:type:`Py_tss_t`. Lưu ý rằng macro này sẽ không được định nghĩa cùng với :ref:`Py_LIMITED_API <stable>`.


Cấp phát động
-------------

Cấp phát động :c:type:`Py_tss_t`, bắt buộc trong các mô-đun mở rộng được xây dựng với :ref:`Py_LIMITED_API <stable>`, vì không thể cấp phát tĩnh kiểu này do cách triển khai của nó là không trong suốt tại thời điểm xây dựng.


.. c:function:: Py_tss_t* PyThread_tss_alloc()

   Trả về một giá trị có trạng thái giống với giá trị được khởi tạo bằng
   :c:macro:`Py_tss_NEEDS_INIT`, hoặc ``NULL`` trong trường hợp cấp phát động không thành công.


.. c:function:: void PyThread_tss_free(Py_tss_t *key)

   Giải phóng *key* đã cho được :c:func:`PyThread_tss_alloc` cấp phát, sau khi gọi :c:func:`PyThread_tss_delete` trước để đảm bảo mọi biến cục bộ của thread liên kết đều đã được hủy gán. Đây là thao tác không thực hiện gì nếu đối số *key* là ``NULL``.

   .. note::
      Một key đã được giải phóng sẽ trở thành con trỏ treo. Bạn nên đặt lại key thành ``NULL``.


Các phương thức
---------------

Tham số *key* của các hàm này không được là ``NULL``.  Ngoài ra, hành vi của :c:func:`PyThread_tss_set` và :c:func:`PyThread_tss_get` là không xác định nếu :c:type:`Py_tss_t` đã cho chưa được khởi tạo bằng
:c:func:`PyThread_tss_create`.


.. c:function:: int PyThread_tss_is_created(Py_tss_t *key)

   Trả về giá trị khác không nếu :c:type:`Py_tss_t` đã được khởi tạo bởi :c:func:`PyThread_tss_create`.


.. c:function:: int PyThread_tss_create(Py_tss_t *key)

   Trả về giá trị bằng không khi khởi tạo thành công một khóa TSS. Hành vi không được xác định nếu giá trị được trỏ tới bởi đối số *key* chưa được khởi tạo bởi :c:macro:`Py_tss_NEEDS_INIT`. Có thể gọi hàm này nhiều lần trên cùng một khóa -- gọi hàm trên một khóa đã được khởi tạo sẽ không thực hiện thao tác nào và ngay lập tức trả về thành công.


.. c:function:: void PyThread_tss_delete(Py_tss_t *key)

   Hủy một khóa TSS để quên các giá trị liên kết với khóa trên tất cả các thread, đồng thời chuyển trạng thái khởi tạo của khóa thành chưa khởi tạo. Một khóa đã bị hủy có thể được khởi tạo lại bởi
   :c:func:`PyThread_tss_create`. Có thể gọi hàm này nhiều lần trên cùng một khóa -- gọi hàm trên một khóa đã bị hủy sẽ không thực hiện thao tác nào.


.. c:function:: int PyThread_tss_set(Py_tss_t *key, void *value)

   Trả về giá trị bằng không để cho biết đã liên kết thành công một giá trị :c:expr:`void*` với khóa TSS trong thread hiện tại. Mỗi thread có một ánh xạ riêng từ khóa đến giá trị :c:expr:`void*`.


.. c:function:: void* PyThread_tss_get(Py_tss_t *key)

   Trả về giá trị :c:expr:`void*` được liên kết với khóa TSS trong thread hiện tại. Hàm này trả về ``NULL`` nếu không có giá trị nào được liên kết với khóa trong thread hiện tại.


.. _thread-local-storage-api:

API cũ
------

.. deprecated:: 3.7
   API này bị thay thế bởi
   :ref:`API lưu trữ dành riêng cho thread (TSS) <thread-specific-storage-api>`.

.. note::
   Phiên bản API này không hỗ trợ các nền tảng mà khóa TLS gốc được định nghĩa theo cách không thể ép kiểu an toàn thành ``int``.  Trên những nền tảng đó,
   :c:func:`PyThread_create_key` sẽ ngay lập tức trả về trạng thái thất bại, còn tất cả các hàm TLS khác sẽ không thực hiện thao tác nào trên những nền tảng đó.

Do vấn đề tương thích nêu trên, không nên sử dụng phiên bản API này trong mã mới.

.. c:function:: int PyThread_create_key()
.. c:function:: void PyThread_delete_key(int key)
.. c:function:: int PyThread_set_key_value(int key, void *value)
.. c:function:: void* PyThread_get_key_value(int key)
.. c:function:: void PyThread_delete_key_value(int key)
.. c:function:: void PyThread_ReInitTLS()
