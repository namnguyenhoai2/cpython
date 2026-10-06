:mod:`!concurrent.futures` --- Khởi chạy các tác vụ song song
=============================================================

.. module:: concurrent.futures
   :synopsis: Thực thi các phép tính đồng thời bằng thread hoặc process.

.. versionadded:: 3.2

**Mã nguồn:** :source:`Lib/concurrent/futures/thread.py`,
:source:`Lib/concurrent/futures/process.py`, và :source:`Lib/concurrent/futures/interpreter.py`

--------------

Mô-đun :mod:`!concurrent.futures` cung cấp một giao diện cấp cao để thực thi các đối tượng callable một cách bất đồng bộ.

Việc thực thi bất đồng bộ có thể được thực hiện bằng thread, sử dụng
:class:`ThreadPoolExecutor` hoặc :class:`InterpreterPoolExecutor`, hoặc bằng các process riêng biệt, sử dụng :class:`ProcessPoolExecutor`. Mỗi lớp đều triển khai cùng một interface, được định nghĩa bởi lớp trừu tượng :class:`Executor`.

:class:`concurrent.futures.Future` không được nhầm lẫn với
:class:`asyncio.Future`, được thiết kế để sử dụng với các task và coroutine :mod:`asyncio`. Xem tài liệu :doc:`asyncio's Future <asyncio-future>` để so sánh chi tiết hai đối tượng này.

.. include:: ../includes/wasm-notavail.rst

Các đối tượng Executor
----------------------

.. class:: Executor

   Một lớp trừu tượng cung cấp các phương thức để thực thi các lời gọi một cách bất đồng bộ. Không nên sử dụng trực tiếp lớp này mà nên sử dụng thông qua các lớp con cụ thể của nó.

   .. method:: submit(fn, /, *args, **kwargs)

      Lên lịch cho callable, *fn*, để thực thi ``fn(*args, **kwargs)`` và trả về một :class:`Future` object đại diện cho việc thực thi callable.::

         with ThreadPoolExecutor(max_workers=1) as executor:
             future = executor.submit(pow, 323, 1235)
             print(future.result())

   .. method:: map(fn, *iterables, timeout=None, chunksize=1, buffersize=None)

      Tương tự như :func:`map(fn, *iterables) <map>` ngoại trừ:

      * Các *iterables* được thu thập ngay lập tức thay vì một cách lazy, trừ khi chỉ định *buffersize* để giới hạn số task đã gửi mà kết quả vẫn chưa được yield. Nếu bộ đệm đầy, việc lặp qua các *iterables* sẽ tạm dừng cho đến khi một kết quả được yield từ bộ đệm.

      * *fn* được thực thi bất đồng bộ và có thể thực hiện đồng thời nhiều lệnh gọi đến *fn*.

      Iterator được trả về sẽ phát sinh :exc:`TimeoutError` nếu :meth:`~iterator.__next__` được gọi và kết quả chưa có sau *timeout* giây kể từ lệnh gọi ban đầu đến :meth:`Executor.map`. *timeout* có thể là số nguyên hoặc số thực. Nếu *timeout* không được chỉ định hoặc là ``None``, thời gian chờ là không giới hạn.

      Nếu lệnh gọi *fn* phát sinh ngoại lệ, ngoại lệ đó sẽ được phát sinh khi giá trị của lệnh gọi được lấy từ iterator.

      Khi sử dụng :class:`ProcessPoolExecutor`, phương thức này chia *iterables* thành một số chunk rồi gửi chúng đến pool dưới dạng các task riêng biệt. Có thể chỉ định kích thước (xấp xỉ) của các chunk này bằng cách đặt *chunksize* thành một số nguyên dương. Đối với các iterable rất dài, việc sử dụng giá trị lớn cho *chunksize* có thể cải thiện đáng kể hiệu suất so với kích thước mặc định là 1. Với
      :class:`ThreadPoolExecutor` và :class:`InterpreterPoolExecutor`, *chunksize* không có tác dụng.

      .. versionchanged:: 3.5
         Đã thêm tham số *chunksize*.

      .. versionchanged:: 3.14
         Đã thêm tham số *buffersize*.

   .. method:: shutdown(wait=True, *, cancel_futures=False)

      Báo cho executor rằng nó nên giải phóng mọi tài nguyên đang sử dụng khi các future đang chờ hiện tại hoàn tất việc thực thi. Các lệnh gọi đến
      :meth:`Executor.submit` và :meth:`Executor.map` được thực hiện sau khi shutdown sẽ gây ra :exc:`RuntimeError`.

      Nếu *wait* là ``True`` thì phương thức này sẽ không trả về cho đến khi tất cả future đang chờ hoàn tất việc thực thi và các tài nguyên liên kết với executor được giải phóng. Nếu *wait* là ``False`` thì phương thức này sẽ trả về ngay lập tức và các tài nguyên liên kết với executor sẽ được giải phóng khi tất cả future đang chờ hoàn tất việc thực thi. Bất kể giá trị của *wait* là gì, toàn bộ chương trình Python sẽ không thoát cho đến khi tất cả future đang chờ hoàn tất việc thực thi.

      Nếu *cancel_futures* là ``True``, phương thức này sẽ hủy tất cả future đang chờ mà executor chưa bắt đầu chạy. Mọi future đã hoàn tất hoặc đang chạy sẽ không bị hủy, bất kể giá trị của *cancel_futures* là gì.

      Nếu cả *cancel_futures* và *wait* đều là ``True``, tất cả future mà executor đã bắt đầu chạy sẽ hoàn tất trước khi phương thức này trả về. Các future còn lại sẽ bị hủy.

      Bạn có thể tránh phải gọi phương thức này một cách rõ ràng nếu sử dụng executor như một :term:`context manager` thông qua câu lệnh :keyword:`with`, câu lệnh này sẽ shutdown :class:`Executor` (chờ như thể :meth:`Executor.shutdown` được gọi với *wait* được đặt thành ``True``)::

         import shutil
         with ThreadPoolExecutor(max_workers=4) as e:
             e.submit(shutil.copy, 'src1.txt', 'dest1.txt')
             e.submit(shutil.copy, 'src2.txt', 'dest2.txt')
             e.submit(shutil.copy, 'src3.txt', 'dest3.txt')
             e.submit(shutil.copy, 'src4.txt', 'dest4.txt')

      .. versionchanged:: 3.9
         Đã thêm *cancel_futures*.


