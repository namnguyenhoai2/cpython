:mod:`!urllib.request` --- Thư viện có thể mở rộng để mở các URL
================================================================

.. module:: urllib.request
   :synopsis: Thư viện có thể mở rộng để mở các URL.

.. moduleauthor:: Jeremy Hylton <jeremy@alum.mit.edu>
.. sectionauthor:: Moshe Zadka <moshez@users.sourceforge.net>
.. sectionauthor:: Senthil Kumaran <senthil@uthcode.com>

**Mã nguồn:** :source:`Lib/urllib/request.py`

--------------

Module :mod:`!urllib.request` định nghĩa các hàm và lớp hỗ trợ mở các URL (chủ yếu là HTTP) trong một thế giới phức tạp — xác thực cơ bản và digest, chuyển hướng, cookie và nhiều tính năng khác.

.. seealso::

    `Gói Requests <https://requests.readthedocs.io/en/master/>`_ được khuyến nghị để sử dụng interface HTTP client ở cấp độ cao hơn.

.. warning::

   Trên macOS, việc sử dụng module này trong các chương trình sử dụng
   :func:`os.fork` là không an toàn vì implementation :func:`getproxies` cho macOS sử dụng một system API cấp cao hơn. Đặt biến môi trường ``no_proxy`` thành ``*`` để tránh vấn đề này (ví dụ: ``os.environ["no_proxy"] = "*"``).

.. include:: ../includes/wasm-notavail.rst

Mô-đun :mod:`!urllib.request` định nghĩa các hàm sau:


.. function:: urlopen(url, data=None[, timeout], *, context=None)

   Mở *url*, có thể là một chuỗi chứa URL hợp lệ, được mã hóa đúng cách, hoặc một đối tượng :class:`Request`.

   *data* phải là một đối tượng chỉ định dữ liệu bổ sung sẽ được gửi đến máy chủ, hoặc ``None`` nếu không cần dữ liệu đó. Xem :class:`Request` để biết chi tiết.

   Mô-đun urllib.request sử dụng HTTP/1.1 và đưa tiêu đề ``Connection:close`` vào các yêu cầu HTTP.

   Tham số *timeout* tùy chọn chỉ định thời gian chờ tính bằng giây cho các thao tác chặn như thao tác cố gắng kết nối (nếu không được chỉ định, cài đặt thời gian chờ mặc định toàn cục sẽ được sử dụng). Tham số này thực sự chỉ hoạt động với các kết nối HTTP, HTTPS và FTP.

   Nếu *context* được chỉ định, nó phải là một thực thể :class:`ssl.SSLContext` mô tả các tùy chọn SSL khác nhau. Xem :class:`~http.client.HTTPSConnection` để biết thêm chi tiết.

   Hàm này luôn trả về một đối tượng có thể hoạt động như một
   :term:`context manager` và có các thuộc tính *url*, *headers* và *status*. Xem :class:`urllib.response.addinfourl` để biết thêm chi tiết về các thuộc tính này.

   Đối với các URL HTTP và HTTPS, hàm này trả về một
   đối tượng :class:`http.client.HTTPResponse` được sửa đổi đôi chút. Ngoài ba phương thức mới ở trên, thuộc tính msg chứa cùng thông tin với thuộc tính :attr:`~http.client.HTTPResponse.reason` --- cụm từ lý do do máy chủ trả về --- thay vì các tiêu đề phản hồi như được nêu trong tài liệu về
   :class:`~http.client.HTTPResponse`.

   Đối với các URL FTP, file và data, hàm này trả về một đối tượng :class:`urllib.response.addinfourl`.

   Phát sinh :exc:`~urllib.error.URLError` khi xảy ra lỗi giao thức.

   Lưu ý rằng ``None`` có thể được trả về nếu không có handler nào xử lý yêu cầu (mặc dù :class:`OpenerDirector` toàn cục mặc định được cài đặt sử dụng
   :class:`UnknownHandler` để đảm bảo điều này không bao giờ xảy ra).

   Ngoài ra, nếu phát hiện thấy các thiết lập proxy (ví dụ: khi một biến môi trường ``*_proxy`` như :envvar:`!http_proxy` được đặt),
   :class:`ProxyHandler` được cài đặt theo mặc định và đảm bảo các request được xử lý thông qua proxy.

   Hàm ``urllib.urlopen`` cũ từ Python 2.6 trở về trước đã bị ngừng sử dụng; :func:`urllib.request.urlopen` tương ứng với ``urllib2.urlopen`` cũ. Việc xử lý proxy, trước đây được thực hiện bằng cách truyền một tham số dictionary cho ``urllib.urlopen``, có thể thực hiện bằng cách sử dụng
   các đối tượng :class:`ProxyHandler`.

   .. audit-event:: urllib.Request fullurl,data,headers,method urllib.request.urlopen

      opener mặc định phát ra một :ref:`sự kiện auditing <auditing>` ``urllib.Request`` với các đối số ``fullurl``, ``data``, ``headers``, ``method`` được lấy từ request object.

   .. versionchanged:: 3.2
      *cafile* và *capath* đã được bổ sung.

      Virtual host HTTPS hiện được hỗ trợ nếu có thể (nghĩa là, nếu
      :const:`ssl.HAS_SNI` là true).

      *data* có thể là một đối tượng iterable.

   .. versionchanged:: 3.3
      *cadefault* đã được thêm vào.

   .. versionchanged:: 3.4.3
      *context* đã được thêm vào.

   .. versionchanged:: 3.10
      Kết nối HTTPS hiện gửi một extension ALPN với chỉ báo giao thức ``http/1.1`` khi không cung cấp *context*. *context* tùy chỉnh nên thiết lập các giao thức ALPN bằng :meth:`~ssl.SSLContext.set_alpn_protocols`.

   .. versionchanged:: 3.13
      Xóa các tham số *cafile*, *capath* và *cadefault*: thay vào đó, sử dụng tham số *context*.


.. function:: install_opener(opener)

   Cài đặt một instance :class:`OpenerDirector` làm opener toàn cục mặc định. Chỉ cần cài đặt một opener nếu bạn muốn urlopen sử dụng opener đó; nếu không, chỉ cần gọi :meth:`OpenerDirector.open` thay vì
   :func:`~urllib.request.urlopen`. Mã không kiểm tra xem đó có phải là một đối tượng thực hay không
   :class:`OpenerDirector`, và bất kỳ class nào có interface phù hợp đều sẽ hoạt động.


.. function:: build_opener([handler, ...])

   Trả về một instance :class:`OpenerDirector`, liên kết các handler theo thứ tự đã cho. *handler*\s có thể là các instance của :class:`BaseHandler` hoặc các subclass của :class:`BaseHandler` (trong trường hợp đó, phải có thể gọi constructor mà không truyền tham số nào). Các instance của những class sau sẽ được đặt trước *handler*\s, trừ khi *handler*\s chứa chúng, các instance của chúng hoặc các subclass của chúng: :class:`ProxyHandler` (nếu phát hiện thấy cài đặt proxy), :class:`UnknownHandler`, :class:`HTTPHandler`,
   :class:`HTTPDefaultErrorHandler`, :class:`HTTPRedirectHandler`,
   :class:`FTPHandler`, :class:`FileHandler`, :class:`HTTPErrorProcessor`.

   Nếu bản cài đặt Python có hỗ trợ SSL (tức là có thể import module :mod:`ssl`), thì :class:`HTTPSHandler` cũng sẽ được thêm vào.

   Một subclass :class:`BaseHandler` cũng có thể thay đổi thuộc tính :attr:`handler_order` để điều chỉnh vị trí của nó trong danh sách handler.


.. function:: pathname2url(path, *, add_scheme=False)

   Chuyển đường dẫn cục bộ đã cho thành URL ``file:``. Hàm này sử dụng
   hàm :func:`~urllib.parse.quote` để mã hóa đường dẫn.

   Nếu *add_scheme* là false (mặc định), giá trị trả về sẽ bỏ qua tiền tố scheme ``file:``. Đặt *add_scheme* thành true để trả về một URL hoàn chỉnh.

   Ví dụ này minh họa cách sử dụng hàm trên Windows::

      >>> from urllib.request import pathname2url
      >>> path = 'C:\\Program Files'
      >>> pathname2url(path, add_scheme=True)
      'file:///C:/Program%20Files'

   .. versionchanged:: 3.14
      Các ký tự ổ đĩa Windows không còn được chuyển thành chữ hoa, và các ký tự ``:`` không theo sau một ký tự ổ đĩa sẽ không còn khiến
      :exc:`OSError` một ngoại lệ được phát sinh trên Windows.

   .. versionchanged:: 3.14
      Các đường dẫn bắt đầu bằng dấu gạch chéo được chuyển đổi thành các URL có phần authority. Ví dụ, đường dẫn ``/etc/hosts`` được chuyển đổi thành URL ``///etc/hosts``.

   .. versionchanged:: 3.14
      Tham số *add_scheme* đã được thêm vào.


