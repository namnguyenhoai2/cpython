:mod:`!statistics` --- Các hàm thống kê toán học
================================================

.. module:: statistics
   :synopsis: Các hàm thống kê toán học

.. moduleauthor:: Steven D'Aprano <steve+python@pearwood.info>
.. sectionauthor:: Steven D'Aprano <steve+python@pearwood.info>

.. versionadded:: 3.4

**Mã nguồn:** :source:`Lib/statistics.py`

.. testsetup:: *

   from statistics import *
   import math
   __name__ = '<doctest>'

--------------

Mô-đun này cung cấp các hàm để tính toán thống kê toán học của dữ liệu số (có giá trị :class:`~numbers.Real`).

Mô-đun này không nhằm cạnh tranh với các thư viện bên thứ ba như `NumPy <https://numpy.org>`_, `SciPy <https://scipy.org/>`_, hoặc các gói thống kê độc quyền đầy đủ tính năng dành cho các nhà thống kê chuyên nghiệp như Minitab, SAS và Matlab. Mô-đun này hướng đến mức độ của các máy tính vẽ đồ thị và máy tính khoa học.

Trừ khi được nêu rõ, các hàm này hỗ trợ :class:`int`,
:class:`float`, :class:`~decimal.Decimal` và :class:`~fractions.Fraction`. Hành vi với các kiểu khác (dù có thuộc numeric tower hay không) hiện chưa được hỗ trợ. Các collection chứa kết hợp nhiều kiểu cũng không được xác định và phụ thuộc vào cách triển khai. Nếu dữ liệu đầu vào của bạn gồm nhiều kiểu, bạn có thể sử dụng :func:`map` để đảm bảo kết quả nhất quán, ví dụ: ``map(float, input_data)``.

Một số bộ dữ liệu sử dụng các giá trị ``NaN`` (không phải số) để biểu diễn dữ liệu bị thiếu. Vì NaN có ngữ nghĩa so sánh bất thường, chúng gây ra hành vi đáng ngạc nhiên hoặc không xác định trong các hàm thống kê sắp xếp dữ liệu hoặc đếm số lần xuất hiện. Các hàm bị ảnh hưởng là ``median()``, ``median_low()``, ``median_high()``, ``median_grouped()``, ``mode()``, ``multimode()`` và ``quantiles()``. Cần loại bỏ các giá trị ``NaN`` trước khi gọi những hàm này::

    >>> from statistics import median
    >>> from math import isnan
    >>> from itertools import filterfalse

    >>> data = [20.7, float('NaN'),19.2, 18.3, float('NaN'), 14.4]
    >>> sorted(data)  # Điều này có hành vi đáng ngạc nhiên
    [20.7, nan, 14.4, 18.3, 19.2, nan]
    >>> median(data)  # Kết quả này không như mong đợi
    16.35

    >>> sum(map(isnan, data))    # Số lượng giá trị bị thiếu
    2
    >>> clean = list(filterfalse(isnan, data))  # Loại bỏ các giá trị NaN
    >>> clean
    [20.7, 19.2, 18.3, 14.4]
    >>> sorted(clean)  # Việc sắp xếp giờ đã hoạt động như mong đợi
    [14.4, 18.3, 19.2, 20.7]
    >>> median(clean)       # Kết quả này giờ đã được xác định rõ ràng
    18.75


Các giá trị trung bình và thước đo vị trí trung tâm
---------------------------------------------------

Các hàm này tính giá trị trung bình hoặc giá trị điển hình từ một tổng thể hoặc mẫu.

+------------------------+------------------------------------------------------------------------------------------------------+
| :func:`mean`           | Trung bình số học ("trung bình") của dữ liệu.                                                        |
+------------------------+------------------------------------------------------------------------------------------------------+
| :func:`fmean`          | Trung bình số học dấu phẩy động nhanh, có hỗ trợ trọng số tùy chọn.                                  |
+------------------------+------------------------------------------------------------------------------------------------------+
| :func:`geometric_mean` | Trung bình hình học của dữ liệu.                                                                     |
+------------------------+------------------------------------------------------------------------------------------------------+
| :func:`harmonic_mean`  | Trung bình điều hòa của dữ liệu.                                                                     |
+------------------------+------------------------------------------------------------------------------------------------------+
| :func:`kde`            | Ước tính phân phối mật độ xác suất của dữ liệu.                                                      |
+------------------------+------------------------------------------------------------------------------------------------------+
| :func:`kde_random`     | Lấy mẫu ngẫu nhiên từ PDF được tạo bởi kde().                                                        |
+------------------------+------------------------------------------------------------------------------------------------------+
| :func:`median`         | Trung vị (giá trị ở giữa) của dữ liệu.                                                               |
+------------------------+------------------------------------------------------------------------------------------------------+
| :func:`median_low`     | Trung vị thấp của dữ liệu.                                                                           |
+------------------------+------------------------------------------------------------------------------------------------------+
| :func:`median_high`    | Trung vị cao của dữ liệu.                                                                            |
+------------------------+------------------------------------------------------------------------------------------------------+
| :func:`median_grouped` | Trung vị (phân vị thứ 50) của dữ liệu được nhóm.                                                     |
+------------------------+------------------------------------------------------------------------------------------------------+
| :func:`mode`           | Mode đơn (giá trị xuất hiện phổ biến nhất) của dữ liệu rời rạc hoặc dữ liệu định danh.               |
+------------------------+------------------------------------------------------------------------------------------------------+
| :func:`multimode`      | Danh sách các mode (các giá trị xuất hiện phổ biến nhất) của dữ liệu rời rạc hoặc dữ liệu định danh. |
+------------------------+------------------------------------------------------------------------------------------------------+
| :func:`quantiles`      | Chia dữ liệu thành các khoảng có xác suất bằng nhau.                                                 |
+------------------------+------------------------------------------------------------------------------------------------------+

Các thước đo độ phân tán
------------------------

Các hàm này tính toán một thước đo cho biết tổng thể hoặc mẫu có xu hướng lệch khỏi các giá trị điển hình hoặc trung bình ở mức nào.

+-------------------+---------------------------------------------+
| :func:`pstdev`    | Độ lệch chuẩn của tổng thể đối với dữ liệu. |
+-------------------+---------------------------------------------+
| :func:`pvariance` | Phương sai của tổng thể đối với dữ liệu.    |
+-------------------+---------------------------------------------+
| :func:`stdev`     | Độ lệch chuẩn của mẫu đối với dữ liệu.      |
+-------------------+---------------------------------------------+
| :func:`variance`  | Phương sai của mẫu đối với dữ liệu.         |
+-------------------+---------------------------------------------+

Thống kê cho mối quan hệ giữa hai đầu vào
-----------------------------------------

Các hàm này tính toán các thống kê liên quan đến mối quan hệ giữa hai đầu vào.

+---------------------------+----------------------------------------------------------+
| :func:`covariance`        | Hiệp phương sai mẫu cho hai biến.                        |
+---------------------------+----------------------------------------------------------+
| :func:`correlation`       | Các hệ số tương quan Pearson và Spearman.                |
+---------------------------+----------------------------------------------------------+
| :func:`linear_regression` | Hệ số góc và hệ số chặn cho hồi quy tuyến tính đơn giản. |
+---------------------------+----------------------------------------------------------+


Chi tiết về hàm
---------------

Lưu ý: Các hàm không yêu cầu dữ liệu được cung cấp cho chúng phải được sắp xếp. Tuy nhiên, để thuận tiện khi đọc, hầu hết các ví dụ đều minh họa các dãy đã được sắp xếp.

