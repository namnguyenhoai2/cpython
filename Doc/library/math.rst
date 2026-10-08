:mod:`!math` --- Các hàm toán học
=================================

.. module:: math
   :synopsis: Các hàm toán học (sin() v.v.).

.. testsetup::

   from math import fsum

--------------

Mô-đun này cung cấp quyền truy cập vào các hàm và hằng số toán học phổ biến, bao gồm cả những hàm và hằng số được định nghĩa theo tiêu chuẩn C.

Không thể sử dụng các hàm này với số phức; nếu cần hỗ trợ số phức, hãy sử dụng các hàm cùng tên từ mô-đun :mod:`cmath`. Sự phân biệt giữa các hàm hỗ trợ số phức và các hàm không hỗ trợ được đưa ra vì hầu hết người dùng không muốn học nhiều kiến thức toán học đến mức cần thiết để hiểu số phức. Việc nhận được một exception thay vì kết quả phức cho phép phát hiện sớm hơn số phức không mong muốn được sử dụng làm tham số, để lập trình viên có thể xác định nó được tạo ra ngay từ đầu như thế nào và vì sao.

Mô-đun này cung cấp các hàm sau. Trừ khi có ghi chú rõ ràng khác, tất cả đều trả về giá trị dạng float.


====================================================  ============================================
**Number-theoretic functions**
--------------------------------------------------------------------------------------------------
:func:`comb(n, k) <comb>`                             Number of ways to choose *k* items from *n* items without repetition and without order
:func:`factorial(n) <factorial>`                      *n* factorial
:func:`gcd(*integers) <gcd>`                          Greatest common divisor of the integer arguments
:func:`isqrt(n) <isqrt>`                              Integer square root of a nonnegative integer *n*
:func:`lcm(*integers) <lcm>`                          Least common multiple of the integer arguments
:func:`perm(n, k) <perm>`                             Number of ways to choose *k* items from *n* items without repetition and with order

**Floating point arithmetic**
--------------------------------------------------------------------------------------------------
:func:`ceil(x) <ceil>`                                Ceiling of *x*, the smallest integer greater than or equal to *x*
:func:`fabs(x) <fabs>`                                Absolute value of *x*
:func:`floor(x)  <floor>`                             Floor of *x*, the largest integer less than or equal to *x*
:func:`fma(x, y, z) <fma>`                            Fused multiply-add operation: ``(x * y) + z``
:func:`fmod(x, y) <fmod>`                             Remainder of division ``x / y``
:func:`modf(x) <modf>`                                Fractional and integer parts of *x*
:func:`remainder(x, y) <remainder>`                   Remainder of *x* with respect to *y*
:func:`trunc(x) <trunc>`                              Integer part of *x*

**Floating point manipulation functions**
--------------------------------------------------------------------------------------------------
:func:`copysign(x, y) <copysign>`                     Magnitude (absolute value) of *x* with the sign of *y*
:func:`frexp(x) <frexp>`                              Mantissa and exponent of *x*
:func:`isclose(a, b, rel_tol, abs_tol) <isclose>`     Check if the values *a* and *b* are close to each other
:func:`isfinite(x) <isfinite>`                        Check if *x* is neither an infinity nor a NaN
:func:`isinf(x) <isinf>`                              Check if *x* is a positive or negative infinity
:func:`isnan(x) <isnan>`                              Check if *x* is a NaN  (not a number)
:func:`ldexp(x, i) <ldexp>`                           ``x * (2**i)``, inverse of function :func:`frexp`
:func:`nextafter(x, y, steps) <nextafter>`            Floating-point value *steps* steps after *x* towards *y*
:func:`ulp(x) <ulp>`                                  Value of the least significant bit of *x*

**Power, exponential and logarithmic functions**
--------------------------------------------------------------------------------------------------
:func:`cbrt(x) <cbrt>`                                Cube root of *x*
:func:`exp(x) <exp>`                                  *e* raised to the power *x*
:func:`exp2(x) <exp2>`                                *2* raised to the power *x*
:func:`expm1(x) <expm1>`                              *e* raised to the power *x*, minus 1
:func:`log(x, base) <log>`                            Logarithm of *x* to the given base (*e* by default)
:func:`log1p(x) <log1p>`                              Natural logarithm of *1+x* (base *e*)
:func:`log2(x) <log2>`                                Base-2 logarithm of *x*
:func:`log10(x) <log10>`                              Base-10 logarithm of *x*
:func:`pow(x, y) <math.pow>`                          *x* raised to the power *y*
:func:`sqrt(x) <sqrt>`                                Square root of *x*

