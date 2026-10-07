.. highlight:: c

.. _typeobjects:

Đối tượng kiểu
--------------

.. index:: pair: object; type


.. c:type:: PyTypeObject

   Cấu trúc C của các đối tượng được dùng để mô tả các kiểu dựng sẵn.


.. c:var:: PyTypeObject PyType_Type

   Đây là đối tượng kiểu dành cho các đối tượng kiểu; nó chính là đối tượng
   :class:`type` trong lớp Python.


.. c:function:: int PyType_Check(PyObject *o)

   Trả về giá trị khác 0 nếu đối tượng *o* là một đối tượng kiểu, bao gồm cả các thể hiện của những kiểu được dẫn xuất từ đối tượng kiểu chuẩn. Trả về 0 trong mọi trường hợp khác. Hàm này luôn thành công.


.. c:function:: int PyType_CheckExact(PyObject *o)

   Trả về giá trị khác 0 nếu đối tượng *o* là một đối tượng kiểu, nhưng không phải là kiểu con của đối tượng kiểu chuẩn. Trả về 0 trong mọi trường hợp khác. Hàm này luôn thành công.


.. c:function:: unsigned int PyType_ClearCache()

   Xóa bộ nhớ đệm tra cứu nội bộ. Trả về thẻ phiên bản hiện tại.

.. c:function:: unsigned long PyType_GetFlags(PyTypeObject* type)

   Trả về thành phần :c:member:`~PyTypeObject.tp_flags` của *type*. Hàm này chủ yếu được dùng với ``Py_LIMITED_API``; các bit cờ riêng lẻ được đảm bảo ổn định giữa các bản phát hành Python, nhưng quyền truy cập vào
   :c:member:`~PyTypeObject.tp_flags` bản thân nó không thuộc :ref:`limited API <limited-c-api>`.

   .. versionadded:: 3.2

   .. versionchanged:: 3.4
      Kiểu trả về hiện là ``unsigned long`` thay vì ``long``.


.. c:function:: PyObject* PyType_GetDict(PyTypeObject* type)

   Trả về namespace nội bộ của đối tượng kiểu, vốn chỉ được cung cấp theo cách khác thông qua một proxy chỉ đọc (:attr:`cls.__dict__ <type.__dict__>`). Đây là cách thay thế cho việc truy cập trực tiếp vào :c:member:`~PyTypeObject.tp_dict`. Từ điển được trả về phải được coi là chỉ đọc.

   Hàm này dành cho các trường hợp embedding và language binding cụ thể, khi cần truy cập trực tiếp vào dict và việc truy cập gián tiếp (ví dụ: thông qua proxy hoặc :c:func:`PyObject_GetAttr`) không đủ đáp ứng.

   Các extension module tiếp tục sử dụng ``tp_dict``, trực tiếp hoặc gián tiếp, khi thiết lập các type của riêng chúng.

   .. versionadded:: 3.12


.. c:function:: void PyType_Modified(PyTypeObject *type)

   Vô hiệu hóa bộ nhớ đệm tra cứu nội bộ cho type và tất cả subtype của nó. Hàm này phải được gọi sau mọi sửa đổi thủ công đối với các thuộc tính hoặc base class của type.


.. c:function:: int PyType_AddWatcher(PyType_WatchCallback callback)

   Đăng ký *callback* làm trình theo dõi kiểu. Trả về một ID số nguyên không âm, ID này phải được truyền vào các lần gọi sau đến :c:func:`PyType_Watch`. Trong trường hợp xảy ra lỗi (ví dụ: không còn ID trình theo dõi khả dụng), trả về ``-1`` và thiết lập một ngoại lệ.

   Trong các bản build free-threaded, :c:func:`PyType_AddWatcher` không an toàn với thread, vì vậy phải gọi nó khi khởi động (trước khi tạo thread đầu tiên).

   .. versionadded:: 3.12


.. c:function:: int PyType_ClearWatcher(int watcher_id)

   Xóa trình theo dõi được xác định bởi *watcher_id* (trước đó được trả về từ
   :c:func:`PyType_AddWatcher`). Trả về ``0`` nếu thành công, ``-1`` nếu xảy ra lỗi (ví dụ: nếu *watcher_id* chưa từng được đăng ký.)

   Một extension không bao giờ được gọi ``PyType_ClearWatcher`` với *watcher_id* chưa từng được trả về cho extension đó bởi một lần gọi trước đến
   :c:func:`PyType_AddWatcher`.

   .. versionadded:: 3.12