.. function:: mean(data)

   Trả về giá trị trung bình số học của *data*, có thể là một sequence hoặc iterable.

   Trung bình số học là tổng của dữ liệu chia cho số lượng điểm dữ liệu. Nó thường được gọi là "giá trị trung bình", mặc dù đây chỉ là một trong nhiều loại trung bình toán học khác nhau. Đây là một thước đo vị trí trung tâm của dữ liệu.

   Nếu *data* trống, :exc:`StatisticsError` sẽ được phát sinh.

   Một số ví dụ sử dụng:

   .. doctest::

      >>> mean([1, 2, 3, 4, 4])
      2.8
      >>> mean([-1.0, 2.5, 3.25, 5.75])
      2.625

      >>> from fractions import Fraction as F
      >>> mean([F(3, 7), F(1, 21), F(5, 3), F(1, 3)])
      Fraction(13, 21)

      >>> from decimal import Decimal as D
      >>> mean([D("0.5"), D("0.75"), D("0.625"), D("0.375")])
      Decimal('0.5625')

   .. note::

      Trung bình chịu ảnh hưởng mạnh bởi `outliers <https://en.wikipedia.org/wiki/Outlier>`_ và không nhất thiết là một ví dụ điển hình của các điểm dữ liệu. Để có một thước đo `central tendency <https://en.wikipedia.org/wiki/Central_tendency>`_ mạnh hơn, dù kém hiệu quả hơn, hãy xem :func:`median`.

      Trung bình mẫu đưa ra một ước lượng không chệch cho trung bình tổng thể thực, vì vậy khi lấy trung bình trên tất cả các mẫu có thể có, ``mean(sample)`` hội tụ về trung bình thực của toàn bộ tổng thể. Nếu *data* đại diện cho toàn bộ tổng thể thay vì một mẫu, thì ``mean(data)`` tương đương với việc tính trung bình tổng thể thực μ.


.. function:: fmean(data, weights=None)

   Chuyển *data* thành các số thực và tính trung bình số học.

   Hàm này chạy nhanh hơn hàm :func:`mean` và luôn trả về một
   :class:`float`.  *data* có thể là một sequence hoặc iterable.  Nếu dataset đầu vào trống, một :exc:`StatisticsError` sẽ được phát sinh.

   .. doctest::

      >>> fmean([3.5, 4.0, 5.25])
      4.25

   Có hỗ trợ weighting tùy chọn.  Ví dụ, một giáo sư chấm điểm cho một khóa học bằng cách tính trọng số cho các bài kiểm tra ngắn là 20%, bài tập về nhà là 20%, bài thi giữa kỳ là 30% và bài thi cuối kỳ là 30%:

   .. doctest::

      >>> grades = [85, 92, 83, 91]
      >>> weights = [0.20, 0.20, 0.30, 0.30]
      >>> fmean(grades, weights)
      87.6

   Nếu cung cấp *weights*, nó phải có cùng độ dài với *data*, nếu không sẽ phát sinh một :exc:`ValueError`.

   .. versionadded:: 3.8

   .. versionchanged:: 3.11
      Đã bổ sung hỗ trợ cho *weights*.


.. function:: geometric_mean(data)

   Chuyển *data* thành các số thực và tính geometric mean.

   Geometric mean biểu thị xu hướng trung tâm hoặc giá trị điển hình của *data* bằng cách sử dụng tích của các giá trị (trái với arithmetic mean, sử dụng tổng của chúng).

   Phát sinh một :exc:`StatisticsError` nếu tập dữ liệu đầu vào trống, nếu chứa số 0 hoặc nếu chứa giá trị âm. *data* có thể là một sequence hoặc iterable.

   Không có nỗ lực đặc biệt nào được thực hiện để đạt kết quả chính xác tuyệt đối. (Tuy nhiên, điều này có thể thay đổi trong tương lai.)

   .. doctest::

      >>> round(geometric_mean([54, 24, 36]), 1)
      36.0

   .. versionadded:: 3.8


.. function:: harmonic_mean(data, weights=None)

   Trả về trung bình điều hòa của *data*, một sequence hoặc iterable gồm các số có giá trị thực. Nếu *weights* bị bỏ qua hoặc ``None``, thì giả định rằng các giá trị có trọng số bằng nhau.

   Trung bình điều hòa là nghịch đảo của :func:`mean` trung bình cộng của các nghịch đảo của dữ liệu. Ví dụ, trung bình điều hòa của ba giá trị *a*, *b* và *c* sẽ tương đương với ``3/(1/a + 1/b + 1/c)``. Nếu một trong các giá trị bằng 0, kết quả sẽ bằng 0.

   Trung bình điều hòa là một loại giá trị trung bình, một thước đo vị trí trung tâm của dữ liệu. Phương pháp này thường phù hợp khi tính trung bình các tỷ số hoặc tốc độ, chẳng hạn như tốc độ di chuyển.

   Giả sử một chiếc xe đi được 10 km với tốc độ 40 km/hr, sau đó đi thêm 10 km với tốc độ 60 km/hr. Tốc độ trung bình là bao nhiêu?

   .. doctest::

      >>> harmonic_mean([40, 60])
      48.0

   Giả sử một chiếc xe di chuyển với tốc độ 40 km/hr trong quãng đường 5 km, rồi khi giao thông thông thoáng, tăng tốc lên 60 km/hr trong 30 km còn lại của hành trình. Tốc độ trung bình là bao nhiêu?

   .. doctest::

      >>> harmonic_mean([40, 60], weights=[5, 30])
      56.0

   :exc:`StatisticsError` được phát sinh nếu *data* rỗng, bất kỳ phần tử nào nhỏ hơn 0 hoặc tổng có trọng số không dương.

   Thuật toán hiện tại sẽ kết thúc sớm khi gặp giá trị 0 trong đầu vào. Điều này có nghĩa là các đầu vào tiếp theo không được kiểm tra tính hợp lệ. (Hành vi này có thể thay đổi trong tương lai.)

   .. versionadded:: 3.6

   .. versionchanged:: 3.10
      Đã bổ sung hỗ trợ cho *weights*.


