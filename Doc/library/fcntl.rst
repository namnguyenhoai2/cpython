:mod:`!fcntl` --- Các lệnh gọi hệ thống ``fcntl`` và ``ioctl``
==============================================================

.. module:: fcntl
   :synopsis: Các lệnh gọi hệ thống fcntl() và ioctl().

.. sectionauthor:: Jaap Vermeulen

.. index::
   pair: UNIX; file control
   pair: UNIX; I/O control

----------------

Mô-đun này thực hiện việc điều khiển tệp và I/O trên các bộ mô tả tệp. Đây là giao diện cho các hàm Unix :c:func:`fcntl` và :c:func:`ioctl`. Xem các trang hướng dẫn Unix :manpage:`fcntl(2)` và :manpage:`ioctl(2)` để biết đầy đủ chi tiết.

.. availability:: Unix, not WASI.

Tất cả các hàm trong mô-đun này nhận một bộ mô tả tệp *fd* làm đối số đầu tiên. Đây có thể là một bộ mô tả tệp dạng số nguyên, chẳng hạn như bộ mô tả được trả về bởi ``sys.stdin.fileno()``, hoặc một đối tượng :class:`io.IOBase`, chẳng hạn như chính ``sys.stdin``, cung cấp một :meth:`~io.IOBase.fileno` trả về một bộ mô tả tệp thực sự.

.. versionchanged:: 3.3
   Các thao tác trong mô-đun này trước đây phát sinh :exc:`IOError`, còn hiện nay phát sinh :exc:`OSError`.

.. versionchanged:: 3.8
   Mô-đun :mod:`!fcntl` hiện chứa các hằng ``F_ADD_SEALS``, ``F_GET_SEALS`` và ``F_SEAL_*`` để niêm phong các bộ mô tả tệp :func:`os.memfd_create`.

.. versionchanged:: 3.9
   Trên macOS, mô-đun :mod:`!fcntl` cung cấp hằng ``F_GETPATH``, dùng để lấy đường dẫn của một tệp từ bộ mô tả tệp. Trên Linux(>=3.15), mô-đun :mod:`!fcntl` cung cấp các hằng ``F_OFD_GETLK``, ``F_OFD_SETLK`` và ``F_OFD_SETLKW``, được sử dụng khi làm việc với các khóa mô tả tệp đang mở.

.. versionchanged:: 3.10
   Trên Linux >= 2.6.11, module :mod:`!fcntl` cung cấp các hằng số ``F_GETPIPE_SZ`` và ``F_SETPIPE_SZ``, lần lượt cho phép kiểm tra và thay đổi kích thước của pipe.

.. versionchanged:: 3.11
   Trên FreeBSD, module :mod:`!fcntl` cung cấp các hằng số ``F_DUP2FD`` và ``F_DUP2FD_CLOEXEC``, cho phép sao chép một file descriptor; hằng số sau đồng thời đặt cờ ``FD_CLOEXEC``.

.. versionchanged:: 3.12
   Trên Linux >= 4.5, module :mod:`!fcntl` cung cấp các hằng số ``FICLONE`` và ``FICLONERANGE``, cho phép chia sẻ một phần dữ liệu của tệp này với tệp khác bằng cách reflink trên một số filesystem (ví dụ: btrfs, OCFS2 và XFS). Hành vi này thường được gọi là "copy-on-write".

.. versionchanged:: 3.13
   Trên Linux >= 2.6.32, module :mod:`!fcntl` cung cấp các hằng số ``F_GETOWN_EX``, ``F_SETOWN_EX``, ``F_OWNER_TID``, ``F_OWNER_PID``, ``F_OWNER_PGRP``, cho phép chuyển các tín hiệu về khả năng I/O đến một thread, process hoặc process group cụ thể. Trên Linux >= 4.13, module :mod:`!fcntl` cung cấp các hằng số ``F_GET_RW_HINT``, ``F_SET_RW_HINT``, ``F_GET_FILE_RW_HINT``, ``F_SET_FILE_RW_HINT`` và ``RWH_WRITE_LIFE_*``, cho phép thông báo cho kernel về thời gian tồn tại tương đối dự kiến của các thao tác ghi trên một inode nhất định hoặc thông qua một open file description cụ thể. Trên Linux >= 5.1 và NetBSD, module :mod:`!fcntl` cung cấp hằng số ``F_SEAL_FUTURE_WRITE`` để sử dụng với các thao tác ``F_ADD_SEALS`` và ``F_GET_SEALS``. Trên FreeBSD, module :mod:`!fcntl` cung cấp các hằng số ``F_READAHEAD``, ``F_ISUNIONSTACK`` và ``F_KINFO``. Trên macOS và FreeBSD, module :mod:`!fcntl` cung cấp hằng số ``F_RDAHEAD``. Trên NetBSD và AIX, module :mod:`!fcntl` cung cấp hằng số ``F_CLOSEM``. Trên NetBSD, module :mod:`!fcntl` cung cấp hằng số ``F_MAXFD``. Trên macOS và NetBSD, module :mod:`!fcntl` cung cấp các hằng số ``F_GETNOSIGPIPE`` và ``F_SETNOSIGPIPE``.

