.. highlight:: c

.. _boolobjects:

Đối tượng Boolean
-----------------

Boolean trong Python được triển khai dưới dạng lớp con của số nguyên. Chỉ có hai giá trị boolean là :c:data:`Py_False` và :c:data:`Py_True`. Vì vậy, các hàm tạo và xóa thông thường không áp dụng cho boolean. Tuy nhiên, có các macro sau đây.


.. c:var:: PyTypeObject PyBool_Type

   Instance này của :c:type:`PyTypeObject` đại diện cho kiểu boolean của Python; nó là cùng một đối tượng với :class:`bool` ở tầng Python.


.. c:function:: int PyBool_Check(PyObject *o)

   Trả về true nếu *o* có kiểu :c:data:`PyBool_Type`. Hàm này luôn thành công.


.. c:var:: PyObject* Py_False

   Đối tượng ``False`` của Python. Đối tượng này không có phương thức và là
   :term:`immortal`.

   .. versionchanged:: 3.12
      :c:data:`Py_False` is :term:`immortal`.


.. c:var:: PyObject* Py_True

   Đối tượng ``True`` của Python. Đối tượng này không có phương thức và là
   :term:`immortal`.

   .. versionchanged:: 3.12
      :c:data:`Py_True` is :term:`immortal`.


.. c:macro:: Py_RETURN_FALSE

   Trả về :c:data:`Py_False` từ một hàm.


.. c:macro:: Py_RETURN_TRUE

   Trả về :c:data:`Py_True` từ một hàm.


.. c:function:: PyObject* PyBool_FromLong(long v)

   Trả về :c:data:`Py_True` hoặc :c:data:`Py_False`, tùy thuộc vào giá trị đúng/sai của *v*.
