:mod:`!smtplib` --- Máy khách giao thức SMTP
============================================

.. module:: smtplib
   :synopsis: Máy khách giao thức SMTP (yêu cầu sockets).

.. sectionauthor:: Eric S. Raymond <esr@snark.thyrsus.com>

**Mã nguồn:** :source:`Lib/smtplib.py`

.. index::
   pair: SMTP; protocol
   single: Simple Mail Transfer Protocol

--------------

Mô-đun :mod:`!smtplib` định nghĩa một đối tượng phiên SMTP client có thể được dùng để gửi thư đến bất kỳ máy nào trên Internet có daemon listener SMTP hoặc ESMTP. Để biết chi tiết về hoạt động của SMTP và ESMTP, hãy tham khảo :rfc:`821` (Simple Mail Transfer Protocol) và :rfc:`1869` (SMTP Service Extensions).

.. include:: ../includes/wasm-notavail.rst

.. class:: SMTP(host='', port=0, local_hostname=None[, timeout], source_address=None)

   Một thực thể :class:`SMTP` đóng gói một kết nối SMTP. Thực thể này có các phương thức hỗ trợ đầy đủ các thao tác SMTP và ESMTP. Nếu cung cấp các tham số tùy chọn *host* và *port*, phương thức SMTP :meth:`connect` sẽ được gọi với các tham số đó trong quá trình khởi tạo. Nếu được chỉ định, *local_hostname* được dùng làm FQDN của máy cục bộ trong lệnh HELO/EHLO. Nếu không, tên máy cục bộ được tìm bằng cách sử dụng
   :func:`socket.getfqdn`. Nếu lệnh gọi :meth:`connect` trả về bất kỳ giá trị nào khác mã thành công, một :exc:`SMTPConnectError` sẽ được raised. Tham số tùy chọn *timeout* chỉ định thời gian chờ tính bằng giây cho các thao tác blocking như lần thử kết nối (nếu không chỉ định, thiết lập thời gian chờ mặc định toàn cục sẽ được sử dụng). Nếu thời gian chờ hết hạn, :exc:`TimeoutError` sẽ được raised. Tham số tùy chọn *source_address* cho phép binding với một địa chỉ nguồn cụ thể trên máy có nhiều network interface và/hoặc với một TCP port nguồn cụ thể. Tham số này nhận một tuple 2 phần tử ``(host, port)``, để socket binding với tư cách địa chỉ nguồn trước khi kết nối. Nếu bỏ qua (hoặc nếu *host* hoặc *port* lần lượt là ``''`` và/hoặc ``0``) thì hành vi mặc định của OS sẽ được sử dụng.

   Trong trường hợp sử dụng thông thường, bạn chỉ cần khởi tạo/kết nối,
   :meth:`sendmail`, và các phương thức :meth:`SMTP.quit`. Bên dưới có một ví dụ.

   Lớp :class:`SMTP` hỗ trợ câu lệnh :keyword:`with`. Khi được sử dụng như thế này, lệnh SMTP ``QUIT`` sẽ tự động được gửi khi
   câu lệnh :keyword:`!with` kết thúc. Ví dụ:::

    >>> from smtplib import SMTP
    >>> with SMTP("domain.org") as smtp:
    ...     smtp.noop()
    ...
    (250, b'Ok')
    >>>

   .. audit-event:: smtplib.send self,data smtplib.SMTP

      Tất cả các lệnh sẽ phát sinh một :ref:`sự kiện auditing <auditing>` ``smtplib.SMTP.send`` với các đối số ``self`` và ``data``, trong đó ``data`` là các byte sắp được gửi đến máy chủ từ xa.

   .. versionchanged:: 3.3
      Đã bổ sung hỗ trợ cho câu lệnh :keyword:`with`.

   .. versionchanged:: 3.3
      Đã bổ sung đối số *source_address*.

   .. versionadded:: 3.5
      Phần mở rộng SMTPUTF8 (:rfc:`6531`) hiện đã được hỗ trợ.

   .. versionchanged:: 3.9
      Nếu tham số *timeout* được đặt bằng không, tham số này sẽ gây ra một
      :class:`ValueError` để ngăn việc tạo một socket không chặn.

