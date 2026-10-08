:mod:`!random` --- Tạo số giả ngẫu nhiên
========================================

.. module:: random
   :synopsis: Tạo số giả ngẫu nhiên với nhiều phân phối phổ biến khác nhau.

**Mã nguồn:** :source:`Lib/random.py`

--------------

Mô-đun này triển khai các bộ sinh số giả ngẫu nhiên cho nhiều phân phối khác nhau.

Đối với số nguyên, mô-đun cung cấp cách chọn đồng đều từ một khoảng. Đối với các dãy, mô-đun cung cấp cách chọn đồng đều một phần tử ngẫu nhiên, một hàm tạo hoán vị ngẫu nhiên của một danh sách ngay tại chỗ và một hàm lấy mẫu ngẫu nhiên không hoàn lại.

Trên trục số thực, có các hàm tính các phân phối đều, chuẩn (Gaussian), lognormal, mũ âm, gamma và beta. Để tạo các phân phối góc, có thể sử dụng phân phối von Mises.

Hầu hết các hàm của mô-đun đều phụ thuộc vào hàm cơ bản :func:`.random`, hàm này tạo ra một số thực ngẫu nhiên theo phân phối đều trong khoảng nửa kín ``0.0 <= X < 1.0``. Python sử dụng Mersenne Twister làm bộ sinh cốt lõi. Nó tạo ra các số thực với độ chính xác 53 bit và có chu kỳ 2\*\*19937-1. Phần triển khai nền tảng bằng C vừa nhanh vừa an toàn với luồng. Mersenne Twister là một trong những bộ sinh số ngẫu nhiên được kiểm thử kỹ lưỡng nhất hiện nay. Tuy nhiên, vì hoàn toàn mang tính xác định, nó không phù hợp cho mọi mục đích và hoàn toàn không phù hợp cho các mục đích mật mã.

Các hàm do module này cung cấp thực chất là các bound method của một instance ẩn thuộc lớp :class:`random.Random`. Bạn có thể khởi tạo các instance :class:`Random` của riêng mình để nhận được các generator không dùng chung trạng thái.

Lớp :class:`Random` cũng có thể được subclass nếu bạn muốn sử dụng một basic generator khác do chính mình thiết kế: xem tài liệu về lớp đó để biết thêm chi tiết.

Module :mod:`!random` cũng cung cấp lớp :class:`SystemRandom`, lớp này sử dụng hàm hệ thống :func:`os.urandom` để tạo các số ngẫu nhiên từ những nguồn do hệ điều hành cung cấp.

.. warning::

   Không nên sử dụng các pseudo-random generator của module này cho mục đích bảo mật. Để sử dụng cho mục đích bảo mật hoặc mật mã, hãy xem
   module :mod:`secrets`.

.. seealso::

   M. Matsumoto và T. Nishimura, "Bộ sinh số giả ngẫu nhiên đồng nhất, phân bố đều trong 623 chiều
   ", ACM Transactions on Modeling and Computer Simulation Tập 8, Số 1, tháng 1, tr. 3--30, 1998.


   `Công thức Complementary-Multiply-with-Carry <https://code.activestate.com/recipes/576707-long-period-random-number-generator/>`_ cho một bộ tạo số ngẫu nhiên thay thế tương thích, có chu kỳ dài và các thao tác cập nhật tương đối đơn giản.

.. note::
   Bộ tạo số ngẫu nhiên toàn cục và các thực thể của :class:`Random` đều an toàn với thread. Tuy nhiên, trong bản build free-threaded, các lệnh gọi đồng thời đến bộ tạo toàn cục hoặc cùng một thực thể của :class:`Random` có thể gặp tình trạng tranh chấp và hiệu năng kém. Thay vào đó, hãy cân nhắc sử dụng các thực thể riêng của :class:`Random` cho từng thread.


Các hàm quản lý
---------------

.. function:: seed(a=None, version=2)

   Khởi tạo bộ tạo số ngẫu nhiên.

   Nếu *a* bị bỏ qua hoặc ``None``, thời gian hệ thống hiện tại sẽ được sử dụng. Nếu hệ điều hành cung cấp các nguồn ngẫu nhiên, chúng sẽ được sử dụng thay cho thời gian hệ thống (xem hàm :func:`os.urandom` để biết chi tiết về khả năng cung cấp).

   Nếu *a* là một int, giá trị tuyệt đối của nó sẽ được sử dụng trực tiếp.

   Với phiên bản 2 (mặc định), một đối tượng :class:`str`, :class:`bytes` hoặc :class:`bytearray` sẽ được chuyển đổi thành :class:`int` và tất cả các bit của nó đều được sử dụng.

   Với version 1 (được cung cấp để tái tạo các chuỗi ngẫu nhiên từ những version Python cũ hơn), thuật toán cho :class:`str` và :class:`bytes` tạo ra một phạm vi seed hẹp hơn.

   .. versionchanged:: 3.2
      Đã chuyển sang scheme version 2, sử dụng tất cả các bit trong seed dạng chuỗi.

   .. versionchanged:: 3.11
      *seed* phải thuộc một trong các kiểu sau: ``None``, :class:`int`, :class:`float`, :class:`str`,
      :class:`bytes`, hoặc :class:`bytearray`.

