:mod:`!pwd` --- Cơ sở dữ liệu mật khẩu
======================================

.. module:: pwd
   :synopsis: Cơ sở dữ liệu mật khẩu (getpwnam() và các hàm liên quan).

--------------

Mô-đun này cung cấp quyền truy cập vào cơ sở dữ liệu tài khoản người dùng và mật khẩu Unix. Mô-đun này có sẵn trên mọi phiên bản Unix.

.. availability:: Unix, not WASI, not iOS.

Các mục trong cơ sở dữ liệu mật khẩu được trả về dưới dạng một đối tượng giống tuple, với các thuộc tính tương ứng với các thành phần của cấu trúc ``passwd`` (trường Attribute bên dưới, xem ``<pwd.h>``):

+---------+---------------+--------------------------------------+
| Chỉ mục | Thuộc tính    | Ý nghĩa                              |
+=========+===============+======================================+
| 0       | ``pw_name``   | Tên đăng nhập                        |
+---------+---------------+--------------------------------------+
| 1       | ``pw_passwd`` | Mật khẩu được mã hóa, không bắt buộc |
+---------+---------------+--------------------------------------+
| 2       | ``pw_uid``    | ID người dùng dạng số                |
+---------+---------------+--------------------------------------+
| 3       | ``pw_gid``    | ID nhóm dạng số                      |
+---------+---------------+--------------------------------------+
| 4       | ``pw_gecos``  | Tên người dùng hoặc trường chú thích |
+---------+---------------+--------------------------------------+
| 5       | ``pw_dir``    | Thư mục chính của người dùng         |
+---------+---------------+--------------------------------------+
| 6       | ``pw_shell``  | Trình thông dịch lệnh của người dùng |
+---------+---------------+--------------------------------------+

Các mục uid và gid là số nguyên, tất cả các mục khác đều là chuỗi. :exc:`KeyError` được phát sinh nếu không tìm thấy mục nhập được yêu cầu.

.. note::

   Trong Unix truyền thống, trường ``pw_passwd`` thường chứa mật khẩu được mã hóa bằng một thuật toán bắt nguồn từ DES. Tuy nhiên, hầu hết các hệ Unix hiện đại đều sử dụng hệ thống *shadow password*. Trên các hệ Unix đó, trường *pw_passwd* chỉ chứa dấu hoa thị (``'*'``) hoặc chữ cái ``'x'``, trong khi mật khẩu được mã hóa được lưu trong một tệp :file:`/etc/shadow` không cho phép mọi người đọc. Trường *pw_passwd* có chứa thông tin hữu ích hay không tùy thuộc vào hệ thống.

Mô-đun này định nghĩa các mục sau:


.. function:: getpwuid(uid)

   Trả về mục nhập cơ sở dữ liệu mật khẩu cho ID người dùng dạng số đã cho.


.. function:: getpwnam(name)

   Trả về mục nhập cơ sở dữ liệu mật khẩu cho tên người dùng đã cho.


.. function:: getpwall()

   Trả về danh sách tất cả các mục nhập cơ sở dữ liệu mật khẩu hiện có, theo thứ tự bất kỳ.


.. seealso::

   Mô-đun :mod:`grp`
      Một giao diện tới cơ sở dữ liệu nhóm, tương tự như giao diện này.