**Summation and product functions**
--------------------------------------------------------------------------------------------------
:func:`dist(p, q) <dist>`                             Euclidean distance between two points *p* and *q* given as an iterable of coordinates
:func:`fsum(iterable) <fsum>`                         Sum of values in the input *iterable*
:func:`hypot(*coordinates) <hypot>`                   Euclidean norm of an iterable of coordinates
:func:`prod(iterable, start) <prod>`                  Product of elements in the input *iterable* with a *start* value
:func:`sumprod(p, q) <sumprod>`                       Sum of products from two iterables *p* and *q*

**Angular conversion**
--------------------------------------------------------------------------------------------------
:func:`degrees(x) <degrees>`                          Convert angle *x* from radians to degrees
:func:`radians(x) <radians>`                          Convert angle *x* from degrees to radians

**Trigonometric functions**
--------------------------------------------------------------------------------------------------
:func:`acos(x) <acos>`                                Arc cosine of *x*
:func:`asin(x) <asin>`                                Arc sine of *x*
:func:`atan(x) <atan>`                                Arc tangent of *x*
:func:`atan2(y, x) <atan2>`                           ``atan(y / x)``
:func:`cos(x) <cos>`                                  Cosine of *x*
:func:`sin(x) <sin>`                                  Sine of *x*
:func:`tan(x) <tan>`                                  Tangent of *x*

**Hyperbolic functions**
--------------------------------------------------------------------------------------------------
:func:`acosh(x) <acosh>`                              Inverse hyperbolic cosine of *x*
:func:`asinh(x) <asinh>`                              Inverse hyperbolic sine of *x*
:func:`atanh(x) <atanh>`                              Inverse hyperbolic tangent of *x*
:func:`cosh(x) <cosh>`                                Hyperbolic cosine of *x*
:func:`sinh(x) <sinh>`                                Hyperbolic sine of *x*
:func:`tanh(x) <tanh>`                                Hyperbolic tangent of *x*

**Special functions**
--------------------------------------------------------------------------------------------------
:func:`erf(x) <erf>`                                  `Error function <https://en.wikipedia.org/wiki/Error_function>`_ at *x*
:func:`erfc(x) <erfc>`                                `Complementary error function <https://en.wikipedia.org/wiki/Error_function>`_ at *x*
:func:`gamma(x) <gamma>`                              `Gamma function <https://en.wikipedia.org/wiki/Gamma_function>`_ at *x*
:func:`lgamma(x) <lgamma>`                            Natural logarithm of the absolute value of the `Gamma function <https://en.wikipedia.org/wiki/Gamma_function>`_ at *x*

**Constants**
--------------------------------------------------------------------------------------------------
:data:`pi`                                            *π* = 3.141592...
:data:`e`                                             *e* = 2.718281...
:data:`tau`                                           *τ* = 2\ *π* = 6.283185...
:data:`inf`                                           Positive infinity
:data:`nan`                                           "Not a number" (NaN)
====================================================  ============================================


Các hàm lý thuyết số
--------------------

.. function:: comb(n, k)

   Trả về số cách chọn *k* phần tử từ *n* phần tử mà không lặp lại và không xét thứ tự.

   Cho kết quả là ``n! / (k! * (n - k)!)`` khi ``k <= n`` và cho kết quả bằng không khi ``k > n``.

   Còn được gọi là hệ số nhị thức vì nó tương đương với hệ số của số hạng thứ k trong khai triển đa thức của ``(1 + x)ⁿ``.

   Phát sinh :exc:`TypeError` nếu một trong hai đối số không phải là số nguyên. Phát sinh :exc:`ValueError` nếu một trong hai đối số là số âm.

   .. versionadded:: 3.8


.. function:: factorial(n)

   Trả về giai thừa của số nguyên không âm *n*.

   .. versionchanged:: 3.10
      Các số thực có giá trị nguyên (như ``5.0``) không còn được chấp nhận.


.. function:: gcd(*integers)

   Trả về ước chung lớn nhất của các đối số nguyên đã chỉ định. Nếu bất kỳ đối số nào khác không, giá trị trả về là số nguyên dương lớn nhất là ước của tất cả các đối số. Nếu tất cả các đối số đều bằng không, giá trị trả về là ``0``. ``gcd()`` không có đối số sẽ trả về ``0``.

   .. versionadded:: 3.5

   .. versionchanged:: 3.9
      Đã thêm hỗ trợ cho số lượng đối số tùy ý. Trước đây, chỉ hỗ trợ hai đối số.


