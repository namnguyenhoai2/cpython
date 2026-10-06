.. currentmodule:: asyncio


.. _asyncio-policies:

==========
Chính sách
==========

.. warning::

   Các chính sách đã bị phản đối và sẽ bị xóa trong Python 3.16. Người dùng nên sử dụng hàm :func:`asyncio.run` hoặc :class:`asyncio.Runner` với *loop_factory* để sử dụng cách triển khai event loop mong muốn.


Policy của event loop là một đối tượng toàn cục được dùng để lấy và thiết lập :ref:`event loop <asyncio-event-loop>` hiện tại, cũng như tạo các event loop mới. Policy mặc định có thể được :ref:`thay thế <asyncio-policy-get-set>` bằng
:ref:`các lựa chọn tích hợp sẵn <asyncio-policy-builtin>` để sử dụng các cách triển khai event loop khác nhau, hoặc được thay thế bằng một :ref:`policy tùy chỉnh <asyncio-custom-policies>` có thể ghi đè các hành vi này.

:ref:`Đối tượng policy <asyncio-policy-objects>` lấy và thiết lập một event loop riêng cho mỗi *ngữ cảnh*. Theo mặc định, ngữ cảnh này là theo thread, nhưng các policy tùy chỉnh có thể định nghĩa *ngữ cảnh* theo cách khác.

Các policy event loop tùy chỉnh có thể kiểm soát hành vi của
:func:`get_event_loop`, :func:`set_event_loop` và :func:`new_event_loop`.

Các đối tượng policy phải triển khai các API được định nghĩa trong lớp cơ sở trừu tượng :class:`AbstractEventLoopPolicy`.


.. _asyncio-policy-get-set:

Lấy và thiết lập Policy
=======================

Có thể sử dụng các hàm sau để lấy và thiết lập policy cho tiến trình hiện tại:

.. function:: get_event_loop_policy()

   Trả về policy áp dụng trên toàn bộ tiến trình hiện tại.

   .. deprecated:: 3.14
      Hàm :func:`get_event_loop_policy` đã lỗi thời và sẽ bị xóa trong Python 3.16.

.. function:: set_event_loop_policy(policy)

   Thiết lập policy áp dụng trên toàn bộ tiến trình hiện tại thành *policy*.

   Nếu *policy* được đặt thành ``None``, policy mặc định sẽ được khôi phục.

   .. deprecated:: 3.14
      Hàm :func:`set_event_loop_policy` không được dùng nữa và sẽ bị loại bỏ trong Python 3.16.


.. _asyncio-policy-objects:

Đối tượng Policy
================

Lớp cơ sở policy trừu tượng của event loop được định nghĩa như sau:

.. class:: AbstractEventLoopPolicy

   Lớp cơ sở trừu tượng dành cho các policy của asyncio.

   .. method:: get_event_loop()

      Lấy event loop cho context hiện tại.

      Trả về một đối tượng event loop triển khai
      giao diện :class:`AbstractEventLoop`.

      Phương thức này không bao giờ được trả về ``None``.

      .. versionchanged:: 3.6

   .. method:: set_event_loop(loop)

      Đặt event loop cho ngữ cảnh hiện tại thành *loop*.

   .. method:: new_event_loop()

      Tạo và trả về một đối tượng event loop mới.

      Phương thức này không bao giờ được trả về ``None``.

   .. deprecated:: 3.14
      Lớp :class:`AbstractEventLoopPolicy` đã lỗi thời và sẽ bị xóa trong Python 3.16.


.. _asyncio-policy-builtin:

asyncio đi kèm các policy tích hợp sẵn sau:


.. class:: DefaultEventLoopPolicy

   Policy asyncio mặc định. Sử dụng :class:`SelectorEventLoop` trên Unix và :class:`ProactorEventLoop` trên Windows.

   Không cần cài đặt policy mặc định theo cách thủ công. asyncio được cấu hình để tự động sử dụng policy mặc định.

   .. versionchanged:: 3.8

      Trên Windows, :class:`ProactorEventLoop` hiện được sử dụng theo mặc định.

   .. versionchanged:: 3.14
      Phương thức :meth:`get_event_loop` của policy asyncio mặc định hiện sẽ raise một :exc:`RuntimeError` nếu chưa có event loop nào được thiết lập.

   .. deprecated:: 3.14
      Lớp :class:`DefaultEventLoopPolicy` không được dùng nữa và sẽ bị loại bỏ trong Python 3.16.


.. class:: WindowsSelectorEventLoopPolicy

   Một policy event loop thay thế sử dụng
   triển khai event loop :class:`SelectorEventLoop`.

   .. availability:: Windows.

   .. deprecated:: 3.14
      Lớp :class:`WindowsSelectorEventLoopPolicy` không được dùng nữa và sẽ bị loại bỏ trong Python 3.16.


.. class:: WindowsProactorEventLoopPolicy

   Một policy event loop thay thế sử dụng
   :class:`ProactorEventLoop` triển khai event loop.

   .. availability:: Windows.

   .. deprecated:: 3.14
      Lớp :class:`WindowsProactorEventLoopPolicy` đã deprecated và sẽ bị xóa trong Python 3.16.


.. _asyncio-custom-policies:

Chính sách tùy chỉnh
====================

Để triển khai một chính sách event loop mới, bạn nên kế thừa
:class:`DefaultEventLoopPolicy` và ghi đè các phương thức cần hành vi tùy chỉnh, ví dụ:::

    class MyEventLoopPolicy(asyncio.DefaultEventLoopPolicy):

        def get_event_loop(self):
            """Get the event loop.

            This may be None or an instance of EventLoop.
            """
            loop = super().get_event_loop()
            # Làm gì đó với loop ...
            return loop

    asyncio.set_event_loop_policy(MyEventLoopPolicy())
