:mod:`!signal` --- Thiết lập trình xử lý cho các sự kiện bất đồng bộ
====================================================================

.. module:: signal
   :synopsis: Thiết lập trình xử lý cho các sự kiện bất đồng bộ.

**Mã nguồn:** :source:`Lib/signal.py`

--------------

Mô-đun này cung cấp các cơ chế để sử dụng trình xử lý signal trong Python.


Các quy tắc chung
-----------------

Hàm :func:`signal.signal` cho phép định nghĩa các trình xử lý tùy chỉnh để thực thi khi nhận được một signal. Một số ít trình xử lý mặc định được cài đặt: :const:`SIGPIPE` bị bỏ qua (vì vậy các lỗi ghi vào pipe và socket có thể được báo cáo dưới dạng các ngoại lệ Python thông thường) và :const:`SIGINT` được chuyển thành một ngoại lệ :exc:`KeyboardInterrupt` nếu tiến trình cha chưa thay đổi nó.

Trình xử lý cho một signal cụ thể, sau khi được thiết lập, sẽ tiếp tục được cài đặt cho đến khi được đặt lại một cách rõ ràng (Python mô phỏng giao diện kiểu BSD bất kể cách triển khai bên dưới), ngoại trừ trình xử lý cho
:const:`SIGCHLD`, tuân theo cách triển khai bên dưới.

Trên các nền tảng WebAssembly, các signal được mô phỏng và do đó hoạt động khác đi. Một số hàm và signal không khả dụng trên các nền tảng này.

Thực thi các signal handler của Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Một signal handler của Python không được thực thi bên trong signal handler cấp thấp (C). Thay vào đó, signal handler cấp thấp đặt một cờ để báo cho
:term:`virtual machine` thực thi signal handler Python tương ứng vào thời điểm sau đó (ví dụ: tại lệnh :term:`bytecode` tiếp theo). Điều này dẫn đến các hệ quả sau:

* Việc bắt các lỗi đồng bộ như :const:`SIGFPE` hoặc
  :const:`SIGSEGV` do một thao tác không hợp lệ trong mã C gây ra là không mấy ý nghĩa. Python sẽ trở về từ signal handler về mã C, và mã này có khả năng sẽ phát sinh lại signal tương tự, khiến Python dường như bị treo. Kể từ Python 3.3, bạn có thể sử dụng module :mod:`faulthandler` để báo cáo các lỗi đồng bộ.

* Một phép tính chạy lâu được triển khai hoàn toàn bằng C (chẳng hạn như so khớp biểu thức chính quy trên một lượng lớn văn bản) có thể chạy liên tục trong một khoảng thời gian tùy ý, bất kể đã nhận được tín hiệu nào. Các trình xử lý tín hiệu của Python sẽ được gọi khi phép tính kết thúc.

* Nếu trình xử lý phát sinh một ngoại lệ, ngoại lệ đó sẽ xuất hiện "từ hư không" trong luồng chính. Xem :ref:`ghi chú dưới đây <handlers-and-exceptions>` để biết thêm thông tin.

.. _signals-and-threads:


Tín hiệu và luồng
^^^^^^^^^^^^^^^^^

Các trình xử lý tín hiệu của Python luôn được thực thi trong luồng Python chính của trình thông dịch chính, ngay cả khi tín hiệu được nhận trong một luồng khác. Điều này có nghĩa là không thể sử dụng tín hiệu để giao tiếp giữa các luồng. Thay vào đó, bạn có thể sử dụng các primitive đồng bộ hóa từ module :mod:`threading`.

Ngoài ra, chỉ luồng chính của trình thông dịch chính mới được phép thiết lập một trình xử lý tín hiệu mới.

.. warning::

   Không nên sử dụng các primitive đồng bộ hóa như :class:`threading.Lock` bên trong trình xử lý tín hiệu. Làm như vậy có thể dẫn đến deadlock không mong muốn.


Nội dung module
---------------

.. versionchanged:: 3.5
   các hằng số liên quan đến signal (SIG*), handler (:const:`SIG_DFL`, :const:`SIG_IGN`) và sigmask (:const:`SIG_BLOCK`, :const:`SIG_UNBLOCK`, :const:`SIG_SETMASK`) được liệt kê dưới đây đã được chuyển thành
   :class:`enums <enum.IntEnum>` (:class:`Signals`, :class:`Handlers` và :class:`Sigmasks` tương ứng).
   :func:`getsignal`, :func:`pthread_sigmask`, :func:`sigpending` và
   các hàm :func:`sigwait` trả về dạng dễ đọc
   :class:`enums <enum.IntEnum>` dưới dạng các đối tượng :class:`Signals`.