.. function:: url2pathname(url, *, require_scheme=False, resolve_host=False)

   Chuyển đổi ``file:`` URL đã cho thành đường dẫn cục bộ. Hàm này sử dụng
   :func:`~urllib.parse.unquote` để giải mã URL.

   Nếu *require_scheme* là false (mặc định), giá trị đã cho không được có tiền tố ``file:`` scheme. Nếu *require_scheme* được đặt thành true, giá trị đã cho phải có tiền tố này; nếu không, một :exc:`~urllib.error.URLError` sẽ được raise.

   Authority của URL sẽ bị loại bỏ nếu nó rỗng, là ``localhost``, hoặc là hostname cục bộ. Nếu không, khi *resolve_host* được đặt thành true, authority sẽ được phân giải bằng :func:`socket.gethostbyname` và bị loại bỏ nếu khớp với một địa chỉ IP cục bộ (theo :rfc:`RFC 8089 §3 <8089#section-3>`). Nếu authority vẫn chưa được xử lý, trên Windows một đường dẫn UNC sẽ được trả về, còn trên các nền tảng khác một :exc:`~urllib.error.URLError` sẽ được raise.

   Ví dụ này minh họa cách sử dụng hàm trên Windows::

      >>> from urllib.request import url2pathname
      >>> url = 'file:///C:/Program%20Files'
      >>> url2pathname(url, require_scheme=True)
      'C:\\Program Files'

   .. versionchanged:: 3.14
      Các ký tự ổ đĩa Windows không còn được chuyển thành chữ hoa, và các ký tự ``:`` không theo sau một ký tự ổ đĩa sẽ không còn khiến
      :exc:`OSError` một ngoại lệ được phát sinh trên Windows.

   .. versionchanged:: 3.14
      Authority của URL sẽ bị loại bỏ nếu khớp với hostname cục bộ. Nếu không, khi authority không rỗng hoặc là ``localhost``, thì trên Windows một đường dẫn UNC sẽ được trả về (như trước đây), còn trên các nền tảng khác một
      :exc:`~urllib.error.URLError` được ném ra.

   .. versionchanged:: 3.14
      Các thành phần truy vấn và fragment của URL sẽ bị loại bỏ nếu có.

   .. versionchanged:: 3.14
      Các tham số *require_scheme* và *resolve_host* đã được thêm vào.


.. function:: getproxies()

   Hàm trợ giúp này trả về một dictionary ánh xạ scheme với URL của máy chủ proxy. Trước tiên, hàm quét môi trường trên tất cả hệ điều hành để tìm các biến có tên ``<scheme>_proxy``, không phân biệt chữ hoa chữ thường; nếu không tìm thấy, hàm sẽ tìm thông tin proxy từ System Configuration trên macOS và Windows Systems Registry trên Windows. Nếu tồn tại cả biến môi trường viết thường và viết hoa (và chúng có giá trị khác nhau), biến viết thường sẽ được ưu tiên.

   .. note::

      Nếu biến môi trường ``REQUEST_METHOD`` được đặt, thường cho biết script của bạn đang chạy trong môi trường CGI, biến môi trường ``HTTP_PROXY`` (viết hoa ``_PROXY``) sẽ bị bỏ qua. Nguyên nhân là vì biến đó có thể bị client chèn vào thông qua HTTP header "Proxy:". Nếu cần sử dụng HTTP proxy trong môi trường CGI, hãy sử dụng ``ProxyHandler`` một cách rõ ràng hoặc đảm bảo tên biến được viết thường (hoặc ít nhất là phần hậu tố ``_proxy``).


Các lớp sau được cung cấp:

.. class:: Request(url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None)

   Lớp này là abstraction của một yêu cầu URL.

   *url* phải là một chuỗi chứa URL hợp lệ, được mã hóa đúng cách.

   *data* phải là một đối tượng chỉ định dữ liệu bổ sung cần gửi đến máy chủ, hoặc ``None`` nếu không cần dữ liệu đó. Hiện tại, chỉ các yêu cầu HTTP sử dụng *data*. Các kiểu đối tượng được hỗ trợ bao gồm bytes, các đối tượng dạng tệp và các iterable gồm các đối tượng giống bytes. Nếu chưa cung cấp trường tiêu đề ``Content-Length`` hoặc ``Transfer-Encoding``, :class:`HTTPHandler` sẽ thiết lập các tiêu đề này theo kiểu của *data*. ``Content-Length`` sẽ được dùng để gửi các đối tượng bytes, còn ``Transfer-Encoding: chunked`` như được chỉ định trong
   :rfc:`7230`, Mục 3.3.1 sẽ được dùng để gửi các tệp và các iterable khác.

   Đối với phương thức yêu cầu HTTP POST, *data* phải là một bộ đệm ở định dạng :mimetype:`application/x-www-form-urlencoded` tiêu chuẩn.
   :func:`urllib.parse.urlencode` function nhận một mapping hoặc một sequence gồm các bộ 2 phần tử và trả về một chuỗi ASCII ở định dạng này. Chuỗi này phải được mã hóa thành bytes trước khi được dùng làm tham số *data*.

   *headers* phải là một dictionary và sẽ được xử lý như thể
   :meth:`add_header` được gọi với từng khóa và giá trị làm các đối số. Cách này thường được dùng để "giả mạo" giá trị tiêu đề ``User-Agent``, vốn được trình duyệt dùng để tự nhận diện -- một số máy chủ HTTP chỉ cho phép các yêu cầu đến từ những trình duyệt phổ biến thay vì từ các script. Ví dụ, Mozilla Firefox có thể tự nhận diện là ``"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"``, trong khi
   :mod:`urllib` có chuỗi user agent mặc định là ``"Python-urllib/2.6"`` (trên Python 2.6). Tất cả các khóa header đều được gửi theo kiểu camel case.

   Cần bao gồm header ``Content-Type`` thích hợp nếu có đối số *data*. Nếu header này chưa được cung cấp và *data* không phải là ``None``, ``Content-Type: application/x-www-form-urlencoded`` sẽ được thêm vào theo mặc định.

   Hai đối số tiếp theo chỉ cần thiết để xử lý đúng các cookie HTTP của bên thứ ba:

   *origin_req_host* phải là request-host của giao dịch gốc, như được định nghĩa bởi :rfc:`2965`. Giá trị mặc định là ``http.cookiejar.request_host(self)``. Đây là tên máy chủ hoặc địa chỉ IP của request gốc do người dùng khởi tạo. Ví dụ, nếu request là để lấy một hình ảnh trong tài liệu HTML, đây phải là request-host của request lấy trang chứa hình ảnh đó.

   *unverifiable* phải cho biết liệu request có thể xác minh được hay không, như được định nghĩa bởi :rfc:`2965`. Giá trị mặc định là ``False``. Một request không thể xác minh là request mà người dùng không có tùy chọn phê duyệt URL của nó. Ví dụ, nếu request là để lấy một hình ảnh trong tài liệu HTML và người dùng không có tùy chọn phê duyệt việc tự động lấy hình ảnh, giá trị này phải là true.

   *method* phải là một chuỗi cho biết phương thức HTTP của request sẽ được sử dụng (ví dụ: ``'HEAD'``). Nếu được cung cấp, giá trị của nó sẽ được lưu trong
   :attr:`~Request.method` attribute và được :meth:`get_method` sử dụng. Giá trị mặc định là ``'GET'`` nếu *data* là ``None``, hoặc ``'POST'`` trong các trường hợp khác. Các lớp con có thể chỉ định một phương thức mặc định khác bằng cách đặt
   thuộc tính :attr:`~Request.method` ngay trong lớp.

   .. note::
      Yêu cầu sẽ không hoạt động như mong đợi nếu đối tượng dữ liệu không thể cung cấp nội dung của nó nhiều hơn một lần (ví dụ: một tệp hoặc một iterable chỉ có thể tạo nội dung một lần) và yêu cầu được thử lại do chuyển hướng HTTP hoặc xác thực. *data* được gửi ngay đến máy chủ HTTP sau các header. Thư viện không hỗ trợ expectation 100-continue.

   .. versionchanged:: 3.3
      :attr:`Request.method` argument is added to the Request class.

   .. versionchanged:: 3.4
      :attr:`Request.method` mặc định có thể được chỉ định ở cấp lớp.

   .. versionchanged:: 3.6
      Không phát sinh lỗi nếu ``Content-Length`` chưa được cung cấp và *data* không phải là ``None`` cũng không phải đối tượng bytes. Thay vào đó, sử dụng mã hóa truyền theo từng chunk.

.. class:: OpenerDirector()

   Lớp :class:`OpenerDirector` mở các URL thông qua các :class:`BaseHandler`\ s được nối với nhau. Lớp này quản lý việc nối chuỗi các handler và khôi phục sau lỗi.


.. class:: BaseHandler()

   Đây là lớp cơ sở cho tất cả handler đã đăng ký --- và chỉ xử lý các cơ chế đơn giản của việc đăng ký.


