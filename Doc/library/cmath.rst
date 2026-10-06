:mod:`!cmath` --- Các hàm toán học cho số phức
==============================================

.. module:: cmath
   :synopsis: Các hàm toán học cho số phức.

--------------

Mô-đun này cung cấp quyền truy cập vào các hàm toán học cho số phức. Các hàm trong mô-đun này chấp nhận số nguyên, số thực dấu phẩy động hoặc số phức làm đối số. Chúng cũng chấp nhận bất kỳ đối tượng Python nào có một
:meth:`~object.__complex__` hoặc phương thức :meth:`~object.__float__`: các phương thức này được dùng để chuyển đổi đối tượng tương ứng thành số phức hoặc số thực dấu phẩy động, sau đó hàm được áp dụng cho kết quả của phép chuyển đổi.

.. note::

   Đối với các hàm liên quan đến branch cut, chúng ta phải quyết định cách định nghĩa các hàm đó ngay trên branch cut. Theo bài viết "Branch cuts for complex elementary functions" của Kahan, cũng như Phụ lục G của C99 và các tiêu chuẩn C mới hơn, chúng ta sử dụng dấu của số 0 để phân biệt một phía của branch cut với phía còn lại: đối với branch cut nằm dọc theo (một phần của) trục thực, chúng ta xét dấu của phần ảo, còn đối với branch cut nằm dọc theo trục ảo, chúng ta xét dấu của phần thực.

   Ví dụ, hàm :func:`cmath.sqrt` có branch cut dọc theo trục thực âm. Đối số ``-2-0j`` được xem như nằm *bên dưới* branch cut, và do đó cho kết quả trên trục ảo âm::

      >>> cmath.sqrt(-2-0j)
      -1.4142135623730951j

   Nhưng đối số ``-2+0j`` được xem như nằm phía trên branch cut::

      >>> cmath.sqrt(-2+0j)
      1.4142135623730951j


====================================================  ============================================
**Conversions to and from polar coordinates**
--------------------------------------------------------------------------------------------------
:func:`phase(z) <phase>`                              Return the phase of *z*
:func:`polar(z) <polar>`                              Return the representation of *z* in polar coordinates
:func:`rect(r, phi) <rect>`                           Return the complex number *z* with polar coordinates *r* and *phi*

**Power and logarithmic functions**
--------------------------------------------------------------------------------------------------
:func:`exp(z) <exp>`                                  Return *e* raised to the power *z*
:func:`log(z[, base]) <log>`                          Return the logarithm of *z* to the given *base* (*e* by default)
:func:`log10(z) <log10>`                              Return the base-10 logarithm of *z*
:func:`sqrt(z) <sqrt>`                                Return the square root of *z*

**Trigonometric functions**
--------------------------------------------------------------------------------------------------
:func:`acos(z) <acos>`                                Return the arc cosine of *z*
:func:`asin(z) <asin>`                                Return the arc sine of *z*
:func:`atan(z) <atan>`                                Return the arc tangent of *z*
:func:`cos(z) <cos>`                                  Return the cosine of *z*
:func:`sin(z) <sin>`                                  Return the sine of *z*
:func:`tan(z) <tan>`                                  Return the tangent of *z*

**Hyperbolic functions**
--------------------------------------------------------------------------------------------------
:func:`acosh(z) <acosh>`                              Return the inverse hyperbolic cosine of *z*
:func:`asinh(z) <asinh>`                              Return the inverse hyperbolic sine of *z*
:func:`atanh(z) <atanh>`                              Return the inverse hyperbolic tangent of *z*
:func:`cosh(z) <cosh>`                                Return the hyperbolic cosine of *z*
:func:`sinh(z) <sinh>`                                Return the hyperbolic sine of *z*
:func:`tanh(z) <tanh>`                                Return the hyperbolic tangent of *z*

**Classification functions**
--------------------------------------------------------------------------------------------------
:func:`isfinite(z) <isfinite>`                        Check if all components of *z* are finite
:func:`isinf(z) <isinf>`                              Check if any component of *z* is infinite
:func:`isnan(z) <isnan>`                              Check if any component of *z* is a NaN
:func:`isclose(a, b, *, rel_tol, abs_tol) <isclose>`  Check if the values *a* and *b* are close to each other

**Constants**
--------------------------------------------------------------------------------------------------
:data:`pi`                                            *π* = 3.141592...
:data:`e`                                             *e* = 2.718281...
:data:`tau`                                           *τ* = 2\ *π* = 6.283185...
:data:`inf`                                           Positive infinity
:data:`infj`                                          Pure imaginary infinity
:data:`nan`                                           "Not a number" (NaN)
:data:`nanj`                                          Pure imaginary NaN
====================================================  ============================================


Chuyển đổi sang và từ tọa độ cực
--------------------------------

Một số phức Python ``z`` được lưu trữ nội bộ bằng tọa độ *rectangular* hoặc *Cartesian*. Nó được xác định hoàn toàn bởi *real part* ``z.real`` và *imaginary part* ``z.imag``.

