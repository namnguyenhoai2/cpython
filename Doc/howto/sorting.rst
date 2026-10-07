.. _sortinghowto:

Các kỹ thuật sắp xếp
********************

:Author: Andrew Dalke và Raymond Hettinger


Các list trong Python có sẵn phương thức :meth:`list.sort` để sửa đổi list ngay tại chỗ. Ngoài ra còn có hàm tích hợp :func:`sorted` để tạo một list mới đã được sắp xếp từ một iterable.

Trong tài liệu này, chúng ta tìm hiểu các kỹ thuật khác nhau để sắp xếp dữ liệu bằng Python.


Kiến thức cơ bản về sắp xếp
===========================

Sắp xếp tăng dần đơn giản rất dễ: chỉ cần gọi hàm :func:`sorted`. Hàm này trả về một list mới đã được sắp xếp:

.. doctest::

    >>> sorted([5, 2, 3, 1, 4])
    [1, 2, 3, 4, 5]

Bạn cũng có thể sử dụng phương thức :meth:`list.sort`. Phương thức này sửa đổi list ngay tại chỗ (và trả về ``None`` để tránh nhầm lẫn). Thông thường, cách này kém tiện lợi hơn :func:`sorted` - nhưng nếu bạn không cần list ban đầu thì hiệu quả hơn một chút.

.. doctest::

    >>> a = [5, 2, 3, 1, 4]
    >>> a.sort()
    >>> a
    [1, 2, 3, 4, 5]

Một điểm khác biệt nữa là phương thức :meth:`list.sort` chỉ được định nghĩa cho các list. Ngược lại, hàm :func:`sorted` chấp nhận mọi iterable.

.. doctest::

    >>> sorted({1: 'D', 2: 'B', 3: 'B', 4: 'E', 5: 'A'})
    [1, 2, 3, 4, 5]

Các hàm key
===========

Phương thức :meth:`list.sort` và các hàm :func:`sorted`,
:func:`min`, :func:`max`, :func:`heapq.nsmallest`, và
:func:`heapq.nlargest` có tham số *key* để chỉ định một hàm (hoặc callable khác) được gọi trên từng phần tử của list trước khi thực hiện so sánh.

Ví dụ: sau đây là phép so sánh chuỗi không phân biệt chữ hoa chữ thường sử dụng
:meth:`str.casefold`:

.. doctest::

    >>> sorted("This is a test string from Andrew".split(), key=str.casefold)
    ['a', 'Andrew', 'from', 'is', 'string', 'test', 'This']

Giá trị của tham số *key* phải là một hàm (hoặc callable khác) nhận một đối số duy nhất và trả về một key được dùng cho mục đích sắp xếp. Kỹ thuật này nhanh vì hàm key được gọi chính xác một lần cho mỗi bản ghi đầu vào.

Một mẫu phổ biến là sắp xếp các đối tượng phức tạp bằng cách sử dụng một số chỉ mục của đối tượng làm khóa. Ví dụ:

.. doctest::

    >>> student_tuples = [
    ...     ('john', 'A', 15),
    ...     ('jane', 'B', 12),
    ...     ('dave', 'B', 10),
    ... ]
    >>> sorted(student_tuples, key=lambda student: student[2])   # sắp xếp theo tuổi
    [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

Kỹ thuật tương tự cũng áp dụng cho các đối tượng có thuộc tính được đặt tên. Ví dụ:

.. doctest::

    >>> class Student:
    ...     def __init__(self, name, grade, age):
    ...         self.name = name
    ...         self.grade = grade
    ...         self.age = age
    ...     def __repr__(self):
    ...         return repr((self.name, self.grade, self.age))

    >>> student_objects = [
    ...     Student('john', 'A', 15),
    ...     Student('jane', 'B', 12),
    ...     Student('dave', 'B', 10),
    ... ]
    >>> sorted(student_objects, key=lambda student: student.age)   # sắp xếp theo tuổi
    [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

Các đối tượng có thuộc tính được đặt tên có thể được tạo bằng một lớp thông thường như đã trình bày ở trên, hoặc có thể là các thể hiện của :class:`~dataclasses.dataclass` hoặc một :term:`named tuple`.

Các hàm của module Operator và đánh giá hàm từng phần
=====================================================

Các mẫu :term:`key function` được trình bày ở trên rất phổ biến, vì vậy Python cung cấp các hàm tiện ích để việc tạo các hàm accessor trở nên dễ dàng và nhanh hơn. Các
Mô-đun :mod:`operator` có :func:`~operator.itemgetter`,
:func:`~operator.attrgetter`, và một hàm :func:`~operator.methodcaller`.

Với các hàm đó, những ví dụ trên trở nên đơn giản và nhanh hơn:

.. doctest::

    >>> from operator import itemgetter, attrgetter

    >>> sorted(student_tuples, key=itemgetter(2))
    [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

    >>> sorted(student_objects, key=attrgetter('age'))
    [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

Các hàm của mô-đun operator cho phép sắp xếp theo nhiều cấp. Ví dụ, để sắp xếp theo *grade* rồi theo *age*:

.. doctest::

    >>> sorted(student_tuples, key=itemgetter(1,2))
    [('john', 'A', 15), ('dave', 'B', 10), ('jane', 'B', 12)]

    >>> sorted(student_objects, key=attrgetter('grade', 'age'))
    [('john', 'A', 15), ('dave', 'B', 10), ('jane', 'B', 12)]

Mô-đun :mod:`functools` cung cấp một công cụ hữu ích khác để tạo các hàm khóa. Hàm :func:`~functools.partial` có thể giảm `arity <https://en.wikipedia.org/wiki/Arity>`_ của một hàm có nhiều đối số, khiến hàm đó phù hợp để dùng làm hàm khóa.

.. doctest::

    >>> from functools import partial
    >>> from unicodedata import normalize

    >>> names = 'Zoë Åbjørn Núñez Élana Zeke Abe Nubia Eloise'.split()

    >>> sorted(names, key=partial(normalize, 'NFD'))
    ['Abe', 'Åbjørn', 'Eloise', 'Élana', 'Nubia', 'Núñez', 'Zeke', 'Zoë']

    >>> sorted(names, key=partial(normalize, 'NFC'))
    ['Abe', 'Eloise', 'Nubia', 'Núñez', 'Zeke', 'Zoë', 'Åbjørn', 'Élana']

Tăng dần và giảm dần
====================

Cả :meth:`list.sort` và :func:`sorted` đều chấp nhận tham số *reverse* có giá trị boolean. Tham số này được dùng để đánh dấu việc sắp xếp giảm dần. Ví dụ, để lấy dữ liệu sinh viên theo thứ tự *age* ngược lại:

.. doctest::

    >>> sorted(student_tuples, key=itemgetter(2), reverse=True)
    [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]

    >>> sorted(student_objects, key=attrgetter('age'), reverse=True)
    [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]

Tính ổn định của phép sắp xếp và các phép sắp xếp phức tạp
==========================================================

Các phép sắp xếp được đảm bảo là `ổn định <https://en.wikipedia.org/wiki/Sorting_algorithm#Stability>`_\. Điều đó có nghĩa là khi nhiều bản ghi có cùng khóa, thứ tự ban đầu của chúng được giữ nguyên.

.. doctest::

    >>> data = [('red', 1), ('blue', 1), ('red', 2), ('blue', 2)]
    >>> sorted(data, key=itemgetter(0))
    [('blue', 1), ('blue', 2), ('red', 1), ('red', 2)]

Hãy chú ý cách hai bản ghi cho *blue* giữ nguyên thứ tự ban đầu, vì vậy ``('blue', 1)`` được đảm bảo đứng trước ``('blue', 2)``.

Thuộc tính tuyệt vời này cho phép bạn xây dựng các phép sắp xếp phức tạp qua một chuỗi bước sắp xếp. Ví dụ: để sắp xếp dữ liệu sinh viên theo *grade* giảm dần rồi theo *age* tăng dần, trước tiên hãy thực hiện phép sắp xếp *age*, sau đó sắp xếp lại bằng *grade*:

.. doctest::

    >>> s = sorted(student_objects, key=attrgetter('age'))     # sắp xếp theo khóa phụ
    >>> sorted(s, key=attrgetter('grade'), reverse=True)       # bây giờ sắp xếp theo khóa chính, theo thứ tự giảm dần
    [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

Điều này có thể được trừu tượng hóa thành một hàm wrapper nhận một danh sách và các tuple gồm trường cùng thứ tự để sắp xếp chúng qua nhiều lượt.

.. doctest::

    >>> def multisort(xs, specs):
    ...     for key, reverse in reversed(specs):
    ...         xs.sort(key=attrgetter(key), reverse=reverse)
    ...     return xs

    >>> multisort(list(student_objects), (('grade', True), ('age', False)))
    [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

Thuật toán `Timsort <https://en.wikipedia.org/wiki/Timsort>`_ được sử dụng trong Python thực hiện nhiều lần sắp xếp một cách hiệu quả vì có thể tận dụng thứ tự đã có trong tập dữ liệu.

Decorate-Sort-Undecorate
========================

Idiom này được gọi là Decorate-Sort-Undecorate theo ba bước của nó:

* Trước tiên, danh sách ban đầu được bổ sung các giá trị mới để điều khiển thứ tự sắp xếp.

* Tiếp theo, danh sách đã được bổ sung giá trị sẽ được sắp xếp.

* Cuối cùng, các giá trị bổ sung được loại bỏ, tạo ra một danh sách chỉ chứa các giá trị ban đầu theo thứ tự mới.

Ví dụ, để sắp xếp dữ liệu sinh viên theo *grade* bằng phương pháp DSU:

.. doctest::

    >>> decorated = [(student.grade, i, student) for i, student in enumerate(student_objects)]
    >>> decorated.sort()
    >>> [student for grade, i, student in decorated]               # gỡ trang trí
    [('john', 'A', 15), ('jane', 'B', 12), ('dave', 'B', 10)]

Cách viết này hoạt động vì các tuple được so sánh theo thứ tự từ điển; các phần tử đầu tiên được so sánh; nếu chúng giống nhau thì các phần tử thứ hai được so sánh, và cứ tiếp tục như vậy.

Trong mọi trường hợp, không nhất thiết phải đưa chỉ mục *i* vào danh sách đã trang trí, nhưng việc đưa chỉ mục này vào mang lại hai lợi ích:

* Phép sắp xếp có tính ổn định -- nếu hai phần tử có cùng khóa, thứ tự của chúng sẽ được giữ nguyên trong danh sách đã sắp xếp.

* Các phần tử ban đầu không cần phải so sánh được vì thứ tự của các tuple đã trang trí sẽ được xác định bởi nhiều nhất là hai phần tử đầu tiên. Vì vậy, chẳng hạn, danh sách ban đầu có thể chứa các số phức, vốn không thể được sắp xếp trực tiếp.

Một tên gọi khác của cách viết này là `Schwartzian transform <https://en.wikipedia.org/wiki/Schwartzian_transform>`_\,, theo tên Randal L. Schwartz, người đã phổ biến cách này trong cộng đồng lập trình viên Perl.

Giờ đây, khi tính năng sắp xếp của Python cung cấp các key-function, kỹ thuật này không còn thường xuyên cần thiết.

Hàm so sánh
===========

Khác với các hàm key trả về một giá trị tuyệt đối để sắp xếp, hàm so sánh tính toán thứ tự tương đối của hai đầu vào.

Ví dụ, `cân thăng bằng <https://upload.wikimedia.org/wikipedia/commons/1/17/Balance_à_tabac_1850.JPG>`_ so sánh hai mẫu và cho biết thứ tự tương đối: nhẹ hơn, bằng nhau hoặc nặng hơn. Tương tự, một hàm so sánh như ``cmp(a, b)`` sẽ trả về giá trị âm nếu nhỏ hơn, bằng 0 nếu các đầu vào bằng nhau hoặc giá trị dương nếu lớn hơn.

Bạn thường gặp các hàm so sánh khi chuyển các thuật toán từ những ngôn ngữ khác. Ngoài ra, một số thư viện cung cấp các hàm so sánh như một phần API của chúng. Ví dụ, :func:`locale.strcoll` là một hàm so sánh.

Để đáp ứng những trường hợp đó, Python cung cấp
:class:`functools.cmp_to_key` để bọc hàm so sánh, giúp hàm này có thể được sử dụng như một hàm key::

    sorted(words, key=cmp_to_key(strcoll))  # thứ tự sắp xếp theo locale

Chiến lược xử lý các kiểu và giá trị không thể sắp xếp
======================================================

Khi sắp xếp, có thể phát sinh một số vấn đề về kiểu và giá trị. Sau đây là một số chiến lược có thể hữu ích:

* Chuyển đổi các kiểu đầu vào không thể so sánh thành chuỗi trước khi sắp xếp:

.. doctest::

   >>> data = ['twelve', '11', 10]
   >>> sorted(map(str, data))
   ['10', '11', 'twelve']

Điều này cần thiết vì hầu hết các phép so sánh giữa các kiểu đều phát sinh một
:exc:`TypeError`.

* Loại bỏ các giá trị đặc biệt trước khi sắp xếp:

.. doctest::

   >>> from math import isnan
   >>> from itertools import filterfalse
   >>> data = [3.3, float('nan'), 1.1, 2.2]
   >>> sorted(filterfalse(isnan, data))
   [1.1, 2.2, 3.3]

Điều này cần thiết vì tiêu chuẩn `IEEE-754 <https://en.wikipedia.org/wiki/IEEE_754>`_ quy định rằng, "Mọi NaN phải được so sánh là không có thứ tự với mọi thứ, kể cả chính nó."

Tương tự, ``None`` cũng có thể được loại bỏ khỏi các tập dữ liệu:

.. doctest::

   >>> data = [3.3, None, 1.1, 2.2]
   >>> sorted(x for x in data if x is not None)
   [1.1, 2.2, 3.3]

Điều này là cần thiết vì ``None`` không thể được so sánh với các kiểu khác.

* Chuyển các kiểu mapping thành danh sách các mục đã sắp xếp trước khi sắp xếp:

.. doctest::

   >>> data = [{'a': 1}, {'b': 2}]
   >>> sorted(data, key=lambda d: sorted(d.items()))
   [{'a': 1}, {'b': 2}]

Điều này là cần thiết vì phép so sánh dict với dict sẽ phát sinh một
:exc:`TypeError`.

* Chuyển các kiểu set thành danh sách đã sắp xếp trước khi sắp xếp:

.. doctest::

    >>> data = [{'a', 'b', 'c'}, {'b', 'c', 'd'}]
    >>> sorted(map(sorted, data))
    [['a', 'b', 'c'], ['b', 'c', 'd']]

Điều này là cần thiết vì các phần tử trong các kiểu set không có thứ tự xác định. Ví dụ: ``list({'a', 'b'})`` có thể tạo ra ``['a', 'b']`` hoặc ``['b', 'a']``.

Những điểm lặt vặt
==================

* Để sắp xếp nhận biết locale, hãy dùng :func:`locale.strxfrm` cho một hàm key hoặc
  Sử dụng :func:`locale.strcoll` cho một hàm so sánh. Điều này là cần thiết vì thứ tự sắp xếp "theo bảng chữ cái" có thể khác nhau giữa các nền văn hóa, ngay cả khi bảng chữ cái cơ bản giống nhau.

* Tham số *reverse* vẫn duy trì tính ổn định của phép sắp xếp (để các bản ghi có khóa bằng nhau giữ nguyên thứ tự ban đầu). Điều thú vị là có thể mô phỏng hiệu ứng đó mà không cần tham số này bằng cách sử dụng hàm :func:`reversed` tích hợp sẵn hai lần:

  .. doctest::

    >>> data = [('red', 1), ('blue', 1), ('red', 2), ('blue', 2)]
    >>> standard_way = sorted(data, key=itemgetter(0), reverse=True)
    >>> double_reversed = list(reversed(sorted(reversed(data), key=itemgetter(0))))
    >>> assert standard_way == double_reversed
    >>> standard_way
    [('red', 1), ('red', 2), ('blue', 1), ('blue', 2)]

* Các routine sắp xếp sử dụng ``<`` khi so sánh hai đối tượng. Vì vậy, bạn có thể dễ dàng thêm một thứ tự sắp xếp chuẩn cho một class bằng cách định nghĩa phương thức :meth:`~object.__lt__`:

  .. doctest::

    >>> Student.__lt__ = lambda self, other: self.age < other.age
    >>> sorted(student_objects)
    [('dave', 'B', 10), ('jane', 'B', 12), ('john', 'A', 15)]

  Tuy nhiên, lưu ý rằng ``<`` có thể chuyển sang sử dụng :meth:`~object.__gt__` nếu
  :meth:`~object.__lt__` chưa được triển khai (xem :func:`object.__lt__` để biết chi tiết về cơ chế). Để tránh những kết quả bất ngờ, :pep:`8` khuyến nghị triển khai cả sáu phương thức so sánh. Decorator :deco:`~functools.total_ordering` được cung cấp để giúp công việc đó dễ dàng hơn.

* Các key function không nhất thiết phải phụ thuộc trực tiếp vào những đối tượng đang được sắp xếp. Một key function cũng có thể truy cập các tài nguyên bên ngoài. Ví dụ, nếu điểm của sinh viên được lưu trong một dictionary, chúng có thể được dùng để sắp xếp một danh sách riêng gồm tên sinh viên:

  .. doctest::

    >>> students = ['dave', 'john', 'jane']
    >>> newgrades = {'john': 'F', 'jane':'A', 'dave': 'C'}
    >>> sorted(students, key=newgrades.__getitem__)
    ['jane', 'dave', 'john']

Các phép sắp xếp một phần
=========================

Một số ứng dụng chỉ yêu cầu sắp xếp một phần dữ liệu. Thư viện chuẩn cung cấp một số công cụ thực hiện ít công việc hơn so với sắp xếp toàn bộ:

* :func:`min` và :func:`max` lần lượt trả về các giá trị nhỏ nhất và lớn nhất. Các hàm này duyệt qua dữ liệu đầu vào một lần và hầu như không cần bộ nhớ phụ.

* :func:`heapq.nsmallest` và :func:`heapq.nlargest` lần lượt trả về *n* giá trị nhỏ nhất và lớn nhất. Các hàm này duyệt qua dữ liệu một lần và mỗi thời điểm chỉ giữ *n* phần tử trong bộ nhớ. Khi *n* nhỏ so với số lượng giá trị đầu vào, các hàm này thực hiện ít phép so sánh hơn nhiều so với sắp xếp toàn bộ.

* :func:`heapq.heappush` và :func:`heapq.heappop` tạo và duy trì một cấu trúc dữ liệu được sắp xếp một phần, trong đó phần tử nhỏ nhất luôn ở vị trí ``0``. Các hàm này phù hợp để triển khai hàng đợi ưu tiên, vốn thường được dùng để lập lịch tác vụ.

.. _`arity`: https://en.wikipedia.org/wiki/Arity
.. _`stable`: https://en.wikipedia.org/wiki/Sorting_algorithm#Stability
.. _`Timsort`: https://en.wikipedia.org/wiki/Timsort
.. _`Schwartzian transform`: https://en.wikipedia.org/wiki/Schwartzian_transform
.. _`balance scale`: https://upload.wikimedia.org/wikipedia/commons/1/17/Balance_à_tabac_1850.JPG
.. _`IEEE-754 standard`: https://en.wikipedia.org/wiki/IEEE_754
