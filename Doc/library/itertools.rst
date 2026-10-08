:mod:`!itertools` --- Các hàm tạo iterator để lặp hiệu quả
==========================================================

.. module:: itertools
   :synopsis: Các hàm tạo iterator để lặp hiệu quả.

.. moduleauthor:: Raymond Hettinger <python@rcn.com>
.. sectionauthor:: Raymond Hettinger <python@rcn.com>

.. testsetup::

   from itertools import *
   import collections
   import math
   import operator
   import random

--------------

Module này triển khai một số :term:`iterator` khối xây dựng lấy cảm hứng từ các cấu trúc trong APL, Haskell và SML. Mỗi khối được chuyển thành dạng phù hợp với Python.

Module này chuẩn hóa một tập hợp cốt lõi gồm các công cụ nhanh, tiết kiệm bộ nhớ, hữu ích khi sử dụng riêng lẻ hoặc kết hợp với nhau. Khi kết hợp, chúng tạo thành một "đại số iterator" giúp xây dựng các công cụ chuyên biệt một cách ngắn gọn và hiệu quả chỉ bằng Python thuần.

Ví dụ, SML cung cấp một công cụ lập bảng: ``tabulate(f)`` tạo ra một dãy ``f(0), f(1), ...``. Trong Python, có thể đạt được hiệu ứng tương tự bằng cách kết hợp :func:`map` và :func:`count` để tạo thành ``map(f, count())``.

**Các iterator tổng quát:**

+-----------------------------+-----------------------------+--------------------------------------------------------+------------------------------------------------------------+
| Iterator                    | Đối số                      | Kết quả                                                | Ví dụ                                                      |
+=============================+=============================+========================================================+============================================================+
| :func:`accumulate`          | p [,func]                   | p0, p0+p1, p0+p1+p2, ...                               | ``accumulate([1,2,3,4,5]) → 1 3 6 10 15``                  |
+-----------------------------+-----------------------------+--------------------------------------------------------+------------------------------------------------------------+
| :func:`batched`             | p, n                        | (p0, p1, ..., p_n-1), ...                              | ``batched('ABCDEFG', n=3) → ABC DEF G``                    |
+-----------------------------+-----------------------------+--------------------------------------------------------+------------------------------------------------------------+
| :func:`chain`               | p, q, ...                   | p0, p1, ... plast, q0, q1, ...                         | ``chain('ABC', 'DEF') → A B C D E F``                      |
+-----------------------------+-----------------------------+--------------------------------------------------------+------------------------------------------------------------+
| :func:`chain.from_iterable` | iterable                    | p0, p1, ... plast, q0, q1, ...                         | ``chain.from_iterable(['ABC', 'DEF']) → A B C D E F``      |
+-----------------------------+-----------------------------+--------------------------------------------------------+------------------------------------------------------------+
| :func:`compress`            | data, selectors             | (d[0] if s[0]), (d[1] if s[1]), ...                    | ``compress('ABCDEF', [1,0,1,0,1,1]) → A C E F``            |
+-----------------------------+-----------------------------+--------------------------------------------------------+------------------------------------------------------------+
| :func:`count`               | [start[, step]]             | start, start+step, start+2*step, ...                   | ``count(10) → 10 11 12 13 14 ...``                         |
+-----------------------------+-----------------------------+--------------------------------------------------------+------------------------------------------------------------+
| :func:`cycle`               | p                           | p0, p1, ... plast, p0, p1, ...                         | ``cycle('ABCD') → A B C D A B C D ...``                    |
+-----------------------------+-----------------------------+--------------------------------------------------------+------------------------------------------------------------+
| :func:`dropwhile`           | predicate, seq              | seq[n], seq[n+1], bắt đầu khi predicate không thỏa mãn | ``dropwhile(lambda x: x<5, [1,4,6,3,8]) → 6 3 8``          |
+-----------------------------+-----------------------------+--------------------------------------------------------+------------------------------------------------------------+
| :func:`filterfalse`         | predicate, seq              | các phần tử của seq mà predicate(elem) không thỏa mãn  | ``filterfalse(lambda x: x<5, [1,4,6,3,8]) → 6 8``          |
+-----------------------------+-----------------------------+--------------------------------------------------------+------------------------------------------------------------+
| :func:`groupby`             | iterable[, key]             | các sub-iterator được nhóm theo giá trị của key(v)     | ``groupby(['A','B','DEF'], len) → (1, A B) (3, DEF)``      |
+-----------------------------+-----------------------------+--------------------------------------------------------+------------------------------------------------------------+
| :func:`islice`              | seq, [start,] stop [, step] | các phần tử từ seq[start:stop:step]                    | ``islice('ABCDEFG', 2, None) → C D E F G``                 |
+-----------------------------+-----------------------------+--------------------------------------------------------+------------------------------------------------------------+
| :func:`pairwise`            | iterable                    | (p[0], p[1]), (p[1], p[2])                             | ``pairwise('ABCDEFG') → AB BC CD DE EF FG``                |
+-----------------------------+-----------------------------+--------------------------------------------------------+------------------------------------------------------------+
| :func:`repeat`              | elem [,n]                   | elem, elem, elem, ... vô hạn hoặc tối đa n lần         | ``repeat(10, 3) → 10 10 10``                               |
+-----------------------------+-----------------------------+--------------------------------------------------------+------------------------------------------------------------+
| :func:`starmap`             | func, seq                   | func(\*seq[0]), func(\*seq[1]), ...                    | ``starmap(pow, [(2,5), (3,2), (10,3)]) → 32 9 1000``       |
+-----------------------------+-----------------------------+--------------------------------------------------------+------------------------------------------------------------+
| :func:`takewhile`           | predicate, seq              | seq[0], seq[1], cho đến khi predicate không còn đúng   | ``takewhile(lambda x: x<5, [1,4,6,3,8]) → 1 4``            |
+-----------------------------+-----------------------------+--------------------------------------------------------+------------------------------------------------------------+
| :func:`tee`                 | it, n                       | it1, it2, ... itn  chia một iterator thành n iterator  | ``tee('ABC', 2) → A B C, A B C``                           |
+-----------------------------+-----------------------------+--------------------------------------------------------+------------------------------------------------------------+
| :func:`zip_longest`         | p, q, ...                   | (p[0], q[0]), (p[1], q[1]), ...                        | ``zip_longest('ABCD', 'xy', fillvalue='-') → Ax By C- D-`` |
+-----------------------------+-----------------------------+--------------------------------------------------------+------------------------------------------------------------+

**Các iterator tổ hợp:**

+---------------------------------------+----------------------+------------------------------------------------------------------+
| Iterator                              | Đối số               | Kết quả                                                          |
+=======================================+======================+==================================================================+
| :func:`product`                       | p, q, ... [repeat=1] | tích Descartes, tương đương với một nested for-loop              |
+---------------------------------------+----------------------+------------------------------------------------------------------+
| :func:`permutations`                  | p[, r]               | các tuple có độ dài r, mọi thứ tự có thể, không lặp phần tử      |
+---------------------------------------+----------------------+------------------------------------------------------------------+
| :func:`combinations`                  | p, r                 | các tuple có độ dài r, theo thứ tự đã sắp xếp, không lặp phần tử |
+---------------------------------------+----------------------+------------------------------------------------------------------+
| :func:`combinations_with_replacement` | p, r                 | các tuple có độ dài r, theo thứ tự đã sắp xếp, có lặp phần tử    |
+---------------------------------------+----------------------+------------------------------------------------------------------+

+----------------------------------------------+-----------------------------------------------------+
| Ví dụ                                        | Kết quả                                             |
+==============================================+=====================================================+
| ``product('ABCD', repeat=2)``                | ``AA AB AC AD BA BB BC BD CA CB CC CD DA DB DC DD`` |
+----------------------------------------------+-----------------------------------------------------+
| ``permutations('ABCD', 2)``                  | ``AB AC AD BA BC BD CA CB CD DA DB DC``             |
+----------------------------------------------+-----------------------------------------------------+
| ``combinations('ABCD', 2)``                  | ``AB AC AD BC BD CD``                               |
+----------------------------------------------+-----------------------------------------------------+
| ``combinations_with_replacement('ABCD', 2)`` | ``AA AB AC AD BB BC BD CC CD DD``                   |
+----------------------------------------------+-----------------------------------------------------+


.. _itertools-functions:

Các hàm Itertool
----------------

Các hàm sau đều tạo và trả về iterator. Một số hàm cung cấp các stream có độ dài vô hạn, vì vậy chỉ nên truy cập chúng bằng các hàm hoặc vòng lặp có khả năng cắt ngắn stream.


.. function:: accumulate(iterable[, function, *, initial=None])

    Tạo một iterator trả về các tổng tích lũy hoặc các kết quả tích lũy từ những hàm nhị phân khác.

    *Hàm* mặc định thực hiện phép cộng. *Hàm* phải chấp nhận hai đối số: tổng đã tích lũy và một giá trị từ *iterable*.

    Nếu cung cấp một giá trị *initial*, quá trình tích lũy sẽ bắt đầu bằng giá trị đó và đầu ra sẽ có nhiều hơn iterable đầu vào một phần tử.

    Tương đương về cơ bản với::

        def accumulate(iterable, function=operator.add, *, initial=None):
            'Return running totals'
            # accumulate([1,2,3,4,5]) → 1 3 6 10 15
            # accumulate([1,2,3,4,5], initial=100) → 100 101 103 106 110 115
            # accumulate([1,2,3,4,5], operator.mul) → 1 2 6 24 120

            iterator = iter(iterable)
            total = initial
            if initial is None:
                try:
                    total = next(iterator)
                except StopIteration:
                    return

            yield total
            for element in iterator:
                total = function(total, element)
                yield total

    Để tính giá trị nhỏ nhất lũy tiến, hãy đặt *hàm* thành :func:`min`. Để tính giá trị lớn nhất lũy tiến, hãy đặt *hàm* thành :func:`max`. Hoặc để tính tích lũy tiến, hãy đặt *hàm* thành :func:`operator.mul`. Để xây dựng `bảng khấu hao <https://www.ramseysolutions.com/real-estate/amortization-schedule>`_, hãy cộng dồn tiền lãi và áp dụng các khoản thanh toán:

    .. doctest::

      >>> data = [3, 4, 6, 2, 1, 9, 0, 7, 5, 8]
      >>> list(accumulate(data, max))              # giá trị lớn nhất lũy tiến
      [3, 4, 6, 6, 6, 9, 9, 9, 9, 9]
      >>> list(accumulate(data, operator.mul))     # tích lũy tiến
      [3, 12, 72, 144, 144, 1296, 0, 0, 0, 0]

      # Tính lịch trả khoản vay 5% trị giá 1000 với 10 khoản thanh toán hằng năm, mỗi khoản 90
      >>> update = lambda balance, payment: round(balance * 1.05) - payment
      >>> list(accumulate(repeat(90, 10), update, initial=1_000))
      [1000, 960, 918, 874, 828, 779, 728, 674, 618, 559, 497]

    Xem :func:`functools.reduce` để biết một hàm tương tự chỉ trả về giá trị tích lũy cuối cùng.

    .. versionadded:: 3.2

    .. versionchanged:: 3.3
       Đã thêm tham số *function* tùy chọn.

    .. versionchanged:: 3.8
       Đã thêm tham số *initial* tùy chọn.


