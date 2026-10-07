:mod:`!errno` --- Ký hiệu hệ thống errno tiêu chuẩn
===================================================

.. module:: errno
   :synopsis: Ký hiệu hệ thống errno tiêu chuẩn.

----------------

Mô-đun này cung cấp các ký hiệu hệ thống ``errno`` tiêu chuẩn. Giá trị của mỗi ký hiệu là giá trị số nguyên tương ứng. Tên và mô tả được lấy từ :file:`linux/include/errno.h`, vốn được cho là bao quát đầy đủ.


.. data:: errorcode

   Từ điển cung cấp ánh xạ từ giá trị errno tới tên chuỗi trong hệ thống bên dưới. Ví dụ: ``errno.errorcode[errno.EPERM]`` ánh xạ tới ``'EPERM'``.

Để chuyển mã lỗi dạng số thành thông báo lỗi, hãy sử dụng :func:`os.strerror`.

Trong danh sách sau, các ký hiệu không được sử dụng trên nền tảng hiện tại sẽ không được mô-đun định nghĩa. Danh sách cụ thể các ký hiệu được định nghĩa có tại ``errno.errorcode.keys()``. Các ký hiệu khả dụng có thể bao gồm:


.. data:: EPERM

   Không được phép thực hiện thao tác. Lỗi này được ánh xạ tới ngoại lệ
   :exc:`PermissionError`.


.. data:: ENOENT

   Không có tệp hoặc thư mục như vậy. Lỗi này được ánh xạ tới exception
   :exc:`FileNotFoundError`.


.. data:: ESRCH

   Không có tiến trình như vậy. Lỗi này được ánh xạ tới exception
   :exc:`ProcessLookupError`.


.. data:: EINTR

   Lời gọi hệ thống bị gián đoạn. Lỗi này được ánh xạ tới exception
   :exc:`InterruptedError`.


.. data:: EIO

   Lỗi I/O


.. data:: ENXIO

   Không có thiết bị hoặc địa chỉ như vậy


.. data:: E2BIG

   Danh sách đối số quá dài


.. data:: ENOEXEC

   Lỗi định dạng Exec


.. data:: EBADF

   Số hiệu tệp không hợp lệ


.. data:: ECHILD

   Không có tiến trình con. Lỗi này được ánh xạ tới ngoại lệ
   :exc:`ChildProcessError`.


.. data:: EAGAIN

   Hãy thử lại. Lỗi này được ánh xạ tới ngoại lệ :exc:`BlockingIOError`.


.. data:: ENOMEM

   Không đủ bộ nhớ


.. data:: EACCES

   Bị từ chối quyền truy cập. Lỗi này được ánh xạ tới ngoại lệ
   :exc:`PermissionError`.


.. data:: EFAULT

   Địa chỉ không hợp lệ


.. data:: ENOTBLK

   Yêu cầu thiết bị khối


.. data:: EBUSY

   Thiết bị hoặc tài nguyên đang bận


.. data:: EEXIST

   Tệp đã tồn tại. Lỗi này được ánh xạ tới ngoại lệ
   :exc:`FileExistsError`.


.. data:: EXDEV

   Liên kết giữa các thiết bị


.. data:: ENODEV

   Không có thiết bị như vậy


.. data:: ENOTDIR

   Không phải là thư mục. Lỗi này được ánh xạ tới ngoại lệ
   :exc:`NotADirectoryError`.


.. data:: EISDIR

   Là một thư mục. Lỗi này được ánh xạ tới ngoại lệ
   :exc:`IsADirectoryError`.


.. data:: EINVAL

   Đối số không hợp lệ


.. data:: ENFILE

   Tràn bảng tệp


.. data:: EMFILE

   Quá nhiều tệp đang mở


.. data:: ENOTTY

   Không phải máy đánh chữ


.. data:: ETXTBSY

   Tệp văn bản đang bận


.. data:: EFBIG

   Tệp quá lớn


