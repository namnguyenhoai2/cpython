.. currentmodule:: argparse

.. _upgrading-optparse-code:
.. _migrating-optparse-code:

===========================================
Di chuyển mã ``optparse`` sang ``argparse``
===========================================

Mô-đun :mod:`argparse` cung cấp một số tính năng cấp cao hơn mà mô-đun :mod:`optparse` không hỗ trợ sẵn, bao gồm:

* Xử lý các đối số vị trí.
* Hỗ trợ các subcommand.
* Cho phép sử dụng các tiền tố tùy chọn thay thế như ``+`` và ``/``.
* Xử lý các đối số kiểu không hoặc nhiều và một hoặc nhiều.
* Tạo các thông báo hướng dẫn sử dụng giàu thông tin hơn.
* Cung cấp một giao diện đơn giản hơn nhiều cho các ``type`` và ``action`` tùy chỉnh.

Ban đầu, mô-đun :mod:`argparse` cố gắng duy trì khả năng tương thích với :mod:`optparse`. Tuy nhiên, những khác biệt cơ bản trong thiết kế giữa việc hỗ trợ xử lý tùy chọn dòng lệnh theo khai báo (đồng thời để mã ứng dụng xử lý các đối số vị trí) và việc hỗ trợ cả tùy chọn có tên lẫn đối số vị trí trong giao diện khai báo khiến API dần khác với API của ``optparse``.

Như đã mô tả trong :ref:`choosing-an-argument-parser`, các ứng dụng hiện đang sử dụng :mod:`optparse` và hài lòng với cách thức hoạt động của nó có thể tiếp tục sử dụng ``optparse``.

Các nhà phát triển ứng dụng đang cân nhắc việc chuyển đổi cũng nên xem lại danh sách những khác biệt về hành vi vốn có được mô tả trong phần đó trước khi quyết định có nên chuyển đổi hay không.

Đối với các ứng dụng thực sự chuyển đổi từ :mod:`optparse` sang :mod:`argparse`, những đề xuất sau đây sẽ hữu ích:

* Thay thế tất cả các lệnh gọi :meth:`optparse.OptionParser.add_option` bằng
  các lệnh gọi :meth:`ArgumentParser.add_argument`.

* Thay thế ``(options, args) = parser.parse_args()`` bằng ``args = parser.parse_args()`` và thêm các lệnh gọi :meth:`ArgumentParser.add_argument` cho các đối số vị trí. Hãy lưu ý rằng thứ trước đây được gọi là ``options`` thì trong ngữ cảnh :mod:`argparse` hiện được gọi là ``args``.

* Thay thế :meth:`optparse.OptionParser.disable_interspersed_args` bằng cách sử dụng :meth:`~ArgumentParser.parse_intermixed_args` thay cho
  :meth:`~ArgumentParser.parse_args`.

* Thay thế các callback action và đối số keyword ``callback_*`` bằng đối số ``type`` hoặc ``action``.

* Thay thế tên chuỗi cho các đối số keyword ``type`` bằng các đối tượng kiểu tương ứng (ví dụ: int, float, complex, v.v.).

* Thay thế :class:`optparse.Values` bằng :class:`Namespace` và
  :exc:`optparse.OptionError` và :exc:`optparse.OptionValueError` bằng
  :exc:`ArgumentError`.

* Thay thế các chuỗi có đối số ngầm định như ``%default`` hoặc ``%prog`` bằng cú pháp Python chuẩn để sử dụng dictionary nhằm định dạng chuỗi, cụ thể là ``%(default)s`` và ``%(prog)s``.

* Thay đối số ``version`` của hàm khởi tạo OptionParser bằng một lệnh gọi đến ``parser.add_argument('--version', action='version', version='<the version>')``.