Mô-đun signal định nghĩa ba enum:

.. class:: Signals

   Bộ sưu tập :class:`enum.IntEnum` gồm các hằng số SIG* và các hằng số CTRL_*.

   .. versionadded:: 3.5

.. class:: Handlers

   :class:`enum.IntEnum` tập hợp các hằng số :const:`SIG_DFL` và :const:`SIG_IGN`.

   .. versionadded:: 3.5

.. class:: Sigmasks

   :class:`enum.IntEnum` tập hợp các hằng số :const:`SIG_BLOCK`, :const:`SIG_UNBLOCK` và :const:`SIG_SETMASK`.

   .. availability:: Unix.

      Xem trang hướng dẫn :manpage:`sigprocmask(2)` và
      :manpage:`pthread_sigmask(3)` để biết thêm thông tin.

   .. versionadded:: 3.5


Các biến được định nghĩa trong mô-đun :mod:`!signal` là:


.. data:: SIG_DFL

   Đây là một trong hai tùy chọn xử lý tín hiệu tiêu chuẩn; tùy chọn này chỉ thực hiện hàm mặc định cho tín hiệu. Ví dụ, trên hầu hết các hệ thống, hành động mặc định cho :const:`SIGQUIT` là kết xuất core rồi thoát, còn hành động mặc định cho :const:`SIGCHLD` là đơn giản bỏ qua tín hiệu đó.


.. data:: SIG_IGN

   Đây là một trình xử lý tín hiệu tiêu chuẩn khác, chỉ đơn giản bỏ qua tín hiệu đã cho.


.. data:: SIGABRT

   Tín hiệu hủy từ :manpage:`abort(3)`.

.. data:: SIGALRM

   Tín hiệu bộ hẹn giờ từ :manpage:`alarm(2)`.

   .. availability:: Unix.

.. data:: SIGBREAK

   Ngắt từ bàn phím (CTRL + BREAK).

   .. availability:: Windows.

.. data:: SIGBUS

   Lỗi bus (truy cập bộ nhớ không hợp lệ).

   .. availability:: Unix.

.. data:: SIGCHLD

   Tiến trình con đã dừng hoặc bị chấm dứt.

   .. availability:: Unix.

.. data:: SIGCLD

   Bí danh của :data:`SIGCHLD`.

   .. availability:: not macOS.

.. data:: SIGCONT

   Tiếp tục tiến trình nếu tiến trình hiện đang dừng

   .. availability:: Unix.

.. data:: SIGFPE

   Ngoại lệ số thực dấu phẩy động. Ví dụ: phép chia cho không.

   .. seealso::
      :exc:`ZeroDivisionError` is raised when the second argument of a division
      hoặc phép modulo bằng không.

.. data:: SIGHUP

   Phát hiện tín hiệu ngắt trên terminal điều khiển hoặc tiến trình điều khiển đã kết thúc.

   .. availability:: Unix.

.. data:: SIGILL

   Lệnh không hợp lệ.

.. data:: SIGINT

   Tín hiệu ngắt từ bàn phím (CTRL + C).

   Hành động mặc định là phát sinh :exc:`KeyboardInterrupt`.

.. data:: SIGKILL

   Tín hiệu kết thúc.

   Không thể bắt, chặn hoặc bỏ qua tín hiệu này.

   .. availability:: Unix.

.. data:: SIGPIPE

   Đường ống bị hỏng: ghi vào đường ống không có trình đọc.

   Hành động mặc định là bỏ qua tín hiệu.

   .. availability:: Unix.

.. data:: SIGPROF

   Bộ hẹn giờ profiling đã hết hạn.

   .. availability:: Unix.

.. data:: SIGQUIT

   Tín hiệu thoát terminal.

   .. availability:: Unix.

.. data:: SIGSEGV

   Lỗi segmentation fault: tham chiếu bộ nhớ không hợp lệ.

.. data:: SIGSTOP

   Dừng thực thi (không thể bắt hoặc bỏ qua).

   .. availability:: Unix.

.. data:: SIGSTKFLT

   Lỗi ngăn xếp trên bộ đồng xử lý. Nhân Linux không phát tín hiệu này: tín hiệu này chỉ có thể được phát trong không gian người dùng.

   .. availability:: Linux.

      Trên các kiến trúc có hỗ trợ tín hiệu này. Xem trang hướng dẫn :manpage:`signal(7)` để biết thêm thông tin.

   .. versionadded:: 3.11

.. data:: SIGTERM

   Tín hiệu kết thúc.

