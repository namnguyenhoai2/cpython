:mod:`!email.generator`: Tạo tài liệu MIME
------------------------------------------

.. module:: email.generator
   :synopsis: Tạo các thư email dạng văn bản phẳng từ cấu trúc thư.

**Mã nguồn:** :source:`Lib/email/generator.py`

--------------

Một trong những tác vụ phổ biến nhất là tạo phiên bản phẳng (đã tuần tự hóa) của thư email được biểu diễn bằng cấu trúc đối tượng thư. Bạn cần thực hiện việc này nếu muốn gửi thư qua :meth:`smtplib.SMTP.sendmail` hoặc in thư ra console. Việc nhận một cấu trúc đối tượng thư và tạo ra biểu diễn đã tuần tự hóa là nhiệm vụ của các lớp generator.

Cũng như module :mod:`email.parser`, bạn không bị giới hạn ở chức năng của generator đi kèm; bạn có thể tự viết một generator từ đầu. Tuy nhiên, generator đi kèm biết cách tạo hầu hết email theo cách tuân thủ tiêu chuẩn, xử lý tốt cả thư email MIME và không phải MIME, đồng thời được thiết kế để các thao tác phân tích cú pháp và tạo dữ liệu theo hướng byte là nghịch đảo của nhau, với điều kiện sử dụng cùng một :mod:`~email.policy` không biến đổi cho cả hai. Nghĩa là, việc phân tích cú pháp luồng byte đã tuần tự hóa thông qua
:class:`~email.parser.BytesParser` class rồi tạo lại luồng byte đã tuần tự hóa bằng :class:`BytesGenerator` sẽ cho ra kết quả giống hệt đầu vào [#]_. (Mặt khác, việc sử dụng generator trên một
:class:`~email.message.EmailMessage` được tạo bằng chương trình có thể dẫn đến thay đổi đối tượng :class:`~email.message.EmailMessage` khi các giá trị mặc định được điền vào.)

Lớp :class:`Generator` có thể được dùng để làm phẳng một message thành dạng biểu diễn được serialize dưới dạng văn bản (thay vì nhị phân), nhưng vì Unicode không thể biểu diễn trực tiếp dữ liệu nhị phân nên message nhất thiết được chuyển đổi thành dạng chỉ chứa các ký tự ASCII, bằng cách sử dụng các kỹ thuật RFC Content Transfer Encoding tiêu chuẩn của email để mã hóa message email khi truyền qua các kênh không "8 bit clean".

Để hỗ trợ việc xử lý có thể tái lập đối với các message được ký bằng SMIME
:class:`Generator` vô hiệu hóa việc gấp tiêu đề (header folding) cho các phần của message thuộc kiểu ``multipart/signed`` và tất cả các phần con.


