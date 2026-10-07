:mod:`!decimal` --- Số học dấu phẩy cố định và dấu phẩy động thập phân
======================================================================

.. module:: decimal
   :synopsis: Triển khai Đặc tả Số học Thập phân Tổng quát.

.. moduleauthor:: Eric Price <eprice at tjhsst.edu>
.. moduleauthor:: Facundo Batista <facundo at taniquetil.com.ar>
.. moduleauthor:: Raymond Hettinger <python at rcn.com>
.. moduleauthor:: Aahz <aahz at pobox.com>
.. moduleauthor:: Tim Peters <tim.one at comcast.net>
.. moduleauthor:: Stefan Krah <skrah at bytereef.org>
.. sectionauthor:: Raymond D. Hettinger <python at rcn.com>

**Mã nguồn:** :source:`Lib/decimal.py`

.. import modules for testing inline doctests with the Sphinx doctest builder
.. testsetup:: *

   import decimal
   import math
   from decimal import *
   # make sure each group gets a fresh context
   setcontext(Context())

.. testcleanup:: *

   # make sure other tests (outside this file) get a fresh context
   setcontext(Context())

--------------

Mô-đun :mod:`!decimal` cung cấp khả năng thực hiện số học dấu phẩy động thập phân được làm tròn chính xác và nhanh chóng. Mô-đun này có một số ưu điểm so với
:class:`float` kiểu dữ liệu:

* Decimal “dựa trên một `mô hình dấu phẩy động <https://speleotrove.com/decimal/damodel.html#refnumber>`__ được thiết kế với con người làm trọng tâm, và tất yếu có một nguyên tắc chỉ đạo tối thượng -- máy tính phải cung cấp một phép tính hoạt động theo cùng cách với phép tính mà con người học ở trường.” -- trích từ đặc tả số học thập phân.

* Các số thập phân có thể được biểu diễn chính xác. Trái lại, những số như ``1.1`` và ``2.2`` không có biểu diễn chính xác trong số dấu phẩy động nhị phân. Người dùng cuối thường không mong đợi ``1.1 + 2.2`` hiển thị thành ``3.3000000000000003`` như khi dùng số dấu phẩy động nhị phân.

* Tính chính xác này cũng được thể hiện trong phép tính số học. Với floating point thập phân, ``0.1
  + 0.1 + 0.1 - 0.3`` bằng chính xác không. Với floating point nhị phân, kết quả
  là ``5.5511151231257827e-017``. Mặc dù gần bằng không, những khác biệt này khiến việc kiểm tra tính bằng nhau trở nên không đáng tin cậy, và các sai khác có thể tích lũy. Vì lý do này, decimal được ưu tiên trong các ứng dụng kế toán có các bất biến về tính bằng nhau nghiêm ngặt.

* module decimal tích hợp khái niệm về chữ số có nghĩa, vì vậy ``1.30
  + 1.20`` is ``2.50``. Số 0 ở cuối được giữ lại để biểu thị tính có nghĩa.
  Đây là cách trình bày thông dụng trong các ứng dụng tiền tệ. Đối với phép nhân, cách tính "schoolbook" sử dụng tất cả các chữ số trong các thừa số. Chẳng hạn, ``1.3 * 1.2`` cho kết quả ``1.56``, còn ``1.30 * 1.20`` cho kết quả ``1.5600``.

* Không giống floating point nhị phân dựa trên phần cứng, module decimal có độ chính xác do người dùng thay đổi được (mặc định là 28 chữ số), và có thể lớn đến mức cần thiết cho một bài toán cụ thể:

     >>> from decimal import *
     >>> getcontext().prec = 6
     >>> Decimal(1) / Decimal(7)
     Decimal('0.142857')
     >>> getcontext().prec = 28
     >>> Decimal(1) / Decimal(7)
     Decimal('0.1428571428571428571428571429')

* Cả số dấu phẩy động nhị phân và thập phân đều được triển khai dựa trên các tiêu chuẩn đã công bố. Mặc dù kiểu float tích hợp sẵn chỉ cung cấp một phần khiêm tốn các khả năng của mình, module decimal cung cấp tất cả các phần bắt buộc của tiêu chuẩn. Khi cần, lập trình viên có toàn quyền kiểm soát việc làm tròn và xử lý tín hiệu. Điều này bao gồm một tùy chọn để thực thi phép tính chính xác bằng cách sử dụng ngoại lệ nhằm chặn mọi phép toán không chính xác.

* Module decimal được thiết kế để hỗ trợ "không thiên lệch, cả phép tính thập phân chính xác không làm tròn (đôi khi được gọi là phép tính dấu phẩy cố định) và phép tính dấu phẩy động có làm tròn." -- trích từ đặc tả phép tính thập phân.

Thiết kế của module xoay quanh ba khái niệm: số thập phân, context cho phép tính và các tín hiệu.

Một số thập phân là bất biến. Nó có dấu, các chữ số của phần hệ số và số mũ. Để bảo toàn độ chính xác biểu diễn, các chữ số của phần hệ số không cắt bỏ các số 0 ở cuối. Số thập phân cũng bao gồm các giá trị đặc biệt như ``Infinity``, ``-Infinity`` và ``NaN``. Tiêu chuẩn cũng phân biệt ``-0`` với ``+0``.

Context cho phép tính là một môi trường chỉ định độ chính xác, các quy tắc làm tròn, giới hạn của số mũ, các cờ cho biết kết quả của phép toán và các bộ kích hoạt trap xác định liệu tín hiệu có được xử lý như ngoại lệ hay không. Các tùy chọn làm tròn bao gồm :const:`ROUND_CEILING`, :const:`ROUND_DOWN`,
:const:`ROUND_FLOOR`, :const:`ROUND_HALF_DOWN`, :const:`ROUND_HALF_EVEN`,
:const:`ROUND_HALF_UP`, :const:`ROUND_UP` và :const:`ROUND_05UP`.

Tín hiệu là các nhóm điều kiện bất thường phát sinh trong quá trình tính toán. Tùy theo nhu cầu của ứng dụng, tín hiệu có thể bị bỏ qua, được xem là thông tin hoặc được xử lý như ngoại lệ. Các tín hiệu trong module decimal là: :const:`Clamped`, :const:`InvalidOperation`,
:const:`DivisionByZero`, :const:`Inexact`, :const:`Rounded`, :const:`Subnormal`,
:const:`Overflow`, :const:`Underflow` và :const:`FloatOperation`.

Mỗi signal đều có một flag và một trap enabler. Khi gặp một signal, flag của nó được đặt thành một, sau đó, nếu trap enabler được đặt thành một, một exception sẽ được raised. Các flag có tính sticky, vì vậy người dùng cần reset chúng trước khi theo dõi một phép tính.


.. seealso::

   * Đặc tả General Decimal Arithmetic của IBM, `The General Decimal Arithmetic Specification <https://speleotrove.com/decimal/decarith.html>`_.

.. %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


.. _decimal-tutorial:

Hướng dẫn bắt đầu nhanh
-----------------------

Cách bắt đầu thông thường khi sử dụng decimal là import module, xem context hiện tại bằng :func:`getcontext` và, nếu cần, đặt các giá trị mới cho precision, rounding hoặc các trap được bật::

   >>> from decimal import *
   >>> getcontext()
   Context(prec=28, rounding=ROUND_HALF_EVEN, Emin=-999999, Emax=999999,
           capitals=1, clamp=0, flags=[], traps=[Overflow, DivisionByZero,
           InvalidOperation])

   >>> getcontext().prec = 7       # Đặt precision mới

Các instance Decimal có thể được tạo từ số nguyên, chuỗi, số thực hoặc tuple. Việc tạo từ số nguyên hoặc số thực sẽ thực hiện chuyển đổi chính xác giá trị của số nguyên hoặc số thực đó. Các số Decimal bao gồm những giá trị đặc biệt như ``NaN``, đại diện cho "Not a number", ``Infinity`` dương và âm, cùng ``-0``::

   >>> getcontext().prec = 28
   >>> Decimal(10)
   Decimal('10')
   >>> Decimal('3.14')
   Decimal('3.14')
   >>> Decimal(3.14)
   Decimal('3.140000000000000124344978758017532527446746826171875')
   >>> Decimal((0, (3, 1, 4), -2))
   Decimal('3.14')
   >>> Decimal(str(2.0 ** 0.5))
   Decimal('1.4142135623730951')
   >>> Decimal(2) ** Decimal('0.5')
   Decimal('1.414213562373095048801688724')
   >>> Decimal('NaN')
   Decimal('NaN')
   >>> Decimal('-Infinity')
   Decimal('-Infinity')

Nếu tín hiệu :exc:`FloatOperation` bị bắt, việc vô tình trộn số thập phân và số dấu phẩy động trong các hàm khởi tạo hoặc phép so sánh thứ tự sẽ phát sinh ngoại lệ::

   >>> c = getcontext()
   >>> c.traps[FloatOperation] = True
   >>> Decimal(3.14)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   decimal.FloatOperation: [<class 'decimal.FloatOperation'>]
   >>> Decimal('3.5') < 3.7
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   decimal.FloatOperation: [<class 'decimal.FloatOperation'>]
   >>> Decimal('3.5') == 3.5
   True

.. versionadded:: 3.3

Ý nghĩa của một Decimal mới chỉ được xác định bởi số chữ số đầu vào. Độ chính xác và cách làm tròn của Context chỉ có tác dụng trong các phép toán số học.

.. doctest:: newcontext

   >>> getcontext().prec = 6
   >>> Decimal('3.0')
   Decimal('3.0')
   >>> Decimal('3.1415926535')
   Decimal('3.1415926535')
   >>> Decimal('3.1415926535') + Decimal('2.7182818285')
   Decimal('5.85987')
   >>> getcontext().rounding = ROUND_UP
   >>> Decimal('3.1415926535') + Decimal('2.7182818285')
   Decimal('5.85988')

Nếu vượt quá các giới hạn nội bộ của phiên bản C, việc tạo một số thập phân sẽ phát sinh :class:`InvalidOperation`::

   >>> Decimal("1e9999999999999999999")
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   decimal.InvalidOperation: [<class 'decimal.InvalidOperation'>]

.. versionchanged:: 3.3

Các số thập phân tương tác tốt với phần lớn các thành phần còn lại của Python. Sau đây là một màn trình diễn nhỏ về số dấu phẩy động thập phân:

.. doctest::
   :options: +NORMALIZE_WHITESPACE

   >>> data = list(map(Decimal, '1.34 1.87 3.45 2.35 1.00 0.03 9.25'.split()))
   >>> max(data)
   Decimal('9.25')
   >>> min(data)
   Decimal('0.03')
   >>> sorted(data)
   [Decimal('0.03'), Decimal('1.00'), Decimal('1.34'), Decimal('1.87'),
    Decimal('2.35'), Decimal('3.45'), Decimal('9.25')]
   >>> sum(data)
   Decimal('19.29')
   >>> a,b,c = data[:3]
   >>> str(a)
   '1.34'
   >>> float(a)
   1.34
   >>> round(a, 1)
   Decimal('1.3')
   >>> int(a)
   1
   >>> a * 5
   Decimal('6.70')
   >>> a * b
   Decimal('2.5058')
   >>> c % a
   Decimal('0.77')

Các số thập phân có thể được định dạng (bằng :func:`format` tích hợp sẵn hoặc :ref:`f-strings`) theo ký hiệu dấu phẩy cố định hoặc ký hiệu khoa học, sử dụng cùng cú pháp định dạng (xem
:ref:`formatspec`) như kiểu :class:`float` tích hợp sẵn:

.. doctest::

   >>> format(Decimal('2.675'), "f")
   '2.675'
   >>> format(Decimal('2.675'), ".2f")
   '2.68'
   >>> f"{Decimal('2.675'):.2f}"
   '2.68'
   >>> format(Decimal('2.675'), ".2e")
   '2.68e+0'
   >>> with localcontext() as ctx:
   ...     ctx.rounding = ROUND_DOWN
   ...     print(format(Decimal('2.675'), ".2f"))
   ...
   2.67

Một số hàm toán học cũng khả dụng cho Decimal:

   >>> getcontext().prec = 28
   >>> Decimal(2).sqrt()
   Decimal('1.414213562373095048801688724')
   >>> Decimal(1).exp()
   Decimal('2.718281828459045235360287471')
   >>> Decimal('10').ln()
   Decimal('2.302585092994045684017991455')
   >>> Decimal('10').log10()
   Decimal('1')

