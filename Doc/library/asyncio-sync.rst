.. currentmodule:: asyncio

.. _asyncio-sync:

=========================
Các primitive đồng bộ hóa
=========================

**Mã nguồn:** :source:`Lib/asyncio/locks.py`

-----------------------------------------------

Các primitive đồng bộ hóa của asyncio được thiết kế tương tự như các primitive trong mô-đun :mod:`threading` với hai điểm cần lưu ý:

* Các primitive của asyncio không an toàn khi sử dụng với thread, vì vậy không nên dùng chúng để đồng bộ hóa thread của hệ điều hành (hãy sử dụng :mod:`threading` cho mục đích đó);

* Các phương thức của những primitive đồng bộ hóa này không chấp nhận đối số *timeout*; hãy sử dụng hàm :func:`asyncio.wait_for` để thực hiện các thao tác có thời gian chờ.

asyncio có các primitive đồng bộ hóa cơ bản sau:

* :class:`Lock`
* :class:`Event`
* :class:`Condition`
* :class:`Semaphore`
* :class:`BoundedSemaphore`
* :class:`Barrier`


---------


Lock
====

.. class:: Lock()

   Triển khai khóa mutex cho các tác vụ asyncio. Không an toàn khi sử dụng với nhiều luồng.

   Có thể sử dụng khóa asyncio để đảm bảo quyền truy cập độc quyền vào tài nguyên dùng chung.

   Cách ưu tiên để sử dụng Lock là một câu lệnh :keyword:`async with`::

       lock = asyncio.Lock()

       # ... về sau
       async with lock:
           # truy cập trạng thái dùng chung

   tương đương với::

       lock = asyncio.Lock()

       # ... về sau
       await lock.acquire()
       try:
           # truy cập trạng thái dùng chung
       finally:
           lock.release()

   .. versionchanged:: 3.10
      Đã xóa tham số *loop*.

   .. method:: acquire()
      :async:

      Lấy khóa.

      Phương thức này chờ cho đến khi khóa ở trạng thái *unlocked*, đặt khóa thành *locked* rồi trả về ``True``.

      Khi có nhiều coroutine bị chặn trong :meth:`acquire` chờ khóa được mở, cuối cùng chỉ một coroutine tiếp tục thực thi.

      Việc lấy khóa là *fair*: coroutine tiếp tục thực thi sẽ là coroutine đầu tiên bắt đầu chờ khóa.

   .. method:: release()

      Giải phóng khóa.

      Khi lock ở trạng thái *locked*, hãy đặt lại về trạng thái *unlocked* rồi trả về.

      Nếu lock ở trạng thái *unlocked*, một :exc:`RuntimeError` sẽ được phát sinh.

   .. method:: locked()

      Trả về ``True`` nếu lock ở trạng thái *locked*.


Event
=====

.. class:: Event()

   Một đối tượng event. Không thread-safe.

   Có thể sử dụng một event asyncio để thông báo cho nhiều task asyncio rằng một sự kiện nào đó đã xảy ra.

   Một đối tượng Event quản lý một cờ nội bộ có thể được đặt thành *true* bằng phương thức :meth:`~Event.set` và được đặt lại thành *false* bằng
   Phương thức :meth:`clear`. Phương thức :meth:`~Event.wait` chặn cho đến khi cờ được đặt thành *true*. Ban đầu, cờ được đặt thành *false*.

   .. versionchanged:: 3.10
      Đã loại bỏ tham số *loop*.

   .. _asyncio_example_sync_event:

   Ví dụ::

      async def waiter(event):
          print('waiting for it ...')
          await event.wait()
          print('... got it!')

      async def main():
          # Tạo một đối tượng Event.
          event = asyncio.Event()

          # Tạo một Task để chờ cho đến khi 'event' được đặt.
          waiter_task = asyncio.create_task(waiter(event))

          # Ngủ trong 1 giây rồi đặt event.
          await asyncio.sleep(1)
          event.set()

          # Chờ cho đến khi tác vụ waiter hoàn tất.
          await waiter_task

      asyncio.run(main())

   .. method:: wait()
      :async:

      Chờ cho đến khi event được thiết lập.

      Nếu event đã được thiết lập, lập tức trả về ``True``. Nếu không, hãy chặn cho đến khi một task khác gọi :meth:`~Event.set`.

   .. method:: set()

      Thiết lập event.

      Tất cả các task đang chờ event được thiết lập sẽ ngay lập tức được đánh thức.

   .. method:: clear()

      Xóa (hủy thiết lập) event.

      Các task tiếp theo đang chờ :meth:`~Event.wait` giờ đây sẽ bị chặn cho đến khi
      phương thức :meth:`~Event.set` được gọi lại.

   .. method:: is_set()

      Trả về ``True`` nếu event được thiết lập.


