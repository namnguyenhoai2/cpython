:mod:`!operator` --- Các toán tử chuẩn dưới dạng hàm
====================================================

.. module:: operator
   :synopsis: Các hàm tương ứng với những toán tử chuẩn.

.. sectionauthor:: Skip Montanaro <skip@automatrix.com>

**Mã nguồn:** :source:`Lib/operator.py`

.. testsetup::

   import operator
   from operator import itemgetter, iadd

--------------

Mô-đun :mod:`!operator` xuất ra một tập hợp các hàm hiệu quả tương ứng với những toán tử tích hợp sẵn của Python. Ví dụ, ``operator.add(x, y)`` tương đương với biểu thức ``x+y``. Nhiều tên hàm là tên được sử dụng cho các special method, nhưng không có dấu gạch dưới kép. Để duy trì khả năng tương thích ngược, nhiều hàm trong số này có một biến thể vẫn giữ lại dấu gạch dưới kép. Các biến thể không có dấu gạch dưới kép được ưu tiên vì tính rõ ràng.

Các hàm được chia thành những nhóm thực hiện so sánh đối tượng, thao tác logic, thao tác toán học và thao tác trên sequence.

Các hàm so sánh đối tượng hữu ích cho mọi đối tượng và được đặt tên theo những toán tử so sánh mở rộng mà chúng hỗ trợ:


.. function:: lt(a, b)
              le(a, b) eq(a, b) ne(a, b) ge(a, b) gt(a, b) __lt__(a, b) __le__(a, b) __eq__(a, b) __ne__(a, b) __ge__(a, b) __gt__(a, b)

   Thực hiện “các phép so sánh nâng cao (rich comparisons)” giữa *a* và *b*. Cụ thể, ``lt(a, b)`` tương đương với ``a < b``, ``le(a, b)`` tương đương với ``a <= b``, ``eq(a, b)`` tương đương với ``a == b``, ``ne(a, b)`` tương đương với ``a != b``, ``gt(a, b)`` tương đương với ``a > b`` và ``ge(a, b)`` tương đương với ``a >= b``. Lưu ý rằng các hàm này có thể trả về bất kỳ giá trị nào, và giá trị đó có thể được diễn giải thành giá trị Boolean hoặc không. Xem
   :ref:`comparisons` để biết thêm thông tin về các phép so sánh nâng cao.


Các phép toán logic nhìn chung cũng áp dụng được cho mọi đối tượng, đồng thời hỗ trợ kiểm tra tính đúng sai, kiểm tra định danh và các phép toán Boolean:


.. function:: not_(obj)
              __not__(obj)

   Trả về kết quả của :keyword:`not` *obj*. (Lưu ý rằng không có
   :meth:`!__not__` phương thức cho các thực thể đối tượng; chỉ lõi trình thông dịch định nghĩa phép toán này. Kết quả bị ảnh hưởng bởi các phương thức :meth:`~object.__bool__` và
   :meth:`~object.__len__`.)


.. function:: truth(obj)

   Trả về :const:`True` nếu *obj* là true, và :const:`False` nếu không. Điều này tương đương với việc sử dụng constructor :class:`bool`.


.. function:: is_(a, b)

   Trả về ``a is b``. Kiểm tra object identity.


.. function:: is_not(a, b)

   Trả về ``a is not b``. Kiểm tra object identity.


.. function:: is_none(a)

   Trả về ``a is None``. Kiểm tra object identity.

   .. versionadded:: 3.14


.. function:: is_not_none(a)

   Trả về ``a is not None``. Kiểm tra object identity.

   .. versionadded:: 3.14


Các phép toán số học và bitwise là nhiều nhất:


.. function:: abs(obj)
              __abs__(obj)

   Trả về giá trị tuyệt đối của *obj*.


.. function:: add(a, b)
              __add__(a, b)

   Trả về ``a + b``, với *a* và *b* là các số.


.. function:: and_(a, b)
              __and__(a, b)

   Trả về ``a & b``.


.. function:: floordiv(a, b)
              __floordiv__(a, b)

   Trả về ``a // b``.


.. function:: index(a)
              __index__(a)

   Trả về *a* được chuyển đổi thành số nguyên. Tương đương với ``a.__index__()``.

   .. versionchanged:: 3.10
      Kết quả luôn có kiểu chính xác là :class:`int`. Trước đây, kết quả có thể là một instance của lớp con của ``int``.