.. data:: SIGUSR1

   Tín hiệu do người dùng định nghĩa 1.

   .. availability:: Unix.

.. data:: SIGUSR2

   Tín hiệu do người dùng định nghĩa 2.

   .. availability:: Unix.

.. data:: SIGVTALRM

   Bộ hẹn giờ ảo đã hết hạn.

   .. availability:: Unix.

.. data:: SIGWINCH

   Tín hiệu thay đổi kích thước cửa sổ.

   .. availability:: Unix.

.. data:: SIGXCPU

   Đã vượt quá giới hạn thời gian CPU.

   .. availability:: Unix.

.. data:: SIG*

   Tất cả số hiệu tín hiệu đều được định nghĩa bằng tên tượng trưng. Ví dụ, tín hiệu ngắt kết nối được định nghĩa là :const:`signal.SIGHUP`; tên biến giống hệt tên được sử dụng trong các chương trình C, như được nêu trong ``<signal.h>``. Trang hướng dẫn Unix cho '``signal``' liệt kê các tín hiệu hiện có (trên một số hệ thống, đây là
   :manpage:`signal(2)`, trên các hệ thống khác, danh sách nằm trong :manpage:`signal(7)`). Lưu ý rằng không phải tất cả hệ thống đều định nghĩa cùng một tập hợp tên tín hiệu; chỉ những tên được hệ thống định nghĩa mới được module này định nghĩa.


.. data:: CTRL_C_EVENT

   Tín hiệu tương ứng với sự kiện nhấn phím :kbd:`Ctrl+C`. Tín hiệu này chỉ có thể được sử dụng với :func:`os.kill`.

   .. availability:: Windows.

   .. versionadded:: 3.2


.. data:: CTRL_BREAK_EVENT

   Tín hiệu tương ứng với sự kiện nhấn phím :kbd:`Ctrl+Break`. Tín hiệu này chỉ có thể được sử dụng với :func:`os.kill`.

   .. availability:: Windows.

   .. versionadded:: 3.2


.. data:: NSIG

   Lớn hơn số hiệu của tín hiệu cao nhất một đơn vị. Sử dụng :func:`valid_signals` để lấy các số hiệu tín hiệu hợp lệ.


.. data:: ITIMER_REAL

   Giảm bộ định thời khoảng thời gian theo thời gian thực và gửi :const:`SIGALRM` khi hết hạn.


.. data:: ITIMER_VIRTUAL

   Giảm bộ hẹn giờ khoảng thời gian chỉ khi tiến trình đang thực thi và gửi SIGVTALRM khi hết hạn.


.. data:: ITIMER_PROF

   Giảm bộ hẹn giờ khoảng thời gian cả khi tiến trình thực thi và khi hệ thống thực thi thay cho tiến trình. Kết hợp với ITIMER_VIRTUAL, bộ hẹn giờ này thường được dùng để lập hồ sơ thời gian ứng dụng sử dụng trong user space và kernel space. SIGPROF được gửi khi hết hạn.


.. data:: SIG_BLOCK

   Một giá trị khả dĩ cho tham số *how* của :func:`pthread_sigmask`, cho biết các signal sẽ bị chặn.

   .. versionadded:: 3.3

.. data:: SIG_UNBLOCK

   Một giá trị khả dĩ cho tham số *how* của :func:`pthread_sigmask`, cho biết các signal sẽ được bỏ chặn.

   .. versionadded:: 3.3

.. data:: SIG_SETMASK

   Một giá trị khả dĩ cho tham số *how* của :func:`pthread_sigmask`, cho biết signal mask sẽ được thay thế.

   .. versionadded:: 3.3


Module :mod:`!signal` định nghĩa một exception:

.. exception:: ItimerError

   Được nâng lên để báo hiệu lỗi từ :func:`setitimer` bên dưới hoặc
   Triển khai :func:`getitimer`. Dự kiến lỗi này nếu truyền bộ hẹn giờ theo khoảng thời gian không hợp lệ hoặc thời gian âm cho :func:`setitimer`. Lỗi này là một kiểu con của :exc:`OSError`.

   .. versionadded:: 3.3
      Lỗi này trước đây là một kiểu con của :exc:`IOError`, hiện đã trở thành bí danh của :exc:`OSError`.


Mô-đun :mod:`!signal` định nghĩa các hàm sau:


.. function:: alarm(time)

   Nếu *time* khác 0, hàm này yêu cầu gửi tín hiệu :const:`SIGALRM` đến tiến trình sau *time* giây. Mọi cảnh báo đã được lên lịch trước đó sẽ bị hủy (tại một thời điểm chỉ có thể lên lịch một cảnh báo). Giá trị trả về là số giây còn lại trước khi cảnh báo được thiết lập trước đó được gửi. Nếu *time* bằng 0, không có cảnh báo nào được lên lịch và mọi cảnh báo đã lên lịch sẽ bị hủy. Nếu giá trị trả về bằng 0, hiện không có cảnh báo nào được lên lịch.

   .. availability:: Unix.

      Xem trang hướng dẫn :manpage:`alarm(2)` để biết thêm thông tin.


.. function:: getsignal(signalnum)

   Trả về signal handler hiện tại cho tín hiệu *signalnum*. Giá trị trả về có thể là một đối tượng Python có thể gọi hoặc một trong các giá trị đặc biệt
   :const:`signal.SIG_IGN`, :const:`signal.SIG_DFL` hoặc :const:`None`. Tại đây,
   :const:`signal.SIG_IGN` có nghĩa là tín hiệu trước đó đã bị bỏ qua,
   :const:`signal.SIG_DFL` có nghĩa là cách xử lý mặc định đối với tín hiệu trước đó đang được sử dụng, còn ``None`` có nghĩa là trình xử lý tín hiệu trước đó không được cài đặt từ Python.


.. function:: strsignal(signalnum)

   Trả về mô tả của tín hiệu *signalnum*, chẳng hạn như "Interrupt" đối với :const:`SIGINT`. Trả về :const:`None` nếu *signalnum* không có mô tả. Phát sinh :exc:`ValueError` nếu *signalnum* không hợp lệ.

   .. versionadded:: 3.8


.. function:: valid_signals()

   Trả về tập hợp các số hiệu tín hiệu hợp lệ trên nền tảng này. Tập hợp này có thể ít hơn ``range(1, NSIG)`` nếu một số tín hiệu được hệ thống dành riêng cho mục đích sử dụng nội bộ.

   .. versionadded:: 3.8


.. function:: pause()

   Khiến tiến trình tạm dừng cho đến khi nhận được một tín hiệu; sau đó trình xử lý thích hợp sẽ được gọi. Không trả về giá trị nào.

   .. availability:: Unix.

      Xem trang hướng dẫn :manpage:`signal(2)` để biết thêm thông tin.

   Xem thêm :func:`sigwait`, :func:`sigwaitinfo`, :func:`sigtimedwait` và
   :func:`sigpending`.


.. function:: raise_signal(signum)

   Gửi một tín hiệu đến tiến trình gọi. Không trả về giá trị nào.

   .. versionadded:: 3.8


.. function:: pidfd_send_signal(pidfd, sig, siginfo=None, flags=0)

   Gửi tín hiệu *sig* đến tiến trình được xác định bởi bộ mô tả tệp *pidfd*. Python hiện chưa hỗ trợ tham số *siginfo*; tham số này phải là ``None``. Đối số *flags* được cung cấp cho các phần mở rộng trong tương lai; hiện chưa có giá trị cờ nào được định nghĩa.

   Xem trang hướng dẫn :manpage:`pidfd_send_signal(2)` để biết thêm thông tin.

   .. availability:: Linux >= 5.1, Android >= :func:`build-time <sys.getandroidapilevel>` API level 31
   .. versionadded:: 3.9


.. function:: pthread_kill(thread_id, signalnum)

   Gửi tín hiệu *signalnum* đến luồng *thread_id*, tức một luồng khác trong cùng tiến trình với bên gọi. Luồng đích có thể đang thực thi bất kỳ mã nào (Python hoặc không). Tuy nhiên, nếu luồng đích đang thực thi trình thông dịch Python, các trình xử lý tín hiệu Python sẽ được :ref:`thực thi bởi luồng chính của trình thông dịch chính <signals-and-threads>`. Vì vậy, mục đích duy nhất của việc gửi tín hiệu đến một luồng Python cụ thể là buộc một system call đang chạy thất bại với :exc:`InterruptedError`.

   Sử dụng :func:`threading.get_ident` hoặc thuộc tính :attr:`~threading.Thread.ident` của các đối tượng :class:`threading.Thread` để lấy giá trị phù hợp cho *thread_id*.

   Nếu *signalnum* là 0 thì không có tín hiệu nào được gửi, nhưng việc kiểm tra lỗi vẫn được thực hiện; bạn có thể dùng cách này để kiểm tra xem luồng đích còn đang chạy hay không.

   .. audit-event:: signal.pthread_kill thread_id,signalnum signal.pthread_kill

   .. availability:: Unix.

      Xem trang hướng dẫn :manpage:`pthread_kill(3)` để biết thêm thông tin.

   Xem thêm :func:`os.kill`.

   .. versionadded:: 3.3


