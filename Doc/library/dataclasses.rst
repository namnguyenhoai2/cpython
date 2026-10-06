:mod:`!dataclasses` --- Các lớp dữ liệu
=======================================

.. module:: dataclasses
    :synopsis: Tạo các phương thức đặc biệt trên các lớp do người dùng định nghĩa.

.. moduleauthor:: Eric V. Smith <eric@trueblade.com>
.. sectionauthor:: Eric V. Smith <eric@trueblade.com>

**Mã nguồn:** :source:`Lib/dataclasses.py`

--------------

Mô-đun này cung cấp một decorator và các hàm để tự động thêm các :term:`phương thức đặc biệt <special method>` được sinh tự động, chẳng hạn như :meth:`~object.__init__` và
:meth:`~object.__repr__` vào các lớp do người dùng định nghĩa.  Mô-đun này ban đầu được mô tả trong :pep:`557`.

Các biến thành viên được sử dụng trong những phương thức được sinh tự động này được định nghĩa bằng :pep:`526` chú thích kiểu (type annotation).  Ví dụ: đoạn mã này::

  from dataclasses import dataclass

  @dataclass
  class InventoryItem:
      """Class for keeping track of an item in inventory."""
      name: str
      unit_price: float
      quantity_on_hand: int = 0

      def total_cost(self) -> float:
          return self.unit_price * self.quantity_on_hand

sẽ thêm, cùng với nhiều thành phần khác, một :meth:`!__init__` có dạng như sau::

  def __init__(self, name: str, unit_price: float, quantity_on_hand: int = 0):
      self.name = name
      self.unit_price = unit_price
      self.quantity_on_hand = quantity_on_hand

Lưu ý rằng phương thức này được tự động thêm vào class: phương thức này không được chỉ định trực tiếp trong định nghĩa :class:`!InventoryItem` được trình bày ở trên.

.. versionadded:: 3.7

Nội dung module
---------------