.. versionchanged:: 3.14
   Trên Linux >= 6.1, module :mod:`!fcntl` cung cấp ``F_DUPFD_QUERY`` để truy vấn một file descriptor trỏ đến cùng một tệp.

Module định nghĩa các hàm sau:


.. function:: fcntl(fd, cmd, arg=0, /)

   Thực hiện thao tác *cmd* trên file descriptor *fd* (các đối tượng tệp cung cấp phương thức :meth:`~io.IOBase.fileno` cũng được chấp nhận). Các giá trị được sử dụng cho *cmd* phụ thuộc vào hệ điều hành và có sẵn dưới dạng các hằng số trong module :mod:`!fcntl`, sử dụng cùng tên như trong các tệp header C tương ứng. Đối số *arg* có thể là một giá trị số nguyên, một
   :term:`bytes-like object`, hoặc một chuỗi. Kiểu và kích thước của *arg* phải khớp với kiểu và kích thước của đối số của operation như được chỉ định trong tài liệu C tương ứng.

   Khi *arg* là một số nguyên, hàm trả về giá trị trả về dạng số nguyên của lệnh gọi C :c:func:`fcntl`.

   Khi đối số là bytes-like object, nó biểu diễn một cấu trúc nhị phân, chẳng hạn như cấu trúc được tạo bởi :func:`struct.pack`. Một giá trị chuỗi được mã hóa thành nhị phân bằng encoding UTF-8. Dữ liệu nhị phân được sao chép vào một buffer có địa chỉ được truyền cho lệnh gọi C :c:func:`fcntl`. Giá trị trả về sau khi lệnh gọi thành công là nội dung của buffer, được chuyển đổi thành đối tượng :class:`bytes`. Độ dài của đối tượng được trả về sẽ bằng độ dài của đối số *arg*. Kích thước này bị giới hạn ở 1024 byte.

   Nếu lệnh gọi :c:func:`fcntl` thất bại, một :exc:`OSError` sẽ được phát sinh.

   .. note::
      Nếu kiểu hoặc kích thước của *arg* không khớp với kiểu hoặc kích thước của đối số của operation (ví dụ: truyền một số nguyên khi cần một con trỏ, hoặc thông tin do hệ điều hành trả về trong buffer lớn hơn 1024 byte), điều này rất có thể dẫn đến lỗi phân đoạn hoặc làm hỏng dữ liệu theo cách khó nhận biết hơn.

   .. audit-event:: fcntl.fcntl fd,cmd,arg fcntl.fcntl

   .. versionchanged:: 3.14
      Thêm hỗ trợ cho các :term:`bytes-like objects <bytes-like object>` tùy ý, không chỉ :class:`bytes`.


.. function:: ioctl(fd, request, arg=0, mutate_flag=True, /)

   Hàm này giống hệt hàm :func:`~fcntl.fcntl`, ngoại trừ việc xử lý đối số còn phức tạp hơn.

   Tham số *request* chỉ nhận các giá trị có thể chứa được trong 32 bit hoặc 64 bit, tùy thuộc vào nền tảng. Các hằng số bổ sung đáng chú ý để sử dụng làm đối số *request* có thể được tìm thấy trong mô-đun :mod:`termios`, với cùng tên như trong các tệp header C tương ứng.

   Tham số *arg* có thể là một số nguyên, một :term:`bytes-like object`, hoặc một chuỗi. Kiểu và kích thước của *arg* phải khớp với kiểu và kích thước của đối số cho thao tác, như được chỉ định trong tài liệu C tương ứng.

   Nếu *arg* không hỗ trợ giao diện read-write buffer hoặc *mutate_flag* là false, hành vi sẽ giống như đối với hàm :func:`~fcntl.fcntl`.

   Nếu *arg* hỗ trợ giao diện read-write buffer (giống như :class:`bytearray`) và *mutate_flag* là true (giá trị mặc định), thì buffer về cơ bản được truyền cho system call :c:func:`!ioctl` bên dưới, mã trả về của system call này được chuyển lại cho Python đang gọi, còn nội dung mới của buffer phản ánh tác động của :c:func:`ioctl`. Đây là một đơn giản hóa nhỏ, vì nếu buffer được cung cấp có độ dài dưới 1024 byte thì trước tiên nó được sao chép vào một buffer tĩnh dài 1024 byte, sau đó buffer này được truyền cho :func:`ioctl` và sao chép ngược lại vào buffer được cung cấp.

   Nếu lệnh gọi :c:func:`ioctl` thất bại, một ngoại lệ :exc:`OSError` sẽ được phát sinh.

   .. note::
      Nếu kiểu hoặc kích thước của *arg* không khớp với kiểu hoặc kích thước của đối số của thao tác (ví dụ: truyền một số nguyên trong khi cần một con trỏ, hoặc thông tin do hệ điều hành trả về trong buffer lớn hơn 1024 byte, hoặc kích thước của đối tượng tương tự bytes có thể thay đổi quá nhỏ), điều này rất có thể dẫn đến lỗi vi phạm phân đoạn hoặc hỏng dữ liệu khó nhận biết hơn.

   Ví dụ::

      >>> import array, fcntl, struct, termios, os
      >>> os.getpgrp()
      13341
      >>> struct.unpack('h', fcntl.ioctl(0, termios.TIOCGPGRP, "  "))[0]
      13341
      >>> buf = array.array('h', [0])
      >>> fcntl.ioctl(0, termios.TIOCGPGRP, buf, 1)
      0
      >>> buf
      array('h', [13341])

   .. audit-event:: fcntl.ioctl fd,request,arg fcntl.ioctl

   .. versionchanged:: 3.14
      GIL luôn được giải phóng trong khi thực hiện một lời gọi hệ thống. Các lời gọi hệ thống thất bại với EINTR sẽ được tự động thử lại.

