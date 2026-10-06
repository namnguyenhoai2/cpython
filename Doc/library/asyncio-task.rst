.. currentmodule:: asyncio


=================
Coroutine và task
=================

Phần này trình bày các API asyncio cấp cao để làm việc với coroutine và Task.

.. contents::
   :depth: 1
   :local:


.. _coroutine:

Coroutine
=========

**Mã nguồn:** :source:`Lib/asyncio/coroutines.py`

----------------------------------------------------

:term:`Coroutine <coroutine>` được khai báo bằng cú pháp async/await là cách được khuyến nghị để viết các ứng dụng asyncio. Ví dụ, đoạn mã sau in ra "hello", chờ 1 giây, rồi in ra "world"::

    >>> import asyncio

    >>> async def main():
    ...     print('hello')
    ...     await asyncio.sleep(1)
    ...     print('world')

    >>> asyncio.run(main())
    hello
    world

Lưu ý rằng chỉ gọi một coroutine sẽ không lên lịch để coroutine đó được thực thi::

    >>> main()
    <coroutine object main at 0x1053bb7c8>

Để thực sự chạy một coroutine, asyncio cung cấp các cơ chế sau:

* Hàm :func:`asyncio.run` để chạy hàm entry point cấp cao nhất "main()" (xem ví dụ ở trên.)

* Chờ một coroutine. Đoạn mã sau sẽ in "hello" sau khi chờ 1 giây, rồi in "world" sau khi chờ *một* 2 giây::

      import asyncio
      import time

      async def say_after(delay, what):
          await asyncio.sleep(delay)
          print(what)

      async def main():
          print(f"started at {time.strftime('%X')}")

          await say_after(1, 'hello')
          await say_after(2, 'world')

          print(f"finished at {time.strftime('%X')}")

      asyncio.run(main())

  Kết quả dự kiến::

      started at 17:13:52
      hello
      world
      finished at 17:13:55

* Hàm :func:`asyncio.create_task` để chạy đồng thời các coroutine dưới dạng asyncio :class:`Tasks <Task>`.

  Hãy sửa đổi ví dụ trên và chạy hai ``say_after`` coroutine *đồng thời*::

      async def main():
          task1 = asyncio.create_task(
              say_after(1, 'hello'))

          task2 = asyncio.create_task(
              say_after(2, 'world'))

          print(f"started at {time.strftime('%X')}")

          # Chờ cho đến khi cả hai task hoàn tất (mất khoảng
          # 2 giây.)
          await task1
          await task2

          print(f"finished at {time.strftime('%X')}")

  Lưu ý rằng kết quả đầu ra dự kiến hiện cho thấy đoạn mã chạy nhanh hơn 1 giây so với trước đây::

      started at 17:14:32
      hello
      world
      finished at 17:14:34

* Lớp :class:`asyncio.TaskGroup` cung cấp một lựa chọn hiện đại hơn cho :func:`create_task`. Khi sử dụng API này, ví dụ cuối cùng trở thành::

      async def main():
          async with asyncio.TaskGroup() as tg:
              task1 = tg.create_task(
                  say_after(1, 'hello'))

              task2 = tg.create_task(
                  say_after(2, 'world'))

              print(f"started at {time.strftime('%X')}")

          # Việc await được thực hiện ngầm khi trình quản lý ngữ cảnh thoát.

          print(f"finished at {time.strftime('%X')}")

  Thời gian và kết quả đầu ra sẽ giống như ở phiên bản trước.

  .. versionadded:: 3.11
     :class:`asyncio.TaskGroup`.


.. _asyncio-awaitables:

Các đối tượng có thể await
==========================

Chúng ta gọi một đối tượng là đối tượng **awaitable** nếu nó có thể được sử dụng trong một biểu thức :keyword:`await`. Nhiều API của asyncio được thiết kế để chấp nhận các awaitable.

Có ba loại đối tượng *awaitable* chính: **coroutines**, **Tasks** và **Futures**.


.. rubric:: Các coroutine

Các coroutine Python là *awaitable* và do đó có thể được await từ các coroutine khác::

    import asyncio

    async def nested():
        return 42

    async def main():
        # Sẽ không có gì xảy ra nếu chỉ gọi "nested()".
        # Một đối tượng coroutine được tạo nhưng không được await,
        # vì vậy nó *sẽ hoàn toàn không chạy*.
        nested()  # sẽ tạo ra một "RuntimeWarning".

        # Bây giờ hãy làm theo cách khác và await nó:
        print(await nested())  # sẽ in "42".

    asyncio.run(main())

.. important::

   Trong tài liệu này, thuật ngữ "coroutine" có thể được dùng cho hai khái niệm có liên quan chặt chẽ:

   * một *hàm coroutine*: một :keyword:`async def` hàm;

   * một *đối tượng coroutine*: một đối tượng được trả về khi gọi một *hàm coroutine*.


.. rubric:: Task

*Task* được dùng để lập lịch cho các coroutine *đồng thời*.

Khi một coroutine được bọc trong một *Task* bằng các hàm như
:func:`asyncio.create_task` coroutine được tự động lên lịch để sớm chạy::

    import asyncio

    async def nested():
        return 42

    async def main():
        # Lên lịch để nested() sớm chạy đồng thời
        # với "main()".
        task = asyncio.create_task(nested())

        # Có thể dùng "task" để hủy "nested()", hoặc
        # chỉ cần await để chờ cho đến khi hoàn tất:
        await task

    asyncio.run(main())


.. rubric:: Futures

Một :class:`Future` là một đối tượng awaitable **cấp thấp** đặc biệt, đại diện cho **kết quả sau cùng** của một thao tác bất đồng bộ.

Khi một đối tượng Future được *awaited*, điều đó có nghĩa là coroutine sẽ chờ cho đến khi Future được resolve ở một nơi khác.

Các đối tượng Future trong asyncio cần thiết để cho phép sử dụng mã dựa trên callback cùng với async/await.

Thông thường, **there is no need** phải tạo các đối tượng Future ở cấp mã ứng dụng.

Các đối tượng Future, đôi khi được các thư viện và một số API của asyncio cung cấp, có thể được await::

    async def main():
        await function_that_returns_a_future_object()

        # điều này cũng hợp lệ:
        await asyncio.gather(
            function_that_returns_a_future_object(),
            some_python_coroutine()
        )

Một ví dụ điển hình về hàm cấp thấp trả về một đối tượng Future là :meth:`loop.run_in_executor`.


Tạo task
========

**Mã nguồn:** :source:`Lib/asyncio/tasks.py`

-----------------------------------------------

