:mod:`!urllib.parse` --- Phân tích URL thành các thành phần
===========================================================

.. module:: urllib.parse
   :synopsis: Phân tích URL thành các thành phần hoặc lắp ráp URL từ các thành phần đó.

**Mã nguồn:** :source:`Lib/urllib/parse.py`

.. index::
   single: WWW
   single: World Wide Web
   single: URL
   pair: URL; parsing
   pair: relative; URL

--------------

Mô-đun này định nghĩa một giao diện tiêu chuẩn để tách các chuỗi Uniform Resource Locator (URL) thành các thành phần (scheme định địa chỉ, vị trí mạng, đường dẫn, v.v.), kết hợp các thành phần đó lại thành một chuỗi URL và chuyển đổi một "URL tương đối" thành URL tuyệt đối khi đã cho một "URL cơ sở".

Mô-đun này được thiết kế để phù hợp với RFC Internet về Relative Uniform Resource Locators. Mô-đun hỗ trợ các scheme URL sau: ``file``, ``ftp``, ``gopher``, ``hdl``, ``http``, ``https``, ``imap``, ``itms-services``, ``mailto``, ``mms``, ``news``, ``nntp``, ``prospero``, ``rsync``, ``rtsp``, ``rtsps``, ``rtspu``, ``sftp``, ``shttp``, ``sip``, ``sips``, ``snews``, ``svn``, ``svn+ssh``, ``telnet``, ``wais``, ``ws``, ``wss``.

.. impl-detail::

   Việc bao gồm scheme URL ``itms-services`` có thể khiến một ứng dụng không vượt qua được quy trình xét duyệt của Apple App Store dành cho macOS và iOS. Việc xử lý scheme ``itms-services`` luôn bị loại bỏ trên iOS; trên macOS, nó *có thể* bị loại bỏ nếu CPython được xây dựng với
   :option:`--with-app-store-compliance` option.

Mô-đun :mod:`!urllib.parse` định nghĩa các hàm thuộc hai nhóm chính: phân tích cú pháp URL và trích dẫn URL. Các nội dung này được trình bày chi tiết trong những phần sau.

Các hàm của mô-đun này sử dụng thuật ngữ đã lỗi thời ``netloc`` (hoặc ``net_loc``), được giới thiệu trong :rfc:`1808`. Tuy nhiên, thuật ngữ này đã bị thay thế bởi
:rfc:`3986`, trong đó giới thiệu thuật ngữ ``authority`` để thay thế. Việc sử dụng ``netloc`` vẫn được duy trì để đảm bảo khả năng tương thích ngược.

Phân tích cú pháp URL
---------------------

Các hàm phân tích cú pháp URL tập trung vào việc tách một chuỗi URL thành các thành phần hoặc kết hợp các thành phần URL thành một chuỗi URL.

