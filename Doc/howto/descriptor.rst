.. _descriptorhowto:

=======================
Hướng dẫn về descriptor
=======================

:Author: Raymond Hettinger
:Contact: <python at rcn dot com>

.. Contents::


:term:`Descriptor <descriptor>` cho phép các đối tượng tùy chỉnh việc tra cứu, lưu trữ và xóa thuộc tính.

Hướng dẫn này gồm bốn phần chính:

1) "Phần nhập môn" cung cấp tổng quan cơ bản, bắt đầu nhẹ nhàng từ những ví dụ đơn giản và lần lượt bổ sung từng tính năng. Hãy bắt đầu từ đây nếu bạn chưa quen với descriptor.

2) Phần thứ hai trình bày một ví dụ descriptor hoàn chỉnh và thiết thực. Nếu bạn đã nắm được những kiến thức cơ bản, hãy bắt đầu từ đó.

3) Phần thứ ba cung cấp một hướng dẫn kỹ thuật chuyên sâu hơn, đi vào cơ chế chi tiết của cách descriptor hoạt động. Hầu hết mọi người không cần mức độ chi tiết này.

4) Phần cuối có các phiên bản tương đương bằng Python thuần túy cho những descriptor tích hợp được viết bằng C. Hãy đọc phần này nếu bạn tò mò về cách các hàm trở thành bound method hoặc về cách triển khai những công cụ phổ biến như
   :deco:`classmethod`, :deco:`staticmethod`, :deco:`property`, và
   :term:`__slots__`.


Nhập môn
^^^^^^^^

Trong phần nhập môn này, chúng ta bắt đầu với ví dụ cơ bản nhất có thể, sau đó lần lượt bổ sung từng khả năng mới.


Ví dụ đơn giản: Descriptor trả về một hằng số
---------------------------------------------

Lớp :class:`!Ten` là một descriptor có phương thức :meth:`~object.__get__` luôn trả về hằng số ``10``:

.. testcode::

    class Ten:
        def __get__(self, obj, objtype=None):
            return 10

Để sử dụng descriptor, nó phải được lưu trữ dưới dạng biến lớp trong một lớp khác:

.. testcode::

    class A:
        x = 5                       # Thuộc tính lớp thông thường
        y = Ten()                   # Instance của descriptor

Một phiên tương tác cho thấy sự khác biệt giữa việc tra cứu thuộc tính thông thường và tra cứu descriptor:

.. doctest::

    >>> a = A()                     # Tạo một instance của lớp A
    >>> a.x                         # Tra cứu thuộc tính thông thường
    5
    >>> a.y                         # Tra cứu descriptor
    10

Trong phép tra cứu thuộc tính ``a.x``, toán tử dấu chấm tìm thấy ``'x': 5`` trong từ điển lớp. Trong phép tra cứu ``a.y``, toán tử dấu chấm tìm thấy một instance descriptor, được nhận diện bởi phương thức ``__get__``. Việc gọi phương thức đó trả về ``10``.

Lưu ý rằng giá trị ``10`` không được lưu trong từ điển lớp cũng như từ điển instance. Thay vào đó, giá trị ``10`` được tính theo yêu cầu.

Ví dụ này cho thấy cách một descriptor đơn giản hoạt động, nhưng nó không hữu ích lắm. Để truy xuất các hằng số, phép tra cứu thuộc tính thông thường sẽ phù hợp hơn.

Trong phần tiếp theo, chúng ta sẽ tạo ra một thứ hữu ích hơn: phép tra cứu động.


Phép tra cứu động
-----------------

Các descriptor thú vị thường thực hiện phép tính thay vì trả về hằng số:

.. testcode::

    import os

    class DirectorySize:

        def __get__(self, obj, objtype=None):
            return len(os.listdir(obj.dirname))

    class Directory:

        size = DirectorySize()              # Instance descriptor

        def __init__(self, dirname):
            self.dirname = dirname          # Thuộc tính instance thông thường

Một phiên tương tác cho thấy việc tra cứu là động — mỗi lần đều tính toán các kết quả khác nhau và được cập nhật::

    >>> s = Directory('songs')
    >>> g = Directory('games')
    >>> s.size                              # Thư mục songs có hai mươi tệp
    20
    >>> g.size                              # Thư mục games có ba tệp
    3
    >>> os.remove('games/chess')            # Xóa một game
    >>> g.size                              # Số lượng tệp được tự động cập nhật
    2

Ngoài việc cho thấy descriptor có thể thực hiện các phép tính, ví dụ này còn cho thấy mục đích của các tham số của :meth:`~object.__get__`.  Tham số *self* là *size*, một instance của *DirectorySize*.  Tham số *obj* là *g* hoặc *s*, một instance của *Directory*.  Chính tham số *obj* cho phép phương thức :meth:`~object.__get__` biết thư mục đích.  Tham số *objtype* là lớp *Directory*.


Thuộc tính được quản lý
-----------------------

Một cách sử dụng phổ biến của descriptor là quản lý quyền truy cập vào dữ liệu của instance. Descriptor được gán cho một thuộc tính public trong từ điển của class, còn dữ liệu thực tế được lưu trữ dưới dạng thuộc tính private trong từ điển của instance. Các phương thức :meth:`~object.__get__` và :meth:`~object.__set__` của descriptor được gọi khi thuộc tính public được truy cập.

Trong ví dụ sau, *age* là thuộc tính public còn *_age* là thuộc tính private. Khi thuộc tính public được truy cập, descriptor sẽ ghi nhật ký thao tác tra cứu hoặc cập nhật:

.. testcode::

    import logging

    logging.basicConfig(level=logging.INFO)

    class LoggedAgeAccess:

        def __get__(self, obj, objtype=None):
            value = obj._age
            logging.info('Accessing %r giving %r', 'age', value)
            return value

        def __set__(self, obj, value):
            logging.info('Updating %r to %r', 'age', value)
            obj._age = value

    class Person:

        age = LoggedAgeAccess()             # Instance descriptor

        def __init__(self, name, age):
            self.name = name                # Thuộc tính instance thông thường
            self.age = age                  # Gọi __set__()

        def birthday(self):
            self.age += 1                   # Gọi cả __get__() và __set__()


Một phiên tương tác cho thấy mọi quyền truy cập vào thuộc tính được quản lý *age* đều được ghi nhật ký, nhưng thuộc tính thông thường *name* thì không:

.. testcode::
    :hide:

    import logging, sys
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, force=True)

.. doctest::

    >>> mary = Person('Mary M', 30)         # Lần cập nhật age đầu tiên được ghi nhật ký
    INFO:root:Updating 'age' to 30
    >>> dave = Person('David D', 40)
    INFO:root:Updating 'age' to 40

    >>> vars(mary)                          # Dữ liệu thực tế nằm trong một thuộc tính riêng tư
    {'name': 'Mary M', '_age': 30}
    >>> vars(dave)
    {'name': 'David D', '_age': 40}

    >>> mary.age                            # Truy cập dữ liệu và ghi nhật ký việc tra cứu
    INFO:root:Accessing 'age' giving 30
    30
    >>> mary.birthday()                     # Các lần cập nhật cũng được ghi nhật ký
    INFO:root:Accessing 'age' giving 30
    INFO:root:Updating 'age' to 31

    >>> dave.name                           # Việc tra cứu thuộc tính thông thường không được ghi nhật ký
    'David D'
    >>> dave.age                            # Chỉ thuộc tính được quản lý được ghi nhật ký
    INFO:root:Accessing 'age' giving 40
    40

Một vấn đề lớn với ví dụ này là tên private *_age* được gán cố định trong lớp *LoggedAgeAccess*. Điều đó có nghĩa là mỗi instance chỉ có thể có một thuộc tính được ghi nhật ký và tên của thuộc tính đó không thể thay đổi. Trong ví dụ tiếp theo, chúng ta sẽ khắc phục vấn đề này.


