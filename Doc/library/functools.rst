:mod:`!functools` --- Các hàm bậc cao và các thao tác trên đối tượng có thể gọi
===============================================================================

.. module:: functools
   :synopsis: Các hàm bậc cao và các thao tác trên đối tượng có thể gọi.

.. moduleauthor:: Peter Harris <scav@blueyonder.co.uk>
.. moduleauthor:: Raymond Hettinger <python@rcn.com>
.. moduleauthor:: Nick Coghlan <ncoghlan@gmail.com>
.. moduleauthor:: Łukasz Langa <lukasz@langa.pl>
.. moduleauthor:: Pablo Galindo <pablogsal@gmail.com>
.. sectionauthor:: Peter Harris <scav@blueyonder.co.uk>

**Mã nguồn:** :source:`Lib/functools.py`

.. testsetup:: default

   import functools
   from functools import *

--------------

Module :mod:`!functools` dành cho các hàm bậc cao: những hàm thao tác trên hoặc trả về các hàm khác. Nhìn chung, mọi đối tượng có thể gọi đều có thể được xem như một hàm trong phạm vi của module này.

Module :mod:`!functools` định nghĩa các hàm sau:

.. decorator:: cache(user_function)

   Bộ nhớ đệm hàm đơn giản, nhẹ và không giới hạn. Đôi khi được gọi là `"memoize" <https://en.wikipedia.org/wiki/Memoization>`_.

   Trả về kết quả giống như ``lru_cache(maxsize=None)``, đồng thời tạo một lớp bọc mỏng quanh thao tác tra cứu từ điển cho các đối số của hàm. Vì không bao giờ cần loại bỏ các giá trị cũ, cách này nhỏ gọn và nhanh hơn
   :deco:`lru_cache` với giới hạn kích thước.

   Ví dụ::

        @cache
        def factorial(n):
            return n * factorial(n-1) if n else 1

        >>> factorial(10)   # không có kết quả được lưu trong bộ nhớ đệm trước đó, thực hiện 11 lần gọi đệ quy
        3628800
        >>> factorial(5)    # không có lệnh gọi mới, chỉ trả về kết quả đã lưu trong bộ nhớ đệm
        120
        >>> factorial(12)   # hai lần gọi đệ quy mới, factorial(10) đã được lưu trong bộ nhớ đệm
        479001600

   Bộ nhớ đệm an toàn trong môi trường đa luồng, vì vậy hàm được bao bọc có thể được sử dụng trong nhiều luồng. Điều này có nghĩa là cấu trúc dữ liệu bên dưới vẫn nhất quán trong quá trình cập nhật đồng thời.

   Hàm được bao bọc có thể được gọi nhiều hơn một lần nếu một luồng khác thực hiện thêm một lệnh gọi trước khi lệnh gọi ban đầu hoàn tất và được lưu vào bộ nhớ đệm.

   .. versionadded:: 3.9


