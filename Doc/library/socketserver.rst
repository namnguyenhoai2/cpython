:mod:`!socketserver` --- Khung cho các máy chủ mạng
===================================================

.. module:: socketserver
   :synopsis: Khung cho các máy chủ mạng.

**Mã nguồn:** :source:`Lib/socketserver.py`

--------------

Mô-đun :mod:`!socketserver` đơn giản hóa việc viết các máy chủ mạng.

.. include:: ../includes/wasm-notavail.rst

Có bốn lớp máy chủ cụ thể cơ bản:


.. class:: TCPServer(server_address, RequestHandlerClass, bind_and_activate=True)

   Lớp này sử dụng giao thức TCP internet, cung cấp các luồng dữ liệu liên tục giữa máy khách và máy chủ. Nếu *bind_and_activate* là true, hàm khởi tạo sẽ tự động cố gắng gọi :meth:`~BaseServer.server_bind` và
   :meth:`~BaseServer.server_activate`.  Các tham số khác được truyền cho lớp cơ sở :class:`BaseServer`.


.. class:: UDPServer(server_address, RequestHandlerClass, bind_and_activate=True)

   Phần này sử dụng datagram, tức là các gói thông tin riêng biệt có thể đến không theo thứ tự hoặc bị mất trong quá trình truyền. Các tham số giống như đối với :class:`TCPServer`.


.. class:: UnixStreamServer(server_address, RequestHandlerClass, bind_and_activate=True)
           UnixDatagramServer(server_address, RequestHandlerClass, bind_and_activate=True)

   Các lớp ít được sử dụng thường xuyên hơn này tương tự như các lớp TCP và UDP, nhưng sử dụng Unix domain socket; chúng không có trên các nền tảng không phải Unix. Các tham số giống như đối với
   :class:`TCPServer`.


Bốn lớp này xử lý các yêu cầu :dfn:`đồng bộ`; mỗi yêu cầu phải hoàn tất trước khi yêu cầu tiếp theo có thể bắt đầu. Cách này không phù hợp nếu mỗi yêu cầu mất nhiều thời gian để hoàn tất, vì yêu cầu đó cần nhiều phép tính hoặc trả về nhiều dữ liệu mà client xử lý chậm. Giải pháp là tạo một process hoặc thread riêng để xử lý từng yêu cầu;
Các lớp mix-in :class:`ForkingMixIn` và :class:`ThreadingMixIn` có thể được sử dụng để hỗ trợ hành vi bất đồng bộ.

Để tạo một server, cần thực hiện một số bước. Trước tiên, bạn phải tạo một lớp xử lý yêu cầu bằng cách kế thừa lớp :class:`BaseRequestHandler` và ghi đè phương thức :meth:`~BaseRequestHandler.handle`; phương thức này sẽ xử lý các yêu cầu đến. Tiếp theo, bạn phải khởi tạo một trong các lớp server, truyền vào địa chỉ của server và lớp xử lý yêu cầu. Bạn nên sử dụng server trong câu lệnh :keyword:`with`. Sau đó gọi
:meth:`~BaseServer.handle_request` hoặc
phương thức :meth:`~BaseServer.serve_forever` của đối tượng server để xử lý một hoặc nhiều request. Cuối cùng, hãy gọi :meth:`~BaseServer.server_close` để đóng socket (trừ khi bạn đã sử dụng câu lệnh :keyword:`!with`).

Khi kế thừa từ :class:`ThreadingMixIn` để xử lý kết nối bằng thread, bạn nên khai báo rõ các thread sẽ hoạt động như thế nào khi server tắt đột ngột. Lớp :class:`ThreadingMixIn` định nghĩa một thuộc tính *daemon_threads*, cho biết server có chờ các thread kết thúc hay không. Bạn nên đặt cờ này một cách rõ ràng nếu muốn các thread hoạt động độc lập; giá trị mặc định là :const:`False`, nghĩa là Python sẽ không thoát cho đến khi tất cả các thread do :class:`ThreadingMixIn` tạo đã kết thúc.

Các lớp server có cùng những method và attribute bên ngoài, bất kể chúng sử dụng giao thức mạng nào.


Ghi chú về việc tạo server
--------------------------

