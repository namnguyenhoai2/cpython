:mod:`!tkinter.scrolledtext` --- Tiện ích văn bản có thanh cuộn
===============================================================

.. module:: tkinter.scrolledtext
   :synopsis: Widget văn bản có thanh cuộn dọc.

.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>

**Mã nguồn:** :source:`Lib/tkinter/scrolledtext.py`

--------------

Mô-đun :mod:`!tkinter.scrolledtext` cung cấp một lớp cùng tên, triển khai một widget văn bản cơ bản có thanh cuộn dọc được cấu hình để hoạt động "đúng cách". Sử dụng lớp :class:`ScrolledText` dễ dàng hơn nhiều so với việc trực tiếp thiết lập một widget văn bản và thanh cuộn.

Widget văn bản và thanh cuộn được đóng gói cùng nhau trong một :class:`~tkinter.Frame`, còn các phương thức của :class:`~tkinter.Pack`, :class:`~tkinter.Grid` và
các trình quản lý hình học :class:`~tkinter.Place` được lấy từ
đối tượng :class:`~tkinter.Frame`. Điều này cho phép sử dụng trực tiếp widget :class:`ScrolledText` để đạt được hầu hết hành vi quản lý hình học thông thường.

Nếu cần kiểm soát cụ thể hơn, có thể sử dụng các thuộc tính sau:

.. class:: ScrolledText(master=None, **kw)


   .. attribute:: frame

      Khung bao quanh widget văn bản và widget thanh cuộn.


   .. attribute:: vbar

      Widget thanh cuộn.