.. function:: isqrt(n)

   Trả về căn bậc hai nguyên của số nguyên không âm *n*. Đây là phần nguyên của căn bậc hai chính xác của *n*, hay tương đương là số nguyên lớn nhất *a* sao cho *a*\ ² |nbsp| ≤ |nbsp| *n*.

   Trong một số ứng dụng, sẽ thuận tiện hơn nếu có số nguyên nhỏ nhất *a* sao cho *n* |nbsp| ≤ |nbsp| *a*\ ², hay nói cách khác là giá trị làm tròn lên của căn bậc hai chính xác của *n*. Với *n* dương, có thể tính giá trị này bằng ``a = 1 + isqrt(n - 1)``.

   .. versionadded:: 3.8


.. function:: lcm(*integers)

   Trả về bội chung nhỏ nhất của các đối số nguyên được chỉ định. Nếu tất cả các đối số đều khác không, giá trị trả về là số nguyên dương nhỏ nhất chia hết cho tất cả các đối số. Nếu bất kỳ đối số nào bằng không, giá trị trả về là ``0``. ``lcm()`` không có đối số sẽ trả về ``1``.

   .. versionadded:: 3.9


.. function:: perm(n, k=None)

   Trả về số cách chọn *k* phần tử từ *n* phần tử mà không lặp lại và có xét thứ tự.

   Cho kết quả là ``n! / (n - k)!`` khi ``k <= n`` và cho kết quả bằng 0 khi ``k > n``.

   Nếu *k* không được chỉ định hoặc là ``None``, thì *k* mặc định là *n* và hàm trả về ``n!``.

   Phát sinh :exc:`TypeError` nếu một trong hai đối số không phải là số nguyên. Phát sinh :exc:`ValueError` nếu một trong hai đối số là số âm.

   .. versionadded:: 3.8


Số học dấu phẩy động
--------------------

.. function:: ceil(x)

   Trả về giá trị trần của *x*, là số nguyên nhỏ nhất lớn hơn hoặc bằng *x*. Nếu *x* không phải là một số thực, ủy quyền cho :meth:`x.__ceil__ <object.__ceil__>`, hàm này phải trả về một giá trị :class:`~numbers.Integral`.


.. function:: fabs(x)

   Trả về giá trị tuyệt đối của *x*.


.. function:: floor(x)

   Trả về giá trị sàn của *x*, là số nguyên lớn nhất nhỏ hơn hoặc bằng *x*. Nếu *x* không phải là một số thực, ủy quyền cho :meth:`x.__floor__ <object.__floor__>`, hàm này phải trả về một giá trị :class:`~numbers.Integral`.


.. function:: fma(x, y, z)

   Phép toán fused multiply-add. Trả về ``(x * y) + z``, được tính như thể với độ chính xác và phạm vi vô hạn, sau đó làm tròn một lần duy nhất về định dạng ``float``. Phép toán này thường cho độ chính xác cao hơn biểu thức trực tiếp ``(x * y) + z``.

   Hàm này tuân theo đặc tả của phép toán fusedMultiplyAdd được mô tả trong tiêu chuẩn IEEE 754. Tiêu chuẩn để việc triển khai tự định nghĩa trong một trường hợp, cụ thể là kết quả của ``fma(0, inf, nan)`` và ``fma(inf, 0, nan)``. Trong các trường hợp này, ``math.fma`` trả về một NaN và không phát sinh ngoại lệ nào.

   .. versionadded:: 3.13


.. function:: fmod(x, y)

   Trả về phần dư dấu phẩy động của ``x / y``, như được định nghĩa bởi hàm thư viện C của nền tảng ``fmod(x, y)``. Lưu ý rằng biểu thức Python ``x % y`` có thể không trả về cùng một kết quả. Mục đích của tiêu chuẩn C là ``fmod(x, y)`` phải chính xác (về mặt toán học; với độ chính xác vô hạn) bằng ``x - n*y`` với một số nguyên *n* nào đó, sao cho kết quả có cùng dấu với *x* và độ lớn nhỏ hơn ``abs(y)``. ``x % y`` của Python thay vào đó trả về kết quả có dấu của *y*, và có thể không tính được chính xác với các đối số float. Ví dụ, ``fmod(-1e-100, 1e100)`` là ``-1e-100``, nhưng kết quả của ``-1e-100 % 1e100`` trong Python là ``1e100-1e-100``, không thể được biểu diễn chính xác dưới dạng float và được làm tròn thành giá trị đáng ngạc nhiên ``1e100``. Vì lý do này, hàm :func:`fmod` thường được ưu tiên khi làm việc với float, trong khi ``x % y`` của Python được ưu tiên khi làm việc với số nguyên.


.. function:: modf(x)

   Trả về phần phân số và phần nguyên của *x*. Cả hai kết quả đều mang dấu của *x* và là số thực.

   Lưu ý rằng :func:`modf` có mẫu gọi/trả về khác với các phiên bản tương đương trong C: hàm này nhận một đối số và trả về một cặp giá trị, thay vì trả về giá trị thứ hai thông qua một “tham số đầu ra” (trong Python không có khái niệm như vậy).