.. class:: BytesGenerator(outfp, mangle_from_=None, maxheaderlen=None, *, \
                          policy=None)

   Trả về một đối tượng :class:`BytesGenerator` ghi mọi message được cung cấp cho phương thức :meth:`flatten`, hoặc mọi văn bản được mã hóa bằng surrogateescape được cung cấp cho phương thức :meth:`write`, vào :term:`file-like object` *outfp*. *outfp* phải hỗ trợ phương thức ``write`` chấp nhận dữ liệu nhị phân.

   Nếu *mangle_from_* tùy chọn là ``True``, hãy thêm một ký tự ``>`` vào trước mọi dòng trong phần thân bắt đầu bằng chuỗi chính xác ``"From "``, tức là ``From`` theo sau bởi một khoảng trắng ở đầu dòng.  *mangle_from_* mặc định nhận giá trị từ thiết lập :attr:`~email.policy.Policy.mangle_from_` của *policy* (là ``True`` đối với
   chính sách :data:`~email.policy.compat32` và ``False`` đối với tất cả các chính sách khác). *mangle_from_* được dùng khi message được lưu ở định dạng Unix mbox (xem :mod:`mailbox` và `WHY THE CONTENT-LENGTH FORMAT IS BAD <https://www.jwz.org/doc/content-length.html>`_).

   Nếu *maxheaderlen* không phải là ``None``, sẽ định dạng lại các dòng tiêu đề dài hơn *maxheaderlen*; còn nếu là ``0``, sẽ không bọc lại bất kỳ tiêu đề nào. Nếu *manheaderlen* là ``None`` (mặc định), các tiêu đề và những dòng thư khác sẽ được bọc theo các thiết lập *policy*.

   Nếu *policy* được chỉ định, hãy sử dụng policy đó để kiểm soát việc tạo thư. Nếu *policy* là ``None`` (mặc định), hãy sử dụng policy được liên kết với
   đối tượng :class:`~email.message.Message` hoặc :class:`~email.message.EmailMessage` được truyền vào ``flatten`` để kiểm soát việc tạo thư. Xem
   :mod:`email.policy` để biết chi tiết về những gì *policy* kiểm soát.

   .. versionadded:: 3.2

   .. versionchanged:: 3.3 Đã thêm từ khóa *policy*.

   .. versionchanged:: 3.6 Hành vi mặc định của *mangle_from_*
      và các tham số *maxheaderlen* là tuân theo policy.


   .. method:: flatten(msg, unixfrom=False, linesep=None)

      In biểu diễn dạng văn bản của cấu trúc đối tượng message bắt nguồn từ *msg* vào tệp đầu ra được chỉ định khi instance :class:`BytesGenerator` được tạo.

      Nếu tùy chọn :mod:`~email.policy` :attr:`~email.policy.Policy.cte_type` là ``8bit`` (mặc định), sao chép mọi header trong message gốc đã được phân tích mà chưa bị sửa đổi vào đầu ra, với mọi byte có bit cao được tái tạo như trong bản gốc, đồng thời giữ lại phần không phải ASCII
      :mailheader:`Content-Transfer-Encoding` của mọi body part có chúng. Nếu ``cte_type`` là ``7bit``, chuyển đổi các byte có bit cao khi cần bằng cách sử dụng :mailheader:`Content-Transfer-Encoding` tương thích ASCII. Nghĩa là chuyển đổi các part có :mailheader:`Content-Transfer-Encoding` không phải ASCII
      :mailheader:`Content-Transfer-Encoding` (:mailheader:`Content-Transfer-Encoding: 8bit`) thành dạng tương thích ASCII
      :mailheader:`Content-Transfer-Encoding`, và mã hóa các byte không phải ASCII không hợp lệ theo RFC trong header bằng bộ ký tự MIME ``unknown-8bit``, nhờ đó làm cho chúng tuân thủ RFC.

      .. XXX: There should be an option that just does the RFC
         compliance transformation on headers but leaves CTE 8bit parts alone.

      Nếu *unixfrom* là ``True``, in dấu phân cách header phong bì được định dạng Unix mailbox sử dụng (xem :mod:`mailbox`) trước header đầu tiên trong số các
      :rfc:`5322` header của đối tượng message gốc. Nếu đối tượng gốc không có header phong bì, hãy tạo một header tiêu chuẩn. Mặc định là ``False``. Lưu ý rằng đối với các subpart, không bao giờ in header phong bì.

      Nếu *linesep* không phải là ``None``, hãy dùng nó làm ký tự phân cách giữa tất cả các dòng của thông điệp đã được làm phẳng. Nếu *linesep* là ``None`` (mặc định), hãy dùng giá trị được chỉ định trong *policy*.

      .. XXX: flatten should take a *policy* keyword.


   .. method:: clone(fp)

      Trả về một bản sao độc lập của thực thể :class:`BytesGenerator` này với chính xác cùng các tùy chọn, và *fp* làm *outfp* mới.


   .. method:: write(s)

      Mã hóa *s* bằng ``ASCII`` codec và ``surrogateescape`` error handler, rồi truyền nó cho phương thức *write* của *outfp* được truyền cho
      hàm khởi tạo của :class:`BytesGenerator`.


Để thuận tiện, :class:`~email.message.EmailMessage` cung cấp các phương thức
:meth:`~email.message.EmailMessage.as_bytes` và ``bytes(aMessage)`` (còn được gọi là
:meth:`~email.message.EmailMessage.__bytes__`), giúp đơn giản hóa việc tạo biểu diễn nhị phân đã tuần tự hóa của một đối tượng thông điệp. Để biết thêm chi tiết, hãy xem
:mod:`email.message`.


Vì chuỗi không thể biểu diễn dữ liệu nhị phân, lớp :class:`Generator` phải chuyển đổi mọi dữ liệu nhị phân trong bất kỳ message nào mà nó flatten sang một định dạng tương thích với ASCII, bằng cách chuyển đổi chúng sang một định dạng tương thích với ASCII
:mailheader:`Content-Transfer_Encoding`. Theo thuật ngữ của các RFC về email, bạn có thể hình dung đây là :class:`Generator` serialize vào một I/O stream không "8 bit clean". Nói cách khác, hầu hết các ứng dụng sẽ muốn sử dụng :class:`BytesGenerator`, chứ không phải :class:`Generator`.