.. function:: create_task(coro, *, name=None, context=None, eager_start=None, **kwargs)

   Đóng gói *coro* :ref:`coroutine <coroutine>` vào một :class:`Task` và lên lịch thực thi. Trả về đối tượng Task.

   Chữ ký hàm đầy đủ phần lớn giống với chữ ký của
   :class:`Task` constructor (hoặc factory) - tất cả đối số từ khóa của hàm này được truyền tiếp đến interface đó.

   Đối số chỉ từ khóa tùy chọn *context* cho phép chỉ định một :class:`contextvars.Context` tùy chỉnh để *coro* chạy trong đó. Bản sao của context hiện tại sẽ được tạo khi không cung cấp *context*.

   Đối số chỉ từ khóa tùy chọn *eager_start* cho phép chỉ định liệu task có được thực thi ngay trong lúc gọi create_task hay được lên lịch sau đó. Nếu không truyền *eager_start*, chế độ do :meth:`loop.set_task_factory` thiết lập sẽ được sử dụng.

   Task được thực thi trong loop do :func:`get_running_loop` trả về,
   :exc:`RuntimeError` được đưa ra nếu không có loop đang chạy trong thread hiện tại.

   .. note::

      :meth:`asyncio.TaskGroup.create_task` là một lựa chọn thay thế mới tận dụng structural concurrency; cho phép chờ một nhóm các task liên quan với những đảm bảo an toàn chặt chẽ.

   .. important::

      Hãy lưu một tham chiếu đến kết quả của hàm này để tránh việc một task biến mất giữa chừng khi đang thực thi. Event loop chỉ giữ các tham chiếu yếu đến các task. Một task không được tham chiếu ở nơi khác có thể bị garbage collection bất kỳ lúc nào, ngay cả trước khi hoàn tất. Để các task nền "fire-and-forget" hoạt động đáng tin cậy, hãy tập hợp chúng trong một collection::

          background_tasks = set()

          for i in range(10):
              task = asyncio.create_task(some_coro(param=i))

              # Thêm task vào set. Việc này tạo một tham chiếu mạnh.
              background_tasks.add(task)

              # Để tránh giữ các tham chiếu đến những task đã hoàn tất mãi mãi,
              # hãy để mỗi task tự xóa tham chiếu của nó khỏi set sau khi
              # hoàn tất:
              task.add_done_callback(background_tasks.discard)

      Lưu ý rằng cách tiếp cận này không bao giờ await các task, vì vậy nếu một task gặp lỗi, exception của nó sẽ không bao giờ được lấy ra và asyncio sẽ ghi log thông báo "Task exception was never retrieved" khi task được garbage collect. Để tránh điều này, hãy sử dụng :class:`asyncio.TaskGroup`, công cụ này giữ tham chiếu mạnh đến từng task, await chúng và truyền lại các exception của chúng::

          async with asyncio.TaskGroup() as tg:
              for i in range(10):
                  tg.create_task(some_coro(param=i))

   .. versionadded:: 3.7

   .. versionchanged:: 3.8
      Đã thêm tham số *name*.

   .. versionchanged:: 3.11
      Đã thêm tham số *context*.

   .. versionchanged:: 3.14
      Đã thêm tham số *eager_start* bằng cách truyền tất cả *kwargs*.


Hủy task
========

Các task có thể được hủy một cách dễ dàng và an toàn. Khi một task bị hủy, :exc:`asyncio.CancelledError` sẽ được phát sinh trong task vào thời điểm thích hợp tiếp theo.

Khuyến nghị coroutine sử dụng các block ``try/finally`` để thực hiện logic dọn dẹp một cách đáng tin cậy. Nếu :exc:`asyncio.CancelledError` được bắt một cách rõ ràng, thông thường nên truyền lại nó sau khi hoàn tất việc dọn dẹp. :exc:`asyncio.CancelledError` kế thừa trực tiếp
:exc:`BaseException` vì vậy hầu hết mã sẽ không cần biết về nó.

Các thành phần asyncio cho phép concurrency có cấu trúc, chẳng hạn như
:class:`asyncio.TaskGroup` và :func:`asyncio.timeout`, được triển khai nội bộ bằng cơ chế hủy và có thể hoạt động không đúng nếu một coroutine nuốt :exc:`asyncio.CancelledError`. Tương tự, mã do người dùng viết nhìn chung không nên gọi :meth:`uncancel <asyncio.Task.uncancel>`. Tuy nhiên, trong những trường hợp thực sự cần bỏ qua :exc:`asyncio.CancelledError`, cũng cần gọi ``uncancel()`` để loại bỏ hoàn toàn trạng thái hủy.

.. _taskgroups:

Nhóm task
=========

Nhóm task kết hợp API tạo task với một cách thuận tiện và đáng tin cậy để chờ tất cả task trong nhóm hoàn tất.

.. class:: TaskGroup()

   Một :ref:`trình quản lý ngữ cảnh bất đồng bộ <async-context-managers>` chứa một nhóm task. Có thể thêm task vào nhóm bằng :meth:`create_task`. Tất cả task sẽ được await khi trình quản lý ngữ cảnh kết thúc.

   .. versionadded:: 3.11

   .. method:: create_task(coro, *, name=None, context=None, eager_start=None, **kwargs)

      Tạo một task trong nhóm task này. Chữ ký khớp với :func:`asyncio.create_task`. Nếu nhóm task không hoạt động (ví dụ: chưa được truy cập, đã hoàn tất hoặc đang trong quá trình tắt), chúng ta sẽ đóng ``coro`` đã cho và phát sinh :exc:`RuntimeError`.

      .. versionchanged:: 3.13

         Đóng coroutine đã cho nếu nhóm tác vụ không hoạt động.

      .. versionchanged:: 3.14

         Truyền tất cả *kwargs* tới :meth:`loop.create_task`

Ví dụ::

    async def main():
        async with asyncio.TaskGroup() as tg:
            task1 = tg.create_task(some_coro(...))
            task2 = tg.create_task(another_coro(...))
        print(f"Both tasks have completed now: {task1.result()}, {task2.result()}")

Câu lệnh ``async with`` sẽ chờ tất cả tác vụ trong nhóm hoàn tất. Trong khi chờ, bạn vẫn có thể thêm các tác vụ mới vào nhóm (ví dụ: bằng cách truyền ``tg`` vào một trong các coroutine và gọi ``tg.create_task()`` trong coroutine đó). Sau khi tác vụ cuối cùng hoàn tất và thoát khỏi khối ``async with``, không thể thêm tác vụ mới nào vào nhóm.

Lần đầu tiên bất kỳ tác vụ nào thuộc nhóm bị lỗi với một ngoại lệ không phải :exc:`asyncio.CancelledError`, các tác vụ còn lại trong nhóm sẽ bị hủy. Sau đó không thể thêm tác vụ nào khác vào nhóm. Tại thời điểm này, nếu phần thân của câu lệnh ``async with`` vẫn đang hoạt động (tức là :meth:`~object.__aexit__` chưa được gọi), tác vụ trực tiếp chứa câu lệnh ``async with`` cũng sẽ bị hủy. :exc:`asyncio.CancelledError` phát sinh sẽ ngắt một ``await``, nhưng sẽ không nổi lên khỏi câu lệnh ``async with`` chứa nó.

Sau khi tất cả tác vụ hoàn tất, nếu có tác vụ nào bị lỗi với một ngoại lệ không phải :exc:`asyncio.CancelledError`, các ngoại lệ đó sẽ được kết hợp trong một
:exc:`ExceptionGroup` hoặc :exc:`BaseExceptionGroup` (tùy trường hợp; xem tài liệu tương ứng), sau đó được phát sinh.

Hai base exception được xử lý đặc biệt: Nếu bất kỳ task nào thất bại với :exc:`KeyboardInterrupt` hoặc :exc:`SystemExit`, task group vẫn hủy các task còn lại và chờ chúng, nhưng sau đó :exc:`KeyboardInterrupt` hoặc :exc:`SystemExit` ban đầu sẽ được raise lại thay vì :exc:`ExceptionGroup` hoặc :exc:`BaseExceptionGroup`.