.. c:function:: int PyType_Watch(int watcher_id, PyObject *type)

   Đánh dấu *type* là đang được theo dõi. Callback được cấp *watcher_id* bởi
   :c:func:`PyType_AddWatcher` sẽ được gọi bất cứ khi nào
   :c:func:`PyType_Modified` báo cáo một thay đổi đối với *type*. (Callback có thể chỉ được gọi một lần cho một loạt các sửa đổi liên tiếp đối với *type*, nếu
   :c:func:`!_PyType_Lookup` không được gọi trên *type* giữa các lần sửa đổi; đây là một chi tiết triển khai và có thể thay đổi.)

   Một extension không bao giờ được gọi ``PyType_Watch`` với một *watcher_id* chưa được trả về cho nó bởi một lần gọi trước đó tới :c:func:`PyType_AddWatcher`.

   .. versionadded:: 3.12


.. c:function:: int PyType_Unwatch(int watcher_id, PyObject *type)

   Đánh dấu *type* là không được theo dõi. Thao tác này hoàn tác một lần gọi trước đó tới
   :c:func:`PyType_Watch`. *type* không được là ``NULL``.

   Một extension không bao giờ được gọi hàm này với một *watcher_id* chưa được trả về cho nó bởi một lần gọi trước đó tới :c:func:`PyType_AddWatcher`.

   Khi thành công, hàm này trả về ``0``. Khi thất bại, hàm này trả về ``-1`` cùng với một exception được thiết lập.

   .. versionadded:: 3.12


.. c:type:: int (*PyType_WatchCallback)(PyObject *type)

   Kiểu của hàm callback theo dõi kiểu.

   Callback không được sửa đổi *type* hoặc khiến :c:func:`PyType_Modified` được gọi trên *type* hay bất kỳ kiểu nào trong MRO của nó; vi phạm quy tắc này có thể gây ra đệ quy vô hạn.

   .. versionadded:: 3.12


.. c:function:: int PyType_HasFeature(PyTypeObject *o, int feature)

   Trả về giá trị khác 0 nếu đối tượng kiểu *o* thiết lập tính năng *feature*. Các tính năng của kiểu được biểu thị bằng các cờ bit đơn.


.. c:function:: int PyType_FastSubclass(PyTypeObject *type, int flag)

   Trả về giá trị khác 0 nếu đối tượng kiểu *type* thiết lập cờ lớp con *flag*. Các cờ lớp con được biểu thị bằng
   :c:macro:`Py_TPFLAGS_*_SUBCLASS <Py_TPFLAGS_LONG_SUBCLASS>`. Hàm này được nhiều hàm ``_Check`` sử dụng cho các kiểu thông dụng.

   .. seealso::
       :c:func:`PyObject_TypeCheck`, which is used as a slower alternative in
       ``_Check`` hàm dành cho các kiểu không đi kèm cờ lớp con.


.. c:function:: int PyType_IS_GC(PyTypeObject *o)

   Trả về true nếu đối tượng kiểu hỗ trợ bộ phát hiện chu kỳ; hàm này kiểm tra cờ kiểu :c:macro:`Py_TPFLAGS_HAVE_GC`.


.. c:function:: int PyType_IsSubtype(PyTypeObject *a, PyTypeObject *b)

   Trả về true nếu *a* là kiểu con của *b*.

   Hàm này chỉ kiểm tra các kiểu con thực sự, nghĩa là
   :meth:`~type.__subclasscheck__` không được gọi trên *b*. Hãy gọi
   :c:func:`PyObject_IsSubclass` để thực hiện cùng phép kiểm tra mà :func:`issubclass` sẽ thực hiện.