.. function:: remainder(x, y)

   Trả về phần dư theo kiểu IEEE 754 của *x* đối với *y*. Với *x* hữu hạn và *y* hữu hạn, khác 0, đây là hiệu ``x - n*y``, trong đó ``n`` là số nguyên gần nhất với giá trị chính xác của thương ``x / y``. Nếu ``x / y`` nằm chính xác giữa hai số nguyên liên tiếp, số nguyên chẵn gần nhất *even* được dùng cho ``n``. Do đó, phần dư ``r = remainder(x, y)`` luôn thỏa mãn ``abs(r) <= 0.5 * abs(y)``.

   Các trường hợp đặc biệt tuân theo IEEE 754: cụ thể, ``remainder(x, math.inf)`` là *x* với mọi *x* hữu hạn, còn ``remainder(x, 0)`` và ``remainder(math.inf, x)`` phát sinh :exc:`ValueError` với mọi *x* không phải NaN. Nếu kết quả của phép tính phần dư bằng 0, số 0 đó sẽ có cùng dấu với *x*.

   Trên các nền tảng sử dụng số thực nhị phân theo IEEE 754, kết quả của phép toán này luôn biểu diễn được chính xác: không phát sinh sai số làm tròn.

   .. versionadded:: 3.7


.. function:: trunc(x)

   Trả về *x* sau khi loại bỏ phần phân số, giữ lại phần nguyên. Phép toán này làm tròn về 0: ``trunc()`` tương đương với :func:`floor` đối với *x* dương và tương đương với :func:`ceil` đối với *x* âm. Nếu *x* không phải là số thực, hàm ủy quyền cho :meth:`x.__trunc__ <object.__trunc__>`, hàm này sẽ trả về một giá trị :class:`~numbers.Integral`.


Đối với các hàm :func:`ceil`, :func:`floor` và :func:`modf`, lưu ý rằng *mọi* số thực có độ lớn đủ lớn đều là số nguyên chính xác. Các số thực Python thường có không quá 53 bit độ chính xác (giống kiểu double của C trên nền tảng), trong trường hợp đó, mọi số thực *x* thỏa mãn ``abs(x) >= 2**52`` nhất thiết không có bit phân số.


Các hàm thao tác với số dấu phẩy động
-------------------------------------

.. function:: copysign(x, y)

   Trả về một số thực có độ lớn (giá trị tuyệt đối) của *x* nhưng có dấu của *y*. Trên các nền tảng hỗ trợ số 0 có dấu, ``copysign(1.0, -0.0)`` trả về *-1.0*.


.. function:: frexp(x)

   Trả về phần định trị và số mũ của *x* dưới dạng cặp ``(m, e)``. Nếu *x* là một số hữu hạn khác không, thì *m* là một số thực với ``0.5 <= abs(m) < 1.0`` và số nguyên *e* sao cho ``x == m * 2**e`` chính xác. Nếu không, trả về ``(x, 0)``. Cách này được dùng để “tách rời” biểu diễn nội bộ của một số thực theo cách khả chuyển.

   Lưu ý rằng :func:`frexp` có cách gọi và trả về khác với các hàm tương đương trong C: hàm này nhận một đối số và trả về một cặp giá trị, thay vì trả về giá trị thứ hai thông qua một “tham số đầu ra” (Python không có khái niệm này).

.. function:: isclose(a, b, *, rel_tol=1e-09, abs_tol=0.0)

   Trả về ``True`` nếu các giá trị *a* và *b* gần nhau, và ``False`` nếu không.

   Việc hai giá trị có được xem là gần nhau hay không được xác định dựa trên các dung sai tuyệt đối và tương đối đã cho. Nếu không xảy ra lỗi, kết quả sẽ là: ``abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)``.

   *rel_tol* là dung sai tương đối -- đây là độ chênh lệch tối đa được phép giữa *a* và *b*, tính tương đối so với giá trị tuyệt đối lớn hơn giữa *a* và *b*. Ví dụ, để đặt dung sai là 5%, hãy truyền ``rel_tol=0.05``. Dung sai mặc định là ``1e-09``, đảm bảo rằng hai giá trị giống nhau với độ chính xác khoảng 9 chữ số thập phân. *rel_tol* phải không âm và nhỏ hơn ``1.0``.

   *abs_tol* là dung sai tuyệt đối; giá trị mặc định là ``0.0`` và phải không âm. Khi so sánh ``x`` với ``0.0``, ``isclose(x, 0)`` được tính là ``abs(x) <= rel_tol  * abs(x)``, tức là ``False`` với mọi ``x`` khác không và *rel_tol* nhỏ hơn ``1.0``. Vì vậy, hãy thêm đối số *abs_tol* dương phù hợp vào lệnh gọi.

   Các giá trị đặc biệt theo IEEE 754 của ``NaN``, ``inf`` và ``-inf`` sẽ được xử lý theo các quy tắc của IEEE. Cụ thể, ``NaN`` không được xem là gần với bất kỳ giá trị nào khác, kể cả ``NaN``. ``inf`` và ``-inf`` chỉ được xem là gần với chính chúng.

   .. versionadded:: 3.5

   .. seealso::

      :pep:`485` -- Một hàm dùng để kiểm tra tính gần bằng nhau


