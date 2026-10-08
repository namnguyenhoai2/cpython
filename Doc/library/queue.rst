:mod:`!queue` --- Lớp hàng đợi đồng bộ
======================================

.. module:: queue
   :synopsis: Lớp hàng đợi đồng bộ.

**Mã nguồn:** :source:`Lib/queue.py`

--------------

Mô-đun :mod:`!queue` triển khai các hàng đợi đa producer, đa consumer. Mô-đun này đặc biệt hữu ích trong lập trình đa luồng khi thông tin cần được trao đổi an toàn giữa nhiều thread. Lớp :class:`Queue` trong mô-đun này triển khai tất cả ngữ nghĩa khóa cần thiết.

Mô-đun triển khai ba loại hàng đợi, chỉ khác nhau ở thứ tự các mục được lấy ra. Trong hàng đợi :abbr:`FIFO (vào trước, ra trước)`, các tác vụ được thêm vào trước sẽ được lấy ra trước. Trong một
hàng đợi :abbr:`LIFO (vào sau, ra trước)`, mục được thêm gần đây nhất sẽ được lấy ra trước (hoạt động như một stack). Với hàng đợi ưu tiên, các mục được sắp xếp (bằng mô-đun :mod:`heapq`) và mục có giá trị thấp nhất sẽ được lấy ra trước.

Về nội bộ, ba loại hàng đợi này sử dụng các khóa để tạm thời chặn các thread cạnh tranh; tuy nhiên, chúng không được thiết kế để xử lý việc tái nhập trong một thread.

Ngoài ra, mô-đun triển khai một "simple"
:abbr:`FIFO (vào trước, ra trước)` kiểu hàng đợi, :class:`SimpleQueue`, mà phần triển khai cụ thể cung cấp thêm các đảm bảo để đổi lấy ít chức năng hơn.

Mô-đun :mod:`!queue` định nghĩa các lớp và ngoại lệ sau:

.. class:: Queue(maxsize=0)

   Hàm khởi tạo cho một hàng đợi :abbr:`FIFO (vào trước, ra trước)`. *maxsize* là một số nguyên đặt giới hạn trên về số lượng mục có thể được đưa vào hàng đợi. Việc chèn sẽ bị chặn khi đạt đến kích thước này, cho đến khi các mục trong hàng đợi được lấy ra. Nếu *maxsize* nhỏ hơn hoặc bằng không, kích thước hàng đợi là vô hạn.

.. class:: LifoQueue(maxsize=0)

   Hàm khởi tạo cho một hàng đợi :abbr:`LIFO (vào sau, ra trước)`. *maxsize* là một số nguyên đặt giới hạn trên về số lượng mục có thể được đưa vào hàng đợi. Việc chèn sẽ bị chặn khi đạt đến kích thước này, cho đến khi các mục trong hàng đợi được lấy ra. Nếu *maxsize* nhỏ hơn hoặc bằng không, kích thước hàng đợi là vô hạn.


.. class:: PriorityQueue(maxsize=0)

   Hàm khởi tạo cho một hàng đợi ưu tiên. *maxsize* là một số nguyên đặt giới hạn trên về số lượng mục có thể được đưa vào hàng đợi. Việc chèn sẽ bị chặn khi đạt đến kích thước này, cho đến khi các mục trong hàng đợi được lấy ra. Nếu *maxsize* nhỏ hơn hoặc bằng không, kích thước hàng đợi là vô hạn.

   Các mục có giá trị thấp nhất được lấy ra trước (mục có giá trị thấp nhất là mục sẽ được ``min(entries)`` trả về). Một mẫu điển hình cho các mục là một tuple có dạng: ``(priority_number, data)``.

   Nếu các phần tử *data* không thể so sánh được, có thể bọc dữ liệu trong một class bỏ qua mục dữ liệu và chỉ so sánh số độ ưu tiên::

        from dataclasses import dataclass, field
        from typing import Any

        @dataclass(order=True)
        class PrioritizedItem:
            priority: int
            item: Any=field(compare=False)