.. c:function:: PyObject* PyType_GenericAlloc(PyTypeObject *type, Py_ssize_t nitems)

   Bộ xử lý chung cho slot :c:member:`~PyTypeObject.tp_alloc` của một đối tượng kiểu. Sử dụng cơ chế cấp phát bộ nhớ mặc định của Python để cấp phát bộ nhớ cho một instance mới, đặt toàn bộ vùng nhớ về 0, sau đó khởi tạo vùng nhớ như thể đang gọi :c:func:`PyObject_Init` hoặc :c:func:`PyObject_InitVar`.

   Không gọi trực tiếp hàm này để cấp phát bộ nhớ cho một đối tượng; thay vào đó, hãy gọi slot của type
   :c:member:`~PyTypeObject.tp_alloc`.

   Đối với các kiểu hỗ trợ garbage collection (tức là cờ
   :c:macro:`Py_TPFLAGS_HAVE_GC` được đặt), hàm này hoạt động như
   :c:macro:`PyObject_GC_New` hoặc :c:macro:`PyObject_GC_NewVar` (ngoại trừ việc bộ nhớ được bảo đảm đã được đặt về 0 trước khi khởi tạo), và nên được dùng cùng với :c:func:`PyObject_GC_Del` trong :c:member:`~PyTypeObject.tp_free`. Nếu không, nó hoạt động như :c:macro:`PyObject_New` hoặc
   :c:macro:`PyObject_NewVar` (ngoại trừ việc bộ nhớ được bảo đảm đã được đặt về 0 trước khi khởi tạo) và nên được dùng cùng với :c:func:`PyObject_Free` trong
   :c:member:`~PyTypeObject.tp_free`.


.. c:function:: PyObject* PyType_GenericNew(PyTypeObject *type, PyObject *args, PyObject *kwds)

   Trình xử lý chung cho slot :c:member:`~PyTypeObject.tp_new` của một đối tượng kiểu. Tạo một instance mới bằng slot :c:member:`~PyTypeObject.tp_new` của kiểu và trả về đối tượng thu được.
   :c:member:`~PyTypeObject.tp_alloc` của kiểu và trả về đối tượng thu được.


.. c:function:: int PyType_Ready(PyTypeObject *type)

   Hoàn tất một đối tượng kiểu. Hàm này nên được gọi trên tất cả các đối tượng kiểu để hoàn tất quá trình khởi tạo. Hàm này chịu trách nhiệm thêm các slot được kế thừa từ lớp cơ sở của một kiểu. Trả về ``0`` khi thành công, hoặc trả về ``-1`` và đặt một exception khi xảy ra lỗi.

   .. note::
       Nếu một số lớp cơ sở triển khai giao thức GC và kiểu được cung cấp không bao gồm :c:macro:`Py_TPFLAGS_HAVE_GC` trong các cờ của nó, thì giao thức GC sẽ được tự động triển khai từ các lớp cha. Ngược lại, nếu kiểu đang được tạo có bao gồm
       :c:macro:`Py_TPFLAGS_HAVE_GC` trong các cờ của nó thì nó **bắt buộc** phải tự triển khai giao thức GC bằng cách ít nhất triển khai
       :c:member:`~PyTypeObject.tp_traverse` handle.


.. c:function:: PyObject* PyType_GetName(PyTypeObject *type)

   Trả về tên của type. Tương đương với việc lấy thuộc tính
   :attr:`~type.__name__` của type.

   .. versionadded:: 3.11


.. c:function:: PyObject* PyType_GetQualName(PyTypeObject *type)

   Trả về tên đủ điều kiện của type. Tương đương với việc lấy thuộc tính :attr:`~type.__qualname__` của type.

   .. versionadded:: 3.11

.. c:function:: PyObject* PyType_GetFullyQualifiedName(PyTypeObject *type)

   Trả về tên đầy đủ của type. Tương đương với ``f"{type.__module__}.{type.__qualname__}"``, hoặc :attr:`type.__qualname__` nếu :attr:`type.__module__` không phải là một chuỗi hoặc bằng ``"builtins"``.

   .. versionadded:: 3.13


.. c:function:: PyObject* PyType_GetModuleName(PyTypeObject *type)

   Trả về tên module của kiểu. Tương đương với việc lấy
   thuộc tính :attr:`type.__module__`.

   .. versionadded:: 3.13


