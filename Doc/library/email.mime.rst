:mod:`!email.mime`: Tạo các đối tượng email và MIME từ đầu
----------------------------------------------------------

.. module:: email.mime
   :synopsis: Xây dựng các message MIME.

**Mã nguồn:** :source:`Lib/email/mime/`

--------------

Mô-đun này thuộc API email cũ (``Compat32``). Chức năng của nó được thay thế một phần bởi :mod:`~email.contentmanager` trong API mới, nhưng trong một số ứng dụng, các lớp này vẫn có thể hữu ích, ngay cả trong mã không còn dùng API cũ.

Thông thường, bạn có được một cấu trúc đối tượng message bằng cách truyền một tệp hoặc một đoạn văn bản cho parser, trình này phân tích văn bản và trả về đối tượng message gốc. Tuy nhiên, bạn cũng có thể xây dựng toàn bộ cấu trúc message từ đầu, hoặc thậm chí từng
:class:`~email.message.Message` các đối tượng bằng tay. Trên thực tế, bạn cũng có thể lấy một cấu trúc hiện có và thêm các :class:`~email.message.Message` đối tượng mới, di chuyển chúng, v.v. Điều này tạo ra một giao diện rất thuận tiện để cắt và phân tách các thông điệp MIME.

Bạn có thể tạo một cấu trúc đối tượng mới bằng cách tạo các instance :class:`~email.message.Message`, thêm tệp đính kèm và tự thêm tất cả các header thích hợp. Tuy nhiên, đối với message MIME, package :mod:`email` cung cấp một số lớp con thuận tiện để giúp mọi việc trở nên dễ dàng hơn.

Dưới đây là các lớp:

.. module:: email.mime.base

.. class:: MIMEBase(_maintype, _subtype, *, policy=compat32, **_params)

   Mô-đun: :mod:`email.mime.base`

   Đây là lớp cơ sở cho tất cả các lớp con dành riêng cho MIME của
   :class:`~email.message.Message`.  Thông thường, bạn sẽ không tạo các thực thể cụ thể của :class:`MIMEBase`, mặc dù bạn có thể làm vậy.  :class:`MIMEBase` chủ yếu được cung cấp làm lớp cơ sở thuận tiện cho các lớp con cụ thể hơn có hỗ trợ MIME.

   *_maintype* là kiểu chính :mailheader:`Content-Type` (ví dụ: :mimetype:`text` hoặc :mimetype:`image`), còn *_subtype* là kiểu phụ :mailheader:`Content-Type` (ví dụ: :mimetype:`plain` hoặc :mimetype:`gif`).  *_params* là một từ điển khóa/giá trị tham số và được truyền trực tiếp cho :meth:`Message.add_header <email.message.Message.add_header>`.

   Nếu *policy* được chỉ định (mặc định là policy
   :class:`compat32 <email.policy.Compat32>`), nó sẽ được truyền cho
   :class:`~email.message.Message`.

   Lớp :class:`MIMEBase` luôn thêm một header :mailheader:`Content-Type` (dựa trên *_maintype*, *_subtype* và *_params*), và một
   header :mailheader:`MIME-Version` (luôn được đặt thành ``1.0``).

   .. versionchanged:: 3.6
      Đã thêm tham số chỉ dùng theo từ khóa *policy*.


.. module:: email.mime.nonmultipart

.. class:: MIMENonMultipart()

   Mô-đun: :mod:`email.mime.nonmultipart`

   Là một lớp con của :class:`~email.mime.base.MIMEBase`, đây là lớp cơ sở trung gian cho các message MIME không phải là :mimetype:`multipart`. Mục đích chính của lớp này là ngăn việc sử dụng
   phương thức :meth:`~email.message.Message.attach`, vốn chỉ có ý nghĩa đối với
   các message :mimetype:`multipart`. Nếu gọi :meth:`~email.message.Message.attach`, một ngoại lệ :exc:`~email.errors.MultipartConversionError` sẽ được đưa ra.


.. module:: email.mime.multipart

.. class:: MIMEMultipart(_subtype='mixed', boundary=None, _subparts=None, \
                         *, policy=compat32, **_params)

   Mô-đun: :mod:`email.mime.multipart`

   Là một lớp con của :class:`~email.mime.base.MIMEBase`, đây là lớp cơ sở trung gian cho các thông điệp MIME có :mimetype:`multipart`. *_subtype* tùy chọn mặc định là :mimetype:`mixed`, nhưng có thể được dùng để chỉ định subtype của thông điệp. Một header :mailheader:`Content-Type` có giá trị :mimetype:`multipart/_subtype` sẽ được thêm vào đối tượng thông điệp. Một header :mailheader:`MIME-Version` cũng sẽ được thêm vào.

   *boundary* tùy chọn là chuỗi boundary của multipart. Khi là ``None`` (mặc định), boundary được tính khi cần (chẳng hạn khi thông điệp được serialize).

   *_subparts* là một sequence gồm các subpart ban đầu cho payload. Phải có thể chuyển sequence này thành một list. Bạn luôn có thể đính kèm các subpart mới vào thông điệp bằng cách sử dụng phương thức :meth:`Message.attach <email.message.Message.attach>`.

   Đối số *policy* tùy chọn mặc định là :class:`compat32 <email.policy.Compat32>`.

   Các tham số bổ sung cho header :mailheader:`Content-Type` được lấy từ các keyword argument hoặc được truyền vào đối số *_params*, vốn là một keyword dictionary.

   .. versionchanged:: 3.6
      Đã thêm tham số chỉ dùng theo từ khóa *policy*.

