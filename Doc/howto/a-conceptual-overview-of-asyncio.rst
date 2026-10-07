.. _a-conceptual-overview-of-asyncio:

**************************************
Tổng quan khái niệm về :mod:`!asyncio`
**************************************

Bài viết :ref:`HOWTO <how-tos>` này nhằm giúp bạn xây dựng một mô hình tư duy vững chắc về cách :mod:`asyncio` thực sự hoạt động, qua đó hiểu được cơ sở và lý do đằng sau các mẫu được khuyến nghị.

Bạn có thể tò mò về một số khái niệm :mod:`!asyncio` then chốt. Đến cuối bài viết này, bạn sẽ có thể tự tin trả lời các câu hỏi sau:

- Điều gì xảy ra ở phía sau khi một đối tượng được await?
- :mod:`!asyncio` phân biệt như thế nào giữa một tác vụ không cần thời gian CPU (chẳng hạn như yêu cầu mạng hoặc đọc tệp) và một tác vụ cần thời gian CPU (chẳng hạn như tính giai thừa của n)?
- Cách viết một biến thể bất đồng bộ của một thao tác, chẳng hạn như thao tác sleep bất đồng bộ hoặc yêu cầu cơ sở dữ liệu.

.. seealso::

   * `guide <https://github.com/anordin95/a-conceptual-overview-of-asyncio/ tree/main>`_ đã truyền cảm hứng cho bài viết HOWTO này, do Alexander Nordin viết.
   * Loạt `hướng dẫn chuyên sâu trên YouTube <https://www.youtube.com/ watch?v=Xbl7XjFYsN4&list=PLhNSoGM2ik6SIkVGXWBwerucXjgP1rHmB>`_ này về ``asyncio`` do thành viên nhóm phát triển cốt lõi của Python, Łukasz Langa, thực hiện.
   * `500 dòng mã trở xuống: Trình thu thập dữ liệu web với các coroutine asyncio <https:// aosabook.org/en/500L/a-web-crawler-with-asyncio-coroutines.html>`_ của A. Jesse Jiryu Davis và Guido van Rossum.

------------------------------------
Tổng quan khái niệm, phần 1: cấp cao
------------------------------------

Trong phần 1, chúng ta sẽ tìm hiểu các khối xây dựng cấp cao chính của :mod:`!asyncio`: event loop, các hàm coroutine, các đối tượng coroutine, task và ``await``.

==========
Event Loop
==========

Mọi thứ trong :mod:`!asyncio` đều diễn ra trong mối quan hệ với event loop. Nó là nhân vật chính của toàn bộ hệ thống. Nó giống như một nhạc trưởng. Nó âm thầm quản lý các tài nguyên ở phía sau. Một phần quyền hạn được cấp rõ ràng cho nó, nhưng phần lớn khả năng hoàn thành công việc của nó đến từ sự tôn trọng và phối hợp của những worker tận tụy.

Theo cách nói kỹ thuật hơn, event loop chứa một tập hợp các công việc cần được chạy. Một số công việc do bạn trực tiếp thêm vào, còn một số được :mod:`!asyncio` thêm vào gián tiếp. Event loop lấy một công việc từ danh sách công việc đang chờ và gọi nó (hoặc "trao quyền điều khiển cho nó"), tương tự như khi gọi một hàm, rồi công việc đó bắt đầu chạy. Khi tạm dừng hoặc hoàn tất, công việc sẽ trả quyền điều khiển về cho event loop. Sau đó, event loop sẽ chọn một công việc khác từ nhóm của mình và gọi nó. Bạn có thể *hình dung một cách tương đối* tập hợp các công việc như một hàng đợi: các công việc được thêm vào rồi xử lý lần lượt từng công việc, nhìn chung (nhưng không phải lúc nào cũng vậy) theo thứ tự. Quá trình này lặp lại vô thời hạn, khi event loop liên tục chuyển sang các công việc tiếp theo. Nếu không còn công việc nào đang chờ thực thi, event loop đủ thông minh để nghỉ và tránh lãng phí chu kỳ CPU không cần thiết, rồi quay lại khi có thêm việc cần làm.

