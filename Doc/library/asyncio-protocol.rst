.. currentmodule:: asyncio


.. _asyncio-transports-protocols:


=====================
Transport và Protocol
=====================

.. rubric:: Lời nói đầu

Transport và Protocol được các API event loop **cấp thấp** như :meth:`loop.create_connection` sử dụng. Chúng sử dụng phong cách lập trình dựa trên callback và cho phép triển khai hiệu năng cao các protocol mạng hoặc IPC (ví dụ: HTTP).

Về cơ bản, transport và protocol chỉ nên được sử dụng trong các thư viện và framework, không nên được sử dụng trong các ứng dụng asyncio cấp cao.

Trang tài liệu này bao quát cả `Transports`_ và `Protocols`_.

.. rubric:: Giới thiệu

Ở cấp độ cao nhất, transport chịu trách nhiệm về *cách* các byte được truyền, trong khi protocol xác định *những* byte nào sẽ được truyền (và ở một mức độ nào đó là thời điểm truyền).

Một cách diễn đạt khác cho cùng một điều: transport là một abstraction cho socket (hoặc endpoint I/O tương tự), còn protocol là một abstraction cho application, xét từ góc nhìn của transport.

Một góc nhìn khác là các interface của transport và protocol khi kết hợp với nhau sẽ định nghĩa một interface trừu tượng để sử dụng network I/O và interprocess I/O.

Luôn có mối quan hệ 1:1 giữa các đối tượng transport và protocol: protocol gọi các phương thức của transport để gửi dữ liệu, còn transport gọi các phương thức của protocol để truyền cho protocol dữ liệu đã nhận.

Hầu hết các phương thức của event loop hướng kết nối (chẳng hạn như :meth:`loop.create_connection`) thường nhận một đối số *protocol_factory* dùng để tạo một đối tượng *Protocol* cho một kết nối được chấp nhận, được biểu diễn bằng một đối tượng *Transport*. Những phương thức này thường trả về một tuple gồm ``(transport, protocol)``.

.. rubric:: Nội dung

Trang tài liệu này chứa các phần sau:

* Phần `Transports`_ trình bày về asyncio :class:`BaseTransport`,
  :class:`ReadTransport`, :class:`WriteTransport`, :class:`Transport`,
  :class:`DatagramTransport`, và các lớp :class:`SubprocessTransport`.

* Phần `Protocols`_ trình bày về asyncio :class:`BaseProtocol`,
  :class:`Protocol`, :class:`BufferedProtocol`,
  :class:`DatagramProtocol`, và các lớp :class:`SubprocessProtocol`.

* Phần `Examples`_ minh họa cách làm việc với transports, protocols và các API event loop cấp thấp.


.. _asyncio-transport:

.. _`Transports`:

Transports
==========

**Mã nguồn:** :source:`Lib/asyncio/transports.py`

----------------------------------------------------

Transports là các lớp do :mod:`asyncio` cung cấp nhằm trừu tượng hóa nhiều loại kênh giao tiếp.

Các đối tượng transport luôn được khởi tạo bởi một
:ref:`vòng lặp sự kiện asyncio <asyncio-event-loop>`.

asyncio triển khai transport cho TCP, UDP, SSL và các pipe của subprocess. Các phương thức có sẵn trên một transport phụ thuộc vào loại transport đó.

Các lớp transport :ref:`không an toàn khi sử dụng trong thread <asyncio-multithreading>`.


Phân cấp Transports
-------------------

.. class:: BaseTransport

   Lớp cơ sở cho tất cả transport. Chứa các phương thức mà mọi transport của asyncio đều dùng chung.

.. class:: WriteTransport(BaseTransport)

   Một transport cơ sở cho các kết nối chỉ ghi.

   Các instance của lớp *WriteTransport* được trả về từ phương thức event loop :meth:`loop.connect_write_pipe` và cũng được sử dụng bởi các phương thức liên quan đến subprocess như
   :meth:`loop.subprocess_exec`.

.. class:: ReadTransport(BaseTransport)

   Một transport cơ sở dành cho các kết nối chỉ đọc.

   Các instance của lớp *ReadTransport* được trả về từ phương thức event loop :meth:`loop.connect_read_pipe` và cũng được sử dụng bởi các phương thức liên quan đến subprocess như
   :meth:`loop.subprocess_exec`.

.. class:: Transport(WriteTransport, ReadTransport)

   Interface đại diện cho một transport hai chiều, chẳng hạn như kết nối TCP.

   Người dùng không khởi tạo transport trực tiếp; họ gọi một hàm tiện ích, truyền vào đó một protocol factory cùng các thông tin khác cần thiết để tạo transport và protocol.

   Các instance của lớp *Transport* được trả về hoặc được sử dụng bởi các phương thức event loop như :meth:`loop.create_connection`,
   :meth:`loop.create_unix_connection`,
   :meth:`loop.create_server`, :meth:`loop.sendfile`, v.v.