.. c:function:: void* PyType_GetSlot(PyTypeObject *type, int slot)

   Trả về con trỏ hàm được lưu trong slot đã cho. Nếu kết quả là ``NULL``, điều này cho biết slot là ``NULL``, hoặc hàm đã được gọi với các tham số không hợp lệ. Thông thường, bên gọi sẽ ép con trỏ kết quả sang kiểu hàm thích hợp.

   Xem :c:member:`PyType_Slot.slot` để biết các giá trị có thể có của đối số *slot*.

   .. versionadded:: 3.4

   .. versionchanged:: 3.10
      :c:func:`PyType_GetSlot` can now accept all types.
      Trước đây, nó chỉ bị giới hạn ở :ref:`các kiểu heap <heap-types>`.


.. c:function:: PyObject* PyType_GetModule(PyTypeObject *type)

   Trả về đối tượng module liên kết với kiểu đã cho khi kiểu đó được tạo bằng :c:func:`PyType_FromModuleAndSpec`.

   Tham chiếu được trả về là :term:`mượn <borrowed reference>` từ *kiểu*, và sẽ hợp lệ miễn là bạn còn giữ một tham chiếu đến *kiểu*. Không giải phóng tham chiếu này bằng :c:func:`Py_DECREF` hoặc tương tự.

   Nếu không có module nào được liên kết với kiểu đã cho, đặt :py:class:`TypeError` và trả về ``NULL``.

   Hàm này thường được dùng để lấy module mà trong đó một phương thức được định nghĩa. Lưu ý rằng trong một phương thức như vậy, ``PyType_GetModule(Py_TYPE(self))`` có thể không trả về kết quả mong muốn. ``Py_TYPE(self)`` có thể là một *subclass* của class dự kiến, và các subclass không nhất thiết được định nghĩa trong cùng module với superclass của chúng. Xem :c:type:`PyCMethod` để lấy class định nghĩa phương thức. Xem :c:func:`PyType_GetModuleByDef` để biết các trường hợp không thể sử dụng :c:type:`!PyCMethod`.

   .. versionadded:: 3.9


.. c:function:: void* PyType_GetModuleState(PyTypeObject *type)

   Trả về trạng thái của đối tượng module được liên kết với kiểu đã cho. Đây là cách viết tắt để gọi :c:func:`PyModule_GetState()` trên kết quả của :c:func:`PyType_GetModule`.

   Nếu không có module nào được liên kết với kiểu đã cho, đặt :py:class:`TypeError` và trả về ``NULL``.

   Nếu *type* có module liên kết nhưng trạng thái của module là ``NULL``, trả về ``NULL`` mà không đặt exception.

   .. versionadded:: 3.9


.. c:function:: PyObject* PyType_GetModuleByDef(PyTypeObject *type, struct PyModuleDef *def)

   Tìm superclass đầu tiên có module được tạo từ :c:type:`PyModuleDef` *def* đã cho, rồi trả về module đó.

   Nếu không tìm thấy module nào, phát sinh một :py:class:`TypeError` và trả về ``NULL``.

   Hàm này được dùng cùng với
   :c:func:`PyModule_GetState()` để lấy trạng thái mô-đun từ các phương thức slot (chẳng hạn như
   :c:member:`~PyTypeObject.tp_init` hoặc :c:member:`~PyNumberMethods.nb_add`) và những nơi khác mà lớp định nghĩa của một phương thức không thể được truyền bằng quy ước gọi
   :c:type:`PyCMethod`.

   Tham chiếu được trả về là :term:`mượn <borrowed reference>` từ *kiểu*, và sẽ hợp lệ miễn là bạn còn giữ một tham chiếu đến *kiểu*. Không giải phóng tham chiếu này bằng :c:func:`Py_DECREF` hoặc tương tự.

   .. versionadded:: 3.11


.. c:function:: int PyType_GetBaseByToken(PyTypeObject *type, void *token, PyTypeObject **result)

   Tìm lớp cha đầu tiên trong *type*'s :term:`method resolution order` mà
   :c:macro:`Py_tp_token` token bằng với token đã cho.

   * Nếu tìm thấy, đặt *\*result* thành một :term:`strong reference` mới tới nó và trả về ``1``.
   * Nếu không tìm thấy, đặt *\*result* thành ``NULL`` và trả về ``0``.
   * Khi xảy ra lỗi, đặt *\*result* thành ``NULL`` và trả về ``-1`` với một exception được thiết lập.

   Đối số *result* có thể là ``NULL``, trong trường hợp đó *\*result* không được thiết lập. Sử dụng tùy chọn này nếu bạn chỉ cần giá trị trả về.

   Đối số *token* không được là ``NULL``.

   .. versionadded:: 3.14