Phương thức :meth:`~Decimal.quantize` làm tròn một số đến một số mũ cố định. Phương thức này hữu ích cho các ứng dụng tiền tệ, vốn thường làm tròn kết quả đến một số chữ số thập phân cố định:

   >>> Decimal('7.325').quantize(Decimal('.01'), rounding=ROUND_DOWN)
   Decimal('7.32')
   >>> Decimal('7.325').quantize(Decimal('1.'), rounding=ROUND_UP)
   Decimal('8')

Như đã trình bày ở trên, hàm :func:`getcontext` truy cập context hiện tại và cho phép thay đổi các thiết lập. Cách tiếp cận này đáp ứng nhu cầu của hầu hết các ứng dụng.

Đối với các tác vụ nâng cao hơn, việc tạo các context thay thế bằng
constructor :meth:`Context` có thể hữu ích. Để kích hoạt một context thay thế, hãy sử dụng hàm :func:`setcontext`.

Theo tiêu chuẩn, module :mod:`!decimal` cung cấp hai context tiêu chuẩn sẵn sàng sử dụng, :const:`BasicContext` và :const:`ExtendedContext`. Context đầu tiên đặc biệt hữu ích cho việc debug vì nhiều trap đã được bật:

.. doctest:: newcontext
   :options: +NORMALIZE_WHITESPACE

   >>> myothercontext = Context(prec=60, rounding=ROUND_HALF_DOWN)
   >>> setcontext(myothercontext)
   >>> Decimal(1) / Decimal(7)
   Decimal('0.142857142857142857142857142857142857142857142857142857142857')

   >>> ExtendedContext
   Context(prec=9, rounding=ROUND_HALF_EVEN, Emin=-999999, Emax=999999,
           capitals=1, clamp=0, flags=[], traps=[])
   >>> setcontext(ExtendedContext)
   >>> Decimal(1) / Decimal(7)
   Decimal('0.142857143')
   >>> Decimal(42) / Decimal(0)
   Decimal('Infinity')

   >>> setcontext(BasicContext)
   >>> Decimal(42) / Decimal(0)
   Traceback (most recent call last):
     File "<pyshell#143>", line 1, in -toplevel-
       Decimal(42) / Decimal(0)
   DivisionByZero: x / 0

Các context cũng có các cờ signal để theo dõi những điều kiện bất thường xảy ra trong quá trình tính toán. Các cờ vẫn được đặt cho đến khi được xóa rõ ràng, vì vậy tốt nhất là xóa các cờ trước mỗi nhóm phép tính cần theo dõi bằng phương thức :meth:`~Context.clear_flags`.::

   >>> setcontext(ExtendedContext)
   >>> getcontext().clear_flags()
   >>> Decimal(355) / Decimal(113)
   Decimal('3.14159292')
   >>> getcontext()
   Context(prec=9, rounding=ROUND_HALF_EVEN, Emin=-999999, Emax=999999,
           capitals=1, clamp=0, flags=[Inexact, Rounded], traps=[])

Mục nhập *flags* cho biết phép xấp xỉ hữu tỉ của pi đã được làm tròn (các chữ số vượt quá độ chính xác của context đã bị loại bỏ) và kết quả là không chính xác (một số chữ số bị loại bỏ khác không).

Các bẫy riêng lẻ được thiết lập bằng dictionary trong thuộc tính :attr:`~Context.traps` của một context:

.. doctest:: newcontext

   >>> setcontext(ExtendedContext)
   >>> Decimal(1) / Decimal(0)
   Decimal('Infinity')
   >>> getcontext().traps[DivisionByZero] = 1
   >>> Decimal(1) / Decimal(0)
   Traceback (most recent call last):
     File "<pyshell#112>", line 1, in -toplevel-
       Decimal(1) / Decimal(0)
   DivisionByZero: x / 0

Hầu hết các chương trình chỉ điều chỉnh context hiện tại một lần, ở phần đầu chương trình. Và trong nhiều ứng dụng, dữ liệu được chuyển đổi thành :class:`Decimal` bằng một phép cast duy nhất bên trong vòng lặp. Sau khi context được thiết lập và các số thập phân được tạo, phần lớn chương trình thao tác với dữ liệu không khác gì khi sử dụng các kiểu số Python khác.

.. %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


.. _decimal-decimal:

Đối tượng Decimal
-----------------


