:mod:`!imaplib` --- ứng dụng khách giao thức IMAP4
==================================================

.. module:: imaplib
   :synopsis: Ứng dụng khách giao thức IMAP4 (yêu cầu sockets).

.. moduleauthor:: Piers Lauder <piers@communitysolutions.com.au>
.. sectionauthor:: Piers Lauder <piers@communitysolutions.com.au>
.. revised by ESR, January 2000
.. changes for IMAP4_SSL by Tino Lange <Tino.Lange@isg.de>, March 2002
.. changes for IMAP4_stream by Piers Lauder <piers@communitysolutions.com.au>,
   November 2002
.. changes for IMAP4 IDLE by Forest <forestix@nom.one>, August 2024

**Mã nguồn:** :source:`Lib/imaplib.py`

.. index::
   pair: IMAP4; protocol
   pair: IMAP4_SSL; protocol
   pair: IMAP4_stream; protocol

--------------

Mô-đun này định nghĩa ba lớp, :class:`IMAP4`, :class:`IMAP4_SSL` và
:class:`IMAP4_stream`, đóng gói một kết nối đến máy chủ IMAP4 và triển khai một phần lớn giao thức ứng dụng khách IMAP4rev1 như được định nghĩa trong
:rfc:`3501`. Nó tương thích ngược với các máy chủ IMAP4 (:rfc:`1730`), nhưng lưu ý rằng lệnh ``STATUS`` không được hỗ trợ trong IMAP4.

.. include:: ../includes/wasm-notavail.rst

Mô-đun :mod:`!imaplib` cung cấp ba lớp, trong đó :class:`IMAP4` là lớp cơ sở:


.. class:: IMAP4(host='', port=IMAP4_PORT, timeout=None)

   Lớp này triển khai giao thức IMAP4 thực tế. Kết nối được tạo và phiên bản giao thức (IMAP4 hoặc IMAP4rev1) được xác định khi instance được khởi tạo. Nếu không chỉ định *host*, ``''`` (host cục bộ) sẽ được sử dụng. Nếu bỏ qua *port*, cổng IMAP4 tiêu chuẩn (143) sẽ được sử dụng. Tham số *timeout* tùy chọn chỉ định thời gian chờ tính bằng giây cho lần thử kết nối. Nếu không cung cấp timeout hoặc timeout là ``None``, thời gian chờ socket mặc định toàn cục sẽ được sử dụng.

   Lớp :class:`IMAP4` hỗ trợ câu lệnh :keyword:`with`. Khi được sử dụng như vậy, lệnh ``LOGOUT`` của IMAP4 sẽ tự động được thực thi khi
   câu lệnh :keyword:`!with` kết thúc. Ví dụ:::

    >>> from imaplib import IMAP4
    >>> with IMAP4("domain.org") as M:
    ...     M.noop()
    ...
    ('OK', [b'Nothing Accomplished. d25if65hy903weo.87'])

   .. versionchanged:: 3.5
      Đã bổ sung hỗ trợ cho câu lệnh :keyword:`with`.

   .. versionchanged:: 3.9
      Đã bổ sung tham số *timeout* tùy chọn.

Ba ngoại lệ được định nghĩa dưới dạng các thuộc tính của lớp :class:`IMAP4`:


.. exception:: IMAP4.error

   Ngoại lệ được phát sinh khi xảy ra bất kỳ lỗi nào. Nguyên nhân của ngoại lệ được truyền cho hàm khởi tạo dưới dạng một chuỗi.


.. exception:: IMAP4.abort

   Lỗi máy chủ IMAP4 khiến ngoại lệ này được phát sinh. Đây là một lớp con của
   :exc:`IMAP4.error`. Lưu ý rằng việc đóng đối tượng và khởi tạo một đối tượng mới thường sẽ cho phép khôi phục sau ngoại lệ này.


.. exception:: IMAP4.readonly

   Ngoại lệ này được phát sinh khi máy chủ thay đổi trạng thái của một mailbox có quyền ghi. Đây là một lớp con của :exc:`IMAP4.error`. Một client khác hiện có quyền ghi, và mailbox sẽ cần được mở lại để lấy lại quyền ghi.


Ngoài ra còn có một lớp con dành cho các kết nối bảo mật:


.. class:: IMAP4_SSL(host='', port=IMAP4_SSL_PORT, *, ssl_context=None, \
                     timeout=None)

   Đây là một lớp con bắt nguồn từ :class:`IMAP4`, kết nối qua socket được mã hóa SSL (để sử dụng lớp này, bạn cần một module socket được biên dịch với hỗ trợ SSL). Nếu không chỉ định *host*, sẽ sử dụng ``''`` (máy chủ cục bộ). Nếu bỏ qua *port*, cổng IMAP4-over-SSL tiêu chuẩn (993) sẽ được sử dụng. *ssl_context* là một đối tượng :class:`ssl.SSLContext` cho phép gộp các tùy chọn cấu hình SSL, chứng chỉ và khóa riêng vào một cấu trúc duy nhất (có thể tồn tại trong thời gian dài). Vui lòng đọc :ref:`ssl-security` để biết các phương pháp tốt nhất.

   .. note::

      Với *ssl_context* mặc định, kết nối được mã hóa nhưng chứng chỉ máy chủ và tên máy chủ không được xác minh. Để xác minh chúng, hãy truyền vào một context được tạo bởi
      :func:`ssl.create_default_context`.

   Tham số tùy chọn *timeout* chỉ định thời gian chờ tính bằng giây cho lần thử kết nối. Nếu không cung cấp timeout hoặc timeout là ``None``, thời gian chờ socket mặc định toàn cục sẽ được sử dụng.

   .. versionchanged:: 3.3
      Đã bổ sung tham số *ssl_context*.

   .. versionchanged:: 3.4
      Lớp này hiện hỗ trợ kiểm tra hostname với
      :attr:`ssl.SSLContext.check_hostname` và *Server Name Indication* (xem
      :const:`ssl.HAS_SNI`).

   .. versionchanged:: 3.9
      Đã bổ sung tham số *timeout* tùy chọn.

   .. versionchanged:: 3.12
      Các tham số *keyfile* và *certfile* đã bị loại bỏ.

Lớp con thứ hai cho phép tạo các kết nối bởi một tiến trình con:


.. class:: IMAP4_stream(command)

   Đây là một lớp con kế thừa từ :class:`IMAP4`, kết nối với các bộ mô tả tệp ``stdin/stdout`` được tạo bằng cách truyền *command* cho ``subprocess.Popen()``.


Các hàm tiện ích sau được định nghĩa:


.. function:: Internaldate2tuple(resp)

   Phân tích cú pháp một :term:`bytes-like object` chứa phản hồi ``INTERNALDATE`` của IMAP4 và trả về thời gian cục bộ tương ứng. Giá trị trả về là một
   tuple :class:`time.struct_time` hoặc ``None`` nếu đầu vào có định dạng không đúng.

.. function:: Int2AP(num)

   Chuyển đổi một số nguyên thành dạng biểu diễn bytes bằng các ký tự trong tập [``A`` .. ``P``].


.. function:: ParseFlags(resp)

   Chuyển đổi một :term:`bytes-like object` chứa phản hồi ``FLAGS`` của IMAP4 thành một tuple gồm các flag riêng lẻ dưới dạng :class:`bytes`. Giá trị trả về là một tuple rỗng nếu đầu vào có định dạng không đúng.


.. function:: Time2Internaldate(date_time)

   Chuyển đổi *date_time* thành dạng biểu diễn ``INTERNALDATE`` của IMAP4. Giá trị trả về là một chuỗi có dạng: ``"DD-Mmm-YYYY HH:MM:SS +HHMM"`` (bao gồm cả dấu ngoặc kép). Đối số *date_time* có thể là một số (int hoặc float) biểu thị số giây kể từ epoch (do :func:`time.time` trả về), một tuple 9 phần tử biểu thị thời gian cục bộ, một instance của :class:`time.struct_time` (do trả về
   :func:`time.localtime`), một thực thể aware của
   :class:`datetime.datetime`, hoặc một chuỗi được đặt trong dấu ngoặc kép. Trong trường hợp cuối, chuỗi được giả định là đã ở đúng định dạng.

Lưu ý rằng số thứ tự thư IMAP4 thay đổi khi mailbox thay đổi; cụ thể, sau khi lệnh ``EXPUNGE`` thực hiện việc xóa, các thư còn lại sẽ được đánh lại số. Vì vậy, bạn nên sử dụng UID thay thế, với lệnh UID.

Ở cuối module có một phần kiểm thử chứa ví dụ sử dụng đầy đủ hơn.


