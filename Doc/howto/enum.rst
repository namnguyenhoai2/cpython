.. _enum-howto:

=================
HƯỚNG DẪN VỀ Enum
=================

.. _enum-basic-tutorial:

.. currentmodule:: enum

:class:`Enum` là một tập hợp các tên tượng trưng được liên kết với những giá trị duy nhất. Chúng tương tự như các biến toàn cục, nhưng cung cấp :func:`repr` hữu ích hơn, khả năng nhóm, type-safety và một số tính năng khác.

Chúng hữu ích nhất khi bạn có một biến chỉ có thể nhận một trong số giới hạn các giá trị được chọn. Ví dụ: các ngày trong tuần::

    >>> from enum import Enum
    >>> class Weekday(Enum):
    ...     MONDAY = 1
    ...     TUESDAY = 2
    ...     WEDNESDAY = 3
    ...     THURSDAY = 4
    ...     FRIDAY = 5
    ...     SATURDAY = 6
    ...     SUNDAY = 7

Hoặc có thể là các màu cơ bản RGB::

    >>> from enum import Enum
    >>> class Color(Enum):
    ...     RED = 1
    ...     GREEN = 2
    ...     BLUE = 3

Như bạn có thể thấy, việc tạo một :class:`Enum` đơn giản như viết một lớp kế thừa trực tiếp từ :class:`Enum`.

.. note:: Quy tắc viết hoa tên thành viên Enum

    Vì Enum được dùng để biểu diễn các hằng số và giúp tránh các vấn đề xung đột tên giữa các phương thức/thuộc tính của lớp mixin với tên enum, chúng tôi đặc biệt khuyến nghị sử dụng tên UPPER_CASE cho các thành viên và sẽ dùng kiểu này trong các ví dụ của mình.

Tùy thuộc vào bản chất của enum, giá trị của một member có thể quan trọng hoặc không, nhưng trong cả hai trường hợp, giá trị đó đều có thể được dùng để lấy member tương ứng::

    >>> Weekday(3)
    <Weekday.WEDNESDAY: 3>

Như bạn có thể thấy, ``repr()`` của một member hiển thị tên enum, tên member và giá trị. ``str()`` của một member chỉ hiển thị tên enum và tên member::

    >>> print(Weekday.THURSDAY)
    Weekday.THURSDAY

*type* của một member trong enumeration là enum mà member đó thuộc về::

    >>> type(Weekday.MONDAY)
    <enum 'Weekday'>
    >>> isinstance(Weekday.FRIDAY, Weekday)
    True

Các member của enum có một thuộc tính chỉ chứa :attr:`!name` của chúng::

    >>> print(Weekday.TUESDAY.name)
    TUESDAY

Tương tự, chúng có một thuộc tính dành cho :attr:`!value` của mình::


    >>> Weekday.WEDNESDAY.value
    3

Không giống nhiều ngôn ngữ chỉ xem enumeration là các cặp tên/giá trị, Python Enum có thể được bổ sung behavior. Ví dụ, :class:`datetime.date` có hai phương thức để trả về ngày trong tuần:
:meth:`~datetime.date.weekday` và :meth:`~datetime.date.isoweekday`. Điểm khác biệt là một phương thức đếm từ 0-6, còn phương thức kia đếm từ 1-7. Thay vì tự theo dõi điều đó, chúng ta có thể thêm một phương thức vào enum :class:`!Weekday` để trích xuất ngày từ instance :class:`~datetime.date` và trả về member enum tương ứng::

        @classmethod
        def from_date(cls, date):
            return cls(date.isoweekday())

Enum :class:`!Weekday` hoàn chỉnh hiện có dạng như sau::

    >>> class Weekday(Enum):
    ...     MONDAY = 1
    ...     TUESDAY = 2
    ...     WEDNESDAY = 3
    ...     THURSDAY = 4
    ...     FRIDAY = 5
    ...     SATURDAY = 6
    ...     SUNDAY = 7
    ...     #
    ...     @classmethod
    ...     def from_date(cls, date):
    ...         return cls(date.isoweekday())

Bây giờ chúng ta có thể biết hôm nay là ngày nào! Hãy xem::

    >>> import datetime as dt
    >>> Weekday.from_date(dt.date.today())     # doctest: +SKIP
    <Weekday.TUESDAY: 2>

Tất nhiên, nếu bạn đang đọc phần này vào một ngày khác, bạn sẽ thấy ngày đó thay vào đó.

Enum :class:`!Weekday` này rất hữu ích nếu biến của chúng ta chỉ cần một ngày, nhưng nếu cần nhiều ngày thì sao? Có thể chúng ta đang viết một hàm để lập lịch các việc nhà trong một tuần và không muốn sử dụng :class:`list` -- chúng ta có thể dùng một kiểu :class:`Enum` khác::

    >>> from enum import Flag
    >>> class Weekday(Flag):
    ...     MONDAY = 1
    ...     TUESDAY = 2
    ...     WEDNESDAY = 4
    ...     THURSDAY = 8
    ...     FRIDAY = 16
    ...     SATURDAY = 32
    ...     SUNDAY = 64

Chúng ta đã thay đổi hai điều: kế thừa từ :class:`Flag`, và các giá trị đều là lũy thừa của 2.

Giống như enum :class:`!Weekday` ban đầu ở trên, chúng ta có thể chọn một giá trị duy nhất::

    >>> first_week_day = Weekday.MONDAY
    >>> first_week_day
    <Weekday.MONDAY: 1>

Nhưng :class:`Flag` cũng cho phép chúng ta kết hợp nhiều thành viên vào một biến duy nhất::

    >>> weekend = Weekday.SATURDAY | Weekday.SUNDAY
    >>> weekend
    <Weekday.SATURDAY|SUNDAY: 96>

Bạn thậm chí có thể lặp qua một biến :class:`Flag`::

    >>> for day in weekend:
    ...     print(day)
    Weekday.SATURDAY
    Weekday.SUNDAY

Được rồi, hãy thiết lập một số việc cần làm::

    >>> chores_for_ethan = {
    ...     'feed the cat': Weekday.MONDAY | Weekday.WEDNESDAY | Weekday.FRIDAY,
    ...     'do the dishes': Weekday.TUESDAY | Weekday.THURSDAY,
    ...     'answer SO questions': Weekday.SATURDAY,
    ...     }

Và một hàm để hiển thị các việc cần làm cho một ngày cụ thể::

    >>> def show_chores(chores, day):
    ...     for chore, days in chores.items():
    ...         if day in days:
    ...             print(chore)
    ...
    >>> show_chores(chores_for_ethan, Weekday.SATURDAY)
    answer SO questions

Trong những trường hợp giá trị thực tế của các thành viên không quan trọng, bạn có thể giảm bớt công việc cho mình bằng cách sử dụng :func:`auto` làm các giá trị::

    >>> from enum import auto
    >>> class Weekday(Flag):
    ...     MONDAY = auto()
    ...     TUESDAY = auto()
    ...     WEDNESDAY = auto()
    ...     THURSDAY = auto()
    ...     FRIDAY = auto()
    ...     SATURDAY = auto()
    ...     SUNDAY = auto()
    ...     WEEKEND = SATURDAY | SUNDAY


.. _enum-advanced-tutorial:


