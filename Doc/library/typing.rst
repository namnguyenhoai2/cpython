====================================
:mod:`!typing` --- Hỗ trợ gợi ý kiểu
====================================

.. testsetup:: *

   import typing
   from dataclasses import dataclass
   from typing import *

.. module:: typing
   :synopsis: Hỗ trợ gợi ý kiểu (xem :pep:`484`).

.. versionadded:: 3.5

**Mã nguồn:** :source:`Lib/typing.py`

.. note::

   Python runtime không thực thi các chú thích kiểu của hàm và biến. Các chú thích này có thể được các công cụ của bên thứ ba như :term:`trình kiểm tra kiểu <static type checker>`, IDE, linter, v.v. sử dụng.

--------------

Mô-đun này cung cấp hỗ trợ runtime cho các gợi ý kiểu.

Hãy xem xét hàm dưới đây::

   def surface_area_of_cube(edge_length: float) -> str:
       return f"The surface area of the cube is {6 * edge_length ** 2}."

Hàm ``surface_area_of_cube`` nhận một đối số được kỳ vọng là một thể hiện của :class:`float`, như được chỉ ra bởi :term:`type hint` ``edge_length: float``. Hàm này được kỳ vọng trả về một thể hiện của :class:`str`, như được chỉ ra bởi gợi ý ``-> str``.

Mặc dù type hint có thể là những class đơn giản như :class:`float` hoặc :class:`str`, chúng cũng có thể phức tạp hơn. Module :mod:`typing` cung cấp một bộ thuật ngữ cho các type hint nâng cao hơn.

Các tính năng mới thường xuyên được thêm vào module ``typing``. Package :pypi:`typing_extensions` cung cấp các bản backport của những tính năng mới này cho các phiên bản Python cũ hơn.

.. seealso::

   `Bảng tóm tắt typing <https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html>`_
       Tổng quan nhanh về type hint (được lưu trữ trên tài liệu mypy)

   Phần Tham khảo Hệ thống Kiểu của `tài liệu mypy <https://mypy.readthedocs.io/en/stable/index.html>`_
      Hệ thống typing của Python được tiêu chuẩn hóa thông qua các PEP, vì vậy tài liệu tham khảo này nhìn chung áp dụng cho hầu hết các trình kiểm tra kiểu Python. (Một số phần vẫn có thể chỉ áp dụng cho mypy.)

   `Typing tĩnh với Python <https://typing.python.org/en/latest/>`_
      Tài liệu không phụ thuộc type checker do cộng đồng biên soạn, trình bày chi tiết các tính năng của hệ thống kiểu, những công cụ hữu ích liên quan đến typing và các phương pháp hay nhất khi sử dụng typing.

.. _relevant-peps:

Đặc tả cho Hệ thống Kiểu của Python
===================================

Đặc tả chính thức, được cập nhật mới nhất về hệ thống kiểu của Python có tại `Đặc tả cho hệ thống kiểu của Python <https://typing.python.org/en/latest/spec/index.html>`_.

.. _type-aliases:

Bí danh kiểu
============

Bí danh kiểu được định nghĩa bằng câu lệnh :keyword:`type`, câu lệnh này tạo một thực thể của :class:`TypeAliasType`. Trong ví dụ này, ``Vector`` và ``list[float]`` sẽ được các trình kiểm tra kiểu tĩnh xem là tương đương::

   type Vector = list[float]

   def scale(scalar: float, vector: Vector) -> Vector:
       return [scalar * num for num in vector]

   # vượt qua kiểm tra kiểu; một danh sách các số thực được xem là một Vector.
   new_vector = scale(2.0, [1.0, -4.2, 5.4])

Bí danh kiểu hữu ích trong việc đơn giản hóa các chữ ký kiểu phức tạp. Ví dụ::

   from collections.abc import Sequence

   type ConnectionOptions = dict[str, str]
   type Address = tuple[str, int]
   type Server = tuple[Address, ConnectionOptions]

   def broadcast_message(message: str, servers: Sequence[Server]) -> None:
       ...

   # Trình kiểm tra kiểu tĩnh sẽ xem chữ ký kiểu trước đó là
   # hoàn toàn tương đương với chữ ký này.
   def broadcast_message(
       message: str,
       servers: Sequence[tuple[tuple[str, int], dict[str, str]]]
   ) -> None:
       ...

Câu lệnh :keyword:`type` là tính năng mới trong Python 3.12. Để đảm bảo tương thích ngược, bạn cũng có thể tạo bí danh kiểu bằng phép gán đơn giản::

   Vector = list[float]

Hoặc đánh dấu bằng :data:`TypeAlias` để nêu rõ đây là bí danh kiểu, không phải phép gán biến thông thường::

   from typing import TypeAlias

   Vector: TypeAlias = list[float]

.. _distinct:

NewType
=======

Sử dụng helper :class:`NewType` để tạo các kiểu riêng biệt::

   from typing import NewType

   UserId = NewType('UserId', int)
   some_id = UserId(524313)

Trình kiểm tra kiểu tĩnh sẽ xem kiểu mới như thể đó là một lớp con của kiểu ban đầu. Điều này hữu ích để giúp phát hiện các lỗi logic::

   def get_user_name(user_id: UserId) -> str:
       ...

   # vượt qua kiểm tra kiểu
   user_a = get_user_name(UserId(42351))

   # không vượt qua kiểm tra kiểu; int không phải là UserId
   user_b = get_user_name(-1)

Bạn vẫn có thể thực hiện mọi thao tác ``int`` trên một biến có kiểu ``UserId``, nhưng kết quả sẽ luôn có kiểu ``int``. Điều này cho phép bạn truyền một ``UserId`` ở bất cứ nơi nào có thể yêu cầu một ``int``, nhưng sẽ ngăn bạn vô tình tạo một ``UserId`` theo cách không hợp lệ::

   # 'output' có kiểu 'int', không phải 'UserId'
   output = UserId(23413) + UserId(54341)

Lưu ý rằng các kiểm tra này chỉ được thực thi bởi trình kiểm tra kiểu tĩnh. Khi chạy, câu lệnh ``Derived = NewType('Derived', Base)`` sẽ khiến ``Derived`` trở thành một callable ngay lập tức trả về bất kỳ tham số nào bạn truyền vào. Điều đó có nghĩa là biểu thức ``Derived(some_value)`` không tạo một class mới và hầu như không gây thêm overhead so với một lần gọi hàm thông thường.

Chính xác hơn, biểu thức ``some_value is Derived(some_value)`` luôn có giá trị true khi chạy.

Không hợp lệ khi tạo subtype của ``Derived``::

   from typing import NewType

   UserId = NewType('UserId', int)

   # Không thành công khi runtime và không vượt qua kiểm tra kiểu
   class AdminUserId(UserId): pass

Tuy nhiên, bạn có thể tạo một :class:`NewType` dựa trên một ``NewType`` 'dẫn xuất'.::

   from typing import NewType

   UserId = NewType('UserId', int)

   ProUserId = NewType('ProUserId', UserId)

và việc kiểm tra kiểu cho ``ProUserId`` sẽ hoạt động như mong đợi.

Xem :pep:`484` để biết thêm chi tiết.

.. note::

   Hãy nhớ rằng việc sử dụng bí danh kiểu khai báo hai kiểu là *tương đương* với nhau. Thực hiện ``type Alias = Original`` sẽ khiến bộ kiểm tra kiểu tĩnh xem ``Alias`` là *hoàn toàn tương đương* với ``Original`` trong mọi trường hợp. Điều này hữu ích khi bạn muốn đơn giản hóa các chữ ký kiểu phức tạp.

   Ngược lại, ``NewType`` khai báo một kiểu là *kiểu con* của một kiểu khác. Thực hiện ``Derived = NewType('Derived', Original)`` sẽ khiến bộ kiểm tra kiểu tĩnh xem ``Derived`` là một *lớp con* của ``Original``, nghĩa là một giá trị kiểu ``Original`` không thể được sử dụng ở nơi yêu cầu một giá trị kiểu ``Derived``. Điều này hữu ích khi bạn muốn ngăn ngừa lỗi logic với chi phí runtime tối thiểu.

.. versionadded:: 3.5.2

.. versionchanged:: 3.10
   ``NewType`` hiện là một lớp thay vì một hàm. Do đó, việc gọi ``NewType`` sẽ tốn thêm chi phí runtime so với một hàm thông thường.

.. versionchanged:: 3.11
   Hiệu năng khi gọi ``NewType`` đã được khôi phục về mức như trong Python 3.9.

.. _annotating-callables:

Chú thích cho các đối tượng có thể gọi
======================================

Các hàm -- hoặc những đối tượng :term:`callable` khác -- có thể được chú thích bằng
:class:`collections.abc.Callable` hoặc :data:`typing.Callable` đã lỗi thời. ``Callable[[int], str]`` biểu thị một hàm nhận một tham số duy nhất thuộc kiểu :class:`int` và trả về một :class:`str`.

Ví dụ:

.. testcode::

   from collections.abc import Callable, Awaitable

   def feeder(get_next_item: Callable[[], str]) -> None:
       ...  # Thân hàm

   def async_query(on_success: Callable[[int], None],
                   on_error: Callable[[int, Exception], None]) -> None:
       ...  # Thân hàm

   async def on_update(value: str) -> None:
       ...  # Thân hàm

   callback: Callable[[str], Awaitable[None]] = on_update

.. index:: single: ...; ellipsis literal

Cú pháp subscription phải luôn được sử dụng với đúng hai giá trị: danh sách đối số và kiểu trả về. Danh sách đối số phải là một danh sách các kiểu, một :class:`ParamSpec`, :data:`Concatenate`, hoặc một dấu chấm lửng (``...``). Kiểu trả về phải là một kiểu duy nhất.

Nếu một dấu chấm lửng literal ``...`` được cung cấp làm danh sách đối số, điều đó cho biết rằng một callable với bất kỳ danh sách tham số nào cũng được chấp nhận:

.. testcode::

   def concat(x: str, y: str) -> str:
       return x + y

   x: Callable[..., str]
   x = str     # OK
   x = concat  # Cũng OK

``Callable`` không thể biểu diễn các signature phức tạp, chẳng hạn như các hàm nhận số lượng đối số biến đổi, :ref:`các hàm overloaded <overload>`, hoặc các hàm có tham số chỉ dành cho từ khóa. Tuy nhiên, có thể biểu diễn các signature này bằng cách định nghĩa một lớp :class:`Protocol` với một
phương thức :meth:`~object.__call__`:

.. testcode::

   from collections.abc import Iterable
   from typing import Protocol

   class Combiner(Protocol):
       def __call__(self, *vals: bytes, maxlen: int | None = None) -> list[bytes]: ...

   def batch_proc(data: Iterable[bytes], cb_results: Combiner) -> bytes:
       for item in data:
           ...

   def good_cb(*vals: bytes, maxlen: int | None = None) -> list[bytes]:
       ...
   def bad_cb(*vals: bytes, maxitems: int | None) -> list[bytes]:
       ...

   batch_proc([], good_cb)  # OK
   batch_proc([], bad_cb)   # Lỗi! Đối số 2 có kiểu không tương thích vì
                            # tên và loại khác nhau trong callback

Các callable nhận những callable khác làm đối số có thể cho biết rằng kiểu tham số của chúng phụ thuộc lẫn nhau bằng cách sử dụng :class:`ParamSpec`. Ngoài ra, nếu callable đó thêm hoặc xóa các đối số khỏi những callable khác, có thể sử dụng toán tử :data:`Concatenate`. Chúng lần lượt có dạng ``Callable[ParamSpecVariable, ReturnType]`` và ``Callable[Concatenate[Arg1Type, Arg2Type, ..., ParamSpecVariable], ReturnType]``.

.. versionchanged:: 3.10
   ``Callable`` hiện hỗ trợ :class:`ParamSpec` và :data:`Concatenate`. Xem :pep:`612` để biết thêm chi tiết.

.. seealso::
   Tài liệu dành cho :class:`ParamSpec` và :class:`Concatenate` cung cấp các ví dụ về cách sử dụng trong ``Callable``.

.. _generics:

Generics
========

Vì không thể suy luận tĩnh một cách tổng quát thông tin kiểu của các đối tượng được lưu trong container, nhiều lớp container trong thư viện chuẩn hỗ trợ cú pháp subscription để biểu thị các kiểu dự kiến của phần tử container.

.. testcode::

   from collections.abc import Mapping, Sequence

   class Employee: ...

   # Sequence[Employee] cho biết tất cả phần tử trong sequence
   # phải là các instance của "Employee".
   # Mapping[str, str] cho biết tất cả key và value trong mapping
   # phải là chuỗi.
   def notify_by_email(employees: Sequence[Employee],
                       overrides: Mapping[str, str]) -> None: ...

Các hàm và lớp generic có thể được tham số hóa bằng cách sử dụng
:ref:`cú pháp tham số kiểu <type-params>`::

   from collections.abc import Sequence

   def first[T](l: Sequence[T]) -> T:  # Hàm có tính generic với TypeVar "T"
       return l[0]

Hoặc bằng cách sử dụng trực tiếp factory :class:`TypeVar`::

   from collections.abc import Sequence
   from typing import TypeVar

   U = TypeVar('U')                  # Khai báo biến kiểu "U"

   def second(l: Sequence[U]) -> U:  # Hàm có tính generic với TypeVar "U"
       return l[1]

.. versionchanged:: 3.12
   Hỗ trợ cú pháp cho generics là tính năng mới trong Python 3.12.

.. _annotating-tuples:

Chú thích kiểu cho tuple
========================

Đối với hầu hết container trong Python, hệ thống typing giả định rằng tất cả phần tử trong container sẽ có cùng một kiểu. Ví dụ::

   from collections.abc import Mapping

   # Trình kiểm tra kiểu sẽ suy luận rằng tất cả các phần tử trong ``x`` đều là ints
   x: list[int] = []

   # Lỗi của trình kiểm tra kiểu: ``list`` chỉ chấp nhận một đối số kiểu duy nhất:
   y: list[int, str] = [1, 'foo']

   # Trình kiểm tra kiểu sẽ suy luận rằng tất cả các khóa trong ``z`` đều là strings,
   # và tất cả các giá trị trong ``z`` đều là strings hoặc ints
   z: Mapping[str, str | int] = {}

:class:`list` chỉ chấp nhận một đối số kiểu, vì vậy trình kiểm tra kiểu sẽ báo lỗi tại phép gán ``y`` ở trên. Tương tự,
:class:`~collections.abc.Mapping` chỉ chấp nhận hai đối số kiểu: đối số thứ nhất cho biết kiểu của các khóa, còn đối số thứ hai cho biết kiểu của các giá trị.

Tuy nhiên, không giống hầu hết các container khác trong Python, trong mã Python theo phong cách chuẩn, việc các phần tử của tuple không cùng một kiểu là điều phổ biến. Vì lý do này, tuple được xử lý đặc biệt trong hệ thống typing của Python. :class:`tuple` chấp nhận *bất kỳ số lượng nào* đối số kiểu::

   # OK: ``x`` được gán cho một tuple có độ dài 1, trong đó phần tử duy nhất là một int
   x: tuple[int] = (5,)

   # OK: ``y`` được gán cho một tuple có độ dài 2;
   # phần tử 1 là một int, phần tử 2 là một str
   y: tuple[int, str] = (5, "foo")

   # Error: the type annotation indicates a tuple of length 1,
   # nhưng ``z`` đã được gán cho một tuple có độ dài 3
   z: tuple[int] = (1, 2, 3)

.. index:: single: ...; ellipsis literal

Để biểu thị một tuple có thể có độ dài *bất kỳ*, trong đó tất cả các phần tử đều có cùng kiểu ``T``, hãy sử dụng dấu chấm lửng literal ``...``: ``tuple[T, ...]``. Để biểu thị một tuple rỗng, hãy sử dụng ``tuple[()]``. Việc sử dụng riêng ``tuple`` làm chú thích tương đương với việc sử dụng ``tuple[Any, ...]``::

   x: tuple[int, ...] = (1, 2)
   # Các phép gán lại này đều hợp lệ: ``tuple[int, ...]`` cho biết x có thể có độ dài bất kỳ
   x = (1, 2, 3)
   x = ()
   # Phép gán lại này gây lỗi: tất cả các phần tử trong ``x`` phải là int
   x = ("foo", "bar")

   # ``y`` chỉ có thể được gán cho một tuple rỗng
   y: tuple[()] = ()

   z: tuple = ("foo", "bar")
   # Các phép gán lại này đều hợp lệ: ``tuple`` thuần túy tương đương với ``tuple[Any, ...]``
   z = (1, 2, 3)
   z = ()

.. _type-of-class-objects:

Kiểu của các đối tượng lớp
==========================

Một biến được chú thích bằng ``C`` có thể nhận một giá trị thuộc kiểu ``C``. Ngược lại, một biến được chú thích bằng ``type[C]`` (hoặc không còn được khuyến nghị
:class:`typing.Type[C] <Type>`) có thể nhận các giá trị vốn là các lớp -- cụ thể là, nó sẽ nhận *đối tượng lớp* của ``C``. Ví dụ::

   a = 3         # Có kiểu ``int``
   b = int       # Có kiểu ``type[int]``
   c = type(a)   # Cũng có kiểu ``type[int]``

Lưu ý rằng ``type[C]`` là covariant::

   class User: ...
   class ProUser(User): ...
   class TeamUser(User): ...

   def make_new_user(user_class: type[User]) -> User:
       # ...
       return user_class()

   make_new_user(User)      # OK
   make_new_user(ProUser)   # Cũng hợp lệ: ``type[ProUser]`` là kiểu con của ``type[User]``
   make_new_user(TeamUser)  # Vẫn hợp lệ
   make_new_user(User())    # Lỗi: cần ``type[User]`` nhưng nhận được ``User``
   make_new_user(int)       # Lỗi: ``type[int]`` không phải là kiểu con của ``type[User]``

Các tham số hợp lệ duy nhất cho :class:`type` là các lớp, :data:`Any`,
:ref:`biến kiểu <generics>`, và hợp của bất kỳ kiểu nào trong số này. Ví dụ::

   def new_non_team_user(user_class: type[BasicUser | ProUser]): ...

   new_non_team_user(BasicUser)  # OK
   new_non_team_user(ProUser)    # OK
   new_non_team_user(TeamUser)   # Lỗi: ``type[TeamUser]`` không phải là kiểu con
                                 # của ``type[BasicUser | ProUser]``
   new_non_team_user(User)       # Cũng là một lỗi

``type[Any]`` tương đương với :class:`type`, là gốc của Python
:ref:`hệ thống phân cấp metaclass <metaclasses>`.


.. _annotating-generators-and-coroutines:

Chú thích generator và coroutine
================================

Có thể chú thích generator bằng kiểu generic
:class:`Generator[YieldType, SendType, ReturnType] <collections.abc.Generator>`. Ví dụ::

   def echo_round() -> Generator[int, float, str]:
       sent = yield 0
       while sent >= 0:
           sent = yield round(sent)
       return 'Done'

Lưu ý rằng, không giống như nhiều lớp generic khác trong standard library, ``SendType`` của :class:`~collections.abc.Generator` có tính phản biến (contravariant), không phải đồng biến (covariant) hay bất biến (invariant).

Các tham số ``SendType`` và ``ReturnType`` mặc định là :const:`!None`::

   def infinite_stream(start: int) -> Generator[int]:
       while True:
           yield start
           start += 1

Bạn cũng có thể thiết lập rõ ràng các kiểu này::

   def infinite_stream(start: int) -> Generator[int, None, None]:
       while True:
           yield start
           start += 1

Các generator đơn giản chỉ yield giá trị cũng có thể được chú thích là có kiểu trả về là một trong hai
:class:`Iterable[YieldType] <collections.abc.Iterable>` hoặc :class:`Iterator[YieldType] <collections.abc.Iterator>`::

   def infinite_stream(start: int) -> Iterator[int]:
       while True:
           yield start
           start += 1

Các async generator được xử lý tương tự, nhưng không cần đối số kiểu ``ReturnType`` (:class:`AsyncGenerator[YieldType, SendType] <collections.abc.AsyncGenerator>`). Đối số ``SendType`` mặc định là :const:`!None`, vì vậy các định nghĩa sau là tương đương::

   async def infinite_stream(start: int) -> AsyncGenerator[int]:
       while True:
           yield start
           start = await increment(start)

   async def infinite_stream(start: int) -> AsyncGenerator[int, None]:
       while True:
           yield start
           start = await increment(start)

Như trong trường hợp đồng bộ,
:class:`AsyncIterable[YieldType] <collections.abc.AsyncIterable>` và :class:`AsyncIterator[YieldType] <collections.abc.AsyncIterator>` cũng có sẵn::

   async def infinite_stream(start: int) -> AsyncIterator[int]:
       while True:
           yield start
           start = await increment(start)

Có thể chú thích coroutine bằng
:class:`Coroutine[YieldType, SendType, ReturnType] <collections.abc.Coroutine>`. Các đối số generic tương ứng với các đối số của :class:`~collections.abc.Generator`, chẳng hạn như::

   from collections.abc import Coroutine
   c: Coroutine[list[str], str, int]  # Một coroutine được định nghĩa ở nơi khác
   x = c.send('hi')                   # Kiểu được suy luận của 'x' là list[str]
   async def bar() -> None:
       y = await c                    # Kiểu được suy luận của 'y' là int