Tên tùy chỉnh
-------------

Khi một lớp sử dụng descriptor, lớp đó có thể thông báo cho mỗi descriptor biết tên biến nào đã được sử dụng.

Trong ví dụ này, lớp :class:`!Person` có hai instance descriptor là *name* và *age*. Khi lớp :class:`!Person` được định nghĩa, lớp này gọi callback đến :meth:`~object.__set_name__` trong *LoggedAccess* để ghi lại tên các trường, nhờ đó mỗi descriptor có *public_name* và *private_name* riêng:

.. testcode::

    import logging

    logging.basicConfig(level=logging.INFO)

    class LoggedAccess:

        def __set_name__(self, owner, name):
            self.public_name = name
            self.private_name = '_' + name

        def __get__(self, obj, objtype=None):
            value = getattr(obj, self.private_name)
            logging.info('Accessing %r giving %r', self.public_name, value)
            return value

        def __set__(self, obj, value):
            logging.info('Updating %r to %r', self.public_name, value)
            setattr(obj, self.private_name, value)

    class Person:

        name = LoggedAccess()                # Instance descriptor thứ nhất
        age = LoggedAccess()                 # Instance descriptor thứ hai

        def __init__(self, name, age):
            self.name = name                 # Gọi descriptor thứ nhất
            self.age = age                   # Gọi descriptor thứ hai

        def birthday(self):
            self.age += 1

Một interactive session cho thấy class :class:`!Person` đã gọi
:meth:`~object.__set_name__` để các tên trường được ghi lại. Ở đây, chúng ta gọi :func:`vars` để tra cứu descriptor mà không kích hoạt nó:

.. doctest::

    >>> vars(vars(Person)['name'])
    {'public_name': 'name', 'private_name': '_name'}
    >>> vars(vars(Person)['age'])
    {'public_name': 'age', 'private_name': '_age'}

Giờ đây, class mới ghi nhật ký việc truy cập cả *name* và *age*:

.. testcode::
    :hide:

    import logging, sys
    logging.basicConfig(level=logging.INFO, stream=sys.stdout, force=True)

.. doctest::

    >>> pete = Person('Peter P', 10)
    INFO:root:Updating 'name' to 'Peter P'
    INFO:root:Updating 'age' to 10
    >>> kate = Person('Catherine C', 20)
    INFO:root:Updating 'name' to 'Catherine C'
    INFO:root:Updating 'age' to 20

Hai instance *Person* chỉ chứa các tên private:

.. doctest::

    >>> vars(pete)
    {'_name': 'Peter P', '_age': 10}
    >>> vars(kate)
    {'_name': 'Catherine C', '_age': 20}


Suy nghĩ cuối cùng
------------------

:term:`descriptor` là cách chúng ta gọi bất kỳ đối tượng nào định nghĩa :meth:`~object.__get__`,
:meth:`~object.__set__`, hoặc :meth:`~object.__delete__`.

Tùy chọn, descriptor có thể có phương thức :meth:`~object.__set_name__`. Phương thức này chỉ được sử dụng trong trường hợp descriptor cần biết lớp nơi nó được tạo hoặc tên của biến lớp mà nó được gán cho. (Phương thức này, nếu có, vẫn được gọi ngay cả khi lớp đó không phải là một descriptor.)

Descriptor được gọi bởi toán tử dấu chấm trong quá trình tra cứu thuộc tính. Nếu descriptor được truy cập gián tiếp bằng ``vars(some_class)[descriptor_name]``, thì đối tượng descriptor được trả về mà không gọi nó.

Descriptor chỉ hoạt động khi được sử dụng như biến lớp. Khi được đặt trong các instance, chúng không có tác dụng.

Động lực chính của descriptor là cung cấp một hook cho phép các đối tượng được lưu trong biến lớp kiểm soát điều gì xảy ra trong quá trình tra cứu thuộc tính.

Theo cách truyền thống, lớp gọi sẽ kiểm soát điều gì xảy ra trong quá trình tra cứu. Descriptor đảo ngược mối quan hệ đó và cho phép dữ liệu đang được tra cứu có tiếng nói trong vấn đề này.

Descriptor được sử dụng xuyên suốt ngôn ngữ. Đó là cách các hàm trở thành bound method. Những công cụ phổ biến như :deco:`classmethod`, :deco:`staticmethod`,
:deco:`property` và :deco:`functools.cached_property` đều được triển khai dưới dạng descriptor.


Ví dụ thực tế hoàn chỉnh
^^^^^^^^^^^^^^^^^^^^^^^^

Trong ví dụ này, chúng ta tạo một công cụ thực tế và mạnh mẽ để tìm các lỗi làm hỏng dữ liệu vốn nổi tiếng là rất khó phát hiện.


Lớp Validator
-------------

Validator là một descriptor để truy cập thuộc tính được quản lý. Trước khi lưu trữ bất kỳ dữ liệu nào, nó xác minh rằng giá trị mới đáp ứng nhiều ràng buộc khác nhau về kiểu và phạm vi. Nếu không đáp ứng các ràng buộc đó, nó sẽ raise một exception để ngăn dữ liệu bị hỏng ngay từ nguồn.

Lớp :class:`!Validator` này vừa là một :term:`abstract base class` vừa là một descriptor thuộc tính được quản lý:

.. testcode::

    from abc import ABC, abstractmethod

    class Validator(ABC):

        def __set_name__(self, owner, name):
            self.private_name = '_' + name

        def __get__(self, obj, objtype=None):
            return getattr(obj, self.private_name)

        def __set__(self, obj, value):
            self.validate(value)
            setattr(obj, self.private_name, value)

        @abstractmethod
        def validate(self, value):
            pass

Các validator tùy chỉnh cần kế thừa từ :class:`!Validator` và phải cung cấp một
Phương thức :meth:`!validate` dùng để kiểm tra các ràng buộc khác nhau khi cần.


Validator tùy chỉnh
-------------------

Dưới đây là ba tiện ích xác thực dữ liệu thiết thực:

1) :class:`!OneOf` xác minh rằng một giá trị là một trong số các tùy chọn bị giới hạn.

2) :class:`!Number` xác minh rằng một giá trị là một :class:`int` hoặc
   :class:`float`. Tùy chọn, nó xác minh rằng một giá trị nằm trong khoảng từ giá trị tối thiểu hoặc tối đa được chỉ định.

3) :class:`!String` xác minh rằng một giá trị là một :class:`str`. Tùy chọn, nó xác thực độ dài tối thiểu hoặc tối đa được chỉ định. Nó cũng có thể xác thực một `predicate <https://en.wikipedia.org/wiki/Predicate_(mathematical_logic)>`_ do người dùng định nghĩa.

.. testcode::

    class OneOf(Validator):

        def __init__(self, *options):
            self.options = set(options)

        def validate(self, value):
            if value not in self.options:
                raise ValueError(
                    f'Expected {value!r} to be one of {self.options!r}'
                )

    class Number(Validator):

        def __init__(self, minvalue=None, maxvalue=None):
            self.minvalue = minvalue
            self.maxvalue = maxvalue

        def validate(self, value):
            if not isinstance(value, (int, float)):
                raise TypeError(f'Expected {value!r} to be an int or float')
            if self.minvalue is not None and value < self.minvalue:
                raise ValueError(
                    f'Expected {value!r} to be at least {self.minvalue!r}'
                )
            if self.maxvalue is not None and value > self.maxvalue:
                raise ValueError(
                    f'Expected {value!r} to be no more than {self.maxvalue!r}'
                )

    class String(Validator):

        def __init__(self, minsize=None, maxsize=None, predicate=None):
            self.minsize = minsize
            self.maxsize = maxsize
            self.predicate = predicate

        def validate(self, value):
            if not isinstance(value, str):
                raise TypeError(f'Expected {value!r} to be a str')
            if self.minsize is not None and len(value) < self.minsize:
                raise ValueError(
                    f'Expected {value!r} to be no smaller than {self.minsize!r}'
                )
            if self.maxsize is not None and len(value) > self.maxsize:
                raise ValueError(
                    f'Expected {value!r} to be no bigger than {self.maxsize!r}'
                )
            if self.predicate is not None and not self.predicate(value):
                raise ValueError(
                    f'Expected {self.predicate} to be true for {value!r}'
                )


