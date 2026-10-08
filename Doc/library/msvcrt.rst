:mod:`!msvcrt` --- Các routine hữu ích từ runtime MS VC++
=========================================================

.. module:: msvcrt
   :synopsis: Các routine hữu ích khác từ runtime MS VC++.

.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>

--------------

Các hàm này cung cấp quyền truy cập vào một số khả năng hữu ích trên các nền tảng Windows. Một số module cấp cao hơn sử dụng các hàm này để xây dựng phần triển khai các dịch vụ của chúng trên Windows. Ví dụ: module :mod:`getpass` sử dụng module này trong phần triển khai hàm :func:`getpass`.

Bạn có thể tìm thấy tài liệu bổ sung về các hàm này trong tài liệu Platform API.

Module này triển khai cả các biến thể console I/O API dùng ký tự thông thường và ký tự wide. API thông thường chỉ xử lý các ký tự ASCII và có phạm vi sử dụng hạn chế đối với các ứng dụng quốc tế hóa. Nên sử dụng wide char API bất cứ khi nào có thể.

.. availability:: Windows.

.. versionchanged:: 3.3
   Các thao tác trong module này hiện sẽ phát sinh :exc:`OSError` ở những nơi trước đây phát sinh :exc:`IOError`.


.. _msvcrt-files:

Các thao tác với tệp
--------------------


.. function:: locking(fd, mode, nbytes)

   Khóa một phần tệp dựa trên bộ mô tả tệp *fd* từ C runtime. Gây ra
   :exc:`OSError` khi không thành công. Vùng bị khóa của tệp bắt đầu từ vị trí hiện tại trong tệp với độ dài *nbytes* byte và có thể kéo dài vượt quá phần cuối tệp. *mode* phải là một trong các hằng số :const:`!LK_\*` được liệt kê bên dưới. Có thể khóa đồng thời nhiều vùng trong một tệp, nhưng các vùng đó không được chồng lấp. Các vùng liền kề không được hợp nhất; chúng phải được mở khóa riêng lẻ.

   .. audit-event:: msvcrt.locking fd,mode,nbytes msvcrt.locking


.. data:: LK_LOCK
          LK_RLCK

   Khóa các byte được chỉ định. Nếu không thể khóa các byte này, chương trình sẽ thử lại ngay sau 1 giây. Nếu sau 10 lần thử mà vẫn không thể khóa các byte, :exc:`OSError` sẽ được phát sinh.


.. data:: LK_NBLCK
          LK_NBRLCK

   Khóa các byte được chỉ định. Nếu không thể khóa các byte này, :exc:`OSError` sẽ được phát sinh.


.. data:: LK_UNLCK

   Mở khóa các byte được chỉ định; trước đó các byte này phải đã được khóa.


.. function:: setmode(fd, flags)

   Đặt chế độ dịch cuối dòng cho bộ mô tả tệp *fd*. Để đặt thành chế độ văn bản, *flags* phải là :const:`os.O_TEXT`; đối với nhị phân, nó phải là
   :const:`os.O_BINARY`.


.. function:: open_osfhandle(handle, flags)

   Tạo bộ mô tả tệp của C runtime từ handle tệp *handle*. Tham số *flags* phải là phép OR theo bit của :const:`os.O_APPEND`,
   :const:`os.O_RDONLY`, :const:`os.O_TEXT` và :const:`os.O_NOINHERIT`. Bộ mô tả tệp được trả về có thể được dùng làm tham số cho :func:`os.fdopen` để tạo một đối tượng tệp.

   Theo mặc định, bộ mô tả tệp có thể được kế thừa. Truyền cờ :const:`os.O_NOINHERIT` để làm cho nó không thể được kế thừa.

   .. audit-event:: msvcrt.open_osfhandle handle,flags msvcrt.open_osfhandle


.. function:: get_osfhandle(fd)

   Trả về handle tệp tương ứng với bộ mô tả tệp *fd*. Gây ra :exc:`OSError` nếu *fd* không được nhận diện.

   .. audit-event:: msvcrt.get_osfhandle fd msvcrt.get_osfhandle


.. _msvcrt-console:

I/O bàn điều khiển
------------------


.. function:: kbhit()

   Trả về giá trị khác 0 nếu đang chờ đọc một lần nhấn phím. Nếu không, trả về 0.


.. function:: getch()

   Đọc một lần nhấn phím và trả về ký tự tương ứng dưới dạng chuỗi byte. Không có gì được hiển thị trên console. Lệnh gọi này sẽ chặn nếu chưa có lần nhấn phím nào sẵn sàng, nhưng sẽ không chờ phím :kbd:`Enter` được nhấn. Nếu phím được nhấn là một phím chức năng đặc biệt, hàm này sẽ trả về ``'\000'`` hoặc ``'\xe0'``; lần gọi tiếp theo sẽ trả về mã phím. Không thể đọc lần nhấn phím :kbd:`Control-C` bằng hàm này.