Nếu phần thân của câu lệnh ``async with`` thoát với một exception (do đó :meth:`~object.__aexit__` được gọi khi đã thiết lập exception), trường hợp này được xử lý giống như khi một trong các task thất bại: các task còn lại bị hủy rồi được chờ hoàn tất, và các exception không phải do hủy sẽ được nhóm vào một exception group rồi raise. Exception được truyền vào :meth:`~object.__aexit__`, trừ khi đó là :exc:`asyncio.CancelledError`, cũng được đưa vào exception group. Trường hợp đặc biệt tương tự cũng được áp dụng cho
:exc:`KeyboardInterrupt` và :exc:`SystemExit` như trong đoạn trước.

Task group cẩn thận không nhầm lẫn việc hủy nội bộ được dùng để "đánh thức" :meth:`~object.__aexit__` của chúng với các yêu cầu hủy task mà chúng đang chạy, được thực hiện bởi các bên khác. Cụ thể, khi một task group được lồng về mặt cú pháp bên trong một task group khác, và cả hai đồng thời gặp exception trong một task con của chúng, task group bên trong sẽ xử lý các exception của mình, sau đó task group bên ngoài sẽ nhận một yêu cầu hủy khác và xử lý các exception của chính nó.

Trong trường hợp một task group bị hủy từ bên ngoài và đồng thời phải raise một :exc:`ExceptionGroup`, nó sẽ gọi phương thức
:meth:`~asyncio.Task.cancel` của task cha. Điều này đảm bảo rằng một
:exc:`asyncio.CancelledError` sẽ được raise ở lần tiếp theo
:keyword:`await`, vì vậy việc hủy không bị mất.

Các nhóm tác vụ bảo toàn số lần hủy do :meth:`asyncio.Task.cancelling` báo cáo.

.. versionchanged:: 3.13

   Cải thiện việc xử lý các thao tác hủy nội bộ và bên ngoài đồng thời, đồng thời bảo toàn chính xác số lần hủy.

Kết thúc một nhóm tác vụ
------------------------

Mặc dù thư viện chuẩn không hỗ trợ việc kết thúc một nhóm tác vụ một cách nguyên gốc, bạn có thể thực hiện việc này bằng cách thêm một tác vụ tạo ngoại lệ vào nhóm tác vụ và bỏ qua ngoại lệ được tạo ra:

.. code-block:: python

   import asyncio
   from asyncio import TaskGroup

   class TerminateTaskGroup(Exception):
       """Exception raised to terminate a task group."""

   async def force_terminate_task_group():
       """Used to force termination of a task group."""
       raise TerminateTaskGroup()

   async def job(task_id, sleep_time):
       print(f'Task {task_id}: start')
       await asyncio.sleep(sleep_time)
       print(f'Task {task_id}: done')

   async def main():
       try:
           async with TaskGroup() as group:
               # tạo một số tác vụ
               group.create_task(job(1, 0.5))
               group.create_task(job(2, 1.5))
               # ngủ trong 1 giây
               await asyncio.sleep(1)
               # thêm một task phát sinh ngoại lệ để buộc nhóm kết thúc
               group.create_task(force_terminate_task_group())
       except* TerminateTaskGroup:
           pass

   asyncio.run(main())

Đầu ra dự kiến:

.. code-block:: text

   Task 1: start
   Task 2: start
   Task 1: done

Ngủ
===

.. function:: sleep(delay, result=None)
   :async:

   Tạm dừng trong *delay* giây.

   Nếu cung cấp *result*, giá trị này sẽ được trả về cho caller khi coroutine hoàn tất.

   ``sleep()`` luôn tạm dừng task hiện tại, cho phép các task khác chạy.

   Đặt thời gian trễ bằng 0 sẽ cung cấp một nhánh được tối ưu hóa để cho phép các task khác chạy. Có thể sử dụng cách này trong các hàm chạy lâu để tránh chặn event loop trong toàn bộ thời gian thực thi hàm.

   .. _asyncio_example_sleep:

   Ví dụ về coroutine hiển thị ngày hiện tại mỗi giây trong 5 giây::

    import asyncio
    import datetime as dt

    async def display_date():
        loop = asyncio.get_running_loop()
        end_time = loop.time() + 5.0
        while True:
            print(dt.datetime.now())
            if (loop.time() + 1.0) >= end_time:
                break
            await asyncio.sleep(1)

    asyncio.run(display_date())


   .. versionchanged:: 3.10
      Đã xóa tham số *loop*.

   .. versionchanged:: 3.13
      Phát sinh :exc:`ValueError` nếu *delay* là :data:`~math.nan`.


Chạy các task đồng thời
=======================

.. awaitablefunction:: gather(*aws, return_exceptions=False)

   Chạy :ref:`awaitable objects <asyncio-awaitables>` trong chuỗi *aws* một cách *concurrently*.

   Nếu bất kỳ awaitable nào trong *aws* là một coroutine, nó sẽ tự động được lập lịch dưới dạng một Task.

   Nếu tất cả awaitable hoàn tất thành công, kết quả là một danh sách tổng hợp các giá trị được trả về. Thứ tự của các giá trị kết quả tương ứng với thứ tự của các awaitable trong *aws*.

   Nếu *return_exceptions* là ``False`` (mặc định), ngoại lệ đầu tiên được phát sinh sẽ ngay lập tức được truyền đến task đang await ``gather()``. Các awaitable khác trong chuỗi *aws* **won't be cancelled** và sẽ tiếp tục chạy.

   Nếu *return_exceptions* là ``True``, các ngoại lệ được xử lý giống như các kết quả thành công và được gom vào danh sách kết quả.

   Nếu ``gather()`` bị *cancelled*, tất cả awaitable đã được gửi (nhưng chưa hoàn tất) cũng sẽ bị *cancelled*.

   Nếu bất kỳ Task hoặc Future nào trong chuỗi *aws* bị *cancelled*, nó được xử lý như thể đã phát sinh :exc:`CancelledError` -- lệnh gọi ``gather()`` **not** bị hủy trong trường hợp này. Điều này nhằm ngăn việc hủy một Task/Future đã gửi khiến các Task/Future khác bị hủy.

   .. note::
      Một lựa chọn mới để tạo và chạy đồng thời các task rồi chờ chúng hoàn tất là :class:`asyncio.TaskGroup`. *TaskGroup* cung cấp các bảo đảm an toàn mạnh hơn *gather* khi lập lịch cho các subtasks lồng nhau: nếu một task (hoặc một subtask, tức task được một task lập lịch) phát sinh ngoại lệ, *TaskGroup* sẽ hủy các task còn lại đã được lập lịch, còn *gather* thì không.

   .. _asyncio_example_gather:

   Ví dụ::

      import asyncio

      async def factorial(name, number):
          f = 1
          for i in range(2, number + 1):
              print(f"Task {name}: Compute factorial({number}), currently i={i}...")
              await asyncio.sleep(1)
              f *= i
          print(f"Task {name}: factorial({number}) = {f}")
          return f

      async def main():
          # Lập lịch đồng thời cho ba lệnh gọi *concurrently*:
          L = await asyncio.gather(
              factorial("A", 2),
              factorial("B", 3),
              factorial("C", 4),
          )
          print(L)

      asyncio.run(main())

      # Kết quả mong đợi:
      #
      #     Tác vụ A: Tính factorial(2), hiện tại i=2...
      #     Tác vụ B: Tính factorial(3), hiện tại i=2...
      #     Tác vụ C: Tính factorial(4), hiện tại i=2...
      #     Tác vụ A: factorial(2) = 2
      #     Tác vụ B: Tính factorial(3), hiện tại i=3...
      #     Tác vụ C: Tính factorial(4), hiện tại i=3...
      #     Task B: factorial(3) = 6
      #     Task C: Tính factorial(4), hiện tại i=4...
      #     Task C: factorial(4) = 24
      #     [2, 6, 24]

   .. note::
      Nếu *return_exceptions* là false, việc hủy gather() sau khi nó được đánh dấu là đã hoàn tất sẽ không hủy bất kỳ awaitable nào đã được gửi. Chẳng hạn, gather có thể được đánh dấu là đã hoàn tất sau khi chuyển tiếp một exception đến caller; do đó, việc gọi ``gather.cancel()`` sau khi bắt được một exception (được raise bởi một trong các awaitable) từ gather sẽ không hủy các awaitable khác.

   .. versionchanged:: 3.7
      Nếu chính *gather* bị hủy, việc hủy sẽ được truyền tiếp bất kể *return_exceptions* là gì.

   .. versionchanged:: 3.10
      Đã loại bỏ tham số *loop*.

   .. deprecated:: 3.10
      Cảnh báo ngừng sử dụng được phát ra nếu không cung cấp đối số positional nào, hoặc không phải tất cả đối số positional đều là đối tượng dạng Future, và không có event loop đang chạy.