.. _user-defined-generics:

Các kiểu generic do người dùng định nghĩa
=========================================

Một lớp do người dùng định nghĩa có thể được khai báo là lớp generic.

::

   from logging import Logger

   class LoggedVar[T]:
       def __init__(self, value: T, name: str, logger: Logger) -> None:
           self.name = name
           self.logger = logger
           self.value = value

       def set(self, new: T) -> None:
           self.log('Set ' + repr(self.value))
           self.value = new

       def get(self) -> T:
           self.log('Get ' + repr(self.value))
           return self.value

       def log(self, message: str) -> None:
           self.logger.info('%s: %s', self.name, message)

Cú pháp này cho biết rằng lớp ``LoggedVar`` được tham số hóa quanh một :ref:`biến kiểu <typevar>` ``T`` . Điều này cũng khiến ``T`` hợp lệ dưới dạng một kiểu trong thân lớp.

Các lớp generic ngầm kế thừa từ :class:`Generic`. Để tương thích với Python 3.11 trở xuống, bạn cũng có thể kế thừa rõ ràng từ
:class:`Generic` để chỉ báo một lớp generic::

   from typing import TypeVar, Generic

   T = TypeVar('T')

   class LoggedVar(Generic[T]):
       ...

Các lớp generic có các phương thức :meth:`~object.__class_getitem__`, nghĩa là chúng có thể được tham số hóa tại runtime (ví dụ: ``LoggedVar[int]`` bên dưới)::

   from collections.abc import Iterable

   def zero_all_vars(vars: Iterable[LoggedVar[int]]) -> None:
       for var in vars:
           var.set(0)

Một kiểu generic có thể có bất kỳ số lượng biến kiểu nào. Mọi dạng của
:class:`TypeVar` đều được phép dùng làm tham số cho một kiểu generic::

   from typing import TypeVar, Generic, Sequence

   class WeirdTrio[T, B: Sequence[bytes], S: (int, str)]:
       ...

   OldT = TypeVar('OldT', contravariant=True)
   OldB = TypeVar('OldB', bound=Sequence[bytes], covariant=True)
   OldS = TypeVar('OldS', int, str)

   class OldWeirdTrio(Generic[OldT, OldB, OldS]):
       ...

Mỗi đối số biến kiểu của :class:`Generic` phải là duy nhất. Do đó, cách sau không hợp lệ::

   from typing import TypeVar, Generic
   ...

   class Pair[M, M]:  # SyntaxError
       ...

   T = TypeVar('T')

   class Pair(Generic[T, T]):   # KHÔNG HỢP LỆ
       ...

Các lớp generic cũng có thể kế thừa từ các lớp khác::

   from collections.abc import Sized

   class LinkedList[T](Sized):
       ...

Khi kế thừa từ các lớp generic, một số tham số kiểu có thể được cố định::

    from collections.abc import Mapping

    class MyDict[T](Mapping[str, T]):
        ...

Trong trường hợp này ``MyDict`` có một tham số duy nhất, ``T``.

Việc sử dụng một lớp generic mà không chỉ định các tham số kiểu sẽ giả định
:data:`Any` cho mỗi vị trí. Trong ví dụ sau, ``MyIterable`` không phải là generic nhưng ngầm kế thừa từ ``Iterable[Any]``:

.. testcode::

   from collections.abc import Iterable

   class MyIterable(Iterable): # Giống với Iterable[Any]
       ...

Bí danh kiểu generic do người dùng định nghĩa cũng được hỗ trợ. Ví dụ::

   from collections.abc import Iterable

   type Response[S] = Iterable[S] | int

   # Kiểu trả về ở đây giống với Iterable[str] | int
   def response(query: str) -> Response[str]:
       ...

   type Vec[T] = Iterable[tuple[T, T]]

   def inproduct[T: (int, float, complex)](v: Vec[T]) -> T: # Giống với Iterable[tuple[T, T]]
       return sum(x*y for x, y in v)

Để đảm bảo khả năng tương thích ngược, bạn cũng có thể tạo bí danh kiểu generic thông qua phép gán đơn giản::

   from collections.abc import Iterable
   from typing import TypeVar

   S = TypeVar("S")
   Response = Iterable[S] | int

.. versionchanged:: 3.7
    :class:`Generic` no longer has a custom metaclass.

.. versionchanged:: 3.12
   Hỗ trợ cú pháp cho generic và bí danh kiểu là tính năng mới trong phiên bản 3.12. Trước đây, các lớp generic phải kế thừa tường minh từ :class:`Generic` hoặc chứa một biến kiểu trong một trong các lớp cơ sở của chúng.

Generic do người dùng định nghĩa cho các biểu thức tham số cũng được hỗ trợ thông qua các biến đặc tả tham số dưới dạng ``[**P]``. Hành vi này nhất quán với các biến kiểu được mô tả ở trên, vì các biến đặc tả tham số được mô-đun :mod:`!typing` xử lý như một biến kiểu chuyên biệt. Ngoại lệ duy nhất là có thể sử dụng một danh sách các kiểu để thay thế cho một :class:`ParamSpec`::

   >>> class Z[T, **P]: ...  # T là TypeVar; P là ParamSpec
   ...
   >>> Z[int, [dict, float]]
   __main__.Z[int, [dict, float]]

Các lớp generic trên một :class:`ParamSpec` cũng có thể được tạo bằng cách kế thừa tường minh từ :class:`Generic`. Trong trường hợp này, ``**`` không được sử dụng::

   from typing import ParamSpec, Generic

   P = ParamSpec('P')

   class Z(Generic[P]):
       ...

Một điểm khác biệt nữa giữa :class:`TypeVar` và :class:`ParamSpec` là generic chỉ có một biến đặc tả tham số sẽ chấp nhận các danh sách tham số ở dạng ``X[[Type1, Type2, ...]]`` và cả ``X[Type1, Type2, ...]`` vì lý do thẩm mỹ. Về nội bộ, dạng sau được chuyển đổi thành dạng trước, vì vậy các khai báo sau là tương đương::

   >>> class X[**P]: ...
   ...
   >>> X[int, str]
   __main__.X[[int, str]]
   >>> X[[int, str]]
   __main__.X[[int, str]]

Lưu ý rằng trong một số trường hợp, các generic có :class:`ParamSpec` có thể không có ``__parameters__`` chính xác sau khi thay thế, vì chúng chủ yếu được dùng để kiểm tra kiểu tĩnh.

.. versionchanged:: 3.10
   :class:`Generic` can now be parameterized over parameter expressions.
   Xem :class:`ParamSpec` và :pep:`612` để biết thêm chi tiết.

Một lớp generic do người dùng định nghĩa có thể có các ABC làm lớp cơ sở mà không xảy ra xung đột metaclass. Không hỗ trợ generic metaclass. Kết quả của việc tham số hóa generic được lưu vào bộ nhớ đệm, và hầu hết các kiểu trong mô-đun :mod:`!typing` đều :term:`hashable` và có thể so sánh bằng nhau.


Kiểu :data:`Any`
================

Một loại kiểu đặc biệt là :data:`Any`. Trình kiểm tra kiểu tĩnh sẽ coi mọi kiểu đều có thể gán cho :data:`Any` và :data:`Any` có thể gán cho mọi kiểu.

Điều này có nghĩa là bạn có thể thực hiện bất kỳ thao tác hoặc lời gọi phương thức nào trên một giá trị có kiểu :data:`Any` và gán giá trị đó cho bất kỳ biến nào::

   from typing import Any

   a: Any = None
   a = []          # OK
   a = 2           # OK

   s: str = ''
   s = a           # OK

   def foo(item: Any) -> int:
       # Vượt qua kiểm tra kiểu; 'item' có thể thuộc bất kỳ kiểu nào,
       # và kiểu đó có thể có một phương thức 'bar'
       item.bar()
       ...

Lưu ý rằng không có kiểm tra kiểu nào được thực hiện khi gán một giá trị có kiểu
Gán :data:`Any` cho một kiểu chính xác hơn. Ví dụ, trình kiểm tra kiểu tĩnh không báo lỗi khi gán ``a`` cho ``s``, mặc dù ``s`` được khai báo có kiểu :class:`str` và nhận một giá trị :class:`int` trong runtime!

Hơn nữa, tất cả các hàm không có kiểu trả về hoặc kiểu tham số sẽ mặc định ngầm sử dụng :data:`Any`::

   def legacy_parser(text):
       ...
       return data

   # trình kiểm tra kiểu tĩnh sẽ xem phần trên
   # là có cùng chữ ký với:
   def legacy_parser(text: Any) -> Any:
       ...
       return data

Hành vi này cho phép :data:`Any` được sử dụng như một *lối thoát* khi bạn cần kết hợp mã được định kiểu động và mã được định kiểu tĩnh.

Hãy so sánh hành vi của :data:`Any` với hành vi của :class:`object`. Tương tự như :data:`Any`, mọi kiểu đều là kiểu con của :class:`object`. Tuy nhiên, không giống :data:`Any`, điều ngược lại không đúng: :class:`object` *không* phải là kiểu con của mọi kiểu khác.

Điều đó có nghĩa là khi kiểu của một giá trị là :class:`object`, trình kiểm tra kiểu sẽ từ chối hầu hết mọi thao tác trên giá trị đó, và việc gán nó cho một biến (hoặc sử dụng nó làm giá trị trả về) có kiểu chuyên biệt hơn sẽ là một lỗi kiểu. Ví dụ::

   def hash_a(item: object) -> int:
       # Không vượt qua kiểm tra kiểu; một object không có phương thức 'magic'.
       item.magic()
       ...

   def hash_b(item: Any) -> int:
       # Vượt qua kiểm tra kiểu
       item.magic()
       ...

   # Vượt qua kiểm tra kiểu, vì int và str là các lớp con của object
   hash_a(42)
   hash_a("foo")

   # Vượt qua kiểm tra kiểu, vì Any có thể được gán cho mọi kiểu
   hash_b(42)
   hash_b("foo")

Sử dụng :class:`object` để chỉ ra theo cách an toàn kiểu rằng một giá trị có thể thuộc bất kỳ kiểu nào. Sử dụng :data:`Any` để chỉ ra rằng một giá trị có kiểu động.


Kiểu con danh nghĩa và kiểu con cấu trúc
========================================

Ban đầu, :pep:`484` định nghĩa hệ thống kiểu tĩnh của Python là sử dụng *kiểu con danh nghĩa*. Điều này có nghĩa là một lớp ``A`` được phép sử dụng ở nơi dự kiến một lớp ``B`` khi và chỉ khi ``A`` là lớp con của ``B``.

Yêu cầu này trước đây cũng áp dụng cho các lớp cơ sở trừu tượng, chẳng hạn như
:class:`~collections.abc.Iterable`. Vấn đề với cách tiếp cận này là một lớp phải được đánh dấu rõ ràng để hỗ trợ chúng, điều này không mang tính Pythonic và không giống cách người ta thường viết mã Python định kiểu động theo phong cách tự nhiên. Ví dụ, điều này tuân theo :pep:`484`::

   from collections.abc import Sized, Iterable, Iterator

   class Bucket(Sized, Iterable[int]):
       ...
       def __len__(self) -> int: ...
       def __iter__(self) -> Iterator[int]: ...

:pep:`544` giải quyết vấn đề này bằng cách cho phép người dùng viết đoạn mã trên mà không cần các lớp cơ sở rõ ràng trong định nghĩa lớp, cho phép ``Bucket`` được các trình kiểm tra kiểu tĩnh ngầm coi là kiểu con của cả ``Sized`` và ``Iterable[int]``. Điều này được gọi là *structural subtyping* (hoặc duck typing tĩnh)::

   from collections.abc import Iterator, Iterable

   class Bucket:  # Lưu ý: không có lớp cơ sở
       ...
       def __len__(self) -> int: ...
       def __iter__(self) -> Iterator[int]: ...

   def collect(items: Iterable[int]) -> int: ...
   result = collect(Bucket())  # Đạt kiểm tra kiểu

Ngoài ra, bằng cách kế thừa một lớp đặc biệt :class:`Protocol`, người dùng có thể định nghĩa các protocol tùy chỉnh mới để tận dụng đầy đủ structural subtyping (xem các ví dụ bên dưới).

Nội dung mô-đun
===============

Module ``typing`` định nghĩa các lớp, hàm và decorator sau đây.

Các primitive typing đặc biệt
-----------------------------

Các kiểu đặc biệt
"""""""""""""""""

Có thể sử dụng chúng làm kiểu trong các annotation. Chúng không hỗ trợ phép subscription bằng ``[]``.

.. data:: Any

   Kiểu đặc biệt biểu thị một kiểu không bị ràng buộc.

   * Mọi kiểu đều có thể gán cho :data:`Any`.
   * :data:`Any` có thể gán cho mọi kiểu.

   .. versionchanged:: 3.11
      :data:`Any` can now be used as a base class. This can be useful for
      tránh lỗi của trình kiểm tra kiểu với các lớp có thể duck type ở mọi nơi hoặc có tính động cao.

.. data:: AnyStr

   Một :ref:`biến kiểu bị ràng buộc <typing-constrained-typevar>`.

   Định nghĩa::

      AnyStr = TypeVar('AnyStr', str, bytes)

   ``AnyStr`` được dùng cho các hàm có thể chấp nhận :class:`str` hoặc
   :class:`bytes` các đối số nhưng không thể cho phép trộn lẫn hai loại này.

   Ví dụ::

      def concat(a: AnyStr, b: AnyStr) -> AnyStr:
          return a + b

      concat("foo", "bar")    # OK, đầu ra có kiểu 'str'
      concat(b"foo", b"bar")  # OK, đầu ra có kiểu 'bytes'
      concat("foo", b"bar")   # Lỗi, không thể kết hợp str và bytes

   Lưu ý rằng, bất chấp tên gọi, ``AnyStr`` không liên quan gì đến
   kiểu :class:`Any`, cũng không có nghĩa là "bất kỳ chuỗi nào". Cụ thể, ``AnyStr`` và ``str | bytes`` khác nhau và có các trường hợp sử dụng khác nhau::

      # Sử dụng AnyStr không hợp lệ:
      # Biến kiểu chỉ được sử dụng một lần trong chữ ký hàm,
      # nên không thể được bộ kiểm tra kiểu "giải"
      def greet_bad(cond: bool) -> AnyStr:
          return "hi there!" if cond else b"greetings!"

      # Cách tốt hơn để chú thích kiểu cho hàm này:
      def greet_proper(cond: bool) -> str | bytes:
          return "hi there!" if cond else b"greetings!"

   .. deprecated-removed:: 3.13 3.18
      Đã lỗi thời và được thay thế bằng cú pháp tham số :ref:`type mới <type-params>`. Sử dụng ``class A[T: (str, bytes)]: ...`` thay vì import ``AnyStr``. Xem
      :pep:`695` để biết thêm chi tiết.

      Trong Python 3.16, ``AnyStr`` sẽ bị xóa khỏi ``typing.__all__``, và cảnh báo ngừng sử dụng sẽ được phát ra tại runtime khi nó được truy cập hoặc import từ ``typing``. ``AnyStr`` sẽ bị xóa khỏi ``typing`` trong Python 3.18.

.. data:: LiteralString

   Kiểu đặc biệt chỉ bao gồm các chuỗi literal.

   Mọi chuỗi literal đều tương thích với ``LiteralString``, cũng như một ``LiteralString`` khác. Tuy nhiên, một đối tượng chỉ được định kiểu là ``str`` thì không. Một chuỗi được tạo bằng cách ghép các đối tượng có kiểu ``LiteralString`` cũng được chấp nhận là một ``LiteralString``.

   Ví dụ:

   .. testcode::

      def run_query(sql: LiteralString) -> None:
          ...

      def caller(arbitrary_string: str, literal_string: LiteralString) -> None:
          run_query("SELECT * FROM students")  # OK
          run_query(literal_string)  # OK
          run_query("SELECT * FROM " + literal_string)  # OK
          run_query(arbitrary_string)  # lỗi trình kiểm tra kiểu
          run_query(  # lỗi trình kiểm tra kiểu
              f"SELECT * FROM students WHERE name = {arbitrary_string}"
          )

   ``LiteralString`` hữu ích cho các API nhạy cảm, nơi các chuỗi tùy ý do người dùng tạo có thể gây ra sự cố. Ví dụ, hai trường hợp ở trên tạo ra lỗi trình kiểm tra kiểu có thể dễ bị tấn công SQL injection.

   Xem :pep:`675` để biết thêm chi tiết.

   .. versionadded:: 3.11

.. data:: Never
          NoReturn

   :data:`!Never` và :data:`!NoReturn` đại diện cho `kiểu bottom <https://en.wikipedia.org/wiki/Bottom_type>`_, một kiểu không có thành viên nào.

   Chúng có thể được dùng để chỉ ra rằng một hàm không bao giờ trả về, chẳng hạn như :func:`sys.exit`::

      from typing import Never  # hoặc NoReturn

      def stop() -> Never:
          raise RuntimeError('no way')

   Hoặc để định nghĩa một hàm không nên được gọi, vì không có đối số hợp lệ nào, chẳng hạn như
   :func:`assert_never`::

      from typing import Never  # hoặc NoReturn

      def never_call_me(arg: Never) -> None:
          pass

      def int_or_str(arg: int | str) -> None:
          never_call_me(arg)  # lỗi trình kiểm tra kiểu
          match arg:
              case int():
                  print("It's an int")
              case str():
                  print("It's a str")
              case _:
                  never_call_me(arg)  # OK, arg có kiểu Never (hoặc NoReturn)

   :data:`!Never` và :data:`!NoReturn` có cùng ý nghĩa trong hệ thống kiểu, và các trình kiểm tra kiểu tĩnh xử lý cả hai tương đương nhau.

   .. versionadded:: 3.6.2

      Đã thêm :data:`NoReturn`.

   .. versionadded:: 3.11

      Đã thêm :data:`Never`.

.. data:: Self

   Kiểu đặc biệt để biểu thị class bao quanh hiện tại.

   Ví dụ::

      from typing import Self, reveal_type

      class Foo:
          def return_self(self) -> Self:
              ...
              return self

      class SubclassOfFoo(Foo): pass

      reveal_type(Foo().return_self())  # Kiểu được xác định là "Foo"
      reveal_type(SubclassOfFoo().return_self())  # Kiểu được xác định là "SubclassOfFoo"

   Chú thích này tương đương về mặt ngữ nghĩa với nội dung sau, mặc dù ngắn gọn hơn::

      from typing import TypeVar

      Self = TypeVar("Self", bound="Foo")

      class Foo:
          def return_self(self: Self) -> Self:
              ...
              return self

   Nói chung, nếu một thứ trả về ``self``, như trong các ví dụ trên, bạn nên dùng ``Self`` làm chú thích kiểu trả về. Nếu ``Foo.return_self`` được chú thích là trả về ``"Foo"``, trình kiểm tra kiểu sẽ suy ra đối tượng được trả về từ ``SubclassOfFoo.return_self`` có kiểu ``Foo`` thay vì ``SubclassOfFoo``.

   Các trường hợp sử dụng phổ biến khác bao gồm:

   - Các :class:`classmethod`\s được dùng làm hàm khởi tạo thay thế và trả về các thực thể của tham số ``cls``.
   - Chú thích một phương thức :meth:`~object.__enter__` trả về chính nó.

   Bạn không nên dùng ``Self`` làm chú thích kiểu trả về nếu phương thức không được đảm bảo sẽ trả về một thực thể của lớp con khi lớp được phân lớp::

      class Eggs:
          # Self sẽ là chú thích kiểu trả về không chính xác ở đây,
          # vì đối tượng được trả về luôn là một thể hiện của Eggs,
          # ngay cả trong các lớp con
          def returns_eggs(self) -> "Eggs":
              return Eggs()

   Xem :pep:`673` để biết thêm chi tiết.

   .. versionadded:: 3.11

.. data:: TypeAlias

   Chú thích đặc biệt để khai báo rõ ràng một :ref:`bí danh kiểu <type-aliases>`.

   Ví dụ::

      from typing import TypeAlias

      Factors: TypeAlias = list[int]

   ``TypeAlias`` đặc biệt hữu ích trên các phiên bản Python cũ để chú thích những bí danh sử dụng tham chiếu chuyển tiếp, vì các trình kiểm tra kiểu có thể khó phân biệt chúng với các phép gán biến thông thường:

   .. testcode::

      from typing import Generic, TypeAlias, TypeVar

      T = TypeVar("T")

      # "Box" vẫn chưa tồn tại,
      # vì vậy chúng ta phải dùng dấu ngoặc kép cho tham chiếu chuyển tiếp trên Python <3.12.
      # Việc sử dụng ``TypeAlias`` cho trình kiểm tra kiểu biết rằng đây là một khai báo bí danh kiểu,
      # chứ không phải phép gán một biến cho một chuỗi.
      BoxOfStrings: TypeAlias = "Box[str]"

      class Box(Generic[T]):
          @classmethod
          def make_box_of_strings(cls) -> BoxOfStrings: ...

   Xem :pep:`613` để biết thêm chi tiết.

   .. versionadded:: 3.10

   .. deprecated:: 3.12
      :data:`TypeAlias` is deprecated in favor of the :keyword:`type` statement,
      tạo các instance của :class:`TypeAliasType` và hỗ trợ tham chiếu chuyển tiếp một cách tự nhiên. Lưu ý rằng mặc dù :data:`TypeAlias` và :class:`TypeAliasType` phục vụ các mục đích tương tự và có tên tương tự, chúng là các khái niệm riêng biệt, và cái sau không phải là kiểu của cái trước. Hiện chưa có kế hoạch loại bỏ :data:`TypeAlias`, nhưng người dùng được khuyến khích chuyển sang các câu lệnh :keyword:`type`.

Các dạng đặc biệt
"""""""""""""""""