Việc thực thi hiệu quả phụ thuộc vào việc các job phối hợp và chia sẻ quyền điều khiển tốt; một job tham lam có thể chiếm quyền điều khiển và khiến các job khác bị đói tài nguyên, làm cho cách tiếp cận event loop tổng thể trở nên khá vô ích.

::

   import asyncio

   # Tạo một event loop và lặp vô hạn qua
   # tập hợp các job của nó.
   event_loop = asyncio.new_event_loop()
   event_loop.run_forever()

================================
Các hàm bất đồng bộ và coroutine
================================

Đây là một hàm Python cơ bản, đơn điệu::

   def hello_printer():
       print(
           "Hi, I am a lowly, simple printer, though I have all I "
           "need in life -- \nfresh paper and my dearly beloved octopus "
           "partner in crime."
       )

Việc gọi một hàm thông thường sẽ thực thi logic hoặc phần thân của hàm đó::

   >>> hello_printer()
   Hi, I am a lowly, simple printer, though I have all I need in life --
   fresh paper and my dearly beloved octopus partner in crime.

:ref:`async def <async def>`, thay vì chỉ là một ``def``, khiến đây trở thành một hàm bất đồng bộ (hay "hàm coroutine"). Việc gọi hàm này sẽ tạo và trả về một đối tượng :ref:`coroutine <coroutine>`.

::

   async def loudmouth_penguin(magic_number: int):
       print(
        "I am a super special talking penguin. Far cooler than that printer. "
        f"By the way, my lucky number is: {magic_number}."
       )

Việc gọi hàm async, ``loudmouth_penguin``, không thực thi câu lệnh print; thay vào đó, nó tạo ra một đối tượng coroutine::

   >>> loudmouth_penguin(magic_number=3)
   <coroutine object loudmouth_penguin at 0x104ed2740>

Các thuật ngữ "coroutine function" và "coroutine object" thường bị gộp chung thành coroutine. Điều đó có thể gây nhầm lẫn! Trong bài viết này, coroutine cụ thể chỉ một đối tượng coroutine, hay chính xác hơn là một instance của :class:`types.CoroutineType` (native coroutine). Lưu ý rằng coroutine cũng có thể tồn tại dưới dạng instance của
:class:`collections.abc.Coroutine` -- một điểm khác biệt quan trọng khi kiểm tra kiểu.

Một coroutine đại diện cho phần thân hoặc logic của hàm. Coroutine phải được khởi động một cách rõ ràng; một lần nữa, chỉ tạo coroutine không có nghĩa là khởi động nó. Đáng chú ý, coroutine có thể tạm dừng và tiếp tục tại nhiều điểm khác nhau trong phần thân hàm. Khả năng tạm dừng và tiếp tục đó cho phép thực hiện hành vi bất đồng bộ!

Coroutine và coroutine function được xây dựng bằng cách tận dụng chức năng của :term:`generators <generator iterator>` và
:term:`generator functions <generator>`. Hãy nhớ rằng, một hàm generator là một hàm :keyword:`yield`\s, như hàm này::

   def get_random_number():
       # Đây sẽ là một bộ tạo số ngẫu nhiên tồi!
       print("Hi")
       yield 1
       print("Hello")
       yield 7
       print("Howdy")
       yield 4
       ...

Tương tự như một hàm coroutine, việc gọi một hàm generator không thực thi hàm đó. Thay vào đó, nó tạo ra một đối tượng generator::

   >>> get_random_number()
   <generator object get_random_number at 0x1048671c0>

Bạn có thể chuyển sang ``yield`` tiếp theo của một generator bằng cách sử dụng hàm dựng sẵn :func:`next`. Nói cách khác, generator chạy rồi tạm dừng. Ví dụ::

   >>> generator = get_random_number()
   >>> next(generator)
   Hi
   1
   >>> next(generator)
   Hello
   7

====
Task
====

Nói một cách khái quát, :ref:`task <asyncio-task-obj>` là các coroutine (không phải hàm coroutine) được liên kết với một event loop. Một task cũng duy trì danh sách các hàm callback; tầm quan trọng của danh sách này sẽ trở nên rõ ràng sau khi chúng ta thảo luận về :keyword:`await`. Cách được khuyến nghị để tạo task là thông qua :func:`asyncio.create_task`.