ThreadPoolExecutor
------------------

:class:`ThreadPoolExecutor` là một lớp con của :class:`Executor`, sử dụng một nhóm thread để thực thi các lệnh gọi một cách bất đồng bộ.

Có thể xảy ra deadlock khi callable liên kết với :class:`Future` chờ kết quả của một :class:`Future` khác. Ví dụ:::

   import time
   def wait_on_b():
       time.sleep(5)
       print(b.result())  # b sẽ không bao giờ hoàn tất vì đang chờ a.
       return 5

   def wait_on_a():
       time.sleep(5)
       print(a.result())  # a sẽ không bao giờ hoàn tất vì đang chờ b.
       return 6


   executor = ThreadPoolExecutor(max_workers=2)
   a = executor.submit(wait_on_b)
   b = executor.submit(wait_on_a)

Và::

   def wait_on_future():
       f = executor.submit(pow, 5, 2)
       # Sẽ không bao giờ hoàn tất vì chỉ có một worker thread và
       # nó đang thực thi hàm này.
       print(f.result())

   executor = ThreadPoolExecutor(max_workers=1)
   future = executor.submit(wait_on_future)
   # Lưu ý: gọi future.result() cũng sẽ gây ra deadlock vì
   # luồng worker duy nhất đã đang chờ wait_on_future().