.. class:: Decimal(value="0", context=None)

   Tạo một đối tượng :class:`Decimal` mới dựa trên *value*.

   *value* có thể là một số nguyên, chuỗi, tuple, :class:`float`, hoặc một đối tượng :class:`Decimal` khác. Nếu không cung cấp *value*, hàm trả về ``Decimal('0')``. Nếu *value* là một chuỗi, chuỗi đó phải tuân theo cú pháp chuỗi số thập phân sau khi đã loại bỏ các ký tự khoảng trắng ở đầu và cuối, cũng như các dấu gạch dưới trong chuỗi::

      sign           ::=  '+' | '-'
      digit          ::=  '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
      indicator      ::=  'e' | 'E'
      digits         ::=  digit [digit]...
      decimal-part   ::=  digits '.' [digits] | ['.'] digits
      exponent-part  ::=  indicator [sign] digits
      infinity       ::=  'Infinity' | 'Inf'
      nan            ::=  'NaN' [digits] | 'sNaN' [digits]
      numeric-value  ::=  decimal-part [exponent-part] | infinity
      numeric-string ::=  [sign] numeric-value | [sign] nan

   Các chữ số thập phân Unicode khác cũng được phép sử dụng ở vị trí ``digit`` xuất hiện ở trên. Những chữ số này bao gồm các chữ số thập phân từ nhiều bảng chữ cái khác (ví dụ: chữ số Ả Rập-Ấn Độ và Devanāgarī), cùng với các chữ số fullwidth từ ``'\uff10'`` đến ``'\uff19'``. Không phân biệt chữ hoa chữ thường, vì vậy, chẳng hạn, ``inf``, ``Inf``, ``INFINITY`` và ``iNfINity`` đều là cách viết hợp lệ của vô cực dương.

   Nếu *value* là một :class:`tuple`, nó phải có ba thành phần: một dấu (``0`` cho số dương hoặc ``1`` cho số âm), một :class:`tuple` gồm các chữ số và một số mũ nguyên. Ví dụ, ``Decimal((0, (1, 4, 1, 4), -3))`` trả về ``Decimal('1.414')``.

   Nếu *value* là một :class:`float`, giá trị dấu phẩy động nhị phân sẽ được chuyển đổi không mất mát sang giá trị thập phân tương đương chính xác. Việc chuyển đổi này thường có thể yêu cầu độ chính xác từ 53 chữ số trở lên. Ví dụ: ``Decimal(float('1.1'))`` được chuyển đổi thành ``Decimal('1.100000000000000088817841970012523233890533447265625')``.

   Độ chính xác của *context* không ảnh hưởng đến số chữ số được lưu trữ. Điều đó được xác định hoàn toàn bởi số chữ số trong *value*. Ví dụ: ``Decimal('3.00000')`` ghi lại cả năm số 0, ngay cả khi độ chính xác của context chỉ là ba.

   Mục đích của đối số *context* là xác định cần làm gì nếu *value* là một chuỗi không hợp lệ. Nếu context bẫy :const:`InvalidOperation`, một ngoại lệ sẽ được phát sinh; nếu không, hàm khởi tạo trả về một Decimal mới có giá trị bằng ``NaN``.

   Sau khi được khởi tạo, các đối tượng :class:`Decimal` là bất biến.

   .. versionchanged:: 3.2
      Đối số của hàm khởi tạo giờ đây được phép là một thực thể :class:`float`.

   .. versionchanged:: 3.3
      :class:`float` arguments raise an exception if the :exc:`FloatOperation`
      trap được bật. Theo mặc định, trap bị tắt.

   .. versionchanged:: 3.6
      Có thể sử dụng dấu gạch dưới để phân nhóm, giống như với các literal số nguyên và dấu phẩy động trong mã.

   Các đối tượng số dấu phẩy động thập phân có nhiều thuộc tính giống với các kiểu số dựng sẵn khác, chẳng hạn như :class:`float` và :class:`int`. Tất cả các phép toán toán học thông thường và phương thức đặc biệt đều áp dụng được. Tương tự, các đối tượng thập phân có thể được sao chép, pickle, in, dùng làm khóa từ điển, dùng làm phần tử của tập hợp, so sánh, sắp xếp và chuyển đổi sang một kiểu khác (chẳng hạn như :class:`float` hoặc
   :class:`int`).

   Có một số khác biệt nhỏ giữa phép tính trên các đối tượng Decimal và phép tính trên số nguyên và số thực. Khi áp dụng toán tử phần dư ``%`` cho các đối tượng Decimal, dấu của kết quả là dấu của *số bị chia* thay vì dấu của số chia::

      >>> (-7) % 4
      1
      >>> Decimal(-7) % Decimal(4)
      Decimal('-3')

   Toán tử chia lấy phần nguyên ``//`` hoạt động tương tự, trả về phần nguyên của thương thực (cắt về phía 0) thay vì phần sàn của nó, nhằm duy trì đẳng thức thông thường ``x == (x // y) * y + x % y``::

      >>> -7 // 4
      -2
      >>> Decimal(-7) // Decimal(4)
      Decimal('-1')

   Các toán tử ``%`` và ``//`` lần lượt thực hiện các phép toán ``remainder`` và ``divide-integer`` như được mô tả trong đặc tả.

   Các đối tượng Decimal nhìn chung không thể kết hợp với số thực hoặc các thể hiện của :class:`fractions.Fraction` trong các phép toán số học: chẳng hạn, việc cộng một :class:`Decimal` với một :class:`float` sẽ gây ra :exc:`TypeError`. Tuy nhiên, có thể sử dụng các toán tử so sánh của Python để so sánh một thể hiện :class:`Decimal` ``x`` với một số khác ``y``. Điều này giúp tránh các kết quả gây nhầm lẫn khi thực hiện phép so sánh bằng giữa các số thuộc các kiểu khác nhau.

   .. versionchanged:: 3.2
      Các phép so sánh khác kiểu giữa các thực thể :class:`Decimal` và các kiểu số khác hiện đã được hỗ trợ đầy đủ.

   Ngoài các thuộc tính số tiêu chuẩn, các đối tượng số dấu phẩy động thập phân còn có một số phương thức chuyên biệt:


   .. method:: adjusted()

      Trả về số mũ đã điều chỉnh sau khi dịch các chữ số ngoài cùng bên phải của coefficient cho đến khi chỉ còn lại chữ số đầu tiên: ``Decimal('321e+5').adjusted()`` trả về bảy.  Được dùng để xác định vị trí của chữ số có nghĩa nhất so với dấu thập phân.

   .. method:: as_integer_ratio()

      Trả về một cặp ``(n, d)`` số nguyên biểu diễn giá trị đã cho
      :class:`Decimal` instance dưới dạng phân số, ở dạng tối giản và có mẫu số dương::

          >>> Decimal('-3.14').as_integer_ratio()
          (-157, 50)

      Phép chuyển đổi là chính xác.  Phát sinh OverflowError đối với các giá trị vô cực và ValueError đối với NaN.

   .. versionadded:: 3.6

   .. method:: as_tuple()

      Trả về biểu diễn :term:`named tuple` của số: ``DecimalTuple(sign, digits, exponent)``.


   .. method:: canonical()

      Trả về encoding chuẩn tắc của đối số.  Hiện tại, encoding của một instance :class:`Decimal` luôn là chuẩn tắc, vì vậy thao tác này trả về đối số mà không thay đổi.

   .. method:: compare(other, context=None)

      So sánh giá trị của hai đối tượng Decimal.  :meth:`compare` trả về một đối tượng Decimal và nếu một trong hai toán hạng là NaN thì kết quả là NaN::

         a or b is a NaN  ==> Decimal('NaN')
         a < b            ==> Decimal('-1')
         a == b           ==> Decimal('0')
         a > b            ==> Decimal('1')

   .. method:: compare_signal(other, context=None)

      Phép toán này giống hệt phương thức :meth:`compare`, ngoại trừ việc tất cả NaN đều phát tín hiệu.  Nghĩa là, nếu không có toán hạng nào là signaling NaN thì mọi toán hạng quiet NaN đều được xử lý như thể là signaling NaN.

   .. method:: compare_total(other, context=None)

      So sánh hai toán hạng bằng cách sử dụng biểu diễn trừu tượng thay vì giá trị số của chúng.  Tương tự phương thức :meth:`compare`, nhưng kết quả cung cấp một thứ tự toàn phần trên các đối tượng :class:`Decimal`.  Hai
      đối tượng :class:`Decimal` có cùng giá trị số nhưng biểu diễn khác nhau sẽ được so sánh là không bằng nhau theo thứ tự này:

         >>> Decimal('12.0').compare_total(Decimal('12'))
         Decimal('-1')

      Quiet NaN và signaling NaN cũng được đưa vào thứ tự toàn phần.  Kết quả của hàm này là ``Decimal('0')`` nếu cả hai toán hạng có cùng biểu diễn, ``Decimal('-1')`` nếu toán hạng thứ nhất đứng trước toán hạng thứ hai trong thứ tự toàn phần, và ``Decimal('1')`` nếu toán hạng thứ nhất đứng sau toán hạng thứ hai trong thứ tự toàn phần.  Xem đặc tả để biết chi tiết về thứ tự toàn phần.

      Phép toán này không bị ảnh hưởng bởi context và không phát tín hiệu: không có cờ nào bị thay đổi và không thực hiện làm tròn.  Ngoại lệ là phiên bản C có thể phát sinh InvalidOperation nếu không thể chuyển đổi chính xác toán hạng thứ hai.

   .. method:: compare_total_mag(other, context=None)

      So sánh hai toán hạng bằng cách sử dụng biểu diễn trừu tượng thay vì giá trị của chúng như trong :meth:`compare_total`, nhưng bỏ qua dấu của từng toán hạng. ``x.compare_total_mag(y)`` tương đương với ``x.copy_abs().compare_total(y.copy_abs())``.

      Phép toán này không bị ảnh hưởng bởi context và không phát tín hiệu: không có cờ nào bị thay đổi và không thực hiện làm tròn.  Ngoại lệ là phiên bản C có thể phát sinh InvalidOperation nếu không thể chuyển đổi chính xác toán hạng thứ hai.

   .. method:: conjugate()

      Chỉ trả về chính nó; phương thức này chỉ nhằm tuân thủ Decimal Specification.

   .. method:: copy_abs()

      Trả về giá trị tuyệt đối của đối số. Thao tác này không bị ảnh hưởng bởi context và không gây hiệu ứng: không có flag nào bị thay đổi và không thực hiện làm tròn.

   .. method:: copy_negate()

      Trả về giá trị phủ định của đối số. Thao tác này không bị ảnh hưởng bởi context và không gây hiệu ứng: không có flag nào bị thay đổi và không thực hiện làm tròn.

   .. method:: copy_sign(other, context=None)

      Trả về một bản sao của toán hạng thứ nhất với dấu được đặt giống với dấu của toán hạng thứ hai. Ví dụ:

         >>> Decimal('2.3').copy_sign(Decimal('-1.5'))
         Decimal('-2.3')

      Phép toán này không bị ảnh hưởng bởi context và không phát tín hiệu: không có cờ nào bị thay đổi và không thực hiện làm tròn.  Ngoại lệ là phiên bản C có thể phát sinh InvalidOperation nếu không thể chuyển đổi chính xác toán hạng thứ hai.

   .. method:: exp(context=None)

      Trả về giá trị của hàm mũ (tự nhiên) ``e**x`` tại số đã cho. Kết quả được làm tròn chính xác bằng cách sử dụng
      chế độ làm tròn :const:`ROUND_HALF_EVEN`.

      >>> Decimal(1).exp()
      Decimal('2.718281828459045235360287471')
      >>> Decimal(321).exp()
      Decimal('2.561702493119680037517373933E+139')

   .. classmethod:: from_float(f, /)

      Hàm khởi tạo thay thế chỉ chấp nhận các thực thể của :class:`float` hoặc
      :class:`int`.

      Lưu ý ``Decimal.from_float(0.1)`` không giống với ``Decimal('0.1')``. Vì 0.1 không thể biểu diễn chính xác dưới dạng số thực dấu phẩy động nhị phân, giá trị này được lưu dưới dạng giá trị có thể biểu diễn gần nhất là ``0x1.999999999999ap-4``. Giá trị tương đương đó ở dạng thập phân là ``0.1000000000000000055511151231257827021181583404541015625``.

      .. note:: Kể từ Python 3.2, một thực thể :class:`Decimal` cũng có thể được tạo trực tiếp từ một :class:`float`.

      .. doctest::

          >>> Decimal.from_float(0.1)
          Decimal('0.1000000000000000055511151231257827021181583404541015625')
          >>> Decimal.from_float(float('nan'))
          Decimal('NaN')
          >>> Decimal.from_float(float('inf'))
          Decimal('Infinity')
          >>> Decimal.from_float(float('-inf'))
          Decimal('-Infinity')

      .. versionadded:: 3.1

   .. classmethod:: from_number(number, /)

      Hàm khởi tạo thay thế chỉ chấp nhận các thực thể của
      :class:`float`, :class:`int` hoặc :class:`Decimal`, nhưng không chấp nhận chuỗi hoặc tuple.

      .. doctest::

          >>> Decimal.from_number(314)
          Decimal('314')
          >>> Decimal.from_number(0.1)
          Decimal('0.1000000000000000055511151231257827021181583404541015625')
          >>> Decimal.from_number(Decimal('3.14'))
          Decimal('3.14')

      .. versionadded:: 3.14

   .. method:: fma(other, third, context=None)

      Phép nhân-cộng hợp nhất. Trả về self*other+third mà không làm tròn tích trung gian self*other.

      >>> Decimal(2).fma(3, 5)
      Decimal('11')

   .. method:: is_canonical()

      Trả về :const:`True` nếu đối số là canonical và :const:`False` nếu không. Hiện tại, một đối tượng :class:`Decimal` luôn là canonical, vì vậy thao tác này luôn trả về :const:`True`.

   .. method:: is_finite()

      Trả về :const:`True` nếu đối số là một số hữu hạn, và
      :const:`False` nếu đối số là vô cực hoặc NaN.

   .. method:: is_infinite()

      Trả về :const:`True` nếu đối số là vô cực dương hoặc vô cực âm và :const:`False` nếu không.

   .. method:: is_nan()

      Trả về :const:`True` nếu đối số là NaN (quiet hoặc signaling) và
      :const:`False` nếu không.

   .. method:: is_normal(context=None)

      Trả về :const:`True` nếu đối số là một số hữu hạn *normal*. Trả về
      :const:`False` nếu đối số là số không, số dưới chuẩn, vô hạn hoặc NaN.

   .. method:: is_qnan()

      Trả về :const:`True` nếu đối số là NaN im lặng, và
      :const:`False` nếu không.

   .. method:: is_signed()

      Trả về :const:`True` nếu đối số có dấu âm và
      :const:`False` nếu không. Lưu ý rằng cả số không và NaN đều có thể mang dấu.

   .. method:: is_snan()

      Trả về :const:`True` nếu đối số là NaN báo hiệu và :const:`False` nếu không.

   .. method:: is_subnormal(context=None)

      Trả về :const:`True` nếu đối số là số dưới chuẩn và :const:`False` nếu không.

   .. method:: is_zero()

      Trả về :const:`True` nếu đối số là số 0 (dương hoặc âm) và
      :const:`False` nếu không.

   .. method:: ln(context=None)

      Trả về logarit tự nhiên (cơ số e) của toán hạng. Kết quả được làm tròn chính xác bằng chế độ làm tròn :const:`ROUND_HALF_EVEN`.

   .. method:: log10(context=None)

      Trả về logarit cơ số mười của toán hạng. Kết quả được làm tròn chính xác bằng chế độ làm tròn :const:`ROUND_HALF_EVEN`.

   .. method:: logb(context=None)

      Đối với một số khác không, trả về số mũ đã điều chỉnh của toán hạng dưới dạng một
      đối tượng :class:`Decimal`. Nếu toán hạng là số 0 thì trả về ``Decimal('-Infinity')`` và đặt cờ :const:`DivisionByZero`. Nếu toán hạng là vô cực thì trả về ``Decimal('Infinity')``.

   .. method:: logical_and(other, context=None)

      :meth:`logical_and` là một phép toán logic nhận hai *toán hạng logic* (xem :ref:`logical_operands_label`). Kết quả là phép ``and`` theo từng chữ số của hai toán hạng.

   .. method:: logical_invert(context=None)

      :meth:`logical_invert` là một phép toán logic. Kết quả là phép đảo từng chữ số của toán hạng.

   .. method:: logical_or(other, context=None)

      :meth:`logical_or` là một phép toán logic nhận hai *toán hạng logic* (xem :ref:`logical_operands_label`). Kết quả là phép ``or`` theo từng chữ số của hai toán hạng.

   .. method:: logical_xor(other, context=None)

      :meth:`logical_xor` là một phép toán logic nhận hai *toán hạng logic* (xem :ref:`logical_operands_label`). Kết quả là phép OR loại trừ theo từng chữ số của hai toán hạng.

   .. method:: max(other, context=None)

      Giống như ``max(self, other)``, ngoại trừ việc quy tắc làm tròn của context được áp dụng trước khi trả về, và các giá trị ``NaN`` được báo hiệu hoặc bỏ qua (tùy thuộc vào context và việc chúng là signaling hay quiet).

   .. method:: max_mag(other, context=None)

      Tương tự phương thức :meth:`.max`, nhưng phép so sánh được thực hiện bằng cách sử dụng giá trị tuyệt đối của các toán hạng.

   .. method:: min(other, context=None)

      Giống như ``min(self, other)``, ngoại trừ việc quy tắc làm tròn của context được áp dụng trước khi trả về, và các giá trị ``NaN`` được báo hiệu hoặc bỏ qua (tùy thuộc vào context và việc chúng là signaling hay quiet).

   .. method:: min_mag(other, context=None)

      Tương tự phương thức :meth:`.min`, nhưng phép so sánh được thực hiện bằng cách sử dụng giá trị tuyệt đối của các toán hạng.

   .. method:: next_minus(context=None)

      Trả về số lớn nhất có thể biểu diễn trong context đã cho (hoặc trong context của thread hiện tại nếu không cung cấp context) và nhỏ hơn toán hạng đã cho.

   .. method:: next_plus(context=None)

      Trả về số nhỏ nhất có thể biểu diễn trong context đã cho (hoặc trong context của thread hiện tại nếu không cung cấp context) và lớn hơn toán hạng đã cho.

   .. method:: next_toward(other, context=None)

      Nếu hai toán hạng không bằng nhau, trả về số gần với toán hạng thứ nhất nhất theo hướng của toán hạng thứ hai. Nếu cả hai toán hạng bằng nhau về giá trị số, trả về một bản sao của toán hạng thứ nhất với dấu được đặt giống dấu của toán hạng thứ hai.

   .. method:: normalize(context=None)

      Được dùng để tạo các giá trị chuẩn tắc của một lớp tương đương trong context hiện tại hoặc context được chỉ định.

      Phương thức này có ngữ nghĩa giống thao tác cộng một ngôi, ngoại trừ việc nếu kết quả cuối cùng là hữu hạn thì kết quả được rút gọn về dạng đơn giản nhất, loại bỏ mọi số 0 ở cuối và giữ nguyên dấu. Cụ thể, khi hệ số khác 0 và là bội số của mười, hệ số được chia cho mười và số mũ được tăng thêm 1. Ngược lại (khi hệ số bằng 0), số mũ được đặt thành 0. Trong mọi trường hợp, dấu không thay đổi.

      Ví dụ, ``Decimal('32.100')`` và ``Decimal('0.321000e+2')`` đều được chuẩn hóa thành giá trị tương đương ``Decimal('32.1')``.

      Lưu ý rằng việc làm tròn được áp dụng *trước khi* rút gọn về dạng đơn giản nhất.

      Trong các phiên bản mới nhất của đặc tả, thao tác này còn được gọi là ``reduce``.

   .. method:: number_class(context=None)

      Trả về một chuỗi mô tả *class* của toán hạng. Giá trị trả về là một trong mười chuỗi sau.

      * ``"-Infinity"``, cho biết toán hạng là vô cực âm.
      * ``"-Normal"``, cho biết toán hạng là một số chuẩn âm.
      * ``"-Subnormal"``, cho biết toán hạng là số dưới chuẩn âm.
      * ``"-Zero"``, cho biết toán hạng là số 0 âm.
      * ``"+Zero"``, cho biết toán hạng là số 0 dương.
      * ``"+Subnormal"``, cho biết toán hạng là số dương dưới chuẩn.
      * ``"+Normal"``, cho biết toán hạng là một số dương chuẩn.
      * ``"+Infinity"``, cho biết toán hạng là vô cực dương.
      * ``"NaN"``, cho biết toán hạng là NaN yên lặng (Not a Number).
      * ``"sNaN"``, cho biết toán hạng là NaN báo hiệu.

   .. method:: quantize(exp, rounding=None, context=None)

      Trả về một giá trị bằng toán hạng đầu tiên sau khi làm tròn và có số mũ của toán hạng thứ hai.

      >>> Decimal('1.41421356').quantize(Decimal('1.000'))
      Decimal('1.414')

      Không giống các phép toán khác, nếu độ dài của hệ số sau phép toán quantize lớn hơn precision thì sẽ có một
      :const:`InvalidOperation` được báo hiệu. Điều này đảm bảo rằng, trừ khi có điều kiện lỗi, số mũ đã lượng tử hóa luôn bằng số mũ của toán hạng bên phải.

      Ngoài ra, không giống các phép toán khác, quantize không bao giờ báo hiệu Underflow, ngay cả khi kết quả là số dưới chuẩn và không chính xác.

      Nếu số mũ của toán hạng thứ hai lớn hơn số mũ của toán hạng thứ nhất thì có thể cần làm tròn. Trong trường hợp này, chế độ làm tròn được xác định bởi đối số ``rounding`` nếu được cung cấp, nếu không thì bởi đối số ``context`` đã cho; nếu không cung cấp đối số nào, chế độ làm tròn của context của thread hiện tại sẽ được sử dụng.

      Một lỗi được trả về bất cứ khi nào số mũ kết quả lớn hơn
      :attr:`~Context.Emax` hoặc nhỏ hơn :meth:`~Context.Etiny`.

   .. method:: radix()

      Trả về ``Decimal(10)``, cơ số (base) mà lớp :class:`Decimal` sử dụng để thực hiện mọi phép toán. Được cung cấp để tương thích với đặc tả.

   .. method:: remainder_near(other, context=None)

      Trả về phần dư của *self* khi chia cho *other*. Điều này khác với ``self % other`` ở chỗ dấu của phần dư được chọn để giảm thiểu giá trị tuyệt đối của nó. Cụ thể hơn, giá trị trả về là ``self - n * other``, trong đó ``n`` là số nguyên gần nhất với giá trị chính xác của ``self / other``, và nếu có hai số nguyên cách đều thì chọn số chẵn.

      Nếu kết quả bằng không thì dấu của nó sẽ là dấu của *self*.

      >>> Decimal(18).remainder_near(Decimal(10))
      Decimal('-2')
      >>> Decimal(25).remainder_near(Decimal(10))
      Decimal('5')
      >>> Decimal(35).remainder_near(Decimal(10))
      Decimal('-5')

   .. method:: rotate(other, context=None)

      Trả về kết quả xoay các chữ số của toán hạng thứ nhất theo số lượng được chỉ định bởi toán hạng thứ hai. Toán hạng thứ hai phải là một số nguyên trong phạm vi từ -precision đến precision. Giá trị tuyệt đối của toán hạng thứ hai cho biết số vị trí cần xoay. Nếu toán hạng thứ hai là số dương thì xoay sang trái; nếu không thì xoay sang phải. Nếu cần, phần hệ số của toán hạng thứ nhất sẽ được thêm các số 0 ở bên trái để đạt độ dài precision. Dấu và số mũ của toán hạng thứ nhất không thay đổi.

   .. method:: same_quantum(other, context=None)

      Kiểm tra xem self và other có cùng số mũ hay cả hai đều là ``NaN``.

      Phép toán này không bị ảnh hưởng bởi context và không phát tín hiệu: không có cờ nào bị thay đổi và không thực hiện làm tròn.  Ngoại lệ là phiên bản C có thể phát sinh InvalidOperation nếu không thể chuyển đổi chính xác toán hạng thứ hai.

   .. method:: scaleb(other, context=None)

      Trả về toán hạng thứ nhất với số mũ được điều chỉnh theo toán hạng thứ hai. Tương đương, trả về toán hạng thứ nhất nhân với ``10**other``. Toán hạng thứ hai phải là một số nguyên.

   .. method:: shift(other, context=None)

      Trả về kết quả dịch các chữ số của toán hạng thứ nhất theo số lượng được chỉ định bởi toán hạng thứ hai. Toán hạng thứ hai phải là một số nguyên trong phạm vi từ -precision đến precision. Giá trị tuyệt đối của toán hạng thứ hai cho biết số vị trí cần dịch. Nếu toán hạng thứ hai là số dương thì dịch sang trái; nếu không thì dịch sang phải. Các chữ số được dịch vào phần hệ số là các số 0. Dấu và số mũ của toán hạng thứ nhất không thay đổi.

   .. method:: sqrt(context=None)

      Trả về căn bậc hai của đối số với độ chính xác đầy đủ.


   .. method:: to_eng_string(context=None)

      Chuyển đổi thành chuỗi, sử dụng ký hiệu kỹ thuật nếu cần dùng số mũ.

      Ký hiệu kỹ thuật có số mũ là bội số của 3. Điều này có thể để lại tối đa 3 chữ số ở bên trái dấu thập phân và có thể yêu cầu thêm một hoặc hai số 0 ở cuối.

      Ví dụ, thao tác này chuyển đổi ``Decimal('123E+1')`` thành ``Decimal('1.23E+3')``.

   .. method:: to_integral(rounding=None, context=None)

      Giống hệt phương thức :meth:`to_integral_value`. Tên ``to_integral`` được giữ lại để tương thích với các phiên bản cũ hơn.

   .. method:: to_integral_exact(rounding=None, context=None)

      Làm tròn đến số nguyên gần nhất, phát tín hiệu :const:`Inexact` hoặc
      :const:`Rounded` tùy trường hợp nếu xảy ra làm tròn. Chế độ làm tròn được xác định bởi tham số ``rounding`` nếu được cung cấp, nếu không thì bởi ``context`` đã cho. Nếu không cung cấp tham số nào, chế độ làm tròn của context hiện tại sẽ được sử dụng.

   .. method:: to_integral_value(rounding=None, context=None)

      Làm tròn đến số nguyên gần nhất mà không phát tín hiệu :const:`Inexact` hoặc
      :const:`Rounded`. Nếu được cung cấp, áp dụng phương thức làm tròn *rounding*; nếu không, sử dụng phương thức làm tròn trong *context* được cung cấp hoặc context hiện tại.

   Các số Decimal có thể được làm tròn bằng hàm :func:`.round`:

   .. describe:: round(number)
   .. describe:: round(number, ndigits)

      Nếu *ndigits* không được cung cấp hoặc ``None``, trả về giá trị gần nhất với :class:`int` của *number*, làm tròn các trường hợp hòa về số chẵn và bỏ qua phương thức làm tròn của
      :class:`Decimal` context. Phát sinh :exc:`OverflowError` nếu *number* là vô cực hoặc :exc:`ValueError` nếu đó là NaN (quiet hoặc signaling).

      Nếu *ndigits* là một :class:`int`, phương thức làm tròn của context được tuân theo và một :class:`Decimal` biểu diễn *number* được làm tròn đến bội số gần nhất của ``Decimal('1E-ndigits')`` sẽ được trả về; trong trường hợp này, ``round(number, ndigits)`` tương đương với ``self.quantize(Decimal('1E-ndigits'))``. Trả về ``Decimal('NaN')`` nếu *number* là quiet NaN. Phát sinh :class:`InvalidOperation` nếu *number* là vô cực, signaling NaN hoặc nếu độ dài của coefficient sau thao tác quantize lớn hơn precision của context hiện tại. Nói cách khác, đối với các trường hợp thông thường:

      * nếu *ndigits* là số dương, trả về *number* được làm tròn đến *ndigits* chữ số thập phân;
      * nếu *ndigits* bằng không, trả về *number* được làm tròn đến số nguyên gần nhất;
      * nếu *ndigits* là số âm, trả về *number* được làm tròn đến bội số gần nhất của ``10**abs(ndigits)``.

      Ví dụ::

          >>> from decimal import Decimal, getcontext, ROUND_DOWN
          >>> getcontext().rounding = ROUND_DOWN
          >>> round(Decimal('3.75'))     # bỏ qua việc làm tròn của context
          4
          >>> round(Decimal('3.5'))      # round-ties-to-even
          4
          >>> round(Decimal('3.75'), 0)  # sử dụng việc làm tròn của context
          Decimal('3')
          >>> round(Decimal('3.75'), 1)
          Decimal('3.7')
          >>> round(Decimal('3.75'), -1)
          Decimal('0E+1')


