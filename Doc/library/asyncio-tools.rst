.. currentmodule:: asyncio

.. _asyncio-introspection-tools:

=======================================
Các công cụ introspection qua dòng lệnh
=======================================

**Mã nguồn:** :source:`Lib/asyncio/tools.py`

-------------------------------------

Mô-đun :mod:`!asyncio` có thể được gọi như một script thông qua ``python -m asyncio`` để kiểm tra task graph của một tiến trình Python khác đang chạy mà không sửa đổi hoặc khởi động lại tiến trình đó. Submodule :mod:`!asyncio.tools` triển khai giao diện này.

Các lệnh sau đây kiểm tra tiến trình được xác định bởi ``PID``:

.. code-block:: shell-session

   $ python -m asyncio pstree PID
   $ python -m asyncio ps PID

Các lệnh này đọc trạng thái của tiến trình đích mà không thực thi bất kỳ mã nào trong đó. Chúng chỉ khả dụng trên các nền tảng được hỗ trợ và có thể yêu cầu quyền kiểm tra một tiến trình khác. Xem :ref:`yêu cầu quyền <permission-requirements>` để biết chi tiết.

.. seealso::

   :ref:`asyncio-graph`
      Các API lập trình để kiểm tra async call graph của một task hoặc future trong tiến trình hiện tại.

Các ví dụ về lệnh bên dưới sử dụng chương trình này; chương trình tạo một hệ thống phân cấp task phù hợp để kiểm tra và in ra process ID của nó:

.. code-block:: python
   :caption: example.py

   import asyncio
   import os

   async def play(track):
       await asyncio.sleep(3600)
       print(f"🎵 Finished: {track}")

   async def album(name, tracks):
       async with asyncio.TaskGroup() as tg:
           for track in tracks:
               tg.create_task(play(track), name=track)

   async def main():
       print(f"PID: {os.getpid()}")
       async with asyncio.TaskGroup() as tg:
           tg.create_task(
               album("Sundowning", ["TNDNBTG", "Levitate"]),
               name="Sundowning",
           )
           tg.create_task(
               album("TMBTE", ["DYWTYLM", "Aqua Regia"]),
               name="TMBTE",
           )

   asyncio.run(main())

Chạy chương trình trong một terminal và để chương trình tiếp tục chạy:

.. code-block:: shell-session

   $ python example.py
   PID: 12345

Sau đó, truyền ID tiến trình được in ra cho các lệnh từ một terminal khác. ID luồng, ID tác vụ, đường dẫn tệp và số dòng thay đổi tùy theo mỗi lần chạy và bố cục mã nguồn.

.. versionadded:: 3.14

Tùy chọn dòng lệnh
==================

.. option:: pstree PID

   Hiển thị mối quan hệ giữa các task và coroutine dưới dạng cây. Mỗi task được hiển thị cùng với toàn bộ coroutine stack của nó, lồng bên dưới task (nếu có) đang await task đó. Subcommand này hữu ích để nhanh chóng xác định nhánh nào trong hệ thống phân cấp task đang bị chặn và quá trình thực thi đã tạm dừng ở đâu trong coroutine stack của nhánh đó:

   .. code-block:: shell-session

      $ python -m asyncio pstree 12345
      └── (T) Task-1
          └──  main example.py:12
              └──  TaskGroup.__aexit__ Lib/asyncio/taskgroups.py:75
                  └──  TaskGroup._aexit Lib/asyncio/taskgroups.py:124
                      ├── (T) Sundowning
                      │   └──  album example.py:7
                      │       └──  TaskGroup.__aexit__ Lib/asyncio/taskgroups.py:75
                      │           └──  TaskGroup._aexit Lib/asyncio/taskgroups.py:124
                      │               ├── (T) TNDNBTG
                      │               │   └──  play example.py:4
                      │               │       └──  sleep Lib/asyncio/tasks.py:702
                      │               └── (T) Levitate
                      │                   └──  play example.py:4
                      │                       └──  sleep Lib/asyncio/tasks.py:702
                      └── (T) TMBTE
                          └──  album example.py:7
                              └──  TaskGroup.__aexit__ Lib/asyncio/taskgroups.py:75
                                  └──  TaskGroup._aexit Lib/asyncio/taskgroups.py:124
                                      ├── (T) DYWTYLM
                                      │   └──  play example.py:4
                                      │       └──  sleep Lib/asyncio/tasks.py:702
                                      └── (T) Aqua Regia
                                          └──  play example.py:4
                                              └──  sleep Lib/asyncio/tasks.py:702

   Nếu await graph chứa một chu kỳ, ``pstree`` sẽ báo lỗi thay vì in ra cây. Chu kỳ trong await graph là điều bất thường và thường cho thấy lỗi lập trình:

   .. code-block:: shell-session

      $ python -m asyncio pstree 12345
      ERROR: await-graph contains cycles - cannot print a tree!

      cycle: Task-2 → Task-3 → Task-2

.. option:: ps PID

   Hiển thị bảng phẳng gồm tất cả task đang chờ xử lý trong tiến trình *PID*. Mỗi hàng hiển thị ID luồng của event loop, ID và tên task, coroutine stack, cùng stack, tên và ID của task đang await task đó, nếu có.

   Subcommand này in ra tất cả các tác vụ bất kể đồ thị await có chứa chu kỳ hay không:

   .. code-block:: shell-session

      $ python -m asyncio ps 12345
      tid        task id              task name            coroutine stack                                    awaiter chain                                      awaiter name    awaiter id
      ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      18445801   0x10a456060          Task-1               TaskGroup._aexit -> TaskGroup.__aexit__ -> main                                                                       0x0
      18445801   0x10a439f60          Sundowning           TaskGroup._aexit -> TaskGroup.__aexit__ -> album   TaskGroup._aexit -> TaskGroup.__aexit__ -> main    Task-1          0x10a456060
      18445801   0x10a439d70          TMBTE                TaskGroup._aexit -> TaskGroup.__aexit__ -> album   TaskGroup._aexit -> TaskGroup.__aexit__ -> main    Task-1          0x10a456060
      18445801   0x10a2a3a80          TNDNBTG              sleep -> play                                      TaskGroup._aexit -> TaskGroup.__aexit__ -> album   Sundowning      0x10a439f60
      18445801   0x10a2a38a0          Levitate             sleep -> play                                      TaskGroup._aexit -> TaskGroup.__aexit__ -> album   Sundowning      0x10a439f60
      18445801   0x10a2d7150          DYWTYLM              sleep -> play                                      TaskGroup._aexit -> TaskGroup.__aexit__ -> album   TMBTE           0x10a439d70
      18445801   0x10a6bdaa0          Aqua Regia           sleep -> play                                      TaskGroup._aexit -> TaskGroup.__aexit__ -> album   TMBTE           0x10a439d70
