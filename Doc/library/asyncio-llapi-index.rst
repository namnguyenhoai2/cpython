.. currentmodule:: asyncio


====================
Chỉ mục API cấp thấp
====================

Trang này liệt kê tất cả API asyncio cấp thấp.


Lấy Event Loop
==============

.. list-table::
    :widths: 50 50
    :class: full-width-table

    * - :func:`asyncio.get_running_loop`
      - Hàm **được khuyến nghị** để lấy event loop đang chạy.

    * - :func:`asyncio.get_event_loop`
      - Lấy một thực thể event loop (đang chạy hoặc hiện tại thông qua policy hiện tại).

    * - :func:`asyncio.set_event_loop`
      - Đặt event loop làm event loop hiện tại thông qua policy hiện tại.

    * - :func:`asyncio.new_event_loop`
      - Tạo một event loop mới.


.. rubric:: Ví dụ

* :ref:`Sử dụng asyncio.get_running_loop() <asyncio_example_future>`.


Các phương thức của Event Loop
==============================

Xem thêm phần tài liệu chính về
:ref:`asyncio-event-loop-methods`.

.. rubric:: Vòng đời
.. list-table::
    :widths: 50 50
    :class: full-width-table

    * - :meth:`loop.run_until_complete`
      - Chạy một Future/Task/awaitable cho đến khi hoàn tất.

    * - :meth:`loop.run_forever`
      - Chạy event loop vô hạn.

    * - :meth:`loop.stop`
      - Dừng vòng lặp sự kiện.

    * - :meth:`loop.close`
      - Đóng vòng lặp sự kiện.

    * - :meth:`loop.is_running`
      - Trả về ``True`` nếu vòng lặp sự kiện đang chạy.

    * - :meth:`loop.is_closed`
      - Trả về ``True`` nếu vòng lặp sự kiện đã đóng.

    * - ``await`` :meth:`loop.shutdown_asyncgens`
      - Đóng các trình tạo bất đồng bộ.


.. rubric:: Gỡ lỗi
.. list-table::
    :widths: 50 50
    :class: full-width-table

    * - :meth:`loop.set_debug`
      - Bật hoặc tắt chế độ gỡ lỗi.

    * - :meth:`loop.get_debug`
      - Lấy chế độ debug hiện tại.


.. rubric:: Lập lịch callback
.. list-table::
    :widths: 50 50
    :class: full-width-table

    * - :meth:`loop.call_soon`
      - Gọi callback sớm.

    * - :meth:`loop.call_soon_threadsafe`
      - Một biến thể an toàn luồng của :meth:`loop.call_soon`.

    * - :meth:`loop.call_later`
      - Gọi callback *sau* khoảng thời gian đã cho.

    * - :meth:`loop.call_at`
      - Gọi callback *vào* thời điểm đã cho.


.. rubric:: Thread/Interpreter/Process Pool
.. list-table::
    :widths: 50 50
    :class: full-width-table

    * - ``await`` :meth:`loop.run_in_executor`
      - Chạy một hàm sử dụng CPU-bound hoặc một hàm blocking khác trong một executor :mod:`concurrent.futures`.

    * - :meth:`loop.set_default_executor`
      - Đặt executor mặc định cho :meth:`loop.run_in_executor`.


.. rubric:: Tasks và Futures
.. list-table::
    :widths: 50 50
    :class: full-width-table

    * - :meth:`loop.create_future`
      - Tạo một đối tượng :class:`Future`.

    * - :meth:`loop.create_task`
      - Lên lịch coroutine dưới dạng :class:`Task`.

    * - :meth:`loop.set_task_factory`
      - Đặt factory được :meth:`loop.create_task` sử dụng để tạo :class:`Tasks <Task>`.

    * - :meth:`loop.get_task_factory`
      - Lấy factory mà :meth:`loop.create_task` sử dụng để tạo :class:`Tasks <Task>`.


.. rubric:: DNS
.. list-table::
    :widths: 50 50
    :class: full-width-table

    * - ``await`` :meth:`loop.getaddrinfo`
      - Phiên bản bất đồng bộ của :meth:`socket.getaddrinfo`.

    * - ``await`` :meth:`loop.getnameinfo`
      - Phiên bản bất đồng bộ của :meth:`socket.getnameinfo`.