.. class:: ThreadPoolExecutor(max_workers=None, thread_name_prefix='', initializer=None, initargs=())

   Một lớp con của :class:`Executor` sử dụng pool gồm tối đa *max_workers* luồng để thực thi các lời gọi một cách bất đồng bộ.

   Tất cả các luồng được đưa vào hàng đợi của ``ThreadPoolExecutor`` sẽ được join trước khi interpreter có thể thoát. Lưu ý rằng exit handler thực hiện việc này được thực thi *trước* bất kỳ exit handler nào được thêm bằng ``atexit``. Điều này có nghĩa là các exception trong luồng chính phải được bắt và xử lý để báo hiệu cho các luồng thoát một cách an toàn. Vì lý do này, bạn không nên sử dụng ``ThreadPoolExecutor`` cho các tác vụ chạy lâu.

   *initializer* là một callable tùy chọn được gọi khi bắt đầu mỗi luồng worker; *initargs* là một tuple các đối số được truyền cho initializer. Nếu *initializer* gây ra exception, tất cả các job hiện đang chờ sẽ gây ra :exc:`~concurrent.futures.thread.BrokenThreadPool`, cũng như mọi nỗ lực submit thêm job vào pool.

   .. versionchanged:: 3.5
      Nếu *max_workers* là ``None`` hoặc không được cung cấp, giá trị mặc định sẽ là số processor trên máy nhân với ``5``, với giả định rằng :class:`ThreadPoolExecutor` thường được dùng để chồng lấp các thao tác I/O thay vì công việc CPU và số worker nên lớn hơn số worker của :class:`ProcessPoolExecutor`.

   .. versionchanged:: 3.6
      Đã thêm tham số *thread_name_prefix* để cho phép người dùng kiểm soát :class:`threading.Thread` tên của các worker thread do pool tạo ra, giúp việc debug dễ dàng hơn.

   .. versionchanged:: 3.7
      Đã thêm các đối số *initializer* và *initargs*.

   .. versionchanged:: 3.8
      Giá trị mặc định của *max_workers* được thay đổi thành ``min(32, os.cpu_count() + 4)``. Giá trị mặc định này duy trì ít nhất 5 worker cho các tác vụ bị giới hạn bởi I/O. Giá trị này sử dụng nhiều nhất 32 lõi CPU cho các tác vụ bị giới hạn bởi CPU có giải phóng GIL. Đồng thời, nó tránh ngầm sử dụng lượng tài nguyên rất lớn trên các máy có nhiều lõi.

      ThreadPoolExecutor giờ đây cũng tái sử dụng các worker thread đang rảnh trước khi khởi chạy *max_workers* worker thread.

   .. versionchanged:: 3.13
      Giá trị mặc định của *max_workers* được thay đổi thành ``min(32, (os.process_cpu_count() or 1) + 4)``.


.. _threadpoolexecutor-example:

Ví dụ về ThreadPoolExecutor
~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

   import concurrent.futures
   import urllib.request

   URLS = ['http://www.foxnews.com/',
           'http://www.cnn.com/',
           'http://europe.wsj.com/',
           'http://www.bbc.co.uk/',
           'http://nonexistent-subdomain.python.org/']

   # Retrieve a single page and report the URL and contents
   def load_url(url, timeout):
       with urllib.request.urlopen(url, timeout=timeout) as conn:
           return conn.read()

   # We can use a with statement to ensure threads are cleaned up promptly
   with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
       # Start the load operations and mark each future with its URL
       future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
       for future in concurrent.futures.as_completed(future_to_url):
           url = future_to_url[future]
           try:
               data = future.result()
           except Exception as exc:
               print('%r generated an exception: %s' % (url, exc))
           else:
               print('%r page is %d bytes' % (url, len(data)))


InterpreterPoolExecutor
-----------------------

.. versionadded:: 3.14

Lớp :class:`InterpreterPoolExecutor` sử dụng một pool các interpreter để thực thi các lệnh gọi một cách bất đồng bộ. Đây là một subclass của :class:`ThreadPoolExecutor`, nghĩa là mỗi worker chạy trong thread riêng. Điểm khác biệt ở đây là mỗi worker có interpreter riêng và thực thi từng task bằng interpreter đó.

Lợi ích lớn nhất của việc sử dụng interpreter thay vì chỉ dùng thread là khả năng parallelism thực sự trên nhiều core CPU. Mỗi interpreter có riêng
:term:`Global Interpreter Lock <global interpreter lock>`, vì vậy mã chạy trong một trình thông dịch có thể chạy trên một lõi CPU, trong khi mã trong một trình thông dịch khác chạy không bị chặn trên một lõi khác.

Đánh đổi là việc viết code concurrent để sử dụng với nhiều interpreter có thể đòi hỏi thêm công sức. Tuy nhiên, đó là vì cách này buộc bạn phải cân nhắc kỹ cách thức và thời điểm các interpreter tương tác với nhau, đồng thời phải nêu rõ dữ liệu nào được chia sẻ giữa các interpreter. Điều này mang lại một số lợi ích giúp cân bằng công sức bỏ ra, trong đó có parallelism thực sự trên nhiều core CPU. Ví dụ, code được viết theo cách này có thể giúp bạn dễ suy luận hơn về concurrency. Một lợi ích lớn khác là bạn không phải xử lý một số vấn đề khó chịu lớn khi sử dụng thread, chẳng hạn như race condition.

