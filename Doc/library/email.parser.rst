:mod:`!email.parser`: Phân tích cú pháp thư email
-------------------------------------------------

.. module:: email.parser
   :synopsis: Phân tích cú pháp các thư email dạng văn bản phẳng để tạo ra cấu trúc đối tượng thư.

**Mã nguồn:** :source:`Lib/email/parser.py`

--------------

Có thể tạo cấu trúc đối tượng thư theo một trong hai cách: tạo mới hoàn toàn bằng cách tạo một đối tượng :class:`~email.message.EmailMessage`, thêm các header bằng giao diện từ điển và thêm payload bằng :meth:`~email.message.EmailMessage.set_content` cùng các phương thức liên quan, hoặc tạo bằng cách phân tích cú pháp biểu diễn đã được tuần tự hóa của thư email.

Gói :mod:`email` cung cấp một parser tiêu chuẩn hiểu hầu hết các cấu trúc tài liệu email, bao gồm cả tài liệu MIME. Bạn có thể truyền cho parser một đối tượng bytes, string hoặc file, và parser sẽ trả về cho bạn đối tượng gốc
:class:`~email.message.EmailMessage` của cấu trúc đối tượng. Đối với các thư đơn giản, không phải MIME, payload của đối tượng gốc này có thể sẽ là một string chứa nội dung thư. Đối với thư MIME, đối tượng gốc sẽ trả về ``True`` từ phương thức :meth:`~email.message.EmailMessage.is_multipart` của nó, và có thể truy cập các phần con thông qua những phương thức thao tác payload, chẳng hạn như :meth:`~email.message.EmailMessage.get_body`,
:meth:`~email.message.EmailMessage.iter_parts`, và
:meth:`~email.message.EmailMessage.walk`.

Thực tế có hai interface parser sẵn có để sử dụng: API :class:`Parser` và API :class:`FeedParser` theo kiểu incremental. API :class:`Parser` hữu ích nhất nếu bạn có toàn bộ nội dung của thông điệp trong bộ nhớ hoặc nếu toàn bộ thông điệp nằm trong một tệp trên hệ thống tệp. :class:`FeedParser` phù hợp hơn khi bạn đang đọc thông điệp từ một stream có thể bị chặn để chờ thêm dữ liệu đầu vào (chẳng hạn như khi đọc một email message từ socket). API
:class:`FeedParser` có thể tiếp nhận và phân tích cú pháp thông điệp theo từng phần, đồng thời chỉ trả về đối tượng gốc khi bạn đóng parser.

Lưu ý rằng parser có thể được mở rộng theo một số cách có giới hạn; tất nhiên, bạn cũng có thể tự triển khai hoàn toàn một parser từ đầu. Toàn bộ logic kết nối parser đi kèm của package :mod:`email` với
class :class:`~email.message.EmailMessage` được thể hiện trong class :class:`~email.policy.Policy`, vì vậy parser tùy chỉnh có thể tạo các cây đối tượng message theo bất kỳ cách nào cần thiết bằng cách triển khai các phiên bản tùy chỉnh của những phương thức :class:`!Policy` phù hợp.


FeedParser API
^^^^^^^^^^^^^^

:class:`BytesFeedParser`, được import từ module :mod:`email.feedparser`, cung cấp một API phù hợp cho việc phân tích cú pháp email message theo từng phần, chẳng hạn như khi cần đọc nội dung của một email message từ một nguồn có thể bị chặn (ví dụ như socket). Tất nhiên, có thể dùng :class:`BytesFeedParser` để phân tích cú pháp một email message được chứa hoàn toàn trong :term:`bytes-like object`, string hoặc file, nhưng API :class:`BytesParser` có thể thuận tiện hơn cho những trường hợp sử dụng như vậy. Ngữ nghĩa và kết quả của hai API parser là giống hệt nhau.

API của :class:`BytesFeedParser` rất đơn giản; bạn tạo một instance, feed cho nó một lượng byte cho đến khi không còn gì để feed nữa, rồi đóng parser để lấy đối tượng message gốc. :class:`BytesFeedParser` cực kỳ chính xác khi phân tích các message tuân thủ tiêu chuẩn, đồng thời xử lý rất tốt các message không tuân thủ, cung cấp thông tin về lý do message được xem là không hợp lệ. Nó sẽ điền vào đối tượng message một
thuộc tính :attr:`~email.message.EmailMessage.defects` chứa danh sách mọi vấn đề mà nó phát hiện trong một message. Xem module :mod:`email.errors` để biết danh sách các lỗi mà nó có thể phát hiện.