.. _logical_operands_label:

Toán hạng logic
^^^^^^^^^^^^^^^

Các phương thức :meth:`~Decimal.logical_and`, :meth:`~Decimal.logical_invert`, :meth:`~Decimal.logical_or` và :meth:`~Decimal.logical_xor` yêu cầu các đối số của chúng là *toán hạng logic*. Một *toán hạng logic* là một thực thể :class:`Decimal` có số mũ và dấu đều bằng không, đồng thời tất cả các chữ số của nó đều là ``0`` hoặc ``1``.

.. %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


.. _decimal-context:

Đối tượng Context
-----------------

Context là các môi trường cho những phép toán số học. Chúng kiểm soát độ chính xác, thiết lập quy tắc làm tròn, xác định những signal nào được xử lý như các exception và giới hạn phạm vi của số mũ.

Mỗi thread có context hiện tại riêng, được truy cập hoặc thay đổi bằng
các hàm :func:`getcontext` và :func:`setcontext`:


.. function:: getcontext()

   Trả về context hiện tại của thread đang hoạt động.


.. function:: setcontext(c, /)

   Đặt context hiện tại của thread đang hoạt động thành *c*.

Bạn cũng có thể sử dụng câu lệnh :keyword:`with` và hàm :func:`localcontext` để tạm thời thay đổi context đang hoạt động.

.. function:: localcontext(ctx=None, **kwargs)

   Trả về một context manager đặt context hiện tại của luồng đang hoạt động thành một bản sao của *ctx* khi bắt đầu câu lệnh with và khôi phục context trước đó khi thoát khỏi câu lệnh with. Nếu không chỉ định context, một bản sao của context hiện tại sẽ được sử dụng. Đối số *kwargs* được dùng để đặt các thuộc tính của context mới.

   Ví dụ: đoạn mã sau đặt độ chính xác thập phân hiện tại thành 42 chữ số, thực hiện một phép tính, rồi tự động khôi phục context trước đó::

      from decimal import localcontext

      with localcontext() as ctx:
          ctx.prec = 42   # Thực hiện phép tính với độ chính xác cao
          s = calculate_something()
      s = +s  # Làm tròn kết quả cuối cùng về độ chính xác mặc định

   Nếu sử dụng các đối số keyword, đoạn mã sẽ như sau::

      from decimal import localcontext

      with localcontext(prec=42) as ctx:
          s = calculate_something()
      s = +s

   Tăng :exc:`TypeError` nếu *kwargs* cung cấp một thuộc tính mà :class:`Context` không hỗ trợ. Tăng :exc:`TypeError` hoặc :exc:`ValueError` nếu *kwargs* cung cấp một giá trị không hợp lệ cho một thuộc tính.

   .. versionchanged:: 3.11
      :meth:`localcontext` now supports setting context attributes through the use of keyword arguments.

.. function:: IEEEContext(bits)

   Trả về một đối tượng context được khởi tạo với các giá trị thích hợp cho một trong các định dạng trao đổi IEEE. Đối số phải là bội số của 32 và nhỏ hơn :const:`IEEE_CONTEXT_MAX_BITS`.

   .. versionadded:: 3.14

Bạn cũng có thể tạo các context mới bằng constructor :class:`Context` được mô tả bên dưới. Ngoài ra, module còn cung cấp ba context được tạo sẵn:


.. data:: BasicContext

   Đây là một context tiêu chuẩn được định nghĩa bởi General Decimal Arithmetic Specification. Precision được đặt là chín. Rounding được đặt thành
   :const:`ROUND_HALF_UP`. Tất cả các flag đều được xóa. Tất cả các trap đều được bật (được xử lý như các exception), ngoại trừ :const:`Inexact`, :const:`Rounded`, và
   :const:`Subnormal`.

   Vì nhiều trap được bật, context này hữu ích cho việc debugging.


.. data:: ExtendedContext

   Đây là một context tiêu chuẩn được định nghĩa bởi General Decimal Arithmetic Specification. Precision được đặt là chín. Rounding được đặt thành
   :const:`ROUND_HALF_EVEN`. Tất cả các flag đều được xóa. Không có trap nào được bật (vì vậy exception sẽ không được raise trong quá trình tính toán).

   Vì các trap bị tắt, context này hữu ích cho những ứng dụng muốn nhận giá trị kết quả là ``NaN`` hoặc ``Infinity`` thay vì raise exception. Điều này cho phép ứng dụng hoàn tất một lần chạy ngay cả khi gặp các điều kiện mà nếu không sẽ làm chương trình dừng lại.