Interpreter của mỗi worker được cô lập khỏi tất cả interpreter khác. "Cô lập" có nghĩa là mỗi interpreter có runtime state riêng và hoạt động hoàn toàn độc lập. Ví dụ, nếu bạn chuyển hướng
:data:`sys.stdout` trong một interpreter, nó sẽ không tự động được chuyển hướng sang bất kỳ interpreter nào khác. Nếu bạn import một module trong một interpreter, module đó sẽ không tự động được import trong bất kỳ interpreter nào khác. Bạn sẽ cần import module riêng trong interpreter nơi bạn cần sử dụng nó. Trên thực tế, mỗi module được import trong một interpreter là một object hoàn toàn riêng biệt với cùng module đó trong một interpreter khác, bao gồm cả :mod:`sys`, :mod:`builtins` và thậm chí ``__main__``.

Việc cô lập có nghĩa là một mutable object hoặc dữ liệu khác không thể được nhiều interpreter sử dụng cùng lúc. Điều đó đồng nghĩa với việc các interpreter thực sự không thể chia sẻ những object hoặc dữ liệu như vậy. Thay vào đó, mỗi interpreter phải có bản sao riêng và bạn sẽ phải đồng bộ thủ công mọi thay đổi giữa các bản sao. Các object và dữ liệu immutable, chẳng hạn như các singleton dựng sẵn, string và tuple chứa các immutable object, không bị những hạn chế này.

Việc giao tiếp và đồng bộ hóa giữa các interpreter được thực hiện hiệu quả nhất bằng các công cụ chuyên dụng, chẳng hạn như những công cụ được đề xuất trong :pep:`734`. Một phương án kém hiệu quả hơn là serialize bằng :mod:`pickle` rồi gửi các byte qua một :mod:`socket <socket>` dùng chung hoặc
:func:`pipe <os.pipe>`.

.. class:: InterpreterPoolExecutor(max_workers=None, thread_name_prefix='', initializer=None, initargs=())

   Một lớp con của :class:`ThreadPoolExecutor` thực thi các lệnh gọi một cách bất đồng bộ bằng cách sử dụng một pool gồm nhiều nhất *max_workers* thread. Mỗi thread chạy các tác vụ trong interpreter riêng của nó. Các interpreter worker được cô lập với nhau, nghĩa là mỗi interpreter có trạng thái runtime riêng và chúng không thể chia sẻ bất kỳ đối tượng mutable hoặc dữ liệu nào khác. Mỗi interpreter có :term:`Global Interpreter Lock <global interpreter lock>` riêng, nghĩa là code chạy với executor này có khả năng song song thực sự trên nhiều core.

   Các đối số tùy chọn *initializer* và *initargs* có cùng ý nghĩa như trong :class:`!ThreadPoolExecutor`: initializer được chạy khi mỗi worker được tạo, nhưng trong trường hợp này, nó được chạy trong interpreter của worker. Executor serialize *initializer* và *initargs* bằng :mod:`pickle` khi gửi chúng đến interpreter của worker.

   .. note::
      Executor có thể thay thế các exception không được bắt từ *initializer* bằng :class:`~concurrent.interpreters.ExecutionFailed`.

   Các lưu ý khác từ lớp cha :class:`ThreadPoolExecutor` cũng áp dụng ở đây.

:meth:`~Executor.submit` và :meth:`~Executor.map` hoạt động như bình thường, ngoại trừ việc worker serialize callable và các đối số bằng
:mod:`pickle` khi gửi chúng đến interpreter của nó. Worker cũng serialize giá trị trả về khi gửi giá trị đó trở lại.

Khi tác vụ hiện tại của một worker phát sinh ngoại lệ không được bắt, worker luôn cố gắng giữ nguyên ngoại lệ đó. Nếu thành công thì worker cũng đặt ``__cause__`` thành một
instance :class:`~concurrent.interpreters.ExecutionFailed` tương ứng, chứa phần tóm tắt về ngoại lệ ban đầu. Trong trường hợp hiếm gặp khi worker không thể giữ nguyên ngoại lệ ban đầu thì worker sẽ trực tiếp giữ lại
instance :class:`~concurrent.interpreters.ExecutionFailed` tương ứng.


ProcessPoolExecutor
-------------------

