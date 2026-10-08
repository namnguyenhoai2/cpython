:mod:`!threading` --- Song song dựa trên thread
===============================================

.. module:: threading
   :synopsis: Song song dựa trên thread.

**Mã nguồn:** :source:`Lib/threading.py`

--------------

Module này xây dựng các interface threading cấp cao hơn dựa trên module :mod:`_thread` cấp thấp hơn.

.. include:: ../includes/wasm-notavail.rst

Giới thiệu
----------

Module :mod:`!threading` cung cấp một cách để chạy đồng thời nhiều `luồng <https://en.wikipedia.org/wiki/Thread_(computing)>`_ (các đơn vị nhỏ hơn của một process) trong cùng một process. Module này cho phép tạo và quản lý các luồng, giúp thực thi các tác vụ song song và chia sẻ không gian bộ nhớ. Luồng đặc biệt hữu ích khi các tác vụ bị giới hạn bởi I/O, chẳng hạn như thao tác với tệp hoặc gửi yêu cầu mạng, trong đó phần lớn thời gian được dành để chờ tài nguyên bên ngoài.

Một trường hợp sử dụng điển hình của :mod:`!threading` là quản lý một pool các worker thread có thể xử lý đồng thời nhiều tác vụ. Sau đây là ví dụ cơ bản về cách tạo và khởi động các thread bằng :class:`~threading.Thread`::

   import threading
   import time

   def crawl(link, delay=3):
       print(f"crawl started for {link}")
       time.sleep(delay)  # I/O blocking (mô phỏng một yêu cầu mạng)
       print(f"crawl ended for {link}")

   links = [
       "https://python.org",
       "https://docs.python.org",
       "https://peps.python.org",
   ]

   # Khởi động các luồng cho từng liên kết
   threads = []
   for link in links:
       # Sử dụng `args` để truyền các đối số vị trí và `kwargs` cho các đối số từ khóa
       t = threading.Thread(target=crawl, args=(link,), kwargs={"delay": 2})
       threads.append(t)

   # Khởi động từng luồng
   for t in threads:
       t.start()

   # Chờ tất cả các luồng hoàn tất
   for t in threads:
       t.join()

.. versionchanged:: 3.7
   Mô-đun này trước đây là tùy chọn, nhưng hiện luôn khả dụng.

.. seealso::

   :class:`concurrent.futures.ThreadPoolExecutor` cung cấp một interface cấp cao hơn để đẩy các tác vụ vào một luồng chạy nền mà không chặn quá trình thực thi của luồng gọi, đồng thời vẫn có thể truy xuất kết quả của chúng khi cần.

   :mod:`queue` cung cấp một interface an toàn với thread để trao đổi dữ liệu giữa các thread đang chạy.

   :mod:`asyncio` cung cấp một cách tiếp cận khác để đạt được tính đồng thời ở cấp tác vụ mà không cần sử dụng nhiều thread của hệ điều hành.

.. note::

   Trong dòng Python 2.x, module này chứa các tên ``camelCase`` cho một số phương thức và hàm. Những tên này đã không còn được khuyến nghị kể từ Python 3.10, nhưng vẫn được hỗ trợ để tương thích với Python 2.5 trở xuống.


.. impl-detail::

   Trong CPython, do :term:`Global Interpreter Lock <global interpreter lock>`, mỗi lần chỉ một thread có thể thực thi mã Python (mặc dù một số thư viện chú trọng đến hiệu năng có thể khắc phục hạn chế này). Nếu muốn ứng dụng tận dụng tốt hơn các tài nguyên tính toán của những máy có nhiều lõi, bạn nên sử dụng
   :mod:`multiprocessing` hoặc :class:`concurrent.futures.ProcessPoolExecutor`. Tuy nhiên, threading vẫn là một mô hình phù hợp nếu bạn muốn chạy đồng thời nhiều tác vụ phụ thuộc I/O.

Các cân nhắc về GIL và hiệu năng
--------------------------------

Không giống module :mod:`multiprocessing`, module này sử dụng các process riêng biệt để vượt qua :term:`global interpreter lock` (GIL), module threading hoạt động trong một process duy nhất, nghĩa là tất cả thread đều chia sẻ cùng một không gian bộ nhớ. Tuy nhiên, GIL hạn chế mức cải thiện hiệu năng của threading đối với các tác vụ phụ thuộc CPU, vì mỗi lần chỉ một thread có thể thực thi bytecode Python. Dù vậy, thread vẫn là một công cụ hữu ích để đạt được tính đồng thời trong nhiều tình huống.

Kể từ Python 3.13, các bản dựng :term:`free-threaded <free threading>` có thể vô hiệu hóa GIL, cho phép các thread thực thi song song thực sự, nhưng tính năng này không được bật theo mặc định (xem :pep:`703`).

.. TODO: At some point this feature will become available by default.

Tham khảo
---------

Mô-đun này định nghĩa các hàm sau:


.. function:: active_count()

   Trả về số lượng đối tượng :class:`Thread` hiện đang tồn tại. Số lượng được trả về bằng độ dài của danh sách do :func:`.enumerate` trả về.

   Hàm ``activeCount`` là bí danh không được khuyến nghị sử dụng cho hàm này.


.. function:: current_thread()

   Trả về đối tượng :class:`Thread` hiện tại, tương ứng với luồng điều khiển của caller. Nếu luồng điều khiển của caller không được tạo thông qua
   mô-đun :mod:`!threading`, một đối tượng thread giả với chức năng hạn chế sẽ được trả về.

   Hàm ``currentThread`` là bí danh không còn được khuyến nghị cho hàm này.


.. function:: excepthook(args, /)

   Xử lý ngoại lệ chưa được bắt do :func:`Thread.run` phát sinh.

   Đối số *args* có các thuộc tính sau:

   * *exc_type*: Kiểu ngoại lệ.
   * *exc_value*: Giá trị ngoại lệ, có thể là ``None``.
   * *exc_traceback*: Traceback của ngoại lệ, có thể là ``None``.
   * *thread*: Luồng đã phát sinh ngoại lệ, có thể là ``None``.

   Nếu *exc_type* là :exc:`SystemExit`, ngoại lệ sẽ bị bỏ qua một cách im lặng. Nếu không, ngoại lệ sẽ được in ra :data:`sys.stderr`.

   Nếu hàm này phát sinh ngoại lệ, :func:`sys.excepthook` sẽ được gọi để xử lý ngoại lệ đó.

   Có thể ghi đè :func:`threading.excepthook` để kiểm soát cách xử lý các ngoại lệ chưa được bắt do :func:`Thread.run` phát sinh.

   Việc lưu trữ *exc_value* bằng một custom hook có thể tạo ra một chu kỳ tham chiếu. Cần xóa rõ ràng giá trị này để phá vỡ chu kỳ tham chiếu khi không còn cần đến ngoại lệ.

   Việc lưu trữ *thread* bằng một custom hook có thể làm sống lại đối tượng nếu giá trị này được đặt thành một đối tượng đang được hoàn tất. Tránh lưu trữ *thread* sau khi custom hook hoàn tất để tránh làm sống lại các đối tượng.

   .. seealso::
      :func:`sys.excepthook` handles uncaught exceptions.

   .. versionadded:: 3.8

.. data:: __excepthook__

   Lưu giữ giá trị ban đầu của :func:`threading.excepthook`. Giá trị này được lưu để có thể khôi phục giá trị ban đầu trong trường hợp chúng vô tình bị thay thế bằng các đối tượng bị hỏng hoặc đối tượng thay thế.

   .. versionadded:: 3.10

.. function:: get_ident()

   Trả về 'mã định danh luồng' của luồng hiện tại. Đây là một số nguyên khác không. Giá trị của nó không có ý nghĩa trực tiếp; nó được dùng như một mã bí mật để, chẳng hạn, lập chỉ mục vào một dictionary chứa dữ liệu riêng cho từng luồng. Mã định danh luồng có thể được tái sử dụng khi một luồng kết thúc và một luồng khác được tạo.

   .. versionadded:: 3.3


