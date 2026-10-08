:mod:`!http.client` --- HTTP protocol client
============================================

.. module:: http.client
   :synopsis: Ứng dụng khách cho giao thức HTTP và HTTPS (yêu cầu sockets).

**Mã nguồn:** :source:`Lib/http/client.py`

.. index::
   pair: HTTP; protocol
   single: HTTP; http.client (standard module)

.. index:: pair: module; urllib.request

--------------

Mô-đun này định nghĩa các lớp triển khai phía ứng dụng khách của các giao thức HTTP và HTTPS. Thông thường, mô-đun này không được sử dụng trực tiếp --- mô-đun
:mod:`urllib.request` sử dụng nó để xử lý các URL sử dụng HTTP và HTTPS.

.. seealso::

    Gói `Requests package <https://requests.readthedocs.io/en/latest/>`_ được khuyến nghị để cung cấp giao diện ứng dụng khách HTTP ở cấp cao hơn.

.. note::

   Chỉ có thể hỗ trợ HTTPS nếu Python được biên dịch với hỗ trợ SSL (thông qua mô-đun :mod:`ssl`).

.. include:: ../includes/wasm-notavail.rst

Mô-đun cung cấp các lớp sau:


.. class:: HTTPConnection(host, port=None[, timeout], source_address=None, \
                          blocksize=8192)

   Một đối tượng :class:`HTTPConnection` đại diện cho một giao dịch với máy chủ HTTP. Đối tượng này nên được khởi tạo bằng cách truyền vào một host và số cổng tùy chọn. Nếu không truyền số cổng, cổng sẽ được trích xuất từ chuỗi host nếu chuỗi có dạng ``host:port``; nếu không, cổng HTTP mặc định (80) sẽ được sử dụng. Nếu truyền tham số *timeout* tùy chọn, các thao tác blocking (chẳng hạn như việc cố gắng kết nối) sẽ hết thời gian chờ sau số giây tương ứng (nếu không truyền, thiết lập timeout mặc định toàn cục sẽ được sử dụng). Tham số *source_address* tùy chọn có thể là một tuple gồm (host, port) để sử dụng làm địa chỉ nguồn nơi kết nối HTTP được thiết lập. Tham số *blocksize* tùy chọn đặt kích thước bộ đệm tính bằng byte để gửi phần thân thông điệp dạng file-like.

   Ví dụ, tất cả các lệnh gọi sau đều tạo ra các đối tượng kết nối đến máy chủ có cùng host và port::

      >>> h1 = http.client.HTTPConnection('www.python.org')
      >>> h2 = http.client.HTTPConnection('www.python.org:80')
      >>> h3 = http.client.HTTPConnection('www.python.org', 80)
      >>> h4 = http.client.HTTPConnection('www.python.org', 80, timeout=10)

   .. versionchanged:: 3.2
      Đã thêm *source_address*.

   .. versionchanged:: 3.4
      Tham số *strict* đã bị xóa. Các "Simple Responses" theo kiểu HTTP 0.9 không còn được hỗ trợ.

   .. versionchanged:: 3.7
      Đã thêm tham số *blocksize*.


