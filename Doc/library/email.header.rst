:mod:`!email.header`: Tiêu đề được quốc tế hóa
----------------------------------------------

.. module:: email.header
   :synopsis: Biểu diễn các tiêu đề không phải ASCII

**Mã nguồn:** :source:`Lib/email/header.py`

--------------

Mô-đun này là một phần của API email cũ (``Compat32``). Trong API hiện tại, việc mã hóa và giải mã tiêu đề được xử lý minh bạch bởi API dạng từ điển của lớp :class:`~email.message.EmailMessage`. Ngoài việc được sử dụng trong mã cũ, mô-đun này còn hữu ích trong các ứng dụng cần kiểm soát hoàn toàn các bộ ký tự được dùng khi mã hóa tiêu đề.

Phần văn bản còn lại trong mục này là tài liệu gốc của mô-đun.

:rfc:`2822` là tiêu chuẩn cơ sở mô tả định dạng của thư email. Tiêu chuẩn này bắt nguồn từ tiêu chuẩn :rfc:`822` cũ hơn, được sử dụng rộng rãi vào thời điểm hầu hết email chỉ được soạn bằng các ký tự ASCII. :rfc:`2822` là một đặc tả được viết với giả định rằng email chỉ chứa các ký tự ASCII 7 bit.

Dĩ nhiên, khi email được triển khai trên toàn thế giới, nó đã trở nên quốc tế hóa, cho phép sử dụng các bộ ký tự dành riêng cho từng ngôn ngữ trong thư email. Tiêu chuẩn cơ sở vẫn yêu cầu thư email chỉ được truyền bằng các ký tự ASCII 7 bit, vì vậy một loạt RFC đã được viết để mô tả cách mã hóa email chứa các ký tự không phải ASCII thành
định dạng tuân thủ :rfc:`2822`\ . Các RFC này bao gồm :rfc:`2045`, :rfc:`2046`,
:rfc:`2047` và :rfc:`2231`. Gói :mod:`email` hỗ trợ các tiêu chuẩn này trong các mô-đun :mod:`!email.header` và :mod:`email.charset`.

Nếu bạn muốn đưa các ký tự non-ASCII vào tiêu đề email, chẳng hạn trong các trường
:mailheader:`Subject` hoặc :mailheader:`To`, bạn nên sử dụng
lớp :class:`Header` và gán trường trong đối tượng :class:`~email.message.Message` cho một thực thể :class:`Header` thay vì sử dụng chuỗi làm giá trị tiêu đề.  Nhập lớp :class:`Header` từ mô-đun :mod:`!email.header`. Ví dụ::

   >>> from email.message import Message
   >>> from email.header import Header
   >>> msg = Message()
   >>> h = Header('p\xf6stal', 'iso-8859-1')
   >>> msg['Subject'] = h
   >>> msg.as_string()
   'Subject: =?iso-8859-1?q?p=F6stal?=\n\n'



Lưu ý rằng ở đây chúng ta muốn trường :mailheader:`Subject` chứa một ký tự non-ASCII.  Chúng ta thực hiện điều đó bằng cách tạo một thực thể :class:`Header` và truyền vào bộ ký tự cần sử dụng khi mã hóa thực thể này.  Khi phần tiếp theo
thực thể :class:`~email.message.Message` được chuyển thành dạng phẳng, trường :mailheader:`Subject` đã được mã hóa :rfc:`2047` đúng cách.  Các trình đọc thư hỗ trợ MIME sẽ hiển thị tiêu đề này bằng ký tự ISO-8859-1 được nhúng.

Sau đây là phần mô tả lớp :class:`Header`:


.. class:: Header(s=None, charset=None, maxlinelen=None, header_name=None, continuation_ws=' ', errors='strict')

   Tạo một header tuân thủ MIME có thể chứa các chuỗi thuộc nhiều bộ ký tự khác nhau.

   *s* tùy chọn là giá trị header ban đầu. Nếu ``None`` (mặc định), giá trị header ban đầu sẽ không được thiết lập. Sau đó, bạn có thể nối thêm vào header bằng các lời gọi phương thức
   :meth:`append`. *s* có thể là một thực thể của :class:`bytes` hoặc
   :class:`str`, nhưng hãy xem tài liệu :meth:`append` để biết ngữ nghĩa.

   *charset* tùy chọn có hai mục đích: nó có cùng ý nghĩa với đối số *charset* của phương thức :meth:`append`. Nó cũng đặt bộ ký tự mặc định cho tất cả các lời gọi :meth:`append` tiếp theo không cung cấp đối số *charset*. Nếu *charset* không được cung cấp trong hàm khởi tạo (mặc định), bộ ký tự ``us-ascii`` sẽ được dùng làm charset ban đầu của *s* cũng như giá trị mặc định cho các lời gọi :meth:`append` tiếp theo.

   Có thể chỉ định rõ ràng độ dài dòng tối đa thông qua *maxlinelen*. Để tách dòng đầu tiên thành một giá trị ngắn hơn (nhằm tính đến field header không được bao gồm trong *s*, chẳng hạn như :mailheader:`Subject`), hãy truyền tên của field vào *header_name*. Giá trị mặc định của *maxlinelen* là 78, còn giá trị mặc định của *header_name* là ``None``, nghĩa là nó không được tính đến đối với dòng đầu tiên của một header dài được tách dòng.

   *continuation_ws* tùy chọn phải là khoảng trắng gấp dòng tuân thủ :rfc:`2822`\ -compliant, và thường là một dấu cách hoặc ký tự tab cứng. Ký tự này sẽ được thêm vào trước các dòng tiếp nối. *continuation_ws* mặc định là một ký tự dấu cách đơn.

   *errors* tùy chọn được truyền thẳng vào phương thức :meth:`append`.


   .. method:: append(s, charset=None, errors='strict')

      Nối chuỗi *s* vào header MIME.

      *charset* tùy chọn, nếu được cung cấp, phải là một instance của :class:`~email.charset.Charset` (xem :mod:`email.charset`) hoặc tên của một bộ ký tự, tên này sẽ được chuyển đổi thành một instance của :class:`~email.charset.Charset`. Giá trị ``None`` (mặc định) có nghĩa là sử dụng *charset* được cung cấp trong hàm khởi tạo.

      *s* có thể là một instance của :class:`bytes` hoặc :class:`str`. Nếu là một instance của :class:`bytes`, thì *charset* là encoding của chuỗi byte đó, và sẽ phát sinh :exc:`UnicodeError` nếu không thể giải mã chuỗi bằng bộ ký tự đó.

      Nếu *s* là một instance của :class:`str`, thì *charset* là một gợi ý chỉ định bộ ký tự của các ký tự trong chuỗi.

      Trong cả hai trường hợp, khi tạo một header tuân thủ :rfc:`2822`\  bằng cách sử dụng
      Theo các quy tắc :rfc:`2047`, chuỗi sẽ được mã hóa bằng codec đầu ra của charset. Nếu không thể mã hóa chuỗi bằng codec đầu ra, một UnicodeError sẽ được phát sinh.

      Tùy chọn *errors* được truyền làm đối số errors cho lệnh gọi decode nếu *s* là một chuỗi byte.


   .. method:: encode(splitchars=';, \t', maxlinelen=None, linesep='\n')

      Mã hóa tiêu đề thư thành định dạng tuân thủ RFC, có thể ngắt các dòng dài và đóng gói các phần không phải ASCII bằng mã hóa base64 hoặc quoted-printable.

      Tùy chọn *splitchars* là một chuỗi chứa các ký tự được thuật toán tách dòng ưu tiên hơn trong quá trình ngắt tiêu đề thông thường. Đây là hỗ trợ rất sơ lược cho :RFC:`2822`\'s 'các điểm ngắt cú pháp cấp cao hơn': các điểm tách đứng trước một splitchar được ưu tiên khi tách dòng, trong đó các ký tự được ưu tiên theo thứ tự xuất hiện trong chuỗi. Có thể đưa dấu cách và tab vào chuỗi để cho biết nên ưu tiên ký tự nào hơn làm điểm tách khi không có ký tự tách nào khác xuất hiện trong dòng đang được tách. Splitchars không ảnh hưởng đến các dòng được mã hóa bằng :RFC:`2047`.

      *maxlinelen*, nếu được cung cấp, sẽ ghi đè giá trị của instance về độ dài dòng tối đa.

      *linesep* chỉ định các ký tự được dùng để phân tách các dòng của tiêu đề đã được gấp. Giá trị mặc định là giá trị hữu ích nhất cho mã ứng dụng Python (``\n``), nhưng có thể chỉ định ``\r\n`` để tạo các tiêu đề có ký tự phân tách dòng tuân thủ RFC.

      .. versionchanged:: 3.2
         Đã thêm đối số *linesep*.


   Lớp :class:`Header` cũng cung cấp một số phương thức hỗ trợ các toán tử chuẩn và hàm tích hợp sẵn.

   .. method:: __str__()

      Trả về giá trị gần đúng của :class:`Header` dưới dạng chuỗi, sử dụng độ dài dòng không giới hạn. Tất cả các phần đều được giải mã bằng encoding được chỉ định và nối lại với nhau một cách phù hợp. Mọi phần có charset là ``'unknown-8bit'`` đều được giải mã dưới dạng ASCII bằng error handler ``'replace'``.

      .. versionchanged:: 3.2
         Đã bổ sung khả năng xử lý charset ``'unknown-8bit'``.


   .. method:: __eq__(other)

      Phương thức này cho phép bạn so sánh hai thực thể :class:`Header` để kiểm tra tính bằng nhau.


   .. method:: __ne__(other)

      Phương thức này cho phép bạn so sánh hai thực thể :class:`Header` để kiểm tra tính không bằng nhau.