.. function:: kde(data, h, kernel='normal', *, cumulative=False)

   `Ước lượng mật độ kernel (Kernel Density Estimation, KDE) <https://www.itm-conferences.org/articles/itmconf/pdf/2018/08/itmconf_sam2018_00037.pdf>`_: Tạo hàm mật độ xác suất liên tục hoặc hàm phân phối tích lũy từ các mẫu rời rạc.

   Ý tưởng cơ bản là làm trơn dữ liệu bằng cách sử dụng `một hàm kernel <https://en.wikipedia.org/wiki/Kernel_(statistics)>`_. để giúp suy luận về một tổng thể từ một mẫu.

   Mức độ làm trơn được kiểm soát bởi tham số tỷ lệ *h*, được gọi là bandwidth. Các giá trị nhỏ hơn nhấn mạnh những đặc trưng cục bộ, trong khi các giá trị lớn hơn cho kết quả trơn hơn.

   *kernel* xác định trọng số tương đối của các điểm dữ liệu mẫu. Nhìn chung, việc chọn hình dạng kernel không quan trọng bằng tham số làm trơn bandwidth có ảnh hưởng lớn hơn.

   Các kernel gán trọng số cho mọi điểm mẫu bao gồm *normal* (*gauss*), *logistic* và *sigmoid*.

   Các kernel chỉ gán trọng số cho những điểm mẫu nằm trong bandwidth bao gồm *rectangular* (*uniform*), *triangular*, *parabolic* (*epanechnikov*), *quartic* (*biweight*), *triweight* và *cosine*.

   Nếu *cumulative* là true, hàm sẽ trả về một hàm phân phối tích lũy.

   Một :exc:`StatisticsError` sẽ được raised nếu sequence *data* rỗng.

   `Wikipedia có một ví dụ <https://en.wikipedia.org/wiki/Kernel_density_estimation#Example>`_ trong đó chúng ta có thể sử dụng :func:`kde` để tạo và vẽ biểu đồ hàm mật độ xác suất được ước tính từ một mẫu nhỏ:

   .. doctest::

      >>> sample = [-2.1, -1.3, -0.4, 1.9, 5.1, 6.2]
      >>> f_hat = kde(sample, h=1.5)
      >>> xarr = [i/100 for i in range(-750, 1100)]
      >>> yarr = [f_hat(x) for x in xarr]

   Các điểm trong ``xarr`` và ``yarr`` có thể được dùng để tạo biểu đồ PDF:

   .. image:: kde_example.png
      :alt: Biểu đồ phân tán của hàm mật độ xác suất được ước tính.

   Vì hàm ``f_hat`` được trả về thường được gọi nhiều lần, nó lưu vào bộ nhớ đệm *data* để cải thiện hiệu suất. Để hỗ trợ các tập dữ liệu động, bộ nhớ đệm này sẽ tự động làm mới bất cứ khi nào độ dài của *data* thay đổi. Điều này cho phép thêm các mẫu mới khi chúng khả dụng.

   .. versionadded:: 3.13


.. function:: kde_random(data, h, kernel='normal', *, seed=None)

   Trả về một hàm thực hiện lựa chọn ngẫu nhiên từ hàm mật độ xác suất ước tính do ``kde(data, h, kernel)`` tạo ra.

   Việc cung cấp *seed* cho phép thực hiện các lựa chọn có thể tái lập. Trong tương lai, các giá trị có thể thay đổi đôi chút khi các ước tính kernel inverse CDF chính xác hơn được triển khai.  Seed có thể là một số nguyên, số thực, chuỗi hoặc bytes.

   Một :exc:`StatisticsError` sẽ được raised nếu sequence *data* rỗng.

   Tiếp tục ví dụ về :func:`kde`, chúng ta có thể sử dụng
   :func:`kde_random` để tạo các lựa chọn ngẫu nhiên mới từ một hàm mật độ xác suất ước tính:

      >>> data = [-2.1, -1.3, -0.4, 1.9, 5.1, 6.2]
      >>> rand = kde_random(data, h=1.5, seed=8675309)
      >>> new_selections = [rand() for i in range(10)]
      >>> [round(x, 1) for x in new_selections]
      [0.7, 6.2, 1.2, 6.9, 7.0, 1.8, 2.5, -0.5, -1.8, 5.6]

   .. versionadded:: 3.13


.. function:: median(data)

   Trả về trung vị (giá trị ở giữa) của dữ liệu số, sử dụng phương pháp phổ biến "trung bình của hai giá trị ở giữa".  Nếu *data* trống, :exc:`StatisticsError` sẽ được phát sinh. *data* có thể là một sequence hoặc iterable.

   Trung vị là một thước đo bền vững về vị trí trung tâm và ít bị ảnh hưởng hơn bởi sự hiện diện của các giá trị ngoại lệ. Khi số lượng điểm dữ liệu là số lẻ, điểm dữ liệu ở giữa sẽ được trả về:

   .. doctest::

      >>> median([1, 3, 5])
      3

   Khi số lượng điểm dữ liệu là số chẵn, trung vị được nội suy bằng cách lấy giá trị trung bình của hai giá trị ở giữa:

   .. doctest::

      >>> median([1, 3, 5, 7])
      4.0

   Cách này phù hợp khi dữ liệu của bạn là rời rạc và bạn không ngại việc trung vị có thể không phải là một điểm dữ liệu thực tế.

   Nếu dữ liệu là thứ bậc (hỗ trợ các phép toán về thứ tự) nhưng không phải dữ liệu số (không hỗ trợ phép cộng), hãy cân nhắc sử dụng :func:`median_low` hoặc :func:`median_high` thay thế.

.. function:: median_low(data)

   Trả về trung vị thấp của dữ liệu số. Nếu *data* trống,
   :exc:`StatisticsError` sẽ được đưa ra. *data* có thể là một sequence hoặc iterable.

   Trung vị thấp luôn là một phần tử của tập dữ liệu. Khi số lượng điểm dữ liệu là số lẻ, giá trị ở giữa sẽ được trả về. Khi số lượng này là số chẵn, giá trị nhỏ hơn trong hai giá trị ở giữa sẽ được trả về.

   .. doctest::

      >>> median_low([1, 3, 5])
      3
      >>> median_low([1, 3, 5, 7])
      3

   Sử dụng trung vị thấp khi dữ liệu của bạn là rời rạc và bạn muốn trung vị là một điểm dữ liệu thực tế thay vì được nội suy.


.. function:: median_high(data)

   Trả về trung vị cao của dữ liệu. Nếu *data* trống, :exc:`StatisticsError` sẽ được phát sinh. *data* có thể là một sequence hoặc iterable.

   Trung vị cao luôn là một phần tử của tập dữ liệu. Khi số điểm dữ liệu là số lẻ, giá trị ở giữa được trả về. Khi là số chẵn, giá trị lớn hơn trong hai giá trị ở giữa được trả về.

   .. doctest::

      >>> median_high([1, 3, 5])
      3
      >>> median_high([1, 3, 5, 7])
      5

   Sử dụng trung vị cao khi dữ liệu của bạn là rời rạc và bạn muốn trung vị là một điểm dữ liệu thực tế thay vì được nội suy.


.. function:: median_grouped(data, interval=1.0)

   Ước tính trung vị cho dữ liệu số đã được `nhóm hoặc chia thành các bin <https://en.wikipedia.org/wiki/Data_binning>`_ quanh trung điểm của các khoảng liên tiếp có độ rộng cố định.

   *data* có thể là bất kỳ iterable nào chứa dữ liệu số, trong đó mỗi giá trị chính xác là trung điểm của một bin. Phải có ít nhất một giá trị.

   *interval* là độ rộng của mỗi bin.

   Ví dụ: thông tin nhân khẩu học có thể đã được tóm tắt thành các nhóm tuổi liên tiếp, mỗi nhóm được biểu thị bằng điểm giữa 5 năm của các khoảng tuổi:

   .. doctest::

      >>> from collections import Counter
      >>> demographics = Counter({
      ...    25: 172,   # 20 đến 30 tuổi
      ...    35: 484,   # 30 đến 40 tuổi
      ...    45: 387,   # 40 đến 50 tuổi
      ...    55:  22,   # 50 đến 60 tuổi
      ...    65:   6,   # 60 đến 70 tuổi
      ... })
      ...

   Phân vị thứ 50 (trung vị) là người thứ 536 trong nhóm gồm 1071 thành viên. Người đó thuộc nhóm tuổi từ 30 đến 40.

   Hàm :func:`median` thông thường sẽ giả định rằng mọi người trong nhóm tuổi ba mươi đều đúng 35 tuổi. Một giả định hợp lý hơn là 484 thành viên của nhóm tuổi đó được phân bố đều trong khoảng từ 30 đến 40. Để làm vậy, chúng ta sử dụng
   :func:`median_grouped`:

   .. doctest::

       >>> data = list(demographics.elements())
       >>> median(data)
       35
       >>> round(median_grouped(data, interval=10), 1)
       37.5

   Bên gọi có trách nhiệm đảm bảo rằng các điểm dữ liệu được phân cách bởi các bội số chính xác của *interval*. Điều này thiết yếu để có được kết quả chính xác. Hàm không kiểm tra điều kiện tiên quyết này.

   Đầu vào có thể là bất kỳ kiểu số nào có thể được chuyển đổi thành số thực trong bước nội suy.