.. rubric:: Mạng và IPC
.. list-table::
    :widths: 50 50
    :class: full-width-table

    * - ``await`` :meth:`loop.create_connection`
      - Mở kết nối TCP.

    * - ``await`` :meth:`loop.create_server`
      - Tạo máy chủ TCP.

    * - ``await`` :meth:`loop.create_unix_connection`
      - Mở kết nối socket Unix.

    * - ``await`` :meth:`loop.create_unix_server`
      - Tạo một máy chủ socket Unix.

    * - ``await`` :meth:`loop.connect_accepted_socket`
      - Bọc một :class:`~socket.socket` vào một cặp ``(transport, protocol)``.

    * - ``await`` :meth:`loop.create_datagram_endpoint`
      - Mở một kết nối datagram (UDP).

    * - ``await`` :meth:`loop.sendfile`
      - Gửi một tệp qua transport.

    * - ``await`` :meth:`loop.start_tls`
      - Nâng cấp một kết nối hiện có lên TLS.

    * - ``await`` :meth:`loop.connect_read_pipe`
      - Bọc đầu đọc của một pipe vào một cặp ``(transport, protocol)``.

    * - ``await`` :meth:`loop.connect_write_pipe`
      - Bọc đầu ghi của một pipe vào một cặp ``(transport, protocol)``.


.. rubric:: Socket
.. list-table::
    :widths: 50 50
    :class: full-width-table

    * - ``await`` :meth:`loop.sock_recv`
      - Nhận dữ liệu từ :class:`~socket.socket`.

    * - ``await`` :meth:`loop.sock_recv_into`
      - Nhận dữ liệu từ :class:`~socket.socket` vào một buffer.

    * - ``await`` :meth:`loop.sock_recvfrom`
      - Nhận một datagram từ :class:`~socket.socket`.

    * - ``await`` :meth:`loop.sock_recvfrom_into`
      - Nhận một datagram từ :class:`~socket.socket` vào một buffer.

    * - ``await`` :meth:`loop.sock_sendall`
      - Gửi dữ liệu đến :class:`~socket.socket`.

    * - ``await`` :meth:`loop.sock_sendto`
      - Gửi một datagram qua :class:`~socket.socket` đến địa chỉ được cung cấp.

    * - ``await`` :meth:`loop.sock_connect`
      - Kết nối :class:`~socket.socket`.

    * - ``await`` :meth:`loop.sock_accept`
      - Chấp nhận một kết nối :class:`~socket.socket`.

    * - ``await`` :meth:`loop.sock_sendfile`
      - Gửi một tệp qua :class:`~socket.socket`.

    * - :meth:`loop.add_reader`
      - Bắt đầu theo dõi một file descriptor để biết khi có thể đọc.

    * - :meth:`loop.remove_reader`
      - Dừng theo dõi một file descriptor để biết khi có thể đọc.

    * - :meth:`loop.add_writer`
      - Bắt đầu theo dõi một file descriptor để biết khi có thể ghi.

    * - :meth:`loop.remove_writer`
      - Dừng theo dõi một file descriptor để biết khi có thể ghi.


.. rubric:: Tín hiệu Unix
.. list-table::
    :widths: 50 50
    :class: full-width-table

    * - :meth:`loop.add_signal_handler`
      - Thêm một handler cho :mod:`signal`.

    * - :meth:`loop.remove_signal_handler`
      - Xóa một handler cho :mod:`signal`.


.. rubric:: Tiến trình con
.. list-table::
    :widths: 50 50
    :class: full-width-table

    * - :meth:`loop.subprocess_exec`
      - Khởi chạy một tiến trình con.

    * - :meth:`loop.subprocess_shell`
      - Khởi chạy một tiến trình con từ một lệnh shell.


.. rubric:: Xử lý lỗi
.. list-table::
    :widths: 50 50
    :class: full-width-table

    * - :meth:`loop.call_exception_handler`
      - Gọi trình xử lý ngoại lệ.

    * - :meth:`loop.set_exception_handler`
      - Thiết lập trình xử lý ngoại lệ mới.

    * - :meth:`loop.get_exception_handler`
      - Lấy trình xử lý ngoại lệ hiện tại.

    * - :meth:`loop.default_exception_handler`
      - Triển khai trình xử lý ngoại lệ mặc định.


.. rubric:: Ví dụ

* :ref:`Using asyncio.new_event_loop() and loop.run_forever() <asyncio_example_lowlevel_helloworld>`.

* :ref:`Using loop.call_later() <asyncio_example_call_later>`.

* Sử dụng ``loop.create_connection()`` để triển khai
  :ref:`một echo-client <asyncio_example_tcp_echo_client_protocol>`.

* Sử dụng ``loop.create_connection()`` để
  :ref:`kết nối một socket <asyncio_example_create_connection>`.