.. module:: email.mime.application

.. class:: MIMEApplication(_data, _subtype='octet-stream', \
                           _encoder=email.encoders.encode_base64, \ *, policy=compat32, **_params)

   Mô-đun: :mod:`email.mime.application`

   Là một lớp con của :class:`~email.mime.nonmultipart.MIMENonMultipart`, lớp này
   Lớp :class:`MIMEApplication` được dùng để biểu diễn các đối tượng thông báo MIME có kiểu chính là :mimetype:`application`.  *_data* chứa các byte của dữ liệu ứng dụng thô.  *_subtype* tùy chọn chỉ định subtype MIME và mặc định là :mimetype:`octet-stream`.

   *_encoder* tùy chọn là một callable (tức là hàm) thực hiện việc mã hóa dữ liệu để truyền tải.  Callable này nhận một đối số, đó là đối tượng :class:`MIMEApplication`. Đối tượng này nên sử dụng
   :meth:`~email.message.Message.get_payload` và
   :meth:`~email.message.Message.set_payload` được gọi để thay đổi payload sang dạng đã mã hóa. Hàm này cũng sẽ thêm mọi :mailheader:`Content-Transfer-Encoding` hoặc header khác vào đối tượng message khi cần. Dạng mã hóa mặc định là base64. Xem
   mô-đun :mod:`email.encoders` để biết danh sách các encoder tích hợp sẵn.

   Đối số *policy* tùy chọn mặc định là :class:`compat32 <email.policy.Compat32>`.

   *_params* được truyền trực tiếp đến hàm khởi tạo của lớp cơ sở.

   .. versionchanged:: 3.6
      Đã thêm tham số chỉ dùng theo từ khóa *policy*.

.. module:: email.mime.audio

.. class:: MIMEAudio(_audiodata, _subtype=None, \
                     _encoder=email.encoders.encode_base64, \ *, policy=compat32, **_params)

   Mô-đun: :mod:`email.mime.audio`

   Là một lớp con của :class:`~email.mime.nonmultipart.MIMENonMultipart`, lớp này
   Lớp :class:`MIMEAudio` được dùng để tạo các đối tượng thông điệp MIME có kiểu chính
   :mimetype:`audio`. *_audiodata* chứa các byte của dữ liệu âm thanh thô. Nếu dữ liệu này có thể được giải mã dưới dạng au, wav, aiff hoặc aifc, thì subtype sẽ tự động được đưa vào header :mailheader:`Content-Type`. Nếu không, bạn có thể chỉ định rõ subtype âm thanh thông qua đối số *_subtype*. Nếu không thể suy đoán minor type và không cung cấp *_subtype*, thì :exc:`TypeError` sẽ được đưa ra.

   *_encoder* tùy chọn là một callable (tức là một hàm) thực hiện việc encoding thực tế dữ liệu âm thanh để truyền tải. Callable này nhận một đối số là instance :class:`MIMEAudio`. Callable này nên sử dụng
   :meth:`~email.message.Message.get_payload` và
   :meth:`~email.message.Message.set_payload` được gọi để thay đổi payload sang dạng đã mã hóa. Hàm này cũng sẽ thêm mọi :mailheader:`Content-Transfer-Encoding` hoặc header khác vào đối tượng message khi cần. Dạng mã hóa mặc định là base64. Xem
   mô-đun :mod:`email.encoders` để biết danh sách các encoder tích hợp sẵn.

   Đối số *policy* tùy chọn mặc định là :class:`compat32 <email.policy.Compat32>`.

   *_params* được truyền trực tiếp đến hàm khởi tạo của lớp cơ sở.

   .. versionchanged:: 3.6
      Đã thêm tham số chỉ dùng theo từ khóa *policy*.

.. module:: email.mime.image

