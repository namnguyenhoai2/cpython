:mod:`!select` --- Chờ hoàn tất I/O
===================================

.. module:: select
   :synopsis: Chờ hoàn tất I/O trên nhiều luồng.

--------------

Mô-đun này cung cấp quyền truy cập vào các hàm :c:func:`!select` và :c:func:`!poll` có sẵn trong hầu hết các hệ điều hành, :c:func:`!devpoll` có sẵn trên Solaris và các hệ điều hành phái sinh, :c:func:`!epoll` có sẵn trên Linux 2.5 trở lên và
:c:func:`!kqueue` có sẵn trên hầu hết các hệ điều hành BSD. Lưu ý rằng trên Windows, hàm này chỉ hoạt động với socket; trên các hệ điều hành khác, hàm này cũng hoạt động với các loại tệp khác (đặc biệt là trên Unix, hàm này hoạt động với pipe). Không thể sử dụng hàm này trên các tệp thông thường để xác định xem tệp có tăng kích thước kể từ lần đọc gần nhất hay không.

.. note::

   Mô-đun :mod:`selectors` cho phép ghép kênh I/O hiệu quả ở cấp cao, được xây dựng dựa trên các primitive của mô-đun :mod:`!select`. Người dùng nên sử dụng mô-đun :mod:`selectors` thay thế, trừ khi họ muốn kiểm soát chính xác các primitive ở cấp hệ điều hành được sử dụng.

.. include:: ../includes/wasm-notavail.rst

Mô-đun này định nghĩa các thành phần sau:


.. exception:: error

   Bí danh đã lỗi thời của :exc:`OSError`.

   .. versionchanged:: 3.3
      Sau :pep:`3151`, lớp này trở thành bí danh của :exc:`OSError`.


.. function:: devpoll()

   Trả về một đối tượng polling ``/dev/poll``; xem phần :ref:`devpoll-objects` bên dưới để biết các phương thức được devpoll objects hỗ trợ.

   Các đối tượng :c:func:`!devpoll` được liên kết với số lượng file descriptor được cho phép tại thời điểm khởi tạo. Nếu chương trình của bạn giảm giá trị này, :c:func:`!devpoll` sẽ thất bại. Nếu chương trình của bạn tăng giá trị này, :c:func:`!devpoll` có thể trả về danh sách file descriptor đang hoạt động không đầy đủ.

   File descriptor mới là :ref:`không kế thừa <fd_inheritance>`.

   .. versionadded:: 3.3

   .. versionchanged:: 3.4
      File descriptor mới hiện không thể kế thừa.

   .. availability:: Solaris.

.. function:: epoll(sizehint=-1, flags=0)

   Trả về một đối tượng polling theo edge, có thể được dùng làm giao diện Edge hoặc Level Triggered cho các sự kiện I/O.

   *sizehint* thông báo cho epoll về số lượng sự kiện dự kiến sẽ được đăng ký. Giá trị này phải dương hoặc là ``-1`` để sử dụng giá trị mặc định. Nó chỉ được dùng trên các hệ thống cũ, nơi :c:func:`!epoll_create1` không khả dụng; nếu không thì không có tác dụng (mặc dù giá trị của nó vẫn được kiểm tra).

   *flags* đã lỗi thời và hoàn toàn bị bỏ qua. Tuy nhiên, khi được cung cấp, giá trị của nó phải là ``0`` hoặc ``select.EPOLL_CLOEXEC``, nếu không sẽ phát sinh ``OSError``.

   Xem phần :ref:`epoll-objects` bên dưới để biết các phương thức được các đối tượng epoll hỗ trợ.

   Các đối tượng ``epoll`` hỗ trợ giao thức quản lý ngữ cảnh: khi được sử dụng trong một
   câu lệnh :keyword:`with`, bộ mô tả tệp mới sẽ tự động được đóng khi kết thúc khối.

   File descriptor mới là :ref:`không kế thừa <fd_inheritance>`.

   .. versionchanged:: 3.3
      Đã thêm tham số *flags*.

   .. versionchanged:: 3.4
      Đã thêm hỗ trợ cho câu lệnh :keyword:`with`. Bộ mô tả tệp mới hiện không thể kế thừa.

   .. deprecated:: 3.4
      Tham số *flags*. ``select.EPOLL_CLOEXEC`` hiện được sử dụng theo mặc định. Sử dụng :func:`os.set_inheritable` để khiến file descriptor có thể được kế thừa.

   .. availability:: Linux >= 2.5.44.