Có năm lớp trong sơ đồ kế thừa, trong đó bốn lớp đại diện cho bốn loại server đồng bộ.::

   +------------+
   | BaseServer |
   +------------+
         |
         v
   +-----------+        +------------------+
   | TCPServer |------->| UnixStreamServer |
   +-----------+        +------------------+
         |
         v
   +-----------+        +--------------------+
   | UDPServer |------->| UnixDatagramServer |
   +-----------+        +--------------------+

Lưu ý rằng :class:`UnixDatagramServer` kế thừa từ :class:`UDPServer`, không phải từ
:class:`UnixStreamServer` — điểm khác biệt duy nhất giữa server IP và server Unix là họ địa chỉ.


.. class:: ForkingMixIn
           ThreadingMixIn

   Có thể tạo các phiên bản server sử dụng forking và threading cho từng loại server bằng các lớp mix-in này. Ví dụ, :class:`ThreadingUDPServer` được tạo như sau::

      class ThreadingUDPServer(ThreadingMixIn, UDPServer):
          pass

   Lớp mix-in được đặt trước, vì nó ghi đè một phương thức được định nghĩa trong
   :class:`UDPServer`. Việc thiết lập các thuộc tính khác nhau cũng làm thay đổi cách hoạt động của cơ chế server bên dưới.

   :class:`ForkingMixIn` và các lớp Forking được đề cập bên dưới chỉ khả dụng trên các nền tảng POSIX hỗ trợ :func:`~os.fork`.

   .. attribute:: block_on_close

      :meth:`ForkingMixIn.server_close <BaseServer.server_close>` chờ cho đến khi tất cả các tiến trình con hoàn tất, trừ khi
      thuộc tính :attr:`block_on_close` là ``False``.

      :meth:`ThreadingMixIn.server_close <BaseServer.server_close>` sẽ chờ cho đến khi tất cả các thread không phải daemon hoàn tất, trừ khi
      thuộc tính :attr:`block_on_close` là ``False``.

   .. attribute:: max_children

      Chỉ định số lượng tiến trình con sẽ tồn tại để xử lý các yêu cầu cùng lúc cho :class:`ForkingMixIn`. Nếu đạt đến giới hạn, các yêu cầu mới sẽ chờ cho đến khi một tiến trình con hoàn tất.

   .. attribute:: daemon_threads

      Đối với :class:`ThreadingMixIn`, hãy sử dụng các thread daemon bằng cách đặt
      :data:`ThreadingMixIn.daemon_threads <daemon_threads>` thành ``True`` để không phải chờ cho đến khi các thread hoàn tất.

   .. versionchanged:: 3.7

      :meth:`ForkingMixIn.server_close <BaseServer.server_close>` và
      :meth:`ThreadingMixIn.server_close <BaseServer.server_close>` hiện sẽ chờ cho đến khi tất cả các tiến trình con và thread không phải daemon hoàn tất. Thêm một thuộc tính lớp :attr:`ForkingMixIn.block_on_close <block_on_close>` mới để bật hành vi trước phiên bản 3.7.


.. class:: ForkingTCPServer
           ForkingUDPServer ThreadingTCPServer ThreadingUDPServer ForkingUnixStreamServer ForkingUnixDatagramServer ThreadingUnixStreamServer ThreadingUnixDatagramServer

   Các lớp này được định nghĩa sẵn bằng cách sử dụng các lớp mix-in.

.. versionadded:: 3.12
   Các lớp ``ForkingUnixStreamServer`` và ``ForkingUnixDatagramServer`` đã được thêm vào.

Để triển khai một dịch vụ, bạn phải tạo một lớp dẫn xuất từ :class:`BaseRequestHandler` và định nghĩa lại phương thức :meth:`~BaseRequestHandler.handle` của lớp đó. Sau đó, bạn có thể chạy nhiều phiên bản khác nhau của dịch vụ bằng cách kết hợp một trong các lớp server với lớp xử lý yêu cầu của mình. Lớp xử lý yêu cầu phải khác nhau đối với dịch vụ datagram hoặc stream. Bạn có thể ẩn sự khác biệt này bằng cách sử dụng các lớp con của handler
:class:`StreamRequestHandler` hoặc :class:`DatagramRequestHandler`.

