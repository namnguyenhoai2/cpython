.. currentmodule:: asyncio


.. _asyncio-event-loop:

================
Vòng lặp sự kiện
================

**Mã nguồn:** :source:`Lib/asyncio/events.py`,
:source:`Lib/asyncio/base_events.py`

------------------------------------

.. rubric:: Lời nói đầu

Vòng lặp sự kiện là phần cốt lõi của mọi ứng dụng asyncio. Vòng lặp sự kiện chạy các tác vụ bất đồng bộ và callback, thực hiện các thao tác IO mạng, đồng thời chạy các tiến trình con.

Các nhà phát triển ứng dụng thường nên sử dụng các hàm asyncio cấp cao, chẳng hạn như :func:`asyncio.run`, và hiếm khi cần tham chiếu đến đối tượng vòng lặp hoặc gọi các phương thức của nó. Phần này chủ yếu dành cho tác giả của mã nguồn cấp thấp, thư viện và framework, những người cần kiểm soát chi tiết hơn hành vi của vòng lặp sự kiện.

.. rubric:: Lấy vòng lặp sự kiện

Có thể sử dụng các hàm cấp thấp sau để lấy, thiết lập hoặc tạo một vòng lặp sự kiện:

.. function:: get_running_loop()

   Trả về event loop đang chạy trong thread OS hiện tại.

   Phát sinh :exc:`RuntimeError` nếu không có event loop nào đang chạy.

   Chỉ có thể gọi hàm này từ một coroutine hoặc callback.

   .. versionadded:: 3.7

.. function:: get_event_loop()

   Lấy event loop hiện tại.

   Khi được gọi từ một coroutine hoặc callback (ví dụ: được lập lịch bằng call_soon hoặc API tương tự), hàm này sẽ luôn trả về event loop đang chạy.

   Nếu không có event loop nào đang chạy được thiết lập, hàm sẽ trả về kết quả của lệnh gọi ``get_event_loop_policy().get_event_loop()``.

   Vì hàm này có hành vi khá phức tạp (đặc biệt khi sử dụng các chính sách event loop tùy chỉnh), việc sử dụng
   Hàm :func:`get_running_loop` được ưu tiên hơn :func:`get_event_loop` trong coroutine và callback.

   Như đã lưu ý ở trên, hãy cân nhắc sử dụng hàm :func:`asyncio.run` cấp cao hơn, thay vì sử dụng các hàm cấp thấp hơn này để tự tạo và đóng event loop.

   .. versionchanged:: 3.14
      Phát sinh :exc:`RuntimeError` nếu không có event loop hiện tại.

   .. note::

      Hệ thống policy :mod:`!asyncio` không còn được khuyến nghị và sẽ bị xóa trong Python 3.16; từ thời điểm đó, hàm này sẽ trả về event loop đang chạy hiện tại nếu có, nếu không thì sẽ trả về loop được thiết lập bởi :func:`set_event_loop`.

.. function:: set_event_loop(loop)

   Đặt *loop* làm event loop hiện tại cho thread OS hiện tại.

.. function:: new_event_loop()

   Tạo và trả về một đối tượng event loop mới.

Lưu ý rằng hành vi của các hàm :func:`get_event_loop`, :func:`set_event_loop` và :func:`new_event_loop` có thể được thay đổi bởi
:ref:`thiết lập một chính sách event loop tùy chỉnh <asyncio-policies>`.


.. rubric:: Mục lục

Trang tài liệu này chứa các phần sau:

* Phần `Event Loop Methods <Event Loop Methods_>`_ là tài liệu tham khảo về các API của event loop;

* Phần `Callback Handles <Callback Handles_>`_ mô tả :class:`Handle` và
  :class:`TimerHandle` các instance được trả về từ những phương thức lập lịch như :meth:`loop.call_soon` và :meth:`loop.call_later`;

* Phần `Server Objects <Server Objects_>`_ mô tả các kiểu được trả về từ những phương thức của event loop như :meth:`loop.create_server`;

* Phần `Các triển khai Event Loop <Event Loop Implementations_>`_ trình bày
  :class:`SelectorEventLoop` và :class:`ProactorEventLoop` các lớp;

* Phần `Examples`_ giới thiệu cách làm việc với một số API của event loop.


.. _asyncio-event-loop-methods:

.. _`Event loop methods`:

Các phương thức của event loop
==============================

Event loop có các API **cấp thấp** cho những thao tác sau:

.. contents::
   :depth: 1
   :local:


Chạy và dừng event loop
^^^^^^^^^^^^^^^^^^^^^^^

.. method:: loop.run_until_complete(future)

   Chạy cho đến khi *future* (một đối tượng thuộc :class:`Future`) hoàn tất.

   Nếu đối số là một :ref:`coroutine object <coroutine>`, đối số đó sẽ được ngầm định lên lịch để chạy dưới dạng :class:`asyncio.Task`.

   Trả về kết quả của Future hoặc phát sinh exception của nó.

.. method:: loop.run_forever()

   Chạy event loop cho đến khi :meth:`stop` được gọi.

   Nếu :meth:`stop` được gọi trước khi :meth:`run_forever` được gọi, loop sẽ thăm dò bộ chọn I/O một lần với thời gian chờ bằng không, chạy tất cả callback được lên lịch để phản hồi các sự kiện I/O (cũng như những callback đã được lên lịch trước đó), rồi thoát.

   Nếu :meth:`stop` được gọi trong khi :meth:`run_forever` đang chạy, loop sẽ chạy lô callback hiện tại rồi thoát. Lưu ý rằng các callback mới được callback lên lịch sẽ không chạy trong trường hợp này; thay vào đó, chúng sẽ chạy vào lần tiếp theo khi :meth:`run_forever` hoặc
   :meth:`run_until_complete` được gọi.

.. method:: loop.stop()

   Dừng event loop.

.. method:: loop.is_running()

   Trả về ``True`` nếu event loop hiện đang chạy.

.. method:: loop.is_closed()

   Trả về ``True`` nếu event loop đã bị đóng.

.. method:: loop.close()

   Đóng event loop.

   Event loop không được chạy khi gọi hàm này. Mọi callback đang chờ sẽ bị loại bỏ.

   Phương thức này xóa tất cả các hàng đợi và tắt executor, nhưng không chờ executor hoàn tất.

   Phương thức này có tính idempotent và không thể đảo ngược. Không nên gọi bất kỳ phương thức nào khác sau khi event loop đã bị đóng.

.. method:: loop.shutdown_asyncgens()
   :async:

   Lên lịch đóng tất cả các đối tượng :term:`asynchronous generator` hiện đang mở bằng một lệnh gọi :meth:`~agen.aclose`. Sau khi gọi phương thức này, event loop sẽ đưa ra cảnh báo nếu một asynchronous generator mới được lặp qua. Nên sử dụng phương thức này để hoàn tất đáng tin cậy tất cả các asynchronous generator đã được lên lịch.

   Lưu ý rằng không cần gọi hàm này khi
   :func:`asyncio.run` được sử dụng.

   Ví dụ::

    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()

   .. versionadded:: 3.6

.. method:: loop.shutdown_default_executor(timeout=None)
   :async:

   Lên lịch đóng executor mặc định và chờ executor này join tất cả các thread trong :class:`~concurrent.futures.ThreadPoolExecutor`. Sau khi phương thức này được gọi, việc sử dụng executor mặc định với :meth:`loop.run_in_executor` sẽ gây ra :exc:`RuntimeError`.

   Tham số *timeout* chỉ khoảng thời gian (tính bằng :class:`float` giây) mà executor được phép để hoàn tất việc join. Với giá trị mặc định là ``None``, executor được phép có khoảng thời gian không giới hạn.

   Nếu đạt đến *timeout*, một :exc:`RuntimeWarning` sẽ được phát ra và executor mặc định sẽ bị chấm dứt mà không chờ các thread hoàn tất việc join.

   .. note::

      Không gọi phương thức này khi sử dụng :func:`asyncio.run`, vì :func:`asyncio.run` tự động xử lý việc tắt executor mặc định.

   .. versionadded:: 3.9

   .. versionchanged:: 3.12
      Đã thêm tham số *timeout*.

Lập lịch callback
^^^^^^^^^^^^^^^^^

.. method:: loop.call_soon(callback, *args, context=None)

   Lập lịch để *callback* :term:`callback` được gọi với *args* đối số ở lần lặp tiếp theo của event loop.

   Trả về một instance của :class:`asyncio.Handle`, có thể được dùng sau đó để hủy callback.

   Các callback được gọi theo thứ tự chúng được đăng ký. Mỗi callback sẽ được gọi đúng một lần.

   Đối số chỉ dành cho keyword tùy chọn *context* chỉ định một :class:`contextvars.Context` tùy chỉnh để *callback* chạy trong đó. Callback sử dụng context hiện tại khi không cung cấp *context*.

   Không giống :meth:`call_soon_threadsafe`, phương thức này không an toàn với thread.

.. method:: loop.call_soon_threadsafe(callback, *args, context=None)

   Một biến thể an toàn với thread của :meth:`call_soon`. Khi lên lịch callback từ một thread khác, hàm này *phải* được sử dụng, vì :meth:`call_soon` không an toàn với thread.

   Hàm này có thể được gọi an toàn từ context reentrant hoặc signal handler; tuy nhiên, việc sử dụng handle được trả về trong các context như vậy không an toàn hoặc không mang lại tác dụng.

   Ném :exc:`RuntimeError` nếu được gọi trên một loop đã bị đóng. Điều này có thể xảy ra trên một thread phụ khi ứng dụng chính đang tắt.

   Xem phần :ref:`concurrency và multithreading <asyncio-multithreading>` trong tài liệu.

   .. versionchanged:: 3.7
      Tham số chỉ có keyword *context* đã được thêm vào. Xem :pep:`567` để biết thêm chi tiết.

.. _asyncio-pass-keywords:

.. note::

   Hầu hết các hàm :mod:`asyncio` scheduling không cho phép truyền keyword arguments. Để làm vậy, hãy sử dụng :func:`functools.partial`::

      # sẽ lên lịch "print("Hello", flush=True)"
      loop.call_soon(
          functools.partial(print, "Hello", flush=True))

   Việc sử dụng các partial object thường thuận tiện hơn việc sử dụng lambda, vì asyncio có thể hiển thị partial object tốt hơn trong các thông báo debug và lỗi.


.. _asyncio-delayed-calls:

Lên lịch callback bị trì hoãn
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Event loop cung cấp các cơ chế để lên lịch cho các hàm callback được gọi vào một thời điểm nào đó trong tương lai. Event loop sử dụng đồng hồ đơn điệu (monotonic clock) để theo dõi thời gian.


