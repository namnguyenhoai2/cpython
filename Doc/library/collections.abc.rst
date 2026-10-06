:mod:`!collections.abc` --- Các lớp cơ sở trừu tượng cho container
==================================================================

.. module:: collections.abc
   :synopsis: Các lớp cơ sở trừu tượng cho container

.. moduleauthor:: Raymond Hettinger <python at rcn.com>
.. sectionauthor:: Raymond Hettinger <python at rcn.com>

.. versionadded:: 3.3
   Trước đây, mô-đun này là một phần của mô-đun :mod:`collections`.

**Mã nguồn:** :source:`Lib/_collections_abc.py`

.. testsetup:: *

   from collections.abc import *
   import itertools
   __name__ = '<doctest>'

--------------

Mô-đun này cung cấp :term:`các lớp cơ sở trừu tượng <abstract base class>` có thể được dùng để kiểm tra xem một lớp có cung cấp một interface cụ thể hay không; ví dụ: liệu lớp đó có phải là :term:`hashable` hay liệu nó có phải là một :term:`mapping`.

Một phép kiểm tra :func:`issubclass` hoặc :func:`isinstance` đối với một interface hoạt động theo một trong ba cách.

1) Một lớp mới được viết có thể kế thừa trực tiếp từ một trong các lớp cơ sở trừu tượng. Lớp đó phải cung cấp các phương thức trừu tượng bắt buộc. Các phương thức mixin còn lại được kế thừa và có thể được ghi đè nếu muốn. Có thể thêm các phương thức khác khi cần:

   .. testcode::

      class C(Sequence):                      # Kế thừa trực tiếp
          def __init__(self): ...             # Phương thức bổ sung không bắt buộc bởi ABC
          def __getitem__(self, index):  ...  # Phương thức trừu tượng bắt buộc
          def __len__(self):  ...             # Phương thức trừu tượng bắt buộc
          def count(self, value): ...         # Tùy chọn ghi đè phương thức mixin

   .. doctest::

      >>> issubclass(C, Sequence)
      True
      >>> isinstance(C(), Sequence)
      True

2) Các lớp hiện có và lớp tích hợp sẵn có thể được đăng ký làm "lớp con ảo" của các ABC. Những lớp đó nên định nghĩa đầy đủ API, bao gồm tất cả phương thức trừu tượng và tất cả phương thức mixin. Điều này cho phép người dùng dựa vào các phép kiểm tra :func:`issubclass` hoặc :func:`isinstance` để xác định xem giao diện đầy đủ có được hỗ trợ hay không. Ngoại lệ của quy tắc này là các phương thức được tự động suy ra từ phần API còn lại:

   .. testcode::

      class D:                                 # Không kế thừa
          def __init__(self): ...              # Phương thức bổ sung không bắt buộc bởi ABC
          def __getitem__(self, index):  ...   # Phương thức trừu tượng
          def __len__(self):  ...              # Phương thức trừu tượng
          def count(self, value): ...          # Phương thức mixin
          def index(self, value): ...          # Phương thức mixin

      Sequence.register(D)                     # Đăng ký thay vì kế thừa

   .. doctest::

      >>> issubclass(D, Sequence)
      True
      >>> isinstance(D(), Sequence)
      True

   Trong ví dụ này, lớp :class:`!D` không cần định nghĩa ``__contains__``, ``__iter__`` và ``__reversed__`` vì
   :ref:`in-operator <comparisons>`, logic :term:`iteration <iterable>`, và hàm :func:`reversed` tự động chuyển sang sử dụng ``__getitem__`` và ``__len__``.

3) Một số interface đơn giản có thể được nhận diện trực tiếp nhờ sự hiện diện của các phương thức bắt buộc (trừ khi các phương thức đó đã được đặt thành :const:`None`):

   .. testcode::

      class E:
          def __iter__(self): ...
          def __next__(self): ...

   .. doctest::

      >>> issubclass(E, Iterable)
      True
      >>> isinstance(E(), Iterable)
      True

   Các interface phức tạp không hỗ trợ kỹ thuật cuối cùng này vì một interface không chỉ đơn thuần là sự hiện diện của tên phương thức. Interface xác định ngữ nghĩa và mối quan hệ giữa các phương thức, những điều không thể được suy ra chỉ từ sự hiện diện của các tên phương thức cụ thể. Ví dụ, biết rằng một class cung cấp ``__getitem__``, ``__len__`` và ``__iter__`` là chưa đủ để phân biệt :class:`Sequence` với :class:`Mapping`.

