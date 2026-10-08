:mod:`!wsgiref` --- Tiện ích WSGI và Triển khai Tham chiếu
==========================================================

.. module:: wsgiref
   :synopsis: Tiện ích WSGI và Triển khai Tham chiếu.

.. moduleauthor:: Phillip J. Eby <pje@telecommunity.com>
.. sectionauthor:: Phillip J. Eby <pje@telecommunity.com>

**Mã nguồn:** :source:`Lib/wsgiref`

--------------

.. warning::

   :mod:`!wsgiref` là một triển khai tham chiếu và không được khuyến nghị dùng trong môi trường production. Mô-đun này chỉ thực hiện các kiểm tra bảo mật cơ bản.

Web Server Gateway Interface (WSGI) là một interface tiêu chuẩn giữa phần mềm web server và các web application được viết bằng Python. Việc có một interface tiêu chuẩn giúp dễ dàng sử dụng một application hỗ trợ WSGI với nhiều web server khác nhau.

Chỉ tác giả của web server và programming framework mới cần biết mọi chi tiết và trường hợp đặc biệt trong thiết kế WSGI. Bạn không cần hiểu mọi chi tiết của WSGI chỉ để cài đặt một WSGI application hoặc viết một web application bằng framework hiện có.

:mod:`!wsgiref` là một triển khai tham chiếu của đặc tả WSGI, có thể được dùng để bổ sung hỗ trợ WSGI cho web server hoặc framework. Nó cung cấp các tiện ích để thao tác với các biến môi trường WSGI và response header, các base class để triển khai WSGI server, một HTTP server demo phục vụ các WSGI application, các type dùng cho static type checking, và một công cụ validation để kiểm tra WSGI server và application có tuân thủ đặc tả WSGI hay không (:pep:`3333`).

Xem `wsgi.readthedocs.io <https://wsgi.readthedocs.io/>`_ để biết thêm thông tin về WSGI, cùng các liên kết đến hướng dẫn và những tài nguyên khác.

.. XXX If you're just trying to write a web application...


:mod:`!wsgiref.util` -- các tiện ích môi trường WSGI
----------------------------------------------------

.. module:: wsgiref.util
   :synopsis: Các tiện ích môi trường WSGI.


Mô-đun này cung cấp nhiều hàm tiện ích để làm việc với các môi trường WSGI. Môi trường WSGI là một dictionary chứa các biến của HTTP request như được mô tả trong :pep:`3333`. Tất cả các hàm nhận tham số *environ* đều yêu cầu cung cấp một dictionary tuân thủ WSGI; vui lòng xem
:pep:`3333` để biết đặc tả chi tiết và
:data:`~wsgiref.types.WSGIEnvironment` để biết bí danh kiểu có thể dùng trong type annotations.


.. function:: guess_scheme(environ)

   Trả về dự đoán về việc ``wsgi.url_scheme`` nên là "http" hay "https", bằng cách kiểm tra biến môi trường ``HTTPS`` trong dictionary *environ*. Giá trị trả về là một chuỗi.

   Hàm này hữu ích khi tạo một gateway bao bọc CGI hoặc một giao thức tương tự CGI chẳng hạn như FastCGI. Thông thường, các máy chủ cung cấp những giao thức như vậy sẽ bao gồm một biến ``HTTPS`` có giá trị là "1", "yes" hoặc "on" khi nhận được một request qua SSL. Vì vậy, hàm này trả về "https" nếu tìm thấy giá trị như vậy và trả về "http" trong trường hợp ngược lại.


.. function:: request_uri(environ, include_query=True)

   Trả về URI đầy đủ của request, có thể bao gồm query string, bằng thuật toán được nêu trong phần "URL Reconstruction" của :pep:`3333`. Nếu *include_query* là false, query string sẽ không được đưa vào URI kết quả.


.. function:: application_uri(environ)

   Tương tự như :func:`request_uri`, ngoại trừ việc các biến ``PATH_INFO`` và ``QUERY_STRING`` bị bỏ qua. Kết quả là URI cơ sở của application object được request định địa chỉ.


.. function:: shift_path_info(environ)

   Chuyển một name duy nhất từ ``PATH_INFO`` sang ``SCRIPT_NAME`` rồi trả về name đó. Dictionary *environ* được *sửa đổi* ngay tại chỗ; hãy sử dụng một bản sao nếu bạn cần giữ nguyên ``PATH_INFO`` hoặc ``SCRIPT_NAME`` ban đầu.

   Nếu không còn path segment nào trong ``PATH_INFO``, ``None`` sẽ được trả về.

   Thông thường, routine này được dùng để xử lý từng phần của path trong URI của request, chẳng hạn như coi path là một chuỗi dictionary key. Routine này sửa đổi environment được truyền vào để environment phù hợp với việc gọi một WSGI application khác nằm tại target URI. Ví dụ, nếu có một WSGI application tại ``/foo``, path trong URI của request là ``/foo/bar/baz``, và WSGI application tại ``/foo`` gọi :func:`shift_path_info`, application đó sẽ nhận được chuỗi "bar", còn environment sẽ được cập nhật để phù hợp với việc truyền vào một WSGI application tại ``/foo/bar``. Nghĩa là, ``SCRIPT_NAME`` sẽ đổi từ ``/foo`` thành ``/foo/bar``, và ``PATH_INFO`` sẽ đổi từ ``/bar/baz`` thành ``/baz``.

   Khi ``PATH_INFO`` chỉ là "/", routine này trả về một chuỗi rỗng và thêm dấu gạch chéo ở cuối vào ``SCRIPT_NAME``, mặc dù các path segment rỗng thường bị bỏ qua và ``SCRIPT_NAME`` thông thường không kết thúc bằng dấu gạch chéo. Đây là hành vi có chủ ý, nhằm đảm bảo application có thể phân biệt các URI kết thúc bằng ``/x`` với những URI kết thúc bằng ``/x/`` khi sử dụng routine này để thực hiện việc duyệt object.


