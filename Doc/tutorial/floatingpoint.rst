.. testsetup::

    import math
    from fractions import Fraction

.. _tut-fp-issues:

******************************************************
Phép tính số thực dấu phẩy động: Các vấn đề và hạn chế
******************************************************

.. sectionauthor:: Tim Peters <tim_one@users.sourceforge.net>
.. sectionauthor:: Raymond Hettinger <python at rcn dot com>


Trong phần cứng máy tính, các số dấu phẩy động được biểu diễn dưới dạng phân số cơ số 2 (nhị phân). Ví dụ, phân số **decimal** ``0.625`` có giá trị 6/10 + 2/100 + 5/1000, và tương tự, phân số **binary** ``0.101`` có giá trị 1/2 + 0/4 + 1/8. Hai phân số này có giá trị giống hệt nhau; điểm khác biệt thực sự duy nhất là phân số đầu tiên được viết theo ký hiệu phân số cơ số 10, còn phân số thứ hai được viết theo cơ số 2.

Đáng tiếc là hầu hết các phân số thập phân không thể được biểu diễn chính xác dưới dạng phân số nhị phân. Hệ quả là nhìn chung, các số dấu phẩy động thập phân bạn nhập vào chỉ được các số dấu phẩy động nhị phân thực sự lưu trong máy tính xấp xỉ.

Ban đầu, vấn đề này dễ hiểu hơn trong cơ số 10. Hãy xét phân số 1/3. Bạn có thể xấp xỉ phân số đó dưới dạng một phân số cơ số 10::

   0.3

hoặc chính xác hơn,::

   0.33

hoặc chính xác hơn,::

   0.333

và cứ tiếp tục như vậy. Dù bạn sẵn sàng viết bao nhiêu chữ số đi nữa, kết quả sẽ không bao giờ chính xác bằng 1/3, mà chỉ là một phép xấp xỉ 1/3 ngày càng tốt hơn.

Tương tự, cho dù bạn sẵn sàng sử dụng bao nhiêu chữ số cơ số 2 đi nữa, giá trị thập phân 0.1 cũng không thể được biểu diễn chính xác dưới dạng phân số cơ số 2. Trong cơ số 2, 1/10 là phân số lặp vô hạn::

   0.0001100110011001100110011001100110011001100110011...

Dừng lại ở bất kỳ số bit hữu hạn nào, bạn sẽ nhận được một giá trị xấp xỉ. Trên hầu hết các máy hiện nay, số thực dấu phẩy động được xấp xỉ bằng một phân số nhị phân, trong đó tử số sử dụng 53 bit đầu tiên bắt đầu từ bit có trọng số lớn nhất và mẫu số là một lũy thừa của hai. Với 1/10, phân số nhị phân là ``3602879701896397 / 2 ** 55``, gần nhưng không hoàn toàn bằng giá trị thực của 1/10.

Nhiều người dùng không nhận ra sự xấp xỉ này do cách các giá trị được hiển thị. Python chỉ in ra một giá trị thập phân xấp xỉ giá trị thập phân thực của giá trị xấp xỉ nhị phân được máy lưu trữ. Trên hầu hết các máy, nếu Python in ra giá trị thập phân thực của giá trị xấp xỉ nhị phân được lưu trữ cho 0.1, nó sẽ phải hiển thị::

   >>> 0.1
   0.1000000000000000055511151231257827021181583404541015625

Đó là nhiều chữ số hơn mức mà hầu hết mọi người thấy hữu ích, vì vậy Python giữ cho số chữ số ở mức vừa phải bằng cách hiển thị một giá trị đã được làm tròn:

.. doctest::

   >>> 1 / 10
   0.1

Chỉ cần nhớ rằng, mặc dù kết quả được in ra trông giống như giá trị chính xác của 1/10, giá trị thực sự được lưu trữ là phân số nhị phân có thể biểu diễn gần nhất.

Điều thú vị là có nhiều số thập phân khác nhau cùng có một phân số nhị phân xấp xỉ gần nhất. Ví dụ, các số ``0.1``, ``0.10000000000000001`` và ``0.1000000000000000055511151231257827021181583404541015625`` đều được xấp xỉ bằng ``3602879701896397 / 2 ** 55``. Vì tất cả các giá trị thập phân này đều có cùng một giá trị xấp xỉ, bất kỳ giá trị nào trong số chúng cũng có thể được hiển thị mà vẫn bảo toàn bất biến ``eval(repr(x)) == x``.

