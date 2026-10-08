:mod:`!ftplib` --- client giao thức FTP
=======================================

.. module:: ftplib
   :synopsis: Client giao thức FTP (yêu cầu sockets).

**Mã nguồn:** :source:`Lib/ftplib.py`

.. index::
   pair: FTP; protocol
   single: FTP; ftplib (standard module)

--------------

Mô-đun này định nghĩa lớp :class:`FTP` và một vài thành phần liên quan. Lớp này
:class:`FTP` triển khai phía client của giao thức FTP. Bạn có thể sử dụng lớp này để viết các chương trình Python thực hiện nhiều tác vụ FTP tự động, chẳng hạn như mirror các FTP server khác. Mô-đun này cũng được sử dụng bởi mô-đun
:mod:`urllib.request` để xử lý các URL sử dụng FTP. Để biết thêm thông tin về FTP (File Transfer Protocol), hãy xem :rfc:`959` trên Internet.

Mã hóa mặc định là UTF-8, theo :rfc:`2640`.

.. include:: ../includes/wasm-notavail.rst

Sau đây là một phiên làm việc mẫu sử dụng mô-đun :mod:`!ftplib`::

   >>> from ftplib import FTP
   >>> ftp = FTP('ftp.us.debian.org')  # kết nối tới máy chủ, cổng mặc định
   >>> ftp.login()                     # người dùng anonymous, mật khẩu anonymous@
   '230 Login successful.'
   >>> ftp.cwd('debian')               # chuyển vào thư mục "debian"
   '250 Directory successfully changed.'
   >>> ftp.retrlines('LIST')           # liệt kê nội dung thư mục
   -rw-rw-r--    1 1176     1176         1063 Jun 15 10:18 README
   ...
   drwxr-sr-x    5 1176     1176         4096 Dec 19  2000 pool
   drwxr-sr-x    4 1176     1176         4096 Nov 17  2008 project
   drwxr-xr-x    3 1176     1176         4096 Oct 10  2012 tools
   '226 Directory send OK.'
   >>> with open('README', 'wb') as fp:
   >>>     ftp.retrbinary('RETR README', fp.write)
   '226 Transfer complete.'
   >>> ftp.quit()
   '221 Goodbye.'


.. _ftplib-reference:

Tài liệu tham khảo
------------------

.. _ftp-objects:

Đối tượng FTP
^^^^^^^^^^^^^

.. Use substitutions for some param docs so we don't need to repeat them
   in multiple places.

.. |param_doc_user| replace::Tên người dùng dùng để đăng nhập (mặc định: ``'anonymous'``).

.. |param_doc_passwd| replace::Mật khẩu dùng khi đăng nhập. Nếu không được cung cấp, và nếu *passwd* là chuỗi rỗng hoặc ``"-"``, mật khẩu sẽ được tự động tạo.

.. Ideally, we'd like to use the :rfc: directive, but Sphinx will not allow it.

.. |param_doc_acct| replace::Thông tin tài khoản được sử dụng cho lệnh FTP ``ACCT``. Rất ít hệ thống triển khai lệnh này. Xem `RFC-959 <https://datatracker.ietf.org/doc/html/rfc959.html>`__ để biết thêm chi tiết.

.. |param_doc_source_address| replace::Một bộ 2 phần tử ``(host, port)`` dành cho socket để liên kết làm địa chỉ nguồn trước khi kết nối.

.. |param_doc_encoding| replace::Mã hóa dùng cho thư mục và tên tệp (mặc định: ``'utf-8'``).

