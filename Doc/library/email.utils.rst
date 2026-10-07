:mod:`!email.utils`: Các tiện ích khác
--------------------------------------

.. module:: email.utils
   :synopsis: Các tiện ích khác của gói email.

**Mã nguồn:** :source:`Lib/email/utils.py`

--------------

Mô-đun :mod:`!email.utils` cung cấp một số tiện ích hữu ích:

.. function:: localtime(dt=None)

   Trả về thời gian địa phương dưới dạng đối tượng datetime có thông tin múi giờ. Nếu được gọi mà không có đối số, hàm trả về thời gian hiện tại. Nếu không, đối số *dt* phải là một
   :class:`~datetime.datetime` thể hiện, và đối tượng này được chuyển đổi sang múi giờ địa phương theo cơ sở dữ liệu múi giờ của hệ thống. Nếu *dt* là naive (nghĩa là ``dt.tzinfo`` là ``None``), đối tượng này được giả định là ở giờ địa phương.

   .. versionadded:: 3.3

   .. deprecated-removed:: 3.12 3.14
      Tham số *isdst*.

.. function:: make_msgid(idstring=None, domain=None)

   Trả về một chuỗi phù hợp với :rfc:`2822`\ -compliant
   :mailheader:`Message-ID` header.  Tùy chọn *idstring* nếu được cung cấp là một chuỗi được dùng để tăng cường tính duy nhất của message id. Tùy chọn *domain* nếu được cung cấp sẽ cung cấp phần của msgid sau '@'. Giá trị mặc định là hostname cục bộ. Thông thường không cần ghi đè giá trị mặc định này, nhưng có thể hữu ích trong một số trường hợp, chẳng hạn như khi xây dựng một hệ thống phân tán sử dụng cùng một domain name trên nhiều máy chủ.

   .. versionchanged:: 3.2
      Đã thêm keyword *domain*.


Các hàm còn lại thuộc API email cũ (``Compat32``). Không cần sử dụng trực tiếp các hàm này với API mới, vì việc phân tích cú pháp và định dạng mà chúng cung cấp được tự động thực hiện bởi cơ chế phân tích cú pháp header của API mới.


.. function:: quote(str)

   Trả về một chuỗi mới, trong đó các dấu gạch chéo ngược trong *str* được thay thế bằng hai dấu gạch chéo ngược, còn dấu ngoặc kép được thay thế bằng dấu gạch chéo ngược và dấu ngoặc kép.


.. function:: unquote(str)

   Trả về một chuỗi mới là phiên bản *unquoted* của *str*. Nếu *str* bắt đầu và kết thúc bằng dấu ngoặc kép, các dấu này sẽ được loại bỏ. Tương tự, nếu *str* bắt đầu và kết thúc bằng dấu ngoặc nhọn, các dấu này sẽ được loại bỏ.


.. function:: parseaddr(address, *, strict=True)

   Phân tích địa chỉ -- địa chỉ này phải là giá trị của một trường chứa địa chỉ nào đó, chẳng hạn như :mailheader:`To` hoặc :mailheader:`Cc` -- thành các phần cấu thành là *realname* và *email address*. Trả về một tuple chứa thông tin đó, trừ khi việc phân tích cú pháp thất bại; trong trường hợp đó, một tuple 2 phần tử gồm ``('', '')`` sẽ được trả về.

   Nếu *strict* là true, hãy sử dụng trình phân tích cú pháp nghiêm ngặt, trình này sẽ từ chối các đầu vào không đúng định dạng.

   .. versionchanged:: 3.13
      Thêm tham số tùy chọn *strict* và mặc định từ chối các đầu vào không đúng định dạng.


.. function:: formataddr(pair, charset='utf-8')

   Là phiên bản đảo ngược của :meth:`parseaddr`, hàm này nhận một bộ 2 phần tử có dạng ``(realname, email_address)`` và trả về giá trị chuỗi phù hợp cho :mailheader:`To` hoặc
   :mailheader:`Cc` header. Nếu phần tử đầu tiên của *pair* là false thì phần tử thứ hai được trả về không thay đổi.

   *charset* tùy chọn là bộ ký tự sẽ được sử dụng trong quá trình mã hóa :rfc:`2047` của ``realname`` nếu ``realname`` chứa các ký tự không phải ASCII. Có thể là một thực thể của :class:`str` hoặc một
   :class:`~email.charset.Charset`. Mặc định là ``utf-8``.

   .. versionchanged:: 3.3
      Đã thêm tùy chọn *charset*.