.. decorator:: dataclass(*, init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False, match_args=True, kw_only=False, slots=False, weakref_slot=False)

   Hàm này là một :term:`decorator` được dùng để thêm các
   :term:`phương thức đặc biệt <special method>` được tạo tự động vào các class, như mô tả bên dưới.

   Decorator ``@dataclass`` kiểm tra class để tìm ``field``\s.  Một ``field`` được định nghĩa là một biến class có một
   :term:`chú thích kiểu <variable annotation>`.  Ngoại trừ hai trường hợp được mô tả bên dưới, không có thành phần nào trong ``@dataclass`` kiểm tra kiểu được chỉ định trong chú thích biến.

   Thứ tự của các field trong tất cả các phương thức được tạo tự động là thứ tự mà chúng xuất hiện trong định nghĩa class.

   Trình trang trí ``@dataclass`` sẽ thêm nhiều phương thức "dunder" khác nhau vào lớp, được mô tả bên dưới. Nếu bất kỳ phương thức nào được thêm đã tồn tại trong lớp, hành vi sẽ phụ thuộc vào tham số, như được ghi lại bên dưới. Trình trang trí trả về chính lớp mà nó được gọi trên đó; không tạo lớp mới.

   Nếu ``@dataclass`` được sử dụng chỉ như một trình trang trí đơn giản không có tham số, nó hoạt động như thể có các giá trị mặc định được ghi lại trong chữ ký này. Nghĩa là, ba cách sử dụng ``@dataclass`` sau đây là tương đương::

     @dataclass
     class C:
         ...

     @dataclass()
     class C:
         ...

     @dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False,
                match_args=True, kw_only=False, slots=False, weakref_slot=False)
     class C:
         ...

   Các tham số của ``@dataclass`` là:

   - *init*: Nếu là true (mặc định), một phương thức :meth:`~object.__init__` sẽ được tạo.

     Nếu lớp đã định nghĩa :meth:`!__init__`, tham số này sẽ bị bỏ qua.

   - *repr*: Nếu là true (mặc định), một phương thức :meth:`~object.__repr__` sẽ được tạo. Chuỗi repr được tạo sẽ có tên lớp, cùng tên và repr của từng trường, theo thứ tự chúng được định nghĩa trong lớp. Các trường được đánh dấu là loại trừ khỏi repr sẽ không được đưa vào. Ví dụ: ``InventoryItem(name='widget', unit_price=3.0, quantity_on_hand=10)``.

     Nếu lớp đã định nghĩa :meth:`!__repr__`, tham số này sẽ bị bỏ qua.

   - *eq*: Nếu là true (mặc định), một phương thức :meth:`~object.__eq__` sẽ được tạo.

     Phương thức này so sánh lớp bằng cách lần lượt so sánh từng trường. Hai đối tượng trong phép so sánh phải có cùng kiểu.

     Nếu lớp đã định nghĩa :meth:`!__eq__`, tham số này sẽ bị bỏ qua.

     .. versionchanged:: 3.13
        Phương thức ``__eq__`` được tạo giờ đây sẽ so sánh từng trường riêng lẻ (ví dụ: ``self.a == other.a and self.b == other.b``), thay vì so sánh các tuple trường như trong những phiên bản trước.

        Thay đổi này giúp phép so sánh nhanh hơn, nhưng có thể làm thay đổi kết quả trong những trường hợp các thuộc tính so sánh bằng nhau theo identity nhưng không bằng nhau theo value (chẳng hạn như ``float('nan')``).

        Trong Python 3.12 và các phiên bản trước đó, phép so sánh được thực hiện bằng cách tạo các tuple từ các trường rồi so sánh chúng (ví dụ: ``(self.a, self.b) == (other.a, other.b)``).

   - *order*: Nếu là true (mặc định là ``False``), :meth:`~object.__lt__`,
     :meth:`~object.__le__`, :meth:`~object.__gt__`, và :meth:`~object.__ge__` sẽ được tạo. Các phương thức này so sánh lớp như thể đó là một tuple gồm các trường của lớp, theo thứ tự. Cả hai instance trong phép so sánh phải có cùng một kiểu hoàn toàn. Nếu *order* là true và *eq* là false, sẽ phát sinh một
     :exc:`ValueError`.

     Nếu lớp đã định nghĩa bất kỳ phương thức nào trong số :meth:`!__lt__`,
     :meth:`!__le__`, :meth:`!__gt__`, hoặc :meth:`!__ge__`, thì
     :exc:`TypeError` sẽ được phát sinh.

   - *unsafe_hash*: Nếu là true, buộc ``dataclasses`` tạo một
     :meth:`~object.__hash__` method, ngay cả khi việc này có thể không an toàn. Nếu không, hãy tạo một phương thức :meth:`~object.__hash__` theo cách *eq* và *frozen* được thiết lập. Giá trị mặc định là ``False``.

     :meth:`!__hash__` được :meth:`hash` tích hợp sẵn sử dụng, cũng như khi các đối tượng được thêm vào những tập hợp băm như dictionary và set. Việc có một
     :meth:`!__hash__` ngụ ý rằng các thực thể của lớp là bất biến. Tính khả biến là một thuộc tính phức tạp, phụ thuộc vào ý định của lập trình viên, sự tồn tại và hành vi của :meth:`!__eq__`, cũng như giá trị của các cờ *eq* và *frozen* trong decorator ``@dataclass``.

     Theo mặc định, ``@dataclass`` sẽ không tự động thêm một phương thức :meth:`~object.__hash__` trừ khi việc đó an toàn. Nó cũng sẽ không thêm hoặc thay đổi một phương thức :meth:`!__hash__` hiện có được định nghĩa tường minh. Việc đặt thuộc tính lớp ``__hash__ = None`` mang một ý nghĩa cụ thể đối với Python, như được mô tả trong tài liệu :meth:`!__hash__`.

     Nếu :meth:`!__hash__` không được định nghĩa tường minh, hoặc được đặt thành ``None``, thì ``@dataclass`` *có thể* thêm một phương thức :meth:`!__hash__` ngầm định. Mặc dù không được khuyến nghị, bạn có thể buộc ``@dataclass`` tạo một
     phương thức :meth:`!__hash__` với ``unsafe_hash=True``. Trường hợp này có thể xảy ra nếu lớp của bạn về mặt logic là bất biến nhưng vẫn có thể bị thay đổi. Đây là một trường hợp sử dụng chuyên biệt và cần được cân nhắc cẩn thận.

     Sau đây là các quy tắc chi phối việc tạo ngầm định một phương thức :meth:`!__hash__`. Lưu ý rằng bạn không thể vừa có một phương thức :meth:`!__hash__` tường minh trong dataclass vừa đặt ``unsafe_hash=True``; điều này sẽ dẫn đến một :exc:`TypeError`.

     Nếu cả *eq* và *frozen* đều là true, theo mặc định ``@dataclass`` sẽ tạo một phương thức :meth:`!__hash__` cho bạn. Nếu *eq* là true và *frozen* là false, :meth:`!__hash__` sẽ được đặt thành ``None``, đánh dấu nó là không thể băm (đúng như vậy, vì nó có thể thay đổi). Nếu *eq* là false,
     :meth:`!__hash__` sẽ được giữ nguyên, nghĩa là phương thức :meth:`!__hash__` của superclass sẽ được sử dụng (nếu superclass là
     :class:`object`, điều này có nghĩa là sẽ chuyển sang băm dựa trên id).

   - *frozen*: Nếu là true (mặc định là ``False``), việc gán cho các trường sẽ tạo ra một exception. Điều này mô phỏng các instance frozen chỉ đọc. Xem :ref:`phần thảo luận <dataclasses-frozen>` bên dưới.

     Nếu :meth:`~object.__setattr__` hoặc :meth:`~object.__delattr__` được định nghĩa trong class và *frozen* là true, thì :exc:`TypeError` sẽ được tạo ra.

   - *match_args*: Nếu là true (mặc định là ``True``),
     :attr:`~object.__match_args__` tuple sẽ được tạo từ danh sách các tham số không chỉ định bằng keyword-only của phương thức :meth:`~object.__init__` được tạo tự động (ngay cả khi
     :meth:`!__init__` không được tạo, xem ở trên). Nếu là false, hoặc nếu
     Nếu :attr:`!__match_args__` đã được định nghĩa trong class thì
     :attr:`!__match_args__` sẽ không được tạo.

    .. versionadded:: 3.10

   - *kw_only*: Nếu là true (giá trị mặc định là ``False``), thì tất cả các field sẽ được đánh dấu là keyword-only. Nếu một field được đánh dấu là keyword-only, thì hiệu ứng duy nhất là tham số :meth:`~object.__init__` được tạo từ field keyword-only phải được chỉ định bằng một keyword khi gọi :meth:`!__init__`. Xem mục :term:`parameter` trong bảng thuật ngữ để biết chi tiết. Đồng thời xem phần
     :const:`KW_ONLY`.

     Các field keyword-only không được đưa vào :attr:`!__match_args__`.

    .. versionadded:: 3.10

   - *slots*: Nếu là true (mặc định là ``False``), thuộc tính :attr:`~object.__slots__` sẽ được tạo và một class mới sẽ được trả về thay cho class ban đầu. Nếu :attr:`!__slots__` đã được định nghĩa trong class thì :exc:`TypeError` sẽ được phát sinh.

    .. warning::
       Việc truyền các tham số cho :meth:`~object.__init_subclass__` của một base class khi sử dụng ``slots=True`` sẽ dẫn đến :exc:`TypeError`. Để khắc phục, hãy sử dụng ``__init_subclass__`` không có tham số hoặc sử dụng các giá trị mặc định. Xem :gh:`91126` để biết đầy đủ chi tiết.

    .. versionadded:: 3.10

    .. versionchanged:: 3.11
       Nếu tên trường đã được bao gồm trong :attr:`!__slots__` của một lớp cơ sở, tên đó sẽ không được bao gồm trong :attr:`!__slots__` được tạo ra để ngăn :ref:`ghi đè chúng <datamodel-note-slots>`. Do đó, không sử dụng :attr:`!__slots__` để lấy tên các trường của một dataclass. Thay vào đó, hãy sử dụng :func:`fields`. Để có thể xác định các slot được kế thừa, :attr:`!__slots__` của lớp cơ sở có thể là bất kỳ iterable nào, nhưng *không được là* một iterator.


   - *weakref_slot*: Nếu là true (mặc định là ``False``), thêm một slot có tên "__weakref__", vốn cần thiết để làm cho một instance
     :func:`weakref-able <weakref.ref>`. Việc chỉ định ``weakref_slot=True`` mà không đồng thời chỉ định ``slots=True`` là một lỗi.

    .. versionadded:: 3.11

   ``field``\s có thể tùy chọn chỉ định một giá trị mặc định bằng cú pháp Python thông thường::

     @dataclass
     class C:
         a: int       # 'a' không có giá trị mặc định
         b: int = 0   # gán giá trị mặc định cho 'b'

   Trong ví dụ này, cả :attr:`!a` và :attr:`!b` đều sẽ được đưa vào phần được thêm vào
   phương thức :meth:`~object.__init__`, được định nghĩa là::

     def __init__(self, a: int, b: int = 0):

   :exc:`TypeError` sẽ được phát sinh nếu một trường không có giá trị mặc định đứng sau một trường có giá trị mặc định. Điều này đúng cho dù xảy ra trong một lớp đơn lẻ hay do kế thừa lớp.