.. function:: get_native_id()

   Trả về Thread ID nguyên bản dạng số nguyên của thread hiện tại do kernel gán. Đây là một số nguyên không âm. Giá trị này có thể được dùng để nhận diện duy nhất thread cụ thể này trên toàn hệ thống (cho đến khi thread kết thúc; sau đó giá trị có thể được OS tái sử dụng).

   .. availability:: Windows, FreeBSD, Linux, macOS, OpenBSD, NetBSD, AIX, DragonFlyBSD, GNU/kFreeBSD.

   .. versionadded:: 3.8

   .. versionchanged:: 3.13
      Đã bổ sung hỗ trợ cho GNU/kFreeBSD.


.. function:: enumerate()

   Trả về danh sách tất cả các đối tượng :class:`Thread` hiện đang hoạt động. Danh sách này bao gồm các thread daemon và các đối tượng thread giả được tạo bởi
   :func:`current_thread`. Danh sách loại trừ các thread đã kết thúc và các thread chưa được khởi động. Tuy nhiên, thread chính luôn nằm trong kết quả, ngay cả khi đã kết thúc.


.. function:: main_thread()

   Trả về đối tượng :class:`Thread` chính. Trong điều kiện bình thường, thread chính là thread nơi trình thông dịch Python được khởi động.

   .. versionadded:: 3.4


.. function:: settrace(func)

   .. index:: single: trace function

   Đặt một hàm trace cho tất cả các thread được khởi động từ module :mod:`!threading`. *func* sẽ được truyền cho :func:`sys.settrace` đối với mỗi thread, trước khi phương thức
   :meth:`~Thread.run` được gọi.

.. function:: settrace_all_threads(func)

   Thiết lập một hàm trace cho tất cả các thread được khởi chạy từ module :mod:`!threading` và tất cả các thread Python hiện đang thực thi.

   *func* sẽ được truyền cho :func:`sys.settrace` đối với mỗi thread, trước khi nó
   :meth:`~Thread.run` được gọi.

   .. versionadded:: 3.12

.. function:: gettrace()

   .. index::
      single: trace function
      single: debugger

   Lấy hàm trace được thiết lập bởi :func:`settrace`.

   .. versionadded:: 3.10


.. function:: setprofile(func)

   .. index:: single: profile function

   Thiết lập một hàm profile cho tất cả các thread được khởi chạy từ module :mod:`!threading`. *func* sẽ được truyền cho :func:`sys.setprofile` đối với mỗi thread, trước khi nó
   :meth:`~Thread.run` được gọi.

.. function:: setprofile_all_threads(func)

   Thiết lập một hàm profile cho tất cả các thread được khởi chạy từ module :mod:`!threading` và tất cả các thread Python hiện đang thực thi.

   *func* sẽ được truyền cho :func:`sys.setprofile` đối với mỗi thread, trước khi thread đó
   :meth:`~Thread.run` được gọi.

   .. versionadded:: 3.12

.. function:: getprofile()

   .. index:: single: profile function

   Lấy hàm profiler do :func:`setprofile` thiết lập.

   .. versionadded:: 3.10


.. function:: stack_size([size])

   Trả về kích thước stack của thread được sử dụng khi tạo các thread mới. Đối số *size* tùy chọn chỉ định kích thước stack sẽ được sử dụng cho các thread được tạo sau đó, và phải là 0 (sử dụng giá trị mặc định của nền tảng hoặc cấu hình) hoặc một giá trị số nguyên dương tối thiểu là 32.768 (32 KiB). Nếu không chỉ định *size*, giá trị 0 sẽ được sử dụng. Nếu không hỗ trợ thay đổi kích thước stack của thread, một :exc:`RuntimeError` sẽ được phát sinh. Nếu kích thước stack được chỉ định không hợp lệ, một :exc:`ValueError` sẽ được phát sinh và kích thước stack không thay đổi. Hiện tại, 32 KiB là giá trị kích thước stack tối thiểu được hỗ trợ để đảm bảo đủ không gian stack cho chính interpreter. Lưu ý rằng một số nền tảng có thể áp dụng các hạn chế riêng đối với các giá trị kích thước stack, chẳng hạn yêu cầu kích thước stack tối thiểu > 32 KiB hoặc yêu cầu cấp phát theo bội số của kích thước trang bộ nhớ hệ thống - cần tham khảo tài liệu của nền tảng để biết thêm thông tin (trang 4 KiB là phổ biến; khi không có thông tin cụ thể hơn, nên sử dụng kích thước stack là bội số của 4096).

   .. availability:: Windows, pthreads.

      Các nền tảng Unix hỗ trợ POSIX threads.


Module này cũng định nghĩa hằng số sau:

.. data:: TIMEOUT_MAX

   Giá trị tối đa được phép cho tham số *timeout* của các hàm blocking (:meth:`Lock.acquire`, :meth:`RLock.acquire`, :meth:`Condition.wait`, v.v.). Việc chỉ định timeout lớn hơn giá trị này sẽ phát sinh một
   :exc:`OverflowError`.

   .. versionadded:: 3.2


Mô-đun này định nghĩa một số lớp, được trình bày chi tiết trong các phần dưới đây.

Thiết kế của mô-đun này phần nào dựa trên mô hình threading của Java. Tuy nhiên, trong khi Java coi lock và condition variable là hành vi cơ bản của mọi đối tượng, thì trong Python, chúng là các đối tượng riêng biệt. Lớp :class:`Thread` của Python hỗ trợ một phần hành vi của lớp Thread trong Java; hiện tại không có mức ưu tiên, không có nhóm thread, và thread không thể bị hủy, dừng, tạm ngưng, tiếp tục hoặc ngắt. Các phương thức static của lớp Thread trong Java, khi được triển khai, sẽ được ánh xạ thành các hàm cấp mô-đun.

Tất cả các phương thức được mô tả dưới đây đều được thực thi một cách nguyên tử.


Dữ liệu cục bộ theo thread
^^^^^^^^^^^^^^^^^^^^^^^^^^

Dữ liệu cục bộ theo thread là dữ liệu có các giá trị riêng cho từng thread. Nếu bạn có dữ liệu mà bạn muốn chỉ thuộc về một thread, hãy tạo một
đối tượng :class:`local` và sử dụng các thuộc tính của đối tượng đó::

   >>> mydata = local()
   >>> mydata.number = 42
   >>> mydata.number
   42

Bạn cũng có thể truy cập từ điển của đối tượng :class:`local`::

   >>> mydata.__dict__
   {'number': 42}
   >>> mydata.__dict__.setdefault('widgets', [])
   []
   >>> mydata.widgets
   []

Nếu chúng ta truy cập dữ liệu trong một thread khác::

   >>> log = []
   >>> def f():
   ...     items = sorted(mydata.__dict__.items())
   ...     log.append(items)
   ...     mydata.number = 11
   ...     log.append(mydata.number)

   >>> import threading
   >>> thread = threading.Thread(target=f)
   >>> thread.start()
   >>> thread.join()
   >>> log
   [[], 11]

chúng ta sẽ nhận được dữ liệu khác.  Hơn nữa, những thay đổi được thực hiện trong thread kia không ảnh hưởng đến dữ liệu được thấy trong thread này::

   >>> mydata.number
   42

Tất nhiên, các giá trị bạn nhận được từ một đối tượng :class:`local`, bao gồm cả
thuộc tính :attr:`~object.__dict__`, là các giá trị tương ứng với thread đang hiện hành tại thời điểm thuộc tính được đọc.  Vì lý do đó, bạn thường không nên lưu các giá trị này qua các thread, vì chúng chỉ áp dụng cho thread mà chúng xuất phát từ đó.

Bạn có thể tạo các đối tượng :class:`local` tùy chỉnh bằng cách tạo lớp con của
lớp :class:`local`::

   >>> class MyLocal(local):
   ...     number = 2
   ...     def __init__(self, /, **kw):
   ...         self.__dict__.update(kw)
   ...     def squared(self):
   ...         return self.number ** 2