.. seealso::

   Bạn có thể tìm thấy các tài liệu mô tả giao thức và mã nguồn của các server triển khai giao thức này do University of Washington's IMAP Information Center cung cấp tại (**Mã nguồn**) https://github.com/uw-imap/imap (**Không được duy trì**).


.. _imap4-objects:

Đối tượng IMAP4
---------------

Tất cả các lệnh IMAP4rev1 đều được biểu diễn bằng các phương thức có cùng tên, viết hoa hoặc viết thường.

Tất cả đối số của các lệnh đều được chuyển đổi thành chuỗi, ngoại trừ ``AUTHENTICATE``, và đối số cuối cùng của ``APPEND`` được truyền dưới dạng literal IMAP4. Nếu cần (chuỗi chứa các ký tự nhạy cảm với giao thức IMAP4 và không được đặt trong dấu ngoặc đơn hoặc dấu ngoặc kép) thì mỗi chuỗi sẽ được đặt trong dấu ngoặc kép. Tuy nhiên, đối số *password* của lệnh ``LOGIN`` luôn được đặt trong dấu ngoặc kép. Nếu muốn tránh việc một chuỗi đối số được đặt trong dấu ngoặc kép (ví dụ: đối số *flags* của ``STORE``) thì hãy đặt chuỗi đó trong dấu ngoặc đơn (ví dụ: ``r'(\Deleted)'``). Nhìn chung, hãy truyền các đối số không có dấu ngoặc và để module tự đặt chúng vào dấu ngoặc khi cần. Một đối số đã được đặt trong dấu ngoặc kép sẽ được giữ nguyên, nhờ đó mã tự đặt dấu ngoặc cho các đối số vẫn tiếp tục hoạt động.

Hầu hết các lệnh đều trả về một tuple: ``(type, [data, ...])``, trong đó *type* thường là ``'OK'`` hoặc ``'NO'``, còn *data* là văn bản từ phản hồi của lệnh hoặc các kết quả bắt buộc do lệnh quy định. Mỗi *data* либо là một ``bytes`` hoặc một tuple. Nếu là tuple, phần đầu tiên là phần đầu của phản hồi, còn phần thứ hai chứa dữ liệu (tức là giá trị 'literal').

Tùy chọn *message_set* của các lệnh dưới đây là một chuỗi chỉ định một hoặc nhiều thư để thực hiện thao tác. Chuỗi này có thể là một số thư đơn giản (``'1'``), một dải số thư (``'2:4'``) hoặc một nhóm các dải không liên tiếp được phân tách bằng dấu phẩy (``'1:3,6:9'``). Một dải có thể chứa dấu hoa thị để biểu thị giới hạn trên vô hạn (``'3:*'``).

Một thực thể :class:`IMAP4` có các phương thức sau:


.. method:: IMAP4.append(mailbox, flags, date_time, message)

   Append *message* vào hộp thư được chỉ định tên.

   *flags* có thể là ``None`` hoặc một chuỗi các token cờ IMAP. Nhiều cờ được phân tách bằng dấu cách, ví dụ ``r'\Seen \Answered'``. Nếu *flags* chưa được đặt trong dấu ngoặc đơn, dấu ngoặc đơn sẽ được tự động thêm vào.


.. method:: IMAP4.authenticate(mechanism, authobject)

   Lệnh Authenticate --- yêu cầu xử lý phản hồi.

   *mechanism* chỉ định cơ chế xác thực sẽ được sử dụng - nó phải xuất hiện trong biến instance ``capabilities`` dưới dạng ``AUTH=mechanism``.

   *authobject* phải là một callable object::

      data = authobject(response)

   Nó sẽ được gọi để xử lý các phản hồi tiếp tục từ server; đối số *response* được truyền cho nó sẽ là ``bytes``. Nó phải trả về ``bytes`` *data*, dữ liệu này sẽ được mã hóa base64 và gửi đến server. Nó phải trả về ``None`` nếu thay vào đó cần gửi phản hồi hủy của client ``*``.

   .. versionchanged:: 3.5
      username và password dạng string giờ được encode thành ``utf-8`` thay vì bị giới hạn ở ASCII.


.. method:: IMAP4.check()

   Tạo checkpoint cho mailbox trên server.


.. method:: IMAP4.close()

   Đóng mailbox hiện đang được chọn. Các message đã xóa sẽ bị loại khỏi mailbox có thể ghi. Đây là command được khuyến nghị trước ``LOGOUT``.


.. method:: IMAP4.copy(message_set, new_mailbox)

   Sao chép các message *message_set* vào cuối *new_mailbox*.


