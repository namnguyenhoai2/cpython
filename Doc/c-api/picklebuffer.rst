.. highlight:: c

.. _picklebuffer-objects:

.. index::
   pair: object; PickleBuffer

Đối tượng bộ đệm pickle
-----------------------

.. versionadded:: 3.8

Một đối tượng :class:`pickle.PickleBuffer` bao bọc một :ref:`đối tượng cung cấp bộ đệm <bufferobjects>` để truyền dữ liệu ngoài băng với mô-đun :mod:`pickle`.


.. c:var:: PyTypeObject PyPickleBuffer_Type

   Instance này của :c:type:`PyTypeObject` đại diện cho kiểu bộ đệm pickle của Python. Đây là cùng một đối tượng với :class:`pickle.PickleBuffer` trong lớp Python.


.. c:function:: int PyPickleBuffer_Check(PyObject *op)

   Trả về true nếu *op* là một instance bộ đệm pickle. Hàm này luôn thành công.


.. c:function:: PyObject *PyPickleBuffer_FromObject(PyObject *obj)

   Tạo một bộ đệm pickle từ đối tượng *obj*.

   Hàm này sẽ thất bại nếu *obj* không hỗ trợ :ref:`giao thức bộ đệm <bufferobjects>`.

   Khi thành công, trả về một instance bộ đệm pickle mới. Khi thất bại, đặt một ngoại lệ và trả về ``NULL``.

   Tương tự như việc gọi :class:`pickle.PickleBuffer` với *obj* trong Python.


.. c:function:: const Py_buffer *PyPickleBuffer_GetBuffer(PyObject *picklebuf)

   Lấy con trỏ tới :c:type:`Py_buffer` bên dưới mà pickle buffer bao bọc.

   Con trỏ được trả về hợp lệ miễn là *picklebuf* vẫn tồn tại và chưa được giải phóng. Bên gọi không được sửa đổi hoặc giải phóng :c:type:`Py_buffer` được trả về. Nếu pickle buffer đã được giải phóng, hãy phát sinh :exc:`ValueError`.

   Khi thành công, trả về con trỏ tới buffer view. Khi thất bại, đặt một exception và trả về ``NULL``.


.. c:function:: int PyPickleBuffer_Release(PyObject *picklebuf)

   Giải phóng buffer bên dưới được pickle buffer giữ.

   Trả về ``0`` khi thành công. Khi thất bại, đặt một exception và trả về ``-1``.

   Tương tự như việc gọi :meth:`pickle.PickleBuffer.release` trong Python.