.. class:: SimpleQueue()

   Hàm khởi tạo cho một hàng đợi :abbr:`FIFO (vào trước, ra trước)` không giới hạn. Hàng đợi đơn giản không có các chức năng nâng cao như theo dõi tác vụ.

   Hàng đợi đơn giản là :ref:`generic <generics>` theo kiểu của các mục trong hàng đợi.

   .. versionadded:: 3.7


.. exception:: Empty

   Ngoại lệ được phát sinh khi gọi :meth:`~Queue.get` không chặn (hoặc
   :meth:`~Queue.get_nowait`) trên một đối tượng :class:`Queue` đang trống.


.. exception:: Full

   Ngoại lệ được phát sinh khi gọi :meth:`~Queue.put` không chặn (hoặc
   :meth:`~Queue.put_nowait`) trên một đối tượng :class:`Queue` đã đầy.


.. exception:: ShutDown

   Ngoại lệ được nêu ra khi gọi :meth:`~Queue.put` hoặc :meth:`~Queue.get` trên một đối tượng :class:`Queue` đã bị tắt.

   .. versionadded:: 3.13


.. _queueobjects:

Đối tượng Queue
---------------

Các đối tượng Queue (:class:`Queue`, :class:`LifoQueue` hoặc :class:`PriorityQueue`) cung cấp các phương thức công khai được mô tả dưới đây.


.. method:: Queue.qsize()

   Trả về kích thước gần đúng của queue. Lưu ý rằng qsize() > 0 không đảm bảo rằng một lệnh gọi get() tiếp theo sẽ không bị block, cũng như qsize() < maxsize không đảm bảo rằng put() sẽ không bị block.


.. method:: Queue.empty()

   Trả về ``True`` nếu queue trống, nếu không thì trả về ``False``. Nếu empty() trả về ``True``, điều đó không đảm bảo rằng một lệnh gọi put() tiếp theo sẽ không bị block. Tương tự, nếu empty() trả về ``False``, điều đó không đảm bảo rằng một lệnh gọi get() tiếp theo sẽ không bị block.


.. method:: Queue.full()

   Trả về ``True`` nếu queue đầy, nếu không thì trả về ``False``. Nếu full() trả về ``True``, điều đó không đảm bảo rằng một lệnh gọi get() tiếp theo sẽ không bị block. Tương tự, nếu full() trả về ``False``, điều đó không đảm bảo rằng một lệnh gọi put() tiếp theo sẽ không bị block.


.. method:: Queue.put(item, block=True, timeout=None)

   Đưa *item* vào queue. Nếu đối số tùy chọn *block* là true và *timeout* là ``None`` (giá trị mặc định), thì block nếu cần cho đến khi có chỗ trống. Nếu *timeout* là một số dương, lệnh này block nhiều nhất *timeout* giây và nêu :exc:`Full` exception nếu không có chỗ trống trong khoảng thời gian đó. Ngược lại (*block* là false), đưa một item vào queue nếu ngay lập tức có chỗ trống; nếu không, nêu :exc:`Full` exception (*timeout* bị bỏ qua trong trường hợp này).

   Phát sinh :exc:`ShutDown` nếu hàng đợi đã bị tắt.


.. method:: Queue.put_nowait(item)

   Tương đương với ``put(item, block=False)``.


.. method:: Queue.get(block=True, timeout=None)

   Xóa và trả về một mục khỏi hàng đợi. Nếu đối số tùy chọn *block* là true và *timeout* là ``None`` (mặc định), hãy chờ nếu cần cho đến khi có một mục. Nếu *timeout* là một số dương, thao tác sẽ chờ tối đa *timeout* giây và phát sinh ngoại lệ :exc:`Empty` nếu không có mục nào khả dụng trong khoảng thời gian đó. Ngược lại (*block* là false), trả về một mục nếu có sẵn ngay lập tức; nếu không, phát sinh ngoại lệ :exc:`Empty` (*timeout* sẽ bị bỏ qua trong trường hợp này).

   Trước phiên bản 3.0 trên các hệ thống POSIX và trên Windows ở mọi phiên bản, nếu *block* là true và *timeout* là ``None``, thao tác này sẽ chờ không thể bị ngắt trên một khóa nền tảng. Điều này có nghĩa là không ngoại lệ nào có thể xảy ra, đặc biệt là SIGINT sẽ không kích hoạt :exc:`KeyboardInterrupt`.

   Phát sinh :exc:`ShutDown` nếu hàng đợi đã bị tắt và đang trống, hoặc nếu hàng đợi đã bị tắt ngay lập tức.