.. class:: DatagramTransport(BaseTransport)

   Một transport cho các kết nối datagram (UDP).

   Các instance của lớp *DatagramTransport* được trả về từ phương thức vòng lặp sự kiện :meth:`loop.create_datagram_endpoint`.


.. class:: SubprocessTransport(BaseTransport)

   Một abstraction dùng để biểu diễn kết nối giữa một tiến trình OS cha và tiến trình con của nó.

   Các instance của lớp *SubprocessTransport* được trả về từ các phương thức vòng lặp sự kiện :meth:`loop.subprocess_shell` và
   :meth:`loop.subprocess_exec`.


Transport cơ sở
---------------

.. method:: BaseTransport.close()

   Đóng transport.

   Nếu transport có bộ đệm cho dữ liệu gửi đi, dữ liệu trong bộ đệm sẽ được flush một cách bất đồng bộ. Sẽ không nhận thêm dữ liệu nào nữa. Sau khi toàn bộ dữ liệu trong bộ đệm được flush, phương thức :meth:`protocol.connection_lost() <BaseProtocol.connection_lost>` của protocol sẽ được gọi với
   :const:`None` làm đối số của nó. Không nên sử dụng transport sau khi đã đóng.

.. method:: BaseTransport.is_closing()

   Trả về ``True`` nếu transport đang đóng hoặc đã đóng.

.. method:: BaseTransport.get_extra_info(name, default=None)

   Trả về thông tin về transport hoặc các tài nguyên bên dưới mà nó sử dụng.

   *name* là một chuỗi biểu thị phần thông tin dành riêng cho transport cần lấy.

   *default* là giá trị cần trả về nếu không có thông tin này hoặc nếu transport không hỗ trợ truy vấn thông tin đó bằng cách triển khai event loop của bên thứ ba đã cho hoặc trên nền tảng hiện tại.

   Ví dụ, đoạn mã sau đây cố gắng lấy đối tượng socket bên dưới của transport::

      sock = transport.get_extra_info('socket')
      if sock is not None:
          print(sock.getsockopt(...))

   Các danh mục thông tin có thể được truy vấn trên một số transport:

   * socket:

     - ``'peername'``: địa chỉ từ xa mà socket được kết nối tới, kết quả của :meth:`socket.socket.getpeername` (``None`` khi có lỗi)

     - ``'socket'``: instance của :class:`socket.socket`

     - ``'sockname'``: địa chỉ của chính socket, kết quả của :meth:`socket.socket.getsockname`

   * SSL socket:

     - ``'compression'``: thuật toán nén đang được sử dụng dưới dạng chuỗi, hoặc ``None`` nếu kết nối không được nén; kết quả của :meth:`ssl.SSLSocket.compression`

     - ``'cipher'``: tuple gồm ba giá trị, chứa tên của cipher đang được sử dụng, phiên bản của giao thức SSL quy định việc sử dụng cipher đó và số lượng bit bí mật đang được sử dụng; kết quả của
       :meth:`ssl.SSLSocket.cipher`

     - ``'peercert'``: chứng chỉ ngang hàng; kết quả của
       :meth:`ssl.SSLSocket.getpeercert`

     - ``'sslcontext'``: thực thể :class:`ssl.SSLContext`

     - ``'ssl_object'``: :class:`ssl.SSLObject` hoặc
       thực thể :class:`ssl.SSLSocket`

   * pipe:

     - ``'pipe'``: đối tượng pipe

   * subprocess:

     - ``'subprocess'``: một instance của :class:`subprocess.Popen`

.. method:: BaseTransport.set_protocol(protocol)

   Thiết lập protocol mới.

   Chỉ nên chuyển đổi protocol khi cả hai protocol đều được ghi rõ là hỗ trợ việc chuyển đổi.

.. method:: BaseTransport.get_protocol()

   Trả về protocol hiện tại.


Transport chỉ đọc
-----------------

.. method:: ReadTransport.is_reading()

   Trả về ``True`` nếu transport đang nhận dữ liệu mới.

   .. versionadded:: 3.7

.. method:: ReadTransport.pause_reading()

   Tạm dừng đầu nhận của transport. Sẽ không có dữ liệu nào được truyền đến phương thức :meth:`protocol.data_received() <Protocol.data_received>` của protocol cho đến khi :meth:`resume_reading` được gọi.

   .. versionchanged:: 3.7
      Phương thức này có tính idempotent, tức là có thể được gọi khi transport đã tạm dừng hoặc đóng.