.. class:: HTTPDefaultErrorHandler()

   Một lớp định nghĩa handler mặc định cho các phản hồi lỗi HTTP; tất cả phản hồi đều được chuyển thành các ngoại lệ :exc:`~urllib.error.HTTPError`.


.. class:: HTTPRedirectHandler()

   Một class để xử lý việc chuyển hướng.


.. class:: HTTPCookieProcessor(cookiejar=None)

   Một class để xử lý HTTP Cookies.


.. class:: ProxyHandler(proxies=None)

   Khi cung cấp *proxies*, giá trị này phải là một dictionary ánh xạ tên giao thức tới URL của các proxy. Mặc định, danh sách proxy được đọc từ các biến môi trường ``<protocol>_proxy``. Nếu không đặt biến môi trường proxy nào, trong môi trường Windows, các thiết lập proxy được lấy từ phần Internet Settings của registry, còn trong môi trường macOS, thông tin proxy được lấy từ System Configuration Framework.

   Để tắt proxy được tự động phát hiện, hãy truyền vào một dictionary rỗng.

   Có thể sử dụng biến môi trường :envvar:`no_proxy` để chỉ định các host không nên được truy cập qua proxy; nếu được đặt, biến này phải là danh sách các hậu tố hostname được phân tách bằng dấu phẩy, có thể kèm ``:port`` ở cuối, ví dụ ``cern.ch,ncsa.uiuc.edu,some.host:8080``.

   .. note::

      ``HTTP_PROXY`` sẽ bị bỏ qua nếu biến ``REQUEST_METHOD`` được đặt; xem tài liệu về :func:`~urllib.request.getproxies`.


.. class:: HTTPPasswordMgr()

   Duy trì cơ sở dữ liệu gồm các ánh xạ ``(realm, uri) -> (user, password)``.


.. class:: HTTPPasswordMgrWithDefaultRealm()

   Duy trì cơ sở dữ liệu về các ánh xạ ``(realm, uri) -> (user, password)``. Một realm của ``None`` được xem là realm catch-all, được tìm kiếm nếu không có realm nào khác phù hợp.


.. class:: HTTPPasswordMgrWithPriorAuth()

   Một biến thể của :class:`HTTPPasswordMgrWithDefaultRealm` cũng có cơ sở dữ liệu về các ánh xạ ``uri -> is_authenticated``. Có thể được BasicAuth handler sử dụng để xác định thời điểm gửi thông tin xác thực ngay lập tức thay vì trước tiên phải chờ phản hồi ``401``.

   .. versionadded:: 3.5


.. class:: AbstractBasicAuthHandler(password_mgr=None)

   Đây là một mixin class hỗ trợ xác thực HTTP, cả với máy chủ từ xa và proxy. *password_mgr*, nếu được cung cấp, phải là đối tượng tương thích với :class:`HTTPPasswordMgr`; tham khảo phần
   :ref:`http-password-mgr` để biết thông tin về interface cần được hỗ trợ. Nếu *passwd_mgr* cũng cung cấp các phương thức ``is_authenticated`` và ``update_authenticated`` (xem
   :ref:`http-password-mgr-with-prior-auth`), handler sẽ sử dụng kết quả ``is_authenticated`` cho một URI nhất định để xác định có gửi thông tin xác thực cùng với request hay không. Nếu ``is_authenticated`` trả về ``True`` cho URI đó, thông tin xác thực sẽ được gửi. Nếu ``is_authenticated`` là ``False``, thông tin xác thực sẽ không được gửi; sau đó, nếu nhận được phản hồi ``401``, request sẽ được gửi lại cùng với thông tin xác thực. Nếu xác thực thành công, ``update_authenticated`` được gọi để thiết lập ``is_authenticated`` ``True`` cho URI, ताकि các request tiếp theo đến URI hoặc bất kỳ super-URI nào của URI sẽ tự động bao gồm thông tin xác thực.

   .. versionadded:: 3.5
      Đã thêm hỗ trợ ``is_authenticated``.


.. class:: HTTPBasicAuthHandler(password_mgr=None)

   Xử lý việc xác thực với máy chủ từ xa. *password_mgr*, nếu được cung cấp, phải là đối tượng tương thích với :class:`HTTPPasswordMgr`; tham khảo phần :ref:`http-password-mgr` để biết thông tin về interface cần được hỗ trợ. HTTPBasicAuthHandler sẽ raise một :exc:`ValueError` khi nhận được scheme Authentication không đúng.


.. class:: ProxyBasicAuthHandler(password_mgr=None)

   Xử lý việc xác thực với proxy. *password_mgr*, nếu được cung cấp, phải là đối tượng tương thích với :class:`HTTPPasswordMgr`; hãy tham khảo phần
   :ref:`http-password-mgr` để biết thông tin về giao diện phải được hỗ trợ.


.. class:: AbstractDigestAuthHandler(password_mgr=None)

   Đây là một mixin class hỗ trợ xác thực HTTP, cả với máy chủ từ xa và proxy. *password_mgr*, nếu được cung cấp, phải là đối tượng tương thích với :class:`HTTPPasswordMgr`; tham khảo phần
   :ref:`http-password-mgr` để biết thông tin về giao diện phải được hỗ trợ.

   .. versionchanged:: 3.14
      Đã bổ sung hỗ trợ cho thuật toán xác thực HTTP digest ``SHA-256``.


.. class:: HTTPDigestAuthHandler(password_mgr=None)

   Xử lý việc xác thực với máy chủ từ xa. *password_mgr*, nếu được cung cấp, phải là đối tượng tương thích với :class:`HTTPPasswordMgr`; hãy tham khảo phần :ref:`http-password-mgr` để biết thông tin về giao diện phải được hỗ trợ. Khi cả Digest Authentication Handler và Basic Authentication Handler đều được thêm vào, Digest Authentication luôn được thử trước. Nếu Digest Authentication lại trả về phản hồi 40x, phản hồi đó sẽ được chuyển đến Basic Authentication handler để xử lý. Phương thức Handler này sẽ phát sinh một
   :exc:`ValueError` khi gặp một lược đồ xác thực khác với Digest hoặc Basic.

   .. versionchanged:: 3.3
      Phát sinh :exc:`ValueError` khi Scheme xác thực không được hỗ trợ.



.. class:: ProxyDigestAuthHandler(password_mgr=None)

   Xử lý việc xác thực với proxy. *password_mgr*, nếu được cung cấp, phải là đối tượng tương thích với :class:`HTTPPasswordMgr`; hãy tham khảo phần
   :ref:`http-password-mgr` để biết thông tin về giao diện phải được hỗ trợ.


.. class:: HTTPHandler()

   Một lớp dùng để xử lý việc mở các URL HTTP.


.. class:: HTTPSHandler(debuglevel=0, context=None, check_hostname=None)

   Một lớp dùng để xử lý việc mở các URL HTTPS.  *context* và *check_hostname* có cùng ý nghĩa như trong :class:`http.client.HTTPSConnection`.

   .. versionchanged:: 3.2
      Đã bổ sung *context* và *check_hostname*.


.. class:: FileHandler()

   Mở các tệp cục bộ.

.. class:: DataHandler()

   Mở các URL data.

   .. versionadded:: 3.4

.. class:: FTPHandler()

   Mở các URL FTP.


.. class:: CacheFTPHandler()

   Mở các URL FTP, đồng thời duy trì bộ nhớ đệm của các kết nối FTP đang mở để giảm thiểu độ trễ.


.. class:: UnknownHandler()

   Một lớp tổng quát để xử lý các URL không xác định.


.. class:: HTTPErrorProcessor()

   Xử lý các phản hồi lỗi HTTP.


.. _request-objects:

Đối tượng Request
-----------------

Các phương thức sau đây mô tả giao diện công khai của :class:`Request`, vì vậy tất cả đều có thể được ghi đè trong các lớp con. Đối tượng này cũng định nghĩa một số thuộc tính công khai mà client có thể sử dụng để kiểm tra request đã được phân tích cú pháp.

.. attribute:: Request.full_url

   URL ban đầu được truyền vào constructor.

   .. versionchanged:: 3.4

   Request.full_url là một property có setter, getter và deleter. Việc lấy
   :attr:`~Request.full_url` trả về URL request ban đầu cùng với fragment, nếu có.

.. attribute:: Request.type

   Scheme của URI.

.. attribute:: Request.host

   Authority của URI, thường là host, nhưng cũng có thể chứa port được phân tách bằng dấu hai chấm.

.. attribute:: Request.origin_req_host

   Host ban đầu của request, không có port.

.. attribute:: Request.selector

   Path của URI. Nếu :class:`Request` sử dụng proxy, thì selector sẽ là URL đầy đủ được truyền đến proxy.

.. attribute:: Request.data

   Nội dung thực thể của request hoặc ``None`` nếu không được chỉ định.

   .. versionchanged:: 3.4
      Việc thay đổi giá trị của :attr:`Request.data` hiện sẽ xóa header "Content-Length" nếu header này trước đó đã được thiết lập hoặc tính toán.

