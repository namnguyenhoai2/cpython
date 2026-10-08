:mod:`!tokenize` --- Tokenizer cho mã nguồn Python
==================================================

.. module:: tokenize
   :synopsis: Bộ quét từ vựng cho mã nguồn Python.

.. moduleauthor:: Ka Ping Yee
.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>

**Mã nguồn:** :source:`Lib/tokenize.py`

--------------

Mô-đun :mod:`!tokenize` cung cấp một bộ quét từ vựng cho mã nguồn Python, được triển khai bằng Python. Bộ quét trong mô-đun này cũng trả về các chú thích dưới dạng token, nhờ đó hữu ích khi triển khai các "pretty-printer", bao gồm cả các bộ tô màu cho nội dung hiển thị trên màn hình.

Để đơn giản hóa việc xử lý luồng token, tất cả :ref:`operator <operators>` và
các token :ref:`delimiter <delimiters>` và :data:`Ellipsis` được trả về bằng kiểu token chung :data:`~token.OP`. Có thể xác định kiểu chính xác bằng cách kiểm tra thuộc tính ``exact_type`` trên
:term:`named tuple` được trả về từ :func:`tokenize.tokenize`.


.. warning::

   Lưu ý rằng các hàm trong mô-đun này chỉ được thiết kế để phân tích cú pháp mã Python hợp lệ về mặt cú pháp (mã không gây ra lỗi khi được phân tích bằng :func:`ast.parse`). Hành vi của các hàm trong mô-đun này là **không xác định** khi cung cấp mã Python không hợp lệ và có thể thay đổi bất kỳ lúc nào.

Tokenizing Input
----------------

Điểm truy cập chính là một :term:`generator`:

.. function:: tokenize(readline)

   Generator :func:`.tokenize` yêu cầu một đối số là *readline*, đối số này phải là một đối tượng có thể gọi, cung cấp cùng giao diện như
   phương thức :meth:`io.IOBase.readline` của các đối tượng tệp. Mỗi lần gọi hàm phải trả về một dòng đầu vào dưới dạng bytes.

   Generator tạo ra các bộ 5 phần tử với những thành phần sau: kiểu token; chuỗi token; một bộ 2 phần tử ``(srow, scol)`` gồm các số nguyên chỉ định hàng và cột nơi token bắt đầu trong mã nguồn; một bộ 2 phần tử ``(erow, ecol)`` gồm các số nguyên chỉ định hàng và cột nơi token kết thúc trong mã nguồn; và dòng nơi tìm thấy token. Dòng được truyền vào (phần tử cuối cùng của bộ) là dòng *thực tế*. Bộ 5 phần tử được trả về dưới dạng một :term:`named tuple` với các tên trường: ``type string start end line``.

   :term:`named tuple` được trả về có thêm một thuộc tính tên là ``exact_type``, chứa kiểu toán tử chính xác cho
   :data:`~token.OP` token. Đối với tất cả các loại token khác, ``exact_type`` tương ứng với trường ``type`` của named tuple.

   .. versionchanged:: 3.1
      Đã thêm hỗ trợ cho named tuple.

   .. versionchanged:: 3.3
      Đã thêm hỗ trợ cho ``exact_type``.

   :func:`.tokenize` xác định encoding nguồn của tệp bằng cách tìm BOM UTF-8 hoặc encoding cookie, theo :pep:`263`.

.. function:: generate_tokens(readline)

   Tokenize mã nguồn bằng cách đọc các chuỗi unicode thay vì bytes.

   Giống như :func:`.tokenize`, đối số *readline* là một callable trả về một dòng đầu vào. Tuy nhiên, :func:`generate_tokens` yêu cầu *readline* trả về một đối tượng str thay vì bytes.

   Kết quả là một iterator trả về các named tuple, chính xác như
   :func:`.tokenize`. Nó không tạo ra token :data:`~token.ENCODING`.

Tất cả hằng số từ mô-đun :mod:`token` cũng được xuất từ
:mod:`!tokenize`.