.. class:: Generator(outfp, mangle_from_=None, maxheaderlen=None, *, \
                     policy=None)

   Trả về một đối tượng :class:`Generator` sẽ ghi mọi message được cung cấp cho phương thức :meth:`flatten`, hoặc mọi văn bản được cung cấp cho phương thức :meth:`write`, vào :term:`file-like object` *outfp*. *outfp* phải hỗ trợ một phương thức ``write`` chấp nhận dữ liệu chuỗi.

   Nếu *mangle_from_* tùy chọn là ``True``, hãy thêm một ký tự ``>`` vào trước mọi dòng trong phần thân bắt đầu bằng chuỗi chính xác ``"From "``, tức là ``From`` theo sau bởi một khoảng trắng ở đầu dòng.  *mangle_from_* mặc định nhận giá trị từ thiết lập :attr:`~email.policy.Policy.mangle_from_` của *policy* (là ``True`` đối với
   chính sách :data:`~email.policy.compat32` và ``False`` đối với tất cả các chính sách khác). *mangle_from_* được dùng khi message được lưu ở định dạng Unix mbox (xem :mod:`mailbox` và `WHY THE CONTENT-LENGTH FORMAT IS BAD <https://www.jwz.org/doc/content-length.html>`_).

   Nếu *maxheaderlen* không phải là ``None``, sẽ định dạng lại các dòng tiêu đề dài hơn *maxheaderlen*; còn nếu là ``0``, sẽ không bọc lại bất kỳ tiêu đề nào. Nếu *manheaderlen* là ``None`` (mặc định), các tiêu đề và những dòng thư khác sẽ được bọc theo các thiết lập *policy*.

   Nếu *policy* được chỉ định, hãy sử dụng policy đó để kiểm soát việc tạo thư. Nếu *policy* là ``None`` (mặc định), hãy sử dụng policy được liên kết với
   đối tượng :class:`~email.message.Message` hoặc :class:`~email.message.EmailMessage` được truyền vào ``flatten`` để kiểm soát việc tạo thư. Xem
   :mod:`email.policy` để biết chi tiết về những gì *policy* kiểm soát.

   .. versionchanged:: 3.3 Đã thêm từ khóa *policy*.

   .. versionchanged:: 3.6 Hành vi mặc định của *mangle_from_*
      và các tham số *maxheaderlen* là tuân theo policy.


   .. method:: flatten(msg, unixfrom=False, linesep=None)

      In biểu diễn dạng văn bản của cấu trúc đối tượng thông điệp bắt nguồn từ *msg* vào tệp đầu ra được chỉ định khi thực thể :class:`Generator` được tạo.

      Nếu tùy chọn :mod:`~email.policy` :attr:`~email.policy.Policy.cte_type` là ``8bit``, hãy tạo thông báo như thể tùy chọn này được đặt thành ``7bit``. (Điều này là bắt buộc vì chuỗi không thể biểu diễn các byte không phải ASCII.) Chuyển đổi mọi byte có bit cao được thiết lập khi cần bằng cách sử dụng một :mailheader:`Content-Transfer-Encoding` tương thích với ASCII. Nghĩa là, biến đổi các phần có :mailheader:`Content-Transfer-Encoding` không phải ASCII (:mailheader:`Content-Transfer-Encoding: 8bit`) thành một dạng tương thích với ASCII
      :mailheader:`Content-Transfer-Encoding`, và mã hóa các byte không phải ASCII không hợp lệ theo RFC trong header bằng bộ ký tự MIME ``unknown-8bit``, nhờ đó làm cho chúng tuân thủ RFC.

      Nếu *unixfrom* là ``True``, in dấu phân cách header phong bì được định dạng Unix mailbox sử dụng (xem :mod:`mailbox`) trước header đầu tiên trong số các
      :rfc:`5322` header của đối tượng message gốc. Nếu đối tượng gốc không có header phong bì, hãy tạo một header tiêu chuẩn. Mặc định là ``False``. Lưu ý rằng đối với các subpart, không bao giờ in header phong bì.

      Nếu *linesep* không phải là ``None``, hãy dùng nó làm ký tự phân cách giữa tất cả các dòng của thông điệp đã được làm phẳng. Nếu *linesep* là ``None`` (mặc định), hãy dùng giá trị được chỉ định trong *policy*.

      .. XXX: flatten should take a *policy* keyword.

      .. versionchanged:: 3.2
         Đã bổ sung hỗ trợ mã hóa lại nội dung thông báo ``8bit`` và đối số *linesep*.


   .. method:: clone(fp)

      Trả về một bản sao độc lập của thực thể :class:`Generator` này với các tùy chọn hoàn toàn giống nhau và *fp* làm *outfp* mới.


   .. method:: write(s)

      Ghi *s* vào phương thức *write* của *outfp* được truyền cho
      :class:`Generator`'s constructor. Điều này cung cấp API dạng tệp vừa đủ để các thực thể :class:`Generator` có thể được sử dụng trong hàm :func:`print`.


