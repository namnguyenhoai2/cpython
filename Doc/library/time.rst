:mod:`!time` --- Truy cập thời gian và chuyển đổi
=================================================

.. module:: time
   :synopsis: Truy cập thời gian và chuyển đổi.

--------------

Mô-đun này cung cấp nhiều hàm liên quan đến thời gian. Để biết các chức năng liên quan, hãy xem thêm các mô-đun :mod:`datetime` và :mod:`calendar`.

Mặc dù mô-đun này luôn khả dụng, không phải tất cả các hàm đều khả dụng trên mọi nền tảng. Hầu hết các hàm được định nghĩa trong mô-đun này đều gọi các hàm thư viện C của nền tảng có cùng tên. Đôi khi, việc tham khảo tài liệu của nền tảng có thể hữu ích, vì ngữ nghĩa của các hàm này khác nhau giữa các nền tảng.

Sau đây là phần giải thích một số thuật ngữ và quy ước.

.. _epoch:

.. index:: single: epoch

* :dfn:`Kỷ nguyên` là thời điểm bắt đầu tính thời gian, tức giá trị trả về của ``time.gmtime(0)``. Trên mọi nền tảng, đó là ngày 1 tháng 1 năm 1970, 00:00:00 (UTC).

.. _leap seconds: https://en.wikipedia.org/wiki/Leap_second

.. index:: seconds since the epoch

* Thuật ngữ :dfn:`số giây kể từ kỷ nguyên` đề cập đến tổng số giây đã trôi qua kể từ kỷ nguyên, thường không bao gồm `giây nhuận <leap seconds_>`_. Giây nhuận được loại trừ khỏi tổng số này trên mọi nền tảng tuân thủ POSIX.

.. index:: single: Year 2038

* Các hàm trong mô-đun này có thể không xử lý được ngày và giờ trước epoch_ hoặc quá xa trong tương lai. Mốc giới hạn trong tương lai do thư viện C xác định; đối với các hệ thống 32-bit, mốc này thường là năm 2038.

.. index::
   single: 2-digit years

* Hàm :func:`strptime` có thể phân tích cú pháp năm gồm 2 chữ số khi được cung cấp mã định dạng ``%y``. Khi năm gồm 2 chữ số được phân tích cú pháp, chúng được chuyển đổi theo các tiêu chuẩn POSIX và ISO C: các giá trị 69--99 được ánh xạ thành 1969--1999, còn các giá trị 0--68 được ánh xạ thành 2000--2068.

.. index::
   single: UTC
   single: Coordinated Universal Time
   single: Greenwich Mean Time

* UTC là `Giờ Phối hợp Quốc tế <Coordinated Universal Time_>`_ và đã thay thế `Giờ Greenwich <Greenwich Mean Time_>`_ hay GMT làm cơ sở cho việc đo thời gian quốc tế. Từ viết tắt UTC không phải là một lỗi mà tuân theo một quy ước đặt tên không phụ thuộc ngôn ngữ có từ trước dành cho các tiêu chuẩn thời gian như UT0, UT1 và UT2.

.. _Coordinated Universal Time: https://en.wikipedia.org/wiki/Coordinated_Universal_Time
.. _Greenwich Mean Time: https://en.wikipedia.org/wiki/Greenwich_Mean_Time

.. index:: single: Daylight Saving Time

* DST là Giờ Mùa hè, tức việc điều chỉnh múi giờ (thường) thêm một giờ trong một khoảng thời gian của năm. Các quy tắc DST rất đặc thù (do luật địa phương quy định) và có thể thay đổi theo từng năm. Thư viện C có một bảng chứa các quy tắc địa phương (thường được đọc từ một tệp hệ thống để tăng tính linh hoạt) và là nguồn duy nhất của Chân lý Tuyệt đối về vấn đề này.

* Độ chính xác của nhiều hàm thời gian thực có thể thấp hơn mức được gợi ý bởi các đơn vị dùng để biểu diễn giá trị hoặc đối số của chúng. Ví dụ: trên hầu hết các hệ thống Unix, đồng hồ chỉ “nhịp” 50 hoặc 100 lần mỗi giây.

* Mặt khác, độ chính xác của :func:`.time` và :func:`sleep` tốt hơn các phiên bản tương đương trên Unix: thời gian được biểu diễn dưới dạng số dấu phẩy động,
  :func:`.time` trả về thời gian chính xác nhất hiện có (sử dụng Unix
  :c:func:`!gettimeofday` khi khả dụng), và :func:`sleep` sẽ chấp nhận thời gian có phần lẻ khác 0 (Unix :c:func:`!select` được dùng để triển khai điều này, khi khả dụng).

* Giá trị thời gian được trả về bởi :func:`gmtime`, :func:`localtime`, và
  :func:`strptime`, và được chấp nhận bởi :func:`asctime`, :func:`mktime` và
  :func:`strftime`, là một dãy gồm 9 số nguyên. Các giá trị trả về của
  :func:`gmtime`, :func:`localtime`, và :func:`strptime` cũng cung cấp tên thuộc tính cho từng trường riêng lẻ.

  Xem :class:`struct_time` để biết mô tả về các đối tượng này.

  .. versionchanged:: 3.3
     Kiểu :class:`struct_time` đã được mở rộng để cung cấp các thuộc tính :attr:`~struct_time.tm_gmtoff` và :attr:`~struct_time.tm_zone` khi nền tảng hỗ trợ các thành viên ``struct tm`` tương ứng.

  .. versionchanged:: 3.6
     Các thuộc tính :class:`struct_time`
     :attr:`~struct_time.tm_gmtoff` và :attr:`~struct_time.tm_zone` hiện có trên mọi nền tảng.

* Sử dụng các hàm sau để chuyển đổi giữa các biểu diễn thời gian:

  +------------------------------------------+------------------------------------------+-------------------------+
  | Từ                                       | Sang                                     | Sử dụng                 |
  +==========================================+==========================================+=========================+
  | số giây kể từ epoch                      | :class:`struct_time` theo UTC            | :func:`gmtime`          |
  +------------------------------------------+------------------------------------------+-------------------------+
  | số giây kể từ epoch                      | :class:`struct_time` theo giờ địa phương | :func:`localtime`       |
  +------------------------------------------+------------------------------------------+-------------------------+
  | :class:`struct_time` theo UTC            | số giây kể từ epoch                      | :func:`calendar.timegm` |
  +------------------------------------------+------------------------------------------+-------------------------+
  | :class:`struct_time` theo giờ địa phương | số giây kể từ epoch                      | :func:`mktime`          |
  +------------------------------------------+------------------------------------------+-------------------------+


