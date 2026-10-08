:mod:`!types` --- Tạo kiểu động và tên cho các kiểu dựng sẵn
============================================================

.. module:: types
   :synopsis: Tên của các kiểu dựng sẵn.

**Mã nguồn:** :source:`Lib/types.py`

--------------

Mô-đun này định nghĩa các hàm tiện ích hỗ trợ việc tạo động các kiểu mới.

Mô-đun này cũng định nghĩa tên cho một số kiểu đối tượng được trình thông dịch Python chuẩn sử dụng nhưng không được cung cấp dưới dạng các đối tượng dựng sẵn như :class:`int` hoặc
:class:`str`.

Cuối cùng, mô-đun cung cấp thêm một số lớp và hàm tiện ích liên quan đến kiểu, nhưng chưa đủ cơ bản để trở thành các đối tượng dựng sẵn.


Tạo kiểu động
-------------

.. function:: new_class(name, bases=(), kwds=None, exec_body=None)

   Tạo một đối tượng lớp một cách động bằng siêu lớp (metaclass) thích hợp.

   Ba đối số đầu tiên là các thành phần tạo nên phần đầu định nghĩa lớp: tên lớp, các lớp cơ sở (theo thứ tự), các đối số từ khóa (chẳng hạn như ``metaclass``).

   Đối số *exec_body* là một callback được dùng để điền namespace của lớp vừa tạo. Đối số này phải chấp nhận namespace của lớp làm đối số duy nhất và cập nhật trực tiếp namespace bằng nội dung lớp. Nếu không cung cấp callback, kết quả sẽ giống như truyền vào ``lambda ns: None``.

   .. versionadded:: 3.3

.. function:: prepare_class(name, bases=(), kwds=None)

   Tính toán siêu lớp (metaclass) thích hợp và tạo namespace của lớp.

   Các đối số là những thành phần tạo nên phần đầu định nghĩa lớp: tên lớp, các lớp cơ sở (theo thứ tự) và các đối số từ khóa (chẳng hạn như ``metaclass``).

   Giá trị trả về là một bộ 3 phần tử: ``metaclass, namespace, kwds``

   *metaclass* là metaclass thích hợp, *namespace* là namespace đã chuẩn bị của lớp và *kwds* là bản sao đã cập nhật của đối số *kwds* được truyền vào, trong đó mọi mục nhập ``'metaclass'`` đều đã bị loại bỏ. Nếu không truyền đối số *kwds*, đây sẽ là một dict rỗng.

   .. versionadded:: 3.3

   .. versionchanged:: 3.6

      Giá trị mặc định cho phần tử ``namespace`` của tuple được trả về đã thay đổi. Hiện tại, một mapping bảo toàn thứ tự chèn được sử dụng khi metaclass không có phương thức ``__prepare__``.

.. seealso::

   :ref:`metaclasses`
      Thông tin đầy đủ về quy trình tạo lớp được các hàm này hỗ trợ

   :pep:`3115` - Các metaclass trong Python 3000
      Đã giới thiệu hook namespace ``__prepare__``

.. function:: resolve_bases(bases)

   Giải quyết các mục nhập MRO một cách động như được đặc tả bởi :pep:`560`.

   Hàm này tìm các mục trong *bases* không phải là các instance của
   :class:`type` và trả về một tuple trong đó mỗi đối tượng có phương thức :meth:`~object.__mro_entries__` được thay thế bằng kết quả đã unpack khi gọi phương thức này. Nếu một phần tử *bases* là một thể hiện của :class:`type` hoặc không có phương thức :meth:`!__mro_entries__`, thì phần tử đó được giữ nguyên trong tuple trả về.

   .. versionadded:: 3.7