.. data:: DefaultContext

   Context này được hàm :class:`Context` sử dụng làm nguyên mẫu cho các context mới. Việc thay đổi một trường (chẳng hạn như precision) sẽ làm thay đổi giá trị mặc định cho các context mới được tạo bởi hàm :class:`Context`.

   Context này hữu ích nhất trong các môi trường đa luồng. Việc thay đổi một trong các trường trước khi các luồng được khởi động sẽ có tác dụng thiết lập các giá trị mặc định trên toàn hệ thống. Không nên thay đổi các trường sau khi các luồng đã được khởi động, vì điều đó sẽ yêu cầu đồng bộ hóa luồng để ngăn ngừa các race condition.

   Trong các môi trường đơn luồng, tốt hơn hết là không sử dụng context này. Thay vào đó, chỉ cần tạo các context một cách tường minh như mô tả bên dưới.

   Các giá trị mặc định là :attr:`Context.prec`\ =\ ``28``,
   :attr:`Context.rounding`\ =\ :const:`ROUND_HALF_EVEN`, và các trap được bật cho :class:`Overflow`, :class:`InvalidOperation`, và
   :class:`DivisionByZero`.

Ngoài ba context được cung cấp, có thể tạo các context mới bằng hàm
:class:`Context`.


.. class:: Context(prec=None, rounding=None, Emin=None, Emax=None, capitals=None, clamp=None, flags=None, traps=None)

   Tạo một context mới. Nếu một trường không được chỉ định hoặc là :const:`None`, các giá trị mặc định sẽ được sao chép từ :const:`DefaultContext`. Nếu trường *flags* không được chỉ định hoặc là :const:`None`, tất cả các flag sẽ được xóa.

   .. attribute:: prec

      Một số nguyên trong phạm vi [``1``, :const:`MAX_PREC`] dùng để thiết lập độ chính xác cho các phép toán số học trong context.

   .. attribute:: rounding

      Một trong các hằng số được liệt kê trong phần `Chế độ làm tròn <Rounding Modes_>`_.

   .. attribute:: traps
                  flags

      Danh sách các signal cần thiết lập. Thông thường, context mới chỉ nên thiết lập các trap và để các flag ở trạng thái đã xóa.

   .. attribute:: Emin
                  Emax

      Các số nguyên chỉ định giới hạn ngoài cho phép của số mũ. *Emin* phải nằm trong phạm vi [:const:`MIN_EMIN`, ``0``], còn *Emax* phải nằm trong phạm vi [``0``, :const:`MAX_EMAX`].

   .. attribute:: capitals

      ``0`` hoặc ``1`` (mặc định). Nếu được đặt thành ``1``, số mũ được in bằng ``E`` viết hoa; nếu không, ``e`` viết thường được sử dụng: ``Decimal('6.02e+23')``.

   .. attribute:: clamp

      ``0`` (mặc định) hoặc ``1``. Nếu được đặt thành ``1``, số mũ ``e`` của một thực thể :class:`Decimal` có thể biểu diễn trong context này bị giới hạn nghiêm ngặt trong phạm vi ``Emin - prec + 1 <= e <= Emax - prec + 1``. Nếu *clamp* là ``0`` thì điều kiện yếu hơn được áp dụng: số mũ đã điều chỉnh của thực thể :class:`Decimal` nhiều nhất là :attr:`~Context.Emax`. Khi *clamp* là ``1``, một số chuẩn lớn, nếu có thể, sẽ được giảm số mũ và thêm số lượng số 0 tương ứng vào coefficient của nó để phù hợp với các ràng buộc về số mũ; điều này bảo toàn giá trị của số nhưng làm mất thông tin về các số 0 có nghĩa ở cuối. Ví dụ::

         >>> Context(prec=6, Emax=999, clamp=1).create_decimal('1.23e999')
         Decimal('1.23000E+999')

      Giá trị *clamp* bằng ``1`` cho phép tương thích với các định dạng trao đổi số thập phân có độ rộng cố định được quy định trong IEEE 754.

   Lớp :class:`Context` định nghĩa một số phương thức đa dụng cũng như nhiều phương thức để thực hiện phép toán trực tiếp trong một context nhất định. Ngoài ra, với mỗi phương thức :class:`Decimal` được mô tả ở trên (ngoại trừ các phương thức :meth:`~Decimal.adjusted` và :meth:`~Decimal.as_tuple`), có một phương thức :class:`Context` tương ứng. Ví dụ, với một thực thể :class:`Context` ``C`` và thực thể :class:`Decimal` ``x``, ``C.exp(x)`` tương đương với ``x.exp(context=C)``. Mỗi phương thức :class:`Context` chấp nhận một số nguyên Python (một thực thể của :class:`int`) ở bất kỳ vị trí nào chấp nhận một thực thể Decimal.


   .. method:: clear_flags()

      Đặt lại tất cả các cờ về ``0``.

   .. method:: clear_traps()

      Đặt lại tất cả các trap về ``0``.

      .. versionadded:: 3.3

   .. method:: copy()

      Trả về một bản sao của context.

   .. method:: copy_decimal(num, /)

      Trả về một bản sao của instance Decimal num.

   .. method:: create_decimal(num='0', /)

      Tạo một instance Decimal mới từ *num* nhưng sử dụng *self* làm context. Không giống :class:`Decimal` constructor, precision, phương thức làm tròn, flags và traps của context được áp dụng cho quá trình chuyển đổi.

      Điều này hữu ích vì các hằng số thường được cung cấp với precision lớn hơn mức ứng dụng cần. Một lợi ích khác là việc làm tròn ngay lập tức loại bỏ các tác động ngoài ý muốn của những chữ số vượt quá precision hiện tại. Trong ví dụ sau, việc sử dụng các đầu vào chưa được làm tròn có nghĩa là cộng zero vào một tổng có thể làm thay đổi kết quả:

      .. doctest:: newcontext

         >>> getcontext().prec = 3
         >>> Decimal('3.4445') + Decimal('1.0023')
         Decimal('4.45')
         >>> Decimal('3.4445') + Decimal(0) + Decimal('1.0023')
         Decimal('4.44')

      Phương thức này triển khai thao tác to-number trong đặc tả IBM. Nếu đối số là một chuỗi, không được phép có khoảng trắng hoặc dấu gạch dưới ở đầu hay cuối.

   .. method:: create_decimal_from_float(f, /)

      Tạo một instance Decimal mới từ một float *f* nhưng thực hiện làm tròn bằng cách sử dụng *self* làm context. Không giống class method :meth:`Decimal.from_float`, precision, phương thức làm tròn, flags và traps của context được áp dụng cho quá trình chuyển đổi.

      .. doctest::

         >>> context = Context(prec=5, rounding=ROUND_DOWN)
         >>> context.create_decimal_from_float(math.pi)
         Decimal('3.1415')
         >>> context = Context(prec=5, traps=[Inexact])
         >>> context.create_decimal_from_float(math.pi)
         Traceback (most recent call last):
             ...
         decimal.Inexact: None

      .. versionadded:: 3.1

   .. method:: Etiny()

      Trả về một giá trị bằng ``Emin - prec + 1``, là giá trị exponent tối thiểu cho các kết quả subnormal. Khi xảy ra underflow, exponent được đặt thành :const:`Etiny`.

   .. method:: Etop()

      Trả về một giá trị bằng ``Emax - prec + 1``.

   Cách tiếp cận thông thường khi làm việc với số thập phân là tạo các thực thể :class:`Decimal` rồi áp dụng các phép toán số học diễn ra trong context hiện tại của thread đang hoạt động. Một cách tiếp cận khác là sử dụng các phương thức của context để tính toán trong một context cụ thể. Các phương thức này tương tự như các phương thức của lớp :class:`Decimal` và chỉ được nhắc lại ngắn gọn ở đây.


   .. method:: abs(x, /)

      Trả về giá trị tuyệt đối của *x*.


   .. method:: add(x, y, /)

      Trả về tổng của *x* và *y*.


   .. method:: canonical(x, /)

      Trả về chính đối tượng Decimal *x*.


   .. method:: compare(x, y, /)

      So sánh *x* và *y* theo giá trị số.


   .. method:: compare_signal(x, y, /)

      So sánh các giá trị của hai toán hạng theo giá trị số.


   .. method:: compare_total(x, y, /)

      So sánh hai toán hạng bằng cách sử dụng biểu diễn trừu tượng của chúng.


   .. method:: compare_total_mag(x, y, /)

      So sánh hai toán hạng bằng biểu diễn trừu tượng của chúng, bỏ qua dấu.


   .. method:: copy_abs(x, /)

      Trả về một bản sao của *x* với dấu được đặt thành 0.


   .. method:: copy_negate(x, /)

      Trả về một bản sao của *x* với dấu bị đảo ngược.


   .. method:: copy_sign(x, y, /)

      Sao chép dấu từ *y* sang *x*.


   .. method:: divide(x, y, /)

      Trả về *x* chia cho *y*.


   .. method:: divide_int(x, y, /)

      Trả về *x* chia cho *y*, được cắt ngắn thành một số nguyên.


   .. method:: divmod(x, y, /)

      Chia hai số và trả về phần nguyên của kết quả.


   .. method:: exp(x, /)

      Trả về ``e ** x``.


   .. method:: fma(x, y, z, /)

      Trả về *x* nhân với *y*, cộng với *z*.


   .. method:: is_canonical(x, /)

      Trả về ``True`` nếu *x* là số chính tắc; nếu không, trả về ``False``.


   .. method:: is_finite(x, /)

      Trả về ``True`` nếu *x* là số hữu hạn; nếu không, trả về ``False``.


   .. method:: is_infinite(x, /)

      Trả về ``True`` nếu *x* là vô hạn; nếu không, trả về ``False``.


   .. method:: is_nan(x, /)

      Trả về ``True`` nếu *x* là qNaN hoặc sNaN; nếu không, trả về ``False``.


   .. method:: is_normal(x, /)

      Trả về ``True`` nếu *x* là một số bình thường; nếu không, trả về ``False``.


   .. method:: is_qnan(x, /)

      Trả về ``True`` nếu *x* là NaN im lặng; nếu không, trả về ``False``.


   .. method:: is_signed(x, /)

      Trả về ``True`` nếu *x* là số âm; nếu không, trả về ``False``.


   .. method:: is_snan(x, /)

      Trả về ``True`` nếu *x* là NaN báo hiệu; nếu không, trả về ``False``.


   .. method:: is_subnormal(x, /)

      Trả về ``True`` nếu *x* là số dưới chuẩn; nếu không, trả về ``False``.


   .. method:: is_zero(x, /)

      Trả về ``True`` nếu *x* là số 0; nếu không, trả về ``False``.


   .. method:: ln(x, /)

      Trả về logarit tự nhiên (cơ số e) của *x*.


   .. method:: log10(x, /)

      Trả về logarit cơ số 10 của *x*.


   .. method:: logb(x, /)

       Trả về số mũ của độ lớn của MSD của toán hạng.


   .. method:: logical_and(x, y, /)

      Áp dụng phép toán logic *and* giữa các chữ số của mỗi toán hạng.


   .. method:: logical_invert(x, /)

      Đảo tất cả các chữ số trong *x*.


   .. method:: logical_or(x, y, /)

      Áp dụng phép toán logic *or* giữa các chữ số của mỗi toán hạng.


   .. method:: logical_xor(x, y, /)

      Áp dụng phép toán logic *xor* giữa các chữ số của mỗi toán hạng.


   .. method:: max(x, y, /)

      So sánh hai giá trị về mặt số học và trả về giá trị lớn nhất.


   .. method:: max_mag(x, y, /)

      So sánh các giá trị về mặt số học mà không xét dấu của chúng.


   .. method:: min(x, y, /)

      So sánh hai giá trị về mặt số học và trả về giá trị nhỏ nhất.


   .. method:: min_mag(x, y, /)

      So sánh các giá trị về mặt số học mà không xét dấu của chúng.


   .. method:: minus(x, /)

      Minus tương ứng với toán tử trừ tiền tố một ngôi trong Python.


   .. method:: multiply(x, y, /)

      Trả về tích của *x* và *y*.


   .. method:: next_minus(x, /)

      Trả về số lớn nhất có thể biểu diễn nhưng nhỏ hơn *x*.


   .. method:: next_plus(x, /)

      Trả về số nhỏ nhất có thể biểu diễn nhưng lớn hơn *x*.


   .. method:: next_toward(x, y, /)

      Trả về số gần nhất với *x*, theo hướng về phía *y*.


   .. method:: normalize(x, /)

      Rút gọn *x* về dạng đơn giản nhất.


   .. method:: number_class(x, /)

      Trả về thông tin cho biết lớp của *x*.


   .. method:: plus(x, /)

      Plus tương ứng với toán tử cộng một ngôi ở tiền tố trong Python. Thao tác này áp dụng độ chính xác và quy tắc làm tròn của context, vì vậy nó *không phải* là thao tác đồng nhất.


   .. method:: power(x, y, modulo=None)

      Trả về ``x`` lũy thừa ``y``, được rút gọn theo modulo ``modulo`` nếu được cung cấp.

      Với hai đối số, tính ``x**y``. Nếu ``x`` là số âm thì ``y`` phải là số nguyên. Kết quả sẽ không chính xác trừ khi ``y`` là số nguyên, đồng thời kết quả hữu hạn và có thể được biểu diễn chính xác bằng 'precision' chữ số. Chế độ làm tròn của context được sử dụng. Trong phiên bản Python, kết quả luôn được làm tròn chính xác.

      ``Decimal(0) ** Decimal(0)`` cho kết quả là ``InvalidOperation``, và nếu ``InvalidOperation`` không bị trap thì cho kết quả là ``Decimal('NaN')``.

      .. versionchanged:: 3.3
         Mô-đun C tính :meth:`power` dựa trên giá trị được làm tròn chính xác
         Các hàm :meth:`exp` và :meth:`ln`. Kết quả được xác định rõ, nhưng chỉ "gần như luôn được làm tròn chính xác".

      Với ba đối số, tính ``(x**y) % modulo``. Đối với dạng ba đối số, các đối số phải tuân theo những hạn chế sau:

      - cả ba đối số phải là số nguyên
      - ``y`` phải không âm
      - ít nhất một trong ``x`` hoặc ``y`` phải khác không
      - ``modulo`` phải khác không và có nhiều nhất 'precision' chữ số

      Giá trị thu được từ ``Context.power(x, y, modulo)`` bằng với giá trị sẽ nhận được khi tính ``(x**y) % modulo`` với độ chính xác không giới hạn, nhưng được tính hiệu quả hơn. Số mũ của kết quả bằng không, bất kể các số mũ của ``x``, ``y`` và ``modulo``. Kết quả luôn chính xác.


   .. method:: quantize(x, y, /)

      Trả về một giá trị bằng *x* (đã làm tròn), có số mũ của *y*.


   .. method:: radix()

      Chỉ trả về 10, vì đây là Decimal, :)


   .. method:: remainder(x, y, /)

      Trả về phần dư của phép chia nguyên.

      Dấu của kết quả, nếu khác 0, giống với dấu của số bị chia ban đầu.


   .. method:: remainder_near(x, y, /)

      Trả về ``x - y * n``, trong đó *n* là số nguyên gần nhất với giá trị chính xác của ``x / y`` (nếu kết quả là 0 thì dấu của nó sẽ là dấu của *x*).


   .. method:: rotate(x, y, /)

      Trả về một bản sao đã xoay của *x*, *y* lần.


   .. method:: same_quantum(x, y, /)

      Trả về ``True`` nếu hai toán hạng có cùng số mũ.


   .. method:: scaleb (x, y, /)

      Trả về toán hạng thứ nhất sau khi cộng số mũ của giá trị thứ hai vào nó.


   .. method:: shift(x, y, /)

      Trả về một bản sao đã dịch của *x*, *y* lần.


   .. method:: sqrt(x, /)

      Căn bậc hai của một số không âm với độ chính xác của context.


   .. method:: subtract(x, y, /)

      Trả về hiệu giữa *x* và *y*.


   .. method:: to_eng_string(x, /)

      Chuyển đổi thành chuỗi, sử dụng ký hiệu kỹ thuật nếu cần số mũ.

      Ký hiệu kỹ thuật có số mũ là bội số của 3. Điều này có thể để lại tối đa 3 chữ số ở bên trái dấu thập phân và có thể yêu cầu thêm một hoặc hai số 0 ở cuối.


   .. method:: to_integral_exact(x, /)

      Làm tròn thành một số nguyên.


   .. method:: to_sci_string(x, /)

      Chuyển đổi một số thành chuỗi bằng cách sử dụng ký hiệu khoa học.