.. data:: ENOSPC

   Thiết bị không còn chỗ trống


.. data:: ESPIPE

   Thao tác seek không hợp lệ


.. data:: EROFS

   Hệ thống tệp chỉ đọc


.. data:: EMLINK

   Quá nhiều liên kết


.. data:: EPIPE

   Đường ống bị hỏng. Lỗi này được ánh xạ tới ngoại lệ
   :exc:`BrokenPipeError`.


.. data:: EDOM

   Đối số toán học nằm ngoài miền của hàm


.. data:: ERANGE

   Kết quả toán học không thể biểu diễn


.. data:: EDEADLK

   Sẽ xảy ra deadlock tài nguyên


.. data:: ENAMETOOLONG

   Tên tệp quá dài


.. data:: ENOLCK

   Không có khóa bản ghi nào khả dụng


.. data:: ENOSYS

   Hàm chưa được triển khai


.. data:: ENOTEMPTY

   Thư mục không trống


.. data:: ELOOP

   Đã gặp quá nhiều liên kết tượng trưng


.. data:: EWOULDBLOCK

   Thao tác sẽ bị chặn. Lỗi này được ánh xạ tới ngoại lệ
   :exc:`BlockingIOError`.


.. data:: ENOMSG

   Không có thông báo thuộc loại mong muốn


.. data:: EIDRM

   Mã định danh đã bị xóa


.. data:: ECHRNG

   Số kênh nằm ngoài phạm vi


.. data:: EL2NSYNC

   Tầng 2 chưa được đồng bộ hóa


.. data:: EL3HLT

   Tầng 3 đã dừng


.. data:: EL3RST

   Tầng 3 đã được đặt lại


.. data:: ELNRNG

   Số liên kết nằm ngoài phạm vi


.. data:: EUNATCH

   Trình điều khiển giao thức chưa được gắn kết


.. data:: ENOCSI

   Không có cấu trúc CSI khả dụng


.. data:: EL2HLT

   Cấp 2 đã dừng


.. data:: EBADE

   Trao đổi không hợp lệ


.. data:: EBADR

   Bộ mô tả yêu cầu không hợp lệ


.. data:: EXFULL

   Trao đổi đã đầy


.. data:: ENOANO

   Không có cực dương


.. data:: EBADRQC

   Mã yêu cầu không hợp lệ


.. data:: EBADSLT

   Slot không hợp lệ


.. data:: EDEADLOCK

   Lỗi deadlock khi khóa tệp


.. data:: EBFONT

   Định dạng tệp phông chữ không hợp lệ


.. data:: ENOSTR

   Thiết bị không phải là stream


.. data:: ENODATA

   Không có dữ liệu


.. data:: ETIME

   Bộ hẹn giờ đã hết hạn


.. data:: ENOSR

   Hết tài nguyên stream


.. data:: ENONET

   Máy không kết nối mạng


.. data:: ENOPKG

   Gói chưa được cài đặt


.. data:: EREMOTE

   Đối tượng ở xa


.. data:: ENOLINK

   Liên kết đã bị ngắt


.. data:: EADV

   Lỗi quảng bá


.. data:: ESRMNT

   Lỗi Srmount


.. data:: ECOMM

   Lỗi giao tiếp khi gửi


.. data:: EPROTO

   Lỗi giao thức


.. data:: EMULTIHOP

   Đã thử multihop


.. data:: EDOTDOT

   Lỗi cụ thể của RFS


.. data:: EBADMSG

   Không phải thông báo dữ liệu


.. data:: EOVERFLOW

   Giá trị quá lớn đối với kiểu dữ liệu đã định nghĩa


.. data:: ENOTUNIQ

   Tên không duy nhất trên mạng


.. data:: EBADFD

   File descriptor ở trạng thái không hợp lệ


.. data:: EREMCHG

   Địa chỉ từ xa đã thay đổi


.. data:: ELIBACC

   Không thể truy cập thư viện dùng chung cần thiết