.. versionadded:: 3.9
   Các abstract class này hiện hỗ trợ ``[]``. Xem :ref:`types-genericalias` và :pep:`585`.

.. _collections-abstract-base-classes:

Các Abstract Base Class của collections
---------------------------------------

Module collections cung cấp các :term:`ABC <abstract base class>` sau:

.. tabularcolumns:: |l|L|L|L|

+------------------------------+------------------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ABC                          | Kế thừa từ             | Phương thức trừu tượng | Phương thức Mixin                                                                                                                                                       |
+==============================+========================+========================+=========================================================================================================================================================================+
| :class:`Container` [1]_      |                        | ``__contains__``       |                                                                                                                                                                         |
+------------------------------+------------------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :class:`Hashable` [1]_       |                        | ``__hash__``           |                                                                                                                                                                         |
+------------------------------+------------------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :class:`Iterable` [1]_ [2]_  |                        | ``__iter__``           |                                                                                                                                                                         |
+------------------------------+------------------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :class:`Iterator` [1]_       | :class:`Iterable`      | ``__next__``           | ``__iter__``                                                                                                                                                            |
+------------------------------+------------------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :class:`Reversible` [1]_     | :class:`Iterable`      | ``__reversed__``       |                                                                                                                                                                         |
+------------------------------+------------------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :class:`Generator`  [1]_     | :class:`Iterator`      | ``send``, ``throw``    | ``close``, ``__iter__``, ``__next__``                                                                                                                                   |
+------------------------------+------------------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :class:`Sized`  [1]_         |                        | ``__len__``            |                                                                                                                                                                         |
+------------------------------+------------------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :class:`Callable`  [1]_      |                        | ``__call__``           |                                                                                                                                                                         |
+------------------------------+------------------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :class:`Collection`  [1]_    | :class:`Sized`,        | ``__contains__``,      |                                                                                                                                                                         |
|                              | :class:`Iterable`,     | ``__iter__``,          |                                                                                                                                                                         |
|                              | :class:`Container`     | ``__len__``            |                                                                                                                                                                         |
+------------------------------+------------------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :class:`Sequence`            | :class:`Reversible`,   | ``__getitem__``,       | ``__contains__``, ``__iter__``, ``__reversed__``, ``index``, và ``count``                                                                                               |
|                              | :class:`Collection`    | ``__len__``            |                                                                                                                                                                         |
+------------------------------+------------------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :class:`MutableSequence`     | :class:`Sequence`      | ``__getitem__``,       | Các phương thức :class:`Sequence` được kế thừa và ``append``, ``clear``, ``reverse``, ``extend``, ``pop``, ``remove``, và ``__iadd__``                                  |
|                              |                        | ``__setitem__``,       |                                                                                                                                                                         |
|                              |                        | ``__delitem__``,       |                                                                                                                                                                         |
|                              |                        | ``__len__``,           |                                                                                                                                                                         |
|                              |                        | ``insert``             |                                                                                                                                                                         |
+------------------------------+------------------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :class:`ByteString`          | :class:`Sequence`      | ``__getitem__``,       | Các phương thức :class:`Sequence` được kế thừa                                                                                                                          |
|                              |                        | ``__len__``            |                                                                                                                                                                         |
+------------------------------+------------------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :class:`Set`                 | :class:`Collection`    | ``__contains__``,      | ``__le__``, ``__lt__``, ``__eq__``, ``__ne__``, ``__gt__``, ``__ge__``, ``__and__``, ``__or__``, ``__sub__``, ``__rsub__``, ``__xor__``, ``__rxor__`` và ``isdisjoint`` |
|                              |                        | ``__iter__``,          |                                                                                                                                                                         |
|                              |                        | ``__len__``            |                                                                                                                                                                         |
+------------------------------+------------------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :class:`MutableSet`          | :class:`Set`           | ``__contains__``,      | Các phương thức :class:`Set` được kế thừa và ``clear``, ``pop``, ``remove``, ``__ior__``, ``__iand__``, ``__ixor__`` và ``__isub__``                                    |
|                              |                        | ``__iter__``,          |                                                                                                                                                                         |
|                              |                        | ``__len__``,           |                                                                                                                                                                         |
|                              |                        | ``add``,               |                                                                                                                                                                         |
|                              |                        | ``discard``            |                                                                                                                                                                         |
+------------------------------+------------------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :class:`Mapping`             | :class:`Collection`    | ``__getitem__``,       | ``__contains__``, ``keys``, ``items``, ``values``, ``get``, ``__eq__`` và ``__ne__``                                                                                    |
|                              |                        | ``__iter__``,          |                                                                                                                                                                         |
|                              |                        | ``__len__``            |                                                                                                                                                                         |
+------------------------------+------------------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :class:`MutableMapping`      | :class:`Mapping`       | ``__getitem__``,       | Các phương thức :class:`Mapping` được kế thừa và ``pop``, ``popitem``, ``clear``, ``update`` và ``setdefault``                                                          |
|                              |                        | ``__setitem__``,       |                                                                                                                                                                         |
|                              |                        | ``__delitem__``,       |                                                                                                                                                                         |
|                              |                        | ``__iter__``,          |                                                                                                                                                                         |
|                              |                        | ``__len__``            |                                                                                                                                                                         |
+------------------------------+------------------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :class:`MappingView`         | :class:`Sized`         |                        | ``__init__``, ``__len__`` và ``__repr__``                                                                                                                               |
+------------------------------+------------------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :class:`ItemsView`           | :class:`MappingView`,  |                        | ``__contains__``,                                                                                                                                                       |
|                              | :class:`Set`           |                        | ``__iter__``                                                                                                                                                            |
+------------------------------+------------------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :class:`KeysView`            | :class:`MappingView`,  |                        | ``__contains__``,                                                                                                                                                       |
|                              | :class:`Set`           |                        | ``__iter__``                                                                                                                                                            |
+------------------------------+------------------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :class:`ValuesView`          | :class:`MappingView`,  |                        | ``__contains__``, ``__iter__``                                                                                                                                          |
|                              | :class:`Collection`    |                        |                                                                                                                                                                         |
+------------------------------+------------------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :class:`Awaitable` [1]_      |                        | ``__await__``          |                                                                                                                                                                         |
+------------------------------+------------------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :class:`Coroutine` [1]_      | :class:`Awaitable`     | ``send``, ``throw``    | ``close``                                                                                                                                                               |
+------------------------------+------------------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :class:`AsyncIterable` [1]_  |                        | ``__aiter__``          |                                                                                                                                                                         |
+------------------------------+------------------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :class:`AsyncIterator` [1]_  | :class:`AsyncIterable` | ``__anext__``          | ``__aiter__``                                                                                                                                                           |
+------------------------------+------------------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :class:`AsyncGenerator` [1]_ | :class:`AsyncIterator` | ``asend``, ``athrow``  | ``aclose``, ``__aiter__``, ``__anext__``                                                                                                                                |
+------------------------------+------------------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :class:`Buffer` [1]_         |                        | ``__buffer__``         |                                                                                                                                                                         |
+------------------------------+------------------------+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+