Việc tạo một task sẽ tự động lên lịch thực thi task đó (bằng cách thêm một callback để chạy task vào danh sách việc cần làm của event loop, tức là tập hợp các job).

:mod:`!asyncio` tự động liên kết các task với event loop cho bạn. Cơ chế liên kết tự động này được cố ý thiết kế vào :mod:`!asyncio` để đơn giản hóa việc sử dụng. Nếu không có nó, bạn sẽ phải tự theo dõi đối tượng event loop và truyền đối tượng đó cho mọi hàm coroutine muốn tạo task, khiến mã của bạn trở nên rườm rà không cần thiết.

::

   coroutine = loudmouth_penguin(magic_number=5)
   # Tạo một đối tượng Task và lên lịch thực thi đối tượng này thông qua event loop.
   task = asyncio.create_task(coroutine)

Trước đó, chúng ta đã tự tạo event loop và thiết lập để nó chạy vô hạn. Trong thực tế, bạn nên sử dụng (và thường sẽ thấy) :func:`asyncio.run`, vì nó đảm nhiệm việc quản lý event loop và đảm bảo coroutine được cung cấp hoàn tất trước khi tiếp tục. Ví dụ, nhiều chương trình async sử dụng cấu trúc sau::

   import asyncio

   async def main():
       # Thực hiện đủ mọi thứ bất đồng bộ kỳ quặc, hoang dã...
       ...

   if __name__ == "__main__":
       asyncio.run(main())
       # Chương trình sẽ không thực thi câu lệnh print sau đây cho đến khi
       # coroutine main() hoàn tất.
       print("coroutine main() is done!")

Điều quan trọng cần lưu ý là bản thân task không được thêm vào event loop; chỉ có một callback gọi task mới được thêm vào. Điều này quan trọng nếu đối tượng task mà bạn tạo bị garbage collection trước khi event loop gọi nó. Hãy xem xét chương trình sau:

.. code-block::
   :linenos:

   async def hello():
       print("hello!")

   async def main():
       asyncio.create_task(hello())
       # Các chỉ thị bất đồng bộ khác chạy trong một khoảng thời gian
       # và nhường quyền điều khiển cho event loop...
       ...

   asyncio.run(main())

Vì không có tham chiếu nào đến đối tượng task được tạo ở dòng 5, nó *có thể* bị garbage collector thu gom trước khi event loop gọi nó. Các chỉ dẫn tiếp theo trong coroutine ``main()`` trả quyền điều khiển lại cho event loop để nó có thể gọi các job khác. Cuối cùng, khi event loop cố chạy task, nó có thể gặp lỗi và phát hiện đối tượng task không tồn tại! Điều này cũng có thể xảy ra ngay cả khi một coroutine giữ tham chiếu đến một task nhưng hoàn tất trước khi task đó kết thúc. Khi coroutine thoát, các biến cục bộ không còn nằm trong phạm vi và có thể bị garbage collector thu gom. Trên thực tế, ``asyncio`` và garbage collector của Python hoạt động khá tích cực để đảm bảo điều này không xảy ra. Nhưng đó không phải là lý do để hành động bất cẩn!||||

=====
await
=====

:keyword:`await` là một từ khóa Python thường được sử dụng theo một trong hai cách khác nhau::

   await task
   await coroutine

Ở một khía cạnh quan trọng, hành vi của ``await`` phụ thuộc vào kiểu của đối tượng được await.

Await một task sẽ nhường quyền điều khiển từ task hoặc coroutine hiện tại cho event loop. Trong quá trình nhường quyền điều khiển, một vài việc quan trọng sẽ xảy ra. Chúng ta sẽ sử dụng ví dụ mã sau để minh họa::

   async def plant_a_tree():
       dig_the_hole_task = asyncio.create_task(dig_the_hole())
       await dig_the_hole_task

       # Các chỉ dẫn khác liên quan đến việc trồng cây.
       ...