.. function:: poll()

   Trả về một đối tượng polling, hỗ trợ đăng ký và hủy đăng ký các file descriptor, sau đó polling chúng để tìm các sự kiện I/O; xem phần :ref:`poll-objects` bên dưới để biết các phương thức được các đối tượng polling hỗ trợ.

   .. availability:: Unix.


.. function:: kqueue()

   Trả về một đối tượng hàng đợi kernel; xem phần
   :ref:`kqueue-objects` bên dưới để biết các phương thức được các đối tượng kqueue hỗ trợ.

   File descriptor mới là :ref:`không kế thừa <fd_inheritance>`.

   .. versionchanged:: 3.4
      File descriptor mới hiện không thể kế thừa.

   .. availability:: BSD, macOS.


.. function:: kevent(ident, filter=KQ_FILTER_READ, flags=KQ_EV_ADD, fflags=0, data=0, udata=0)

   Trả về một đối tượng sự kiện kernel; xem phần
   :ref:`kevent-objects` bên dưới để xem các phương thức được hỗ trợ cho các đối tượng kevent.

   .. availability:: BSD, macOS.


.. function:: select(rlist, wlist, xlist, timeout=None)

   Đây là một giao diện đơn giản cho lời gọi hệ thống Unix :c:func:`!select`. Ba đối số đầu tiên là các iterable gồm "đối tượng có thể chờ": hoặc là các số nguyên biểu thị bộ mô tả tệp, hoặc là các đối tượng có một phương thức không có tham số tên :meth:`~io.IOBase.fileno`, trả về một số nguyên như vậy:

   * *rlist*: chờ đến khi sẵn sàng để đọc
   * *wlist*: chờ đến khi sẵn sàng để ghi
   * *xlist*: chờ một "điều kiện bất thường" (xem trang hướng dẫn để biết hệ thống của bạn xem điều gì là một điều kiện như vậy)

   Có thể sử dụng các iterable rỗng, nhưng việc chấp nhận ba iterable rỗng phụ thuộc vào nền tảng. (Tính năng này được biết là hoạt động trên Unix nhưng không hoạt động trên Windows.) Đối số tùy chọn *timeout* chỉ định thời gian chờ dưới dạng số thực tính bằng giây. Khi bỏ qua đối số *timeout* hoặc đối số này là ``None``, hàm sẽ chặn cho đến khi ít nhất một bộ mô tả tệp sẵn sàng. Giá trị thời gian chờ bằng 0 chỉ định một lần thăm dò và không bao giờ chặn.

   Giá trị trả về là một bộ ba danh sách gồm các đối tượng đã sẵn sàng: các tập con của ba đối số đầu tiên. Khi hết thời gian chờ mà không có bộ mô tả tệp nào sẵn sàng, ba danh sách rỗng sẽ được trả về.

   .. index::
      single: socket() (in module socket)
      single: popen() (in module os)

   Trong số các kiểu đối tượng có thể chấp nhận được trong các iterable là :term:`các đối tượng file <file object>` của Python (ví dụ ``sys.stdin``, hoặc các đối tượng được trả về bởi
   :func:`open` hoặc :func:`os.popen`), các đối tượng socket được trả về bởi
   :func:`socket.socket`. Bạn cũng có thể tự định nghĩa một lớp :dfn:`wrapper`, miễn là lớp đó có phương thức :meth:`~io.IOBase.fileno` phù hợp (thực sự trả về một file descriptor, chứ không chỉ là một số nguyên bất kỳ).

   .. note::

      .. index:: single: WinSock

      Các đối tượng file trên Windows không được chấp nhận, nhưng socket thì được. Trên Windows, hàm :c:func:`!select` cơ sở được cung cấp bởi thư viện WinSock và không xử lý các file descriptor không bắt nguồn từ WinSock.

   .. versionchanged:: 3.5
      Giờ đây, hàm sẽ được thử lại với timeout được tính toán lại khi bị gián đoạn bởi một signal, trừ khi trình xử lý signal raise một exception (xem
      :pep:`475` để biết lý do), thay vì raise
      :exc:`InterruptedError`.