.. _eager-task-factory:

Bộ tạo task eager
=================

.. function:: eager_task_factory(loop, coro, *, name=None, context=None)

    Bộ tạo task để thực thi task eager.

    Khi sử dụng bộ tạo này (thông qua :meth:`loop.set_task_factory(asyncio.eager_task_factory) <loop.set_task_factory>`), các coroutine bắt đầu thực thi đồng bộ trong quá trình tạo :class:`Task`. Task chỉ được lên lịch trên event loop nếu chúng bị block. Điều này có thể cải thiện hiệu năng vì tránh được overhead của việc lên lịch trên loop đối với các coroutine hoàn tất đồng bộ.

    Một ví dụ phổ biến mà cách này hữu ích là các coroutine sử dụng caching hoặc memoization để tránh I/O thực tế khi có thể.

    .. note::

        Việc thực thi coroutine ngay lập tức là một thay đổi về ngữ nghĩa. Nếu coroutine trả về hoặc phát sinh exception, task sẽ không bao giờ được lên lịch trên event loop. Nếu quá trình thực thi coroutine bị block, task sẽ được lên lịch trên event loop. Thay đổi này có thể làm thay đổi hành vi của các ứng dụng hiện có. Ví dụ, thứ tự thực thi task của ứng dụng có khả năng sẽ thay đổi.

    .. versionadded:: 3.12

.. function:: create_eager_task_factory(custom_task_constructor)

    Tạo một bộ tạo task eager, tương tự như :func:`eager_task_factory`, sử dụng *custom_task_constructor* được cung cấp khi tạo task mới thay vì :class:`Task` mặc định.

    *custom_task_constructor* phải là một *callable* có signature khớp với signature của :class:`Task.__init__ <Task>`. Callable này phải trả về một đối tượng tương thích với :class:`asyncio.Task`.

    Hàm này trả về một *callable* được dùng làm task factory của event loop thông qua :meth:`loop.set_task_factory(factory) <loop.set_task_factory>`).

    .. versionadded:: 3.12


Bảo vệ khỏi việc hủy
====================

.. awaitablefunction:: shield(aw)

   Bảo vệ một :ref:`awaitable object <asyncio-awaitables>` khỏi bị :meth:`cancelled <Task.cancel>`.

   Nếu *aw* là một coroutine, nó sẽ tự động được lên lịch dưới dạng một Task.

   Câu lệnh::

       task = asyncio.create_task(something())
       res = await shield(task)

   tương đương với::

       res = await something()

   *except* rằng nếu coroutine chứa nó bị hủy, Task đang chạy trong ``something()`` sẽ không bị hủy. Theo quan điểm của ``something()``, việc hủy đã không xảy ra. Mặc dù caller của nó vẫn bị hủy, nên biểu thức "await" vẫn phát sinh một :exc:`CancelledError`.

   Nếu ``something()`` bị hủy bằng cách khác (tức là từ bên trong chính nó), điều đó cũng sẽ hủy ``shield()``.

   Nếu muốn hoàn toàn bỏ qua việc hủy (không khuyến nghị), nên kết hợp hàm ``shield()`` với mệnh đề try/except như sau::

       task = asyncio.create_task(something())
       try:
           res = await shield(task)
       except CancelledError:
           res = None

   .. important::

      Hãy lưu một tham chiếu đến các task được truyền vào hàm này để tránh task biến mất giữa chừng khi đang thực thi. Event loop chỉ giữ các tham chiếu yếu đến task. Một task không được tham chiếu ở nơi khác có thể bị garbage collection bất kỳ lúc nào, ngay cả trước khi hoàn tất.

   .. versionchanged:: 3.10
      Đã loại bỏ tham số *loop*.

   .. deprecated:: 3.10
      Cảnh báo ngừng sử dụng được phát ra nếu *aw* không phải là đối tượng tương tự Future và không có event loop đang chạy.


Timeout
=======

.. function:: timeout(delay)

    Trả về một :ref:`asynchronous context manager <async-context-managers>` có thể được dùng để giới hạn thời gian chờ đợi một việc nào đó.

    *delay* có thể là ``None``, hoặc một số giây dạng float/int cần chờ. Nếu *delay* là ``None``, sẽ không áp dụng giới hạn thời gian; điều này hữu ích nếu chưa biết delay khi tạo context manager.

    Trong cả hai trường hợp, context manager có thể được lên lịch lại sau khi tạo bằng :meth:`Timeout.reschedule`.

    Ví dụ::

        async def main():
            async with asyncio.timeout(10):
                await long_running_task()

    Nếu ``long_running_task`` mất hơn 10 giây để hoàn tất, context manager sẽ hủy task hiện tại và xử lý nội bộ :exc:`asyncio.CancelledError` phát sinh, chuyển nó thành :exc:`TimeoutError` để có thể bắt và xử lý.

    .. note::

      Context manager :func:`asyncio.timeout` sẽ chuyển :exc:`asyncio.CancelledError` thành :exc:`TimeoutError`, điều đó có nghĩa là chỉ có thể bắt :exc:`TimeoutError` *outside* context manager.

    Ví dụ về việc bắt :exc:`TimeoutError`::

        async def main():
            try:
                async with asyncio.timeout(10):
                    await long_running_task()
            except TimeoutError:
                print("The long operation timed out, but we've handled it.")

            print("This statement will run regardless.")

    Context manager được tạo bởi :func:`asyncio.timeout` có thể được lên lịch lại đến một thời hạn khác và được kiểm tra.

    .. class:: Timeout(when)

       Một :ref:`trình quản lý ngữ cảnh bất đồng bộ <async-context-managers>` để hủy các coroutine đã quá thời gian.

       Nên sử dụng :func:`asyncio.timeout` hoặc :func:`asyncio.timeout_at` thay vì khởi tạo trực tiếp :class:`!Timeout`.

       ``when`` phải là một thời điểm tuyệt đối mà tại đó ngữ cảnh sẽ hết thời gian chờ, được đo bằng đồng hồ của event loop:

       - Nếu ``when`` là ``None``, thời gian chờ sẽ không bao giờ được kích hoạt.
       - Nếu ``when < loop.time()``, thời gian chờ sẽ được kích hoạt ở lần lặp tiếp theo của event loop.

        .. method:: when() -> float | None

           Trả về deadline hiện tại hoặc ``None`` nếu deadline hiện tại chưa được thiết lập.

        .. method:: reschedule(when: float | None)

            Lập lịch lại thời gian chờ.

        .. method:: expired() -> bool

           Trả về liệu context manager đã vượt quá thời hạn (expired) hay chưa.

    Ví dụ::

        async def main():
            try:
                # Khi bắt đầu, chúng ta chưa biết thời gian chờ, nên truyền ``None``.
                async with asyncio.timeout(None) as cm:
                    # Bây giờ chúng ta đã biết thời gian chờ, nên lên lịch lại cho nó.
                    new_deadline = get_running_loop().time() + 10
                    cm.reschedule(new_deadline)

                    await long_running_task()
            except TimeoutError:
                pass

            if cm.expired():
                print("Looks like we haven't finished on time.")

    Các context manager timeout có thể được lồng nhau một cách an toàn.

    .. versionadded:: 3.11