Điều này có thể hữu ích để hỗ trợ các giá trị mặc định, các phương thức và việc khởi tạo.  Lưu ý rằng nếu bạn định nghĩa một phương thức :py:meth:`~object.__init__`, phương thức này sẽ được gọi mỗi khi đối tượng :class:`local` được sử dụng trong một thread riêng biệt.  Điều này cần thiết để khởi tạo từ điển của mỗi thread.

Bây giờ, nếu chúng ta tạo một đối tượng :class:`local`::

   >>> mydata = MyLocal(color='red')

chúng ta có một số mặc định::

   >>> mydata.number
   2

một màu ban đầu::

   >>> mydata.color
   'red'
   >>> del mydata.color

Và một phương thức hoạt động trên dữ liệu::

   >>> mydata.squared()
   4

Như trước đây, chúng ta có thể truy cập dữ liệu trong một thread riêng biệt::

   >>> log = []
   >>> thread = threading.Thread(target=f)
   >>> thread.start()
   >>> thread.join()
   >>> log
   [[('color', 'red')], 11]

mà không ảnh hưởng đến dữ liệu của thread này::

   >>> mydata.number
   2
   >>> mydata.color
   Traceback (most recent call last):
   ...
   AttributeError: 'MyLocal' object has no attribute 'color'

Lưu ý rằng các lớp con có thể định nghĩa :term:`__slots__`, nhưng chúng không phải là thread-local. Chúng được dùng chung giữa các thread::

   >>> class MyLocal(local):
   ...     __slots__ = 'number'

   >>> mydata = MyLocal()
   >>> mydata.number = 42
   >>> mydata.color = 'red'

Vì vậy, thread riêng biệt::

   >>> thread = threading.Thread(target=f)
   >>> thread.start()
   >>> thread.join()

ảnh hưởng đến những gì chúng ta thấy::

   >>> mydata.number
   11


.. class:: local()

   Một class biểu diễn dữ liệu cục bộ của thread.


.. _thread-objects:

Các đối tượng thread
^^^^^^^^^^^^^^^^^^^^

Class :class:`Thread` biểu diễn một hoạt động được chạy trong một thread điều khiển riêng biệt. Có hai cách chỉ định hoạt động này: truyền một đối tượng callable vào constructor hoặc ghi đè phương thức :meth:`~Thread.run` trong một subclass. Không nên ghi đè phương thức nào khác (ngoại trừ constructor) trong subclass. Nói cách khác, *chỉ* ghi đè các phương thức ``__init__()`` và :meth:`~Thread.run` của class này.

Sau khi một đối tượng thread được tạo, hoạt động của nó phải được bắt đầu bằng cách gọi phương thức :meth:`~Thread.start` của thread. Thao tác này gọi phương thức :meth:`~Thread.run` trong một thread điều khiển riêng biệt.

Sau khi hoạt động của thread bắt đầu, thread được xem là “đang hoạt động”. Thread không còn hoạt động khi phương thức :meth:`~Thread.run` của nó kết thúc -- entweder bình thường hoặc do phát sinh một ngoại lệ chưa được xử lý. Phương thức :meth:`~Thread.is_alive` kiểm tra xem thread có đang hoạt động hay không.

Các thread khác có thể gọi phương thức :meth:`~Thread.join` của một thread. Thao tác này sẽ chặn thread đang gọi cho đến khi thread được gọi phương thức :meth:`~Thread.join` kết thúc.

Một thread có một tên. Tên này có thể được truyền cho hàm khởi tạo, cũng như được đọc hoặc thay đổi thông qua thuộc tính :attr:`~Thread.name`.

Nếu phương thức :meth:`~Thread.run` phát sinh một ngoại lệ,
:func:`threading.excepthook` được gọi để xử lý ngoại lệ đó. Theo mặc định,
:func:`threading.excepthook` âm thầm bỏ qua :exc:`SystemExit`.

Một thread có thể được đánh dấu là "daemon thread". Ý nghĩa của cờ này là toàn bộ chương trình Python sẽ thoát khi chỉ còn lại các daemon thread. Giá trị ban đầu được kế thừa từ thread tạo ra nó. Cờ này có thể được thiết lập thông qua thuộc tính :attr:`~Thread.daemon` hoặc đối số hàm khởi tạo *daemon*.

.. note::
   Daemon thread sẽ bị dừng đột ngột khi tắt chương trình. Tài nguyên của chúng (chẳng hạn như tệp đang mở, giao dịch cơ sở dữ liệu, v.v.) có thể không được giải phóng đúng cách. Nếu muốn các thread của mình dừng một cách nhẹ nhàng, hãy đặt chúng ở chế độ không phải daemon và sử dụng một cơ chế báo hiệu phù hợp, chẳng hạn như một :class:`Event`.

Có một đối tượng "main thread"; đối tượng này tương ứng với thread điều khiển ban đầu trong chương trình Python. Đây không phải là daemon thread.

Có khả năng các "dummy thread objects" được tạo. Đây là các đối tượng thread tương ứng với "alien threads", tức các thread điều khiển được khởi chạy bên ngoài module threading, chẳng hạn trực tiếp từ mã C. Các dummy thread objects có chức năng hạn chế; chúng luôn được xem là đang hoạt động và là daemonic, đồng thời không thể được :ref:`joined <meth-thread-join>`. Chúng không bao giờ bị xóa, vì không thể phát hiện thời điểm các alien threads kết thúc.