.. _time-functions:

Các hàm
-------

.. function:: asctime([time_tuple])

   Chuyển đổi một tuple hoặc :class:`struct_time` đại diện cho thời gian như được trả về bởi
   :func:`gmtime` hoặc :func:`localtime` thành một chuỗi có dạng sau: ``'Sun Jun 20 23:21:05 1993'``. Trường ngày dài hai ký tự và được đệm bằng khoảng trắng nếu ngày có một chữ số, ví dụ: ``'Wed Jun  9 04:26:40 1993'``.

   Nếu *time_tuple* không được cung cấp, thời gian hiện tại do :func:`localtime` trả về sẽ được sử dụng. Thông tin locale không được sử dụng bởi :func:`asctime`.

   .. note::

      Không giống hàm C cùng tên, :func:`asctime` không thêm ký tự xuống dòng ở cuối.

.. function:: pthread_getcpuclockid(thread_id, /)

   Trả về *clk_id* của đồng hồ đo thời gian CPU dành riêng cho thread của *thread_id* đã chỉ định.

   Sử dụng :func:`threading.get_ident` hoặc thuộc tính :attr:`~threading.Thread.ident` của các đối tượng :class:`threading.Thread` để lấy giá trị phù hợp cho *thread_id*.

   .. warning::
      Việc truyền *thread_id* không hợp lệ hoặc đã hết hạn có thể dẫn đến hành vi không xác định, chẳng hạn như lỗi segmentation fault.

   .. availability:: Unix

      Xem trang man của :manpage:`pthread_getcpuclockid(3)` để biết thêm thông tin.

   .. versionadded:: 3.7

.. function:: clock_getres(clk_id, /)

   Trả về độ phân giải (độ chính xác) của clock được chỉ định *clk_id*.  Tham khảo
   :ref:`time-clock-id-constants` để xem danh sách các giá trị được chấp nhận cho *clk_id*.

   .. availability:: Unix.

   .. versionadded:: 3.3


.. function:: clock_gettime(clk_id, /) -> float

   Trả về thời gian của clock được chỉ định *clk_id*.  Tham khảo
   :ref:`time-clock-id-constants` để xem danh sách các giá trị được chấp nhận cho *clk_id*.

   Sử dụng :func:`clock_gettime_ns` để tránh mất độ chính xác do
   kiểu :class:`float`.

   .. availability:: Unix.

   .. versionadded:: 3.3


.. function:: clock_gettime_ns(clk_id, /) -> int

   Tương tự như :func:`clock_gettime` nhưng trả về thời gian dưới dạng nanosecond.

   .. availability:: Unix.

   .. versionadded:: 3.7


.. function:: clock_settime(clk_id, time: float, /)

   Đặt thời gian của clock được chỉ định *clk_id*. Hiện tại,
   :data:`CLOCK_REALTIME` là giá trị duy nhất được chấp nhận cho *clk_id*.

   Sử dụng :func:`clock_settime_ns` để tránh mất độ chính xác do kiểu
   :class:`float` gây ra.

   .. availability:: Unix, not Android, not iOS.

   .. versionadded:: 3.3


.. function:: clock_settime_ns(clk_id, time: int, /)

   Tương tự như :func:`clock_settime` nhưng đặt thời gian bằng nanosecond.

   .. availability:: Unix, not Android, not iOS.

   .. versionadded:: 3.7


.. function:: ctime(seconds=None, /)

   Chuyển đổi thời gian được biểu diễn bằng số giây kể từ epoch_ thành một chuỗi có dạng: ``'Sun Jun 20 23:21:05 1993'``, biểu thị giờ địa phương. Trường ngày có độ dài hai ký tự và được đệm bằng dấu cách nếu ngày chỉ có một chữ số, ví dụ: ``'Wed Jun  9 04:26:40 1993'``.

   Nếu *giây* không được cung cấp hoặc :const:`None`, thời gian hiện tại do :func:`.time` trả về sẽ được sử dụng. ``ctime(seconds)`` tương đương với ``asctime(localtime(seconds))``. Thông tin về locale không được sử dụng bởi
   :func:`ctime`.


.. function:: get_clock_info(name, /)

   Lấy thông tin về clock được chỉ định dưới dạng một namespace object. Các tên clock được hỗ trợ và các hàm tương ứng để đọc giá trị của chúng là:

   * ``'monotonic'``: :func:`time.monotonic`
   * ``'perf_counter'``: :func:`time.perf_counter`
   * ``'process_time'``: :func:`time.process_time`
   * ``'thread_time'``: :func:`time.thread_time`
   * ``'time'``: :func:`time.time`

   Kết quả có các thuộc tính sau:

   - *adjustable*: ``True`` nếu clock có thể được đặt để nhảy tiến hoặc lùi theo thời gian, nếu không thì là ``False``. Không đề cập đến các điều chỉnh tốc độ NTP dần dần.
   - *implementation*: Tên của hàm C bên dưới được sử dụng để lấy giá trị của clock. Tham khảo :ref:`time-clock-id-constants` để biết các giá trị có thể có.
   - *monotonic*: ``True`` nếu clock không thể chạy lùi, nếu không thì là ``False``
   - *resolution*: Độ phân giải của đồng hồ tính bằng giây (:class:`float`)

   .. versionadded:: 3.3


.. function:: gmtime(seconds=None, /)

   Chuyển đổi thời gian được biểu diễn bằng số giây kể từ epoch_ thành một :class:`struct_time` theo UTC, trong đó cờ dst luôn bằng không. Nếu *seconds* không được cung cấp hoặc
   :const:`None`, thời gian hiện tại do :func:`.time` trả về sẽ được sử dụng. Phần lẻ của giây bị bỏ qua. Xem phần trên để biết mô tả về đối tượng
   :class:`struct_time`. Xem :func:`calendar.timegm` để biết hàm đảo ngược của hàm này.