.. c:function:: int PyUnstable_Type_AssignVersionTag(PyTypeObject *type)

   Cố gắng gán một thẻ phiên bản cho kiểu đã cho.

   Trả về 1 nếu kiểu đã có thẻ phiên bản hợp lệ hoặc một thẻ mới đã được gán, hoặc 0 nếu không thể gán thẻ mới.

   .. versionadded:: 3.12


.. c:function:: int PyType_SUPPORTS_WEAKREFS(PyTypeObject *type)

   Trả về true nếu các instance của *type* hỗ trợ tạo weak reference, ngược lại trả về false. Hàm này luôn thành công. *type* không được là ``NULL``.

   .. seealso::
      * :ref:`weakrefobjects`
      * :py:mod:`weakref`


Tạo các kiểu heap được cấp phát trên heap
.........................................

Các hàm và cấu trúc sau được dùng để tạo
:ref:`các kiểu heap <heap-types>`.

.. c:function:: PyObject* PyType_FromMetaclass(PyTypeObject *metaclass, PyObject *module, PyType_Spec *spec, PyObject *bases)

   Tạo và trả về một :ref:`kiểu heap <heap-types>` từ *đặc tả* (xem :c:macro:`Py_TPFLAGS_HEAPTYPE`).

   *Metaclass* được dùng để xây dựng đối tượng kiểu kết quả. Khi *metaclass* là ``NULL``, metaclass được suy ra từ *bases* (hoặc các slot *Py_tp_base[s]* nếu *bases* là ``NULL``, xem bên dưới).

   Các metaclass ghi đè :c:member:`~PyTypeObject.tp_new` không được hỗ trợ, trừ khi ``tp_new`` là ``NULL``.

   Đối số *bases* có thể được dùng để chỉ định các lớp cơ sở; đối số này có thể là một lớp duy nhất hoặc một tuple các lớp. Nếu *bases* là ``NULL``, slot :c:data:`Py_tp_bases` sẽ được sử dụng thay thế. Nếu giá trị đó cũng là ``NULL``, slot :c:data:`Py_tp_base` sẽ được sử dụng thay thế. Nếu giá trị đó cũng là ``NULL``, kiểu mới sẽ kế thừa từ :class:`object`.

   Đối số *module* có thể được dùng để ghi lại module nơi lớp mới được định nghĩa. Đối số này phải là một đối tượng module hoặc ``NULL``. Nếu không phải ``NULL``, module sẽ được liên kết với kiểu mới và sau đó có thể được lấy lại bằng :c:func:`PyType_GetModule`. Module được liên kết không được kế thừa bởi các lớp con; module phải được chỉ định riêng cho từng lớp.

   Hàm này gọi :c:func:`PyType_Ready` trên kiểu mới.

   Lưu ý rằng hàm này *not* hoàn toàn khớp với hành vi khi gọi :py:class:`type() <type>` hoặc sử dụng câu lệnh :keyword:`class`. Với các kiểu cơ sở hoặc metaclass do người dùng cung cấp, nên ưu tiên
   :ref:`calling <capi-call>` :py:class:`type` (hoặc metaclass) thay vì các hàm ``PyType_From*``. Cụ thể:

   * :py:meth:`~object.__new__` không được gọi trên lớp mới (và phải được đặt thành ``type.__new__``).
   * :py:meth:`~object.__init__` không được gọi trên lớp mới.
   * :py:meth:`~object.__init_subclass__` không được gọi trên bất kỳ lớp cơ sở nào.
   * :py:meth:`~object.__set_name__` không được gọi trên các descriptor mới.

   .. versionadded:: 3.12


