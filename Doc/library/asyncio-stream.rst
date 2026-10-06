.. currentmodule:: asyncio

.. _asyncio-streams:

=======
Streams
=======

**Mã nguồn:** :source:`Lib/asyncio/streams.py`

-------------------------------------------------

Streams là các primitive bất đồng bộ cấp cao, sẵn sàng sử dụng với async/await, để làm việc với các kết nối mạng. Streams cho phép gửi và nhận dữ liệu mà không cần sử dụng callback hoặc các protocol và transport cấp thấp.

.. _asyncio_example_stream:

Sau đây là một TCP echo client được viết bằng streams của asyncio::

    import asyncio

    async def tcp_echo_client(message):
        reader, writer = await asyncio.open_connection(
            '127.0.0.1', 8888)

        print(f'Send: {message!r}')
        writer.write(message.encode())
        await writer.drain()

        data = await reader.read(100)
        print(f'Received: {data.decode()!r}')

        print('Close the connection')
        writer.close()
        await writer.wait_closed()

    asyncio.run(tcp_echo_client('Hello World!'))


Xem thêm phần `Examples`_ bên dưới.


.. rubric:: Các hàm Stream

Có thể sử dụng các hàm asyncio cấp cao nhất sau đây để tạo và làm việc với streams:


.. function:: open_connection(host=None, port=None, *, \
                 limit=65536, ssl=None, family=0, proto=0, \ flags=0, sock=None, local_addr=None, \ server_hostname=None, ssl_handshake_timeout=None, \ ssl_shutdown_timeout=None, \ happy_eyeballs_delay=None, interleave=None)
   :async:

   Thiết lập kết nối mạng và trả về một cặp ``(reader, writer)`` đối tượng.

   Các đối tượng *reader* và *writer* được trả về là các thể hiện của
   :class:`StreamReader` và :class:`StreamWriter` các lớp.

   *limit* xác định giới hạn kích thước bộ đệm được sử dụng bởi thể hiện :class:`StreamReader` được trả về. Theo mặc định, *limit* được đặt thành 64 KiB.

   Các đối số còn lại được truyền trực tiếp tới
   :meth:`loop.create_connection`.

   .. note::

      Đối số *sock* chuyển quyền sở hữu socket cho
      :class:`StreamWriter` đã được tạo. Để đóng socket, hãy gọi
      phương thức :meth:`~asyncio.StreamWriter.close`.

   .. versionchanged:: 3.7
      Đã thêm tham số *ssl_handshake_timeout*.

   .. versionchanged:: 3.8
      Đã thêm các tham số *happy_eyeballs_delay* và *interleave*.

   .. versionchanged:: 3.10
      Đã xóa tham số *loop*.

   .. versionchanged:: 3.11
      Đã thêm tham số *ssl_shutdown_timeout*.


