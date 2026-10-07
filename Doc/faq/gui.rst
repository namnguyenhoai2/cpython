:tocdepth: 2

==================================
FAQ về giao diện người dùng đồ họa
==================================

.. only:: html

   .. contents::

.. XXX need review for Python 3.


Các câu hỏi chung về GUI
========================

Có những bộ công cụ GUI nào cho Python?
=======================================

Các bản build tiêu chuẩn của Python bao gồm một interface hướng đối tượng cho bộ widget Tcl/Tk, có tên là :ref:`tkinter <Tkinter>`. Đây có lẽ là lựa chọn dễ cài đặt và sử dụng nhất (vì nó đi kèm với hầu hết `bản phân phối nhị phân <https://www.python.org/downloads/>`_ của Python). Để biết thêm thông tin về Tk, bao gồm các liên kết đến mã nguồn, hãy xem `trang chủ Tcl/Tk <https://www.tcl.tk>`_. Tcl/Tk hoàn toàn portable trên các nền tảng macOS, Windows và Unix.

Tùy thuộc vào (các) nền tảng bạn nhắm đến, cũng có một số lựa chọn khác. Có thể tìm thấy một `danh sách các framework GUI đa nền tảng <https://wiki.python.org/moin/GuiProgramming#Cross-Platform_Frameworks>`_ và `dành riêng cho từng nền tảng <https://wiki.python.org/moin/GuiProgramming#Platform-specific_Frameworks>`_ trên wiki của Python.

Các câu hỏi về Tkinter
======================

Làm thế nào để freeze các ứng dụng Tkinter?
-------------------------------------------

Freeze là một công cụ để tạo các ứng dụng độc lập. Khi đóng băng các ứng dụng Tkinter, các ứng dụng sẽ không thực sự độc lập, vì chúng vẫn cần các thư viện Tcl và Tk.

Một giải pháp là đóng gói ứng dụng cùng với các thư viện Tcl và Tk, rồi trỏ đến chúng trong thời gian chạy bằng các biến môi trường :envvar:`!TCL_LIBRARY` và :envvar:`!TK_LIBRARY`.

Nhiều thư viện đóng băng của bên thứ ba như py2exe và cx_Freeze đã tích hợp sẵn khả năng xử lý các ứng dụng Tkinter.


Tôi có thể xử lý các sự kiện Tk trong khi chờ I/O không?
--------------------------------------------------------

Trên các nền tảng khác Windows, câu trả lời là có, và bạn thậm chí không cần đến thread! Tuy nhiên, bạn sẽ phải cấu trúc lại một chút mã I/O của mình. Tk có lệnh tương đương với lệnh :c:func:`!XtAddInput` của Xt, cho phép bạn đăng ký một hàm callback sẽ được gọi từ mainloop của Tk khi có thể thực hiện I/O trên một file descriptor. Xem :ref:`tkinter-file-handlers`.


Tại sao tôi không thể làm cho các liên kết phím hoạt động trong Tkinter?
------------------------------------------------------------------------

Một phàn nàn thường được nghe là các trình xử lý sự kiện :ref:`bound <bindings-and-events>` với các sự kiện bằng phương thức :meth:`!bind` không được xử lý ngay cả khi nhấn đúng phím.

Nguyên nhân phổ biến nhất là widget mà binding áp dụng không có “keyboard focus”. Hãy xem tài liệu Tk về lệnh focus. Thông thường, một widget nhận keyboard focus bằng cách nhấp vào widget đó (nhưng không áp dụng cho label; xem tùy chọn takefocus).

.. _`binary distributions`: https://www.python.org/downloads/
.. _`Tcl/Tk home page`: https://www.tcl.tk
.. _`list of cross-platform`: https://wiki.python.org/moin/GuiProgramming#Cross-Platform_Frameworks
.. _`platform-specific`: https://wiki.python.org/moin/GuiProgramming#Platform-specific_Frameworks