Trong ví dụ này, hãy tưởng tượng event loop đã chuyển quyền điều khiển cho phần bắt đầu của coroutine ``plant_a_tree()``. Như đã thấy ở trên, coroutine tạo một task rồi await task đó. Chỉ dẫn ``await dig_the_hole_task`` thêm một callback (callback này sẽ tiếp tục ``plant_a_tree()``) vào danh sách callback của đối tượng ``dig_the_hole_task``. Sau đó, chỉ dẫn này nhường quyền điều khiển cho event loop. Một thời gian sau, event loop sẽ chuyển quyền điều khiển cho ``dig_the_hole_task`` và task sẽ hoàn tất mọi việc cần làm. Khi task hoàn tất, nó sẽ thêm các callback khác nhau của mình vào event loop; trong trường hợp này là một lệnh gọi để tiếp tục ``plant_a_tree()``.

Nói chung, khi task được await hoàn tất (``dig_the_hole_task``), task hoặc coroutine ban đầu (``plant_a_tree()``) sẽ được thêm lại vào danh sách việc cần làm của event loop để tiếp tục chạy.

Đây là một mô hình tư duy cơ bản nhưng đáng tin cậy. Trên thực tế, việc chuyển quyền điều khiển phức tạp hơn một chút, nhưng không đáng kể. Trong phần 2, chúng ta sẽ đi qua các chi tiết giúp điều này khả thi.

**Không giống task, việc await một coroutine không chuyển quyền điều khiển lại cho event loop!** Trước tiên, nếu bọc một coroutine trong task rồi await task đó, quyền điều khiển sẽ được nhường lại. Hành vi của ``await coroutine`` về cơ bản giống với việc gọi một hàm Python thông thường, đồng bộ. Hãy xem xét chương trình này::

   import asyncio

   async def coro_a():
      print("I am coro_a(). Hi!")

   async def coro_b():
      print("I am coro_b(). I sure hope no one hogs the event loop...")

   async def main():
      task_b = asyncio.create_task(coro_b())
      num_repeats = 3
      for _ in range(num_repeats):
         await coro_a()
      await task_b

   asyncio.run(main())

Câu lệnh đầu tiên trong coroutine ``main()`` tạo ``task_b`` và lên lịch thực thi nó thông qua event loop. Sau đó, ``coro_a()`` được await lặp đi lặp lại. Quyền điều khiển không bao giờ được nhường cho event loop, đó là lý do chúng ta thấy đầu ra của cả ba lần gọi ``coro_a()`` trước đầu ra của ``coro_b()``:

.. code-block:: none

   I am coro_a(). Hi!
   I am coro_a(). Hi!
   I am coro_a(). Hi!
   I am coro_b(). I sure hope no one hogs the event loop...

Nếu chúng ta thay đổi ``await coro_a()`` thành ``await asyncio.create_task(coro_a())``, hành vi sẽ thay đổi. Với câu lệnh đó, coroutine ``main()`` nhường quyền điều khiển cho event loop. Sau đó, event loop tiếp tục xử lý các công việc đang chờ, gọi ``task_b`` rồi đến task bọc ``coro_a()`` trước khi tiếp tục chạy coroutine ``main()``.

.. code-block:: none

   I am coro_b(). I sure hope no one hogs the event loop...
   I am coro_a(). Hi!
   I am coro_a(). Hi!
   I am coro_a(). Hi!

Hành vi này của ``await coroutine`` có thể khiến nhiều người bối rối! Ví dụ đó cho thấy việc chỉ sử dụng ``await coroutine`` có thể vô tình chiếm quyền điều khiển từ các task khác và thực tế làm event loop bị đình trệ.
:func:`asyncio.run` có thể giúp bạn phát hiện những trường hợp như vậy thông qua cờ ``debug=True``, cờ này cho phép
:ref:`chế độ debug <asyncio-debug-mode>`. Trong số những việc khác, nó sẽ ghi lại mọi coroutine chiếm quyền thực thi trong 100ms trở lên.

Thiết kế này cố ý đánh đổi một phần tính rõ ràng về mặt khái niệm khi sử dụng ``await`` để cải thiện hiệu suất. Mỗi khi một task được await, quyền điều khiển cần được truyền ngược lên toàn bộ call stack đến event loop. Điều đó có thể nghe có vẻ không đáng kể, nhưng trong một chương trình lớn với nhiều câu lệnh ``await`` và call stack sâu, phần overhead đó có thể tích tụ thành mức suy giảm hiệu suất đáng kể.