.. function:: getstate()

   Trả về một object ghi lại state nội bộ hiện tại của generator. Có thể truyền object này vào :func:`setstate` để khôi phục state.


.. function:: setstate(state)

   *state* lẽ ra phải được lấy từ một lần gọi trước đó đến :func:`getstate`, và
   :func:`setstate` khôi phục state nội bộ của generator về trạng thái tại thời điểm gọi :func:`getstate`.


Các hàm cho byte
----------------

.. function:: randbytes(n)

   Tạo *n* byte ngẫu nhiên.

   Không nên sử dụng phương thức này để tạo token bảo mật. Hãy sử dụng :func:`secrets.token_bytes` thay thế.

   .. versionadded:: 3.9


Các hàm cho số nguyên
---------------------

.. function:: randrange(stop)
              randrange(start, stop[, step])

   Trả về một phần tử được chọn ngẫu nhiên từ ``range(start, stop, step)``.

   Hàm này gần tương đương với ``choice(range(start, stop, step))`` nhưng hỗ trợ các phạm vi lớn tùy ý và được tối ưu hóa cho những trường hợp phổ biến.

   Mẫu đối số vị trí khớp với hàm :func:`range`.

   Không nên sử dụng đối số từ khóa vì chúng có thể được diễn giải theo những cách không mong muốn. Ví dụ, ``randrange(start=100)`` được diễn giải là ``randrange(0, 100, 1)``.

   .. versionchanged:: 3.2
      :meth:`randrange` is more sophisticated about producing equally distributed
      các giá trị. Trước đây, hàm này sử dụng kiểu như ``int(random()*n)``, có thể tạo ra các phân phối hơi không đồng đều.

   .. versionchanged:: 3.12
      Không còn hỗ trợ tự động chuyển đổi các kiểu không phải số nguyên. Những lệnh gọi như ``randrange(10.0)`` và ``randrange(Fraction(10, 1))`` hiện sẽ phát sinh :exc:`TypeError`.

.. function:: randint(a, b)

   Trả về một số nguyên ngẫu nhiên *N* sao cho ``a <= N <= b``. Bí danh của ``randrange(a, b+1)``.

.. function:: getrandbits(k)

   Trả về một số nguyên Python không âm với *k* bit ngẫu nhiên. Phương thức này được cung cấp cùng với bộ sinh Mersenne Twister; một số bộ sinh khác cũng có thể cung cấp phương thức này như một phần tùy chọn của API. Khi khả dụng,
   :meth:`getrandbits` cho phép :meth:`randrange` xử lý các phạm vi lớn tùy ý.

   .. versionchanged:: 3.9
      Phương thức này hiện chấp nhận giá trị 0 cho *k*.


Các hàm cho sequence
--------------------

.. function:: choice(seq)

   Trả về một phần tử ngẫu nhiên từ sequence không rỗng *seq*. Nếu *seq* rỗng, sẽ phát sinh :exc:`IndexError`.

.. function:: choices(population, weights=None, *, cum_weights=None, k=1)

   Trả về một danh sách có kích thước *k*, gồm các phần tử được chọn từ *population* có lặp lại. Nếu *population* rỗng, sẽ phát sinh :exc:`IndexError`.

   Nếu chỉ định một sequence *weights*, các lựa chọn được thực hiện theo trọng số tương đối. Ngoài ra, nếu cung cấp một sequence *cum_weights*, các lựa chọn được thực hiện theo trọng số tích lũy (có thể được tính bằng :func:`itertools.accumulate`). Ví dụ, các trọng số tương đối ``[10, 5, 30, 5]`` tương đương với các trọng số tích lũy ``[10, 15, 45, 50]``. Bên trong, các trọng số tương đối được chuyển đổi thành trọng số tích lũy trước khi thực hiện lựa chọn, vì vậy việc cung cấp trọng số tích lũy sẽ tiết kiệm công sức.

   Nếu không chỉ định *weights* và *cum_weights*, các lựa chọn được thực hiện với xác suất bằng nhau. Nếu cung cấp một sequence weights, sequence đó phải có cùng độ dài với sequence *population*. Việc chỉ định đồng thời :exc:`TypeError` và *weights* và *cum_weights* là :exc:`TypeError`.

   *weights* hoặc *cum_weights* có thể sử dụng bất kỳ kiểu số nào tương thích với các giá trị :class:`float` do :func:`random` trả về (bao gồm số nguyên, số thực và phân số nhưng không bao gồm số thập phân). Các trọng số được giả định là không âm và hữu hạn. Sẽ phát sinh :exc:`ValueError` nếu tất cả trọng số đều bằng 0.

   Với một seed nhất định, hàm :func:`choices` sử dụng trọng số bằng nhau thường tạo ra một chuỗi khác với các lần gọi lặp lại đến
   :func:`choice`.  Thuật toán được :func:`choices` sử dụng dùng phép tính dấu phẩy động để đảm bảo tính nhất quán nội bộ và tốc độ.  Thuật toán được :func:`choice` sử dụng mặc định dùng phép tính số nguyên cùng các lần chọn lặp lại để tránh những sai lệch nhỏ do lỗi làm tròn.

   .. versionadded:: 3.6

   .. versionchanged:: 3.9
      Phát sinh :exc:`ValueError` nếu tất cả trọng số đều bằng không.


