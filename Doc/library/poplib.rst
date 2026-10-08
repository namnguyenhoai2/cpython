:mod:`!poplib` --- ứng dụng khách giao thức POP3
================================================

.. module:: poplib
   :synopsis: Ứng dụng khách giao thức POP3 (yêu cầu sockets).

.. sectionauthor:: Andrew T. Csillag
.. revised by ESR, January 2000

**Mã nguồn:** :source:`Lib/poplib.py`

.. index:: pair: POP3; protocol

--------------

Mô-đun này định nghĩa một lớp, :class:`POP3`, đóng gói một kết nối đến máy chủ POP3 và triển khai giao thức được định nghĩa trong :rfc:`1939`. Lớp này
:class:`POP3` hỗ trợ cả tập lệnh tối thiểu và tùy chọn từ
:rfc:`1939`. Lớp :class:`POP3` cũng hỗ trợ lệnh ``STLS`` được giới thiệu trong :rfc:`2595` để bật giao tiếp được mã hóa trên một kết nối đã thiết lập.

Ngoài ra, mô-đun này cung cấp một lớp :class:`POP3_SSL`, hỗ trợ kết nối đến các máy chủ POP3 sử dụng SSL làm lớp giao thức bên dưới.

Lưu ý rằng POP3, dù được hỗ trợ rộng rãi, đã lỗi thời. Chất lượng triển khai của các POP3 server rất khác nhau, và có quá nhiều server khá kém. Nếu mailserver của bạn hỗ trợ IMAP, bạn nên sử dụng
:class:`imaplib.IMAP4` class, vì các IMAP server thường được triển khai tốt hơn.

.. include:: ../includes/wasm-notavail.rst

Module :mod:`!poplib` cung cấp hai class:


.. class:: POP3(host, port=POP3_PORT[, timeout])

   Class này triển khai giao thức POP3 thực tế. Kết nối được tạo khi instance được khởi tạo. Nếu *port* bị bỏ qua, cổng POP3 tiêu chuẩn (110) sẽ được sử dụng. Tham số *timeout* tùy chọn chỉ định thời gian chờ tính bằng giây cho lần thử kết nối (nếu không được chỉ định, thiết lập thời gian chờ mặc định toàn cục sẽ được sử dụng).

   .. audit-event:: poplib.connect self,host,port poplib.POP3

   .. audit-event:: poplib.putline self,line poplib.POP3

      Tất cả các lệnh sẽ phát sinh một :ref:`auditing event <auditing>` ``poplib.putline`` với các đối số ``self`` và ``line``, trong đó ``line`` là các byte sắp được gửi đến máy chủ từ xa.

   .. versionchanged:: 3.9
      Nếu tham số *timeout* được đặt bằng không, nó sẽ phát sinh một
      :class:`ValueError` để ngăn việc tạo socket không chặn.

.. class:: POP3_SSL(host, port=POP3_SSL_PORT, *, timeout=None, context=None)

   Đây là một lớp con của :class:`POP3` kết nối với máy chủ qua một socket được mã hóa bằng SSL. Nếu *port* không được chỉ định, cổng 995, cổng POP3-over-SSL tiêu chuẩn, sẽ được sử dụng. *timeout* hoạt động như trong constructor :class:`POP3`. *context* là một đối tượng :class:`ssl.SSLContext` tùy chọn, cho phép gộp các tùy chọn cấu hình SSL, chứng chỉ và khóa riêng vào một cấu trúc duy nhất (có thể tồn tại lâu dài). Vui lòng đọc :ref:`ssl-security` để biết các phương pháp hay nhất.

   .. audit-event:: poplib.connect self,host,port poplib.POP3_SSL

   .. audit-event:: poplib.putline self,line poplib.POP3_SSL

      Tất cả các lệnh sẽ phát sinh một :ref:`auditing event <auditing>` ``poplib.putline`` với các đối số ``self`` và ``line``, trong đó ``line`` là các byte sắp được gửi đến máy chủ từ xa.

   .. versionchanged:: 3.2
      Đã thêm tham số *context*.

   .. versionchanged:: 3.4
      Lớp này hiện hỗ trợ kiểm tra hostname bằng
      :attr:`ssl.SSLContext.check_hostname` và *Server Name Indication* (xem
      :const:`ssl.HAS_SNI`).

   .. versionchanged:: 3.9
      Nếu tham số *timeout* được đặt bằng không, nó sẽ phát sinh một
      :class:`ValueError` để ngăn việc tạo socket không chặn.

   .. versionchanged:: 3.12
      Các tham số *keyfile* và *certfile* đã không còn được dùng và đã bị loại bỏ.

