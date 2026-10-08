:mod:`!unittest.mock` --- thư viện đối tượng mock
=================================================

.. module:: unittest.mock
   :synopsis: Thư viện đối tượng mock.

.. moduleauthor:: Michael Foord <michael@python.org>
.. currentmodule:: unittest.mock

.. versionadded:: 3.3

**Mã nguồn:** :source:`Lib/unittest/mock.py`

--------------

:mod:`!unittest.mock` là một thư viện dùng để kiểm thử trong Python. Thư viện này cho phép bạn thay thế các phần của hệ thống đang được kiểm thử bằng các đối tượng mock và đưa ra các assertion về cách chúng đã được sử dụng.

:mod:`!unittest.mock` cung cấp một lớp :class:`Mock` cốt lõi, loại bỏ nhu cầu tạo hàng loạt stub trong toàn bộ bộ kiểm thử của bạn. Sau khi thực hiện một hành động, bạn có thể đưa ra các assertion về những phương thức / thuộc tính nào đã được sử dụng và các đối số mà chúng được gọi với. Bạn cũng có thể chỉ định các giá trị trả về và thiết lập các thuộc tính cần thiết theo cách thông thường.

Ngoài ra, mock cung cấp một decorator :func:`patch` xử lý việc patch các thuộc tính ở cấp mô-đun và cấp lớp trong phạm vi của một bài kiểm thử, cùng với
:const:`sentinel` để tạo các đối tượng duy nhất. Xem `hướng dẫn nhanh <quick guide_>`_ để biết một số ví dụ về cách sử dụng :class:`Mock`, :class:`MagicMock` và
:func:`patch`.

Mock được thiết kế để sử dụng với :mod:`unittest` và dựa trên mẫu 'action -> assertion' thay vì mẫu 'record -> replay' được nhiều mocking framework sử dụng.

Có một bản backport của :mod:`!unittest.mock` dành cho các phiên bản Python cũ hơn, có sẵn trên PyPI dưới dạng :pypi:`mock`.


.. _`Quick Guide`:

Hướng dẫn nhanh
---------------

.. testsetup::

    class ProductionClass:
        def method(self, a, b, c):
            pass

    class SomeClass:
        @staticmethod
        def static_method(args):
            return args

        @classmethod
        def class_method(cls, args):
            return args


Các đối tượng :class:`Mock` và :class:`MagicMock` tạo tất cả thuộc tính và phương thức khi bạn truy cập chúng, đồng thời lưu lại chi tiết về cách chúng đã được sử dụng. Bạn có thể cấu hình chúng để chỉ định giá trị trả về hoặc giới hạn các thuộc tính khả dụng, sau đó đưa ra các assertion về cách chúng đã được sử dụng:

    >>> from unittest.mock import MagicMock
    >>> thing = ProductionClass()
    >>> thing.method = MagicMock(return_value=3)
    >>> thing.method(3, 4, 5, key='value')
    3
    >>> thing.method.assert_called_with(3, 4, 5, key='value')

:attr:`~Mock.side_effect` cho phép bạn thực hiện các side effect, bao gồm cả việc phát sinh exception khi mock được gọi:

   >>> from unittest.mock import Mock
   >>> mock = Mock(side_effect=KeyError('foo'))
   >>> mock()
   Traceback (most recent call last):
    ...
   KeyError: 'foo'

   >>> values = {'a': 1, 'b': 2, 'c': 3}
   >>> def side_effect(arg):
   ...     return values[arg]
   ...
   >>> mock.side_effect = side_effect
   >>> mock('a'), mock('b'), mock('c')
   (1, 2, 3)
   >>> mock.side_effect = [5, 4, 3, 2, 1]
   >>> mock(), mock(), mock()
   (5, 4, 3)

Mock có nhiều cách khác để bạn cấu hình và kiểm soát hành vi của nó. Ví dụ, đối số *spec* cấu hình mock để lấy specification từ một đối tượng khác. Việc cố gắng truy cập các thuộc tính hoặc phương thức không tồn tại trong spec trên mock sẽ thất bại với một :exc:`AttributeError`.

Decorator / context manager :func:`patch` giúp bạn dễ dàng mock các class hoặc object trong module đang được kiểm thử. Đối tượng bạn chỉ định sẽ được thay thế bằng một mock (hoặc object khác) trong suốt quá trình kiểm thử và được khôi phục khi kiểm thử kết thúc::

    >>> from unittest.mock import patch
    >>> @patch('module.ClassName2')
    ... @patch('module.ClassName1')
    ... def test(MockClass1, MockClass2):
    ...     module.ClassName1()
    ...     module.ClassName2()
    ...     assert MockClass1 is module.ClassName1
    ...     assert MockClass2 is module.ClassName2
    ...     assert MockClass1.called
    ...     assert MockClass2.called
    ...
    >>> test()

.. note::

   Khi lồng các decorator patch, các mock được truyền vào hàm đã được trang trí theo đúng thứ tự mà chúng được áp dụng (theo thứ tự *Python* thông thường khi áp dụng decorator). Điều này có nghĩa là theo thứ tự từ dưới lên, vì vậy trong ví dụ trên, mock cho ``module.ClassName1`` được truyền vào trước tiên.

   Với :func:`patch`, điều quan trọng là bạn phải patch các đối tượng trong namespace nơi chúng được tra cứu. Điều này thường khá đơn giản, nhưng để xem hướng dẫn nhanh, hãy đọc :ref:`where to patch <where-to-patch>`.

Ngoài việc được dùng như một decorator, :func:`patch` còn có thể được dùng như một context manager trong câu lệnh with:

    >>> with patch.object(ProductionClass, 'method', return_value=None) as mock_method:
    ...     thing = ProductionClass()
    ...     thing.method(1, 2, 3)
    ...
    >>> mock_method.assert_called_once_with(1, 2, 3)


Ngoài ra còn có :func:`patch.dict` để thiết lập các giá trị trong một dictionary chỉ trong một phạm vi và khôi phục dictionary về trạng thái ban đầu khi test kết thúc:

   >>> foo = {'key': 'value'}
   >>> original = foo.copy()
   >>> with patch.dict(foo, {'newkey': 'newvalue'}, clear=True):
   ...     assert foo == {'newkey': 'newvalue'}
   ...
   >>> assert foo == original

Mock hỗ trợ việc mock các :ref:`magic methods <magic-methods>` của Python. Cách dễ nhất để sử dụng magic methods là dùng class :class:`MagicMock`. Class này cho phép bạn thực hiện những việc như sau:

    >>> mock = MagicMock()
    >>> mock.__str__.return_value = 'foobarbaz'
    >>> str(mock)
    'foobarbaz'
    >>> mock.__str__.assert_called_with()

Mock cho phép bạn gán các hàm (hoặc các instance Mock khác) cho magic methods và chúng sẽ được gọi một cách thích hợp. Class :class:`MagicMock` chỉ là một biến thể của Mock, trong đó tất cả magic methods đã được tạo sẵn cho bạn (ít nhất là tất cả những phương thức hữu ích).

Sau đây là một ví dụ về cách sử dụng magic methods với class Mock thông thường:

    >>> mock = Mock()
    >>> mock.__str__ = Mock(return_value='wheeeeee')
    >>> str(mock)
    'wheeeeee'

Để đảm bảo các mock object trong những bài kiểm thử của bạn có cùng API với các object mà chúng thay thế, bạn có thể sử dụng :ref:`auto-speccing <auto-speccing>`. Có thể thực hiện auto-speccing thông qua đối số *autospec* của patch, hoặc
:func:`create_autospec` function. Auto-speccing tạo ra các mock object có cùng thuộc tính và phương thức với các object mà chúng thay thế, đồng thời mọi function và method (bao gồm cả constructor) đều có cùng chữ ký lời gọi như object thực.

Điều này đảm bảo rằng các mock của bạn sẽ thất bại theo cùng cách với code production nếu được sử dụng không đúng cách:

   >>> from unittest.mock import create_autospec
   >>> def function(a, b, c):
   ...     pass
   ...
   >>> mock_function = create_autospec(function, return_value='fishy')
   >>> mock_function(1, 2, 3)
   'fishy'
   >>> mock_function.assert_called_once_with(1, 2, 3)
   >>> mock_function('wrong arguments')
   Traceback (most recent call last):
    ...
   TypeError: missing a required argument: 'b'

:func:`create_autospec` cũng có thể được sử dụng trên các class, trong đó nó sao chép chữ ký của phương thức ``__init__``, và trên các callable object, trong đó nó sao chép chữ ký của phương thức ``__call__``.



Lớp Mock
--------

.. testsetup::

    import asyncio
    import inspect
    import unittest
    import threading
    from unittest.mock import sentinel, DEFAULT, ANY
    from unittest.mock import patch, call, Mock, MagicMock, PropertyMock, AsyncMock
    from unittest.mock import ThreadingMock
    from unittest.mock import mock_open