Ứng dụng thực tế
----------------

Sau đây là cách sử dụng các trình xác thực dữ liệu trong một class thực tế:

.. testcode::

    class Component:

        name = String(minsize=3, maxsize=10, predicate=str.isupper)
        kind = OneOf('wood', 'metal', 'plastic')
        quantity = Number(minvalue=0)

        def __init__(self, name, kind, quantity):
            self.name = name
            self.kind = kind
            self.quantity = quantity

Các descriptor ngăn không cho tạo ra các instance không hợp lệ:

.. doctest::

    >>> Component('Widget', 'metal', 5)      # Bị chặn: 'Widget' không viết toàn bộ bằng chữ hoa
    Traceback (most recent call last):
        ...
    ValueError: Expected <method 'isupper' of 'str' objects> to be true for 'Widget'

    >>> Component('WIDGET', 'metle', 5)      # Bị chặn: 'metle' bị viết sai chính tả
    Traceback (most recent call last):
        ...
    ValueError: Expected 'metle' to be one of {'metal', 'plastic', 'wood'}

    >>> Component('WIDGET', 'metal', -5)     # Bị chặn: -5 là số âm
    Traceback (most recent call last):
        ...
    ValueError: Expected -5 to be at least 0

    >>> Component('WIDGET', 'metal', 'V')    # Bị chặn: 'V' không phải là một số
    Traceback (most recent call last):
        ...
    TypeError: Expected 'V' to be an int or float

    >>> c = Component('WIDGET', 'metal', 5)  # Được phép: Các đầu vào hợp lệ


Hướng dẫn kỹ thuật
^^^^^^^^^^^^^^^^^^

Phần tiếp theo là hướng dẫn kỹ thuật chuyên sâu hơn về cơ chế và các chi tiết trong cách descriptor hoạt động.


Tóm tắt
-------

Định nghĩa descriptor, tóm tắt protocol và trình bày cách gọi descriptor. Cung cấp một ví dụ minh họa cách thức hoạt động của ánh xạ quan hệ đối tượng.

Việc tìm hiểu về descriptor không chỉ giúp bạn tiếp cận một bộ công cụ lớn hơn mà còn mang lại hiểu biết sâu sắc hơn về cách Python hoạt động.


Định nghĩa và giới thiệu
------------------------

Nói chung, descriptor là một giá trị thuộc tính có một trong các phương thức thuộc descriptor protocol. Các phương thức đó là :meth:`~object.__get__`, :meth:`~object.__set__` và :meth:`~object.__delete__`. Nếu bất kỳ phương thức nào trong số đó được định nghĩa cho một thuộc tính, thì thuộc tính đó được gọi là một :term:`descriptor`.

Hành vi mặc định khi truy cập thuộc tính là lấy, đặt hoặc xóa thuộc tính khỏi dictionary của một đối tượng. Ví dụ, ``a.x`` có chuỗi tra cứu bắt đầu bằng ``a.__dict__['x']``, tiếp đến là ``type(a).__dict__['x']``, rồi tiếp tục theo thứ tự phân giải phương thức của ``type(a)``. Nếu giá trị được tra cứu là một đối tượng định nghĩa một trong các phương thức descriptor, Python có thể ghi đè hành vi mặc định và gọi phương thức descriptor thay thế. Vị trí xảy ra việc này trong chuỗi ưu tiên phụ thuộc vào những phương thức descriptor nào được định nghĩa.

Descriptor là một protocol mạnh mẽ và đa dụng. Đây là cơ chế đứng sau property, method, static method, class method và
:func:`super`. Chúng được sử dụng xuyên suốt chính Python. Descriptor đơn giản hóa mã C bên dưới và cung cấp một tập hợp linh hoạt các công cụ mới cho những chương trình Python thường ngày.


Descriptor protocol
-------------------

``descr.__get__(self, obj, type=None)``

``descr.__set__(self, obj, value)``

``descr.__delete__(self, obj)``

Chỉ vậy thôi. Hãy định nghĩa bất kỳ phương thức nào trong số này, và một đối tượng sẽ được xem là descriptor, đồng thời có thể ghi đè hành vi mặc định khi được tra cứu dưới dạng thuộc tính.

Nếu một đối tượng định nghĩa :meth:`~object.__set__` hoặc :meth:`~object.__delete__`, thì đối tượng đó được xem là data descriptor. Descriptor chỉ định nghĩa :meth:`~object.__get__` được gọi là non-data descriptor (chúng thường được dùng cho method, nhưng cũng có thể dùng cho những mục đích khác).

Data descriptor và non-data descriptor khác nhau ở cách xác định việc ghi đè đối với các mục trong dictionary của một instance. Nếu dictionary của một instance có mục có cùng tên với một data descriptor, data descriptor sẽ được ưu tiên. Nếu dictionary của một instance có mục có cùng tên với một non-data descriptor, mục trong dictionary sẽ được ưu tiên.

Để tạo một data descriptor chỉ đọc, hãy định nghĩa cả :meth:`~object.__get__` và
:meth:`~object.__set__` với :meth:`~object.__set__` tạo ra một :exc:`AttributeError` khi được gọi. Chỉ cần định nghĩa phương thức :meth:`~object.__set__` với một placeholder tạo ra ngoại lệ là đủ để biến nó thành một data descriptor.


Tổng quan về việc gọi descriptor
--------------------------------

Một descriptor có thể được gọi trực tiếp bằng ``desc.__get__(obj)`` hoặc ``desc.__get__(None, cls)``.

Tuy nhiên, descriptor thường được tự động gọi khi truy cập thuộc tính.

Biểu thức ``obj.x`` tra cứu thuộc tính ``x`` trong chuỗi namespace của ``obj``. Nếu quá trình tìm kiếm tìm thấy một descriptor bên ngoài :attr:`~object.__dict__` của instance, phương thức :meth:`~object.__get__` của descriptor sẽ được gọi theo các quy tắc ưu tiên được liệt kê bên dưới.

Chi tiết về việc gọi phụ thuộc vào việc ``obj`` là một object, class hay instance của super.


Gọi từ một instance
-------------------

Việc tra cứu instance quét qua một chuỗi namespace, trong đó data descriptor có độ ưu tiên cao nhất, tiếp theo là biến instance, rồi đến non-data descriptor, biến class và cuối cùng là :meth:`~object.__getattr__` nếu được cung cấp.

Nếu tìm thấy một descriptor cho ``a.x``, descriptor đó sẽ được gọi với: ``desc.__get__(a, type(a))``.

Logic cho việc tra cứu bằng dấu chấm nằm trong :meth:`object.__getattribute__`. Sau đây là một phiên bản tương đương thuần Python:

.. testcode::

    def find_name_in_mro(cls, name, default):
        "Emulate _PyType_Lookup() in Objects/typeobject.c"
        for base in cls.__mro__:
            if name in vars(base):
                return vars(base)[name]
        return default

    def object_getattribute(obj, name):
        "Emulate PyObject_GenericGetAttr() in Objects/object.c"
        null = object()
        objtype = type(obj)
        cls_var = find_name_in_mro(objtype, name, null)
        descr_get = getattr(type(cls_var), '__get__', null)
        if descr_get is not null:
            if (hasattr(type(cls_var), '__set__')
                or hasattr(type(cls_var), '__delete__')):
                return descr_get(cls_var, obj, objtype)     # data descriptor
        if hasattr(obj, '__dict__') and name in vars(obj):
            return vars(obj)[name]                          # biến instance
        if descr_get is not null:
            return descr_get(cls_var, obj, objtype)         # descriptor không chứa dữ liệu
        if cls_var is not null:
            return cls_var                                  # biến lớp
        raise AttributeError(name)