Sau đây là API cho :class:`BytesFeedParser`:


.. class:: BytesFeedParser(_factory=None, *, policy=policy.compat32)

   Tạo một instance :class:`BytesFeedParser`. *_factory* tùy chọn là một callable không có đối số; nếu không được chỉ định, hãy sử dụng
   :attr:`~email.policy.Policy.message_factory` từ *policy*. Gọi *_factory* mỗi khi cần một message object mới.

   Nếu *policy* được chỉ định, hãy sử dụng các quy tắc mà nó quy định để cập nhật biểu diễn của message. Nếu *policy* chưa được thiết lập, hãy sử dụng
   policy :class:`compat32 <email.policy.Compat32>`, duy trì khả năng tương thích ngược với phiên bản Python 3.2 của email package và cung cấp
   :class:`~email.message.Message` làm factory mặc định. Tất cả các policy khác cung cấp :class:`~email.message.EmailMessage` làm *_factory* mặc định. Để biết thêm thông tin về những gì *policy* kiểm soát, hãy xem
   Tài liệu về :mod:`~email.policy`.

   Lưu ý: **Luôn phải chỉ định từ khóa policy**; Giá trị mặc định sẽ thay đổi thành :data:`email.policy.default` trong một phiên bản Python tương lai.

   .. versionadded:: 3.2

   .. versionchanged:: 3.3 Đã thêm từ khóa *policy*.
   .. versionchanged:: 3.6 *_factory* mặc định sử dụng policy ``message_factory``.


   .. method:: feed(data)

      Cung cấp thêm dữ liệu cho parser. *data* phải là một :term:`bytes-like object` chứa một hoặc nhiều dòng. Các dòng có thể chưa hoàn chỉnh và parser sẽ ghép các dòng chưa hoàn chỉnh đó lại đúng cách. Các dòng có thể sử dụng bất kỳ kiểu kết thúc dòng phổ biến nào trong ba kiểu: carriage return, newline hoặc carriage return và newline (thậm chí có thể trộn lẫn).


   .. method:: close()

      Hoàn tất việc phân tích cú pháp tất cả dữ liệu đã cung cấp trước đó và trả về đối tượng message gốc. Không xác định được điều gì xảy ra nếu :meth:`~feed` được gọi sau khi phương thức này đã được gọi.


.. class:: FeedParser(_factory=None, *, policy=policy.compat32)

   Hoạt động giống như :class:`BytesFeedParser`, ngoại trừ đầu vào của
   Phương thức :meth:`~BytesFeedParser.feed` phải là một chuỗi. Điều này chỉ hữu ích ở mức hạn chế, vì cách duy nhất để một message như vậy hợp lệ là nó chỉ chứa văn bản ASCII hoặc, nếu :attr:`~email.policy.EmailPolicy.utf8` là ``True``, không có tệp đính kèm nhị phân.

   .. versionchanged:: 3.3 Đã thêm từ khóa *policy*.


API của Parser
^^^^^^^^^^^^^^

Lớp :class:`BytesParser`, được import từ module :mod:`!email.parser`, cung cấp một API có thể dùng để phân tích một message khi toàn bộ nội dung của message có trong một :term:`bytes-like object` hoặc tệp. Mô-đun
:mod:`!email.parser` cũng cung cấp :class:`Parser` để phân tích các chuỗi, cùng các parser chỉ dành cho header, :class:`BytesHeaderParser` và
:class:`HeaderParser`, có thể được sử dụng nếu bạn chỉ quan tâm đến các header của message. :class:`BytesHeaderParser` và :class:`HeaderParser` có thể nhanh hơn nhiều trong những tình huống này, vì chúng không cố gắng phân tích phần body của message mà thay vào đó đặt payload thành body thô.