.. method:: ReadTransport.resume_reading()

   Tiếp tục hoạt động ở đầu nhận. Phương thức của protocol
   :meth:`protocol.data_received() <Protocol.data_received>` sẽ lại được gọi nếu có dữ liệu để đọc.

   .. versionchanged:: 3.7
      Phương thức này có tính idempotent, tức là có thể được gọi khi transport đang đọc.


Transport chỉ ghi
-----------------

.. method:: WriteTransport.abort()

   Đóng transport ngay lập tức mà không chờ các thao tác đang chờ hoàn tất. Dữ liệu được đệm sẽ bị mất. Sẽ không nhận thêm dữ liệu nào. Cuối cùng, phương thức :meth:`protocol.connection_lost() <BaseProtocol.connection_lost>` của protocol sẽ được gọi với :const:`None` làm đối số.

.. method:: WriteTransport.can_write_eof()

   Trả về :const:`True` nếu transport hỗ trợ
   :meth:`~WriteTransport.write_eof`, :const:`False` nếu không.

.. method:: WriteTransport.get_write_buffer_size()

   Trả về kích thước hiện tại của bộ đệm đầu ra được transport sử dụng.

.. method:: WriteTransport.get_write_buffer_limits()

   Lấy các ngưỡng *cao* và *thấp* để điều khiển luồng ghi. Trả về một tuple ``(low, high)`` trong đó *thấp* và *cao* là số byte dương.

   Sử dụng :meth:`set_write_buffer_limits` để thiết lập các giới hạn.

   .. versionadded:: 3.4.2

.. method:: WriteTransport.set_write_buffer_limits(high=None, low=None)

   Thiết lập các ngưỡng *cao* và *thấp* để điều khiển luồng ghi.

   Hai giá trị này (được đo bằng số byte) kiểm soát thời điểm các phương thức của protocol
   :meth:`protocol.pause_writing() <BaseProtocol.pause_writing>` và :meth:`protocol.resume_writing() <BaseProtocol.resume_writing>` được gọi. Nếu được chỉ định, ngưỡng thấp phải nhỏ hơn hoặc bằng ngưỡng cao. Cả *cao* và *thấp* đều không được là số âm.

   :meth:`~BaseProtocol.pause_writing` được gọi khi kích thước bộ đệm lớn hơn hoặc bằng giá trị *high*. Nếu việc ghi đã bị tạm dừng, :meth:`~BaseProtocol.resume_writing` được gọi khi kích thước bộ đệm nhỏ hơn hoặc bằng giá trị *low*.

   Các giá trị mặc định phụ thuộc vào từng implementation. Nếu chỉ cung cấp high watermark, low watermark sẽ mặc định là một giá trị phụ thuộc vào implementation và nhỏ hơn hoặc bằng high watermark. Đặt *high* thành zero cũng buộc *low* thành zero và khiến :meth:`~BaseProtocol.pause_writing` được gọi bất cứ khi nào bộ đệm trở nên không rỗng. Đặt *low* thành zero khiến
   :meth:`~BaseProtocol.resume_writing` chỉ được gọi khi bộ đệm đã rỗng. Nhìn chung, việc sử dụng zero cho một trong hai giới hạn là không tối ưu vì làm giảm cơ hội thực hiện I/O và tính toán đồng thời.

   Sử dụng :meth:`~WriteTransport.get_write_buffer_limits` để lấy các giới hạn.

.. method:: WriteTransport.write(data)

   Ghi một số byte *data* vào transport.

   Phương thức này không chặn; phương thức đệm dữ liệu và sắp xếp để dữ liệu được gửi đi một cách bất đồng bộ.

.. method:: WriteTransport.writelines(list_of_data)

   Ghi một danh sách (hoặc bất kỳ iterable nào) gồm các byte dữ liệu vào transport. Về chức năng, thao tác này tương đương với việc gọi :meth:`write` trên từng phần tử do iterable cung cấp, nhưng có thể được triển khai hiệu quả hơn.

.. method:: WriteTransport.write_eof()

   Đóng đầu ghi của transport sau khi flush toàn bộ dữ liệu đã được đệm. Dữ liệu vẫn có thể được nhận.

   Phương thức này có thể raise :exc:`NotImplementedError` nếu transport (ví dụ: SSL) không hỗ trợ các kết nối đóng một nửa.


Transport Datagram
------------------

.. method:: DatagramTransport.sendto(data, addr=None)

   Gửi các byte *data* đến peer từ xa được chỉ định bởi *addr* (một địa chỉ đích phụ thuộc vào transport). Nếu *addr* là :const:`None`, dữ liệu sẽ được gửi đến địa chỉ đích được chỉ định khi tạo transport.

   Phương thức này không block; nó đệm dữ liệu và sắp xếp để dữ liệu được gửi đi một cách bất đồng bộ.

   .. versionchanged:: 3.13
      Có thể gọi phương thức này với một đối tượng bytes rỗng để gửi một datagram có độ dài bằng không. Việc tính kích thước bộ đệm được dùng cho flow control cũng được cập nhật để tính đến header của datagram.

