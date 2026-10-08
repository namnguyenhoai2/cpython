:mod:`!posix` --- Các lời gọi hệ thống POSIX phổ biến nhất
==========================================================

.. module:: posix
   :synopsis: Các lời gọi hệ thống POSIX phổ biến nhất (thường được sử dụng thông qua mô-đun os).

--------------

Mô-đun này cung cấp quyền truy cập vào các chức năng của hệ điều hành được chuẩn hóa bởi Tiêu chuẩn C và tiêu chuẩn POSIX (một giao diện Unix được che giấu khá kỹ).

.. availability:: Unix.

.. index:: pair: module; os

**Không nhập trực tiếp mô-đun này.**  Thay vào đó, hãy nhập mô-đun :mod:`os`, mô-đun này cung cấp phiên bản *portable* của giao diện này.  Trên Unix, mô-đun :mod:`os` cung cấp một siêu tập của giao diện :mod:`!posix`.  Trên các hệ điều hành không phải Unix, mô-đun :mod:`!posix` không khả dụng, nhưng một tập con luôn khả dụng thông qua giao diện :mod:`os`.  Sau khi :mod:`os` được nhập, việc sử dụng nó thay cho :mod:`!posix` sẽ *không* gây tổn thất hiệu năng.  Ngoài ra,
:mod:`os` cung cấp một số chức năng bổ sung, chẳng hạn như tự động gọi
:func:`~os.putenv` khi một mục trong ``os.environ`` bị thay đổi.

Các lỗi được báo cáo dưới dạng ngoại lệ; các ngoại lệ thông thường được sử dụng cho lỗi kiểu, trong khi những lỗi do các lời gọi hệ thống báo cáo sẽ phát sinh :exc:`OSError`.


.. _posix-large-files:

Hỗ trợ tệp lớn
--------------

.. index::
   single: large files
   single: file; large files

.. sectionauthor:: Steve Clift <clift@mail.anacapa.net>

Một số hệ điều hành (bao gồm AIX và Solaris) cung cấp hỗ trợ cho các tệp lớn hơn 2 GiB từ mô hình lập trình C, trong đó
:c:expr:`int` và :c:expr:`long` là các giá trị 32 bit. Điều này thường được thực hiện bằng cách định nghĩa các kiểu kích thước và offset liên quan là các giá trị 64 bit. Những tệp như vậy đôi khi được gọi là :dfn:`tệp lớn`.

Hỗ trợ tệp lớn được bật trong Python khi kích thước của một :c:type:`off_t` lớn hơn một :c:expr:`long` và :c:expr:`long long` ít nhất phải lớn bằng một :c:type:`off_t`. Có thể cần cấu hình và biên dịch Python với một số cờ compiler nhất định để bật chế độ này. Ví dụ, với Solaris 2.6 và 2.7, bạn cần làm như sau::

   CFLAGS="`getconf LFS_CFLAGS`" OPT="-g -O2 $CFLAGS" \
           ./configure

Trên các hệ thống Linux hỗ trợ tệp lớn, cách này có thể hoạt động::

   CFLAGS='-D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64' OPT="-g -O2 $CFLAGS" \
           ./configure


.. _posix-contents:

Nội dung đáng chú ý của module
------------------------------

Ngoài nhiều hàm được mô tả trong tài liệu module :mod:`os`,
:mod:`!posix` định nghĩa mục dữ liệu sau:

.. data:: environ

   Một ánh xạ biểu diễn môi trường chuỗi tại thời điểm trình thông dịch được khởi động. Khóa và giá trị là bytes trên Unix và str trên Windows. Ví dụ, ``environ[b'HOME']`` (``environ['HOME']`` trên Windows) là pathname của thư mục chính của bạn, tương đương với ``getenv("HOME")`` trong C.

   Việc sửa đổi ánh xạ này không ảnh hưởng đến môi trường chuỗi được truyền tiếp bởi
   :func:`~os.execv`, :func:`~os.popen` hoặc :func:`~os.system`; nếu cần thay đổi môi trường, hãy truyền ``environ`` cho :func:`~os.execve` hoặc thêm các phép gán biến và câu lệnh export vào chuỗi lệnh cho
   :func:`~os.system` hoặc :func:`~os.popen`.

   .. versionchanged:: 3.2
      Trên Unix, khóa và giá trị là bytes.

   .. note::

      Mô-đun :mod:`os` cung cấp một cách triển khai thay thế cho ``environ``, trong đó môi trường được cập nhật khi có sửa đổi. Cũng lưu ý rằng việc cập nhật
      :data:`os.environ` sẽ khiến từ điển này trở nên lỗi thời. Nên sử dụng
      :mod:`os`, phiên bản mô-đun của cách này, thay vì truy cập trực tiếp vào
      :mod:`!posix` mô-đun.
