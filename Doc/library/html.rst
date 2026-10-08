:mod:`!html` --- Hỗ trợ HyperText Markup Language
=================================================

.. module:: html
   :synopsis: Các hàm hỗ trợ để thao tác với HTML.

**Mã nguồn:** :source:`Lib/html/__init__.py`

--------------

Mô-đun này định nghĩa các tiện ích để thao tác với HTML.

.. function:: escape(s, quote=True)

   Chuyển đổi các ký tự ``&``, ``<`` và ``>`` trong chuỗi *s* thành các chuỗi an toàn cho HTML. Sử dụng hàm này nếu bạn cần hiển thị văn bản có thể chứa những ký tự đó trong HTML. Nếu cờ tùy chọn *quote* là true (mặc định), các ký tự (``"``) và (``'``) cũng được chuyển đổi; điều này hữu ích khi đưa vào giá trị thuộc tính HTML được bao quanh bằng dấu ngoặc kép, như trong ``<a href="...">``. Nếu *quote* được đặt thành false, các ký tự (``"``) và (``'``) sẽ không được chuyển đổi.


   .. versionadded:: 3.2


.. function:: unescape(s)

   Chuyển đổi tất cả các tham chiếu ký tự có tên và dạng số (ví dụ: ``&gt;``, ``&#62;``, ``&#x3e;``) trong chuỗi *s* thành các ký tự Unicode tương ứng. Hàm này sử dụng các quy tắc được định nghĩa trong tiêu chuẩn HTML 5 cho cả các tham chiếu ký tự hợp lệ và không hợp lệ, cùng với :data:`list of HTML 5 named character references <html.entities.html5>`.

   .. versionadded:: 3.4

--------------

Các mô-đun con trong gói ``html`` là:

* :mod:`html.parser` -- trình phân tích cú pháp HTML/XHTML với chế độ phân tích cú pháp linh hoạt
* :mod:`html.entities` -- các định nghĩa thực thể HTML