Một ngoại lệ được định nghĩa dưới dạng thuộc tính của mô-đun :mod:`!poplib`:.


.. exception:: error_proto

   Ngoại lệ được phát sinh khi có bất kỳ lỗi nào từ mô-đun này (các lỗi từ mô-đun :mod:`socket` không bị bắt). Nguyên nhân của ngoại lệ được truyền vào hàm khởi tạo dưới dạng một chuỗi.


.. seealso::

   Mô-đun :mod:`imaplib`
      Mô-đun IMAP chuẩn của Python.

   `Các câu hỏi thường gặp về Fetchmail <http://www.catb.org/~esr/fetchmail/fetchmail-FAQ.html>`_
      FAQ dành cho ứng dụng client POP/IMAP :program:`fetchmail` tập hợp thông tin về các biến thể của máy chủ POP3 và những trường hợp không tuân thủ RFC, có thể hữu ích nếu bạn cần viết một ứng dụng dựa trên giao thức POP.


.. _pop3-objects:

Đối tượng POP3
--------------

Tất cả các lệnh POP3 đều được biểu diễn bằng các phương thức cùng tên, viết thường; hầu hết đều trả về văn bản phản hồi do máy chủ gửi.

Một instance :class:`POP3` có các phương thức sau:


.. method:: POP3.set_debuglevel(level)

   Thiết lập mức độ debugging của instance. Mức này kiểm soát lượng thông tin debugging được in ra. Giá trị mặc định, ``0``, không tạo ra thông tin debugging. Giá trị ``1`` tạo ra lượng thông tin debugging vừa phải, thường là một dòng cho mỗi request. Giá trị ``2`` trở lên tạo ra lượng thông tin debugging tối đa, ghi lại từng dòng được gửi và nhận trên kết nối điều khiển.


.. method:: POP3.getwelcome()

   Trả về chuỗi lời chào do máy chủ POP3 gửi.


.. method:: POP3.capa()

   Truy vấn các khả năng của máy chủ như được chỉ định trong :rfc:`2449`. Trả về một dictionary có dạng ``{'name': ['param'...]}``.

   .. versionadded:: 3.4


.. method:: POP3.user(username)

   Gửi lệnh user; phản hồi phải cho biết rằng cần có mật khẩu.


.. method:: POP3.pass_(password)

   Gửi mật khẩu, phản hồi bao gồm số lượng thư và kích thước hộp thư. Lưu ý: hộp thư trên máy chủ sẽ bị khóa cho đến khi :meth:`~POP3.quit` được gọi.


.. method:: POP3.apop(user, secret)

   Sử dụng xác thực APOP bảo mật hơn để đăng nhập vào máy chủ POP3.


.. method:: POP3.rpop(user)

   Sử dụng xác thực RPOP (tương tự các lệnh r- của UNIX) để đăng nhập vào máy chủ POP3.


.. method:: POP3.stat()

   Lấy trạng thái hộp thư. Kết quả là một tuple gồm 2 số nguyên: ``(message count, mailbox size)``.


.. method:: POP3.list([which])

   Yêu cầu danh sách thư, kết quả có dạng ``(response, ['mesg_num octets', ...], octets)``. Nếu *which* được thiết lập, đó là thư cần liệt kê.