Để thuận tiện, :class:`~email.message.EmailMessage` cung cấp các phương thức
:meth:`~email.message.EmailMessage.as_string` và ``str(aMessage)`` (còn được gọi là
:meth:`~email.message.EmailMessage.__str__`), giúp đơn giản hóa việc tạo biểu diễn chuỗi đã định dạng của một đối tượng message. Để biết thêm chi tiết, hãy xem
:mod:`email.message`.


Mô-đun :mod:`!email.generator` cũng cung cấp một lớp dẫn xuất,
:class:`DecodedGenerator`, tương tự như lớp cơ sở :class:`Generator`, ngoại trừ việc các phần không phải \ :mimetype:`text` không được tuần tự hóa mà thay vào đó được biểu diễn trong output stream bằng một chuỗi được tạo từ template, điền thông tin về phần đó.

.. class:: DecodedGenerator(outfp, mangle_from_=None, maxheaderlen=None, \
                            fmt=None, *, policy=None)

   Hoạt động giống như :class:`Generator`, ngoại trừ việc đối với bất kỳ phần con nào của thông điệp được truyền cho :meth:`Generator.flatten`, nếu phần con đó có kiểu chính là
   :mimetype:`text`, hãy in payload đã giải mã của phần con đó; nếu kiểu chính không phải là :mimetype:`text`, thay vì in nó, hãy điền thông tin từ phần đó vào chuỗi *fmt* rồi in chuỗi đã được điền.

   Để điền vào *fmt*, hãy thực thi ``fmt % part_info``, trong đó ``part_info`` là một dictionary gồm các khóa và giá trị sau:

   * ``type`` -- Kiểu MIME đầy đủ của phần không phải \ :mimetype:`text`

   * ``maintype`` -- Kiểu MIME chính của phần không phải \ :mimetype:`text`

   * ``subtype`` -- Kiểu MIME phụ của phần không phải \ :mimetype:`text`

   * ``filename`` -- Tên tệp của phần không phải \ :mimetype:`text`

   * ``description`` -- Mô tả liên kết với phần không phải \ :mimetype:`text`

   * ``encoding`` -- Mã hóa truyền nội dung của phần không phải \ :mimetype:`text`

   Nếu *fmt* là ``None``, hãy sử dụng *fmt* mặc định sau đây:

      "[Đã bỏ qua phần không phải văn bản (%(type)s) của thư, tên tệp %(filename)s]"

   *_mangle_from_* và *maxheaderlen* tùy chọn được xử lý giống như trong
   lớp cơ sở :class:`Generator`.


.. rubric:: Chú thích cuối trang

.. [#] Câu lệnh này giả định rằng bạn sử dụng thiết lập thích hợp cho ``unixfrom``, và không có thiết lập :mod:`email.policy` nào yêu cầu điều chỉnh tự động (ví dụ như,
       :attr:`~email.policy.EmailPolicy.refold_source` phải là ``none``, vốn *không* phải là mặc định). Điều này cũng không hoàn toàn đúng 100%, vì nếu thông điệp không tuân theo các tiêu chuẩn RFC thì đôi khi thông tin về chính xác văn bản gốc sẽ bị mất trong quá trình khôi phục sau lỗi phân tích cú pháp. Mục tiêu là khắc phục các trường hợp biên này khi có thể.

.. _`WHY THE CONTENT-LENGTH FORMAT IS BAD`: https://www.jwz.org/doc/content-length.html