.. function:: field(*, default=MISSING, default_factory=MISSING, init=True, repr=True, hash=None, compare=True, metadata=None, kw_only=MISSING, doc=None)

   Đối với các trường hợp sử dụng phổ biến và đơn giản, không cần thêm chức năng nào khác. Tuy nhiên, có một số tính năng của dataclass yêu cầu thông tin bổ sung cho từng trường. Để đáp ứng nhu cầu về thông tin bổ sung này, bạn có thể thay thế giá trị mặc định của trường bằng một lệnh gọi đến hàm :func:`!field` được cung cấp. Ví dụ::

     @dataclass
     class C:
         mylist: list[int] = field(default_factory=list)

     c = C()
     c.mylist += [1, 2, 3]

   Như đã trình bày ở trên, giá trị :const:`MISSING` là một đối tượng sentinel được dùng để phát hiện xem người dùng có cung cấp một số tham số hay không. Sentinel này được sử dụng vì ``None`` là một giá trị hợp lệ đối với một số tham số và có ý nghĩa riêng. Không mã nào được sử dụng trực tiếp giá trị :const:`MISSING`.

   Các tham số của :func:`!field` là:

   - *default*: Nếu được cung cấp, đây sẽ là giá trị mặc định cho trường này. Điều này là cần thiết vì lệnh gọi :func:`!field` tự nó thay thế vị trí thông thường của giá trị mặc định.

   - *default_factory*: Nếu được cung cấp, đây phải là một callable không có đối số, sẽ được gọi khi cần một giá trị mặc định cho trường này. Ngoài các mục đích khác, nó có thể được dùng để chỉ định các trường có giá trị mặc định có thể thay đổi, như thảo luận bên dưới. Việc chỉ định đồng thời *default* và *default_factory* là một lỗi.

   - *init*: Nếu là true (giá trị mặc định), trường này được đưa vào làm tham số cho phương thức :meth:`~object.__init__` được tạo tự động.

   - *repr*: Nếu là true (giá trị mặc định), trường này được đưa vào chuỗi được phương thức :meth:`~object.__repr__` được tạo tự động trả về.

   - *hash*: Giá trị này có thể là bool hoặc ``None``. Nếu là true, trường này được đưa vào phương thức :meth:`~object.__hash__` được tạo tự động. Nếu là false, trường này bị loại khỏi :meth:`~object.__hash__` được tạo tự động. Nếu là ``None`` (giá trị mặc định), hãy sử dụng giá trị của *compare*: đây thường là hành vi được mong đợi, vì một trường nên được đưa vào hash nếu nó được dùng để so sánh. Không nên đặt giá trị này thành bất kỳ giá trị nào khác ngoài ``None``.

     Một lý do có thể để đặt ``hash=False`` nhưng ``compare=True`` là khi việc tính giá trị hash cho một trường tốn nhiều chi phí, trường đó cần thiết cho việc kiểm tra tính bằng nhau và có các trường khác góp phần vào giá trị hash của kiểu. Ngay cả khi một trường bị loại khỏi hash, trường đó vẫn được dùng để so sánh.

   - *compare*: Nếu là true (giá trị mặc định), trường này được đưa vào các phương thức kiểm tra tính bằng nhau và so sánh được tạo tự động (:meth:`~object.__eq__`,
     :meth:`~object.__gt__`, v.v.).

   - *metadata*: Giá trị này có thể là một mapping hoặc ``None``. ``None`` được xử lý như một dict rỗng. Giá trị này được bọc trong
     :func:`~types.MappingProxyType` để biến nó thành chỉ đọc và được cung cấp trên đối tượng :class:`Field`. Data Classes hoàn toàn không sử dụng nó; nó được cung cấp như một cơ chế mở rộng của bên thứ ba. Nhiều bên thứ ba có thể có khóa riêng, dùng khóa đó làm namespace trong metadata.

   - *kw_only*: Nếu là true, trường này sẽ được đánh dấu là chỉ nhận đối số từ khóa. Điều này được sử dụng khi các tham số của phương thức :meth:`~object.__init__` được tạo được tính toán.

     Các trường chỉ nhận đối số từ khóa cũng không được đưa vào :attr:`!__match_args__`.

    .. versionadded:: 3.10

   - *doc*: docstring tùy chọn cho trường này.

    .. versionadded:: 3.14

   Nếu giá trị mặc định của một trường được chỉ định bằng một lệnh gọi đến
   :func:`!field`, thì thuộc tính lớp của trường này sẽ được thay thế bằng giá trị *default* được chỉ định. Nếu *default* không được cung cấp, thuộc tính lớp sẽ bị xóa. Mục đích là sau khi decorator :deco:`dataclass` chạy, tất cả thuộc tính lớp sẽ chứa các giá trị mặc định cho những trường tương ứng, giống như khi tự chỉ định giá trị mặc định. Ví dụ, sau khi::

     @dataclass
     class C:
         x: int
         y: int = field(repr=False)
         z: int = field(repr=False, default=10)
         t: int = 20

   Thuộc tính lớp :attr:`!C.z` sẽ là ``10``, còn thuộc tính lớp
   :attr:`!C.t` sẽ là ``20``, và các thuộc tính lớp :attr:`!C.x` cùng
   :attr:`!C.y` sẽ không được thiết lập.