.. function:: mode(data)

   Trả về điểm dữ liệu phổ biến nhất duy nhất từ *data* rời rạc hoặc định danh. Mode (khi tồn tại) là giá trị điển hình nhất và được dùng làm thước đo vị trí trung tâm.

   Nếu có nhiều mode có cùng tần suất, trả về mode đầu tiên được gặp trong *data*. Nếu muốn lấy mode nhỏ nhất hoặc lớn nhất trong số đó, hãy sử dụng ``min(multimode(data))`` hoặc ``max(multimode(data))``. Nếu *data* đầu vào rỗng, :exc:`StatisticsError` sẽ được phát sinh.

   ``mode`` giả định dữ liệu rời rạc và trả về một giá trị duy nhất. Đây là cách xử lý mode tiêu chuẩn thường được giảng dạy ở trường học:

   .. doctest::

      >>> mode([1, 1, 2, 3, 3, 3, 3, 4])
      3

   Mode có tính độc đáo vì đây là thống kê duy nhất trong gói này cũng áp dụng cho dữ liệu định danh (không phải số):

   .. doctest::

      >>> mode(["red", "blue", "blue", "red", "green", "red", "red"])
      'red'

   Chỉ hỗ trợ các đầu vào có thể băm (hashable). Để xử lý kiểu :class:`set`, hãy cân nhắc chuyển kiểu sang :class:`frozenset`. Để xử lý kiểu :class:`list`, hãy cân nhắc chuyển kiểu sang :class:`tuple`. Với các đầu vào hỗn hợp hoặc lồng nhau, hãy cân nhắc sử dụng thuật toán bậc hai chậm hơn này, chỉ phụ thuộc vào các phép kiểm tra tính bằng nhau: ``max(data, key=data.count)``.

   .. versionchanged:: 3.8
      Hiện xử lý các tập dữ liệu đa mode bằng cách trả về mode đầu tiên gặp phải. Trước đây, hàm sẽ phát sinh :exc:`StatisticsError` khi tìm thấy nhiều hơn một mode.


.. function:: multimode(data)

   Trả về danh sách các giá trị xuất hiện thường xuyên nhất theo thứ tự chúng xuất hiện lần đầu trong *data*. Sẽ trả về nhiều hơn một kết quả nếu có nhiều mode hoặc một danh sách rỗng nếu *data* rỗng:

   .. doctest::

        >>> multimode('aabbbbccddddeeffffgg')
        ['b', 'd', 'f']
        >>> multimode('')
        []

   .. versionadded:: 3.8


.. function:: pstdev(data, mu=None)

   Trả về độ lệch chuẩn của tổng thể (căn bậc hai của phương sai tổng thể). Xem :func:`pvariance` để biết các đối số và thông tin chi tiết khác.

   .. doctest::

      >>> pstdev([1.5, 2.5, 2.5, 2.75, 3.25, 4.75])
      0.986893273527251


.. function:: pvariance(data, mu=None)

   Trả về phương sai tổng thể của *data*, một chuỗi hoặc iterable không rỗng gồm các số có giá trị thực. Phương sai, hay moment bậc hai quanh giá trị trung bình, là thước đo mức độ biến thiên (độ phân tán hoặc độ dàn trải) của dữ liệu. Phương sai lớn cho biết dữ liệu bị phân tán rộng; phương sai nhỏ cho biết dữ liệu tập trung gần giá trị trung bình.

   Nếu cung cấp đối số thứ hai tùy chọn *mu*, đối số này phải là giá trị trung bình *population* của *data*. Đối số này cũng có thể được dùng để tính moment bậc hai quanh một điểm không phải là giá trị trung bình. Nếu bị thiếu hoặc là ``None`` (giá trị mặc định), giá trị trung bình số học sẽ được tự động tính.

   Dùng hàm này để tính phương sai từ toàn bộ tổng thể. Để ước tính phương sai từ một mẫu, hàm :func:`variance` thường là lựa chọn phù hợp hơn.

   Ném :exc:`StatisticsError` nếu *data* trống.

   Ví dụ:

   .. doctest::

      >>> data = [0.0, 0.25, 0.25, 1.25, 1.5, 1.75, 2.75, 3.25]
      >>> pvariance(data)
      1.25

   Nếu bạn đã tính mean của dữ liệu, bạn có thể truyền giá trị đó làm đối số thứ hai tùy chọn *mu* để tránh tính toán lại:

   .. doctest::

      >>> mu = mean(data)
      >>> pvariance(data, mu)
      1.25

   Decimal và Fraction được hỗ trợ:

   .. doctest::

      >>> from decimal import Decimal as D
      >>> pvariance([D("27.5"), D("30.25"), D("30.25"), D("34.5"), D("41.75")])
      Decimal('24.815')

      >>> from fractions import Fraction as F
      >>> pvariance([F(1, 4), F(5, 4), F(1, 2)])
      Fraction(13, 72)

   .. note::

      Khi được gọi với toàn bộ tổng thể, hàm này cho ra phương sai tổng thể σ². Khi được gọi trên một mẫu thay vào đó, đây là phương sai mẫu có độ chệch s², còn được gọi là phương sai với N bậc tự do.

      Nếu bằng cách nào đó bạn biết mean tổng thể thực sự μ, bạn có thể sử dụng hàm này để tính phương sai của một mẫu bằng cách truyền mean tổng thể đã biết làm đối số thứ hai. Với điều kiện các điểm dữ liệu là một mẫu ngẫu nhiên của tổng thể, kết quả sẽ là một ước tính không chệch của phương sai tổng thể.


.. function:: stdev(data, xbar=None)

   Trả về độ lệch chuẩn mẫu (căn bậc hai của phương sai mẫu). Xem :func:`variance` để biết các đối số và thông tin chi tiết khác.

   .. doctest::

      >>> stdev([1.5, 2.5, 2.5, 2.75, 3.25, 4.75])
      1.0810874155219827


