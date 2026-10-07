:mod:`!enum` --- Hỗ trợ kiểu liệt kê
====================================

.. module:: enum
   :synopsis: Triển khai một lớp enumeration.

.. moduleauthor:: Ethan Furman <ethan@stoneleaf.us>
.. sectionauthor:: Barry Warsaw <barry@python.org>
.. sectionauthor:: Eli Bendersky <eliben@gmail.com>
.. sectionauthor:: Ethan Furman <ethan@stoneleaf.us>

.. versionadded:: 3.4

**Mã nguồn:** :source:`Lib/enum.py`

.. sidebar:: Quan trọng

   Trang này chứa thông tin tham chiếu API. Để xem thông tin hướng dẫn và thảo luận về các chủ đề nâng cao hơn, hãy xem

   * :ref:`Hướng dẫn cơ bản <enum-basic-tutorial>`
   * :ref:`Hướng dẫn nâng cao <enum-advanced-tutorial>`
   * :ref:`Cẩm nang Enum <enum-cookbook>`

---------------

Một enumeration:

* là một tập hợp các tên tượng trưng (thành viên) được liên kết với các giá trị duy nhất
* có thể được lặp qua để trả về các thành viên chính tắc (tức là không phải bí danh) theo thứ tự định nghĩa
* sử dụng cú pháp *call* để trả về các thành viên theo giá trị
* sử dụng cú pháp *index* để trả về các thành viên theo tên

Enumeration được tạo entweder bằng cách sử dụng cú pháp :keyword:`class`, hoặc bằng cú pháp gọi hàm::

   >>> from enum import Enum

   >>> # cú pháp lớp
   >>> class Color(Enum):
   ...     RED = 1
   ...     GREEN = 2
   ...     BLUE = 3

   >>> # cú pháp hàm
   >>> Color = Enum('Color', [('RED', 1), ('GREEN', 2), ('BLUE', 3)])

Mặc dù chúng ta có thể sử dụng :keyword:`class` cú pháp để tạo Enum, Enum không phải là các lớp Python thông thường. Xem
:ref:`Các Enum khác biệt như thế nào? <enum-class-differences>` để biết thêm chi tiết.

.. note:: Thuật ngữ

   - Lớp :class:`!Color` là một *enumeration* (hay *enum*)
   - Các thuộc tính :attr:`!Color.RED`, :attr:`!Color.GREEN`, v.v. là *các thành viên enumeration* (hay *member*) và về chức năng là các hằng số.
   - Các thành viên enum có *tên* và *giá trị* (tên của
     :attr:`!Color.RED` là ``RED``, giá trị của :attr:`!Color.BLUE` là ``3``, v.v.)

---------------

Nội dung mô-đun
---------------

   :class:`EnumType`

      ``type`` của Enum và các lớp con của nó.

   :class:`Enum`

      Lớp cơ sở để tạo các hằng số liệt kê.

   :class:`IntEnum`

      Lớp cơ sở để tạo các hằng số liệt kê đồng thời là các lớp con của :class:`int`. (`Notes`_)

   :class:`StrEnum`

      Lớp cơ sở để tạo các hằng số liệt kê đồng thời là các lớp con của :class:`str`. (`Notes`_)

   :class:`Flag`

      Lớp cơ sở để tạo các hằng số liệt kê có thể được kết hợp bằng các phép toán bitwise mà không làm mất tính thành viên :class:`Flag` của chúng.

   :class:`IntFlag`

      Lớp cơ sở để tạo các hằng số liệt kê có thể được kết hợp bằng các toán tử bitwise mà không làm mất tính thành viên :class:`IntFlag` của chúng.
      Các thành viên :class:`IntFlag` cũng là các lớp con của :class:`int`. (`Notes`_)

   :class:`ReprEnum`

      Được :class:`IntEnum`, :class:`StrEnum` và :class:`IntFlag` sử dụng để giữ lại :class:`str() <str>` của kiểu được trộn vào.

   :class:`EnumCheck`

      Một kiểu liệt kê có các giá trị ``CONTINUOUS``, ``NAMED_FLAGS`` và ``UNIQUE``, được dùng với :func:`verify` để đảm bảo một kiểu liệt kê nhất định đáp ứng nhiều ràng buộc khác nhau.

   :class:`FlagBoundary`

      Một kiểu liệt kê có các giá trị ``STRICT``, ``CONFORM``, ``EJECT`` và ``KEEP``, cho phép kiểm soát chi tiết hơn cách xử lý các giá trị không hợp lệ trong một kiểu liệt kê.

   :class:`EnumDict`

      Một lớp con của :class:`dict`, được dùng khi tạo lớp con của :class:`EnumType`.

   :class:`auto`

      Các instance được thay thế bằng một giá trị thích hợp cho các thành viên Enum.
      :class:`StrEnum` mặc định là phiên bản viết thường của tên thành viên, trong khi các Enum khác mặc định là 1 và tăng dần từ đó.

   :deco:`~enum.property`

      Cho phép các thành viên :class:`Enum` có các thuộc tính mà không xung đột với tên thành viên. Các thuộc tính ``value`` và ``name`` được triển khai theo cách này.

   :deco:`unique`

      Decorator lớp Enum đảm bảo chỉ một tên duy nhất được liên kết với mỗi giá trị.

   :deco:`verify`

      Decorator lớp Enum kiểm tra các ràng buộc do người dùng lựa chọn trên một enumeration.

   :deco:`member`

      Biến ``obj`` thành một thành viên. Có thể được sử dụng làm decorator.

   :deco:`nonmember`

      Không biến ``obj`` thành một thành viên. Có thể được sử dụng làm decorator.

   :deco:`global_enum`

      Sửa đổi :class:`str() <str>` và :func:`repr` của một enum để hiển thị các thành viên của nó là thuộc về module thay vì class của nó, đồng thời export các thành viên enum vào global namespace.

   :func:`show_flag_values`

      Trả về danh sách tất cả các số nguyên là lũy thừa của hai có trong một flag.

   :func:`enum.bin`

      Tương tự :func:`bin` tích hợp sẵn, ngoại trừ các giá trị âm được biểu diễn theo bù hai, và bit đầu tiên luôn biểu thị dấu (``0`` nghĩa là dương, ``1`` nghĩa là âm).