.. testcode::
    :hide:

    # Kiểm tra độ trung thực của object_getattribute() bằng cách so sánh với
    # object.__getattribute__() thông thường.  Cái trước sẽ được truy cập bằng
    # dấu ngoặc vuông, còn cái sau bằng toán tử dấu chấm.

    class Object:

        def __getitem__(obj, name):
            try:
                return object_getattribute(obj, name)
            except AttributeError:
                if not hasattr(type(obj), '__getattr__'):
                    raise
            return type(obj).__getattr__(obj, name)             # __getattr__

    class DualOperator(Object):

        x = 10

        def __init__(self, z):
            self.z = z

        @property
        def p2(self):
            return 2 * self.x

        @property
        def p3(self):
            return 3 * self.x

        def m5(self, y):
            return 5 * y

        def m7(self, y):
            return 7 * y

        def __getattr__(self, name):
            return ('getattr_hook', self, name)

    class DualOperatorWithSlots:

        __getitem__ = Object.__getitem__

        __slots__ = ['z']

        x = 15

        def __init__(self, z):
            self.z = z

        @property
        def p2(self):
            return 2 * self.x

        def m5(self, y):
            return 5 * y

        def __getattr__(self, name):
            return ('getattr_hook', self, name)

    class D1:
        def __get__(self, obj, objtype=None):
            return type(self), obj, objtype

    class U1:
        x = D1()

    class U2(U1):
        pass

.. doctest::
    :hide:

    >>> a = DualOperator(11)
    >>> vars(a).update(p3 = '_p3', m7 = '_m7')
    >>> a.x == a['x'] == 10
    True
    >>> a.z == a['z'] == 11
    True
    >>> a.p2 == a['p2'] == 20
    True
    >>> a.p3 == a['p3'] == 30
    True
    >>> a.m5(100) == a.m5(100) == 500
    True
    >>> a.m7 == a['m7'] == '_m7'
    True
    >>> a.g == a['g'] == ('getattr_hook', a, 'g')
    True

    >>> b = DualOperatorWithSlots(22)
    >>> b.x == b['x'] == 15
    True
    >>> b.z == b['z'] == 22
    True
    >>> b.p2 == b['p2'] == 30
    True
    >>> b.m5(200) == b['m5'](200) == 1000
    True
    >>> b.g == b['g'] == ('getattr_hook', b, 'g')
    True

    >>> u2 = U2()
    >>> object_getattribute(u2, 'x') == u2.x == (D1, u2, U2)
    True

Lưu ý, không có hook :meth:`~object.__getattr__` trong mã :meth:`~object.__getattribute__`.  Vì vậy, việc gọi trực tiếp :meth:`~object.__getattribute__` hoặc gọi bằng ``super().__getattribute__`` sẽ hoàn toàn bỏ qua :meth:`~object.__getattr__`.

Thay vào đó, chính toán tử dấu chấm và hàm :func:`getattr` chịu trách nhiệm gọi :meth:`~object.__getattr__` mỗi khi :meth:`~object.__getattribute__` phát sinh :exc:`AttributeError`. Logic của chúng được đóng gói trong một hàm trợ giúp:

.. testcode::

    def getattr_hook(obj, name):
        "Emulate slot_tp_getattr_hook() in Objects/typeobject.c"
        try:
            return obj.__getattribute__(name)
        except AttributeError:
            if not hasattr(type(obj), '__getattr__'):
                raise
        return type(obj).__getattr__(obj, name)             # __getattr__

.. doctest::
    :hide:


    >>> class ClassWithGetAttr:
    ...     x = 123
    ...     def __getattr__(self, attr):
    ...         return attr.upper()
    ...
    >>> cw = ClassWithGetAttr()
    >>> cw.y = 456
    >>> getattr_hook(cw, 'x')
    123
    >>> getattr_hook(cw, 'y')
    456
    >>> getattr_hook(cw, 'z')
    'Z'

    >>> class ClassWithoutGetAttr:
    ...     x = 123
    ...
    >>> cwo = ClassWithoutGetAttr()
    >>> cwo.y = 456
    >>> getattr_hook(cwo, 'x')
    123
    >>> getattr_hook(cwo, 'y')
    456
    >>> getattr_hook(cwo, 'z')
    Traceback (most recent call last):
        ...
    AttributeError: 'ClassWithoutGetAttr' object has no attribute 'z'


Gọi từ một lớp
--------------

Logic để tra cứu có dấu chấm, chẳng hạn như ``A.x``, nằm trong
:meth:`!type.__getattribute__`. Các bước tương tự như đối với
:meth:`!object.__getattribute__`, nhưng việc tra cứu từ điển của instance được thay thế bằng quá trình tìm kiếm trong :term:`method resolution order` của lớp.

Nếu tìm thấy một descriptor, nó sẽ được gọi với ``desc.__get__(None, A)``.

Toàn bộ triển khai C có thể được tìm thấy trong :c:func:`!type_getattro` và
:c:func:`!_PyType_Lookup` trong :source:`Objects/typeobject.c`.


Gọi từ super
------------

Logic tra cứu dạng chấm của super nằm trong phương thức :meth:`~object.__getattribute__` của đối tượng được trả về bởi :func:`super`.

Một phép tra cứu dạng chấm như ``super(A, obj).m`` sẽ tìm kiếm ``obj.__class__.__mro__`` để tìm lớp cơ sở ``B`` ngay sau ``A``, rồi trả về ``B.__dict__['m'].__get__(obj, A)``. Nếu không phải là descriptor, ``m`` sẽ được trả về nguyên trạng.

Toàn bộ triển khai C có thể được tìm thấy trong :c:func:`!super_getattro` trong
:source:`Objects/typeobject.c`. Có thể tìm thấy phiên bản tương đương thuần Python trong `Guido's Tutorial <https://www.python.org/download/releases/2.2.3/descrintro/#cooperation>`_.


Tóm tắt logic gọi
-----------------

Cơ chế của descriptor được tích hợp trong các phương thức :meth:`~object.__getattribute__` dành cho :class:`object`, :class:`type` và :func:`super`.

Các điểm quan trọng cần ghi nhớ là:

* Descriptor được gọi bởi phương thức :meth:`~object.__getattribute__`.

* Các lớp kế thừa cơ chế này từ :class:`object`, :class:`type` hoặc
  :func:`super`.

* Việc ghi đè :meth:`~object.__getattribute__` sẽ ngăn các lệnh gọi descriptor tự động vì toàn bộ logic của descriptor nằm trong phương thức đó.

* :meth:`!object.__getattribute__` và :meth:`!type.__getattribute__` thực hiện các lệnh gọi khác nhau đến :meth:`~object.__get__`. Lệnh gọi đầu tiên bao gồm instance và có thể bao gồm class. Lệnh gọi thứ hai đưa ``None`` vào cho instance và luôn bao gồm class.

* Các descriptor dữ liệu luôn ghi đè lên dictionary của instance.

* Các descriptor không phải dữ liệu có thể bị dictionary của instance ghi đè.


Thông báo tên tự động
---------------------

Đôi khi, việc một descriptor biết tên biến lớp mà nó được gán vào là điều hữu ích. Khi một lớp mới được tạo, metaclass :class:`type` sẽ quét dictionary của lớp mới. Nếu bất kỳ mục nào là descriptor và định nghĩa :meth:`~object.__set_name__`, phương thức đó sẽ được gọi với hai đối số. *owner* là lớp nơi descriptor được sử dụng, còn *name* là biến lớp mà descriptor được gán vào.