.. class:: Field

   Các đối tượng :class:`!Field` mô tả từng trường được định nghĩa. Các đối tượng này được tạo nội bộ và được trả về bởi phương thức cấp mô-đun :func:`fields` (xem bên dưới). Người dùng không bao giờ nên khởi tạo một
   đối tượng :class:`!Field` trực tiếp. Các thuộc tính được tài liệu hóa của nó là:

   - :attr:`!name`: Tên của trường.
   - :attr:`!type`: Kiểu của trường.
   - :attr:`!default`, :attr:`!default_factory`, :attr:`!init`, :attr:`!repr`, :attr:`!hash`,
     :attr:`!compare`, :attr:`!metadata` và :attr:`!kw_only` có ý nghĩa và giá trị giống hệt như trong hàm :func:`field`.

   Có thể tồn tại các thuộc tính khác, nhưng chúng là thuộc tính private và không được kiểm tra hoặc dựa vào.

.. class:: InitVar

   ``InitVar[T]`` Các chú thích kiểu mô tả những biến là :ref:`init-only <dataclasses-init-only-variables>`. Các trường được chú thích bằng :class:`!InitVar` được xem là pseudo-field, vì vậy không được hàm
   :func:`fields` trả về và không được sử dụng theo bất kỳ cách nào, ngoại trừ việc thêm chúng làm tham số cho :meth:`~object.__init__` và một tùy chọn
   :meth:`__post_init__`.

.. function:: fields(class_or_instance)

   Trả về một tuple gồm các đối tượng :class:`Field` xác định những trường cho dataclass này. Chấp nhận một dataclass hoặc một instance của dataclass. Gây ra :exc:`TypeError` nếu đối số truyền vào không phải là dataclass hoặc instance của dataclass. Không trả về các pseudo-field là ``ClassVar`` hoặc ``InitVar``.