.. versionadded:: 3.6  ``Flag``, ``IntFlag``, ``auto``
.. versionadded:: 3.11  ``StrEnum``, ``EnumCheck``, ``ReprEnum``, ``FlagBoundary``, ``property``, ``member``, ``nonmember``, ``global_enum``, ``show_flag_values``
.. versionadded:: 3.13  ``EnumDict``

---------------

Kiểu dữ liệu
------------


.. class:: EnumType

   *EnumType* là :term:`metaclass` cho các enumeration *enum*. Có thể tạo subclass của *EnumType* -- xem :ref:`Subclassing EnumType <enumtype-examples>` để biết chi tiết.

   ``EnumType`` chịu trách nhiệm thiết lập đúng :meth:`!__repr__`,
   các phương thức :meth:`!__str__`, :meth:`!__format__` và :meth:`!__reduce__` trên *enum* cuối cùng, cũng như tạo các thành viên enum, xử lý đúng các thành viên trùng lặp, cung cấp khả năng lặp qua enum class, v.v.

   .. versionadded:: 3.11

      Trước phiên bản 3.11, ``EnumType`` được gọi là ``EnumMeta``, tên này vẫn có thể được sử dụng như một bí danh.

   .. method:: EnumType.__call__(cls, value, names=None, *, module=None, qualname=None, type=None, start=1, boundary=None)

      Phương thức này được gọi theo hai cách khác nhau:

      * để tra cứu một member hiện có:

         :cls:   Lớp enum đang được gọi.
         :value: Giá trị cần tra cứu.

      * để sử dụng enum ``cls`` nhằm tạo một enum mới (chỉ khi enum hiện có không có member nào):

         :cls:   Lớp enum đang được gọi.
         :value: Tên của Enum mới cần tạo.
         :names: Tên/giá trị của các thành viên cho Enum mới.
         :module:    Tên của module mà Enum mới được tạo trong đó.
         :qualname:  Vị trí thực tế trong module nơi có thể tìm thấy Enum này.
         :type:  Một kiểu mix-in cho Enum mới.
         :start: Giá trị số nguyên đầu tiên cho Enum (được :class:`auto` sử dụng).
         :boundary:  Cách xử lý các giá trị nằm ngoài phạm vi từ các phép toán bit (chỉ :class:`Flag`).

   .. method:: EnumType.__contains__(cls, member)

      Trả về ``True`` nếu thành viên thuộc ``cls``::

        >>> some_var = Color.RED
        >>> some_var in Color
        True
        >>> Color.RED.value in Color
        True

      .. versionchanged:: 3.12

         Trước Python 3.12, một ``TypeError`` được đưa ra nếu một đối tượng không phải thành viên Enum được sử dụng trong phép kiểm tra chứa.

   .. method:: EnumType.__dir__(cls)

      Trả về ``['__class__', '__doc__', '__members__', '__module__']`` và tên của các thành viên trong *cls*::

        >>> dir(Color)
        ['BLUE', 'GREEN', 'RED', '__class__', '__contains__', '__doc__', '__getitem__', '__init_subclass__', '__iter__', '__len__', '__members__', '__module__', '__name__', '__qualname__']

   .. method:: EnumType.__getitem__(cls, name)

      Trả về thành viên Enum trong *cls* khớp với *name*, hoặc đưa ra một :exc:`KeyError`::

        >>> Color['BLUE']
        <Color.BLUE: 3>

   .. method:: EnumType.__iter__(cls)

      Trả về từng thành viên trong *cls* theo thứ tự định nghĩa::

        >>> list(Color)
        [<Color.RED: 1>, <Color.GREEN: 2>, <Color.BLUE: 3>]

   .. method:: EnumType.__len__(cls)

      Trả về số lượng thành viên trong *cls*::

        >>> len(Color)
        3

   .. attribute:: EnumType.__members__

      Trả về ánh xạ từ mọi tên enum đến thành viên tương ứng, bao gồm cả bí danh

   .. method:: EnumType.__reversed__(cls)

      Trả về từng thành viên trong *cls* theo thứ tự định nghĩa ngược::

        >>> list(reversed(Color))
        [<Color.BLUE: 3>, <Color.GREEN: 2>, <Color.RED: 1>]