.. function:: variance(data, xbar=None)

   Trả về phương sai mẫu của *data*, một iterable gồm ít nhất hai số thực. Phương sai, hay moment bậc hai quanh giá trị trung bình, là thước đo mức độ biến thiên (độ phân tán hoặc độ phân tán) của dữ liệu. Phương sai lớn cho biết dữ liệu bị phân tán rộng; phương sai nhỏ cho biết dữ liệu tập trung gần giá trị trung bình.

   Nếu cung cấp đối số thứ hai tùy chọn *xbar*, đối số này phải là giá trị trung bình *sample* của *data*. Nếu đối số này bị thiếu hoặc là ``None`` (giá trị mặc định), giá trị trung bình sẽ được tự động tính.

   Sử dụng hàm này khi dữ liệu của bạn là một mẫu từ một tổng thể. Để tính phương sai của toàn bộ tổng thể, hãy xem :func:`pvariance`.

   Phát sinh :exc:`StatisticsError` nếu *data* có ít hơn hai giá trị.

   Ví dụ:

   .. doctest::

      >>> data = [2.75, 1.75, 1.25, 0.25, 0.5, 1.25, 3.5]
      >>> variance(data)
      1.3720238095238095

   Nếu bạn đã tính giá trị trung bình mẫu của dữ liệu, bạn có thể truyền giá trị đó làm đối số thứ hai tùy chọn *xbar* để tránh tính lại:

   .. doctest::

      >>> m = mean(data)
      >>> variance(data, m)
      1.3720238095238095

   Hàm này không cố gắng xác minh rằng bạn đã truyền giá trị trung bình thực tế làm *xbar*. Việc sử dụng các giá trị tùy ý cho *xbar* có thể dẫn đến kết quả không hợp lệ hoặc không thể xảy ra.

   Các giá trị Decimal và Fraction được hỗ trợ:

   .. doctest::

      >>> from decimal import Decimal as D
      >>> variance([D("27.5"), D("30.25"), D("30.25"), D("34.5"), D("41.75")])
      Decimal('31.01875')

      >>> from fractions import Fraction as F
      >>> variance([F(1, 6), F(1, 2), F(5, 3)])
      Fraction(67, 108)

   .. note::

      Đây là phương sai mẫu s² với hiệu chỉnh Bessel, còn được gọi là phương sai với N-1 bậc tự do. Với điều kiện các điểm dữ liệu mang tính đại diện (ví dụ: độc lập và phân phối đồng nhất), kết quả sẽ là một ước lượng không chệch của phương sai tổng thể thực.

      Nếu bằng cách nào đó bạn biết giá trị trung bình tổng thể thực tế μ, hãy truyền giá trị đó vào
      :func:`pvariance` function dưới dạng tham số *mu* để lấy phương sai của một mẫu.

.. function:: quantiles(data, *, n=4, method='exclusive')

   Chia *data* thành *n* khoảng liên tục có xác suất bằng nhau. Trả về danh sách gồm ``n - 1`` điểm cắt phân tách các khoảng.

   Đặt *n* thành 4 để lấy các tứ phân vị (mặc định). Đặt *n* thành 10 để lấy các thập phân vị. Đặt *n* thành 100 để lấy các phân vị, cho ra 99 điểm cắt phân tách *data* thành 100 nhóm có kích thước bằng nhau. Phát sinh :exc:`StatisticsError` nếu *n* nhỏ hơn 1.

   *data* có thể là bất kỳ iterable nào chứa dữ liệu mẫu. Để có kết quả có ý nghĩa, số điểm dữ liệu trong *data* phải lớn hơn *n*. Phát sinh :exc:`StatisticsError` nếu không có ít nhất một điểm dữ liệu.

   Các điểm cắt được nội suy tuyến tính từ hai điểm dữ liệu gần nhất. Ví dụ: nếu một điểm cắt nằm cách một phần ba khoảng cách giữa hai giá trị mẫu, ``100`` và ``112``, thì điểm cắt sẽ có giá trị ``104``.

   *method* dùng để tính các quantile có thể thay đổi tùy theo việc *data* có bao gồm hay loại trừ các giá trị nhỏ nhất và lớn nhất có thể có trong tổng thể hay không.

   *method* mặc định là "exclusive" và được dùng cho dữ liệu lấy mẫu từ một tổng thể có thể có các giá trị cực đoan hơn những giá trị được tìm thấy trong các mẫu. Tỷ lệ của tổng thể nằm dưới *i-th* trong số *m* điểm dữ liệu đã sắp xếp được tính là ``i / (m + 1)``. Với chín giá trị mẫu, phương pháp này sắp xếp chúng và gán các percentile sau: 10%, 20%, 30%, 40%, 50%, 60%, 70%, 80%, 90%.

   Đặt *method* thành "inclusive" được dùng để mô tả dữ liệu của tổng thể hoặc các mẫu được biết là bao gồm những giá trị cực đoan nhất từ tổng thể. Giá trị nhỏ nhất trong *data* được xem là percentile thứ 0 và giá trị lớn nhất được xem là percentile thứ 100. Tỷ lệ của tổng thể nằm dưới *i-th* trong số *m* điểm dữ liệu đã sắp xếp được tính là ``(i - 1) / (m - 1)``. Với 11 giá trị mẫu, phương pháp này sắp xếp chúng và gán các percentile sau: 0%, 10%, 20%, 30%, 40%, 50%, 60%, 70%, 80%, 90%, 100%.

   .. doctest::

        # Điểm cắt decile cho dữ liệu được lấy mẫu theo thực nghiệm
        >>> data = [105, 129, 87, 86, 111, 111, 89, 81, 108, 92, 110,
        ...         100, 75, 105, 103, 109, 76, 119, 99, 91, 103, 129,
        ...         106, 101, 84, 111, 74, 87, 86, 103, 103, 106, 86,
        ...         111, 75, 87, 102, 121, 111, 88, 89, 101, 106, 95,
        ...         103, 107, 101, 81, 109, 104]
        >>> [round(q, 1) for q in quantiles(data, n=10)]
        [81.0, 86.2, 89.0, 99.4, 102.5, 103.6, 106.0, 109.8, 111.0]

   .. versionadded:: 3.8

   .. versionchanged:: 3.13
      Không còn phát sinh ngoại lệ khi đầu vào chỉ có một điểm dữ liệu. Điều này cho phép xây dựng các ước tính quantile từng điểm mẫu một, dần được tinh chỉnh với mỗi điểm dữ liệu mới.

.. function:: covariance(x, y, /)

   Trả về hiệp phương sai mẫu của hai đầu vào *x* và *y*. Hiệp phương sai là thước đo mức độ biến thiên đồng thời của hai đầu vào.

   Cả hai đầu vào phải có cùng độ dài (không nhỏ hơn hai), nếu không
   :exc:`StatisticsError` sẽ được phát sinh.

   Ví dụ:

   .. doctest::

      >>> x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
      >>> y = [1, 2, 3, 1, 2, 3, 1, 2, 3]
      >>> covariance(x, y)
      0.75
      >>> z = [9, 8, 7, 6, 5, 4, 3, 2, 1]
      >>> covariance(x, z)
      -7.5
      >>> covariance(z, x)
      -7.5

   .. versionadded:: 3.10

.. function:: correlation(x, y, /, *, method='linear')

   Trả về `hệ số tương quan Pearson <https://en.wikipedia.org/wiki/Pearson_correlation_coefficient>`_ cho hai đầu vào. Hệ số tương quan Pearson *r* nhận các giá trị từ -1 đến +1. Hệ số này đo độ mạnh và hướng của mối quan hệ tuyến tính.

   Nếu *method* là "ranked", tính `hệ số tương quan thứ hạng Spearman <https://en.wikipedia.org/wiki/Spearman%27s_rank_correlation_coefficient>`_ cho hai đầu vào. Dữ liệu được thay thế bằng thứ hạng. Các giá trị trùng nhau được lấy trung bình để các giá trị bằng nhau nhận cùng một thứ hạng. Hệ số thu được đo độ mạnh của một mối quan hệ đơn điệu.

   Hệ số tương quan Spearman phù hợp với dữ liệu thứ bậc hoặc dữ liệu liên tục không đáp ứng yêu cầu về tỷ lệ tuyến tính của hệ số tương quan Pearson.

   Cả hai đầu vào phải có cùng độ dài (không nhỏ hơn hai) và không được là hằng số; nếu không, :exc:`StatisticsError` sẽ được phát sinh.

   Ví dụ về `các định luật chuyển động hành tinh của Kepler <https://en.wikipedia.org/wiki/Kepler's_laws_of_planetary_motion>`_:

   .. doctest::

      >>> # Sao Thủy, Sao Kim, Trái Đất, Sao Hỏa, Sao Mộc, Sao Thổ, Sao Thiên Vương và Sao Hải Vương
      >>> orbital_period = [88, 225, 365, 687, 4331, 10_756, 30_687, 60_190]    # ngày
      >>> dist_from_sun = [58, 108, 150, 228, 778, 1_400, 2_900, 4_500] # triệu km

      >>> # Cho thấy tồn tại mối quan hệ đơn điệu hoàn hảo
      >>> correlation(orbital_period, dist_from_sun, method='ranked')
      1.0

      >>> # Quan sát thấy mối quan hệ tuyến tính không hoàn hảo
      >>> round(correlation(orbital_period, dist_from_sun), 4)
      0.9882

      >>> # Minh họa định luật thứ ba của Kepler: Có tương quan tuyến tính
      >>> # giữa bình phương của chu kỳ quỹ đạo và lập phương của
      >>> # khoảng cách từ Mặt Trời.
      >>> period_squared = [p * p for p in orbital_period]
      >>> dist_cubed = [d * d * d for d in dist_from_sun]
      >>> round(correlation(period_squared, dist_cubed), 4)
      1.0

   .. versionadded:: 3.10

   .. versionchanged:: 3.12
      Đã bổ sung hỗ trợ cho hệ số tương quan thứ hạng Spearman.