.. class:: HTTPSConnection(host, port=None, *[, timeout], \
                           source_address=None, context=None, \ blocksize=8192)

   Một lớp con của :class:`HTTPConnection` sử dụng SSL để giao tiếp với các máy chủ bảo mật. Cổng mặc định là ``443``. Nếu chỉ định *context*, thì giá trị này phải là một thực thể :class:`ssl.SSLContext` mô tả các tùy chọn SSL khác nhau.

   Vui lòng đọc :ref:`ssl-security` để biết thêm thông tin về các phương pháp hay nhất.

   .. versionchanged:: 3.2
      *source_address*, *context* và *check_hostname* đã được bổ sung.

   .. versionchanged:: 3.2
      Lớp này hiện hỗ trợ các virtual host HTTPS nếu có thể (nghĩa là nếu :const:`ssl.HAS_SNI` là true).

   .. versionchanged:: 3.4
      Tham số *strict* đã bị loại bỏ. Các "Phản hồi đơn giản" theo kiểu HTTP 0.9 không còn được hỗ trợ.

   .. versionchanged:: 3.4.3
      Lớp này hiện thực hiện tất cả các bước kiểm tra chứng chỉ và hostname cần thiết theo mặc định. Để khôi phục hành vi trước đây, không thực hiện xác minh
      :func:`!ssl._create_unverified_context` có thể được truyền vào tham số *context*.

   .. versionchanged:: 3.8
      Lớp này hiện cho phép TLS 1.3
      :attr:`ssl.SSLContext.post_handshake_auth` cho *context* mặc định hoặc khi *cert_file* được truyền cùng với *context* tùy chỉnh.

   .. versionchanged:: 3.10
      Khi không cung cấp *context*, lớp này hiện gửi một phần mở rộng ALPN với chỉ báo giao thức ``http/1.1``. *context* tùy chỉnh nên thiết lập các giao thức ALPN bằng :meth:`~ssl.SSLContext.set_alpn_protocols`.

   .. versionchanged:: 3.12
      Các tham số không còn được khuyến nghị *key_file*, *cert_file* và *check_hostname* đã bị loại bỏ.


.. class:: HTTPResponse(sock, debuglevel=0, method=None, url=None)

   Lớp có các thể hiện được trả về khi kết nối thành công. Người dùng không khởi tạo lớp này trực tiếp.

   .. versionchanged:: 3.4
      Tham số *strict* đã bị loại bỏ. Các "Simple Responses" theo kiểu HTTP 0.9 không còn được hỗ trợ.

Mô-đun này cung cấp hàm sau:

.. function:: parse_headers(fp)

   Phân tích các header từ con trỏ tệp *fp* đại diện cho một yêu cầu/phản hồi HTTP. Tệp phải là một reader :class:`~io.BufferedIOBase` (tức là không phải văn bản) và phải cung cấp header kiểu :rfc:`5322` hợp lệ.

   Hàm này trả về một thực thể của :class:`http.client.HTTPMessage` chứa các trường header nhưng không có payload (giống như :attr:`HTTPResponse.msg` và :attr:`http.server.BaseHTTPRequestHandler.headers`). Sau khi hàm trả về, con trỏ tệp *fp* đã sẵn sàng để đọc phần nội dung HTTP.

   .. note::
      :meth:`parse_headers` does not parse the start-line of a HTTP message;
      hàm này chỉ phân tích các dòng ``Name: value``. Tệp phải sẵn sàng để đọc các dòng trường này, vì vậy dòng đầu tiên phải được đọc trước khi gọi hàm.

Các ngoại lệ sau sẽ được phát sinh khi thích hợp:


.. exception:: HTTPException

   Lớp cơ sở của các ngoại lệ khác trong mô-đun này. Đây là lớp con của
   :exc:`Exception`.


.. exception:: NotConnected

   Một lớp con của :exc:`HTTPException`.


.. exception:: InvalidURL

   Một lớp con của :exc:`HTTPException`, được phát sinh khi một cổng được cung cấp nhưng không phải là số hoặc bị để trống.


.. exception:: UnknownProtocol

   Một lớp con của :exc:`HTTPException`.


.. exception:: UnknownTransferEncoding

   Một lớp con của :exc:`HTTPException`.


.. exception:: UnimplementedFileMode

   Một lớp con của :exc:`HTTPException`.


.. exception:: IncompleteRead

   Một lớp con của :exc:`HTTPException`.


.. exception:: ImproperConnectionState

   Một lớp con của :exc:`HTTPException`.


.. exception:: CannotSendRequest

   Một lớp con của :exc:`ImproperConnectionState`.


.. exception:: CannotSendHeader

   Một lớp con của :exc:`ImproperConnectionState`.


.. exception:: ResponseNotReady

   Một lớp con của :exc:`ImproperConnectionState`.


.. exception:: BadStatusLine

   Một lớp con của :exc:`HTTPException`. Được phát sinh nếu máy chủ phản hồi bằng mã trạng thái HTTP mà chúng ta không hiểu.