.. function:: shuffle(x)

   Xáo trộn dãy *x* tại chỗ.

   Để xáo trộn một dãy bất biến và trả về một danh sách mới đã được xáo trộn, hãy sử dụng ``sample(x, k=len(x))`` thay thế.

   Lưu ý rằng ngay cả với ``len(x)`` nhỏ, tổng số hoán vị của *x* có thể nhanh chóng lớn hơn chu kỳ của hầu hết các bộ sinh số ngẫu nhiên. Điều này có nghĩa là hầu hết các hoán vị của một dãy dài không bao giờ có thể được tạo ra.  Ví dụ, một dãy có độ dài 2080 là dãy lớn nhất có thể nằm trong chu kỳ của bộ sinh số ngẫu nhiên Mersenne Twister.

   .. versionchanged:: 3.11
      Đã loại bỏ tham số tùy chọn *random*.


.. function:: sample(population, k, *, counts=None)

   Trả về một danh sách có độ dài *k* gồm các phần tử duy nhất được chọn từ chuỗi population. Dùng để lấy mẫu ngẫu nhiên không hoàn lại.

   Trả về một danh sách mới chứa các phần tử từ population mà không làm thay đổi population ban đầu. Danh sách kết quả được sắp xếp theo thứ tự được chọn, vì vậy mọi lát con đều cũng là các mẫu ngẫu nhiên hợp lệ. Điều này cho phép chia những người trúng xổ số (mẫu) thành người thắng giải nhất và người thắng giải nhì (các lát con).

   Các phần tử của population không cần phải là :term:`hashable` hoặc duy nhất. Nếu population chứa các phần tử lặp lại, thì mỗi lần xuất hiện đều có thể được chọn vào mẫu.

   Các phần tử lặp lại có thể được chỉ định từng phần tử một hoặc bằng tham số chỉ dành cho keyword tùy chọn *counts*. Ví dụ, ``sample(['red', 'blue'], counts=[4, 2], k=5)`` tương đương với ``sample(['red', 'red', 'red', 'red', 'blue', 'blue'], k=5)``.

   Để chọn một mẫu từ một khoảng số nguyên, hãy dùng một đối tượng :func:`range` làm đối số. Cách này đặc biệt nhanh và tiết kiệm bộ nhớ khi lấy mẫu từ một population lớn: ``sample(range(10000000), k=60)``.

   Nếu kích thước mẫu lớn hơn kích thước population, một :exc:`ValueError` sẽ được phát sinh.

   .. versionchanged:: 3.9
      Đã thêm tham số *counts*.

   .. versionchanged:: 3.11

      *population* phải là một sequence. Tính năng tự động chuyển set thành list không còn được hỗ trợ.

Các phân phối rời rạc
---------------------

Hàm sau đây tạo một phân phối rời rạc.

.. function:: binomialvariate(n=1, p=0.5)

   `Phân phối nhị thức <https://mathworld.wolfram.com/BinomialDistribution.html>`_. Trả về số lần thành công trong *n* phép thử độc lập, với xác suất thành công trong mỗi phép thử là *p*:

   Tương đương về mặt toán học với::

       sum(random() < p for i in range(n))

   Số phép thử *n* phải là một số nguyên không âm. Xác suất thành công *p* phải nằm trong khoảng ``0.0 <= p <= 1.0``. Kết quả là một số nguyên trong phạm vi ``0 <= X <= n``.

   .. versionadded:: 3.12


.. _real-valued-distributions:

Các phân phối giá trị thực
--------------------------

Các hàm sau đây tạo ra những phân phối cụ thể có giá trị thực. Tham số của hàm được đặt tên theo các biến tương ứng trong phương trình của phân phối, như cách thường dùng trong toán học; bạn có thể tìm thấy hầu hết các phương trình này trong bất kỳ tài liệu thống kê nào.


.. function:: random()

   Trả về số dấu phẩy động ngẫu nhiên tiếp theo trong phạm vi ``0.0 <= X < 1.0``