.. rubric:: Chú thích

.. [1] Các ABC này ghi đè :meth:`~abc.ABCMeta.__subclasshook__` để hỗ trợ kiểm tra một interface bằng cách xác minh rằng các phương thức bắt buộc có tồn tại và chưa được đặt thành :const:`None`. Cách này chỉ hoạt động với các interface đơn giản. Các interface phức tạp hơn yêu cầu đăng ký hoặc kế thừa trực tiếp từ lớp con.

.. [2] Việc kiểm tra ``isinstance(obj, Iterable)`` sẽ phát hiện các lớp được đăng ký là :class:`Iterable` hoặc có phương thức :meth:`~container.__iter__`, nhưng không phát hiện các lớp lặp qua
   phương thức :meth:`~object.__getitem__`. Cách đáng tin cậy duy nhất để xác định một đối tượng có phải là :term:`iterable` hay không là gọi ``iter(obj)``.


Các lớp cơ sở trừu tượng của Collections -- Mô tả chi tiết
----------------------------------------------------------


.. class:: Container

   ABC dành cho các lớp cung cấp phương thức :meth:`~object.__contains__`.

.. class:: Hashable

   ABC dành cho các lớp cung cấp phương thức :meth:`~object.__hash__`.

.. class:: Sized

   ABC dành cho các lớp cung cấp phương thức :meth:`~object.__len__`.

