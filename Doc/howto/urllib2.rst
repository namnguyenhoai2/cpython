.. _urllib-howto:

*************************************************
HƯỚNG DẪN Lấy tài nguyên Internet bằng gói urllib
*************************************************

:Author: `Michael Foord <https://agileabstractions.com/>`_


Giới thiệu
==========

.. sidebar:: Các bài viết liên quan

    Bạn cũng có thể thấy bài viết sau đây hữu ích khi tìm nạp tài nguyên web bằng Python:

    * `Xác thực cơ bản <https://web.archive.org/web/20201215133350/http://www.voidspace.org.uk/python/articles/authentication.shtml>`__

        Hướng dẫn về *Xác thực cơ bản*, kèm các ví dụ bằng Python.

**urllib.request** là một module Python dùng để tìm nạp URL (Uniform Resource Locators). Module này cung cấp một giao diện rất đơn giản dưới dạng hàm *urlopen*. Hàm này có thể tìm nạp URL bằng nhiều giao thức khác nhau. Module cũng cung cấp một giao diện phức tạp hơn một chút để xử lý các tình huống thường gặp—chẳng hạn như xác thực cơ bản, cookie, proxy, v.v. Các chức năng này được cung cấp thông qua những đối tượng gọi là handler và opener.

urllib.request hỗ trợ tìm nạp URL cho nhiều "lược đồ URL" (được xác định bởi chuỗi đứng trước ``":"`` trong URL—ví dụ ``"ftp"`` là lược đồ URL của ``"ftp://python.org/"``) bằng các giao thức mạng tương ứng (ví dụ: FTP, HTTP). Tutorial này tập trung vào trường hợp phổ biến nhất là HTTP.

Trong các tình huống đơn giản, *urlopen* rất dễ sử dụng. Tuy nhiên, ngay khi gặp lỗi hoặc các trường hợp không đơn giản khi mở URL HTTP, bạn sẽ cần hiểu một số kiến thức về HyperText Transfer Protocol. Tài liệu tham khảo toàn diện và có tính thẩm quyền nhất về HTTP là :rfc:`2616`. Đây là một tài liệu kỹ thuật và không được viết để dễ đọc. HOWTO này nhằm minh họa cách sử dụng *urllib*, đồng thời cung cấp đủ chi tiết về HTTP để hỗ trợ bạn. Tài liệu này không nhằm thay thế tài liệu :mod:`urllib.request`, mà bổ sung cho tài liệu đó.


Tìm nạp URL
===========

Cách đơn giản nhất để sử dụng urllib.request như sau::

    import urllib.request
    with urllib.request.urlopen('http://python.org/') as response:
       html = response.read()

Nếu muốn truy xuất một tài nguyên thông qua URL và lưu tài nguyên đó vào một vị trí tạm thời, bạn có thể thực hiện việc này thông qua :func:`shutil.copyfileobj` và
các hàm :func:`tempfile.NamedTemporaryFile`::

    import shutil
    import tempfile
    import urllib.request

    with urllib.request.urlopen('http://python.org/') as response:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            shutil.copyfileobj(response, tmp_file)

    with open(tmp_file.name) as html:
        pass

Nhiều cách sử dụng urllib sẽ đơn giản như vậy (lưu ý rằng thay vì URL 'http:', chúng ta có thể sử dụng URL bắt đầu bằng 'ftp:', 'file:', v.v.). Tuy nhiên, mục đích của hướng dẫn này là giải thích những trường hợp phức tạp hơn, tập trung vào HTTP.

HTTP dựa trên các request và response - client gửi request, còn server gửi response. urllib.request phản ánh điều này bằng một đối tượng ``Request`` đại diện cho request HTTP mà bạn đang thực hiện. Ở dạng đơn giản nhất, bạn tạo một đối tượng Request chỉ định URL mà bạn muốn truy xuất. Việc gọi ``urlopen`` với đối tượng Request này sẽ trả về một đối tượng response cho URL được yêu cầu. Đây là một đối tượng giống tệp, nghĩa là bạn có thể, chẳng hạn, gọi ``.read()`` trên response::

    import urllib.request

    req = urllib.request.Request('http://python.org/')
    with urllib.request.urlopen(req) as response:
       the_page = response.read()

Lưu ý rằng urllib.request sử dụng cùng một interface Request để xử lý tất cả các lược đồ URL. Ví dụ, bạn có thể tạo một request FTP như sau::

    req = urllib.request.Request('ftp://example.com/')