Lớp :class:`ProcessPoolExecutor` là một lớp con của :class:`Executor`, sử dụng một pool các process để thực thi các lời gọi một cách bất đồng bộ.
:class:`ProcessPoolExecutor` sử dụng module :mod:`multiprocessing`, cho phép nó tránh :term:`Global Interpreter Lock <global interpreter lock>`, nhưng cũng có nghĩa là chỉ những object có thể pickle mới có thể được thực thi và trả về.

Module ``__main__`` phải có thể được các subprocess của worker import. Điều này có nghĩa là :class:`ProcessPoolExecutor` sẽ không hoạt động trong trình thông dịch tương tác.

Việc gọi các phương thức :class:`Executor` hoặc :class:`Future` từ một callable được gửi đến :class:`ProcessPoolExecutor` sẽ dẫn đến deadlock.

Lưu ý rằng các hạn chế đối với những hàm và đối số cần có khả năng picklable theo :class:`multiprocessing.Process` cũng được áp dụng khi sử dụng :meth:`~Executor.submit` và :meth:`~Executor.map` trên một :class:`ProcessPoolExecutor`. Không nên kỳ vọng một hàm được định nghĩa trong REPL hoặc một lambda sẽ hoạt động.

.. class:: ProcessPoolExecutor(max_workers=None, mp_context=None, initializer=None, initargs=(), max_tasks_per_child=None)

   Một lớp con của :class:`Executor` thực thi các lệnh gọi một cách bất đồng bộ bằng cách sử dụng một pool gồm tối đa *max_workers* process. Nếu *max_workers* là ``None`` hoặc không được cung cấp, giá trị mặc định sẽ là :func:`os.process_cpu_count`. Nếu *max_workers* nhỏ hơn hoặc bằng ``0``, một :exc:`ValueError` sẽ được raise. Trên Windows, *max_workers* phải nhỏ hơn hoặc bằng ``61``. Nếu không, :exc:`ValueError` sẽ được raise. Nếu *max_workers* là ``None``, giá trị mặc định được chọn sẽ nhiều nhất là ``61``, ngay cả khi có nhiều processor hơn. *mp_context* có thể là một context :mod:`multiprocessing` hoặc ``None``. Context này sẽ được dùng để khởi chạy các worker. Nếu *mp_context* là ``None`` hoặc không được cung cấp, context :mod:`multiprocessing` mặc định sẽ được sử dụng. Xem :ref:`multiprocessing-start-methods`.

   *initializer* là một callable tùy chọn được gọi khi bắt đầu mỗi worker process; *initargs* là một tuple các đối số được truyền cho initializer. Nếu *initializer* raise một exception, tất cả các job đang chờ sẽ raise một :exc:`~concurrent.futures.process.BrokenProcessPool`, cũng như mọi nỗ lực gửi thêm job đến pool.

   *max_tasks_per_child* là một đối số tùy chọn chỉ định số task tối đa mà một process có thể thực thi trước khi thoát và được thay thế bằng một worker process mới. Theo mặc định, *max_tasks_per_child* là ``None``, nghĩa là các worker process sẽ tồn tại trong suốt vòng đời của pool. Khi chỉ định một giá trị tối đa, phương thức khởi động multiprocessing "spawn" sẽ được sử dụng theo mặc định nếu không có tham số *mp_context*. Tính năng này không tương thích với phương thức khởi động "fork".

   .. versionchanged:: 3.3
      Khi một trong các worker process kết thúc đột ngột, một
      :exc:`~concurrent.futures.process.BrokenProcessPool` error hiện được raise. Trước đây, hành vi không được xác định, nhưng các thao tác trên executor hoặc các future của nó thường bị treo hoặc rơi vào deadlock.

   .. versionchanged:: 3.7
      Đối số *mp_context* được thêm vào để cho phép người dùng kiểm soát start_method cho các worker process được pool tạo ra.

      Đã thêm các đối số *initializer* và *initargs*.

   .. versionchanged:: 3.11
      Đối số *max_tasks_per_child* được thêm vào để cho phép người dùng kiểm soát vòng đời của các worker trong pool.

   .. versionchanged:: 3.12
      Trên các hệ thống POSIX, nếu ứng dụng của bạn có nhiều thread và
      :mod:`multiprocessing` context sử dụng ``"fork"`` start method: Hàm :func:`os.fork` được gọi nội bộ để tạo worker có thể phát sinh một
      :exc:`DeprecationWarning`. Truyền một *mp_context* được cấu hình để sử dụng một start method khác. Xem tài liệu :func:`os.fork` để biết thêm giải thích.

   .. versionchanged:: 3.13
      *max_workers* sử dụng :func:`os.process_cpu_count` theo mặc định, thay vì
      :func:`os.cpu_count`.

   .. versionchanged:: 3.14
      Phương thức khởi động tiến trình mặc định (xem
      :ref:`multiprocessing-start-methods`) đã được thay đổi, không còn là *fork*. Nếu bạn yêu cầu phương thức khởi động *fork* cho :class:`ProcessPoolExecutor`, bạn phải truyền rõ ràng ``mp_context=multiprocessing.get_context("fork")``.

   .. versionchanged:: 3.14.7
      Đã khắc phục tình trạng deadlock (:gh:`115634`) khiến executor có thể bị treo sau khi một worker process thoát khi đạt đến giới hạn *max_tasks_per_child* trong lúc vẫn còn các tác vụ đang chờ trong hàng đợi.

   .. method:: terminate_workers()

      Cố gắng chấm dứt ngay lập tức tất cả worker process đang hoạt động bằng cách gọi
      :meth:`Process.terminate <multiprocessing.Process.terminate>` trên mỗi process. Trong nội bộ, phương thức này cũng sẽ gọi :meth:`Executor.shutdown` để đảm bảo tất cả tài nguyên khác liên kết với executor được giải phóng.

      Sau khi gọi phương thức này, caller không nên gửi thêm tác vụ đến executor.

      .. versionadded:: 3.14

   .. method:: kill_workers()

      Cố gắng hủy ngay lập tức tất cả worker process đang hoạt động bằng cách gọi
      :meth:`Process.kill <multiprocessing.Process.kill>` trên từng đối tượng đó. Về nội bộ, nó cũng sẽ gọi :meth:`Executor.shutdown` để đảm bảo rằng tất cả các tài nguyên khác liên kết với executor đều được giải phóng.

      Sau khi gọi phương thức này, caller không nên gửi thêm tác vụ đến executor.

      .. versionadded:: 3.14