.. function:: linear_regression(x, y, /, *, proportional=False)

   Trả về hệ số góc và tung độ gốc của các tham số `hồi quy tuyến tính đơn giản <https://en.wikipedia.org/wiki/Simple_linear_regression>`_ được ước tính bằng phương pháp bình phương tối thiểu thông thường. Hồi quy tuyến tính đơn giản mô tả mối quan hệ giữa biến độc lập *x* và biến phụ thuộc *y* theo hàm tuyến tính sau:

      *y = slope \* x + intercept + noise*

   trong đó ``slope`` và ``intercept`` là các tham số hồi quy được ước tính, còn ``noise`` biểu thị độ biến thiên của dữ liệu không được giải thích bởi hồi quy tuyến tính (bằng hiệu giữa các giá trị dự đoán và giá trị thực tế của biến phụ thuộc).

   Cả hai đầu vào phải có cùng độ dài (không nhỏ hơn hai), và biến độc lập *x* không được là hằng số; nếu không, một :exc:`StatisticsError` sẽ được phát sinh.

   Ví dụ: chúng ta có thể sử dụng `ngày phát hành các bộ phim Monty Python <https://en.wikipedia.org/wiki/Monty_Python#Films>`_ để dự đoán tổng số bộ phim Monty Python lẽ ra đã được sản xuất vào năm 2019, với giả định rằng họ vẫn duy trì tốc độ đó.

   .. doctest::

      >>> year = [1971, 1975, 1979, 1982, 1983]
      >>> films_total = [1, 2, 3, 4, 5]
      >>> slope, intercept = linear_regression(year, films_total)
      >>> round(slope * 2019 + intercept)
      16

   Nếu *tỷ lệ thuận* là true, biến độc lập *x* và biến phụ thuộc *y* được giả định là tỷ lệ thuận trực tiếp. Dữ liệu được khớp với một đường thẳng đi qua gốc tọa độ. Vì *intercept* sẽ luôn là 0.0, hàm tuyến tính cơ sở được rút gọn thành:

      *y = slope \* x + noise*

   Tiếp tục ví dụ từ :func:`correlation`, chúng ta xem xét mức độ chính xác mà một model dựa trên các hành tinh chính có thể dự đoán khoảng cách quỹ đạo của các hành tinh lùn:

   .. doctest::

      >>> model = linear_regression(period_squared, dist_cubed, proportional=True)
      >>> slope = model.slope

      >>> # Các hành tinh lùn:   Pluto,  Eris,    Makemake, Haumea, Ceres
      >>> orbital_periods = [90_560, 204_199, 111_845, 103_410, 1_680]  # ngày
      >>> predicted_dist = [math.cbrt(slope * (p * p)) for p in orbital_periods]
      >>> list(map(round, predicted_dist))
      [5912, 10166, 6806, 6459, 414]

      >>> [5_906, 10_152, 6_796, 6_450, 414]  # khoảng cách thực tế tính bằng triệu km
      [5906, 10152, 6796, 6450, 414]

   .. versionadded:: 3.10

   .. versionchanged:: 3.11
      Đã thêm hỗ trợ cho *tỷ lệ*.

Ngoại lệ
--------

Một ngoại lệ duy nhất được định nghĩa:

.. exception:: StatisticsError

   Lớp con của :exc:`ValueError` dành cho các ngoại lệ liên quan đến thống kê.


Các đối tượng :class:`NormalDist`
---------------------------------

:class:`NormalDist` là công cụ để tạo và thao tác với các phân phối chuẩn của một `biến ngẫu nhiên <http://www.stat.yale.edu/Courses/1997-98/101/ranvar.htm>`_. Đây là một lớp coi giá trị trung bình và độ lệch chuẩn của các phép đo dữ liệu như một thực thể duy nhất.

Các phân phối chuẩn xuất hiện từ `Định lý giới hạn trung tâm <https://en.wikipedia.org/wiki/Central_limit_theorem>`_ và có nhiều ứng dụng trong thống kê.

