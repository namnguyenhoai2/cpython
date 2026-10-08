:mod:`!http.server` --- Máy chủ HTTP
====================================

.. module:: http.server
   :synopsis: Máy chủ HTTP và các trình xử lý yêu cầu.

**Mã nguồn:** :source:`Lib/http/server.py`

.. index::
   pair: WWW; server
   pair: HTTP; protocol
   single: URL
   single: httpd

--------------

Mô-đun này định nghĩa các lớp để triển khai máy chủ HTTP.


.. warning::

    :mod:`!http.server` không được khuyến nghị dùng trong môi trường production. Nó chỉ triển khai
    :ref:`các kiểm tra bảo mật cơ bản <http.server-security>`.

.. include:: ../includes/wasm-notavail.rst

Một lớp, :class:`HTTPServer`, là một lớp con của :class:`socketserver.TCPServer`. Lớp này tạo và lắng nghe trên HTTP socket, phân phối các yêu cầu đến một trình xử lý. Mã để tạo và chạy máy chủ có dạng như sau::

   def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
       server_address = ('', 8000)
       httpd = server_class(server_address, handler_class)
       httpd.serve_forever()


.. class:: HTTPServer(server_address, RequestHandlerClass)

   Lớp này được xây dựng dựa trên lớp :class:`~socketserver.TCPServer` bằng cách lưu trữ địa chỉ máy chủ dưới dạng các biến thực thể có tên :attr:`server_name` và
   :attr:`server_port`. Máy chủ có thể được handler truy cập, thường thông qua biến thực thể :attr:`~socketserver.BaseRequestHandler.server` của handler.

   .. attribute:: server_name

      Tên miền đầy đủ của máy chủ HTTP.

   .. attribute:: server_port

      Số cổng của máy chủ HTTP lấy từ *server_address*.


.. class:: ThreadingHTTPServer(server_address, RequestHandlerClass)

   Lớp này giống hệt HTTPServer nhưng sử dụng các thread để xử lý yêu cầu thông qua :class:`~socketserver.ThreadingMixIn`. Điều này hữu ích khi xử lý các trình duyệt web mở socket trước, trên đó
   :class:`HTTPServer` sẽ chờ vô thời hạn.

   .. versionadded:: 3.7


.. class:: HTTPSServer(server_address, RequestHandlerClass,\
                       bind_and_activate=True, *, certfile, keyfile=None,\ password=None, alpn_protocols=None)

   Lớp con của :class:`HTTPServer` với socket được bọc bằng module :mod:`ssl`. Nếu module :mod:`ssl` không khả dụng, việc khởi tạo đối tượng :class:`!HTTPSServer` sẽ thất bại với :exc:`RuntimeError`.

   Đối số *certfile* là đường dẫn đến tệp chuỗi chứng chỉ SSL, còn *keyfile* là đường dẫn đến tệp chứa khóa riêng tư.

   Có thể chỉ định *password* cho các tệp được bảo vệ và bọc bằng PKCS#8, nhưng hãy lưu ý rằng điều này có thể làm lộ các mật khẩu hardcoded ở dạng văn bản thuần túy.

   .. seealso::

      Xem :meth:`ssl.SSLContext.load_cert_chain` để biết thêm thông tin về các giá trị được chấp nhận cho *certfile*, *keyfile* và *password*.

   Khi được chỉ định, đối số *alpn_protocols* phải là một chuỗi các chuỗi chỉ định những giao thức "Application-Layer Protocol Negotiation" (ALPN) được máy chủ hỗ trợ. ALPN cho phép máy chủ và máy khách thương lượng giao thức ứng dụng trong quá trình bắt tay TLS.

   Theo mặc định, giá trị này là ``["http/1.1"]``, nghĩa là máy chủ hỗ trợ HTTP/1.1.

   .. versionadded:: 3.14