Chi tiết triển khai nằm trong :c:func:`!type_new` và
:c:func:`!set_names` trong :source:`Objects/typeobject.c`.

Vì logic cập nhật nằm trong :meth:`!type.__new__`, thông báo chỉ diễn ra tại thời điểm tạo lớp. Nếu descriptor được thêm vào lớp sau đó, :meth:`~object.__set_name__` sẽ cần được gọi thủ công.


Ví dụ về ORM
------------

Đoạn mã sau đây là một skeleton đơn giản minh họa cách sử dụng các descriptor dữ liệu để triển khai `ánh xạ đối tượng-quan hệ <https://en.wikipedia.org/wiki/Object%E2%80%93relational_mapping>`_.

Ý tưởng cốt lõi là dữ liệu được lưu trữ trong một cơ sở dữ liệu bên ngoài. Các instance Python chỉ lưu các khóa trỏ đến các bảng trong cơ sở dữ liệu. Descriptor sẽ xử lý việc tra cứu hoặc cập nhật:

.. testcode::

    class Field:

        def __set_name__(self, owner, name):
            self.fetch = f'SELECT {name} FROM {owner.table} WHERE {owner.key}=?;'
            self.store = f'UPDATE {owner.table} SET {name}=? WHERE {owner.key}=?;'

        def __get__(self, obj, objtype=None):
            return conn.execute(self.fetch, [obj.key]).fetchone()[0]

        def __set__(self, obj, value):
            conn.execute(self.store, [value, obj.key])
            conn.commit()

Chúng ta có thể sử dụng lớp :class:`!Field` để định nghĩa `các mô hình <https://en.wikipedia.org/wiki/Database_model>`_ mô tả schema cho từng bảng trong cơ sở dữ liệu:

.. testcode::

    class Movie:
        table = 'Movies'                    # Tên bảng
        key = 'title'                       # Khóa chính
        director = Field()
        year = Field()

        def __init__(self, key):
            self.key = key

    class Song:
        table = 'Music'
        key = 'title'
        artist = Field()
        year = Field()
        genre = Field()

        def __init__(self, key):
            self.key = key

Để sử dụng các mô hình, trước tiên hãy kết nối với cơ sở dữ liệu::

    >>> import sqlite3
    >>> conn = sqlite3.connect('entertainment.db')

Một phiên tương tác cho thấy cách truy xuất dữ liệu từ cơ sở dữ liệu và cách cập nhật dữ liệu đó:

.. testsetup::

    song_data = [
        ('Country Roads', 'John Denver', 1972),
        ('Me and Bobby McGee', 'Janice Joplin', 1971),
        ('Coal Miners Daughter', 'Loretta Lynn', 1970),
    ]

    movie_data = [
        ('Star Wars', 'George Lucas', 1977),
        ('Jaws', 'Steven Spielberg', 1975),
        ('Aliens', 'James Cameron', 1986),
    ]

    import sqlite3

    conn = sqlite3.connect(':memory:')
    conn.execute('CREATE TABLE Music (title text, artist text, year integer);')
    conn.execute('CREATE INDEX MusicNdx ON Music (title);')
    conn.executemany('INSERT INTO Music VALUES (?, ?, ?);', song_data)
    conn.execute('CREATE TABLE Movies (title text, director text, year integer);')
    conn.execute('CREATE INDEX MovieNdx ON Music (title);')
    conn.executemany('INSERT INTO Movies VALUES (?, ?, ?);', movie_data)
    conn.commit()

.. doctest::

    >>> Movie('Star Wars').director
    'George Lucas'
    >>> jaws = Movie('Jaws')
    >>> f'Released in {jaws.year} by {jaws.director}'
    'Released in 1975 by Steven Spielberg'

    >>> Song('Country Roads').artist
    'John Denver'

    >>> Movie('Star Wars').director = 'J.J. Abrams'
    >>> Movie('Star Wars').director
    'J.J. Abrams'

.. testcleanup::

   conn.close()


Các tương đương bằng Python thuần túy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Protocol descriptor rất đơn giản và mở ra nhiều khả năng thú vị. Một số trường hợp sử dụng phổ biến đến mức đã được đóng gói sẵn thành các công cụ tích hợp. Properties, bound methods, static methods, class methods và \_\_slots\_\_ đều dựa trên protocol descriptor.


Properties
----------

Gọi :func:`property` là một cách súc tích để xây dựng một data descriptor, trong đó kích hoạt một lời gọi hàm khi truy cập một thuộc tính. Chữ ký của nó là::

    property(fget=None, fset=None, fdel=None, doc=None) -> property

Tài liệu minh họa một cách sử dụng điển hình để định nghĩa một managed attribute ``x``:

.. testcode::

    class C:
        def getx(self): return self.__x
        def setx(self, value): self.__x = value
        def delx(self): del self.__x
        x = property(getx, setx, delx, "I'm the 'x' property.")

.. doctest::
    :hide:

    >>> C.x.__doc__
    "I'm the 'x' property."
    >>> c.x = 2.71828
    >>> c.x
    2.71828
    >>> del c.x
    >>> c.x
    Traceback (most recent call last):
      ...
    AttributeError: 'C' object has no attribute '_C__x'

Để xem :func:`property` được triển khai như thế nào theo protocol descriptor, sau đây là một tương đương bằng Python thuần túy triển khai hầu hết chức năng cốt lõi:

.. testcode::

    class Property:
        "Emulate PyProperty_Type() in Objects/descrobject.c"

        def __init__(self, fget=None, fset=None, fdel=None, doc=None):
            self.fget = fget
            self.fset = fset
            self.fdel = fdel
            if doc is None and fget is not None:
                doc = fget.__doc__
            self.__doc__ = doc

        def __set_name__(self, owner, name):
            self.__name__ = name

        def __get__(self, obj, objtype=None):
            if obj is None:
                return self
            if self.fget is None:
                raise AttributeError
            return self.fget(obj)

        def __set__(self, obj, value):
            if self.fset is None:
                raise AttributeError
            self.fset(obj, value)

        def __delete__(self, obj):
            if self.fdel is None:
                raise AttributeError
            self.fdel(obj)

        def getter(self, fget):
            return type(self)(fget, self.fset, self.fdel, self.__doc__)

        def setter(self, fset):
            return type(self)(self.fget, fset, self.fdel, self.__doc__)

        def deleter(self, fdel):
            return type(self)(self.fget, self.fset, fdel, self.__doc__)

.. testcode::
    :hide:

    # Xác minh mô phỏng Property()

    class CC:
        def getx(self):
            return self.__x
        def setx(self, value):
            self.__x = value
        def delx(self):
            del self.__x
        x = Property(getx, setx, delx, "I'm the 'x' property.")
        no_getter = Property(None, setx, delx, "I'm the 'x' property.")
        no_setter = Property(getx, None, delx, "I'm the 'x' property.")
        no_deleter = Property(getx, setx, None, "I'm the 'x' property.")
        no_doc = Property(getx, setx, delx, None)


    # Bây giờ thực hiện lại nhưng sử dụng kiểu decorator

    class CCC:
        @Property
        def x(self):
            return self.__x
        @x.setter
        def x(self, value):
            self.__x = value
        @x.deleter
        def x(self):
            del self.__x


.. doctest::
    :hide:

    >>> cc = CC()
    >>> hasattr(cc, 'x')
    False
    >>> cc.x = 33
    >>> cc.x
    33
    >>> del cc.x
    >>> hasattr(cc, 'x')
    False

    >>> ccc = CCC()
    >>> hasattr(ccc, 'x')
    False
    >>> ccc.x = 333
    >>> ccc.x == 333
    True
    >>> del ccc.x
    >>> hasattr(ccc, 'x')
    False

    >>> cc = CC()
    >>> cc.x = 33
    >>> try:
    ...     cc.no_getter
    ... except AttributeError as e:
    ...     type(e).__name__
    ...
    'AttributeError'

    >>> try:
    ...     cc.no_setter = 33
    ... except AttributeError as e:
    ...     type(e).__name__
    ...
    'AttributeError'

    >>> try:
    ...     del cc.no_deleter
    ... except AttributeError as e:
    ...     type(e).__name__
    ...
    'AttributeError'

    >>> CC.no_doc.__doc__ is None
    True