.. decorator:: cached_property(func)

   Chuyển một phương thức của lớp thành một thuộc tính có giá trị được tính một lần, sau đó được lưu vào bộ nhớ đệm dưới dạng thuộc tính thông thường trong suốt vòng đời của instance. Tương tự :deco:`property`, nhưng có thêm cơ chế caching. Hữu ích cho các thuộc tính được tính toán tốn kém của những instance vốn dĩ gần như bất biến.

   Ví dụ::

       class DataSet:

           def __init__(self, sequence_of_numbers):
               self._data = tuple(sequence_of_numbers)

           @cached_property
           def stdev(self):
               return statistics.stdev(self._data)

   Cơ chế của :deco:`cached_property` hơi khác so với
   :deco:`property`. Một property thông thường ngăn việc ghi thuộc tính trừ khi đã định nghĩa setter. Ngược lại, một *cached_property* cho phép ghi.

   Decorator *cached_property* chỉ được thực thi khi tra cứu và chỉ khi chưa tồn tại thuộc tính cùng tên. Khi được thực thi, *cached_property* ghi vào thuộc tính cùng tên. Các thao tác đọc và ghi thuộc tính sau đó được ưu tiên hơn phương thức *cached_property* và nó hoạt động như một thuộc tính thông thường.

   Có thể xóa giá trị đã được lưu trong bộ nhớ đệm bằng cách xóa thuộc tính. Điều này cho phép phương thức *cached_property* được thực thi lại.

   *cached_property* không ngăn được khả năng xảy ra race condition khi sử dụng đa luồng. Hàm getter có thể chạy nhiều hơn một lần trên cùng một instance, trong đó lần chạy mới nhất sẽ thiết lập giá trị được lưu trong bộ nhớ đệm. Nếu cached property là idempotent hoặc việc chạy nhiều hơn một lần trên một instance không gây hại theo cách khác, thì điều này không sao. Nếu cần đồng bộ hóa, hãy triển khai cơ chế locking cần thiết bên trong hàm getter được decorated hoặc xung quanh thao tác truy cập cached property.

   Lưu ý rằng decorator này ảnh hưởng đến hoạt động của các từ điển chia sẻ khóa :pep:`412`. Điều này có nghĩa là từ điển của instance có thể chiếm nhiều không gian hơn bình thường.

   Ngoài ra, decorator này yêu cầu thuộc tính ``__dict__`` trên mỗi instance phải là một ánh xạ có thể thay đổi. Điều này có nghĩa là nó sẽ không hoạt động với một số kiểu, chẳng hạn như metaclass (vì các thuộc tính ``__dict__`` trên các instance của type là proxy chỉ đọc cho namespace của class), và những kiểu chỉ định ``__slots__`` mà không đưa ``__dict__`` vào một trong các slot đã định nghĩa (vì các class như vậy hoàn toàn không cung cấp thuộc tính ``__dict__``).

   Nếu không có ánh xạ có thể thay đổi hoặc nếu muốn chia sẻ khóa tiết kiệm không gian, bạn cũng có thể đạt được hiệu ứng tương tự như :deco:`cached_property` bằng cách xếp :deco:`property` lên trên :deco:`lru_cache`. Xem
   :ref:`faq-cache-method-calls` để biết thêm chi tiết về điểm khác biệt giữa nó và :deco:`cached_property`.

   .. versionadded:: 3.8

   .. versionchanged:: 3.12
      Trước Python 3.12, :deco:`!cached_property` có một lock không được tài liệu hóa để đảm bảo rằng khi sử dụng trong môi trường đa luồng, hàm getter chỉ được chạy một lần cho mỗi instance. Tuy nhiên, lock này áp dụng cho mỗi property chứ không phải mỗi instance, nên có thể dẫn đến tranh chấp lock cao đến mức không thể chấp nhận được. Trong Python 3.12 trở lên, cơ chế khóa này đã bị loại bỏ.


.. function:: cmp_to_key(func)

   Chuyển đổi một hàm so sánh kiểu cũ thành một :term:`key function`. Được sử dụng với các công cụ chấp nhận hàm key (chẳng hạn như :func:`sorted`, :func:`min`,
   :func:`max`, :func:`heapq.nlargest`, :func:`heapq.nsmallest`,
   :func:`itertools.groupby`). Hàm này chủ yếu được dùng như một công cụ chuyển đổi cho các chương trình đang được chuyển từ Python 2, phiên bản hỗ trợ việc sử dụng các hàm so sánh.

   Hàm comparison là bất kỳ đối tượng callable nào nhận hai đối số, so sánh chúng và trả về một số âm nếu nhỏ hơn, bằng 0 nếu bằng nhau hoặc một số dương nếu lớn hơn. Hàm key là một đối tượng callable nhận một đối số và trả về một giá trị khác để dùng làm khóa sắp xếp.

   Ví dụ::

       sorted(iterable, key=cmp_to_key(locale.strcoll))  # thứ tự sắp xếp phụ thuộc locale

   Để xem các ví dụ về sắp xếp và hướng dẫn ngắn về sắp xếp, hãy xem :ref:`sortinghowto`.

   .. versionadded:: 3.2