Các kiểu này có thể được dùng trong chú thích kiểu. Tất cả đều hỗ trợ cú pháp subscription bằng ``[]``, nhưng mỗi kiểu có cú pháp riêng.

.. class:: Union

   Kiểu hợp (Union); ``Union[X, Y]`` tương đương với ``X | Y`` và có nghĩa là X hoặc Y.

   Để định nghĩa một kiểu hợp, hãy dùng chẳng hạn ``Union[int, str]`` hoặc dạng viết tắt ``int | str``. Khuyến nghị sử dụng dạng viết tắt này. Chi tiết:

   * Các đối số phải là kiểu và phải có ít nhất một đối số.

   * Các kiểu hợp của kiểu hợp sẽ được làm phẳng, chẳng hạn:::

       Union[Union[int, str], float] == Union[int, str, float]

     However, this does not apply to unions referenced through a type
     alias, to avoid forcing evaluation of the underlying :class:`TypeAliasType`::

       type A = Union[int, str]
       Union[A, float] != Union[int, str, float]

   * Các kiểu hợp chỉ có một đối số sẽ biến mất, chẳng hạn:::

       Union[int] == int  # Hàm khởi tạo thực sự trả về int

   * Các đối số dư thừa được bỏ qua, ví dụ:::

       Union[int, str, int] == Union[int, str] == int | str

   * Khi so sánh các union, thứ tự đối số bị bỏ qua, ví dụ:::

       Union[int, str] == Union[str, int]

   * Bạn không thể tạo lớp con hoặc khởi tạo một ``Union``.

   * Bạn không thể viết ``Union[X][Y]``.

   .. versionchanged:: 3.7
      Đừng loại bỏ các lớp con tường minh khỏi các union trong runtime.

   .. versionchanged:: 3.10
      Giờ đây, các union có thể được viết dưới dạng ``X | Y``. Xem
      :ref:`các biểu thức kiểu union <types-union>`.

   .. versionchanged:: 3.14
      :class:`types.UnionType` is now an alias for :class:`Union`, and both
      ``Union[int, str]`` và ``int | str`` tạo các instance của cùng một class. Để kiểm tra tại runtime xem một object có phải là ``Union`` hay không, hãy sử dụng ``isinstance(obj, Union)``. Để tương thích với các phiên bản Python trước đây, hãy sử dụng ``get_origin(obj) is typing.Union or get_origin(obj) is types.UnionType``.

.. data:: Optional

   ``Optional[X]`` tương đương với ``X | None`` (hoặc ``Union[X, None]``).

   Lưu ý rằng đây không phải là cùng một khái niệm với một đối số tùy chọn, tức là đối số có giá trị mặc định. Một đối số tùy chọn có giá trị mặc định không cần qualifier ``Optional`` trong type annotation chỉ vì nó là tùy chọn. Ví dụ:::

      def foo(arg: int = 0) -> None:
          ...

   Mặt khác, nếu cho phép giá trị ``None`` được chỉ định rõ ràng, thì việc sử dụng ``Optional`` là phù hợp, bất kể đối số đó có phải là tùy chọn hay không. Ví dụ:::

      def foo(arg: Optional[int] = None) -> None:
          ...

   .. versionchanged:: 3.10
      Giờ đây, Optional có thể được viết là ``X | None``. Xem
      :ref:`các biểu thức kiểu union <types-union>`.

.. data:: Concatenate

   Special form dùng để chú thích các hàm higher-order.

   .. index:: single: ...; ellipsis literal

   ``Concatenate`` có thể được sử dụng cùng với :ref:`Callable <annotating-callables>` và
   :class:`ParamSpec` để chú thích một higher-order callable bổ sung, loại bỏ hoặc biến đổi các tham số của một callable khác. Cách sử dụng có dạng ``Concatenate[Arg1Type, Arg2Type, ..., ParamSpecVariable]``. ``Concatenate`` hợp lệ khi được sử dụng trong các type hint :ref:`Callable <annotating-callables>` và khi khởi tạo các generic class do người dùng định nghĩa với các tham số :class:`ParamSpec`. Tham số cuối cùng của ``Concatenate`` phải là :class:`ParamSpec` hoặc dấu ba chấm (``...``).

   Ví dụ, để chú thích một decorator ``with_lock`` cung cấp một
   :class:`threading.Lock` cho hàm được decorator, có thể sử dụng ``Concatenate`` để cho biết rằng ``with_lock`` mong đợi một callable nhận một ``Lock`` làm đối số đầu tiên và trả về một callable có chữ ký kiểu khác. Trong trường hợp này, :class:`ParamSpec` cho biết rằng các kiểu tham số của callable được trả về phụ thuộc vào các kiểu tham số của callable được truyền vào::

      from collections.abc import Callable
      from threading import Lock
      from typing import Concatenate

      # Sử dụng khóa này để đảm bảo rằng chỉ một thread thực thi một hàm
      # tại một thời điểm.
      my_lock = Lock()

      def with_lock[**P, R](f: Callable[Concatenate[Lock, P], R]) -> Callable[P, R]:
          '''A type-safe decorator which provides a lock.'''
          def inner(*args: P.args, **kwargs: P.kwargs) -> R:
              # Truyền khóa làm đối số đầu tiên.
              return f(my_lock, *args, **kwargs)
          return inner

      @with_lock
      def sum_threadsafe(lock: Lock, numbers: list[float]) -> float:
          '''Add a list of numbers together in a thread-safe manner.'''
          with lock:
              return sum(numbers)

      # Nhờ decorator, chúng ta không cần tự truyền lock vào.
      sum_threadsafe([1.1, 2.2, 3.3])

   .. versionadded:: 3.10

   .. seealso::

      * :pep:`612` -- Biến đặc tả tham số (PEP đã giới thiệu ``ParamSpec`` và ``Concatenate``)
      * :class:`ParamSpec`
      * :ref:`annotating-callables`

.. data:: Literal

   Dạng typing đặc biệt để định nghĩa "literal types".

   ``Literal`` có thể được dùng để cho các trình kiểm tra kiểu biết rằng đối tượng được chú thích có giá trị tương đương với một trong các literal được cung cấp.

   Ví dụ::

      def validate_simple(data: Any) -> Literal[True]:  # luôn trả về True
          ...

      type Mode = Literal['r', 'rb', 'w', 'wb']
      def open_helper(file: str, mode: Mode) -> str:
          ...

      open_helper('/some/path', 'r')      # Vượt qua kiểm tra kiểu
      open_helper('/other/path', 'typo')  # Lỗi trong trình kiểm tra kiểu

   ``Literal[...]`` không thể được phân lớp. Trong runtime, một giá trị bất kỳ được phép làm đối số kiểu cho ``Literal[...]``, nhưng trình kiểm tra kiểu có thể áp đặt các hạn chế. Xem :pep:`586` để biết thêm chi tiết về các kiểu literal.

   Chi tiết bổ sung:

   * Các đối số phải là giá trị literal và phải có ít nhất một đối số.

   * Các kiểu ``Literal`` lồng nhau được làm phẳng, ví dụ:::

      assert Literal[Literal[1, 2], 3] == Literal[1, 2, 3]

     However, this does not apply to ``Literal`` types referenced through a type
     alias, to avoid forcing evaluation of the underlying :class:`TypeAliasType`::

      type A = Literal[1, 2]
      assert Literal[A, 3] != Literal[1, 2, 3]

   * Các đối số dư thừa được bỏ qua, ví dụ:::

      assert Literal[1, 2, 1] == Literal[1, 2]

   * Khi so sánh các literal, thứ tự của các đối số bị bỏ qua, ví dụ:::

      assert Literal[1, 2] == Literal[2, 1]

   * Bạn không thể tạo lớp con hoặc khởi tạo một ``Literal``.

   * Bạn không thể viết ``Literal[X][Y]``.

   .. versionadded:: 3.8

   .. versionchanged:: 3.9.1
      ``Literal`` hiện đã loại bỏ các tham số trùng lặp. Các phép so sánh bằng của các đối tượng ``Literal`` không còn phụ thuộc vào thứ tự. Các đối tượng ``Literal`` giờ đây sẽ phát sinh ngoại lệ :exc:`TypeError` trong quá trình so sánh bằng nếu một trong các tham số của chúng không phải là :term:`hashable`.

.. data:: ClassVar

   Cấu trúc kiểu đặc biệt để đánh dấu các biến lớp.

   Như đã giới thiệu trong :pep:`526`, một chú thích biến được bọc trong ClassVar cho biết một thuộc tính nhất định được thiết kế để dùng làm biến lớp và không nên được thiết lập trên các instance của lớp đó. Cách sử dụng::

      class Starship:
          stats: ClassVar[dict[str, int]] = {} # biến lớp
          damage: int = 10                     # biến instance

   :data:`ClassVar` chỉ chấp nhận các kiểu và không thể được tham số hóa thêm.

   :data:`ClassVar` bản thân không phải là một lớp và không thể được sử dụng với :func:`isinstance` hoặc :func:`issubclass`.
   :data:`ClassVar` không thay đổi hành vi runtime của Python, nhưng có thể được các trình kiểm tra kiểu tĩnh sử dụng. Ví dụ: một trình kiểm tra kiểu có thể đánh dấu đoạn mã sau là lỗi::

      enterprise_d = Starship(3000)
      enterprise_d.stats = {} # Lỗi, đang đặt biến lớp trên thực thể
      Starship.stats = {}     # Điều này hợp lệ

   .. versionadded:: 3.5.3

   .. versionchanged:: 3.13

      Giờ đây, :data:`ClassVar` có thể được lồng trong :data:`Final` và ngược lại.

.. data:: Final

   Cấu trúc typing đặc biệt để chỉ báo các tên final cho trình kiểm tra kiểu.

   Tên final không thể được gán lại trong bất kỳ phạm vi nào. Tên final được khai báo trong phạm vi lớp không thể bị ghi đè trong các lớp con.

   Ví dụ::

      MAX_SIZE: Final = 9000
      MAX_SIZE += 1  # Lỗi do type checker báo cáo

      class Connection:
          TIMEOUT: Final[int] = 10

      class FastConnector(Connection):
          TIMEOUT = 1  # Lỗi do type checker báo cáo

   Các thuộc tính này không được kiểm tra tại runtime. Xem :pep:`591` để biết thêm chi tiết.

   .. versionadded:: 3.8

   .. versionchanged:: 3.13

      :data:`Final` giờ đây có thể được lồng trong :data:`ClassVar` và ngược lại.

.. data:: Required

   Cấu trúc typing đặc biệt để đánh dấu một khóa :class:`TypedDict` là bắt buộc.

   Điều này chủ yếu hữu ích cho ``total=False`` TypedDict. Xem :class:`TypedDict` và :pep:`655` để biết thêm chi tiết.

   .. versionadded:: 3.11

.. data:: NotRequired

   Cấu trúc typing đặc biệt để đánh dấu một :class:`TypedDict` key có thể bị thiếu.

   Xem :class:`TypedDict` và :pep:`655` để biết thêm chi tiết.

   .. versionadded:: 3.11

.. data:: ReadOnly

   Cấu trúc typing đặc biệt để đánh dấu một phần tử của :class:`TypedDict` là chỉ đọc.

   Ví dụ::

      class Movie(TypedDict):
         title: ReadOnly[str]
         year: int

      def mutate_movie(m: Movie) -> None:
         m["year"] = 1999  # được phép
         m["title"] = "The Matrix"  # lỗi trình kiểm tra kiểu

   Không có việc kiểm tra thuộc tính này khi runtime.

   Xem :class:`TypedDict` và :pep:`705` để biết thêm chi tiết.

   .. versionadded:: 3.13

.. data:: Annotated

   Dạng typing đặc biệt để thêm metadata theo ngữ cảnh vào một annotation.

   Thêm metadata ``x`` vào một type ``T`` nhất định bằng cách sử dụng annotation ``Annotated[T, x]``. Metadata được thêm bằng ``Annotated`` có thể được các công cụ static analysis hoặc runtime sử dụng. Khi runtime, metadata được lưu trong thuộc tính :attr:`!__metadata__`.

   Nếu một thư viện hoặc công cụ gặp annotation ``Annotated[T, x]`` nhưng không có logic đặc biệt để xử lý metadata, thư viện hoặc công cụ đó nên bỏ qua metadata và chỉ coi annotation là ``T``. Vì vậy, ``Annotated`` có thể hữu ích cho mã muốn sử dụng annotation vào những mục đích nằm ngoài hệ thống static typing của Python.

   Việc sử dụng ``Annotated[T, x]`` làm annotation vẫn cho phép kiểm tra kiểu tĩnh đối với ``T``, vì các trình kiểm tra kiểu sẽ chỉ bỏ qua metadata ``x``. Theo cách này, ``Annotated`` khác với
   decorator :deco:`no_type_check`, cũng có thể được dùng để thêm annotation bên ngoài phạm vi của hệ thống typing, nhưng sẽ vô hiệu hóa hoàn toàn việc kiểm tra kiểu đối với một hàm hoặc lớp.

   Trách nhiệm diễn giải metadata thuộc về công cụ hoặc thư viện gặp chú thích ``Annotated``. Công cụ hoặc thư viện gặp kiểu ``Annotated`` có thể quét qua các phần tử metadata để xác định xem chúng có đáng quan tâm hay không (ví dụ: sử dụng :func:`isinstance`).

   .. describe:: Annotated[<type>, <metadata>]

   Dưới đây là ví dụ về cách bạn có thể sử dụng ``Annotated`` để thêm metadata vào các chú thích kiểu nếu đang thực hiện phân tích phạm vi:

   .. testcode::

      @dataclass
      class ValueRange:
          lo: int
          hi: int

      T1 = Annotated[int, ValueRange(-10, 5)]
      T2 = Annotated[T1, ValueRange(-20, 3)]

   Đối số đầu tiên của ``Annotated`` phải là một kiểu hợp lệ. Có thể cung cấp nhiều phần tử metadata vì ``Annotated`` hỗ trợ các đối số biến thiên. Thứ tự của các phần tử metadata được giữ nguyên và có ý nghĩa khi kiểm tra tính bằng nhau::

      @dataclass
      class ctype:
           kind: str

      a1 = Annotated[int, ValueRange(3, 10), ctype("char")]
      a2 = Annotated[int, ctype("char"), ValueRange(3, 10)]

      assert a1 != a2  # Thứ tự có ý nghĩa

   Công cụ sử dụng các chú thích sẽ quyết định liệu client có được phép thêm nhiều phần tử metadata vào một chú thích hay không, cũng như cách hợp nhất các chú thích đó.

   Các kiểu ``Annotated`` lồng nhau được làm phẳng. Thứ tự của các phần tử metadata bắt đầu từ chú thích bên trong cùng::

      assert Annotated[Annotated[int, ValueRange(3, 10)], ctype("char")] == Annotated[
          int, ValueRange(3, 10), ctype("char")
      ]

   Tuy nhiên, điều này không áp dụng cho các kiểu ``Annotated`` được tham chiếu thông qua bí danh kiểu, nhằm tránh buộc phải đánh giá :class:`TypeAliasType` bên dưới::

      type From3To10[T] = Annotated[T, ValueRange(3, 10)]
      assert Annotated[From3To10[int], ctype("char")] != Annotated[
         int, ValueRange(3, 10), ctype("char")
      ]

   Các phần tử metadata trùng lặp không bị loại bỏ::

      assert Annotated[int, ValueRange(3, 10)] != Annotated[
          int, ValueRange(3, 10), ValueRange(3, 10)
      ]

   ``Annotated`` có thể được sử dụng với các alias lồng nhau và alias generic:

     .. testcode::

        @dataclass
        class MaxLen:
            value: int

        type Vec[T] = Annotated[list[tuple[T, T]], MaxLen(10)]

        # Khi được sử dụng trong chú thích kiểu, trình kiểm tra kiểu sẽ coi "V" giống như
        # ``Annotated[list[tuple[int, int]], MaxLen(10)]``:
        type V = Vec[int]

   Không thể sử dụng ``Annotated`` với :class:`TypeVarTuple` đã được unpack::

        type Variadic[*Ts] = Annotated[*Ts, Ann1] = Annotated[T1, T2, T3, ..., Ann1]  # KHÔNG hợp lệ

   trong đó ``T1``, ``T2``, ... là :class:`TypeVars <TypeVar>`. Điều này không hợp lệ vì chỉ nên truyền một kiểu vào Annotated.

   Theo mặc định, :func:`get_type_hints` loại bỏ metadata khỏi các chú thích. Truyền ``include_extras=True`` để giữ lại metadata:

     .. doctest::

        >>> from typing import Annotated, get_type_hints
        >>> def func(x: Annotated[int, "metadata"]) -> None: pass
        ...
        >>> get_type_hints(func)
        {'x': <class 'int'>, 'return': <class 'NoneType'>}
        >>> get_type_hints(func, include_extras=True)
        {'x': typing.Annotated[int, 'metadata'], 'return': <class 'NoneType'>}

   Trong runtime, bạn có thể truy xuất siêu dữ liệu liên kết với một kiểu ``Annotated`` thông qua thuộc tính :attr:`!__metadata__`:‌

     .. doctest::

        >>> from typing import Annotated
        >>> X = Annotated[int, "very", "important", "metadata"]
        >>> X
        typing.Annotated[int, 'very', 'important', 'metadata']
        >>> X.__metadata__
        ('very', 'important', 'metadata')

   Nếu muốn truy xuất kiểu ban đầu được bọc bởi ``Annotated``, hãy sử dụng
   thuộc tính :attr:`!__origin__`:‌

     .. doctest::

        >>> from typing import Annotated, get_origin
        >>> Password = Annotated[str, "secret"]
        >>> Password.__origin__
        <class 'str'>

   Lưu ý rằng việc sử dụng :func:`get_origin` sẽ trả về chính ``Annotated``:‌

     .. doctest::

        >>> get_origin(Password)
        typing.Annotated

   .. seealso::

      :pep:`593` - Chú thích linh hoạt cho hàm và biến
         PEP giới thiệu ``Annotated`` vào thư viện chuẩn.

   .. versionadded:: 3.9


.. data:: TypeIs

   Cấu trúc typing đặc biệt dùng để đánh dấu các hàm predicate kiểu do người dùng định nghĩa.

   ``TypeIs`` có thể được dùng để chú thích kiểu trả về của một hàm type predicate do người dùng định nghĩa. ``TypeIs`` chỉ chấp nhận một đối số kiểu duy nhất. Khi chạy, các hàm được đánh dấu theo cách này phải trả về một giá trị boolean và nhận ít nhất một đối số vị trí.

   ``TypeIs`` hướng đến việc hỗ trợ *thu hẹp kiểu* -- một kỹ thuật được các trình kiểm tra kiểu tĩnh sử dụng để xác định kiểu chính xác hơn của một biểu thức trong luồng mã của chương trình. Thông thường, việc thu hẹp kiểu được thực hiện bằng cách phân tích luồng mã điều kiện và áp dụng việc thu hẹp cho một khối mã. Biểu thức điều kiện ở đây đôi khi được gọi là "type predicate"::

      def is_str(val: str | float):
          # "isinstance" type predicate
          if isinstance(val, str):
              # Kiểu của ``val`` được thu hẹp thành ``str``
              ...
          else:
              # Else, type of ``val`` is narrowed to ``float``.
              ...

   Đôi khi sẽ rất tiện lợi nếu có thể dùng một hàm boolean do người dùng định nghĩa làm type predicate. Hàm như vậy nên dùng ``TypeIs[...]`` hoặc
   :data:`TypeGuard` làm kiểu trả về để thông báo cho các trình kiểm tra kiểu tĩnh về ý định này. ``TypeIs`` thường có hành vi trực quan hơn ``TypeGuard``, nhưng không thể dùng khi kiểu đầu vào và kiểu đầu ra không tương thích (ví dụ: từ ``list[object]`` đến ``list[int]``) hoặc khi hàm không trả về ``True`` cho mọi thực thể thuộc kiểu đã được thu hẹp.

   Việc sử dụng ``-> TypeIs[NarrowedType]`` cho trình kiểm tra kiểu tĩnh biết rằng đối với một hàm nhất định:

   1. Giá trị trả về là một boolean.
   2. Nếu giá trị trả về là ``True``, kiểu của đối số là phép giao giữa kiểu ban đầu của đối số và ``NarrowedType``.
   3. Nếu giá trị trả về là ``False``, kiểu của đối số được thu hẹp để loại trừ ``NarrowedType``.

   Ví dụ::

        from typing import assert_type, final, TypeIs

        class Parent: pass
        class Child(Parent): pass
        @final
        class Unrelated: pass

        def is_parent(val: object) -> TypeIs[Parent]:
            return isinstance(val, Parent)

        def run(arg: Child | Unrelated):
            if is_parent(arg):
                # Kiểu của ``arg`` được thu hẹp thành phép giao
                # của ``Parent`` và ``Child``, tương đương với
                # ``Child``.
                assert_type(arg, Child)
            else:
                # Kiểu của ``arg`` được thu hẹp để loại trừ ``Parent``,
                # vì vậy chỉ còn ``Unrelated``.
                assert_type(arg, Unrelated)

   Kiểu bên trong ``TypeIs`` phải nhất quán với kiểu của đối số của hàm; nếu không, các trình kiểm tra kiểu tĩnh sẽ báo lỗi. Một hàm ``TypeIs`` được viết không chính xác có thể dẫn đến hành vi không an toàn trong hệ thống kiểu; người dùng có trách nhiệm viết các hàm như vậy theo cách an toàn về kiểu.

   Nếu một hàm ``TypeIs`` là một phương thức lớp hoặc phương thức instance, thì kiểu trong ``TypeIs`` ánh xạ tới kiểu của tham số thứ hai (sau ``cls`` hoặc ``self``).

   Tóm lại, dạng ``def foo(arg: TypeA) -> TypeIs[TypeB]: ...`` có nghĩa là nếu ``foo(arg)`` trả về ``True``, thì ``arg`` là một instance của ``TypeB``, còn nếu nó trả về ``False``, thì nó không phải là một instance của ``TypeB``.

   ``TypeIs`` cũng hoạt động với các biến kiểu. Để biết thêm thông tin, hãy xem
   :pep:`742` (Thu hẹp kiểu bằng ``TypeIs``).

   .. versionadded:: 3.13


