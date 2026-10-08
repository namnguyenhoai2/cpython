:mod:`!termios` --- điều khiển tty theo kiểu POSIX
==================================================

.. module:: termios
   :synopsis: Điều khiển tty theo kiểu POSIX.

.. index::
   pair: POSIX; I/O control
   pair: tty; I/O control

--------------

Mô-đun này cung cấp giao diện cho các lệnh gọi POSIX dùng để điều khiển I/O tty. Để xem mô tả đầy đủ về các lệnh gọi này, hãy xem :manpage:`termios(3)` trang hướng dẫn Unix.  Mô-đun này chỉ khả dụng trên những phiên bản Unix hỗ trợ điều khiển I/O tty theo kiểu POSIX *termios* được cấu hình trong quá trình cài đặt.

.. availability:: Unix.

Tất cả các hàm trong mô-đun này đều nhận một bộ mô tả tệp *fd* làm đối số đầu tiên.  Đây có thể là một bộ mô tả tệp dạng số nguyên, chẳng hạn như giá trị được trả về bởi ``sys.stdin.fileno()``, hoặc một :term:`file object`, chẳng hạn như chính ``sys.stdin``.

Mô-đun này cũng định nghĩa tất cả các hằng số cần thiết để làm việc với những hàm được cung cấp tại đây; chúng có cùng tên với các thành phần tương ứng trong C.  Vui lòng tham khảo tài liệu hệ thống để biết thêm thông tin về cách sử dụng các giao diện điều khiển terminal này.

Mô-đun định nghĩa các hàm sau:


.. function:: tcgetattr(fd)

   Trả về một danh sách chứa các thuộc tính tty của bộ mô tả tệp *fd*, như sau: ``[iflag, oflag, cflag, lflag, ispeed, ospeed, cc]`` trong đó *cc* là danh sách các ký tự đặc biệt của tty (mỗi ký tự là một chuỗi có độ dài 1, ngoại trừ các phần tử có chỉ mục :const:`VMIN` và :const:`VTIME`, là số nguyên khi các trường này được định nghĩa). Việc diễn giải các cờ và tốc độ, cũng như lập chỉ mục trong mảng *cc*, phải được thực hiện bằng các hằng số ký hiệu được định nghĩa trong mô-đun :mod:`!termios`.


.. function:: tcsetattr(fd, when, attributes)

   Đặt các thuộc tính tty cho bộ mô tả tệp *fd* từ *attributes*, là một danh sách tương tự như danh sách được trả về bởi :func:`tcgetattr`. Đối số *when* xác định thời điểm các thuộc tính được thay đổi:

   .. data:: TCSANOW

      Thay đổi các thuộc tính ngay lập tức.

   .. data:: TCSADRAIN

      Thay đổi các thuộc tính sau khi truyền xong toàn bộ dữ liệu đầu ra đang chờ trong hàng đợi.

   .. data:: TCSAFLUSH

      Thay đổi các thuộc tính sau khi truyền xong toàn bộ dữ liệu đầu ra đang chờ trong hàng đợi và loại bỏ toàn bộ dữ liệu đầu vào đang chờ trong hàng đợi.


.. function:: tcsendbreak(fd, duration)

   Gửi một tín hiệu break trên bộ mô tả tệp *fd*. *duration* bằng 0 sẽ gửi tín hiệu break trong 0.25--0.5 giây; *duration* khác 0 có ý nghĩa phụ thuộc vào hệ thống.


.. function:: tcdrain(fd)

   Chờ cho đến khi toàn bộ dữ liệu đầu ra được ghi vào bộ mô tả tệp *fd* đã được truyền đi.


.. function:: tcflush(fd, queue)

   Loại bỏ dữ liệu đang chờ trong hàng đợi trên bộ mô tả tệp *fd*. Bộ chọn *queue* chỉ định hàng đợi cần xử lý: :const:`TCIFLUSH` cho hàng đợi đầu vào, :const:`TCOFLUSH` cho hàng đợi đầu ra hoặc :const:`TCIOFLUSH` cho cả hai hàng đợi.


.. function:: tcflow(fd, action)

   Tạm dừng hoặc tiếp tục việc nhập hoặc xuất trên file descriptor *fd*. Đối số *action* có thể là :const:`TCOOFF` để tạm dừng xuất, :const:`TCOON` để khởi động lại xuất, :const:`TCIOFF` để tạm dừng nhập hoặc :const:`TCION` để khởi động lại nhập.


.. function:: tcgetwinsize(fd)

   Trả về một tuple ``(ws_row, ws_col)`` chứa kích thước cửa sổ tty cho file descriptor *fd*. Yêu cầu :const:`termios.TIOCGWINSZ` hoặc
   :const:`termios.TIOCGSIZE`.

   .. versionadded:: 3.11


.. function:: tcsetwinsize(fd, winsize)

   Đặt kích thước cửa sổ tty cho file descriptor *fd* từ *winsize*, đây là một tuple gồm hai phần tử ``(ws_row, ws_col)`` giống tuple được trả về bởi
   :func:`tcgetwinsize`. Yêu cầu xác định ít nhất một trong các cặp (:const:`termios.TIOCGWINSZ`, :const:`termios.TIOCSWINSZ`); (:const:`termios.TIOCGSIZE`, :const:`termios.TIOCSSIZE`).

   .. versionadded:: 3.11


.. seealso::

   Module :mod:`tty`
      Các hàm tiện ích cho những thao tác điều khiển terminal phổ biến.


.. _termios-example:

Ví dụ
-----

Đây là một hàm nhắc nhập mật khẩu với chế độ echo bị tắt. Lưu ý kỹ thuật sử dụng một lệnh gọi :func:`tcgetattr` riêng biệt và một :keyword:`try` ...
câu lệnh :keyword:`finally` để đảm bảo rằng các thuộc tính tty cũ được khôi phục chính xác bất kể điều gì xảy ra::

   def getpass(prompt="Password: "):
       import termios, sys
       fd = sys.stdin.fileno()
       old = termios.tcgetattr(fd)
       new = termios.tcgetattr(fd)
       new[3] = new[3] & ~termios.ECHO          # lflags
       try:
           termios.tcsetattr(fd, termios.TCSADRAIN, new)
           passwd = input(prompt)
       finally:
           termios.tcsetattr(fd, termios.TCSADRAIN, old)
       return passwd