.. function:: localtime(seconds=None, /)

   Tương tự :func:`gmtime` nhưng chuyển đổi sang giờ địa phương. Nếu *seconds* không được cung cấp hoặc :const:`None`, thời gian hiện tại do :func:`.time` trả về sẽ được sử dụng. Cờ dst được đặt thành ``1`` khi DST áp dụng cho thời gian đã cho.

   :func:`localtime` có thể phát sinh :exc:`OverflowError` nếu dấu thời gian nằm ngoài phạm vi giá trị được các hàm :c:func:`localtime` hoặc :c:func:`gmtime` trong C của nền tảng hỗ trợ, và :exc:`OSError` trên :c:func:`localtime` hoặc
   :c:func:`gmtime` không thành công. Thông thường, phạm vi này bị giới hạn trong các năm từ 1970 đến 2038.


.. function:: mktime(time_tuple, /)

   Đây là hàm ngược của :func:`localtime`. Đối số của hàm là
   :class:`struct_time` hoặc bộ 9 phần tử đầy đủ (vì cần cờ dst; sử dụng ``-1`` làm cờ dst nếu không xác định), biểu thị thời gian theo *local* chứ không phải UTC. Hàm trả về một số dấu phẩy động để tương thích với :func:`.time`. Nếu giá trị đầu vào không thể được biểu diễn dưới dạng thời gian hợp lệ, một trong hai lỗi sau sẽ được phát sinh:
   :exc:`OverflowError` hoặc :exc:`ValueError` sẽ được phát sinh (điều này phụ thuộc vào việc giá trị không hợp lệ bị Python hay các thư viện C bên dưới bắt giữ). Ngày sớm nhất mà hàm có thể tạo ra thời gian phụ thuộc vào nền tảng.


.. function:: monotonic() -> float

   Trả về giá trị (tính bằng giây phân số) của một đồng hồ đơn điệu (monotonic), tức là một đồng hồ không thể chạy lùi. Đồng hồ này không bị ảnh hưởng bởi các cập nhật đồng hồ hệ thống. Điểm tham chiếu của giá trị được trả về không được xác định, vì vậy chỉ hiệu giữa kết quả của hai lần gọi mới có giá trị.

   Đồng hồ:

   * Trên Windows, gọi ``QueryPerformanceCounter()`` và ``QueryPerformanceFrequency()``.
   * Trên macOS, gọi ``mach_absolute_time()`` và ``mach_timebase_info()``.
   * Trên HP-UX, gọi ``gethrtime()``.
   * Gọi ``clock_gettime(CLOCK_HIGHRES)`` nếu có.
   * Nếu không, gọi ``clock_gettime(CLOCK_MONOTONIC)``.

   Sử dụng :func:`monotonic_ns` để tránh mất độ chính xác do
   :class:`float` gây ra.

   .. versionadded:: 3.3

   .. versionchanged:: 3.5
      Hiện hàm này luôn khả dụng và đồng hồ hiện giống nhau đối với tất cả các tiến trình.

   .. versionchanged:: 3.10
      Trên macOS, đồng hồ hiện giống nhau đối với tất cả các tiến trình.


.. function:: monotonic_ns() -> int

   Tương tự như :func:`monotonic`, nhưng trả về thời gian dưới dạng nanosecond.

   .. versionadded:: 3.7

.. function:: perf_counter() -> float

   .. index::
      single: benchmarking

   Trả về giá trị (tính bằng giây phân số) của performance counter, tức là một clock có độ phân giải cao nhất hiện có để đo một khoảng thời gian ngắn. Clock này bao gồm cả thời gian đã trôi qua trong khi sleep. Clock này giống nhau đối với mọi process. Điểm tham chiếu của giá trị được trả về không được xác định, vì vậy chỉ hiệu của kết quả từ hai lần gọi mới hợp lệ.

   .. impl-detail::

      Trên CPython, sử dụng cùng clock với :func:`time.monotonic` và đây là monotonic clock, tức là clock không thể chạy ngược.

   Sử dụng :func:`perf_counter_ns` để tránh mất độ chính xác do
   :class:`float` gây ra.

   .. versionadded:: 3.3

   .. versionchanged:: 3.10
      Trên Windows, clock hiện giống nhau đối với mọi process.

   .. versionchanged:: 3.13
      Sử dụng cùng clock với :func:`time.monotonic`.


.. function:: perf_counter_ns() -> int

   Tương tự như :func:`perf_counter`, nhưng trả về thời gian theo đơn vị nanôgiây.

   .. versionadded:: 3.7


.. function:: process_time() -> float

   .. index::
      single: CPU time
      single: processor time
      single: benchmarking

   Trả về giá trị (tính theo giây phân số) của tổng thời gian CPU của hệ thống và người dùng cho tiến trình hiện tại. Giá trị này không bao gồm thời gian đã trôi qua trong khi ngủ. Theo định nghĩa, đây là thời gian trên toàn tiến trình. Mốc tham chiếu của giá trị được trả về là không xác định, vì vậy chỉ hiệu giữa kết quả của hai lần gọi mới có giá trị.

   Sử dụng :func:`process_time_ns` để tránh mất độ chính xác do
   :class:`float` gây ra.

   .. versionadded:: 3.3

.. function:: process_time_ns() -> int

   Tương tự như :func:`process_time` nhưng trả về thời gian theo đơn vị nanôgiây.

   .. versionadded:: 3.7