.. %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

.. _decimal-rounding-modes:

Hằng số
-------

Các hằng số trong phần này chỉ liên quan đến mô-đun C. Chúng cũng được 포함 trong phiên bản Python thuần túy để đảm bảo khả năng tương thích.

+---------------------------------+----------------+--------------------------+
|                                 | 32-bit         | 64-bit                   |
+=================================+================+==========================+
| .. data:: MAX_PREC              | ``425000000``  | ``999999999999999999``   |
+---------------------------------+----------------+--------------------------+
| .. data:: MAX_EMAX              | ``425000000``  | ``999999999999999999``   |
+---------------------------------+----------------+--------------------------+
| .. data:: MIN_EMIN              | ``-425000000`` | ``-999999999999999999``  |
+---------------------------------+----------------+--------------------------+
| .. data:: MIN_ETINY             | ``-849999999`` | ``-1999999999999999997`` |
+---------------------------------+----------------+--------------------------+
| .. data:: IEEE_CONTEXT_MAX_BITS | ``256``        | ``512``                  |
+---------------------------------+----------------+--------------------------+

.. data:: HAVE_THREADS

   Giá trị là ``True``. Không còn được dùng, vì Python hiện luôn có thread.

   .. deprecated:: 3.9

.. data:: HAVE_CONTEXTVAR

   Giá trị mặc định là ``True``. Nếu Python là :option:`configured using the --without-decimal-contextvar option <--without-decimal-contextvar>`, phiên bản C sử dụng context thread-local thay vì coroutine-local và giá trị là ``False``. Điều này nhanh hơn một chút trong một số tình huống context lồng nhau.

   .. versionadded:: 3.8.3


.. _`Rounding modes`:

Các chế độ làm tròn
-------------------

.. data:: ROUND_CEILING

   Làm tròn về phía ``Infinity``.

.. data:: ROUND_DOWN

   Làm tròn về 0.

.. data:: ROUND_FLOOR

   Làm tròn về phía ``-Infinity``.

.. data:: ROUND_HALF_DOWN

   Làm tròn đến số gần nhất, nếu hòa thì làm tròn về 0.

.. data:: ROUND_HALF_EVEN

   Làm tròn đến số gần nhất, nếu hòa thì làm tròn đến số nguyên chẵn gần nhất.

.. data:: ROUND_HALF_UP

   Làm tròn đến số gần nhất, nếu hòa thì làm tròn ra xa 0.

.. data:: ROUND_UP

   Làm tròn ra xa số 0.

.. data:: ROUND_05UP

   Làm tròn ra xa số 0 nếu chữ số cuối cùng sau khi làm tròn về phía 0 sẽ là 0 hoặc 5; nếu không thì làm tròn về phía 0.


.. _decimal-signals:

Tín hiệu
--------

Tín hiệu biểu thị các điều kiện phát sinh trong quá trình tính toán. Mỗi tín hiệu tương ứng với một cờ ngữ cảnh và một bộ cho phép bẫy ngữ cảnh.

Cờ ngữ cảnh được đặt mỗi khi gặp điều kiện tương ứng. Sau khi tính toán xong, có thể kiểm tra các cờ này cho mục đích cung cấp thông tin (chẳng hạn để xác định phép tính có chính xác hay không). Sau khi kiểm tra các cờ, hãy nhớ xóa tất cả các cờ trước khi bắt đầu phép tính tiếp theo.

Nếu bộ cho phép bẫy của ngữ cảnh được đặt cho tín hiệu, điều kiện đó sẽ khiến một ngoại lệ Python được phát sinh. Ví dụ, nếu bẫy :class:`DivisionByZero` được đặt, thì một ngoại lệ :exc:`DivisionByZero` sẽ được phát sinh khi gặp điều kiện đó.


.. class:: Clamped

   Đã thay đổi số mũ để phù hợp với các ràng buộc biểu diễn.

   Thông thường, hiện tượng giới hạn xảy ra khi số mũ nằm ngoài các
   :attr:`~Context.Emin` và :attr:`~Context.Emax` của context. Nếu có thể, số mũ sẽ được giảm xuống cho phù hợp bằng cách thêm các số 0 vào coefficient.


.. class:: DecimalException

   Lớp cơ sở cho các signal khác và là lớp con của :exc:`ArithmeticError`.


.. class:: DivisionByZero

   Báo hiệu phép chia một số không vô hạn cho số 0.

   Có thể xảy ra khi chia, chia modulo hoặc khi nâng một số lên lũy thừa âm. Nếu signal này không bị trap, kết quả trả về là ``Infinity`` hoặc ``-Infinity``, với dấu được xác định bởi các đầu vào của phép tính.


.. class:: Inexact

   Cho biết đã xảy ra việc làm tròn và kết quả không chính xác tuyệt đối.

   Báo hiệu khi các chữ số khác 0 bị loại bỏ trong quá trình làm tròn. Kết quả đã làm tròn được trả về. Cờ signal hoặc trap được dùng để phát hiện khi kết quả không chính xác.


.. class:: InvalidOperation

   Đã thực hiện một thao tác không hợp lệ.

   Cho biết đã yêu cầu một thao tác không có ý nghĩa. Nếu không bị bắt, thao tác này trả về ``NaN``. Các nguyên nhân có thể bao gồm::

      Infinity - Infinity
      0 * Infinity
      Infinity / Infinity
      x % 0
      Infinity % x
      sqrt(-x) and x > 0
      0 ** 0
      x ** (non-integer)
      x ** Infinity


.. class:: Overflow

   Tràn số.

   Cho biết số mũ lớn hơn :attr:`Context.Emax` sau khi làm tròn. Nếu không bị bắt, kết quả phụ thuộc vào chế độ làm tròn: либо thu hẹp về số hữu hạn lớn nhất có thể biểu diễn, либо làm tròn ra ngoài thành ``Infinity``. Trong cả hai trường hợp, :class:`Inexact` và :class:`Rounded` cũng được phát tín hiệu.


.. class:: Rounded

   Đã xảy ra việc làm tròn, mặc dù có thể không mất thông tin nào.

   Được phát tín hiệu bất cứ khi nào việc làm tròn loại bỏ các chữ số, kể cả khi những chữ số đó là số 0 (chẳng hạn như làm tròn ``5.00`` thành ``5.0``). Nếu không bị bắt, trả về kết quả không thay đổi. Tín hiệu này được dùng để phát hiện việc mất các chữ số có nghĩa.


.. class:: Subnormal

   Số mũ thấp hơn :attr:`~Context.Emin` trước khi làm tròn.

   Xảy ra khi kết quả của một phép toán là số dưới chuẩn (số mũ quá nhỏ). Nếu không bị trap, kết quả được trả về không thay đổi.


.. class:: Underflow

   Tràn xuống số học với kết quả được làm tròn thành 0.

   Xảy ra khi một kết quả dưới chuẩn bị phép làm tròn đẩy về 0. :class:`Inexact` và :class:`Subnormal` cũng được phát tín hiệu.


.. class:: FloatOperation

    Bật ngữ nghĩa nghiêm ngặt hơn khi trộn float và Decimal.

    Nếu tín hiệu không bị trap (mặc định), việc trộn float và Decimal được cho phép trong hàm khởi tạo :class:`~decimal.Decimal`,
    :meth:`~decimal.Context.create_decimal` và tất cả các toán tử so sánh. Cả việc chuyển đổi lẫn so sánh đều chính xác. Mọi phép toán trộn đều được ghi nhận một cách im lặng bằng cách đặt :exc:`FloatOperation` trong các cờ của context. Các phép chuyển đổi tường minh bằng :meth:`~decimal.Decimal.from_float` hoặc :meth:`~decimal.Context.create_decimal_from_float` không đặt cờ này.

    Ngược lại (khi tín hiệu bị trap), chỉ các phép so sánh bằng và phép chuyển đổi tường minh là im lặng. Mọi phép toán trộn khác đều raise :exc:`FloatOperation`.


Bảng sau đây tóm tắt hệ thống phân cấp của các tín hiệu::

   exceptions.ArithmeticError(exceptions.Exception)
       DecimalException
           Clamped
           DivisionByZero(DecimalException, exceptions.ZeroDivisionError)
           Inexact
               Overflow(Inexact, Rounded)
               Underflow(Inexact, Rounded, Subnormal)
           InvalidOperation
           Rounded
           Subnormal
           FloatOperation(DecimalException, exceptions.TypeError)

.. %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



.. _decimal-notes:

Ghi chú về số dấu phẩy động
---------------------------


