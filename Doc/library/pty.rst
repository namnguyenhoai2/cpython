:mod:`!pty` --- Tiện ích pseudo-terminal
========================================

.. module:: pty
   :synopsis: Xử lý pseudo-terminal cho Unix.

.. moduleauthor:: Steen Lumholt
.. sectionauthor:: Moshe Zadka <moshez@zadka.site.co.il>

**Mã nguồn:** :source:`Lib/pty.py`

--------------

Mô-đun :mod:`!pty` định nghĩa các thao tác để xử lý khái niệm pseudo-terminal: khởi động một tiến trình khác và cho phép ghi vào cũng như đọc từ terminal điều khiển của tiến trình đó bằng chương trình.

.. availability:: Unix.

Việc xử lý pseudo-terminal phụ thuộc nhiều vào nền tảng. Mã này chủ yếu được kiểm thử trên Linux, FreeBSD và macOS (được cho là sẽ hoạt động trên các nền tảng POSIX khác, nhưng chưa được kiểm thử kỹ lưỡng).

Mô-đun :mod:`!pty` định nghĩa các hàm sau:


.. function:: fork()

   Fork. Kết nối terminal điều khiển của tiến trình con với một pseudo-terminal. Giá trị trả về là ``(pid, fd)``. Lưu ý rằng tiến trình con nhận được *pid* bằng 0, và *fd* là *không hợp lệ*. Giá trị trả về của tiến trình cha là *pid* của tiến trình con, còn *fd* là một file descriptor được kết nối với terminal điều khiển của tiến trình con (đồng thời với đầu vào và đầu ra tiêu chuẩn của tiến trình con).

   .. warning:: Trên macOS, việc sử dụng hàm này là không an toàn khi kết hợp với các system API cấp cao hơn, bao gồm cả việc sử dụng :mod:`urllib.request`.


.. function:: openpty()

   Mở một cặp pseudo-terminal mới, sử dụng :func:`os.openpty` nếu có thể, hoặc sử dụng mã mô phỏng cho các hệ thống Unix nói chung. Trả về một cặp file descriptor ``(master, slave)``, lần lượt dành cho đầu master và đầu slave.


.. function:: spawn(argv[, master_read[, stdin_read]])

   Tạo một process và kết nối terminal điều khiển của process đó với standard I/O của process hiện tại. Cách này thường được dùng để làm rối các chương trình nhất quyết đọc từ terminal điều khiển. Process được tạo phía sau pty được kỳ vọng sẽ kết thúc, và khi process đó kết thúc, *spawn* sẽ trả về.

   Một vòng lặp sao chép STDIN của process hiện tại đến child và dữ liệu nhận được từ child đến STDOUT của process hiện tại. Child sẽ không được thông báo nếu STDIN của process hiện tại đóng.

   Các hàm *master_read* và *stdin_read* được truyền vào một file descriptor mà chúng phải đọc, và luôn phải trả về một chuỗi byte. Để buộc spawn trả về trước khi child process thoát, cần trả về một mảng byte rỗng nhằm báo hiệu kết thúc file.

   Triển khai mặc định cho cả hai hàm sẽ đọc và trả về tối đa 1024 byte mỗi lần hàm được gọi. Callback *master_read* được truyền file descriptor master của pseudo-terminal để đọc output từ child process, còn *stdin_read* được truyền file descriptor 0 để đọc từ standard input của parent process.

   Việc trả về một chuỗi byte rỗng từ một trong hai callback được hiểu là điều kiện kết thúc file (EOF), và callback đó sẽ không được gọi sau đó. Nếu *stdin_read* báo hiệu EOF, terminal điều khiển không còn có thể giao tiếp với parent process HOẶC child process. Trừ khi child process sẽ thoát mà không cần input, *spawn* sẽ lặp vô hạn. Nếu *master_read* báo hiệu EOF, hành vi tương tự cũng xảy ra (ít nhất là trên Linux).

   Trả về giá trị trạng thái thoát từ :func:`os.waitpid` của tiến trình con.

   Có thể dùng :func:`os.waitstatus_to_exitcode` để chuyển đổi trạng thái thoát thành mã thoát.

   .. audit-event:: pty.spawn argv pty.spawn

   .. versionchanged:: 3.4
      :func:`spawn` now returns the status value from :func:`os.waitpid`
      của tiến trình con.

Ví dụ
-----

.. sectionauthor:: Steen Lumholt

Chương trình sau đây hoạt động như lệnh Unix :manpage:`script(1)`, sử dụng pseudo-terminal để ghi lại toàn bộ dữ liệu đầu vào và đầu ra của một phiên terminal vào một "typescript".::

    import argparse
    import os
    import pty
    import sys
    import time

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', dest='append', action='store_true')
    parser.add_argument('-p', dest='use_python', action='store_true')
    parser.add_argument('filename', nargs='?', default='typescript')
    options = parser.parse_args()

    shell = sys.executable if options.use_python else os.environ.get('SHELL', 'sh')
    filename = options.filename
    mode = 'ab' if options.append else 'wb'

    with open(filename, mode) as script:
        def read(fd):
            data = os.read(fd, 1024)
            script.write(data)
            return data

        print('Script started, file is', filename)
        script.write(('Script started on %s\n' % time.asctime()).encode())

        pty.spawn(shell, read)

        script.write(('Script done on %s\n' % time.asctime()).encode())
        print('Script done, file is', filename)
