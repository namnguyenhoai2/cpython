:mod:`!multiprocessing` --- Tính song song dựa trên tiến trình
==============================================================

.. module:: multiprocessing
   :synopsis: Tính song song dựa trên tiến trình.

**Mã nguồn:** :source:`Lib/multiprocessing/`

--------------

.. include:: ../includes/wasm-mobile-notavail.rst

Giới thiệu
----------

:mod:`!multiprocessing` là một package hỗ trợ tạo tiến trình bằng API tương tự module :mod:`threading`. Package :mod:`!multiprocessing` cung cấp khả năng chạy đồng thời cả cục bộ và từ xa, qua đó tránh hiệu quả
:term:`Global Interpreter Lock <global interpreter lock>` bằng cách sử dụng các subprocess thay vì thread. Vì vậy, module :mod:`!multiprocessing` cho phép lập trình viên tận dụng tối đa nhiều bộ xử lý trên một máy. Module này chạy trên cả POSIX và Windows.

Module :mod:`!multiprocessing` cũng giới thiệu
:class:`~multiprocessing.pool.Pool` là đối tượng cung cấp một phương thức thuận tiện để thực hiện song song một hàm trên nhiều giá trị đầu vào, phân phối dữ liệu đầu vào cho các tiến trình (data parallelism). Ví dụ sau đây minh họa cách thường dùng là định nghĩa các hàm như vậy trong một module để các tiến trình con có thể import module đó thành công. Ví dụ cơ bản về data parallelism này sử dụng :class:`~multiprocessing.pool.Pool`,::

   from multiprocessing import Pool

   def f(x):
       return x*x

   if __name__ == '__main__':
       with Pool(5) as p:
           print(p.map(f, [1, 2, 3]))

sẽ in ra đầu ra tiêu chuẩn::

   [1, 4, 9]

Module :mod:`!multiprocessing` cũng giới thiệu các API không có phần tương đương trong module :mod:`threading`, chẳng hạn như khả năng :meth:`terminate <Process.terminate>`, :meth:`interrupt <Process.interrupt>` hoặc :meth:`kill <Process.kill>` một tiến trình đang chạy.

.. seealso::

   :class:`concurrent.futures.ProcessPoolExecutor` cung cấp một interface cấp cao hơn để đẩy các tác vụ vào một tiến trình nền mà không chặn việc thực thi của tiến trình gọi. So với việc sử dụng trực tiếp interface :class:`~multiprocessing.pool.Pool`, API :mod:`concurrent.futures` cho phép dễ dàng hơn tách việc gửi công việc đến process pool bên dưới khỏi việc chờ kết quả.


Lớp :class:`Process`
^^^^^^^^^^^^^^^^^^^^

Trong :mod:`!multiprocessing`, các tiến trình được tạo bằng cách tạo một đối tượng :class:`Process` rồi gọi phương thức :meth:`~Process.start` của đối tượng đó. :class:`Process` tuân theo API của :class:`threading.Thread`. Một ví dụ đơn giản về chương trình multiprocess là::

   from multiprocessing import Process

   def f(name):
       print('hello', name)

   if __name__ == '__main__':
       p = Process(target=f, args=('bob',))
       p.start()
       p.join()

Để hiển thị các ID tiến trình riêng lẻ có liên quan, dưới đây là một ví dụ mở rộng::

    from multiprocessing import Process
    import os

    def info(title):
        print(title)
        print('module name:', __name__)
        print('parent process:', os.getppid())
        print('process id:', os.getpid())

    def f(name):
        info('function f')
        print('hello', name)

    if __name__ == '__main__':
        info('main line')
        p = Process(target=f, args=('bob',))
        p.start()
        p.join()

Để biết giải thích về lý do phần ``if __name__ == '__main__'`` là cần thiết, hãy xem :ref:`multiprocessing-programming`.

Các đối số của :class:`Process` thường cần có thể được picklable để có thể truyền chúng cho tiến trình con. Nếu bạn thử nhập trực tiếp ví dụ trên vào REPL, điều đó có thể dẫn đến :exc:`AttributeError` trong tiến trình con khi cố gắng tìm hàm *f* trong mô-đun ``__main__``.


.. _multiprocessing-start-methods:

Ngữ cảnh và phương thức khởi động
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Tùy thuộc vào nền tảng, :mod:`!multiprocessing` hỗ trợ ba cách để khởi động một tiến trình. Các *start methods* này là

  .. _multiprocessing-start-method-spawn:

  *spawn*
    Tiến trình cha khởi động một tiến trình trình thông dịch Python mới. Tiến trình con sẽ chỉ kế thừa những tài nguyên cần thiết để chạy phương thức :meth:`~Process.run` của đối tượng tiến trình. Cụ thể, các bộ mô tả tệp và handle không cần thiết từ tiến trình cha sẽ không được kế thừa. Việc khởi động một tiến trình bằng phương thức này khá chậm so với việc sử dụng *fork* hoặc *forkserver*.

    Có trên các nền tảng POSIX và Windows. Đây là mặc định trên Windows và macOS.

  .. _multiprocessing-start-method-fork:

  *fork*
    Quy trình cha sử dụng :func:`os.fork` để fork trình thông dịch Python. Khi bắt đầu, quy trình con về cơ bản giống hệt quy trình cha. Tất cả tài nguyên của quy trình cha đều được kế thừa bởi quy trình con. Lưu ý rằng việc fork một quy trình đa luồng một cách an toàn là vấn đề phức tạp.

    Có trên các hệ thống POSIX.

    .. versionchanged:: 3.14
       Đây không còn là phương thức khởi động mặc định trên bất kỳ nền tảng nào. Mã yêu cầu *fork* phải chỉ định rõ điều đó thông qua
       :func:`get_context` hoặc :func:`set_start_method`.

    .. versionchanged:: 3.12
       Nếu Python phát hiện quy trình của bạn có nhiều luồng,
       hàm :func:`os.fork` được phương thức khởi động này gọi nội bộ sẽ phát sinh :exc:`DeprecationWarning`. Hãy sử dụng một phương thức khởi động khác. Xem tài liệu :func:`os.fork` để biết thêm giải thích.

  .. _multiprocessing-start-method-forkserver:

  *forkserver*
    Khi chương trình khởi động và chọn phương thức khởi động *forkserver*, một tiến trình máy chủ sẽ được tạo.  Kể từ đó, bất cứ khi nào cần một tiến trình mới, tiến trình cha sẽ kết nối với máy chủ và yêu cầu máy chủ fork một tiến trình mới.  Tiến trình máy chủ fork là tiến trình đơn luồng, trừ khi các thư viện hệ thống hoặc các import được tải trước tạo ra các luồng như một tác dụng phụ, vì vậy nhìn chung việc sử dụng :func:`os.fork` là an toàn. Không kế thừa các tài nguyên không cần thiết.

    Có sẵn trên các nền tảng POSIX hỗ trợ truyền file descriptor qua các pipe Unix, chẳng hạn như Linux. Đây là mặc định trên các nền tảng đó.

    .. versionchanged:: 3.14
       Đây đã trở thành phương thức khởi động mặc định trên các nền tảng POSIX.

.. versionchanged:: 3.4
   *spawn* được thêm vào tất cả các nền tảng POSIX, còn *forkserver* được thêm vào một số nền tảng POSIX. Các tiến trình con không còn kế thừa tất cả các handle có thể kế thừa của tiến trình cha trên Windows.

.. versionchanged:: 3.8

   Trên macOS, phương thức khởi động *spawn* hiện là mặc định.  Phương thức khởi động *fork* nên được xem là không an toàn vì có thể khiến tiến trình con bị crash, do các thư viện hệ thống macOS có thể khởi động các luồng. Xem :issue:`33725`.

.. versionchanged:: 3.14

   Trên các nền tảng POSIX, phương thức khởi động mặc định đã được thay đổi từ *fork* thành *forkserver* để duy trì hiệu năng nhưng tránh các vấn đề không tương thích phổ biến giữa các tiến trình đa luồng. Xem :gh:`84559`.


Trên POSIX, việc sử dụng các phương thức khởi động *spawn* hoặc *forkserver* cũng sẽ khởi động một tiến trình *resource tracker*, tiến trình này theo dõi các tài nguyên hệ thống có tên chưa được hủy liên kết (chẳng hạn như semaphore có tên hoặc
:class:`~multiprocessing.shared_memory.SharedMemory` objects) được tạo bởi các tiến trình của chương trình. Khi tất cả tiến trình đã thoát, resource tracker sẽ hủy liên kết mọi đối tượng còn lại đang được theo dõi. Thông thường sẽ không có đối tượng nào, nhưng nếu một tiến trình bị kết thúc bởi một signal thì có thể còn một số tài nguyên "bị rò rỉ". (Các semaphore bị rò rỉ và các phân đoạn shared memory đều sẽ không được tự động hủy liên kết cho đến lần khởi động lại tiếp theo. Điều này gây vấn đề cho cả hai loại đối tượng, vì hệ thống chỉ cho phép một số lượng semaphore có tên hạn chế, còn các phân đoạn shared memory chiếm một phần dung lượng bộ nhớ chính.)

Để chọn một phương thức khởi động, bạn sử dụng :func:`set_start_method` trong mệnh đề ``if __name__ == '__main__'`` của mô-đun chính. Ví dụ::

       import multiprocessing as mp

       def foo(q):
           q.put('hello')

       if __name__ == '__main__':
           mp.set_start_method('spawn')
           q = mp.Queue()
           p = mp.Process(target=foo, args=(q,))
           p.start()
           print(q.get())
           p.join()

:func:`set_start_method` không nên được sử dụng nhiều hơn một lần trong chương trình.

Ngoài ra, bạn có thể sử dụng :func:`get_context` để lấy một đối tượng context. Các đối tượng context có cùng API như mô-đun multiprocessing và cho phép sử dụng nhiều phương thức khởi động trong cùng một chương trình.::

       import multiprocessing as mp

       def foo(q):
           q.put('hello')

       if __name__ == '__main__':
           ctx = mp.get_context('spawn')
           q = ctx.Queue()
           p = ctx.Process(target=foo, args=(q,))
           p.start()
           print(q.get())
           p.join()

Lưu ý rằng các đối tượng liên quan đến một context có thể không tương thích với các tiến trình thuộc một context khác. Cụ thể, các lock được tạo bằng context *fork* không thể được truyền cho các tiến trình được khởi động bằng các phương thức khởi động *spawn* hoặc *forkserver*.

Các thư viện sử dụng :mod:`!multiprocessing` hoặc
:class:`~concurrent.futures.ProcessPoolExecutor` nên được thiết kế để cho phép người dùng của chúng cung cấp context multiprocessing của riêng họ. Việc sử dụng một context cụ thể của riêng bạn trong một thư viện có thể dẫn đến sự không tương thích với phần còn lại trong ứng dụng của người dùng thư viện. Luôn ghi rõ trong tài liệu nếu thư viện của bạn yêu cầu một start method cụ thể.

.. warning::

   Các start method ``'spawn'`` và ``'forkserver'`` nhìn chung không thể được sử dụng với các tệp thực thi "đóng băng" (tức là các tệp nhị phân được tạo bởi những package như **PyInstaller** và **cx_Freeze**) trên các hệ thống POSIX. Start method ``'fork'`` có thể hoạt động nếu mã không sử dụng thread.


Trao đổi object giữa các process
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:mod:`!multiprocessing` hỗ trợ hai loại kênh giao tiếp giữa các process:

**Queues**

   Class :class:`Queue` gần như là bản sao của :class:`queue.Queue`. Ví dụ:::

      from multiprocessing import Process, Queue

      def f(q):
          q.put([42, None, 'hello'])

      if __name__ == '__main__':
          q = Queue()
          p = Process(target=f, args=(q,))
          p.start()
          print(q.get())    # in ra "[42, None, 'hello']"
          p.join()

   Queue an toàn với thread và process. Bất kỳ đối tượng nào được đưa vào queue :mod:`!multiprocessing` đều sẽ được serialize.

**Pipes**

   Hàm :func:`Pipe` trả về một cặp connection object được kết nối bằng một pipe, theo mặc định là duplex (hai chiều). Ví dụ::

      from multiprocessing import Process, Pipe

      def f(conn):
          conn.send([42, None, 'hello'])
          conn.close()

      if __name__ == '__main__':
          parent_conn, child_conn = Pipe()
          p = Process(target=f, args=(child_conn,))
          p.start()
          print(parent_conn.recv())   # in ra "[42, None, 'hello']"
          p.join()

   Hai connection object được :func:`Pipe` trả về đại diện cho hai đầu của pipe. Mỗi connection object có :meth:`~Connection.send` và
   các phương thức :meth:`~Connection.recv` (cùng những phương thức khác). Lưu ý rằng dữ liệu trong pipe có thể bị hỏng nếu hai process (hoặc thread) cùng cố đọc từ hoặc ghi vào *same* đầu của pipe tại cùng một thời điểm. Tất nhiên, không có nguy cơ dữ liệu bị hỏng khi các process đồng thời sử dụng những đầu khác nhau của pipe.

   Phương thức :meth:`~Connection.send` serialize đối tượng và
   :meth:`~Connection.recv` tạo lại đối tượng.

Đồng bộ hóa giữa các tiến trình
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:mod:`!multiprocessing` chứa các thành phần tương đương với tất cả các primitive đồng bộ hóa từ :mod:`threading`. Ví dụ, bạn có thể sử dụng lock để đảm bảo rằng mỗi lần chỉ có một tiến trình in ra đầu ra tiêu chuẩn::

   from multiprocessing import Process, Lock

   def f(l, i):
       l.acquire()
       try:
           print('hello world', i)
       finally:
           l.release()

   if __name__ == '__main__':
       lock = Lock()

       for num in range(10):
           Process(target=f, args=(lock, num)).start()

Nếu không sử dụng lock, đầu ra từ các tiến trình khác nhau rất dễ bị trộn lẫn hoàn toàn.


Chia sẻ trạng thái giữa các tiến trình
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Như đã đề cập ở trên, khi lập trình đồng thời, thông thường tốt nhất là tránh sử dụng trạng thái dùng chung ככל có thể. Điều này đặc biệt đúng khi sử dụng nhiều tiến trình.

Tuy nhiên, nếu thực sự cần sử dụng một số dữ liệu dùng chung thì
:mod:`!multiprocessing` cung cấp một vài cách để thực hiện việc đó.

**Bộ nhớ dùng chung**

   Dữ liệu có thể được lưu trữ trong một map bộ nhớ dùng chung bằng :class:`Value` hoặc
   :class:`Array`. Ví dụ: đoạn mã sau đây::

      from multiprocessing import Process, Value, Array

      def f(n, a):
          n.value = 3.1415927
          for i in range(len(a)):
              a[i] = -a[i]

      if __name__ == '__main__':
          num = Value('d', 0.0)
          arr = Array('i', range(10))

          p = Process(target=f, args=(num, arr))
          p.start()
          p.join()

          print(num.value)
          print(arr[:])

   sẽ in ra::

      3.1415927
      [0, -1, -2, -3, -4, -5, -6, -7, -8, -9]

   Các đối số ``'d'`` và ``'i'`` được sử dụng khi tạo ``num`` và ``arr`` là các mã kiểu (typecode) thuộc loại được sử dụng bởi module :mod:`array`: ``'d'`` cho biết một số thực có độ chính xác kép, còn ``'i'`` cho biết một số nguyên có dấu. Các đối tượng dùng chung này sẽ an toàn đối với process và thread.

   Để linh hoạt hơn khi sử dụng bộ nhớ dùng chung, bạn có thể sử dụng
   :mod:`multiprocessing.sharedctypes` mô-đun hỗ trợ tạo các đối tượng ctypes tùy ý được cấp phát từ bộ nhớ dùng chung.

