:mod:`!stat` --- Diễn giải kết quả của :func:`~os.stat`
=======================================================

.. module:: stat
   :synopsis: Các tiện ích để diễn giải kết quả của os.stat(), os.lstat() và os.fstat().

.. sectionauthor:: Skip Montanaro <skip@automatrix.com>

**Mã nguồn:** :source:`Lib/stat.py`

--------------

Mô-đun :mod:`!stat` định nghĩa các hằng số và hàm để diễn giải kết quả của :func:`os.stat`, :func:`os.fstat` và :func:`os.lstat` (nếu chúng tồn tại). Để biết đầy đủ chi tiết về các :c:func:`stat`, :c:func:`!fstat` và
:c:func:`!lstat` lệnh gọi, hãy tham khảo tài liệu dành cho hệ thống của bạn.

.. versionchanged:: 3.4
   Mô-đun stat được hỗ trợ bởi một triển khai C.

Mô-đun :mod:`!stat` định nghĩa các hàm sau để kiểm tra các loại tệp cụ thể:


.. function:: S_ISDIR(mode)

   Trả về giá trị khác 0 nếu mode là của một thư mục.


.. function:: S_ISCHR(mode)

   Trả về giá trị khác 0 nếu mode là của một tệp thiết bị đặc biệt kiểu ký tự.


.. function:: S_ISBLK(mode)

   Trả về giá trị khác 0 nếu mode là của một tệp thiết bị đặc biệt kiểu khối.


.. function:: S_ISREG(mode)

   Trả về giá trị khác 0 nếu mode là của một tệp thông thường.


.. function:: S_ISFIFO(mode)

   Trả về giá trị khác 0 nếu mode là của một FIFO (đường ống có tên).


.. function:: S_ISLNK(mode)

   Trả về giá trị khác 0 nếu mode là của một symbolic link.


.. function:: S_ISSOCK(mode)

   Trả về giá trị khác 0 nếu mode là của một socket.

.. function:: S_ISDOOR(mode)

   Trả về giá trị khác 0 nếu mode là của một door.

   .. versionadded:: 3.4

.. function:: S_ISPORT(mode)

   Trả về giá trị khác 0 nếu mode là của một event port.

   .. versionadded:: 3.4

.. function:: S_ISWHT(mode)

   Trả về giá trị khác 0 nếu mode là của một whiteout.

   .. versionadded:: 3.4

Hai hàm bổ sung được định nghĩa để thao tác tổng quát hơn với mode của tệp:


.. function:: S_IMODE(mode)

   Trả về phần mode của tệp có thể được thiết lập bởi
   :func:`os.chmod`\ ---tức là các bit quyền của tệp, cùng với bit sticky, bit set-group-id và bit set-user-id (trên những hệ thống hỗ trợ chúng).


.. function:: S_IFMT(mode)

   Trả về phần mode của tệp mô tả loại tệp (được dùng bởi
   các hàm :func:`!S_IS\*` ở trên).

Thông thường, bạn sẽ sử dụng các hàm :func:`!os.path.is\*` để kiểm tra loại tệp; các hàm ở đây hữu ích khi bạn thực hiện nhiều phép kiểm tra trên cùng một tệp và muốn tránh chi phí của lời gọi hệ thống :c:func:`stat` cho mỗi phép kiểm tra. Các hàm này cũng hữu ích khi kiểm tra thông tin về một tệp mà :mod:`os.path` không xử lý, chẳng hạn như các phép kiểm tra đối với thiết bị khối và thiết bị ký tự.

Ví dụ::

   import os, sys
   from stat import *

   def walktree(top, callback):
       '''recursively descend the directory tree rooted at top,
          calling the callback function for each regular file'''

       for f in os.listdir(top):
           pathname = os.path.join(top, f)
           mode = os.lstat(pathname).st_mode
           if S_ISDIR(mode):
               # Đây là một thư mục, đệ quy vào đó
               walktree(pathname, callback)
           elif S_ISREG(mode):
               # Đây là một tệp, gọi hàm callback
               callback(pathname)
           else:
               # Không rõ loại tệp, in một thông báo
               print('Skipping %s' % pathname)

   def visitfile(file):
       print('visiting', file)

   if __name__ == '__main__':
       walktree(sys.argv[1], visitfile)

Một hàm tiện ích bổ sung được cung cấp để chuyển mode của tệp thành chuỗi mà con người có thể đọc được:

.. function:: filemode(mode)

   Chuyển mode của một tệp thành chuỗi có dạng '-rwxrwxrwx'.

   .. versionadded:: 3.3

   .. versionchanged:: 3.4
      Hàm hỗ trợ :data:`S_IFDOOR`, :data:`S_IFPORT` và
      :data:`S_IFWHT`.


Tất cả các biến dưới đây chỉ đơn giản là các chỉ mục mang tính ký hiệu trong bộ 10 phần tử được trả về bởi :func:`os.stat`, :func:`os.fstat` hoặc :func:`os.lstat`.


.. data:: ST_MODE

   Mode bảo vệ inode.


.. data:: ST_INO

   Số inode.