.. decorator:: lru_cache(user_function)
               lru_cache(maxsize=128, typed=False)

   Decorator bọc một hàm bằng một đối tượng callable có cơ chế ghi nhớ, lưu tối đa *maxsize* lời gọi gần đây nhất. Decorator này có thể tiết kiệm thời gian khi một hàm tốn nhiều chi phí hoặc bị giới hạn bởi I/O được gọi định kỳ với cùng các đối số.

   Bộ nhớ đệm an toàn trong môi trường đa luồng, vì vậy hàm được bao bọc có thể được sử dụng trong nhiều luồng. Điều này có nghĩa là cấu trúc dữ liệu bên dưới vẫn nhất quán trong quá trình cập nhật đồng thời.

   Hàm được bao bọc có thể được gọi nhiều hơn một lần nếu một luồng khác thực hiện thêm một lệnh gọi trước khi lệnh gọi ban đầu hoàn tất và được lưu vào bộ nhớ đệm.

   Vì một dictionary được dùng để lưu kết quả vào cache, các đối số vị trí và từ khóa của hàm phải là :term:`hashable`.

   Các mẫu đối số khác nhau có thể được xem là những lần gọi khác nhau với các mục cache riêng biệt. Ví dụ: ``f(a=1, b=2)`` và ``f(b=2, a=1)`` khác nhau về thứ tự đối số từ khóa và có thể có hai mục cache riêng biệt.

   Nếu chỉ định *user_function*, giá trị này phải là một callable. Điều này cho phép áp dụng decorator *lru_cache* trực tiếp cho một user function, giữ *maxsize* ở giá trị mặc định là 128.::

       @lru_cache
       def count_vowels(sentence):
           return sum(sentence.count(vowel) for vowel in 'AEIOUaeiou')

   Nếu *maxsize* được đặt thành ``None``, tính năng LRU sẽ bị vô hiệu hóa và cache có thể tăng không giới hạn.

   Nếu *typed* được đặt thành true, các đối số hàm thuộc những kiểu khác nhau sẽ được lưu vào cache riêng biệt. Nếu *typed* là false, implementation thường xem chúng là những lần gọi tương đương và chỉ lưu vào cache một kết quả duy nhất. (Một số kiểu như *str* và *int* có thể vẫn được lưu vào cache riêng biệt ngay cả khi *typed* là false.)

   Lưu ý rằng tính đặc thù theo kiểu chỉ áp dụng cho các đối số trực tiếp của hàm, không áp dụng cho nội dung của chúng. Các đối số vô hướng, ``Decimal(42)`` và ``Fraction(42)``, được xem là những lần gọi khác nhau với các kết quả khác nhau. Ngược lại, các đối số tuple ``('answer', Decimal(42))`` và ``('answer', Fraction(42))`` được xem là tương đương.

   Hàm được bọc có thêm một hàm :func:`!cache_parameters` trả về một :class:`dict` mới, hiển thị các giá trị của *maxsize* và *typed*.  Thông tin này chỉ nhằm mục đích tham khảo.  Việc thay đổi các giá trị không có tác dụng.

   .. method:: lru_cache.cache_info()
      :no-typesetting:

   Để giúp đo lường hiệu quả của cache và điều chỉnh tham số *maxsize*, hàm được bọc có thêm một hàm :func:`!cache_info` trả về một :term:`named tuple` hiển thị *hits*, *misses*, *maxsize* và *currsize*.

   .. method:: lru_cache.cache_clear()
      :no-typesetting:

   Decorator này cũng cung cấp một hàm :func:`!cache_clear` để xóa hoặc vô hiệu hóa cache.

   Hàm gốc bên dưới có thể được truy cập thông qua
   thuộc tính :attr:`__wrapped__`.  Điều này hữu ích cho việc introspection, bỏ qua cache hoặc bọc lại hàm bằng một cache khác.

   Cache giữ các tham chiếu đến các đối số và giá trị trả về cho đến khi chúng hết hạn khỏi cache hoặc cache được xóa.

   Nếu một method được cache, đối số instance ``self`` sẽ được đưa vào cache.  Xem :ref:`faq-cache-method-calls`

   Một `bộ nhớ đệm LRU (ít được sử dụng gần đây nhất) <https://en.wikipedia.org/wiki/Cache_replacement_policies#Least_Recently_Used_(LRU)>`_ hoạt động tốt nhất khi các lần gọi gần đây nhất là yếu tố dự đoán tốt nhất cho các lần gọi sắp tới (ví dụ: các bài viết phổ biến nhất trên một máy chủ tin tức thường thay đổi mỗi ngày). Giới hạn kích thước của bộ nhớ đệm đảm bảo rằng bộ nhớ đệm không tăng không giới hạn trong các tiến trình chạy lâu như máy chủ web.

   Nhìn chung, chỉ nên sử dụng bộ nhớ đệm LRU khi bạn muốn tái sử dụng các giá trị đã được tính toán trước đó. Vì vậy, việc lưu vào bộ nhớ đệm các hàm có tác dụng phụ, các hàm cần tạo ra những đối tượng có thể thay đổi riêng biệt trong mỗi lần gọi (chẳng hạn như generator và hàm async), hoặc các hàm không thuần túy như time() hay random() là không hợp lý.

   Ví dụ về bộ nhớ đệm LRU cho nội dung web tĩnh::

        @lru_cache(maxsize=32)
        def get_pep(num):
            'Retrieve text of a Python Enhancement Proposal'
            resource = f'https://peps.python.org/pep-{num:04d}'
            try:
                with urllib.request.urlopen(resource) as s:
                    return s.read()
            except urllib.error.HTTPError:
                return 'Not Found'

        >>> for n in 8, 290, 308, 320, 8, 218, 320, 279, 289, 320, 9991:
        ...     pep = get_pep(n)
        ...     print(n, len(pep))

        >>> get_pep.cache_info()
        CacheInfo(hits=3, misses=8, maxsize=32, currsize=8)

   Ví dụ về cách tính hiệu quả `các số Fibonacci <https://en.wikipedia.org/wiki/Fibonacci_number>`_ bằng cách sử dụng bộ nhớ đệm để triển khai kỹ thuật `lập trình động <https://en.wikipedia.org/wiki/Dynamic_programming>`_::

        @lru_cache(maxsize=None)
        def fib(n):
            if n < 2:
                return n
            return fib(n-1) + fib(n-2)

        >>> [fib(n) for n in range(16)]
        [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]

        >>> fib.cache_info()
        CacheInfo(hits=28, misses=16, maxsize=None, currsize=16)

   .. versionadded:: 3.2

   .. versionchanged:: 3.3
      Đã thêm tùy chọn *typed*.

   .. versionchanged:: 3.8
      Đã thêm tùy chọn *user_function*.

   .. versionchanged:: 3.9
      Đã thêm hàm :func:`!cache_parameters`