.. function:: uniform(a, b)

   Trả về một số dấu phẩy động ngẫu nhiên *N* sao cho ``a <= N <= b`` với ``a <= b`` và ``b <= N <= a`` với ``b < a``.

   Giá trị điểm cuối ``b`` có thể được đưa vào hoặc không được đưa vào phạm vi, tùy thuộc vào việc làm tròn số dấu phẩy động trong biểu thức ``a + (b-a) * random()``.


.. function:: triangular(low, high, mode)

   Trả về một số dấu phẩy động ngẫu nhiên *N* sao cho ``low <= N <= high`` và có *mode* được chỉ định nằm giữa hai giới hạn đó. Hai giới hạn *low* và *high* mặc định lần lượt là 0 và 1. Đối số *mode* mặc định là điểm giữa hai giới hạn, tạo ra một phân phối đối xứng.


.. function:: betavariate(alpha, beta)

   Phân phối beta. Điều kiện đối với các tham số là ``alpha > 0`` và ``beta > 0``. Các giá trị trả về nằm trong khoảng từ 0 đến 1.


.. function:: expovariate(lambd = 1.0)

   Phân phối mũ. *lambd* là 1.0 chia cho giá trị trung bình mong muốn. Giá trị này phải khác không. (Tham số này lẽ ra được gọi là "lambda", nhưng đó là một từ dành riêng trong Python.) Các giá trị trả về nằm trong khoảng từ 0 đến dương vô cùng nếu *lambd* dương, và từ âm vô cùng đến 0 nếu *lambd* âm.

   .. versionchanged:: 3.12
      Đã thêm giá trị mặc định cho ``lambd``.


.. function:: gammavariate(alpha, beta)

   Phân phối gamma.  (*Không phải* hàm gamma!)  Các tham số hình dạng và tỷ lệ, *alpha* và *beta*, phải có giá trị dương. (Quy ước gọi hàm có thể khác nhau và một số nguồn định nghĩa 'beta' là nghịch đảo của tỷ lệ).

   Hàm phân phối xác suất là::

                 x ** (alpha - 1) * math.exp(-x / beta)
       pdf(x) =  --------------------------------------
                   math.gamma(alpha) * beta ** alpha


.. function:: gauss(mu=0.0, sigma=1.0)

   Phân phối chuẩn, còn được gọi là phân phối Gaussian. *mu* là giá trị trung bình và *sigma* là độ lệch chuẩn.  Hàm này nhanh hơn một chút so với hàm :func:`normalvariate` được định nghĩa bên dưới.

   Lưu ý về đa luồng:  Khi hai thread gọi hàm này đồng thời, chúng có thể nhận được cùng một giá trị trả về.  Có thể tránh điều này bằng ba cách.
   1) Để mỗi thread sử dụng một instance khác nhau của bộ sinh số ngẫu nhiên
   bộ sinh số. 2) Đặt khóa quanh tất cả các lời gọi. 3) Thay vào đó, hãy sử dụng hàm :func:`normalvariate` chậm hơn nhưng an toàn với luồng.

   .. versionchanged:: 3.11
      *mu* và *sigma* hiện có các đối số mặc định.


.. function:: lognormvariate(mu, sigma)

   Phân phối log-normal. Nếu lấy logarit tự nhiên của phân phối này, bạn sẽ nhận được một phân phối chuẩn với giá trị trung bình *mu* và độ lệch chuẩn *sigma*. *mu* có thể nhận bất kỳ giá trị nào, còn *sigma* phải lớn hơn 0.


.. function:: normalvariate(mu=0.0, sigma=1.0)

   Phân phối chuẩn. *mu* là giá trị trung bình, còn *sigma* là độ lệch chuẩn.

   .. versionchanged:: 3.11
      *mu* và *sigma* hiện có các đối số mặc định.


.. function:: vonmisesvariate(mu, kappa)

   *mu* là góc trung bình, được biểu diễn theo radian trong khoảng từ 0 đến 2\*\ *pi*, còn *kappa* là tham số nồng độ, phải lớn hơn hoặc bằng 0. Nếu *kappa* bằng 0, phân phối này trở thành một góc ngẫu nhiên phân bố đều trong khoảng từ 0 đến 2\*\ *pi*.


.. function:: paretovariate(alpha)

   Phân phối Pareto. *alpha* là tham số hình dạng.


.. function:: weibullvariate(alpha, beta)

   Phân phối Weibull. *alpha* là tham số tỷ lệ, còn *beta* là tham số hình dạng.


Bộ sinh thay thế
----------------