Tất nhiên, bạn vẫn phải suy nghĩ thận trọng! Chẳng hạn, sẽ không hợp lý khi sử dụng một server fork nếu dịch vụ chứa trạng thái trong bộ nhớ có thể bị các yêu cầu khác nhau sửa đổi, vì những thay đổi trong tiến trình con sẽ không bao giờ được phản ánh vào trạng thái ban đầu nằm trong tiến trình cha và được truyền cho mỗi tiến trình con. Trong trường hợp này, bạn có thể sử dụng một server threading, nhưng có lẽ sẽ phải sử dụng các lock để bảo vệ tính toàn vẹn của dữ liệu dùng chung.

Mặt khác, nếu bạn đang xây dựng một HTTP server trong đó tất cả dữ liệu được lưu trữ bên ngoài (chẳng hạn trong hệ thống tệp), một lớp synchronous về cơ bản sẽ khiến dịch vụ trở nên "điếc" trong khi một yêu cầu đang được xử lý -- thời gian này có thể rất dài nếu client nhận dữ liệu mà nó yêu cầu một cách chậm chạp. Trong trường hợp này, server threading hoặc forking là lựa chọn phù hợp.

Trong một số trường hợp, việc xử lý một phần request một cách đồng bộ có thể phù hợp, nhưng việc xử lý có thể được hoàn tất trong một tiến trình con được fork tùy thuộc vào dữ liệu của request. Có thể triển khai điều này bằng cách sử dụng một synchronous server và thực hiện fork tường minh trong phương thức :meth:`~BaseRequestHandler.handle` của lớp request handler.

Một cách tiếp cận khác để xử lý nhiều request đồng thời trong môi trường không hỗ trợ threads hoặc :func:`~os.fork` (hoặc khi các cơ chế này quá tốn kém hay không phù hợp với service) là duy trì một bảng tường minh gồm các request chưa hoàn tất và sử dụng :mod:`selectors` để quyết định request nào sẽ được xử lý tiếp theo (hoặc có nên xử lý một request mới đến hay không). Điều này đặc biệt quan trọng đối với các stream service, nơi mỗi client có thể duy trì kết nối trong thời gian dài (nếu không thể sử dụng threads hoặc subprocesses).

.. XXX should data and methods be intermingled, or separate?
   how should the distinction between class and instance variables be drawn?


Các đối tượng Server
--------------------