.. method:: loop.call_later(delay, callback, *args, context=None)

   Lên lịch để *callback* được gọi sau số giây *delay* đã cho (có thể là int hoặc float).

   Một instance của :class:`asyncio.TimerHandle` được trả về và có thể được sử dụng để hủy callback.

   *callback* sẽ được gọi chính xác một lần. Nếu hai callback được lên lịch vào chính xác cùng một thời điểm, thứ tự chúng được gọi là không xác định.

   Các *args* vị trí tùy chọn sẽ được truyền cho callback khi callback được gọi. Sử dụng :func:`functools.partial`
   :ref:`để truyền các đối số từ khóa <asyncio-pass-keywords>` cho *callback*.

   Đối số chỉ nhận theo từ khóa *context* tùy chọn cho phép chỉ định một :class:`contextvars.Context` tùy chỉnh để *callback* chạy trong đó. Context hiện tại được sử dụng khi không cung cấp *context*.

   .. note::

      Để tối ưu hiệu năng, các callback được lập lịch bằng :meth:`loop.call_later` có thể chạy sớm hơn tối đa một độ phân giải đồng hồ (xem ``time.get_clock_info('monotonic').resolution``).

   .. versionchanged:: 3.7
      Tham số chỉ nhận theo từ khóa *context* đã được thêm vào. Xem :pep:`567` để biết thêm chi tiết.

   .. versionchanged:: 3.8
      Trong Python 3.7 trở về trước với triển khai event loop mặc định, *delay* không thể vượt quá một ngày. Vấn đề này đã được khắc phục trong Python 3.8.

.. method:: loop.call_at(when, callback, *args, context=None)

   Lập lịch để *callback* được gọi tại mốc thời gian tuyệt đối *when* đã cho (một int hoặc float), sử dụng cùng tham chiếu thời gian với
   :meth:`loop.time`.

   Hành vi của phương thức này giống với :meth:`call_later`.

   Một instance của :class:`asyncio.TimerHandle` được trả về và có thể được sử dụng để hủy callback.

   .. note::

      Để đạt hiệu suất, các callback được lập lịch bằng :meth:`loop.call_at` có thể chạy sớm tối đa một độ phân giải đồng hồ (xem ``time.get_clock_info('monotonic').resolution``).

   .. versionchanged:: 3.7
      Tham số chỉ nhận theo từ khóa *context* đã được thêm vào. Xem :pep:`567` để biết thêm chi tiết.

   .. versionchanged:: 3.8
      Trong Python 3.7 trở về trước với triển khai event loop mặc định, chênh lệch giữa *when* và thời gian hiện tại không thể vượt quá một ngày. Điều này đã được khắc phục trong Python 3.8.

.. method:: loop.time()

   Trả về thời gian hiện tại dưới dạng giá trị :class:`float`, theo đồng hồ đơn điệu nội bộ của event loop.

.. note::
   .. versionchanged:: 3.8
      Trong Python 3.7 trở về trước, các timeout (độ trễ tương đối *delay* hoặc thời điểm tuyệt đối *when*) không được vượt quá một ngày. Điều này đã được khắc phục trong Python 3.8.

.. seealso::

   Hàm :func:`asyncio.sleep`.


Tạo future và task
^^^^^^^^^^^^^^^^^^

.. method:: loop.create_future()

   Tạo một :class:`asyncio.Future` object được gắn với event loop.

   Đây là cách được khuyến nghị để tạo Futures trong asyncio. Cách này cho phép các event loop bên thứ ba cung cấp các triển khai thay thế của đối tượng Future (có hiệu suất hoặc khả năng instrumentation tốt hơn).

   .. versionadded:: 3.5.2

.. method:: loop.create_task(coro, *, name=None, context=None, eager_start=None, **kwargs)

   Lập lịch thực thi :ref:`coroutine <coroutine>` *coro*. Trả về một :class:`Task` object.

   Các event loop bên thứ ba có thể sử dụng subclass riêng của :class:`Task` để đảm bảo khả năng tương tác. Trong trường hợp này, kiểu kết quả là một subclass của :class:`Task`.

   Chữ ký hàm đầy đủ phần lớn giống với chữ ký của
   :class:`Task` constructor (hoặc factory) - tất cả keyword arguments của hàm này đều được truyền tiếp đến interface đó.

   Nếu đối số *name* được cung cấp và không phải là ``None``, đối số này sẽ được đặt làm tên của task bằng :meth:`Task.set_name`.

   Đối số chỉ dành cho keyword tùy chọn *context* cho phép chỉ định một :class:`contextvars.Context` tùy chỉnh để *coro* chạy trong đó. Một bản sao của context hiện tại sẽ được tạo khi không cung cấp *context*.

   Đối số chỉ dành cho keyword tùy chọn *eager_start* cho phép chỉ định task có thực thi eager trong khi gọi create_task hay được lên lịch sau. Nếu không truyền *eager_start*, chế độ do :meth:`loop.set_task_factory` thiết lập sẽ được sử dụng.

   .. versionchanged:: 3.8
      Đã thêm tham số *name*.

   .. versionchanged:: 3.11
      Đã thêm tham số *context*.

   .. versionchanged:: 3.13.3
      Đã thêm ``kwargs``, truyền tiếp các tham số bổ sung tùy ý, bao gồm  ``name`` và ``context``.

   .. versionchanged:: 3.13.4
      Đã hoàn tác thay đổi truyền tiếp *name* và *context* (nếu giá trị là None), đồng thời vẫn truyền tiếp các đối số keyword tùy ý khác (để tránh phá vỡ khả năng tương thích ngược với 3.13.3).

   .. versionchanged:: 3.14
      Tất cả *kwargs* giờ đây đều được truyền tiếp. Tham số *eager_start* hoạt động với eager task factory.

.. method:: loop.set_task_factory(factory)

   Thiết lập một task factory sẽ được sử dụng bởi
   :meth:`loop.create_task`.

   Nếu *factory* là ``None`` thì task factory mặc định sẽ được thiết lập. Nếu không, *factory* phải là một *callable* có signature khớp với ``(loop, coro, **kwargs)``, trong đó *loop* là tham chiếu đến event loop đang hoạt động và *coro* là một đối tượng coroutine. Callable này phải truyền tiếp tất cả *kwargs* và trả về một đối tượng tương thích với :class:`asyncio.Task`.

   .. versionchanged:: 3.13.3
      Bắt buộc phải truyền tiếp tất cả *kwargs* cho :class:`asyncio.Task`.

   .. versionchanged:: 3.13.4
      *name* không còn được truyền cho task factory. *context* không còn được truyền cho task factory nếu nó là ``None``.

      .. versionchanged:: 3.14
         *name* và *context* giờ đây lại luôn được truyền cho task factory.

.. method:: loop.get_task_factory()

   Trả về một task factory hoặc ``None`` nếu đang sử dụng task factory mặc định.


Mở kết nối mạng
^^^^^^^^^^^^^^^