.. function:: asdict(obj, *, dict_factory=dict)

   Chuyển dataclass *obj* thành một dict (bằng cách sử dụng factory function *dict_factory*). Mỗi dataclass được chuyển thành một dict gồm các trường của nó dưới dạng các cặp ``name: value``. Các dataclass, dict, list và tuple được đệ quy. Các object khác được sao chép bằng
   :func:`copy.deepcopy`.

   Ví dụ sử dụng :func:`!asdict` với các dataclass lồng nhau::

     @dataclass
     class Point:
          x: int
          y: int

     @dataclass
     class C:
          mylist: list[Point]

     p = Point(10, 20)
     assert asdict(p) == {'x': 10, 'y': 20}

     c = C([Point(0, 0), Point(10, 4)])
     assert asdict(c) == {'mylist': [{'x': 0, 'y': 0}, {'x': 10, 'y': 4}]}

   Để tạo một bản sao nông, có thể sử dụng cách khắc phục sau::

     {field.name: getattr(obj, field.name) for field in fields(obj)}

   :func:`!asdict` tăng :exc:`TypeError` nếu *obj* không phải là một instance của dataclass.

.. function:: astuple(obj, *, tuple_factory=tuple)

   Chuyển dataclass *obj* thành một tuple (bằng cách sử dụng factory function *tuple_factory*). Mỗi dataclass được chuyển thành một tuple gồm các giá trị trường của nó. Các dataclass, dict, list và tuple được xử lý đệ quy. Các đối tượng khác được sao chép bằng
   :func:`copy.deepcopy`.

   Tiếp tục từ ví dụ trước::

     assert astuple(p) == (10, 20)
     assert astuple(c) == ([(0, 0), (10, 4)],)

   Để tạo một bản sao nông, có thể sử dụng cách khắc phục sau::

     tuple(getattr(obj, field.name) for field in dataclasses.fields(obj))

   :func:`!astuple` tăng :exc:`TypeError` nếu *obj* không phải là một instance của dataclass.

.. function:: make_dataclass(cls_name, fields, *, bases=(), namespace=None, init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False, match_args=True, kw_only=False, slots=False, weakref_slot=False, module=None, decorator=dataclass)

   Tạo một dataclass mới với tên *cls_name*, các trường được định nghĩa trong *fields*, các lớp cơ sở được cung cấp trong *bases*, và được khởi tạo với namespace được cung cấp trong *namespace*. *fields* là một iterable mà mỗi phần tử đều là ``name``, ``(name, type)`` hoặc ``(name, type, Field)``. Nếu chỉ cung cấp ``name``,
   :data:`typing.Any` được sử dụng cho ``type``. Các giá trị của *init*, *repr*, *eq*, *order*, *unsafe_hash*, *frozen*, *match_args*, *kw_only*, *slots* và *weakref_slot* có cùng ý nghĩa như trong :deco:`dataclass`.

   Nếu *module* được định nghĩa, thuộc tính :attr:`!__module__` của dataclass sẽ được đặt thành giá trị đó. Theo mặc định, thuộc tính này được đặt thành tên module của caller.

   Tham số *decorator* là một callable được dùng để tạo dataclass. Callable này phải nhận đối tượng class làm đối số đầu tiên và các keyword argument giống như :deco:`dataclass`. Theo mặc định, hàm :deco:`dataclass` được sử dụng.

   Hàm này không hoàn toàn bắt buộc, vì bất kỳ cơ chế Python nào để tạo một class mới với :attr:`~object.__annotations__` đều có thể áp dụng hàm :deco:`dataclass` để chuyển class đó thành dataclass. Hàm này được cung cấp nhằm thuận tiện. Ví dụ::

     C = make_dataclass('C',
                        [('x', int),
                          'y',
                         ('z', int, field(default=5))],
                        namespace={'add_one': lambda self: self.x + 1})

   Tương đương với::

     @dataclass
     class C:
         x: int
         y: 'typing.Any'
         z: int = 5

         def add_one(self):
             return self.x + 1

   .. versionadded:: 3.14
      Đã thêm tham số *decorator*.

.. function:: replace(obj, /, **changes)

   Tạo một đối tượng mới cùng kiểu với *obj*, thay thế các field bằng các giá trị từ *changes*. Nếu *obj* không phải là Data Class, sẽ phát sinh :exc:`TypeError`. Nếu các key trong *changes* không phải là tên field của dataclass đã cho, sẽ phát sinh :exc:`TypeError`.

   Đối tượng mới được trả về sẽ được tạo bằng cách gọi method :meth:`~object.__init__` của dataclass. Điều này đảm bảo rằng
   :meth:`__post_init__`, nếu có, cũng được gọi là.

   Các biến chỉ khởi tạo không có giá trị mặc định, nếu có, phải được chỉ định trong lệnh gọi :func:`!replace` để có thể được truyền cho
   :meth:`!__init__` và :meth:`__post_init__`.

   *changes* chứa bất kỳ trường nào được định nghĩa là có ``init=False`` là một lỗi. Trong trường hợp này, một :exc:`ValueError` sẽ được phát sinh.

   Hãy lưu ý về cách các trường ``init=False`` hoạt động trong một lệnh gọi đến
   :func:`!replace`. Chúng không được sao chép từ đối tượng nguồn mà được khởi tạo trong :meth:`__post_init__`, nếu chúng được khởi tạo. Các trường ``init=False`` được cho là sẽ hiếm khi được sử dụng và cần được sử dụng thận trọng. Nếu sử dụng chúng, có thể nên có các hàm khởi tạo lớp thay thế hoặc có thể là một phương thức :func:`!replace` (hoặc có tên tương tự) tùy chỉnh để xử lý việc sao chép instance.
   :func:`!replace` (hoặc có tên tương tự) để xử lý việc sao chép instance.

   Các instance của dataclass cũng được generic function :func:`copy.replace` hỗ trợ.