.. method:: Queue.get_nowait()

   Tương đương với ``get(False)``.

Có hai phương thức được cung cấp để theo dõi xem các tác vụ đã xếp hàng có được các luồng consumer daemon xử lý hoàn toàn hay chưa.


.. method:: Queue.task_done()

   Cho biết một tác vụ đã được đưa vào hàng đợi trước đó đã hoàn tất. Được các thread consumer của queue sử dụng. Với mỗi :meth:`get` được sử dụng để lấy một tác vụ, một lần gọi tiếp theo đến
   :meth:`task_done` cho queue biết rằng quá trình xử lý tác vụ đã hoàn tất.

   Nếu một :meth:`join` hiện đang bị chặn, nó sẽ tiếp tục khi tất cả các mục đã được xử lý (nghĩa là đã nhận được một lần gọi :meth:`task_done` cho mỗi mục đã được :meth:`put` vào queue).

   Phát sinh một :exc:`ValueError` nếu được gọi nhiều lần hơn số mục đã được đưa vào queue.


.. method:: Queue.join()

   Chặn cho đến khi tất cả các mục trong queue được lấy ra và xử lý.

   Số lượng tác vụ chưa hoàn tất tăng lên mỗi khi một mục được thêm vào queue. Số lượng này giảm xuống mỗi khi một thread consumer gọi :meth:`task_done` để cho biết rằng mục đó đã được lấy ra và mọi công việc trên mục đó đã hoàn tất. Khi số lượng tác vụ chưa hoàn tất giảm xuống bằng không, :meth:`join` sẽ bỏ chặn.


Chờ tác vụ hoàn tất
^^^^^^^^^^^^^^^^^^^

Ví dụ về cách chờ các tác vụ đã xếp hàng hoàn tất::

    import threading
    import queue

    q = queue.Queue()

    def worker():
        while True:
            item = q.get()
            print(f'Working on {item}')
            print(f'Finished {item}')
            q.task_done()

    # Bật worker thread.
    threading.Thread(target=worker, daemon=True).start()

    # Gửi ba mươi yêu cầu tác vụ đến worker.
    for item in range(30):
        q.put(item)

    # Chặn cho đến khi mọi tác vụ hoàn tất.
    q.join()
    print('All work completed')


Kết thúc các hàng đợi
^^^^^^^^^^^^^^^^^^^^^

Khi không còn cần thiết, các đối tượng :class:`Queue` có thể được giảm dần cho đến khi rỗng hoặc chấm dứt ngay lập tức bằng hard shutdown.