.. class:: ThreadingHTTPSServer(server_address, RequestHandlerClass,\
                                bind_and_activate=True, *, certfile, keyfile=None,\ password=None, alpn_protocols=None)

   Lớp này giống hệt :class:`HTTPSServer` nhưng sử dụng các thread để xử lý yêu cầu bằng cách kế thừa từ :class:`~socketserver.ThreadingMixIn`. Điều này tương tự như :class:`ThreadingHTTPServer`, chỉ khác là sử dụng :class:`HTTPSServer`.

   .. versionadded:: 3.14


:class:`HTTPServer`, :class:`ThreadingHTTPServer`, :class:`HTTPSServer` và
:class:`ThreadingHTTPSServer` phải được cung cấp một *RequestHandlerClass* khi khởi tạo; mô-đun này cung cấp ba biến thể khác nhau của lớp đó:

.. class:: BaseHTTPRequestHandler(request, client_address, server)

   Lớp này được dùng để xử lý các yêu cầu HTTP đến máy chủ. Tự nó không thể phản hồi bất kỳ yêu cầu HTTP thực tế nào; nó phải được tạo lớp con để xử lý từng phương thức yêu cầu (ví dụ: ``'GET'`` hoặc ``'POST'``).
   :class:`BaseHTTPRequestHandler` cung cấp một số biến lớp và biến instance, cùng các phương thức để các lớp con sử dụng.

   Handler sẽ phân tích yêu cầu và các header, sau đó gọi một phương thức tương ứng với loại yêu cầu. Tên phương thức được tạo từ yêu cầu. Ví dụ, với phương thức yêu cầu ``SPAM``, phương thức :meth:`!do_SPAM` sẽ được gọi mà không có đối số. Tất cả thông tin liên quan được lưu trong các biến instance của handler. Các lớp con không cần phải ghi đè hoặc mở rộng phương thức :meth:`!__init__`.

   :class:`BaseHTTPRequestHandler` có các biến instance sau:

   .. attribute:: client_address

      Chứa một tuple có dạng ``(host, port)`` tham chiếu đến địa chỉ của client.

   .. attribute:: server

      Chứa instance của server.

   .. attribute:: close_connection

      Giá trị Boolean cần được thiết lập trước khi :meth:`handle_one_request` trả về, cho biết có thể có request khác hay không, hoặc kết nối có nên được đóng hay không.

   .. attribute:: requestline

      Chứa biểu diễn dạng chuỗi của dòng request HTTP. CRLF kết thúc bị loại bỏ. Thuộc tính này cần được thiết lập bởi
      :meth:`handle_one_request`. Nếu không xử lý được dòng request hợp lệ nào, thuộc tính này cần được thiết lập thành chuỗi rỗng.

   .. attribute:: command

      Chứa command (loại request). Ví dụ: ``'GET'``.

   .. attribute:: path

      Chứa đường dẫn request. Nếu URL có query component, thì ``path`` bao gồm query đó. Theo thuật ngữ của :rfc:`3986`, ``path`` ở đây bao gồm ``hier-part`` và ``query``.

   .. attribute:: request_version

      Chứa chuỗi phiên bản từ request. Ví dụ: ``'HTTP/1.0'``.

   .. attribute:: headers

      Lưu một instance của class được chỉ định bởi biến class :attr:`MessageClass`. Instance này phân tích cú pháp và quản lý các header trong HTTP request. Hàm :func:`~http.client.parse_headers` từ
      :mod:`http.client` được dùng để phân tích cú pháp các header và yêu cầu HTTP request cung cấp một header kiểu :rfc:`5322` hợp lệ.

   .. attribute:: rfile

      Một input stream :class:`io.BufferedIOBase`, sẵn sàng để đọc từ đầu phần dữ liệu đầu vào tùy chọn.

   .. attribute:: wfile

      Chứa output stream để ghi response trả về client. Khi ghi vào stream này, phải tuân thủ đúng giao thức HTTP để đảm bảo khả năng tương tác thành công với các HTTP client.

      .. versionchanged:: 3.6
         Đây là một stream :class:`io.BufferedIOBase`.

   :class:`BaseHTTPRequestHandler` có các thuộc tính sau:

   .. attribute:: server_version

      Chỉ định phiên bản phần mềm máy chủ. Bạn có thể muốn ghi đè giá trị này. Định dạng gồm nhiều chuỗi được phân tách bằng khoảng trắng, trong đó mỗi chuỗi có dạng name[/version]. Ví dụ: ``'BaseHTTP/0.2'``.

   .. attribute:: sys_version

      Chứa phiên bản hệ thống Python, ở dạng có thể được sử dụng bởi
      :attr:`version_string` phương thức và biến lớp :attr:`server_version`. Ví dụ: ``'Python/1.4'``.

   .. attribute:: error_message_format

      Chỉ định chuỗi định dạng sẽ được phương thức :meth:`send_error` sử dụng để tạo phản hồi lỗi gửi đến máy khách. Theo mặc định, chuỗi này được điền các biến từ :attr:`responses` dựa trên mã trạng thái được truyền vào :meth:`send_error`.

   .. attribute:: error_content_type

      Chỉ định HTTP header Content-Type của các phản hồi lỗi gửi đến máy khách. Giá trị mặc định là ``'text/html'``.

   .. attribute:: protocol_version

      Chỉ định phiên bản HTTP mà máy chủ tuân thủ. Phiên bản này được gửi trong các phản hồi để cho máy khách biết khả năng giao tiếp của máy chủ cho các yêu cầu sau này. Nếu được đặt thành ``'HTTP/1.1'``, máy chủ sẽ cho phép các kết nối HTTP persistent; tuy nhiên, máy chủ của bạn *phải* sau đó bao gồm một header ``Content-Length`` chính xác (sử dụng :meth:`send_header`) trong tất cả phản hồi gửi đến máy khách. Để tương thích ngược, cài đặt này mặc định là ``'HTTP/1.0'``.

   .. attribute:: MessageClass

      Chỉ định một lớp tương tự :class:`email.message.Message`\  để phân tích các HTTP header. Thông thường, giá trị này không được ghi đè và mặc định là
      :class:`http.client.HTTPMessage`.

   .. attribute:: responses

      Thuộc tính này chứa ánh xạ từ các số nguyên mã lỗi đến các tuple gồm hai phần tử, chứa thông báo ngắn và dài. Ví dụ: ``{code: (shortmessage, longmessage)}``. *shortmessage* thường được dùng làm khóa *message* trong phản hồi lỗi, còn *longmessage* được dùng làm khóa *explain*. Thuộc tính này được sử dụng bởi
      các phương thức :meth:`send_response_only` và :meth:`send_error`.

   Một instance :class:`BaseHTTPRequestHandler` có các phương thức sau:

   .. method:: handle()

      Gọi :meth:`handle_one_request` một lần (hoặc nhiều lần nếu bật persistent connection) để xử lý các yêu cầu HTTP đến. Bạn không bao giờ cần ghi đè phương thức này; thay vào đó, hãy triển khai các phương thức :meth:`!do_\*` thích hợp.

   .. method:: handle_one_request()

      Phương thức này sẽ phân tích cú pháp và điều phối yêu cầu đến
      phương thức :meth:`!do_\*` thích hợp. Bạn không bao giờ cần ghi đè phương thức này.

   .. method:: handle_expect_100()

      Khi một server tuân thủ HTTP/1.1 nhận được header yêu cầu ``Expect: 100-continue``, server sẽ phản hồi bằng ``100 Continue`` rồi đến các header ``200 OK``. Có thể ghi đè phương thức này để phát sinh lỗi nếu server không muốn client tiếp tục. Ví dụ, server có thể chọn gửi ``417 Expectation Failed`` dưới dạng header phản hồi và ``return False``.

      .. versionadded:: 3.2

   .. method:: send_error(code, message=None, explain=None)

      Gửi và ghi nhật ký một phản hồi lỗi hoàn chỉnh cho client. Số *code* chỉ định mã lỗi HTTP, trong đó *message* là phần mô tả lỗi ngắn gọn, dễ đọc đối với con người và không bắt buộc. Đối số *explain* có thể được dùng để cung cấp thông tin chi tiết hơn về lỗi; thông tin này sẽ được định dạng bằng thuộc tính :attr:`error_message_format` và được ghi ra sau một bộ header hoàn chỉnh, dưới dạng nội dung phản hồi. Thuộc tính :attr:`responses` chứa các giá trị mặc định cho *message* và *explain*, được sử dụng nếu không cung cấp giá trị; đối với các mã không xác định, giá trị mặc định cho cả hai là chuỗi ``???``. Nội dung sẽ rỗng nếu method là HEAD hoặc mã phản hồi là một trong các mã sau: :samp:`1{xx}`, ``204 No Content``, ``205 Reset Content``, ``304 Not Modified``.

      .. versionchanged:: 3.4
         Phản hồi lỗi bao gồm header Content-Length. Đã thêm đối số *explain*.

   .. method:: send_response(code, message=None)

      Thêm một header phản hồi vào bộ đệm header và ghi nhật ký request đã được chấp nhận. Dòng phản hồi HTTP được ghi vào bộ đệm nội bộ, theo sau là các header *Server* và *Date*. Giá trị của hai header này được lấy từ :meth:`version_string` và
      các method :meth:`date_time_string`, tương ứng. Nếu server không định gửi thêm header nào bằng method :meth:`send_header`, thì sau :meth:`send_response` phải gọi :meth:`end_headers`.

      .. versionchanged:: 3.3
         Các header được lưu vào bộ đệm nội bộ và cần gọi :meth:`end_headers` một cách rõ ràng.

   .. method:: send_header(keyword, value)

      Thêm header HTTP vào bộ đệm nội bộ, bộ đệm này sẽ được ghi vào stream đầu ra khi gọi :meth:`end_headers` hoặc :meth:`flush_headers`. *keyword* phải chỉ định keyword của header, còn *value* chỉ định giá trị của header. Lưu ý rằng, sau khi hoàn tất các lệnh gọi send_header,
      :meth:`end_headers` BẮT BUỘC phải được gọi để hoàn tất thao tác.

      Phương thức này không từ chối đầu vào chứa các chuỗi CRLF.

      .. versionchanged:: 3.2
         Các header được lưu trong một bộ đệm nội bộ.

   .. method:: send_response_only(code, message=None)

      Chỉ gửi header phản hồi, được dùng trong trường hợp ``100 Continue`` phản hồi được máy chủ gửi đến client. Các header không được đệm mà được gửi trực tiếp đến luồng đầu ra. Nếu không chỉ định *message*, thông điệp HTTP tương ứng với *code* phản hồi sẽ được gửi.

      Phương thức này không từ chối *message* chứa các chuỗi CRLF.

      .. versionadded:: 3.2

   .. method:: end_headers()

      Thêm một dòng trống (cho biết phần cuối của các HTTP header trong phản hồi) vào bộ đệm header và gọi :meth:`flush_headers`.

      .. versionchanged:: 3.2
         Các header được đệm sẽ được ghi vào luồng đầu ra.

   .. method:: flush_headers()

      Cuối cùng, gửi các header đến luồng đầu ra và xóa bộ đệm header nội bộ.

      .. versionadded:: 3.3

   .. method:: log_request(code='-', size='-')

      Ghi nhật ký một yêu cầu đã được chấp nhận (thành công). *code* phải chỉ định mã HTTP dạng số tương ứng với phản hồi. Nếu có kích thước của phản hồi, thì kích thước đó phải được truyền dưới dạng tham số *size*.

   .. method:: log_error(...)

      Ghi nhật ký lỗi khi không thể đáp ứng một yêu cầu. Theo mặc định, phương thức này truyền thông báo đến :meth:`log_message`, vì vậy nó nhận cùng các đối số (*format* và các giá trị bổ sung).


   .. method:: log_message(format, ...)

      Ghi một thông báo tùy ý vào ``sys.stderr``. Thông thường, phương thức này được ghi đè để tạo các cơ chế ghi nhật ký lỗi tùy chỉnh. Đối số *format* là một chuỗi định dạng theo kiểu printf tiêu chuẩn, trong đó các đối số bổ sung truyền cho
      :meth:`log_message` được dùng làm đầu vào cho việc định dạng. Địa chỉ IP của máy khách cùng ngày và giờ hiện tại được thêm vào trước mọi thông báo được ghi nhật ký.

   .. method:: version_string()

      Trả về chuỗi phiên bản của phần mềm máy chủ. Chuỗi này là sự kết hợp của
      các thuộc tính :attr:`server_version` và :attr:`sys_version`.

   .. method:: date_time_string(timestamp=None)

      Trả về ngày và giờ do *timestamp* cung cấp (phải là ``None`` hoặc có định dạng do :func:`time.time` trả về), được định dạng để dùng trong tiêu đề thông báo. Nếu bỏ qua *timestamp*, phương thức này sử dụng ngày và giờ hiện tại.

      Kết quả có dạng ``'Sun, 06 Nov 1994 08:49:37 GMT'``.

   .. method:: log_date_time_string()

      Trả về ngày và giờ hiện tại, được định dạng để ghi nhật ký.

   .. method:: address_string()

      Trả về địa chỉ của client.

      .. versionchanged:: 3.3
         Trước đây, thao tác tra cứu tên đã được thực hiện. Để tránh độ trễ khi phân giải tên, hiện tại phương thức này luôn trả về địa chỉ IP.