.. function:: getwch()

   Biến thể wide char của :func:`getch`, trả về một giá trị Unicode.


.. function:: getche()

   Tương tự :func:`getch`, nhưng lần nhấn phím sẽ được hiển thị nếu biểu thị một ký tự có thể in được.


.. function:: getwche()

   Biến thể wide char của :func:`getche`, trả về một giá trị Unicode.


.. function:: putch(char)

   In chuỗi byte *char* ra console mà không đệm.


.. function:: putwch(unicode_char)

   Biến thể wide char của :func:`putch`, nhận một giá trị Unicode.


.. function:: ungetch(char)

   Khiến chuỗi byte *char* được “đẩy ngược” vào bộ đệm console; đây sẽ là ký tự tiếp theo được :func:`getch` hoặc :func:`getche` đọc.


.. function:: ungetwch(unicode_char)

   Biến thể wide char của :func:`ungetch`, chấp nhận một giá trị Unicode.


.. _msvcrt-other:

Các hàm khác
------------


.. function:: heapmin()

   Buộc heap :c:func:`malloc` tự dọn dẹp và trả các block chưa sử dụng về cho hệ điều hành. Nếu thất bại, hàm này sẽ raise :exc:`OSError`.


.. function:: set_error_mode(mode)

   Thay đổi vị trí mà C runtime ghi thông báo lỗi đối với một lỗi có thể khiến chương trình kết thúc. *mode* phải là một trong các hằng số :const:`!OUT_\*` được liệt kê dưới đây  hoặc :const:`REPORT_ERRMODE`. Trả về thiết lập cũ hoặc -1 nếu xảy ra lỗi. Chỉ khả dụng trong
   :ref:`bản build debug của Python <debug-build>`.


.. data:: OUT_TO_DEFAULT

   Nơi nhận lỗi được xác định bởi loại ứng dụng. Chỉ khả dụng trong
   :ref:`bản build debug của Python <debug-build>`.


.. data:: OUT_TO_STDERR

   Error sink là lỗi chuẩn. Chỉ khả dụng trong
   :ref:`bản build debug của Python <debug-build>`.


.. data:: OUT_TO_MSGBOX

   Error sink là hộp thông báo. Chỉ khả dụng trong
   :ref:`bản build debug của Python <debug-build>`.


.. data:: REPORT_ERRMODE

   Báo cáo giá trị chế độ lỗi hiện tại. Chỉ khả dụng trong
   :ref:`bản build debug của Python <debug-build>`.


.. function:: CrtSetReportMode(type, mode)

   Chỉ định đích hoặc các đích cho một loại báo cáo cụ thể được tạo bởi :c:func:`!_CrtDbgReport` trong runtime MS VC++. *type* phải là một trong các hằng số :const:`!CRT_\*` được liệt kê bên dưới. *mode* phải là một trong các
   :const:`!CRTDBG_\*` các hằng số được liệt kê dưới đây. Chỉ khả dụng trong
   :ref:`bản build debug của Python <debug-build>`.


.. function:: CrtSetReportFile(type, file)

   Sau khi sử dụng :func:`CrtSetReportMode` để chỉ định :const:`CRTDBG_MODE_FILE`, bạn có thể chỉ định file handle để nhận nội dung thông báo. *type* phải là một trong các hằng số :const:`!CRT_\*` được liệt kê dưới đây. *file* phải là file handle mà bạn muốn chỉ định. Chỉ khả dụng trong
   :ref:`bản build debug của Python <debug-build>`.


.. data:: CRT_WARN

   Cảnh báo, thông báo và thông tin không cần được xử lý ngay lập tức.


.. data:: CRT_ERROR

   Lỗi, sự cố không thể khôi phục và các vấn đề cần được xử lý ngay lập tức.


.. data:: CRT_ASSERT

   Lỗi xác nhận.


.. data:: CRTDBG_MODE_DEBUG

   Ghi thông báo vào cửa sổ đầu ra của trình gỡ lỗi.


.. data:: CRTDBG_MODE_FILE

   Ghi thông báo vào file handle do người dùng cung cấp. :func:`CrtSetReportFile` nên được gọi để xác định file hoặc stream cụ thể dùng làm đích.


.. data:: CRTDBG_MODE_WNDW

   Tạo một message box để hiển thị thông báo cùng với các nút ``Abort``, ``Retry`` và ``Ignore``.


.. data:: CRTDBG_REPORT_MODE

   Trả về *chế độ* hiện tại cho *loại* được chỉ định.


.. data:: CRT_ASSEMBLY_VERSION

   Phiên bản CRT Assembly, từ file header :file:`crtassem.h`.


.. data:: VC_ASSEMBLY_PUBLICKEYTOKEN

   Mã token public key của VC Assembly, từ file header :file:`crtassem.h`.


.. data:: LIBRARIES_ASSEMBLY_NAME_PREFIX

   Tiền tố tên Libraries Assembly, từ file header :file:`crtassem.h`.