Mô-đun :mod:`!email.header` cũng cung cấp các hàm tiện lợi sau đây.


.. function:: decode_header(header)

   Giải mã giá trị header của một message mà không chuyển đổi charset. Giá trị header nằm trong *header*.

   Vì những lý do mang tính lịch sử, hàm này có thể trả về một trong các dạng sau:

   1. Một danh sách các cặp chứa từng phần đã được giải mã của header, ``(decoded_bytes, charset)``, trong đó *decoded_bytes* luôn là một thể hiện của
      :class:`bytes`, và *charset* là một trong các giá trị sau:

        - Một chuỗi chữ thường chứa tên của bộ ký tự được chỉ định.

        - ``None`` đối với các phần không được mã hóa của header.

   2. Một danh sách có độ dài 1 chứa một cặp ``(string, None)``, trong đó *string* luôn là một thể hiện của :class:`str`.

   Một :exc:`email.errors.HeaderParseError` có thể được phát sinh khi xảy ra một số lỗi giải mã nhất định (ví dụ: ngoại lệ giải mã base64).

   Dưới đây là các ví dụ:

      >>> from email.header import decode_header
      >>> decode_header('=?iso-8859-1?q?p=F6stal?=')
      [(b'p\xf6stal', 'iso-8859-1')]
      >>> decode_header('unencoded_string')
      [('unencoded_string', None)]
      >>> decode_header('bar =?utf-8?B?ZsOzbw==?=')
      [(b'bar ', None), (b'f\xc3\xb3o', 'utf-8')]

   .. note::

       Hàm này chỉ tồn tại để duy trì khả năng tương thích ngược. Đối với mã mới, chúng tôi khuyến nghị sử dụng :class:`email.headerregistry.HeaderRegistry`.


.. function:: make_header(decoded_seq, maxlinelen=None, header_name=None, continuation_ws=' ')

   Tạo một thực thể :class:`Header` từ một chuỗi các cặp như được trả về bởi
   :func:`decode_header`.

   :func:`decode_header` nhận một chuỗi giá trị header và trả về một chuỗi các cặp có định dạng ``(decoded_string, charset)``, trong đó *charset* là tên của bộ ký tự.

   Hàm này nhận một trong các chuỗi cặp đó và trả về một
   thực thể :class:`Header`. Các tùy chọn *maxlinelen*, *header_name* và *continuation_ws* giống như trong hàm khởi tạo :class:`Header`.

   .. note::

       Hàm này chỉ tồn tại để duy trì khả năng tương thích ngược và không được khuyến nghị sử dụng trong mã mới.