.. data:: TypeGuard

   Cấu trúc typing đặc biệt dùng để đánh dấu các hàm predicate kiểu do người dùng định nghĩa.

   Các hàm predicate kiểu là những hàm do người dùng định nghĩa, trả về thông tin cho biết đối số của chúng có phải là một instance của một kiểu cụ thể hay không. ``TypeGuard`` hoạt động tương tự như :data:`TypeIs`, nhưng có tác động hơi khác đến hành vi kiểm tra kiểu (xem bên dưới).

   Việc sử dụng ``-> TypeGuard`` cho trình kiểm tra kiểu tĩnh biết rằng, đối với một hàm nhất định:

   1. Giá trị trả về là một boolean.
   2. Nếu giá trị trả về là ``True``, kiểu của đối số của hàm là kiểu nằm trong ``TypeGuard``.

   ``TypeGuard`` cũng hoạt động với các biến kiểu. Xem :pep:`647` để biết thêm chi tiết.

   Ví dụ::

         def is_str_list(val: list[object]) -> TypeGuard[list[str]]:
             '''Determines whether all objects in the list are strings'''
             return all(isinstance(x, str) for x in val)

         def func1(val: list[object]):
             if is_str_list(val):
                 # Kiểu của ``val`` được thu hẹp thành ``list[str]``.
                 print(" ".join(val))
             else:
                 # Kiểu của ``val`` vẫn là ``list[object]``.
                 print("Not a list of strings!")

   ``TypeIs`` và ``TypeGuard`` khác nhau ở những điểm sau:

   * ``TypeIs`` yêu cầu kiểu đã thu hẹp phải là subtype của kiểu đầu vào, còn ``TypeGuard`` thì không. Lý do chính là cho phép những thao tác như thu hẹp ``list[object]`` thành ``list[str]`` dù kiểu sau không phải là subtype của kiểu trước, vì ``list`` là bất biến.
   * Khi một hàm ``TypeGuard`` trả về ``True``, type checker sẽ thu hẹp kiểu của biến thành đúng kiểu ``TypeGuard``. Khi một hàm ``TypeIs`` trả về ``True``, type checker có thể suy luận một kiểu chính xác hơn bằng cách kết hợp kiểu đã biết trước đó của biến với kiểu ``TypeIs``. (Về mặt kỹ thuật, đây được gọi là kiểu giao.)
   * Khi một hàm ``TypeGuard`` trả về ``False``, type checker hoàn toàn không thể thu hẹp kiểu của biến. Khi một hàm ``TypeIs`` trả về ``False``, type checker có thể thu hẹp kiểu của biến để loại trừ kiểu ``TypeIs``.

   .. versionadded:: 3.10


.. data:: Unpack

   Toán tử typing dùng để biểu thị về mặt khái niệm rằng một đối tượng đã được unpack.

   Ví dụ: sử dụng toán tử unpack ``*`` trên một
   :ref:`tuple biến kiểu <typevartuple>` tương đương với việc sử dụng ``Unpack`` để đánh dấu tuple biến kiểu đã được unpack::

      Ts = TypeVarTuple('Ts')
      tup: tuple[*Ts]
      # Thực chất là:
      tup: tuple[Unpack[Ts]]

   Thực tế, ``Unpack`` có thể được sử dụng thay thế cho ``*`` trong ngữ cảnh của :class:`typing.TypeVarTuple <TypeVarTuple>` và
   :class:`builtins.tuple <tuple>` các kiểu. Bạn có thể thấy ``Unpack`` được sử dụng tường minh trong các phiên bản Python cũ hơn, khi ``*`` không thể được sử dụng ở một số vị trí nhất định::

      # Trong các phiên bản Python cũ hơn, TypeVarTuple và Unpack
      # nằm trong package `typing_extensions` backports.
      from typing_extensions import TypeVarTuple, Unpack

      Ts = TypeVarTuple('Ts')
      tup: tuple[*Ts]         # Lỗi cú pháp trên Python <= 3.10!
      tup: tuple[Unpack[Ts]]  # Tương đương về ngữ nghĩa và tương thích ngược

   ``Unpack`` cũng có thể được sử dụng cùng với :class:`typing.TypedDict` để định kiểu ``**kwargs`` trong chữ ký hàm::

      from typing import TypedDict, Unpack

      class Movie(TypedDict):
          name: str
          year: int

      # Hàm này yêu cầu hai đối số keyword - `name` có kiểu `str`
      # và `year` có kiểu `int`.
      def foo(**kwargs: Unpack[Movie]): ...

   Xem :pep:`692` để biết thêm chi tiết về cách sử dụng ``Unpack`` cho việc định kiểu ``**kwargs``.

   .. versionadded:: 3.11