.. class:: FTP(host='', user='', passwd='', acct='', timeout=None, \
               source_address=None, *, encoding='utf-8')

   Trả về một thực thể mới của lớp :class:`FTP`.

   :param str host:Tên máy chủ cần kết nối. Nếu được cung cấp, :code:`connect(host)` sẽ được hàm khởi tạo gọi ngầm.

   :param str user:|param_doc_user| Nếu được cung cấp, :code:`login(host, passwd, acct)` sẽ được hàm khởi tạo gọi ngầm.

   :param str passwd:
      |param_doc_passwd|

   :param str acct:
      |param_doc_acct|

   :param timeout:Thời gian chờ tính bằng giây cho các thao tác blocking như :meth:`connect` (mặc định: cài đặt thời gian chờ mặc định toàn cục).
   :type timeout: float | None

   :param source_address:
      |param_doc_source_address|
   :type source_address: tuple | None

   :param str encoding:
      |param_doc_encoding|

   Lớp :class:`FTP` hỗ trợ câu lệnh :keyword:`with`, ví dụ:

    >>> from ftplib import FTP
    >>> with FTP("ftp1.at.proftpd.org") as ftp:
    ...     ftp.login()
    ...     ftp.dir()
    ... # doctest: +SKIP
    '230 Anonymous login ok, restrictions apply.'
    dr-xr-xr-x   9 ftp      ftp           154 May  6 10:43 .
    dr-xr-xr-x   9 ftp      ftp           154 May  6 10:43 ..
    dr-xr-xr-x   5 ftp      ftp          4096 May  6 10:43 CentOS
    dr-xr-xr-x   3 ftp      ftp            18 Jul 10  2008 Fedora
    >>>

   .. versionchanged:: 3.2
      Đã bổ sung hỗ trợ cho câu lệnh :keyword:`with`.

   .. versionchanged:: 3.3
      Đã bổ sung tham số *source_address*.

   .. versionchanged:: 3.9
      Nếu tham số *timeout* được đặt bằng không, tham số này sẽ phát sinh một
      :class:`ValueError` để ngăn việc tạo socket không chặn. Đã bổ sung tham số *encoding*, đồng thời thay đổi giá trị mặc định từ Latin-1 thành UTF-8 để tuân theo :rfc:`2640`.

   Một số phương thức :class:`!FTP` có sẵn dưới hai dạng: một dạng để xử lý tệp văn bản và một dạng khác để xử lý tệp nhị phân. Tên các phương thức được đặt theo lệnh được sử dụng, theo sau là ``lines`` đối với phiên bản văn bản hoặc ``binary`` đối với phiên bản nhị phân.

   Các instance :class:`FTP` có những phương thức sau:

   .. method:: FTP.set_debuglevel(level)

      Đặt mức debug của instance thành :class:`int`. Mức này kiểm soát lượng thông tin debug được in ra. Các mức debug gồm:

      * ``0`` (mặc định): Không có đầu ra debug.
      * ``1``: Tạo một lượng đầu ra debug vừa phải, thường là một dòng cho mỗi request.
      * ``2`` trở lên: Tạo lượng đầu ra debug tối đa, ghi nhật ký từng dòng được gửi và nhận trên kết nối điều khiển.

   .. method:: FTP.connect(host='', port=0, timeout=None, source_address=None)

      Kết nối đến host và port đã cho. Hàm này chỉ nên được gọi một lần cho mỗi instance; không nên gọi hàm này nếu đã cung cấp đối số *host* khi tạo :class:`FTP` instance. Tất cả các phương thức :class:`!FTP` khác chỉ có thể được gọi sau khi kết nối đã được thiết lập thành công.

      :param str host:Host cần kết nối đến.

      :param int port:TCP port cần kết nối đến (mặc định: ``21``, như được quy định trong đặc tả giao thức FTP). Hiếm khi cần chỉ định một số port khác.

      :param timeout:Thời gian chờ tính bằng giây cho lần thử kết nối (mặc định: cài đặt thời gian chờ mặc định toàn cục).
      :type timeout: float | None

      :param source_address:
         |param_doc_source_address|
      :type source_address: tuple | None

      .. audit-event:: ftplib.connect self,host,port ftplib.FTP.connect

      .. versionchanged:: 3.3
         Đã bổ sung tham số *source_address*.


   .. method:: FTP.getwelcome()

      Trả về thông báo chào mừng do máy chủ gửi để phản hồi kết nối ban đầu.  (Thông báo này đôi khi chứa tuyên bố miễn trừ trách nhiệm hoặc thông tin trợ giúp có thể liên quan đến người dùng.)


   .. method:: FTP.login(user='anonymous', passwd='', acct='')

      Đăng nhập vào máy chủ FTP đã kết nối. Hàm này chỉ nên được gọi một lần cho mỗi instance, sau khi đã thiết lập kết nối; không nên gọi hàm này nếu các đối số *host* và *user* được cung cấp khi :class:`FTP` instance được tạo. Hầu hết các lệnh FTP chỉ được phép sử dụng sau khi client đã đăng nhập.

      :param str user:
         |param_doc_user|

      :param str passwd:
         |param_doc_passwd|

      :param str acct:
         |param_doc_acct|


   .. method:: FTP.abort()

      Hủy quá trình truyền tệp đang diễn ra.  Việc sử dụng hàm này không phải lúc nào cũng hiệu quả, nhưng vẫn đáng để thử.


   .. method:: FTP.sendcmd(cmd)

      Gửi một chuỗi lệnh đơn giản đến máy chủ và trả về chuỗi phản hồi.

      .. audit-event:: ftplib.sendcmd self,cmd ftplib.FTP.sendcmd


   .. method:: FTP.voidcmd(cmd)

      Gửi một chuỗi lệnh đơn giản đến máy chủ và xử lý phản hồi. Trả về chuỗi phản hồi nếu mã phản hồi biểu thị thành công (các mã trong phạm vi 200--299). Nếu không, raise :exc:`error_reply`.

      .. audit-event:: ftplib.sendcmd self,cmd ftplib.FTP.voidcmd


   .. method:: FTP.retrbinary(cmd, callback, blocksize=8192, rest=None)

      Truy xuất một tệp ở chế độ truyền binary.

      :param str cmd:Một lệnh ``RETR`` phù hợp: :samp:`"RETR {filename}"`.

      :param callback:Một callable nhận một tham số, được gọi cho mỗi khối dữ liệu nhận được, với tham số duy nhất là dữ liệu dưới dạng :class:`bytes`.
      :type callback: :term:`callable`

      :param int blocksize:Kích thước chunk tối đa được đọc ở tầng thấp
         Đối tượng :class:`~socket.socket` được tạo để thực hiện quá trình truyền thực tế. Giá trị này cũng tương ứng với kích thước dữ liệu lớn nhất được truyền cho *callback*. Mặc định là ``8192``.

      :param int rest:Một lệnh ``REST`` sẽ được gửi đến máy chủ. Xem tài liệu về tham số *rest* của phương thức :meth:`transfercmd`.


   .. method:: FTP.retrlines(cmd, callback=None)

      Truy xuất một tệp hoặc danh sách thư mục theo encoding được chỉ định bởi tham số *encoding* khi khởi tạo. *cmd* phải là một ``RETR`` command phù hợp (xem :meth:`retrbinary`) hoặc một command như ``LIST`` hay ``NLST`` (thường chỉ là chuỗi ``'LIST'``). ``LIST`` truy xuất danh sách tệp cùng thông tin về các tệp đó. ``NLST`` truy xuất danh sách tên tệp. Hàm *callback* được gọi cho từng dòng với một đối số chuỗi chứa dòng đó sau khi loại bỏ CRLF ở cuối. *callback* mặc định in dòng đó ra :data:`sys.stdout`.


   .. method:: FTP.set_pasv(val)

      Bật chế độ "passive" nếu *val* là true; nếu không thì tắt chế độ passive. Theo mặc định, chế độ passive được bật.


   .. method:: FTP.storbinary(cmd, fp, blocksize=8192, callback=None, rest=None)

      Lưu một tệp ở chế độ truyền nhị phân.

      :param str cmd:Một ``STOR`` command phù hợp: :samp:`"STOR {filename}"`.

      :param fp:Một đối tượng tệp (được mở ở chế độ nhị phân) được đọc cho đến EOF, bằng cách sử dụng phương thức :meth:`~io.RawIOBase.read` của đối tượng theo từng khối có kích thước *blocksize* để cung cấp dữ liệu cần lưu.
      :type fp: :term:`file object`

      :param int blocksize:Kích thước khối đọc. Mặc định là ``8192``.

      :param callback:Một callable nhận một tham số, được gọi cho mỗi khối dữ liệu đã gửi, với đối số duy nhất là dữ liệu dưới dạng :class:`bytes`.
      :type callback: :term:`callable`

      :param int rest:Một lệnh ``REST`` sẽ được gửi đến máy chủ. Xem tài liệu về tham số *rest* của phương thức :meth:`transfercmd`.

      .. versionchanged:: 3.2
         Tham số *rest* đã được thêm vào.


   .. method:: FTP.storlines(cmd, fp, callback=None)

      Lưu một tệp ở chế độ dòng.  *cmd* phải là một ``STOR`` command phù hợp (xem :meth:`storbinary`).  Các dòng được đọc cho đến EOF từ
      :term:`file object` *fp* (được mở ở chế độ nhị phân) bằng phương thức :meth:`~io.IOBase.readline` của nó để cung cấp dữ liệu cần lưu.  *callback* là một callable một tham số tùy chọn, được gọi trên mỗi dòng sau khi dòng đó được gửi.


   .. method:: FTP.transfercmd(cmd, rest=None)

      Khởi tạo một lần truyền qua kết nối dữ liệu.  Nếu lần truyền đang ở chế độ active, gửi lệnh ``EPRT`` hoặc  ``PORT`` và lệnh truyền được chỉ định bởi *cmd*, rồi chấp nhận kết nối.  Nếu server ở chế độ passive, gửi lệnh ``EPSV`` hoặc ``PASV``, kết nối đến server đó và bắt đầu lệnh truyền.  Dù theo cách nào, socket của kết nối cũng được trả về.

      Nếu cung cấp *rest* tùy chọn, một lệnh ``REST`` sẽ được gửi đến server, truyền *rest* làm đối số.  *rest* thường là một offset byte trong tệp được yêu cầu, cho server biết bắt đầu gửi các byte của tệp từ offset được yêu cầu, bỏ qua các byte ban đầu.  Tuy nhiên, lưu ý rằng phương thức :meth:`transfercmd` chuyển *rest* thành một chuỗi với tham số *encoding* được chỉ định khi khởi tạo, nhưng không kiểm tra nội dung của chuỗi.  Nếu server không nhận dạng được lệnh ``REST``, một ngoại lệ :exc:`error_reply` sẽ được phát sinh.  Nếu điều này xảy ra, chỉ cần gọi :meth:`transfercmd` mà không truyền đối số *rest*.


   .. method:: FTP.ntransfercmd(cmd, rest=None)

      Tương tự như :meth:`transfercmd`, nhưng trả về một tuple gồm kết nối dữ liệu và kích thước dữ liệu dự kiến.  Nếu không thể tính kích thước dự kiến, ``None`` sẽ được trả về làm kích thước dự kiến.  *cmd* và *rest* có ý nghĩa giống như trong :meth:`transfercmd`.


   .. method:: FTP.mlsd(path="", facts=[])

      Liệt kê một thư mục theo định dạng chuẩn bằng cách sử dụng lệnh ``MLSD`` (:rfc:`3659`). Nếu bỏ qua *path* thì thư mục hiện tại sẽ được sử dụng. *facts* là danh sách các chuỗi biểu thị loại thông tin mong muốn (ví dụ: ``["type", "size", "perm"]``). Trả về một đối tượng generator, đối tượng này sinh ra một tuple gồm hai phần tử cho mỗi tệp được tìm thấy trong path. Phần tử thứ nhất là tên tệp, phần tử thứ hai là một dictionary chứa các thông tin về tên tệp. Nội dung của dictionary này có thể bị giới hạn bởi đối số *facts*, nhưng server không đảm bảo sẽ trả về tất cả thông tin được yêu cầu.

      .. versionadded:: 3.3


   .. method:: FTP.nlst(argument[, ...])

      Trả về danh sách tên tệp do lệnh ``NLST`` trả về. *argument* tùy chọn là thư mục cần liệt kê (mặc định là thư mục hiện tại trên server). Có thể sử dụng nhiều argument để truyền các tùy chọn không theo chuẩn cho lệnh ``NLST``.

      .. note:: Nếu server của bạn hỗ trợ lệnh này, :meth:`mlsd` cung cấp một API tốt hơn.


   .. method:: FTP.dir(argument[, ...])

      Tạo danh sách thư mục giống như kết quả do lệnh ``LIST`` trả về và in danh sách đó ra standard output. *argument* tùy chọn là thư mục cần liệt kê (mặc định là thư mục hiện tại trên server). Có thể sử dụng nhiều argument để truyền các tùy chọn không theo chuẩn cho lệnh ``LIST``. Nếu argument cuối cùng là một function, function đó sẽ được sử dụng làm function *callback* như đối với :meth:`retrlines`; mặc định là in ra
      :data:`sys.stdout`. Phương thức này trả về ``None``.

      .. note:: Nếu server của bạn hỗ trợ lệnh này, :meth:`mlsd` cung cấp một API tốt hơn.


   .. method:: FTP.rename(fromname, toname)

      Đổi tên tệp *fromname* trên server thành *toname*.


   .. method:: FTP.delete(filename)

      Xóa tệp có tên *filename* khỏi máy chủ. Nếu thành công, trả về nội dung của phản hồi; nếu không, phát sinh :exc:`error_perm` khi không có quyền hoặc
      :exc:`error_reply` trong các lỗi khác.


   .. method:: FTP.cwd(pathname)

      Đặt thư mục hiện tại trên máy chủ.


   .. method:: FTP.mkd(pathname)

      Tạo một thư mục mới trên máy chủ.


   .. method:: FTP.pwd()

      Trả về đường dẫn của thư mục hiện tại trên máy chủ.


   .. method:: FTP.rmd(dirname)

      Xóa thư mục có tên *dirname* trên máy chủ.


   .. method:: FTP.size(filename)

      Yêu cầu kích thước của tệp có tên *filename* trên máy chủ. Khi thành công, kích thước của tệp được trả về dưới dạng số nguyên; nếu không, ``None`` được trả về. Lưu ý rằng lệnh ``SIZE`` không được chuẩn hóa, nhưng được nhiều triển khai máy chủ phổ biến hỗ trợ.


   .. method:: FTP.quit()

      Gửi lệnh ``QUIT`` đến máy chủ và đóng kết nối. Đây là cách "lịch sự" để đóng kết nối, nhưng có thể phát sinh ngoại lệ nếu máy chủ phản hồi lỗi với lệnh ``QUIT``. Điều này ngụ ý một lệnh gọi đến
      phương thức :meth:`close`, khiến thực thể :class:`FTP` không thể sử dụng cho các lần gọi tiếp theo (xem bên dưới).


   .. method:: FTP.close()

      Đóng kết nối một cách đơn phương. Không nên áp dụng thao tác này cho một kết nối đã đóng, chẳng hạn như sau khi gọi :meth:`~FTP.quit` thành công. Sau lần gọi này, không nên sử dụng thực thể :class:`FTP` nữa (sau khi gọi :meth:`close` hoặc :meth:`~FTP.quit`, bạn không thể mở lại kết nối bằng cách gọi một phương thức :meth:`login` khác).