.. function:: setup_testing_defaults(environ)

   Cập nhật *environ* bằng các giá trị mặc định đơn giản để phục vụ việc kiểm thử.

   Routine này thêm nhiều tham số cần thiết cho WSGI, bao gồm ``HTTP_HOST``, ``SERVER_NAME``, ``SERVER_PORT``, ``REQUEST_METHOD``, ``SCRIPT_NAME``, ``PATH_INFO``, và tất cả các biến :pep:`3333`\ -defined ``wsgi.*``. Routine này chỉ cung cấp các giá trị mặc định và không thay thế bất kỳ thiết lập hiện có nào cho các biến này.

   Routine này được thiết kế để giúp việc thiết lập các environment giả cho unit test của WSGI server và application trở nên dễ dàng hơn. KHÔNG được sử dụng routine này cho WSGI server hoặc application thực tế, vì dữ liệu là giả!

   Ví dụ sử dụng (xem thêm :func:`~wsgiref.simple_server.demo_app` để biết một ví dụ khác)::

      from wsgiref.util import setup_testing_defaults
      from wsgiref.simple_server import make_server

      # Một ứng dụng WSGI tương đối đơn giản. Ứng dụng này sẽ in ra
      # từ điển environment sau khi được setup_testing_defaults cập nhật
      def simple_app(environ, start_response):
          setup_testing_defaults(environ)

          status = '200 OK'
          headers = [('Content-type', 'text/plain; charset=utf-8')]

          start_response(status, headers)

          ret = [("%s: %s\n" % (key, value)).encode("utf-8")
                 for key, value in environ.items()]
          return ret

      with make_server('', 8000, simple_app) as httpd:
          print("Serving on port 8000...")
          httpd.serve_forever()


Ngoài các hàm environment ở trên, module :mod:`!wsgiref.util` cũng cung cấp các tiện ích linh tinh sau đây:


.. function:: is_hop_by_hop(header_name)

   Trả về ``True`` nếu 'header_name' là header "Hop-by-Hop" của HTTP/1.1, như được định nghĩa bởi
   :rfc:`2616`.


.. class:: FileWrapper(filelike, blksize=8192)

   Một triển khai cụ thể của giao thức :class:`wsgiref.types.FileWrapper` được dùng để chuyển đổi một đối tượng giống tệp thành một :term:`iterator`. Các đối tượng kết quả là các :term:`iterable`\ s. Khi đối tượng được lặp qua, tham số *blksize* tùy chọn sẽ được truyền lặp lại cho phương thức *filelike* của đối tượng :meth:`read` để lấy các chuỗi byte cần trả về. Khi :meth:`read` trả về một chuỗi byte rỗng, quá trình lặp kết thúc và không thể tiếp tục.

   Nếu *filelike* có phương thức :meth:`close`, đối tượng được trả về cũng sẽ có một
   phương thức :meth:`close`, và phương thức này sẽ gọi phương thức :meth:`close` của đối tượng *filelike* khi được gọi.

   Ví dụ sử dụng::

      from io import StringIO
      from wsgiref.util import FileWrapper

      # Chúng ta đang sử dụng bộ đệm StringIO làm đối tượng giống tệp
      filelike = StringIO("This is an example file-like object"*10)
      wrapper = FileWrapper(filelike, blksize=5)

      for chunk in wrapper:
          print(chunk)

   .. versionchanged:: 3.11
      Hỗ trợ cho phương thức :meth:`~object.__getitem__` đã bị loại bỏ.


:mod:`!wsgiref.headers` -- công cụ header phản hồi WSGI
-------------------------------------------------------

.. module:: wsgiref.headers
   :synopsis: Công cụ header phản hồi WSGI.


Module này cung cấp một class duy nhất, :class:`Headers`, để thao tác thuận tiện với các header phản hồi WSGI bằng interface giống mapping.


