README Tài liệu Python
~~~~~~~~~~~~~~~~~~~~~~

Thư mục này chứa các nguồn reStructuredText (reST) cho tài liệu Python. Bạn không cần tự xây dựng tài liệu; `các phiên bản dựng sẵn có sẵn <https://docs.python.org/dev/download.html>`_.

Tài liệu về cách biên soạn tài liệu Python, bao gồm thông tin về cả văn phong và markup, có trong chương "`Documenting Python <https://devguide.python.org/documenting/>`_" của hướng dẫn dành cho nhà phát triển.


Xây dựng tài liệu
=================

Tài liệu được xây dựng bằng một số công cụ không có trong cây thư mục này nhưng được duy trì riêng và có sẵn trên `PyPI <https://pypi.org/>`_.

* `Sphinx <https://pypi.org/project/Sphinx/>`_
* `blurb <https://pypi.org/project/blurb/>`_
* `python-docs-theme <https://pypi.org/project/python-docs-theme/>`_

Cách dễ nhất để cài đặt các công cụ này là tạo một virtual environment và cài đặt các công cụ vào đó.

Sử dụng make
------------

Để bắt đầu trên Unix, bạn có thể tạo một virtual environment và build tài liệu bằng các lệnh::

  make venv
  make html

Virtual environment trong thư mục ``venv`` sẽ chứa tất cả các công cụ cần thiết để build tài liệu, được tải xuống và cài đặt từ PyPI. Nếu muốn tạo virtual environment ở một vị trí khác, bạn có thể chỉ định vị trí đó bằng biến ``VENVDIR``.

Bạn cũng có thể bỏ qua hoàn toàn việc tạo virtual environment; trong trường hợp đó, ``Makefile`` sẽ tìm các phiên bản của ``sphinx-build`` và ``blurb`` được cài đặt trên ``PATH`` của process, có thể cấu hình bằng các biến ``SPHINXBUILD`` và ``BLURB``.

Trên Windows, chúng tôi cố gắng mô phỏng ``Makefile`` sát nhất có thể bằng tệp ``make.bat``. Nếu cần chỉ định trình thông dịch Python sẽ sử dụng, hãy đặt biến môi trường ``PYTHON``.

Các mục tiêu make hiện có:

* "clean", xóa tất cả các tệp build và môi trường ảo.

* "clean-venv", xóa thư mục môi trường ảo.

* "venv", tạo một môi trường ảo với tất cả công cụ cần thiết đã được cài đặt.

* "html", build các tệp HTML độc lập để xem offline.

* "htmlview", sử dụng lại builder "html", sau đó mở trang chính trong trình duyệt web mặc định của bạn.

* "htmllive", sử dụng lại builder "html", build lại tài liệu, khởi động một server cục bộ và tự động tải lại trang trong trình duyệt khi bạn thực hiện thay đổi đối với các tệp reST (chỉ Unix).

* "htmlhelp", tạo các tệp HTML và một tệp dự án HTML Help có thể dùng để chuyển chúng thành một tệp Compiled HTML (.chm) duy nhất -- các tệp này phổ biến trên Microsoft Windows nhưng cũng rất hữu ích trên mọi nền tảng.

  Để tạo tệp CHM, bạn cần chạy Microsoft HTML Help Workshop trên tệp dự án (.hhp) đã tạo. Script ``make.bat`` thực hiện việc này cho bạn trên Windows.

* "latex", tạo các tệp mã nguồn LaTeX làm đầu vào cho ``pdflatex`` để tạo các tài liệu PDF.

* "text", tạo một tệp văn bản thuần túy cho mỗi tệp mã nguồn.

* "epub", tạo một tài liệu EPUB, phù hợp để xem trên các thiết bị đọc sách điện tử.

* "linkcheck", kiểm tra tất cả các tham chiếu bên ngoài để xem chúng có bị hỏng, chuyển hướng hoặc sai định dạng hay không, đồng thời xuất thông tin này ra stdout cũng như một tệp văn bản thuần túy (.txt).

* "changes", tạo một bản tổng quan về tất cả các mục versionadded/versionchanged/ deprecated trong phiên bản hiện tại. Tính năng này nhằm hỗ trợ người viết tài liệu "Có gì mới".

* "coverage", dùng để tạo tổng quan về độ bao phủ cho các module thư viện chuẩn và C API.

* "pydoc-topics", dùng để tạo một module Python chứa một dictionary với tài liệu dạng văn bản thuần cho các nhãn được định nghĩa trong ``tools/pyspecific.py`` -- pydoc cần chúng để hiển thị trợ giúp về chủ đề và từ khóa.

* "check", dùng để kiểm tra các lỗi markup thường gặp.

* "dist", (chỉ dành cho Unix) dùng để tạo các archive có thể phân phối của các bản build HTML, văn bản, PDF và EPUB.


Không dùng make
---------------

Trước tiên, cài đặt các dependency của công cụ từ PyPI.

Sau đó, từ thư mục ``Doc``, chạy::

   sphinx-build -b<builder> . build/<builder>

trong đó ``<builder>`` là một trong html, text, latex hoặc htmlhelp (xem phần giải thích trong các make target ở trên).

Tiêu đề ngừng hỗ trợ
====================

Bạn có thể định nghĩa biến ``outdated`` trong ``html_context`` để hiển thị một banner màu đỏ trên mỗi trang, chuyển hướng đến phiên bản "latest".

Liên kết trỏ đến cùng một trang trên ``/3/``; đáng tiếc là hiện tại ngôn ngữ bị mất trong quá trình này.


Đóng góp
========

Các lỗi trong nội dung cần được báo cáo cho trình theo dõi lỗi `Python <https://github.com/python/cpython/issues>`_.

Các lỗi trong bộ công cụ cần được báo cáo cho chính các công cụ đó.

Để hỗ trợ tài liệu hoặc báo cáo bất kỳ vấn đề nào, vui lòng để lại tin nhắn trên `discuss.python.org <https://discuss.python.org/c/documentation>`_.

.. _`prebuilt versions are available`: https://docs.python.org/dev/download.html
.. _`Documenting Python`: https://devguide.python.org/documenting/
.. _`PyPI`: https://pypi.org/
.. _`Sphinx`: https://pypi.org/project/Sphinx/
.. _`blurb`: https://pypi.org/project/blurb/
.. _`python-docs-theme`: https://pypi.org/project/python-docs-theme/
.. _`Python bug tracker`: https://github.com/python/cpython/issues
.. _`discuss.python.org`: https://discuss.python.org/c/documentation
