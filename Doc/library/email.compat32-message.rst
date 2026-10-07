.. _compat32_message:

:mod:`email.message.Message`: Biểu diễn một email bằng API :data:`~email.policy.compat32`
-----------------------------------------------------------------------------------------

.. module:: email.message
   :synopsis: Lớp cơ sở biểu diễn các email theo cách tương thích ngược với Python 3.2
   :noindex:
   :no-index:


Lớp :class:`Message` rất tương tự như
lớp :class:`~email.message.EmailMessage`, nhưng không có các phương thức được lớp đó thêm vào, đồng thời hành vi mặc định của một số phương thức khác cũng hơi khác. Ở đây, chúng tôi cũng ghi lại một số phương thức tuy được lớp
:class:`~email.message.EmailMessage` hỗ trợ nhưng không được khuyến nghị, trừ khi bạn đang làm việc với mã legacy.

Về mặt khác, triết lý và cấu trúc của hai lớp này là như nhau.

Tài liệu này mô tả hành vi theo policy mặc định (dành cho :class:`Message`) :attr:`~email.policy.Compat32`. Nếu bạn định sử dụng policy khác, bạn nên sử dụng lớp :class:`~email.message.EmailMessage`.

Một email gồm *các header* và một *payload*.  Header phải là
các tên và giá trị theo kiểu :rfc:`5322`, trong đó tên trường và giá trị được phân cách bằng dấu hai chấm.  Dấu hai chấm không thuộc về tên trường hay giá trị trường.  Payload có thể là một thông điệp văn bản đơn giản, một đối tượng nhị phân hoặc một chuỗi có cấu trúc gồm các thông điệp con, mỗi thông điệp có tập header và payload riêng.  Loại payload sau được biểu thị bằng việc thông điệp có kiểu MIME như :mimetype:`multipart/\*` hoặc
:mimetype:`message/rfc822`.

Mô hình khái niệm do một đối tượng :class:`Message` cung cấp là một từ điển có thứ tự gồm các header, cùng các phương thức bổ sung để truy cập thông tin chuyên biệt từ header, truy cập payload, tạo phiên bản tuần tự hóa của thông điệp và duyệt đệ quy qua cây đối tượng.  Lưu ý rằng các header trùng lặp được hỗ trợ, nhưng phải sử dụng các phương thức đặc biệt để truy cập chúng.

Pseudo-dictionary :class:`Message` được lập chỉ mục theo tên header, các tên này phải là giá trị ASCII.  Các giá trị của dictionary là những chuỗi được cho là chỉ chứa các ký tự ASCII; có một số xử lý đặc biệt cho dữ liệu đầu vào không phải ASCII, nhưng không phải lúc nào cũng cho ra kết quả chính xác.  Header được lưu trữ và trả về dưới dạng giữ nguyên kiểu chữ, nhưng tên trường được so khớp không phân biệt chữ hoa chữ thường.  Ngoài ra có thể có một header phong bì duy nhất, còn được gọi là header *Unix-From* hoặc header ``From_``.  *Payload* либо là chuỗi hoặc bytes đối với các đối tượng thông điệp đơn giản, hoặc là một danh sách gồm
các đối tượng :class:`Message` đối với các tài liệu vùng chứa MIME (ví dụ như
:mimetype:`multipart/\*` và :mimetype:`message/rfc822`).

Sau đây là các phương thức của lớp :class:`Message`:


.. class:: Message(policy=compat32)

   Nếu *policy* được chỉ định (nó phải là một instance của lớp :mod:`~email.policy`), hãy sử dụng các quy tắc mà nó chỉ định để cập nhật và serialize biểu diễn của message. Nếu *policy* chưa được thiết lập, hãy sử dụng policy :class:`compat32 <email.policy.Compat32>`, policy này duy trì khả năng tương thích ngược với phiên bản Python 3.2 của package email. Để biết thêm thông tin, hãy xem
   tài liệu :mod:`~email.policy`.

   .. versionchanged:: 3.3 Đối số từ khóa *policy* đã được thêm vào.


   .. method:: as_string(unixfrom=False, maxheaderlen=0, policy=None)

      Trả về toàn bộ message đã được chuyển thành chuỗi. Khi *unixfrom* tùy chọn là true, header phong bì sẽ được đưa vào chuỗi trả về. *unixfrom* mặc định là ``False``. Vì lý do tương thích ngược, *maxheaderlen* mặc định là ``0``, do đó nếu muốn sử dụng giá trị khác, bạn phải ghi đè giá trị này một cách rõ ràng (giá trị được chỉ định cho *max_line_length* trong policy sẽ bị phương thức này bỏ qua). Có thể sử dụng đối số *policy* để ghi đè policy mặc định lấy từ instance của message. Bạn có thể dùng cách này để kiểm soát một số định dạng do phương thức tạo ra, vì *policy* được chỉ định sẽ được truyền cho ``Generator``.

      Việc chuyển message thành chuỗi có thể kích hoạt các thay đổi đối với :class:`Message` nếu cần điền các giá trị mặc định để hoàn tất quá trình chuyển đổi thành chuỗi (ví dụ: các MIME boundary có thể được tạo hoặc sửa đổi).

      Lưu ý rằng phương thức này được cung cấp để thuận tiện và có thể không phải lúc nào cũng định dạng message theo cách bạn muốn. Ví dụ: theo mặc định, phương thức này không xử lý việc biến đổi các dòng bắt đầu bằng ``From``, vốn là yêu cầu của định dạng Unix mbox. Để có thêm tính linh hoạt, hãy khởi tạo một
      instance :class:`~email.generator.Generator` và sử dụng
      :meth:`~email.generator.Generator.flatten` trực tiếp. Ví dụ::

         from io import StringIO
         from email.generator import Generator
         fp = StringIO()
         g = Generator(fp, mangle_from_=True, maxheaderlen=60)
         g.flatten(msg)
         text = fp.getvalue()

      Nếu đối tượng message chứa dữ liệu nhị phân không được mã hóa theo các tiêu chuẩn RFC, dữ liệu không tuân thủ sẽ được thay thế bằng các điểm mã Unicode “ký tự không xác định”. (Xem thêm :meth:`.as_bytes` và
      :class:`~email.generator.BytesGenerator`.)

      .. versionchanged:: 3.4 đối số từ khóa *policy* đã được bổ sung.


   .. method:: __str__()

      Tương đương với :meth:`.as_string`. Cho phép ``str(msg)`` tạo ra một chuỗi chứa message đã được định dạng.


   .. method:: as_bytes(unixfrom=False, policy=None)

      Trả về toàn bộ message đã được chuyển thành một đối tượng bytes. Khi *unixfrom* tùy chọn là true, header phong bì sẽ được включ trong chuỗi được trả về. *unixfrom* mặc định là ``False``. Đối số *policy* có thể được dùng để ghi đè policy mặc định lấy từ instance message. Có thể dùng đối số này để kiểm soát một số định dạng do method tạo ra, vì *policy* được chỉ định sẽ được truyền cho ``BytesGenerator``.

      Việc chuyển message thành chuỗi có thể kích hoạt các thay đổi đối với :class:`Message` nếu cần điền các giá trị mặc định để hoàn tất quá trình chuyển đổi thành chuỗi (ví dụ: các MIME boundary có thể được tạo hoặc sửa đổi).

      Lưu ý rằng phương thức này được cung cấp để thuận tiện và có thể không phải lúc nào cũng định dạng message theo cách bạn muốn. Ví dụ: theo mặc định, phương thức này không xử lý việc biến đổi các dòng bắt đầu bằng ``From``, vốn là yêu cầu của định dạng Unix mbox. Để có thêm tính linh hoạt, hãy khởi tạo một
      đối tượng :class:`~email.generator.BytesGenerator` và sử dụng phương thức của nó
      phương thức :meth:`~email.generator.BytesGenerator.flatten` trực tiếp. Ví dụ::

         from io import BytesIO
         from email.generator import BytesGenerator
         fp = BytesIO()
         g = BytesGenerator(fp, mangle_from_=True, maxheaderlen=60)
         g.flatten(msg)
         text = fp.getvalue()

      .. versionadded:: 3.4


   .. method:: __bytes__()

      Tương đương với :meth:`.as_bytes`. Cho phép ``bytes(msg)`` tạo ra một đối tượng bytes chứa thông điệp đã được định dạng.

      .. versionadded:: 3.4


   .. method:: is_multipart()

      Trả về ``True`` nếu payload của thông điệp là một danh sách các đối tượng \ :class:`Message` con, nếu không thì trả về ``False``. Khi
      :meth:`is_multipart` trả về ``False``, payload phải là một đối tượng chuỗi (có thể là payload nhị phân được mã hóa CTE). (Lưu ý rằng
      việc :meth:`is_multipart` trả về ``True`` không nhất thiết có nghĩa là "msg.get_content_maintype() == 'multipart'" sẽ trả về ``True``. Ví dụ, ``is_multipart`` sẽ trả về ``True`` khi
      :class:`Message` thuộc kiểu ``message/rfc822``.)


   .. method:: set_unixfrom(unixfrom)

      Đặt tiêu đề phong bì của message thành *unixfrom*, giá trị này phải là một chuỗi.


   .. method:: get_unixfrom()

      Trả về tiêu đề phong bì của message. Mặc định là ``None`` nếu tiêu đề phong bì chưa từng được đặt.


   .. method:: attach(payload)

      Thêm *payload* đã cho vào payload hiện tại, vốn phải là ``None`` hoặc một danh sách các đối tượng :class:`Message` trước khi gọi. Sau khi gọi, payload sẽ luôn là một danh sách các đối tượng :class:`Message`. Nếu muốn đặt payload thành một đối tượng vô hướng (ví dụ: một chuỗi), hãy sử dụng
      :meth:`set_payload` thay thế.

      Đây là một phương thức kế thừa. Trên
      lớp :class:`~email.message.EmailMessage`, chức năng của phương thức này được thay thế bằng :meth:`~email.message.EmailMessage.set_content` và các phương thức ``make`` và ``add`` liên quan.


   .. method:: get_payload(i=None, decode=False)

      Trả về payload hiện tại, đây sẽ là một danh sách các
      :class:`Message` các đối tượng khi :meth:`is_multipart` là ``True``, hoặc một chuỗi khi :meth:`is_multipart` là ``False``. Nếu payload là một danh sách và bạn thay đổi đối tượng danh sách, bạn sẽ sửa payload của message ngay tại chỗ.

      Với đối số tùy chọn *i*, :meth:`get_payload` sẽ trả về phần tử thứ *i* của payload, tính từ 0, nếu :meth:`is_multipart` là ``True``. Một :exc:`IndexError` sẽ được phát sinh nếu *i* nhỏ hơn 0 hoặc lớn hơn hoặc bằng số lượng mục trong payload. Nếu payload là một chuỗi (tức là :meth:`is_multipart` là ``False``) và *i* được cung cấp, một :exc:`TypeError` sẽ được phát sinh.

      *decode* tùy chọn là một cờ cho biết payload có nên được giải mã hay không, theo header :mailheader:`Content-Transfer-Encoding`. Khi ``True`` và message không phải là multipart, payload sẽ được giải mã nếu giá trị của header này là ``quoted-printable`` hoặc ``base64``. Nếu sử dụng một encoding khác, hoặc thiếu header :mailheader:`Content-Transfer-Encoding`, payload sẽ được trả về nguyên trạng (chưa được giải mã). Trong mọi trường hợp, giá trị trả về là dữ liệu nhị phân. Nếu message là multipart và cờ *decode* là ``True``, thì ``None`` được trả về. Nếu payload là base64 và không được định dạng hoàn chỉnh (thiếu padding, có ký tự nằm ngoài bảng chữ cái base64), thì một defect thích hợp sẽ được thêm vào thuộc tính defect của message (:class:`~email.errors.InvalidBase64PaddingDefect` hoặc
      :class:`~email.errors.InvalidBase64CharactersDefect`, tương ứng).

      Khi *decode* là ``False`` (mặc định), phần thân được trả về dưới dạng chuỗi mà không giải mã :mailheader:`Content-Transfer-Encoding`. Tuy nhiên, đối với :mailheader:`Content-Transfer-Encoding` có giá trị 8bit, một nỗ lực sẽ được thực hiện để giải mã các byte ban đầu bằng ``charset`` được chỉ định bởi
      :mailheader:`Content-Type` header, sử dụng trình xử lý lỗi ``replace``. Nếu không chỉ định ``charset``, hoặc nếu ``charset`` được cung cấp không được gói email nhận diện, phần thân sẽ được giải mã bằng charset ASCII mặc định.

      Đây là một phương thức kế thừa. Trên
      :class:`~email.message.EmailMessage` lớp này, chức năng của nó được thay thế bởi :meth:`~email.message.EmailMessage.get_content` và
      :meth:`~email.message.EmailMessage.iter_parts`.


   .. method:: set_payload(payload, charset=None)

      Đặt payload của toàn bộ đối tượng message thành *payload*.  Client có trách nhiệm đảm bảo các bất biến của payload.  *charset* tùy chọn đặt bộ ký tự mặc định của message; xem :meth:`set_charset` để biết chi tiết.

      Đây là một phương thức kế thừa. Trên
      :class:`~email.message.EmailMessage` lớp này, chức năng của nó được thay thế bởi :meth:`~email.message.EmailMessage.set_content`.


   .. method:: set_charset(charset)

      Đặt bộ ký tự của payload thành *charset*, có thể là một
      :class:`~email.charset.Charset` instance (xem :mod:`email.charset`), một chuỗi chỉ tên bộ ký tự hoặc ``None``.  Nếu là chuỗi, nó sẽ được chuyển đổi thành một instance :class:`~email.charset.Charset`.  Nếu *charset* là ``None``, tham số ``charset`` sẽ bị xóa khỏi
      :mailheader:`Content-Type` header (message sẽ không được sửa đổi theo cách nào khác).  Mọi giá trị khác sẽ tạo ra một :exc:`TypeError`.

      Nếu không có header :mailheader:`MIME-Version` hiện có thì sẽ thêm một header. Nếu không có header :mailheader:`Content-Type` hiện có thì sẽ thêm một header với giá trị :mimetype:`text/plain`. Dù
      :mailheader:`Content-Type` header đã tồn tại hay chưa, tham số ``charset`` của nó sẽ được đặt thành *charset.output_charset*. Nếu *charset.input_charset* và *charset.output_charset* khác nhau, payload sẽ được mã hóa lại thành *output_charset*. Nếu không có header hiện có
      :mailheader:`Content-Transfer-Encoding` thì payload sẽ được mã hóa chuyển tiếp nếu cần, bằng cách sử dụng
      :class:`~email.charset.Charset` được chỉ định, và một header với giá trị thích hợp sẽ được thêm vào. Nếu header :mailheader:`Content-Transfer-Encoding` đã tồn tại, payload được giả định là đã được mã hóa chính xác bằng :mailheader:`Content-Transfer-Encoding` đó và sẽ không bị thay đổi.

      Đây là một phương thức kế thừa. Trên
      Đối với lớp :class:`~email.message.EmailMessage`, chức năng của lớp này được thay thế bằng tham số *charset* của
      :meth:`email.message.EmailMessage.set_content` method.


   .. method:: get_charset()

      Trả về instance :class:`~email.charset.Charset` được liên kết với payload của message.

      Đây là một phương thức kế thừa. Trên
      Lớp :class:`~email.message.EmailMessage` luôn trả về ``None``.


   Các phương thức sau triển khai interface tương tự mapping để truy cập các header :rfc:`2822` của message. Lưu ý rằng có một số khác biệt về ngữ nghĩa giữa các phương thức này và interface mapping (tức là dictionary) thông thường. Ví dụ, trong dictionary không có các key trùng lặp, nhưng ở đây có thể có các header trùng lặp trong message. Ngoài ra, trong dictionary không có gì đảm bảo về thứ tự của các key được :meth:`keys` trả về, nhưng trong đối tượng :class:`Message`, các header luôn được trả về theo thứ tự chúng xuất hiện trong message ban đầu hoặc được thêm vào message sau đó. Mọi header bị xóa rồi được thêm lại luôn được nối vào cuối danh sách header.

   Những khác biệt về ngữ nghĩa này là có chủ đích và thiên về sự thuận tiện tối đa.

   Lưu ý rằng trong mọi trường hợp, mọi envelope header có trong message đều không được đưa vào interface mapping.

   Trong model được tạo từ các byte, mọi giá trị header chứa các byte không phải ASCII (trái với quy định của RFC) khi được truy xuất qua interface này sẽ được biểu diễn dưới dạng các đối tượng :class:`~email.header.Header` với charset là ``unknown-8bit``.


   .. method:: __len__()

      Trả về tổng số header, bao gồm cả các header trùng lặp.


   .. method:: __contains__(name)

      Trả về ``True`` nếu đối tượng message có một trường tên *name*. Việc so khớp không phân biệt chữ hoa chữ thường và *name* không được bao gồm dấu hai chấm ở cuối. Được dùng cho toán tử ``in``, ví dụ:::

           if 'message-id' in myMessage:
              print('Message-ID:', myMessage['message-id'])


   .. method:: __getitem__(name)

      Trả về giá trị của trường header có tên được chỉ định.  *name* không được bao gồm dấu phân cách trường là dấu hai chấm.  Nếu thiếu header, ``None`` sẽ được trả về; một
      :exc:`KeyError` không bao giờ được phát sinh.

      Lưu ý rằng nếu trường có tên được chỉ định xuất hiện nhiều lần trong các header của message, không xác định chính xác giá trị nào trong số các giá trị đó sẽ được trả về.  Sử dụng phương thức :meth:`get_all` để lấy các giá trị của tất cả header hiện có với tên được chỉ định.


   .. method:: __setitem__(name, val)

      Thêm một header vào message với tên trường *name* và giá trị *val*.  Trường này được thêm vào cuối các trường hiện có của message.

      Lưu ý rằng thao tác này *not* ghi đè hoặc xóa bất kỳ header hiện có nào có cùng tên.  Nếu muốn đảm bảo header mới là header duy nhất có mặt trong message với tên trường *name*, trước tiên hãy xóa trường đó, ví dụ:::

         del msg['subject']
         msg['subject'] = 'Python roolz!'


   .. method:: __delitem__(name)

      Xóa mọi lần xuất hiện của trường có tên *name* khỏi các header của message. Không có exception nào được đưa ra nếu trường có tên đó không tồn tại trong các header.


   .. method:: keys()

      Trả về danh sách tên của tất cả các trường header của message.


   .. method:: values()

      Trả về danh sách giá trị của tất cả các trường trong message.


   .. method:: items()

      Trả về danh sách các tuple 2 phần tử chứa tất cả header trường và giá trị của message.


   .. method:: get(name, failobj=None)

      Trả về giá trị của trường header có tên được chỉ định. Điều này giống hệt
      :meth:`~object.__getitem__` ngoại trừ việc *failobj* tùy chọn được trả về nếu header có tên bị thiếu (mặc định là ``None``).

   Dưới đây là một số phương thức hữu ích khác:


   .. method:: get_all(name, failobj=None)

      Trả về danh sách tất cả các giá trị của trường có tên *name*. Nếu thông điệp không có header nào mang tên đó, *failobj* sẽ được trả về (mặc định là ``None``).


   .. method:: add_header(_name, _value, **_params)

      Thiết lập header mở rộng. Phương thức này tương tự :meth:`__setitem__`, ngoại trừ việc có thể cung cấp thêm các tham số của header dưới dạng keyword argument. *_name* là trường header cần thêm và *_value* là giá trị *primary* của header.

      Với mỗi mục trong dictionary keyword argument *_params*, khóa được dùng làm tên tham số, trong đó dấu gạch dưới được chuyển thành dấu gạch ngang (vì dấu gạch ngang không hợp lệ trong các định danh Python). Thông thường, tham số sẽ được thêm dưới dạng ``key="value"``, nhưng nếu giá trị là ``None`` thì chỉ có khóa được thêm vào. Nếu giá trị chứa các ký tự non-ASCII, có thể chỉ định giá trị đó dưới dạng tuple ba phần tử theo định dạng ``(CHARSET, LANGUAGE, VALUE)``, trong đó ``CHARSET`` là chuỗi chỉ định charset dùng để mã hóa giá trị, ``LANGUAGE`` thường có thể được đặt thành ``None`` hoặc chuỗi rỗng (xem :rfc:`2231` để biết các tùy chọn khác), còn ``VALUE`` là chuỗi giá trị chứa các code point non-ASCII. Nếu không truyền tuple ba phần tử mà giá trị chứa các ký tự non-ASCII, giá trị sẽ tự động được mã hóa theo định dạng :rfc:`2231` bằng ``CHARSET`` là ``utf-8`` và ``LANGUAGE`` là ``None``.

      Đây là một ví dụ::

         msg.add_header('Content-Disposition', 'attachment', filename='bud.gif')

      Thao tác này sẽ thêm một header có dạng::

         Content-Disposition: attachment; filename="bud.gif"

      Ví dụ với các ký tự non-ASCII::

         msg.add_header('Content-Disposition', 'attachment',
                        filename=('iso-8859-1', '', 'Fußballer.ppt'))

      Kết quả là::

         Content-Disposition: attachment; filename*="iso-8859-1''Fu%DFballer.ppt"


   .. method:: replace_header(_name, _value)

      Thay thế một header. Thay thế header đầu tiên được tìm thấy trong message khớp với *_name*, đồng thời giữ nguyên thứ tự header và kiểu chữ của tên trường. Nếu không tìm thấy header nào khớp, một :exc:`KeyError` sẽ được raise.


   .. method:: get_content_type()

      Trả về content type của message. Chuỗi được trả về sẽ được chuyển thành chữ thường theo dạng :mimetype:`maintype/subtype`. Nếu không có
      header :mailheader:`Content-Type` trong message, type mặc định do :meth:`get_default_type` cung cấp sẽ được trả về. Vì theo
      :rfc:`2045`, message luôn có một type mặc định, :meth:`get_content_type` sẽ luôn trả về một giá trị.

      :rfc:`2045` xác định type mặc định của một message là :mimetype:`text/plain`, trừ khi message xuất hiện bên trong một container :mimetype:`multipart/digest`, trong trường hợp đó type sẽ là :mimetype:`message/rfc822`. Nếu
      header :mailheader:`Content-Type` có đặc tả type không hợp lệ,
      :rfc:`2045` yêu cầu type mặc định phải là :mimetype:`text/plain`.


   .. method:: get_content_maintype()

      Trả về loại nội dung chính của message. Đây là phần :mimetype:`maintype` trong chuỗi được :meth:`get_content_type` trả về.


   .. method:: get_content_subtype()

      Trả về loại nội dung phụ của message. Đây là phần :mimetype:`subtype` trong chuỗi được :meth:`get_content_type` trả về.


   .. method:: get_default_type()

      Trả về loại nội dung mặc định. Hầu hết message có loại nội dung mặc định là :mimetype:`text/plain`, ngoại trừ các message là subpart của
      container :mimetype:`multipart/digest`. Các subpart như vậy có loại nội dung mặc định là :mimetype:`message/rfc822`.


   .. method:: set_default_type(ctype)

      Đặt loại nội dung mặc định. *ctype* phải là một trong các giá trị
      :mimetype:`text/plain` hoặc :mimetype:`message/rfc822`, mặc dù điều này không được bắt buộc. Loại nội dung mặc định không được lưu trong
      header :mailheader:`Content-Type`.


   .. method:: get_params(failobj=None, header='content-type', unquote=True)

      Trả về các tham số :mailheader:`Content-Type` của thư, dưới dạng một danh sách. Các phần tử trong danh sách được trả về là các bộ 2 gồm những cặp khóa/giá trị, được tách theo dấu ``'='``. Vế trái của ``'='`` là khóa, còn vế phải là giá trị. Nếu tham số không có dấu ``'='`` thì giá trị là chuỗi rỗng; nếu không, giá trị được mô tả trong :meth:`get_param` và sẽ được bỏ dấu ngoặc kép nếu tùy chọn *unquote* là ``True`` (mặc định).

      *failobj* tùy chọn là đối tượng được trả về nếu không có
      :mailheader:`Content-Type` header. *header* tùy chọn là header cần tìm thay cho :mailheader:`Content-Type`.

      Đây là một phương thức kế thừa. Trên
      Trong lớp :class:`~email.message.EmailMessage`, chức năng này được thay thế bằng thuộc tính *params* của từng đối tượng header được các phương thức truy cập header trả về.


   .. method:: get_param(param, failobj=None, header='content-type', unquote=True)

      Trả về giá trị của tham số *param* trong header :mailheader:`Content-Type` dưới dạng chuỗi. Nếu thư không có header :mailheader:`Content-Type` hoặc không có tham số như vậy, thì *failobj* được trả về (mặc định là ``None``).

      *header* tùy chọn, nếu được cung cấp, chỉ định header của thư cần sử dụng thay cho
      :mailheader:`Content-Type`.

      Các khóa tham số luôn được so sánh không phân biệt chữ hoa chữ thường. Giá trị trả về có thể là một chuỗi hoặc một bộ 3 phần tử nếu tham số được mã hóa :rfc:`2231`. Khi là một bộ 3 phần tử, các phần tử của giá trị có dạng ``(CHARSET, LANGUAGE, VALUE)``. Lưu ý rằng cả ``CHARSET`` và ``LANGUAGE`` đều có thể là ``None``, trong trường hợp đó bạn nên xem ``VALUE`` là được mã hóa bằng bộ ký tự ``us-ascii``. Thông thường bạn có thể bỏ qua ``LANGUAGE``.

      Nếu ứng dụng của bạn không quan tâm tham số có được mã hóa như trong
      :rfc:`2231`, bạn có thể thu gọn giá trị tham số bằng cách gọi
      :func:`email.utils.collapse_rfc2231_value`, truyền giá trị trả về từ :meth:`get_param`. Thao tác này sẽ trả về một chuỗi Unicode được giải mã phù hợp khi giá trị là một bộ, hoặc chuỗi ban đầu sau khi bỏ dấu trích dẫn nếu không phải. Ví dụ::

         rawparam = msg.get_param('foo')
         param = email.utils.collapse_rfc2231_value(rawparam)

      Trong mọi trường hợp, giá trị tham số (chuỗi được trả về hoặc phần tử ``VALUE`` trong bộ 3 phần tử) luôn không có dấu trích dẫn, trừ khi *unquote* được đặt thành ``False``.

      Đây là một phương thức kế thừa. Trên
      Trong lớp :class:`~email.message.EmailMessage`, chức năng này được thay thế bằng thuộc tính *params* của từng đối tượng header được các phương thức truy cập header trả về.


   .. method:: set_param(param, value, header='Content-Type', requote=True, \
                         charset=None, language='', replace=False)

      Đặt một tham số trong tiêu đề :mailheader:`Content-Type`. Nếu tham số đó đã tồn tại trong tiêu đề, giá trị của nó sẽ được thay thế bằng *value*. Nếu tiêu đề :mailheader:`Content-Type` chưa được định nghĩa cho thư này, tiêu đề sẽ được đặt thành :mimetype:`text/plain` và giá trị tham số mới sẽ được nối thêm theo :rfc:`2045`.

      *header* tùy chọn chỉ định một tiêu đề thay thế cho
      :mailheader:`Content-Type`, và tất cả các tham số sẽ được đặt trong dấu ngoặc kép khi cần, trừ khi *requote* tùy chọn là ``False`` (mặc định là ``True``).

      Nếu chỉ định *charset* tùy chọn, tham số sẽ được mã hóa theo :rfc:`2231`. *language* tùy chọn chỉ định ngôn ngữ RFC 2231, mặc định là chuỗi rỗng. Cả *charset* và *language* đều phải là chuỗi.

      Nếu *replace* là ``False`` (mặc định), tiêu đề sẽ được chuyển đến cuối danh sách các tiêu đề. Nếu *replace* là ``True``, tiêu đề sẽ được cập nhật tại vị trí hiện tại.

      .. versionchanged:: 3.4 Đã thêm từ khóa ``replace``.


   .. method:: del_param(param, header='content-type', requote=True)

      Xóa hoàn toàn tham số đã cho khỏi header :mailheader:`Content-Type`. Header sẽ được ghi lại tại chỗ mà không có tham số hoặc giá trị của tham số đó. Mọi giá trị sẽ được đặt trong dấu ngoặc kép khi cần, trừ khi *requote* là ``False`` (mặc định là ``True``). Tùy chọn *header* chỉ định một header thay thế cho :mailheader:`Content-Type`.


   .. method:: set_type(type, header='Content-Type', requote=True)

      Đặt kiểu chính và kiểu phụ cho header :mailheader:`Content-Type`. *type* phải là một chuỗi có dạng :mimetype:`maintype/subtype`, nếu không sẽ phát sinh :exc:`ValueError`.

      Phương thức này thay thế header :mailheader:`Content-Type`, giữ nguyên tất cả các tham số. Nếu *requote* là ``False``, cách đặt dấu ngoặc kép của header hiện có sẽ được giữ nguyên; nếu không, các tham số sẽ được đặt trong dấu ngoặc kép (đây là mặc định).

      Có thể chỉ định một header thay thế trong đối số *header*. Khi
      Header :mailheader:`Content-Type` được đặt, một header :mailheader:`MIME-Version` cũng được thêm vào.

      Đây là một phương thức kế thừa. Trên
      Trong lớp :class:`~email.message.EmailMessage` class, chức năng của lớp này được thay thế bằng các phương thức ``make_`` và ``add_``.


   .. method:: get_filename(failobj=None)

      Trả về giá trị của tham số ``filename`` của
      tiêu đề :mailheader:`Content-Disposition` của thư. Nếu tiêu đề không có tham số ``filename``, phương thức này chuyển sang tìm tham số ``name`` trên tiêu đề :mailheader:`Content-Type`. Nếu không tìm thấy cả hai hoặc tiêu đề bị thiếu, thì *failobj* được trả về. Chuỗi được trả về luôn ở dạng không có dấu ngoặc kép theo
      :func:`email.utils.unquote`.


   .. method:: get_boundary(failobj=None)

      Trả về giá trị của tham số ``boundary`` của
      tiêu đề :mailheader:`Content-Type` của thư, hoặc *failobj* nếu tiêu đề bị thiếu hoặc không có tham số ``boundary``. Chuỗi được trả về luôn ở dạng không có dấu ngoặc kép theo :func:`email.utils.unquote`.


   .. method:: set_boundary(boundary)

      Đặt tham số ``boundary`` của tiêu đề :mailheader:`Content-Type` thành *boundary*. :meth:`set_boundary` sẽ luôn đặt *boundary* trong dấu ngoặc kép nếu cần. Một :exc:`~email.errors.HeaderParseError` sẽ được nêu nếu đối tượng thư không có tiêu đề :mailheader:`Content-Type`.

      Lưu ý rằng việc sử dụng phương thức này hơi khác so với việc xóa tiêu đề cũ
      :mailheader:`Content-Type` và thêm một tiêu đề mới với boundary mới thông qua :meth:`add_header`, vì :meth:`set_boundary` bảo toàn thứ tự của tiêu đề :mailheader:`Content-Type` trong danh sách tiêu đề. Tuy nhiên, nó *not* bảo toàn bất kỳ dòng tiếp nối nào có thể đã có trong tiêu đề :mailheader:`Content-Type` ban đầu.


   .. method:: get_content_charset(failobj=None)

      Trả về tham số ``charset`` của header :mailheader:`Content-Type`, được chuyển thành chữ thường. Nếu không có header :mailheader:`Content-Type`, hoặc header đó không có tham số ``charset``, *failobj* sẽ được trả về.

      Lưu ý rằng phương thức này khác với :meth:`get_charset`, vốn trả về
      :class:`~email.charset.Charset` cho encoding mặc định của phần thân message.


   .. method:: get_charsets(failobj=None)

      Trả về danh sách chứa tên các bộ ký tự trong message. Nếu message là :mimetype:`multipart`, danh sách sẽ chứa một phần tử cho mỗi subpart trong payload; nếu không, danh sách sẽ có độ dài là 1.

      Mỗi mục trong danh sách sẽ là một chuỗi, chính là giá trị của tham số ``charset`` trong header :mailheader:`Content-Type` của subpart được biểu diễn. Tuy nhiên, nếu subpart không có
      header :mailheader:`Content-Type`, không có tham số ``charset``, hoặc không thuộc MIME main type :mimetype:`text`, thì mục tương ứng trong danh sách được trả về sẽ là *failobj*.


   .. method:: get_content_disposition()

      Trả về giá trị viết thường (không kèm tham số) của
      :mailheader:`Content-Disposition` header nếu có, hoặc ``None``. Các giá trị có thể có của phương thức này là *inline*, *attachment* hoặc ``None`` nếu thông báo tuân theo :rfc:`2183`.

      .. versionadded:: 3.5

   .. method:: walk()

      Phương thức :meth:`walk` là một generator đa dụng, có thể được sử dụng để lặp qua tất cả các phần và phần con của cây đối tượng thông báo theo thứ tự duyệt depth-first. Thông thường, bạn sẽ sử dụng :meth:`walk` làm iterator trong vòng lặp ``for``; mỗi lần lặp trả về phần con tiếp theo.

      Dưới đây là một ví dụ in ra MIME type của mọi phần trong một cấu trúc thông báo multipart:

      .. testsetup::

         import email
         from email import message_from_binary_file
         from os.path import join, dirname
         lib_dir = dirname(dirname(email.__file__))
         file_path = join(lib_dir, 'test/test_email/data/msg_16.txt')
         with open(file_path, 'rb') as f:
             msg = message_from_binary_file(f)
         from email.iterators import _structure

      .. doctest::

         >>> for part in msg.walk():
         ...     print(part.get_content_type())
         multipart/report
         text/plain
         message/delivery-status
         text/plain
         text/plain
         message/rfc822
         text/plain

      ``walk`` lặp qua các phần con của mọi phần mà
      :meth:`is_multipart` trả về ``True``, mặc dù ``msg.get_content_maintype() == 'multipart'`` có thể trả về ``False``. Ta có thể thấy điều này trong ví dụ bằng cách sử dụng hàm trợ giúp gỡ lỗi ``_structure``:

      .. doctest::

         >>> for part in msg.walk():
         ...     print(part.get_content_maintype() == 'multipart',
         ...           part.is_multipart())
         True True
         False False
         False True
         False False
         False False
         False True
         False False
         >>> _structure(msg)
         multipart/report
             text/plain
             message/delivery-status
                 text/plain
                 text/plain
             message/rfc822
                 text/plain

      Ở đây, các phần ``message`` không phải là ``multiparts``, nhưng chúng có chứa các phần con. ``is_multipart()`` trả về ``True`` và ``walk`` đi sâu vào các phần con.


   Các đối tượng :class:`Message` cũng có thể tùy chọn chứa hai thuộc tính của instance, được sử dụng khi tạo văn bản thuần của một thông báo MIME.


   .. attribute:: preamble

      Định dạng của một tài liệu MIME cho phép có một phần văn bản nằm giữa dòng trống sau các header và chuỗi boundary multipart đầu tiên. Thông thường, phần văn bản này không bao giờ hiển thị trong trình đọc thư hỗ trợ MIME vì nó nằm ngoài phần bao bọc MIME tiêu chuẩn. Tuy nhiên, khi xem văn bản thô của thư hoặc xem thư trong trình đọc không hỗ trợ MIME, phần văn bản này có thể trở nên hiển thị.

      Thuộc tính *preamble* chứa phần văn bản bao bọc bổ sung ở đầu này của các tài liệu MIME. Khi :class:`~email.parser.Parser` phát hiện một phần văn bản sau các header nhưng trước chuỗi boundary đầu tiên, nó gán phần văn bản này cho thuộc tính *preamble* của message. Khi
      :class:`~email.generator.Generator` đang ghi biểu diễn văn bản thuần túy của một message MIME và phát hiện message có thuộc tính *preamble*, nó sẽ ghi phần văn bản này vào khu vực giữa các header và boundary đầu tiên. Xem :mod:`email.parser` và
      :mod:`email.generator` để biết chi tiết.

      Lưu ý rằng nếu đối tượng message không có preamble, thuộc tính *preamble* sẽ là ``None``.


   .. attribute:: epilogue

      Thuộc tính *epilogue* hoạt động giống như thuộc tính *preamble*, ngoại trừ việc nó chứa phần văn bản xuất hiện giữa boundary cuối cùng và phần cuối của message.

      Bạn không cần đặt epilogue thành chuỗi rỗng để
      :class:`~email.generator.Generator` để in ký tự xuống dòng ở cuối tệp.


   .. attribute:: defects

      Thuộc tính *defects* chứa danh sách tất cả các vấn đề được phát hiện khi phân tích cú pháp thông báo này. Xem :mod:`email.errors` để biết mô tả chi tiết về các lỗi phân tích cú pháp có thể xảy ra.
