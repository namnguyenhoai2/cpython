:mod:`!resource` --- Thông tin sử dụng tài nguyên
=================================================

.. module:: resource
   :synopsis: Một interface cung cấp thông tin sử dụng tài nguyên của tiến trình hiện tại.

.. moduleauthor:: Jeremy Hylton <jeremy@alum.mit.edu>
.. sectionauthor:: Jeremy Hylton <jeremy@alum.mit.edu>

--------------

Module này cung cấp các cơ chế cơ bản để đo lường và kiểm soát tài nguyên hệ thống được một chương trình sử dụng.

.. availability:: Unix, not WASI.

Các hằng số ký hiệu được sử dụng để chỉ định những tài nguyên hệ thống cụ thể và yêu cầu thông tin sử dụng về tiến trình hiện tại hoặc các tiến trình con của nó.

:exc:`OSError` được nêu ra khi syscall thất bại.


.. exception:: error

   Một bí danh đã lỗi thời của :exc:`OSError`.

   .. versionchanged:: 3.3
      Sau :pep:`3151`, class này trở thành bí danh của :exc:`OSError`.


Giới hạn tài nguyên
-------------------

Có thể giới hạn mức sử dụng tài nguyên bằng hàm :func:`setrlimit` được mô tả bên dưới. Mỗi tài nguyên được kiểm soát bằng một cặp giới hạn: giới hạn mềm và giới hạn cứng. Giới hạn mềm là giới hạn hiện tại và một process có thể giảm hoặc tăng giới hạn này theo thời gian. Giới hạn mềm không bao giờ có thể vượt quá giới hạn cứng. Có thể giảm giới hạn cứng xuống bất kỳ giá trị nào lớn hơn giới hạn mềm, nhưng không thể tăng giới hạn này. (Chỉ các process có UID hiệu lực của super-user mới có thể tăng giới hạn cứng.)

Các tài nguyên cụ thể có thể bị giới hạn phụ thuộc vào hệ thống. Chúng được mô tả trong trang man :manpage:`getrlimit(2)`. Các tài nguyên được liệt kê bên dưới được hỗ trợ khi hệ điều hành bên dưới hỗ trợ chúng; các tài nguyên không thể được hệ điều hành kiểm tra hoặc kiểm soát sẽ không được định nghĩa trong module này trên các nền tảng đó.


.. data:: RLIM_INFINITY

   Hằng số dùng để biểu diễn giới hạn của một tài nguyên không giới hạn.


.. function:: getrlimit(resource)

   Trả về một tuple ``(soft, hard)`` chứa các giới hạn mềm và cứng hiện tại của *resource*. Phát sinh :exc:`ValueError` nếu chỉ định một tài nguyên không hợp lệ, hoặc
   :exc:`error` nếu system call bên dưới gặp lỗi không mong đợi.


.. function:: setrlimit(resource, limits)

   Đặt các giới hạn mới về mức tiêu thụ của *resource*. Đối số *limits* phải là một tuple ``(soft, hard)`` gồm hai số nguyên mô tả các giới hạn mới. Một giá trị
   :const:`~resource.RLIM_INFINITY` có thể được sử dụng để yêu cầu một giới hạn không bị giới hạn.

   Phát sinh :exc:`ValueError` nếu chỉ định tài nguyên không hợp lệ, nếu giới hạn mềm mới vượt quá giới hạn cứng, hoặc nếu một tiến trình cố gắng tăng giới hạn cứng của nó. Việc chỉ định giới hạn :const:`~resource.RLIM_INFINITY` khi giới hạn cứng hoặc giới hạn hệ thống cho tài nguyên đó không phải là không bị giới hạn sẽ dẫn đến một
   :exc:`ValueError`. Một tiến trình có UID hiệu dụng của super-user có thể yêu cầu bất kỳ giá trị giới hạn hợp lệ nào, bao gồm cả không bị giới hạn, nhưng :exc:`ValueError` vẫn sẽ được phát sinh nếu giới hạn được yêu cầu vượt quá giới hạn do hệ thống áp đặt.

   ``setrlimit`` cũng có thể phát sinh :exc:`error` nếu system call bên dưới thất bại.

   VxWorks chỉ hỗ trợ thiết lập :const:`RLIMIT_NOFILE`.

   .. audit-event:: resource.setrlimit resource,limits resource.setrlimit


