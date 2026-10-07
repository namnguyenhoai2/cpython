.. highlight:: c

.. _memoryview-objects:

.. index::
   pair: object; memoryview

Các đối tượng MemoryView
------------------------

Một đối tượng :class:`memoryview` cung cấp giao diện :ref:`buffer ở cấp C <bufferobjects>` dưới dạng một đối tượng Python, sau đó có thể được truyền qua lại như mọi đối tượng khác.


.. c:var:: PyTypeObject PyMemoryView_Type

   Instance này của :c:type:`PyTypeObject` đại diện cho kiểu memoryview của Python. Đây chính là đối tượng :class:`memoryview` ở lớp Python.


.. c:function:: PyObject *PyMemoryView_FromObject(PyObject *obj)

   Tạo một đối tượng memoryview từ một đối tượng cung cấp giao diện buffer. Nếu *obj* hỗ trợ xuất buffer có thể ghi, đối tượng memoryview sẽ cho phép đọc/ghi; nếu không, đối tượng có thể chỉ cho phép đọc hoặc cho phép đọc/ghi, tùy theo quyết định của bên xuất.


.. c:macro:: PyBUF_READ

   Cờ yêu cầu buffer chỉ đọc.


.. c:macro:: PyBUF_WRITE

   Cờ yêu cầu buffer có thể ghi.


.. c:function:: PyObject *PyMemoryView_FromMemory(char *mem, Py_ssize_t size, int flags)

   Tạo một đối tượng memoryview sử dụng *mem* làm buffer nền. *flags* có thể là :c:macro:`PyBUF_READ` hoặc :c:macro:`PyBUF_WRITE`.

   .. versionadded:: 3.3

.. c:function:: PyObject *PyMemoryView_FromBuffer(const Py_buffer *view)

   Tạo một đối tượng memoryview bao bọc cấu trúc bộ đệm đã cho *view*. Đối với các bộ đệm byte đơn giản, :c:func:`PyMemoryView_FromMemory` là hàm được ưu tiên.

.. c:function:: PyObject *PyMemoryView_GetContiguous(PyObject *obj, int buffertype, char order)

   Tạo một đối tượng memoryview trỏ đến một :term:`contiguous` khối bộ nhớ (theo thứ tự 'C' hoặc 'Fortran *thứ tự*) từ một đối tượng định nghĩa buffer interface. Nếu bộ nhớ liên tục, đối tượng memoryview trỏ đến vùng bộ nhớ ban đầu. Nếu không, một bản sao được tạo và memoryview trỏ đến một đối tượng bytes mới.

   *buffertype* có thể là :c:macro:`PyBUF_READ` hoặc :c:macro:`PyBUF_WRITE`.


.. c:function:: int PyMemoryView_Check(PyObject *obj)

   Trả về true nếu đối tượng *obj* là một đối tượng memoryview. Hiện tại không được phép tạo các lớp con của :class:`memoryview`. Hàm này luôn thành công.


.. c:function:: Py_buffer *PyMemoryView_GET_BUFFER(PyObject *mview)

   Trả về một con trỏ đến bản sao riêng của memoryview đối với bộ đệm của exporter. *mview* **must** là một instance của memoryview; macro này không kiểm tra kiểu của nó, bạn phải tự thực hiện việc đó, nếu không sẽ có nguy cơ gây lỗi.

.. c:function:: PyObject *PyMemoryView_GET_BASE(PyObject *mview)

   Trả về một con trỏ đến đối tượng exporting mà memoryview dựa trên hoặc ``NULL`` nếu memoryview được tạo bởi một trong các hàm
   :c:func:`PyMemoryView_FromMemory` hoặc :c:func:`PyMemoryView_FromBuffer`. *mview* **must** là một instance của memoryview.
