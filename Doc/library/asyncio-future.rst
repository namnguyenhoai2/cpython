.. currentmodule:: asyncio


.. _asyncio-futures:

======
Future
======

**Mã nguồn:** :source:`Lib/asyncio/futures.py`,
:source:`Lib/asyncio/base_futures.py`

-------------------------------------

Các đối tượng *Future* được dùng để kết nối **mã dựa trên callback cấp thấp** với mã async/await cấp cao.


Các hàm Future
==============

.. function:: isfuture(obj)

   Trả về ``True`` nếu *obj* là một trong các trường hợp sau:

   * một thực thể của :class:`asyncio.Future`,
   * một thực thể của :class:`asyncio.Task`,
   * một đối tượng tương tự Future có thuộc tính ``_asyncio_future_blocking``.

   .. versionadded:: 3.5


.. function:: ensure_future(obj, *, loop=None)

   Trả về:

   * đối số *obj* nguyên trạng nếu *obj* là một :class:`Future`, một :class:`Task` hoặc một đối tượng tương tự Future (:func:`isfuture` được dùng để kiểm tra).

   * một đối tượng :class:`Task` bao bọc *obj* nếu *obj* là một coroutine (:func:`iscoroutine` được dùng để kiểm tra); trong trường hợp này, coroutine sẽ được ``ensure_future()`` lên lịch.

   * một đối tượng :class:`Task` sẽ await trên *obj* nếu *obj* là một awaitable (:func:`inspect.isawaitable` được dùng để kiểm tra).

   Nếu *obj* không thuộc bất kỳ loại nào nêu trên, một :exc:`TypeError` sẽ được đưa ra.

   .. important::

      Hãy lưu một tham chiếu đến kết quả của hàm này để tránh việc task biến mất giữa chừng trong khi thực thi.

      Xem thêm hàm :func:`create_task`, đây là cách được khuyến nghị để tạo các task mới, hoặc sử dụng :class:`asyncio.TaskGroup`, hàm này lưu tham chiếu đến task internally.

   .. versionchanged:: 3.5.1
      Hàm này chấp nhận bất kỳ đối tượng :term:`awaitable` nào.

   .. deprecated:: 3.10
      Cảnh báo ngừng sử dụng được phát ra nếu *obj* không phải là đối tượng giống Future, *loop* không được chỉ định và không có event loop đang chạy.


.. function:: wrap_future(future, *, loop=None)

   Bọc một đối tượng :class:`concurrent.futures.Future` vào một
   đối tượng :class:`asyncio.Future`.

   .. deprecated:: 3.10
      Cảnh báo ngừng sử dụng được phát ra nếu *future* không phải là đối tượng giống Future, *loop* không được chỉ định và không có event loop đang chạy.

.. _asyncio-future-obj:

Đối tượng Future
================