.. method:: DatagramTransport.abort()

   Đóng transport ngay lập tức mà không chờ các thao tác đang chờ hoàn tất. Dữ liệu đã đệm sẽ bị mất. Sẽ không nhận thêm dữ liệu nào. protocol's
   Phương thức :meth:`protocol.connection_lost() <BaseProtocol.connection_lost>` cuối cùng sẽ được gọi với :const:`None` làm đối số.


.. _asyncio-subprocess-transports:

Subprocess Transports
---------------------

.. method:: SubprocessTransport.get_pid()

   Trả về mã định danh tiến trình subprocess dưới dạng số nguyên.

.. method:: SubprocessTransport.get_pipe_transport(fd)

   Trả về transport cho pipe giao tiếp tương ứng với file descriptor số nguyên *fd*:

   * ``0``: transport dạng streaming có thể ghi của đầu vào chuẩn (*stdin*), hoặc :const:`None` nếu subprocess không được tạo bằng ``stdin=PIPE``
   * ``1``: transport dạng streaming có thể đọc của đầu ra chuẩn (*stdout*), hoặc :const:`None` nếu subprocess không được tạo bằng ``stdout=PIPE``
   * ``2``: transport dạng streaming có thể đọc của lỗi chuẩn (*stderr*), hoặc :const:`None` nếu subprocess không được tạo bằng ``stderr=PIPE``
   * fd khác: *fd*: :const:`None`

.. method:: SubprocessTransport.get_returncode()

   Trả về mã thoát của subprocess dưới dạng số nguyên hoặc :const:`None` nếu subprocess chưa kết thúc, tương tự như
   thuộc tính :attr:`subprocess.Popen.returncode`.

.. method:: SubprocessTransport.kill()

   Dừng subprocess.

   Trên các hệ thống POSIX, hàm này gửi SIGKILL đến subprocess. Trên Windows, phương thức này là bí danh của :meth:`terminate`.

   Xem thêm :meth:`subprocess.Popen.kill`.

.. method:: SubprocessTransport.send_signal(signal)

   Gửi số *signal* đến subprocess, như trong
   :meth:`subprocess.Popen.send_signal`.

.. method:: SubprocessTransport.terminate()

   Dừng subprocess.

   Trên các hệ thống POSIX, phương thức này gửi :py:const:`~signal.SIGTERM` đến subprocess. Trên Windows, hàm API của Windows :c:func:`!TerminateProcess` được gọi để dừng subprocess.

   Xem thêm :meth:`subprocess.Popen.terminate`.

.. method:: SubprocessTransport.close()

   Kết thúc subprocess bằng cách gọi phương thức :meth:`kill`.

   Nếu subprocess vẫn chưa trả về, hãy đóng các pipe stdin *stdin*, stdout *stdout* và stderr *stderr* của transport.


.. _asyncio-protocol:

.. _`Protocols`:

Protocols
=========

**Mã nguồn:** :source:`Lib/asyncio/protocols.py`

---------------------------------------------------

asyncio cung cấp một tập hợp các lớp cơ sở trừu tượng nên được dùng để triển khai các network protocol. Những lớp này được thiết kế để dùng cùng với :ref:`transports <asyncio-transport>`.

Các lớp con của những lớp protocol cơ sở trừu tượng có thể triển khai một số hoặc tất cả các phương thức. Tất cả những phương thức này đều là callback: chúng được transport gọi khi xảy ra các sự kiện nhất định, chẳng hạn như khi nhận được dữ liệu. Một phương thức protocol cơ sở phải được transport tương ứng gọi.


Các Protocol cơ sở
------------------

.. class:: BaseProtocol

   Protocol cơ sở với các phương thức được mọi protocol dùng chung.

.. class:: Protocol(BaseProtocol)

   Lớp cơ sở để triển khai các protocol dạng streaming (TCP, Unix socket, v.v.).

.. class:: BufferedProtocol(BaseProtocol)

   Lớp cơ sở để triển khai các protocol dạng streaming với quyền kiểm soát thủ công đối với bộ đệm nhận.

.. class:: DatagramProtocol(BaseProtocol)

   Lớp cơ sở để triển khai các protocol datagram (UDP).

.. class:: SubprocessProtocol(BaseProtocol)

   Lớp cơ sở để triển khai các protocol giao tiếp với tiến trình con (pipe một chiều).


Protocol cơ sở
--------------

Tất cả protocol asyncio đều có thể triển khai các callback của Base Protocol.

.. rubric:: Callback kết nối

Các callback kết nối được gọi trên tất cả protocol, chính xác một lần cho mỗi kết nối thành công. Tất cả callback protocol khác chỉ có thể được gọi giữa hai phương thức đó.