.. attribute:: Request.unverifiable

   boolean, cho biết request có thể xác minh được hay không theo định nghĩa của :rfc:`2965`.

.. attribute:: Request.method

   Phương thức HTTP sẽ sử dụng cho request.  Theo mặc định, giá trị của nó là :const:`None`, nghĩa là :meth:`~Request.get_method` sẽ thực hiện phép tính thông thường để xác định phương thức cần sử dụng.  Có thể thiết lập giá trị của nó (qua đó ghi đè phép tính mặc định trong :meth:`~Request.get_method`) bằng cách cung cấp giá trị mặc định khi thiết lập ở cấp lớp trong một lớp con của :class:`Request`, hoặc bằng cách truyền giá trị vào hàm khởi tạo :class:`Request` thông qua đối số *method*.

   .. versionadded:: 3.3

   .. versionchanged:: 3.4
      Giờ đây có thể thiết lập giá trị mặc định trong các lớp con; trước đây chỉ có thể thiết lập giá trị này thông qua đối số của hàm khởi tạo.


.. method:: Request.get_method()

   Trả về một chuỗi cho biết phương thức HTTP request.  Nếu
   :attr:`Request.method` không phải là ``None``, trả về giá trị của nó; nếu không, trả về ``'GET'`` nếu :attr:`Request.data` là ``None``, hoặc ``'POST'`` nếu không phải. Điều này chỉ có ý nghĩa đối với các request HTTP.

   .. versionchanged:: 3.3
      get_method hiện xem xét giá trị của :attr:`Request.method`.


.. method:: Request.add_header(key, val)

   Thêm một header khác vào request. Hiện tại, tất cả handler đều bỏ qua các header, ngoại trừ HTTP handler, trong đó chúng được thêm vào danh sách các header gửi đến server. Lưu ý rằng không thể có nhiều hơn một header có cùng tên, và các lần gọi sau sẽ ghi đè các lần gọi trước nếu *key* bị trùng. Hiện tại, điều này không làm mất chức năng HTTP nào, vì tất cả header có ý nghĩa khi được sử dụng nhiều hơn một lần đều có một cách (riêng cho từng header) để đạt được chức năng tương tự chỉ bằng một header. Lưu ý rằng các header được thêm bằng phương thức này cũng được thêm vào các request được chuyển hướng.


.. method:: Request.add_unredirected_header(key, header)

   Thêm một header sẽ không được thêm vào request được chuyển hướng.


.. method:: Request.has_header(header)

   Trả về việc instance có header được đặt tên đó hay không (kiểm tra cả header thông thường và header không chuyển hướng).


.. method:: Request.remove_header(header)

   Xóa header được đặt tên khỏi instance request (cả khỏi các header thông thường và không chuyển hướng).

   .. versionadded:: 3.4


.. method:: Request.get_full_url()

   Trả về URL được cung cấp trong constructor.

   .. versionchanged:: 3.4

   Trả về :attr:`Request.full_url`


.. method:: Request.set_proxy(host, type)

   Chuẩn bị yêu cầu bằng cách kết nối đến một proxy server. *host* và *type* sẽ thay thế các giá trị tương ứng của instance, còn selector của instance sẽ là URL ban đầu được cung cấp trong constructor.


.. method:: Request.get_header(header_name, default=None)

   Trả về giá trị của header đã cho. Nếu header không tồn tại, trả về giá trị mặc định.


.. method:: Request.header_items()

   Trả về danh sách các tuple (header_name, header_value) của các header trong Request.

.. versionchanged:: 3.4
   Các phương thức request add_data, has_data, get_data, get_type, get_host, get_selector, get_origin_req_host và is_unverifiable đã bị xóa vì đã deprecated kể từ phiên bản 3.3.


.. _opener-director-objects:

Đối tượng OpenerDirector
------------------------

Các instance :class:`OpenerDirector` có những phương thức sau:


.. method:: OpenerDirector.add_handler(handler)

   *handler* phải là một instance của :class:`BaseHandler`. Các phương thức sau sẽ được tìm kiếm và thêm vào các chuỗi khả dĩ (lưu ý rằng lỗi HTTP là một trường hợp đặc biệt). Trong phần sau, *protocol* cần được thay thế bằng protocol thực tế cần xử lý; chẳng hạn, :meth:`http_response` sẽ là trình xử lý phản hồi của protocol HTTP. Tương tự, *type* cần được thay thế bằng mã HTTP thực tế; chẳng hạn, :meth:`http_error_404` sẽ xử lý lỗi HTTP 404.

   * :meth:`!<protocol>_open` --- cho biết handler biết cách mở các URL *protocol*.

     Xem |protocol_open|_ để biết thêm thông tin.

   * :meth:`!http_error_\<type\>` --- cho biết handler biết cách xử lý các lỗi HTTP với mã lỗi HTTP *type*.

     Xem |http_error_nnn|_ để biết thêm thông tin.

   * :meth:`!<protocol>_error` --- cho biết handler biết cách xử lý các lỗi từ *protocol* (không phải \ ``http``).

   * :meth:`!<protocol>_request` --- cho biết handler biết cách tiền xử lý các yêu cầu *protocol*.

     Xem |protocol_request|_ để biết thêm thông tin.

   * :meth:`!<protocol>_response` --- tín hiệu cho biết handler có thể hậu xử lý các phản hồi *protocol*.

     Xem |protocol_response|_ để biết thêm thông tin.

.. |protocol_open| replace:: :meth:`BaseHandler.<protocol>_open`
.. |http_error_nnn| replace:: :meth:`BaseHandler.http_error_\<nnn\>`
.. |protocol_request| replace:: :meth:`BaseHandler.<protocol>_request`
.. |protocol_response| replace:: :meth:`BaseHandler.<protocol>_response`

.. method:: OpenerDirector.open(url, data=None[, timeout])

   Mở *url* đã cho (có thể là một request object hoặc một chuỗi), tùy chọn truyền *data* đã cho. Các đối số, giá trị trả về và ngoại lệ được nêu giống như của :func:`urlopen` (phương thức này chỉ gọi phương thức :meth:`open` trên :class:`OpenerDirector` toàn cục hiện được cài đặt). Tham số *timeout* tùy chọn chỉ định thời gian chờ tính bằng giây cho các thao tác chặn như cố gắng kết nối (nếu không được chỉ định, thiết lập thời gian chờ mặc định toàn cục sẽ được sử dụng). Tính năng thời gian chờ thực sự chỉ hoạt động với các kết nối HTTP, HTTPS và FTP.


.. method:: OpenerDirector.error(proto, *args)

   Xử lý lỗi của protocol đã cho. Thao tác này sẽ gọi các error handler đã đăng ký cho protocol đã cho cùng với các đối số đã cho (phụ thuộc vào protocol). Protocol HTTP là một trường hợp đặc biệt, sử dụng mã phản hồi HTTP để xác định error handler cụ thể; hãy tham khảo các phương thức :meth:`!http_error_\<type\>` của các lớp handler.

   Các giá trị trả về và ngoại lệ được nêu giống như của :func:`urlopen`.

Các đối tượng OpenerDirector mở URL theo ba giai đoạn:

Thứ tự gọi các phương thức này trong mỗi giai đoạn được xác định bằng cách sắp xếp các instance của handler.

#. Mọi handler có một phương thức được đặt tên theo dạng :meth:`!<protocol>_request` đều sẽ được gọi phương thức đó để tiền xử lý request.

#. Các handler có một phương thức được đặt tên theo dạng :meth:`!<protocol>_open` sẽ được gọi để xử lý request. Giai đoạn này kết thúc khi một handler либо trả về một giá trị không phải \ :const:`None` (tức là một response), hoặc ném ra một exception (thường là
   :exc:`~urllib.error.URLError`). Các exception được phép lan truyền.

   Trên thực tế, thuật toán trên trước tiên được áp dụng cho các phương thức có tên là
   :meth:`~BaseHandler.default_open`. Nếu tất cả các phương thức như vậy đều trả về :const:`None`, thuật toán sẽ được lặp lại với các phương thức có tên theo dạng :meth:`!<protocol>_open`. Nếu tất cả các phương thức như vậy đều trả về :const:`None`, thuật toán sẽ được lặp lại với các phương thức có tên là
   :meth:`~BaseHandler.unknown_open`.

   Lưu ý rằng việc triển khai các phương thức này có thể bao gồm các lệnh gọi đến
   :class:`OpenerDirector` instance's :meth:`~OpenerDirector.open` và
   các phương thức :meth:`~OpenerDirector.error`.

#. Mọi handler có một phương thức được đặt tên giống như :meth:`!<protocol>_response` đều sẽ gọi phương thức đó để xử lý hậu kỳ response.


.. _base-handler-objects:

Đối tượng BaseHandler
---------------------