Trước đây, dấu nhắc Python và hàm tích hợp sẵn :func:`repr` sẽ chọn giá trị có 17 chữ số có nghĩa, ``0.10000000000000001``. Bắt đầu từ Python 3.1, Python (trên hầu hết các hệ thống) đã có thể chọn giá trị ngắn nhất trong số này và chỉ hiển thị ``0.1``.

Lưu ý rằng đây là bản chất của số dấu phẩy động nhị phân: đây không phải là lỗi trong Python và cũng không phải là lỗi trong mã của bạn. Bạn sẽ thấy hiện tượng tương tự trong mọi ngôn ngữ hỗ trợ phép tính dấu phẩy động của phần cứng mà bạn sử dụng (mặc dù một số ngôn ngữ có thể không *display* sự khác biệt theo mặc định hoặc trong mọi chế độ đầu ra).

Để có kết quả đầu ra dễ đọc hơn, bạn có thể muốn sử dụng định dạng chuỗi để tạo ra một số lượng chữ số có nghĩa giới hạn:

.. doctest::

   >>> format(math.pi, '.12g')  # give 12 significant digits
   '3.14159265359'

   >>> format(math.pi, '.2f')   # give 2 digits after the point
   '3.14'

   >>> repr(math.pi)
   '3.141592653589793'

Điều quan trọng cần hiểu là, theo một nghĩa thực tế, đây chỉ là một ảo giác: bạn chỉ đang làm tròn *display* của giá trị máy thực sự.

Một ảo giác có thể dẫn đến một ảo giác khác. Ví dụ, vì 0.1 không chính xác bằng 1/10, nên việc cộng ba giá trị 0.1 có thể cũng không cho kết quả chính xác bằng 0.3:

.. doctest::

   >>> 0.1 + 0.1 + 0.1 == 0.3
   False

Ngoài ra, vì 0.1 không thể tiến gần hơn đến giá trị chính xác của 1/10 và 0.3 không thể tiến gần hơn đến giá trị chính xác của 3/10, nên việc làm tròn trước bằng
:func:`round` hàm này không thể giúp:

.. doctest::

   >>> round(0.1, 1) + round(0.1, 1) + round(0.1, 1) == round(0.3, 1)
   False

:func:`math.isclose` có thể hữu ích khi so sánh các giá trị không chính xác:

.. doctest::

   >>> math.isclose(0.1 + 0.1 + 0.1, 0.3)
   True

Ngoài ra, có thể sử dụng hàm :func:`round` để so sánh các giá trị xấp xỉ gần đúng:

.. doctest::

   >>> round(math.pi, ndigits=2) == round(22 / 7, ndigits=2)
   True

Số học dấu phẩy động nhị phân ẩn chứa nhiều điều bất ngờ như vậy. Vấn đề với "0.1" được giải thích chi tiết và chính xác bên dưới, trong phần "Lỗi biểu diễn". Xem `Các ví dụ về vấn đề với số dấu phẩy động <https://jvns.ca/blog/2023/01/13/examples-of-floating-point-problems/>`_ để có phần tóm tắt dễ hiểu về cách số dấu phẩy động nhị phân hoạt động và những vấn đề thường gặp trong thực tế. Ngoài ra, hãy xem `Những cạm bẫy của số dấu phẩy động <http://www.indowsway.com/floatingpoint.htm>`_ để có phần trình bày đầy đủ hơn về những điều bất ngờ phổ biến khác.

Như phần đó nêu ở gần cuối, "không có câu trả lời dễ dàng nào". Tuy vậy, đừng quá e ngại số dấu phẩy động! Các lỗi trong phép toán float của Python bắt nguồn từ phần cứng dấu phẩy động và trên hầu hết các máy tính có độ lớn không vượt quá 1 phần trong 2\*\*53 cho mỗi phép toán. Mức này là quá đủ cho hầu hết tác vụ, nhưng bạn cần nhớ rằng đây không phải là số học thập phân và mọi phép toán float đều có thể phát sinh một lỗi làm tròn mới.

Mặc dù vẫn tồn tại các trường hợp bất thường, với hầu hết nhu cầu sử dụng số học dấu phẩy động thông thường, cuối cùng bạn sẽ nhận được kết quả như mong đợi nếu chỉ cần làm tròn phần hiển thị của các kết quả cuối cùng đến số chữ số thập phân mà bạn mong muốn.
:func:`str` thường là đủ; để kiểm soát chi tiết hơn, hãy xem các chỉ định định dạng của phương thức :meth:`str.format` trong :ref:`formatstrings`.