.. function:: inv(obj)
              invert(obj) __inv__(obj) __invert__(obj)

   Trả về ``~obj``.


.. function:: lshift(a, b)
              __lshift__(a, b)

   Trả về ``a << b``.


.. function:: mod(a, b)
              __mod__(a, b)

   Trả về ``a % b``.


.. function:: mul(a, b)
              __mul__(a, b)

   Trả về ``a * b``.


.. function:: matmul(a, b)
              __matmul__(a, b)

   Trả về ``a @ b``.

   .. versionadded:: 3.5


.. function:: neg(obj)
              __neg__(obj)

   Trả về *obj* đã được phủ định (``-obj``).


.. function:: or_(a, b)
              __or__(a, b)

   Trả về ``a | b``.


.. function:: pos(obj)
              __pos__(obj)

   Trả về ``+obj``.


.. function:: pow(a, b)
              __pow__(a, b)

   Trả về ``a ** b``.


.. function:: rshift(a, b)
              __rshift__(a, b)

   Trả về ``a >> b``.


.. function:: sub(a, b)
              __sub__(a, b)

   Trả về ``a - b``.


.. function:: truediv(a, b)
              __truediv__(a, b)

   Trả về ``a / b``, trong đó 2/3 là .66 thay vì 0. Đây còn được gọi là phép chia "true".


.. function:: xor(a, b)
              __xor__(a, b)

   Trả về ``a ^ b``.


Các phép toán hoạt động với sequence (một số trong đó cũng hoạt động với mapping) bao gồm:

.. function:: concat(a, b)
              __concat__(a, b)

   Trả về ``a + b`` cho *a* và *b*, cả hai đều là sequence.


.. function:: contains(a, b)
              __contains__(a, b)

   Trả về kết quả của phép kiểm tra ``b in a``. Lưu ý rằng các toán hạng bị đảo ngược.


.. function:: countOf(a, b)

   Trả về số lần xuất hiện của *b* trong *a*.


.. function:: delitem(a, b)
              __delitem__(a, b)

   Xóa giá trị của *a* tại chỉ mục *b*.


.. function:: getitem(a, b)
              __getitem__(a, b)

   Trả về giá trị của *a* tại chỉ mục *b*.


.. function:: indexOf(a, b)

   Trả về chỉ mục của lần xuất hiện đầu tiên của *b* trong *a*.


.. function:: setitem(a, b, c)
              __setitem__(a, b, c)

   Đặt giá trị của *a* tại chỉ mục *b* thành *c*.


.. function:: length_hint(obj, default=0)

   Trả về độ dài ước tính của đối tượng *obj*. Trước tiên, hãy thử trả về độ dài thực tế của đối tượng, sau đó là giá trị ước tính bằng :meth:`object.__length_hint__`, và cuối cùng trả về giá trị mặc định.

   .. versionadded:: 3.4


Thao tác sau đây làm việc với các callable:

.. function:: call(obj, /, *args, **kwargs)
              __call__(obj, /, *args, **kwargs)

   Trả về ``obj(*args, **kwargs)``.

   .. versionadded:: 3.11


Mô-đun :mod:`!operator` cũng định nghĩa các công cụ để tra cứu thuộc tính và mục tổng quát. Những công cụ này hữu ích để tạo các field extractor nhanh làm đối số cho
:func:`map`, :func:`sorted`, :meth:`itertools.groupby`, hoặc các hàm khác yêu cầu một đối số hàm.


.. function:: attrgetter(attr)
              attrgetter(*attrs)

   Trả về một đối tượng có thể gọi để lấy *attr* từ toán hạng của nó. Nếu yêu cầu nhiều thuộc tính, hàm sẽ trả về một tuple các thuộc tính. Tên thuộc tính cũng có thể chứa dấu chấm. Ví dụ:

   * Sau ``f = attrgetter('name')``, lệnh gọi ``f(b)`` trả về ``b.name``.

   * Sau ``f = attrgetter('name', 'date')``, lệnh gọi ``f(b)`` trả về ``(b.name, b.date)``.

   * Sau ``f = attrgetter('name.first', 'name.last')``, lệnh gọi ``f(b)`` trả về ``(b.name.first, b.name.last)``.

   Tương đương với::

      def attrgetter(*items):
          if any(not isinstance(item, str) for item in items):
              raise TypeError('attribute name must be a string')
          if len(items) == 1:
              attr = items[0]
              def g(obj):
                  return resolve_attr(obj, attr)
          else:
              def g(obj):
                  return tuple(resolve_attr(obj, attr) for attr in items)
          return g

      def resolve_attr(obj, attr):
          for name in attr.split("."):
              obj = getattr(obj, name)
          return obj