.. function:: batched(iterable, n, *, strict=False)

   Gộp dữ liệu theo lô từ *iterable* thành các tuple có độ dài *n*. Lô cuối cùng có thể ngắn hơn *n*.

   Nếu *strict* là true, sẽ phát sinh một :exc:`ValueError` nếu lô cuối cùng ngắn hơn *n*.

   Lặp qua iterable đầu vào và tích lũy dữ liệu thành các tuple có kích thước *n*. Iterable đầu vào được tiêu thụ theo kiểu lazy, vừa đủ để lấp đầy một lô. Kết quả được yield ngay khi lô đầy hoặc khi iterable đầu vào đã :term:`exhausted`:

   .. doctest::

      >>> flattened_data = ['roses', 'red', 'violets', 'blue', 'sugar', 'sweet']
      >>> unflattened = list(batched(flattened_data, 2))
      >>> unflattened
      [('roses', 'red'), ('violets', 'blue'), ('sugar', 'sweet')]

   Tương đương về cơ bản với::

      def batched(iterable, n, *, strict=False):
          # batched('ABCDEFG', 3) → ABC DEF G
          if n < 1:
              raise ValueError('n must be at least one')
          iterator = iter(iterable)
          while batch := tuple(islice(iterator, n)):
              if strict and len(batch) != n:
                  raise ValueError('batched(): incomplete batch')
              yield batch

   .. versionadded:: 3.12

   .. versionchanged:: 3.13
      Đã thêm tùy chọn *strict*.


.. function:: chain(*iterables)

   Tạo một iterator trả về các phần tử từ iterable đầu tiên cho đến khi nó :term:`exhausted`, sau đó chuyển sang iterable tiếp theo cho đến khi tất cả các iterable đều cạn kiệt. Cách này kết hợp nhiều nguồn dữ liệu thành một iterator duy nhất. Về cơ bản tương đương với::

      def chain(*iterables):
          # chain('ABC', 'DEF') → A B C D E F
          for iterable in iterables:
              yield from iterable


.. classmethod:: chain.from_iterable(iterable)

   Hàm khởi tạo thay thế cho :func:`chain`. Nhận các đầu vào được nối từ một đối số iterable duy nhất, đối số này được đánh giá một cách lười biếng. Về cơ bản tương đương với::

      def from_iterable(iterables):
          # chain.from_iterable(['ABC', 'DEF']) → A B C D E F
          for iterable in iterables:
              yield from iterable


.. function:: combinations(iterable, r)

   Trả về các dãy con có độ dài *r* của các phần tử từ *iterable* đầu vào.

   Đầu ra là một dãy con của :func:`product`, chỉ giữ lại các mục là dãy con của *iterable*. Độ dài của đầu ra được xác định bởi :func:`math.comb`, tính ``n! / r! / (n - r)!`` khi ``0 ≤ r ≤ n`` hoặc bằng không khi ``r > n``.

   Các tuple tổ hợp được tạo theo thứ tự từ điển dựa trên thứ tự của *iterable* đầu vào. Nếu *iterable* đầu vào được sắp xếp, các tuple đầu ra sẽ được tạo theo thứ tự đã sắp xếp.

   Các phần tử được xem là duy nhất dựa trên vị trí của chúng, không dựa trên giá trị. Nếu các phần tử đầu vào là duy nhất, sẽ không có giá trị lặp lại trong mỗi tổ hợp.

   Tương đương về cơ bản với::

        def combinations(iterable, r):
            # combinations('ABCD', 2) → AB AC AD BC BD CD
            # combinations(range(4), 3) → 012 013 023 123

            pool = tuple(iterable)
            n = len(pool)
            if r > n:
                return
            indices = list(range(r))

            yield tuple(pool[i] for i in indices)
            while True:
                for i in reversed(range(r)):
                    if indices[i] != i + n - r:
                        break
                else:
                    return
                indices[i] += 1
                for j in range(i+1, r):
                    indices[j] = indices[j-1] + 1
                yield tuple(pool[i] for i in indices)


.. function:: combinations_with_replacement(iterable, r)

   Trả về các subsequence có độ dài *r* gồm các phần tử từ *iterable*, cho phép lặp lại từng phần tử nhiều hơn một lần.

   Đầu ra là một subsequence của :func:`product`, chỉ giữ lại các mục là subsequence (có thể chứa các phần tử lặp lại) của *iterable*. Số lượng subsequence được trả về là ``(n + r - 1)! / r! / (n - 1)!`` khi ``n > 0``.

   Các tuple tổ hợp được phát ra theo thứ tự từ điển dựa trên thứ tự của *iterable*. Nếu *iterable* đầu vào đã được sắp xếp, các tuple đầu ra cũng sẽ được tạo theo thứ tự đã sắp xếp.

   Các phần tử được xem là duy nhất dựa trên vị trí của chúng, không phải dựa trên giá trị. Nếu các phần tử đầu vào là duy nhất, các tổ hợp được tạo cũng sẽ là duy nhất.

   Tương đương về cơ bản với::

        def combinations_with_replacement(iterable, r):
            # combinations_with_replacement('ABC', 2) → AA AB AC BB BC CC

            pool = tuple(iterable)
            n = len(pool)
            if not n and r:
                return
            indices = [0] * r

            yield tuple(pool[i] for i in indices)
            while True:
                for i in reversed(range(r)):
                    if indices[i] != n - 1:
                        break
                else:
                    return
                indices[i:] = [indices[i] + 1] * (r - i)
                yield tuple(pool[i] for i in indices)

   .. versionadded:: 3.1


.. function:: compress(data, selectors)

   Tạo một iterator trả về các phần tử từ *data* mà phần tử tương ứng trong *selectors* là true. Dừng khi một trong hai iterable *data* hoặc *selectors* đã :term:`exhausted`. Tương đương gần đúng với::

       def compress(data, selectors):
           # compress('ABCDEF', [1,0,1,0,1,1]) → A C E F
           return (datum for datum, selector in zip(data, selectors) if selector)

   .. versionadded:: 3.1


.. function:: count(start=0, step=1)

   Tạo một iterator trả về các giá trị cách đều nhau, bắt đầu với *start*. Có thể dùng với :func:`map` để tạo các điểm dữ liệu liên tiếp hoặc với :func:`zip` để thêm số thứ tự. Gần tương đương với::

      def count(start=0, step=1):
          # count(10) → 10 11 12 13 14 ...
          # count(2.5, 0.5) → 2.5 3.0 3.5 ...
          n = start
          while True:
              yield n
              n += step

   Khi đếm bằng số dấu phẩy động, đôi khi có thể đạt độ chính xác cao hơn bằng cách thay thế bằng mã nhân, chẳng hạn như: ``(start + step * i for i in count())``.

   .. versionchanged:: 3.1
      Đã thêm đối số *step* và cho phép các đối số không nguyên.


.. function:: cycle(iterable)

   Tạo một iterator trả về các phần tử từ *iterable* và lưu một bản sao của từng phần tử. Khi iterable là :term:`exhausted`, trả về các phần tử từ bản sao đã lưu. Lặp lại vô hạn. Gần tương đương với::

      def cycle(iterable):
          # cycle('ABCD') → A B C D A B C D A B C D ...

          saved = []
          for element in iterable:
              yield element
              saved.append(element)

          while saved:
              for element in saved:
                  yield element

   itertool này có thể yêu cầu lượng bộ nhớ phụ đáng kể (tùy thuộc vào độ dài của iterable).


.. function:: dropwhile(predicate, iterable)

   Tạo một iterator loại bỏ các phần tử khỏi *iterable* trong khi *predicate* là true, sau đó trả về mọi phần tử. Gần tương đương với::

      def dropwhile(predicate, iterable):
          # dropwhile(lambda x: x<5, [1,4,6,3,8]) → 6 3 8

          iterator = iter(iterable)
          for x in iterator:
              if not predicate(x):
                  yield x
                  break

          for x in iterator:
              yield x

   Lưu ý rằng hàm này không tạo ra *bất kỳ* kết quả nào cho đến khi predicate lần đầu trở thành false, vì vậy itertool này có thể mất nhiều thời gian khởi động.


.. function:: filterfalse(predicate, iterable)

   Tạo một iterator lọc các phần tử từ *iterable*, chỉ trả về những phần tử mà *predicate* trả về giá trị false. Nếu *predicate* là ``None``, trả về các phần tử có giá trị false. Gần tương đương với::

      def filterfalse(predicate, iterable):
          # filterfalse(lambda x: x<5, [1,4,6,3,8]) → 6 8

          if predicate is None:
              predicate = bool

          for x in iterable:
              if not predicate(x):
                  yield x