.. class:: Enum

   *Enum* là lớp cơ sở cho tất cả các enumeration *enum*.

   .. attribute:: Enum.name

      Tên được dùng để định nghĩa thành viên ``Enum``::

        >>> Color.BLUE.name
        'BLUE'

   .. attribute:: Enum.value

      Giá trị được gán cho thành viên ``Enum``::

         >>> Color.RED.value
         1

      Giá trị của thành viên, có thể được đặt trong :meth:`~Enum.__new__`.

      .. note:: Giá trị thành viên của Enum

         Giá trị thành viên có thể là bất kỳ thứ gì: :class:`int`, :class:`str`, v.v. Nếu giá trị cụ thể không quan trọng, bạn có thể sử dụng các instance :class:`auto` và một giá trị phù hợp sẽ được tự động chọn cho bạn. Xem :class:`auto` để biết chi tiết.

         Mặc dù có thể sử dụng các giá trị có thể thay đổi/không thể băm (mutable/unhashable), chẳng hạn như :class:`dict`, :class:`list` hoặc một :class:`~dataclasses.dataclass` có thể thay đổi, nhưng chúng sẽ làm giảm hiệu năng theo cấp số nhân trong quá trình tạo, tương ứng với tổng số giá trị có thể thay đổi/không thể băm trong enum.

   .. attribute:: Enum._name_

      Tên của member.

   .. attribute:: Enum._value_

      Giá trị của thành viên, có thể được đặt trong :meth:`~Enum.__new__`.

   .. attribute:: Enum._order_

      Không còn được sử dụng, được giữ lại để tương thích ngược. (class attribute, bị xóa trong quá trình tạo class).

      Có thể cung cấp attribute :attr:`~Enum._order_` để giúp giữ cho code Python 2 / Python 3 đồng bộ. Attribute này sẽ được kiểm tra với thứ tự thực tế của enumeration và sẽ phát sinh lỗi nếu hai thứ không khớp::

         >>> class Color(Enum):
         ...     _order_ = 'RED GREEN BLUE'
         ...     RED = 1
         ...     BLUE = 3
         ...     GREEN = 2
         ...
         Traceback (most recent call last):
         ...
         TypeError: member order does not match _order_:
            ['RED', 'BLUE', 'GREEN']
            ['RED', 'GREEN', 'BLUE']

      .. note::

         Trong code Python 2, attribute :attr:`~Enum._order_` là cần thiết vì thứ tự định nghĩa bị mất trước khi có thể được ghi lại.

      .. versionadded:: 3.6

   .. attribute:: Enum._ignore_

      ``_ignore_`` chỉ được sử dụng trong quá trình tạo và bị xóa khỏi enumeration sau khi quá trình tạo hoàn tất.

      ``_ignore_`` là danh sách các tên sẽ không trở thành thành viên và tên của chúng cũng sẽ bị loại khỏi phép liệt kê hoàn chỉnh. Xem
      :ref:`TimePeriod <enum-time-period>` để xem ví dụ.

      .. versionadded:: 3.7

   .. method:: Enum.__dir__(self)

      Trả về ``['__class__', '__doc__', '__module__', 'name', 'value']`` và mọi phương thức công khai được định nghĩa trên *self.__class__*::

         >>> from enum import Enum
         >>> import datetime as dt
         >>> class Weekday(Enum):
         ...     MONDAY = 1
         ...     TUESDAY = 2
         ...     WEDNESDAY = 3
         ...     THURSDAY = 4
         ...     FRIDAY = 5
         ...     SATURDAY = 6
         ...     SUNDAY = 7
         ...     @classmethod
         ...     def today(cls):
         ...         print(f'today is {cls(dt.date.today().isoweekday()).name}')
         ...
         >>> dir(Weekday.SATURDAY)
         ['__class__', '__doc__', '__eq__', '__hash__', '__module__', 'name', 'today', 'value']

   .. method:: Enum._generate_next_value_(name, start, count, last_values)

         :name: Tên của thành viên đang được định nghĩa (ví dụ: 'RED').
         :start: Giá trị bắt đầu cho Enum; mặc định là 1.
         :count: Số lượng thành viên hiện được định nghĩa, không bao gồm thành viên này.
         :last_values: Danh sách các giá trị trước đó.

      Một *staticmethod* được sử dụng để xác định giá trị tiếp theo được trả về bởi
      :class:`auto`.

      .. note::
         Đối với các lớp :class:`Enum` tiêu chuẩn, giá trị tiếp theo được chọn là giá trị cao nhất đã thấy cộng thêm một.

         Đối với các lớp :class:`Flag`, giá trị tiếp theo được chọn sẽ là lũy thừa của hai nhỏ nhất tiếp theo.

      Có thể ghi đè phương thức này, ví dụ:::

         >>> from enum import auto, Enum
         >>> class PowersOfThree(Enum):
         ...     @staticmethod
         ...     def _generate_next_value_(name, start, count, last_values):
         ...         return 3 ** (count + 1)
         ...     FIRST = auto()
         ...     SECOND = auto()
         ...
         >>> PowersOfThree.SECOND.value
         9

      .. versionadded:: 3.6
      .. versionchanged:: 3.13
         Các phiên bản trước đây sẽ sử dụng giá trị được thấy gần nhất thay vì giá trị cao nhất.

   .. method:: Enum.__init__(self, *args, **kwds)

      Theo mặc định, phương thức này không làm gì. Nếu phép gán thành viên cung cấp nhiều giá trị, các giá trị đó trở thành các đối số riêng biệt của ``__init__``; ví dụ:

         >>> from enum import Enum
         >>> class Weekday(Enum):
         ...     MONDAY = 1, 'Mon'

      ``Weekday.__init__()`` sẽ được gọi như sau: ``Weekday.__init__(self, 1, 'Mon')``

   .. method:: Enum.__init_subclass__(cls, **kwds)

      Một *classmethod* được dùng để cấu hình thêm cho các lớp con tiếp theo. Theo mặc định, không thực hiện gì.

   .. method:: Enum._missing_(cls, value)

      Một *classmethod* dùng để tra cứu các giá trị không tìm thấy trong *cls*. Theo mặc định, phương thức này không thực hiện gì, nhưng có thể được ghi đè để triển khai hành vi tìm kiếm tùy chỉnh::

         >>> from enum import auto, StrEnum
         >>> class Build(StrEnum):
         ...     DEBUG = auto()
         ...     OPTIMIZED = auto()
         ...     @classmethod
         ...     def _missing_(cls, value):
         ...         value = value.lower()
         ...         for member in cls:
         ...             if member.value == value:
         ...                 return member
         ...         return None
         ...
         >>> Build.DEBUG.value
         'debug'
         >>> Build('deBUG')
         <Build.DEBUG: 'debug'>

      .. versionadded:: 3.6

   .. method:: Enum.__new__(cls, *args, **kwds)

      Theo mặc định, không tồn tại. Nếu được chỉ định trong định nghĩa lớp enum hoặc trong một lớp mixin (chẳng hạn như ``int``), tất cả các giá trị được cung cấp trong phép gán member sẽ được truyền vào; ví dụ:

         >>> from enum import Enum
         >>> class MyIntEnum(int, Enum):
         ...     TWENTYSIX = '1a', 16

      dẫn đến lời gọi ``int('1a', 16)`` và giá trị ``26`` cho member.

      .. note::

         Khi viết ``__new__`` tùy chỉnh, không sử dụng ``super().__new__`` -- hãy gọi ``__new__`` thích hợp thay thế.

   .. method:: Enum.__repr__(self)

      Trả về chuỗi được dùng cho các lời gọi *repr()*. Theo mặc định, trả về tên *Enum*, tên member và giá trị, nhưng có thể được ghi đè::

         >>> from enum import auto, Enum
         >>> class OtherStyle(Enum):
         ...     ALTERNATE = auto()
         ...     OTHER = auto()
         ...     SOMETHING_ELSE = auto()
         ...     def __repr__(self):
         ...         cls_name = self.__class__.__name__
         ...         return f'{cls_name}.{self.name}'
         ...
         >>> OtherStyle.ALTERNATE, str(OtherStyle.ALTERNATE), f"{OtherStyle.ALTERNATE}"
         (OtherStyle.ALTERNATE, 'OtherStyle.ALTERNATE', 'OtherStyle.ALTERNATE')

   .. method:: Enum.__str__(self)

      Trả về chuỗi được dùng cho các lời gọi *str()*. Theo mặc định, trả về tên *Enum* và tên member, nhưng có thể được ghi đè::

         >>> from enum import auto, Enum
         >>> class OtherStyle(Enum):
         ...     ALTERNATE = auto()
         ...     OTHER = auto()
         ...     SOMETHING_ELSE = auto()
         ...     def __str__(self):
         ...         return f'{self.name}'
         ...
         >>> OtherStyle.ALTERNATE, str(OtherStyle.ALTERNATE), f"{OtherStyle.ALTERNATE}"
         (<OtherStyle.ALTERNATE: 1>, 'ALTERNATE', 'ALTERNATE')

   .. method:: Enum.__format__(self)

      Trả về chuỗi được sử dụng cho các lệnh gọi *format()* và *f-string*. Theo mặc định, trả về giá trị :meth:`__str__`, nhưng có thể ghi đè::

         >>> from enum import auto, Enum
         >>> class OtherStyle(Enum):
         ...     ALTERNATE = auto()
         ...     OTHER = auto()
         ...     SOMETHING_ELSE = auto()
         ...     def __format__(self, spec):
         ...         return f'{self.name}'
         ...
         >>> OtherStyle.ALTERNATE, str(OtherStyle.ALTERNATE), f"{OtherStyle.ALTERNATE}"
         (<OtherStyle.ALTERNATE: 1>, 'OtherStyle.ALTERNATE', 'ALTERNATE')

   .. note::

      Khi sử dụng :class:`auto` với :class:`Enum`, kết quả là các số nguyên có giá trị tăng dần, bắt đầu từ ``1``.

   .. versionchanged:: 3.12 Đã thêm :ref:`enum-dataclass-support`

   .. method:: Enum._add_alias_

      Thêm một tên mới làm bí danh cho một thành viên hiện có::

         >>> Color.RED._add_alias_("ERROR")
         >>> Color.ERROR
         <Color.RED: 1>

      Nêu ra một :exc:`NameError` nếu tên đã được gán cho một thành viên khác.

      .. versionadded:: 3.13

   .. method:: Enum._add_value_alias_

      Thêm một giá trị mới làm bí danh cho một thành viên hiện có::

         >>> Color.RED._add_value_alias_(42)
         >>> Color(42)
         <Color.RED: 1>

      | Nêu ra một :exc:`ValueError` nếu giá trị đã được liên kết với một thành viên khác.
      | Xem :ref:`multi-value-enum` để biết ví dụ.

      .. versionadded:: 3.13