Một hàm khác được cung cấp để đảo ngược quá trình tokenization. Điều này hữu ích khi tạo các công cụ tokenization cho một script, sửa đổi token stream rồi ghi lại script đã sửa đổi.


.. function:: untokenize(iterable)

    Chuyển các token trở lại mã nguồn Python. *iterable* phải trả về các sequence có ít nhất hai phần tử: kiểu token và chuỗi token. Mọi phần tử bổ sung trong sequence đều bị bỏ qua.

    Kết quả được đảm bảo sẽ được tokenization lại để khớp với đầu vào, nhờ đó quá trình chuyển đổi không làm mất dữ liệu và việc chuyển đổi hai chiều được đảm bảo. Sự đảm bảo này chỉ áp dụng cho kiểu token và chuỗi token, vì khoảng cách giữa các token (vị trí cột) có thể thay đổi.

    Nó trả về bytes, được mã hóa bằng token :data:`~token.ENCODING`, là sequence token đầu tiên do :func:`.tokenize` xuất ra. Nếu đầu vào không có token mã hóa, nó sẽ trả về một str.


:func:`.tokenize` cần phát hiện encoding của các tệp mã nguồn mà nó tokenization. Hàm được sử dụng để thực hiện việc này hiện có sẵn:

.. function:: detect_encoding(readline)

    Hàm :func:`detect_encoding` được dùng để phát hiện encoding cần sử dụng nhằm giải mã tệp mã nguồn Python. Hàm này yêu cầu một đối số, readline, giống như generator :func:`.tokenize`.

    Hàm sẽ gọi readline tối đa hai lần và trả về encoding được sử dụng (dưới dạng chuỗi) cùng danh sách các dòng (chưa được giải mã từ byte) mà hàm đã đọc.

    Hàm phát hiện encoding dựa trên sự hiện diện của BOM UTF-8 hoặc encoding cookie được chỉ định trong :pep:`263`. Nếu cả BOM và cookie đều xuất hiện nhưng không khớp nhau, :exc:`SyntaxError` sẽ được raise. Lưu ý rằng nếu tìm thấy BOM, ``'utf-8-sig'`` sẽ được trả về dưới dạng encoding.

    Nếu không chỉ định encoding, giá trị mặc định ``'utf-8'`` sẽ được trả về.

    Sử dụng :func:`.open` để mở các tệp mã nguồn Python: hàm này sử dụng
    :func:`detect_encoding` để phát hiện encoding của tệp.


.. function:: open(filename)

   Mở tệp ở chế độ chỉ đọc bằng encoding được phát hiện bởi
   :func:`detect_encoding`.

   .. versionadded:: 3.2