*Polar coordinates* cung cấp một cách khác để biểu diễn số phức. Trong tọa độ cực, số phức *z* được xác định bởi mô-đun *r* và góc pha *phi*. Mô-đun *r* là khoảng cách từ *z* đến gốc tọa độ, còn pha *phi* là góc ngược chiều kim đồng hồ, được đo bằng radian, từ trục x dương đến đoạn thẳng nối gốc tọa độ với *z*.

Có thể sử dụng các hàm sau để chuyển đổi từ tọa độ chữ nhật gốc sang tọa độ cực và ngược lại.

.. function:: phase(z)

   Trả về pha của *z* (còn được gọi là *argument* của *z*), dưới dạng số thực. ``phase(z)`` tương đương với ``math.atan2(z.imag, z.real)``. Kết quả nằm trong khoảng [-\ *π*, *π*], và branch cut của phép toán này nằm dọc theo trục thực âm. Dấu của kết quả giống với dấu của ``z.imag``, ngay cả khi ``z.imag`` bằng không::

      >>> phase(-1+0j)
      3.141592653589793
      >>> phase(-1-0j)
      -3.141592653589793


.. note::

   Mô-đun (giá trị tuyệt đối) của một số phức *z* có thể được tính bằng hàm :func:`abs` tích hợp sẵn. Không có hàm riêng trong mô-đun :mod:`!cmath` cho phép toán này.


.. function:: polar(z)

   Trả về biểu diễn của *z* trong tọa độ cực. Trả về một cặp ``(r, phi)`` trong đó *r* là mô-đun của *z* và *phi* là pha của *z*. ``polar(z)`` tương đương với ``(abs(z), phase(z))``.


.. function:: rect(r, phi)

   Trả về số phức *z* có tọa độ cực *r* và *phi*. Tương đương với ``complex(r * math.cos(phi), r * math.sin(phi))``.


Các hàm lũy thừa và logarithm
-----------------------------

.. function:: exp(z)

   Trả về *e* lũy thừa *z*, trong đó *e* là cơ số của logarithm tự nhiên.


.. function:: log(z[, base])

   Trả về logarithm của *z* theo *cơ số* đã cho. Nếu không chỉ định *cơ số*, hàm trả về logarithm tự nhiên của *z*. Có một đường cắt nhánh từ 0 dọc theo trục thực âm đến -∞.


.. function:: log10(z)

   Trả về logarithm cơ số 10 của *z*. Hàm này có cùng đường cắt nhánh với
   :func:`log`.


.. function:: sqrt(z)

   Trả về căn bậc hai của *z*. Hàm này có cùng đường cắt nhánh với :func:`log`.


Các hàm lượng giác
------------------

.. function:: acos(z)

   Trả về arc cosine của *z*. Có hai nhánh cắt: Một nhánh kéo dài sang phải từ 1 dọc theo trục thực đến ∞. Nhánh còn lại kéo dài sang trái từ -1 dọc theo trục thực đến -∞.


.. function:: asin(z)

   Trả về arc sine của *z*. Hàm này có các nhánh cắt giống như :func:`acos`.


.. function:: atan(z)

   Trả về arc tangent của *z*. Có hai nhánh cắt: Một nhánh kéo dài từ ``1j`` dọc theo trục ảo đến ``∞j``. Nhánh còn lại kéo dài từ ``-1j`` dọc theo trục ảo đến ``-∞j``.


.. function:: cos(z)

   Trả về cosine của *z*.


.. function:: sin(z)

   Trả về sine của *z*.


.. function:: tan(z)

   Trả về tangent của *z*.


Các hàm hyperbolic
------------------

.. function:: acosh(z)

   Trả về cosin hyperbolic nghịch đảo của *z*. Có một nhánh cắt, kéo dài từ 1 về phía bên trái dọc theo trục thực đến -∞.


.. function:: asinh(z)

   Trả về sin hyperbolic nghịch đảo của *z*. Có hai nhánh cắt: Một nhánh kéo dài từ ``1j`` dọc theo trục ảo đến ``∞j``. Nhánh còn lại kéo dài từ ``-1j`` dọc theo trục ảo đến ``-∞j``.


.. function:: atanh(z)

   Trả về tan hyperbolic nghịch đảo của *z*. Có hai nhánh cắt: Một nhánh kéo dài từ ``1`` dọc theo trục thực đến ``∞``. Nhánh còn lại kéo dài từ ``-1`` dọc theo trục thực đến ``-∞``.


.. function:: cosh(z)

   Trả về cosin hyperbolic của *z*.


.. function:: sinh(z)

   Trả về sin hyperbolic của *z*.


.. function:: tanh(z)

   Trả về tan hyperbolic của *z*.


Các hàm phân loại
-----------------

.. function:: isfinite(z)

   Trả về ``True`` nếu cả phần thực và phần ảo của *z* đều hữu hạn, và ``False`` nếu không.

   .. versionadded:: 3.2