.. class:: IntEnum

   *IntEnum* giống như :class:`Enum`, nhưng các thành viên của nó cũng là số nguyên và có thể được sử dụng ở bất kỳ nơi nào có thể sử dụng số nguyên. Nếu thực hiện bất kỳ phép toán số nguyên nào với một thành viên *IntEnum*, giá trị kết quả sẽ không còn thuộc enumeration.

      >>> from enum import IntEnum
      >>> class Number(IntEnum):
      ...     ONE = 1
      ...     TWO = 2
      ...     THREE = 3
      ...
      >>> Number.THREE
      <Number.THREE: 3>
      >>> Number.ONE + Number.TWO
      3
      >>> Number.THREE + 5
      8
      >>> Number.THREE == 3
      True

   .. note::

      Sử dụng :class:`auto` với :class:`IntEnum` sẽ tạo ra các số nguyên có giá trị tăng dần, bắt đầu từ ``1``.

   .. versionchanged:: 3.11 :meth:`~object.__str__` hiện đã :meth:`!int.__str__` để
      hỗ trợ tốt hơn trường hợp sử dụng *thay thế các hằng số hiện có*.
      :meth:`~object.__format__` đã được :meth:`!int.__format__` vì cùng lý do đó.


.. class:: StrEnum

   *StrEnum* giống như :class:`Enum`, nhưng các thành viên của nó cũng là chuỗi và có thể được sử dụng ở hầu hết những nơi có thể sử dụng chuỗi. Kết quả của bất kỳ thao tác chuỗi nào được thực hiện trên hoặc với một thành viên *StrEnum* đều không thuộc enumeration.

   >>> from enum import StrEnum, auto
   >>> class Color(StrEnum):
   ...     RED = 'r'
   ...     GREEN = 'g'
   ...     BLUE = 'b'
   ...     UNKNOWN = auto()
   ...
   >>> Color.RED
   <Color.RED: 'r'>
   >>> Color.UNKNOWN
   <Color.UNKNOWN: 'unknown'>
   >>> str(Color.UNKNOWN)
   'unknown'

   .. note::

      Trong stdlib có những nơi kiểm tra một :class:`str` chính xác thay vì một lớp con của :class:`str` (tức là ``type(unknown) == str`` thay vì ``isinstance(unknown, str)``), và tại những nơi đó, bạn cần sử dụng ``str(MyStrEnum.MY_MEMBER)``.

   .. note::

      Việc sử dụng :class:`auto` với :class:`StrEnum` sẽ cho ra tên thành viên viết thường làm giá trị.

   .. note::

      :meth:`~object.__str__` được :meth:`!str.__str__` để hỗ trợ tốt hơn trường hợp sử dụng *replacement of existing constants*. :meth:`~object.__format__` cũng vậy
      :meth:`!str.__format__` vì cùng lý do đó.

   .. versionadded:: 3.11