.. function:: get_original_bases(cls, /)

    Trả về tuple gồm các đối tượng ban đầu được cung cấp làm các base của *cls* trước khi phương thức :meth:`~object.__mro_entries__` được gọi trên bất kỳ base nào (theo các cơ chế được nêu trong :pep:`560`). Điều này hữu ích khi kiểm tra nội quan các :ref:`Generics <user-defined-generics>`.

    Đối với các lớp có thuộc tính ``__orig_bases__``, hàm này trả về giá trị của ``cls.__orig_bases__``. Đối với các lớp không có thuộc tính ``__orig_bases__``,
    :attr:`cls.__bases__ <type.__bases__>` được trả về.

    Ví dụ::

        from typing import TypeVar, Generic, NamedTuple, TypedDict

        T = TypeVar("T")
        class Foo(Generic[T]): ...
        class Bar(Foo[int], float): ...
        class Baz(list[str]): ...
        Eggs = NamedTuple("Eggs", [("a", int), ("b", str)])
        Spam = TypedDict("Spam", {"a": int, "b": str})

        assert Bar.__bases__ == (Foo, float)
        assert get_original_bases(Bar) == (Foo[int], float)

        assert Baz.__bases__ == (list,)
        assert get_original_bases(Baz) == (list[str],)

        assert Eggs.__bases__ == (tuple,)
        assert get_original_bases(Eggs) == (NamedTuple,)

        assert Spam.__bases__ == (dict,)
        assert get_original_bases(Spam) == (TypedDict,)

        assert int.__bases__ == (object,)
        assert get_original_bases(int) == (object,)

    .. versionadded:: 3.12

.. seealso::

   :pep:`560` - Hỗ trợ cốt lõi cho mô-đun typing và các kiểu generic


Các kiểu của trình thông dịch chuẩn
-----------------------------------

Mô-đun này cung cấp tên cho nhiều kiểu cần thiết để triển khai một trình thông dịch Python. Mô-đun cố ý không bao gồm một số kiểu chỉ phát sinh ngẫu nhiên trong quá trình xử lý, chẳng hạn như kiểu ``listiterator``.

Cách sử dụng điển hình của các tên này là để kiểm tra :func:`isinstance` hoặc
kiểm tra :func:`issubclass`.


Nếu khởi tạo bất kỳ kiểu nào trong số này, hãy lưu ý rằng chữ ký có thể khác nhau giữa các phiên bản Python.

Các tên chuẩn được định nghĩa cho những kiểu sau:

.. class:: NoneType

   Kiểu của :data:`None`.

   .. versionadded:: 3.10


.. class:: FunctionType
           LambdaType

   Kiểu của các hàm do người dùng định nghĩa và các hàm được tạo bởi
   :keyword:`lambda`  biểu thức.

   .. audit-event:: function.__new__ code types.FunctionType

   Sự kiện audit chỉ xảy ra khi các đối tượng hàm được khởi tạo trực tiếp và không được phát sinh trong quá trình biên dịch thông thường.


.. class:: GeneratorType

   Kiểu của các đối tượng :term:`generator`-iterator, được tạo bởi các hàm generator.


.. class:: CoroutineType

   Kiểu của các đối tượng :term:`coroutine`, được tạo bởi
   các hàm :keyword:`async def`.

   .. versionadded:: 3.5


.. class:: AsyncGeneratorType

   Kiểu của các đối tượng :term:`asynchronous generator`-iterator, được tạo bởi các hàm generator bất đồng bộ.

   .. versionadded:: 3.6


.. class:: CodeType(**kwargs)

   .. index:: pair: built-in function; compile

   Kiểu của các :ref:`đối tượng code <code-objects>` như những đối tượng được trả về bởi :func:`compile`.

   .. audit-event:: code.__new__ code,filename,name,argcount,posonlyargcount,kwonlyargcount,nlocals,stacksize,flags types.CodeType

   Lưu ý rằng các đối số được kiểm tra có thể không khớp với tên hoặc vị trí mà initializer yêu cầu. Sự kiện kiểm tra chỉ xảy ra khi khởi tạo trực tiếp các đối tượng code và không được phát ra trong quá trình biên dịch thông thường.

.. class:: CellType

   Kiểu của các đối tượng cell: những đối tượng này được dùng làm vùng chứa cho các :term:`biến closure <closure variable>` của một hàm.

   .. versionadded:: 3.8


.. class:: MethodType

   Kiểu của các phương thức thuộc các instance của lớp do người dùng định nghĩa.