Trong trường hợp HTTP, các đối tượng Request cho phép bạn thực hiện thêm hai việc: Thứ nhất, bạn có thể truyền dữ liệu đến server. Thứ hai, bạn có thể truyền thêm thông tin ("metadata") *về* dữ liệu hoặc về chính request đó đến server - thông tin này được gửi dưới dạng các "header" HTTP. Hãy lần lượt xem xét từng việc.

Dữ liệu
-------

Đôi khi bạn muốn gửi dữ liệu đến một URL (thường URL này sẽ trỏ đến một script CGI (Common Gateway Interface) hoặc ứng dụng web khác). Với HTTP, việc này thường được thực hiện bằng một request **POST**. Đây thường là việc trình duyệt thực hiện khi bạn gửi một biểu mẫu HTML đã điền trên web. Không phải mọi POST đều phải đến từ biểu mẫu: bạn có thể sử dụng POST để truyền dữ liệu tùy ý đến ứng dụng của riêng mình. Trong trường hợp phổ biến là biểu mẫu HTML, dữ liệu cần được mã hóa theo một cách chuẩn, sau đó truyền cho đối tượng Request dưới dạng đối số ``data``. Việc mã hóa được thực hiện bằng một hàm trong thư viện :mod:`urllib.parse`.::

    import urllib.parse
    import urllib.request

    url = 'http://www.someserver.com/cgi-bin/register.cgi'
    values = {'name' : 'Michael Foord',
              'location' : 'Northampton',
              'language' : 'Python' }

    data = urllib.parse.urlencode(values)
    data = data.encode('ascii') # data phải là bytes
    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as response:
       the_page = response.read()

Lưu ý rằng đôi khi cần các encoding khác (ví dụ: để tải tệp lên từ các biểu mẫu HTML - xem `Đặc tả HTML, Gửi biểu mẫu <https://www.w3.org/TR/REC-html40/interact/forms.html#h-17.13>`_ để biết thêm chi tiết).

Nếu bạn không truyền đối số ``data``, urllib sẽ sử dụng một yêu cầu **GET**. Một điểm khác biệt giữa các yêu cầu GET và POST là các yêu cầu POST thường có "tác dụng phụ": chúng thay đổi trạng thái của hệ thống theo một cách nào đó (ví dụ: đặt hàng với website một hundredweight spam đóng hộp để giao đến tận cửa nhà bạn). Mặc dù tiêu chuẩn HTTP nêu rõ rằng POST được thiết kế để *luôn luôn* gây ra tác dụng phụ, còn các yêu cầu GET *không bao giờ* gây ra tác dụng phụ, nhưng không có gì ngăn cản một yêu cầu GET có tác dụng phụ, cũng như một yêu cầu POST không có tác dụng phụ. Dữ liệu cũng có thể được truyền trong một yêu cầu HTTP GET bằng cách mã hóa dữ liệu ngay trong URL.

Việc này được thực hiện như sau::

    >>> import urllib.request
    >>> import urllib.parse
    >>> data = {}
    >>> data['name'] = 'Somebody Here'
    >>> data['location'] = 'Northampton'
    >>> data['language'] = 'Python'
    >>> url_values = urllib.parse.urlencode(data)
    >>> print(url_values)  # Thứ tự có thể khác với bên dưới.  #doctest: +SKIP
    name=Somebody+Here&language=Python&location=Northampton
    >>> url = 'http://www.example.com/example.cgi'
    >>> full_url = url + '?' + url_values
    >>> data = urllib.request.urlopen(full_url)

Lưu ý rằng URL đầy đủ được tạo bằng cách thêm một ``?`` vào URL, sau đó là các giá trị đã mã hóa.

Tiêu đề
-------

Ở đây, chúng ta sẽ thảo luận về một HTTP header cụ thể để minh họa cách thêm header vào HTTP request của bạn.