.. class:: Thread(group=None, target=None, name=None, args=(), kwargs={}, *, \
                  daemon=None, context=None)

   Hàm khởi tạo này luôn phải được gọi bằng các đối số từ khóa. Các đối số gồm:

   *group* phải là ``None`` vì nó được dành cho việc mở rộng trong tương lai khi một
   :class:`!ThreadGroup` lớp được triển khai.

   *target* là đối tượng có thể gọi sẽ được gọi bởi phương thức :meth:`run`. Mặc định là ``None``, nghĩa là không có gì được gọi.

   *name* là tên của thread. Theo mặc định, một tên duy nhất được tạo theo dạng "Thread-*N*" trong đó *N* là một số thập phân nhỏ, hoặc "Thread-*N* (target)" trong đó "target" là ``target.__name__`` nếu đối số *target* được chỉ định.

   *args* là danh sách hoặc tuple các đối số để gọi target. Mặc định là ``()``.

   *kwargs* là một dictionary chứa các đối số keyword để gọi target. Mặc định là ``{}``.

   Nếu không phải ``None``, *daemon* sẽ xác định rõ thread có chạy ở chế độ daemonic hay không. Nếu là ``None`` (giá trị mặc định), thuộc tính daemonic sẽ được kế thừa từ thread hiện tại.

   *context* là giá trị :class:`~contextvars.Context` được sử dụng khi khởi động thread. Giá trị mặc định là ``None``, cho biết rằng
   :data:`sys.flags.thread_inherit_context` kiểm soát hành vi. Nếu cờ này là true, các thread sẽ bắt đầu với một bản sao context của bên gọi :meth:`~Thread.start`. Nếu là false, chúng sẽ bắt đầu với một context trống. Để bắt đầu một cách rõ ràng với context trống, hãy truyền một instance mới của
   :class:`~contextvars.Context()`. Để bắt đầu một cách rõ ràng với bản sao của context hiện tại, hãy truyền giá trị từ :func:`~contextvars.copy_context`. Cờ này mặc định là true trên các bản build free-threaded và false trong các trường hợp khác.

   Nếu lớp con ghi đè hàm khởi tạo, nó phải đảm bảo gọi hàm khởi tạo của lớp cơ sở (``Thread.__init__()``) trước khi thực hiện bất kỳ thao tác nào khác trên thread.

   .. versionchanged:: 3.3
      Đã thêm tham số *daemon*.

   .. versionchanged:: 3.10
      Sử dụng tên *target* nếu bỏ qua đối số *name*.

   .. versionchanged:: 3.14
      Đã thêm tham số *context*.

   .. method:: start()

      Bắt đầu hoạt động của thread.

      Phương thức này được gọi nhiều nhất một lần cho mỗi đối tượng thread. Phương thức này sắp xếp để phương thức :meth:`~Thread.run` của đối tượng được gọi trong một luồng điều khiển riêng.

      Phương thức này sẽ phát sinh :exc:`RuntimeError` nếu được gọi nhiều hơn một lần trên cùng một đối tượng thread.

      Nếu được hỗ trợ, đặt tên luồng của hệ điều hành thành
      :attr:`threading.Thread.name`. Tên này có thể bị cắt bớt tùy thuộc vào giới hạn độ dài tên luồng của hệ điều hành.

      .. versionchanged:: 3.14
         Đặt tên luồng của hệ điều hành.

   .. method:: run()

      Phương thức đại diện cho hoạt động của luồng.

      Bạn có thể ghi đè phương thức :meth:`run` này trong một lớp con. Phương thức :meth:`run` tiêu chuẩn gọi đối tượng có thể gọi được truyền vào hàm khởi tạo của đối tượng với tư cách là đối số *target*, nếu có, cùng các đối số vị trí và đối số từ khóa lần lượt lấy từ các đối số *args* và *kwargs*.

      Việc sử dụng list hoặc tuple làm đối số *args* được truyền vào :class:`Thread` có thể đạt được hiệu quả tương tự.

      Ví dụ::

         >>> from threading import Thread
         >>> t = Thread(target=print, args=[1])
         >>> t.run()
         1
         >>> t = Thread(target=print, args=(1,))
         >>> t.run()
         1

   .. _meth-thread-join:

   .. method:: join(timeout=None)

      Chờ cho đến khi thread kết thúc. Thao tác này chặn thread gọi cho đến khi thread được gọi phương thức :meth:`~Thread.join` kết thúc -- dù bình thường hay do một ngoại lệ không được xử lý -- hoặc cho đến khi hết thời gian chờ tùy chọn.

      Khi đối số *timeout* có mặt và không phải ``None``, đối số này phải là một số dấu phẩy động chỉ định thời gian chờ cho thao tác tính bằng giây (hoặc phần lẻ của giây). Vì :meth:`~Thread.join` luôn trả về ``None``, bạn phải gọi :meth:`~Thread.is_alive` sau :meth:`~Thread.join` để xác định xem đã xảy ra hết thời gian chờ hay chưa -- nếu thread vẫn đang hoạt động thì
      lệnh gọi :meth:`~Thread.join` đã hết thời gian chờ.

      Khi đối số *timeout* không có mặt hoặc là ``None``, thao tác sẽ chặn cho đến khi thread kết thúc.

      Có thể join một thread nhiều lần.

      :meth:`~Thread.join` phát sinh :exc:`RuntimeError` nếu cố gắng join thread hiện tại, vì điều đó sẽ gây deadlock. Việc :meth:`~Thread.join` một thread trước khi thread đó được khởi động cũng là lỗi và những lần thử như vậy sẽ phát sinh cùng ngoại lệ.

      Nếu cố gắng join một thread daemon đang chạy trong các giai đoạn cuối của :term:`Python finalization <interpreter shutdown>` thì :meth:`!join` sẽ phát sinh :exc:`PythonFinalizationError`.

      .. versionchanged:: 3.14

         Có thể phát sinh :exc:`PythonFinalizationError`.

   .. attribute:: name

      Một chuỗi chỉ được dùng cho mục đích nhận dạng. Chuỗi này không có ngữ nghĩa. Nhiều thread có thể được đặt cùng một tên. Tên ban đầu được thiết lập bởi constructor.

      Trên một số nền tảng, tên thread được thiết lập ở cấp hệ điều hành khi thread bắt đầu, để tên này hiển thị trong các trình quản lý tác vụ. Tên này có thể bị cắt ngắn để phù hợp với giới hạn riêng của hệ thống (ví dụ: 15 byte trên Linux hoặc 63 byte trên macOS).

      Các thay đổi đối với *name* chỉ được phản ánh ở cấp hệ điều hành khi thread đang chạy được đổi tên. (Việc thiết lập thuộc tính *name* của một thread khác chỉ cập nhật đối tượng Thread trong Python.)

   .. method:: getName()
               setName()

      API getter/setter không còn được khuyến nghị cho :attr:`~Thread.name`; thay vào đó, hãy sử dụng trực tiếp thuộc tính này.

      .. deprecated:: 3.10

   .. attribute:: ident

      'thread identifier' của thread này hoặc ``None`` nếu thread chưa được khởi động. Đây là một số nguyên khác không. Xem hàm :func:`get_ident`. Thread identifier có thể được tái sử dụng khi một thread kết thúc và một thread khác được tạo. Identifier này vẫn khả dụng ngay cả sau khi thread đã kết thúc.

   .. attribute:: native_id

      Thread ID (``TID``) của thread này, do OS (kernel) gán. Đây là một số nguyên không âm, hoặc ``None`` nếu thread chưa được khởi chạy. Xem hàm :func:`get_native_id`. Giá trị này có thể được dùng để định danh duy nhất thread cụ thể này trên toàn hệ thống (cho đến khi thread kết thúc; sau đó giá trị có thể được OS tái sử dụng).

      .. note::

         Tương tự như Process ID, Thread ID chỉ hợp lệ (được đảm bảo là duy nhất trên toàn hệ thống) từ thời điểm thread được tạo cho đến khi thread bị kết thúc.

      .. availability:: Windows, FreeBSD, Linux, macOS, OpenBSD, NetBSD, AIX, DragonFlyBSD.

      .. versionadded:: 3.8

   .. method:: is_alive()

      Trả về việc thread có đang hoạt động hay không.

      Phương thức này trả về ``True`` ngay trước khi phương thức :meth:`~Thread.run` bắt đầu cho đến ngay sau khi phương thức :meth:`~Thread.run` kết thúc. Hàm module :func:`.enumerate` trả về danh sách tất cả các thread đang hoạt động.

   .. attribute:: daemon

      Một giá trị boolean cho biết thread này là daemon thread (``True``) hay không (``False``). Giá trị này phải được thiết lập trước khi :meth:`~Thread.start` được gọi; nếu không, :exc:`RuntimeError` sẽ được phát sinh. Giá trị ban đầu được kế thừa từ thread tạo ra nó; main thread không phải là daemon thread, do đó tất cả các thread được tạo trong main thread mặc định là
      :attr:`~Thread.daemon` = ``False``.

      Toàn bộ chương trình Python sẽ thoát khi không còn thread non-daemon nào đang hoạt động.

   .. method:: isDaemon()
               setDaemon()

      API getter/setter không còn được khuyến nghị cho :attr:`~Thread.daemon`; thay vào đó, hãy sử dụng trực tiếp nó như một thuộc tính.

      .. deprecated:: 3.10


.. _lock-objects:

Đối tượng Lock
^^^^^^^^^^^^^^

Lock nguyên thủy là một primitive đồng bộ hóa không thuộc sở hữu của một thread cụ thể khi bị khóa. Trong Python, hiện đây là primitive đồng bộ hóa ở mức thấp nhất hiện có, được triển khai trực tiếp bởi module mở rộng :mod:`_thread`.

Lock nguyên thủy có một trong hai trạng thái: "locked" hoặc "unlocked". Nó được tạo ở trạng thái unlocked. Nó có hai phương thức cơ bản là :meth:`~Lock.acquire` và
:meth:`~Lock.release`. Khi trạng thái là unlocked, :meth:`~Lock.acquire` chuyển trạng thái thành locked và trả về ngay lập tức. Khi trạng thái là locked,
:meth:`~Lock.acquire` sẽ chặn cho đến khi một lệnh gọi :meth:`~Lock.release` trong thread khác chuyển nó thành unlocked; sau đó, lệnh gọi :meth:`~Lock.acquire` sẽ đặt lại trạng thái thành locked và trả về. Chỉ nên gọi phương thức :meth:`~Lock.release` khi đang ở trạng thái locked; phương thức này chuyển trạng thái thành unlocked và trả về ngay lập tức. Nếu cố gắng giải phóng một lock đang unlocked, một
:exc:`RuntimeError` sẽ được phát sinh.

Lock cũng hỗ trợ :ref:`giao thức quản lý ngữ cảnh <with-locks>`.