.. method:: loop.create_connection(protocol_factory, \
                 host=None, port=None, *, ssl=None, \ family=0, proto=0, flags=0, sock=None, \ local_addr=None, server_hostname=None, \ ssl_handshake_timeout=None, \ ssl_shutdown_timeout=None, \ happy_eyeballs_delay=None, interleave=None, \ all_errors=False)
   :async:

   Mở một kết nối truyền tải dạng streaming đến địa chỉ được chỉ định bởi *host* và *port*.

   Họ socket có thể là :py:const:`~socket.AF_INET` hoặc
   :py:const:`~socket.AF_INET6` tùy thuộc vào *host* (hoặc đối số *family*, nếu được cung cấp).

   Loại socket sẽ là :py:const:`~socket.SOCK_STREAM`.

   *protocol_factory* phải là một callable trả về một
   Triển khai :ref:`asyncio protocol <asyncio-protocol>`.

   Phương thức này sẽ cố gắng thiết lập kết nối ở chế độ nền. Khi thành công, phương thức trả về một ``(transport, protocol)`` pair.

   Tóm lược theo trình tự thời gian của thao tác bên dưới như sau:

   #. Kết nối được thiết lập và một :ref:`transport <asyncio-transport>` được tạo cho kết nối đó.

   #. *protocol_factory* được gọi mà không có đối số và được kỳ vọng sẽ trả về một thực thể :ref:`protocol <asyncio-protocol>`.

   #. Thực thể protocol được ghép nối với transport bằng cách gọi method của nó
      :meth:`~BaseProtocol.connection_made`.

   #. Một tuple ``(transport, protocol)`` được trả về khi thành công.

   Transport được tạo là một bidirectional stream phụ thuộc vào implementation.

   Các đối số khác:

   * *ssl*: nếu được cung cấp và không phải false, một transport SSL/TLS sẽ được tạo (mặc định, một transport TCP thuần sẽ được tạo). Nếu *ssl* là một đối tượng :class:`ssl.SSLContext`, context này được dùng để tạo transport; nếu *ssl* là :const:`True`, một context mặc định được trả về từ :func:`ssl.create_default_context` sẽ được sử dụng.

     .. seealso:: :ref:`Các vấn đề cần cân nhắc về bảo mật SSL/TLS <ssl-security>`

   * *server_hostname* thiết lập hoặc ghi đè hostname dùng để đối chiếu với chứng chỉ của server đích. Chỉ nên truyền giá trị này nếu *ssl* không phải là ``None``. Theo mặc định, giá trị của đối số *host* được sử dụng. Nếu *host* rỗng, sẽ không có giá trị mặc định và bạn phải truyền một giá trị cho *server_hostname*. Nếu *server_hostname* là một chuỗi rỗng, việc đối chiếu hostname sẽ bị vô hiệu hóa (đây là một rủi ro bảo mật nghiêm trọng, có thể cho phép xảy ra các cuộc tấn công man-in-the-middle).

   * *family*, *proto*, *flags* là family địa chỉ, protocol và flags tùy chọn được truyền cho getaddrinfo() để phân giải *host*. Nếu được cung cấp, tất cả các giá trị này phải là số nguyên từ giá trị tương ứng
     :mod:`socket` các hằng số của module.

   * *happy_eyeballs_delay*, nếu được cung cấp, sẽ bật Happy Eyeballs cho kết nối này. Giá trị này phải là một số dấu phẩy động biểu thị khoảng thời gian tính bằng giây cần chờ một lần thử kết nối hoàn tất trước khi bắt đầu lần thử tiếp theo song song. Đây là "Connection Attempt Delay" được định nghĩa trong :rfc:`8305`. Giá trị mặc định hợp lý được RFC khuyến nghị là ``0.25`` (250 mili giây).

   * *interleave* kiểm soát việc sắp xếp lại địa chỉ khi một tên máy chủ phân giải thành nhiều địa chỉ IP. Nếu ``0`` hoặc không được chỉ định, sẽ không thực hiện sắp xếp lại và các địa chỉ được thử theo thứ tự do :meth:`getaddrinfo` trả về. Nếu chỉ định một số nguyên dương, các địa chỉ sẽ được xen kẽ theo họ địa chỉ và số nguyên đã cho được hiểu là "First Address Family Count" như được định nghĩa trong :rfc:`8305`. Giá trị mặc định là ``0`` nếu không chỉ định *happy_eyeballs_delay*, và là ``1`` nếu có chỉ định.

   * *sock*, nếu được cung cấp, phải là một socket hiện có và đã được kết nối
     :class:`socket.socket` object được transport sử dụng. Nếu cung cấp *sock*, không được chỉ định bất kỳ giá trị nào cho *host*, *port*, *family*, *proto*, *flags*, *happy_eyeballs_delay*, *interleave* và *local_addr*.

     .. note::

        Đối số *sock* chuyển quyền sở hữu socket cho transport được tạo. Để đóng socket, hãy gọi
        :meth:`~asyncio.BaseTransport.close` phương thức.

   * *local_addr*, nếu được cung cấp, là một tuple ``(local_host, local_port)`` dùng để liên kết socket với địa chỉ cục bộ. *local_host* và *local_port* được tra cứu bằng ``getaddrinfo()``, tương tự như *host* và *port*.

   * *ssl_handshake_timeout* là (đối với kết nối TLS) thời gian tính bằng giây chờ quá trình bắt tay TLS hoàn tất trước khi hủy kết nối. ``60.0`` giây nếu ``None`` (mặc định).

   * *ssl_shutdown_timeout* là thời gian tính bằng giây chờ quá trình tắt SSL hoàn tất trước khi hủy kết nối. ``30.0`` giây nếu ``None`` (mặc định).

   * *all_errors* xác định các ngoại lệ được raise khi không thể tạo kết nối. Theo mặc định, chỉ một ``Exception`` được raise: ngoại lệ đầu tiên nếu chỉ có một ngoại lệ hoặc tất cả lỗi có cùng thông báo, hoặc một ``OSError`` duy nhất với các thông báo lỗi được kết hợp. Khi ``all_errors`` là ``True``, một ``ExceptionGroup`` sẽ được raise, chứa tất cả các ngoại lệ (ngay cả khi chỉ có một ngoại lệ).


   .. versionchanged:: 3.5

      Đã bổ sung hỗ trợ SSL/TLS trong :class:`ProactorEventLoop`.

   .. versionchanged:: 3.6

      Tùy chọn socket :ref:`socket.TCP_NODELAY <socket-unix-constants>` được đặt theo mặc định cho tất cả các kết nối TCP.

   .. versionchanged:: 3.7

      Đã bổ sung tham số *ssl_handshake_timeout*.

   .. versionchanged:: 3.8

      Đã thêm các tham số *happy_eyeballs_delay* và *interleave*.

      Thuật toán Happy Eyeballs: Kết nối thành công với các máy chủ dual-stack. Khi đường dẫn IPv4 và giao thức của máy chủ hoạt động, nhưng đường dẫn IPv6 và giao thức của máy chủ không hoạt động, ứng dụng client dual-stack sẽ gặp độ trễ kết nối đáng kể so với client chỉ dùng IPv4. Điều này không mong muốn vì khiến trải nghiệm người dùng của client dual-stack kém hơn. Tài liệu này nêu rõ các yêu cầu đối với những thuật toán giúp giảm độ trễ mà người dùng nhận thấy này, đồng thời cung cấp một thuật toán.

      Để biết thêm thông tin: https://datatracker.ietf.org/doc/html/rfc6555

   .. versionchanged:: 3.11

      Đã thêm tham số *ssl_shutdown_timeout*.

   .. versionchanged:: 3.12
      Đã thêm *all_errors*.

   .. versionchanged:: 3.14.8
      Gây ra một ``ValueError`` nếu ``ssl.check_hostname`` là ``True`` và ``server_hostname`` không được cung cấp.

   .. seealso::

      Hàm :func:`open_connection` là một API thay thế cấp cao. Hàm này trả về một cặp (:class:`StreamReader`, :class:`StreamWriter`) có thể được sử dụng trực tiếp trong mã async/await.

.. method:: loop.create_datagram_endpoint(protocol_factory, \
               local_addr=None, remote_addr=None, *, \ family=0, proto=0, flags=0, \ reuse_port=None, \ allow_broadcast=None, sock=None)
   :async:

   Tạo một kết nối datagram.

   Họ socket có thể là :py:const:`~socket.AF_INET`,
   :py:const:`~socket.AF_INET6`, hoặc :py:const:`~socket.AF_UNIX`, tùy thuộc vào *host* (hoặc đối số *family*, nếu được cung cấp).

   Loại socket sẽ là :py:const:`~socket.SOCK_DGRAM`.

   *protocol_factory* phải là một đối tượng có thể gọi, trả về một
   bản triển khai :ref:`protocol <asyncio-protocol>`.

   Một tuple gồm ``(transport, protocol)`` sẽ được trả về khi thành công.

   Các đối số khác:

   * *local_addr*, nếu được cung cấp, là một tuple ``(local_host, local_port)`` được dùng để liên kết socket trên máy cục bộ. *local_host* và *local_port* được tra cứu bằng :meth:`getaddrinfo`.

     .. note::

        Trên Windows, khi sử dụng proactor event loop với ``local_addr=None``, một :exc:`OSError` với :attr:`!errno.WSAEINVAL` sẽ được raise khi chạy nó.

   * *remote_addr*, nếu được cung cấp, là một tuple ``(remote_host, remote_port)`` được dùng để kết nối socket với một địa chỉ từ xa. *remote_host* và *remote_port* được tra cứu bằng :meth:`getaddrinfo`.

   * *family*, *proto*, *flags* là các family địa chỉ, protocol và flag tùy chọn được truyền qua :meth:`getaddrinfo` để phân giải *host*. Nếu được cung cấp, tất cả các giá trị này phải là số nguyên từ các hằng số tương ứng của module :mod:`socket`.

   * *reuse_port* yêu cầu kernel cho phép liên kết endpoint này với cùng một port mà các endpoint hiện có khác đang được liên kết, miễn là tất cả chúng đều đặt flag này khi được tạo. Tùy chọn này không được hỗ trợ trên Windows và một số hệ điều hành Unix. Nếu hằng số :ref:`socket.SO_REUSEPORT <socket-unix-constants>` không được định nghĩa thì khả năng này không được hỗ trợ.

   * *allow_broadcast* yêu cầu kernel cho phép endpoint này gửi thông báo đến địa chỉ broadcast.

   * Có thể tùy chọn chỉ định *sock* để sử dụng một đối tượng :class:`socket.socket` đã tồn tại và đã được kết nối cho transport. Nếu được chỉ định, cần bỏ qua *local_addr* và *remote_addr* (bắt buộc phải là :const:`None`).

     .. note::

        Đối số *sock* chuyển quyền sở hữu socket cho transport được tạo. Để đóng socket, hãy gọi
        :meth:`~asyncio.BaseTransport.close` phương thức.

   Xem các ví dụ về :ref:`UDP echo client protocol <asyncio-udp-echo-client-protocol>` và
   :ref:`UDP echo server protocol <asyncio-udp-echo-server-protocol>`.

   .. versionchanged:: 3.4.4
      Các tham số *family*, *proto*, *flags*, *reuse_address*, *reuse_port*, *allow_broadcast* và *sock* đã được bổ sung.

   .. versionchanged:: 3.8
      Đã thêm hỗ trợ cho Windows.

   .. versionchanged:: 3.8.1
      Tham số *reuse_address* không còn được hỗ trợ vì việc sử dụng
      :ref:`socket.SO_REUSEADDR <socket-unix-constants>` gây ra mối lo ngại đáng kể về bảo mật đối với UDP. Việc truyền rõ ràng ``reuse_address=True`` sẽ gây ra một ngoại lệ.

      Khi nhiều tiến trình có UID khác nhau gán socket cho cùng một địa chỉ socket UDP bằng ``SO_REUSEADDR``, các gói tin đến có thể được phân phối ngẫu nhiên giữa các socket.

      Trên các nền tảng được hỗ trợ, có thể sử dụng *reuse_port* để thay thế cho chức năng tương tự. Với *reuse_port*,
      :ref:`socket.SO_REUSEPORT <socket-unix-constants>` được sử dụng thay thế, qua đó ngăn cụ thể các tiến trình có UID khác nhau gán socket cho cùng một địa chỉ socket.

   .. versionchanged:: 3.11
      Tham số *reuse_address*, đã bị vô hiệu hóa kể từ Python 3.8.1, 3.7.6 và 3.6.10, nay đã bị loại bỏ hoàn toàn.

.. method:: loop.create_unix_connection(protocol_factory, \
               path=None, *, ssl=None, sock=None, \ server_hostname=None, ssl_handshake_timeout=None, \ ssl_shutdown_timeout=None)
   :async:

   Tạo một kết nối Unix.

   Họ socket sẽ là :py:const:`~socket.AF_UNIX`; kiểu socket sẽ là :py:const:`~socket.SOCK_STREAM`.

   Một tuple gồm ``(transport, protocol)`` sẽ được trả về khi thành công.

   *path* là tên của một Unix domain socket và là bắt buộc, trừ khi tham số *sock* được chỉ định.  Abstract Unix sockets,
   :class:`str`, :class:`bytes` và :class:`~pathlib.Path` paths được hỗ trợ.

   Xem tài liệu về phương thức :meth:`loop.create_connection` để biết thông tin về các đối số của phương thức này.

   .. availability:: Unix.

   .. versionchanged:: 3.7
      Đã thêm tham số *ssl_handshake_timeout*. Tham số *path* giờ đây có thể là một :term:`path-like object`.

   .. versionchanged:: 3.11

      Đã thêm tham số *ssl_shutdown_timeout*.


Tạo máy chủ mạng
^^^^^^^^^^^^^^^^

.. _loop_create_server:

.. method:: loop.create_server(protocol_factory, \
               host=None, port=None, *, \ family=socket.AF_UNSPEC, \ flags=socket.AI_PASSIVE, \ sock=None, backlog=100, ssl=None, \ reuse_address=None, reuse_port=None, \ keep_alive=None, \ ssl_handshake_timeout=None, \ ssl_shutdown_timeout=None, \ start_serving=True)
   :async:

   Tạo một máy chủ TCP (loại socket :const:`~socket.SOCK_STREAM`) lắng nghe trên *port* của địa chỉ *host*.

   Trả về một đối tượng :class:`Server`.

   Đối số:

   * *protocol_factory* phải là một callable trả về một
     :ref:`protocol <asyncio-protocol>` implementation.

   * Tham số *host* có thể được đặt thành nhiều kiểu khác nhau, xác định nơi server sẽ lắng nghe:

     - Nếu *host* là một chuỗi, TCP server sẽ được liên kết với một network interface duy nhất được chỉ định bởi *host*.

     - Nếu *host* là một sequence gồm các chuỗi, TCP server sẽ được liên kết với tất cả network interface được chỉ định bởi sequence đó.

     - Nếu *host* là một chuỗi rỗng hoặc ``None``, tất cả interface sẽ được sử dụng và một danh sách gồm nhiều socket sẽ được trả về (nhiều khả năng một socket cho IPv4 và một socket khác cho IPv6).

   * Tham số *port* có thể được đặt để chỉ định port mà server sẽ lắng nghe. Nếu là ``0`` hoặc ``None`` (mặc định), một port chưa được sử dụng ngẫu nhiên sẽ được chọn (lưu ý rằng nếu *host* phân giải thành nhiều network interface, mỗi interface sẽ được chọn một port ngẫu nhiên khác nhau).

   * *family* có thể được đặt thành :const:`socket.AF_INET` hoặc
     :const:`~socket.AF_INET6` để buộc socket sử dụng IPv4 hoặc IPv6. Nếu không được đặt, *family* sẽ được xác định từ tên máy chủ (mặc định là :const:`~socket.AF_UNSPEC`).

   * *flags* là một bitmask cho :meth:`getaddrinfo`.

   * *sock* có thể được chỉ định tùy chọn để sử dụng một đối tượng socket có sẵn. Nếu được chỉ định, không được chỉ định *host* và *port*.

     .. note::

        Đối số *sock* chuyển quyền sở hữu socket cho server được tạo. Để đóng socket, hãy gọi
        phương thức :meth:`~asyncio.Server.close`.

   * *backlog* là số lượng kết nối tối đa được xếp hàng truyền cho
     :meth:`~socket.socket.listen` (mặc định là 100).

   * *ssl* có thể được đặt thành một đối tượng :class:`~ssl.SSLContext` để bật TLS trên các kết nối được chấp nhận.

   * *reuse_address* yêu cầu kernel sử dụng lại một socket cục bộ đang ở trạng thái ``TIME_WAIT``, mà không cần chờ hết thời gian chờ tự nhiên của socket. Nếu không được chỉ định, tùy chọn này sẽ tự động được đặt thành ``True`` trên Unix.

   * *reuse_port* yêu cầu kernel cho phép endpoint này được liên kết với cùng một cổng mà các endpoint hiện có khác đang được liên kết, miễn là tất cả chúng đều đặt cờ này khi được tạo. Tùy chọn này không được hỗ trợ trên Windows.

   * *keep_alive* được đặt thành ``True`` sẽ duy trì các kết nối bằng cách bật việc truyền thông báo định kỳ.

   .. versionchanged:: 3.13

      Đã thêm tham số *keep_alive*.

   * *ssl_handshake_timeout* là (đối với máy chủ TLS) thời gian tính bằng giây chờ quá trình bắt tay TLS hoàn tất trước khi hủy kết nối. ``60.0`` giây nếu ``None`` (mặc định).

   * *ssl_shutdown_timeout* là thời gian tính bằng giây cần chờ để quá trình tắt SSL hoàn tất trước khi hủy kết nối. ``30.0`` giây nếu ``None`` (mặc định).

   * *start_serving* được đặt thành ``True`` (mặc định) sẽ khiến server được tạo bắt đầu chấp nhận kết nối ngay lập tức. Khi được đặt thành ``False``, người dùng nên await :meth:`Server.start_serving` hoặc
     :meth:`Server.serve_forever` để khiến server bắt đầu chấp nhận kết nối.

   .. versionchanged:: 3.5

      Đã bổ sung hỗ trợ SSL/TLS trong :class:`ProactorEventLoop`.

   .. versionchanged:: 3.5.1

      Tham số *host* có thể là một chuỗi các chuỗi.

   .. versionchanged:: 3.6

      Đã bổ sung các tham số *ssl_handshake_timeout* và *start_serving*. Tùy chọn socket :ref:`socket.TCP_NODELAY <socket-unix-constants>` được đặt theo mặc định cho mọi kết nối TCP.

   .. versionchanged:: 3.11

      Đã bổ sung tham số *ssl_shutdown_timeout*.

   .. seealso::

      Hàm :func:`start_server` là một API thay thế ở cấp cao hơn, trả về một cặp :class:`StreamReader` và :class:`StreamWriter` có thể được sử dụng trong mã async/await.


.. method:: loop.create_unix_server(protocol_factory, path=None, \
                 *, sock=None, backlog=100, ssl=None, \ ssl_handshake_timeout=None, \ ssl_shutdown_timeout=None, \ start_serving=True, cleanup_socket=True)
   :async:

   Tương tự như :meth:`loop.create_server` nhưng hoạt động với họ
   socket :py:const:`~socket.AF_UNIX`.

   *path* là tên của một Unix domain socket và là bắt buộc, trừ khi cung cấp đối số *sock*. Các Unix socket dạng abstract,
   các đường dẫn :class:`str`, :class:`bytes` và :class:`~pathlib.Path` đều được hỗ trợ.

   Nếu *cleanup_socket* là true thì Unix socket sẽ tự động bị xóa khỏi hệ thống tệp khi server được đóng, trừ khi socket đã được thay thế sau khi server được tạo.

   Xem tài liệu về phương thức :meth:`loop.create_server` để biết thông tin về các đối số của phương thức này.

   .. availability:: Unix.

   .. versionchanged:: 3.7

      Đã thêm các tham số *ssl_handshake_timeout* và *start_serving*. Tham số *path* hiện có thể là một đối tượng :class:`~pathlib.Path`.

   .. versionchanged:: 3.11

      Đã bổ sung tham số *ssl_shutdown_timeout*.

   .. versionchanged:: 3.13

      Đã thêm tham số *cleanup_socket*.


.. method:: loop.connect_accepted_socket(protocol_factory, \
               sock, *, ssl=None, ssl_handshake_timeout=None, \ ssl_shutdown_timeout=None)
   :async:

   Đóng gói một kết nối đã được chấp nhận thành một cặp transport/protocol.

   Các server chấp nhận kết nối bên ngoài asyncio nhưng sử dụng asyncio để xử lý chúng có thể dùng phương thức này.

   Tham số:

   * *protocol_factory* phải là một callable trả về một
     :ref:`protocol <asyncio-protocol>` implementation.

   * *sock* là một đối tượng socket có sẵn được trả về từ
     :meth:`socket.accept <socket.socket.accept>`.

     .. note::

        Đối số *sock* chuyển quyền sở hữu socket cho transport được tạo. Để đóng socket, hãy gọi
        :meth:`~asyncio.BaseTransport.close` phương thức.

   * *ssl* có thể được đặt thành một :class:`~ssl.SSLContext` để bật SSL trên các kết nối được chấp nhận.

   * *ssl_handshake_timeout* là (đối với kết nối SSL) thời gian tính bằng giây chờ quá trình bắt tay SSL hoàn tất trước khi hủy kết nối. ``60.0`` giây nếu ``None`` (mặc định).

   * *ssl_shutdown_timeout* là thời gian tính bằng giây cần chờ để quá trình tắt SSL hoàn tất trước khi hủy kết nối. ``30.0`` giây nếu ``None`` (mặc định).

   Trả về một ``(transport, protocol)`` cặp.

   .. versionadded:: 3.5.3

   .. versionchanged:: 3.7

      Đã thêm tham số *ssl_handshake_timeout*.

   .. versionchanged:: 3.11

      Đã bổ sung tham số *ssl_shutdown_timeout*.


Truyền tệp
^^^^^^^^^^

.. method:: loop.sendfile(transport, file, \
                          offset=0, count=None, *, fallback=True)
   :async:

   Gửi một *file* qua một *transport*. Trả về tổng số byte đã gửi.

   Phương thức này sử dụng :meth:`os.sendfile` hiệu năng cao nếu có.

   *file* phải là một đối tượng tệp thông thường được mở ở chế độ nhị phân.

   *offset* cho biết vị trí bắt đầu đọc tệp. Nếu được chỉ định, *count* là tổng số byte cần truyền, thay vì gửi tệp cho đến khi đạt EOF. Vị trí tệp luôn được cập nhật, ngay cả khi phương thức này phát sinh lỗi, và
   :meth:`file.tell() <io.IOBase.tell>` có thể được sử dụng để lấy số byte thực tế đã gửi.

   *fallback* được đặt thành ``True`` sẽ khiến asyncio tự đọc và gửi tệp khi nền tảng không hỗ trợ lời gọi hệ thống sendfile (ví dụ: Windows hoặc socket SSL trên Unix).

   Phát sinh :exc:`SendfileNotAvailableError` nếu hệ thống không hỗ trợ syscall *sendfile* và *fallback* là ``False``.

   .. versionadded:: 3.7


Nâng cấp TLS
^^^^^^^^^^^^

.. method:: loop.start_tls(transport, protocol, \
               sslcontext, *, server_side=False, \ server_hostname=None, ssl_handshake_timeout=None, \ ssl_shutdown_timeout=None)
   :async:

   Nâng cấp một kết nối hiện có dựa trên transport lên TLS.

   Tạo một bộ mã hóa/giải mã TLS và chèn nó giữa *transport* và *protocol*. Bộ mã hóa/giải mã này triển khai cả protocol hướng về *transport* lẫn transport hướng về *protocol*.

   Trả về instance hai giao diện đã tạo. Sau *await*, *protocol* phải ngừng sử dụng *transport* ban đầu và chỉ giao tiếp với đối tượng được trả về, vì bộ mã hóa lưu dữ liệu phía *protocol* trong bộ nhớ đệm và thỉnh thoảng trao đổi thêm các gói phiên TLS với *transport*.

   Trong một số trường hợp (ví dụ: khi transport được truyền vào đã bắt đầu đóng), hàm này có thể trả về ``None``.

   Tham số:

   * các instance *transport* và *protocol* mà những phương thức như
     :meth:`~loop.create_server` và
     :meth:`~loop.create_connection` trả về.

   * *sslcontext*: một instance đã được cấu hình của :class:`~ssl.SSLContext`.

   * *server_side* truyền ``True`` khi một kết nối phía máy chủ đang được nâng cấp (như kết nối được tạo bởi :meth:`~loop.create_server`).

   * *server_hostname*: đặt hoặc ghi đè tên máy chủ mà chứng chỉ của máy chủ đích sẽ được đối chiếu.

   * *ssl_handshake_timeout* là (đối với một kết nối TLS) thời gian tính bằng giây chờ quá trình bắt tay TLS hoàn tất trước khi hủy kết nối. ``60.0`` giây nếu ``None`` (mặc định).

   * *ssl_shutdown_timeout* là thời gian tính bằng giây cần chờ để quá trình SSL shutdown hoàn tất trước khi hủy kết nối. ``30.0`` giây nếu ``None`` (mặc định).

   .. versionadded:: 3.7

   .. versionchanged:: 3.11

      Đã thêm tham số *ssl_shutdown_timeout*.



