:mod:`!unittest.mock` --- bắt đầu sử dụng
=========================================

.. moduleauthor:: Michael Foord <michael@python.org>
.. currentmodule:: unittest.mock

.. versionadded:: 3.3


.. _getting-started:


.. testsetup::

    import asyncio
    import unittest
    from unittest.mock import Mock, MagicMock, AsyncMock, patch, call, sentinel

    class SomeClass:
        attribute = 'this is a doctest'

        @staticmethod
        def static_method():
            pass

Sử dụng Mock
------------

Patch phương thức bằng Mock
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Các cách sử dụng phổ biến cho đối tượng :class:`Mock` bao gồm:

* Patch phương thức
* Ghi lại các lệnh gọi phương thức trên đối tượng

Bạn có thể muốn thay thế một phương thức trên một đối tượng để kiểm tra rằng phương thức đó được một phần khác của hệ thống gọi với các đối số chính xác:

    >>> real = SomeClass()
    >>> real.method = MagicMock(name='method')
    >>> real.method(3, 4, 5, key='value')
    <MagicMock name='method()' id='...'>

Sau khi mock của chúng ta đã được sử dụng (``real.method`` trong ví dụ này), nó có các phương thức và thuộc tính cho phép bạn kiểm tra cách nó đã được sử dụng.

.. note::

    Trong hầu hết các ví dụ này, hai lớp :class:`Mock` và :class:`MagicMock` có thể thay thế cho nhau. Vì ``MagicMock`` là lớp có nhiều khả năng hơn, nên việc sử dụng lớp này làm mặc định là hợp lý.

Sau khi mock được gọi, thuộc tính :attr:`~Mock.called` của nó được đặt thành ``True``. Quan trọng hơn, chúng ta có thể sử dụng :meth:`~Mock.assert_called_with` hoặc
phương thức :meth:`~Mock.assert_called_once_with` để kiểm tra rằng nó đã được gọi với các đối số chính xác.

Ví dụ này kiểm tra rằng việc gọi ``ProductionClass().method`` sẽ dẫn đến một lần gọi phương thức ``something``:

    >>> class ProductionClass:
    ...     def method(self):
    ...         self.something(1, 2, 3)
    ...     def something(self, a, b, c):
    ...         pass
    ...
    >>> real = ProductionClass()
    >>> real.something = MagicMock()
    >>> real.method()
    >>> real.something.assert_called_once_with(1, 2, 3)



Mock cho các lần gọi phương thức trên một đối tượng
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Trong ví dụ trước, chúng ta đã patch trực tiếp một phương thức trên một đối tượng để kiểm tra rằng nó được gọi chính xác. Một trường hợp sử dụng phổ biến khác là truyền một đối tượng vào một phương thức (hoặc một phần nào đó của hệ thống đang được kiểm thử), rồi kiểm tra rằng đối tượng đó được sử dụng đúng cách.

``ProductionClass`` đơn giản dưới đây có một phương thức ``closer``. Nếu được gọi với một đối tượng, nó sẽ gọi ``close`` trên đối tượng đó.

    >>> class ProductionClass:
    ...     def closer(self, something):
    ...         something.close()
    ...

Vì vậy, để kiểm thử, chúng ta cần truyền vào một đối tượng có phương thức ``close`` và kiểm tra xem phương thức đó có được gọi đúng cách hay không.

    >>> real = ProductionClass()
    >>> mock = Mock()
    >>> real.closer(mock)
    >>> mock.close.assert_called_with()

Chúng ta không cần thực hiện thêm thao tác nào để cung cấp phương thức 'close' trên mock. Việc truy cập close sẽ tạo phương thức đó. Vì vậy, nếu 'close' chưa được gọi thì việc truy cập nó trong bài kiểm thử sẽ tạo ra phương thức này, nhưng :meth:`~Mock.assert_called_with` sẽ phát sinh một ngoại lệ báo lỗi.


Mock các lớp
~~~~~~~~~~~~

Một trường hợp sử dụng phổ biến là mock các lớp được khởi tạo bởi code đang được kiểm thử. Khi bạn patch một lớp, lớp đó sẽ được thay thế bằng một mock. Các instance được tạo bằng cách *gọi lớp*. Điều này có nghĩa là bạn truy cập "mock instance" bằng cách xem giá trị trả về của lớp đã được mock.

Trong ví dụ dưới đây, chúng ta có một hàm ``some_function`` khởi tạo ``Foo`` và gọi một phương thức trên đó. Lệnh gọi :func:`patch` thay thế lớp ``Foo`` bằng một mock. Instance ``Foo`` là kết quả của việc gọi mock, vì vậy instance này được cấu hình bằng cách sửa đổi mock :attr:`~Mock.return_value`.::

    >>> def some_function():
    ...     instance = module.Foo()
    ...     return instance.method()
    ...
    >>> with patch('module.Foo') as mock:
    ...     instance = mock.return_value
    ...     instance.method.return_value = 'the result'
    ...     result = some_function()
    ...     assert result == 'the result'


Đặt tên cho mock
~~~~~~~~~~~~~~~~

Việc đặt tên cho các mock có thể rất hữu ích. Tên này được hiển thị trong repr của mock và có thể giúp ích khi mock xuất hiện trong các thông báo kiểm thử thất bại. Tên này cũng được truyền cho các thuộc tính hoặc phương thức của mock:

    >>> mock = MagicMock(name='foo')
    >>> mock
    <MagicMock name='foo' id='...'>
    >>> mock.method
    <MagicMock name='foo.method' id='...'>


Theo dõi tất cả các lời gọi
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Thông thường, bạn muốn theo dõi nhiều hơn một lời gọi đến một phương thức. Đối tượng
:attr:`~Mock.mock_calls` ghi lại tất cả các lời gọi đến các thuộc tính con của mock, cũng như đến các thuộc tính con của chúng.

    >>> mock = MagicMock()
    >>> mock.method()
    <MagicMock name='mock.method()' id='...'>
    >>> mock.attribute.method(10, x=53)
    <MagicMock name='mock.attribute.method()' id='...'>
    >>> mock.mock_calls
    [call.method(), call.attribute.method(10, x=53)]

Nếu bạn thực hiện một assertion về ``mock_calls`` và bất kỳ phương thức không mong đợi nào đã được gọi, assertion sẽ thất bại. Điều này hữu ích vì ngoài việc xác nhận rằng các lời gọi bạn mong đợi đã được thực hiện, bạn còn kiểm tra rằng chúng được thực hiện đúng thứ tự và không có lời gọi bổ sung nào:

Bạn sử dụng đối tượng :data:`call` để tạo các danh sách dùng cho việc so sánh với ``mock_calls``:

    >>> expected = [call.method(), call.attribute.method(10, x=53)]
    >>> mock.mock_calls == expected
    True

Tuy nhiên, các tham số của những lời gọi trả về mock không được ghi lại, điều này có nghĩa là không thể theo dõi các lời gọi lồng nhau khi các tham số được dùng để tạo các đối tượng tổ tiên là quan trọng:

    >>> m = Mock()
    >>> m.factory(important=True).deliver()
    <Mock name='mock.factory().deliver()' id='...'>
    >>> m.mock_calls[-1] == call.factory(important=False).deliver()
    True


Thiết lập giá trị trả về và thuộc tính
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Việc thiết lập các giá trị trả về trên một đối tượng mock cực kỳ đơn giản:

    >>> mock = Mock()
    >>> mock.return_value = 3
    >>> mock()
    3

Tất nhiên, bạn cũng có thể làm tương tự với các phương thức trên mock:

    >>> mock = Mock()
    >>> mock.method.return_value = 3
    >>> mock.method()
    3