.. c:function:: PyObject* PyType_FromModuleAndSpec(PyObject *module, PyType_Spec *spec, PyObject *bases)

   Tương đương với ``PyType_FromMetaclass(NULL, module, spec, bases)``.

   .. versionadded:: 3.9

   .. versionchanged:: 3.10

      Hàm hiện chấp nhận một lớp duy nhất làm đối số *bases* và ``NULL`` làm slot ``tp_doc``.

   .. versionchanged:: 3.12

      Hàm hiện tìm và sử dụng một metaclass tương ứng với các lớp cơ sở được cung cấp. Trước đây, chỉ các thực thể :class:`type` được trả về.

      :c:member:`~PyTypeObject.tp_new` của metaclass bị *bỏ qua*, điều này có thể dẫn đến việc khởi tạo không đầy đủ. Việc tạo các lớp có metaclass ghi đè
      :c:member:`~PyTypeObject.tp_new` đã lỗi thời.

   .. versionchanged:: 3.14

      Tạo các lớp có metaclass ghi đè
      :c:member:`~PyTypeObject.tp_new` không còn được cho phép.


.. c:function:: PyObject* PyType_FromSpecWithBases(PyType_Spec *spec, PyObject *bases)

   Tương đương với ``PyType_FromMetaclass(NULL, NULL, spec, bases)``.

   .. versionadded:: 3.3

   .. versionchanged:: 3.12

      Hàm hiện tìm và sử dụng một metaclass tương ứng với các lớp cơ sở được cung cấp. Trước đây, chỉ các thực thể :class:`type` được trả về.

      :c:member:`~PyTypeObject.tp_new` của metaclass bị *bỏ qua*, điều này có thể dẫn đến việc khởi tạo không đầy đủ. Việc tạo các lớp có metaclass ghi đè
      :c:member:`~PyTypeObject.tp_new` đã lỗi thời.

   .. versionchanged:: 3.14

      Tạo các lớp có metaclass ghi đè
      :c:member:`~PyTypeObject.tp_new` không còn được cho phép.


.. c:function:: PyObject* PyType_FromSpec(PyType_Spec *spec)

   Tương đương với ``PyType_FromMetaclass(NULL, NULL, spec, NULL)``.

   .. versionchanged:: 3.12

      Giờ đây, hàm sẽ tìm và sử dụng một metaclass tương ứng với các lớp cơ sở được cung cấp trong các slot *Py_tp_base[s]*. Trước đây, chỉ các instance :class:`type` được trả về.

      :c:member:`~PyTypeObject.tp_new` của metaclass bị *bỏ qua*, điều này có thể dẫn đến việc khởi tạo không đầy đủ. Việc tạo các lớp có metaclass ghi đè
      :c:member:`~PyTypeObject.tp_new` đã lỗi thời.

   .. versionchanged:: 3.14

      Tạo các lớp có metaclass ghi đè
      :c:member:`~PyTypeObject.tp_new` không còn được cho phép.


.. c:function:: int PyType_Freeze(PyTypeObject *type)

   Làm cho một kiểu trở nên bất biến: đặt cờ :c:macro:`Py_TPFLAGS_IMMUTABLETYPE`.

   Mọi lớp cơ sở của *type* phải là bất biến.

   Nếu thành công, trả về ``0``. Nếu có lỗi, đặt một exception và trả về ``-1``.

   Không được sử dụng kiểu này trước khi làm cho nó trở nên bất biến. Ví dụ: không được tạo các thực thể của kiểu trước khi kiểu này trở nên bất biến.

   .. versionadded:: 3.14

.. raw:: html

   <!-- Keep old URL fragments working (see gh-97908) -->
   <span id='c.PyType_Spec.PyType_Spec.name'></span>
   <span id='c.PyType_Spec.PyType_Spec.basicsize'></span>
   <span id='c.PyType_Spec.PyType_Spec.itemsize'></span>
   <span id='c.PyType_Spec.PyType_Spec.flags'></span>
   <span id='c.PyType_Spec.PyType_Spec.slots'></span>