Builtin :func:`property` hữu ích bất cứ khi nào một giao diện người dùng đã cho phép truy cập thuộc tính, rồi các thay đổi tiếp theo yêu cầu sự can thiệp của một method.

Ví dụ, một class bảng tính có thể cho phép truy cập giá trị của một ô thông qua ``Cell('b10').value``. Những cải tiến tiếp theo đối với chương trình yêu cầu ô phải được tính toán lại sau mỗi lần truy cập; tuy nhiên, lập trình viên không muốn ảnh hưởng đến mã client hiện có đang truy cập trực tiếp vào thuộc tính. Giải pháp là bọc quyền truy cập vào thuộc tính value trong một property data descriptor:

.. testcode::

    class Cell:
        ...

        @property
        def value(self):
            "Recalculate the cell before returning value"
            self.recalc()
            return self._value

Trong ví dụ này, builtin :func:`property` hoặc phiên bản tương đương :func:`!Property` của chúng ta đều hoạt động.


Functions và methods
--------------------

Các tính năng hướng đối tượng của Python được xây dựng trên một môi trường dựa trên function. Nhờ sử dụng non-data descriptor, hai khái niệm này được hợp nhất một cách liền mạch.

Các hàm được lưu trong từ điển lớp sẽ được chuyển thành các method khi được gọi. Method chỉ khác hàm thông thường ở chỗ instance của đối tượng được thêm vào trước các đối số còn lại. Theo quy ước, instance được gọi là *self*, nhưng cũng có thể được gọi là *this* hoặc bất kỳ tên biến nào khác.

Có thể tạo method thủ công bằng :class:`types.MethodType`, tương đương về cơ bản với:

.. testcode::

    class MethodType:
        "Emulate PyMethod_Type in Objects/classobject.c"

        def __init__(self, func, obj):
            self.__func__ = func
            self.__self__ = obj

        def __call__(self, *args, **kwargs):
            func = self.__func__
            obj = self.__self__
            return func(obj, *args, **kwargs)

        def __getattribute__(self, name):
            "Emulate method_getset() in Objects/classobject.c"
            if name == '__doc__':
                return self.__func__.__doc__
            return object.__getattribute__(self, name)

        def __getattr__(self, name):
            "Emulate method_getattro() in Objects/classobject.c"
            return getattr(self.__func__, name)

        def __get__(self, obj, objtype=None):
            "Emulate method_descr_get() in Objects/classobject.c"
            return self

Để hỗ trợ việc tự động tạo method, các hàm bao gồm
:meth:`~object.__get__` method để liên kết các method trong quá trình truy cập thuộc tính. Điều này có nghĩa là các hàm là descriptor không phải dữ liệu, trả về các bound method trong quá trình tra cứu bằng dấu chấm từ một instance. Cách hoạt động như sau:

.. testcode::

    class Function:
        ...

        def __get__(self, obj, objtype=None):
            "Simulate func_descr_get() in Objects/funcobject.c"
            if obj is None:
                return self
            return MethodType(self, obj)

Chạy lớp sau trong interpreter cho thấy descriptor của hàm hoạt động trên thực tế như thế nào:

.. testcode::

    class D:
        def f(self):
             return self

    class D2:
        pass

.. doctest::
    :hide:

    >>> d = D()
    >>> d2 = D2()
    >>> d2.f = d.f.__get__(d2, D2)
    >>> d2.f() is d
    True

Hàm có thuộc tính :term:`qualified name` để hỗ trợ việc introspection:

.. doctest::

    >>> D.f.__qualname__
    'D.f'

Truy cập hàm thông qua từ điển lớp không gọi
:meth:`~object.__get__`.  Thay vào đó, nó chỉ trả về đối tượng hàm nền tảng::

    >>> D.__dict__['f']
    <function D.f at 0x00C45070>

Truy cập bằng dấu chấm từ một class gọi :meth:`~object.__get__`, vốn chỉ trả về hàm nền tảng mà không thay đổi::

    >>> D.f
    <function D.f at 0x00C45070>

Hành vi đáng chú ý xảy ra khi truy cập bằng dấu chấm từ một instance.  Việc tra cứu bằng dấu chấm gọi :meth:`~object.__get__`, vốn trả về một đối tượng bound method::

    >>> d = D()
    >>> d.f
    <bound method D.f of <__main__.D object at 0x00B18C90>>

Bên trong, bound method lưu trữ hàm nền tảng và instance đã được liên kết::

    >>> d.f.__func__
    <function D.f at 0x00C45070>

    >>> d.f.__self__
    <__main__.D object at 0x00B18C90>

Nếu bạn từng thắc mắc *self* trong các method thông thường hoặc *cls* trong các class method bắt nguồn từ đâu, thì đây chính là câu trả lời!


Các loại method
---------------

Các non-data descriptor cung cấp một cơ chế đơn giản cho những biến thể của các mẫu thông thường dùng để liên kết các hàm thành method.

Tóm lại, các hàm có phương thức :meth:`~object.__get__` để chúng có thể được chuyển đổi thành một method khi được truy cập dưới dạng thuộc tính. Descriptor không dữ liệu sẽ chuyển một lệnh gọi ``obj.f(*args)`` thành ``f(obj, *args)``. Việc gọi ``cls.f(*args)`` sẽ trở thành ``f(*args)``.

Bảng này tóm tắt binding và hai biến thể hữu ích nhất của nó:

      +--------------+------------------------+-----------------------+
      | Chuyển đổi   | Được gọi từ một object | Được gọi từ một class |
      +==============+========================+=======================+
      | hàm          | f(obj, \*args)         | f(\*args)             |
      +--------------+------------------------+-----------------------+
      | staticmethod | f(\*args)              | f(\*args)             |
      +--------------+------------------------+-----------------------+
      | classmethod  | f(type(obj), \*args)   | f(cls, \*args)        |
      +--------------+------------------------+-----------------------+


Phương thức static
------------------

Phương thức static trả về hàm bên dưới mà không thay đổi. Việc gọi ``c.f`` hoặc ``C.f`` tương đương với việc tra cứu trực tiếp trong ``object.__getattribute__(c, "f")`` hoặc ``object.__getattribute__(C, "f")``. Do đó, hàm có thể được truy cập giống hệt nhau từ một object hoặc một class.

Các ứng viên phù hợp cho phương thức static là những phương thức không tham chiếu đến biến ``self``.

Ví dụ, một package thống kê có thể bao gồm một container class dành cho dữ liệu thực nghiệm. Class này cung cấp các phương thức thông thường để tính giá trị trung bình, mean, median và các thống kê mô tả khác phụ thuộc vào dữ liệu. Tuy nhiên, có thể có những hàm hữu ích về mặt khái niệm có liên quan nhưng không phụ thuộc vào dữ liệu. Chẳng hạn, ``erf(x)`` là một routine chuyển đổi tiện dụng thường xuất hiện trong công việc thống kê nhưng không phụ thuộc trực tiếp vào một dataset cụ thể. Nó có thể được gọi từ một object hoặc class: ``s.erf(1.5) --> 0.9332`` hoặc ``Sample.erf(1.5) --> 0.9332``.

Vì phương thức static trả về hàm bên dưới mà không thay đổi, các lệnh gọi trong ví dụ không có gì đặc biệt:

.. testcode::

    class E:
        @staticmethod
        def f(x):
            return x * 10

