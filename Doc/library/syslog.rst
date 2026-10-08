:mod:`!syslog` --- Các thủ tục thư viện Unix syslog
===================================================

.. module:: syslog
   :synopsis: Giao diện cho các thủ tục thư viện Unix syslog.

--------------

Mô-đun này cung cấp giao diện cho các thủ tục thư viện Unix ``syslog``. Tham khảo các trang hướng dẫn sử dụng Unix để biết mô tả chi tiết về cơ chế ``syslog``.

.. availability:: Unix, not WASI, not iOS.

Mô-đun này bao bọc nhóm thủ tục ``syslog`` của hệ thống. Một thư viện Python thuần có thể giao tiếp với máy chủ syslog có sẵn trong
mô-đun :mod:`logging.handlers` dưới dạng :class:`~logging.handlers.SysLogHandler`.

Mô-đun định nghĩa các hàm sau:


.. function:: syslog(message)
              syslog(priority, message)

   Gửi chuỗi *message* đến system logger. Một ký tự xuống dòng ở cuối sẽ được thêm vào nếu cần. Mỗi thông báo được gắn thẻ bằng một priority bao gồm *facility* và *level*. Đối số *priority* tùy chọn, mặc định là :const:`LOG_INFO`, xác định priority của thông báo. Nếu facility không được mã hóa trong *priority* bằng phép logical-or (``LOG_INFO | LOG_USER``), thì giá trị được cung cấp trong lệnh gọi :func:`openlog` sẽ được sử dụng.

   Nếu :func:`openlog` chưa được gọi trước lệnh gọi :func:`syslog`,
   :func:`openlog` sẽ được gọi mà không có đối số.

   .. audit-event:: syslog.syslog priority,message syslog.syslog

   .. versionchanged:: 3.2
      Trong các phiên bản trước, :func:`openlog` sẽ không được tự động gọi nếu chưa được gọi trước lệnh gọi :func:`syslog`, mà để việc triển khai syslog gọi ``openlog()``.

   .. versionchanged:: 3.12
      Hàm này bị giới hạn trong các subinterpreter. (Chỉ mã chạy trong nhiều interpreter bị ảnh hưởng; giới hạn này không liên quan đến hầu hết người dùng.)
      Phải gọi :func:`openlog` trong main interpreter trước khi có thể sử dụng :func:`syslog` trong một subinterpreter. Nếu không, hàm sẽ raise :exc:`RuntimeError`.


.. function:: openlog([ident[, logoption[, facility]]])

   Có thể thiết lập các tùy chọn logging của những lệnh gọi :func:`syslog` tiếp theo bằng cách gọi
   :func:`openlog`.  :func:`syslog` sẽ gọi :func:`openlog` không có đối số nếu nhật ký hiện chưa được mở.

   Đối số từ khóa *ident* tùy chọn là một chuỗi được thêm vào trước mọi thông báo và mặc định là ``sys.argv[0]`` sau khi loại bỏ các thành phần đường dẫn ở đầu.  Đối số từ khóa *logoption* tùy chọn (mặc định là 0) là một trường bit -- xem bên dưới để biết các giá trị có thể kết hợp.  Đối số từ khóa *facility* tùy chọn (mặc định là :const:`LOG_USER`) đặt facility mặc định cho các thông báo không được mã hóa facility rõ ràng.

   .. audit-event:: syslog.openlog ident,logoption,facility syslog.openlog

   .. versionchanged:: 3.2
      Trong các phiên bản trước, không được phép sử dụng đối số từ khóa và *ident* là bắt buộc.

   .. versionchanged:: 3.12
      Hàm này bị hạn chế trong các subinterpreter. (Chỉ mã chạy trong nhiều interpreter mới bị ảnh hưởng; hạn chế này không liên quan đến hầu hết người dùng.) Hàm này chỉ có thể được gọi trong interpreter chính. Hàm sẽ phát sinh :exc:`RuntimeError` nếu được gọi trong một subinterpreter.