.. function:: timeout_at(when)

   Tương tự như :func:`asyncio.timeout`, ngoại trừ *khi* là thời điểm tuyệt đối để dừng chờ, hoặc ``None``.

   Ví dụ::

      async def main():
          loop = get_running_loop()
          deadline = loop.time() + 20
          try:
              async with asyncio.timeout_at(deadline):
                  await long_running_task()
          except TimeoutError:
              print("The long operation timed out, but we've handled it.")

          print("This statement will run regardless.")

   .. versionadded:: 3.11

.. function:: wait_for(aw, timeout)
   :async:

   Chờ *aw* :ref:`awaitable <asyncio-awaitables>` hoàn tất trong thời gian chờ.

   *timeout* có thể là ``None`` hoặc một số giây kiểu float hoặc int cần chờ. Nếu *timeout* là ``None``, hãy chặn cho đến khi future hoàn tất.

   Nếu xảy ra timeout, hàm này sẽ hủy *aw* và ném :exc:`TimeoutError`.

   Để ngăn *aw* bị hủy, hãy bọc nó trong :func:`shield`.

   Hàm sẽ chờ cho đến khi future thực sự bị hủy, vì vậy tổng thời gian chờ có thể vượt quá *timeout*. Nếu xảy ra ngoại lệ trong quá trình hủy, ngoại lệ đó sẽ được truyền lên.

   Nếu thao tác chờ bị hủy, future *aw* cũng sẽ bị hủy.

   .. _asyncio_example_waitfor:

   Ví dụ::

       async def eternity():
           # Ngủ trong một giờ
           await asyncio.sleep(3600)
           print('yay!')

       async def main():
           # Chờ tối đa 1 giây
           try:
               await asyncio.wait_for(eternity(), timeout=1.0)
           except TimeoutError:
               print('timeout!')

       asyncio.run(main())

       # Đầu ra dự kiến:
       #
       #     timeout!

   .. versionchanged:: 3.7
      Khi *aw* bị hủy do timeout, ``wait_for`` chờ *aw* bị hủy. Trước đây, nó đã phát sinh
      :exc:`TimeoutError` ngay lập tức.

   .. versionchanged:: 3.10
      Đã loại bỏ tham số *loop*.

   .. versionchanged:: 3.11
      Nâng :exc:`TimeoutError` thay vì :exc:`asyncio.TimeoutError`.

   .. versionchanged:: 3.12
      Được triển khai bằng :func:`asyncio.timeout`, một coroutine được truyền dưới dạng *aw* sẽ không còn được bọc trong một :class:`Task` khi *timeout* có giá trị dương.


Các primitive chờ
=================

.. function:: wait(aws, *, timeout=None, return_when=ALL_COMPLETED)
   :async:

   Chạy đồng thời các instance :class:`~asyncio.Future` và :class:`~asyncio.Task` trong iterable *aws* và chặn cho đến khi điều kiện được chỉ định bởi *return_when* được thỏa mãn.

   Iterable *aws* không được để trống.

   Trả về hai tập hợp Task/Future: ``(done, pending)``.

   Cách sử dụng::

        done, pending = await asyncio.wait(aws)

   *timeout* (một số thực hoặc số nguyên), nếu được chỉ định, có thể được dùng để kiểm soát số giây tối đa cần chờ trước khi trả về.

   Lưu ý rằng hàm này không raise :exc:`TimeoutError`. Các Future hoặc Task chưa hoàn tất khi hết thời gian chờ sẽ được trả về trong tập hợp thứ hai.

   *return_when* cho biết thời điểm hàm này sẽ trả về. Giá trị này phải là một trong các hằng số sau:

   .. list-table::
      :header-rows: 1

      * - Hằng số
        - Mô tả

      * - .. data:: FIRST_COMPLETED
        - Hàm sẽ trả về khi bất kỳ future nào hoàn tất hoặc bị hủy.

      * - .. data:: FIRST_EXCEPTION
        - Hàm sẽ trả về khi bất kỳ future nào hoàn tất bằng cách raise một exception. Nếu không có future nào raise exception thì giá trị này tương đương với :const:`ALL_COMPLETED`.

      * - .. data:: ALL_COMPLETED
        - Hàm sẽ trả về khi tất cả future hoàn tất hoặc bị hủy.

   Không giống :func:`~asyncio.wait_for`, ``wait()`` không hủy các future khi xảy ra timeout.

   Nếu ``wait()`` bị hủy, các future trong *aws* sẽ không bị hủy và tiếp tục chạy.

   .. versionchanged:: 3.10
      Đã xóa tham số *loop*.

   .. versionchanged:: 3.11
      Không được phép truyền trực tiếp các đối tượng coroutine vào ``wait()``.

   .. versionchanged:: 3.12
      Đã thêm hỗ trợ cho các generator tạo ra task.