.. function:: itemgetter(item)
              itemgetter(*items)

   Trả về một đối tượng có thể gọi để lấy *item* từ toán hạng của nó bằng phương thức :meth:`~object.__getitem__` của toán hạng. Nếu chỉ định nhiều item, hàm sẽ trả về một tuple các giá trị tra cứu. Ví dụ:

   * Sau ``f = itemgetter(2)``, lệnh gọi ``f(r)`` trả về ``r[2]``.

   * Sau ``g = itemgetter(2, 5, 3)``, lệnh gọi ``g(r)`` trả về ``(r[2], r[5], r[3])``.

   Tương đương với::

      def itemgetter(*items):
          if len(items) == 1:
              item = items[0]
              def g(obj):
                  return obj[item]
          else:
              def g(obj):
                  return tuple(obj[item] for item in items)
          return g

   Các mục có thể thuộc bất kỳ kiểu nào được phương thức :meth:`~object.__getitem__` của toán hạng chấp nhận. Từ điển chấp nhận mọi giá trị :term:`hashable`. Danh sách, tuple và chuỗi chấp nhận một chỉ mục hoặc một lát cắt:

      >>> itemgetter(1)('ABCDEFG')
      'B'
      >>> itemgetter(1, 3, 5)('ABCDEFG')
      ('B', 'D', 'F')
      >>> itemgetter(slice(2, None))('ABCDEFG')
      'CDEFG'
      >>> soldier = dict(rank='captain', name='dotterbart')
      >>> itemgetter('rank')(soldier)
      'captain'

   Ví dụ sử dụng :func:`itemgetter` để lấy các trường cụ thể từ một bản ghi tuple:

      >>> inventory = [('apple', 3), ('banana', 2), ('pear', 5), ('orange', 1)]
      >>> getcount = itemgetter(1)
      >>> list(map(getcount, inventory))
      [3, 2, 5, 1]
      >>> sorted(inventory, key=getcount)
      [('orange', 1), ('banana', 2), ('apple', 3), ('pear', 5)]


.. function:: methodcaller(name, /, *args, **kwargs)

   Trả về một đối tượng có thể gọi, đối tượng này gọi phương thức *name* trên toán hạng của nó. Nếu cung cấp thêm các đối số và/hoặc đối số từ khóa, chúng cũng sẽ được truyền cho phương thức. Ví dụ:

   * Sau ``f = methodcaller('name')``, lệnh gọi ``f(b)`` trả về ``b.name()``.

   * Sau ``f = methodcaller('name', 'foo', bar=1)``, lệnh gọi ``f(b)`` trả về ``b.name('foo', bar=1)``.

   Tương đương với::

      def methodcaller(name, /, *args, **kwargs):
          def caller(obj):
              return getattr(obj, name)(*args, **kwargs)
          return caller


.. _operator-map:

Ánh xạ toán tử thành hàm
------------------------

Bảng này cho thấy các phép toán trừu tượng tương ứng với các ký hiệu toán tử trong cú pháp Python và các hàm trong mô-đun :mod:`!operator`.