Giảm thiểu sai số làm tròn bằng cách tăng độ chính xác
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Việc sử dụng số dấu phẩy động thập phân loại bỏ lỗi biểu diễn thập phân (nhờ đó có thể biểu diễn chính xác ``0.1``); tuy nhiên, một số phép toán vẫn có thể phát sinh sai số làm tròn khi số chữ số khác 0 vượt quá độ chính xác cố định.

Ảnh hưởng của sai số làm tròn có thể được khuếch đại khi cộng hoặc trừ các đại lượng gần như triệt tiêu nhau, dẫn đến mất độ chính xác đáng kể. Knuth đưa ra hai ví dụ minh họa trong đó phép tính số dấu phẩy động đã làm tròn với độ chính xác không đủ gây ra sự phá vỡ các tính chất kết hợp và phân phối của phép cộng:

.. doctest:: newcontext

   # Các ví dụ từ Seminumerical Algorithms, Mục 4.2.2.
   >>> from decimal import Decimal, getcontext
   >>> getcontext().prec = 8

   >>> u, v, w = Decimal(11111113), Decimal(-11111111), Decimal('7.51111111')
   >>> (u + v) + w
   Decimal('9.5111111')
   >>> u + (v + w)
   Decimal('10')

   >>> u, v, w = Decimal(20000), Decimal(-6), Decimal('6.0000003')
   >>> (u*v) + (u*w)
   Decimal('0.01')
   >>> u * (v+w)
   Decimal('0.0060000')

Mô-đun :mod:`!decimal` cho phép khôi phục các đẳng thức bằng cách mở rộng độ chính xác đủ để tránh mất độ chính xác đáng kể:

.. doctest:: newcontext

   >>> getcontext().prec = 20
   >>> u, v, w = Decimal(11111113), Decimal(-11111111), Decimal('7.51111111')
   >>> (u + v) + w
   Decimal('9.51111111')
   >>> u + (v + w)
   Decimal('9.51111111')
   >>>
   >>> u, v, w = Decimal(20000), Decimal(-6), Decimal('6.0000003')
   >>> (u*v) + (u*w)
   Decimal('0.0060000')
   >>> u * (v+w)
   Decimal('0.0060000')


Các giá trị đặc biệt
^^^^^^^^^^^^^^^^^^^^

Hệ thống số của module :mod:`!decimal` cung cấp các giá trị đặc biệt, bao gồm ``NaN``, ``sNaN``, ``-Infinity``, ``Infinity`` và hai số 0 là ``+0`` và ``-0``.

Có thể tạo trực tiếp các giá trị vô cực bằng:  ``Decimal('Infinity')``. Ngoài ra, chúng có thể phát sinh khi chia cho 0 nếu tín hiệu :exc:`DivisionByZero` không bị bắt.  Tương tự, khi tín hiệu :exc:`Overflow` không bị bắt, kết quả làm tròn vượt quá giới hạn của số lớn nhất có thể biểu diễn cũng có thể là vô cực.

Các giá trị vô cực có dấu (affine) và có thể được sử dụng trong các phép toán số học, trong đó chúng được xử lý như những số rất lớn nhưng không xác định.  Chẳng hạn, cộng một hằng số với vô cực sẽ cho một kết quả vô cực khác.

Một số phép toán không xác định và trả về ``NaN``, hoặc nếu tín hiệu
:exc:`InvalidOperation` bị bắt thì phát sinh một ngoại lệ.  Ví dụ, ``0/0`` trả về ``NaN``, có nghĩa là "không phải một số".  Dạng ``NaN`` này là dạng im lặng và sau khi được tạo sẽ truyền qua các phép tính khác, luôn cho ra một ``NaN`` khác.  Hành vi này có thể hữu ích cho một chuỗi phép tính đôi khi bị thiếu đầu vào --- nó cho phép phép tính tiếp tục trong khi đánh dấu các kết quả cụ thể là không hợp lệ.

Một biến thể là ``sNaN``, biến thể này phát tín hiệu thay vì im lặng sau mỗi phép toán. Đây là một giá trị trả về hữu ích khi một kết quả không hợp lệ cần ngắt phép tính để được xử lý đặc biệt.

Hành vi của các toán tử so sánh trong Python có thể hơi bất ngờ khi có ``NaN`` tham gia. Phép kiểm tra bằng nhau trong đó một toán hạng là ``NaN`` im lặng hoặc báo hiệu luôn trả về :const:`False` (ngay cả khi thực hiện ``Decimal('NaN')==Decimal('NaN')``), còn phép kiểm tra không bằng luôn trả về
:const:`True`. Việc thử so sánh hai Decimal bằng bất kỳ toán tử ``<``, ``<=``, ``>`` hoặc ``>=`` nào sẽ phát tín hiệu :exc:`InvalidOperation` nếu một trong hai toán hạng là ``NaN``, và trả về :const:`False` nếu tín hiệu này không bị bắt. Lưu ý rằng đặc tả General Decimal Arithmetic không quy định hành vi của các phép so sánh trực tiếp; các quy tắc so sánh có liên quan đến ``NaN`` này được lấy từ tiêu chuẩn IEEE 854 (xem Bảng 3 trong mục 5.7). Để đảm bảo tuân thủ nghiêm ngặt các tiêu chuẩn, hãy sử dụng các phương thức :meth:`~Decimal.compare` và :meth:`~Decimal.compare_signal` thay thế.

Các số 0 có dấu có thể xuất hiện từ những phép tính bị underflow. Chúng giữ lại dấu lẽ ra sẽ có nếu phép tính được thực hiện với độ chính xác cao hơn. Vì độ lớn của chúng bằng 0, cả số 0 dương và số 0 âm đều được xem là bằng nhau, còn dấu của chúng chỉ mang tính thông tin.

Ngoài hai số 0 có dấu, khác nhau nhưng bằng nhau, còn có nhiều cách biểu diễn số 0 với độ chính xác khác nhau nhưng giá trị tương đương. Điều này cần một chút thời gian để làm quen. Với người đã quen với các biểu diễn dấu phẩy động chuẩn hóa, không dễ nhận ra ngay rằng phép tính sau trả về một giá trị bằng 0:

   >>> 1 / Decimal('Infinity')
   Decimal('0E-1000026')

.. %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


.. _decimal-threads:

Làm việc với thread
-------------------

Hàm :func:`getcontext` truy cập một đối tượng :class:`Context` khác nhau cho mỗi thread. Việc có các thread context riêng biệt nghĩa là các thread có thể thực hiện thay đổi (chẳng hạn như ``getcontext().prec=10``) mà không ảnh hưởng đến các thread khác.

Tương tự, hàm :func:`setcontext` tự động gán target của nó cho thread hiện tại.

Nếu :func:`setcontext` chưa được gọi trước :func:`getcontext` thì
:func:`getcontext` sẽ tự động tạo một ngữ cảnh mới để sử dụng trong thread hiện tại. Các đối tượng ngữ cảnh mới có các giá trị mặc định được thiết lập từ
đối tượng :data:`decimal.DefaultContext`.

Cờ :data:`sys.flags.thread_inherit_context` ảnh hưởng đến ngữ cảnh của các thread mới. Nếu cờ này là false, các thread mới sẽ bắt đầu với ngữ cảnh trống. Trong trường hợp này, :func:`getcontext` sẽ tạo một đối tượng ngữ cảnh mới khi được gọi và sử dụng các giá trị mặc định từ *DefaultContext*. Nếu cờ này là true, các thread mới sẽ bắt đầu với một bản sao ngữ cảnh từ bên gọi
:meth:`threading.Thread.start`.

Để kiểm soát các giá trị mặc định sao cho mỗi thread sử dụng cùng một tập giá trị trong toàn bộ ứng dụng, hãy trực tiếp sửa đổi đối tượng *DefaultContext*. Việc này nên được thực hiện *trước* khi bất kỳ thread nào được khởi chạy, để không xảy ra race condition giữa các thread gọi :func:`getcontext`. Ví dụ::

   # Thiết lập các giá trị mặc định áp dụng trên toàn ứng dụng cho tất cả thread sắp được khởi chạy
   DefaultContext.prec = 12
   DefaultContext.rounding = ROUND_DOWN
   DefaultContext.traps = ExtendedContext.traps.copy()
   DefaultContext.traps[InvalidOperation] = 1
   setcontext(DefaultContext)

   # Sau đó, có thể khởi chạy các thread
   t1.start()
   t2.start()
   t3.start()
    . . .

.. %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


.. _decimal-recipes:

Công thức
---------

Dưới đây là một số công thức đóng vai trò như các hàm tiện ích và minh họa cách làm việc với lớp :class:`Decimal`::

   def moneyfmt(value, places=2, curr='', sep=',', dp='.',
                pos='', neg='-', trailneg=''):
       """Convert Decimal to a money formatted string.

       places:  required number of places after the decimal point
       curr:    optional currency symbol before the sign (may be blank)
       sep:     optional grouping separator (comma, period, space, or blank)
       dp:      decimal point indicator (comma or period)
                only specify as blank when places is zero
       pos:     optional sign for positive numbers: '+', space or blank
       neg:     optional sign for negative numbers: '-', '(', space or blank
       trailneg:optional trailing minus indicator:  '-', ')', space or blank

       >>> d = Decimal('-1234567.8901')
       >>> moneyfmt(d, curr='$')
       '-$1,234,567.89'
       >>> moneyfmt(d, places=0, sep='.', dp='', neg='', trailneg='-')
       '1.234.568-'
       >>> moneyfmt(d, curr='$', neg='(', trailneg=')')
       '($1,234,567.89)'
       >>> moneyfmt(Decimal(123456789), sep=' ')
       '123 456 789.00'
       >>> moneyfmt(Decimal('-0.02'), neg='<', trailneg='>')
       '<0.02>'

       """
       q = Decimal(10) ** -places      # 2 chữ số thập phân --> '0.01'
       sign, digits, exp = value.quantize(q).as_tuple()
       result = []
       digits = list(map(str, digits))
       build, next = result.append, digits.pop
       if sign:
           build(trailneg)
       for i in range(places):
           build(next() if digits else '0')
       if places:
           build(dp)
       if not digits:
           build('0')
       i = 0
       while digits:
           build(next())
           i += 1
           if i == 3 and digits:
               i = 0
               build(sep)
       build(curr)
       build(neg if sign else pos)
       return ''.join(reversed(result))

   def pi():
       """Compute Pi to the current precision.

       >>> print(pi())
       3.141592653589793238462643383

       """
       getcontext().prec += 2  # các chữ số bổ sung cho những bước trung gian
       three = Decimal(3)      # thay "three=3.0" cho các số thực thông thường
       lasts, t, s, n, na, d, da = 0, three, 3, 1, 0, 0, 24
       while s != lasts:
           lasts = s
           n, na = n+na, na+8
           d, da = d+da, da+32
           t = (t * n) / d
           s += t
       getcontext().prec -= 2
       return +s               # dấu cộng một ngôi áp dụng độ chính xác mới

   def exp(x):
       """Return e raised to the power of x.  Result type matches input type.

       >>> print(exp(Decimal(1)))
       2.718281828459045235360287471
       >>> print(exp(Decimal(2)))
       7.389056098930650227230427461
       >>> print(exp(2.0))
       7.38905609893
       >>> print(exp(2+0j))
       (7.38905609893+0j)

       """
       getcontext().prec += 2
       i, lasts, s, fact, num = 0, 0, 1, 1, 1
       while s != lasts:
           lasts = s
           i += 1
           fact *= i
           num *= x
           s += num / fact
       getcontext().prec -= 2
       return +s

   def cos(x):
       """Return the cosine of x as measured in radians.

       The Taylor series approximation works best for a small value of x.
       For larger values, first compute x = x % (2 * pi).

       >>> print(cos(Decimal('0.5')))
       0.8775825618903727161162815826
       >>> print(cos(0.5))
       0.87758256189
       >>> print(cos(0.5+0j))
       (0.87758256189+0j)

       """
       getcontext().prec += 2
       i, lasts, s, fact, num, sign = 0, 0, 1, 1, 1, 1
       while s != lasts:
           lasts = s
           i += 2
           fact *= i * (i-1)
           num *= x * x
           sign *= -1
           s += num / fact * sign
       getcontext().prec -= 2
       return +s

   def sin(x):
       """Return the sine of x as measured in radians.

       The Taylor series approximation works best for a small value of x.
       For larger values, first compute x = x % (2 * pi).

       >>> print(sin(Decimal('0.5')))
       0.4794255386042030002732879352
       >>> print(sin(0.5))
       0.479425538604
       >>> print(sin(0.5+0j))
       (0.479425538604+0j)

       """
       getcontext().prec += 2
       i, lasts, s, fact, num, sign = 1, 0, x, 1, x, 1
       while s != lasts:
           lasts = s
           i += 2
           fact *= i * (i-1)
           num *= x * x
           sign *= -1
           s += num / fact * sign
       getcontext().prec -= 2
       return +s