Truy cập theo chương trình vào các thành viên của enumeration và thuộc tính của chúng
-------------------------------------------------------------------------------------

Đôi khi, việc truy cập các thành viên trong enumeration theo cách lập trình rất hữu ích (ví dụ: trong những tình huống mà ``Color.RED`` không đáp ứng được vì không biết chính xác màu nào tại thời điểm viết chương trình).  ``Enum`` cho phép truy cập như vậy::

    >>> Color(1)
    <Color.RED: 1>
    >>> Color(3)
    <Color.BLUE: 3>

Nếu bạn muốn truy cập các thành viên enum theo *name*, hãy sử dụng phép truy cập mục::

    >>> Color['RED']
    <Color.RED: 1>
    >>> Color['GREEN']
    <Color.GREEN: 2>

Nếu bạn có một thành viên enum và cần :attr:`!name` hoặc :attr:`!value`::

    >>> member = Color.RED
    >>> member.name
    'RED'
    >>> member.value
    1


Sao chép các thành viên và giá trị của enum
-------------------------------------------

Không thể có hai thành viên enum cùng tên::

    >>> class Shape(Enum):
    ...     SQUARE = 2
    ...     SQUARE = 3
    ...
    Traceback (most recent call last):
    ...
    TypeError: 'SQUARE' already defined as 2

Tuy nhiên, một thành viên enum có thể có các tên khác được liên kết với nó. Với hai mục nhập ``A`` và ``B`` có cùng giá trị (và ``A`` được định nghĩa trước), ``B`` là bí danh của thành viên ``A``. Tra cứu theo giá trị của ``A`` sẽ trả về thành viên ``A``. Tra cứu theo tên của ``A`` sẽ trả về thành viên ``A``. Tra cứu theo tên của ``B`` cũng sẽ trả về thành viên ``A``::

    >>> class Shape(Enum):
    ...     SQUARE = 2
    ...     DIAMOND = 1
    ...     CIRCLE = 3
    ...     ALIAS_FOR_SQUARE = 2
    ...
    >>> Shape.SQUARE
    <Shape.SQUARE: 2>
    >>> Shape.ALIAS_FOR_SQUARE
    <Shape.SQUARE: 2>
    >>> Shape(2)
    <Shape.SQUARE: 2>

.. note::

    Không được phép tạo một thành viên có cùng tên với một thuộc tính đã được định nghĩa (một thành viên khác, một phương thức, v.v.) hoặc tạo một thuộc tính có cùng tên với một thành viên.


Đảm bảo các giá trị enum là duy nhất
------------------------------------

Theo mặc định, enumeration cho phép nhiều tên làm bí danh cho cùng một giá trị. Khi không mong muốn hành vi này, bạn có thể sử dụng decorator :deco:`unique`::

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


Sử dụng các giá trị tự động
---------------------------

Nếu giá trị chính xác không quan trọng, bạn có thể sử dụng :class:`auto`::

    >>> from enum import Enum, auto
    >>> class Color(Enum):
    ...     RED = auto()
    ...     BLUE = auto()
    ...     GREEN = auto()
    ...
    >>> [member.value for member in Color]
    [1, 2, 3]

Các giá trị được chọn bởi :func:`~Enum._generate_next_value_`, và có thể được ghi đè::

    >>> class AutoName(Enum):
    ...     @staticmethod
    ...     def _generate_next_value_(name, start, count, last_values):
    ...         return name
    ...
    >>> class Ordinal(AutoName):
    ...     NORTH = auto()
    ...     SOUTH = auto()
    ...     EAST = auto()
    ...     WEST = auto()
    ...
    >>> [member.value for member in Ordinal]
    ['NORTH', 'SOUTH', 'EAST', 'WEST']

.. note::

    Phương thức :meth:`~Enum._generate_next_value_` phải được định nghĩa trước mọi member.

Lặp qua
-------

Việc lặp qua các member của một enum không cung cấp các bí danh::

    >>> list(Shape)
    [<Shape.SQUARE: 2>, <Shape.DIAMOND: 1>, <Shape.CIRCLE: 3>]
    >>> list(Weekday)
    [<Weekday.MONDAY: 1>, <Weekday.TUESDAY: 2>, <Weekday.WEDNESDAY: 4>, <Weekday.THURSDAY: 8>, <Weekday.FRIDAY: 16>, <Weekday.SATURDAY: 32>, <Weekday.SUNDAY: 64>]

Lưu ý rằng các bí danh ``Shape.ALIAS_FOR_SQUARE`` và ``Weekday.WEEKEND`` không được hiển thị.

Thuộc tính đặc biệt ``__members__`` là một ánh xạ có thứ tự chỉ đọc từ tên đến thành viên. Nó bao gồm tất cả các tên được định nghĩa trong enumeration, bao gồm cả các bí danh::

    >>> for name, member in Shape.__members__.items():
    ...     name, member
    ...
    ('SQUARE', <Shape.SQUARE: 2>)
    ('DIAMOND', <Shape.DIAMOND: 1>)
    ('CIRCLE', <Shape.CIRCLE: 3>)
    ('ALIAS_FOR_SQUARE', <Shape.SQUARE: 2>)

Có thể sử dụng thuộc tính ``__members__`` để truy cập lập trình chi tiết vào các thành viên của enumeration. Ví dụ: tìm tất cả các bí danh::

    >>> [name for name, member in Shape.__members__.items() if member.name != name]
    ['ALIAS_FOR_SQUARE']

.. note::

   Các bí danh cho flags bao gồm những giá trị có nhiều flag được thiết lập, chẳng hạn như ``3``, và không có flag nào được thiết lập, tức là ``0``.


So sánh
-------

Các thành viên của enumeration được so sánh bằng identity::

    >>> Color.RED is Color.RED
    True
    >>> Color.RED is Color.BLUE
    False
    >>> Color.RED is not Color.BLUE
    True

So sánh có thứ tự giữa các giá trị enumeration *không* được hỗ trợ. Các thành viên Enum không phải là số nguyên (nhưng xem `IntEnum`_ bên dưới)::

    >>> Color.RED < Color.BLUE
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: '<' not supported between instances of 'Color' and 'Color'

Các phép so sánh bằng được định nghĩa, dù vậy::

    >>> Color.BLUE == Color.RED
    False
    >>> Color.BLUE != Color.RED
    True
    >>> Color.BLUE == Color.BLUE
    True

Các phép so sánh với những giá trị không thuộc enumeration sẽ luôn cho kết quả không bằng nhau (một lần nữa, :class:`IntEnum` được thiết kế rõ ràng để hoạt động khác đi, xem bên dưới)::

    >>> Color.BLUE == 2
    False

.. warning::

   Có thể tải lại các module -- nếu một module được tải lại chứa các enumeration, chúng sẽ được tạo lại, và các member mới có thể không identical/equal với các member ban đầu.

Các member và attribute được phép của enumeration
-------------------------------------------------

Hầu hết các ví dụ trên đều sử dụng số nguyên làm giá trị enumeration. Việc sử dụng số nguyên ngắn gọn và tiện lợi (và được cung cấp theo mặc định bởi `Functional API <Functional API_>`_), nhưng không bắt buộc. Trong phần lớn các trường hợp sử dụng, người ta không quan tâm giá trị thực tế của một enumeration là gì. Tuy nhiên, nếu giá trị *là* quan trọng, enumeration có thể có các giá trị tùy ý.