---------------------------------------------------
Tổng quan khái niệm, phần 2: các chi tiết bên trong
---------------------------------------------------

Phần 2 đi sâu vào các cơ chế mà :mod:`!asyncio` sử dụng để quản lý control flow. Đây là nơi phép màu xảy ra. Sau khi hoàn thành phần này, bạn sẽ hiểu ``await`` thực hiện những gì ở phía sau và cách tạo các toán tử bất đồng bộ của riêng mình.

========================================
Cơ chế hoạt động bên trong của coroutine
========================================

:mod:`!asyncio` sử dụng bốn thành phần để truyền quyền điều khiển.

:meth:`coroutine.send(arg) <generator.send>` là phương thức được dùng để bắt đầu hoặc tiếp tục một coroutine. Nếu coroutine đã bị tạm dừng và hiện đang được tiếp tục, đối số ``arg`` sẽ được truyền vào làm giá trị trả về của câu lệnh ``yield`` vốn đã tạm dừng coroutine đó. Nếu coroutine đang được sử dụng lần đầu tiên (thay vì được tiếp tục), ``arg`` phải là ``None``.

.. code-block::
   :linenos:

   class Rock:
       def __await__(self):
           value_sent_in = yield 7
           print(f"Rock.__await__ resuming with value: {value_sent_in}.")
           return value_sent_in

   async def main():
       print("Beginning coroutine main().")
       rock = Rock()
       print("Awaiting rock...")
       value_from_rock = await rock
       print(f"Coroutine received value: {value_from_rock} from rock.")
       return 23

   coroutine = main()
   intermediate_result = coroutine.send(None)
   print(f"Coroutine paused and returned intermediate value: {intermediate_result}.")

   print(f"Resuming coroutine and sending in value: 42.")
   try:
       coroutine.send(42)
   except StopIteration as e:
       returned_value = e.value
   print(f"Coroutine main() finished and provided value: {returned_value}.")

:ref:`yield <yieldexpr>`, như thường lệ, tạm dừng quá trình thực thi và trả quyền điều khiển về cho bên gọi. Trong ví dụ trên, ``yield``, ở dòng 3, được gọi bởi ``... = await rock`` ở dòng 11. Nói rộng hơn, ``await`` gọi phương thức :meth:`~object.__await__` của đối tượng đã cho. ``await`` còn thực hiện thêm một việc rất đặc biệt: nó truyền (hay “chuyển tiếp”) mọi ``yield``\ s mà nó nhận được ngược lên chuỗi lời gọi. Trong trường hợp này, đó là quay lại ``... = coroutine.send(None)`` ở dòng 16.

Coroutine được tiếp tục thông qua lời gọi ``coroutine.send(42)`` ở dòng 21. Coroutine tiếp tục từ nơi nó ``yield``\ ed (hoặc tạm dừng) ở dòng 3 và thực thi các câu lệnh còn lại trong thân của nó. Khi một coroutine kết thúc, nó phát sinh một ngoại lệ :exc:`StopIteration`, trong đó giá trị trả về được đính kèm trong thuộc tính :attr:`~StopIteration.value`.

Đoạn mã đó tạo ra kết quả sau:

.. code-block:: none

   Beginning coroutine main().
   Awaiting rock...
   Coroutine paused and returned intermediate value: 7.
   Resuming coroutine and sending in value: 42.
   Rock.__await__ resuming with value: 42.
   Coroutine received value: 42 from rock.
   Coroutine main() finished and provided value: 23.

Bạn nên tạm dừng một chút ở đây để bảo đảm rằng mình đã theo dõi được những cách khác nhau mà luồng điều khiển và các giá trị được truyền đi. Đã có nhiều ý quan trọng được đề cập, vì vậy bạn nên chắc chắn rằng mình đã nắm vững chúng.