.. class:: BytesParser(_class=None, *, policy=policy.compat32)

   Tạo một instance :class:`BytesParser`. Các đối số *_class* và *policy* có cùng ý nghĩa và ngữ nghĩa với các đối số *_factory* và *policy* của :class:`BytesFeedParser`.

   Lưu ý: **Từ khóa policy luôn phải được chỉ định**; Giá trị mặc định sẽ được đổi thành :data:`email.policy.default` trong một phiên bản Python tương lai.

   .. versionchanged:: 3.3
      Đã loại bỏ đối số *strict* vốn đã bị ngừng sử dụng từ phiên bản 2.4. Đã thêm từ khóa *policy*.
   .. versionchanged:: 3.6 *_class* mặc định sử dụng policy ``message_factory``.


   .. method:: parse(fp, headersonly=False)

      Đọc toàn bộ dữ liệu từ đối tượng giống tệp nhị phân *fp*, phân tích cú pháp các byte thu được và trả về đối tượng message. *fp* phải hỗ trợ cả hai phương thức :meth:`~io.IOBase.readline` và :meth:`~io.BufferedIOBase.read`.

      Các byte chứa trong *fp* phải được định dạng dưới dạng một khối các header kiểu :rfc:`5322` (hoặc, nếu :attr:`~email.policy.EmailPolicy.utf8` là ``True``, kiểu :rfc:`6532`) và các dòng tiếp tục header, tùy chọn có thể được đặt trước bởi một envelope header. Khối header kết thúc khi dữ liệu kết thúc hoặc khi gặp một dòng trống. Sau khối header là phần thân của message (có thể chứa các subpart được mã hóa MIME, bao gồm các subpart có :mailheader:`Content-Transfer-Encoding` là ``8bit``).

      *headersonly* tùy chọn là một cờ chỉ định có dừng phân tích cú pháp sau khi đọc các header hay không. Giá trị mặc định là ``False``, nghĩa là phân tích toàn bộ nội dung của tệp.


   .. method:: parsebytes(bytes, headersonly=False)

      Tương tự phương thức :meth:`parse` này, ngoại trừ việc phương thức nhận một :term:`bytes-like object` thay vì một đối tượng giống tệp. Việc gọi phương thức này trên một
      :term:`bytes-like object` tương đương với việc bọc *bytes* trong một
      :class:`~io.BytesIO` tạo instance trước và gọi :meth:`parse`.

      Tùy chọn *headersonly* cũng giống như với phương thức :meth:`parse`.

   .. versionadded:: 3.2


.. class:: BytesHeaderParser(_class=None, *, policy=policy.compat32)

   Hoàn toàn giống :class:`BytesParser`, ngoại trừ việc *headersonly* mặc định là ``True``.

   .. versionadded:: 3.3


.. class:: Parser(_class=None, *, policy=policy.compat32)

   Lớp này tương tự như :class:`BytesParser`, nhưng xử lý đầu vào dạng chuỗi.

   .. versionchanged:: 3.3
      Đã loại bỏ đối số *strict*. Đã thêm từ khóa *policy*.
   .. versionchanged:: 3.6 *_class* mặc định sử dụng policy ``message_factory``.


   .. method:: parse(fp, headersonly=False)

      Đọc toàn bộ dữ liệu từ đối tượng giống tệp ở chế độ văn bản *fp*, phân tích văn bản thu được và trả về đối tượng thông báo gốc. *fp* phải hỗ trợ cả :meth:`~io.TextIOBase.readline` và
      :meth:`~io.TextIOBase.read` các phương thức trên đối tượng giống tệp.

      Ngoài yêu cầu về chế độ văn bản, phương thức này hoạt động giống như
      :meth:`BytesParser.parse`.


   .. method:: parsestr(text, headersonly=False)

      Tương tự phương thức :meth:`parse`, nhưng nhận một đối tượng chuỗi thay vì đối tượng giống tệp. Gọi phương thức này trên một chuỗi tương đương với việc trước tiên bọc *text* trong một thực thể :class:`~io.StringIO` rồi gọi :meth:`parse`.

      Tùy chọn *headersonly* cũng giống như với phương thức :meth:`parse`.


.. class:: HeaderParser(_class=None, *, policy=policy.compat32)

   Hoàn toàn giống :class:`Parser`, ngoại trừ việc *headersonly* mặc định là ``True``.


Vì việc tạo cấu trúc đối tượng thông báo từ một chuỗi hoặc đối tượng tệp là một tác vụ rất phổ biến, bốn hàm được cung cấp để thuận tiện. Chúng có sẵn trong namespace package cấp cao nhất :mod:`email`.

.. currentmodule:: email


