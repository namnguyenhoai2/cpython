.. currentmodule:: asyncio


==========
Trình chạy
==========

**Mã nguồn:** :source:`Lib/asyncio/runners.py`


Phần này trình bày các primitive asyncio cấp cao để chạy mã asyncio.

Chúng được xây dựng trên :ref:`vòng lặp sự kiện <asyncio-event-loop>` với mục tiêu đơn giản hóa việc sử dụng mã bất đồng bộ trong các tình huống phổ biến.

.. contents::
   :depth: 1
   :local:



Chạy một chương trình asyncio
=============================

.. function:: run(coro, *, debug=None, loop_factory=None)

   Thực thi *coro* trong một event loop của asyncio và trả về kết quả.

   Đối số có thể là bất kỳ đối tượng awaitable nào.

   Hàm này chạy awaitable, đảm nhiệm việc quản lý event loop của asyncio, *hoàn tất các asynchronous generator*, và đóng executor.

   Không thể gọi hàm này khi một event loop khác của asyncio đang chạy trong cùng thread.

   Nếu *debug* là ``True``, event loop sẽ chạy ở chế độ debug. ``False`` tắt chế độ debug một cách rõ ràng. ``None`` được dùng để tuân theo các thiết lập toàn cục
   :ref:`asyncio-debug-mode`.

   Nếu *loop_factory* không phải là ``None``, nó sẽ được dùng để tạo event loop mới; nếu không, :func:`asyncio.new_event_loop` sẽ được dùng. Loop được đóng khi kết thúc. Nên dùng hàm này làm điểm vào chính cho các chương trình asyncio và lý tưởng nhất là chỉ gọi hàm này một lần. Khuyến nghị sử dụng *loop_factory* để cấu hình event loop thay vì các policy. Truyền :class:`asyncio.EventLoop` cho phép chạy asyncio mà không cần hệ thống policy.

   Executor được cấp thời lượng chờ 5 phút để tắt. Nếu executor chưa hoàn tất trong khoảng thời gian đó, một cảnh báo sẽ được phát ra và executor sẽ được đóng.

   Ví dụ::

       async def main():
           await asyncio.sleep(1)
           print('hello')

       asyncio.run(main())

   .. versionadded:: 3.7

   .. versionchanged:: 3.9
      Đã cập nhật để sử dụng :meth:`loop.shutdown_default_executor`.

   .. versionchanged:: 3.10

      *debug* được ``None`` theo mặc định để tuân theo các thiết lập debug toàn cục.

   .. versionchanged:: 3.12

      Đã thêm tham số *loop_factory*.

   .. versionchanged:: 3.14

      *coro* có thể là bất kỳ đối tượng awaitable nào.

   .. note::

      Hệ thống :mod:`!asyncio` policy đã lỗi thời và sẽ bị xóa trong Python 3.16; kể từ đó, cần có *loop_factory* tường minh để cấu hình event loop.


Trình quản lý ngữ cảnh Runner
=============================

.. class:: Runner(*, debug=None, loop_factory=None)

   Một trình quản lý ngữ cảnh giúp đơn giản hóa việc gọi *multiple* hàm async trong cùng một ngữ cảnh.

   Đôi khi cần gọi một số hàm async cấp cao nhất trong cùng một :ref:`event loop <asyncio-event-loop>` và :class:`contextvars.Context`.

   Nếu *debug* là ``True``, event loop sẽ chạy ở chế độ debug. ``False`` tắt chế độ debug một cách rõ ràng. ``None`` được dùng để tôn trọng các thiết lập chung
   :ref:`asyncio-debug-mode`.

   *loop_factory* có thể được dùng để ghi đè việc tạo loop. Trách nhiệm của *loop_factory* là đặt loop được tạo làm loop hiện tại. Theo mặc định, :func:`asyncio.new_event_loop` được sử dụng và đặt làm event loop hiện tại bằng :func:`asyncio.set_event_loop` nếu *loop_factory* là ``None``.

   Về cơ bản, :func:`asyncio.run` ví dụ có thể được viết lại bằng cách sử dụng runner::

        async def main():
            await asyncio.sleep(1)
            print('hello')

        with asyncio.Runner() as runner:
            runner.run(main())

   .. versionadded:: 3.11

   .. method:: run(coro, *, context=None)

      Thực thi *coro* trong event loop được nhúng.

      Đối số có thể là bất kỳ đối tượng awaitable nào.

      Nếu đối số là một coroutine, nó sẽ được bọc trong một Task.

      Đối số chỉ dành cho từ khóa *context* tùy chọn cho phép chỉ định một :class:`contextvars.Context` tùy chỉnh để mã chạy trong đó. Context mặc định của runner được sử dụng nếu context là ``None``.

      Trả về kết quả của awaitable hoặc phát sinh một exception.

      Không thể gọi hàm này khi một event loop asyncio khác đang chạy trong cùng thread.

      .. versionchanged:: 3.14

         *coro* có thể là bất kỳ đối tượng awaitable nào.

   .. method:: close()

      Đóng runner.

      Hoàn tất các asynchronous generator, tắt default executor, đóng event loop và giải phóng :class:`contextvars.Context` được nhúng.

   .. method:: get_loop()

      Trả về event loop được liên kết với runner instance.

   .. note::

      :class:`Runner` sử dụng chiến lược khởi tạo lười, constructor của nó không khởi tạo các cấu trúc cấp thấp bên dưới.

      *loop* và *context* được nhúng sẽ được tạo khi bắt đầu đi vào phần thân của :keyword:`with` hoặc trong lần gọi đầu tiên đến :meth:`run` hay :meth:`get_loop`.


Xử lý việc ngắt bằng bàn phím
=============================

.. versionadded:: 3.11

Khi :const:`signal.SIGINT` được :kbd:`Ctrl-C` phát sinh, ngoại lệ :exc:`KeyboardInterrupt` mặc định được phát sinh trong main thread. Tuy nhiên, cách này không hoạt động với
:mod:`asyncio` vì nó có thể làm gián đoạn các thành phần nội bộ của asyncio và khiến chương trình bị treo khi thoát.

Để giảm thiểu vấn đề này, :mod:`asyncio` xử lý :const:`signal.SIGINT` như sau:

1. :meth:`asyncio.Runner.run` cài đặt một bộ xử lý :const:`signal.SIGINT` tùy chỉnh trước khi bất kỳ mã người dùng nào được thực thi và gỡ bỏ bộ xử lý này khi thoát khỏi hàm.
2. :class:`~asyncio.Runner` tạo task chính để thực thi coroutine được truyền vào.
3. Khi :const:`signal.SIGINT` được :kbd:`Ctrl-C` raise, bộ xử lý tín hiệu tùy chỉnh sẽ hủy task chính bằng cách gọi :meth:`asyncio.Task.cancel`, lệnh này raise
   :exc:`asyncio.CancelledError` bên trong task chính. Điều này khiến stack Python unwind; các block ``try/except`` và ``try/finally`` có thể được dùng để dọn dẹp tài nguyên. Sau khi task chính bị hủy, :meth:`asyncio.Runner.run` raise
   :exc:`KeyboardInterrupt`.
4. Người dùng có thể viết một vòng lặp chặt không thể bị ngắt bởi
   :meth:`asyncio.Task.cancel`; trong trường hợp đó, lần :kbd:`Ctrl-C` thứ hai ngay sau đó sẽ lập tức raise :exc:`KeyboardInterrupt` mà không hủy task chính.