Enumeration là các lớp Python và có thể có các method cũng như special method như thường lệ. Nếu chúng ta có enumeration này::

    >>> class Mood(Enum):
    ...     FUNKY = 1
    ...     HAPPY = 3
    ...
    ...     def describe(self):
    ...         # self là member ở đây
    ...         return self.name, self.value
    ...
    ...     def __str__(self):
    ...         return 'my custom str! {0}'.format(self.value)
    ...
    ...     @classmethod
    ...     def favorite_mood(cls):
    ...         # cls ở đây là enumeration
    ...         return cls.HAPPY
    ...

Tiếp theo::

    >>> Mood.favorite_mood()
    <Mood.HAPPY: 3>
    >>> Mood.HAPPY.describe()
    ('HAPPY', 3)
    >>> str(Mood.FUNKY)
    'my custom str! 1'

Các quy tắc về những gì được phép như sau: tên bắt đầu và kết thúc bằng một dấu gạch dưới được enum dành riêng và không thể sử dụng; mọi thuộc tính khác được định nghĩa bên trong một enumeration sẽ trở thành thành viên của enumeration này, ngoại trừ các special method (:meth:`~object.__str__`,
:meth:`~object.__add__`, v.v.), descriptor (method cũng là descriptor) và các tên biến được liệt kê trong :attr:`~Enum._ignore_`.

Lưu ý: nếu enumeration của bạn định nghĩa :meth:`~object.__new__` và/hoặc :meth:`~object.__init__`, mọi giá trị được gán cho thành viên enum sẽ được truyền vào các method đó. Xem `Planet`_ để biết ví dụ.

.. note::

    Method :meth:`~object.__new__`, nếu được định nghĩa, được sử dụng trong quá trình tạo các thành viên Enum; sau đó nó được thay thế bằng :meth:`~object.__new__` của Enum, method được sử dụng sau khi tạo class để tra cứu các thành viên hiện có. Xem :ref:`new-vs-init` để biết thêm chi tiết.


Kế thừa lớp con Enum bị hạn chế
-------------------------------

Một lớp :class:`Enum` mới phải có một lớp enum cơ sở, nhiều nhất một kiểu dữ liệu cụ thể và số lượng tùy ý các lớp mixin dựa trên :class:`object`. Thứ tự của các lớp cơ sở này là::

    class EnumName([mix-in, ...,] [data-type,] base-enum):
        pass

Ngoài ra, chỉ được phép phân lớp một enumeration nếu enumeration đó không định nghĩa thành viên nào. Vì vậy, cách này bị cấm::

    >>> class MoreColor(Color):
    ...     PINK = 17
    ...
    Traceback (most recent call last):
    ...
    TypeError: <enum 'MoreColor'> cannot extend <enum 'Color'>

Nhưng cách này được phép::

    >>> class Foo(Enum):
    ...     def some_behavior(self):
    ...         pass
    ...
    >>> class Bar(Foo):
    ...     HAPPY = 1
    ...     SAD = 2
    ...

Cho phép phân lớp các enum có định nghĩa thành viên sẽ dẫn đến việc vi phạm một số bất biến quan trọng của kiểu và thực thể. Mặt khác, việc cho phép chia sẻ một số hành vi chung giữa một nhóm enumeration là hợp lý. (Xem `OrderedEnum`_ để biết ví dụ.)


.. _enum-dataclass-support:

Hỗ trợ Dataclass
----------------

Khi kế thừa từ một :class:`~dataclasses.dataclass`, :meth:`~Enum.__repr__` sẽ bỏ qua tên của lớp được kế thừa. Ví dụ::

    >>> from dataclasses import dataclass, field
    >>> @dataclass
    ... class CreatureDataMixin:
    ...     size: str
    ...     legs: int
    ...     tail: bool = field(repr=False, default=True)
    ...
    >>> class Creature(CreatureDataMixin, Enum):
    ...     BEETLE = 'small', 6
    ...     DOG = 'medium', 4
    ...
    >>> Creature.DOG
    <Creature.DOG: size='medium', legs=4>

Sử dụng đối số :func:`~dataclasses.dataclass` ``repr=False`` để sử dụng :func:`repr` tiêu chuẩn.

.. versionchanged:: 3.12
   Chỉ các trường của dataclass được hiển thị trong vùng giá trị, không hiển thị tên của dataclass.

.. note::

   Không hỗ trợ thêm decorator :deco:`~dataclasses.dataclass` vào :class:`Enum` và các lớp con của nó. Việc này sẽ không gây ra lỗi nào, nhưng sẽ tạo ra những kết quả rất kỳ lạ khi runtime, chẳng hạn như các thành viên bằng nhau::

      >>> @dataclass               # đừng làm vậy: việc này hoàn toàn vô nghĩa
      ... class Color(Enum):
      ...    RED = 1
      ...    BLUE = 2
      ...
      >>> Color.RED is Color.BLUE
      False
      >>> Color.RED == Color.BLUE  # vấn đề nằm ở đây: chúng không được bằng nhau
      True


Pickling
--------

Các enumeration có thể được pickling và unpickling::

    >>> from test.test_enum import Fruit
    >>> from pickle import dumps, loads
    >>> Fruit.TOMATO is loads(dumps(Fruit.TOMATO))
    True

Các hạn chế thông thường đối với pickling vẫn được áp dụng: các enumeration có thể pickling phải được định nghĩa ở cấp cao nhất của một module, vì unpickling yêu cầu chúng có thể được import từ module đó.

.. note::

    Với pickle protocol phiên bản 4, bạn có thể dễ dàng pickle các enum được lồng trong những class khác.

Bạn có thể thay đổi cách các thành viên enum được pickle/unpickle bằng cách định nghĩa
:meth:`~object.__reduce_ex__` trong class enumeration. Phương thức mặc định là theo giá trị, nhưng các enum có giá trị phức tạp có thể muốn sử dụng theo tên::

    >>> import enum
    >>> class MyEnum(enum.Enum):
    ...     __reduce_ex__ = enum.pickle_by_enum_name

.. note::

    Không nên sử dụng cách theo tên cho các cờ, vì các alias không có tên sẽ không thể unpickle.


.. _`Functional API`:

API dạng hàm
------------

class :class:`Enum` có thể gọi được, cung cấp API dạng hàm sau đây::

    >>> Animal = Enum('Animal', 'ANT BEE CAT DOG')
    >>> Animal
    <enum 'Animal'>
    >>> Animal.ANT
    <Animal.ANT: 1>
    >>> list(Animal)
    [<Animal.ANT: 1>, <Animal.BEE: 2>, <Animal.CAT: 3>, <Animal.DOG: 4>]

Ngữ nghĩa của API này tương tự như :class:`~collections.namedtuple`. Đối số đầu tiên của lời gọi :class:`Enum` là tên của enumeration.