.. class:: SMTP_SSL(host='', port=0, local_hostname=None, * [, timeout], \
                    context=None, source_address=None)

   Một instance :class:`SMTP_SSL` hoạt động hoàn toàn giống như các instance của
   :class:`SMTP`. :class:`SMTP_SSL` nên được sử dụng trong những trường hợp SSL là bắt buộc ngay từ đầu kết nối và việc sử dụng :meth:`~SMTP.starttls` là không phù hợp. Nếu không chỉ định *host*, máy chủ cục bộ sẽ được sử dụng. Nếu *port* bằng không, cổng SMTP-over-SSL tiêu chuẩn (465) sẽ được sử dụng. Các đối số tùy chọn *local_hostname*, *timeout* và *source_address* có cùng ý nghĩa như trong lớp :class:`SMTP`. *context*, cũng là tùy chọn, có thể chứa một :class:`~ssl.SSLContext` và cho phép cấu hình nhiều khía cạnh của kết nối bảo mật. Vui lòng đọc :ref:`ssl-security` để biết các phương pháp hay nhất.

   .. versionchanged:: 3.3
      Đã bổ sung *context*.

   .. versionchanged:: 3.3
      Đã bổ sung đối số *source_address*.

   .. versionchanged:: 3.4
      Lớp này hiện hỗ trợ kiểm tra hostname bằng
      :attr:`ssl.SSLContext.check_hostname` và *Server Name Indication* (xem
      :const:`ssl.HAS_SNI`).

   .. versionchanged:: 3.9
      Nếu tham số *timeout* được đặt bằng không, tham số này sẽ gây ra một
      :class:`ValueError` để ngăn việc tạo socket không blocking

   .. versionchanged:: 3.12
      Các tham số *keyfile* và *certfile* không còn được hỗ trợ đã bị loại bỏ.

.. class:: LMTP(host='', port=LMTP_PORT, local_hostname=None, \
                source_address=None[, timeout])

   Giao thức LMTP, rất giống ESMTP, phần lớn dựa trên SMTP client tiêu chuẩn. LMTP thường sử dụng Unix socket, vì vậy của chúng tôi
   Phương thức :meth:`~SMTP.connect` cũng phải hỗ trợ điều đó, ngoài máy chủ host:port thông thường. Các đối số tùy chọn *local_hostname* và *source_address* có cùng ý nghĩa như trong lớp :class:`SMTP`. Để chỉ định Unix socket, bạn phải sử dụng đường dẫn tuyệt đối cho *host*, bắt đầu bằng '/'.

   Cơ chế xác thực được hỗ trợ bằng cách sử dụng cơ chế SMTP thông thường. Khi sử dụng Unix socket, LMTP thường không hỗ trợ hoặc không yêu cầu xác thực, nhưng điều này có thể khác tùy trường hợp.

   .. versionchanged:: 3.9
      Tham số tùy chọn *timeout* đã được bổ sung.


Một tập hợp phong phú các exception cũng được định nghĩa:


.. exception:: SMTPException

   Lớp con của :exc:`OSError`, là lớp exception cơ sở cho tất cả các exception khác do module này cung cấp.

   .. versionchanged:: 3.4
      SMTPException đã trở thành lớp con của :exc:`OSError`


.. exception:: SMTPServerDisconnected

   Exception này được raise khi máy chủ ngắt kết nối đột ngột hoặc khi cố gắng sử dụng instance :class:`SMTP` trước khi kết nối nó với máy chủ.


.. exception:: SMTPResponseException

   Lớp cơ sở cho tất cả các ngoại lệ bao gồm mã lỗi SMTP. Các ngoại lệ này được tạo ra trong một số trường hợp khi máy chủ SMTP trả về mã lỗi.

   .. attribute:: smtp_code

      Mã lỗi.

   .. attribute:: smtp_error

      Thông báo lỗi.