.. class:: BuiltinFunctionType
           BuiltinMethodType

   Kiểu của các hàm tích hợp như :func:`len` hoặc :func:`sys.exit`, và các phương thức của các lớp tích hợp. (Ở đây, thuật ngữ "tích hợp" có nghĩa là "được viết bằng C".)


.. class:: WrapperDescriptorType

   Kiểu của các phương thức thuộc một số kiểu dữ liệu tích hợp và các lớp cơ sở như
   :meth:`object.__init__` hoặc :meth:`object.__lt__`.

   .. versionadded:: 3.7


.. class:: MethodWrapperType

   Kiểu của các phương thức *bound* của một số kiểu dữ liệu dựng sẵn và lớp cơ sở. Ví dụ: đây là kiểu của :code:`object().__str__`.

   .. versionadded:: 3.7


.. class:: NotImplementedType

   Kiểu của :data:`NotImplemented`.

   .. versionadded:: 3.10


.. class:: MethodDescriptorType

   Kiểu của các phương thức thuộc một số kiểu dữ liệu dựng sẵn, chẳng hạn như :meth:`str.join`.

   .. versionadded:: 3.7


.. class:: ClassMethodDescriptorType

   Kiểu của các phương thức lớp *unbound* của một số kiểu dữ liệu dựng sẵn, chẳng hạn như ``dict.__dict__['fromkeys']``.

   .. versionadded:: 3.7


.. class:: ModuleType(name, doc=None)

   Kiểu của :term:`modules <module>`. Hàm khởi tạo nhận tên của module cần tạo và, tùy chọn, :term:`docstring` của module đó.

   .. seealso::

      :ref:`Tài liệu về các đối tượng module <module-objects>`
         Cung cấp thông tin chi tiết về các thuộc tính đặc biệt có thể tìm thấy trên các instance của :class:`!ModuleType`.

      :func:`importlib.util.module_from_spec`
         Các module được tạo bằng constructor :class:`!ModuleType` sẽ có nhiều thuộc tính đặc biệt chưa được thiết lập hoặc được đặt thành các giá trị mặc định. :func:`!module_from_spec` cung cấp một cách mạnh mẽ hơn để tạo các instance :class:`!ModuleType`, bảo đảm rằng các thuộc tính khác nhau được thiết lập phù hợp.

.. class:: EllipsisType

   Kiểu của :data:`Ellipsis`.

   .. versionadded:: 3.10

.. class:: GenericAlias(t_origin, t_args)

   Kiểu của :ref:`các generic có tham số <types-genericalias>` như ``list[int]``.

   ``t_origin`` phải là một lớp generic không có tham số, chẳng hạn như ``list``, ``tuple`` hoặc ``dict``. ``t_args`` phải là một :class:`tuple` (có thể có độ dài 1) gồm các kiểu dùng để tham số hóa ``t_origin``::

      >>> from types import GenericAlias

      >>> list[int] == GenericAlias(list, (int,))
      True
      >>> dict[str, int] == GenericAlias(dict, (str, int))
      True

   .. versionadded:: 3.9

   .. versionchanged:: 3.9.2
      Kiểu này hiện có thể được subclass.

   .. seealso::

      :ref:`Các kiểu Generic Alias <types-genericalias>`
         Tài liệu chuyên sâu về các instance của :class:`!types.GenericAlias`

      :pep:`585` - Generic dùng để type hint trong các collection chuẩn
         Giới thiệu lớp :class:`!types.GenericAlias`

.. class:: UnionType

   Kiểu của :ref:`biểu thức kiểu hợp <types-union>`.

   .. versionadded:: 3.10

   .. versionchanged:: 3.14

      Hiện là bí danh cho :class:`typing.Union`.

.. class:: TracebackType(tb_next, tb_frame, tb_lasti, tb_lineno)

   Kiểu của các đối tượng traceback, chẳng hạn như các đối tượng được tìm thấy trong ``sys.exception().__traceback__``.

   Xem :ref:`tài liệu tham chiếu ngôn ngữ <traceback-objects>` để biết chi tiết về các thuộc tính và phép toán hiện có, cũng như hướng dẫn tạo traceback một cách động.