.. decorator:: total_ordering

   Với một lớp định nghĩa một hoặc nhiều phương thức sắp thứ tự so sánh mở rộng, class decorator này sẽ cung cấp các phương thức còn lại. Điều này giúp đơn giản hóa công sức cần thiết để chỉ định tất cả các phép toán so sánh mở rộng có thể có:

   Lớp phải định nghĩa một trong :meth:`~object.__lt__`, :meth:`~object.__le__`,
   :meth:`~object.__gt__`, hoặc :meth:`~object.__ge__`. Ngoài ra, lớp nên cung cấp một phương thức :meth:`~object.__eq__`.

   Ví dụ::

       @total_ordering
       class Student:
           def _is_valid_operand(self, other):
               return (hasattr(other, "lastname") and
                       hasattr(other, "firstname"))
           def __eq__(self, other):
               if not self._is_valid_operand(other):
                   return NotImplemented
               return ((self.lastname.lower(), self.firstname.lower()) ==
                       (other.lastname.lower(), other.firstname.lower()))
           def __lt__(self, other):
               if not self._is_valid_operand(other):
                   return NotImplemented
               return ((self.lastname.lower(), self.firstname.lower()) <
                       (other.lastname.lower(), other.firstname.lower()))

   .. note::

      Mặc dù decorator này giúp dễ dàng tạo các kiểu có thứ tự hoàn toàn hoạt động đúng, nhưng nó *có* cái giá là tốc độ thực thi chậm hơn và stack trace phức tạp hơn đối với các phương thức so sánh được tạo ra. Nếu việc benchmark hiệu năng cho thấy đây là điểm nghẽn của một ứng dụng cụ thể, việc triển khai cả sáu phương thức so sánh mở rộng thay vào đó có thể mang lại cải thiện tốc độ dễ dàng.

   .. note::

      Decorator này không cố gắng ghi đè các phương thức đã được khai báo trong lớp *hoặc các lớp cha của nó*. Điều đó có nghĩa là nếu một lớp cha định nghĩa một toán tử so sánh, *total_ordering* sẽ không triển khai lại toán tử đó, ngay cả khi phương thức ban đầu là abstract.

   .. versionadded:: 3.2

   .. versionchanged:: 3.4
      Hiện đã hỗ trợ việc trả về ``NotImplemented`` từ hàm so sánh bên dưới đối với các kiểu không được nhận dạng.

.. data:: Placeholder

   Một đối tượng singleton được dùng làm sentinel để dành chỗ cho các đối số vị trí khi gọi :func:`partial` và :func:`partialmethod`.

   .. versionadded:: 3.14