+----------------------------------+-----------------------+---------------------------------------+
| Phép toán                        | Cú pháp               | Hàm                                   |
+==================================+=======================+=======================================+
| Phép cộng                        | ``a + b``             | ``add(a, b)``                         |
+----------------------------------+-----------------------+---------------------------------------+
| Phép nối                         | ``seq1 + seq2``       | ``concat(seq1, seq2)``                |
+----------------------------------+-----------------------+---------------------------------------+
| Kiểm tra chứa                    | ``obj in seq``        | ``contains(seq, obj)``                |
+----------------------------------+-----------------------+---------------------------------------+
| Phép chia                        | ``a / b``             | ``truediv(a, b)``                     |
+----------------------------------+-----------------------+---------------------------------------+
| Phép chia                        | ``a // b``            | ``floordiv(a, b)``                    |
+----------------------------------+-----------------------+---------------------------------------+
| Phép AND bit, hoặc phép giao     | ``a & b``             | ``and_(a, b)``                        |
+----------------------------------+-----------------------+---------------------------------------+
| Phép XOR bit, hoặc hiệu đối xứng | ``a ^ b``             | ``xor(a, b)``                         |
+----------------------------------+-----------------------+---------------------------------------+
| Đảo bit, hay phép bù             | ``~ a``               | ``invert(a)``                         |
+----------------------------------+-----------------------+---------------------------------------+
| Phép OR bit, hay phép hợp        | ``a | b``             | ``or_(a, b)``                         |
+----------------------------------+-----------------------+---------------------------------------+
| Lũy thừa                         | ``a ** b``            | ``pow(a, b)``                         |
+----------------------------------+-----------------------+---------------------------------------+
| Phép đồng nhất                   | ``a is b``            | ``is_(a, b)``                         |
+----------------------------------+-----------------------+---------------------------------------+
| Phép đồng nhất                   | ``a is not b``        | ``is_not(a, b)``                      |
+----------------------------------+-----------------------+---------------------------------------+
| Phép đồng nhất                   | ``a is None``         | ``is_none(a)``                        |
+----------------------------------+-----------------------+---------------------------------------+
| Phép đồng nhất                   | ``a is not None``     | ``is_not_none(a)``                    |
+----------------------------------+-----------------------+---------------------------------------+
| Gán theo chỉ mục                 | ``obj[k] = v``        | ``setitem(obj, k, v)``                |
+----------------------------------+-----------------------+---------------------------------------+
| Xóa theo chỉ mục                 | ``del obj[k]``        | ``delitem(obj, k)``                   |
+----------------------------------+-----------------------+---------------------------------------+
| Lập chỉ mục                      | ``obj[k]``            | ``getitem(obj, k)``                   |
+----------------------------------+-----------------------+---------------------------------------+
| Dịch trái                        | ``a << b``            | ``lshift(a, b)``                      |
+----------------------------------+-----------------------+---------------------------------------+
| Phép modulo                      | ``a % b``             | ``mod(a, b)``                         |
+----------------------------------+-----------------------+---------------------------------------+
| Phép nhân                        | ``a * b``             | ``mul(a, b)``                         |
+----------------------------------+-----------------------+---------------------------------------+
| Phép nhân ma trận                | ``a @ b``             | ``matmul(a, b)``                      |
+----------------------------------+-----------------------+---------------------------------------+
| Phép lấy đối (số học)            | ``- a``               | ``neg(a)``                            |
+----------------------------------+-----------------------+---------------------------------------+
| Phép phủ định (logic)            | ``not a``             | ``not_(a)``                           |
+----------------------------------+-----------------------+---------------------------------------+
| Số dương                         | ``+ a``               | ``pos(a)``                            |
+----------------------------------+-----------------------+---------------------------------------+
| Dịch phải                        | ``a >> b``            | ``rshift(a, b)``                      |
+----------------------------------+-----------------------+---------------------------------------+
| Gán lát cắt                      | ``seq[i:j] = values`` | ``setitem(seq, slice(i, j), values)`` |
+----------------------------------+-----------------------+---------------------------------------+
| Xóa lát cắt                      | ``del seq[i:j]``      | ``delitem(seq, slice(i, j))``         |
+----------------------------------+-----------------------+---------------------------------------+
| Lát cắt                          | ``seq[i:j]``          | ``getitem(seq, slice(i, j))``         |
+----------------------------------+-----------------------+---------------------------------------+
| Định dạng chuỗi                  | ``s % obj``           | ``mod(s, obj)``                       |
+----------------------------------+-----------------------+---------------------------------------+
| Phép trừ                         | ``a - b``             | ``sub(a, b)``                         |
+----------------------------------+-----------------------+---------------------------------------+
| Kiểm tra giá trị đúng            | ``obj``               | ``truth(obj)``                        |
+----------------------------------+-----------------------+---------------------------------------+
| Thứ tự                           | ``a < b``             | ``lt(a, b)``                          |
+----------------------------------+-----------------------+---------------------------------------+
| Thứ tự                           | ``a <= b``            | ``le(a, b)``                          |
+----------------------------------+-----------------------+---------------------------------------+
| So sánh bằng                     | ``a == b``            | ``eq(a, b)``                          |
+----------------------------------+-----------------------+---------------------------------------+
| Hiệu                             | ``a != b``            | ``ne(a, b)``                          |
+----------------------------------+-----------------------+---------------------------------------+
| Thứ tự                           | ``a >= b``            | ``ge(a, b)``                          |
+----------------------------------+-----------------------+---------------------------------------+
| Thứ tự                           | ``a > b``             | ``gt(a, b)``                          |
+----------------------------------+-----------------------+---------------------------------------+