.. class:: Headers([headers])

   Tạo một đối tượng giống mapping bao bọc *headers*, trong đó phải là một danh sách các tuple tên/giá trị header như được mô tả trong :pep:`3333`. Giá trị mặc định của *headers* là một danh sách rỗng.

   Các đối tượng :class:`Headers` hỗ trợ những thao tác mapping thông thường, bao gồm
   :meth:`~object.__getitem__`, :meth:`~dict.get`, :meth:`~object.__setitem__`,
   :meth:`~dict.setdefault`,
   :meth:`~object.__delitem__` và :meth:`~object.__contains__`. Với mỗi phương thức này, khóa là tên header (không phân biệt chữ hoa chữ thường), còn giá trị là giá trị đầu tiên được liên kết với tên header đó. Việc thiết lập một header sẽ xóa mọi giá trị hiện có của header đó, sau đó thêm một giá trị mới vào cuối danh sách header được bao bọc. Thứ tự hiện có của các header nhìn chung được duy trì, còn các header mới được thêm vào cuối danh sách được bao bọc.

   Không giống dictionary, các đối tượng :class:`Headers` không phát sinh lỗi khi bạn cố lấy hoặc xóa một khóa không có trong danh sách header được bao bọc. Việc lấy một header không tồn tại chỉ trả về ``None``, còn việc xóa một header không tồn tại sẽ không làm gì cả.

   Các đối tượng :class:`Headers` cũng hỗ trợ :meth:`keys`, :meth:`values`, và
   các phương thức :meth:`items`. Các danh sách được :meth:`keys` và :meth:`items` trả về có thể chứa cùng một khóa nhiều lần nếu có một header nhiều giá trị. ``len()`` của một đối tượng :class:`Headers` giống với độ dài của nó
   :meth:`items`, vốn cũng bằng độ dài của danh sách header được bao bọc. Thực tế, phương thức :meth:`items` chỉ trả về một bản sao của danh sách header được bao bọc.

   Việc gọi ``bytes()`` trên một đối tượng :class:`Headers` sẽ trả về một chuỗi byte đã được định dạng, phù hợp để truyền dưới dạng các header phản hồi HTTP. Mỗi header được đặt trên một dòng cùng với giá trị của nó, ngăn cách bằng dấu hai chấm và một dấu cách. Mỗi dòng kết thúc bằng ký tự xuống dòng và ký tự về đầu dòng, còn chuỗi byte kết thúc bằng một dòng trống.

   Ngoài giao diện mapping và các tính năng định dạng, các đối tượng :class:`Headers` còn có những phương thức sau để truy vấn và thêm các header nhiều giá trị, cũng như thêm các header có tham số MIME:


   .. method:: Headers.get_all(name)

      Trả về một danh sách gồm tất cả giá trị của header được chỉ định tên.

      Danh sách được trả về sẽ được sắp xếp theo thứ tự chúng xuất hiện trong danh sách header ban đầu hoặc được thêm vào instance này, và có thể chứa các giá trị trùng lặp. Mọi trường bị xóa rồi chèn lại luôn được thêm vào cuối danh sách header. Nếu không có trường nào có tên đã cho, phương thức trả về một danh sách rỗng.


   .. method:: Headers.add_header(name, value, **_params)

      Thêm một header (có thể có nhiều giá trị), với các tham số MIME tùy chọn được chỉ định qua các đối số từ khóa.

      *name* là trường header cần thêm. Có thể sử dụng các đối số từ khóa để thiết lập các tham số MIME cho trường header. Mỗi tham số phải là một chuỗi hoặc ``None``. Dấu gạch dưới trong tên tham số được chuyển thành dấu gạch ngang, vì dấu gạch ngang không hợp lệ trong mã định danh Python, nhưng nhiều tên tham số MIME lại có dấu gạch ngang. Nếu giá trị tham số là một chuỗi, tham số đó được thêm vào các tham số giá trị header theo dạng ``name="value"``. Nếu là ``None``, chỉ tên tham số được thêm vào. (Cách này được dùng cho các tham số MIME không có giá trị.) Ví dụ sử dụng::

         h.add_header('content-disposition', 'attachment', filename='bud.gif')

      Đoạn mã trên sẽ thêm một header có dạng như sau::

         Content-Disposition: attachment; filename="bud.gif"


   .. versionchanged:: 3.5
      Tham số *headers* là tùy chọn.


:mod:`!wsgiref.simple_server` -- một máy chủ HTTP WSGI đơn giản
---------------------------------------------------------------

.. module:: wsgiref.simple_server
   :synopsis: Một máy chủ HTTP WSGI đơn giản.


Mô-đun này triển khai một máy chủ HTTP đơn giản (dựa trên :mod:`http.server`) để phục vụ các ứng dụng WSGI. Mỗi phiên bản máy chủ phục vụ một ứng dụng WSGI duy nhất trên một host và port cụ thể. Nếu muốn phục vụ nhiều ứng dụng trên cùng một host và port, bạn nên tạo một ứng dụng WSGI phân tích ``PATH_INFO`` để chọn ứng dụng nào sẽ được gọi cho từng request. (Ví dụ: sử dụng hàm :func:`shift_path_info` từ
:mod:`wsgiref.util`.)


.. function:: make_server(host, port, app, server_class=WSGIServer, handler_class=WSGIRequestHandler)

   Tạo một máy chủ WSGI mới lắng nghe trên *host* và *port*, chấp nhận các kết nối cho *app*. Giá trị trả về là một instance của *server_class* được cung cấp và sẽ xử lý các yêu cầu bằng *handler_class* được chỉ định. *app* phải là một đối tượng WSGI application, như được định nghĩa bởi :pep:`3333`.

   Ví dụ sử dụng::

      from wsgiref.simple_server import make_server, demo_app

      with make_server('', 8000, demo_app) as httpd:
          print("Serving HTTP on port 8000...")

          # Phản hồi các yêu cầu cho đến khi tiến trình bị kết thúc
          httpd.serve_forever()

          # Cách khác: phục vụ một yêu cầu rồi thoát
          httpd.handle_request()


.. function:: demo_app(environ, start_response)

   Hàm này là một WSGI application nhỏ nhưng hoàn chỉnh, trả về một trang văn bản chứa thông báo "Hello world!" và danh sách các cặp key/value được cung cấp trong tham số *environ*. Hàm này hữu ích để xác minh rằng một máy chủ WSGI (chẳng hạn như :mod:`!wsgiref.simple_server`) có thể chạy đúng cách một WSGI application đơn giản.

   Callable *start_response* phải tuân theo :class:`.StartResponse` protocol.