Một số website [#]_ không cho phép các chương trình truy cập, hoặc gửi các phiên bản khác nhau đến những trình duyệt khác nhau [#]_. Theo mặc định, urllib tự nhận diện là ``Python-urllib/x.y`` (trong đó ``x`` và ``y`` lần lượt là số phiên bản chính và phụ của bản phát hành Python, ví dụ ``Python-urllib/2.5``), điều này có thể khiến website hiểu nhầm hoặc hoàn toàn không hoạt động. Trình duyệt tự nhận diện thông qua header ``User-Agent`` [#]_. Khi tạo một đối tượng Request, bạn có thể truyền vào một dictionary chứa các header. Ví dụ sau thực hiện cùng request như trên, nhưng tự nhận diện là một phiên bản của Internet Explorer [#]_.::

    import urllib.parse
    import urllib.request

    url = 'http://www.someserver.com/cgi-bin/register.cgi'
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    values = {'name': 'Michael Foord',
              'location': 'Northampton',
              'language': 'Python' }
    headers = {'User-Agent': user_agent}

    data = urllib.parse.urlencode(values)
    data = data.encode('ascii')
    req = urllib.request.Request(url, data, headers)
    with urllib.request.urlopen(req) as response:
       the_page = response.read()

Response cũng có hai phương thức hữu ích. Hãy xem phần `info và geturl <info and geturl_>`_, nằm sau phần chúng ta xem xét điều gì xảy ra khi có lỗi.


Xử lý ngoại lệ
==============

*urlopen* phát sinh :exc:`~urllib.error.URLError` khi không thể xử lý một response (tuy nhiên, như thường lệ với các API Python, những ngoại lệ dựng sẵn như :exc:`ValueError`,
:exc:`TypeError` v.v. cũng có thể được phát sinh).

:exc:`~urllib.error.HTTPError` là lớp con của :exc:`~urllib.error.URLError` được phát sinh trong trường hợp cụ thể của các URL HTTP.

Các lớp ngoại lệ được export từ module :mod:`urllib.error`.

URLError
--------

Thông thường, URLError được phát sinh vì không có kết nối mạng (không có route đến máy chủ được chỉ định) hoặc máy chủ được chỉ định không tồn tại. Trong trường hợp này, exception được phát sinh sẽ có thuộc tính 'reason', là một tuple chứa mã lỗi và thông báo lỗi dạng văn bản.

ví dụ::

    >>> req = urllib.request.Request('http://www.pretend_server.org')
    >>> try: urllib.request.urlopen(req)
    ... except urllib.error.URLError as e:
    ...     print(e.reason)      #doctest: +SKIP
    ...
    (4, 'getaddrinfo failed')


HTTPError
---------

Mọi phản hồi HTTP từ máy chủ đều chứa một "status code" dạng số. Đôi khi status code cho biết máy chủ không thể đáp ứng request. Các handler mặc định sẽ xử lý một số phản hồi này thay bạn (ví dụ: nếu phản hồi là một "redirection" yêu cầu client lấy tài liệu từ URL khác, urllib sẽ xử lý việc đó thay bạn). Với những phản hồi không thể xử lý, urlopen sẽ phát sinh một :exc:`~urllib.error.HTTPError`. Các lỗi thường gặp bao gồm '404' (không tìm thấy trang), '403' (request bị từ chối) và '401' (yêu cầu xác thực).

Xem mục 10 của :rfc:`2616` để tham khảo tất cả các mã lỗi HTTP.

Đối tượng :exc:`~urllib.error.HTTPError` được nâng lên sẽ có thuộc tính 'code' kiểu số nguyên, tương ứng với lỗi do máy chủ gửi về.

Mã lỗi
~~~~~~

Vì các handler mặc định xử lý các redirect (mã trong phạm vi 300), còn các mã trong phạm vi 100--299 biểu thị thành công, nên thông thường bạn chỉ thấy các mã lỗi trong phạm vi 400--599.

:attr:`http.server.BaseHTTPRequestHandler.responses` là một dictionary hữu ích về các mã phản hồi, hiển thị tất cả mã phản hồi được :rfc:`2616` sử dụng. Một phần trích xuất từ dictionary được hiển thị bên dưới::

    responses = {
        ...
        <HTTPStatus.OK: 200>: ('OK', 'Request fulfilled, document follows'),
        ...
        <HTTPStatus.FORBIDDEN: 403>: ('Forbidden',
                                      'Request forbidden -- authorization will '
                                      'not help'),
        <HTTPStatus.NOT_FOUND: 404>: ('Not Found',
                                      'Nothing matches the given URI'),
        ...
        <HTTPStatus.IM_A_TEAPOT: 418>: ("I'm a Teapot",
                                        'Server refuses to brew coffee because '
                                        'it is a teapot'),
        ...
        <HTTPStatus.SERVICE_UNAVAILABLE: 503>: ('Service Unavailable',
                                                'The server cannot process the '
                                                'request due to a high load'),
        ...
        }

Khi xảy ra lỗi, máy chủ phản hồi bằng cách trả về mã lỗi HTTP *và* một trang lỗi. Bạn có thể sử dụng đối tượng :exc:`~urllib.error.HTTPError` làm response trên trang được trả về. Điều này có nghĩa là ngoài thuộc tính code, đối tượng này còn có các phương thức read, geturl và info, giống như các phương thức được trả về bởi module ``urllib.response``::

    >>> req = urllib.request.Request('http://www.python.org/fish.html')
    >>> try:
    ...     urllib.request.urlopen(req)
    ... except urllib.error.HTTPError as e:
    ...     print(e.code)
    ...     print(e.read())  #doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    ...
    404
    b'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
      "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n\n\n<html
      ...
      <title>Page Not Found</title>\n
      ...

Tổng kết
--------

Vì vậy, nếu muốn chuẩn bị cho :exc:`~urllib.error.HTTPError` *hoặc* :exc:`~urllib.error.URLError` thì có hai cách tiếp cận cơ bản. Tôi thích cách tiếp cận thứ hai hơn.

Số 1
~~~~

::


    from urllib.request import Request, urlopen
    from urllib.error import URLError, HTTPError
    req = Request(someurl)
    try:
        response = urlopen(req)
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
    else:
        # mọi thứ đều ổn


.. note::

    ``except HTTPError`` *phải* xuất hiện trước, nếu không ``except URLError`` sẽ *cũng* bắt được một :exc:`~urllib.error.HTTPError`.

Số 2
~~~~

::

    from urllib.request import Request, urlopen
    from urllib.error import URLError
    req = Request(someurl)
    try:
        response = urlopen(req)
    except URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
    else:
        # mọi thứ đều ổn


.. _`info and geturl`:

info and geturl
===============

Phản hồi được trả về bởi urlopen (hoặc instance :exc:`~urllib.error.HTTPError`) có hai phương thức hữu ích là :meth:`!info` và :meth:`!geturl`, và được định nghĩa trong module
:mod:`urllib.response`.

* **geturl** - phương thức này trả về URL thực của trang đã được tìm nạp. Điều này hữu ích vì ``urlopen`` (hoặc đối tượng opener được sử dụng) có thể đã đi theo một chuyển hướng. URL của trang đã được tìm nạp có thể không giống với URL được yêu cầu.

* **info** - phương thức này trả về một đối tượng có dạng như từ điển, mô tả trang đã được tìm nạp, đặc biệt là các header do máy chủ gửi. Hiện tại, đây là một
  :class:`http.client.HTTPMessage` instance.

Các header thường gặp bao gồm 'Content-length', 'Content-type', v.v. Hãy xem `Quick Reference to HTTP Headers <https://jkorpela.fi/http.html>`_ để biết danh sách hữu ích các header HTTP cùng phần giải thích ngắn gọn về ý nghĩa và cách sử dụng của chúng.


Openers và Handlers
===================

Khi tìm nạp một URL, bạn sử dụng một opener (một instance của :class:`urllib.request.OpenerDirector` có tên gọi dễ gây nhầm lẫn). Thông thường, chúng ta đã sử dụng opener mặc định - thông qua ``urlopen`` - nhưng bạn có thể tạo các opener tùy chỉnh. Opener sử dụng handlers. Mọi "phần việc nặng" đều do các handler thực hiện. Mỗi handler biết cách mở URL cho một scheme URL cụ thể (http, ftp, v.v.) hoặc cách xử lý một khía cạnh của việc mở URL, chẳng hạn như chuyển hướng HTTP hoặc cookie HTTP.

Bạn sẽ muốn tạo opener nếu muốn fetch URL bằng các handler cụ thể đã được cài đặt, chẳng hạn như để lấy một opener xử lý cookie hoặc một opener không xử lý chuyển hướng.

Để tạo một opener, hãy khởi tạo một ``OpenerDirector``, sau đó gọi ``.add_handler(some_handler_instance)`` nhiều lần.

Ngoài ra, bạn có thể sử dụng ``build_opener``, đây là một hàm tiện ích để tạo các đối tượng opener chỉ bằng một lần gọi hàm. ``build_opener`` mặc định thêm một số handler, đồng thời cung cấp cách nhanh chóng để thêm handler và/hoặc ghi đè các handler mặc định.

Các loại handler khác mà bạn có thể muốn sử dụng có thể xử lý proxy, authentication và những tình huống phổ biến khác nhưng hơi chuyên biệt.

``install_opener`` có thể được dùng để đặt một đối tượng ``opener`` làm opener mặc định (toàn cục). Điều này có nghĩa là các lệnh gọi đến ``urlopen`` sẽ sử dụng opener mà bạn đã cài đặt.

Các đối tượng opener có một phương thức ``open``, có thể được gọi trực tiếp để fetch URL theo cách giống như hàm ``urlopen``: không cần gọi ``install_opener``, trừ khi muốn dùng cho thuận tiện.


.. _`Basic Authentication`:

Xác thực cơ bản
===============

Để minh họa việc tạo và cài đặt một handler, chúng ta sẽ sử dụng ``HTTPBasicAuthHandler``. Để tìm hiểu chi tiết hơn về chủ đề này -- bao gồm giải thích về cách Basic Authentication hoạt động - hãy xem `Basic Authentication Tutorial <https://web.archive.org/web/20201215133350/http://www.voidspace.org.uk/python/articles/authentication.shtml>`__.

Khi yêu cầu xác thực, server sẽ gửi một header (cũng như mã lỗi 401) yêu cầu xác thực. Header này chỉ định authentication scheme và một 'realm'. Header có dạng: ``WWW-Authenticate: SCHEME realm="REALM"``.

ví dụ:

.. code-block:: none

    WWW-Authenticate: Basic realm="cPanel Users"


Sau đó, client nên thử lại request với tên và mật khẩu phù hợp với realm, được đưa vào request dưới dạng header. Đây là 'basic authentication'. Để đơn giản hóa quy trình này, chúng ta có thể tạo một instance của ``HTTPBasicAuthHandler`` và một opener để sử dụng handler này.

``HTTPBasicAuthHandler`` sử dụng một object gọi là password manager để xử lý ánh xạ giữa URL, realm với mật khẩu và username. Nếu biết realm là gì (từ authentication header do server gửi), bạn có thể sử dụng ``HTTPPasswordMgr``. Thông thường, chúng ta không quan tâm realm là gì. Trong trường hợp đó, sẽ thuận tiện hơn nếu sử dụng ``HTTPPasswordMgrWithDefaultRealm``. Cách này cho phép bạn chỉ định username và mật khẩu mặc định cho một URL. Các thông tin này sẽ được cung cấp nếu bạn không đưa ra một cặp thông tin thay thế cho realm cụ thể. Chúng ta biểu thị điều này bằng cách cung cấp ``None`` làm đối số realm cho phương thức ``add_password``.

URL cấp cao nhất là URL đầu tiên yêu cầu xác thực. Các URL "sâu hơn" URL bạn truyền cho .add_password() cũng sẽ khớp.::

    # tạo password manager
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()

    # Thêm username và password.
    # Nếu biết realm, chúng ta có thể dùng nó thay cho None.
    top_level_url = "http://example.com/foo/"
    password_mgr.add_password(None, top_level_url, username, password)

    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)

    # tạo "opener" (một OpenerDirector instance)
    opener = urllib.request.build_opener(handler)

    # dùng opener để lấy một URL
    opener.open(a_url)

    # Cài đặt opener.
    # Giờ đây, mọi lệnh gọi đến urllib.request.urlopen đều sử dụng opener của chúng ta.
    urllib.request.install_opener(opener)

