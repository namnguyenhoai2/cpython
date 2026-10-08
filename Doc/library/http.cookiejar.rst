:mod:`!http.cookiejar` --- Xử lý cookie cho HTTP client
=======================================================

.. module:: http.cookiejar
   :synopsis: Các lớp để tự động xử lý cookie HTTP.

.. moduleauthor:: John J. Lee <jjl@pobox.com>
.. sectionauthor:: John J. Lee <jjl@pobox.com>

**Mã nguồn:** :source:`Lib/http/cookiejar.py`

--------------

Module :mod:`!http.cookiejar` định nghĩa các lớp để tự động xử lý cookie HTTP. Module này hữu ích khi truy cập các website yêu cầu những phần dữ liệu nhỏ -- :dfn:`cookie` -- được một phản hồi HTTP từ web server thiết lập trên máy client, sau đó được gửi lại cho server trong các yêu cầu HTTP tiếp theo.

Cả giao thức cookie Netscape thông thường và giao thức được định nghĩa bởi
:rfc:`2965` đều được hỗ trợ. Việc xử lý RFC 2965 bị tắt theo mặc định.
Cookie :rfc:`2109` được phân tích cú pháp như cookie Netscape, sau đó được xử lý dưới dạng cookie Netscape hoặc RFC 2965 tùy theo 'policy' đang có hiệu lực. Lưu ý rằng phần lớn cookie trên internet là cookie Netscape.
:mod:`!http.cookiejar` cố gắng tuân theo giao thức cookie Netscape trên thực tế (giao thức này khác biệt đáng kể so với giao thức được nêu trong đặc tả Netscape ban đầu), bao gồm cả việc lưu ý đến các thuộc tính cookie ``max-age`` và ``port`` được giới thiệu cùng với RFC 2965.

.. note::

   Các tham số được đặt tên khác nhau được tìm thấy trong :mailheader:`Set-Cookie` và
   các header :mailheader:`Set-Cookie2` (ví dụ: ``domain`` và ``expires``) theo quy ước được gọi là các :dfn:`attributes`. Để phân biệt chúng với các thuộc tính Python, tài liệu của module này sử dụng thuật ngữ
   :dfn:`cookie-attribute` thay thế.


Module định nghĩa ngoại lệ sau:


.. exception:: LoadError

   Các instance của :class:`FileCookieJar` sẽ phát sinh ngoại lệ này khi không thể tải cookie từ một tệp. :exc:`LoadError` là một lớp con của :exc:`OSError`.

   .. versionchanged:: 3.3
      :exc:`LoadError` used to be a subtype of :exc:`IOError`, which is now an
      bí danh của :exc:`OSError`.


Các lớp sau được cung cấp:


.. class:: CookieJar(policy=None)

   *policy* là một đối tượng triển khai giao diện :class:`CookiePolicy`.

   Lớp :class:`CookieJar` lưu trữ cookie HTTP. Lớp này trích xuất cookie từ các yêu cầu HTTP và trả về chúng trong các phản hồi HTTP. Các thực thể :class:`CookieJar` tự động làm hết hạn các cookie chứa bên trong khi cần. Các lớp con cũng chịu trách nhiệm lưu trữ và truy xuất cookie từ một tệp hoặc cơ sở dữ liệu.


.. class:: FileCookieJar(filename=None, delayload=None, policy=None)

   *policy* là một đối tượng triển khai giao diện :class:`CookiePolicy`. Đối với các đối số khác, hãy xem tài liệu về các thuộc tính tương ứng.

   Một :class:`CookieJar` có thể tải cookie từ, và có thể lưu cookie vào, một tệp trên đĩa. Cookie **NOT** chưa được tải từ tệp đã chỉ định cho đến khi một trong hai
   phương thức :meth:`load` hoặc :meth:`revert` được gọi. Các lớp con của lớp này được mô tả trong phần :ref:`file-cookie-jar-classes`.

   Không nên khởi tạo lớp này trực tiếp – thay vào đó, hãy sử dụng các lớp con bên dưới.

   .. versionchanged:: 3.8

      Tham số filename hỗ trợ một :term:`path-like object`.


.. class:: CookiePolicy()

   Lớp này chịu trách nhiệm quyết định xem từng cookie có nên được máy chủ chấp nhận hoặc nhận lại hay không.