Điều kiện
=========

.. class:: Condition(lock=None)

   Một đối tượng Condition. Không an toàn khi sử dụng trong môi trường đa luồng.

   Một primitive điều kiện asyncio có thể được task sử dụng để chờ một sự kiện xảy ra, sau đó giành quyền truy cập độc quyền vào một tài nguyên dùng chung.

   Về cơ bản, một đối tượng Condition kết hợp chức năng của một :class:`Event` và một :class:`Lock`. Có thể để nhiều đối tượng Condition dùng chung một Lock, cho phép điều phối quyền truy cập độc quyền vào một tài nguyên dùng chung giữa các task khác nhau quan tâm đến những trạng thái cụ thể của tài nguyên dùng chung đó.

   Đối số *lock* tùy chọn phải là một đối tượng :class:`Lock` hoặc ``None``. Trong trường hợp sau, một đối tượng Lock mới sẽ được tự động tạo.

   .. versionchanged:: 3.10
      Đã xóa tham số *loop*.

   Cách được khuyến nghị để sử dụng Condition là dùng câu lệnh :keyword:`async with`::

       cond = asyncio.Condition()

       # ... sau đó
       async with cond:
           await cond.wait()

   tương đương với::

       cond = asyncio.Condition()

       # ... sau đó
       await cond.acquire()
       try:
           await cond.wait()
       finally:
           cond.release()

   .. method:: acquire()
      :async:

      Acquire khóa nền tảng.

      Phương thức này chờ cho đến khi khóa nền tảng được *mở khóa*, đặt khóa thành *đã khóa* rồi trả về ``True``.

   .. method:: notify(n=1)

      Đánh thức *n* tác vụ (mặc định là 1) đang chờ trên condition này. Nếu có ít hơn *n* tác vụ đang chờ thì tất cả chúng đều được đánh thức.

      Phải giành được khóa trước khi gọi phương thức này và giải phóng khóa ngay sau đó. Nếu được gọi với một khóa *unlocked*, lỗi :exc:`RuntimeError` sẽ được phát sinh.

   .. method:: locked()

      Trả về ``True`` nếu khóa bên dưới được giành quyền.

   .. method:: notify_all()

      Đánh thức tất cả các tác vụ đang chờ trên điều kiện này.

      Phương thức này hoạt động giống :meth:`notify`, nhưng đánh thức tất cả các tác vụ đang chờ.

      Phải giành được khóa trước khi gọi phương thức này và giải phóng khóa ngay sau đó. Nếu được gọi với một khóa *unlocked*, lỗi :exc:`RuntimeError` sẽ được phát sinh.

   .. method:: release()

      Giải phóng khóa bên dưới.

      Khi được gọi trên một khóa chưa được khóa, một :exc:`RuntimeError` sẽ được phát sinh.

   .. method:: wait()
      :async:

      Chờ cho đến khi được thông báo.

      Nếu task gọi chưa giành được lock khi phương thức này được gọi, một :exc:`RuntimeError` sẽ được phát sinh.

      Phương thức này giải phóng lock bên dưới, sau đó chặn cho đến khi được đánh thức bởi lệnh gọi :meth:`notify` hoặc :meth:`notify_all`. Sau khi được đánh thức, Condition giành lại lock của nó và phương thức này trả về ``True``.

      Lưu ý rằng một task *có thể* trở về từ lệnh gọi này một cách ngoài dự kiến; vì vậy, bên gọi luôn phải kiểm tra lại trạng thái và sẵn sàng :meth:`~Condition.wait` một lần nữa. Vì lý do này, bạn có thể muốn sử dụng :meth:`~Condition.wait_for` thay thế.

   .. method:: wait_for(predicate)
      :async:

      Chờ cho đến khi một predicate trở thành *đúng*.

      Predicate phải là một callable mà kết quả của nó sẽ được diễn giải như một giá trị boolean. Phương thức này sẽ lặp lại
      :meth:`~Condition.wait` cho đến khi predicate được đánh giá là *đúng*. Giá trị cuối cùng là giá trị trả về.


