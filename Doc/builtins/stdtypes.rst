.. XXX: reference/datamodel and this have quite a few overlaps!


.. _bltin-types:

*****************
Các kiểu dựng sẵn
*****************

Các phần sau mô tả những kiểu chuẩn được tích hợp sẵn trong trình thông dịch.

.. index:: pair: built-in; types

Các kiểu dựng sẵn chính gồm kiểu số, kiểu chuỗi, kiểu ánh xạ, lớp, thể hiện và ngoại lệ.

Một số lớp tập hợp có thể thay đổi. Các phương thức thêm, bớt hoặc sắp xếp lại các phần tử của chúng tại chỗ và không trả về một phần tử cụ thể sẽ không bao giờ trả về chính thể hiện tập hợp mà ``None``.

Một số phép toán được hỗ trợ bởi nhiều kiểu đối tượng; cụ thể là hầu hết mọi đối tượng đều có thể được so sánh về tính bằng nhau, kiểm tra giá trị đúng và chuyển đổi thành chuỗi (bằng hàm :func:`repr` hoặc hàm :func:`str` có khác biệt đôi chút). Hàm sau được sử dụng ngầm khi một đối tượng được ghi bằng hàm :func:`print`.


.. _truth:

Kiểm tra giá trị đúng
=====================

.. index::
   pair: statement; if
   pair: statement; while
   pair: truth; value
   pair: Boolean; operations
   single: false

Bất kỳ đối tượng nào cũng có thể được kiểm tra giá trị đúng để sử dụng trong :keyword:`if` hoặc
:keyword:`while` điều kiện hoặc làm toán hạng của các phép toán Boolean bên dưới.

.. index:: single: true

Theo mặc định, một đối tượng được coi là đúng trừ khi lớp của nó định nghĩa một
:meth:`~object.__bool__` phương thức trả về ``False`` hoặc một
:meth:`~object.__len__` phương thức trả về số không khi được gọi với đối tượng. [1]_ Nếu một trong các phương thức này phát sinh ngoại lệ khi được gọi, ngoại lệ sẽ được truyền tiếp và đối tượng không có giá trị chân lý (ví dụ: :data:`NotImplemented`). Sau đây là hầu hết các đối tượng tích hợp được coi là sai:

.. index::
   single: None (Built-in object)
   single: False (Built-in object)

* các hằng số được định nghĩa là sai: ``None`` và ``False``

* số không thuộc bất kỳ kiểu số nào: ``0``, ``0.0``, ``0j``, ``Decimal(0)``, ``Fraction(0, 1)``

* các dãy và collection rỗng: ``''``, ``()``, ``[]``, ``{}``, ``set()``, ``range(0)``

.. index::
   pair: operator; or
   pair: operator; and
   single: False
   single: True

Các phép toán và hàm tích hợp có kết quả Boolean luôn trả về ``0`` hoặc ``False`` khi sai và ``1`` hoặc ``True`` khi đúng, trừ khi có nêu khác. (Ngoại lệ quan trọng: các phép toán Boolean ``or`` và ``and`` luôn trả về một trong các toán hạng của chúng.)


.. _boolean:

Phép toán Boolean --- :keyword:`!and`, :keyword:`!or`, :keyword:`!not`
======================================================================

.. index:: pair: Boolean; operations

Đây là các phép toán Boolean, được sắp xếp theo thứ tự ưu tiên tăng dần:

+-------------+--------------------------------------------------------+---------+
| Phép toán   | Kết quả                                                | Ghi chú |
+=============+========================================================+=========+
| ``x or y``  | nếu *x* là đúng, thì *x*, nếu không thì *y*            | \(1)    |
+-------------+--------------------------------------------------------+---------+
| ``x and y`` | nếu *x* là false thì *x*, nếu không thì *y*            | \(2)    |
+-------------+--------------------------------------------------------+---------+
| ``not x``   | nếu *x* là false thì ``True``, nếu không thì ``False`` | \(3)    |
+-------------+--------------------------------------------------------+---------+

.. index::
   pair: operator; and
   pair: operator; or
   pair: operator; not

Lưu ý:

(1)
   Đây là toán tử short-circuit, vì vậy nó chỉ đánh giá đối số thứ hai nếu đối số thứ nhất là false.

(2)
   Đây là toán tử short-circuit, vì vậy nó chỉ đánh giá đối số thứ hai nếu đối số thứ nhất là true.

(3)
   ``not`` có độ ưu tiên thấp hơn các toán tử không phải Boolean, vì vậy ``not a == b`` được diễn giải là ``not (a == b)``, còn ``a == not b`` là lỗi cú pháp.


.. _stdcomparisons:

So sánh
=======

.. index::
   pair: chaining; comparisons
   pair: operator; comparison
   pair: operator; ==
   pair: operator; < (less)
   pair: operator; <=
   pair: operator; > (greater)
   pair: operator; >=
   pair: operator; !=
   pair: operator; is
   pair: operator; is not

Có tám phép toán so sánh trong Python. Tất cả đều có cùng độ ưu tiên (cao hơn độ ưu tiên của các phép toán Boolean). Các phép so sánh có thể được nối tùy ý; ví dụ, ``x < y <= z`` tương đương với ``x < y and y <= z``, ngoại trừ việc *y* chỉ được đánh giá một lần (nhưng trong cả hai trường hợp, *z* hoàn toàn không được đánh giá khi ``x < y`` được xác định là sai).

Bảng này tóm tắt các phép toán so sánh:

+------------+------------------------------+
| Phép toán  | Ý nghĩa                      |
+============+==============================+
| ``<``      | nhỏ hơn nghiêm ngặt          |
+------------+------------------------------+
| ``<=``     | nhỏ hơn hoặc bằng            |
+------------+------------------------------+
| ``>``      | lớn hơn nghiêm ngặt          |
+------------+------------------------------+
| ``>=``     | lớn hơn hoặc bằng            |
+------------+------------------------------+
| ``==``     | bằng                         |
+------------+------------------------------+
| ``!=``     | khác                         |
+------------+------------------------------+
| ``is``     | định danh đối tượng          |
+------------+------------------------------+
| ``is not`` | phủ định định danh đối tượng |
+------------+------------------------------+

.. index::
   pair: object; numeric
   pair: objects; comparing

Trừ khi có quy định khác, các đối tượng thuộc những kiểu khác nhau không bao giờ được so sánh là bằng nhau. Toán tử ``==`` luôn được định nghĩa, nhưng đối với một số kiểu đối tượng (ví dụ: các đối tượng lớp), nó tương đương với :keyword:`is`. Các toán tử ``<``, ``<=``, ``>`` và ``>=`` chỉ được định nghĩa khi chúng có ý nghĩa; ví dụ: chúng phát sinh một
ngoại lệ :exc:`TypeError` khi một trong các đối số là số phức.

.. index::
   single: __eq__() (instance method)
   single: __ne__() (instance method)
   single: __lt__() (instance method)
   single: __le__() (instance method)
   single: __gt__() (instance method)
   single: __ge__() (instance method)

Các thể hiện không đồng nhất của một lớp thường được so sánh là không bằng nhau, trừ khi lớp định nghĩa phương thức :meth:`~object.__eq__`.

Các thể hiện của một lớp không thể được sắp thứ tự so với các thể hiện khác của cùng lớp hoặc các kiểu đối tượng khác, trừ khi lớp định nghĩa đủ các phương thức :meth:`~object.__lt__`, :meth:`~object.__le__`, :meth:`~object.__gt__`, và
:meth:`~object.__ge__` (nói chung, :meth:`~object.__lt__` và
:meth:`~object.__eq__` là đủ nếu bạn muốn các toán tử so sánh mang ý nghĩa thông thường).

Hành vi của các toán tử :keyword:`is` và :keyword:`is not` không thể được tùy chỉnh; ngoài ra, chúng có thể được áp dụng cho bất kỳ hai đối tượng nào và không bao giờ phát sinh ngoại lệ.

.. index::
   pair: operator; in
   pair: operator; not in

Hai phép toán khác có cùng mức ưu tiên cú pháp, :keyword:`in` và
:keyword:`not in`, được các kiểu :term:`iterable` hoặc triển khai phương thức :meth:`~object.__contains__` hỗ trợ.

.. _typesnumeric:

Các kiểu số --- :class:`int`, :class:`float`, :class:`complex`
==============================================================

.. index::
   pair: object; numeric
   pair: object; Boolean
   pair: object; integer
   pair: object; floating-point
   pair: object; complex number
   pair: C; language

Có ba kiểu số riêng biệt: :dfn:`số nguyên`, :dfn:`số dấu phẩy động`, và :dfn:`số phức`. Ngoài ra, Boolean là một kiểu con của số nguyên. Số nguyên có độ chính xác không giới hạn. Số dấu phẩy động thường được triển khai bằng :c:expr:`double` trong C; thông tin về độ chính xác và biểu diễn nội bộ của số dấu phẩy động trên máy đang chạy chương trình của bạn có trong :data:`sys.float_info`. Số phức có phần thực và phần ảo, mỗi phần đều là một số dấu phẩy động. Để trích xuất các phần này từ số phức *z*, hãy sử dụng ``z.real`` và ``z.imag``. (Thư viện chuẩn bao gồm các kiểu số bổ sung :mod:`fractions.Fraction` cho số hữu tỉ và :mod:`decimal.Decimal` cho số dấu phẩy động có độ chính xác do người dùng định nghĩa.)

.. index::
   pair: numeric; literals
   pair: integer; literals
   pair: floating-point; literals
   pair: complex number; literals
   pair: hexadecimal; literals
   pair: octal; literals
   pair: binary; literals

Số được tạo bởi các literal số hoặc là kết quả của các hàm và toán tử tích hợp sẵn. Các literal số nguyên không có hậu tố (bao gồm số thập lục phân, bát phân và nhị phân) tạo ra số nguyên. Các literal số chứa dấu thập phân hoặc dấu mũ tạo ra số dấu phẩy động. Việc thêm ``'j'`` hoặc ``'J'`` vào một literal số sẽ tạo ra một số ảo (một số phức có phần thực bằng 0), mà bạn có thể cộng với một số nguyên hoặc số dấu phẩy động để nhận được một số phức có phần thực và phần ảo.

Các hàm khởi tạo :func:`int`, :func:`float`, và
:func:`complex` có thể được sử dụng để tạo ra các số thuộc một kiểu cụ thể.

.. index::
   single: arithmetic
   pair: built-in function; int
   pair: built-in function; float
   pair: built-in function; complex
   single: operator; + (plus)
   single: + (plus); unary operator
   single: + (plus); binary operator
   single: operator; - (minus)
   single: - (minus); unary operator
   single: - (minus); binary operator
   pair: operator; * (asterisk)
   pair: operator; / (slash)
   pair: operator; //
   pair: operator; % (percent)
   pair: operator; **

.. _stdtypes-mixed-arithmetic:

Python hỗ trợ đầy đủ phép tính hỗn hợp: khi một toán tử số học nhị phân có các toán hạng thuộc những kiểu số tích hợp sẵn khác nhau, toán hạng có kiểu "hẹp hơn" sẽ được mở rộng thành kiểu của toán hạng còn lại:

* Nếu cả hai đối số đều là số phức thì không thực hiện chuyển đổi;
* nếu một trong hai đối số là số phức hoặc số dấu phẩy động, đối số còn lại được chuyển đổi thành số dấu phẩy động;
* nếu không, cả hai phải là số nguyên và không cần chuyển đổi.

Phép toán số học với các toán hạng phức và thực được xác định theo công thức toán học thông thường, ví dụ::

    x + complex(u, v) = complex(x + u, v)
    x * complex(u, v) = complex(x * u, x * v)

So sánh giữa các số thuộc các kiểu khác nhau được thực hiện như thể đang so sánh các giá trị chính xác của những số đó. [2]_

Tất cả các kiểu số (ngoại trừ số phức) đều hỗ trợ các phép toán sau (về độ ưu tiên của các phép toán, xem :ref:`operator-summary`):

