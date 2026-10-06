.. currentmodule:: asyncio

.. _asyncio-threading:

asyncio và Python free-threaded
===============================

asyncio sử dụng event loop làm bộ lập lịch để cho phép concurrency đạt hiệu quả cao bằng cách chuyển đổi giữa các task, nhờ đó cho phép thực hiện các thao tác I/O không chặn. Điều này mang lại hiệu năng tốt hơn cho các trường hợp sử dụng bị giới hạn bởi I/O. asyncio cũng cho phép chuyển công việc bị giới hạn bởi CPU sang thread pool hoặc process pool, nhưng việc này vẫn bị giới hạn bởi :term:`global interpreter lock` trong CPython.

Tuy nhiên, trong :ref:`Python free-threaded <freethreading-python-howto>`, GIL bị vô hiệu hóa và Python có thể chạy mã đa luồng thực sự. Điều này có nghĩa là asyncio giờ đây có thể tận dụng nhiều lõi CPU mà không bị những hạn chế do GIL áp đặt.

Kể từ Python 3.14, asyncio hỗ trợ đầy đủ Python free-threaded, và việc triển khai asyncio an toàn khi sử dụng trong môi trường đa luồng.

Một event loop duy nhất trên một lõi có thể xử lý đồng thời nhiều kết nối, nhưng mã Python chạy để xử lý từng kết nối vẫn được thực thi tuần tự. Khi các request cần một lượng tính toán đáng kể cho mỗi request, việc xử lý đó sẽ trở thành điểm nghẽn và một lõi đơn không còn đáp ứng kịp. Kết hợp asyncio với các thread hữu ích nhất trong trường hợp này: bằng cách chạy một event loop trên mỗi thread, việc xử lý các request khác nhau có thể chạy song song trên nhiều lõi CPU. Cách này cũng hữu ích khi bạn cần chạy mã blocking hoặc mã bị giới hạn bởi CPU từ một ứng dụng asyncio.


.. seealso::

   `Mở rộng asyncio trên Python Free-Threaded <https://labs.quansight.org/blog/scaling-asyncio-on-free-threaded-python>`__, một bài viết trên blog của Kumar Aditya giải thích những thay đổi nội bộ giúp asyncio an toàn và hiệu quả trên Python free-threaded, cùng với các benchmark về những cải thiện đạt được.


Các vấn đề cần cân nhắc về tính an toàn khi sử dụng thread
----------------------------------------------------------

Mặc dù asyncio được thiết kế để an toàn với thread trong môi trường Python không bị giới hạn bởi GIL, vẫn có một số điểm cần lưu ý khi sử dụng asyncio với các thread:

1. **Vòng lặp sự kiện**: Mỗi thread nên có một event loop riêng và không nên chia sẻ event loop đó giữa các thread. Điều này đảm bảo event loop có thể quản lý các task và callback của riêng mình mà không bị các thread khác can thiệp.

2. **Quản lý task**: Không nên await hoặc thao tác với các task và future được tạo trong một thread từ một thread khác.

3. **API an toàn với thread**: Khi tương tác với asyncio từ nhiều thread, điều quan trọng là sử dụng các API an toàn với thread do asyncio cung cấp, chẳng hạn như :func:`asyncio.run_coroutine_threadsafe` để gửi coroutine đến một event loop từ thread khác. Nếu cần gọi một callback từ thread khác, bạn có thể sử dụng
   :meth:`loop.call_soon_threadsafe` để lên lịch cho callback đó một cách an toàn.

4. **Đồng bộ hóa**: Các primitive đồng bộ hóa do asyncio cung cấp (chẳng hạn như :class:`asyncio.Lock` và :class:`asyncio.Event`) không được thiết kế để sử dụng giữa các thread. Nếu cần đồng bộ hóa giữa các thread, bạn nên sử dụng các primitive đồng bộ hóa từ module :mod:`threading` thay thế.


Sử dụng asyncio với các thread
------------------------------

asyncio hỗ trợ chạy một event loop cho mỗi thread, cho phép bạn tận dụng nhiều CPU core trong môi trường Python free-threaded. Mỗi thread có thể chạy event loop riêng, và các task có thể được lập lịch độc lập trên những event loop đó.

Dưới đây là một ví dụ về cách sử dụng asyncio với các thread::

    import asyncio
    import threading

    async def worker(name: str) -> None:
        print(f"Worker {name} starting")
        await asyncio.sleep(1)
        print(f"Worker {name} done")

    def run_loop(name: str) -> None:
        asyncio.run(worker(name))

    threads = [
        threading.Thread(target=run_loop, args=(f"T{i}",))
        for i in range(4)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

Trong ví dụ này, mỗi thread tạo event loop riêng bằng
:func:`asyncio.run` và chạy một coroutine trên đó. Các thread thực thi đồng thời, và trong một bản build free-threaded, chúng có thể chạy song song trên các CPU core riêng biệt.


Producer/consumer giữa các thread
---------------------------------

Khi một thread thông thường (không phải asyncio) cần chuyển công việc cho một event loop của asyncio đang chạy trong thread khác, hãy sử dụng một primitive an toàn với thread, chẳng hạn như :class:`queue.Queue`, thay vì :class:`asyncio.Queue`, vốn chỉ an toàn trong một event loop duy nhất.::

    import asyncio
    import queue
    import threading

    def producer(q: queue.Queue[int]) -> None:
        for i in range(5):
            print(f"Producing {i}")
            q.put(i)
        q.shutdown()

    async def consumer(q: queue.Queue[int]) -> None:
        while True:
            try:
                item = q.get_nowait()
            except queue.Empty:
                await asyncio.sleep(0.1)
                continue
            except queue.ShutDown:
                break
            print(f"Consumed {item}")
            await asyncio.sleep(item)

    q: queue.Queue[int] = queue.Queue()
    consumer_thread = threading.Thread(
        target=lambda: asyncio.run(consumer(q))
    )
    consumer_thread.start()
    producer(q)
    consumer_thread.join()

Producer chạy trên main thread, còn consumer chạy bên trong một event loop trên thread riêng, nhưng chúng vẫn giao tiếp an toàn thông qua ``queue.Queue``. Khi hàng đợi trống, consumer sẽ tạm dừng trong thời gian ngắn rồi thử lại. Khi producer hoàn tất, nó gọi
:meth:`~queue.Queue.shutdown`, khiến các lệnh gọi tiếp theo
:meth:`~queue.Queue.get_nowait` gọi :exc:`queue.ShutDown` để consumer có thể thoát một cách an toàn.