.. class:: BaseServer(server_address, RequestHandlerClass)

   Đây là lớp cha của tất cả các đối tượng Server trong module. Lớp này định nghĩa interface được mô tả bên dưới, nhưng không triển khai hầu hết các phương thức; việc đó được thực hiện trong các lớp con. Hai tham số được lưu trong các
   thuộc tính :attr:`server_address` và :attr:`RequestHandlerClass` tương ứng.


   .. method:: fileno()

      Trả về một file descriptor dạng số nguyên cho socket mà server đang lắng nghe. Hàm này thường được truyền cho :mod:`selectors` để cho phép giám sát nhiều server trong cùng một process.


   .. method:: handle_request()

      Xử lý một request đơn. Hàm này lần lượt gọi các phương thức sau: :meth:`get_request`, :meth:`verify_request`, và
      :meth:`process_request`.  Nếu người dùng cung cấp
      phương thức :meth:`~BaseRequestHandler.handle` của lớp handler phát sinh ngoại lệ, phương thức :meth:`handle_error` của server sẽ được gọi.  Nếu không nhận được request nào trong vòng :attr:`timeout` giây, :meth:`handle_timeout` sẽ được gọi và :meth:`handle_request` sẽ trả về.


   .. method:: serve_forever(poll_interval=0.5)

      Xử lý các request cho đến khi nhận được một request :meth:`shutdown` rõ ràng.  Thăm dò trạng thái shutdown sau mỗi *poll_interval* giây. Bỏ qua thuộc tính :attr:`timeout`.  Phương thức này cũng gọi :meth:`service_actions`, có thể được subclass hoặc mixin sử dụng để cung cấp các hành động riêng cho một service cụ thể.  Ví dụ,
      lớp :class:`ForkingMixIn` sử dụng :meth:`service_actions` để dọn dẹp các tiến trình con zombie.

      .. versionchanged:: 3.3
         Đã thêm lệnh gọi ``service_actions`` vào phương thức ``serve_forever``.


   .. method:: service_actions()

      Phương thức này được gọi trong vòng lặp :meth:`serve_forever`. Phương thức này có thể được các subclass hoặc lớp mixin ghi đè để thực hiện các hành động riêng cho một service cụ thể, chẳng hạn như các thao tác dọn dẹp.

      .. versionadded:: 3.3

   .. method:: shutdown()

      Yêu cầu vòng lặp :meth:`serve_forever` dừng lại và chờ cho đến khi vòng lặp dừng.
      :meth:`shutdown` phải được gọi khi :meth:`serve_forever` đang chạy trong một thread khác; nếu không, nó sẽ bị deadlock.


   .. method:: server_close()

      Dọn dẹp server. Có thể được ghi đè.


   .. attribute:: address_family

      Họ giao thức mà socket của server thuộc về. Các ví dụ phổ biến là :const:`socket.AF_INET`, :const:`socket.AF_INET6`, và
      :const:`socket.AF_UNIX`. Phân lớp các lớp server TCP hoặc UDP trong module này với class attribute ``address_family = AF_INET6`` được thiết lập nếu bạn muốn các lớp server IPv6.


   .. attribute:: RequestHandlerClass

      Lớp request handler do người dùng cung cấp; một instance của lớp này được tạo cho mỗi request.


   .. attribute:: server_address

      Địa chỉ mà server đang lắng nghe. Định dạng địa chỉ thay đổi tùy thuộc vào họ giao thức; hãy xem tài liệu của module :mod:`socket` để biết chi tiết. Đối với các giao thức internet, đây là một tuple chứa một string chỉ địa chỉ và một số nguyên chỉ số cổng: ``('127.0.0.1', 80)``, chẳng hạn.


   .. attribute:: socket

      Đối tượng socket mà server sẽ lắng nghe các request đến.


   Các lớp server hỗ trợ những biến lớp sau:

   .. XXX should class variables be covered before instance variables, or vice versa?

   .. attribute:: allow_reuse_address

      Cho biết server có cho phép sử dụng lại một địa chỉ hay không. Giá trị này mặc định là
      :const:`False`, và có thể được thiết lập trong các lớp con để thay đổi chính sách.


   .. attribute:: request_queue_size

      Kích thước của hàng đợi yêu cầu. Nếu mất nhiều thời gian để xử lý một yêu cầu, mọi yêu cầu đến trong khi server đang bận sẽ được xếp vào hàng đợi, tối đa :attr:`request_queue_size` yêu cầu. Khi hàng đợi đầy, các yêu cầu tiếp theo từ client sẽ nhận được lỗi "Connection denied". Giá trị mặc định thường là 5, nhưng các lớp con có thể ghi đè giá trị này.


   .. attribute:: socket_type

      Loại socket được server sử dụng; :const:`socket.SOCK_STREAM` và
      :const:`socket.SOCK_DGRAM` là hai giá trị phổ biến.


   .. attribute:: timeout

      Thời lượng timeout, tính bằng giây, hoặc :const:`None` nếu không muốn đặt timeout. Nếu :meth:`handle_request` không nhận được yêu cầu đến nào trong khoảng thời gian timeout, phương thức :meth:`handle_timeout` sẽ được gọi.


   Có nhiều phương thức server khác nhau có thể được các lớp con của những lớp server cơ sở như :class:`TCPServer` ghi đè; các phương thức này không hữu ích đối với người dùng bên ngoài của đối tượng server.

   .. XXX should the default implementations of these be documented, or should
      it be assumed that the user will look at socketserver.py?

   .. method:: finish_request(request, client_address)

      Thực sự xử lý request bằng cách khởi tạo :attr:`RequestHandlerClass` và gọi phương thức :meth:`~BaseRequestHandler.handle` của nó.


   .. method:: get_request()

      Phải chấp nhận một request từ socket và trả về một bộ 2 phần chứa đối tượng socket *new* được sử dụng để giao tiếp với client và địa chỉ của client.


   .. method:: handle_error(request, client_address)

      Hàm này được gọi nếu phương thức :meth:`~BaseRequestHandler.handle` của một instance :attr:`RequestHandlerClass` phát sinh exception. Hành động mặc định là in traceback ra standard error và tiếp tục xử lý các request tiếp theo.

      .. versionchanged:: 3.6
         Hiện chỉ được gọi cho các exception bắt nguồn từ lớp :exc:`Exception`.


   .. method:: handle_timeout()

      Hàm này được gọi khi thuộc tính :attr:`timeout` được đặt thành một giá trị khác :const:`None` và khoảng thời gian timeout đã trôi qua mà không nhận được request nào. Hành động mặc định đối với các server sử dụng fork là thu thập trạng thái của mọi tiến trình con đã thoát, còn trong các server sử dụng threading, phương thức này không thực hiện gì.


   .. method:: process_request(request, client_address)

      Gọi :meth:`finish_request` để tạo một instance của
      :attr:`RequestHandlerClass`. Nếu muốn, hàm này có thể tạo một tiến trình hoặc luồng mới để xử lý yêu cầu; các :class:`ForkingMixIn` và
      :class:`ThreadingMixIn` thực hiện việc này.


   .. Is there any point in documenting the following two functions?
      What would the purpose of overriding them be: initializing server
      instance variables, adding new network families?

   .. method:: server_activate()

      Được gọi bởi hàm dựng của server để kích hoạt server. Hành vi mặc định đối với TCP server chỉ gọi :meth:`~socket.socket.listen` trên socket của server. Có thể được ghi đè.


   .. method:: server_bind()

      Được gọi bởi hàm dựng của server để liên kết socket với địa chỉ mong muốn. Có thể được ghi đè.


   .. method:: verify_request(request, client_address)

      Phải trả về một giá trị Boolean; nếu giá trị là :const:`True`, yêu cầu sẽ được xử lý, còn nếu là :const:`False`, yêu cầu sẽ bị từ chối. Có thể ghi đè hàm này để triển khai các quyền kiểm soát truy cập cho server. Cách triển khai mặc định luôn trả về :const:`True`.


   .. versionchanged:: 3.6
      Đã bổ sung hỗ trợ cho giao thức :term:`context manager`. Việc thoát khỏi context manager tương đương với việc gọi :meth:`server_close`.