.. function:: groupby(iterable, key=None)

   Tạo một iterator trả về các key và group liên tiếp từ *iterable*. *key* là một hàm tính giá trị key cho từng phần tử. Nếu không được chỉ định hoặc là ``None``, *key* mặc định là một hàm identity và trả về nguyên vẹn phần tử. Nhìn chung, iterable cần được sắp xếp theo cùng một hàm key từ trước.

   Hoạt động của :func:`groupby` tương tự như ``uniq`` filter trong Unix. Nó tạo ra một điểm ngắt hoặc group mới mỗi khi giá trị của hàm key thay đổi (đó là lý do thường cần sắp xếp dữ liệu bằng cùng một hàm key). Hành vi này khác với GROUP BY của SQL, vốn tổng hợp các phần tử giống nhau bất kể thứ tự đầu vào của chúng.

   Group được trả về bản thân nó là một iterator dùng chung iterable nền với :func:`groupby`. Vì source được dùng chung, khi đối tượng :func:`groupby` được tiến lên, group trước đó sẽ không còn hiển thị. Vì vậy, nếu cần dùng dữ liệu đó sau này, bạn nên lưu nó dưới dạng list::

      groups = []
      uniquekeys = []
      data = sorted(data, key=keyfunc)
      for k, g in groupby(data, keyfunc):
          groups.append(list(g))      # Lưu group iterator dưới dạng list
          uniquekeys.append(k)

   :func:`groupby` gần tương đương với::

      def groupby(iterable, key=None):
          # [k for k, g in groupby('AAAABBBCCDAABBB')] → A B C D A B
          # [list(g) for k, g in groupby('AAAABBBCCD')] → AAAA BBB CC D

          keyfunc = (lambda x: x) if key is None else key
          iterator = iter(iterable)
          exhausted = False

          def _grouper(target_key):
              nonlocal curr_value, curr_key, exhausted
              yield curr_value
              for curr_value in iterator:
                  curr_key = keyfunc(curr_value)
                  if curr_key != target_key:
                      return
                  yield curr_value
              exhausted = True

          try:
              curr_value = next(iterator)
          except StopIteration:
              return
          curr_key = keyfunc(curr_value)

          while not exhausted:
              target_key = curr_key
              curr_group = _grouper(target_key)
              yield curr_key, curr_group
              if curr_key == target_key:
                  for _ in curr_group:
                      pass


.. function:: islice(iterable, stop)
              islice(iterable, start, stop[, step])

   Tạo một iterator trả về các phần tử được chọn từ iterable. Hoạt động giống như cắt sequence nhưng không hỗ trợ các giá trị âm cho *start*, *stop* hoặc *step*.

   Nếu *start* bằng không hoặc ``None``, quá trình lặp bắt đầu từ số không. Nếu không, các phần tử từ iterable sẽ được bỏ qua cho đến khi đạt đến *start*.

   Nếu *stop* là ``None``, quá trình lặp tiếp tục cho đến khi đầu vào là
   :term:`exhausted`, nếu có. Nếu không, quá trình lặp dừng tại vị trí được chỉ định.

   Nếu *step* là ``None``, step mặc định là một. Các phần tử được trả về liên tiếp, trừ khi *step* được đặt lớn hơn một, khiến một số phần tử bị bỏ qua.

   Tương đương về cơ bản với::

      def islice(iterable, *args):
          # islice('ABCDEFG', 2) → A B
          # islice('ABCDEFG', 2, 4) → C D
          # islice('ABCDEFG', 2, None) → C D E F G
          # islice('ABCDEFG', 0, None, 2) → A C E G

          s = slice(*args)
          start = 0 if s.start is None else s.start
          stop = s.stop
          step = 1 if s.step is None else s.step
          if start < 0 or (stop is not None and stop < 0) or step <= 0:
              raise ValueError

          indices = count() if stop is None else range(max(start, stop))
          next_i = start
          for i, element in zip(indices, iterable):
              if i == next_i:
                  yield element
                  next_i += step

   Nếu đầu vào là một iterator, việc tiêu thụ hoàn toàn *islice* sẽ tiến iterator đầu vào thêm ``max(start, stop)`` bước, bất kể giá trị *step*.


.. function:: pairwise(iterable)

   Trả về các cặp chồng lấn liên tiếp được lấy từ *iterable* đầu vào.

   Số lượng bộ 2 phần tử trong iterator đầu ra sẽ ít hơn số lượng đầu vào một phần tử. Iterator này sẽ rỗng nếu iterable đầu vào có ít hơn hai giá trị.

   Tương đương về cơ bản với::

        def pairwise(iterable):
            # pairwise('ABCDEFG') → AB BC CD DE EF FG

            iterator = iter(iterable)
            a = next(iterator, None)

            for b in iterator:
                yield a, b
                a = b

   .. versionadded:: 3.10


.. function:: permutations(iterable, r=None)

   Trả về lần lượt các hoán vị có độ dài *r* `của các phần tử <https://www.britannica.com/science/permutation>`_ từ *iterable*.

   Nếu *r* không được chỉ định hoặc là ``None``, thì *r* mặc định bằng độ dài của *iterable* và tất cả các hoán vị có độ dài đầy đủ có thể được tạo ra.

   Đầu ra là một dãy con của :func:`product`, trong đó các phần tử bị lặp đã được lọc bỏ. Độ dài của đầu ra được cho bởi :func:`math.perm`, giá trị này tính ``n! / (n - r)!`` khi ``0 ≤ r ≤ n`` hoặc bằng 0 khi ``r > n``.

   Các tuple hoán vị được xuất theo thứ tự từ điển dựa trên thứ tự của *iterable* đầu vào. Nếu *iterable* đầu vào được sắp xếp, các tuple đầu ra sẽ được tạo theo thứ tự đã sắp xếp.

   Các phần tử được xem là duy nhất dựa trên vị trí của chúng, không phải giá trị của chúng. Nếu các phần tử đầu vào là duy nhất, sẽ không có giá trị nào bị lặp lại trong một hoán vị.

   Tương đương về cơ bản với::

        def permutations(iterable, r=None):
            # permutations('ABCD', 2) → AB AC AD BA BC BD CA CB CD DA DB DC
            # permutations(range(3)) → 012 021 102 120 201 210

            pool = tuple(iterable)
            n = len(pool)
            r = n if r is None else r
            if r > n:
                return

            indices = list(range(n))
            cycles = list(range(n, n-r, -1))
            yield tuple(pool[i] for i in indices[:r])

            while n:
                for i in reversed(range(r)):
                    cycles[i] -= 1
                    if cycles[i] == 0:
                        indices[i:] = indices[i+1:] + indices[i:i+1]
                        cycles[i] = n - i
                    else:
                        j = cycles[i]
                        indices[i], indices[-j] = indices[-j], indices[i]
                        yield tuple(pool[i] for i in indices[:r])
                        break
                else:
                    return


.. function:: product(*iterables, repeat=1)

   `Tích Descartes <https://en.wikipedia.org/wiki/Cartesian_product>`_ của các iterable đầu vào.

   Tương đương về cơ bản với các vòng lặp for lồng nhau trong một biểu thức generator. Ví dụ, ``product(A, B)`` trả về kết quả giống như ``((x,y) for x in A for y in B)``.

   Các vòng lặp lồng nhau hoạt động như một công tơ mét, trong đó phần tử ngoài cùng bên phải tiến lên sau mỗi lần lặp. Mẫu này tạo ra thứ tự từ điển, vì vậy nếu các iterable đầu vào đã được sắp xếp, các tuple sản phẩm cũng được xuất ra theo thứ tự đã sắp xếp.

   Để tính tích của một iterable với chính nó, hãy chỉ định số lần lặp lại bằng đối số từ khóa tùy chọn *repeat*. Ví dụ, ``product(A, repeat=4)`` có nghĩa tương đương với ``product(A, A, A, A)``.

   Hàm này gần tương đương với đoạn mã sau, ngoại trừ việc phần triển khai thực tế không xây dựng các kết quả trung gian trong bộ nhớ::

       def product(*iterables, repeat=1):
           # product('ABCD', 'xy') → Ax Ay Bx By Cx Cy Dx Dy
           # product(range(2), repeat=3) → 000 001 010 011 100 101 110 111

           if repeat < 0:
               raise ValueError('repeat argument cannot be negative')
           pools = [tuple(pool) for pool in iterables] * repeat

           result = [[]]
           for pool in pools:
               result = [x+[y] for x in result for y in pool]

           for prod in result:
               yield tuple(prod)

   Trước khi :func:`product` chạy, nó sẽ tiêu thụ hoàn toàn các iterable đầu vào, giữ các pool giá trị trong bộ nhớ để tạo ra các tích. Vì vậy, nó chỉ hữu ích với các đầu vào hữu hạn.


.. function:: repeat(object[, times])

   Tạo một iterator trả về *object* lặp đi lặp lại. Chạy vô hạn trừ khi chỉ định đối số *times*.

   Tương đương về cơ bản với::

      def repeat(object, times=None):
          # repeat(10, 3) → 10 10 10
          if times is None:
              while True:
                  yield object
          else:
              for i in range(times):
                  yield object

   Một cách sử dụng phổ biến của *repeat* là cung cấp một luồng các giá trị hằng cho *map* hoặc *zip*:

   .. doctest::

      >>> list(map(pow, range(10), repeat(2)))
      [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]


.. function:: starmap(function, iterable)

   Tạo một iterator tính toán *function* bằng các đối số lấy từ *iterable*. Dùng thay cho :func:`map` khi các tham số đối số đã được "pre-zipped" thành các tuple.

   Sự khác biệt giữa :func:`map` và :func:`starmap` tương tự như sự phân biệt giữa ``function(a,b)`` và ``function(*c)``. Gần tương đương với::

      def starmap(function, iterable):
          # starmap(pow, [(2,5), (3,2), (10,3)]) → 32 9 1000
          for args in iterable:
              yield function(*args)


.. function:: takewhile(predicate, iterable)

   Tạo một iterator trả về các phần tử từ *iterable* chừng nào *predicate* còn đúng. Gần tương đương với::

      def takewhile(predicate, iterable):
          # takewhile(lambda x: x<5, [1,4,6,3,8]) → 1 4
          for x in iterable:
              if not predicate(x):
                  break
              yield x

   Lưu ý rằng phần tử đầu tiên không thỏa điều kiện của predicate sẽ bị lấy khỏi input iterator và không có cách nào truy cập phần tử đó. Đây có thể là vấn đề nếu một ứng dụng muốn tiếp tục lấy dữ liệu từ input iterator sau khi *takewhile* đã chạy đến :term:`exhaustion <exhausted>`. Để khắc phục vấn đề này, hãy cân nhắc sử dụng `more-itertools before_and_after() <https://more-itertools.readthedocs.io/en/stable/api.html#more_itertools.before_and_after>`__ thay thế.


