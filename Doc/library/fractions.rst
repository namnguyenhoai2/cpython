:mod:`!fractions` --- Số hữu tỉ
===============================

.. module:: fractions
   :synopsis: Số hữu tỉ.

.. moduleauthor:: Jeffrey Yasskin <jyasskin at gmail.com>
.. sectionauthor:: Jeffrey Yasskin <jyasskin at gmail.com>

**Mã nguồn:** :source:`Lib/fractions.py`

--------------

Mô-đun :mod:`!fractions` cung cấp khả năng hỗ trợ thực hiện phép tính số hữu tỉ.


Có thể tạo một đối tượng Fraction từ một cặp số hữu tỉ, một số đơn lẻ hoặc một chuỗi.

.. index:: single: as_integer_ratio()

.. class:: Fraction(numerator=0, denominator=1)
           Fraction(number) Fraction(string)

   Phiên bản đầu tiên yêu cầu *numerator* và *denominator* là các thể hiện của :class:`numbers.Rational` và trả về một thể hiện :class:`Fraction` mới có giá trị bằng ``numerator/denominator``. Nếu *denominator* bằng không, nó sẽ phát sinh :exc:`ZeroDivisionError`.

   Phiên bản thứ hai yêu cầu *number* là một instance của
   :class:`numbers.Rational` hoặc có phương thức :meth:`!as_integer_ratio` (bao gồm :class:`float` và :class:`decimal.Decimal`). Phương thức này trả về một instance :class:`Fraction` có chính xác cùng giá trị. Giả định rằng phương thức :meth:`!as_integer_ratio` trả về một cặp số nguyên nguyên tố cùng nhau và số cuối cùng là số dương. Lưu ý rằng do các vấn đề thường gặp với dấu chấm động nhị phân (xem :ref:`tut-fp-issues`), đối số truyền cho ``Fraction(1.1)`` không hoàn toàn bằng 11/10, vì vậy ``Fraction(1.1)`` không *not* trả về ``Fraction(11, 10)`` như người ta có thể mong đợi. (Tuy nhiên, hãy xem tài liệu về phương thức :meth:`limit_denominator` bên dưới.)

   Phiên bản cuối cùng của hàm khởi tạo mong đợi một chuỗi. Dạng thông thường của chuỗi này là::

      [sign] numerator ['/' denominator]

   Trong đó ``sign`` tùy chọn có thể là '+' hoặc '-' và ``numerator`` và ``denominator`` (nếu có) là các chuỗi gồm các chữ số thập phân (có thể dùng dấu gạch dưới để phân tách các chữ số như với các literal số nguyên trong mã). Ngoài ra, mọi chuỗi biểu diễn một giá trị hữu hạn và được chấp nhận bởi hàm khởi tạo :class:`float` cũng được chấp nhận bởi hàm khởi tạo :class:`Fraction`. Ở cả hai dạng, chuỗi đầu vào cũng có thể chứa khoảng trắng ở đầu và/hoặc cuối. Dưới đây là một số ví dụ::

      >>> from fractions import Fraction
      >>> Fraction(16, -10)
      Fraction(-8, 5)
      >>> Fraction(123)
      Fraction(123, 1)
      >>> Fraction()
      Fraction(0, 1)
      >>> Fraction('3/7')
      Fraction(3, 7)
      >>> Fraction(' -3/7 ')
      Fraction(-3, 7)
      >>> Fraction('1.414213 \t\n')
      Fraction(1414213, 1000000)
      >>> Fraction('-.125')
      Fraction(-1, 8)
      >>> Fraction('7e-6')
      Fraction(7, 1000000)
      >>> Fraction(2.25)
      Fraction(9, 4)
      >>> Fraction(1.1)
      Fraction(2476979795053773, 2251799813685248)
      >>> from decimal import Decimal
      >>> Fraction(Decimal('1.1'))
      Fraction(11, 10)


   Lớp :class:`Fraction` kế thừa từ lớp cơ sở trừu tượng
   :class:`numbers.Rational`, và triển khai tất cả các phương thức và phép toán của lớp đó. Các instance :class:`Fraction` là :term:`hashable`, và nên được xem là bất biến. Ngoài ra,
   :class:`Fraction` có các thuộc tính và phương thức sau:

   .. versionchanged:: 3.2
      Hàm khởi tạo :class:`Fraction` hiện chấp nhận :class:`float` và
      các thực thể :class:`decimal.Decimal`.

   .. versionchanged:: 3.9
      Hàm :func:`math.gcd` hiện được dùng để chuẩn hóa *tử số* và *mẫu số*. :func:`math.gcd` luôn trả về kiểu :class:`int`. Trước đây, kiểu GCD phụ thuộc vào *tử số* và *mẫu số*.

   .. versionchanged:: 3.11
      Giờ đây, dấu gạch dưới được cho phép khi tạo một thực thể :class:`Fraction` từ chuỗi, theo các quy tắc của :PEP:`515`.

   .. versionchanged:: 3.11
      :class:`Fraction` implements ``__int__`` now to satisfy
      Các phép kiểm tra thực thể ``typing.SupportsInt``.

   .. versionchanged:: 3.12
      Được phép có khoảng trắng quanh dấu gạch chéo đối với đầu vào chuỗi: ``Fraction('2 / 3')``.

   .. versionchanged:: 3.12
      :class:`Fraction` instances now support float-style formatting, with
      các kiểu trình bày ``"e"``, ``"E"``, ``"f"``, ``"F"``, ``"g"``, ``"G"`` và ``"%""``.

   .. versionchanged:: 3.13
      Việc định dạng các đối tượng :class:`Fraction` mà không chỉ định kiểu hiển thị hiện hỗ trợ ký tự điền, căn chỉnh, xử lý dấu, độ rộng tối thiểu và nhóm chữ số.

   .. versionchanged:: 3.14
      Hàm khởi tạo :class:`Fraction` hiện chấp nhận mọi đối tượng có
      phương thức :meth:`!as_integer_ratio`.

   .. attribute:: numerator

      Tử số của Fraction ở dạng tối giản.

   .. attribute:: denominator

      Mẫu số của Fraction ở dạng tối giản. Được đảm bảo là số dương.


   .. method:: as_integer_ratio()

      Trả về một tuple gồm hai số nguyên, trong đó tỷ số của chúng bằng với Fraction ban đầu. Tỷ số ở dạng tối giản và có mẫu số dương.

      .. versionadded:: 3.8

   .. method:: is_integer()

      Trả về ``True`` nếu Fraction là một số nguyên.

      .. versionadded:: 3.12

   .. classmethod:: from_float(f)

      Hàm khởi tạo thay thế chỉ chấp nhận các thực thể của
      :class:`float` hoặc :class:`numbers.Integral`. Lưu ý rằng ``Fraction.from_float(0.3)`` không có cùng giá trị với ``Fraction(3, 10)``.

      .. note::

         Kể từ Python 3.2, bạn cũng có thể tạo một
         thực thể :class:`Fraction` trực tiếp từ một :class:`float`.


   .. classmethod:: from_decimal(dec)

      Hàm khởi tạo thay thế chỉ chấp nhận các thực thể của
      :class:`decimal.Decimal` hoặc :class:`numbers.Integral`.

      .. note::

         Kể từ Python 3.2, bạn cũng có thể tạo một
         Tạo một instance :class:`Fraction` trực tiếp từ một instance :class:`decimal.Decimal`.


   .. classmethod:: from_number(number)

      Hàm khởi tạo thay thế chỉ chấp nhận các thực thể của
      :class:`numbers.Integral`, :class:`numbers.Rational`,
      :class:`float` hoặc :class:`decimal.Decimal`, và các đối tượng có phương thức :meth:`!as_integer_ratio`, nhưng không phải chuỗi.

      .. versionadded:: 3.14


   .. method:: limit_denominator(max_denominator=1000000)

      Tìm và trả về :class:`Fraction` gần nhất với ``self`` có mẫu số không vượt quá max_denominator. Phương thức này hữu ích để tìm các xấp xỉ hữu tỉ cho một số dấu phẩy động đã cho:

         >>> from fractions import Fraction
         >>> Fraction('3.1415926535897932').limit_denominator(1000)
         Fraction(355, 113)

      hoặc để khôi phục một số hữu tỉ được biểu diễn dưới dạng float:

         >>> from math import pi, cos
         >>> Fraction(cos(pi/3))
         Fraction(4503599627370497, 9007199254740992)
         >>> Fraction(cos(pi/3)).limit_denominator()
         Fraction(1, 2)
         >>> Fraction(1.1).limit_denominator()
         Fraction(11, 10)


   .. method:: __floor__()

      Trả về :class:`int` lớn nhất ``<= self``. Phương thức này cũng có thể được truy cập thông qua hàm :func:`math.floor`:

        >>> from math import floor
        >>> floor(Fraction(355, 113))
        3


   .. method:: __ceil__()

      Trả về :class:`int` nhỏ nhất ``>= self``. Phương thức này cũng có thể được truy cập thông qua hàm :func:`math.ceil`.


   .. method:: __round__()
               __round__(ndigits)

      Phiên bản đầu tiên trả về :class:`int` gần nhất với ``self``, làm tròn nửa về số chẵn. Phiên bản thứ hai làm tròn ``self`` đến bội số gần nhất của ``Fraction(1, 10**ndigits)`` (về mặt logic, nếu ``ndigits`` là số âm), cũng làm tròn nửa về số chẵn. Phương thức này cũng có thể được truy cập thông qua hàm :func:`round`.

   .. method:: __format__(format_spec, /)

      Hỗ trợ định dạng các thực thể :class:`Fraction` thông qua
      phương thức :meth:`str.format`, hàm dựng sẵn :func:`format`, hoặc
      :ref:`chuỗi định dạng <f-strings>`.

      Nếu chuỗi đặc tả định dạng ``format_spec`` format không kết thúc bằng một trong các kiểu trình bày ``'e'``, ``'E'``, ``'f'``, ``'F'``, ``'g'``, ``'G'`` hoặc ``'%'`` thì việc định dạng tuân theo các quy tắc chung về điền, căn chỉnh, xử lý dấu, độ rộng tối thiểu và nhóm như được mô tả trong
      :ref:`ngôn ngữ mini đặc tả định dạng <formatspec>`. Cờ "dạng thay thế" ``'#'`` được hỗ trợ: nếu có, cờ này buộc chuỗi đầu ra luôn bao gồm mẫu số tường minh, ngay cả khi giá trị được định dạng là một số nguyên chính xác. Cờ điền bằng số 0 ``'0'`` không được hỗ trợ.

      Nếu chuỗi đặc tả định dạng ``format_spec`` kết thúc bằng một trong các kiểu trình bày ``'e'``, ``'E'``, ``'f'``, ``'F'``, ``'g'``, ``'G'`` hoặc ``'%'`` thì việc định dạng tuân theo các quy tắc được nêu cho
      kiểu :class:`float` trong phần :ref:`formatspec`.

      Dưới đây là một số ví dụ::

         >>> from fractions import Fraction
         >>> format(Fraction(103993, 33102), '_')
         '103_993/33_102'
         >>> format(Fraction(1, 7), '.^+10')
         '...+1/7...'
         >>> format(Fraction(3, 1), '')
         '3'
         >>> format(Fraction(3, 1), '#')
         '3/1'
         >>> format(Fraction(1, 7), '.40g')
         '0.1428571428571428571428571428571428571429'
         >>> format(Fraction('1234567.855'), '_.2f')
         '1_234_567.86'
         >>> f"{Fraction(355, 113):*>20.6e}"
         '********3.141593e+00'
         >>> old_price, new_price = 499, 672
         >>> "{:.2%} price increase".format(Fraction(new_price, old_price) - 1)
         '34.67% price increase'


.. seealso::

   Mô-đun :mod:`numbers`
      Các lớp cơ sở trừu tượng tạo nên tháp số học.