Theo dõi file descriptor
^^^^^^^^^^^^^^^^^^^^^^^^

.. method:: loop.add_reader(fd, callback, *args)

   Bắt đầu theo dõi file descriptor *fd* để kiểm tra khả năng đọc và gọi *callback* với các đối số được chỉ định khi *fd* sẵn sàng để đọc.

   Mọi callback hiện có đã đăng ký cho *fd* sẽ bị hủy và được thay thế bằng *callback*.

.. method:: loop.remove_reader(fd)

   Dừng theo dõi file descriptor *fd* để kiểm tra khả năng đọc. Trả về ``True`` nếu *fd* trước đó đang được theo dõi để đọc.

.. method:: loop.add_writer(fd, callback, *args)

   Bắt đầu theo dõi file descriptor *fd* để kiểm tra khả năng ghi và gọi *callback* với các đối số được chỉ định *args* khi *fd* sẵn sàng để ghi.

   Mọi callback hiện có đã đăng ký cho *fd* sẽ bị hủy và được thay thế bằng *callback*.

   Sử dụng :func:`functools.partial` :ref:`để truyền các đối số từ khóa <asyncio-pass-keywords>` cho *callback*.

.. method:: loop.remove_writer(fd)

   Ngừng theo dõi bộ mô tả tệp *fd* để kiểm tra khả năng sẵn sàng ghi. Trả về ``True`` nếu *fd* trước đó đang được theo dõi để ghi.

Xem thêm phần :ref:`Nền tảng được hỗ trợ <asyncio-platform-support>` để biết một số hạn chế của các phương thức này.


Làm việc trực tiếp với các đối tượng socket
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Nhìn chung, các triển khai protocol sử dụng các API dựa trên transport như :meth:`loop.create_connection` và :meth:`loop.create_server` nhanh hơn các triển khai làm việc trực tiếp với socket. Tuy nhiên, có một số trường hợp hiệu năng không quan trọng và việc làm việc trực tiếp với các đối tượng :class:`~socket.socket` sẽ thuận tiện hơn.

.. method:: loop.sock_recv(sock, nbytes)
   :async:

   Nhận tối đa *nbytes* từ *sock*.  Phiên bản bất đồng bộ của
   :meth:`socket.recv() <socket.socket.recv>`.

   Trả về dữ liệu đã nhận dưới dạng đối tượng bytes.

   *sock* phải là socket không blocking.

   .. versionchanged:: 3.7
      Mặc dù phương thức này luôn được ghi chép là một phương thức coroutine, các bản phát hành trước Python 3.7 trả về một :class:`Future`. Kể từ Python 3.7, đây là một phương thức ``async def``.

.. method:: loop.sock_recv_into(sock, buf)
   :async:

   Nhận dữ liệu từ *sock* vào bộ đệm *buf*. Mô phỏng theo phương thức blocking
   :meth:`socket.recv_into() <socket.socket.recv_into>`.

   Trả về số byte được ghi vào bộ đệm.

   *sock* phải là socket không blocking.

   .. versionadded:: 3.7

.. method:: loop.sock_recvfrom(sock, bufsize)
   :async:

   Nhận một datagram có kích thước tối đa *bufsize* từ *sock*. Phiên bản bất đồng bộ của
   :meth:`socket.recvfrom() <socket.socket.recvfrom>`.

   Trả về một tuple gồm (dữ liệu đã nhận, địa chỉ từ xa).

   *sock* phải là socket không blocking.

   .. versionadded:: 3.11

.. method:: loop.sock_recvfrom_into(sock, buf, nbytes=0)
   :async:

   Nhận một datagram có kích thước tối đa *nbytes* từ *sock* vào *buf*. Phiên bản bất đồng bộ của
   :meth:`socket.recvfrom_into() <socket.socket.recvfrom_into>`.

   Trả về một tuple gồm (số byte đã nhận, địa chỉ từ xa).

   *sock* phải là socket không blocking.

   .. versionadded:: 3.11

.. method:: loop.sock_sendall(sock, data)
   :async:

   Gửi *data* đến socket *sock*. Phiên bản bất đồng bộ của
   :meth:`socket.sendall() <socket.socket.sendall>`.

   Phương thức này tiếp tục gửi đến socket cho đến khi toàn bộ dữ liệu trong *data* đã được gửi hoặc xảy ra lỗi. ``None`` được trả về khi thành công. Khi xảy ra lỗi, một ngoại lệ sẽ được phát sinh. Ngoài ra, không có cách nào xác định được bao nhiêu dữ liệu, nếu có, đã được phía nhận của kết nối xử lý thành công.

   *sock* phải là socket không blocking.

   .. versionchanged:: 3.7
      Mặc dù phương thức này luôn được ghi trong tài liệu là một phương thức coroutine, trước Python 3.7, nó trả về một :class:`Future`. Kể từ Python 3.7, đây là một phương thức ``async def``.

.. method:: loop.sock_sendto(sock, data, address)
   :async:

   Gửi một datagram từ *sock* đến *address*. Phiên bản bất đồng bộ của
   :meth:`socket.sendto() <socket.socket.sendto>`.

   Trả về số byte đã gửi.

   *sock* phải là socket không blocking.

   .. versionadded:: 3.11

.. method:: loop.sock_connect(sock, address)
   :async:

   Kết nối *sock* với một socket từ xa tại *address*.

   Phiên bản bất đồng bộ của :meth:`socket.connect() <socket.socket.connect>`.

   *sock* phải là socket không blocking.

   Với :class:`SelectorEventLoop`, *address* không cần được phân giải: đối với socket :const:`~socket.AF_INET` và :const:`~socket.AF_INET6`, ``sock_connect`` trước tiên kiểm tra xem *address* đã được phân giải hay chưa bằng cách gọi :func:`socket.inet_pton`, và sử dụng :meth:`loop.getaddrinfo` để phân giải nếu chưa được phân giải.

   :class:`ProactorEventLoop`, vòng lặp sự kiện mặc định trên Windows, không phân giải *address*. Host phải là một địa chỉ IP dạng số; truyền tên host sẽ gây ra :exc:`OSError`. Hãy phân giải địa chỉ bằng
   :meth:`loop.getaddrinfo` trước, hoặc sử dụng :meth:`loop.create_connection`, hàm này phân giải địa chỉ trên mọi nền tảng.

   .. versionchanged:: 3.5.2
      Với :class:`SelectorEventLoop`, ``address`` không còn cần được phân giải nữa.

   .. seealso::

      :meth:`loop.create_connection` và :func:`asyncio.open_connection() <open_connection>`.


.. method:: loop.sock_accept(sock)
   :async:

   Chấp nhận một kết nối. Mô phỏng theo phương thức blocking
   :meth:`socket.accept() <socket.socket.accept>` phương thức.

   Socket phải được liên kết với một địa chỉ và đang lắng nghe các kết nối. Giá trị trả về là một cặp ``(conn, address)`` trong đó *conn* là một đối tượng socket *new* có thể dùng để gửi và nhận dữ liệu trên kết nối, còn *address* là địa chỉ được liên kết với socket ở đầu kia của kết nối.

   *sock* phải là socket không blocking.

   .. versionchanged:: 3.7
      Mặc dù phương thức này luôn được ghi trong tài liệu là một phương thức coroutine, trước Python 3.7, nó trả về một :class:`Future`. Kể từ Python 3.7, đây là một phương thức ``async def``.

   .. seealso::

      :meth:`loop.create_server` và :func:`start_server`.

.. method:: loop.sock_sendfile(sock, file, offset=0, count=None, \
                               *, fallback=True)
   :async:

   Gửi một tệp bằng :mod:`os.sendfile` hiệu suất cao nếu có thể. Trả về tổng số byte đã gửi.

   Phiên bản bất đồng bộ của :meth:`socket.sendfile() <socket.socket.sendfile>`.

   *sock* phải là một :const:`socket.SOCK_STREAM` không chặn
   :class:`~socket.socket`.

   *file* phải là một đối tượng tệp thông thường được mở ở chế độ nhị phân.

   *offset* cho biết bắt đầu đọc tệp từ đâu. Nếu được chỉ định, *count* là tổng số byte cần truyền, thay vì gửi tệp cho đến khi đạt EOF. Vị trí tệp luôn được cập nhật, ngay cả khi phương thức này phát sinh lỗi, và
   :meth:`file.tell() <io.IOBase.tell>` có thể được dùng để lấy số byte thực tế đã gửi.

   *fallback*, khi được đặt thành ``True``, khiến asyncio tự đọc và gửi tệp khi nền tảng không hỗ trợ syscall sendfile (ví dụ: Windows hoặc socket SSL trên Unix).

   Phát sinh :exc:`SendfileNotAvailableError` nếu hệ thống không hỗ trợ syscall *sendfile* và *fallback* là ``False``.

   *sock* phải là socket không blocking.

   .. versionadded:: 3.7


DNS
^^^

.. method:: loop.getaddrinfo(host, port, *, family=0, \
               type=0, proto=0, flags=0)
   :async:

   Phiên bản bất đồng bộ của :meth:`socket.getaddrinfo`.

.. method:: loop.getnameinfo(sockaddr, flags=0)
   :async:

   Phiên bản bất đồng bộ của :meth:`socket.getnameinfo`.

.. note::
   Cả *getaddrinfo* và *getnameinfo* đều sử dụng nội bộ các phiên bản đồng bộ của chúng thông qua thread pool executor mặc định của loop. Khi executor này đã đạt giới hạn, các phương thức này có thể bị trì hoãn, khiến các thư viện networking cấp cao hơn báo cáo thời gian chờ tăng lên. Để giảm thiểu điều này, hãy cân nhắc sử dụng một executor tùy chỉnh cho các tác vụ khác của người dùng hoặc thiết lập một executor mặc định với số lượng worker lớn hơn.

.. versionchanged:: 3.7
   Cả hai phương thức *getaddrinfo* và *getnameinfo* luôn được tài liệu hóa là trả về một coroutine, nhưng trước Python 3.7, trên thực tế, chúng lại trả về các đối tượng :class:`asyncio.Future`. Kể từ Python 3.7, cả hai phương thức đều là coroutine.