.. class:: NormalDist(mu=0.0, sigma=1.0)

    Trả về một đối tượng *NormalDist* mới, trong đó *mu* biểu thị `trung bình cộng <https://en.wikipedia.org/wiki/Arithmetic_mean>`_ và *sigma* biểu thị `độ lệch chuẩn <https://en.wikipedia.org/wiki/Standard_deviation>`_.

    Nếu *sigma* là số âm, sẽ ném :exc:`StatisticsError`.

    .. attribute:: mean

       Một thuộc tính chỉ đọc biểu thị `trung bình cộng <https://en.wikipedia.org/wiki/Arithmetic_mean>`_ của một phân phối chuẩn.

    .. attribute:: median

       Một thuộc tính chỉ đọc biểu thị `trung vị <https://en.wikipedia.org/wiki/Median>`_ của một phân phối chuẩn.

    .. attribute:: mode

       Một thuộc tính chỉ đọc biểu thị `mốt <https://en.wikipedia.org/wiki/Mode_(statistics)>`_ của một phân phối chuẩn.

    .. attribute:: stdev

       Một thuộc tính chỉ đọc biểu thị `độ lệch chuẩn <https://en.wikipedia.org/wiki/Standard_deviation>`_ của một phân phối chuẩn.

    .. attribute:: variance

       Một thuộc tính chỉ đọc biểu thị `phương sai <https://en.wikipedia.org/wiki/Variance>`_ của một phân phối chuẩn. Bằng bình phương của độ lệch chuẩn.

    .. classmethod:: NormalDist.from_samples(data)

       Tạo một thể hiện phân phối chuẩn với các tham số *mu* và *sigma*, được ước tính từ *data* bằng cách sử dụng :func:`fmean` và :func:`stdev`.

       *data* có thể là bất kỳ :term:`iterable` nào và phải bao gồm các giá trị có thể được chuyển đổi thành kiểu :class:`float`. Nếu *data* không chứa ít nhất hai phần tử, sẽ phát sinh :exc:`StatisticsError` vì cần ít nhất một điểm để ước tính giá trị trung tâm và ít nhất hai điểm để ước tính độ phân tán.

    .. method:: NormalDist.samples(n, *, seed=None)

       Tạo *n* mẫu ngẫu nhiên với giá trị trung bình và độ lệch chuẩn đã cho. Trả về một :class:`list` gồm các giá trị :class:`float`.

       Nếu cung cấp *seed*, một thể hiện mới của bộ tạo số ngẫu nhiên nền tảng sẽ được tạo. Điều này hữu ích để tạo ra các kết quả có thể tái lập, ngay cả trong ngữ cảnh đa luồng.

       .. versionchanged:: 3.13

       Đã chuyển sang một thuật toán nhanh hơn. Để tái tạo các mẫu từ các phiên bản trước, hãy sử dụng :func:`random.seed` và :func:`random.gauss`.

    .. method:: NormalDist.pdf(x)

       Sử dụng `hàm mật độ xác suất (pdf) <https://en.wikipedia.org/wiki/Probability_density_function>`_, tính khả năng tương đối rằng biến ngẫu nhiên *X* sẽ ở gần giá trị *x* đã cho. Về mặt toán học, đây là giới hạn của tỷ số ``P(x <= X < x+dx) / dx`` khi *dx* tiến đến bằng không.

       Khả năng tương đối được tính bằng xác suất một mẫu xuất hiện trong một khoảng hẹp chia cho độ rộng của khoảng đó (do đó có từ "mật độ"). Vì khả năng này mang tính tương đối so với các điểm khác, giá trị của nó có thể lớn hơn ``1.0``.

    .. method:: NormalDist.cdf(x)

       Sử dụng `hàm phân phối tích lũy (cdf) <https://en.wikipedia.org/wiki/Cumulative_distribution_function>`_, tính xác suất để biến ngẫu nhiên *X* nhỏ hơn hoặc bằng *x*. Về mặt toán học, được viết là ``P(X <= x)``.

    .. method:: NormalDist.inv_cdf(p)

       Tính hàm phân phối tích lũy nghịch đảo, còn được gọi là `hàm quantile <https://en.wikipedia.org/wiki/Quantile_function>`_ hoặc hàm `percent-point <https://web.archive.org/web/20190203145224/https://www.statisticshowto.datasciencecentral.com/inverse-distribution-function/>`_. Về mặt toán học, được viết là ``x : P(X <= x) = p``.

       Tìm giá trị *x* của biến ngẫu nhiên *X* sao cho xác suất biến này nhỏ hơn hoặc bằng giá trị đó bằng xác suất đã cho *p*.

    .. method:: NormalDist.overlap(other)

       Đo mức độ phù hợp giữa hai phân phối xác suất chuẩn. Trả về một giá trị từ 0.0 đến 1.0, biểu thị `diện tích chồng lấp của hai hàm mật độ xác suất <https://www.rasch.org/rmt/rmt101r.htm>`_.

    .. method:: NormalDist.quantiles(n=4)

        Chia phân phối chuẩn thành *n* khoảng liên tục có xác suất bằng nhau. Trả về danh sách gồm (n - 1) điểm cắt phân tách các khoảng.

        Đặt *n* bằng 4 cho các tứ phân vị (giá trị mặc định). Đặt *n* bằng 10 cho các phân vị thập phân. Đặt *n* bằng 100 cho các phần trăm vị, tạo ra 99 điểm cắt phân tách phân phối chuẩn thành 100 nhóm có kích thước bằng nhau.

    .. method:: NormalDist.zscore(x)

        Tính `Điểm chuẩn hóa <https://www.statisticshowto.com/probability-and-statistics/z-score/>`_ mô tả *x* theo số độ lệch chuẩn cao hơn hoặc thấp hơn giá trị trung bình của phân phối chuẩn: ``(x - mean) / stdev``.

        .. versionadded:: 3.9

    Các instance của :class:`NormalDist` hỗ trợ phép cộng, phép trừ, phép nhân và phép chia với một hằng số. Các phép toán này được dùng để tịnh tiến và co giãn. Ví dụ:

    .. doctest::

        >>> temperature_february = NormalDist(5, 2.5)             # Celsius
        >>> temperature_february * (9/5) + 32                     # Fahrenheit
        NormalDist(mu=41.0, sigma=4.5)

    Không hỗ trợ phép chia một hằng số cho một instance của :class:`NormalDist` vì kết quả sẽ không có phân phối chuẩn.

    Vì các phân phối chuẩn phát sinh từ các tác động cộng của những biến độc lập, bạn có thể `cộng và trừ hai biến ngẫu nhiên độc lập có phân phối chuẩn <https://en.wikipedia.org/wiki/Sum_of_normally_distributed_random_variables>`_ được biểu diễn dưới dạng các instance của :class:`NormalDist`. Ví dụ:

    .. doctest::

        >>> birth_weights = NormalDist.from_samples([2.5, 3.1, 2.1, 2.4, 2.7, 3.5])
        >>> drug_effects = NormalDist(0.4, 0.15)
        >>> combined = birth_weights + drug_effects
        >>> round(combined.mean, 1)
        3.1
        >>> round(combined.stdev, 1)
        0.5

    .. versionadded:: 3.8


Các ví dụ và công thức
----------------------


Các bài toán xác suất kinh điển
*******************************

:class:`NormalDist` dễ dàng giải quyết các bài toán xác suất kinh điển.

Ví dụ, dựa trên `dữ liệu lịch sử về các kỳ thi SAT <https://nces.ed.gov/programs/digest/d17/tables/dt17_226.40.asp>`_ cho thấy điểm số có phân phối chuẩn với giá trị trung bình là 1060 và độ lệch chuẩn là 195, hãy xác định tỷ lệ phần trăm học sinh có điểm kiểm tra từ 1100 đến 1200, sau khi làm tròn đến số nguyên gần nhất:

.. doctest::

    >>> sat = NormalDist(1060, 195)
    >>> fraction = sat.cdf(1200 + 0.5) - sat.cdf(1100 - 0.5)
    >>> round(fraction * 100.0, 1)
    18.4

Tìm `các tứ phân vị <https://en.wikipedia.org/wiki/Quartile>`_ và `các thập phân vị <https://en.wikipedia.org/wiki/Decile>`_ của điểm SAT:

.. doctest::

    >>> list(map(round, sat.quantiles()))
    [928, 1060, 1192]
    >>> list(map(round, sat.quantiles(n=10)))
    [810, 896, 958, 1011, 1060, 1109, 1162, 1224, 1310]


Các đầu vào Monte Carlo cho mô phỏng
************************************

Để ước tính phân phối cho một mô hình không dễ giải bằng phương pháp giải tích, :class:`NormalDist` có thể tạo các mẫu đầu vào cho một `mô phỏng Monte Carlo <https://en.wikipedia.org/wiki/Monte_Carlo_method>`_:

.. doctest::

    >>> def model(x, y, z):
    ...     return (3*x + 7*x*y - 5*y) / (11 * z)
    ...
    >>> n = 100_000
    >>> X = NormalDist(10, 2.5).samples(n, seed=3652260728)
    >>> Y = NormalDist(15, 1.75).samples(n, seed=4582495471)
    >>> Z = NormalDist(50, 1.25).samples(n, seed=6582483453)
    >>> quantiles(map(model, X, Y, Z))       # doctest: +SKIP
    [1.4591308524824727, 1.8035946855390597, 2.175091447274739]

Xấp xỉ các phân phối nhị thức
*****************************

Có thể dùng phân phối chuẩn để xấp xỉ `phân phối nhị thức <https://mathworld.wolfram.com/BinomialDistribution.html>`_ khi kích thước mẫu lớn và xác suất một phép thử thành công gần 50%.