Xây dựng các kiểu generic và bí danh kiểu
"""""""""""""""""""""""""""""""""""""""""

Không nên sử dụng trực tiếp các lớp sau làm chú thích kiểu. Mục đích của chúng là làm các khối xây dựng để tạo các kiểu generic và bí danh kiểu.

Các đối tượng này có thể được tạo bằng cú pháp đặc biệt (danh sách :ref:`tham số kiểu <type-params>` và :keyword:`type` câu lệnh). Để tương thích với Python 3.11 trở về trước, chúng cũng có thể được tạo mà không cần cú pháp chuyên dụng, như được trình bày bên dưới.

.. class:: Generic

   Lớp cơ sở trừu tượng dành cho các kiểu generic.

   Một kiểu generic thường được khai báo bằng cách thêm danh sách tham số kiểu sau tên lớp::

      class Mapping[KT, VT]:
          def __getitem__(self, key: KT) -> VT:
              ...
              # V.v.

   Một lớp như vậy ngầm kế thừa từ ``Generic``. Ngữ nghĩa runtime của cú pháp này được thảo luận trong
   :ref:`Tài liệu tham khảo ngôn ngữ <generic-classes>`.

   Sau đó, lớp này có thể được sử dụng như sau::

      def lookup_name[X, Y](mapping: Mapping[X, Y], key: X, default: Y) -> Y:
          try:
              return mapping[key]
          except KeyError:
              return default

   Ở đây, dấu ngoặc sau tên hàm cho biết đây là một
   :ref:`hàm generic <generic-functions>`.

   Để đảm bảo khả năng tương thích ngược, các lớp generic cũng có thể được khai báo bằng cách kế thừa rõ ràng từ ``Generic``. Trong trường hợp này, các tham số kiểu phải được khai báo riêng::

      KT = TypeVar('KT')
      VT = TypeVar('VT')

      class Mapping(Generic[KT, VT]):
          def __getitem__(self, key: KT) -> VT:
              ...
              # V.v.

.. _typevar:

.. class:: TypeVar(name, *constraints, bound=None, covariant=False, contravariant=False, infer_variance=False, default=typing.NoDefault)

   Biến kiểu.

   Cách ưu tiên để tạo một biến kiểu là sử dụng cú pháp chuyên dụng cho :ref:`hàm generic <generic-functions>`,
   :ref:`lớp generic <generic-classes>`, và
   :ref:`bí danh kiểu generic <generic-type-aliases>`::

      class Sequence[T]:  # T là một TypeVar
          ...

   Cú pháp này cũng có thể được dùng để tạo các biến kiểu có giới hạn và có ràng buộc::

      class StrSequence[S: str]:  # S là một TypeVar có `str` làm upper bound;
          ...                     # ta có thể nói rằng S "bị giới hạn bởi `str`"


      class StrOrBytesSequence[A: (str, bytes)]:  # A là một TypeVar bị ràng buộc vào str hoặc bytes
          ...

   Tuy nhiên, nếu muốn, bạn cũng có thể tạo thủ công các biến kiểu có thể tái sử dụng như sau::

      T = TypeVar('T')  # Có thể là bất kỳ kiểu nào
      S = TypeVar('S', bound=str)  # Có thể là bất kỳ kiểu con nào của str
      A = TypeVar('A', str, bytes)  # Phải chính xác là str hoặc bytes

   Các biến kiểu chủ yếu tồn tại để phục vụ các static type checker. Chúng đóng vai trò là các tham số cho generic type, cũng như cho các định nghĩa generic function và type alias. Xem :class:`Generic` để biết thêm thông tin về generic type. Generic function hoạt động như sau::

      def repeat[T](x: T, n: int) -> Sequence[T]:
          """Return a list containing n references to x."""
          return [x]*n


      def print_capitalized[S: str](x: S) -> S:
          """Print x capitalized, and return x."""
          print(x.capitalize())
          return x


      def concatenate[A: (str, bytes)](x: A, y: A) -> A:
          """Add two strings or bytes objects together."""
          return x + y

   Lưu ý rằng các biến kiểu có thể được *giới hạn*, *ràng buộc*, hoặc không thuộc cả hai loại, nhưng không thể vừa được giới hạn *vừa* bị ràng buộc.

   Variance của các biến kiểu được type checker suy ra khi chúng được tạo thông qua :ref:`cú pháp type parameter <type-params>` hoặc khi ``infer_variance=True`` được truyền vào. Các biến kiểu được tạo thủ công có thể được đánh dấu rõ ràng là covariant hoặc contravariant bằng cách truyền ``covariant=True`` hoặc ``contravariant=True``. Theo mặc định, các biến kiểu được tạo thủ công là invariant. Xem :pep:`484` và :pep:`695` để biết thêm chi tiết.

   Các biến kiểu bị giới hạn và các biến kiểu bị ràng buộc có ngữ nghĩa khác nhau theo một số cách quan trọng. Việc sử dụng một biến kiểu *bị giới hạn* có nghĩa là ``TypeVar`` sẽ được xác định bằng kiểu cụ thể nhất có thể::

      x = print_capitalized('a string')
      reveal_type(x)  # kiểu được suy luận là str

      class StringSubclass(str):
          pass

      y = print_capitalized(StringSubclass('another string'))
      reveal_type(y)  # kiểu được suy luận là StringSubclass

      z = print_capitalized(45)  # lỗi: int không phải là kiểu con của str

   Giới hạn trên của một biến kiểu có thể là một kiểu cụ thể, kiểu trừu tượng (ABC hoặc Protocol), hoặc thậm chí là một union các kiểu::

      # Có thể là bất kỳ đối tượng nào có phương thức __abs__
      def print_abs[T: SupportsAbs](arg: T) -> None:
          print("Absolute value:", abs(arg))

      U = TypeVar('U', bound=str|bytes)  # Có thể là bất kỳ kiểu con nào của union str|bytes
      V = TypeVar('V', bound=SupportsAbs)  # Có thể là bất kỳ đối tượng nào có phương thức __abs__

   .. _typing-constrained-typevar:

   Tuy nhiên, việc sử dụng biến kiểu *constrained* có nghĩa là ``TypeVar`` chỉ có thể được giải quyết chính xác thành một trong các ràng buộc đã cho::

      a = concatenate('one', 'two')
      reveal_type(a)  # kiểu được suy luận là str

      b = concatenate(StringSubclass('one'), StringSubclass('two'))
      reveal_type(b)  # kiểu được tiết lộ là str, mặc dù StringSubclass được truyền vào

      c = concatenate('one', b'two')  # lỗi: biến kiểu 'A' có thể là str hoặc bytes trong một lần gọi hàm, nhưng không thể là cả hai

   Trong runtime, ``isinstance(x, T)`` sẽ raise :exc:`TypeError`.

   .. attribute:: __name__

      Tên của biến kiểu.

   .. attribute:: __covariant__

      Biến kiểu có được đánh dấu rõ ràng là covariant hay không.

   .. attribute:: __contravariant__

      Liệu type var có được đánh dấu rõ ràng là contravariant hay không.

   .. attribute:: __infer_variance__

      Liệu variance của type variable có nên được trình kiểm tra kiểu suy luận hay không.

      .. versionadded:: 3.12

   .. attribute:: __bound__

      Cận trên của type variable, nếu có.

      .. versionchanged:: 3.12

         Đối với các type variable được tạo thông qua cú pháp :ref:`type parameter syntax <type-params>`, bound chỉ được đánh giá khi thuộc tính được truy cập, không phải khi type variable được tạo (xem :ref:`lazy-evaluation`).

   .. method:: evaluate_bound

      Một :term:`evaluate function` tương ứng với thuộc tính :attr:`~TypeVar.__bound__`. Khi được gọi trực tiếp, phương thức này chỉ hỗ trợ định dạng :attr:`~annotationlib.Format.VALUE`, tương đương với việc truy cập trực tiếp thuộc tính :attr:`~TypeVar.__bound__`, nhưng đối tượng phương thức có thể được truyền vào :func:`annotationlib.call_evaluate_function` để đánh giá giá trị theo một định dạng khác.

      .. versionadded:: 3.14

   .. attribute:: __constraints__

      Một tuple chứa các ràng buộc của type variable, nếu có.

      .. versionchanged:: 3.12

         Đối với các type variable được tạo thông qua cú pháp :ref:`type parameter syntax <type-params>`, các ràng buộc chỉ được đánh giá khi thuộc tính được truy cập, không phải khi type variable được tạo (xem :ref:`lazy-evaluation`).

   .. method:: evaluate_constraints

      Một :term:`evaluate function` tương ứng với thuộc tính :attr:`~TypeVar.__constraints__`. Khi được gọi trực tiếp, phương thức này chỉ hỗ trợ định dạng :attr:`~annotationlib.Format.VALUE`, tương đương với việc truy cập trực tiếp thuộc tính :attr:`~TypeVar.__constraints__`, nhưng đối tượng phương thức có thể được truyền cho :func:`annotationlib.call_evaluate_function` để đánh giá giá trị ở một định dạng khác.

      .. versionadded:: 3.14

   .. attribute:: __default__

      Giá trị mặc định của biến kiểu, hoặc :data:`typing.NoDefault` nếu biến không có giá trị mặc định.

      .. versionadded:: 3.13

   .. method:: evaluate_default

      Một :term:`evaluate function` tương ứng với thuộc tính :attr:`~TypeVar.__default__`. Khi được gọi trực tiếp, phương thức này chỉ hỗ trợ định dạng :attr:`~annotationlib.Format.VALUE`, tương đương với việc truy cập trực tiếp thuộc tính :attr:`~TypeVar.__default__`, nhưng đối tượng phương thức có thể được truyền cho :func:`annotationlib.call_evaluate_function` để đánh giá giá trị ở một định dạng khác.

      .. versionadded:: 3.14

   .. method:: has_default()

      Trả về việc biến kiểu có giá trị mặc định hay không. Điều này tương đương với việc kiểm tra xem :attr:`__default__` có khác singleton :data:`typing.NoDefault` hay không, ngoại trừ việc không buộc đánh giá
      :ref:`giá trị mặc định được đánh giá trì hoãn <lazy-evaluation>`.

      .. versionadded:: 3.13

   .. versionchanged:: 3.12

      Giờ đây, có thể khai báo biến kiểu bằng
      :ref:`cú pháp tham số kiểu <type-params>` được giới thiệu bởi :pep:`695`. Tham số ``infer_variance`` đã được thêm vào.

   .. versionchanged:: 3.13

      Đã bổ sung hỗ trợ cho các giá trị mặc định.

.. _typevartuple:

.. class:: TypeVarTuple(name, *, default=typing.NoDefault)

   Tuple biến kiểu. Một dạng chuyên biệt của :ref:`biến kiểu <typevar>`, cho phép tạo các generic *biến thiên*.

   Có thể khai báo tuple biến kiểu trong :ref:`danh sách tham số kiểu <type-params>` bằng một dấu hoa thị đơn (``*``) trước tên::

      def move_first_element_to_last[T, *Ts](tup: tuple[T, *Ts]) -> tuple[*Ts, T]:
          return (*tup[1:], tup[0])

   Hoặc bằng cách gọi rõ ràng ``TypeVarTuple`` hàm khởi tạo::

      T = TypeVar("T")
      Ts = TypeVarTuple("Ts")

      def move_first_element_to_last(tup: tuple[T, *Ts]) -> tuple[*Ts, T]:
          return (*tup[1:], tup[0])

   Một biến kiểu thông thường cho phép tham số hóa với một kiểu duy nhất. Ngược lại, tuple biến kiểu cho phép tham số hóa với một *bất kỳ* số kiểu bằng cách hoạt động như một *bất kỳ* số biến kiểu được bọc trong một tuple. Ví dụ::

      # T được gắn với int, Ts được gắn với ()
      # Giá trị trả về là (1,), có kiểu tuple[int]
      move_first_element_to_last(tup=(1,))

      # T được ràng buộc với int, Ts được ràng buộc với (str,)
      # Giá trị trả về là ('spam', 1), có kiểu tuple[str, int]
      move_first_element_to_last(tup=(1, 'spam'))

      # T được ràng buộc với int, Ts được ràng buộc với (str, float)
      # Giá trị trả về là ('spam', 3.0, 1), có kiểu tuple[str, float, int]
      move_first_element_to_last(tup=(1, 'spam', 3.0))

      # Lệnh này không vượt qua bước kiểm tra kiểu (và sẽ lỗi khi chạy)
      # vì tuple[()] không tương thích với tuple[T, *Ts]
      # (cần ít nhất một phần tử)
      move_first_element_to_last(tup=())

   Lưu ý việc sử dụng toán tử unpacking ``*`` trong ``tuple[T, *Ts]``. Về mặt khái niệm, bạn có thể xem ``Ts`` là một tuple gồm các biến kiểu ``(T1, T2, ...)``. Khi đó, ``tuple[T, *Ts]`` sẽ trở thành ``tuple[T, *(T1, T2, ...)]``, tương đương với ``tuple[T, T1, T2, ...]``. (Lưu ý rằng trong các phiên bản Python cũ hơn, bạn có thể thấy cách viết này sử dụng :data:`Unpack <Unpack>` thay thế, như trong ``Unpack[Ts]``.)

   Các tuple biến kiểu phải *luôn luôn* được unpack. Điều này giúp phân biệt tuple biến kiểu với các biến kiểu thông thường::

      x: Ts          # Không hợp lệ
      x: tuple[Ts]   # Không hợp lệ
      x: tuple[*Ts]  # Cách thực hiện đúng

   Tuple biến kiểu có thể được sử dụng trong các ngữ cảnh giống như biến kiểu thông thường. Ví dụ: trong định nghĩa lớp, các đối số và kiểu trả về::

      class Array[*Shape]:
          def __getitem__(self, key: tuple[*Shape]) -> float: ...
          def __abs__(self) -> "Array[*Shape]": ...
          def get_shape(self) -> tuple[*Shape]: ...

   Tuple biến kiểu có thể dễ dàng kết hợp với các biến kiểu thông thường:

   .. testcode::

      class Array[DType, *Shape]:  # Điều này ổn
          pass

      class Array2[*Shape, DType]:  # Cách này cũng ổn
          pass

      class Height: ...
      class Width: ...

      float_array_1d: Array[float, Height] = Array()     # Hoàn toàn ổn
      int_array_2d: Array[int, Height, Width] = Array()  # Ừ, cách này cũng ổn

   Tuy nhiên, lưu ý rằng trong một danh sách các đối số kiểu hoặc tham số kiểu, chỉ có thể xuất hiện nhiều nhất một type variable tuple::

      x: tuple[*Ts, *Ts]            # Không hợp lệ
      class Array[*Shape, *Shape]:  # Không hợp lệ
          pass

   Cuối cùng, một tuple biến kiểu chưa được unpack có thể được dùng làm chú thích kiểu của ``*args``::

      def call_soon[*Ts](
          callback: Callable[[*Ts], None],
          *args: *Ts
      ) -> None:
          ...
          callback(*args)

   Khác với các chú thích không unpack của ``*args`` - chẳng hạn như ``*args: int``, trong đó chỉ định rằng *all* đối số đều là ``int`` - ``*args: *Ts`` cho phép tham chiếu đến kiểu của các đối số *individual* trong ``*args``. Ở đây, điều này cho phép chúng ta đảm bảo kiểu của ``*args`` được truyền vào ``call_soon`` khớp với kiểu của các đối số (vị trí) của ``callback``.

   Xem :pep:`646` để biết thêm chi tiết về các tuple biến kiểu.

   .. attribute:: __name__

      Tên của tuple biến kiểu.

   .. attribute:: __default__

      Giá trị mặc định của tuple biến kiểu, hoặc :data:`typing.NoDefault` nếu tuple không có giá trị mặc định.

      .. versionadded:: 3.13

   .. method:: evaluate_default

      Một :term:`evaluate function` tương ứng với thuộc tính :attr:`~TypeVarTuple.__default__`. Khi được gọi trực tiếp, phương thức này chỉ hỗ trợ định dạng :attr:`~annotationlib.Format.VALUE`, tương đương với việc truy cập trực tiếp thuộc tính :attr:`~TypeVarTuple.__default__`, nhưng đối tượng phương thức có thể được truyền vào :func:`annotationlib.call_evaluate_function` để đánh giá giá trị ở một định dạng khác.

      .. versionadded:: 3.14

   .. method:: has_default()

      Trả về việc tuple biến kiểu có giá trị mặc định hay không. Điều này tương đương với việc kiểm tra xem :attr:`__default__` không phải là singleton :data:`typing.NoDefault`, ngoại trừ việc không buộc đánh giá
      :ref:`giá trị mặc định được đánh giá trì hoãn <lazy-evaluation>`.

      .. versionadded:: 3.13

   .. versionadded:: 3.11

   .. versionchanged:: 3.12

      Các tuple biến kiểu giờ đây có thể được khai báo bằng
      :ref:`cú pháp tham số kiểu <type-params>` được giới thiệu bởi :pep:`695`.

   .. versionchanged:: 3.13

      Đã bổ sung hỗ trợ cho các giá trị mặc định.

.. class:: ParamSpec(name, *, bound=None, covariant=False, contravariant=False, infer_variance=False, default=typing.NoDefault)

   Biến đặc tả tham số. Một phiên bản chuyên biệt của
   :ref:`biến kiểu <typevar>`.

   Trong :ref:`danh sách tham số kiểu <type-params>`, các đặc tả tham số có thể được khai báo bằng hai dấu hoa thị (``**``)::

      type IntFunc[**P] = Callable[P, int]

   Để tương thích với Python 3.11 và các phiên bản cũ hơn, các đối tượng ``ParamSpec`` cũng có thể được tạo như sau::

      P = ParamSpec('P')

   Các biến đặc tả tham số chủ yếu tồn tại để phục vụ các trình kiểm tra kiểu tĩnh. Chúng được dùng để chuyển tiếp các kiểu tham số của một callable này sang một callable khác -- một mẫu thường thấy trong các hàm bậc cao và decorator. Chúng chỉ hợp lệ khi được dùng trong ``Concatenate``, hoặc làm đối số đầu tiên cho ``Callable``, hoặc làm tham số cho các Generics do người dùng định nghĩa. Xem :class:`Generic` để biết thêm thông tin về các kiểu generic.

   Ví dụ, để thêm tính năng ghi nhật ký cơ bản vào một hàm, ta có thể tạo một decorator ``add_logging`` để ghi nhật ký các lần gọi hàm. Biến đặc tả tham số cho trình kiểm tra kiểu biết rằng callable được truyền vào decorator và callable mới do nó trả về có các tham số kiểu phụ thuộc lẫn nhau::

      from collections.abc import Callable
      import logging

      def add_logging[T, **P](f: Callable[P, T]) -> Callable[P, T]:
          '''A type-safe decorator to add logging to a function.'''
          def inner(*args: P.args, **kwargs: P.kwargs) -> T:
              logging.info(f'{f.__name__} was called')
              return f(*args, **kwargs)
          return inner

      @add_logging
      def add_two(x: float, y: float) -> float:
          '''Add two numbers together.'''
          return x + y

   Nếu không có ``ParamSpec``, trước đây cách đơn giản nhất để chú thích trường hợp này là sử dụng một :class:`TypeVar` với giới hạn trên là ``Callable[..., Any]``. Tuy nhiên, cách này gây ra hai vấn đề:

   1. Trình kiểm tra kiểu không thể kiểm tra kiểu của hàm ``inner`` vì ``*args`` và ``**kwargs`` phải được định kiểu là :data:`Any`.
   2. Có thể cần :func:`~cast` trong phần thân của decorator ``add_logging`` khi trả về hàm ``inner``, hoặc phải yêu cầu trình kiểm tra kiểu tĩnh bỏ qua ``return inner``.

   .. attribute:: args
   .. attribute:: kwargs

      Vì ``ParamSpec`` nắm bắt cả tham số vị trí và tham số từ khóa, có thể dùng ``P.args`` và ``P.kwargs`` để tách một ``ParamSpec`` thành các thành phần của nó. ``P.args`` biểu diễn tuple gồm các tham số vị trí trong một lời gọi cụ thể và chỉ nên được dùng để chú thích ``*args``. ``P.kwargs`` biểu diễn ánh xạ từ các tham số từ khóa đến giá trị của chúng trong một lời gọi cụ thể và chỉ nên được dùng để chú thích ``**kwargs``. Cả hai thuộc tính đều yêu cầu tham số được chú thích phải nằm trong phạm vi. Tại thời điểm chạy, ``P.args`` và ``P.kwargs`` lần lượt là các thực thể của
      :class:`ParamSpecArgs` và :class:`ParamSpecKwargs`.

   .. attribute:: __name__

      Tên của đặc tả tham số.

   .. attribute:: __default__

      Giá trị mặc định của đặc tả tham số, hoặc :data:`typing.NoDefault` nếu không có giá trị mặc định.

      .. versionadded:: 3.13

   .. method:: evaluate_default

      Một :term:`evaluate function` tương ứng với thuộc tính :attr:`~ParamSpec.__default__`. Khi được gọi trực tiếp, phương thức này chỉ hỗ trợ định dạng :attr:`~annotationlib.Format.VALUE`, tương đương với việc truy cập trực tiếp thuộc tính :attr:`~ParamSpec.__default__`, nhưng đối tượng phương thức có thể được truyền vào :func:`annotationlib.call_evaluate_function` để đánh giá giá trị theo một định dạng khác.

      .. versionadded:: 3.14

   .. method:: has_default()

      Trả về việc đặc tả tham số có giá trị mặc định hay không. Điều này tương đương với việc kiểm tra xem :attr:`__default__` không phải là singleton :data:`typing.NoDefault`, ngoại trừ việc nó không buộc đánh giá
      :ref:`giá trị mặc định được đánh giá trì hoãn <lazy-evaluation>`.

      .. versionadded:: 3.13

   Các biến đặc tả tham số được tạo bằng ``covariant=True`` hoặc ``contravariant=True`` có thể được dùng để khai báo các kiểu generic đồng biến hoặc phản biến. Đối số ``bound`` cũng được chấp nhận, tương tự như
   :class:`TypeVar`. Tuy nhiên, ngữ nghĩa thực tế của các từ khóa này vẫn chưa được quyết định.

   .. versionadded:: 3.10

   .. versionchanged:: 3.12

      Giờ đây, các đặc tả tham số có thể được khai báo bằng
      :ref:`cú pháp tham số kiểu <type-params>` được giới thiệu bởi :pep:`695`.

   .. versionchanged:: 3.13

      Đã bổ sung hỗ trợ cho các giá trị mặc định.

   .. note::
      Chỉ các biến đặc tả tham số được định nghĩa trong phạm vi toàn cục mới có thể được pickle.

   .. seealso::
      * :pep:`612` -- Các biến đặc tả tham số (PEP đã giới thiệu ``ParamSpec`` và ``Concatenate``)
      * :data:`Concatenate`
      * :ref:`annotating-callables`

.. class:: ParamSpecArgs
           ParamSpecKwargs

   Các thuộc tính arguments và keyword arguments của một :class:`ParamSpec`. Thuộc tính ``P.args`` của một ``ParamSpec`` là một thể hiện của ``ParamSpecArgs``, còn ``P.kwargs`` là một thể hiện của ``ParamSpecKwargs``. Chúng được dùng để kiểm tra nội tại runtime và không có ý nghĩa đặc biệt đối với các trình kiểm tra kiểu tĩnh.

   Gọi :func:`get_origin` trên một trong hai đối tượng này sẽ trả về ``ParamSpec`` ban đầu:

   .. doctest::

      >>> from typing import ParamSpec, get_origin
      >>> P = ParamSpec("P")
      >>> get_origin(P.args) is P
      True
      >>> get_origin(P.kwargs) is P
      True

   .. versionadded:: 3.10


.. class:: TypeAliasType(name, value, *, type_params=())

   Kiểu của các bí danh kiểu được tạo thông qua câu lệnh :keyword:`type`.

   Ví dụ:

   .. doctest::

      >>> type Alias = int
      >>> type(Alias)
      <class 'typing.TypeAliasType'>

   .. versionadded:: 3.12

   .. attribute:: __name__

      Tên của bí danh kiểu:

      .. doctest::

         >>> type Alias = int
         >>> Alias.__name__
         'Alias'

   .. attribute:: __module__

      Tên của module nơi bí danh kiểu được định nghĩa::

         >>> type Alias = int
         >>> Alias.__module__
         '__main__'

   .. attribute:: __type_params__

      Các tham số kiểu của bí danh kiểu hoặc một tuple rỗng nếu bí danh không phải là generic:

      .. doctest::

         >>> type ListOrSet[T] = list[T] | set[T]
         >>> ListOrSet.__type_params__
         (T,)
         >>> type NotGeneric = int
         >>> NotGeneric.__type_params__
         ()

   .. attribute:: __value__

      Giá trị của bí danh kiểu. Giá trị này được :ref:`đánh giá lười <lazy-evaluation>`, vì vậy các tên được sử dụng trong định nghĩa bí danh sẽ không được phân giải cho đến khi thuộc tính ``__value__`` được truy cập:

      .. doctest::

         >>> type Mutually = Recursive
         >>> type Recursive = Mutually
         >>> Mutually
         Mutually
         >>> Recursive
         Recursive
         >>> Mutually.__value__
         Recursive
         >>> Recursive.__value__
         Mutually

   .. method:: evaluate_value

      Một :term:`evaluate function` tương ứng với thuộc tính :attr:`__value__`. Khi được gọi trực tiếp, phương thức này chỉ hỗ trợ định dạng :attr:`~annotationlib.Format.VALUE`, tương đương với việc truy cập trực tiếp thuộc tính :attr:`__value__`, nhưng đối tượng phương thức có thể được truyền cho :func:`annotationlib.call_evaluate_function` để đánh giá giá trị theo một định dạng khác:

      .. doctest::

         >>> type Alias = undefined
         >>> Alias.__value__
         Traceback (most recent call last):
         ...
         NameError: name 'undefined' is not defined
         >>> from annotationlib import Format, call_evaluate_function
         >>> Alias.evaluate_value(Format.VALUE)
         Traceback (most recent call last):
         ...
         NameError: name 'undefined' is not defined
         >>> call_evaluate_function(Alias.evaluate_value, Format.FORWARDREF)
         ForwardRef('undefined')

      .. versionadded:: 3.14

   .. rubric:: Giải nén

   Bí danh kiểu hỗ trợ giải nén bằng dấu sao với cú pháp ``*Alias``. Điều này tương đương với việc sử dụng trực tiếp ``Unpack[Alias]``:

   .. doctest::

      >>> type Alias = tuple[int, str]
      >>> type Unpacked = tuple[bool, *Alias]
      >>> Unpacked.__value__
      tuple[bool, typing.Unpack[Alias]]

   .. versionadded:: 3.14


Các chỉ thị đặc biệt khác
"""""""""""""""""""""""""

Không nên sử dụng trực tiếp các hàm và lớp này làm chú thích. Mục đích của chúng là làm các khối xây dựng để tạo và khai báo kiểu.

.. class:: NamedTuple

   Phiên bản có kiểu của :func:`collections.namedtuple`.

   Cách sử dụng::

       class Employee(NamedTuple):
           name: str
           id: int

   Điều này tương đương với::

       Employee = collections.namedtuple('Employee', ['name', 'id'])

   Để cung cấp giá trị mặc định cho một field, bạn có thể gán giá trị đó cho field trong phần thân class::

      class Employee(NamedTuple):
          name: str
          id: int = 3

      employee = Employee('Guido')
      assert employee.id == 3

   Các field có giá trị mặc định phải đứng sau mọi field không có giá trị mặc định.

   Có thể lấy các kiểu của từng tên field bằng cách gọi
   :func:`annotationlib.get_annotations` trên class thu được. (Tên các field nằm trong thuộc tính ``_fields`` và các giá trị mặc định nằm trong thuộc tính ``_field_defaults``, cả hai đều thuộc API :func:`~collections.namedtuple`.)

   Các lớp con của ``NamedTuple`` cũng có thể có docstring và các method::

      class Employee(NamedTuple):
          """Represents an employee."""
          name: str
          id: int = 3

          def __repr__(self) -> str:
              return f'<Employee {self.name}, id={self.id}>'

   Các lớp con của ``NamedTuple`` có thể là generic::

      class Group[T](NamedTuple):
          key: T
          group: list[T]

   Cách sử dụng tương thích ngược::

       # Để tạo một NamedTuple generic trên Python 3.11
       T = TypeVar("T")

       class Group(NamedTuple, Generic[T]):
           key: T
           group: list[T]

       # Cú pháp hàm cũng được hỗ trợ
       Employee = NamedTuple('Employee', [('name', str), ('id', int)])

   .. versionchanged:: 3.6
      Đã bổ sung hỗ trợ cho cú pháp chú thích biến :pep:`526`.

   .. versionchanged:: 3.6.1
      Đã bổ sung hỗ trợ cho các giá trị mặc định, phương thức và docstring.

   .. versionchanged:: 3.8
      Các thuộc tính ``_field_types`` và ``__annotations__`` giờ đây là các dictionary thông thường thay vì các instance của ``OrderedDict``.

   .. versionchanged:: 3.9
      Đã loại bỏ thuộc tính ``_field_types`` để thay bằng thuộc tính ``__annotations__`` tiêu chuẩn hơn, vốn chứa cùng thông tin.

   .. versionchanged:: 3.9
      ``NamedTuple`` hiện là một function thay vì một class. Nó vẫn có thể được dùng làm class base, như mô tả ở trên.

   .. versionchanged:: 3.11
      Đã bổ sung hỗ trợ cho namedtuple tổng quát.

   .. versionchanged:: 3.14
      Việc sử dụng :func:`super` (và ``__class__`` :term:`closure variable`) trong các method của các subclass ``NamedTuple`` không được hỗ trợ và gây ra :class:`TypeError`.

   .. deprecated-removed:: 3.13 3.15
      Cú pháp đối số keyword không được ghi nhận để tạo các class NamedTuple (``NT = NamedTuple("NT", x=int)``) đã không còn được khuyến nghị và sẽ bị vô hiệu hóa trong 3.15. Thay vào đó, hãy sử dụng cú pháp dựa trên class hoặc cú pháp functional.

   .. deprecated-removed:: 3.13 3.15
      Khi sử dụng cú pháp functional để tạo một class NamedTuple, việc không truyền giá trị cho tham số 'fields' (``NT = NamedTuple("NT")``) đã không còn được khuyến nghị. Việc truyền ``None`` cho tham số 'fields' (``NT = NamedTuple("NT", None)``) cũng không còn được khuyến nghị. Cả hai cách này sẽ bị vô hiệu hóa trong Python 3.15. Để tạo một class NamedTuple có 0 field, hãy sử dụng ``class NT(NamedTuple): pass`` hoặc ``NT = NamedTuple("NT", [])``.

.. class:: NewType(name, tp)

   Lớp trợ giúp để tạo các kiểu :ref:`distinct có overhead thấp <distinct>`.

   ``NewType`` được trình kiểm tra kiểu xem là một kiểu riêng biệt. Tuy nhiên, trong runtime, việc gọi ``NewType`` sẽ trả về đối số của nó mà không thay đổi.

   Cách sử dụng::

      UserId = NewType('UserId', int)  # Khai báo NewType "UserId"
      first_user = UserId(1)  # "UserId" trả về đối số mà không thay đổi trong runtime

   .. attribute:: __module__

      Tên của module nơi kiểu mới được định nghĩa.

   .. attribute:: __name__

      Tên của kiểu mới.

   .. attribute:: __supertype__

      Kiểu mà kiểu mới dựa trên.

   .. versionadded:: 3.5.2

   .. versionchanged:: 3.10
      ``NewType`` hiện là một class thay vì một function.

.. class:: Protocol(Generic)

   Class cơ sở cho các class protocol.

   Các class protocol được định nghĩa như sau::

      class Proto(Protocol):
          def meth(self) -> int:
              ...

   Các class như vậy chủ yếu được dùng với các static type checker nhận diện structural subtyping (static duck-typing), chẳng hạn như::

      class C:
          def meth(self) -> int:
              return 0

      def func(x: Proto) -> int:
          return x.meth()

      func(C())  # Vượt qua kiểm tra kiểu tĩnh

   Xem :pep:`544` để biết thêm chi tiết. Các class protocol được trang trí bằng
   :deco:`runtime_checkable` (được mô tả ở phần sau) hoạt động như các protocol runtime đơn giản, chỉ kiểm tra sự hiện diện của các thuộc tính được chỉ định và bỏ qua chữ ký kiểu của chúng. Không thể dùng các class protocol không có decorator này làm đối số thứ hai của :func:`isinstance` hoặc :func:`issubclass`.

   Các lớp Protocol có thể là generic, ví dụ như::

      class GenProto[T](Protocol):
          def meth(self) -> T:
              ...

   Trong mã cần tương thích với Python 3.11 trở xuống, có thể viết các Protocol generic như sau::

      T = TypeVar("T")

      class GenProto(Protocol[T]):
          def meth(self) -> T:
              ...

   .. versionadded:: 3.8

.. decorator:: runtime_checkable

   Đánh dấu một lớp protocol là runtime protocol.

   Có thể sử dụng protocol như vậy với :func:`isinstance` và :func:`issubclass`. Điều này cho phép thực hiện một kiểm tra cấu trúc đơn giản, rất giống với các "one-trick ponies" trong :mod:`collections.abc` chẳng hạn như :class:`~collections.abc.Iterable`. Ví dụ::

      @runtime_checkable
      class Closable(Protocol):
          def close(self): ...

      assert isinstance(open('/some/file'), Closable)

      @runtime_checkable
      class Named(Protocol):
          name: str

      import threading
      assert isinstance(threading.Thread(name='Bob'), Named)

   Decorator này phát sinh :exc:`TypeError` khi được áp dụng cho một lớp không phải protocol.

   .. note::

        :deco:`!runtime_checkable` sẽ chỉ kiểm tra sự hiện diện của các phương thức hoặc thuộc tính bắt buộc, không kiểm tra chữ ký kiểu hoặc kiểu của chúng. Ví dụ, :class:`ssl.SSLObject` là một lớp, vì vậy nó vượt qua kiểm tra :func:`issubclass` đối với :ref:`Callable <annotating-callables>`. Tuy nhiên, phương thức ``ssl.SSLObject.__init__`` chỉ tồn tại để phát sinh một
        :exc:`TypeError` với thông báo chi tiết hơn, do đó khiến không thể gọi (khởi tạo) :class:`ssl.SSLObject`.

   .. note::

        Phép kiểm tra :func:`isinstance` đối với một protocol có thể kiểm tra tại runtime có thể chậm một cách đáng ngạc nhiên so với phép kiểm tra ``isinstance()`` đối với một class không phải protocol. Hãy cân nhắc sử dụng các cách viết thay thế như
        :func:`hasattr` để thực hiện các phép kiểm tra cấu trúc trong mã nhạy cảm về hiệu năng.

   .. versionadded:: 3.8

   .. versionchanged:: 3.12
      Việc triển khai nội bộ các phép kiểm tra :func:`isinstance` đối với protocol có thể kiểm tra tại runtime hiện sử dụng :func:`inspect.getattr_static` để tra cứu các thuộc tính (trước đây sử dụng :func:`hasattr`). Do đó, một số đối tượng trước đây được xem là instance của một protocol có thể kiểm tra tại runtime có thể không còn được xem là instance của protocol đó trên Python 3.12+ và ngược lại. Hầu hết người dùng khó bị ảnh hưởng bởi thay đổi này.

   .. versionchanged:: 3.12
      Các thành viên của một protocol có thể kiểm tra tại runtime hiện được xem là đã "đóng băng" tại runtime ngay khi class được tạo. Việc monkey-patch các thuộc tính vào một protocol có thể kiểm tra tại runtime vẫn hoạt động, nhưng sẽ không ảnh hưởng đến các phép kiểm tra :func:`isinstance` so sánh các đối tượng với protocol đó. Xem :ref:`Có gì mới trong Python 3.12 <whatsnew-typing-py312>` để biết thêm chi tiết.


.. class:: TypedDict(dict)

   Một cấu trúc đặc biệt để thêm type hint vào một dictionary. Tại runtime, "các instance :class:`!TypedDict`" đơn giản chỉ là :class:`dicts <dict>`.

   ``TypedDict`` khai báo một kiểu dictionary yêu cầu tất cả instance của nó phải có một tập khóa nhất định, trong đó mỗi khóa được liên kết với một giá trị có kiểu nhất quán. Yêu cầu này không được kiểm tra tại runtime mà chỉ được các trình kiểm tra kiểu thực thi. Cách sử dụng::

      class Point2D(TypedDict):
          x: int
          y: int
          label: str

      a: Point2D = {'x': 1, 'y': 2, 'label': 'good'}  # OK
      b: Point2D = {'z': 3, 'label': 'bad'}           # Không vượt qua kiểm tra kiểu

      assert Point2D(x=1, y=2, label='first') == dict(x=1, y=2, label='first')

   Một cách khác để tạo ``TypedDict`` là sử dụng cú pháp gọi hàm. Đối số thứ hai phải là một :class:`dict` literal::

      Point2D = TypedDict('Point2D', {'x': int, 'y': int, 'label': str})

   Cú pháp hàm này cho phép định nghĩa các khóa không hợp lệ
   :ref:`định danh <identifiers>`, chẳng hạn vì chúng là từ khóa hoặc chứa dấu gạch nối, hoặc khi tên khóa không được
   :ref:`biến đổi <private-name-mangling>` như các tên private thông thường::

      # gây ra SyntaxError
      class Point2D(TypedDict):
          in: int  # 'in' là một từ khóa
          x-y: int  # tên có dấu gạch ngang

      class Definition(TypedDict):
          __schema: str  # được biến đổi thành `_Definition__schema`

      # Được, cú pháp hàm
      Point2D = TypedDict('Point2D', {'in': int, 'x-y': int})
      Definition = TypedDict('Definition', {'__schema': str})  # không được biến đổi

   Theo mặc định, tất cả các khóa phải có mặt trong một ``TypedDict``. Có thể đánh dấu từng khóa là không bắt buộc bằng :data:`NotRequired`::

      class Point2D(TypedDict):
          x: int
          y: int
          label: NotRequired[str]

      # Cú pháp thay thế
      Point2D = TypedDict('Point2D', {'x': int, 'y': int, 'label': NotRequired[str]})

   Điều này có nghĩa là một ``Point2D`` ``TypedDict`` có thể bỏ qua khóa ``label``.

   Cũng có thể đánh dấu tất cả các key là không bắt buộc theo mặc định bằng cách chỉ định tính toàn phần là ``False``::

      class Point2D(TypedDict, total=False):
          x: int
          y: int

      # Cú pháp thay thế
      Point2D = TypedDict('Point2D', {'x': int, 'y': int}, total=False)

   Điều này có nghĩa là một ``Point2D`` ``TypedDict`` có thể bỏ qua bất kỳ key nào. Một type checker chỉ được yêu cầu hỗ trợ giá trị literal ``False`` hoặc ``True`` cho đối số ``total``. ``True`` là giá trị mặc định và khiến tất cả các item được định nghĩa trong phần thân class trở thành bắt buộc.

   Có thể đánh dấu từng key riêng lẻ của một ``total=False`` ``TypedDict`` là bắt buộc bằng cách sử dụng :data:`Required`::

      class Point2D(TypedDict, total=False):
          x: Required[int]
          y: Required[int]
          label: str

      # Cú pháp thay thế
      Point2D = TypedDict('Point2D', {
          'x': Required[int],
          'y': Required[int],
          'label': str
      }, total=False)

   Một kiểu ``TypedDict`` có thể kế thừa từ một hoặc nhiều kiểu ``TypedDict`` khác bằng cú pháp dựa trên class. Cách sử dụng::

      class Point3D(Point2D):
          z: int

   ``Point3D`` có ba item: ``x``, ``y`` và ``z``. Nó tương đương với định nghĩa này::

      class Point3D(TypedDict):
          x: int
          y: int
          z: int

   Một ``TypedDict`` không thể kế thừa từ một lớp không phải \ ``TypedDict``, ngoại trừ :class:`Generic`. Ví dụ::

      class X(TypedDict):
          x: int

      class Y(TypedDict):
          y: int

      class Z(object): pass  # Một lớp không phải TypedDict

      class XY(X, Y): pass  # OK

      class XZ(X, Z): pass  # gây ra TypeError

   Một ``TypedDict`` có thể là generic::

      class Group[T](TypedDict):
          key: T
          group: list[T]

   Để tạo một ``TypedDict`` generic tương thích với Python 3.11 trở xuống, hãy kế thừa rõ ràng từ :class:`Generic`:

   .. testcode::

      T = TypeVar("T")

      class Group(TypedDict, Generic[T]):
          key: T
          group: list[T]

   Có thể introspect một ``TypedDict`` thông qua :func:`annotationlib.get_annotations` (xem :ref:`annotations-howto` để biết thêm thông tin về các phương pháp hay nhất khi sử dụng annotations) và các thuộc tính sau:

   .. attribute:: __total__

      ``Point2D.__total__`` cung cấp giá trị của đối số ``total``. Ví dụ:

      .. doctest::

         >>> from typing import TypedDict
         >>> class Point2D(TypedDict): pass
         >>> Point2D.__total__
         True
         >>> class Point2D(TypedDict, total=False): pass
         >>> Point2D.__total__
         False
         >>> class Point3D(Point2D): pass
         >>> Point3D.__total__
         True

      Thuộc tính này chỉ phản ánh *only* giá trị của đối số ``total`` đối với lớp ``TypedDict`` hiện tại, chứ không phản ánh việc lớp đó có đầy đủ về mặt ngữ nghĩa hay không. Ví dụ, một ``TypedDict`` có ``__total__`` được đặt thành ``True`` có thể có các khóa được đánh dấu bằng :data:`NotRequired`, hoặc có thể kế thừa từ một ``TypedDict`` khác với ``total=False``. Vì vậy, nhìn chung nên sử dụng
      :attr:`__required_keys__` và :attr:`__optional_keys__` để introspection.

   .. attribute:: __required_keys__

      .. versionadded:: 3.9

   .. attribute:: __optional_keys__

      ``Point2D.__required_keys__`` và ``Point2D.__optional_keys__`` trả về
      các đối tượng :class:`frozenset` lần lượt chứa các khóa bắt buộc và không bắt buộc.

      Các khóa được đánh dấu bằng :data:`Required` sẽ luôn xuất hiện trong ``__required_keys__``, còn các khóa được đánh dấu bằng :data:`NotRequired` sẽ luôn xuất hiện trong ``__optional_keys__``.

      Để tương thích ngược với Python 3.10 trở xuống, bạn cũng có thể sử dụng tính kế thừa để khai báo cả khóa bắt buộc và không bắt buộc trong cùng một ``TypedDict``. Việc này được thực hiện bằng cách khai báo một ``TypedDict`` với một giá trị cho đối số ``total``, sau đó kế thừa từ nó trong một ``TypedDict`` khác với giá trị khác cho ``total``:

      .. doctest::

         >>> class Point2D(TypedDict, total=False):
         ...     x: int
         ...     y: int
         ...
         >>> class Point3D(Point2D):
         ...     z: int
         ...
         >>> Point3D.__required_keys__ == frozenset({'z'})
         True
         >>> Point3D.__optional_keys__ == frozenset({'x', 'y'})
         True

      .. versionadded:: 3.9

      .. note::

         Nếu sử dụng ``from __future__ import annotations`` hoặc nếu các chú thích được cung cấp dưới dạng chuỗi, các chú thích sẽ không được đánh giá khi ``TypedDict`` được định nghĩa. Do đó, quá trình introspection tại runtime mà ``__required_keys__`` và ``__optional_keys__`` dựa vào có thể không hoạt động chính xác, và giá trị của các thuộc tính có thể không đúng.

   Hỗ trợ cho :data:`ReadOnly` được thể hiện qua các thuộc tính sau:

   .. attribute:: __readonly_keys__

      Một :class:`frozenset` chứa tên của tất cả các key chỉ đọc. Các key là chỉ đọc nếu có qualifier :data:`ReadOnly`.

      .. versionadded:: 3.13

   .. attribute:: __mutable_keys__

      Một :class:`frozenset` chứa tên của tất cả các key có thể thay đổi. Các key có thể thay đổi nếu không có qualifier :data:`ReadOnly`.

      .. versionadded:: 3.13

   Xem phần `TypedDict <https://typing.python.org/en/latest/spec/typeddict.html#typeddict>`_ trong tài liệu typing để biết thêm ví dụ và các quy tắc chi tiết.

   .. versionadded:: 3.8

   .. versionchanged:: 3.9
      ``TypedDict`` hiện là một function thay vì một class. Nó vẫn có thể được sử dụng làm class base, như mô tả ở trên.

   .. versionchanged:: 3.11
      Đã thêm hỗ trợ đánh dấu từng key riêng lẻ là :data:`Required` hoặc :data:`NotRequired`. Xem :pep:`655`.

   .. versionchanged:: 3.11
      Đã thêm hỗ trợ cho các ``TypedDict``\ s tổng quát.

   .. versionchanged:: 3.13
      Đã loại bỏ hỗ trợ cho phương thức tạo ``TypedDict``\ s bằng đối số từ khóa.

   .. versionchanged:: 3.13
      Đã thêm hỗ trợ cho bộ định tính :data:`ReadOnly`.

   .. deprecated-removed:: 3.13 3.15
      Khi sử dụng cú pháp hàm để tạo một lớp TypedDict, việc không truyền giá trị cho tham số 'fields' (``TD = TypedDict("TD")``) đã không còn được khuyến nghị. Việc truyền ``None`` vào tham số 'fields' (``TD = TypedDict("TD", None)``) cũng không còn được khuyến nghị. Cả hai cách sẽ bị cấm trong Python 3.15. Để tạo một lớp TypedDict không có trường nào, hãy sử dụng ``class TD(TypedDict): pass`` hoặc ``TD = TypedDict("TD", {})``.

Các protocol
------------

Mô-đun :mod:`!typing` cung cấp các protocol sau. Tất cả đều được trang trí bằng :deco:`runtime_checkable`.

.. class:: SupportsAbs

    Một protocol có một phương thức trừu tượng ``__abs__`` duy nhất, với kiểu trả về có tính đồng biến.

.. class:: SupportsBytes

    Một giao thức có một phương thức trừu tượng ``__bytes__``.

.. class:: SupportsComplex

    Một giao thức có một phương thức trừu tượng ``__complex__``.

.. class:: SupportsFloat

    Một giao thức có một phương thức trừu tượng ``__float__``.

.. class:: SupportsIndex

    Một giao thức có một phương thức trừu tượng ``__index__``.

    .. versionadded:: 3.8

.. class:: SupportsInt

    Một giao thức có một phương thức trừu tượng ``__int__``.

.. class:: SupportsRound

    Một giao thức có một phương thức trừu tượng ``__round__`` có tính đồng biến theo kiểu trả về.

.. _typing-io:

Các ABC và Protocol để làm việc với I/O
---------------------------------------

.. class:: IO[AnyStr]
           TextIO BinaryIO

   Lớp generic ``IO[AnyStr]`` và các lớp con ``TextIO(IO[str])`` và ``BinaryIO(IO[bytes])`` biểu thị các kiểu stream I/O như được trả về bởi
   :func:`open`. Lưu ý rằng các lớp này không phải là protocol và interface của chúng khá rộng.

Các protocol :class:`io.Reader` và :class:`io.Writer` cung cấp một lựa chọn đơn giản hơn cho kiểu đối số khi lần lượt chỉ truy cập các phương thức ``read()`` hoặc ``write()``::

   def read_and_write(reader: Reader[str], writer: Writer[bytes]):
       data = reader.read()
       writer.write(data.encode())

Ngoài ra, hãy cân nhắc sử dụng :class:`collections.abc.Iterable` để lặp qua các dòng của input stream::

   def read_config(stream: Iterable[str]):
       for line in stream:
           ...

Các hàm và decorator
--------------------

.. function:: cast(typ, val)

   Ép một giá trị về một kiểu.

   Giá trị này được trả về không thay đổi. Đối với trình kiểm tra kiểu, điều này cho biết giá trị trả về có kiểu được chỉ định, nhưng trong runtime, chúng ta cố ý không kiểm tra gì cả (chúng ta muốn thao tác này nhanh nhất có thể).

.. function:: assert_type(val, typ, /)

   Yêu cầu trình kiểm tra kiểu tĩnh xác nhận rằng *val* có kiểu được suy luận là *typ*.

   Trong runtime, thao tác này không làm gì cả: nó trả về đối số đầu tiên không thay đổi, không thực hiện kiểm tra hay gây ra side effect nào, bất kể kiểu thực tế của đối số là gì.

   Khi trình kiểm tra kiểu tĩnh gặp một lời gọi đến ``assert_type()``, nó sẽ phát sinh lỗi nếu giá trị không có kiểu được chỉ định::

       def greet(name: str) -> None:
           assert_type(name, str)  # OK, kiểu được suy luận của `name` là `str`
           assert_type(name, int)  # lỗi của trình kiểm tra kiểu

   Hàm này hữu ích để đảm bảo cách trình kiểm tra kiểu hiểu về một script phù hợp với ý định của developer::

       def complex_function(arg: object):
           # Thực hiện một số logic thu hẹp kiểu phức tạp,
           # sau đó chúng ta hy vọng kiểu được suy luận sẽ là `int`
           ...
           # Kiểm tra xem trình kiểm tra kiểu có hiểu đúng hàm của chúng ta hay không
           assert_type(arg, int)

   .. versionadded:: 3.11

.. function:: assert_never(arg, /)

   Yêu cầu trình kiểm tra kiểu tĩnh xác nhận rằng một dòng mã không thể được thực thi.

   Ví dụ::

       def int_or_str(arg: int | str) -> None:
           match arg:
               case int():
                   print("It's an int")
               case str():
                   print("It's a str")
               case _ as unreachable:
                   assert_never(unreachable)

   Ở đây, các chú thích cho phép trình kiểm tra kiểu suy luận rằng trường hợp cuối cùng không bao giờ có thể được thực thi, vì ``arg`` hoặc là :class:`int` hoặc là :class:`str`, và cả hai tùy chọn đều đã được bao quát bởi các trường hợp trước đó.

   Nếu trình kiểm tra kiểu phát hiện rằng một lệnh gọi đến ``assert_never()`` có thể đạt tới, nó sẽ phát ra một lỗi. Ví dụ: nếu chú thích kiểu của ``arg`` thay vào đó là ``int | str | float``, trình kiểm tra kiểu sẽ phát ra một lỗi chỉ ra rằng ``unreachable`` có kiểu :class:`float`. Để một lệnh gọi đến ``assert_never`` vượt qua kiểm tra kiểu, kiểu được suy luận của đối số được truyền vào phải là kiểu dưới, :data:`Never`, và không thể là kiểu nào khác.

   Trong runtime, lệnh gọi này sẽ ném ra một exception.

   .. seealso::
      `Kiểm tra mã không thể thực thi và tính đầy đủ <https://typing.python.org/en/latest/guides/unreachable.html>`__ cung cấp thêm thông tin về việc kiểm tra tính đầy đủ với static typing.

   .. versionadded:: 3.11

.. function:: reveal_type(obj, /)

   Yêu cầu static type checker hiển thị kiểu được suy luận của một biểu thức.

   Khi static type checker gặp lệnh gọi đến hàm này, nó sẽ phát diagnostic kèm kiểu được suy luận của đối số. Ví dụ::

      x: int = 1
      reveal_type(x)  # Kiểu được tiết lộ là "builtins.int"

   Điều này hữu ích khi bạn muốn gỡ lỗi cách type checker xử lý một đoạn mã cụ thể.

   Trong runtime, hàm này in kiểu runtime của đối số ra
   :data:`sys.stderr` và trả về đối số không thay đổi (cho phép sử dụng lời gọi trong một biểu thức)::

      x = reveal_type(1)  # in ra "Runtime type is int"
      print(x)  # in ra "1"

   Lưu ý rằng kiểu runtime có thể khác với kiểu được trình kiểm tra kiểu suy luận tĩnh (cụ thể hơn hoặc tổng quát hơn).

   Hầu hết trình kiểm tra kiểu đều hỗ trợ ``reveal_type()`` ở bất kỳ đâu, ngay cả khi tên này không được import từ ``typing``. Tuy nhiên, việc import tên này từ ``typing`` cho phép mã của bạn chạy mà không gặp lỗi runtime và truyền đạt mục đích rõ ràng hơn.

   .. versionadded:: 3.11

.. decorator:: dataclass_transform(*, eq_default=True, order_default=False, \
                                   kw_only_default=False, frozen_default=False, \ field_specifiers=(), ****kwargs)

   Decorator dùng để đánh dấu một đối tượng là đối tượng cung cấp
   Hành vi tương tự :func:`dataclass <dataclasses.dataclass>`.

   ``@dataclass_transform`` có thể được dùng để trang trí một lớp, metaclass hoặc một hàm vốn là decorator. Sự hiện diện của ``@dataclass_transform()`` cho trình kiểm tra kiểu tĩnh biết rằng đối tượng được trang trí thực hiện "phép thuật" trong runtime để biến đổi một lớp theo cách tương tự như
   :deco:`dataclasses.dataclass`.

   Ví dụ sử dụng với một hàm decorator:

   .. testcode::

      @dataclass_transform()
      def create_model[T](cls: type[T]) -> type[T]:
          ...
          return cls

      @create_model
      class CustomerModel:
          id: int
          name: str

   Trên một lớp cơ sở::

      @dataclass_transform()
      class ModelBase: ...

      class CustomerModel(ModelBase):
          id: int
          name: str

   Trên một metaclass::

      @dataclass_transform()
      class ModelMeta(type): ...

      class ModelBase(metaclass=ModelMeta): ...

      class CustomerModel(ModelBase):
          id: int
          name: str

   Các lớp ``CustomerModel`` được định nghĩa ở trên sẽ được trình kiểm tra kiểu xử lý tương tự như các lớp được tạo bằng
   :deco:`dataclasses.dataclass`. Ví dụ, trình kiểm tra kiểu sẽ giả định rằng các lớp này có các phương thức ``__init__`` nhận ``id`` và ``name``.

   Lớp, metaclass hoặc hàm được trang trí có thể chấp nhận các đối số bool sau đây mà các trình kiểm tra kiểu sẽ giả định là có cùng tác dụng như khi chúng được áp dụng cho
   decorator :deco:`dataclasses.dataclass`: ``init``, ``eq``, ``order``, ``unsafe_hash``, ``frozen``, ``match_args``, ``kw_only`` và ``slots``. Giá trị của các đối số này (``True`` hoặc ``False``) phải có thể được đánh giá tĩnh.

   Có thể sử dụng các đối số của decorator ``@dataclass_transform`` để tùy chỉnh các hành vi mặc định của lớp, metaclass hoặc hàm được trang trí:

   :param bool eq_default:Cho biết liệu tham số ``eq`` được giả định là ``True`` hay ``False`` nếu bên gọi bỏ qua tham số này. Mặc định là ``True``.

   :param bool order_default:Cho biết liệu tham số ``order`` được giả định là ``True`` hay ``False`` nếu bên gọi bỏ qua tham số này. Mặc định là ``False``.

   :param bool kw_only_default:Cho biết liệu tham số ``kw_only`` được giả định là ``True`` hay ``False`` nếu bên gọi bỏ qua tham số này. Mặc định là ``False``.

   :param bool frozen_default:Cho biết liệu tham số ``frozen`` được giả định là ``True`` hay ``False`` nếu bên gọi bỏ qua tham số này. Mặc định là ``False``.

       .. versionadded:: 3.12

   :param field_specifiers:Chỉ định một danh sách tĩnh gồm các class hoặc function được hỗ trợ để mô tả các trường, tương tự như :func:`dataclasses.field`. Mặc định là ``()``.
   :type field_specifiers: tuple[Callable[..., Any], ...]

   :param Any \**kwargs:Các đối số keyword tùy ý khác được chấp nhận để cho phép các phần mở rộng có thể có trong tương lai.

   Các type checker nhận diện những tham số tùy chọn sau đây trên các bộ chỉ định trường:

   .. list-table:: **Các tham số được nhận diện cho bộ chỉ định trường**
      :header-rows: 1
      :widths: 20 80

      * - Tên tham số
        - Mô tả
      * - ``init``
        - Cho biết liệu trường có được đưa vào phương thức ``__init__`` được tổng hợp hay không. Nếu không được chỉ định, ``init`` mặc định là ``True``.
      * - ``default``
        - Cung cấp giá trị mặc định cho trường.
      * - ``default_factory``
        - Cung cấp một callback runtime trả về giá trị mặc định cho trường. Nếu không chỉ định ``default`` và ``default_factory``, trường được coi là không có giá trị mặc định và phải được cung cấp một giá trị khi khởi tạo lớp.
      * - ``factory``
        - Bí danh cho tham số ``default_factory`` trên các bộ chỉ định trường.
      * - ``kw_only``
        - Cho biết liệu trường có được đánh dấu là chỉ dùng keyword hay không. Nếu ``True``, trường sẽ chỉ dùng keyword. Nếu ``False``, trường sẽ không chỉ dùng keyword. Nếu không được chỉ định, giá trị của tham số ``kw_only`` trên đối tượng được trang trí bằng ``@dataclass_transform`` sẽ được sử dụng; nếu tham số đó cũng không được chỉ định, giá trị của ``kw_only_default`` trên ``@dataclass_transform`` sẽ được sử dụng.
      * - ``alias``
        - Cung cấp một tên thay thế cho trường. Tên thay thế này được sử dụng trong phương thức ``__init__`` được tổng hợp.

   Trong runtime, decorator này ghi lại các đối số của nó vào thuộc tính ``__dataclass_transform__`` trên đối tượng được trang trí. Nó không có tác động runtime nào khác.

   Xem :pep:`681` để biết thêm chi tiết.

   .. versionadded:: 3.11

.. _overload:

.. decorator:: overload

   Decorator dùng để tạo các hàm và phương thức overload.

   Decorator ``@overload`` cho phép mô tả các hàm và phương thức hỗ trợ nhiều tổ hợp kiểu đối số khác nhau. Một chuỗi các định nghĩa được trang trí bằng ``@overload`` phải được theo sau chính xác một định nghĩa không được trang trí bằng ``@overload`` (cho cùng một hàm/phương thức).

   Các định nghĩa được trang trí bằng ``@overload`` chỉ phục vụ type checker, vì chúng sẽ bị định nghĩa không được trang trí bằng ``@overload`` ghi đè. Trong khi đó, định nghĩa không được trang trí bằng ``@overload`` sẽ được sử dụng tại runtime nhưng nên bị type checker bỏ qua. Khi chạy, việc gọi trực tiếp một hàm được trang trí bằng ``@overload`` sẽ gây ra
   :exc:`NotImplementedError`.

   Một ví dụ về overload cho kiểu chính xác hơn kiểu có thể biểu diễn bằng union hoặc type variable:

   .. testcode::

      @overload
      def process(response: None) -> None:
          ...
      @overload
      def process(response: int) -> tuple[int, str]:
          ...
      @overload
      def process(response: bytes) -> str:
          ...
      def process(response):
          ...  # đặt phần triển khai thực tế ở đây

   Xem :pep:`484` để biết thêm chi tiết và so sánh với các ngữ nghĩa typing khác.

   .. versionchanged:: 3.11
      Giờ đây, có thể introspect các hàm overloaded tại runtime bằng cách sử dụng
      :func:`get_overloads`.


.. function:: get_overloads(func)

   Trả về một chuỗi các định nghĩa được trang trí bằng :deco:`overload` cho *func*.

   *func* là đối tượng hàm dùng để triển khai hàm overloaded. Ví dụ, với định nghĩa của ``process`` trong tài liệu về :deco:`overload`, ``get_overloads(process)`` sẽ trả về một chuỗi gồm ba đối tượng hàm tương ứng với ba overload đã được định nghĩa. Nếu được gọi trên một hàm không có overload, ``get_overloads()`` sẽ trả về một chuỗi rỗng.

   Có thể sử dụng ``get_overloads()`` để introspect một hàm overloaded tại runtime.

   .. versionadded:: 3.11


.. function:: clear_overloads()

   Xóa tất cả các overload đã đăng ký trong registry nội bộ.

   Có thể sử dụng thao tác này để thu hồi bộ nhớ mà registry đã sử dụng.

   .. versionadded:: 3.11


.. decorator:: final

   Decorator dùng để chỉ báo các phương thức final và các lớp final.

   Việc trang trí một phương thức bằng ``@final`` cho trình kiểm tra kiểu biết rằng phương thức đó không thể bị ghi đè trong một lớp con. Việc trang trí một lớp bằng ``@final`` cho biết lớp đó không thể được phân lớp.

   Ví dụ::

      class Base:
          @final
          def done(self) -> None:
              ...
      class Sub(Base):
          def done(self) -> None:  # Lỗi do trình kiểm tra kiểu báo cáo
              ...

      @final
      class Leaf:
          ...
      class Other(Leaf):  # Lỗi do trình kiểm tra kiểu báo cáo
          ...

   Các thuộc tính này không được kiểm tra trong runtime. Xem :pep:`591` để biết thêm chi tiết.

   .. versionadded:: 3.8

   .. versionchanged:: 3.11
      Decorator giờ đây sẽ cố gắng đặt thuộc tính ``__final__`` thành ``True`` trên đối tượng được trang trí. Do đó, có thể sử dụng một phép kiểm tra như ``if getattr(obj, "__final__", False)`` trong runtime để xác định liệu một đối tượng ``obj`` đã được đánh dấu là final hay chưa. Nếu đối tượng được trang trí không hỗ trợ việc đặt thuộc tính, decorator sẽ trả về đối tượng đó mà không đưa ra ngoại lệ.


.. decorator:: no_type_check

   Decorator dùng để cho biết rằng các annotation không phải là type hint.

   Điều này hoạt động như một class hoặc function :term:`decorator`. Với một class, nó được áp dụng đệ quy cho tất cả method và class được định nghĩa trong class đó (nhưng không áp dụng cho các method được định nghĩa trong superclass hoặc subclass của nó). Các trình kiểm tra kiểu sẽ bỏ qua mọi annotation trong function hoặc class có decorator này.

   ``@no_type_check`` thay đổi trực tiếp đối tượng được decorate.

.. decorator:: no_type_check_decorator

   Decorator dùng để tạo hiệu ứng :func:`no_type_check` cho một decorator khác.

   Lệnh này bọc decorator bằng một thành phần bọc function được decorate trong :func:`no_type_check`.

   .. deprecated-removed:: 3.13 3.15
      Không có trình kiểm tra kiểu nào từng hỗ trợ ``@no_type_check_decorator``. Vì vậy, nó đã bị deprecated và sẽ bị xóa trong Python 3.15.

.. decorator:: override

   Decorator cho biết một method trong subclass được dự định ghi đè một method hoặc attribute trong superclass.

   Các trình kiểm tra kiểu nên phát hiện lỗi nếu một method được decorate bằng ``@override`` thực tế không ghi đè bất kỳ thành phần nào. Điều này giúp ngăn các lỗi có thể xảy ra khi một base class được thay đổi mà không có thay đổi tương ứng trong child class.

   Ví dụ:

   .. testcode::

      class Base:
          def log_status(self) -> None:
              ...

      class Sub(Base):
          @override
          def log_status(self) -> None:  # Được: ghi đè Base.log_status
              ...

          @override
          def done(self) -> None:  # Lỗi được trình kiểm tra kiểu báo cáo
              ...

   Thuộc tính này không được kiểm tra trong runtime.

   Decorator sẽ cố gắng đặt thuộc tính ``__override__`` thành ``True`` trên đối tượng được áp dụng decorator. Do đó, có thể sử dụng một phép kiểm tra như ``if getattr(obj, "__override__", False)`` trong runtime để xác định xem đối tượng ``obj`` có được đánh dấu là một override hay không. Nếu đối tượng được áp dụng decorator không hỗ trợ việc đặt thuộc tính, decorator sẽ trả về đối tượng đó không thay đổi mà không phát sinh ngoại lệ.

   Xem :pep:`698` để biết thêm chi tiết.

   .. versionadded:: 3.12


.. decorator:: type_check_only

   Decorator dùng để đánh dấu một lớp hoặc hàm là không khả dụng trong runtime.

   Bản thân decorator này không khả dụng tại runtime. Nó chủ yếu được dùng để đánh dấu các lớp được định nghĩa trong các tệp type stub nếu một implementation trả về một instance của lớp private::

      @type_check_only
      class Response:  # private hoặc không khả dụng tại runtime
          code: int
          def get_header(self, name: str) -> str: ...

      def fetch_response() -> Response: ...

   Lưu ý rằng không nên trả về các instance của lớp private. Thông thường, tốt hơn là làm cho các lớp đó public.

Các hàm hỗ trợ introspection
----------------------------

.. function:: get_type_hints(obj, globalns=None, localns=None, include_extras=False, *, format=Format.VALUE)

   Trả về một dictionary chứa các type hint cho một function, method, module, class object hoặc đối tượng callable khác.

   Giá trị này thường giống với :func:`annotationlib.get_annotations`, nhưng function này thực hiện các thay đổi sau đối với dictionary annotations:

   * Các forward reference được mã hóa dưới dạng string literal hoặc đối tượng :class:`ForwardRef` sẽ được xử lý bằng cách đánh giá chúng trong *globalns*, *localns* và (khi thích hợp) namespace của *obj*'s :ref:`type parameter <type-params>`. Nếu *globalns* hoặc *localns* không được cung cấp, các dictionary namespace phù hợp sẽ được suy ra từ *obj*.
   * ``None`` được thay thế bằng :class:`types.NoneType`.
   * Nếu :deco:`no_type_check` đã được áp dụng cho *obj*, một từ điển rỗng sẽ được trả về.
   * Nếu *obj* là một class ``C``, hàm sẽ trả về một từ điển hợp nhất các annotation từ các lớp cơ sở của ``C`` với những annotation được khai báo trực tiếp trên ``C``. Việc này được thực hiện bằng cách duyệt qua :attr:`C.__mro__ <type.__mro__>` và lần lượt kết hợp
     :term:`annotations <variable annotation>` của từng lớp cơ sở. Các annotation trên những lớp xuất hiện sớm hơn trong :term:`method resolution order` luôn được ưu tiên hơn các annotation trên những lớp xuất hiện muộn hơn trong thứ tự phân giải phương thức.
   * Hàm sẽ đệ quy thay thế mọi lần xuất hiện của ``Annotated[T, ...]``, ``Required[T]``, ``NotRequired[T]`` và ``ReadOnly[T]`` bằng ``T``, trừ khi *include_extras* được đặt thành ``True`` (xem
     :class:`Annotated` để biết thêm thông tin).

   .. caution::

      Hàm này có thể thực thi mã tùy ý được chứa trong các annotation. Xem :ref:`annotationlib-security` để biết thêm thông tin.

   .. note::

      Nếu sử dụng :attr:`Format.VALUE <annotationlib.Format.VALUE>` và không thể phân giải bất kỳ tham chiếu tiến (forward reference) nào trong các chú thích của *obj*, một
      ngoại lệ :exc:`NameError` sẽ được đưa ra. Ví dụ, điều này có thể xảy ra với các tên được nhập dưới :data:`if TYPE_CHECKING <TYPE_CHECKING>`. Tổng quát hơn, bất kỳ loại ngoại lệ nào cũng có thể được đưa ra nếu một chú thích chứa mã Python không hợp lệ.

   .. note::

      Không hỗ trợ gọi :func:`get_type_hints` trên một instance. Để truy xuất các chú thích cho một instance, hãy gọi
      :func:`get_type_hints` trên lớp của instance đó (ví dụ: ``get_type_hints(type(obj))``).

   .. versionchanged:: 3.9
      Đã thêm tham số ``include_extras`` như một phần của :pep:`593`. Xem tài liệu về :data:`Annotated` để biết thêm thông tin.

   .. versionchanged:: 3.11
      Trước đây, ``Optional[t]`` được thêm vào các chú thích của hàm và phương thức nếu một giá trị mặc định bằng ``None`` được thiết lập. Giờ đây, chú thích được trả về không thay đổi.

   .. versionchanged:: 3.14
      Đã thêm tham số ``format``. Xem tài liệu về
      :func:`annotationlib.get_annotations` để biết thêm thông tin.

   .. versionchanged:: 3.14
      Không còn hỗ trợ gọi :func:`get_type_hints` trên các instance. Một số instance từng được chấp nhận trong các phiên bản trước như một chi tiết triển khai không được ghi lại.

.. function:: get_origin(tp)

   Lấy phiên bản không có chỉ số của một kiểu: đối với một đối tượng typing có dạng ``X[Y, Z, ...]``, trả về ``X``.

   Nếu ``X`` là bí danh trong typing-module cho một builtin hoặc
   :mod:`collections` class, nó sẽ được chuẩn hóa thành class gốc. Nếu ``X`` là một instance của :class:`ParamSpecArgs` hoặc :class:`ParamSpecKwargs`, trả về :class:`ParamSpec` cơ bản. Trả về ``None`` cho các đối tượng không được hỗ trợ.

   Ví dụ:

   .. testcode::

      assert get_origin(str) is None
      assert get_origin(Dict[str, int]) is dict
      assert get_origin(Union[int, str]) is Union
      assert get_origin(Annotated[str, "metadata"]) is Annotated
      P = ParamSpec('P')
      assert get_origin(P.args) is P
      assert get_origin(P.kwargs) is P

   .. versionadded:: 3.8

.. function:: get_args(tp)

   Lấy các đối số kiểu với tất cả phép thay thế đã được thực hiện: đối với một đối tượng typing có dạng ``X[Y, Z, ...]``, trả về ``(Y, Z, ...)``.

   Nếu ``X`` là một union hoặc :class:`Literal` nằm trong một kiểu generic khác, thứ tự của ``(Y, Z, ...)`` có thể khác với thứ tự của các đối số ban đầu ``[Y, Z, ...]`` do việc lưu vào bộ nhớ đệm kiểu. Trả về ``()`` đối với các đối tượng không được hỗ trợ.

   Ví dụ:

   .. testcode::

      assert get_args(int) == ()
      assert get_args(Dict[int, str]) == (int, str)
      assert get_args(Union[int, str]) == (int, str)

   .. versionadded:: 3.8

.. function:: get_protocol_members(tp)

   Trả về tập hợp các thành viên được định nghĩa trong một :class:`Protocol`.

   .. doctest::

      >>> from typing import Protocol, get_protocol_members
      >>> class P(Protocol):
      ...     def a(self) -> str: ...
      ...     b: int
      >>> get_protocol_members(P) == frozenset({'a', 'b'})
      True

   Ném :exc:`TypeError` đối với các đối số không phải là Protocol.

   .. versionadded:: 3.13

.. function:: is_protocol(tp)

   Xác định xem một kiểu có phải là :class:`Protocol` hay không.

   Ví dụ:

   .. testcode::

      class P(Protocol):
          def a(self) -> str: ...
          b: int

      assert is_protocol(P)
      assert not is_protocol(int)

   Hàm này chỉ trả về true đối với các lớp ``Protocol``, không phải đối với
   :ref:`bí danh generic <types-genericalias>` của chúng:

   .. testcode::

      class GenericP[T](Protocol):
          def a(self) -> T: ...
          b: int

      assert not is_protocol(GenericP[int])

   .. versionadded:: 3.13

.. function:: is_typeddict(tp)

   Kiểm tra xem một kiểu có phải là :class:`TypedDict` hay không.

   Ví dụ:

   .. testcode::

      class Film(TypedDict):
          title: str
          year: int

      assert is_typeddict(Film)
      assert not is_typeddict(list | str)

      # TypedDict là một factory để tạo các typed dict,
      # chứ bản thân nó không phải là một typed dict
      assert not is_typeddict(TypedDict)

   Hàm này chỉ trả về true cho các lớp ``TypedDict``, không phải cho
   :ref:`bí danh generic <types-genericalias>` của chúng:

   .. testcode::

      class GenericFilm[T](TypedDict):
          title: str
          year: T

      assert not is_typeddict(GenericFilm[int])

   .. versionadded:: 3.10

.. class:: ForwardRef

   Lớp được sử dụng để biểu diễn kiểu nội bộ cho các tham chiếu chuyển tiếp đến chuỗi.

   Ví dụ, ``List["SomeClass"]`` được chuyển đổi ngầm thành ``List[ForwardRef("SomeClass")]``. Người dùng không nên khởi tạo :class:`!ForwardRef`, nhưng các công cụ introspection có thể sử dụng nó.

   .. note::
      :pep:`585` generic types such as ``list["SomeClass"]`` will not be
      được chuyển đổi ngầm thành ``list[ForwardRef("SomeClass")]`` và do đó sẽ không tự động phân giải thành ``list[SomeClass]``.

   .. versionadded:: 3.7.4

   .. versionchanged:: 3.14
      Hiện đây là bí danh của :class:`annotationlib.ForwardRef`. Một số hành vi chưa được ghi chép của lớp này đã thay đổi; ví dụ, sau khi ``ForwardRef`` được đánh giá, giá trị đã đánh giá sẽ không còn được lưu vào bộ nhớ đệm.

.. function:: evaluate_forward_ref(forward_ref, *, owner=None, globals=None, locals=None, type_params=None, format=annotationlib.Format.VALUE)

   Đánh giá một :class:`annotationlib.ForwardRef` dưới dạng :term:`type hint`.

   Điều này tương tự như việc gọi :meth:`annotationlib.ForwardRef.evaluate`, nhưng không giống phương thức đó, :func:`!evaluate_forward_ref` cũng đánh giá đệ quy các tham chiếu chuyển tiếp được lồng trong gợi ý kiểu.

   Xem tài liệu về :meth:`annotationlib.ForwardRef.evaluate` để biết ý nghĩa của các tham số *owner*, *globals*, *locals*, *type_params* và *format*.

   .. caution::

      Hàm này có thể thực thi mã tùy ý được chứa trong các annotation. Xem :ref:`annotationlib-security` để biết thêm thông tin.

   .. versionadded:: 3.14

.. data:: NoDefault

   Một đối tượng sentinel được dùng để cho biết rằng một tham số kiểu không có giá trị mặc định. Ví dụ:

   .. doctest::

      >>> T = TypeVar("T")
      >>> T.__default__ is typing.NoDefault
      True
      >>> S = TypeVar("S", default=None)
      >>> S.__default__ is None
      True

   .. versionadded:: 3.13

Hằng số
-------

.. data:: TYPE_CHECKING

   Một hằng số đặc biệt được các trình kiểm tra kiểu tĩnh giả định là ``True``. Khi runtime, nó là ``False``.

   Một module tốn nhiều chi phí để import và chỉ chứa các kiểu được dùng cho chú thích kiểu có thể được import an toàn bên trong khối ``if TYPE_CHECKING:``. Điều này ngăn module thực sự được import tại runtime; các chú thích không được đánh giá ngay (xem :pep:`649`), vì vậy việc sử dụng các ký hiệu chưa được định nghĩa trong chú thích là vô hại—miễn là sau đó bạn không kiểm tra chúng. Công cụ phân tích kiểu tĩnh sẽ đặt ``TYPE_CHECKING`` thành ``True`` trong quá trình phân tích kiểu tĩnh, nghĩa là module sẽ được import và các kiểu sẽ được kiểm tra đúng cách trong quá trình phân tích đó.

   Cách sử dụng::

      if TYPE_CHECKING:
          import expensive_mod

      def fun(arg: expensive_mod.SomeType) -> None:
          local_var: expensive_mod.AnotherType = other_fun()

   Nếu đôi khi bạn cần kiểm tra các chú thích kiểu tại runtime, trong đó có thể chứa các ký hiệu chưa được định nghĩa, hãy sử dụng
   :meth:`annotationlib.get_annotations` với tham số ``format`` là :attr:`annotationlib.Format.STRING` hoặc
   :attr:`annotationlib.Format.FORWARDREF` để truy xuất an toàn các chú thích mà không gây ra :exc:`NameError`.

   .. versionadded:: 3.5.2

.. _generic-concrete-collections:
.. _deprecated-aliases:

Bí danh đã lỗi thời
-------------------

Mô-đun này định nghĩa một số bí danh đã lỗi thời cho các lớp có sẵn trong thư viện chuẩn. Ban đầu, các bí danh này được đưa vào mô-đun :mod:`!typing` để hỗ trợ việc tham số hóa các lớp generic này bằng ``[]``. Tuy nhiên, các bí danh đã trở nên dư thừa trong Python 3.9, khi các lớp tương ứng có sẵn được nâng cấp để hỗ trợ ``[]`` (xem
:pep:`585`).

Các kiểu dư thừa này đã lỗi thời kể từ Python 3.9. Tuy nhiên, mặc dù các bí danh có thể bị xóa vào một thời điểm nào đó, hiện chưa có kế hoạch xóa chúng. Do đó, hiện tại interpreter không phát hành cảnh báo lỗi thời cho các bí danh này.

Nếu sau này quyết định xóa các bí danh đã lỗi thời này, interpreter sẽ phát hành cảnh báo lỗi thời trong ít nhất hai bản phát hành trước khi xóa. Các bí danh được đảm bảo vẫn tồn tại trong mô-đun :mod:`!typing` mà không có cảnh báo lỗi thời cho đến ít nhất Python 3.14.

Khuyến nghị các trình kiểm tra kiểu đánh dấu việc sử dụng những kiểu đã lỗi thời nếu chương trình mà chúng đang kiểm tra nhắm đến phiên bản Python tối thiểu là 3.9 hoặc mới hơn.

.. _corresponding-to-built-in-types:

Bí danh cho các kiểu tích hợp sẵn
"""""""""""""""""""""""""""""""""