**Quy trình máy chủ**

   Một đối tượng manager được trả về bởi :func:`Manager` điều khiển một quy trình máy chủ lưu giữ các đối tượng Python và cho phép các quy trình khác thao tác với chúng bằng proxy.

   Một manager được trả về bởi :func:`Manager` sẽ hỗ trợ các kiểu
   :class:`list`, :class:`dict`, :class:`set`, :class:`~managers.Namespace`, :class:`Lock`,
   :class:`RLock`, :class:`Semaphore`, :class:`BoundedSemaphore`,
   :class:`Condition`, :class:`Event`, :class:`Barrier`,
   :class:`Queue`, :class:`Value` và :class:`Array`.  Ví dụ:::

      from multiprocessing import Process, Manager

      def f(d, l, s):
          d[1] = '1'
          d['2'] = 2
          d[0.25] = None
          l.reverse()
          s.add('a')
          s.add('b')

      if __name__ == '__main__':
          with Manager() as manager:
              d = manager.dict()
              l = manager.list(range(10))
              s = manager.set()

              p = Process(target=f, args=(d, l, s))
              p.start()
              p.join()

              print(d)
              print(l)
              print(s)

   sẽ in ra::

       {0.25: None, 1: '1', '2': 2}
       [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
       {'a', 'b'}

   Các manager quy trình máy chủ linh hoạt hơn so với việc sử dụng các đối tượng bộ nhớ dùng chung vì chúng có thể được cấu hình để hỗ trợ các kiểu đối tượng tùy ý. Ngoài ra, một manager duy nhất có thể được các quy trình trên những máy tính khác nhau chia sẻ qua mạng. Tuy nhiên, chúng chậm hơn so với việc sử dụng bộ nhớ dùng chung.


Sử dụng một nhóm worker
^^^^^^^^^^^^^^^^^^^^^^^

Lớp :class:`~multiprocessing.pool.Pool` biểu diễn một nhóm các tiến trình worker. Lớp này có các phương thức cho phép chuyển tác vụ sang các tiến trình worker theo một vài cách khác nhau.

Ví dụ::

   from multiprocessing import Pool, TimeoutError
   import time
   import os

   def f(x):
       return x*x

   if __name__ == '__main__':
       # khởi động 4 tiến trình worker
       with Pool(processes=4) as pool:

           # in "[0, 1, 4,..., 81]"
           print(pool.map(f, range(10)))

           # in các số đó theo thứ tự bất kỳ
           for i in pool.imap_unordered(f, range(10)):
               print(i)

           # đánh giá "f(20)" một cách bất đồng bộ
           res = pool.apply_async(f, (20,))      # chạy trong *chỉ* một process
           print(res.get(timeout=1))             # in "400"

           # đánh giá "os.getpid()" một cách bất đồng bộ
           res = pool.apply_async(os.getpid, ()) # chạy trong *chỉ* một process
           print(res.get(timeout=1))             # in PID của process đó

           # việc khởi chạy nhiều lần đánh giá một cách bất đồng bộ *có thể* sử dụng nhiều process
           multiple_results = [pool.apply_async(os.getpid, ()) for i in range(4)]
           print([res.get(timeout=1) for res in multiple_results])

           # cho một worker duy nhất ngủ trong 10 giây
           res = pool.apply_async(time.sleep, (10,))
           try:
               print(res.get(timeout=1))
           except TimeoutError:
               print("We lacked patience and got a multiprocessing.TimeoutError")

           print("For the moment, the pool remains available for more work")

       # thoát khỏi khối 'with' đã dừng pool
       print("Now the pool is closed and no longer available")

Lưu ý rằng các phương thức của pool chỉ được sử dụng bởi tiến trình đã tạo ra pool đó.

.. note::

   Các chức năng trong package này yêu cầu module ``__main__`` có thể được import bởi các tiến trình con. Điều này đã được đề cập trong :ref:`multiprocessing-programming`, tuy nhiên vẫn cần lưu ý ở đây. Điều này có nghĩa là một số ví dụ, chẳng hạn như các ví dụ :class:`multiprocessing.pool.Pool`, sẽ không hoạt động trong trình thông dịch tương tác. Ví dụ::

      >>> from multiprocessing import Pool
      >>> p = Pool(5)
      >>> def f(x):
      ...     return x*x
      ...
      >>> with p:
      ...     p.map(f, [1,2,3])
      Process PoolWorker-1:
      Process PoolWorker-2:
      Process PoolWorker-3:
      Traceback (most recent call last):
      Traceback (most recent call last):
      Traceback (most recent call last):
      AttributeError: Can't get attribute 'f' on <module '__main__' (<class '_frozen_importlib.BuiltinImporter'>)>
      AttributeError: Can't get attribute 'f' on <module '__main__' (<class '_frozen_importlib.BuiltinImporter'>)>
      AttributeError: Can't get attribute 'f' on <module '__main__' (<class '_frozen_importlib.BuiltinImporter'>)>

   (Nếu thử chạy đoạn này, thực tế nó sẽ xuất ra ba traceback đầy đủ xen kẽ theo thứ tự gần như ngẫu nhiên, sau đó bạn có thể phải dừng tiến trình cha bằng cách nào đó.)


Tham khảo
---------

Package :mod:`!multiprocessing` chủ yếu mô phỏng API của
module :mod:`threading`.

.. _global-start-method:

Phương thức khởi động toàn cục
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Python hỗ trợ một số cách để tạo và khởi tạo một process. Phương thức khởi động toàn cục đặt cơ chế mặc định để tạo process.

Một số hàm và phương thức multiprocessing cũng có thể khởi tạo một số đối tượng nhất định sẽ ngầm đặt phương thức khởi động toàn cục thành giá trị mặc định của hệ thống, nếu phương thức này chưa được đặt. Phương thức khởi động toàn cục chỉ có thể được đặt một lần. Nếu cần thay đổi phương thức khởi động khỏi giá trị mặc định của hệ thống, bạn phải chủ động đặt phương thức khởi động toàn cục trước khi gọi các hàm hoặc phương thức, hoặc tạo các đối tượng này.


:class:`Process` và các ngoại lệ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Process(group=None, target=None, name=None, args=(), kwargs={}, \
                   *, daemon=None)

   Các đối tượng Process biểu diễn hoạt động được chạy trong một process riêng biệt.
   Lớp :class:`Process` có các phương thức tương đương với tất cả các phương thức của
   :class:`threading.Thread`.

   Hàm khởi tạo luôn phải được gọi bằng các đối số từ khóa. *group* luôn phải là ``None``; nó chỉ tồn tại để duy trì khả năng tương thích với
   :class:`threading.Thread`. *target* là đối tượng callable sẽ được gọi bởi phương thức :meth:`run`. Giá trị mặc định là ``None``, nghĩa là không có gì được gọi. *name* là tên của process (xem :attr:`name` để biết thêm chi tiết). *args* là tuple đối số dùng để gọi target. *kwargs* là dictionary chứa các đối số từ khóa dùng để gọi target. Nếu được cung cấp, đối số chỉ có thể dùng với từ khóa *daemon* sẽ đặt cờ :attr:`daemon` của process thành ``True`` hoặc ``False``. Nếu là ``None`` (giá trị mặc định), cờ này sẽ được kế thừa từ process tạo ra nó.

   Theo mặc định, không có đối số nào được truyền cho *target*. Đối số *args*, có giá trị mặc định là ``()``, có thể được dùng để chỉ định danh sách hoặc tuple các đối số truyền cho *target*.

   Nếu một subclass ghi đè hàm khởi tạo, subclass đó phải bảo đảm gọi hàm khởi tạo của lớp cơ sở (``super().__init__()``) trước khi thực hiện bất kỳ thao tác nào khác với process.

   .. note::

      Nhìn chung, mọi đối số truyền cho :class:`Process` đều phải có thể được pickling. Điều này thường được nhận thấy khi cố tạo một :class:`Process` hoặc sử dụng một
      :class:`concurrent.futures.ProcessPoolExecutor` từ REPL với một hàm *target* được định nghĩa cục bộ.

      Việc truyền một đối tượng callable được định nghĩa trong phiên REPL hiện tại khiến child process kết thúc do ngoại lệ :exc:`AttributeError` không được bắt khi khởi động, vì *target* phải được định nghĩa trong một module có thể import để được tải trong quá trình unpickling.

      Ví dụ về lỗi không thể bắt này từ tiến trình con::

         >>> import multiprocessing as mp
         >>> def knigit():
         ...     print("Ni!")
         ...
         >>> process = mp.Process(target=knigit)
         >>> process.start()
         >>> Traceback (most recent call last):
           File ".../multiprocessing/spawn.py", line ..., in spawn_main
           File ".../multiprocessing/spawn.py", line ..., in _main
         AttributeError: module '__main__' has no attribute 'knigit'
         >>> process
         <SpawnProcess name='SpawnProcess-1' pid=379473 parent=378707 stopped exitcode=1>

      Xem :ref:`multiprocessing-programming-spawn`. Mặc dù hạn chế này không đúng khi sử dụng phương thức start ``"fork"``, kể từ Python ``3.14`` phương thức này không còn là mặc định trên bất kỳ nền tảng nào. Xem
      :ref:`multiprocessing-start-methods`. Xem thêm :gh:`132898`.

   .. versionchanged:: 3.3
      Đã thêm tham số *daemon*.

   .. method:: run()

      Phương thức đại diện cho hoạt động của tiến trình.

      Bạn có thể ghi đè phương thức này trong một lớp con. Phương thức :meth:`run` chuẩn gọi đối tượng callable được truyền vào hàm khởi tạo của đối tượng làm đối số target, nếu có, với các đối số tuần tự và đối số từ khóa lần lượt được lấy từ các đối số *args* và *kwargs*.

      Sử dụng một list hoặc tuple làm đối số *args* được truyền vào :class:`Process` sẽ tạo ra hiệu ứng tương tự.

      Ví dụ::

         >>> from multiprocessing import Process
         >>> p = Process(target=print, args=[1])
         >>> p.run()
         1
         >>> p = Process(target=print, args=(1,))
         >>> p.run()
         1

   .. method:: start()

      Bắt đầu hoạt động của tiến trình.

      Phương thức này phải được gọi nhiều nhất một lần cho mỗi đối tượng tiến trình. Phương thức này sắp xếp để phương thức :meth:`run` của đối tượng được gọi trong một tiến trình riêng.

   .. method:: join([timeout])

      Nếu đối số tùy chọn *timeout* là ``None`` (giá trị mặc định), phương thức sẽ chặn cho đến khi tiến trình có phương thức :meth:`join` được gọi kết thúc. Nếu *timeout* là một số dương, phương thức sẽ chặn nhiều nhất *timeout* giây. Lưu ý rằng phương thức trả về ``None`` nếu tiến trình của nó kết thúc hoặc nếu phương thức hết thời gian chờ. Kiểm tra :attr:`exitcode` của tiến trình để xác định xem tiến trình đó đã kết thúc hay chưa.

      Có thể join một tiến trình nhiều lần.

      Một tiến trình không thể join chính nó vì điều này sẽ gây ra deadlock. Việc cố gắng join một tiến trình trước khi tiến trình đó được khởi động là một lỗi.

   .. attribute:: name

      Tên của tiến trình. Tên là một chuỗi chỉ được dùng cho mục đích nhận dạng. Tên không mang ngữ nghĩa nào. Nhiều tiến trình có thể được đặt cùng một tên.

      Tên ban đầu được đặt bởi constructor. Nếu không cung cấp tên rõ ràng cho constructor, một tên có dạng 'Process-N\ :sub:`1`:N\ :sub:`2`:...:N\ :sub:`k`' sẽ được tạo, trong đó mỗi N\ :sub:`k` là con thứ N của tiến trình cha.

   .. method:: is_alive

      Trả về liệu tiến trình có đang hoạt động hay không.

      Nói chung, một đối tượng tiến trình được xem là đang hoạt động kể từ thời điểm phương thức :meth:`start` trả về cho đến khi tiến trình con kết thúc.

   .. attribute:: daemon

      Cờ daemon của tiến trình, một giá trị Boolean. Giá trị này phải được đặt trước khi
      gọi :meth:`start`.

      Giá trị ban đầu được kế thừa từ tiến trình tạo ra nó.

      Khi một tiến trình kết thúc, nó cố gắng chấm dứt tất cả các tiến trình con daemon của mình.

      Lưu ý rằng một tiến trình daemon không được phép tạo các tiến trình con. Nếu không, tiến trình daemon sẽ để lại các tiến trình con của nó ở trạng thái mồ côi nếu bị chấm dứt khi tiến trình cha kết thúc. Ngoài ra, đây **không phải** là Unix daemon hoặc service, mà là các tiến trình thông thường sẽ bị chấm dứt (chứ không được join) nếu các tiến trình không phải daemon đã kết thúc.

   Ngoài :class:`threading.Thread` API, các đối tượng :class:`Process` cũng hỗ trợ các thuộc tính và phương thức sau:

   .. attribute:: pid

      Trả về ID của tiến trình. Trước khi tiến trình được tạo, giá trị này sẽ là ``None``.

   .. attribute:: exitcode

      Mã thoát của tiến trình con. Giá trị này sẽ là ``None`` nếu tiến trình chưa kết thúc.

      Nếu phương thức :meth:`run` của tiến trình con trả về bình thường, mã thoát sẽ là 0. Nếu tiến trình kết thúc qua :func:`sys.exit` với đối số số nguyên *N*, mã thoát sẽ là *N*.

      Nếu tiến trình con kết thúc do một ngoại lệ không được bắt trong
      :meth:`run`, mã thoát sẽ là 1. Nếu tiến trình bị chấm dứt bởi signal *N*, mã thoát sẽ là giá trị âm *-N*.

   .. attribute:: authkey

      Khóa xác thực của process (một chuỗi byte).

      Khi :mod:`!multiprocessing` được khởi tạo, process chính được gán một chuỗi ngẫu nhiên bằng :func:`os.urandom`.

      Khi một đối tượng :class:`Process` được tạo, đối tượng này sẽ kế thừa khóa xác thực của process cha, mặc dù khóa này có thể được thay đổi bằng cách đặt :attr:`authkey` thành một chuỗi byte khác.

      Xem :ref:`multiprocessing-auth-keys`.

   .. attribute:: sentinel

      Một handle dạng số của đối tượng hệ thống sẽ chuyển sang trạng thái "sẵn sàng" khi process kết thúc.

      Bạn có thể sử dụng giá trị này nếu muốn chờ nhiều sự kiện cùng lúc bằng :func:`multiprocessing.connection.wait`. Nếu không, việc gọi :meth:`join` sẽ đơn giản hơn.

      Trên Windows, đây là một handle của hệ điều hành có thể sử dụng với nhóm lệnh gọi API ``WaitForSingleObject`` và ``WaitForMultipleObjects``. Trên POSIX, đây là một file descriptor có thể sử dụng với các primitive từ module :mod:`select`.

      .. versionadded:: 3.3

   .. method:: interrupt()

      Kết thúc tiến trình. Hoạt động trên POSIX bằng tín hiệu :py:const:`~signal.SIGINT`. Hành vi trên Windows không được xác định.

      Theo mặc định, thao tác này kết thúc tiến trình con bằng cách phát sinh :exc:`KeyboardInterrupt`. Có thể thay đổi hành vi này bằng cách thiết lập trình xử lý tín hiệu tương ứng trong tiến trình con :func:`signal.signal` cho :py:const:`~signal.SIGINT`.

      Lưu ý: nếu tiến trình con bắt và loại bỏ :exc:`KeyboardInterrupt`, tiến trình sẽ không bị kết thúc.

      Lưu ý: hành vi mặc định cũng sẽ đặt :attr:`exitcode` thành ``1``, như thể một ngoại lệ không được bắt đã được phát sinh trong tiến trình con. Để có một
      :attr:`exitcode` khác, bạn chỉ cần bắt :exc:`KeyboardInterrupt` và gọi ``exit(your_code)``.

      .. versionadded:: 3.14

   .. method:: terminate()

      Kết thúc tiến trình. Trên POSIX, việc này được thực hiện bằng tín hiệu :py:const:`~signal.SIGTERM`; trên Windows, :c:func:`!TerminateProcess` được sử dụng. Lưu ý rằng các trình xử lý khi thoát và mệnh đề finally, v.v. sẽ không được thực thi.

      Lưu ý rằng các tiến trình hậu duệ của tiến trình này *không* bị kết thúc -- chúng sẽ đơn giản trở thành các tiến trình mồ côi.

      .. warning::

         Nếu phương thức này được sử dụng khi process liên quan đang sử dụng pipe hoặc queue thì pipe hoặc queue có nguy cơ bị hỏng và có thể không thể được process khác sử dụng. Tương tự, nếu process đã chiếm một lock hoặc semaphore, v.v. thì việc kết thúc process đó có nguy cơ khiến các process khác bị deadlock.

   .. method:: kill()

      Tương tự như :meth:`terminate` nhưng sử dụng signal ``SIGKILL`` trên POSIX.

      .. versionadded:: 3.7

   .. method:: close()

      Đóng đối tượng :class:`Process`, giải phóng tất cả tài nguyên liên kết với đối tượng đó. :exc:`ValueError` sẽ được phát sinh nếu process nền vẫn đang chạy. Sau khi :meth:`close` trả về thành công, hầu hết các phương thức và thuộc tính khác của đối tượng :class:`Process` sẽ phát sinh :exc:`ValueError`.

      .. versionadded:: 3.7

   Lưu ý rằng các phương thức :meth:`start`, :meth:`join`, :meth:`is_alive`,
   :meth:`terminate` và :attr:`exitcode` chỉ nên được gọi bởi process đã tạo đối tượng process.

   Ví dụ sử dụng một số phương thức của :class:`Process`:

   .. doctest::

       >>> import multiprocessing, time, signal
       >>> mp_context = multiprocessing.get_context('spawn')
       >>> p = mp_context.Process(target=time.sleep, args=(1000,))
       >>> print(p, p.is_alive())
       <...Process ... initial> False
       >>> p.start()
       >>> print(p, p.is_alive())
       <...Process ... started> True
       >>> p.terminate()
       >>> time.sleep(0.1)
       >>> print(p, p.is_alive())
       <...Process ... stopped exitcode=-SIGTERM> False
       >>> p.exitcode == -signal.SIGTERM
       True

.. exception:: ProcessError

   Lớp cơ sở của tất cả các exception :mod:`!multiprocessing`.

.. exception:: BufferTooShort

   Ngoại lệ do :meth:`Connection.recv_bytes_into` đưa ra khi đối tượng buffer được cung cấp quá nhỏ so với thông báo được đọc.

   Nếu ``e`` là một thể hiện của :exc:`BufferTooShort` thì ``e.args[0]`` sẽ cung cấp thông báo dưới dạng chuỗi byte.

.. exception:: AuthenticationError

   Được đưa ra khi xảy ra lỗi xác thực.

.. exception:: TimeoutError

   Được đưa ra bởi các phương thức có thời gian chờ khi thời gian chờ hết hạn.

Pipe và Queue
^^^^^^^^^^^^^

Khi sử dụng nhiều process, thông thường người ta dùng truyền thông báo để giao tiếp giữa các process và tránh phải sử dụng các primitive đồng bộ hóa như lock.

Để truyền thông báo, có thể sử dụng :func:`Pipe` (cho một kết nối giữa hai process) hoặc queue (cho phép nhiều producer và consumer).

Các kiểu :class:`Queue`, :class:`SimpleQueue` và :class:`JoinableQueue` là các hàng đợi :abbr:`FIFO (first-in, first-out)` đa nhà sản xuất, đa người tiêu dùng, được mô phỏng theo lớp :class:`queue.Queue` trong thư viện chuẩn. Chúng khác ở chỗ :class:`Queue` không có
các phương thức :meth:`~queue.Queue.task_done` và :meth:`~queue.Queue.join` được giới thiệu trong lớp :class:`queue.Queue` của Python 2.5.

Nếu sử dụng :class:`JoinableQueue`, bạn **must** gọi
:meth:`JoinableQueue.task_done` cho mỗi tác vụ được lấy khỏi hàng đợi; nếu không, semaphore dùng để đếm số tác vụ chưa hoàn thành cuối cùng có thể bị tràn, khiến một ngoại lệ được nâng lên.

Một điểm khác so với các cách triển khai hàng đợi Python khác là các hàng đợi :mod:`!multiprocessing` tuần tự hóa tất cả đối tượng được đưa vào chúng bằng :mod:`pickle`. Đối tượng được phương thức get trả về là một đối tượng được tạo lại và không dùng chung bộ nhớ với đối tượng ban đầu.

Lưu ý rằng bạn cũng có thể tạo một hàng đợi dùng chung bằng cách sử dụng đối tượng manager -- xem
:ref:`multiprocessing-managers`.

.. note::

   :mod:`!multiprocessing` sử dụng :exc:`queue.Empty` thông thường và
   :exc:`queue.Full` để báo hiệu hết thời gian chờ. Chúng không có trong namespace :mod:`!multiprocessing`, vì vậy bạn cần import chúng từ
   :mod:`queue`.

.. note::

   Khi một đối tượng được đưa vào queue, đối tượng đó sẽ được pickle và một background thread sau đó sẽ flush dữ liệu đã pickle vào pipe bên dưới. Điều này dẫn đến một số hệ quả hơi bất ngờ, nhưng không gây ra khó khăn thực tế nào -- nếu chúng thực sự khiến bạn khó chịu, bạn có thể thay vào đó sử dụng một queue được tạo bằng
   :ref:`manager <multiprocessing-managers>`.

   (1) Sau khi đưa một đối tượng vào queue đang trống, có thể xảy ra một khoảng trễ cực nhỏ trước khi phương thức :meth:`~Queue.empty` của queue trả về :const:`False` và :meth:`~Queue.get_nowait` có thể trả về mà không phát sinh :exc:`queue.Empty`.

   (2) Nếu nhiều process đang đưa các đối tượng vào queue, các đối tượng có thể được nhận ở đầu bên kia không đúng thứ tự. Tuy nhiên, các đối tượng được đưa vào queue bởi cùng một process sẽ luôn giữ đúng thứ tự tương ứng với nhau.

.. warning::

   Nếu một process bị kết thúc bằng :meth:`Process.terminate` hoặc :func:`os.kill` trong khi đang cố sử dụng :class:`Queue`, dữ liệu trong queue có thể bị hỏng. Điều này có thể khiến bất kỳ process nào khác phát sinh exception khi cố sử dụng queue về sau.

.. warning::

   Như đã đề cập ở trên, nếu một child process đã đưa các mục vào queue (và chưa sử dụng :meth:`JoinableQueue.cancel_join_thread <multiprocessing.Queue.cancel_join_thread>`), process đó sẽ không kết thúc cho đến khi tất cả các mục trong buffer được flush vào pipe.

   Điều này có nghĩa là nếu bạn cố gắng join tiến trình đó, bạn có thể gặp deadlock trừ khi chắc chắn rằng tất cả các mục đã được đưa vào queue đều đã được xử lý. Tương tự, nếu tiến trình con không phải daemon thì tiến trình cha có thể bị treo khi thoát, lúc cố gắng join tất cả các tiến trình con không phải daemon của nó.

   Lưu ý rằng queue được tạo bằng manager không gặp vấn đề này. Xem
   :ref:`multiprocessing-programming`.

Để xem ví dụ về cách sử dụng queue cho giao tiếp giữa các tiến trình, hãy xem
:ref:`multiprocessing-examples`.


.. function:: Pipe(duplex=True)

   Trả về một cặp ``(conn1, conn2)`` gồm
   các đối tượng :class:`~multiprocessing.connection.Connection` đại diện cho hai đầu của một pipe.

   Nếu *duplex* là ``True`` (mặc định) thì pipe là hai chiều. Nếu *duplex* là ``False`` thì pipe là một chiều: ``conn1`` chỉ có thể được dùng để nhận thông báo và ``conn2`` chỉ có thể được dùng để gửi thông báo.

   Phương thức :meth:`~multiprocessing.Connection.send` tuần tự hóa đối tượng bằng cách sử dụng
   :mod:`pickle` và :meth:`~multiprocessing.Connection.recv` tạo lại đối tượng.

.. class:: Queue([maxsize])

   Trả về một queue dùng chung giữa các process, được triển khai bằng một pipe và một số locks/semaphores. Khi một process lần đầu đưa một item vào queue, một feeder thread sẽ được khởi động để chuyển các object từ bộ đệm vào pipe.

   Việc khởi tạo class này có thể thiết lập phương thức start toàn cục. Xem
   :ref:`global-start-method` để biết thêm chi tiết.

   Các exception :exc:`queue.Empty` và :exc:`queue.Full` thông thường từ module :mod:`queue` của standard library được raise để báo hiệu timeout.

   :class:`Queue` triển khai tất cả các phương thức của :class:`queue.Queue` ngoại trừ
   :meth:`~queue.Queue.task_done`, :meth:`~queue.Queue.join`, và
   :meth:`~queue.Queue.shutdown`.

   .. method:: qsize()

      Trả về kích thước xấp xỉ của hàng đợi. Do ngữ nghĩa của multithreading/multiprocessing, con số này không đáng tin cậy.

      Lưu ý rằng thao tác này có thể phát sinh :exc:`NotImplementedError` trên các nền tảng như macOS, nơi ``sem_getvalue()`` chưa được triển khai.

   .. method:: empty()

      Trả về ``True`` nếu hàng đợi trống, ngược lại trả về ``False``. Do ngữ nghĩa của multithreading/multiprocessing, kết quả này không đáng tin cậy.

      Có thể phát sinh một :exc:`OSError` trên các hàng đợi đã đóng. (không được đảm bảo)

   .. method:: full()

      Trả về ``True`` nếu hàng đợi đầy, ngược lại trả về ``False``. Do ngữ nghĩa của multithreading/multiprocessing, kết quả này không đáng tin cậy.

   .. method:: put(obj[, block[, timeout]])

      Đưa obj vào hàng đợi. Nếu đối số tùy chọn *block* là ``True`` (mặc định) và *timeout* là ``None`` (mặc định), thao tác sẽ chặn nếu cần cho đến khi có một vị trí trống. Nếu *timeout* là một số dương, thao tác sẽ chặn tối đa *timeout* giây và phát sinh ngoại lệ :exc:`queue.Full` nếu không có vị trí trống trong khoảng thời gian đó. Ngược lại (*block* là ``False``), đưa một mục vào hàng đợi nếu có ngay một vị trí trống; nếu không, phát sinh ngoại lệ :exc:`queue.Full` (*timeout* bị bỏ qua trong trường hợp này).

      .. versionchanged:: 3.8
         Nếu hàng đợi đã đóng, :exc:`ValueError` sẽ được phát sinh thay vì
         :exc:`AssertionError`.

   .. method:: put_nowait(obj)

      Tương đương với ``put(obj, False)``.

   .. method:: get([block[, timeout]])

      Xóa và trả về một mục khỏi queue. Nếu các đối số tùy chọn *block* là ``True`` (mặc định) và *timeout* là ``None`` (mặc định), hãy chờ nếu cần cho đến khi có một mục. Nếu *timeout* là một số dương, thao tác sẽ chờ tối đa *timeout* giây và phát sinh ngoại lệ :exc:`queue.Empty` nếu không có mục nào trong khoảng thời gian đó. Ngược lại (block là ``False``), trả về một mục nếu có sẵn ngay lập tức; nếu không, phát sinh
      ngoại lệ :exc:`queue.Empty` (*timeout* bị bỏ qua trong trường hợp đó).

      .. versionchanged:: 3.8
         Nếu hàng đợi đã đóng, :exc:`ValueError` sẽ được phát sinh thay vì
         :exc:`OSError`.

   .. method:: get_nowait()

      Tương đương với ``get(False)``.

   :class:`multiprocessing.Queue` có một số phương thức bổ sung không có trong
   :class:`queue.Queue`. Các phương thức này thường không cần thiết đối với hầu hết mã nguồn:

   .. method:: close()

      Đóng queue: giải phóng các tài nguyên nội bộ.

      Không được sử dụng queue nữa sau khi đã đóng. Ví dụ:
      Không được gọi các phương thức :meth:`~Queue.get`, :meth:`~Queue.put` và :meth:`~Queue.empty` nữa.

      Luồng nền sẽ thoát sau khi đã flush toàn bộ dữ liệu được đệm vào pipe. Thao tác này được tự động gọi khi queue được garbage collect.

   .. method:: join_thread()

      Join luồng nền. Chỉ có thể sử dụng thao tác này sau khi đã gọi :meth:`close`. Thao tác này sẽ chặn cho đến khi luồng nền thoát, đảm bảo toàn bộ dữ liệu trong bộ đệm đã được flush vào pipe.

      Theo mặc định, nếu một process không phải là process tạo queue thì khi thoát, process đó sẽ cố gắng join luồng nền của queue. Process có thể gọi
      :meth:`cancel_join_thread` để khiến :meth:`join_thread` không thực hiện thao tác nào.

   .. method:: cancel_join_thread()

      Ngăn :meth:`join_thread` chặn. Cụ thể, thao tác này ngăn luồng nền tự động được join khi tiến trình thoát — xem :meth:`join_thread`.

      Một tên phù hợp hơn cho phương thức này có thể là ``allow_exit_without_flush()``. Phương thức này có khả năng khiến dữ liệu đã xếp hàng bị mất, và gần như chắc chắn bạn sẽ không cần sử dụng nó. Thực ra, phương thức này chỉ tồn tại trong trường hợp bạn cần tiến trình hiện tại thoát ngay lập tức mà không chờ xả dữ liệu đã xếp hàng vào pipe bên dưới, đồng thời không quan tâm đến việc dữ liệu bị mất.

   .. note::

      Chức năng của lớp này yêu cầu hệ điều hành máy chủ có một implementation semaphore dùng chung hoạt động được. Nếu không có, chức năng của lớp này sẽ bị vô hiệu hóa, và việc khởi tạo một :class:`Queue` sẽ dẫn đến :exc:`ImportError`. Xem
      :issue:`3770` để biết thêm thông tin. Điều tương tự cũng áp dụng cho bất kỳ kiểu queue chuyên biệt nào được liệt kê bên dưới.

.. class:: SimpleQueue()

   Đây là một kiểu :class:`Queue` đơn giản hóa, rất gần với một :class:`Pipe` bị khóa.

   Việc khởi tạo class này có thể thiết lập phương thức start toàn cục. Xem
   :ref:`global-start-method` để biết thêm chi tiết.

   .. method:: close()

      Đóng queue: giải phóng các tài nguyên nội bộ.

      Không được sử dụng queue nữa sau khi đã đóng. Ví dụ:
      Không được gọi các phương thức :meth:`get`, :meth:`put` và :meth:`empty` nữa.

      .. versionadded:: 3.9

   .. method:: empty()

      Trả về ``True`` nếu hàng đợi rỗng, nếu không thì trả về ``False``.

      Luôn phát sinh một :exc:`OSError` nếu SimpleQueue bị đóng.

   .. method:: get()

      Xóa và trả về một mục khỏi hàng đợi.

   .. method:: put(item)

      Đưa *item* vào hàng đợi.


.. class:: JoinableQueue([maxsize])

   :class:`JoinableQueue`, một lớp con của :class:`Queue`, là một queue có thêm các phương thức :meth:`task_done` và :meth:`join`.

   Việc khởi tạo class này có thể thiết lập phương thức start toàn cục. Xem
   :ref:`global-start-method` để biết thêm chi tiết.

   .. method:: task_done()

      Đánh dấu rằng một tác vụ đã được đưa vào queue trước đó đã hoàn tất. Được các consumer của queue sử dụng. Với mỗi :meth:`~Queue.get` được sử dụng để lấy một tác vụ, một lần gọi :meth:`task_done` tiếp theo sẽ cho queue biết rằng việc xử lý tác vụ đó đã hoàn tất.

      Nếu một :meth:`~queue.Queue.join` hiện đang bị chặn, nó sẽ tiếp tục khi tất cả các mục đã được xử lý (nghĩa là đã nhận được một lần gọi :meth:`task_done` cho mỗi mục đã được :meth:`~Queue.put` vào queue).

      Phát sinh :exc:`ValueError` nếu được gọi nhiều lần hơn số mục đã được đưa vào queue.


   .. method:: join()

      Chặn cho đến khi tất cả các mục trong queue đã được lấy ra và xử lý.

      Số lượng tác vụ chưa hoàn tất tăng lên mỗi khi một mục được thêm vào queue. Số lượng này giảm xuống mỗi khi consumer gọi
      :meth:`task_done` để cho biết rằng mục đó đã được truy xuất và mọi công việc liên quan đã hoàn tất. Khi số lượng tác vụ chưa hoàn tất giảm xuống bằng 0,
      :meth:`~queue.Queue.join` bỏ chặn.


Linh tinh
^^^^^^^^^

.. function:: active_children()

   Trả về danh sách tất cả tiến trình con đang hoạt động của tiến trình hiện tại.

   Việc gọi hàm này có tác dụng phụ là "join" mọi tiến trình đã kết thúc.

.. function:: cpu_count()

   Trả về số lượng CPU trong hệ thống.

   Con số này không tương đương với số CPU mà tiến trình hiện tại có thể sử dụng. Có thể lấy số CPU khả dụng bằng
   :func:`os.process_cpu_count` (hoặc ``len(os.sched_getaffinity(0))``).

   Khi không thể xác định số CPU, :exc:`NotImplementedError` sẽ được đưa ra.

   .. seealso::
      :func:`os.cpu_count`
      :func:`os.process_cpu_count`

   .. versionchanged:: 3.13

      Giá trị trả về cũng có thể được ghi đè bằng
      cờ :option:`-X cpu_count <-X>` hoặc :envvar:`PYTHON_CPU_COUNT`, vì đây chỉ là một wrapper quanh các API đếm CPU :mod:`os`.

.. function:: current_process()

   Trả về đối tượng :class:`Process` tương ứng với tiến trình hiện tại.

   Một phiên bản tương đương với :func:`threading.current_thread`.

.. function:: parent_process()

   Trả về đối tượng :class:`Process` tương ứng với tiến trình cha của :func:`current_process`. Đối với tiến trình chính, ``parent_process`` sẽ là ``None``.

   .. versionadded:: 3.8

.. function:: freeze_support()

   Thêm hỗ trợ cho trường hợp một chương trình sử dụng :mod:`!multiprocessing` đã được đóng băng để tạo thành tệp thực thi. (Đã được kiểm thử với **py2exe**, **PyInstaller** và **cx_Freeze**.)

   Cần gọi hàm này ngay sau dòng ``if __name__ == '__main__'`` của module chính. Ví dụ::

      from multiprocessing import Process, freeze_support

      def f():
          print('hello world!')

      if __name__ == '__main__':
          freeze_support()
          Process(target=f).start()

   Nếu bỏ qua dòng ``freeze_support()`` thì việc cố chạy tệp thực thi đã đóng băng sẽ gây ra :exc:`RuntimeError`.

   Việc gọi ``freeze_support()`` không có tác dụng khi phương thức khởi động không phải là *spawn*. Ngoài ra, nếu module đang được chạy bình thường bằng trình thông dịch Python (chương trình chưa được đóng băng), thì ``freeze_support()`` cũng không có tác dụng.

.. function:: get_all_start_methods()

   Trả về danh sách các phương thức khởi động được hỗ trợ, trong đó phương thức đầu tiên là mặc định. Các phương thức khởi động có thể có là ``'fork'``, ``'spawn'`` và ``'forkserver'``. Không phải nền tảng nào cũng hỗ trợ tất cả các phương thức. Xem :ref:`multiprocessing-start-methods`.

   .. versionadded:: 3.4

.. function:: get_context(method=None)

   Trả về một đối tượng context có các thuộc tính giống như
   mô-đun :mod:`!multiprocessing`.

   Nếu *method* là ``None`` thì context mặc định sẽ được trả về. Lưu ý rằng nếu phương thức start toàn cục chưa được đặt, thao tác này sẽ đặt nó thành mặc định của hệ thống. Xem :ref:`global-start-method` để biết thêm chi tiết. Nếu không, *method* phải là ``'fork'``, ``'spawn'`` hoặc ``'forkserver'``. :exc:`ValueError` sẽ được phát sinh nếu phương thức start được chỉ định không khả dụng. Xem :ref:`multiprocessing-start-methods`.

   .. versionadded:: 3.4

.. function:: get_start_method(allow_none=False)

   Trả về tên của phương thức start được sử dụng để khởi động các process.

   Nếu phương thức start toàn cục chưa được đặt và *allow_none* là ``False``, phương thức start toàn cục sẽ được đặt thành giá trị mặc định và tên của nó được trả về. Xem
   :ref:`global-start-method` để biết thêm chi tiết.

   Giá trị trả về có thể là ``'fork'``, ``'spawn'``, ``'forkserver'`` hoặc ``None``. Xem :ref:`multiprocessing-start-methods`.

   .. versionadded:: 3.4

   .. versionchanged:: 3.8

      Trên macOS, phương thức start *spawn* hiện là mặc định. Phương thức start *fork* nên được xem là không an toàn vì có thể khiến subprocess bị crash. Xem :issue:`33725`.

.. function:: set_executable(executable)

   Đặt đường dẫn đến trình thông dịch Python sẽ được sử dụng khi khởi động tiến trình con. (Theo mặc định, sử dụng :data:`sys.executable`). Các chương trình nhúng có thể sẽ cần thực hiện việc như sau::

      set_executable(os.path.join(sys.exec_prefix, 'pythonw.exe'))

   trước khi có thể tạo các tiến trình con.

   .. versionchanged:: 3.4
      Hiện được hỗ trợ trên POSIX khi sử dụng phương thức khởi động ``'spawn'``.

   .. versionchanged:: 3.11
      Nhận một :term:`path-like object`.

.. function:: set_forkserver_preload(module_names)

   Đặt danh sách tên mô-đun để tiến trình chính của forkserver cố gắng import, ताकि trạng thái đã import của chúng được các tiến trình fork kế thừa. Mọi :exc:`ImportError` xảy ra trong quá trình này sẽ bị bỏ qua một cách im lặng. Có thể sử dụng tùy chọn này để cải thiện hiệu năng bằng cách tránh thực hiện lặp lại công việc trong mỗi tiến trình.

   Để hoạt động, hàm này phải được gọi trước khi tiến trình forkserver được khởi chạy (trước khi tạo :class:`Pool` hoặc khởi động :class:`Process`).

   Chỉ có ý nghĩa khi sử dụng phương thức khởi động ``'forkserver'``. Xem :ref:`multiprocessing-start-methods`.

   .. versionadded:: 3.4

.. function:: set_start_method(method, force=False)

   Đặt phương thức sẽ được sử dụng để khởi động các tiến trình con. Đối số *method* có thể là ``'fork'``, ``'spawn'`` hoặc ``'forkserver'``. Gây ra :exc:`RuntimeError` nếu phương thức khởi động đã được đặt và *force* không phải là ``True``. Nếu *method* là ``None`` và *force* là ``True`` thì phương thức khởi động được đặt thành ``None``. Nếu *method* là ``None`` và *force* là ``False`` thì context được đặt thành context mặc định.

   Lưu ý rằng hàm này chỉ nên được gọi nhiều nhất một lần và nên được bảo vệ bên trong mệnh đề ``if __name__ == '__main__'`` của mô-đun chính.

   Xem :ref:`multiprocessing-start-methods`.

   .. versionadded:: 3.4

.. note::

   :mod:`!multiprocessing` không chứa các thành phần tương đương với
   :func:`threading.active_count`, :func:`threading.enumerate`,
   :func:`threading.settrace`, :func:`threading.setprofile`,
   :class:`threading.Timer` hoặc :class:`threading.local`.


Đối tượng kết nối
^^^^^^^^^^^^^^^^^

.. currentmodule:: multiprocessing.connection

Các đối tượng kết nối cho phép gửi và nhận các đối tượng có thể pickle hoặc các chuỗi. Có thể hình dung chúng như các socket được kết nối theo hướng thông điệp.

Các đối tượng Connection thường được tạo bằng
:func:`Pipe <multiprocessing.Pipe>` -- xem thêm
:ref:`multiprocessing-listeners-clients`.

.. class:: Connection

   .. method:: send(obj)

      Gửi một đối tượng đến đầu kia của kết nối; đối tượng này sẽ được đọc bằng :meth:`recv`.

      Đối tượng phải có thể pickle. Các pickle rất lớn (khoảng từ 32 MiB trở lên, tùy thuộc vào hệ điều hành) có thể gây ra ngoại lệ :exc:`ValueError`.

   .. method:: recv()

      Trả về một đối tượng được gửi từ đầu kia của kết nối bằng
      :meth:`send`. Chặn cho đến khi có dữ liệu để nhận. Gây ra
      :exc:`EOFError` nếu không còn gì để nhận và đầu kia đã bị đóng.

   .. method:: fileno()

      Trả về file descriptor hoặc handle được kết nối sử dụng.

   .. method:: close()

      Đóng kết nối.

      Thao tác này được tự động gọi khi kết nối được garbage collected.

   .. method:: poll([timeout])

      Cho biết có dữ liệu nào sẵn sàng để đọc hay không.

      Nếu *timeout* không được chỉ định thì hàm sẽ trả về ngay lập tức.  Nếu *timeout* là một số thì giá trị này chỉ định thời gian tối đa tính bằng giây mà hàm sẽ chờ.  Nếu *timeout* là ``None`` thì sẽ sử dụng thời gian chờ vô hạn.

      Lưu ý rằng có thể poll nhiều đối tượng kết nối cùng lúc bằng cách sử dụng :func:`multiprocessing.connection.wait`.

   .. method:: send_bytes(buf[, offset[, size]])

      Gửi dữ liệu byte từ một :term:`bytes-like object` dưới dạng một message hoàn chỉnh.

      Nếu *offset* được cung cấp thì dữ liệu sẽ được đọc từ vị trí đó trong *buf*. Nếu *size* được cung cấp thì số byte tương ứng sẽ được đọc từ *buf*. Các buffer rất lớn (xấp xỉ từ 32 MiB trở lên, mặc dù còn tùy thuộc vào hệ điều hành) có thể phát sinh một
      :exc:`ValueError` ngoại lệ

   .. method:: recv_bytes([maxlength])

      Trả về toàn bộ thông báo chứa dữ liệu byte được gửi từ đầu kia của kết nối dưới dạng một chuỗi. Chặn cho đến khi có dữ liệu để nhận. Phát sinh :exc:`EOFError` nếu không còn gì để nhận và đầu kia đã đóng kết nối.

      Nếu *maxlength* được chỉ định và thông báo dài hơn *maxlength* thì :exc:`OSError` sẽ được phát sinh và kết nối sẽ không còn có thể đọc được.

      .. versionchanged:: 3.3
         Trước đây, hàm này phát sinh :exc:`IOError`, hiện là bí danh của :exc:`OSError`.


   .. method:: recv_bytes_into(buf[, offset])

      Đọc vào *buf* toàn bộ thông báo chứa dữ liệu byte được gửi từ đầu kia của kết nối và trả về số byte trong thông báo. Chặn cho đến khi có dữ liệu để nhận. Phát sinh
      :exc:`EOFError` nếu không còn gì để nhận và đầu kia đã bị đóng.

      *buf* phải là một :term:`bytes-like object` có thể ghi. Nếu *offset* được cung cấp thì thông báo sẽ được ghi vào bộ đệm từ vị trí đó. Offset phải là một số nguyên không âm nhỏ hơn độ dài của *buf* (tính bằng byte).

      Nếu bộ đệm quá ngắn thì một ngoại lệ :exc:`BufferTooShort` sẽ được phát sinh và toàn bộ thông báo có sẵn dưới dạng ``e.args[0]``, trong đó ``e`` là thực thể ngoại lệ.

   .. versionchanged:: 3.3
      Bản thân các đối tượng Connection giờ đây có thể được truyền giữa các tiến trình bằng cách sử dụng :meth:`Connection.send` và :meth:`Connection.recv`.

      Các đối tượng Connection giờ đây cũng hỗ trợ giao thức quản lý ngữ cảnh -- xem
      :ref:`typecontextmanager`. :meth:`~contextmanager.__enter__` trả về đối tượng Connection, còn :meth:`~contextmanager.__exit__` gọi :meth:`close`.

Ví dụ:

.. doctest::

    >>> from multiprocessing import Pipe
    >>> a, b = Pipe()
    >>> a.send([1, 'hello', None])
    >>> b.recv()
    [1, 'hello', None]
    >>> b.send_bytes(b'thank you')
    >>> a.recv_bytes()
    b'thank you'
    >>> import array
    >>> arr1 = array.array('i', range(5))
    >>> arr2 = array.array('i', [0] * 10)
    >>> a.send_bytes(arr1)
    >>> count = b.recv_bytes_into(arr2)
    >>> assert count == len(arr1) * arr1.itemsize
    >>> arr2
    array('i', [0, 1, 2, 3, 4, 0, 0, 0, 0, 0])

.. _multiprocessing-recv-pickle-security:

.. warning::

    Phương thức :meth:`Connection.recv` tự động unpickle dữ liệu mà nó nhận được, điều này có thể gây rủi ro bảo mật trừ khi bạn có thể tin tưởng tiến trình đã gửi thông báo.

    Do đó, trừ khi đối tượng connection được tạo bằng :func:`Pipe`, bạn chỉ nên sử dụng các phương thức :meth:`~Connection.recv` và :meth:`~Connection.send` sau khi thực hiện một hình thức authentication nào đó. Xem
    :ref:`multiprocessing-auth-keys`.

.. warning::

    Nếu một process bị kết thúc trong khi đang cố đọc hoặc ghi vào pipe, dữ liệu trong pipe có khả năng bị hỏng, vì có thể không thể xác định chắc chắn ranh giới giữa các message.


Các primitive đồng bộ hóa
^^^^^^^^^^^^^^^^^^^^^^^^^

.. currentmodule:: multiprocessing

Nhìn chung, các primitive đồng bộ hóa không cần thiết trong chương trình multiprocess nhiều như trong chương trình multithread. Xem tài liệu về
module :mod:`threading`.

Lưu ý rằng bạn cũng có thể tạo các primitive đồng bộ hóa bằng cách sử dụng đối tượng manager -- xem :ref:`multiprocessing-managers`.

.. class:: Barrier(parties[, action[, timeout]])

   Một đối tượng barrier: bản sao của :class:`threading.Barrier`.

   Việc khởi tạo lớp này có thể thiết lập phương thức start toàn cục. Xem
   :ref:`global-start-method` để biết thêm chi tiết.

   .. versionadded:: 3.3

.. class:: BoundedSemaphore([value])

   Một đối tượng semaphore bị giới hạn: tương tự gần nhất của
   :class:`threading.BoundedSemaphore`.

   Việc khởi tạo lớp này có thể thiết lập phương thức start toàn cục. Xem
   :ref:`global-start-method` để biết thêm chi tiết.

   Chỉ có một điểm khác biệt so với đối tượng tương tự gần nhất: đối số đầu tiên của phương thức ``acquire`` có tên là *block*, phù hợp với :meth:`Lock.acquire`.

   .. method:: locked()

      Trả về một giá trị boolean cho biết liệu đối tượng này hiện có đang bị khóa hay không.

      .. versionadded:: 3.14

   .. note::
      Trên macOS, điều này không thể phân biệt được với :class:`Semaphore` vì ``sem_getvalue()`` chưa được triển khai trên nền tảng đó.

.. class:: Condition([lock])

   Một condition variable: bí danh của :class:`threading.Condition`.

   Nếu chỉ định *lock* thì đó phải là một đối tượng :class:`Lock` hoặc :class:`RLock` từ :mod:`!multiprocessing`.

   Việc khởi tạo lớp này có thể thiết lập phương thức start toàn cục. Xem
   :ref:`global-start-method` để biết thêm chi tiết.

   .. versionchanged:: 3.3
      Phương thức :meth:`~threading.Condition.wait_for` đã được thêm vào.

.. class:: Event()

   Một bản sao của :class:`threading.Event`.

   Việc khởi tạo lớp này có thể thiết lập phương thức start toàn cục. Xem
   :ref:`global-start-method` để biết thêm chi tiết.

.. class:: Lock()

   Một đối tượng khóa không đệ quy: tương tự gần nhất với :class:`threading.Lock`. Sau khi một tiến trình hoặc luồng đã lấy được khóa, mọi nỗ lực tiếp theo nhằm lấy khóa từ bất kỳ tiến trình hoặc luồng nào sẽ bị chặn cho đến khi khóa được giải phóng; bất kỳ tiến trình hoặc luồng nào cũng có thể giải phóng khóa. Các khái niệm và hành vi của
   :class:`threading.Lock` khi áp dụng cho các luồng được mô phỏng tại đây trong
   :class:`multiprocessing.Lock` khi áp dụng cho tiến trình hoặc luồng, ngoại trừ các trường hợp được lưu ý.

   Lưu ý rằng :class:`Lock` thực chất là một hàm factory trả về một thực thể của ``multiprocessing.synchronize.Lock`` được khởi tạo với một context mặc định.

   Việc khởi tạo lớp này có thể thiết lập phương thức start toàn cục. Xem
   :ref:`global-start-method` để biết thêm chi tiết.

   :class:`Lock` hỗ trợ giao thức :term:`context manager` và do đó có thể được sử dụng trong các câu lệnh :keyword:`with`.

   .. method:: acquire(block=True, timeout=None)

      Nhận một lock, theo cách chặn hoặc không chặn.

      Với đối số *block* được đặt thành ``True`` (mặc định), lệnh gọi phương thức sẽ chặn cho đến khi lock ở trạng thái không bị khóa, sau đó đặt lock về trạng thái đã khóa và trả về ``True``. Lưu ý rằng tên của đối số đầu tiên này khác với tên trong :meth:`threading.Lock.acquire`.

      Với đối số *block* được đặt thành ``False``, lệnh gọi phương thức không chặn. Nếu lock hiện đang ở trạng thái đã khóa, trả về ``False``; nếu không, đặt lock về trạng thái đã khóa và trả về ``True``.

      Khi được gọi với giá trị dấu phẩy động dương cho *timeout*, chặn trong nhiều nhất số giây được chỉ định bởi *timeout* miễn là không thể nhận lock. Các lần gọi với giá trị âm cho *timeout* tương đương với *timeout* bằng không. Các lần gọi với giá trị *timeout* là ``None`` (mặc định) sẽ đặt khoảng thời gian chờ thành vô hạn. Lưu ý rằng cách xử lý các giá trị âm hoặc ``None`` của *timeout* khác với hành vi được triển khai trong
      :meth:`threading.Lock.acquire`. Đối số *timeout* không có tác dụng thực tế nếu đối số *block* được đặt thành ``False`` và do đó sẽ bị bỏ qua. Trả về ``True`` nếu đã nhận được lock hoặc ``False`` nếu khoảng thời gian chờ đã hết.


   .. method:: release()

      Giải phóng một lock. Có thể gọi hàm này từ bất kỳ process hoặc thread nào, không chỉ process hoặc thread đã lấy lock ban đầu.

      Hành vi giống như :meth:`threading.Lock.release`, ngoại trừ khi được gọi trên một lock chưa được khóa, hàm sẽ phát sinh :exc:`ValueError`.


   .. method:: locked()

      Trả về một giá trị boolean cho biết liệu đối tượng này hiện có đang bị khóa hay không.

      .. versionadded:: 3.14


.. class:: RLock()

   Một đối tượng recursive lock: tương tự như :class:`threading.RLock`. Recursive lock phải được process hoặc thread đã lấy nó giải phóng. Sau khi một process hoặc thread đã lấy recursive lock, chính process hoặc thread đó có thể lấy lại lock mà không bị chặn; process hoặc thread đó phải giải phóng lock một lần cho mỗi lần đã lấy lock.

   Lưu ý rằng :class:`RLock` thực chất là một factory function trả về một instance của ``multiprocessing.synchronize.RLock`` được khởi tạo với context mặc định.

   Việc khởi tạo lớp này có thể thiết lập phương thức start toàn cục. Xem
   :ref:`global-start-method` để biết thêm chi tiết.

   :class:`RLock` hỗ trợ giao thức :term:`context manager` và do đó có thể được sử dụng trong các câu lệnh :keyword:`with`.


   .. method:: acquire(block=True, timeout=None)

      Nhận một lock, theo cách chặn hoặc không chặn.

      Khi được gọi với đối số *block* được đặt thành ``True``, hãy chặn cho đến khi khóa ở trạng thái mở khóa (không do bất kỳ tiến trình hoặc thread nào sở hữu), trừ khi khóa đã được tiến trình hoặc thread hiện tại sở hữu. Khi đó, tiến trình hoặc thread hiện tại sẽ sở hữu khóa (nếu chưa sở hữu) và mức đệ quy bên trong khóa tăng lên một, dẫn đến giá trị trả về là ``True``. Lưu ý rằng hành vi của đối số thứ nhất này có một số điểm khác biệt so với cách triển khai của :meth:`threading.RLock.acquire`, bắt đầu từ chính tên của đối số.

      Khi được gọi với đối số *block* được đặt thành ``False``, không chặn. Nếu khóa đã được một tiến trình hoặc thread khác thu nhận (và do đó đang được sở hữu), tiến trình hoặc thread hiện tại không sở hữu khóa và mức đệ quy bên trong khóa không thay đổi, dẫn đến giá trị trả về là ``False``. Nếu khóa ở trạng thái mở khóa, tiến trình hoặc thread hiện tại sẽ sở hữu khóa và mức đệ quy tăng lên, dẫn đến giá trị trả về là ``True``.

      Cách sử dụng và hành vi của đối số *timeout* giống như trong
      :meth:`Lock.acquire`. Lưu ý rằng một số hành vi của *timeout* khác với các hành vi được triển khai trong :meth:`threading.RLock.acquire`.


   .. method:: release()

      Giải phóng khóa, giảm mức đệ quy. Nếu sau khi giảm, mức đệ quy bằng không, đặt lại khóa về trạng thái mở khóa (không do bất kỳ tiến trình hoặc thread nào sở hữu) và nếu có tiến trình hoặc thread khác đang bị chặn chờ khóa được mở khóa, cho phép chính xác một tiến trình hoặc thread trong số đó tiếp tục. Nếu sau khi giảm, mức đệ quy vẫn khác không, khóa vẫn bị khóa và do tiến trình hoặc thread đang gọi sở hữu.

      Chỉ gọi phương thức này khi process hoặc thread gọi nó đang sở hữu lock. Một :exc:`AssertionError` sẽ được raise nếu phương thức này được gọi bởi process hoặc thread không phải chủ sở hữu, hoặc nếu lock đang ở trạng thái chưa được khóa (không có chủ sở hữu). Lưu ý rằng loại exception được raise trong tình huống này khác với hành vi được triển khai trong :meth:`threading.RLock.release`.


   .. method:: locked()

      Trả về một giá trị boolean cho biết liệu đối tượng này hiện có đang bị khóa hay không.

      .. versionadded:: 3.14


.. class:: Semaphore([value])

   Một semaphore object: tương tự gần giống :class:`threading.Semaphore`.

   Việc khởi tạo lớp này có thể thiết lập phương thức start toàn cục. Xem
   :ref:`global-start-method` để biết thêm chi tiết.

   Chỉ có một điểm khác biệt so với đối tượng tương tự gần nhất: đối số đầu tiên của phương thức ``acquire`` có tên là *block*, phù hợp với :meth:`Lock.acquire`.


   .. method:: get_value()

      Trả về giá trị hiện tại của semaphore.

      Lưu ý rằng điều này có thể gây ra :exc:`NotImplementedError` trên các nền tảng như macOS, nơi ``sem_getvalue()`` chưa được triển khai.


   .. method:: locked()

      Trả về một giá trị boolean cho biết liệu đối tượng này hiện có đang bị khóa hay không.

      .. versionadded:: 3.14


.. note::

   Trên macOS, ``sem_timedwait`` không được hỗ trợ, vì vậy việc gọi ``acquire()`` với thời gian chờ sẽ mô phỏng hành vi của hàm đó bằng một vòng lặp tạm dừng.

.. note::

   Một số chức năng của gói này yêu cầu hệ điều hành máy chủ phải có triển khai semaphore dùng chung hoạt động được. Nếu không có, mô-đun
   :mod:`multiprocessing.synchronize` sẽ bị vô hiệu hóa và việc cố gắng nhập mô-đun này sẽ dẫn đến :exc:`ImportError`. Xem
   :issue:`3770` để biết thêm thông tin.


Các đối tượng :mod:`ctypes` dùng chung
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Có thể tạo các đối tượng dùng chung bằng bộ nhớ dùng chung, bộ nhớ này có thể được các tiến trình con kế thừa.

.. function:: Value(typecode_or_type, *args, lock=True)

   Trả về một đối tượng :mod:`ctypes` được cấp phát từ bộ nhớ dùng chung. Theo mặc định, giá trị trả về thực chất là một trình bao bọc được đồng bộ hóa cho đối tượng. Bản thân đối tượng có thể được truy cập thông qua thuộc tính *value* của một :class:`Value`.

   *typecode_or_type* xác định kiểu của đối tượng được trả về: đó có thể là một kiểu ctypes hoặc một typecode gồm một ký tự, thuộc loại được :mod:`array` module sử dụng. *\*args* được truyền cho hàm khởi tạo của kiểu đó.

   Nếu *lock* là ``True`` (mặc định) thì một đối tượng khóa đệ quy mới sẽ được tạo để đồng bộ hóa quyền truy cập vào giá trị. Nếu *lock* là một đối tượng :class:`Lock` hoặc :class:`RLock` thì đối tượng đó sẽ được dùng để đồng bộ hóa quyền truy cập vào giá trị. Nếu *lock* là ``False`` thì quyền truy cập vào đối tượng được trả về sẽ không được khóa tự động bảo vệ, vì vậy không nhất thiết phải "an toàn cho tiến trình".

   Các thao tác như ``+=`` có liên quan đến việc đọc và ghi không phải là nguyên tử. Vì vậy, chẳng hạn, nếu muốn tăng một giá trị dùng chung theo cách nguyên tử thì chỉ thực hiện::

       counter.value += 1

   Với điều kiện khóa liên kết là khóa đệ quy (theo mặc định là như vậy), thay vào đó bạn có thể thực hiện::

       with counter.get_lock():
           counter.value += 1

   Lưu ý rằng *lock* là một đối số chỉ dùng cho từ khóa.

.. function:: Array(typecode_or_type, size_or_initializer, *, lock=True)

   Trả về một mảng ctypes được cấp phát từ bộ nhớ dùng chung. Theo mặc định, giá trị trả về thực chất là một wrapper được đồng bộ hóa cho mảng.

   *typecode_or_type* xác định kiểu của các phần tử trong mảng được trả về: đó là một :ref:`ctypes type <ctypes-fundamental-data-types>` hoặc một typecode dài một ký tự thuộc loại được :mod:`array` module sử dụng, ngoại trừ ``'w'``, vốn không được hỗ trợ. Ngoài ra, typecode ``'c'`` là bí danh của :class:`ctypes.c_char`. Nếu *size_or_initializer* là một số nguyên thì nó xác định độ dài của mảng và mảng ban đầu sẽ được đặt toàn bộ về 0. Nếu không, *size_or_initializer* là một sequence được dùng để khởi tạo mảng, đồng thời độ dài của sequence này xác định độ dài của mảng.

   Nếu *lock* là ``True`` (mặc định), một đối tượng lock mới sẽ được tạo để đồng bộ hóa việc truy cập vào giá trị. Nếu *lock* là một :class:`Lock` hoặc
   :class:`RLock` object thì đối tượng đó sẽ được dùng để đồng bộ hóa việc truy cập vào giá trị. Nếu *lock* là ``False`` thì việc truy cập vào đối tượng được trả về sẽ không được tự động bảo vệ bằng lock, vì vậy không nhất thiết phải là "process-safe".

   Lưu ý rằng *lock* là một đối số chỉ dành cho keyword.

   Lưu ý rằng một mảng :data:`ctypes.c_char` có các thuộc tính *value* và *raw*, cả hai đều có thể được dùng để lưu trữ và truy xuất các chuỗi byte. Trong khi *raw* cho phép tương tác với một đối tượng :class:`bytes` có kích thước đầy đủ của mảng, việc đọc *value* sẽ kết thúc sau một byte null, giống như cách hầu hết các ngôn ngữ lập trình xử lý chuỗi.


Module :mod:`!multiprocessing.sharedctypes`
"""""""""""""""""""""""""""""""""""""""""""

.. module:: multiprocessing.sharedctypes
   :synopsis: Cấp phát các đối tượng ctypes từ bộ nhớ dùng chung.

Mô-đun :mod:`!multiprocessing.sharedctypes` cung cấp các hàm để cấp phát
các đối tượng :mod:`ctypes` từ bộ nhớ dùng chung, có thể được các tiến trình con kế thừa.

.. note::

   Mặc dù có thể lưu trữ một con trỏ trong bộ nhớ dùng chung, hãy nhớ rằng con trỏ này sẽ trỏ đến một vị trí trong không gian địa chỉ của một tiến trình cụ thể. Tuy nhiên, con trỏ này rất có thể không hợp lệ trong ngữ cảnh của tiến trình thứ hai, và việc cố gắng giải tham chiếu con trỏ từ tiến trình thứ hai có thể gây ra lỗi.

.. function:: RawArray(typecode_or_type, size_or_initializer)

   Trả về một mảng ctypes được cấp phát từ bộ nhớ dùng chung.

   *typecode_or_type* xác định kiểu của các phần tử trong mảng được trả về: đó là một kiểu ctypes hoặc một typecode gồm một ký tự thuộc loại được :mod:`array` module sử dụng. Nếu *size_or_initializer* là một số nguyên thì nó xác định độ dài của mảng, và mảng sẽ được khởi tạo bằng các giá trị 0. Nếu không, *size_or_initializer* là một sequence được dùng để khởi tạo mảng, và độ dài của sequence này xác định độ dài của mảng.

   Lưu ý rằng việc thiết lập và lấy một phần tử có thể không mang tính nguyên tử -- hãy sử dụng
   :func:`Array` thay vào đó để đảm bảo rằng quyền truy cập được tự động đồng bộ hóa bằng một khóa.

.. function:: RawValue(typecode_or_type, *args)

   Trả về một đối tượng ctypes được cấp phát từ bộ nhớ dùng chung.

   *typecode_or_type* xác định kiểu của đối tượng được trả về: đó là một kiểu ctypes hoặc một typecode gồm một ký tự, thuộc loại được :mod:`array` sử dụng.  *\*args* được truyền cho hàm khởi tạo của kiểu đó.

   Lưu ý rằng việc đặt và lấy giá trị có khả năng không nguyên tử -- hãy sử dụng
   :func:`Value` thay vào đó để đảm bảo rằng quyền truy cập được tự động đồng bộ hóa bằng một khóa.

   Lưu ý rằng một mảng :data:`ctypes.c_char` có các thuộc tính ``value`` và ``raw``, cho phép sử dụng nó để lưu trữ và truy xuất chuỗi -- xem tài liệu về :mod:`ctypes`.

.. function:: Array(typecode_or_type, size_or_initializer, *, lock=True, ctx=None)

   Tương tự như :func:`RawArray`, ngoại trừ việc tùy thuộc vào giá trị của *lock*, một wrapper đồng bộ hóa an toàn cho tiến trình có thể được trả về thay vì một mảng ctypes thô.

   Nếu *lock* là ``True`` (mặc định) thì một đối tượng lock mới sẽ được tạo để đồng bộ hóa quyền truy cập vào giá trị. Nếu *lock* là một
   :class:`~multiprocessing.Lock` hoặc đối tượng :class:`~multiprocessing.RLock` thì đối tượng đó sẽ được dùng để đồng bộ hóa quyền truy cập vào giá trị. Nếu *lock* là ``False`` thì quyền truy cập vào đối tượng được trả về sẽ không được bảo vệ tự động bằng lock, vì vậy không nhất thiết là "an toàn cho tiến trình" (process-safe).

   *ctx* là một đối tượng context hoặc ``None`` (sử dụng context hiện tại). Nếu ``None``, việc gọi hàm này có thể đặt start method toàn cục. Xem
   :ref:`global-start-method` để biết thêm chi tiết.

   Lưu ý rằng *lock* và *ctx* là các tham số chỉ có thể được truyền bằng từ khóa.

.. function:: Value(typecode_or_type, *args, lock=True, ctx=None)

   Tương tự như :func:`RawValue`, ngoại trừ việc tùy thuộc vào giá trị của *lock*, một wrapper đồng bộ hóa an toàn cho tiến trình có thể được trả về thay vì một đối tượng ctypes thô.

   Nếu *lock* là ``True`` (mặc định) thì một đối tượng lock mới sẽ được tạo để đồng bộ hóa quyền truy cập vào giá trị. Nếu *lock* là một :class:`~multiprocessing.Lock` hoặc
   :class:`~multiprocessing.RLock` đối tượng, sau đó đối tượng này sẽ được dùng để đồng bộ hóa quyền truy cập vào giá trị. Nếu *lock* là ``False`` thì quyền truy cập vào đối tượng được trả về sẽ không được bảo vệ tự động bằng lock, vì vậy không nhất thiết sẽ “an toàn cho process”.

   *ctx* là một đối tượng context hoặc ``None`` (sử dụng context hiện tại). Nếu ``None``, việc gọi hàm này có thể đặt start method toàn cục. Xem
   :ref:`global-start-method` để biết thêm chi tiết.

   Lưu ý rằng *lock* và *ctx* là các tham số chỉ có thể được truyền bằng từ khóa.

.. function:: copy(obj)

   Trả về một đối tượng ctypes được cấp phát từ shared memory, là bản sao của đối tượng ctypes *obj*.

.. function:: synchronized(obj, lock=None, ctx=None)

   Trả về một đối tượng wrapper an toàn cho process cho một đối tượng ctypes, sử dụng *lock* để đồng bộ hóa quyền truy cập. Nếu *lock* là ``None`` (mặc định) thì một
   :class:`multiprocessing.RLock` đối tượng sẽ được tự động tạo.

   *ctx* là một đối tượng context hoặc ``None`` (sử dụng context hiện tại). Nếu ``None``, việc gọi hàm này có thể đặt start method toàn cục. Xem
   :ref:`global-start-method` để biết thêm chi tiết.

   Một wrapper đồng bộ sẽ có hai phương thức, ngoài các phương thức của đối tượng mà nó bao bọc: :meth:`get_obj` trả về đối tượng được bao bọc và
   :meth:`get_lock` trả về đối tượng lock được dùng để đồng bộ hóa.

   Lưu ý rằng việc truy cập đối tượng ctypes thông qua wrapper có thể chậm hơn rất nhiều so với việc truy cập đối tượng ctypes thô.

   .. versionchanged:: 3.5
      Các đối tượng đồng bộ hỗ trợ protocol :term:`context manager`.


Bảng dưới đây so sánh cú pháp tạo các đối tượng shared ctypes từ shared memory với cú pháp ctypes thông thường. (Trong bảng, ``MyStruct`` là một lớp con của :class:`ctypes.Structure`.)

+----------------------+----------------------------+-------------------------------+
| ctypes               | sharedctypes sử dụng kiểu  | sharedctypes sử dụng typecode |
+======================+============================+===============================+
| c_double(2.4)        | RawValue(c_double, 2.4)    | RawValue('d', 2.4)            |
+----------------------+----------------------------+-------------------------------+
| MyStruct(4, 6)       | RawValue(MyStruct, 4, 6)   |                               |
+----------------------+----------------------------+-------------------------------+
| (c_short * 7)()      | RawArray(c_short, 7)       | RawArray('h', 7)              |
+----------------------+----------------------------+-------------------------------+
| (c_int * 3)(9, 2, 8) | RawArray(c_int, (9, 2, 8)) | RawArray('i', (9, 2, 8))      |
+----------------------+----------------------------+-------------------------------+


Dưới đây là một ví dụ trong đó một số đối tượng ctypes được sửa đổi bởi một tiến trình con::

   from multiprocessing import Process, Lock
   from multiprocessing.sharedctypes import Value, Array
   from ctypes import Structure, c_double

   class Point(Structure):
       _fields_ = [('x', c_double), ('y', c_double)]

   def modify(n, x, s, A):
       n.value **= 2
       x.value **= 2
       s.value = s.value.upper()
       for a in A:
           a.x **= 2
           a.y **= 2

   if __name__ == '__main__':
       lock = Lock()

       n = Value('i', 7)
       x = Value(c_double, 1.0/3.0, lock=False)
       s = Array('c', b'hello world', lock=lock)
       A = Array(Point, [(1.875,-6.25), (-5.75,2.0), (2.375,9.5)], lock=lock)

       p = Process(target=modify, args=(n, x, s, A))
       p.start()
       p.join()

       print(n.value)
       print(x.value)
       print(s.value)
       print([(a.x, a.y) for a in A])


.. highlight:: none

Kết quả được in ra là::

    49
    0.1111111111111111
    HELLO WORLD
    [(3.515625, 39.0625), (33.0625, 4.0), (5.640625, 90.25)]

.. highlight:: python3


.. _multiprocessing-managers:

Managers
^^^^^^^^

Manager cung cấp một cách để tạo dữ liệu có thể được chia sẻ giữa các process khác nhau, bao gồm cả việc chia sẻ qua mạng giữa các process chạy trên những máy khác nhau. Một manager object điều khiển một server process quản lý *các object được chia sẻ*. Các process khác có thể truy cập những object được chia sẻ bằng cách sử dụng proxy.

.. function:: multiprocessing.Manager()
   :module:

   Trả về một đối tượng :class:`~multiprocessing.managers.SyncManager` đã được khởi động, có thể được dùng để chia sẻ các đối tượng giữa các tiến trình. Đối tượng manager được trả về tương ứng với một tiến trình con được tạo và có các phương thức tạo các đối tượng được chia sẻ rồi trả về các proxy tương ứng.

.. module:: multiprocessing.managers
   :synopsis: Chia sẻ dữ liệu giữa các tiến trình bằng các đối tượng được chia sẻ.

Các tiến trình manager sẽ được tắt ngay khi chúng được thu gom rác hoặc khi tiến trình cha của chúng thoát. Các lớp manager được định nghĩa trong
:mod:`multiprocessing.managers` mô-đun:

.. class:: BaseManager(address=None, authkey=None, serializer='pickle', ctx=None, *, shutdown_timeout=1.0)

   Tạo một đối tượng BaseManager.

   Sau khi tạo, nên gọi :meth:`start` hoặc ``get_server().serve_forever()`` để đảm bảo rằng đối tượng manager tham chiếu đến một tiến trình manager đã khởi động.

   *address* là địa chỉ mà tiến trình manager lắng nghe các kết nối mới. Nếu *address* là ``None`` thì một địa chỉ bất kỳ sẽ được chọn.

   *authkey* là khóa xác thực được dùng để kiểm tra tính hợp lệ của các kết nối đến tiến trình máy chủ. Nếu *authkey* là ``None`` thì ``current_process().authkey`` được sử dụng. Nếu không, *authkey* được sử dụng và phải là một chuỗi byte.

   *serializer* phải là ``'pickle'`` (sử dụng cơ chế tuần tự hóa :mod:`pickle`) hoặc ``'xmlrpclib'`` (sử dụng cơ chế tuần tự hóa :mod:`xmlrpc.client`).

   *ctx* là một đối tượng context hoặc ``None`` (sử dụng context hiện tại). Nếu ``None``, việc gọi phương thức này có thể thiết lập phương thức khởi động toàn cục. Xem
   :ref:`global-start-method` để biết thêm chi tiết.

   *shutdown_timeout* là thời gian chờ tính bằng giây, được dùng để đợi cho đến khi tiến trình do manager sử dụng hoàn tất trong phương thức :meth:`shutdown`. Nếu hết thời gian chờ shutdown, tiến trình sẽ bị chấm dứt. Nếu thao tác chấm dứt tiến trình cũng hết thời gian chờ, tiến trình sẽ bị kill.

   .. versionchanged:: 3.11
      Đã thêm tham số *shutdown_timeout*.

   .. method:: start([initializer[, initargs]])

      Khởi động một subprocess để khởi động manager. Nếu *initializer* không phải là ``None`` thì subprocess sẽ gọi ``initializer(*initargs)`` khi khởi động.

   .. method:: get_server()

      Trả về một đối tượng :class:`Server`, đại diện cho server thực tế dưới sự điều khiển của Manager. Đối tượng :class:`Server` hỗ trợ
      phương thức :meth:`serve_forever`::

      >>> from multiprocessing.managers import BaseManager
      >>> manager = BaseManager(address=('', 50000), authkey=b'abc')
      >>> server = manager.get_server()
      >>> server.serve_forever()

      :class:`Server` cũng có một thuộc tính :attr:`address`.

   .. method:: connect()

      Kết nối một đối tượng manager cục bộ với một tiến trình manager từ xa::

      >>> from multiprocessing.managers import BaseManager
      >>> m = BaseManager(address=('127.0.0.1', 50000), authkey=b'abc')
      >>> m.connect()

   .. method:: shutdown()

      Dừng tiến trình được manager sử dụng. Tính năng này chỉ khả dụng nếu
      :meth:`start` đã được dùng để khởi động tiến trình server.

      Có thể gọi hàm này nhiều lần.

   .. method:: register(typeid[, callable[, proxytype[, exposed[, method_to_typeid[, create_method]]]]])

      Một classmethod có thể được dùng để đăng ký một kiểu hoặc callable với lớp manager.

      *typeid* là một "mã định danh kiểu" được dùng để xác định một kiểu cụ thể của đối tượng dùng chung. Giá trị này phải là một chuỗi.

      *callable* là một callable được dùng để tạo các đối tượng cho mã định danh kiểu này. Nếu một instance của manager sẽ được kết nối với server bằng phương thức :meth:`connect`, hoặc nếu đối số *create_method* là ``False`` thì có thể để giá trị này là ``None``.

      *proxytype* là một lớp con của :class:`BaseProxy`, được dùng để tạo proxy cho các đối tượng dùng chung có *typeid* này. Nếu ``None`` thì một lớp proxy sẽ được tự động tạo.

      *exposed* được dùng để chỉ định một chuỗi tên phương thức mà các proxy cho typeid này được phép truy cập bằng
      :meth:`BaseProxy._callmethod`.  (Nếu *exposed* là ``None`` thì
      :attr:`proxytype._exposed_` sẽ được sử dụng thay thế nếu tồn tại.) Trong trường hợp không chỉ định danh sách exposed, tất cả "public methods" của đối tượng dùng chung đều có thể được truy cập. (Ở đây, "public method" nghĩa là bất kỳ thuộc tính nào có phương thức :meth:`~object.__call__` và tên của thuộc tính đó không bắt đầu bằng ``'_'``.)

      *method_to_typeid* là một ánh xạ dùng để chỉ định kiểu trả về của những phương thức exposed cần trả về một proxy. Ánh xạ này liên kết tên phương thức với các chuỗi typeid. (Nếu *method_to_typeid* là ``None`` thì
      :attr:`proxytype._method_to_typeid_` sẽ được sử dụng thay thế nếu tồn tại.) Nếu tên của một phương thức không phải là khóa của ánh xạ này hoặc nếu ánh xạ là ``None`` thì đối tượng do phương thức trả về sẽ được sao chép theo giá trị.

      *create_method* xác định liệu một phương thức có nên được tạo với tên *typeid* hay không; phương thức này có thể được dùng để yêu cầu tiến trình máy chủ tạo một đối tượng dùng chung mới và trả về một proxy cho đối tượng đó. Theo mặc định, giá trị này là ``True``.

   Các instance của :class:`BaseManager` cũng có một thuộc tính chỉ đọc:

   .. attribute:: address

      Địa chỉ được manager sử dụng.

   .. versionchanged:: 3.3
      Các đối tượng Manager hỗ trợ context management protocol -- xem
      :ref:`typecontextmanager`.  :meth:`~contextmanager.__enter__` khởi động tiến trình server (nếu tiến trình này chưa được khởi động) rồi trả về đối tượng manager.  :meth:`~contextmanager.__exit__` gọi :meth:`shutdown`.

      Trong các phiên bản trước, :meth:`~contextmanager.__enter__` không khởi động tiến trình server của manager nếu tiến trình này chưa được khởi động.

.. class:: SyncManager

   Một lớp con của :class:`BaseManager` có thể được dùng để đồng bộ hóa các tiến trình. Các đối tượng thuộc kiểu này được trả về bởi
   :func:`multiprocessing.Manager`.

   Các phương thức của nó tạo và trả về :ref:`multiprocessing-proxy_objects` cho một số kiểu dữ liệu thường dùng cần được đồng bộ hóa giữa các tiến trình. Đáng chú ý trong số đó là các list và dictionary dùng chung.

   .. method:: Barrier(parties[, action[, timeout]])

      Tạo một đối tượng :class:`threading.Barrier` dùng chung và trả về một proxy cho đối tượng đó.

      .. versionadded:: 3.3

   .. method:: BoundedSemaphore([value])

      Tạo một đối tượng :class:`threading.BoundedSemaphore` dùng chung và trả về một proxy cho đối tượng đó.

   .. method:: Condition([lock])

      Tạo một đối tượng :class:`threading.Condition` dùng chung và trả về một proxy cho đối tượng đó.

      Nếu *lock* được cung cấp thì nó phải là một proxy cho một
      đối tượng :class:`threading.Lock` hoặc :class:`threading.RLock`.

      .. versionchanged:: 3.3
         Phương thức :meth:`~threading.Condition.wait_for` đã được thêm.

   .. method:: Event()

      Tạo một đối tượng :class:`threading.Event` dùng chung và trả về một proxy cho đối tượng đó.

   .. method:: Lock()

      Tạo một đối tượng :class:`threading.Lock` dùng chung và trả về một proxy cho đối tượng đó.

   .. method:: Namespace()

      Tạo một đối tượng :class:`Namespace` dùng chung và trả về một proxy cho đối tượng đó.

   .. method:: Queue([maxsize])

      Tạo một đối tượng :class:`queue.Queue` dùng chung và trả về một proxy cho đối tượng đó.

   .. method:: RLock()

      Tạo một đối tượng :class:`threading.RLock` dùng chung và trả về một proxy cho đối tượng đó.

   .. method:: Semaphore([value])

      Tạo một đối tượng :class:`threading.Semaphore` dùng chung và trả về một proxy cho đối tượng đó.

   .. method:: Array(typecode, sequence)

      Tạo một mảng và trả về một proxy cho mảng đó.

   .. method:: Value(typecode, value)

      Tạo một đối tượng có thuộc tính ``value`` có thể ghi và trả về một proxy cho đối tượng đó.

   .. method:: dict()
               dict(mapping) dict(sequence)

      Tạo một đối tượng :class:`dict` dùng chung và trả về một proxy cho đối tượng đó.

   .. method:: list()
               list(sequence)

      Tạo một đối tượng :class:`list` dùng chung và trả về một proxy cho đối tượng đó.

   .. method:: set()
               set(sequence) set(mapping)

      Tạo một đối tượng :class:`set` dùng chung và trả về một proxy cho đối tượng đó.

      .. versionadded:: 3.14
         :class:`set` support was added.

   .. versionchanged:: 3.6
      Các đối tượng dùng chung có thể được lồng nhau. Ví dụ: một đối tượng container dùng chung như một list dùng chung có thể chứa các đối tượng dùng chung khác, và tất cả sẽ được :class:`SyncManager` quản lý và đồng bộ hóa.

.. class:: Namespace

   Một kiểu có thể đăng ký với :class:`SyncManager`.

   Đối tượng namespace không có phương thức công khai, nhưng có các thuộc tính có thể ghi. Biểu diễn của đối tượng hiển thị các giá trị thuộc tính của nó.

   Tuy nhiên, khi sử dụng proxy cho một đối tượng namespace, một thuộc tính bắt đầu bằng ``'_'`` sẽ là thuộc tính của proxy, không phải thuộc tính của đối tượng được tham chiếu:

   .. doctest::

    >>> mp_context = multiprocessing.get_context('spawn')
    >>> manager = mp_context.Manager()
    >>> Global = manager.Namespace()
    >>> Global.x = 10
    >>> Global.y = 'hello'
    >>> Global._z = 12.3    # đây là thuộc tính của proxy
    >>> print(Global)
    Namespace(x=10, y='hello')


Các manager tùy chỉnh
"""""""""""""""""""""

Để tạo manager riêng, ta tạo một lớp con của :class:`BaseManager` và sử dụng classmethod :meth:`~BaseManager.register` để đăng ký các kiểu hoặc callable mới với lớp manager. Ví dụ::

   from multiprocessing.managers import BaseManager

   class MathsClass:
       def add(self, x, y):
           return x + y
       def mul(self, x, y):
           return x * y

   class MyManager(BaseManager):
       pass

   MyManager.register('Maths', MathsClass)

   if __name__ == '__main__':
       with MyManager() as manager:
           maths = manager.Maths()
           print(maths.add(4, 3))         # in ra 7
           print(maths.mul(7, 8))         # in ra 56


Sử dụng manager từ xa
"""""""""""""""""""""

Bạn có thể chạy một manager server trên một máy và cho phép các client sử dụng nó từ những máy khác (với điều kiện các firewall liên quan cho phép điều này).

Chạy các lệnh sau sẽ tạo một server cho một hàng đợi dùng chung duy nhất mà các client từ xa có thể truy cập::

   >>> from multiprocessing.managers import BaseManager
   >>> from queue import Queue
   >>> queue = Queue()
   >>> class QueueManager(BaseManager): pass
   >>> QueueManager.register('get_queue', callable=lambda:queue)
   >>> m = QueueManager(address=('', 50000), authkey=b'abracadabra')
   >>> s = m.get_server()
   >>> s.serve_forever()

Một client có thể truy cập server như sau::

   >>> from multiprocessing.managers import BaseManager
   >>> class QueueManager(BaseManager): pass
   >>> QueueManager.register('get_queue')
   >>> m = QueueManager(address=('foo.bar.org', 50000), authkey=b'abracadabra')
   >>> m.connect()
   >>> queue = m.get_queue()
   >>> queue.put('hello')

Một client khác cũng có thể sử dụng nó::

   >>> from multiprocessing.managers import BaseManager
   >>> class QueueManager(BaseManager): pass
   >>> QueueManager.register('get_queue')
   >>> m = QueueManager(address=('foo.bar.org', 50000), authkey=b'abracadabra')
   >>> m.connect()
   >>> queue = m.get_queue()
   >>> queue.get()
   'hello'

Các tiến trình cục bộ cũng có thể truy cập hàng đợi đó bằng cách sử dụng code ở trên phía client để truy cập từ xa::

    >>> from multiprocessing import Process, Queue
    >>> from multiprocessing.managers import BaseManager
    >>> class Worker(Process):
    ...     def __init__(self, q):
    ...         self.q = q
    ...         super().__init__()
    ...     def run(self):
    ...         self.q.put('local hello')
    ...
    >>> queue = Queue()
    >>> w = Worker(queue)
    >>> w.start()
    >>> class QueueManager(BaseManager): pass
    ...
    >>> QueueManager.register('get_queue', callable=lambda: queue)
    >>> m = QueueManager(address=('', 50000), authkey=b'abracadabra')
    >>> s = m.get_server()
    >>> s.serve_forever()

.. _multiprocessing-proxy_objects:

Đối tượng Proxy
^^^^^^^^^^^^^^^

Proxy là một đối tượng *tham chiếu* đến một đối tượng dùng chung, đối tượng này (có lẽ) nằm trong một process khác. Đối tượng dùng chung được gọi là *đối tượng được tham chiếu* của proxy. Nhiều đối tượng proxy có thể có cùng một đối tượng được tham chiếu.

Một đối tượng proxy có các phương thức gọi những phương thức tương ứng của đối tượng được tham chiếu (mặc dù không phải mọi phương thức của đối tượng được tham chiếu đều nhất thiết khả dụng thông qua proxy). Theo cách này, proxy có thể được sử dụng giống như đối tượng được tham chiếu:

.. doctest::

   >>> mp_context = multiprocessing.get_context('spawn')
   >>> manager = mp_context.Manager()
   >>> l = manager.list([i*i for i in range(10)])
   >>> print(l)
   [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
   >>> print(repr(l))
   <ListProxy object, typeid 'list' at 0x...>
   >>> l[4]
   16
   >>> l[2:5]
   [4, 9, 16]

Lưu ý rằng việc áp dụng :func:`str` cho một proxy sẽ trả về biểu diễn của đối tượng được tham chiếu, trong khi việc áp dụng :func:`repr` sẽ trả về biểu diễn của proxy.

Một đặc điểm quan trọng của các đối tượng proxy là chúng có thể được pickle, nên có thể truyền giữa các process. Vì vậy, một đối tượng được tham chiếu có thể chứa
:ref:`multiprocessing-proxy_objects`. Điều này cho phép lồng các list, dict và các :ref:`multiprocessing-proxy_objects` được quản lý khác:

.. doctest::

   >>> a = manager.list()
   >>> b = manager.list()
   >>> a.append(b)         # đối tượng được tham chiếu của a hiện chứa đối tượng được tham chiếu của b
   >>> print(a, b)
   [<ListProxy object, typeid 'list' at ...>] []
   >>> b.append('hello')
   >>> print(a[0], b)
   ['hello'] ['hello']

Tương tự, các proxy dict và list có thể được lồng vào nhau::

   >>> l_outer = manager.list([ manager.dict() for i in range(2) ])
   >>> d_first_inner = l_outer[0]
   >>> d_first_inner['a'] = 1
   >>> d_first_inner['b'] = 2
   >>> l_outer[1]['c'] = 3
   >>> l_outer[1]['z'] = 26
   >>> print(l_outer[0])
   {'a': 1, 'b': 2}
   >>> print(l_outer[1])
   {'c': 3, 'z': 26}

Nếu các đối tượng :class:`list` hoặc :class:`dict` tiêu chuẩn (không phải proxy) được chứa trong referent, các sửa đổi đối với những giá trị có thể thay đổi đó sẽ không được truyền qua manager vì proxy không có cách nào biết khi các giá trị bên trong được sửa đổi. Tuy nhiên, việc lưu một giá trị vào container proxy (kích hoạt ``__setitem__`` trên đối tượng proxy) sẽ truyền thay đổi qua manager; do đó, để sửa đổi một phần tử như vậy một cách hiệu quả, bạn có thể gán lại giá trị đã sửa đổi cho container proxy::

   # tạo một list proxy và thêm một đối tượng có thể thay đổi (một dictionary)
   lproxy = manager.list()
   lproxy.append({})
   # bây giờ thay đổi dictionary
   d = lproxy[0]
   d['a'] = 1
   d['b'] = 2
   # tại thời điểm này, các thay đổi đối với d vẫn chưa được đồng bộ, nhưng bằng cách
   # cập nhật dictionary, proxy sẽ được thông báo về thay đổi
   lproxy[0] = d

Cách tiếp cận này có lẽ kém thuận tiện hơn so với việc sử dụng các proxy lồng nhau
:ref:`multiprocessing-proxy_objects` cho hầu hết các trường hợp sử dụng, nhưng cũng thể hiện mức độ kiểm soát đối với việc đồng bộ hóa.

.. note::

   Các kiểu proxy trong :mod:`!multiprocessing` không hỗ trợ việc so sánh theo giá trị. Vì vậy, chẳng hạn, ta có:

   .. doctest::

       >>> manager.list([1,2,3]) == [1,2,3]
       False

   Thay vào đó, khi thực hiện so sánh, bạn chỉ nên sử dụng một bản sao của đối tượng được tham chiếu.

.. class:: BaseProxy

   Các đối tượng proxy là những thể hiện của các lớp con của :class:`BaseProxy`.

   .. method:: _callmethod(methodname[, args[, kwds]])

      Gọi một phương thức của đối tượng được proxy tham chiếu và trả về kết quả.

      Nếu ``proxy`` là một proxy có đối tượng được tham chiếu là ``obj`` thì biểu thức::

         proxy._callmethod(methodname, args, kwds)

      sẽ đánh giá biểu thức::

         getattr(obj, methodname)(*args, **kwds)

      trong tiến trình của manager.

      Giá trị được trả về sẽ là một bản sao của kết quả lời gọi hoặc một proxy tới một shared object mới -- xem tài liệu về đối số *method_to_typeid* của :meth:`BaseManager.register`.

      Nếu lời gọi phát sinh một ngoại lệ thì ngoại lệ đó sẽ được phát sinh lại bởi
      :meth:`_callmethod`. Nếu một ngoại lệ khác được phát sinh trong tiến trình của manager thì ngoại lệ này được chuyển thành ngoại lệ :exc:`RemoteError` và được phát sinh bởi :meth:`_callmethod`.

      Đặc biệt lưu ý rằng một ngoại lệ sẽ được phát sinh nếu *methodname* chưa được *exposed*.

      Ví dụ về cách sử dụng :meth:`_callmethod`:

      .. doctest::

         >>> l = manager.list(range(10))
         >>> l._callmethod('__len__')
         10
         >>> l._callmethod('__getitem__', (slice(2, 7),)) # tương đương với l[2:7]
         [2, 3, 4, 5, 6]
         >>> l._callmethod('__getitem__', (20,))          # tương đương với l[20]
         Traceback (most recent call last):
         ...
         IndexError: list index out of range

   .. method:: _getvalue()

      Trả về một bản sao của đối tượng được tham chiếu.

      Nếu đối tượng được tham chiếu không thể pickle thì thao tác này sẽ phát sinh ngoại lệ.

   .. method:: __repr__

      Trả về biểu diễn của đối tượng proxy.

   .. method:: __str__

      Trả về biểu diễn của đối tượng được tham chiếu.


Dọn dẹp
"""""""

Một đối tượng proxy sử dụng callback weakref để khi được garbage collector thu gom, nó sẽ tự hủy đăng ký khỏi manager sở hữu đối tượng được tham chiếu.

Một shared object sẽ bị xóa khỏi tiến trình manager khi không còn proxy nào tham chiếu đến nó.


Các pool tiến trình
^^^^^^^^^^^^^^^^^^^

.. module:: multiprocessing.pool
   :synopsis: Tạo các pool tiến trình.

Có thể tạo một pool tiến trình để thực hiện các tác vụ được gửi đến nó bằng lớp :class:`Pool`.

.. class:: Pool([processes[, initializer[, initargs[, maxtasksperchild [, context]]]]])

   Một đối tượng process pool điều khiển một pool gồm các worker process, nơi có thể gửi các job. Đối tượng này hỗ trợ kết quả bất đồng bộ với timeout và callback, đồng thời có một triển khai map song song.

   *processes* là số worker process cần sử dụng. Nếu *processes* là ``None`` thì số được :func:`os.process_cpu_count` trả về sẽ được sử dụng.

   Nếu *initializer* không phải là ``None`` thì mỗi worker process sẽ gọi ``initializer(*initargs)`` khi khởi động.

   *maxtasksperchild* là số lượng tác vụ mà một worker process có thể hoàn thành trước khi thoát và được thay thế bằng một worker process mới, nhằm giải phóng các tài nguyên không còn được sử dụng. Giá trị mặc định của *maxtasksperchild* là ``None``, nghĩa là các worker process sẽ tồn tại trong suốt thời gian hoạt động của pool.

   *context* có thể được sử dụng để chỉ định context dùng để khởi chạy các worker process. Thông thường, pool được tạo bằng hàm :func:`multiprocessing.Pool` hoặc phương thức :meth:`Pool` của một đối tượng context. Trong cả hai trường hợp, *context* được thiết lập phù hợp. Nếu ``None``, việc gọi hàm này sẽ có thêm tác dụng thiết lập start method toàn cục hiện tại nếu phương thức này chưa được thiết lập. Xem hàm :func:`get_context`.

   Lưu ý rằng các phương thức của đối tượng pool chỉ nên được gọi bởi process đã tạo pool.

   .. warning::
      :class:`multiprocessing.pool` objects have internal resources that need to be
      được quản lý đúng cách (giống như mọi tài nguyên khác) bằng cách sử dụng pool như một context manager hoặc gọi thủ công :meth:`close` và :meth:`terminate`. Nếu không làm vậy, process có thể bị treo trong quá trình hoàn tất.

      Lưu ý rằng **không đúng** khi dựa vào garbage collector để hủy pool, vì CPython không đảm bảo rằng finalizer của pool sẽ được gọi (xem :meth:`object.__del__` để biết thêm thông tin).

   .. versionchanged:: 3.2
      Đã thêm tham số *maxtasksperchild*.

   .. versionchanged:: 3.4
      Đã thêm tham số *context*.

   .. versionchanged:: 3.13
      *processes* sử dụng :func:`os.process_cpu_count` theo mặc định, thay vì
      :func:`os.cpu_count`.

   .. note::

      Các worker process trong một :class:`Pool` thường tồn tại trong toàn bộ thời gian hàng đợi công việc của Pool. Một mẫu thường gặp trong các hệ thống khác (chẳng hạn như Apache, mod_wsgi, v.v.) để giải phóng tài nguyên do các worker nắm giữ là cho phép một worker trong pool chỉ hoàn thành một lượng công việc nhất định trước khi thoát, được dọn dẹp và một process mới được tạo ra để thay thế process cũ. Đối số *maxtasksperchild* của :class:`Pool` cung cấp khả năng này cho người dùng cuối.

   .. method:: apply(func[, args[, kwds]])

      Gọi *func* với các đối số *args* và các đối số từ khóa *kwds*. Lệnh này sẽ chặn cho đến khi kết quả sẵn sàng. Vì thao tác này bị chặn, :meth:`apply_async` phù hợp hơn để thực hiện công việc song song. Ngoài ra, *func* chỉ được thực thi trong một worker của pool.

   .. method:: apply_async(func[, args[, kwds[, callback[, error_callback]]]])

      Một biến thể của phương thức :meth:`apply` trả về một
      :class:`~multiprocessing.pool.AsyncResult` đối tượng.

      Nếu *callback* được chỉ định thì đó phải là một callable chấp nhận một đối số. Khi kết quả sẵn sàng, *callback* sẽ được gọi với kết quả đó, trừ khi lệnh gọi thất bại; trong trường hợp đó, *error_callback* sẽ được gọi thay thế.

      Nếu *error_callback* được chỉ định thì đó phải là một callable chấp nhận một đối số. Nếu hàm đích thất bại, *error_callback* sẽ được gọi với instance của exception.

      Các callback nên hoàn tất ngay lập tức, vì nếu không, thread xử lý kết quả sẽ bị chặn.

   .. method:: map(func, iterable[, chunksize])

      Một phiên bản tương đương chạy song song của hàm dựng sẵn :func:`map` (tuy nhiên, hàm này chỉ hỗ trợ một đối số *iterable*; để sử dụng nhiều iterable, hãy xem :meth:`starmap`). Hàm này sẽ chặn cho đến khi kết quả sẵn sàng.

      Phương thức này chia iterable thành một số chunk rồi gửi chúng đến process pool dưới dạng các task riêng biệt. Có thể chỉ định kích thước (xấp xỉ) của các chunk này bằng cách đặt *chunksize* thành một số nguyên dương.

      Lưu ý rằng điều này có thể gây ra mức sử dụng bộ nhớ cao đối với các iterable rất dài. Hãy cân nhắc sử dụng :meth:`imap` hoặc :meth:`imap_unordered` với tùy chọn *chunksize* được chỉ định rõ ràng để đạt hiệu quả tốt hơn.

   .. method:: map_async(func, iterable[, chunksize[, callback[, error_callback]]])

      Một biến thể của phương thức :meth:`.map` trả về một
      :class:`~multiprocessing.pool.AsyncResult` đối tượng.

      Nếu *callback* được chỉ định thì đó phải là một callable chấp nhận một đối số. Khi kết quả sẵn sàng, *callback* sẽ được gọi với kết quả đó, trừ khi lệnh gọi thất bại; trong trường hợp đó, *error_callback* sẽ được gọi thay thế.

      Nếu *error_callback* được chỉ định thì đó phải là một callable chấp nhận một đối số. Nếu hàm đích thất bại, *error_callback* sẽ được gọi với instance của exception.

      Các callback nên hoàn tất ngay lập tức, vì nếu không, thread xử lý kết quả sẽ bị chặn.

   .. method:: imap(func, iterable[, chunksize])

      Một phiên bản dựa trên iterator của :meth:`.map`.

      Đối số *chunksize* giống với đối số được sử dụng bởi phương thức :meth:`.map`. Đối với các iterable rất dài, việc sử dụng giá trị lớn cho *chunksize* có thể giúp công việc hoàn tất **much** nhanh hơn đáng kể so với việc sử dụng giá trị mặc định là ``1``.

      Ngoài ra, nếu *chunksize* là ``1``, thì phương thức :meth:`!next` của iterator được trả về bởi phương thức :meth:`imap` có một tham số tùy chọn *timeout*: ``next(timeout)`` sẽ phát sinh :exc:`multiprocessing.TimeoutError` nếu không thể trả về kết quả trong vòng *timeout* giây.

   .. method:: imap_unordered(func, iterable[, chunksize])

      Tương tự :meth:`imap`, ngoại trừ việc thứ tự các kết quả từ iterator được trả về nên được xem là tùy ý. (Chỉ khi có duy nhất một worker process thì thứ tự mới được đảm bảo là "đúng".)

   .. method:: starmap(func, iterable[, chunksize])

      Tương tự :meth:`~multiprocessing.pool.Pool.map`, ngoại trừ việc các phần tử của *iterable* được kỳ vọng là các iterable sẽ được unpack thành các đối số.

      Do đó, một *iterable* của ``[(1,2), (3, 4)]`` sẽ cho kết quả là ``[func(1,2), func(3,4)]``.

      .. versionadded:: 3.3

   .. method:: starmap_async(func, iterable[, chunksize[, callback[, error_callback]]])

      Sự kết hợp giữa :meth:`starmap` và :meth:`map_async`, lặp qua *iterable* gồm các iterable và gọi *func* với các iterable được unpack. Trả về một đối tượng kết quả.

      .. versionadded:: 3.3

   .. method:: close()

      Ngăn không cho gửi thêm task nào đến pool. Sau khi tất cả task hoàn tất, các worker process sẽ thoát.

   .. method:: terminate()

      Dừng ngay các worker process mà không hoàn thành công việc đang chờ. Khi đối tượng pool được garbage collect, :meth:`terminate` sẽ được gọi ngay lập tức.

   .. method:: join()

      Chờ các worker process thoát. Phải gọi :meth:`close` hoặc
      :meth:`terminate` trước khi sử dụng :meth:`join`.

   .. versionchanged:: 3.3
      Các đối tượng Pool hiện hỗ trợ context management protocol -- xem
      :ref:`typecontextmanager`.  :meth:`~contextmanager.__enter__` trả về đối tượng pool, còn :meth:`~contextmanager.__exit__` gọi :meth:`terminate`.


.. class:: AsyncResult

   Lớp của kết quả được :meth:`Pool.apply_async` trả về và
   :meth:`Pool.map_async`.

   .. method:: get([timeout])

      Trả về kết quả khi kết quả có sẵn.  Nếu *timeout* không phải là ``None`` và kết quả không xuất hiện trong vòng *timeout* giây thì
      :exc:`multiprocessing.TimeoutError` được đưa ra.  Nếu lệnh gọi từ xa đưa ra một ngoại lệ thì ngoại lệ đó sẽ được :meth:`get` đưa ra lại.

   .. method:: wait([timeout])

      Chờ cho đến khi kết quả có sẵn hoặc cho đến khi *timeout* giây trôi qua.

   .. method:: ready()

      Trả về việc lệnh gọi đã hoàn tất hay chưa.

   .. method:: successful()

      Trả về việc lệnh gọi đã hoàn tất mà không đưa ra ngoại lệ hay chưa.  Sẽ đưa ra :exc:`ValueError` nếu kết quả chưa sẵn sàng.

      .. versionchanged:: 3.7
         Nếu kết quả chưa sẵn sàng, :exc:`ValueError` sẽ được raised thay vì
         :exc:`AssertionError`.

Ví dụ sau minh họa cách sử dụng một pool::

   from multiprocessing import Pool
   import time

   def f(x):
       return x*x

   if __name__ == '__main__':
       with Pool(processes=4) as pool:         # khởi động 4 worker process
           result = pool.apply_async(f, (10,)) # đánh giá "f(10)" một cách bất đồng bộ trong một process duy nhất
           print(result.get(timeout=1))        # in "100" trừ khi máy tính của bạn *cực kỳ* chậm

           print(pool.map(f, range(10)))       # in "[0, 1, 4,..., 81]"

           it = pool.imap(f, range(10))
           print(next(it))                     # in "0"
           print(next(it))                     # in "1"
           print(it.next(timeout=1))           # in "4" trừ khi máy tính của bạn *rất* chậm

           result = pool.apply_async(time.sleep, (10,))
           print(result.get(timeout=1))        # phát sinh multiprocessing.TimeoutError


.. _multiprocessing-listeners-clients:

Listeners và Clients
^^^^^^^^^^^^^^^^^^^^

.. module:: multiprocessing.connection
   :synopsis: API để làm việc với socket.

Thông thường, việc truyền thông điệp giữa các tiến trình được thực hiện bằng queue hoặc bằng cách sử dụng
:class:`~Connection` các đối tượng được trả về bởi
:func:`~multiprocessing.Pipe`.

Tuy nhiên, mô-đun :mod:`!multiprocessing.connection` cho phép linh hoạt hơn. Về cơ bản, mô-đun này cung cấp một API cấp cao hướng thông điệp để làm việc với socket hoặc named pipe của Windows. Mô-đun này cũng hỗ trợ *digest authentication* bằng mô-đun :mod:`hmac`, cũng như hỗ trợ polling nhiều kết nối cùng lúc.


.. function:: deliver_challenge(connection, authkey)

   Gửi một thông điệp được tạo ngẫu nhiên đến đầu bên kia của kết nối và chờ phản hồi.

   Nếu phản hồi khớp với digest của thông điệp khi sử dụng *authkey* làm khóa thì một thông điệp chào mừng sẽ được gửi đến đầu bên kia của kết nối. Nếu không thì
   :exc:`~multiprocessing.AuthenticationError` được phát sinh.

.. function:: answer_challenge(connection, authkey)

   Nhận một thông điệp, tính digest của thông điệp bằng *authkey* làm khóa, sau đó gửi digest trở lại.

   Nếu không nhận được thông điệp chào mừng thì
   :exc:`~multiprocessing.AuthenticationError` được phát sinh.

.. function:: Client(address[, family[, authkey]])

   Thử thiết lập kết nối tới listener đang sử dụng địa chỉ *address*, trả về một :class:`~Connection`.

   Loại kết nối được xác định bởi đối số *family*, nhưng nhìn chung có thể bỏ qua đối số này vì thường có thể suy ra từ định dạng của *address*. (Xem :ref:`multiprocessing-address-formats`)

   Nếu *authkey* được cung cấp và không phải là ``None``, thì giá trị này phải là một chuỗi byte và sẽ được dùng làm khóa bí mật cho thử thách xác thực dựa trên HMAC. Không thực hiện xác thực nếu *authkey* là ``None``.
   :exc:`~multiprocessing.AuthenticationError` được phát sinh nếu xác thực thất bại. Xem :ref:`multiprocessing-auth-keys`.

.. class:: Listener([address[, family[, backlog[, authkey]]]])

   Một wrapper cho socket đã liên kết hoặc named pipe của Windows đang 'lắng nghe' các kết nối.

   *address* là địa chỉ được sử dụng bởi socket đã liên kết hoặc named pipe của đối tượng listener.

   .. note::

      Nếu sử dụng địa chỉ '0.0.0.0', địa chỉ này sẽ không phải là một điểm cuối có thể kết nối trên Windows. Nếu cần một điểm cuối có thể kết nối, bạn nên sử dụng '127.0.0.1'.

   *family* là loại socket (hoặc named pipe) cần sử dụng. Giá trị này có thể là một trong các chuỗi ``'AF_INET'`` (cho socket TCP), ``'AF_UNIX'`` (cho Unix domain socket) hoặc ``'AF_PIPE'`` (cho Windows named pipe). Trong số đó, chỉ giá trị đầu tiên được đảm bảo luôn khả dụng. Nếu *family* là ``None`` thì family được suy ra từ định dạng của *address*. Nếu *address* cũng là ``None`` thì một giá trị mặc định sẽ được chọn. Giá trị mặc định này là family được giả định là nhanh nhất trong các family hiện có. Xem
   :ref:`multiprocessing-address-formats`. Lưu ý rằng nếu *family* là ``'AF_UNIX'`` và address là ``None`` thì socket sẽ được tạo trong một thư mục tạm riêng được tạo bằng :func:`tempfile.mkstemp`.

   Nếu listener object sử dụng socket thì *backlog* (mặc định là 1) sẽ được truyền cho phương thức :meth:`~socket.socket.listen` của socket sau khi socket được bind.

   Nếu *authkey* được cung cấp và không phải là ``None``, thì giá trị này phải là một chuỗi byte và sẽ được dùng làm khóa bí mật cho thử thách xác thực dựa trên HMAC. Không thực hiện xác thực nếu *authkey* là ``None``.
   :exc:`~multiprocessing.AuthenticationError` được phát sinh nếu xác thực thất bại. Xem :ref:`multiprocessing-auth-keys`.

   .. method:: accept()

      Chấp nhận một kết nối trên socket đã bind hoặc named pipe của listener object và trả về một :class:`~Connection` object. Nếu quá trình xác thực được thực hiện nhưng thất bại thì
      :exc:`~multiprocessing.AuthenticationError` được phát sinh.

   .. method:: close()

      Đóng socket đã liên kết hoặc named pipe của đối tượng listener. Thao tác này được tự động gọi khi listener được thu gom rác. Tuy nhiên, bạn nên gọi nó một cách tường minh.

   Đối tượng listener có các thuộc tính chỉ đọc sau:

   .. attribute:: address

      Địa chỉ đang được đối tượng Listener sử dụng.

   .. attribute:: last_accepted

      Địa chỉ mà từ đó kết nối được chấp nhận gần đây nhất đến. Nếu không lấy được địa chỉ này thì đó là ``None``.

   .. versionchanged:: 3.3
      Các đối tượng listener hiện hỗ trợ context management protocol -- xem
      :ref:`typecontextmanager`. :meth:`~contextmanager.__enter__` trả về đối tượng listener, còn :meth:`~contextmanager.__exit__` gọi :meth:`close`.

.. function:: wait(object_list, timeout=None)

   Chờ cho đến khi một đối tượng trong *object_list* sẵn sàng. Trả về danh sách các đối tượng trong *object_list* đang sẵn sàng. Nếu *timeout* là một số thực thì lệnh gọi sẽ chặn tối đa trong khoảng thời gian đó, tính bằng giây. Nếu *timeout* là ``None`` thì lệnh gọi sẽ chặn trong thời gian không giới hạn. Timeout âm tương đương với timeout bằng không.

   Đối với cả POSIX và Windows, một đối tượng có thể xuất hiện trong *object_list* nếu đó là

   * một đối tượng :class:`~multiprocessing.connection.Connection` có thể đọc được;
   * một đối tượng :class:`socket.socket` đã kết nối và có thể đọc được; hoặc
   * thuộc tính :attr:`~multiprocessing.Process.sentinel` của một
     :class:`~multiprocessing.Process` đối tượng.

   Một đối tượng kết nối hoặc socket ở trạng thái sẵn sàng khi có dữ liệu để đọc từ nó hoặc đầu bên kia đã đóng kết nối.

   **POSIX**: ``wait(object_list, timeout)`` gần như tương đương ``select.select(object_list, [], [], timeout)``.  Điểm khác biệt là nếu :func:`select.select` bị gián đoạn bởi một signal, nó có thể phát sinh :exc:`OSError` với số lỗi là ``EINTR``, trong khi
   :func:`wait` sẽ không.

   **Windows**: Một mục trong *object_list* phải là một integer handle có thể chờ được (theo định nghĩa được sử dụng trong tài liệu của hàm Win32 ``WaitForMultipleObjects()``) hoặc có thể là một object có phương thức :meth:`~io.IOBase.fileno` trả về socket handle hoặc pipe handle. (Lưu ý rằng pipe handle và socket handle là các handle **not** có thể chờ được.)

   .. versionadded:: 3.3


**Ví dụ**

Đoạn mã server sau đây tạo một listener sử dụng ``'secret password'`` làm khóa xác thực. Sau đó, nó chờ một kết nối và gửi một số dữ liệu đến client::

   from multiprocessing.connection import Listener
   from array import array

   address = ('localhost', 6000)     # family được suy ra là 'AF_INET'

   with Listener(address, authkey=b'secret password') as listener:
       with listener.accept() as conn:
           print('connection accepted from', listener.last_accepted)

           conn.send([2.25, None, 'junk', float])

           conn.send_bytes(b'hello')

           conn.send_bytes(array('i', [42, 1729]))

Đoạn mã sau đây kết nối đến server và nhận một số dữ liệu từ server::

   from multiprocessing.connection import Client
   from array import array

   address = ('localhost', 6000)

   with Client(address, authkey=b'secret password') as conn:
       print(conn.recv())                  # => [2.25, None, 'junk', float]

       print(conn.recv_bytes())            # => 'hello'

       arr = array('i', [0, 0, 0, 0, 0])
       print(conn.recv_bytes_into(arr))    # => 8
       print(arr)                          # => array('i', [42, 1729, 0, 0, 0])

Đoạn mã sau sử dụng :func:`~multiprocessing.connection.wait` để chờ thông báo từ nhiều tiến trình cùng lúc::

   from multiprocessing import Process, Pipe, current_process
   from multiprocessing.connection import wait

   def foo(w):
       for i in range(10):
           w.send((i, current_process().name))
       w.close()

   if __name__ == '__main__':
       readers = []

       for i in range(4):
           r, w = Pipe(duplex=False)
           readers.append(r)
           p = Process(target=foo, args=(w,))
           p.start()
           # Bây giờ chúng ta đóng đầu có thể ghi của pipe để chắc chắn rằng
           # p là tiến trình duy nhất sở hữu một handle cho đầu này. Điều này
           # đảm bảo rằng khi p đóng handle của nó đối với đầu có thể ghi,
           # wait() sẽ nhanh chóng báo cáo rằng đầu có thể đọc đã sẵn sàng.
           w.close()

       while readers:
           for r in wait(readers):
               try:
                   msg = r.recv()
               except EOFError:
                   readers.remove(r)
               else:
                   print(msg)


.. _multiprocessing-address-formats:

Định dạng địa chỉ
"""""""""""""""""

* Địa chỉ ``'AF_INET'`` là một tuple có dạng ``(hostname, port)``, trong đó *hostname* là một chuỗi và *port* là một số nguyên.

* Địa chỉ ``'AF_UNIX'`` là một chuỗi biểu diễn tên tệp trên hệ thống tệp.

* Địa chỉ ``'AF_PIPE'`` là một chuỗi có dạng
  :samp:`r'\\\\\\.\\pipe\\\\{PipeName}'`.  Để sử dụng :func:`Client` kết nối đến một named pipe trên máy tính từ xa có tên là *ServerName*, cần sử dụng địa chỉ có dạng :samp:`r'\\\\\\\\{ServerName}\\pipe\\\\{PipeName}'` thay thế.

Lưu ý rằng mọi chuỗi bắt đầu bằng hai dấu gạch chéo ngược theo mặc định đều được coi là địa chỉ ``'AF_PIPE'`` thay vì địa chỉ ``'AF_UNIX'``.


.. _multiprocessing-auth-keys:

Khóa xác thực
^^^^^^^^^^^^^

Khi sử dụng :meth:`Connection.recv <Connection.recv>`, dữ liệu nhận được sẽ tự động được unpickle. Đáng tiếc là việc unpickle dữ liệu từ nguồn không đáng tin cậy tiềm ẩn rủi ro bảo mật. Vì vậy, :class:`Listener` và :func:`Client` sử dụng module :mod:`hmac` để cung cấp cơ chế xác thực digest.

Khóa xác thực là một chuỗi byte có thể được xem như một mật khẩu: sau khi kết nối được thiết lập, cả hai đầu sẽ yêu cầu bằng chứng rằng đầu kia biết khóa xác thực. (Việc chứng minh rằng cả hai đầu đang sử dụng cùng một khóa **không** đòi hỏi phải gửi khóa qua kết nối.)

Nếu xác thực được yêu cầu nhưng không chỉ định khóa xác thực thì giá trị trả về của ``current_process().authkey`` sẽ được sử dụng (xem
:class:`~multiprocessing.Process`). Giá trị này sẽ được mọi đối tượng :class:`~multiprocessing.Process` mà tiến trình hiện tại tạo ra tự động kế thừa. Điều này có nghĩa là (theo mặc định) mọi tiến trình của một chương trình đa tiến trình sẽ dùng chung một khóa xác thực, có thể được sử dụng khi thiết lập các kết nối giữa chúng.

Bạn cũng có thể tạo các khóa xác thực phù hợp bằng cách sử dụng :func:`os.urandom`.

Cơ chế xác thực này bảo vệ các kết nối :class:`Listener` và :func:`Client`, vốn có thể được truy cập bằng địa chỉ. Cơ chế này không được áp dụng cho các pipe ẩn danh do :func:`~multiprocessing.Pipe` tạo ra hoặc được sử dụng nội bộ bởi
:class:`~multiprocessing.Queue`.
:mod:`multiprocessing` xem mọi tiến trình cục bộ chạy với cùng một người dùng là đáng tin cậy; trên hầu hết các hệ điều hành, các tiến trình như vậy vốn có thể truy cập bộ mô tả pipe của nhau. Các ứng dụng yêu cầu sự cô lập giữa những tiến trình của cùng một người dùng phải thực hiện việc đó ở cấp hệ điều hành -- chẳng hạn bằng cách chạy worker dưới một tài khoản người dùng khác hoặc trong một sandbox.


Ghi nhật ký
^^^^^^^^^^^

Có hỗ trợ ghi nhật ký ở mức nhất định. Tuy nhiên, lưu ý rằng gói :mod:`logging` không sử dụng các khóa dùng chung giữa các process, vì vậy (tùy thuộc vào loại handler) các thông báo từ những process khác nhau có thể bị trộn lẫn.

.. currentmodule:: multiprocessing
.. function:: get_logger()

   Trả về logger được :mod:`!multiprocessing` sử dụng. Nếu cần, một logger mới sẽ được tạo.

   Khi mới được tạo, logger có level :const:`logging.NOTSET` và không có handler mặc định. Theo mặc định, các thông báo gửi đến logger này sẽ không được truyền đến root logger.

   Lưu ý rằng trên Windows, các process con chỉ kế thừa level của logger trong process cha -- mọi tùy chỉnh khác của logger sẽ không được kế thừa.

.. currentmodule:: multiprocessing
.. function:: log_to_stderr(level=None)

   Hàm này thực hiện một lệnh gọi đến :func:`get_logger`, nhưng ngoài việc trả về logger do get_logger tạo, nó còn thêm một handler gửi đầu ra đến :data:`sys.stderr` bằng format ``'[%(levelname)s/%(processName)s] %(message)s'``. Bạn có thể sửa đổi ``levelname`` của logger bằng cách truyền một đối số ``level``.

Dưới đây là một phiên làm việc mẫu khi bật tính năng ghi nhật ký::

    >>> import multiprocessing, logging
    >>> logger = multiprocessing.log_to_stderr()
    >>> logger.setLevel(logging.INFO)
    >>> logger.warning('doomed')
    [WARNING/MainProcess] doomed
    >>> m = multiprocessing.Manager()
    [INFO/SyncManager-...] child process calling self.run()
    [INFO/SyncManager-...] created temp directory /.../pymp-...
    [INFO/SyncManager-...] manager serving at '/.../listener-...'
    >>> del m
    [INFO/MainProcess] sending shutdown message to manager
    [INFO/SyncManager-...] manager exiting with exitcode 0

Để xem bảng đầy đủ về các cấp độ logging, hãy xem mô-đun :mod:`logging`.


Mô-đun :mod:`!multiprocessing.dummy`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. module:: multiprocessing.dummy
   :synopsis: Lớp bọc đơn giản quanh threading.

:mod:`!multiprocessing.dummy` tái tạo API của :mod:`!multiprocessing` nhưng không hơn gì một lớp bọc quanh mô-đun :mod:`threading`.

.. currentmodule:: multiprocessing.pool

Cụ thể, hàm ``Pool`` do :mod:`!multiprocessing.dummy` cung cấp trả về một thực thể của :class:`ThreadPool`, là một lớp con của
:class:`Pool` hỗ trợ tất cả các lời gọi phương thức tương tự nhưng sử dụng một pool của các worker thread thay vì các worker process.


.. class:: ThreadPool([processes[, initializer[, initargs]]])

   Một đối tượng thread pool điều khiển một pool gồm các worker thread để nhận những công việc được gửi đến. Các thực thể :class:`ThreadPool` hoàn toàn tương thích về giao diện với các thực thể :class:`Pool`, và tài nguyên của chúng cũng phải được quản lý đúng cách, bằng cách sử dụng pool như một context manager hoặc gọi :meth:`~multiprocessing.pool.Pool.close` và
   :meth:`~multiprocessing.pool.Pool.terminate` theo cách thủ công.

   *processes* là số lượng luồng worker cần sử dụng. Nếu *processes* là ``None`` thì giá trị do :func:`os.process_cpu_count` trả về được sử dụng.

   Nếu *initializer* không phải là ``None`` thì mỗi tiến trình worker sẽ gọi ``initializer(*initargs)`` khi khởi động.

   Không giống :class:`Pool`, không thể cung cấp *maxtasksperchild* và *context*.

   .. note::

      Một :class:`ThreadPool` có cùng giao diện với :class:`Pool`, vốn được thiết kế xoay quanh một pool các tiến trình và có trước khi giới thiệu :class:`concurrent.futures` module. Vì vậy, nó kế thừa một số thao tác không phù hợp với pool được hỗ trợ bởi các luồng, đồng thời có kiểu riêng để biểu diễn trạng thái của các job bất đồng bộ,
      :class:`AsyncResult`, mà không thư viện nào khác hiểu được.

      Nhìn chung, người dùng nên ưu tiên sử dụng
      :class:`concurrent.futures.ThreadPoolExecutor`, có giao diện đơn giản hơn được thiết kế ngay từ đầu dựa trên các thread và trả về các instance :class:`concurrent.futures.Future` tương thích với nhiều thư viện khác, bao gồm cả :mod:`asyncio`.


.. _multiprocessing-programming:

Hướng dẫn lập trình
-------------------

Có một số hướng dẫn và quy ước cần tuân thủ khi sử dụng
:mod:`!multiprocessing`.


Tất cả phương thức khởi động
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Những điều sau đây áp dụng cho tất cả các phương thức khởi động.

Tránh trạng thái dùng chung

    Trong phạm vi có thể, nên cố gắng tránh chuyển một lượng lớn dữ liệu giữa các tiến trình.

    Có lẽ tốt nhất là dùng queue hoặc pipe để giao tiếp giữa các tiến trình thay vì sử dụng các primitive đồng bộ hóa cấp thấp hơn.

Khả năng pickle hóa

    Đảm bảo các đối số truyền cho các phương thức của proxy có thể pickle hóa.

Tính an toàn luồng của proxy

    Không sử dụng đối tượng proxy từ nhiều thread, trừ khi bạn bảo vệ nó bằng một lock.

    (Không bao giờ có vấn đề khi các tiến trình khác nhau sử dụng cùng một proxy *same*.)

Chờ các tiến trình zombie

    Trên POSIX, khi một process kết thúc nhưng chưa được join, nó sẽ trở thành zombie. Số lượng zombie không bao giờ nên quá nhiều, vì mỗi khi một process mới khởi chạy (hoặc
    :func:`~multiprocessing.active_children` được gọi), tất cả các process đã hoàn tất nhưng chưa được join sẽ được join. Ngoài ra, việc gọi :meth:`Process.is_alive <multiprocessing.Process.is_alive>` của một process đã hoàn tất cũng sẽ join process đó. Dù vậy, việc chủ động join tất cả các process mà bạn khởi chạy vẫn được xem là một thực hành tốt.

Nên kế thừa thay vì pickle/unpickle

    Khi sử dụng phương thức khởi chạy *spawn* hoặc *forkserver*, nhiều kiểu từ :mod:`!multiprocessing` cần có khả năng pickle để các process con có thể sử dụng chúng. Tuy nhiên, nhìn chung bạn nên tránh gửi các đối tượng dùng chung đến các process khác bằng pipe hoặc queue. Thay vào đó, hãy tổ chức chương trình sao cho một process cần truy cập tài nguyên dùng chung được tạo ở nơi khác có thể kế thừa tài nguyên đó từ một process tổ tiên.

Tránh kết thúc process

    Việc sử dụng phương thức :meth:`Process.terminate <multiprocessing.Process.terminate>` để dừng một process có thể khiến mọi tài nguyên dùng chung (chẳng hạn như lock, semaphore, pipe và queue) mà process đó đang sử dụng bị hỏng hoặc không thể truy cập bởi các process khác.

    Vì vậy, có lẽ tốt nhất là chỉ cân nhắc sử dụng
    :meth:`Process.terminate <multiprocessing.Process.terminate>` trên các tiến trình không bao giờ sử dụng tài nguyên dùng chung nào.

Tham gia các tiến trình sử dụng hàng đợi

    Hãy lưu ý rằng một tiến trình đã đưa các mục vào hàng đợi sẽ chờ trước khi kết thúc cho đến khi tất cả các mục đã được đệm được luồng "feeder" đưa vào pipe bên dưới. (Tiến trình con có thể gọi phương thức
    :meth:`Queue.cancel_join_thread <multiprocessing.Queue.cancel_join_thread>` của hàng đợi để tránh hành vi này.)

    Điều này có nghĩa là bất cứ khi nào sử dụng hàng đợi, bạn cần đảm bảo rằng tất cả các mục đã được đưa vào hàng đợi cuối cùng đều được lấy ra trước khi tiến trình được join. Nếu không, bạn không thể chắc chắn rằng các tiến trình đã đưa mục vào hàng đợi sẽ kết thúc. Cũng hãy nhớ rằng các tiến trình không phải daemon sẽ tự động được join.

    Ví dụ sau sẽ gây deadlock::

        from multiprocessing import Process, Queue

        def f(q):
            q.put('X' * 1000000)

        if __name__ == '__main__':
            queue = Queue()
            p = Process(target=f, args=(queue,))
            p.start()
            p.join()                    # gây deadlock
            obj = queue.get()

    Một cách khắc phục ở đây là hoán đổi hai dòng cuối (hoặc chỉ cần xóa dòng ``p.join()``).

Truyền tường minh các tài nguyên cho tiến trình con

    Trên POSIX, khi sử dụng phương thức khởi động *fork*, một tiến trình con có thể sử dụng tài nguyên dùng chung được tạo trong tiến trình cha thông qua một tài nguyên toàn cục. Tuy nhiên, tốt hơn là truyền đối tượng này làm đối số cho hàm khởi tạo của tiến trình con.

    Ngoài việc giúp mã (có khả năng) tương thích với Windows và các phương thức khởi động khác, cách này còn đảm bảo rằng đối tượng sẽ không bị garbage collection trong tiến trình cha chừng nào tiến trình con vẫn còn hoạt động. Điều này có thể quan trọng nếu một tài nguyên nào đó được giải phóng khi đối tượng bị garbage collection trong tiến trình cha.

    Ví dụ::

        from multiprocessing import Process, Lock

        def f():
            ... do something using "lock" ...

        if __name__ == '__main__':
            lock = Lock()
            for i in range(10):
                Process(target=f).start()

    nên được viết lại thành::

        from multiprocessing import Process, Lock

        def f(l):
            ... do something using "l" ...

        if __name__ == '__main__':
            lock = Lock()
            for i in range(10):
                Process(target=f, args=(lock,)).start()

Cẩn thận khi thay thế :data:`sys.stdin` bằng một "đối tượng dạng tệp"

    :mod:`!multiprocessing` ban đầu luôn gọi vô điều kiện::

        os.close(sys.stdin.fileno())

    trong phương thức :meth:`multiprocessing.Process._bootstrap` --- điều này gây ra sự cố với các quy trình trong quy trình. Điều này đã được thay đổi thành::

        sys.stdin.close()
        sys.stdin = open(os.open(os.devnull, os.O_RDONLY), closefd=False)

    Điều này giải quyết vấn đề cốt lõi về việc các quy trình va chạm với nhau, dẫn đến lỗi bộ mô tả tệp không hợp lệ, nhưng lại tạo ra một nguy cơ tiềm ẩn đối với các ứng dụng thay thế :func:`sys.stdin` bằng một "đối tượng giống tệp" có bộ đệm đầu ra. Nguy cơ này xảy ra khi nhiều quy trình gọi
    :meth:`~io.IOBase.close` trên đối tượng giống tệp này, khiến cùng một dữ liệu có thể được flush vào đối tượng nhiều lần và dẫn đến hỏng dữ liệu.

    Nếu bạn viết một đối tượng giống tệp và tự triển khai cơ chế caching, bạn có thể làm cho đối tượng đó an toàn với fork bằng cách lưu pid mỗi khi bạn thêm dữ liệu vào cache và loại bỏ cache khi pid thay đổi. Ví dụ::

       @property
       def cache(self):
           pid = os.getpid()
           if pid != self._pid:
               self._pid = pid
               self._cache = []
           return self._cache

    Để biết thêm thông tin, hãy xem :issue:`5155`, :issue:`5313` và :issue:`5331`

.. _multiprocessing-programming-spawn:
.. _multiprocessing-programming-forkserver:

Các phương thức khởi động *spawn* và *forkserver*
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Có một số hạn chế bổ sung không áp dụng cho phương thức khởi động *fork*.

Yêu cầu về khả năng pickling cao hơn

    Đảm bảo rằng tất cả các đối số của :class:`~multiprocessing.Process` đều có thể được pickling. Ngoài ra, nếu bạn tạo lớp con của ``Process.__init__``, bạn phải đảm bảo rằng các thực thể của lớp đó có thể được pickling khi
    phương thức :meth:`Process.start <multiprocessing.Process.start>` được gọi.

Biến toàn cục

    Hãy lưu ý rằng nếu mã chạy trong một tiến trình con cố gắng truy cập một biến toàn cục, thì giá trị mà nó thấy (nếu có) có thể không giống với giá trị trong tiến trình cha tại thời điểm :meth:`Process.start <multiprocessing.Process.start>` được gọi.

    Tuy nhiên, các biến toàn cục chỉ là hằng số cấp mô-đun thì không gây ra vấn đề gì.

.. _multiprocessing-safe-main-import:

Nhập module chính an toàn

    Hãy đảm bảo rằng module chính có thể được một trình thông dịch Python mới nhập một cách an toàn mà không gây ra các tác dụng phụ ngoài ý muốn (chẳng hạn như khởi động một tiến trình mới).

    Ví dụ: nếu sử dụng phương thức khởi động *spawn* hoặc *forkserver*, việc chạy module sau sẽ thất bại với một
    :exc:`RuntimeError`::

        from multiprocessing import Process

        def foo():
            print('hello')

        p = Process(target=foo)
        p.start()

    Thay vào đó, cần bảo vệ "entry point" của chương trình bằng cách sử dụng ``if __name__ == '__main__':`` như sau::

       from multiprocessing import Process, freeze_support, set_start_method

       def foo():
           print('hello')

       if __name__ == '__main__':
           freeze_support()
           set_start_method('spawn')
           p = Process(target=foo)
           p.start()

    (Có thể bỏ qua dòng ``freeze_support()`` nếu chương trình sẽ được chạy bình thường thay vì ở chế độ frozen.)

    Điều này cho phép trình thông dịch Python mới được tạo an toàn nhập module, sau đó chạy hàm ``foo()`` của module.

    Các hạn chế tương tự cũng áp dụng nếu một pool hoặc manager được tạo trong module chính.


.. _multiprocessing-examples:

Ví dụ
-----

Minh họa cách tạo và sử dụng các manager và proxy tùy chỉnh:

.. literalinclude:: ../includes/mp_newtype.py
   :language: python3


Sử dụng :class:`~multiprocessing.pool.Pool`:

.. literalinclude:: ../includes/mp_pool.py
   :language: python3


Ví dụ minh họa cách sử dụng các queue để phân phối tác vụ cho một tập hợp các tiến trình worker và thu thập kết quả:

.. literalinclude:: ../includes/mp_workers.py