.. class:: Random([seed])

   Lớp triển khai bộ sinh số giả ngẫu nhiên mặc định được sử dụng bởi
   :mod:`!random` mô-đun.

   .. versionchanged:: 3.11
      Trước đây, *seed* có thể là bất kỳ đối tượng nào có thể băm được. Hiện tại, nó chỉ được giới hạn ở: ``None``, :class:`int`, :class:`float`, :class:`str`,
      :class:`bytes`, hoặc :class:`bytearray`.

   Các lớp con của :class:`!Random` nên ghi đè các phương thức sau nếu muốn sử dụng một bộ sinh cơ bản khác:

   .. method:: Random.seed(a=None, version=2)

      Ghi đè phương thức này trong các lớp con để tùy chỉnh hành vi :meth:`~random.seed` của các thực thể :class:`!Random`.

   .. method:: Random.getstate()

      Ghi đè phương thức này trong các lớp con để tùy chỉnh hành vi :meth:`~random.getstate` của các thể hiện :class:`!Random`.

   .. method:: Random.setstate(state)

      Ghi đè phương thức này trong các lớp con để tùy chỉnh hành vi :meth:`~random.setstate` của các thể hiện :class:`!Random`.

   .. method:: Random.random()

      Ghi đè phương thức này trong các lớp con để tùy chỉnh hành vi :meth:`~random.random` của các thể hiện :class:`!Random`.

   Ngoài ra, một lớp con generator tùy chỉnh cũng có thể cung cấp phương thức sau:

   .. method:: Random.getrandbits(k)

      Ghi đè phương thức này trong các lớp con để tùy chỉnh
      hành vi :meth:`~random.getrandbits` của các thể hiện :class:`!Random`.

   .. method:: Random.randbytes(n)

      Ghi đè phương thức này trong các lớp con để tùy chỉnh
      :meth:`~random.randbytes` hành vi của các instance :class:`!Random`.


.. class:: SystemRandom([seed])

   Lớp sử dụng hàm :func:`os.urandom` để tạo các số ngẫu nhiên từ những nguồn do hệ điều hành cung cấp. Không khả dụng trên tất cả các hệ thống. Không phụ thuộc vào trạng thái phần mềm, và các chuỗi không thể tái tạo. Do đó, phương thức :meth:`seed` không có tác dụng và bị bỏ qua. Các phương thức :meth:`getstate` và :meth:`setstate` sẽ ném ra
   :exc:`NotImplementedError` nếu được gọi.


Lưu ý về khả năng tái tạo
-------------------------

Đôi khi, việc có thể tái tạo các chuỗi do bộ tạo số giả ngẫu nhiên cung cấp rất hữu ích. Bằng cách sử dụng lại một giá trị seed, cùng một chuỗi sẽ có thể được tái tạo qua mỗi lần chạy, miễn là không có nhiều thread chạy đồng thời.

Hầu hết các thuật toán và hàm tạo seed của module random có thể thay đổi giữa các phiên bản Python, nhưng có hai khía cạnh được đảm bảo không thay đổi:

* Nếu một phương thức tạo seed mới được thêm vào, thì sẽ có một seeder tương thích ngược được cung cấp.

* Phương thức :meth:`~Random.random` của generator sẽ tiếp tục tạo ra cùng một chuỗi khi compatible seeder được cung cấp cùng một seed.

.. _random-examples:

Ví dụ
-----

Ví dụ cơ bản::

   >>> random()                          # Số thực ngẫu nhiên:  0.0 <= x < 1.0
   0.37444887175646646

   >>> uniform(2.5, 10.0)                # Số thực ngẫu nhiên:  2.5 <= x <= 10.0
   3.1800146073117523

   >>> expovariate(1 / 5)                # Khoảng thời gian giữa các lần đến, trung bình 5 giây
   5.148957571865031

   >>> randrange(10)                     # Số nguyên từ 0 đến 9, bao gồm cả hai đầu
   7

   >>> randrange(0, 101, 2)              # Số nguyên chẵn từ 0 đến 100, bao gồm cả hai đầu mút
   26

   >>> choice(['win', 'lose', 'draw'])   # Một phần tử ngẫu nhiên duy nhất từ một dãy
   'draw'

   >>> deck = 'ace two three four'.split()
   >>> shuffle(deck)                     # Xáo trộn một danh sách
   >>> deck
   ['four', 'two', 'ace', 'three']

   >>> sample([10, 20, 30, 40, 50], k=4) # Bốn mẫu không hoàn lại
   [40, 10, 50, 30]

Mô phỏng::

   >>> # Sáu lượt quay bánh xe roulette (lấy mẫu có trọng số và hoàn lại)
   >>> choices(['red', 'black', 'green'], [18, 18, 2], k=6)
   ['red', 'green', 'black', 'black', 'red', 'black']

   >>> # Chia 20 lá bài không hoàn lại từ một bộ bài
   >>> # trong 52 lá bài, và xác định tỷ lệ các lá bài
   >>> # có giá trị mười: mười, jack, queen hoặc king.
   >>> deal = sample(['tens', 'low cards'], counts=[16, 36], k=20)
   >>> deal.count('tens') / 20
   0.15

   >>> # Ước tính xác suất nhận được 5 hoặc nhiều hơn mặt ngửa sau 7 lần tung
   >>> # của một đồng xu thiên lệch, cho kết quả mặt ngửa 60% số lần.
   >>> sum(binomialvariate(n=7, p=0.6) >= 5 for i in range(10_000)) / 10_000
   0.4169

   >>> # Xác suất trung vị của 5 mẫu nằm trong hai tứ phân vị giữa
   >>> def trial():
   ...     return 2_500 <= sorted(choices(range(10_000), k=5))[2] < 7_500
   ...
   >>> sum(trial() for i in range(10_000)) / 10_000
   0.7958