Làm việc với pipe
^^^^^^^^^^^^^^^^^

.. method:: loop.connect_read_pipe(protocol_factory, pipe)
   :async:

   Đăng ký đầu đọc của *pipe* trong event loop.

   *protocol_factory* phải là một callable trả về một
   triển khai :ref:`asyncio protocol <asyncio-protocol>`.

   *pipe* là một :term:`đối tượng giống tệp <file object>`. Xem
   :ref:`Các đối tượng pipe được hỗ trợ <asyncio-pipe-objects>` để biết các đối tượng được hỗ trợ làm *pipe*.

   Trả về cặp ``(transport, protocol)``, trong đó *transport* hỗ trợ giao diện :class:`ReadTransport` và *protocol* là một đối tượng được khởi tạo bởi *protocol_factory*.

   Với event loop :class:`SelectorEventLoop`, *pipe* được đặt ở chế độ non-blocking.

.. method:: loop.connect_write_pipe(protocol_factory, pipe)
   :async:

   Đăng ký đầu ghi của *pipe* trong event loop.

   *protocol_factory* phải là một callable trả về một
   triển khai :ref:`asyncio protocol <asyncio-protocol>`.

   *pipe* là một :term:`đối tượng giống tệp <file object>`. Xem
   :ref:`Các đối tượng pipe được hỗ trợ <asyncio-pipe-objects>` để biết các đối tượng được hỗ trợ làm *pipe*.

   Trả về cặp ``(transport, protocol)``, trong đó *transport* hỗ trợ
   giao diện :class:`WriteTransport` và *protocol* là một đối tượng được khởi tạo bởi *protocol_factory*.

   Với event loop :class:`SelectorEventLoop`, *pipe* được đặt ở chế độ non-blocking.

.. _asyncio-pipe-objects:

.. rubric:: Các đối tượng pipe được hỗ trợ

Các phương thức này chỉ hoạt động với những đối tượng mà hệ điều hành có thể thăm dò trạng thái sẵn sàng hoặc thực hiện I/O chồng lấp. Các tệp thông thường trên đĩa **not** được hỗ trợ trên bất kỳ nền tảng nào. asyncio không có I/O tệp bất đồng bộ; hãy sử dụng :meth:`loop.run_in_executor` để đọc và ghi các tệp thông thường mà không chặn event loop.

Trên Unix, với :class:`SelectorEventLoop`, *pipe* phải bọc một trong các đối tượng sau:

* một pipe, chẳng hạn như một đầu của một cặp :func:`os.pipe` hoặc một FIFO được tạo bằng
  :func:`os.mkfifo`;
* một socket;
* một character device, chẳng hạn như một terminal.

Trên Windows, nơi chỉ có :class:`ProactorEventLoop` triển khai các phương thức này, *pipe* phải bao bọc một handle được mở cho overlapped I/O (tức là được tạo bằng cờ ``FILE_FLAG_OVERLAPPED``), vì handle này phải được liên kết với một I/O completion port. Các handle không được mở cho overlapped I/O sẽ bị từ chối. Cụ thể, các standard stream (:data:`sys.stdin`,
:data:`sys.stdout` và :data:`sys.stderr`), các console handle và các pipe được tạo bởi :func:`os.pipe` đều **không** được mở cho overlapped I/O, do đó không thể được sử dụng với các phương thức này.

.. note::

   :class:`SelectorEventLoop` không hỗ trợ các phương thức trên trong Windows. Thay vào đó, hãy sử dụng :class:`ProactorEventLoop` cho Windows.

.. seealso::

   Các phương thức :meth:`loop.subprocess_exec` và
   của :meth:`loop.subprocess_shell`.


Tín hiệu Unix
^^^^^^^^^^^^^

.. _loop_add_signal_handler:

.. method:: loop.add_signal_handler(signum, callback, *args)

   Đặt *callback* làm trình xử lý cho tín hiệu *signum*, truyền *args* làm các đối số vị trí.

   callback sẽ được *loop* gọi cùng với các callback khác đang chờ và các coroutine có thể chạy của event loop đó. Không giống các trình xử lý tín hiệu được đăng ký bằng :func:`signal.signal`, callback được đăng ký bằng hàm này được phép tương tác với event loop.

   Phát sinh :exc:`ValueError` nếu số hiệu tín hiệu không hợp lệ hoặc không thể bắt. Phát sinh :exc:`RuntimeError` nếu có vấn đề khi thiết lập trình xử lý.

   Sử dụng :func:`functools.partial` :ref:`để truyền các đối số từ khóa <asyncio-pass-keywords>` cho *callback*.

   Giống như :func:`signal.signal`, hàm này phải được gọi trong main thread.

.. method:: loop.remove_signal_handler(sig)

   Xóa trình xử lý cho tín hiệu *sig*.

   Trả về ``True`` nếu trình xử lý tín hiệu đã bị xóa, hoặc ``False`` nếu chưa có trình xử lý nào được thiết lập cho tín hiệu đã cho.

   .. availability:: Unix.

.. seealso::

   Mô-đun :mod:`signal`.


Thực thi mã trong các thread hoặc process pool
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. awaitablemethod:: loop.run_in_executor(executor, func, *args)

   Sắp xếp để *func* được gọi trong executor được chỉ định, với *args* làm các đối số vị trí.

   Đối số *executor* phải là một thực thể :class:`concurrent.futures.Executor`. Executor mặc định được sử dụng nếu *executor* là ``None``. Executor mặc định có thể được thiết lập bằng :meth:`loop.set_default_executor`; nếu không, một :class:`concurrent.futures.ThreadPoolExecutor` sẽ được khởi tạo theo nhu cầu và được :func:`run_in_executor` sử dụng khi cần.

   Ví dụ::

      import asyncio
      import concurrent.futures

      def blocking_io():
          # Các thao tác với tệp (chẳng hạn như ghi nhật ký) có thể chặn
          # vòng lặp sự kiện: chạy chúng trong thread pool.
          with open('/dev/urandom', 'rb') as f:
              return f.read(100)

      def cpu_bound():
          # Các thao tác phụ thuộc CPU sẽ chặn vòng lặp sự kiện:
          # nhìn chung, nên chạy chúng trong một
          # process pool.
          return sum(i * i for i in range(10 ** 7))

      async def main():
          loop = asyncio.get_running_loop()

          ## Các tùy chọn:

          # 1. Chạy trong executor mặc định của vòng lặp:
          result = await loop.run_in_executor(
              None, blocking_io)
          print('default thread pool', result)

          # 2. Chạy trong thread pool tùy chỉnh:
          with concurrent.futures.ThreadPoolExecutor() as pool:
              result = await loop.run_in_executor(
                  pool, blocking_io)
              print('custom thread pool', result)

          # 3. Chạy trong một process pool tùy chỉnh:
          with concurrent.futures.ProcessPoolExecutor() as pool:
              result = await loop.run_in_executor(
                  pool, cpu_bound)
              print('custom process pool', result)

          # 4. Chạy trong một interpreter pool tùy chỉnh:
          with concurrent.futures.InterpreterPoolExecutor() as pool:
              result = await loop.run_in_executor(
                  pool, cpu_bound)
              print('custom interpreter pool', result)

      if __name__ == '__main__':
          asyncio.run(main())

   Lưu ý rằng guard điểm vào (``if __name__ == '__main__'``) là bắt buộc đối với tùy chọn 3 do những đặc thù của :mod:`multiprocessing`, được :class:`~concurrent.futures.ProcessPoolExecutor` sử dụng. Xem :ref:`Nhập main module an toàn <multiprocessing-safe-main-import>`.

   Phương thức này trả về một đối tượng :class:`asyncio.Future`.

   Sử dụng :func:`functools.partial` :ref:`để truyền các đối số từ khóa <asyncio-pass-keywords>` cho *func*.

   .. versionchanged:: 3.5.3
      :meth:`loop.run_in_executor` no longer configures the
      ``max_workers`` của thread pool executor mà nó tạo ra, thay vào đó để thread pool executor (:class:`~concurrent.futures.ThreadPoolExecutor`) tự đặt giá trị mặc định.

.. method:: loop.set_default_executor(executor)

   Đặt *executor* làm executor mặc định được :meth:`run_in_executor` sử dụng. *executor* phải là một instance của
   :class:`~concurrent.futures.ThreadPoolExecutor`, bao gồm
   :class:`~concurrent.futures.InterpreterPoolExecutor`.

   .. versionchanged:: 3.11
      *executor* phải là một thực thể của
      :class:`~concurrent.futures.ThreadPoolExecutor`.


API xử lý lỗi
^^^^^^^^^^^^^

Cho phép tùy chỉnh cách các ngoại lệ được xử lý trong event loop.

.. method:: loop.set_exception_handler(handler)

   Đặt *handler* làm trình xử lý ngoại lệ mới của event loop.

   Nếu *handler* là ``None``, trình xử lý ngoại lệ mặc định sẽ được đặt. Nếu không, *handler* phải là một callable có signature khớp với ``(loop, context)``, trong đó ``loop`` là tham chiếu đến event loop đang hoạt động và ``context`` là một đối tượng ``dict`` chứa thông tin chi tiết về ngoại lệ (xem tài liệu :meth:`call_exception_handler` để biết chi tiết về context).

   Nếu trình xử lý được gọi thay mặt cho một :class:`~asyncio.Task` hoặc
   :class:`~asyncio.Handle`, nó được chạy trong
   :class:`contextvars.Context` của tác vụ hoặc handle đó.

   .. versionchanged:: 3.12

      Handler có thể được gọi trong :class:`~contextvars.Context` của tác vụ hoặc handle nơi ngoại lệ bắt nguồn.

.. method:: loop.get_exception_handler()

   Trả về exception handler hiện tại hoặc ``None`` nếu chưa thiết lập exception handler tùy chỉnh nào.

   .. versionadded:: 3.5.2

.. method:: loop.default_exception_handler(context)

   Exception handler mặc định.

   Hàm này được gọi khi xảy ra ngoại lệ và chưa thiết lập exception handler nào. Một exception handler tùy chỉnh muốn chuyển việc xử lý cho behavior của handler mặc định cũng có thể gọi hàm này.

   Tham số *context* có cùng ý nghĩa như trong
   :meth:`call_exception_handler`.