.. function:: tee(iterable, n=2)

   Trả về *n* iterator độc lập từ một iterable duy nhất.

   Tương đương về cơ bản với::

        def tee(iterable, n=2):
            if n < 0:
                raise ValueError
            if n == 0:
                return ()
            iterator = _tee(iterable)
            result = [iterator]
            for _ in range(n - 1):
                result.append(_tee(iterator))
            return tuple(result)

        class _tee:

            def __init__(self, iterable):
                it = iter(iterable)
                if isinstance(it, _tee):
                    self.iterator = it.iterator
                    self.link = it.link
                else:
                    self.iterator = it
                    self.link = [None, None]

            def __iter__(self):
                return self

            def __next__(self):
                link = self.link
                if link[1] is None:
                    link[0] = next(self.iterator)
                    link[1] = [None, None]
                value, self.link = link
                return value

   Khi đầu vào *iterable* đã là một đối tượng tee iterator, mọi thành phần của tuple trả về đều được tạo như thể chúng được tạo bởi lời gọi :func:`tee` ở upstream. "Bước làm phẳng" này cho phép các lời gọi :func:`tee` lồng nhau dùng chung một chuỗi dữ liệu nền và chỉ cần một bước cập nhật thay vì một chuỗi lời gọi.

   Tính chất làm phẳng giúp tee iterator có thể peek một cách hiệu quả:

   .. testcode::

      def lookahead(tee_iterator):
           "Return the next value without moving the input forward"
           [forked_iterator] = tee(tee_iterator, 1)
           return next(forked_iterator)

   .. doctest::

      >>> iterator = iter('abcdef')
      >>> [iterator] = tee(iterator, 1)   # Cho đầu vào có thể peek
      >>> next(iterator)                  # Tiến iterator về phía trước
      'a'
      >>> lookahead(iterator)             # Kiểm tra giá trị tiếp theo
      'b'
      >>> next(iterator)                  # Tiếp tục di chuyển về phía trước
      'b'

   ``tee`` iterator không an toàn khi sử dụng trong nhiều thread. Có thể phát sinh :exc:`RuntimeError` khi đồng thời sử dụng các iterator được trả về bởi cùng một lệnh gọi :func:`tee`, ngay cả khi *iterable* ban đầu không gặp vấn đề này.

   itertool này có thể yêu cầu lượng bộ nhớ lưu trữ phụ trợ đáng kể (tùy thuộc vào lượng dữ liệu tạm thời cần lưu trữ). Nhìn chung, nếu một iterator sử dụng hầu hết hoặc toàn bộ dữ liệu trước khi một iterator khác bắt đầu, thì sử dụng
   :func:`list` thay vì :func:`tee` sẽ nhanh hơn.


.. function:: zip_longest(*iterables, fillvalue=None)

   Tạo một iterator tổng hợp các phần tử từ từng *iterables*.

   Nếu các iterable có độ dài không bằng nhau, các giá trị còn thiếu sẽ được điền bằng *fillvalue*. Nếu không được chỉ định, *fillvalue* mặc định là ``None``.

   Việc lặp tiếp tục cho đến khi iterable dài nhất là :term:`exhausted`.

   Tương đương về cơ bản với::

      def zip_longest(*iterables, fillvalue=None):
          # zip_longest('ABCD', 'xy', fillvalue='-') → Ax By C- D-

          iterators = list(map(iter, iterables))
          num_active = len(iterators)
          if not num_active:
              return

          while True:
              values = []
              for i, iterator in enumerate(iterators):
                  try:
                      value = next(iterator)
                  except StopIteration:
                      num_active -= 1
                      if not num_active:
                          return
                      iterators[i] = repeat(fillvalue)
                      value = fillvalue
                  values.append(value)
              yield tuple(values)

   Nếu một trong các iterable có khả năng là vô hạn, thì hàm :func:`zip_longest` nên được bọc bằng một thành phần giới hạn số lần gọi (ví dụ :func:`islice` hoặc :func:`takewhile`).


.. _itertools-recipes:

Các công thức itertools
-----------------------

Phần này trình bày các công thức để tạo một bộ công cụ mở rộng bằng cách sử dụng các itertools hiện có làm khối xây dựng.

Mục đích chính của các công thức itertools là phục vụ việc học. Các công thức cho thấy nhiều cách khác nhau để tư duy về từng công cụ — ví dụ, ``chain.from_iterable`` có liên quan đến khái niệm làm phẳng. Các công thức cũng đưa ra ý tưởng về cách kết hợp các công cụ — ví dụ, cách ``starmap()`` và ``repeat()`` có thể hoạt động cùng nhau. Các công thức cũng trình bày các mẫu sử dụng itertools với các module :mod:`operator` và :mod:`collections`, cũng như với các itertools tích hợp sẵn như ``map()``, ``filter()``, ``reversed()`` và ``enumerate()``.

Mục đích thứ hai của các công thức là làm vườn ươm. Các itertools ``accumulate()``, ``compress()`` và ``pairwise()`` ban đầu là các công thức. Hiện tại, các công thức ``sliding_window()``, ``derangements()`` và ``sieve()`` đang được thử nghiệm để xem chúng có chứng minh được giá trị hay không.

Phần lớn các recipe này và rất nhiều recipe khác có thể được cài đặt từ dự án :pypi:`more-itertools` trên Python Package Index::

    python -m pip install more-itertools

Nhiều recipe mang lại hiệu năng cao tương đương với bộ công cụ nền tảng. Hiệu quả bộ nhớ vượt trội được duy trì bằng cách xử lý từng phần tử một thay vì đưa toàn bộ iterable vào bộ nhớ cùng lúc. Khối lượng mã được giữ ở mức nhỏ bằng cách liên kết các công cụ với nhau theo `phong cách functional <https://www.cs.kent.ac.uk/people/staff/dat/miranda/whyfp90.pdf>`_. Tốc độ cao được duy trì bằng cách ưu tiên các khối xây dựng "vectorized" thay vì sử dụng vòng lặp for và :term:`generator <generator>`, vốn gây ra overhead cho interpreter.