.. exception:: SMTPSenderRefused

   Địa chỉ người gửi bị từ chối. Ngoài các thuộc tính được thiết lập trên tất cả
   các ngoại lệ :exc:`SMTPResponseException`, thuộc tính này đặt 'sender' thành chuỗi mà máy chủ SMTP đã từ chối.


.. exception:: SMTPRecipientsRefused

   Tất cả địa chỉ người nhận đều bị từ chối.

   .. attribute:: recipients

      Một dictionary có đúng cùng kiểu với dictionary được trả về bởi :meth:`SMTP.sendmail`, chứa các lỗi cho từng người nhận.


.. exception:: SMTPDataError

   Máy chủ SMTP từ chối chấp nhận dữ liệu thư.


.. exception:: SMTPConnectError

   Đã xảy ra lỗi trong quá trình thiết lập kết nối với máy chủ.


.. exception:: SMTPHeloError

   Máy chủ từ chối thư ``HELO`` của chúng tôi.


.. exception:: SMTPNotSupportedError

    Máy chủ không hỗ trợ lệnh hoặc tùy chọn được yêu cầu.

    .. versionadded:: 3.5


.. exception:: SMTPAuthenticationError

   Xác thực SMTP không thành công.  Rất có thể máy chủ không chấp nhận tổ hợp tên người dùng/mật khẩu được cung cấp.


.. seealso::

   :rfc:`821` - Giao thức truyền thư đơn giản
      Định nghĩa giao thức SMTP.  Tài liệu này trình bày mô hình, quy trình vận hành và các chi tiết của giao thức SMTP.

   :rfc:`1869` - Các phần mở rộng dịch vụ SMTP
      Định nghĩa các phần mở rộng ESMTP cho SMTP. Nội dung này mô tả một framework để mở rộng SMTP bằng các lệnh mới, hỗ trợ tự động phát hiện các lệnh do máy chủ cung cấp và định nghĩa thêm một số lệnh.


.. _smtp-objects:

Các đối tượng SMTP
------------------

Một thực thể :class:`SMTP` có các phương thức sau:

.. method:: SMTP.set_debuglevel(level)

   Đặt mức độ xuất thông tin gỡ lỗi. Giá trị 1 hoặc ``True`` cho *level* sẽ tạo thông báo gỡ lỗi cho kết nối và cho tất cả thông báo được gửi đến cũng như nhận từ máy chủ. Giá trị 2 cho *level* sẽ khiến các thông báo này được thêm dấu thời gian.

   .. versionchanged:: 3.5 Đã thêm debuglevel 2.


.. method:: SMTP.docmd(cmd, args='')

   Gửi lệnh *cmd* đến máy chủ. Đối số tùy chọn *args* chỉ đơn giản được nối vào lệnh, được phân cách bằng một dấu cách.

   Phương thức này trả về một bộ 2 phần tử gồm mã phản hồi dạng số và dòng phản hồi thực tế (các phản hồi nhiều dòng được nối thành một dòng dài duy nhất.)

   Trong hoạt động thông thường, bạn không cần gọi phương thức này một cách tường minh. Phương thức này được dùng để triển khai các phương thức khác và có thể hữu ích khi kiểm thử các phần mở rộng riêng tư.

   Nếu kết nối với máy chủ bị mất trong khi đang chờ phản hồi,
   :exc:`SMTPServerDisconnected` sẽ được đưa ra.


.. method:: SMTP.connect(host='localhost', port=0)

   Kết nối với một máy chủ trên cổng đã cho. Mặc định, phương thức này kết nối với máy chủ cục bộ qua cổng SMTP tiêu chuẩn (25). Nếu tên máy chủ kết thúc bằng dấu hai chấm (``':'``) theo sau là một số, phần hậu tố đó sẽ bị loại bỏ và số này được hiểu là số cổng cần sử dụng. Phương thức này được hàm khởi tạo tự động gọi nếu một máy chủ được chỉ định khi khởi tạo. Trả về một bộ 2 phần tử gồm mã phản hồi và thông báo do máy chủ gửi trong phản hồi kết nối.

   .. audit-event:: smtplib.connect self,host,port smtplib.SMTP.connect