.. method:: BaseProtocol.connection_made(transport)

   Được gọi khi một kết nối được thiết lập.

   Được gọi khi một kết nối được thiết lập. Đối số *transport* là transport đại diện cho kết nối. Protocol chịu trách nhiệm lưu tham chiếu đến transport của nó.

.. method:: BaseProtocol.connection_lost(exc)

   Được gọi khi kết nối bị mất hoặc bị đóng.

   Đối số là một đối tượng exception hoặc :const:`None`. Trường hợp sau có nghĩa là đã nhận EOF thông thường, hoặc kết nối đã bị phía này của kết nối hủy bỏ hoặc đóng.


.. rubric:: Callback kiểm soát luồng

Các callback kiểm soát luồng có thể được transport gọi để tạm dừng hoặc tiếp tục hoạt động ghi do protocol thực hiện.

Xem tài liệu về phương thức :meth:`~WriteTransport.set_write_buffer_limits` để biết thêm chi tiết.

.. method:: BaseProtocol.pause_writing()

   Được gọi khi bộ đệm của transport vượt quá ngưỡng cao.

.. method:: BaseProtocol.resume_writing()

   Được gọi khi bộ đệm của transport giảm xuống dưới ngưỡng thấp.

Nếu kích thước bộ đệm bằng ngưỡng cao nhất,
:meth:`~BaseProtocol.pause_writing` sẽ không được gọi: kích thước bộ đệm phải lớn hơn hoàn toàn.

Ngược lại, :meth:`~BaseProtocol.resume_writing` được gọi khi kích thước bộ đệm bằng hoặc thấp hơn ngưỡng thấp nhất. Những điều kiện kết thúc này rất quan trọng để bảo đảm mọi thứ diễn ra như mong đợi khi một trong hai mốc bằng không.


.. _`Streaming Protocols`:

Các Streaming Protocol
----------------------

Các phương thức sự kiện, chẳng hạn như :meth:`loop.create_server`,
:meth:`loop.create_unix_server`, :meth:`loop.create_connection`,
:meth:`loop.create_unix_connection`, :meth:`loop.connect_accepted_socket`,
:meth:`loop.connect_read_pipe`, và :meth:`loop.connect_write_pipe` chấp nhận các factory trả về các streaming protocol.

.. method:: Protocol.data_received(data)

   Được gọi khi nhận được một số dữ liệu. *data* là một đối tượng bytes không rỗng chứa dữ liệu đến.

   Việc dữ liệu được đệm, chia thành các đoạn hay tập hợp lại phụ thuộc vào transport. Nhìn chung, bạn không nên dựa vào các ngữ nghĩa cụ thể mà thay vào đó hãy làm cho việc phân tích cú pháp của mình mang tính tổng quát và linh hoạt. Tuy nhiên, dữ liệu luôn được nhận theo đúng thứ tự.

   Phương thức này có thể được gọi số lần tùy ý trong khi kết nối đang mở.

   Tuy nhiên, :meth:`protocol.eof_received() <Protocol.eof_received>` được gọi nhiều nhất một lần. Sau khi ``eof_received()`` được gọi, ``data_received()`` sẽ không được gọi nữa.

.. method:: Protocol.eof_received()

   Được gọi khi đầu bên kia báo hiệu rằng nó sẽ không gửi thêm dữ liệu nào nữa (ví dụ bằng cách gọi :meth:`transport.write_eof() <WriteTransport.write_eof>`, nếu đầu bên kia cũng sử dụng asyncio).

   Phương thức này có thể trả về một giá trị false (bao gồm ``None``), trong trường hợp đó transport sẽ tự đóng. Ngược lại, nếu phương thức này trả về một giá trị true, giao thức được sử dụng sẽ quyết định có đóng transport hay không. Vì phần triển khai mặc định trả về ``None``, nên kết nối sẽ được đóng một cách ngầm định.

   Một số transport, bao gồm SSL, không hỗ trợ các kết nối đóng một nửa, trong trường hợp đó việc trả về true từ phương thức này sẽ khiến kết nối bị đóng.


Máy trạng thái:

.. code-block:: none

    start -> connection_made
        [-> data_received]*
        [-> eof_received]?
    -> connection_lost -> end


Các giao thức streaming có bộ đệm
---------------------------------

.. versionadded:: 3.7

Các Buffered Protocol có thể được sử dụng với bất kỳ phương thức event loop nào hỗ trợ `Streaming Protocols <Streaming Protocols_>`_.