.. exception:: LineTooLong

   Một lớp con của :exc:`HTTPException`. Được phát sinh nếu nhận được một dòng quá dài trong giao thức HTTP từ máy chủ.


.. exception:: RemoteDisconnected

   Một lớp con của :exc:`ConnectionResetError` và :exc:`BadStatusLine`. Được :meth:`HTTPConnection.getresponse` phát sinh khi nỗ lực đọc phản hồi không đọc được dữ liệu nào từ kết nối, cho biết đầu bên kia đã đóng kết nối.

   .. versionadded:: 3.5
      Trước đây, :exc:`BadStatusLine`\ ``('')`` đã được phát sinh.


Các hằng số được định nghĩa trong module này là:

.. data:: HTTP_PORT

   Cổng mặc định cho giao thức HTTP (luôn là ``80``).

.. data:: HTTPS_PORT

   Cổng mặc định cho giao thức HTTPS (luôn là ``443``).

.. data:: responses

   Từ điển này ánh xạ các mã trạng thái HTTP 1.1 với tên W3C.

   Ví dụ: ``http.client.responses[http.client.NOT_FOUND]`` là ``'Not Found'``.

Xem :ref:`http-status-codes` để biết danh sách các mã trạng thái HTTP có sẵn trong mô-đun này dưới dạng hằng số.


.. _httpconnection-objects:

Đối tượng HTTPConnection
------------------------

Các instance của :class:`HTTPConnection` có những phương thức sau:


.. method:: HTTPConnection.request(method, url, body=None, headers={}, *, \
            encode_chunked=False)

   Thao tác này sẽ gửi một request đến máy chủ bằng HTTP request method *method* và request URI *url*. *url* được cung cấp phải là một đường dẫn tuyệt đối để tuân thủ :rfc:`RFC 2616 §5.1.2 <2616#section-5.1.2>` (trừ khi kết nối đến HTTP proxy server hoặc sử dụng các method ``OPTIONS`` hoặc ``CONNECT``).

   Nếu *body* được chỉ định, dữ liệu đã chỉ định sẽ được gửi sau khi hoàn tất các headers. Dữ liệu này có thể là một :class:`str`, một :term:`bytes-like object`, một :term:`file object` đang mở hoặc một iterable của :class:`bytes`. Nếu *body* là một chuỗi, chuỗi đó được mã hóa bằng ISO-8859-1, là mã hóa mặc định cho HTTP. Nếu đó là một đối tượng dạng bytes, các byte sẽ được gửi nguyên trạng. Nếu đó là một :term:`file object`, nội dung của tệp sẽ được gửi; đối tượng tệp này ít nhất phải hỗ trợ phương thức ``read()`` Nếu đối tượng tệp là một instance của :class:`io.TextIOBase`, dữ liệu do phương thức ``read()`` trả về sẽ được mã hóa bằng ISO-8859-1; nếu không, dữ liệu do ``read()`` trả về sẽ được gửi nguyên trạng. Nếu *body* là một iterable, các phần tử của iterable sẽ được gửi nguyên trạng cho đến khi iterable được :term:`exhausted`.

   Đối số *headers* phải là một mapping chứa các HTTP header bổ sung cần gửi cùng request. Phải cung cấp một :rfc:`Host header <2616#section-14.23>` để tuân thủ :rfc:`RFC 2616 §5.1.2 <2616#section-5.1.2>` (trừ khi kết nối đến HTTP proxy server hoặc sử dụng các method ``OPTIONS`` hoặc ``CONNECT``).

   Nếu *headers* không chứa Content-Length cũng như Transfer-Encoding, nhưng có request body, một trong các trường header đó sẽ được tự động thêm vào. Nếu *body* là ``None``, header Content-Length được đặt thành ``0`` cho các method yêu cầu body (``PUT``, ``POST`` và ``PATCH``). Nếu *body* là một string hoặc một đối tượng giống bytes nhưng không đồng thời là một
   :term:`file <file object>`, header Content-Length được đặt bằng độ dài của nó. Mọi kiểu *body* khác (file và iterable nói chung) sẽ được mã hóa theo chunk, còn header Transfer-Encoding sẽ tự động được đặt thay cho Content-Length.

   Đối số *encode_chunked* chỉ có ý nghĩa khi Transfer-Encoding được chỉ định trong *headers*. Nếu *encode_chunked* là ``False``, đối tượng HTTPConnection giả định rằng toàn bộ việc encoding được xử lý bởi code gọi nó. Nếu là ``True``, body sẽ được mã hóa theo chunk.

   Ví dụ, để thực hiện một yêu cầu ``GET`` tới ``https://docs.python.org/3/``::

      >>> import http.client
      >>> host = "docs.python.org"
      >>> conn = http.client.HTTPSConnection(host)
      >>> conn.request("GET", "/3/", headers={"Host": host})
      >>> response = conn.getresponse()
      >>> print(response.status, response.reason)
      200 OK

   .. note::
      Mã hóa truyền theo chunk đã được bổ sung vào phiên bản 1.1 của giao thức HTTP. Trừ khi biết chắc máy chủ HTTP xử lý HTTP 1.1, bên gọi phải chỉ định Content-Length hoặc phải truyền một
      :class:`str` hoặc đối tượng tương tự bytes không đồng thời là tệp làm phần biểu diễn body.

   .. note::

      Lưu ý rằng bạn phải đọc toàn bộ response hoặc gọi :meth:`close` nếu :meth:`getresponse` đã phát sinh một ngoại lệ không phải :exc:`ConnectionError` trước khi có thể gửi yêu cầu mới đến máy chủ.

   .. versionchanged:: 3.2
      *body* giờ đây có thể là một iterable.

   .. versionchanged:: 3.6
      Nếu cả Content-Length lẫn Transfer-Encoding đều không được đặt trong *headers*, các đối tượng *body* dạng tệp và iterable hiện được mã hóa theo chunk. Đã bổ sung đối số *encode_chunked*. Không có nỗ lực nào được thực hiện để xác định Content-Length cho các đối tượng tệp.

