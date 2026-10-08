:mod:`!netrc` --- xử lý tệp netrc
=================================

.. module:: netrc
   :synopsis: Tải các tệp .netrc.

.. moduleauthor:: Eric S. Raymond <esr@snark.thyrsus.com>
.. sectionauthor:: Eric S. Raymond <esr@snark.thyrsus.com>

**Mã nguồn:** :source:`Lib/netrc.py`

--------------

Lớp :class:`~netrc.netrc` phân tích cú pháp và đóng gói định dạng tệp netrc được chương trình Unix :program:`ftp` và các FTP client khác sử dụng.


.. class:: netrc([file])

   Một đối tượng :class:`~netrc.netrc` hoặc đối tượng lớp con đóng gói dữ liệu từ một tệp netrc. Đối số khởi tạo, nếu có, chỉ định tệp cần phân tích cú pháp. Nếu không cung cấp đối số, tệp :file:`.netrc` trong thư mục chính của người dùng -- được xác định bởi :func:`os.path.expanduser` -- sẽ được đọc. Nếu không, một ngoại lệ :exc:`FileNotFoundError` sẽ được phát sinh. Lỗi phân tích cú pháp sẽ phát sinh :exc:`NetrcParseError` cùng thông tin chẩn đoán, bao gồm tên tệp, số dòng và token kết thúc.

   Nếu không chỉ định đối số trên hệ thống POSIX, việc có mật khẩu trong tệp :file:`.netrc` sẽ phát sinh một :exc:`NetrcParseError` nếu quyền sở hữu hoặc quyền truy cập của tệp không an toàn (do người dùng khác với người đang chạy process sở hữu, hoặc bất kỳ người dùng nào khác có quyền đọc hoặc ghi). Cơ chế này triển khai hành vi bảo mật tương đương với ftp và các chương trình khác sử dụng :file:`.netrc`. Những kiểm tra bảo mật này không khả dụng trên các nền tảng không hỗ trợ :func:`os.getuid`.

   .. versionchanged:: 3.4 Đã bổ sung kiểm tra quyền POSIX.

   .. versionchanged:: 3.7
      :func:`os.path.expanduser` is used to find the location of the
      :file:`.netrc` file when *file* is not passed as argument.

   .. versionchanged:: 3.10
      :class:`netrc` try UTF-8 encoding before using locale specific
      encoding. Mục nhập trong tệp netrc không còn cần chứa tất cả các token. Giá trị của các token bị thiếu mặc định là chuỗi rỗng. Tất cả các token và giá trị của chúng giờ đây có thể chứa các ký tự tùy ý, chẳng hạn như khoảng trắng và ký tự không phải ASCII. Nếu tên đăng nhập là anonymous, tên này sẽ không kích hoạt bước kiểm tra bảo mật.


.. exception:: NetrcParseError

   Ngoại lệ do lớp :class:`~netrc.netrc` phát sinh khi phát hiện lỗi cú pháp trong văn bản nguồn. Các thực thể của ngoại lệ này cung cấp ba thuộc tính đáng chú ý:

   .. attribute:: msg

      Mô tả bằng văn bản về lỗi.

   .. attribute:: filename

      Tên của tệp nguồn.

   .. attribute:: lineno

      Số dòng tại đó phát hiện lỗi.


.. _netrc-objects:

Các đối tượng netrc
-------------------

Một thực thể :class:`~netrc.netrc` có các phương thức sau:


.. method:: netrc.authenticators(host)

   Trả về một bộ 3 phần tử ``(login, account, password)`` gồm thông tin xác thực cho *host*. Nếu tệp netrc không chứa mục nhập cho host đã cho, trả về bộ tuple tương ứng với mục nhập 'default'. Nếu không có host phù hợp hoặc mục nhập default, trả về ``None``.


.. method:: netrc.__repr__()

   Kết xuất dữ liệu của lớp thành một chuỗi theo định dạng của tệp netrc. (Thao tác này sẽ loại bỏ các chú thích và có thể sắp xếp lại các mục nhập.)

Các thực thể của :class:`~netrc.netrc` có các biến thực thể công khai sau:


.. attribute:: netrc.hosts

   Từ điển ánh xạ tên host tới các tuple ``(login, account, password)``. Mục nhập 'default', nếu có, được biểu diễn dưới dạng một pseudo-host có tên đó.


.. attribute:: netrc.macros

   Từ điển ánh xạ tên macro tới các danh sách chuỗi.