.. function:: sleep(seconds, /)

   Tạm dừng việc thực thi của thread đang gọi trong số giây đã cho. Đối số có thể là một số dấu phẩy động để biểu thị thời gian ngủ chính xác hơn.

   Nếu việc ngủ bị gián đoạn bởi một signal và signal handler không phát sinh ngoại lệ, thao tác ngủ sẽ được khởi động lại với thời gian chờ được tính lại.

   Thời gian tạm dừng có thể dài hơn thời gian được yêu cầu một khoảng tùy ý, do lịch thực thi của các hoạt động khác trong hệ thống.

   .. rubric:: Triển khai trên Windows

   Trên Windows, nếu *seconds* bằng 0, thread sẽ nhường phần thời gian còn lại của lát thời gian cho bất kỳ thread nào khác đang sẵn sàng chạy. Nếu không có thread nào khác sẵn sàng chạy, hàm sẽ trả về ngay lập tức và thread tiếp tục thực thi. Trên Windows 10 trở lên, việc triển khai sử dụng `bộ hẹn giờ độ phân giải cao <https://learn.microsoft.com/windows/win32/api/synchapi/nf-synchapi-createwaitabletimerexw>`_, cung cấp độ phân giải 100 nanosecond. Nếu *seconds* bằng 0, ``Sleep(0)`` sẽ được sử dụng.

   .. rubric:: Triển khai trên Unix

   * Sử dụng ``clock_nanosleep()`` nếu có (độ phân giải: 1 nanosecond);
   * Hoặc sử dụng ``nanosleep()`` nếu có (độ phân giải: 1 nanosecond);
   * Hoặc sử dụng ``select()`` (độ phân giải: 1 microsecond).

   .. note::

      Để mô phỏng một "no-op", hãy sử dụng :keyword:`pass` thay vì ``time.sleep(0)``.

      Để tự nguyện nhường CPU, hãy chỉ định :ref:`chính sách lập lịch thời gian thực <os-scheduling-policy>` và sử dụng :func:`os.sched_yield` thay vào đó.

   .. audit-event:: time.sleep seconds

   .. versionchanged:: 3.5
      Hàm hiện ngủ ít nhất *giây* ngay cả khi việc ngủ bị gián đoạn bởi một tín hiệu, trừ khi trình xử lý tín hiệu ném ra một ngoại lệ (xem :pep:`475` để biết lý do).

   .. versionchanged:: 3.11
      Trên Unix, các hàm ``clock_nanosleep()`` và ``nanosleep()`` hiện được sử dụng nếu có sẵn. Trên Windows, hiện sử dụng một bộ hẹn giờ có thể chờ.

   .. versionchanged:: 3.13
      Phát sinh một sự kiện kiểm tra.

.. index::
   single: % (percent); datetime format

.. function:: strftime(format[, time_tuple])

   Chuyển đổi một tuple hoặc :class:`struct_time` đại diện cho thời gian như được trả về bởi
   :func:`gmtime` hoặc :func:`localtime` thành một chuỗi như được chỉ định bởi đối số *định dạng*. Nếu *bộ_tuple_thời_gian* không được cung cấp, thời gian hiện tại như được trả về bởi
   :func:`localtime` được sử dụng. *format* phải là một chuỗi. :exc:`ValueError` được phát sinh nếu bất kỳ trường nào trong *time_tuple* nằm ngoài phạm vi cho phép.

   0 là một đối số hợp lệ cho mọi vị trí trong time tuple; nếu bình thường không hợp lệ, giá trị sẽ được ép về giá trị đúng.

   Các directive sau đây có thể được nhúng trong chuỗi *format*. Chúng được hiển thị mà không có phần đặc tả tùy chọn về độ rộng trường và độ chính xác, đồng thời được thay thế bằng các ký tự được chỉ định trong kết quả :func:`strftime`:

   +-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
   | Directive | Ý nghĩa                                                                                                                                                                                                                   | Ghi chú |
   +===========+===========================================================================================================================================================================================================================+=========+
   | ``%a``    | Tên viết tắt của ngày trong tuần theo locale.                                                                                                                                                                             |         |
   +-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
   | ``%A``    | Tên đầy đủ của ngày trong tuần theo locale.                                                                                                                                                                               |         |
   +-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
   | ``%b``    | Tên viết tắt của tháng theo locale.                                                                                                                                                                                       |         |
   +-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
   | ``%B``    | Tên đầy đủ của tháng theo locale.                                                                                                                                                                                         |         |
   +-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
   | ``%c``    | Cách biểu diễn ngày và giờ phù hợp theo locale.                                                                                                                                                                           |         |
   +-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
   | ``%d``    | Ngày trong tháng dưới dạng số thập phân [01,31].                                                                                                                                                                          |         |
   +-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
   | ``%f``    | Microsecond dưới dạng số thập phân                                                                                                                                                                                        | \(1)    |
   |           |    [000000,999999].                                                                                                                                                                                                       |         |
   +-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
   | ``%H``    | Giờ (đồng hồ 24 giờ) dưới dạng số thập phân [00,23].                                                                                                                                                                      |         |
   +-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
   | ``%I``    | Giờ (đồng hồ 12 giờ) dưới dạng số thập phân [01,12].                                                                                                                                                                      |         |
   +-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
   | ``%j``    | Ngày trong năm dưới dạng số thập phân [001,366].                                                                                                                                                                          |         |
   +-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
   | ``%m``    | Tháng dưới dạng số thập phân [01,12].                                                                                                                                                                                     |         |
   +-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
   | ``%M``    | Phút dưới dạng số thập phân [00,59].                                                                                                                                                                                      |         |
   +-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
   | ``%p``    | Giá trị tương đương với AM hoặc PM trong locale.                                                                                                                                                                          | \(2)    |
   +-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
   | ``%S``    | Giây dưới dạng số thập phân [00,61].                                                                                                                                                                                      | \(3)    |
   +-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
   | ``%U``    | Số tuần trong năm (Chủ nhật là ngày đầu tuần) dưới dạng số thập phân [00,53]. Tất cả các ngày đầu năm trước Chủ nhật đầu tiên được coi là thuộc tuần 0.                                                                   | \(4)    |
   +-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
   | ``%u``    | Ngày trong tuần (Thứ Hai là 1; Chủ Nhật là 7) dưới dạng số thập phân [1, 7].                                                                                                                                              |         |
   +-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
   | ``%w``    | Ngày trong tuần dưới dạng số thập phân [0(Chủ Nhật),6].                                                                                                                                                                   |         |
   +-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
   | ``%W``    | Số tuần trong năm (Thứ Hai là ngày đầu tiên trong tuần) dưới dạng số thập phân [00,53]. Tất cả các ngày trong năm mới trước Thứ Hai đầu tiên được xem là thuộc tuần 0.                                                    | \(4)    |
   +-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
   | ``%x``    | Biểu diễn ngày phù hợp với locale.                                                                                                                                                                                        |         |
   +-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
   | ``%X``    | Biểu diễn thời gian phù hợp với locale.                                                                                                                                                                                   |         |
   +-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
   | ``%y``    | Năm không có thế kỷ dưới dạng số thập phân [00,99].                                                                                                                                                                       |         |
   +-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
   | ``%Y``    | Năm có thế kỷ dưới dạng số thập phân.                                                                                                                                                                                     |         |
   +-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
   | ``%z``    | Độ lệch múi giờ cho biết chênh lệch thời gian dương hoặc âm so với UTC/GMT, có dạng +HHMM hoặc -HHMM, trong đó H biểu thị các chữ số của giờ thập phân và M biểu thị các chữ số của phút thập phân [-23:59, +23:59]. [1]_ |         |
   +-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
   | ``%Z``    | Tên múi giờ (không có ký tự nào nếu không tồn tại múi giờ). Đã lỗi thời. [1]_                                                                                                                                             |         |
   +-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
   | ``%G``    | Năm ISO 8601 (tương tự ``%Y`` nhưng tuân theo các quy tắc của năm theo lịch ISO 8601). Năm bắt đầu từ tuần chứa thứ Năm đầu tiên của năm dương lịch.                                                                      |         |
   +-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
   | ``%V``    | Số tuần ISO 8601 (dưới dạng số thập phân [01,53]). Tuần đầu tiên của năm là tuần chứa thứ Năm đầu tiên của năm. Các tuần bắt đầu từ thứ Hai.                                                                              |         |
   +-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
   | ``%%``    | Một ký tự ``'%'`` theo nghĩa đen.                                                                                                                                                                                         |         |
   +-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+

   Lưu ý:

   (1)
       Chỉ thị định dạng ``%f`` chỉ áp dụng cho :func:`strptime`, không áp dụng cho :func:`strftime`. Tuy nhiên, hãy xem thêm :meth:`datetime.datetime.strptime` và
       :meth:`datetime.datetime.strftime` trong đó chỉ thị định dạng ``%f``
       :ref:`áp dụng cho microsecond <format-codes>`.

   (2)
      Khi được sử dụng với hàm :func:`strptime`, chỉ thị ``%p`` chỉ ảnh hưởng đến trường giờ của đầu ra nếu chỉ thị ``%I`` được sử dụng để phân tích cú pháp giờ.

   .. _leap-second:

   (3)
      Phạm vi thực sự là từ ``0`` đến ``61``; giá trị ``60`` hợp lệ trong các timestamp biểu thị `giây nhuận <leap seconds_>`_ và giá trị ``61`` được hỗ trợ vì lý do lịch sử.

   (4)
      Khi được sử dụng với hàm :func:`strptime`, ``%U`` và ``%W`` chỉ được dùng trong các phép tính khi ngày trong tuần và năm được chỉ định.

   Dưới đây là một ví dụ, một định dạng ngày tháng tương thích với định dạng được chỉ định trong
   :rfc:`5322` tiêu chuẩn email Internet.  [1]_::

      >>> from time import gmtime, strftime
      >>> strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
      'Thu, 28 Jun 2001 14:17:15 +0000'

   Một số chỉ thị bổ sung có thể được hỗ trợ trên một số nền tảng nhất định, nhưng chỉ những chỉ thị được liệt kê ở đây mới có ý nghĩa được ANSI C chuẩn hóa. Để xem toàn bộ tập mã định dạng được nền tảng của bạn hỗ trợ, hãy tham khảo tài liệu :manpage:`strftime(3)`.

   Trên một số nền tảng, đặc tả độ rộng trường và độ chính xác tùy chọn có thể ngay lập tức theo sau ``'%'`` ban đầu của một chỉ thị theo thứ tự sau; điều này cũng không portable. Độ rộng trường thường là 2, ngoại trừ ``%j`` là 3.