.. method:: HTTPConnection.getresponse()

   Nên được gọi sau khi gửi một request để nhận response từ máy chủ. Trả về một instance :class:`HTTPResponse`.

   .. versionchanged:: 3.5
      Nếu một :exc:`ConnectionError` hoặc lớp con được phát sinh, đối tượng
      :class:`HTTPConnection` sẽ sẵn sàng kết nối lại khi một request mới được gửi.

      Lưu ý rằng điều này không áp dụng cho :exc:`OSError`\s được phát sinh bởi socket bên dưới. Thay vào đó, caller chịu trách nhiệm gọi :meth:`close` trên connection hiện có.


.. method:: HTTPConnection.set_debuglevel(level)

   Đặt mức debugging. Mức debug mặc định là ``0``, nghĩa là không in output debugging nào. Bất kỳ giá trị nào lớn hơn ``0`` sẽ khiến tất cả output debugging hiện được định nghĩa được in ra stdout. ``debuglevel`` được truyền cho mọi đối tượng :class:`HTTPResponse` mới được tạo.

   .. versionadded:: 3.1


.. method:: HTTPConnection.set_tunnel(host, port=None, headers=None)

   Đặt host và port cho HTTP Connect Tunnelling. Điều này cho phép chạy connection thông qua proxy server.

   Các đối số *host* và *port* chỉ định endpoint của connection được tunnel (tức là địa chỉ được đưa vào request CONNECT, *không phải* địa chỉ của proxy server).

   Đối số *headers* phải là một mapping gồm các HTTP header bổ sung cần gửi cùng request CONNECT.

   Vì HTTP/1.1 được sử dụng cho yêu cầu tunnelling HTTP CONNECT, `theo RFC <https://datatracker.ietf.org/doc/html/rfc7231#section-4.3.6>`_, một HTTP ``Host:`` header phải được cung cấp, khớp với dạng authority-form của request target được cung cấp làm đích cho yêu cầu CONNECT. Nếu không cung cấp HTTP ``Host:`` header thông qua đối số headers, một header sẽ được tự động tạo và truyền đi.

   Ví dụ, để tunnelling qua một HTTPS proxy server đang chạy cục bộ trên cổng 8080, chúng ta sẽ truyền địa chỉ của proxy cho constructor :class:`HTTPSConnection`, và địa chỉ của host mà cuối cùng chúng ta muốn truy cập cho method :meth:`~HTTPConnection.set_tunnel`::

      >>> import http.client
      >>> conn = http.client.HTTPSConnection("localhost", 8080)
      >>> conn.set_tunnel("www.python.org")
      >>> conn.request("HEAD","/index.html")

   .. versionadded:: 3.2

   .. versionchanged:: 3.12
      Các yêu cầu HTTP CONNECT tunnelling sử dụng protocol HTTP/1.1, được nâng cấp từ protocol HTTP/1.0. ``Host:`` HTTP headers là bắt buộc đối với HTTP/1.1, vì vậy một header sẽ được tự động tạo và truyền đi nếu không được cung cấp trong đối số headers.