Khi có nhiều hơn một thread bị chặn trong :meth:`~Lock.acquire` đang chờ trạng thái chuyển sang unlocked, chỉ một thread tiếp tục khi một lệnh gọi :meth:`~Lock.release` đặt lại trạng thái thành unlocked; không xác định thread nào trong số các thread đang chờ sẽ tiếp tục, và điều này có thể khác nhau giữa các implementation.

Tất cả các phương thức đều được thực thi một cách nguyên tử.


.. class:: Lock()

   Class triển khai các lock object nguyên thủy. Khi một thread đã acquire lock, các lần thử acquire lock tiếp theo sẽ bị chặn cho đến khi lock được release; bất kỳ thread nào cũng có thể release lock đó.

   .. versionchanged:: 3.13
      ``Lock`` hiện là một class. Trong các phiên bản Python trước đây, ``Lock`` là một factory function trả về một instance của kiểu lock riêng bên dưới.


   .. method:: acquire(blocking=True, timeout=-1)

      Acquire lock theo cách blocking hoặc non-blocking.

      Khi được gọi với đối số *blocking* được đặt thành ``True`` (mặc định), lệnh gọi sẽ block cho đến khi lock được unlock, sau đó đặt lock thành locked và trả về ``True``.

      Khi được gọi với đối số *blocking* được đặt thành ``False``, không chặn. Nếu một lệnh gọi với *blocking* được đặt thành ``True`` sẽ bị chặn, trả về ``False`` ngay lập tức; nếu không, đặt khóa thành trạng thái đã khóa và trả về ``True``.

      Khi được gọi với đối số *timeout* kiểu dấu phẩy động được đặt thành một giá trị dương, chặn tối đa trong số giây được chỉ định bởi *timeout* và trong khoảng thời gian khóa chưa thể được lấy. Đối số *timeout* có giá trị ``-1`` chỉ định thời gian chờ không giới hạn. Không được chỉ định *timeout* khi *blocking* là ``False``.

      Giá trị trả về là ``True`` nếu khóa được lấy thành công, và là ``False`` nếu không (ví dụ: nếu *timeout* đã hết hạn).

      .. versionchanged:: 3.2
         Tham số *timeout* là tham số mới.

      .. versionchanged:: 3.2
         Giờ đây, việc lấy khóa có thể bị gián đoạn bởi các tín hiệu trên POSIX nếu triển khai threading nền tảng hỗ trợ tính năng này.

      .. versionchanged:: 3.14
         Giờ đây, việc lấy khóa có thể bị gián đoạn bởi các tín hiệu trên Windows.


   .. method:: release()

      Giải phóng một khóa. Có thể gọi thao tác này từ bất kỳ thread nào, không chỉ thread đã lấy khóa.

      Khi khóa đang ở trạng thái đã khóa, hãy đặt lại về trạng thái chưa khóa rồi trả về. Nếu có luồng nào khác đang bị chặn và chờ khóa chuyển sang trạng thái chưa khóa, hãy cho phép chính xác một luồng trong số đó tiếp tục.

      Khi được gọi trên một khóa chưa khóa, một :exc:`RuntimeError` sẽ được phát sinh.

      Không có giá trị trả về.

   .. method:: locked()

      Trả về ``True`` nếu khóa được lấy.



.. _rlock-objects:

Đối tượng RLock
^^^^^^^^^^^^^^^

Khóa có thể tái nhập (reentrant lock) là một primitive đồng bộ hóa có thể được cùng một luồng lấy nhiều lần. Về mặt nội bộ, nó sử dụng các khái niệm "luồng sở hữu" và "cấp độ đệ quy", bên cạnh trạng thái đã khóa/chưa khóa được các khóa nguyên thủy sử dụng. Ở trạng thái đã khóa, một luồng nào đó sở hữu khóa; ở trạng thái chưa khóa, không có luồng nào sở hữu khóa.

Các luồng gọi phương thức :meth:`~RLock.acquire` của khóa để khóa khóa đó, và phương thức :meth:`~Lock.release` của khóa để mở khóa.

.. note::

  Các khóa reentrant hỗ trợ :ref:`giao thức quản lý ngữ cảnh <with-locks>`, vì vậy bạn nên sử dụng :keyword:`with` thay vì gọi thủ công
  :meth:`~RLock.acquire` và :meth:`~RLock.release` để xử lý việc acquire và release khóa cho một khối mã.

Các cặp gọi :meth:`~RLock.acquire`/:meth:`~RLock.release` của RLock có thể được lồng nhau, không giống như :meth:`~Lock.acquire`/:meth:`~Lock.release` của Lock. Chỉ lần
:meth:`~RLock.release` cuối cùng (tức :meth:`~Lock.release` của cặp ngoài cùng) mới đặt lại khóa về trạng thái không khóa và cho phép một thread khác đang bị chặn trong
:meth:`~RLock.acquire` tiếp tục.

:meth:`~RLock.acquire`/:meth:`~RLock.release` phải được sử dụng theo từng cặp: mỗi lần acquire phải có một lần release trong thread đã acquire khóa. Nếu không gọi release đủ số lần khóa đã được acquire, chương trình có thể bị deadlock.


.. class:: RLock()

   Lớp này triển khai các đối tượng khóa reentrant. Một khóa reentrant phải được release bởi thread đã acquire khóa đó. Sau khi một thread đã acquire khóa reentrant, chính thread đó có thể acquire khóa thêm lần nữa mà không bị chặn; thread phải release khóa một lần cho mỗi lần đã acquire khóa.

   Lưu ý rằng ``RLock`` thực ra là một hàm factory trả về một instance của phiên bản hiệu quả nhất của lớp RLock cụ thể được nền tảng hỗ trợ.


   .. method:: acquire(blocking=True, timeout=-1)

      Acquire một lock, ở chế độ blocking hoặc non-blocking.

      .. seealso::

         :ref:`Sử dụng RLock làm context manager <with-locks>`
            Nên sử dụng cách này thay cho các lệnh gọi :meth:`!acquire` và :meth:`release` thủ công bất cứ khi nào có thể.


      Khi được gọi với đối số *blocking* được đặt thành ``True`` (mặc định):

         * Nếu không có thread nào sở hữu lock, acquire lock và trả về ngay lập tức.

         * Nếu một thread khác sở hữu lock, hãy block cho đến khi có thể acquire lock hoặc *timeout*, nếu được đặt thành một giá trị float dương.

         * Nếu cùng một thread đang sở hữu lock, hãy acquire lock lần nữa rồi trả về ngay lập tức. Đây là điểm khác biệt giữa :class:`Lock` và
           :class:`!RLock`; :class:`Lock` xử lý trường hợp này giống như trường hợp trước đó, chặn cho đến khi có thể acquire lock.

      Khi được gọi với đối số *blocking* được đặt thành ``False``:

         * Nếu không có thread nào sở hữu lock, acquire lock và trả về ngay lập tức.

         * Nếu một thread khác đang sở hữu lock, hãy trả về ngay lập tức.

         * Nếu cùng thread đang sở hữu lock, hãy acquire lock lần nữa rồi trả về ngay lập tức.

      Trong mọi trường hợp, nếu thread có thể acquire lock, hãy trả về ``True``. Nếu thread không thể acquire lock (tức là khi không blocking hoặc đã đạt đến timeout), hãy trả về ``False``.

      Nếu được gọi nhiều lần, việc không gọi :meth:`~RLock.release` đủ số lần tương ứng có thể dẫn đến deadlock. Hãy cân nhắc sử dụng :class:`!RLock` như một context manager thay vì gọi trực tiếp acquire/release.

      .. versionchanged:: 3.2
         Tham số *timeout* là tham số mới.


   .. method:: release()

      Giải phóng lock, giảm cấp độ đệ quy. Nếu sau khi giảm, cấp độ này bằng không, hãy đặt lại lock về trạng thái chưa khóa (không thuộc sở hữu của thread nào) và nếu có thread nào khác đang bị chặn để chờ lock được mở khóa, cho phép chính xác một thread trong số đó tiếp tục. Nếu sau khi giảm, cấp độ đệ quy vẫn khác không, lock vẫn bị khóa và thuộc sở hữu của thread đang gọi.

      Chỉ gọi phương thức này khi thread đang gọi sở hữu lock. Một
      :exc:`RuntimeError` sẽ được raised nếu phương thức này được gọi khi lock chưa được acquire.

      Không có giá trị trả về.


   .. method:: locked()

      Trả về một boolean cho biết đối tượng này hiện có đang bị khóa hay không.

      .. versionadded:: 3.14


