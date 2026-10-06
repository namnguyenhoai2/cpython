.. currentmodule:: asyncio


.. _asyncio-exceptions:

========
Ngoại lệ
========

**Mã nguồn:** :source:`Lib/asyncio/exceptions.py`

----------------------------------------------------

.. exception:: TimeoutError

   Một bí danh đã không còn được dùng của :exc:`TimeoutError`, được raise khi thao tác đã vượt quá thời hạn được chỉ định.

   .. versionchanged:: 3.11

      Lớp này hiện là bí danh của :exc:`TimeoutError`.


.. exception:: CancelledError

   Thao tác đã bị hủy.

   Có thể bắt ngoại lệ này để thực hiện các thao tác tùy chỉnh khi các asyncio Tasks bị hủy. Trong hầu hết mọi trường hợp, ngoại lệ này phải được raise lại.

   .. versionchanged:: 3.8

      :exc:`CancelledError` hiện là lớp con của :class:`BaseException` thay vì :class:`Exception`.


.. exception:: InvalidStateError

   Trạng thái nội bộ không hợp lệ của :class:`Task` hoặc :class:`Future`.

   Có thể được phát sinh trong những tình huống như đặt giá trị kết quả cho một đối tượng *Future* đã được đặt giá trị kết quả.


.. exception:: SendfileNotAvailableError

   Lệnh gọi hệ thống "sendfile" không khả dụng cho socket hoặc loại tệp đã cho.

   Một lớp con của :exc:`RuntimeError`.


.. exception:: IncompleteReadError

   Thao tác đọc được yêu cầu chưa hoàn tất đầy đủ.

   Được phát sinh bởi :ref:`các API stream của asyncio <asyncio-streams>`.

   Ngoại lệ này là một lớp con của :exc:`EOFError`.

   .. attribute:: expected

      Tổng số (:class:`int`) byte dự kiến.

   .. attribute:: partial

      Một chuỗi gồm :class:`bytes` được đọc trước khi đạt đến cuối stream.


.. exception:: LimitOverrunError

   Đã đạt đến giới hạn kích thước buffer trong khi tìm dấu phân cách.

   Được phát sinh bởi :ref:`các API stream của asyncio <asyncio-streams>`.

   .. attribute:: consumed

      Tổng số byte sẽ được tiêu thụ.
