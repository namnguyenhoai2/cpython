.. highlight:: c

.. _marshalling-utils:

Hỗ trợ marshalling dữ liệu
==========================

Các routine này cho phép mã C làm việc với các đối tượng đã được tuần tự hóa bằng cùng định dạng dữ liệu như module :mod:`marshal`. Có các hàm để ghi dữ liệu vào định dạng tuần tự hóa, cùng các hàm bổ sung có thể dùng để đọc lại dữ liệu. Các tệp dùng để lưu trữ dữ liệu đã được marshal phải được mở ở chế độ nhị phân.

Các giá trị số được lưu với byte có ý nghĩa thấp nhất ở trước.

Module hỗ trợ một số phiên bản của định dạng dữ liệu; xem tài liệu module :py:mod:`Python <marshal>` để biết chi tiết.

.. c:macro:: Py_MARSHAL_VERSION

   Phiên bản định dạng hiện tại. Xem :py:data:`marshal.version`.

.. c:function:: void PyMarshal_WriteLongToFile(long value, FILE *file, int version)

   Marshal một số nguyên :c:expr:`long`, *value*, vào *file*. Thao tác này chỉ ghi 32 bit có ý nghĩa thấp nhất của *value*, bất kể kích thước của kiểu :c:expr:`long` gốc. *version* cho biết định dạng tệp.

   Hàm này có thể không thành công; trong trường hợp đó, hàm sẽ đặt chỉ báo lỗi. Dùng :c:func:`PyErr_Occurred` để kiểm tra điều đó.

.. c:function:: void PyMarshal_WriteObjectToFile(PyObject *value, FILE *file, int version)

   Marshal một đối tượng Python, *value*, vào *file*. *version* cho biết định dạng tệp.

   Hàm này có thể không thành công; trong trường hợp đó, hàm sẽ đặt chỉ báo lỗi. Dùng :c:func:`PyErr_Occurred` để kiểm tra điều đó.

.. c:function:: PyObject* PyMarshal_WriteObjectToString(PyObject *value, int version)

   Trả về một đối tượng bytes chứa biểu diễn đã được marshal của *value*. *version* cho biết định dạng tệp.


Các hàm sau đây cho phép đọc lại những giá trị đã được marshal.


.. c:function:: long PyMarshal_ReadLongFromFile(FILE *file)

   Trả về một :c:expr:`long` C từ luồng dữ liệu trong :c:expr:`FILE*` được mở để đọc. Chỉ có thể đọc một giá trị 32-bit bằng hàm này, bất kể kích thước native của :c:expr:`long`.

   Khi xảy ra lỗi, đặt ngoại lệ thích hợp (:exc:`EOFError`) và trả về ``-1``.


.. c:function:: int PyMarshal_ReadShortFromFile(FILE *file)

   Trả về một :c:expr:`short` C từ luồng dữ liệu trong :c:expr:`FILE*` được mở để đọc. Chỉ có thể đọc một giá trị 16-bit bằng hàm này, bất kể kích thước native của :c:expr:`short`.

   Khi xảy ra lỗi, đặt ngoại lệ thích hợp (:exc:`EOFError`) và trả về ``-1``.


.. c:function:: PyObject* PyMarshal_ReadObjectFromFile(FILE *file)

   Trả về một đối tượng Python từ luồng dữ liệu trong một :c:expr:`FILE*` được mở để đọc.

   Khi xảy ra lỗi, đặt ngoại lệ thích hợp (:exc:`EOFError`, :exc:`ValueError` hoặc :exc:`TypeError`) và trả về ``NULL``.


.. c:function:: PyObject* PyMarshal_ReadLastObjectFromFile(FILE *file)

   Trả về một đối tượng Python từ luồng dữ liệu trong một :c:expr:`FILE*` được mở để đọc. Không giống như :c:func:`PyMarshal_ReadObjectFromFile`, hàm này giả định rằng sẽ không đọc thêm đối tượng nào từ tệp, cho phép tải mạnh tay dữ liệu tệp vào bộ nhớ để quá trình giải tuần tự hóa có thể hoạt động trên dữ liệu trong bộ nhớ thay vì đọc từng byte một từ tệp. Chỉ sử dụng biến thể này nếu bạn chắc chắn rằng sẽ không đọc thêm bất kỳ thứ gì từ tệp.

   Khi xảy ra lỗi, đặt ngoại lệ thích hợp (:exc:`EOFError`, :exc:`ValueError` hoặc :exc:`TypeError`) và trả về ``NULL``.


.. c:function:: PyObject* PyMarshal_ReadObjectFromString(const char *data, Py_ssize_t len)

   Trả về một đối tượng Python từ luồng dữ liệu trong bộ đệm byte chứa *len* byte được trỏ tới bởi *data*.

   Khi xảy ra lỗi, đặt ngoại lệ thích hợp (:exc:`EOFError`, :exc:`ValueError` hoặc :exc:`TypeError`) và trả về ``NULL``.

