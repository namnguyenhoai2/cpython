:mod:`!abc` --- Lớp cơ sở trừu tượng
====================================

.. module:: abc
   :synopsis: Các lớp cơ sở trừu tượng theo :pep:`3119`.

.. moduleauthor:: Guido van Rossum
.. sectionauthor:: Georg Brandl
.. much of the content adapted from docstrings

**Mã nguồn:** :source:`Lib/abc.py`

--------------

Mô-đun này cung cấp cơ sở hạ tầng để định nghĩa :term:`lớp cơ sở trừu tượng <abstract base class>` (ABC) trong Python, như được nêu trong :pep:`3119`; hãy xem PEP để biết lý do tính năng này được thêm vào Python. (Xem thêm :pep:`3141` và
:mod:`numbers` mô-đun liên quan đến hệ phân cấp kiểu cho các số dựa trên ABC.)

Mô-đun :mod:`collections` có một số lớp cụ thể kế thừa từ ABC; tất nhiên, bạn có thể tiếp tục tạo các lớp dẫn xuất từ chúng. Ngoài ra,
mô-đun con :mod:`collections.abc` có một số ABC có thể được dùng để kiểm tra xem một lớp hoặc thực thể có cung cấp một giao diện cụ thể hay không, chẳng hạn như nếu nó
:term:`hashable` hoặc nếu đó là một :term:`mapping`.


Mô-đun này cung cấp metaclass :class:`ABCMeta` để định nghĩa các ABC và một lớp trợ giúp :class:`ABC` để định nghĩa các ABC thông qua kế thừa theo cách khác:

.. class:: ABC

   Một lớp trợ giúp có :class:`ABCMeta` làm metaclass. Với lớp này, có thể tạo một abstract base class bằng cách đơn giản là kế thừa từ :class:`!ABC`, tránh việc đôi khi gây nhầm lẫn khi sử dụng metaclass, ví dụ::

     from abc import ABC

     class MyABC(ABC):
         pass

   Lưu ý rằng kiểu của :class:`!ABC` vẫn là :class:`ABCMeta`, do đó việc kế thừa từ :class:`!ABC` đòi hỏi các biện pháp thận trọng thông thường khi sử dụng metaclass, vì đa kế thừa có thể dẫn đến xung đột metaclass. Bạn cũng có thể định nghĩa một abstract base class bằng cách truyền từ khóa metaclass và sử dụng trực tiếp :class:`!ABCMeta`, ví dụ::

     from abc import ABCMeta

     class MyABC(metaclass=ABCMeta):
         pass

   .. versionadded:: 3.4