.. note::

    Trong ví dụ trên, chúng ta chỉ cung cấp ``HTTPBasicAuthHandler`` cho ``build_opener``. Theo mặc định, opener có các handler cho những tình huống thông thường -- ``ProxyHandler`` (nếu một thiết lập proxy như biến môi trường :envvar:`!http_proxy` được đặt), ``UnknownHandler``, ``HTTPHandler``, ``HTTPDefaultErrorHandler``, ``HTTPRedirectHandler``, ``FTPHandler``, ``FileHandler``, ``DataHandler``, ``HTTPErrorProcessor``.

``top_level_url`` thực tế là *hoặc* một URL đầy đủ (bao gồm thành phần scheme 'http:', hostname và tùy chọn số cổng), ví dụ ``"http://example.com/"`` *hoặc* một "authority" (tức là hostname, tùy chọn bao gồm số cổng), ví dụ ``"example.com"`` hoặc ``"example.com:8080"`` (ví dụ sau có bao gồm số cổng). Authority, nếu có, KHÔNG được chứa thành phần "userinfo" - ví dụ ``"joe:password@example.com"`` là không đúng.


Proxy
=====

**urllib** sẽ tự động phát hiện các thiết lập proxy của bạn và sử dụng chúng. Việc này được thực hiện thông qua ``ProxyHandler``, thành phần thuộc chuỗi handler thông thường khi phát hiện có thiết lập proxy. Thông thường, đây là điều hữu ích, nhưng đôi khi có thể không phù hợp [#]_. Một cách để làm vậy là tự thiết lập ``ProxyHandler`` mà không định nghĩa proxy nào. Việc này được thực hiện bằng các bước tương tự như khi thiết lập handler `Basic Authentication <Basic Authentication_>`_:::

    >>> proxy_support = urllib.request.ProxyHandler({})
    >>> opener = urllib.request.build_opener(proxy_support)
    >>> urllib.request.install_opener(opener)

.. note::

    Hiện tại ``urllib.request`` *does not* hỗ trợ truy xuất các location ``https`` thông qua proxy. Tuy nhiên, bạn có thể bật tính năng này bằng cách mở rộng urllib.request như trong công thức [#]_.

.. note::

    ``HTTP_PROXY`` sẽ bị bỏ qua nếu một biến ``REQUEST_METHOD`` được thiết lập; xem tài liệu về :func:`~urllib.request.getproxies`.


Socket và các lớp
=================

Hỗ trợ của Python cho việc truy xuất tài nguyên từ web được phân tầng. urllib sử dụng thư viện :mod:`http.client`, thư viện này lần lượt sử dụng thư viện socket.

Kể từ Python 2.3, bạn có thể chỉ định thời gian một socket chờ phản hồi trước khi hết thời gian chờ. Điều này có thể hữu ích trong các ứng dụng cần tải các trang web. Theo mặc định, module socket có *không có thời gian chờ* và có thể bị treo. Hiện tại, thời gian chờ của socket chưa được cung cấp ở cấp http.client hoặc urllib.request. Tuy nhiên, bạn có thể đặt thời gian chờ mặc định trên toàn cục cho tất cả socket bằng cách sử dụng::

    import socket
    import urllib.request

    # thời gian chờ tính bằng giây
    timeout = 10
    socket.setdefaulttimeout(timeout)

    # lệnh gọi này đến urllib.request.urlopen giờ đây sử dụng thời gian chờ mặc định
    # mà chúng ta đã đặt trong module socket
    req = urllib.request.Request('http://www.voidspace.org.uk')
    response = urllib.request.urlopen(req)


-------


Chú thích cuối trang
====================

Tài liệu này đã được John Lee xem xét và chỉnh sửa.

.. [#] Ví dụ: Google.
.. [#] Browser sniffing là một thực hành rất tồi trong thiết kế website - xây dựng website bằng các web standard hợp lý hơn nhiều. Đáng tiếc là nhiều website vẫn gửi các phiên bản khác nhau đến những trình duyệt khác nhau.
.. [#] User agent của MSIE 6 là *'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)'*
.. [#] Để biết thêm chi tiết về các HTTP request header khác, hãy xem `Tài liệu tham khảo nhanh về HTTP header <Quick Reference to HTTP Headers_>`_.
.. [#] Trong trường hợp của tôi, tôi phải sử dụng proxy để truy cập Internet tại nơi làm việc. Nếu bạn cố gắng fetch các URL *localhost* thông qua proxy này, proxy sẽ chặn chúng. IE được thiết lập để sử dụng proxy và urllib tự động nhận thiết lập này. Để kiểm thử các script với một máy chủ localhost, tôi phải ngăn urllib sử dụng proxy.
.. [#] urllib opener cho SSL proxy (phương thức CONNECT): `ASPN Cookbook Recipe <https://code.activestate.com/recipes/456195-urrlib2-opener-for-ssl-proxy-connect-method/>`_.

.. _`Michael Foord`: https://agileabstractions.com/
.. _`HTML Specification, Form Submission`: https://www.w3.org/TR/REC-html40/interact/forms.html#h-17.13
.. _`Quick Reference to HTTP Headers`: https://jkorpela.fi/http.html
.. _`ASPN Cookbook Recipe`: https://code.activestate.com/recipes/456195-urrlib2-opener-for-ssl-proxy-connect-method/