Đối số thứ hai là *source* của tên các thành viên enumeration. Đối số này có thể là một chuỗi tên được phân tách bằng khoảng trắng, một chuỗi các tên, một chuỗi gồm các bộ 2 phần tử chứa các cặp khóa/giá trị hoặc một mapping (ví dụ: dictionary) ánh xạ tên với giá trị. Hai tùy chọn cuối cho phép gán các giá trị tùy ý cho enumeration; các tùy chọn còn lại sẽ tự động gán các số nguyên tăng dần, bắt đầu từ 1 (sử dụng tham số ``start`` để chỉ định giá trị bắt đầu khác). Một class mới kế thừa từ :class:`Enum` sẽ được trả về. Nói cách khác, phép gán :class:`!Animal` ở trên tương đương với::

    >>> class Animal(Enum):
    ...     ANT = 1
    ...     BEE = 2
    ...     CAT = 3
    ...     DOG = 4
    ...

Lý do mặc định chọn ``1`` làm số bắt đầu thay vì ``0`` là vì ``0`` là ``False`` về mặt boolean, nhưng theo mặc định, tất cả thành viên enum đều được đánh giá là ``True``.

Việc pickle các enum được tạo bằng functional API có thể phức tạp vì các chi tiết triển khai của ngăn xếp frame được sử dụng để cố gắng xác định enumeration đang được tạo trong module nào (ví dụ: thao tác này sẽ thất bại nếu bạn sử dụng một hàm tiện ích trong một module riêng biệt, đồng thời cũng có thể không hoạt động trên IronPython hoặc Jython). Giải pháp là chỉ định rõ ràng tên module như sau::

    >>> Animal = Enum('Animal', 'ANT BEE CAT DOG', module=__name__)

.. warning::

    Nếu ``module`` không được cung cấp và Enum không thể xác định giá trị này, các thành viên Enum mới sẽ không thể unpickle; để giữ cho lỗi gần với nguồn hơn, thao tác pickle sẽ bị vô hiệu hóa.

Giao thức pickle 4 mới cũng trong một số trường hợp dựa vào
việc :attr:`~type.__qualname__` được đặt thành vị trí mà pickle có thể tìm thấy class. Ví dụ: nếu class được cung cấp trong class SomeData ở phạm vi global::

    >>> Animal = Enum('Animal', 'ANT BEE CAT DOG', qualname='SomeData.Animal')

Chữ ký đầy đủ là::

    Enum(
        value='NewEnumName',
        names=<...>,
        *,
        module='...',
        qualname='...',
        type=<mixed-in class>,
        start=1,
        )

* *value*: Tên mà lớp enum mới sẽ ghi nhận.

* *names*: Các thành viên enum. Đây có thể là một chuỗi được phân tách bằng khoảng trắng hoặc dấu phẩy (các giá trị sẽ bắt đầu từ 1 nếu không được chỉ định khác)::

    'RED GREEN BLUE' | 'RED,GREEN,BLUE' | 'RED, GREEN, BLUE'

  hoặc một iterator chứa các tên::

    ['RED', 'GREEN', 'BLUE']

  hoặc một iterator chứa các cặp (name, value)::

    [('CYAN', 4), ('MAGENTA', 5), ('YELLOW', 6)]

  hoặc một mapping::

    {'CHARTREUSE': 7, 'SEA_GREEN': 11, 'ROSEMARY': 42}

* *module*: tên của module nơi có thể tìm thấy lớp enum mới.

* *qualname*: vị trí trong module nơi có thể tìm thấy lớp enum mới.

* *type*: kiểu để trộn vào lớp enum mới.

* *start*: số bắt đầu đếm nếu chỉ truyền tên.

.. versionchanged:: 3.5
   Tham số *start* đã được thêm vào.


Các Enumeration phái sinh
-------------------------

.. _`IntEnum`:

IntEnum
^^^^^^^

Biến thể đầu tiên của :class:`Enum` được cung cấp cũng là một lớp con của
:class:`int`. Các thành viên của một :class:`IntEnum` có thể được so sánh với các số nguyên; do đó, các enumeration số nguyên thuộc các kiểu khác nhau cũng có thể được so sánh với nhau::

    >>> from enum import IntEnum
    >>> class Shape(IntEnum):
    ...     CIRCLE = 1
    ...     SQUARE = 2
    ...
    >>> class Request(IntEnum):
    ...     POST = 1
    ...     GET = 2
    ...
    >>> Shape == 1
    False
    >>> Shape.CIRCLE == 1
    True
    >>> Shape.CIRCLE == Request.POST
    True

Tuy nhiên, chúng vẫn không thể được so sánh với các enumeration :class:`Enum` tiêu chuẩn::

    >>> class Shape(IntEnum):
    ...     CIRCLE = 1
    ...     SQUARE = 2
    ...
    >>> class Color(Enum):
    ...     RED = 1
    ...     GREEN = 2
    ...
    >>> Shape.CIRCLE == Color.RED
    False

Các giá trị :class:`IntEnum` hoạt động như số nguyên theo những cách khác mà bạn mong đợi::

    >>> int(Shape.CIRCLE)
    1
    >>> ['a', 'b', 'c'][Shape.CIRCLE]
    'b'
    >>> [i for i in range(Shape.SQUARE)]
    [0, 1]


StrEnum
^^^^^^^

Biến thể thứ hai của :class:`Enum` được cung cấp cũng là một lớp con của
:class:`str`. Các thành viên của :class:`StrEnum` có thể được so sánh với các chuỗi; do đó, các enumeration chuỗi thuộc những kiểu khác nhau cũng có thể được so sánh với nhau.

.. versionadded:: 3.11


IntFlag
^^^^^^^

Biến thể tiếp theo của :class:`Enum` được cung cấp, :class:`IntFlag`, cũng dựa trên :class:`int`. Điểm khác biệt là các thành viên :class:`IntFlag` có thể được kết hợp bằng các toán tử bit (&, \|, ^, ~) và kết quả vẫn là một
thành viên :class:`IntFlag`, nếu có thể. Giống như :class:`IntEnum`, các thành viên :class:`IntFlag` cũng là số nguyên và có thể được sử dụng ở bất cứ nơi nào :class:`int` được sử dụng.

.. note::

    Mọi thao tác trên một thành viên :class:`IntFlag` ngoài các thao tác bitwise sẽ làm mất tư cách thành viên :class:`IntFlag`.

    Các thao tác bitwise cho ra các giá trị :class:`IntFlag` không hợp lệ sẽ làm mất
    tư cách thành viên :class:`IntFlag`. Xem :class:`FlagBoundary` để biết chi tiết.

.. versionadded:: 3.6
.. versionchanged:: 3.11

Lớp :class:`IntFlag` mẫu::

    >>> from enum import IntFlag
    >>> class Perm(IntFlag):
    ...     R = 4
    ...     W = 2
    ...     X = 1
    ...
    >>> Perm.R | Perm.W
    <Perm.R|W: 6>
    >>> Perm.R + Perm.W
    6
    >>> RW = Perm.R | Perm.W
    >>> Perm.R in RW
    True

Cũng có thể đặt tên cho các tổ hợp::

    >>> class Perm(IntFlag):
    ...     R = 4
    ...     W = 2
    ...     X = 1
    ...     RWX = 7
    ...
    >>> Perm.RWX
    <Perm.RWX: 7>
    >>> ~Perm.RWX
    <Perm: 0>
    >>> Perm(7)
    <Perm.RWX: 7>