.. function:: as_completed(aws, *, timeout=None)

   Chạy đồng thời các đối tượng :ref:`awaitable objects <asyncio-awaitables>` trong iterable *aws*. Có thể lặp qua đối tượng được trả về để lấy kết quả của các awaitable khi chúng hoàn tất.

   Đối tượng được ``as_completed()`` trả về có thể được lặp qua dưới dạng một
   :term:`asynchronous iterator` hoặc một :term:`iterator` thông thường. Khi sử dụng phép lặp bất đồng bộ, các awaitable được cung cấp ban đầu sẽ được trả về nếu chúng là task hoặc future. Điều này giúp dễ dàng liên kết các task đã được lên lịch trước đó với kết quả của chúng. Ví dụ::

       ipv4_connect = create_task(open_connection("127.0.0.1", 80))
       ipv6_connect = create_task(open_connection("::1", 80))
       tasks = [ipv4_connect, ipv6_connect]

       async for earliest_connect in as_completed(tasks):
           # earliest_connect đã hoàn tất. Có thể lấy kết quả bằng cách
           # await nó hoặc gọi earliest_connect.result()
           reader, writer = await earliest_connect

           if earliest_connect is ipv6_connect:
               print("IPv6 connection established.")
           else:
               print("IPv4 connection established.")

   Trong quá trình lặp bất đồng bộ, các task được tạo ngầm sẽ được trả về đối với những awaitable được cung cấp nhưng không phải là task hoặc future.

   Khi được sử dụng như một iterator thông thường, mỗi lần lặp sẽ trả về một coroutine mới, coroutine này trả về kết quả hoặc phát sinh ngoại lệ của awaitable tiếp theo đã hoàn tất. Mẫu này tương thích với các phiên bản Python cũ hơn 3.13::

       ipv4_connect = create_task(open_connection("127.0.0.1", 80))
       ipv6_connect = create_task(open_connection("::1", 80))
       tasks = [ipv4_connect, ipv6_connect]

       for next_connect in as_completed(tasks):
           # next_connect không phải là một trong các đối tượng task ban đầu. Nó phải được
           # được await để nhận giá trị kết quả hoặc phát sinh ngoại lệ của
           # awaitable hoàn tất tiếp theo.
           reader, writer = await next_connect

   Một :exc:`TimeoutError` được phát sinh nếu hết thời gian chờ trước khi tất cả awaitable hoàn tất. Ngoại lệ này được phát sinh bởi vòng lặp ``async for`` trong quá trình lặp bất đồng bộ hoặc bởi các coroutine được yield trong quá trình lặp thông thường.

   ``as_completed()`` không hủy các task đang chạy những awaitable được cung cấp: nếu hết thời gian chờ hoặc quá trình lặp bị hủy, các task còn lại vẫn tiếp tục chạy.

   .. versionchanged:: 3.10
      Đã xóa tham số *loop*.

   .. deprecated:: 3.10
      Một cảnh báo ngừng sử dụng được phát ra nếu không phải tất cả đối tượng awaitable trong iterable *aws* đều là đối tượng dạng Future và không có event loop nào đang chạy.

   .. versionchanged:: 3.12
      Đã thêm hỗ trợ cho các generator tạo ra task.

   .. versionchanged:: 3.13
      Kết quả giờ đây có thể được sử dụng dưới dạng :term:`asynchronous iterator` hoặc dưới dạng :term:`iterator` thuần túy (trước đây nó chỉ là một iterator thuần túy).


Chạy trong các thread
=====================

.. function:: to_thread(func, /, *args, **kwargs)
   :async:

   Chạy bất đồng bộ hàm *func* trong một thread riêng biệt.

   Mọi \*args và \*\*kwargs được cung cấp cho hàm này đều được truyền trực tiếp đến *func*. Ngoài ra, :class:`contextvars.Context` hiện tại cũng được truyền tiếp, cho phép truy cập các biến context từ thread của event loop trong thread riêng biệt.

   Trả về một coroutine có thể được await để nhận kết quả sau cùng của *func*.

   Hàm coroutine này chủ yếu được dùng để thực thi các hàm/phương thức bị giới hạn bởi IO (IO-bound), vốn sẽ chặn event loop nếu được chạy trong thread chính. Ví dụ::

       def blocking_io():
           print(f"start blocking_io at {time.strftime('%X')}")
           # Lưu ý rằng time.sleep() có thể được thay thế bằng bất kỳ thao tác chặn nào
           # Tác vụ bị giới hạn bởi I/O, chẳng hạn như thao tác với tệp.
           time.sleep(1)
           print(f"blocking_io complete at {time.strftime('%X')}")

       async def main():
           print(f"started main at {time.strftime('%X')}")

           await asyncio.gather(
               asyncio.to_thread(blocking_io),
               asyncio.sleep(1))

           print(f"finished main at {time.strftime('%X')}")


       asyncio.run(main())

       # Kết quả mong đợi:
       #
       # đã bắt đầu main lúc 19:50:53
       # bắt đầu blocking_io lúc 19:50:53
       # blocking_io hoàn tất lúc 19:50:54
       # đã hoàn tất main lúc 19:50:54

   Gọi trực tiếp ``blocking_io()`` trong bất kỳ coroutine nào sẽ chặn event loop trong suốt thời gian thực thi, khiến thời gian chạy tăng thêm 1 giây. Thay vào đó, bằng cách sử dụng ``asyncio.to_thread()``, chúng ta có thể chạy nó trong một thread riêng mà không chặn event loop.

   .. note::

      Do :term:`GIL`, ``asyncio.to_thread()`` thường chỉ có thể được dùng để làm cho các hàm bị giới hạn bởi IO không chặn. Tuy nhiên, đối với các extension module giải phóng GIL hoặc các triển khai Python thay thế không có GIL, ``asyncio.to_thread()`` cũng có thể được dùng cho các hàm bị giới hạn bởi CPU.

   .. versionadded:: 3.9


Lập lịch từ các thread khác
===========================

.. function:: run_coroutine_threadsafe(coro, loop)

   Gửi một coroutine vào event loop được chỉ định. An toàn khi sử dụng từ nhiều thread.

   Trả về một :class:`concurrent.futures.Future` để chờ kết quả từ một OS thread khác.

   Hàm này được thiết kế để gọi từ một OS thread khác với thread đang chạy event loop. Ví dụ::

     def in_thread(loop: asyncio.AbstractEventLoop) -> None:
         # Chạy một thao tác IO blocking
         pathlib.Path("example.txt").write_text("hello world", encoding="utf8")

         # Tạo một coroutine
         coro = asyncio.sleep(1, result=3)

         # Gửi coroutine đến loop được chỉ định
         future = asyncio.run_coroutine_threadsafe(coro, loop)

         # Chờ kết quả với đối số timeout tùy chọn
         assert future.result(timeout=2) == 3

     async def amain() -> None:
         # Lấy loop đang chạy
         loop = asyncio.get_running_loop()

         # Chạy một tác vụ trong thread
         await asyncio.to_thread(in_thread, loop)

   Cũng có thể thực hiện theo chiều ngược lại. Ví dụ::

     @contextlib.contextmanager
     def loop_in_thread() -> Generator[asyncio.AbstractEventLoop]:
         loop_fut = concurrent.futures.Future[asyncio.AbstractEventLoop]()
         stop_event = asyncio.Event()

         async def main() -> None:
             loop_fut.set_result(asyncio.get_running_loop())
             await stop_event.wait()

         with concurrent.futures.ThreadPoolExecutor(1) as tpe:
             complete_fut = tpe.submit(asyncio.run, main())
             for fut in concurrent.futures.as_completed((loop_fut, complete_fut)):
                 if fut is loop_fut:
                     loop = loop_fut.result()
                     try:
                         yield loop
                     finally:
                         loop.call_soon_threadsafe(stop_event.set)
                 else:
                     fut.result()

     # Tạo một loop trong thread khác
     with loop_in_thread() as loop:
         # Tạo một coroutine
         coro = asyncio.sleep(1, result=3)

         # Gửi coroutine đến loop được chỉ định
         future = asyncio.run_coroutine_threadsafe(coro, loop)

         # Chờ kết quả với đối số timeout tùy chọn
         assert future.result(timeout=2) == 3

   Nếu một exception được raise trong coroutine, Future được trả về sẽ nhận thông báo. Future này cũng có thể được dùng để hủy task trong event loop::

     try:
         result = future.result(timeout)
     except TimeoutError:
         print('The coroutine took too long, cancelling the task...')
         future.cancel()
     except Exception as exc:
         print(f'The coroutine raised an exception: {exc!r}')
     else:
         print(f'The coroutine returned: {result!r}')

   Xem phần :ref:`concurrency and multithreading <asyncio-multithreading>` trong tài liệu.

   Không giống các hàm asyncio khác, hàm này yêu cầu truyền tường minh đối số *loop*.

   .. versionadded:: 3.5.1