.. function:: partial(func, /, *args, **keywords)

   Trả về một đối tượng :ref:`partial object <partial-objects>` mới; khi được gọi, đối tượng này sẽ hoạt động như thể *func* được gọi với các đối số vị trí *args* và các đối số từ khóa *keywords*. Nếu cung cấp thêm đối số khi gọi, chúng sẽ được thêm vào *args*. Nếu cung cấp thêm đối số từ khóa, chúng sẽ mở rộng và ghi đè *keywords*. Về cơ bản tương đương với::

      def partial(func, /, *args, **keywords):
          def newfunc(*more_args, **more_keywords):
              return func(*args, *more_args, **(keywords | more_keywords))
          newfunc.func = func
          newfunc.args = args
          newfunc.keywords = keywords
          return newfunc

   Hàm :func:`!partial` được dùng để áp dụng hàm từng phần (partial function application), tức là “đóng băng” một phần các đối số và/hoặc đối số từ khóa của một hàm, từ đó tạo ra một đối tượng mới với chữ ký đơn giản hơn. Ví dụ, có thể dùng :func:`partial` để tạo một đối tượng có thể gọi hoạt động như hàm :func:`int`, trong đó đối số *base* mặc định là ``2``:

   .. doctest::

      >>> basetwo = partial(int, base=2)
      >>> basetwo.__doc__ = 'Convert base 2 string to an int.'
      >>> basetwo('10010')
      18

   Nếu có các sentinel :data:`Placeholder` trong *args*, chúng sẽ được điền trước khi :func:`!partial` được gọi. Nhờ đó, có thể điền trước bất kỳ đối số vị trí nào bằng một lệnh gọi tới :func:`!partial`; nếu không có :data:`!Placeholder`, chỉ có thể điền trước số đối số vị trí đầu tiên đã chọn.

   Nếu có bất kỳ sentinel :data:`!Placeholder` nào, tất cả chúng phải được điền tại thời điểm gọi:

   .. doctest::

      >>> say_to_world = partial(print, Placeholder, Placeholder, "world!")
      >>> say_to_world('Hello', 'dear')
      Hello dear world!

   Việc gọi ``say_to_world('Hello')`` sẽ phát sinh :exc:`TypeError`, vì chỉ có một đối số vị trí được cung cấp, trong khi có hai placeholder cần được điền.

   Nếu :func:`!partial` được áp dụng cho một
   :ref:`đối tượng partial <partial-objects>`, các :data:`!Placeholder` sentinel của đối tượng đầu vào được điền bằng các đối số vị trí mới. Có thể giữ lại một placeholder bằng cách chèn một
   :data:`!Placeholder` sentinel mới vào vị trí mà một :data:`!Placeholder` trước đó chiếm giữ:

   .. doctest::

      >>> from functools import partial, Placeholder as _
      >>> remove = partial(str.replace, _, _, '')
      >>> message = 'Hello, dear dear world!'
      >>> remove(message, ' dear')
      'Hello, world!'
      >>> remove_dear = partial(remove, _, ' dear')
      >>> remove_dear(message)
      'Hello, world!'
      >>> remove_first_dear = partial(remove_dear, _, 1)
      >>> remove_first_dear(message)
      'Hello, dear world!'

   :data:`!Placeholder` không thể được truyền cho :func:`!partial` dưới dạng đối số từ khóa.

   .. versionchanged:: 3.14
      Đã bổ sung hỗ trợ cho :data:`Placeholder` trong các đối số vị trí.

.. class:: partialmethod(func, /, *args, **keywords)

   Trả về một descriptor :class:`partialmethod` mới, hoạt động giống như :class:`partial`, ngoại trừ việc nó được thiết kế để dùng làm định nghĩa phương thức thay vì có thể gọi trực tiếp.

   *func* phải là một :term:`descriptor` hoặc một callable (các đối tượng đồng thời thuộc cả hai loại, như các hàm thông thường, được xử lý dưới dạng descriptor).

   Khi *func* là một descriptor (chẳng hạn như một hàm Python thông thường,
   :func:`classmethod`, :func:`staticmethod`, :func:`~abc.abstractmethod` hoặc một thực thể khác của :class:`partialmethod`), các lệnh gọi đến ``__get__`` được ủy quyền cho descriptor bên dưới, và một
   :ref:`partial object <partial-objects>` thích hợp được trả về làm kết quả.

   Khi *func* là một callable không phải descriptor, một bound method thích hợp sẽ được tạo động. Cách này hoạt động như một hàm Python thông thường khi được sử dụng làm method: đối số *self* sẽ được chèn vào làm đối số vị trí đầu tiên, thậm chí trước cả *args* và *keywords* được cung cấp cho hàm khởi tạo :class:`partialmethod`.

   Ví dụ::

      >>> class Cell:
      ...     def __init__(self):
      ...         self._alive = False
      ...     @property
      ...     def alive(self):
      ...         return self._alive
      ...     def set_state(self, state):
      ...         self._alive = bool(state)
      ...     set_alive = partialmethod(set_state, True)
      ...     set_dead = partialmethod(set_state, False)
      ...
      >>> c = Cell()
      >>> c.alive
      False
      >>> c.set_alive()
      >>> c.alive
      True

   .. versionadded:: 3.4


.. function:: reduce(function, iterable, /[, initial])

   Áp dụng *function* có hai đối số lần lượt cho các phần tử của *iterable*, từ trái sang phải, để rút gọn iterable thành một giá trị duy nhất. Ví dụ: ``reduce(lambda x, y: x+y, [1, 2, 3, 4, 5])`` tính ``((((1+2)+3)+4)+5)``. Đối số bên trái, *x*, là giá trị tích lũy, còn đối số bên phải, *y*, là giá trị cập nhật từ *iterable*. Nếu có *initial* tùy chọn, giá trị này được đặt trước các phần tử của iterable trong phép tính và đóng vai trò là giá trị mặc định khi iterable rỗng. Nếu không cung cấp *initial* và *iterable* chỉ chứa một phần tử, phần tử đầu tiên sẽ được trả về.

   Gần tương đương với::

      initial_missing = object()

      def reduce(function, iterable, /, initial=initial_missing):
          it = iter(iterable)
          if initial is initial_missing:
              value = next(it)
          else:
              value = initial
          for element in it:
              value = function(value, element)
          return value

   Xem :func:`itertools.accumulate` để biết iterator trả về tất cả các giá trị trung gian.

   .. versionchanged:: 3.14
      *initial* hiện được hỗ trợ dưới dạng đối số từ khóa.