.. method:: IMAP4.create(mailbox)

   Tạo mailbox mới có tên *mailbox*.


.. method:: IMAP4.delete(mailbox)

   Xóa mailbox cũ có tên *mailbox*.


.. method:: IMAP4.deleteacl(mailbox, who)

   Xóa các ACL (gỡ mọi quyền) được thiết lập cho who trên mailbox.


.. method:: IMAP4.enable(capability)

   Bật *capability* (xem :rfc:`5161`). Hầu hết capability không cần được bật. Hiện tại chỉ hỗ trợ capability ``UTF8=ACCEPT`` (xem :RFC:`6855`).

   .. versionadded:: 3.5
      Bản thân phương thức :meth:`enable` và hỗ trợ :RFC:`6855`.


.. method:: IMAP4.expunge()

   Xóa vĩnh viễn các mục đã xóa khỏi mailbox được chọn. Tạo một phản hồi ``EXPUNGE`` cho mỗi thư đã xóa. Dữ liệu trả về chứa danh sách số thư ``EXPUNGE`` theo thứ tự nhận được.


.. method:: IMAP4.fetch(message_set, message_parts)

   Lấy (các phần của) thư. *message_parts* phải là một chuỗi gồm tên các phần của thư được đặt trong dấu ngoặc đơn, ví dụ: ``"(UID BODY[TEXT])"``. Dữ liệu trả về là các tuple gồm envelope và dữ liệu của phần thư.


.. method:: IMAP4.getacl(mailbox)

   Lấy các ``ACL``\ s cho *mailbox*. Phương thức này không theo tiêu chuẩn, nhưng được ``Cyrus`` server hỗ trợ.


.. method:: IMAP4.getannotation(mailbox, entry, attribute)

   Truy xuất các ``ANNOTATION``\ s được chỉ định cho *mailbox*. Phương thức này không theo tiêu chuẩn, nhưng được ``Cyrus`` server hỗ trợ.


.. method:: IMAP4.getquota(root)

   Lấy mức sử dụng tài nguyên và các giới hạn của ``quota`` *root*. Phương thức này thuộc phần mở rộng IMAP4 QUOTA được định nghĩa trong rfc2087.


.. method:: IMAP4.getquotaroot(mailbox)

   Lấy danh sách ``quota`` ``roots`` cho *mailbox* có tên. Phương thức này thuộc phần mở rộng IMAP4 QUOTA được định nghĩa trong rfc2087.