Đối với các trường hợp sử dụng yêu cầu biểu diễn thập phân chính xác, hãy thử sử dụng
module :mod:`decimal`, module này triển khai số học thập phân phù hợp cho các ứng dụng kế toán và ứng dụng độ chính xác cao.

Một dạng số học chính xác khác được mô-đun :mod:`fractions` hỗ trợ; mô-đun này triển khai phép tính dựa trên các số hữu tỉ (vì vậy những số như 1/3 có thể được biểu diễn chính xác).

Nếu bạn thường xuyên sử dụng các phép toán dấu phẩy động, bạn nên xem qua gói NumPy và nhiều gói khác dành cho các phép toán toán học và thống kê do dự án SciPy cung cấp. Xem <https://scipy.org>.

Python cung cấp các công cụ có thể hữu ích trong những trường hợp hiếm hoi khi bạn thực sự *muốn* biết giá trị chính xác của một số float.  Phương thức
:meth:`float.as_integer_ratio` biểu diễn giá trị của một số float dưới dạng phân số:

.. doctest::

   >>> x = 3.14159
   >>> x.as_integer_ratio()
   (3537115888337719, 1125899906842624)

Vì tỉ số này là chính xác, nó có thể được dùng để tái tạo giá trị ban đầu mà không mất mát:

.. doctest::

    >>> x == 3537115888337719 / 1125899906842624
    True

Phương thức :meth:`float.hex` biểu diễn một số float dưới dạng hệ thập lục phân (cơ số 16), một lần nữa cho biết giá trị chính xác được máy tính của bạn lưu trữ:

.. doctest::

   >>> x.hex()
   '0x1.921f9f01b866ep+1'

Biểu diễn thập lục phân chính xác này có thể được dùng để tái tạo chính xác giá trị float:

.. doctest::

    >>> x == float.fromhex('0x1.921f9f01b866ep+1')
    True

Vì cách biểu diễn là chính xác, nó hữu ích để chuyển các giá trị một cách đáng tin cậy giữa những phiên bản Python khác nhau (độc lập với nền tảng) và trao đổi dữ liệu với các ngôn ngữ khác hỗ trợ cùng định dạng (chẳng hạn như Java và C99).

Một công cụ hữu ích khác là hàm :func:`sum`, giúp giảm thiểu mất độ chính xác trong quá trình tính tổng. Hàm này sử dụng độ chính xác mở rộng cho các bước làm tròn trung gian khi các giá trị được cộng dồn vào một tổng đang tính. Điều đó có thể tạo ra khác biệt về độ chính xác tổng thể, nhờ vậy các sai số không tích lũy đến mức ảnh hưởng đến tổng cuối cùng:

.. doctest::

   >>> 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 == 1.0
   False
   >>> sum([0.1] * 10) == 1.0
   True

:func:`math.fsum` còn tiến xa hơn khi theo dõi tất cả "chữ số bị mất" trong lúc các giá trị được cộng dồn vào một tổng đang tính, nhờ đó kết quả chỉ phải làm tròn một lần. Cách này chậm hơn :func:`sum` nhưng sẽ chính xác hơn trong những trường hợp hiếm gặp khi các đầu vào có độ lớn lớn chủ yếu triệt tiêu lẫn nhau, để lại một tổng cuối gần bằng không:

.. doctest::

   >>> arr = [-0.10430216751806065, -266310978.67179024, 143401161448607.16,
   ...        -143401161400469.7, 266262841.31058735, -0.003244936839808227]
   >>> float(sum(map(Fraction, arr)))   # Exact summation with single rounding
   8.042173697819788e-13
   >>> math.fsum(arr)                   # Single rounding
   8.042173697819788e-13
   >>> sum(arr)                         # Multiple roundings in extended precision
   8.042178034628478e-13
   >>> total = 0.0
   >>> for x in arr:
   ...     total += x                   # Multiple roundings in standard precision
   ...
   >>> total                            # Straight addition has no correct digits!
   -0.0051575902860057365


.. _tut-fp-error:

Lỗi biểu diễn
=============

Phần này giải thích chi tiết ví dụ "0.1" và chỉ ra cách bạn có thể tự thực hiện phân tích chính xác những trường hợp như vậy. Giả định rằng bạn đã quen thuộc ở mức cơ bản với cách biểu diễn số dấu phẩy động nhị phân.