.. doctest::

    >>> E.f(3)
    30
    >>> E().f(3)
    30

Sử dụng non-data descriptor protocol, phiên bản Python thuần của
:deco:`staticmethod` sẽ trông như sau:

.. testcode::

    import functools

    class StaticMethod:
        "Emulate PyStaticMethod_Type() in Objects/funcobject.c"

        def __init__(self, f):
            self.f = f
            functools.update_wrapper(self, f)

        def __get__(self, obj, objtype=None):
            return self.f

        def __call__(self, *args, **kwds):
            return self.f(*args, **kwds)

        @property
        def __annotations__(self):
            return self.f.__annotations__

Lệnh gọi :func:`functools.update_wrapper` thêm một thuộc tính ``__wrapped__`` tham chiếu đến hàm bên dưới. Đồng thời, nó chuyển tiếp các thuộc tính cần thiết để wrapper trông giống hàm được bọc, bao gồm :attr:`~function.__name__`, :attr:`~function.__qualname__` và :attr:`~function.__doc__`.

.. testcode::
    :hide:

    class E_sim:
        @StaticMethod
        def f(x: int) -> str:
            "Simple function example"
            return "!" * x

    wrapped_ord = StaticMethod(ord)

.. doctest::
    :hide:

    >>> E_sim.f(3)
    '!!!'
    >>> E_sim().f(3)
    '!!!'

    >>> sm = vars(E_sim)['f']
    >>> type(sm).__name__
    'StaticMethod'
    >>> f = E_sim.f
    >>> type(f).__name__
    'function'
    >>> sm.__name__
    'f'
    >>> f.__name__
    'f'
    >>> sm.__qualname__
    'E_sim.f'
    >>> f.__qualname__
    'E_sim.f'
    >>> sm.__doc__
    'Simple function example'
    >>> f.__doc__
    'Simple function example'
    >>> sm.__annotations__
    {'x': <class 'int'>, 'return': <class 'str'>}
    >>> f.__annotations__
    {'x': <class 'int'>, 'return': <class 'str'>}
    >>> sm.__module__ == f.__module__
    True
    >>> sm(3)
    '!!!'
    >>> f(3)
    '!!!'

    >>> wrapped_ord('A')
    65
    >>> wrapped_ord.__module__ == ord.__module__
    True
    >>> wrapped_ord.__wrapped__ == ord
    True
    >>> wrapped_ord.__name__ == ord.__name__
    True
    >>> wrapped_ord.__qualname__ == ord.__qualname__
    True
    >>> wrapped_ord.__doc__ == ord.__doc__
    True


Phương thức lớp
---------------

Không giống phương thức tĩnh, phương thức lớp thêm tham chiếu đến lớp vào đầu danh sách đối số trước khi gọi hàm. Định dạng này giống nhau bất kể bên gọi là một đối tượng hay một lớp:

.. testcode::

    class F:
        @classmethod
        def f(cls, x):
            return cls.__name__, x

.. doctest::

    >>> F.f(3)
    ('F', 3)
    >>> F().f(3)
    ('F', 3)

Cách hoạt động này hữu ích whenever phương thức chỉ cần một tham chiếu đến lớp và không phụ thuộc vào dữ liệu được lưu trong một instance cụ thể. Một cách sử dụng của phương thức lớp là tạo các constructor thay thế cho lớp. Ví dụ, classmethod :func:`dict.fromkeys` tạo một dictionary mới từ danh sách các khóa. Cách tương đương bằng Python thuần là:

.. testcode::

    class Dict(dict):
        @classmethod
        def fromkeys(cls, iterable, value=None):
            "Emulate dict_fromkeys() in Objects/dictobject.c"
            d = cls()
            for key in iterable:
                d[key] = value
            return d

Giờ đây, bạn có thể tạo một dictionary mới gồm các khóa duy nhất như sau:

.. doctest::

    >>> d = Dict.fromkeys('abracadabra')
    >>> type(d) is Dict
    True
    >>> d
    {'a': None, 'b': None, 'r': None, 'c': None, 'd': None}

Sử dụng non-data descriptor protocol, phiên bản Python thuần của
:deco:`classmethod` sẽ có dạng như sau:

.. testcode::

    import functools

    class ClassMethod:
        "Emulate PyClassMethod_Type() in Objects/funcobject.c"

        def __init__(self, f):
            self.f = f
            functools.update_wrapper(self, f)

        def __get__(self, obj, cls=None):
            if cls is None:
                cls = type(obj)
            return MethodType(self.f, cls)

.. testcode::
    :hide:

    # Kiểm tra mô phỏng hoạt động
    class T:
        @ClassMethod
        def cm(cls, x: int, y: str) -> tuple[str, int, str]:
            "Class method that returns a tuple"
            return (cls.__name__, x, y)


.. doctest::
    :hide:

    >>> T.cm(11, 22)
    ('T', 11, 22)

    # Cũng gọi nó từ một instance
    >>> t = T()
    >>> t.cm(11, 22)
    ('T', 11, 22)

    # Kiểm tra T sử dụng mô phỏng của chúng ta
    >>> type(vars(T)['cm']).__name__
    'ClassMethod'

    # Kiểm tra update_wrapper() đã sao chép đúng các thuộc tính
    >>> T.cm.__name__
    'cm'
    >>> T.cm.__qualname__
    'T.cm'
    >>> T.cm.__doc__
    'Class method that returns a tuple'
    >>> T.cm.__annotations__
    {'x': <class 'int'>, 'y': <class 'str'>, 'return': tuple[str, int, str]}

    # Kiểm tra __wrapped__ đã được thêm và hoạt động đúng
    >>> f = vars(T)['cm'].__wrapped__
    >>> type(f).__name__
    'function'
    >>> f.__name__
    'cm'
    >>> f(T, 11, 22)
    ('T', 11, 22)


Lệnh gọi :func:`functools.update_wrapper` trong ``ClassMethod`` thêm một thuộc tính ``__wrapped__`` tham chiếu đến hàm bên dưới. Nó cũng giữ lại các thuộc tính cần thiết để wrapper trông giống như hàm được bọc: :attr:`~function.__name__`,
:attr:`~function.__qualname__`, :attr:`~function.__doc__` và :attr:`~function.__annotations__`.


Đối tượng thành viên và __slots__
---------------------------------

Khi một lớp định nghĩa ``__slots__``, nó thay thế các dictionary của instance bằng một mảng có độ dài cố định chứa các giá trị slot. Từ góc nhìn người dùng, điều này có một số tác động:

1. Phát hiện ngay các lỗi do viết sai tên thuộc tính
khi gán. Chỉ cho phép các tên thuộc tính được chỉ định trong ``__slots__``:

.. testcode::

        class Vehicle:
            __slots__ = ('id_number', 'make', 'model')

.. doctest::

        >>> auto = Vehicle()
        >>> auto.id_nubmer = 'VYE483814LQEX'
        Traceback (most recent call last):
            ...
        AttributeError: 'Vehicle' object has no attribute 'id_nubmer'

2. Giúp tạo các đối tượng bất biến, trong đó descriptor quản lý quyền truy cập vào các
thuộc tính được lưu trữ trong ``__slots__``:

.. testcode::

    class Immutable:

        __slots__ = ('_dept', '_name')          # Thay thế dictionary của instance

        def __init__(self, dept, name):
            self._dept = dept                   # Lưu vào thuộc tính riêng tư
            self._name = name                   # Lưu vào thuộc tính riêng tư

        @property                               # Descriptor chỉ đọc
        def dept(self):
            return self._dept

        @property
        def name(self):                         # Descriptor chỉ đọc
            return self._name