.. method:: HTTPConnection.get_proxy_response_headers()

   Trả về một dictionary chứa các headers của response nhận được từ proxy server cho yêu cầu CONNECT.

   Nếu yêu cầu CONNECT chưa được gửi, method sẽ trả về ``None``.

   .. versionadded:: 3.12


.. method:: HTTPConnection.connect()

   Kết nối đến server được chỉ định khi object được tạo. Theo mặc định, thao tác này được tự động gọi khi thực hiện request nếu client chưa có kết nối.

   .. audit-event:: http.client.connect self,host,port http.client.HTTPConnection.connect


.. method:: HTTPConnection.close()

   Đóng kết nối đến server.


.. attribute:: HTTPConnection.blocksize

   Kích thước bộ đệm tính bằng byte để gửi phần thân thông báo dạng tệp.

   .. versionadded:: 3.7


Ngoài việc sử dụng phương thức :meth:`~HTTPConnection.request` được mô tả ở trên, bạn cũng có thể gửi yêu cầu từng bước bằng cách sử dụng bốn hàm dưới đây.


.. method:: HTTPConnection.putrequest(method, url, skip_host=False, \
                                      skip_accept_encoding=False)

   Đây phải là lời gọi đầu tiên sau khi đã thiết lập kết nối với máy chủ. Lời gọi này gửi một dòng đến máy chủ, bao gồm chuỗi *method*, chuỗi *url* và phiên bản HTTP (``HTTP/1.1``). Để tắt việc tự động gửi các header ``Host:`` hoặc ``Accept-Encoding:`` (ví dụ: để chấp nhận các content encoding bổ sung), hãy chỉ định *skip_host* hoặc *skip_accept_encoding* với các giá trị khác False.


.. method:: HTTPConnection.putheader(header, argument[, ...])

   Gửi một header kiểu :rfc:`822`\  đến máy chủ. Lời gọi này gửi một dòng đến máy chủ, bao gồm header, dấu hai chấm và một khoảng trắng, rồi đến đối số đầu tiên. Nếu có thêm đối số, các dòng tiếp nối sẽ được gửi, mỗi dòng bao gồm một tab và một đối số.


.. method:: HTTPConnection.endheaders(message_body=None, *, encode_chunked=False)

   Gửi một dòng trống đến máy chủ để báo hiệu kết thúc các header. Có thể sử dụng đối số tùy chọn *message_body* để truyền phần thân thông báo gắn với yêu cầu.

   Nếu *encode_chunked* là ``True``, kết quả của mỗi lần lặp qua *message_body* sẽ được mã hóa theo từng chunk như quy định trong :rfc:`7230`, Mục 3.3.1. Cách mã hóa dữ liệu phụ thuộc vào kiểu của *message_body*. Nếu *message_body* triển khai :ref:`buffer interface <bufferobjects>` thì việc mã hóa sẽ tạo ra một chunk duy nhất. Nếu *message_body* là một :class:`collections.abc.Iterable`, mỗi lần lặp qua *message_body* sẽ tạo ra một chunk. Nếu *message_body* là một
   :term:`file object`, mỗi lần gọi ``.read()`` sẽ tạo ra một chunk. Phương thức này tự động báo hiệu kết thúc dữ liệu được mã hóa theo chunk ngay sau *message_body*.

   .. note:: Theo đặc tả mã hóa theo chunk, các chunk rỗng do một iterator body tạo ra sẽ bị chunk-encoder bỏ qua. Điều này nhằm tránh việc máy chủ đích kết thúc sớm quá trình đọc request do mã hóa không đúng định dạng.

   .. versionchanged:: 3.6
      Đã bổ sung hỗ trợ mã hóa theo chunk và tham số *encode_chunked*.