Ví dụ về `bootstrap thống kê <https://en.wikipedia.org/wiki/Bootstrapping_(statistics)>`_ bằng cách lấy mẫu lại có hoàn lại để ước tính khoảng tin cậy cho trung bình của một mẫu::

   # https://www.thoughtco.com/example-of-bootstrapping-3126155
   from statistics import fmean as mean
   from random import choices

   data = [41, 50, 29, 37, 81, 30, 73, 63, 20, 35, 68, 22, 60, 31, 95]
   means = sorted(mean(choices(data, k=len(data))) for i in range(100))
   print(f'The sample mean of {mean(data):.1f} has a 90% confidence '
         f'interval from {means[5]:.1f} to {means[94]:.1f}')

Ví dụ về `kiểm định hoán vị bằng cách lấy mẫu lại <https://en.wikipedia.org/wiki/Resampling_(statistics)#Permutation_tests>`_ để xác định ý nghĩa thống kê hoặc `p-value <https://en.wikipedia.org/wiki/P-value>`_ của sự khác biệt quan sát được giữa tác động của một loại thuốc và giả dược::

    # Ví dụ trích từ "Statistics is Easy" của Dennis Shasha và Manda Wilson
    from statistics import fmean as mean
    from random import shuffle

    drug = [54, 73, 53, 70, 73, 68, 52, 65, 65]
    placebo = [54, 51, 58, 44, 55, 52, 42, 47, 58, 46]
    observed_diff = mean(drug) - mean(placebo)

    n = 10_000
    count = 0
    combined = drug + placebo
    for i in range(n):
        shuffle(combined)
        new_diff = mean(combined[:len(drug)]) - mean(combined[len(drug):])
        count += (new_diff >= observed_diff)

    print(f'{n} label reshufflings produced only {count} instances with a difference')
    print(f'at least as extreme as the observed difference of {observed_diff:.1f}.')
    print(f'The one-sided p-value of {count / n:.4f} leads us to reject the null')
    print(f'hypothesis that there is no difference between the drug and the placebo.')

Mô phỏng thời điểm đến và việc phục vụ cho một hàng đợi nhiều máy chủ::

    from heapq import heapify, heapreplace
    from random import expovariate, gauss
    from statistics import mean, quantiles

    average_arrival_interval = 5.6
    average_service_time = 15.0
    stdev_service_time = 3.5
    num_servers = 3

    waits = []
    arrival_time = 0.0
    servers = [0.0] * num_servers  # thời điểm mỗi máy chủ khả dụng trở lại
    heapify(servers)
    for i in range(1_000_000):
        arrival_time += expovariate(1.0 / average_arrival_interval)
        next_server_available = servers[0]
        wait = max(0.0, next_server_available - arrival_time)
        waits.append(wait)
        service_duration = max(0.0, gauss(average_service_time, stdev_service_time))
        service_completed = arrival_time + wait + service_duration
        heapreplace(servers, service_completed)

    print(f'Mean wait: {mean(waits):.1f}   Max wait: {max(waits):.1f}')
    print('Quartiles:', [round(q, 1) for q in quantiles(waits)])

.. seealso::

   `Statistics for Hackers <https://www.youtube.com/watch?v=Iq9DzN6mvYA>`_ một video hướng dẫn của `Jake Vanderplas <https://us.pycon.org/2016/speaker/profile/295/>`_ về phân tích thống kê chỉ sử dụng một vài khái niệm nền tảng, bao gồm mô phỏng, lấy mẫu, xáo trộn và cross-validation.

   `Economics Simulation <https://nbviewer.org/url/norvig.com/ipython/Economics.ipynb>`_ một mô phỏng thị trường của `Peter Norvig <https://norvig.com/bio.html>`_ cho thấy cách sử dụng hiệu quả nhiều công cụ và phân phối do module này cung cấp (gauss, uniform, sample, betavariate, choice, triangular và randrange).

   `A Concrete Introduction to Probability (using Python) <https://nbviewer.org/url/norvig.com/ipython/Probability.ipynb>`_ một hướng dẫn của `Peter Norvig <https://norvig.com/bio.html>`_ trình bày những kiến thức cơ bản về lý thuyết xác suất, cách viết mô phỏng và cách thực hiện phân tích dữ liệu bằng Python.


Công thức
---------

Các công thức này cho biết cách thực hiện hiệu quả việc chọn ngẫu nhiên từ các iterator tổ hợp trong mô-đun :mod:`itertools`:

.. testcode::

   import random

   def random_product(*iterables, repeat=1):
       "Random selection from itertools.product(*iterables, repeat=repeat)"
       pools = tuple(map(tuple, iterables)) * repeat
       return tuple(map(random.choice, pools))

   def random_permutation(iterable, r=None):
       "Random selection from itertools.permutations(iterable, r)"
       pool = tuple(iterable)
       r = len(pool) if r is None else r
       return tuple(random.sample(pool, r))

   def random_combination(iterable, r):
       "Random selection from itertools.combinations(iterable, r)"
       pool = tuple(iterable)
       n = len(pool)
       indices = sorted(random.sample(range(n), r))
       return tuple(pool[i] for i in indices)

   def random_combination_with_replacement(iterable, r):
       "Choose r elements with replacement.  Order the result to match the iterable."
       # Kết quả sẽ là set(itertools.combinations_with_replacement(iterable, r)).
       pool = tuple(iterable)
       n = len(pool)
       indices = sorted(random.choices(range(n), k=r))
       return tuple(pool[i] for i in indices)

   def random_derangement(iterable):
       "Choose a permutation where no element stays in its original position."
       seq = tuple(iterable)
       if len(seq) < 2:
           if not seq:
               return ()
           raise IndexError('No derangments to choose from')
       perm = list(range(len(seq)))
       start = tuple(perm)
       while True:
           random.shuffle(perm)
           if all(p != q for p, q in zip(start, perm)):
               return tuple([seq[i] for i in perm])

.. doctest::
    :hide:

    >>> import random


    >>> random.seed(8675309)
    >>> random_product('ABCDEFG', repeat=5)
    ('D', 'B', 'E', 'F', 'E')


    >>> random.seed(8675309)
    >>> random_permutation('ABCDEFG')
    ('D', 'B', 'E', 'C', 'G', 'A', 'F')
    >>> random_permutation('ABCDEFG', 5)
    ('A', 'G', 'D', 'C', 'B')


    >>> random.seed(8675309)
    >>> random_combination('ABCDEFG', 7)
    ('A', 'B', 'C', 'D', 'E', 'F', 'G')
    >>> random_combination('ABCDEFG', 6)
    ('A', 'B', 'C', 'D', 'F', 'G')
    >>> random_combination('ABCDEFG', 5)
    ('A', 'B', 'C', 'E', 'F')
    >>> random_combination('ABCDEFG', 4)
    ('B', 'C', 'D', 'G')
    >>> random_combination('ABCDEFG', 3)
    ('B', 'E', 'G')
    >>> random_combination('ABCDEFG', 2)
    ('E', 'G')
    >>> random_combination('ABCDEFG', 1)
    ('C',)
    >>> random_combination('ABCDEFG', 0)
    ()


    >>> random.seed(8675309)
    >>> random_combination_with_replacement('ABCDEFG', 7)
    ('B', 'C', 'D', 'E', 'E', 'E', 'G')
    >>> random_combination_with_replacement('ABCDEFG', 3)
    ('A', 'B', 'E')
    >>> random_combination_with_replacement('ABCDEFG', 2)
    ('A', 'G')
    >>> random_combination_with_replacement('ABCDEFG', 1)
    ('E',)
    >>> random_combination_with_replacement('ABCDEFG', 0)
    ()


    >>> random.seed(8675309)
    >>> random_derangement('')
    ()
    >>> random_derangement('A')
    Traceback (most recent call last):
    ...
    IndexError: No derangments to choose from
    >>> random_derangement('AB')
    ('B', 'A')
    >>> random_derangement('ABC')
    ('C', 'A', 'B')
    >>> random_derangement('ABCD')
    ('B', 'A', 'D', 'C')
    >>> random_derangement('ABCDE')
    ('B', 'C', 'A', 'E', 'D')
    >>> # Các đầu vào giống hệt nhau được xem là khác nhau
    >>> identical = 20
    >>> random_derangement((10, identical, 30, identical))
    (20, 30, 10, 20)


:func:`.random` mặc định trả về các bội số của 2⁻⁵³ trong phạm vi *0.0 ≤ x < 1.0*. Tất cả các số như vậy cách đều nhau và có thể được biểu diễn chính xác dưới dạng số thực Python. Tuy nhiên, nhiều số thực có thể biểu diễn khác trong khoảng đó lại không thể được chọn. Ví dụ: ``0.05954861408025609`` không phải là bội số nguyên của 2⁻⁵³.

Công thức sau đây sử dụng một cách tiếp cận khác. Mọi số thực trong khoảng đều có thể được chọn. Phần định trị được lấy từ một phân phối đều của các số nguyên trong phạm vi *2⁵² ≤ mantissa < 2⁵³*. Số mũ được lấy từ một phân phối hình học, trong đó các số mũ nhỏ hơn *-53* xuất hiện với tần suất bằng một nửa so với số mũ lớn hơn kế tiếp.