.. _condition-objects:

Đối tượng condition
^^^^^^^^^^^^^^^^^^^

Một biến condition luôn được liên kết với một loại lock nào đó; lock này có thể được truyền vào hoặc sẽ được tạo theo mặc định. Việc truyền lock vào rất hữu ích khi nhiều biến condition phải dùng chung một lock. Lock là một phần của đối tượng condition: bạn không cần theo dõi riêng lock này.

Một biến condition tuân theo :ref:`giao thức quản lý ngữ cảnh <with-locks>`: sử dụng câu lệnh ``with`` sẽ lấy lock liên kết trong suốt thời gian của khối được bao quanh. Các phương thức :meth:`~Condition.acquire` và
:meth:`~Condition.release` cũng gọi các phương thức tương ứng của lock liên kết.

Các phương thức khác phải được gọi khi đang giữ lock liên kết. Phương thức
:meth:`~Condition.wait` giải phóng lock, sau đó chặn cho đến khi một thread khác đánh thức nó bằng cách gọi :meth:`~Condition.notify` hoặc
:meth:`~Condition.notify_all`. Sau khi được đánh thức, :meth:`~Condition.wait` sẽ lấy lại lock và trả về. Bạn cũng có thể chỉ định thời gian chờ.

Phương thức :meth:`~Condition.notify` đánh thức một trong các thread đang chờ biến điều kiện, nếu có thread nào đang chờ. Phương thức :meth:`~Condition.notify_all` đánh thức tất cả các thread đang chờ biến điều kiện.

Lưu ý: các phương thức :meth:`~Condition.notify` và :meth:`~Condition.notify_all` không giải phóng lock; điều này có nghĩa là thread hoặc các thread được đánh thức sẽ không ngay lập tức trở về từ lời gọi :meth:`~Condition.wait`, mà chỉ trở về khi thread đã gọi :meth:`~Condition.notify` hoặc :meth:`~Condition.notify_all` cuối cùng giải phóng quyền sở hữu lock.

Kiểu lập trình điển hình sử dụng biến điều kiện dùng lock để đồng bộ hóa quyền truy cập vào một trạng thái dùng chung nào đó; các thread quan tâm đến một thay đổi trạng thái cụ thể sẽ gọi :meth:`~Condition.wait` lặp đi lặp lại cho đến khi thấy trạng thái mong muốn, trong khi các thread sửa đổi trạng thái sẽ gọi
:meth:`~Condition.notify` hoặc :meth:`~Condition.notify_all` khi chúng thay đổi trạng thái theo cách có thể khiến trạng thái đó trở thành trạng thái mong muốn của một trong các thread đang chờ. Ví dụ: đoạn mã sau đây minh họa tình huống producer-consumer tổng quát với dung lượng bộ đệm không giới hạn::

   # Tiêu thụ một mục
   with cv:
       while not an_item_is_available():
           cv.wait()
       get_an_available_item()

   # Tạo một mục
   with cv:
       make_an_item_available()
       cv.notify()

Vòng lặp ``while`` kiểm tra điều kiện của ứng dụng là cần thiết vì :meth:`~Condition.wait` có thể trở về sau một khoảng thời gian dài tùy ý, và điều kiện khiến lời gọi :meth:`~Condition.notify` được thực hiện có thể không còn đúng nữa. Đây là đặc điểm vốn có của lập trình đa thread.
Có thể sử dụng phương thức :meth:`~Condition.wait_for` để tự động hóa việc kiểm tra điều kiện và giúp tính thời gian chờ dễ dàng hơn::

   # Tiêu thụ một mục
   with cv:
       cv.wait_for(an_item_is_available)
       get_an_available_item()

Để chọn giữa :meth:`~Condition.notify` và :meth:`~Condition.notify_all`, hãy cân nhắc xem một thay đổi trạng thái chỉ có thể hữu ích đối với một hay nhiều luồng đang chờ. Ví dụ, trong tình huống producer-consumer điển hình, việc thêm một mục vào bộ đệm chỉ cần đánh thức một luồng consumer.


.. class:: Condition(lock=None)

   Lớp này triển khai các đối tượng biến điều kiện. Biến điều kiện cho phép một hoặc nhiều luồng chờ cho đến khi được một luồng khác thông báo.

   Nếu đối số *lock* được cung cấp và không phải là ``None``, đối số này phải là một đối tượng :class:`Lock` hoặc :class:`RLock`, và được sử dụng làm lock bên dưới. Nếu không, một đối tượng :class:`RLock` mới sẽ được tạo và sử dụng làm lock bên dưới.

   .. versionchanged:: 3.3
      được thay đổi từ một hàm factory thành một lớp.

   .. method:: acquire(*args)

      Acquire lock bên dưới. Phương thức này gọi phương thức tương ứng trên lock bên dưới; giá trị trả về là bất kỳ giá trị nào mà phương thức đó trả về.

   .. method:: release()

      Giải phóng khóa bên dưới. Phương thức này gọi phương thức tương ứng trên khóa bên dưới; không có giá trị trả về.

   .. method:: locked()

      Trả về một giá trị boolean cho biết đối tượng này hiện có đang bị khóa hay không.

      .. versionadded:: 3.14

   .. method:: wait(timeout=None)

      Chờ cho đến khi được thông báo hoặc xảy ra timeout. Nếu thread gọi phương thức này chưa acquire khóa khi phương thức được gọi, một :exc:`RuntimeError` sẽ được phát sinh.

      Phương thức này giải phóng khóa bên dưới, sau đó chặn cho đến khi được đánh thức bởi lệnh gọi :meth:`notify` hoặc :meth:`notify_all` cho cùng biến điều kiện trong một thread khác, hoặc cho đến khi timeout tùy chọn xảy ra. Sau khi được đánh thức hoặc hết thời gian chờ, phương thức acquire lại khóa và trả về.

      Khi đối số *timeout* được cung cấp và không phải là ``None``, đối số này phải là một số dấu phẩy động chỉ định thời gian chờ cho thao tác theo đơn vị giây (hoặc phần lẻ của giây).

      Khi khóa bên dưới là một :class:`RLock`, khóa đó không được giải phóng bằng phương thức :meth:`release` của nó, vì phương thức này có thể không thực sự mở khóa khi khóa đã được acquire nhiều lần theo cách đệ quy. Thay vào đó, một interface nội bộ của lớp :class:`RLock` được sử dụng; interface này thực sự mở khóa ngay cả khi khóa đã được acquire đệ quy nhiều lần. Sau đó, một interface nội bộ khác được sử dụng để khôi phục cấp độ đệ quy khi khóa được acquire lại.

      Giá trị trả về là ``True`` trừ khi một *timeout* nhất định đã hết hạn; trong trường hợp đó, giá trị trả về là ``False``.

      .. versionchanged:: 3.2
         Trước đây, phương thức luôn trả về ``None``.

   .. method:: wait_for(predicate, timeout=None)

      Chờ cho đến khi một điều kiện được đánh giá là true. *predicate* phải là một callable có kết quả được diễn giải dưới dạng giá trị boolean. Có thể cung cấp *timeout* để chỉ định thời gian chờ tối đa.

      Phương thức tiện ích này có thể gọi :meth:`wait` lặp đi lặp lại cho đến khi predicate được thỏa mãn hoặc xảy ra timeout. Giá trị trả về là giá trị trả về cuối cùng của predicate và sẽ được đánh giá là ``False`` nếu phương thức hết thời gian chờ.

      Bỏ qua tính năng timeout, việc gọi phương thức này gần tương đương với việc viết::

        while not predicate():
            cv.wait()

      Do đó, các quy tắc tương tự như với :meth:`wait` được áp dụng: lock phải được giữ khi gọi và được acquire lại khi trả về. Predicate được đánh giá khi lock đang được giữ.

      .. versionadded:: 3.2

   .. method:: notify(n=1)

      Theo mặc định, đánh thức một thread đang chờ điều kiện này, nếu có. Nếu thread gọi chưa acquire lock khi phương thức này được gọi, một
      :exc:`RuntimeError` sẽ được raise.

      Phương thức này đánh thức nhiều nhất *n* luồng đang chờ biến điều kiện; phương thức không thực hiện gì nếu không có luồng nào đang chờ.

      Cách triển khai hiện tại đánh thức chính xác *n* luồng nếu có ít nhất *n* luồng đang chờ. Tuy nhiên, không an toàn khi dựa vào hành vi này. Một cách triển khai được tối ưu hóa trong tương lai đôi khi có thể đánh thức nhiều hơn *n* luồng.

      Lưu ý: một luồng đã được đánh thức thực sự không trở về từ lời gọi :meth:`wait` cho đến khi có thể giành lại lock. Vì :meth:`notify` không giải phóng lock, code gọi nó nên thực hiện việc đó.

   .. method:: notify_all()

      Đánh thức tất cả các luồng đang chờ trên điều kiện này. Phương thức này hoạt động như
      :meth:`notify`, nhưng đánh thức tất cả các luồng đang chờ thay vì chỉ một luồng. Nếu luồng gọi chưa acquire lock khi phương thức này được gọi, một
      :exc:`RuntimeError` sẽ được raise.

      Phương thức ``notifyAll`` là bí danh không được khuyến nghị dùng nữa của phương thức này.