.. class:: WSGIServer(server_address, RequestHandlerClass)

   Tạo một instance :class:`WSGIServer`. *server_address* phải là một tuple ``(host,port)``, còn *RequestHandlerClass* phải là lớp con của
   :class:`http.server.BaseHTTPRequestHandler` sẽ được sử dụng để xử lý các request.

   Bạn thường không cần gọi constructor này, vì hàm :func:`make_server` có thể tự xử lý mọi chi tiết cho bạn.

   :class:`WSGIServer` là một lớp con của :class:`http.server.HTTPServer`, vì vậy tất cả các phương thức của nó (chẳng hạn như :meth:`serve_forever` và :meth:`handle_request`) đều khả dụng. :class:`WSGIServer` cũng cung cấp các phương thức dành riêng cho WSGI sau:


   .. method:: WSGIServer.set_app(application)

      Thiết lập callable *application* làm ứng dụng WSGI sẽ nhận các request.


   .. method:: WSGIServer.get_app()

      Trả về application callable hiện được thiết lập.

   Tuy nhiên, thông thường bạn không cần sử dụng các phương thức bổ sung này, vì
   :meth:`set_app` thường được :func:`make_server` gọi, và
   :meth:`get_app` chủ yếu tồn tại để phục vụ các instance của request handler.


.. class:: WSGIRequestHandler(request, client_address, server)

   Tạo một HTTP handler cho *request* đã cho (tức là một socket), *client_address* (một tuple ``(host,port)``) và *server* (một instance :class:`WSGIServer`).

   Bạn không cần trực tiếp tạo các instance của class này; chúng sẽ tự động được tạo khi cần bởi các object :class:`WSGIServer`. Tuy nhiên, bạn có thể subclass class này và cung cấp nó làm *handler_class* cho
   hàm :func:`make_server`. Một số method có thể cần override trong các subclass:


   .. method:: WSGIRequestHandler.get_environ()

      Trả về một dictionary :data:`~wsgiref.types.WSGIEnvironment` cho một request. Implementation mặc định sao chép nội dung của thuộc tính dictionary :class:`WSGIServer` của object
      :attr:`base_environ` rồi thêm nhiều header khác nhau được suy ra từ HTTP request. Mỗi lần gọi method này phải trả về một dictionary mới chứa tất cả biến môi trường CGI liên quan như được chỉ định trong
      :pep:`3333`.


   .. method:: WSGIRequestHandler.get_stderr()

      Trả về object sẽ được sử dụng làm stream ``wsgi.errors``. Implementation mặc định chỉ trả về ``sys.stderr``.


   .. method:: WSGIRequestHandler.handle()

      Xử lý yêu cầu HTTP. Bản triển khai mặc định tạo một thực thể handler bằng cách sử dụng một lớp :mod:`wsgiref.handlers` để triển khai giao diện ứng dụng WSGI thực tế.


:mod:`!wsgiref.validate` --- trình kiểm tra tính tuân thủ WSGI
--------------------------------------------------------------

.. module:: wsgiref.validate
   :synopsis: Trình kiểm tra tính tuân thủ WSGI.


Khi tạo các đối tượng ứng dụng WSGI, framework, server hoặc middleware mới, việc xác thực tính tuân thủ của mã mới bằng cách sử dụng
:mod:`!wsgiref.validate` rất hữu ích. Mô-đun này cung cấp một hàm tạo các đối tượng ứng dụng WSGI để xác thực quá trình giao tiếp giữa một server hoặc gateway WSGI và một đối tượng ứng dụng WSGI, nhằm kiểm tra tính tuân thủ giao thức của cả hai phía.

Lưu ý rằng tiện ích này không đảm bảo tính tuân thủ :pep:`3333` hoàn toàn; việc mô-đun này không phát hiện lỗi không nhất thiết có nghĩa là không tồn tại lỗi. Tuy nhiên, nếu mô-đun này tạo ra một lỗi thì gần như chắc chắn server hoặc ứng dụng không tuân thủ 100%.

Mô-đun này dựa trên mô-đun :mod:`paste.lint` trong thư viện "Python Paste" của Ian Bicking.


.. function:: validator(application)

   Bọc *application* và trả về một đối tượng WSGI application mới. Application được trả về sẽ chuyển tiếp mọi request đến *application* ban đầu, đồng thời kiểm tra để bảo đảm cả *application* và server gọi nó đều tuân thủ đặc tả WSGI và :rfc:`2616`.

   Mọi trường hợp không tuân thủ được phát hiện sẽ khiến một :exc:`AssertionError` được raise; tuy nhiên, lưu ý rằng cách các lỗi này được xử lý phụ thuộc vào server. Ví dụ, :mod:`wsgiref.simple_server` và các server khác dựa trên
   :mod:`wsgiref.handlers` (không override các phương thức xử lý lỗi để thực hiện việc khác) sẽ chỉ đơn giản xuất ra thông báo rằng đã xảy ra lỗi và ghi traceback vào ``sys.stderr`` hoặc một error stream khác.

   Wrapper này cũng có thể tạo output bằng module :mod:`warnings` để chỉ ra những hành vi đáng ngờ nhưng có thể thực tế không bị :pep:`3333` cấm. Trừ khi bị vô hiệu hóa bằng các tùy chọn dòng lệnh của Python hoặc API :mod:`warnings`, mọi warning như vậy sẽ được ghi vào ``sys.stderr`` (*không phải* ``wsgi.errors``, trừ khi chúng tình cờ là cùng một object).

   Ví dụ sử dụng::

      from wsgiref.validate import validator
      from wsgiref.simple_server import make_server

      # Đối tượng callable của chúng ta cố ý không tuân thủ
      # chuẩn, nên validator sẽ bị lỗi
      def simple_app(environ, start_response):
          status = '200 OK'  # Trạng thái HTTP
          headers = [('Content-type', 'text/plain')]  # Tiêu đề HTTP
          start_response(status, headers)

          # Điều này sẽ gây lỗi vì chúng ta cần trả về một danh sách, và
          # trình xác thực sẽ thông báo cho chúng ta
          return b"Hello World"

      # Đây là ứng dụng được bọc trong một trình xác thực
      validator_app = validator(simple_app)

      with make_server('', 8000, validator_app) as httpd:
          print("Listening on port 8000....")
          httpd.serve_forever()