.. c:type:: PyType_Spec

   Cấu trúc xác định hành vi của một kiểu.

   .. c:member:: const char* name

      Tên của kiểu, được dùng để đặt :c:member:`PyTypeObject.tp_name`.

   .. c:member:: int basicsize

      Nếu là số dương, chỉ định kích thước của thực thể tính bằng byte. Giá trị này được dùng để đặt :c:member:`PyTypeObject.tp_basicsize`.

      Nếu bằng không, chỉ định rằng :c:member:`~PyTypeObject.tp_basicsize` sẽ được kế thừa.

      Nếu âm, giá trị tuyệt đối chỉ định lượng không gian mà các thực thể của lớp cần *ngoài phần* của lớp cha. Sử dụng :c:func:`PyObject_GetTypeData` để lấy con trỏ đến vùng nhớ dành riêng cho lớp con theo cách này. Với :c:member:`!basicsize` âm, Python sẽ chèn phần đệm khi cần để đáp ứng các yêu cầu căn chỉnh của :c:member:`~PyTypeObject.tp_basicsize`.

      .. versionchanged:: 3.12

         Trước đây, trường này không thể nhận giá trị âm.

   .. c:member:: int itemsize

      Kích thước tính theo byte của một phần tử thuộc kiểu có kích thước biến đổi. Được dùng để thiết lập :c:member:`PyTypeObject.tp_itemsize`. Xem tài liệu ``tp_itemsize`` để biết các lưu ý.

      Nếu bằng không, :c:member:`~PyTypeObject.tp_itemsize` sẽ được kế thừa. Việc mở rộng các lớp có kích thước biến đổi tùy ý rất nguy hiểm, vì một số kiểu sử dụng độ lệch cố định cho vùng nhớ có kích thước biến đổi, và vùng này có thể chồng lấn lên vùng nhớ có kích thước cố định được lớp con sử dụng. Để giúp ngăn ngừa sai sót, chỉ có thể kế thừa ``itemsize`` trong các trường hợp sau:

      - Lớp cơ sở không có kích thước biến đổi (giá trị của nó
        :c:member:`~PyTypeObject.tp_itemsize` bằng không).
      - :c:member:`PyType_Spec.basicsize` được yêu cầu có giá trị dương, cho thấy bố cục bộ nhớ của lớp cơ sở đã được biết.
      - :c:member:`PyType_Spec.basicsize` được yêu cầu có giá trị bằng không, cho thấy lớp con không truy cập trực tiếp vào bộ nhớ của thực thể.
      - Với cờ :c:macro:`Py_TPFLAGS_ITEMS_AT_END`.

   .. c:member:: unsigned int flags

      Các cờ kiểu, được dùng để thiết lập :c:member:`PyTypeObject.tp_flags`.

      Nếu cờ ``Py_TPFLAGS_HEAPTYPE`` chưa được thiết lập,
      :c:func:`PyType_FromSpecWithBases` sẽ tự động thiết lập cờ này.

   .. c:member:: PyType_Slot *slots

      Mảng các cấu trúc :c:type:`PyType_Slot`. Kết thúc bằng giá trị khe đặc biệt ``{0, NULL}``.

      Mỗi slot ID chỉ nên được chỉ định nhiều nhất một lần.

.. raw:: html

   <!-- Keep old URL fragments working (see gh-97908) -->
   <span id='c.PyType_Slot.PyType_Slot.slot'></span>
   <span id='c.PyType_Slot.PyType_Slot.pfunc'></span>