Các triển khai ``BufferedProtocol`` cho phép cấp phát và kiểm soát bộ đệm nhận một cách thủ công, rõ ràng. Sau đó, event loop có thể sử dụng bộ đệm do protocol cung cấp để tránh các thao tác sao chép dữ liệu không cần thiết. Điều này có thể cải thiện hiệu suất đáng kể đối với các protocol nhận lượng dữ liệu lớn. Những triển khai protocol nâng cao có thể giảm đáng kể số lần cấp phát bộ đệm.

Các callback sau được gọi trên các instance :class:`BufferedProtocol`:

.. method:: BufferedProtocol.get_buffer(sizehint)

   Được gọi để cấp phát một bộ đệm nhận mới.

   *sizehint* là kích thước tối thiểu được khuyến nghị cho bộ đệm được trả về. Có thể trả về bộ đệm nhỏ hơn hoặc lớn hơn kích thước mà *sizehint* đề xuất. Khi được đặt thành -1, kích thước bộ đệm có thể tùy ý. Trả về bộ đệm có kích thước bằng 0 là một lỗi.

   ``get_buffer()`` phải trả về một đối tượng triển khai
   :ref:`buffer protocol <bufferobjects>`.

.. method:: BufferedProtocol.buffer_updated(nbytes)

   Được gọi khi buffer được cập nhật với dữ liệu đã nhận.

   *nbytes* là tổng số byte đã được ghi vào buffer.

.. method:: BufferedProtocol.eof_received()

   Xem tài liệu về :meth:`protocol.eof_received() <Protocol.eof_received>` method.


:meth:`~BufferedProtocol.get_buffer` có thể được gọi một số lần tùy ý trong suốt một kết nối. Tuy nhiên, :meth:`protocol.eof_received() <Protocol.eof_received>` được gọi nhiều nhất một lần và nếu được gọi, :meth:`~BufferedProtocol.get_buffer` và
:meth:`~BufferedProtocol.buffer_updated` sẽ không được gọi sau đó.

Máy trạng thái:

.. code-block:: none

    start -> connection_made
        [-> get_buffer
            [-> buffer_updated]?
        ]*
        [-> eof_received]?
    -> connection_lost -> end


Các giao thức Datagram
----------------------

Các instance của Datagram Protocol nên được tạo bởi các protocol factory được truyền vào phương thức :meth:`loop.create_datagram_endpoint`.

.. method:: DatagramProtocol.datagram_received(data, addr)

   Được gọi khi nhận một datagram. *data* là một đối tượng bytes chứa dữ liệu đến. *addr* là địa chỉ của peer gửi dữ liệu; định dạng chính xác phụ thuộc vào transport.

.. method:: DatagramProtocol.error_received(exc)

   Được gọi khi một thao tác gửi hoặc nhận trước đó phát sinh một
   :class:`OSError`. *exc* là instance :class:`OSError`.

   Phương thức này được gọi trong những điều kiện hiếm gặp, khi transport (ví dụ: UDP) phát hiện rằng một datagram không thể được chuyển đến bên nhận. Tuy nhiên, trong nhiều trường hợp, các datagram không thể chuyển đến nơi nhận sẽ bị loại bỏ một cách im lặng.

.. note::

   Trên các hệ thống BSD (macOS, FreeBSD, v.v.), flow control không được hỗ trợ cho các giao thức datagram vì không có cách đáng tin cậy để phát hiện lỗi gửi do ghi quá nhiều packet gây ra.

   Socket luôn xuất hiện ở trạng thái 'ready' và các gói tin dư thừa sẽ bị loại bỏ. Một
   :class:`OSError` với ``errno`` được đặt thành :const:`errno.ENOBUFS` có thể được phát sinh hoặc không; nếu được phát sinh, nó sẽ được báo cáo cho
   :meth:`DatagramProtocol.error_received`, nhưng nếu không thì sẽ bị bỏ qua.


.. _asyncio-subprocess-protocols:

Protocol của tiến trình con
---------------------------

Các instance Subprocess Protocol nên được tạo bởi các protocol factory được truyền vào :meth:`loop.subprocess_exec` và
các phương thức :meth:`loop.subprocess_shell`.

.. method:: SubprocessProtocol.pipe_data_received(fd, data)

   Được gọi khi tiến trình con ghi dữ liệu vào pipe stdout hoặc stderr của nó.

   *fd* là bộ mô tả tệp dạng số nguyên của pipe.

   *data* là một đối tượng bytes không rỗng chứa dữ liệu đã nhận.

.. method:: SubprocessProtocol.pipe_connection_lost(fd, exc)

   Được gọi khi một trong các pipe giao tiếp với tiến trình con bị đóng.

   *fd* là bộ mô tả tệp dạng số nguyên đã bị đóng.

.. method:: SubprocessProtocol.process_exited()

   Được gọi khi tiến trình con đã thoát.

   Nó có thể được gọi trước :meth:`~SubprocessProtocol.pipe_data_received` và
   :meth:`~SubprocessProtocol.pipe_connection_lost` các phương thức.