.. data:: PIPE_BUF

   Số byte tối thiểu có thể được ghi mà không chặn vào một pipe khi pipe đã được :func:`~select.select` báo là sẵn sàng để ghi,
   :func:`!poll` hoặc một interface khác trong module này. Điều này không áp dụng cho các loại đối tượng dạng tệp khác, chẳng hạn như socket.

   POSIX đảm bảo giá trị này ít nhất là 512.

   .. availability:: Unix

   .. versionadded:: 3.2


.. _devpoll-objects:

``/dev/poll`` các đối tượng polling
-----------------------------------

Solaris và các hệ dẫn xuất có ``/dev/poll``. Trong khi :c:func:`!select` là *O*\ (*highest file descriptor*) và :c:func:`!poll` là *O*\ (*number of file descriptors*), ``/dev/poll`` là *O*\ (*active file descriptors*).

Hành vi của ``/dev/poll`` rất gần với đối tượng :c:func:`!poll` tiêu chuẩn.


.. method:: devpoll.close()

   Đóng file descriptor của đối tượng polling.

   .. versionadded:: 3.4


.. attribute:: devpoll.closed

   ``True`` nếu đối tượng polling đã bị đóng.

   .. versionadded:: 3.4


.. method:: devpoll.fileno()

   Trả về số bộ mô tả tệp của đối tượng polling.

   .. versionadded:: 3.4


.. method:: devpoll.register(fd[, eventmask])

   Đăng ký một bộ mô tả tệp với đối tượng polling. Các lần gọi sau đến
   :meth:`poll` phương thức sẽ kiểm tra xem bộ mô tả tệp có sự kiện I/O nào đang chờ xử lý hay không. *fd* có thể là một số nguyên hoặc một đối tượng có
   :meth:`~io.IOBase.fileno` phương thức trả về một số nguyên. Các đối tượng tệp triển khai :meth:`!fileno`, vì vậy chúng cũng có thể được dùng làm đối số.

   *eventmask* là một bitmask tùy chọn mô tả loại sự kiện bạn muốn kiểm tra. Các hằng số giống với các hằng số của đối tượng :c:func:`!poll`. Giá trị mặc định là sự kết hợp của các hằng số :const:`POLLIN`,
   :const:`POLLPRI`, và :const:`POLLOUT`.

   .. warning::

      Việc đăng ký một bộ mô tả tệp đã được đăng ký không phải là lỗi, nhưng kết quả không được xác định. Cách xử lý phù hợp là hủy đăng ký hoặc sửa đổi nó trước. Đây là một điểm khác biệt quan trọng so với :c:func:`!poll`.


.. method:: devpoll.modify(fd[, eventmask])

   Phương thức này thực hiện một :meth:`unregister` rồi đến một
   :meth:`register`. Phương thức này (hơi) hiệu quả hơn so với việc thực hiện hai thao tác đó một cách tường minh.


.. method:: devpoll.unregister(fd)

   Xóa một file descriptor đang được một polling object theo dõi. Cũng giống như
   phương thức :meth:`register`, *fd* có thể là một số nguyên hoặc một object có
   phương thức :meth:`~io.IOBase.fileno` trả về một số nguyên.

   Việc cố gắng xóa một file descriptor chưa từng được đăng ký sẽ được bỏ qua một cách an toàn.


