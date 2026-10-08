:mod:`!token` --- Các hằng số được sử dụng với cây phân tích cú pháp Python
===========================================================================

.. module:: token
   :synopsis: Các hằng số biểu diễn các nút tận cùng của cây phân tích cú pháp.

.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>

**Mã nguồn:** :source:`Lib/token.py`

--------------

Mô-đun này cung cấp các hằng số biểu diễn giá trị số của các nút lá trong cây phân tích cú pháp (các token đầu cuối). Tham khảo tệp :file:`Grammar/Tokens` trong bản phân phối Python để xem định nghĩa của các tên trong ngữ cảnh ngữ pháp của ngôn ngữ. Các giá trị số cụ thể mà những tên này ánh xạ tới có thể thay đổi giữa các phiên bản Python.

Mô-đun này cũng cung cấp ánh xạ từ mã số tới tên và một số hàm. Các hàm này phản ánh những định nghĩa trong các tệp header C của Python.

Lưu ý rằng giá trị của một token có thể phụ thuộc vào các tùy chọn tokenizer. Ví dụ: một token ``"+"`` có thể được báo cáo là :data:`PLUS` hoặc :data:`OP`, hoặc một token ``"match"`` có thể là :data:`NAME` hoặc :data:`SOFT_KEYWORD`.


.. data:: tok_name

   Từ điển ánh xạ các giá trị số của những hằng số được định nghĩa trong mô-đun này ngược lại về các chuỗi tên, cho phép tạo ra biểu diễn dễ đọc hơn đối với các cây phân tích cú pháp.


.. function:: ISTERMINAL(x)

   Trả về ``True`` cho các giá trị token đầu cuối.


.. function:: ISNONTERMINAL(x)

   Trả về ``True`` cho các giá trị token không đầu cuối.


.. function:: ISEOF(x)

   Trả về ``True`` nếu *x* là dấu hiệu cho biết đã kết thúc đầu vào.


Các hằng số token gồm:

.. data:: NAME

   Giá trị token cho biết một :ref:`identifier hoặc keyword <identifiers>`.

.. data:: NUMBER

   Giá trị token cho biết một :ref:`numeric literal <numbers>`

.. data:: STRING

   Giá trị token cho biết một :ref:`string hoặc byte literal <strings>`, không bao gồm :ref:`formatted string literals <f-strings>`. Chuỗi token không được diễn giải: chuỗi này bao gồm dấu ngoặc kép bao quanh và tiền tố (nếu có); các dấu gạch chéo ngược được giữ nguyên, không xử lý các chuỗi thoát.

.. data:: OP

   Một giá trị token chung biểu thị một
   :ref:`operator <operators>` hoặc :ref:`delimiter <delimiters>`.

   .. impl-detail::

      Giá trị này chỉ được module :mod:`tokenize` báo cáo. Bên trong, tokenizer sử dụng
      :ref:`exact token types <token_operators_delimiters>` thay vào đó.

.. data:: COMMENT

   Giá trị token dùng để biểu thị một comment. Parser bỏ qua các token :data:`!COMMENT`.

.. data:: NEWLINE

   Giá trị token biểu thị phần cuối của một :ref:`logical line <logical-lines>`.

.. data:: NL

   Giá trị token dùng để biểu thị một dòng mới không kết thúc.
   Các token :data:`!NL` được tạo khi một dòng logic của mã được tiếp tục trên nhiều dòng vật lý. Trình phân tích cú pháp bỏ qua các token :data:`!NL`.

.. data:: INDENT

   Giá trị token được sử dụng ở đầu :ref:`dòng logic <logical-lines>` để biểu thị phần bắt đầu của :ref:`khối thụt lề <indentation>`.

.. data:: DEDENT

   Giá trị token được sử dụng ở đầu :ref:`dòng logic <logical-lines>` để biểu thị phần kết thúc của :ref:`khối thụt lề <indentation>`.

.. data:: FSTRING_START

   Giá trị token được sử dụng để biểu thị phần bắt đầu của một
   :ref:`literal f-string <f-strings>`.

   .. impl-detail::

      Chuỗi token bao gồm tiền tố và (các) dấu nháy mở, nhưng không bao gồm bất kỳ nội dung nào của literal.

.. data:: FSTRING_MIDDLE

   Giá trị token được sử dụng cho văn bản literal bên trong :ref:`literal f-string <f-strings>`, bao gồm cả các đặc tả định dạng.

   .. impl-detail::

      Các trường thay thế (tức là những phần không phải literal của f-string) sử dụng cùng các token như những biểu thức khác và được phân cách bằng
      :data:`LBRACE`, :data:`RBRACE`, :data:`EXCLAMATION` và :data:`COLON`.

.. data:: FSTRING_END

   Giá trị token được dùng để biểu thị phần kết thúc của :ref:`f-string <f-strings>`.

   .. impl-detail::

      Chuỗi token chứa dấu ngoặc kép đóng.