::

    from random import Random
    from math import ldexp

    class FullRandom(Random):

        def random(self):
            mantissa = 0x10_0000_0000_0000 | self.getrandbits(52)
            exponent = -53
            x = 0
            while not x:
                x = self.getrandbits(32)
                exponent += x.bit_length() - 32
            return ldexp(mantissa, exponent)

Tất cả các :ref:`phân phối giá trị thực <real-valued-distributions>` trong lớp sẽ sử dụng phương thức mới::

    >>> fr = FullRandom()
    >>> fr.random()
    0.05954861408025609
    >>> fr.expovariate(0.25)
    8.87925541791544

Về mặt khái niệm, công thức này tương đương với một thuật toán chọn từ tất cả các bội số của 2⁻¹⁰⁷⁴ trong phạm vi *0.0 ≤ x < 1.0*. Tất cả các số như vậy cách đều nhau, nhưng phần lớn phải được làm tròn xuống số thực Python có thể biểu diễn gần nhất. (Giá trị 2⁻¹⁰⁷⁴ là số thực chưa chuẩn hóa dương nhỏ nhất và bằng ``math.ulp(0.0)``.)


.. seealso::

   `Tạo các giá trị dấu phẩy động giả ngẫu nhiên <https://allendowney.com/research/rand/downey07randfloat.pdf>`_, một bài viết của Allen B. Downey mô tả các cách tạo ra các giá trị dấu phẩy động chi tiết hơn so với các giá trị thường được tạo bởi :func:`.random`.

.. _random-cli:

Cách sử dụng dòng lệnh
----------------------

.. versionadded:: 3.13

Có thể thực thi mô-đun :mod:`!random` từ dòng lệnh.

.. code-block:: sh

   python -m random [-h] [-c CHOICE [CHOICE ...] | -i N | -f N] [input ...]

Các tùy chọn sau được chấp nhận:

.. program:: random

.. option:: -h, --help

   Hiển thị thông báo trợ giúp và thoát.

.. option:: -c CHOICE [CHOICE ...]
            --choice CHOICE [CHOICE ...]

   In ra một lựa chọn ngẫu nhiên bằng :meth:`choice`.

.. option:: -i <N>
            --integer <N>

   In ra một số nguyên ngẫu nhiên từ 1 đến N, bao gồm cả hai đầu mút, bằng cách sử dụng :meth:`randint`.

.. option:: -f <N>
            --float <N>

   In ra một số dấu phẩy động ngẫu nhiên từ 0 đến N, bao gồm cả hai đầu mút, bằng cách sử dụng :meth:`uniform`.

Nếu không cung cấp tùy chọn nào, đầu ra sẽ phụ thuộc vào đầu vào:

* Chuỗi hoặc nhiều giá trị: giống như :option:`--choice`.
* Số nguyên: giống như :option:`--integer`.
* Float: giống như :option:`--float`.

.. _random-cli-example:

Ví dụ dòng lệnh
---------------

Dưới đây là một số ví dụ về giao diện dòng lệnh của lệnh :mod:`!random`:

.. code-block:: console

   $ # Choose one at random
   $ python -m random egg bacon sausage spam "Lobster Thermidor aux crevettes with a Mornay sauce"
   Lobster Thermidor aux crevettes with a Mornay sauce

   $ # Random integer
   $ python -m random 6
   6

   $ # Random floating-point number
   $ python -m random 1.8
   1.7080016272295635

   $ # With explicit arguments
   $ python  -m random --choice egg bacon sausage spam "Lobster Thermidor aux crevettes with a Mornay sauce"
   egg

   $ python -m random --integer 6
   3

   $ python -m random --float 1.8
   1.5666339105010318

   $ python -m random --integer 6
   5

   $ python -m random --float 6
   3.1942323316565915

.. _`Complementary-Multiply-with-Carry recipe`: https://code.activestate.com/recipes/576707-long-period-random-number-generator/
.. _`Binomial distribution`: https://mathworld.wolfram.com/BinomialDistribution.html
.. _`statistical bootstrapping`: https://en.wikipedia.org/wiki/Bootstrapping_(statistics)
.. _`resampling permutation test`: https://en.wikipedia.org/wiki/Resampling_(statistics)#Permutation_tests
.. _`p-value`: https://en.wikipedia.org/wiki/P-value
.. _`Statistics for Hackers`: https://www.youtube.com/watch?v=Iq9DzN6mvYA
.. _`Jake Vanderplas`: https://us.pycon.org/2016/speaker/profile/295/
.. _`Economics Simulation`: https://nbviewer.org/url/norvig.com/ipython/Economics.ipynb
.. _`Peter Norvig`: https://norvig.com/bio.html
.. _`A Concrete Introduction to Probability (using Python)`: https://nbviewer.org/url/norvig.com/ipython/Probability.ipynb
.. _`Generating Pseudo-random Floating-Point Values`: https://allendowney.com/research/rand/downey07randfloat.pdf
