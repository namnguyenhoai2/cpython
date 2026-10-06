.. currentmodule:: asyncio


=======
Mở rộng
=======

Hướng chính để mở rộng :mod:`asyncio` là viết các lớp *event loop* tùy chỉnh. Asyncio cung cấp các helper có thể được dùng để đơn giản hóa nhiệm vụ này.

.. note::

   Các bên thứ ba nên thận trọng khi sử dụng lại mã asyncio hiện có; một phiên bản Python mới có thể tự do phá vỡ khả năng tương thích ngược trong phần *internal* của API.


Viết Event Loop tùy chỉnh
=========================

:class:`asyncio.AbstractEventLoop` khai báo rất nhiều phương thức. Việc triển khai tất cả các phương thức đó từ đầu là một công việc tẻ nhạt.

Một loop có thể được thừa hưởng miễn phí phần triển khai của nhiều phương thức phổ biến bằng cách kế thừa từ
:class:`asyncio.BaseEventLoop`.

Đổi lại, lớp kế thừa phải triển khai một loạt phương thức *private* được khai báo nhưng chưa được triển khai trong :class:`asyncio.BaseEventLoop`.

Ví dụ, ``loop.create_connection()`` kiểm tra các đối số, phân giải địa chỉ DNS và gọi ``loop._make_socket_transport()``, vốn cần được triển khai bởi lớp kế thừa. Phương thức ``_make_socket_transport()`` không được ghi chép và được xem là API *nội bộ*.



Các constructor riêng tư của Future và Task
===========================================

Không nên tạo trực tiếp :class:`asyncio.Future` và :class:`asyncio.Task`; hãy sử dụng :meth:`loop.create_future` và :meth:`loop.create_task` tương ứng, hoặc các factory :func:`asyncio.create_task`.

Tuy nhiên, các *event loop* của bên thứ ba có thể *tái sử dụng* các triển khai future và task tích hợp sẵn để có được miễn phí mã phức tạp và được tối ưu hóa cao.

Với mục đích này, các constructor *riêng tư* sau đây được liệt kê:

.. method:: Future.__init__(*, loop=None)

   Tạo một instance future tích hợp sẵn.

   *loop* là một instance event loop tùy chọn.

.. method:: Task.__init__(coro, *, loop=None, name=None, context=None)

   Tạo một instance task tích hợp sẵn.

   *loop* là một instance event loop tùy chọn. Các đối số còn lại được mô tả trong
   :meth:`loop.create_task` mô tả.

   .. versionchanged:: 3.11

      Đối số *context* được thêm vào.



Hỗ trợ vòng đời task
====================

Một implementation task của bên thứ ba nên gọi các hàm sau để task vẫn hiển thị với :func:`asyncio.all_tasks` và :func:`asyncio.current_task`:

.. function:: _register_task(task)

   Đăng ký một *task* mới dưới sự quản lý của *asyncio*.

   Gọi hàm từ một constructor của task.

.. function:: _unregister_task(task)

   Hủy đăng ký một *task* khỏi các cấu trúc nội bộ của *asyncio*.

   Hàm này sẽ được gọi khi một task sắp kết thúc.

.. function:: _enter_task(loop, task)

   Chuyển task hiện tại sang đối số *task*.

   Gọi hàm ngay trước khi thực thi một phần của *coroutine* được nhúng (:meth:`coroutine.send` hoặc :meth:`coroutine.throw`).

.. function:: _leave_task(loop, task)

   Chuyển task hiện tại trở lại từ *task* sang ``None``.

   Gọi hàm ngay sau khi thực thi :meth:`coroutine.send` hoặc :meth:`coroutine.throw`.