.. _`Examples`:

Ví dụ
=====

.. _asyncio_example_tcp_echo_server_protocol:

Máy chủ echo TCP
----------------

Tạo máy chủ echo TCP bằng phương thức :meth:`loop.create_server`, gửi lại dữ liệu đã nhận và đóng kết nối::

    import asyncio


    class EchoServerProtocol(asyncio.Protocol):
        def connection_made(self, transport):
            peername = transport.get_extra_info('peername')
            print('Connection from {}'.format(peername))
            self.transport = transport

        def data_received(self, data):
            message = data.decode()
            print('Data received: {!r}'.format(message))

            print('Send: {!r}'.format(message))
            self.transport.write(data)

            print('Close the client socket')
            self.transport.close()


    async def main():
        # Lấy tham chiếu đến event loop vì chúng ta dự định sử dụng
        # các API cấp thấp.
        loop = asyncio.get_running_loop()

        server = await loop.create_server(
            EchoServerProtocol,
            '127.0.0.1', 8888)

        async with server:
            await server.serve_forever()


    asyncio.run(main())


.. seealso::

   Ví dụ :ref:`máy chủ echo TCP sử dụng streams <asyncio-tcp-echo-server-streams>` dùng hàm :func:`asyncio.start_server` cấp cao.

.. _asyncio_example_tcp_echo_client_protocol:

Máy khách echo TCP
------------------

TCP echo client sử dụng phương thức :meth:`loop.create_connection`, gửi dữ liệu và chờ cho đến khi connection được đóng::

    import asyncio


    class EchoClientProtocol(asyncio.Protocol):
        def __init__(self, message, on_con_lost):
            self.message = message
            self.on_con_lost = on_con_lost

        def connection_made(self, transport):
            transport.write(self.message.encode())
            print('Data sent: {!r}'.format(self.message))

        def data_received(self, data):
            print('Data received: {!r}'.format(data.decode()))

        def connection_lost(self, exc):
            print('The server closed the connection')
            self.on_con_lost.set_result(True)


    async def main():
        # Lấy tham chiếu đến event loop vì chúng ta dự định sử dụng các
        # API cấp thấp.
        loop = asyncio.get_running_loop()

        on_con_lost = loop.create_future()
        message = 'Hello World!'

        transport, protocol = await loop.create_connection(
            lambda: EchoClientProtocol(message, on_con_lost),
            '127.0.0.1', 8888)

        # Chờ cho đến khi protocol báo hiệu rằng connection
        # đã bị mất rồi đóng transport.
        try:
            await on_con_lost
        finally:
            transport.close()


    asyncio.run(main())


.. seealso::

   Ví dụ :ref:`TCP echo client sử dụng streams <asyncio-tcp-echo-client-streams>` sử dụng hàm cấp cao :func:`asyncio.open_connection`.


.. _asyncio-udp-echo-server-protocol:

Máy chủ UDP Echo
----------------

Một UDP echo server, sử dụng phương thức :meth:`loop.create_datagram_endpoint`, gửi lại dữ liệu đã nhận::

    import asyncio


    class EchoServerProtocol:
        def connection_made(self, transport):
            self.transport = transport

        def datagram_received(self, data, addr):
            message = data.decode()
            print('Received %r from %s' % (message, addr))
            print('Send %r to %s' % (message, addr))
            self.transport.sendto(data, addr)


    async def main():
        print("Starting UDP server")

        # Lấy tham chiếu đến event loop vì chúng ta dự định sử dụng
        # các API cấp thấp.
        loop = asyncio.get_running_loop()

        # Một protocol instance sẽ được tạo để phục vụ tất cả
        # các yêu cầu của client.
        transport, protocol = await loop.create_datagram_endpoint(
            EchoServerProtocol,
            local_addr=('127.0.0.1', 9999))

        try:
            await asyncio.sleep(3600)  # Phục vụ trong 1 giờ.
        finally:
            transport.close()


    asyncio.run(main())


.. _asyncio-udp-echo-client-protocol:

UDP Echo Client
---------------

Một UDP echo client, sử dụng phương thức :meth:`loop.create_datagram_endpoint`, gửi dữ liệu và đóng transport khi nhận được câu trả lời::

    import asyncio


    class EchoClientProtocol:
        def __init__(self, message, on_con_lost):
            self.message = message
            self.on_con_lost = on_con_lost
            self.transport = None

        def connection_made(self, transport):
            self.transport = transport
            print('Send:', self.message)
            self.transport.sendto(self.message.encode())

        def datagram_received(self, data, addr):
            print("Received:", data.decode())

            print("Close the socket")
            self.transport.close()

        def error_received(self, exc):
            print('Error received:', exc)

        def connection_lost(self, exc):
            print("Connection closed")
            self.on_con_lost.set_result(True)


    async def main():
        # Lấy tham chiếu đến event loop vì chúng ta dự định sử dụng
        # các API cấp thấp.
        loop = asyncio.get_running_loop()

        on_con_lost = loop.create_future()
        message = "Hello World!"

        transport, protocol = await loop.create_datagram_endpoint(
            lambda: EchoClientProtocol(message, on_con_lost),
            remote_addr=('127.0.0.1', 9999))

        try:
            await on_con_lost
        finally:
            transport.close()


    asyncio.run(main())