Các đối tượng FTP_TLS
^^^^^^^^^^^^^^^^^^^^^

.. class:: FTP_TLS(host='', user='', passwd='', acct='', *, context=None, \
                   timeout=None, source_address=None, encoding='utf-8')

   Một lớp con :class:`FTP` bổ sung hỗ trợ TLS cho FTP như được mô tả trong
   :rfc:`4217`. Kết nối đến cổng 21, ngầm bảo mật kết nối điều khiển FTP trước khi xác thực.

   .. note::
      Người dùng phải chủ động bảo mật kết nối dữ liệu bằng cách gọi phương thức :meth:`prot_p`.

   :param str host:Tên máy chủ cần kết nối. Nếu được cung cấp, :code:`connect(host)` sẽ được gọi ngầm bởi hàm khởi tạo.

   :param str user:|param_doc_user| Nếu được cung cấp, :code:`login(host, passwd, acct)` sẽ được gọi ngầm bởi hàm khởi tạo.

   :param str passwd:
      |param_doc_passwd|

   :param str acct:
      |param_doc_acct|

   :param context:Một đối tượng SSL context cho phép đóng gói các tùy chọn cấu hình SSL, chứng chỉ và khóa riêng vào một cấu trúc duy nhất, có khả năng tồn tại trong thời gian dài. Vui lòng đọc :ref:`ssl-security` để biết các phương pháp hay nhất.
   :type context: :class:`ssl.SSLContext`

   :param timeout:Thời gian chờ tính bằng giây cho các thao tác chặn như :meth:`~FTP.connect` (mặc định: cài đặt thời gian chờ mặc định toàn cục).
   :type timeout: float | None

   :param source_address:
      |param_doc_source_address|
   :type source_address: tuple | None

   :param str encoding:
      |param_doc_encoding|

   .. versionadded:: 3.2

   .. versionchanged:: 3.3
      Đã thêm tham số *source_address*.

   .. versionchanged:: 3.4
      Lớp này hiện hỗ trợ kiểm tra hostname với
      :attr:`ssl.SSLContext.check_hostname` và *Server Name Indication* (xem
      :const:`ssl.HAS_SNI`).

   .. versionchanged:: 3.9
      Nếu tham số *timeout* được đặt thành 0, tham số này sẽ phát sinh một
      :class:`ValueError` để ngăn việc tạo socket không blocking. Tham số *encoding* đã được thêm vào và giá trị mặc định đã được đổi từ Latin-1 thành UTF-8 để tuân theo :rfc:`2640`.

   .. versionchanged:: 3.12
      Các tham số *keyfile* và *certfile* không được khuyến nghị dùng nữa đã bị xóa.

   Sau đây là một phiên làm việc mẫu sử dụng lớp :class:`FTP_TLS`::

      >>> ftps = FTP_TLS('ftp.pureftpd.org')
      >>> ftps.login()
      '230 Anonymous user logged in'
      >>> ftps.prot_p()
      '200 Data protection level set to "private"'
      >>> ftps.nlst()
      ['6jack', 'OpenBSD', 'antilink', 'blogbench', 'bsdcam', 'clockspeed', 'djbdns-jedi', 'docs', 'eaccelerator-jedi', 'favicon.ico', 'francotone', 'fugu', 'ignore', 'libpuzzle', 'metalog', 'minidentd', 'misc', 'mysql-udf-global-user-variables', 'php-jenkins-hash', 'php-skein-hash', 'php-webdav', 'phpaudit', 'phpbench', 'pincaster', 'ping', 'posto', 'pub', 'public', 'public_keys', 'pure-ftpd', 'qscan', 'qtc', 'sharedance', 'skycache', 'sound', 'tmp', 'ucarp']

   Lớp :class:`!FTP_TLS` kế thừa từ :class:`FTP`, định nghĩa các phương thức và thuộc tính bổ sung sau:

   .. attribute:: FTP_TLS.ssl_version

      Phiên bản SSL sẽ sử dụng (mặc định là :data:`ssl.PROTOCOL_SSLv23`).

   .. method:: FTP_TLS.auth()

      Thiết lập kết nối điều khiển bảo mật bằng TLS hoặc SSL, tùy thuộc vào nội dung được chỉ định trong thuộc tính :attr:`ssl_version`.

      .. versionchanged:: 3.4
         Phương thức hiện hỗ trợ kiểm tra hostname với
         :attr:`ssl.SSLContext.check_hostname` và *Server Name Indication* (xem
         :const:`ssl.HAS_SNI`).

   .. method:: FTP_TLS.ccc()

      Đưa kênh điều khiển trở lại dạng văn bản thuần túy. Điều này có thể hữu ích để tận dụng các tường lửa biết cách xử lý NAT với FTP không bảo mật mà không cần mở các cổng cố định.

      .. versionadded:: 3.3

   .. method:: FTP_TLS.prot_p()

      Thiết lập kết nối dữ liệu bảo mật.

   .. method:: FTP_TLS.prot_c()

      Thiết lập kết nối dữ liệu văn bản rõ ràng.