.. class:: Dict(dict, MutableMapping[KT, VT])

   Bí danh không còn được khuyến nghị của :class:`dict`.

   Lưu ý rằng khi chú thích các đối số, nên sử dụng một kiểu collection trừu tượng như :class:`~collections.abc.Mapping` thay vì sử dụng :class:`dict` hoặc :class:`!typing.Dict`.

   .. deprecated:: 3.9
      :class:`builtins.dict <dict>` now supports subscripting (``[]``).
      Xem :pep:`585` và :ref:`types-genericalias`.

.. class:: List(list, MutableSequence[T])

   Bí danh không còn được khuyến nghị của :class:`list`.

   Lưu ý rằng khi chú thích các đối số, nên sử dụng một kiểu collection trừu tượng như
   :class:`~collections.abc.Sequence` hoặc :class:`~collections.abc.Iterable` thay vì sử dụng :class:`list` hoặc :class:`!typing.List`.

   .. deprecated:: 3.9
      :class:`builtins.list <list>` now supports subscripting (``[]``).
      Xem :pep:`585` và :ref:`types-genericalias`.

.. class:: Set(set, MutableSet[T])

   Bí danh không còn được khuyến nghị cho :class:`builtins.set <set>`.

   Lưu ý rằng để chú thích các đối số, nên sử dụng một kiểu collection trừu tượng như :class:`collections.abc.Set` thay vì sử dụng :class:`set` hoặc :class:`typing.Set`.

   .. deprecated:: 3.9
      :class:`builtins.set <set>` now supports subscripting (``[]``).
      Xem :pep:`585` và :ref:`types-genericalias`.

