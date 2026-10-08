:mod:`!unicodedata` --- Cơ sở dữ liệu Unicode
=============================================

.. module:: unicodedata
   :synopsis: Truy cập Cơ sở dữ liệu Unicode.

.. moduleauthor:: Marc-André Lemburg <mal@lemburg.com>
.. sectionauthor:: Marc-André Lemburg <mal@lemburg.com>
.. sectionauthor:: Martin v. Löwis <martin@v.loewis.de>

.. index::
   single: Unicode
   single: character
   pair: Unicode; database

--------------

Mô-đun này cung cấp quyền truy cập vào Unicode Character Database (UCD), nơi định nghĩa các thuộc tính ký tự cho tất cả ký tự Unicode. Dữ liệu trong cơ sở dữ liệu này được biên soạn từ `UCD version 16.0.0 <https://www.unicode.org/Public/16.0.0/ucd>`_.

Mô-đun này sử dụng cùng các tên và ký hiệu được định nghĩa trong Unicode Standard Annex #44, `"Unicode Character Database" <https://www.unicode.org/reports/tr44/>`_. Mô-đun định nghĩa các hàm sau:

.. seealso::

   Xem :ref:`unicode-howto` để biết thêm thông tin về Unicode và cách sử dụng mô-đun này.


.. function:: lookup(name)

   Tra cứu ký tự theo tên. Nếu tìm thấy ký tự có tên đã cho, trả về ký tự tương ứng. Nếu không tìm thấy, :exc:`KeyError` sẽ được phát sinh. Ví dụ:::

      >>> unicodedata.lookup('LEFT CURLY BRACKET')
      '{'

   Các ký tự được hàm này trả về giống với các ký tự được tạo bởi ``\N`` escape sequence trong string literal. Ví dụ:::

      >>> unicodedata.lookup('MIDDLE DOT') == '\N{MIDDLE DOT}'
      True

   .. versionchanged:: 3.3
      Đã bổ sung hỗ trợ cho bí danh tên [#]_ và các chuỗi có tên [#]_.


.. function:: name(chr, default=None, /)

   Trả về tên được gán cho ký tự *chr* dưới dạng chuỗi. Nếu không có tên nào được định nghĩa, *default* sẽ được trả về; nếu không cung cấp giá trị này, :exc:`ValueError` sẽ được nêu ra. Ví dụ::

      >>> unicodedata.name('½')
      'VULGAR FRACTION ONE HALF'
      >>> unicodedata.name('\uFFFF', 'fallback')
      'fallback'


.. function:: decimal(chr, default=None, /)

   Trả về giá trị thập phân được gán cho ký tự *chr* dưới dạng số nguyên. Nếu không có giá trị như vậy được định nghĩa, *default* sẽ được trả về; nếu không cung cấp giá trị này,
   :exc:`ValueError` sẽ được nêu ra. Ví dụ::

      >>> unicodedata.decimal('\N{ARABIC-INDIC DIGIT NINE}')
      9
      >>> unicodedata.decimal('\N{SUPERSCRIPT NINE}', -1)
      -1


.. function:: digit(chr, default=None, /)

   Trả về giá trị chữ số được gán cho ký tự *chr* dưới dạng số nguyên. Nếu không có giá trị như vậy được định nghĩa, *default* sẽ được trả về; nếu không cung cấp giá trị này,
   :exc:`ValueError` sẽ được nêu ra::

      >>> unicodedata.digit('\N{SUPERSCRIPT NINE}')
      9


.. function:: numeric(chr, default=None, /)

   Trả về giá trị số được gán cho ký tự *chr* dưới dạng số thực. Nếu không có giá trị như vậy được định nghĩa, *default* sẽ được trả về; nếu không cung cấp giá trị này,
   :exc:`ValueError` sẽ được nêu ra::

      >>> unicodedata.numeric('½')
      0.5


.. function:: category(chr)

   Trả về danh mục chung được gán cho ký tự *chr* dưới dạng chuỗi. Tên danh mục chung gồm hai chữ cái. Xem `phần Các giá trị danh mục chung trong tài liệu Cơ sở dữ liệu ký tự Unicode <https://www.unicode.org/reports/tr44/tr44-34.html#General_Category_Values>`_ để biết danh sách mã danh mục. Ví dụ::

      >>> unicodedata.category('A')  # 'L'etter, 'u'ppercase
      'Lu'


.. function:: bidirectional(chr)

   Trả về lớp hai chiều được gán cho ký tự *chr* dưới dạng chuỗi. Nếu không xác định giá trị tương ứng, một chuỗi rỗng sẽ được trả về. Xem `phần Các giá trị lớp hai chiều trong tài liệu Cơ sở dữ liệu ký tự Unicode <https://www.unicode.org/reports/tr44/tr44-34.html#Bidi_Class_Values>`_ để biết danh sách mã hai chiều. Ví dụ::

      >>> unicodedata.bidirectional('\N{ARABIC-INDIC DIGIT SEVEN}') # 'A'rabic, 'N'umber
      'AN'


.. function:: combining(chr)

   Trả về lớp kết hợp chuẩn được gán cho ký tự *chr* dưới dạng số nguyên. Trả về ``0`` nếu không xác định lớp kết hợp. Xem `phần Các giá trị lớp kết hợp chuẩn trong Cơ sở dữ liệu ký tự Unicode <https://www.unicode.org/reports/tr44/tr44-34.html#Canonical_Combining_Class_Values>`_ để biết thêm thông tin.


.. function:: east_asian_width(chr)

   Trả về độ rộng Đông Á được gán cho ký tự *chr* dưới dạng chuỗi. Để xem danh sách độ rộng và biết thêm thông tin, hãy xem `Unicode Standard Annex #11 <https://www.unicode.org/reports/tr11/tr11-43.html>`_.


.. function:: mirrored(chr)

   Trả về thuộc tính mirrored được gán cho ký tự *chr* dưới dạng số nguyên. Trả về ``1`` nếu ký tự được xác định là ký tự "mirrored" trong văn bản hai chiều, và ``0`` trong các trường hợp khác. Ví dụ::

      >>> unicodedata.mirrored('>')
      1


.. function:: decomposition(chr)

   Trả về ánh xạ phân rã ký tự được gán cho ký tự *chr* dưới dạng chuỗi. Một chuỗi rỗng được trả về nếu không có ánh xạ như vậy được định nghĩa. Ví dụ::

      >>> unicodedata.decomposition('Ã')
      '0041 0303'


.. function:: normalize(form, unistr)

   Trả về dạng chuẩn *form* cho chuỗi Unicode *unistr*. Các giá trị hợp lệ cho *form* là 'NFC', 'NFKC', 'NFD' và 'NFKD'.

   Tiêu chuẩn Unicode định nghĩa nhiều dạng chuẩn hóa khác nhau của một chuỗi Unicode, dựa trên định nghĩa về tương đương chính tắc và tương đương tương thích. Trong Unicode, một số ký tự có thể được biểu diễn theo nhiều cách khác nhau. Ví dụ, ký tự U+00C7 (LATIN CAPITAL LETTER C WITH CEDILLA) cũng có thể được biểu diễn dưới dạng dãy U+0043 (LATIN CAPITAL LETTER C) U+0327 (COMBINING CEDILLA).

   Với mỗi ký tự, có hai dạng chuẩn: dạng chuẩn C và dạng chuẩn D. Dạng chuẩn D (NFD) còn được gọi là phân rã chính tắc, và chuyển mỗi ký tự thành dạng đã phân rã của nó. Dạng chuẩn C (NFC) trước tiên áp dụng phép phân rã chính tắc, sau đó lại kết hợp các ký tự đã được kết hợp sẵn.

   Ngoài hai dạng này, còn có thêm hai dạng chuẩn dựa trên tương đương tương thích. Trong Unicode, một số ký tự được hỗ trợ mặc dù thông thường chúng sẽ được hợp nhất với các ký tự khác. Ví dụ, U+2160 (ROMAN NUMERAL ONE) thực chất giống với U+0049 (LATIN CAPITAL LETTER I). Tuy nhiên, ký tự này được hỗ trợ trong Unicode để tương thích với các bộ ký tự hiện có (ví dụ: gb2312).

   Dạng chuẩn KD (NFKD) sẽ áp dụng phép phân rã tương thích, tức là thay thế tất cả các ký tự tương thích bằng các ký tự tương đương của chúng. Dạng chuẩn KC (NFKC) trước tiên áp dụng phép phân rã tương thích, sau đó là phép hợp thành chính tắc.

   Ngay cả khi hai chuỗi Unicode được chuẩn hóa và trông giống nhau đối với người đọc, nếu một chuỗi có các ký tự kết hợp còn chuỗi kia thì không, chúng có thể không được xem là bằng nhau khi so sánh.


.. function:: is_normalized(form, unistr)

   Trả về liệu chuỗi Unicode *unistr* có ở dạng chuẩn *form* hay không. Các giá trị hợp lệ cho *form* là 'NFC', 'NFKC', 'NFD' và 'NFKD'.

   .. versionadded:: 3.8


Ngoài ra, module còn cung cấp hằng số sau:

.. data:: unidata_version

   Phiên bản của cơ sở dữ liệu Unicode được sử dụng trong module này.


.. data:: ucd_3_2_0

   Đây là một đối tượng có các phương thức giống như toàn bộ module, nhưng thay vào đó sử dụng phiên bản 3.2 của cơ sở dữ liệu Unicode, dành cho các ứng dụng yêu cầu phiên bản cụ thể này của cơ sở dữ liệu Unicode (chẳng hạn như IDNA).


.. rubric:: Chú thích

.. [#] https://www.unicode.org/Public/16.0.0/ucd/NameAliases.txt

.. [#] https://www.unicode.org/Public/16.0.0/ucd/NamedSequences.txt

.. _`UCD version 16.0.0`: https://www.unicode.org/Public/16.0.0/ucd
.. _`"Unicode Character Database"`: https://www.unicode.org/reports/tr44/
.. _`General Category Values section of the Unicode Character Database documentation`: https://www.unicode.org/reports/tr44/tr44-34.html#General_Category_Values
.. _`Bidirectional Class Values section of the Unicode Character Database`: https://www.unicode.org/reports/tr44/tr44-34.html#Bidi_Class_Values
.. _`Canonical Combining Class Values section of the Unicode Character Database`: https://www.unicode.org/reports/tr44/tr44-34.html#Canonical_Combining_Class_Values
.. _`Unicode Standard Annex #11`: https://www.unicode.org/reports/tr11/tr11-43.html