Các đối tượng :class:`BaseHandler` cung cấp một số phương thức hữu ích khi sử dụng trực tiếp, cùng những phương thức khác dành cho các lớp dẫn xuất. Các phương thức sau đây được dùng trực tiếp:


.. method:: BaseHandler.add_parent(director)

   Thêm một director làm parent.


.. method:: BaseHandler.close()

   Xóa mọi parent.

Thuộc tính và các phương thức sau đây chỉ nên được sử dụng bởi các lớp dẫn xuất từ
:class:`BaseHandler`.

.. note::

   Đã áp dụng quy ước rằng các lớp con định nghĩa
   các phương thức :meth:`!<protocol>_request` hoặc :meth:`!<protocol>_response` được đặt tên
   :class:`!\*Processor`; tất cả các phương thức khác được đặt tên là :class:`!\*Handler`.


.. attribute:: BaseHandler.parent

   Một :class:`OpenerDirector` hợp lệ, có thể được dùng để mở bằng một giao thức khác hoặc xử lý lỗi.


.. method:: BaseHandler.default_open(req)

   Phương thức này *không* được định nghĩa trong :class:`BaseHandler`, nhưng các lớp con nên định nghĩa nó nếu muốn bắt tất cả URL.

   Nếu được triển khai, phương thức này sẽ được gọi bởi lớp cha
   :class:`OpenerDirector`. Phương thức này phải trả về một đối tượng giống tệp như được mô tả trong giá trị trả về của phương thức :meth:`~OpenerDirector.open` của :class:`OpenerDirector`, hoặc ``None``. Phương thức này phải phát sinh :exc:`~urllib.error.URLError`, trừ khi xảy ra một tình huống thực sự bất thường (ví dụ: :exc:`MemoryError` không nên được ánh xạ tới
   :exc:`~urllib.error.URLError`).

   Phương thức này sẽ được gọi trước bất kỳ phương thức open dành riêng cho giao thức nào.


.. _protocol_open:
.. method:: BaseHandler.<protocol>_open(req)
   :noindex:

   Phương thức này *không* được định nghĩa trong :class:`BaseHandler`, nhưng các lớp con nên định nghĩa nó nếu muốn xử lý các URL sử dụng giao thức đã cho.

   Phương thức này, nếu được định nghĩa, sẽ được gọi bởi :class:`OpenerDirector` cha. Các giá trị trả về phải giống như đối với :meth:`~BaseHandler.default_open`.


.. method:: BaseHandler.unknown_open(req)

   Phương thức này *không* được định nghĩa trong :class:`BaseHandler`, nhưng các lớp con nên định nghĩa nó nếu muốn bắt tất cả các URL không có handler cụ thể nào được đăng ký để mở.

   Phương thức này, nếu được triển khai, sẽ được gọi bởi :attr:`parent`
   :class:`OpenerDirector`. Các giá trị trả về phải giống như đối với
   :meth:`default_open`.


.. method:: BaseHandler.http_error_default(req, fp, code, msg, hdrs)

   Phương thức này *không* được định nghĩa trong :class:`BaseHandler`, nhưng các lớp con nên ghi đè nó nếu muốn cung cấp một handler tổng quát cho các lỗi HTTP chưa được xử lý theo cách khác. Nó sẽ được :class:`OpenerDirector` nhận lỗi gọi tự động và thông thường không nên được gọi trong các trường hợp khác.

   :class:`OpenerDirector` sẽ gọi phương thức này với năm đối số vị trí:

   1. một đối tượng :class:`Request`,
   #. một đối tượng giống tệp chứa nội dung phần thân lỗi HTTP,
   #. mã lỗi gồm ba chữ số, dưới dạng chuỗi,
   #. phần giải thích về mã lỗi mà người dùng có thể nhìn thấy, dưới dạng chuỗi, và
   #. các header của lỗi, dưới dạng một đối tượng ánh xạ.

   Các giá trị trả về và ngoại lệ được phát sinh phải giống với
   :func:`urlopen`.


.. _http_error_nnn:
.. method:: BaseHandler.http_error_<nnn>(req, fp, code, msg, hdrs)

   *nnn* phải là mã lỗi HTTP gồm ba chữ số. Phương thức này cũng không được định nghĩa trong :class:`BaseHandler`, nhưng sẽ được gọi, nếu tồn tại, trên một instance của lớp con khi xảy ra lỗi HTTP có mã *nnn*.

   Các lớp con nên override phương thức này để xử lý các lỗi HTTP cụ thể.

   Các đối số, giá trị trả về và ngoại lệ được phát sinh phải giống như đối với
   :meth:`~BaseHandler.http_error_default`.


.. _protocol_request:
.. method:: BaseHandler.<protocol>_request(req)
   :noindex:

   Phương thức này *không* được định nghĩa trong :class:`BaseHandler`, nhưng các lớp con nên định nghĩa nó nếu muốn tiền xử lý các request của protocol đã cho.

   Phương thức này, nếu được định nghĩa, sẽ được gọi bởi :class:`OpenerDirector` cha. *req* sẽ là một đối tượng :class:`Request`. Giá trị trả về phải là một
   :class:`Request` đối tượng.


.. _protocol_response:
.. method:: BaseHandler.<protocol>_response(req, response)
   :noindex:

   Phương thức này *không* được định nghĩa trong :class:`BaseHandler`, nhưng các lớp con nên định nghĩa nó nếu muốn hậu xử lý các response của protocol đã cho.

   Phương thức này, nếu được định nghĩa, sẽ được parent :class:`OpenerDirector` gọi. *req* sẽ là một đối tượng :class:`Request`. *response* sẽ là một đối tượng triển khai cùng interface với giá trị trả về của :func:`urlopen`. Giá trị trả về phải triển khai cùng interface với giá trị trả về của
   :func:`urlopen`.


.. _http-redirect-handler:

Đối tượng HTTPRedirectHandler
-----------------------------

.. note::

   Một số chuyển hướng HTTP yêu cầu mã client của mô-đun này thực hiện hành động. Nếu đúng như vậy, :exc:`~urllib.error.HTTPError` sẽ được nâng lên. Xem :rfc:`2616` để biết ý nghĩa chính xác của các mã chuyển hướng khác nhau.

   Một ngoại lệ :exc:`~urllib.error.HTTPError` được nâng lên vì lý do bảo mật nếu HTTPRedirectHandler nhận được một URL đã chuyển hướng không phải là URL HTTP, HTTPS hoặc FTP.


.. method:: HTTPRedirectHandler.redirect_request(req, fp, code, msg, hdrs, newurl)

   Trả về một :class:`Request` hoặc ``None`` để phản hồi một chuyển hướng. Phương thức này được các triển khai mặc định của những phương thức :meth:`!http_error_30\*` gọi khi nhận được chuyển hướng từ máy chủ. Nếu cần thực hiện chuyển hướng, hãy trả về một :class:`Request` mới để cho phép :meth:`!http_error_30\*` thực hiện chuyển hướng đến *newurl*. Nếu không, hãy nâng lên :exc:`~urllib.error.HTTPError` nếu không có handler nào khác nên thử xử lý URL này, hoặc trả về ``None`` nếu bạn không thể xử lý nhưng một handler khác có thể làm được.

   .. note::

      Triển khai mặc định của phương thức này không hoàn toàn tuân theo :rfc:`2616`, trong đó quy định rằng các phản hồi 301 và 302 đối với yêu cầu ``POST`` không được tự động chuyển hướng nếu chưa có xác nhận của người dùng. Trên thực tế, trình duyệt vẫn cho phép tự động chuyển hướng các phản hồi này, chuyển POST thành ``GET``, và triển khai mặc định mô phỏng hành vi này.


.. method:: HTTPRedirectHandler.http_error_301(req, fp, code, msg, hdrs)

   Chuyển hướng đến URL ``Location:`` hoặc ``URI:``. Phương thức này được parent :class:`OpenerDirector` gọi khi nhận được phản hồi HTTP "moved permanently".


.. method:: HTTPRedirectHandler.http_error_302(req, fp, code, msg, hdrs)

   Giống như :meth:`http_error_301`, nhưng được gọi cho phản hồi 'found'.


.. method:: HTTPRedirectHandler.http_error_303(req, fp, code, msg, hdrs)

   Giống như :meth:`http_error_301`, nhưng được gọi cho phản hồi 'see other'.


.. method:: HTTPRedirectHandler.http_error_307(req, fp, code, msg, hdrs)

   Giống như :meth:`http_error_301`, nhưng được gọi cho phản hồi 'temporary redirect'. Không cho phép thay đổi phương thức request từ ``POST`` thành ``GET``.


.. method:: HTTPRedirectHandler.http_error_308(req, fp, code, msg, hdrs)

   Giống như :meth:`http_error_301`, nhưng được gọi cho phản hồi 'permanent redirect'. Không cho phép thay đổi phương thức request từ ``POST`` thành ``GET``.

   .. versionadded:: 3.11


.. _http-cookie-processor:

Các đối tượng HTTPCookieProcessor
---------------------------------

Các instance của :class:`HTTPCookieProcessor` có một thuộc tính:

.. attribute:: HTTPCookieProcessor.cookiejar

   :class:`http.cookiejar.CookieJar` nơi lưu trữ cookie.


.. _proxy-handler:

Đối tượng ProxyHandler
----------------------


.. method:: ProxyHandler.<protocol>_open(request)
   :noindex:

   :class:`ProxyHandler` sẽ có một phương thức :meth:`!<protocol>_open` cho mỗi *protocol* có proxy trong từ điển *proxies* được cung cấp trong hàm khởi tạo. Phương thức này sẽ sửa đổi các request để đi qua proxy bằng cách gọi ``request.set_proxy()``, rồi gọi handler tiếp theo trong chuỗi để thực sự thực thi protocol.


.. _http-password-mgr:

Đối tượng HTTPPasswordMgr
-------------------------

Các phương thức này có sẵn trên :class:`HTTPPasswordMgr` và
các đối tượng :class:`HTTPPasswordMgrWithDefaultRealm`.


.. method:: HTTPPasswordMgr.add_password(realm, uri, user, passwd)

   *uri* có thể là một URI đơn hoặc một chuỗi URI. *realm*, *user* và *passwd* phải là các chuỗi. Điều này khiến ``(user, passwd)`` được sử dụng làm token xác thực khi thông tin xác thực cho *realm* và một super-URI của bất kỳ URI nào đã cho được cung cấp. Nếu một URI bao gồm scheme, thông tin xác thực của URI đó chỉ khớp với các URI xác thực có cùng scheme hoặc không có scheme. URI không có scheme khớp với các URI xác thực sử dụng bất kỳ scheme nào.

   .. versionchanged:: 3.14.8
      Thông tin xác thực cho các URI có scheme hiện được giới hạn theo scheme đó.


.. method:: HTTPPasswordMgr.find_user_password(realm, authuri)

   Lấy user/password cho realm và URI đã cho, nếu có. Phương thức này sẽ trả về ``(None, None)`` nếu không có user/password nào khớp.

   Đối với các đối tượng :class:`HTTPPasswordMgrWithDefaultRealm`, realm ``None`` sẽ được tìm kiếm nếu *realm* đã cho không có user/password nào khớp.


.. _http-password-mgr-with-prior-auth:

Đối tượng HTTPPasswordMgrWithPriorAuth
--------------------------------------

Trình quản lý password này mở rộng :class:`HTTPPasswordMgrWithDefaultRealm` để hỗ trợ theo dõi các URI mà thông tin xác thực luôn được gửi đến.


.. method:: HTTPPasswordMgrWithPriorAuth.add_password(realm, uri, user, \
            passwd, is_authenticated=False)

   *realm*, *uri*, *user*, *passwd* tương tự như
   :meth:`HTTPPasswordMgr.add_password`. *is_authenticated* đặt giá trị ban đầu của cờ ``is_authenticated`` cho URI hoặc danh sách URI đã cho. Nếu *is_authenticated* được chỉ định là ``True``, *realm* sẽ bị bỏ qua.


.. method:: HTTPPasswordMgrWithPriorAuth.find_user_password(realm, authuri)

   Giống như đối với các đối tượng :class:`HTTPPasswordMgrWithDefaultRealm`


.. method:: HTTPPasswordMgrWithPriorAuth.update_authenticated(self, uri, \
            is_authenticated=False)

   Cập nhật cờ ``is_authenticated`` cho *uri* hoặc danh sách URI đã cho.


.. method:: HTTPPasswordMgrWithPriorAuth.is_authenticated(self, authuri)

   Trả về trạng thái hiện tại của cờ ``is_authenticated`` cho URI đã cho.


.. _abstract-basic-auth-handler:

Các đối tượng AbstractBasicAuthHandler
--------------------------------------


.. method:: AbstractBasicAuthHandler.http_error_auth_reqed(authreq, host, req, headers)

   Xử lý yêu cầu xác thực bằng cách lấy một cặp tên người dùng/mật khẩu rồi thử lại yêu cầu. *authreq* phải là tên của tiêu đề chứa thông tin về realm trong yêu cầu, *host* chỉ định URL và đường dẫn cần xác thực, *req* phải là đối tượng :class:`Request` (không thành công), còn *headers* phải là các tiêu đề lỗi.

   *headers* phải là một đối tượng dạng mapping hỗ trợ tra cứu không phân biệt chữ hoa chữ thường và triển khai phương thức ``get_all()``, chẳng hạn như :class:`email.message.Message` hoặc :class:`wsgiref.headers.Headers`.

   *host* либо là một authority (ví dụ: ``"python.org"``) hoặc một URL chứa thành phần authority (ví dụ: ``"https://python.org/"``). Trong cả hai trường hợp, authority không được chứa thành phần userinfo (vì vậy, ``"python.org"`` và ``"python.org:80"`` là hợp lệ, còn ``"joe:password@python.org"`` thì không).


.. _http-basic-auth-handler:

HTTPBasicAuthHandler Objects
----------------------------


.. method:: HTTPBasicAuthHandler.http_error_401(req, fp, code,  msg, hdrs)

   Thử lại yêu cầu với thông tin xác thực, nếu có.


.. _proxy-basic-auth-handler:

ProxyBasicAuthHandler Objects
-----------------------------


.. method:: ProxyBasicAuthHandler.http_error_407(req, fp, code,  msg, hdrs)

   Thử lại yêu cầu với thông tin xác thực, nếu có.


.. _abstract-digest-auth-handler:

AbstractDigestAuthHandler Objects
---------------------------------


.. method:: AbstractDigestAuthHandler.http_error_auth_reqed(authreq, host, req, headers)

   *authreq* phải là tên của header chứa thông tin về realm trong yêu cầu, *host* phải là host cần xác thực, *req* phải là đối tượng :class:`Request` (đã thất bại), và *headers* phải là các header lỗi.

   *headers* phải là một đối tượng dạng mapping có khả năng tra cứu không phân biệt chữ hoa chữ thường, chẳng hạn như :class:`email.message.Message` hoặc :class:`wsgiref.headers.Headers`.


.. _http-digest-auth-handler:

Đối tượng HTTPDigestAuthHandler
-------------------------------


.. method:: HTTPDigestAuthHandler.http_error_401(req, fp, code,  msg, hdrs)

   Thử lại yêu cầu kèm thông tin xác thực, nếu có.


.. _proxy-digest-auth-handler:

Đối tượng ProxyDigestAuthHandler
--------------------------------


.. method:: ProxyDigestAuthHandler.http_error_407(req, fp, code,  msg, hdrs)

   Thử lại yêu cầu kèm thông tin xác thực, nếu có.


.. _http-handler-objects:

Đối tượng HTTPHandler
---------------------


.. method:: HTTPHandler.http_open(req)

   Gửi một yêu cầu HTTP, có thể là GET hoặc POST, tùy thuộc vào ``req.data``.


.. _https-handler-objects:

Đối tượng HTTPSHandler
----------------------


.. method:: HTTPSHandler.https_open(req)

   Gửi một yêu cầu HTTPS, có thể là GET hoặc POST, tùy thuộc vào ``req.data``.


.. _file-handler-objects:

Đối tượng FileHandler
---------------------


.. method:: FileHandler.file_open(req)

   Mở tệp cục bộ nếu không có tên máy chủ hoặc tên máy chủ là ``'localhost'``.

   .. versionchanged:: 3.2
      Phương thức này chỉ áp dụng cho các tên máy chủ cục bộ. Khi cung cấp tên máy chủ từ xa, một :exc:`~urllib.error.URLError` sẽ được phát sinh.


.. _data-handler-objects:

Đối tượng DataHandler
---------------------

.. method:: DataHandler.data_open(req)

   Đọc một data URL. Loại URL này chứa nội dung được mã hóa ngay trong chính URL. Cú pháp data URL được quy định trong :rfc:`2397`. Bản triển khai này bỏ qua khoảng trắng trong các data URL được mã hóa bằng base64, vì vậy URL có thể được ngắt dòng tùy theo tệp nguồn chứa nó. Tuy nhiên, dù một số trình duyệt không gặp vấn đề với việc thiếu phần đệm ở cuối data URL được mã hóa bằng base64, bản triển khai này sẽ phát sinh :exc:`ValueError` trong trường hợp đó.


.. _ftp-handler-objects:

Đối tượng FTPHandler
--------------------


.. method:: FTPHandler.ftp_open(req)

   Mở tệp FTP được chỉ định bởi *req*. Việc đăng nhập luôn được thực hiện với tên người dùng và mật khẩu trống.


.. _cacheftp-handler-objects:

Đối tượng CacheFTPHandler
-------------------------

Các đối tượng :class:`CacheFTPHandler` là các đối tượng :class:`FTPHandler` với những phương thức bổ sung sau:


.. method:: CacheFTPHandler.setTimeout(t)

   Đặt thời gian chờ của các kết nối thành *t* giây.


.. method:: CacheFTPHandler.setMaxConns(m)

   Đặt số lượng kết nối được lưu trong bộ nhớ đệm tối đa thành *m*.


.. _unknown-handler-objects:

Đối tượng UnknownHandler
------------------------


.. method:: UnknownHandler.unknown_open()

   Ném một ngoại lệ :exc:`~urllib.error.URLError`.


.. _http-error-processor-objects:

Các đối tượng HTTPErrorProcessor
--------------------------------

.. method:: HTTPErrorProcessor.http_response(request, response)

   Xử lý các phản hồi lỗi HTTP.

   Đối với các mã lỗi 200, đối tượng phản hồi được trả về ngay lập tức.

   Đối với các mã lỗi khác 200, phương thức này chỉ chuyển việc xử lý cho
   các phương thức xử lý :meth:`!http_error_\<type\>`, thông qua :meth:`OpenerDirector.error`. Cuối cùng, :class:`HTTPDefaultErrorHandler` sẽ ném một
   :exc:`~urllib.error.HTTPError` nếu không có trình xử lý nào khác xử lý lỗi này.


.. method:: HTTPErrorProcessor.https_response(request, response)

   Xử lý các phản hồi lỗi HTTPS.

   Hành vi giống với :meth:`http_response`.


.. _urllib-request-examples:

Ví dụ
-----

Ngoài các ví dụ dưới đây, còn có thêm ví dụ trong
:ref:`urllib-howto`.

Ví dụ này lấy trang chính của python.org và hiển thị 300 byte đầu tiên của trang đó::

   >>> import urllib.request
   >>> with urllib.request.urlopen('https://www.python.org/') as f:
   ...     # Phản hồi có thể được nén (ví dụ: 'gzip').
   ...     print(f.headers.get('Content-Encoding'))
   ...     data = f.read()
   ...     if f.headers.get('Content-Encoding') == 'gzip':
   ...         import gzip
   ...         data = gzip.decompress(data)
   ...     print(data[:300].decode('utf-8', errors='replace'))

Lưu ý rằng urlopen trả về một đối tượng bytes. Điều này là do urlopen không có cách nào tự động xác định encoding của luồng byte nhận được từ máy chủ HTTP. Nhìn chung, chương trình sẽ giải mã đối tượng bytes đã trả về thành chuỗi sau khi xác định hoặc phỏng đoán encoding phù hợp.

Tài liệu đặc tả HTML sau đây, https://html.spec.whatwg.org/#charset, liệt kê các cách khác nhau mà một tài liệu HTML hoặc XML có thể đã chỉ định thông tin encoding của nó.

Để biết thêm thông tin, hãy xem tài liệu W3C: https://www.w3.org/International/questions/qa-html-encoding-declarations.

Vì website python.org sử dụng encoding *utf-8* như được chỉ định trong thẻ meta, chúng ta sẽ dùng cùng encoding này để giải mã đối tượng bytes::

   >>> with urllib.request.urlopen('https://www.python.org/') as f:
   ...     # Kiểm tra việc nén và giải mã cho phù hợp.
   ...     enc = f.headers.get('Content-Encoding')
   ...     data = f.read()
   ...     if enc == 'gzip':
   ...         import gzip
   ...         data = gzip.decompress(data)
   ...     print(data[:100].decode('utf-8', errors='replace'))
   ...

Cũng có thể đạt được kết quả tương tự mà không sử dụng
:term:`context manager` cách tiếp cận::

   >>> import urllib.request
   >>> f = urllib.request.urlopen('https://www.python.org/')
   >>> try:
   ...     enc = f.headers.get('Content-Encoding')
   ...     data = f.read()
   ...     if enc == 'gzip':
   ...         import gzip
   ...         data = gzip.decompress(data)
   ...     print(data[:100].decode('utf-8', errors='replace'))
   ... finally:
   ...     f.close()

Trong ví dụ sau, chúng ta gửi một data-stream đến stdin của một CGI và đọc dữ liệu mà nó trả về. Lưu ý rằng ví dụ này chỉ hoạt động khi bản cài đặt Python hỗ trợ SSL.::

   >>> import urllib.request
   >>> req = urllib.request.Request(url='https://localhost/cgi-bin/test.cgi',
   ...                       data=b'This data is passed to stdin of the CGI')
   >>> with urllib.request.urlopen(req) as f:
   ...     print(f.read().decode('utf-8'))
   ...
   Got Data: "This data is passed to stdin of the CGI"

Mã cho CGI mẫu được sử dụng trong ví dụ trên là::

   #!/usr/bin/env python
   import sys
   data = sys.stdin.read()
   print('Content-type: text/plain\n\nGot Data: "%s"' % data)

Dưới đây là ví dụ về việc thực hiện một yêu cầu ``PUT`` bằng :class:`Request`::

    import urllib.request
    DATA = b'some data'
    req = urllib.request.Request(url='http://localhost:8080', data=DATA, method='PUT')
    with urllib.request.urlopen(req) as f:
        pass
    print(f.status)
    print(f.reason)

Sử dụng Basic HTTP Authentication::

   import urllib.request
   # Tạo một OpenerDirector có hỗ trợ Basic HTTP Authentication...
   auth_handler = urllib.request.HTTPBasicAuthHandler()
   auth_handler.add_password(realm='PDQ Application',
                             uri='https://mahler:8092/site-updates.py',
                             user='klem',
                             passwd='kadidd!ehopper')
   opener = urllib.request.build_opener(auth_handler)
   # ...và cài đặt nó trên toàn cục để có thể sử dụng với urlopen.
   urllib.request.install_opener(opener)
   with urllib.request.urlopen('http://www.example.com/login.html') as f:
       print(f.read().decode('utf-8'))

:func:`build_opener` cung cấp nhiều handler theo mặc định, bao gồm một
:class:`ProxyHandler`. Theo mặc định, :class:`ProxyHandler` sử dụng các biến môi trường có tên ``<scheme>_proxy``, trong đó ``<scheme>`` là lược đồ URL liên quan. Ví dụ: biến môi trường :envvar:`!http_proxy` được đọc để lấy URL của HTTP proxy.

Ví dụ này thay thế :class:`ProxyHandler` mặc định bằng một phiên bản sử dụng các URL proxy được cung cấp theo cách lập trình, đồng thời bổ sung hỗ trợ xác thực proxy với
:class:`ProxyBasicAuthHandler`. ::

   proxy_handler = urllib.request.ProxyHandler({'http': 'http://www.example.com:3128/'})
   proxy_auth_handler = urllib.request.ProxyBasicAuthHandler()
   proxy_auth_handler.add_password('realm', 'host', 'username', 'password')

   opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
   # Lần này, thay vì cài đặt OpenerDirector, chúng ta sử dụng trực tiếp:
   with opener.open('http://www.example.com/login.html') as f:
      print(f.read().decode('utf-8'))

Thêm các HTTP header:

Sử dụng đối số *headers* cho constructor :class:`Request`, hoặc::

   import urllib.request
   req = urllib.request.Request('http://www.example.com/')
   req.add_header('Referer', 'https://www.python.org/')
   # Tùy chỉnh giá trị header User-Agent mặc định:
   req.add_header('User-Agent', 'urllib-example/0.1 (Contact: . . .)')
   with urllib.request.urlopen(req) as f:
       print(f.read().decode('utf-8'))


:class:`OpenerDirector` tự động thêm một header :mailheader:`User-Agent` vào mọi :class:`Request`.  Để thay đổi giá trị này::

   import urllib.request
   opener = urllib.request.build_opener()
   opener.addheaders = [('User-agent', 'Mozilla/5.0')]
   with opener.open('http://www.example.com/') as f:
      print(f.read().decode('utf-8'))

Ngoài ra, hãy nhớ rằng một số header tiêu chuẩn (:mailheader:`Content-Length`,
:mailheader:`Content-Type` và :mailheader:`Host`) được thêm vào khi :class:`Request` được truyền cho :func:`urlopen` (hoặc
:meth:`OpenerDirector.open`).

.. _urllib-examples:

Sau đây là một phiên làm việc mẫu sử dụng phương thức ``GET`` để truy xuất một URL chứa các tham số::

   >>> import urllib.request
   >>> import urllib.parse
   >>> params = urllib.parse.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
   >>> url = "https://www.python.org/?%s" % params
   >>> with urllib.request.urlopen(url) as f:
   ...     print(f.read().decode('utf-8'))
   ...

Ví dụ sau sử dụng phương thức ``POST`` thay thế. Lưu ý rằng đầu ra params từ urlencode được mã hóa thành bytes trước khi được gửi đến urlopen dưới dạng data::

   >>> import urllib.request
   >>> import urllib.parse
   >>> data = urllib.parse.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
   >>> data = data.encode('ascii')
   >>> with urllib.request.urlopen("https://httpbin.org/post", data) as f:
   ...     print(f.read().decode('utf-8'))
   ...