.. method:: IMAP4.idle(duration=None)

   Trả về một :class:`!Idler`: một context manager có thể lặp, triển khai lệnh ``IDLE`` của IMAP4 như được định nghĩa trong :rfc:`2177`.

   Đối tượng được trả về sẽ gửi lệnh ``IDLE`` khi được kích hoạt bởi
   câu lệnh :keyword:`with`, tạo ra các phản hồi không gắn thẻ của IMAP thông qua
   :term:`iterator` protocol và gửi ``DONE`` khi thoát khỏi context.

   Tất cả các phản hồi không gắn thẻ đến sau khi gửi lệnh ``IDLE`` (bao gồm cả những phản hồi đến trước khi máy chủ xác nhận lệnh) sẽ có thể được lấy qua phép lặp. Mọi phản hồi còn lại (những phản hồi không được lặp qua trong context :keyword:`with`) có thể được lấy theo cách thông thường sau khi ``IDLE`` kết thúc, bằng cách sử dụng :meth:`IMAP4.response`.

   Các phản hồi được biểu diễn dưới dạng các tuple ``(type, [data, ...])``, như mô tả trong :ref:`IMAP4 Objects <imap4-objects>`.

   Đối số *duration* đặt thời lượng tối đa (tính bằng giây) để duy trì trạng thái chờ, sau đó mọi phép lặp đang diễn ra sẽ dừng. Đối số này có thể là một :class:`int` hoặc
   :class:`float`, hoặc ``None`` để không giới hạn thời gian. Những bên gọi muốn tránh timeout do không hoạt động trên các máy chủ áp dụng giới hạn này nên đặt giá trị này không quá 29 phút (1740 giây). Yêu cầu kết nối socket; *duration* phải là ``None`` trên
   :class:`IMAP4_stream` connections.

   .. code-block:: pycon

      >>> with M.idle(duration=29 * 60) as idler:
      ...     for typ, data in idler:
      ...         print(typ, data)
      ...
      EXISTS [b'1']
      RECENT [b'1']


   .. method:: Idler.burst(interval=0.1)

      Trả về một loạt phản hồi cách nhau không quá *interval* giây (được biểu diễn dưới dạng :class:`int` hoặc :class:`float`).

      :term:`generator` này là một giải pháp thay thế cho việc lần lượt lặp qua từng response, nhằm hỗ trợ xử lý theo lô hiệu quả. Nó lấy response tiếp theo cùng với mọi response tiếp sau đang có sẵn ngay lập tức. (Ví dụ: một loạt response ``EXPUNGE`` nhanh sau khi xóa hàng loạt.)

      Yêu cầu kết nối socket; không hoạt động với các kết nối :class:`IMAP4_stream`.

      .. code-block:: pycon

         >>> with M.idle() as idler:
         ...     # lấy một response và mọi response khác theo sau trong vòng < 0.1 giây
         ...     batch = list(idler.burst())
         ...     print(f'processing {len(batch)} responses...')
         ...     print(batch)
         ...
         processing 3 responses...
         [('EXPUNGE', [b'2']), ('EXPUNGE', [b'1']), ('RECENT', [b'0'])]

      .. tip::

         Thời lượng tối đa của context ``IDLE``, được truyền vào
         :meth:`IMAP4.idle`, được tuân thủ khi chờ response đầu tiên trong một loạt. Do đó, một :class:`!Idler` đã hết hạn sẽ khiến generator này trả về ngay lập tức mà không tạo ra bất kỳ kết quả nào. Người gọi nên lưu ý điều này khi sử dụng nó trong một vòng lặp.


   .. note::

      Iterator do :meth:`IMAP4.idle` trả về chỉ có thể được sử dụng trong một
      câu lệnh :keyword:`with`. Trước hoặc sau context đó, các response không được yêu cầu sẽ được thu thập nội bộ mỗi khi một lệnh kết thúc và có thể được lấy bằng :meth:`IMAP4.response`.

   .. note::

      Tên lớp và cấu trúc của :class:`!Idler` là các interface nội bộ và có thể thay đổi. Mã gọi có thể dựa vào việc lớp này duy trì ổn định cơ chế quản lý ngữ cảnh, phép lặp và phương thức public, nhưng không nên kế thừa, khởi tạo, so sánh hoặc tham chiếu trực tiếp đến lớp này theo bất kỳ cách nào khác.

   .. versionadded:: 3.14


.. method:: IMAP4.list(directory='', pattern='*')

   Liệt kê tên các mailbox trong *directory* khớp với *pattern*.  *directory* mặc định là thư mục thư cấp cao nhất, còn *pattern* mặc định khớp với mọi thứ.  Dữ liệu trả về chứa một danh sách các phản hồi ``LIST``.


.. method:: IMAP4.login(user, password)

   Xác định client bằng mật khẩu dạng văn bản thuần túy. *password* sẽ được đặt trong dấu ngoặc kép.


.. method:: IMAP4.login_cram_md5(user, password)

   Buộc sử dụng phương thức xác thực ``CRAM-MD5`` khi xác định client để bảo vệ mật khẩu.  Chỉ hoạt động nếu phản hồi ``CAPABILITY`` của server bao gồm cụm từ ``AUTH=CRAM-MD5``.

   .. versionchanged:: 3.14
      Một :exc:`IMAP4.error` sẽ được phát sinh nếu không có hỗ trợ MD5.


.. method:: IMAP4.logout()

   Đóng kết nối tới server. Trả về phản hồi ``BYE`` của server.

   .. versionchanged:: 3.8
      Phương thức này không còn âm thầm bỏ qua các ngoại lệ tùy ý.


.. method:: IMAP4.lsub(directory='', pattern='*')

   Liệt kê tên các mailbox đã đăng ký trong thư mục khớp với mẫu. *directory* mặc định là thư mục cấp cao nhất và *pattern* mặc định khớp với mọi mailbox. Dữ liệu trả về là các tuple gồm envelope của phần thông báo và dữ liệu.


.. method:: IMAP4.myrights(mailbox)

   Hiển thị các ACL của tôi cho một mailbox (tức là các quyền mà tôi có trên mailbox đó).


.. method:: IMAP4.namespace()

   Trả về các namespace IMAP như được định nghĩa trong :rfc:`2342`.


.. method:: IMAP4.noop()

   Gửi ``NOOP`` đến server.