.. class:: SimpleHTTPRequestHandler(request, client_address, server, directory=None)

   Lớp này phục vụ các tệp từ thư mục *directory* trở xuống hoặc từ thư mục hiện tại nếu không cung cấp *directory*, trực tiếp ánh xạ cấu trúc thư mục với các yêu cầu HTTP.

   .. versionchanged:: 3.7
      Đã thêm tham số *directory*.

   .. versionchanged:: 3.9
      Tham số *directory* chấp nhận một :term:`path-like object`.

   Phần lớn công việc, chẳng hạn như phân tích cú pháp request, được thực hiện bởi lớp cơ sở
   :class:`BaseHTTPRequestHandler`. Lớp này triển khai các hàm :func:`do_GET` và :func:`do_HEAD`.

   Sau đây được định nghĩa là các thuộc tính cấp lớp của
   :class:`SimpleHTTPRequestHandler`:

   .. attribute:: server_version

      Đây sẽ là ``"SimpleHTTP/" + __version__``, trong đó ``__version__`` được định nghĩa ở cấp module.

   .. attribute:: index_pages

      Chỉ định các tên tệp được coi là các trang chỉ mục của thư mục.

      Mặc định là ``("index.html", "index.htm")``.

      .. versionadded:: 3.12

   .. attribute:: extensions_map

      Một dictionary ánh xạ các hậu tố sang các MIME type, chứa các ghi đè tùy chỉnh cho các ánh xạ mặc định của hệ thống. Việc ánh xạ không phân biệt chữ hoa chữ thường, vì vậy chỉ nên chứa các khóa được viết bằng chữ thường.

      .. versionchanged:: 3.9
         Từ điển này không còn được điền bằng các ánh xạ hệ thống mặc định mà chỉ chứa các giá trị ghi đè.

   Lớp :class:`SimpleHTTPRequestHandler` định nghĩa các phương thức sau:

   .. method:: do_HEAD()

      Phương thức này xử lý loại yêu cầu ``'HEAD'``: nó gửi các header mà nó sẽ gửi cho yêu cầu ``GET`` tương đương. Xem phương thức :meth:`do_GET` để biết giải thích đầy đủ hơn về các header có thể có.

   .. method:: do_GET()

      Yêu cầu được ánh xạ tới một tệp cục bộ bằng cách diễn giải yêu cầu như một đường dẫn tương đối so với thư mục làm việc hiện tại.

      Nếu yêu cầu được ánh xạ tới một thư mục, thư mục đó sẽ được kiểm tra để tìm trang chỉ mục như được chỉ định bởi :attr:`index_pages`. Nếu tìm thấy, nội dung của tệp sẽ được trả về; nếu không, danh sách thư mục sẽ được tạo bằng cách gọi phương thức :meth:`list_directory`. Phương thức này sử dụng
      :func:`os.listdir` để quét thư mục và trả về phản hồi lỗi ``404`` nếu :func:`~os.listdir` không thành công.

      Nếu yêu cầu được ánh xạ tới một tệp, tệp đó sẽ được mở. Mọi ngoại lệ :exc:`OSError` khi mở tệp được yêu cầu sẽ được ánh xạ tới lỗi ``404``, ``'File not found'``. Nếu yêu cầu có header ``'If-Modified-Since'`` và tệp không được sửa đổi sau thời điểm này, phản hồi ``304``, ``'Not Modified'`` sẽ được gửi. Nếu không, loại nội dung được suy đoán bằng cách gọi phương thức :meth:`guess_type`, phương thức này lần lượt sử dụng biến *extensions_map*, rồi nội dung tệp được trả về.

      Một header ``'Content-type:'`` với kiểu nội dung được phỏng đoán sẽ được xuất ra, tiếp theo là header ``'Content-Length:'`` với kích thước tệp và header ``'Last-Modified:'`` với thời điểm tệp được sửa đổi.

      Tiếp theo là một dòng trống biểu thị phần kết thúc của các header, rồi nội dung của tệp được xuất ra.

      Để xem ví dụ sử dụng, hãy xem phần triển khai của hàm ``test`` trong :source:`Lib/http/server.py`.

      .. versionchanged:: 3.7
         Hỗ trợ header ``'If-Modified-Since'``.

   .. method:: list_directory(path)

      Hàm trợ giúp liệt kê nội dung của *path* khi không có trang chỉ mục.

      Hàm này trả về либо một :term:`file-like object` (bên gọi phải đóng đối tượng này) hoặc ``None`` để chỉ ra lỗi; trong trường hợp đó, bên gọi không cần thực hiện thêm thao tác nào. Trong cả hai trường hợp, các header đều được gửi.

   .. method:: guess_type(path)

      Đoán kiểu của tệp tại *path* đã cho.

      Phương thức này trả về một chuỗi có dạng ``type/subtype``, có thể dùng cho header MIME Content-type.

      Cài đặt mặc định tra cứu phần mở rộng của tệp trong
      :attr:`extensions_map`, nếu không tìm thấy thì chuyển sang
      :func:`mimetypes.guess_file_type`, rồi đến ``'application/octet-stream'``.

      .. versionchanged:: 3.13
         Thêm :func:`mimetypes.guess_file_type` làm giá trị dự phòng.