.. class:: Flag

   ``Flag`` giống với :class:`Enum`, nhưng các thành viên của nó hỗ trợ các toán tử bitwise ``&`` (*AND*), ``|`` (*OR*), ``^`` (*XOR*) và ``~`` (*INVERT*); kết quả của các phép toán đó là (bí danh của) các thành viên trong enumeration.

   .. method:: __contains__(self, value)

      Trả về *True* nếu value nằm trong self::

         >>> from enum import Flag, auto
         >>> class Color(Flag):
         ...     RED = auto()
         ...     GREEN = auto()
         ...     BLUE = auto()
         ...
         >>> purple = Color.RED | Color.BLUE
         >>> white = Color.RED | Color.GREEN | Color.BLUE
         >>> Color.GREEN in purple
         False
         >>> Color.GREEN in white
         True
         >>> purple in white
         True
         >>> white in purple
         False

   .. method:: __iter__(self)

      Trả về tất cả các thành viên được chứa, không phải bí danh::

         >>> list(Color.RED)
         [<Color.RED: 1>]
         >>> list(purple)
         [<Color.RED: 1>, <Color.BLUE: 4>]

      .. versionadded:: 3.11

   .. method:: __len__(self)

      Trả về số lượng thành viên trong cờ::

         >>> len(Color.GREEN)
         1
         >>> len(white)
         3

      .. versionadded:: 3.11

   .. method:: __bool__(self)

      Trả về *True* nếu cờ có bất kỳ thành viên nào, nếu không thì trả về *False*::

         >>> bool(Color.GREEN)
         True
         >>> bool(white)
         True
         >>> black = Color(0)
         >>> bool(black)
         False

   .. method:: __or__(self, other)

      Trả về kết quả OR nhị phân của cờ hiện tại với giá trị khác::

         >>> Color.RED | Color.GREEN
         <Color.RED|GREEN: 3>

   .. method:: __and__(self, other)

      Trả về kết quả AND nhị phân của cờ hiện tại với giá trị khác::

         >>> purple & white
         <Color.RED|BLUE: 5>
         >>> purple & Color.GREEN
         <Color: 0>

   .. method:: __xor__(self, other)

      Trả về kết quả XOR nhị phân của cờ hiện tại với giá trị khác::

         >>> purple ^ white
         <Color.GREEN: 2>
         >>> purple ^ Color.GREEN
         <Color.RED|GREEN|BLUE: 7>

   .. method:: __invert__(self)

      Trả về tất cả các cờ trong *type(self)* không có trong *self*::

         >>> ~white
         <Color: 0>
         >>> ~purple
         <Color.GREEN: 2>
         >>> ~Color.RED
         <Color.GREEN|BLUE: 6>

   .. method:: _numeric_repr_

      Hàm được dùng để định dạng mọi giá trị số còn lại chưa được đặt tên. Mặc định là repr của giá trị; các lựa chọn phổ biến là :func:`hex` và :func:`oct`.

   .. note::

      Việc sử dụng :class:`auto` với :class:`Flag` tạo ra các số nguyên là lũy thừa của hai, bắt đầu từ ``1``.

   .. versionchanged:: 3.11 *repr()* của các flag có giá trị bằng không đã thay đổi. Nó
      hiện là:

         >>> Color(0) # doctest: +SKIP
         <Color: 0>