.. decorator:: singledispatch

   Chuyển một hàm thành một :term:`single-dispatch <single dispatch>` :term:`generic function`.

   Để định nghĩa một hàm generic, hãy trang trí hàm đó bằng decorator ``@singledispatch``. Khi định nghĩa một hàm bằng ``@singledispatch``, hãy lưu ý rằng việc dispatch diễn ra dựa trên kiểu của đối số đầu tiên::

     >>> from functools import singledispatch
     >>> @singledispatch
     ... def fun(arg, verbose=False):
     ...     if verbose:
     ...         print("Let me just say,", end=" ")
     ...     print(arg)

   .. method:: singledispatch.register()
      :no-typesetting:

   Để thêm các triển khai overloaded vào hàm, hãy sử dụng thuộc tính :func:`!register` của hàm generic; thuộc tính này có thể được dùng làm decorator. Với các hàm được chú thích kiểu, decorator sẽ tự động suy ra kiểu của đối số đầu tiên::

     >>> @fun.register
     ... def _(arg: int, verbose=False):
     ...     if verbose:
     ...         print("Strength in numbers, eh?", end=" ")
     ...     print(arg)
     ...
     >>> @fun.register
     ... def _(arg: list, verbose=False):
     ...     if verbose:
     ...         print("Enumerate this:")
     ...     for i, elem in enumerate(arg):
     ...         print(i, elem)

   :class:`typing.Union` cũng có thể được sử dụng::

    >>> @fun.register
    ... def _(arg: int | float, verbose=False):
    ...     if verbose:
    ...         print("Strength in numbers, eh?", end=" ")
    ...     print(arg)
    ...
    >>> from typing import Union
    >>> @fun.register
    ... def _(arg: Union[list, set], verbose=False):
    ...     if verbose:
    ...         print("Enumerate this:")
    ...     for i, elem in enumerate(arg):
    ...         print(i, elem)
    ...

   Đối với mã không sử dụng type annotation, có thể truyền rõ ràng đối số kiểu thích hợp cho chính decorator::

     >>> @fun.register(complex)
     ... def _(arg, verbose=False):
     ...     if verbose:
     ...         print("Better than complicated.", end=" ")
     ...     print(arg.real, arg.imag)
     ...

   Đối với mã dispatch dựa trên kiểu collections (ví dụ: ``list``), nhưng muốn chỉ định type hint cho các phần tử của collection (ví dụ: ``list[int]``), kiểu dispatch cần được truyền rõ ràng cho chính decorator, còn type hint được đặt trong phần định nghĩa hàm::

     >>> @fun.register(list)
     ... def _(arg: list[int], verbose=False):
     ...     if verbose:
     ...         print("Enumerate this:")
     ...     for i, elem in enumerate(arg):
     ...         print(i, elem)

   .. note::

      Trong runtime, hàm sẽ dispatch trên một instance của list bất kể kiểu dữ liệu được chứa trong list, tức là ``[1,2,3]`` sẽ được dispatch giống như ``["foo", "bar", "baz"]``. Annotation được cung cấp trong ví dụ này chỉ dành cho static type checker và không ảnh hưởng đến runtime.

   Để cho phép đăng ký :term:`lambdas <lambda>` và các hàm có sẵn, thuộc tính :func:`~singledispatch.register` cũng có thể được sử dụng dưới dạng functional::

     >>> def nothing(arg, verbose=False):
     ...     print("Nothing.")
     ...
     >>> fun.register(type(None), nothing)

   Thuộc tính :func:`~singledispatch.register` trả về hàm chưa được áp dụng decorator. Điều này cho phép xếp chồng decorator, :mod:`pickling<pickle>`, và tạo unit test cho từng biến thể một cách độc lập::

     >>> @fun.register(float)
     ... @fun.register(Decimal)
     ... def fun_num(arg, verbose=False):
     ...     if verbose:
     ...         print("Half of your number:", end=" ")
     ...     print(arg / 2)
     ...
     >>> fun_num is fun
     False

   Khi được gọi, generic function sẽ dispatch dựa trên kiểu của đối số đầu tiên::

     >>> fun("Hello, world.")
     Hello, world.
     >>> fun("test.", verbose=True)
     Let me just say, test.
     >>> fun(42, verbose=True)
     Strength in numbers, eh? 42
     >>> fun(['spam', 'spam', 'eggs', 'spam'], verbose=True)
     Enumerate this:
     0 spam
     1 spam
     2 eggs
     3 spam
     >>> fun(None)
     Nothing.
     >>> fun(1.23)
     0.615

   Khi không có implementation nào được đăng ký cho một kiểu cụ thể, method resolution order của kiểu đó được sử dụng để tìm một implementation tổng quát hơn. Hàm gốc được áp dụng ``@singledispatch`` được đăng ký cho kiểu :class:`object` cơ sở, nghĩa là nó sẽ được sử dụng nếu không tìm thấy implementation phù hợp hơn.

   Nếu một implementation được đăng ký cho :term:`abstract base class`, các virtual subclass của base class sẽ được dispatch đến implementation đó::

     >>> from collections.abc import Mapping
     >>> @fun.register
     ... def _(arg: Mapping, verbose=False):
     ...     if verbose:
     ...         print("Keys & Values")
     ...     for key, value in arg.items():
     ...         print(key, "=>", value)
     ...
     >>> fun({"a": "b"})
     a => b

   Để kiểm tra generic function sẽ chọn implementation nào cho một kiểu nhất định, hãy sử dụng thuộc tính ``dispatch()``::

     >>> fun.dispatch(float)
     <function fun_num at 0x1035a2840>
     >>> fun.dispatch(dict)    # ghi chú: triển khai mặc định
     <function fun at 0x103fe0000>

   Để truy cập tất cả các triển khai đã đăng ký, hãy sử dụng thuộc tính chỉ đọc ``registry``::

    >>> fun.registry.keys()
    dict_keys([<class 'NoneType'>, <class 'int'>, <class 'object'>,
              <class 'decimal.Decimal'>, <class 'list'>,
              <class 'float'>])
    >>> fun.registry[float]
    <function fun_num at 0x1035a2840>
    >>> fun.registry[object]
    <function fun at 0x103fe0000>

   .. versionadded:: 3.4

   .. versionchanged:: 3.7
      Thuộc tính :func:`~singledispatch.register` hiện hỗ trợ sử dụng type annotations.

   .. versionchanged:: 3.11
      Thuộc tính :func:`~singledispatch.register` hiện hỗ trợ
      :class:`typing.Union` làm type annotation.