.. function:: message_from_bytes(s, _class=None, *, policy=policy.compat32)

   Trả về cấu trúc đối tượng message từ một :term:`bytes-like object`. Điều này tương đương với ``BytesParser().parsebytes(s)``. Các *_class* và *policy* tùy chọn được diễn giải như trong hàm khởi tạo lớp :class:`~email.parser.BytesParser`.

   .. versionadded:: 3.2
   .. versionchanged:: 3.3
      Đã loại bỏ đối số *strict*. Đã thêm từ khóa *policy*.


.. function:: message_from_binary_file(fp, _class=None, *, \
                                       policy=policy.compat32)

   Trả về cây cấu trúc đối tượng message từ một :term:`file object` nhị phân đang mở. Điều này tương đương với ``BytesParser().parse(fp)``. *_class* và *policy* được diễn giải như trong hàm khởi tạo lớp :class:`~email.parser.BytesParser`.

   .. versionadded:: 3.2
   .. versionchanged:: 3.3
      Đã loại bỏ đối số *strict*. Đã thêm từ khóa *policy*.


.. function:: message_from_string(s, _class=None, *, policy=policy.compat32)

   Trả về cấu trúc đối tượng message từ một chuỗi. Điều này tương đương với ``Parser().parsestr(s)``. *_class* và *policy* được diễn giải như trong hàm khởi tạo lớp :class:`~email.parser.Parser`.

   .. versionchanged:: 3.3
      Đã loại bỏ đối số *strict*. Đã thêm từ khóa *policy*.


.. function:: message_from_file(fp, _class=None, *, policy=policy.compat32)

   Trả về cây cấu trúc đối tượng thông điệp từ một :term:`file object` đang mở. Điều này tương đương với ``Parser().parse(fp)``. *_class* và *policy* được diễn giải giống như trong hàm khởi tạo lớp :class:`~email.parser.Parser`.

   .. versionchanged:: 3.3
      Đã loại bỏ đối số *strict*. Đã thêm từ khóa *policy*.
   .. versionchanged:: 3.6 *_class* mặc định sử dụng policy ``message_factory``.


Đây là ví dụ về cách bạn có thể sử dụng :func:`message_from_bytes` tại dấu nhắc Python tương tác::

   >>> import email
   >>> msg = email.message_from_bytes(myBytes)  # doctest: +SKIP


Ghi chú bổ sung
^^^^^^^^^^^^^^^

Dưới đây là một số ghi chú về ngữ nghĩa phân tích cú pháp:

* Hầu hết các tin nhắn có kiểu không phải \ :mimetype:`multipart` được phân tích cú pháp thành một đối tượng tin nhắn duy nhất với payload là một chuỗi. Các đối tượng này sẽ trả về ``False`` cho
  :meth:`~email.message.EmailMessage.is_multipart`, và
  :meth:`~email.message.EmailMessage.iter_parts` sẽ tạo ra một danh sách rỗng.

* Tất cả tin nhắn kiểu :mimetype:`multipart` sẽ được phân tích cú pháp thành một đối tượng tin nhắn container với payload là một danh sách các đối tượng tin nhắn con. Tin nhắn container bên ngoài sẽ trả về ``True`` cho
  :meth:`~email.message.EmailMessage.is_multipart`, và
  :meth:`~email.message.EmailMessage.iter_parts` sẽ tạo ra một danh sách các phần con.

* Hầu hết các tin nhắn có content type là :mimetype:`message/\*` (chẳng hạn như
  :mimetype:`message/delivery-status` và :mimetype:`message/rfc822`) cũng sẽ được phân tích cú pháp thành đối tượng container chứa payload dạng danh sách có độ dài 1. Các
  Phương thức :meth:`~email.message.EmailMessage.is_multipart` sẽ trả về ``True``. Phần tử duy nhất do :meth:`~email.message.EmailMessage.iter_parts` tạo ra sẽ là một đối tượng sub-message.

* Một số message không tuân thủ tiêu chuẩn có thể không nhất quán về mặt nội bộ đối với tính :mimetype:`multipart`\ -edness của chúng. Những message như vậy có thể có một
  header :mailheader:`Content-Type` thuộc kiểu :mimetype:`multipart`, nhưng
  phương thức :meth:`~email.message.EmailMessage.is_multipart` có thể trả về ``False``. Nếu những message như vậy được phân tích cú pháp bằng :class:`~email.parser.FeedParser`, chúng sẽ có một thể hiện của
  lớp :class:`~email.errors.MultipartInvariantViolationDefect` trong danh sách thuộc tính *defects* của chúng. Xem :mod:`email.errors` để biết chi tiết.
