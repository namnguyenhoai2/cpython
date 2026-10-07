.. highlight:: c

.. _allocating-objects:

Phân bổ đối tượng trên heap
===========================


.. c:function:: PyObject* _PyObject_New(PyTypeObject *type)


.. c:function:: PyVarObject* _PyObject_NewVar(PyTypeObject *type, Py_ssize_t size)


.. c:function:: PyObject* PyObject_Init(PyObject *op, PyTypeObject *type)

   Khởi tạo một đối tượng mới được cấp phát *op* với kiểu và tham chiếu ban đầu. Trả về đối tượng đã được khởi tạo. Các trường khác của đối tượng không được khởi tạo. Dù tên gọi là như vậy, hàm này không liên quan đến phương thức :meth:`~object.__init__` của đối tượng (:c:member:`~PyTypeObject.tp_init` slot). Cụ thể, hàm này **không** gọi
   phương thức :meth:`!__init__` của đối tượng.

   Nhìn chung, hãy xem hàm này là một routine cấp thấp. Hãy sử dụng
   :c:member:`~PyTypeObject.tp_alloc` khi có thể. Để triển khai :c:member:`!tp_alloc` cho kiểu của bạn, hãy ưu tiên
   :c:func:`PyType_GenericAlloc` hoặc :c:func:`PyObject_New`.

   .. note::

      Hàm này chỉ khởi tạo phần bộ nhớ của đối tượng tương ứng với cấu trúc :c:type:`PyObject` ban đầu. Nó không đặt phần còn lại về 0.


.. c:function:: PyVarObject* PyObject_InitVar(PyVarObject *op, PyTypeObject *type, Py_ssize_t size)

   Hàm này thực hiện mọi việc mà :c:func:`PyObject_Init` thực hiện, đồng thời khởi tạo thông tin về độ dài cho một đối tượng có kích thước biến đổi.

   .. note::

      Hàm này chỉ khởi tạo một phần bộ nhớ của đối tượng. Nó không đặt phần còn lại về không.


.. c:macro:: PyObject_New(TYPE, typeobj)

   Cấp phát một đối tượng Python mới bằng cách sử dụng kiểu cấu trúc C *TYPE* và đối tượng kiểu Python *typeobj* (``PyTypeObject*``) bằng cách gọi
   :c:func:`PyObject_Malloc` để cấp phát bộ nhớ và khởi tạo nó như sau
   :c:func:`PyObject_Init`. Bên gọi sẽ sở hữu tham chiếu duy nhất đến đối tượng (tức là số lượng tham chiếu của đối tượng sẽ là một).

   Tránh gọi trực tiếp hàm này để cấp phát bộ nhớ cho một đối tượng; thay vào đó, hãy gọi
   slot :c:member:`~PyTypeObject.tp_alloc` của kiểu.

   Khi điền vào slot :c:member:`~PyTypeObject.tp_alloc` của một type,
   nên ưu tiên :c:func:`PyType_GenericAlloc` thay vì một hàm tùy chỉnh chỉ đơn giản gọi macro này.

   Macro này không gọi :c:member:`~PyTypeObject.tp_alloc`,
   :c:member:`~PyTypeObject.tp_new` (:meth:`~object.__new__`), hoặc
   :c:member:`~PyTypeObject.tp_init` (:meth:`~object.__init__`).

   Không thể sử dụng cách này cho các object có :c:macro:`Py_TPFLAGS_HAVE_GC` được đặt trong
   :c:member:`~PyTypeObject.tp_flags`; thay vào đó, hãy sử dụng :c:macro:`PyObject_GC_New`.

   Bộ nhớ được cấp phát bởi macro này phải được giải phóng bằng :c:func:`PyObject_Free` (thường được gọi thông qua slot :c:member:`~PyTypeObject.tp_free` của object).

   .. note::

      Bộ nhớ được trả về không được đảm bảo là đã được đặt về không hoàn toàn trước khi được khởi tạo.

   .. note::

      Macro này không tạo một đối tượng thuộc kiểu đã cho được khởi tạo đầy đủ; nó chỉ cấp phát bộ nhớ và chuẩn bị bộ nhớ đó để :c:member:`~PyTypeObject.tp_init` tiếp tục khởi tạo.  Để tạo một đối tượng được khởi tạo đầy đủ, hãy gọi *typeobj* thay vào đó.  Ví dụ::

         PyObject *foo = PyObject_CallNoArgs((PyObject *)&PyFoo_Type);

   .. seealso::

      * :c:func:`PyObject_Free`
      * :c:macro:`PyObject_GC_New`
      * :c:func:`PyType_GenericAlloc`
      * :c:member:`~PyTypeObject.tp_alloc`