.. note::

    Các tổ hợp có tên được xem là alias. Alias không xuất hiện trong quá trình lặp, nhưng có thể được trả về khi tra cứu theo giá trị.

.. versionchanged:: 3.11

Một khác biệt quan trọng khác giữa :class:`IntFlag` và :class:`Enum` là nếu không có cờ nào được thiết lập (giá trị là 0), phép đánh giá boolean của nó là :data:`False`::

    >>> Perm.R & Perm.X
    <Perm: 0>
    >>> bool(Perm.R & Perm.X)
    False

Vì các thành viên :class:`IntFlag` cũng là các lớp con của :class:`int`, chúng có thể được kết hợp với các thành viên đó (nhưng có thể mất tư cách thành viên :class:`IntFlag`::

    >>> Perm.X | 4
    <Perm.R|X: 5>

    >>> Perm.X + 8
    9

.. note::

    Toán tử phủ định, ``~``, luôn trả về một thành viên :class:`IntFlag` với giá trị dương::

        >>> (~Perm.X).value == (Perm.R|Perm.W).value == 6
        True

Các thành viên :class:`IntFlag` cũng có thể được lặp qua::

    >>> list(RW)
    [<Perm.R: 4>, <Perm.W: 2>]

.. versionadded:: 3.11


Flag
^^^^

Biến thể cuối cùng là :class:`Flag`.  Giống như :class:`IntFlag`, các thành viên :class:`Flag` có thể được kết hợp bằng các toán tử bit (&, \|, ^, ~).  Không giống như
:class:`IntFlag`, chúng không thể được kết hợp với hoặc so sánh với bất kỳ enumeration :class:`Flag` nào khác, cũng như :class:`int`.  Mặc dù có thể chỉ định trực tiếp các giá trị, bạn nên sử dụng :class:`auto` làm giá trị và để :class:`Flag` chọn một giá trị phù hợp.

.. versionadded:: 3.6

Giống như :class:`IntFlag`, nếu sự kết hợp của các thành viên :class:`Flag` không đặt bất kỳ cờ nào, phép đánh giá boolean sẽ là :data:`False`::

    >>> from enum import Flag, auto
    >>> class Color(Flag):
    ...     RED = auto()
    ...     BLUE = auto()
    ...     GREEN = auto()
    ...
    >>> Color.RED & Color.GREEN
    <Color: 0>
    >>> bool(Color.RED & Color.GREEN)
    False

Các cờ riêng lẻ nên có các giá trị là lũy thừa của hai (1, 2, 4, 8, ...), trong khi các tổ hợp cờ thì không::

    >>> class Color(Flag):
    ...     RED = auto()
    ...     BLUE = auto()
    ...     GREEN = auto()
    ...     WHITE = RED | BLUE | GREEN
    ...
    >>> Color.WHITE
    <Color.WHITE: 7>

Việc đặt tên cho điều kiện "không có cờ nào được đặt" không làm thay đổi giá trị boolean của điều kiện đó::

    >>> class Color(Flag):
    ...     BLACK = 0
    ...     RED = auto()
    ...     BLUE = auto()
    ...     GREEN = auto()
    ...
    >>> Color.BLACK
    <Color.BLACK: 0>
    >>> bool(Color.BLACK)
    False

Các thành viên :class:`Flag` cũng có thể được lặp qua::

    >>> purple = Color.RED | Color.BLUE
    >>> list(purple)
    [<Color.RED: 1>, <Color.BLUE: 2>]

.. versionadded:: 3.11

.. note::

    Đối với phần lớn mã mới, :class:`Enum` và :class:`Flag` được khuyến nghị mạnh mẽ, vì :class:`IntEnum` và :class:`IntFlag` phá vỡ một số cam kết ngữ nghĩa của một enumeration (do có thể so sánh với số nguyên, và do tính bắc cầu, với các enumeration không liên quan khác). :class:`IntEnum` và :class:`IntFlag` chỉ nên được sử dụng trong những trường hợp :class:`Enum` và
    :class:`Flag` không đáp ứng được; chẳng hạn như khi thay thế các hằng số số nguyên bằng enumeration hoặc để tương tác với các hệ thống khác.


Các nội dung khác
^^^^^^^^^^^^^^^^^

Mặc dù :class:`IntEnum` là một phần của mô-đun :mod:`enum`, việc triển khai độc lập sẽ rất đơn giản::

    class IntEnum(int, ReprEnum):   # hoặc Enum thay vì ReprEnum
        pass

Điều này minh họa cách định nghĩa các enumeration dẫn xuất tương tự; ví dụ: một :class:`!FloatEnum` kết hợp :class:`float` thay vì :class:`int`.

Một số quy tắc:

1. Khi tạo lớp con của :class:`Enum`, các kiểu mix-in phải xuất hiện trước
   chính lớp :class:`Enum` trong chuỗi các lớp cơ sở, như trong ví dụ :class:`IntEnum` ở trên.
2. Các kiểu mix-in phải có thể được tạo lớp con. Ví dụ: :class:`bool` và
   :class:`range` không thể được phân lớp và sẽ gây ra lỗi trong quá trình tạo Enum nếu được sử dụng làm kiểu mix-in.
3. Mặc dù :class:`Enum` có thể có các thành viên thuộc bất kỳ kiểu nào, nhưng khi bạn mix-in thêm một kiểu, tất cả các thành viên phải có giá trị thuộc kiểu đó, ví dụ:
   :class:`int` ở trên. Hạn chế này không áp dụng cho các mix-in chỉ thêm phương thức và không chỉ định một kiểu khác.
4. Khi một kiểu dữ liệu khác được mix-in, thuộc tính :attr:`~Enum.value` *không giống* chính thành viên enum, mặc dù chúng tương đương và sẽ được so sánh là bằng nhau.
5. Một ``data type`` là một mixin định nghĩa :meth:`~object.__new__`, hoặc một
   :class:`~dataclasses.dataclass`
6. Định dạng kiểu %:  ``%s`` và ``%r`` gọi lớp :class:`Enum`
   :meth:`~object.__str__` và :meth:`~object.__repr__` lần lượt; các mã khác (chẳng hạn như ``%i`` hoặc ``%h`` đối với IntEnum) xử lý thành viên enum theo kiểu được mix-in.
7. :ref:`Các formatted string literal <f-strings>`, :meth:`str.format` và :func:`format` sẽ sử dụng phương thức :meth:`~object.__str__` của enum.

.. note::

   Vì :class:`IntEnum`, :class:`IntFlag` và :class:`StrEnum` được thiết kế để thay thế trực tiếp cho các hằng số hiện có, :class:`IntEnum` của chúng
   phương thức đã được đặt lại thành :meth:`~object.__str__` của các kiểu dữ liệu tương ứng
   phương thức :meth:`~object.__str__`.

.. _new-vs-init:

Khi nào nên dùng :meth:`~object.__new__` so với :meth:`~object.__init__`
------------------------------------------------------------------------

:meth:`~object.__new__` phải được sử dụng bất cứ khi nào bạn muốn tùy chỉnh giá trị thực tế mà thành viên :class:`Enum` đại diện. Mọi sửa đổi khác có thể nằm ở cả hai
:meth:`~object.__new__` hoặc :meth:`~object.__init__`, trong đó ưu tiên :meth:`~object.__init__`.

Ví dụ, nếu bạn muốn truyền nhiều mục vào constructor nhưng chỉ muốn một trong số đó là giá trị::

    >>> class Coordinate(bytes, Enum):
    ...     """
    ...     Coordinate with binary codes that can be indexed by the int code.
    ...     """
    ...     def __new__(cls, value, label, unit):
    ...         obj = bytes.__new__(cls, [value])
    ...         obj._value_ = value
    ...         obj.label = label
    ...         obj.unit = unit
    ...         return obj
    ...     PX = (0, 'P.X', 'km')
    ...     PY = (1, 'P.Y', 'km')
    ...     VX = (2, 'V.X', 'km/s')
    ...     VY = (3, 'V.Y', 'km/s')
    ...

    >>> print(Coordinate['PY'])
    Coordinate.PY

    >>> print(Coordinate(3))
    Coordinate.VY

.. warning::

    *Đừng* gọi ``super().__new__()``, vì ``__new__`` chỉ dùng để tra cứu là thứ được tìm thấy; thay vào đó, hãy sử dụng trực tiếp kiểu dữ liệu.


Các điểm cần lưu ý
------------------

Các tên ``__dunder__`` và ``_sunder_`` được hỗ trợ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Các tên ``__dunder__`` và ``_sunder_`` được hỗ trợ có thể được tìm thấy trong tài liệu :ref:`API Enum <enum-dunder-sunder>`.


_Private__names
^^^^^^^^^^^^^^^

:ref:`Các tên riêng <private-name-mangling>` không được chuyển đổi thành các thành viên enum mà vẫn giữ nguyên là các thuộc tính thông thường.

.. versionchanged:: 3.11


``Enum`` kiểu thành viên
^^^^^^^^^^^^^^^^^^^^^^^^

Các thành viên Enum là các thực thể của lớp enum tương ứng và thường được truy cập dưới dạng ``EnumClass.member``. Trong một số tình huống, chẳng hạn như khi viết hành vi enum tùy chỉnh, việc có thể truy cập trực tiếp một thành viên từ một thành viên khác rất hữu ích và được hỗ trợ; tuy nhiên, để tránh xung đột tên giữa tên thành viên và các thuộc tính/phương thức từ những lớp được trộn vào, bạn nên sử dụng mạnh các tên viết hoa.

.. versionchanged:: 3.5


Tạo các thành viên được trộn với những kiểu dữ liệu khác
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Khi kế thừa các kiểu dữ liệu khác, chẳng hạn như :class:`int` hoặc :class:`str`, bằng một :class:`Enum`, tất cả các giá trị sau ``=`` sẽ được truyền cho hàm khởi tạo của kiểu dữ liệu đó. Ví dụ:::

    >>> class MyEnum(IntEnum):      # help(int) -> int(x, base=10) -> integer
    ...     example = '11', 16      # vì vậy x='11' và base=16
    ...
    >>> MyEnum.example.value        # và hex(11) là...
    17


Giá trị Boolean của các lớp và thành viên ``Enum``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Các lớp Enum được trộn với các kiểu không phải :class:`Enum` (chẳng hạn như
:class:`int`, :class:`str`, v.v.) được đánh giá theo quy tắc của kiểu được trộn vào; nếu không, tất cả các thành viên đều được đánh giá là :data:`True`.  Để việc đánh giá Boolean của enum riêng phụ thuộc vào giá trị của thành viên, hãy thêm đoạn sau vào lớp của bạn::

    def __bool__(self):
        return bool(self.value)

Các lớp :class:`Enum` thuần túy luôn được đánh giá là :data:`True`.


Các lớp ``Enum`` có phương thức
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Nếu cung cấp cho lớp con enum của mình các phương thức bổ sung, như lớp `Planet`_ bên dưới, những phương thức đó sẽ xuất hiện trong :func:`dir` của thành viên, nhưng không xuất hiện trong :func:`dir` của lớp::

    >>> dir(Planet)                         # doctest: +SKIP
    ['EARTH', 'JUPITER', 'MARS', 'MERCURY', 'NEPTUNE', 'SATURN', 'URANUS', 'VENUS', '__class__', '__doc__', '__members__', '__module__']
    >>> dir(Planet.EARTH)                   # doctest: +SKIP
    ['__class__', '__doc__', '__module__', 'mass', 'name', 'radius', 'surface_gravity', 'value']


Kết hợp các thành viên của ``Flag``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Việc lặp qua một tổ hợp các thành viên :class:`Flag` sẽ chỉ trả về những thành viên được cấu thành từ một bit đơn::

    >>> class Color(Flag):
    ...     RED = auto()
    ...     GREEN = auto()
    ...     BLUE = auto()
    ...     MAGENTA = RED | BLUE
    ...     YELLOW = RED | GREEN
    ...     CYAN = GREEN | BLUE
    ...
    >>> Color(3)  # tổ hợp có tên
    <Color.YELLOW: 3>
    >>> Color(7)      # tổ hợp không có tên
    <Color.RED|GREEN|BLUE: 7>


Một số chi tiết về ``Flag`` và ``IntFlag``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sử dụng đoạn mã sau cho các ví dụ của chúng ta::

    >>> class Color(IntFlag):
    ...     BLACK = 0
    ...     RED = 1
    ...     GREEN = 2
    ...     BLUE = 4
    ...     PURPLE = RED | BLUE
    ...     WHITE = RED | GREEN | BLUE
    ...

những điều sau là đúng:

- các flag một bit là các flag chuẩn tắc
- các flag nhiều bit và không bit là các bí danh
- chỉ các flag chuẩn tắc được trả về trong quá trình lặp::

    >>> list(Color.WHITE)
    [<Color.RED: 1>, <Color.GREEN: 2>, <Color.BLUE: 4>]

- việc lấy phủ định của một flag hoặc tập flag sẽ trả về một flag hoặc tập flag mới với giá trị số nguyên dương tương ứng::

    >>> Color.BLUE
    <Color.BLUE: 4>

    >>> ~Color.BLUE
    <Color.RED|GREEN: 3>

- tên của các pseudo-flag được tạo từ tên của các thành viên của chúng::

    >>> (Color.RED | Color.GREEN).name
    'RED|GREEN'

    >>> class Perm(IntFlag):
    ...     R = 4
    ...     W = 2
    ...     X = 1
    ...
    >>> (Perm.R & Perm.W).name is None  # về cơ bản là Perm(0)
    True

- các cờ nhiều bit, hay còn gọi là alias, có thể được trả về từ các phép toán::

    >>> Color.RED | Color.BLUE
    <Color.PURPLE: 5>

    >>> Color(7)  # hoặc Color(-1)
    <Color.WHITE: 7>

    >>> Color(0)
    <Color.BLACK: 0>

- kiểm tra membership / containment: các cờ có giá trị bằng không luôn được xem là nằm trong::

    >>> Color.BLACK in Color.WHITE
    True

  nếu không, chỉ khi tất cả các bit của một cờ đều nằm trong cờ kia thì mới trả về True::

    >>> Color.PURPLE in Color.WHITE
    True

    >>> Color.GREEN in Color.PURPLE
    False

Có một cơ chế boundary mới kiểm soát cách xử lý các bit vượt ngoài phạm vi / không hợp lệ: ``STRICT``, ``CONFORM``, ``EJECT`` và ``KEEP``:

* STRICT --> tạo exception khi nhận các giá trị không hợp lệ
* CONFORM --> loại bỏ mọi bit không hợp lệ
* EJECT --> mất trạng thái Flag và trở thành một int thông thường với giá trị đã cho
* KEEP --> giữ lại các bit bổ sung

  - giữ trạng thái Flag và các bit bổ sung
  - các bit bổ sung không xuất hiện khi lặp
  - các bit bổ sung xuất hiện trong repr() và str()

Giá trị mặc định của Flag là ``STRICT``, giá trị mặc định của ``IntFlag`` là ``EJECT``, và giá trị mặc định của ``_convert_`` là ``KEEP`` (xem ``ssl.Options`` để biết ví dụ về trường hợp cần ``KEEP``).


.. _enum-class-differences:

Enums và Flags khác nhau như thế nào?
-------------------------------------

Enum có một metaclass tùy chỉnh, ảnh hưởng đến nhiều khía cạnh của cả các lớp :class:`Enum` dẫn xuất và các thể hiện (member) của chúng.


Các lớp Enum
^^^^^^^^^^^^

Metaclass :class:`EnumType` chịu trách nhiệm cung cấp
:meth:`~object.__contains__`, :meth:`~object.__dir__`, :meth:`~object.__iter__` và các phương thức khác cho phép thực hiện những thao tác trên một lớp :class:`Enum` mà sẽ thất bại trên một lớp thông thường, chẳng hạn như ``list(Color)`` hoặc ``some_enum_var in Color``.  :class:`EnumType` chịu trách nhiệm đảm bảo rằng nhiều phương thức khác trên lớp :class:`Enum` cuối cùng là chính xác (chẳng hạn như :meth:`~object.__new__`, :meth:`~object.__getnewargs__`,
:meth:`~object.__str__` và :meth:`~object.__repr__`).

Các lớp Flag
^^^^^^^^^^^^

Flag có cách nhìn mở rộng về việc đặt bí danh: để là canonical, giá trị của một flag phải là một giá trị lũy thừa của hai và không được trùng tên.  Vì vậy, ngoài
:class:`Enum` định nghĩa alias, một flag không có giá trị (còn gọi là ``0``) hoặc có nhiều hơn một giá trị lũy thừa của hai (ví dụ: ``3``) được xem là một alias.

Các thành viên Enum (hay còn gọi là các instance)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Điều thú vị nhất về các thành viên Enum là chúng là các singleton.
:class:`EnumType` tạo tất cả chúng trong quá trình tạo chính lớp Enum, sau đó đặt một :meth:`~object.__new__` tùy chỉnh để đảm bảo không có instance mới nào được khởi tạo, bằng cách chỉ trả về các instance thành viên hiện có.

Các thành viên Flag
^^^^^^^^^^^^^^^^^^^

Có thể lặp qua các thành viên Flag giống như lớp :class:`Flag`, và chỉ các thành viên canonical mới được trả về. Ví dụ:::

    >>> list(Color)
    [<Color.RED: 1>, <Color.GREEN: 2>, <Color.BLUE: 4>]

(Lưu ý rằng ``BLACK``, ``PURPLE`` và ``WHITE`` không xuất hiện.)

Đảo một thành viên cờ sẽ trả về giá trị dương tương ứng, thay vì giá trị âm --- ví dụ::

    >>> ~Color.RED
    <Color.GREEN|BLUE: 6>

Các thành viên cờ có độ dài tương ứng với số lượng giá trị lũy thừa của hai mà chúng chứa. Ví dụ::

    >>> len(Color.PURPLE)
    2


.. _enum-cookbook:

Cẩm nang Enum
-------------


Mặc dù :class:`Enum`, :class:`IntEnum`, :class:`StrEnum`, :class:`Flag` và
:class:`IntFlag` được kỳ vọng sẽ đáp ứng phần lớn các trường hợp sử dụng, chúng không thể đáp ứng tất cả. Sau đây là các công thức cho một số kiểu enumeration khác nhau, có thể sử dụng trực tiếp hoặc làm ví dụ để tạo enumeration của riêng bạn.


Bỏ qua giá trị
^^^^^^^^^^^^^^

Trong nhiều trường hợp sử dụng, người ta không quan tâm giá trị thực tế của một enumeration là gì. Có một số cách để định nghĩa kiểu enumeration đơn giản này:

- sử dụng các thực thể của :class:`auto` làm giá trị
- sử dụng các thực thể của :class:`object` làm giá trị
- sử dụng một chuỗi mô tả làm giá trị
- sử dụng một tuple làm giá trị và một :meth:`~object.__new__` tùy chỉnh để thay thế tuple bằng một giá trị :class:`int`

Sử dụng bất kỳ phương pháp nào trong số này sẽ cho người dùng biết rằng các giá trị này không quan trọng, đồng thời cho phép thêm, xóa hoặc sắp xếp lại các thành viên mà không cần đánh lại số cho các thành viên còn lại.


Sử dụng :class:`auto`
"""""""""""""""""""""

Sử dụng :class:`auto` sẽ có dạng::

    >>> class Color(Enum):
    ...     RED = auto()
    ...     BLUE = auto()
    ...     GREEN = auto()
    ...
    >>> Color.GREEN
    <Color.GREEN: 3>


Sử dụng :class:`object`
"""""""""""""""""""""""

Việc sử dụng :class:`object` sẽ có dạng như sau::

    >>> class Color(Enum):
    ...     RED = object()
    ...     GREEN = object()
    ...     BLUE = object()
    ...
    >>> Color.GREEN                         # doctest: +SKIP
    <Color.GREEN: <object object at 0x...>>

Đây cũng là một ví dụ điển hình cho lý do bạn có thể muốn tự viết
:meth:`~object.__repr__`::

    >>> class Color(Enum):
    ...     RED = object()
    ...     GREEN = object()
    ...     BLUE = object()
    ...     def __repr__(self):
    ...         return "<%s.%s>" % (self.__class__.__name__, self._name_)
    ...
    >>> Color.GREEN
    <Color.GREEN>



Sử dụng một chuỗi mô tả
"""""""""""""""""""""""

Việc sử dụng một chuỗi làm giá trị sẽ có dạng như sau::

    >>> class Color(Enum):
    ...     RED = 'stop'
    ...     GREEN = 'go'
    ...     BLUE = 'too fast!'
    ...
    >>> Color.GREEN
    <Color.GREEN: 'go'>


Sử dụng một :meth:`~object.__new__` tùy chỉnh
"""""""""""""""""""""""""""""""""""""""""""""

Sử dụng một :meth:`~object.__new__` tự động đánh số sẽ trông như sau::

    >>> class AutoNumber(Enum):
    ...     def __new__(cls):
    ...         value = len(cls.__members__) + 1
    ...         obj = object.__new__(cls)
    ...         obj._value_ = value
    ...         return obj
    ...
    >>> class Color(AutoNumber):
    ...     RED = ()
    ...     GREEN = ()
    ...     BLUE = ()
    ...
    >>> Color.GREEN
    <Color.GREEN: 2>

Để tạo một ``AutoNumber`` có mục đích tổng quát hơn, hãy thêm ``*args`` vào chữ ký::

    >>> class AutoNumber(Enum):
    ...     def __new__(cls, *args):      # đây là thay đổi duy nhất so với phần trên
    ...         value = len(cls.__members__) + 1
    ...         obj = object.__new__(cls)
    ...         obj._value_ = value
    ...         return obj
    ...

Sau đó, khi kế thừa từ ``AutoNumber``, bạn có thể viết ``__init__`` của riêng mình để xử lý mọi đối số bổ sung::

    >>> class Swatch(AutoNumber):
    ...     def __init__(self, pantone='unknown'):
    ...         self.pantone = pantone
    ...     AUBURN = '3497'
    ...     SEA_GREEN = '1246'
    ...     BLEACHED_CORAL = () # Màu mới, chưa có mã Pantone!
    ...
    >>> Swatch.SEA_GREEN
    <Swatch.SEA_GREEN: 2>
    >>> Swatch.SEA_GREEN.pantone
    '1246'
    >>> Swatch.BLEACHED_CORAL.pantone
    'unknown'

.. note::

    Phương thức :meth:`~object.__new__`, nếu được định nghĩa, sẽ được sử dụng trong quá trình tạo các thành viên Enum; sau đó, nó được thay thế bằng :meth:`~object.__new__` của Enum, được sử dụng sau khi lớp được tạo để tra cứu các thành viên hiện có.

.. warning::

    *Không được* gọi ``super().__new__()``, vì ``__new__`` chỉ dùng để tra cứu mới là phương thức được tìm thấy; thay vào đó, hãy sử dụng trực tiếp kiểu dữ liệu -- ví dụ::

       obj = int.__new__(cls, value)


.. _`OrderedEnum`:

OrderedEnum
^^^^^^^^^^^

Một enumeration có thứ tự không dựa trên :class:`IntEnum` và do đó duy trì các bất biến :class:`Enum` thông thường (chẳng hạn như không thể so sánh với các enumeration khác)::

    >>> class OrderedEnum(Enum):
    ...     def __ge__(self, other):
    ...         if self.__class__ is other.__class__:
    ...             return self.value >= other.value
    ...         return NotImplemented
    ...     def __gt__(self, other):
    ...         if self.__class__ is other.__class__:
    ...             return self.value > other.value
    ...         return NotImplemented
    ...     def __le__(self, other):
    ...         if self.__class__ is other.__class__:
    ...             return self.value <= other.value
    ...         return NotImplemented
    ...     def __lt__(self, other):
    ...         if self.__class__ is other.__class__:
    ...             return self.value < other.value
    ...         return NotImplemented
    ...
    >>> class Grade(OrderedEnum):
    ...     A = 5
    ...     B = 4
    ...     C = 3
    ...     D = 2
    ...     F = 1
    ...
    >>> Grade.C < Grade.A
    True


DuplicateFreeEnum
^^^^^^^^^^^^^^^^^

Phát sinh lỗi nếu tìm thấy giá trị thành viên trùng lặp thay vì tạo một alias::

    >>> class DuplicateFreeEnum(Enum):
    ...     def __init__(self, *args):
    ...         cls = self.__class__
    ...         if any(self.value == e.value for e in cls):
    ...             a = self.name
    ...             e = cls(self.value).name
    ...             raise ValueError(
    ...                 "aliases not allowed in DuplicateFreeEnum:  %r --> %r"
    ...                 % (a, e))
    ...
    >>> class Color(DuplicateFreeEnum):
    ...     RED = 1
    ...     GREEN = 2
    ...     BLUE = 3
    ...     GRENE = 2
    ...
    Traceback (most recent call last):
      ...
    ValueError: aliases not allowed in DuplicateFreeEnum:  'GRENE' --> 'GREEN'

.. note::

    Đây là một ví dụ hữu ích về việc subclass Enum để thêm hoặc thay đổi các hành vi khác, đồng thời không cho phép alias. Nếu thay đổi duy nhất mong muốn là không cho phép alias, có thể sử dụng decorator :func:`unique` thay thế.

.. _multi-value-enum:

MultiValueEnum
^^^^^^^^^^^^^^

Hỗ trợ việc có nhiều hơn một giá trị cho mỗi thành viên::

    >>> class MultiValueEnum(Enum):
    ...     def __new__(cls, value, *values):
    ...         self = object.__new__(cls)
    ...         self._value_ = value
    ...         for v in values:
    ...             self._add_value_alias_(v)
    ...         return self
    ...
    >>> class DType(MultiValueEnum):
    ...     float32 = 'f', 8
    ...     double64 = 'd', 9
    ...
    >>> DType('f')
    <DType.float32: 'f'>
    >>> DType(9)
    <DType.double64: 'd'>


.. _`Planet`:

Planet
^^^^^^

Nếu :meth:`~object.__new__` hoặc :meth:`~object.__init__` được định nghĩa, giá trị của thành viên enum sẽ được truyền vào các phương thức đó::

    >>> class Planet(Enum):
    ...     MERCURY = (3.303e+23, 2.4397e6)
    ...     VENUS   = (4.869e+24, 6.0518e6)
    ...     EARTH   = (5.976e+24, 6.37814e6)
    ...     MARS    = (6.421e+23, 3.3972e6)
    ...     JUPITER = (1.9e+27,   7.1492e7)
    ...     SATURN  = (5.688e+26, 6.0268e7)
    ...     URANUS  = (8.686e+25, 2.5559e7)
    ...     NEPTUNE = (1.024e+26, 2.4746e7)
    ...     def __init__(self, mass, radius):
    ...         self.mass = mass       # tính bằng kilôgam
    ...         self.radius = radius   # tính bằng mét
    ...     @property
    ...     def surface_gravity(self):
    ...         # hằng số hấp dẫn vũ trụ (m3 kg-1 s-2)
    ...         G = 6.67300E-11
    ...         return G * self.mass / (self.radius * self.radius)
    ...
    >>> Planet.EARTH.value
    (5.976e+24, 6378140.0)
    >>> Planet.EARTH.surface_gravity
    9.802652743337129

.. _enum-time-period:

TimePeriod
^^^^^^^^^^

Ví dụ minh họa cách sử dụng thuộc tính :attr:`~Enum._ignore_`::

    >>> import datetime as dt
    >>> class Period(dt.timedelta, Enum):
    ...     "different lengths of time"
    ...     _ignore_ = 'Period i'
    ...     Period = vars()
    ...     for i in range(367):
    ...         Period['day_%d' % i] = i
    ...
    >>> list(Period)[:2]
    [<Period.day_0: datetime.timedelta(0)>, <Period.day_1: datetime.timedelta(days=1)>]
    >>> list(Period)[-2:]
    [<Period.day_365: datetime.timedelta(days=365)>, <Period.day_366: datetime.timedelta(days=366)>]


.. _enumtype-examples:

Phân lớp EnumType
-----------------

Mặc dù hầu hết nhu cầu về enum đều có thể được đáp ứng bằng cách tùy chỉnh các lớp con của :class:`Enum`, thông qua class decorator hoặc các hàm tùy chỉnh, :class:`EnumType` vẫn có thể được phân lớp để cung cấp trải nghiệm Enum khác biệt.