.. class:: Callable

   ABC dành cho các lớp cung cấp phương thức :meth:`~object.__call__`.

   Xem :ref:`annotating-callables` để biết chi tiết về cách sử dụng
   :class:`!Callable` trong chú thích kiểu.

.. class:: Iterable

   ABC dành cho các lớp cung cấp phương thức :meth:`~container.__iter__`.

   Việc kiểm tra ``isinstance(obj, Iterable)`` sẽ phát hiện các lớp được đăng ký dưới dạng :class:`Iterable` hoặc có phương thức :meth:`~container.__iter__`, nhưng không phát hiện các lớp lặp qua phương thức :meth:`~object.__getitem__`. Cách đáng tin cậy duy nhất để xác định một đối tượng có :term:`iterable` hay không là gọi ``iter(obj)``.

.. class:: Collection

   ABC dành cho các lớp vùng chứa có kích thước và có thể lặp.

   .. versionadded:: 3.6

.. class:: Iterator

   ABC dành cho các lớp cung cấp :meth:`~iterator.__iter__` và
   các phương thức :meth:`~iterator.__next__`. Xem thêm định nghĩa về
   :term:`iterator`.

.. class:: Reversible

   ABC dành cho các lớp có thể lặp cũng cung cấp phương thức :meth:`~object.__reversed__`.

   .. versionadded:: 3.6

.. class:: Generator

   ABC cho các lớp :term:`generator` triển khai giao thức được định nghĩa trong
   :pep:`342` mở rộng :term:`iterators <iterator>` với các
   :meth:`~generator.send`,
   :meth:`~generator.throw` và các phương thức :meth:`~generator.close`.

   Xem :ref:`annotating-generators-and-coroutines` để biết chi tiết về cách sử dụng :class:`!Generator` trong chú thích kiểu.

   .. versionadded:: 3.5

.. class:: Sequence
           MutableSequence ByteString

   Các ABC cho :term:`sequences <sequence>` chỉ đọc và có thể thay đổi.

   Lưu ý về triển khai: Một số phương thức mixin, chẳng hạn như
   :meth:`~container.__iter__`, :meth:`~object.__reversed__` và :meth:`~sequence.index` thực hiện các lần gọi lặp lại đến phương thức nền tảng
   phương thức :meth:`~object.__getitem__`. Do đó, nếu :meth:`~object.__getitem__` được triển khai với tốc độ truy cập hằng số, các phương thức mixin sẽ có hiệu năng tuyến tính; tuy nhiên, nếu phương thức nền tảng có hiệu năng tuyến tính (như khi sử dụng danh sách liên kết), các phương thức mixin sẽ có hiệu năng bậc hai và nhiều khả năng cần được ghi đè.

   .. method:: index(value, start=0, stop=None)

      Trả về chỉ mục đầu tiên của *value*.

      Phát sinh :exc:`ValueError` nếu không tìm thấy giá trị.

      Việc hỗ trợ các đối số *start* và *stop* là tùy chọn nhưng được khuyến nghị.

      .. versionchanged:: 3.5
         Phương thức :meth:`~sequence.index` đã được bổ sung khả năng hỗ trợ các đối số *stop* và *start*.

   .. deprecated-removed:: 3.12 3.17
      ABC :class:`ByteString` đã không còn được khuyến nghị sử dụng.

      Dùng ``isinstance(obj, collections.abc.Buffer)`` để kiểm tra tại runtime xem ``obj`` có triển khai :ref:`giao thức buffer <bufferobjects>` hay không. Khi sử dụng trong type annotation, hãy dùng :class:`Buffer` hoặc một union chỉ rõ các kiểu mà mã của bạn hỗ trợ (ví dụ: ``bytes | bytearray | memoryview``).

      :class:`!ByteString` ban đầu được dự định là một abstract class đóng vai trò supertype của cả :class:`bytes` và :class:`bytearray`. Tuy nhiên, vì ABC này chưa bao giờ có phương thức nào nên việc biết một đối tượng là một instance của :class:`!ByteString` thực tế không cho bạn biết điều gì hữu ích về đối tượng đó. Các kiểu buffer phổ biến khác như
      :class:`memoryview` cũng chưa bao giờ được coi là subtype của
      :class:`!ByteString` (dù ở runtime hay bởi các static type checker).

      Xem :pep:`PEP 688 <688#current-options>` để biết thêm chi tiết.

