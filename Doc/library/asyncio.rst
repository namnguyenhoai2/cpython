:mod:`!asyncio` --- I/O bất đồng bộ
===================================

.. module:: asyncio
   :synopsis: I/O bất đồng bộ.

-------------------------------

.. sidebar:: Hello World!

   ::

       import asyncio

       async def main():
           print('Hello ...')
           await asyncio.sleep(1)
           print('... World!')

       asyncio.run(main())

asyncio là một thư viện để viết mã **đồng thời** bằng cú pháp **async/await**.

asyncio được dùng làm nền tảng cho nhiều framework bất đồng bộ của Python, cung cấp máy chủ mạng và web hiệu năng cao, thư viện kết nối cơ sở dữ liệu, hàng đợi tác vụ phân tán, v.v.

asyncio thường là lựa chọn hoàn hảo cho mã mạng **có cấu trúc** cấp cao và bị giới hạn bởi I/O.

.. seealso::

   :ref:`a-conceptual-overview-of-asyncio`
      Giải thích các khái niệm nền tảng của asyncio.

asyncio cung cấp một tập hợp các API **cấp cao** để:

* :ref:`chạy đồng thời các coroutine Python <coroutine>` và toàn quyền kiểm soát việc thực thi chúng;

* thực hiện :ref:`I/O mạng và IPC <asyncio-streams>`;

* điều khiển :ref:`các tiến trình con <asyncio-subprocess>`;

* phân phối các tác vụ thông qua :ref:`các queue <asyncio-queues>`;

* :ref:`đồng bộ hóa <asyncio-sync>` mã chạy đồng thời;

Để **kiểm tra nội tại**, asyncio cung cấp các API và công cụ cho:

* kiểm tra :ref:`đồ thị lời gọi async <asyncio-graph>` của các task và future;

* kiểm tra các task trong một tiến trình Python khác đang chạy bằng
  :ref:`công cụ dòng lệnh <asyncio-introspection-tools>`;

Ngoài ra, còn có các API **cấp thấp** dành cho *nhà phát triển thư viện và framework* để:

* tạo và quản lý :ref:`event loop <asyncio-event-loop>`, cung cấp các API bất đồng bộ cho :ref:`kết nối mạng <loop_create_server>`, chạy :ref:`tiến trình con <loop_subprocess_exec>`, xử lý :ref:`tín hiệu OS <loop_add_signal_handler>`, v.v.;

* triển khai các protocol hiệu quả bằng
  :ref:`transport <asyncio-transports-protocols>`;

* :ref:`kết nối <asyncio-futures>` các thư viện dựa trên callback và mã bằng cú pháp async/await.

.. include:: ../includes/wasm-notavail.rst

.. _asyncio-cli:

.. rubric:: REPL asyncio

Bạn có thể thử nghiệm trong một ``asyncio`` ngữ cảnh đồng thời trong :term:`REPL`:

.. code-block:: pycon

   $ python -m asyncio
   asyncio REPL ...
   Use "await" directly instead of "asyncio.run()".
   Type "help", "copyright", "credits" or "license" for more information.
   >>> import asyncio
   >>> await asyncio.sleep(10, result='hello')
   'hello'

REPL này cung cấp khả năng tương thích hạn chế với :envvar:`PYTHON_BASIC_REPL`. Bạn nên sử dụng REPL mặc định để có đầy đủ chức năng và các tính năng mới nhất.

.. audit-event:: cpython.run_stdin "" ""

.. versionchanged:: 3.12.5 (cũng là 3.11.10, 3.10.15, 3.9.20 và 3.8.20)
   Phát ra các sự kiện audit.

.. versionchanged:: 3.13
   Sử dụng PyREPL nếu có thể; trong trường hợp đó, :envvar:`PYTHONSTARTUP` cũng được thực thi. Phát ra các sự kiện audit.

.. We use the "rubric" directive here to avoid creating
   the "Reference" subsection in the TOC.

.. rubric:: Tài liệu tham khảo

.. toctree::
   :caption: API cấp cao
   :maxdepth: 1

   asyncio-runner.rst
   asyncio-task.rst
   asyncio-stream.rst
   asyncio-sync.rst
   asyncio-subprocess.rst
   asyncio-queue.rst
   asyncio-exceptions.rst

.. toctree::
   :caption: API kiểm tra nội tại
   :maxdepth: 1

   asyncio-graph.rst
   asyncio-tools.rst

.. toctree::
   :caption: API cấp thấp
   :maxdepth: 1

   asyncio-eventloop.rst
   asyncio-future.rst
   asyncio-protocol.rst
   asyncio-policy.rst
   asyncio-platforms.rst
   asyncio-extending.rst

.. toctree::
   :caption: Hướng dẫn và bài hướng dẫn
   :maxdepth: 1

   asyncio-api-index.rst
   asyncio-llapi-index.rst
   asyncio-dev.rst
   asyncio-threading.rst

.. note::
   Mã nguồn của asyncio có thể được tìm thấy trong :source:`Lib/asyncio/`.