.. _asyncio_example_create_connection:

Kết nối các socket hiện có
--------------------------

Chờ cho đến khi một socket nhận dữ liệu bằng
phương thức :meth:`loop.create_connection` với một protocol::

    import asyncio
    import socket


    class MyProtocol(asyncio.Protocol):

        def __init__(self, on_con_lost):
            self.transport = None
            self.on_con_lost = on_con_lost

        def connection_made(self, transport):
            self.transport = transport

        def data_received(self, data):
            print("Received:", data.decode())

            # Chúng ta đã hoàn tất: đóng transport;
            # connection_lost() sẽ được gọi tự động.
            self.transport.close()

        def connection_lost(self, exc):
            # Socket đã được đóng
            self.on_con_lost.set_result(True)


    async def main():
        # Lấy tham chiếu đến event loop vì chúng ta dự định sử dụng
        # các API cấp thấp.
        loop = asyncio.get_running_loop()
        on_con_lost = loop.create_future()

        # Tạo một cặp socket được kết nối
        rsock, wsock = socket.socketpair()

        # Đăng ký socket để chờ dữ liệu.
        transport, protocol = await loop.create_connection(
            lambda: MyProtocol(on_con_lost), sock=rsock)

        # Mô phỏng việc nhận dữ liệu từ mạng.
        loop.call_soon(wsock.send, 'abc'.encode())

        try:
            await protocol.on_con_lost
        finally:
            transport.close()
            wsock.close()

    asyncio.run(main())

.. seealso::

   Ví dụ :ref:`theo dõi một bộ mô tả tệp để phát hiện các sự kiện đọc <asyncio_example_watch_fd>` sử dụng API cấp thấp
   phương thức :meth:`loop.add_reader` để đăng ký một FD.

   Ví dụ :ref:`đăng ký một socket đang mở để chờ dữ liệu bằng streams <asyncio_example_create_connection-streams>` sử dụng các stream cấp cao được tạo bởi hàm :func:`open_connection` trong một coroutine.

.. _asyncio_example_subprocess_proto:

loop.subprocess_exec() and SubprocessProtocol
---------------------------------------------

Ví dụ về một subprocess protocol được dùng để lấy đầu ra của một subprocess và chờ subprocess kết thúc.

Subprocess được tạo bởi phương thức :meth:`loop.subprocess_exec`::

    import asyncio
    import sys

    class DateProtocol(asyncio.SubprocessProtocol):
        def __init__(self, exit_future):
            self.exit_future = exit_future
            self.output = bytearray()
            self.pipe_closed = False
            self.exited = False

        def pipe_connection_lost(self, fd, exc):
            self.pipe_closed = True
            self.check_for_exit()

        def pipe_data_received(self, fd, data):
            self.output.extend(data)

        def process_exited(self):
            self.exited = True
            # phương thức process_exited() có thể được gọi trước
            # phương thức pipe_connection_lost(): chờ cho đến khi cả hai phương thức đều
            # được gọi.
            self.check_for_exit()

        def check_for_exit(self):
            if self.pipe_closed and self.exited:
                self.exit_future.set_result(True)

    async def get_date():
        # Lấy tham chiếu đến event loop vì chúng ta dự định sử dụng
        # các API cấp thấp.
        loop = asyncio.get_running_loop()

        code = 'import datetime as dt; print(dt.datetime.now())'
        exit_future = asyncio.Future(loop=loop)

        # Tạo subprocess do DateProtocol điều khiển;
        # chuyển hướng đầu ra tiêu chuẩn vào một pipe.
        transport, protocol = await loop.subprocess_exec(
            lambda: DateProtocol(exit_future),
            sys.executable, '-c', code,
            stdin=None, stderr=None)

        # Chờ subprocess thoát bằng process_exited()
        # phương thức của protocol.
        await exit_future

        # Đóng pipe stdout.
        transport.close()

        # Đọc đầu ra đã được thu thập bởi
        # phương thức pipe_data_received() của protocol.
        data = bytes(protocol.output)
        return data.decode('ascii').rstrip()

    date = asyncio.run(get_date())
    print(f"Current date: {date}")

Xem thêm :ref:`ví dụ tương tự <asyncio_example_create_subprocess_exec>` được viết bằng các API cấp cao.