.. function:: getaddresses(fieldvalues, *, strict=True)

   Phương thức này trả về một danh sách các bộ 2 phần tử có dạng được trả về bởi ``parseaddr()``. *fieldvalues* là một chuỗi các giá trị trường tiêu đề như có thể được trả về bởi
   :meth:`Message.get_all <email.message.Message.get_all>`.

   Nếu *strict* là true, hãy sử dụng trình phân tích cú pháp nghiêm ngặt, trình này sẽ từ chối các đầu vào không đúng định dạng.

   Dưới đây là một ví dụ đơn giản lấy tất cả người nhận của một thư::

      from email.utils import getaddresses

      tos = msg.get_all('to', [])
      ccs = msg.get_all('cc', [])
      resent_tos = msg.get_all('resent-to', [])
      resent_ccs = msg.get_all('resent-cc', [])
      all_recipients = getaddresses(tos + ccs + resent_tos + resent_ccs)

   .. versionchanged:: 3.13
      Thêm tham số tùy chọn *strict* và mặc định từ chối các đầu vào không đúng định dạng.


.. function:: parsedate(date)

   Cố gắng phân tích cú pháp một ngày theo các quy tắc trong :rfc:`2822`. Tuy nhiên, một số mailer không tuân theo định dạng đó như đã chỉ định, vì vậy :func:`parsedate` cố gắng đoán chính xác trong những trường hợp như vậy. *date* là một chuỗi chứa một ngày :rfc:`2822`, chẳng hạn như ``"Mon, 20 Nov 1995 19:12:08 -0500"``. Nếu phân tích cú pháp ngày thành công, :func:`parsedate` trả về một bộ 9 phần tử có thể được truyền trực tiếp cho
   :func:`time.mktime`; nếu không, ``None`` sẽ được trả về. Lưu ý rằng các chỉ mục 6, 7 và 8 của bộ kết quả không thể sử dụng được.