.. method:: SMTP.helo(name='')

   Xác định danh tính của bạn với máy chủ SMTP bằng ``HELO``. Đối số hostname mặc định là tên miền đầy đủ của máy chủ cục bộ. Thông báo do máy chủ trả về được lưu trong thuộc tính :attr:`helo_resp` của đối tượng.

   Trong hoạt động thông thường, bạn không cần gọi phương thức này một cách tường minh. Phương thức này sẽ được :meth:`sendmail` gọi ngầm khi cần.


.. method:: SMTP.ehlo(name='')

   Xác thực danh tính của bạn với máy chủ ESMTP bằng ``EHLO``. Đối số hostname mặc định là tên miền đủ điều kiện (FQDN) của máy chủ cục bộ. Kiểm tra phản hồi để tìm các tùy chọn ESMTP và lưu chúng để :meth:`has_extn` sử dụng. Đồng thời thiết lập một số thuộc tính thông tin: thông báo do máy chủ trả về được lưu trong thuộc tính :attr:`ehlo_resp`, :attr:`does_esmtp` được đặt thành ``True`` hoặc ``False`` tùy thuộc vào việc máy chủ có hỗ trợ ESMTP hay không, và :attr:`esmtp_features` sẽ là một từ điển chứa tên của các phần mở rộng dịch vụ SMTP mà máy chủ này hỗ trợ cùng với các tham số của chúng (nếu có).

   Trừ khi bạn muốn sử dụng :meth:`has_extn` trước khi gửi thư, bạn không cần gọi phương thức này một cách rõ ràng. Phương thức này sẽ được gọi ngầm bởi
   :meth:`sendmail` khi cần.

.. method:: SMTP.ehlo_or_helo_if_needed()

   Phương thức này gọi :meth:`ehlo` và/hoặc :meth:`helo` nếu trước đó trong phiên này chưa có lệnh ``EHLO`` hoặc ``HELO``. Trước tiên, phương thức thử ESMTP ``EHLO``.

   :exc:`SMTPHeloError`
     Máy chủ không phản hồi đúng cách với lời chào ``HELO``.

.. method:: SMTP.has_extn(name)

   Trả về :const:`True` nếu *name* nằm trong tập các phần mở rộng dịch vụ SMTP do máy chủ trả về; nếu không thì trả về :const:`False`. Không phân biệt chữ hoa chữ thường.


.. method:: SMTP.verify(address)

   Kiểm tra tính hợp lệ của một địa chỉ trên máy chủ này bằng SMTP ``VRFY``. Trả về một tuple gồm mã 250 và địa chỉ :rfc:`822` đầy đủ (bao gồm tên hiển thị) nếu địa chỉ người dùng hợp lệ. Nếu không, trả về mã lỗi SMTP từ 400 trở lên và một chuỗi lỗi.

   .. note::

      Nhiều trang web vô hiệu hóa ``VRFY`` SMTP để ngăn chặn spammer.