.. function:: urlsplit(urlstring, scheme=None, allow_fragments=True)

   Phân tích cú pháp một URL thành năm thành phần, trả về một :term:`named tuple` gồm 5 mục
   :class:`SplitResult` hoặc :class:`SplitResultBytes`. Điều này tương ứng với cấu trúc chung của một URL: ``scheme://netloc/path?query#fragment``. Mỗi mục trong tuple là một chuỗi, có thể rỗng.

   Các dấu phân cách như minh họa ở trên không thuộc về kết quả, ngoại trừ dấu gạch chéo đứng đầu trong thành phần *path*, được giữ lại nếu có.

   Ngoài ra, thuộc tính netloc được phân tách thành các thuộc tính bổ sung sau và được thêm vào đối tượng trả về: username, password, hostname và port.

   Các chuỗi được mã hóa theo phần trăm không được giải mã.

   Ví dụ:

   .. doctest::
      :options: +NORMALIZE_WHITESPACE

      >>> from urllib.parse import urlsplit
      >>> urlsplit("scheme://netloc/path?query#fragment")
      SplitResult(scheme='scheme', netloc='netloc', path='/path',
                  query='query', fragment='fragment')
      >>> o = urlsplit("http://docs.python.org:80/3/library/urllib.parse.html?"
      ...              "highlight=params#url-parsing")
      >>> o
      SplitResult(scheme='http', netloc='docs.python.org:80',
                  path='/3/library/urllib.parse.html',
                  query='highlight=params', fragment='url-parsing')
      >>> o.scheme
      'http'
      >>> o.netloc
      'docs.python.org:80'
      >>> o.hostname
      'docs.python.org'
      >>> o.port
      80
      >>> o._replace(fragment="").geturl()
      'http://docs.python.org:80/3/library/urllib.parse.html?highlight=params'

   Theo các đặc tả cú pháp trong :rfc:`1808`, :func:`!urlsplit` chỉ nhận diện netloc nếu nó được giới thiệu đúng bằng '//'. Nếu không, đầu vào được xem là một URL tương đối và do đó bắt đầu bằng một thành phần path.

   .. doctest::
      :options: +NORMALIZE_WHITESPACE

      >>> from urllib.parse import urlsplit
      >>> urlsplit('//www.cwi.nl:80/%7Eguido/Python.html')
      SplitResult(scheme='', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html',
                  query='', fragment='')
      >>> urlsplit('www.cwi.nl/%7Eguido/Python.html')
      SplitResult(scheme='', netloc='', path='www.cwi.nl/%7Eguido/Python.html',
                  query='', fragment='')
      >>> urlsplit('help/Python.html')
      SplitResult(scheme='', netloc='', path='help/Python.html',
                  query='', fragment='')

   Đối số *scheme* cung cấp scheme định địa chỉ mặc định, chỉ được sử dụng nếu URL không chỉ định scheme. Đối số này phải có cùng kiểu (text hoặc bytes) với *urlstring*, ngoại trừ giá trị mặc định ``''`` luôn được cho phép và sẽ tự động được chuyển đổi thành ``b''`` nếu thích hợp.

   Nếu đối số *allow_fragments* là false, các fragment identifier sẽ không được nhận diện. Thay vào đó, chúng được phân tích cú pháp như một phần của thành phần path, parameters hoặc query, và :attr:`fragment` được đặt thành chuỗi rỗng trong giá trị trả về.

   Giá trị trả về là một :term:`named tuple`, nghĩa là các phần tử của nó có thể được truy cập theo chỉ mục hoặc dưới dạng các thuộc tính có tên, bao gồm:

   +------------------+---------+-------------------------------------+----------------------+
   | Thuộc tính       | Chỉ mục | Giá trị                             | Giá trị nếu không có |
   +==================+=========+=====================================+======================+
   | :attr:`scheme`   | 0       | Bộ chỉ định scheme của URL          | tham số *scheme*     |
   +------------------+---------+-------------------------------------+----------------------+
   | :attr:`netloc`   | 1       | Phần vị trí mạng                    | chuỗi rỗng           |
   +------------------+---------+-------------------------------------+----------------------+
   | :attr:`path`     | 2       | Đường dẫn phân cấp                  | chuỗi rỗng           |
   +------------------+---------+-------------------------------------+----------------------+
   | :attr:`query`    | 3       | Thành phần truy vấn                 | chuỗi rỗng           |
   +------------------+---------+-------------------------------------+----------------------+
   | :attr:`fragment` | 4       | Mã định danh fragment               | chuỗi rỗng           |
   +------------------+---------+-------------------------------------+----------------------+
   | :attr:`username` |         | Tên người dùng                      | :const:`None`        |
   +------------------+---------+-------------------------------------+----------------------+
   | :attr:`password` |         | Mật khẩu                            | :const:`None`        |
   +------------------+---------+-------------------------------------+----------------------+
   | :attr:`hostname` |         | Tên máy chủ (chữ thường)            | :const:`None`        |
   +------------------+---------+-------------------------------------+----------------------+
   | :attr:`port`     |         | Số cổng dưới dạng số nguyên, nếu có | :const:`None`        |
   +------------------+---------+-------------------------------------+----------------------+

   Việc đọc thuộc tính :attr:`port` sẽ gây ra :exc:`ValueError` nếu URL chỉ định một cổng không hợp lệ. Xem mục
   :ref:`urlparse-result-object` để biết thêm thông tin về đối tượng kết quả.

   Các dấu ngoặc vuông không khớp trong thuộc tính :attr:`netloc` sẽ gây ra một
   :exc:`ValueError`.

   Các ký tự trong thuộc tính :attr:`netloc` khi phân rã theo chuẩn hóa NFKC (được sử dụng bởi mã hóa IDNA) thành bất kỳ ký tự nào trong số ``/``, ``?``, ``#``, ``@`` hoặc ``:`` sẽ gây ra :exc:`ValueError`. Nếu URL được phân rã trước khi phân tích cú pháp, sẽ không xảy ra lỗi.

   Tuân theo một phần của đặc tả `WHATWG spec <WHATWG spec_>`_ cập nhật :rfc:`3986`, các ký tự điều khiển C0 và ký tự khoảng trắng ở đầu sẽ bị loại bỏ khỏi URL. Các ký tự ``\n``, ``\r`` và tab ``\t`` được xóa khỏi URL ở mọi vị trí.

   Tương tự như mọi named tuple, lớp con có thêm một số phương thức và thuộc tính đặc biệt hữu ích. Một trong những phương thức đó là :meth:`_replace`. Phương thức :meth:`_replace` sẽ trả về một đối tượng :class:`SplitResult` mới, thay thế các trường được chỉ định bằng các giá trị mới.

   .. doctest::
      :options: +NORMALIZE_WHITESPACE

      >>> from urllib.parse import urlsplit
      >>> u = urlsplit('//www.cwi.nl:80/%7Eguido/Python.html')
      >>> u
      SplitResult(scheme='', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html',
                  query='', fragment='')
      >>> u._replace(scheme='http')
      SplitResult(scheme='http', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html',
                  query='', fragment='')

   .. warning::

      :func:`urlsplit` không thực hiện việc xác thực. Xem :ref:`Bảo mật khi phân tích cú pháp URL <url-parsing-security>` để biết chi tiết.

   .. versionchanged:: 3.2
      Đã bổ sung khả năng phân tích cú pháp URL IPv6.

   .. versionchanged:: 3.3
      Giờ đây, fragment được phân tích cú pháp cho tất cả các lược đồ URL (trừ khi *allow_fragments* là false), phù hợp với :rfc:`3986`. Trước đây, tồn tại một allowlist gồm các lược đồ hỗ trợ fragment.

   .. versionchanged:: 3.6
      Số cổng nằm ngoài phạm vi giờ sẽ phát sinh :exc:`ValueError`, thay vì trả về :const:`None`.

   .. versionchanged:: 3.8
      Các ký tự ảnh hưởng đến việc phân tích netloc khi chuẩn hóa theo NFKC giờ sẽ phát sinh :exc:`ValueError`.

   .. versionchanged:: 3.10
      Các ký tự xuống dòng và tab ASCII sẽ bị loại bỏ khỏi URL.

   .. versionchanged:: 3.12
      Các ký tự điều khiển C0 và ký tự khoảng trắng ở đầu theo WHATWG sẽ bị loại bỏ khỏi URL.