.. function:: prlimit(pid, resource[, limits])

   Kết hợp :func:`setrlimit` và :func:`getrlimit` trong một hàm, đồng thời hỗ trợ lấy và thiết lập giới hạn tài nguyên của một tiến trình bất kỳ. Nếu *pid* bằng 0, lệnh gọi sẽ áp dụng cho tiến trình hiện tại. *resource* và *limits* có cùng ý nghĩa như trong :func:`setrlimit`, ngoại trừ việc *limits* là tùy chọn.

   Khi không cung cấp *limits*, hàm trả về giới hạn *resource* của tiến trình *pid*. Khi cung cấp *limits*, giới hạn *resource* của tiến trình sẽ được thiết lập và giới hạn tài nguyên trước đó được trả về.

   Ném :exc:`ProcessLookupError` khi không tìm thấy *pid* và
   :exc:`PermissionError` khi người dùng không có ``CAP_SYS_RESOURCE`` cho tiến trình.

   .. audit-event:: resource.prlimit pid,resource,limits resource.prlimit

   .. availability:: Linux >= 2.6.36 with glibc >= 2.13.

   .. versionadded:: 3.4


Các ký hiệu này xác định những tài nguyên mà mức tiêu thụ có thể được kiểm soát bằng
các hàm :func:`setrlimit` và :func:`getrlimit` được mô tả bên dưới. Giá trị của các ký hiệu này chính xác là những hằng số được các chương trình C sử dụng.

Trang man Unix về :manpage:`getrlimit(2)` liệt kê các tài nguyên hiện có. Lưu ý rằng không phải tất cả các hệ thống đều sử dụng cùng một ký hiệu hoặc cùng một giá trị để biểu thị cùng một tài nguyên. Mô-đun này không cố gắng che giấu những khác biệt giữa các nền tảng --- các ký hiệu không được định nghĩa cho một nền tảng sẽ không khả dụng từ mô-đun này trên nền tảng đó.


.. data:: RLIMIT_CORE

   Kích thước tối đa (tính bằng byte) của tệp core mà tiến trình hiện tại có thể tạo. Điều này có thể dẫn đến việc tạo một tệp core không đầy đủ nếu cần một tệp core lớn hơn để chứa toàn bộ ảnh tiến trình.


.. data:: RLIMIT_CPU

   Lượng thời gian xử lý tối đa (tính bằng giây) mà một tiến trình có thể sử dụng. Nếu vượt quá giới hạn này, một tín hiệu :const:`~signal.SIGXCPU` sẽ được gửi đến tiến trình. (Xem tài liệu về mô-đun :mod:`signal` để biết cách bắt tín hiệu này và thực hiện điều hữu ích, chẳng hạn như flush các tệp đang mở xuống đĩa.)


.. data:: RLIMIT_FSIZE

   Kích thước tối đa của một tệp mà tiến trình có thể tạo.


.. data:: RLIMIT_DATA

   Kích thước tối đa (tính bằng byte) của heap của tiến trình.


.. data:: RLIMIT_STACK

   Kích thước tối đa (tính bằng byte) của call stack của tiến trình hiện tại. Điều này chỉ ảnh hưởng đến stack của luồng chính trong một tiến trình đa luồng.


.. data:: RLIMIT_RSS

   Kích thước tập thường trú tối đa nên được cung cấp cho tiến trình.


.. data:: RLIMIT_NPROC

   Số lượng tiến trình tối đa mà tiến trình hiện tại có thể tạo.


.. data:: RLIMIT_NOFILE

   Số lượng file descriptor đang mở tối đa của tiến trình hiện tại.


.. data:: RLIMIT_OFILE

   Tên BSD của :const:`RLIMIT_NOFILE`.


.. data:: RLIMIT_MEMLOCK

   Không gian địa chỉ tối đa có thể được khóa trong bộ nhớ.


.. data:: RLIMIT_VMEM

   Vùng bộ nhớ được ánh xạ lớn nhất mà tiến trình có thể chiếm dụng. Thường là bí danh của :const:`RLIMIT_AS`.

   .. availability:: Solaris, FreeBSD, NetBSD.


.. data:: RLIMIT_AS

   Vùng tối đa (tính bằng byte) của không gian địa chỉ mà tiến trình có thể sử dụng.


.. data:: RLIMIT_MSGQUEUE

   Số byte có thể được cấp phát cho các hàng đợi thông báo POSIX.

   .. availability:: Linux >= 2.6.8.

   .. versionadded:: 3.4