.. function:: is_dataclass(obj)

   Trả về ``True`` nếu tham số của nó là một dataclass (bao gồm các lớp con của một dataclass, nhưng không bao gồm :ref:`generic aliases <types-genericalias>`) hoặc một instance của dataclass, nếu không thì trả về ``False``.

   Nếu cần biết một class là một instance của dataclass (chứ không phải bản thân một dataclass), hãy thêm một kiểm tra nữa cho ``not isinstance(obj, type)``::

     def is_dataclass_instance(obj):
         return is_dataclass(obj) and not isinstance(obj, type)

.. data:: MISSING

   Một giá trị sentinel biểu thị default hoặc default_factory bị thiếu.

.. data:: KW_ONLY

   Một giá trị sentinel được dùng làm type annotation. Mọi field sau một pseudo-field có kiểu :const:`!KW_ONLY` đều được đánh dấu là keyword-only field. Lưu ý rằng một pseudo-field có kiểu
   :const:`!KW_ONLY` về cơ bản sẽ bị bỏ qua hoàn toàn. Điều này bao gồm cả tên của field đó. Theo quy ước, tên ``_`` được dùng cho một
   field :const:`!KW_ONLY`. Keyword-only field biểu thị
   các tham số :meth:`~object.__init__` phải được chỉ định dưới dạng từ khóa khi lớp được khởi tạo.

   Trong ví dụ này, các trường ``y`` và ``z`` sẽ được đánh dấu là các trường chỉ nhận từ khóa::

    @dataclass
    class Point:
        x: float
        _: KW_ONLY
        y: float
        z: float

    p = Point(0, y=1.5, z=2.0)

   Trong một dataclass, việc chỉ định nhiều hơn một trường có kiểu :const:`!KW_ONLY` sẽ gây ra lỗi.

   .. versionadded:: 3.10

.. exception:: FrozenInstanceError

   Được phát sinh khi :meth:`~object.__setattr__` được định nghĩa ngầm hoặc
   :meth:`~object.__delattr__` được gọi trên một dataclass được định nghĩa với ``frozen=True``. Đây là một lớp con của :exc:`AttributeError`.

.. _post-init-processing:

Xử lý sau khởi tạo
------------------

.. function:: __post_init__()

   Khi được định nghĩa trên lớp, nó sẽ được gọi bởi phần mã được tạo tự động
   :meth:`~object.__init__`, thường dưới dạng :meth:`!self.__post_init__`. Tuy nhiên, nếu có bất kỳ trường ``InitVar`` nào được định nghĩa, chúng cũng sẽ được truyền vào :meth:`!__post_init__` theo thứ tự được định nghĩa trong lớp.  Nếu không có phương thức :meth:`!__init__` nào được tạo, thì
   :meth:`!__post_init__` sẽ không được tự động gọi.

   Trong số các cách sử dụng khác, điều này cho phép khởi tạo các giá trị trường phụ thuộc vào một hoặc nhiều trường khác. Ví dụ::

     @dataclass
     class C:
         a: float
         b: float
         c: float = field(init=False)

         def __post_init__(self):
             self.c = self.a + self.b

Phương thức :meth:`~object.__init__` do :deco:`dataclass` tạo ra không gọi các phương thức :meth:`!__init__` của lớp cơ sở. Nếu lớp cơ sở có một phương thức :meth:`!__init__` cần được gọi, thông thường người ta sẽ gọi phương thức này trong một
phương thức :meth:`__post_init__`::

    class Rectangle:
        def __init__(self, height, width):
            self.height = height
            self.width = width

    @dataclass
    class Square(Rectangle):
        side: float

        def __post_init__(self):
            super().__init__(self.side, self.side)

Tuy nhiên, lưu ý rằng nhìn chung không cần gọi các phương thức :meth:`!__init__` do dataclass tạo ra, vì dataclass dẫn xuất sẽ đảm nhiệm việc khởi tạo tất cả các trường của bất kỳ lớp cơ sở nào vốn cũng là dataclass.

Xem phần bên dưới về các biến chỉ dùng cho init để biết cách truyền tham số cho :meth:`!__post_init__`. Đồng thời xem cảnh báo về cách
:func:`replace` xử lý các trường ``init=False``.

.. _dataclasses-class-variables:

Biến lớp
--------

Một trong số ít nơi :deco:`dataclass` thực sự kiểm tra kiểu của một trường là để xác định xem trường đó có phải là biến lớp như được định nghĩa trong :pep:`526` hay không. Nó thực hiện việc này bằng cách kiểm tra xem kiểu của trường có phải là
:data:`typing.ClassVar`. Nếu một trường là ``ClassVar``, trường đó sẽ bị loại khỏi việc xem xét như một trường và bị các cơ chế dataclass bỏ qua. Các trường giả ``ClassVar`` như vậy không được hàm cấp mô-đun :func:`fields` trả về.

.. _dataclasses-init-only-variables:

Biến chỉ dùng khi khởi tạo
--------------------------