.. class:: FrozenSet(frozenset, AbstractSet[T_co])

   Bí danh không còn được khuyến nghị cho :class:`builtins.frozenset <frozenset>`.

   .. deprecated:: 3.9
      :class:`builtins.frozenset <frozenset>`
      hiện hỗ trợ phép lập chỉ mục (``[]``). Xem :pep:`585` và :ref:`types-genericalias`.

.. data:: Tuple

   Bí danh không còn được khuyến nghị cho :class:`tuple`.

   :class:`tuple` và ``Tuple`` được xử lý đặc biệt trong hệ thống kiểu; xem
   :ref:`annotating-tuples` để biết thêm chi tiết.

   .. deprecated:: 3.9
      :class:`builtins.tuple <tuple>` now supports subscripting (``[]``).
      Xem :pep:`585` và :ref:`types-genericalias`.

.. class:: Type(Generic[CT_co])

   Bí danh không còn được khuyến nghị cho :class:`type`.

   Xem :ref:`type-of-class-objects` để biết chi tiết về cách sử dụng :class:`type` hoặc ``typing.Type`` trong chú thích kiểu.

   .. versionadded:: 3.5.2

   .. deprecated:: 3.9
      :class:`builtins.type <type>` now supports subscripting (``[]``).
      Xem :pep:`585` và :ref:`types-genericalias`.