.. function:: pthread_sigmask(how, mask)

   Lấy và/hoặc thay đổi signal mask của luồng đang gọi. Signal mask là tập hợp các signal mà việc phân phối hiện đang bị chặn đối với bên gọi. Trả về signal mask cũ dưới dạng một tập hợp các signal.

   Cách hoạt động của lệnh gọi phụ thuộc vào giá trị của *how*, như sau.

   * :data:`SIG_BLOCK`: Tập hợp các signal bị chặn là hợp của tập hợp hiện tại và đối số *mask*.
   * :data:`SIG_UNBLOCK`: Các signal trong *mask* được loại bỏ khỏi tập hợp signal hiện đang bị chặn. Có thể thử bỏ chặn một signal hiện không bị chặn.
   * :data:`SIG_SETMASK`: Tập hợp các signal bị chặn được đặt thành đối số *mask*.

   *mask* là một tập hợp các số signal (ví dụ: {:const:`signal.SIGINT`,
   :const:`signal.SIGTERM`}). Sử dụng :func:`~signal.valid_signals` để tạo một mask đầy đủ bao gồm tất cả các signal.

   Ví dụ: ``signal.pthread_sigmask(signal.SIG_BLOCK, [])`` đọc signal mask của thread gọi nó.

   Không thể block :data:`SIGKILL` và :data:`SIGSTOP`.

   .. availability:: Unix.

      Xem trang hướng dẫn :manpage:`sigprocmask(2)` và
      :manpage:`pthread_sigmask(3)` để biết thêm thông tin.

   Xem thêm :func:`pause`, :func:`sigpending` và :func:`sigwait`.

   .. versionadded:: 3.3


.. function:: setitimer(which, seconds, interval=0.0)

   Thiết lập timer theo khoảng thời gian đã cho (một trong :const:`signal.ITIMER_REAL`,
   :const:`signal.ITIMER_VIRTUAL` hoặc :const:`signal.ITIMER_PROF`) được chỉ định bởi *which* để kích hoạt sau *seconds* (chấp nhận float, khác với
   :func:`alarm`) và sau đó cứ mỗi *interval* giây (nếu *interval* khác không). Bộ hẹn giờ interval được chỉ định bởi *which* có thể được hủy bằng cách đặt *seconds* thành 0.

   Khi interval timer được kích hoạt, một signal sẽ được gửi đến process. Signal được gửi phụ thuộc vào timer đang được sử dụng;
   :const:`signal.ITIMER_REAL` sẽ gửi :const:`SIGALRM`,
   :const:`signal.ITIMER_VIRTUAL` gửi :const:`SIGVTALRM`, còn :const:`signal.ITIMER_PROF` sẽ gửi :const:`SIGPROF`.

   Các giá trị cũ được trả về dưới dạng một tuple: (delay, interval).

   Việc cố gắng truyền vào một interval timer không hợp lệ sẽ gây ra một
   :exc:`ItimerError`.

   .. availability:: Unix.


.. function:: getitimer(which)

   Trả về giá trị hiện tại của bộ hẹn giờ theo khoảng thời gian được chỉ định bởi *which*.

   .. availability:: Unix.