.. _processpoolexecutor-example:

Ví dụ về ProcessPoolExecutor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

   import concurrent.futures
   import math

   PRIMES = [
       112272535095293,
       112582705942171,
       112272535095293,
       115280095190773,
       115797848077099,
       1099726899285419]

   def is_prime(n):
       if n < 2:
           return False
       if n == 2:
           return True
       if n % 2 == 0:
           return False

       sqrt_n = int(math.floor(math.sqrt(n)))
       for i in range(3, sqrt_n + 1, 2):
           if n % i == 0:
               return False
       return True

   def main():
       with concurrent.futures.ProcessPoolExecutor() as executor:
           for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
               print('%d is prime: %s' % (number, prime))

   if __name__ == '__main__':
       main()


Đối tượng Future
----------------

Lớp :class:`Future` đóng gói việc thực thi bất đồng bộ của một callable.
Các instance :class:`Future` được tạo bởi :meth:`Executor.submit`.

.. class:: Future

   Đóng gói việc thực thi bất đồng bộ của một callable. Các instance :class:`Future` được tạo bởi :meth:`Executor.submit` và không nên được tạo trực tiếp, ngoại trừ mục đích kiểm thử.

   .. method:: cancel()

      Cố gắng hủy lệnh gọi. Nếu lệnh gọi hiện đang được thực thi hoặc đã chạy xong và không thể bị hủy, phương thức sẽ trả về ``False``; nếu không, lệnh gọi sẽ bị hủy và phương thức sẽ trả về ``True``.

   .. method:: cancelled()

      Trả về ``True`` nếu lệnh gọi đã được hủy thành công.

   .. method:: running()

      Trả về ``True`` nếu lệnh gọi hiện đang được thực thi và không thể bị hủy.

   .. method:: done()

      Trả về ``True`` nếu lệnh gọi đã được hủy thành công hoặc đã chạy xong.

   .. method:: result(timeout=None)

      Trả về giá trị do lệnh gọi trả về. Nếu lệnh gọi chưa hoàn tất, phương thức này sẽ chờ tối đa *timeout* giây. Nếu lệnh gọi chưa hoàn tất trong *timeout* giây thì một
      :exc:`TimeoutError` sẽ được phát sinh. *timeout* có thể là int hoặc float. Nếu *timeout* không được chỉ định hoặc là ``None``, thì thời gian chờ là không giới hạn.

      Nếu future bị hủy trước khi hoàn tất thì :exc:`.CancelledError` sẽ được phát sinh.

      Nếu lời gọi phát sinh một ngoại lệ, phương thức này sẽ phát sinh chính ngoại lệ đó.

   .. method:: exception(timeout=None)

      Trả về ngoại lệ do lời gọi phát sinh. Nếu lời gọi chưa hoàn tất, phương thức này sẽ chờ tối đa *timeout* giây. Nếu lời gọi chưa hoàn tất trong *timeout* giây, thì một
      :exc:`TimeoutError` sẽ được phát sinh. *timeout* có thể là một số nguyên hoặc số thực. Nếu *timeout* không được chỉ định hoặc là ``None``, thời gian chờ là không giới hạn.

      Nếu future bị hủy trước khi hoàn tất thì :exc:`.CancelledError` sẽ được phát sinh.

      Nếu lời gọi hoàn tất mà không phát sinh ngoại lệ, ``None`` sẽ được trả về.

   .. method:: add_done_callback(fn)

      Gắn callable *fn* vào future. *fn* sẽ được gọi với future là đối số duy nhất khi future bị hủy hoặc hoàn tất chạy.

      Các callable được thêm vào sẽ được gọi theo thứ tự thêm vào và luôn được gọi trong một thread thuộc về process đã thêm chúng. Nếu callable phát sinh một lớp con của :exc:`Exception`, lỗi đó sẽ được ghi vào log và bỏ qua. Nếu callable phát sinh một lớp con của :exc:`BaseException`, hành vi sẽ không được xác định.

      Nếu future đã hoàn tất hoặc bị hủy, *fn* sẽ được gọi ngay lập tức.

   Các :class:`Future` phương thức sau đây предназначены cho việc sử dụng trong unit test và
   các :class:`Executor` triển khai.

   .. method:: set_running_or_notify_cancel()

      Phương thức này chỉ nên được gọi bởi các :class:`Executor` triển khai trước khi thực thi công việc liên kết với :class:`Future` và bởi các unit test.

      Nếu phương thức trả về ``False`` thì :class:`Future` đã bị hủy, tức là :meth:`Future.cancel` đã được gọi và trả về ``True``. Mọi thread đang chờ :class:`Future` hoàn tất (tức là thông qua
      :func:`as_completed` hoặc :func:`wait`) sẽ được đánh thức.

      Nếu phương thức trả về ``True`` thì :class:`Future` chưa bị hủy và đã được chuyển sang trạng thái đang chạy, tức là các lệnh gọi đến
      :meth:`Future.running` sẽ trả về ``True``.

      Phương thức này chỉ có thể được gọi một lần và không thể được gọi sau
      khi :meth:`Future.set_result` hoặc :meth:`Future.set_exception` đã được gọi.

   .. method:: set_result(result)

      Đặt kết quả của công việc liên kết với :class:`Future` thành *result*.

      Phương thức này chỉ nên được sử dụng bởi các triển khai :class:`Executor` và các bài kiểm thử đơn vị.

      .. versionchanged:: 3.8
         Phương thức này phát sinh
         :exc:`concurrent.futures.InvalidStateError` nếu :class:`Future` đã hoàn tất.

   .. method:: set_exception(exception)

      Đặt kết quả của công việc liên kết với :class:`Future` thành
      :class:`Exception` *ngoại lệ*.

      Phương thức này chỉ nên được sử dụng bởi các triển khai :class:`Executor` và các bài kiểm thử đơn vị.

      .. versionchanged:: 3.8
         Phương thức này phát sinh
         :exc:`concurrent.futures.InvalidStateError` nếu :class:`Future` đã hoàn tất.