.. method:: devpoll.poll([timeout])

   Thăm dò tập hợp các file descriptor đã đăng ký và trả về một danh sách có thể rỗng, chứa các bộ 2 phần tử ``(fd, event)`` cho những descriptor có sự kiện hoặc lỗi cần báo cáo. *fd* là file descriptor, còn *event* là một bitmask với các bit được đặt tương ứng với những sự kiện được báo cáo cho descriptor đó --- :const:`POLLIN` để chờ đầu vào, :const:`POLLOUT` cho biết descriptor có thể được ghi vào, v.v. Một danh sách rỗng cho biết lệnh gọi đã hết thời gian chờ và không có file descriptor nào có sự kiện cần báo cáo. Nếu cung cấp *timeout*, giá trị này chỉ khoảng thời gian tính bằng mili giây mà hệ thống sẽ chờ sự kiện trước khi trả về. Nếu bỏ qua *timeout*, đặt là -1 hoặc :const:`None`, lệnh gọi sẽ chặn cho đến khi có một sự kiện dành cho polling object này.

   .. versionchanged:: 3.5
      Hàm hiện được thử lại với thời gian chờ được tính toán lại khi bị ngắt bởi một tín hiệu, trừ khi bộ xử lý tín hiệu phát sinh một ngoại lệ (xem
      :pep:`475` để biết lý do), thay vì phát sinh
      :exc:`InterruptedError`.


.. _epoll-objects:

Đối tượng polling theo edge và level (epoll)
--------------------------------------------

   https://linux.die.net/man/4/epoll

   *eventmask* là một bit mask sử dụng các hằng số sau:

   +-------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | Hằng số                 | Ý nghĩa                                                                                                                                                          |
   +=========================+==================================================================================================================================================================+
   | :const:`EPOLLIN`        | Có sẵn để đọc.                                                                                                                                                   |
   +-------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | :const:`EPOLLOUT`       | Có thể ghi.                                                                                                                                                      |
   +-------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | :const:`EPOLLPRI`       | Dữ liệu khẩn cấp để đọc.                                                                                                                                         |
   +-------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | :const:`EPOLLERR`       | Đã xảy ra điều kiện lỗi trên fd liên kết.                                                                                                                        |
   +-------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | :const:`EPOLLHUP`       | Đã xảy ra ngắt kết nối trên fd liên kết.                                                                                                                         |
   +-------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | :const:`EPOLLET`        | Bật hành vi Edge Trigger; mặc định là hành vi Level Trigger.                                                                                                     |
   +-------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | :const:`EPOLLONESHOT`   | Bật hành vi one-shot. Sau khi một sự kiện được lấy ra, fd sẽ bị vô hiệu hóa nội bộ.                                                                              |
   +-------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | :const:`EPOLLEXCLUSIVE` | Chỉ đánh thức một đối tượng epoll khi fd liên kết có sự kiện. Mặc định (nếu cờ này không được đặt) là đánh thức tất cả đối tượng epoll đang polling trên một fd. |
   +-------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | :const:`EPOLLRDHUP`     | Socket stream đã đóng kết nối hoặc ngừng ghi ở một nửa kết nối.                                                                                                  |
   +-------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | :const:`EPOLLRDNORM`    | Tương đương với :const:`EPOLLIN`                                                                                                                                 |
   +-------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | :const:`EPOLLRDBAND`    | Có thể đọc dải dữ liệu ưu tiên.                                                                                                                                  |
   +-------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | :const:`EPOLLWRNORM`    | Tương đương với :const:`EPOLLOUT`.                                                                                                                               |
   +-------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | :const:`EPOLLWRBAND`    | Có thể ghi dữ liệu ưu tiên.                                                                                                                                      |
   +-------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | :const:`EPOLLMSG`       | Bị bỏ qua.                                                                                                                                                       |
   +-------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | :const:`EPOLLWAKEUP`    | Ngăn chế độ ngủ trong khi chờ sự kiện.                                                                                                                           |
   +-------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------+

   .. versionadded:: 3.6
      :const:`EPOLLEXCLUSIVE` was added.  It's only supported by Linux Kernel 4.5
      hoặc mới hơn.

   .. versionadded:: 3.14
      :const:`EPOLLWAKEUP` was added. It's only supported by Linux Kernel 3.5
      hoặc mới hơn.

