:mod:`!sched` --- Bộ lập lịch sự kiện
=====================================

.. module:: sched
   :synopsis: Bộ lập lịch sự kiện cho mục đích chung.

.. sectionauthor:: Moshe Zadka <moshez@zadka.site.co.il>

**Mã nguồn:** :source:`Lib/sched.py`

.. index:: single: event scheduling

--------------

Mô-đun :mod:`!sched` định nghĩa một lớp triển khai bộ lập lịch sự kiện cho mục đích chung:

.. class:: scheduler(timefunc=time.monotonic, delayfunc=time.sleep)

   Lớp :class:`scheduler` định nghĩa một giao diện chung để lập lịch các sự kiện. Lớp này cần hai hàm để thực sự tương tác với “thế giới bên ngoài” --- *timefunc* phải có thể được gọi mà không cần đối số và trả về một số ("thời gian", theo bất kỳ đơn vị nào). Hàm *delayfunc* phải có thể được gọi với một đối số tương thích với đầu ra của *timefunc*, đồng thời trì hoãn trong số đơn vị thời gian tương ứng. *delayfunc* cũng sẽ được gọi với đối số ``0`` sau khi mỗi sự kiện chạy xong, để tạo cơ hội cho các thread khác chạy trong các ứng dụng đa luồng.

   .. versionchanged:: 3.3
      Các tham số *timefunc* và *delayfunc* là tùy chọn.

   .. versionchanged:: 3.3
      :class:`scheduler` class can be safely used in multi-threaded
      môi trường.

Ví dụ::

   >>> import sched, time
   >>> s = sched.scheduler(time.time, time.sleep)
   >>> def print_time(a='default'):
   ...     print("From print_time", time.time(), a)
   ...
   >>> def print_some_times():
   ...     print(time.time())
   ...     s.enter(10, 1, print_time)
   ...     s.enter(5, 2, print_time, argument=('positional',))
   ...     # mặc dù có độ ưu tiên cao hơn, 'keyword' chạy sau 'positional' vì enter() mang tính tương đối
   ...     s.enter(5, 1, print_time, kwargs={'a': 'keyword'})
   ...     s.enterabs(1_650_000_000, 10, print_time, argument=("first enterabs",))
   ...     s.enterabs(1_650_000_000, 5, print_time, argument=("second enterabs",))
   ...     s.run()
   ...     print(time.time())
   ...
   >>> print_some_times()
   1652342830.3640375
   From print_time 1652342830.3642538 second enterabs
   From print_time 1652342830.3643398 first enterabs
   From print_time 1652342835.3694863 positional
   From print_time 1652342835.3696074 keyword
   From print_time 1652342840.369612 default
   1652342840.3697174


.. _scheduler-objects:

Đối tượng Scheduler
-------------------

Các instance :class:`scheduler` có các phương thức và thuộc tính sau:


.. method:: scheduler.enterabs(time, priority, action, argument=(), kwargs={})

   Lập lịch một sự kiện mới. Đối số *time* phải là một kiểu số tương thích với giá trị trả về của hàm *timefunc* được truyền vào hàm khởi tạo. Các sự kiện được lập lịch cho cùng một *time* sẽ được thực thi theo thứ tự *priority* của chúng. Số nhỏ hơn biểu thị độ ưu tiên cao hơn.

   Thực thi sự kiện có nghĩa là thực thi ``action(*argument, **kwargs)``. *argument* là một sequence chứa các đối số positional cho *action*. *kwargs* là một dictionary chứa các đối số keyword cho *action*.

   Giá trị trả về là một sự kiện có thể được dùng để hủy sự kiện sau đó (xem :meth:`cancel`).

   .. versionchanged:: 3.3
      Tham số *argument* là tùy chọn.

   .. versionchanged:: 3.3
      Đã thêm tham số *kwargs*.


.. method:: scheduler.enter(delay, priority, action, argument=(), kwargs={})

   Lập lịch một sự kiện sau thêm *delay* đơn vị thời gian. Ngoài thời gian tương đối, các đối số khác, hiệu ứng và giá trị trả về giống như của
   :meth:`enterabs`.

   .. versionchanged:: 3.3
      Tham số *argument* là tùy chọn.

   .. versionchanged:: 3.3
      Đã thêm tham số *kwargs*.

.. method:: scheduler.cancel(event)

   Xóa sự kiện khỏi hàng đợi. Nếu *event* không phải là một sự kiện hiện đang nằm trong hàng đợi, phương thức này sẽ raise một :exc:`ValueError`.


.. method:: scheduler.empty()

   Trả về ``True`` nếu hàng đợi sự kiện trống.


.. method:: scheduler.run(blocking=True)

   Chạy tất cả các sự kiện đã lên lịch. Phương thức này sẽ chờ (sử dụng hàm *delayfunc* được truyền cho hàm khởi tạo) sự kiện tiếp theo, sau đó thực thi sự kiện đó và tiếp tục như vậy cho đến khi không còn sự kiện nào được lên lịch.

   Nếu *blocking* là false, ngay lập tức thực thi tất cả các sự kiện trong hàng đợi có giá trị thời gian nhỏ hơn hoặc bằng giá trị *timefunc* hiện tại (nếu có), rồi trả về chênh lệch giữa giá trị *timefunc* hiện tại và giá trị thời gian của sự kiện tiếp theo được lên lịch trong hàng đợi sự kiện của scheduler. Nếu hàng đợi trống, trả về ``None``.

   *action* hoặc *delayfunc* đều có thể phát sinh ngoại lệ. Trong cả hai trường hợp, scheduler sẽ duy trì trạng thái nhất quán và truyền tiếp ngoại lệ. Nếu ngoại lệ được phát sinh bởi *action*, sự kiện đó sẽ không được thử thực thi trong các lần gọi :meth:`run` sau.

   Nếu một chuỗi sự kiện mất nhiều thời gian thực thi hơn khoảng thời gian có sẵn trước sự kiện tiếp theo, scheduler sẽ đơn giản bị chậm lại. Không có sự kiện nào bị loại bỏ; mã gọi có trách nhiệm hủy các sự kiện không còn phù hợp.

   .. versionchanged:: 3.3
      Đã thêm tham số *blocking*.

.. attribute:: scheduler.queue

   Thuộc tính chỉ đọc, trả về danh sách các sự kiện sắp tới theo thứ tự chúng sẽ được chạy. Mỗi sự kiện được hiển thị dưới dạng một :term:`named tuple` với các trường sau: time, priority, action, argument, kwargs.