.. method:: SMTP.login(user, password, *, initial_response_ok=True)

   Đăng nhập vào máy chủ SMTP yêu cầu xác thực. Các đối số là tên người dùng và mật khẩu dùng để xác thực. Nếu trước đó trong phiên này chưa có lệnh ``EHLO`` hoặc ``HELO``, phương thức này trước tiên sẽ thử ESMTP ``EHLO``. Phương thức này sẽ trả về bình thường nếu xác thực thành công hoặc có thể phát sinh các ngoại lệ sau:

   :exc:`SMTPHeloError`
      Máy chủ không phản hồi đúng cách với lời chào ``HELO``.

   :exc:`SMTPAuthenticationError`
      Máy chủ không chấp nhận tổ hợp tên người dùng/mật khẩu.

   :exc:`SMTPNotSupportedError`
      Lệnh ``AUTH`` không được máy chủ hỗ trợ.

   :exc:`SMTPException`
      Không tìm thấy phương thức xác thực phù hợp.

   Mỗi phương thức xác thực được :mod:`!smtplib` hỗ trợ sẽ lần lượt được thử nếu máy chủ thông báo rằng phương thức đó được hỗ trợ. Xem :meth:`auth` để biết danh sách các phương thức xác thực được hỗ trợ. *initial_response_ok* được truyền qua :meth:`auth`.

   Đối số từ khóa tùy chọn *initial_response_ok* chỉ định liệu, đối với các phương thức xác thực hỗ trợ tính năng này, một "initial response" như được chỉ định trong :rfc:`4954` có thể được gửi cùng với lệnh ``AUTH``, thay vì yêu cầu challenge/response.

   .. versionchanged:: 3.5
      :exc:`SMTPNotSupportedError` may be raised, and the
      Đã thêm tham số *initial_response_ok*.


.. method:: SMTP.auth(mechanism, authobject, *, initial_response_ok=True)

   Phát hành lệnh ``SMTP`` ``AUTH`` cho *mechanism* xác thực được chỉ định và xử lý challenge response thông qua *authobject*.

   *mechanism* chỉ định mechanism xác thực được dùng làm đối số cho lệnh ``AUTH``; các giá trị hợp lệ là những giá trị được liệt kê trong phần tử ``auth`` của :attr:`esmtp_features`.

   *authobject* phải là một đối tượng callable nhận một đối số đơn tùy chọn::

     data = authobject(challenge=None)

   Nếu đối số từ khóa tùy chọn *initial_response_ok* là true, ``authobject()`` sẽ được gọi trước tiên mà không có đối số. Nó có thể trả về
   :rfc:`4954` "initial response" ASCII ``str``, chuỗi này sẽ được mã hóa và gửi cùng với lệnh ``AUTH`` như bên dưới. Nếu ``authobject()`` không hỗ trợ initial response (ví dụ: vì yêu cầu challenge), nó sẽ trả về ``None`` khi được gọi với ``challenge=None``. Nếu *initial_response_ok* là false, thì ``authobject()`` sẽ không được gọi trước tiên với ``None``.

   Nếu bước kiểm tra phản hồi ban đầu trả về ``None``, hoặc nếu *initial_response_ok* là false, ``authobject()`` sẽ được gọi để xử lý phản hồi thử thách của máy chủ; đối số *challenge* được truyền cho nó sẽ là một ``bytes``. Nó phải trả về dữ liệu ASCII ``str`` *data*, dữ liệu này sẽ được mã hóa base64 và gửi đến máy chủ.

   Lớp ``SMTP`` cung cấp ``authobjects`` cho các cơ chế ``CRAM-MD5``, ``PLAIN`` và ``LOGIN``; lần lượt chúng được đặt tên là ``SMTP.auth_cram_md5``, ``SMTP.auth_plain`` và ``SMTP.auth_login``. Tất cả đều yêu cầu các thuộc tính ``user`` và ``password`` của thực thể ``SMTP`` được đặt thành các giá trị phù hợp.

   Mã người dùng thường không cần gọi trực tiếp ``auth``, mà có thể gọi phương thức :meth:`login`, phương thức này sẽ lần lượt thử từng cơ chế nêu trên theo thứ tự được liệt kê. ``auth`` được cung cấp để hỗ trợ triển khai các phương thức xác thực chưa được :mod:`!smtplib` hỗ trợ trực tiếp (hoặc chưa được hỗ trợ).

   .. versionadded:: 3.5