.. function:: flock(fd, operation, /)

   Thực hiện thao tác khóa *operation* trên bộ mô tả tệp *fd* (các đối tượng tệp cung cấp phương thức :meth:`~io.IOBase.fileno` cũng được chấp nhận). Xem hướng dẫn sử dụng Unix
   :manpage:`flock(2)` để biết chi tiết. (Trên một số hệ thống, hàm này được mô phỏng bằng :c:func:`fcntl`.)

   Nếu lời gọi :c:func:`flock` thất bại, một ngoại lệ :exc:`OSError` sẽ được phát sinh.

   .. audit-event:: fcntl.flock fd,operation fcntl.flock


.. function:: lockf(fd, cmd, len=0, start=0, whence=0, /)

   Về cơ bản, đây là một wrapper quanh các lời gọi khóa :func:`~fcntl.fcntl`. *fd* là bộ mô tả tệp (các đối tượng tệp cung cấp phương thức :meth:`~io.IOBase.fileno` cũng được chấp nhận) của tệp cần khóa hoặc mở khóa, còn *cmd* là một trong các giá trị sau:

   .. data:: LOCK_UN

      Giải phóng một khóa hiện có.

   .. data:: LOCK_SH

      Lấy một khóa dùng chung.

   .. data:: LOCK_EX

      Có được một khóa độc quyền.

   .. data:: LOCK_NB

      Dùng phép OR theo bit với bất kỳ hằng số nào trong ba hằng số ``LOCK_*`` còn lại để làm cho yêu cầu không chặn.

   Nếu sử dụng :const:`!LOCK_NB` và không thể có được khóa, một
   :exc:`OSError` sẽ được phát sinh và ngoại lệ sẽ có thuộc tính *errno* được đặt thành :const:`~errno.EACCES` hoặc :const:`~errno.EAGAIN` (tùy thuộc vào hệ điều hành; để đảm bảo tính khả chuyển, hãy kiểm tra cả hai giá trị). Trên ít nhất một số hệ thống, :const:`!LOCK_EX` chỉ có thể được sử dụng nếu file descriptor tham chiếu đến một tệp được mở để ghi.

   *len* là số byte cần khóa, *start* là vị trí byte bắt đầu khóa, tương đối với *whence*, và *whence* được xác định như trong
   :func:`io.IOBase.seek`, cụ thể là:

   * ``0`` -- tương đối với phần đầu tệp (:const:`os.SEEK_SET`)
   * ``1`` -- tương đối với vị trí hiện tại trong buffer (:const:`os.SEEK_CUR`)
   * ``2`` -- tương đối với cuối tệp (:const:`os.SEEK_END`)

   Giá trị mặc định của *start* là 0, nghĩa là bắt đầu từ đầu tệp. Giá trị mặc định của *len* là 0, nghĩa là khóa đến cuối tệp. Giá trị mặc định của *whence* cũng là 0.

   .. audit-event:: fcntl.lockf fd,cmd,len,start,whence fcntl.lockf

Các ví dụ (tất cả đều trên hệ thống tương thích với SVR4)::

   import struct, fcntl, os

   f = open(...)
   rv = fcntl.fcntl(f, fcntl.F_SETFL, os.O_NDELAY)

   lockdata = struct.pack('hhllhh', fcntl.F_WRLCK, 0, 0, 0, 0, 0)
   rv = fcntl.fcntl(f, fcntl.F_SETLKW, lockdata)

Lưu ý rằng trong ví dụ đầu tiên, biến lưu giá trị trả về *rv* sẽ chứa một giá trị số nguyên; trong ví dụ thứ hai, nó sẽ chứa một đối tượng :class:`bytes`. Bố cục cấu trúc của biến *lockdata* phụ thuộc vào hệ thống — do đó, việc sử dụng lời gọi :func:`flock` có thể tốt hơn.


.. seealso::

   Mô-đun :mod:`os`
      Nếu các cờ khóa :const:`~os.O_SHLOCK` và :const:`~os.O_EXLOCK` hiện diện trong mô-đun :mod:`os` (chỉ trên BSD), hàm :func:`os.open` cung cấp một giải pháp thay thế cho các hàm :func:`lockf` và :func:`flock`.