.. data:: ELIBBAD

   Đang truy cập thư viện dùng chung bị hỏng


.. data:: ELIBSCN

   Phần .lib trong a.out bị hỏng


.. data:: ELIBMAX

   Đang cố gắng liên kết quá nhiều thư viện dùng chung


.. data:: ELIBEXEC

   Không thể thực thi trực tiếp một thư viện dùng chung


.. data:: EILSEQ

   Chuỗi byte không hợp lệ


.. data:: ERESTART

   Cuộc gọi hệ thống bị gián đoạn nên được khởi động lại


.. data:: ESTRPIPE

   Lỗi pipe của stream


.. data:: EUSERS

   Quá nhiều người dùng


.. data:: ENOTSOCK

   Thao tác socket trên đối tượng không phải socket


.. data:: EDESTADDRREQ

   Yêu cầu địa chỉ đích


.. data:: EMSGSIZE

   Thông báo quá dài


.. data:: EPROTOTYPE

   Giao thức không đúng loại cho socket


.. data:: ENOPROTOOPT

   Giao thức không khả dụng


.. data:: EPROTONOSUPPORT

   Giao thức không được hỗ trợ


.. data:: ESOCKTNOSUPPORT

   Kiểu socket không được hỗ trợ


.. data:: EOPNOTSUPP

   Thao tác không được hỗ trợ trên endpoint truyền tải


.. data:: ENOTSUP

   Thao tác không được hỗ trợ

   .. versionadded:: 3.2


.. data:: EPFNOSUPPORT

   Họ giao thức không được hỗ trợ


.. data:: EAFNOSUPPORT

   Họ địa chỉ không được giao thức hỗ trợ


.. data:: EADDRINUSE

   Địa chỉ đã được sử dụng


.. data:: EADDRNOTAVAIL

   Không thể gán địa chỉ được yêu cầu


.. data:: ENETDOWN

   Mạng không hoạt động


.. data:: ENETUNREACH

   Không thể truy cập mạng


.. data:: ENETRESET

   Mạng đã ngắt kết nối do bị đặt lại


.. data:: ECONNABORTED

   Phần mềm đã khiến kết nối bị hủy bỏ. Lỗi này được ánh xạ tới ngoại lệ :exc:`ConnectionAbortedError`.


.. data:: ECONNRESET

   Kết nối đã bị máy ngang hàng đặt lại. Lỗi này được ánh xạ tới ngoại lệ
   :exc:`ConnectionResetError`.


.. data:: ENOBUFS

   Không còn dung lượng bộ đệm


.. data:: EISCONN

   Điểm cuối truyền tải đã được kết nối


.. data:: ENOTCONN

   Điểm cuối truyền tải chưa được kết nối


.. data:: ESHUTDOWN

   Không thể gửi sau khi điểm cuối truyền tải bị tắt. Lỗi này được ánh xạ tới ngoại lệ :exc:`BrokenPipeError`.


.. data:: ETOOMANYREFS

   Quá nhiều tham chiếu: không thể splice


.. data:: ETIMEDOUT

   Kết nối đã hết thời gian chờ. Lỗi này được ánh xạ tới ngoại lệ
   :exc:`TimeoutError`.


.. data:: ECONNREFUSED

   Kết nối bị từ chối. Lỗi này được ánh xạ tới ngoại lệ
   :exc:`ConnectionRefusedError`.


.. data:: EHOSTDOWN

   Máy chủ đang ngừng hoạt động


.. data:: EHOSTUNREACH

   Không có đường dẫn đến máy chủ


.. data:: EHWPOISON

   Trang bộ nhớ gặp lỗi phần cứng.

   .. versionadded:: 3.14


.. data:: EALREADY

   Thao tác đã được thực hiện. Lỗi này được ánh xạ tới ngoại lệ :exc:`BlockingIOError`.


.. data:: EINPROGRESS

   Thao tác đang được thực hiện. Lỗi này được ánh xạ tới ngoại lệ
   :exc:`BlockingIOError`.