.. function:: isinf(z)

   Trả về ``True`` nếu phần thực hoặc phần ảo của *z* là vô cực, và ``False`` nếu không.


.. function:: isnan(z)

   Trả về ``True`` nếu phần thực hoặc phần ảo của *z* là NaN, và ``False`` nếu không.


.. function:: isclose(a, b, *, rel_tol=1e-09, abs_tol=0.0)

   Trả về ``True`` nếu các giá trị *a* và *b* gần bằng nhau, và ``False`` nếu không.

   Việc hai giá trị có được xem là gần bằng nhau hay không được xác định theo các dung sai tuyệt đối và tương đối đã cho. Nếu không xảy ra lỗi, kết quả sẽ là: ``abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)``.

   *rel_tol* là dung sai tương đối -- đây là độ chênh lệch tối đa được phép giữa *a* và *b*, so với giá trị tuyệt đối lớn hơn của *a* hoặc *b*. Ví dụ, để đặt dung sai 5%, hãy truyền ``rel_tol=0.05``. Dung sai mặc định là ``1e-09``, đảm bảo rằng hai giá trị giống nhau trong khoảng 9 chữ số thập phân. *rel_tol* phải không âm và nhỏ hơn ``1.0``.

   *abs_tol* là dung sai tuyệt đối; giá trị mặc định là ``0.0`` và nó phải không âm. Khi so sánh ``x`` với ``0.0``, ``isclose(x, 0)`` được tính là ``abs(x) <= rel_tol  * abs(x)``, giá trị này bằng ``False`` với mọi ``x`` và rel_tol nhỏ hơn ``1.0``. Vì vậy, hãy thêm đối số abs_tol dương thích hợp vào lời gọi.

   Các giá trị đặc biệt của IEEE 754 là ``NaN``, ``inf`` và ``-inf`` sẽ được xử lý theo các quy tắc của IEEE. Cụ thể, ``NaN`` không được xem là gần với bất kỳ giá trị nào khác, kể cả ``NaN``. ``inf`` và ``-inf`` chỉ được xem là gần với chính chúng.

   .. versionadded:: 3.5

   .. seealso::

      :pep:`485` -- Một hàm dùng để kiểm tra tính bằng nhau xấp xỉ


Hằng số
-------

.. data:: pi

   Hằng số toán học *π*, dưới dạng số thực dấu phẩy động.


.. data:: e

   Hằng số toán học *e*, dưới dạng số thực dấu phẩy động.


.. data:: tau

   Hằng số toán học *τ*, dưới dạng số thực dấu phẩy động.

   .. versionadded:: 3.6


.. data:: inf

   Vô cực dương dấu phẩy động. Tương đương với ``float('inf')``.

   .. versionadded:: 3.6


.. data:: infj

   Số phức có phần thực bằng không và phần ảo là dương vô cực. Tương đương với ``complex(0.0, float('inf'))``.

   .. versionadded:: 3.6


.. data:: nan

   Giá trị dấu phẩy động "không phải là một số" (NaN). Tương đương với ``float('nan')``. Xem thêm :data:`math.nan`.

   .. versionadded:: 3.6


.. data:: nanj

   Số phức có phần thực bằng không và phần ảo là NaN. Tương đương với ``complex(0.0, float('nan'))``.

   .. versionadded:: 3.6


.. index:: pair: module; math

Lưu ý rằng tập hợp các hàm tương tự, nhưng không hoàn toàn giống, tập hợp trong module :mod:`math`. Lý do có hai module là vì một số người dùng không quan tâm đến số phức, và có thể thậm chí không biết chúng là gì. Họ muốn ``math.sqrt(-1)`` phát sinh một ngoại lệ thay vì trả về một số phức. Cũng lưu ý rằng các hàm được định nghĩa trong :mod:`!cmath` luôn trả về một số phức, ngay cả khi kết quả có thể được biểu diễn dưới dạng số thực (trong trường hợp đó, số phức có phần ảo bằng không).

Lưu ý về các nhánh cắt: Đó là những đường cong mà trên đó hàm đã cho không liên tục. Chúng là một đặc điểm cần thiết của nhiều hàm phức. Giả định rằng nếu cần tính toán với các hàm phức, bạn sẽ hiểu về các nhánh cắt. Hãy tham khảo hầu như bất kỳ cuốn sách nào về biến phức (không quá nhập môn) để hiểu rõ hơn. Để biết thông tin về lựa chọn nhánh cắt phù hợp cho mục đích tính toán số, tài liệu tham khảo tốt là bài viết sau:


.. seealso::

   Kahan, W: Các nhánh cắt cho các hàm sơ cấp phức; hay, Chuyện bé xé ra to về bit dấu của số không. Trong Iserles, A. và Powell, M. (biên tập), Tình hình hiện tại trong phân tích số. Clarendon Press (1987), trang 165--211.