.. _semaphore-objects:

Đối tượng semaphore
^^^^^^^^^^^^^^^^^^^

Đây là một trong những primitive đồng bộ hóa lâu đời nhất trong lịch sử khoa học máy tính, được phát minh bởi nhà khoa học máy tính người Hà Lan thời kỳ đầu Edsger W. Dijkstra (ông sử dụng các tên ``P()`` và ``V()`` thay cho :meth:`~Semaphore.acquire` và
:meth:`~Semaphore.release`).

Một semaphore quản lý một bộ đếm nội bộ, bộ đếm này được giảm đi sau mỗi
lần gọi :meth:`~Semaphore.acquire` và tăng lên sau mỗi lần gọi :meth:`~Semaphore.release`. Bộ đếm không bao giờ có thể nhỏ hơn 0; khi :meth:`~Semaphore.acquire` phát hiện bộ đếm bằng 0, nó sẽ chặn và chờ cho đến khi một thread khác gọi
:meth:`~Semaphore.release`.

Semaphore cũng hỗ trợ :ref:`giao thức quản lý ngữ cảnh <with-locks>`.


.. class:: Semaphore(value=1)

   Lớp này triển khai các đối tượng semaphore. Một semaphore quản lý một bộ đếm nguyên tử biểu thị số lần gọi :meth:`release` trừ đi số lần gọi
   :meth:`acquire`, cộng với giá trị ban đầu. Phương thức :meth:`acquire` sẽ chặn nếu cần thiết cho đến khi có thể trả về mà không làm bộ đếm trở thành số âm. Nếu không được cung cấp, *value* mặc định là 1.

   Đối số tùy chọn cung cấp *giá trị* ban đầu cho bộ đếm nội bộ; giá trị mặc định là ``1``. Nếu *giá trị* được cung cấp nhỏ hơn 0, :exc:`ValueError` sẽ được phát sinh.

   .. versionchanged:: 3.3
      được thay đổi từ một factory function thành một class.

   .. method:: acquire(blocking=True, timeout=None)

      Nhận một semaphore.

      Khi được gọi mà không có đối số:

      * Nếu bộ đếm nội bộ lớn hơn 0 khi bắt đầu, giảm nó đi 1 và trả về ``True`` ngay lập tức.
      * Nếu bộ đếm nội bộ bằng 0 khi bắt đầu, chặn cho đến khi được đánh thức bởi một lời gọi đến
        :meth:`~Semaphore.release`.  Sau khi được đánh thức (và bộ đếm lớn hơn 0), giảm bộ đếm đi 1 và trả về ``True``.  Mỗi lời gọi đến :meth:`~Semaphore.release` sẽ đánh thức chính xác một luồng. Không nên dựa vào thứ tự các luồng được đánh thức.

      Khi được gọi với *blocking* được đặt thành ``False``, không chặn. Nếu một lệnh gọi không có đối số sẽ chặn, lập tức trả về ``False``; nếu không, thực hiện tương tự như khi được gọi không có đối số và trả về ``True``.

      Khi được gọi với *timeout* khác ``None``, nó sẽ chặn trong nhiều nhất *timeout* giây. Nếu acquire không hoàn tất thành công trong khoảng thời gian đó, trả về ``False``. Nếu không, trả về ``True``.

      .. versionchanged:: 3.2
         Tham số *timeout* là tham số mới.

   .. method:: release(n=1)

      Giải phóng một semaphore, tăng bộ đếm nội bộ thêm *n*. Khi giá trị ban đầu là 0 và có các thread khác đang chờ giá trị này lại lớn hơn 0, đánh thức *n* trong số các thread đó.

      .. versionchanged:: 3.9
         Đã thêm tham số *n* để đánh thức nhiều thread đang chờ cùng một lúc.


.. class:: BoundedSemaphore(value=1)

   Lớp triển khai các đối tượng bounded semaphore. Bounded semaphore kiểm tra để đảm bảo giá trị hiện tại của nó không vượt quá giá trị ban đầu. Nếu vượt quá,
   :exc:`ValueError` sẽ được phát sinh. Trong hầu hết các trường hợp, semaphore được dùng để bảo vệ các tài nguyên có dung lượng giới hạn. Nếu semaphore được giải phóng quá nhiều lần, đó là dấu hiệu cho thấy có lỗi. Nếu không được cung cấp, *value* mặc định là 1.

   .. versionchanged:: 3.3
      được thay đổi từ một factory function thành một class.


.. _semaphore-examples:

:class:`Semaphore` ví dụ
^^^^^^^^^^^^^^^^^^^^^^^^

Semaphore thường được dùng để bảo vệ các tài nguyên có dung lượng giới hạn, chẳng hạn như máy chủ cơ sở dữ liệu. Trong mọi trường hợp mà kích thước của tài nguyên là cố định, bạn nên sử dụng bounded semaphore. Trước khi tạo bất kỳ worker thread nào, main thread của bạn sẽ khởi tạo semaphore::

   maxconnections = 5
   # ...
   pool_sema = BoundedSemaphore(value=maxconnections)

Sau khi được tạo, các worker thread sẽ gọi các phương thức acquire và release của semaphore khi cần kết nối với máy chủ::

   with pool_sema:
       conn = connectdb()
       try:
           # ... sử dụng kết nối ...
       finally:
           conn.close()

Việc sử dụng bounded semaphore làm giảm khả năng một lỗi lập trình khiến semaphore được release nhiều lần hơn số lần được acquire mà không bị phát hiện.


.. _event-objects:

Đối tượng Event
^^^^^^^^^^^^^^^

Đây là một trong những cơ chế đơn giản nhất để giao tiếp giữa các thread: một thread phát tín hiệu cho một event và các thread khác chờ event đó.

Một event object quản lý một cờ nội bộ có thể được đặt thành true bằng
:meth:`~Event.set` method và đặt lại thành false bằng :meth:`~Event.clear` method. :meth:`~Event.wait` method sẽ chặn cho đến khi cờ là true.