Tự kiểm tra
===========


.. function:: current_task(loop=None)

   Trả về instance :class:`Task` đang chạy hiện tại hoặc ``None`` nếu không có task nào đang chạy.

   Nếu *loop* là ``None`` thì :func:`get_running_loop` được dùng để lấy loop hiện tại.

   .. versionadded:: 3.7


.. function:: all_tasks(loop=None)

   Trả về một tập hợp các đối tượng :class:`Task` chưa hoàn tất do loop chạy.

   Nếu *loop* là ``None`` thì :func:`get_running_loop` được dùng để lấy loop hiện tại.

   .. versionadded:: 3.7


.. function:: iscoroutine(obj)

   Trả về ``True`` nếu *obj* là một đối tượng coroutine.

   .. versionadded:: 3.4

.. _asyncio-task-obj:

Đối tượng Task
==============

.. class:: Task(coro, *, loop=None, name=None, context=None, eager_start=False)

   Một đối tượng :class:`Future-like <Future>` chạy một Python
   :ref:`coroutine <coroutine>`. Không an toàn khi sử dụng với thread.

   Task được dùng để chạy các coroutine trong event loop. Nếu một coroutine await một Future, Task sẽ tạm dừng việc thực thi coroutine và chờ Future hoàn tất. Khi Future đã *done*, việc thực thi coroutine được bao bọc sẽ tiếp tục.

   Event loop sử dụng cơ chế lập lịch hợp tác: mỗi lần event loop chỉ chạy một Task. Trong khi một Task chờ Future hoàn tất, event loop sẽ chạy các Task khác, các callback hoặc thực hiện các thao tác IO.

   Sử dụng hàm :func:`asyncio.create_task` cấp cao để tạo Task hoặc sử dụng :meth:`loop.create_task` cấp thấp hoặc
   các hàm :func:`ensure_future`. Không khuyến khích khởi tạo Task thủ công.

   Để hủy một Task đang chạy, hãy sử dụng phương thức :meth:`cancel`. Việc gọi phương thức này sẽ khiến Task ném một ngoại lệ :exc:`CancelledError` vào coroutine được bao bọc. Nếu một coroutine đang chờ một đối tượng Future trong khi bị hủy, đối tượng Future đó sẽ bị hủy.

   Có thể sử dụng :meth:`cancelled` để kiểm tra xem Task đã bị hủy hay chưa. Phương thức này trả về ``True`` nếu coroutine được bao bọc không chặn ngoại lệ :exc:`CancelledError` và thực sự đã bị hủy.

   :class:`asyncio.Task` kế thừa từ :class:`Future` toàn bộ API của nó, ngoại trừ :meth:`Future.set_result` và
   :meth:`Future.set_exception`.

   Đối số chỉ dùng dưới dạng keyword *context* tùy chọn cho phép chỉ định một :class:`contextvars.Context` tùy chỉnh để *coro* chạy trong đó. Nếu không cung cấp *context*, Task sẽ sao chép context hiện tại và sau đó chạy coroutine của nó trong context đã sao chép.

   Đối số chỉ dùng dưới dạng keyword *eager_start* tùy chọn cho phép bắt đầu thực thi :class:`asyncio.Task` ngay khi tạo task. Nếu được đặt thành ``True`` và event loop đang chạy, task sẽ bắt đầu thực thi coroutine ngay lập tức cho đến lần đầu tiên coroutine bị block. Nếu coroutine trả về hoặc phát sinh ngoại lệ mà không bị block, task sẽ được hoàn tất ngay và bỏ qua việc lên lịch vào event loop.

   Tasks là :ref:`generic <generics>` theo kiểu trả về của các coroutine được chúng bao bọc.

   .. versionchanged:: 3.7
      Đã thêm hỗ trợ cho module :mod:`contextvars`.

   .. versionchanged:: 3.8
      Đã thêm tham số *name*.

   .. deprecated:: 3.10
      Cảnh báo ngừng sử dụng sẽ được phát ra nếu không chỉ định *loop* và không có event loop nào đang chạy.

   .. versionchanged:: 3.11
      Đã thêm tham số *context*.

   .. versionchanged:: 3.12
      Đã thêm tham số *eager_start*.

   .. method:: done()

      Trả về ``True`` nếu Task *hoàn tất*.

      Task được *hoàn tất* khi coroutine được bọc trả về một giá trị, phát sinh một exception hoặc Task bị hủy.

   .. method:: result()

      Trả về kết quả của Task.

      Nếu Task *hoàn tất*, kết quả của coroutine được bọc sẽ được trả về (hoặc nếu coroutine phát sinh một exception, exception đó sẽ được phát sinh lại).

      Nếu Task đã *bị hủy*, phương thức này sẽ phát sinh một :exc:`CancelledError` exception.

      Nếu kết quả của Task chưa khả dụng, phương thức này sẽ phát sinh một :exc:`InvalidStateError` exception.

   .. method:: exception()

      Trả về ngoại lệ của Task.

      Nếu coroutine được bao bọc phát sinh một ngoại lệ thì ngoại lệ đó sẽ được trả về. Nếu coroutine được bao bọc kết thúc bình thường thì phương thức này trả về ``None``.

      Nếu Task đã được *hủy*, phương thức này sẽ phát sinh một
      :exc:`CancelledError` ngoại lệ.

      Nếu Task vẫn chưa *hoàn tất*, phương thức này sẽ phát sinh một
      :exc:`InvalidStateError` ngoại lệ.

   .. method:: add_done_callback(callback, *, context=None)

      Thêm một callback sẽ được chạy khi Task *hoàn tất*.

      Phương thức này chỉ nên được sử dụng trong mã cấp thấp dựa trên callback.

      Xem tài liệu về :meth:`Future.add_done_callback` để biết thêm chi tiết.

   .. method:: remove_done_callback(callback)

      Xóa *callback* khỏi danh sách callback.

      Phương thức này chỉ nên được sử dụng trong mã cấp thấp dựa trên callback.

      Xem tài liệu về :meth:`Future.remove_done_callback` để biết thêm chi tiết.

   .. method:: get_stack(*, limit=None)

      Trả về danh sách các stack frame của Task này.

      Nếu coroutine được bọc chưa hoàn tất, hàm này trả về stack nơi coroutine đang tạm dừng. Nếu coroutine đã hoàn tất thành công hoặc đã bị hủy, hàm này trả về một danh sách rỗng. Nếu coroutine bị kết thúc do một exception, hàm này trả về danh sách các frame trong traceback.

      Các frame luôn được sắp xếp từ cũ nhất đến mới nhất.

      Chỉ một stack frame được trả về cho coroutine bị tạm dừng.

      Đối số *limit* tùy chọn đặt số frame tối đa cần trả về; theo mặc định, tất cả frame hiện có được trả về. Thứ tự của danh sách được trả về sẽ khác nhau tùy thuộc vào việc trả về stack hay traceback: các frame mới nhất của stack được trả về, còn các frame cũ nhất của traceback được trả về. (Điều này khớp với hành vi của module traceback.)

   .. method:: print_stack(*, limit=None, file=None)

      In stack hoặc traceback cho Task này.

      Lệnh này tạo ra kết quả tương tự module traceback đối với các frame được truy xuất bởi :meth:`get_stack`.

      Đối số *limit* được truyền trực tiếp cho :meth:`get_stack`.

      Đối số *file* là một luồng I/O mà kết quả được ghi vào đó; theo mặc định, kết quả được ghi vào :data:`sys.stdout`.

   .. method:: get_coro()

      Trả về đối tượng coroutine được :class:`Task` bọc.

      .. note::

         Điều này sẽ trả về ``None`` đối với các Task đã hoàn tất một cách eager. Xem :ref:`Eager Task Factory <eager-task-factory>`.

      .. versionadded:: 3.8

      .. versionchanged:: 3.12

         Việc thực thi eager task mới được bổ sung có nghĩa là result có thể là ``None``.

   .. method:: get_context()

      Trả về đối tượng :class:`contextvars.Context` liên kết với task.

      .. versionadded:: 3.12

   .. method:: get_name()

      Trả về tên của Task.

      Nếu chưa gán tên rõ ràng cho Task, implementation Task mặc định của asyncio sẽ tạo một tên mặc định trong quá trình khởi tạo.

      .. versionadded:: 3.8

   .. method:: set_name(value)

      Đặt tên cho Task.

      Đối số *value* có thể là bất kỳ đối tượng nào và sau đó sẽ được chuyển đổi thành chuỗi.

      Trong cách triển khai Task mặc định, tên sẽ hiển thị trong :func:`repr` output của một đối tượng Task.

      .. versionadded:: 3.8

   .. method:: cancel(msg=None)

      Yêu cầu Task bị hủy.

      Nếu Task đã *done* hoặc *cancelled*, trả về ``False``; nếu không, trả về ``True``.

      Phương thức này sắp xếp để một :exc:`CancelledError` exception được ném vào coroutine được bao bọc trong chu kỳ tiếp theo của event loop.

      Sau đó, coroutine có cơ hội dọn dẹp hoặc thậm chí từ chối yêu cầu bằng cách ngăn exception với một khối :keyword:`try` ... ... ``except CancelledError`` ... :keyword:`finally`. Do đó, không giống như :meth:`Future.cancel`, :meth:`Task.cancel` không đảm bảo rằng Task sẽ bị hủy, mặc dù việc hoàn toàn ngăn quá trình hủy là không phổ biến và chủ động không được khuyến khích. Tuy nhiên, nếu coroutine vẫn quyết định ngăn quá trình hủy, nó cần gọi :meth:`Task.uncancel` ngoài việc bắt exception.

      .. versionchanged:: 3.9
         Đã thêm tham số *msg*.

      .. versionchanged:: 3.11
         Tham số ``msg`` được truyền từ task đã bị hủy đến awaiter của task đó.

      .. _asyncio_example_task_cancel:

      Ví dụ sau minh họa cách các coroutine có thể chặn yêu cầu hủy::

          async def cancel_me():
              print('cancel_me(): before sleep')

              try:
                  # Chờ trong 1 giờ
                  await asyncio.sleep(3600)
              except asyncio.CancelledError:
                  print('cancel_me(): cancel sleep')
                  raise
              finally:
                  print('cancel_me(): after sleep')

          async def main():
              # Tạo một Task "cancel_me"
              task = asyncio.create_task(cancel_me())

              # Chờ trong 1 giây
              await asyncio.sleep(1)

              task.cancel()
              try:
                  await task
              except asyncio.CancelledError:
                  print("main(): cancel_me is cancelled now")

          asyncio.run(main())

          # Kết quả mong đợi:
          #
          #     cancel_me(): trước khi sleep
          #     cancel_me(): hủy sleep
          #     cancel_me(): sau sleep
          #     main(): cancel_me hiện đã bị hủy

   .. method:: cancelled()

      Trả về ``True`` nếu Task là *bị hủy*.

      Task ở trạng thái *bị hủy* khi yêu cầu hủy được thực hiện bằng
      :meth:`cancel` và coroutine được bao bọc đã truyền tiếp
      :exc:`CancelledError` ngoại lệ được ném vào nó.

   .. method:: uncancel()

      Giảm số lượng yêu cầu hủy đối với Task này.

      Trả về số lượng yêu cầu hủy còn lại.

      Lưu ý rằng sau khi quá trình thực thi một task đã bị hủy hoàn tất, các lần gọi tiếp theo đến :meth:`uncancel` sẽ không có tác dụng.

      .. versionadded:: 3.11

      Phương thức này được sử dụng trong nội bộ asyncio và không dành cho mã của người dùng cuối. Cụ thể, nếu một Task được bỏ hủy thành công, phương thức này cho phép các phần tử của structured concurrency như
      :ref:`taskgroups` và :func:`asyncio.timeout` tiếp tục chạy, giới hạn việc hủy trong block có cấu trúc tương ứng. Ví dụ::

        async def make_request_with_timeout():
            try:
                async with asyncio.timeout(1):
                    # Block có cấu trúc bị ảnh hưởng bởi thời gian chờ:
                    await make_request()
                    await make_another_request()
            except TimeoutError:
                log("There was a timeout")
            # Mã bên ngoài không bị ảnh hưởng bởi thời gian chờ:
            await unrelated_code()

      Mặc dù khối chứa ``make_request()`` và ``make_another_request()`` có thể bị hủy do hết thời gian chờ, ``unrelated_code()`` vẫn sẽ tiếp tục chạy ngay cả khi hết thời gian chờ. Điều này được triển khai bằng :meth:`uncancel`. Các trình quản lý ngữ cảnh :class:`TaskGroup` sử dụng
      :func:`uncancel` theo cách tương tự.

      Nếu mã của người dùng cuối vì lý do nào đó ngăn việc hủy bằng cách bắt :exc:`CancelledError`, mã đó cần gọi phương thức này để xóa trạng thái hủy.

      Khi phương thức này giảm số lượng yêu cầu hủy xuống 0, phương thức sẽ kiểm tra xem một lệnh gọi :meth:`cancel` trước đó có thiết lập để :exc:`CancelledError` được ném vào task hay chưa. Nếu nó vẫn chưa được ném, thiết lập đó sẽ bị hủy bỏ (bằng cách đặt lại cờ ``_must_cancel`` nội bộ).

   .. versionchanged:: 3.13
      Đã thay đổi để hủy bỏ các yêu cầu hủy đang chờ khi số lượng giảm xuống 0.

   .. method:: cancelling()

      Trả về số lượng yêu cầu hủy đang chờ đối với Task này, tức là số lần gọi :meth:`cancel` trừ đi số lần gọi
      :meth:`uncancel`.

      Lưu ý rằng nếu số này lớn hơn 0 nhưng Task vẫn đang thực thi, :meth:`cancelled` vẫn sẽ trả về ``False``. Điều này là do số này có thể được giảm bằng cách gọi :meth:`uncancel`, dẫn đến việc tác vụ cuối cùng có thể không bị hủy nếu số lượng yêu cầu hủy giảm xuống 0.

      Phương thức này được sử dụng trong nội bộ asyncio và không dự kiến được gọi từ code của người dùng cuối. Xem :meth:`uncancel` để biết thêm chi tiết.

      .. versionadded:: 3.11