Đối tượng xử lý yêu cầu
-----------------------

.. class:: BaseRequestHandler

   Đây là lớp cha của tất cả các đối tượng xử lý yêu cầu. Lớp này định nghĩa giao diện như dưới đây. Một lớp con xử lý yêu cầu cụ thể phải định nghĩa một phương thức :meth:`handle` mới và có thể ghi đè bất kỳ phương thức nào khác. Một instance mới của lớp con được tạo cho mỗi yêu cầu.


   .. method:: setup()

      Được gọi trước phương thức :meth:`handle` để thực hiện mọi thao tác khởi tạo cần thiết. Cài đặt mặc định không thực hiện thao tác nào.


   .. method:: handle()

      Hàm này phải thực hiện mọi công việc cần thiết để xử lý một yêu cầu. Cài đặt mặc định không thực hiện thao tác nào. Hàm này có thể sử dụng một số thuộc tính instance; yêu cầu được cung cấp dưới dạng :attr:`request`; địa chỉ máy khách dưới dạng :attr:`client_address`; và instance máy chủ dưới dạng
      :attr:`server`, trong trường hợp cần truy cập thông tin riêng của máy chủ.

      Kiểu của :attr:`request` khác nhau tùy theo dịch vụ datagram hoặc stream. Đối với dịch vụ stream, :attr:`request` là một đối tượng socket; đối với dịch vụ datagram, :attr:`request` là một cặp gồm chuỗi và socket.


   .. method:: finish()

      Được gọi sau phương thức :meth:`handle` để thực hiện mọi thao tác dọn dẹp cần thiết. Cài đặt mặc định không thực hiện thao tác nào. Nếu :meth:`setup` phát sinh một ngoại lệ, hàm này sẽ không được gọi.


   .. attribute:: request

      Đối tượng *new* :class:`socket.socket` được dùng để giao tiếp với máy khách.


   .. attribute:: client_address

      Địa chỉ client được trả về bởi :meth:`BaseServer.get_request`.


   .. attribute:: server

      Đối tượng :class:`BaseServer` được sử dụng để xử lý yêu cầu.