.. function:: set_wakeup_fd(fd, *, warn_on_full_buffer=True)

   Đặt file descriptor đánh thức thành *fd*. Khi nhận được một tín hiệu mà chương trình của bạn đã đăng ký signal handler, số hiệu tín hiệu sẽ được ghi dưới dạng một byte duy nhất vào fd. Nếu bạn chưa đăng ký signal handler cho các tín hiệu mình quan tâm, sẽ không có gì được ghi vào wakeup fd. Thư viện có thể sử dụng cơ chế này để đánh thức một lệnh gọi poll hoặc select, cho phép tín hiệu được xử lý hoàn toàn.

   Trả về wakeup fd cũ (hoặc -1 nếu chưa bật cơ chế đánh thức bằng file descriptor). Nếu *fd* là -1, cơ chế đánh thức bằng file descriptor sẽ bị tắt. Nếu không phải -1, *fd* phải ở chế độ non-blocking. Thư viện có trách nhiệm xóa mọi byte khỏi *fd* trước khi gọi lại poll hoặc select.

   Khi các thread được bật, hàm này chỉ có thể được gọi từ :ref:`thread chính của interpreter chính <signals-and-threads>`; nếu cố gọi từ các thread khác, một ngoại lệ :exc:`ValueError` sẽ được phát sinh.

   Có hai cách phổ biến để sử dụng hàm này. Với cả hai cách, bạn dùng fd để đánh thức khi có tín hiệu đến, nhưng chúng khác nhau ở cách xác định *tín hiệu nào hoặc những tín hiệu nào* đã đến.

   Trong cách thứ nhất, chúng ta đọc dữ liệu ra khỏi bộ đệm của fd, và các giá trị byte cho biết số hiệu tín hiệu. Cách này đơn giản, nhưng trong một số trường hợp hiếm gặp có thể phát sinh vấn đề: nhìn chung fd sẽ có dung lượng bộ đệm giới hạn, và nếu có quá nhiều tín hiệu đến quá nhanh, bộ đệm có thể bị đầy khiến một số tín hiệu bị mất. Nếu sử dụng cách này, bạn nên đặt ``warn_on_full_buffer=True``, việc này ít nhất sẽ khiến một cảnh báo được in ra stderr khi tín hiệu bị mất.

   Trong cách thứ hai, chúng ta sử dụng wakeup fd *chỉ* để đánh thức và bỏ qua các giá trị byte thực tế. Trong trường hợp này, điều duy nhất chúng ta quan tâm là bộ đệm của fd trống hay không trống; bộ đệm đầy hoàn toàn không cho thấy có vấn đề. Nếu sử dụng cách này, bạn nên đặt ``warn_on_full_buffer=False``, để người dùng không bị nhầm lẫn bởi các thông báo cảnh báo không cần thiết.

   .. versionchanged:: 3.5
      Trên Windows, hàm này hiện cũng hỗ trợ các socket handle.

   .. versionchanged:: 3.7
      Đã thêm tham số ``warn_on_full_buffer``.

.. function:: siginterrupt(signalnum, flag)

   Thay đổi hành vi khởi động lại system call: nếu *flag* là :const:`False`, system call sẽ được khởi động lại khi bị ngắt bởi signal *signalnum*, nếu không, system call sẽ bị ngắt. Không trả về giá trị nào.

   .. availability:: Unix.

      Xem trang hướng dẫn :manpage:`siginterrupt(3)` để biết thêm thông tin.

   Lưu ý rằng việc cài đặt signal handler bằng :func:`signal` sẽ đặt lại hành vi khởi động lại thành có thể bị ngắt bằng cách ngầm gọi
   :c:func:`!siginterrupt` với giá trị *flag* là true cho signal đã cho.


.. function:: signal(signalnum, handler)

   Đặt handler cho signal *signalnum* thành hàm *handler*. *handler* có thể là một đối tượng Python có thể gọi nhận hai đối số (xem bên dưới), hoặc một trong các giá trị đặc biệt :const:`signal.SIG_IGN` hoặc :const:`signal.SIG_DFL`. Signal handler trước đó sẽ được trả về (xem phần mô tả về :func:`getsignal` ở trên). (Xem trang hướng dẫn Unix :manpage:`signal(2)` để biết thêm thông tin.)

   Khi các thread được bật, hàm này chỉ có thể được gọi từ :ref:`thread chính của interpreter chính <signals-and-threads>`; nếu cố gọi từ các thread khác, một ngoại lệ :exc:`ValueError` sẽ được phát sinh.

   *Trình xử lý* được gọi với hai đối số: số hiệu tín hiệu và stack frame hiện tại (``None`` hoặc một đối tượng frame; để xem mô tả về các đối tượng frame, hãy xem :ref:`mô tả trong hệ thống phân cấp kiểu <frame-objects>` hoặc xem mô tả thuộc tính trong mô-đun :mod:`inspect`).

   Trên Windows, :func:`signal` chỉ có thể được gọi với :const:`SIGABRT`,
   :const:`SIGFPE`, :const:`SIGILL`, :const:`SIGINT`, :const:`SIGSEGV`,
   :const:`SIGTERM`, hoặc :const:`SIGBREAK`. Một :exc:`ValueError` sẽ được đưa ra trong mọi trường hợp khác. Lưu ý rằng không phải tất cả các hệ thống đều định nghĩa cùng một tập hợp tên tín hiệu;
   một :exc:`AttributeError` sẽ được đưa ra nếu tên tín hiệu không được định nghĩa dưới dạng hằng số cấp mô-đun ``SIG*``.