.. function:: isfinite(x)

   Trả về ``True`` nếu *x* không phải là vô cực cũng không phải NaN, và trả về ``False`` trong trường hợp ngược lại. (Lưu ý rằng ``0.0`` *is* được xem là hữu hạn.)

   .. versionadded:: 3.2


.. function:: isinf(x)

   Trả về ``True`` nếu *x* là vô cực dương hoặc vô cực âm, và trả về ``False`` trong trường hợp ngược lại.


.. function:: isnan(x)

   Trả về ``True`` nếu *x* là NaN (không phải số), và trả về ``False`` trong trường hợp ngược lại.


.. function:: ldexp(x, i)

   Trả về ``x * (2**i)``. Về cơ bản, đây là nghịch đảo của hàm
   :func:`frexp`.


.. function:: nextafter(x, y, steps=1)

   Trả về giá trị dấu phẩy động *steps* bước tính từ *x* theo hướng về phía *y*.

   Nếu *x* bằng *y*, trả về *y*, trừ khi *steps* bằng không.

   Ví dụ:

   * ``math.nextafter(x, math.inf)`` tăng lên: về phía vô cực dương.
   * ``math.nextafter(x, -math.inf)`` giảm xuống: về phía vô cực âm.
   * ``math.nextafter(x, 0.0)`` tiến về số không.
   * ``math.nextafter(x, math.copysign(math.inf, x))`` ra xa số không.

   Xem thêm :func:`math.ulp`.

   .. versionadded:: 3.9

   .. versionchanged:: 3.12
      Đã thêm đối số *steps*.


.. function:: ulp(x)

   Trả về giá trị của bit ít có ý nghĩa nhất của số thực *x*:

   * Nếu *x* là NaN (không phải là một số), trả về *x*.
   * Nếu *x* là số âm, trả về ``ulp(-x)``.
   * Nếu *x* là vô cực dương, trả về *x*.
   * Nếu *x* bằng 0, trả về số thực dương *denormalized* nhỏ nhất có thể biểu diễn (nhỏ hơn số thực dương *normalized* nhỏ nhất, :data:`sys.float_info.min <sys.float_info>`).
   * Nếu *x* bằng số thực dương lớn nhất có thể biểu diễn, trả về giá trị của bit ít quan trọng nhất của *x*, sao cho số thực đầu tiên nhỏ hơn *x* là ``x - ulp(x)``.
   * Nếu không (*x* là một số hữu hạn dương), trả về giá trị của bit ít quan trọng nhất của *x*, sao cho số thực đầu tiên lớn hơn *x* là ``x + ulp(x)``.

   ULP là viết tắt của "Unit in the Last Place".

   Xem thêm :func:`math.nextafter` và :data:`sys.float_info.epsilon <sys.float_info>`.

   .. versionadded:: 3.9


Các hàm lũy thừa, hàm mũ và hàm logarithm
-----------------------------------------

.. function:: cbrt(x)

   Trả về căn bậc ba của *x*.

   .. versionadded:: 3.11


.. function:: exp(x)

   Trả về *e* lũy thừa *x*, trong đó *e* = 2.718281... là cơ số của logarithm tự nhiên.  Giá trị này thường chính xác hơn ``math.e ** x`` hoặc ``pow(math.e, x)``.


.. function:: exp2(x)

   Trả về *2* lũy thừa *x*.

   .. versionadded:: 3.11


.. function:: expm1(x)

   Trả về *e* lũy thừa *x*, rồi trừ 1.  Ở đây, *e* là cơ số của logarit tự nhiên.  Với các số thực dấu phẩy động *x* nhỏ, phép trừ trong ``exp(x) - 1`` có thể dẫn đến `sự mất độ chính xác đáng kể <https://en.wikipedia.org/wiki/Loss_of_significance>`_\;, hàm :func:`expm1` cung cấp một cách để tính đại lượng này với đầy đủ độ chính xác:

      >>> from math import exp, expm1
      >>> exp(1e-5) - 1  # cho kết quả chính xác đến 11 chữ số
      1.0000050000069649e-05
      >>> expm1(1e-5)    # kết quả chính xác với đầy đủ độ chính xác
      1.0000050000166668e-05

   .. versionadded:: 3.2


