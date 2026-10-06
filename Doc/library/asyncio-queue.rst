.. currentmodule:: asyncio

.. _asyncio-queues:

========
Hàng đợi
========

**Mã nguồn:** :source:`Lib/asyncio/queues.py`

------------------------------------------------

Các hàng đợi asyncio được thiết kế tương tự như các lớp của
:mod:`queue` mô-đun. Mặc dù các hàng đợi asyncio không an toàn đối với thread, chúng được thiết kế đặc biệt để sử dụng trong mã async/await.

Lưu ý rằng các phương thức của hàng đợi asyncio không có tham số *timeout*; hãy sử dụng hàm :func:`asyncio.wait_for` để thực hiện các thao tác với hàng đợi có thời gian chờ.

Xem thêm phần `Examples`_ bên dưới.

Queue
=====

.. class:: Queue(maxsize=0)

   Một hàng đợi vào trước, ra trước (FIFO).

   Nếu *maxsize* nhỏ hơn hoặc bằng không, kích thước hàng đợi là vô hạn. Nếu đây là một số nguyên lớn hơn ``0``, thì ``await put()`` sẽ bị chặn khi hàng đợi đạt đến *maxsize* cho đến khi một mục được :meth:`get` xóa.

   Không giống như :mod:`queue` Queue của thư viện chuẩn threading, kích thước của hàng đợi luôn được biết và có thể được trả về bằng cách gọi
   :meth:`qsize` method.

   .. versionchanged:: 3.10
      Đã loại bỏ tham số *loop*.


   Lớp này :ref:`không an toàn khi sử dụng trong nhiều luồng <asyncio-multithreading>`.

   .. attribute:: maxsize

      Số lượng mục được phép có trong hàng đợi.

   .. method:: empty()

      Trả về ``True`` nếu hàng đợi trống, nếu không thì trả về ``False``.

   .. method:: full()

      Trả về ``True`` nếu có :attr:`maxsize` mục trong hàng đợi.

      Nếu hàng đợi được khởi tạo bằng ``maxsize=0`` (mặc định), thì :meth:`full` không bao giờ trả về ``True``.

   .. method:: get()
      :async:

      Xóa và trả về một mục khỏi hàng đợi. Nếu hàng đợi trống, hãy chờ cho đến khi có mục.

      Phát sinh :exc:`QueueShutDown` nếu hàng đợi đã bị tắt và đang trống, hoặc nếu hàng đợi bị tắt ngay lập tức.

   .. method:: get_nowait()

      Trả về một mục nếu có sẵn ngay lập tức, nếu không thì phát sinh
      :exc:`QueueEmpty`.

      Phát sinh :exc:`QueueShutDown` nếu hàng đợi đã bị tắt và đang trống.

   .. method:: join()
      :async:

      Chặn cho đến khi tất cả các mục trong hàng đợi đã được nhận và xử lý.

      Số lượng tác vụ chưa hoàn tất tăng lên mỗi khi một mục được thêm vào hàng đợi. Số lượng này giảm xuống mỗi khi một coroutine consumer gọi
      :meth:`task_done` để cho biết rằng mục đó đã được truy xuất và mọi công việc liên quan đã hoàn tất. Khi số lượng tác vụ chưa hoàn tất giảm xuống bằng không, :meth:`join` sẽ được bỏ chặn.

   .. method:: put(item)
      :async:

      Đưa một mục vào hàng đợi. Nếu hàng đợi đầy, hãy chờ cho đến khi có chỗ trống trước khi thêm mục đó.

      Phát sinh :exc:`QueueShutDown` nếu hàng đợi đã bị tắt.

   .. method:: put_nowait(item)

      Đưa một mục vào hàng đợi mà không chặn.

      Nếu không có chỗ trống ngay lập tức, hãy phát sinh :exc:`QueueFull`.

      Phát sinh :exc:`QueueShutDown` nếu hàng đợi đã bị tắt.

   .. method:: qsize()

      Trả về số lượng mục trong queue.

   .. method:: shutdown(immediate=False)

      Đưa một instance :class:`Queue` vào chế độ shutdown.

      Queue không thể tăng thêm. Các lần gọi :meth:`~Queue.put` trong tương lai sẽ raise :exc:`QueueShutDown`. Các caller hiện đang bị block bởi :meth:`~Queue.put` sẽ được unblock và sẽ raise :exc:`QueueShutDown` trong task trước đó đang chờ.

      Nếu *immediate* là false (giá trị mặc định), queue có thể được xử lý để kết thúc bình thường bằng các lần gọi :meth:`~Queue.get` nhằm lấy ra những task đã được nạp.

      Và nếu :meth:`~Queue.task_done` được gọi cho từng task còn lại, một :meth:`~Queue.join` đang pending sẽ được unblock bình thường.

      Khi queue trống, các lần gọi :meth:`~Queue.get` trong tương lai sẽ raise :exc:`QueueShutDown`.

      Nếu *ngay lập tức* là true, hàng đợi sẽ bị chấm dứt ngay lập tức. Hàng đợi được làm trống hoàn toàn và số lượng tác vụ chưa hoàn thành được giảm đi bằng số tác vụ đã được lấy ra. Nếu số tác vụ chưa hoàn thành bằng không, các caller của :meth:`~Queue.join` sẽ được bỏ chặn. Ngoài ra, các caller đang bị chặn của :meth:`~Queue.get` cũng được bỏ chặn và sẽ raise :exc:`QueueShutDown` vì hàng đợi đã trống.

      Hãy thận trọng khi sử dụng :meth:`~Queue.join` với *immediate* được đặt thành true. Lệnh này bỏ chặn thao tác join ngay cả khi chưa có công việc nào được thực hiện trên các tác vụ, vi phạm invariant thông thường khi join một hàng đợi.

      .. versionadded:: 3.13

   .. method:: task_done()

      Cho biết một mục công việc trước đây đã được đưa vào hàng đợi đã hoàn tất.

      Được các consumer của hàng đợi sử dụng. Với mỗi :meth:`~Queue.get` được sử dụng để lấy một mục công việc, một lệnh gọi tiếp theo đến :meth:`task_done` sẽ cho hàng đợi biết rằng quá trình xử lý mục công việc đó đã hoàn tất.

      Nếu một :meth:`join` hiện đang bị chặn, lệnh này sẽ tiếp tục khi tất cả các mục đã được xử lý (nghĩa là đã nhận được một lệnh gọi :meth:`task_done` cho mọi mục đã được :meth:`~Queue.put` vào hàng đợi).

      Raise :exc:`ValueError` nếu được gọi nhiều lần hơn số mục đã được đưa vào hàng đợi.