.. exception:: TokenError

   Được phát sinh khi một docstring hoặc biểu thức có thể được tách trên nhiều dòng không được hoàn tất ở bất kỳ đâu trong tệp, ví dụ như::

      """Beginning of
      docstring

   hoặc::

      [1,
       2,
       3

.. _tokenize-cli:

Cách sử dụng dòng lệnh
----------------------

.. versionadded:: 3.3

Mô-đun :mod:`!tokenize` có thể được thực thi dưới dạng một script từ dòng lệnh. Cách thực hiện rất đơn giản:

.. code-block:: sh

   python -m tokenize [-e] [filename.py]

Các tùy chọn sau được chấp nhận:

.. program:: tokenize

.. option:: -h, --help

   hiển thị thông báo trợ giúp này rồi thoát

.. option:: -e, --exact

   hiển thị tên token bằng kiểu chính xác

Nếu :file:`filename.py` được chỉ định, nội dung của nó sẽ được tokenize ra stdout. Nếu không, việc tokenize sẽ được thực hiện trên stdin.

Ví dụ
-----

Ví dụ về script rewriter chuyển đổi các literal float thành các đối tượng Decimal::

    from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP
    from io import BytesIO

    def decistmt(s):
        """Substitute Decimals for floats in a string of statements.

        >>> from decimal import Decimal
        >>> s = 'print(+21.3e-5*-.1234/81.7)'
        >>> decistmt(s)
        "print (+Decimal ('21.3e-5')*-Decimal ('.1234')/Decimal ('81.7'))"

        The format of the exponent is inherited from the platform C library.
        Known cases are "e-007" (Windows) and "e-07" (not Windows).  Since
        we're only showing 12 digits, and the 13th isn't close to 5, the
        rest of the output should be platform-independent.

        >>> exec(s)  #doctest: +ELLIPSIS
        -3.21716034272e-0...7

        Output from calculations with Decimal should be identical across all
        platforms.

        >>> exec(decistmt(s))
        -3.217160342717258261933904529E-7
        """
        result = []
        g = tokenize(BytesIO(s.encode('utf-8')).readline)  # tokenize chuỗi
        for toknum, tokval, _, _, _ in g:
            if toknum == NUMBER and '.' in tokval:  # thay thế các token NUMBER
                result.extend([
                    (NAME, 'Decimal'),
                    (OP, '('),
                    (STRING, repr(tokval)),
                    (OP, ')')
                ])
            else:
                result.append((toknum, tokval))
        return untokenize(result).decode('utf-8')

Ví dụ về việc tokenize từ command line. Script::

    def say_hello():
        print("Hello, World!")

    say_hello()

sẽ được token hóa thành đầu ra sau đây, trong đó cột đầu tiên là phạm vi tọa độ dòng/cột nơi token được tìm thấy, cột thứ hai là tên của token và cột cuối cùng là giá trị của token (nếu có)

.. code-block:: shell-session

    $ python -m tokenize hello.py
    0,0-0,0:            ENCODING       'utf-8'
    1,0-1,3:            NAME           'def'
    1,4-1,13:           NAME           'say_hello'
    1,13-1,14:          OP             '('
    1,14-1,15:          OP             ')'
    1,15-1,16:          OP             ':'
    1,16-1,17:          NEWLINE        '\n'
    2,0-2,4:            INDENT         '    '
    2,4-2,9:            NAME           'print'
    2,9-2,10:           OP             '('
    2,10-2,25:          STRING         '"Hello, World!"'
    2,25-2,26:          OP             ')'
    2,26-2,27:          NEWLINE        '\n'
    3,0-3,1:            NL             '\n'
    4,0-4,0:            DEDENT         ''
    4,0-4,9:            NAME           'say_hello'
    4,9-4,10:           OP             '('
    4,10-4,11:          OP             ')'
    4,11-4,12:          NEWLINE        '\n'
    5,0-5,0:            ENDMARKER      ''

Có thể hiển thị tên chính xác của loại token bằng tùy chọn :option:`-e`:

.. code-block:: shell-session

    $ python -m tokenize -e hello.py
    0,0-0,0:            ENCODING       'utf-8'
    1,0-1,3:            NAME           'def'
    1,4-1,13:           NAME           'say_hello'
    1,13-1,14:          LPAR           '('
    1,14-1,15:          RPAR           ')'
    1,15-1,16:          COLON          ':'
    1,16-1,17:          NEWLINE        '\n'
    2,0-2,4:            INDENT         '    '
    2,4-2,9:            NAME           'print'
    2,9-2,10:           LPAR           '('
    2,10-2,25:          STRING         '"Hello, World!"'
    2,25-2,26:          RPAR           ')'
    2,26-2,27:          NEWLINE        '\n'
    3,0-3,1:            NL             '\n'
    4,0-4,0:            DEDENT         ''
    4,0-4,9:            NAME           'say_hello'
    4,9-4,10:           LPAR           '('
    4,10-4,11:          RPAR           ')'
    4,11-4,12:          NEWLINE        '\n'
    5,0-5,0:            ENDMARKER      ''

Ví dụ về cách token hóa một tệp theo phương thức lập trình, đọc các chuỗi unicode thay vì các byte bằng :func:`generate_tokens`::

    import tokenize

    with tokenize.open('hello.py') as f:
        tokens = tokenize.generate_tokens(f.readline)
        for token in tokens:
            print(token)

Hoặc đọc trực tiếp các byte bằng :func:`.tokenize`::

    import tokenize

    with open('hello.py', 'rb') as f:
        tokens = tokenize.tokenize(f.readline)
        for token in tokens:
            print(token)
