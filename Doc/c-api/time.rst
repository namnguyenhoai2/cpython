.. highlight:: c

.. _c-api-time:

PyTime C API
============

.. versionadded:: 3.13

Clock C API cung cấp quyền truy cập vào các clock của hệ thống. API này tương tự như module Python :mod:`time`.

Để biết C API liên quan đến module :mod:`datetime`, hãy xem :ref:`datetimeobjects`.


Các kiểu dữ liệu
----------------

.. c:type:: PyTime_t

   Một timestamp hoặc duration tính bằng nanosecond, được biểu diễn dưới dạng số nguyên có dấu 64-bit.

   Điểm tham chiếu của timestamp phụ thuộc vào clock được sử dụng. Ví dụ:
   :c:func:`PyTime_Time` trả về các timestamp tính tương đối so với UNIX epoch.

   Phạm vi được hỗ trợ vào khoảng [-292,3 năm; +292,3 năm]. Lấy kỷ nguyên Unix (ngày 1 tháng 1 năm 1970) làm mốc tham chiếu, phạm vi ngày được hỗ trợ vào khoảng [1677-09-21; 2262-04-11]. Các giới hạn chính xác được cung cấp dưới dạng hằng số:

.. c:var:: PyTime_t PyTime_MIN

   Giá trị nhỏ nhất của :c:type:`PyTime_t`.

.. c:var:: PyTime_t PyTime_MAX

   Giá trị lớn nhất của :c:type:`PyTime_t`.


Các hàm đồng hồ
---------------

Các hàm sau nhận một con trỏ đến :c:expr:`PyTime_t` và gán cho nó giá trị của một đồng hồ cụ thể. Chi tiết về từng đồng hồ được nêu trong tài liệu của hàm Python tương ứng.

Các hàm trả về ``0`` khi thành công hoặc ``-1`` (và thiết lập một exception) khi thất bại.

Khi xảy ra tràn số nguyên, chúng thiết lập exception :c:data:`PyExc_OverflowError` và đặt ``*result`` thành giá trị được giới hạn trong phạm vi ``[PyTime_MIN; PyTime_MAX]``. (Trên các hệ thống hiện tại, tràn số nguyên có thể là do thời gian hệ thống được cấu hình sai.)

Như với mọi C API khác (trừ khi có quy định khác), các hàm phải được gọi với một :term:`attached thread state`.

.. c:function:: int PyTime_Monotonic(PyTime_t *result)

   Đọc đồng hồ đơn điệu (monotonic clock). Xem :func:`time.monotonic` để biết các chi tiết quan trọng về đồng hồ này.

.. c:function:: int PyTime_PerfCounter(PyTime_t *result)

   Đọc bộ đếm hiệu suất. Xem :func:`time.perf_counter` để biết các chi tiết quan trọng về đồng hồ này.

.. c:function:: int PyTime_Time(PyTime_t *result)

   Đọc thời gian của “đồng hồ thực” (wall clock). Xem :func:`time.time` để biết các chi tiết về đồng hồ này.


Các hàm đồng hồ thô
-------------------

Tương tự các hàm đồng hồ, nhưng không đặt exception khi xảy ra lỗi và không yêu cầu caller phải có một :term:`attached thread state`.

Khi thành công, các hàm sẽ trả về ``0``.

Khi thất bại, các hàm này đặt ``*result`` thành ``0`` và trả về ``-1``, *mà không* đặt exception. Để lấy nguyên nhân của lỗi, :term:`đính kèm <attached thread state>` một :term:`thread state` rồi gọi hàm thông thường (không-``Raw``). Lưu ý rằng hàm thông thường có thể thành công sau khi hàm ``Raw`` thất bại.

.. c:function:: int PyTime_MonotonicRaw(PyTime_t *result)

   Tương tự như :c:func:`PyTime_Monotonic`, nhưng không đặt exception khi xảy ra lỗi và không yêu cầu một :term:`attached thread state`.

.. c:function:: int PyTime_PerfCounterRaw(PyTime_t *result)

   Tương tự như :c:func:`PyTime_PerfCounter`, nhưng không đặt exception khi xảy ra lỗi và không yêu cầu một :term:`attached thread state`.

.. c:function:: int PyTime_TimeRaw(PyTime_t *result)

   Tương tự như :c:func:`PyTime_Time`, nhưng không đặt exception khi xảy ra lỗi và không yêu cầu một :term:`attached thread state`.


Các hàm chuyển đổi
------------------

.. c:function:: double PyTime_AsSecondsDouble(PyTime_t t)

   Chuyển đổi dấu thời gian thành số giây dưới dạng kiểu C :c:expr:`double`.

   Hàm này không thể thất bại, nhưng lưu ý rằng :c:expr:`double` có độ chính xác hạn chế đối với các giá trị lớn.