.. class:: IntFlag

   ``IntFlag`` giống với :class:`Flag`, nhưng các phần tử của nó cũng là số nguyên và có thể được sử dụng ở bất cứ nơi nào có thể sử dụng một số nguyên.

      >>> from enum import IntFlag, auto
      >>> class Color(IntFlag):
      ...     RED = auto()
      ...     GREEN = auto()
      ...     BLUE = auto()
      ...
      >>> Color.RED & 2
      <Color: 0>
      >>> Color.RED | 2
      <Color.RED|GREEN: 3>

   Nếu thực hiện bất kỳ phép toán số nguyên nào với một phần tử *IntFlag*, kết quả không phải là một *IntFlag*::

        >>> Color.RED + 2
        3

   Nếu thực hiện phép :class:`Flag` với một phần tử *IntFlag* và:

   * kết quả là một *IntFlag* hợp lệ: một *IntFlag* được trả về
   * kết quả không phải là một *IntFlag* hợp lệ: kết quả phụ thuộc vào thiết lập :class:`FlagBoundary`

   :func:`repr` của các flag không có tên có giá trị bằng không đã thay đổi. Hiện tại nó là::

      >>> Color(0)
      <Color: 0>

   .. note::

      Việc sử dụng :class:`auto` với :class:`IntFlag` tạo ra các số nguyên là lũy thừa của hai, bắt đầu từ ``1``.

   .. versionchanged:: 3.11

      :meth:`~object.__str__` hiện :meth:`!int.__str__` để hỗ trợ tốt hơn trường hợp sử dụng *thay thế các hằng số hiện có*. :meth:`~object.__format__` đã :meth:`!int.__format__` vì cùng lý do đó.

      Phép đảo của một :class:`!IntFlag` hiện trả về một giá trị dương là hợp của tất cả các flag không có trong flag đã cho, thay vì một giá trị âm. Điều này phù hợp với hành vi :class:`Flag` hiện có.

.. class:: ReprEnum

   :class:`!ReprEnum` sử dụng :meth:`repr() <Enum.__repr__>` của :class:`Enum`, nhưng sử dụng :class:`str() <str>` của kiểu dữ liệu được trộn vào:

   * :meth:`!int.__str__` cho :class:`IntEnum` và :class:`IntFlag`
   * :meth:`!str.__str__` cho :class:`StrEnum`

   Kế thừa từ :class:`!ReprEnum` để giữ lại :class:`str() <str>` / :func:`format` của kiểu dữ liệu được trộn vào thay vì sử dụng
   :class:`Enum`-mặc định :meth:`str() <Enum.__str__>`.


   .. versionadded:: 3.11

.. class:: EnumCheck

   *EnumCheck* chứa các tùy chọn được decorator :func:`verify` sử dụng để đảm bảo nhiều ràng buộc; các ràng buộc không đạt sẽ dẫn đến một :exc:`ValueError`.

   .. attribute:: UNIQUE

      Đảm bảo mỗi giá trị chỉ có một tên::

         >>> from enum import Enum, verify, UNIQUE
         >>> @verify(UNIQUE)
         ... class Color(Enum):
         ...     RED = 1
         ...     GREEN = 2
         ...     BLUE = 3
         ...     CRIMSON = 1
         Traceback (most recent call last):
         ...
         ValueError: aliases found in <enum 'Color'>: CRIMSON -> RED


   .. attribute:: CONTINUOUS

      Đảm bảo không có giá trị nào bị thiếu giữa thành viên có giá trị thấp nhất và thành viên có giá trị cao nhất::

         >>> from enum import Enum, verify, CONTINUOUS
         >>> @verify(CONTINUOUS)
         ... class Color(Enum):
         ...     RED = 1
         ...     GREEN = 2
         ...     BLUE = 5
         Traceback (most recent call last):
         ...
         ValueError: invalid enum 'Color': missing values 3, 4

   .. attribute:: NAMED_FLAGS

      Đảm bảo rằng mọi nhóm/mask cờ chỉ chứa các cờ được đặt tên -- hữu ích khi các giá trị được chỉ định thay vì được tạo bởi :func:`auto`::

         >>> from enum import Flag, verify, NAMED_FLAGS
         >>> @verify(NAMED_FLAGS)
         ... class Color(Flag):
         ...     RED = 1
         ...     GREEN = 2
         ...     BLUE = 4
         ...     WHITE = 15
         ...     NEON = 31
         Traceback (most recent call last):
         ...
         ValueError: invalid Flag 'Color': aliases WHITE and NEON are missing combined values of 0x18 [use enum.show_flag_values(value) for details]

   .. note::

      CONTINUOUS và NAMED_FLAGS được thiết kế để hoạt động với các member có giá trị nguyên.

   .. versionadded:: 3.11