Có thể dùng lớp :class:`SimpleHTTPRequestHandler` để tạo một webserver rất cơ bản, phục vụ các tệp tương đối với thư mục hiện tại như sau::

   import http.server
   import socketserver

   PORT = 8000

   Handler = http.server.SimpleHTTPRequestHandler

   with socketserver.TCPServer(("", PORT), Handler) as httpd:
       print("serving at port", PORT)
       httpd.serve_forever()


:class:`SimpleHTTPRequestHandler` cũng có thể được phân lớp để mở rộng hành vi, chẳng hạn như sử dụng các tên tệp chỉ mục khác bằng cách ghi đè thuộc tính lớp
:attr:`~SimpleHTTPRequestHandler.index_pages`.


.. class:: CGIHTTPRequestHandler(request, client_address, server)

   Lớp này được dùng để phục vụ các tệp hoặc đầu ra của các script CGI từ thư mục hiện tại và các thư mục bên dưới. Lưu ý rằng việc ánh xạ cấu trúc phân cấp HTTP sang cấu trúc thư mục cục bộ hoàn toàn giống như trong :class:`SimpleHTTPRequestHandler`.

   .. note::

      Các script CGI được chạy bởi lớp :class:`CGIHTTPRequestHandler` không thể thực hiện chuyển hướng (mã HTTP 302), vì mã 200 (sau đó là đầu ra của script) được gửi trước khi thực thi script CGI. Điều này khiến mã trạng thái bị bỏ qua.

   Tuy nhiên, lớp này sẽ chạy script CGI thay vì phục vụ script đó dưới dạng tệp nếu nhận định đó là một script CGI. Chỉ CGI dựa trên thư mục được sử dụng --- cấu hình máy chủ phổ biến khác là coi các phần mở rộng đặc biệt là dấu hiệu của script CGI.

   :func:`~SimpleHTTPRequestHandler.do_GET` và
   Các hàm :func:`~SimpleHTTPRequestHandler.do_HEAD` được sửa đổi để chạy các script CGI và phục vụ đầu ra của chúng thay vì phục vụ tệp, nếu yêu cầu dẫn đến một vị trí bên dưới đường dẫn ``cgi_directories``.

   :class:`CGIHTTPRequestHandler` định nghĩa thành viên dữ liệu sau:

   .. attribute:: cgi_directories

      Giá trị mặc định là ``['/cgi-bin', '/htbin']`` và mô tả các thư mục được coi là chứa các script CGI.

   :class:`CGIHTTPRequestHandler` định nghĩa phương thức sau:

   .. method:: do_POST()

      Phương thức này phục vụ loại yêu cầu ``'POST'``, chỉ được phép đối với các CGI script. Lỗi 501, "Can only POST to CGI scripts", sẽ được xuất ra khi cố gắng POST đến một url không phải CGI.

   Lưu ý rằng các CGI script sẽ được chạy với UID của người dùng nobody vì lý do bảo mật. Các vấn đề với CGI script sẽ được chuyển thành lỗi 403.

   .. deprecated-removed:: 3.13 3.15

      :class:`CGIHTTPRequestHandler` sẽ bị loại bỏ trong 3.15. CGI từ lâu, hơn một thập kỷ, đã không được xem là cách làm tốt. Mã này đã không được bảo trì trong một thời gian và hầu như không được sử dụng trong thực tế. Việc giữ lại mã này có thể dẫn đến các :ref:`security considerations <http.server-security>` tiếp theo.