+---------------------+------------------------------------------------------------------------------+----------+-----------------+
| Phép toán           | Kết quả                                                                      | Ghi chú  | Tài liệu đầy đủ |
+=====================+==============================================================================+==========+=================+
| ``x + y``           | tổng của *x* và *y*                                                          |          |                 |
+---------------------+------------------------------------------------------------------------------+----------+-----------------+
| ``x - y``           | hiệu của *x* và *y*                                                          |          |                 |
+---------------------+------------------------------------------------------------------------------+----------+-----------------+
| ``x * y``           | tích của *x* và *y*                                                          |          |                 |
+---------------------+------------------------------------------------------------------------------+----------+-----------------+
| ``x / y``           | thương của *x* và *y*                                                        |          |                 |
+---------------------+------------------------------------------------------------------------------+----------+-----------------+
| ``x // y``          | thương nguyên của *x* và *y*                                                 | \(1)\(2) |                 |
+---------------------+------------------------------------------------------------------------------+----------+-----------------+
| ``x % y``           | phần dư của ``x / y``                                                        | \(2)     |                 |
+---------------------+------------------------------------------------------------------------------+----------+-----------------+
| ``-x``              | *x* được đổi dấu                                                             |          |                 |
+---------------------+------------------------------------------------------------------------------+----------+-----------------+
| ``+x``              | *x* không đổi                                                                |          |                 |
+---------------------+------------------------------------------------------------------------------+----------+-----------------+
| ``abs(x)``          | giá trị tuyệt đối hoặc độ lớn của *x*                                        |          | :func:`abs`     |
+---------------------+------------------------------------------------------------------------------+----------+-----------------+
| ``int(x)``          | *x* được chuyển đổi thành số nguyên                                          | \(3)\(6) | :func:`int`     |
+---------------------+------------------------------------------------------------------------------+----------+-----------------+
| ``float(x)``        | *x* được chuyển đổi thành số dấu phẩy động                                   | \(4)\(6) | :func:`float`   |
+---------------------+------------------------------------------------------------------------------+----------+-----------------+
| ``complex(re, im)`` | một số phức có phần thực là *re*, phần ảo là *im*. *im* mặc định bằng không. | \(6)     | :func:`complex` |
+---------------------+------------------------------------------------------------------------------+----------+-----------------+
| ``c.conjugate()``   | liên hợp của số phức *c*                                                     |          |                 |
+---------------------+------------------------------------------------------------------------------+----------+-----------------+
| ``divmod(x, y)``    | cặp ``(x // y, x % y)``                                                      | \(2)     | :func:`divmod`  |
+---------------------+------------------------------------------------------------------------------+----------+-----------------+
| ``pow(x, y)``       | *x* lũy thừa *y*                                                             | \(5)     | :func:`pow`     |
+---------------------+------------------------------------------------------------------------------+----------+-----------------+
| ``x ** y``          | *x* lũy thừa *y*                                                             | \(5)     |                 |
+---------------------+------------------------------------------------------------------------------+----------+-----------------+

.. index::
   triple: operations on; numeric; types
   single: conjugate() (complex number method)

Ghi chú:

(1)
   Còn được gọi là phép chia nguyên. Với các toán hạng có kiểu :class:`int`, kết quả có kiểu :class:`int`. Với các toán hạng có kiểu :class:`float`, kết quả có kiểu :class:`float`. Nhìn chung, kết quả là một số nguyên, mặc dù kiểu của kết quả không nhất thiết là :class:`int`. Kết quả luôn được làm tròn về phía âm vô cực: ``1//2`` là ``0``, ``(-1)//2`` là ``-1``, ``1//(-2)`` là ``-1``, và ``(-1)//(-2)`` là ``0``.

(2)
   Không áp dụng cho số phức. Thay vào đó, hãy chuyển đổi sang số thực bằng :func:`abs` nếu phù hợp.

(3)
   .. index::
      pair: module; math
      single: floor() (in module math)
      single: ceil() (in module math)
      single: trunc() (in module math)
      pair: numeric; conversions

   Việc chuyển đổi từ :class:`float` sang :class:`int` sẽ cắt bỏ phần thập phân. Hãy xem các hàm :func:`math.floor` và :func:`math.ceil` để biết các cách chuyển đổi khác.

(4)
   float cũng chấp nhận các chuỗi "nan" và "inf", cùng với tiền tố tùy chọn "+" hoặc "-", tương ứng với Not a Number (NaN) và vô cực dương hoặc âm.

(5)
   Python định nghĩa ``pow(0, 0)`` và ``0 ** 0`` là ``1``, như thường thấy trong các ngôn ngữ lập trình.

(6)
   Các literal số được chấp nhận bao gồm các chữ số từ ``0`` đến ``9`` hoặc bất kỳ ký tự tương đương nào trong Unicode (các code point có thuộc tính ``Nd``).

   Xem `the Unicode Standard <https://unicode.org/Public/UNIDATA/extracted/DerivedNumericType.txt>`_ để biết danh sách đầy đủ các code point có thuộc tính ``Nd``.


Tất cả các kiểu :class:`numbers.Real` (:class:`int` và :class:`float`) cũng bao gồm các phép toán sau:

+--------------------+---------------------------------------------+
| Operation          | Result                                      |
+====================+=============================================+
| :func:`math.trunc(\| *x* truncated to :class:`~numbers.Integral` |
| x) <math.trunc>`   |                                             |
+--------------------+---------------------------------------------+
| :func:`round(x[,   | *x* rounded to *n* digits,                  |
| n]) <round>`       | rounding half to even. If *n* is            |
|                    | omitted, it defaults to 0.                  |
+--------------------+---------------------------------------------+
| :func:`math.floor(\| the greatest :class:`~numbers.Integral`     |
| x) <math.floor>`   | <= *x*                                      |
+--------------------+---------------------------------------------+
| :func:`math.ceil(x)| the least :class:`~numbers.Integral` >= *x* |
| <math.ceil>`       |                                             |
+--------------------+---------------------------------------------+

Để biết thêm các phép toán số, hãy xem các module :mod:`math` và :mod:`cmath`.

.. XXXJH exceptions: overflow (when? what operations?) zerodivision


.. _bitstring-ops:

Các phép toán bit trên kiểu số nguyên
-------------------------------------

.. index::
   triple: operations on; integer; types
   pair: bitwise; operations
   pair: shifting; operations
   pair: masking; operations
   pair: operator; | (vertical bar)
   pair: operator; ^ (caret)
   pair: operator; & (ampersand)
   pair: operator; <<
   pair: operator; >>
   pair: operator; ~ (tilde)

Các phép toán bit chỉ có ý nghĩa đối với số nguyên. Kết quả của các phép toán bit được tính như thể chúng được thực hiện trong biểu diễn bù hai với vô hạn bit dấu.

Độ ưu tiên của tất cả các phép toán bit nhị phân đều thấp hơn các phép toán số học và cao hơn các phép so sánh; phép toán một ngôi ``~`` có cùng độ ưu tiên với các phép toán số học một ngôi khác (``+`` và ``-``).

Bảng này liệt kê các phép toán bit theo thứ tự độ ưu tiên tăng dần:

+------------+--------------------------------------------------+---------+
| Phép toán  | Kết quả                                          | Ghi chú |
+============+==================================================+=========+
| ``x | y``  | phép :dfn:`or` theo bit của *x* và *y*           | \(4)    |
+------------+--------------------------------------------------+---------+
| ``x ^ y``  | phép :dfn:`exclusive or` theo bit của *x* và *y* | \(4)    |
+------------+--------------------------------------------------+---------+
| ``x & y``  | phép :dfn:`and` theo bit của *x* và *y*          | \(4)    |
+------------+--------------------------------------------------+---------+
| ``x << n`` | *x* dịch trái *n* bit                            | (1)(2)  |
+------------+--------------------------------------------------+---------+
| ``x >> n`` | *x* dịch phải *n* bit                            | (1)(3)  |
+------------+--------------------------------------------------+---------+
| ``~x``     | các bit của *x* được đảo ngược                   |         |
+------------+--------------------------------------------------+---------+

Ghi chú:

(1)
   Số lượng dịch âm là không hợp lệ và khiến :exc:`ValueError` được phát sinh.

(2)
   Dịch trái *n* bit tương đương với phép nhân với ``pow(2, n)``.

(3)
   Dịch phải *n* bit tương đương với phép chia lấy phần nguyên cho ``pow(2, n)``.

(4)
   Thực hiện các phép tính này với ít nhất một bit mở rộng dấu bổ sung trong biểu diễn bù hai hữu hạn (độ rộng bit sử dụng là ``1 + max(x.bit_length(), y.bit_length())`` trở lên) là đủ để nhận được kết quả giống như khi có vô hạn bit dấu.


Các phương thức bổ sung trên kiểu số nguyên
-------------------------------------------

Kiểu int triển khai :class:`numbers.Integral` :term:`abstract base class`. Ngoài ra, kiểu này cung cấp thêm một số phương thức:

.. method:: int.bit_length()

    Trả về số bit cần thiết để biểu diễn một số nguyên ở dạng nhị phân, không bao gồm dấu và các số 0 ở đầu::

        >>> n = -37
        >>> bin(n)
        '-0b100101'
        >>> n.bit_length()
        6

    Chính xác hơn, nếu ``x`` khác không, thì ``x.bit_length()`` là số nguyên dương duy nhất ``k`` sao cho ``2**(k-1) <= abs(x) < 2**k``. Tương đương, khi ``abs(x)`` đủ nhỏ để có logarithm được làm tròn chính xác, thì ``k = 1 + int(log(abs(x), 2))``. Nếu ``x`` bằng không, thì ``x.bit_length()`` trả về ``0``.

    Tương đương với::

        def bit_length(self):
            s = bin(self)       # biểu diễn nhị phân:  bin(-37) --> '-0b100101'
            s = s.lstrip('-0b') # xóa các số 0 ở đầu và dấu trừ
            return len(s)       # len('100101') --> 6

    .. versionadded:: 3.1

.. method:: int.bit_count()

    Trả về số lượng số 1 trong biểu diễn nhị phân của giá trị tuyệt đối của số nguyên. Giá trị này còn được gọi là population count. Ví dụ::

        >>> n = 19
        >>> bin(n)
        '0b10011'
        >>> n.bit_count()
        3
        >>> (-n).bit_count()
        3

    Tương đương với::

        def bit_count(self):
            return bin(self).count("1")

    .. versionadded:: 3.10

.. method:: int.to_bytes(length=1, byteorder='big', *, signed=False)

    Trả về một mảng byte biểu diễn một số nguyên.

        >>> (1024).to_bytes(2, byteorder='big')
        b'\x04\x00'
        >>> (1024).to_bytes(10, byteorder='big')
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00'
        >>> (-1024).to_bytes(10, byteorder='big', signed=True)
        b'\xff\xff\xff\xff\xff\xff\xff\xff\xfc\x00'
        >>> x = 1000
        >>> x.to_bytes((x.bit_length() + 7) // 8, byteorder='little')
        b'\xe8\x03'

    Số nguyên được biểu diễn bằng *length* byte và mặc định là 1. Một
    :exc:`OverflowError` sẽ được phát sinh nếu số nguyên không thể biểu diễn bằng số byte đã cho.

    Đối số *byteorder* xác định thứ tự byte được dùng để biểu diễn số nguyên và mặc định là ``"big"``. Nếu *byteorder* là ``"big"``, byte có trọng số lớn nhất nằm ở đầu mảng byte. Nếu *byteorder* là ``"little"``, byte có trọng số lớn nhất nằm ở cuối mảng byte.

    Đối số *signed* xác định liệu có sử dụng biểu diễn bù hai để biểu diễn số nguyên hay không. Nếu *signed* là ``False`` và một số nguyên âm được cung cấp, một :exc:`OverflowError` sẽ được phát sinh. Giá trị mặc định của *signed* là ``False``.

    Các giá trị mặc định có thể được sử dụng để thuận tiện chuyển một số nguyên thành một đối tượng byte đơn::

        >>> (65).to_bytes()
        b'A'

    Tuy nhiên, khi sử dụng các đối số mặc định, đừng cố chuyển đổi một giá trị lớn hơn 255, nếu không bạn sẽ nhận được :exc:`OverflowError`.

    Tương đương với::

        def to_bytes(n, length=1, byteorder='big', signed=False):
            if byteorder == 'little':
                order = range(length)
            elif byteorder == 'big':
                order = reversed(range(length))
            else:
                raise ValueError("byteorder must be either 'little' or 'big'")

            return bytes((n >> i*8) & 0xff for i in order)

    .. versionadded:: 3.2
    .. versionchanged:: 3.11
       Đã thêm các giá trị đối số mặc định cho ``length`` và ``byteorder``.

.. classmethod:: int.from_bytes(bytes, byteorder='big', *, signed=False)

    Trả về số nguyên được biểu diễn bởi mảng byte đã cho.

        >>> int.from_bytes(b'\x00\x10', byteorder='big')
        16
        >>> int.from_bytes(b'\x00\x10', byteorder='little')
        4096
        >>> int.from_bytes(b'\xfc\x00', byteorder='big', signed=True)
        -1024
        >>> int.from_bytes(b'\xfc\x00', byteorder='big', signed=False)
        64512
        >>> int.from_bytes([255, 0, 0], byteorder='big')
        16711680

    Đối số *bytes* phải là một :term:`bytes-like object` hoặc một iterable tạo ra các byte.

    Đối số *byteorder* xác định thứ tự byte được dùng để biểu diễn số nguyên và mặc định là ``"big"``. Nếu *byteorder* là ``"big"``, byte có ý nghĩa lớn nhất nằm ở đầu mảng byte. Nếu *byteorder* là ``"little"``, byte có ý nghĩa lớn nhất nằm ở cuối mảng byte. Để yêu cầu thứ tự byte gốc của hệ thống máy chủ, hãy dùng :data:`sys.byteorder` làm giá trị thứ tự byte.

    Đối số *signed* cho biết có sử dụng biểu diễn bù hai (two's complement) cho số nguyên hay không.

    Tương đương với::

        def from_bytes(bytes, byteorder='big', signed=False):
            if byteorder == 'little':
                little_ordered = list(bytes)
            elif byteorder == 'big':
                little_ordered = list(reversed(bytes))
            else:
                raise ValueError("byteorder must be either 'little' or 'big'")

            n = sum(b << i*8 for i, b in enumerate(little_ordered))
            if signed and little_ordered and (little_ordered[-1] & 0x80):
                n -= 1 << 8*len(little_ordered)

            return n

    .. versionadded:: 3.2
    .. versionchanged:: 3.11
       Đã thêm giá trị đối số mặc định cho ``byteorder``.

.. method:: int.as_integer_ratio()

   Trả về một cặp số nguyên có tỉ số bằng số nguyên ban đầu và có mẫu số dương. Tỉ số nguyên của các số nguyên (số nguyên không phân số) luôn có số nguyên làm tử số và ``1`` làm mẫu số.

   .. versionadded:: 3.8

.. method:: int.is_integer()

   Trả về ``True``. Tồn tại để tương thích về kiểu linh hoạt (duck type) với :meth:`float.is_integer`.

   .. versionadded:: 3.12

Các phương thức bổ sung trên Float
----------------------------------

Kiểu float triển khai :class:`numbers.Real` :term:`abstract base class`. float cũng có các phương thức bổ sung sau.

.. classmethod:: float.from_number(x)

   Phương thức lớp trả về một số dấu phẩy động được tạo từ một số *x*.

   Nếu đối số là một số nguyên hoặc số dấu phẩy động, một số dấu phẩy động có cùng giá trị (trong phạm vi độ chính xác số dấu phẩy động của Python) sẽ được trả về. Nếu đối số nằm ngoài phạm vi của một số float trong Python, một :exc:`OverflowError` sẽ được phát sinh.

   Đối với một đối tượng Python tổng quát ``x``, ``float.from_number(x)`` ủy quyền cho ``x.__float__()``. Nếu :meth:`~object.__float__` chưa được định nghĩa thì sẽ chuyển sang :meth:`~object.__index__`.

   .. versionadded:: 3.14


.. method:: float.as_integer_ratio()

   Trả về một cặp số nguyên có thương bằng chính xác giá trị float ban đầu. Thương được rút gọn và có mẫu số dương.  Phát sinh
   :exc:`OverflowError` đối với vô cực và :exc:`ValueError` đối với NaN.

.. method:: float.is_integer()

   Trả về ``True`` nếu instance float là hữu hạn và có giá trị nguyên, nếu không thì trả về ``False``::

      >>> (-2.0).is_integer()
      True
      >>> (3.2).is_integer()
      False

Hai phương thức hỗ trợ chuyển đổi sang và từ chuỗi thập lục phân. Vì các float của Python được lưu trữ nội bộ dưới dạng số nhị phân, việc chuyển đổi một float sang hoặc từ chuỗi *decimal* thường có sai số làm tròn nhỏ. Ngược lại, chuỗi thập lục phân cho phép biểu diễn và đặc tả chính xác các số dấu phẩy động. Điều này có thể hữu ích khi gỡ lỗi và trong các công việc số học.


.. method:: float.hex()

   Trả về biểu diễn của một số dấu phẩy động dưới dạng chuỗi thập lục phân. Đối với các số dấu phẩy động hữu hạn, biểu diễn này luôn bao gồm ``0x`` ở đầu và ``p`` cùng số mũ ở cuối.


.. classmethod:: float.fromhex(s)

   Phương thức lớp trả về float được biểu diễn bởi chuỗi thập lục phân *s*. Chuỗi *s* có thể có khoảng trắng ở đầu và cuối.


Lưu ý rằng :meth:`float.hex` là một phương thức instance, còn
:meth:`float.fromhex` là một phương thức class.

Một chuỗi hệ thập lục phân có dạng::

   [sign] ['0x'] integer ['.' fraction] ['p' exponent]

trong đó ``sign`` tùy chọn có thể là ``+`` hoặc ``-``, ``integer`` và ``fraction`` là các chuỗi gồm các chữ số hệ thập lục phân, còn ``exponent`` là một số nguyên thập phân có thể có dấu ở đầu. Chữ hoa, chữ thường không ảnh hưởng, và phần nguyên hoặc phần thập phân phải có ít nhất một chữ số hệ thập lục phân. Cú pháp này tương tự cú pháp được quy định trong mục 6.4.4.2 của tiêu chuẩn C99, đồng thời cũng tương tự cú pháp được sử dụng trong Java từ phiên bản 1.5 trở đi. Cụ thể, kết quả của
:meth:`float.hex` có thể được sử dụng làm một literal số thực dấu phẩy động hệ thập lục phân trong mã C hoặc Java, và các chuỗi thập lục phân được tạo bởi ký tự định dạng ``%a`` của C hoặc ``Double.toHexString`` của Java được chấp nhận bởi
:meth:`float.fromhex`.


Lưu ý rằng số mũ được viết ở dạng thập phân thay vì hệ thập lục phân, và nó biểu thị lũy thừa của 2 dùng để nhân với hệ số. Ví dụ, chuỗi hệ thập lục phân ``0x3.a7p10`` biểu diễn số thực ``(3 + 10./16 + 7./16**2) * 2.0**10``, hoặc ``3740.0``::

   >>> float.fromhex('0x3.a7p10')
   3740.0


Áp dụng phép chuyển đổi ngược cho ``3740.0`` sẽ cho ra một chuỗi hệ thập lục phân khác biểu diễn cùng một số::

   >>> float.hex(3740.0)
   '0x1.d380000000000p+11'


Các phương thức bổ sung trên Complex
------------------------------------

Kiểu :class:`!complex` triển khai :class:`numbers.Complex`
:term:`abstract base class`.
:class:`!complex` cũng có các phương thức bổ sung sau.

.. classmethod:: complex.from_number(x)

   Phương thức lớp để chuyển đổi một số thành số phức.

   Đối với một đối tượng Python tổng quát ``x``, ``complex.from_number(x)`` ủy quyền cho ``x.__complex__()``.  Nếu :meth:`~object.__complex__` chưa được định nghĩa thì phương thức này chuyển sang :meth:`~object.__float__`.  Nếu :meth:`!__float__` chưa được định nghĩa thì phương thức này chuyển sang :meth:`~object.__index__`.

   .. versionadded:: 3.14


.. _numeric-hash:

Băm các kiểu số
---------------

Đối với các số ``x`` và ``y``, có thể thuộc các kiểu khác nhau, yêu cầu là ``hash(x) == hash(y)`` khi ``x == y`` (xem tài liệu về phương thức :meth:`~object.__hash__` để biết thêm chi tiết).  Để dễ triển khai và đạt hiệu quả trên nhiều kiểu số khác nhau (bao gồm :class:`int`,
:class:`float`, :class:`decimal.Decimal` và :class:`fractions.Fraction`) Giá trị băm của Python cho các kiểu số dựa trên một hàm toán học duy nhất được định nghĩa cho mọi số hữu tỉ, và do đó áp dụng cho mọi thể hiện của
:class:`int` và :class:`fractions.Fraction`, cũng như mọi thể hiện hữu hạn của
:class:`float` và :class:`decimal.Decimal`. Về cơ bản, hàm này được xác định bằng phép lấy phần dư modulo ``P`` với một số nguyên tố cố định ``P``. Giá trị của ``P`` được cung cấp cho Python dưới dạng thuộc tính :attr:`~sys.hash_info.modulus` của
:data:`sys.hash_info`.

.. impl-detail::

   Hiện tại, số nguyên tố được sử dụng là ``P = 2**31 - 1`` trên các máy có kiểu long C dài 32 bit và ``P = 2**61 - 1`` trên các máy có kiểu long C dài 64 bit.

Dưới đây là các quy tắc chi tiết:

- Nếu ``x = m / n`` là một số hữu tỉ không âm và ``n`` không chia hết cho ``P``, hãy định nghĩa ``hash(x)`` là ``m * invmod(n, P) % P``, trong đó ``invmod(n, P)`` cho nghịch đảo của ``n`` modulo ``P``.

- Nếu ``x = m / n`` là một số hữu tỉ không âm và ``n`` chia hết cho ``P`` (nhưng ``m`` thì không), thì ``n`` không có nghịch đảo modulo ``P`` và quy tắc trên không áp dụng; trong trường hợp này, định nghĩa ``hash(x)`` là giá trị hằng số ``sys.hash_info.inf``.

- Nếu ``x = m / n`` là một số hữu tỉ âm, hãy định nghĩa ``hash(x)`` là ``-hash(-x)``. Nếu giá trị băm thu được là ``-1``, hãy thay thế nó bằng ``-2``.

- Các giá trị cụ thể ``sys.hash_info.inf`` và ``-sys.hash_info.inf`` được dùng làm giá trị băm tương ứng cho dương vô cùng và âm vô cùng.

- Đối với một số :class:`complex` ``z``, các giá trị băm của phần thực và phần ảo được kết hợp bằng cách tính ``hash(z.real) + sys.hash_info.imag * hash(z.imag)``, rồi lấy phần dư theo modulo ``2**sys.hash_info.width`` để kết quả nằm trong ``range(-2**(sys.hash_info.width - 1), 2**(sys.hash_info.width - 1))``. Một lần nữa, nếu kết quả là ``-1``, nó sẽ được thay thế bằng ``-2``.


Để làm rõ các quy tắc trên, dưới đây là một đoạn mã Python ví dụ, tương đương với hàm băm tích hợp sẵn, dùng để tính giá trị băm của một số hữu tỉ, :class:`float` hoặc :class:`complex`::


   import sys, math

   def hash_fraction(m, n):
       """Compute the hash of a rational number m / n.

       Assumes m and n are integers, with n positive.
       Equivalent to hash(fractions.Fraction(m, n)).

       """
       P = sys.hash_info.modulus
       # Loại bỏ các thừa số chung của P. (Không cần thiết nếu m và n đã nguyên tố cùng nhau.)
       while m % P == n % P == 0:
           m, n = m // P, n // P

       if n % P == 0:
           hash_value = sys.hash_info.inf
       else:
           # Định lý nhỏ Fermat: pow(n, P-1, P) bằng 1, do đó
           # pow(n, P-2, P) cho nghịch đảo của n theo modulo P.
           hash_value = (abs(m) % P) * pow(n, P - 2, P) % P
       if m < 0:
           hash_value = -hash_value
       if hash_value == -1:
           hash_value = -2
       return hash_value

   def hash_float(x):
       """Compute the hash of a float x."""

       if math.isnan(x):
           return object.__hash__(x)
       elif math.isinf(x):
           return sys.hash_info.inf if x > 0 else -sys.hash_info.inf
       else:
           return hash_fraction(*x.as_integer_ratio())

   def hash_complex(z):
       """Compute the hash of a complex number z."""

       hash_value = hash_float(z.real) + sys.hash_info.imag * hash_float(z.imag)
       # thực hiện phép rút gọn có dấu modulo 2**sys.hash_info.width
       M = 2**(sys.hash_info.width - 1)
       hash_value = (hash_value & (M - 1)) - (hash_value & M)
       if hash_value == -1:
           hash_value = -2
       return hash_value

.. _bltin-boolean-values:
.. _typebool:

Kiểu Boolean - :class:`bool`
============================

Boolean biểu diễn các giá trị đúng/sai. Kiểu :class:`bool` có chính xác hai thể hiện hằng: ``True`` và ``False``.

.. index::
   single: False
   single: True
   pair: Boolean; values

Hàm tích hợp :func:`bool` chuyển đổi bất kỳ giá trị nào thành boolean, nếu giá trị đó có thể được diễn giải như một giá trị đúng/sai (xem phần :ref:`truth` ở trên).

Đối với các phép toán logic, hãy sử dụng :ref:`toán tử boolean <boolean>` ``and``, ``or`` và ``not``. Khi áp dụng các toán tử bit ``&``, ``|``, ``^`` cho hai boolean, chúng trả về một bool tương đương với các phép toán logic "and", "or", "xor". Tuy nhiên, nên ưu tiên các toán tử logic ``and``, ``or`` và ``!=`` hơn ``&``, ``|`` và ``^``.

.. deprecated:: 3.12

   Việc sử dụng toán tử đảo bit ``~`` đã lỗi thời và sẽ gây ra lỗi trong Python 3.16.

:class:`bool` là một lớp con của :class:`int` (xem :ref:`typesnumeric`). Trong nhiều ngữ cảnh số, ``False`` và ``True`` hoạt động tương ứng như các số nguyên 0 và 1. Tuy nhiên, không nên dựa vào điều này; thay vào đó, hãy chuyển đổi một cách tường minh bằng :func:`int`.

.. _typeiter:

Các kiểu iterator
=================

.. index::
   single: iterator protocol
   single: protocol; iterator
   single: sequence; iteration
   single: container; iteration over

Python hỗ trợ khái niệm lặp qua các container. Điều này được triển khai bằng hai phương thức riêng biệt; chúng được dùng để cho phép các lớp do người dùng định nghĩa hỗ trợ phép lặp. Các sequence, được mô tả chi tiết hơn bên dưới, luôn hỗ trợ các phương thức lặp.

Đối với các đối tượng container, cần định nghĩa một phương thức để cung cấp khả năng hỗ trợ :term:`iterable`:

.. XXX duplicated in reference/datamodel!

.. method:: container.__iter__()

   Trả về một đối tượng :term:`iterator`. Đối tượng này phải hỗ trợ iterator protocol được mô tả bên dưới. Nếu một container hỗ trợ nhiều kiểu lặp khác nhau, có thể cung cấp thêm các phương thức để yêu cầu riêng iterator cho từng kiểu lặp. (Ví dụ về một đối tượng hỗ trợ nhiều hình thức lặp là cấu trúc cây hỗ trợ cả duyệt theo chiều rộng và duyệt theo chiều sâu.) Phương thức này tương ứng với
   slot :c:member:`~PyTypeObject.tp_iter` của cấu trúc kiểu dành cho các đối tượng Python trong Python/C API.

Bản thân các đối tượng iterator phải hỗ trợ hai phương thức sau, cùng tạo thành :dfn:`giao thức iterator`:


.. method:: iterator.__iter__()

   Trả về chính đối tượng :term:`iterator`. Điều này là bắt buộc để cho phép cả container và iterator được sử dụng với :keyword:`for` và
   :keyword:`in` câu lệnh. Phương thức này tương ứng với
   slot :c:member:`~PyTypeObject.tp_iter` của cấu trúc kiểu dành cho các đối tượng Python trong Python/C API.


.. method:: iterator.__next__()

   Trả về mục tiếp theo từ :term:`iterator`. Nếu không còn mục nào, hãy raise exception :exc:`StopIteration`. Phương thức này tương ứng với slot :c:member:`~PyTypeObject.tp_iternext` của cấu trúc kiểu dành cho các đối tượng Python trong Python/C API.

Python định nghĩa một số đối tượng iterator để hỗ trợ việc lặp qua các kiểu sequence tổng quát và cụ thể, dictionary cũng như các dạng chuyên biệt hơn. Các kiểu cụ thể không quan trọng ngoài việc chúng triển khai iterator protocol.

Khi phương thức :meth:`~iterator.__next__` của iterator raise
:exc:`StopIteration`, nó phải tiếp tục làm như vậy trong các lần gọi tiếp theo. Các triển khai không tuân thủ thuộc tính này được xem là bị hỏng.


.. _generator-types:

Các kiểu Generator
------------------

Các :term:`generator`\s của Python cung cấp một cách thuận tiện để triển khai iterator protocol. Nếu phương thức :meth:`~object.__iter__` của một đối tượng container được triển khai dưới dạng generator, nó sẽ tự động trả về một iterator (về mặt kỹ thuật là một generator object) cung cấp các phương thức :meth:`~iterator.__iter__` và :meth:`~generator.__next__`. Có thể tìm thêm thông tin về generator trong :ref:`tài liệu về biểu thức yield <yieldexpr>`.


.. _typesseq:

Các kiểu sequence --- :class:`list`, :class:`tuple`, :class:`range`
===================================================================

Có ba kiểu sequence cơ bản: list, tuple và các đối tượng range. Các kiểu sequence bổ sung được thiết kế riêng để xử lý
:ref:`dữ liệu nhị phân <binaryseq>` và :ref:`chuỗi văn bản <textseq>` được mô tả trong các phần riêng.


.. _typesseq-common:

Các thao tác sequence phổ biến
------------------------------

.. index:: pair: object; sequence

Hầu hết các kiểu sequence, cả mutable và immutable, đều hỗ trợ các thao tác trong bảng sau. ABC :class:`collections.abc.Sequence` được cung cấp để giúp việc triển khai chính xác các thao tác này trên những kiểu sequence tùy chỉnh trở nên dễ dàng hơn.

Bảng sau liệt kê các thao tác sequence theo thứ tự ưu tiên tăng dần. Trong bảng, *s* và *t* là các sequence cùng kiểu, *n*, *i*, *j* và *k* là các số nguyên, còn *x* là một đối tượng bất kỳ đáp ứng mọi ràng buộc về kiểu và giá trị do *s* áp đặt.

Các phép toán ``in`` và ``not in`` có cùng độ ưu tiên với các phép toán so sánh. Các phép toán ``+`` (nối) và ``*`` (lặp) có cùng độ ưu tiên với các phép toán số học tương ứng. [3]_

Xem :ref:`time-complexity` để biết chi phí của các phép toán chuỗi khác nhau.

.. index::
   triple: operations on; sequence; types
   pair: built-in function; len
   pair: built-in function; min
   pair: built-in function; max
   pair: concatenation; operation
   pair: repetition; operation
   pair: subscript; operation
   pair: slice; operation
   pair: operator; in
   pair: operator; not in

+--------------------------+--------------------------------------------------------------------+---------+
| Phép toán                | Kết quả                                                            | Ghi chú |
+==========================+====================================================================+=========+
| ``x in s``               | ``True`` nếu một phần tử của *s* bằng *x*, nếu không thì ``False`` | \(1)    |
+--------------------------+--------------------------------------------------------------------+---------+
| ``x not in s``           | ``False`` nếu một phần tử của *s* bằng *x*, nếu không thì ``True`` | \(1)    |
+--------------------------+--------------------------------------------------------------------+---------+
| ``s + t``                | phép nối của *s* và *t*                                            | (6)(7)  |
+--------------------------+--------------------------------------------------------------------+---------+
| ``s * n`` hoặc ``n * s`` | tương đương với việc cộng *s* với chính nó *n* lần                 | (2)(7)  |
+--------------------------+--------------------------------------------------------------------+---------+
| ``s[i]``                 | *i*\ -là phần tử thứ của *s*, bắt đầu từ 0                         | (3)(8)  |
+--------------------------+--------------------------------------------------------------------+---------+
| ``s[i:j]``               | slice của *s* từ *i* đến *j*                                       | (3)(4)  |
+--------------------------+--------------------------------------------------------------------+---------+
| ``s[i:j:k]``             | slice của *s* từ *i* đến *j* với bước *k*                          | (3)(5)  |
+--------------------------+--------------------------------------------------------------------+---------+
| ``len(s)``               | độ dài của *s*                                                     |         |
+--------------------------+--------------------------------------------------------------------+---------+
| ``min(s)``               | phần tử nhỏ nhất của *s*                                           |         |
+--------------------------+--------------------------------------------------------------------+---------+
| ``max(s)``               | phần tử lớn nhất của *s*                                           |         |
+--------------------------+--------------------------------------------------------------------+---------+

Các sequence cùng kiểu cũng hỗ trợ phép so sánh. Cụ thể, tuple và list được so sánh theo thứ tự từ điển bằng cách so sánh các phần tử tương ứng. Điều này có nghĩa là để được xem là bằng nhau, mọi phần tử phải so sánh bằng nhau, đồng thời hai sequence phải cùng kiểu và có cùng độ dài. (Để biết đầy đủ chi tiết, hãy xem :ref:`comparisons` trong tài liệu tham khảo ngôn ngữ.)

.. index::
   single: loop; over mutable sequence
   single: mutable sequence; loop over

Các iterator tiến và iterator đảo ngược trên sequence có thể thay đổi truy cập các giá trị bằng một chỉ mục. Chỉ mục đó vẫn tiếp tục tăng (hoặc giảm) ngay cả khi sequence bên dưới bị thay đổi. Iterator chỉ kết thúc khi gặp một
:exc:`IndexError` hoặc một :exc:`StopIteration` (hoặc khi chỉ mục giảm xuống dưới 0).

Lưu ý:

(1)
   Mặc dù trong trường hợp tổng quát, các phép toán ``in`` và ``not in`` chỉ được dùng để kiểm tra chứa đơn giản, một số sequence chuyên biệt (chẳng hạn như :class:`str`, :class:`bytes` và :class:`bytearray`) cũng dùng chúng để kiểm tra chuỗi con::

      >>> "gg" in "eggs"
      True

(2)
   Các giá trị của *n* nhỏ hơn ``0`` được coi là ``0`` (tạo ra một dãy rỗng cùng kiểu với *s*). Lưu ý rằng các phần tử trong dãy *s* không được sao chép; chúng được tham chiếu nhiều lần. Điều này thường khiến những người mới học Python gặp khó khăn; hãy xét::

      >>> lists = [[]] * 3
      >>> lists
      [[], [], []]
      >>> lists[0].append(3)
      >>> lists
      [[3], [3], [3]]

   Điều xảy ra là ``[[]]`` là một danh sách một phần tử chứa một danh sách rỗng, vì vậy cả ba phần tử của ``[[]] * 3`` đều tham chiếu đến cùng một danh sách rỗng này. Việc sửa đổi bất kỳ phần tử nào của ``lists`` sẽ sửa đổi danh sách duy nhất này. Bạn có thể tạo một danh sách gồm các danh sách khác nhau theo cách này::

      >>> lists = [[] for i in range(3)]
      >>> lists[0].append(3)
      >>> lists[1].append(5)
      >>> lists[2].append(7)
      >>> lists
      [[3], [5], [7]]

   Bạn có thể xem phần giải thích thêm trong mục FAQ
   :ref:`faq-multidimensional-list`.

(3)
   Nếu *i* hoặc *j* là số âm, chỉ mục sẽ được tính tương đối từ cuối dãy *s*: ``len(s) + i`` hoặc ``len(s) + j`` sẽ được thay thế. Tuy nhiên, lưu ý rằng ``-0`` vẫn là ``0``.

(4)
   Lát cắt của *s* từ *i* đến *j* được định nghĩa là dãy các phần tử có chỉ mục *k* sao cho ``i <= k < j``.

   * Nếu *i* bị bỏ qua hoặc là ``None``, hãy sử dụng ``0``.
   * Nếu *j* bị bỏ qua hoặc là ``None``, hãy sử dụng ``len(s)``.
   * Nếu *i* hoặc *j* nhỏ hơn ``-len(s)``, hãy sử dụng ``0``.
   * Nếu *i* hoặc *j* lớn hơn ``len(s)``, hãy sử dụng ``len(s)``.
   * Nếu *i* lớn hơn hoặc bằng *j*, slice sẽ rỗng.

(5)
   Slice của *s* từ *i* đến *j* với bước *k* được định nghĩa là dãy các mục có chỉ mục ``x = i + n*k`` sao cho ``0 <= n < (j-i)/k``. Nói cách khác, các chỉ mục là ``i``, ``i+k``, ``i+2*k``, ``i+3*k`` và tiếp tục như vậy, dừng khi đạt đến *j* (nhưng không bao giờ bao gồm *j*). Khi *k* là số dương, *i* và *j* được giảm xuống ``len(s)`` nếu chúng lớn hơn giá trị này. Khi *k* là số âm, *i* và *j* được giảm xuống ``len(s) - 1`` nếu chúng lớn hơn giá trị này. Nếu *i* hoặc *j* bị bỏ qua hoặc là ``None``, chúng sẽ trở thành các giá trị "end" (giá trị kết thúc nào được dùng phụ thuộc vào dấu của *k*). Lưu ý rằng *k* không thể bằng 0. Nếu *k* là ``None``, nó được xử lý như ``1``.

.. _typesseq-repeated-concatenation:

(6)
   Việc nối các sequence bất biến luôn tạo ra một đối tượng mới. Điều này có nghĩa là việc xây dựng một sequence bằng cách nối lặp lại sẽ có chi phí runtime bậc hai theo tổng độ dài của sequence. Để có chi phí runtime tuyến tính, bạn phải chuyển sang một trong các phương án sau:

   * nếu nối các đối tượng :class:`str`, bạn có thể tạo một list và sử dụng
     :meth:`str.join` ở cuối; hoặc ghi vào một instance :class:`io.StringIO` và lấy giá trị của nó khi hoàn tất

   * khi nối các đối tượng :class:`bytes`, bạn cũng có thể sử dụng
     :meth:`bytes.join` hoặc :class:`io.BytesIO`, hoặc bạn có thể thực hiện phép nối tại chỗ với một đối tượng :class:`bytearray`. Các đối tượng :class:`bytearray` có thể thay đổi và có cơ chế cấp phát dư hiệu quả

   * khi nối các đối tượng :class:`tuple`, thay vào đó hãy mở rộng một :class:`list`

   * đối với các kiểu khác, hãy xem tài liệu về lớp tương ứng


(7)
  Một số kiểu sequence (chẳng hạn như :class:`range`) chỉ hỗ trợ các sequence phần tử tuân theo những mẫu cụ thể, vì vậy không hỗ trợ phép nối hoặc lặp sequence.

(8)
   Một :exc:`IndexError` được phát sinh nếu *i* nằm ngoài phạm vi của sequence.

.. rubric:: Các phương thức của sequence

Các kiểu sequence cũng hỗ trợ những phương thức sau:

.. method:: list.count(value, /)
            range.count(value, /) tuple.count(value, /)
   :no-contents-entry:
   :no-index-entry:
   :no-typesetting:
.. method:: sequence.count(value, /)

   Trả về tổng số lần xuất hiện của *value* trong *sequence*.

.. method:: list.index(value[, start[, stop]])
            range.index(value[, start[, stop]]) tuple.index(value[, start[, stop]])
   :no-contents-entry:
   :no-index-entry:
   :no-typesetting:
.. method:: sequence.index(value[, start[, stop]])

   Trả về chỉ mục của lần xuất hiện đầu tiên của *value* trong *sequence*.

   Gây ra :exc:`ValueError` nếu *value* không được tìm thấy trong *sequence*.

   Các đối số *start* hoặc *stop* cho phép tìm kiếm hiệu quả trong các phần con của sequence, bắt đầu từ *start* và kết thúc tại *stop*. Điều này gần tương đương với ``start + sequence[start:stop].index(value)``, chỉ khác là không sao chép dữ liệu.

   .. caution::
      Không phải tất cả các kiểu sequence đều hỗ trợ truyền đối số *start* và *stop*.


.. _typesseq-immutable:

Các kiểu sequence bất biến
--------------------------

.. index::
   triple: immutable; sequence; types
   pair: object; tuple
   pair: built-in function; hash

Hoạt động duy nhất mà các kiểu sequence bất biến thường triển khai nhưng các kiểu sequence khả biến không triển khai là hỗ trợ cho :func:`hash` tích hợp sẵn.

Hỗ trợ này cho phép các sequence bất biến, chẳng hạn như các instance :class:`tuple`, được sử dụng làm khóa :class:`dict` và được lưu trữ trong các instance :class:`set` và :class:`frozenset`.

Việc cố gắng băm một sequence bất biến chứa các giá trị không thể băm sẽ dẫn đến :exc:`TypeError`.


.. _typesseq-mutable:

Các kiểu sequence khả biến
--------------------------

.. index::
   triple: mutable; sequence; types
   pair: object; list
   pair: object; bytearray

Các thao tác trong bảng sau được định nghĩa trên các kiểu sequence khả biến. ABC :class:`collections.abc.MutableSequence` được cung cấp để giúp triển khai chính xác các thao tác này trên các kiểu sequence tùy chỉnh dễ dàng hơn.

Trong bảng, *s* là một thể hiện của kiểu sequence có thể thay đổi (mutable), *t* là một đối tượng iterable bất kỳ và *x* là một đối tượng tùy ý đáp ứng mọi giới hạn về kiểu và giá trị do *s* áp đặt (ví dụ: :class:`bytearray` chỉ chấp nhận các số nguyên đáp ứng giới hạn về giá trị ``0 <= x <= 255``).


.. index::
   triple: operations on; sequence; types
   triple: operations on; list; type
   pair: subscript; assignment
   pair: slice; assignment
   pair: statement; del

+------------------+---------------------------------------------------------------------------------+---------+
| Thao tác         | Kết quả                                                                         | Ghi chú |
+==================+=================================================================================+=========+
| ``s[i] = x``     | item *i* của *s* được thay thế bằng *x*                                         |         |
+------------------+---------------------------------------------------------------------------------+---------+
| ``del s[i]``     | xóa item *i* của *s*                                                            |         |
+------------------+---------------------------------------------------------------------------------+---------+
| ``s[i:j] = t``   | slice của *s* từ *i* đến *j* được thay thế bằng nội dung của iterable *t*       |         |
+------------------+---------------------------------------------------------------------------------+---------+
| ``del s[i:j]``   | xóa các phần tử của ``s[i:j]`` khỏi danh sách (giống như ``s[i:j] = []``)       |         |
+------------------+---------------------------------------------------------------------------------+---------+
| ``s[i:j:k] = t`` | các phần tử của ``s[i:j:k]`` được thay thế bằng các phần tử của *t*             | \(1)    |
+------------------+---------------------------------------------------------------------------------+---------+
| ``del s[i:j:k]`` | xóa các phần tử của ``s[i:j:k]`` khỏi danh sách                                 |         |
+------------------+---------------------------------------------------------------------------------+---------+
| ``s += t``       | mở rộng *s* bằng nội dung của *t* (phần lớn giống như ``s[len(s):len(s)] = t``) |         |
+------------------+---------------------------------------------------------------------------------+---------+
| ``s *= n``       | cập nhật *s* với nội dung của nó được lặp lại *n* lần                           | \(2)    |
+------------------+---------------------------------------------------------------------------------+---------+

Lưu ý:

(1)
   Nếu *k* không bằng ``1``, *t* phải có cùng độ dài với lát cắt mà nó thay thế.

(2)
   Giá trị *n* là một số nguyên hoặc một đối tượng triển khai
   :meth:`~object.__index__`.  Các giá trị bằng không và âm của *n* sẽ xóa sequence.  Các phần tử trong sequence không được sao chép; chúng được tham chiếu nhiều lần, như đã giải thích đối với ``s * n`` trong :ref:`typesseq-common`.

.. rubric:: Các phương thức của Mutable sequence

Các kiểu Mutable sequence cũng hỗ trợ những phương thức sau:

.. method:: bytearray.append(value, /)
            list.append(value, /)
   :no-contents-entry:
   :no-index-entry:
   :no-typesetting:
.. method:: sequence.append(value, /)

   Thêm *value* vào cuối sequence. Điều này tương đương với việc viết ``seq[len(seq):len(seq)] = [value]``.

.. method:: bytearray.clear()
            list.clear()
   :no-contents-entry:
   :no-index-entry:
   :no-typesetting:
.. method:: sequence.clear()

   .. versionadded:: 3.3

   Xóa tất cả các phần tử khỏi *sequence*. Điều này tương đương với việc viết ``del sequence[:]``.

.. method:: bytearray.copy()
            list.copy()
   :no-contents-entry:
   :no-index-entry:
   :no-typesetting:
.. method:: sequence.copy()

   .. versionadded:: 3.3

   Tạo một bản sao nông của *sequence*. Điều này tương đương với việc viết ``sequence[:]``.

   .. hint:: Phương thức :meth:`!copy` không thuộc về
             :class:`~collections.abc.MutableSequence` :class:`~abc.ABC`,
             nhưng hầu hết các kiểu sequence có thể thay đổi cụ thể đều cung cấp phương thức này.

.. method:: bytearray.extend(iterable, /)
            list.extend(iterable, /)
   :no-contents-entry:
   :no-index-entry:
   :no-typesetting:
.. method:: sequence.extend(iterable, /)

   Mở rộng *sequence* bằng nội dung của *iterable*. Phần lớn, thao tác này giống với việc viết ``seq[len(seq):len(seq)] = iterable``.

.. method:: bytearray.insert(index, value, /)
            list.insert(index, value, /)
   :no-contents-entry:
   :no-index-entry:
   :no-typesetting:
.. method:: sequence.insert(index, value, /)

   Chèn *value* vào *sequence* tại *index* đã cho. Tương đương với việc viết ``sequence[index:index] = [value]``.

.. method:: bytearray.pop(index=-1, /)
            list.pop(index=-1, /)
   :no-contents-entry:
   :no-index-entry:
   :no-typesetting:
.. method:: sequence.pop(index=-1, /)

   Lấy mục tại *index* và đồng thời xóa mục đó khỏi *sequence*. Theo mặc định, mục cuối cùng trong *sequence* sẽ bị xóa và trả về.

.. method:: bytearray.remove(value, /)
            list.remove(value, /)
   :no-contents-entry:
   :no-index-entry:
   :no-typesetting:
.. method:: sequence.remove(value, /)

   Xóa mục đầu tiên khỏi *sequence* thỏa mãn ``sequence[i] == value``.

   Gây ra :exc:`ValueError` nếu không tìm thấy *value* trong *sequence*.

.. method:: bytearray.reverse()
            list.reverse()
   :no-contents-entry:
   :no-index-entry:
   :no-typesetting:
.. method:: sequence.reverse()

   Đảo ngược các phần tử của *sequence* ngay tại chỗ. Phương thức này giúp tiết kiệm không gian khi đảo ngược một sequence lớn. Để nhắc người dùng rằng phương thức này hoạt động bằng side effect, nó trả về ``None``.


.. _typesseq-list:

Danh sách
---------

.. index:: pair: object; list

Danh sách là các sequence có thể thay đổi, thường được dùng để lưu trữ các tập hợp phần tử đồng nhất (mức độ tương đồng chính xác sẽ khác nhau tùy theo ứng dụng).

.. class:: list(iterable=(), /)

   Có thể tạo danh sách bằng một số cách:

   * Sử dụng một cặp dấu ngoặc vuông để biểu thị danh sách rỗng: ``[]``
   * Sử dụng dấu ngoặc vuông, phân tách các phần tử bằng dấu phẩy: ``[a]``, ``[a, b, c]``
   * Sử dụng list comprehension: ``[x for x in iterable]``
   * Sử dụng type constructor: ``list()`` hoặc ``list(iterable)``

   Constructor tạo một list có các phần tử giống và theo cùng thứ tự như các phần tử của *iterable*.  *iterable* có thể là một sequence, một container hỗ trợ phép lặp hoặc một iterator object.  Nếu *iterable* đã là một list, một bản sao sẽ được tạo và trả về, tương tự như ``iterable[:]``. Ví dụ, ``list('abc')`` trả về ``['a', 'b', 'c']`` và ``list( (1, 2, 3) )`` trả về ``[1, 2, 3]``. Nếu không cung cấp đối số, constructor sẽ tạo một list trống mới, ``[]``.


   Nhiều thao tác khác cũng tạo ra list, bao gồm cả built-in :func:`sorted`.

   List là :ref:`generic <generics>` theo kiểu dữ liệu của các phần tử.

   List triển khai tất cả các phép toán :ref:`common <typesseq-common>` và
   các phép toán trên sequence :ref:`mutable <typesseq-mutable>`. List cũng cung cấp phương thức bổ sung sau:

   .. method:: list.sort(*, key=None, reverse=False)

      Phương thức này sắp xếp danh sách ngay tại chỗ, chỉ sử dụng các phép so sánh ``<`` giữa các phần tử. Ngoại lệ không bị bỏ qua - nếu bất kỳ phép so sánh nào không thành công, toàn bộ thao tác sắp xếp sẽ thất bại (và danh sách có thể sẽ ở trạng thái đã bị sửa đổi một phần).

      :meth:`sort` chấp nhận hai đối số chỉ có thể được truyền bằng tên (:ref:`đối số chỉ có thể truyền bằng từ khóa <keyword-only_parameter>`):

      *key* chỉ định một hàm nhận một đối số, được dùng để trích xuất khóa so sánh từ mỗi phần tử danh sách (ví dụ: ``key=str.lower``). Khóa tương ứng với mỗi mục trong danh sách được tính một lần, sau đó được sử dụng trong toàn bộ quá trình sắp xếp. Giá trị mặc định của ``None`` có nghĩa là các mục trong danh sách được sắp xếp trực tiếp mà không tính một giá trị khóa riêng.

      Tiện ích :func:`functools.cmp_to_key` có sẵn để chuyển đổi hàm *cmp* kiểu 2.x thành hàm *key*.

      *reverse* là một giá trị boolean. Nếu được đặt thành ``True``, các phần tử trong danh sách sẽ được sắp xếp như thể mỗi phép so sánh đều bị đảo ngược.

      Phương thức này sửa đổi chuỗi ngay tại chỗ để tiết kiệm không gian khi sắp xếp một chuỗi lớn. Để nhắc người dùng rằng phương thức này hoạt động bằng side effect, nó không trả về chuỗi đã sắp xếp (sử dụng :func:`sorted` để yêu cầu rõ ràng một instance danh sách mới đã được sắp xếp).

      Phương thức :meth:`sort` được đảm bảo là stable. Một phép sắp xếp là stable nếu đảm bảo không thay đổi thứ tự tương đối của các phần tử được so sánh là bằng nhau --- điều này hữu ích khi sắp xếp qua nhiều lượt (ví dụ: sắp xếp theo phòng ban, sau đó theo bậc lương).

      Để xem các ví dụ về sắp xếp và hướng dẫn ngắn về sắp xếp, hãy xem :ref:`sortinghowto`.

      .. impl-detail::

         Trong khi một danh sách đang được sắp xếp, tác động của việc cố gắng thay đổi hoặc thậm chí kiểm tra danh sách là không xác định. Python được triển khai bằng C sẽ làm cho danh sách có vẻ trống trong suốt thời gian này và phát sinh :exc:`ValueError` nếu phát hiện danh sách đã bị thay đổi trong quá trình sắp xếp.

.. seealso::

   Để biết thông tin chi tiết về các đảm bảo an toàn luồng đối với các đối tượng :class:`list`, hãy xem :ref:`thread-safety-list`.


.. _typesseq-tuple:

Tuple
-----

.. index:: pair: object; tuple

Tuple là các sequence bất biến, thường được dùng để lưu trữ các tập hợp dữ liệu không đồng nhất (chẳng hạn như các tuple 2 phần tử do built-in :func:`enumerate` tạo ra). Tuple cũng được dùng trong các trường hợp cần một sequence bất biến gồm dữ liệu đồng nhất (chẳng hạn như cho phép lưu trữ trong một :class:`set` hoặc
đối tượng :class:`dict`).

.. class:: tuple(iterable=(), /)

   Tuple có thể được tạo theo nhiều cách:

   * Dùng một cặp dấu ngoặc đơn để biểu thị tuple rỗng: ``()``
   * Dùng dấu phẩy ở cuối cho tuple một phần tử: ``a,`` hoặc ``(a,)``
   * Phân tách các phần tử bằng dấu phẩy: ``a, b, c`` hoặc ``(a, b, c)``
   * Sử dụng built-in :func:`tuple`: ``tuple()`` hoặc ``tuple(iterable)``

   Hàm khởi tạo tạo ra một tuple có các phần tử giống và theo cùng thứ tự như các phần tử của *iterable*.  *iterable* có thể là một sequence, một container hỗ trợ iteration hoặc một iterator object.  Nếu *iterable* đã là một tuple, hàm sẽ trả về nó mà không thay đổi. Ví dụ, ``tuple('abc')`` trả về ``('a', 'b', 'c')`` và ``tuple( [1, 2, 3] )`` trả về ``(1, 2, 3)``. Nếu không cung cấp đối số, hàm khởi tạo sẽ tạo một tuple rỗng mới, ``()``.

   Lưu ý rằng chính dấu phẩy tạo ra tuple, không phải dấu ngoặc đơn. Dấu ngoặc đơn là tùy chọn, ngoại trừ trường hợp tuple rỗng hoặc khi cần dùng chúng để tránh sự mơ hồ về cú pháp. Ví dụ, ``f(a, b, c)`` là một lời gọi hàm với ba đối số, còn ``f((a, b, c))`` là một lời gọi hàm với một tuple 3 phần tử làm đối số duy nhất.

   Tuple triển khai tất cả các thao tác sequence :ref:`common <typesseq-common>`.

   Tuple là :ref:`generic <generics>` theo các kiểu của nội dung bên trong. Để biết thêm thông tin, hãy tham khảo
   :ref:`the typing documentation on annotating tuples <annotating-tuples>`.

Đối với các tập hợp dữ liệu không đồng nhất mà việc truy cập theo tên rõ ràng hơn việc truy cập theo chỉ mục, :func:`collections.namedtuple` có thể là lựa chọn phù hợp hơn so với một đối tượng tuple đơn giản.


.. _typesseq-range:

Ranges
------

.. index:: pair: object; range

Kiểu :class:`range` biểu diễn một chuỗi số bất biến và thường được dùng để lặp một số lần cụ thể trong các vòng lặp :keyword:`for`.

.. class:: range(stop, /)
           range(start, stop, step=1, /)

   Các đối số của hàm khởi tạo range phải là số nguyên (dù là kiểu tích hợp sẵn
   :class:`int` hoặc bất kỳ đối tượng nào triển khai phương thức đặc biệt :meth:`~object.__index__`). Nếu đối số *step* bị bỏ qua, giá trị mặc định là ``1``. Nếu đối số *start* bị bỏ qua, giá trị mặc định là ``0``. Nếu *step* bằng 0, :exc:`ValueError` sẽ được raise.

   Đối với *step* dương, nội dung của một range ``r`` được xác định bởi công thức ``r[i] = start + step*i``, trong đó ``i >= 0`` và ``r[i] < stop``.

   Đối với *step* âm, nội dung của range vẫn được xác định bởi công thức ``r[i] = start + step*i``, nhưng các ràng buộc là ``i >= 0`` và ``r[i] > stop``.

   Một đối tượng range sẽ rỗng nếu ``r[0]`` không thỏa mãn ràng buộc về giá trị. Các range hỗ trợ chỉ mục âm, nhưng những chỉ mục này được hiểu là chỉ mục từ cuối của sequence được xác định bởi các chỉ mục dương.

   Các range chứa giá trị tuyệt đối lớn hơn :data:`sys.maxsize` vẫn được cho phép, nhưng một số tính năng (chẳng hạn như :func:`len`) có thể phát sinh
   :exc:`OverflowError`.

   Ví dụ về range::

      >>> list(range(10))
      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
      >>> list(range(1, 11))
      [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
      >>> list(range(0, 30, 5))
      [0, 5, 10, 15, 20, 25]
      >>> list(range(0, 10, 3))
      [0, 3, 6, 9]
      >>> list(range(0, -10, -1))
      [0, -1, -2, -3, -4, -5, -6, -7, -8, -9]
      >>> list(range(0))
      []
      >>> list(range(1, 0))
      []

   Các range triển khai tất cả các phép toán sequence :ref:`common <typesseq-common>` ngoại trừ phép nối và phép lặp (do các đối tượng range chỉ có thể biểu diễn những sequence tuân theo một mẫu nghiêm ngặt, trong khi phép lặp và phép nối thường sẽ vi phạm mẫu đó).

   .. attribute:: start

      Giá trị của tham số *start* (hoặc ``0`` nếu không cung cấp tham số này)

   .. attribute:: stop

      Giá trị của tham số *stop*

   .. attribute:: step

      Giá trị của tham số *step* (hoặc ``1`` nếu không cung cấp tham số này)

Ưu điểm của kiểu :class:`range` so với một :class:`list` thông thường hoặc
:class:`tuple` là một đối tượng :class:`range` luôn chiếm cùng một lượng bộ nhớ (nhỏ), bất kể kích thước của phạm vi mà nó biểu diễn (vì nó chỉ lưu trữ các giá trị ``start``, ``stop`` và ``step``, đồng thời tính toán các phần tử và phạm vi con riêng lẻ khi cần).

Các đối tượng phạm vi triển khai ABC :class:`collections.abc.Sequence` và cung cấp những tính năng như kiểm tra phép chứa, tra cứu chỉ mục phần tử, cắt lát và hỗ trợ chỉ mục âm (xem :ref:`typesseq`):

   >>> r = range(0, 20, 2)
   >>> r
   range(0, 20, 2)
   >>> 11 in r
   False
   >>> 10 in r
   True
   >>> r.index(10)
   5
   >>> r[5]
   10
   >>> r[:5]
   range(0, 10, 2)
   >>> r[-1]
   18

Việc kiểm tra tính bằng nhau của các đối tượng phạm vi với ``==`` và ``!=`` sẽ so sánh chúng như các sequence. Nói cách khác, hai đối tượng phạm vi được xem là bằng nhau nếu chúng biểu diễn cùng một sequence giá trị. (Lưu ý rằng hai đối tượng phạm vi so sánh bằng nhau có thể có các giá trị :attr:`~range.start` khác nhau,
các thuộc tính :attr:`~range.stop` và :attr:`~range.step`, chẳng hạn như ``range(0) == range(2, 1, 3)`` hoặc ``range(0, 3, 2) == range(0, 4, 2)``.)

.. versionchanged:: 3.2
   Triển khai Sequence ABC. Hỗ trợ slicing và các chỉ mục âm. Kiểm tra việc một đối tượng :class:`int` có thuộc tập hợp trong thời gian hằng số thay vì lặp qua tất cả các phần tử.

.. versionchanged:: 3.3
   Định nghĩa '==' và '!=' để so sánh các đối tượng range dựa trên chuỗi giá trị mà chúng xác định (thay vì so sánh dựa trên danh tính đối tượng).

   Đã thêm các thuộc tính :attr:`~range.start`, :attr:`~range.stop` và :attr:`~range.step`.

.. seealso::

   * `Công thức linspace <https://code.activestate.com/recipes/579000-equally-spaced-numbers-linspace/>`_ cho thấy cách triển khai một phiên bản lazy của range, phù hợp với các ứng dụng số dấu phẩy động.

.. index::
   single: string; text sequence type
   single: str (built-in class); (see also string)
   pair: object; string

.. _text-methods-summary:

Tóm tắt các phương thức của kiểu chuỗi văn bản và chuỗi nhị phân
================================================================
Bảng sau đây tóm tắt các phương thức của kiểu chuỗi văn bản và chuỗi nhị phân theo từng danh mục.


+--------------------------+-------------------------------------------+---------------------------------------------------+
| Category                 |  :class:`str` methods                     |   :class:`bytes` and :class:`bytearray` methods   |
+==========================+===========================================+===================================================+
| Formatting               |  :meth:`str.format`                       |                                                   |
|                          +-------------------------------------------+---------------------------------------------------+
|                          |  :meth:`str.format_map`                   |                                                   |
|                          +-------------------------------------------+---------------------------------------------------+
|                          |  :ref:`f-strings`                         |                                                   |
|                          +-------------------------------------------+---------------------------------------------------+
|                          |  :ref:`old-string-formatting`             |  :ref:`bytes-formatting`                          |
+--------------------------+------------------+------------------------+--------------------+------------------------------+
| Searching and Replacing  | :meth:`str.find` | :meth:`str.rfind`      | :meth:`bytes.find` | :meth:`bytes.rfind`          |
|                          +------------------+------------------------+--------------------+------------------------------+
|                          | :meth:`str.index`| :meth:`str.rindex`     | :meth:`bytes.index`| :meth:`bytes.rindex`         |
|                          +------------------+------------------------+--------------------+------------------------------+
|                          |  :meth:`str.startswith`                   |  :meth:`bytes.startswith`                         |
|                          +-------------------------------------------+---------------------------------------------------+
|                          |  :meth:`str.endswith`                     |  :meth:`bytes.endswith`                           |
|                          +-------------------------------------------+---------------------------------------------------+
|                          |  :meth:`str.count`                        |  :meth:`bytes.count`                              |
|                          +-------------------------------------------+---------------------------------------------------+
|                          |  :meth:`str.replace`                      |  :meth:`bytes.replace`                            |
+--------------------------+-------------------+-----------------------+---------------------+-----------------------------+
| Splitting and Joining    | :meth:`str.split` | :meth:`str.rsplit`    | :meth:`bytes.split` | :meth:`bytes.rsplit`        |
|                          +-------------------+-----------------------+---------------------+-----------------------------+
|                          |  :meth:`str.splitlines`                   |  :meth:`bytes.splitlines`                         |
|                          +-------------------------------------------+---------------------------------------------------+
|                          |  :meth:`str.partition`                    |  :meth:`bytes.partition`                          |
|                          +-------------------------------------------+---------------------------------------------------+
|                          |  :meth:`str.rpartition`                   |  :meth:`bytes.rpartition`                         |
|                          +-------------------------------------------+---------------------------------------------------+
|                          |  :meth:`str.join`                         |  :meth:`bytes.join`                               |
+--------------------------+-------------------------------------------+---------------------------------------------------+
| String Classification    |  :meth:`str.isalpha`                      |  :meth:`bytes.isalpha`                            |
|                          +-------------------------------------------+---------------------------------------------------+
|                          |  :meth:`str.isdecimal`                    |                                                   |
|                          +-------------------------------------------+---------------------------------------------------+
|                          |  :meth:`str.isdigit`                      |  :meth:`bytes.isdigit`                            |
|                          +-------------------------------------------+---------------------------------------------------+
|                          |  :meth:`str.isnumeric`                    |                                                   |
|                          +-------------------------------------------+---------------------------------------------------+
|                          |  :meth:`str.isalnum`                      |  :meth:`bytes.isalnum`                            |
|                          +-------------------------------------------+---------------------------------------------------+
|                          |  :meth:`str.isidentifier`                 |                                                   |
|                          +-------------------------------------------+---------------------------------------------------+
|                          |  :meth:`str.islower`                      |  :meth:`bytes.islower`                            |
|                          +-------------------------------------------+---------------------------------------------------+
|                          |  :meth:`str.isupper`                      |  :meth:`bytes.isupper`                            |
|                          +-------------------------------------------+---------------------------------------------------+
|                          |  :meth:`str.istitle`                      |  :meth:`bytes.istitle`                            |
|                          +-------------------------------------------+---------------------------------------------------+
|                          |  :meth:`str.isspace`                      |  :meth:`bytes.isspace`                            |
|                          +-------------------------------------------+---------------------------------------------------+
|                          |  :meth:`str.isprintable`                  |                                                   |
+--------------------------+-------------------------------------------+---------------------------------------------------+
| Case Manipulation        |  :meth:`str.lower`                        |  :meth:`bytes.lower`                              |
|                          +-------------------------------------------+---------------------------------------------------+
|                          |  :meth:`str.upper`                        |  :meth:`bytes.upper`                              |
|                          +-------------------------------------------+---------------------------------------------------+
|                          |  :meth:`str.casefold`                     |                                                   |
|                          +-------------------------------------------+---------------------------------------------------+
|                          |  :meth:`str.capitalize`                   |  :meth:`bytes.capitalize`                         |
|                          +-------------------------------------------+---------------------------------------------------+
|                          |  :meth:`str.title`                        |  :meth:`bytes.title`                              |
|                          +-------------------------------------------+---------------------------------------------------+
|                          |  :meth:`str.swapcase`                     |  :meth:`bytes.swapcase`                           |
+--------------------------+-------------------+-----------------------+---------------------+-----------------------------+
| Padding and Stripping    | :meth:`str.ljust` | :meth:`str.rjust`     | :meth:`bytes.ljust` | :meth:`bytes.rjust`         |
|                          +-------------------+-----------------------+---------------------+-----------------------------+
|                          |  :meth:`str.center`                       |  :meth:`bytes.center`                             |
|                          +-------------------------------------------+---------------------------------------------------+
|                          |  :meth:`str.expandtabs`                   |  :meth:`bytes.expandtabs`                         |
|                          +-------------------------------------------+---------------------------------------------------+
|                          |  :meth:`str.strip`                        |  :meth:`bytes.strip`                              |
|                          +--------------------+----------------------+----------------------+----------------------------+
|                          | :meth:`str.lstrip` | :meth:`str.rstrip`   | :meth:`bytes.lstrip` | :meth:`bytes.rstrip`       |
|                          +--------------------+----------------------+----------------------+----------------------------+
|                          |  :meth:`str.removeprefix`                 |  :meth:`bytes.removeprefix`                       |
|                          +-------------------------------------------+---------------------------------------------------+
|                          |  :meth:`str.removesuffix`                 |  :meth:`bytes.removesuffix`                       |
+--------------------------+-------------------------------------------+---------------------------------------------------+
| Translation and Encoding |  :meth:`str.translate`                    |  :meth:`bytes.translate`                          |
|                          +-------------------------------------------+---------------------------------------------------+
|                          |  :meth:`str.maketrans`                    |  :meth:`bytes.maketrans`                          |
|                          +-------------------------------------------+---------------------------------------------------+
|                          |  :meth:`str.encode`                       |                                                   |
|                          +-------------------------------------------+---------------------------------------------------+
|                          |                                           |  :meth:`bytes.decode`                             |
+--------------------------+-------------------------------------------+---------------------------------------------------+

.. _textseq:

Kiểu chuỗi văn bản --- :class:`str`
===================================

Dữ liệu dạng văn bản trong Python được xử lý bằng các đối tượng :class:`str`, hay :dfn:`chuỗi`. Chuỗi là bất biến
:ref:`các chuỗi <typesseq>` của các điểm mã Unicode. Chuỗi ký tự được viết theo nhiều cách khác nhau:

* Dấu nháy đơn: ``'allows embedded "double" quotes'``
* Dấu nháy kép: ``"allows embedded 'single' quotes"``
* Dấu nháy ba: ``'''Three single quotes'''``, ``"""Three double quotes"""``

Chuỗi được đặt trong ba dấu nháy có thể trải dài trên nhiều dòng - mọi khoảng trắng đi kèm đều sẽ được đưa vào chuỗi ký tự.

Các string literal là một phần của cùng một biểu thức và chỉ có khoảng trắng ở giữa sẽ được ngầm chuyển thành một string literal duy nhất. Nghĩa là, ``("spam " "eggs") == "spam eggs"``.

Xem :ref:`strings` để biết thêm về các dạng string literal khác nhau, bao gồm :ref:`escape sequences <escape-sequences>` được hỗ trợ và tiền tố ``r`` ("raw"), vốn vô hiệu hóa hầu hết việc xử lý escape sequence.

String cũng có thể được tạo từ các đối tượng khác bằng constructor :class:`str`.

Vì không có kiểu "character" riêng biệt, việc lập chỉ mục một string sẽ tạo ra các string có độ dài 1. Nghĩa là, với một string không rỗng *s*, ``s[0] == s[0:1]``.

.. index::
   pair: object; io.StringIO

Cũng không có kiểu string có thể thay đổi, nhưng có thể sử dụng :meth:`str.join` hoặc
:class:`io.StringIO` để xây dựng string từ nhiều fragment một cách hiệu quả.

.. versionchanged:: 3.3
   Để tương thích ngược với dòng Python 2, tiền tố ``u`` một lần nữa được cho phép trong các string literal. Nó không ảnh hưởng đến ý nghĩa của string literal và không thể kết hợp với tiền tố ``r``.


.. index::
   single: string; str (built-in class)

.. class:: str(*, encoding='utf-8', errors='strict')
           str(object) str(object, encoding, errors='strict') str(object, *, errors)

   Trả về phiên bản :ref:`string <textseq>` của *object*. Nếu không cung cấp *object*, hàm trả về chuỗi rỗng. Nếu không, hành vi của ``str()`` phụ thuộc vào việc có cung cấp *encoding* hoặc *errors* hay không, như sau.

   Nếu không cung cấp cả *encoding* lẫn *errors*, ``str(object)`` sẽ trả về
   :meth:`type(object).__str__(object) <object.__str__>`, là biểu diễn chuỗi "không chính thức" hoặc dễ in của *object*. Với các đối tượng chuỗi, đây chính là chuỗi đó. Nếu *object* không có phương thức :meth:`~object.__str__`, thì :func:`str` sẽ quay về việc trả về
   :func:`repr(object) <repr>`.

   .. index::
      single: buffer protocol; str (built-in class)
      single: bytes; str (built-in class)

   Nếu cung cấp ít nhất một trong *encoding* hoặc *errors*, *object* phải là
   :term:`bytes-like object` (ví dụ: :class:`bytes` hoặc :class:`bytearray`). Trong trường hợp này, nếu *object* là một đối tượng :class:`bytes` (hoặc :class:`bytearray`), thì ``str(bytes, encoding, errors)`` tương đương với
   :meth:`bytes.decode(encoding, errors) <bytes.decode>`. Nếu không, đối tượng bytes nằm bên dưới đối tượng buffer sẽ được lấy ra trước khi gọi
   :meth:`bytes.decode`.  Xem :ref:`binaryseq` và
   :ref:`bufferobjects` để biết thông tin về các đối tượng buffer.

   Việc truyền một đối tượng :class:`bytes` vào :func:`str` mà không có các đối số *encoding* hoặc *errors* thuộc trường hợp đầu tiên của việc trả về biểu diễn chuỗi không chính thức (xem thêm tùy chọn dòng lệnh :option:`-b` của Python).  Ví dụ::

      >>> str(b'Zoot!')
      "b'Zoot!'"

   Để biết thêm thông tin về lớp ``str`` và các phương thức của lớp này, hãy xem
   :ref:`textseq` và phần :ref:`string-methods` bên dưới.  Để xuất các chuỗi được định dạng, hãy xem các phần :ref:`f-strings` và :ref:`formatstrings`.  Ngoài ra, hãy xem phần :ref:`stringservices`.


.. index::
   pair: string; methods

.. _string-methods:

Các phương thức chuỗi
---------------------

.. index::
   pair: module; re

Chuỗi triển khai tất cả các phép toán trình tự :ref:`phổ biến <typesseq-common>`, cùng với các phương thức bổ sung được mô tả dưới đây.

Chuỗi cũng hỗ trợ hai kiểu định dạng chuỗi, trong đó một kiểu cung cấp mức độ linh hoạt và khả năng tùy chỉnh cao (xem :meth:`str.format`,
:ref:`formatstrings` và :ref:`string-formatting`) còn kiểu kia dựa trên định dạng theo kiểu C ``printf``, xử lý phạm vi kiểu dữ liệu hẹp hơn và khó sử dụng đúng hơn một chút, nhưng thường nhanh hơn trong những trường hợp mà nó có thể xử lý (:ref:`old-string-formatting`).

Phần :ref:`textservices` của thư viện chuẩn bao gồm một số module khác cung cấp nhiều tiện ích liên quan đến văn bản (bao gồm hỗ trợ biểu thức chính quy trong module :mod:`re`).

.. method:: str.capitalize()

   Trả về một bản sao của chuỗi với ký tự đầu tiên được viết hoa và các ký tự còn lại được viết thường.

   .. versionchanged:: 3.8
      Ký tự đầu tiên hiện được chuyển thành chữ hoa kiểu titlecase thay vì chữ hoa thông thường. Điều này có nghĩa là các ký tự như digraph chỉ được viết hoa chữ cái đầu tiên, thay vì toàn bộ ký tự.

.. method:: str.casefold()

   Trả về một bản sao của chuỗi đã được casefold. Các chuỗi đã được casefold có thể được dùng để so khớp không phân biệt hoa thường.

   Casefold tương tự như chuyển thành chữ thường nhưng mạnh hơn, vì mục đích của nó là loại bỏ mọi phân biệt hoa thường trong một chuỗi. Ví dụ, chữ cái thường tiếng Đức ``'ß'`` tương đương với ``"ss"``. Vì vốn đã là chữ thường, :meth:`lower` sẽ không làm gì với ``'ß'``; :meth:`casefold` chuyển nó thành ``"ss"``. Ví dụ:

   .. doctest::

      >>> 'straße'.lower()
      'straße'
      >>> 'straße'.casefold()
      'strasse'

   Thuật toán chuyển đổi kiểu chữ được `described in section 3.13 'Default Case Folding' of the Unicode Standard <https://www.unicode.org/versions/Unicode16.0.0/core-spec/chapter-3/#G33992>`__.

   .. versionadded:: 3.3


.. method:: str.center(width, fillchar=' ', /)

   Trả về chuỗi được căn giữa trong một chuỗi có độ dài *width*. Việc đệm được thực hiện bằng *fillchar* được chỉ định (mặc định là dấu cách ASCII). Chuỗi ban đầu được trả về nếu *width* nhỏ hơn hoặc bằng ``len(s)``. Ví dụ::

      >>> 'Python'.center(10)
      '  Python  '
      >>> 'Python'.center(10, '-')
      '--Python--'
      >>> 'Python'.center(4)
      'Python'


.. method:: str.count(sub[, start[, end]])

   Trả về số lần xuất hiện không chồng lấp của chuỗi con *sub* trong phạm vi [*start*, *end*]. Các đối số tùy chọn *start* và *end* được diễn giải như trong ký hiệu lát cắt.

   Nếu *sub* là chuỗi rỗng, trả về số chuỗi rỗng nằm giữa các ký tự, bằng độ dài của chuỗi cộng một. Ví dụ::

      >>> 'spam, spam, spam'.count('spam')
      3
      >>> 'spam, spam, spam'.count('spam', 5)
      2
      >>> 'spam, spam, spam'.count('spam', 5, 10)
      1
      >>> 'spam, spam, spam'.count('eggs')
      0
      >>> 'spam, spam, spam'.count('')
      17

.. method:: str.encode(encoding="utf-8", errors="strict")

   Trả về chuỗi được mã hóa thành :class:`bytes`.

   *encoding* mặc định là ``'utf-8'``; xem :ref:`standard-encodings` để biết các giá trị có thể dùng.

   *errors* kiểm soát cách xử lý các lỗi mã hóa. Nếu là ``'strict'`` (mặc định), một ngoại lệ :exc:`UnicodeError` sẽ được phát sinh. Các giá trị khả dĩ khác là ``'ignore'``, ``'replace'``, ``'xmlcharrefreplace'``, ``'backslashreplace'`` và mọi tên khác được đăng ký thông qua :func:`codecs.register_error`. Xem :ref:`error-handlers` để biết chi tiết.

   Vì lý do hiệu năng, giá trị của *errors* không được kiểm tra tính hợp lệ trừ khi thực sự xảy ra lỗi encoding,
   :ref:`devmode` được bật hoặc một :ref:`bản dựng debug <debug-build>` được sử dụng. Ví dụ::

      >>> encoded_str_to_bytes = 'Python'.encode()
      >>> type(encoded_str_to_bytes)
      <class 'bytes'>
      >>> encoded_str_to_bytes
      b'Python'


   .. versionchanged:: 3.1
      Đã bổ sung hỗ trợ cho các đối số từ khóa.

   .. versionchanged:: 3.9
      Giá trị của đối số *errors* hiện được kiểm tra trong :ref:`devmode` và trong :ref:`chế độ debug <debug-build>`.


.. method:: str.endswith(suffix[, start[, end]])

   Trả về ``True`` nếu chuỗi kết thúc bằng *hậu tố* được chỉ định, nếu không thì trả về ``False``. *hậu tố* cũng có thể là một tuple gồm các hậu tố cần tìm. Với *vị trí bắt đầu* tùy chọn, việc kiểm tra bắt đầu tại vị trí đó. Với *vị trí kết thúc* tùy chọn, việc so sánh dừng tại vị trí đó. Việc sử dụng *vị trí bắt đầu* và *vị trí kết thúc* tương đương với ``str[start:end].endswith(suffix)``. Ví dụ::

      >>> 'Python'.endswith('on')
      True
      >>> 'a tuple of suffixes'.endswith(('at', 'in'))
      False
      >>> 'a tuple of suffixes'.endswith(('at', 'es'))
      True
      >>> 'Python is amazing'.endswith('is', 0, 9)
      True

   Xem thêm :meth:`startswith` và :meth:`removesuffix`.


.. method:: str.expandtabs(tabsize=8)

   Trả về một bản sao của chuỗi, trong đó tất cả ký tự tab được thay thế bằng một hoặc nhiều dấu cách, tùy thuộc vào cột hiện tại và kích thước tab đã cho. Các vị trí tab xuất hiện sau mỗi *tabsize* ký tự (mặc định là 8, tạo các vị trí tab tại cột 0, 8, 16, v.v.). Để mở rộng chuỗi, cột hiện tại được đặt về 0 và chuỗi được kiểm tra lần lượt từng ký tự. Nếu ký tự là tab (``\t``), một hoặc nhiều dấu cách được chèn vào kết quả cho đến khi cột hiện tại bằng vị trí tab tiếp theo. (Bản thân ký tự tab không được sao chép.) Nếu ký tự là ký tự xuống dòng (``\n``) hoặc ký tự xuống dòng về đầu dòng (``\r``), ký tự đó được sao chép và cột hiện tại được đặt lại về 0. Mọi ký tự khác đều được sao chép không thay đổi và cột hiện tại được tăng thêm một, bất kể ký tự đó được biểu diễn như thế nào khi in ra. Ví dụ::

      >>> '01\t012\t0123\t01234'.expandtabs()
      '01      012     0123    01234'
      >>> '01\t012\t0123\t01234'.expandtabs(4)
      '01  012 0123    01234'
      >>> print('01\t012\n0123\t01234'.expandtabs(4))
      01  012
      0123    01234


.. method:: str.find(sub[, start[, end]])

   Trả về chỉ mục nhỏ nhất trong chuỗi tại đó chuỗi con *sub* được tìm thấy trong lát cắt ``s[start:end]``. Các đối số tùy chọn *start* và *end* được diễn giải như trong ký hiệu lát cắt. Trả về ``-1`` nếu không tìm thấy *sub*. Ví dụ::

      >>> 'spam, spam, spam'.find('sp')
      0
      >>> 'spam, spam, spam'.find('sp', 5)
      6

   Xem thêm :meth:`rfind` và :meth:`index`.

   .. note::

      Chỉ nên sử dụng phương thức :meth:`~str.find` nếu bạn cần biết vị trí của *sub*. Để kiểm tra xem *sub* có phải là chuỗi con hay không, hãy sử dụng
      toán tử :keyword:`in`::

         >>> 'Py' in 'Python'
         True


.. method:: str.format(*args, **kwargs)

   Thực hiện thao tác định dạng chuỗi. Chuỗi mà phương thức này được gọi trên đó có thể chứa văn bản cố định hoặc các trường thay thế được phân cách bằng dấu ngoặc nhọn ``{}``. Mỗi trường thay thế chứa chỉ mục số của một đối số vị trí hoặc tên của một đối số từ khóa. Trả về một bản sao của chuỗi, trong đó mỗi trường thay thế được thay thế bằng giá trị chuỗi của đối số tương ứng. Ví dụ:

   .. doctest::

      >>> "The sum of 1 + 2 is {0}".format(1+2)
      'The sum of 1 + 2 is 3'
      >>> "The sum of {a} + {b} is {answer}".format(answer=1+2, a=1, b=2)
      'The sum of 1 + 2 is 3'
      >>> "{1} expects the {0} Inquisition!".format("Spanish", "Nobody")
      'Nobody expects the Spanish Inquisition!'

   Xem :ref:`formatstrings` để biết mô tả về các tùy chọn định dạng khác nhau có thể được chỉ định trong các chuỗi định dạng.

   .. note::
      Khi định dạng một số (:class:`int`, :class:`float`, :class:`complex`,
      :class:`decimal.Decimal` và các lớp con) với kiểu ``n`` (ví dụ: ``'{:n}'.format(1234)``), hàm tạm thời đặt locale ``LC_CTYPE`` thành locale ``LC_NUMERIC`` để giải mã các trường ``decimal_point`` và ``thousands_sep`` của :c:func:`localeconv` nếu chúng chứa ký tự không phải ASCII hoặc dài hơn 1 byte, và locale ``LC_NUMERIC`` khác locale ``LC_CTYPE``. Thay đổi tạm thời này ảnh hưởng đến các thread khác.

   .. versionchanged:: 3.7
      Khi định dạng một số bằng kiểu ``n``, trong một số trường hợp, hàm tạm thời đặt locale ``LC_CTYPE`` thành locale ``LC_NUMERIC``.


.. method:: str.format_map(mapping, /)

   Tương tự ``str.format(**mapping)``, ngoại trừ việc ``mapping`` được sử dụng trực tiếp thay vì được sao chép vào một :class:`dict`. Điều này hữu ích nếu, chẳng hạn, ``mapping`` là một lớp con của dict:

   >>> class Default(dict):
   ...     def __missing__(self, key):
   ...         return key
   ...
   >>> '{name} was born in {country}'.format_map(Default(name='Guido'))
   'Guido was born in country'

   .. versionadded:: 3.2


.. method:: str.index(sub[, start[, end]])

   Giống như :meth:`~str.find`, nhưng raise :exc:`ValueError` khi không tìm thấy chuỗi con. Ví dụ:

   .. doctest::

      >>> 'spam, spam, spam'.index('spam')
      0
      >>> 'spam, spam, spam'.index('eggs')
      Traceback (most recent call last):
        File "<python-input-0>", line 1, in <module>
          'spam, spam, spam'.index('eggs')
          ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^
      ValueError: substring not found

   Xem thêm :meth:`rindex`.


.. method:: str.isalnum()

   Trả về ``True`` nếu tất cả ký tự trong chuỗi đều là chữ và số và có ít nhất một ký tự, nếu không thì trả về ``False``. Một ký tự ``c`` là chữ và số nếu một trong các hàm sau trả về ``True``: ``c.isalpha()``, ``c.isdecimal()``, ``c.isdigit()`` hoặc ``c.isnumeric()``. Ví dụ:

   .. doctest::

      >>> 'abc123'.isalnum()
      True
      >>> 'abc123!@#'.isalnum()
      False
      >>> ''.isalnum()
      False
      >>> ' '.isalnum()
      False


.. method:: str.isalpha()

   Trả về ``True`` nếu tất cả ký tự trong chuỗi đều là chữ cái và có ít nhất một ký tự, nếu không thì trả về ``False``. Ký tự chữ cái là những ký tự được định nghĩa trong cơ sở dữ liệu ký tự Unicode là "Letter", tức là những ký tự có thuộc tính phân loại chung là một trong các giá trị "Lm", "Lt", "Lu", "Ll" hoặc "Lo". Lưu ý rằng điều này khác với thuộc tính `Alphabetic được định nghĩa trong mục 4.10 'Letters, Alphabetic, and Ideographic' của Tiêu chuẩn Unicode <https://www.unicode.org/versions/Unicode16.0.0/core-spec/chapter-4/#G91002>`_. Ví dụ:

   .. doctest::

      >>> 'Letters and spaces'.isalpha()
      False
      >>> 'LettersOnly'.isalpha()
      True
      >>> 'µ'.isalpha()  # các ký tự không phải ASCII cũng có thể được xem là thuộc bảng chữ cái
      True

   Xem :ref:`unicode-properties`.


.. method:: str.isascii()

   Trả về ``True`` nếu chuỗi trống hoặc tất cả các ký tự trong chuỗi đều là ASCII, nếu không thì trả về ``False``. Các ký tự ASCII có các code point trong phạm vi U+0000-U+007F. Ví dụ:

   .. doctest::

      >>> 'ASCII characters'.isascii()
      True
      >>> 'µ'.isascii()
      False

   .. versionadded:: 3.7


.. method:: str.isdecimal()

   Trả về ``True`` nếu tất cả các ký tự trong chuỗi đều là ký tự thập phân và có ít nhất một ký tự, nếu không thì trả về ``False``. Ký tự thập phân là những ký tự có thể được dùng để tạo thành các số trong hệ cơ số 10, chẳng hạn như U+0660, CHỮ SỐ 0 Ả RẬP-ẤN. Về mặt hình thức, ký tự thập phân là ký tự thuộc Unicode General Category "Nd". Ví dụ:

   .. doctest::

      >>> '0123456789'.isdecimal()
      True
      >>> '٠١٢٣٤٥٦٧٨٩'.isdecimal()  # các chữ số Ả Rập-Ấn từ 0 đến 9
      True
      >>> 'alphabetic'.isdecimal()
      False


.. method:: str.isdigit()

   Trả về ``True`` nếu tất cả các ký tự trong chuỗi đều là chữ số và có ít nhất một ký tự, nếu không thì trả về ``False``. Chữ số bao gồm các ký tự thập phân và những chữ số cần được xử lý đặc biệt, chẳng hạn như các chữ số mũ tương thích. Điều này bao gồm những chữ số không thể được dùng để tạo thành các số trong hệ cơ số 10, chẳng hạn như `các số Kharosthi <https://en.wikipedia.org/wiki/Kharosthi#Numerals>`__. Về mặt hình thức, chữ số là ký tự có giá trị thuộc tính Numeric_Type=Digit hoặc Numeric_Type=Decimal.

   Ví dụ:

   .. doctest::

      >>> '0123456789'.isdigit()
      True
      >>> '٠١٢٣٤٥٦٧٨٩'.isdigit()  # các chữ số Ả Rập-Ấn từ 0 đến 9
      True
      >>> '⅕'.isdigit()  # Phân số thường một phần năm
      False
      >>> '²'.isdecimal(), '²'.isdigit(),  '²'.isnumeric()
      (False, True, True)

   Xem thêm :meth:`isdecimal` và :meth:`isnumeric`.


.. method:: str.isidentifier()

   Trả về ``True`` nếu chuỗi là một định danh hợp lệ theo định nghĩa ngôn ngữ, mục :ref:`identifiers`.

   :func:`keyword.iskeyword` có thể được dùng để kiểm tra xem chuỗi ``s`` có phải là một định danh dành riêng hay không, chẳng hạn như :keyword:`def` và :keyword:`class`.

   Ví dụ:
   ::::::

      >>> from keyword import iskeyword

      >>> 'hello'.isidentifier(), iskeyword('hello')
      (True, False)
      >>> 'def'.isidentifier(), iskeyword('def')
      (True, True)


.. method:: str.islower()

   Trả về ``True`` nếu tất cả các ký tự có phân biệt hoa thường [4]_ trong chuỗi đều là chữ thường và có ít nhất một ký tự có phân biệt hoa thường, ``False`` nếu không.


.. method:: str.isnumeric()

   Trả về ``True`` nếu tất cả các ký tự trong chuỗi đều là ký tự số và chuỗi có ít nhất một ký tự, nếu không thì trả về ``False``. Ký tự số bao gồm các chữ số và tất cả các ký tự có thuộc tính giá trị số Unicode, ví dụ U+2155, PHÂN SỐ THÔNG THƯỜNG MỘT PHẦN NĂM. Về mặt hình thức, ký tự số là những ký tự có giá trị thuộc tính Numeric_Type=Digit, Numeric_Type=Decimal hoặc Numeric_Type=Numeric. Ví dụ:

   .. doctest::

      >>> '0123456789'.isnumeric()
      True
      >>> '٠١٢٣٤٥٦٧٨٩'.isnumeric()  # Chữ số Ả Rập-Ấn Độ từ 0 đến 9
      True
      >>> '⅕'.isnumeric()  # Phân số thông thường một phần năm
      True
      >>> '²'.isdecimal(), '²'.isdigit(),  '²'.isnumeric()
      (False, True, True)

   Xem thêm :meth:`isdecimal` và :meth:`isdigit`.


.. method:: str.isprintable()

   Trả về ``True`` nếu tất cả các ký tự trong chuỗi đều có thể in được, ``False`` nếu chuỗi chứa ít nhất một ký tự không thể in được.

   Ở đây, "có thể in được" nghĩa là ký tự đó phù hợp để :func:`repr` sử dụng trong đầu ra của nó; "không thể in được" nghĩa là :func:`repr` trên các kiểu dựng sẵn sẽ thoát ký tự bằng mã thập lục phân. Điều này không ảnh hưởng đến cách xử lý các chuỗi được ghi vào :data:`sys.stdout` hoặc :data:`sys.stderr`.

   Các ký tự có thể in được là những ký tự trong cơ sở dữ liệu ký tự Unicode (xem :mod:`unicodedata`) có danh mục tổng quát thuộc nhóm Letter, Mark, Number, Punctuation hoặc Symbol (L, M, N, P hoặc S); cộng thêm ký tự khoảng trắng ASCII 0x20. Các ký tự không thể in được là những ký tự thuộc nhóm Separator hoặc Other (Z hoặc C), ngoại trừ ký tự khoảng trắng ASCII.

   Ví dụ:

   .. doctest::

      >>> ''.isprintable(), ' '.isprintable()
      (True, True)
      >>> '\t'.isprintable(), '\n'.isprintable()
      (False, False)

   Xem thêm :meth:`isspace`.


.. method:: str.isspace()

   Trả về ``True`` nếu chuỗi chỉ chứa các ký tự khoảng trắng và có ít nhất một ký tự, ngược lại trả về ``False``.

   Ví dụ:

   .. doctest::

      >>> ''.isspace()
      False
      >>> ' '.isspace()
      True
      >>> '\t\n'.isspace() # TAB và BREAK LINE
      True
      >>> '\u3000'.isspace() # IDEOGRAPHIC SPACE
      True

   Một ký tự là *whitespace* nếu trong cơ sở dữ liệu ký tự Unicode (xem :mod:`unicodedata`), hoặc category tổng quát của nó là ``Zs`` ("Separator, space"), hoặc lớp hai chiều của nó là một trong ``WS``, ``B`` hoặc ``S``.

   Xem thêm :meth:`isprintable`.


.. method:: str.istitle()

   Trả về ``True`` nếu chuỗi là chuỗi viết hoa chữ cái đầu và có ít nhất một ký tự; ví dụ: các ký tự viết hoa chỉ có thể đứng sau các ký tự không có dạng hoa thường, còn các ký tự viết thường chỉ có thể đứng sau các ký tự có dạng hoa thường. Trả về ``False`` nếu không.

   Ví dụ:

   .. doctest::

      >>> 'Spam, Spam, Spam'.istitle()
      True
      >>> 'spam, spam, spam'.istitle()
      False
      >>> 'SPAM, SPAM, SPAM'.istitle()
      False

   Xem thêm :meth:`title`.


.. method:: str.isupper()

   Trả về ``True`` nếu tất cả các ký tự có dạng hoa thường [4]_ trong chuỗi đều là chữ hoa và có ít nhất một ký tự có dạng hoa thường; nếu không, trả về ``False``.

      >>> 'BANANA'.isupper()
      True
      >>> 'banana'.isupper()
      False
      >>> 'baNana'.isupper()
      False
      >>> ' '.isupper()
      False



.. _meth-str-join:

.. method:: str.join(iterable, /)

   Trả về một chuỗi là kết quả nối các chuỗi trong *iterable*. Một :exc:`TypeError` sẽ được phát sinh nếu có bất kỳ giá trị không phải chuỗi nào trong *iterable*, bao gồm cả các đối tượng :class:`bytes`. Chuỗi cung cấp phương thức này sẽ là dấu phân cách giữa các phần tử. Ví dụ:

   .. doctest::

      >>> ', '.join(['spam', 'spam', 'spam'])
      'spam, spam, spam'
      >>> '-'.join('Python')
      'P-y-t-h-o-n'

   Xem thêm :meth:`split`.


.. method:: str.ljust(width, fillchar=' ', /)

   Trả về chuỗi được căn trái trong một chuỗi có độ dài *width*. Việc đệm được thực hiện bằng *fillchar* đã chỉ định (mặc định là một khoảng trắng ASCII). Chuỗi ban đầu được trả về nếu *width* nhỏ hơn hoặc bằng ``len(s)``.

   Ví dụ:

   .. doctest::

      >>> 'Python'.ljust(10)
      'Python    '
      >>> 'Python'.ljust(10, '.')
      'Python....'
      >>> 'Monty Python'.ljust(10, '.')
      'Monty Python'

   Xem thêm :meth:`rjust`.


.. method:: str.lower()

   Trả về một bản sao của chuỗi, trong đó tất cả các ký tự có phân biệt hoa thường [4]_ được chuyển thành chữ thường. Ví dụ:

   .. doctest::

      >>> 'Lower Method Example'.lower()
      'lower method example'

   Thuật toán chuyển thành chữ thường được sử dụng được `mô tả trong mục 3.13 'Default Case Folding' của Unicode Standard <https://www.unicode.org/versions/Unicode16.0.0/core-spec/chapter-3/#G33992>`__.


.. method:: str.lstrip(chars=None, /)

   Trả về một bản sao của chuỗi sau khi loại bỏ các ký tự ở đầu. Đối số *chars* là một chuỗi chỉ định tập hợp các ký tự cần loại bỏ. Nếu bị bỏ qua hoặc là ``None``, đối số *chars* mặc định sẽ loại bỏ khoảng trắng. Đối số *chars* không phải là tiền tố; thay vào đó, mọi tổ hợp của các giá trị trong đó đều bị loại bỏ::

      >>> '   spacious   '.lstrip()
      'spacious   '
      >>> 'www.example.com'.lstrip('cmowz.')
      'example.com'

   Xem :meth:`str.removeprefix` để biết phương thức loại bỏ một chuỗi tiền tố duy nhất thay vì toàn bộ một tập hợp ký tự. Ví dụ::

      >>> 'Arthur: three!'.lstrip('Arthur: ')
      'ee!'
      >>> 'Arthur: three!'.removeprefix('Arthur: ')
      'three!'


.. staticmethod:: str.maketrans(dict, /)
                  str.maketrans(from, to, remove='', /)

   Phương thức tĩnh này trả về một bảng chuyển đổi có thể dùng cho :meth:`str.translate`.

   Nếu chỉ có một đối số, đối số đó phải là một từ điển ánh xạ các ordinal Unicode (số nguyên) hoặc ký tự (chuỗi có độ dài 1) tới các ordinal Unicode, chuỗi (có độ dài tùy ý) hoặc ``None``. Sau đó, các khóa ký tự sẽ được chuyển đổi thành ordinal.

   Nếu có hai đối số, chúng phải là các chuỗi có độ dài bằng nhau; trong từ điển kết quả, mỗi ký tự trong *from* sẽ được ánh xạ tới ký tự ở cùng vị trí trong *to*. Nếu có đối số thứ ba, đối số đó phải là một chuỗi; các ký tự của chuỗi sẽ được ánh xạ tới ``None`` trong kết quả.


.. method:: str.partition(sep, /)

   Tách chuỗi tại lần xuất hiện đầu tiên của *sep* và trả về một bộ 3 phần tử gồm phần trước dấu phân cách, chính dấu phân cách và phần sau dấu phân cách. Nếu không tìm thấy dấu phân cách, trả về một bộ 3 phần tử gồm chính chuỗi đó, tiếp theo là hai chuỗi rỗng.

   Ví dụ:

   .. doctest::

      >>> 'Monty Python'.partition(' ')
      ('Monty', ' ', 'Python')
      >>> "Monty Python's Flying Circus".partition(' ')
      ('Monty', ' ', "Python's Flying Circus")
      >>> 'Monty Python'.partition('-')
      ('Monty Python', '', '')

   Xem thêm :meth:`rpartition`.


.. method:: str.removeprefix(prefix, /)

   Nếu chuỗi bắt đầu bằng chuỗi *prefix*, hãy trả về ``string[len(prefix):]``. Nếu không, hãy trả về một bản sao của chuỗi ban đầu:

   .. doctest::

      >>> 'TestHook'.removeprefix('Test')
      'Hook'
      >>> 'BaseTestCase'.removeprefix('Test')
      'BaseTestCase'

   .. versionadded:: 3.9

   Xem thêm :meth:`removesuffix` và :meth:`startswith`.


.. method:: str.removesuffix(suffix, /)

   Nếu chuỗi kết thúc bằng chuỗi *suffix* và *suffix* đó không rỗng, hãy trả về ``string[:-len(suffix)]``. Nếu không, hãy trả về một bản sao của chuỗi ban đầu:

   .. doctest::

      >>> 'MiscTests'.removesuffix('Tests')
      'Misc'
      >>> 'TmpDirMixin'.removesuffix('Tests')
      'TmpDirMixin'

   .. versionadded:: 3.9

   Xem thêm :meth:`removeprefix` và :meth:`endswith`.


.. method:: str.replace(old, new, /, count=-1)

   Trả về một bản sao của chuỗi, trong đó mọi lần xuất hiện của chuỗi con *old* được thay thế bằng *new*. Nếu *count* được cung cấp, chỉ những lần xuất hiện đầu tiên của *count* được thay thế. Nếu *count* không được chỉ định hoặc là ``-1``, thì mọi lần xuất hiện đều được thay thế. Ví dụ:

   .. doctest::

      >>> 'spam, spam, spam'.replace('spam', 'eggs')
      'eggs, eggs, eggs'
      >>> 'spam, spam, spam'.replace('spam', 'eggs', 1)
      'eggs, spam, spam'

   .. versionchanged:: 3.13
      *count* hiện được hỗ trợ dưới dạng đối số từ khóa.


.. method:: str.rfind(sub[, start[, end]])

   Trả về chỉ mục lớn nhất trong chuỗi tại đó tìm thấy chuỗi con *sub*, sao cho *sub* nằm trong ``s[start:end]``. Các đối số tùy chọn *start* và *end* được diễn giải như trong ký hiệu lát cắt. Trả về ``-1`` nếu không tìm thấy. Ví dụ:

   .. doctest::

      >>> 'spam, spam, spam'.rfind('sp')
      12
      >>> 'spam, spam, spam'.rfind('sp', 0, 10)
      6

   Xem thêm :meth:`find` và :meth:`rindex`.


.. method:: str.rindex(sub[, start[, end]])

   Tương tự như :meth:`rfind` nhưng sẽ phát sinh :exc:`ValueError` khi không tìm thấy chuỗi con *sub*. Ví dụ:

   .. doctest::

      >>> 'spam, spam, spam'.rindex('spam')
      12
      >>> 'spam, spam, spam'.rindex('eggs')
      Traceback (most recent call last):
        File "<stdin-0>", line 1, in <module>
          'spam, spam, spam'.rindex('eggs')
          ~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^
      ValueError: substring not found

   Xem thêm :meth:`index` và :meth:`find`.


.. method:: str.rjust(width, fillchar=' ', /)

   Trả về chuỗi được căn phải trong một chuỗi có độ dài *width*. Việc đệm được thực hiện bằng *fillchar* đã chỉ định (mặc định là một khoảng trắng ASCII). Chuỗi ban đầu được trả về nếu *width* nhỏ hơn hoặc bằng ``len(s)``.

   Ví dụ:

   .. doctest::

      >>> 'Python'.rjust(10)
      '    Python'
      >>> 'Python'.rjust(10, '.')
      '....Python'
      >>> 'Monty Python'.rjust(10, '.')
      'Monty Python'

   Xem thêm :meth:`ljust` và :meth:`zfill`.


.. method:: str.rpartition(sep, /)

   Tách chuỗi tại lần xuất hiện cuối cùng của *sep* và trả về một bộ 3 phần tử gồm phần trước dấu phân cách, chính dấu phân cách và phần sau dấu phân cách. Nếu không tìm thấy dấu phân cách, trả về một bộ 3 phần tử gồm hai chuỗi rỗng, theo sau là chính chuỗi đó.

   Ví dụ:

   .. doctest::

      >>> 'Monty Python'.rpartition(' ')
      ('Monty', ' ', 'Python')
      >>> "Monty Python's Flying Circus".rpartition(' ')
      ("Monty Python's Flying", ' ', 'Circus')
      >>> 'Monty Python'.rpartition('-')
      ('', '', 'Monty Python')

   Xem thêm :meth:`partition`.


.. method:: str.rsplit(sep=None, maxsplit=-1)

   Trả về danh sách các từ trong chuỗi, sử dụng *sep* làm chuỗi phân cách. Nếu *maxsplit* được cung cấp, sẽ thực hiện nhiều nhất *maxsplit* lần tách, cụ thể là các lần tách *rightmost*. Nếu *sep* không được chỉ định hoặc là ``None``, bất kỳ
   :meth:`whitespace <str.isspace>` chuỗi nào cũng là dấu phân cách. Ngoại trừ việc tách từ bên phải, :meth:`rsplit` hoạt động như
   :meth:`split` được mô tả chi tiết bên dưới.


.. method:: str.rstrip(chars=None, /)

   Trả về một bản sao của chuỗi sau khi loại bỏ các ký tự ở cuối. Đối số *chars* là một chuỗi chỉ định tập hợp các ký tự cần loại bỏ. Nếu bị bỏ qua hoặc là ``None``, đối số *chars* mặc định sẽ loại bỏ khoảng trắng. Đối số *chars* không phải là một hậu tố; thay vào đó, mọi tổ hợp các giá trị của nó đều bị loại bỏ. Ví dụ:

   .. doctest::

      >>> '   spacious   '.rstrip()
      '   spacious'
      >>> 'mississippi'.rstrip('ipz')
      'mississ'

   Xem :meth:`removesuffix` để biết một phương thức loại bỏ một chuỗi hậu tố đơn lẻ thay vì toàn bộ một tập hợp ký tự. Ví dụ::

      >>> 'Monty Python'.rstrip(' Python')
      'M'
      >>> 'Monty Python'.removesuffix(' Python')
      'Monty'

   Xem thêm :meth:`strip`.


.. method:: str.split(sep=None, maxsplit=-1)

   Trả về danh sách các từ trong chuỗi, sử dụng *sep* làm chuỗi phân cách.  Nếu *maxsplit* được cung cấp, nhiều nhất *maxsplit* lần tách sẽ được thực hiện (do đó, danh sách sẽ có nhiều nhất ``maxsplit+1`` phần tử).  Nếu *maxsplit* không được chỉ định hoặc là ``-1``, thì không giới hạn số lần tách (tất cả các lần tách có thể thực hiện đều được thực hiện).

   Nếu *sep* được cung cấp, các dấu phân cách liên tiếp không được nhóm lại với nhau và được xem là phân cách các chuỗi rỗng (ví dụ: ``'1,,2'.split(',')`` trả về ``['1', '', '2']``).  Đối số *sep* có thể gồm nhiều ký tự được xem như một dấu phân cách duy nhất (để tách bằng nhiều dấu phân cách, hãy sử dụng
   :func:`re.split`). Việc tách một chuỗi rỗng bằng dấu phân cách được chỉ định sẽ trả về ``['']``.

   Ví dụ:

   .. doctest::

      >>> '1,2,3'.split(',')
      ['1', '2', '3']
      >>> '1,2,3'.split(',', maxsplit=1)
      ['1', '2,3']
      >>> '1,2,,3,'.split(',')
      ['1', '2', '', '3', '']
      >>> '1<>2<>3<4'.split('<>')
      ['1', '2', '3<4']

   Nếu *sep* không được chỉ định hoặc là ``None``, một thuật toán tách khác sẽ được áp dụng: các chuỗi liên tiếp gồm :meth:`whitespace <str.isspace>` được xem là một dấu phân cách duy nhất và kết quả sẽ không chứa chuỗi rỗng ở đầu hoặc cuối nếu chuỗi có khoảng trắng ở đầu hoặc cuối.  Do đó, việc tách một chuỗi rỗng hoặc một chuỗi chỉ gồm khoảng trắng bằng dấu phân cách ``None`` sẽ trả về ``[]``.

   Ví dụ:

   .. doctest::

      >>> '1 2 3'.split()
      ['1', '2', '3']
      >>> '1 2 3'.split(maxsplit=1)
      ['1', '2 3']
      >>> '   1   2   3   '.split()
      ['1', '2', '3']

   Nếu *sep* không được chỉ định hoặc là ``None`` và *maxsplit* là ``0``, thì chỉ các chuỗi khoảng trắng liên tiếp ở đầu mới được xem xét.

   Ví dụ:

   .. doctest::

      >>> "".split(None, 0)
      []
      >>> "   ".split(None, 0)
      []
      >>> "   foo   ".split(maxsplit=0)
      ['foo   ']

   Xem thêm :meth:`join` và :meth:`rsplit`.


.. index::
   single: universal newlines; str.splitlines method

.. method:: str.splitlines(keepends=False)

   Trả về danh sách các dòng trong chuỗi, ngắt tại các ranh giới dòng. Các ký tự ngắt dòng không được đưa vào danh sách kết quả, trừ khi *keepends* được cung cấp và có giá trị true.

   Phương thức này ngắt tại các ranh giới dòng sau đây. Cụ thể, các ranh giới này là một tập siêu của :term:`universal newlines`.

   +----------------------+--------------------------------------+
   | Biểu diễn            | Mô tả                                |
   +======================+======================================+
   | ``\n``               | Ký tự xuống dòng                     |
   +----------------------+--------------------------------------+
   | ``\r``               | Ký tự về đầu dòng                    |
   +----------------------+--------------------------------------+
   | ``\r\n``             | Ký tự về đầu dòng + ký tự xuống dòng |
   +----------------------+--------------------------------------+
   | ``\v`` hoặc ``\x0b`` | Ký tự tab dòng                       |
   +----------------------+--------------------------------------+
   | ``\f`` hoặc ``\x0c`` | Ký tự ngắt trang                     |
   +----------------------+--------------------------------------+
   | ``\x1c``             | Dấu phân tách tệp                    |
   +----------------------+--------------------------------------+
   | ``\x1d``             | Dấu phân tách nhóm                   |
   +----------------------+--------------------------------------+
   | ``\x1e``             | Dấu phân tách bản ghi                |
   +----------------------+--------------------------------------+
   | ``\x85``             | Dòng tiếp theo (Mã điều khiển C1)    |
   +----------------------+--------------------------------------+
   | ``\u2028``           | Dấu phân tách dòng                   |
   +----------------------+--------------------------------------+
   | ``\u2029``           | Dấu phân tách đoạn văn               |
   +----------------------+--------------------------------------+

   .. versionchanged:: 3.2

      ``\v`` và ``\f`` được thêm vào danh sách các ranh giới dòng.

   Ví dụ::

      >>> 'ab c\n\nde fg\rkl\r\n'.splitlines()
      ['ab c', '', 'de fg', 'kl']
      >>> 'ab c\n\nde fg\rkl\r\n'.splitlines(keepends=True)
      ['ab c\n', '\n', 'de fg\r', 'kl\r\n']

   Không giống :meth:`~str.split` khi cung cấp chuỗi phân cách *sep*, phương thức này trả về một danh sách rỗng đối với chuỗi rỗng, và dấu ngắt dòng ở cuối không tạo ra một dòng bổ sung::

      >>> "".splitlines()
      []
      >>> "One line\n".splitlines()
      ['One line']

   Để so sánh, ``split('\n')`` cho kết quả::

      >>> ''.split('\n')
      ['']
      >>> 'Two lines\n'.split('\n')
      ['Two lines', '']


.. method:: str.startswith(prefix[, start[, end]])

   Trả về ``True`` nếu chuỗi bắt đầu bằng *prefix*, nếu không thì trả về ``False``. *prefix* cũng có thể là một tuple gồm các tiền tố cần tìm. Với *start* tùy chọn, kiểm tra chuỗi bắt đầu tại vị trí đó. Với *end* tùy chọn, dừng so sánh chuỗi tại vị trí đó.

   Ví dụ:

   .. doctest::

      >>> 'Python'.startswith('Py')
      True
      >>> 'a tuple of prefixes'.startswith(('at', 'a'))
      True
      >>> 'Python is amazing'.startswith('is', 7)
      True

   Xem thêm :meth:`endswith` và :meth:`removeprefix`.


.. method:: str.strip(chars=None, /)

   Trả về một bản sao của chuỗi sau khi loại bỏ các ký tự ở đầu và cuối. Đối số *chars* là một chuỗi chỉ định tập hợp các ký tự cần loại bỏ. Nếu bị bỏ qua hoặc là ``None``, đối số *chars* mặc định sẽ loại bỏ khoảng trắng. Đối số *chars* không phải là tiền tố hay hậu tố; thay vào đó, tất cả các tổ hợp của các giá trị trong đó đều bị loại bỏ.

   Các ký tự khoảng trắng được định nghĩa bởi :meth:`str.isspace`.

   Ví dụ:

   .. doctest::

      >>> '   spacious   '.strip()
      'spacious'
      >>> 'www.example.com'.strip('cmowz.')
      'example'

   Các giá trị đối số *chars* ở đầu và cuối cùng của chuỗi sẽ bị loại bỏ. Các ký tự được xóa từ đầu chuỗi cho đến khi gặp một ký tự chuỗi không nằm trong tập hợp các ký tự trong *chars*. Thao tác tương tự cũng diễn ra ở cuối chuỗi.

   Ví dụ:

   .. doctest::

      >>> comment_string = '#....... Section 3.2.1 Issue #32 .......'
      >>> comment_string.strip('.#! ')
      'Section 3.2.1 Issue #32'

   Xem thêm :meth:`rstrip`.


.. method:: str.swapcase()

   Trả về một bản sao của chuỗi, trong đó các ký tự viết hoa được chuyển thành chữ thường và ngược lại. Ví dụ:

   .. doctest::

      >>> 'Hello World'.swapcase()
      'hELLO wORLD'

   Lưu ý rằng không nhất thiết ``s.swapcase().swapcase() == s``. Ví dụ:

   .. doctest::

      >>> 'straße'.swapcase().swapcase()
      'strasse'

   Xem thêm :meth:`str.lower` và :meth:`str.upper`.


.. method:: str.title()

   Trả về phiên bản viết hoa kiểu tiêu đề của chuỗi, trong đó các từ bắt đầu bằng một ký tự viết hoa và các ký tự còn lại được viết thường.

   Ví dụ::

      >>> 'Hello world'.title()
      'Hello World'

   Thuật toán sử dụng một định nghĩa đơn giản, không phụ thuộc vào ngôn ngữ, về một từ là một nhóm các chữ cái liên tiếp. Định nghĩa này hoạt động trong nhiều ngữ cảnh, nhưng có nghĩa là dấu nháy đơn trong các dạng viết tắt và sở hữu tạo thành ranh giới từ, và đây có thể không phải là kết quả mong muốn::

        >>> "they're bill's friends from the UK".title()
        "They'Re Bill'S Friends From The Uk"

   Hàm :func:`string.capwords` không gặp vấn đề này vì nó chỉ tách các từ tại khoảng trắng.

   Ngoài ra, có thể xây dựng một giải pháp tạm thời cho dấu nháy đơn bằng cách sử dụng regular expression::

        >>> import re
        >>> def titlecase(s):
        ...     return re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
        ...                   lambda mo: mo.group(0).capitalize(),
        ...                   s)
        ...
        >>> titlecase("they're bill's friends.")
        "They're Bill's Friends."

   Xem thêm :meth:`istitle`.


.. method:: str.translate(table, /)

   Trả về một bản sao của chuỗi, trong đó mỗi ký tự đã được ánh xạ qua bảng dịch đã cho. Bảng này phải là một đối tượng triển khai việc lập chỉ mục thông qua :meth:`~object.__getitem__`, thường là một :term:`mapping` hoặc
   :term:`sequence`. Khi được lập chỉ mục bằng một ordinal Unicode (một số nguyên), đối tượng bảng có thể thực hiện một trong các thao tác sau: trả về một ordinal Unicode hoặc một chuỗi để ánh xạ ký tự thành một hoặc nhiều ký tự khác; trả về ``None`` để xóa ký tự khỏi chuỗi kết quả; hoặc phát sinh một
   ngoại lệ :exc:`LookupError` để giữ nguyên ký tự.

   Bạn có thể sử dụng :meth:`str.maketrans` để tạo một bản đồ dịch từ các ánh xạ ký tự-sang-ký tự ở nhiều định dạng khác nhau.

   Xem thêm module :mod:`codecs` để có cách tiếp cận linh hoạt hơn khi tùy chỉnh ánh xạ ký tự.


.. method:: str.upper()

   Trả về một bản sao của chuỗi, trong đó tất cả các ký tự có phân biệt hoa thường [4]_ được chuyển thành chữ hoa. Lưu ý rằng ``s.upper().isupper()`` có thể là ``False`` nếu ``s`` chứa các ký tự không có dạng hoa thường hoặc nếu danh mục Unicode của (các) ký tự kết quả không phải là "Lu" (Letter, uppercase) mà chẳng hạn là "Lt" (Letter, titlecase).

   Thuật toán viết hoa được sử dụng là `được mô tả trong mục 3.13 'Default Case Folding' của Unicode Standard <https://www.unicode.org/versions/Unicode16.0.0/core-spec/chapter-3/#G33992>`__.


.. method:: str.zfill(width, /)

   Trả về một bản sao của chuỗi, được điền bên trái bằng các chữ số ASCII ``'0'`` để tạo thành chuỗi có độ dài *width*. Tiền tố dấu đứng đầu (``'+'``/``'-'``) được xử lý bằng cách chèn phần đệm *after* dấu thay vì chèn trước dấu đó. Chuỗi ban đầu được trả về nếu *width* nhỏ hơn hoặc bằng ``len(s)``.

   Ví dụ:

   .. doctest::

      >>> "42".zfill(5)
      '00042'
      >>> "-42".zfill(5)
      '-0042'

   Xem thêm :meth:`rjust`.


.. index::
   single: ! formatted string literal
   single: formatted string literals
   single: ! f-string
   single: f-strings
   single: fstring
   single: interpolated string literal
   single: string; formatted literal
   single: string; interpolated literal
   single: {} (curly brackets); in formatted string literal
   single: ! (exclamation mark); in formatted string literal
   single: : (colon); in formatted string literal
   single: = (equals); for help in debugging using string literals

.. _stdtypes-fstrings:

Chuỗi ký tự được định dạng (f-strings)
--------------------------------------

.. versionadded:: 3.6
.. versionchanged:: 3.7
   Có thể sử dụng :keyword:`await` và :keyword:`async for` trong các biểu thức bên trong f-strings.
.. versionchanged:: 3.8
   Đã bổ sung bộ chỉ định debug (``=``)
.. versionchanged:: 3.12
   Nhiều hạn chế đối với các biểu thức bên trong f-strings đã được gỡ bỏ. Đáng chú ý là hiện đã cho phép chuỗi lồng nhau, chú thích và dấu gạch chéo ngược.

:dfn:`f-string` (chính thức là :dfn:`literal chuỗi được định dạng`) là một literal chuỗi được thêm tiền tố ``f`` hoặc ``F``. Loại literal chuỗi này cho phép nhúng kết quả của các biểu thức Python tùy ý vào *các trường thay thế*, được phân cách bằng dấu ngoặc nhọn (``{}``). Mỗi trường thay thế phải chứa một biểu thức, tùy chọn theo sau bởi:

* một *debug specifier* -- dấu bằng (``=``);
* một *conversion specifier* -- ``!s``, ``!r`` hoặc ``!a``; và/hoặc
* một *format specifier* có tiền tố là dấu hai chấm (``:``).

Xem :ref:`phần Lexical Analysis về f-string <f-strings>` để biết chi tiết về cú pháp của các trường này.

Debug specifier
^^^^^^^^^^^^^^^

.. versionadded:: 3.8

Nếu một debug specifier -- dấu bằng (``=``) -- xuất hiện sau biểu thức của trường thay thế, f-string kết quả sẽ chứa mã nguồn của biểu thức, dấu bằng và giá trị của biểu thức. Điều này thường hữu ích khi gỡ lỗi::

   >>> number = 14.3
   >>> f'{number=}'
   'number=14.3'

Khoảng trắng trước, bên trong và sau biểu thức, cũng như khoảng trắng sau dấu bằng, đều có ý nghĩa --- chúng được giữ lại trong kết quả::

   >>> f'{ number  -  4  = }'
   ' number  -  4  = 10.3'


Chỉ định chuyển đổi
^^^^^^^^^^^^^^^^^^^

Theo mặc định, giá trị của biểu thức trong trường thay thế được chuyển đổi thành chuỗi bằng cách sử dụng :func:`str`::

   >>> from fractions import Fraction
   >>> one_third = Fraction(1, 3)
   >>> f'{one_third}'
   '1/3'

Khi sử dụng chỉ định gỡ lỗi nhưng không có chỉ định định dạng, việc chuyển đổi mặc định sẽ sử dụng :func:`repr`::

   >>> f'{one_third = }'
   'one_third = Fraction(1, 3)'

Có thể chỉ định chuyển đổi một cách tường minh bằng một trong các chỉ định sau:

* ``!s`` cho :func:`str`
* ``!r`` cho :func:`repr`
* ``!a`` cho :func:`ascii`

Ví dụ::

   >>> str(one_third)
   '1/3'
   >>> repr(one_third)
   'Fraction(1, 3)'

   >>> f'{one_third!s} is {one_third!r}'
   '1/3 is Fraction(1, 3)'

   >>> string = "¡kočka 😸!"
   >>> ascii(string)
   "'\\xa1ko\\u010dka \\U0001f638!'"

   >>> f'{string = !a}'
   "string = '\\xa1ko\\u010dka \\U0001f638!'"


Bộ chỉ định định dạng
^^^^^^^^^^^^^^^^^^^^^

Sau khi biểu thức được đánh giá và có thể được chuyển đổi bằng bộ chỉ định chuyển đổi tường minh, biểu thức sẽ được định dạng bằng hàm :func:`format`. Nếu trường thay thế bao gồm *bộ chỉ định định dạng* được giới thiệu bằng dấu hai chấm (``:``), bộ chỉ định này sẽ được truyền cho :func:`!format` dưới dạng đối số thứ hai. Sau đó, kết quả của :func:`!format` được dùng làm giá trị cuối cùng cho trường thay thế. Ví dụ::

   >>> from fractions import Fraction
   >>> one_third = Fraction(1, 3)
   >>> f'{one_third:.6f}'
   '0.333333'
   >>> f'{one_third:_^+10}'
   '___+1/3___'
   >>> f'{one_third!r:_^20}'
   '___Fraction(1, 3)___'
   >>> f'{one_third = :~>10}~'
   'one_third = ~~~~~~~1/3~'

.. _stdtypes-tstrings:

Literal chuỗi template (t-string)
---------------------------------

:dfn:`t-string` (tên gọi chính thức là :dfn:`template string literal`) là một literal chuỗi có tiền tố ``t`` hoặc ``T``.

Các chuỗi này tuân theo cùng cú pháp và quy tắc đánh giá như
:ref:`các literal chuỗi được định dạng <stdtypes-fstrings>`, với những điểm khác biệt sau:

* Thay vì được đánh giá thành một object ``str``, các literal chuỗi mẫu được đánh giá thành một object :class:`string.templatelib.Template`.

* Giao thức :func:`format` không được sử dụng. Thay vào đó, trình định dạng và các phép chuyển đổi (nếu có) được truyền vào một object :class:`~string.templatelib.Interpolation` mới, được tạo cho mỗi biểu thức được đánh giá. Mã xử lý object :class:`~string.templatelib.Template` kết quả sẽ quyết định cách xử lý các trình định dạng và phép chuyển đổi.

* Các trình định dạng chứa những trường thay thế lồng nhau được đánh giá eager trước khi được truyền vào object :class:`~string.templatelib.Interpolation`. Ví dụ, phép nội suy có dạng ``{amount:.{precision}f}`` sẽ đánh giá biểu thức bên trong ``{precision}`` để xác định giá trị của thuộc tính ``format_spec``. Nếu ``precision`` là ``2``, trình định dạng kết quả sẽ là ``'.2f'``.

* Khi dấu bằng ``'='`` được cung cấp trong một biểu thức nội suy, văn bản của biểu thức sẽ được nối vào literal chuỗi đứng trước phép nội suy tương ứng. Điều này bao gồm cả dấu bằng và mọi khoảng trắng xung quanh. Instance :class:`!Interpolation` cho biểu thức sẽ được tạo như bình thường, ngoại trừ việc :attr:`~string.templatelib.Interpolation.conversion` theo mặc định sẽ được đặt thành '``r``' (:func:`repr`). Nếu cung cấp phép chuyển đổi hoặc trình định dạng rõ ràng, giá trị này sẽ ghi đè hành vi mặc định.


.. _old-string-formatting:

``printf``-kiểu Định dạng Chuỗi
-------------------------------

.. index::
   single: formatting, string (%)
   single: interpolation, string (%)
   single: string; formatting, printf
   single: string; interpolation, printf
   single: printf-style formatting
   single: sprintf-style formatting
   single: % (percent); printf-style formatting

.. note::

   Các thao tác định dạng được mô tả ở đây có nhiều đặc điểm bất thường, dẫn đến một số lỗi phổ biến (chẳng hạn như không hiển thị tuple và dictionary đúng cách).

   Việc sử dụng :ref:`formatted string literals <f-strings>`, giao diện :meth:`str.format` hoặc :class:`string.Template` có thể giúp tránh những lỗi này. Mỗi lựa chọn thay thế đều có những đánh đổi riêng, cùng các lợi ích về tính đơn giản, tính linh hoạt và/hoặc khả năng mở rộng.

Đối tượng chuỗi có một phép toán tích hợp đặc biệt: toán tử ``%`` (phép modulo). Toán tử này còn được gọi là toán tử *formatting* hoặc *interpolation* của chuỗi. Với ``format % values`` (trong đó *format* là một chuỗi), các đặc tả chuyển đổi ``%`` trong *format* sẽ được thay thế bằng không hoặc nhiều phần tử của *values*. Hiệu ứng này tương tự như khi sử dụng hàm :c:func:`sprintf` trong ngôn ngữ C. Ví dụ:

.. doctest::

   >>> print('%s has %d quote types.' % ('Python', 2))
   Python has 2 quote types.

Nếu *format* yêu cầu một đối số duy nhất, *values* có thể là một đối tượng không phải tuple duy nhất. [5]_  Trong trường hợp ngược lại, *values* phải là một tuple có chính xác số phần tử được chỉ định bởi chuỗi định dạng hoặc là một đối tượng mapping duy nhất (ví dụ: một dictionary).

.. index::
   single: () (parentheses); in printf-style formatting
   single: * (asterisk); in printf-style formatting
   single: . (dot); in printf-style formatting

Một đặc tả chuyển đổi chứa từ hai ký tự trở lên và có các thành phần sau, phải xuất hiện theo thứ tự này:

#. Ký tự ``'%'``, đánh dấu phần bắt đầu của đặc tả.

#. Khóa mapping (tùy chọn), gồm một chuỗi ký tự đặt trong dấu ngoặc đơn (ví dụ: ``(somename)``).

#. Các cờ chuyển đổi (tùy chọn), ảnh hưởng đến kết quả của một số kiểu chuyển đổi.

#. Độ rộng trường tối thiểu (tùy chọn). Nếu được chỉ định là ``'*'`` (dấu hoa thị), độ rộng thực tế sẽ được đọc từ phần tử tiếp theo của tuple trong *values*, và đối tượng cần chuyển đổi sẽ nằm sau độ rộng trường tối thiểu và độ chính xác tùy chọn.

#. Độ chính xác (tùy chọn), được chỉ định bằng ``'.'`` (dấu chấm) theo sau là độ chính xác. Nếu được chỉ định là ``'*'`` (dấu hoa thị), độ chính xác thực tế sẽ được đọc từ phần tử tiếp theo của tuple trong *values*, và giá trị cần chuyển đổi sẽ nằm sau độ chính xác.

#. Bộ bổ nghĩa độ dài (tùy chọn).

#. Kiểu chuyển đổi.

Khi đối số bên phải là một dictionary (hoặc kiểu mapping khác), các định dạng trong chuỗi *must* bao gồm một khóa mapping đặt trong dấu ngoặc đơn của dictionary đó, được chèn ngay sau ký tự ``'%'``. Khóa mapping chọn giá trị cần định dạng từ mapping. Ví dụ:

   >>> print('%(language)s has %(number)03d quote types.' %
   ...       {'language': "Python", "number": 2})
   Python has 002 quote types.

Trong trường hợp này, không được xuất hiện bộ chỉ định ``*`` nào trong một định dạng (vì chúng yêu cầu một danh sách tham số tuần tự).

Các ký tự cờ chuyển đổi là:

.. index::
   single: # (hash); in printf-style formatting
   single: - (minus); in printf-style formatting
   single: + (plus); in printf-style formatting
   single: space; in printf-style formatting

+---------+-----------------------------------------------------------------------------------------------------------------------------+
| Cờ      | Ý nghĩa                                                                                                                     |
+=========+=============================================================================================================================+
| ``'#'`` | Việc chuyển đổi giá trị sẽ sử dụng "dạng thay thế" (được định nghĩa bên dưới).                                              |
+---------+-----------------------------------------------------------------------------------------------------------------------------+
| ``'0'`` | Kết quả chuyển đổi sẽ được đệm bằng số 0 đối với các giá trị số.                                                            |
+---------+-----------------------------------------------------------------------------------------------------------------------------+
| ``'-'`` | Giá trị đã chuyển đổi được căn trái (ghi đè chuyển đổi ``'0'`` nếu cả hai được chỉ định).                                   |
+---------+-----------------------------------------------------------------------------------------------------------------------------+
| ``' '`` | (một khoảng trắng) Một khoảng trắng sẽ được đặt trước một số dương (hoặc chuỗi rỗng) được tạo ra bởi một chuyển đổi có dấu. |
+---------+-----------------------------------------------------------------------------------------------------------------------------+
| ``'+'`` | Một ký tự dấu (``'+'`` hoặc ``'-'``) sẽ đứng trước kết quả chuyển đổi (ghi đè cờ "khoảng trắng").                           |
+---------+-----------------------------------------------------------------------------------------------------------------------------+

Có thể có một length modifier (``h``, ``l`` hoặc ``L``), nhưng nó bị bỏ qua vì không cần thiết trong Python -- vì vậy, chẳng hạn, ``%ld`` giống hệt ``%d``.

Các kiểu chuyển đổi là:

+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| Chuyển đổi | Ý nghĩa                                                                                                                                                            | Ghi chú |
+============+====================================================================================================================================================================+=========+
| ``'d'``    | Số nguyên thập phân có dấu.                                                                                                                                        |         |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'i'``    | Số nguyên thập phân có dấu.                                                                                                                                        |         |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'o'``    | Giá trị bát phân có dấu.                                                                                                                                           | \(1)    |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'u'``    | Kiểu đã lỗi thời -- giống hệt ``'d'``.                                                                                                                             | \(6)    |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'x'``    | Hệ thập lục phân có dấu (chữ thường).                                                                                                                              | \(2)    |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'X'``    | Hệ thập lục phân có dấu (chữ hoa).                                                                                                                                 | \(2)    |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'e'``    | Định dạng số mũ dấu phẩy động (chữ thường).                                                                                                                        | \(3)    |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'E'``    | Định dạng số mũ dấu phẩy động (chữ hoa).                                                                                                                           | \(3)    |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'f'``    | Định dạng thập phân dấu phẩy động.                                                                                                                                 | \(3)    |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'F'``    | Định dạng số thập phân dấu phẩy động.                                                                                                                              | \(3)    |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'g'``    | Định dạng số dấu phẩy động. Sử dụng định dạng lũy thừa chữ thường nếu số mũ nhỏ hơn -4 hoặc không nhỏ hơn độ chính xác; nếu không thì sử dụng định dạng thập phân. | \(4)    |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'G'``    | Định dạng số dấu phẩy động. Sử dụng định dạng lũy thừa chữ hoa nếu số mũ nhỏ hơn -4 hoặc không nhỏ hơn độ chính xác; nếu không thì sử dụng định dạng thập phân.    | \(4)    |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'c'``    | Ký tự đơn (chấp nhận số nguyên hoặc chuỗi một ký tự).                                                                                                              |         |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'r'``    | Chuỗi (chuyển đổi mọi đối tượng Python bằng                                                                                                                        | \(5)    |
|            | :func:`repr`).                                                                                                                                                     |         |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'s'``    | Chuỗi (chuyển đổi mọi đối tượng Python bằng                                                                                                                        | \(5)    |
|            | :func:`str`).                                                                                                                                                      |         |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'a'``    | Chuỗi (chuyển đổi mọi đối tượng Python bằng                                                                                                                        | \(5)    |
|            | :func:`ascii`).                                                                                                                                                    |         |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'%'``    | Không có đối số nào được chuyển đổi, dẫn đến một ký tự ``'%'`` trong kết quả.                                                                                      |         |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+

Đối với các định dạng số dấu phẩy động, kết quả phải được làm tròn chính xác đến độ chính xác cho trước ``p`` chữ số sau dấu thập phân. Chế độ làm tròn khớp với chế độ của hàm dựng sẵn :func:`round`.

Lưu ý:

(1)
   Dạng thay thế khiến một dấu chỉ định hệ bát phân ở đầu (``'0o'``) được chèn trước chữ số đầu tiên.

(2)
   Dạng thay thế khiến một ``'0x'`` hoặc ``'0X'`` ở đầu (tùy thuộc vào việc sử dụng định dạng ``'x'`` hay ``'X'``) được chèn trước chữ số đầu tiên.

(3)
   Dạng thay thế khiến kết quả luôn chứa dấu thập phân, ngay cả khi không có chữ số nào theo sau dấu đó.

   Độ chính xác xác định số chữ số sau dấu thập phân và mặc định là 6.

(4)
   Dạng thay thế khiến kết quả luôn chứa dấu thập phân và các số 0 ở cuối không bị loại bỏ như trong trường hợp khác.

   Độ chính xác xác định số chữ số có nghĩa trước và sau dấu thập phân, mặc định là 6.

(5)
   Nếu độ chính xác là ``N``, đầu ra sẽ được cắt ngắn còn ``N`` ký tự.

(6)
   Xem :pep:`237`.

Vì chuỗi Python có độ dài tường minh, các phép chuyển đổi ``%s`` không giả định rằng ``'\0'`` là phần cuối của chuỗi.

.. XXX Examples?

.. versionchanged:: 3.1
   Các phép chuyển đổi ``%f`` cho những số có giá trị tuyệt đối lớn hơn 1e50 không còn được thay thế bằng các phép chuyển đổi ``%g``.


.. index::
   single: buffer protocol; binary sequence types

.. _binaryseq:

Các kiểu chuỗi nhị phân --- :class:`bytes`, :class:`bytearray`, :class:`memoryview`
===================================================================================

.. index::
   pair: object; bytes
   pair: object; bytearray
   pair: object; memoryview
   pair: module; array

Các kiểu dựng sẵn cốt lõi để thao tác với dữ liệu nhị phân là :class:`bytes` và
:class:`bytearray`. Chúng được :class:`memoryview` hỗ trợ, sử dụng :ref:`buffer protocol <bufferobjects>` để truy cập bộ nhớ của các đối tượng nhị phân khác mà không cần tạo bản sao.

Mô-đun :mod:`array` hỗ trợ lưu trữ hiệu quả các kiểu dữ liệu cơ bản như số nguyên 32 bit và các giá trị dấu phẩy động độ chính xác kép theo chuẩn IEEE754.

.. _typebytes:

Đối tượng Bytes
---------------

.. index:: pair: object; bytes

Đối tượng bytes là các chuỗi bất biến gồm những byte đơn. Vì nhiều giao thức nhị phân chính dựa trên mã hóa văn bản ASCII, các đối tượng bytes cung cấp một số phương thức chỉ hợp lệ khi làm việc với dữ liệu tương thích ASCII, đồng thời có nhiều điểm tương đồng với các đối tượng chuỗi.

.. class:: bytes(source=b'')
           bytes(source, encoding, errors='strict')

   Trước hết, cú pháp cho các literal bytes phần lớn giống với cú pháp cho các literal chuỗi, ngoại trừ việc thêm tiền tố ``b``:

   * Dấu nháy đơn: ``b'still allows embedded "double" quotes'``
   * Dấu nháy kép: ``b"still allows embedded 'single' quotes"``
   * Dấu nháy ba: ``b'''3 single quotes'''``, ``b"""3 double quotes"""``

   Chỉ cho phép các ký tự ASCII trong các literal bytes (bất kể encoding mã nguồn được khai báo). Mọi giá trị nhị phân lớn hơn 127 phải được nhập vào các literal bytes bằng escape sequence phù hợp.

   Giống như các string literal, literal bytes cũng có thể sử dụng tiền tố ``r`` để tắt việc xử lý các escape sequence. Xem :ref:`strings` để biết thêm về các dạng literal bytes khác nhau, bao gồm cả các escape sequence được hỗ trợ.

   Mặc dù các literal bytes và biểu diễn của chúng dựa trên văn bản ASCII, các đối tượng bytes thực tế hoạt động như những chuỗi số nguyên bất biến, trong đó mỗi giá trị trong chuỗi bị giới hạn sao cho ``0 <= x < 256`` (việc cố gắng vi phạm giới hạn này sẽ kích hoạt :exc:`ValueError`). Điều này được thực hiện có chủ ý để nhấn mạnh rằng mặc dù nhiều định dạng nhị phân có các thành phần dựa trên ASCII và có thể được xử lý hữu ích bằng một số thuật toán hướng văn bản, điều này nhìn chung không đúng với dữ liệu nhị phân tùy ý (việc áp dụng một cách máy móc các thuật toán xử lý văn bản cho những định dạng dữ liệu nhị phân không tương thích với ASCII thường sẽ dẫn đến hỏng dữ liệu).

   Ngoài các dạng literal, các đối tượng bytes còn có thể được tạo theo một số cách khác:

   * Một đối tượng bytes được điền bằng số 0 với độ dài đã chỉ định: ``bytes(10)``
   * Từ một iterable gồm các số nguyên: ``bytes(range(20))``
   * Sao chép dữ liệu nhị phân hiện có thông qua buffer protocol: ``bytes(obj)``

   Xem thêm built-in :ref:`bytes <func-bytes>`.

   Vì 2 chữ số thập lục phân tương ứng chính xác với một byte, các số thập lục phân là định dạng thường được dùng để mô tả dữ liệu nhị phân. Do đó, kiểu bytes có thêm một class method để đọc dữ liệu ở định dạng này:

   .. classmethod:: fromhex(string, /)

      Class method :class:`bytes` này trả về một đối tượng bytes bằng cách giải mã đối tượng chuỗi đã cho. Chuỗi phải chứa hai chữ số thập lục phân cho mỗi byte; khoảng trắng ASCII sẽ được bỏ qua.

      >>> bytes.fromhex('2Ef0 F1f2  ')
      b'.\xf0\xf1\xf2'

      .. versionchanged:: 3.7
         :meth:`bytes.fromhex` now skips all ASCII whitespace in the string,
         không chỉ dấu cách.

      .. versionchanged:: 3.14
         :meth:`bytes.fromhex` now accepts ASCII :class:`bytes` and
         :term:`bytes-like objects <bytes-like object>` as input.

   Một hàm chuyển đổi ngược tồn tại để biến đổi đối tượng bytes thành biểu diễn hệ thập lục phân của nó.

   .. method:: hex(*, bytes_per_sep=1)
               hex(sep, bytes_per_sep=1)

      Trả về một đối tượng chuỗi chứa hai chữ số thập lục phân cho mỗi byte trong đối tượng.

      >>> b'\xf0\xf1\xf2'.hex()
      'f0f1f2'

      Nếu muốn chuỗi thập lục phân dễ đọc hơn, bạn có thể chỉ định tham số *sep* là một ký tự đơn để đưa vào kết quả. Theo mặc định, dấu phân cách này sẽ được chèn giữa mỗi byte. Một tham số tùy chọn thứ hai, *bytes_per_sep*, kiểm soát khoảng cách. Các giá trị dương tính vị trí của dấu phân cách từ phải sang, còn các giá trị âm tính từ trái sang.

      >>> value = b'\xf0\xf1\xf2'
      >>> value.hex('-')
      'f0-f1-f2'
      >>> value.hex('_', 2)
      'f0_f1f2'
      >>> b'UUDDLRLRAB'.hex(' ', -4)
      '55554444 4c524c52 4142'

      .. versionadded:: 3.5

      .. versionchanged:: 3.8
         :meth:`bytes.hex` now supports optional *sep* and *bytes_per_sep*
         các tham số để chèn dấu phân cách giữa các byte trong kết quả thập lục phân.

Vì các đối tượng bytes là các dãy số nguyên (tương tự như tuple), đối với một đối tượng bytes *b*, ``b[0]`` sẽ là một số nguyên, còn ``b[0:1]`` sẽ là một đối tượng bytes có độ dài 1. (Điều này khác với chuỗi văn bản, trong đó cả thao tác lập chỉ mục và cắt đều tạo ra một chuỗi có độ dài 1)

Biểu diễn của các đối tượng bytes sử dụng định dạng literal (``b'...'``) vì định dạng này thường hữu ích hơn, chẳng hạn như ``bytes([46, 46, 46])``. Bạn luôn có thể chuyển đổi một đối tượng bytes thành danh sách các số nguyên bằng cách sử dụng ``list(b)``.


.. _typebytearray:

Đối tượng bytearray
-------------------

.. index:: pair: object; bytearray

Các đối tượng :class:`bytearray` là phiên bản có thể thay đổi của các đối tượng :class:`bytes`.

.. class:: bytearray(source=b'')
           bytearray(source, encoding, errors='strict')

   Không có cú pháp literal riêng cho các đối tượng bytearray; thay vào đó, chúng luôn được tạo bằng cách gọi constructor:

   * Tạo một instance rỗng: ``bytearray()``
   * Tạo một instance chứa các giá trị 0 với độ dài cho trước: ``bytearray(10)``
   * Từ một iterable gồm các số nguyên: ``bytearray(range(20))``
   * Sao chép dữ liệu nhị phân hiện có thông qua giao thức buffer:  ``bytearray(b'Hi!')``

   Vì các đối tượng bytearray có thể thay đổi, chúng hỗ trợ các
   thao tác trên chuỗi :ref:`có thể thay đổi <typesseq-mutable>` ngoài các thao tác phổ biến trên bytes và bytearray được mô tả trong :ref:`bytes-methods`.

   Cũng xem built-in :ref:`bytearray <func-bytearray>`.

   Vì 2 chữ số thập lục phân tương ứng chính xác với một byte, các số thập lục phân là định dạng thường được dùng để mô tả dữ liệu nhị phân. Do đó, kiểu bytearray có thêm một phương thức lớp để đọc dữ liệu ở định dạng đó:

   .. classmethod:: fromhex(string, /)

      Phương thức lớp :class:`bytearray` này trả về một đối tượng bytearray bằng cách giải mã đối tượng chuỗi đã cho. Chuỗi phải chứa hai chữ số thập lục phân cho mỗi byte, trong đó khoảng trắng ASCII được bỏ qua.

      >>> bytearray.fromhex('2Ef0 F1f2  ')
      bytearray(b'.\xf0\xf1\xf2')

      .. versionchanged:: 3.7
         :meth:`bytearray.fromhex` now skips all ASCII whitespace in the string,
         không chỉ khoảng trắng.

      .. versionchanged:: 3.14
         :meth:`bytearray.fromhex` now accepts ASCII :class:`bytes` and
         :term:`bytes-like objects <bytes-like object>` as input.

   Có một hàm chuyển đổi ngược để biến đối tượng bytearray thành biểu diễn thập lục phân của nó.

   .. method:: hex(*, bytes_per_sep=1)
               hex(sep, bytes_per_sep=1)

      Trả về một đối tượng chuỗi chứa hai chữ số thập lục phân cho mỗi byte trong instance.

      >>> bytearray(b'\xf0\xf1\xf2').hex()
      'f0f1f2'

      .. versionadded:: 3.5

      .. versionchanged:: 3.8
         Tương tự như :meth:`bytes.hex`, hiện :meth:`bytearray.hex` hỗ trợ các tham số *sep* và *bytes_per_sep* tùy chọn để chèn dấu phân cách giữa các byte trong đầu ra thập lục phân.

   .. method:: resize(size, /)

      Thay đổi kích thước :class:`bytearray` để chứa *size* byte. *size* phải lớn hơn hoặc bằng 0.

      Nếu :class:`bytearray` cần được thu nhỏ, các byte nằm sau *size* sẽ bị cắt bỏ.

      Nếu :class:`bytearray` cần được mở rộng, tất cả byte mới, tức các byte nằm sau *size*, sẽ được đặt thành các byte null.


      Điều này tương đương với:

      >>> def resize(ba, size):
      ...     if len(ba) > size:
      ...         del ba[size:]
      ...     else:
      ...         ba += b'\0' * (size - len(ba))

      Ví dụ:

      >>> shrink = bytearray(b'abc')
      >>> shrink.resize(1)
      >>> (shrink, len(shrink))
      (bytearray(b'a'), 1)
      >>> grow = bytearray(b'abc')
      >>> grow.resize(5)
      >>> (grow, len(grow))
      (bytearray(b'abc\x00\x00'), 5)

      .. versionadded:: 3.14

Vì các đối tượng bytearray là các dãy số nguyên (tương tự như một danh sách), đối với một đối tượng bytearray *b*, ``b[0]`` sẽ là một số nguyên, trong khi ``b[0:1]`` sẽ là một đối tượng bytearray có độ dài 1. (Điều này khác với các chuỗi văn bản, trong đó cả thao tác lập chỉ mục và cắt đều tạo ra một chuỗi có độ dài 1)

Biểu diễn của các đối tượng bytearray sử dụng định dạng bytes literal (``bytearray(b'...')``) vì định dạng này thường hữu ích hơn, chẳng hạn như ``bytearray([46, 46, 46])``. Bạn luôn có thể chuyển đổi một đối tượng bytearray thành một danh sách các số nguyên bằng cách sử dụng ``list(b)``.

.. seealso::

   Để biết thông tin chi tiết về các đảm bảo an toàn luồng cho các đối tượng :class:`bytearray`, hãy xem :ref:`thread-safety-bytearray`.


.. _bytes-methods:

Các thao tác với Bytes và Bytearray
-----------------------------------

.. index:: pair: bytes; methods
           pair: bytearray; methods

Cả các đối tượng bytes và bytearray đều hỗ trợ các thao tác chuỗi :ref:`common <typesseq-common>`. Chúng không chỉ tương tác với các toán hạng cùng kiểu mà còn với bất kỳ :term:`bytes-like object` nào. Nhờ tính linh hoạt này, bạn có thể tự do kết hợp chúng trong các thao tác mà không gây ra lỗi. Tuy nhiên, kiểu trả về của kết quả có thể phụ thuộc vào thứ tự của các toán hạng.

.. note::

   Các phương thức trên đối tượng bytes và bytearray không chấp nhận chuỗi làm đối số, cũng như các phương thức trên chuỗi không chấp nhận bytes làm đối số. Ví dụ, bạn phải viết::

      a = "abc"
      b = a.replace("a", "f")

   và::

      a = b"abc"
      b = a.replace(b"a", b"f")

Một số thao tác trên bytes và bytearray giả định sử dụng các định dạng nhị phân tương thích với ASCII, do đó nên tránh dùng chúng khi làm việc với dữ liệu nhị phân tùy ý. Những hạn chế này được trình bày bên dưới.

.. note::
   Việc sử dụng các thao tác dựa trên ASCII này để xử lý dữ liệu nhị phân không được lưu trữ ở định dạng dựa trên ASCII có thể dẫn đến hỏng dữ liệu.

Có thể sử dụng các phương thức sau trên đối tượng bytes và bytearray với dữ liệu nhị phân tùy ý.

.. method:: bytes.count(sub[, start[, end]])
            bytearray.count(sub[, start[, end]])

   Trả về số lần xuất hiện không chồng lấp của chuỗi con *sub* trong phạm vi [*start*, *end*]. Các đối số tùy chọn *start* và *end* được diễn giải như trong ký hiệu lát cắt.

   Chuỗi con cần tìm có thể là bất kỳ :term:`bytes-like object` nào hoặc một số nguyên trong phạm vi từ 0 đến 255.

   Nếu *sub* rỗng, trả về số lát cắt rỗng giữa các ký tự, bằng độ dài của đối tượng bytes cộng một.

   .. versionchanged:: 3.3
      Cũng chấp nhận một số nguyên trong phạm vi từ 0 đến 255 làm chuỗi con.


.. method:: bytes.removeprefix(prefix, /)
            bytearray.removeprefix(prefix, /)

   Nếu dữ liệu nhị phân bắt đầu bằng chuỗi *prefix*, trả về ``bytes[len(prefix):]``. Nếu không, trả về một bản sao của dữ liệu nhị phân ban đầu.::

      >>> b'TestHook'.removeprefix(b'Test')
      b'Hook'
      >>> b'BaseTestCase'.removeprefix(b'Test')
      b'BaseTestCase'

   *prefix* có thể là bất kỳ :term:`bytes-like object` nào.

   .. note::

      Phiên bản bytearray của phương thức này *không* hoạt động tại chỗ — nó luôn tạo ra một đối tượng mới, ngay cả khi không có thay đổi nào được thực hiện.

   .. versionadded:: 3.9


.. method:: bytes.removesuffix(suffix, /)
            bytearray.removesuffix(suffix, /)

   Nếu dữ liệu nhị phân kết thúc bằng chuỗi *hậu tố* và *hậu tố* đó không rỗng, hãy trả về ``bytes[:-len(suffix)]``. Nếu không, hãy trả về một bản sao của dữ liệu nhị phân ban đầu::

      >>> b'MiscTests'.removesuffix(b'Tests')
      b'Misc'
      >>> b'TmpDirMixin'.removesuffix(b'Tests')
      b'TmpDirMixin'

   *Hậu tố* có thể là bất kỳ :term:`bytes-like object` nào.

   .. note::

      Phiên bản bytearray của phương thức này *không* hoạt động tại chỗ — nó luôn tạo ra một đối tượng mới, ngay cả khi không có thay đổi nào được thực hiện.

   .. versionadded:: 3.9


.. method:: bytes.decode(encoding="utf-8", errors="strict")
            bytearray.decode(encoding="utf-8", errors="strict")

   Trả về các byte được giải mã thành một :class:`str`.

   *encoding* mặc định là ``'utf-8'``; xem :ref:`standard-encodings` để biết các giá trị có thể dùng.

   *errors* kiểm soát cách xử lý các lỗi giải mã. Nếu ``'strict'`` (mặc định), một ngoại lệ :exc:`UnicodeError` sẽ được phát sinh. Các giá trị khả dĩ khác là ``'ignore'``, ``'replace'`` và mọi tên khác được đăng ký qua :func:`codecs.register_error`. Xem :ref:`error-handlers` để biết chi tiết.

   Vì lý do hiệu năng, giá trị của *errors* không được kiểm tra tính hợp lệ trừ khi lỗi giải mã thực sự xảy ra,
   :ref:`devmode` được bật hoặc một bản dựng :ref:`debug build <debug-build>` được sử dụng.

   .. note::

      Việc truyền đối số *encoding* cho :class:`str` cho phép giải mã bất kỳ
      :term:`bytes-like object` trực tiếp mà không cần tạo một
      :class:`!bytes` hoặc đối tượng :class:`!bytearray`.

   .. versionchanged:: 3.1
      Đã bổ sung hỗ trợ cho các đối số từ khóa.

   .. versionchanged:: 3.9
      Giá trị của đối số *errors* hiện được kiểm tra trong :ref:`devmode` và trong :ref:`debug mode <debug-build>`.


.. method:: bytes.endswith(suffix[, start[, end]])
            bytearray.endswith(suffix[, start[, end]])

   Trả về ``True`` nếu dữ liệu nhị phân kết thúc bằng *suffix* được chỉ định, nếu không thì trả về ``False``.  *suffix* cũng có thể là một tuple gồm các hậu tố cần tìm.  Với *start* tùy chọn, kiểm tra bắt đầu từ vị trí đó.  Với *end* tùy chọn, dừng so sánh tại vị trí đó.

   (Các) hậu tố cần tìm có thể là bất kỳ :term:`bytes-like object` nào.


.. method:: bytes.find(sub[, start[, end]])
            bytearray.find(sub[, start[, end]])

   Trả về chỉ mục nhỏ nhất trong dữ liệu tại đó tìm thấy chuỗi con *sub*, sao cho *sub* nằm trong lát cắt ``s[start:end]``.  Các đối số tùy chọn *start* và *end* được diễn giải như trong ký hiệu lát cắt.  Trả về ``-1`` nếu không tìm thấy *sub*.

   Chuỗi con cần tìm có thể là bất kỳ :term:`bytes-like object` nào hoặc một số nguyên trong phạm vi từ 0 đến 255.

   .. note::

      Chỉ nên sử dụng phương thức :meth:`~bytes.find` nếu bạn cần biết vị trí của *sub*. Để kiểm tra xem *sub* có phải là chuỗi con hay không, hãy sử dụng
      toán tử :keyword:`in`::

         >>> b'Py' in b'Python'
         True

   .. versionchanged:: 3.3
      Cũng chấp nhận một số nguyên trong phạm vi từ 0 đến 255 làm chuỗi con.


.. method:: bytes.index(sub[, start[, end]])
            bytearray.index(sub[, start[, end]])

   Tương tự :meth:`~bytes.find`, nhưng sẽ phát sinh :exc:`ValueError` nếu không tìm thấy chuỗi con.

   Chuỗi con cần tìm có thể là bất kỳ :term:`bytes-like object` nào hoặc một số nguyên trong phạm vi từ 0 đến 255.

   .. versionchanged:: 3.3
      Cũng chấp nhận một số nguyên trong phạm vi từ 0 đến 255 làm chuỗi con.


.. method:: bytes.join(iterable, /)
            bytearray.join(iterable, /)

   Trả về một đối tượng bytes hoặc bytearray là kết quả nối các chuỗi dữ liệu nhị phân trong *iterable*. Một :exc:`TypeError` sẽ được phát sinh nếu có bất kỳ giá trị nào trong *iterable* không phải là :term:`bytes-like objects <bytes-like object>`, bao gồm cả các đối tượng :class:`str`. Dấu phân cách giữa các phần tử là nội dung của đối tượng bytes hoặc bytearray cung cấp phương thức này.


.. staticmethod:: bytes.maketrans(from, to, /)
                  bytearray.maketrans(from, to, /)

   Phương thức static này trả về một bảng chuyển đổi có thể dùng cho
   :meth:`bytes.translate` để ánh xạ mỗi ký tự trong *from* thành ký tự ở cùng vị trí trong *to*; *from* và *to* đều phải là
   :term:`bytes-like objects <bytes-like object>` và có cùng độ dài.

   .. versionadded:: 3.1


.. method:: bytes.partition(sep, /)
            bytearray.partition(sep, &)

   Tách sequence tại lần xuất hiện đầu tiên của *sep*, rồi trả về một 3-tuple chứa phần trước dấu phân tách, chính dấu phân tách hoặc bản sao bytearray của nó, và phần sau dấu phân tách. Nếu không tìm thấy dấu phân tách, trả về một 3-tuple chứa bản sao của sequence ban đầu, theo sau là hai đối tượng bytes hoặc bytearray rỗng.

   Dấu phân tách cần tìm có thể là bất kỳ :term:`bytes-like object` nào.


.. method:: bytes.replace(old, new, count=-1, /)
            bytearray.replace(old, new, count=-1, /)

   Trả về một bản sao của sequence, trong đó tất cả các lần xuất hiện của subsequence *old* được thay thế bằng *new*. Nếu cung cấp đối số tùy chọn *count*, chỉ *count* lần xuất hiện đầu tiên được thay thế.

   Subsequence cần tìm và phần thay thế có thể là bất kỳ
   :term:`bytes-like object`.

   .. note::

      Phiên bản bytearray của phương thức này *không* hoạt động tại chỗ — nó luôn tạo ra một đối tượng mới, ngay cả khi không có thay đổi nào được thực hiện.


.. method:: bytes.rfind(sub[, start[, end]])
            bytearray.rfind(sub[, start[, end]])

   Trả về chỉ số lớn nhất trong dãy mà tại đó chuỗi con *sub* được tìm thấy, sao cho *sub* nằm trong ``s[start:end]``. Các đối số tùy chọn *start* và *end* được diễn giải như trong cú pháp lát cắt. Trả về ``-1`` nếu không tìm thấy.

   Chuỗi con cần tìm có thể là bất kỳ :term:`bytes-like object` nào hoặc một số nguyên trong phạm vi từ 0 đến 255.

   .. versionchanged:: 3.3
      Cũng chấp nhận một số nguyên trong phạm vi từ 0 đến 255 làm chuỗi con.


.. method:: bytes.rindex(sub[, start[, end]])
            bytearray.rindex(sub[, start[, end]])

   Tương tự :meth:`~bytes.rfind`, nhưng phát sinh :exc:`ValueError` khi không tìm thấy chuỗi con *sub*.

   Chuỗi con cần tìm có thể là bất kỳ :term:`bytes-like object` nào hoặc một số nguyên trong phạm vi từ 0 đến 255.

   .. versionchanged:: 3.3
      Cũng chấp nhận một số nguyên trong phạm vi từ 0 đến 255 làm chuỗi con.


.. method:: bytes.rpartition(sep, /)
            bytearray.rpartition(sep, /)

   Tách chuỗi tại lần xuất hiện cuối cùng của *sep*, rồi trả về một bộ 3 phần tử gồm phần trước dấu phân tách, chính dấu phân tách hoặc bản sao bytearray của nó, và phần sau dấu phân tách. Nếu không tìm thấy dấu phân tách, trả về một bộ 3 phần tử gồm hai đối tượng bytes hoặc bytearray rỗng, theo sau là bản sao của chuỗi ban đầu.

   Dấu phân tách cần tìm có thể là bất kỳ :term:`bytes-like object` nào.


.. method:: bytes.startswith(prefix[, start[, end]])
            bytearray.startswith(prefix[, start[, end]])

   Trả về ``True`` nếu dữ liệu nhị phân bắt đầu bằng *prefix* được chỉ định; nếu không, trả về ``False``. *prefix* cũng có thể là một tuple gồm các tiền tố cần tìm. Với *start* tùy chọn, kiểm tra bắt đầu từ vị trí đó. Với *end* tùy chọn, dừng so sánh tại vị trí đó.

   Các tiền tố cần tìm có thể là bất kỳ :term:`bytes-like object`.


.. method:: bytes.translate(table, /, delete=b'')
            bytearray.translate(table, /, delete=b'')

   Trả về một bản sao của đối tượng bytes hoặc bytearray, trong đó tất cả các byte xuất hiện trong đối số tùy chọn *delete* đều bị xóa, còn các byte còn lại được ánh xạ qua bảng chuyển đổi đã cho; bảng này phải là một đối tượng bytes có độ dài 256.

   Bạn có thể sử dụng phương thức :func:`bytes.maketrans` để tạo bảng chuyển đổi.

   Đặt đối số *table* thành ``None`` cho các phép chuyển đổi chỉ xóa ký tự::

      >>> b'read this short text'.translate(None, b'aeiou')
      b'rd ths shrt txt'

   .. versionchanged:: 3.6
      *delete* hiện được hỗ trợ dưới dạng đối số từ khóa.


Các phương thức sau đây trên đối tượng bytes và bytearray có hành vi mặc định giả định rằng đang sử dụng các định dạng nhị phân tương thích với ASCII, nhưng vẫn có thể được sử dụng với dữ liệu nhị phân tùy ý bằng cách truyền các đối số thích hợp. Lưu ý rằng tất cả các phương thức bytearray trong phần này *not* đều không hoạt động tại chỗ mà thay vào đó tạo ra các đối tượng mới.

.. method:: bytes.center(width, fillbyte=b' ', /)
            bytearray.center(width, fillbyte=b' ', /)

   Trả về một bản sao của đối tượng được căn giữa trong một chuỗi có độ dài *width*. Việc đệm được thực hiện bằng *fillbyte* đã chỉ định (mặc định là dấu cách ASCII). Đối với các đối tượng :class:`bytes`, chuỗi ban đầu được trả về nếu *width* nhỏ hơn hoặc bằng ``len(s)``.

   .. note::

      Phiên bản bytearray của phương thức này *không* hoạt động tại chỗ — nó luôn tạo ra một đối tượng mới, ngay cả khi không có thay đổi nào được thực hiện.


.. method:: bytes.ljust(width, fillbyte=b' ', /)
            bytearray.ljust(width, fillbyte=b' ', /)

   Trả về một bản sao của đối tượng được căn trái trong một chuỗi có độ dài *width*. Việc đệm được thực hiện bằng *fillbyte* đã chỉ định (mặc định là khoảng trắng ASCII). Đối với các đối tượng :class:`bytes`, chuỗi ban đầu được trả về nếu *width* nhỏ hơn hoặc bằng ``len(s)``.

   .. note::

      Phiên bản bytearray của phương thức này *không* hoạt động tại chỗ — nó luôn tạo ra một đối tượng mới, ngay cả khi không có thay đổi nào được thực hiện.


.. method:: bytes.lstrip(bytes=None, /)
            bytearray.lstrip(bytes=None, /)

   Trả về một bản sao của chuỗi sau khi loại bỏ các byte đứng đầu được chỉ định. Đối số *bytes* là một chuỗi nhị phân chỉ định tập hợp các giá trị byte cần loại bỏ. Nếu bị bỏ qua hoặc là ``None``, đối số *bytes* mặc định loại bỏ :meth:`ASCII whitespace <bytes.isspace>`. Đối số *bytes* không phải là tiền tố; thay vào đó, mọi tổ hợp các giá trị của nó đều bị loại bỏ::

      >>> b'   spacious   '.lstrip()
      b'spacious   '
      >>> b'www.example.com'.lstrip(b'cmowz.')
      b'example.com'

   Chuỗi nhị phân gồm các giá trị byte cần loại bỏ có thể là bất kỳ
   :term:`bytes-like object`. Xem :meth:`~bytes.removeprefix` để biết một phương pháp sẽ loại bỏ một chuỗi tiền tố duy nhất thay vì toàn bộ một tập hợp ký tự. Ví dụ::

      >>> b'Arthur: three!'.lstrip(b'Arthur: ')
      b'ee!'
      >>> b'Arthur: three!'.removeprefix(b'Arthur: ')
      b'three!'

   .. note::

      Phiên bản bytearray của phương thức này *không* hoạt động tại chỗ — nó luôn tạo ra một đối tượng mới, ngay cả khi không có thay đổi nào được thực hiện.


.. method:: bytes.rjust(width, fillbyte=b' ', /)
            bytearray.rjust(width, fillbyte=b' ', /)

   Trả về một bản sao của đối tượng được căn phải trong một chuỗi có độ dài *width*. Việc đệm được thực hiện bằng *fillbyte* đã chỉ định (mặc định là một khoảng trắng ASCII). Đối với các đối tượng :class:`bytes`, chuỗi ban đầu được trả về nếu *width* nhỏ hơn hoặc bằng ``len(s)``.

   .. note::

      Phiên bản bytearray của phương thức này *không* hoạt động tại chỗ — nó luôn tạo ra một đối tượng mới, ngay cả khi không có thay đổi nào được thực hiện.


.. method:: bytes.rsplit(sep=None, maxsplit=-1)
            bytearray.rsplit(sep=None, maxsplit=-1)

   Tách chuỗi nhị phân thành các chuỗi con cùng kiểu, sử dụng *sep* làm chuỗi phân cách. Nếu *maxsplit* được cung cấp, sẽ thực hiện nhiều nhất *maxsplit* lần tách, tính từ các vị trí *rightmost*. Nếu *sep* không được chỉ định hoặc ``None``, mọi chuỗi con chỉ bao gồm
   :meth:`ASCII whitespace <bytes.isspace>` là một dấu phân cách. Ngoại trừ việc tách từ bên phải, :meth:`rsplit` hoạt động giống như
   :meth:`split` được mô tả chi tiết bên dưới.


.. method:: bytes.rstrip(bytes=None, /)
            bytearray.rstrip(bytes=None, /)

   Trả về một bản sao của chuỗi với các byte ở cuối được chỉ định đã bị loại bỏ. Đối số *bytes* là một chuỗi nhị phân xác định tập hợp các giá trị byte cần loại bỏ. Nếu bị bỏ qua hoặc là ``None``, đối số *bytes* mặc định sẽ loại bỏ :meth:`ASCII whitespace <bytes.isspace>`. Đối số *bytes* không phải là một hậu tố; thay vào đó, tất cả các tổ hợp giá trị của nó đều bị loại bỏ::

      >>> b'   spacious   '.rstrip()
      b'   spacious'
      >>> b'mississippi'.rstrip(b'ipz')
      b'mississ'

   Chuỗi nhị phân gồm các giá trị byte cần loại bỏ có thể là bất kỳ
   :term:`bytes-like object`. Xem :meth:`~bytes.removesuffix` để biết một phương thức loại bỏ một chuỗi hậu tố duy nhất thay vì toàn bộ một tập hợp ký tự. Ví dụ::

      >>> b'Monty Python'.rstrip(b' Python')
      b'M'
      >>> b'Monty Python'.removesuffix(b' Python')
      b'Monty'

   .. note::

      Phiên bản bytearray của phương thức này *không* hoạt động tại chỗ — nó luôn tạo ra một đối tượng mới, ngay cả khi không có thay đổi nào được thực hiện.


.. method:: bytes.split(sep=None, maxsplit=-1)
            bytearray.split(sep=None, maxsplit=-1)

   Tách chuỗi nhị phân thành các chuỗi con cùng kiểu, sử dụng *sep* làm chuỗi phân cách. Nếu *maxsplit* được cung cấp và không âm, thực hiện tối đa *maxsplit* lần tách (do đó, danh sách sẽ có nhiều nhất ``maxsplit+1`` phần tử). Nếu *maxsplit* không được chỉ định hoặc là ``-1``, thì số lần tách không bị giới hạn (thực hiện mọi lần tách có thể).

   Nếu cung cấp *sep*, các dấu phân cách liên tiếp không được nhóm lại với nhau và được xem là phân cách các chuỗi con rỗng (ví dụ, ``b'1,,2'.split(b',')`` trả về ``[b'1', b'', b'2']``). Đối số *sep* có thể gồm một chuỗi nhiều byte làm một dấu phân cách duy nhất. Tách một chuỗi rỗng bằng dấu phân cách được chỉ định sẽ trả về ``[b'']`` hoặc ``[bytearray(b'')]``, tùy thuộc vào kiểu của đối tượng được tách. Đối số *sep* có thể là bất kỳ
   :term:`bytes-like object`.

   Ví dụ::

      >>> b'1,2,3'.split(b',')
      [b'1', b'2', b'3']
      >>> b'1,2,3'.split(b',', maxsplit=1)
      [b'1', b'2,3']
      >>> b'1,2,,3,'.split(b',')
      [b'1', b'2', b'', b'3', b'']
      >>> b'1<>2<>3<4'.split(b'<>')
      [b'1', b'2', b'3<4']

   Nếu *sep* không được chỉ định hoặc là ``None``, một thuật toán tách khác sẽ được áp dụng: các chuỗi liên tiếp gồm :meth:`ASCII whitespace <bytes.isspace>` được xem là một dấu phân cách duy nhất, và kết quả sẽ không chứa các chuỗi rỗng ở đầu hoặc cuối nếu chuỗi có khoảng trắng ở đầu hoặc cuối. Do đó, việc tách một chuỗi rỗng hoặc một chuỗi chỉ gồm khoảng trắng ASCII mà không chỉ định dấu phân cách sẽ trả về ``[]``.

   Ví dụ::


      >>> b'1 2 3'.split()
      [b'1', b'2', b'3']
      >>> b'1 2 3'.split(maxsplit=1)
      [b'1', b'2 3']
      >>> b'   1   2   3   '.split()
      [b'1', b'2', b'3']


.. method:: bytes.strip(bytes=None, /)
            bytearray.strip(bytes=None, _)

   Trả về một bản sao của chuỗi sau khi loại bỏ các byte đầu và cuối được chỉ định. Đối số *bytes* là một chuỗi nhị phân chỉ định tập hợp các giá trị byte cần loại bỏ. Nếu bị bỏ qua hoặc là ``None``, đối số *bytes* mặc định sẽ loại bỏ :meth:`ASCII whitespace <bytes.isspace>`. Đối số *bytes* không phải là tiền tố hay hậu tố; thay vào đó, tất cả các tổ hợp của các giá trị trong đó đều bị loại bỏ::

      >>> b'   spacious   '.strip()
      b'spacious'
      >>> b'www.example.com'.strip(b'cmowz.')
      b'example'

   Chuỗi nhị phân gồm các giá trị byte cần loại bỏ có thể là bất kỳ
   :term:`bytes-like object`.

   .. note::

      Phiên bản bytearray của phương thức này *không* hoạt động tại chỗ — nó luôn tạo ra một đối tượng mới, ngay cả khi không có thay đổi nào được thực hiện.


Các phương thức sau đây trên các đối tượng bytes và bytearray giả định sử dụng các định dạng nhị phân tương thích với ASCII và không nên được áp dụng cho dữ liệu nhị phân tùy ý. Lưu ý rằng tất cả các phương thức bytearray trong phần này *không* hoạt động tại chỗ mà thay vào đó tạo ra các đối tượng mới.

.. method:: bytes.capitalize()
            bytearray.capitalize()

   Trả về một bản sao của chuỗi, trong đó mỗi byte được diễn giải dưới dạng một ký tự ASCII, byte đầu tiên được viết hoa và các byte còn lại được viết thường. Các giá trị byte không phải ASCII được giữ nguyên.

   .. note::

      Phiên bản bytearray của phương thức này *không* hoạt động tại chỗ — nó luôn tạo ra một đối tượng mới, ngay cả khi không có thay đổi nào được thực hiện.


.. method:: bytes.expandtabs(tabsize=8)
            bytearray.expandtabs(tabsize=8)

   Trả về một bản sao của chuỗi, trong đó tất cả ký tự tab ASCII được thay thế bằng một hoặc nhiều khoảng trắng ASCII, tùy thuộc vào cột hiện tại và kích thước tab đã cho. Vị trí tab xuất hiện sau mỗi *tabsize* byte (mặc định là 8, tạo ra các vị trí tab ở cột 0, 8, 16, v.v.). Để mở rộng chuỗi, cột hiện tại được đặt về 0 và chuỗi được kiểm tra từng byte một. Nếu byte là ký tự tab ASCII (``b'\t'``), một hoặc nhiều ký tự khoảng trắng được chèn vào kết quả cho đến khi cột hiện tại bằng vị trí tab tiếp theo. (Bản thân ký tự tab không được sao chép.) Nếu byte hiện tại là ký tự dòng mới ASCII (``b'\n'``) hoặc ký tự xuống dòng ASCII (``b'\r'``), byte đó được sao chép và cột hiện tại được đặt lại về 0. Mọi giá trị byte khác được sao chép không thay đổi và cột hiện tại được tăng thêm một, bất kể giá trị byte đó được biểu diễn như thế nào khi in ra::

      >>> b'01\t012\t0123\t01234'.expandtabs()
      b'01      012     0123    01234'
      >>> b'01\t012\t0123\t01234'.expandtabs(4)
      b'01  012 0123    01234'

   .. note::

      Phiên bản bytearray của phương thức này *không* hoạt động tại chỗ — nó luôn tạo ra một đối tượng mới, ngay cả khi không có thay đổi nào được thực hiện.


.. method:: bytes.isalnum()
            bytearray.isalnum()

   Trả về ``True`` nếu tất cả byte trong chuỗi là các ký tự chữ cái ASCII hoặc chữ số thập phân ASCII và chuỗi không rỗng, nếu không thì trả về ``False``. Các ký tự chữ cái ASCII là những giá trị byte trong chuỗi ``b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'``. Chữ số thập phân ASCII là những giá trị byte trong chuỗi ``b'0123456789'``.

   Ví dụ::

      >>> b'ABCabc1'.isalnum()
      True
      >>> b'ABC abc1'.isalnum()
      False


.. method:: bytes.isalpha()
            bytearray.isalpha()

   Trả về ``True`` nếu tất cả byte trong dãy đều là ký tự ASCII chữ cái và dãy không rỗng, và ``False`` trong trường hợp ngược lại. Ký tự ASCII chữ cái là các giá trị byte trong dãy ``b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'``.

   Ví dụ::

      >>> b'ABCabc'.isalpha()
      True
      >>> b'ABCabc1'.isalpha()
      False


.. method:: bytes.isascii()
            bytearray.isascii()

   Trả về ``True`` nếu dãy rỗng hoặc tất cả byte trong dãy đều là ASCII, và ``False`` trong trường hợp ngược lại. Byte ASCII nằm trong phạm vi từ 0 đến 0x7F.

   .. versionadded:: 3.7


.. method:: bytes.isdigit()
            bytearray.isdigit()

   Trả về ``True`` nếu tất cả byte trong dãy đều là chữ số thập phân ASCII và dãy không rỗng, và ``False`` trong trường hợp ngược lại. Chữ số thập phân ASCII là các giá trị byte trong dãy ``b'0123456789'``.

   Ví dụ::

      >>> b'1234'.isdigit()
      True
      >>> b'1.23'.isdigit()
      False


.. method:: bytes.islower()
            bytearray.islower()

   Trả về ``True`` nếu trong chuỗi có ít nhất một ký tự ASCII viết thường và không có ký tự ASCII viết hoa nào, nếu không thì trả về ``False``.

   Ví dụ::

      >>> b'hello world'.islower()
      True
      >>> b'Hello world'.islower()
      False

   Ký tự ASCII viết thường là các giá trị byte trong chuỗi ``b'abcdefghijklmnopqrstuvwxyz'``. Ký tự ASCII viết hoa là các giá trị byte trong chuỗi ``b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'``.


.. method:: bytes.isspace()
            bytearray.isspace()

   Trả về ``True`` nếu tất cả byte trong chuỗi đều là khoảng trắng ASCII và chuỗi không rỗng, nếu không thì trả về ``False``. Các ký tự khoảng trắng ASCII là những giá trị byte trong chuỗi ``b' \t\n\r\x0b\f'`` (dấu cách, tab, dòng mới, xuống dòng về đầu, tab dọc, ngắt trang).


.. method:: bytes.istitle()
            bytearray.istitle()

   Trả về ``True`` nếu chuỗi ở dạng titlecase ASCII và không rỗng, ngược lại trả về ``False``. Xem :meth:`bytes.title` để biết thêm chi tiết về định nghĩa của "titlecase".

   Ví dụ::

      >>> b'Hello World'.istitle()
      True
      >>> b'Hello world'.istitle()
      False


.. method:: bytes.isupper()
            bytearray.isupper()

   Trả về ``True`` nếu chuỗi có ít nhất một ký tự chữ cái ASCII viết hoa và không có ký tự ASCII viết thường nào, ngược lại trả về ``False``.

   Ví dụ::

      >>> b'HELLO WORLD'.isupper()
      True
      >>> b'Hello world'.isupper()
      False

   Ký tự ASCII viết thường là các giá trị byte trong chuỗi ``b'abcdefghijklmnopqrstuvwxyz'``. Ký tự ASCII viết hoa là các giá trị byte trong chuỗi ``b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'``.


.. method:: bytes.lower()
            bytearray.lower()

   Trả về một bản sao của chuỗi, trong đó tất cả ký tự ASCII viết hoa được chuyển thành ký tự viết thường tương ứng.

   Ví dụ::

      >>> b'Hello World'.lower()
      b'hello world'

   Ký tự ASCII viết thường là các giá trị byte trong chuỗi ``b'abcdefghijklmnopqrstuvwxyz'``. Ký tự ASCII viết hoa là các giá trị byte trong chuỗi ``b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'``.

   .. note::

      Phiên bản bytearray của phương thức này *không* hoạt động tại chỗ — nó luôn tạo ra một đối tượng mới, ngay cả khi không có thay đổi nào được thực hiện.


.. index::
   single: universal newlines; bytes.splitlines method
   single: universal newlines; bytearray.splitlines method

.. method:: bytes.splitlines(keepends=False)
            bytearray.splitlines(keepends=False)

   Trả về danh sách các dòng trong chuỗi nhị phân, phân tách tại các ranh giới dòng ASCII. Phương thức này sử dụng cách tiếp cận :term:`universal newlines` để tách dòng. Các dấu ngắt dòng không được đưa vào danh sách kết quả, trừ khi *keepends* được cung cấp và có giá trị true.

   Ví dụ::

      >>> b'ab c\n\nde fg\rkl\r\n'.splitlines()
      [b'ab c', b'', b'de fg', b'kl']
      >>> b'ab c\n\nde fg\rkl\r\n'.splitlines(keepends=True)
      [b'ab c\n', b'\n', b'de fg\r', b'kl\r\n']

   Không giống :meth:`~bytes.split` khi cung cấp chuỗi dấu phân cách *sep*, phương thức này trả về một danh sách rỗng đối với chuỗi rỗng, và ký tự ngắt dòng ở cuối không tạo thêm dòng nào::

      >>> b"".split(b'\n'), b"Two lines\n".split(b'\n')
      ([b''], [b'Two lines', b''])
      >>> b"".splitlines(), b"One line\n".splitlines()
      ([], [b'One line'])


.. method:: bytes.swapcase()
            bytearray.swapcase()

   Trả về một bản sao của chuỗi, trong đó tất cả các ký tự ASCII viết thường được chuyển thành ký tự viết hoa tương ứng và ngược lại.

   Ví dụ::

      >>> b'Hello World'.swapcase()
      b'hELLO wORLD'

   Ký tự ASCII viết thường là các giá trị byte trong chuỗi ``b'abcdefghijklmnopqrstuvwxyz'``. Ký tự ASCII viết hoa là các giá trị byte trong chuỗi ``b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'``.

   Không giống :func:`str.swapcase`, ``bin.swapcase().swapcase() == bin`` luôn đúng đối với các phiên bản nhị phân. Việc chuyển đổi kiểu chữ có tính đối xứng trong ASCII, mặc dù điều này nhìn chung không đúng với các điểm mã Unicode tùy ý.

   .. note::

      Phiên bản bytearray của phương thức này *không* hoạt động tại chỗ — nó luôn tạo ra một đối tượng mới, ngay cả khi không có thay đổi nào được thực hiện.


.. method:: bytes.title()
            bytearray.title()

   Trả về phiên bản viết hoa kiểu tiêu đề của chuỗi nhị phân, trong đó các từ bắt đầu bằng một ký tự ASCII viết hoa và các ký tự còn lại được viết thường. Các giá trị byte không có dạng chữ được giữ nguyên.

   Ví dụ::

      >>> b'Hello world'.title()
      b'Hello World'

   Các ký tự ASCII viết thường là những giá trị byte trong chuỗi ``b'abcdefghijklmnopqrstuvwxyz'``. Các ký tự ASCII viết hoa là những giá trị byte trong chuỗi ``b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'``. Tất cả các giá trị byte khác đều không có dạng chữ.

   Thuật toán sử dụng một định nghĩa đơn giản, không phụ thuộc ngôn ngữ, về một từ là một nhóm các chữ cái liên tiếp. Định nghĩa này phù hợp trong nhiều ngữ cảnh, nhưng có nghĩa là dấu nháy đơn trong các dạng viết tắt và sở hữu cách tạo thành ranh giới từ, có thể không cho ra kết quả mong muốn::

        >>> b"they're bill's friends from the UK".title()
        b"They'Re Bill'S Friends From The Uk"

   Có thể xây dựng một giải pháp khắc phục cho dấu nháy đơn bằng cách sử dụng biểu thức chính quy::

        >>> import re
        >>> def titlecase(s):
        ...     return re.sub(rb"[A-Za-z]+('[A-Za-z]+)?",
        ...                   lambda mo: mo.group(0)[0:1].upper() +
        ...                              mo.group(0)[1:].lower(),
        ...                   s)
        ...
        >>> titlecase(b"they're bill's friends.")
        b"They're Bill's Friends."

   .. note::

      Phiên bản bytearray của phương thức này *không* hoạt động tại chỗ — nó luôn tạo ra một đối tượng mới, ngay cả khi không có thay đổi nào được thực hiện.


.. method:: bytes.upper()
            bytearray.upper()

   Trả về một bản sao của dãy với tất cả các ký tự ASCII chữ thường được chuyển đổi thành ký tự chữ hoa tương ứng.

   Ví dụ::

      >>> b'Hello World'.upper()
      b'HELLO WORLD'

   Ký tự ASCII viết thường là các giá trị byte trong chuỗi ``b'abcdefghijklmnopqrstuvwxyz'``. Ký tự ASCII viết hoa là các giá trị byte trong chuỗi ``b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'``.

   .. note::

      Phiên bản bytearray của phương thức này *không* hoạt động tại chỗ — nó luôn tạo ra một đối tượng mới, ngay cả khi không có thay đổi nào được thực hiện.


.. method:: bytes.zfill(width, /)
            bytearray.zfill(width, /)

   Trả về một bản sao của dãy được điền bên trái bằng các chữ số ASCII ``b'0'`` để tạo thành dãy có độ dài *width*. Tiền tố dấu đứng đầu (``b'+'``/ ``b'-'``) được xử lý bằng cách chèn phần đệm *sau* ký tự dấu thay vì trước nó. Đối với các đối tượng :class:`bytes`, dãy ban đầu được trả về nếu *width* nhỏ hơn hoặc bằng ``len(seq)``.

   Ví dụ::

      >>> b"42".zfill(5)
      b'00042'
      >>> b"-42".zfill(5)
      b'-0042'

   .. note::

      Phiên bản bytearray của phương thức này *không* hoạt động tại chỗ — nó luôn tạo ra một đối tượng mới, ngay cả khi không có thay đổi nào được thực hiện.


.. _bytes-formatting:

``printf``-style Định dạng Bytes
--------------------------------

.. index::
   single: formatting; bytes (%)
   single: formatting; bytearray (%)
   single: interpolation; bytes (%)
   single: interpolation; bytearray (%)
   single: bytes; formatting
   single: bytearray; formatting
   single: bytes; interpolation
   single: bytearray; interpolation
   single: printf-style formatting
   single: sprintf-style formatting
   single: % (percent); printf-style formatting

.. note::

   Các thao tác định dạng được mô tả ở đây có nhiều điểm đặc biệt, dẫn đến một số lỗi thường gặp (chẳng hạn như không hiển thị đúng tuple và dictionary). Nếu giá trị được in ra có thể là tuple hoặc dictionary, hãy bọc nó trong một tuple.

Các đối tượng bytes (``bytes``/``bytearray``) có một thao tác tích hợp duy nhất: toán tử ``%`` modulo. Đây còn được gọi là toán tử *định dạng* bytes hoặc toán tử *nội suy* bytes. Với ``format % values`` (trong đó *định dạng* là một đối tượng bytes), ``%`` các đặc tả chuyển đổi trong *định dạng* được thay thế bằng không hoặc nhiều phần tử của *giá trị*. Hiệu ứng này tương tự như việc sử dụng hàm :c:func:`sprintf` trong ngôn ngữ C.

Nếu *định dạng* yêu cầu một đối số duy nhất, *giá trị* có thể là một đối tượng duy nhất không phải tuple. [5]_  Nếu không, *giá trị* phải là một tuple có số lượng phần tử đúng bằng số lượng được chỉ định bởi đối tượng bytes định dạng hoặc là một đối tượng mapping duy nhất (ví dụ: một dictionary).

.. index::
   single: () (parentheses); in printf-style formatting
   single: * (asterisk); in printf-style formatting
   single: . (dot); in printf-style formatting

Một đặc tả chuyển đổi gồm hai ký tự trở lên và có các thành phần sau, phải xuất hiện theo thứ tự này:

#. Ký tự ``'%'``, đánh dấu phần bắt đầu của đặc tả.

#. Khóa ánh xạ (tùy chọn), gồm một chuỗi ký tự đặt trong dấu ngoặc đơn (ví dụ: ``(somename)``).

#. Các cờ chuyển đổi (tùy chọn), ảnh hưởng đến kết quả của một số kiểu chuyển đổi.

#. Độ rộng trường tối thiểu (tùy chọn). Nếu được chỉ định bằng ``'*'`` (dấu hoa thị), độ rộng thực tế sẽ được đọc từ phần tử tiếp theo của tuple trong *values*, còn đối tượng cần chuyển đổi nằm sau độ rộng trường tối thiểu và độ chính xác tùy chọn.

#. Độ chính xác (tùy chọn), được chỉ định bằng ``'.'`` (dấu chấm) theo sau là độ chính xác. Nếu được chỉ định bằng ``'*'`` (dấu hoa thị), độ chính xác thực tế sẽ được đọc từ phần tử tiếp theo của tuple trong *values*, còn giá trị cần chuyển đổi nằm sau độ chính xác.

#. Bổ nghĩa độ dài (tùy chọn).

#. Kiểu chuyển đổi.

Khi đối số bên phải là một dictionary (hoặc kiểu mapping khác), thì các định dạng trong đối tượng bytes *phải* bao gồm một khóa mapping đặt trong dấu ngoặc đơn của dictionary đó, được chèn ngay sau ký tự ``'%'``. Ví dụ:

   >>> print(b'%(language)s has %(number)03d quote types.' %
   ...       {b'language': b"Python", b"number": 2})
   b'Python has 002 quote types.'

Trong trường hợp này, không được xuất hiện các ``*`` specifier trong một định dạng (vì chúng yêu cầu một danh sách tham số tuần tự).

Các ký tự cờ chuyển đổi là:

.. index::
   single: # (hash); in printf-style formatting
   single: - (minus); in printf-style formatting
   single: + (plus); in printf-style formatting
   single: space; in printf-style formatting

+---------+-------------------------------------------------------------------------------------------------------------------------+
| Cờ      | Ý nghĩa                                                                                                                 |
+=========+=========================================================================================================================+
| ``'#'`` | Việc chuyển đổi giá trị sẽ sử dụng "alternate form" (dạng thay thế, như được định nghĩa bên dưới).                      |
+---------+-------------------------------------------------------------------------------------------------------------------------+
| ``'0'`` | Đối với các giá trị số, kết quả chuyển đổi sẽ được đệm bằng số 0.                                                       |
+---------+-------------------------------------------------------------------------------------------------------------------------+
| ``'-'`` | Giá trị đã chuyển đổi được căn trái (ghi đè chuyển đổi ``'0'`` nếu cả hai đều được cung cấp).                           |
+---------+-------------------------------------------------------------------------------------------------------------------------+
| ``' '`` | (một khoảng trắng) Một khoảng trắng sẽ được đặt trước số dương (hoặc chuỗi rỗng) được tạo ra bởi một chuyển đổi có dấu. |
+---------+-------------------------------------------------------------------------------------------------------------------------+
| ``'+'`` | Một ký tự dấu (``'+'`` hoặc ``'-'``) sẽ đứng trước phép chuyển đổi (ghi đè cờ "space").                                 |
+---------+-------------------------------------------------------------------------------------------------------------------------+

Một bộ sửa độ dài (``h``, ``l`` hoặc ``L``) có thể xuất hiện, nhưng bị bỏ qua vì không cần thiết đối với Python -- vì vậy, chẳng hạn, ``%ld`` giống hệt ``%d``.

Các kiểu chuyển đổi gồm:

+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| Chuyển đổi | Ý nghĩa                                                                                                                                                      | Ghi chú |
+============+==============================================================================================================================================================+=========+
| ``'d'``    | Số nguyên thập phân có dấu.                                                                                                                                  |         |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'i'``    | Số nguyên thập phân có dấu.                                                                                                                                  |         |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'o'``    | Giá trị bát phân có dấu.                                                                                                                                     | \(1)    |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'u'``    | Kiểu lỗi thời -- nó giống hệt ``'d'``.                                                                                                                       | \(8)    |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'x'``    | Hệ thập lục phân có dấu (chữ thường).                                                                                                                        | \(2)    |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'X'``    | Hệ thập lục phân có dấu (chữ hoa).                                                                                                                           | \(2)    |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'e'``    | Định dạng số mũ dấu phẩy động (chữ thường).                                                                                                                  | \(3)    |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'E'``    | Định dạng số mũ dấu phẩy động (chữ hoa).                                                                                                                     | \(3)    |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'f'``    | Định dạng thập phân dấu phẩy động.                                                                                                                           | \(3)    |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'F'``    | Định dạng thập phân dấu phẩy động.                                                                                                                           | \(3)    |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'g'``    | Định dạng dấu phẩy động. Sử dụng định dạng số mũ chữ thường nếu số mũ nhỏ hơn -4 hoặc không nhỏ hơn độ chính xác; nếu không thì sử dụng định dạng thập phân. | \(4)    |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'G'``    | Định dạng dấu phẩy động. Sử dụng định dạng số mũ chữ hoa nếu số mũ nhỏ hơn -4 hoặc không nhỏ hơn độ chính xác; nếu không thì sử dụng định dạng thập phân.    | \(4)    |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'c'``    | Một byte (chấp nhận số nguyên hoặc các đối tượng một byte).                                                                                                  |         |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'b'``    | Bytes (bất kỳ đối tượng nào tuân theo                                                                                                                        | \(5)    |
|            | :ref:`buffer protocol <bufferobjects>` hoặc có                                                                                                               |         |
|            | :meth:`~object.__bytes__`).                                                                                                                                  |         |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'s'``    | ``'s'`` là bí danh của ``'b'`` và chỉ nên được sử dụng cho các code base Python2/3.                                                                          | \(6)    |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'a'``    | Bytes (chuyển đổi mọi đối tượng Python bằng ``repr(obj).encode('ascii', 'backslashreplace')``).                                                              | \(5)    |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'r'``    | ``'r'`` là bí danh của ``'a'`` và chỉ nên được sử dụng cho các code base Python2/3.                                                                          | \(7)    |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+
| ``'%'``    | Không có đối số nào được chuyển đổi, kết quả là một ký tự ``'%'``.                                                                                           |         |
+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+---------+

Ghi chú:

(1)
   Dạng thay thế khiến một tiền tố bát phân (``'0o'``) được chèn trước chữ số đầu tiên.

(2)
   Dạng thay thế khiến một tiền tố ``'0x'`` hoặc ``'0X'`` (tùy thuộc vào việc sử dụng định dạng ``'x'`` hay ``'X'``) được chèn trước chữ số đầu tiên.

(3)
   Dạng thay thế khiến kết quả luôn chứa dấu thập phân, ngay cả khi không có chữ số nào theo sau.

   Độ chính xác xác định số chữ số sau dấu thập phân và mặc định là 6.

(4)
   Dạng thay thế khiến kết quả luôn chứa dấu thập phân và các số 0 ở cuối không bị loại bỏ như trong trường hợp thông thường.

   Độ chính xác xác định số chữ số có nghĩa trước và sau dấu thập phân và mặc định là 6.

(5)
   Nếu precision là ``N``, đầu ra sẽ bị cắt ngắn còn ``N`` ký tự.

(6)
   ``b'%s'`` đã lỗi thời nhưng sẽ không bị xóa trong dòng phiên bản 3.x.

(7)
   ``b'%r'`` đã lỗi thời nhưng sẽ không bị xóa trong dòng phiên bản 3.x.

(8)
   Xem :pep:`237`.

.. note::

   Phiên bản bytearray của phương thức này *không* thực hiện tại chỗ - nó luôn tạo một đối tượng mới, ngay cả khi không có thay đổi nào được thực hiện.

.. seealso::

   :pep:`461` - Thêm định dạng % vào bytes và bytearray

.. versionadded:: 3.5

.. _typememoryview:

Chế độ xem bộ nhớ
-----------------

Các đối tượng :class:`memoryview` cho phép mã Python truy cập dữ liệu nội bộ của một đối tượng hỗ trợ :ref:`buffer protocol <bufferobjects>` mà không cần sao chép.

.. class:: memoryview(object)

   Tạo một :class:`memoryview` tham chiếu đến *object*. *object* phải hỗ trợ buffer protocol. Các object tích hợp hỗ trợ buffer protocol bao gồm :class:`bytes` và :class:`bytearray`.

   Một :class:`memoryview` có khái niệm về một *element*, là đơn vị bộ nhớ nguyên tử được *object* ban đầu xử lý. Với nhiều kiểu đơn giản như :class:`bytes` và :class:`bytearray`, một element là một byte đơn, nhưng các kiểu khác như :class:`array.array` có thể có các element lớn hơn.

   :class:`!memoryview`\s là :ref:`generic <generics>` theo kiểu dữ liệu nền tảng của chúng.

   ``len(view)`` bằng độ dài của :meth:`~memoryview.tolist`, là biểu diễn danh sách lồng nhau của view. Nếu ``view.ndim == 1``, giá trị này bằng số element trong view.

   .. versionchanged:: 3.12
      Nếu ``view.ndim == 0``, ``len(view)`` giờ đây sẽ raise :exc:`TypeError` thay vì trả về 1.

   Thuộc tính :class:`~memoryview.itemsize` cho biết số byte trong một element đơn.

   Một :class:`memoryview` hỗ trợ slicing và indexing để hiển thị dữ liệu của nó. Slicing một chiều sẽ tạo ra một subview::

    >>> v = memoryview(b'abcefg')
    >>> v[1]
    98
    >>> v[-1]
    103
    >>> v[1:4]
    <memory at 0x7f3ddc9f4350>
    >>> bytes(v[1:4])
    b'bce'

   Nếu :class:`~memoryview.format` là một trong các bộ chỉ định định dạng gốc của mô-đun :mod:`struct`, thì việc lập chỉ mục bằng một số nguyên hoặc một tuple các số nguyên cũng được hỗ trợ và trả về một *phần tử* duy nhất với kiểu chính xác. memoryview một chiều có thể được lập chỉ mục bằng một số nguyên hoặc một tuple gồm một số nguyên. memoryview đa chiều có thể được lập chỉ mục bằng các tuple chứa đúng *ndim* số nguyên, trong đó *ndim* là số chiều. memoryview không chiều có thể được lập chỉ mục bằng tuple rỗng.

   Dưới đây là một ví dụ với định dạng không phải byte::

      >>> import array
      >>> a = array.array('l', [-11111111, 22222222, -33333333, 44444444])
      >>> m = memoryview(a)
      >>> m[0]
      -11111111
      >>> m[-1]
      44444444
      >>> m[::2].tolist()
      [-11111111, -33333333]

   Nếu đối tượng nền có thể ghi, memoryview hỗ trợ phép gán lát cắt một chiều. Không cho phép thay đổi kích thước::

      >>> data = bytearray(b'abcefg')
      >>> v = memoryview(data)
      >>> v.readonly
      False
      >>> v[0] = ord(b'z')
      >>> data
      bytearray(b'zbcefg')
      >>> v[1:4] = b'123'
      >>> data
      bytearray(b'z123fg')
      >>> v[2:3] = b'spam'
      Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
      ValueError: memoryview assignment: lvalue and rvalue have different structures
      >>> v[2:6] = b'spam'
      >>> data
      bytearray(b'z1spam')

   memoryview một chiều của các kiểu :term:`hashable` (chỉ đọc) với các định dạng 'B', 'b' hoặc 'c' cũng có thể băm được. Giá trị băm được định nghĩa là ``hash(m) == hash(m.tobytes())``::

      >>> v = memoryview(b'abcefg')
      >>> hash(v) == hash(b'abcefg')
      True
      >>> hash(v[2:4]) == hash(b'ce')
      True
      >>> hash(v[::-2]) == hash(b'abcefg'[::-2])
      True

   .. versionchanged:: 3.3
      Giờ đây, memoryview một chiều có thể được cắt lát. memoryview một chiều với các định dạng 'B', 'b' hoặc 'c' giờ đây là :term:`hashable`.

   .. versionchanged:: 3.4
      Giờ đây, memoryview được đăng ký tự động với
      :class:`collections.abc.Sequence`

   .. versionchanged:: 3.5
      Giờ đây, memoryview có thể được lập chỉ mục bằng một tuple các số nguyên.

   .. versionchanged:: 3.14
      memoryview hiện là một :term:`generic type`.

   :class:`memoryview` có một số phương thức:

   .. method:: __eq__(exporter)

      Một memoryview và một đối tượng exporter :pep:`3118` bằng nhau nếu hình dạng của chúng tương đương và tất cả các giá trị tương ứng đều bằng nhau khi các mã định dạng tương ứng của hai toán hạng được diễn giải bằng cú pháp :mod:`struct`.

      Đối với tập hợp con các chuỗi định dạng :mod:`struct` hiện được hỗ trợ bởi
      :meth:`tolist`, ``v`` và ``w`` bằng nhau nếu ``v.tolist() == w.tolist()``::

         >>> import array
         >>> a = array.array('I', [1, 2, 3, 4, 5])
         >>> b = array.array('d', [1.0, 2.0, 3.0, 4.0, 5.0])
         >>> c = array.array('b', [5, 3, 1])
         >>> x = memoryview(a)
         >>> y = memoryview(b)
         >>> x == a == y == b
         True
         >>> x.tolist() == a.tolist() == y.tolist() == b.tolist()
         True
         >>> z = y[::-2]
         >>> z == c
         True
         >>> z.tolist() == c.tolist()
         True

      Nếu một trong hai chuỗi định dạng không được mô-đun :mod:`struct` hỗ trợ, thì các đối tượng sẽ luôn được so sánh là không bằng nhau (ngay cả khi các chuỗi định dạng và nội dung bộ đệm giống hệt nhau)::

         >>> from ctypes import BigEndianStructure, c_long
         >>> class BEPoint(BigEndianStructure):
         ...     _fields_ = [("x", c_long), ("y", c_long)]
         ...
         >>> point = BEPoint(100, 200)
         >>> a = memoryview(point)
         >>> b = memoryview(point)
         >>> a == point
         False
         >>> a == b
         False

      Lưu ý rằng, cũng như với các số dấu phẩy động, ``v is w`` có *không* ngụ ý ``v == w`` đối với các đối tượng memoryview.

      .. versionchanged:: 3.3
         Các phiên bản trước đây so sánh vùng nhớ thô mà không xét đến định dạng phần tử và cấu trúc mảng logic.

   .. method:: tobytes(order='C')

      Trả về dữ liệu trong buffer dưới dạng chuỗi byte. Điều này tương đương với việc gọi hàm khởi tạo :class:`bytes` trên memoryview.::

         >>> m = memoryview(b"abc")
         >>> m.tobytes()
         b'abc'
         >>> bytes(m)
         b'abc'

      Đối với các mảng không liên tục, kết quả bằng biểu diễn danh sách đã làm phẳng, trong đó tất cả phần tử được chuyển đổi thành byte. :meth:`tobytes` hỗ trợ mọi chuỗi định dạng, bao gồm cả những chuỗi không có trong
      cú pháp mô-đun :mod:`struct`.

      .. versionadded:: 3.8
         *order* có thể là {'C', 'F', 'A'}. Khi *order* là 'C' hoặc 'F', dữ liệu của mảng ban đầu được chuyển đổi sang thứ tự C hoặc Fortran. Đối với các view liên tục, 'A' trả về một bản sao chính xác của vùng nhớ vật lý. Cụ thể, thứ tự Fortran trong bộ nhớ được giữ nguyên. Đối với các view không liên tục, dữ liệu trước tiên được chuyển đổi sang C. *order=None* tương đương với *order='C'*.

   .. method:: hex(*, bytes_per_sep=1)
               hex(sep, bytes_per_sep=1)

      Trả về một đối tượng chuỗi chứa hai chữ số thập lục phân cho mỗi byte trong buffer.::

         >>> m = memoryview(b"abc")
         >>> m.hex()
         '616263'

      .. versionadded:: 3.5

      .. versionchanged:: 3.8
         Tương tự như :meth:`bytes.hex`, :meth:`memoryview.hex` hiện hỗ trợ các tham số tùy chọn *sep* và *bytes_per_sep* để chèn dấu phân cách giữa các byte trong đầu ra hex.

   .. method:: tolist()

      Trả về dữ liệu trong bộ đệm dưới dạng danh sách các phần tử.::

         >>> memoryview(b'abc').tolist()
         [97, 98, 99]
         >>> import array
         >>> a = array.array('d', [1.1, 2.2, 3.3])
         >>> m = memoryview(a)
         >>> m.tolist()
         [1.1, 2.2, 3.3]

      .. versionchanged:: 3.3
         :meth:`tolist` now supports all single character native formats in
         :mod:`struct` module syntax as well as multi-dimensional
         các biểu diễn.

   .. method:: toreadonly()

      Trả về phiên bản chỉ đọc của đối tượng memoryview. Đối tượng memoryview ban đầu không bị thay đổi.::

         >>> m = memoryview(bytearray(b'abc'))
         >>> mm = m.toreadonly()
         >>> mm.tolist()
         [97, 98, 99]
         >>> mm[0] = 42
         Traceback (most recent call last):
           File "<stdin>", line 1, in <module>
         TypeError: cannot modify read-only memory
         >>> m[0] = 43
         >>> mm.tolist()
         [43, 98, 99]

      .. versionadded:: 3.8

   .. method:: release()

      Giải phóng bộ đệm bên dưới được đối tượng memoryview cung cấp. Nhiều đối tượng thực hiện các hành động đặc biệt khi có một view đang được giữ trên chúng (ví dụ: một :class:`bytearray` sẽ tạm thời không cho phép thay đổi kích thước); do đó, việc gọi release() rất hữu ích để loại bỏ các hạn chế này (và giải phóng mọi tài nguyên còn tồn đọng) sớm nhất có thể.

      Sau khi phương thức này được gọi, mọi thao tác tiếp theo trên view sẽ phát sinh :class:`ValueError` (ngoại trừ chính :meth:`release`, phương thức có thể được gọi nhiều lần)::

         >>> m = memoryview(b'abc')
         >>> m.release()
         >>> m[0]
         Traceback (most recent call last):
           File "<stdin>", line 1, in <module>
         ValueError: operation forbidden on released memoryview object

      Có thể sử dụng giao thức quản lý ngữ cảnh để đạt được hiệu ứng tương tự, bằng cách sử dụng câu lệnh ``with``::

         >>> with memoryview(b'abc') as m:
         ...     m[0]
         ...
         97
         >>> m[0]
         Traceback (most recent call last):
           File "<stdin>", line 1, in <module>
         ValueError: operation forbidden on released memoryview object

      .. versionadded:: 3.2

   .. method:: cast(format, /)
               cast(format, shape, /)

      Chuyển một memoryview sang format hoặc shape mới. *shape* mặc định là ``[byte_length//new_itemsize]``, nghĩa là view kết quả sẽ có một chiều. Giá trị trả về là một memoryview mới, nhưng bản thân buffer không được sao chép. Các phép chuyển kiểu được hỗ trợ là 1D -> C-:term:`contiguous` và C-contiguous -> 1D.

      Format đích bị giới hạn ở một native format gồm một phần tử trong
      cú pháp :mod:`struct`. Một trong các format phải là byte format ('B', 'b' hoặc 'c'). Độ dài byte của kết quả phải bằng độ dài ban đầu. Lưu ý rằng mọi độ dài byte đều có thể phụ thuộc vào hệ điều hành.

      Chuyển 1D/long thành 1D/unsigned bytes::

         >>> import array
         >>> a = array.array('l', [1,2,3])
         >>> x = memoryview(a)
         >>> x.format
         'l'
         >>> x.itemsize
         8
         >>> len(x)
         3
         >>> x.nbytes
         24
         >>> y = x.cast('B')
         >>> y.format
         'B'
         >>> y.itemsize
         1
         >>> len(y)
         24
         >>> y.nbytes
         24

      Chuyển 1D/unsigned bytes thành 1D/char::

         >>> b = bytearray(b'zyz')
         >>> x = memoryview(b)
         >>> x[0] = b'a'
         Traceback (most recent call last):
           ...
         TypeError: memoryview: invalid type for format 'B'
         >>> y = x.cast('c')
         >>> y[0] = b'a'
         >>> b
         bytearray(b'ayz')

      Chuyển 1D/bytes thành 3D/ints thành 1D/signed char::

         >>> import struct
         >>> buf = struct.pack("i"*12, *list(range(12)))
         >>> x = memoryview(buf)
         >>> y = x.cast('i', shape=[2,2,3])
         >>> y.tolist()
         [[[0, 1, 2], [3, 4, 5]], [[6, 7, 8], [9, 10, 11]]]
         >>> y.format
         'i'
         >>> y.itemsize
         4
         >>> len(y)
         2
         >>> y.nbytes
         48
         >>> z = y.cast('b')
         >>> z.format
         'b'
         >>> z.itemsize
         1
         >>> len(z)
         48
         >>> z.nbytes
         48

      Ép kiểu 1D/unsigned long sang 2D/unsigned long::

         >>> buf = struct.pack("L"*6, *list(range(6)))
         >>> x = memoryview(buf)
         >>> y = x.cast('L', shape=[2,3])
         >>> len(y)
         2
         >>> y.nbytes
         48
         >>> y.tolist()
         [[0, 1, 2], [3, 4, 5]]

      .. versionadded:: 3.3

      .. versionchanged:: 3.5
         Định dạng nguồn không còn bị giới hạn khi ép kiểu sang chế độ xem byte.

   .. method:: count(value, /)

      Đếm số lần xuất hiện của *value*.

      .. versionadded:: 3.14

  .. method:: index(value, start=0, stop=sys.maxsize, /)

      Trả về chỉ mục của lần xuất hiện đầu tiên của *value* (tại hoặc sau chỉ mục *start* và trước chỉ mục *stop*).

      Phát sinh một :exc:`ValueError` nếu không tìm thấy *value*.

      .. versionadded:: 3.14

   Ngoài ra, có một số thuộc tính chỉ đọc:

   .. attribute:: obj

      Đối tượng nền tảng của memoryview::

         >>> b  = bytearray(b'xyz')
         >>> m = memoryview(b)
         >>> m.obj is b
         True

      .. versionadded:: 3.3

   .. attribute:: nbytes

      ``nbytes == product(shape) * itemsize == len(m.tobytes())``. Đây là lượng không gian tính bằng byte mà mảng sẽ sử dụng trong biểu diễn liên tục. Lượng này không nhất thiết bằng ``len(m)``::

         >>> import array
         >>> a = array.array('i', [1,2,3,4,5])
         >>> m = memoryview(a)
         >>> len(m)
         5
         >>> m.nbytes
         20
         >>> y = m[::2]
         >>> len(y)
         3
         >>> y.nbytes
         12
         >>> len(y.tobytes())
         12

      Mảng đa chiều::

         >>> import struct
         >>> buf = struct.pack("d"*12, *[1.5*x for x in range(12)])
         >>> x = memoryview(buf)
         >>> y = x.cast('d', shape=[3,4])
         >>> y.tolist()
         [[0.0, 1.5, 3.0, 4.5], [6.0, 7.5, 9.0, 10.5], [12.0, 13.5, 15.0, 16.5]]
         >>> len(y)
         3
         >>> y.nbytes
         96

      .. versionadded:: 3.3

   .. attribute:: readonly

      Một giá trị bool cho biết bộ nhớ có chỉ đọc hay không.

   .. attribute:: format

      Một chuỗi chứa format (theo kiểu mô-đun :mod:`struct`) cho từng phần tử trong view. Có thể tạo memoryview từ các exporter với các chuỗi format tùy ý, nhưng một số phương thức (ví dụ: :meth:`tolist`) bị giới hạn ở các format phần tử đơn native.

      .. versionchanged:: 3.3
         format ``'B'`` hiện được xử lý theo cú pháp của mô-đun struct. Điều này có nghĩa là ``memoryview(b'abc')[0] == b'abc'[0] == 97``.

   .. attribute:: itemsize

      Kích thước tính bằng byte của mỗi phần tử trong memoryview::

         >>> import array, struct
         >>> m = memoryview(array.array('H', [32000, 32001, 32002]))
         >>> m.itemsize
         2
         >>> m[0]
         32000
         >>> struct.calcsize('H') == m.itemsize
         True

   .. attribute:: ndim

      Một số nguyên cho biết bộ nhớ biểu diễn bao nhiêu chiều của một mảng đa chiều.

   .. attribute:: shape

      Một tuple gồm các số nguyên có độ dài :attr:`ndim`, biểu thị hình dạng của vùng nhớ dưới dạng một mảng N chiều.

      .. versionchanged:: 3.3
         Một tuple rỗng thay cho ``None`` khi ndim = 0.

   .. attribute:: strides

      Một tuple gồm các số nguyên có độ dài :attr:`ndim`, biểu thị kích thước tính bằng byte để truy cập từng phần tử theo mỗi chiều của mảng.

      .. versionchanged:: 3.3
         Một tuple rỗng thay cho ``None`` khi ndim = 0.

   .. attribute:: suboffsets

      Được sử dụng nội bộ cho các mảng kiểu PIL. Giá trị này chỉ mang tính thông tin.

   .. attribute:: c_contiguous

      Một bool cho biết vùng nhớ có :term:`contiguous` theo kiểu C hay không.

      .. versionadded:: 3.3

   .. attribute:: f_contiguous

      Một bool cho biết vùng nhớ có :term:`contiguous` theo kiểu Fortran hay không.

      .. versionadded:: 3.3

   .. attribute:: contiguous

      Một bool cho biết bộ nhớ có :term:`contiguous` hay không.

      .. versionadded:: 3.3

Để biết thông tin về tính an toàn luồng của các đối tượng :class:`memoryview` trong :term:`free-threaded build`, hãy xem :ref:`thread-safety-memoryview`.


.. _types-set:

Các kiểu tập hợp --- :class:`set`, :class:`frozenset`
=====================================================

.. index:: pair: object; set

Một đối tượng :dfn:`set` là một tập hợp không có thứ tự gồm các đối tượng :term:`hashable` khác nhau. Các cách sử dụng phổ biến gồm kiểm tra phần tử, loại bỏ các phần tử trùng lặp khỏi một dãy và thực hiện các phép toán trong toán học như giao, hợp, hiệu và hiệu đối xứng. (Đối với các container khác, hãy xem các lớp tích hợp sẵn :class:`dict`, :class:`list` và :class:`tuple`, cùng với module :mod:`collections`.) Xem :ref:`time-complexity` để biết chi phí của các phép toán tập hợp khác nhau.

Giống như các collection khác, tập hợp hỗ trợ ``x in set``, ``len(set)`` và ``for x in set``. Vì là một collection không có thứ tự, tập hợp không ghi lại vị trí của phần tử hoặc thứ tự chèn. Do đó, tập hợp không hỗ trợ lập chỉ mục, cắt lát hoặc các hành vi tương tự sequence khác.

Hiện có hai kiểu tập hợp tích hợp sẵn là :class:`set` và :class:`frozenset`. Kiểu :class:`set` có thể thay đổi --- nội dung có thể được thay đổi bằng các method như :meth:`~set.add` và :meth:`~set.remove`. Vì có thể thay đổi, kiểu này không có giá trị hash và không thể được dùng làm khóa dictionary hoặc làm phần tử của một tập hợp khác. Kiểu :class:`frozenset` là bất biến và :term:`hashable` --- nội dung không thể được thay đổi sau khi tạo; vì vậy, kiểu này có thể được dùng làm khóa dictionary hoặc làm phần tử của một tập hợp khác.

Có thể tạo các tập hợp không rỗng (không phải frozenset) bằng cách đặt một danh sách các phần tử được phân tách bằng dấu phẩy trong dấu ngoặc nhọn, ví dụ: ``{'jack', 'sjoerd'}``, ngoài ra còn
:class:`set` hàm khởi tạo.

Các hàm khởi tạo của cả hai lớp hoạt động giống nhau:

.. class:: set(iterable=(), /)
           frozenset(iterable=(), /)

   Trả về một đối tượng set hoặc frozenset mới, với các phần tử được lấy từ *iterable*. Các phần tử của một set phải :term:`hashable`. Để biểu diễn các set của các set, các set bên trong phải là :class:`frozenset` đối tượng frozenset. Nếu không chỉ định *iterable*, một set rỗng mới sẽ được trả về.

Có thể tạo set bằng một số cách:

* Sử dụng danh sách các phần tử được phân tách bằng dấu phẩy trong dấu ngoặc nhọn: ``{'jack', 'sjoerd'}``
* Sử dụng set comprehension: ``{c for c in 'abracadabra' if c not in 'abc'}``
* Sử dụng hàm khởi tạo kiểu: ``set()``, ``set('foobar')``, ``set(['a', 'b', 'foo'])``

Các instance của :class:`set` và :class:`frozenset` cung cấp các phép toán sau:

.. describe:: len(s)

   Trả về số phần tử trong tập hợp *s* (lực lượng của *s*).

.. describe:: x in s

   Kiểm tra *x* có thuộc *s* hay không.

.. describe:: x not in s

   Kiểm tra *x* không thuộc *s*.

.. method:: frozenset.isdisjoint(other, /)
            set.isdisjoint(other, /)

   Trả về ``True`` nếu tập hợp không có phần tử chung với *other*. Hai tập hợp rời nhau khi và chỉ khi giao của chúng là tập hợp rỗng.

.. method:: frozenset.issubset(other, /)
            set.issubset(other, /)
.. describe:: set <= other

   Kiểm tra xem mọi phần tử trong tập hợp có nằm trong *other* hay không.

.. describe:: set < other

   Kiểm tra xem tập hợp có phải là tập con thực sự của *other* hay không, tức là ``set <= other and set != other``.

.. method:: frozenset.issuperset(other, /)
            set.issuperset(other, /)
.. describe:: set >= other

   Kiểm tra xem mọi phần tử trong *other* có nằm trong tập hợp hay không.

.. describe:: set > other

   Kiểm tra xem tập hợp có phải là tập cha thực sự của *other* hay không, tức là ``set >= other and set != other``.

.. method:: frozenset.union(*others)
            set.union(*others)
.. describe:: set | other | ...

   Trả về một tập hợp mới chứa các phần tử của tập hợp này và tất cả các tập hợp khác.

.. method:: frozenset.intersection(*others)
            set.intersection(*others)
.. describe:: set & other & ...

   Trả về một tập hợp mới chứa các phần tử chung của tập hợp này và tất cả các tập hợp khác.

.. method:: frozenset.difference(*others)
            set.difference(*others)
.. describe:: set - other - ...

   Trả về một tập hợp mới chứa các phần tử có trong tập hợp này nhưng không có trong các tập hợp khác.

.. method:: frozenset.symmetric_difference(other, /)
            set.symmetric_difference(other, /)
.. describe:: set ^ other

   Trả về một tập hợp mới chứa các phần tử có trong tập hợp này hoặc *other* nhưng không có trong cả hai.

.. method:: frozenset.copy()
            set.copy()

   Trả về một bản sao nông của tập hợp.


Lưu ý rằng các phiên bản không phải toán tử của :meth:`~frozenset.union`,
:meth:`~frozenset.intersection`, :meth:`~frozenset.difference`, :meth:`~frozenset.symmetric_difference`, :meth:`~frozenset.issubset`, và
các phương thức :meth:`~frozenset.issuperset` sẽ chấp nhận mọi iterable làm đối số. Ngược lại, các phiên bản dựa trên toán tử của chúng yêu cầu đối số phải là các tập hợp. Điều này loại bỏ những cách viết dễ gây lỗi như ``set('abc') & 'cbs'`` để dùng cách viết dễ đọc hơn là ``set('abc').intersection('cbs')``.

Cả :class:`set` và :class:`frozenset` đều hỗ trợ so sánh tập hợp với tập hợp. Hai tập hợp bằng nhau khi và chỉ khi mọi phần tử của mỗi tập hợp đều nằm trong tập hợp kia (mỗi tập hợp là tập con của tập hợp còn lại). Một tập hợp nhỏ hơn tập hợp khác khi và chỉ khi tập hợp đầu tiên là tập con thực sự của tập hợp thứ hai (là tập con nhưng không bằng nhau). Một tập hợp lớn hơn tập hợp khác khi và chỉ khi tập hợp đầu tiên là tập cha thực sự của tập hợp thứ hai (là tập cha nhưng không bằng nhau).

Các thể hiện của :class:`set` được so sánh với các thể hiện của :class:`frozenset` dựa trên các phần tử của chúng. Ví dụ, ``set('abc') == frozenset('abc')`` trả về ``True`` và ``set('abc') in set([frozenset('abc')])`` cũng vậy.

Các phép so sánh tập con và bằng nhau không tổng quát hóa thành một hàm sắp thứ tự toàn phần. Ví dụ, hai tập hợp khác rỗng và không giao nhau bất kỳ đều không bằng nhau và không là tập con của nhau, vì vậy *all* các phép so sánh sau đều trả về ``False``: ``a<b``, ``a==b`` hoặc ``a>b``.

Vì các tập hợp chỉ xác định thứ tự bộ phận (mối quan hệ tập con), kết quả của phương thức :meth:`list.sort` không được xác định đối với các danh sách chứa tập hợp.

Các phần tử của tập hợp, cũng như các khóa từ điển, phải :term:`hashable`.

Các phép toán nhị phân kết hợp các đối tượng :class:`set` với :class:`frozenset` trả về kiểu của toán hạng đầu tiên. Ví dụ: ``frozenset('ab') | set('bc')`` trả về một đối tượng thuộc kiểu :class:`frozenset`.

Bảng sau liệt kê các phép toán có sẵn cho :class:`set` nhưng không áp dụng cho các đối tượng bất biến :class:`frozenset`:

.. method:: set.update(*others)
.. describe:: set |= other | ...

   Cập nhật tập hợp, thêm các phần tử từ tất cả các tập hợp khác.

.. method:: set.intersection_update(*others)
.. describe:: set &= other & ...

   Cập nhật tập hợp, chỉ giữ lại các phần tử có trong tập hợp đó và tất cả các tập hợp khác.

.. method:: set.difference_update(*others)
.. describe:: set -= other | ...

   Cập nhật set, loại bỏ các phần tử có trong các set khác.

.. method:: set.symmetric_difference_update(other, /)
.. describe:: set ^= other

   Cập nhật set, chỉ giữ lại các phần tử có trong một trong hai set nhưng không có trong cả hai.

.. method:: set.add(elem, /)

   Thêm phần tử *elem* vào set.

.. method:: set.remove(elem, /)

   Xóa phần tử *elem* khỏi set.  Phát sinh :exc:`KeyError` nếu *elem* không nằm trong set.

.. method:: set.discard(elem, /)

   Xóa phần tử *elem* khỏi set nếu phần tử đó tồn tại.

.. method:: set.pop()

   Xóa và trả về một phần tử bất kỳ từ set.  Phát sinh
   :exc:`KeyError` nếu set trống.

.. method:: set.clear()

   Xóa tất cả phần tử khỏi set.


Lưu ý rằng các phiên bản không phải toán tử của :meth:`~set.update`,
:meth:`~set.intersection_update`, :meth:`~set.difference_update` và
các phương thức :meth:`~set.symmetric_difference_update` sẽ chấp nhận bất kỳ iterable nào làm đối số.

Lưu ý rằng đối số *elem* của :meth:`~object.__contains__`,
:meth:`~set.remove` và
các phương thức :meth:`~set.discard` có thể là một set. Để hỗ trợ việc tìm kiếm một frozenset tương đương, một frozenset tạm thời được tạo từ *elem*.

.. seealso::

   Để biết thông tin chi tiết về các bảo đảm an toàn luồng cho các đối tượng :class:`set`, hãy xem :ref:`thread-safety-set`.

   Set và frozenset là :ref:`generic <generics>` theo kiểu của các phần tử trong chúng.


.. _typesmapping:

Kiểu ánh xạ --- :class:`dict`
=============================

.. index::
   pair: object; mapping
   pair: object; dictionary
   triple: operations on; mapping; types
   triple: operations on; dictionary; type
   pair: statement; del
   pair: built-in function; len

Một đối tượng :term:`mapping` ánh xạ các giá trị :term:`hashable` tới những đối tượng bất kỳ. Các ánh xạ là những đối tượng có thể thay đổi. Hiện tại chỉ có một kiểu ánh xạ tiêu chuẩn, đó là :dfn:`dictionary`. (Để xem các container khác, hãy xem các
:class:`list`, :class:`set`, và các lớp :class:`tuple`, cùng với
:mod:`collections` module.) Hãy xem :ref:`time-complexity` để biết chi phí của các thao tác dictionary khác nhau.

Các khóa của dictionary là *almost* những giá trị bất kỳ. Các giá trị không
:term:`hashable`, tức là, các giá trị chứa danh sách, từ điển hoặc các kiểu mutable khác (được so sánh theo giá trị thay vì theo identity của đối tượng) không thể được dùng làm khóa. Các giá trị được so sánh là bằng nhau (chẳng hạn như ``1``, ``1.0`` và ``True``) có thể được dùng thay thế cho nhau để truy cập cùng một mục trong từ điển.

.. class:: dict(**kwargs)
           dict(mapping, /, ****kwargs) dict(iterable, /, ****kwargs)

   Trả về một từ điển mới được khởi tạo từ một đối số vị trí tùy chọn và một tập keyword argument có thể rỗng.

   Có thể tạo từ điển bằng một số cách:

   * Dùng danh sách các cặp ``key: value`` được phân tách bằng dấu phẩy trong dấu ngoặc nhọn: ``{'jack': 4098, 'sjoerd': 4127}`` hoặc ``{4098: 'jack', 4127: 'sjoerd'}``
   * Dùng dict comprehension: ``{}``, ``{x: x ** 2 for x in range(10)}``
   * Dùng type constructor: ``dict()``, ``dict([('foo', 100), ('bar', 200)])``, ``dict(foo=100, bar=200)``

   Nếu không cung cấp đối số vị trí, một từ điển rỗng sẽ được tạo. Nếu cung cấp đối số vị trí và đối số đó định nghĩa phương thức ``keys()``, một từ điển sẽ được tạo bằng cách gọi :meth:`~object.__getitem__` trên đối số đó với từng khóa được phương thức trả về. Nếu không, đối số vị trí phải là một
   đối tượng :term:`iterable`. Mỗi mục trong đối tượng có thể lặp phải tự nó là một đối tượng có thể lặp gồm chính xác hai phần tử. Phần tử đầu tiên của mỗi mục trở thành khóa trong từ điển mới, còn phần tử thứ hai trở thành giá trị tương ứng. Nếu một khóa xuất hiện nhiều hơn một lần, giá trị cuối cùng của khóa đó sẽ trở thành giá trị tương ứng trong từ điển mới.

   Nếu cung cấp các đối số từ khóa, các đối số từ khóa và giá trị của chúng sẽ được thêm vào từ điển được tạo từ đối số vị trí. Nếu một khóa đang được thêm đã tồn tại, giá trị từ đối số từ khóa sẽ thay thế giá trị từ đối số vị trí.

   Hai từ điển được xem là bằng nhau khi và chỉ khi chúng có cùng các cặp ``(key, value)`` (không phụ thuộc vào thứ tự). Các phép so sánh thứ tự ('<', '<=', '>=', '>') sẽ gây ra
   :exc:`TypeError`. Để minh họa việc tạo từ điển và phép so sánh bằng nhau, tất cả các ví dụ sau đều trả về một từ điển bằng ``{"one": 1, "two": 2, "three": 3}``::

      >>> a = dict(one=1, two=2, three=3)
      >>> b = {'one': 1, 'two': 2, 'three': 3}
      >>> c = dict(zip(['one', 'two', 'three'], [1, 2, 3]))
      >>> d = dict([('two', 2), ('one', 1), ('three', 3)])
      >>> e = dict({'three': 3, 'one': 1, 'two': 2})
      >>> f = dict({'one': 1, 'three': 3}, two=2)
      >>> a == b == c == d == e == f
      True

   Việc cung cấp các đối số từ khóa như trong ví dụ đầu tiên chỉ áp dụng được cho các khóa là định danh Python hợp lệ. Nếu không, có thể sử dụng mọi khóa hợp lệ.

   Từ điển giữ nguyên thứ tự chèn. Lưu ý rằng việc cập nhật một khóa không ảnh hưởng đến thứ tự. Các khóa được thêm sau khi xóa sẽ được chèn vào cuối.::

      >>> d = {"one": 1, "two": 2, "three": 3, "four": 4}
      >>> d
      {'one': 1, 'two': 2, 'three': 3, 'four': 4}
      >>> list(d)
      ['one', 'two', 'three', 'four']
      >>> list(d.values())
      [1, 2, 3, 4]
      >>> d["one"] = 42
      >>> d
      {'one': 42, 'two': 2, 'three': 3, 'four': 4}
      >>> del d["two"]
      >>> d["two"] = None
      >>> d
      {'one': 42, 'three': 3, 'four': 4, 'two': None}

   .. versionchanged:: 3.7
      Thứ tự của từ điển được đảm bảo là thứ tự chèn. Hành vi này là một chi tiết triển khai của CPython từ phiên bản 3.6.

   Từ điển là :ref:`generic <generics>` trên hai kiểu, lần lượt biểu thị kiểu của các khóa và giá trị trong từ điển.

   Đây là các thao tác mà từ điển hỗ trợ (và do đó, các kiểu ánh xạ tùy chỉnh cũng nên hỗ trợ):

   .. describe:: list(d)

      Trả về danh sách tất cả các khóa được sử dụng trong từ điển *d*.

   .. describe:: len(d)

      Trả về số lượng mục trong từ điển *d*.

   .. describe:: d[key]

      Trả về mục của *d* có khóa *key*. Gây ra một :exc:`KeyError` nếu *key* không có trong ánh xạ.

      .. index:: __missing__()

      Nếu một lớp con của dict định nghĩa một phương thức :meth:`~object.__missing__` và *key* không tồn tại, thao tác ``d[key]`` sẽ gọi phương thức đó với khóa *key* làm đối số. Sau đó, thao tác ``d[key]`` trả về hoặc gây ra bất kỳ giá trị nào được trả về hoặc lỗi nào được gây ra bởi lệnh gọi ``__missing__(key)``. Không có thao tác hoặc phương thức nào khác gọi :meth:`~object.__missing__`. Nếu
      :meth:`~object.__missing__` chưa được định nghĩa, :exc:`KeyError` được phát sinh.
      :meth:`~object.__missing__` phải là một method; nó không thể là một biến instance::

          >>> class Counter(dict):
          ...     def __missing__(self, key):
          ...         return 0
          ...
          >>> c = Counter()
          >>> c['red']
          0
          >>> c['red'] += 1
          >>> c['red']
          1

      Ví dụ trên cho thấy một phần cách triển khai của
      :class:`collections.Counter`. :meth:`!__missing__` method khác được :class:`collections.defaultdict` sử dụng.

   .. describe:: d[key] = value

      Gán ``d[key]`` thành *value*.

   .. describe:: del d[key]

      Xóa ``d[key]`` khỏi *d*. Phát sinh một :exc:`KeyError` nếu *key* không có trong map.

   .. describe:: key in d

      Trả về ``True`` nếu *d* có khóa *key*, nếu không thì ``False``.

   .. describe:: key not in d

      Tương đương với ``not key in d``.

   .. describe:: iter(d)

      Trả về một iterator trên các khóa của từ điển. Đây là cách viết tắt của ``iter(d.keys())``.

   .. method:: clear()

      Xóa tất cả các mục khỏi từ điển.

   .. method:: copy()

      Trả về một bản sao nông của từ điển.

   .. classmethod:: fromkeys(iterable, value=None, /)

      Tạo một từ điển mới với các khóa từ *iterable* và các giá trị được đặt thành *value*.

      :meth:`fromkeys` là một class method trả về một từ điển mới. *value* mặc định là ``None``. Tất cả các giá trị đều tham chiếu đến cùng một instance, vì vậy thông thường không nên để *value* là một đối tượng có thể thay đổi như một danh sách rỗng. Để nhận các giá trị riêng biệt, hãy sử dụng :ref:`dict comprehension <dict>` thay thế.

   .. method:: get(key, default=None, /)

      Trả về giá trị của *key* nếu *key* có trong từ điển; nếu không thì trả về *default*. Nếu không cung cấp *default*, giá trị mặc định là ``None``, để phương thức này không bao giờ phát sinh :exc:`KeyError`.

   .. method:: items()

      Trả về một view mới của các mục trong dictionary (``(key, value)`` cặp). Xem :ref:`tài liệu về các đối tượng view <dict-views>`.

   .. method:: keys()

      Trả về một view mới của các khóa trong dictionary. Xem :ref:`tài liệu về các đối tượng view <dict-views>`.

   .. method:: pop(key, /)
               pop(key, default, /)

      Nếu *key* có trong dictionary, hãy xóa nó và trả về giá trị của nó; nếu không, trả về *default*. Nếu không cung cấp *default* và *key* không có trong dictionary, một :exc:`KeyError` sẽ được phát sinh.

   .. method:: popitem()

      Xóa và trả về một ``(key, value)`` cặp từ dictionary. Các cặp được trả về theo thứ tự :abbr:`LIFO (vào sau, ra trước)`.

      :meth:`popitem` hữu ích để lặp qua dictionary theo cách làm thay đổi trực tiếp dictionary, như thường được dùng trong các thuật toán tập hợp. Nếu dictionary trống, việc gọi
      :meth:`popitem` sẽ phát sinh một :exc:`KeyError`.

      .. versionchanged:: 3.7
         Thứ tự LIFO hiện đã được đảm bảo. Trong các phiên bản trước, :meth:`popitem` sẽ trả về một cặp khóa/giá trị bất kỳ.

   .. describe:: reversed(d)

      Trả về một trình lặp ngược qua các khóa của từ điển. Đây là cách viết tắt của ``reversed(d.keys())``.

      .. versionadded:: 3.8

   .. method:: setdefault(key, default=None, /)

      Nếu *key* có trong từ điển, hãy trả về giá trị của nó. Nếu không, chèn *key* với giá trị là *default* rồi trả về *default*. *default* mặc định là ``None``.

   .. method:: update(**kwargs)
               update(mapping, /, ****kwargs) update(iterable, /, ****kwargs)

      Cập nhật từ điển bằng các cặp khóa/giá trị từ *mapping* hoặc *iterable* và *kwargs*, ghi đè các khóa hiện có. Trả về ``None``.

      :meth:`update` chấp nhận một đối tượng khác có phương thức ``keys()`` (trong trường hợp đó, :meth:`~object.__getitem__` được gọi với từng khóa mà phương thức trả về) hoặc một iterable gồm các cặp khóa/giá trị (dưới dạng tuple hoặc các iterable khác có độ dài là hai). Nếu có chỉ định các đối số từ khóa, sau đó từ điển sẽ được cập nhật bằng các cặp khóa/giá trị đó: ``d.update(red=1, blue=2)``.

   .. method:: values()

      Trả về một view mới của các giá trị trong từ điển. Xem
      :ref:`tài liệu về các đối tượng view <dict-views>`.

      Phép so sánh bằng giữa một ``dict.values()`` view và một view khác sẽ luôn trả về ``False``. Điều này cũng áp dụng khi so sánh ``dict.values()`` với chính nó::

         >>> d = {'a': 1}
         >>> d.values() == d.values()
         False

   .. describe:: d | other

      Tạo một dictionary mới với các khóa và giá trị được hợp nhất của *d* và *other*, cả hai đều phải là dictionary. Các giá trị của *other* được ưu tiên khi *d* và *other* có chung khóa.

      .. versionadded:: 3.9

   .. describe:: d |= other

      Cập nhật dictionary *d* bằng các khóa và giá trị từ *other*, có thể là một :term:`mapping` hoặc một :term:`iterable` gồm các cặp khóa/giá trị. Các giá trị của *other* được ưu tiên khi *d* và *other* có chung khóa.

      .. versionadded:: 3.9

   Dictionary và dictionary view có thể đảo ngược.::

      >>> d = {"one": 1, "two": 2, "three": 3, "four": 4}
      >>> d
      {'one': 1, 'two': 2, 'three': 3, 'four': 4}
      >>> list(reversed(d))
      ['four', 'three', 'two', 'one']
      >>> list(reversed(d.values()))
      [4, 3, 2, 1]
      >>> list(reversed(d.items()))
      [('four', 4), ('three', 3), ('two', 2), ('one', 1)]

   .. versionchanged:: 3.8
      Dictionary hiện có thể đảo ngược.


.. seealso::
   :class:`types.MappingProxyType` can be used to create a read-only view
   của một :class:`dict`.


.. seealso::

   Để biết thông tin chi tiết về các đảm bảo an toàn luồng đối với các đối tượng :class:`dict`, hãy xem :ref:`thread-safety-dict`.


.. _dict-views:

Các đối tượng view của từ điển
------------------------------

Các đối tượng được trả về bởi :meth:`dict.keys`, :meth:`dict.values` và
:meth:`dict.items` là *các đối tượng view*. Chúng cung cấp một chế độ xem động đối với các mục nhập của từ điển, nghĩa là khi từ điển thay đổi, chế độ xem cũng phản ánh những thay đổi đó.

Có thể lặp qua các chế độ xem từ điển để lấy dữ liệu tương ứng của chúng và thực hiện các phép kiểm tra thành viên:

.. describe:: len(dictview)

   Trả về số lượng mục nhập trong từ điển.

.. describe:: iter(dictview)

   Trả về một iterator trên các khóa, giá trị hoặc mục (được biểu diễn dưới dạng các tuple của ``(key, value)``) trong từ điển.

   Các khóa và giá trị được lặp theo thứ tự chèn. Điều này cho phép tạo các cặp ``(value, key)`` bằng :func:`zip`: ``pairs = zip(d.values(), d.keys())``. Một cách khác để tạo cùng danh sách là ``pairs = [(v, k) for (k, v) in d.items()]``.

   Việc lặp qua các view trong khi thêm hoặc xóa mục trong dictionary có thể gây ra :exc:`RuntimeError` hoặc khiến quá trình lặp không duyệt qua tất cả các mục.

   .. versionchanged:: 3.7
      Thứ tự của dictionary được đảm bảo là thứ tự chèn.

.. describe:: x in dictview

   Trả về ``True`` nếu *x* nằm trong các khóa, giá trị hoặc mục của dictionary bên dưới (trong trường hợp sau, *x* phải là một tuple ``(key, value)``).

.. describe:: reversed(dictview)

   Trả về một iterator ngược qua các khóa, giá trị hoặc mục của dictionary. View sẽ được lặp theo thứ tự ngược với thứ tự chèn.

   .. versionchanged:: 3.8
      Các view của dictionary hiện có thể được duyệt ngược.

.. describe:: dictview.mapping

   Trả về một :class:`types.MappingProxyType` bao bọc dictionary ban đầu mà view tham chiếu đến.

   .. versionadded:: 3.10

Các view khóa có tính chất giống tập hợp vì các phần tử của chúng là duy nhất và :term:`hashable`. Các view mục cũng hỗ trợ các phép toán giống tập hợp vì các cặp (khóa, giá trị) là duy nhất và các khóa có thể băm được. Nếu tất cả các giá trị trong một view mục cũng có thể băm được, thì view mục đó có thể tương tác với các tập hợp khác. (Các view giá trị không được xem là giống tập hợp vì các phần tử nhìn chung không duy nhất.) Đối với các view giống tập hợp, tất cả các phép toán được định nghĩa cho lớp cơ sở trừu tượng :class:`collections.abc.Set` đều khả dụng (ví dụ: ``==``, ``<`` hoặc ``^``). Khi sử dụng các toán tử tập hợp, các view giống tập hợp chấp nhận bất kỳ iterable nào làm toán hạng còn lại, không giống các tập hợp vốn chỉ chấp nhận các tập hợp làm đầu vào.

Ví dụ về cách sử dụng view từ điển::

   >>> dishes = {'eggs': 2, 'sausage': 1, 'bacon': 1, 'spam': 500}
   >>> keys = dishes.keys()
   >>> values = dishes.values()

   >>> # lặp
   >>> n = 0
   >>> for val in values:
   ...     n += val
   ...
   >>> print(n)
   504

   >>> # khóa và giá trị được lặp theo cùng một thứ tự (thứ tự chèn)
   >>> list(keys)
   ['eggs', 'sausage', 'bacon', 'spam']
   >>> list(values)
   [2, 1, 1, 500]

   >>> # các đối tượng view là động và phản ánh các thay đổi của dict
   >>> del dishes['eggs']
   >>> del dishes['sausage']
   >>> list(keys)
   ['bacon', 'spam']

   >>> # các phép toán tập hợp
   >>> keys & {'eggs', 'bacon', 'salad'}
   {'bacon'}
   >>> keys ^ {'sausage', 'juice'} == {'juice', 'sausage', 'bacon', 'spam'}
   True
   >>> keys | ['juice', 'juice', 'juice'] == {'bacon', 'spam', 'juice'}
   True

   >>> # nhận lại proxy chỉ đọc cho từ điển ban đầu
   >>> values.mapping
   mappingproxy({'bacon': 1, 'spam': 500})
   >>> values.mapping['spam']
   500


.. _typecontextmanager:

Các loại Context Manager
========================

.. index::
   single: context manager
   single: context management protocol
   single: protocol; context management

Câu lệnh :keyword:`with` của Python hỗ trợ khái niệm runtime context được định nghĩa bởi một context manager. Khái niệm này được triển khai bằng một cặp phương thức, cho phép các lớp do người dùng định nghĩa xác định một runtime context được bắt đầu trước khi thực thi phần thân câu lệnh và kết thúc khi câu lệnh kết thúc:


.. method:: contextmanager.__enter__()

   Bắt đầu runtime context và trả về chính đối tượng này hoặc một đối tượng khác liên quan đến runtime context. Giá trị được phương thức này trả về được liên kết với identifier trong mệnh đề :keyword:`!as` của các câu lệnh :keyword:`with` sử dụng context manager này.

   Một ví dụ về context manager trả về chính nó là :term:`file object`. Các đối tượng tệp trả về chính chúng từ __enter__() để cho phép :func:`open` được sử dụng làm biểu thức context trong câu lệnh :keyword:`with`.

   Một ví dụ về context manager trả về một đối tượng liên quan là đối tượng được trả về bởi :func:`decimal.localcontext`. Các context manager này đặt decimal context đang hoạt động thành một bản sao của decimal context ban đầu, sau đó trả về bản sao đó. Điều này cho phép thực hiện các thay đổi đối với decimal context hiện tại trong phần thân của câu lệnh :keyword:`with` mà không ảnh hưởng đến mã bên ngoài
   câu lệnh :keyword:`!with`.


.. method:: contextmanager.__exit__(exc_type, exc_val, exc_tb)

   Kết thúc runtime context và trả về một cờ Boolean cho biết có nên bỏ qua mọi exception đã xảy ra hay không. Nếu một exception xảy ra trong khi thực thi phần thân của câu lệnh :keyword:`with`, các đối số sẽ chứa kiểu exception, giá trị và thông tin traceback. Nếu không, cả ba đối số đều là ``None``.

   Việc trả về giá trị true từ phương thức này sẽ khiến câu lệnh :keyword:`with` bỏ qua ngoại lệ và tiếp tục thực thi với câu lệnh ngay sau câu lệnh :keyword:`!with`. Nếu không, ngoại lệ sẽ tiếp tục lan truyền sau khi phương thức này thực thi xong.

   Nếu phương thức này phát sinh một ngoại lệ trong khi xử lý một ngoại lệ trước đó từ
   khối :keyword:`with`, ngoại lệ mới sẽ được phát sinh và ngoại lệ ban đầu được lưu trong thuộc tính :attr:`~BaseException.__context__` của nó.

   Không bao giờ được phát sinh lại một cách tường minh ngoại lệ được truyền vào—thay vào đó, phương thức này nên trả về giá trị false để cho biết phương thức đã hoàn tất thành công và không muốn bỏ qua ngoại lệ đã phát sinh. Điều này cho phép mã quản lý context dễ dàng xác định liệu phương thức :meth:`~object.__exit__` có thực sự thất bại hay không.

Python định nghĩa một số context manager để hỗ trợ đồng bộ hóa luồng, đóng kịp thời các tệp hoặc đối tượng khác và thao tác đơn giản hơn với context số học decimal đang hoạt động. Các kiểu cụ thể không được xử lý đặc biệt ngoài việc triển khai giao thức quản lý context. Xem
module :mod:`contextlib` để biết một số ví dụ.

:term:`generator`\s của Python và decorator :class:`contextlib.contextmanager` cung cấp một cách thuận tiện để triển khai các giao thức này. Nếu một hàm generator được trang trí bằng decorator :class:`contextlib.contextmanager`, hàm đó sẽ trả về một context manager triển khai các :meth:`~contextmanager.__enter__` cần thiết và
các phương thức :meth:`~contextmanager.__exit__`, thay vì iterator được tạo bởi một hàm generator chưa được trang trí.

Lưu ý rằng trong cấu trúc kiểu dành cho các đối tượng Python trong Python/C API không có slot cụ thể nào cho bất kỳ phương thức nào trong số này. Các kiểu mở rộng muốn định nghĩa những phương thức này phải cung cấp chúng dưới dạng một phương thức Python có thể truy cập thông thường. So với chi phí thiết lập context runtime, chi phí tra cứu một từ điển lớp đơn lẻ là không đáng kể.


Các kiểu chú thích kiểu --- :ref:`Generic Alias <types-genericalias>`, :ref:`Union <types-union>`
=================================================================================================

.. index::
   single: annotation; type annotation; type hint

Các kiểu dựng sẵn cốt lõi cho :term:`chú thích kiểu <annotation>` là
:ref:`Generic Alias <types-genericalias>` và :ref:`Union <types-union>`.


.. _types-genericalias:

Kiểu Generic Alias
------------------

.. index::
   pair: object; GenericAlias
   pair: Generic; Alias

Các đối tượng ``GenericAlias`` thường được tạo bởi
:ref:`việc dùng cú pháp chỉ số <subscriptions>` với một lớp. Chúng thường được sử dụng nhất cùng với
:ref:`các lớp container <sequence-types>`, chẳng hạn như :class:`list` hoặc
:class:`dict`. Ví dụ, ``list[int]`` là một đối tượng ``GenericAlias`` được tạo bằng cách dùng cú pháp chỉ số với lớp ``list`` và đối số :class:`int`. Các đối tượng ``GenericAlias`` chủ yếu được dùng với
:term:`type annotations <annotation>`.

.. note::

   Nhìn chung, chỉ có thể dùng cú pháp chỉ số với một lớp nếu lớp đó triển khai phương thức đặc biệt :meth:`~object.__class_getitem__`.

Một đối tượng ``GenericAlias`` hoạt động như một proxy cho :term:`generic type`, triển khai *các generic được tham số hóa*.

Đối với một lớp container, (các) đối số được cung cấp trong :ref:`cú pháp chỉ số <subscriptions>` của lớp có thể cho biết (các) kiểu của những phần tử mà một đối tượng chứa. Ví dụ, ``set[bytes]`` có thể được dùng trong type annotations để biểu thị một :class:`set` trong đó tất cả các phần tử đều có kiểu :class:`bytes`.

Đối với một lớp định nghĩa :meth:`~object.__class_getitem__` nhưng không phải là container, các đối số được cung cấp khi subscription lớp thường cho biết kiểu trả về của một hoặc nhiều phương thức được định nghĩa trên một đối tượng. Ví dụ: :mod:`regular expressions <re>` có thể được sử dụng cho cả kiểu dữ liệu :class:`str` và kiểu dữ liệu :class:`bytes`:

* Nếu ``x = re.search('foo', 'foo')``, ``x`` sẽ là một
  đối tượng :ref:`re.Match <match-objects>` trong đó các giá trị trả về của ``x.group(0)`` và ``x[0]`` đều có kiểu :class:`str`. Ta có thể biểu diễn loại đối tượng này trong type annotation bằng ``GenericAlias`` ``re.Match[str]``.

* Nếu ``y = re.search(b'bar', b'bar')`` (lưu ý ``b`` cho :class:`bytes`), ``y`` cũng sẽ là một instance của ``re.Match``, nhưng các giá trị trả về của ``y.group(0)`` và ``y[0]`` đều sẽ có kiểu
  :class:`bytes`. Trong type annotation, ta sẽ biểu diễn biến thể này của các đối tượng :ref:`re.Match <match-objects>` bằng ``re.Match[bytes]``.

Các đối tượng ``GenericAlias`` là các instance của lớp
:class:`types.GenericAlias`, cũng có thể được sử dụng để trực tiếp tạo các đối tượng ``GenericAlias``. Các specialization của :ref:`các lớp generic do người dùng định nghĩa <generic-classes>` có thể không phải là các instance của :class:`types.GenericAlias`, nhưng cung cấp chức năng tương tự.

.. describe:: T[X, Y, ...]

   Tạo một ``GenericAlias`` đại diện cho một kiểu ``T`` được tham số hóa bằng các kiểu *X*, *Y* và các kiểu khác tùy thuộc vào ``T`` được sử dụng. Ví dụ: một hàm mong đợi một :class:`list` chứa
   các phần tử :class:`float`::

      def average(values: list[float]) -> float:
          return sum(values) / len(values)

   Một ví dụ khác về các đối tượng :term:`mapping`, sử dụng một :class:`dict`, là một kiểu generic yêu cầu hai tham số kiểu đại diện cho kiểu của khóa và kiểu của giá trị. Trong ví dụ này, hàm mong đợi một ``dict`` có các khóa thuộc kiểu :class:`str` và các giá trị thuộc kiểu :class:`int`::

      def send_post_request(url: str, body: dict[str, int]) -> None:
          ...

Các hàm dựng sẵn :func:`isinstance` và :func:`issubclass` không chấp nhận các kiểu ``GenericAlias`` làm đối số thứ hai::

   >>> isinstance([1, 2], list[str])
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: isinstance() argument 2 cannot be a parameterized generic

Python runtime không thực thi :term:`chú thích kiểu <annotation>`. Điều này cũng áp dụng cho các kiểu generic và các tham số kiểu của chúng. Khi tạo một container object từ một ``GenericAlias``, các phần tử trong container không được kiểm tra theo kiểu của chúng. Ví dụ: đoạn mã sau đây không được khuyến khích, nhưng vẫn chạy mà không có lỗi::

   >>> t = list[str]
   >>> t([1, 2, 3])
   [1, 2, 3]

Ngoài ra, các generic được tham số hóa sẽ loại bỏ các tham số kiểu trong quá trình tạo object::

   >>> t = list[str]
   >>> type(t)
   <class 'types.GenericAlias'>

   >>> l = t()
   >>> type(l)
   <class 'list'>


Các instance của ``GenericAlias`` không phải là class tại runtime, dù chúng hoạt động như class (có thể được khởi tạo và tạo lớp con)::

   >>> import inspect
   >>> inspect.isclass(list[int])
   False

Điều này cũng đúng với :ref:`các generic do người dùng định nghĩa <user-defined-generics>`.

Việc gọi :func:`repr` hoặc :func:`str` trên một generic sẽ hiển thị kiểu đã tham số hóa::

   >>> repr(list[int])
   'list[int]'

   >>> str(list[int])
   'list[int]'

Phương thức :meth:`~object.__getitem__` của các container generic sẽ phát sinh ngoại lệ để ngăn những lỗi như ``dict[str][str]``::

   >>> dict[str][str]
   Traceback (most recent call last):
     ...
   TypeError: dict[str] is not a generic class

Tuy nhiên, các biểu thức như vậy hợp lệ khi sử dụng :ref:`các biến kiểu <generics>`. Chỉ mục phải có số phần tử bằng số mục biến kiểu trong ``GenericAlias`` object's :attr:`~genericalias.__args__`.::

   >>> from typing import TypeVar
   >>> Y = TypeVar('Y')
   >>> dict[str, Y][int]
   dict[str, int]


Các lớp Generic tiêu chuẩn
^^^^^^^^^^^^^^^^^^^^^^^^^^

Các lớp trong thư viện chuẩn sau đây hỗ trợ generic có tham số. Danh sách này không đầy đủ.

* :class:`tuple`
* :class:`list`
* :class:`dict`
* :class:`set`
* :class:`frozenset`
* :class:`type`
* :class:`asyncio.Future`
* :class:`asyncio.Task`
* :class:`collections.deque`
* :class:`collections.defaultdict`
* :class:`collections.OrderedDict`
* :class:`collections.Counter`
* :class:`collections.ChainMap`
* :class:`collections.abc.Awaitable`
* :class:`collections.abc.Coroutine`
* :class:`collections.abc.AsyncIterable`
* :class:`collections.abc.AsyncIterator`
* :class:`collections.abc.AsyncGenerator`
* :class:`collections.abc.Iterable`
* :class:`collections.abc.Iterator`
* :class:`collections.abc.Generator`
* :class:`collections.abc.Reversible`
* :class:`collections.abc.Container`
* :class:`collections.abc.Collection`
* :class:`collections.abc.Callable`
* :class:`collections.abc.Set`
* :class:`collections.abc.MutableSet`
* :class:`collections.abc.Mapping`
* :class:`collections.abc.MutableMapping`
* :class:`collections.abc.Sequence`
* :class:`collections.abc.MutableSequence`
* :class:`collections.abc.ByteString`
* :class:`collections.abc.MappingView`
* :class:`collections.abc.KeysView`
* :class:`collections.abc.ItemsView`
* :class:`collections.abc.ValuesView`
* :class:`contextlib.AbstractContextManager`
* :class:`contextlib.AbstractAsyncContextManager`
* :class:`dataclasses.Field`
* :class:`functools.cached_property`
* :class:`functools.partialmethod`
* :class:`os.PathLike`
* :class:`queue.LifoQueue`
* :class:`queue.Queue`
* :class:`queue.PriorityQueue`
* :class:`queue.SimpleQueue`
* :ref:`re.Pattern <re-objects>`
* :ref:`re.Match <match-objects>`
* :class:`shelve.BsdDbShelf`
* :class:`shelve.DbfilenameShelf`
* :class:`shelve.Shelf`
* :class:`types.MappingProxyType`
* :class:`weakref.WeakKeyDictionary`
* :class:`weakref.WeakMethod`
* :class:`weakref.WeakSet`
* :class:`weakref.WeakValueDictionary`



Các thuộc tính đặc biệt của đối tượng ``GenericAlias``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Tất cả generic đã tham số hóa đều triển khai các thuộc tính đặc biệt chỉ đọc.

.. attribute:: genericalias.__origin__

   Thuộc tính này trỏ tới generic class không có tham số::

      >>> list[int].__origin__
      <class 'list'>


.. attribute:: genericalias.__args__

   Thuộc tính này là một :class:`tuple` (có thể có độ dài là 1) gồm các generic type được truyền vào :meth:`~object.__class_getitem__` ban đầu của generic class::

      >>> dict[str, list[int]].__args__
      (<class 'str'>, list[int])


.. attribute:: genericalias.__parameters__

   Thuộc tính này là một tuple được tính toán một cách trì hoãn (có thể rỗng), gồm các type variable duy nhất được tìm thấy trong ``__args__``::

      >>> from typing import TypeVar

      >>> T = TypeVar('T')
      >>> list[T].__parameters__
      (~T,)


   .. note::
      Một đối tượng ``GenericAlias`` có các tham số :class:`typing.ParamSpec` có thể không có ``__parameters__`` chính xác sau khi thay thế vì
      :class:`typing.ParamSpec` chủ yếu được dùng để kiểm tra kiểu tĩnh.


.. attribute:: genericalias.__unpacked__

   Một giá trị boolean là true nếu alias đã được unpack bằng toán tử ``*`` (xem :data:`~typing.TypeVarTuple`).

   .. versionadded:: 3.11


.. seealso::

   :pep:`484` - Gợi ý kiểu
      Giới thiệu framework về chú thích kiểu của Python.

   :pep:`585` - Generic gợi ý kiểu trong các collection chuẩn
      Giới thiệu khả năng parameterize nguyên bản các lớp trong thư viện chuẩn, với điều kiện chúng triển khai class method đặc biệt
      :meth:`~object.__class_getitem__`.

   :ref:`Generics`, :ref:`generic do người dùng định nghĩa <user-defined-generics>` và :class:`typing.Generic`
      Tài liệu về cách triển khai các lớp generic có thể được tham số hóa tại runtime và được các trình kiểm tra kiểu tĩnh hiểu.

.. versionadded:: 3.9


.. _types-union:

Kiểu Union
----------

.. index::
   pair: object; Union
   pair: union; type

Một đối tượng union chứa giá trị của phép toán ``|`` (bitwise or) trên nhiều :ref:`đối tượng kiểu <bltin-type-objects>`. Các kiểu này chủ yếu được dùng cho :term:`chú thích kiểu <annotation>`. Biểu thức kiểu union cho phép sử dụng cú pháp gợi ý kiểu rõ ràng hơn so với việc lập chỉ mục :class:`typing.Union`.

.. describe:: X | Y | ...

   Định nghĩa một đối tượng union chứa các kiểu *X*, *Y*, v.v. ``X | Y`` có nghĩa là X hoặc Y. Nó tương đương với ``typing.Union[X, Y]``. Ví dụ: hàm sau đây yêu cầu một đối số có kiểu
   :class:`int` hoặc :class:`float`::

      def square(number: int | float) -> int | float:
          return number ** 2

   .. note::

      Không thể sử dụng toán tử ``|`` tại runtime để định nghĩa các union trong đó một hoặc nhiều thành viên là forward reference. Ví dụ: ``int | "Foo"``, trong đó ``"Foo"`` là tham chiếu đến một lớp chưa được định nghĩa, sẽ gây lỗi tại runtime. Đối với các union bao gồm forward reference, hãy biểu diễn toàn bộ biểu thức dưới dạng chuỗi, chẳng hạn như ``"int | Foo"``.

.. describe:: union_object == other

   Có thể kiểm tra tính bằng nhau của các đối tượng union với các đối tượng union khác. Chi tiết:

   * Các union của union được làm phẳng::

       (int | str) | float == int | str | float

   * Các kiểu dư thừa được loại bỏ::

       int | str | int == int | str

   * Khi so sánh các union, thứ tự bị bỏ qua::

      int | str == str | int

   * Nó tạo các instance của :class:`typing.Union`::

      int | str == typing.Union[int, str]
      type(int | str) is typing.Union

   * Các kiểu tùy chọn có thể được viết dưới dạng union với ``None``::

      str | None == typing.Optional[str]

.. describe:: isinstance(obj, union_object)
.. describe:: issubclass(obj, union_object)

   Các lệnh gọi đến :func:`isinstance` và :func:`issubclass` cũng được hỗ trợ với một đối tượng union::

      >>> isinstance("", int | str)
      True

   Tuy nhiên, :ref:`generic được tham số hóa <types-genericalias>` trong các đối tượng union không thể được kiểm tra::

      >>> isinstance(1, int | list[int])  # đánh giá short-circuit
      True
      >>> isinstance([1], int | list[int])
      Traceback (most recent call last):
        ...
      TypeError: isinstance() argument 2 cannot be a parameterized generic

Kiểu được cung cấp cho người dùng của đối tượng union có thể được truy cập từ
:class:`typing.Union` và được dùng cho các phép kiểm tra :func:`isinstance`::

   >>> import typing
   >>> isinstance(int | str, typing.Union)
   True
   >>> typing.Union()
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: cannot create 'typing.Union' instances

.. note::
   Phương thức :meth:`!__or__` dành cho các đối tượng kiểu được thêm vào để hỗ trợ cú pháp ``X | Y``. Nếu một metaclass triển khai :meth:`!__or__`, Union có thể ghi đè phương thức này:

   .. doctest::

      >>> class M(type):
      ...     def __or__(self, other):
      ...         return "Hello"
      ...
      >>> class C(metaclass=M):
      ...     pass
      ...
      >>> C | int
      'Hello'
      >>> int | C
      int | C

.. seealso::

   :pep:`604` -- PEP đề xuất cú pháp ``X | Y`` và kiểu Union.

.. versionadded:: 3.10

.. versionchanged:: 3.14

   Các đối tượng Union hiện là các thể hiện của :class:`typing.Union`. Trước đây, chúng là các thể hiện của :class:`types.UnionType`, vốn vẫn là bí danh cho :class:`typing.Union`.


.. _typesother:

Các kiểu dựng sẵn khác
======================

Trình thông dịch hỗ trợ một số loại đối tượng khác. Hầu hết các đối tượng này chỉ hỗ trợ một hoặc hai thao tác.


.. _typesmodules:

Mô-đun
------

Thao tác đặc biệt duy nhất trên một mô-đun là truy cập thuộc tính: ``m.name``, trong đó *m* là một mô-đun và *name* truy cập một tên được định nghĩa trong bảng ký hiệu của *m*. Có thể gán giá trị cho các thuộc tính mô-đun.  (Lưu ý rằng câu lệnh :keyword:`import` không phải, nói chính xác, là một thao tác trên đối tượng mô-đun; ``import foo`` không yêu cầu phải tồn tại một đối tượng mô-đun có tên *foo*, mà yêu cầu một *định nghĩa* (bên ngoài) cho một mô-đun có tên *foo* ở đâu đó.)

Một thuộc tính đặc biệt của mọi mô-đun là :attr:`~object.__dict__`. Đây là từ điển chứa bảng ký hiệu của mô-đun. Việc sửa đổi từ điển này thực sự sẽ thay đổi bảng ký hiệu của mô-đun, nhưng việc gán trực tiếp cho
thuộc tính :attr:`~object.__dict__` là không thể (bạn có thể viết ``m.__dict__['a'] = 1``, thao tác này định nghĩa ``m.a`` là ``1``, nhưng bạn không thể viết ``m.__dict__ = {}``).  Không nên sửa đổi trực tiếp :attr:`~object.__dict__`.

Các mô-đun được tích hợp trong trình thông dịch được viết như sau: ``<module 'sys' (built-in)>``.  Nếu được tải từ một tệp, chúng được viết là ``<module 'os' from '/usr/local/lib/pythonX.Y/os.pyc'>``.


.. _typesobjects:

Lớp và các thực thể lớp
-----------------------

Xem :ref:`objects` và :ref:`class` để biết thêm về những nội dung này.


.. _typesfunctions:

Hàm
---

Các đối tượng hàm được tạo bởi các định nghĩa hàm. Thao tác duy nhất trên một đối tượng hàm là gọi nó: ``func(argument-list)``.

Thực sự có hai loại đối tượng hàm: hàm tích hợp sẵn và hàm do người dùng định nghĩa. Cả hai đều hỗ trợ cùng một thao tác (gọi hàm), nhưng cách triển khai khác nhau, do đó có các kiểu đối tượng khác nhau.

Xem :ref:`function` để biết thêm thông tin.


.. _typesmethods:

Phương thức
-----------

.. index:: pair: object; method

Phương thức là các hàm được gọi bằng cú pháp thuộc tính. Có hai loại: :ref:`phương thức tích hợp sẵn <builtin-methods>` (chẳng hạn như :meth:`~list.append` trên các danh sách) và :ref:`phương thức thể hiện lớp <instance-methods>`. Các phương thức tích hợp sẵn được mô tả cùng với những kiểu hỗ trợ chúng.

Nếu bạn truy cập một method (một function được định nghĩa trong namespace của class) thông qua một instance, bạn sẽ nhận được một object đặc biệt: một :dfn:`bound method` (còn được gọi là
đối tượng :ref:`instance method <instance-methods>`. Khi được gọi, nó sẽ thêm đối số ``self`` vào danh sách đối số. Bound method có hai thuộc tính chỉ đọc đặc biệt:
:attr:`m.__self__ <method.__self__>` là đối tượng mà method hoạt động trên đó, còn :attr:`m.__func__ <method.__func__>` là function triển khai method. Việc gọi ``m(arg-1, arg-2, ..., arg-n)`` hoàn toàn tương đương với việc gọi ``m.__func__(m.__self__, arg-1, arg-2, ..., arg-n)``.

Giống như các :ref:`function objects <user-defined-funcs>`, bound method object hỗ trợ lấy các thuộc tính tùy ý. Tuy nhiên, vì các thuộc tính của method thực tế được lưu trên function object bên dưới (:attr:`method.__func__`), việc thiết lập thuộc tính của method trên bound method không được cho phép. Việc cố gắng thiết lập một thuộc tính trên method sẽ khiến :exc:`AttributeError` được phát sinh. Để thiết lập thuộc tính của method, bạn cần thiết lập rõ ràng thuộc tính đó trên function object bên dưới:

.. doctest::

   >>> class C:
   ...     def method(self):
   ...         pass
   ...
   >>> c = C()
   >>> c.method.whoami = 'my name is method'  # không thể thiết lập trên method
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   AttributeError: 'method' object has no attribute 'whoami'
   >>> c.method.__func__.whoami = 'my name is method'
   >>> c.method.whoami
   'my name is method'

Xem :ref:`instance-methods` để biết thêm thông tin.


.. index:: object; code, code object

.. _bltin-code-objects:

Các Code Object
---------------

.. index::
   pair: built-in function; compile
   single: __code__ (function object attribute)

Đối tượng mã được dùng trong quá trình triển khai để biểu diễn mã Python thực thi "được biên dịch giả" (pseudo-compiled), chẳng hạn như phần thân của một hàm. Chúng khác với đối tượng hàm vì không chứa tham chiếu đến môi trường thực thi toàn cục của chúng. Đối tượng mã được trả về bởi hàm dựng sẵn :func:`compile` và có thể được trích xuất từ các đối tượng hàm thông qua
thuộc tính :attr:`~function.__code__` của chúng. Xem thêm mô-đun :mod:`code`.

Việc truy cập :attr:`~function.__code__` sẽ phát sinh sự kiện kiểm tra :ref:`auditing event <auditing>` ``object.__getattr__`` với các đối số ``obj`` và ``"__code__"``.

.. index::
   pair: built-in function; exec
   pair: built-in function; eval

Có thể thực thi hoặc đánh giá một đối tượng mã bằng cách truyền nó (thay vì một chuỗi mã nguồn) cho các hàm dựng sẵn :func:`exec` hoặc :func:`eval`.

Xem :ref:`types` để biết thêm thông tin.


.. _bltin-type-objects:

Đối tượng kiểu
--------------

.. index::
   pair: built-in function; type
   pair: module; types

Đối tượng kiểu biểu diễn các loại đối tượng khác nhau. Kiểu của một đối tượng được truy cập bằng hàm dựng sẵn :func:`type`. Không có thao tác đặc biệt nào trên các kiểu. Mô-đun chuẩn :mod:`types` định nghĩa tên cho tất cả các kiểu dựng sẵn chuẩn.

Kiểu được viết như sau: ``<class 'int'>``.


.. _bltin-null-object:

Đối tượng Null
--------------

Đối tượng này được các hàm trả về khi chúng không trả về giá trị một cách tường minh. Đối tượng này không hỗ trợ thao tác đặc biệt nào. Chỉ có duy nhất một đối tượng null, có tên là ``None`` (một tên dựng sẵn). ``type(None)()`` tạo ra cùng một singleton.

Nó được viết là ``None``.


.. index:: single: ...; ellipsis literal
.. _bltin-ellipsis-object:

Đối tượng Ellipsis
------------------

Đối tượng này thường được dùng để biểu thị rằng một phần nào đó bị lược bỏ. Đối tượng này không hỗ trợ thao tác đặc biệt nào. Chỉ có duy nhất một đối tượng ellipsis, có tên là
:const:`Ellipsis` (một tên dựng sẵn). ``type(Ellipsis)()`` tạo ra
:const:`Ellipsis` là một singleton.

Nó được viết là ``Ellipsis`` hoặc ``...``.

Trong cách sử dụng thông thường, ``...`` với tư cách là đối tượng ``Ellipsis`` xuất hiện ở một vài nơi khác nhau, chẳng hạn:

- Trong type annotation, chẳng hạn như :ref:`callable arguments <annotating-callables>` hoặc :ref:`tuple elements <annotating-tuples>`.

- Làm phần thân của một hàm thay cho :ref:`pass statement <tut-pass>`.

- Trong các thư viện bên thứ ba, chẳng hạn như `Numpy's slicing and striding <https://numpy.org/doc/stable/user/basics.indexing.html#slicing-and-striding>`_.

Python cũng sử dụng ba dấu chấm theo những cách không phải là các đối tượng ``Ellipsis``, chẳng hạn:

- :const:`ELLIPSIS <doctest.ELLIPSIS>` của Doctest, được dùng như một mẫu cho nội dung bị thiếu.

- Dấu nhắc Python mặc định của shell :term:`interactive` khi phần nhập từng phần chưa hoàn chỉnh.

Cuối cùng, tài liệu Python thường sử dụng ba dấu chấm theo cách dùng tiếng Anh thông thường để biểu thị nội dung bị lược bỏ, ngay cả trong các ví dụ mã cũng sử dụng chúng làm ``Ellipsis``.


.. _bltin-notimplemented-object:

Đối tượng NotImplemented
------------------------

Đối tượng này được trả về từ các phép so sánh và phép toán nhị phân khi chúng được yêu cầu hoạt động trên các kiểu mà chúng không hỗ trợ. Xem :ref:`comparisons` để biết thêm thông tin. Có chính xác một đối tượng :data:`NotImplemented`.
:code:`type(NotImplemented)()` tạo ra instance singleton.

Nó được viết là :code:`NotImplemented`.


.. _typesinternal:

Đối tượng nội bộ
----------------

Xem :ref:`types` để biết thông tin này.  Nội dung đó mô tả
:ref:`các đối tượng stack frame <frame-objects>`,
:ref:`các đối tượng traceback <traceback-objects>`, và các đối tượng slice.


.. _specialattrs:

Thuộc tính đặc biệt
===================

Bản triển khai bổ sung một số thuộc tính chỉ đọc đặc biệt cho một số kiểu đối tượng, khi chúng phù hợp.  Một số thuộc tính trong đó không được báo cáo bởi
:func:`dir` hàm tích hợp sẵn.


.. attribute:: definition.__name__

   Tên của class, function, method, descriptor hoặc instance của generator.


.. attribute:: definition.__qualname__

   :term:`qualified name` của class, function, method, descriptor hoặc instance của generator.

   .. versionadded:: 3.3


.. attribute:: definition.__module__

   Tên của module nơi class hoặc function được định nghĩa.


.. attribute:: definition.__doc__

   Chuỗi documentation của class hoặc function, hoặc ``None`` nếu chưa được định nghĩa.


.. attribute:: definition.__type_params__

   :ref:`type parameters <type-params>` của các class, function generic và :ref:`type aliases <type-aliases>`. Đối với các class và function không phải generic, đây sẽ là một tuple rỗng.

   .. versionadded:: 3.12


.. _int_max_str_digits:

Giới hạn độ dài khi chuyển đổi chuỗi số nguyên
==============================================

CPython có một giới hạn chung khi chuyển đổi giữa :class:`int` và :class:`str` để giảm thiểu các cuộc tấn công từ chối dịch vụ. Giới hạn này *chỉ* áp dụng cho cơ số thập phân hoặc các cơ số số khác không phải lũy thừa của hai. Các phép chuyển đổi sang hệ thập lục phân, bát phân và nhị phân không bị giới hạn. Có thể cấu hình giới hạn này.

Kiểu :class:`int` trong CPython là một số có độ dài tùy ý được lưu dưới dạng nhị phân (thường được gọi là "bignum"). Không tồn tại thuật toán nào có thể chuyển đổi một chuỗi thành số nguyên nhị phân hoặc chuyển đổi một số nguyên nhị phân thành chuỗi trong thời gian tuyến tính, *trừ khi* cơ số là lũy thừa của 2. Ngay cả những thuật toán tốt nhất hiện nay cho cơ số 10 cũng có độ phức tạp dưới bậc hai. Việc chuyển đổi một giá trị lớn như ``int('1' * 500_000)`` có thể mất hơn một giây trên CPU nhanh.

Giới hạn kích thước chuyển đổi là một cách thiết thực để tránh :cve:`2020-10735`.

Giới hạn được áp dụng cho số ký tự chữ số trong chuỗi đầu vào hoặc đầu ra khi có liên quan đến một thuật toán chuyển đổi phi tuyến. Dấu gạch dưới và dấu của số không được tính vào giới hạn.

Khi một thao tác vượt quá giới hạn, một :exc:`ValueError` sẽ được phát sinh:

.. doctest::

   >>> import sys
   >>> sys.set_int_max_str_digits(4300)  # Mang tính minh họa, đây là giá trị mặc định.
   >>> _ = int('2' * 5432)
   Traceback (most recent call last):
   ...
   ValueError: Exceeds the limit (4300 digits) for integer string conversion: value has 5432 digits; use sys.set_int_max_str_digits() to increase the limit
   >>> i = int('2' * 4300)
   >>> len(str(i))
   4300
   >>> i_squared = i*i
   >>> len(str(i_squared))
   Traceback (most recent call last):
   ...
   ValueError: Exceeds the limit (4300 digits) for integer string conversion; use sys.set_int_max_str_digits() to increase the limit
   >>> len(hex(i_squared))
   7144
   >>> assert int(hex(i_squared), base=16) == i*i  # Hệ thập lục phân không bị giới hạn.

Giới hạn mặc định là 4300 chữ số, được cung cấp trong
:data:`sys.int_info.default_max_str_digits <sys.int_info>`. Giới hạn thấp nhất có thể cấu hình là 640 chữ số, như được cung cấp trong
:data:`sys.int_info.str_digits_check_threshold <sys.int_info>`.

Xác minh:

.. doctest::

   >>> import sys
   >>> assert sys.int_info.default_max_str_digits == 4300, sys.int_info
   >>> assert sys.int_info.str_digits_check_threshold == 640, sys.int_info
   >>> msg = int('578966293710682886880994035146873798396722250538762761564'
   ...           '9252925514383915483333812743580549779436104706260696366600'
   ...           '571186405732').to_bytes(53, 'big')
   ...

.. versionadded:: 3.11

Các API bị ảnh hưởng
--------------------

Giới hạn này chỉ áp dụng cho các phép chuyển đổi có khả năng chậm giữa :class:`int` và :class:`str` hoặc :class:`bytes`:

* ``int(string)`` với cơ số mặc định là 10.
* ``int(string, base)`` cho mọi cơ số không phải là lũy thừa của 2.
* ``str(integer)``.
* ``repr(integer)``.
* bất kỳ phép chuyển đổi chuỗi nào khác sang cơ số 10, chẳng hạn như ``f"{integer}"``, ``"{}".format(integer)`` hoặc ``b"%d" % integer``.

Các giới hạn này không áp dụng cho những hàm có thuật toán tuyến tính:

* ``int(string, base)`` với cơ số 2, 4, 8, 16 hoặc 32.
* :func:`int.from_bytes` và :func:`int.to_bytes`.
* :func:`hex`, :func:`oct`, :func:`bin`.
* :ref:`formatspec` cho các số thập lục phân, bát phân và nhị phân.
* :class:`str` thành :class:`float`.
* :class:`str` thành :class:`decimal.Decimal`.

Cấu hình giới hạn
-----------------

Trước khi Python khởi động, bạn có thể sử dụng một biến môi trường hoặc cờ dòng lệnh của interpreter để cấu hình giới hạn:

* :envvar:`PYTHONINTMAXSTRDIGITS`, ví dụ ``PYTHONINTMAXSTRDIGITS=640 python3`` để đặt giới hạn thành 640 hoặc ``PYTHONINTMAXSTRDIGITS=0 python3`` để tắt giới hạn.
* :option:`-X int_max_str_digits <-X>`, ví dụ ``python3 -X int_max_str_digits=640``
* :data:`sys.flags.int_max_str_digits` chứa giá trị của
  :envvar:`PYTHONINTMAXSTRDIGITS` hoặc :option:`-X int_max_str_digits <-X>`. Nếu cả biến môi trường và tùy chọn ``-X`` đều được đặt, tùy chọn ``-X`` sẽ được ưu tiên. Giá trị *-1* cho biết cả hai đều chưa được đặt, do đó giá trị của
  :data:`sys.int_info.default_max_str_digits` đã được sử dụng trong quá trình khởi tạo.

Trong mã, bạn có thể kiểm tra giới hạn hiện tại và đặt giới hạn mới bằng các
Các API :mod:`sys`:

* :func:`sys.get_int_max_str_digits` và :func:`sys.set_int_max_str_digits` lần lượt là getter và setter cho giới hạn trên toàn bộ interpreter. Các subinterpreter có giới hạn riêng.

Thông tin về giá trị mặc định và giá trị tối thiểu có trong :data:`sys.int_info`:

* :data:`sys.int_info.default_max_str_digits <sys.int_info>` là giới hạn mặc định được biên dịch sẵn.
* :data:`sys.int_info.str_digits_check_threshold <sys.int_info>` là giá trị thấp nhất được chấp nhận cho giới hạn này (ngoại trừ 0, giá trị sẽ vô hiệu hóa giới hạn).

.. versionadded:: 3.11

.. caution::

   Việc đặt giới hạn thấp *có thể* gây ra sự cố. Dù hiếm gặp, vẫn có mã chứa các hằng số số nguyên ở dạng thập phân trong mã nguồn, vượt quá ngưỡng tối thiểu. Một hệ quả của việc đặt giới hạn là mã nguồn Python chứa các literal số nguyên thập phân dài hơn giới hạn sẽ gặp lỗi trong quá trình phân tích cú pháp, thường là lúc khởi động hoặc import, thậm chí lúc cài đặt—bất cứ khi nào mã chưa có sẵn ``.pyc`` được cập nhật. Cách khắc phục cho mã nguồn chứa các hằng số lớn như vậy là chuyển chúng sang dạng thập lục phân ``0x``, vì dạng này không bị giới hạn.

   Hãy kiểm thử kỹ ứng dụng nếu bạn sử dụng giới hạn thấp. Đảm bảo các bài kiểm thử của bạn chạy với giới hạn được thiết lập sớm thông qua environment hoặc flag để giới hạn này được áp dụng trong quá trình khởi động và cả trong bất kỳ bước cài đặt nào có thể gọi Python để biên dịch trước mã nguồn ``.py`` thành các tệp ``.pyc``.

Cấu hình được khuyến nghị
-------------------------

:data:`sys.int_info.default_max_str_digits` mặc định được cho là phù hợp với hầu hết ứng dụng. Nếu ứng dụng của bạn yêu cầu giới hạn khác, hãy đặt giới hạn đó từ điểm vào chính bằng mã không phụ thuộc vào phiên bản Python, vì các API này đã được bổ sung trong các bản phát hành bản vá bảo mật ở những phiên bản trước 3.12.

Ví dụ::

   >>> import sys
   >>> if hasattr(sys, "set_int_max_str_digits"):
   ...     upper_bound = 68000
   ...     lower_bound = 4004
   ...     current_limit = sys.get_int_max_str_digits()
   ...     if current_limit == 0 or current_limit > upper_bound:
   ...         sys.set_int_max_str_digits(upper_bound)
   ...     elif current_limit < lower_bound:
   ...         sys.set_int_max_str_digits(lower_bound)

Nếu bạn cần tắt hoàn toàn, hãy đặt thành ``0``.


.. rubric:: Chú thích

.. [1] Bạn có thể tìm thấy thêm thông tin về các phương thức đặc biệt này trong Python Reference Manual (:ref:`customization`).

.. [2] Do đó, danh sách ``[1, 2]`` được xem là bằng ``[1.0, 2.0]``, và các tuple cũng tương tự.

.. [3] Chúng phải có, vì trình phân tích cú pháp không thể xác định kiểu của các toán hạng.

.. [4] Các ký tự có phân biệt kiểu chữ là những ký tự có thuộc tính phân loại tổng quát thuộc một trong các giá trị "Lu" (Chữ cái, chữ hoa), "Ll" (Chữ cái, chữ thường) hoặc "Lt" (Chữ cái, viết hoa kiểu tiêu đề).

.. [5] Do đó, để chỉ định dạng cho chỉ một tuple, bạn phải cung cấp một tuple singleton mà phần tử duy nhất của nó là tuple cần được định dạng.

.. _`the Unicode Standard`: https://unicode.org/Public/UNIDATA/extracted/DerivedNumericType.txt
.. _`linspace recipe`: https://code.activestate.com/recipes/579000-equally-spaced-numbers-linspace/
.. _`Alphabetic property defined in section 4.10 'Letters, Alphabetic, and Ideographic' of the Unicode Standard`: https://www.unicode.org/versions/Unicode16.0.0/core-spec/chapter-4/#G91002
.. _`Numpy's slicing and striding`: https://numpy.org/doc/stable/user/basics.indexing.html#slicing-and-striding
