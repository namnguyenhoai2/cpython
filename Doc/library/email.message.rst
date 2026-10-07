:mod:`!email.message`: Biểu diễn một thông điệp email
-----------------------------------------------------

.. module:: email.message
   :synopsis: Lớp cơ sở biểu diễn các thông điệp email.
.. moduleauthor:: R. David Murray <rdmurray@bitdance.com>
.. sectionauthor:: R. David Murray <rdmurray@bitdance.com>,
                   Barry A. Warsaw <barry@python.org>

**Mã nguồn:** :source:`Lib/email/message.py`

--------------

.. versionadded:: 3.6 [1]_

Lớp trung tâm trong gói :mod:`email` là lớp :class:`EmailMessage`, được nhập từ mô-đun :mod:`!email.message`. Đây là lớp cơ sở cho mô hình đối tượng :mod:`email`. :class:`EmailMessage` cung cấp chức năng cốt lõi để thiết lập và truy vấn các trường tiêu đề, truy cập phần nội dung thông điệp cũng như tạo hoặc sửa đổi các thông điệp có cấu trúc.

Một thông điệp email gồm *tiêu đề* và một *payload* (còn được gọi là *nội dung*). Tiêu đề là các tên và giá trị trường theo kiểu :rfc:`5322` hoặc :rfc:`6532`, trong đó tên trường và giá trị được phân tách bằng dấu hai chấm. Dấu hai chấm không thuộc về tên trường cũng như giá trị trường. Payload có thể là một thông điệp văn bản đơn giản, một đối tượng nhị phân hoặc một chuỗi có cấu trúc gồm các thông điệp con, mỗi thông điệp có tập tiêu đề và payload riêng. Loại payload sau được biểu thị bằng việc thông điệp có kiểu MIME như
:mimetype:`multipart/\*` hoặc :mimetype:`message/rfc822`.

Mô hình khái niệm do một đối tượng :class:`EmailMessage` cung cấp là một từ điển có thứ tự gồm các tiêu đề kết hợp với *payload* đại diện cho
:rfc:`5322` phần thân của thư, có thể là một danh sách các đối tượng con-``EmailMessage``. Ngoài các phương thức từ điển thông thường để truy cập tên và giá trị của các header, còn có các phương thức để truy cập thông tin chuyên biệt từ các header (ví dụ: kiểu nội dung MIME), thao tác trên payload, tạo phiên bản đã tuần tự hóa của thư và duyệt đệ quy qua cây đối tượng.

Giao diện giống từ điển :class:`EmailMessage` được lập chỉ mục theo tên các header, vốn phải là các giá trị ASCII. Các giá trị của từ điển là các chuỗi có thêm một số phương thức. Header được lưu trữ và trả về với kiểu chữ được giữ nguyên, nhưng tên trường được so khớp không phân biệt chữ hoa chữ thường. Các khóa được sắp xếp theo thứ tự, nhưng không giống một dict thực sự, chúng có thể bị trùng lặp. Có thêm các phương thức để làm việc với các header có khóa trùng lặp.

*payload* là một đối tượng chuỗi hoặc bytes trong trường hợp các đối tượng thư đơn giản, hoặc là một danh sách các đối tượng :class:`EmailMessage` đối với các tài liệu container MIME, chẳng hạn như các đối tượng thư :mimetype:`multipart/\*` và :mimetype:`message/rfc822`.