.. c:type:: PyType_Slot

   Cấu trúc xác định chức năng tùy chọn của một kiểu, chứa slot ID và con trỏ giá trị.

   .. c:member:: int slot

      Một slot ID.

      Slot ID được đặt tên giống như tên trường của các cấu trúc
      :c:type:`PyTypeObject`, :c:type:`PyNumberMethods`,
      :c:type:`PySequenceMethods`, :c:type:`PyMappingMethods` và
      :c:type:`PyAsyncMethods` với tiền tố ``Py_`` được thêm vào. Ví dụ, sử dụng:

      * :c:data:`Py_tp_dealloc` để thiết lập :c:member:`PyTypeObject.tp_dealloc`
      * :c:data:`Py_nb_add` để thiết lập :c:member:`PyNumberMethods.nb_add`
      * :c:data:`Py_sq_length` để thiết lập :c:member:`PySequenceMethods.sq_length`

      Một slot bổ sung được hỗ trợ nhưng không tương ứng với một
      :c:type:`!PyTypeObject` trường struct:

      * :c:data:`Py_tp_token`

      Các trường “offset” sau đây không thể được thiết lập bằng :c:type:`PyType_Slot`:

      * :c:member:`~PyTypeObject.tp_weaklistoffset` (hãy sử dụng :c:macro:`Py_TPFLAGS_MANAGED_WEAKREF` thay thế nếu có thể)
      * :c:member:`~PyTypeObject.tp_dictoffset` (hãy sử dụng :c:macro:`Py_TPFLAGS_MANAGED_DICT` thay thế nếu có thể)
      * :c:member:`~PyTypeObject.tp_vectorcall_offset` (sử dụng ``"__vectorcalloffset__"`` trong
        :ref:`PyMemberDef <pymemberdef-offsets>`)

      Nếu không thể chuyển sang cờ ``MANAGED`` (ví dụ: đối với vectorcall hoặc để hỗ trợ Python cũ hơn 3.12), hãy chỉ định offset trong :c:data:`Py_tp_members`. Xem :ref:`tài liệu PyMemberDef <pymemberdef-offsets>` để biết chi tiết.

      Không thể đặt các trường nội bộ sau đây khi tạo heap type:

      * :c:member:`~PyTypeObject.tp_dict`,
        :c:member:`~PyTypeObject.tp_mro`,
        :c:member:`~PyTypeObject.tp_cache`,
        :c:member:`~PyTypeObject.tp_subclasses`, và
        :c:member:`~PyTypeObject.tp_weaklist`.

      Việc thiết lập :c:data:`Py_tp_bases` hoặc :c:data:`Py_tp_base` có thể gây ra vấn đề trên một số nền tảng. Để tránh sự cố, hãy sử dụng đối số *bases* của
      :c:func:`PyType_FromSpecWithBases` thay vào đó.

      .. versionchanged:: 3.9
         Các slot trong :c:type:`PyBufferProcs` có thể được thiết lập trong unlimited API.

      .. versionchanged:: 3.11
         :c:member:`~PyBufferProcs.bf_getbuffer` and
         :c:member:`~PyBufferProcs.bf_releasebuffer` are now available
         trong :ref:`limited API <limited-c-api>`.

      .. versionchanged:: 3.14
         Trường :c:member:`~PyTypeObject.tp_vectorcall` hiện có thể được thiết lập bằng :c:data:`Py_tp_vectorcall`.  Xem tài liệu về trường này để biết chi tiết.

   .. c:member:: void *pfunc

      Giá trị mong muốn của slot. Trong hầu hết các trường hợp, đây là một con trỏ đến một hàm.

      Các giá trị *pfunc* không được ``NULL``, ngoại trừ các slot sau:

      * :c:data:`Py_tp_doc`
      * :c:data:`Py_tp_token` (để rõ ràng, hãy ưu tiên :c:data:`Py_TP_USE_SPEC` thay vì ``NULL``)


.. c:macro:: Py_tp_token

   Một :c:member:`~PyType_Slot.slot` ghi lại ID bố cục bộ nhớ tĩnh cho một lớp.

   Nếu :c:type:`PyType_Spec` của lớp được cấp phát tĩnh, token có thể được đặt theo đặc tả bằng giá trị đặc biệt
   :c:data:`Py_TP_USE_SPEC`:

   .. code-block:: c

      static PyType_Slot foo_slots[] = {
         {Py_tp_token, Py_TP_USE_SPEC},

   Nó cũng có thể được đặt thành một con trỏ tùy ý, nhưng bạn phải đảm bảo rằng:

   * Con trỏ tồn tại lâu hơn lớp, vì vậy nó không được tái sử dụng cho mục đích khác trong khi lớp còn tồn tại.
   * Nó “thuộc về” module mở rộng nơi lớp được định nghĩa, để không xung đột với các extension khác.

   Sử dụng :c:func:`PyType_GetBaseByToken` để kiểm tra xem superclass của một lớp có token đã cho hay không -- tức là kiểm tra xem layout bộ nhớ có tương thích hay không.

   Để lấy token cho một lớp nhất định (không xét các superclass), hãy sử dụng :c:func:`PyType_GetSlot` với ``Py_tp_token``.

   .. versionadded:: 3.14

   .. c:namespace:: NULL

   .. c:macro:: Py_TP_USE_SPEC

      Được sử dụng làm giá trị với :c:data:`Py_tp_token` để đặt token thành :c:type:`PyType_Spec` của lớp. Mở rộng thành ``NULL``.

      .. versionadded:: 3.14
