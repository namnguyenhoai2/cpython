:mod:`!getpass` --- Nhập mật khẩu portable
==========================================

.. module:: getpass
   :synopsis: Đọc mật khẩu portable và truy xuất userid.

.. moduleauthor:: Piers Lauder <piers@cs.su.oz.au>
.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>
.. Windows (& Mac?) support by Guido van Rossum.

**Mã nguồn:** :source:`Lib/getpass.py`

--------------

.. include:: ../includes/wasm-notavail.rst

Module :mod:`!getpass` cung cấp hai hàm:

.. function:: getpass(prompt='Password: ', stream=None, *, echo_char=None)

   Nhắc người dùng nhập mật khẩu mà không hiển thị ký tự. Người dùng được nhắc bằng chuỗi *prompt*, mặc định là ``'Password: '``. Trên Unix, lời nhắc được ghi vào đối tượng giống tệp *stream* bằng trình xử lý lỗi replace nếu cần. *stream* mặc định là terminal điều khiển (:file:`/dev/tty`) hoặc nếu terminal đó không khả dụng thì là ``sys.stderr`` (đối số này bị bỏ qua trên Windows).

   Đối số *echo_char* kiểm soát cách hiển thị dữ liệu nhập của người dùng trong khi gõ. Nếu *echo_char* là ``None`` (mặc định), dữ liệu nhập vẫn được ẩn. Nếu không, *echo_char* phải là một ký tự ASCII có thể in duy nhất và mỗi ký tự được gõ sẽ được thay thế bằng ký tự đó. Ví dụ, ``echo_char='*'`` sẽ hiển thị các dấu hoa thị thay vì dữ liệu nhập thực tế.

   Nếu không thể nhập mà không hiển thị ký tự, getpass() sẽ chuyển sang in thông báo cảnh báo vào *stream*, đọc từ ``sys.stdin`` và phát ra một :exc:`GetPassWarning`.

   .. note::
      Nếu bạn gọi getpass từ bên trong IDLE, dữ liệu nhập có thể được thực hiện trong terminal nơi bạn đã khởi chạy IDLE thay vì trong chính cửa sổ IDLE.

   .. note::
      Trên các hệ thống Unix, khi *echo_char* được đặt, terminal sẽ được cấu hình để hoạt động ở
      :manpage:`noncanonical mode <termios(3)#Canonical_and_noncanonical_mode>`. Cụ thể, điều này có nghĩa là các phím tắt chỉnh sửa dòng như
      :kbd:`Ctrl+U` sẽ không hoạt động và có thể chèn các ký tự không mong muốn vào dữ liệu nhập.

   .. versionchanged:: 3.14
      Đã thêm tham số *echo_char* để cung cấp phản hồi từ bàn phím.

.. exception:: GetPassWarning

   Một :exc:`UserWarning` subclass được phát sinh khi dữ liệu nhập mật khẩu có thể được hiển thị lại.


.. function:: getuser()

   Trả về "tên đăng nhập" của người dùng.

   Hàm này kiểm tra các biến môi trường :envvar:`LOGNAME`,
   :envvar:`USER`, :envvar:`!LNAME` và :envvar:`USERNAME`, theo thứ tự, rồi trả về giá trị của biến đầu tiên được đặt thành một chuỗi không rỗng. Nếu không biến nào được đặt, tên đăng nhập từ cơ sở dữ liệu mật khẩu sẽ được trả về trên các hệ thống hỗ trợ mô-đun :mod:`pwd`; nếu không, một :exc:`OSError` sẽ được phát sinh.

   Nhìn chung, nên ưu tiên sử dụng hàm này thay cho :func:`os.getlogin`.

   .. versionchanged:: 3.13
      Trước đây, nhiều exception khác ngoài :exc:`OSError` cũng được phát sinh.