Ví dụ: một hội nghị mã nguồn mở có 750 người tham dự và hai phòng, mỗi phòng có sức chứa 500 người. Có một bài nói chuyện về Python và một bài khác về Ruby. Trong các hội nghị trước, 65% người tham dự thích nghe các bài nói chuyện về Python. Giả sử sở thích của quần thể không thay đổi, xác suất phòng Python vẫn nằm trong giới hạn sức chứa là bao nhiêu?

.. doctest::

    >>> n = 750             # Kích thước mẫu
    >>> p = 0.65            # Sở thích Python
    >>> q = 1.0 - p         # Sở thích Ruby
    >>> k = 500             # Sức chứa phòng

    >>> # Xấp xỉ bằng phân phối chuẩn tích lũy
    >>> from math import sqrt
    >>> round(NormalDist(mu=n*p, sigma=sqrt(n*p*q)).cdf(k + 0.5), 4)
    0.8402

    >>> # Giải pháp chính xác sử dụng phân phối nhị thức tích lũy
    >>> from math import comb, fsum
    >>> round(fsum(comb(n, r) * p**r * q**(n-r) for r in range(k+1)), 4)
    0.8402

    >>> # Phép xấp xỉ bằng mô phỏng
    >>> from random import seed, binomialvariate
    >>> seed(8675309)
    >>> mean(binomialvariate(n, p) <= k for i in range(10_000))
    0.8406


Bộ phân loại Bayes ngây thơ
***************************

Các phân phối chuẩn thường xuất hiện trong những bài toán machine learning.

Wikipedia có `một ví dụ hay về Bộ phân loại Bayes ngây thơ <https://en.wikipedia.org/wiki/Naive_Bayes_classifier#Person_classification>`_. Thách thức là dự đoán giới tính của một người từ các phép đo của những đặc trưng có phân phối chuẩn, bao gồm chiều cao, cân nặng và cỡ bàn chân.

Chúng ta được cung cấp một tập dữ liệu huấn luyện với các phép đo của tám người. Các phép đo được giả định là có phân phối chuẩn, vì vậy chúng ta tóm tắt dữ liệu bằng :class:`NormalDist`:

.. doctest::

    >>> height_male = NormalDist.from_samples([6, 5.92, 5.58, 5.92])
    >>> height_female = NormalDist.from_samples([5, 5.5, 5.42, 5.75])
    >>> weight_male = NormalDist.from_samples([180, 190, 170, 165])
    >>> weight_female = NormalDist.from_samples([100, 150, 130, 150])
    >>> foot_size_male = NormalDist.from_samples([12, 11, 12, 10])
    >>> foot_size_female = NormalDist.from_samples([6, 8, 7, 9])

Tiếp theo, chúng ta gặp một người mới đã biết các phép đo đặc trưng nhưng chưa biết giới tính:

.. doctest::

    >>> ht = 6.0        # chiều cao
    >>> wt = 130        # cân nặng
    >>> fs = 8          # cỡ bàn chân

Bắt đầu với `xác suất tiên nghiệm <https://en.wikipedia.org/wiki/Prior_probability>`_ 50% cho khả năng là nam hoặc nữ, chúng ta tính xác suất hậu nghiệm bằng xác suất tiên nghiệm nhân với tích của các likelihood tương ứng với các phép đo đặc trưng khi biết giới tính:

.. doctest::

   >>> prior_male = 0.5
   >>> prior_female = 0.5
   >>> posterior_male = (prior_male * height_male.pdf(ht) *
   ...                   weight_male.pdf(wt) * foot_size_male.pdf(fs))

   >>> posterior_female = (prior_female * height_female.pdf(ht) *
   ...                     weight_female.pdf(wt) * foot_size_female.pdf(fs))

Dự đoán cuối cùng sẽ là lớp có xác suất hậu nghiệm lớn nhất. Đây được gọi là `maximum a posteriori <https://en.wikipedia.org/wiki/Maximum_a_posteriori_estimation>`_ hay MAP:

.. doctest::

  >>> 'male' if posterior_male > posterior_female else 'female'
  'female'


..
   # Các modeline này phải xuất hiện trong mười dòng cuối cùng của tệp. kate: indent-width 3; remove-trailing-space on; replace-tabs on; encoding utf-8;

.. _`NumPy`: https://numpy.org
.. _`SciPy`: https://scipy.org/
.. _`outliers`: https://en.wikipedia.org/wiki/Outlier
.. _`central tendency`: https://en.wikipedia.org/wiki/Central_tendency
.. _`Kernel Density Estimation (KDE)`: https://www.itm-conferences.org/articles/itmconf/pdf/2018/08/itmconf_sam2018_00037.pdf
.. _`a kernel function`: https://en.wikipedia.org/wiki/Kernel_(statistics)
.. _`Wikipedia has an example`: https://en.wikipedia.org/wiki/Kernel_density_estimation#Example
.. _`grouped or binned`: https://en.wikipedia.org/wiki/Data_binning
.. _`Pearson's correlation coefficient`: https://en.wikipedia.org/wiki/Pearson_correlation_coefficient
.. _`Spearman's rank correlation coefficient`: https://en.wikipedia.org/wiki/Spearman%27s_rank_correlation_coefficient
.. _`Kepler's laws of planetary motion`: https://en.wikipedia.org/wiki/Kepler's_laws_of_planetary_motion
.. _`simple linear regression`: https://en.wikipedia.org/wiki/Simple_linear_regression
.. _`release dates of the Monty Python films`: https://en.wikipedia.org/wiki/Monty_Python#Films
.. _`random variable`: http://www.stat.yale.edu/Courses/1997-98/101/ranvar.htm
.. _`Central Limit Theorem`: https://en.wikipedia.org/wiki/Central_limit_theorem
.. _`arithmetic mean`: https://en.wikipedia.org/wiki/Arithmetic_mean
.. _`standard deviation`: https://en.wikipedia.org/wiki/Standard_deviation
.. _`median`: https://en.wikipedia.org/wiki/Median
.. _`mode`: https://en.wikipedia.org/wiki/Mode_(statistics)
.. _`variance`: https://en.wikipedia.org/wiki/Variance
.. _`probability density function (pdf)`: https://en.wikipedia.org/wiki/Probability_density_function
.. _`cumulative distribution function (cdf)`: https://en.wikipedia.org/wiki/Cumulative_distribution_function
.. _`quantile function`: https://en.wikipedia.org/wiki/Quantile_function
.. _`percent-point`: https://web.archive.org/web/20190203145224/https://www.statisticshowto.datasciencecentral.com/inverse-distribution-function/
.. _`the overlapping area for the two probability density functions`: https://www.rasch.org/rmt/rmt101r.htm
.. _`Standard Score`: https://www.statisticshowto.com/probability-and-statistics/z-score/
.. _`add and subtract two independent normally distributed random variables`: https://en.wikipedia.org/wiki/Sum_of_normally_distributed_random_variables
.. _`historical data for SAT exams`: https://nces.ed.gov/programs/digest/d17/tables/dt17_226.40.asp
.. _`quartiles`: https://en.wikipedia.org/wiki/Quartile
.. _`deciles`: https://en.wikipedia.org/wiki/Decile
.. _`Monte Carlo simulation`: https://en.wikipedia.org/wiki/Monte_Carlo_method
.. _`Binomial distributions`: https://mathworld.wolfram.com/BinomialDistribution.html
.. _`nice example of a Naive Bayesian Classifier`: https://en.wikipedia.org/wiki/Naive_Bayes_classifier#Person_classification
.. _`prior probability`: https://en.wikipedia.org/wiki/Prior_probability
.. _`maximum a posteriori`: https://en.wikipedia.org/wiki/Maximum_a_posteriori_estimation