:mod:`!wsgiref.handlers` -- các lớp cơ sở của server/gateway
------------------------------------------------------------

.. module:: wsgiref.handlers
   :synopsis: Các lớp cơ sở của server/gateway WSGI.


Mô-đun này cung cấp các lớp handler cơ sở để triển khai WSGI server và gateway. Các lớp cơ sở này xử lý phần lớn công việc giao tiếp với một ứng dụng WSGI, miễn là chúng được cung cấp một môi trường tương tự CGI, cùng với các stream đầu vào, đầu ra và lỗi.


.. class:: CGIHandler()

   Gọi thực thi dựa trên CGI thông qua ``sys.stdin``, ``sys.stdout``, ``sys.stderr`` và ``os.environ``. Điều này hữu ích khi bạn có một ứng dụng WSGI và muốn chạy ứng dụng đó dưới dạng một CGI script. Chỉ cần gọi ``CGIHandler().run(app)``, trong đó ``app`` là đối tượng ứng dụng WSGI mà bạn muốn gọi.

   Lớp này là một lớp con của :class:`BaseCGIHandler`, đặt ``wsgi.run_once`` thành true, ``wsgi.multithread`` thành false và ``wsgi.multiprocess`` thành true, đồng thời luôn sử dụng :mod:`sys` và :mod:`os` để lấy các stream CGI và môi trường cần thiết.


.. class:: IISCGIHandler()

   Một lựa chọn chuyên biệt thay thế cho :class:`CGIHandler`, dùng khi triển khai trên web server IIS của Microsoft mà chưa thiết lập tùy chọn cấu hình allowPathInfo (IIS>=7) hoặc metabase allowPathInfoForScriptMappings (IIS<7).

   Theo mặc định, IIS cung cấp một ``PATH_INFO`` trùng lặp với ``SCRIPT_NAME`` ở phía trước, gây ra sự cố cho các ứng dụng WSGI muốn triển khai routing. Handler này loại bỏ mọi path bị trùng lặp như vậy.

   IIS có thể được cấu hình để truyền ``PATH_INFO`` chính xác, nhưng điều này lại gây ra một lỗi khác, khiến ``PATH_TRANSLATED`` không chính xác. May mắn là biến này hiếm khi được sử dụng và không được WSGI đảm bảo. Tuy nhiên, trên IIS<7, thiết lập này chỉ có thể được thực hiện ở cấp vhost, ảnh hưởng đến tất cả script mapping khác, nhiều trong số đó sẽ bị lỗi khi gặp lỗi ``PATH_TRANSLATED``. Vì lý do này, IIS<7 hầu như không bao giờ được triển khai cùng bản sửa lỗi (Ngay cả IIS7 cũng hiếm khi sử dụng nó vì vẫn chưa có UI cho thiết lập này.).

   Không có cách nào để mã CGI biết tùy chọn đó đã được thiết lập hay chưa, vì vậy một lớp handler riêng được cung cấp. Lớp này được sử dụng theo cùng cách như
   :class:`CGIHandler`, tức là bằng cách gọi ``IISCGIHandler().run(app)``, trong đó ``app`` là đối tượng ứng dụng WSGI mà bạn muốn gọi.

   .. versionadded:: 3.2


.. class:: BaseCGIHandler(stdin, stdout, stderr, environ, multithread=True, multiprocess=False)

   Tương tự như :class:`CGIHandler`, nhưng thay vì sử dụng :mod:`sys` và
   các mô-đun :mod:`os`, môi trường CGI và các luồng I/O được chỉ định một cách rõ ràng. Các giá trị *multithread* và *multiprocess* được dùng để thiết lập các cờ ``wsgi.multithread`` và ``wsgi.multiprocess`` cho mọi ứng dụng do thực thể handler chạy.

   Lớp này là lớp con của :class:`SimpleHandler`, предназначена để sử dụng với phần mềm khác với các "origin server" HTTP. Nếu bạn đang viết một triển khai giao thức gateway (chẳng hạn như CGI, FastCGI, SCGI, v.v.) sử dụng header ``Status:`` để gửi trạng thái HTTP, có lẽ bạn nên tạo lớp con từ lớp này thay vì từ :class:`SimpleHandler`.


