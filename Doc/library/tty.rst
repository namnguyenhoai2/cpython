:mod:`!tty` --- Các hàm điều khiển terminal
===========================================

.. module:: tty
   :synopsis: Các hàm tiện ích thực hiện những thao tác điều khiển terminal phổ biến.

.. moduleauthor:: Steen Lumholt
.. sectionauthor:: Moshe Zadka <moshez@zadka.site.co.il>

**Mã nguồn:** :source:`Lib/tty.py`

--------------

Module :mod:`!tty` định nghĩa các hàm để đưa tty vào chế độ cbreak và raw.

.. availability:: Unix.

Vì yêu cầu module :mod:`termios`, module này chỉ hoạt động trên Unix.

Module :mod:`!tty` định nghĩa các hàm sau:


.. function:: cfmakeraw(mode)

   Chuyển đổi danh sách thuộc tính tty *mode*, là một danh sách giống danh sách được :func:`termios.tcgetattr` trả về, thành danh sách thuộc tính của tty ở chế độ raw.

   .. versionadded:: 3.12


.. function:: cfmakecbreak(mode)

   Chuyển đổi danh sách thuộc tính tty *mode*, là một danh sách tương tự như danh sách được trả về bởi :func:`termios.tcgetattr`, thành danh sách thuộc tính của tty ở chế độ cbreak.

   Thao tác này xóa các cờ chế độ cục bộ ``ECHO`` và ``ICANON`` trong *mode*, đồng thời đặt dữ liệu đầu vào tối thiểu là 1 byte và không có độ trễ.

   .. versionadded:: 3.12

   .. versionchanged:: 3.12.2
      Cờ ``ICRNL`` không còn bị xóa nữa. Điều này khớp với hành vi ``stty cbreak`` trên Linux và macOS, cũng như hành vi trước đây của :func:`setcbreak`.


.. function:: setraw(fd, when=termios.TCSAFLUSH)

   Thay đổi chế độ của bộ mô tả tệp *fd* thành raw. Nếu *when* bị bỏ qua, giá trị mặc định là :const:`termios.TCSAFLUSH` và được truyền cho
   :func:`termios.tcsetattr`. Giá trị trả về của :func:`termios.tcgetattr` được lưu trước khi đặt *fd* thành chế độ raw; giá trị này sẽ được trả về.

   .. versionchanged:: 3.12
      Giờ đây, giá trị trả về là các thuộc tính tty ban đầu, thay vì ``None``.


.. function:: setcbreak(fd, when=termios.TCSAFLUSH)

   Thay đổi chế độ của bộ mô tả tệp *fd* thành cbreak. Nếu *when* bị bỏ qua, giá trị mặc định là :const:`termios.TCSAFLUSH` và được truyền cho
   :func:`termios.tcsetattr`. Giá trị trả về của :func:`termios.tcgetattr` được lưu trước khi đặt *fd* sang chế độ cbreak; giá trị này được trả về.

   Thao tác này xóa các cờ chế độ cục bộ ``ECHO`` và ``ICANON``, đồng thời đặt dữ liệu đầu vào tối thiểu là 1 byte mà không có độ trễ.

   .. versionchanged:: 3.12
      Giờ đây, giá trị trả về là các thuộc tính tty ban đầu, thay vì ``None``.

   .. versionchanged:: 3.12.2
      Cờ ``ICRNL`` không còn bị xóa. Điều này khôi phục hành vi của Python 3.11 trở về trước, đồng thời phù hợp với mô tả trong các trang hướng dẫn man ``stty(1)`` của Linux, macOS và BSD về chế độ cbreak.


.. seealso::

   Mô-đun :mod:`termios`
      Giao diện điều khiển terminal cấp thấp.