.. function:: closelog()

   Đặt lại các giá trị của module syslog và gọi ``closelog()`` của thư viện hệ thống.

   Điều này khiến module hoạt động như khi mới được import.  Ví dụ, :func:`openlog` sẽ được gọi trong lần gọi :func:`syslog` đầu tiên (nếu
   :func:`openlog` chưa được gọi), còn *ident* và các
   Các tham số :func:`openlog` được đặt lại về giá trị mặc định.

   .. audit-event:: syslog.closelog "" syslog.closelog

   .. versionchanged:: 3.12
      Hàm này bị hạn chế trong các subinterpreter. (Chỉ mã chạy trong nhiều interpreter mới bị ảnh hưởng; hạn chế này không liên quan đến hầu hết người dùng.) Hàm này chỉ có thể được gọi trong interpreter chính. Hàm sẽ phát sinh :exc:`RuntimeError` nếu được gọi trong một subinterpreter.


.. function:: setlogmask(maskpri)

   Đặt mặt nạ mức độ ưu tiên thành *maskpri* và trả về giá trị mặt nạ trước đó. Các lệnh gọi đến :func:`syslog` với mức độ ưu tiên không được thiết lập trong *maskpri* sẽ bị bỏ qua. Mặc định là ghi nhật ký tất cả các mức độ ưu tiên. Hàm ``LOG_MASK(pri)`` tính mặt nạ cho mức độ ưu tiên riêng lẻ *pri*. Hàm ``LOG_UPTO(pri)`` tính mặt nạ cho tất cả các mức độ ưu tiên lên đến và bao gồm *pri*.

   .. audit-event:: syslog.setlogmask maskpri syslog.setlogmask

Mô-đun định nghĩa các hằng số sau:


.. data:: LOG_EMERG
          LOG_ALERT LOG_CRIT LOG_ERR LOG_WARNING LOG_NOTICE LOG_INFO LOG_DEBUG

   Các mức độ ưu tiên (từ cao đến thấp).


.. data:: LOG_AUTH
          LOG_AUTHPRIV LOG_CRON LOG_DAEMON LOG_FTP LOG_INSTALL LOG_KERN LOG_LAUNCHD LOG_LPR LOG_MAIL LOG_NETINFO LOG_NEWS LOG_RAS LOG_REMOTEAUTH LOG_SYSLOG LOG_USER LOG_UUCP LOG_LOCAL0 LOG_LOCAL1 LOG_LOCAL2 LOG_LOCAL3 LOG_LOCAL4 LOG_LOCAL5 LOG_LOCAL6 LOG_LOCAL7

   Các facility, tùy thuộc vào tính khả dụng trong ``<syslog.h>`` đối với :const:`LOG_AUTHPRIV`,
   :const:`LOG_FTP`, :const:`LOG_NETINFO`, :const:`LOG_REMOTEAUTH`,
   :const:`LOG_INSTALL` và :const:`LOG_RAS`.

   .. versionchanged:: 3.13
       Đã bổ sung :const:`LOG_FTP`, :const:`LOG_NETINFO`, :const:`LOG_REMOTEAUTH`,
       :const:`LOG_INSTALL`, :const:`LOG_RAS` và :const:`LOG_LAUNCHD`.

.. data:: LOG_PID
          LOG_CONS LOG_NDELAY LOG_ODELAY LOG_NOWAIT LOG_PERROR

   Các tùy chọn log, tùy thuộc vào tính khả dụng trong ``<syslog.h>`` đối với
   :const:`LOG_ODELAY`, :const:`LOG_NOWAIT` và :const:`LOG_PERROR`.


Ví dụ
-----

Ví dụ đơn giản
~~~~~~~~~~~~~~

Một tập hợp ví dụ đơn giản::

   import syslog

   syslog.syslog('Processing started')
   if error:
       syslog.syslog(syslog.LOG_ERR, 'Processing started')

Ví dụ về cách thiết lập một số tùy chọn log; các tùy chọn này sẽ bao gồm ID của tiến trình trong các thông báo được ghi log và ghi các thông báo vào facility đích được dùng để ghi log thư::

   syslog.openlog(logoption=syslog.LOG_PID, facility=syslog.LOG_MAIL)
   syslog.syslog('E-mail processing initiated...')