.. method:: HTTPConnection.send(data)

   Gửi dữ liệu đến máy chủ. Chỉ nên sử dụng trực tiếp thao tác này sau khi
   phương thức :meth:`endheaders` đã được gọi và trước khi gọi :meth:`getresponse`.

   .. audit-event:: http.client.send self,data http.client.HTTPConnection.send


.. _httpresponse-objects:

HTTPResponse Objects
--------------------

Một instance :class:`HTTPResponse` bọc response HTTP từ máy chủ. Nó cung cấp quyền truy cập vào các request header và entity body. Response là một iterable object và có thể được sử dụng trong câu lệnh with.

.. versionchanged:: 3.5
   Giao diện :class:`io.BufferedIOBase` hiện đã được triển khai và tất cả thao tác đọc của giao diện đều được hỗ trợ.


.. method:: HTTPResponse.read([amt])

   Đọc và trả về phần thân phản hồi, hoặc tối đa *amt* byte tiếp theo.

.. method:: HTTPResponse.readinto(b)

   Đọc tối đa len(b) byte tiếp theo của phần thân phản hồi vào bộ đệm *b*. Trả về số byte đã đọc.

   .. versionadded:: 3.3

.. method:: HTTPResponse.getheader(name, default=None)

   Trả về giá trị của header *name*, hoặc *default* nếu không có header nào khớp với *name*. Nếu có nhiều header có tên *name*, trả về tất cả các giá trị, được nối bằng ', '. Nếu *default* là bất kỳ iterable nào không phải một chuỗi đơn, các phần tử của nó cũng được trả về bằng cách nối chúng bằng dấu phẩy.

.. method:: HTTPResponse.getheaders()

   Trả về danh sách các tuple (header, value).

.. method:: HTTPResponse.fileno()

   Trả về ``fileno`` của socket bên dưới.

.. attribute:: HTTPResponse.msg

   Một instance :class:`http.client.HTTPMessage` chứa các header của phản hồi. :class:`http.client.HTTPMessage` là một lớp con của
   :class:`email.message.Message`.

.. attribute:: HTTPResponse.version

   Phiên bản giao thức HTTP được máy chủ sử dụng.  10 cho HTTP/1.0, 11 cho HTTP/1.1.

.. attribute:: HTTPResponse.url

   URL của tài nguyên đã truy xuất, thường được dùng để xác định xem có chuyển hướng hay không.

.. attribute:: HTTPResponse.headers

   Các header của response dưới dạng một instance :class:`email.message.EmailMessage`.

.. attribute:: HTTPResponse.status

   Mã trạng thái do máy chủ trả về.

.. attribute:: HTTPResponse.reason

   Cụm từ lý do do máy chủ trả về.

.. attribute:: HTTPResponse.debuglevel

   Một hook dùng để debug.  Nếu :attr:`debuglevel` lớn hơn 0, các thông báo sẽ được in ra stdout khi response được đọc và phân tích cú pháp.

.. attribute:: HTTPResponse.closed

   Là ``True`` nếu stream đã đóng.

.. method:: HTTPResponse.geturl()

   .. deprecated:: 3.9
      Không dùng nữa, thay vào đó sử dụng :attr:`~HTTPResponse.url`.

.. method:: HTTPResponse.info()

   .. deprecated:: 3.9
      Không dùng nữa, thay vào đó sử dụng :attr:`~HTTPResponse.headers`.