.. method:: loop.call_exception_handler(context)

   Gọi exception handler của event loop hiện tại.

   *context* là một ``dict`` đối tượng chứa các khóa sau (các khóa mới có thể được giới thiệu trong những phiên bản Python tương lai):

   * 'message': Thông báo lỗi;
   * 'exception' (tùy chọn): Đối tượng Exception;
   * 'future' (tùy chọn): :class:`asyncio.Future` instance;
   * 'task' (tùy chọn): :class:`asyncio.Task` instance;
   * 'handle' (tùy chọn): :class:`asyncio.Handle` instance;
   * 'protocol' (optional): :ref:`Protocol <asyncio-protocol>` instance;
   * 'transport' (optional): :ref:`Transport <asyncio-transport>` instance;
   * 'socket' (tùy chọn): instance của :class:`socket.socket`;
   * 'source_traceback' (optional): Traceback của nguồn;
   * 'handle_traceback' (optional): Traceback của handle;
   * 'asyncgen' (optional): Trình sinh bất đồng bộ gây ra
                            ngoại lệ.

   .. note::

       Không nên overload phương thức này trong các event loop được phân lớp. Để xử lý ngoại lệ tùy chỉnh, hãy sử dụng phương thức :meth:`set_exception_handler`.

Bật chế độ debug
^^^^^^^^^^^^^^^^

.. method:: loop.get_debug()

   Lấy chế độ debug (:class:`bool`) của event loop.

   Giá trị mặc định là ``True`` nếu biến môi trường
   :envvar:`PYTHONASYNCIODEBUG` được đặt thành một chuỗi không rỗng, ngược lại là ``False``.

.. method:: loop.set_debug(enabled: bool)

   Đặt chế độ debug của event loop.

   .. versionchanged:: 3.7

      :ref:`Python Development Mode <devmode>` hiện cũng có thể được dùng để bật chế độ debug.

.. attribute:: loop.slow_callback_duration

   Thuộc tính này có thể được dùng để đặt thời lượng thực thi tối thiểu, tính bằng giây, được xem là "chậm". Khi bật chế độ debug, các callback "chậm" sẽ được ghi log.

   Giá trị mặc định là 100 mili giây.

.. seealso::

   Chế độ :ref:`debug của asyncio <asyncio-debug-mode>`.


Chạy các tiến trình con
^^^^^^^^^^^^^^^^^^^^^^^

Các phương thức được mô tả trong tiểu mục này ở mức thấp. Trong mã async/await thông thường, hãy cân nhắc sử dụng các hàm cấp cao
:func:`asyncio.create_subprocess_shell` và
:func:`asyncio.create_subprocess_exec` các hàm tiện lợi thay thế.

.. note::

   Trên Windows, event loop mặc định :class:`ProactorEventLoop` hỗ trợ subprocess, trong khi :class:`SelectorEventLoop` thì không. Xem
   :ref:`Hỗ trợ subprocess trên Windows <asyncio-windows-subprocess>` để biết chi tiết.

.. _loop_subprocess_exec:

.. method:: loop.subprocess_exec(protocol_factory, *args, \
             stdin=subprocess.PIPE, stdout=subprocess.PIPE, \ stderr=subprocess.PIPE, ****kwargs)
   :async:

   Tạo một subprocess từ một hoặc nhiều đối số chuỗi được chỉ định bởi *args*.

   *args* phải là một danh sách các chuỗi được biểu diễn bởi:

   * :class:`str`;
   * hoặc :class:`bytes`, được mã hóa theo
     :ref:`mã hóa hệ thống tệp <filesystem-encoding>`.

   Chuỗi đầu tiên chỉ định tệp thực thi của chương trình, còn các chuỗi còn lại chỉ định các đối số. Kết hợp lại, các đối số chuỗi tạo thành ``argv`` của chương trình.

   Điều này tương tự như lớp :class:`subprocess.Popen` của thư viện chuẩn được gọi với ``shell=False`` và danh sách các chuỗi được truyền làm đối số đầu tiên; tuy nhiên, trong khi :class:`~subprocess.Popen` nhận một đối số duy nhất là danh sách các chuỗi, *subprocess_exec* nhận nhiều đối số chuỗi.

   *protocol_factory* phải là một đối tượng có thể gọi, trả về một lớp con của
   :class:`asyncio.SubprocessProtocol` lớp.

   Các tham số khác:

   * *stdin* có thể là bất kỳ đối tượng nào sau đây:

     * một đối tượng giống tệp
     * một file descriptor hiện có (một số nguyên dương), chẳng hạn như những file descriptor được tạo bằng :meth:`os.pipe`
     * hằng số :const:`subprocess.PIPE` (mặc định), hằng số này sẽ tạo một pipe mới và kết nối với pipe đó,
     * giá trị ``None``, giá trị này sẽ khiến subprocess kế thừa file descriptor từ process này
     * hằng số :const:`subprocess.DEVNULL`, cho biết rằng file đặc biệt :data:`os.devnull` sẽ được sử dụng

   * *stdout* có thể là bất kỳ giá trị nào trong số sau:

     * một đối tượng giống tệp
     * hằng số :const:`subprocess.PIPE` (mặc định), hằng số này sẽ tạo một pipe mới và kết nối với pipe đó,
     * giá trị ``None``, giá trị này sẽ khiến subprocess kế thừa file descriptor từ process này
     * hằng số :const:`subprocess.DEVNULL`, cho biết rằng file đặc biệt :data:`os.devnull` sẽ được sử dụng

   * *stderr* có thể là bất kỳ giá trị nào sau đây:

     * một đối tượng giống tệp
     * hằng số :const:`subprocess.PIPE` (mặc định), hằng số này sẽ tạo một pipe mới và kết nối với pipe đó,
     * giá trị ``None``, giá trị này sẽ khiến subprocess kế thừa file descriptor từ process này
     * hằng số :const:`subprocess.DEVNULL`, cho biết rằng file đặc biệt :data:`os.devnull` sẽ được sử dụng
     * hằng số :const:`subprocess.STDOUT` sẽ kết nối luồng lỗi chuẩn với luồng đầu ra chuẩn của tiến trình

   * Tất cả đối số từ khóa khác được truyền cho :class:`subprocess.Popen` mà không được diễn giải, ngoại trừ *bufsize*, *universal_newlines*, *shell*, *text*, *encoding* và *errors*, vốn hoàn toàn không được chỉ định.

     API ``asyncio`` subprocess không hỗ trợ giải mã các luồng dưới dạng văn bản. Có thể sử dụng :func:`bytes.decode` để chuyển đổi các byte được trả về từ luồng thành văn bản.

   Nếu một đối tượng giống tệp được truyền dưới dạng *stdin*, *stdout* hoặc *stderr* đại diện cho một pipe, thì đầu còn lại của pipe này phải được đăng ký với
   :meth:`~loop.connect_write_pipe` hoặc :meth:`~loop.connect_read_pipe` để sử dụng với event loop.

   Xem hàm khởi tạo của lớp :class:`subprocess.Popen` để biết tài liệu về các đối số khác.

   Trả về một cặp ``(transport, protocol)``, trong đó *transport* tuân theo lớp cơ sở :class:`asyncio.SubprocessTransport` và *protocol* là một đối tượng được khởi tạo bởi *protocol_factory*.

   Nếu transport bị đóng hoặc bị garbage collect, tiến trình con sẽ bị kill nếu vẫn đang chạy.

.. method:: loop.subprocess_shell(protocol_factory, cmd, *, \
               stdin=subprocess.PIPE, stdout=subprocess.PIPE, \ stderr=subprocess.PIPE, ****kwargs)
   :async:

   Tạo một subprocess từ *cmd*, có thể là một :class:`str` hoặc một
   :class:`bytes` chuỗi được mã hóa theo
   :ref:`mã hóa filesystem <filesystem-encoding>`, bằng cú pháp "shell" của nền tảng.

   Điều này tương tự như lớp :class:`subprocess.Popen` trong standard library được gọi với ``shell=True``.

   *protocol_factory* phải là một đối tượng có thể gọi, trả về một lớp con của
   lớp :class:`SubprocessProtocol`.

   Xem :meth:`~loop.subprocess_exec` để biết thêm chi tiết về các đối số còn lại.

   Trả về một cặp ``(transport, protocol)``, trong đó *transport* tuân theo lớp cơ sở :class:`SubprocessTransport` và *protocol* là một đối tượng được khởi tạo bởi *protocol_factory*.

   Nếu transport bị đóng hoặc bị garbage collect, tiến trình con sẽ bị kill nếu vẫn đang chạy.

.. note::
   Ứng dụng có trách nhiệm đảm bảo rằng mọi khoảng trắng và ký tự đặc biệt đều được trích dẫn phù hợp để tránh các lỗ hổng `shell injection <https://en.wikipedia.org/wiki/Shell_injection#Shell_injection>`_. Có thể sử dụng hàm :func:`shlex.quote` để thoát đúng cách các khoảng trắng và ký tự đặc biệt trong những chuỗi sẽ được dùng để tạo các lệnh shell.


.. _`Callback handles`:

Các handle callback
===================

.. class:: Handle

   Một đối tượng wrapper callback được trả về bởi :meth:`loop.call_soon`,
   :meth:`loop.call_soon_threadsafe`.

   .. method:: get_context()

      Trả về đối tượng :class:`contextvars.Context` được liên kết với handle.

      .. versionadded:: 3.12

   .. method:: cancel()

      Hủy callback. Nếu callback đã bị hủy hoặc đã được thực thi, phương thức này không có tác dụng.

   .. method:: cancelled()

      Trả về ``True`` nếu callback đã bị hủy.

      .. versionadded:: 3.7

.. class:: TimerHandle

   Một đối tượng wrapper của callback được :meth:`loop.call_later` và :meth:`loop.call_at` trả về.

   Lớp này là lớp con của :class:`Handle`.

   .. method:: when()

      Trả về thời điểm callback được lập lịch dưới dạng số giây :class:`float`.

      Thời điểm này là một dấu thời gian tuyệt đối, sử dụng cùng tham chiếu thời gian với :meth:`loop.time`.

      .. versionadded:: 3.7


.. _`Server objects`:

Đối tượng Server
================

Đối tượng Server được tạo bởi :meth:`loop.create_server`,
các hàm :meth:`loop.create_unix_server`, :func:`start_server` và :func:`start_unix_server`.

Không khởi tạo trực tiếp lớp :class:`Server`.