* :ref:`Sử dụng add_reader() để theo dõi một FD cho các sự kiện đọc <asyncio_example_watch_fd>`.

* :ref:`Sử dụng loop.add_signal_handler() <asyncio_example_unix_signals>`.

* :ref:`Sử dụng loop.subprocess_exec() <asyncio_example_subprocess_proto>`.


Các transport
=============

Tất cả transport đều triển khai các phương thức sau:

.. list-table::
    :widths: 50 50
    :class: full-width-table

    * - :meth:`transport.close() <BaseTransport.close>`
      - Đóng transport.

    * - :meth:`transport.is_closing() <BaseTransport.is_closing>`
      - Trả về ``True`` nếu transport đang đóng hoặc đã đóng.

    * - :meth:`transport.get_extra_info() <BaseTransport.get_extra_info>`
      - Yêu cầu thông tin về transport.

    * - :meth:`transport.set_protocol() <BaseTransport.set_protocol>`
      - Thiết lập protocol mới.

    * - :meth:`transport.get_protocol() <BaseTransport.get_protocol>`
      - Trả về protocol hiện tại.


Các transport có thể nhận dữ liệu (kết nối TCP và Unix, pipe, v.v.). Được trả về từ các phương thức như
:meth:`loop.create_connection`, :meth:`loop.create_unix_connection`,
:meth:`loop.connect_read_pipe`, v.v.:

.. rubric:: Đọc Transports
.. list-table::
    :widths: 50 50
    :class: full-width-table

    * - :meth:`transport.is_reading() <ReadTransport.is_reading>`
      - Trả về ``True`` nếu transport đang nhận dữ liệu.

    * - :meth:`transport.pause_reading() <ReadTransport.pause_reading>`
      - Tạm dừng việc nhận dữ liệu.

    * - :meth:`transport.resume_reading() <ReadTransport.resume_reading>`
      - Tiếp tục việc nhận dữ liệu.


Các transport có thể gửi dữ liệu (kết nối TCP và Unix, pipe, v.v.). Được trả về từ các phương thức như
:meth:`loop.create_connection`, :meth:`loop.create_unix_connection`,
:meth:`loop.connect_write_pipe`, v.v.:

.. rubric:: Ghi vào Transports
.. list-table::
    :widths: 50 50
    :class: full-width-table

    * - :meth:`transport.write() <WriteTransport.write>`
      - Ghi dữ liệu vào transport.

    * - :meth:`transport.writelines() <WriteTransport.writelines>`
      - Ghi các buffer vào transport.

    * - :meth:`transport.can_write_eof() <WriteTransport.can_write_eof>`
      - Trả về :const:`True` nếu transport hỗ trợ gửi EOF.

    * - :meth:`transport.write_eof() <WriteTransport.write_eof>`
      - Đóng và gửi EOF sau khi flush dữ liệu trong buffer.

    * - :meth:`transport.abort() <WriteTransport.abort>`
      - Đóng transport ngay lập tức.

    * - :meth:`transport.get_write_buffer_size()
        <WriteTransport.get_write_buffer_size>`
      - Trả về kích thước hiện tại của bộ đệm đầu ra.

    * - :meth:`transport.get_write_buffer_limits()
        <WriteTransport.get_write_buffer_limits>`
      - Trả về các ngưỡng cao và thấp để kiểm soát luồng ghi.

    * - :meth:`transport.set_write_buffer_limits()
        <WriteTransport.set_write_buffer_limits>`
      - Đặt các ngưỡng cao và thấp mới để kiểm soát luồng ghi.


Các transport được trả về bởi :meth:`loop.create_datagram_endpoint`:

.. rubric:: Transport datagram
.. list-table::
    :widths: 50 50
    :class: full-width-table

    * - :meth:`transport.sendto() <DatagramTransport.sendto>`
      - Gửi dữ liệu đến peer từ xa.

    * - :meth:`transport.abort() <DatagramTransport.abort>`
      - Đóng transport ngay lập tức.


Lớp trừu tượng transport cấp thấp trên các subprocess. Được trả về bởi :meth:`loop.subprocess_exec` và
:meth:`loop.subprocess_shell`:

.. rubric:: Các transport của subprocess
.. list-table::
    :widths: 50 50
    :class: full-width-table

    * - :meth:`transport.get_pid() <SubprocessTransport.get_pid>`
      - Trả về process id của subprocess.

    * - :meth:`transport.get_pipe_transport()
        <SubprocessTransport.get_pipe_transport>`
      - Trả về transport cho pipe giao tiếp được yêu cầu (*stdin*, *stdout*, hoặc *stderr*).

    * - :meth:`transport.get_returncode() <SubprocessTransport.get_returncode>`
      - Trả về mã return của subprocess.

    * - :meth:`transport.kill() <SubprocessTransport.kill>`
      - Kill subprocess.

    * - :meth:`transport.send_signal() <SubprocessTransport.send_signal>`
      - Gửi signal đến subprocess.

    * - :meth:`transport.terminate() <SubprocessTransport.terminate>`
      - Dừng subprocess.

    * - :meth:`transport.close() <SubprocessTransport.close>`
      - Dừng subprocess và đóng tất cả các pipe.


Protocols
=========

Các lớp Protocol có thể triển khai những **phương thức callback** sau:

.. list-table::
    :widths: 50 50
    :class: full-width-table

    * - ``callback`` :meth:`connection_made() <BaseProtocol.connection_made>`
      - Được gọi khi một kết nối được thiết lập.

    * - ``callback`` :meth:`connection_lost() <BaseProtocol.connection_lost>`
      - Được gọi khi kết nối bị mất hoặc bị đóng.

    * - ``callback`` :meth:`pause_writing() <BaseProtocol.pause_writing>`
      - Được gọi khi bộ đệm của transport vượt quá ngưỡng high water mark.

    * - ``callback`` :meth:`resume_writing() <BaseProtocol.resume_writing>`
      - Được gọi khi bộ đệm của transport giảm xuống dưới ngưỡng thấp.


.. rubric:: Các Protocol Streaming (TCP, Unix Sockets, Pipes)
.. list-table::
    :widths: 50 50
    :class: full-width-table

    * - ``callback`` :meth:`data_received() <Protocol.data_received>`
      - Được gọi khi nhận được một phần dữ liệu.

    * - ``callback`` :meth:`eof_received() <Protocol.eof_received>`
      - Được gọi khi nhận được EOF.


.. rubric:: Các Protocol Streaming có bộ đệm
.. list-table::
    :widths: 50 50
    :class: full-width-table

    * - ``callback`` :meth:`get_buffer() <BufferedProtocol.get_buffer>`
      - Được gọi để cấp phát một bộ đệm nhận mới.

    * - ``callback`` :meth:`buffer_updated() <BufferedProtocol.buffer_updated>`
      - Được gọi khi bộ đệm được cập nhật bằng dữ liệu đã nhận.

    * - ``callback`` :meth:`eof_received() <BufferedProtocol.eof_received>`
      - Được gọi khi nhận được EOF.


.. rubric:: Các giao thức Datagram
.. list-table::
    :widths: 50 50
    :class: full-width-table

    * - ``callback`` :meth:`datagram_received()
        <DatagramProtocol.datagram_received>`
      - Được gọi khi nhận được một datagram.

    * - ``callback`` :meth:`error_received() <DatagramProtocol.error_received>`
      - Được gọi khi một thao tác gửi hoặc nhận trước đó phát sinh một
        :class:`OSError`.


.. rubric:: Các giao thức Subprocess
.. list-table::
    :widths: 50 50
    :class: full-width-table

    * - ``callback`` :meth:`~SubprocessProtocol.pipe_data_received`
      - Được gọi khi tiến trình con ghi dữ liệu vào pipe *stdout* hoặc *stderr* của tiến trình đó.

    * - ``callback`` :meth:`~SubprocessProtocol.pipe_connection_lost`
      - Được gọi khi một trong các pipe giao tiếp với tiến trình con bị đóng.

    * - ``callback`` :meth:`process_exited()
        <SubprocessProtocol.process_exited>`
      - Được gọi khi tiến trình con đã thoát. Nó có thể được gọi trước
        :meth:`~SubprocessProtocol.pipe_data_received` và
        :meth:`~SubprocessProtocol.pipe_connection_lost` các phương thức.


Các Policy của Event Loop
=========================

Policies là một cơ chế cấp thấp để thay đổi hành vi của các hàm như :func:`asyncio.get_event_loop`. Xem thêm :ref:`phần policies chính <asyncio-policies>` để biết thêm chi tiết.


.. rubric:: Truy cập Policies
.. list-table::
    :widths: 50 50
    :class: full-width-table

    * - :meth:`asyncio.get_event_loop_policy`
      - Trả về policy hiện tại trên toàn bộ tiến trình.

    * - :meth:`asyncio.set_event_loop_policy`
      - Đặt một policy mới áp dụng trên toàn bộ tiến trình.

    * - :class:`AbstractEventLoopPolicy`
      - Lớp cơ sở cho các đối tượng policy.