.. doctest::

    >>> mark = Immutable('Botany', 'Mark Watney')
    >>> mark.dept
    'Botany'
    >>> mark.dept = 'Space Pirate'
    Traceback (most recent call last):
        ...
    AttributeError: property 'dept' of 'Immutable' object has no setter
    >>> mark.location = 'Mars'
    Traceback (most recent call last):
        ...
    AttributeError: 'Immutable' object has no attribute 'location'

3. Giúp tiết kiệm bộ nhớ. Trên bản dựng Linux 64-bit, một thể hiện có hai thuộc tính
chiếm 48 byte với ``__slots__`` và 152 byte nếu không có. Mẫu thiết kế `flyweight <https://en.wikipedia.org/wiki/Flyweight_pattern>`_ này có lẽ chỉ quan trọng khi sẽ tạo một số lượng lớn các thể hiện.

4. Cải thiện tốc độ. Việc đọc các biến của thể hiện nhanh hơn 35% với
``__slots__`` (được đo bằng Python 3.10 trên bộ xử lý Apple M1).

5. Ngăn các công cụ như :deco:`functools.cached_property`, vốn yêu cầu một
từ điển instance để hoạt động chính xác:

.. testcode::

    from functools import cached_property

    class CP:
        __slots__ = ()                          # Loại bỏ dict của instance

        @cached_property                        # Yêu cầu dict của instance
        def pi(self):
            return 4 * sum((-1.0)**n / (2.0*n + 1.0)
                           for n in reversed(range(100_000)))

.. doctest::

    >>> CP().pi
    Traceback (most recent call last):
      ...
    TypeError: No '__dict__' attribute on 'CP' instance to cache 'pi' property.

Không thể tạo một phiên bản Python thuần túy thay thế trực tiếp và chính xác cho ``__slots__`` vì nó yêu cầu quyền truy cập trực tiếp vào các cấu trúc C và quyền kiểm soát việc cấp phát bộ nhớ cho đối tượng. Tuy nhiên, ta có thể xây dựng một mô phỏng tương đối trung thực, trong đó cấu trúc C thực tế dành cho các slot được mô phỏng bằng một danh sách ``_slotvalues`` riêng tư. Các thao tác đọc và ghi vào cấu trúc riêng tư đó được quản lý bởi các member descriptor:

.. testcode::

    null = object()

    class Member:

        def __init__(self, name, clsname, offset):
            'Emulate PyMemberDef in Include/descrobject.h'
            # Xem thêm descr_new() trong Objects/descrobject.c
            self.name = name
            self.clsname = clsname
            self.offset = offset

        def __get__(self, obj, objtype=None):
            'Emulate member_get() in Objects/descrobject.c'
            # Xem thêm PyMember_GetOne() trong Python/structmember.c
            if obj is None:
                return self
            value = obj._slotvalues[self.offset]
            if value is null:
                raise AttributeError(self.name)
            return value

        def __set__(self, obj, value):
            'Emulate member_set() in Objects/descrobject.c'
            obj._slotvalues[self.offset] = value

        def __delete__(self, obj):
            'Emulate member_delete() in Objects/descrobject.c'
            value = obj._slotvalues[self.offset]
            if value is null:
                raise AttributeError(self.name)
            obj._slotvalues[self.offset] = null

        def __repr__(self):
            'Emulate member_repr() in Objects/descrobject.c'
            return f'<Member {self.name!r} of {self.clsname!r}>'

Phương thức :meth:`!type.__new__` đảm nhiệm việc thêm các đối tượng member vào các biến lớp:

.. testcode::

    class Type(type):
        'Simulate how the type metaclass adds member objects for slots'

        def __new__(mcls, clsname, bases, mapping, **kwargs):
            'Emulate type_new() in Objects/typeobject.c'
            # type_new() gọi PyTypeReady(), rồi gọi add_methods()
            slot_names = mapping.get('slot_names', [])
            for offset, name in enumerate(slot_names):
                mapping[name] = Member(name, clsname, offset)
            return type.__new__(mcls, clsname, bases, mapping, **kwargs)

Phương thức :meth:`object.__new__` đảm nhiệm việc tạo các instance có slots thay vì dictionary của instance. Đây là một mô phỏng sơ lược bằng Python thuần:

.. testcode::

    class Object:
        'Simulate how object.__new__() allocates memory for __slots__'

        def __new__(cls, *args, **kwargs):
            'Emulate object_new() in Objects/typeobject.c'
            inst = super().__new__(cls)
            if hasattr(cls, 'slot_names'):
                empty_slots = [null] * len(cls.slot_names)
                object.__setattr__(inst, '_slotvalues', empty_slots)
            return inst

        def __setattr__(self, name, value):
            'Emulate _PyObject_GenericSetAttrWithDict() Objects/object.c'
            cls = type(self)
            if hasattr(cls, 'slot_names') and name not in cls.slot_names:
                raise AttributeError(
                    f'{cls.__name__!r} object has no attribute {name!r}'
                )
            super().__setattr__(name, value)

        def __delattr__(self, name):
            'Emulate _PyObject_GenericSetAttrWithDict() Objects/object.c'
            cls = type(self)
            if hasattr(cls, 'slot_names') and name not in cls.slot_names:
                raise AttributeError(
                    f'{cls.__name__!r} object has no attribute {name!r}'
                )
            super().__delattr__(name)

Để sử dụng mô phỏng này trong một class thực, chỉ cần kế thừa từ :class:`!Object` và đặt :term:`metaclass` thành :class:`Type`:

.. testcode::

    class H(Object, metaclass=Type):
        'Instance variables stored in slots'

        slot_names = ['x', 'y']

        def __init__(self, x, y):
            self.x = x
            self.y = y

Tại thời điểm này, metaclass đã nạp các đối tượng member cho *x* và *y*::

    >>> from pprint import pp
    >>> pp(dict(vars(H)))
    {'__module__': '__main__',
     '__doc__': 'Instance variables stored in slots',
     'slot_names': ['x', 'y'],
     '__init__': <function H.__init__ at 0x7fb5d302f9d0>,
     'x': <Member 'x' of 'H'>,
     'y': <Member 'y' of 'H'>}

.. doctest::
    :hide:

    # Chúng tôi kiểm thử riêng phần này vì phần trước không
    # có thể kiểm thử bằng doctest do địa chỉ bộ nhớ dạng hex của hàm __init__
    >>> isinstance(vars(H)['x'], Member)
    True
    >>> isinstance(vars(H)['y'], Member)
    True

Khi các instance được tạo, chúng có một danh sách ``slot_values`` nơi các thuộc tính được lưu trữ:

.. doctest::

    >>> h = H(10, 20)
    >>> vars(h)
    {'_slotvalues': [10, 20]}
    >>> h.x = 55
    >>> vars(h)
    {'_slotvalues': [55, 20]}

Các thuộc tính bị viết sai hoặc chưa được gán sẽ gây ra một ngoại lệ:

.. doctest::

    >>> h.xz
    Traceback (most recent call last):
        ...
    AttributeError: 'H' object has no attribute 'xz'

.. doctest::
   :hide:

    # Examples for deleted attributes are not shown because this section
    # is already a bit lengthy.  We still test that code here.
    >>> del h.x
    >>> hasattr(h, 'x')
    False

    # Also test the code for uninitialized slots
    >>> class HU(Object, metaclass=Type):
    ...     slot_names = ['x', 'y']
    ...
    >>> hu = HU()
    >>> hasattr(hu, 'x')
    False
    >>> hasattr(hu, 'y')
    False

.. _`predicate`: https://en.wikipedia.org/wiki/Predicate_(mathematical_logic)
.. _`Guido's Tutorial`: https://www.python.org/download/releases/2.2.3/descrintro/#cooperation
.. _`object relational mapping`: https://en.wikipedia.org/wiki/Object%E2%80%93relational_mapping
.. _`models`: https://en.wikipedia.org/wiki/Database_model
.. _`flyweight design pattern`: https://en.wikipedia.org/wiki/Flyweight_pattern