.. function:: log(x[, base])

   Với một đối số, trả về logarit tự nhiên của *x* (theo cơ số *e*).

   Với hai đối số, trả về logarit của *x* theo *cơ số* được chỉ định, được tính là ``log(x)/log(base)``.


.. function:: log1p(x)

   Trả về logarit tự nhiên của *1+x* (cơ số *e*). Kết quả được tính theo cách đảm bảo độ chính xác cho *x* gần bằng không.


.. function:: log2(x)

   Trả về logarithm cơ số 2 của *x*. Giá trị này thường chính xác hơn ``log(x, 2)``.

   .. versionadded:: 3.3

   .. seealso::

      :meth:`int.bit_length` trả về số bit cần thiết để biểu diễn một số nguyên ở dạng nhị phân, không bao gồm dấu và các số 0 ở đầu.


.. function:: log10(x)

   Trả về logarithm cơ số 10 của *x*. Giá trị này thường chính xác hơn ``log(x, 10)``.


.. function:: pow(x, y)

   Trả về *x* lũy thừa *y*. Các trường hợp đặc biệt tuân theo tiêu chuẩn IEEE 754 trong phạm vi có thể. Cụ thể, ``pow(1.0, x)`` và ``pow(x, 0.0)`` luôn trả về ``1.0``, ngay cả khi *x* là số 0 hoặc NaN. Nếu cả *x* và *y* đều hữu hạn, *x* là số âm và *y* không phải là số nguyên, thì ``pow(x, y)`` không được xác định và sẽ phát sinh :exc:`ValueError`.

   Không giống toán tử dựng sẵn ``**``, :func:`math.pow` chuyển đổi cả hai đối số sang kiểu :class:`float`. Sử dụng ``**`` hoặc toán tử dựng sẵn
   :func:`pow` để tính các lũy thừa số nguyên chính xác.

   .. versionchanged:: 3.11
      Các trường hợp đặc biệt ``pow(0.0, -inf)`` và ``pow(-0.0, -inf)`` đã được thay đổi để trả về ``inf`` thay vì phát sinh :exc:`ValueError`, nhằm nhất quán với IEEE 754.


.. function:: sqrt(x)

   Trả về căn bậc hai của *x*.


Các hàm tính tổng và tích
-------------------------

.. function:: dist(p, q)

   Trả về khoảng cách Euclid giữa hai điểm *p* và *q*, mỗi điểm được cung cấp dưới dạng một chuỗi (hoặc iterable) các tọa độ. Hai điểm phải có cùng số chiều.

   Gần tương đương với::

       sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))

   .. versionadded:: 3.8


.. function:: fsum(iterable)

   Trả về tổng số thực dấu phẩy động chính xác của các giá trị trong iterable. Tránh mất độ chính xác bằng cách theo dõi nhiều tổng bộ phận trung gian.

   Độ chính xác của thuật toán phụ thuộc vào các đảm bảo của phép tính IEEE-754 và trường hợp điển hình khi chế độ làm tròn là nửa về số chẵn. Trên một số bản dựng không phải Windows, thư viện C bên dưới sử dụng phép cộng với độ chính xác mở rộng và đôi khi có thể làm tròn hai lần một tổng trung gian, khiến bit có trọng số thấp nhất của tổng bị sai.

   Để xem thảo luận thêm và hai phương pháp thay thế, hãy xem `các công thức trong cookbook ASPN để tính tổng số thực dấu phẩy động chính xác <https://code.activestate.com/recipes/393090-binary-floating-point-summation-accurate-to-full-p/>`_\.


.. function:: hypot(*coordinates)

   Trả về chuẩn Euclid, ``sqrt(sum(x**2 for x in coordinates))``. Đây là độ dài của vectơ từ gốc tọa độ đến điểm được xác định bởi các tọa độ.

   Đối với một điểm hai chiều ``(x, y)``, điều này tương đương với việc tính cạnh huyền của một tam giác vuông bằng định lý Pythagore, ``sqrt(x*x + y*y)``.

   .. versionchanged:: 3.8
      Đã bổ sung hỗ trợ cho các điểm n chiều. Trước đây, chỉ trường hợp hai chiều được hỗ trợ.

   .. versionchanged:: 3.10
      Đã cải thiện độ chính xác của thuật toán để sai số tối đa nhỏ hơn 1 ulp (đơn vị ở chữ số cuối cùng). Thông thường hơn, kết quả hầu như luôn được làm tròn chính xác trong phạm vi 1/2 ulp.


