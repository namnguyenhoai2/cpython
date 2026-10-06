.. currentmodule:: asyncio


===================
Mục lục API cấp cao
===================

Trang này liệt kê tất cả API asyncio cấp cao hỗ trợ async/await.


Tác vụ
======

Các tiện ích để chạy chương trình asyncio, tạo Task và chờ nhiều đối tượng với thời gian chờ.

.. list-table::
    :widths: 50 50
    :class: full-width-table

    * - :func:`run`
      - Tạo event loop, chạy coroutine, đóng loop.

    * - :class:`Runner`
      - Một context manager giúp đơn giản hóa việc gọi nhiều hàm async.

    * - :class:`Task`
      - Đối tượng Task.

    * - :class:`TaskGroup`
      - Một context manager chứa một nhóm task. Cung cấp cách thuận tiện và đáng tin cậy để chờ tất cả task trong nhóm hoàn tất.

    * - :func:`create_task`
      - Khởi chạy một asyncio Task, sau đó trả về task đó.

    * - :func:`current_task`
      - Trả về Task hiện tại.

    * - :func:`all_tasks`
      - Trả về tất cả task chưa hoàn tất của một event loop.

    * - ``await`` :func:`sleep`
      - Tạm dừng trong một số giây.

    * - ``await`` :func:`gather`
      - Lập lịch và chờ các tác vụ chạy đồng thời.

    * - ``await`` :func:`wait_for`
      - Chạy với thời gian chờ.

    * - ``await`` :func:`shield`
      - Bảo vệ khỏi việc hủy.

    * - ``await`` :func:`wait`
      - Theo dõi quá trình hoàn tất.

    * - :func:`timeout`
      - Chạy với thời gian chờ. Hữu ích trong trường hợp ``wait_for`` không phù hợp.

    * - :func:`to_thread`
      - Chạy bất đồng bộ một hàm trong một luồng OS riêng.

    * - :func:`run_coroutine_threadsafe`
      - Lập lịch một coroutine từ một luồng OS khác.

    * - ``for in`` :func:`as_completed`
      - Theo dõi quá trình hoàn tất bằng vòng lặp ``for``.


.. rubric:: Ví dụ

* :ref:`Sử dụng asyncio.gather() để chạy các tác vụ song song <asyncio_example_gather>`.

* :ref:`Sử dụng asyncio.wait_for() để áp dụng thời gian chờ <asyncio_example_waitfor>`.

* :ref:`Hủy <asyncio_example_task_cancel>`.

* :ref:`Sử dụng asyncio.sleep() <asyncio_example_sleep>`.

* Xem thêm :ref:`trang tài liệu Tasks chính <coroutine>`.


Hàng đợi
========

Hàng đợi nên được sử dụng để phân phối công việc giữa nhiều asyncio Task, triển khai connection pool và các mẫu pub/sub.


.. list-table::
    :widths: 50 50
    :class: full-width-table

    * - :class:`Queue`
      - Một hàng đợi FIFO.

    * - :class:`PriorityQueue`
      - Một hàng đợi ưu tiên.

    * - :class:`LifoQueue`
      - Một hàng đợi LIFO.


.. rubric:: Ví dụ

* :ref:`Sử dụng asyncio.Queue để phân phối khối lượng công việc giữa nhiều Task <asyncio_example_queue_dist>`.

* Xem thêm :ref:`trang tài liệu về Queues <asyncio-queues>`.


Các tiến trình con
==================

Các tiện ích để tạo tiến trình con và chạy lệnh shell.

.. list-table::
    :widths: 50 50
    :class: full-width-table

    * - ``await`` :func:`create_subprocess_exec`
      - Tạo một tiến trình con.

    * - ``await`` :func:`create_subprocess_shell`
      - Chạy một lệnh shell.


.. rubric:: Ví dụ

* :ref:`Thực thi một lệnh shell <asyncio_example_subprocess_shell>`.

* Xem thêm tài liệu về :ref:`API subprocess <asyncio-subprocess>`.


Streams
=======

Các API cấp cao để làm việc với IO mạng.

.. list-table::
    :widths: 50 50
    :class: full-width-table

    * - ``await`` :func:`open_connection`
      -  Thiết lập kết nối TCP.

    * - ``await`` :func:`open_unix_connection`
      -  Thiết lập kết nối Unix socket.

    * - ``await`` :func:`start_server`
      - Khởi động máy chủ TCP.

    * - ``await`` :func:`start_unix_server`
      - Khởi động máy chủ Unix socket.

    * - :class:`StreamReader`
      - Đối tượng async/await cấp cao để nhận dữ liệu mạng.

    * - :class:`StreamWriter`
      - Đối tượng async/await cấp cao để gửi dữ liệu mạng.


.. rubric:: Ví dụ

* :ref:`Ví dụ về TCP client <asyncio_example_stream>`.

* Xem thêm tài liệu về :ref:`streams APIs <asyncio-streams>`.


Đồng bộ hóa
===========

Các primitive đồng bộ hóa tương tự threading có thể được sử dụng trong Tasks.

.. list-table::
    :widths: 50 50
    :class: full-width-table

    * - :class:`Lock`
      - Một khóa mutex.

    * - :class:`Event`
      - Một đối tượng event.

    * - :class:`Condition`
      - Một đối tượng điều kiện.

    * - :class:`Semaphore`
      - Một semaphore.

    * - :class:`BoundedSemaphore`
      - Một bounded semaphore.

    * - :class:`Barrier`
      - Một đối tượng barrier.


.. rubric:: Ví dụ

* :ref:`Sử dụng asyncio.Event <asyncio_example_sync_event>`.

* :ref:`Sử dụng asyncio.Barrier <asyncio_example_barrier>`.

* Xem thêm tài liệu về asyncio
  :ref:`các primitive đồng bộ hóa <asyncio-sync>`.


Ngoại lệ
========

.. list-table::
    :widths: 50 50
    :class: full-width-table


    * - :exc:`asyncio.CancelledError`
      - Được phát sinh khi một Task bị hủy. Xem thêm :meth:`Task.cancel`.

    * - :exc:`asyncio.BrokenBarrierError`
      - Được phát sinh khi một Barrier bị hỏng. Xem thêm :meth:`Barrier.wait`.


.. rubric:: Ví dụ

* :ref:`Xử lý CancelledError để chạy mã khi có yêu cầu hủy <asyncio_example_task_cancel>`.

* Xem thêm danh sách đầy đủ về
  :ref:`các ngoại lệ dành riêng cho asyncio <asyncio-exceptions>`.
