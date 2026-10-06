.. currentmodule:: asyncio

.. _asyncio-dev:

======================
Phát triển với asyncio
======================

Lập trình bất đồng bộ khác với lập trình "tuần tự" truyền thống.

Trang này liệt kê các lỗi và bẫy thường gặp, đồng thời giải thích cách tránh chúng.


.. _asyncio-debug-mode:

Chế độ debug
============

Theo mặc định, asyncio chạy ở chế độ production. Để thuận tiện cho việc phát triển, asyncio có *chế độ debug*.

Có một số cách để bật chế độ debug của asyncio:

* Đặt biến môi trường :envvar:`PYTHONASYNCIODEBUG` thành ``1``.

* Sử dụng :ref:`Python Development Mode <devmode>`.

* Truyền ``debug=True`` vào :func:`asyncio.run`.

* Gọi :meth:`loop.set_debug`.

Ngoài việc bật chế độ gỡ lỗi, bạn cũng nên cân nhắc:

* đặt mức log của :ref:`logger asyncio <asyncio-logger>` thành
  :py:const:`logging.DEBUG`, chẳng hạn, đoạn mã sau có thể được chạy khi ứng dụng khởi động::

    logging.basicConfig(level=logging.DEBUG)

* cấu hình module :mod:`warnings` để hiển thị
  :exc:`ResourceWarning` cảnh báo. Một cách để thực hiện việc đó là sử dụng tùy chọn dòng lệnh :option:`-W` ``default``.


Khi chế độ debug được bật:

* Nhiều API asyncio không an toàn với thread (chẳng hạn như :meth:`loop.call_soon` và
  các phương thức :meth:`loop.call_at`) sẽ phát sinh ngoại lệ nếu được gọi từ sai thread.

* Thời gian thực thi của bộ chọn I/O được ghi lại nếu mất quá nhiều thời gian để thực hiện một thao tác I/O.

* Các callback mất hơn 100 mili giây để thực thi sẽ được ghi lại. Thuộc tính
  :attr:`loop.slow_callback_duration` có thể được sử dụng để đặt thời lượng thực thi tối thiểu tính bằng giây được xem là "chậm".


.. _asyncio-multithreading:

Đồng thời và Đa luồng
=====================

Một event loop chạy trong một thread (thường là main thread) và thực thi tất cả callback và Task trong thread đó. Khi một Task đang chạy trong event loop, không Task nào khác có thể chạy trong cùng thread. Khi một Task thực thi biểu thức ``await``, Task đang chạy sẽ bị tạm dừng và event loop thực thi Task tiếp theo.

Để lập lịch một :term:`callback` từ một OS thread khác, cần sử dụng
phương thức :meth:`loop.call_soon_threadsafe`. Ví dụ::

    loop.call_soon_threadsafe(callback, *args)

Hầu hết các đối tượng asyncio không an toàn khi sử dụng trong thread, nhưng điều này thường không gây vấn đề trừ khi có code làm việc với chúng bên ngoài một Task hoặc callback. Nếu cần để code như vậy gọi một API asyncio cấp thấp, nên sử dụng phương thức :meth:`loop.call_soon_threadsafe`, chẳng hạn như::

    loop.call_soon_threadsafe(fut.cancel)

Để lập lịch một đối tượng coroutine từ một OS thread khác, cần sử dụng
hàm :func:`run_coroutine_threadsafe`. Hàm này trả về một
:class:`concurrent.futures.Future` để truy cập kết quả::

     async def coro_func():
          return await asyncio.sleep(1, 42)

     # Sau đó trong một OS thread khác:

     future = asyncio.run_coroutine_threadsafe(coro_func(), loop)
     # Chờ kết quả:
     result = future.result()

Để xử lý các signal, event loop phải được chạy trong main thread.

Có thể sử dụng phương thức :meth:`loop.run_in_executor` với một
:class:`concurrent.futures.ThreadPoolExecutor` hoặc
:class:`~concurrent.futures.InterpreterPoolExecutor` để thực thi mã blocking trong một OS thread khác mà không chặn OS thread nơi event loop đang chạy.

Hiện tại không có cách nào để lập lịch coroutine hoặc callback trực tiếp từ một tiến trình khác (chẳng hạn như tiến trình được khởi chạy bằng
:mod:`multiprocessing`). Phần :ref:`asyncio-event-loop-methods` liệt kê các API có thể đọc từ pipe và theo dõi các file descriptor mà không chặn event loop. Ngoài ra, các API
:ref:`Subprocess <asyncio-subprocess>` của asyncio cung cấp cách khởi chạy một tiến trình và giao tiếp với tiến trình đó từ event loop. Cuối cùng, phương thức :meth:`loop.run_in_executor` nói trên cũng có thể được sử dụng với :class:`concurrent.futures.ProcessPoolExecutor` để thực thi mã trong một tiến trình khác.

.. _asyncio-handle-blocking:

Chạy mã blocking
================

Không nên gọi trực tiếp mã blocking (CPU-bound). Ví dụ: nếu một hàm thực hiện phép tính tốn nhiều CPU trong 1 giây, tất cả các asyncio Task đồng thời và thao tác IO sẽ bị trì hoãn 1 giây.