.. class:: StreamRequestHandler
           DatagramRequestHandler

   Các lớp con :class:`BaseRequestHandler` này ghi đè
   các phương thức :meth:`~BaseRequestHandler.setup` và :meth:`~BaseRequestHandler.finish`, đồng thời cung cấp các thuộc tính :attr:`rfile` và :attr:`wfile`.

   .. attribute:: rfile

      Một đối tượng file dùng để đọc yêu cầu nhận được. Hỗ trợ interface readable của :class:`io.BufferedIOBase`.

   .. attribute:: wfile

      Một đối tượng file dùng để ghi phản hồi. Hỗ trợ interface writable của :class:`io.BufferedIOBase`


   .. versionchanged:: 3.6
      :attr:`wfile` also supports the
      :class:`io.BufferedIOBase` writable interface.


Ví dụ
-----

:class:`socketserver.TCPServer` Ví dụ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Đây là phía máy chủ::

   import socketserver

   class MyTCPHandler(socketserver.BaseRequestHandler):
       """
       The request handler class for our server.

       It is instantiated once per connection to the server, and must
       override the handle() method to implement communication to the
       client.
       """

       def handle(self):
           # self.request là TCP socket được kết nối với client
           pieces = [b'']
           total = 0
           while b'\n' not in pieces[-1] and total < 10_000:
               pieces.append(self.request.recv(2000))
               total += len(pieces[-1])
           self.data = b''.join(pieces)
           print(f"Received from {self.client_address[0]}:")
           print(self.data.decode("utf-8"))
           # chỉ gửi lại cùng dữ liệu đó nhưng chuyển thành chữ hoa
           self.request.sendall(self.data.upper())
           # sau khi chúng ta trả về, socket sẽ được đóng.

   if __name__ == "__main__":
       HOST, PORT = "localhost", 9999

       # Tạo server, liên kết với localhost trên port 9999
       with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
           # Kích hoạt server; server sẽ tiếp tục chạy cho đến khi bạn
           # ngắt chương trình bằng Ctrl-C
           server.serve_forever()

Một lớp xử lý request thay thế sử dụng streams (các đối tượng giống tệp giúp đơn giản hóa việc giao tiếp bằng cách cung cấp giao diện tệp tiêu chuẩn)::

   class MyTCPHandler(socketserver.StreamRequestHandler):

       def handle(self):
           # self.rfile là một đối tượng giống tệp được handler tạo ra.
           # Giờ đây, chúng ta có thể sử dụng, chẳng hạn, readline() thay vì gọi recv() thô.
           # Chúng ta giới hạn ở 10000 byte để tránh sender lạm dụng.
           self.data = self.rfile.readline(10000).rstrip()
           print(f"{self.client_address[0]} wrote:")
           print(self.data.decode("utf-8"))
           # Tương tự, self.wfile là một đối tượng giống tệp được dùng để ghi trả về
           # tới client
           self.wfile.write(self.data.upper())

Điểm khác biệt là lệnh gọi ``readline()`` trong handler thứ hai sẽ gọi ``recv()`` nhiều lần cho đến khi gặp ký tự xuống dòng, trong khi handler đầu tiên phải sử dụng vòng lặp ``recv()`` để tích lũy dữ liệu cho đến khi gặp ký tự xuống dòng. Nếu chỉ sử dụng một ``recv()`` duy nhất mà không có vòng lặp, nó chỉ trả về phần dữ liệu đã nhận được từ client cho đến thời điểm đó. TCP hoạt động dựa trên stream: dữ liệu đến theo đúng thứ tự đã được gửi, nhưng không có mối liên hệ nào giữa số lần gọi ``send()`` hoặc ``sendall()`` của client và số lần gọi ``recv()`` cần thiết trên server để nhận dữ liệu đó.


Đây là phía client::

   import socket
   import sys

   HOST, PORT = "localhost", 9999
   data = " ".join(sys.argv[1:])

   # Tạo một socket (SOCK_STREAM có nghĩa là socket TCP)
   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
       # Kết nối tới server và gửi dữ liệu
       sock.connect((HOST, PORT))
       sock.sendall(bytes(data, "utf-8"))
       sock.sendall(b"\n")

       # Nhận dữ liệu từ server và tắt kết nối
       received = str(sock.recv(1024), "utf-8")

   print("Sent:    ", data)
   print("Received:", received)