.. class:: FlagBoundary

   ``FlagBoundary`` kiểm soát cách xử lý các giá trị nằm ngoài phạm vi trong :class:`Flag` và các lớp con của nó.

   .. attribute:: STRICT

      Các giá trị nằm ngoài phạm vi khiến :exc:`ValueError` được phát sinh. Đây là giá trị mặc định cho :class:`Flag`::

         >>> from enum import Flag, STRICT, auto
         >>> class StrictFlag(Flag, boundary=STRICT):
         ...     RED = auto()
         ...     GREEN = auto()
         ...     BLUE = auto()
         ...
         >>> StrictFlag(2**2 + 2**4)
         Traceback (most recent call last):
         ...
         ValueError: <flag 'StrictFlag'> invalid value 20
             given 0b0 10100
           allowed 0b0 00111

   .. attribute:: CONFORM

      Các giá trị nằm ngoài phạm vi bị loại bỏ các giá trị không hợp lệ, để lại một giá trị :class:`Flag` hợp lệ::

         >>> from enum import Flag, CONFORM, auto
         >>> class ConformFlag(Flag, boundary=CONFORM):
         ...     RED = auto()
         ...     GREEN = auto()
         ...     BLUE = auto()
         ...
         >>> ConformFlag(2**2 + 2**4)
         <ConformFlag.BLUE: 4>

   .. attribute:: EJECT

      Các giá trị nằm ngoài phạm vi mất tư cách thành viên :class:`Flag` và trở về :class:`int`.

         >>> from enum import Flag, EJECT, auto
         >>> class EjectFlag(Flag, boundary=EJECT):
         ...     RED = auto()
         ...     GREEN = auto()
         ...     BLUE = auto()
         ...
         >>> EjectFlag(2**2 + 2**4)
         20

   .. attribute:: KEEP

      Các giá trị nằm ngoài phạm vi được giữ lại, đồng thời tư cách thành viên :class:`Flag` cũng được giữ lại. Đây là giá trị mặc định cho :class:`IntFlag`::

         >>> from enum import Flag, KEEP, auto
         >>> class KeepFlag(Flag, boundary=KEEP):
         ...     RED = auto()
         ...     GREEN = auto()
         ...     BLUE = auto()
         ...
         >>> KeepFlag(2**2 + 2**4)
         <KeepFlag.BLUE|16: 20>

   .. versionadded:: 3.11

.. class:: EnumDict

   *EnumDict* là một lớp con của :class:`dict` được dùng làm namespace để định nghĩa các lớp enum (xem :ref:`prepare`). Nó được cung cấp để cho phép tạo các lớp con của :class:`EnumType` với hành vi nâng cao, chẳng hạn như mỗi member có nhiều giá trị. Lớp này phải được gọi với tên của lớp enum đang được tạo; nếu không, các tên riêng tư và lớp nội bộ sẽ không được xử lý chính xác.

   Lưu ý rằng chỉ có interface :class:`~collections.abc.MutableMapping` (:meth:`~object.__setitem__` và :meth:`~dict.update`) được ghi đè. Có thể vượt qua các bước kiểm tra bằng cách sử dụng những thao tác :class:`!dict` khác như :meth:`|= <object.__ior__>`.

   .. attribute:: EnumDict.member_names

      Danh sách tên member.

   .. versionadded:: 3.13

---------------

.. _enum-dunder-sunder:

Các tên ``__dunder__`` được hỗ trợ
""""""""""""""""""""""""""""""""""

:attr:`~EnumType.__members__` là một ánh xạ có thứ tự, chỉ đọc, gồm các mục ``member_name``:``member``. Nó chỉ khả dụng trên class.

:meth:`~Enum.__new__`, nếu được chỉ định, phải tạo và trả về các enum member; đồng thời, bạn cũng nên đặt :attr:`~Enum._value_` của member một cách phù hợp. Sau khi tất cả member được tạo, nó sẽ không còn được sử dụng.


Các tên ``_sunder_`` được hỗ trợ
""""""""""""""""""""""""""""""""

- :attr:`~Enum._name_` -- tên của member
- :attr:`~Enum._value_` -- giá trị của member; có thể được đặt trong ``__new__``
- :meth:`~Enum._missing_` -- hàm tra cứu được dùng khi không tìm thấy giá trị; có thể được ghi đè
- :attr:`~Enum._ignore_` -- danh sách tên, ở dạng :class:`list` hoặc một
  :class:`str`, sẽ không được chuyển thành các member và sẽ bị xóa khỏi class cuối cùng
- :attr:`~Enum._order_` -- không còn được sử dụng, được giữ lại để tương thích ngược (thuộc tính class, bị xóa trong quá trình tạo class)

- :meth:`~Enum._generate_next_value_` -- được dùng để lấy giá trị phù hợp cho một enum member; có thể được ghi đè

- :meth:`~Enum._add_alias_` -- thêm một tên mới làm bí danh cho một member hiện có.
- :meth:`~Enum._add_value_alias_` -- thêm một giá trị mới làm bí danh cho một member hiện có.

- Mặc dù các tên ``_sunder_`` thường được dành riêng cho việc phát triển tiếp theo của lớp :class:`Enum` và không thể sử dụng, một số tên được cho phép rõ ràng:

  - ``_repr_*`` (ví dụ: ``_repr_html_``), được sử dụng trong `IPython's rich display <IPython's rich display_>`_

.. versionadded:: 3.6 ``_missing_``, ``_order_``, ``_generate_next_value_``
.. versionadded:: 3.7 ``_ignore_``
.. versionadded:: 3.13 ``_add_alias_``, ``_add_value_alias_``, ``_repr_*``
.. _`IPython's rich display`: https://ipython.readthedocs.io/en/stable/config/integrating.html#rich-display

---------------

Các tiện ích và decorator
-------------------------

.. class:: auto

   *auto* có thể được dùng thay cho một giá trị. Nếu được sử dụng, cơ chế *Enum* sẽ gọi :class:`Enum` của :meth:`~Enum._generate_next_value_` để lấy một giá trị phù hợp. Với :class:`Enum` và :class:`IntEnum`, giá trị phù hợp sẽ là giá trị cuối cùng cộng một; với :class:`Flag` và :class:`IntFlag`, đó sẽ là lũy thừa của hai nhỏ nhất lớn hơn giá trị cao nhất; với :class:`StrEnum`, đó sẽ là phiên bản viết thường của tên member. Cần thận trọng khi kết hợp *auto()* với các giá trị được chỉ định thủ công.

   Các instance *auto* chỉ được phân giải khi ở cấp cao nhất của một phép gán, либо tự nó hoặc là một phần của tuple:

   * ``FIRST = auto()`` sẽ hoạt động (auto() được thay thế bằng ``1``);
   * ``SECOND = auto(), -2`` sẽ hoạt động (auto được thay thế bằng ``2``, vì vậy ``2, -2`` được dùng để tạo member ``SECOND`` của enum;
   * ``THREE = [auto(), -3]`` sẽ *không* hoạt động (``[<auto instance>, -3]`` được dùng để tạo member ``THREE`` của enum)

   .. versionchanged:: 3.11.1

      Trong các phiên bản trước, ``auto()`` phải là thành phần duy nhất trên dòng phép gán thì mới hoạt động đúng cách.

   ``_generate_next_value_`` có thể được ghi đè để tùy chỉnh các giá trị được *auto* sử dụng.

   .. note:: trong 3.13, ``_generate_next_value_`` mặc định sẽ luôn trả về giá trị member cao nhất cộng thêm 1 và sẽ không thành công nếu bất kỳ member nào có kiểu không tương thích.

.. decorator:: property

   Một decorator tương tự như :deco:`property` tích hợp sẵn, nhưng dành riêng cho các enumeration. Nó cho phép các thuộc tính của member có cùng tên với chính các member đó.

   .. note:: *property* và member phải được định nghĩa trong các class riêng biệt; ví dụ, các thuộc tính *value* và *name* được định nghĩa trong class *Enum*, còn các subclass *Enum* có thể định nghĩa các member có tên ``value`` và ``name``.

   .. versionadded:: 3.11

.. decorator:: unique

   Một decorator :keyword:`class` dành riêng cho enumeration. Nó tìm kiếm :attr:`~EnumType.__members__` của một enumeration và thu thập mọi alias tìm thấy; nếu tìm thấy alias nào, :exc:`ValueError` sẽ được raise kèm theo thông tin chi tiết::

      >>> from enum import Enum, unique
      >>> @unique
      ... class Mistake(Enum):
      ...     ONE = 1
      ...     TWO = 2
      ...     THREE = 3
      ...     FOUR = 3
      ...
      Traceback (most recent call last):
      ...
      ValueError: duplicate values found in <enum 'Mistake'>: FOUR -> THREE

.. decorator:: verify

   Một decorator :keyword:`class` dành riêng cho enumeration. Các member từ
   :class:`EnumCheck` được dùng để chỉ định những ràng buộc nào cần được kiểm tra trên enumeration được decorator áp dụng.

   .. versionadded:: 3.11

.. decorator:: member

   Một decorator dùng trong enum: đối tượng đích của nó sẽ trở thành một member.

   .. versionadded:: 3.11

.. decorator:: nonmember

   Một decorator dùng trong enum: đối tượng đích của nó sẽ không trở thành một member.

   .. versionadded:: 3.11

.. decorator:: global_enum

   Một decorator dùng để thay đổi :class:`str() <str>` và :func:`repr` của một enum, nhằm hiển thị các member của enum là thuộc về module thay vì class của nó. Chỉ nên sử dụng khi các member của enum được export vào global namespace của module (xem :class:`re.RegexFlag` để biết ví dụ).


   .. versionadded:: 3.11

.. function:: show_flag_values(value)

   Trả về danh sách tất cả các số nguyên là lũy thừa của hai được chứa trong một flag *value*.

   .. versionadded:: 3.11

.. function:: bin(num, max_bits=None)

   Giống như :func:`bin` tích hợp sẵn, ngoại trừ việc các giá trị âm được biểu diễn bằng bù hai và bit đầu tiên luôn biểu thị dấu (``0`` là số dương, ``1`` là số âm).

      >>> import enum
      >>> enum.bin(10)
      '0b0 1010'
      >>> enum.bin(~10)   # ~10 là -11
      '0b1 0101'

   .. versionadded:: 3.11

---------------

.. _`Notes`:

Ghi chú
-------

:class:`IntEnum`, :class:`StrEnum` và :class:`IntFlag`

   Ba kiểu enum này được thiết kế để thay thế trực tiếp cho các giá trị hiện có dựa trên số nguyên và chuỗi; do đó, chúng có thêm một số hạn chế:

   - ``__str__`` sử dụng giá trị chứ không sử dụng tên của thành viên enum

   - ``__format__``, vì sử dụng ``__str__``, cũng sẽ sử dụng giá trị của thành viên enum thay vì tên của nó

   Nếu bạn không cần hoặc không muốn những hạn chế đó, bạn có thể tự tạo lớp cơ sở của riêng mình bằng cách tự mix-in kiểu ``int`` hoặc ``str``::

       >>> from enum import Enum
       >>> class MyIntEnum(int, Enum):
       ...     pass

   hoặc bạn có thể gán lại :meth:`str` tương ứng, v.v. trong enum của mình::

       >>> from enum import Enum, IntEnum
       >>> class MyIntEnum(IntEnum):
       ...     __str__ = Enum.__str__
