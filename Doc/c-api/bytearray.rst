.. highlight:: c

.. _bytearrayobjects:

Đối tượng mảng byte
-------------------

.. index:: pair: object; bytearray


.. c:type:: PyByteArrayObject

   Kiểu con này của :c:type:`PyObject` đại diện cho một đối tượng bytearray của Python.

   .. impl-detail::

      Bộ đệm nội bộ của :c:type:`PyByteArrayObject` luôn bao gồm thêm một byte null ở cuối để tương thích với các chuỗi C kết thúc bằng null. Byte bổ sung này không được tính trong :c:func:`PyByteArray_Size` cũng như trong các đối số *len* của các hàm bên dưới.

.. c:var:: PyTypeObject PyByteArray_Type

   Thể hiện này của :c:type:`PyTypeObject` đại diện cho kiểu bytearray của Python; nó là cùng một đối tượng với :class:`bytearray` ở lớp Python.


Macro kiểm tra kiểu
^^^^^^^^^^^^^^^^^^^

.. c:function:: int PyByteArray_Check(PyObject *o)

   Trả về true nếu đối tượng *o* là một đối tượng bytearray hoặc là một thể hiện của kiểu con của kiểu bytearray. Hàm này luôn thành công.


.. c:function:: int PyByteArray_CheckExact(PyObject *o)

   Trả về true nếu đối tượng *o* là một đối tượng bytearray, nhưng không phải là một thể hiện của kiểu con của kiểu bytearray. Hàm này luôn thành công.


Các hàm API trực tiếp
^^^^^^^^^^^^^^^^^^^^^

.. c:function:: PyObject* PyByteArray_FromObject(PyObject *o)

   Trả về một đối tượng bytearray mới từ bất kỳ đối tượng nào, *o*, triển khai
   :ref:`buffer protocol <bufferobjects>`.

   Khi xảy ra lỗi, trả về ``NULL`` cùng với một ngoại lệ đã được thiết lập.

   .. note::
      Nếu đối tượng triển khai buffer protocol, thì buffer không được thay đổi trong khi đối tượng bytearray đang được tạo.


.. c:function:: PyObject* PyByteArray_FromStringAndSize(const char *string, Py_ssize_t len)

   Tạo một đối tượng bytearray mới từ *string* và độ dài của nó, *len*.

   Khi xảy ra lỗi, trả về ``NULL`` cùng với một ngoại lệ đã được thiết lập.


.. c:function:: PyObject* PyByteArray_Concat(PyObject *a, PyObject *b)

   Nối các bytearray *a* và *b*, rồi trả về một bytearray mới chứa kết quả.

   Khi xảy ra lỗi, trả về ``NULL`` cùng với một ngoại lệ đã được thiết lập.

   .. note::
      Nếu đối tượng triển khai buffer protocol, thì buffer không được thay đổi trong khi đối tượng bytearray đang được tạo.


.. c:function:: Py_ssize_t PyByteArray_Size(PyObject *bytearray)

   Trả về kích thước của *bytearray* sau khi kiểm tra một ``NULL`` pointer.


.. c:function:: char* PyByteArray_AsString(PyObject *bytearray)

   Trả về nội dung của *bytearray* dưới dạng một mảng char sau khi kiểm tra một ``NULL`` pointer. Mảng được trả về luôn có thêm một byte null ở cuối.

   .. note::
      Không an toàn cho thread khi thay đổi đối tượng bytearray trong lúc sử dụng mảng char được trả về.


.. c:function:: int PyByteArray_Resize(PyObject *bytearray, Py_ssize_t len)

   Thay đổi kích thước buffer nội bộ của *bytearray* thành *len*. Nếu thất bại, hàm trả về ``-1`` và đặt một exception.

   .. versionchanged:: 3.14
      Giá trị *len* âm giờ đây sẽ khiến một exception được thiết lập và trả về -1.


Macro
^^^^^

Các macro này đánh đổi tính an toàn để lấy tốc độ và không kiểm tra pointer.

.. c:function:: char* PyByteArray_AS_STRING(PyObject *bytearray)

   Tương tự :c:func:`PyByteArray_AsString`, nhưng không kiểm tra lỗi.

   .. note::
      Không an toàn luồng khi thay đổi đối tượng bytearray trong lúc sử dụng mảng char được trả về.


.. c:function:: Py_ssize_t PyByteArray_GET_SIZE(PyObject *bytearray)

   Tương tự :c:func:`PyByteArray_Size`, nhưng không kiểm tra lỗi.