.. method:: epoll.close()

   Đóng file descriptor điều khiển của đối tượng epoll.


.. attribute:: epoll.closed

   ``True`` nếu đối tượng epoll bị đóng.


.. method:: epoll.fileno()

   Trả về số file descriptor của fd điều khiển.


.. method:: epoll.fromfd(fd)

   Tạo một đối tượng epoll từ file descriptor đã cho.


.. method:: epoll.register(fd[, eventmask])

   Đăng ký một file descriptor *fd* với đối tượng epoll.


.. method:: epoll.modify(fd, eventmask)

   Sửa đổi một file descriptor đã đăng ký *fd*.


.. method:: epoll.unregister(fd)

   Xóa một file descriptor đã đăng ký khỏi đối tượng epoll.

   .. versionchanged:: 3.9
      Phương thức không còn bỏ qua lỗi :data:`~errno.EBADF`.


.. method:: epoll.poll(timeout=None, maxevents=-1)

   Chờ các sự kiện. timeout tính bằng giây (float)

   .. versionchanged:: 3.5
      Hàm hiện được thử lại với timeout được tính toán lại khi bị gián đoạn bởi một signal, ngoại trừ khi signal handler tạo ra một exception (xem
      :pep:`475` để biết lý do), thay vì tạo ra
      :exc:`InterruptedError`.


.. _poll-objects:

Các đối tượng polling
---------------------

Lệnh gọi hệ thống :c:func:`!poll`, được hầu hết các hệ thống Unix hỗ trợ, có khả năng mở rộng tốt hơn cho các máy chủ mạng phục vụ rất nhiều máy khách cùng lúc. :c:func:`!poll` có khả năng mở rộng tốt hơn vì lệnh gọi hệ thống này chỉ yêu cầu liệt kê các bộ mô tả tệp cần quan tâm, trong khi :c:func:`!select` xây dựng một bitmap, bật các bit tương ứng với các fd cần quan tâm, rồi sau đó phải quét tuyến tính toàn bộ bitmap một lần nữa. :c:func:`!select` có độ phức tạp *O*\ (*bộ mô tả tệp lớn nhất*), trong khi
:c:func:`!poll` có độ phức tạp *O*\ (*số lượng bộ mô tả tệp*).


.. method:: poll.register(fd[, eventmask])

   Đăng ký một bộ mô tả tệp với đối tượng polling. Các lần gọi sau này đến phương thức
   :meth:`poll` sẽ kiểm tra xem bộ mô tả tệp đó có sự kiện I/O nào đang chờ xử lý hay không. *fd* có thể là một số nguyên hoặc một đối tượng có phương thức
   :meth:`~io.IOBase.fileno` trả về một số nguyên. Các đối tượng tệp triển khai :meth:`!fileno`, vì vậy chúng cũng có thể được dùng làm đối số.

   *eventmask* là một bitmask tùy chọn mô tả loại sự kiện bạn muốn kiểm tra và có thể là sự kết hợp của các hằng số :const:`POLLIN`,
   :const:`POLLPRI`, và :const:`POLLOUT`, được mô tả trong bảng bên dưới. Nếu không được chỉ định, giá trị mặc định sẽ được dùng để kiểm tra cả 3 loại sự kiện.

   +--------------------+---------------------------------------------------------------------------+
   | Hằng số            | Ý nghĩa                                                                   |
   +====================+===========================================================================+
   | :const:`POLLIN`    | Có dữ liệu để đọc.                                                        |
   +--------------------+---------------------------------------------------------------------------+
   | :const:`POLLPRI`   | Có dữ liệu khẩn cấp để đọc.                                               |
   +--------------------+---------------------------------------------------------------------------+
   | :const:`POLLOUT`   | Sẵn sàng xuất dữ liệu: thao tác ghi sẽ không bị chặn.                     |
   +--------------------+---------------------------------------------------------------------------+
   | :const:`POLLERR`   | Đã xảy ra một dạng lỗi nào đó.                                            |
   +--------------------+---------------------------------------------------------------------------+
   | :const:`POLLHUP`   | Đã ngắt kết nối.                                                          |
   +--------------------+---------------------------------------------------------------------------+
   | :const:`POLLRDHUP` | Socket stream đóng kết nối ngang hàng hoặc ngừng ghi vào một nửa kết nối. |
   +--------------------+---------------------------------------------------------------------------+
   | :const:`POLLNVAL`  | Yêu cầu không hợp lệ: descriptor chưa được mở.                            |
   +--------------------+---------------------------------------------------------------------------+

   Việc đăng ký một file descriptor đã được đăng ký không phải là lỗi và có tác dụng giống như đăng ký descriptor đó đúng một lần.


