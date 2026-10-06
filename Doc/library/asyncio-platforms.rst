.. currentmodule:: asyncio


.. _asyncio-platform-support:


===============
Hỗ trợ nền tảng
===============

Mô-đun :mod:`asyncio` được thiết kế để có tính portable, nhưng một số nền tảng có những khác biệt và giới hạn tinh tế do kiến trúc và khả năng nền tảng cơ sở.


Tất cả nền tảng
===============

* Không thể sử dụng :meth:`loop.add_reader` và :meth:`loop.add_writer` để giám sát hoạt động I/O tệp.

* Không thể sử dụng :meth:`loop.connect_read_pipe` và :meth:`loop.connect_write_pipe` với các tệp thông thường. Xem :ref:`Các đối tượng pipe được hỗ trợ <asyncio-pipe-objects>` để biết những đối tượng được chấp nhận trên mỗi nền tảng.


Windows
=======

**Mã nguồn:** :source:`Lib/asyncio/proactor_events.py`,
:source:`Lib/asyncio/windows_events.py`,
:source:`Lib/asyncio/windows_utils.py`

--------------------------------------

.. versionchanged:: 3.8

   Trên Windows, :class:`ProactorEventLoop` hiện là vòng lặp sự kiện mặc định.

Tất cả vòng lặp sự kiện trên Windows đều không hỗ trợ các phương thức sau:

* :meth:`loop.create_unix_connection` và
  :meth:`loop.create_unix_server` không được hỗ trợ. Họ socket :const:`socket.AF_UNIX` chỉ dành riêng cho Unix.

* :meth:`loop.add_signal_handler` và
  :meth:`loop.remove_signal_handler` không được hỗ trợ.

:class:`SelectorEventLoop` có những hạn chế sau:

* :class:`~selectors.SelectSelector` được dùng để chờ các sự kiện socket: nó hỗ trợ socket và bị giới hạn ở 512 socket.

* :meth:`loop.add_reader` và :meth:`loop.add_writer` chỉ chấp nhận các socket handle (ví dụ: pipe file descriptor không được hỗ trợ).

* Pipe không được hỗ trợ, vì vậy các phương thức :meth:`loop.connect_read_pipe` và :meth:`loop.connect_write_pipe` không được triển khai.

* :ref:`Các tiến trình con <asyncio-subprocess>` không được hỗ trợ, tức là
  Các phương thức :meth:`loop.subprocess_exec` và :meth:`loop.subprocess_shell` không được triển khai.

:class:`ProactorEventLoop` có các hạn chế sau:

* Các phương thức :meth:`loop.add_reader` và :meth:`loop.add_writer` không được hỗ trợ.

* :meth:`loop.connect_read_pipe` và :meth:`loop.connect_write_pipe` chỉ chấp nhận handle được mở cho I/O chồng lấp (overlapped I/O). Xem :ref:`Các đối tượng pipe được hỗ trợ <asyncio-pipe-objects>` để biết những đối tượng nào được hỗ trợ.

Độ phân giải của đồng hồ đơn điệu (monotonic clock) trên Windows thường vào khoảng 15,6 mili giây. Độ phân giải tốt nhất là 0,5 mili giây. Độ phân giải phụ thuộc vào phần cứng (khả dụng `HPET <https://en.wikipedia.org/wiki/High_Precision_Event_Timer>`_) và cấu hình Windows.


.. _asyncio-windows-subprocess:

Hỗ trợ subprocess trên Windows
------------------------------

Trên Windows, event loop mặc định :class:`ProactorEventLoop` hỗ trợ subprocess, còn :class:`SelectorEventLoop` thì không.


macOS
=====

Các phiên bản macOS hiện đại được hỗ trợ đầy đủ.

.. rubric:: macOS <= 10.8

Trên macOS 10.6, 10.7 và 10.8, event loop mặc định sử dụng :class:`selectors.KqueueSelector`, không hỗ trợ các thiết bị ký tự trên những phiên bản này. Có thể cấu hình thủ công :class:`SelectorEventLoop` để sử dụng :class:`~selectors.SelectSelector` hoặc :class:`~selectors.PollSelector`, nhằm hỗ trợ các thiết bị ký tự trên những phiên bản macOS cũ hơn này. Ví dụ::

    import asyncio
    import selectors

    selector = selectors.SelectSelector()
    loop = asyncio.SelectorEventLoop(selector)
    asyncio.set_event_loop(loop)

.. _`HPET`: https://en.wikipedia.org/wiki/High_Precision_Event_Timer