.. function:: start_server(client_connected_cb, host=None, \
                 port=None, *, limit=65536, \ family=socket.AF_UNSPEC, \ flags=socket.AI_PASSIVE, sock=None, \ backlog=100, ssl=None, reuse_address=None, \ reuse_port=None, keep_alive=None, \ ssl_handshake_timeout=None, \ ssl_shutdown_timeout=None, start_serving=True
   :async:

   Khởi động một máy chủ socket.

   Callback *client_connected_cb* được gọi bất cứ khi nào một kết nối client mới được thiết lập. Callback này nhận một cặp ``(reader, writer)`` dưới dạng hai đối số, là các thể hiện của :class:`StreamReader` và
   :class:`StreamWriter` các lớp.

   *client_connected_cb* có thể là một callable thông thường hoặc một
   :ref:`hàm coroutine <coroutine>`; nếu là một hàm coroutine, hàm này sẽ tự động được lập lịch dưới dạng một :class:`Task`.

   *limit* xác định giới hạn kích thước bộ đệm được sử dụng bởi thể hiện :class:`StreamReader` được trả về. Theo mặc định, *limit* được đặt thành 64 KiB.

   Các đối số còn lại được truyền trực tiếp tới
   :meth:`loop.create_server`.

   .. note::

      Đối số *sock* chuyển quyền sở hữu socket cho server được tạo. Để đóng socket, hãy gọi phương thức của server
      :meth:`~asyncio.Server.close`.

   .. versionchanged:: 3.7
      Đã thêm các tham số *ssl_handshake_timeout* và *start_serving*.

   .. versionchanged:: 3.10
      Đã xóa tham số *loop*.

   .. versionchanged:: 3.11
      Đã thêm tham số *ssl_shutdown_timeout*.

   .. versionchanged:: 3.13
      Đã thêm tham số *keep_alive*.


.. rubric:: Socket Unix

.. function:: open_unix_connection(path=None, *, limit=65536, \
               ssl=None, sock=None, server_hostname=None, \ ssl_handshake_timeout=None, ssl_shutdown_timeout=None)
   :async:

   Thiết lập kết nối socket Unix và trả về một cặp ``(reader, writer)``.

   Tương tự như :func:`open_connection` nhưng hoạt động trên các socket Unix.

   Xem thêm tài liệu về :meth:`loop.create_unix_connection`.

   .. note::

      Đối số *sock* chuyển quyền sở hữu socket cho
      :class:`StreamWriter` đã được tạo. Để đóng socket, hãy gọi
      phương thức :meth:`~asyncio.StreamWriter.close`.

   .. availability:: Unix.

   .. versionchanged:: 3.7
      Đã thêm tham số *ssl_handshake_timeout*. Tham số *path* giờ đây có thể là :term:`path-like object`

   .. versionchanged:: 3.10
      Đã xóa tham số *loop*.

   .. versionchanged:: 3.11
      Đã thêm tham số *ssl_shutdown_timeout*.


.. function:: start_unix_server(client_connected_cb, path=None, \
                 *, limit=65536, sock=None, backlog=100, ssl=None, \ ssl_handshake_timeout=None, \ ssl_shutdown_timeout=None, start_serving=True, cleanup_socket=True)
   :async:

   Khởi động máy chủ Unix socket.

   Tương tự như :func:`start_server` nhưng hoạt động với Unix socket.

   Nếu *cleanup_socket* là true thì Unix socket sẽ tự động bị xóa khỏi hệ thống tệp khi máy chủ được đóng, trừ khi socket đã được thay thế sau khi máy chủ được tạo.

   Xem thêm tài liệu về :meth:`loop.create_unix_server`.

   .. note::

      Đối số *sock* chuyển quyền sở hữu socket cho server được tạo. Để đóng socket, hãy gọi phương thức của server
      :meth:`~asyncio.Server.close`.

   .. availability:: Unix.

   .. versionchanged:: 3.7
      Đã thêm các tham số *ssl_handshake_timeout* và *start_serving*. Tham số *path* hiện có thể là một :term:`path-like object`.

   .. versionchanged:: 3.10
      Đã xóa tham số *loop*.

   .. versionchanged:: 3.11
      Đã thêm tham số *ssl_shutdown_timeout*.

   .. versionchanged:: 3.13
      Đã thêm tham số *cleanup_socket*.


StreamReader
============

.. class:: StreamReader

   Đại diện cho một đối tượng reader cung cấp các API để đọc dữ liệu từ luồng IO. Với vai trò là một :term:`asynchronous iterable`, đối tượng hỗ trợ câu lệnh :keyword:`async for`.

   Không nên khởi tạo trực tiếp các đối tượng *StreamReader*; thay vào đó, hãy sử dụng :func:`open_connection` và :func:`start_server`.

   .. method:: feed_eof()

      Xác nhận EOF.

   .. method:: read(n=-1)
      :async:

      Đọc tối đa *n* byte từ luồng.

      Nếu *n* không được cung cấp hoặc được đặt thành ``-1``, hãy đọc cho đến EOF, sau đó trả về toàn bộ :class:`bytes` đã đọc. Nếu đã nhận EOF và bộ đệm nội bộ trống, hãy trả về một đối tượng ``bytes`` rỗng.

      Nếu *n* là ``0``, hãy trả về ngay một đối tượng ``bytes`` rỗng.

      Nếu *n* dương, trả về tối đa *n* ``bytes`` có sẵn ngay khi có ít nhất 1 byte trong bộ đệm nội bộ. Nếu nhận được EOF trước khi đọc bất kỳ byte nào, trả về một đối tượng ``bytes`` rỗng.

   .. method:: readline()
      :async:

      Đọc một dòng, trong đó "dòng" là một chuỗi byte kết thúc bằng ``\n``.

      Nếu nhận được EOF và không tìm thấy ``\n``, phương thức sẽ trả về dữ liệu đã đọc được một phần.

      Nếu nhận được EOF và bộ đệm nội bộ trống, trả về một đối tượng ``bytes`` rỗng.

   .. method:: readexactly(n)
      :async:

      Đọc chính xác *n* byte.

      Phát sinh :exc:`IncompleteReadError` nếu đạt đến EOF trước khi có thể đọc *n*. Sử dụng thuộc tính :attr:`IncompleteReadError.partial` để lấy dữ liệu đã đọc được một phần.

   .. method:: readuntil(separator=b'\n')
      :async:

      Đọc dữ liệu từ stream cho đến khi tìm thấy *separator*.

      Khi thành công, dữ liệu và dấu phân cách sẽ được xóa khỏi bộ đệm nội bộ (đã tiêu thụ). Dữ liệu được trả về sẽ bao gồm dấu phân cách ở cuối.

      Nếu lượng dữ liệu đã đọc vượt quá giới hạn stream được cấu hình, một
      :exc:`LimitOverrunError` exception sẽ được phát sinh và dữ liệu vẫn nằm trong bộ đệm nội bộ, nên có thể được đọc lại.

      Nếu đạt đến EOF trước khi tìm thấy đầy đủ dấu phân cách, một :exc:`IncompleteReadError` exception sẽ được phát sinh và bộ đệm nội bộ sẽ được đặt lại. Thuộc tính :attr:`IncompleteReadError.partial` có thể chứa một phần của dấu phân cách.

      *separator* cũng có thể là một tuple gồm các dấu phân cách. Trong trường hợp này, giá trị trả về sẽ là giá trị ngắn nhất có thể với bất kỳ dấu phân cách nào làm hậu tố. Đối với :exc:`LimitOverrunError`, dấu phân cách ngắn nhất có thể được xem là dấu phân cách đã khớp.

      .. versionadded:: 3.5.2

      .. versionchanged:: 3.13

         Tham số *separator* giờ đây có thể là một :class:`tuple` gồm các dấu phân cách.

   .. method:: at_eof()

      Trả về ``True`` nếu bộ đệm trống và :meth:`feed_eof` đã được gọi.


StreamWriter
============

.. class:: StreamWriter

   Đại diện cho một đối tượng writer cung cấp các API để ghi dữ liệu vào luồng IO.

   Không nên khởi tạo trực tiếp các đối tượng *StreamWriter*; thay vào đó, hãy sử dụng :func:`open_connection` và :func:`start_server`.

   .. method:: write(data)

      Phương thức này cố gắng ghi *data* vào socket bên dưới ngay lập tức. Nếu không thành công, dữ liệu sẽ được xếp vào bộ đệm ghi nội bộ cho đến khi có thể được gửi đi.

      Bộ đệm *data* phải là một đối tượng bytes, bytearray hoặc memoryview một chiều liên tục theo C (C-contiguous).

      Nên sử dụng phương thức này cùng với ``drain()`` method::

         stream.write(data)
         await stream.drain()


   .. method:: writelines(data)

      Phương thức này ghi một danh sách (hoặc bất kỳ iterable nào) gồm các byte vào socket bên dưới ngay lập tức. Nếu không thành công, dữ liệu sẽ được xếp vào bộ đệm ghi nội bộ cho đến khi có thể được gửi đi.

      Nên sử dụng phương thức này cùng với ``drain()`` method::

         stream.writelines(lines)
         await stream.drain()

   .. method:: close()

      Phương thức này đóng stream và socket bên dưới.

      Nên sử dụng phương thức này, dù không bắt buộc, cùng với phương thức ``wait_closed()``::

         stream.close()
         await stream.wait_closed()

   .. method:: can_write_eof()

      Trả về ``True`` nếu transport bên dưới hỗ trợ phương thức :meth:`write_eof`, nếu không thì trả về ``False``.

   .. method:: write_eof()

      Đóng đầu ghi của stream sau khi dữ liệu ghi được đệm đã được flush.

   .. attribute:: transport

      Trả về asyncio transport bên dưới.

   .. method:: get_extra_info(name, default=None)

      Truy cập thông tin transport tùy chọn; xem
      :meth:`BaseTransport.get_extra_info` để biết thêm chi tiết.

   .. method:: drain()
      :async:

      Chờ cho đến khi thích hợp để tiếp tục ghi vào stream. Ví dụ::

          writer.write(data)
          await writer.drain()

      Đây là một phương thức điều khiển luồng dữ liệu tương tác với bộ đệm ghi IO bên dưới. Khi kích thước bộ đệm đạt đến ngưỡng cao, *drain()* sẽ chặn cho đến khi kích thước bộ đệm giảm xuống ngưỡng thấp và có thể tiếp tục ghi. Khi không có gì cần chờ, :meth:`drain` sẽ trả về ngay lập tức.

      .. note::

         Khi bộ đệm ghi thấp hơn ngưỡng cao,
         :meth:`drain` sẽ trả về ngay lập tức mà không nhường quyền cho event loop. Do đó, mã liên tục gọi ``write()`` rồi đến ``await drain()`` có thể ngăn các task khác chạy. Để tránh hành vi chặn, hãy chủ động nhường quyền cho event loop bằng ``await asyncio.sleep(0)`` (xem :func:`asyncio.sleep`).

   .. method:: start_tls(sslcontext, *, server_hostname=None, \
                         ssl_handshake_timeout=None, ssl_shutdown_timeout=None)
      :async:

      Nâng cấp một kết nối hiện có dựa trên stream lên TLS.

      Tham số:

      * *sslcontext*: một instance đã được cấu hình của :class:`~ssl.SSLContext`.

      * *server_hostname*: đặt hoặc ghi đè tên máy chủ mà chứng chỉ của máy chủ đích sẽ được đối chiếu.

      * *ssl_handshake_timeout* là thời gian tính bằng giây chờ quá trình bắt tay TLS hoàn tất trước khi hủy kết nối. ``60.0`` giây nếu ``None`` (mặc định).

      * *ssl_shutdown_timeout* là thời gian tính bằng giây chờ quá trình tắt SSL hoàn tất trước khi hủy kết nối. ``30.0`` giây nếu ``None`` (mặc định).

      .. versionadded:: 3.11

      .. versionchanged:: 3.12
         Đã thêm tham số *ssl_shutdown_timeout*.

      .. versionchanged:: 3.14.8
         Ném ``ValueError`` nếu ``sslcontext.check_hostname`` là ``True`` và ``server_hostname`` không được cung cấp.


   .. method:: is_closing()

      Trả về ``True`` nếu stream đã đóng hoặc đang trong quá trình đóng.

      .. versionadded:: 3.7

   .. method:: wait_closed()
      :async:

      Chờ cho đến khi stream được đóng.

      Nên được gọi sau :meth:`close` để chờ cho đến khi kết nối bên dưới được đóng, đảm bảo mọi dữ liệu đã được flush trước khi thoát chương trình, chẳng hạn.

      .. versionadded:: 3.7


.. _`Examples`:

Ví dụ
=====

.. _asyncio-tcp-echo-client-streams:

Máy khách echo TCP sử dụng streams
----------------------------------

Máy khách echo TCP sử dụng hàm :func:`asyncio.open_connection`::

    import asyncio

    async def tcp_echo_client(message):
        reader, writer = await asyncio.open_connection(
            '127.0.0.1', 8888)

        print(f'Send: {message!r}')
        writer.write(message.encode())
        await writer.drain()

        data = await reader.read(100)
        print(f'Received: {data.decode()!r}')

        print('Close the connection')
        writer.close()
        await writer.wait_closed()

    asyncio.run(tcp_echo_client('Hello World!'))


.. seealso::

   Ví dụ :ref:`giao thức máy khách echo TCP <asyncio_example_tcp_echo_client_protocol>` sử dụng phương thức cấp thấp :meth:`loop.create_connection`.


.. _asyncio-tcp-echo-server-streams:

Máy chủ echo TCP sử dụng streams
--------------------------------

Máy chủ echo TCP sử dụng hàm :func:`asyncio.start_server`::

    import asyncio

    async def handle_echo(reader, writer):
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')

        print(f"Received {message!r} from {addr!r}")

        print(f"Send: {message!r}")
        writer.write(data)
        await writer.drain()

        print("Close the connection")
        writer.close()
        await writer.wait_closed()

    async def main():
        server = await asyncio.start_server(
            handle_echo, '127.0.0.1', 8888)

        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        print(f'Serving on {addrs}')

        async with server:
            await server.serve_forever()

    asyncio.run(main())


.. seealso::

   Ví dụ :ref:`giao thức máy chủ echo TCP <asyncio_example_tcp_echo_server_protocol>` sử dụng phương thức :meth:`loop.create_server`.


Lấy các header HTTP
-------------------

Ví dụ đơn giản truy vấn các header HTTP của URL được truyền trên dòng lệnh::

    import asyncio
    import urllib.parse
    import sys

    async def print_http_headers(url):
        url = urllib.parse.urlsplit(url)
        if url.scheme == 'https':
            reader, writer = await asyncio.open_connection(
                url.hostname, 443, ssl=True)
        else:
            reader, writer = await asyncio.open_connection(
                url.hostname, 80)

        query = (
            f"HEAD {url.path or '/'} HTTP/1.0\r\n"
            f"Host: {url.hostname}\r\n"
            f"\r\n"
        )

        writer.write(query.encode('latin-1'))
        while True:
            line = await reader.readline()
            if not line:
                break

            line = line.decode('latin1').rstrip()
            if line:
                print(f'HTTP header> {line}')

        # Bỏ qua body, đóng socket
        writer.close()
        await writer.wait_closed()

    url = sys.argv[1]
    asyncio.run(print_http_headers(url))


Cách sử dụng::

    python example.py http://example.com/path/page.html

hoặc với HTTPS::

    python example.py https://example.com/path/page.html


.. _asyncio_example_create_connection-streams:

Đăng ký một socket đang mở để chờ dữ liệu bằng streams
------------------------------------------------------

Coroutine chờ cho đến khi một socket nhận dữ liệu bằng
hàm :func:`open_connection`::

    import asyncio
    import socket

    async def wait_for_data():
        # Lấy tham chiếu đến event loop hiện tại vì
        # chúng ta muốn truy cập các API cấp thấp.
        loop = asyncio.get_running_loop()

        # Tạo một cặp socket được kết nối với nhau.
        rsock, wsock = socket.socketpair()

        # Đăng ký socket đang mở để chờ dữ liệu.
        reader, writer = await asyncio.open_connection(sock=rsock)

        # Mô phỏng việc nhận dữ liệu từ mạng
        loop.call_soon(wsock.send, 'abc'.encode())

        # Chờ dữ liệu
        data = await reader.read(100)

        # Đã nhận dữ liệu, hoàn tất: đóng socket
        print("Received:", data.decode())
        writer.close()
        await writer.wait_closed()

        # Đóng socket thứ hai
        wsock.close()

    asyncio.run(wait_for_data())

.. seealso::

   Ví dụ :ref:`đăng ký socket đang mở để chờ dữ liệu bằng một protocol <asyncio_example_create_connection>` sử dụng protocol cấp thấp và phương thức :meth:`loop.create_connection`.

   Ví dụ :ref:`theo dõi một file descriptor để phát hiện các sự kiện đọc <asyncio_example_watch_fd>` sử dụng cấp thấp
   :meth:`loop.add_reader` là phương thức để theo dõi một file descriptor.
