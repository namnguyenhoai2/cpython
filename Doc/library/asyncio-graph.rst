.. currentmodule:: asyncio


.. _asyncio-graph:

=================================
Phân tích nội quan đồ thị lời gọi
=================================

**Mã nguồn:** :source:`Lib/asyncio/graph.py`

-------------------------------------

asyncio cung cấp các tiện ích mạnh mẽ để phân tích nội quan đồ thị lời gọi trong runtime, cho phép truy vết toàn bộ đồ thị lời gọi của một *coroutine* đang chạy hoặc một *task*, hay một *future* đang bị tạm dừng. Các tiện ích này và cơ chế nền tảng có thể được sử dụng từ bên trong một chương trình Python hoặc bởi các profiler và debugger bên ngoài.

.. seealso::

   :ref:`asyncio-introspection-tools`
      Các công cụ dòng lệnh để kiểm tra các task trong một tiến trình Python khác đang chạy.

.. versionadded:: 3.14


.. function:: print_call_graph(future=None, /, *, file=None, depth=1, limit=None)

   In đồ thị lời gọi async cho task hiện tại hoặc đối tượng được cung cấp
   :class:`Task` hoặc :class:`Future`.

   Hàm này in các mục bắt đầu từ frame trên cùng và đi xuống về phía điểm gọi.

   Hàm nhận một đối số *future* tùy chọn. Nếu không được truyền vào, task đang chạy hiện tại sẽ được sử dụng.

   Nếu hàm được gọi trên *the current task*, có thể sử dụng đối số chỉ dành cho keyword *depth* tùy chọn để bỏ qua số frame được chỉ định tính từ đầu stack.

   Nếu cung cấp đối số chỉ dành cho keyword *limit* tùy chọn, mỗi call stack trong graph kết quả sẽ được rút gọn để chứa nhiều nhất ``abs(limit)`` mục. Nếu *limit* là số dương, các mục còn lại sẽ là những mục gần điểm gọi nhất. Nếu *limit* là số âm, các mục ở đầu stack sẽ được giữ lại. Nếu *limit* bị bỏ qua hoặc là ``None``, tất cả các mục sẽ được giữ lại. Nếu *limit* là ``0``, call stack hoàn toàn không được in ra, mà chỉ in thông tin "awaited by".

   Nếu *file* bị bỏ qua hoặc là ``None``, hàm sẽ in ra :data:`sys.stdout`.

   **Ví dụ:**

   Đoạn mã Python sau đây:

   .. code-block:: python

      import asyncio

      async def test():
          asyncio.print_call_graph()

      async def main():
          async with asyncio.TaskGroup() as g:
              g.create_task(test(), name='test')

      asyncio.run(main())

   sẽ in ra::

      * Task(name='test', id=0x1039f0fe0)
      + Call stack:
      |   File 't2.py', line 4, in async test()
      + Awaited by:
         * Task(name='Task-1', id=0x103a5e060)
            + Call stack:
            |   File 'taskgroups.py', line 107, in async TaskGroup.__aexit__()
            |   File 't2.py', line 7, in async main()

.. function:: format_call_graph(future=None, /, *, depth=1, limit=None)

   Tương tự :func:`print_call_graph`, nhưng trả về một chuỗi. Nếu *future* là ``None`` và không có task hiện tại, hàm sẽ trả về một chuỗi rỗng.


.. function:: capture_call_graph(future=None, /, *, depth=1, limit=None)

   Ghi lại call graph bất đồng bộ cho task hiện tại hoặc task được cung cấp
   :class:`Task` hoặc :class:`Future`.

   Hàm nhận một đối số *future* tùy chọn. Nếu không được truyền vào, task đang chạy hiện tại sẽ được sử dụng. Nếu không có task hiện tại, hàm sẽ trả về ``None``.

   Nếu hàm được gọi trên *the current task*, có thể sử dụng đối số chỉ dành cho keyword *depth* tùy chọn để bỏ qua số frame được chỉ định tính từ đầu stack.

   Trả về một đối tượng lớp dữ liệu ``FutureCallGraph``:

   * ``FutureCallGraph(future, call_stack, awaited_by)``

      Trong đó, *future* là tham chiếu đến một :class:`Future` hoặc một :class:`Task` (hoặc các lớp con của chúng).

      ``call_stack`` là một tuple gồm các đối tượng ``FrameCallGraphEntry``.

      ``awaited_by`` là một tuple gồm các đối tượng ``FutureCallGraph``.

   * ``FrameCallGraphEntry(frame)``

      Trong đó, *frame* là một đối tượng frame của một hàm Python thông thường trong call stack.


Các hàm tiện ích cấp thấp
=========================

Để introspect call graph bất đồng bộ, asyncio yêu cầu sự phối hợp từ các cấu trúc control flow, chẳng hạn như :func:`shield` hoặc :class:`TaskGroup`. Bất cứ khi nào có một đối tượng :class:`Future` trung gian với các API cấp thấp như
Khi :meth:`Future.add_done_callback() <asyncio.Future.add_done_callback>` có liên quan, nên sử dụng hai hàm sau để thông báo cho asyncio biết chính xác các đối tượng future trung gian như vậy được kết nối với các task mà chúng bao bọc hoặc điều khiển như thế nào.


.. function:: future_add_to_awaited_by(future, waiter, /)

   Ghi lại rằng *future* được *waiter* chờ đợi.

   Cả *future* và *waiter* đều phải là các thực thể của
   :class:`Future` hoặc :class:`Task`, hoặc các lớp con của chúng; nếu không, lệnh gọi sẽ không có tác dụng.

   Một lệnh gọi đến ``future_add_to_awaited_by()`` phải được tiếp nối bằng một lệnh gọi sau đó đến hàm :func:`future_discard_from_awaited_by` với cùng các đối số.


.. function:: future_discard_from_awaited_by(future, waiter, /)

   Ghi nhận rằng *future* không còn được *waiter* chờ đợi nữa.

   Cả *future* và *waiter* đều phải là các thực thể của
   :class:`Future` hoặc :class:`Task`, hoặc các lớp con của chúng; nếu không, lệnh gọi sẽ không có tác dụng.