.. data:: ESTALE

   Handle tệp NFS đã cũ


.. data:: EUCLEAN

   Cấu trúc cần được dọn dẹp


.. data:: ENOTNAM

   Không phải là tệp kiểu được đặt tên XENIX


.. data:: ENAVAIL

   Không có semaphore XENIX nào khả dụng


.. data:: EISNAM

   Là tệp kiểu có tên


.. data:: EREMOTEIO

   Lỗi I/O từ xa


.. data:: EDQUOT

   Đã vượt quá hạn ngạch

.. data:: EQFULL

   Hàng đợi đầu ra của interface đã đầy

   .. versionadded:: 3.11


.. data:: ENOMEDIUM

   Không tìm thấy phương tiện


.. data:: EMEDIUMTYPE

   Sai loại phương tiện


.. data:: ENOKEY

   Không có khóa bắt buộc


.. data:: EKEYEXPIRED

   Khóa đã hết hạn


.. data:: EKEYREVOKED

   Khóa đã bị thu hồi


.. data:: EKEYREJECTED

   Dịch vụ đã từ chối khóa


.. data:: ERFKILL

   Không thể thực hiện thao tác do RF-kill


.. data:: ELOCKUNMAPPED

   Khóa bị khóa đã được bỏ ánh xạ


.. data:: ENOTACTIVE

   Cơ chế không hoạt động


.. data:: EAUTH

   Lỗi xác thực

   .. versionadded:: 3.2


.. data:: EBADARCH

   Loại CPU không hợp lệ trong tệp thực thi

   .. versionadded:: 3.2


.. data:: EBADEXEC

   Tệp thực thi (hoặc thư viện dùng chung) không hợp lệ

   .. versionadded:: 3.2


.. data:: EBADMACHO

   Tệp Mach-O không đúng định dạng

   .. versionadded:: 3.2


.. data:: EDEVERR

   Lỗi thiết bị

   .. versionadded:: 3.2


.. data:: EFTYPE

   Loại hoặc định dạng tệp không phù hợp

   .. versionadded:: 3.2


.. data:: ENEEDAUTH

   Cần trình xác thực

   .. versionadded:: 3.2


.. data:: ENOATTR

   Không tìm thấy thuộc tính

   .. versionadded:: 3.2


.. data:: ENOPOLICY

   Không tìm thấy chính sách

   .. versionadded:: 3.2


.. data:: EPROCLIM

   Quá nhiều tiến trình

   .. versionadded:: 3.2


.. data:: EPROCUNAVAIL

   Thủ tục không hợp lệ cho chương trình

   .. versionadded:: 3.2


.. data:: EPROGMISMATCH

   Phiên bản chương trình không đúng

   .. versionadded:: 3.2


.. data:: EPROGUNAVAIL

   Không có chương trình RPC

   .. versionadded:: 3.2


.. data:: EPWROFF

   Thiết bị đã tắt nguồn

   .. versionadded:: 3.2


.. data:: EBADRPC

   Cấu trúc RPC không hợp lệ

   .. versionadded:: 3.2


.. data:: ERPCMISMATCH

   Phiên bản RPC không đúng

   .. versionadded:: 3.2


.. data:: ESHLIBVERS

   Phiên bản thư viện dùng chung không khớp

   .. versionadded:: 3.2


.. data:: ENOTCAPABLE

   Không đủ capability. Lỗi này được ánh xạ tới ngoại lệ
   :exc:`PermissionError`.

   .. availability:: WASI, FreeBSD

   .. versionadded:: 3.11.1


.. data:: ECANCELED

   Thao tác đã bị hủy

   .. versionadded:: 3.2


.. data:: EOWNERDEAD

   Chủ sở hữu đã chết

   .. versionadded:: 3.2


.. data:: ENOTRECOVERABLE

   Trạng thái không thể khôi phục

   .. versionadded:: 3.2