.. class:: Set
           MutableSet

   Các ABC cho :ref:`tập hợp <types-set>` chỉ đọc và có thể thay đổi.

.. class:: Mapping
           MutableMapping

   Các ABC cho :term:`ánh xạ <mapping>` chỉ đọc và có thể thay đổi.

.. class:: MappingView
           ItemsView KeysView ValuesView

   Các ABC cho :term:`view <dictionary view>` ánh xạ, phần tử, khóa và giá trị.

.. class:: Awaitable

   ABC cho các đối tượng :term:`awaitable`, có thể được sử dụng trong các biểu thức :keyword:`await`. Các triển khai tùy chỉnh phải cung cấp
   phương thức :meth:`~object.__await__`.

   Các đối tượng :term:`Coroutine <coroutine>` và các thể hiện của
   :class:`~collections.abc.Coroutine` ABC đều là các thể hiện của ABC này.

   .. note::
      Trong CPython, các coroutine dựa trên generator (:term:`generators <generator>` được trang trí bằng :deco:`types.coroutine`) là *awaitables*, mặc dù chúng không có phương thức :meth:`~object.__await__`. Sử dụng ``isinstance(gencoro, Awaitable)`` cho chúng sẽ trả về ``False``. Sử dụng :func:`inspect.isawaitable` để phát hiện chúng.

   .. versionadded:: 3.5

.. class:: Coroutine

   ABC cho các lớp tương thích với :term:`coroutine`. Các lớp này triển khai các phương thức sau, được định nghĩa trong :ref:`coroutine-objects`:
   :meth:`~coroutine.send`, :meth:`~coroutine.throw`, và
   :meth:`~coroutine.close`. Các triển khai tùy chỉnh cũng phải triển khai
   :meth:`~object.__await__`. Tất cả các thể hiện :class:`Coroutine` cũng là các thể hiện của :class:`Awaitable`.

   .. note::
      Trong CPython, các coroutine dựa trên generator (:term:`generators <generator>` được trang trí bằng :deco:`types.coroutine`) là *awaitables*, mặc dù chúng không có phương thức :meth:`~object.__await__`. Sử dụng ``isinstance(gencoro, Coroutine)`` cho chúng sẽ trả về ``False``. Sử dụng :func:`inspect.isawaitable` để phát hiện chúng.

   Xem :ref:`annotating-generators-and-coroutines` để biết chi tiết về cách sử dụng :class:`!Coroutine` trong chú thích kiểu. Tính biến thiên và thứ tự của các tham số kiểu tương ứng với các tham số của
   :class:`Generator`.

   .. versionadded:: 3.5

.. class:: AsyncIterable

   ABC dành cho các lớp cung cấp phương thức ``__aiter__``. Xem thêm định nghĩa của :term:`asynchronous iterable`.

   .. versionadded:: 3.5

.. class:: AsyncIterator

   ABC dành cho các lớp cung cấp các phương thức ``__aiter__`` và ``__anext__``. Xem thêm định nghĩa của :term:`asynchronous iterator`.

   .. versionadded:: 3.5