.. method:: poll.modify(fd, eventmask)

   Sửa đổi một fd đã được đăng ký. Điều này có tác dụng giống như ``register(fd, eventmask)``. Việc cố gắng sửa đổi một file descriptor chưa từng được đăng ký sẽ gây ra một ngoại lệ :exc:`OSError` với errno
   :const:`ENOENT`.


.. method:: poll.unregister(fd)

   Xóa một file descriptor đang được một polling object theo dõi. Cũng giống như phương thức
   :meth:`register`, *fd* có thể là một số nguyên hoặc một object có
   Phương thức :meth:`~io.IOBase.fileno` trả về một số nguyên.

   Việc cố gắng xóa một bộ mô tả tệp chưa từng được đăng ký sẽ làm phát sinh
   ngoại lệ :exc:`KeyError`.


.. method:: poll.poll([timeout])

   Thăm dò tập hợp các bộ mô tả tệp đã đăng ký và trả về một danh sách có thể rỗng, chứa các bộ 2 phần tử ``(fd, event)`` đối với những bộ mô tả có sự kiện hoặc lỗi cần báo cáo. *fd* là bộ mô tả tệp, còn *event* là một bitmask với các bit được đặt tương ứng với những sự kiện được báo cáo cho bộ mô tả đó --- :const:`POLLIN` để chờ dữ liệu đầu vào, :const:`POLLOUT` để cho biết bộ mô tả có thể được ghi, v.v. Danh sách rỗng cho biết lệnh gọi đã hết thời gian chờ và không có bộ mô tả tệp nào có sự kiện cần báo cáo. Nếu cung cấp *timeout*, giá trị này chỉ khoảng thời gian tính bằng mili giây mà hệ thống sẽ chờ sự kiện trước khi trả về. Nếu *timeout* bị bỏ qua, là số âm hoặc là :const:`None`, lệnh gọi sẽ chặn cho đến khi có sự kiện đối với đối tượng poll này.

   .. versionchanged:: 3.5
      Hàm hiện sẽ được thử lại với thời gian chờ được tính toán lại khi bị gián đoạn bởi một signal, trừ khi trình xử lý signal phát sinh một ngoại lệ (xem
      :pep:`475` để biết lý do), thay vì phát sinh
      :exc:`InterruptedError`.


.. _kqueue-objects:

Đối tượng Kqueue
----------------

.. method:: kqueue.close()

   Đóng file descriptor điều khiển của đối tượng kqueue.


.. attribute:: kqueue.closed

   ``True`` nếu đối tượng kqueue được đóng.


.. method:: kqueue.fileno()

   Trả về số file descriptor của control fd.


.. method:: kqueue.fromfd(fd)

   Tạo một đối tượng kqueue từ file descriptor được cung cấp.


.. method:: kqueue.control(changelist, max_events[, timeout]) -> eventlist

   Giao diện cấp thấp cho kevent

   - changelist phải là một iterable gồm các đối tượng kevent hoặc ``None``
   - max_events phải là 0 hoặc một số nguyên dương
   - thời gian chờ tính bằng giây (có thể là số thực); mặc định là ``None``, để chờ vô thời hạn

   .. versionchanged:: 3.5
      Hàm hiện sẽ được thử lại với thời gian chờ được tính toán lại khi bị gián đoạn bởi một signal, trừ khi trình xử lý signal phát sinh một ngoại lệ (xem
      :pep:`475` để biết lý do), thay vì phát sinh
      :exc:`InterruptedError`.