.. testcode::

   from itertools import (accumulate, batched, chain, combinations, compress,
        count, cycle, filterfalse, groupby, islice, permutations, product,
        repeat, starmap, tee, zip_longest)
   from collections import Counter, deque
   from contextlib import suppress
   from functools import reduce
   from heapq import heappush, heappushpop, heappush_max, heappushpop_max
   from math import comb, isqrt, prod, sumprod
   from operator import getitem, is_not, itemgetter, mul, neg, truediv


   # ==== Các dòng lệnh cơ bản ====

   def take(n, iterable):
       "Return first n items of the iterable as a list."
       return list(islice(iterable, n))

   def prepend(value, iterable):
       "Prepend a single value in front of an iterable."
       # prepend(1, [2, 3, 4]) → 1 2 3 4
       return chain([value], iterable)

   def repeatfunc(function, times=None, *args):
       "Repeat calls to a function with specified arguments."
       if times is None:
           return starmap(function, repeat(args))
       return starmap(function, repeat(args, times))

   def flatten(list_of_lists):
       "Flatten one level of nesting."
       return chain.from_iterable(list_of_lists)

   def ncycles(iterable, n):
       "Returns the sequence elements n times."
       return chain.from_iterable(repeat(tuple(iterable), n))

   def loops(n):
       "Loop n times. Like range(n) but without creating integers."
       # for _ in loops(100): ...
       return repeat(None, n)

   def tail(n, iterable):
       "Return an iterator over the last n items."
       # tail(3, 'ABCDEFG') → E F G
       return iter(deque(iterable, maxlen=n))

   def consume(iterator, n=None):
       "Advance the iterator n-steps ahead. If n is None, consume entirely."
       # Sử dụng các hàm tiêu thụ iterator ở tốc độ C.
       if n is None:
           deque(iterator, maxlen=0)
       else:
           next(islice(iterator, n, n), None)

   def nth(iterable, n, default=None):
       "Returns the nth item or a default value."
       return next(islice(iterable, n, None), default)

   def quantify(iterable, predicate=bool):
       "Given a predicate that returns True or False, count the True results."
       return sum(map(predicate, iterable))

   def first_true(iterable, default=False, predicate=None):
       "Returns the first true value or the *default* if there is no true value."
       # first_true([a, b, c], x) → a or b or c or x
       # first_true([a, b], x, f) → a if f(a) else b if f(b) else x
       return next(filter(predicate, iterable), default)

   def all_equal(iterable, key=None):
       "Returns True if all the elements are equal to each other."
       # all_equal('4٤௪౪໔', key=int) → True
       return len(take(2, groupby(iterable, key))) <= 1


   # ==== Quy trình dữ liệu ====

   def unique_justseen(iterable, key=None):
       "Yield unique elements, preserving order. Remember only the element just seen."
       # unique_justseen('AAAABBBCCDAABBB') → A B C D A B
       # unique_justseen('ABBcCAD', str.casefold) → A B c A D
       if key is None:
           return map(itemgetter(0), groupby(iterable))
       return map(next, map(itemgetter(1), groupby(iterable, key)))

   def unique_everseen(iterable, key=None):
       "Yield unique elements, preserving order. Remember all elements ever seen."
       # unique_everseen('AAAABBBCCDAABBB') → A B C D
       # unique_everseen('ABBcCAD', str.casefold) → A B c D
       seen = set()
       if key is None:
           for element in filterfalse(seen.__contains__, iterable):
               seen.add(element)
               yield element
       else:
           for element in iterable:
               k = key(element)
               if k not in seen:
                   seen.add(k)
                   yield element

   def unique(iterable, key=None, reverse=False):
       "Yield unique elements in sorted order. Supports unhashable inputs."
       # unique([[1, 2], [3, 4], [1, 2]]) → [1, 2] [3, 4]
       sequenced = sorted(iterable, key=key, reverse=reverse)
       return unique_justseen(sequenced, key=key)

   def sliding_window(iterable, n):
       "Collect data into overlapping fixed-length chunks or blocks."
       # sliding_window('ABCDEFG', 3) → ABC BCD CDE DEF EFG
       iterator = iter(iterable)
       window = deque(islice(iterator, n - 1), maxlen=n)
       for x in iterator:
           window.append(x)
           yield tuple(window)

   def grouper(iterable, n, *, incomplete='fill', fillvalue=None):
       "Collect data into non-overlapping fixed-length chunks or blocks."
       # grouper('ABCDEFG', 3, fillvalue='x')       → ABC DEF Gxx
       # grouper('ABCDEFG', 3, incomplete='strict') → ABC DEF ValueError
       # grouper('ABCDEFG', 3, incomplete='ignore') → ABC DEF
       iterators = [iter(iterable)] * n
       match incomplete:
           case 'fill':
               return zip_longest(*iterators, fillvalue=fillvalue)
           case 'strict':
               return zip(*iterators, strict=True)
           case 'ignore':
               return zip(*iterators)
           case _:
               raise ValueError('Expected fill, strict, or ignore')

   def roundrobin(*iterables):
       "Visit input iterables in a cycle until each is exhausted."
       # roundrobin('ABC', 'D', 'EF') → A D E B F C
       # Thuật toán do George Sakkis đề xuất
       iterators = map(iter, iterables)
       for num_active in range(len(iterables), 0, -1):
           iterators = cycle(islice(iterators, num_active))
           yield from map(next, iterators)

   def subslices(seq):
       "Return all contiguous non-empty subslices of a sequence."
       # subslices('ABCD') → A AB ABC ABCD B BC BCD C CD D
       slices = starmap(slice, combinations(range(len(seq) + 1), 2))
       return map(getitem, repeat(seq), slices)

   def derangements(iterable, r=None):
       "Produce r length permutations without fixed points."
       # derangements('ABCD') → BADC BCDA BDAC CADB CDAB CDBA DABC DCAB DCBA
       # Thuật toán do Stefan Pochmann đề xuất
       seq = tuple(iterable)
       pos = tuple(range(len(seq)))
       have_moved = map(map, repeat(is_not), repeat(pos), permutations(pos, r=r))
       valid_derangements = map(all, have_moved)
       return compress(permutations(seq, r=r), valid_derangements)

   def iter_index(iterable, value, start=0, stop=None):
       "Return indices where a value occurs in a sequence or iterable."
       # iter_index('AABCADEAF', 'A') → 0 1 4 7
       seq_index = getattr(iterable, 'index', None)
       if seq_index is None:
           iterator = islice(iterable, start, stop)
           for i, element in enumerate(iterator, start):
               if element is value or element == value:
                   yield i
       else:
           stop = len(iterable) if stop is None else stop
           i = start
           with suppress(ValueError):
               while True:
                   yield (i := seq_index(value, i, stop))
                   i += 1

   def iter_except(function, exception, first=None):
       "Convert a call-until-exception interface to an iterator interface."
       # iter_except(d.popitem, KeyError) → iterator dictionary không chặn
       with suppress(exception):
           if first is not None:
               yield first()
           while True:
               yield function()


   # ==== Các phép toán toán học ====

   def multinomial(*counts):
       "Number of distinct arrangements of a multiset."
       # Counter('abracadabra').values() → 5 2 2 1 1
       # multinomial(5, 2, 2, 1, 1) → 83160
       return prod(map(comb, accumulate(counts), counts))

   def powerset(iterable):
       "Subsequences of the iterable from shortest to longest."
       # powerset([1,2,3]) → () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
       s = list(iterable)
       return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

   def sum_of_squares(iterable):
       "Add up the squares of the input values."
       # sum_of_squares([10, 20, 30]) → 1400
       return sumprod(*tee(iterable))


   # ==== Các phép toán ma trận ====

   def reshape(matrix, columns):
       "Reshape a 2-D matrix to have a given number of columns."
       # reshape([(0, 1), (2, 3), (4, 5)], 3) →  (0, 1, 2) (3, 4, 5)
       return batched(chain.from_iterable(matrix), columns, strict=True)

   def transpose(matrix):
       "Swap the rows and columns of a 2-D matrix."
       # transpose([(1, 2, 3), (11, 22, 33)]) → (1, 11) (2, 22) (3, 33)
       return zip(*matrix, strict=True)

   def matmul(m1, m2):
       "Multiply two matrices."
       # matmul([(7, 5), (3, 5)], [(2, 5), (7, 9)]) → (49, 80) (41, 60)
       n = len(m2[0])
       return batched(starmap(sumprod, product(m1, transpose(m2))), n)


   # ==== Số học đa thức ====

   def convolve(signal, kernel):
       """Discrete linear convolution of two iterables.
       Equivalent to polynomial multiplication.

       Convolutions are mathematically commutative; however, the inputs are
       evaluated differently.  The signal is consumed lazily and can be
       infinite. The kernel is fully consumed before the calculations begin.

       Article:  https://betterexplained.com/articles/intuitive-convolution/
       Video:    https://www.youtube.com/watch?v=KuXjwB4LzSA
       """
       # convolve([1, -1, -20], [1, -3]) → 1 -4 -17 60
       # convolve(data, [0.25, 0.25, 0.25, 0.25]) → Trung bình trượt (làm mờ)
       # convolve(data, [1/2, 0, -1/2]) → Ước lượng đạo hàm cấp 1
       # convolve(data, [1, -2, 1]) → Ước lượng đạo hàm cấp 2
       kernel = tuple(kernel)[::-1]
       n = len(kernel)
       padded_signal = chain(repeat(0, n-1), signal, repeat(0, n-1))
       windowed_signal = sliding_window(padded_signal, n)
       return map(sumprod, repeat(kernel), windowed_signal)

   def polynomial_from_roots(roots):
       """Compute a polynomial's coefficients from its roots.

          (x - 5) (x + 4) (x - 3)  expands to:   x³ -4x² -17x + 60
       """
       # polynomial_from_roots([5, -4, 3]) → [1, -4, -17, 60]
       factors = zip(repeat(1), map(neg, roots))
       return list(reduce(convolve, factors, [1]))

   def polynomial_eval(coefficients, x):
       """Evaluate a polynomial at a specific value.

       Computes with better numeric stability than Horner's method.
       """
       # Tính giá trị của x³ -4x² -17x + 60 tại x = 5
       # polynomial_eval([1, -4, -17, 60], x=5) → 0
       n = len(coefficients)
       if not n:
           return type(x)(0)
       powers = map(pow, repeat(x), reversed(range(n)))
       return sumprod(coefficients, powers)

   def polynomial_derivative(coefficients):
       """Compute the first derivative of a polynomial.

          f(x)  =  x³ -4x² -17x + 60
          f'(x) = 3x² -8x  -17
       """
       # polynomial_derivative([1, -4, -17, 60]) → [3, -8, -17]
       n = len(coefficients)
       powers = reversed(range(1, n))
       return list(map(mul, coefficients, powers))


   # ==== Lý thuyết số ====

   def sieve(n):
       "Primes less than n."
       # sieve(30) → 2 3 5 7 11 13 17 19 23 29
       if n > 2:
           yield 2
       data = bytearray((0, 1)) * (n // 2)
       for p in iter_index(data, 1, start=3, stop=isqrt(n) + 1):
           data[p*p : n : p+p] = bytes(len(range(p*p, n, p+p)))
       yield from iter_index(data, 1, start=3)

   def factor(n):
       "Prime factors of n."
       # factor(99) → 3 3 11
       # factor(1_000_000_000_000_007) → 47 59 360620266859
       # factor(1_000_000_000_000_403) → 1000000000000403
       for prime in sieve(isqrt(n) + 1):
           while not n % prime:
               yield prime
               n //= prime
               if n == 1:
                   return
       if n > 1:
           yield n

   def is_prime(n):
       "Return True if n is prime."
       # is_prime(1_000_000_000_000_403) → True
       return n > 1 and next(factor(n)) == n

   def totient(n):
       "Count of natural numbers up to n that are coprime to n."
       # https://mathworld.wolfram.com/TotientFunction.html
       # totient(12) → 4 vì len([1, 5, 7, 11]) == 4
       for prime in set(factor(n)):
           n -= n // prime
       return n


   # ==== Thống kê lũy tiến ====

   def running_mean(iterable):
       "Average of values seen so far."
       # running_mean([37, 33, 38, 28]) → 37 35 36 34
       return map(truediv, accumulate(iterable), count(1))

   def running_min(iterable):
       "Smallest of values seen so far."
       # running_min([37, 33, 38, 28]) → 37 33 33 28
       return accumulate(iterable, func=min)

   def running_max(iterable):
       "Largest of values seen so far."
       # running_max([37, 33, 38, 28]) → 37 37 38 38
       return accumulate(iterable, func=max)

   def running_median(iterable):
       "Median of values seen so far."
       # running_median([37, 33, 38, 28]) → 37 35 37 35
       read = iter(iterable).__next__
       lo = []  # max-heap
       hi = []  # min-heap có cùng kích thước với lo hoặc nhỏ hơn lo một phần tử
       with suppress(StopIteration):
           while True:
               heappush_max(lo, heappushpop(hi, read()))
               yield lo[0]
               heappush(hi, heappushpop_max(lo, read()))
               yield (lo[0] + hi[0]) / 2

   def running_statistics(iterable):
       "Aggregate statistics for values seen so far."
       # Tạo các tuple:  (size, minimum, median, maximum, mean)
       t0, t1, t2, t3 = tee(iterable, 4)
       return zip(
           count(1),
           running_min(t0),
           running_median(t1),
           running_max(t2),
           running_mean(t3),
       )


.. doctest::
    :hide:

    These examples no longer appear in the docs but are guaranteed
    to keep working.

    >>> amounts = [120.15, 764.05, 823.14]
    >>> for checknum, amount in zip(count(1200), amounts):
    ...     print('Check %d is for $%.2f' % (checknum, amount))
    ...
    Check 1200 is for $120.15
    Check 1201 is for $764.05
    Check 1202 is for $823.14

    >>> import operator
    >>> for cube in map(operator.pow, range(1,4), repeat(3)):
    ...    print(cube)
    ...
    1
    8
    27

    >>> reportlines = ['EuroPython', 'Roster', '', 'alex', '', 'laura', '', 'martin', '', 'walter', '', 'samuele']
    >>> for name in islice(reportlines, 3, None, 2):
    ...    print(name.title())
    ...
    Alex
    Laura
    Martin
    Walter
    Samuele

    >>> from operator import itemgetter
    >>> d = dict(a=1, b=2, c=1, d=2, e=1, f=2, g=3)
    >>> di = sorted(sorted(d.items()), key=itemgetter(1))
    >>> for k, g in groupby(di, itemgetter(1)):
    ...     print(k, list(map(itemgetter(0), g)))
    ...
    1 ['a', 'c', 'e']
    2 ['b', 'd', 'f']
    3 ['g']

    # Tìm các dãy số liên tiếp bằng groupby.  Mấu chốt của lời giải
    # là lấy hiệu với một range để tất cả các số liên tiếp đều xuất hiện trong
    # cùng một nhóm.
    >>> data = [ 1,  4,5,6, 10, 15,16,17,18, 22, 25,26,27,28]
    >>> for k, g in groupby(enumerate(data), lambda t:t[0]-t[1]):
    ...     print(list(map(operator.itemgetter(1), g)))
    ...
    [1]
    [4, 5, 6]
    [10]
    [15, 16, 17, 18]
    [22]
    [25, 26, 27, 28]

    Now, we test all of the itertool recipes

    >>> take(10, count())
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> # Xác minh rằng đầu vào được tiêu thụ theo kiểu lazy
    >>> it = iter('abcdef')
    >>> take(3, it)
    ['a', 'b', 'c']
    >>> list(it)
    ['d', 'e', 'f']


    >>> list(prepend(1, [2, 3, 4]))
    [1, 2, 3, 4]


    >>> list(enumerate('abc'))
    [(0, 'a'), (1, 'b'), (2, 'c')]


    >>> for _ in loops(5):
    ...     print('hi')
    ...
    hi
    hi
    hi
    hi
    hi


    >>> list(tail(3, 'ABCDEFG'))
    ['E', 'F', 'G']
    >>> # Xác minh rằng đầu vào được tiêu thụ theo kiểu greedy
    >>> input_iterator = iter('ABCDEFG')
    >>> output_iterator = tail(3, input_iterator)
    >>> list(input_iterator)
    []


    >>> it = iter(range(10))
    >>> consume(it, 3)
    >>> # Xác minh rằng đầu vào được tiêu thụ theo kiểu lazy
    >>> next(it)
    3
    >>> # Xác minh rằng đầu vào được tiêu thụ hoàn toàn
    >>> consume(it)
    >>> next(it, 'Done')
    'Done'


    >>> nth('abcde', 3)
    'd'
    >>> nth('abcde', 9) is None
    True
    >>> # Xác minh rằng đầu vào được tiêu thụ theo kiểu lazy
    >>> it = iter('abcde')
    >>> nth(it, 2)
    'c'
    >>> list(it)
    ['d', 'e']


    >>> [all_equal(s) for s in ('', 'A', 'AAAA', 'AAAB', 'AAABA')]
    [True, True, True, False, False]
    >>> [all_equal(s, key=str.casefold) for s in ('', 'A', 'AaAa', 'AAAB', 'AAABA')]
    [True, True, True, False, False]
    >>> # Xác minh rằng đầu vào được tiêu thụ theo kiểu lazy và chỉ
    >>> # một phần tử của lớp tương đương thứ hai được dùng để bác bỏ
    >>> # khẳng định rằng tất cả các phần tử đều bằng nhau.
    >>> it = iter('aaabbbccc')
    >>> all_equal(it)
    False
    >>> ''.join(it)
    'bbccc'


    >>> quantify(range(99), lambda x: x%2==0)
    50
    >>> quantify([True, False, False, True, True])
    3
    >>> quantify(range(12), predicate=lambda x: x%2==1)
    6


    >>> a = [[1, 2, 3], [4, 5, 6]]
    >>> list(flatten(a))
    [1, 2, 3, 4, 5, 6]


    >>> list(ncycles('abc', 3))
    ['a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c']
    >>> # Xác minh việc tiêu thụ tham lam iterator đầu vào
    >>> input_iterator = iter('abc')
    >>> output_iterator = ncycles(input_iterator, 3)
    >>> list(input_iterator)
    []


    >>> sum_of_squares([10, 20, 30])
    1400


    >>> list(reshape([(0, 1), (2, 3), (4, 5)], 3))
    [(0, 1, 2), (3, 4, 5)]
    >>> M = [(0, 1, 2, 3), (4, 5, 6, 7), (8, 9, 10, 11)]
    >>> list(reshape(M, 1))
    [(0,), (1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (10,), (11,)]
    >>> list(reshape(M, 2))
    [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10, 11)]
    >>> list(reshape(M, 3))
    [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11)]
    >>> list(reshape(M, 4))
    [(0, 1, 2, 3), (4, 5, 6, 7), (8, 9, 10, 11)]
    >>> list(reshape(M, 5))
    Traceback (most recent call last):
    ...
    ValueError: batched(): incomplete batch
    >>> list(reshape(M, 6))
    [(0, 1, 2, 3, 4, 5), (6, 7, 8, 9, 10, 11)]
    >>> list(reshape(M, 12))
    [(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)]


    >>> list(transpose([(1, 2, 3), (11, 22, 33)]))
    [(1, 11), (2, 22), (3, 33)]
    >>> # Xác minh rằng các đầu vào được tiêu thụ theo cách lazy
    >>> input1 = iter([1, 2, 3])
    >>> input2 = iter([11, 22, 33])
    >>> output_iterator = transpose([input1, input2])
    >>> next(output_iterator)
    (1, 11)
    >>> list(zip(input1, input2))
    [(2, 22), (3, 33)]


    >>> list(matmul([(7, 5), (3, 5)], [[2, 5], [7, 9]]))
    [(49, 80), (41, 60)]
    >>> list(matmul([[2, 5], [7, 9], [3, 4]], [[7, 11, 5, 4, 9], [3, 5, 2, 6, 3]]))
    [(29, 47, 20, 38, 33), (76, 122, 53, 82, 90), (33, 53, 23, 36, 39)]


    >>> list(convolve([1, -1, -20], [1, -3])) == [1, -4, -17, 60]
    True
    >>> data = [20, 40, 24, 32, 20, 28, 16]
    >>> list(convolve(data, [0.25, 0.25, 0.25, 0.25]))
    [5.0, 15.0, 21.0, 29.0, 29.0, 26.0, 24.0, 16.0, 11.0, 4.0]
    >>> list(convolve(data, [1, -1]))
    [20, 20, -16, 8, -12, 8, -12, -16]
    >>> list(convolve(data, [1, -2, 1]))
    [20, 0, -36, 24, -20, 20, -20, -4, 16]
    >>> # Xác minh rằng signal được tiêu thụ theo cách lazy còn kernel được tiêu thụ tham lam
    >>> signal_iterator = iter([10, 20, 30, 40, 50])
    >>> kernel_iterator = iter([1, 2, 3])
    >>> output_iterator = convolve(signal_iterator, kernel_iterator)
    >>> list(kernel_iterator)
    []
    >>> next(output_iterator)
    10
    >>> next(output_iterator)
    40
    >>> list(signal_iterator)
    [30, 40, 50]


    >>> from fractions import Fraction
    >>> from decimal import Decimal
    >>> polynomial_eval([1, -4, -17, 60], x=5)
    0
    >>> x = 5; x**3 - 4*x**2 -17*x + 60
    0
    >>> polynomial_eval([1, -4, -17, 60], x=2.5)
    8.125
    >>> x = 2.5; x**3 - 4*x**2 -17*x + 60
    8.125
    >>> polynomial_eval([1, -4, -17, 60], x=Fraction(2, 3))
    Fraction(1274, 27)
    >>> x = Fraction(2, 3); x**3 - 4*x**2 -17*x + 60
    Fraction(1274, 27)
    >>> polynomial_eval([1, -4, -17, 60], x=Decimal('1.75'))
    Decimal('23.359375')
    >>> x = Decimal('1.75'); x**3 - 4*x**2 -17*x + 60
    Decimal('23.359375')
    >>> polynomial_eval([], 2)
    0
    >>> polynomial_eval([], 2.5)
    0.0
    >>> polynomial_eval([], Fraction(2, 3))
    Fraction(0, 1)
    >>> polynomial_eval([], Decimal('1.75'))
    Decimal('0')
    >>> polynomial_eval([11], 7) == 11
    True
    >>> polynomial_eval([11, 2], 7) == 11 * 7 + 2
    True


    >>> polynomial_from_roots([5, -4, 3])
    [1, -4, -17, 60]
    >>> factored = lambda x: (x - 5) * (x + 4) * (x - 3)
    >>> expanded = lambda x: x**3 -4*x**2 -17*x + 60
    >>> all(factored(x) == expanded(x) for x in range(-10, 11))
    True


    >>> polynomial_derivative([1, -4, -17, 60])
    [3, -8, -17]


    >>> list(iter_index('AABCADEAF', 'A'))
    [0, 1, 4, 7]
    >>> list(iter_index('AABCADEAF', 'B'))
    [2]
    >>> list(iter_index('AABCADEAF', 'X'))
    []
    >>> list(iter_index('', 'X'))
    []
    >>> list(iter_index('AABCADEAF', 'A', 1))
    [1, 4, 7]
    >>> list(iter_index(iter('AABCADEAF'), 'A', 1))
    [1, 4, 7]
    >>> list(iter_index('AABCADEAF', 'A', 2))
    [4, 7]
    >>> list(iter_index(iter('AABCADEAF'), 'A', 2))
    [4, 7]
    >>> list(iter_index('AABCADEAF', 'A', 10))
    []
    >>> list(iter_index(iter('AABCADEAF'), 'A', 10))
    []
    >>> list(iter_index('AABCADEAF', 'A', 1, 7))
    [1, 4]
    >>> list(iter_index(iter('AABCADEAF'), 'A', 1, 7))
    [1, 4]
    >>> # Xác minh rằng các ValueError không bị nuốt (gh-107208)
    >>> def assert_no_value(iterable, forbidden_value):
    ...     for item in iterable:
    ...         if item == forbidden_value:
    ...             raise ValueError
    ...         yield item
    ...
    >>> list(iter_index(assert_no_value('AABCADEAF', 'B'), 'A'))
    Traceback (most recent call last):
    ...
    ValueError
    >>> # Xác minh rằng cả hai đường đi đều có thể tìm thấy các giá trị NaN giống hệt nhau
    >>> x = float('NaN')
    >>> y = float('NaN')
    >>> list(iter_index([0, x, x, y, 0], x))
    [1, 2]
    >>> list(iter_index(iter([0, x, x, y, 0]), x))
    [1, 2]
    >>> # Kiểm thử đầu vào dạng list. List không hỗ trợ None cho đối số stop
    >>> list(iter_index(list('AABCADEAF'), 'A'))
    [0, 1, 4, 7]
    >>> # Kiểm tra rằng input được xử lý theo cơ chế lazy
    >>> input_iterator = iter('AABCADEAF')
    >>> output_iterator = iter_index(input_iterator, 'A')
    >>> next(output_iterator)
    0
    >>> next(output_iterator)
    1
    >>> next(output_iterator)
    4
    >>> ''.join(input_iterator)
    'DEAF'


    >>> # Kiểm tra rằng giá trị đích có thể là một sequence.
    >>> seq = [[10, 20], [30, 40], 30, 40, [30, 40], 50]
    >>> target = [30, 40]
    >>> list(iter_index(seq, target))
    [1, 4]


    >>> # Kiểm tra tính nhất quán với hành vi của phương thức index() riêng theo từng kiểu dữ liệu.
    >>> # Ví dụ: bytes và str thực hiện tìm kiếm các chuỗi con liên tiếp
    >>> # không khớp với hành vi chung được chỉ định
    >>> # trong collections.abc.Sequence.index().
    >>> seq = 'abracadabra'
    >>> target = 'ab'
    >>> list(iter_index(seq, target))
    [0, 7]


    >>> list(sieve(30))
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    >>> small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    >>> all(list(sieve(n)) == [p for p in small_primes if p < n] for n in range(101))
    True
    >>> len(list(sieve(100)))
    25
    >>> len(list(sieve(1_000)))
    168
    >>> len(list(sieve(10_000)))
    1229
    >>> len(list(sieve(100_000)))
    9592
    >>> len(list(sieve(1_000_000)))
    78498
    >>> carmichael = {561, 1105, 1729, 2465, 2821, 6601, 8911}  # https://oeis.org/A002997
    >>> set(sieve(10_000)).isdisjoint(carmichael)
    True


    >>> small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    >>> list(filter(is_prime, range(-100, 100))) == small_primes
    True
    >>> carmichael = {561, 1105, 1729, 2465, 2821, 6601, 8911}  # https://oeis.org/A002997
    >>> any(map(is_prime, carmichael))
    False
    >>> # https://www.wolframalpha.com/input?i=is+128884753939+prime
    >>> is_prime(128_884_753_939)           # số nguyên tố lớn
    True
    >>> is_prime(999953 * 999983)           # số bán nguyên tố lớn
    False
    >>> is_prime(1_000_000_000_000_007)     # ví dụ factor()
    False
    >>> is_prime(1_000_000_000_000_403)     # ví dụ factor()
    True


    >>> list(factor(99))                    # Ví dụ mã 1
    [3, 3, 11]
    >>> list(factor(1_000_000_000_000_007)) # Ví dụ mã 2
    [47, 59, 360620266859]
    >>> list(factor(1_000_000_000_000_403)) # Ví dụ mã 3
    [1000000000000403]
    >>> list(factor(0))
    []
    >>> list(factor(1))
    []
    >>> list(factor(2))
    [2]
    >>> list(factor(3))
    [3]
    >>> list(factor(4))
    [2, 2]
    >>> list(factor(5))
    [5]
    >>> list(factor(6))
    [2, 3]
    >>> list(factor(7))
    [7]
    >>> list(factor(8))
    [2, 2, 2]
    >>> list(factor(9))
    [3, 3]
    >>> list(factor(10))
    [2, 5]
    >>> list(factor(128_884_753_939))       # số nguyên tố lớn
    [128884753939]
    >>> list(factor(999953 * 999983))       # số bán nguyên tố lớn
    [999953, 999983]
    >>> list(factor(6 ** 20)) == [2] * 20 + [3] * 20   # lũy thừa lớn
    True
    >>> list(factor(909_909_090_909))       # hợp số lớn có nhiều thừa số
    [3, 3, 7, 13, 13, 751, 113797]
    >>> math.prod([3, 3, 7, 13, 13, 751, 113797])
    909909090909
    >>> all(math.prod(factor(n)) == n for n in range(1, 2_000))
    True
    >>> all(set(factor(n)) <= set(sieve(n+1)) for n in range(2_000))
    True
    >>> all(list(factor(n)) == sorted(factor(n)) for n in range(2_000))
    True


    >>> totient(0)  # https://www.wolframalpha.com/input?i=totient+0
    0
    >>> first_totients = [1, 1, 2, 2, 4, 2, 6, 4, 6, 4, 10, 4, 12, 6, 8, 8, 16, 6,
    ... 18, 8, 12, 10, 22, 8, 20, 12, 18, 12, 28, 8, 30, 16, 20, 16, 24, 12, 36, 18,
    ... 24, 16, 40, 12, 42, 20, 24, 22, 46, 16, 42, 20, 32, 24, 52, 18, 40, 24, 36,
    ... 28, 58, 16, 60, 30, 36, 32, 48, 20, 66, 32, 44]  # https://oeis.org/A000010
    ...
    >>> list(map(totient, range(1, 70))) == first_totients
    True
    >>> reference_totient = lambda n: sum(math.gcd(t, n) == 1 for t in range(1, n+1))
    >>> all(totient(n) == reference_totient(n) for n in range(1000))
    True
    >>> totient(128_884_753_939) == 128_884_753_938  # số nguyên tố lớn
    True
    >>> totient(999953 * 999983) == 999952 * 999982  # số bán nguyên tố lớn
    True
    >>> totient(6 ** 20) == 1 * 2**19 * 2 * 3**19    # các số nguyên tố lặp lại
    True


    >>> list(flatten([('a', 'b'), (), ('c', 'd', 'e'), ('f',), ('g', 'h', 'i')]))
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']


    >>> list(repeatfunc(pow, 5, 2, 3))
    [8, 8, 8, 8, 8]
    >>> take(5, map(int, repeatfunc(random.random)))
    [0, 0, 0, 0, 0]
    >>> random.seed(85753098575309)
    >>> list(repeatfunc(random.random, 3))
    [0.16370491282496968, 0.45889608687313455, 0.3747076837820118]
    >>> list(repeatfunc(chr, 3, 65))
    ['A', 'A', 'A']
    >>> list(repeatfunc(pow, 3, 2, 5))
    [32, 32, 32]


    >>> list(grouper('abcdefg', 3, fillvalue='x'))
    [('a', 'b', 'c'), ('d', 'e', 'f'), ('g', 'x', 'x')]


    >>> it = grouper('abcdefg', 3, incomplete='strict')
    >>> next(it)
    ('a', 'b', 'c')
    >>> next(it)
    ('d', 'e', 'f')
    >>> next(it)
    Traceback (most recent call last):
      ...
    ValueError: zip() argument 2 is shorter than argument 1

    >>> list(grouper('abcdefg', n=3, incomplete='ignore'))
    [('a', 'b', 'c'), ('d', 'e', 'f')]


    >>> list(sliding_window('ABCDEFG', 1))
    [('A',), ('B',), ('C',), ('D',), ('E',), ('F',), ('G',)]
    >>> list(sliding_window('ABCDEFG', 2))
    [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F'), ('F', 'G')]
    >>> list(sliding_window('ABCDEFG', 3))
    [('A', 'B', 'C'), ('B', 'C', 'D'), ('C', 'D', 'E'), ('D', 'E', 'F'), ('E', 'F', 'G')]
    >>> list(sliding_window('ABCDEFG', 4))
    [('A', 'B', 'C', 'D'), ('B', 'C', 'D', 'E'), ('C', 'D', 'E', 'F'), ('D', 'E', 'F', 'G')]
    >>> list(sliding_window('ABCDEFG', 5))
    [('A', 'B', 'C', 'D', 'E'), ('B', 'C', 'D', 'E', 'F'), ('C', 'D', 'E', 'F', 'G')]
    >>> list(sliding_window('ABCDEFG', 6))
    [('A', 'B', 'C', 'D', 'E', 'F'), ('B', 'C', 'D', 'E', 'F', 'G')]
    >>> list(sliding_window('ABCDEFG', 7))
    [('A', 'B', 'C', 'D', 'E', 'F', 'G')]
    >>> list(sliding_window('ABCDEFG', 8))
    []
    >>> try:
    ...     list(sliding_window('ABCDEFG', -1))
    ... except ValueError:
    ...     'zero or negative n not supported'
    ...
    'zero or negative n not supported'
    >>> try:
    ...     list(sliding_window('ABCDEFG', 0))
    ... except ValueError:
    ...     'zero or negative n not supported'
    ...
    'zero or negative n not supported'


    >>> list(roundrobin('abc', 'd', 'ef'))
    ['a', 'd', 'e', 'b', 'f', 'c']
    >>> ranges = [range(5, 1000), range(4, 3000), range(0), range(3, 2000), range(2, 5000), range(1, 3500)]
    >>> collections.Counter(roundrobin(*ranges)) == collections.Counter(chain(*ranges))
    True
    >>> # Xác minh rằng các đầu vào được tiêu thụ theo cách lazy
    >>> input_iterators = list(map(iter, ['abcd', 'ef', '', 'ghijk', 'l', 'mnopqr']))
    >>> output_iterator = roundrobin(*input_iterators)
    >>> ''.join(islice(output_iterator, 10))
    'aeglmbfhnc'
    >>> ''.join(chain(*input_iterators))
    'dijkopqr'


    >>> list(subslices('ABCD'))
    ['A', 'AB', 'ABC', 'ABCD', 'B', 'BC', 'BCD', 'C', 'CD', 'D']


    >>> ' '.join(map(''.join, derangements('ABCD')))
    'BADC BCDA BDAC CADB CDAB CDBA DABC DCAB DCBA'
    >>> ' '.join(map(''.join, derangements('ABCD', 3)))
    'BAD BCA BCD BDA CAB CAD CDA CDB DAB DCA DCB'
    >>> ' '.join(map(''.join, derangements('ABCD', 2)))
    'BA BC BD CA CD DA DC'
    >>> ' '.join(map(''.join, derangements('ABCD', 1)))
    'B C D'
    >>> ' '.join(map(''.join, derangements('ABCD', 0)))
    ''
    >>> # So sánh số lượng hoán vị không điểm cố định với https://oeis.org/A000166
    >>> [len(list(derangements(range(n)))) for n in range(10)]
    [1, 0, 1, 2, 9, 44, 265, 1854, 14833, 133496]
    >>> # Xác minh rằng các đối tượng giống hệt nhau được xem là duy nhất dựa trên vị trí
    >>> identical = 'X'
    >>> distinct = 'x'
    >>> seq1 = ('A', identical, 'B', identical)
    >>> result1 = ' '.join(map(''.join, derangements(seq1)))
    >>> result1
    'XAXB XBXA XXAB BAXX BXAX BXXA XAXB XBAX XBXA'
    >>> seq2 = ('A', identical, 'B', distinct)
    >>> result2 = ' '.join(map(''.join, derangements(seq2)))
    >>> result2
    'XAxB XBxA XxAB BAxX BxAX BxXA xAXB xBAX xBXA'
    >>> result1 == result2
    False
    >>> result1.casefold() == result2.casefold()
    True


    >>> list(powerset([1,2,3]))
    [(), (1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)]
    >>> all(len(list(powerset(range(n)))) == 2**n for n in range(18))
    True
    >>> list(powerset('abcde')) == sorted(sorted(set(powerset('abcde'))), key=len)
    True


    >>> list(unique_everseen('AAAABBBCCDAABBB'))
    ['A', 'B', 'C', 'D']
    >>> list(unique_everseen('ABBCcAD', str.casefold))
    ['A', 'B', 'C', 'D']
    >>> list(unique_everseen('ABBcCAD', str.casefold))
    ['A', 'B', 'c', 'D']
    >>> # Xác minh rằng đầu vào được tiêu thụ theo kiểu lazy
    >>> input_iterator = iter('AAAABBBCCDAABBB')
    >>> output_iterator = unique_everseen(input_iterator)
    >>> next(output_iterator)
    'A'
    >>> ''.join(input_iterator)
    'AAABBBCCDAABBB'


    >>> list(unique_justseen('AAAABBBCCDAABBB'))
    ['A', 'B', 'C', 'D', 'A', 'B']
    >>> list(unique_justseen('ABBCcAD', str.casefold))
    ['A', 'B', 'C', 'A', 'D']
    >>> list(unique_justseen('ABBcCAD', str.casefold))
    ['A', 'B', 'c', 'A', 'D']
    >>> # Xác minh rằng đầu vào được tiêu thụ theo kiểu lazy
    >>> input_iterator = iter('AAAABBBCCDAABBB')
    >>> output_iterator = unique_justseen(input_iterator)
    >>> next(output_iterator)
    'A'
    >>> ''.join(input_iterator)
    'AAABBBCCDAABBB'


    >>> list(unique([[1, 2], [3, 4], [1, 2]]))
    [[1, 2], [3, 4]]
    >>> list(unique('ABBcCAD', str.casefold))
    ['A', 'B', 'c', 'D']
    >>> list(unique('ABBcCAD', str.casefold, reverse=True))
    ['D', 'c', 'B', 'A']


    >>> d = dict(a=1, b=2, c=3)
    >>> it = iter_except(d.popitem, KeyError)
    >>> d['d'] = 4
    >>> next(it)
    ('d', 4)
    >>> next(it)
    ('c', 3)
    >>> next(it)
    ('b', 2)
    >>> d['e'] = 5
    >>> next(it)
    ('e', 5)
    >>> next(it)
    ('a', 1)
    >>> next(it, 'empty')
    'empty'


    >>> first_true('ABC0DEF1', '9', str.isdigit)
    '0'
    >>> # Xác minh rằng các đầu vào được tiêu thụ một cách lười biếng
    >>> it = iter('ABC0DEF1')
    >>> first_true(it, predicate=str.isdigit)
    '0'
    >>> ''.join(it)
    'DEF1'

    >>> multinomial(5, 2, 2, 1, 1)
    83160
    >>> word = 'coffee'
    >>> multinomial(*Counter(word).values()) == len(set(permutations(word)))
    True


    >>> list(running_mean([8.5, 9.5, 7.5, 6.5]))
    [8.5, 9.0, 8.5, 8.0]
    >>> list(running_mean([37, 33, 38, 28]))
    [37.0, 35.0, 36.0, 34.0]


    >>> list(running_min([37, 33, 38, 28]))
    [37, 33, 33, 28]


    >>> list(running_max([37, 33, 38, 28]))
    [37, 37, 38, 38]


    >>> list(running_median([37, 33, 38, 28]))
    [37, 35.0, 37, 35.0]


    >>> list(running_statistics([37, 33, 38, 28]))
    [(1, 37, 37, 37, 37.0), (2, 33, 35.0, 37, 35.0), (3, 33, 37, 38, 36.0), (4, 28, 35.0, 38, 34.0)]


.. testcode::
    :hide:

    # Các công thức cũ và các bài kiểm thử của chúng được đảm bảo sẽ tiếp tục hoạt động.

    def tabulate(function, start=0):
        "Return function(0), function(1), ..."
        return map(function, count(start))

    def old_sumprod_recipe(vec1, vec2):
        "Compute a sum of products."
        return sum(starmap(operator.mul, zip(vec1, vec2, strict=True)))

    def dotproduct(vec1, vec2):
        return sum(map(operator.mul, vec1, vec2))

    def pad_none(iterable):
        """Returns the sequence elements and then returns None indefinitely.

        Useful for emulating the behavior of the built-in map() function.
        """
        return chain(iterable, repeat(None))

    def triplewise(iterable):
        "Return overlapping triplets from an iterable"
        # triplewise('ABCDEFG') → ABC BCD CDE DEF EFG
        for (a, _), (b, c) in pairwise(pairwise(iterable)):
            yield a, b, c

    def nth_combination(iterable, r, index):
        "Equivalent to list(combinations(iterable, r))[index]"
        pool = tuple(iterable)
        n = len(pool)
        c = math.comb(n, r)
        if index < 0:
            index += c
        if index < 0 or index >= c:
            raise IndexError
        result = []
        while r:
            c, n, r = c*r//n, n-1, r-1
            while index >= c:
                index -= c
                c, n = c*(n-r)//n, n-1
            result.append(pool[-1-n])
        return tuple(result)

    def before_and_after(predicate, it):
       """ Variant of takewhile() that allows complete
           access to the remainder of the iterator.

           >>> it = iter('ABCdEfGhI')
           >>> all_upper, remainder = before_and_after(str.isupper, it)
           >>> ''.join(all_upper)
           'ABC'
           >>> ''.join(remainder)     # takewhile() sẽ làm mất chữ 'd'
           'dEfGhI'

           Note that the true iterator must be fully consumed
           before the remainder iterator can generate valid results.
       """
       it = iter(it)
       transition = []

       def true_iterator():
           for elem in it:
               if predicate(elem):
                   yield elem
               else:
                   transition.append(elem)
                   return

       return true_iterator(), chain(transition, it)

    def partition(predicate, iterable):
        """Partition entries into false entries and true entries.

        If *predicate* is slow, consider wrapping it with functools.lru_cache().
        """
        # partition(is_odd, range(10)) → 0 2 4 6 8   và  1 3 5 7 9
        t1, t2 = tee(iterable)
        return filterfalse(predicate, t1), filter(predicate, t2)



.. doctest::
    :hide:

    >>> list(islice(tabulate(lambda x: 2*x), 4))
    [0, 2, 4, 6]


    >>> dotproduct([1,2,3], [4,5,6])
    32


    >>> old_sumprod_recipe([1,2,3], [4,5,6])
    32


    >>> list(islice(pad_none('abc'), 0, 6))
    ['a', 'b', 'c', None, None, None]


    >>> list(triplewise('ABCDEFG'))
    [('A', 'B', 'C'), ('B', 'C', 'D'), ('C', 'D', 'E'), ('D', 'E', 'F'), ('E', 'F', 'G')]


    >>> population = 'ABCDEFGH'
    >>> for r in range(len(population) + 1):
    ...     seq = list(combinations(population, r))
    ...     for i in range(len(seq)):
    ...         assert nth_combination(population, r, i) == seq[i]
    ...     for i in range(-len(seq), 0):
    ...         assert nth_combination(population, r, i) == seq[i]
    ...
    >>> iterable = 'abcde'
    >>> r = 3
    >>> combos = list(combinations(iterable, r))
    >>> all(nth_combination(iterable, r, i) == comb for i, comb in enumerate(combos))
    True


    >>> it = iter('ABCdEfGhI')
    >>> all_upper, remainder = before_and_after(str.isupper, it)
    >>> ''.join(all_upper)
    'ABC'
    >>> ''.join(remainder)
    'dEfGhI'


    >>> def is_odd(x):
    ...     return x % 2 == 1
    ...
    >>> evens, odds = partition(is_odd, range(10))
    >>> list(evens)
    [0, 2, 4, 6, 8]
    >>> list(odds)
    [1, 3, 5, 7, 9]
    >>> # Xác minh rằng đầu vào được tiêu thụ theo kiểu lazy
    >>> input_iterator = iter(range(10))
    >>> evens, odds = partition(is_odd, input_iterator)
    >>> next(odds)
    1
    >>> next(odds)
    3
    >>> next(evens)
    0
    >>> list(input_iterator)
    [4, 5, 6, 7, 8, 9]

.. _`amortization table`: https://www.ramseysolutions.com/real-estate/amortization-schedule
.. _`permutations of elements`: https://www.britannica.com/science/permutation
.. _`Cartesian product`: https://en.wikipedia.org/wiki/Cartesian_product
.. _`functional style`: https://www.cs.kent.ac.uk/people/staff/dat/miranda/whyfp90.pdf