.. method:: HTTPResponse.getcode()

   .. deprecated:: 3.9
      Không dùng nữa, thay vào đó sử dụng :attr:`~HTTPResponse.status`.

Ví dụ
-----

Sau đây là một phiên làm việc ví dụ sử dụng phương thức ``GET``::

   >>> import http.client
   >>> conn = http.client.HTTPSConnection("www.python.org")
   >>> conn.request("GET", "/")
   >>> r1 = conn.getresponse()
   >>> print(r1.status, r1.reason)
   200 OK
   >>> data1 = r1.read()  # Lệnh này sẽ trả về toàn bộ nội dung.
   >>> # Ví dụ sau minh họa cách đọc dữ liệu theo từng phần.
   >>> conn.request("GET", "/")
   >>> r1 = conn.getresponse()
   >>> while chunk := r1.read(200):
   ...     print(repr(chunk))
   b'<!doctype html>\n<!--[if"...
   ...
   >>> # Ví dụ về một yêu cầu không hợp lệ
   >>> conn = http.client.HTTPSConnection("docs.python.org")
   >>> conn.request("GET", "/parrot.spam")
   >>> r2 = conn.getresponse()
   >>> print(r2.status, r2.reason)
   404 Not Found
   >>> data2 = r2.read()
   >>> conn.close()

Sau đây là một phiên làm việc mẫu sử dụng phương thức ``HEAD``. Lưu ý rằng phương thức ``HEAD`` không bao giờ trả về dữ liệu nào.::

   >>> import http.client
   >>> conn = http.client.HTTPSConnection("www.python.org")
   >>> conn.request("HEAD", "/")
   >>> res = conn.getresponse()
   >>> print(res.status, res.reason)
   200 OK
   >>> data = res.read()
   >>> print(len(data))
   0
   >>> data == b''
   True

Sau đây là một phiên làm việc mẫu sử dụng phương thức ``POST``::

   >>> import http.client, urllib.parse
   >>> params = urllib.parse.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})
   >>> headers = {"Content-type": "application/x-www-form-urlencoded",
   ...            "Accept": "text/plain"}
   >>> conn = http.client.HTTPConnection("bugs.python.org")
   >>> conn.request("POST", "", params, headers)
   >>> response = conn.getresponse()
   >>> print(response.status, response.reason)
   302 Found
   >>> data = response.read()
   >>> data
   b'Redirecting to <a href="https://bugs.python.org/issue12524">https://bugs.python.org/issue12524</a>'
   >>> conn.close()

Các yêu cầu HTTP ``PUT`` phía máy khách rất giống với các yêu cầu ``POST``. Điểm khác biệt chỉ nằm ở phía máy chủ, nơi các máy chủ HTTP cho phép tạo tài nguyên thông qua các yêu cầu ``PUT``. Cần lưu ý rằng các phương thức HTTP tùy chỉnh cũng được xử lý trong :class:`urllib.request.Request` bằng cách đặt thuộc tính method thích hợp. Sau đây là một phiên làm việc mẫu sử dụng phương thức ``PUT``::

    >>> # Điều này tạo một yêu cầu HTTP
    >>> # với nội dung của BODY làm biểu diễn được đính kèm
    >>> # cho tài nguyên http://localhost:8080/file
    ...
    >>> import http.client
    >>> BODY = "***filecontents***"
    >>> conn = http.client.HTTPConnection("localhost", 8080)
    >>> conn.request("PUT", "/file", BODY)
    >>> response = conn.getresponse()
    >>> print(response.status, response.reason)
    200, OK

.. _httpmessage-objects:

Đối tượng HTTPMessage
---------------------

.. class:: HTTPMessage(email.message.Message)

Một thực thể :class:`http.client.HTTPMessage` chứa các header từ một phản hồi HTTP. Nó được triển khai bằng lớp :class:`email.message.Message`.

.. XXX Define the methods that clients can depend upon between versions.

.. _`Requests package`: https://requests.readthedocs.io/en/latest/
.. _`as per the RFC`: https://datatracker.ietf.org/doc/html/rfc7231#section-4.3.6