Giá trị trả về cũng có thể được thiết lập trong constructor:

    >>> mock = Mock(return_value=3)
    >>> mock()
    3

Nếu cần thiết lập một thuộc tính trên mock, chỉ cần thực hiện như sau:

    >>> mock = Mock()
    >>> mock.x = 3
    >>> mock.x
    3

Đôi khi bạn muốn mô phỏng một tình huống phức tạp hơn, chẳng hạn như ``mock.connection.cursor().execute("SELECT 1")``. Nếu muốn lệnh gọi này trả về một danh sách, chúng ta phải cấu hình kết quả của lệnh gọi lồng nhau.

Chúng ta có thể sử dụng :data:`call` để xây dựng tập hợp các lệnh gọi trong một "lệnh gọi chuỗi" như sau, giúp dễ dàng assertion sau đó:

    >>> mock = Mock()
    >>> cursor = mock.connection.cursor.return_value
    >>> cursor.execute.return_value = ['foo']
    >>> mock.connection.cursor().execute("SELECT 1")
    ['foo']
    >>> expected = call.connection.cursor().execute("SELECT 1").call_list()
    >>> mock.mock_calls
    [call.connection.cursor(), call.connection.cursor().execute('SELECT 1')]
    >>> mock.mock_calls == expected
    True

Chính lệnh gọi đến ``.call_list()`` sẽ chuyển đối tượng call của chúng ta thành một danh sách các lệnh gọi biểu diễn các lệnh gọi được chain.


Tạo exception bằng mock
~~~~~~~~~~~~~~~~~~~~~~~

Một thuộc tính hữu ích là :attr:`~Mock.side_effect`. Nếu đặt thuộc tính này thành một exception class hoặc instance, exception sẽ được raise khi mock được gọi.

    >>> mock = Mock(side_effect=Exception('Boom!'))
    >>> mock()
    Traceback (most recent call last):
      ...
    Exception: Boom!


Các hàm và iterable side effect
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``side_effect`` cũng có thể được đặt thành một hàm hoặc iterable. Trường hợp sử dụng ``side_effect`` dưới dạng iterable là khi mock của bạn sẽ được gọi nhiều lần và bạn muốn mỗi lần gọi trả về một giá trị khác nhau. Khi đặt ``side_effect`` thành một iterable, mỗi lần gọi mock sẽ trả về giá trị tiếp theo từ iterable:

    >>> mock = MagicMock(side_effect=[4, 5, 6])
    >>> mock()
    4
    >>> mock()
    5
    >>> mock()
    6


Đối với các trường hợp sử dụng nâng cao hơn, chẳng hạn như thay đổi động các giá trị trả về tùy thuộc vào đối số được truyền khi gọi mock, ``side_effect`` có thể là một hàm. Hàm này sẽ được gọi với cùng các đối số như mock. Hàm trả về giá trị nào thì lệnh gọi sẽ trả về giá trị đó:

    >>> vals = {(1, 2): 1, (2, 3): 2}
    >>> def side_effect(*args):
    ...     return vals[args]
    ...
    >>> mock = MagicMock(side_effect=side_effect)
    >>> mock(1, 2)
    1
    >>> mock(2, 3)
    2


Mock asynchronous iterator
~~~~~~~~~~~~~~~~~~~~~~~~~~

Kể từ Python 3.8, ``AsyncMock`` và ``MagicMock`` đã hỗ trợ mô phỏng
:ref:`async-iterators` đến ``__aiter__``. Thuộc tính :attr:`~Mock.return_value` của ``__aiter__`` có thể được dùng để thiết lập các giá trị trả về dùng cho việc lặp.

    >>> mock = MagicMock()  # AsyncMock cũng hoạt động trong trường hợp này
    >>> mock.__aiter__.return_value = [1, 2, 3]
    >>> async def main():
    ...     return [i async for i in mock]
    ...
    >>> asyncio.run(main())
    [1, 2, 3]


Mô phỏng asynchronous context manager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Kể từ Python 3.8, ``AsyncMock`` và ``MagicMock`` đã hỗ trợ mô phỏng
:ref:`async-context-managers` đến ``__aenter__`` và ``__aexit__``. Theo mặc định, ``__aenter__`` và ``__aexit__`` là các instance ``AsyncMock`` trả về một hàm bất đồng bộ.

    >>> class AsyncContextManager:
    ...     async def __aenter__(self):
    ...         return self
    ...     async def __aexit__(self, exc_type, exc, tb):
    ...         pass
    ...
    >>> mock_instance = MagicMock(AsyncContextManager())  # AsyncMock cũng hoạt động trong trường hợp này
    >>> async def main():
    ...     async with mock_instance as result:
    ...         pass
    ...
    >>> asyncio.run(main())
    >>> mock_instance.__aenter__.assert_awaited_once()
    >>> mock_instance.__aexit__.assert_awaited_once()


Tạo một mock từ một đối tượng hiện có
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Một vấn đề với việc lạm dụng mocking là nó khiến các bài kiểm thử của bạn phụ thuộc vào cách triển khai của các mock thay vì mã thực tế. Giả sử bạn có một class triển khai ``some_method``. Trong bài kiểm thử cho một class khác, bạn cung cấp một mock của đối tượng này mà *cũng* cung cấp ``some_method``. Nếu sau này bạn tái cấu trúc class đầu tiên để nó không còn ``some_method`` nữa thì các bài kiểm thử của bạn vẫn tiếp tục đạt, mặc dù mã của bạn hiện đã bị hỏng!

:class:`Mock` cho phép bạn cung cấp một đối tượng làm đặc tả cho mock bằng cách sử dụng đối số từ khóa *spec*. Việc truy cập các method / thuộc tính trên mock không tồn tại trên đối tượng đặc tả sẽ ngay lập tức gây ra lỗi thuộc tính. Nếu bạn thay đổi cách triển khai của đối tượng đặc tả, các bài kiểm thử sử dụng class đó sẽ bắt đầu thất bại ngay lập tức mà bạn không cần phải khởi tạo class trong các bài kiểm thử đó.

    >>> mock = Mock(spec=SomeClass)
    >>> mock.old_method()
    Traceback (most recent call last):
       ...
    AttributeError: Mock object has no attribute 'old_method'. Did you mean: 'class_method'?

Việc sử dụng đặc tả cũng cho phép đối sánh thông minh hơn các lời gọi được thực hiện đến mock, bất kể một số tham số được truyền dưới dạng đối số vị trí hay đối số có tên.::

   >>> def f(a, b, c): pass
   ...
   >>> mock = Mock(spec=f)
   >>> mock(1, 2, 3)
   <Mock name='mock()' id='140161580456576'>
   >>> mock.assert_called_with(a=1, b=2, c=3)

Nếu muốn việc đối sánh thông minh hơn này cũng hoạt động với các lời gọi method trên mock, bạn có thể sử dụng :ref:`auto-speccing <auto-speccing>`.

Nếu muốn một dạng đặc tả chặt chẽ hơn, ngăn việc thiết lập các thuộc tính tùy ý cũng như việc lấy chúng, bạn có thể sử dụng *spec_set* thay cho *spec*.