.. class:: EmailMessage(policy=default)

   Nếu *policy* được chỉ định, hãy sử dụng các quy tắc mà nó chỉ định để cập nhật và tuần tự hóa biểu diễn của thư. Nếu *policy* chưa được thiết lập, hãy sử dụng
   :class:`~email.policy.default` policy, tuân theo các quy tắc của các RFC về email, ngoại trừ phần kết thúc dòng (thay vì ``\r\n`` bắt buộc theo RFC, nó sử dụng phần kết thúc dòng tiêu chuẩn ``\n`` của Python). Để biết thêm thông tin, hãy xem
   tài liệu :mod:`~email.policy`. [2]_

   .. method:: as_string(unixfrom=False, maxheaderlen=None, policy=None)

      Trả về toàn bộ thư đã được làm phẳng dưới dạng một chuỗi. Khi *unixfrom* tùy chọn là true, header phong bì được đưa vào chuỗi trả về. *unixfrom* mặc định là ``False``. Để tương thích ngược với lớp cơ sở :class:`~email.message.Message`, *maxheaderlen* được chấp nhận, nhưng mặc định là ``None``, nghĩa là theo mặc định, độ dài dòng được kiểm soát bởi
      :attr:`~email.policy.Policy.max_line_length` của policy. Đối số *policy* có thể được sử dụng để ghi đè policy mặc định nhận được từ message instance. Điều này có thể được dùng để kiểm soát một số định dạng do method tạo ra, vì *policy* được chỉ định sẽ được truyền vào :class:`~email.generator.Generator`.

      Việc flatten message có thể kích hoạt các thay đổi đối với :class:`EmailMessage` nếu cần điền các giá trị mặc định để hoàn tất quá trình chuyển đổi thành một chuỗi (ví dụ: các MIME boundary có thể được tạo hoặc sửa đổi).

      Lưu ý rằng method này được cung cấp như một tiện ích và có thể không phải là cách hữu ích nhất để serialize các message trong ứng dụng của bạn, đặc biệt nếu bạn đang xử lý nhiều message. Xem
      :class:`email.generator.Generator` để sử dụng API linh hoạt hơn cho việc serialize các message. Cũng lưu ý rằng method này bị giới hạn ở việc tạo ra các message được serialize dưới dạng "7 bit clean" khi
      :attr:`~email.policy.EmailPolicy.utf8` là ``False``, đây là giá trị mặc định.

      .. versionchanged:: 3.6 hành vi mặc định khi *maxheaderlen*
         không được chỉ định đã được thay đổi từ giá trị mặc định là 0 thành giá trị của *max_line_length* trong policy.


   .. method:: __str__()

      Tương đương với ``as_string(policy=self.policy.clone(utf8=True))``. Cho phép ``str(msg)`` tạo ra một chuỗi chứa thông điệp đã được tuần tự hóa ở định dạng dễ đọc.

      .. versionchanged:: 3.4 phương thức này đã được thay đổi để sử dụng ``utf8=True``,
         do đó tạo ra một biểu diễn thông điệp tương tự :rfc:`6531`, thay vì là bí danh trực tiếp của :meth:`as_string`.


   .. method:: as_bytes(unixfrom=False, policy=None)

      Trả về toàn bộ thông điệp đã được chuyển phẳng dưới dạng đối tượng bytes. Khi *unixfrom* tùy chọn là true, header phong bì được đưa vào chuỗi trả về. *unixfrom* mặc định là ``False``. Có thể sử dụng đối số *policy* để ghi đè policy mặc định nhận được từ thực thể thông điệp. Điều này có thể được dùng để kiểm soát một số định dạng do phương thức tạo ra, vì *policy* được chỉ định sẽ được truyền cho
      :class:`~email.generator.BytesGenerator`.

      Việc flatten message có thể kích hoạt các thay đổi đối với :class:`EmailMessage` nếu cần điền các giá trị mặc định để hoàn tất quá trình chuyển đổi thành một chuỗi (ví dụ: các MIME boundary có thể được tạo hoặc sửa đổi).

      Lưu ý rằng method này được cung cấp như một tiện ích và có thể không phải là cách hữu ích nhất để serialize các message trong ứng dụng của bạn, đặc biệt nếu bạn đang xử lý nhiều message. Xem
      :class:`email.generator.BytesGenerator` để có API linh hoạt hơn cho việc tuần tự hóa thông điệp.


   .. method:: __bytes__()

      Tương đương với :meth:`.as_bytes`. Cho phép ``bytes(msg)`` tạo ra một đối tượng bytes chứa message đã được serialize.


   .. method:: is_multipart()

      Trả về ``True`` nếu payload của message là một danh sách các đối tượng \ :class:`EmailMessage` con, nếu không thì trả về ``False``. Khi
      :meth:`is_multipart` trả về ``False``, payload phải là một đối tượng chuỗi (có thể là payload nhị phân được mã hóa CTE). Lưu ý rằng
      :meth:`is_multipart` trả về ``True`` không nhất thiết có nghĩa là "msg.get_content_maintype() == 'multipart'" sẽ trả về ``True``. Ví dụ: ``is_multipart`` sẽ trả về ``True`` khi
      :class:`EmailMessage` có kiểu ``message/rfc822``.


   .. method:: set_unixfrom(unixfrom)

      Đặt envelope header của message thành *unixfrom*, giá trị này phải là một chuỗi. (Xem :class:`~mailbox.mboxMessage` để biết mô tả ngắn gọn về header này.)


   .. method:: get_unixfrom()

      Trả về envelope header của message. Mặc định là ``None`` nếu envelope header chưa bao giờ được đặt.


   Các phương thức sau đây triển khai interface giống mapping để truy cập các header của message. Lưu ý rằng có một số khác biệt về ngữ nghĩa giữa các phương thức này và interface mapping thông thường (tức dictionary). Ví dụ, trong dictionary không có các key trùng lặp, nhưng ở đây có thể có các header message trùng lặp. Ngoài ra, trong dictionary không có bảo đảm về thứ tự của các key được :meth:`keys`, nhưng trong một đối tượng :class:`EmailMessage`, các header luôn được trả về theo thứ tự chúng xuất hiện trong message ban đầu hoặc theo thứ tự chúng được thêm vào message sau đó. Bất kỳ header nào bị xóa rồi được thêm lại sẽ luôn được nối vào cuối danh sách header.

   Những khác biệt về ngữ nghĩa này là có chủ ý và được thiên về sự tiện lợi trong các trường hợp sử dụng phổ biến nhất.

   Lưu ý rằng trong mọi trường hợp, bất kỳ envelope header nào có trong message cũng không được đưa vào interface mapping.


   .. method:: __len__()

      Trả về tổng số header, bao gồm cả các header trùng lặp.


   .. method:: __contains__(name)

      Trả về ``True`` nếu đối tượng message có một trường có tên là *name*. Việc so khớp không phân biệt chữ hoa chữ thường và *name* không bao gồm dấu hai chấm ở cuối. Được sử dụng cho toán tử ``in``. Ví dụ::

           if 'message-id' in myMessage:
              print('Message-ID:', myMessage['message-id'])


   .. method:: __getitem__(name)

      Trả về giá trị của trường header có tên được chỉ định. *name* không bao gồm dấu phân cách trường là dấu hai chấm. Nếu không tìm thấy header, ``None`` được trả về; một
      :exc:`KeyError` không bao giờ được ném ra.

      Lưu ý rằng nếu trường có tên đã chỉ định xuất hiện nhiều hơn một lần trong phần header của thông điệp, thì không xác định được chính xác giá trị nào trong các giá trị của trường đó sẽ được trả về. Sử dụng phương thức :meth:`get_all` để lấy giá trị của tất cả các header hiện có có tên *name*.

      Khi sử dụng các policy tiêu chuẩn (không phải ``compat32``), giá trị được trả về là một thể hiện của một lớp con của :class:`email.headerregistry.BaseHeader`.


   .. method:: __setitem__(name, val)

      Thêm một header vào thông điệp với tên trường *name* và giá trị *val*. Trường này được nối vào cuối các header hiện có của thông điệp.

      Lưu ý rằng thao tác này *not* ghi đè hoặc xóa bất kỳ header hiện có nào có cùng tên. Nếu muốn đảm bảo header mới là header duy nhất trong thông điệp có tên trường *name*, trước tiên hãy xóa trường đó, chẳng hạn như:::

         del msg['subject']
         msg['subject'] = 'Python roolz!'

      Nếu :mod:`policy <email.policy>` xác định một số header là duy nhất (như các policy tiêu chuẩn), phương thức này có thể phát sinh :exc:`ValueError` khi cố gắng gán giá trị cho một header như vậy trong khi đã có một header cùng tên. Hành vi này là có chủ ý để đảm bảo tính nhất quán, nhưng đừng phụ thuộc vào nó vì trong tương lai, chúng tôi có thể chọn để những phép gán như vậy tự động xóa header hiện có.


   .. method:: __delitem__(name)

      Xóa mọi trường có tên *name* khỏi các header của thông điệp. Không phát sinh ngoại lệ nếu trường có tên đã chỉ định không tồn tại trong các header.


   .. method:: keys()

      Trả về danh sách tất cả tên trường header của thông điệp.


   .. method:: values()

      Trả về danh sách tất cả các giá trị trường của message.


   .. method:: items()

      Trả về danh sách các bộ 2-tuples chứa tất cả tiêu đề và giá trị trường của message.


   .. method:: get(name, failobj=None)

      Trả về giá trị của trường tiêu đề được đặt tên. Phương thức này giống hệt
      :meth:`~object.__getitem__` ngoại trừ việc *failobj* tùy chọn được trả về nếu không tìm thấy tiêu đề được đặt tên (*failobj* mặc định là ``None``).


   Dưới đây là một số phương thức hữu ích bổ sung liên quan đến tiêu đề:


   .. method:: get_all(name, failobj=None)

      Trả về danh sách tất cả các giá trị của trường có tên *name*. Nếu message không có tiêu đề nào mang tên đó, *failobj* sẽ được trả về (mặc định là ``None``).


   .. method:: add_header(_name, _value, **_params)

      Thiết lập tiêu đề mở rộng. Phương thức này tương tự như :meth:`__setitem__`, nhưng có thể cung cấp thêm các tham số tiêu đề dưới dạng đối số từ khóa. *_name* là trường tiêu đề cần thêm và *_value* là giá trị *primary* của tiêu đề.

      Với mỗi mục trong từ điển đối số từ khóa *_params*, khóa được lấy làm tên tham số, với dấu gạch dưới được chuyển thành dấu gạch ngang (vì dấu gạch ngang không hợp lệ trong các định danh Python). Thông thường, tham số sẽ được thêm dưới dạng ``key="value"``, trừ khi giá trị là ``None``, khi đó chỉ khóa được thêm vào.

      Nếu giá trị chứa các ký tự non-ASCII, bộ mã ký tự và ngôn ngữ có thể được điều khiển rõ ràng bằng cách chỉ định giá trị dưới dạng một tuple ba phần theo định dạng ``(CHARSET, LANGUAGE, VALUE)``, trong đó ``CHARSET`` là chuỗi chỉ định bộ mã ký tự được dùng để mã hóa giá trị, ``LANGUAGE`` thường có thể được đặt thành ``None`` hoặc chuỗi rỗng (xem :rfc:`2231` để biết các khả năng khác), còn ``VALUE`` là chuỗi giá trị chứa các code point non-ASCII. Nếu không truyền tuple ba phần và giá trị chứa các ký tự non-ASCII, giá trị sẽ tự động được mã hóa theo định dạng :rfc:`2231` bằng cách sử dụng ``CHARSET`` là ``utf-8`` và ``LANGUAGE`` là ``None``.

      Sau đây là một ví dụ::

         msg.add_header('Content-Disposition', 'attachment', filename='bud.gif')

      Thao tác này sẽ thêm một header có dạng::

         Content-Disposition: attachment; filename="bud.gif"

      Ví dụ về interface mở rộng với các ký tự non-ASCII::

         msg.add_header('Content-Disposition', 'attachment',
                        filename=('iso-8859-1', '', 'Fußballer.ppt'))


   .. method:: replace_header(_name, _value)

      Thay thế một header. Thay thế header đầu tiên được tìm thấy trong message khớp với *_name*, đồng thời giữ nguyên thứ tự header và kiểu chữ của tên trường trong header ban đầu. Nếu không tìm thấy header phù hợp, hãy raise a
      :exc:`KeyError`.


   .. method:: get_content_type()

      Trả về content type của message, được chuyển thành chữ thường theo dạng
      :mimetype:`maintype/subtype`.  Nếu không có tiêu đề :mailheader:`Content-Type` trong thông điệp, hãy trả về giá trị do
      :meth:`get_default_type`.  Nếu tiêu đề :mailheader:`Content-Type` không hợp lệ, hãy trả về ``text/plain``.

      (Theo :rfc:`2045`, thông điệp luôn có một kiểu mặc định,
      :meth:`get_content_type` sẽ luôn trả về một giá trị.  :rfc:`2045` xác định kiểu mặc định của thông điệp là :mimetype:`text/plain`, trừ khi thông điệp xuất hiện bên trong một vùng chứa :mimetype:`multipart/digest`, trong trường hợp đó kiểu mặc định sẽ là :mimetype:`message/rfc822`.  Nếu tiêu đề :mailheader:`Content-Type` có đặc tả kiểu không hợp lệ, :rfc:`2045` yêu cầu kiểu mặc định phải là :mimetype:`text/plain`.)


   .. method:: get_content_maintype()

      Trả về kiểu nội dung chính của thông điệp.  Đây là phần :mimetype:`maintype` của chuỗi được :meth:`get_content_type` trả về.


   .. method:: get_content_subtype()

      Trả về kiểu nội dung phụ của thông điệp.  Đây là phần :mimetype:`subtype` của chuỗi được :meth:`get_content_type` trả về.


   .. method:: get_default_type()

      Trả về kiểu nội dung mặc định.  Hầu hết thông điệp có kiểu nội dung mặc định là :mimetype:`text/plain`, ngoại trừ các thông điệp là phần con của
      :mimetype:`multipart/digest` các vùng chứa. Những phần con như vậy có kiểu nội dung mặc định là :mimetype:`message/rfc822`.


   .. method:: set_default_type(ctype)

      Đặt kiểu nội dung mặc định. *ctype* phải là một trong các giá trị sau:
      :mimetype:`text/plain` hoặc :mimetype:`message/rfc822`, mặc dù điều này không được thực thi. Kiểu nội dung mặc định không được lưu trong
      :mailheader:`Content-Type` header, vì vậy nó chỉ ảnh hưởng đến giá trị trả về của các phương thức ``get_content_type`` khi không có header :mailheader:`Content-Type` trong message.


   .. method:: set_param(param, value, header='Content-Type', requote=True, \
                         charset=None, language='', replace=False)

      Đặt một tham số trong header :mailheader:`Content-Type`. Nếu tham số đó đã tồn tại trong header, thay thế giá trị của nó bằng *value*. Khi *header* là ``Content-Type`` (mặc định) và header chưa tồn tại trong message, hãy thêm header đó, đặt giá trị của nó thành
      :mimetype:`text/plain`, rồi nối thêm giá trị tham số mới. *header* tùy chọn chỉ định một header thay thế cho :mailheader:`Content-Type`.

      Nếu giá trị chứa các ký tự non-ASCII, có thể chỉ định rõ charset và language bằng các tham số tùy chọn *charset* và *language*. Tham số *language* tùy chọn chỉ định :rfc:`2231` language, mặc định là chuỗi rỗng. Cả *charset* và *language* đều phải là chuỗi. Mặc định là sử dụng ``utf8`` *charset* và ``None`` cho *language*.

      Nếu *replace* là ``False`` (mặc định), header sẽ được chuyển đến cuối danh sách các header. Nếu *replace* là ``True``, header sẽ được cập nhật tại chỗ.

      Việc sử dụng tham số *requote* với các đối tượng :class:`EmailMessage` không còn được khuyến nghị.

      Lưu ý rằng có thể truy cập các giá trị tham số hiện có của header thông qua thuộc tính :attr:`~email.headerregistry.ParameterizedMIMEHeader.params` của giá trị header (ví dụ: ``msg['Content-Type'].params['charset']``).

      .. versionchanged:: 3.4 Từ khóa ``replace`` đã được thêm.


   .. method:: del_param(param, header='content-type', requote=True)

      Xóa hoàn toàn tham số đã cho khỏi header :mailheader:`Content-Type`. Header sẽ được viết lại tại chỗ mà không có tham số hoặc giá trị của nó. *header* tùy chọn chỉ định một lựa chọn thay thế cho
      :mailheader:`Content-Type`.

      Việc sử dụng tham số *requote* với các đối tượng :class:`EmailMessage` không còn được khuyến nghị.


   .. method:: get_filename(failobj=None)

      Trả về giá trị của tham số ``filename`` của
      header :mailheader:`Content-Disposition` của thư. Nếu header không có tham số ``filename``, phương thức này sẽ chuyển sang tìm tham số ``name`` trong header :mailheader:`Content-Type`. Nếu không tìm thấy cả hai tham số, hoặc header bị thiếu, thì *failobj* được trả về. Chuỗi được trả về luôn không có dấu ngoặc kép theo
      :func:`email.utils.unquote`.


   .. method:: get_boundary(failobj=None)

      Trả về giá trị của tham số ``boundary`` của
      header :mailheader:`Content-Type` của thư, hoặc *failobj* nếu header bị thiếu hoặc không có tham số ``boundary``. Chuỗi được trả về luôn không có dấu ngoặc kép theo :func:`email.utils.unquote`.


   .. method:: set_boundary(boundary)

      Đặt tham số ``boundary`` của header :mailheader:`Content-Type` thành *boundary*. :meth:`set_boundary` sẽ luôn đặt *boundary* trong dấu ngoặc kép nếu cần. Một :exc:`~email.errors.HeaderParseError` sẽ được phát sinh nếu đối tượng thư không có header :mailheader:`Content-Type`.

      Lưu ý rằng việc sử dụng phương thức này hơi khác so với việc xóa
      header :mailheader:`Content-Type` cũ rồi thêm một header mới với boundary mới thông qua :meth:`add_header`, vì :meth:`set_boundary` giữ nguyên thứ tự của header :mailheader:`Content-Type` trong danh sách các header.


   .. method:: get_content_charset(failobj=None)

      Trả về tham số ``charset`` của tiêu đề :mailheader:`Content-Type`, được chuyển thành chữ thường. Nếu không có tiêu đề :mailheader:`Content-Type`, hoặc tiêu đề đó không có tham số ``charset``, *failobj* sẽ được trả về.


   .. method:: get_charsets(failobj=None)

      Trả về một danh sách chứa tên các bộ ký tự trong message. Nếu message là một :mimetype:`multipart`, danh sách sẽ chứa một phần tử cho mỗi phân phần trong payload; nếu không, danh sách sẽ có độ dài 1.

      Mỗi phần tử trong danh sách sẽ là một chuỗi, tương ứng với giá trị của tham số ``charset`` trong tiêu đề :mailheader:`Content-Type` của phân phần được biểu diễn. Nếu phân phần không có tiêu đề :mailheader:`Content-Type`, không có tham số ``charset``, hoặc không thuộc kiểu MIME chính :mimetype:`text`, thì phần tử tương ứng trong danh sách trả về sẽ là *failobj*.


   .. method:: is_attachment

      Trả về ``True`` nếu có tiêu đề :mailheader:`Content-Disposition` và giá trị của tiêu đề đó (không phân biệt chữ hoa chữ thường) là ``attachment``, nếu không thì trả về ``False``.

      .. versionchanged:: 3.4.2
         is_attachment hiện là một method thay vì một property, để nhất quán với :meth:`~email.message.Message.is_multipart`.


   .. method:: get_content_disposition()

      Trả về giá trị viết thường (không kèm tham số) của message's
      tiêu đề :mailheader:`Content-Disposition` nếu có, hoặc ``None``. Các giá trị có thể có của method này là *inline*, *attachment* hoặc ``None`` nếu message tuân theo :rfc:`2183`.

      .. versionadded:: 3.5


   Các phương thức sau đây liên quan đến việc truy vấn và thao tác với nội dung (payload) của message.


   .. method:: walk()

      Phương thức :meth:`walk` là một generator đa dụng có thể được dùng để lặp qua tất cả các phần và phần con của cây đối tượng message theo thứ tự duyệt depth-first. Thông thường, bạn sẽ dùng :meth:`walk` làm iterator trong vòng lặp ``for``; mỗi lần lặp trả về phần con tiếp theo.

      Sau đây là một ví dụ in ra MIME type của mọi phần trong một cấu trúc message multipart:

      .. testsetup::

         from email import message_from_binary_file
         with open('../Lib/test/test_email/data/msg_16.txt', 'rb') as f:
             msg = message_from_binary_file(f)

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

      ``walk`` lặp qua các phần con của bất kỳ phần nào mà
      :meth:`is_multipart` trả về ``True``, mặc dù ``msg.get_content_maintype() == 'multipart'`` có thể trả về ``False``. Chúng ta có thể thấy điều này trong ví dụ bằng cách sử dụng hàm trợ giúp debug ``_structure``:

      .. doctest::

         >>> from email.iterators import _structure
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


   .. method:: get_body(preferencelist=('related', 'html', 'plain'))

      Trả về phần MIME có khả năng cao nhất là "body" của message.

      *preferencelist* phải là một dãy các chuỗi thuộc tập hợp ``related``, ``html`` và ``plain``, đồng thời cho biết thứ tự ưu tiên của kiểu nội dung của phần được trả về.

      Bắt đầu tìm các kết quả khớp tiềm năng với đối tượng mà phương thức ``get_body`` được gọi trên đó.

      Nếu ``related`` không được đưa vào *preferencelist*, hãy xem phần gốc (hoặc phần con của phần gốc) của bất kỳ phần liên quan nào được gặp như một kết quả khớp tiềm năng nếu phần đó khớp với một tùy chọn ưu tiên.

      Khi gặp một ``multipart/related``, hãy kiểm tra tham số ``start`` và nếu tìm thấy một phần có :mailheader:`Content-ID` khớp, chỉ xem xét phần đó khi tìm các kết quả khớp tiềm năng. Nếu không, chỉ xem xét phần đầu tiên (phần gốc mặc định) của ``multipart/related``.

      Nếu một phần có tiêu đề :mailheader:`Content-Disposition`, chỉ xem phần đó là một kết quả khớp tiềm năng nếu giá trị của tiêu đề là ``inline``.

      Nếu không có ứng viên nào khớp với bất kỳ tùy chọn ưu tiên nào trong *preferencelist*, hãy trả về ``None``.

      Lưu ý: (1) Đối với hầu hết các ứng dụng, các tổ hợp *preferencelist* duy nhất thực sự hợp lý là ``('plain',)``, ``('html', 'plain')`` và ``('related', 'html', 'plain')`` mặc định. (2) Vì việc khớp bắt đầu với đối tượng mà ``get_body`` được gọi trên đó, việc gọi ``get_body`` trên một ``multipart/related`` sẽ trả về chính đối tượng đó, trừ khi *preferencelist* có giá trị khác mặc định. (3) Các message (hoặc phần message) không chỉ định :mailheader:`Content-Type` hoặc có
      Tiêu đề :mailheader:`Content-Type` không hợp lệ sẽ được xử lý như thể thuộc kiểu ``text/plain``, điều này đôi khi có thể khiến ``get_body`` trả về kết quả không như mong đợi.


   .. method:: iter_attachments()

      Trả về một iterator chứa tất cả các phần con trực tiếp của message không phải là các phần ứng viên cho "body". Nghĩa là, bỏ qua lần xuất hiện đầu tiên của mỗi ``text/plain``, ``text/html``, ``multipart/related`` hoặc ``multipart/alternative`` (trừ khi chúng được đánh dấu rõ ràng là tệp đính kèm thông qua :mailheader:`Content-Disposition: attachment`), rồi trả về tất cả các phần còn lại. Khi được áp dụng trực tiếp cho một ``multipart/related``, trả về một iterator chứa tất cả các phần liên quan ngoại trừ phần gốc (tức là phần được tham chiếu bởi tham số ``start``, hoặc phần đầu tiên nếu không có tham số ``start`` hoặc tham số ``start`` không khớp với :mailheader:`Content-ID` của bất kỳ phần nào). Khi được áp dụng trực tiếp cho một ``multipart/alternative`` hoặc một đối tượng không phải ``multipart``, trả về một iterator rỗng.


   .. method:: iter_parts()

      Trả về một iterator chứa tất cả các phần con trực tiếp của message; iterator này sẽ rỗng đối với một đối tượng không phải ``multipart``. (Xem thêm
      :meth:`~email.message.EmailMessage.walk`.)


   .. method:: get_content(*args, content_manager=None, **kw)

      Gọi phương thức :meth:`~email.contentmanager.ContentManager.get_content` của *content_manager*, truyền self làm đối tượng message và truyền mọi đối số hoặc từ khóa khác dưới dạng các đối số bổ sung. Nếu *content_manager* không được chỉ định, hãy sử dụng ``content_manager`` được chỉ định bởi :mod:`~email.policy` hiện tại.


   .. method:: set_content(*args, content_manager=None, **kw)

      Gọi phương thức :meth:`~email.contentmanager.ContentManager.set_content` của *content_manager*, truyền self làm đối tượng message và truyền mọi đối số hoặc từ khóa khác dưới dạng các đối số bổ sung. Nếu *content_manager* không được chỉ định, hãy sử dụng ``content_manager`` được chỉ định bởi :mod:`~email.policy` hiện tại.


   .. method:: make_related(boundary=None)

      Chuyển đổi một message không phải ``multipart`` thành một message ``multipart/related``, chuyển mọi header và payload :mailheader:`Content-` hiện có vào một phần đầu tiên (mới) của ``multipart``. Nếu *boundary* được chỉ định, hãy sử dụng nó làm chuỗi boundary trong multipart; nếu không, để boundary được tự động tạo khi cần (ví dụ: khi message được serialize).


   .. method:: make_alternative(boundary=None)

      Chuyển đổi một đối tượng không phải ``multipart`` hoặc một ``multipart/related`` thành một ``multipart/alternative``, chuyển mọi header và payload :mailheader:`Content-` hiện có vào một phần đầu tiên (mới) của ``multipart``. Nếu *boundary* được chỉ định, hãy sử dụng nó làm chuỗi boundary trong multipart; nếu không, để boundary được tự động tạo khi cần (ví dụ: khi message được serialize).


   .. method:: make_mixed(boundary=None)

      Chuyển đổi một ``multipart`` không phải loại ..., một ``multipart/related``, hoặc một ``multipart-alternative`` thành một ``multipart/mixed``, đồng thời chuyển mọi
      header và payload :mailheader:`Content-` hiện có vào phần đầu tiên (mới) của ``multipart``. Nếu *boundary* được chỉ định, hãy sử dụng nó làm chuỗi boundary trong multipart; nếu không, để boundary được tự động tạo khi cần (ví dụ: khi message được serialize).


   .. method:: add_related(*args, content_manager=None, **kw)

      Nếu message là một ``multipart/related``, hãy tạo một đối tượng message mới, truyền tất cả đối số vào phương thức :meth:`set_content` của nó, rồi :meth:`~email.message.Message.attach` nó vào ``multipart``. Nếu message không phải là một ``multipart``, hãy gọi :meth:`make_related`, rồi tiếp tục như trên. Nếu message thuộc bất kỳ kiểu ``multipart`` nào khác, hãy raise một :exc:`TypeError`. Nếu *content_manager* không được chỉ định, hãy sử dụng ``content_manager`` được chỉ định bởi :mod:`~email.policy` hiện tại. Nếu phần được thêm không có header :mailheader:`Content-Disposition`, hãy thêm một header với giá trị ``inline``.


   .. method:: add_alternative(*args, content_manager=None, **kw)

      Nếu message là một ``multipart/alternative``, hãy tạo một đối tượng message mới, truyền tất cả đối số vào phương thức :meth:`set_content` của nó, rồi
      :meth:`~email.message.Message.attach` nó vào ``multipart``. Nếu message không phải là một ``multipart`` hoặc ``multipart/related``, hãy gọi
      :meth:`make_alternative`, rồi tiếp tục như trên. Nếu message thuộc bất kỳ kiểu ``multipart`` nào khác, hãy raise một :exc:`TypeError`. Nếu *content_manager* không được chỉ định, hãy sử dụng ``content_manager`` được chỉ định bởi :mod:`~email.policy` hiện tại.


   .. method:: add_attachment(*args, content_manager=None, **kw)

      Nếu message là một ``multipart/mixed``, hãy tạo một đối tượng message mới, truyền tất cả đối số vào phương thức :meth:`set_content` của nó, rồi
      :meth:`~email.message.Message.attach` nó vào ``multipart``.  Nếu thông điệp không phải ``multipart``, ``multipart/related`` hoặc ``multipart/alternative``, hãy gọi :meth:`make_mixed` rồi tiếp tục như trên. Nếu *content_manager* không được chỉ định, hãy sử dụng ``content_manager`` được chỉ định bởi :mod:`~email.policy` hiện tại. Nếu phần được thêm không có header :mailheader:`Content-Disposition`, hãy thêm một header với giá trị ``attachment``. Phương thức này có thể được sử dụng cho cả tệp đính kèm tường minh (:mailheader:`Content-Disposition: attachment`) và tệp đính kèm ``inline`` (:mailheader:`Content-Disposition: inline`), bằng cách truyền các tùy chọn thích hợp cho ``content_manager``.


   .. method:: clear()

      Xóa payload và tất cả các header.


   .. method:: clear_content()

      Xóa payload và tất cả các header :mailheader:`!Content-`, giữ nguyên mọi header khác theo đúng thứ tự ban đầu.


   Các đối tượng :class:`EmailMessage` có những thuộc tính instance sau:


   .. attribute:: preamble

      Định dạng của tài liệu MIME cho phép có một phần văn bản nằm giữa dòng trống sau các header và chuỗi boundary multipart đầu tiên. Thông thường, phần văn bản này không bao giờ hiển thị trong trình đọc thư có hỗ trợ MIME vì nó nằm ngoài phần bao bọc MIME tiêu chuẩn. Tuy nhiên, khi xem văn bản thô của thông điệp hoặc xem thông điệp trong trình đọc không hỗ trợ MIME, phần văn bản này có thể hiển thị.

      Thuộc tính *preamble* chứa phần văn bản bổ sung nằm ở đầu, bên ngoài phần bao bọc, của các tài liệu MIME. Khi :class:`~email.parser.Parser` phát hiện một phần văn bản sau các header nhưng trước chuỗi boundary đầu tiên, nó gán phần văn bản này cho thuộc tính *preamble* của thông điệp. Khi
      :class:`~email.generator.Generator` đang ghi biểu diễn văn bản thuần túy của một thông điệp MIME và phát hiện thông điệp có thuộc tính *preamble*, nó sẽ ghi phần văn bản này vào khu vực giữa các header và boundary đầu tiên. Xem :mod:`email.parser` và
      :mod:`email.generator` để biết thêm chi tiết.

      Lưu ý rằng nếu đối tượng message không có phần mở đầu, thuộc tính *preamble* sẽ là ``None``.


   .. attribute:: epilogue

      Thuộc tính *epilogue* hoạt động giống như thuộc tính *preamble*, ngoại trừ việc nó chứa văn bản xuất hiện giữa boundary cuối cùng và phần cuối của message. Cũng như với :attr:`~EmailMessage.preamble`, nếu không có văn bản kết thúc thì thuộc tính này sẽ là ``None``.


   .. attribute:: defects

      Thuộc tính *defects* chứa danh sách tất cả các vấn đề được phát hiện khi phân tích message này. Xem :mod:`email.errors` để biết mô tả chi tiết về các lỗi phân tích có thể xảy ra.


.. class:: MIMEPart(policy=default)

    Lớp này biểu diễn một subpart của message MIME. Nó giống hệt
    :class:`EmailMessage`, ngoại trừ việc không có header :mailheader:`MIME-Version` nào được thêm khi gọi :meth:`~EmailMessage.set_content`, vì các subpart không cần header :mailheader:`MIME-Version` riêng.


.. rubric:: Chú thích

.. [1] Được bổ sung lần đầu trong 3.4 dưới dạng một :term:`mô-đun tạm thời <provisional package>`. Tài liệu về lớp message cũ đã được chuyển đến
       :ref:`compat32_message`.

.. [2] Lớp :class:`EmailMessage` yêu cầu một policy cung cấp thuộc tính ``content_manager`` để các phương thức quản lý nội dung như ``set_content()`` và ``get_content()`` hoạt động. Lớp legacy
       Policy :const:`~email.policy.compat32` không hỗ trợ các phương thức này và không nên được sử dụng với :class:`EmailMessage`.