.. class:: FrameType

   Kiểu của các đối tượng :ref:`frame <frame-objects>` như được tìm thấy trong
   :attr:`tb.tb_frame <traceback.tb_frame>` nếu ``tb`` là một đối tượng traceback.


.. class:: GetSetDescriptorType

   Kiểu của các đối tượng được định nghĩa trong các extension module bằng ``PyGetSetDef``, chẳng hạn như :attr:`FrameType.f_locals <frame.f_locals>` hoặc ``array.array.typecode``. Kiểu này được dùng làm descriptor cho các thuộc tính đối tượng; nó có cùng mục đích như
   kiểu :class:`property`, nhưng dành cho các lớp được định nghĩa trong extension module.


.. class:: MemberDescriptorType

   Kiểu của các đối tượng được định nghĩa trong các extension module bằng ``PyMemberDef``, chẳng hạn như ``datetime.timedelta.days``. Kiểu này được dùng làm descriptor cho các thành viên dữ liệu C đơn giản sử dụng các hàm chuyển đổi tiêu chuẩn; nó có cùng mục đích như kiểu :class:`property`, nhưng dành cho các lớp được định nghĩa trong extension module.

   Ngoài ra, khi một lớp được định nghĩa với thuộc tính :attr:`~object.__slots__`, thì đối với mỗi slot, một thể hiện của :class:`!MemberDescriptorType` sẽ được thêm làm thuộc tính trên lớp đó. Điều này cho phép slot xuất hiện trong :attr:`~type.__dict__` của lớp.

   .. impl-detail::

      Trong các triển khai Python khác, kiểu này có thể giống hệt ``GetSetDescriptorType``.

.. class:: MappingProxyType(mapping)

   Proxy chỉ đọc của một mapping. Proxy này cung cấp một chế độ xem động đối với các mục trong mapping, nghĩa là khi mapping thay đổi, chế độ xem cũng phản ánh những thay đổi đó.

   :class:`!MappingProxyType`\s là :ref:`generic <generics>` trên hai kiểu, lần lượt biểu thị kiểu của các khóa và giá trị trong mapping bên dưới.

   .. versionadded:: 3.3

   .. versionchanged:: 3.9

      Đã được cập nhật để hỗ trợ toán tử union mới (``|``) từ :pep:`584`, toán tử này chỉ ủy quyền cho mapping bên dưới.

   .. describe:: key in proxy

      Trả về ``True`` nếu mapping bên dưới có khóa *key*, nếu không thì trả về ``False``.

   .. describe:: proxy[key]

      Trả về mục trong mapping bên dưới có khóa *key*.  Phát sinh một
      :exc:`KeyError` nếu *key* không có trong mapping bên dưới.

   .. describe:: iter(proxy)

      Trả về một iterator trên các khóa của mapping bên dưới.  Đây là cách viết tắt của ``iter(proxy.keys())``.

   .. describe:: len(proxy)

      Trả về số lượng mục trong ánh xạ cơ sở.

   .. method:: copy()

      Trả về một bản sao nông của ánh xạ cơ sở.

   .. method:: get(key[, default])

      Trả về giá trị của *key* nếu *key* có trong ánh xạ cơ sở, nếu không thì trả về *default*. Nếu *default* không được cung cấp, giá trị mặc định là ``None``, để phương thức này không bao giờ phát sinh :exc:`KeyError`.

   .. method:: items()

      Trả về một view mới về các mục (``(key, value)`` cặp) của ánh xạ cơ sở.

   .. method:: keys()

      Trả về một view mới về các khóa của ánh xạ cơ sở.

   .. method:: values()

      Trả về một view mới về các giá trị của ánh xạ cơ sở.

   .. describe:: reversed(proxy)

      Trả về một iterator ngược trên các khóa của ánh xạ cơ sở.

      .. versionadded:: 3.9

   .. describe:: hash(proxy)

      Trả về một hash của ánh xạ nền tảng.

      .. versionadded:: 3.12

.. class:: CapsuleType

   Kiểu của các đối tượng :ref:`capsule <capsules>`.

   .. versionadded:: 3.13


Các lớp và hàm tiện ích bổ sung
-------------------------------