.. index::
   single: % (percent); datetime format

.. function:: strptime(string[, format])

   Phân tích một chuỗi biểu diễn thời gian theo một định dạng. Giá trị trả về là một :class:`struct_time` được trả về bởi :func:`gmtime` hoặc
   :func:`localtime`.

   Tham số *format* sử dụng cùng các chỉ thị như các chỉ thị được dùng bởi
   :func:`strftime`; giá trị mặc định là ``"%a %b %d %H:%M:%S %Y"``, khớp với định dạng được trả về bởi :func:`ctime`. Nếu không thể phân tích *string* theo *format*, hoặc nếu còn dữ liệu thừa sau khi phân tích, :exc:`ValueError` sẽ được phát sinh. Các giá trị mặc định được dùng để điền vào mọi dữ liệu còn thiếu khi không thể suy ra các giá trị chính xác hơn là ``(1900, 1, 1, 0, 0, 0, 0, 1, -1)``. Cả *string* và *format* đều phải là các chuỗi.

   Ví dụ:

      >>> import time
      >>> time.strptime("30 Nov 00", "%d %b %y")   # doctest: +NORMALIZE_WHITESPACE
      time.struct_time(tm_year=2000, tm_mon=11, tm_mday=30, tm_hour=0, tm_min=0,
                       tm_sec=0, tm_wday=3, tm_yday=335, tm_isdst=-1)

   Việc hỗ trợ chỉ thị ``%Z`` dựa trên các giá trị có trong ``tzname`` và việc ``daylight`` có phải là true hay không. Vì vậy, tính năng này phụ thuộc vào nền tảng, ngoại trừ việc nhận dạng UTC và GMT, vốn luôn được biết đến (và được xem là các múi giờ không áp dụng giờ mùa hè).

   Chỉ các chỉ thị được nêu trong tài liệu mới được hỗ trợ. Vì ``strftime()`` được triển khai riêng theo từng nền tảng nên đôi khi có thể cung cấp nhiều chỉ thị hơn danh sách đã nêu. Tuy nhiên, ``strptime()`` không phụ thuộc vào nền tảng nào, vì vậy không nhất thiết hỗ trợ tất cả các chỉ thị hiện có nhưng không được tài liệu ghi rõ là được hỗ trợ.