Các hàm của mô-đun
------------------

.. function:: wait(fs, timeout=None, return_when=ALL_COMPLETED)

   Chờ các instance :class:`Future` (có thể được tạo bởi các
   các instance :class:`Executor` được cung cấp cho *fs* để hoàn tất. Các future trùng lặp được cung cấp cho *fs* sẽ bị loại bỏ và chỉ được trả về một lần. Trả về một named 2-tuple gồm các tập hợp. Tập hợp đầu tiên, có tên là ``done``, chứa các future đã hoàn tất (future đã kết thúc hoặc bị hủy) trước khi quá trình chờ hoàn tất. Tập hợp thứ hai, có tên là ``not_done``, chứa các future chưa hoàn tất (future đang chờ hoặc đang chạy).

   *timeout* có thể được dùng để kiểm soát số giây tối đa cần chờ trước khi trả về. *timeout* có thể là int hoặc float. Nếu *timeout* không được chỉ định hoặc là ``None``, thời gian chờ sẽ không bị giới hạn.

   *return_when* cho biết khi nào hàm này sẽ trả về. Giá trị này phải là một trong các hằng số sau:

   .. list-table::
      :header-rows: 1

      * - Hằng số
        - Mô tả

      * - .. data:: FIRST_COMPLETED
        - Hàm sẽ trả về khi bất kỳ future nào hoàn tất hoặc bị hủy.

      * - .. data:: FIRST_EXCEPTION
        - Hàm sẽ trả về khi bất kỳ future nào hoàn tất bằng cách phát sinh một ngoại lệ. Nếu không có future nào phát sinh ngoại lệ thì tương đương với :const:`ALL_COMPLETED`.

      * - .. data:: ALL_COMPLETED
        - Hàm sẽ trả về khi tất cả future hoàn tất hoặc bị hủy.

.. function:: as_completed(fs, timeout=None)

   Trả về một iterator trên các instance :class:`Future` (có thể được tạo bởi các instance :class:`Executor` khác nhau) được cung cấp bởi *fs*, iterator này trả về các future khi chúng hoàn tất (các future đã hoàn tất hoặc bị hủy). Mọi future trùng lặp được cung cấp bởi *fs* sẽ chỉ được trả về một lần. Mọi future đã hoàn tất trước
   :func:`as_completed` được gọi sẽ được yield trước. Iterator được trả về sẽ phát sinh một :exc:`TimeoutError` nếu :meth:`~iterator.__next__` được gọi và kết quả chưa khả dụng sau *timeout* giây kể từ lần gọi :func:`as_completed` ban đầu. *timeout* có thể là int hoặc float. Nếu *timeout* không được chỉ định hoặc là ``None``, thời gian chờ là không giới hạn.


.. seealso::

   :pep:`3148` -- futures - thực thi các phép tính không đồng bộ
      Đề xuất mô tả tính năng này để đưa vào thư viện chuẩn Python.


Các lớp ngoại lệ
----------------

.. currentmodule:: concurrent.futures

.. exception:: CancelledError

   Được phát sinh khi một future bị hủy.

.. exception:: TimeoutError

   Một bí danh đã lỗi thời của :exc:`TimeoutError`, được phát sinh khi một thao tác future vượt quá thời gian chờ đã cho.

   .. versionchanged:: 3.11

      Lớp này đã trở thành bí danh của :exc:`TimeoutError`.


.. exception:: BrokenExecutor

   Được dẫn xuất từ :exc:`RuntimeError`, lớp ngoại lệ này được phát sinh khi một executor bị hỏng vì một lý do nào đó và không thể được sử dụng để gửi hoặc thực thi các tác vụ mới.

   .. versionadded:: 3.7

.. exception:: InvalidStateError

   Được phát sinh khi một thao tác được thực hiện trên một future không được phép ở trạng thái hiện tại.

   .. versionadded:: 3.8

.. currentmodule:: concurrent.futures.thread

.. exception:: BrokenThreadPool

   Được dẫn xuất từ :exc:`~concurrent.futures.BrokenExecutor`, lớp ngoại lệ này được phát sinh khi một trong các worker của :class:`~concurrent.futures.ThreadPoolExecutor` không khởi tạo được.

   .. versionadded:: 3.7

.. currentmodule:: concurrent.futures.interpreter

.. exception:: BrokenInterpreterPool

   Được dẫn xuất từ :exc:`~concurrent.futures.thread.BrokenThreadPool`, lớp ngoại lệ này được phát sinh khi một trong các worker của :class:`~concurrent.futures.InterpreterPoolExecutor` không khởi tạo được.

   .. versionadded:: 3.14

.. currentmodule:: concurrent.futures.process

.. exception:: BrokenProcessPool

   Được dẫn xuất từ :exc:`~concurrent.futures.BrokenExecutor` (trước đây
   :exc:`RuntimeError`), lớp ngoại lệ này được phát sinh khi một trong các worker của :class:`~concurrent.futures.ProcessPoolExecutor` đã kết thúc theo cách không sạch sẽ (ví dụ: bị kill từ bên ngoài).

   .. versionadded:: 3.3