.. class:: MIMEImage(_imagedata, _subtype=None, \
                     _encoder=email.encoders.encode_base64, \
                    *, policy=compat32, **_params)

   Mô-đun: :mod:`email.mime.image`

   Là một lớp con của :class:`~email.mime.nonmultipart.MIMENonMultipart`, lớp này
   Lớp :class:`MIMEImage` được dùng để tạo các đối tượng thông báo MIME có kiểu chính là
   :mimetype:`image`. *_imagedata* chứa các byte của dữ liệu hình ảnh thô. Nếu có thể xác định được kiểu dữ liệu này (đã thử jpeg, png, gif, tiff, rgb, pbm, pgm, ppm, rast, xbm, bmp, webp và exr), thì kiểu phụ sẽ tự động được đưa vào header :mailheader:`Content-Type`. Nếu không, bạn có thể chỉ định rõ kiểu phụ của hình ảnh thông qua đối số *_subtype*. Nếu không thể suy đoán kiểu phụ và *_subtype* không được cung cấp, thì
   :exc:`TypeError` sẽ được phát sinh.

   *_encoder* tùy chọn là một callable (tức là một hàm) thực hiện việc mã hóa thực tế dữ liệu hình ảnh để truyền đi. Callable này nhận một đối số, là thể hiện :class:`MIMEImage`. Callable này nên sử dụng
   :meth:`~email.message.Message.get_payload` và
   :meth:`~email.message.Message.set_payload` được gọi để thay đổi payload sang dạng đã mã hóa. Hàm này cũng sẽ thêm mọi :mailheader:`Content-Transfer-Encoding` hoặc header khác vào đối tượng message khi cần. Dạng mã hóa mặc định là base64. Xem
   mô-đun :mod:`email.encoders` để biết danh sách các encoder tích hợp sẵn.

   Đối số *policy* tùy chọn mặc định là :class:`compat32 <email.policy.Compat32>`.

   *_params* được truyền trực tiếp vào hàm khởi tạo :class:`~email.mime.base.MIMEBase`.

   .. versionchanged:: 3.6
      Đã thêm tham số chỉ dùng theo từ khóa *policy*.

.. module:: email.mime.message

.. class:: MIMEMessage(_msg, _subtype='rfc822', *, policy=compat32)

   Mô-đun: :mod:`email.mime.message`

   Là một lớp con của :class:`~email.mime.nonmultipart.MIMENonMultipart`, lớp này
   Lớp :class:`MIMEMessage` được dùng để tạo các đối tượng MIME thuộc kiểu chính
   :mimetype:`message`. *_msg* được dùng làm payload và phải là một thể hiện của lớp :class:`~email.message.Message` (hoặc một lớp con của lớp đó); nếu không, một :exc:`TypeError` sẽ được phát sinh.

   *_subtype* tùy chọn đặt subtype của message; mặc định là
   :mimetype:`rfc822`.

   Đối số *policy* tùy chọn mặc định là :class:`compat32 <email.policy.Compat32>`.

   .. versionchanged:: 3.6
      Đã thêm tham số chỉ dùng theo từ khóa *policy*.

.. module:: email.mime.text

.. class:: MIMEText(_text, _subtype='plain', _charset=None, *, policy=compat32)

   Mô-đun: :mod:`email.mime.text`

   Là một lớp con của :class:`~email.mime.nonmultipart.MIMENonMultipart`, lớp này
   Lớp :class:`MIMEText` được dùng để tạo các MIME object có kiểu chính
   :mimetype:`text`. *_text* là chuỗi cho payload.  *_subtype* là kiểu phụ và mặc định là :mimetype:`plain`.  *_charset* là bộ ký tự của văn bản và được truyền dưới dạng đối số cho
   :class:`~email.mime.nonmultipart.MIMENonMultipart` hàm khởi tạo; mặc định là ``us-ascii`` nếu chuỗi chỉ chứa các code point ``ascii``, và ``utf-8`` nếu không. Tham số *_charset* chấp nhận một chuỗi hoặc một
   đối tượng :class:`~email.charset.Charset`.

   Trừ khi đối số *_charset* được đặt rõ ràng thành ``None``, đối tượng MIMEText được tạo sẽ có cả một header :mailheader:`Content-Type` với tham số ``charset``, và một header :mailheader:`Content-Transfer-Encoding`. Điều này có nghĩa là một lệnh gọi ``set_payload`` tiếp theo sẽ không tạo payload được mã hóa, ngay cả khi một charset được truyền trong lệnh ``set_payload``. Bạn có thể "đặt lại" hành vi này bằng cách xóa header ``Content-Transfer-Encoding``; sau đó, một lệnh gọi ``set_payload`` sẽ tự động mã hóa payload mới (và thêm một header
   :mailheader:`Content-Transfer-Encoding`).

   Đối số *policy* tùy chọn mặc định là :class:`compat32 <email.policy.Compat32>`.

   .. versionchanged:: 3.5
      *_charset* cũng chấp nhận các instance :class:`~email.charset.Charset`.

   .. versionchanged:: 3.6
      Đã thêm tham số chỉ dùng theo từ khóa *policy*.