.. data:: TSTRING_START

   Giá trị token được dùng để biểu thị phần bắt đầu của một template string literal.

   .. impl-detail::

      Chuỗi token bao gồm tiền tố và (các) dấu nháy mở, nhưng không bao gồm bất kỳ nội dung nào của literal.

   .. versionadded:: 3.14

.. data:: TSTRING_MIDDLE

   Giá trị token được dùng cho văn bản literal bên trong một template string literal, bao gồm cả các đặc tả định dạng.

   .. impl-detail::

      Các trường thay thế (tức là những phần không phải literal của t-strings) sử dụng cùng các token như những biểu thức khác và được phân tách bằng
      :data:`LBRACE`, :data:`RBRACE`, :data:`EXCLAMATION` và :data:`COLON`.

   .. versionadded:: 3.14

.. data:: TSTRING_END

   Giá trị token dùng để chỉ phần kết thúc của một literal chuỗi mẫu.

   .. impl-detail::

      Chuỗi token chứa dấu ngoặc kép đóng.

   .. versionadded:: 3.14

.. data:: ENDMARKER

   Giá trị token cho biết phần kết thúc của đầu vào. Được sử dụng trong :ref:`các quy tắc ngữ pháp cấp cao nhất <top-level>`.

.. data:: ENCODING

   Giá trị token cho biết encoding được dùng để giải mã các byte nguồn thành văn bản. Token đầu tiên được :func:`tokenize.tokenize` trả về sẽ luôn là một token ``ENCODING``.

   .. impl-detail::

      Loại token này không được C tokenizer sử dụng nhưng cần thiết cho module :mod:`tokenize`.


Các loại token sau đây không được module :mod:`tokenize` tạo ra và được định nghĩa để sử dụng cho các mục đích đặc biệt trong tokenizer hoặc parser:

.. data:: TYPE_IGNORE

   Giá trị token cho biết một comment ``type: ignore`` đã được nhận diện. Các token như vậy chỉ được tạo ra thay cho các token :data:`COMMENT` thông thường khi có cờ :data:`~ast.PyCF_TYPE_COMMENTS`.

.. data:: TYPE_COMMENT

   Giá trị token cho biết một type comment đã được nhận diện. Các token như vậy chỉ được tạo ra thay cho các token :data:`COMMENT` thông thường khi có cờ :data:`~ast.PyCF_TYPE_COMMENTS`.

.. data:: SOFT_KEYWORD

   Giá trị token cho biết một :ref:`soft keyword <soft-keywords>`.

   Tokenizer không bao giờ tạo ra giá trị này. Để kiểm tra một soft keyword, hãy truyền chuỗi của token :data:`NAME` cho
   :func:`keyword.issoftkeyword`.

.. data:: ERRORTOKEN

   Giá trị token được dùng để cho biết đầu vào không hợp lệ.

   Module :mod:`tokenize` thường cho biết lỗi bằng cách raise exception thay vì phát ra token này. Module này cũng có thể phát ra các token như :data:`OP` hoặc :data:`NAME` với những chuỗi về sau bị parser từ chối.


.. _token_operators_delimiters:

Các token còn lại biểu diễn các :ref:`toán tử <operators>` cụ thể và
các :ref:`dấu phân cách <delimiters>`. (Mô-đun :mod:`tokenize` báo cáo chúng dưới dạng :data:`OP`; xem ``exact_type`` trong tài liệu :mod:`tokenize` để biết chi tiết.)

.. include:: token-list.inc


Các hằng số không phải token sau đây được cung cấp:

.. data:: N_TOKENS

   Số lượng loại token được định nghĩa trong mô-đun này.

.. NT_OFFSET is deliberately undocumented; if you need it you should be
   reading the source

.. data:: EXACT_TOKEN_TYPES

   Một từ điển ánh xạ biểu diễn chuỗi của một token với mã số của token đó.

   .. versionadded:: 3.8


.. versionchanged:: 3.5
   Đã thêm các token :data:`!AWAIT` và :data:`!ASYNC`.

.. versionchanged:: 3.7
   Đã thêm các token :data:`COMMENT`, :data:`NL` và :data:`ENCODING`.

.. versionchanged:: 3.7
   Đã loại bỏ các token :data:`!AWAIT` và :data:`!ASYNC`. "async" và "await" hiện được token hóa thành các token :data:`NAME`.

.. versionchanged:: 3.8
   Đã thêm :data:`TYPE_COMMENT`, :data:`TYPE_IGNORE`, :data:`COLONEQUAL`. Đã thêm lại các token :data:`!AWAIT` và :data:`!ASYNC` (chúng cần thiết để hỗ trợ phân tích cú pháp các phiên bản Python cũ hơn cho :func:`ast.parse` khi ``feature_version`` được đặt thành 6 hoặc thấp hơn).

.. versionchanged:: 3.12
   Đã thêm :data:`EXCLAMATION`.

.. versionchanged:: 3.13
   Đã loại bỏ lại các token :data:`!AWAIT` và :data:`!ASYNC`.

