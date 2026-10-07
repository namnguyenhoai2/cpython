.. highlight:: c

.. _datetimeobjects:

Đối tượng DateTime
------------------

Mô-đun :mod:`datetime` cung cấp nhiều đối tượng ngày và giờ. Trước khi sử dụng bất kỳ hàm nào trong số này, phải đưa tệp tiêu đề :file:`datetime.h` vào mã nguồn của bạn (lưu ý rằng tệp này không được đưa vào bởi :file:`Python.h`), đồng thời phải gọi macro :c:macro:`PyDateTime_IMPORT`, thường là một phần của hàm khởi tạo mô-đun. Macro này đặt một con trỏ tới cấu trúc C vào biến tĩnh :c:data:`PyDateTimeAPI`, được các macro sau sử dụng.

.. c:macro:: PyDateTime_IMPORT()

   Import C API của datetime.

   Khi thành công, điền con trỏ :c:var:`PyDateTimeAPI`. Khi thất bại, đặt :c:var:`PyDateTimeAPI` thành ``NULL`` và đặt một exception. Caller phải kiểm tra xem có xảy ra lỗi hay không thông qua :c:func:`PyErr_Occurred`:

   .. code-block::

      PyDateTime_IMPORT;
      if (PyErr_Occurred()) { /* cleanup */ }

   .. warning::

      Điều này không tương thích với subinterpreter.

.. c:type:: PyDateTime_CAPI

   Cấu trúc chứa các trường cho C API của datetime.

   Các trường của cấu trúc này là private và có thể thay đổi.

   Không sử dụng trực tiếp đối tượng này; thay vào đó, hãy ưu tiên các API ``PyDateTime_*``.

.. c:var:: PyDateTime_CAPI *PyDateTimeAPI

   Đối tượng được cấp phát động, chứa C API cho datetime.

   Biến này chỉ khả dụng sau khi :c:macro:`PyDateTime_IMPORT` thành công.

.. c:type:: PyDateTime_Date

   Kiểu con này của :c:type:`PyObject` biểu diễn một đối tượng date của Python.

.. c:type:: PyDateTime_DateTime

   Kiểu con này của :c:type:`PyObject` biểu diễn một đối tượng datetime của Python.

.. c:type:: PyDateTime_Time

   Kiểu con này của :c:type:`PyObject` biểu diễn một đối tượng time của Python.

.. c:type:: PyDateTime_Delta

   Kiểu con này của :c:type:`PyObject` biểu diễn sự chênh lệch giữa hai giá trị datetime.

.. c:var:: PyTypeObject PyDateTime_DateType

   Instance này của :c:type:`PyTypeObject` biểu thị kiểu date của Python; đây là cùng một đối tượng với :class:`datetime.date` trong lớp Python.

.. c:var:: PyTypeObject PyDateTime_DateTimeType

   Instance này của :c:type:`PyTypeObject` biểu thị kiểu datetime của Python; đây là cùng một đối tượng với :class:`datetime.datetime` trong lớp Python.

.. c:var:: PyTypeObject PyDateTime_TimeType

   Instance này của :c:type:`PyTypeObject` biểu thị kiểu time của Python; đây là cùng một đối tượng với :class:`datetime.time` trong lớp Python.

.. c:var:: PyTypeObject PyDateTime_DeltaType

   Instance này của :c:type:`PyTypeObject` biểu thị kiểu Python cho độ chênh lệch giữa hai giá trị datetime; đây là cùng một đối tượng với :class:`datetime.timedelta` trong lớp Python.

.. c:var:: PyTypeObject PyDateTime_TZInfoType

   Instance này của :c:type:`PyTypeObject` biểu thị kiểu thông tin múi giờ của Python; đây là cùng một đối tượng với :class:`datetime.tzinfo` trong lớp Python.


Macro để truy cập singleton UTC:

.. c:var:: PyObject* PyDateTime_TimeZone_UTC

   Trả về singleton múi giờ biểu thị UTC, cùng một đối tượng với
   :attr:`datetime.timezone.utc`.

   .. versionadded:: 3.7


Macro kiểm tra kiểu:

.. c:function:: int PyDate_Check(PyObject *ob)

   Trả về true nếu *ob* có kiểu :c:data:`PyDateTime_DateType` hoặc một kiểu con của kiểu đó
   :c:data:`!PyDateTime_DateType`.  *ob* không được là ``NULL``.  Hàm này luôn thành công.


.. c:function:: int PyDate_CheckExact(PyObject *ob)

   Trả về true nếu *ob* có kiểu :c:data:`PyDateTime_DateType`. *ob* không được là ``NULL``.  Hàm này luôn thành công.


.. c:function:: int PyDateTime_Check(PyObject *ob)

   Trả về true nếu *ob* có kiểu :c:data:`PyDateTime_DateTimeType` hoặc một kiểu con của kiểu đó
   :c:data:`!PyDateTime_DateTimeType`.  *ob* không được là ``NULL``.  Hàm này luôn thành công.