.. class:: singledispatchmethod(func)

   Chuyển một phương thức thành một :term:`single-dispatch <single dispatch>` :term:`generic function`.

   Để định nghĩa một phương thức generic, hãy trang trí phương thức đó bằng decorator ``@singledispatchmethod``. Khi định nghĩa một phương thức bằng ``@singledispatchmethod``, hãy lưu ý rằng việc dispatch diễn ra dựa trên kiểu của đối số đầu tiên không phải *self* hoặc không phải *cls*::

    class Negator:
        @singledispatchmethod
        def neg(self, arg):
            raise NotImplementedError("Cannot negate a")

        @neg.register
        def _(self, arg: int):
            return -arg

        @neg.register
        def _(self, arg: bool):
            return not arg

   ``@singledispatchmethod`` hỗ trợ việc lồng với các decorator khác, chẳng hạn như
   :deco:`classmethod`. Lưu ý rằng để cho phép ``dispatcher.register``, ``singledispatchmethod`` phải là decorator *ngoài cùng*. Đây là lớp ``Negator`` với các phương thức ``neg`` được liên kết với lớp, thay vì với một thể hiện của lớp::

    class Negator:
        @singledispatchmethod
        @classmethod
        def neg(cls, arg):
            raise NotImplementedError("Cannot negate a")

        @neg.register
        @classmethod
        def _(cls, arg: int):
            return -arg

        @neg.register
        @classmethod
        def _(cls, arg: bool):
            return not arg

   Có thể sử dụng cùng một mẫu cho các decorator tương tự khác:
   :deco:`staticmethod`, :deco:`~abc.abstractmethod` và các decorator khác.

   .. versionadded:: 3.8