:class:`Mock` là một mock object linh hoạt, được dùng để thay thế stub và test double trong toàn bộ code của bạn. Mock có thể được gọi và tạo các thuộc tính dưới dạng mock mới khi bạn truy cập chúng [#]_. Việc truy cập cùng một thuộc tính sẽ luôn trả về cùng một mock. Mock ghi lại cách bạn sử dụng chúng, cho phép bạn đưa ra các assertion về những gì code của bạn đã thực hiện với chúng.

:class:`MagicMock` là một lớp con của :class:`Mock` với tất cả magic method được tạo sẵn và sẵn sàng sử dụng. Ngoài ra còn có các biến thể không thể gọi, hữu ích khi bạn mock các object không thể gọi:
:class:`NonCallableMock` và :class:`NonCallableMagicMock`

Các decorator :func:`patch` giúp dễ dàng tạm thời thay thế các class trong một module cụ thể bằng một đối tượng :class:`Mock`. Theo mặc định, :func:`patch` sẽ tạo một :class:`MagicMock` cho bạn. Bạn có thể chỉ định một class :class:`Mock` thay thế bằng cách sử dụng đối số *new_callable* cho :func:`patch`.


.. class:: Mock(spec=None, side_effect=None, return_value=DEFAULT, wraps=None, name=None, spec_set=None, unsafe=False, **kwargs)

    Tạo một đối tượng :class:`Mock` mới. :class:`Mock` nhận một số đối số tùy chọn để chỉ định hành vi của đối tượng Mock:

    * *spec*: Có thể là một danh sách chuỗi hoặc một object hiện có (một class hoặc instance) đóng vai trò là đặc tả cho mock object. Nếu truyền vào một object, một danh sách chuỗi sẽ được tạo bằng cách gọi dir trên object đó (không bao gồm các magic attribute và method không được hỗ trợ). Việc truy cập bất kỳ attribute nào không có trong danh sách này sẽ gây ra :exc:`AttributeError`.

      Nếu *spec* là một object (thay vì một danh sách chuỗi) thì
      :attr:`~object.__class__` trả về class của spec object. Điều này cho phép các mock vượt qua các bài kiểm tra :func:`isinstance`.

    * *spec_set*: Một biến thể nghiêm ngặt hơn của *spec*. Nếu được sử dụng, việc *set* hoặc lấy một attribute trên mock không có trong object được truyền vào *spec_set* sẽ gây ra :exc:`AttributeError`.

    * *side_effect*: Một hàm được gọi mỗi khi Mock được gọi. Xem thuộc tính :attr:`~Mock.side_effect`. Hữu ích để ném ngoại lệ hoặc thay đổi động các giá trị trả về. Hàm được gọi với cùng các đối số như mock và trừ khi hàm này trả về :data:`DEFAULT`, giá trị trả về của hàm sẽ được dùng làm giá trị trả về.

      Ngoài ra, *side_effect* có thể là một lớp hoặc một thực thể ngoại lệ. Trong trường hợp này, ngoại lệ sẽ được ném ra khi mock được gọi.

      Nếu *side_effect* là một iterable, thì mỗi lần gọi mock sẽ trả về giá trị tiếp theo từ iterable.

      Có thể xóa *side_effect* bằng cách đặt nó thành ``None``.

    * *return_value*: Giá trị được trả về khi mock được gọi. Theo mặc định, đây là một Mock mới (được tạo trong lần truy cập đầu tiên). Xem
      thuộc tính :attr:`return_value`.

    * *unsafe*: Theo mặc định, việc truy cập bất kỳ thuộc tính nào có tên bắt đầu bằng *assert*, *assret*, *asert*, *aseert* hoặc *assrt* sẽ ném ra một
      :exc:`AttributeError`. Việc truyền ``unsafe=True`` sẽ cho phép truy cập các thuộc tính này.

      .. versionadded:: 3.5

    * *wraps*: Đối tượng để mock bọc. Nếu *wraps* không phải là ``None`` thì việc gọi Mock sẽ chuyển tiếp lời gọi đến đối tượng được bọc (trả về kết quả thực). Việc truy cập thuộc tính trên mock sẽ trả về một đối tượng Mock bọc thuộc tính tương ứng của đối tượng được bọc (vì vậy, việc cố truy cập một thuộc tính không tồn tại sẽ gây ra :exc:`AttributeError`).

      Nếu mock đã được thiết lập *return_value* rõ ràng thì các lệnh gọi sẽ không được chuyển đến đối tượng được bọc, mà *return_value* sẽ được trả về.

    * *name*: Nếu mock có tên thì tên đó sẽ được sử dụng trong biểu diễn repr của mock. Điều này có thể hữu ích khi debug. Tên được truyền cho các mock con.

    Mock cũng có thể được gọi với các keyword argument tùy ý. Các đối số này sẽ được dùng để thiết lập thuộc tính trên mock sau khi mock được tạo. Xem
    :meth:`configure_mock` method để biết chi tiết.

    .. method:: assert_called()

        Xác nhận rằng mock đã được gọi ít nhất một lần.

            >>> mock = Mock()
            >>> mock.method()
            <Mock name='mock.method()' id='...'>
            >>> mock.method.assert_called()

        .. versionadded:: 3.6

    .. method:: assert_called_once()

        Xác nhận rằng mock đã được gọi đúng một lần.

            >>> mock = Mock()
            >>> mock.method()
            <Mock name='mock.method()' id='...'>
            >>> mock.method.assert_called_once()
            >>> mock.method()
            <Mock name='mock.method()' id='...'>
            >>> mock.method.assert_called_once()
            Traceback (most recent call last):
            ...
            AssertionError: Expected 'method' to have been called once. Called 2 times.
            Calls: [call(), call()].

        .. versionadded:: 3.6


    .. method:: assert_called_with(*args, **kwargs)

        Phương thức này là một cách thuận tiện để xác nhận rằng lần gọi cuối cùng được thực hiện theo một cách cụ thể:

            >>> mock = Mock()
            >>> mock.method(1, 2, 3, test='wow')
            <Mock name='mock.method()' id='...'>
            >>> mock.method.assert_called_with(1, 2, 3, test='wow')

    .. method:: assert_called_once_with(*args, **kwargs)

       Xác nhận rằng mock đã được gọi đúng một lần và lần gọi đó sử dụng các đối số được chỉ định.

            >>> mock = Mock(return_value=None)
            >>> mock('foo', bar='baz')
            >>> mock.assert_called_once_with('foo', bar='baz')
            >>> mock('other', bar='values')
            >>> mock.assert_called_once_with('other', bar='values')
            Traceback (most recent call last):
              ...
            AssertionError: Expected 'mock' to be called once. Called 2 times.
            Calls: [call('foo', bar='baz'), call('other', bar='values')].

    .. method:: assert_any_call(*args, **kwargs)

        Xác nhận rằng mock đã được gọi với các đối số được chỉ định.

        Phép xác nhận thành công nếu mock đã *ever* được gọi, không giống
        :meth:`assert_called_with` và :meth:`assert_called_once_with` chỉ thành công nếu lần gọi đó là lần gọi gần nhất, còn trong trường hợp
        :meth:`assert_called_once_with` thì đó cũng phải là lần gọi duy nhất.

            >>> mock = Mock(return_value=None)
            >>> mock(1, 2, arg='thing')
            >>> mock('some', 'thing', 'else')
            >>> mock.assert_any_call(1, 2, arg='thing')


    .. method:: assert_has_calls(calls, any_order=False)

        xác nhận rằng mock đã được gọi với các lệnh gọi được chỉ định. Danh sách :attr:`mock_calls` được kiểm tra để tìm các lệnh gọi đó.

        Nếu *any_order* là false thì các lệnh gọi phải theo thứ tự tuần tự. Có thể có các lệnh gọi bổ sung trước hoặc sau những lệnh gọi được chỉ định.

        Nếu *any_order* là true thì các lệnh gọi có thể theo bất kỳ thứ tự nào, nhưng tất cả chúng phải xuất hiện trong :attr:`mock_calls`.

            >>> mock = Mock(return_value=None)
            >>> mock(1)
            >>> mock(2)
            >>> mock(3)
            >>> mock(4)
            >>> calls = [call(2), call(3)]
            >>> mock.assert_has_calls(calls)
            >>> calls = [call(4), call(2), call(3)]
            >>> mock.assert_has_calls(calls, any_order=True)

    .. method:: assert_not_called()

        Xác nhận rằng mock chưa bao giờ được gọi.

            >>> m = Mock()
            >>> m.hello.assert_not_called()
            >>> obj = m.hello()
            >>> m.hello.assert_not_called()
            Traceback (most recent call last):
              ...
            AssertionError: Expected 'hello' to not have been called. Called 1 times.
            Calls: [call()].

        .. versionadded:: 3.5


    .. method:: reset_mock(*, return_value=False, side_effect=False)

        Phương thức reset_mock đặt lại tất cả các thuộc tính lệnh gọi trên một đối tượng mock:

        .. doctest::

            >>> mock = Mock(return_value=None)
            >>> mock('hello')
            >>> mock.called
            True
            >>> mock.reset_mock()
            >>> mock.called
            False

        Điều này hữu ích khi bạn muốn thực hiện một loạt xác nhận sử dụng lại cùng một đối tượng.

        Tham số *return_value* khi được đặt thành ``True`` sẽ đặt lại :attr:`return_value`:

        .. doctest::

            >>> mock = Mock(return_value=5)
            >>> mock('hello')
            5
            >>> mock.reset_mock(return_value=True)
            >>> mock('hello')  # doctest: +ELLIPSIS
            <Mock name='mock()' id='...'>

        tham số *side_effect* khi được đặt thành ``True`` sẽ đặt lại :attr:`side_effect`:

        .. doctest::

            >>> mock = Mock(side_effect=ValueError)
            >>> mock('hello')
            Traceback (most recent call last):
              ...
            ValueError
            >>> mock.reset_mock(side_effect=True)
            >>> mock('hello')  # doctest: +ELLIPSIS
            <Mock name='mock()' id='...'>

        Lưu ý rằng :meth:`reset_mock` *không* xóa
        :attr:`return_value`, :attr:`side_effect` hoặc bất kỳ thuộc tính con nào mà bạn đã đặt bằng phép gán thông thường theo mặc định.

        Các mock con cũng được đặt lại.

        .. versionchanged:: 3.6
           Đã thêm hai đối số chỉ dùng từ khóa vào hàm reset_mock.

    .. method:: mock_add_spec(spec, spec_set=False)

        Thêm một spec vào mock. *spec* có thể là một object hoặc một danh sách các chuỗi. Chỉ các thuộc tính trên *spec* mới có thể được truy xuất dưới dạng thuộc tính từ mock.

        Nếu *spec_set* là true thì chỉ các thuộc tính trên spec mới có thể được thiết lập.


    .. method:: attach_mock(mock, attribute)

        Gắn một mock làm thuộc tính của mock này, thay thế name và parent của nó. Các lệnh gọi đến mock được gắn sẽ được ghi lại trong
        :attr:`method_calls` và :attr:`mock_calls` thuộc tính của mock này.


    .. method:: configure_mock(**kwargs)

        Thiết lập các thuộc tính trên mock thông qua các đối số từ khóa.

        Có thể thiết lập các thuộc tính, cùng với giá trị trả về và side effect, trên các mock con bằng cách sử dụng ký hiệu dấu chấm tiêu chuẩn và giải nén một dictionary trong lời gọi phương thức:

            >>> mock = Mock()
            >>> attrs = {'method.return_value': 3, 'other.side_effect': KeyError}
            >>> mock.configure_mock(**attrs)
            >>> mock.method()
            3
            >>> mock.other()
            Traceback (most recent call last):
              ...
            KeyError

        Điều tương tự có thể được thực hiện trong lời gọi hàm khởi tạo của các mock:

            >>> attrs = {'method.return_value': 3, 'other.side_effect': KeyError}
            >>> mock = Mock(some_attribute='eggs', **attrs)
            >>> mock.some_attribute
            'eggs'
            >>> mock.method()
            3
            >>> mock.other()
            Traceback (most recent call last):
              ...
            KeyError

        :meth:`configure_mock` tồn tại để giúp việc cấu hình sau khi mock được tạo trở nên dễ dàng hơn.


    .. method:: __dir__()

        Các đối tượng :class:`Mock` giới hạn kết quả của ``dir(some_mock)`` ở những kết quả hữu ích. Đối với các mock có *spec*, các kết quả này bao gồm tất cả thuộc tính được phép của mock.

        Xem :data:`FILTER_DIR` để biết bộ lọc này thực hiện những gì và cách tắt nó.


    .. method:: _get_child_mock(**kw)

        Tạo các mock con cho các thuộc tính và giá trị trả về. Theo mặc định, các mock con sẽ có cùng kiểu với mock cha. Các lớp con của Mock có thể muốn ghi đè điều này để tùy chỉnh cách tạo mock con.

        Đối với các mock không thể gọi, biến thể có thể gọi sẽ được sử dụng (thay vì bất kỳ lớp con tùy chỉnh nào).


    .. attribute:: called

        Một giá trị boolean cho biết đối tượng mock đã được gọi hay chưa:

            >>> mock = Mock(return_value=None)
            >>> mock.called
            False
            >>> mock()
            >>> mock.called
            True

    .. attribute:: call_count

        Một số nguyên cho biết đối tượng mock đã được gọi bao nhiêu lần:

            >>> mock = Mock(return_value=None)
            >>> mock.call_count
            0
            >>> mock()
            >>> mock()
            >>> mock.call_count
            2

    .. attribute:: return_value

        Thiết lập giá trị được trả về khi gọi mock:

            >>> mock = Mock()
            >>> mock.return_value = 'fish'
            >>> mock()
            'fish'

        Giá trị trả về mặc định là một đối tượng mock và bạn có thể cấu hình đối tượng này theo cách thông thường:

            >>> mock = Mock()
            >>> mock.return_value.attribute = sentinel.Attribute
            >>> mock.return_value()
            <Mock name='mock()()' id='...'>
            >>> mock.return_value.assert_called_with()

        :attr:`return_value` cũng có thể được thiết lập trong constructor:

            >>> mock = Mock(return_value=3)
            >>> mock.return_value
            3
            >>> mock()
            3


    .. attribute:: side_effect

        Giá trị này có thể là một hàm được gọi khi mock được gọi, một iterable hoặc một exception (class hoặc instance) sẽ được raise.

        Nếu bạn truyền vào một hàm, hàm đó sẽ được gọi với cùng các đối số như mock và trừ khi hàm trả về singleton :data:`DEFAULT`, lệnh gọi mock sau đó sẽ trả về bất kỳ giá trị nào mà hàm trả về. Nếu hàm trả về :data:`DEFAULT` thì mock sẽ trả về giá trị thông thường của nó (từ :attr:`return_value`).

        Nếu bạn truyền vào một iterable, iterable đó sẽ được dùng để lấy một iterator, và iterator này phải yield một giá trị trong mỗi lần gọi. Giá trị này có thể là một exception instance cần được raise hoặc một giá trị được trả về từ lần gọi mock (:data:`DEFAULT` được xử lý giống hệt trường hợp hàm).

        Ví dụ về một mock raise exception (để kiểm thử việc xử lý exception của một API):

            >>> mock = Mock()
            >>> mock.side_effect = Exception('Boom!')
            >>> mock()
            Traceback (most recent call last):
              ...
            Exception: Boom!

        Sử dụng :attr:`side_effect` để trả về một chuỗi giá trị:

            >>> mock = Mock()
            >>> mock.side_effect = [3, 2, 1]
            >>> mock(), mock(), mock()
            (3, 2, 1)

        Sử dụng một đối tượng có thể gọi (callable):

            >>> mock = Mock(return_value=3)
            >>> def side_effect(*args, **kwargs):
            ...     return DEFAULT
            ...
            >>> mock.side_effect = side_effect
            >>> mock()
            3

        :attr:`side_effect` có thể được thiết lập trong hàm khởi tạo. Dưới đây là một ví dụ cộng thêm một vào giá trị mà mock được gọi với và trả về kết quả đó:

            >>> side_effect = lambda value: value + 1
            >>> mock = Mock(side_effect=side_effect)
            >>> mock(3)
            4
            >>> mock(-8)
            -7

        Đặt :attr:`side_effect` thành ``None`` sẽ xóa giá trị này:

            >>> m = Mock(side_effect=KeyError, return_value=3)
            >>> m()
            Traceback (most recent call last):
             ...
            KeyError
            >>> m.side_effect = None
            >>> m()
            3


    .. attribute:: call_args

        Đây là ``None`` (nếu mock chưa được gọi) hoặc các đối số mà mock được gọi lần cuối với chúng. Giá trị này có dạng một tuple: phần tử đầu tiên, cũng có thể được truy cập thông qua thuộc tính ``args``, là mọi đối số vị trí mà mock được gọi với (hoặc một tuple rỗng), còn phần tử thứ hai, cũng có thể được truy cập thông qua thuộc tính ``kwargs``, là mọi đối số từ khóa (hoặc một từ điển rỗng).

            >>> mock = Mock(return_value=None)
            >>> print(mock.call_args)
            None
            >>> mock()
            >>> mock.call_args
            call()
            >>> mock.call_args == ()
            True
            >>> mock(3, 4)
            >>> mock.call_args
            call(3, 4)
            >>> mock.call_args == ((3, 4),)
            True
            >>> mock.call_args.args
            (3, 4)
            >>> mock.call_args.kwargs
            {}
            >>> mock(3, 4, 5, key='fish', next='w00t!')
            >>> mock.call_args
            call(3, 4, 5, key='fish', next='w00t!')
            >>> mock.call_args.args
            (3, 4, 5)
            >>> mock.call_args.kwargs
            {'key': 'fish', 'next': 'w00t!'}

        :attr:`call_args`, cùng với các thành viên của các danh sách :attr:`call_args_list`,
        :attr:`method_calls` và :attr:`mock_calls` là các đối tượng :data:`call`. Đây là các tuple, vì vậy bạn có thể giải nén chúng để lấy từng đối số riêng lẻ và thực hiện các assertion phức tạp hơn. Xem
        :ref:`các lần gọi dưới dạng tuple <calls-as-tuples>`.

        .. versionchanged:: 3.8
           Đã thêm các thuộc tính ``args`` và ``kwargs``.


    .. attribute:: call_args_list

        Đây là danh sách tất cả các lần gọi được thực hiện đến đối tượng mock theo thứ tự (vì vậy độ dài của danh sách là số lần đối tượng đó được gọi). Trước khi có bất kỳ lần gọi nào, đây là một danh sách rỗng. Đối tượng
        :data:`call` có thể được dùng để thuận tiện tạo các danh sách các lần gọi nhằm so sánh với :attr:`call_args_list`.

            >>> mock = Mock(return_value=None)
            >>> mock()
            >>> mock(3, 4)
            >>> mock(key='fish', next='w00t!')
            >>> mock.call_args_list
            [call(), call(3, 4), call(key='fish', next='w00t!')]
            >>> expected = [(), ((3, 4),), ({'key': 'fish', 'next': 'w00t!'},)]
            >>> mock.call_args_list == expected
            True

        Các phần tử của :attr:`call_args_list` là các đối tượng :data:`call`. Có thể giải nén chúng dưới dạng tuple để lấy từng đối số riêng lẻ. Xem
        :ref:`các lần gọi dưới dạng tuple <calls-as-tuples>`.


    .. attribute:: method_calls

        Ngoài việc theo dõi các lần gọi đến chính chúng, các mock còn theo dõi các lần gọi đến phương thức và thuộc tính, cũng như các phương thức và thuộc tính *của chúng*:

            >>> mock = Mock()
            >>> mock.method()
            <Mock name='mock.method()' id='...'>
            >>> mock.property.method.attribute()
            <Mock name='mock.property.method.attribute()' id='...'>
            >>> mock.method_calls
            [call.method(), call.property.method.attribute()]

        Các thành viên của :attr:`method_calls` là các đối tượng :data:`call`. Có thể giải nén chúng dưới dạng tuple để truy cập từng đối số riêng lẻ. Xem
        :ref:`các lần gọi dưới dạng tuple <calls-as-tuples>`.


    .. attribute:: mock_calls

        :attr:`mock_calls` ghi lại *all* lần gọi đến đối tượng mock, các phương thức của nó, các phương thức magic *and* các mock giá trị trả về.

            >>> mock = MagicMock()
            >>> result = mock(1, 2, 3)
            >>> mock.first(a=3)
            <MagicMock name='mock.first()' id='...'>
            >>> mock.second()
            <MagicMock name='mock.second()' id='...'>
            >>> int(mock)
            1
            >>> result(1)
            <MagicMock name='mock()()' id='...'>
            >>> expected = [call(1, 2, 3), call.first(a=3), call.second(),
            ... call.__int__(), call()(1)]
            >>> mock.mock_calls == expected
            True

        Các thành viên của :attr:`mock_calls` là các đối tượng :data:`call`. Có thể giải nén chúng dưới dạng tuple để truy cập từng đối số riêng lẻ. Xem
        :ref:`các lần gọi dưới dạng tuple <calls-as-tuples>`.

        .. note::

            Cách :attr:`mock_calls` được ghi lại có nghĩa là khi thực hiện các lần gọi lồng nhau, các tham số của những lần gọi cấp cao hơn không được ghi lại và vì vậy sẽ luôn được xem là bằng nhau:

                >>> mock = MagicMock()
                >>> mock.top(a=3).bottom()
                <MagicMock name='mock.top().bottom()' id='...'>
                >>> mock.mock_calls
                [call.top(a=3), call.top().bottom()]
                >>> mock.mock_calls[-1] == call.top(a=-1).bottom()
                True

    .. attribute:: __class__

        Thông thường, thuộc tính :attr:`!__class__` của một đối tượng sẽ trả về kiểu của đối tượng đó. Đối với một đối tượng mock có :attr:`!spec`, :attr:`!__class__` sẽ trả về lớp spec thay thế. Điều này cho phép các đối tượng mock vượt qua các phép kiểm tra :func:`isinstance` đối với đối tượng mà chúng đang thay thế hoặc giả lập:

            >>> mock = Mock(spec=3)
            >>> isinstance(mock, int)
            True

        :attr:`!__class__` có thể được gán cho, điều này cho phép một mock vượt qua một
        :func:`isinstance` kiểm tra mà không buộc bạn phải sử dụng spec:

            >>> mock = Mock()
            >>> mock.__class__ = dict
            >>> isinstance(mock, dict)
            True

.. class:: NonCallableMock(spec=None, wraps=None, name=None, spec_set=None, **kwargs)

    Một phiên bản không thể gọi của :class:`Mock`. Các tham số constructor có cùng ý nghĩa với :class:`Mock`, ngoại trừ *return_value* và *side_effect* không có ý nghĩa đối với một mock không thể gọi.

Các đối tượng mock sử dụng một class hoặc một instance làm :attr:`!spec` hoặc
:attr:`!spec_set` có thể vượt qua các bài kiểm tra :func:`isinstance`:

    >>> mock = Mock(spec=SomeClass)
    >>> isinstance(mock, SomeClass)
    True
    >>> mock = Mock(spec_set=SomeClass())
    >>> isinstance(mock, SomeClass)
    True

Các class :class:`Mock` hỗ trợ mock các magic method. Xem :ref:`magic methods <magic-methods>` để biết đầy đủ chi tiết.

Các class mock và các decorator :func:`patch` đều nhận các đối số từ khóa tùy ý để cấu hình. Đối với các decorator :func:`patch`, các từ khóa được truyền vào constructor của mock được tạo. Các đối số từ khóa dùng để cấu hình các thuộc tính của mock:

        >>> m = MagicMock(attribute=3, other='fish')
        >>> m.attribute
        3
        >>> m.other
        'fish'

Giá trị trả về và side effect của các mock con có thể được thiết lập theo cùng một cách, bằng cách sử dụng ký hiệu dấu chấm. Vì bạn không thể sử dụng trực tiếp tên có dấu chấm trong một lời gọi, bạn phải tạo một dictionary rồi unpack nó bằng ``**``:.

    >>> attrs = {'method.return_value': 3, 'other.side_effect': KeyError}
    >>> mock = Mock(some_attribute='eggs', **attrs)
    >>> mock.some_attribute
    'eggs'
    >>> mock.method()
    3
    >>> mock.other()
    Traceback (most recent call last):
      ...
    KeyError

Một mock có thể gọi được được tạo với *spec* (hoặc *spec_set*) sẽ kiểm tra introspection chữ ký của đối tượng đặc tả khi đối chiếu các lời gọi với mock. Do đó, nó có thể đối chiếu các đối số của lời gọi thực tế bất kể chúng được truyền theo vị trí hay theo tên::

   >>> def f(a, b, c): pass
   ...
   >>> mock = Mock(spec=f)
   >>> mock(1, 2, c=3)
   <Mock name='mock()' id='140161580456576'>
   >>> mock.assert_called_with(1, 2, 3)
   >>> mock.assert_called_with(a=1, b=2, c=3)

Điều này áp dụng cho :meth:`~Mock.assert_called_with`,
:meth:`~Mock.assert_called_once_with`, :meth:`~Mock.assert_has_calls` và
:meth:`~Mock.assert_any_call`. Khi :ref:`auto-speccing`, điều này cũng sẽ áp dụng cho các lời gọi phương thức trên đối tượng mock.

.. versionchanged:: 3.4
   Đã bổ sung khả năng kiểm tra introspection chữ ký trên các đối tượng mock có spec và autospec.


.. class:: PropertyMock(*args, **kwargs)

   Một mock được dùng làm :class:`property`, hoặc làm một đối tượng khác
   :term:`descriptor`, trên một class. :class:`PropertyMock` cung cấp
   các phương thức :meth:`~object.__get__` và :meth:`~object.__set__` để bạn có thể chỉ định giá trị trả về khi lấy nó.

   Việc lấy một instance :class:`PropertyMock` từ một đối tượng sẽ gọi mock mà không có đối số. Việc thiết lập nó sẽ gọi mock với giá trị đang được thiết lập.::

        >>> class Foo:
        ...     @property
        ...     def foo(self):
        ...         return 'something'
        ...     @foo.setter
        ...     def foo(self, value):
        ...         pass
        ...
        >>> with patch('__main__.Foo.foo', new_callable=PropertyMock) as mock_foo:
        ...     mock_foo.return_value = 'mockity-mock'
        ...     this_foo = Foo()
        ...     print(this_foo.foo)
        ...     this_foo.foo = 6
        ...
        mockity-mock
        >>> mock_foo.mock_calls
        [call(), call(6)]

Do cách các thuộc tính mock được lưu trữ, bạn không thể trực tiếp gắn một
:class:`PropertyMock` vào một đối tượng mock. Thay vào đó, bạn có thể gắn nó vào đối tượng kiểu mock::

    >>> m = MagicMock()
    >>> p = PropertyMock(return_value=3)
    >>> type(m).foo = p
    >>> m.foo
    3
    >>> p.assert_called_once_with()

.. caution::

    Nếu một :exc:`AttributeError` được :class:`PropertyMock` đưa ra, nó sẽ được hiểu là một descriptor bị thiếu và
    :meth:`~object.__getattr__` sẽ được gọi trên mock cha::

        >>> m = MagicMock()
        >>> no_attribute = PropertyMock(side_effect=AttributeError)
        >>> type(m).my_property = no_attribute
        >>> m.my_property
        <MagicMock name='mock.my_property' id='140165240345424'>

    Xem :meth:`~object.__getattr__` để biết chi tiết.


.. class:: AsyncMock(spec=None, side_effect=None, return_value=DEFAULT, wraps=None, name=None, spec_set=None, unsafe=False, **kwargs)

  Một phiên bản bất đồng bộ của :class:`MagicMock`. Đối tượng :class:`AsyncMock` sẽ hoạt động sao cho được nhận diện là một hàm async và kết quả của một lần gọi là một awaitable.

    >>> mock = AsyncMock()
    >>> inspect.iscoroutinefunction(mock)
    True
    >>> inspect.isawaitable(mock())  # doctest: +SKIP
    True

  Kết quả của ``mock()`` là một hàm async, hàm này sẽ có kết quả là ``side_effect`` hoặc ``return_value`` sau khi được await:

  - nếu ``side_effect`` là một hàm, hàm async sẽ trả về kết quả của hàm đó,
  - nếu ``side_effect`` là một exception, hàm async sẽ raise exception đó,
  - nếu ``side_effect`` là một iterable, hàm async sẽ trả về giá trị tiếp theo của iterable; tuy nhiên, nếu chuỗi kết quả là
    :term:`exhausted`, ``StopAsyncIteration`` được phát sinh ngay lập tức,
  - nếu ``side_effect`` chưa được định nghĩa, async function sẽ trả về giá trị được định nghĩa bởi ``return_value``, do đó, theo mặc định, async function trả về một đối tượng :class:`AsyncMock` mới.


  Việc đặt *spec* của một :class:`Mock` hoặc :class:`MagicMock` thành một async function sẽ khiến một đối tượng coroutine được trả về sau khi gọi.

    >>> async def async_func(): pass
    ...
    >>> mock = MagicMock(async_func)
    >>> mock
    <MagicMock spec='function' id='...'>
    >>> mock()  # doctest: +SKIP
    <coroutine object AsyncMockMixin._mock_call at ...>


  Việc đặt *spec* của một :class:`Mock`, :class:`MagicMock` hoặc :class:`AsyncMock` thành một lớp có các function bất đồng bộ và đồng bộ sẽ tự động phát hiện các function đồng bộ và đặt chúng thành :class:`MagicMock` (nếu mock cha là :class:`AsyncMock` hoặc :class:`MagicMock`) hoặc :class:`Mock` (nếu mock cha là :class:`Mock`). Tất cả các function bất đồng bộ sẽ được
  :class:`AsyncMock`.

  >>> class ExampleClass:
  ...     def sync_foo():
  ...         pass
  ...     async def async_foo():
  ...         pass
  ...
  >>> a_mock = AsyncMock(ExampleClass)
  >>> a_mock.sync_foo
  <MagicMock name='mock.sync_foo' id='...'>
  >>> a_mock.async_foo
  <AsyncMock name='mock.async_foo' id='...'>
  >>> mock = Mock(ExampleClass)
  >>> mock.sync_foo
  <Mock name='mock.sync_foo' id='...'>
  >>> mock.async_foo
  <AsyncMock name='mock.async_foo' id='...'>

  .. versionadded:: 3.8

  .. method:: assert_awaited()

      Khẳng định rằng mock đã được await ít nhất một lần. Lưu ý rằng điều này khác với việc đối tượng đã được gọi; phải sử dụng keyword ``await``:

          >>> mock = AsyncMock()
          >>> async def main(coroutine_mock):
          ...     await coroutine_mock
          ...
          >>> coroutine_mock = mock()
          >>> mock.called
          True
          >>> mock.assert_awaited()
          Traceback (most recent call last):
          ...
          AssertionError: Expected mock to have been awaited.
          >>> asyncio.run(main(coroutine_mock))
          >>> mock.assert_awaited()

  .. method:: assert_awaited_once()

      Khẳng định rằng mock đã được await chính xác một lần.

        >>> mock = AsyncMock()
        >>> async def main():
        ...     await mock()
        ...
        >>> asyncio.run(main())
        >>> mock.assert_awaited_once()
        >>> asyncio.run(main())
        >>> mock.assert_awaited_once()
        Traceback (most recent call last):
        ...
        AssertionError: Expected mock to have been awaited once. Awaited 2 times.

  .. method:: assert_awaited_with(*args, **kwargs)

      Xác nhận rằng lần await cuối cùng sử dụng các đối số được chỉ định.

        >>> mock = AsyncMock()
        >>> async def main(*args, **kwargs):
        ...     await mock(*args, **kwargs)
        ...
        >>> asyncio.run(main('foo', bar='bar'))
        >>> mock.assert_awaited_with('foo', bar='bar')
        >>> mock.assert_awaited_with('other')
        Traceback (most recent call last):
        ...
        AssertionError: expected await not found.
        Expected: mock('other')
        Actual: mock('foo', bar='bar')

  .. method:: assert_awaited_once_with(*args, **kwargs)

      Xác nhận rằng mock đã được await chính xác một lần và với các đối số được chỉ định.

        >>> mock = AsyncMock()
        >>> async def main(*args, **kwargs):
        ...     await mock(*args, **kwargs)
        ...
        >>> asyncio.run(main('foo', bar='bar'))
        >>> mock.assert_awaited_once_with('foo', bar='bar')
        >>> asyncio.run(main('foo', bar='bar'))
        >>> mock.assert_awaited_once_with('foo', bar='bar')
        Traceback (most recent call last):
        ...
        AssertionError: Expected mock to have been awaited once. Awaited 2 times.

  .. method:: assert_any_await(*args, **kwargs)

      Xác nhận rằng mock đã từng được await với các đối số được chỉ định.

        >>> mock = AsyncMock()
        >>> async def main(*args, **kwargs):
        ...     await mock(*args, **kwargs)
        ...
        >>> asyncio.run(main('foo', bar='bar'))
        >>> asyncio.run(main('hello'))
        >>> mock.assert_any_await('foo', bar='bar')
        >>> mock.assert_any_await('other')
        Traceback (most recent call last):
        ...
        AssertionError: mock('other') await not found

  .. method:: assert_has_awaits(calls, any_order=False)

      Xác nhận rằng mock đã được await với các lời gọi được chỉ định. Danh sách :attr:`await_args_list` được kiểm tra để xác nhận các lần await.

      Nếu *any_order* là false thì các lần await phải diễn ra tuần tự. Có thể có các lời gọi bổ sung trước hoặc sau những lần await được chỉ định.

      Nếu *any_order* là true thì các lần await có thể diễn ra theo bất kỳ thứ tự nào, nhưng tất cả phải xuất hiện trong :attr:`await_args_list`.

        >>> mock = AsyncMock()
        >>> async def main(*args, **kwargs):
        ...     await mock(*args, **kwargs)
        ...
        >>> calls = [call("foo"), call("bar")]
        >>> mock.assert_has_awaits(calls)
        Traceback (most recent call last):
        ...
        AssertionError: Awaits not found.
        Expected: [call('foo'), call('bar')]
        Actual: []
        >>> asyncio.run(main('foo'))
        >>> asyncio.run(main('bar'))
        >>> mock.assert_has_awaits(calls)

  .. method:: assert_not_awaited()

    Xác nhận rằng mock chưa bao giờ được await.

        >>> mock = AsyncMock()
        >>> mock.assert_not_awaited()

  .. method:: reset_mock(*args, **kwargs)

    Xem :func:`Mock.reset_mock`. Đồng thời đặt :attr:`await_count` thành 0,
    :attr:`await_args` thành None và xóa :attr:`await_args_list`.

  .. attribute:: await_count

    Một số nguyên theo dõi số lần đối tượng mock đã được await.

      >>> mock = AsyncMock()
      >>> async def main():
      ...     await mock()
      ...
      >>> asyncio.run(main())
      >>> mock.await_count
      1
      >>> asyncio.run(main())
      >>> mock.await_count
      2

  .. attribute:: await_args

    Đây là ``None`` (nếu mock chưa được await), hoặc các đối số mà mock được await lần cuối cùng với. Hoạt động giống :attr:`Mock.call_args`.

      >>> mock = AsyncMock()
      >>> async def main(*args):
      ...     await mock(*args)
      ...
      >>> mock.await_args
      >>> asyncio.run(main('foo'))
      >>> mock.await_args
      call('foo')
      >>> asyncio.run(main('bar'))
      >>> mock.await_args
      call('bar')


  .. attribute:: await_args_list

    Đây là danh sách tất cả các lần await đối tượng mock theo thứ tự (vì vậy độ dài của danh sách là số lần đối tượng đã được await). Trước khi có bất kỳ lần await nào, đây là một danh sách rỗng.

      >>> mock = AsyncMock()
      >>> async def main(*args):
      ...     await mock(*args)
      ...
      >>> mock.await_args_list
      []
      >>> asyncio.run(main('foo'))
      >>> mock.await_args_list
      [call('foo')]
      >>> asyncio.run(main('bar'))
      >>> mock.await_args_list
      [call('foo'), call('bar')]


.. class:: ThreadingMock(spec=None, side_effect=None, return_value=DEFAULT, wraps=None, name=None, spec_set=None, unsafe=False, *, timeout=UNSET, **kwargs)

  Một phiên bản của :class:`MagicMock` dành cho các bài kiểm thử đa luồng. Đối tượng
  :class:`ThreadingMock` cung cấp các phương thức bổ sung để chờ một lệnh gọi được thực thi, thay vì xác nhận ngay lập tức.

  Thời gian chờ mặc định được chỉ định bởi đối số ``timeout``, hoặc nếu chưa được đặt thì bởi
  thuộc tính :attr:`ThreadingMock.DEFAULT_TIMEOUT`, thuộc tính này mặc định là blocking (``None``).

  Bạn có thể cấu hình thời gian chờ mặc định toàn cục bằng cách đặt :attr:`ThreadingMock.DEFAULT_TIMEOUT`.

  .. method:: wait_until_called(*, timeout=UNSET)

      Chờ cho đến khi mock được gọi.

      Nếu một thời gian chờ được truyền khi tạo mock hoặc một đối số thời gian chờ được truyền cho hàm này, hàm sẽ phát sinh một
      :exc:`AssertionError` nếu lệnh gọi không được thực hiện kịp thời.

        >>> mock = ThreadingMock()
        >>> thread = threading.Thread(target=mock)
        >>> thread.start()
        >>> mock.wait_until_called(timeout=1)
        >>> thread.join()

  .. method:: wait_until_any_call_with(*args, **kwargs)

      Chờ cho đến khi mock được gọi với các đối số đã chỉ định.

      Nếu một timeout được truyền vào khi tạo mock, hàm sẽ phát sinh một :exc:`AssertionError` nếu lệnh gọi không được thực hiện kịp thời.

        >>> mock = ThreadingMock()
        >>> thread = threading.Thread(target=mock, args=("arg1", "arg2",), kwargs={"arg": "thing"})
        >>> thread.start()
        >>> mock.wait_until_any_call_with("arg1", "arg2", arg="thing")
        >>> thread.join()

  .. attribute:: DEFAULT_TIMEOUT

    Timeout mặc định toàn cục tính bằng giây để tạo các instance của :class:`ThreadingMock`.

  .. versionadded:: 3.13


Gọi
~~~

Các đối tượng Mock có thể được gọi. Lệnh gọi sẽ trả về giá trị được thiết lập làm
thuộc tính :attr:`~Mock.return_value`. Giá trị trả về mặc định là một đối tượng Mock mới; đối tượng này được tạo lần đầu tiên khi giá trị trả về được truy cập (dù là truy cập rõ ràng hay bằng cách gọi Mock), nhưng được lưu lại và cùng một đối tượng sẽ được trả về mỗi lần.

Các lệnh gọi được thực hiện trên đối tượng sẽ được ghi lại trong những thuộc tính như :attr:`~Mock.call_args` và :attr:`~Mock.call_args_list`.

Nếu :attr:`~Mock.side_effect` được thiết lập thì nó sẽ được gọi sau khi lệnh gọi đã được ghi lại, vì vậy nếu :attr:`!side_effect` phát sinh một ngoại lệ thì lệnh gọi vẫn được ghi lại.

Cách đơn giản nhất để khiến một mock phát sinh ngoại lệ khi được gọi là đặt
:attr:`~Mock.side_effect` thành một lớp hoặc thực thể ngoại lệ:

        >>> m = MagicMock(side_effect=IndexError)
        >>> m(1, 2, 3)
        Traceback (most recent call last):
          ...
        IndexError
        >>> m.mock_calls
        [call(1, 2, 3)]
        >>> m.side_effect = KeyError('Bang!')
        >>> m('two', 'three', 'four')
        Traceback (most recent call last):
          ...
        KeyError: 'Bang!'
        >>> m.mock_calls
        [call(1, 2, 3), call('two', 'three', 'four')]

Nếu :attr:`~Mock.side_effect` là một hàm thì giá trị mà hàm đó trả về sẽ là giá trị mà các lần gọi mock trả về. Hàm :attr:`!side_effect` được gọi với cùng các đối số như mock. Điều này cho phép bạn thay đổi linh động giá trị trả về của lệnh gọi dựa trên đầu vào:

        >>> def side_effect(value):
        ...     return value + 1
        ...
        >>> m = MagicMock(side_effect=side_effect)
        >>> m(1)
        2
        >>> m(2)
        3
        >>> m.mock_calls
        [call(1), call(2)]

Nếu muốn mock vẫn trả về giá trị trả về mặc định (một mock mới) hoặc bất kỳ giá trị trả về nào đã được thiết lập, có hai cách để thực hiện việc này. Hoặc trả về
:attr:`~Mock.return_value` từ bên trong :attr:`~Mock.side_effect`, hoặc trả về :data:`DEFAULT`:

        >>> m = MagicMock()
        >>> def side_effect(*args, **kwargs):
        ...     return m.return_value
        ...
        >>> m.side_effect = side_effect
        >>> m.return_value = 3
        >>> m()
        3
        >>> def side_effect(*args, **kwargs):
        ...     return DEFAULT
        ...
        >>> m.side_effect = side_effect
        >>> m()
        3

Để xóa :attr:`~Mock.side_effect` và trở về hành vi mặc định, hãy đặt
:attr:`!side_effect` thành ``None``:

        >>> m = MagicMock(return_value=6)
        >>> def side_effect(*args, **kwargs):
        ...     return 3
        ...
        >>> m.side_effect = side_effect
        >>> m()
        3
        >>> m.side_effect = None
        >>> m()
        6

:attr:`~Mock.side_effect` cũng có thể là bất kỳ đối tượng iterable nào. Các lần gọi mock lặp lại sẽ trả về các giá trị từ iterable đó (cho đến khi iterable :term:`exhausted` và một :exc:`StopIteration` được phát sinh):

        >>> m = MagicMock(side_effect=[1, 2, 3])
        >>> m()
        1
        >>> m()
        2
        >>> m()
        3
        >>> m()
        Traceback (most recent call last):
          ...
        StopIteration

Nếu bất kỳ phần tử nào của iterable là exception, chúng sẽ được phát sinh thay vì được trả về::

        >>> iterable = (33, ValueError, 66)
        >>> m = MagicMock(side_effect=iterable)
        >>> m()
        33
        >>> m()
        Traceback (most recent call last):
         ...
        ValueError
        >>> m()
        66


.. _deleting-attributes:

Xóa thuộc tính
~~~~~~~~~~~~~~

Các đối tượng Mock tạo thuộc tính theo yêu cầu. Điều này cho phép chúng giả lập các đối tượng thuộc bất kỳ kiểu nào.

Bạn có thể muốn một đối tượng mock trả về ``False`` cho một lời gọi :func:`hasattr`, hoặc phát sinh một
:exc:`AttributeError` khi một thuộc tính được truy xuất. Bạn có thể thực hiện việc này bằng cách cung cấp một đối tượng làm :attr:`!spec` cho một mock, nhưng cách đó không phải lúc nào cũng thuận tiện.

Bạn "chặn" các thuộc tính bằng cách xóa chúng. Sau khi bị xóa, việc truy cập một thuộc tính sẽ phát sinh một :exc:`AttributeError`.

    >>> mock = MagicMock()
    >>> hasattr(mock, 'm')
    True
    >>> del mock.m
    >>> hasattr(mock, 'm')
    False
    >>> del mock.f
    >>> mock.f
    Traceback (most recent call last):
        ...
    AttributeError: f


Tên mock và thuộc tính name
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Vì "name" là một đối số của constructor :class:`Mock`, nếu muốn đối tượng mock của bạn có thuộc tính "name", bạn không thể chỉ truyền thuộc tính này vào khi tạo. Có hai lựa chọn. Một lựa chọn là sử dụng
:meth:`~Mock.configure_mock`::

    >>> mock = MagicMock()
    >>> mock.configure_mock(name='my_name')
    >>> mock.name
    'my_name'

Một lựa chọn đơn giản hơn là chỉ cần đặt thuộc tính "name" sau khi tạo mock::

    >>> mock = MagicMock()
    >>> mock.name = "foo"


Đính kèm Mock dưới dạng thuộc tính
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Khi bạn đính kèm một mock làm thuộc tính của một mock khác (hoặc làm giá trị trả về), nó sẽ trở thành một "child" của mock đó. Các lần gọi đến child được ghi lại trong các thuộc tính :attr:`~Mock.method_calls` và :attr:`~Mock.mock_calls` của parent. Điều này hữu ích khi cấu hình các child mock rồi đính kèm chúng vào parent, hoặc khi đính kèm các mock vào một parent ghi lại tất cả các lần gọi đến các child và cho phép bạn kiểm tra thứ tự gọi giữa các mock:

    >>> parent = MagicMock()
    >>> child1 = MagicMock(return_value=None)
    >>> child2 = MagicMock(return_value=None)
    >>> parent.child1 = child1
    >>> parent.child2 = child2
    >>> child1(1)
    >>> child2(2)
    >>> parent.mock_calls
    [call.child1(1), call.child2(2)]

Ngoại lệ là khi mock có tên. Điều này cho phép bạn ngăn việc "parenting" nếu vì lý do nào đó bạn không muốn việc này xảy ra.

    >>> mock = MagicMock()
    >>> not_a_child = MagicMock(name='not-a-child')
    >>> mock.attribute = not_a_child
    >>> mock.attribute()
    <MagicMock name='not-a-child()' id='...'>
    >>> mock.mock_calls
    []

Các mock được :func:`patch` tạo cho bạn sẽ tự động được đặt tên. Để đính kèm các mock có tên vào một parent, bạn sử dụng phương thức :meth:`~Mock.attach_mock`::

    >>> thing1 = object()
    >>> thing2 = object()
    >>> parent = MagicMock()
    >>> with patch('__main__.thing1', return_value=None) as child1:
    ...     with patch('__main__.thing2', return_value=None) as child2:
    ...         parent.attach_mock(child1, 'child1')
    ...         parent.attach_mock(child2, 'child2')
    ...         child1('one')
    ...         child2('two')
    ...
    >>> parent.mock_calls
    [call.child1('one'), call.child2('two')]


.. [#] Các ngoại lệ duy nhất là magic methods và attributes (những phương thức và thuộc tính có hai dấu gạch dưới ở đầu và cuối). Mock không tạo các đối tượng này mà thay vào đó sẽ phát sinh :exc:`AttributeError`. Điều này là do interpreter thường sẽ ngầm yêu cầu các phương thức này và sẽ *rất* bối rối khi tạo một đối tượng Mock mới trong lúc nó mong đợi một magic method. Nếu cần hỗ trợ magic method, hãy xem :ref:`magic methods <magic-methods>`.


Các patcher
-----------

Các patch decorator được dùng để patch các đối tượng chỉ trong phạm vi của hàm mà chúng decorate. Chúng tự động xử lý việc bỏ patch cho bạn, ngay cả khi có exception xảy ra. Tất cả các hàm này cũng có thể được dùng trong các câu lệnh with hoặc làm class decorator.


patch
~~~~~

.. note::

    Điều quan trọng là thực hiện patch trong đúng namespace. Xem phần `where to patch <where to patch_>`_.

.. function:: patch(target, new=DEFAULT, spec=None, create=False, spec_set=None, autospec=None, new_callable=None, **kwargs)

    :func:`patch` hoạt động như một function decorator, class decorator hoặc context manager. Bên trong phần thân của hàm hoặc câu lệnh with, *target* được patch bằng một đối tượng *new*. Khi hàm/câu lệnh with kết thúc, patch sẽ được hoàn tác.

    Nếu *new* bị bỏ qua, target sẽ được thay thế bằng một
    :class:`AsyncMock` nếu đối tượng được patch là một hàm async, hoặc :class:`MagicMock` nếu không phải. Nếu :func:`patch` được dùng làm decorator và *new* bị bỏ qua, mock được tạo sẽ được truyền vào làm đối số bổ sung cho hàm được trang trí. Nếu :func:`patch` được dùng làm context manager, mock được tạo sẽ được context manager trả về.

    *target* phải là một chuỗi có dạng ``'package.module.ClassName'``. *target* được import và đối tượng được chỉ định sẽ được thay thế bằng đối tượng *new*, vì vậy *target* phải có thể import được từ môi trường nơi bạn gọi :func:`patch`. Target được import khi hàm được trang trí thực thi, không phải tại thời điểm áp dụng decorator.

    Các đối số từ khóa *spec* và *spec_set* sẽ được truyền cho :class:`MagicMock` nếu patch tạo đối tượng này giúp bạn.

    Ngoài ra, bạn có thể truyền ``spec=True`` hoặc ``spec_set=True``, khiến patch truyền đối tượng đang được mock làm đối tượng spec/spec_set.

    *new_callable* cho phép bạn chỉ định một class hoặc đối tượng callable khác, đối tượng này sẽ được gọi để tạo đối tượng *new*. Theo mặc định, :class:`AsyncMock` được dùng cho các hàm async và :class:`MagicMock` được dùng cho các trường hợp còn lại.

    Một dạng mạnh hơn của *spec* là *autospec*. Nếu bạn đặt ``autospec=True``, mock sẽ được tạo với spec lấy từ đối tượng đang được thay thế. Tất cả thuộc tính của mock cũng sẽ có spec của thuộc tính tương ứng trên đối tượng đang được thay thế. Các method và hàm đang được mock sẽ được kiểm tra các đối số và sẽ phát sinh :exc:`TypeError` nếu được gọi với signature không đúng. Đối với mock thay thế một class, giá trị trả về của chúng ("instance") sẽ có cùng spec với class đó. Xem hàm :func:`create_autospec` và
    :ref:`auto-speccing`.

    Thay vì ``autospec=True``, bạn có thể truyền ``autospec=some_object`` để dùng một đối tượng tùy ý làm spec thay cho đối tượng đang được thay thế.

    Theo mặc định, :func:`patch` sẽ không thay thế các attribute không tồn tại. Nếu bạn truyền ``create=True``, và attribute đó không tồn tại, patch sẽ tạo attribute đó cho bạn khi hàm được patch được gọi, rồi xóa nó sau khi hàm được patch kết thúc. Điều này hữu ích khi viết test cho các attribute mà code production của bạn tạo ra trong runtime. Tùy chọn này mặc định bị tắt vì có thể gây nguy hiểm. Khi bật tùy chọn này, bạn có thể viết các test thành công cho những API thực tế không tồn tại!

    .. note::

       .. versionchanged:: 3.5
          Nếu bạn đang patch builtins trong một module thì không cần truyền ``create=True``; nó sẽ được tự động thêm vào.

    Patch có thể được dùng làm decorator cho class :class:`~unittest.TestCase`. Nó hoạt động bằng cách áp dụng decorator cho từng phương thức test trong class. Điều này giúp giảm phần code dư thừa khi các phương thức test của bạn dùng chung một tập patching. :func:`patch` tìm các test bằng cách tìm những tên phương thức bắt đầu bằng ``patch.TEST_PREFIX``. Theo mặc định, tiền tố này là ``'test'``, phù hợp với cách :mod:`unittest` tìm các test. Bạn có thể chỉ định tiền tố khác bằng cách đặt ``patch.TEST_PREFIX``.

    Patch có thể được dùng như một context manager với câu lệnh with. Trong trường hợp này, việc patching được áp dụng cho block thụt lề sau câu lệnh with. Nếu bạn dùng "as", đối tượng đã được patch sẽ được liên kết với tên đứng sau "as"; điều này rất hữu ích nếu :func:`patch` đang tạo một mock object cho bạn.

    :func:`patch` nhận các keyword argument tùy ý. Những đối số này sẽ được truyền cho
    :class:`AsyncMock` nếu đối tượng được patch là bất đồng bộ (asynchronous), cho
    :class:`MagicMock` trong các trường hợp khác hoặc cho *new_callable* nếu được chỉ định.

    ``patch.dict(...)``, ``patch.multiple(...)`` và ``patch.object(...)`` có sẵn cho các trường hợp sử dụng thay thế.

:func:`patch` dưới dạng function decorator, tự tạo mock cho bạn và truyền mock đó vào hàm được trang trí::

    >>> @patch('__main__.SomeClass')
    ... def function(normal_argument, mock_class):
    ...     print(mock_class is SomeClass)
    ...
    >>> function(None)
    True

Việc patch một class sẽ thay thế class đó bằng một :class:`MagicMock` *instance*. Nếu class được khởi tạo trong code đang được kiểm thử thì đó sẽ là
:attr:`~Mock.return_value` của mock được sử dụng.

Nếu class được khởi tạo nhiều lần, bạn có thể dùng
:attr:`~Mock.side_effect` để trả về một mock mới mỗi lần. Ngoài ra, bạn có thể đặt *return_value* thành bất kỳ giá trị nào bạn muốn.

Để cấu hình các giá trị trả về trên các phương thức của *instances* trên class đã được patch, bạn phải thực hiện việc này trên :attr:`~Mock.return_value`. Ví dụ::

    >>> class Class:
    ...     def method(self):
    ...         pass
    ...
    >>> with patch('__main__.Class') as MockClass:
    ...     instance = MockClass.return_value
    ...     instance.method.return_value = 'foo'
    ...     assert Class() is instance
    ...     assert Class().method() == 'foo'
    ...

Nếu bạn sử dụng *spec* hoặc *spec_set* và :func:`patch` đang thay thế một *class*, thì giá trị trả về của mock được tạo sẽ có cùng spec.::

    >>> Original = Class
    >>> patcher = patch('__main__.Class', spec=True)
    >>> MockClass = patcher.start()
    >>> instance = MockClass()
    >>> assert isinstance(instance, Original)
    >>> patcher.stop()

Đối số *new_callable* hữu ích khi bạn muốn sử dụng một class thay thế cho :class:`MagicMock` mặc định của mock được tạo. Ví dụ, nếu bạn muốn sử dụng một :class:`NonCallableMock`::

    >>> thing = object()
    >>> with patch('__main__.thing', new_callable=NonCallableMock) as mock_thing:
    ...     assert thing is mock_thing
    ...     thing()
    ...
    Traceback (most recent call last):
      ...
    TypeError: 'NonCallableMock' object is not callable

Một trường hợp sử dụng khác có thể là thay thế một đối tượng bằng một instance :class:`io.StringIO`::

    >>> from io import StringIO
    >>> def foo():
    ...     print('Something')
    ...
    >>> @patch('sys.stdout', new_callable=StringIO)
    ... def test(mock_stdout):
    ...     foo()
    ...     assert mock_stdout.getvalue() == 'Something\n'
    ...
    >>> test()

Khi :func:`patch` tạo mock cho bạn, việc đầu tiên bạn thường cần làm là cấu hình mock. Một phần cấu hình đó có thể được thực hiện trong lời gọi patch. Mọi keyword tùy ý bạn truyền vào lời gọi sẽ được dùng để thiết lập các thuộc tính trên mock được tạo::

    >>> patcher = patch('__main__.thing', first='one', second='two')
    >>> mock_thing = patcher.start()
    >>> mock_thing.first
    'one'
    >>> mock_thing.second
    'two'

Ngoài các thuộc tính trên mock được tạo, các thuộc tính như
:attr:`~Mock.return_value` và :attr:`~Mock.side_effect` của các mock con cũng có thể được cấu hình. Về mặt cú pháp, không thể truyền trực tiếp các thuộc tính này dưới dạng keyword argument, nhưng vẫn có thể mở rộng một dictionary có các thuộc tính này làm key vào lời gọi :func:`patch` bằng cách sử dụng ``**``::

    >>> config = {'method.return_value': 3, 'other.side_effect': KeyError}
    >>> patcher = patch('__main__.thing', **config)
    >>> mock_thing = patcher.start()
    >>> mock_thing.method()
    3
    >>> mock_thing.other()
    Traceback (most recent call last):
      ...
    KeyError

Theo mặc định, việc cố gắng patch một function trong một module (hoặc một method hay một attribute trong một class) không tồn tại sẽ thất bại với :exc:`AttributeError`::

    >>> @patch('sys.non_existing_attribute', 42)
    ... def test():
    ...     assert sys.non_existing_attribute == 42
    ...
    >>> test()
    Traceback (most recent call last):
      ...
    AttributeError: <module 'sys' (built-in)> does not have the attribute 'non_existing_attribute'

nhưng thêm ``create=True`` vào lệnh gọi :func:`patch` sẽ khiến ví dụ trước hoạt động như mong đợi::

    >>> @patch('sys.non_existing_attribute', 42, create=True)
    ... def test(mock_stdout):
    ...     assert sys.non_existing_attribute == 42
    ...
    >>> test()

.. versionchanged:: 3.8

    :func:`patch` giờ đây trả về một :class:`AsyncMock` nếu target là một hàm async.


patch.object
~~~~~~~~~~~~

.. function:: patch.object(target, attribute, new=DEFAULT, spec=None, create=False, spec_set=None, autospec=None, new_callable=None, **kwargs)

    patch thành viên có tên (*attribute*) trên một đối tượng (*target*) bằng một mock object.

    :func:`patch.object` có thể được dùng làm decorator, class decorator hoặc context manager. Các đối số *new*, *spec*, *create*, *spec_set*, *autospec* và *new_callable* có cùng ý nghĩa như đối với :func:`patch`. Giống như :func:`patch`,
    :func:`patch.object` nhận các keyword argument tùy ý để cấu hình mock object mà nó tạo ra.

    Khi được dùng làm class decorator, :func:`patch.object` tuân theo ``patch.TEST_PREFIX`` để chọn các phương thức cần bọc.

Bạn có thể gọi :func:`patch.object` với ba đối số hoặc hai đối số. Dạng ba đối số nhận đối tượng cần patch, tên thuộc tính và đối tượng dùng để thay thế thuộc tính đó.

Khi gọi bằng dạng hai đối số, bạn bỏ qua đối tượng thay thế; một mock sẽ được tạo cho bạn và truyền vào hàm được trang trí dưới dạng một đối số bổ sung:

    >>> @patch.object(SomeClass, 'class_method')
    ... def test(mock_method):
    ...     SomeClass.class_method(3)
    ...     mock_method.assert_called_with(3)
    ...
    >>> test()

*spec*, *create* và các đối số khác của :func:`patch.object` có cùng ý nghĩa như trong :func:`patch`.


patch.dict
~~~~~~~~~~

.. function:: patch.dict(in_dict, values=(), clear=False, **kwargs)

    Patch một dictionary hoặc đối tượng tương tự dictionary, rồi khôi phục dictionary về trạng thái ban đầu sau khi kiểm thử; dictionary được khôi phục là bản sao của dictionary trước khi kiểm thử.

    *in_dict* có thể là một dictionary hoặc container tương tự mapping. Nếu là một mapping, nó phải hỗ trợ tối thiểu việc lấy, đặt và xóa các mục, cũng như lặp qua các khóa.

    *in_dict* cũng có thể là một chuỗi chỉ định tên của dictionary; khi đó dictionary sẽ được lấy bằng cách import.

    *các giá trị* có thể là một dictionary chứa các giá trị cần thiết lập trong dictionary. *các giá trị* cũng có thể là một iterable gồm các ``(key, value)`` cặp.

    Nếu *clear* là true thì dictionary sẽ được xóa trước khi các giá trị mới được thiết lập.

    :func:`patch.dict` cũng có thể được gọi với các keyword argument tùy ý để thiết lập các giá trị trong dictionary.

    .. versionchanged:: 3.8

        :func:`patch.dict` hiện trả về dictionary đã được patch khi được sử dụng như một context manager.

:func:`patch.dict` có thể được sử dụng như một context manager, decorator hoặc class decorator:

    >>> foo = {}
    >>> @patch.dict(foo, {'newkey': 'newvalue'})
    ... def test():
    ...     assert foo == {'newkey': 'newvalue'}
    ...
    >>> test()
    >>> assert foo == {}

Khi được sử dụng như một class decorator, :func:`patch.dict` tuân theo ``patch.TEST_PREFIX`` (mặc định là ``'test'``) để chọn các phương thức cần wrap:

    >>> import os
    >>> import unittest
    >>> from unittest.mock import patch
    >>> @patch.dict('os.environ', {'newkey': 'newvalue'})
    ... class TestSample(unittest.TestCase):
    ...     def test_sample(self):
    ...         self.assertEqual(os.environ['newkey'], 'newvalue')

Nếu bạn muốn sử dụng một prefix khác cho test của mình, bạn có thể thông báo cho các patcher về prefix khác đó bằng cách thiết lập ``patch.TEST_PREFIX``. Để biết thêm chi tiết về cách thay đổi giá trị này, hãy xem :ref:`test-prefix`.

:func:`patch.dict` có thể được dùng để thêm các phần tử vào một dictionary, hoặc đơn giản là cho phép một test thay đổi dictionary, đồng thời đảm bảo dictionary được khôi phục khi test kết thúc.

    >>> foo = {}
    >>> with patch.dict(foo, {'newkey': 'newvalue'}) as patched_foo:
    ...     assert foo == {'newkey': 'newvalue'}
    ...     assert patched_foo == {'newkey': 'newvalue'}
    ...     # Bạn có thể thêm, cập nhật hoặc xóa các key của foo (hoặc patched_foo, chúng là cùng một dict)
    ...     patched_foo['spam'] = 'eggs'
    ...
    >>> assert foo == {}
    >>> assert patched_foo == {}

    >>> import os
    >>> with patch.dict('os.environ', {'newkey': 'newvalue'}):
    ...     print(os.environ['newkey'])
    ...
    newvalue
    >>> assert 'newkey' not in os.environ

Có thể sử dụng các keyword trong lệnh gọi :func:`patch.dict` để thiết lập các giá trị trong dictionary:

    >>> mymodule = MagicMock()
    >>> mymodule.function.return_value = 'fish'
    >>> with patch.dict('sys.modules', mymodule=mymodule):
    ...     import mymodule
    ...     mymodule.function('some', 'args')
    ...
    'fish'

:func:`patch.dict` có thể được dùng với các đối tượng tương tự dictionary nhưng thực tế không phải là dictionary. Tối thiểu, chúng phải hỗ trợ việc lấy, thiết lập và xóa item, cùng với việc lặp hoặc kiểm tra thành viên. Điều này tương ứng với các magic method :meth:`~object.__getitem__`, :meth:`~object.__setitem__`,
:meth:`~object.__delitem__` và một trong hai :meth:`~container.__iter__` hoặc
:meth:`~object.__contains__`.

    >>> class Container:
    ...     def __init__(self):
    ...         self.values = {}
    ...     def __getitem__(self, name):
    ...         return self.values[name]
    ...     def __setitem__(self, name, value):
    ...         self.values[name] = value
    ...     def __delitem__(self, name):
    ...         del self.values[name]
    ...     def __iter__(self):
    ...         return iter(self.values)
    ...
    >>> thing = Container()
    >>> thing['one'] = 1
    >>> with patch.dict(thing, one=2, two=3):
    ...     assert thing['one'] == 2
    ...     assert thing['two'] == 3
    ...
    >>> assert thing['one'] == 1
    >>> assert list(thing) == ['one']


patch.multiple
~~~~~~~~~~~~~~

.. function:: patch.multiple(target, spec=None, create=False, spec_set=None, autospec=None, new_callable=None, **kwargs)

    Thực hiện nhiều bản patch trong một lần gọi. Nó nhận đối tượng cần patch (dưới dạng đối tượng hoặc chuỗi để lấy đối tượng bằng cách import) và các keyword argument cho những bản patch::

        with patch.multiple(settings, FIRST_PATCH='one', SECOND_PATCH='two'):
            ...

    Sử dụng :data:`DEFAULT` làm giá trị nếu bạn muốn :func:`patch.multiple` tạo mock cho mình. Trong trường hợp này, các mock được tạo sẽ được truyền vào hàm đã được trang trí bằng keyword, và một dictionary sẽ được trả về khi :func:`patch.multiple` được sử dụng làm context manager.

    :func:`patch.multiple` có thể được sử dụng làm decorator, class decorator hoặc context manager. Các đối số *spec*, *spec_set*, *create*, *autospec* và *new_callable* có cùng ý nghĩa như đối với :func:`patch`. Các đối số này sẽ được áp dụng cho *all* patch được thực hiện bởi :func:`patch.multiple`.

    Khi được sử dụng làm class decorator, :func:`patch.multiple` tuân theo ``patch.TEST_PREFIX`` để chọn các phương thức cần bọc.

Nếu bạn muốn :func:`patch.multiple` tạo mock cho mình, bạn có thể sử dụng
:data:`DEFAULT` làm giá trị. Nếu bạn sử dụng :func:`patch.multiple` làm decorator, các mock được tạo sẽ được truyền vào hàm đã được trang trí bằng keyword.::

    >>> thing = object()
    >>> other = object()

    >>> @patch.multiple('__main__', thing=DEFAULT, other=DEFAULT)
    ... def test_function(thing, other):
    ...     assert isinstance(thing, MagicMock)
    ...     assert isinstance(other, MagicMock)
    ...
    >>> test_function()

:func:`patch.multiple` có thể được lồng với các decorator ``patch`` khác, nhưng hãy đặt các đối số được truyền bằng keyword *after* sau bất kỳ đối số tiêu chuẩn nào được tạo bởi :func:`patch`::

    >>> @patch('sys.exit')
    ... @patch.multiple('__main__', thing=DEFAULT, other=DEFAULT)
    ... def test_function(mock_exit, other, thing):
    ...     assert 'other' in repr(other)
    ...     assert 'thing' in repr(thing)
    ...     assert 'exit' in repr(mock_exit)
    ...
    >>> test_function()

Nếu :func:`patch.multiple` được sử dụng làm context manager, giá trị do context manager trả về là một dictionary trong đó các mock được tạo được lập chỉ mục theo tên::

    >>> with patch.multiple('__main__', thing=DEFAULT, other=DEFAULT) as values:
    ...     assert 'other' in repr(values['other'])
    ...     assert 'thing' in repr(values['thing'])
    ...     assert values['thing'] is thing
    ...     assert values['other'] is other
    ...


.. _start-and-stop:

các phương thức patch: start và stop
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tất cả các patcher đều có các phương thức :meth:`!start` và :meth:`!stop`. Các phương thức này giúp việc patch trong các phương thức ``setUp`` hoặc khi bạn muốn thực hiện nhiều patch mà không phải lồng các decorator hoặc các câu lệnh with trở nên đơn giản hơn.

Để sử dụng, hãy gọi :func:`patch`, :func:`patch.object` hoặc :func:`patch.dict` như bình thường và giữ một tham chiếu đến đối tượng ``patcher`` được trả về. Sau đó, bạn có thể gọi :meth:`!start` để áp dụng patch và :meth:`!stop` để hoàn tác.

Nếu bạn sử dụng :func:`patch` để tạo một mock thì mock đó sẽ được trả về bởi lệnh gọi đến ``patcher.start``.::

    >>> patcher = patch('package.module.ClassName')
    >>> from package import module
    >>> original = module.ClassName
    >>> new_mock = patcher.start()
    >>> assert module.ClassName is not original
    >>> assert module.ClassName is new_mock
    >>> patcher.stop()
    >>> assert module.ClassName is original
    >>> assert module.ClassName is not new_mock


Một trường hợp sử dụng điển hình là thực hiện nhiều patch trong phương thức ``setUp`` của một :class:`~unittest.TestCase`::

    >>> class MyTest(unittest.TestCase):
    ...     def setUp(self):
    ...         self.patcher1 = patch('package.module.Class1')
    ...         self.patcher2 = patch('package.module.Class2')
    ...         self.MockClass1 = self.patcher1.start()
    ...         self.MockClass2 = self.patcher2.start()
    ...
    ...     def tearDown(self):
    ...         self.patcher1.stop()
    ...         self.patcher2.stop()
    ...
    ...     def test_something(self):
    ...         assert package.module.Class1 is self.MockClass1
    ...         assert package.module.Class2 is self.MockClass2
    ...
    >>> MyTest('test_something').run()

.. caution::

    Nếu sử dụng kỹ thuật này, bạn phải đảm bảo patch được "hoàn tác" bằng cách gọi ``stop``. Việc này có thể phức tạp hơn bạn nghĩ, vì nếu một exception được phát sinh trong ``setUp`` thì ``tearDown`` sẽ không được gọi.
    :meth:`unittest.TestCase.addCleanup` giúp việc này dễ dàng hơn::

        >>> class MyTest(unittest.TestCase):
        ...     def setUp(self):
        ...         patcher = patch('package.module.Class')
        ...         self.MockClass = patcher.start()
        ...         self.addCleanup(patcher.stop)
        ...
        ...     def test_something(self):
        ...         assert package.module.Class is self.MockClass
        ...

    Ngoài ra, bạn không còn cần giữ tham chiếu đến đối tượng ``patcher`` nữa.

Bạn cũng có thể dừng tất cả các patch đã được khởi động bằng cách sử dụng
:func:`patch.stopall`.

.. function:: patch.stopall

    Dừng tất cả các patch đang hoạt động. Chỉ dừng những patch được khởi động bằng ``start``.


.. _patch-builtins:

patch builtins
~~~~~~~~~~~~~~
Bạn có thể patch bất kỳ builtins nào trong một module. Ví dụ sau đây patch builtin :func:`ord`::

    >>> @patch('__main__.ord')
    ... def test(mock_ord):
    ...     mock_ord.return_value = 101
    ...     print(ord('c'))
    ...
    >>> test()
    101


.. _test-prefix:

TEST_PREFIX
~~~~~~~~~~~

Tất cả patcher đều có thể được sử dụng làm class decorator. Khi được sử dụng theo cách này, chúng bọc mọi phương thức kiểm thử trong class. Các patcher nhận diện những phương thức bắt đầu bằng ``'test'`` là phương thức kiểm thử. Đây cũng là cách mà
:class:`unittest.TestLoader` mặc định tìm các phương thức kiểm thử.

Có thể bạn muốn sử dụng một tiền tố khác cho các bài kiểm thử của mình. Bạn có thể thông báo cho patcher về tiền tố khác này bằng cách đặt ``patch.TEST_PREFIX``::

    >>> patch.TEST_PREFIX = 'foo'
    >>> value = 3
    >>>
    >>> @patch('__main__.value', 'not three')
    ... class Thing:
    ...     def foo_one(self):
    ...         print(value)
    ...     def foo_two(self):
    ...         print(value)
    ...
    >>>
    >>> Thing().foo_one()
    not three
    >>> Thing().foo_two()
    not three
    >>> value
    3


Lồng ghép các patch decorator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Nếu muốn thực hiện nhiều bản patch, bạn chỉ cần xếp chồng các decorator lên nhau.

Bạn có thể xếp chồng nhiều patch decorator bằng mẫu sau:

    >>> @patch.object(SomeClass, 'class_method')
    ... @patch.object(SomeClass, 'static_method')
    ... def test(mock1, mock2):
    ...     assert SomeClass.static_method is mock1
    ...     assert SomeClass.class_method is mock2
    ...     SomeClass.static_method('foo')
    ...     SomeClass.class_method('bar')
    ...     return mock1, mock2
    ...
    >>> mock1, mock2 = test()
    >>> mock1.assert_called_once_with('foo')
    >>> mock2.assert_called_once_with('bar')


Lưu ý rằng các decorator được áp dụng từ dưới lên trên. Đây là cách Python áp dụng decorator theo tiêu chuẩn. Thứ tự của các mock được tạo và truyền vào hàm kiểm thử của bạn khớp với thứ tự này.


.. _where-to-patch:

.. _`Where to patch`:

Vị trí cần patch
~~~~~~~~~~~~~~~~

:func:`patch` hoạt động bằng cách (tạm thời) thay đổi đối tượng mà *name* trỏ tới thành một đối tượng khác. Có thể có nhiều name trỏ tới cùng một đối tượng, vì vậy để patch hoạt động, bạn phải đảm bảo rằng mình patch name được hệ thống đang kiểm thử sử dụng.

Nguyên tắc cơ bản là bạn patch tại nơi một đối tượng được *tra cứu*, nơi này không nhất thiết giống với nơi đối tượng được định nghĩa. Một vài ví dụ sẽ giúp làm rõ điều này.

Hãy tưởng tượng chúng ta có một project muốn kiểm thử với cấu trúc sau::

    a.py
        -> Defines SomeClass

    b.py
        -> from a import SomeClass
        -> some_function instantiates SomeClass

Bây giờ chúng ta muốn kiểm thử ``some_function`` nhưng muốn mock ``SomeClass`` bằng cách sử dụng
:func:`patch`. Vấn đề là khi import module b, việc chúng ta sẽ phải làm vì module này import ``SomeClass`` từ module a. Nếu sử dụng :func:`patch` để mock ``a.SomeClass``, việc đó sẽ không có tác dụng với bài kiểm thử của chúng ta; module b đã có một tham chiếu tới *thực* ``SomeClass`` và có vẻ như việc patch của chúng ta không có tác dụng.

Điểm mấu chốt là patch ``SomeClass`` tại nơi nó được sử dụng (hoặc nơi nó được tra cứu). Trong trường hợp này, ``some_function`` thực sự sẽ tra cứu ``SomeClass`` trong module b, nơi chúng ta đã import nó. Việc patch nên được thực hiện như sau::

    @patch('b.SomeClass')

Tuy nhiên, hãy xem xét kịch bản thay thế, trong đó thay vì ``from a import SomeClass``, module b thực hiện ``import a`` và ``some_function`` sử dụng ``a.SomeClass``. Cả hai dạng import này đều phổ biến. Trong trường hợp này, class chúng ta muốn patch được tra cứu trong module, vì vậy thay vào đó chúng ta phải patch ``a.SomeClass``::

    @patch('a.SomeClass')


Patching Descriptor và Proxy Object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cả patch_ và patch.object_ đều patch và khôi phục descriptor chính xác: class method, static method và property. Bạn nên patch các đối tượng này trên *class* thay vì trên một instance. Chúng cũng hoạt động với *some* object proxy quyền truy cập thuộc tính, chẳng hạn như `django settings object <https://web.archive.org/web/20200603181648/http://www.voidspace.org.uk/python/weblog/arch_d7_2010_12_04.shtml#e1198>`_.


Hỗ trợ MagicMock và magic method
--------------------------------

.. _magic-methods:

Mock Magic Method
~~~~~~~~~~~~~~~~~

:class:`Mock` hỗ trợ mock các phương thức protocol của Python, còn được gọi là
:term:`"magic method" <magic method>`. Điều này cho phép các mock object thay thế container hoặc các object khác triển khai protocol của Python.

Vì magic method được tra cứu khác với method thông thường [#]_, nên tính năng hỗ trợ này được triển khai đặc biệt. Điều này có nghĩa là chỉ một số magic method cụ thể được hỗ trợ. Danh sách được hỗ trợ bao gồm *almost* tất cả các magic method. Nếu có phương thức nào còn thiếu mà bạn cần, vui lòng cho chúng tôi biết.

Bạn mock các magic method bằng cách gán method mà bạn quan tâm cho một function hoặc một mock instance. Nếu sử dụng function thì function đó *must* nhận ``self`` làm đối số đầu tiên [#]_.

   >>> def __str__(self):
   ...     return 'fooble'
   ...
   >>> mock = Mock()
   >>> mock.__str__ = __str__
   >>> str(mock)
   'fooble'

   >>> mock = Mock()
   >>> mock.__str__ = Mock()
   >>> mock.__str__.return_value = 'fooble'
   >>> str(mock)
   'fooble'

   >>> mock = Mock()
   >>> mock.__iter__ = Mock(return_value=iter([]))
   >>> list(mock)
   []

Một trường hợp sử dụng của việc này là mock các object được dùng làm context manager trong một
:keyword:`with` câu lệnh:

   >>> mock = Mock()
   >>> mock.__enter__ = Mock(return_value='foo')
   >>> mock.__exit__ = Mock(return_value=False)
   >>> with mock as m:
   ...     assert m == 'foo'
   ...
   >>> mock.__enter__.assert_called_with()
   >>> mock.__exit__.assert_called_with(None, None, None)

Các lời gọi đến magic method không xuất hiện trong :attr:`~Mock.method_calls`, nhưng được ghi lại trong :attr:`~Mock.mock_calls`.

.. note::

   Nếu sử dụng đối số từ khóa *spec* để tạo mock, việc cố gắng thiết lập một magic method không có trong spec sẽ gây ra :exc:`AttributeError`.

Danh sách đầy đủ các magic method được hỗ trợ là:

* ``__hash__``, ``__sizeof__``, ``__repr__`` và ``__str__``
* ``__dir__``, ``__format__`` và ``__subclasses__``
* ``__round__``, ``__floor__``, ``__trunc__`` và ``__ceil__``
* Các phép so sánh: ``__lt__``, ``__gt__``, ``__le__``, ``__ge__``, ``__eq__`` và ``__ne__``
* Các phương thức container: ``__getitem__``, ``__setitem__``, ``__delitem__``, ``__contains__``, ``__len__``, ``__iter__``, ``__reversed__`` và ``__missing__``
* Trình quản lý ngữ cảnh: ``__enter__``, ``__exit__``, ``__aenter__`` và ``__aexit__``
* Các phương thức số một ngôi: ``__neg__``, ``__pos__`` và ``__invert__``
* Các phương thức số (bao gồm các biến thể right hand và in-place): ``__add__``, ``__sub__``, ``__mul__``, ``__matmul__``, ``__truediv__``, ``__floordiv__``, ``__mod__``, ``__divmod__``, ``__lshift__``, ``__rshift__``, ``__and__``, ``__xor__``, ``__or__`` và ``__pow__``
* Các phương thức chuyển đổi số: ``__complex__``, ``__int__``, ``__float__`` và ``__index__``
* Các phương thức descriptor: ``__get__``, ``__set__`` và ``__delete__``
* Pickling: ``__reduce__``, ``__reduce_ex__``, ``__getinitargs__``, ``__getnewargs__``, ``__getstate__`` và ``__setstate__``
* Biểu diễn đường dẫn hệ thống tệp: ``__fspath__``
* Các phương thức lặp bất đồng bộ: ``__aiter__`` và ``__anext__``

.. versionchanged:: 3.8
   Đã thêm hỗ trợ cho :func:`os.PathLike.__fspath__`.

.. versionchanged:: 3.8
   Đã thêm hỗ trợ cho ``__aenter__``, ``__aexit__``, ``__aiter__`` và ``__anext__``.


Các phương thức sau tồn tại nhưng *không* được hỗ trợ vì chúng đang được mock sử dụng, không thể thiết lập một cách động hoặc có thể gây ra sự cố:

* ``__getattr__``, ``__setattr__``, ``__init__`` và ``__new__``
* ``__prepare__``, ``__instancecheck__``, ``__subclasscheck__``, ``__del__``



Magic Mock
~~~~~~~~~~

Có hai biến thể ``MagicMock``: :class:`MagicMock` và :class:`NonCallableMagicMock`.


.. class:: MagicMock(*args, **kw)

   ``MagicMock`` là một lớp con của :class:`Mock`, cung cấp các triển khai mặc định cho hầu hết :term:`magic methods <magic method>`. Bạn có thể sử dụng ``MagicMock`` mà không cần tự cấu hình các magic methods.

   Các tham số của hàm khởi tạo có ý nghĩa giống như đối với :class:`Mock`.

   Nếu bạn sử dụng các đối số *spec* hoặc *spec_set* thì *chỉ* các magic methods tồn tại trong spec mới được tạo.


.. class:: NonCallableMagicMock(*args, **kw)

    Phiên bản không thể gọi của :class:`MagicMock`.

    Các tham số của hàm khởi tạo có cùng ý nghĩa như đối với
    :class:`MagicMock`, ngoại trừ *return_value* và *side_effect* không có ý nghĩa đối với mock không thể gọi.

Các magic method được thiết lập bằng các đối tượng :class:`MagicMock`, vì vậy bạn có thể cấu hình và sử dụng chúng theo cách thông thường:

   >>> mock = MagicMock()
   >>> mock[3] = 'fish'
   >>> mock.__setitem__.assert_called_with(3, 'fish')
   >>> mock.__getitem__.return_value = 'result'
   >>> mock[2]
   'result'

Theo mặc định, nhiều phương thức giao thức phải trả về các đối tượng thuộc một kiểu cụ thể. Các phương thức này được cấu hình sẵn với một giá trị trả về mặc định, để bạn có thể sử dụng chúng mà không cần làm gì nếu không quan tâm đến giá trị trả về. Bạn vẫn có thể *set* giá trị trả về theo cách thủ công nếu muốn thay đổi giá trị mặc định.

Các phương thức và giá trị mặc định của chúng:

* ``__lt__``: :data:`NotImplemented`
* ``__gt__``: :data:`!NotImplemented`
* ``__le__``: :data:`!NotImplemented`
* ``__ge__``: :data:`!NotImplemented`
* ``__int__``: ``1``
* ``__contains__``: ``False``
* ``__len__``: ``0``
* ``__iter__``: ``iter([])``
* ``__exit__``: ``False``
* ``__aexit__``: ``False``
* ``__complex__``: ``1j``
* ``__float__``: ``1.0``
* ``__bool__``: ``True``
* ``__index__``: ``1``
* ``__hash__``: mã băm mặc định cho mock
* ``__str__``: str mặc định cho mock
* ``__sizeof__``: sizeof mặc định cho mock

Ví dụ:

   >>> mock = MagicMock()
   >>> int(mock)
   1
   >>> len(mock)
   0
   >>> list(mock)
   []
   >>> object() in mock
   False

Hai phương thức so sánh bằng, :meth:`!__eq__` và :meth:`!__ne__`, là các phương thức đặc biệt. Theo mặc định, chúng thực hiện phép so sánh bằng dựa trên identity, sử dụng
thuộc tính :attr:`~Mock.side_effect`, trừ khi bạn thay đổi giá trị trả về của chúng để trả về một giá trị khác::

   >>> MagicMock() == 3
   False
   >>> MagicMock() != 3
   True
   >>> mock = MagicMock()
   >>> mock.__eq__.return_value = True
   >>> mock == 3
   True

Giá trị trả về của :meth:`!__iter__` có thể là bất kỳ đối tượng iterable nào và không bắt buộc phải là một iterator:

   >>> mock = MagicMock()
   >>> mock.__iter__.return_value = ['a', 'b', 'c']
   >>> list(mock)
   ['a', 'b', 'c']
   >>> list(mock)
   ['a', 'b', 'c']

Nếu giá trị trả về *is* một iterator, thì việc lặp qua nó một lần sẽ tiêu thụ nó và các lần lặp tiếp theo sẽ cho ra một danh sách rỗng:

   >>> mock.__iter__.return_value = iter(['a', 'b', 'c'])
   >>> list(mock)
   ['a', 'b', 'c']
   >>> list(mock)
   []

``MagicMock`` đã được cấu hình với tất cả các magic method được hỗ trợ, ngoại trừ một số phương thức tối nghĩa và lỗi thời. Bạn vẫn có thể thiết lập chúng nếu muốn.

Các magic method được hỗ trợ nhưng không được thiết lập mặc định trong ``MagicMock`` là:

* ``__subclasses__``
* ``__dir__``
* ``__format__``
* ``__get__``, ``__set__`` và ``__delete__``
* ``__reversed__`` và ``__missing__``
* ``__reduce__``, ``__reduce_ex__``, ``__getinitargs__``, ``__getnewargs__``, ``__getstate__`` và ``__setstate__``
* ``__getformat__``



.. [#] Các magic method *nên* được tra cứu trên class thay vì instance. Các phiên bản Python khác nhau không nhất quán trong việc áp dụng quy tắc này. Các phương thức protocol được hỗ trợ sẽ hoạt động với mọi phiên bản Python được hỗ trợ.
.. [#] Về cơ bản, hàm được liên kết với class, nhưng mỗi instance ``Mock`` được giữ tách biệt với các instance khác.


Các hàm trợ giúp
----------------

sentinel
~~~~~~~~

.. data:: sentinel

   Đối tượng ``sentinel`` cung cấp một cách thuận tiện để tạo các đối tượng duy nhất cho các bài kiểm thử của bạn.

   Các thuộc tính được tạo theo yêu cầu khi bạn truy cập chúng bằng tên. Việc truy cập cùng một thuộc tính sẽ luôn trả về cùng một đối tượng. Các đối tượng được trả về có biểu diễn repr hợp lý, nhờ đó thông báo lỗi kiểm thử dễ đọc.

   .. versionchanged:: 3.7
      Các thuộc tính ``sentinel`` giờ đây bảo toàn danh tính của chúng khi được
      :mod:`copied <copy>` hoặc :mod:`pickled <pickle>`.

Đôi khi, khi kiểm thử, bạn cần kiểm tra rằng một đối tượng cụ thể được truyền làm đối số cho một phương thức khác hoặc được trả về. Việc tạo các đối tượng sentinel có tên để kiểm thử điều này là khá phổ biến. :data:`sentinel` cung cấp một cách thuận tiện để tạo và kiểm tra danh tính của các đối tượng như vậy.

Trong ví dụ này, chúng ta monkey patch ``method`` để trả về ``sentinel.some_object``:

    >>> real = ProductionClass()
    >>> real.method = Mock(name="method")
    >>> real.method.return_value = sentinel.some_object
    >>> result = real.method()
    >>> assert result is sentinel.some_object
    >>> result
    sentinel.some_object


DEFAULT
~~~~~~~


.. data:: DEFAULT

    Đối tượng :data:`DEFAULT` là một sentinel được tạo sẵn (thực ra là ``sentinel.DEFAULT``). Nó có thể được các hàm :attr:`~Mock.side_effect` sử dụng để cho biết rằng nên dùng giá trị trả về thông thường.


call
~~~~

.. function:: call(*args, **kwargs)

    :func:`call` là một đối tượng trợ giúp để tạo các phép kiểm tra đơn giản hơn, dùng để so sánh với
    :attr:`~Mock.call_args`, :attr:`~Mock.call_args_list`,
    :attr:`~Mock.mock_calls` và :attr:`~Mock.method_calls`. :func:`call` cũng có thể được sử dụng với :meth:`~Mock.assert_has_calls`.

        >>> m = MagicMock(return_value=None)
        >>> m(1, 2, a='foo', b='bar')
        >>> m()
        >>> m.call_args_list == [call(1, 2, a='foo', b='bar'), call()]
        True

.. method:: call.call_list()

    Đối với một đối tượng call biểu diễn nhiều lần gọi, :meth:`call_list` trả về danh sách gồm tất cả các lần gọi trung gian cũng như lần gọi cuối cùng.

``call_list`` đặc biệt hữu ích khi thực hiện các assertion trên "lệnh gọi nối tiếp". Một lệnh gọi nối tiếp là nhiều lệnh gọi trên cùng một dòng mã. Điều này tạo ra nhiều mục trong :attr:`~Mock.mock_calls` trên một mock. Việc tự xây dựng chuỗi lệnh gọi có thể khá tẻ nhạt.

:meth:`~call.call_list` có thể xây dựng chuỗi lệnh gọi từ cùng một lệnh gọi nối tiếp:

    >>> m = MagicMock()
    >>> m(1).method(arg='foo').other('bar')(2.0)
    <MagicMock name='mock().method().other()()' id='...'>
    >>> kall = call(1).method(arg='foo').other('bar')(2.0)
    >>> kall.call_list()
    [call(1),
     call().method(arg='foo'),
     call().method().other('bar'),
     call().method().other()(2.0)]
    >>> m.mock_calls == kall.call_list()
    True

.. _calls-as-tuples:

Một đối tượng ``call`` là một tuple gồm (đối số vị trí, đối số từ khóa) hoặc (tên, đối số vị trí, đối số từ khóa), tùy thuộc vào cách đối tượng được tạo. Khi tự tạo chúng, điều này không quá đáng chú ý, nhưng các đối tượng ``call`` nằm trong :attr:`Mock.call_args`, :attr:`Mock.call_args_list` và
các thuộc tính :attr:`Mock.mock_calls` có thể được introspect để truy cập từng đối số mà chúng chứa.

Các đối tượng ``call`` trong :attr:`Mock.call_args` và :attr:`Mock.call_args_list` là các bộ hai phần tử gồm (đối số vị trí, đối số từ khóa), trong khi các đối tượng ``call`` trong :attr:`Mock.mock_calls`, cùng với những đối tượng bạn tự tạo, là các bộ ba phần tử gồm (tên, đối số vị trí, đối số từ khóa).

Bạn có thể sử dụng "tính chất tuple" của chúng để lấy ra từng đối số nhằm thực hiện introspection và assertion phức tạp hơn. Các đối số vị trí là một tuple (tuple rỗng nếu không có đối số vị trí), còn các đối số từ khóa là một dictionary:

    >>> m = MagicMock(return_value=None)
    >>> m(1, 2, 3, arg='one', arg2='two')
    >>> kall = m.call_args
    >>> kall.args
    (1, 2, 3)
    >>> kall.kwargs
    {'arg': 'one', 'arg2': 'two'}
    >>> kall.args is kall[0]
    True
    >>> kall.kwargs is kall[1]
    True

    >>> m = MagicMock()
    >>> m.foo(4, 5, 6, arg='two', arg2='three')
    <MagicMock name='mock.foo()' id='...'>
    >>> kall = m.mock_calls[0]
    >>> name, args, kwargs = kall
    >>> name
    'foo'
    >>> args
    (4, 5, 6)
    >>> kwargs
    {'arg': 'two', 'arg2': 'three'}
    >>> name is m.mock_calls[0][0]
    True


create_autospec
~~~~~~~~~~~~~~~

.. function:: create_autospec(spec, spec_set=False, instance=False, **kwargs)

    Tạo một đối tượng mock bằng cách sử dụng một đối tượng khác làm spec. Các thuộc tính trên mock sẽ sử dụng thuộc tính tương ứng trên đối tượng *spec* làm spec.

    Các function hoặc method được mock sẽ được kiểm tra các đối số để đảm bảo rằng chúng được gọi với signature chính xác.

    Nếu *spec_set* là ``True`` thì việc cố gắng đặt các thuộc tính không tồn tại trên đối tượng spec sẽ phát sinh :exc:`AttributeError`.

    Nếu một class được sử dụng làm spec thì giá trị trả về của mock (instance của class) sẽ có cùng spec. Bạn có thể sử dụng một class làm spec cho một đối tượng instance bằng cách truyền ``instance=True``. Mock được trả về sẽ chỉ có thể được gọi nếu các instance của mock có thể gọi được.

    :func:`create_autospec` cũng nhận các đối số keyword tùy ý được truyền đến constructor của mock được tạo.

Xem :ref:`auto-speccing` để biết các ví dụ về cách sử dụng auto-speccing với
:func:`create_autospec` và đối số *autospec* của :func:`patch`.


.. versionchanged:: 3.8

    :func:`create_autospec` hiện trả về một :class:`AsyncMock` nếu target là một async function.


ANY
~~~

.. data:: ANY

Đôi khi bạn có thể cần đưa ra các assertion về *một số* đối số trong một lần gọi đến mock, nhưng либо không quan tâm đến một số đối số, hoặc muốn lấy riêng từng đối số từ :attr:`~Mock.call_args` và đưa ra các assertion phức tạp hơn cho chúng.

Để bỏ qua một số đối số nhất định, bạn có thể truyền vào các object so sánh bằng với *mọi thứ*. Các lần gọi đến :meth:`~Mock.assert_called_with` và
:meth:`~Mock.assert_called_once_with` sau đó sẽ thành công bất kể giá trị được truyền vào là gì.

    >>> mock = Mock(return_value=None)
    >>> mock('foo', bar=object())
    >>> mock.assert_called_once_with('foo', bar=ANY)

:data:`ANY` cũng có thể được sử dụng để so sánh với các danh sách call như
:attr:`~Mock.mock_calls`:

    >>> m = MagicMock(return_value=None)
    >>> m(1)
    >>> m(1, 2)
    >>> m(object())
    >>> m.mock_calls == [call(1), call(1, 2), ANY]
    True

:data:`ANY` không bị giới hạn trong việc so sánh với các object call, vì vậy cũng có thể được sử dụng trong các assertion kiểm thử::

    class TestStringMethods(unittest.TestCase):

        def test_split(self):
            s = 'hello world'
            self.assertEqual(s.split(), ['hello', ANY])


FILTER_DIR
~~~~~~~~~~

.. data:: FILTER_DIR

:data:`FILTER_DIR` là một biến cấp mô-đun kiểm soát cách các mock object phản hồi với :func:`dir`. Giá trị mặc định là ``True``, sử dụng cơ chế lọc được mô tả dưới đây để chỉ hiển thị các thành phần hữu ích. Nếu bạn không thích cơ chế lọc này hoặc cần tắt nó cho mục đích chẩn đoán, hãy đặt ``mock.FILTER_DIR = False``.

Khi bật tính năng lọc, ``dir(some_mock)`` chỉ hiển thị các thuộc tính hữu ích và sẽ bao gồm mọi thuộc tính được tạo động vốn thường không được hiển thị. Nếu mock được tạo bằng *spec* (hoặc tất nhiên là *autospec*), thì tất cả thuộc tính từ đối tượng gốc đều được hiển thị, ngay cả khi chúng chưa được truy cập:

.. doctest::
    :options: +ELLIPSIS,+NORMALIZE_WHITESPACE

    >>> dir(Mock())
    ['assert_any_call',
     'assert_called',
     'assert_called_once',
     'assert_called_once_with',
     'assert_called_with',
     'assert_has_calls',
     'assert_not_called',
     'attach_mock',
     ...
    >>> from urllib import request
    >>> dir(Mock(spec=request))
    ['AbstractBasicAuthHandler',
     'AbstractDigestAuthHandler',
     'AbstractHTTPHandler',
     'BaseHandler',
     ...

Nhiều thuộc tính bắt đầu bằng dấu gạch dưới và hai dấu gạch dưới không thực sự hữu ích (là thuộc tính private của :class:`Mock` thay vì của đối tượng đang được mock) đã được lọc khỏi kết quả gọi :func:`dir` trên một :class:`Mock`. Nếu bạn không thích hành vi này, bạn có thể tắt nó bằng cách đặt công tắc cấp mô-đun
:data:`FILTER_DIR`:

.. doctest::
    :options: +ELLIPSIS,+NORMALIZE_WHITESPACE

    >>> from unittest import mock
    >>> mock.FILTER_DIR = False
    >>> dir(mock.Mock())
    ['_NonCallableMock__get_return_value',
     '_NonCallableMock__get_side_effect',
     '_NonCallableMock__return_value_doc',
     '_NonCallableMock__set_return_value',
     '_NonCallableMock__set_side_effect',
     '__call__',
     '__class__',
     ...

Ngoài ra, bạn chỉ cần sử dụng ``vars(my_mock)`` (các thành viên của instance) và ``dir(type(my_mock))`` (các thành viên của type) để bỏ qua cơ chế lọc, bất kể
:const:`FILTER_DIR`.


mock_open
~~~~~~~~~

.. function:: mock_open(mock=None, read_data='')

   Một hàm trợ giúp để tạo một mock thay thế việc sử dụng :func:`open`. Hàm này hoạt động khi :func:`open` được gọi trực tiếp hoặc được sử dụng như một context manager.

   Đối số *mock* là đối tượng mock cần cấu hình. Nếu ``None`` (giá trị mặc định), một :class:`MagicMock` sẽ được tạo cho bạn, với API chỉ giới hạn ở các phương thức hoặc thuộc tính có trên các file handle tiêu chuẩn.

   *read_data* là một chuỗi để các phương thức :meth:`~io.RawIOBase.read` trả về,
   :meth:`~io.IOBase.readline`, và :meth:`~io.IOBase.readlines` của file handle. Các lần gọi những phương thức đó sẽ lấy dữ liệu từ *read_data* cho đến khi dữ liệu được dùng hết. Mock của các phương thức này khá đơn giản: mỗi lần *mock* được gọi, *read_data* sẽ được tua lại về đầu. Nếu cần kiểm soát nhiều hơn đối với dữ liệu cung cấp cho code được kiểm thử, bạn sẽ cần tự tùy chỉnh mock này. Khi cách đó vẫn chưa đủ, một trong các package filesystem trong bộ nhớ trên `PyPI <https://pypi.org>`_ có thể cung cấp một filesystem thực tế để kiểm thử.

   .. versionchanged:: 3.4
      Đã bổ sung hỗ trợ :meth:`~io.IOBase.readline` và :meth:`~io.IOBase.readlines`. Mock của :meth:`~io.RawIOBase.read` đã được thay đổi để dùng hết *read_data* thay vì trả về dữ liệu đó trong mỗi lần gọi.

   .. versionchanged:: 3.5
      *read_data* hiện được đặt lại sau mỗi lần gọi *mock*.

   .. versionchanged:: 3.8
      Đã bổ sung :meth:`~container.__iter__` vào phần triển khai để phép lặp (chẳng hạn như trong vòng lặp for) sử dụng hết *read_data* một cách chính xác.

Sử dụng :func:`open` làm context manager là một cách tuyệt vời để bảo đảm các file handle của bạn được đóng đúng cách và đang trở nên phổ biến::

    with open('/some/path', 'w') as f:
        f.write('something')

Vấn đề là ngay cả khi bạn mock lời gọi đến :func:`open` thì chính *đối tượng được trả về* mới được dùng làm context manager (và có :meth:`~object.__enter__` và
:meth:`~object.__exit__` được gọi).

Việc mock các context manager bằng một :class:`MagicMock` đủ phổ biến và đủ rắc rối để một hàm trợ giúp trở nên hữu ích.::

    >>> m = mock_open()
    >>> with patch('__main__.open', m):
    ...     with open('foo', 'w') as h:
    ...         h.write('some stuff')
    ...
    >>> m.mock_calls
    [call('foo', 'w'),
     call().__enter__(),
     call().write('some stuff'),
     call().__exit__(None, None, None)]
    >>> m.assert_called_once_with('foo', 'w')
    >>> handle = m()
    >>> handle.write.assert_called_once_with('some stuff')

Và để đọc tệp::

    >>> with patch('__main__.open', mock_open(read_data='bibble')) as m:
    ...     with open('foo') as h:
    ...         result = h.read()
    ...
    >>> m.assert_called_once_with('foo')
    >>> assert result == 'bibble'


.. _auto-speccing:

Autospeccing
~~~~~~~~~~~~

Autospeccing dựa trên tính năng :attr:`!spec` hiện có của mock. Tính năng này giới hạn API của các mock ở API của một đối tượng gốc (spec), nhưng hoạt động đệ quy (được triển khai một cách lazy), sodass các thuộc tính của mock chỉ có cùng API với các thuộc tính của spec. Ngoài ra, các hàm / phương thức được mock có cùng chữ ký lời gọi như bản gốc, vì vậy chúng sẽ raise một :exc:`TypeError` nếu được gọi không đúng cách.

Trước khi giải thích cách auto-speccing hoạt động, hãy xem vì sao nó cần thiết.

:class:`Mock` là một đối tượng rất mạnh mẽ và linh hoạt, nhưng nó mắc phải một nhược điểm phổ biến đối với việc mocking. Nếu bạn refactor một phần code, đổi tên member, v.v., mọi test cho code vẫn đang sử dụng *old api* nhưng dùng mock thay vì đối tượng thật vẫn sẽ pass. Điều này có nghĩa là tất cả test của bạn có thể pass dù code của bạn đã bị lỗi.

.. versionchanged:: 3.5

    Trước phiên bản 3.5, các test có lỗi chính tả trong từ assert sẽ âm thầm pass trong khi đáng lẽ phải phát sinh lỗi. Bạn vẫn có thể đạt được hành vi này bằng cách truyền ``unsafe=True`` cho Mock.

Lưu ý rằng đây là một lý do khác cho thấy bạn cần cả integration test lẫn unit test. Việc test mọi thứ trong isolation hoàn toàn ổn, nhưng nếu bạn không test cách các unit được "kết nối với nhau" thì vẫn còn rất nhiều chỗ cho những bug mà test có thể phát hiện.

:mod:`!unittest.mock` đã cung cấp một tính năng giúp giải quyết vấn đề này, gọi là speccing. Nếu bạn sử dụng một class hoặc instance làm :attr:`!spec` cho mock thì bạn chỉ có thể truy cập các attribute trên mock vốn tồn tại trên class thật:

    >>> from urllib import request
    >>> mock = Mock(spec=request.Request)
    >>> mock.assret_called_with  # Cố ý viết sai chính tả!
    Traceback (most recent call last):
     ...
    AttributeError: Mock object has no attribute 'assret_called_with'

spec chỉ áp dụng cho chính mock, vì vậy chúng ta vẫn gặp vấn đề tương tự với mọi method trên mock:

.. code-block:: pycon

    >>> mock.header_items()
    <mock.Mock object at 0x...>
    >>> mock.header_items.assret_called_with()  # Cố ý viết sai chính tả!

Tự động tạo spec giải quyết vấn đề này. Bạn có thể truyền ``autospec=True`` cho
:func:`patch` / :func:`patch.object` hoặc sử dụng hàm :func:`create_autospec` để tạo một mock có spec. Nếu bạn sử dụng đối số ``autospec=True`` cho :func:`patch` thì đối tượng đang được thay thế sẽ được dùng làm đối tượng spec. Vì việc tạo spec được thực hiện "lazily" (spec được tạo khi các thuộc tính trên mock được truy cập), bạn có thể dùng cách này với các đối tượng rất phức tạp hoặc lồng nhau sâu (chẳng hạn như các module import các module khác, rồi các module đó lại import các module khác) mà không gây ảnh hưởng lớn đến hiệu năng.

Dưới đây là một ví dụ về cách sử dụng::

    >>> from urllib import request
    >>> patcher = patch('__main__.request', autospec=True)
    >>> mock_request = patcher.start()
    >>> request is mock_request
    True
    >>> mock_request.Request
    <MagicMock name='request.Request' spec='Request' id='...'>

Bạn có thể thấy rằng :class:`!request.Request` có một spec. :class:`!request.Request` nhận hai đối số trong hàm khởi tạo (một trong số đó là *self*). Đây là điều xảy ra nếu chúng ta thử gọi nó không đúng cách::

    >>> req = request.Request()
    Traceback (most recent call last):
     ...
    TypeError: <lambda>() takes at least 2 arguments (1 given)

Spec cũng áp dụng cho các class đã được khởi tạo (tức là giá trị trả về của các mock có spec)::

    >>> req = request.Request('foo')
    >>> req
    <NonCallableMagicMock name='request.Request()' spec='Request' id='...'>

Các đối tượng :class:`!Request` không thể được gọi, vì vậy giá trị trả về khi khởi tạo :class:`!request.Request` đã được mock là một mock không thể gọi. Khi đã có spec, mọi lỗi đánh máy trong các câu lệnh assert của chúng ta sẽ phát sinh lỗi chính xác::

    >>> req.add_header('spam', 'eggs')
    <MagicMock name='request.Request().add_header()' id='...'>
    >>> req.add_header.assret_called_with  # Lỗi đánh máy có chủ ý!
    Traceback (most recent call last):
     ...
    AttributeError: Mock object has no attribute 'assret_called_with'
    >>> req.add_header.assert_called_with('spam', 'eggs')

Trong nhiều trường hợp, bạn chỉ cần thêm ``autospec=True`` vào các lệnh gọi hiện có
:func:`patch` rồi sẽ được bảo vệ khỏi các lỗi do gõ sai và thay đổi API.

Ngoài việc sử dụng *autospec* thông qua :func:`patch`, còn có một
:func:`create_autospec` để trực tiếp tạo các mock có autospec:

    >>> from urllib import request
    >>> mock_request = create_autospec(request)
    >>> mock_request.Request('foo', 'bar')
    <NonCallableMagicMock name='mock.Request()' spec='Request' id='...'>

Tuy nhiên, cách này không phải không có những điểm cần lưu ý và hạn chế, đó là lý do nó không phải là hành vi mặc định. Để biết những thuộc tính nào có sẵn trên đối tượng spec, autospec phải thực hiện introspection (truy cập các thuộc tính) đối với spec. Khi bạn duyệt qua các thuộc tính trên mock, việc duyệt tương ứng trên đối tượng gốc cũng đang diễn ra ngầm bên dưới. Nếu bất kỳ đối tượng nào được áp dụng spec của bạn có các property hoặc descriptor có thể kích hoạt thực thi code, bạn có thể không sử dụng được autospec. Mặt khác, tốt hơn nhiều nếu thiết kế các đối tượng sao cho việc introspection an toàn [#]_.

Một vấn đề nghiêm trọng hơn là các thuộc tính của instance thường được tạo trong phương thức :meth:`~object.__init__` và hoàn toàn không tồn tại trên class. *autospec* không thể biết về bất kỳ thuộc tính nào được tạo động và giới hạn API ở các thuộc tính hiển thị.::

    >>> class Something:
    ...   def __init__(self):
    ...     self.a = 33
    ...
    >>> with patch('__main__.Something', autospec=True):
    ...   thing = Something()
    ...   thing.a
    ...
    Traceback (most recent call last):
      ...
    AttributeError: Mock object has no attribute 'a'

Có một vài cách khác nhau để giải quyết vấn đề này. Cách dễ nhất, nhưng không nhất thiết là ít gây phiền toái nhất, là chỉ cần đặt các thuộc tính cần thiết trên mock sau khi tạo. Việc *autospec* không cho phép bạn lấy các thuộc tính không tồn tại trên spec không ngăn bạn thiết lập chúng::

    >>> with patch('__main__.Something', autospec=True):
    ...   thing = Something()
    ...   thing.a = 33
    ...

Có một phiên bản chặt chẽ hơn của cả *spec* và *autospec*, phiên bản này *does* ngăn bạn thiết lập các thuộc tính không tồn tại. Điều này hữu ích nếu bạn muốn đảm bảo mã của mình cũng chỉ *sets* các thuộc tính hợp lệ, nhưng rõ ràng nó ngăn cản tình huống cụ thể này:

    >>> with patch('__main__.Something', autospec=True, spec_set=True):
    ...   thing = Something()
    ...   thing.a = 33
    ...
    Traceback (most recent call last):
     ...
    AttributeError: Mock object has no attribute 'a'

Có lẽ cách tốt nhất để giải quyết vấn đề là thêm các thuộc tính lớp làm giá trị mặc định cho những thành viên thể hiện được khởi tạo trong :meth:`~object.__init__`. Lưu ý rằng nếu bạn chỉ thiết lập các thuộc tính mặc định trong :meth:`!__init__` thì việc cung cấp chúng thông qua các thuộc tính lớp (tất nhiên là được chia sẻ giữa các thể hiện) cũng nhanh hơn. Ví dụ:

.. code-block:: python

    class Something:
        a = 33

Điều này dẫn đến một vấn đề khác. Việc cung cấp giá trị mặc định là ``None`` cho các thành viên mà sau đó sẽ là một đối tượng thuộc kiểu khác là khá phổ biến. ``None`` sẽ vô dụng khi làm spec vì nó sẽ không cho phép bạn truy cập *any* thuộc tính hoặc phương thức nào trên đó. Vì ``None`` là *never* hữu ích khi làm spec và có lẽ biểu thị một thành viên thường sẽ thuộc một kiểu khác, autospec không sử dụng spec cho các thành viên được đặt thành ``None``. Những thành viên này sẽ chỉ là các mock thông thường (thực ra là MagicMocks):

    >>> class Something:
    ...     member = None
    ...
    >>> mock = create_autospec(Something)
    >>> mock.member.foo.bar.baz()
    <MagicMock name='mock.member.foo.bar.baz()' id='...'>

Nếu bạn không muốn sửa đổi các lớp production để thêm giá trị mặc định thì vẫn còn những lựa chọn khác. Một trong số đó là chỉ cần sử dụng một thể hiện làm spec thay vì lớp. Lựa chọn còn lại là tạo một lớp con của lớp production và thêm các giá trị mặc định vào lớp con mà không ảnh hưởng đến lớp production. Cả hai cách này đều yêu cầu bạn sử dụng một đối tượng thay thế làm spec. May mắn là :func:`patch` hỗ trợ việc này - bạn chỉ cần truyền đối tượng thay thế làm đối số *autospec*::

    >>> class Something:
    ...   def __init__(self):
    ...     self.a = 33
    ...
    >>> class SomethingForTest(Something):
    ...   a = 33
    ...
    >>> p = patch('__main__.Something', autospec=SomethingForTest)
    >>> mock = p.start()
    >>> mock.a
    <NonCallableMagicMock name='Something.a' spec='int' id='...'>


.. [#] Điều này chỉ áp dụng cho các lớp hoặc các đối tượng đã được khởi tạo. Việc gọi một lớp đã được mock để tạo một mock instance *does not* tạo ra một instance thực. Chỉ có các thao tác tra cứu thuộc tính - cùng với các lệnh gọi đến :func:`dir` - được thực hiện.

Niêm phong các mock
~~~~~~~~~~~~~~~~~~~


.. testsetup::

    from unittest.mock import seal

.. function:: seal(mock)

    Seal sẽ vô hiệu hóa việc tự động tạo mock khi truy cập một thuộc tính của mock đang được niêm phong hoặc bất kỳ thuộc tính nào của nó vốn đã là mock, theo cách đệ quy.

    Nếu một mock instance có tên hoặc spec được gán cho một thuộc tính, nó sẽ không được xem xét trong chuỗi sealing. Điều này cho phép ngăn seal cố định một phần của mock object.::

        >>> mock = Mock()
        >>> mock.submock.attribute1 = 2
        >>> mock.not_submock = mock.Mock(name="sample_name")
        >>> seal(mock)
        >>> mock.new_attribute  # Sẽ gây ra AttributeError.
        >>> mock.submock.attribute2  # Sẽ gây ra AttributeError.
        >>> mock.not_submock.attribute2  # Sẽ không gây ra lỗi.

    .. versionadded:: 3.7


Thứ tự ưu tiên của :attr:`!side_effect`, :attr:`!return_value` và *wraps*
-------------------------------------------------------------------------

Thứ tự ưu tiên của chúng là:

1. :attr:`~Mock.side_effect`
2. :attr:`~Mock.return_value`
3. *wraps*

Nếu cả ba đều được thiết lập, mock sẽ trả về giá trị từ :attr:`~Mock.side_effect`, bỏ qua :attr:`~Mock.return_value` và hoàn toàn bỏ qua object được bọc. Nếu bất kỳ hai giá trị nào được thiết lập, giá trị có mức độ ưu tiên cao hơn sẽ được trả về. Bất kể giá trị nào được thiết lập trước, thứ tự ưu tiên vẫn không thay đổi.

    >>> from unittest.mock import Mock
    >>> class Order:
    ...     @staticmethod
    ...     def get_value():
    ...         return "third"
    ...
    >>> order_mock = Mock(spec=Order, wraps=Order)
    >>> order_mock.get_value.side_effect = ["first"]
    >>> order_mock.get_value.return_value = "second"
    >>> order_mock.get_value()
    'first'

Vì ``None`` là giá trị mặc định của :attr:`~Mock.side_effect`, nếu bạn gán lại giá trị của nó thành ``None``, thứ tự ưu tiên sẽ được kiểm tra giữa
:attr:`~Mock.return_value` và object được bọc, bỏ qua
:attr:`~Mock.side_effect`.

    >>> order_mock.get_value.side_effect = None
    >>> order_mock.get_value()
    'second'

Nếu giá trị được :attr:`~Mock.side_effect` trả về là :data:`DEFAULT`, giá trị đó sẽ bị bỏ qua và thứ tự ưu tiên chuyển sang phần tử kế tiếp để lấy giá trị cần trả về.

    >>> from unittest.mock import DEFAULT
    >>> order_mock.get_value.side_effect = [DEFAULT]
    >>> order_mock.get_value()
    'second'

Khi :class:`Mock` bọc một object, giá trị mặc định của
:attr:`~Mock.return_value` sẽ là :data:`DEFAULT`.

    >>> order_mock = Mock(spec=Order, wraps=Order)
    >>> order_mock.return_value
    sentinel.DEFAULT
    >>> order_mock.get_value.return_value
    sentinel.DEFAULT

Thứ tự ưu tiên sẽ bỏ qua giá trị này và chuyển đến phần tử kế tiếp cuối cùng, tức là object được bọc.

Vì lệnh gọi thực tế được thực hiện trên đối tượng được bọc, việc tạo một instance của mock này sẽ trả về instance thực của class. Phải truyền các đối số vị trí, nếu có, mà đối tượng được bọc yêu cầu.

    >>> order_mock_instance = order_mock()
    >>> isinstance(order_mock_instance, Order)
    True
    >>> order_mock_instance.get_value()
    'third'

    >>> order_mock.get_value.return_value = DEFAULT
    >>> order_mock.get_value()
    'third'

    >>> order_mock.get_value.return_value = "second"
    >>> order_mock.get_value()
    'second'

Nhưng nếu bạn gán ``None`` cho nó thì việc này sẽ không bị bỏ qua vì đó là một phép gán tường minh. Do đó, thứ tự ưu tiên sẽ không chuyển sang đối tượng được bọc.

    >>> order_mock.get_value.return_value = None
    >>> order_mock.get_value() is None
    True

Ngay cả khi bạn đặt cả ba giá trị cùng lúc trong lúc khởi tạo mock, thứ tự ưu tiên vẫn giữ nguyên:

    >>> order_mock = Mock(spec=Order, wraps=Order,
    ...                   **{"get_value.side_effect": ["first"],
    ...                      "get_value.return_value": "second"}
    ...                   )
    ...
    >>> order_mock.get_value()
    'first'
    >>> order_mock.get_value.side_effect = None
    >>> order_mock.get_value()
    'second'
    >>> order_mock.get_value.return_value = DEFAULT
    >>> order_mock.get_value()
    'third'

Nếu :attr:`~Mock.side_effect` là :term:`exhausted`, thứ tự ưu tiên sẽ không khiến một giá trị được lấy từ các đối tượng kế tiếp. Thay vào đó, ngoại lệ ``StopIteration`` sẽ được ném ra.

    >>> order_mock = Mock(spec=Order, wraps=Order)
    >>> order_mock.get_value.side_effect = ["first side effect value",
    ...                                     "another side effect value"]
    >>> order_mock.get_value.return_value = "second"

    >>> order_mock.get_value()
    'first side effect value'
    >>> order_mock.get_value()
    'another side effect value'

    >>> order_mock.get_value()
    Traceback (most recent call last):
     ...
    StopIteration

.. _`django settings object`: https://web.archive.org/web/20200603181648/http://www.voidspace.org.uk/python/weblog/arch_d7_2010_12_04.shtml#e1198
.. _`PyPI`: https://pypi.org