:dfn:`Lỗi biểu diễn` đề cập đến thực tế là một số (thực ra là hầu hết) phân số thập phân không thể được biểu diễn chính xác dưới dạng phân số nhị phân (cơ số 2). Đây là lý do chính khiến Python (hoặc Perl, C, C++, Java, Fortran và nhiều ngôn ngữ khác) thường không hiển thị số thập phân chính xác mà bạn mong đợi.

Tại sao lại như vậy? 1/10 không thể được biểu diễn chính xác dưới dạng phân số nhị phân. Kể từ ít nhất năm 2000, hầu như tất cả máy tính đều sử dụng phép toán số dấu phẩy động nhị phân theo IEEE 754, và hầu như tất cả nền tảng đều ánh xạ các số float của Python thành các giá trị binary64 "độ chính xác kép" theo IEEE 754. Các giá trị binary64 theo IEEE 754 có độ chính xác 53 bit, vì vậy khi nhập vào, máy tính cố gắng chuyển 0.1 thành phân số gần nhất mà nó có thể tạo ra theo dạng *J*/2**\ *N*, trong đó *J* là một số nguyên chứa chính xác 53 bit.
Viết lại
::::::::

   1 / 10 ~= J / (2**N)

do đó::

   J ~= 2**N / 10

và nhớ rằng *J* có chính xác 53 bit (là ``>= 2**52`` nhưng ``< 2**53``), giá trị tốt nhất cho *N* là 56:

.. doctest::

    >>> 2**52 <=  2**56 // 10  < 2**53
    True

Điều đó có nghĩa là 56 là giá trị duy nhất của *N* khiến *J* còn lại đúng 53 bit.  Khi đó, giá trị tốt nhất có thể của *J* là thương sau khi làm tròn:

.. doctest::

   >>> q, r = divmod(2**56, 10)
   >>> r
   6

Vì phần dư lớn hơn một nửa của 10, phép xấp xỉ tốt nhất thu được bằng cách làm tròn lên:

.. doctest::



   >>> q+1
   7205759403792794

Do đó, phép xấp xỉ tốt nhất có thể cho 1/10 ở độ chính xác kép IEEE 754 là::

   7205759403792794 / 2 ** 56

Chia cả tử số và mẫu số cho hai sẽ rút gọn phân số thành::

   3602879701896397 / 2 ** 55

Lưu ý rằng vì chúng ta đã làm tròn lên nên giá trị này thực tế lớn hơn 1/10 một chút; nếu không làm tròn lên, thương sẽ nhỏ hơn 1/10 một chút. Nhưng trong mọi trường hợp, nó không thể *chính xác* là 1/10!

Vì vậy, máy tính không bao giờ "thấy" 1/10: thứ nó thấy là phân số chính xác được cho ở trên, là xấp xỉ double IEEE 754 tốt nhất mà nó có thể nhận được:

.. doctest::

   >>> 0.1 * 2 ** 55
   3602879701896397.0

Nếu nhân phân số đó với 10\*\*55, chúng ta có thể thấy giá trị này với tối đa 55 chữ số thập phân:

.. doctest::

   >>> 3602879701896397 * 10 ** 55 // 2 ** 55
   1000000000000000055511151231257827021181583404541015625

nghĩa là số chính xác được lưu trong máy tính bằng giá trị thập phân 0.1000000000000000055511151231257827021181583404541015625. Thay vì hiển thị toàn bộ giá trị thập phân, nhiều ngôn ngữ (bao gồm các phiên bản Python cũ hơn) làm tròn kết quả còn 17 chữ số có nghĩa:

.. doctest::

   >>> format(0.1, '.17f')
   '0.10000000000000001'

Các mô-đun :mod:`fractions` và :mod:`decimal` giúp thực hiện những phép tính này dễ dàng:

.. doctest::

   >>> from decimal import Decimal
   >>> from fractions import Fraction

   >>> Fraction.from_float(0.1)
   Fraction(3602879701896397, 36028797018963968)

   >>> (0.1).as_integer_ratio()
   (3602879701896397, 36028797018963968)

   >>> Decimal.from_float(0.1)
   Decimal('0.1000000000000000055511151231257827021181583404541015625')

   >>> format(Decimal.from_float(0.1), '.17')
   '0.10000000000000001'

.. _`Examples of Floating Point Problems`: https://jvns.ca/blog/2023/01/13/examples-of-floating-point-problems/
.. _`The Perils of Floating Point`: http://www.indowsway.com/floatingpoint.htm