Kết quả đầu ra của ví dụ sẽ trông gần giống như sau:

Máy chủ:

.. code-block:: shell-session

   $ python TCPServer.py
   127.0.0.1 wrote:
   b'hello world with TCP'
   127.0.0.1 wrote:
   b'python is nice'

Máy khách:

.. code-block:: shell-session

   $ python TCPClient.py hello world with TCP
   Sent:     hello world with TCP
   Received: HELLO WORLD WITH TCP
   $ python TCPClient.py python is nice
   Sent:     python is nice
   Received: PYTHON IS NICE


:class:`socketserver.UDPServer` Ví dụ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Đây là phía máy chủ::

   import socketserver

   class MyUDPHandler(socketserver.BaseRequestHandler):
       """
       This class works similar to the TCP handler class, except that
       self.request consists of a pair of data and client socket, and since
       there is no connection the client address must be given explicitly
       when sending data back via sendto().
       """

       def handle(self):
           data = self.request[0].strip()
           socket = self.request[1]
           print(f"{self.client_address[0]} wrote:")
           print(data)
           socket.sendto(data.upper(), self.client_address)

   if __name__ == "__main__":
       HOST, PORT = "localhost", 9999
       with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
           server.serve_forever()

Đây là phía máy khách::

   import socket
   import sys

   HOST, PORT = "localhost", 9999
   data = " ".join(sys.argv[1:])

   # SOCK_DGRAM là loại socket cần dùng cho các socket UDP
   sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

   # Như bạn có thể thấy, không có lời gọi connect(); UDP không có kết nối.
   # Thay vào đó, dữ liệu được gửi trực tiếp đến bên nhận thông qua sendto().
   sock.sendto(bytes(data + "\n", "utf-8"), (HOST, PORT))
   received = str(sock.recv(1024), "utf-8")

   print("Sent:    ", data)
   print("Received:", received)

Đầu ra của ví dụ phải giống hệt như trong ví dụ về máy chủ TCP.


Mixin bất đồng bộ
~~~~~~~~~~~~~~~~~

Để xây dựng các handler bất đồng bộ, hãy sử dụng :class:`ThreadingMixIn` và
các lớp :class:`ForkingMixIn`.

Ví dụ về lớp :class:`ThreadingMixIn`::

   import socket
   import threading
   import socketserver

   class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

       def handle(self):
           data = str(self.request.recv(1024), 'ascii')
           cur_thread = threading.current_thread()
           response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
           self.request.sendall(response)

   class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
       pass

   def client(ip, port, message):
       with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
           sock.connect((ip, port))
           sock.sendall(bytes(message, 'ascii'))
           response = str(sock.recv(1024), 'ascii')
           print("Received: {}".format(response))

   if __name__ == "__main__":
       # Cổng 0 có nghĩa là chọn một cổng chưa được sử dụng bất kỳ
       HOST, PORT = "localhost", 0

       server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
       with server:
           ip, port = server.server_address

           # Khởi động một luồng cùng với server -- sau đó luồng đó sẽ khởi động một luồng khác cho mỗi yêu cầu
           # thoát khỏi luồng server khi luồng chính kết thúc
           server_thread = threading.Thread(target=server.serve_forever)
           # Thoát khỏi luồng server khi luồng chính kết thúc
           server_thread.daemon = True
           server_thread.start()
           print("Server loop running in thread:", server_thread.name)

           client(ip, port, "Hello World 1")
           client(ip, port, "Hello World 2")
           client(ip, port, "Hello World 3")

           server.shutdown()


Kết quả của ví dụ sẽ có dạng như sau:

.. code-block:: shell-session

   $ python ThreadedTCPServer.py
   Server loop running in thread: Thread-1
   Received: Thread-2: Hello World 1
   Received: Thread-3: Hello World 2
   Received: Thread-4: Hello World 3


Lớp :class:`ForkingMixIn` được sử dụng theo cách tương tự, ngoại trừ việc server sẽ tạo một tiến trình mới cho mỗi yêu cầu. Chỉ khả dụng trên các nền tảng POSIX hỗ trợ :func:`~os.fork`.