.. data:: ST_DEV

   Thiết bị lưu trữ inode.


.. data:: ST_NLINK

   Số lượng liên kết đến inode.


.. data:: ST_UID

   ID người dùng của chủ sở hữu.


.. data:: ST_GID

   ID nhóm của chủ sở hữu.


.. data:: ST_SIZE

   Kích thước tính bằng byte của tệp thông thường; lượng dữ liệu đang chờ trên một số tệp đặc biệt.


.. data:: ST_ATIME

   Thời điểm truy cập gần nhất.


.. data:: ST_MTIME

   Thời điểm sửa đổi gần nhất.


.. data:: ST_CTIME

   Giá trị "ctime" do hệ điều hành báo cáo. Trên một số hệ thống (như Unix), đây là thời điểm thay đổi metadata gần nhất; trên các hệ thống khác (như Windows), đây là thời điểm tạo (xem tài liệu về nền tảng để biết chi tiết).

Cách diễn giải "kích thước tệp" thay đổi tùy theo loại tệp. Đối với tệp thông thường, đây là kích thước của tệp tính bằng byte. Đối với FIFO và socket trên hầu hết các biến thể Unix (đặc biệt là Linux), "kích thước" là số byte đang chờ được đọc tại thời điểm gọi :func:`os.stat`,
:func:`os.fstat`, hoặc :func:`os.lstat`; đôi khi điều này có thể hữu ích, đặc biệt khi thăm dò một trong các tệp đặc biệt này sau khi mở ở chế độ không chặn. Ý nghĩa của trường size đối với các thiết bị ký tự và thiết bị khối khác thay đổi nhiều hơn, tùy thuộc vào cách triển khai system call cơ bản.

Các biến dưới đây xác định những flag được sử dụng trong trường :data:`ST_MODE`.

Việc sử dụng các hàm trên có tính portable cao hơn việc sử dụng nhóm flag đầu tiên:

.. data:: S_IFSOCK

   Socket.

.. data:: S_IFLNK

   Liên kết tượng trưng.

.. data:: S_IFREG

   Tệp thông thường.

.. data:: S_IFBLK

   Thiết bị khối.

.. data:: S_IFDIR

   Thư mục.

.. data:: S_IFCHR

   Thiết bị ký tự.

.. data:: S_IFIFO

   FIFO.

.. data:: S_IFDOOR

   Door.

   .. versionadded:: 3.4

.. data:: S_IFPORT

   Cổng sự kiện.

   .. versionadded:: 3.4

.. data:: S_IFWHT

   Whiteout.

   .. versionadded:: 3.4

.. note::

   :data:`S_IFDOOR`, :data:`S_IFPORT` hoặc :data:`S_IFWHT` được định nghĩa là 0 khi nền tảng không hỗ trợ các loại tệp này.

Các cờ sau đây cũng có thể được sử dụng trong đối số *mode* của :func:`os.chmod`:

.. data:: S_ISUID

   Bit Set UID.

.. data:: S_ISGID

   Bit Set-group-ID. Bit này có một số cách sử dụng đặc biệt. Đối với một thư mục, bit này cho biết thư mục đó sẽ sử dụng ngữ nghĩa BSD: các tệp được tạo tại đó sẽ kế thừa group ID từ thư mục, không phải từ group ID hiệu dụng của tiến trình tạo tệp, và các thư mục được tạo tại đó cũng sẽ được đặt bit :data:`S_ISGID`. Đối với một tệp không được đặt bit thực thi nhóm (:data:`S_IXGRP`), bit Set-group-ID cho biết cơ chế khóa tệp/bản ghi bắt buộc (xem thêm :data:`S_ENFMT`).

.. data:: S_ISVTX

   Bit sticky. Khi bit này được đặt trên một thư mục, điều đó có nghĩa là một tệp trong thư mục đó chỉ có thể được đổi tên hoặc xóa bởi chủ sở hữu tệp, chủ sở hữu thư mục hoặc một tiến trình có đặc quyền.

.. data:: S_IRWXU

   Mặt nạ cho các quyền của chủ sở hữu tệp.

.. data:: S_IRUSR

   Chủ sở hữu có quyền đọc.

.. data:: S_IWUSR

   Chủ sở hữu có quyền ghi.

.. data:: S_IXUSR

   Chủ sở hữu có quyền thực thi.

.. data:: S_IRWXG

   Mặt nạ cho quyền của nhóm.

.. data:: S_IRGRP

   Nhóm có quyền đọc.

.. data:: S_IWGRP

   Nhóm có quyền ghi.

.. data:: S_IXGRP

   Nhóm có quyền thực thi.

.. data:: S_IRWXO

   Mặt nạ cho quyền của những người khác (không thuộc nhóm).

.. data:: S_IROTH

   Những người khác có quyền đọc.

.. data:: S_IWOTH

   Những người dùng khác có quyền ghi.

.. data:: S_IXOTH

   Những người dùng khác có quyền thực thi.

.. data:: S_ENFMT

   Cơ chế thực thi khóa tệp của System V. Cờ này được dùng chung với :data:`S_ISGID`: việc khóa tệp/bản ghi được thực thi trên các tệp không có bit thực thi nhóm (:data:`S_IXGRP`) được đặt.