.. _http-server-cli:

Giao diện dòng lệnh
-------------------

:mod:`!http.server` cũng có thể được gọi trực tiếp bằng switch :option:`-m` của interpreter. Ví dụ sau minh họa cách phục vụ các tệp tương đối với thư mục hiện tại:

.. code-block:: bash

   python -m http.server [OPTIONS] [port]

Các tùy chọn sau được chấp nhận:

.. program:: http.server

.. option:: port

   Theo mặc định, máy chủ lắng nghe trên cổng 8000. Có thể ghi đè giá trị mặc định bằng cách truyền số cổng mong muốn làm đối số:

   .. code-block:: bash

      python -m http.server 9000

.. option:: -b, --bind <address>

   Chỉ định một địa chỉ cụ thể mà máy chủ sẽ liên kết. Cả địa chỉ IPv4 và IPv6 đều được hỗ trợ. Theo mặc định, máy chủ tự liên kết với tất cả các giao diện. Ví dụ: lệnh sau khiến máy chủ chỉ liên kết với localhost:

   .. code-block:: bash

      python -m http.server --bind 127.0.0.1

   .. versionadded:: 3.4

   .. versionchanged:: 3.8
      Hỗ trợ IPv6 trong tùy chọn ``--bind``.

.. option:: -d, --directory <dir>

   Chỉ định một thư mục để máy chủ cung cấp các tệp. Theo mặc định, máy chủ sử dụng thư mục hiện tại. Ví dụ: lệnh sau sử dụng một thư mục cụ thể:

   .. code-block:: bash

      python -m http.server --directory /tmp/

   .. versionadded:: 3.7