.. function:: sigpending()

   Kiểm tra tập hợp các tín hiệu đang chờ được chuyển đến thread đang gọi (tức là các tín hiệu đã được phát sinh trong khi bị chặn). Trả về tập hợp các tín hiệu đang chờ.

   .. availability:: Unix.

      Xem trang hướng dẫn :manpage:`sigpending(2)` để biết thêm thông tin.

   Xem thêm :func:`pause`, :func:`pthread_sigmask` và :func:`sigwait`.

   .. versionadded:: 3.3


.. function:: sigwait(sigset)

   Tạm dừng việc thực thi của thread gọi cho đến khi nhận được một trong các tín hiệu được chỉ định trong tập tín hiệu *sigset*. Hàm tiếp nhận tín hiệu (loại tín hiệu đó khỏi danh sách tín hiệu đang chờ) và trả về số hiệu tín hiệu.

   .. availability:: Unix.

      Xem trang hướng dẫn :manpage:`sigwait(3)` để biết thêm thông tin.

   Xem thêm :func:`pause`, :func:`pthread_sigmask`, :func:`sigpending`,
   :func:`sigwaitinfo` và :func:`sigtimedwait`.

   .. versionadded:: 3.3


.. function:: sigwaitinfo(sigset)

   Tạm dừng việc thực thi của thread gọi cho đến khi nhận được một trong các tín hiệu được chỉ định trong tập tín hiệu *sigset*. Hàm tiếp nhận tín hiệu và loại tín hiệu đó khỏi danh sách tín hiệu đang chờ. Nếu một trong các tín hiệu trong *sigset* đã ở trạng thái chờ đối với thread gọi, hàm sẽ trả về ngay lập tức cùng thông tin về tín hiệu đó. Trình xử lý tín hiệu không được gọi cho tín hiệu đã được phân phối. Hàm sẽ phát sinh một
   :exc:`InterruptedError` nếu bị ngắt bởi một tín hiệu không nằm trong *sigset*.

   Giá trị trả về là một đối tượng biểu diễn dữ liệu có trong cấu trúc ``siginfo_t``, cụ thể là: ``si_signo``, ``si_code``, ``si_errno``, ``si_pid``, ``si_uid``, ``si_status``, ``si_band``.

   .. availability:: Unix.

      Xem trang man :manpage:`sigwaitinfo(2)` để biết thêm thông tin.

   Xem thêm :func:`pause`, :func:`sigwait` và :func:`sigtimedwait`.

   .. versionadded:: 3.3

   .. versionchanged:: 3.5
      Hàm hiện sẽ được thử lại nếu bị gián đoạn bởi một signal không có trong *sigset* và signal handler không phát sinh ngoại lệ (xem :pep:`475` để biết lý do).


.. function:: sigtimedwait(sigset, timeout)

   Tương tự :func:`sigwaitinfo`, nhưng nhận thêm đối số *timeout* chỉ định thời gian chờ. Nếu *timeout* được chỉ định là ``0``, một poll sẽ được thực hiện. Trả về :const:`None` nếu xảy ra hết thời gian chờ.

   .. availability:: Unix.

      Xem trang man :manpage:`sigtimedwait(2)` để biết thêm thông tin.

   Xem thêm :func:`pause`, :func:`sigwait` và :func:`sigwaitinfo`.

   .. versionadded:: 3.3

   .. versionchanged:: 3.5
      Hàm hiện được thử lại với *timeout* được tính toán lại nếu bị gián đoạn bởi một tín hiệu không nằm trong *sigset* và trình xử lý tín hiệu không phát sinh ngoại lệ (xem :pep:`475` để biết lý do).


.. _signal-example:

Ví dụ
-----

Sau đây là một chương trình ví dụ tối giản. Chương trình sử dụng hàm :func:`alarm` để giới hạn thời gian chờ mở tệp; điều này hữu ích nếu tệp tương ứng với một thiết bị nối tiếp có thể chưa được bật, vì trong trường hợp bình thường điều đó sẽ khiến
:func:`os.open` bị treo vô thời hạn. Giải pháp là đặt báo thức 5 giây trước khi mở tệp; nếu thao tác mất quá nhiều thời gian, tín hiệu báo thức sẽ được gửi và trình xử lý sẽ phát sinh một ngoại lệ.::

   import signal, os

   def handler(signum, frame):
       signame = signal.Signals(signum).name
       print(f'Signal handler called with signal {signame} ({signum})')
       raise OSError("Couldn't open device!")

   # Thiết lập trình xử lý tín hiệu và báo thức 5 giây
   signal.signal(signal.SIGALRM, handler)
   signal.alarm(5)

   # Lệnh open() này có thể bị treo vô thời hạn
   fd = os.open('/dev/ttyS0', os.O_RDWR)

   signal.alarm(0)          # Tắt báo thức