.. function:: parsedate_tz(date)

   Thực hiện cùng chức năng như :func:`parsedate`, nhưng trả về ``None`` hoặc một bộ 10 phần tử; 9 phần tử đầu tiên tạo thành một bộ có thể được truyền trực tiếp cho
   :func:`time.mktime`, và phần tử thứ mười là độ lệch múi giờ của ngày so với UTC (tên gọi chính thức của Giờ trung bình Greenwich) [#]_. Nếu chuỗi đầu vào không có múi giờ, phần tử cuối cùng của tuple được trả về là ``0``, đại diện cho UTC. Lưu ý rằng các chỉ mục 6, 7 và 8 của tuple kết quả không thể sử dụng.


.. function:: parsedate_to_datetime(date)

   Phép nghịch đảo của :func:`format_datetime`. Thực hiện cùng chức năng như
   :func:`parsedate`, nhưng khi thành công sẽ trả về một :mod:`~datetime.datetime`; nếu không, ``ValueError`` sẽ được phát sinh nếu *date* chứa một giá trị không hợp lệ, chẳng hạn như giờ lớn hơn 23 hoặc độ lệch múi giờ không nằm trong khoảng từ -24 đến 24 giờ. Nếu ngày đầu vào có múi giờ là ``-0000``, ``datetime`` sẽ là một ``datetime`` ngây thơ (naive), và nếu ngày đó tuân thủ các RFC thì nó sẽ biểu diễn một thời điểm theo UTC nhưng không cho biết múi giờ nguồn thực tế của thông báo chứa ngày đó. Nếu ngày đầu vào có bất kỳ độ lệch múi giờ hợp lệ nào khác, ``datetime`` sẽ là một ``datetime`` có nhận biết (aware), với :class:`~datetime.timezone` :class:`~datetime.tzinfo` tương ứng.

   .. versionadded:: 3.3


.. function:: mktime_tz(tuple)

   Chuyển một tuple 10 phần tử do :func:`parsedate_tz` trả về thành dấu thời gian UTC (số giây kể từ Epoch). Nếu mục múi giờ trong tuple là ``None``, hãy giả định đó là giờ địa phương.


.. function:: formatdate(timeval=None, localtime=False, usegmt=False)

   Trả về một chuỗi ngày theo :rfc:`2822`, ví dụ:::

      Fri, 09 Nov 2001 01:08:47 -0000

   *timeval* tùy chọn, nếu được cung cấp, là một giá trị thời gian dấu phẩy động được chấp nhận bởi
   :func:`time.gmtime` và :func:`time.localtime`; nếu không, thời gian hiện tại sẽ được sử dụng.

   *localtime* tùy chọn là một cờ mà khi ``True``, sẽ diễn giải *timeval* và trả về ngày tháng theo múi giờ cục bộ thay vì UTC, đồng thời xử lý đúng giờ mùa hè. Mặc định là ``False``, nghĩa là UTC được sử dụng.

   *usegmt* tùy chọn là một cờ mà khi ``True``, sẽ xuất ra chuỗi ngày tháng với múi giờ dưới dạng chuỗi ASCII ``GMT`` thay vì ``-0000`` dạng số. Điều này cần thiết cho một số giao thức (chẳng hạn như HTTP). Tùy chọn này chỉ áp dụng khi *localtime* là ``False``. Mặc định là ``False``.


.. function:: format_datetime(dt, usegmt=False)

   Tương tự ``formatdate``, nhưng đầu vào là một đối tượng :mod:`datetime`. Nếu đó là một datetime naive, nó được giả định là "UTC không có thông tin về múi giờ nguồn", và ``-0000`` quy ước được sử dụng cho múi giờ. Nếu đó là một ``datetime`` có thông tin múi giờ, độ lệch múi giờ dạng số sẽ được sử dụng. Nếu đó là một múi giờ có thông tin với độ lệch bằng 0, thì *usegmt* có thể được đặt thành ``True``, trong trường hợp đó chuỗi ``GMT`` được sử dụng thay cho độ lệch múi giờ dạng số. Điều này cung cấp một cách để tạo các tiêu đề ngày tháng HTTP phù hợp với tiêu chuẩn.

   .. versionadded:: 3.3


.. function:: decode_rfc2231(s)

   Giải mã chuỗi *s* theo :rfc:`2231`.


.. function:: encode_rfc2231(s, charset=None, language=None)

   Mã hóa chuỗi *s* theo :rfc:`2231`. Tùy chọn *charset* và *language*, nếu được cung cấp, lần lượt là tên bộ ký tự và tên ngôn ngữ cần sử dụng. Nếu không cung cấp tùy chọn nào, *s* được trả về nguyên trạng. Nếu *charset* được cung cấp nhưng *language* không được cung cấp, chuỗi sẽ được mã hóa bằng chuỗi rỗng cho *language*.


.. function:: collapse_rfc2231_value(value, errors='replace', fallback_charset='us-ascii')

   Khi một tham số tiêu đề được mã hóa theo định dạng :rfc:`2231`,
   :meth:`Message.get_param <email.message.Message.get_param>` có thể trả về một bộ 3 phần tử chứa bộ ký tự, ngôn ngữ và giá trị. :func:`collapse_rfc2231_value` chuyển đổi bộ này thành một chuỗi. Tùy chọn *errors* được truyền vào đối số *errors* của :class:`str`'s
   phương thức :func:`~str.encode`; mặc định là ``'replace'``.  Tùy chọn *fallback_charset* chỉ định bộ ký tự sẽ sử dụng nếu bộ ký tự trong
   tiêu đề :rfc:`2231` không được Python biết đến; mặc định là ``'us-ascii'``.

   Để thuận tiện, nếu *value* được truyền vào :func:`collapse_rfc2231_value` không phải là một tuple, thì nó phải là một chuỗi và được trả về mà không có dấu ngoặc kép.


.. function:: decode_params(params)

   Giải mã danh sách tham số theo :rfc:`2231`.  *params* là một chuỗi gồm các tuple 2 phần tử có dạng ``(content-type, string-value)``.


.. rubric:: Chú thích cuối trang

.. [#] Lưu ý rằng dấu của độ lệch múi giờ ngược với dấu của biến ``time.timezone`` đối với cùng một múi giờ; biến sau tuân theo tiêu chuẩn POSIX, còn module này tuân theo :rfc:`2822`.