.. class:: ABCMeta

   Metaclass dùng để định nghĩa Abstract Base Classes (ABC).

   Sử dụng metaclass này để tạo một ABC. Một ABC có thể được phân lớp trực tiếp và sau đó hoạt động như một lớp mix-in. Bạn cũng có thể đăng ký các lớp cụ thể không liên quan (kể cả các lớp tích hợp sẵn) và các ABC không liên quan dưới dạng "virtual subclass" -- các lớp này và các lớp con của chúng sẽ được hàm tích hợp sẵn :func:`issubclass` xem là các lớp con của ABC đăng ký, nhưng ABC đăng ký sẽ không xuất hiện trong MRO (Method Resolution Order) của chúng, và các triển khai phương thức được định nghĩa bởi ABC đăng ký cũng sẽ không thể gọi được (kể cả thông qua
   :func:`super`). [#]_

   Các lớp được tạo với metaclass là :class:`!ABCMeta` có phương thức sau:

   .. method:: register(subclass)

      Đăng ký *subclass* dưới dạng một “lớp con ảo” (virtual subclass) của ABC này. Ví dụ::

         from abc import ABC

         class MyABC(ABC):
             pass

         MyABC.register(tuple)

         assert issubclass(tuple, MyABC)
         assert isinstance((), MyABC)

      .. versionchanged:: 3.3
         Trả về lớp con đã đăng ký, cho phép sử dụng làm class decorator.

      .. versionchanged:: 3.4
         Để phát hiện các lệnh gọi đến :meth:`!register`, bạn có thể sử dụng
         hàm :func:`get_cache_token`.

   Bạn cũng có thể ghi đè phương thức này trong một abstract base class:

   .. method:: __subclasshook__(subclass)

      (Phải được định nghĩa dưới dạng một class method.)

      Kiểm tra xem *subclass* có được xem là lớp con của ABC này hay không. Điều này có nghĩa là bạn có thể tùy chỉnh thêm hành vi của :func:`issubclass` mà không cần gọi :meth:`register` trên mọi lớp mà bạn muốn xem là lớp con của ABC. (Class method này được gọi từ
      :meth:`~type.__subclasscheck__` của ABC.)

      Phương thức này phải trả về ``True``, ``False`` hoặc :data:`NotImplemented`. Nếu trả về ``True``, *subclass* được xem là một subclass của ABC này. Nếu trả về ``False``, *subclass* không được xem là một subclass của ABC này, ngay cả khi theo thông thường nó phải là một subclass. Nếu trả về
      :data:`!NotImplemented`, việc kiểm tra subclass sẽ tiếp tục bằng cơ chế thông thường.

      .. XXX explain the "usual mechanism"


   Để minh họa các khái niệm này, hãy xem định nghĩa ABC mẫu sau đây::

      class Foo:
          def __getitem__(self, index):
              ...
          def __len__(self):
              ...
          def get_iterator(self):
              return iter(self)

      class MyIterable(ABC):

          @abstractmethod
          def __iter__(self):
              while False:
                  yield None

          def get_iterator(self):
              return self.__iter__()

          @classmethod
          def __subclasshook__(cls, C):
              if cls is MyIterable:
                  if any("__iter__" in B.__dict__ for B in C.__mro__):
                      return True
              return NotImplemented

      MyIterable.register(Foo)

   ABC ``MyIterable`` định nghĩa phương thức iterable tiêu chuẩn,
   :meth:`~object.__iter__`, dưới dạng một abstract method. Phần triển khai được cung cấp ở đây vẫn có thể được gọi từ các subclass. Phương thức :meth:`!get_iterator` cũng là một phần của abstract base class ``MyIterable``, nhưng không bắt buộc phải được ghi đè trong các derived class không trừu tượng.

   Phương thức class :meth:`__subclasshook__` được định nghĩa ở đây cho biết rằng mọi class có phương thức :meth:`~object.__iter__` trong
   :attr:`~object.__dict__` (hoặc trong một lớp cơ sở của nó, được truy cập thông qua danh sách :attr:`~type.__mro__`) cũng được xem là một ``MyIterable``.

   Cuối cùng, dòng cuối biến ``Foo`` thành một lớp con ảo của ``MyIterable``, dù nó không định nghĩa phương thức :meth:`~object.__iter__` (nó sử dụng giao thức iterable kiểu cũ, được định nghĩa theo :meth:`~object.__len__` và
   :meth:`~object.__getitem__`). Lưu ý rằng điều này không làm cho ``get_iterator`` khả dụng dưới dạng một phương thức của ``Foo``, vì vậy nó được cung cấp riêng.




Mô-đun :mod:`!abc` cũng cung cấp decorator sau:

.. decorator:: abstractmethod

   Một decorator cho biết các phương thức là abstract.

   Việc sử dụng decorator này yêu cầu metaclass của lớp là :class:`ABCMeta` hoặc được kế thừa từ nó. Một lớp có metaclass được kế thừa từ
   :class:`!ABCMeta` không thể được khởi tạo trừ khi tất cả các phương thức và thuộc tính abstract của nó được ghi đè. Có thể gọi các phương thức abstract bằng bất kỳ cơ chế gọi 'super' thông thường nào. Có thể sử dụng :deco:`!abstractmethod` để khai báo các phương thức abstract cho thuộc tính và descriptor.

   Việc thêm động các phương thức abstract vào một class hoặc cố gắng thay đổi trạng thái abstraction của một phương thức hay class sau khi đã tạo chỉ được hỗ trợ bằng hàm :func:`update_abstractmethods`.  Hàm
   :deco:`!abstractmethod` chỉ ảnh hưởng đến các subclass được dẫn xuất bằng cơ chế kế thừa thông thường; các "virtual subclass" được đăng ký với ABC
   không bị ảnh hưởng bởi phương thức :meth:`~ABCMeta.register`.

   Khi áp dụng :deco:`!abstractmethod` kết hợp với các method descriptor khác, nên áp dụng nó làm decorator trong cùng, như minh họa trong các ví dụ sử dụng sau đây::

      class C(ABC):
          @abstractmethod
          def my_abstract_method(self, arg1):
              ...
          @classmethod
          @abstractmethod
          def my_abstract_classmethod(cls, arg2):
              ...
          @staticmethod
          @abstractmethod
          def my_abstract_staticmethod(arg3):
              ...

          @property
          @abstractmethod
          def my_abstract_property(self):
              ...
          @my_abstract_property.setter
          @abstractmethod
          def my_abstract_property(self, val):
              ...

          @abstractmethod
          def _get_x(self):
              ...
          @abstractmethod
          def _set_x(self, val):
              ...
          x = property(_get_x, _set_x)

   Để tương tác chính xác với cơ chế abstract base class, descriptor phải tự xác định là abstract bằng cách sử dụng
   :attr:`!__isabstractmethod__`. Nhìn chung, thuộc tính này phải là ``True`` nếu bất kỳ phương thức nào được dùng để tạo descriptor là abstract. Ví dụ, :deco:`property` tích hợp sẵn của Python thực hiện tương đương với::

      class Descriptor:
          ...
          @property
          def __isabstractmethod__(self):
              return any(getattr(f, '__isabstractmethod__', False) for
                         f in (self._fget, self._fset, self._fdel))

   .. note::

      Không giống các abstract method trong Java, những phương thức abstract này có thể có phần triển khai. Có thể gọi phần triển khai này thông qua cơ chế :func:`super` từ class ghi đè nó. Điều này có thể hữu ích làm điểm kết thúc cho một super-call trong framework sử dụng cơ chế multiple-inheritance mang tính hợp tác.

Module :mod:`!abc` cũng hỗ trợ các decorator cũ sau đây:

.. decorator:: abstractclassmethod

   .. versionadded:: 3.2
   .. deprecated:: 3.3
       Giờ đây có thể sử dụng :deco:`classmethod` với
       :deco:`abstractmethod`, khiến decorator này trở nên thừa.

   Một lớp con của :class:`classmethod` tích hợp sẵn, cho biết một classmethod trừu tượng. Nếu không thì nó tương tự như :deco:`abstractmethod`.

   Trường hợp đặc biệt này không còn được khuyến nghị, vì decorator :deco:`classmethod` hiện được nhận diện chính xác là trừu tượng khi được áp dụng cho một phương thức trừu tượng::

      class C(ABC):
          @classmethod
          @abstractmethod
          def my_abstract_classmethod(cls, arg):
              ...


.. decorator:: abstractstaticmethod

   .. versionadded:: 3.2
   .. deprecated:: 3.3
       Giờ đây có thể sử dụng :deco:`staticmethod` với
       :deco:`abstractmethod`, khiến decorator này trở nên thừa.

   Một lớp con của :class:`staticmethod` tích hợp sẵn, biểu thị một staticmethod trừu tượng. Nếu không thì nó tương tự như :deco:`abstractmethod`.

   Trường hợp đặc biệt này không còn được khuyến nghị sử dụng, vì decorator :deco:`staticmethod` hiện được nhận diện chính xác là abstract khi được áp dụng cho một abstract method::

      class C(ABC):
          @staticmethod
          @abstractmethod
          def my_abstract_staticmethod(arg):
              ...


.. decorator:: abstractproperty

   .. deprecated:: 3.3
       Giờ đây có thể sử dụng :deco:`property`, :deco:`property.getter`,
       :deco:`property.setter` và :deco:`property.deleter` cùng với
       :deco:`abstractmethod`, khiến decorator này trở nên thừa.

   Một lớp con của :class:`property` tích hợp sẵn, biểu thị một property trừu tượng.

   Trường hợp đặc biệt này không còn được khuyến nghị sử dụng, vì decorator :deco:`property` hiện được nhận diện chính xác là abstract khi được áp dụng cho một abstract method::

      class C(ABC):
          @property
          @abstractmethod
          def my_abstract_property(self):
              ...

   Ví dụ trên định nghĩa một thuộc tính chỉ đọc; bạn cũng có thể định nghĩa một thuộc tính trừu tượng vừa đọc vừa ghi bằng cách đánh dấu phù hợp một hoặc nhiều phương thức nền tảng là trừu tượng::

      class C(ABC):
          @property
          def x(self):
              ...

          @x.setter
          @abstractmethod
          def x(self, val):
              ...

   Nếu chỉ một số thành phần là trừu tượng, chỉ cần cập nhật các thành phần đó để tạo một thuộc tính cụ thể trong lớp con::

      class D(C):
          @C.x.setter
          def x(self, val):
              ...


Mô-đun :mod:`!abc` cũng cung cấp các hàm sau:

.. function:: get_cache_token()

   Trả về token bộ nhớ đệm của lớp cơ sở trừu tượng hiện tại.

   Token này là một đối tượng không minh bạch (hỗ trợ kiểm tra tính bằng nhau), dùng để xác định phiên bản hiện tại của bộ nhớ đệm lớp cơ sở trừu tượng dành cho các lớp con ảo. Token thay đổi sau mỗi lần gọi :meth:`ABCMeta.register` trên bất kỳ ABC nào.

   .. versionadded:: 3.4

.. function:: update_abstractmethods(cls)

   Một hàm dùng để tính toán lại trạng thái trừu tượng của một lớp. Nên gọi hàm này nếu các phương thức trừu tượng của một lớp được triển khai hoặc thay đổi sau khi lớp đó được tạo. Thông thường, nên gọi hàm này từ bên trong một class decorator.

   Trả về *cls*, cho phép sử dụng hàm này làm class decorator.

   Nếu *cls* không phải là một thực thể của :class:`ABCMeta`, thì không thực hiện gì.

   .. note::

      Hàm này giả định rằng các lớp cha của *cls* đã được cập nhật. Hàm không cập nhật bất kỳ lớp con nào.

   .. versionadded:: 3.10

.. rubric:: Chú thích cuối trang

.. [#] Lập trình viên C++ cần lưu ý rằng khái niệm lớp cơ sở ảo của Python không giống với khái niệm của C++.