Sử dụng side_effect để trả về nội dung theo từng tệp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:func:`mock_open` được dùng để patch phương thức :func:`open`. :attr:`~Mock.side_effect` có thể được dùng để trả về một đối tượng Mock mới cho mỗi lần gọi. Cách này có thể được dùng để trả về nội dung khác nhau cho từng tệp được lưu trong một dictionary::

   DEFAULT = "default"
   data_dict = {"file1": "data1",
                "file2": "data2"}

   def open_side_effect(name):
       return mock_open(read_data=data_dict.get(name, DEFAULT))()

   with patch("builtins.open", side_effect=open_side_effect):
       with open("file1") as file1:
           assert file1.read() == "data1"

       with open("file2") as file2:
           assert file2.read() == "data2"

       with open("file3") as file2:
           assert file2.read() == "default"


Các decorator patch
-------------------

.. note::

   Với :func:`patch`, điều quan trọng là bạn phải patch các đối tượng trong namespace nơi chúng được tra cứu. Điều này thường khá đơn giản, nhưng để xem hướng dẫn nhanh, hãy đọc :ref:`where to patch <where-to-patch>`.


Một nhu cầu phổ biến trong các bài kiểm thử là patch thuộc tính của class hoặc thuộc tính của module, chẳng hạn như patch một builtin hoặc patch một class trong module để kiểm tra xem nó có được khởi tạo hay không. Các module và class về cơ bản là global, vì vậy việc patch chúng phải được hoàn tác sau bài kiểm thử; nếu không, patch sẽ tiếp tục tồn tại trong các bài kiểm thử khác và gây ra những vấn đề khó chẩn đoán.

mock cung cấp ba decorator tiện lợi cho việc này: :func:`patch`, :func:`patch.object` và
:func:`patch.dict`. ``patch`` nhận một chuỗi duy nhất, có dạng ``package.module.Class.attribute``, để chỉ định thuộc tính bạn đang patch. Nó cũng có thể nhận một giá trị mà bạn muốn thay thế thuộc tính (hoặc class hay đối tượng tương tự) bằng giá trị đó. 'patch.object' nhận một đối tượng và tên của thuộc tính bạn muốn patch, cùng với tùy chọn giá trị dùng để patch thuộc tính đó.

``patch.object``::

    >>> original = SomeClass.attribute
    >>> @patch.object(SomeClass, 'attribute', sentinel.attribute)
    ... def test():
    ...     assert SomeClass.attribute == sentinel.attribute
    ...
    >>> test()
    >>> assert SomeClass.attribute == original

    >>> @patch('package.module.attribute', sentinel.attribute)
    ... def test():
    ...     from package.module import attribute
    ...     assert attribute is sentinel.attribute
    ...
    >>> test()

Nếu bạn đang patch một module (bao gồm :mod:`builtins`) thì hãy dùng :func:`patch` thay vì :func:`patch.object`:

    >>> mock = MagicMock(return_value=sentinel.file_handle)
    >>> with patch('builtins.open', mock):
    ...     handle = open('filename', 'r')
    ...
    >>> mock.assert_called_with('filename', 'r')
    >>> assert handle == sentinel.file_handle, "incorrect file handle returned"

Tên module có thể ở dạng 'dotted', theo mẫu ``package.module`` nếu cần::

    >>> @patch('package.module.ClassName.attribute', sentinel.attribute)
    ... def test():
    ...     from package.module import ClassName
    ...     assert ClassName.attribute == sentinel.attribute
    ...
    >>> test()

Một pattern hữu ích là thực sự decorate chính các phương thức test:

    >>> class MyTest(unittest.TestCase):
    ...     @patch.object(SomeClass, 'attribute', sentinel.attribute)
    ...     def test_something(self):
    ...         self.assertEqual(SomeClass.attribute, sentinel.attribute)
    ...
    >>> original = SomeClass.attribute
    >>> MyTest('test_something').test_something()
    >>> assert SomeClass.attribute == original

Nếu bạn muốn patch bằng một Mock, bạn có thể sử dụng :func:`patch` chỉ với một đối số (hoặc :func:`patch.object` với hai đối số). Mock sẽ được tạo cho bạn và truyền vào hàm / phương thức test:

    >>> class MyTest(unittest.TestCase):
    ...     @patch.object(SomeClass, 'static_method')
    ...     def test_something(self, mock_method):
    ...         SomeClass.static_method()
    ...         mock_method.assert_called_with()
    ...
    >>> MyTest('test_something').test_something()

Bạn có thể xếp chồng nhiều patch decorator bằng pattern này::

    >>> class MyTest(unittest.TestCase):
    ...     @patch('package.module.ClassName1')
    ...     @patch('package.module.ClassName2')
    ...     def test_something(self, MockClass2, MockClass1):
    ...         self.assertIs(package.module.ClassName1, MockClass1)
    ...         self.assertIs(package.module.ClassName2, MockClass2)
    ...
    >>> MyTest('test_something').test_something()

Khi lồng các patch decorator, các mock được truyền vào hàm đã decorate theo cùng thứ tự mà chúng được áp dụng (thứ tự *Python* thông thường khi áp dụng decorator). Điều này có nghĩa là theo thứ tự từ dưới lên, nên trong ví dụ trên, mock cho ``test_module.ClassName2`` được truyền vào trước tiên.

Ngoài ra còn có :func:`patch.dict` để thiết lập các giá trị trong một dictionary chỉ trong một scope và khôi phục dictionary về trạng thái ban đầu khi test kết thúc:

   >>> foo = {'key': 'value'}
   >>> original = foo.copy()
   >>> with patch.dict(foo, {'newkey': 'newvalue'}, clear=True):
   ...     assert foo == {'newkey': 'newvalue'}
   ...
   >>> assert foo == original

``patch``, ``patch.object`` và ``patch.dict`` đều có thể được sử dụng làm context manager.

Khi bạn sử dụng :func:`patch` để tạo mock cho mình, bạn có thể lấy tham chiếu đến mock bằng dạng "as" của câu lệnh with:

    >>> class ProductionClass:
    ...     def method(self):
    ...         pass
    ...
    >>> with patch.object(ProductionClass, 'method') as mock_method:
    ...     mock_method.return_value = None
    ...     real = ProductionClass()
    ...     real.method(1, 2, 3)
    ...
    >>> mock_method.assert_called_with(1, 2, 3)


Ngoài ``patch``, ``patch.object`` và ``patch.dict`` cũng có thể được sử dụng làm class decorator. Khi được sử dụng theo cách này, chúng tương đương với việc áp dụng decorator riêng lẻ cho mọi phương thức có tên bắt đầu bằng "test".


.. _further-examples:

Các ví dụ khác
--------------


Dưới đây là thêm một số ví dụ cho các tình huống nâng cao hơn một chút.


Mock các lời gọi liên tiếp
~~~~~~~~~~~~~~~~~~~~~~~~~~

Mock các lời gọi liên tiếp thực ra khá đơn giản với mock khi bạn hiểu thuộc tính :attr:`~Mock.return_value`. Khi một mock được gọi lần đầu tiên, hoặc bạn lấy ``return_value`` của nó trước khi nó được gọi, một :class:`Mock` mới sẽ được tạo.

Điều này có nghĩa là bạn có thể xem đối tượng được trả về từ một lời gọi đến một đối tượng được mock đã được sử dụng như thế nào bằng cách kiểm tra mock ``return_value``:

    >>> mock = Mock()
    >>> mock().foo(a=2, b=3)
    <Mock name='mock().foo()' id='...'>
    >>> mock.return_value.foo.assert_called_with(a=2, b=3)

Từ đây, việc cấu hình rồi đưa ra các assertion về những lời gọi được chain là một bước đơn giản. Tất nhiên, một lựa chọn khác là ngay từ đầu viết code theo cách dễ kiểm thử hơn...