.. class:: SimpleHandler(stdin, stdout, stderr, environ, multithread=True, multiprocess=False)

   Tương tự như :class:`BaseCGIHandler`, nhưng được thiết kế để sử dụng với các origin server HTTP. Nếu bạn đang viết một triển khai HTTP server, có lẽ bạn nên tạo lớp con từ lớp này thay vì từ :class:`BaseCGIHandler`.

   Lớp này là lớp con của :class:`BaseHandler`. Lớp này ghi đè các
   :meth:`!__init__`, :meth:`~BaseHandler.get_stdin`,
   :meth:`~BaseHandler.get_stderr`, :meth:`~BaseHandler.add_cgi_vars`,
   phương thức :meth:`~BaseHandler._write` và :meth:`~BaseHandler._flush` để hỗ trợ việc thiết lập rõ ràng environment và các stream thông qua constructor. Environment và các stream được cung cấp được lưu trong :attr:`stdin`, :attr:`stdout`, :attr:`stderr`, và
   Các thuộc tính :attr:`environ`.

   Phương thức :meth:`~io.BufferedIOBase.write` của *stdout* phải ghi đầy đủ từng khối, giống như :class:`io.BufferedIOBase`.


.. class:: BaseHandler()

   Đây là một lớp cơ sở trừu tượng để chạy các ứng dụng WSGI. Mỗi instance sẽ xử lý một HTTP request, mặc dù về nguyên tắc bạn có thể tạo một subclass có thể tái sử dụng cho nhiều request.

   Các instance :class:`BaseHandler` chỉ có một phương thức dành cho việc sử dụng bên ngoài:


   .. method:: BaseHandler.run(app)

      Chạy ứng dụng WSGI được chỉ định, *app*.

   Tất cả các phương thức :class:`BaseHandler` khác đều được phương thức này gọi trong quá trình chạy ứng dụng, vì vậy chúng chủ yếu tồn tại để cho phép tùy chỉnh quy trình.

   Các phương thức sau PHẢI được ghi đè trong một subclass:


   .. method:: BaseHandler._write(data)

      Đệm các byte *data* để truyền đến client. Việc phương thức này thực sự truyền dữ liệu cũng không sao; :class:`BaseHandler` chỉ tách các thao tác ghi và flush để đạt hiệu quả cao hơn khi hệ thống nền tảng thực sự có sự phân biệt như vậy.


   .. method:: BaseHandler._flush()

      Buộc dữ liệu đã đệm được truyền đến client. Việc phương thức này không thực hiện thao tác nào cũng không sao (tức là nếu :meth:`_write` thực sự gửi dữ liệu).


   .. method:: BaseHandler.get_stdin()

      Trả về một đối tượng tương thích với :class:`~wsgiref.types.InputStream`, phù hợp để dùng làm ``wsgi.input`` của request hiện đang được xử lý.


   .. method:: BaseHandler.get_stderr()

      Trả về một đối tượng tương thích với :class:`~wsgiref.types.ErrorStream`, phù hợp để dùng làm ``wsgi.errors`` của request hiện đang được xử lý.


   .. method:: BaseHandler.add_cgi_vars()

      Chèn các biến CGI của request hiện tại vào thuộc tính :attr:`environ`.

   Dưới đây là một số phương thức và thuộc tính khác mà bạn có thể muốn ghi đè. Tuy nhiên, đây chỉ là bản tóm tắt và không bao gồm mọi phương thức có thể được ghi đè. Bạn nên tham khảo docstring và mã nguồn để biết thêm thông tin trước khi thử tạo một subclass :class:`BaseHandler` tùy chỉnh.

   Các thuộc tính và phương thức để tùy chỉnh môi trường WSGI:


   .. attribute:: BaseHandler.wsgi_multithread

      Giá trị được sử dụng cho biến môi trường ``wsgi.multithread``. Giá trị mặc định là true trong :class:`BaseHandler`, nhưng có thể có giá trị mặc định khác (hoặc được đặt bởi constructor) trong các lớp con khác.


   .. attribute:: BaseHandler.wsgi_multiprocess

      Giá trị được sử dụng cho biến môi trường ``wsgi.multiprocess``. Giá trị mặc định là true trong :class:`BaseHandler`, nhưng có thể có giá trị mặc định khác (hoặc được đặt bởi constructor) trong các lớp con khác.


   .. attribute:: BaseHandler.wsgi_run_once

      Giá trị được sử dụng cho biến môi trường ``wsgi.run_once``. Giá trị mặc định là false trong :class:`BaseHandler`, nhưng :class:`CGIHandler` đặt giá trị mặc định là true.


   .. attribute:: BaseHandler.os_environ

      Các biến môi trường mặc định được đưa vào môi trường WSGI của mọi request. Theo mặc định, đây là một bản sao của ``os.environ`` tại thời điểm
      :mod:`!wsgiref.handlers` được import, nhưng các lớp con có thể tạo biến riêng ở cấp lớp hoặc cấp instance. Lưu ý rằng dictionary này nên được xem là chỉ đọc, vì giá trị mặc định được chia sẻ giữa nhiều lớp và instance.


   .. attribute:: BaseHandler.server_software

      Nếu thuộc tính :attr:`origin_server` được thiết lập, giá trị của thuộc tính này được dùng để đặt biến môi trường WSGI ``SERVER_SOFTWARE`` mặc định, đồng thời đặt header ``Server:`` mặc định trong các response HTTP. Thuộc tính này bị bỏ qua đối với các handler (chẳng hạn như :class:`BaseCGIHandler` và :class:`CGIHandler`) không phải là origin server HTTP.

      .. versionchanged:: 3.3
         Thuật ngữ "Python" được thay thế bằng thuật ngữ riêng của từng implementation, chẳng hạn như "CPython", "Jython", v.v.

   .. method:: BaseHandler.get_scheme()

      Trả về lược đồ URL đang được sử dụng cho request hiện tại. Cài đặt mặc định sử dụng hàm :func:`guess_scheme` từ :mod:`wsgiref.util` để đoán xem lược đồ nên là "http" hay "https", dựa trên các biến :attr:`environ` của request hiện tại.


   .. method:: BaseHandler.setup_environ()

      Đặt thuộc tính :attr:`environ` thành một môi trường WSGI được điền đầy đủ. Cài đặt mặc định sử dụng tất cả các phương thức và thuộc tính nêu trên, cùng với
      các phương thức :meth:`get_stdin`, :meth:`get_stderr` và :meth:`add_cgi_vars`, cùng với
      thuộc tính :attr:`wsgi_file_wrapper`. Nó cũng chèn khóa ``SERVER_SOFTWARE`` nếu khóa này chưa tồn tại, miễn là thuộc tính :attr:`origin_server` có giá trị true và thuộc tính :attr:`server_software` đã được thiết lập.

   Các phương thức và thuộc tính dùng để tùy chỉnh việc xử lý ngoại lệ:


   .. method:: BaseHandler.log_exception(exc_info)

      Ghi tuple *exc_info* vào server log. *exc_info* là một tuple ``(type, value, traceback)``. Cài đặt mặc định chỉ cần ghi traceback vào stream ``wsgi.errors`` của request rồi flush stream đó. Các subclass có thể override phương thức này để thay đổi định dạng hoặc chuyển hướng đầu ra, gửi traceback qua email cho quản trị viên, hoặc thực hiện bất kỳ hành động phù hợp nào khác.


   .. attribute:: BaseHandler.traceback_limit

      Số frame tối đa cần đưa vào traceback do cài đặt mặc định xuất ra
      phương thức :meth:`log_exception`. Nếu ``None``, tất cả các frame đều được bao gồm.


   .. method:: BaseHandler.error_output(environ, start_response)

      Phương thức này là một ứng dụng WSGI dùng để tạo trang lỗi cho người dùng. Phương thức chỉ được gọi nếu xảy ra lỗi trước khi các header được gửi đến client.

      Phương thức này có thể truy cập lỗi hiện tại bằng ``sys.exception()``, và phải truyền thông tin đó cho *start_response* khi gọi nó (như được mô tả trong phần "Xử lý lỗi" của :pep:`3333`). Cụ thể, callable *start_response* phải tuân theo giao thức :class:`.StartResponse`.

      Phần triển khai mặc định chỉ sử dụng :attr:`error_status` để tạo trang đầu ra,
      các thuộc tính :attr:`error_headers` và :attr:`error_body` để tạo một trang đầu ra. Các lớp con có thể ghi đè phần này để tạo đầu ra lỗi động hơn.

      Tuy nhiên, từ góc độ bảo mật, không nên hiển thị thông tin chẩn đoán cho bất kỳ người dùng nào; lý tưởng nhất là phải thực hiện một thao tác đặc biệt để bật đầu ra chẩn đoán, đó là lý do phần triển khai mặc định không bao gồm thông tin nào.


   .. attribute:: BaseHandler.error_status

      Trạng thái HTTP được sử dụng cho các phản hồi lỗi. Đây phải là một chuỗi trạng thái như được định nghĩa trong :pep:`3333`; mặc định là mã và thông báo 500.


   .. attribute:: BaseHandler.error_headers

      Các HTTP header được sử dụng cho các response lỗi. Đây phải là một danh sách các WSGI response header (các tuple ``(name, value)``), như được mô tả trong :pep:`3333`. Danh sách mặc định chỉ đặt content type thành ``text/plain``.


   .. attribute:: BaseHandler.error_body

      Body của response lỗi. Đây phải là một bytestring body của HTTP response. Giá trị mặc định là văn bản thuần túy, "Đã xảy ra lỗi máy chủ. Vui lòng liên hệ với quản trị viên."

   Các method và attribute cho tính năng "Xử lý tệp tùy chọn theo nền tảng" của :pep:`3333`:


   .. attribute:: BaseHandler.wsgi_file_wrapper

      Một factory ``wsgi.file_wrapper``, tương thích với
      :class:`wsgiref.types.FileWrapper`, hoặc ``None``. Giá trị mặc định của attribute này là class :class:`wsgiref.util.FileWrapper`.


   .. method:: BaseHandler.sendfile()

      Ghi đè để triển khai việc truyền tệp dành riêng cho nền tảng. Method này chỉ được gọi nếu giá trị trả về của ứng dụng là một instance của class được chỉ định bởi attribute :attr:`wsgi_file_wrapper`. Method này phải trả về giá trị true nếu đã truyền tệp thành công, để code truyền tệp mặc định không được thực thi. Bản triển khai mặc định của method này chỉ trả về giá trị false.

   Các method và attribute khác:


   .. attribute:: BaseHandler.origin_server

      Thuộc tính này nên được đặt thành giá trị true nếu :meth:`_write` của handler và
      :meth:`_flush` đang được sử dụng để giao tiếp trực tiếp với client, thay vì thông qua một giao thức gateway tương tự CGI yêu cầu trạng thái HTTP trong một header ``Status:`` đặc biệt.

      Giá trị mặc định của thuộc tính này là true trong :class:`BaseHandler`, nhưng là false trong
      :class:`BaseCGIHandler` và :class:`CGIHandler`.


   .. attribute:: BaseHandler.http_version

      Nếu :attr:`origin_server` là true, thuộc tính chuỗi này được dùng để đặt phiên bản HTTP của response gửi đến client. Giá trị mặc định là ``"1.0"``.