.. _kevent-objects:

Đối tượng Kevent
----------------

https://man.freebsd.org/cgi/man.cgi?query=kqueue&sektion=2

.. attribute:: kevent.ident

   Giá trị dùng để xác định event. Cách diễn giải phụ thuộc vào filter, nhưng thường là file descriptor. Trong constructor, ident có thể là một int hoặc một object có phương thức :meth:`~io.IOBase.fileno`. kevent lưu trữ số nguyên này ở bên trong.

.. attribute:: kevent.filter

   Tên của kernel filter.

   +---------------------------+-------------------------------------------------------------------------------+
   | Hằng số                   | Ý nghĩa                                                                       |
   +===========================+===============================================================================+
   | :const:`KQ_FILTER_READ`   | Nhận một descriptor và trả về bất cứ khi nào có dữ liệu sẵn sàng để đọc.      |
   +---------------------------+-------------------------------------------------------------------------------+
   | :const:`KQ_FILTER_WRITE`  | Nhận một descriptor và trả về bất cứ khi nào có dữ liệu sẵn sàng để ghi.      |
   +---------------------------+-------------------------------------------------------------------------------+
   | :const:`KQ_FILTER_AIO`    | Các yêu cầu AIO.                                                              |
   +---------------------------+-------------------------------------------------------------------------------+
   | :const:`KQ_FILTER_VNODE`  | Trả về khi xảy ra một hoặc nhiều sự kiện được yêu cầu theo dõi trong *fflag*. |
   +---------------------------+-------------------------------------------------------------------------------+
   | :const:`KQ_FILTER_PROC`   | Theo dõi các sự kiện trên một ID tiến trình.                                  |
   +---------------------------+-------------------------------------------------------------------------------+
   | :const:`KQ_FILTER_NETDEV` | Theo dõi các sự kiện trên một thiết bị mạng (không khả dụng trên macOS).      |
   +---------------------------+-------------------------------------------------------------------------------+
   | :const:`KQ_FILTER_SIGNAL` | Được trả về bất cứ khi nào tín hiệu được theo dõi được gửi đến tiến trình.    |
   +---------------------------+-------------------------------------------------------------------------------+
   | :const:`KQ_FILTER_TIMER`  | Thiết lập một bộ hẹn giờ tùy ý.                                               |
   +---------------------------+-------------------------------------------------------------------------------+

.. attribute:: kevent.flags

   Hành động lọc.

   +-------------------------+-----------------------------------------+
   | Hằng số                 | Ý nghĩa                                 |
   +=========================+=========================================+
   | :const:`KQ_EV_ADD`      | Thêm hoặc sửa đổi một sự kiện.          |
   +-------------------------+-----------------------------------------+
   | :const:`KQ_EV_DELETE`   | Xóa một sự kiện khỏi hàng đợi.          |
   +-------------------------+-----------------------------------------+
   | :const:`KQ_EV_ENABLE`   | Cho phép control() trả về sự kiện.      |
   +-------------------------+-----------------------------------------+
   | :const:`KQ_EV_DISABLE`  | Vô hiệu hóa sự kiện.                    |
   +-------------------------+-----------------------------------------+
   | :const:`KQ_EV_ONESHOT`  | Xóa sự kiện sau lần xuất hiện đầu tiên. |
   +-------------------------+-----------------------------------------+
   | :const:`KQ_EV_CLEAR`    | Đặt lại trạng thái sau khi lấy sự kiện. |
   +-------------------------+-----------------------------------------+
   | :const:`KQ_EV_SYSFLAGS` | Sự kiện nội bộ.                         |
   +-------------------------+-----------------------------------------+
   | :const:`KQ_EV_FLAG1`    | Sự kiện nội bộ.                         |
   +-------------------------+-----------------------------------------+
   | :const:`KQ_EV_EOF`      | Điều kiện EOF dành riêng cho filter.    |
   +-------------------------+-----------------------------------------+
   | :const:`KQ_EV_ERROR`    | Xem các giá trị trả về.                 |
   +-------------------------+-----------------------------------------+