.. method:: SMTP.starttls(*, context=None)

   Đặt kết nối SMTP vào chế độ TLS (Transport Layer Security). Tất cả lệnh SMTP tiếp theo sẽ được mã hóa. Sau đó, bạn nên gọi lại :meth:`ehlo`.

   Nếu cung cấp *keyfile* và *certfile*, chúng sẽ được dùng để tạo một
   :class:`ssl.SSLContext`.

   Tham số *context* tùy chọn là một đối tượng :class:`ssl.SSLContext`; đây là lựa chọn thay thế cho việc sử dụng keyfile và certfile, và nếu được chỉ định thì cả *keyfile* lẫn *certfile* đều phải là ``None``.

   Nếu trong phiên này chưa có lệnh ``EHLO`` hoặc ``HELO`` nào trước đó, phương thức này trước tiên sẽ thử ESMTP ``EHLO``.

   .. versionchanged:: 3.12
      Các tham số không còn được khuyến nghị *keyfile* và *certfile* đã bị xóa.

   :exc:`SMTPHeloError`
      Máy chủ không phản hồi đúng cách với lời chào ``HELO``.

   :exc:`SMTPNotSupportedError`
     Máy chủ không hỗ trợ extension STARTTLS.

   :exc:`RuntimeError`
     Trình thông dịch Python của bạn không hỗ trợ SSL/TLS.

   .. versionchanged:: 3.3
      *context* đã được thêm.

   .. versionchanged:: 3.4
      Phương thức hiện hỗ trợ kiểm tra hostname với
      :attr:`ssl.SSLContext.check_hostname` và *Server Name Indicator* (xem
      :const:`~ssl.HAS_SNI`).

   .. versionchanged:: 3.5
      Lỗi phát sinh do không hỗ trợ STARTTLS hiện giờ là
      lớp con :exc:`SMTPNotSupportedError` thay vì lớp cơ sở
      :exc:`SMTPException`.