Một nơi khác mà :deco:`dataclass` kiểm tra chú thích kiểu là để xác định xem một trường có phải là biến chỉ dùng khi khởi tạo hay không. Nó thực hiện việc này bằng cách kiểm tra xem kiểu của một trường có thuộc kiểu :class:`InitVar` hay không. Nếu một trường là :class:`InitVar`, trường đó được xem là một trường giả có tên là trường chỉ dùng khi khởi tạo. Vì không phải là một trường thực sự, trường này không được hàm cấp mô-đun :func:`fields` trả về. Các trường chỉ dùng khi khởi tạo được thêm làm tham số vào phương thức :meth:`~object.__init__` được tạo ra và được truyền vào phương thức :meth:`__post_init__` tùy chọn. Ngoài ra, dataclass không sử dụng chúng.

Ví dụ: giả sử một trường sẽ được khởi tạo từ cơ sở dữ liệu nếu không cung cấp giá trị khi tạo lớp::

  @dataclass
  class C:
      i: int
      j: int | None = None
      database: InitVar[DatabaseType | None] = None

      def __post_init__(self, database):
          if self.j is None and database is not None:
              self.j = database.lookup('j')

  c = C(10, database=my_database)

Trong trường hợp này, :func:`fields` sẽ trả về các đối tượng :class:`Field` cho :attr:`!i` và
:attr:`!j`, nhưng không trả về cho :attr:`!database`.

.. _dataclasses-frozen:

Các instance bị đóng băng
-------------------------

Không thể tạo các đối tượng Python thực sự bất biến. Tuy nhiên, bằng cách truyền ``frozen=True`` cho decorator :deco:`dataclass`, bạn có thể mô phỏng tính bất biến. Trong trường hợp đó, dataclasses sẽ thêm
các phương thức :meth:`~object.__setattr__` và :meth:`~object.__delattr__` vào class. Các phương thức này sẽ raise một :exc:`FrozenInstanceError` khi được gọi.

Khi sử dụng ``frozen=True``, hiệu năng sẽ giảm đôi chút:
:meth:`~object.__init__` không thể sử dụng phép gán đơn giản để khởi tạo các field và phải sử dụng :meth:`!object.__setattr__`.

.. Make sure to not remove "object" from "object.__setattr__" in the above markup!

.. _dataclasses-inheritance:

Tính kế thừa
------------

Khi dataclass được tạo bởi decorator :deco:`dataclass`, decorator này duyệt qua tất cả lớp cơ sở của lớp theo thứ tự MRO ngược (tức là bắt đầu từ :class:`object`) và với mỗi dataclass tìm thấy, thêm các field của lớp cơ sở đó vào một ánh xạ có thứ tự của các field. Sau khi thêm tất cả field của các lớp cơ sở, nó thêm các field của chính lớp đó vào ánh xạ có thứ tự. Tất cả phương thức được tạo sẽ sử dụng ánh xạ có thứ tự đã tính toán và kết hợp này của các field. Vì các field được sắp xếp theo thứ tự chèn, các lớp dẫn xuất sẽ ghi đè các lớp cơ sở. Một ví dụ::

  @dataclass
  class Base:
      x: Any = 15.0
      y: int = 0

  @dataclass
  class C(Base):
      z: int = 10
      x: int = 15

Danh sách field cuối cùng theo thứ tự là :attr:`!x`, :attr:`!y`, :attr:`!z`. Kiểu cuối cùng của :attr:`!x` là :class:`int`, như được chỉ định trong lớp :class:`!C`.

Phương thức :meth:`~object.__init__` được tạo cho :class:`!C` sẽ có dạng::

  def __init__(self, x: int = 15, y: int = 0, z: int = 10):

Sắp xếp lại các tham số chỉ dùng từ khóa trong :meth:`!__init__`
----------------------------------------------------------------

Sau khi tính toán các tham số cần thiết cho :meth:`~object.__init__`, mọi tham số chỉ dùng từ khóa sẽ được chuyển xuống sau tất cả tham số thông thường (không chỉ dùng từ khóa). Đây là yêu cầu trong cách Python triển khai các tham số chỉ dùng từ khóa: chúng phải đứng sau các tham số không chỉ dùng từ khóa.

Trong ví dụ này, :attr:`!Base.y`, :attr:`!Base.w` và :attr:`!D.t` là các field chỉ dùng từ khóa, còn :attr:`!Base.x` và :attr:`!D.z` là các field thông thường::

  @dataclass
  class Base:
      x: Any = 15.0
      _: KW_ONLY
      y: int = 0
      w: int = 1

  @dataclass
  class D(Base):
      z: int = 10
      t: int = field(kw_only=True, default=0)

Phương thức :meth:`!__init__` được tạo cho :class:`!D` sẽ có dạng như sau::

  def __init__(self, x: Any = 15.0, z: int = 10, *, y: int = 0, w: int = 1, t: int = 0):

Lưu ý rằng các tham số đã được sắp xếp lại so với thứ tự xuất hiện trong danh sách các trường: các tham số được tạo từ những trường thông thường đứng trước các tham số được tạo từ những trường chỉ nhận đối số từ khóa.

Thứ tự tương đối của các tham số chỉ nhận đối số từ khóa được duy trì trong danh sách tham số :meth:`!__init__` đã được sắp xếp lại.