.. function:: read_environ()

   Chuyển mã các biến CGI từ ``os.environ`` sang :pep:`3333` các chuỗi "bytes in unicode", trả về một dictionary mới. Hàm này được dùng bởi
   :class:`CGIHandler` và :class:`IISCGIHandler` thay cho việc sử dụng trực tiếp ``os.environ``, vốn không nhất thiết tuân thủ WSGI trên mọi nền tảng và web server sử dụng Python 3 -- cụ thể là những nền tảng mà môi trường thực tế của OS là Unicode (tức Windows), hoặc những nền tảng mà môi trường là bytes nhưng encoding hệ thống được Python sử dụng để giải mã không phải ISO-8859-1 (ví dụ các hệ thống Unix sử dụng UTF-8).

   Nếu bạn đang tự triển khai một trình xử lý dựa trên CGI, có lẽ bạn nên sử dụng routine này thay vì chỉ sao chép trực tiếp các giá trị từ ``os.environ``.

   .. versionadded:: 3.2


:mod:`!wsgiref.types` -- Các kiểu WSGI để kiểm tra kiểu tĩnh
------------------------------------------------------------

.. module:: wsgiref.types
   :synopsis: Các kiểu WSGI để kiểm tra kiểu tĩnh


Mô-đun này cung cấp nhiều kiểu khác nhau để kiểm tra kiểu tĩnh như được mô tả trong :pep:`3333`.