.. method:: IMAP4.open(host, port, timeout=None)

   Mở socket đến *port* trên *host*. Tham số tùy chọn *timeout* chỉ định thời gian chờ tính bằng giây cho lần thử kết nối. Nếu không cung cấp timeout hoặc giá trị của nó là ``None``, thời gian chờ socket mặc định toàn cục sẽ được sử dụng. Cũng lưu ý rằng nếu tham số *timeout* được đặt thành 0, phương thức sẽ raise một :class:`ValueError` để từ chối tạo socket không chặn. Phương thức này được gọi ngầm bởi constructor :class:`IMAP4`. Các đối tượng kết nối được thiết lập bởi phương thức này sẽ được sử dụng trong các phương thức :meth:`IMAP4.read`, :meth:`IMAP4.readline`, :meth:`IMAP4.send` và :meth:`IMAP4.shutdown`. Bạn có thể override phương thức này.

   .. audit-event:: imaplib.open self,host,port imaplib.IMAP4.open

   .. versionchanged:: 3.9
      Tham số *timeout* đã được thêm vào.

.. method:: IMAP4.partial(message_num, message_part, start, length)

   Lấy phần đã bị cắt ngắn của một thông báo. Dữ liệu trả về là một tuple gồm envelope của phần thông báo và dữ liệu.


.. method:: IMAP4.proxyauth(user)

   Giả định việc xác thực với tư cách *user*. Cho phép một quản trị viên được ủy quyền proxy vào mailbox của bất kỳ người dùng nào.


.. method:: IMAP4.read(size)

   Đọc *size* byte từ máy chủ từ xa. Bạn có thể ghi đè phương thức này.


.. method:: IMAP4.readline()

   Đọc một dòng từ máy chủ từ xa. Bạn có thể ghi đè phương thức này.


.. method:: IMAP4.recent()

   Yêu cầu máy chủ cập nhật. Dữ liệu trả về là ``None`` nếu không có thư mới, nếu không thì là giá trị của phản hồi ``RECENT``.


.. method:: IMAP4.rename(oldmailbox, newmailbox)

   Đổi tên mailbox có tên *oldmailbox* thành *newmailbox*.


.. method:: IMAP4.response(code)

   Trả về dữ liệu cho phản hồi *code* nếu nhận được, hoặc ``None``. Trả về code đã cho thay vì kiểu thông thường.


.. method:: IMAP4.search(charset, criterion[, ...])

   Tìm kiếm các thư khớp trong mailbox. *charset* có thể là ``None``, trong trường hợp đó sẽ không có ``CHARSET`` nào được chỉ định trong yêu cầu gửi đến máy chủ. Giao thức IMAP yêu cầu phải chỉ định ít nhất một tiêu chí; một ngoại lệ sẽ được phát sinh khi máy chủ trả về lỗi. *charset* phải là ``None`` nếu capability ``UTF8=ACCEPT`` được bật bằng lệnh :meth:`enable`.

   Ví dụ::

      # M là một instance IMAP4 đã kết nối...
      typ, msgnums = M.search(None, 'FROM', '"LDJ"')

      # hoặc:
      typ, msgnums = M.search(None, '(FROM "LDJ")')


.. method:: IMAP4.select(mailbox='INBOX', readonly=False)

   Chọn một hộp thư. Dữ liệu được trả về là số lượng thư trong *hộp thư* (``EXISTS`` phản hồi).  Hộp thư mặc định *hộp thư* là ``'INBOX'``.  Nếu cờ *chỉ đọc* được đặt, không cho phép sửa đổi hộp thư.


.. method:: IMAP4.send(data)

   Gửi ``data`` đến máy chủ từ xa. Bạn có thể ghi đè phương thức này.

   .. audit-event:: imaplib.send self,data imaplib.IMAP4.send


.. method:: IMAP4.setacl(mailbox, who, what)

   Đặt một ``ACL`` cho *hộp thư*. Phương thức này không theo tiêu chuẩn, nhưng được máy chủ ``Cyrus`` hỗ trợ.


.. method:: IMAP4.setannotation(mailbox, entry, attribute[, ...])

   Đặt các ``ANNOTATION``\ s cho *hộp thư*. Phương thức này không theo tiêu chuẩn, nhưng được máy chủ ``Cyrus`` hỗ trợ.


.. method:: IMAP4.setquota(root, limits)

   Đặt ``quota`` *root*'s resource *limits*.