.. method:: SMTP.sendmail(from_addr, to_addrs, msg, mail_options=(), rcpt_options=())

   Gửi thư. Các đối số bắt buộc là một chuỗi địa chỉ người gửi :rfc:`822`, một danh sách các chuỗi địa chỉ người nhận :rfc:`822` (một chuỗi đơn sẽ được coi là danh sách có 1 địa chỉ), và một chuỗi thông báo. Bên gọi có thể truyền một danh sách các tùy chọn ESMTP (chẳng hạn như ``"8bitmime"``) được sử dụng trong các lệnh ``MAIL FROM`` dưới dạng *mail_options*. Có thể truyền các tùy chọn ESMTP (chẳng hạn như các lệnh ``DSN``) cần được sử dụng với tất cả các lệnh ``RCPT`` dưới dạng *rcpt_options*. Mỗi tùy chọn phải được truyền dưới dạng một chuỗi chứa toàn bộ nội dung của tùy chọn, bao gồm cả khóa nếu có (ví dụ: ``"NOTIFY=SUCCESS,FAILURE"``). (Nếu cần sử dụng các tùy chọn ESMTP khác nhau cho những người nhận khác nhau, bạn phải sử dụng các phương thức cấp thấp như
   :meth:`!mail`, :meth:`!rcpt` và :meth:`!data` để gửi thông báo.)

   .. note::

      Các tham số *from_addr* và *to_addrs* được dùng để tạo phong bì thông báo được các tác nhân truyền tải sử dụng. ``sendmail`` không sửa đổi các tiêu đề thông báo theo bất kỳ cách nào.

   *msg* có thể là một chuỗi chứa các ký tự trong phạm vi ASCII hoặc một chuỗi byte. Chuỗi được mã hóa thành byte bằng codec ascii, và các ký tự ``\r`` và ``\n`` đứng riêng lẻ được chuyển thành các ký tự ``\r\n``. Chuỗi byte không bị sửa đổi.

   Nếu trước đó trong phiên này chưa có lệnh ``EHLO`` hoặc ``HELO``, phương thức này trước tiên sẽ thử ESMTP ``EHLO``. Nếu máy chủ hỗ trợ ESMTP, kích thước thông báo và từng tùy chọn được chỉ định sẽ được truyền cho máy chủ (nếu tùy chọn đó nằm trong tập tính năng mà máy chủ công bố). Nếu ``EHLO`` không thành công, ``HELO`` sẽ được thử và các tùy chọn ESMTP sẽ bị bỏ qua.

   Phương thức này sẽ trả về bình thường nếu thư được chấp nhận cho ít nhất một người nhận. Nếu không, phương thức sẽ phát sinh một ngoại lệ. Điều đó có nghĩa là nếu phương thức này không phát sinh ngoại lệ thì thư của bạn sẽ đến được tay ai đó. Nếu phương thức này không phát sinh ngoại lệ, phương thức sẽ trả về một dictionary, với một mục cho mỗi người nhận bị từ chối. Mỗi mục chứa một tuple gồm mã lỗi SMTP và thông báo lỗi đi kèm do máy chủ gửi.

   Nếu ``SMTPUTF8`` được bao gồm trong *mail_options* và máy chủ hỗ trợ tùy chọn này, *from_addr* và *to_addrs* có thể chứa các ký tự không phải ASCII.

   Phương thức này có thể phát sinh các ngoại lệ sau:

   :exc:`SMTPRecipientsRefused`
      Tất cả người nhận đều bị từ chối. Không ai nhận được thư.

   :exc:`SMTPHeloError`
      Máy chủ không phản hồi đúng cách với lời chào ``HELO``.

   :exc:`SMTPSenderRefused`
      Máy chủ không chấp nhận *from_addr*.

   :exc:`SMTPDataError`
      Máy chủ phản hồi bằng một mã lỗi không mong đợi (không phải do từ chối người nhận).

   :exc:`SMTPNotSupportedError`
      ``SMTPUTF8`` được cung cấp trong *mail_options* nhưng máy chủ không hỗ trợ.

   Trừ khi có ghi chú khác, kết nối sẽ vẫn mở ngay cả sau khi một exception được raised.

   .. versionchanged:: 3.2
      *msg* có thể là một chuỗi byte.

   .. versionchanged:: 3.5
      Đã bổ sung hỗ trợ ``SMTPUTF8``, và có thể raised :exc:`SMTPNotSupportedError` nếu ``SMTPUTF8`` được chỉ định nhưng máy chủ không hỗ trợ.


.. method:: SMTP.send_message(msg, from_addr=None, to_addrs=None, \
                              mail_options=(), rcpt_options=())

   Đây là một phương thức tiện ích để gọi :meth:`sendmail` với thông điệp được biểu diễn bởi một đối tượng :class:`email.message.Message`. Các đối số có ý nghĩa giống như trong :meth:`sendmail`, ngoại trừ việc *msg* là một đối tượng ``Message``.

   Nếu *from_addr* là ``None`` hoặc *to_addrs* là ``None``, ``send_message`` sẽ điền các đối số đó bằng những địa chỉ được trích xuất từ các header của *msg* như được chỉ định trong :rfc:`5322`\: *from_addr* được đặt thành trường :mailheader:`Sender` nếu trường này hiện diện, nếu không thì đặt thành trường :mailheader:`From`. *to_addrs* kết hợp các giá trị (nếu có) của :mailheader:`To`,
   :mailheader:`Cc`, và các trường :mailheader:`Bcc` của *msg*. Nếu trong thư xuất hiện đúng một nhóm tiêu đề :mailheader:`Resent-*`, các tiêu đề thông thường sẽ bị bỏ qua và thay vào đó sử dụng các tiêu đề :mailheader:`Resent-*`. Nếu thư chứa nhiều hơn một nhóm tiêu đề :mailheader:`Resent-*`, một :exc:`ValueError` sẽ được phát sinh vì không có cách nào xác định rõ ràng nhóm tiêu đề :mailheader:`Resent-` mới nhất.

   ``send_message`` tuần tự hóa *msg* bằng cách sử dụng
   :class:`~email.generator.BytesGenerator` với ``\r\n`` làm *linesep*, rồi gọi :meth:`sendmail` để truyền thư thu được. Bất kể giá trị của *from_addr* và *to_addrs* là gì, ``send_message`` không truyền bất kỳ
   :mailheader:`Bcc` hoặc tiêu đề :mailheader:`Resent-Bcc` nào có thể xuất hiện trong *msg*. Nếu bất kỳ địa chỉ nào trong *from_addr* và *to_addrs* chứa ký tự không phải ASCII và máy chủ không thông báo hỗ trợ ``SMTPUTF8``, một :exc:`SMTPNotSupportedError` sẽ được phát sinh. Nếu không, ``Message`` được tuần tự hóa cùng với một bản sao của :mod:`~email.policy`, trong đó
   :attr:`~email.policy.EmailPolicy.utf8` thuộc tính được đặt thành ``True``, còn ``SMTPUTF8`` và ``BODY=8BITMIME`` được thêm vào *mail_options*.

   .. versionadded:: 3.2

   .. versionadded:: 3.5
      Hỗ trợ các địa chỉ được quốc tế hóa (``SMTPUTF8``).