.. option:: -p, --protocol <version>

   Chỉ định phiên bản HTTP mà máy chủ tuân thủ. Theo mặc định, máy chủ tuân thủ HTTP/1.0. Ví dụ: lệnh sau chạy một máy chủ tuân thủ HTTP/1.1:

   .. code-block:: bash

      python -m http.server --protocol HTTP/1.1

   .. versionadded:: 3.11

.. option:: --cgi

   Có thể bật :class:`CGIHTTPRequestHandler` trên dòng lệnh bằng cách truyền tùy chọn ``--cgi``::

      python -m http.server --cgi

   .. deprecated-removed:: 3.13 3.15

      :mod:`!http.server` dòng lệnh ``--cgi`` hỗ trợ đang bị loại bỏ vì :class:`CGIHTTPRequestHandler` đang bị loại bỏ.

.. warning::

   :class:`CGIHTTPRequestHandler` và tùy chọn dòng lệnh ``--cgi`` không предназначены để các client không đáng tin cậy sử dụng và có thể dễ bị khai thác. Luôn sử dụng trong môi trường an toàn.

.. option:: --tls-cert

   Chỉ định chuỗi chứng chỉ TLS cho các kết nối HTTPS:

   .. code-block:: bash

      python -m http.server --tls-cert fullchain.pem

   .. versionadded:: 3.14