.. method:: IMAP4.shutdown()

   Đóng kết nối được thiết lập trong ``open``. Phương thức này được :meth:`IMAP4.logout` gọi ngầm. Bạn có thể ghi đè phương thức này.


.. method:: IMAP4.socket()

   Trả về socket instance được dùng để kết nối với server.


.. method:: IMAP4.sort(sort_criteria, charset, search_criterion[, ...])

   Lệnh ``sort`` là một biến thể của ``search`` với ngữ nghĩa sắp xếp cho kết quả. Dữ liệu trả về chứa danh sách các số hiệu thư được phân tách bằng dấu cách.

   Sort có hai đối số trước đối số *search_criterion*; một danh sách *sort_criteria* được đặt trong ngoặc đơn và *charset* dùng để tìm kiếm. Lưu ý rằng không giống như ``search``, đối số *charset* dùng để tìm kiếm là bắt buộc. Ngoài ra còn có lệnh ``uid sort``, tương ứng với ``sort`` giống như ``uid search`` tương ứng với ``search``. Lệnh ``sort`` trước tiên tìm kiếm mailbox để tìm các thư khớp với tiêu chí tìm kiếm đã cho, sử dụng đối số charset để diễn giải các chuỗi trong tiêu chí tìm kiếm. Sau đó, lệnh trả về số hiệu của các thư khớp.

   Đây là một lệnh mở rộng ``IMAP4rev1``.


.. method:: IMAP4.starttls(ssl_context=None)

   Gửi lệnh ``STARTTLS``. Đối số *ssl_context* là tùy chọn và phải là một đối tượng :class:`ssl.SSLContext`. Điều này sẽ bật mã hóa trên kết nối IMAP. Vui lòng đọc :ref:`ssl-security` để biết các phương pháp hay nhất.

   .. note::

      Với *ssl_context* mặc định, kết nối được mã hóa nhưng chứng chỉ máy chủ và hostname không được xác minh. Để xác minh chúng, hãy truyền vào một context được tạo bởi
      :func:`ssl.create_default_context`.

   .. versionadded:: 3.2

   .. versionchanged:: 3.4
      Phương thức này hiện hỗ trợ kiểm tra hostname với
      :attr:`ssl.SSLContext.check_hostname` và *Server Name Indication* (xem
      :const:`ssl.HAS_SNI`).


.. method:: IMAP4.status(mailbox, names)

   Yêu cầu các điều kiện trạng thái được đặt tên cho *hộp thư*.


.. method:: IMAP4.store(message_set, command, flag_list)

   Thay đổi cách xử lý các cờ cho thư trong hộp thư. *lệnh* được quy định trong mục 6.4.6 của :rfc:`3501` là một trong "FLAGS", "+FLAGS" hoặc "-FLAGS", tùy chọn kèm theo hậu tố ".SILENT".

   Ví dụ: để đặt cờ xóa cho tất cả thư::

      typ, data = M.search(None, 'ALL')
      for num in data[0].split():
         M.store(num, '+FLAGS', '\\Deleted')
      M.expunge()

   .. note::

      Việc tạo các cờ chứa ký tự ']' (ví dụ: "[test]") vi phạm
      :rfc:`3501` (giao thức IMAP). Tuy nhiên, imaplib từ trước đến nay vẫn cho phép tạo các cờ như vậy, và các máy chủ IMAP phổ biến, chẳng hạn như Gmail, chấp nhận và tạo ra các cờ như vậy. Cũng có những chương trình không viết bằng Python tạo ra các cờ như vậy. Mặc dù đây là hành vi vi phạm RFC và các ứng dụng khách, máy chủ IMAP được cho là phải nghiêm ngặt, imaplib vẫn tiếp tục cho phép tạo các cờ như vậy vì lý do tương thích ngược; kể từ Python 3.6, imaplib cũng xử lý chúng nếu chúng được máy chủ gửi đến, nhờ đó cải thiện khả năng tương thích trong thực tế.

.. method:: IMAP4.subscribe(mailbox)

   Đăng ký hộp thư mới.