.. class:: Server

   *Server* là các asynchronous context manager. Khi được sử dụng trong câu lệnh ``async with``, bạn được đảm bảo rằng đối tượng Server đã được đóng và không chấp nhận kết nối mới khi câu lệnh ``async with`` hoàn tất::

      srv = await loop.create_server(...)

      async with srv:
          # một đoạn mã

      # Tại thời điểm này, srv đã được đóng và không còn chấp nhận kết nối mới.


   .. versionchanged:: 3.7
      Đối tượng Server là một asynchronous context manager kể từ Python 3.7.

   .. versionchanged:: 3.11
      Lớp này được cung cấp công khai dưới dạng ``asyncio.Server`` trong Python 3.9.11, 3.10.3 và 3.11.

   .. method:: close()

      Dừng cung cấp dịch vụ: đóng các socket lắng nghe và đặt thuộc tính :attr:`sockets` thành ``None``.

      Các socket đại diện cho những kết nối client đến hiện có vẫn được giữ mở.

      Server được đóng bất đồng bộ; sử dụng coroutine :meth:`wait_closed` để chờ cho đến khi server được đóng (và không còn kết nối nào đang hoạt động).

   .. method:: close_clients()

      Đóng tất cả các kết nối client đến hiện có.

      Gọi :meth:`~asyncio.BaseTransport.close` trên tất cả các transport liên kết.

      Cần gọi :meth:`close` trước :meth:`close_clients` khi đóng server để tránh tranh chấp với các client mới đang kết nối.

      .. versionadded:: 3.13

   .. method:: abort_clients()

      Đóng ngay lập tức tất cả kết nối đến hiện có của client mà không chờ các thao tác đang chờ hoàn tất.

      Gọi :meth:`~asyncio.WriteTransport.abort` trên tất cả transport liên kết.

      Cần gọi :meth:`close` trước :meth:`abort_clients` khi đóng server để tránh tranh chấp với các client mới đang kết nối.

      .. versionadded:: 3.13

   .. method:: get_loop()

      Trả về event loop liên kết với đối tượng server.

      .. versionadded:: 3.7

   .. method:: start_serving()
      :async:

      Bắt đầu chấp nhận kết nối.

      Phương thức này có tính idempotent, vì vậy có thể gọi khi server đã bắt đầu phục vụ.

      Tham số chỉ nhận theo từ khóa *start_serving* của
      :meth:`loop.create_server` và
      :meth:`asyncio.start_server` cho phép tạo một đối tượng Server ban đầu không chấp nhận kết nối. Trong trường hợp này, có thể sử dụng ``Server.start_serving()`` hoặc :meth:`Server.serve_forever` để khiến Server bắt đầu chấp nhận kết nối.

      .. versionadded:: 3.7

   .. method:: serve_forever()
      :async:

      Bắt đầu chấp nhận kết nối cho đến khi coroutine bị hủy. Việc hủy task ``serve_forever`` khiến server bị đóng.

      Có thể gọi phương thức này nếu server đã chấp nhận kết nối. Chỉ một task ``serve_forever`` có thể tồn tại trên mỗi đối tượng *Server*.

      Ví dụ::

          async def client_connected(reader, writer):
              # Giao tiếp với client bằng
              # các stream reader/writer. Ví dụ:
              await reader.readline()

          async def main(host, port):
              srv = await asyncio.start_server(
                  client_connected, host, port)
              await srv.serve_forever()

          asyncio.run(main('127.0.0.1', 0))

      .. versionadded:: 3.7

   .. method:: is_serving()

      Trả về ``True`` nếu server đang chấp nhận các kết nối mới.

      .. versionadded:: 3.7

   .. method:: wait_closed()
      :async:

      Chờ cho đến khi phương thức :meth:`close` hoàn tất và tất cả các kết nối đang hoạt động đã kết thúc.

      .. versionchanged:: 3.12
         ``wait_closed()`` hiện sẽ chờ cho đến khi server được đóng và tất cả các kết nối đang hoạt động đã kết thúc. Trước đây, phương thức này trả về ngay lập tức nếu server đã được đóng, ngay cả khi vẫn còn các kết nối đang hoạt động.

   .. attribute:: sockets

      Danh sách các đối tượng giống socket, ``asyncio.trsock.TransportSocket``, mà server đang lắng nghe.

      .. versionchanged:: 3.7
         Trước Python 3.7, ``Server.sockets`` thường trả về trực tiếp một danh sách socket nội bộ của server. Trong 3.7, một bản sao của danh sách đó được trả về.


.. _asyncio-event-loops:
.. _asyncio-event-loop-implementations:

.. _`Event loop implementations`:

Các triển khai event loop
=========================

asyncio đi kèm với hai cách triển khai event loop khác nhau:
:class:`SelectorEventLoop` và :class:`ProactorEventLoop`.

Theo mặc định, asyncio được cấu hình để sử dụng :class:`EventLoop`.


.. class:: SelectorEventLoop

   Một lớp con của :class:`AbstractEventLoop`, dựa trên
   module :mod:`selectors`.

   Sử dụng *selector* hiệu quả nhất hiện có cho nền tảng tương ứng. Bạn cũng có thể tự cấu hình chính xác cách triển khai selector sẽ được sử dụng::

      import asyncio
      import selectors

      async def main():
         ...

      loop_factory = lambda: asyncio.SelectorEventLoop(selectors.SelectSelector())
      asyncio.run(main(), loop_factory=loop_factory)


   .. availability:: Unix, Windows.


.. class:: ProactorEventLoop

   Một lớp con của :class:`AbstractEventLoop` dành cho Windows, sử dụng "I/O Completion Ports" (IOCP).

   .. availability:: Windows.

   .. seealso::

      `Tài liệu MSDN về I/O Completion Ports <https://learn.microsoft.com/windows/win32/fileio/i-o-completion-ports>`_.

.. class:: EventLoop

    Bí danh của lớp con hiệu quả nhất hiện có của :class:`AbstractEventLoop` cho nền tảng tương ứng.

    Đây là bí danh của :class:`SelectorEventLoop` trên Unix và :class:`ProactorEventLoop` trên Windows.

   .. versionadded:: 3.13

.. class:: AbstractEventLoop

   Lớp cơ sở trừu tượng dành cho các event loop tuân thủ asyncio.

   Phần :ref:`asyncio-event-loop-methods` liệt kê tất cả các phương thức mà một triển khai thay thế của ``AbstractEventLoop`` cần định nghĩa.


.. _`Examples`:

Ví dụ
=====

Lưu ý rằng tất cả các ví dụ trong phần này **cố ý** minh họa cách sử dụng các API event loop cấp thấp, chẳng hạn như :meth:`loop.run_forever` và :meth:`loop.call_soon`. Các ứng dụng asyncio hiện đại hiếm khi cần được viết theo cách này; hãy cân nhắc sử dụng các hàm cấp cao như :func:`asyncio.run`.


.. _asyncio_example_lowlevel_helloworld:

Hello World với call_soon()
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ví dụ sử dụng phương thức :meth:`loop.call_soon` để lên lịch một callback. Callback hiển thị ``"Hello World"`` rồi dừng event loop::

    import asyncio

    def hello_world(loop):
        """A callback to print 'Hello World' and stop the event loop"""
        print('Hello World')
        loop.stop()

    loop = asyncio.new_event_loop()

    # Lên lịch gọi hello_world()
    loop.call_soon(hello_world, loop)

    # Lệnh gọi blocking bị gián đoạn bởi loop.stop()
    try:
        loop.run_forever()
    finally:
        loop.close()

.. seealso::

   Một ví dụ :ref:`Hello World <coroutine>` tương tự được tạo bằng coroutine và hàm :func:`run`.


.. _asyncio_example_call_later:

Hiển thị ngày hiện tại với call_later()
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ví dụ về một callback hiển thị ngày hiện tại mỗi giây. Callback sử dụng phương thức :meth:`loop.call_later` để lên lịch lại chính nó sau 5 giây, rồi dừng event loop::

    import asyncio
    import datetime as dt

    def display_date(end_time, loop):
        print(dt.datetime.now())
        if (loop.time() + 1.0) < end_time:
            loop.call_later(1, display_date, end_time, loop)
        else:
            loop.stop()

    loop = asyncio.new_event_loop()

    # Lên lịch cuộc gọi đầu tiên đến display_date()
    end_time = loop.time() + 5.0
    loop.call_soon(display_date, end_time, loop)

    # Lệnh gọi chặn bị gián đoạn bởi loop.stop()
    try:
        loop.run_forever()
    finally:
        loop.close()

.. seealso::

   Một ví dụ tương tự về :ref:`current date <asyncio_example_sleep>` được tạo bằng coroutine và hàm :func:`run`.


.. _asyncio_example_watch_fd:

Theo dõi một file descriptor để phát hiện các sự kiện đọc
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Chờ cho đến khi một file descriptor nhận được dữ liệu bằng cách sử dụng
:meth:`loop.add_reader` method rồi đóng event loop::

    import asyncio
    from socket import socketpair

    # Tạo một cặp file descriptor được kết nối
    rsock, wsock = socketpair()

    loop = asyncio.new_event_loop()

    def reader():
        data = rsock.recv(100)
        print("Received:", data.decode())

        # Đã xong: hủy đăng ký file descriptor
        loop.remove_reader(rsock)

        # Dừng event loop
        loop.stop()

    # Đăng ký file descriptor cho sự kiện đọc
    loop.add_reader(rsock, reader)

    # Mô phỏng việc nhận dữ liệu từ mạng
    loop.call_soon(wsock.send, 'abc'.encode())

    try:
        # Chạy event loop
        loop.run_forever()
    finally:
        # Đã xong. Đóng các socket và event loop.
        rsock.close()
        wsock.close()
        loop.close()

.. seealso::

   * Một :ref:`ví dụ <asyncio_example_create_connection>` tương tự sử dụng transports, protocols và
     phương thức :meth:`loop.create_connection`.

   * Một :ref:`ví dụ <asyncio_example_create_connection-streams>` tương tự khác sử dụng :func:`asyncio.open_connection` function cấp cao và các stream.


.. _asyncio_example_unix_signals:

Thiết lập các trình xử lý tín hiệu cho SIGINT và SIGTERM
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(Ví dụ ``signal`` này chỉ hoạt động trên Unix.)

Đăng ký các trình xử lý cho các tín hiệu :const:`~signal.SIGINT` và :const:`~signal.SIGTERM` bằng phương thức :meth:`loop.add_signal_handler`::

    import asyncio
    import functools
    import os
    import signal

    def ask_exit(signame, loop):
        print("got signal %s: exit" % signame)
        loop.stop()

    async def main():
        loop = asyncio.get_running_loop()

        for signame in {'SIGINT', 'SIGTERM'}:
            loop.add_signal_handler(
                getattr(signal, signame),
                functools.partial(ask_exit, signame, loop))

        await asyncio.sleep(3600)

    print("Event loop running for 1 hour, press Ctrl+C to interrupt.")
    print(f"pid {os.getpid()}: send SIGINT or SIGTERM to exit.")

    asyncio.run(main())

.. _`shell injection`: https://en.wikipedia.org/wiki/Shell_injection#Shell_injection
.. _`MSDN documentation on I/O Completion Ports`: https://learn.microsoft.com/windows/win32/fileio/i-o-completion-ports