.. c:function:: int PyDateTime_CheckExact(PyObject *ob)

   Trả về true nếu *ob* có kiểu :c:data:`PyDateTime_DateTimeType`. *ob* không được là ``NULL``.  Hàm này luôn thành công.


.. c:function:: int PyTime_Check(PyObject *ob)

   Trả về true nếu *ob* thuộc kiểu :c:data:`PyDateTime_TimeType` hoặc một kiểu con của
   :c:data:`!PyDateTime_TimeType`.  *ob* không được là ``NULL``.  Hàm này luôn thực thi thành công.


.. c:function:: int PyTime_CheckExact(PyObject *ob)

   Trả về true nếu *ob* thuộc kiểu :c:data:`PyDateTime_TimeType`. *ob* không được là ``NULL``.  Hàm này luôn thực thi thành công.


.. c:function:: int PyDelta_Check(PyObject *ob)

   Trả về true nếu *ob* thuộc kiểu :c:data:`PyDateTime_DeltaType` hoặc một kiểu con của
   :c:data:`!PyDateTime_DeltaType`.  *ob* không được là ``NULL``.  Hàm này luôn thực thi thành công.


.. c:function:: int PyDelta_CheckExact(PyObject *ob)

   Trả về true nếu *ob* thuộc kiểu :c:data:`PyDateTime_DeltaType`. *ob* không được là ``NULL``.  Hàm này luôn thực thi thành công.


.. c:function:: int PyTZInfo_Check(PyObject *ob)

   Trả về true nếu *ob* thuộc kiểu :c:data:`PyDateTime_TZInfoType` hoặc một kiểu con của
   :c:data:`!PyDateTime_TZInfoType`.  *ob* không được là ``NULL``.  Hàm này luôn thành công.


.. c:function:: int PyTZInfo_CheckExact(PyObject *ob)

   Trả về true nếu *ob* thuộc kiểu :c:data:`PyDateTime_TZInfoType`. *ob* không được là ``NULL``.  Hàm này luôn thành công.


Các macro để tạo object:

.. c:function:: PyObject* PyDate_FromDate(int year, int month, int day)

   Trả về một object :class:`datetime.date` với năm, tháng và ngày được chỉ định.


.. c:function:: PyObject* PyDateTime_FromDateAndTime(int year, int month, int day, int hour, int minute, int second, int usecond)

   Trả về một object :class:`datetime.datetime` với năm, tháng, ngày, giờ, phút, giây và microsecond được chỉ định.


.. c:function:: PyObject* PyDateTime_FromDateAndTimeAndFold(int year, int month, int day, int hour, int minute, int second, int usecond, int fold)

   Trả về một object :class:`datetime.datetime` với năm, tháng, ngày, giờ, phút, giây, microsecond và fold được chỉ định.

   .. versionadded:: 3.6


.. c:function:: PyObject* PyTime_FromTime(int hour, int minute, int second, int usecond)

   Trả về một object :class:`datetime.time` với giờ, phút, giây và microsecond được chỉ định.


.. c:function:: PyObject* PyTime_FromTimeAndFold(int hour, int minute, int second, int usecond, int fold)

   Trả về một đối tượng :class:`datetime.time` với giờ, phút, giây, microsecond và fold được chỉ định.

   .. versionadded:: 3.6


.. c:function:: PyObject* PyDelta_FromDSU(int days, int seconds, int useconds)

   Trả về một đối tượng :class:`datetime.timedelta` biểu diễn số ngày, giây và microsecond đã cho. Việc chuẩn hóa được thực hiện để số microsecond và giây thu được nằm trong các phạm vi được ghi lại cho
   các đối tượng :class:`datetime.timedelta`.


.. c:function:: PyObject* PyTimeZone_FromOffset(PyObject *offset)

   Trả về một đối tượng :class:`datetime.timezone` với offset cố định không có tên, được biểu diễn bằng đối số *offset*.

   .. versionadded:: 3.7


.. c:function:: PyObject* PyTimeZone_FromOffsetAndName(PyObject *offset, PyObject *name)

   Trả về một đối tượng :class:`datetime.timezone` với offset cố định được biểu diễn bằng đối số *offset* và có tzname là *name*.

   .. versionadded:: 3.7


Các macro để trích xuất các trường từ các đối tượng ngày tháng. Đối số phải là một thể hiện của
:c:type:`PyDateTime_Date`, bao gồm cả các lớp con (chẳng hạn như
:c:type:`PyDateTime_DateTime`). Đối số không được là ``NULL``, và kiểu không được kiểm tra:

.. c:function:: int PyDateTime_GET_YEAR(PyDateTime_Date *o)

   Trả về năm dưới dạng số nguyên dương.


.. c:function:: int PyDateTime_GET_MONTH(PyDateTime_Date *o)

   Trả về tháng dưới dạng số nguyên từ 1 đến 12.