.. attribute:: kevent.fflags

   Các cờ dành riêng cho bộ lọc.

   :const:`KQ_FILTER_READ` và  :const:`KQ_FILTER_WRITE` các cờ của bộ lọc:

   +------------------------+--------------------------------+
   | Hằng số                | Ý nghĩa                        |
   +========================+================================+
   | :const:`KQ_NOTE_LOWAT` | Ngưỡng thấp của bộ đệm socket. |
   +------------------------+--------------------------------+

   :const:`KQ_FILTER_VNODE` các cờ của bộ lọc:

   +-------------------------+---------------------------------------+
   | Hằng số                 | Ý nghĩa                               |
   +=========================+=======================================+
   | :const:`KQ_NOTE_DELETE` | Đã gọi *unlink()*.                    |
   +-------------------------+---------------------------------------+
   | :const:`KQ_NOTE_WRITE`  | Đã xảy ra thao tác ghi.               |
   +-------------------------+---------------------------------------+
   | :const:`KQ_NOTE_EXTEND` | Tệp đã được mở rộng.                  |
   +-------------------------+---------------------------------------+
   | :const:`KQ_NOTE_ATTRIB` | Một thuộc tính đã được thay đổi.      |
   +-------------------------+---------------------------------------+
   | :const:`KQ_NOTE_LINK`   | Số lượng liên kết đã thay đổi.        |
   +-------------------------+---------------------------------------+
   | :const:`KQ_NOTE_RENAME` | Tệp đã được đổi tên.                  |
   +-------------------------+---------------------------------------+
   | :const:`KQ_NOTE_REVOKE` | Quyền truy cập vào tệp đã bị thu hồi. |
   +-------------------------+---------------------------------------+

   Các cờ filter của :const:`KQ_FILTER_PROC`:

   +----------------------------+--------------------------------------------------------+
   | Hằng số                    | Ý nghĩa                                                |
   +============================+========================================================+
   | :const:`KQ_NOTE_EXIT`      | Tiến trình đã thoát.                                   |
   +----------------------------+--------------------------------------------------------+
   | :const:`KQ_NOTE_FORK`      | Tiến trình đã gọi *fork()*.                            |
   +----------------------------+--------------------------------------------------------+
   | :const:`KQ_NOTE_EXEC`      | Tiến trình đã thực thi một tiến trình mới.             |
   +----------------------------+--------------------------------------------------------+
   | :const:`KQ_NOTE_PCTRLMASK` | Cờ bộ lọc nội bộ.                                      |
   +----------------------------+--------------------------------------------------------+
   | :const:`KQ_NOTE_PDATAMASK` | Cờ bộ lọc nội bộ.                                      |
   +----------------------------+--------------------------------------------------------+
   | :const:`KQ_NOTE_TRACK`     | Theo dõi một tiến trình qua *fork()*.                  |
   +----------------------------+--------------------------------------------------------+
   | :const:`KQ_NOTE_CHILD`     | Được trả về trên tiến trình con khi dùng *NOTE_TRACK*. |
   +----------------------------+--------------------------------------------------------+
   | :const:`KQ_NOTE_TRACKERR`  | Không thể đính kèm vào tiến trình con.                 |
   +----------------------------+--------------------------------------------------------+

   Cờ bộ lọc :const:`KQ_FILTER_NETDEV` (không khả dụng trên macOS):

   +---------------------------+-----------------------------------+
   | Hằng số                   | Ý nghĩa                           |
   +===========================+===================================+
   | :const:`KQ_NOTE_LINKUP`   | Liên kết đang hoạt động.          |
   +---------------------------+-----------------------------------+
   | :const:`KQ_NOTE_LINKDOWN` | Liên kết không hoạt động.         |
   +---------------------------+-----------------------------------+
   | :const:`KQ_NOTE_LINKINV`  | Trạng thái liên kết không hợp lệ. |
   +---------------------------+-----------------------------------+


.. attribute:: kevent.data

   Dữ liệu dành riêng cho bộ lọc.


.. attribute:: kevent.udata

   Giá trị do người dùng định nghĩa.