.. class:: SimpleNamespace

   Một lớp con :class:`object` đơn giản, cung cấp quyền truy cập thuộc tính vào namespace của nó, đồng thời có repr có ý nghĩa.

   Không giống như :class:`object`, với :class:`!SimpleNamespace` bạn có thể thêm và xóa các thuộc tính.

   Các đối tượng :py:class:`SimpleNamespace` có thể được khởi tạo theo cùng cách với :class:`dict`: bằng các đối số từ khóa, bằng một đối số vị trí duy nhất hoặc bằng cả hai. Khi được khởi tạo bằng các đối số từ khóa, chúng sẽ được thêm trực tiếp vào namespace nền tảng. Ngoài ra, khi được khởi tạo bằng một đối số vị trí, namespace nền tảng sẽ được cập nhật bằng các cặp khóa-giá trị từ đối số đó (là một đối tượng ánh xạ hoặc một đối tượng :term:`iterable` tạo ra các cặp khóa-giá trị). Tất cả các khóa như vậy phải là chuỗi.

   Kiểu này gần tương đương với đoạn mã sau::

       class SimpleNamespace:
           def __init__(self, mapping_or_iterable=(), /, **kwargs):
               self.__dict__.update(mapping_or_iterable)
               self.__dict__.update(kwargs)

           def __repr__(self):
               items = (f"{k}={v!r}" for k, v in self.__dict__.items())
               return "{}({})".format(type(self).__name__, ", ".join(items))

           def __eq__(self, other):
               if isinstance(self, SimpleNamespace) and isinstance(other, SimpleNamespace):
                  return self.__dict__ == other.__dict__
               return NotImplemented

   ``SimpleNamespace`` có thể hữu ích để thay thế cho ``class NS: pass``. Tuy nhiên, đối với kiểu bản ghi có cấu trúc, hãy sử dụng :func:`~collections.namedtuple` thay thế.

   Các đối tượng :class:`!SimpleNamespace` được :func:`copy.replace` hỗ trợ.

   .. versionadded:: 3.3

   .. versionchanged:: 3.9
      Thứ tự thuộc tính trong repr đã thay đổi từ thứ tự alphabet sang thứ tự chèn (giống như ``dict``).

   .. versionchanged:: 3.13
      Đã thêm hỗ trợ cho một đối số vị trí tùy chọn.

.. function:: DynamicClassAttribute(fget=None, fset=None, fdel=None, doc=None)

   Định tuyến việc truy cập thuộc tính trên một lớp đến __getattr__.

   Đây là một descriptor, được dùng để định nghĩa các thuộc tính hoạt động khác nhau khi được truy cập thông qua một instance và thông qua một lớp. Việc truy cập thông qua instance vẫn giữ nguyên như bình thường, nhưng việc truy cập một thuộc tính thông qua một lớp sẽ được định tuyến đến phương thức __getattr__ của lớp; điều này được thực hiện bằng cách phát sinh AttributeError.

   Điều này cho phép có các property hoạt động trên một instance, đồng thời có các thuộc tính ảo trên lớp với cùng tên (xem :class:`enum.Enum` để biết ví dụ).

   .. versionadded:: 3.4


Các hàm tiện ích cho Coroutine
------------------------------

.. function:: coroutine(gen_func)

   Hàm này chuyển đổi một hàm :term:`generator` thành một
   :term:`coroutine function` trả về một coroutine dựa trên generator. Coroutine dựa trên generator này vẫn là một :term:`generator iterator`, nhưng cũng được xem là một đối tượng :term:`coroutine` và là
   :term:`awaitable`. Tuy nhiên, nó không nhất thiết phải triển khai phương thức :meth:`~object.__await__`.

   Nếu *gen_func* là một hàm generator, hàm đó sẽ được sửa trực tiếp.

   Nếu *gen_func* không phải là một hàm generator, hàm đó sẽ được bọc lại. Nếu hàm trả về một thực thể của :class:`collections.abc.Generator`, thực thể đó sẽ được bọc trong một đối tượng proxy *awaitable*. Tất cả các kiểu đối tượng khác sẽ được trả về nguyên trạng.

   .. versionadded:: 3.5