.. c:function:: int PyDateTime_GET_DAY(PyDateTime_Date *o)

   Trả về ngày dưới dạng số nguyên từ 1 đến 31.


Các macro để trích xuất các trường từ các đối tượng datetime. Đối số phải là một thể hiện của :c:type:`PyDateTime_DateTime`, bao gồm cả các lớp con. Đối số không được là ``NULL``, và kiểu không được kiểm tra:

.. c:function:: int PyDateTime_DATE_GET_HOUR(PyDateTime_DateTime *o)

   Trả về giờ dưới dạng số nguyên từ 0 đến 23.


.. c:function:: int PyDateTime_DATE_GET_MINUTE(PyDateTime_DateTime *o)

   Trả về phút dưới dạng số nguyên từ 0 đến 59.


.. c:function:: int PyDateTime_DATE_GET_SECOND(PyDateTime_DateTime *o)

   Trả về giây, dưới dạng số nguyên từ 0 đến 59.


.. c:function:: int PyDateTime_DATE_GET_MICROSECOND(PyDateTime_DateTime *o)

   Trả về microsecond, dưới dạng số nguyên từ 0 đến 999999.


.. c:function:: int PyDateTime_DATE_GET_FOLD(PyDateTime_DateTime *o)

   Trả về fold, dưới dạng số nguyên từ 0 đến 1.

   .. versionadded:: 3.6


.. c:function:: PyObject* PyDateTime_DATE_GET_TZINFO(PyDateTime_DateTime *o)

   Trả về tzinfo (có thể là ``None``).

   .. versionadded:: 3.10


Các macro để trích xuất các trường từ các đối tượng thời gian. Đối số phải là một thể hiện của
:c:type:`PyDateTime_Time`, bao gồm cả các lớp con. Đối số không được là ``NULL``, và kiểu không được kiểm tra:

.. c:function:: int PyDateTime_TIME_GET_HOUR(PyDateTime_Time *o)

   Trả về giờ dưới dạng số nguyên từ 0 đến 23.


.. c:function:: int PyDateTime_TIME_GET_MINUTE(PyDateTime_Time *o)

   Trả về phút dưới dạng số nguyên từ 0 đến 59.


.. c:function:: int PyDateTime_TIME_GET_SECOND(PyDateTime_Time *o)

   Trả về giây, dưới dạng số nguyên từ 0 đến 59.


.. c:function:: int PyDateTime_TIME_GET_MICROSECOND(PyDateTime_Time *o)

   Trả về microsecond, dưới dạng số nguyên từ 0 đến 999999.


.. c:function:: int PyDateTime_TIME_GET_FOLD(PyDateTime_Time *o)

   Trả về fold, dưới dạng số nguyên từ 0 đến 1.

   .. versionadded:: 3.6


.. c:function:: PyObject* PyDateTime_TIME_GET_TZINFO(PyDateTime_Time *o)

   Trả về tzinfo (có thể là ``None``).

   .. versionadded:: 3.10


Các macro để trích xuất các trường từ đối tượng time delta. Đối số phải là một thể hiện của :c:type:`PyDateTime_Delta`, bao gồm cả các lớp con. Đối số không được là ``NULL``, và kiểu của đối số không được kiểm tra:

.. c:function:: int PyDateTime_DELTA_GET_DAYS(PyDateTime_Delta *o)

   Trả về số ngày dưới dạng int, trong khoảng từ -999999999 đến 999999999.

   .. versionadded:: 3.3


.. c:function:: int PyDateTime_DELTA_GET_SECONDS(PyDateTime_Delta *o)

   Trả về số giây dưới dạng int trong khoảng từ 0 đến 86399.

   .. versionadded:: 3.3


.. c:function:: int PyDateTime_DELTA_GET_MICROSECONDS(PyDateTime_Delta *o)

   Trả về số microgiây dưới dạng int trong khoảng từ 0 đến 999999.

   .. versionadded:: 3.3


Các macro nhằm tạo thuận tiện cho những module triển khai DB API:

.. c:function:: PyObject* PyDateTime_FromTimestamp(PyObject *args)

   Tạo và trả về một đối tượng :class:`datetime.datetime` mới với một tuple đối số phù hợp để truyền vào :meth:`datetime.datetime.fromtimestamp`.


.. c:function:: PyObject* PyDate_FromTimestamp(PyObject *args)

   Tạo và trả về một đối tượng :class:`datetime.date` mới với một tuple đối số phù hợp để truyền vào :meth:`datetime.date.fromtimestamp`.


Dữ liệu nội bộ
--------------

Các ký hiệu sau được C API cung cấp nhưng chỉ nên được xem là dành riêng cho nội bộ.

.. c:macro:: PyDateTime_CAPSULE_NAME

   Tên của datetime capsule cần truyền cho :c:func:`PyCapsule_Import`.

   Chỉ dùng nội bộ. Thay vào đó, hãy sử dụng :c:macro:`PyDateTime_IMPORT`.