.. class:: struct_time

   Kiểu của chuỗi giá trị thời gian được :func:`gmtime` trả về,
   :func:`localtime`, và :func:`strptime`. Đây là một đối tượng có giao diện :term:`named tuple`: các giá trị có thể được truy cập theo chỉ mục và theo tên thuộc tính. Các giá trị sau đây hiện diện:

   .. list-table::

      * - Chỉ mục
        - Thuộc tính
        - Giá trị

      * - 0
        - .. attribute:: tm_year
        - (ví dụ: 1993)

      * - 1
        - .. attribute:: tm_mon
        - phạm vi [1, 12]

      * - 2
        - .. attribute:: tm_mday
        - phạm vi [1, 31]

      * - 3
        - .. attribute:: tm_hour
        - phạm vi [0, 23]

      * - 4
        - .. attribute:: tm_min
        - phạm vi [0, 59]

      * - 5
        - .. attribute:: tm_sec
        - phạm vi [0, 61]; xem :ref:`Ghi chú (2) <leap-second>` trong :func:`strftime`

      * - 6
        - .. attribute:: tm_wday
        - phạm vi [0, 6]; Thứ Hai là 0

      * - 7
        - .. attribute:: tm_yday
        - phạm vi [1, 366]

      * - 8
        - .. attribute:: tm_isdst
        - 0, 1 hoặc -1; xem bên dưới

      * - N/A
        - .. attribute:: tm_zone
        - viết tắt của tên múi giờ

      * - N/A
        - .. attribute:: tm_gmtoff
        - độ lệch về phía đông UTC tính bằng giây

   Lưu ý rằng không giống như cấu trúc C, giá trị tháng nằm trong phạm vi [1, 12], không phải [0, 11].

   Trong các lệnh gọi đến :func:`mktime`, :attr:`tm_isdst` có thể được đặt thành 1 khi đang áp dụng giờ mùa hè và thành 0 khi không áp dụng. Giá trị -1 cho biết thông tin này chưa được xác định và thường sẽ dẫn đến việc điền đúng trạng thái.

   Khi một tuple có độ dài không đúng được truyền cho một hàm yêu cầu một
   :class:`struct_time`, hoặc có các phần tử sai kiểu, thì một
   :exc:`TypeError` sẽ được phát sinh.

.. function:: time() -> float

   Trả về thời gian tính bằng giây kể từ epoch_ dưới dạng một số dấu phẩy động. Cách xử lý `leap seconds <leap seconds_>`_ phụ thuộc vào nền tảng. Trên Windows và hầu hết các hệ thống Unix, các giây nhuận không được tính vào thời gian tính bằng giây kể từ epoch_. Giá trị này thường được gọi là `Unix time <https://en.wikipedia.org/wiki/Unix_time>`_.

   Lưu ý rằng mặc dù thời gian luôn được trả về dưới dạng số dấu phẩy động, không phải hệ thống nào cũng cung cấp thời gian với độ chính xác cao hơn 1 giây. Mặc dù hàm này thường trả về các giá trị không giảm, nó có thể trả về giá trị thấp hơn một lần gọi trước đó nếu đồng hồ hệ thống đã được chỉnh lùi trong khoảng thời gian giữa hai lần gọi.

   Số được :func:`.time` trả về có thể được chuyển đổi thành định dạng thời gian phổ biến hơn (tức là năm, tháng, ngày, giờ, v.v...) theo UTC bằng cách truyền nó cho
   hàm :func:`gmtime` hoặc theo giờ địa phương bằng cách truyền nó cho
   hàm :func:`localtime`. Trong cả hai trường hợp, một
   đối tượng :class:`struct_time` được trả về, từ đó có thể truy cập các thành phần của ngày theo lịch dưới dạng các thuộc tính.

   Đồng hồ:

   * Trên Windows, hãy gọi ``GetSystemTimePreciseAsFileTime()``.
   * Hãy gọi ``clock_gettime(CLOCK_REALTIME)`` nếu có sẵn.
   * Nếu không, hãy gọi ``gettimeofday()``.

   Sử dụng :func:`time_ns` để tránh mất độ chính xác do kiểu :class:`float` gây ra.

.. versionchanged:: 3.13

   Trên Windows, gọi ``GetSystemTimePreciseAsFileTime()`` thay vì ``GetSystemTimeAsFileTime()``.


.. function:: time_ns() -> int

   Tương tự như :func:`~time.time` nhưng trả về thời gian dưới dạng số nguyên tính bằng nanosecond kể từ epoch_.

   .. versionadded:: 3.7


.. function:: thread_time() -> float

   .. index::
      single: CPU time
      single: processor time
      single: benchmarking

   Trả về giá trị (tính bằng giây phân số) của tổng thời gian CPU hệ thống và CPU người dùng của thread hiện tại. Giá trị này không bao gồm thời gian đã trôi qua trong khi ngủ. Theo định nghĩa, giá trị này dành riêng cho thread. Mốc tham chiếu của giá trị được trả về không được xác định, vì vậy chỉ hiệu giữa kết quả của hai lần gọi trong cùng một thread mới có giá trị.

   Sử dụng :func:`thread_time_ns` để tránh mất độ chính xác do
   :class:`float` gây ra.

   .. availability::  Linux, Unix, Windows.

      Các hệ thống Unix hỗ trợ ``CLOCK_THREAD_CPUTIME_ID``.

   .. versionadded:: 3.7


.. function:: thread_time_ns() -> int

   Tương tự như :func:`thread_time` nhưng trả về thời gian dưới dạng nanosecond.

   .. versionadded:: 3.7