Hàng đợi ưu tiên
================

.. class:: PriorityQueue

   Một biến thể của :class:`Queue`; truy xuất các mục theo thứ tự ưu tiên (từ thấp nhất trước).

   Các mục thường là các tuple có dạng ``(priority_number, data)``.


Hàng đợi LIFO
=============

.. class:: LifoQueue

   Một biến thể của :class:`Queue`, truy xuất các mục được thêm gần đây nhất trước (vào sau, ra trước).


Ngoại lệ
========

.. exception:: QueueEmpty

   Ngoại lệ này được phát sinh khi phương thức :meth:`~Queue.get_nowait` được gọi trên một hàng đợi trống.


.. exception:: QueueFull

   Ngoại lệ được phát sinh khi phương thức :meth:`~Queue.put_nowait` được gọi trên một hàng đợi đã đạt đến *maxsize*.


.. exception:: QueueShutDown

   Ngoại lệ được đưa ra khi :meth:`~Queue.put`, :meth:`~Queue.put_nowait`,
   :meth:`~Queue.get` hoặc :meth:`~Queue.get_nowait` được gọi trên một queue đã bị tắt.

   .. versionadded:: 3.13


.. _`Examples`:

Ví dụ
=====

.. _asyncio_example_queue_dist:

Có thể sử dụng queue để phân phối khối lượng công việc giữa nhiều tác vụ đồng thời::

   import asyncio
   import random
   import time


   async def worker(name, queue):
       while True:
           # Lấy một "work item" ra khỏi queue.
           sleep_for = await queue.get()

           # Tạm dừng trong "sleep_for" giây.
           await asyncio.sleep(sleep_for)

           # Thông báo cho queue rằng "work item" đã được xử lý.
           queue.task_done()

           print(f'{name} has slept for {sleep_for:.2f} seconds')


   async def main():
       # Tạo một queue để lưu trữ "workload" của chúng ta.
       queue = asyncio.Queue()

       # Tạo các khoảng thời gian ngẫu nhiên và đưa chúng vào queue.
       total_sleep_time = 0
       for _ in range(20):
           sleep_for = random.uniform(0.05, 1.0)
           total_sleep_time += sleep_for
           queue.put_nowait(sleep_for)

       # Tạo ba worker task để xử lý queue đồng thời.
       tasks = []
       for i in range(3):
           task = asyncio.create_task(worker(f'worker-{i}', queue))
           tasks.append(task)

       # Chờ cho đến khi queue được xử lý hoàn toàn.
       started_at = time.monotonic()
       await queue.join()
       total_slept_for = time.monotonic() - started_at

       # Hủy các worker task của chúng ta.
       for task in tasks:
           task.cancel()
       # Chờ cho đến khi tất cả worker task bị hủy.
       await asyncio.gather(*tasks, return_exceptions=True)

       print('====')
       print(f'3 workers slept in parallel for {total_slept_for:.2f} seconds')
       print(f'total expected sleep time: {total_sleep_time:.2f} seconds')


   asyncio.run(main())