.. %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


.. _decimal-faq:

Câu hỏi thường gặp về Decimal
-----------------------------

H: Việc gõ ``decimal.Decimal('1234.5')`` khá bất tiện. Có cách nào giảm số lần gõ khi sử dụng trình thông dịch tương tác không?

Đ: Một số người dùng viết tắt hàm khởi tạo thành chỉ một chữ cái:

   >>> D = decimal.Decimal
   >>> D('1.23') + D('3.45')
   Decimal('4.68')

H: Trong một ứng dụng fixed-point có hai chữ số thập phân, một số đầu vào có nhiều chữ số và cần được làm tròn. Những đầu vào khác không được có chữ số dư thừa và cần được xác thực. Nên sử dụng những phương thức nào?

Đ: Phương thức :meth:`~Decimal.quantize` làm tròn đến một số chữ số thập phân cố định. Nếu trap :const:`Inexact` được thiết lập, phương thức này cũng hữu ích cho việc xác thực:

   >>> TWOPLACES = Decimal(10) ** -2       # giống như Decimal('0.01')

   >>> # Làm tròn đến hai chữ số
   >>> Decimal('3.214').quantize(TWOPLACES)
   Decimal('3.21')

   >>> # Xác thực rằng một số không vượt quá hai chữ số
   >>> Decimal('3.21').quantize(TWOPLACES, context=Context(traps=[Inexact]))
   Decimal('3.21')

   >>> Decimal('3.214').quantize(TWOPLACES, context=Context(traps=[Inexact]))
   Traceback (most recent call last):
      ...
   Inexact: None

H: Khi đã có các đầu vào hợp lệ với hai chữ số thập phân, làm thế nào để duy trì bất biến đó trong suốt ứng dụng?

Đ: Một số phép toán như cộng, trừ và nhân với một số nguyên sẽ tự động bảo toàn fixed-point. Các phép toán khác, như chia và nhân với số không nguyên, sẽ thay đổi số chữ số thập phân và cần được thực hiện tiếp theo bằng một bước :meth:`~Decimal.quantize`:

    >>> a = Decimal('102.72')           # Các giá trị fixed-point ban đầu
    >>> b = Decimal('3.17')
    >>> a + b                           # Phép cộng bảo toàn fixed-point
    Decimal('105.89')
    >>> a - b
    Decimal('99.55')
    >>> a * 42                          # Phép nhân với số nguyên cũng vậy
    Decimal('4314.24')
    >>> (a * b).quantize(TWOPLACES)     # Phải quantize phép nhân với số không nguyên
    Decimal('325.62')
    >>> (b / a).quantize(TWOPLACES)     # Và quantize phép chia
    Decimal('0.03')

Khi phát triển các ứng dụng fixed-point, việc định nghĩa các hàm để xử lý bước :meth:`~Decimal.quantize` sẽ rất thuận tiện:

    >>> def mul(x, y, fp=TWOPLACES):
    ...     return (x * y).quantize(fp)
    ...
    >>> def div(x, y, fp=TWOPLACES):
    ...     return (x / y).quantize(fp)

    >>> mul(a, b)                       # Tự động bảo toàn fixed-point
    Decimal('325.62')
    >>> div(b, a)
    Decimal('0.03')

H: Có nhiều cách để biểu diễn cùng một giá trị. Các số ``200``, ``200.000``, ``2E2`` và ``.02E+4`` đều có cùng giá trị ở các độ chính xác khác nhau. Có cách nào biến chúng thành một giá trị chuẩn duy nhất, dễ nhận biết không?

Đ: Phương thức :meth:`~Decimal.normalize` ánh xạ tất cả các giá trị tương đương về cùng một đại diện duy nhất:

   >>> values = map(Decimal, '200 200.000 2E2 .02E+4'.split())
   >>> [v.normalize() for v in values]
   [Decimal('2E+2'), Decimal('2E+2'), Decimal('2E+2'), Decimal('2E+2')]

H: Khi nào việc làm tròn xảy ra trong một phép tính?

Đ: Việc đó xảy ra *sau* khi thực hiện phép tính. Triết lý của đặc tả decimal là các số được xem là chính xác và được tạo độc lập với context hiện tại. Chúng thậm chí có thể có độ chính xác cao hơn context hiện tại. Các phép tính được thực hiện với những đầu vào chính xác đó, sau đó việc làm tròn (hoặc các thao tác context khác) được áp dụng cho *kết quả* của phép tính::

   >>> getcontext().prec = 5
   >>> pi = Decimal('3.1415926535')   # Hơn 5 chữ số
   >>> pi                             # Giữ lại tất cả các chữ số
   Decimal('3.1415926535')
   >>> pi + 0                         # Làm tròn sau khi cộng
   Decimal('3.1416')
   >>> pi - Decimal('0.00005')        # Trừ các số chưa làm tròn, rồi làm tròn
   Decimal('3.1415')
   >>> pi + 0 - Decimal('0.00005').   # Các giá trị trung gian được làm tròn
   Decimal('3.1416')

H: Một số giá trị thập phân luôn được in ở dạng ký pháp số mũ. Có cách nào để lấy biểu diễn không dùng số mũ không?

Đ: Với một số giá trị, ký pháp số mũ là cách duy nhất để thể hiện số chữ số có nghĩa trong phần định trị. Ví dụ, biểu diễn ``5.0E+3`` dưới dạng ``5000`` giữ nguyên giá trị nhưng không thể thể hiện độ chính xác hai chữ số ban đầu.

Nếu ứng dụng không cần theo dõi độ chính xác, bạn có thể dễ dàng loại bỏ số mũ và các số 0 ở cuối, làm mất độ chính xác nhưng vẫn giữ nguyên giá trị:

    >>> def remove_exponent(d):
    ...     return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()

    >>> remove_exponent(Decimal('5E+3'))
    Decimal('5000')

H: Có cách nào để chuyển một float thông thường thành :class:`Decimal` không?

Đ: Có, mọi số dấu phẩy động nhị phân đều có thể được biểu diễn chính xác dưới dạng Decimal, mặc dù việc chuyển đổi chính xác có thể đòi hỏi nhiều độ chính xác hơn mức trực giác mách bảo:

.. doctest::

    >>> Decimal(math.pi)
    Decimal('3.141592653589793115997963468544185161590576171875')

H: Trong một phép tính phức tạp, làm thế nào để tôi chắc chắn rằng mình không nhận được kết quả sai lệch do độ chính xác không đủ hoặc các bất thường về làm tròn?

Đ: Module decimal giúp dễ dàng kiểm tra kết quả. Một thực hành tốt là chạy lại các phép tính với độ chính xác cao hơn và nhiều chế độ làm tròn khác nhau. Các kết quả khác biệt đáng kể cho thấy độ chính xác không đủ, vấn đề về chế độ làm tròn, đầu vào không được điều kiện hóa tốt hoặc thuật toán không ổn định về mặt số học.

H: Tôi nhận thấy rằng độ chính xác của context được áp dụng cho kết quả của các phép toán nhưng không áp dụng cho đầu vào. Có điều gì cần lưu ý khi kết hợp các giá trị có độ chính xác khác nhau không?

Đ: Có. Nguyên tắc là mọi giá trị đều được xem là chính xác, và phép tính trên các giá trị đó cũng vậy. Chỉ các kết quả mới được làm tròn. Ưu điểm đối với đầu vào là "bạn nhập gì thì nhận được đúng thứ đó". Một nhược điểm là kết quả có thể trông kỳ lạ nếu bạn quên rằng đầu vào chưa được làm tròn:

.. doctest:: newcontext

   >>> getcontext().prec = 3
   >>> Decimal('3.104') + Decimal('2.104')
   Decimal('5.21')
   >>> Decimal('3.104') + Decimal('0.000') + Decimal('2.104')
   Decimal('5.20')

Giải pháp là tăng độ chính xác hoặc buộc làm tròn đầu vào bằng cách sử dụng phép toán cộng một ngôi:

.. doctest:: newcontext

   >>> getcontext().prec = 3
   >>> +Decimal('1.23456789')      # toán tử cộng một ngôi kích hoạt việc làm tròn
   Decimal('1.23')

Ngoài ra, có thể làm tròn đầu vào khi tạo bằng cách sử dụng
:meth:`Context.create_decimal` phương thức:

   >>> Context(prec=5, rounding=ROUND_DOWN).create_decimal('1.2345678')
   Decimal('1.2345')

Hỏi: Việc triển khai CPython có nhanh đối với các số lớn không?

Đáp: Có. Trong các triển khai CPython và PyPy3, các phiên bản C/CFFI của module decimal tích hợp thư viện `libmpdec <https://www.bytereef.org/mpdecimal/doc/libmpdec/index.html>`_ tốc độ cao để thực hiện phép tính số thực dấu phẩy động thập phân có độ chính xác tùy ý và được làm tròn chính xác [#]_. ``libmpdec`` sử dụng `phép nhân Karatsuba <https://en.wikipedia.org/wiki/Karatsuba_algorithm>`_ cho các số có kích thước trung bình và `Biến đổi số học lý thuyết <https://en.wikipedia.org/wiki/Discrete_Fourier_transform_(general)#Number-theoretic_transform>`_ cho các số rất lớn.

Ngữ cảnh phải được điều chỉnh để thực hiện số học chính xác với độ chính xác tùy ý. :attr:`~Context.Emin` và :attr:`~Context.Emax` luôn phải được đặt thành các giá trị tối đa, còn :attr:`~Context.clamp` luôn phải là 0 (giá trị mặc định). Việc đặt :attr:`~Context.prec` cần được thực hiện cẩn thận.

Cách dễ nhất để thử số học bignum là sử dụng giá trị tối đa cho :attr:`~Context.prec` cũng như [#]_::

    >>> setcontext(Context(prec=MAX_PREC, Emax=MAX_EMAX, Emin=MIN_EMIN))
    >>> x = Decimal(2) ** 256
    >>> x / 128
    Decimal('904625697166532776746648320380374280103671755200316906558262375061821325312')


Đối với các kết quả không chính xác, :const:`MAX_PREC` lớn hơn rất nhiều so với mức cần thiết trên các nền tảng 64-bit và bộ nhớ khả dụng sẽ không đủ::

   >>> Decimal(1) / 3
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   MemoryError

Trên các hệ thống có cơ chế cấp phát quá mức (ví dụ: Linux), một cách tiếp cận tinh vi hơn là điều chỉnh :attr:`~Context.prec` theo dung lượng RAM khả dụng. Giả sử bạn có 8GB RAM và dự kiến có 10 toán hạng đồng thời, mỗi toán hạng sử dụng tối đa 500MB::

   >>> import sys
   >>>
   >>> # Số chữ số tối đa cho một toán hạng sử dụng 500MB dưới dạng các từ 8 byte
   >>> # với 19 chữ số trên mỗi từ (bản build 32-bit sử dụng từ 4 byte và 9 chữ số):
   >>> maxdigits = 19 * ((500 * 1024**2) // 8)
   >>>
   >>> # Kiểm tra để đảm bảo điều này hoạt động:
   >>> c = Context(prec=maxdigits, Emax=MAX_EMAX, Emin=MIN_EMIN)
   >>> c.traps[Inexact] = True
   >>> setcontext(c)
   >>>
   >>> # Lấp đầy độ chính xác khả dụng bằng các chữ số 9:
   >>> x = Decimal(0).logical_invert() * 9
   >>> sys.getsizeof(x)
   524288112
   >>> x + 2
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     decimal.Inexact: [<class 'decimal.Inexact'>]

Nói chung (đặc biệt là trên các hệ thống không có cơ chế cấp phát quá mức), bạn nên ước tính các giới hạn chặt chẽ hơn nữa và đặt bẫy :attr:`Inexact` nếu dự kiến tất cả các phép tính đều chính xác.


.. [#]
    .. versionadded:: 3.3

.. [#]
    .. versionchanged:: 3.9
       Cách tiếp cận này hiện hoạt động với mọi kết quả chính xác, ngoại trừ các lũy thừa không nguyên.

.. _`The General Decimal Arithmetic Specification`: https://speleotrove.com/decimal/decarith.html
.. _`libmpdec`: https://www.bytereef.org/mpdecimal/doc/libmpdec/index.html
.. _`Karatsuba multiplication`: https://en.wikipedia.org/wiki/Karatsuba_algorithm
.. _`Number Theoretic Transform`: https://en.wikipedia.org/wiki/Discrete_Fourier_transform_(general)#Number-theoretic_transform