.. method:: IMAP4.thread(threading_algorithm, charset, search_criterion[, ...])

   Lệnh ``thread`` là một biến thể của ``search`` với ngữ nghĩa phân luồng cho các kết quả. Dữ liệu trả về chứa danh sách các thành viên của thread, được phân tách bằng dấu cách.

   Các thành viên của thread bao gồm không hoặc nhiều số thứ tự thư, được phân tách bằng dấu cách, cho biết lần lượt thư cha và thư con.

   Thread có hai đối số trước các đối số *search_criterion* tìm kiếm: một *threading_algorithm* và *charset* dùng cho việc tìm kiếm. Lưu ý rằng không giống như ``search``, đối số *charset* dùng cho việc tìm kiếm là bắt buộc. Ngoài ra còn có lệnh ``uid thread``, tương ứng với ``thread`` giống như ``uid search`` tương ứng với ``search``. Trước tiên, lệnh ``thread`` tìm kiếm trong hộp thư các thư khớp với tiêu chí tìm kiếm đã cho, sử dụng đối số *charset* để diễn giải các chuỗi trong tiêu chí tìm kiếm. Sau đó, lệnh trả về các thư khớp được phân luồng theo thuật toán phân luồng đã chỉ định.

   Đây là một lệnh mở rộng ``IMAP4rev1``.


.. method:: IMAP4.uid(command, arg[, ...])

   Thực thi các đối số của lệnh với các thư được xác định bằng UID thay vì số thứ tự thư. Trả về phản hồi phù hợp với lệnh. Phải cung cấp ít nhất một đối số; nếu không cung cấp đối số nào, máy chủ sẽ trả về lỗi và một ngoại lệ sẽ được phát sinh.


.. method:: IMAP4.unsubscribe(mailbox)

   Hủy đăng ký khỏi hộp thư cũ.

.. method:: IMAP4.unselect()

   :meth:`imaplib.IMAP4.unselect` giải phóng các tài nguyên của máy chủ liên kết với hộp thư đã chọn và đưa máy chủ trở về trạng thái đã xác thực. Lệnh này thực hiện các thao tác giống như :meth:`imaplib.IMAP4.close`, ngoại trừ việc không có thư nào bị xóa vĩnh viễn khỏi hộp thư hiện đang được chọn.

   .. versionadded:: 3.9

.. method:: IMAP4.xatom(name[, ...])

   Cho phép các lệnh mở rộng đơn giản được máy chủ thông báo trong phản hồi ``CAPABILITY``.


Các thuộc tính sau được định nghĩa trên các instance của :class:`IMAP4`:

.. attribute:: IMAP4.capabilities

   Một tuple chứa các capability do máy chủ quảng bá, viết bằng chữ hoa.

   Thuộc tính này được thiết lập khi kết nối được tạo và được làm mới sau khi :meth:`~IMAP4.login` thành công,
   :meth:`~IMAP4.authenticate` hoặc :meth:`~IMAP4.starttls`, vì máy chủ có thể quảng bá các capability khác nhau ở những trạng thái kết nối khác nhau.

   .. versionchanged:: 3.14.7
      Được làm mới sau :meth:`~IMAP4.login` và :meth:`~IMAP4.authenticate`.


.. attribute:: IMAP4.PROTOCOL_VERSION

   Giao thức được hỗ trợ mới nhất trong phản hồi ``CAPABILITY`` từ máy chủ.


.. attribute:: IMAP4.debug

   Giá trị số nguyên dùng để kiểm soát đầu ra gỡ lỗi. Giá trị khởi tạo được lấy từ biến mô-đun ``Debug``. Các giá trị lớn hơn ba sẽ theo dõi từng lệnh.


.. attribute:: IMAP4.utf8_enabled

   Giá trị Boolean thường là ``False``, nhưng được đặt thành ``True`` nếu một
   lệnh :meth:`enable` được gửi thành công cho capability ``UTF8=ACCEPT``.

   .. versionadded:: 3.5


.. _imap4-example:

Ví dụ về IMAP4
--------------

Sau đây là một ví dụ tối giản (không kiểm tra lỗi) mở một mailbox, truy xuất và in tất cả các thư::

   import getpass, imaplib

   M = imaplib.IMAP4(host='example.org')
   M.login(getpass.getuser(), getpass.getpass())
   M.select()
   typ, data = M.search(None, 'ALL')
   for num in data[0].split():
       typ, data = M.fetch(num, '(RFC822)')
       print('Message %s\n%s\n' % (num, data[0][1]))
   M.close()
   M.logout()

.. note::

   Một phản hồi ``FETCH`` có thể chứa dữ liệu bổ sung hoặc không được yêu cầu (xem :rfc:`3501`, mục 7.4.2), vì vậy mã production nên kiểm tra toàn bộ phản hồi thay vì dựa vào ``data[0][1]``.