.. class:: DefaultCookiePolicy( blocked_domains=None, allowed_domains=None, netscape=True, rfc2965=False, rfc2109_as_netscape=None, hide_cookie2=False, strict_domain=False, strict_rfc2965_unverifiable=True, strict_ns_unverifiable=False, strict_ns_domain=DefaultCookiePolicy.DomainLiberal, strict_ns_set_initial_dollar=False, strict_ns_set_path=False, secure_protocols=("https", "wss") )

   Chỉ được truyền các đối số của hàm khởi tạo dưới dạng đối số từ khóa. *blocked_domains* là một chuỗi các tên miền mà chúng tôi không bao giờ chấp nhận cookie từ đó hoặc gửi cookie đến đó. *allowed_domains* nếu không phải là ``None``, đây là một chuỗi chỉ gồm các tên miền mà chúng tôi chấp nhận và gửi cookie đến. *secure_protocols* là một chuỗi các giao thức mà cookie bảo mật có thể được thêm vào. Theo mặc định, *https* và *wss* (websocket bảo mật) được xem là các giao thức bảo mật. Đối với tất cả các đối số khác, hãy xem tài liệu về
   các đối tượng :class:`CookiePolicy` và :class:`DefaultCookiePolicy`.

   :class:`DefaultCookiePolicy` triển khai các quy tắc chấp nhận / từ chối tiêu chuẩn cho cookie Netscape và cookie :rfc:`2965`. Theo mặc định, cookie :rfc:`2109` (tức là cookie nhận được trong tiêu đề :mailheader:`Set-Cookie` với thuộc tính cookie phiên bản là
   1) được xử lý theo các quy tắc RFC 2965. Tuy nhiên, nếu việc xử lý RFC 2965
   bị tắt hoặc :attr:`rfc2109_as_netscape` là ``True``, cookie RFC 2109 sẽ được thực thể :class:`CookieJar` hạ cấp thành cookie Netscape bằng cách đặt thuộc tính :attr:`~Cookie.version` của thực thể :class:`Cookie` thành 0.
   :class:`DefaultCookiePolicy` cũng cung cấp một số tham số để cho phép tinh chỉnh chính sách.


.. class:: Cookie()

   Lớp này đại diện cho cookie Netscape, :rfc:`2109` và :rfc:`2965`. Người dùng :mod:`!http.cookiejar` không được kỳ vọng sẽ tự tạo các instance :class:`Cookie`. Thay vào đó, nếu cần, hãy gọi :meth:`~CookieJar.make_cookies` trên một
   instance :class:`CookieJar`.


.. seealso::

   Mô-đun :mod:`urllib.request`
      Mở URL với tính năng xử lý cookie tự động.

   Mô-đun :mod:`http.cookies`
      Các lớp cookie HTTP, chủ yếu hữu ích cho mã phía máy chủ. The
      Các mô-đun :mod:`!http.cookiejar` và :mod:`http.cookies` không phụ thuộc lẫn nhau.

   https://curl.se/rfc/cookie_spec.html
      Đặc tả của giao thức cookie Netscape nguyên bản. Mặc dù đây vẫn là giao thức được sử dụng phổ biến nhất, “giao thức cookie Netscape” được tất cả các trình duyệt lớn (và :mod:`!http.cookiejar`) triển khai chỉ có nét tương đồng sơ lược với giao thức được phác thảo trong ``cookie_spec.html``.

   :rfc:`2109` - Cơ chế quản lý trạng thái HTTP
      Đã lỗi thời bởi :rfc:`2965`. Sử dụng :mailheader:`Set-Cookie` với version=1.

   :rfc:`2965` - Cơ chế quản lý trạng thái HTTP
      Giao thức Netscape đã được sửa lỗi. Sử dụng :mailheader:`Set-Cookie2` thay cho :mailheader:`Set-Cookie`. Không được sử dụng rộng rãi.

   https://kristol.org/cookie/errata.html
      Các đính chính chưa hoàn thiện cho :rfc:`2965`.

   :rfc:`2964` - Sử dụng quản lý trạng thái HTTP

.. _cookie-jar-objects:

Các đối tượng CookieJar và FileCookieJar
----------------------------------------

Các đối tượng :class:`CookieJar` hỗ trợ giao thức :term:`iterator` để lặp qua các đối tượng :class:`Cookie` chứa bên trong.

:class:`CookieJar` có các phương thức sau:


.. method:: CookieJar.add_cookie_header(request)

   Thêm header :mailheader:`Cookie` chính xác vào *request*.

   Nếu policy cho phép (nghĩa là :attr:`~CookiePolicy.rfc2965` và
   các thuộc tính :attr:`~CookiePolicy.hide_cookie2` của instance :class:`CookieJar`'s :class:`CookiePolicy` lần lượt là true và false), header :mailheader:`Cookie2` cũng được thêm vào khi thích hợp.

   Đối tượng *request* (thường là một :class:`urllib.request.Request` instance) phải hỗ trợ các phương thức :meth:`~urllib.request.Request.get_full_url`,
   :meth:`~urllib.request.Request.has_header`,
   :meth:`~urllib.request.Request.get_header`,
   :meth:`~urllib.request.Request.header_items`,
   :meth:`~urllib.request.Request.add_unredirected_header` và các thuộc tính :attr:`~urllib.request.Request.host`,
   :attr:`~urllib.request.Request.type`, :attr:`~urllib.request.Request.unverifiable` và :attr:`~urllib.request.Request.origin_req_host` theo tài liệu của
   :mod:`urllib.request`.

   .. versionchanged:: 3.3

    Đối tượng *request* cần thuộc tính :attr:`~urllib.request.Request.origin_req_host`. Sự phụ thuộc vào một phương thức đã lỗi thời
    :meth:`!get_origin_req_host` đã bị loại bỏ.


.. method:: CookieJar.extract_cookies(response, request)

   Trích xuất cookie từ *response* HTTP và lưu trữ chúng trong :class:`CookieJar`, khi chính sách cho phép.

   :class:`CookieJar` sẽ tìm các :mailheader:`Set-Cookie` được phép và
   :mailheader:`Set-Cookie2` các header trong đối số *response*, và lưu cookie khi thích hợp (phụ thuộc vào việc phương thức :meth:`CookiePolicy.set_ok` chấp thuận).

   Đối tượng *response* (thường là kết quả của một lệnh gọi đến
   :meth:`urllib.request.urlopen`, hoặc tương tự) phải hỗ trợ một
   phương thức :meth:`~http.client.HTTPResponse.info`, trả về một
   instance :class:`email.message.Message`.

   Đối tượng *request* (thường là một instance :class:`urllib.request.Request`) phải hỗ trợ phương thức :meth:`~urllib.request.Request.get_full_url` và các thuộc tính :attr:`~urllib.request.Request.host`,
   :attr:`~urllib.request.Request.unverifiable` và :attr:`~urllib.request.Request.origin_req_host`, như được :mod:`urllib.request` ghi lại. Request được dùng để đặt các giá trị mặc định cho thuộc tính cookie, cũng như kiểm tra xem cookie có được phép đặt hay không.

   .. versionchanged:: 3.3

    Đối tượng *request* cần thuộc tính :attr:`~urllib.request.Request.origin_req_host`. Sự phụ thuộc vào một phương thức đã lỗi thời
    :meth:`!get_origin_req_host` đã bị loại bỏ.

.. method:: CookieJar.set_policy(policy)

   Đặt instance :class:`CookiePolicy` sẽ được sử dụng.


.. method:: CookieJar.make_cookies(response, request)

   Trả về sequence các đối tượng :class:`Cookie` được trích xuất từ đối tượng *response*.

   Xem tài liệu về :meth:`extract_cookies` để biết các interface cần thiết cho các đối số *response* và *request*.


.. method:: CookieJar.set_cookie_if_ok(cookie, request)

   Đặt một :class:`Cookie` nếu policy cho phép.


.. method:: CookieJar.set_cookie(cookie)

   Đặt một :class:`Cookie` mà không kiểm tra policy để xác định có nên đặt hay không.


.. method:: CookieJar.clear([domain[, path[, name]]])

   Xóa một số cookie.

   Nếu được gọi mà không có đối số, phương thức sẽ xóa tất cả cookie. Nếu được cung cấp một đối số, chỉ các cookie thuộc *domain* đó mới bị xóa. Nếu được cung cấp hai đối số, các cookie thuộc *domain* và URL *path* được chỉ định sẽ bị xóa. Nếu được cung cấp ba đối số, cookie có *domain*, *path* và *name* được chỉ định sẽ bị xóa.

   Phát sinh :exc:`KeyError` nếu không tồn tại cookie phù hợp.


.. method:: CookieJar.clear_session_cookies()

   Xóa tất cả cookie phiên.

   Xóa tất cả cookie chứa có thuộc tính :attr:`~Cookie.discard` mang giá trị true (thường là vì chúng không có thuộc tính cookie ``max-age`` hoặc ``expires``, hoặc có thuộc tính cookie ``discard`` rõ ràng). Đối với các trình duyệt tương tác, kết thúc một phiên thường tương ứng với việc đóng cửa sổ trình duyệt.

   Lưu ý rằng phương thức :meth:`~FileCookieJar.save` dù sao cũng không lưu cookie phiên, trừ khi bạn yêu cầu ngược lại bằng cách truyền đối số *ignore_discard* mang giá trị true.

:class:`FileCookieJar` triển khai các phương thức bổ sung sau:


.. method:: FileCookieJar.save(filename=None, ignore_discard=False, ignore_expires=False)

   Lưu cookie vào một tệp.

   Lớp cơ sở này phát sinh :exc:`NotImplementedError`. Các lớp con có thể không triển khai phương thức này.

   *filename* là tên của tệp dùng để lưu cookie. Nếu không chỉ định *filename*, :attr:`self.filename <FileCookieJar.filename>` sẽ được sử dụng (mặc định là giá trị được truyền cho hàm khởi tạo, nếu có); nếu
   :attr:`self.filename <FileCookieJar.filename>` là ``None``,
   :exc:`ValueError` được phát sinh.

   *ignore_discard*: lưu cả những cookie được đặt để loại bỏ. *ignore_expires*: lưu cả những cookie đã hết hạn

   Tệp sẽ bị ghi đè nếu đã tồn tại, do đó xóa toàn bộ cookie chứa trong đó. Cookie đã lưu có thể được khôi phục sau bằng :meth:`load` hoặc
   Các phương thức :meth:`revert`.


.. method:: FileCookieJar.load(filename=None, ignore_discard=False, ignore_expires=False)

   Tải cookie từ một tệp.

   Các cookie cũ được giữ lại, trừ khi bị ghi đè bởi các cookie mới được tải.

   Các đối số giống như trong :meth:`save`.

   Tệp được chỉ định phải ở định dạng mà lớp này hiểu được, nếu không
   :exc:`LoadError` sẽ được phát sinh. Ngoài ra, :exc:`OSError` cũng có thể được phát sinh, chẳng hạn nếu tệp không tồn tại.

   .. versionchanged:: 3.3
      :exc:`IOError` used to be raised, it is now an alias of :exc:`OSError`.


.. method:: FileCookieJar.revert(filename=None, ignore_discard=False, ignore_expires=False)

   Xóa tất cả cookie và tải lại cookie từ một tệp đã lưu.

   :meth:`revert` có thể phát sinh các ngoại lệ giống như :meth:`load`. Nếu xảy ra lỗi, trạng thái của đối tượng sẽ không bị thay đổi.

Các thực thể :class:`FileCookieJar` có những thuộc tính công khai sau:


.. attribute:: FileCookieJar.filename

   Tên tệp mặc định dùng để lưu cookie. Có thể gán giá trị cho thuộc tính này.


.. attribute:: FileCookieJar.delayload

   Nếu là true, tải cookie một cách lazy từ đĩa. Không nên gán giá trị cho thuộc tính này. Đây chỉ là một gợi ý, vì nó chỉ ảnh hưởng đến hiệu năng chứ không ảnh hưởng đến hành vi (trừ khi cookie trên đĩa đang thay đổi). Một đối tượng :class:`CookieJar` có thể bỏ qua thuộc tính này. Không có lớp :class:`FileCookieJar` nào trong thư viện chuẩn tải cookie một cách lazy.


.. _file-cookie-jar-classes:

Các lớp con của FileCookieJar và khả năng phối hợp với trình duyệt web
----------------------------------------------------------------------

Các lớp con :class:`CookieJar` sau đây được cung cấp để đọc và ghi.

.. class:: MozillaCookieJar(filename=None, delayload=None, policy=None)

   Một :class:`FileCookieJar` có thể tải cookie từ đĩa và lưu cookie vào đĩa theo định dạng tệp ``cookies.txt`` của Mozilla (định dạng này cũng được curl và các trình duyệt Lynx và Netscape sử dụng).

   .. note::

      Điều này làm mất thông tin về cookie :rfc:`2965`, cũng như các thuộc tính cookie mới hơn hoặc không theo tiêu chuẩn như ``port``.

   .. warning::

      Hãy sao lưu cookie trước khi lưu nếu bạn có những cookie mà việc mất hoặc hỏng chúng sẽ gây bất tiện (có một số điểm tinh tế có thể dẫn đến những thay đổi nhỏ trong tệp sau một vòng tải / lưu).

   Cũng lưu ý rằng các cookie được lưu trong khi Mozilla đang chạy sẽ bị Mozilla ghi đè.


.. class:: LWPCookieJar(filename=None, delayload=None, policy=None)

   Một :class:`FileCookieJar` có thể tải cookie từ đĩa và lưu cookie vào đĩa theo định dạng tương thích với định dạng tệp ``Set-Cookie3`` của thư viện libwww-perl. Điều này tiện lợi nếu bạn muốn lưu cookie trong một tệp mà con người có thể đọc được.

   .. versionchanged:: 3.8

      Tham số filename hỗ trợ một :term:`path-like object`.

.. _cookie-policy-objects:

Các đối tượng CookiePolicy
--------------------------

Các đối tượng triển khai giao diện :class:`CookiePolicy` có các phương thức sau:


.. method:: CookiePolicy.set_ok(cookie, request)

   Trả về giá trị boolean cho biết cookie có nên được máy chủ chấp nhận hay không.

   *cookie* là một instance :class:`Cookie`. *request* là một đối tượng triển khai interface được định nghĩa trong tài liệu dành cho
   :meth:`CookieJar.extract_cookies`.


.. method:: CookiePolicy.return_ok(cookie, request)

   Trả về giá trị boolean cho biết cookie có nên được gửi về máy chủ hay không.

   *cookie* là một instance :class:`Cookie`. *request* là một đối tượng triển khai interface được định nghĩa trong tài liệu dành cho
   :meth:`CookieJar.add_cookie_header`.


.. method:: CookiePolicy.domain_return_ok(domain, request)

   Trả về ``False`` nếu không nên gửi cookie về máy chủ, với miền cookie đã cho.

   Phương thức này là một tối ưu hóa. Phương thức này loại bỏ nhu cầu kiểm tra từng cookie có cùng một miền cụ thể (việc này có thể liên quan đến việc đọc nhiều tệp). Việc trả về true từ :meth:`domain_return_ok` và :meth:`path_return_ok` giao toàn bộ công việc cho :meth:`return_ok`.

   Nếu :meth:`domain_return_ok` trả về true cho miền cookie,
   :meth:`path_return_ok` được gọi cho đường dẫn cookie. Nếu không thì,
   :meth:`path_return_ok` và :meth:`return_ok` không bao giờ được gọi cho miền cookie đó. Nếu :meth:`path_return_ok` trả về true, :meth:`return_ok` được gọi với chính đối tượng :class:`Cookie` để kiểm tra đầy đủ. Nếu không thì,
   :meth:`return_ok` không bao giờ được gọi cho đường dẫn cookie đó.

   Lưu ý rằng :meth:`domain_return_ok` được gọi cho mọi miền *cookie*, không chỉ miền *request*. Ví dụ: hàm có thể được gọi với cả ``".example.com"`` và ``"www.example.com"`` nếu miền yêu cầu là ``"www.example.com"``. Điều tương tự cũng áp dụng cho :meth:`path_return_ok`.

   Đối số *request* được mô tả như trong tài liệu của :meth:`return_ok`.


.. method:: CookiePolicy.path_return_ok(path, request)

   Trả về ``False`` nếu không nên trả về cookie, dựa trên đường dẫn cookie.

   Xem tài liệu của :meth:`domain_return_ok`.

Ngoài việc triển khai các phương thức trên, các triển khai của
giao diện :class:`CookiePolicy` cũng phải cung cấp các thuộc tính sau, cho biết nên sử dụng những protocol nào và sử dụng như thế nào. Có thể gán giá trị cho tất cả các thuộc tính này.


.. attribute:: CookiePolicy.netscape

   Triển khai protocol Netscape.


.. attribute:: CookiePolicy.rfc2965

   Triển khai protocol :rfc:`2965`.


.. attribute:: CookiePolicy.hide_cookie2

   Không thêm header :mailheader:`Cookie2` vào các request (sự hiện diện của header này cho máy chủ biết rằng chúng ta hiểu cookie :rfc:`2965`).

Cách hữu ích nhất để định nghĩa một class :class:`CookiePolicy` là tạo subclass từ :class:`DefaultCookiePolicy` và override một số hoặc tất cả các phương thức trên. Bản thân :class:`CookiePolicy` có thể được dùng làm 'null policy' để cho phép thiết lập và nhận mọi cookie (điều này khó có khả năng hữu ích).


.. _default-cookie-policy-objects:

Các đối tượng DefaultCookiePolicy
---------------------------------

Triển khai các quy tắc tiêu chuẩn để chấp nhận và trả về cookie.

Cả cookie :rfc:`2965` và cookie Netscape đều được hỗ trợ. Việc xử lý RFC 2965 bị tắt theo mặc định.

Cách dễ nhất để cung cấp policy của riêng bạn là kế thừa class này và gọi các phương thức của nó trong các triển khai đã ghi đè trước khi thêm các kiểm tra bổ sung của riêng bạn::

   import http.cookiejar
   class MyCookiePolicy(http.cookiejar.DefaultCookiePolicy):
       def set_ok(self, cookie, request):
           if not http.cookiejar.DefaultCookiePolicy.set_ok(self, cookie, request):
               return False
           if i_dont_want_to_store_this_cookie(cookie):
               return False
           return True

Ngoài các tính năng cần thiết để triển khai interface :class:`CookiePolicy`, class này cho phép bạn chặn và cho phép các domain thiết lập và nhận cookie. Ngoài ra còn có một số tùy chọn strictness cho phép bạn siết chặt hơn một chút các quy tắc khá lỏng lẻo của giao thức Netscape (đổi lại, một số cookie vô hại có thể bị chặn).

Có một blocklist và allowlist cho domain (cả hai đều bị tắt theo mặc định). Chỉ những domain không có trong blocklist và có trong allowlist (nếu allowlist đang hoạt động) mới tham gia vào việc thiết lập và trả về cookie. Sử dụng đối số khởi tạo *blocked_domains*, cùng với :meth:`~DefaultCookiePolicy.blocked_domains` và
các phương thức :meth:`~DefaultCookiePolicy.set_blocked_domains` (và đối số cũng như các phương thức tương ứng cho *allowed_domains*). Nếu bạn thiết lập allowlist, bạn có thể tắt lại bằng cách đặt nó thành ``None``.

Các domain trong blocklist hoặc allowlist không bắt đầu bằng dấu chấm phải khớp chính xác với domain của cookie. Ví dụ, ``"example.com"`` khớp với mục ``"example.com"`` trong blocklist, nhưng ``"www.example.com"`` thì không. Các domain bắt đầu bằng dấu chấm cũng được khớp với những domain cụ thể hơn. Ví dụ, cả ``"www.example.com"`` và ``"www.coyote.example.com"`` đều khớp với ``".example.com"`` (nhưng bản thân ``"example.com"`` thì không). Địa chỉ IP là ngoại lệ và phải khớp chính xác. Ví dụ, nếu blocked_domains chứa ``"192.168.1.2"`` và ``".168.1.2"``, thì 192.168.1.2 bị chặn, còn 193.168.1.2 thì không.

:class:`DefaultCookiePolicy` triển khai các phương thức bổ sung sau:


.. method:: DefaultCookiePolicy.blocked_domains()

   Trả về chuỗi các miền bị chặn (dưới dạng tuple).


.. method:: DefaultCookiePolicy.set_blocked_domains(blocked_domains)

   Đặt chuỗi các miền bị chặn.


.. method:: DefaultCookiePolicy.is_blocked(domain)

   Trả về ``True`` nếu *domain* nằm trong danh sách chặn để thiết lập hoặc nhận cookie.


.. method:: DefaultCookiePolicy.allowed_domains()

   Trả về ``None`` hoặc chuỗi các miền được phép (dưới dạng tuple).


.. method:: DefaultCookiePolicy.set_allowed_domains(allowed_domains)

   Đặt chuỗi các miền được phép hoặc ``None``.


.. method:: DefaultCookiePolicy.is_not_allowed(domain)

   Trả về ``True`` nếu *domain* không nằm trong danh sách cho phép để thiết lập hoặc nhận cookie.

Các instance :class:`DefaultCookiePolicy` có các thuộc tính sau, tất cả đều được khởi tạo từ các đối số constructor có cùng tên và đều có thể được gán giá trị.


.. attribute:: DefaultCookiePolicy.rfc2109_as_netscape

   Nếu là true, yêu cầu instance :class:`CookieJar` hạ cấp cookie :rfc:`2109` (tức là các cookie nhận được trong header :mailheader:`Set-Cookie` với thuộc tính cookie version bằng 1) thành cookie Netscape bằng cách đặt thuộc tính version của instance :class:`Cookie` thành 0. Giá trị mặc định là ``None``, trong trường hợp đó cookie RFC 2109 được hạ cấp khi và chỉ khi việc xử lý :rfc:`2965` bị tắt. Vì vậy, theo mặc định, cookie RFC 2109 được hạ cấp.


Các tùy chọn chuyển đổi mức độ nghiêm ngặt chung:

.. attribute:: DefaultCookiePolicy.strict_domain

   Không cho phép các site đặt miền gồm hai thành phần với top-level domain mã quốc gia như ``.co.uk``, ``.gov.uk``, ``.co.nz``.etc. Cách này còn lâu mới hoàn hảo và không được đảm bảo sẽ hoạt động!


Các tùy chọn chuyển đổi mức độ nghiêm ngặt của giao thức :rfc:`2965`:

.. attribute:: DefaultCookiePolicy.strict_rfc2965_unverifiable

   Tuân theo các quy tắc :rfc:`2965` đối với các giao dịch không thể xác minh (thông thường, giao dịch không thể xác minh là giao dịch phát sinh từ một chuyển hướng hoặc yêu cầu đối với một hình ảnh được lưu trữ trên site khác). Nếu là false, cookie sẽ *không bao giờ* bị chặn dựa trên khả năng xác minh.


Các tùy chọn chuyển đổi mức độ nghiêm ngặt của giao thức Netscape:

.. attribute:: DefaultCookiePolicy.strict_ns_unverifiable

   Áp dụng các quy tắc :rfc:`2965` cho những giao dịch không thể xác minh, kể cả với cookie Netscape.


.. attribute:: DefaultCookiePolicy.strict_ns_domain

   Các cờ cho biết mức độ nghiêm ngặt cần áp dụng với các quy tắc đối sánh domain cho cookie Netscape. Xem bên dưới để biết các giá trị được chấp nhận.


.. attribute:: DefaultCookiePolicy.strict_ns_set_initial_dollar

   Bỏ qua các cookie trong header Set-Cookie: có tên bắt đầu bằng ``'$'``.


.. attribute:: DefaultCookiePolicy.strict_ns_set_path

   Không cho phép thiết lập các cookie có path không path-match với URI yêu cầu.

:attr:`~DefaultCookiePolicy.strict_ns_domain` là một tập hợp các cờ. Giá trị của nó được tạo bằng cách thực hiện phép OR trên các cờ (ví dụ: ``DomainStrictNoDots|DomainStrictNonDomain`` có nghĩa là cả hai cờ đều được thiết lập).


.. attribute:: DefaultCookiePolicy.DomainStrictNoDots

   Khi thiết lập cookie, 'host prefix' không được chứa dấu chấm (ví dụ: ``www.foo.bar.com`` không thể thiết lập cookie cho ``.bar.com``, vì ``www.foo`` chứa dấu chấm).


.. attribute:: DefaultCookiePolicy.DomainStrictNonDomain

   Các cookie không chỉ định rõ ràng thuộc tính cookie ``domain`` chỉ có thể được trả về cho domain bằng với domain đã thiết lập cookie (ví dụ: ``spam.example.com`` sẽ không trả về các cookie từ ``example.com`` không có thuộc tính cookie ``domain``).


.. attribute:: DefaultCookiePolicy.DomainRFC2965Match

   Khi thiết lập cookie, hãy yêu cầu :rfc:`2965` khớp miền đầy đủ.

Các thuộc tính sau được cung cấp để thuận tiện và là những tổ hợp hữu ích nhất của các cờ trên:


.. attribute:: DefaultCookiePolicy.DomainLiberal

   Tương đương với 0 (nghĩa là tất cả các cờ kiểm soát độ nghiêm ngặt miền Netscape ở trên đều được tắt).


.. attribute:: DefaultCookiePolicy.DomainStrict

   Tương đương với ``DomainStrictNoDots|DomainStrictNonDomain``.


Đối tượng Cookie
----------------

Các thực thể :class:`Cookie` có các thuộc tính Python tương ứng gần đúng với những thuộc tính cookie tiêu chuẩn được quy định trong các tiêu chuẩn cookie khác nhau. Sự tương ứng này không hoàn toàn một-một, vì có các quy tắc phức tạp để gán giá trị mặc định, vì các thuộc tính cookie ``max-age`` và ``expires`` chứa thông tin tương đương, và vì cookie :rfc:`2109` có thể bị :mod:`!http.cookiejar` “hạ cấp” từ phiên bản 1 xuống cookie phiên bản 0 (Netscape).

Thông thường không cần gán cho các thuộc tính này, ngoại trừ trong những trường hợp hiếm gặp bên trong một phương thức :class:`CookiePolicy`. Lớp này không đảm bảo tính nhất quán nội bộ, vì vậy nếu làm vậy, bạn cần biết rõ mình đang làm gì.


.. attribute:: Cookie.version

   Số nguyên hoặc ``None``. Cookie Netscape có :attr:`version` bằng 0. :rfc:`2965` và
   Cookie :rfc:`2109` có thuộc tính cookie ``version`` bằng 1. Tuy nhiên, lưu ý rằng
   :mod:`!http.cookiejar` có thể “hạ cấp” cookie RFC 2109 thành cookie Netscape; trong trường hợp đó, :attr:`version` bằng 0.


.. attribute:: Cookie.name

   Tên cookie (một chuỗi).


.. attribute:: Cookie.value

   Giá trị cookie (một chuỗi) hoặc ``None``.


.. attribute:: Cookie.port

   Chuỗi biểu diễn một cổng hoặc một tập hợp các cổng (ví dụ: '80' hoặc '80,8080'), hoặc ``None``.


.. attribute:: Cookie.domain

   Miền cookie (một chuỗi).


.. attribute:: Cookie.path

   Đường dẫn cookie (một chuỗi, ví dụ ``'/acme/rocket_launchers'``).


.. attribute:: Cookie.secure

   ``True`` nếu cookie chỉ nên được trả về qua kết nối bảo mật.


.. attribute:: Cookie.expires

   Ngày hết hạn dạng số nguyên tính bằng giây kể từ epoch, hoặc ``None``. Xem thêm phương thức
   :meth:`is_expired`.


.. attribute:: Cookie.discard

   ``True`` nếu đây là cookie phiên.


.. attribute:: Cookie.comment

   Chuỗi nhận xét từ máy chủ giải thích chức năng của cookie này, hoặc ``None``.


.. attribute:: Cookie.comment_url

   URL liên kết đến nhận xét từ máy chủ giải thích chức năng của cookie này, hoặc ``None``.


.. attribute:: Cookie.rfc2109

   ``True`` nếu cookie này được nhận dưới dạng cookie :rfc:`2109` (nghĩa là cookie đến trong header :mailheader:`Set-Cookie`, và giá trị của thuộc tính cookie Version trong header đó là 1). Thuộc tính này được cung cấp vì
   :mod:`!http.cookiejar` có thể “hạ cấp” cookie RFC 2109 thành cookie Netscape; trong trường hợp đó, :attr:`version` bằng 0.


.. attribute:: Cookie.port_specified

   ``True`` nếu máy chủ đã chỉ định rõ một cổng hoặc một tập hợp các cổng (trong
   :mailheader:`Set-Cookie` / :mailheader:`Set-Cookie2` header).


.. attribute:: Cookie.domain_specified

   ``True`` nếu máy chủ đã chỉ định rõ một domain.


.. attribute:: Cookie.domain_initial_dot

   ``True`` nếu domain được máy chủ chỉ định rõ bắt đầu bằng một dấu chấm (``'.'``).

Cookie có thể có các cookie-attribute không chuẩn bổ sung. Có thể truy cập các thuộc tính này bằng những phương thức sau:


.. method:: Cookie.has_nonstandard_attr(name)

   Trả về ``True`` nếu cookie có thuộc tính cookie được chỉ định.


.. method:: Cookie.get_nonstandard_attr(name, default=None)

   Nếu cookie có thuộc tính cookie được chỉ định, hãy trả về giá trị của thuộc tính đó. Nếu không, hãy trả về *default*.


.. method:: Cookie.set_nonstandard_attr(name, value)

   Đặt giá trị của thuộc tính cookie được chỉ định.

Lớp :class:`Cookie` cũng định nghĩa phương thức sau:


.. method:: Cookie.is_expired(now=None)

   ``True`` nếu cookie đã vượt qua thời điểm mà máy chủ yêu cầu nó hết hạn. Nếu cung cấp *now* (tính bằng giây kể từ epoch), hãy trả về liệu cookie đã hết hạn tại thời điểm được chỉ định hay chưa.


Ví dụ
-----

Ví dụ đầu tiên cho thấy cách sử dụng phổ biến nhất của :mod:`!http.cookiejar`::

   import http.cookiejar, urllib.request
   cj = http.cookiejar.CookieJar()
   opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
   r = opener.open("http://example.com/")

Ví dụ này minh họa cách mở một URL bằng cookie Netscape, Mozilla hoặc Lynx của bạn (giả định quy ước Unix/Netscape về vị trí của tệp cookie)::

   import os, http.cookiejar, urllib.request
   cj = http.cookiejar.MozillaCookieJar()
   cj.load(os.path.join(os.path.expanduser("~"), ".netscape", "cookies.txt"))
   opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
   r = opener.open("http://example.com/")

Ví dụ tiếp theo minh họa cách sử dụng :class:`DefaultCookiePolicy`. Bật
:rfc:`2965` cookie, áp dụng quy định nghiêm ngặt hơn về miền khi thiết lập và trả về cookie Netscape, đồng thời chặn một số miền thiết lập cookie hoặc nhận lại cookie::

   import urllib.request
   from http.cookiejar import CookieJar, DefaultCookiePolicy
   policy = DefaultCookiePolicy(
       rfc2965=True, strict_ns_domain=Policy.DomainStrict,
       blocked_domains=["ads.net", ".ads.net"])
   cj = CookieJar(policy)
   opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
   r = opener.open("http://example.com/")