.. data:: RLIMIT_NICE

   Mức trần của mức nice của tiến trình (được tính là 20 - rlim_cur).

   .. availability:: Linux >= 2.6.12.

   .. versionadded:: 3.4


.. data:: RLIMIT_RTPRIO

   Mức trần của độ ưu tiên real-time.

   .. availability:: Linux >= 2.6.12.

   .. versionadded:: 3.4


.. data:: RLIMIT_RTTIME

   Giới hạn thời gian (tính bằng micro giây) đối với thời gian CPU mà một tiến trình có thể sử dụng khi lập lịch real-time mà không thực hiện syscall chặn.

   .. availability:: Linux >= 2.6.25.

   .. versionadded:: 3.4


.. data:: RLIMIT_SIGPENDING

   Số lượng tín hiệu mà tiến trình có thể xếp hàng.

   .. availability:: Linux >= 2.6.8.

   .. versionadded:: 3.4


.. data:: RLIMIT_SBSIZE

   Kích thước tối đa (tính bằng byte) của bộ đệm socket mà người dùng này có thể sử dụng. Điều này giới hạn lượng bộ nhớ mạng, và do đó giới hạn số lượng mbuf mà người dùng này có thể giữ tại bất kỳ thời điểm nào.

   .. availability:: FreeBSD, NetBSD.

   .. versionadded:: 3.4


.. data:: RLIMIT_SWAP

   Kích thước tối đa (tính bằng byte) của không gian swap có thể được dành riêng hoặc sử dụng bởi tất cả các tiến trình thuộc ID người dùng này. Giới hạn này chỉ được áp dụng nếu bit 1 của sysctl vm.overcommit được đặt. Vui lòng xem `tuning(7) <https://man.freebsd.org/cgi/man.cgi?query=tuning&sektion=7>`__ để biết mô tả đầy đủ về sysctl này.

   .. availability:: FreeBSD >= 8.

   .. versionadded:: 3.4


.. data:: RLIMIT_NPTS

   Số lượng pseudo-terminal tối đa mà ID người dùng này có thể tạo.

   .. availability:: FreeBSD >= 8.

   .. versionadded:: 3.4


.. data:: RLIMIT_KQUEUES

   Số lượng kqueue tối đa mà ID người dùng này được phép tạo.

   .. availability:: FreeBSD >= 11.

   .. versionadded:: 3.10


Mức sử dụng tài nguyên
----------------------

Các hàm này được dùng để truy xuất thông tin về mức sử dụng tài nguyên:


.. function:: getrusage(who)

   Hàm này trả về một đối tượng mô tả các tài nguyên được tiến trình hiện tại hoặc các tiến trình con của nó sử dụng, như được chỉ định bởi tham số *who*. Tham số *who* phải được chỉ định bằng một trong các hằng số :const:`!RUSAGE_\*` được mô tả bên dưới.

   Một ví dụ đơn giản::

      from resource import *
      import time

      # một tác vụ không bị giới hạn bởi CPU
      time.sleep(3)
      print(getrusage(RUSAGE_SELF))

      # một tác vụ bị giới hạn bởi CPU
      for i in range(10 ** 8):
         _ = 1 + 1
      print(getrusage(RUSAGE_SELF))

   Mỗi trường trong giá trị trả về mô tả cách một tài nguyên hệ thống cụ thể được sử dụng, chẳng hạn như lượng thời gian chạy ở chế độ người dùng hoặc số lần tiến trình bị hoán đổi khỏi bộ nhớ chính. Một số giá trị phụ thuộc vào khoảng thời gian của nhịp đồng hồ, chẳng hạn như lượng bộ nhớ mà tiến trình đang sử dụng.

   Để đảm bảo khả năng tương thích ngược, giá trị trả về cũng có thể được truy cập dưới dạng một tuple gồm 16 phần tử.

   Các trường :attr:`!ru_utime` và :attr:`!ru_stime` của giá trị trả về là các giá trị dấu phẩy động, lần lượt biểu thị lượng thời gian thực thi ở chế độ người dùng và lượng thời gian thực thi ở chế độ hệ thống. Các giá trị còn lại là số nguyên. Hãy tham khảo trang hướng dẫn :manpage:`getrusage(2)` để biết thông tin chi tiết về các giá trị này. Dưới đây là phần tóm tắt ngắn gọn:

   +---------+----------------------+---------------------------------------------------+
   | Chỉ mục | Trường               | Tài nguyên                                        |
   +=========+======================+===================================================+
   | ``0``   | :attr:`!ru_utime`    | thời gian ở chế độ người dùng (giây dạng số thực) |
   +---------+----------------------+---------------------------------------------------+
   | ``1``   | :attr:`!ru_stime`    | thời gian ở chế độ hệ thống (giây dạng số thực)   |
   +---------+----------------------+---------------------------------------------------+
   | ``2``   | :attr:`!ru_maxrss`   | kích thước tối đa của tập cư trú                  |
   +---------+----------------------+---------------------------------------------------+
   | ``3``   | :attr:`!ru_ixrss`    | kích thước bộ nhớ dùng chung                      |
   +---------+----------------------+---------------------------------------------------+
   | ``4``   | :attr:`!ru_idrss`    | kích thước bộ nhớ không chia sẻ                   |
   +---------+----------------------+---------------------------------------------------+
   | ``5``   | :attr:`!ru_isrss`    | kích thước ngăn xếp không chia sẻ                 |
   +---------+----------------------+---------------------------------------------------+
   | ``6``   | :attr:`!ru_minflt`   | lỗi trang không yêu cầu I/O                       |
   +---------+----------------------+---------------------------------------------------+
   | ``7``   | :attr:`!ru_majflt`   | lỗi trang yêu cầu I/O                             |
   +---------+----------------------+---------------------------------------------------+
   | ``8``   | :attr:`!ru_nswap`    | số lần đưa ra bộ nhớ hoán đổi                     |
   +---------+----------------------+---------------------------------------------------+
   | ``9``   | :attr:`!ru_inblock`  | các thao tác nhập theo khối                       |
   +---------+----------------------+---------------------------------------------------+
   | ``10``  | :attr:`!ru_oublock`  | các thao tác xuất theo khối                       |
   +---------+----------------------+---------------------------------------------------+
   | ``11``  | :attr:`!ru_msgsnd`   | tin nhắn đã gửi                                   |
   +---------+----------------------+---------------------------------------------------+
   | ``12``  | :attr:`!ru_msgrcv`   | tin nhắn đã nhận                                  |
   +---------+----------------------+---------------------------------------------------+
   | ``13``  | :attr:`!ru_nsignals` | tín hiệu đã nhận                                  |
   +---------+----------------------+---------------------------------------------------+
   | ``14``  | :attr:`!ru_nvcsw`    | chuyển đổi ngữ cảnh tự nguyện                     |
   +---------+----------------------+---------------------------------------------------+
   | ``15``  | :attr:`!ru_nivcsw`   | chuyển đổi ngữ cảnh không tự nguyện               |
   +---------+----------------------+---------------------------------------------------+

   Hàm này sẽ phát sinh :exc:`ValueError` nếu chỉ định tham số *who* không hợp lệ. Hàm cũng có thể phát sinh ngoại lệ :exc:`error` trong những trường hợp bất thường.


.. function:: getpagesize()

   Trả về số byte trong một trang hệ thống. (Kích thước này không nhất thiết giống với kích thước trang phần cứng.)

Các ký hiệu :const:`!RUSAGE_\*` sau được truyền vào hàm :func:`getrusage` để chỉ định thông tin của những tiến trình nào cần được cung cấp.


.. data:: RUSAGE_SELF

   Truyền :func:`getrusage` vào để yêu cầu các tài nguyên mà tiến trình gọi đã sử dụng, tức là tổng tài nguyên được tất cả các thread trong tiến trình sử dụng.


.. data:: RUSAGE_CHILDREN

   Truyền :func:`getrusage` vào để yêu cầu các tài nguyên mà những tiến trình con của tiến trình gọi đã sử dụng, với điều kiện các tiến trình đó đã kết thúc và được chờ.


.. data:: RUSAGE_BOTH

   Truyền :func:`getrusage` vào để yêu cầu các tài nguyên mà cả tiến trình hiện tại và các tiến trình con đã sử dụng. Có thể không khả dụng trên mọi hệ thống.


.. data:: RUSAGE_THREAD

   Truyền :func:`getrusage` vào để yêu cầu các tài nguyên mà thread hiện tại đã sử dụng. Có thể không khả dụng trên mọi hệ thống.

   .. versionadded:: 3.2