.. function:: tzset()

   Đặt lại các quy tắc chuyển đổi thời gian được các routine của thư viện sử dụng. Biến môi trường :envvar:`TZ` chỉ định cách thực hiện việc này. Biến này cũng sẽ thiết lập các biến ``tzname`` (từ biến môi trường :envvar:`TZ`), ``timezone`` (số giây không theo DST ở phía Tây UTC), ``altzone`` (số giây theo DST ở phía Tây UTC) và ``daylight`` (bằng 0 nếu múi giờ này không có bất kỳ quy tắc giờ mùa hè nào, hoặc khác 0 nếu có một thời điểm trong quá khứ, hiện tại hoặc tương lai mà giờ mùa hè được áp dụng).

   .. availability:: Unix.

   .. note::

      Mặc dù trong nhiều trường hợp, việc thay đổi biến môi trường :envvar:`TZ` có thể ảnh hưởng đến đầu ra của các hàm như :func:`localtime` mà không gọi
      :func:`tzset`, không nên dựa vào hành vi này.

      Biến môi trường :envvar:`TZ` không được chứa khoảng trắng.

   Định dạng chuẩn của biến môi trường :envvar:`TZ` là (thêm khoảng trắng để dễ hiểu)::

      std offset [dst [offset [,start[/time], end[/time]]]]

   Các thành phần là:

   ``std`` và ``dst``
      Ba hoặc nhiều ký tự chữ và số dùng để chỉ các chữ viết tắt múi giờ. Các ký tự này sẽ được truyền vào time.tzname

   ``offset``
      Độ lệch có dạng: ``± hh[:mm[:ss]]``. Giá trị này cho biết lượng cần cộng vào giờ địa phương để có được UTC. Nếu có dấu '-' đứng trước, múi giờ nằm về phía đông Kinh tuyến gốc; nếu không, nó nằm về phía tây. Nếu không có độ lệch sau dst, giờ mùa hè được giả định là sớm hơn giờ tiêu chuẩn một giờ.

   ``start[/time], end[/time]``
      Cho biết thời điểm chuyển sang và chuyển về từ DST. Định dạng của ngày bắt đầu và ngày kết thúc là một trong các dạng sau:

      :samp:`J{n}`
         Ngày Julian *n* (1 <= *n* <= 365). Ngày nhuận không được tính, vì vậy trong mọi năm, ngày 28 tháng 2 là ngày 59 và ngày 1 tháng 3 là ngày 60.

      :samp:`{n}`
         Ngày Julian bắt đầu từ 0 (0 <= *n* <= 365). Ngày nhuận được tính, nên có thể tham chiếu đến ngày 29 tháng 2.

      :samp:`M{m}.{n}.{d}`
         Ngày thứ *d* (0 <= *d* <= 6) trong tuần *n* của tháng *m* trong năm (1 <= *n* <= 5, 1 <= *m* <= 12, trong đó tuần 5 nghĩa là "ngày *d* cuối cùng trong tháng *m*", có thể rơi vào tuần thứ tư hoặc thứ năm). Tuần 1 là tuần đầu tiên trong đó ngày thứ *d* xuất hiện. Ngày 0 là Chủ nhật.

      ``time`` có cùng định dạng với ``offset``, ngoại trừ việc không cho phép dấu đứng đầu ('-' hoặc '+'). Giá trị mặc định, nếu không cung cấp thời gian, là 02:00:00.

   ::

      >>> os.environ['TZ'] = 'EST+05EDT,M4.1.0,M10.5.0'
      >>> time.tzset()
      >>> time.strftime('%X %x %Z')
      '02:07:36 05/08/03 EDT'
      >>> os.environ['TZ'] = 'AEST-10AEDT-11,M10.5.0,M3.5.0'
      >>> time.tzset()
      >>> time.strftime('%X %x %Z')
      '16:08:12 05/08/03 AEST'

   Trên nhiều hệ thống Unix (bao gồm \*BSD, Linux, Solaris và Darwin), việc sử dụng cơ sở dữ liệu zoneinfo (:manpage:`tzfile(5)`) của hệ thống để chỉ định các quy tắc múi giờ sẽ thuận tiện hơn. Để thực hiện việc này, hãy đặt biến môi trường :envvar:`TZ` thành đường dẫn đến tệp dữ liệu múi giờ cần thiết, tính tương đối từ thư mục gốc của cơ sở dữ liệu múi giờ 'zoneinfo' của hệ thống, thường nằm tại
   :file:`/usr/share/zoneinfo`. Ví dụ: ``'US/Eastern'``, ``'Australia/Melbourne'``, ``'Egypt'`` hoặc ``'Europe/Amsterdam'``.::

      >>> os.environ['TZ'] = 'US/Eastern'
      >>> time.tzset()
      >>> time.tzname
      ('EST', 'EDT')
      >>> os.environ['TZ'] = 'Egypt'
      >>> time.tzset()
      >>> time.tzname
      ('EET', 'EEST')


.. _time-clock-id-constants:

Hằng số Clock ID
----------------

Các hằng số này được dùng làm tham số cho :func:`clock_getres` và
:func:`clock_gettime`.

.. data:: CLOCK_BOOTTIME

   Giống hệt :data:`CLOCK_MONOTONIC`, ngoại trừ việc nó cũng bao gồm mọi khoảng thời gian hệ thống bị tạm ngừng.

   Điều này cho phép các ứng dụng lấy một monotonic clock có nhận biết trạng thái tạm ngừng mà không phải xử lý các vấn đề phức tạp của :data:`CLOCK_REALTIME`, vốn có thể bị gián đoạn nếu thời gian được thay đổi bằng ``settimeofday()`` hoặc tương tự.

   .. availability:: Linux >= 2.6.39.

   .. versionadded:: 3.7


.. data:: CLOCK_HIGHRES

   Hệ điều hành Solaris có bộ hẹn giờ ``CLOCK_HIGHRES`` cố gắng sử dụng nguồn phần cứng tối ưu và có thể cung cấp độ phân giải gần đến nano giây. ``CLOCK_HIGHRES`` là đồng hồ có độ phân giải cao không thể điều chỉnh.

   .. availability:: Solaris.

   .. versionadded:: 3.3


.. data:: CLOCK_MONOTONIC

   Đồng hồ không thể thiết lập và biểu thị thời gian đơn điệu kể từ một thời điểm bắt đầu không xác định.

   .. availability:: Unix.

   .. versionadded:: 3.3


.. data:: CLOCK_MONOTONIC_RAW

   Tương tự như :data:`CLOCK_MONOTONIC`, nhưng cho phép truy cập thời gian thô dựa trên phần cứng, không chịu ảnh hưởng của các điều chỉnh NTP.

   .. availability:: Linux >= 2.6.28, macOS >= 10.12.

   .. versionadded:: 3.3

.. data:: CLOCK_MONOTONIC_RAW_APPROX

   Tương tự như :data:`CLOCK_MONOTONIC_RAW`, nhưng đọc giá trị được hệ thống lưu vào bộ nhớ đệm khi chuyển ngữ cảnh, nên có độ chính xác thấp hơn.

   .. availability:: macOS >= 10.12.

   .. versionadded:: 3.13


