.. highlight:: c

.. _coro-objects:

Đối tượng Coroutine
-------------------

.. versionadded:: 3.5

Các đối tượng coroutine là những gì các hàm được khai báo bằng từ khóa ``async`` trả về.


.. c:type:: PyCoroObject

   Cấu trúc C được sử dụng cho các đối tượng coroutine.


.. c:var:: PyTypeObject PyCoro_Type

   Đối tượng kiểu tương ứng với các đối tượng coroutine.


.. c:function:: int PyCoro_CheckExact(PyObject *ob)

   Trả về true nếu kiểu của *ob* là :c:type:`PyCoro_Type`; *ob* không được là ``NULL``. Hàm này luôn thành công.


.. c:function:: PyObject* PyCoro_New(PyFrameObject *frame, PyObject *name, PyObject *qualname)

   Tạo và trả về một đối tượng coroutine mới dựa trên đối tượng *frame*, với ``__name__`` và ``__qualname__`` được đặt thành *name* và *qualname*. Hàm này lấy đi một tham chiếu đến *frame*. Đối số *frame* không được là ``NULL``.