.. _WHATWG spec: https://url.spec.whatwg.org/#concept-basic-url-parser


.. function:: parse_qs(qs, keep_blank_values=False, strict_parsing=False, encoding='utf-8', errors='replace', max_num_fields=None, separator='&')

   Phân tích chuỗi truy vấn được cung cấp dưới dạng đối số chuỗi (dữ liệu thuộc kiểu
   :mimetype:`application/x-www-form-urlencoded`).  Dữ liệu được trả về dưới dạng từ điển.  Các khóa của từ điển là tên duy nhất của các biến truy vấn, còn các giá trị là danh sách các giá trị tương ứng với từng tên.

   Đối số tùy chọn *keep_blank_values* là một cờ cho biết liệu các giá trị trống trong truy vấn được mã hóa phần trăm có được xử lý dưới dạng chuỗi trống hay không. Giá trị true cho biết các giá trị trống sẽ được giữ lại dưới dạng chuỗi trống.  Giá trị false mặc định cho biết các giá trị trống sẽ bị bỏ qua và được xử lý như thể chúng không được đưa vào.

   Đối số tùy chọn *strict_parsing* là một cờ cho biết cần xử lý lỗi phân tích cú pháp như thế nào. Nếu là false (mặc định), các lỗi sẽ bị bỏ qua một cách im lặng. Nếu là true, các lỗi sẽ gây ra một ngoại lệ :exc:`ValueError`.

   Các tham số tùy chọn *encoding* và *errors* chỉ định cách giải mã các chuỗi được mã hóa phần trăm thành các ký tự Unicode, theo cách được chấp nhận bởi
   phương thức :meth:`bytes.decode`.

   Đối số tùy chọn *max_num_fields* là số trường tối đa cần đọc. Nếu được đặt, một :exc:`ValueError` sẽ được ném ra nếu số trường được đọc nhiều hơn *max_num_fields*.

   Đối số tùy chọn *separator* là ký hiệu được sử dụng để phân tách các đối số truy vấn. Giá trị mặc định là ``&``.

   Sử dụng hàm :func:`urllib.parse.urlencode` (với tham số ``doseq`` được đặt thành ``True``) để chuyển các từ điển như vậy thành các chuỗi truy vấn.


   .. versionchanged:: 3.2
      Thêm các tham số *encoding* và *errors*.

   .. versionchanged:: 3.8
      Đã thêm tham số *max_num_fields*.

   .. versionchanged:: 3.10
      Đã thêm tham số *separator* với giá trị mặc định là ``&``. Các phiên bản Python trước Python 3.10 cho phép sử dụng cả ``;`` và ``&`` làm dấu phân cách tham số truy vấn. Điều này đã được thay đổi để chỉ cho phép một khóa dấu phân cách duy nhất, với ``&`` là dấu phân cách mặc định.

   .. deprecated:: 3.14
      Việc chấp nhận các đối tượng có giá trị false (chẳng hạn như ``0`` và ``[]``) ngoại trừ chuỗi rỗng, các đối tượng dạng byte và ``None`` hiện đã bị deprecated.


.. function:: parse_qsl(qs, keep_blank_values=False, strict_parsing=False, encoding='utf-8', errors='replace', max_num_fields=None, separator='&')

   Phân tích chuỗi truy vấn được cung cấp dưới dạng đối số chuỗi (dữ liệu thuộc kiểu
   :mimetype:`application/x-www-form-urlencoded`). Dữ liệu được trả về dưới dạng danh sách các cặp tên, giá trị.

   Đối số tùy chọn *keep_blank_values* là một cờ cho biết liệu các giá trị trống trong truy vấn được mã hóa phần trăm có được xử lý dưới dạng chuỗi trống hay không. Giá trị true cho biết các giá trị trống sẽ được giữ lại dưới dạng chuỗi trống.  Giá trị false mặc định cho biết các giá trị trống sẽ bị bỏ qua và được xử lý như thể chúng không được đưa vào.

   Đối số tùy chọn *strict_parsing* là một cờ cho biết cần xử lý lỗi phân tích cú pháp như thế nào. Nếu là false (mặc định), các lỗi sẽ bị bỏ qua một cách im lặng. Nếu là true, các lỗi sẽ gây ra một ngoại lệ :exc:`ValueError`.

   Các tham số tùy chọn *encoding* và *errors* chỉ định cách giải mã các chuỗi được mã hóa phần trăm thành các ký tự Unicode, theo cách được chấp nhận bởi
   phương thức :meth:`bytes.decode`.

   Đối số tùy chọn *max_num_fields* là số trường tối đa cần đọc. Nếu được đặt, một :exc:`ValueError` sẽ được ném ra nếu số trường được đọc nhiều hơn *max_num_fields*.

   Đối số tùy chọn *separator* là ký hiệu được sử dụng để phân tách các đối số truy vấn. Giá trị mặc định là ``&``.

   Sử dụng hàm :func:`urllib.parse.urlencode` để chuyển đổi các danh sách cặp như vậy thành chuỗi truy vấn.

   .. versionchanged:: 3.2
      Thêm các tham số *encoding* và *errors*.

   .. versionchanged:: 3.8
      Đã thêm tham số *max_num_fields*.

   .. versionchanged:: 3.10
      Đã thêm tham số *separator* với giá trị mặc định là ``&``. Các phiên bản Python trước Python 3.10 cho phép sử dụng cả ``;`` và ``&`` làm dấu phân cách tham số truy vấn. Điều này đã được thay đổi để chỉ cho phép một khóa dấu phân cách duy nhất, với ``&`` là dấu phân cách mặc định.