Có thể sử dụng executor để chạy một task trong thread khác, kể cả trong một interpreter khác, hoặc thậm chí trong một tiến trình khác nhằm tránh chặn thread của hệ điều hành chứa event loop. Xem phương thức :meth:`loop.run_in_executor` để biết thêm chi tiết.


.. _asyncio-logger:

Logging
=======

asyncio sử dụng module :mod:`logging` và mọi hoạt động logging đều được thực hiện thông qua logger ``"asyncio"``.

Mức log mặc định là :py:const:`logging.INFO`, bạn có thể dễ dàng điều chỉnh mức này::

   logging.getLogger("asyncio").setLevel(logging.WARNING)


Network logging có thể chặn event loop. Bạn nên sử dụng một thread riêng để xử lý log hoặc sử dụng IO không blocking. Ví dụ, xem :ref:`blocking-handlers`.


.. _asyncio-coroutine-not-scheduled:

Phát hiện các coroutine chưa bao giờ được await
===============================================

Khi một hàm coroutine được gọi nhưng không được await (ví dụ: ``coro()`` thay vì ``await coro()``) hoặc coroutine không được lập lịch bằng :meth:`asyncio.create_task`, asyncio sẽ phát ra một :exc:`RuntimeWarning`::

    import asyncio

    async def test():
        print("never scheduled")

    async def main():
        test()

    asyncio.run(main())

Đầu ra::

  test.py:7: RuntimeWarning: coroutine 'test' was never awaited
    test()

Đầu ra ở chế độ debug::

  test.py:7: RuntimeWarning: coroutine 'test' was never awaited
  Coroutine created at (most recent call last)
    File "../t.py", line 9, in <module>
      asyncio.run(main(), debug=True)

    < .. >

    File "../t.py", line 7, in main
      test()
    test()

Cách khắc phục thông thường là await coroutine hoặc gọi
:meth:`asyncio.create_task` hàm::

    async def main():
        await test()


Phát hiện các exception không bao giờ được truy xuất
====================================================

Nếu :meth:`Future.set_exception` được gọi nhưng đối tượng Future không bao giờ được await, exception sẽ không bao giờ được truyền đến code của người dùng. Trong trường hợp này, asyncio sẽ ghi một thông báo nhật ký khi đối tượng Future được garbage collection.

Ví dụ về một exception chưa được xử lý::

    import asyncio

    async def bug():
        raise Exception("not consumed")

    async def main():
        asyncio.create_task(bug())

    asyncio.run(main())

Đầu ra::

    Task exception was never retrieved
    future: <Task finished coro=<bug() done, defined at test.py:3>
      exception=Exception('not consumed')>

    Traceback (most recent call last):
      File "test.py", line 4, in bug
        raise Exception("not consumed")
    Exception: not consumed

:ref:`Bật chế độ debug <asyncio-debug-mode>` để nhận traceback tại nơi task được tạo::

    asyncio.run(main(), debug=True)

Xuất ở chế độ debug::

    Task exception was never retrieved
    future: <Task finished coro=<bug() done, defined at test.py:3>
        exception=Exception('not consumed') created at asyncio/tasks.py:321>

    source_traceback: Object created at (most recent call last):
      File "../t.py", line 9, in <module>
        asyncio.run(main(), debug=True)

    < .. >

    Traceback (most recent call last):
      File "../t.py", line 4, in bug
        raise Exception("not consumed")
    Exception: not consumed


Các phương pháp hay nhất cho asynchronous generator
===================================================

Việc viết mã asyncio chính xác và hiệu quả đòi hỏi bạn phải nhận biết một số cạm bẫy nhất định. Phần này trình bày các phương pháp hay nhất thiết yếu có thể giúp bạn tiết kiệm hàng giờ gỡ lỗi.


Đóng asynchronous generator một cách rõ ràng
--------------------------------------------

Bạn nên đóng thủ công
:term:`asynchronous generator <asynchronous generator iterator>`. Nếu generator kết thúc sớm - chẳng hạn do một ngoại lệ được raised trong phần thân của một ``async for`` vòng lặp - mã dọn dẹp bất đồng bộ của nó có thể chạy trong một context không mong muốn. Điều này có thể xảy ra sau khi các task mà nó phụ thuộc vào đã hoàn tất hoặc trong quá trình event loop tắt, khi hook thu gom rác của async-generator được gọi.

Để tránh điều này, hãy đóng generator một cách rõ ràng bằng cách gọi
phương thức :meth:`~agen.aclose`, hoặc sử dụng context manager :func:`contextlib.aclosing`::

  import asyncio
  import contextlib

  async def gen():
    yield 1
    yield 2

  async def func():
    async with contextlib.aclosing(gen()) as g:
      async for x in g:
        break  # Đừng lặp cho đến hết

  asyncio.run(func())