.. method:: POP3.retr(which)

   Lấy toàn bộ thư có số *which*, đồng thời đặt cờ đã đọc cho thư đó. Kết quả có dạng ``(response, ['line', ...], octets)``.


.. method:: POP3.dele(which)

   Đánh dấu thư có số *which* để xóa. Trên hầu hết máy chủ, thư không thực sự bị xóa cho đến khi QUIT (ngoại lệ lớn là Eudora QPOP, vốn cố tình vi phạm các RFC bằng cách thực hiện các thao tác xóa đang chờ trong mọi lần ngắt kết nối).


.. method:: POP3.rset()

   Xóa mọi dấu đánh dấu xóa khỏi mailbox.


.. method:: POP3.noop()

   Không làm gì cả. Có thể được dùng để duy trì kết nối.


.. method:: POP3.quit()

   Đăng xuất: commit các thay đổi, mở khóa mailbox, ngắt kết nối.


.. method:: POP3.top(which, howmuch)

   Truy xuất phần header của message cùng với *howmuch* dòng của message sau header của message số *which*. Kết quả có dạng ``(response, ['line', ...], octets)``.

   Lệnh POP3 TOP mà method này sử dụng, không giống lệnh RETR, không đặt cờ đã xem của message; đáng tiếc là TOP được đặc tả chưa đầy đủ trong các RFC và thường bị lỗi trên các server không chính hãng. Hãy kiểm thử method này thủ công với các server POP3 bạn sẽ sử dụng trước khi tin cậy nó.


.. method:: POP3.uidl(which=None)

   Trả về danh sách digest (ID duy nhất) của các message. Nếu chỉ định *which*, kết quả chứa ID duy nhất của message đó theo dạng ``'response mesgnum uid``; nếu không, kết quả là danh sách ``(response, ['mesgnum uid', ...], octets)``.


.. method:: POP3.utf8()

   Thử chuyển sang chế độ UTF-8. Trả về phản hồi của server nếu thành công; nếu không, phát sinh :class:`error_proto`. Được đặc tả trong :RFC:`6856`.

   .. versionadded:: 3.5


.. method:: POP3.stls(context=None)

   Bắt đầu một phiên TLS trên kết nối đang hoạt động như được chỉ định trong :rfc:`2595`. Điều này chỉ được phép thực hiện trước khi xác thực người dùng

   Tham số *context* là một đối tượng :class:`ssl.SSLContext`, cho phép gộp các tùy chọn cấu hình SSL, chứng chỉ và khóa riêng vào một cấu trúc duy nhất (có thể tồn tại trong thời gian dài). Vui lòng đọc :ref:`ssl-security` để biết các phương pháp hay nhất.

   Phương thức này hỗ trợ kiểm tra hostname thông qua
   :attr:`ssl.SSLContext.check_hostname` và *Server Name Indication* (xem
   :const:`ssl.HAS_SNI`).

   .. versionadded:: 3.4


Các instance của :class:`POP3_SSL` không có phương thức bổ sung nào. Giao diện của subclass này giống hệt giao diện của lớp cha.


.. _pop3-example:

Ví dụ về POP3
-------------

Sau đây là một ví dụ tối giản (không kiểm tra lỗi) mở một hộp thư, sau đó truy xuất và in tất cả thư::

   import getpass, poplib

   M = poplib.POP3('localhost')
   M.user(getpass.getuser())
   M.pass_(getpass.getpass())
   numMessages = len(M.list()[1])
   for i in range(numMessages):
       for j in M.retr(i+1)[1]:
           print(j)

Ở cuối module có một phần kiểm thử chứa ví dụ sử dụng chi tiết hơn.

.. _`Frequently Asked Questions About Fetchmail`: http://www.catb.org/~esr/fetchmail/fetchmail-FAQ.html