.. function:: urlunsplit(parts)

   Tạo một URL từ một tuple như được trả về bởi ``urlsplit()``. Đối số *parts* có thể là bất kỳ iterable nào gồm năm phần tử. Điều này có thể tạo ra một URL hơi khác nhưng tương đương, nếu URL được phân tích ban đầu có các dấu phân cách không cần thiết (ví dụ: một ``?`` có query rỗng; RFC nêu rằng các URL này tương đương).


.. function:: urlparse(urlstring, scheme=None, allow_fragments=True)

   Điều này tương tự như :func:`urlsplit`, nhưng còn tách thành phần *path* tại *path* và *params*. Hàm này trả về một :term:`named tuple` :class:`ParseResult` gồm 6 phần tử hoặc :class:`ParseResultBytes`. Các phần tử của nó giống với kết quả :func:`!urlsplit`, ngoại trừ *params* được chèn tại chỉ mục 3, giữa *path* và *query*.

   Hàm này dựa trên :rfc:`1738` và :rfc:`1808` đã lỗi thời, trong đó liệt kê *params* là thành phần URL chính. Cú pháp URL mới hơn cho phép áp dụng các tham số cho từng phân đoạn của phần *path* trong URL (xem :rfc:`3986`).
   Nhìn chung nên sử dụng :func:`urlsplit` thay cho :func:`urlparse`. Cần có một hàm riêng để tách các phân đoạn đường dẫn và tham số.

.. function:: urlunparse(parts)

   Kết hợp các phần tử của một tuple như được trả về bởi :func:`urlparse` thành một URL hoàn chỉnh dưới dạng chuỗi. Đối số *parts* có thể là bất kỳ iterable nào gồm sáu phần tử. Điều này có thể tạo ra một URL hơi khác nhưng tương đương, nếu URL được phân tích ban đầu có các dấu phân cách không cần thiết (ví dụ: ? với query rỗng; RFC nêu rằng các URL này tương đương).


