:mod:`!pydoc` --- Trình tạo tài liệu và hệ thống trợ giúp trực tuyến
====================================================================

.. module:: pydoc
   :synopsis: Trình tạo tài liệu và hệ thống trợ giúp trực tuyến.

.. moduleauthor:: Ka-Ping Yee <ping@lfw.org>
.. sectionauthor:: Ka-Ping Yee <ping@lfw.org>

**Mã nguồn:** :source:`Lib/pydoc.py`

.. index::
   single: documentation; generation
   single: documentation; online
   single: help; online

--------------

Mô-đun :mod:`!pydoc` tự động tạo tài liệu từ các mô-đun Python. Tài liệu có thể được hiển thị dưới dạng các trang văn bản trên console, cung cấp cho trình duyệt web hoặc lưu thành các tệp HTML.

Đối với các mô-đun, lớp, hàm và phương thức, tài liệu được hiển thị bắt nguồn từ docstring (tức là thuộc tính :attr:`~definition.__doc__`) của đối tượng và đệ quy từ các thành viên có thể lập tài liệu của đối tượng đó. Nếu không có docstring,
:mod:`!pydoc` cố gắng lấy phần mô tả từ khối các dòng chú thích ngay phía trên phần định nghĩa lớp, hàm hoặc phương thức trong tệp nguồn, hoặc ở đầu mô-đun (xem :func:`inspect.getcomments`).

Hàm dựng sẵn :func:`help` gọi hệ thống trợ giúp trực tuyến trong trình thông dịch tương tác; hệ thống này sử dụng :mod:`!pydoc` để tạo tài liệu dưới dạng văn bản trên console. Bạn cũng có thể xem tài liệu văn bản tương tự từ bên ngoài trình thông dịch Python bằng cách chạy :program:`pydoc` dưới dạng một script tại dấu nhắc lệnh của hệ điều hành. Ví dụ, khi chạy::

   python -m pydoc sys

tại dấu nhắc shell sẽ hiển thị tài liệu về module :mod:`sys`, theo phong cách tương tự các trang hướng dẫn được hiển thị bằng lệnh Unix :program:`man`. Đối số của :program:`pydoc` có thể là tên của một function, module hoặc package, hoặc tham chiếu có dấu chấm đến một class, method hoặc function bên trong một module hoặc module trong một package. Nếu đối số của :program:`pydoc` trông giống một đường dẫn (nghĩa là chứa dấu phân cách đường dẫn của hệ điều hành, chẳng hạn như dấu gạch chéo trong Unix) và trỏ đến một tệp mã nguồn Python hiện có, thì tài liệu sẽ được tạo cho tệp đó.

.. note::

   Để tìm các object và tài liệu của chúng, :mod:`!pydoc` sẽ import các module cần được lập tài liệu. Do đó, mọi mã ở cấp module sẽ được thực thi vào thời điểm đó. Hãy sử dụng một guard ``if __name__ == '__main__':`` để chỉ thực thi mã khi tệp được gọi dưới dạng script, thay vì chỉ được import.

Khi in đầu ra ra console, :program:`pydoc` sẽ cố gắng phân trang đầu ra để dễ đọc hơn. Nếu :envvar:`MANPAGER` hoặc
biến môi trường :envvar:`PAGER` được thiết lập, :program:`pydoc` sẽ sử dụng giá trị của biến này làm chương trình phân trang. Khi cả hai được thiết lập, :envvar:`MANPAGER` sẽ được sử dụng.

Việc chỉ định cờ ``-w`` trước đối số sẽ khiến tài liệu HTML được ghi vào một tệp trong thư mục hiện tại, thay vì hiển thị văn bản trên console.

Việc chỉ định cờ ``-k`` trước đối số sẽ tìm kiếm các dòng tóm tắt của tất cả module hiện có để tìm từ khóa được cung cấp làm đối số, một lần nữa theo cách tương tự lệnh Unix :program:`man`. Dòng tóm tắt của một module là dòng đầu tiên trong chuỗi tài liệu của module đó.

Bạn cũng có thể sử dụng :program:`pydoc` để khởi động một HTTP server trên máy cục bộ, server này sẽ cung cấp tài liệu cho các trình duyệt web truy cập. :program:`python -m pydoc -p 1234` sẽ khởi động HTTP server trên cổng 1234, cho phép bạn duyệt tài liệu tại ``http://localhost:1234/`` bằng trình duyệt web ưa thích. Việc chỉ định ``0`` làm số cổng sẽ chọn một cổng chưa được sử dụng bất kỳ.

.. warning::

   Máy chủ HTTP :mod:`!pydoc` предназначен cho việc sử dụng cục bộ trong quá trình phát triển và không phù hợp để sử dụng trong môi trường production.

:program:`python -m pydoc -n <hostname>` sẽ khởi động máy chủ và lắng nghe tại hostname đã cho. Theo mặc định, hostname là 'localhost', nhưng nếu muốn các máy khác truy cập được máy chủ, bạn có thể thay đổi hostname mà máy chủ phản hồi. Trong quá trình phát triển, điều này đặc biệt hữu ích nếu bạn muốn chạy pydoc bên trong một container.

:program:`python -m pydoc -b` sẽ khởi động máy chủ và đồng thời mở trình duyệt web đến trang chỉ mục module. Mỗi trang được cung cấp đều có thanh điều hướng ở đầu trang, tại đó bạn có thể *Get* trợ giúp về một mục riêng lẻ, *Search* tất cả module có từ khóa trong dòng tóm tắt, cũng như chuyển đến các trang *Module index*, *Topics* và *Keywords*.

Khi :program:`pydoc` tạo tài liệu, nó sử dụng environment và path hiện tại để định vị các module. Vì vậy, việc gọi :program:`pydoc spam` sẽ lập tài liệu chính xác phiên bản của module mà bạn sẽ nhận được nếu khởi động Python interpreter và nhập ``import spam``.

Tài liệu module cho các core module được giả định nằm trong ``https://docs.python.org/X.Y/library/``, trong đó ``X`` và ``Y`` lần lượt là số phiên bản major và minor của Python interpreter. Bạn có thể ghi đè thiết lập này bằng cách đặt biến môi trường :envvar:`!PYTHONDOCS` thành một URL khác hoặc một thư mục cục bộ chứa các trang của Library Reference Manual.

.. versionchanged:: 3.2
   Đã thêm tùy chọn ``-b``.

.. versionchanged:: 3.3
   Tùy chọn dòng lệnh ``-g`` đã bị xóa.

.. versionchanged:: 3.4
   :mod:`!pydoc` now uses :func:`inspect.signature` rather than
   :func:`inspect.getfullargspec` to extract signature information from
   các đối tượng có thể gọi.

.. versionchanged:: 3.7
   Đã thêm tùy chọn ``-n``.