Toán tử tại chỗ
---------------

Nhiều phép toán có một phiên bản "tại chỗ". Dưới đây là các hàm cung cấp cách truy cập nguyên thủy hơn vào các toán tử tại chỗ so với cú pháp thông thường; ví dụ, :term:`statement` ``x += y`` tương đương với ``x = operator.iadd(x, y)``. Nói cách khác, có thể nói rằng ``z = operator.iadd(x, y)`` tương đương với câu lệnh ghép ``z = x; z += y``.

Trong các ví dụ đó, hãy lưu ý rằng khi một phương thức tại chỗ được gọi, việc tính toán và phép gán được thực hiện trong hai bước riêng biệt. Các hàm tại chỗ được liệt kê dưới đây chỉ thực hiện bước đầu tiên, đó là gọi phương thức tại chỗ. Bước thứ hai, phép gán, không được xử lý.

Đối với các đích bất biến như chuỗi, số và tuple, giá trị được cập nhật sẽ được tính toán nhưng không được gán trở lại biến đầu vào:

>>> a = 'hello'
>>> iadd(a, ' world')
'hello world'
>>> a
'hello'

Đối với các đích khả biến như list và dictionary, phương thức tại chỗ sẽ thực hiện việc cập nhật, vì vậy không cần phép gán tiếp theo:

>>> s = ['h', 'e', 'l', 'l', 'o']
>>> iadd(s, [' ', 'w', 'o', 'r', 'l', 'd'])
['h', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd']
>>> s
['h', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd']

.. function:: iadd(a, b)
              __iadd__(a, b)

   ``a = iadd(a, b)`` tương đương với ``a += b``.


.. function:: iand(a, b)
              __iand__(a, b)

   ``a = iand(a, b)`` tương đương với ``a &= b``.


.. function:: iconcat(a, b)
              __iconcat__(a, b)

   ``a = iconcat(a, b)`` tương đương với ``a += b`` đối với các sequence *a* và *b*.


.. function:: ifloordiv(a, b)
              __ifloordiv__(a, b)

   ``a = ifloordiv(a, b)`` tương đương với ``a //= b``.


.. function:: ilshift(a, b)
              __ilshift__(a, b)

   ``a = ilshift(a, b)`` tương đương với ``a <<= b``.


.. function:: imod(a, b)
              __imod__(a, b)

   ``a = imod(a, b)`` tương đương với ``a %= b``.


.. function:: imul(a, b)
              __imul__(a, b)

   ``a = imul(a, b)`` tương đương với ``a *= b``.


.. function:: imatmul(a, b)
              __imatmul__(a, b)

   ``a = imatmul(a, b)`` tương đương với ``a @= b``.

   .. versionadded:: 3.5


.. function:: ior(a, b)
              __ior__(a, b)

   ``a = ior(a, b)`` tương đương với ``a |= b``.


.. function:: ipow(a, b)
              __ipow__(a, b)

   ``a = ipow(a, b)`` tương đương với ``a **= b``.


.. function:: irshift(a, b)
              __irshift__(a, b)

   ``a = irshift(a, b)`` tương đương với ``a >>= b``.


.. function:: isub(a, b)
              __isub__(a, b)

   ``a = isub(a, b)`` tương đương với ``a -= b``.


.. function:: itruediv(a, b)
              __itruediv__(a, b)

   ``a = itruediv(a, b)`` tương đương với ``a /= b``.


.. function:: ixor(a, b)
              __ixor__(a, b)

   ``a = ixor(a, b)`` tương đương với ``a ^= b``.