Các biến mô-đun
^^^^^^^^^^^^^^^

.. exception:: error_reply

   Ngoại lệ được phát sinh khi nhận được phản hồi không mong đợi từ máy chủ.


.. exception:: error_temp

   Ngoại lệ được phát sinh khi nhận được mã lỗi biểu thị lỗi tạm thời (mã phản hồi trong phạm vi 400--499).


.. exception:: error_perm

   Ngoại lệ được phát sinh khi nhận được mã lỗi biểu thị lỗi vĩnh viễn (mã phản hồi trong phạm vi 500--599).


.. exception:: error_proto

   Ngoại lệ được phát sinh khi nhận được phản hồi từ máy chủ không phù hợp với các đặc tả phản hồi của File Transfer Protocol, tức là không bắt đầu bằng một chữ số trong phạm vi 1--5.


.. data:: all_errors

   Tập hợp tất cả các ngoại lệ (dưới dạng một tuple) mà các phương thức của các instance :class:`FTP` có thể phát sinh do các vấn đề với kết nối FTP (trái với các lỗi lập trình do bên gọi gây ra). Tập hợp này bao gồm bốn ngoại lệ được liệt kê ở trên, cũng như :exc:`OSError` và :exc:`EOFError`.


.. seealso::

   Mô-đun :mod:`netrc`
      Trình phân tích cú pháp cho định dạng tệp :file:`.netrc`. Tệp :file:`.netrc` thường được các FTP client sử dụng để tải thông tin xác thực của người dùng trước khi nhắc người dùng nhập.