.. function:: prod(iterable, *, start=1)

   Tính tích của tất cả các phần tử trong *iterable* đầu vào. Giá trị *start* mặc định cho tích là ``1``.

   Khi iterable trống, trả về giá trị start. Hàm này được thiết kế riêng để sử dụng với các giá trị số và có thể từ chối các kiểu không phải số.

   .. versionadded:: 3.8


.. function:: sumprod(p, q)

   Trả về tổng các tích của các giá trị từ hai iterable *p* và *q*.

   Phát sinh :exc:`ValueError` nếu các đầu vào không có cùng độ dài.

   Gần tương đương với::

       sum(map(operator.mul, p, q, strict=True))

   Đối với đầu vào float và int/float hỗn hợp, các tích và tổng trung gian được tính với độ chính xác mở rộng.

   .. versionadded:: 3.12


Chuyển đổi góc
--------------

.. function:: degrees(x)

   Chuyển đổi góc *x* từ radian sang độ.


.. function:: radians(x)

   Chuyển đổi góc *x* từ độ sang radian.


Các hàm lượng giác
------------------

.. function:: acos(x)

   Trả về arc cosine của *x*, tính bằng radian. Kết quả nằm trong khoảng từ ``0`` đến ``pi``.


.. function:: asin(x)

   Trả về arc sine của *x*, tính bằng radian. Kết quả nằm trong khoảng từ ``-pi/2`` đến ``pi/2``.


.. function:: atan(x)

   Trả về arc tangent của *x*, tính bằng radian. Kết quả nằm trong khoảng từ ``-pi/2`` đến ``pi/2``.


.. function:: atan2(y, x)

   Trả về ``atan(y / x)``, tính bằng radian. Kết quả nằm trong khoảng từ ``-pi`` đến ``pi``. Vector trong mặt phẳng từ gốc tọa độ đến điểm ``(x, y)`` tạo với trục X dương một góc bằng góc này. Điểm đặc biệt của :func:`atan2` là nó biết dấu của cả hai đầu vào, nên có thể tính đúng góc phần tư của góc. Ví dụ, ``atan(1)`` và ``atan2(1, 1)`` đều là ``pi/4``, nhưng ``atan2(-1, -1)`` là ``-3*pi/4``.


.. function:: cos(x)

   Trả về cosine của *x* radian.


.. function:: sin(x)

   Trả về sine của *x* radian.


.. function:: tan(x)

   Trả về tangent của *x* radian.


Các hàm hyperbolic
------------------

`Các hàm hyperbolic <https://en.wikipedia.org/wiki/Hyperbolic_functions>`_ là các hàm tương tự hàm lượng giác, nhưng dựa trên hyperbol thay vì đường tròn.

.. function:: acosh(x)

   Trả về cos hyperbolic ngược của *x*.


.. function:: asinh(x)

   Trả về sin hyperbolic ngược của *x*.


.. function:: atanh(x)

   Trả về tan hyperbolic ngược của *x*.


.. function:: cosh(x)

   Trả về cos hyperbolic của *x*.


.. function:: sinh(x)

   Trả về sin hyperbolic của *x*.


.. function:: tanh(x)

   Trả về tang hyperbolic của *x*.


Các hàm đặc biệt
----------------

.. function:: erf(x)

   Trả về `hàm sai số <https://en.wikipedia.org/wiki/Error_function>`_ tại *x*.

   Hàm :func:`erf` có thể được sử dụng để tính các hàm thống kê truyền thống như `phân phối chuẩn tích lũy <https://en.wikipedia.org/wiki/Cumulative_distribution_function>`_::

     def phi(x):
         'Cumulative distribution function for the standard normal distribution'
         return (1.0 + erf(x / sqrt(2.0))) / 2.0

   .. versionadded:: 3.2


.. function:: erfc(x)

   Trả về hàm sai số bù tại *x*.  `Hàm sai số bù <https://en.wikipedia.org/wiki/Error_function>`_ được định nghĩa là ``1.0 - erf(x)``.  Hàm này được sử dụng cho các giá trị lớn của *x* khi phép trừ một sẽ gây ra `mất độ chính xác <https://en.wikipedia.org/wiki/Loss_of_significance>`_\.

   .. versionadded:: 3.2


.. function:: gamma(x)

   Trả về `hàm Gamma <https://en.wikipedia.org/wiki/Gamma_function>`_ tại *x*.

   .. versionadded:: 3.2


.. function:: lgamma(x)

   Trả về logarit tự nhiên của giá trị tuyệt đối của hàm Gamma tại *x*.

   .. versionadded:: 3.2