.. versionadded:: 3.11


.. class:: StartResponse

   Một :class:`typing.Protocol` mô tả các callable :pep:`start_response() <3333#the-start-response-callable>` (:pep:`3333`).

.. data:: WSGIEnvironment

   Một bí danh kiểu mô tả dictionary môi trường WSGI.

.. data:: WSGIApplication

   Một bí danh kiểu mô tả callable ứng dụng WSGI.

.. class:: InputStream()

   Một :class:`typing.Protocol` mô tả một :pep:`WSGI Input Stream <3333#input-and-error-streams>`.

.. class:: ErrorStream()

   Một :class:`typing.Protocol` mô tả một :pep:`WSGI Error Stream <3333#input-and-error-streams>`.

.. class:: FileWrapper()

   Một :class:`typing.Protocol` mô tả một :pep:`file wrapper <3333#optional-platform-specific-file-handling>`. Xem :class:`wsgiref.util.FileWrapper` để biết một triển khai cụ thể của giao thức này.


Ví dụ
-----

Đây là một ứng dụng WSGI "Hello World" hoạt động được, trong đó hàm *start_response* phải tuân theo giao thức :class:`.StartResponse`::

   """
   Every WSGI application must have an application object - a callable
   object that accepts two arguments. For that purpose, we're going to
   use a function (note that you're not limited to a function, you can
   use a class for example). The first argument passed to the function
   is a dictionary containing CGI-style environment variables and the
   second variable is the callable object.
   """
   from wsgiref.simple_server import make_server


   def hello_world_app(environ, start_response):
       status = "200 OK"  # Trạng thái HTTP
       headers = [("Content-type", "text/plain; charset=utf-8")]  # Tiêu đề HTTP
       start_response(status, headers)

       # Đối tượng được trả về sẽ được in ra
       return [b"Hello World"]

   with make_server("", 8000, hello_world_app) as httpd:
       print("Serving on port 8000...")

       # Phục vụ cho đến khi tiến trình bị kết thúc
       httpd.serve_forever()



Ví dụ về một ứng dụng WSGI phục vụ thư mục hiện tại, chấp nhận thư mục và số cổng tùy chọn (mặc định: 8000) trên command line::

    """
    Small wsgiref based web server. Takes a path to serve from and an
    optional port number (defaults to 8000), then tries to serve files.
    MIME types are guessed from the file names, 404 errors are raised
    if the file is not found.
    """
    import mimetypes
    import os
    import sys
    from wsgiref import simple_server, util


    def app(environ, respond):
        # Lấy tên tệp và kiểu MIME
        fn = os.path.join(path, environ["PATH_INFO"][1:])
        if "." not in fn.split(os.path.sep)[-1]:
            fn = os.path.join(fn, "index.html")
        mime_type = mimetypes.guess_file_type(fn)[0]

        # Trả về 200 OK nếu tệp tồn tại, nếu không thì trả về 404 Not Found
        if os.path.exists(fn):
            respond("200 OK", [("Content-Type", mime_type)])
            return util.FileWrapper(open(fn, "rb"))
        else:
            respond("404 Not Found", [("Content-Type", "text/plain")])
            return [b"not found"]


    if __name__ == "__main__":
        # Lấy đường dẫn và cổng từ các đối số command line
        path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
        port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000

        # Tạo và khởi động server cho đến khi nhấn control-c
        httpd = simple_server.make_server("", port, app)
        print(f"Serving {path} on port {port}, control-C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Shutting down.")
            httpd.server_close()

.. _`wsgi.readthedocs.io`: https://wsgi.readthedocs.io/