Ví dụ sau sử dụng một HTTP proxy được chỉ định rõ ràng, ghi đè các thiết lập môi trường::

   >>> import urllib.request
   >>> proxies = {'http': 'http://proxy.example.com:8080/'}
   >>> opener = urllib.request.build_opener(urllib.request.ProxyHandler(proxies))
   >>> with opener.open("https://www.python.org") as f:
   ...     f.read().decode('utf-8')
   ...

Ví dụ sau hoàn toàn không sử dụng proxy nào, ghi đè các thiết lập môi trường::

   >>> import urllib.request
   >>> opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
   >>> with opener.open("https://www.python.org/") as f:
   ...     f.read().decode('utf-8')
   ...


Giao diện cũ
------------

Các hàm và lớp sau đây được chuyển từ module ``urllib`` của Python 2 (thay vì ``urllib2``). Chúng có thể trở nên lỗi thời vào một thời điểm nào đó trong tương lai.

.. function:: urlretrieve(url, filename=None, reporthook=None, data=None)

   Sao chép một đối tượng mạng được biểu thị bằng URL vào một tệp cục bộ. Nếu URL trỏ đến một tệp cục bộ, đối tượng sẽ không được sao chép trừ khi cung cấp filename. Trả về một tuple ``(filename, headers)``, trong đó *filename* là tên tệp cục bộ mà tại đó có thể tìm thấy đối tượng, còn *headers* là kết quả mà phương thức :meth:`!info` của đối tượng do :func:`urlopen` trả về (đối với đối tượng từ xa). Các ngoại lệ cũng giống như đối với :func:`urlopen`.

   Đối số thứ hai, nếu có, chỉ định vị trí tệp để sao chép đến (nếu không có, vị trí sẽ là một tempfile với tên được tạo tự động). Đối số thứ ba, nếu có, là một callable sẽ được gọi một lần khi thiết lập kết nối mạng và một lần sau mỗi lần đọc một block. Callable này sẽ nhận ba đối số: số block đã truyền cho đến thời điểm đó, kích thước block tính bằng byte và tổng kích thước của tệp. Đối số thứ ba có thể là ``-1`` trên các máy chủ FTP cũ không trả về kích thước tệp trong phản hồi cho một yêu cầu truy xuất.

   Ví dụ sau minh họa trường hợp sử dụng phổ biến nhất::

      >>> import urllib.request
      >>> local_filename, headers = urllib.request.urlretrieve('https://python.org/')
      >>> html = open(local_filename)
      >>> html.close()

   Nếu *url* sử dụng mã định danh lược đồ :file:`http:`, có thể cung cấp đối số *data* tùy chọn để chỉ định một yêu cầu ``POST`` (thông thường, loại yêu cầu là ``GET``). Đối số *data* phải là một đối tượng bytes ở định dạng chuẩn
   :mimetype:`application/x-www-form-urlencoded`; hãy xem
   hàm :func:`urllib.parse.urlencode`.

   :func:`urlretrieve` sẽ phát sinh :exc:`~urllib.error.ContentTooShortError` khi phát hiện lượng dữ liệu khả dụng ít hơn lượng dự kiến (là kích thước được báo cáo bởi một header *Content-Length*). Điều này có thể xảy ra, chẳng hạn như khi quá trình tải xuống bị gián đoạn.

   *Content-Length* được xem là giới hạn dưới: nếu còn nhiều dữ liệu hơn cần đọc, urlretrieve sẽ đọc thêm dữ liệu, nhưng nếu có ít dữ liệu hơn, nó sẽ phát sinh ngoại lệ.

   Trong trường hợp này, bạn vẫn có thể lấy dữ liệu đã tải xuống; dữ liệu được lưu trong
   thuộc tính :attr:`!content` của thực thể ngoại lệ.

   Nếu không cung cấp header *Content-Length*, urlretrieve không thể kiểm tra kích thước dữ liệu đã tải xuống và chỉ trả về dữ liệu đó. Trong trường hợp này, bạn chỉ cần giả định rằng quá trình tải xuống đã thành công.

.. function:: urlcleanup()

   Dọn dẹp các tệp tạm có thể còn sót lại từ những lần gọi :func:`urlretrieve` trước đó. Hàm này cũng đặt lại opener toàn cục mặc định được cài đặt bởi :func:`install_opener`.


:mod:`!urllib.request` Các hạn chế
----------------------------------

.. index::
   pair: HTTP; protocol
   pair: FTP; protocol

* Hiện tại, chỉ các giao thức sau được hỗ trợ: HTTP (phiên bản 0.9 và 1.0), FTP, tệp cục bộ và URL dữ liệu.

  .. versionchanged:: 3.4 Đã bổ sung hỗ trợ cho data URL.

* Tính năng caching của :func:`urlretrieve` đã bị vô hiệu hóa cho đến khi có người dành thời gian triển khai việc xử lý đúng các header thời gian hết hạn.

* Nên có một hàm để truy vấn xem một URL cụ thể có nằm trong cache hay không.

* Để đảm bảo khả năng tương thích ngược, nếu một URL có vẻ trỏ đến một tệp cục bộ nhưng không thể mở tệp đó, URL sẽ được diễn giải lại bằng giao thức FTP. Điều này đôi khi có thể gây ra các thông báo lỗi khó hiểu.

* Các hàm :func:`urlopen` và :func:`urlretrieve` có thể gây ra độ trễ tùy ý trong khi chờ thiết lập kết nối mạng. Điều này có nghĩa là rất khó xây dựng một web client tương tác bằng các hàm này nếu không sử dụng thread.

  .. index::
     single: HTML
     pair: HTTP; protocol

* Dữ liệu được :func:`urlopen` hoặc :func:`urlretrieve` trả về là dữ liệu thô do máy chủ trả về. Dữ liệu này có thể là dữ liệu nhị phân (chẳng hạn như một hình ảnh), văn bản thuần túy hoặc (ví dụ) HTML. Giao thức HTTP cung cấp thông tin kiểu trong header phản hồi, có thể kiểm tra bằng cách xem header :mailheader:`Content-Type`. Nếu dữ liệu trả về là HTML, bạn có thể sử dụng module
  :mod:`html.parser` để phân tích dữ liệu đó.

  .. index:: single: FTP

* Mã xử lý giao thức FTP không thể phân biệt giữa tệp và thư mục. Điều này có thể dẫn đến hành vi không mong muốn khi cố đọc một URL trỏ đến tệp không thể truy cập. Nếu URL kết thúc bằng ``/``, URL đó được giả định là trỏ đến một thư mục và sẽ được xử lý tương ứng. Tuy nhiên, nếu việc cố đọc một tệp dẫn đến lỗi 550 (nghĩa là không tìm thấy URL hoặc URL không thể truy cập, thường do lý do quyền truy cập), thì đường dẫn sẽ được xử lý như một thư mục để xử lý trường hợp URL chỉ định một thư mục nhưng thiếu ``/`` ở cuối. Điều này có thể gây ra kết quả sai lệch khi bạn cố lấy một tệp mà quyền đọc khiến tệp không thể truy cập; mã FTP sẽ cố đọc tệp đó, gặp lỗi 550, rồi thực hiện liệt kê thư mục đối với tệp không thể đọc. Nếu cần quyền kiểm soát chi tiết, hãy cân nhắc sử dụng module :mod:`ftplib`.



:mod:`!urllib.response` --- Các lớp response được urllib sử dụng
================================================================

.. module:: urllib.response
   :synopsis: Các lớp response được urllib sử dụng.

Module :mod:`!urllib.response` định nghĩa các hàm và lớp cung cấp một giao diện tối thiểu tương tự tệp, bao gồm ``read()`` và ``readline()``. Các hàm được định nghĩa bởi module này được module :mod:`!urllib.request` sử dụng nội bộ. Đối tượng response thông thường là một thực thể :class:`urllib.response.addinfourl`:

.. class:: addinfourl

   .. attribute:: url

      URL của tài nguyên đã truy xuất, thường được dùng để xác định liệu một chuyển hướng có được thực hiện hay không.

   .. attribute:: headers

      Trả về các header của response dưới dạng một thực thể :class:`~email.message.EmailMessage`.

   .. attribute:: status

      .. versionadded:: 3.9

      Mã trạng thái do máy chủ trả về.

   .. method:: geturl()

      .. deprecated:: 3.9
         Đã lỗi thời và được thay thế bằng :attr:`~addinfourl.url`.

   .. method:: info()

      .. deprecated:: 3.9
         Đã lỗi thời và được thay thế bằng :attr:`~addinfourl.headers`.

   .. attribute:: code

      .. deprecated:: 3.9
         Đã lỗi thời và được thay thế bằng :attr:`~addinfourl.status`.

   .. method:: getcode()

      .. deprecated:: 3.9
         Đã lỗi thời và được thay thế bằng :attr:`~addinfourl.status`.

.. _`Requests package`: https://requests.readthedocs.io/en/master/