.. function:: urljoin(base, url, allow_fragments=True)

   Tạo một URL đầy đủ ("tuyệt đối") bằng cách kết hợp "URL cơ sở" (*base*) với một URL khác (*url*). Nói một cách đơn giản, cách này sử dụng các thành phần của URL cơ sở, đặc biệt là scheme định địa chỉ, vị trí mạng và (một phần của) đường dẫn, để cung cấp các thành phần còn thiếu trong URL tương đối. Ví dụ:

      >>> from urllib.parse import urljoin
      >>> urljoin('http://www.cwi.nl/%7Eguido/Python.html', 'FAQ.html')
      'http://www.cwi.nl/%7Eguido/FAQ.html'

   Đối số *allow_fragments* có cùng ý nghĩa và giá trị mặc định như đối với
   :func:`urlsplit`.

   .. note::

      Nếu *url* là một URL tuyệt đối (nghĩa là bắt đầu bằng ``//`` hoặc ``scheme://``), hostname và/hoặc scheme của *url* sẽ xuất hiện trong kết quả. Ví dụ:

      .. doctest::

         >>> urljoin('http://www.cwi.nl/%7Eguido/Python.html',
         ...         '//www.python.org/%7Eguido')
         'http://www.python.org/%7Eguido'

      Nếu không muốn hành vi đó, hãy tiền xử lý *url* bằng :func:`urlsplit` và
      :func:`urlunsplit`, loại bỏ các phần *scheme* và *netloc* nếu có.

   .. warning::

      Vì một URL tuyệt đối có thể được truyền làm tham số ``url``, việc sử dụng ``urljoin`` với ``url`` do kẻ tấn công kiểm soát thường **không an toàn**. Ví dụ, trong ``urljoin("https://website.com/users/", username)``, nếu ``username`` có thể chứa một URL tuyệt đối, kết quả của ``urljoin`` sẽ là URL tuyệt đối đó.


   .. versionchanged:: 3.5

      Hành vi đã được cập nhật để phù hợp với các ngữ nghĩa được định nghĩa trong :rfc:`3986`.


.. function:: urldefrag(url)

   Nếu *url* chứa mã định danh fragment, hãy trả về một phiên bản đã sửa đổi của *url* không có mã định danh fragment và mã định danh fragment dưới dạng một chuỗi riêng biệt. Nếu *url* không chứa mã định danh fragment, hãy trả về *url* không sửa đổi và một chuỗi rỗng.

   Giá trị trả về là một :term:`named tuple`, các phần tử của nó có thể được truy cập theo chỉ mục hoặc dưới dạng các thuộc tính có tên:

   +------------------+---------+-----------------------+----------------------+
   | Thuộc tính       | Chỉ mục | Giá trị               | Giá trị nếu không có |
   +==================+=========+=======================+======================+
   | :attr:`url`      | 0       | URL không có fragment | chuỗi rỗng           |
   +------------------+---------+-----------------------+----------------------+
   | :attr:`fragment` | 1       | Mã định danh fragment | chuỗi rỗng           |
   +------------------+---------+-----------------------+----------------------+

   Xem phần :ref:`urlparse-result-object` để biết thêm thông tin về đối tượng kết quả.

   .. versionchanged:: 3.2
      Kết quả là một đối tượng có cấu trúc thay vì một tuple 2 phần tử đơn giản.

.. function:: unwrap(url)

   Trích xuất URL từ một URL được bao bọc (tức là một chuỗi có định dạng ``<URL:scheme://host/path>``, ``<scheme://host/path>``, ``URL:scheme://host/path`` hoặc ``scheme://host/path``). Nếu *url* không phải là một URL được bao bọc, nó sẽ được trả về không thay đổi.

.. _url-parsing-security:

Bảo mật khi phân tích cú pháp URL
---------------------------------

Các API :func:`urlsplit` và :func:`urlparse` không thực hiện **validation** đầu vào. Chúng có thể không phát sinh lỗi đối với những đầu vào mà các ứng dụng khác coi là không hợp lệ. Chúng cũng có thể thành công với một số đầu vào có thể không được coi là URL ở nơi khác. Mục đích của chúng là cung cấp chức năng thiết thực thay vì sự thuần túy.

Thay vì phát sinh một exception khi gặp dữ liệu đầu vào bất thường, chúng có thể trả về một số thành phần dưới dạng chuỗi rỗng. Hoặc các thành phần có thể chứa nhiều hơn mức cần thiết.

Chúng tôi khuyến nghị người dùng các API này, khi các giá trị có thể được sử dụng ở bất kỳ đâu có liên quan đến bảo mật, hãy lập trình theo hướng phòng thủ. Hãy thực hiện một số bước xác minh trong code trước khi tin tưởng thành phần được trả về. ``scheme`` đó có hợp lý không? ``path`` đó có phù hợp không? Có điều gì bất thường về ``hostname`` đó không? v.v.

Khái niệm URL không được định nghĩa hoàn toàn thống nhất. Các ứng dụng khác nhau có những nhu cầu và ràng buộc mong muốn khác nhau. Chẳng hạn, `WHATWG spec <WHATWG spec_>`_ hiện tại mô tả những yêu cầu của các client web hướng đến người dùng, chẳng hạn như trình duyệt web. Trong khi :rfc:`3986` thì tổng quát hơn. Các hàm này kết hợp một số khía cạnh của cả hai, nhưng không thể được xem là tuân thủ hoàn toàn tiêu chuẩn nào. Các API và code hiện có của người dùng, với những kỳ vọng về các hành vi cụ thể, đã xuất hiện trước cả hai tiêu chuẩn, khiến chúng tôi phải hết sức thận trọng khi thay đổi hành vi của API.

.. _parsing-ascii-encoded-bytes:

Phân tích các byte được mã hóa ASCII
------------------------------------

Các hàm phân tích URL ban đầu chỉ được thiết kế để hoạt động trên các chuỗi ký tự. Trong thực tế, khả năng thao tác với các URL đã được trích dẫn và mã hóa đúng cách dưới dạng các chuỗi byte ASCII rất hữu ích. Vì vậy, các hàm phân tích URL trong module này đều hoạt động trên :class:`bytes` và
các đối tượng :class:`bytearray` bên cạnh các đối tượng :class:`str`.

Nếu dữ liệu :class:`str` được truyền vào, kết quả cũng sẽ chỉ chứa
dữ liệu :class:`str`. Nếu truyền vào dữ liệu :class:`bytes` hoặc :class:`bytearray`, kết quả sẽ chỉ chứa dữ liệu :class:`bytes`.

Việc cố gắng trộn dữ liệu :class:`str` với :class:`bytes` hoặc
:class:`bytearray` trong cùng một lần gọi hàm sẽ dẫn đến việc phát sinh
:exc:`TypeError`, còn việc cố gắng truyền các giá trị byte không phải ASCII sẽ kích hoạt :exc:`UnicodeDecodeError`.

Để hỗ trợ việc chuyển đổi các đối tượng kết quả giữa :class:`str` và
:class:`bytes` dễ dàng hơn, tất cả giá trị trả về từ các hàm phân tích URL đều cung cấp một phương thức :meth:`encode` (khi kết quả chứa dữ liệu :class:`str`) hoặc một phương thức :meth:`decode` (khi kết quả chứa dữ liệu :class:`bytes`). Chữ ký của các phương thức này khớp với chữ ký của các phương thức :class:`bytes` và :meth:`encode` tương ứng (ngoại trừ việc encoding mặc định là :class:`str` thay vì :meth:`decode`). Mỗi phương thức tạo ra một giá trị thuộc kiểu tương ứng, chứa dữ liệu :class:`bytes` (đối với
các phương thức :class:`str` và :class:`bytes` (ngoại trừ việc encoding mặc định là ``'ascii'`` thay vì ``'utf-8'``). Mỗi phương thức tạo ra một giá trị thuộc kiểu tương ứng, chứa dữ liệu :class:`bytes` (đối với
:meth:`encode` methods) hoặc :class:`str` dữ liệu (để
:meth:`decode` methods).

Các ứng dụng cần xử lý những URL có thể được đặt trong dấu ngoặc kép không đúng cách và có thể chứa dữ liệu không phải ASCII sẽ cần tự giải mã từ byte sang ký tự trước khi gọi các phương thức phân tích URL.

Hành vi được mô tả trong phần này chỉ áp dụng cho các hàm phân tích URL. Các hàm trích dẫn URL sử dụng các quy tắc riêng khi tạo hoặc sử dụng các chuỗi byte, như được nêu chi tiết trong tài liệu của từng hàm trích dẫn URL.

.. versionchanged:: 3.2
   Các hàm phân tích URL hiện chấp nhận các chuỗi byte được mã hóa ASCII


.. _urlparse-result-object:

Kết quả phân tích có cấu trúc
-----------------------------

Các đối tượng kết quả từ :func:`urlsplit`, :func:`urlparse`  và
Các hàm :func:`urldefrag` là các lớp con của kiểu :class:`tuple`. Các lớp con này bổ sung các thuộc tính được liệt kê trong tài liệu dành cho những hàm đó, hỗ trợ mã hóa và giải mã được mô tả trong phần trước, cũng như một phương thức bổ sung:

.. method:: urllib.parse.SplitResult.geturl()

   Trả về phiên bản được kết hợp lại của URL ban đầu dưới dạng chuỗi. Phiên bản này có thể khác URL ban đầu ở chỗ scheme có thể được chuẩn hóa thành chữ thường và các thành phần trống có thể bị loại bỏ. Cụ thể, các tham số, query và mã định danh fragment trống sẽ bị loại bỏ.

   Đối với các kết quả :func:`urldefrag`, chỉ các mã định danh fragment trống mới bị loại bỏ. Đối với các kết quả :func:`urlsplit` và :func:`urlparse`, tất cả thay đổi đã nêu sẽ được thực hiện trên URL do phương thức này trả về.

   Kết quả của phương thức này vẫn không thay đổi nếu được truyền lại qua hàm phân tích ban đầu:

      >>> from urllib.parse import urlsplit
      >>> url = 'HTTP://www.Python.org/doc/#'
      >>> r1 = urlsplit(url)
      >>> r1.geturl()
      'http://www.Python.org/doc/'
      >>> r2 = urlsplit(r1.geturl())
      >>> r2.geturl()
      'http://www.Python.org/doc/'


Các lớp sau cung cấp phần triển khai cho các kết quả phân tích có cấu trúc khi hoạt động trên các đối tượng :class:`str`:

.. class:: DefragResult(url, fragment)

   Lớp cụ thể cho các kết quả :func:`urldefrag` chứa dữ liệu :class:`str`. Phương thức :meth:`encode` trả về một thực thể :class:`DefragResultBytes`.

   .. versionadded:: 3.2

.. class:: ParseResult(scheme, netloc, path, params, query, fragment)

   Lớp cụ thể cho các kết quả :func:`urlparse` chứa dữ liệu :class:`str`. Phương thức :meth:`encode` trả về một thực thể :class:`ParseResultBytes`.

.. class:: SplitResult(scheme, netloc, path, query, fragment)

   Lớp cụ thể cho các kết quả :func:`urlsplit` chứa dữ liệu :class:`str`. Phương thức :meth:`encode` trả về một thực thể :class:`SplitResultBytes`.


Các lớp sau cung cấp phần triển khai cho các kết quả phân tích cú pháp khi hoạt động trên các đối tượng :class:`bytes` hoặc :class:`bytearray`:

.. class:: DefragResultBytes(url, fragment)

   Lớp cụ thể cho các kết quả :func:`urldefrag` chứa dữ liệu :class:`bytes`. Phương thức :meth:`decode` trả về một thực thể :class:`DefragResult`.

   .. versionadded:: 3.2

.. class:: ParseResultBytes(scheme, netloc, path, params, query, fragment)

   Lớp cụ thể cho các kết quả :func:`urlparse` chứa dữ liệu :class:`bytes`. Phương thức :meth:`decode` trả về một thực thể :class:`ParseResult`.

   .. versionadded:: 3.2

.. class:: SplitResultBytes(scheme, netloc, path, query, fragment)

   Lớp cụ thể cho các kết quả :func:`urlsplit` chứa dữ liệu :class:`bytes`. Phương thức :meth:`decode` trả về một thực thể :class:`SplitResult`.

   .. versionadded:: 3.2


Trích dẫn URL
-------------

Các hàm trích dẫn URL tập trung vào việc lấy dữ liệu chương trình và đảm bảo dữ liệu đó an toàn để sử dụng làm các thành phần URL bằng cách trích dẫn các ký tự đặc biệt và mã hóa phù hợp văn bản không phải ASCII. Chúng cũng hỗ trợ đảo ngược các thao tác này để tạo lại dữ liệu ban đầu từ nội dung của một thành phần URL nếu tác vụ đó chưa được các hàm phân tích URL ở trên đảm nhiệm.

.. function:: quote(string, safe='/', encoding=None, errors=None)

   Thay thế các ký tự đặc biệt trong *string* bằng :samp:`%{xx}` escape. Chữ cái, chữ số và các ký tự ``'_.-~'`` không bao giờ được đặt trong dấu trích dẫn. Theo mặc định, hàm này được dùng để đặt phần đường dẫn của URL trong dấu trích dẫn. Tham số tùy chọn *safe* chỉ định các ký tự ASCII bổ sung không nên được đặt trong dấu trích dẫn --- giá trị mặc định là ``'/'``.

   *string* có thể là một đối tượng :class:`str` hoặc :class:`bytes`.

   .. versionchanged:: 3.7
      Đã chuyển từ :rfc:`2396` sang :rfc:`3986` để đặt các chuỗi URL trong dấu trích dẫn. "~" hiện đã được thêm vào tập hợp các ký tự không cần mã hóa.

   Các tham số tùy chọn *encoding* và *errors* chỉ định cách xử lý các ký tự không thuộc ASCII, theo quy định của phương thức :meth:`str.encode`. Mặc dù trong chữ ký hàm, các tham số này mặc định là ``None``, khi xử lý đầu vào :class:`str`, *encoding* trên thực tế mặc định là ``'utf-8'`` và *errors* là ``'strict'``, nghĩa là các ký tự không được hỗ trợ sẽ gây ra một
   :class:`UnicodeEncodeError`. Không được cung cấp *encoding* và *errors* nếu *string* là một
   :class:`bytes`, hoặc một :class:`TypeError` sẽ được phát sinh.

   Lưu ý rằng ``quote(string, safe, encoding, errors)`` tương đương với ``quote_from_bytes(string.encode(encoding, errors), safe)``.

   Ví dụ: ``quote('/El Niño/')`` cho ra ``'/El%20Ni%C3%B1o/'``.


.. function:: quote_plus(string, safe='', encoding=None, errors=None)

   Tương tự :func:`quote`, nhưng cũng thay thế khoảng trắng bằng dấu cộng, như cần thiết khi trích dẫn các giá trị biểu mẫu HTML trong quá trình tạo chuỗi truy vấn để đưa vào URL. Các dấu cộng trong chuỗi ban đầu sẽ được escape, trừ khi chúng được bao gồm trong *safe*. Nó cũng không đặt *safe* mặc định thành ``'/'``.

   Ví dụ: ``quote_plus('/El Niño/')`` cho ra ``'%2FEl+Ni%C3%B1o%2F'``.


.. function:: quote_from_bytes(bytes, safe='/')

   Tương tự :func:`quote`, nhưng chấp nhận một đối tượng :class:`bytes` thay vì một
   :class:`str`, và không thực hiện việc mã hóa chuỗi thành byte.

   Ví dụ: ``quote_from_bytes(b'a&\xef')`` cho ra ``'a%26%EF'``.


.. function:: unquote(string, encoding='utf-8', errors='replace')

   Thay thế các escape :samp:`%{xx}` bằng ký tự tương ứng. Các tham số tùy chọn *encoding* và *errors* chỉ định cách giải mã các chuỗi được mã hóa phần trăm thành ký tự Unicode, như được chấp nhận bởi
   :meth:`bytes.decode` phương thức.

   *string* có thể là một đối tượng :class:`str` hoặc :class:`bytes`.

   *encoding* mặc định là ``'utf-8'``. *errors* mặc định là ``'replace'``, nghĩa là các chuỗi không hợp lệ được thay thế bằng một ký tự giữ chỗ.

   Ví dụ: ``unquote('/El%20Ni%C3%B1o/')`` cho kết quả ``'/El Niño/'``.

   .. versionchanged:: 3.9
      Tham số *string* hỗ trợ các đối tượng bytes và str (trước đây chỉ hỗ trợ str).




.. function:: unquote_plus(string, encoding='utf-8', errors='replace')

   Tương tự :func:`unquote`, nhưng cũng thay thế dấu cộng bằng khoảng trắng, theo yêu cầu khi bỏ trích dẫn các giá trị của biểu mẫu HTML.

   *string* phải là một :class:`str`.

   Ví dụ: ``unquote_plus('/El+Ni%C3%B1o/')`` cho ra ``'/El Niño/'``.


.. function:: unquote_to_bytes(string)

   Thay thế các chuỗi escape :samp:`%{xx}` bằng giá trị tương đương một octet, rồi trả về một
   đối tượng :class:`bytes`.

   *string* có thể là một đối tượng :class:`str` hoặc :class:`bytes`.

   Nếu đó là một :class:`str`, các ký tự không phải ASCII chưa được escape trong *string* sẽ được mã hóa thành các byte UTF-8.

   Ví dụ: ``unquote_to_bytes('a%26%EF')`` cho ra ``b'a&\xef'``.


.. function:: urlencode(query, doseq=False, safe='', encoding=None, \
                        errors=None, quote_via=quote_plus)

   Chuyển đổi một đối tượng mapping hoặc một chuỗi các tuple gồm hai phần tử, có thể chứa các đối tượng :class:`str` hoặc :class:`bytes`, thành một chuỗi văn bản ASCII được mã hóa theo phần trăm. Nếu chuỗi kết quả được dùng làm *data* cho thao tác POST với hàm :func:`~urllib.request.urlopen`, thì chuỗi đó cần được mã hóa thành các byte; nếu không, điều này sẽ dẫn đến một
   :exc:`TypeError`.

   Chuỗi kết quả là một loạt các cặp ``key=value`` được phân tách bằng các ký tự ``'&'``, trong đó cả *key* và *value* đều được trích dẫn bằng hàm *quote_via*. Theo mặc định, :func:`quote_plus` được dùng để trích dẫn các giá trị, nghĩa là dấu cách được trích dẫn thành ký tự ``'+'`` và các ký tự '/' được mã hóa thành ``%2F``, tuân theo tiêu chuẩn dành cho các yêu cầu GET (``application/x-www-form-urlencoded``). Một hàm thay thế có thể được truyền dưới dạng *quote_via* là :func:`quote`, hàm này sẽ mã hóa dấu cách thành ``%20`` và không mã hóa các ký tự '/'. Để kiểm soát tối đa những gì được trích dẫn, hãy sử dụng ``quote`` và chỉ định một giá trị cho *safe*.

   Khi sử dụng một chuỗi các tuple gồm hai phần tử làm đối số *query*, phần tử đầu tiên của mỗi tuple là một khóa và phần tử thứ hai là một giá trị. Bản thân phần tử giá trị có thể là một chuỗi và trong trường hợp đó, nếu tham số tùy chọn *doseq* được đánh giá là ``True``, các cặp ``key=value`` riêng lẻ được phân tách bằng ``'&'`` sẽ được tạo cho mỗi phần tử của chuỗi giá trị tương ứng với khóa. Thứ tự các tham số trong chuỗi được mã hóa sẽ khớp với thứ tự của các tuple tham số trong chuỗi.

   Các tham số *safe*, *encoding* và *errors* được truyền xuống *quote_via* (các tham số *encoding* và *errors* chỉ được truyền khi một phần tử truy vấn là :class:`str`).

   Để đảo ngược quá trình mã hóa này, mô-đun cung cấp :func:`parse_qs` và :func:`parse_qsl` để phân tích chuỗi truy vấn thành các cấu trúc dữ liệu Python.

   Hãy tham khảo :ref:`urllib examples <urllib-examples>` để biết cách
   phương thức :func:`urllib.parse.urlencode` có thể được dùng để tạo chuỗi truy vấn của một URL hoặc dữ liệu cho một yêu cầu POST.

   .. versionchanged:: 3.2
      *query* hỗ trợ các đối tượng bytes và chuỗi.

   .. versionchanged:: 3.5
      Đã thêm tham số *quote_via*.

   .. deprecated:: 3.14
      Việc chấp nhận các đối tượng có giá trị false (chẳng hạn như ``0`` và ``[]``) ngoại trừ chuỗi rỗng, các đối tượng dạng byte và ``None`` hiện không còn được khuyến nghị.


.. seealso::

   `WHATWG`_ -  Tiêu chuẩn Living về URL
      Nhóm công tác về Tiêu chuẩn URL, định nghĩa URL, domain, địa chỉ IP, định dạng application/x-www-form-urlencoded và API của chúng.

   :rfc:`3986` - Mã định danh tài nguyên đồng nhất
      Đây là tiêu chuẩn hiện hành (STD66). Mọi thay đổi đối với module urllib.parse cần tuân thủ tiêu chuẩn này. Có thể quan sát thấy một số điểm sai lệch, chủ yếu nhằm duy trì khả năng tương thích ngược và đáp ứng một số yêu cầu phân tích cú pháp trên thực tế thường thấy ở các trình duyệt phổ biến.

   :rfc:`2732` - Định dạng cho các địa chỉ IPv6 dạng literal trong URL.
      Tài liệu này nêu các yêu cầu phân tích cú pháp của URL IPv6.

   :rfc:`2396` - Uniform Resource Identifiers (URI): Cú pháp chung
      Tài liệu mô tả các yêu cầu cú pháp chung cho cả Uniform Resource Names (URN) và Uniform Resource Locators (URL).

   :rfc:`2368` - Lược đồ URL mailto.
      Các yêu cầu phân tích cú pháp cho lược đồ URL mailto.

   :rfc:`1808` - Uniform Resource Locators tương đối
      Tài liệu Request For Comments này bao gồm các quy tắc để kết hợp URL tuyệt đối và URL tương đối, trong đó có khá nhiều "Ví dụ bất thường" quy định cách xử lý các trường hợp biên.

   :rfc:`1738` - Bộ định vị tài nguyên thống nhất (URL)
      Tài liệu này nêu cú pháp hình thức và ngữ nghĩa của URL tuyệt đối.

.. _WHATWG: https://url.spec.whatwg.org/