.. method:: Queue.shutdown(immediate=False)

   Đưa một instance :class:`Queue` vào chế độ shutdown.

   Hàng đợi không thể phát triển thêm. Các lần gọi :meth:`~Queue.put` trong tương lai sẽ phát sinh :exc:`ShutDown`. Các caller hiện đang bị chặn bởi :meth:`~Queue.put` sẽ được bỏ chặn và phát sinh :exc:`ShutDown` trong thread trước đây bị chặn.

   Nếu *immediate* là false (mặc định), hàng đợi có thể được kết thúc bình thường bằng các lần gọi :meth:`~Queue.get` để lấy ra những task đã được nạp.

   Và nếu :meth:`~Queue.task_done` được gọi cho từng task còn lại, một :meth:`~Queue.join` đang chờ sẽ được bỏ chặn bình thường.

   Sau khi hàng đợi rỗng, các lần gọi :meth:`~Queue.get` trong tương lai sẽ phát sinh :exc:`ShutDown`.

   Nếu *immediate* là true, hàng đợi sẽ được kết thúc ngay lập tức. Hàng đợi được rút hết để hoàn toàn rỗng và số lượng task chưa hoàn tất được giảm đi bằng số task đã rút. Nếu số task chưa hoàn tất bằng không, các caller của :meth:`~Queue.join` sẽ được bỏ chặn. Ngoài ra, các caller đang bị chặn của :meth:`~Queue.get` cũng sẽ được bỏ chặn và phát sinh :exc:`ShutDown` vì hàng đợi đã rỗng.

   Hãy thận trọng khi sử dụng :meth:`~Queue.join` với *immediate* được đặt thành true. Thao tác này bỏ chặn join ngay cả khi chưa có công việc nào được thực hiện trên các task, vi phạm invariant thông thường khi join một hàng đợi.

   .. versionadded:: 3.13


Các đối tượng SimpleQueue
-------------------------

Các đối tượng :class:`SimpleQueue` cung cấp những phương thức công khai được mô tả dưới đây.

.. method:: SimpleQueue.qsize()

   Trả về kích thước gần đúng của hàng đợi. Lưu ý, qsize() > 0 không đảm bảo rằng một lệnh gọi get() tiếp theo sẽ không bị chặn.


.. method:: SimpleQueue.empty()

   Trả về ``True`` nếu hàng đợi trống, nếu không thì trả về ``False``. Nếu empty() trả về ``False``, điều đó không đảm bảo rằng một lệnh gọi get() tiếp theo sẽ không bị chặn.


.. method:: SimpleQueue.put(item, block=True, timeout=None)

   Đưa *item* vào hàng đợi. Phương thức này không bao giờ bị chặn và luôn thành công (ngoại trừ các lỗi cấp thấp có thể xảy ra, chẳng hạn như không thể cấp phát bộ nhớ). Các đối số tùy chọn *block* và *timeout* bị bỏ qua và chỉ được cung cấp để tương thích với :meth:`Queue.put`.

   .. impl-detail::
      Phương thức này có một bản triển khai bằng C và có tính reentrant. Nghĩa là một lời gọi ``put()`` hoặc ``get()`` có thể bị gián đoạn bởi một lời gọi ``put()`` khác trong cùng luồng mà không gây deadlock hoặc làm hỏng trạng thái nội bộ bên trong hàng đợi. Điều này khiến phương thức phù hợp để sử dụng trong các hàm hủy như phương thức ``__del__`` hoặc callback :mod:`weakref`.


.. method:: SimpleQueue.put_nowait(item)

   Tương đương với ``put(item, block=False)``, được cung cấp để tương thích với
   :meth:`Queue.put_nowait`.


.. method:: SimpleQueue.get(block=True, timeout=None)

   Xóa và trả về một mục khỏi hàng đợi. Nếu đối số tùy chọn *block* là true và *timeout* là ``None`` (mặc định), phương thức sẽ chặn nếu cần cho đến khi có một mục. Nếu *timeout* là một số dương, phương thức sẽ chặn nhiều nhất trong *timeout* giây và phát sinh ngoại lệ :exc:`Empty` nếu không có mục nào trong khoảng thời gian đó. Nếu không (*block* là false), trả về một mục nếu có sẵn ngay lập tức; nếu không thì phát sinh ngoại lệ :exc:`Empty` (trong trường hợp đó, *timeout* bị bỏ qua).


.. method:: SimpleQueue.get_nowait()

   Tương đương với ``get(False)``.


.. seealso::

   Lớp :class:`multiprocessing.Queue`
      Một lớp queue dùng trong ngữ cảnh đa xử lý (thay vì đa luồng).

   :class:`collections.deque` là một triển khai thay thế của các queue không giới hạn với các thao tác :meth:`~collections.deque.append` nguyên tử nhanh và
   các thao tác :meth:`~collections.deque.popleft` không yêu cầu khóa và cũng hỗ trợ lập chỉ mục.
