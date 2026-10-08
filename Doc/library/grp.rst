:mod:`!grp` --- Cơ sở dữ liệu nhóm
==================================

.. module:: grp
   :synopsis: Cơ sở dữ liệu nhóm (getgrnam() và các hàm liên quan).

--------------

Mô-đun này cung cấp quyền truy cập vào cơ sở dữ liệu nhóm Unix. Mô-đun này khả dụng trên tất cả các phiên bản Unix.

.. availability:: Unix, not WASI, not Android, not iOS.

Các mục trong cơ sở dữ liệu nhóm được trả về dưới dạng một đối tượng giống tuple, với các thuộc tính tương ứng với các thành phần của cấu trúc ``group`` (trường Attribute bên dưới, xem ``<grp.h>``):

+---------+------------+---------------------------------------------------+
| Chỉ mục | Thuộc tính | Ý nghĩa                                           |
+=========+============+===================================================+
| 0       | gr_name    | tên của group                                     |
+---------+------------+---------------------------------------------------+
| 1       | gr_passwd  | mật khẩu (được mã hóa) của group; thường để trống |
+---------+------------+---------------------------------------------------+
| 2       | gr_gid     | ID dạng số của group                              |
+---------+------------+---------------------------------------------------+
| 3       | gr_mem     | tất cả tên người dùng của thành viên nhóm         |
+---------+------------+---------------------------------------------------+

gid là một số nguyên, name và password là các chuỗi, còn danh sách thành viên là một danh sách các chuỗi. (Lưu ý rằng hầu hết người dùng không được liệt kê rõ ràng là thành viên của nhóm mà họ thuộc về theo password database. Hãy kiểm tra cả hai database để lấy thông tin thành viên đầy đủ. Cũng lưu ý rằng một ``gr_name`` bắt đầu bằng ``+`` hoặc ``-`` có khả năng là một tham chiếu YP/NIS và có thể không thể truy cập thông qua :func:`getgrnam` hoặc :func:`getgrgid`.)

Mô-đun này định nghĩa các mục sau:


.. function:: getgrgid(id)

   Trả về mục trong group database tương ứng với group ID dạng số đã cho. :exc:`KeyError` được phát sinh nếu không tìm thấy mục được yêu cầu.

   .. versionchanged:: 3.10
      :exc:`TypeError` is raised for non-integer arguments like floats or strings.

.. function:: getgrnam(name)

   Trả về mục trong group database tương ứng với tên nhóm đã cho. :exc:`KeyError` được phát sinh nếu không tìm thấy mục được yêu cầu.


.. function:: getgrall()

   Trả về danh sách tất cả các mục nhóm hiện có, theo thứ tự bất kỳ.


.. seealso::

   Mô-đun :mod:`pwd`
      Một interface tới cơ sở dữ liệu người dùng, tương tự như thế này.
