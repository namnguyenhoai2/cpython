.. _unicode-howto:

****************
HOWTO về Unicode
****************

:Release: 1.12

HOWTO này thảo luận về khả năng hỗ trợ đặc tả Unicode của Python trong việc biểu diễn dữ liệu văn bản, đồng thời giải thích nhiều vấn đề thường gặp khi làm việc với Unicode.


Giới thiệu về Unicode
=====================

Định nghĩa
----------

Các chương trình ngày nay cần có khả năng xử lý rất nhiều loại ký tự. Các ứng dụng thường được quốc tế hóa để hiển thị thông báo và đầu ra bằng nhiều ngôn ngữ do người dùng lựa chọn; cùng một chương trình có thể cần xuất thông báo lỗi bằng tiếng Anh, tiếng Pháp, tiếng Nhật, tiếng Hebrew hoặc tiếng Nga. Nội dung web có thể được viết bằng bất kỳ ngôn ngữ nào trong số này và cũng có thể bao gồm nhiều biểu tượng emoji. Kiểu chuỗi của Python sử dụng Unicode Standard để biểu diễn ký tự, cho phép các chương trình Python làm việc với tất cả những ký tự khác nhau này.

Unicode (https://www.unicode.org/) là một đặc tả nhằm liệt kê mọi ký tự được sử dụng trong các ngôn ngữ của con người và cấp cho mỗi ký tự một mã duy nhất. Các đặc tả Unicode liên tục được sửa đổi và cập nhật để bổ sung ngôn ngữ và biểu tượng mới.

Một **ký tự** là thành phần nhỏ nhất có thể có của văn bản. 'A', 'B', 'C', v.v. đều là các ký tự khác nhau. 'È' và 'Í' cũng vậy. Ký tự thay đổi tùy theo ngôn ngữ hoặc ngữ cảnh mà bạn đang nói đến. Ví dụ: có một ký tự cho "Chữ số La Mã Một", 'Ⅰ', riêng biệt với chữ cái viết hoa 'I'. Thông thường chúng sẽ trông giống nhau, nhưng đây là hai ký tự khác nhau với ý nghĩa khác nhau.

Tiêu chuẩn Unicode mô tả cách các ký tự được biểu diễn bằng **các điểm mã**. Giá trị điểm mã là một số nguyên trong phạm vi từ 0 đến 0x10FFFF (khoảng 1,1 triệu giá trị; `số lượng thực tế được gán <https://www.unicode.org/versions/latest/#Summary>`_ nhỏ hơn con số đó). Trong tiêu chuẩn và trong tài liệu này, một điểm mã được viết bằng ký hiệu ``U+265E`` để chỉ ký tự có giá trị ``0x265e`` (9.822 ở dạng thập phân).

Tiêu chuẩn Unicode chứa rất nhiều bảng liệt kê các ký tự và điểm mã tương ứng của chúng:

.. code-block:: none

   0061    'a'; LATIN SMALL LETTER A
   0062    'b'; LATIN SMALL LETTER B
   0063    'c'; LATIN SMALL LETTER C
   ...
   007B    '{'; LEFT CURLY BRACKET
   ...
   2167    'Ⅷ'; ROMAN NUMERAL EIGHT
   2168    'Ⅸ'; ROMAN NUMERAL NINE
   ...
   265E    '♞'; BLACK CHESS KNIGHT
   265F    '♟'; BLACK CHESS PAWN
   ...
   1F600   '😀'; GRINNING FACE
   1F609   '😉'; WINKING FACE
   ...

Nói chính xác, các định nghĩa này ngụ ý rằng việc nói “đây là ký tự ``U+265E``” là vô nghĩa. ``U+265E`` là một điểm mã, đại diện cho một ký tự cụ thể nào đó; trong trường hợp này, nó đại diện cho ký tự “BLACK CHESS KNIGHT”, “♞”. Trong các ngữ cảnh không chính thức, đôi khi sự khác biệt giữa điểm mã và ký tự sẽ bị bỏ qua.

Một ký tự được biểu diễn trên màn hình hoặc trên giấy bằng một tập hợp các thành phần đồ họa gọi là **glyph**. Ví dụ, glyph của chữ A viết hoa gồm hai nét chéo và một nét ngang, mặc dù các chi tiết chính xác sẽ phụ thuộc vào font đang được sử dụng. Phần lớn mã Python không cần quan tâm đến glyph; việc xác định glyph phù hợp để hiển thị thường là nhiệm vụ của GUI toolkit hoặc bộ kết xuất font của terminal.


Encodings
---------

Tóm tắt phần trước: một chuỗi Unicode là một dãy các điểm mã, là những số từ 0 đến ``0x10FFFF`` (1.114.111 ở dạng thập phân). Dãy điểm mã này cần được biểu diễn trong bộ nhớ dưới dạng một tập hợp **đơn vị mã**, sau đó **các đơn vị mã** được ánh xạ thành các byte 8 bit. Các quy tắc chuyển đổi một chuỗi Unicode thành một dãy byte được gọi là **mã hóa ký tự**, hoặc đơn giản là **mã hóa**.

Encoding đầu tiên bạn có thể nghĩ đến là sử dụng các số nguyên 32 bit làm đơn vị mã, sau đó sử dụng cách CPU biểu diễn các số nguyên 32 bit. Trong cách biểu diễn này, chuỗi "Python" có thể trông như sau:

.. code-block:: none

       P           y           t           h           o           n
    0x50 00 00 00 79 00 00 00 74 00 00 00 68 00 00 00 6f 00 00 00 6e 00 00 00
       0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23

Biểu diễn này khá trực tiếp, nhưng việc sử dụng nó gây ra một số vấn đề.

1. Nó không có tính khả chuyển; các bộ xử lý khác nhau sắp xếp các byte theo những thứ tự khác nhau.

2. Nó sử dụng không gian rất lãng phí. Trong hầu hết văn bản, phần lớn các code point nhỏ hơn 127 hoặc nhỏ hơn 255, vì vậy rất nhiều không gian bị chiếm bởi các byte ``0x00``. Chuỗi trên chiếm 24 byte, so với 6 byte cần thiết cho biểu diễn ASCII. Việc tăng mức sử dụng RAM không quá quan trọng (máy tính để bàn có hàng gigabyte RAM và các chuỗi thường không lớn đến vậy), nhưng việc mở rộng mức sử dụng dung lượng đĩa và băng thông mạng lên 4 lần là không thể chấp nhận được.

3. Nó không tương thích với các hàm C hiện có như ``strlen()``, vì vậy cần sử dụng một nhóm hàm chuỗi wide mới.

Do đó, encoding này không được sử dụng nhiều, và thay vào đó mọi người chọn các encoding hiệu quả, thuận tiện hơn như UTF-8.

UTF-8 là một trong những encoding được sử dụng phổ biến nhất và Python thường mặc định sử dụng nó. UTF là viết tắt của "Unicode Transformation Format", còn '8' nghĩa là encoding sử dụng các giá trị 8 bit. (Ngoài ra còn có các encoding UTF-16 và UTF-32, nhưng chúng ít được sử dụng hơn UTF-8.) UTF-8 sử dụng các quy tắc sau:

1. Nếu code point nhỏ hơn 128, nó được biểu diễn bằng giá trị byte tương ứng.
2. Nếu code point >= 128, nó sẽ được chuyển thành một chuỗi gồm hai, ba hoặc bốn byte, trong đó mỗi byte của chuỗi nằm trong khoảng từ 128 đến 255.

UTF-8 có một số thuộc tính tiện lợi:

1. Nó có thể xử lý mọi code point Unicode.
2. Một chuỗi Unicode được chuyển thành một chuỗi byte chỉ chứa các byte 0 được chèn vào khi chúng biểu diễn ký tự null (U+0000). Điều này có nghĩa là các chuỗi UTF-8 có thể được xử lý bởi những hàm C như ``strcpy()`` và được truyền qua các giao thức không thể xử lý byte 0 cho mục đích nào khác ngoài việc đánh dấu kết thúc chuỗi.
3. Một chuỗi văn bản ASCII cũng là văn bản UTF-8 hợp lệ.
4. UTF-8 khá gọn; phần lớn các ký tự thường dùng có thể được biểu diễn bằng một hoặc hai byte.
5. Nếu các byte bị hỏng hoặc bị mất, ta vẫn có thể xác định phần bắt đầu của code point được mã hóa bằng UTF-8 tiếp theo và đồng bộ lại. Dữ liệu 8 bit ngẫu nhiên cũng khó có khả năng trông giống UTF-8 hợp lệ.
6. UTF-8 là một kiểu mã hóa hướng byte. Kiểu mã hóa này quy định rằng mỗi ký tự được biểu diễn bằng một chuỗi cụ thể gồm một hoặc nhiều byte. Điều này tránh được các vấn đề về thứ tự byte có thể xảy ra với các kiểu mã hóa hướng số nguyên và hướng word, như UTF-16 và UTF-32, trong đó chuỗi byte thay đổi tùy thuộc vào phần cứng mà trên đó chuỗi được mã hóa.


Tài liệu tham khảo
------------------

`Trang web của Unicode Consortium <https://www.unicode.org>`_ có các biểu đồ ký tự, bảng thuật ngữ và các phiên bản PDF của đặc tả Unicode. Hãy chuẩn bị tinh thần cho một số nội dung khó đọc. Trên trang web cũng có `một niên biểu <https://www.unicode.org/history/>`_ về nguồn gốc và quá trình phát triển của Unicode.

Trên kênh Youtube Computerphile, Tom Scott `thảo luận ngắn gọn về lịch sử của Unicode và UTF-8 <https://www.youtube.com/watch?v=MijmeoH9LT4>`_ (9 phút 36 giây).

Để giúp hiểu tiêu chuẩn này, Jukka Korpela đã viết `một hướng dẫn nhập môn <https://jkorpela.fi/unicode/guide.html>`_ về cách đọc các bảng ký tự Unicode.

Joel Spolsky cũng đã viết `một bài viết nhập môn hay <https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/>`_. Nếu phần giới thiệu này vẫn chưa giúp bạn hiểu rõ, hãy thử đọc bài viết thay thế này trước khi tiếp tục.

Các bài viết trên Wikipedia thường hữu ích; chẳng hạn, hãy xem các bài viết về "`mã hóa ký tự <https://en.wikipedia.org/wiki/Character_encoding>`_" và `UTF-8 <https://en.wikipedia.org/wiki/UTF-8>`_.


Hỗ trợ Unicode của Python
=========================

Bây giờ, khi đã nắm được những kiến thức cơ bản về Unicode, chúng ta có thể tìm hiểu các tính năng Unicode của Python.

Kiểu chuỗi
----------

Kể từ Python 3.0, kiểu :class:`str` của ngôn ngữ chứa các ký tự Unicode, nghĩa là mọi chuỗi được tạo bằng ``"unicode rocks!"``, ``'unicode rocks!'`` hoặc cú pháp chuỗi ba dấu ngoặc kép đều được lưu dưới dạng Unicode.

Mã hóa mặc định cho mã nguồn Python là UTF-8, vì vậy bạn có thể chỉ cần đưa một ký tự Unicode vào một string literal::

   try:
       with open('/tmp/input.txt', 'r') as f:
           ...
   except OSError:
       # Thông báo lỗi 'File not found'.
       print("Fichier non trouvé")

Lưu ý: Python 3 cũng hỗ trợ sử dụng các ký tự Unicode trong identifier::

   répertoire = "/tmp/records.log"
   with open(répertoire, "w") as f:
       f.write("test\n")

Nếu không thể nhập một ký tự cụ thể trong trình soạn thảo hoặc vì lý do nào đó muốn giữ mã nguồn chỉ chứa ASCII, bạn cũng có thể sử dụng các escape sequence trong string literal. (Tùy thuộc vào hệ thống, bạn có thể thấy glyph delta viết hoa thực tế thay vì escape \u.)::

   >>> "\N{GREEK CAPITAL LETTER DELTA}"  # Sử dụng tên ký tự
   '\u0394'
   >>> "\u0394"                          # Sử dụng giá trị hex 16-bit
   '\u0394'
   >>> "\U00000394"                      # Sử dụng giá trị hex 32-bit
   '\u0394'

Ngoài ra, bạn có thể tạo một chuỗi bằng phương thức :func:`~bytes.decode` của
:class:`bytes`. Phương thức này nhận một đối số *encoding*, chẳng hạn như ``UTF-8``, và tùy chọn nhận thêm đối số *errors*.

Đối số *errors* chỉ định cách phản hồi khi không thể chuyển đổi chuỗi đầu vào theo các quy tắc của encoding. Các giá trị hợp lệ cho đối số này là ``'strict'`` (raise một exception :exc:`UnicodeDecodeError`), ``'replace'`` (sử dụng ``U+FFFD``, ``REPLACEMENT CHARACTER``), ``'ignore'`` (chỉ cần loại bỏ ký tự khỏi kết quả Unicode), hoặc ``'backslashreplace'`` (chèn một escape sequence ``\xNN``). Các ví dụ sau đây cho thấy sự khác biệt::

    >>> b'\x80abc'.decode("utf-8", "strict")  #doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
        ...
    UnicodeDecodeError: 'utf-8' codec can't decode byte 0x80 in position 0:
      invalid start byte
    >>> b'\x80abc'.decode("utf-8", "replace")
    '\ufffdabc'
    >>> b'\x80abc'.decode("utf-8", "backslashreplace")
    '\\x80abc'
    >>> b'\x80abc'.decode("utf-8", "ignore")
    'abc'

Các encoding được chỉ định dưới dạng chuỗi chứa tên của encoding. Python đi kèm khoảng 100 encoding khác nhau; xem Python Library Reference tại
:ref:`standard-encodings` để xem danh sách. Một số encoding có nhiều tên; chẳng hạn, ``'latin-1'``, ``'iso_8859_1'`` và ``'8859``' đều là các từ đồng nghĩa của cùng một encoding.

Các chuỗi Unicode một ký tự cũng có thể được tạo bằng hàm dựng sẵn :func:`chr`, hàm này nhận các số nguyên và trả về một chuỗi Unicode có độ dài 1 chứa code point tương ứng. Thao tác ngược lại là hàm dựng sẵn :func:`ord`, nhận một chuỗi Unicode một ký tự và trả về giá trị code point::

    >>> chr(57344)
    '\ue000'
    >>> ord('\ue000')
    57344

Chuyển đổi sang Bytes
---------------------

Phương thức đối lập với :meth:`bytes.decode` là :meth:`str.encode`, trả về biểu diễn :class:`bytes` của chuỗi Unicode, được mã hóa theo *encoding* được yêu cầu.

Tham số *errors* giống với tham số của
phương thức :meth:`~bytes.decode` nhưng hỗ trợ thêm một số handler khác. Ngoài ``'strict'``, ``'ignore'`` và ``'replace'`` (trong trường hợp này chèn dấu hỏi thay cho ký tự không thể mã hóa), còn có ``'xmlcharrefreplace'`` (chèn tham chiếu ký tự XML), ``backslashreplace`` (chèn chuỗi escape ``\uNNNN``) và ``namereplace`` (chèn chuỗi escape ``\N{...}``).

Ví dụ sau đây cho thấy các kết quả khác nhau::

    >>> u = chr(40960) + 'abcd' + chr(1972)
    >>> u.encode('utf-8')
    b'\xea\x80\x80abcd\xde\xb4'
    >>> u.encode('ascii')  #doctest: +NORMALIZE_WHITESPACE
    Traceback (most recent call last):
        ...
    UnicodeEncodeError: 'ascii' codec can't encode character '\ua000' in
      position 0: ordinal not in range(128)
    >>> u.encode('ascii', 'ignore')
    b'abcd'
    >>> u.encode('ascii', 'replace')
    b'?abcd?'
    >>> u.encode('ascii', 'xmlcharrefreplace')
    b'&#40960;abcd&#1972;'
    >>> u.encode('ascii', 'backslashreplace')
    b'\\ua000abcd\\u07b4'
    >>> u.encode('ascii', 'namereplace')
    b'\\N{YI SYLLABLE IT}abcd\\u07b4'

Các routine cấp thấp để đăng ký và truy cập những encoding hiện có nằm trong module :mod:`codecs`. Việc triển khai encoding mới cũng đòi hỏi hiểu module :mod:`codecs`. Tuy nhiên, các hàm encoding và decoding do module này trả về thường ở mức thấp hơn mức thuận tiện, và viết encoding mới là một tác vụ chuyên biệt, vì vậy module này sẽ không được đề cập trong HOWTO này.


Các Unicode Literal trong Mã nguồn Python
-----------------------------------------

Trong mã nguồn Python, có thể viết các code point Unicode cụ thể bằng chuỗi escape ``\u``, theo sau là bốn chữ số thập lục phân biểu thị code point. Chuỗi escape ``\U`` tương tự, nhưng yêu cầu tám chữ số thập lục phân thay vì bốn::

    >>> s = "a\xac\u1234\u20ac\U00008000"
    ... #     ^^^^ escape hệ thập lục phân gồm hai chữ số
    ... #         ^^^^^^ escape Unicode gồm bốn chữ số
    ... #                     ^^^^^^^^^^ escape Unicode gồm tám chữ số
    >>> [ord(c) for c in s]
    [97, 172, 4660, 8364, 32768]

Sử dụng các escape sequence cho các code point lớn hơn 127 thì ổn nếu chỉ dùng ở mức độ vừa phải, nhưng sẽ trở nên phiền toái nếu bạn sử dụng nhiều ký tự có dấu, như trong một chương trình có thông báo bằng tiếng Pháp hoặc một ngôn ngữ khác dùng dấu. Bạn cũng có thể ghép chuỗi bằng hàm dựng sẵn :func:`chr`, nhưng cách này còn tốn công hơn.

Lý tưởng nhất là bạn có thể viết các literal bằng encoding tự nhiên của ngôn ngữ. Khi đó, bạn có thể chỉnh sửa mã nguồn Python bằng trình soạn thảo yêu thích, trình soạn thảo sẽ hiển thị các ký tự có dấu một cách tự nhiên, và các ký tự chính xác sẽ được sử dụng khi runtime.

Python mặc định hỗ trợ viết mã nguồn bằng UTF-8, nhưng bạn có thể sử dụng gần như bất kỳ encoding nào nếu khai báo encoding đang dùng. Việc này được thực hiện bằng cách thêm một comment đặc biệt vào dòng đầu tiên hoặc dòng thứ hai của tệp mã nguồn::

    #!/usr/bin/env python
    # -*- coding: latin-1 -*-

    u = 'abcdé'
    print(ord(u[-1]))

Cú pháp này lấy cảm hứng từ ký hiệu của Emacs dùng để chỉ định các biến cục bộ của một tệp. Emacs hỗ trợ nhiều biến khác nhau, nhưng Python chỉ hỗ trợ 'coding'. Các ký hiệu ``-*-`` cho Emacs biết rằng comment này là đặc biệt; chúng không có ý nghĩa gì đối với Python mà chỉ là một quy ước. Python tìm ``coding: name`` hoặc ``coding=name`` trong comment.

Nếu bạn không thêm chú thích như vậy, encoding mặc định được sử dụng sẽ là UTF-8 như đã đề cập. Xem thêm :pep:`263` để biết thêm thông tin.


.. _unicode-properties:

Các thuộc tính Unicode
----------------------

Đặc tả Unicode bao gồm một cơ sở dữ liệu chứa thông tin về các code point. Với mỗi code point đã được định nghĩa, thông tin bao gồm tên của ký tự, category của ký tự, giá trị số nếu có (đối với các ký tự biểu thị khái niệm số như chữ số La Mã, các phân số như một phần ba và bốn phần năm, v.v.). Ngoài ra còn có các thuộc tính liên quan đến cách hiển thị, chẳng hạn như cách sử dụng code point trong văn bản hai chiều.

Chương trình sau hiển thị một số thông tin về một vài ký tự và in ra giá trị số của một ký tự cụ thể::

    import unicodedata

    u = chr(233) + chr(0x0bf2) + chr(3972) + chr(6000) + chr(13231)

    for i, c in enumerate(u):
        print(i, '%04x' % ord(c), unicodedata.category(c), end=" ")
        print(unicodedata.name(c))

    # Lấy giá trị số của ký tự thứ hai
    print(unicodedata.numeric(u[1]))

Khi chạy, chương trình sẽ in ra:

.. code-block:: none

    0 00e9 Ll LATIN SMALL LETTER E WITH ACUTE
    1 0bf2 No TAMIL NUMBER ONE THOUSAND
    2 0f84 Mn TIBETAN MARK HALANTA
    3 1770 Lo TAGBANWA LETTER SA
    4 33af So SQUARE RAD OVER S SQUARED
    1000.0

Các mã category là những dạng viết tắt mô tả bản chất của ký tự. Chúng được nhóm thành các category như "Letter", "Number", "Punctuation" hoặc "Symbol", rồi tiếp tục được chia thành các subcategory. Lấy các mã từ kết quả đầu ra ở trên làm ví dụ, ``'Ll'`` có nghĩa là "Letter, lowercase", ``'No'`` là "Number, other", ``'Mn'`` là "Mark, nonspacing", còn ``'So'`` là "Symbol, other". Xem `phần General Category Values trong tài liệu Unicode Character Database <https://www.unicode.org/reports/tr44/#General_Category_Values>`_ để biết danh sách các mã category.


So sánh chuỗi
-------------

Unicode khiến việc so sánh chuỗi trở nên phức tạp hơn đôi chút, vì cùng một tập hợp ký tự có thể được biểu diễn bằng các dãy điểm mã khác nhau. Ví dụ, một chữ cái như 'ê' có thể được biểu diễn bằng một điểm mã duy nhất U+00EA, hoặc bằng U+0065 U+0302, trong đó điểm mã đầu tiên là 'e' và điểm mã tiếp theo là 'COMBINING CIRCUMFLEX ACCENT'. Khi được in ra, chúng sẽ cho cùng một kết quả, nhưng một chuỗi có độ dài 1 còn chuỗi kia có độ dài 2.

Một công cụ để so sánh không phân biệt chữ hoa chữ thường là phương thức chuỗi
:meth:`~str.casefold` chuyển đổi một chuỗi thành dạng không phân biệt chữ hoa chữ thường theo một thuật toán được mô tả trong Unicode Standard. Thuật toán này xử lý đặc biệt các ký tự như chữ cái tiếng Đức 'ß' (điểm mã U+00DF), ký tự này được chuyển thành cặp chữ cái thường 'ss'.

::

    >>> street = 'Gürzenichstraße'
    >>> street.casefold()
    'gürzenichstrasse'

Một công cụ thứ hai là module :mod:`unicodedata` với hàm
:func:`~unicodedata.normalize` chuyển đổi các chuỗi thành một trong một số dạng chuẩn, trong đó các chữ cái theo sau bởi một ký tự kết hợp được thay thế bằng các ký tự đơn. Có thể dùng :func:`~unicodedata.normalize` để thực hiện các phép so sánh chuỗi mà không báo cáo sai rằng hai chuỗi không bằng nhau nếu chúng sử dụng các ký tự kết hợp theo những cách khác nhau:

::

    import unicodedata

    def compare_strs(s1, s2):
        def NFD(s):
            return unicodedata.normalize('NFD', s)

        return NFD(s1) == NFD(s2)

    single_char = 'ê'
    multiple_chars = '\N{LATIN SMALL LETTER E}\N{COMBINING CIRCUMFLEX ACCENT}'
    print('length of first string=', len(single_char))
    print('length of second string=', len(multiple_chars))
    print(compare_strs(single_char, multiple_chars))

Khi chạy, đoạn này sẽ cho ra:

.. code-block:: shell-session

    $ python compare-strs.py
    length of first string= 1
    length of second string= 2
    True

Đối số đầu tiên của hàm :func:`~unicodedata.normalize` là một chuỗi chỉ định dạng chuẩn hóa mong muốn, có thể là một trong các dạng 'NFC', 'NFKC', 'NFD' và 'NFKD'.

Unicode Standard cũng quy định cách thực hiện so sánh không phân biệt chữ hoa chữ thường::

    import unicodedata

    def compare_caseless(s1, s2):
        def NFD(s):
            return unicodedata.normalize('NFD', s)

        return NFD(NFD(s1).casefold()) == NFD(NFD(s2).casefold())

    # Ví dụ sử dụng
    single_char = 'ê'
    multiple_chars = '\N{LATIN CAPITAL LETTER E}\N{COMBINING CIRCUMFLEX ACCENT}'

    print(compare_caseless(single_char, multiple_chars))

Lệnh này sẽ in ra ``True``.  (Tại sao :func:`!NFD` được gọi hai lần?  Vì có một vài ký tự khiến :meth:`~str.casefold` trả về một chuỗi chưa được chuẩn hóa, nên kết quả cần được chuẩn hóa lại. Xem mục 3.13 của Unicode Standard để biết phần thảo luận và ví dụ.)


Biểu thức chính quy Unicode
---------------------------

Các biểu thức chính quy được module :mod:`re` hỗ trợ có thể được cung cấp dưới dạng bytes hoặc chuỗi.  Một số chuỗi ký tự đặc biệt như ``\d`` và ``\w`` có ý nghĩa khác nhau tùy thuộc vào việc pattern được cung cấp dưới dạng bytes hay chuỗi.  Ví dụ, ``\d`` sẽ khớp với các ký tự ``[0-9]`` ở dạng bytes, nhưng ở dạng chuỗi sẽ khớp với mọi ký tự thuộc danh mục ``'Nd'``.

Chuỗi trong ví dụ này có số 57 được viết bằng cả chữ số Thái và chữ số Ả Rập::

   import re
   p = re.compile(r'\d+')

   s = "Over \u0e55\u0e57 57 flavours"
   m = p.search(s)
   print(repr(m.group()))

Khi được thực thi, ``\d+`` sẽ khớp với các chữ số Thái và in chúng ra. Nếu cung cấp cờ :const:`re.ASCII` cho
:func:`~re.compile`, ``\d+`` sẽ khớp với chuỗi con "57" thay vào đó.

Tương tự, ``\w`` khớp với rất nhiều ký tự Unicode, nhưng chỉ khớp với ``[a-zA-Z0-9_]`` trong bytes hoặc khi cung cấp :const:`re.ASCII`, còn ``\s`` sẽ khớp với các ký tự khoảng trắng Unicode hoặc ``[ \t\n\r\f\v]``.


Tài liệu tham khảo
------------------

.. comment should these be mentioned earlier, e.g. at the start of the "introduction to Unicode" first section?

Một số tài liệu thảo luận thay thế hữu ích về hỗ trợ Unicode của Python là:

* `Xử lý tệp văn bản trong Python 3 <https://python-notes.curiousefficiency.org/en/latest/python3/text_file_processing.html>`_, của Nick Coghlan.
* `Unicode thực dụng <https://nedbatchelder.com/text/unipain.html>`_, một bài thuyết trình tại PyCon 2012 của Ned Batchelder.

Kiểu :class:`str` được mô tả trong tài liệu tham khảo của thư viện Python tại
:ref:`textseq`.

Tài liệu về mô-đun :mod:`unicodedata`.

Tài liệu về mô-đun :mod:`codecs`.

Marc-André Lemburg đã trình bày `một bài thuyết trình có tiêu đề "Python và Unicode" (các slide PDF) <https://downloads.egenix.com/python/Unicode-EPC2002-Talk.pdf>`_ tại EuroPython 2002. Các slide này cung cấp một cái nhìn tổng quan xuất sắc về thiết kế các tính năng Unicode của Python 2 (trong đó kiểu chuỗi Unicode được gọi là ``unicode`` và các literal bắt đầu bằng ``u``).


Đọc và Ghi Dữ liệu Unicode
==========================

Sau khi viết một số mã hoạt động với dữ liệu Unicode, vấn đề tiếp theo là nhập/xuất. Làm thế nào để đưa các chuỗi Unicode vào chương trình của bạn và chuyển đổi Unicode sang dạng phù hợp để lưu trữ hoặc truyền tải?

Tùy thuộc vào nguồn đầu vào và đích đầu ra, có thể bạn không cần làm gì; bạn nên kiểm tra xem các thư viện được sử dụng trong ứng dụng của mình có hỗ trợ Unicode nguyên bản hay không. Ví dụ, các trình phân tích cú pháp XML thường trả về dữ liệu Unicode. Nhiều cơ sở dữ liệu quan hệ cũng hỗ trợ các cột chứa giá trị Unicode và có thể trả về các giá trị Unicode từ truy vấn SQL.

Dữ liệu Unicode thường được chuyển đổi sang một encoding cụ thể trước khi được ghi vào đĩa hoặc gửi qua socket. Bạn có thể tự thực hiện toàn bộ công việc: mở một tệp, đọc một đối tượng bytes 8 bit từ đó và chuyển đổi các byte bằng ``bytes.decode(encoding)``. Tuy nhiên, cách làm thủ công không được khuyến nghị.

Một vấn đề là bản chất nhiều byte của các encoding; một ký tự Unicode có thể được biểu diễn bằng nhiều byte. Nếu muốn đọc tệp theo các đoạn có kích thước tùy ý (chẳng hạn 1024 hoặc 4096 byte), bạn cần viết mã xử lý lỗi để bắt trường hợp chỉ đọc được một phần các byte mã hóa một ký tự Unicode ở cuối đoạn. Một giải pháp là đọc toàn bộ tệp vào bộ nhớ rồi thực hiện giải mã, nhưng cách này khiến bạn không thể làm việc với các tệp cực lớn; nếu cần đọc một tệp 2 GiB, bạn cần 2 GiB RAM. (Thực tế còn nhiều hơn, vì ít nhất trong một khoảng thời gian, bạn cần có cả chuỗi đã mã hóa và phiên bản Unicode của nó trong bộ nhớ.)

Giải pháp là sử dụng giao diện giải mã cấp thấp để xử lý trường hợp các chuỗi mã hóa chưa đầy đủ. Công việc triển khai việc này đã được thực hiện sẵn cho bạn: hàm tích hợp :func:`open` có thể trả về một đối tượng giống tệp, giả định rằng nội dung tệp sử dụng một encoding được chỉ định và chấp nhận các tham số Unicode cho những phương thức như :meth:`~io.TextIOBase.read` và
:meth:`~io.TextIOBase.write`. Cách này hoạt động thông qua các tham số :func:`open`\'s *encoding* và *errors*, được diễn giải giống như các tham số trong :meth:`str.encode` và :meth:`bytes.decode`.

Do đó, việc đọc Unicode từ một tệp rất đơn giản::

    with open('unicode.txt', encoding='utf-8') as f:
        for line in f:
            print(repr(line))

Bạn cũng có thể mở tệp ở chế độ update, cho phép vừa đọc vừa ghi::

    with open('test', encoding='utf-8', mode='w+') as f:
        f.write('\u4500 blah blah blah\n')
        f.seek(0)
        print(repr(f.readline()[:1]))

Ký tự Unicode ``U+FEFF`` được dùng làm byte-order mark (BOM) và thường được ghi làm ký tự đầu tiên của tệp để hỗ trợ việc tự động phát hiện thứ tự byte của tệp. Một số encoding, chẳng hạn như UTF-16, yêu cầu phải có BOM ở đầu tệp; khi sử dụng encoding như vậy, BOM sẽ tự động được ghi làm ký tự đầu tiên và sẽ được âm thầm loại bỏ khi tệp được đọc. Có các biến thể của những encoding này, chẳng hạn như 'utf-16-le' và 'utf-16-be' cho encoding little-endian và big-endian, chỉ định một thứ tự byte cụ thể và không bỏ qua BOM.

Ở một số nơi, người ta cũng có quy ước đặt một "BOM" ở đầu các tệp được mã hóa UTF-8; tên gọi này dễ gây hiểu lầm vì UTF-8 không phụ thuộc vào thứ tự byte. Dấu này chỉ đơn giản cho biết tệp được mã hóa bằng UTF-8. Khi đọc các tệp như vậy, hãy sử dụng codec 'utf-8-sig' để tự động bỏ qua dấu này nếu có.


Tên tệp Unicode
---------------

Hầu hết các hệ điều hành được sử dụng phổ biến hiện nay đều hỗ trợ tên tệp chứa các ký tự Unicode bất kỳ. Thông thường, điều này được triển khai bằng cách chuyển đổi chuỗi Unicode thành một encoding thay đổi tùy theo hệ thống. Hiện nay Python đang dần thống nhất sử dụng UTF-8: Python trên MacOS đã sử dụng UTF-8 trong một số phiên bản, và Python 3.6 cũng chuyển sang sử dụng UTF-8 trên Windows. Trên các hệ thống Unix, sẽ chỉ có một :term:`filesystem encoding <filesystem encoding and error handler>` nếu bạn đã đặt các biến môi trường ``LANG`` hoặc ``LC_CTYPE``; nếu chưa đặt, encoding mặc định cũng là UTF-8.

Hàm :func:`sys.getfilesystemencoding` trả về encoding cần sử dụng trên hệ thống hiện tại của bạn, trong trường hợp bạn muốn tự thực hiện việc encoding, nhưng thường không có nhiều lý do để làm vậy. Khi mở một tệp để đọc hoặc ghi, thông thường bạn chỉ cần cung cấp chuỗi Unicode làm tên tệp, và chuỗi này sẽ được tự động chuyển đổi sang encoding phù hợp cho bạn::

    filename = 'filename\u4500abc'
    with open(filename, 'w') as f:
        f.write('blah\n')

Các hàm trong module :mod:`os` như :func:`os.stat` cũng chấp nhận tên tệp Unicode.

Hàm :func:`os.listdir` trả về các tên tệp, điều này đặt ra một vấn đề: hàm nên trả về phiên bản Unicode của tên tệp hay trả về các byte chứa phiên bản đã được mã hóa? :func:`os.listdir` có thể thực hiện cả hai, tùy thuộc vào việc bạn cung cấp đường dẫn thư mục dưới dạng byte hay chuỗi Unicode. Nếu truyền một chuỗi Unicode làm đường dẫn, tên tệp sẽ được giải mã bằng encoding của hệ thống tệp và một danh sách các chuỗi Unicode sẽ được trả về, còn nếu truyền một đường dẫn dạng byte, các tên tệp sẽ được trả về dưới dạng byte. Ví dụ, giả sử :term:`filesystem encoding <filesystem encoding and error handler>` mặc định là UTF-8, việc chạy chương trình sau đây::

   fn = 'filename\u4500abc'
   f = open(fn, 'w')
   f.close()

   import os
   print(os.listdir(b'.'))
   print(os.listdir('.'))

sẽ tạo ra kết quả sau:

.. code-block:: shell-session

   $ python listdir-test.py
   [b'filename\xe4\x94\x80abc', ...]
   ['filename\u4500abc', ...]

Danh sách đầu tiên chứa các tên tệp được mã hóa UTF-8, còn danh sách thứ hai chứa các phiên bản Unicode.

Lưu ý rằng trong hầu hết các trường hợp, bạn chỉ cần sử dụng Unicode với các API này. Chỉ nên sử dụng các API byte trên những hệ thống có thể xuất hiện tên tệp không thể giải mã; hiện nay hầu như chỉ có các hệ thống Unix.


Mẹo viết chương trình hỗ trợ Unicode
------------------------------------

Phần này đưa ra một số gợi ý về việc viết phần mềm xử lý Unicode.

Mẹo quan trọng nhất là:

    Phần mềm chỉ nên làm việc với các chuỗi Unicode bên trong, giải mã dữ liệu đầu vào ngay khi có thể và chỉ mã hóa đầu ra ở bước cuối cùng.

Nếu cố viết các hàm xử lý chấp nhận cả chuỗi Unicode và chuỗi byte, bạn sẽ thấy chương trình của mình dễ phát sinh lỗi ở bất cứ đâu khi kết hợp hai loại chuỗi khác nhau này. Không có cơ chế mã hóa hoặc giải mã tự động: nếu bạn thực hiện chẳng hạn ``str + bytes``, một :exc:`TypeError` sẽ được phát sinh.

Khi sử dụng dữ liệu đến từ trình duyệt web hoặc một nguồn không đáng tin cậy nào khác, một kỹ thuật phổ biến là kiểm tra các ký tự bất hợp lệ trong một chuỗi trước khi sử dụng chuỗi đó trong dòng lệnh được tạo hoặc lưu trữ chuỗi trong cơ sở dữ liệu. Nếu làm vậy, hãy cẩn thận kiểm tra chuỗi đã giải mã, không phải dữ liệu byte đã mã hóa; một số encoding có thể có những đặc tính đáng chú ý, chẳng hạn như không song ánh hoặc không hoàn toàn tương thích với ASCII. Điều này đặc biệt đúng nếu dữ liệu đầu vào cũng chỉ định encoding, vì khi đó kẻ tấn công có thể chọn một cách khéo léo để che giấu văn bản độc hại trong bytestream đã mã hóa.


Chuyển đổi giữa các encoding của tệp
''''''''''''''''''''''''''''''''''''

Lớp :class:`~codecs.StreamRecoder` có thể chuyển đổi minh bạch giữa các encoding, nhận một stream trả về dữ liệu theo encoding #1 và hoạt động như một stream trả về dữ liệu theo encoding #2.

Ví dụ, nếu bạn có một tệp đầu vào *f* sử dụng Latin-1, bạn có thể bọc tệp đó bằng một :class:`~codecs.StreamRecoder` để trả về các byte được mã hóa bằng UTF-8::

    new_f = codecs.StreamRecoder(f,
        # en/decoder: được read() sử dụng để mã hóa kết quả của nó và
        # được write() sử dụng để giải mã đầu vào của nó.
        codecs.getencoder('utf-8'), codecs.getdecoder('utf-8'),

        # reader/writer: được sử dụng để đọc và ghi vào stream.
        codecs.getreader('latin-1'), codecs.getwriter('latin-1') )


Các tệp có encoding không xác định
''''''''''''''''''''''''''''''''''

Bạn có thể làm gì nếu cần thay đổi một tệp nhưng không biết encoding của tệp đó? Nếu biết encoding tương thích với ASCII và chỉ muốn xem xét hoặc sửa đổi các phần ASCII, bạn có thể mở tệp bằng error handler ``surrogateescape``::

   with open(fname, 'r', encoding="ascii", errors="surrogateescape") as f:
       data = f.read()

   # thực hiện thay đổi đối với chuỗi 'data'

   with open(fname + '.new', 'w',
             encoding="ascii", errors="surrogateescape") as f:
       f.write(data)

Error handler ``surrogateescape`` sẽ giải mã mọi byte không phải ASCII thành các code point trong một vùng đặc biệt từ U+DC80 đến U+DCFF. Sau đó, các code point này sẽ chuyển ngược lại thành chính những byte ban đầu khi error handler ``surrogateescape`` được sử dụng để mã hóa dữ liệu và ghi dữ liệu trở lại.


Tài liệu tham khảo
------------------

Một phần của `Làm chủ Python 3 Input/Output <https://pyvideo.org/video/289/pycon-2010--mastering-python-3-i-o>`_, một bài nói chuyện tại PyCon 2010 của David Beazley, thảo luận về việc xử lý văn bản và xử lý dữ liệu nhị phân.

`Các slide PDF cho bài thuyết trình "Writing Unicode-aware Applications in Python" của Marc-André Lemburg <https://downloads.egenix.com/python/LSM2005-Developing-Unicode-aware-applications-in-Python.pdf>`_ thảo luận về các vấn đề liên quan đến encoding ký tự, cũng như cách quốc tế hóa và bản địa hóa một ứng dụng. Các slide này chỉ đề cập đến Python 2.x.

`The Guts of Unicode in Python <https://pyvideo.org/video/1768/the-guts-of-unicode-in-python>`_ là một bài nói chuyện tại PyCon 2013 của Benjamin Peterson, thảo luận về cách biểu diễn Unicode nội bộ trong Python 3.3.


Lời cảm ơn
==========

Bản nháp đầu tiên của tài liệu này do Andrew Kuchling viết. Sau đó, tài liệu tiếp tục được Alexander Belopolsky, Georg Brandl, Andrew Kuchling và Ezio Melotti chỉnh sửa.

Xin cảm ơn những người sau đây đã phát hiện lỗi hoặc đưa ra đề xuất cho bài viết này: Éric Araujo, Nicholas Bastin, Nick Coghlan, Marius Gedminas, Kent Johnson, Ken Krugler, Marc-André Lemburg, Martin von Löwis, Terry J. Reedy, Serhiy Storchaka, Eryk Sun, Chad Whitacre, Graham Wideman.

.. _`actual number assigned`: https://www.unicode.org/versions/latest/#Summary
.. _`Unicode Consortium site`: https://www.unicode.org
.. _`A chronology`: https://www.unicode.org/history/
.. _`discusses the history of Unicode and UTF-8`: https://www.youtube.com/watch?v=MijmeoH9LT4
.. _`an introductory guide`: https://jkorpela.fi/unicode/guide.html
.. _`good introductory article`: https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/
.. _`character encoding`: https://en.wikipedia.org/wiki/Character_encoding
.. _`UTF-8`: https://en.wikipedia.org/wiki/UTF-8
.. _`the General Category Values section of the Unicode Character Database documentation`: https://www.unicode.org/reports/tr44/#General_Category_Values
.. _`Processing Text Files in Python 3`: https://python-notes.curiousefficiency.org/en/latest/python3/text_file_processing.html
.. _`Pragmatic Unicode`: https://nedbatchelder.com/text/unipain.html
.. _`a presentation titled "Python and Unicode" (PDF slides)`: https://downloads.egenix.com/python/Unicode-EPC2002-Talk.pdf
.. _`Mastering Python 3 Input/Output`: https://pyvideo.org/video/289/pycon-2010--mastering-python-3-i-o
.. _`PDF slides for Marc-André Lemburg's presentation "Writing Unicode-aware Applications in Python"`: https://downloads.egenix.com/python/LSM2005-Developing-Unicode-aware-applications-in-Python.pdf
.. _`The Guts of Unicode in Python`: https://pyvideo.org/video/1768/the-guts-of-unicode-in-python