Các hàm factory mặc định
------------------------

Nếu một :func:`field` chỉ định *default_factory*, hàm này sẽ được gọi không có đối số khi cần một giá trị mặc định cho trường. Ví dụ, để tạo một instance mới của list, hãy sử dụng::

  mylist: list = field(default_factory=list)

Nếu một trường bị loại khỏi :meth:`~object.__init__` (bằng cách sử dụng ``init=False``) và trường đó cũng chỉ định *default_factory*, thì hàm factory mặc định sẽ luôn được gọi từ hàm được tạo
:meth:`!__init__`. Điều này xảy ra vì không còn cách nào khác để cung cấp cho trường một giá trị ban đầu.

Các giá trị mặc định có thể thay đổi
------------------------------------

Python lưu trữ các giá trị mặc định của biến thành viên trong các thuộc tính của lớp. Hãy xem xét ví dụ này, không sử dụng dataclasses::

  class C:
      x = []
      def add(self, element):
          self.x.append(element)

  o1 = C()
  o2 = C()
  o1.add(1)
  o2.add(2)
  assert o1.x == [1, 2]
  assert o1.x is o2.x

Lưu ý rằng hai thực thể của lớp :class:`!C` dùng chung cùng một biến lớp :attr:`!x`, như mong đợi.

Khi sử dụng dataclasses, *nếu* đoạn mã này hợp lệ::

  @dataclass
  class D:
      x: list = []      # Đoạn mã này gây ra ValueError
      def add(self, element):
          self.x.append(element)

nó sẽ tạo ra đoạn mã tương tự như sau::

  class D:
      x = []
      def __init__(self, x=x):
          self.x = x
      def add(self, element):
          self.x.append(element)

  assert D().x is D().x

Điều này gặp phải vấn đề giống như ví dụ ban đầu sử dụng lớp :class:`!C`. Nghĩa là, hai thực thể của lớp :class:`!D` không chỉ định giá trị cho :attr:`!x` khi tạo một thực thể lớp sẽ dùng chung một bản sao của :attr:`!x`. Vì dataclasses chỉ sử dụng cách tạo lớp Python thông thường nên chúng cũng có hành vi này. Không có cách tổng quát nào để Data Classes phát hiện điều kiện này. Thay vào đó, các
decorator :deco:`dataclass` sẽ raise một :exc:`ValueError` nếu phát hiện tham số mặc định không thể băm. Giả định là nếu một giá trị không thể băm thì giá trị đó có thể thay đổi. Đây là một giải pháp chưa hoàn chỉnh, nhưng giúp ngăn chặn nhiều lỗi phổ biến.

Việc sử dụng các hàm default factory là một cách để tạo các instance mới của những kiểu có thể thay đổi làm giá trị mặc định cho các trường::

  @dataclass
  class D:
      x: list = field(default_factory=list)

  assert D().x is not D().x

.. versionchanged:: 3.11
   Thay vì tìm và không cho phép các đối tượng thuộc kiểu :class:`list`,
   :class:`dict`, hoặc :class:`set`, các đối tượng không thể băm hiện không được phép làm giá trị mặc định. Tính không thể băm được dùng để ước lượng khả năng thay đổi.

Các trường có kiểu descriptor
-----------------------------

Các trường được gán :ref:`các đối tượng descriptor <descriptors>` làm giá trị mặc định sẽ có các hành vi đặc biệt sau:

* Giá trị của trường được truyền vào phương thức :meth:`~object.__init__` của dataclass sẽ được truyền vào phương thức :meth:`~object.__set__` của descriptor thay vì ghi đè đối tượng descriptor.

* Tương tự, khi lấy hoặc thiết lập trường, phương thức của descriptor
  :meth:`~object.__get__` hoặc phương thức :meth:`!__set__` được gọi thay vì trả về hoặc ghi đè đối tượng descriptor.

* Để xác định liệu một trường có chứa giá trị mặc định hay không, :deco:`dataclass` sẽ gọi phương thức :meth:`!__get__` của descriptor bằng dạng truy cập lớp: ``descriptor.__get__(obj=None, type=cls)``. Nếu descriptor trả về một giá trị trong trường hợp này, giá trị đó sẽ được dùng làm giá trị mặc định của trường. Ngược lại, nếu descriptor phát sinh
  :exc:`AttributeError` trong tình huống này thì trường sẽ không được cung cấp giá trị mặc định.

::

  class IntConversionDescriptor:
      def __init__(self, *, default):
          self._default = default

      def __set_name__(self, owner, name):
          self._name = "_" + name

      def __get__(self, obj, type):
          if obj is None:
              return self._default

          return getattr(obj, self._name, self._default)

      def __set__(self, obj, value):
          setattr(obj, self._name, int(value))

  @dataclass
  class InventoryItem:
      quantity_on_hand: IntConversionDescriptor = IntConversionDescriptor(default=100)

  i = InventoryItem()
  print(i.quantity_on_hand)   # 100
  i.quantity_on_hand = 2.5    # gọi __set__ với 2.5
  print(i.quantity_on_hand)   # 2

Lưu ý rằng nếu một trường được chú thích bằng kiểu descriptor nhưng không được gán đối tượng descriptor làm giá trị mặc định, trường đó sẽ hoạt động như một trường thông thường.