Cách duy nhất để yield (hoặc thực chất là nhường quyền điều khiển) từ một coroutine là ``await`` một đối tượng ``yield``\ s trong phương thức ``__await__`` của nó. Điều này có thể khiến bạn thấy kỳ lạ. Có thể bạn đang nghĩ:

   1. Còn ``yield`` trực tiếp bên trong hàm coroutine thì sao? The
   coroutine function trở thành một
   :ref:`async generator function <asynchronous-generator-functions>`, hoàn toàn khác biệt.

   2. Còn :ref:`yield from <yieldexpr>` bên trong hàm coroutine để tạo ra một
   generator thì sao? Điều đó gây ra lỗi: ``SyntaxError: yield from not allowed in a coroutine.`` Điều này được thiết kế có chủ ý để đơn giản hóa — chỉ yêu cầu một cách duy nhất để sử dụng coroutine. Ban đầu ``yield`` cũng bị cấm, nhưng sau đó được chấp nhận lại để cho phép async generator. Mặc dù vậy, ``yield from`` và ``await`` thực tế làm cùng một việc.

=======
Futures
=======

Một :ref:`future <asyncio-future-obj>` là một đối tượng dùng để biểu diễn trạng thái và kết quả của một phép tính. Thuật ngữ này gợi đến ý tưởng về một điều vẫn sẽ xảy ra hoặc chưa xảy ra, còn đối tượng này là cách để theo dõi điều đó.

Một future có một số thuộc tính quan trọng. Một thuộc tính là trạng thái của nó, có thể là "pending", "cancelled" hoặc "done". Một thuộc tính khác là kết quả, được thiết lập khi trạng thái chuyển sang done. Không giống coroutine, future không biểu diễn phép tính thực sự cần được thực hiện; thay vào đó, nó biểu diễn trạng thái và kết quả của phép tính đó, gần giống như đèn trạng thái (đỏ, vàng hoặc xanh lục) hay đèn báo.

:class:`asyncio.Task` kế thừa :class:`asyncio.Future` để có được nhiều khả năng khác nhau. Phần trước nói rằng task lưu trữ một danh sách callback, điều này không hoàn toàn chính xác. Thực ra, chính lớp ``Future`` triển khai logic này, và ``Task`` kế thừa lớp đó.

Futures cũng có thể được sử dụng trực tiếp (không thông qua tasks). Tasks tự đánh dấu là đã hoàn tất khi coroutine của chúng hoàn thành. Futures linh hoạt hơn nhiều và sẽ được đánh dấu là đã hoàn tất khi bạn yêu cầu. Theo cách này, chúng là giao diện linh hoạt để bạn tự tạo các điều kiện chờ và tiếp tục thực thi.

========================
Một asyncio.sleep tự tạo
========================

Chúng ta sẽ xem qua một ví dụ về cách bạn có thể tận dụng một future để tạo biến thể riêng của thao tác sleep bất đồng bộ (``async_sleep``) mô phỏng
:func:`asyncio.sleep`.

Đoạn mã này đăng ký một vài task với event loop, sau đó await task được tạo bởi ``asyncio.create_task``, task này bao bọc coroutine ``async_sleep(3)``. Chúng ta muốn task đó chỉ hoàn tất sau khi ba giây trôi qua, nhưng không ngăn các task khác chạy.

::

   async def other_work():
       print("I like work. Work work.")

   async def main():
       # Thêm một vài task khác vào event loop để có việc
       # thực hiện trong khi đang sleep bất đồng bộ.
       work_tasks = [
           asyncio.create_task(other_work()),
           asyncio.create_task(other_work()),
           asyncio.create_task(other_work())
       ]
       print(
           "Beginning asynchronous sleep at time: "
           f"{datetime.datetime.now().strftime("%H:%M:%S")}."
       )
       await asyncio.create_task(async_sleep(3))
       print(
           "Done asynchronous sleep at time: "
           f"{datetime.datetime.now().strftime("%H:%M:%S")}."
       )
       # asyncio.gather về cơ bản await từng task trong tập hợp.
       await asyncio.gather(*work_tasks)


Dưới đây, chúng ta sử dụng một future để cho phép kiểm soát tùy chỉnh thời điểm task đó được đánh dấu là đã hoàn tất. Nếu :meth:`future.set_result() <asyncio.Future.set_result>` (phương thức chịu trách nhiệm đánh dấu future đó là đã hoàn tất) không bao giờ được gọi, thì task này sẽ không bao giờ kết thúc. Chúng ta cũng nhờ đến sự hỗ trợ của một task khác, mà chúng ta sẽ xem ngay sau đây, để theo dõi thời gian đã trôi qua và từ đó gọi ``future.set_result()``.