Các hằng số
-----------

.. data:: pi

   Hằng số toán học *π* = 3.141592..., với độ chính xác khả dụng.


.. data:: e

   Hằng số toán học *e* = 2.718281..., với độ chính xác khả dụng.


.. data:: tau

   Hằng số toán học *τ* = 6.283185..., với độ chính xác khả dụng. Tau là hằng số đường tròn bằng 2\ *π*, tức tỷ số giữa chu vi và bán kính của một đường tròn. Để tìm hiểu thêm về Tau, hãy xem video `Pi vẫn sai <https://vimeo.com/147792667>`_ của Vi Hart và bắt đầu ăn mừng `ngày Tau <https://tauday.com/>`_ bằng cách ăn nhiều bánh gấp đôi!

   .. versionadded:: 3.6


.. data:: inf

   Giá trị dương vô cực dạng số thực dấu phẩy động. (Để biểu diễn âm vô cực, hãy dùng ``-math.inf``.) Tương đương với kết quả đầu ra của ``float('inf')``.

   .. versionadded:: 3.5


.. data:: nan

   Giá trị "không phải là một số" (NaN) dạng số thực dấu phẩy động. Tương đương với kết quả đầu ra của ``float('nan')``. Theo yêu cầu của `tiêu chuẩn IEEE-754 <https://en.wikipedia.org/wiki/IEEE_754>`_, ``math.nan`` và ``float('nan')`` không được xem là bằng bất kỳ giá trị số nào khác, kể cả chính chúng. Để kiểm tra xem một số có phải là NaN hay không, hãy dùng :func:`isnan` để kiểm tra NaN thay vì ``is`` hoặc ``==``. Ví dụ:

      >>> import math
      >>> math.nan == math.nan
      False
      >>> float('nan') == float('nan')
      False
      >>> math.isnan(math.nan)
      True
      >>> math.isnan(float('nan'))
      True

   .. versionadded:: 3.5

   .. versionchanged:: 3.11
      Hiện tại, nó luôn khả dụng.


.. impl-detail::

   Mô-đun :mod:`!math` chủ yếu gồm các wrapper mỏng quanh các hàm thư viện toán học C của nền tảng. Khi phù hợp, hành vi trong các trường hợp ngoại lệ tuân theo Phụ lục F của tiêu chuẩn C99. Trong bản triển khai hiện tại, các hàm sẽ phát sinh
   :exc:`ValueError` đối với các phép toán không hợp lệ như ``sqrt(-1.0)`` hoặc ``log(0.0)`` (khi Phụ lục F của C99 khuyến nghị báo hiệu phép toán không hợp lệ hoặc phép chia cho 0), và :exc:`OverflowError` đối với các kết quả bị tràn (ví dụ: ``exp(1000.0)``). Không hàm nào ở trên trả về NaN, trừ khi một hoặc nhiều đối số đầu vào là NaN; trong trường hợp đó, hầu hết các hàm sẽ trả về NaN, nhưng (một lần nữa, theo Phụ lục F của C99) có một số ngoại lệ đối với quy tắc này, chẳng hạn như ``pow(float('nan'), 0.0)`` hoặc ``hypot(float('nan'), float('inf'))``.

   Lưu ý rằng Python không cố gắng phân biệt NaN signaling với NaN quiet, và hành vi đối với NaN signaling vẫn chưa được đặc tả. Hành vi thông thường là xử lý mọi NaN như thể chúng là NaN quiet.


.. seealso::

   Mô-đun :mod:`cmath`
      Các phiên bản dành cho số phức của nhiều hàm trong số này.

.. |nbsp| unicode:: 0xA0
   :trim:

.. _`significant loss of precision`: https://en.wikipedia.org/wiki/Loss_of_significance
.. _`ASPN cookbook recipes for accurate floating-point summation`: https://code.activestate.com/recipes/393090-binary-floating-point-summation-accurate-to-full-p/
.. _`Hyperbolic functions`: https://en.wikipedia.org/wiki/Hyperbolic_functions
.. _`error function`: https://en.wikipedia.org/wiki/Error_function
.. _`cumulative standard normal distribution`: https://en.wikipedia.org/wiki/Cumulative_distribution_function
.. _`complementary error function`: https://en.wikipedia.org/wiki/Error_function
.. _`loss of significance`: https://en.wikipedia.org/wiki/Loss_of_significance
.. _`Gamma function`: https://en.wikipedia.org/wiki/Gamma_function
.. _`Pi is (still) Wrong`: https://vimeo.com/147792667
.. _`Tau day`: https://tauday.com/
.. _`IEEE-754 standard`: https://en.wikipedia.org/wiki/IEEE_754