.. data:: S_IREAD

   Từ đồng nghĩa trong Unix V7 của :data:`S_IRUSR`.

.. data:: S_IWRITE

   Từ đồng nghĩa trong Unix V7 của :data:`S_IWUSR`.

.. data:: S_IEXEC

   Từ đồng nghĩa trong Unix V7 của :data:`S_IXUSR`.

Các cờ sau đây có thể được sử dụng trong đối số *flags* của :func:`os.chflags`:

.. data:: UF_SETTABLE

   Tất cả các cờ người dùng có thể thiết lập.

   .. versionadded:: 3.13

.. data:: UF_NODUMP

   Không kết xuất tệp.

.. data:: UF_IMMUTABLE

   Không được thay đổi tệp.

.. data:: UF_APPEND

   Tệp chỉ được phép nối thêm dữ liệu.

.. data:: UF_OPAQUE

   Thư mục không trong suốt khi được xem qua ngăn xếp union.

.. data:: UF_NOUNLINK

   Không được đổi tên hoặc xóa tệp.

.. data:: UF_COMPRESSED

   Tệp được lưu trữ ở dạng nén (macOS 10.6 trở lên).

.. data:: UF_TRACKED

   Dùng để xử lý ID tài liệu (macOS)

   .. versionadded:: 3.13

.. data:: UF_DATAVAULT

   Tệp cần có entitlement để đọc hoặc ghi (macOS 10.13+)

   .. versionadded:: 3.13

.. data:: UF_HIDDEN

   Không nên hiển thị tệp trong GUI (macOS 10.5+).

.. data:: SF_SETTABLE

   Tất cả các cờ mà super-user có thể thay đổi

   .. versionadded:: 3.13

.. data:: SF_SUPPORTED

   Tất cả các cờ được super-user hỗ trợ

   .. availability:: macOS

   .. versionadded:: 3.13

.. data:: SF_SYNTHETIC

   Tất cả các cờ tổng hợp chỉ đọc của super-user

   .. availability:: macOS

   .. versionadded:: 3.13

.. data:: SF_ARCHIVED

   Tệp có thể được lưu trữ.

.. data:: SF_IMMUTABLE

   Không được thay đổi tệp.

.. data:: SF_APPEND

   Tệp chỉ được phép nối thêm dữ liệu.

.. data:: SF_RESTRICTED

   Tệp cần có entitlement để ghi vào (macOS 10.13+)

   .. versionadded:: 3.13

.. data:: SF_NOUNLINK

   Không được đổi tên hoặc xóa tệp.

.. data:: SF_SNAPSHOT

   Tệp là một tệp snapshot.

.. data:: SF_FIRMLINK

   Tệp là một firmlink (macOS 10.15+)

   .. versionadded:: 3.13

.. data:: SF_DATALESS

   Tệp là một đối tượng không có dữ liệu (macOS 10.15+)

   .. versionadded:: 3.13

Xem \*trang man của hệ thống BSD hoặc macOS :manpage:`chflags(2)` để biết thêm thông tin.

Trên Windows, các hằng số thuộc tính tệp sau đây có thể được sử dụng khi kiểm tra các bit trong thành viên ``st_file_attributes`` được trả về bởi :func:`os.stat`. Xem `tài liệu Windows API <https://msdn.microsoft.com/en-us/library/windows/desktop/gg258117.aspx>`_ để biết thêm chi tiết về ý nghĩa của các hằng số này.

.. data:: FILE_ATTRIBUTE_ARCHIVE
          FILE_ATTRIBUTE_COMPRESSED FILE_ATTRIBUTE_DEVICE FILE_ATTRIBUTE_DIRECTORY FILE_ATTRIBUTE_ENCRYPTED FILE_ATTRIBUTE_HIDDEN FILE_ATTRIBUTE_INTEGRITY_STREAM FILE_ATTRIBUTE_NORMAL FILE_ATTRIBUTE_NOT_CONTENT_INDEXED FILE_ATTRIBUTE_NO_SCRUB_DATA FILE_ATTRIBUTE_OFFLINE FILE_ATTRIBUTE_READONLY FILE_ATTRIBUTE_REPARSE_POINT FILE_ATTRIBUTE_SPARSE_FILE FILE_ATTRIBUTE_SYSTEM FILE_ATTRIBUTE_TEMPORARY FILE_ATTRIBUTE_VIRTUAL

   .. versionadded:: 3.5

Trên Windows, các hằng số sau đây có thể được sử dụng để so sánh với thành viên ``st_reparse_tag`` được trả về bởi :func:`os.lstat`. Đây là các hằng số quen thuộc, nhưng không phải là danh sách đầy đủ.

.. data:: IO_REPARSE_TAG_SYMLINK
          IO_REPARSE_TAG_MOUNT_POINT IO_REPARSE_TAG_APPEXECLINK

   .. versionadded:: 3.8

.. _`Windows API documentation`: https://msdn.microsoft.com/en-us/library/windows/desktop/gg258117.aspx