Semaphore
=========

.. class:: Semaphore(value=1)

   Đối tượng Semaphore. Không an toàn khi sử dụng trong nhiều thread.

   Semaphore quản lý một bộ đếm nội bộ, bộ đếm này được giảm đi sau mỗi
   :meth:`acquire` lần gọi và được tăng lên sau mỗi lần gọi :meth:`release`. Bộ đếm không bao giờ có thể nhỏ hơn 0; khi :meth:`acquire` phát hiện bộ đếm bằng 0, nó sẽ chặn và chờ cho đến khi một task nào đó gọi
   :meth:`release`.

   Đối số *value* tùy chọn cung cấp giá trị ban đầu cho bộ đếm nội bộ (mặc định là ``1``). Nếu giá trị được cung cấp nhỏ hơn ``0``, một :exc:`ValueError` sẽ được nâng lên.

   .. versionchanged:: 3.10
      Đã xóa tham số *loop*.

   Cách được khuyến nghị để sử dụng Semaphore là một câu lệnh :keyword:`async with`::

       sem = asyncio.Semaphore(10)

       # ... sau đó
       async with sem:
           # làm việc với tài nguyên dùng chung

   tương đương với::

       sem = asyncio.Semaphore(10)

       # ... sau đó
       await sem.acquire()
       try:
           # làm việc với tài nguyên dùng chung
       finally:
           sem.release()

   .. method:: acquire()
      :async:

      Acquire một semaphore.

      Nếu bộ đếm nội bộ lớn hơn 0, giảm nó đi một đơn vị và trả về ``True`` ngay lập tức. Nếu bộ đếm bằng 0, hãy chờ cho đến khi :meth:`release` được gọi rồi trả về ``True``.

   .. method:: locked()

      Trả về ``True`` nếu không thể acquire semaphore ngay lập tức.

   .. method:: release()

      Giải phóng một semaphore, tăng bộ đếm nội bộ lên một. Có thể đánh thức một task đang chờ acquire semaphore.

      Không giống :class:`BoundedSemaphore`, :class:`Semaphore` cho phép thực hiện nhiều lời gọi ``release()`` hơn các lời gọi ``acquire()``.


BoundedSemaphore
================

.. class:: BoundedSemaphore(value=1)

   Một đối tượng semaphore có giới hạn. Không an toàn với thread.

   Bounded Semaphore là một phiên bản của :class:`Semaphore` sẽ raise một :exc:`ValueError` trong :meth:`~Semaphore.release` nếu tăng bộ đếm nội bộ vượt quá *value* ban đầu.

   .. versionchanged:: 3.10
      Đã loại bỏ tham số *loop*.


Barrier
=======