.. data:: CLOCK_PROCESS_CPUTIME_ID

   Bộ hẹn giờ độ phân giải cao theo từng process từ CPU.

   .. availability:: Unix.

   .. versionadded:: 3.3


.. data:: CLOCK_PROF

   Bộ hẹn giờ độ phân giải cao theo từng process từ CPU.

   .. availability:: FreeBSD, NetBSD >= 7, OpenBSD.

   .. versionadded:: 3.7

.. data:: CLOCK_TAI

   `Giờ nguyên tử quốc tế <https://www.nist.gov/pml/time-and-frequency-division/how-utcnist-related-coordinated-universal-time-utc-international>`_

   Hệ thống phải có bảng giây nhuận hiện tại để câu lệnh này trả về kết quả chính xác. Phần mềm PTP hoặc NTP có thể duy trì bảng giây nhuận.

   .. availability:: Linux.

   .. versionadded:: 3.9

.. data:: CLOCK_THREAD_CPUTIME_ID

   Đồng hồ thời gian CPU dành riêng cho từng thread.

   .. availability::  Unix.

   .. versionadded:: 3.3


.. data:: CLOCK_UPTIME

   Thời gian có giá trị tuyệt đối là khoảng thời gian hệ thống đã chạy mà không bị tạm dừng, cung cấp phép đo uptime chính xác, cả tuyệt đối lẫn theo khoảng thời gian.

   .. availability:: FreeBSD, OpenBSD >= 5.5.

   .. versionadded:: 3.7


.. data:: CLOCK_UPTIME_RAW

   Đồng hồ tăng đơn điệu, theo dõi thời gian kể từ một thời điểm tùy ý, không bị ảnh hưởng bởi việc điều chỉnh tần số hoặc thời gian và không tăng khi hệ thống ở trạng thái ngủ.

   .. availability:: macOS >= 10.12.

   .. versionadded:: 3.8

.. data:: CLOCK_UPTIME_RAW_APPROX

   Giống như :data:`CLOCK_UPTIME_RAW`, nhưng giá trị được hệ thống lưu vào bộ nhớ đệm khi chuyển đổi ngữ cảnh và do đó kém chính xác hơn.

   .. availability:: macOS >= 10.12.

   .. versionadded:: 3.13

Hằng số sau đây là tham số duy nhất có thể được truyền tới
:func:`clock_settime`.


.. data:: CLOCK_REALTIME

   Đồng hồ thời gian thực. Việc thiết lập đồng hồ này yêu cầu các đặc quyền phù hợp. Đồng hồ này giống nhau đối với tất cả các process.

   .. availability:: Unix.

   .. versionadded:: 3.3


.. _time-timezone-constants:

Hằng số múi giờ
---------------

.. data:: altzone

   Độ lệch của múi giờ DST cục bộ, tính bằng số giây về phía tây so với UTC, nếu được xác định. Giá trị này là số âm nếu múi giờ DST cục bộ nằm về phía đông so với UTC (như ở Tây Âu, bao gồm cả Vương quốc Anh). Chỉ sử dụng giá trị này nếu ``daylight`` khác không. Xem lưu ý bên dưới.

.. data:: daylight

   Khác không nếu múi giờ DST được xác định. Xem lưu ý bên dưới.

.. data:: timezone

   Độ lệch của múi giờ cục bộ (không phải DST), tính bằng số giây về phía tây so với UTC (âm ở hầu hết Tây Âu, dương ở Hoa Kỳ, bằng không ở Vương quốc Anh). Xem lưu ý bên dưới.

.. data:: tzname

   Một tuple gồm hai chuỗi: chuỗi thứ nhất là tên của múi giờ cục bộ không phải DST, chuỗi thứ hai là tên của múi giờ DST cục bộ. Nếu không xác định múi giờ DST, không nên sử dụng chuỗi thứ hai. Xem lưu ý bên dưới.

.. note::

   Đối với các hằng số Múi giờ ở trên (:data:`altzone`, :data:`daylight`, :data:`timezone` và :data:`tzname`), giá trị được xác định bởi các quy tắc múi giờ có hiệu lực tại thời điểm tải module hoặc lần gần nhất :func:`tzset` được gọi và có thể không chính xác đối với các thời điểm trong quá khứ. Bạn nên sử dụng :attr:`~struct_time.tm_gmtoff` và
   :attr:`~struct_time.tm_zone` kết quả từ :func:`localtime` để lấy thông tin múi giờ.


.. seealso::

   Mô-đun :mod:`datetime`
      Giao diện hướng đối tượng hơn dành cho ngày và giờ.

   Mô-đun :mod:`locale`
      Các dịch vụ quốc tế hóa. Thiết lập locale ảnh hưởng đến cách diễn giải nhiều định dạng trong :func:`strftime` và :func:`strptime`.

   Mô-đun :mod:`calendar`
      Các hàm liên quan đến lịch nói chung. :func:`~calendar.timegm` là hàm nghịch đảo của :func:`gmtime` trong mô-đun này.

.. rubric:: Chú thích cuối trang

.. [1] Việc sử dụng ``%Z`` hiện đã không còn được khuyến nghị, nhưng escape ``%z``, vốn mở rộng thành độ lệch giờ/phút được ưu tiên, không được tất cả các thư viện ANSI C hỗ trợ. Ngoài ra, cách diễn giải chặt chẽ tiêu chuẩn :rfc:`822` nguyên bản năm 1982 yêu cầu năm có hai chữ số (``%y`` thay vì ``%Y``), nhưng trên thực tế, năm có 4 chữ số đã được sử dụng từ lâu trước năm 2000. Sau đó, :rfc:`822` trở nên lỗi thời, và năm có 4 chữ số lần đầu được :rfc:`1123` khuyến nghị, sau đó được :rfc:`2822` bắt buộc; :rfc:`5322` tiếp tục duy trì yêu cầu này.

.. _`high-resolution timer`: https://learn.microsoft.com/windows/win32/api/synchapi/nf-synchapi-createwaitabletimerexw
.. _`Unix time`: https://en.wikipedia.org/wiki/Unix_time
.. _`International Atomic Time`: https://www.nist.gov/pml/time-and-frequency-division/how-utcnist-related-coordinated-universal-time-utc-international