.. class:: Future(*, loop=None)

   Future biểu diễn kết quả sẽ có của một thao tác bất đồng bộ. Không an toàn khi sử dụng giữa các thread.

   Future là một đối tượng :term:`awaitable`. Coroutine có thể await các đối tượng Future cho đến khi chúng có kết quả hoặc exception, hoặc bị hủy. Có thể await một Future nhiều lần và kết quả vẫn giống nhau.

   Thông thường, Future được dùng để cho phép mã cấp thấp dựa trên callback (ví dụ: trong các protocol được triển khai bằng asyncio
   :ref:`transports <asyncio-transports-protocols>`) tương tác với mã async/await cấp cao.

   Quy tắc chung là không bao giờ để lộ các đối tượng Future trong API hướng đến người dùng; cách được khuyến nghị để tạo một đối tượng Future là gọi
   :meth:`loop.create_future`. Bằng cách này, các triển khai event loop thay thế có thể đưa vào triển khai được tối ưu hóa riêng cho đối tượng Future.

   Future là :ref:`generic <generics>` theo kiểu dữ liệu của kết quả.

   .. versionchanged:: 3.7
      Đã thêm hỗ trợ cho module :mod:`contextvars`.

   .. deprecated:: 3.10
      Cảnh báo ngừng sử dụng được phát ra nếu *loop* không được chỉ định và không có event loop nào đang chạy.

   .. method:: result()

      Trả về kết quả của Future.

      Nếu Future ở trạng thái *done* và có kết quả được thiết lập bởi
      :meth:`set_result` phương thức, giá trị kết quả sẽ được trả về.

      Nếu Future ở trạng thái *done* và có ngoại lệ được thiết lập bởi
      :meth:`set_exception` phương thức, phương thức này sẽ ném ngoại lệ.

      Nếu Future đã bị *hủy*, phương thức này sẽ phát sinh một :exc:`CancelledError` ngoại lệ.

      Nếu kết quả của Future chưa có sẵn, phương thức này sẽ phát sinh một :exc:`InvalidStateError` ngoại lệ.

   .. method:: set_result(result)

      Đánh dấu Future là *hoàn tất* và đặt kết quả cho nó.

      Phát sinh một :exc:`InvalidStateError` lỗi nếu Future đã *hoàn tất*.

   .. method:: set_exception(exception)

      Đánh dấu Future là *hoàn tất* và đặt một ngoại lệ.

      Phát sinh một :exc:`InvalidStateError` lỗi nếu Future đã *hoàn tất*.

   .. method:: done()

      Trả về ``True`` nếu Future đã *hoàn tất*.

      Một Future ở trạng thái *hoàn tất* nếu nó đã bị *hủy* hoặc nếu nó đã có kết quả hoặc ngoại lệ được thiết lập bằng :meth:`set_result` hoặc
      :meth:`set_exception` các lời gọi.

   .. method:: cancelled()

      Trả về ``True`` nếu Future đã bị *hủy*.

      Phương thức này thường được dùng để kiểm tra xem Future có chưa bị *hủy* hay không trước khi thiết lập kết quả hoặc ngoại lệ cho nó::

          if not fut.cancelled():
              fut.set_result(42)

   .. method:: add_done_callback(callback, *, context=None)

      Thêm một callback sẽ được chạy khi Future ở trạng thái *hoàn tất*.

      *callback* được gọi với đối tượng Future là đối số duy nhất.

      Nếu Future đã ở trạng thái *hoàn tất* khi phương thức này được gọi, callback sẽ được lên lịch bằng :meth:`loop.call_soon`.

      Một đối số *context* chỉ nhận keyword tùy chọn cho phép chỉ định :class:`contextvars.Context` tùy chỉnh để *callback* chạy trong đó. Context hiện tại được sử dụng nếu không cung cấp *context*.

      Có thể sử dụng :func:`functools.partial` để truyền tham số cho callback, chẳng hạn như::

          # Gọi 'print("Future:", fut)' khi "fut" hoàn tất.
          fut.add_done_callback(
              functools.partial(print, "Future:"))

      .. versionchanged:: 3.7
         Tham số chỉ nhận keyword *context* đã được thêm. Xem :pep:`567` để biết thêm chi tiết.

   .. method:: remove_done_callback(callback)

      Xóa *callback* khỏi danh sách callback.

      Trả về số lượng callback đã xóa, thường là 1, trừ khi một callback được thêm nhiều lần.

   .. method:: cancel(msg=None)

      Hủy Future và lên lịch cho các callback.

      Nếu Future đã *done* hoặc *cancelled*, hãy trả về ``False``. Nếu không, hãy chuyển trạng thái của Future thành *cancelled*, lên lịch cho các callback rồi trả về ``True``.

      Đối số chuỗi tùy chọn *msg* được truyền làm đối số cho
      ngoại lệ :exc:`CancelledError` được raise khi await một Future đã bị hủy.

      .. versionchanged:: 3.9
         Đã thêm tham số *msg*.

   .. method:: exception()

      Trả về ngoại lệ đã được thiết lập trên Future này.

      Ngoại lệ (hoặc ``None`` nếu chưa có ngoại lệ nào được thiết lập) chỉ được trả về khi Future *done*.

      Nếu Future đã bị *cancelled*, phương thức này sẽ raise một
      :exc:`CancelledError` ngoại lệ.

      Nếu Future chưa *hoàn tất* thì phương thức này sẽ phát sinh một
      :exc:`InvalidStateError` ngoại lệ.

   .. method:: get_loop()

      Trả về event loop mà đối tượng Future được liên kết.

      .. versionadded:: 3.7


.. _asyncio_example_future:

Ví dụ này tạo một đối tượng Future, tạo và lên lịch một Task bất đồng bộ để đặt kết quả cho Future, rồi chờ cho đến khi Future có kết quả::

    async def set_after(fut, delay, value):
        # Ngủ trong *delay* giây.
        await asyncio.sleep(delay)

        # Đặt *value* làm kết quả của Future *fut*.
        fut.set_result(value)

    async def main():
        # Lấy event loop hiện tại.
        loop = asyncio.get_running_loop()

        # Tạo một đối tượng Future mới.
        fut = loop.create_future()

        # Chạy coroutine "set_after()" trong một Task song song.
        # Ở đây, chúng ta sử dụng API cấp thấp "loop.create_task()" vì
        # chúng ta đã có sẵn tham chiếu đến event loop.
        # Nếu không, chúng ta chỉ cần sử dụng "asyncio.create_task()".
        loop.create_task(
            set_after(fut, 1, '... world'))

        print('hello ...')

        # Chờ *fut* có kết quả (1 giây) rồi in kết quả đó.
        print(await fut)

    asyncio.run(main())


.. important::

   Đối tượng Future được thiết kế để mô phỏng
   :class:`concurrent.futures.Future`.  Các điểm khác biệt chính bao gồm:

   - không giống như các Future của asyncio, các đối tượng :class:`concurrent.futures.Future` không thể được await.

   - :meth:`asyncio.Future.result` và :meth:`asyncio.Future.exception` không chấp nhận đối số *timeout*.

   - :meth:`asyncio.Future.result` và :meth:`asyncio.Future.exception` phát sinh một ngoại lệ :exc:`InvalidStateError` khi Future chưa *done*.

   - Các callback được đăng ký với :meth:`asyncio.Future.add_done_callback` không được gọi ngay lập tức. Chúng được lên lịch bằng
     :meth:`loop.call_soon` thay vào đó.

   - asyncio Future không tương thích với
     :func:`concurrent.futures.wait` và
     :func:`concurrent.futures.as_completed` các hàm.

   - :meth:`asyncio.Future.cancel` chấp nhận một đối số ``msg`` tùy chọn, nhưng :meth:`concurrent.futures.Future.cancel` thì không.