.. class:: AsyncGenerator

   ABC dành cho các lớp :term:`asynchronous generator` triển khai giao thức được định nghĩa trong :pep:`525` và :pep:`492`.

   Xem :ref:`annotating-generators-and-coroutines` để biết chi tiết về cách sử dụng :class:`!AsyncGenerator` trong chú thích kiểu.

   .. versionadded:: 3.6

.. class:: Buffer

   ABC cho các lớp cung cấp :meth:`~object.__buffer__` phương thức, triển khai :ref:`giao thức buffer <bufferobjects>`. Xem :pep:`688`.

   .. versionadded:: 3.12

Ví dụ và công thức
------------------

ABCs cho phép chúng ta hỏi các lớp hoặc instance xem chúng có cung cấp chức năng cụ thể hay không, chẳng hạn như::

    size = None
    if isinstance(myvar, collections.abc.Sized):
        size = len(myvar)

Một số ABC cũng hữu ích dưới dạng mixin, giúp việc phát triển các lớp hỗ trợ API container trở nên dễ dàng hơn. Ví dụ, để viết một lớp hỗ trợ đầy đủ API :class:`Set`, chỉ cần cung cấp ba phương thức abstract nền tảng: :meth:`~object.__contains__`, :meth:`~container.__iter__`, và
:meth:`~object.__len__`. ABC cung cấp các phương thức còn lại, chẳng hạn như
:meth:`!__and__` và :meth:`~frozenset.isdisjoint`::

    class ListBasedSet(collections.abc.Set):
        ''' Alternate set implementation favoring space over speed
            and not requiring the set elements to be hashable. '''
        def __init__(self, iterable):
            self.elements = lst = []
            for value in iterable:
                if value not in lst:
                    lst.append(value)

        def __iter__(self):
            return iter(self.elements)

        def __contains__(self, value):
            return value in self.elements

        def __len__(self):
            return len(self.elements)

    s1 = ListBasedSet('abcdef')
    s2 = ListBasedSet('defghi')
    overlap = s1 & s2            # Phương thức __and__() được hỗ trợ tự động

Lưu ý khi sử dụng :class:`Set` và :class:`MutableSet` dưới dạng mixin:

(1)
   Vì một số phép toán trên set tạo ra các set mới, các phương thức mixin mặc định cần có cách tạo các instance mới từ một :term:`iterable`. Constructor của lớp được giả định có signature ở dạng ``ClassName(iterable)``. Giả định đó được tách riêng thành một :class:`classmethod` nội bộ có tên là
   :meth:`!_from_iterable` gọi ``cls(iterable)`` để tạo một tập hợp mới. Nếu mixin :class:`Set` được sử dụng trong một lớp có chữ ký constructor khác, bạn sẽ cần ghi đè :meth:`!_from_iterable` bằng một classmethod hoặc method thông thường có thể tạo các instance mới từ một đối số iterable.

(2)
   Để ghi đè các phép so sánh (có lẽ nhằm tăng tốc độ, vì ngữ nghĩa đã cố định), hãy định nghĩa lại :meth:`~object.__le__` và
   :meth:`~object.__ge__`, khi đó các phép toán khác sẽ tự động làm theo.

(3)
   Mixin :class:`Set` cung cấp method :meth:`!_hash` để tính giá trị băm cho tập hợp; tuy nhiên, :meth:`~object.__hash__` không được định nghĩa vì không phải mọi tập hợp đều :term:`hashable` hoặc bất biến. Để thêm khả năng băm cho tập hợp bằng mixin, hãy kế thừa cả :class:`Set` và :class:`Hashable`, sau đó định nghĩa ``__hash__ = Set._hash``.

.. seealso::

   * `Công thức OrderedSet <https://code.activestate.com/recipes/576694/>`_ cho một ví dụ được xây dựng trên :class:`MutableSet`.

   * Để biết thêm về ABC, hãy xem module :mod:`abc` và :pep:`3119`.

.. _`OrderedSet recipe`: https://code.activestate.com/recipes/576694/