Như đã lưu ý ở trên, mã dọn dẹp cho các asynchronous generator này được trì hoãn. Ví dụ sau đây cho thấy việc hoàn tất một asynchronous generator có thể xảy ra theo thứ tự không mong đợi::

  import asyncio
  work_done = False

  async def cursor():
      try:
          yield 1
      finally:
          assert work_done

  async def rows():
      global work_done
      try:
          yield 2
      finally:
          await asyncio.sleep(0.1) # Mô phỏng một số công việc async
          work_done = True


  async def main():
      async for c in cursor():
          async for r in rows():
              break
          break

  asyncio.run(main())

Với ví dụ này, chúng ta nhận được kết quả sau::

  unhandled exception during asyncio.run() shutdown
  task: <Task finished name='Task-3' coro=<<async_generator_athrow without __name__>()> exception=AssertionError()>
  Traceback (most recent call last):
    File "example.py", line 6, in cursor
      yield 1
  asyncio.exceptions.CancelledError

  During handling of the above exception, another exception occurred:

  Traceback (most recent call last):
    File "example.py", line 8, in cursor
      assert work_done
             ^^^^^^^^^
  AssertionError

Asynchronous generator ``cursor()`` được hoàn tất trước generator ``rows`` - một hành vi không mong đợi.

Có thể sửa ví dụ bằng cách đóng rõ ràng các async-generator ``cursor`` và ``rows``::

  async def main():
      async with contextlib.aclosing(cursor()) as cursor_gen:
          async for c in cursor_gen:
              async with contextlib.aclosing(rows()) as rows_gen:
                  async for r in rows_gen:
                      break
              break


Chỉ tạo trình tạo bất đồng bộ khi event loop đang chạy
------------------------------------------------------

Bạn nên tạo
:term:`trình tạo bất đồng bộ <asynchronous generator iterator>` chỉ sau khi event loop đã được tạo.

Để đảm bảo các trình tạo bất đồng bộ được đóng một cách đáng tin cậy, event loop sử dụng
hàm :func:`sys.set_asyncgen_hooks` để đăng ký các hàm callback. Các callback này cập nhật danh sách các trình tạo bất đồng bộ đang chạy để giữ danh sách ở trạng thái nhất quán.

Khi hàm :meth:`loop.shutdown_asyncgens() <asyncio.loop.shutdown_asyncgens>` được gọi, các trình tạo đang chạy sẽ được dừng một cách có trật tự và danh sách sẽ được xóa.

Trình tạo bất đồng bộ gọi system hook tương ứng trong lần lặp đầu tiên. Đồng thời, trình tạo ghi nhận rằng hook đã được gọi và không gọi lại hook đó.

Do đó, nếu việc lặp bắt đầu trước khi event loop được tạo, event loop sẽ không thể thêm generator vào danh sách các generator đang hoạt động vì các hook được thiết lập sau khi generator cố gắng gọi chúng. Vì vậy, event loop sẽ không thể kết thúc generator khi cần thiết.

Hãy xem xét ví dụ sau::

  import asyncio

  async def agenfn():
      try:
          yield 10
      finally:
          await asyncio.sleep(0)


  with asyncio.Runner() as runner:
      agen = agenfn()
      print(runner.run(anext(agen)))
      del agen

Đầu ra::

  10
  Exception ignored while closing generator <async_generator object agenfn at 0x000002F71CD10D70>:
  Traceback (most recent call last):
    File "example.py", line 13, in <module>
      del agen
          ^^^^
  RuntimeError: async generator ignored GeneratorExit

Có thể sửa ví dụ này như sau::

  import asyncio

  async def agenfn():
      try:
          yield 10
      finally:
          await asyncio.sleep(0)

  async def main():
      agen = agenfn()
      print(await anext(agen))
      del agen

  asyncio.run(main())


Tránh lặp và đóng đồng thời cùng một generator
----------------------------------------------

Các async generator có thể được reenter trong khi một
:meth:`~agen.__anext__` / :meth:`~agen.athrow` / :meth:`~agen.aclose` đang được gọi. Điều này có thể dẫn đến trạng thái không nhất quán của async generator và gây ra lỗi.

Hãy xem xét ví dụ sau::

  import asyncio

  async def consumer():
      for idx in range(100):
          await asyncio.sleep(0)
          message = yield idx
          print('received', message)

  async def amain():
      agenerator = consumer()
      await agenerator.asend(None)

      fa = asyncio.create_task(agenerator.asend('A'))
      fb = asyncio.create_task(agenerator.asend('B'))
      await fa
      await fb

  asyncio.run(amain())

Kết quả::

  received A
  Traceback (most recent call last):
    File "test.py", line 38, in <module>
      asyncio.run(amain())
      ~~~~~~~~~~~^^^^^^^^^
    File "Lib/asyncio/runners.py", line 204, in run
      return runner.run(main)
             ~~~~~~~~~~^^^^^^
    File "Lib/asyncio/runners.py", line 127, in run
      return self._loop.run_until_complete(task)
             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
    File "Lib/asyncio/base_events.py", line 719, in run_until_complete
      return future.result()
             ~~~~~~~~~~~~~^^
    File "test.py", line 36, in amain
      await fb
  RuntimeError: anext(): asynchronous generator is already running


Do đó, bạn nên tránh sử dụng asynchronous generator trong các tác vụ chạy song song hoặc trên nhiều event loop.