Lưu ý về SIGPIPE
----------------

Việc chuyển đầu ra của chương trình bạn vào các công cụ như :manpage:`head(1)` sẽ khiến một tín hiệu :const:`SIGPIPE` được gửi đến tiến trình của bạn khi bên nhận đầu ra tiêu chuẩn đóng sớm. Điều này dẫn đến một ngoại lệ như :code:`BrokenPipeError: [Errno 32] Broken pipe`. Để xử lý trường hợp này, hãy bọc entry point của bạn để bắt ngoại lệ này như sau::

    import os
    import sys

    def main():
        try:
            # mô phỏng đầu ra lớn (code của bạn thay thế vòng lặp này)
            for x in range(10000):
                print("y")
            # flush đầu ra ở đây để buộc SIGPIPE được kích hoạt
            # khi đang ở trong khối try này.
            sys.stdout.flush()
        except BrokenPipeError:
            # Python flush các stream tiêu chuẩn khi thoát; chuyển hướng đầu ra còn lại
            # sang devnull để tránh một BrokenPipeError khác khi tắt
            devnull = os.open(os.devnull, os.O_WRONLY)
            os.dup2(devnull, sys.stdout.fileno())
            sys.exit(1)  # Python thoát với mã lỗi 1 khi gặp EPIPE

    if __name__ == '__main__':
        main()

Không đặt cách xử lý của :const:`SIGPIPE` thành :const:`SIG_DFL` để tránh :exc:`BrokenPipeError`. Việc đó sẽ khiến chương trình thoát đột ngột bất cứ khi nào một kết nối socket bị gián đoạn trong lúc chương trình vẫn đang ghi vào đó.

.. _handlers-and-exceptions:

Lưu ý về Signal Handler và Exception
------------------------------------

Nếu một signal handler phát sinh exception, exception đó sẽ được truyền đến main thread và có thể phát sinh sau bất kỳ lệnh :term:`bytecode` nào. Đáng chú ý nhất là :exc:`KeyboardInterrupt` có thể xuất hiện tại bất kỳ thời điểm nào trong quá trình thực thi. Hầu hết mã Python, bao gồm cả standard library, không thể được làm cho đủ mạnh để xử lý tình huống này, vì vậy :exc:`KeyboardInterrupt` (hoặc bất kỳ exception nào khác phát sinh từ signal handler) trong một số trường hợp hiếm gặp có thể khiến chương trình rơi vào trạng thái không mong muốn.

Để minh họa cho vấn đề này, hãy xem xét đoạn mã sau::

    class SpamContext:
        def __init__(self):
            self.lock = threading.Lock()

        def __enter__(self):
            # If KeyboardInterrupt occurs here, everything is fine
            self.lock.acquire()
            # If KeyboardInterrupt occurs here, __exit__ will not be called
            ...
            # KeyboardInterrupt có thể xảy ra ngay trước khi hàm trả về

        def __exit__(self, exc_type, exc_val, exc_tb):
            ...
            self.lock.release()

Đối với nhiều chương trình, đặc biệt là những chương trình chỉ muốn thoát khi
:exc:`KeyboardInterrupt`, đây không phải là vấn đề, nhưng các ứng dụng phức tạp hoặc yêu cầu độ tin cậy cao nên tránh phát sinh ngoại lệ từ các signal handler. Chúng cũng nên tránh bắt :exc:`KeyboardInterrupt` để tắt ứng dụng một cách an toàn. Thay vào đó, chúng nên cài đặt
:const:`SIGINT` handler riêng. Dưới đây là một ví dụ về máy chủ HTTP tránh
:exc:`KeyboardInterrupt`::

    import signal
    import socket
    from selectors import DefaultSelector, EVENT_READ
    from http.server import HTTPServer, SimpleHTTPRequestHandler

    interrupt_read, interrupt_write = socket.socketpair()

    def handler(signum, frame):
        print('Signal handler called with signal', signum)
        interrupt_write.send(b'\0')
    signal.signal(signal.SIGINT, handler)

    def serve_forever(httpd):
        sel = DefaultSelector()
        sel.register(interrupt_read, EVENT_READ)
        sel.register(httpd, EVENT_READ)

        while True:
            for key, _ in sel.select():
                if key.fileobj == interrupt_read:
                    interrupt_read.recv(1)
                    return
                if key.fileobj == httpd:
                    httpd.handle_request()

    print("Serving on port 8000")
    httpd = HTTPServer(('', 8000), SimpleHTTPRequestHandler)
    serve_forever(httpd)
    print("Shutdown...")