Giả sử chúng ta có một đoạn code trông gần giống như sau:

    >>> class Something:
    ...     def __init__(self):
    ...         self.backend = BackendProvider()
    ...     def method(self):
    ...         response = self.backend.get_endpoint('foobar').create_call('spam', 'eggs').start_call()
    ...         # thêm code

Giả sử ``BackendProvider`` đã được kiểm thử kỹ, làm thế nào để kiểm thử ``method()``? Cụ thể, chúng ta muốn kiểm thử rằng phần code ``# more code`` sử dụng response object theo đúng cách.

Vì chuỗi lời gọi này được thực hiện từ một instance attribute, chúng ta có thể monkey patch attribute ``backend`` trên một instance ``Something``. Trong trường hợp cụ thể này, chúng ta chỉ quan tâm đến giá trị trả về từ lời gọi cuối cùng đến ``start_call``, nên không cần cấu hình nhiều. Giả sử object mà nó trả về có tính chất 'file-like', vì vậy chúng ta sẽ đảm bảo response object sử dụng :func:`open` tích hợp sẵn làm ``spec`` của nó.

Để thực hiện việc này, chúng ta tạo một mock instance làm mock backend và tạo một mock response object cho nó. Để đặt response làm giá trị trả về cho ``start_call`` cuối cùng đó, chúng ta có thể làm như sau::

    mock_backend.get_endpoint.return_value.create_call.return_value.start_call.return_value = mock_response

Chúng ta có thể thực hiện việc đó theo cách gọn hơn một chút bằng cách sử dụng method :meth:`~Mock.configure_mock` để trực tiếp đặt giá trị trả về cho chúng ta::

    >>> something = Something()
    >>> mock_response = Mock(spec=open)
    >>> mock_backend = Mock()
    >>> config = {'get_endpoint.return_value.create_call.return_value.start_call.return_value': mock_response}
    >>> mock_backend.configure_mock(**config)

Với các đối tượng này, chúng ta monkey patch "mock backend" tại chỗ và có thể thực hiện lời gọi thực::

    >>> something.backend = mock_backend
    >>> something.method()

Bằng cách sử dụng :attr:`~Mock.mock_calls`, chúng ta có thể kiểm tra lời gọi liên kết bằng một assert duy nhất. Một lời gọi liên kết là nhiều lời gọi trong cùng một dòng mã, vì vậy sẽ có nhiều mục trong ``mock_calls``. Chúng ta có thể sử dụng :meth:`call.call_list` để tự tạo danh sách các lời gọi này::

    >>> chained = call.get_endpoint('foobar').create_call('spam', 'eggs').start_call()
    >>> call_list = chained.call_list()
    >>> assert mock_backend.mock_calls == call_list


Mock một phần
~~~~~~~~~~~~~

Đối với một số bài kiểm thử, bạn có thể muốn mock một lời gọi đến :meth:`datetime.date.today` để trả về một ngày đã biết, nhưng không muốn ngăn mã đang được kiểm thử tạo các đối tượng ngày mới. Đáng tiếc là :class:`datetime.date` được viết bằng C, vì vậy bạn không thể פשוט monkey patch phương thức tĩnh :meth:`datetime.date.today`.

Thay vào đó, bạn có thể thực chất bọc lớp date bằng một mock, đồng thời chuyển tiếp các lời gọi đến hàm khởi tạo cho lớp thực (và trả về các instance thực).

:func:`patch decorator <patch>` được dùng ở đây để mock lớp ``date`` trong mô-đun đang được kiểm thử. Sau đó, thuộc tính :attr:`~Mock.side_effect` trên lớp date mock được gán cho một hàm lambda trả về một date thực. Khi lớp date mock được gọi, một date thực sẽ được tạo và được ``side_effect`` trả về.::

    >>> import datetime as dt
    >>> with patch('mymodule.date') as mock_date:
    ...     mock_date.today.return_value = dt.date(2010, 10, 8)
    ...     mock_date.side_effect = lambda *args, **kw: dt.date(*args, **kw)
    ...
    ...     assert mymodule.date.today() == dt.date(2010, 10, 8)
    ...     assert mymodule.date(2009, 6, 8) == dt.date(2009, 6, 8)

Lưu ý rằng chúng ta không patch :class:`datetime.date` trên toàn cục, mà patch ``date`` trong mô-đun mà *sử dụng* nó. Xem :ref:`nơi cần patch <where-to-patch>`.

Khi ``date.today()`` được gọi, một ngày xác định sẽ được trả về, nhưng các lệnh gọi đến constructor ``date(...)`` vẫn trả về các ngày bình thường. Nếu không có điều này, bạn có thể phải tính toán kết quả mong đợi bằng chính xác cùng một thuật toán với mã đang được kiểm thử, đây là một anti-pattern kinh điển trong testing.

Các lệnh gọi đến date constructor được ghi lại trong các thuộc tính ``mock_date`` (``call_count`` và các thuộc tính tương tự), những thuộc tính này cũng có thể hữu ích cho các bài kiểm thử của bạn.

Một cách khác để xử lý việc mocking ngày tháng hoặc các lớp builtin khác được thảo luận trong `bài viết blog này <https://williambert.online/2011/07/how-to-unit-testing-in-django-with-mocking-and-patching/>`_.