.. c:macro:: PyObject_NewVar(TYPE, typeobj, size)

   Tương tự như :c:macro:`PyObject_New`, ngoại trừ:

   * Nó cấp phát đủ bộ nhớ cho cấu trúc *TYPE* cộng với *size* (``Py_ssize_t``) trường có kích thước được chỉ định bởi
     :c:member:`~PyTypeObject.tp_itemsize` của *typeobj*.
   * Bộ nhớ được khởi tạo giống như :c:func:`PyObject_InitVar`.

   Điều này hữu ích khi triển khai các đối tượng như tuple, vốn có thể xác định kích thước của chúng tại thời điểm xây dựng.  Việc nhúng mảng các trường vào cùng một vùng cấp phát giúp giảm số lần cấp phát, từ đó cải thiện hiệu quả quản lý bộ nhớ.

   Tránh gọi trực tiếp hàm này để cấp phát bộ nhớ cho một đối tượng; thay vào đó, hãy gọi
   slot :c:member:`~PyTypeObject.tp_alloc` của kiểu.

   Khi điền vào slot :c:member:`~PyTypeObject.tp_alloc` của một type,
   nên ưu tiên :c:func:`PyType_GenericAlloc` thay vì một hàm tùy chỉnh chỉ đơn giản gọi macro này.

   Không thể sử dụng cách này cho các object có :c:macro:`Py_TPFLAGS_HAVE_GC` được đặt trong
   :c:member:`~PyTypeObject.tp_flags`; thay vào đó, hãy sử dụng :c:macro:`PyObject_GC_NewVar`.

   Vùng nhớ được cấp phát bởi hàm này phải được giải phóng bằng :c:func:`PyObject_Free` (thường được gọi thông qua slot :c:member:`~PyTypeObject.tp_free` của đối tượng).

   .. note::

      Bộ nhớ được trả về không được đảm bảo là đã được đặt về không hoàn toàn trước khi được khởi tạo.

   .. note::

      Macro này không tạo một đối tượng thuộc kiểu đã cho được khởi tạo đầy đủ; nó chỉ cấp phát bộ nhớ và chuẩn bị bộ nhớ đó để :c:member:`~PyTypeObject.tp_init` tiếp tục khởi tạo.  Để tạo một đối tượng được khởi tạo đầy đủ, hãy gọi *typeobj* thay vào đó.  Ví dụ::

         PyObject *list_instance = PyObject_CallNoArgs((PyObject *)&PyList_Type);

   .. seealso::

      * :c:func:`PyObject_Free`
      * :c:macro:`PyObject_GC_NewVar`
      * :c:func:`PyType_GenericAlloc`
      * :c:member:`~PyTypeObject.tp_alloc`


.. c:var:: PyObject _Py_NoneStruct

   Đối tượng hiển thị trong Python dưới dạng ``None``. Chỉ được truy cập đối tượng này bằng macro :c:macro:`Py_None`, macro này trả về một con trỏ tới đối tượng.


.. seealso::

   :ref:`moduleobjects`
      Để cấp phát và tạo các module mở rộng.


Các bí danh đã được đánh dấu không còn khuyến nghị sử dụng
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. soft-deprecated:: 3.10

Đây là các bí danh của những hàm và macro hiện có. Chúng chỉ tồn tại để đảm bảo khả năng tương thích ngược.


.. list-table::
   :widths: auto
   :header-rows: 1

   * * Bí danh đã được đánh dấu không còn khuyến nghị sử dụng
     * Hàm
   * * .. c:macro:: PyObject_NEW(type, typeobj)
     * :c:macro:`PyObject_New`
   * * .. c:macro:: PyObject_NEW_VAR(type, typeobj, n)
     * :c:macro:`PyObject_NewVar`
   * * .. c:macro:: PyObject_INIT(op, typeobj)
     * :c:func:`PyObject_Init`
   * * .. c:macro:: PyObject_INIT_VAR(op, typeobj, n)
     * :c:func:`PyObject_InitVar`
   * * .. c:macro:: PyObject_MALLOC(n)
     * :c:func:`PyObject_Malloc`
   * * .. c:macro:: PyObject_REALLOC(p, n)
     * :c:func:`PyObject_Realloc`
   * * .. c:macro:: PyObject_FREE(p)
     * :c:func:`PyObject_Free`
   * * .. c:macro:: PyObject_DEL(p)
     * :c:func:`PyObject_Free`
   * * .. c:macro:: PyObject_Del(p)
     * :c:func:`PyObject_Free`