.. option:: --tls-key

   Chỉ định tệp khóa riêng tư cho các kết nối HTTPS.

   Tùy chọn này yêu cầu phải chỉ định ``--tls-cert``.

   .. versionadded:: 3.14

.. option:: --tls-password-file

   Chỉ định tệp mật khẩu cho các khóa riêng tư được bảo vệ bằng mật khẩu:

   .. code-block:: bash

      python -m http.server \
             --tls-cert cert.pem \
             --tls-key key.pem \
             --tls-password-file password.txt

   Tùy chọn này yêu cầu phải chỉ định ``--tls-cert``.

   .. versionadded:: 3.14


.. _http.server-security:

Các cân nhắc về bảo mật
-----------------------

.. index:: pair: http.server; security

:class:`SimpleHTTPRequestHandler` sẽ đi theo các symbolic link khi xử lý yêu cầu, khiến các tệp bên ngoài thư mục được chỉ định có thể được phân phát.

Các phương thức :meth:`BaseHTTPRequestHandler.send_header` và
:meth:`BaseHTTPRequestHandler.send_response_only` giả định rằng dữ liệu đầu vào đã được làm sạch và không thực hiện việc xác thực đầu vào, chẳng hạn như kiểm tra sự hiện diện của các chuỗi CRLF. Dữ liệu đầu vào không đáng tin cậy có thể dẫn đến các cuộc tấn công chèn HTTP header.

Các phiên bản Python trước đây không loại bỏ các ký tự điều khiển khỏi thông báo nhật ký được ghi vào stderr từ ``python -m http.server`` hoặc từ triển khai :class:`BaseHTTPRequestHandler` ``.log_message`` mặc định. Điều này có thể cho phép các client từ xa kết nối với máy chủ của bạn gửi các mã điều khiển độc hại đến terminal của bạn.

.. versionchanged:: 3.12
   Các ký tự điều khiển được loại bỏ khỏi nhật ký stderr.