Mocking một phương thức generator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Python generator là một hàm hoặc phương thức sử dụng câu lệnh :keyword:`yield` để trả về một chuỗi giá trị khi được lặp qua [#]_.

Một phương thức / hàm generator được gọi để trả về đối tượng generator. Sau đó, chính đối tượng generator này được lặp qua. Phương thức giao thức dùng cho việc lặp là :meth:`~container.__iter__`, vì vậy chúng ta có thể mock phương thức này bằng một :class:`MagicMock`.

Dưới đây là một ví dụ về lớp có phương thức "iter" được triển khai dưới dạng generator:

    >>> class Foo:
    ...     def iter(self):
    ...         for i in [1, 2, 3]:
    ...             yield i
    ...
    >>> foo = Foo()
    >>> list(foo.iter())
    [1, 2, 3]


Làm thế nào để mock class này, đặc biệt là phương thức "iter" của nó?

Để cấu hình các giá trị được trả về từ quá trình lặp (được ngầm định trong lệnh gọi
:class:`list`), chúng ta cần cấu hình đối tượng được trả về bởi lệnh gọi đến ``foo.iter()``.

    >>> mock_foo = MagicMock()
    >>> mock_foo.iter.return_value = iter([1, 2, 3])
    >>> list(mock_foo.iter())
    [1, 2, 3]

.. [#] Ngoài ra còn có generator expression và các `cách sử dụng nâng cao <http://www.dabeaz.com/coroutines/index.html>`_ khác của generator, nhưng ở đây chúng ta không quan tâm đến chúng. Một tài liệu giới thiệu rất hay về generator và sức mạnh của chúng là: `Generator Tricks for Systems Programmers <http://www.dabeaz.com/generators/>`_.


Áp dụng cùng một patch cho mọi phương thức kiểm thử
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Nếu muốn áp dụng nhiều patch cho nhiều phương thức kiểm thử, cách rõ ràng nhất là áp dụng các patch decorator cho từng phương thức. Điều này có thể khiến mã bị lặp lại không cần thiết. Thay vào đó, bạn có thể sử dụng :func:`patch` (dưới mọi dạng của nó) làm class decorator. Cách này áp dụng các patch cho mọi phương thức kiểm thử trong class. Một phương thức kiểm thử được xác định là phương thức có tên bắt đầu bằng ``test``::

    >>> @patch('mymodule.SomeClass')
    ... class MyTest(unittest.TestCase):
    ...
    ...     def test_one(self, MockSomeClass):
    ...         self.assertIs(mymodule.SomeClass, MockSomeClass)
    ...
    ...     def test_two(self, MockSomeClass):
    ...         self.assertIs(mymodule.SomeClass, MockSomeClass)
    ...
    ...     def not_a_test(self):
    ...         return 'something'
    ...
    >>> MyTest('test_one').test_one()
    >>> MyTest('test_two').test_two()
    >>> MyTest('test_two').not_a_test()
    'something'

Một cách khác để quản lý các patch là sử dụng :ref:`start-and-stop`.
Những điều này cho phép bạn chuyển việc patching vào các phương thức ``setUp`` và ``tearDown``.
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

    >>> class MyTest(unittest.TestCase):
    ...     def setUp(self):
    ...         self.patcher = patch('mymodule.foo')
    ...         self.mock_foo = self.patcher.start()
    ...
    ...     def test_foo(self):
    ...         self.assertIs(mymodule.foo, self.mock_foo)
    ...
    ...     def tearDown(self):
    ...         self.patcher.stop()
    ...
    >>> MyTest('test_foo').run()

Nếu sử dụng kỹ thuật này, bạn phải đảm bảo việc patching được "hoàn tác" bằng cách gọi ``stop``. Điều này có thể phức tạp hơn bạn nghĩ, vì nếu một exception được raise trong setUp thì tearDown sẽ không được gọi.
:meth:`unittest.TestCase.addCleanup` giúp việc này dễ dàng hơn::

    >>> class MyTest(unittest.TestCase):
    ...     def setUp(self):
    ...         patcher = patch('mymodule.foo')
    ...         self.addCleanup(patcher.stop)
    ...         self.mock_foo = patcher.start()
    ...
    ...     def test_foo(self):
    ...         self.assertIs(mymodule.foo, self.mock_foo)
    ...
    >>> MyTest('test_foo').run()


Mocking các unbound method
~~~~~~~~~~~~~~~~~~~~~~~~~~

Đôi khi một test cần patch một *unbound method*, tức là patch method trên class thay vì trên instance. Để có thể assertion về những object nào đang gọi method cụ thể này, bạn cần truyền ``self`` làm đối số đầu tiên. Vấn đề là bạn không thể dùng mock để patch việc này, vì nếu thay thế một unbound method bằng mock thì nó sẽ không trở thành bound method khi được lấy từ instance, và do đó không được truyền ``self`` vào. Cách giải quyết là patch unbound method bằng một function thực sự. Decorator :func:`patch` giúp việc patch method bằng mock trở nên đơn giản đến mức việc phải tạo một function thực sự trở thành điều phiền toái.

Nếu truyền ``autospec=True`` cho patch thì việc patching sẽ được thực hiện bằng một *real* function object. Function object này có cùng signature với function mà nó thay thế, nhưng bên dưới sẽ chuyển tiếp đến một mock. Bạn vẫn nhận được mock được tự động tạo theo đúng cách như trước. Tuy nhiên, điều đó có nghĩa là nếu dùng nó để patch một unbound method trên class, mocked function sẽ được chuyển thành bound method nếu được lấy từ một instance. Nó sẽ được truyền ``self`` làm đối số đầu tiên, đúng như yêu cầu:

    >>> class Foo:
    ...   def foo(self):
    ...     pass
    ...
    >>> with patch.object(Foo, 'foo', autospec=True) as mock_foo:
    ...   mock_foo.return_value = 'foo'
    ...   foo = Foo()
    ...   foo.foo()
    ...
    'foo'
    >>> mock_foo.assert_called_once_with(foo)

Nếu không dùng ``autospec=True`` thì unbound method sẽ được patch bằng một Mock instance thay thế, và không được gọi với ``self``.


Kiểm tra nhiều lần gọi bằng mock
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

mock có một API tiện lợi để đưa ra các assertion về cách các mock object của bạn được sử dụng.

    >>> mock = Mock()
    >>> mock.foo_bar.return_value = None
    >>> mock.foo_bar('baz', spam='eggs')
    >>> mock.foo_bar.assert_called_with('baz', spam='eggs')

Nếu mock của bạn chỉ được gọi một lần, bạn có thể sử dụng
phương thức :meth:`~Mock.assert_called_once_with`, phương thức này cũng kiểm tra rằng
:attr:`~Mock.call_count` là một.

    >>> mock.foo_bar.assert_called_once_with('baz', spam='eggs')
    >>> mock.foo_bar()
    >>> mock.foo_bar.assert_called_once_with('baz', spam='eggs')
    Traceback (most recent call last):
        ...
    AssertionError: Expected 'foo_bar' to be called once. Called 2 times.
    Calls: [call('baz', spam='eggs'), call()].

Cả ``assert_called_with`` và ``assert_called_once_with`` đều đưa ra assertion về lần gọi *gần đây nhất*. Nếu mock của bạn sẽ được gọi nhiều lần và bạn muốn đưa ra assertion về *tất cả* những lần gọi đó, bạn có thể sử dụng
:attr:`~Mock.call_args_list`:

    >>> mock = Mock(return_value=None)
    >>> mock(1, 2, 3)
    >>> mock(4, 5, 6)
    >>> mock()
    >>> mock.call_args_list
    [call(1, 2, 3), call(4, 5, 6), call()]

Helper :data:`call` giúp bạn dễ dàng đưa ra assertion về những lần gọi này. Bạn có thể tạo một danh sách các lần gọi dự kiến rồi so sánh danh sách đó với ``call_args_list``. Kết quả này trông rất giống với repr của ``call_args_list``:

    >>> expected = [call(1, 2, 3), call(4, 5, 6), call()]
    >>> mock.call_args_list == expected
    True


Xử lý các đối số có thể thay đổi
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Một tình huống khác hiếm gặp nhưng có thể gây rắc rối là khi mock được gọi với các đối số có thể thay đổi. ``call_args`` và ``call_args_list`` lưu *các tham chiếu* đến các đối số. Nếu các đối số bị mã đang được kiểm thử thay đổi thì bạn không thể tiếp tục khẳng định các giá trị của chúng tại thời điểm mock được gọi.

Đây là một đoạn mã ví dụ cho thấy vấn đề. Hãy hình dung các hàm sau được định nghĩa trong 'mymodule'::

    def frob(val):
        pass

    def grob(val):
        "First frob and then clear val"
        frob(val)
        val.clear()

Khi thử kiểm tra rằng ``grob`` gọi ``frob`` với đối số chính xác, hãy xem điều gì xảy ra::

    >>> with patch('mymodule.frob') as mock_frob:
    ...     val = {6}
    ...     mymodule.grob(val)
    ...
    >>> val
    set()
    >>> mock_frob.assert_called_with({6})
    Traceback (most recent call last):
        ...
    AssertionError: Expected: (({6},), {})
    Called with: ((set(),), {})

Một khả năng là mock sẽ sao chép các đối số mà bạn truyền vào. Tuy nhiên, điều này có thể gây ra vấn đề nếu bạn thực hiện các phép khẳng định dựa vào identity của đối tượng để so sánh bằng nhau.

Đây là một giải pháp sử dụng chức năng :attr:`~Mock.side_effect`. Nếu cung cấp một hàm ``side_effect`` cho mock thì ``side_effect`` sẽ được gọi với cùng các args như mock. Điều này cho chúng ta cơ hội sao chép các đối số và lưu chúng để khẳng định sau này. Trong ví dụ này, tôi sử dụng *một* mock khác để lưu các đối số, nhờ đó có thể sử dụng các phương thức của mock để thực hiện phép khẳng định. Một lần nữa, một hàm trợ giúp sẽ thiết lập việc này cho tôi.::

    >>> from copy import deepcopy
    >>> from unittest.mock import Mock, patch, DEFAULT
    >>> def copy_call_args(mock):
    ...     new_mock = Mock()
    ...     def side_effect(*args, **kwargs):
    ...         args = deepcopy(args)
    ...         kwargs = deepcopy(kwargs)
    ...         new_mock(*args, **kwargs)
    ...         return DEFAULT
    ...     mock.side_effect = side_effect
    ...     return new_mock
    ...
    >>> with patch('mymodule.frob') as mock_frob:
    ...     new_mock = copy_call_args(mock_frob)
    ...     val = {6}
    ...     mymodule.grob(val)
    ...
    >>> new_mock.assert_called_with({6})
    >>> new_mock.call_args
    call({6})

``copy_call_args`` được gọi với mock sẽ được gọi. Nó trả về một mock mới để chúng ta thực hiện phép khẳng định. Hàm ``side_effect`` sao chép các args và gọi ``new_mock`` của chúng ta với bản sao đó.

.. note::

    Nếu mock của bạn chỉ được sử dụng một lần, có một cách dễ hơn để kiểm tra các đối số ngay tại thời điểm chúng được gọi. Bạn chỉ cần thực hiện việc kiểm tra bên trong một hàm ``side_effect``.

        >>> def side_effect(arg):
        ...     assert arg == {6}
        ...
        >>> mock = Mock(side_effect=side_effect)
        >>> mock({6})
        >>> mock(set())
        Traceback (most recent call last):
            ...
        AssertionError

Một cách tiếp cận khác là tạo một lớp con của :class:`Mock` hoặc
:class:`MagicMock` để sao chép các đối số (bằng cách sử dụng :func:`copy.deepcopy`). Dưới đây là một cách triển khai mẫu:

    >>> from copy import deepcopy
    >>> class CopyingMock(MagicMock):
    ...     def __call__(self, /, *args, **kwargs):
    ...         args = deepcopy(args)
    ...         kwargs = deepcopy(kwargs)
    ...         return super().__call__(*args, **kwargs)
    ...
    >>> c = CopyingMock(return_value=None)
    >>> arg = set()
    >>> c(arg)
    >>> arg.add(1)
    >>> c.assert_called_with(set())
    >>> c.assert_called_with(arg)
    Traceback (most recent call last):
        ...
    AssertionError: expected call not found.
    Expected: mock({1})
    Actual: mock(set())
    >>> c.foo
    <CopyingMock name='mock.foo' id='...'>

Khi bạn tạo lớp con của ``Mock`` hoặc ``MagicMock``, tất cả các thuộc tính được tạo động và ``return_value`` sẽ tự động sử dụng lớp con của bạn. Điều đó có nghĩa là tất cả các đối tượng con của một ``CopyingMock`` cũng sẽ có kiểu ``CopyingMock``.


Lồng ghép các bản vá
~~~~~~~~~~~~~~~~~~~~

Sử dụng patch như một trình quản lý ngữ cảnh rất tiện, nhưng nếu thực hiện nhiều bản vá, bạn có thể kết thúc với các câu lệnh with lồng nhau, khiến thụt lề ngày càng sâu hơn về bên phải::

    >>> class MyTest(unittest.TestCase):
    ...
    ...     def test_foo(self):
    ...         with patch('mymodule.Foo') as mock_foo:
    ...             with patch('mymodule.Bar') as mock_bar:
    ...                 with patch('mymodule.Spam') as mock_spam:
    ...                     assert mymodule.Foo is mock_foo
    ...                     assert mymodule.Bar is mock_bar
    ...                     assert mymodule.Spam is mock_spam
    ...
    >>> original = mymodule.Foo
    >>> MyTest('test_foo').test_foo()
    >>> assert mymodule.Foo is original

Với các hàm unittest ``cleanup`` và :ref:`start-and-stop`, chúng ta có thể đạt được hiệu ứng tương tự mà không cần thụt lề lồng nhau. Một phương thức trợ giúp đơn giản, ``create_patch``, sẽ áp dụng patch và trả về mock đã được tạo cho chúng ta::

    >>> class MyTest(unittest.TestCase):
    ...
    ...     def create_patch(self, name):
    ...         patcher = patch(name)
    ...         thing = patcher.start()
    ...         self.addCleanup(patcher.stop)
    ...         return thing
    ...
    ...     def test_foo(self):
    ...         mock_foo = self.create_patch('mymodule.Foo')
    ...         mock_bar = self.create_patch('mymodule.Bar')
    ...         mock_spam = self.create_patch('mymodule.Spam')
    ...
    ...         assert mymodule.Foo is mock_foo
    ...         assert mymodule.Bar is mock_bar
    ...         assert mymodule.Spam is mock_spam
    ...
    >>> original = mymodule.Foo
    >>> MyTest('test_foo').run()
    >>> assert mymodule.Foo is original


Mô phỏng một dictionary bằng MagicMock
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Bạn có thể muốn mô phỏng một dictionary hoặc đối tượng container khác, ghi lại mọi lần truy cập vào nó nhưng vẫn cho phép nó hoạt động như một dictionary.

Chúng ta có thể thực hiện việc này bằng :class:`MagicMock`, đối tượng này sẽ hoạt động như một dictionary, đồng thời sử dụng :data:`~Mock.side_effect` để ủy quyền việc truy cập dictionary cho một dictionary thực bên dưới mà chúng ta kiểm soát.

Khi các phương thức :meth:`~object.__getitem__` và :meth:`~object.__setitem__` của ``MagicMock`` được gọi (truy cập dictionary thông thường), ``side_effect`` sẽ được gọi với key (và trong trường hợp của ``__setitem__`` thì cả value). Chúng ta cũng có thể kiểm soát giá trị được trả về.

Sau khi sử dụng ``MagicMock``, chúng ta có thể dùng các thuộc tính như
:data:`~Mock.call_args_list` để kiểm tra cách dictionary đã được sử dụng:

    >>> my_dict = {'a': 1, 'b': 2, 'c': 3}
    >>> def getitem(name):
    ...      return my_dict[name]
    ...
    >>> def setitem(name, val):
    ...     my_dict[name] = val
    ...
    >>> mock = MagicMock()
    >>> mock.__getitem__.side_effect = getitem
    >>> mock.__setitem__.side_effect = setitem

.. note::

    Một lựa chọn thay cho việc sử dụng ``MagicMock`` là dùng ``Mock`` và *only* để chỉ cung cấp các magic method mà bạn muốn:

        >>> mock = Mock()
        >>> mock.__getitem__ = Mock(side_effect=getitem)
        >>> mock.__setitem__ = Mock(side_effect=setitem)

    Một *lựa chọn thứ ba* là sử dụng ``MagicMock`` nhưng truyền ``dict`` làm đối số *spec* (hoặc *spec_set*) để ``MagicMock`` được tạo ra chỉ có các magic method của dictionary:

        >>> mock = MagicMock(spec_set=dict)
        >>> mock.__getitem__.side_effect = getitem
        >>> mock.__setitem__.side_effect = setitem

Khi đã thiết lập các hàm side effect này, ``mock`` sẽ hoạt động như một dictionary thông thường nhưng đồng thời ghi lại các lần truy cập. Nó thậm chí còn ném :exc:`KeyError` nếu bạn cố truy cập một khóa không tồn tại.

    >>> mock['a']
    1
    >>> mock['c']
    3
    >>> mock['d']
    Traceback (most recent call last):
        ...
    KeyError: 'd'
    >>> mock['b'] = 'fish'
    >>> mock['d'] = 'eggs'
    >>> mock['b']
    'fish'
    >>> mock['d']
    'eggs'

Sau khi sử dụng, bạn có thể dùng các phương thức và thuộc tính mock thông thường để kiểm tra các lần truy cập:

    >>> mock.__getitem__.call_args_list
    [call('a'), call('c'), call('d'), call('b'), call('d')]
    >>> mock.__setitem__.call_args_list
    [call('b', 'fish'), call('d', 'eggs')]
    >>> my_dict
    {'a': 1, 'b': 'fish', 'c': 3, 'd': 'eggs'}


Các lớp con của Mock và thuộc tính của chúng
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Có nhiều lý do khiến bạn muốn tạo lớp con của :class:`Mock`. Một lý do có thể là để thêm các phương thức helper. Sau đây là một ví dụ hơi ngớ ngẩn:

    >>> class MyMock(MagicMock):
    ...     def has_been_called(self):
    ...         return self.called
    ...
    >>> mymock = MyMock(return_value=None)
    >>> mymock
    <MyMock id='...'>
    >>> mymock.has_been_called()
    False
    >>> mymock()
    >>> mymock.has_been_called()
    True

Hành vi mặc định của các instance ``Mock`` là các thuộc tính và mock giá trị trả về có cùng kiểu với mock mà chúng được truy cập trên đó. Điều này đảm bảo rằng các thuộc tính ``Mock`` là ``Mocks`` và các thuộc tính ``MagicMock`` là ``MagicMocks`` [#]_. Vì vậy, nếu bạn tạo lớp con để thêm các phương thức helper, chúng cũng sẽ có sẵn trên các thuộc tính và mock giá trị trả về của các instance thuộc lớp con đó.

    >>> mymock.foo
    <MyMock name='mock.foo' id='...'>
    >>> mymock.foo.has_been_called()
    False
    >>> mymock.foo()
    <MyMock name='mock.foo()' id='...'>
    >>> mymock.foo.has_been_called()
    True

Đôi khi điều này gây bất tiện. Ví dụ, `một người dùng <https://code.google.com/archive/p/mock/issues/105>`_ đang tạo lớp con của mock để tạo một `bộ chuyển đổi Twisted <https://twisted.org/documents/11.0.0/api/twisted.python.components.html>`_. Việc áp dụng điều này cho cả các thuộc tính thực sự gây ra lỗi.

``Mock`` (trong tất cả các biến thể của nó) sử dụng một phương thức có tên là ``_get_child_mock`` để tạo các "sub-mock" này cho các thuộc tính và giá trị trả về. Bạn có thể ngăn không cho subclass của mình được sử dụng cho các thuộc tính bằng cách ghi đè phương thức này. Chữ ký của phương thức nhận các đối số keyword tùy ý (``**kwargs``), sau đó chuyển chúng cho constructor của mock:

    >>> class Subclass(MagicMock):
    ...     def _get_child_mock(self, /, **kwargs):
    ...         return MagicMock(**kwargs)
    ...
    >>> mymock = Subclass()
    >>> mymock.foo
    <MagicMock name='mock.foo' id='...'>
    >>> assert isinstance(mymock, Subclass)
    >>> assert not isinstance(mymock.foo, Subclass)
    >>> assert not isinstance(mymock(), Subclass)

.. [#] Ngoại lệ của quy tắc này là các mock non-callable. Các thuộc tính sử dụng biến thể callable, vì nếu không thì mock non-callable sẽ không thể có các phương thức callable.


Mock import bằng patch.dict
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Một tình huống mà việc mocking có thể khó khăn là khi bạn có một local import bên trong một hàm. Những import này khó mock hơn vì chúng không sử dụng một đối tượng từ namespace của module mà chúng ta có thể patch.

Nhìn chung, nên tránh local import. Đôi khi chúng được dùng để ngăn circular dependency, mà để giải quyết vấn đề đó *usually* có một cách tốt hơn nhiều (refactor code), hoặc để tránh "up front costs" bằng cách trì hoãn import. Vấn đề này cũng có thể được giải quyết theo những cách tốt hơn so với một local import không điều kiện (lưu module dưới dạng thuộc tính của class hoặc module và chỉ thực hiện import khi dùng lần đầu).

Ngoài điều đó, có một cách sử dụng ``mock`` để tác động đến kết quả của một import. Việc import lấy một *object* từ dictionary :data:`sys.modules`. Lưu ý rằng nó lấy một *object*, đối tượng này không nhất thiết phải là một module. Việc import một module lần đầu tiên khiến một đối tượng module được đưa vào ``sys.modules``, vì vậy thông thường khi bạn import một thứ gì đó, bạn sẽ nhận lại một module. Tuy nhiên, điều này không bắt buộc.

Điều này có nghĩa là bạn có thể dùng :func:`patch.dict` để *temporarily* đặt một mock vào :data:`sys.modules`. Mọi import trong khi patch này đang hoạt động sẽ lấy mock đó. Khi patch hoàn tất (hàm được decorate kết thúc, phần thân của câu lệnh with hoàn tất hoặc ``patcher.stop()`` được gọi), bất kỳ thứ gì đã tồn tại trước đó sẽ được khôi phục an toàn.

Đây là một ví dụ mô phỏng module 'fooble'.

    >>> import sys
    >>> mock = Mock()
    >>> with patch.dict('sys.modules', {'fooble': mock}):
    ...    import fooble
    ...    fooble.blob()
    ...
    <Mock name='mock.blob()' id='...'>
    >>> assert 'fooble' not in sys.modules
    >>> mock.blob.assert_called_once_with()

Như bạn có thể thấy, ``import fooble`` thành công, nhưng khi thoát ra thì không còn 'fooble' trong :data:`sys.modules`.

Cách này cũng hoạt động với dạng ``from module import name``:

    >>> mock = Mock()
    >>> with patch.dict('sys.modules', {'fooble': mock}):
    ...    from fooble import blob
    ...    blob.blip()
    ...
    <Mock name='mock.blob.blip()' id='...'>
    >>> mock.blob.blip.assert_called_once_with()

Với thêm một chút công sức, bạn cũng có thể mô phỏng các lần import package:

    >>> mock = Mock()
    >>> modules = {'package': mock, 'package.module': mock.module}
    >>> with patch.dict('sys.modules', modules):
    ...    from package.module import fooble
    ...    fooble()
    ...
    <Mock name='mock.module.fooble()' id='...'>
    >>> mock.module.fooble.assert_called_once_with()


Theo dõi thứ tự các lần gọi và các assertion về lần gọi ngắn gọn hơn
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lớp :class:`Mock` cho phép bạn theo dõi *thứ tự* các lần gọi phương thức trên các mock object thông qua thuộc tính :attr:`~Mock.method_calls`. Tuy nhiên, cách này không cho phép bạn theo dõi thứ tự các lần gọi giữa những mock object riêng biệt; chúng ta có thể dùng :attr:`~Mock.mock_calls` để đạt được hiệu quả tương tự.

Vì các mock theo dõi những lần gọi đến các mock con trong ``mock_calls``, và việc truy cập một thuộc tính tùy ý của mock sẽ tạo ra một mock con, chúng ta có thể tạo các mock riêng biệt từ một mock cha. Khi đó, các lần gọi đến những mock con này sẽ được ghi lại theo đúng thứ tự trong ``mock_calls`` của mock cha:

    >>> manager = Mock()
    >>> mock_foo = manager.foo
    >>> mock_bar = manager.bar

    >>> mock_foo.something()
    <Mock name='mock.foo.something()' id='...'>
    >>> mock_bar.other.thing()
    <Mock name='mock.bar.other.thing()' id='...'>

    >>> manager.mock_calls
    [call.foo.something(), call.bar.other.thing()]

Sau đó, chúng ta có thể assert về các lệnh gọi, bao gồm cả thứ tự, bằng cách so sánh với thuộc tính ``mock_calls`` trên mock manager:

    >>> expected_calls = [call.foo.something(), call.bar.other.thing()]
    >>> manager.mock_calls == expected_calls
    True

Nếu ``patch`` tạo và thiết lập các mock cho bạn, thì bạn có thể gắn chúng vào một mock manager bằng phương thức :meth:`~Mock.attach_mock`. Sau khi được gắn, các lệnh gọi sẽ được ghi lại trong ``mock_calls`` của manager.::

    >>> manager = MagicMock()
    >>> with patch('mymodule.Class1') as MockClass1:
    ...     with patch('mymodule.Class2') as MockClass2:
    ...         manager.attach_mock(MockClass1, 'MockClass1')
    ...         manager.attach_mock(MockClass2, 'MockClass2')
    ...         MockClass1().foo()
    ...         MockClass2().bar()
    <MagicMock name='mock.MockClass1().foo()' id='...'>
    <MagicMock name='mock.MockClass2().bar()' id='...'>
    >>> manager.mock_calls
    [call.MockClass1(),
    call.MockClass1().foo(),
    call.MockClass2(),
    call.MockClass2().bar()]

Nếu đã có nhiều lệnh gọi được thực hiện nhưng bạn chỉ quan tâm đến một chuỗi cụ thể trong số đó, thì một lựa chọn khác là sử dụng
phương thức :meth:`~Mock.assert_has_calls`. Phương thức này nhận một danh sách các lệnh gọi (được tạo bằng đối tượng :data:`call`). Nếu chuỗi lệnh gọi đó nằm trong
:attr:`~Mock.mock_calls` thì assert sẽ thành công.

    >>> m = MagicMock()
    >>> m().foo().bar().baz()
    <MagicMock name='mock().foo().bar().baz()' id='...'>
    >>> m.one().two().three()
    <MagicMock name='mock.one().two().three()' id='...'>
    >>> calls = call.one().two().three().call_list()
    >>> m.assert_has_calls(calls)

Mặc dù lệnh gọi nối chuỗi ``m.one().two().three()`` không phải là những lệnh gọi duy nhất đã được thực hiện trên mock, assert vẫn thành công.

Đôi khi một mock có thể nhận nhiều lệnh gọi, và bạn chỉ muốn assert về *some* trong số các lệnh gọi đó. Bạn thậm chí có thể không quan tâm đến thứ tự. Trong trường hợp này, bạn có thể truyền ``any_order=True`` cho ``assert_has_calls``:

    >>> m = MagicMock()
    >>> m(1), m.two(2, 3), m.seven(7), m.fifty('50')
    (...)
    >>> calls = [call.fifty('50'), call(1), call.seven(7)]
    >>> m.assert_has_calls(calls, any_order=True)


Đối sánh đối số phức tạp hơn
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sử dụng cùng khái niệm cơ bản như :data:`ANY`, chúng ta có thể triển khai các matcher để thực hiện những phép kiểm tra phức tạp hơn trên các đối tượng được dùng làm đối số cho các mock.

Giả sử chúng ta mong đợi một đối tượng nào đó được truyền vào một mock, mà theo mặc định sẽ so sánh bằng dựa trên identity của đối tượng (đây là mặc định của Python đối với các lớp do người dùng định nghĩa). Để sử dụng :meth:`~Mock.assert_called_with`, chúng ta cần truyền vào chính xác cùng một đối tượng đó. Nếu chúng ta chỉ quan tâm đến một số thuộc tính của đối tượng này, chúng ta có thể tạo một matcher để kiểm tra các thuộc tính đó giúp chúng ta.

Bạn có thể thấy trong ví dụ này rằng một lời gọi 'standard' đến ``assert_called_with`` là chưa đủ:

    >>> class Foo:
    ...     def __init__(self, a, b):
    ...         self.a, self.b = a, b
    ...
    >>> mock = Mock(return_value=None)
    >>> mock(Foo(1, 2))
    >>> mock.assert_called_with(Foo(1, 2))
    Traceback (most recent call last):
        ...
    AssertionError: expected call not found.
    Expected: mock(<__main__.Foo object at 0x...>)
    Actual: mock(<__main__.Foo object at 0x...>)

Một hàm so sánh cho lớp ``Foo`` của chúng ta có thể trông như sau:

    >>> def compare(self, other):
    ...     if not type(self) == type(other):
    ...         return False
    ...     if self.a != other.a:
    ...         return False
    ...     if self.b != other.b:
    ...         return False
    ...     return True
    ...

Một đối tượng matcher có thể sử dụng các hàm so sánh như thế này cho phép toán equality của nó sẽ có dạng như sau:

    >>> class Matcher:
    ...     def __init__(self, compare, some_obj):
    ...         self.compare = compare
    ...         self.some_obj = some_obj
    ...     def __eq__(self, other):
    ...         return self.compare(self.some_obj, other)
    ...

Kết hợp tất cả lại:

    >>> match_foo = Matcher(compare, Foo(1, 2))
    >>> mock.assert_called_with(match_foo)

``Matcher`` được khởi tạo với hàm so sánh của chúng ta và đối tượng ``Foo`` mà chúng ta muốn so sánh. Trong ``assert_called_with``, phương thức kiểm tra tính bằng nhau ``Matcher`` sẽ được gọi; phương thức này so sánh đối tượng mà mock được gọi cùng với đối tượng mà chúng ta đã dùng để tạo matcher. Nếu chúng khớp nhau thì ``assert_called_with`` thành công, còn nếu không thì một :exc:`AssertionError` sẽ được phát sinh:

    >>> match_wrong = Matcher(compare, Foo(3, 4))
    >>> mock.assert_called_with(match_wrong)
    Traceback (most recent call last):
        ...
    AssertionError: Expected: ((<Matcher object at 0x...>,), {})
    Called with: ((<Foo object at 0x...>,), {})

Chỉ cần tinh chỉnh một chút, bạn có thể khiến hàm so sánh phát sinh
:exc:`AssertionError` trực tiếp và cung cấp thông báo lỗi hữu ích hơn.

Kể từ phiên bản 1.5, thư viện kiểm thử Python `PyHamcrest <https://pyhamcrest.readthedocs.io/>`_ cung cấp chức năng tương tự, có thể hữu ích trong trường hợp này, dưới dạng equality matcher (`hamcrest.library.integration.match_equality <https://pyhamcrest.readthedocs.io/en/release-1.8/integration/#module-hamcrest.library.integration.match_equality>`_).

.. _`this blog entry`: https://williambert.online/2011/07/how-to-unit-testing-in-django-with-mocking-and-patching/
.. _`advanced uses`: http://www.dabeaz.com/coroutines/index.html
.. _`Generator Tricks for Systems Programmers`: http://www.dabeaz.com/generators/
.. _`one user`: https://code.google.com/archive/p/mock/issues/105
.. _`Twisted adaptor`: https://twisted.org/documents/11.0.0/api/twisted.python.components.html
.. _`PyHamcrest`: https://pyhamcrest.readthedocs.io/
.. _`hamcrest.library.integration.match_equality`: https://pyhamcrest.readthedocs.io/en/release-1.8/integration/#module-hamcrest.library.integration.match_equality
