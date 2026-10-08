.. _library-index:

#####################
Thư viện chuẩn Python
#####################

Tài liệu tham khảo về thư viện này mô tả thư viện chuẩn được phân phối cùng Python. Tài liệu cũng mô tả một số thành phần tùy chọn thường được tích hợp trong các bản phân phối Python.

Ở nơi khác, :ref:`reference-index` mô tả cú pháp và ngữ nghĩa chính xác của ngôn ngữ Python, còn :ref:`builtins-index` mô tả các hàm tích hợp sẵn.

Thư viện chuẩn của Python rất phong phú, cung cấp nhiều loại tiện ích như được thể hiện trong mục lục dài bên dưới. Thư viện này chứa các mô-đun tích hợp sẵn (được viết bằng C) cung cấp quyền truy cập vào các chức năng của hệ thống, chẳng hạn như I/O tệp vốn không thể truy cập được đối với lập trình viên Python theo cách khác, cũng như các mô-đun được viết bằng Python, cung cấp các giải pháp được chuẩn hóa cho nhiều vấn đề thường gặp trong lập trình hằng ngày. Một số mô-đun được thiết kế rõ ràng để khuyến khích và tăng cường tính khả chuyển của các chương trình Python bằng cách trừu tượng hóa các đặc thù dành riêng cho nền tảng thành các API trung lập với nền tảng.

Các trình cài đặt Python dành cho nền tảng Windows thường bao gồm toàn bộ thư viện chuẩn và thường cũng bao gồm nhiều thành phần bổ sung. Đối với các hệ điều hành giống Unix, Python thường được cung cấp dưới dạng một tập hợp các gói, vì vậy có thể cần sử dụng các công cụ quản lý gói do hệ điều hành cung cấp để có được một phần hoặc toàn bộ các thành phần tùy chọn.

Ngoài thư viện chuẩn, còn có một tập hợp đang hoạt động gồm hàng trăm nghìn thành phần (từ các chương trình và mô-đun riêng lẻ đến các gói và toàn bộ framework phát triển ứng dụng), có sẵn trên `Python Package Index <https://pypi.org>`_.

.. We don't use :numbered: option for the TOC below as it enforces
   numbered sections for the entire stdlib docs.  If desired,
   :numbered: can be enabled on a per-module basis.
.. toctree::
   :maxdepth: 2

   intro.rst

   text.rst
   binary.rst
   datatypes.rst
   numeric.rst
   functional.rst
   filesys.rst
   persistence.rst
   archiving.rst
   fileformats.rst
   crypto.rst
   allos.rst
   cmdlinelibs.rst
   concurrency.rst
   ipc.rst
   netdata.rst
   markup.rst
   internet.rst
   mm.rst
   i18n.rst
   tk.rst
   development.rst
   debug.rst
   distribution.rst
   python.rst
   custominterp.rst
   modules.rst
   language.rst
   windows.rst
   unix.rst
   cmdline.rst
   superseded.rst
   removed.rst
   security_warnings.rst

.. _`Python Package Index`: https://pypi.org