.. _corresponding-to-types-in-collections:

Bí danh cho các kiểu trong :mod:`collections`
"""""""""""""""""""""""""""""""""""""""""""""

.. class:: DefaultDict(collections.defaultdict, MutableMapping[KT, VT])

   Bí danh đã lỗi thời của :class:`collections.defaultdict`.

   .. versionadded:: 3.5.2

   .. deprecated:: 3.9
      :class:`collections.defaultdict` now supports subscripting (``[]``).
      Xem :pep:`585` và :ref:`types-genericalias`.

.. class:: OrderedDict(collections.OrderedDict, MutableMapping[KT, VT])

   Bí danh đã lỗi thời của :class:`collections.OrderedDict`.

   .. versionadded:: 3.7.2

   .. deprecated:: 3.9
      :class:`collections.OrderedDict` now supports subscripting (``[]``).
      Xem :pep:`585` và :ref:`types-genericalias`.

.. class:: ChainMap(collections.ChainMap, MutableMapping[KT, VT])

   Bí danh đã lỗi thời của :class:`collections.ChainMap`.

   .. versionadded:: 3.6.1

   .. deprecated:: 3.9
      :class:`collections.ChainMap` now supports subscripting (``[]``).
      Xem :pep:`585` và :ref:`types-genericalias`.

.. class:: Counter(collections.Counter, Dict[T, int])

   Bí danh đã lỗi thời của :class:`collections.Counter`.

   .. versionadded:: 3.6.1

   .. deprecated:: 3.9
      :class:`collections.Counter` now supports subscripting (``[]``).
      Xem :pep:`585` và :ref:`types-genericalias`.

.. class:: Deque(deque, MutableSequence[T])

   Bí danh không còn được khuyến nghị cho :class:`collections.deque`.

   .. versionadded:: 3.6.1

   .. deprecated:: 3.9
      :class:`collections.deque` now supports subscripting (``[]``).
      Xem :pep:`585` và :ref:`types-genericalias`.

.. _other-concrete-types:

Bí danh cho các kiểu cụ thể khác
""""""""""""""""""""""""""""""""

.. class:: Pattern
           Match

   Các bí danh không còn được khuyến nghị tương ứng với các kiểu trả về từ
   :func:`re.compile` và :func:`re.match`.

   Các kiểu này (và các hàm tương ứng) được tổng quát theo
   :data:`AnyStr`. ``Pattern`` có thể được chuyên biệt hóa thành ``Pattern[str]`` hoặc ``Pattern[bytes]``; ``Match`` có thể được chuyên biệt hóa thành ``Match[str]`` hoặc ``Match[bytes]``.

   .. deprecated:: 3.9
      Các lớp ``Pattern`` và ``Match`` từ :mod:`re` hiện hỗ trợ ``[]``. Xem :pep:`585` và :ref:`types-genericalias`.

.. class:: Text

   Bí danh đã lỗi thời cho :class:`str`.

   ``Text`` được cung cấp để tạo ra một hướng tương thích về sau cho mã Python 2: trong Python 2, ``Text`` là bí danh cho ``unicode``.

   Sử dụng ``Text`` để cho biết rằng một giá trị phải chứa chuỗi unicode theo cách tương thích với cả Python 2 và Python 3::

       def add_unicode_checkmark(text: Text) -> Text:
           return text + u' \u2713'

   .. versionadded:: 3.5.2

   .. deprecated:: 3.11
      Python 2 không còn được hỗ trợ và hầu hết các trình kiểm tra kiểu cũng không còn hỗ trợ kiểm tra kiểu mã Python 2. Hiện chưa có kế hoạch loại bỏ bí danh này, nhưng người dùng được khuyến khích sử dụng
      :class:`str` thay cho ``Text``.

.. _abstract-base-classes:
.. _corresponding-to-collections-in-collections-abc:

Các bí danh cho ABC container trong :mod:`collections.abc`
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. class:: AbstractSet(Collection[T_co])

   Bí danh không còn được khuyến nghị cho :class:`collections.abc.Set`.

   .. deprecated:: 3.9
      :class:`collections.abc.Set` now supports subscripting (``[]``).
      Xem :pep:`585` và :ref:`types-genericalias`.

.. class:: ByteString(Sequence[int])

   Bí danh không còn được khuyến nghị cho :class:`collections.abc.ByteString`.

   Sử dụng ``isinstance(obj, collections.abc.Buffer)`` để kiểm tra tại runtime xem ``obj`` có triển khai :ref:`giao thức buffer <bufferobjects>` hay không. Khi dùng trong type annotation, hãy sử dụng :class:`~collections.abc.Buffer` hoặc một union chỉ định rõ các kiểu mà mã của bạn hỗ trợ (ví dụ: ``bytes | bytearray | memoryview``).

   :class:`!ByteString` ban đầu được dự định là một lớp trừu tượng đóng vai trò là siêu kiểu của cả :class:`bytes` và :class:`bytearray`. Tuy nhiên, vì ABC này chưa bao giờ có phương thức nào, việc biết một đối tượng là một thể hiện của :class:`!ByteString` thực sự không cho bạn biết điều gì hữu ích về đối tượng đó. Các kiểu buffer phổ biến khác như :class:`memoryview` cũng chưa bao giờ được hiểu là kiểu con của :class:`!ByteString` (dù ở runtime hay bởi các trình kiểm tra kiểu tĩnh).

   Xem :pep:`PEP 688 <688#current-options>` để biết thêm chi tiết.

   .. deprecated-removed:: 3.9 3.17

.. class:: Collection(Sized, Iterable[T_co], Container[T_co])

   Bí danh đã lỗi thời của :class:`collections.abc.Collection`.

   .. versionadded:: 3.6

   .. deprecated:: 3.9
      :class:`collections.abc.Collection` now supports subscripting (``[]``).
      Xem :pep:`585` và :ref:`types-genericalias`.

.. class:: Container(Generic[T_co])

   Bí danh đã lỗi thời của :class:`collections.abc.Container`.

   .. deprecated:: 3.9
      :class:`collections.abc.Container` now supports subscripting (``[]``).
      Xem :pep:`585` và :ref:`types-genericalias`.

.. class:: ItemsView(MappingView, AbstractSet[tuple[KT_co, VT_co]])

   Bí danh đã lỗi thời của :class:`collections.abc.ItemsView`.

   .. deprecated:: 3.9
      :class:`collections.abc.ItemsView` now supports subscripting (``[]``).
      Xem :pep:`585` và :ref:`types-genericalias`.

.. class:: KeysView(MappingView, AbstractSet[KT_co])

   Bí danh không còn được khuyến nghị dùng cho :class:`collections.abc.KeysView`.

   .. deprecated:: 3.9
      :class:`collections.abc.KeysView` now supports subscripting (``[]``).
      Xem :pep:`585` và :ref:`types-genericalias`.

.. class:: Mapping(Collection[KT], Generic[KT, VT_co])

   Bí danh không còn được khuyến nghị dùng cho :class:`collections.abc.Mapping`.

   .. deprecated:: 3.9
      :class:`collections.abc.Mapping` now supports subscripting (``[]``).
      Xem :pep:`585` và :ref:`types-genericalias`.

.. class:: MappingView(Sized)

   Bí danh không còn được khuyến nghị dùng cho :class:`collections.abc.MappingView`.

   .. deprecated:: 3.9
      :class:`collections.abc.MappingView` now supports subscripting (``[]``).
      Xem :pep:`585` và :ref:`types-genericalias`.

.. class:: MutableMapping(Mapping[KT, VT])

   Bí danh không còn được khuyến nghị dùng cho :class:`collections.abc.MutableMapping`.

   .. deprecated:: 3.9
      :class:`collections.abc.MutableMapping`
      hiện hỗ trợ phép lập chỉ mục (``[]``). Xem :pep:`585` và :ref:`types-genericalias`.

.. class:: MutableSequence(Sequence[T])

   Bí danh đã lỗi thời của :class:`collections.abc.MutableSequence`.

   .. deprecated:: 3.9
      :class:`collections.abc.MutableSequence`
      hiện hỗ trợ phép lập chỉ mục (``[]``). Xem :pep:`585` và :ref:`types-genericalias`.

.. class:: MutableSet(AbstractSet[T])

   Bí danh đã lỗi thời của :class:`collections.abc.MutableSet`.

   .. deprecated:: 3.9
      :class:`collections.abc.MutableSet` now supports subscripting (``[]``).
      Xem :pep:`585` và :ref:`types-genericalias`.

.. class:: Sequence(Reversible[T_co], Collection[T_co])

   Bí danh đã lỗi thời của :class:`collections.abc.Sequence`.

   .. deprecated:: 3.9
      :class:`collections.abc.Sequence` now supports subscripting (``[]``).
      Xem :pep:`585` và :ref:`types-genericalias`.

.. class:: ValuesView(MappingView, Collection[_VT_co])

   Bí danh không còn được khuyến nghị cho :class:`collections.abc.ValuesView`.

   .. deprecated:: 3.9
      :class:`collections.abc.ValuesView` now supports subscripting (``[]``).
      Xem :pep:`585` và :ref:`types-genericalias`.

.. _asynchronous-programming:

Các bí danh cho ABC bất đồng bộ trong :mod:`collections.abc`
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. class:: Coroutine(Awaitable[ReturnType], Generic[YieldType, SendType, ReturnType])

   Bí danh không còn được khuyến nghị cho :class:`collections.abc.Coroutine`.

   Xem :ref:`annotating-generators-and-coroutines` để biết chi tiết về cách sử dụng :class:`collections.abc.Coroutine` và ``typing.Coroutine`` trong chú thích kiểu.

   .. versionadded:: 3.5.3

   .. deprecated:: 3.9
      :class:`collections.abc.Coroutine` now supports subscripting (``[]``).
      Xem :pep:`585` và :ref:`types-genericalias`.

.. class:: AsyncGenerator(AsyncIterator[YieldType], Generic[YieldType, SendType])

   Bí danh không còn được khuyến nghị cho :class:`collections.abc.AsyncGenerator`.

   Xem :ref:`annotating-generators-and-coroutines` để biết chi tiết về cách sử dụng :class:`collections.abc.AsyncGenerator` và ``typing.AsyncGenerator`` trong các chú thích kiểu.

   .. versionadded:: 3.6.1

   .. deprecated:: 3.9
      :class:`collections.abc.AsyncGenerator`
      hiện hỗ trợ phép lập chỉ mục (``[]``). Xem :pep:`585` và :ref:`types-genericalias`.

   .. versionchanged:: 3.13
      Tham số ``SendType`` hiện có giá trị mặc định.

.. class:: AsyncIterable(Generic[T_co])

   Bí danh đã lỗi thời của :class:`collections.abc.AsyncIterable`.

   .. versionadded:: 3.5.2

   .. deprecated:: 3.9
      :class:`collections.abc.AsyncIterable` now supports subscripting (``[]``).
      Xem :pep:`585` và :ref:`types-genericalias`.

.. class:: AsyncIterator(AsyncIterable[T_co])

   Bí danh đã lỗi thời của :class:`collections.abc.AsyncIterator`.

   .. versionadded:: 3.5.2

   .. deprecated:: 3.9
      :class:`collections.abc.AsyncIterator` now supports subscripting (``[]``).
      Xem :pep:`585` và :ref:`types-genericalias`.

.. class:: Awaitable(Generic[T_co])

   Bí danh không còn được khuyến nghị cho :class:`collections.abc.Awaitable`.

   .. versionadded:: 3.5.2

   .. deprecated:: 3.9
      :class:`collections.abc.Awaitable` now supports subscripting (``[]``).
      Xem :pep:`585` và :ref:`types-genericalias`.

.. _corresponding-to-other-types-in-collections-abc:

Bí danh cho các ABC khác trong :mod:`collections.abc`
"""""""""""""""""""""""""""""""""""""""""""""""""""""

.. class:: Iterable(Generic[T_co])

   Bí danh không còn được khuyến nghị cho :class:`collections.abc.Iterable`.

   .. deprecated:: 3.9
      :class:`collections.abc.Iterable` now supports subscripting (``[]``).
      Xem :pep:`585` và :ref:`types-genericalias`.

.. class:: Iterator(Iterable[T_co])

   Bí danh không còn được khuyến nghị cho :class:`collections.abc.Iterator`.

   .. deprecated:: 3.9
      :class:`collections.abc.Iterator` now supports subscripting (``[]``).
      Xem :pep:`585` và :ref:`types-genericalias`.

.. data:: Callable

   Bí danh không được khuyến nghị cho :class:`collections.abc.Callable`.

   Xem :ref:`annotating-callables` để biết chi tiết về cách sử dụng
   :class:`collections.abc.Callable` và ``typing.Callable`` trong chú thích kiểu.

   .. deprecated:: 3.9
      :class:`collections.abc.Callable` now supports subscripting (``[]``).
      Xem :pep:`585` và :ref:`types-genericalias`.

   .. versionchanged:: 3.10
      ``Callable`` hiện hỗ trợ :class:`ParamSpec` và :data:`Concatenate`. Xem :pep:`612` để biết thêm chi tiết.

.. class:: Generator(Iterator[YieldType], Generic[YieldType, SendType, ReturnType])

   Bí danh không được khuyến nghị cho :class:`collections.abc.Generator`.

   Xem :ref:`annotating-generators-and-coroutines` để biết chi tiết về cách sử dụng :class:`collections.abc.Generator` và ``typing.Generator`` trong chú thích kiểu.

   .. deprecated:: 3.9
      :class:`collections.abc.Generator` now supports subscripting (``[]``).
      Xem :pep:`585` và :ref:`types-genericalias`.

   .. versionchanged:: 3.13
      Các giá trị mặc định cho kiểu send và return đã được thêm.

.. class:: Hashable

   Bí danh không còn được khuyến nghị cho :class:`collections.abc.Hashable`.

   .. deprecated:: 3.12
      Thay vào đó, hãy sử dụng trực tiếp :class:`collections.abc.Hashable`.

.. class:: Reversible(Iterable[T_co])

   Bí danh không còn được khuyến nghị cho :class:`collections.abc.Reversible`.

   .. deprecated:: 3.9
      :class:`collections.abc.Reversible` now supports subscripting (``[]``).
      Xem :pep:`585` và :ref:`types-genericalias`.

.. class:: Sized

   Bí danh không còn được khuyến nghị cho :class:`collections.abc.Sized`.

   .. deprecated:: 3.12
      Thay vào đó, hãy sử dụng :class:`collections.abc.Sized` trực tiếp.

.. _context-manager-types:

Bí danh cho các ABC :mod:`contextlib`
"""""""""""""""""""""""""""""""""""""

.. class:: ContextManager(Generic[T_co, ExitT_co])

   Bí danh đã lỗi thời cho :class:`contextlib.AbstractContextManager`.

   Tham số kiểu đầu tiên, ``T_co``, đại diện cho kiểu được phương thức :meth:`~object.__enter__` trả về. Tham số kiểu thứ hai tùy chọn, ``ExitT_co``, mặc định là ``bool | None``, đại diện cho kiểu được
   phương thức :meth:`~object.__exit__` trả về.

   .. versionadded:: 3.5.4

   .. deprecated:: 3.9
      :class:`contextlib.AbstractContextManager`
      hiện hỗ trợ phép tham số hóa bằng chỉ số (``[]``). Xem :pep:`585` và :ref:`types-genericalias`.

   .. versionchanged:: 3.13
      Đã thêm tham số kiểu thứ hai tùy chọn, ``ExitT_co``.

.. class:: AsyncContextManager(Generic[T_co, AExitT_co])

   Bí danh đã ngừng sử dụng cho :class:`contextlib.AbstractAsyncContextManager`.

   Tham số kiểu đầu tiên, ``T_co``, đại diện cho kiểu được trả về bởi phương thức :meth:`~object.__aenter__`. Tham số kiểu thứ hai tùy chọn, ``AExitT_co``, có giá trị mặc định là ``bool | None``, đại diện cho kiểu được trả về bởi
   phương thức :meth:`~object.__aexit__`.

   .. versionadded:: 3.6.2

   .. deprecated:: 3.9
      :class:`contextlib.AbstractAsyncContextManager`
      hiện hỗ trợ phép tham số hóa bằng chỉ số (``[]``). Xem :pep:`585` và :ref:`types-genericalias`.

   .. versionchanged:: 3.13
      Đã thêm tham số kiểu thứ hai tùy chọn, ``AExitT_co``.

Lộ trình ngừng sử dụng các tính năng chính
==========================================

Một số tính năng trong ``typing`` đã ngừng sử dụng và có thể bị xóa trong phiên bản Python tương lai. Bảng sau đây tóm tắt các tính năng chính đã ngừng sử dụng để bạn tiện tham khảo. Nội dung này có thể thay đổi và không phải tất cả các tính năng đã ngừng sử dụng đều được liệt kê.

.. list-table::
   :header-rows: 1

   * - Tính năng
     - Không dùng nữa từ
     - Dự kiến loại bỏ
     - PEP/issue
   * - ``typing`` phiên bản của các collection chuẩn
     - 3.9
     - Chưa quyết định (xem :ref:`deprecated-aliases` để biết thêm thông tin)
     - :pep:`585`
   * - :class:`typing.ByteString`
     - 3.9
     - 3.17
     - :gh:`91896`
   * - :data:`typing.Text`
     - 3.11
     - Chưa quyết định
     - :gh:`92332`
   * - :class:`typing.Hashable` và :class:`typing.Sized`
     - 3.12
     - Chưa quyết định
     - :gh:`94309`
   * - :data:`typing.TypeAlias`
     - 3.12
     - Chưa quyết định
     - :pep:`695`
   * - :func:`@typing.no_type_check_decorator <no_type_check_decorator>`
     - 3.13
     - 3.15
     - :gh:`106309`
   * - :data:`typing.AnyStr`
     - 3.13
     - 3.18
     - :gh:`105578`

.. _`Typing cheat sheet`: https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
.. _`the mypy docs`: https://mypy.readthedocs.io/en/stable/index.html
.. _`Static Typing with Python`: https://typing.python.org/en/latest/
.. _`Specification for the Python type system`: https://typing.python.org/en/latest/spec/index.html
.. _`bottom type`: https://en.wikipedia.org/wiki/Bottom_type
.. _`TypedDict`: https://typing.python.org/en/latest/spec/typeddict.html#typeddict