::

   async def async_sleep(seconds: float):
       future = asyncio.Future()
       time_to_wake = time.time() + seconds
       # Thêm watcher-task vào event loop.
       watcher_task = asyncio.create_task(_sleep_watcher(future, time_to_wake))
       # Chặn cho đến khi future được đánh dấu là đã hoàn tất.
       await future

Dưới đây, chúng ta sử dụng một đối tượng ``YieldToEventLoop()`` khá đơn giản để ``yield`` từ phương thức ``__await__`` của nó, nhường quyền điều khiển cho event loop. Cách này về cơ bản tương đương với việc gọi ``asyncio.sleep(0)``, nhưng cách tiếp cận này rõ ràng hơn, chưa kể việc sử dụng ``asyncio.sleep`` khi trình bày cách triển khai nó cũng có phần gian lận!

Như thường lệ, event loop tuần tự xử lý các task, trao quyền điều khiển cho chúng và nhận lại quyền điều khiển khi chúng tạm dừng hoặc kết thúc. ``watcher_task``, chạy coroutine ``_sleep_watcher(...)``, sẽ được gọi một lần trong mỗi chu kỳ hoàn chỉnh của event loop. Mỗi khi được tiếp tục, nó sẽ kiểm tra thời gian; nếu chưa đủ thời gian trôi qua, nó sẽ lại tạm dừng và trả quyền điều khiển cho event loop. Khi đã đủ thời gian trôi qua, ``_sleep_watcher(...)`` đánh dấu future là đã hoàn tất và kết thúc bằng cách thoát khỏi vòng lặp ``while`` vô hạn. Vì task trợ giúp này chỉ được gọi một lần trong mỗi chu kỳ của event loop, bạn có thể nhận thấy rằng thao tác sleep bất đồng bộ này sẽ ngủ *ít nhất* ba giây, thay vì chính xác ba giây. Lưu ý rằng điều này cũng đúng với ``asyncio.sleep``.

::

   class YieldToEventLoop:
       def __await__(self):
           yield

   async def _sleep_watcher(future, time_to_wake):
       while True:
           if time.time() >= time_to_wake:
               # Đánh dấu future là đã hoàn tất.
               future.set_result(None)
               break
           else:
               await YieldToEventLoop()

Đây là đầu ra của toàn bộ chương trình:

.. code-block:: none

   $ python custom-async-sleep.py
   Beginning asynchronous sleep at time: 14:52:22.
   I like work. Work work.
   I like work. Work work.
   I like work. Work work.
   Done asynchronous sleep at time: 14:52:25.

Bạn có thể cảm thấy cách triển khai sleep bất đồng bộ này quá rườm rà. Và đúng là như vậy. Ví dụ này nhằm minh họa tính linh hoạt của futures bằng một ví dụ đơn giản có thể được áp dụng tương tự cho những nhu cầu phức tạp hơn. Để tham khảo, bạn có thể triển khai nó mà không cần futures như sau::

   async def simpler_async_sleep(seconds):
       time_to_wake = time.time() + seconds
       while True:
           if time.time() >= time_to_wake:
               return
           else:
               await YieldToEventLoop()

Nhưng hiện tại chỉ đến đây thôi. Hy vọng bạn đã sẵn sàng hơn để tự tin tìm hiểu về lập trình bất đồng bộ hoặc khám phá các chủ đề nâng cao trong
:mod:`rest of the documentation <asyncio>`.

.. _`guide`: https://github.com/anordin95/a-conceptual-overview-of-asyncio/ tree/main
.. _`YouTube tutorial series`: https://www.youtube.com/ watch?v=Xbl7XjFYsN4&list=PLhNSoGM2ik6SIkVGXWBwerucXjgP1rHmB
.. _`500 Lines or Less: A Web Crawler With asyncio Coroutines`: https:// aosabook.org/en/500L/a-web-crawler-with-asyncio-coroutines.html