.. class:: Barrier(parties)

   Một đối tượng barrier. Không an toàn khi sử dụng trong môi trường đa luồng.

   Barrier là một primitive đồng bộ hóa đơn giản, cho phép chặn cho đến khi có số lượng tác vụ bằng *bên tham gia* đang chờ trên đó. Các tác vụ có thể chờ bằng phương thức :meth:`~Barrier.wait` và sẽ bị chặn cho đến khi số lượng tác vụ được chỉ định kết thúc chờ tại :meth:`~Barrier.wait`. Khi đó, tất cả các tác vụ đang chờ sẽ đồng thời được bỏ chặn.

   :keyword:`async with` có thể được sử dụng như một giải pháp thay thế cho việc await trên
   :meth:`~Barrier.wait`.

   Có thể tái sử dụng barrier bao nhiêu lần tùy ý.

   .. _asyncio_example_barrier:

   Ví dụ::

      async def example_barrier():
         # barrier với 3 bên tham gia
         b = asyncio.Barrier(3)

         # tạo 2 task đang chờ mới
         asyncio.create_task(b.wait())
         asyncio.create_task(b.wait())

         await asyncio.sleep(0)
         print(b)

         # Lần gọi .wait() thứ ba vượt qua barrier
         await b.wait()
         print(b)
         print("barrier passed")

         await asyncio.sleep(0)
         print(b)

      asyncio.run(example_barrier())

   Kết quả của ví dụ này là::

      <asyncio.locks.Barrier object at 0x... [filling, waiters:2/3]>
      <asyncio.locks.Barrier object at 0x... [draining, waiters:0/3]>
      barrier passed
      <asyncio.locks.Barrier object at 0x... [filling, waiters:0/3]>

   .. versionadded:: 3.11

   .. method:: wait()
      :async:

      Vượt qua barrier. Khi tất cả task tham gia barrier đã gọi hàm này, chúng sẽ đồng thời được bỏ chặn.

      Khi một task đang chờ hoặc bị chặn trong barrier bị hủy, task đó sẽ thoát khỏi barrier, còn barrier vẫn giữ nguyên trạng thái. Nếu trạng thái của barrier là "filling", số task đang chờ sẽ giảm đi 1.

      Giá trị trả về là một số nguyên trong khoảng từ 0 đến ``parties-1``, khác nhau đối với mỗi task. Có thể dùng giá trị này để chọn một task thực hiện một số công việc dọn dẹp đặc biệt, chẳng hạn như::

         ...
         async with barrier as position:
            if position == 0:
               # Chỉ một task in dòng này
               print('End of *draining phase*')

      Phương thức này có thể raise exception :class:`BrokenBarrierError` nếu barrier bị phá vỡ hoặc đặt lại trong khi một task đang chờ. Nó có thể raise :exc:`CancelledError` nếu một task bị hủy.

   .. method:: reset()
      :async:

      Đưa barrier về trạng thái mặc định, rỗng. Mọi task đang chờ trên đó sẽ nhận được exception :class:`BrokenBarrierError`.

      Nếu barrier bị phá vỡ, có thể tốt hơn là cứ để nguyên và tạo một barrier mới.

   .. method:: abort()
      :async:

      Đưa barrier vào trạng thái bị phá vỡ. Điều này khiến mọi lệnh gọi đang hoạt động hoặc trong tương lai đến :meth:`~Barrier.wait` thất bại với :class:`BrokenBarrierError`. Ví dụ, hãy sử dụng cách này nếu một trong các task cần hủy bỏ, để tránh các task phải chờ vô hạn.

   .. attribute:: parties

      Số lượng task cần thiết để vượt qua barrier.

   .. attribute:: n_waiting

      Số lượng task hiện đang chờ trong barrier khi barrier đang được lấp đầy.

   .. attribute:: broken

      Một giá trị boolean là ``True`` nếu barrier đang ở trạng thái bị phá vỡ.


.. exception:: BrokenBarrierError

   Ngoại lệ này, một lớp con của :exc:`RuntimeError`, được phát sinh khi
   đối tượng :class:`Barrier` được đặt lại hoặc bị hỏng.

---------


.. versionchanged:: 3.9

   Việc acquiring lock bằng ``await lock`` hoặc ``yield from lock`` và/hoặc
   câu lệnh :keyword:`with` (``with await lock``, ``with (yield from lock)``) đã bị loại bỏ. Thay vào đó, hãy sử dụng ``async with lock``.