.. function:: update_wrapper(wrapper, wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES)

   Cập nhật một hàm *wrapper* để trông giống hàm *wrapped*. Các đối số tùy chọn là các tuple dùng để chỉ định những thuộc tính nào của hàm gốc được gán trực tiếp cho các thuộc tính tương ứng trên hàm wrapper, và những thuộc tính nào của hàm wrapper được cập nhật bằng các thuộc tính tương ứng từ hàm gốc. Giá trị mặc định cho các đối số này là các hằng số cấp mô-đun ``WRAPPER_ASSIGNMENTS`` (gán cho hàm wrapper các thuộc tính :attr:`~function.__module__`, :attr:`~function.__name__` và
   :attr:`~function.__qualname__`, :attr:`~function.__annotations__`,
   :attr:`~function.__type_params__`, và :attr:`~function.__doc__`, chuỗi tài liệu) và ``WRAPPER_UPDATES`` (cập nhật :attr:`~function.__dict__` của hàm wrapper, tức là dictionary của instance).

   Để cho phép truy cập vào hàm gốc nhằm phục vụ việc introspection và các mục đích khác (ví dụ: bỏ qua một caching decorator như :deco:`lru_cache`), hàm này tự động thêm thuộc tính ``__wrapped__`` vào wrapper, thuộc tính này tham chiếu đến hàm đang được bọc.

   Mục đích sử dụng chính của hàm này là trong các hàm :term:`decorator`, vốn bọc hàm được trang trí và trả về wrapper. Nếu hàm wrapper không được cập nhật, metadata của hàm được trả về sẽ phản ánh định nghĩa của wrapper thay vì định nghĩa của hàm gốc, điều này thường không hữu ích lắm.

   :func:`update_wrapper` có thể được sử dụng với các callable không phải là hàm. Mọi thuộc tính được nêu tên trong *assigned* hoặc *updated* nhưng bị thiếu trong đối tượng được bọc đều sẽ bị bỏ qua (nghĩa là hàm này sẽ không cố gắng đặt chúng trên hàm wrapper). :exc:`AttributeError` vẫn được phát sinh nếu bản thân hàm wrapper thiếu bất kỳ thuộc tính nào được nêu tên trong *updated*.

   .. versionchanged:: 3.2
      Thuộc tính ``__wrapped__`` hiện được tự động thêm vào. Thuộc tính :attr:`~function.__annotations__` hiện được sao chép theo mặc định. Các thuộc tính bị thiếu không còn gây ra :exc:`AttributeError`.

   .. versionchanged:: 3.4
      Thuộc tính ``__wrapped__`` hiện luôn tham chiếu đến hàm được bọc, ngay cả khi hàm đó đã định nghĩa thuộc tính ``__wrapped__``. (xem :issue:`17482`)

   .. versionchanged:: 3.12
      Thuộc tính :attr:`~function.__type_params__` hiện được sao chép theo mặc định.


.. decorator:: wraps(wrapped, assigned=WRAPPER_ASSIGNMENTS, updated=WRAPPER_UPDATES)

   Đây là một hàm tiện ích để gọi :func:`update_wrapper` như một function decorator khi định nghĩa hàm wrapper. Nó tương đương với ``partial(update_wrapper, wrapped=wrapped, assigned=assigned, updated=updated)``. Ví dụ::

      >>> from functools import wraps
      >>> def my_decorator(f):
      ...     @wraps(f)
      ...     def wrapper(*args, **kwds):
      ...         print('Calling decorated function')
      ...         return f(*args, **kwds)
      ...     return wrapper
      ...
      >>> @my_decorator
      ... def example():
      ...     """Docstring"""
      ...     print('Called example function')
      ...
      >>> example()
      Calling decorated function
      Called example function
      >>> example.__name__
      'example'
      >>> example.__doc__
      'Docstring'

   Nếu không sử dụng decorator factory này, tên của hàm ví dụ sẽ là ``'wrapper'``, và docstring của :func:`!example` gốc sẽ bị mất.


.. _partial-objects:

:class:`partial` Đối tượng
--------------------------

Các đối tượng :class:`partial` là những đối tượng có thể gọi được, được tạo bởi :func:`partial`. Chúng có ba thuộc tính chỉ đọc:


.. attribute:: partial.func

   Một đối tượng hoặc hàm có thể gọi được. Các lệnh gọi đến đối tượng :class:`partial` sẽ được chuyển tiếp đến :attr:`func` cùng với các đối số và từ khóa mới.


.. attribute:: partial.args

   Các đối số vị trí ở ngoài cùng bên trái sẽ được thêm vào trước các đối số vị trí được cung cấp khi gọi đối tượng :class:`partial`.


.. attribute:: partial.keywords

   Các đối số từ khóa sẽ được cung cấp khi đối tượng :class:`partial` được gọi.

Các đối tượng :class:`partial` tương tự như :ref:`đối tượng hàm <user-defined-funcs>` ở chỗ chúng có thể gọi được, có thể được tham chiếu yếu và có thể có các thuộc tính. Tuy nhiên, có một số khác biệt quan trọng. Chẳng hạn, các thuộc tính :attr:`~definition.__name__` và :attr:`~definition.__doc__` không được tự động tạo.

.. _`"memoize"`: https://en.wikipedia.org/wiki/Memoization
.. _`LRU (least recently used) cache`: https://en.wikipedia.org/wiki/Cache_replacement_policies#Least_Recently_Used_(LRU)
.. _`Fibonacci numbers`: https://en.wikipedia.org/wiki/Fibonacci_number
.. _`dynamic programming`: https://en.wikipedia.org/wiki/Dynamic_programming