.. class:: Event()

   Lớp triển khai các event object. Một event quản lý một cờ có thể được đặt thành true bằng :meth:`~Event.set` method và đặt lại thành false bằng
   :meth:`clear` method. :meth:`wait` method sẽ chặn cho đến khi cờ là true. Ban đầu, cờ là false.

   .. versionchanged:: 3.3
      được thay đổi từ một factory function thành một class.

   .. method:: is_set()

      Trả về ``True`` khi và chỉ khi cờ nội bộ là true.

      Phương thức ``isSet`` là bí danh không còn được dùng cho phương thức này.

   .. method:: set()

      Đặt cờ nội bộ thành true. Tất cả các thread đang chờ cờ này chuyển thành true sẽ được đánh thức. Các thread gọi :meth:`wait` sau khi cờ đã là true sẽ hoàn toàn không bị chặn.

   .. method:: clear()

      Đặt lại cờ nội bộ thành false. Sau đó, các thread gọi
      :meth:`wait` sẽ bị chặn cho đến khi :meth:`.set` được gọi để đặt lại cờ nội bộ thành true.

   .. method:: wait(timeout=None)

      Chặn trong khi cờ nội bộ là false và thời gian chờ, nếu được cung cấp, chưa hết hạn. Giá trị trả về cho biết lý do phương thức chặn này trả về; ``True`` nếu trả về vì cờ được đặt thành true, hoặc ``False`` nếu có thời gian chờ được cung cấp và cờ nội bộ không chuyển thành true trong thời gian chờ đã cho.

      Khi đối số timeout xuất hiện và không phải là ``None``, đối số này phải là một số dấu phẩy động chỉ định thời gian chờ cho thao tác tính bằng giây hoặc phần lẻ của giây.

      .. versionchanged:: 3.1
         Trước đây, phương thức này luôn trả về ``None``.


.. _timer-objects:

Đối tượng Timer
^^^^^^^^^^^^^^^

Lớp này đại diện cho một hành động chỉ nên được thực hiện sau khi một khoảng thời gian nhất định đã trôi qua --- một bộ hẹn giờ. :class:`Timer` là một lớp con của :class:`Thread` và do đó cũng là một ví dụ về việc tạo các thread tùy chỉnh.

Cũng như thread, Timer được khởi động bằng cách gọi phương thức :meth:`Timer.start <Thread.start>` của chúng. Có thể dừng Timer (trước khi hành động của nó bắt đầu) bằng cách gọi phương thức
:meth:`~Timer.cancel`. Khoảng thời gian Timer chờ trước khi thực hiện hành động có thể không hoàn toàn giống với khoảng thời gian do người dùng chỉ định.

Ví dụ::

   def hello():
       print("hello, world")

   t = Timer(30.0, hello)
   t.start()  # sau 30 giây, "hello, world" sẽ được in ra


.. class:: Timer(interval, function, args=None, kwargs=None)

   Tạo một Timer sẽ chạy *function* với các đối số *args* và các đối số từ khóa *kwargs* sau khi *interval* giây đã trôi qua. Nếu *args* là ``None`` (giá trị mặc định) thì một danh sách rỗng sẽ được sử dụng. Nếu *kwargs* là ``None`` (giá trị mặc định) thì một dict rỗng sẽ được sử dụng.

   .. versionchanged:: 3.3
      được thay đổi từ một factory function thành một class.

   .. method:: cancel()

      Dừng timer và hủy việc thực thi action của timer. Thao tác này chỉ có hiệu lực nếu timer vẫn đang ở giai đoạn chờ.


Đối tượng Barrier
^^^^^^^^^^^^^^^^^

.. versionadded:: 3.2

Class này cung cấp một primitive đồng bộ hóa đơn giản để một số lượng thread cố định có thể chờ lẫn nhau. Mỗi thread cố gắng vượt qua barrier bằng cách gọi phương thức :meth:`~Barrier.wait` và sẽ bị chặn cho đến khi tất cả thread đã thực hiện các lần gọi :meth:`~Barrier.wait`. Tại thời điểm này, các thread được giải phóng đồng thời.

Có thể tái sử dụng barrier nhiều lần với cùng số lượng thread.

Ví dụ, sau đây là một cách đơn giản để đồng bộ hóa một thread client và một thread server::

   b = Barrier(2, timeout=5)

   def server():
       start_server()
       b.wait()
       while True:
           connection = accept_connection()
           process_server_connection(connection)

   def client():
       b.wait()
       while True:
           connection = make_connection()
           process_client_connection(connection)


.. class:: Barrier(parties, action=None, timeout=None)

   Tạo một đối tượng barrier cho *parties* thread. Một *action*, nếu được cung cấp, là một callable được một trong các thread gọi khi chúng được giải phóng. *timeout* là giá trị timeout mặc định nếu không được chỉ định cho phương thức :meth:`wait`.

   .. method:: wait(timeout=None)

      Vượt qua barrier. Khi tất cả các thread tham gia barrier đã gọi hàm này, tất cả sẽ được giải phóng đồng thời. Nếu cung cấp *timeout*, giá trị này sẽ được ưu tiên sử dụng thay cho giá trị đã cung cấp cho hàm khởi tạo của lớp.

      Giá trị trả về là một số nguyên trong phạm vi từ 0 đến *parties* -- 1, và khác nhau đối với mỗi thread. Có thể dùng giá trị này để chọn một thread thực hiện một số công việc dọn dẹp đặc biệt, chẳng hạn như::

         i = barrier.wait()
         if i == 0:
             # Chỉ một thread cần in dòng này
             print("passed the barrier")

      Nếu đã cung cấp *action* cho hàm khởi tạo, một trong các thread sẽ gọi nó trước khi được giải phóng. Nếu lời gọi này gây ra lỗi, barrier sẽ chuyển sang trạng thái bị hỏng.

      Nếu lời gọi bị hết thời gian chờ, barrier sẽ chuyển sang trạng thái bị hỏng.

      Phương thức này có thể gây ra :class:`BrokenBarrierError` exception nếu barrier bị hỏng hoặc được đặt lại trong khi một thread đang chờ.

   .. method:: reset()

      Đưa barrier về trạng thái mặc định, trống. Mọi thread đang chờ trên đó sẽ nhận được :class:`BrokenBarrierError` exception.

      Lưu ý rằng việc sử dụng hàm này có thể yêu cầu một số cơ chế đồng bộ hóa bên ngoài nếu còn các thread khác có trạng thái không xác định. Nếu một barrier bị hỏng, tốt hơn hết là để nguyên barrier đó và tạo một barrier mới.

   .. method:: abort()

      Đưa barrier vào trạng thái bị hỏng. Điều này khiến mọi lệnh gọi đang hoạt động hoặc trong tương lai đến :meth:`wait` không thành công với :class:`BrokenBarrierError`. Ví dụ, hãy sử dụng cách này nếu một trong các thread cần hủy bỏ, để tránh làm ứng dụng bị deadlock.

      Có thể tốt hơn nếu chỉ cần tạo barrier với giá trị *timeout* hợp lý để tự động đề phòng trường hợp một trong các thread gặp sự cố.

   .. attribute:: parties

      Số thread cần thiết để vượt qua barrier.

   .. attribute:: n_waiting

      Số thread hiện đang chờ tại barrier.

   .. attribute:: broken

      Một giá trị boolean là ``True`` nếu barrier đang ở trạng thái bị hỏng.


.. exception:: BrokenBarrierError

   Ngoại lệ này, là một lớp con của :exc:`RuntimeError`, được phát sinh khi
   Đối tượng :class:`Barrier` bị đặt lại hoặc bị hỏng.


.. _with-locks:

Sử dụng lock, condition và semaphore trong câu lệnh :keyword:`!with`
--------------------------------------------------------------------

Tất cả các đối tượng do module này cung cấp có các phương thức ``acquire`` và ``release`` đều có thể được sử dụng làm trình quản lý ngữ cảnh cho câu lệnh :keyword:`with`. Phương thức ``acquire`` sẽ được gọi khi khối được bắt đầu, còn ``release`` sẽ được gọi khi khối kết thúc. Do đó, đoạn mã sau đây::

   with some_lock:
       # thực hiện việc gì đó...

tương đương với::

   some_lock.acquire()
   try:
       # thực hiện việc gì đó...
   finally:
       some_lock.release()

Hiện tại, :class:`Lock`, :class:`RLock`, :class:`Condition`,
Các đối tượng :class:`Semaphore` và :class:`BoundedSemaphore` có thể được sử dụng làm
trình quản lý ngữ cảnh của câu lệnh :keyword:`with`.

.. _`threads`: https://en.wikipedia.org/wiki/Thread_(computing)