.. method:: SMTP.quit()

   Kết thúc phiên SMTP và đóng kết nối. Trả về kết quả của lệnh SMTP ``QUIT``.


Các phương thức cấp thấp tương ứng với các lệnh SMTP/ESMTP tiêu chuẩn ``HELP``, ``RSET``, ``NOOP``, ``MAIL``, ``RCPT`` và ``DATA`` cũng được hỗ trợ. Thông thường, bạn không cần gọi trực tiếp các phương thức này, nên chúng không được ghi lại ở đây. Để biết chi tiết, hãy tham khảo mã nguồn của module.

Ngoài ra, một instance SMTP có các thuộc tính sau:


.. attribute:: SMTP.helo_resp

   Phản hồi cho lệnh ``HELO``, xem :meth:`helo`.


.. attribute:: SMTP.ehlo_resp

   Phản hồi cho lệnh ``EHLO``, xem :meth:`ehlo`.


.. attribute:: SMTP.does_esmtp

   Một giá trị boolean cho biết máy chủ có hỗ trợ ESMTP hay không, xem
   :meth:`ehlo`.


.. attribute:: SMTP.esmtp_features

   Một dictionary chứa tên các phần mở rộng dịch vụ SMTP được máy chủ hỗ trợ, xem :meth:`ehlo`.


.. _smtp-example:

Ví dụ về SMTP
-------------

Ví dụ này yêu cầu người dùng cung cấp các địa chỉ cần thiết trong phong bì thư (địa chỉ 'To' và 'From') cũng như thư cần gửi. Lưu ý rằng các header được đưa vào thư phải được bao gồm trong nội dung thư như đã nhập; ví dụ này không xử lý các header :rfc:`822`. Cụ thể, các địa chỉ 'To' và 'From' phải được đưa rõ ràng vào header của thư::

   import smtplib

   def prompt(title):
       return input(title).strip()

   from_addr = prompt("From: ")
   to_addrs  = prompt("To: ").split()
   print("Enter message, end with ^D (Unix) or ^Z (Windows):")

   # Thêm header From: và To: ở đầu!
   lines = [f"From: {from_addr}", f"To: {', '.join(to_addrs)}", ""]
   while True:
       try:
           line = input()
       except EOFError:
           break
       else:
           lines.append(line)

   msg = "\r\n".join(lines)
   print("Message length is", len(msg))

   server = smtplib.SMTP("localhost")
   server.set_debuglevel(1)
   server.sendmail(from_addr, to_addrs, msg)
   server.quit()

.. note::

   Nhìn chung, bạn sẽ muốn sử dụng các tính năng của package :mod:`email` để tạo một email message, sau đó có thể gửi qua :meth:`~smtplib.SMTP.send_message`; xem :ref:`email-examples`.
