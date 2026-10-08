:mod:`!inspect` --- Kiểm tra các đối tượng đang hoạt động
=========================================================

.. testsetup:: *

   import inspect
   from inspect import *

.. module:: inspect
   :synopsis: Trích xuất thông tin và mã nguồn từ các đối tượng đang hoạt động.

.. moduleauthor:: Ka-Ping Yee <ping@lfw.org>
.. sectionauthor:: Ka-Ping Yee <ping@lfw.org>

**Mã nguồn:** :source:`Lib/inspect.py`

--------------

Mô-đun :mod:`!inspect` cung cấp một số hàm hữu ích để lấy thông tin về các đối tượng đang hoạt động như mô-đun, lớp, phương thức, hàm, traceback, đối tượng frame và đối tượng code. Ví dụ, mô-đun này có thể giúp bạn kiểm tra nội dung của một lớp, truy xuất mã nguồn của một phương thức, trích xuất và định dạng danh sách đối số cho một hàm hoặc lấy tất cả thông tin cần thiết để hiển thị một traceback chi tiết.

Mô-đun này cung cấp bốn nhóm dịch vụ chính: kiểm tra kiểu, lấy mã nguồn, kiểm tra lớp và hàm, và kiểm tra stack của trình thông dịch.


.. _inspect-types:

Kiểu và thành viên
------------------

Hàm :func:`getmembers` truy xuất các thành viên của một đối tượng như lớp hoặc mô-đun. Các hàm có tên bắt đầu bằng "is" chủ yếu được cung cấp dưới dạng các lựa chọn thuận tiện cho đối số thứ hai của :func:`getmembers`. Chúng cũng giúp bạn xác định khi nào có thể mong đợi tìm thấy các thuộc tính đặc biệt sau (xem :ref:`import-mod-attrs` để biết các thuộc tính của mô-đun):

.. this function name is too big to fit in the ascii-art table below
.. |coroutine-origin-link| replace:: :func:`sys.set_coroutine_origin_tracking_depth`

+-----------------+-------------------+---------------------------+
| Type            | Attribute         | Description               |
+=================+===================+===========================+
| class           | __doc__           | documentation string      |
+-----------------+-------------------+---------------------------+
|                 | __name__          | name with which this      |
|                 |                   | class was defined         |
+-----------------+-------------------+---------------------------+
|                 | __qualname__      | qualified name            |
+-----------------+-------------------+---------------------------+
|                 | __module__        | name of module in which   |
|                 |                   | this class was defined    |
+-----------------+-------------------+---------------------------+
|                 | __type_params__   | A tuple containing the    |
|                 |                   | :ref:`type parameters     |
|                 |                   | <type-params>` of         |
|                 |                   | a generic class           |
+-----------------+-------------------+---------------------------+
| method          | __doc__           | documentation string      |
+-----------------+-------------------+---------------------------+
|                 | __name__          | name with which this      |
|                 |                   | method was defined        |
+-----------------+-------------------+---------------------------+
|                 | __qualname__      | qualified name            |
+-----------------+-------------------+---------------------------+
|                 | __func__          | function object           |
|                 |                   | containing implementation |
|                 |                   | of method                 |
+-----------------+-------------------+---------------------------+
|                 | __self__          | instance to which this    |
|                 |                   | method is bound, or       |
|                 |                   | ``None``                  |
+-----------------+-------------------+---------------------------+
|                 | __module__        | name of module in which   |
|                 |                   | this method was defined   |
+-----------------+-------------------+---------------------------+
| function        | __doc__           | documentation string      |
+-----------------+-------------------+---------------------------+
|                 | __name__          | name with which this      |
|                 |                   | function was defined      |
+-----------------+-------------------+---------------------------+
|                 | __qualname__      | qualified name            |
+-----------------+-------------------+---------------------------+
|                 | __code__          | code object containing    |
|                 |                   | compiled function         |
|                 |                   | :term:`bytecode`          |
+-----------------+-------------------+---------------------------+
|                 | __defaults__      | tuple of any default      |
|                 |                   | values for positional or  |
|                 |                   | keyword parameters        |
+-----------------+-------------------+---------------------------+
|                 | __kwdefaults__    | mapping of any default    |
|                 |                   | values for keyword-only   |
|                 |                   | parameters                |
+-----------------+-------------------+---------------------------+
|                 | __globals__       | global namespace in which |
|                 |                   | this function was defined |
+-----------------+-------------------+---------------------------+
|                 | __builtins__      | builtins namespace        |
+-----------------+-------------------+---------------------------+
|                 | __annotations__   | mapping of parameters     |
|                 |                   | names to annotations;     |
|                 |                   | ``"return"`` key is       |
|                 |                   | reserved for return       |
|                 |                   | annotations.              |
+-----------------+-------------------+---------------------------+
|                 | __type_params__   | A tuple containing the    |
|                 |                   | :ref:`type parameters     |
|                 |                   | <type-params>` of         |
|                 |                   | a generic function        |
+-----------------+-------------------+---------------------------+
|                 | __module__        | name of module in which   |
|                 |                   | this function was defined |
+-----------------+-------------------+---------------------------+
| traceback       | tb_frame          | frame object at this      |
|                 |                   | level                     |
+-----------------+-------------------+---------------------------+
|                 | tb_lasti          | index of last attempted   |
|                 |                   | instruction in bytecode   |
+-----------------+-------------------+---------------------------+
|                 | tb_lineno         | current line number in    |
|                 |                   | Python source code        |
+-----------------+-------------------+---------------------------+
|                 | tb_next           | next inner traceback      |
|                 |                   | object (called by this    |
|                 |                   | level)                    |
+-----------------+-------------------+---------------------------+
| frame           | f_back            | next outer frame object   |
|                 |                   | (this frame's caller)     |
+-----------------+-------------------+---------------------------+
|                 | f_builtins        | builtins namespace seen   |
|                 |                   | by this frame             |
+-----------------+-------------------+---------------------------+
|                 | f_code            | code object being         |
|                 |                   | executed in this frame    |
+-----------------+-------------------+---------------------------+
|                 | f_globals         | global namespace seen by  |
|                 |                   | this frame                |
+-----------------+-------------------+---------------------------+
|                 | f_lasti           | index of last attempted   |
|                 |                   | instruction in bytecode   |
+-----------------+-------------------+---------------------------+
|                 | f_lineno          | current line number in    |
|                 |                   | Python source code        |
+-----------------+-------------------+---------------------------+
|                 | f_locals          | local namespace seen by   |
|                 |                   | this frame                |
+-----------------+-------------------+---------------------------+
|                 | f_generator       | returns the generator or  |
|                 |                   | coroutine object that     |
|                 |                   | owns this frame, or       |
|                 |                   | ``None`` if the frame is  |
|                 |                   | of a regular function     |
+-----------------+-------------------+---------------------------+
|                 | f_trace           | tracing function for this |
|                 |                   | frame, or ``None``        |
+-----------------+-------------------+---------------------------+
|                 | f_trace_lines     | indicate whether a        |
|                 |                   | tracing event is          |
|                 |                   | triggered for each source |
|                 |                   | source line               |
+-----------------+-------------------+---------------------------+
|                 | f_trace_opcodes   | indicate whether          |
|                 |                   | per-opcode events are     |
|                 |                   | requested                 |
+-----------------+-------------------+---------------------------+
|                 | clear()           | used to clear all         |
|                 |                   | references to local       |
|                 |                   | variables                 |
+-----------------+-------------------+---------------------------+
| code            | co_argcount       | number of arguments (not  |
|                 |                   | including keyword only    |
|                 |                   | arguments, \* or \*\*     |
|                 |                   | args)                     |
+-----------------+-------------------+---------------------------+
|                 | co_code           | string of raw compiled    |
|                 |                   | bytecode                  |
+-----------------+-------------------+---------------------------+
|                 | co_cellvars       | tuple of names of cell    |
|                 |                   | variables (referenced by  |
|                 |                   | containing scopes)        |
+-----------------+-------------------+---------------------------+
|                 | co_consts         | tuple of constants used   |
|                 |                   | in the bytecode           |
+-----------------+-------------------+---------------------------+
|                 | co_filename       | name of file in which     |
|                 |                   | this code object was      |
|                 |                   | created                   |
+-----------------+-------------------+---------------------------+
|                 | co_firstlineno    | number of first line in   |
|                 |                   | Python source code        |
+-----------------+-------------------+---------------------------+
|                 | co_flags          | bitmap of ``CO_*`` flags, |
|                 |                   | read more :ref:`here      |
|                 |                   | <inspect-module-co-flags>`|
+-----------------+-------------------+---------------------------+
|                 | co_lnotab         | encoded mapping of line   |
|                 |                   | numbers to bytecode       |
|                 |                   | indices                   |
+-----------------+-------------------+---------------------------+
|                 | co_freevars       | tuple of names of free    |
|                 |                   | variables (referenced via |
|                 |                   | a function's closure)     |
+-----------------+-------------------+---------------------------+
|                 | co_posonlyargcount| number of positional only |
|                 |                   | arguments                 |
+-----------------+-------------------+---------------------------+
|                 | co_kwonlyargcount | number of keyword only    |
|                 |                   | arguments (not including  |
|                 |                   | \*\* arg)                 |
+-----------------+-------------------+---------------------------+
|                 | co_name           | name with which this code |
|                 |                   | object was defined        |
+-----------------+-------------------+---------------------------+
|                 | co_qualname       | fully qualified name with |
|                 |                   | which this code object    |
|                 |                   | was defined               |
+-----------------+-------------------+---------------------------+
|                 | co_names          | tuple of names other      |
|                 |                   | than arguments and        |
|                 |                   | function locals           |
+-----------------+-------------------+---------------------------+
|                 | co_nlocals        | number of local variables |
+-----------------+-------------------+---------------------------+
|                 | co_stacksize      | virtual machine stack     |
|                 |                   | space required            |
+-----------------+-------------------+---------------------------+
|                 | co_varnames       | tuple of names of         |
|                 |                   | arguments and local       |
|                 |                   | variables                 |
+-----------------+-------------------+---------------------------+
|                 | co_lines()        | returns an iterator that  |
|                 |                   | yields successive         |
|                 |                   | bytecode ranges           |
+-----------------+-------------------+---------------------------+
|                 | co_positions()    | returns an iterator of    |
|                 |                   | source code positions for |
|                 |                   | each bytecode instruction |
+-----------------+-------------------+---------------------------+
|                 | replace()         | returns a copy of the     |
|                 |                   | code object with new      |
|                 |                   | values                    |
+-----------------+-------------------+---------------------------+
| generator       | __name__          | name                      |
+-----------------+-------------------+---------------------------+
|                 | __qualname__      | qualified name            |
+-----------------+-------------------+---------------------------+
|                 | gi_frame          | frame                     |
+-----------------+-------------------+---------------------------+
|                 | gi_running        | is the generator running? |
+-----------------+-------------------+---------------------------+
|                 | gi_suspended      | is the generator          |
|                 |                   | suspended?                |
+-----------------+-------------------+---------------------------+
|                 | gi_code           | code                      |
+-----------------+-------------------+---------------------------+
|                 | gi_yieldfrom      | object being iterated by  |
|                 |                   | ``yield from``, or        |
|                 |                   | ``None``                  |
+-----------------+-------------------+---------------------------+
| async generator | __name__          | name                      |
+-----------------+-------------------+---------------------------+
|                 | __qualname__      | qualified name            |
+-----------------+-------------------+---------------------------+
|                 | ag_await          | object being awaited on,  |
|                 |                   | or ``None``               |
+-----------------+-------------------+---------------------------+
|                 | ag_frame          | frame                     |
+-----------------+-------------------+---------------------------+
|                 | ag_running        | is the generator running? |
+-----------------+-------------------+---------------------------+
|                 | ag_suspended      | is the generator          |
|                 |                   | suspended?                |
+-----------------+-------------------+---------------------------+
|                 | ag_code           | code                      |
+-----------------+-------------------+---------------------------+
| coroutine       | __name__          | name                      |
+-----------------+-------------------+---------------------------+
|                 | __qualname__      | qualified name            |
+-----------------+-------------------+---------------------------+
|                 | cr_await          | object being awaited on,  |
|                 |                   | or ``None``               |
+-----------------+-------------------+---------------------------+
|                 | cr_frame          | frame                     |
+-----------------+-------------------+---------------------------+
|                 | cr_running        | is the coroutine running? |
+-----------------+-------------------+---------------------------+
|                 | cr_suspended      | is the coroutine          |
|                 |                   | suspended?                |
+-----------------+-------------------+---------------------------+
|                 | cr_code           | code                      |
+-----------------+-------------------+---------------------------+
|                 | cr_origin         | where coroutine was       |
|                 |                   | created, or ``None``. See |
|                 |                   | |coroutine-origin-link|   |
+-----------------+-------------------+---------------------------+
| builtin         | __doc__           | documentation string      |
+-----------------+-------------------+---------------------------+
|                 | __name__          | original name of this     |
|                 |                   | function or method        |
+-----------------+-------------------+---------------------------+
|                 | __qualname__      | qualified name            |
+-----------------+-------------------+---------------------------+
|                 | __self__          | instance to which a       |
|                 |                   | method is bound, or       |
|                 |                   | ``None``                  |
+-----------------+-------------------+---------------------------+

.. versionchanged:: 3.5

   Thêm các thuộc tính ``__qualname__`` và ``gi_yieldfrom`` vào generator.

   Thuộc tính ``__name__`` của generator giờ đây được đặt từ tên hàm thay vì tên mã, và hiện có thể được sửa đổi.

.. versionchanged:: 3.7

   Thêm thuộc tính ``cr_origin`` vào coroutine.

.. versionchanged:: 3.10

   Thêm thuộc tính ``__builtins__`` vào function.

.. versionchanged:: 3.11

   Thêm thuộc tính ``gi_suspended`` vào generator.

.. versionchanged:: 3.11

   Thêm thuộc tính ``cr_suspended`` vào coroutine.

.. versionchanged:: 3.12

   Thêm thuộc tính ``ag_suspended`` vào async generator.

.. versionchanged:: 3.14

   Thêm thuộc tính ``f_generator`` vào các frame.

.. function:: getmembers(object[, predicate])

   Trả về tất cả các member của một object trong một danh sách các cặp ``(name, value)``, được sắp xếp theo tên. Nếu cung cấp đối số *predicate* tùy chọn—đối số này sẽ được gọi với object ``value`` của mỗi member—thì chỉ các member mà predicate trả về giá trị true mới được đưa vào.

   .. note::

      :func:`getmembers` sẽ chỉ trả về các class attribute được định nghĩa trong metaclass khi đối số là một class và các attribute đó đã được liệt kê trong :meth:`~object.__dir__` tùy chỉnh của metaclass.


.. function:: getmembers_static(object[, predicate])

    Trả về tất cả các member của một object trong một danh sách các cặp ``(name, value)``, được sắp xếp theo tên, mà không kích hoạt dynamic lookup thông qua descriptor protocol, __getattr__ hoặc __getattribute__. Có thể chỉ trả về các member thỏa mãn một predicate đã cho.

    .. note::

        :func:`getmembers_static` có thể không truy xuất được tất cả các member mà getmembers có thể lấy (chẳng hạn như các attribute được tạo động) và có thể tìm thấy những member mà getmembers không thể tìm thấy (chẳng hạn như các descriptor gây ra AttributeError). Trong một số trường hợp, nó cũng có thể trả về các descriptor object thay vì các instance member.

    .. versionadded:: 3.11


.. function:: getmodulename(path)

   Trả về tên của module được đặt tên bởi tệp *path*, không bao gồm tên của các package bao quanh. Phần mở rộng tệp được kiểm tra với tất cả các mục trong :func:`importlib.machinery.all_suffixes`. Nếu khớp, thành phần đường dẫn cuối cùng được trả về sau khi loại bỏ phần mở rộng. Nếu không, ``None`` được trả về.

   Lưu ý rằng hàm này *only* trả về tên có ý nghĩa cho các module Python thực tế—các đường dẫn có khả năng trỏ đến các package Python vẫn sẽ trả về ``None``.

   .. versionchanged:: 3.3
      Hàm này dựa trực tiếp trên :mod:`importlib`.


.. function:: ismodule(object)

   Trả về ``True`` nếu đối tượng là một module.


.. function:: isclass(object)

   Trả về ``True`` nếu đối tượng là một lớp, bất kể là lớp dựng sẵn hay được tạo trong mã Python.

   Hàm này trả về ``False`` cho :ref:`các bí danh tổng quát <types-genericalias>` của các lớp, chẳng hạn như ``list[int]``.


.. function:: ismethod(object)

   Trả về ``True`` nếu đối tượng là một bound method được viết bằng Python.

   .. note::

      Ví dụ, với lớp sau đây::

          >>> class Greeter:
          ...     def say_hello(self):
          ...         print('hello!')

      Một bound method (còn gọi là *phương thức instance*) được tạo khi truy cập ``say_hello`` (một :term:`function` được định nghĩa trong namespace ``Greeter``) thông qua một instance của lớp ``Greeter``::

          >>> instance = Greeter()

          >>> instance.say_hello
          <bound method Greeter.say_hello of <__main__.Greeter object ...>>
          >>> ismethod(instance.say_hello)
          True
          >>> isfunction(instance.say_hello)
          False

      Việc truy cập ``say_hello`` thông qua lớp ``Greeter`` sẽ trả về chính hàm đó. Đối với hàm này, :func:`ismethod` sẽ trả về ``False``, nhưng :func:`isfunction` sẽ trả về ``True``::

          >>> Greeter.say_hello
          <function Greeter.say_hello at 0x7f7503854a90>
          >>> ismethod(Greeter.say_hello)
          False
          >>> isfunction(Greeter.say_hello)
          True

      Xem :ref:`typesmethods` để biết chi tiết.


.. function:: isfunction(object)

   Trả về ``True`` nếu đối tượng là một hàm Python, bao gồm các hàm được tạo bởi biểu thức :term:`lambda`.

   Xem ghi chú cho :func:`~inspect.ismethod` để biết ví dụ.


.. function:: ispackage(object)

   Trả về ``True`` nếu đối tượng là một :term:`package`.

   .. versionadded:: 3.14


.. function:: isgeneratorfunction(object)

   Trả về ``True`` nếu đối tượng là một hàm generator Python.

   Hàm này cũng trả về ``True`` đối với các phương thức bound được tạo từ các hàm generator Python (xem :ref:`typesmethods` để biết thêm thông tin).

   .. versionchanged:: 3.8
      Các hàm được bọc trong :func:`functools.partial` hiện trả về ``True`` nếu hàm được bọc là một hàm generator của Python.

   .. versionchanged:: 3.10.6
      :term:`Duck-typed <duck-typing>` function-like objects now return
      ``True`` nếu code object của chúng có cờ :data:`CO_GENERATOR`.

   .. versionchanged:: 3.13
      Các hàm được bọc trong :func:`functools.partialmethod` hiện trả về ``True`` nếu hàm được bọc là một hàm generator của Python.

.. function:: isgenerator(object)

   Trả về ``True`` nếu đối tượng là một generator.


.. function:: iscoroutinefunction(object)

   Trả về ``True`` nếu đối tượng là một :term:`coroutine function` (một hàm được định nghĩa bằng cú pháp :keyword:`async def`), một :func:`functools.partial` bọc một :term:`coroutine function`, hoặc một hàm sync được đánh dấu bằng
   :func:`markcoroutinefunction`.

   .. versionadded:: 3.5

   .. versionchanged:: 3.8
      Các hàm được bọc trong :func:`functools.partial` hiện trả về ``True`` nếu hàm được bọc là một :term:`coroutine function`.

   .. versionchanged:: 3.10.6
      :term:`Duck-typed <duck-typing>` function-like objects now return
      ``True`` nếu code object của chúng có cờ :data:`CO_COROUTINE`.

   .. versionchanged:: 3.12
      Các hàm đồng bộ được đánh dấu bằng :func:`markcoroutinefunction` giờ đây trả về ``True``.

   .. versionchanged:: 3.13
      Các hàm được bọc trong :func:`functools.partialmethod` giờ đây trả về ``True`` nếu hàm được bọc là một :term:`coroutine function`.


.. function:: markcoroutinefunction(func)

   Decorator dùng để đánh dấu một đối tượng có thể gọi là :term:`coroutine function` nếu đối tượng đó không được :func:`iscoroutinefunction` phát hiện theo cách khác.

   Điều này có thể hữu ích cho các hàm đồng bộ trả về một :term:`coroutine`, nếu hàm được truyền cho một API yêu cầu :func:`iscoroutinefunction`.

   Khi có thể, nên ưu tiên sử dụng một hàm :keyword:`async def`. Cũng có thể gọi hàm và kiểm tra giá trị trả về bằng
   :func:`iscoroutine`.

   .. versionadded:: 3.12


.. function:: iscoroutine(object)

   Trả về ``True`` nếu đối tượng là một :term:`coroutine` được tạo bởi một
   hàm :keyword:`async def`.

   .. versionadded:: 3.5


.. function:: isawaitable(object)

   Trả về ``True`` nếu đối tượng có thể được sử dụng trong biểu thức :keyword:`await`.

   Cũng có thể được sử dụng để phân biệt coroutine dựa trên generator với generator thông thường:

   .. testcode::

      import types

      def gen():
          yield
      @types.coroutine
      def gen_coro():
          yield

      assert not isawaitable(gen())
      assert isawaitable(gen_coro())

   .. versionadded:: 3.5


.. function:: isasyncgenfunction(object)

   Trả về ``True`` nếu đối tượng là một hàm :term:`asynchronous generator`, ví dụ:

   .. doctest::

      >>> async def agen():
      ...     yield 1
      ...
      >>> inspect.isasyncgenfunction(agen)
      True

   .. versionadded:: 3.6

   .. versionchanged:: 3.8
      Các hàm được bọc trong :func:`functools.partial` giờ đây trả về ``True`` nếu hàm được bọc là một hàm :term:`asynchronous generator`.

   .. versionchanged:: 3.10.6
      :term:`Duck-typed <duck-typing>` function-like objects now return
      ``True`` nếu đối tượng mã của chúng có cờ :data:`CO_ASYNC_GENERATOR`.

   .. versionchanged:: 3.13
      Các hàm được bọc trong :func:`functools.partialmethod` giờ đây trả về ``True`` nếu hàm được bọc là một hàm :term:`asynchronous generator`.

.. function:: isasyncgen(object)

   Trả về ``True`` nếu đối tượng là một :term:`asynchronous generator iterator` được tạo bởi một hàm :term:`asynchronous generator`.

   .. versionadded:: 3.6

.. function:: istraceback(object)

   Trả về ``True`` nếu đối tượng là một traceback.


.. function:: isframe(object)

   Trả về ``True`` nếu đối tượng là một frame.


.. function:: iscode(object)

   Trả về ``True`` nếu đối tượng là một code.


.. function:: isbuiltin(object)

   Trả về ``True`` nếu đối tượng là một hàm tích hợp hoặc một phương thức tích hợp bị ràng buộc.


.. function:: ismethodwrapper(object)

   Trả về ``True`` nếu kiểu của đối tượng là một :class:`~types.MethodWrapperType`.

   Đây là các thực thể của :class:`~types.MethodWrapperType`, chẳng hạn như :meth:`~object.__str__`,
   :meth:`~object.__eq__` và :meth:`~object.__repr__`.

   .. versionadded:: 3.11


.. function:: isroutine(object)

   Trả về ``True`` nếu đối tượng là hàm hoặc phương thức do người dùng định nghĩa hay được tích hợp sẵn.


.. function:: isabstract(object)

   Trả về ``True`` nếu đối tượng là một abstract base class.


.. function:: ismethoddescriptor(object)

   Trả về ``True`` nếu đối tượng là một method descriptor, nhưng không nếu
   :func:`isclass`, :func:`ismethod` hoặc :func:`isfunction` là true.

   Ví dụ, điều này đúng với ``int.__add__``. Một đối tượng vượt qua phép kiểm tra này có phương thức :meth:`~object.__get__`, nhưng không có phương thức :meth:`~object.__set__` hoặc phương thức :meth:`~object.__delete__`. Ngoài ra, tập hợp các thuộc tính sẽ thay đổi. Thuộc tính :attr:`~definition.__name__` thường là hợp lý, và :attr:`~definition.__doc__` cũng thường như vậy.

   Các method descriptor đồng thời vượt qua bất kỳ phép kiểm tra nào khác (:func:`!isclass`,
   :func:`!ismethod` hoặc :func:`!isfunction`) khiến hàm này trả về ``False``, đơn giản vì các phép kiểm tra khác đó đảm bảo nhiều hơn -- chẳng hạn, bạn có thể chắc chắn rằng thuộc tính :attr:`~method.__func__` tồn tại khi một đối tượng vượt qua
   :func:`ismethod`.

   .. versionchanged:: 3.13
      Hàm này không còn báo cáo không chính xác các đối tượng có :meth:`~object.__get__` và :meth:`~object.__delete__`, nhưng không có :meth:`~object.__set__`, là các method descriptor (bộ mô tả phương thức) nữa (những đối tượng như vậy là data descriptor (bộ mô tả dữ liệu), không phải method descriptor).


.. function:: isdatadescriptor(object)

   Trả về ``True`` nếu đối tượng là một data descriptor, nhưng không trả về nếu
   :func:`isclass`, :func:`ismethod` hoặc :func:`isfunction` là true.

   Data descriptor luôn có phương thức :meth:`~object.__set__` và/hoặc phương thức :meth:`~object.__delete__`. Theo tùy chọn, chúng cũng có thể có một
   phương thức :meth:`~object.__get__`.

   Ví dụ về data descriptor là :func:`properties <property>`, getset và member descriptor. Lưu ý rằng đối với hai loại sau (chỉ được định nghĩa trong các mô-đun mở rộng C), có các phép kiểm tra cụ thể hơn: :func:`isgetsetdescriptor` và
   :func:`ismemberdescriptor`, tương ứng.

   Mặc dù các data descriptor cũng có thể có :attr:`~definition.__name__` và
   :attr:`!__doc__` thuộc tính (như các property, getset và member descriptor), nhưng nhìn chung điều này không nhất thiết đúng.

   .. versionchanged:: 3.8
      Hàm này hiện báo cáo các đối tượng chỉ có phương thức :meth:`~object.__set__` là data descriptor (không còn yêu cầu phải có :meth:`~object.__get__`). Hơn nữa, các đối tượng có :meth:`~object.__delete__` nhưng không có :meth:`~object.__set__` giờ đây cũng được nhận diện chính xác là data descriptor, trong khi trước đây thì không.

.. function:: isgetsetdescriptor(object)

   Trả về ``True`` nếu đối tượng là một getset descriptor.

   .. impl-detail::

      getset là các thuộc tính được định nghĩa trong các extension module thông qua
      các cấu trúc :c:type:`PyGetSetDef`. Đối với các triển khai Python không có những kiểu như vậy, phương thức này sẽ luôn trả về ``False``.


.. function:: ismemberdescriptor(object)

   Trả về ``True`` nếu đối tượng là một member descriptor.

   .. impl-detail::

      Các member descriptor là những thuộc tính được định nghĩa trong các mô-đun mở rộng thông qua
      các cấu trúc :c:type:`PyMemberDef`. Đối với các triển khai Python không có những kiểu như vậy, phương thức này sẽ luôn trả về ``False``.


.. _inspect-source:

Lấy mã nguồn
------------

.. function:: getdoc(object)

   Lấy chuỗi tài liệu của một đối tượng và làm sạch bằng :func:`cleandoc`. Nếu chuỗi tài liệu của một đối tượng không được cung cấp và đối tượng đó là một lớp, phương thức, thuộc tính hoặc descriptor, hãy lấy chuỗi tài liệu từ hệ thống phân cấp kế thừa. Trả về ``None`` nếu chuỗi tài liệu không hợp lệ hoặc bị thiếu.

   .. versionchanged:: 3.5
      Giờ đây, các chuỗi tài liệu sẽ được kế thừa nếu không bị ghi đè.


.. function:: getcomments(object)

   Trả về trong một chuỗi duy nhất mọi dòng chú thích ngay trước mã nguồn của đối tượng (đối với một lớp, hàm hoặc phương thức), hoặc ở đầu tệp mã nguồn Python (nếu đối tượng là một mô-đun). Nếu không thể lấy mã nguồn của đối tượng, hãy trả về ``None``. Điều này có thể xảy ra nếu đối tượng được định nghĩa bằng C hoặc trong shell tương tác.


.. function:: getfile(object)

   Trả về tên của tệp (văn bản hoặc nhị phân) trong đó một đối tượng được định nghĩa. Một :exc:`OSError` sẽ được phát sinh nếu không thể lấy mã nguồn. Thao tác này sẽ thất bại với :exc:`TypeError` nếu đối tượng là một mô-đun, lớp hoặc hàm tích hợp.


.. function:: getmodule(object)

   Cố gắng đoán xem một đối tượng được định nghĩa trong module nào. Trả về ``None`` nếu không thể xác định module.


.. function:: getsourcefile(object)

   Trả về tên tệp nguồn Python mà trong đó một đối tượng được định nghĩa hoặc ``None`` nếu không có cách nào xác định để lấy mã nguồn. Một :exc:`OSError` được phát sinh nếu không thể truy xuất mã nguồn. Thao tác này sẽ thất bại với :exc:`TypeError` nếu đối tượng là một module, class hoặc function tích hợp sẵn.


.. function:: getsourcelines(object)

   Trả về danh sách các dòng mã nguồn và số dòng bắt đầu của một đối tượng. Đối số có thể là một module, class, method, function, traceback, frame hoặc code object. Mã nguồn được trả về dưới dạng danh sách các dòng tương ứng với đối tượng, còn số dòng cho biết vị trí trong tệp nguồn gốc mà tại đó dòng mã đầu tiên được tìm thấy. Một :exc:`OSError` được phát sinh nếu không thể truy xuất mã nguồn. Một :exc:`TypeError` được phát sinh nếu đối tượng là một module, class hoặc function tích hợp sẵn.

   .. versionchanged:: 3.3
      :exc:`OSError` is raised instead of :exc:`IOError`, now an alias of the
      phần trước.


.. function:: getsource(object)

   Trả về văn bản của mã nguồn cho một đối tượng. Đối số có thể là một module, class, method, function, traceback, frame hoặc code object. Mã nguồn được trả về dưới dạng một chuỗi duy nhất. Một :exc:`OSError` được phát sinh nếu không thể truy xuất mã nguồn. Một :exc:`TypeError` được phát sinh nếu đối tượng là một module, class hoặc function tích hợp sẵn.

   .. versionchanged:: 3.3
      :exc:`OSError` is raised instead of :exc:`IOError`, now an alias of the
      phần trước.


.. function:: cleandoc(doc)

   Dọn dẹp thụt lề khỏi các docstring được thụt lề để thẳng hàng với các khối mã.

   Mọi khoảng trắng ở đầu dòng đều bị xóa khỏi dòng đầu tiên. Mọi khoảng trắng ở đầu dòng có thể được xóa đồng nhất từ dòng thứ hai trở đi cũng bị xóa. Sau đó, các dòng trống ở đầu và cuối cũng bị xóa. Ngoài ra, tất cả các tab đều được mở rộng thành khoảng trắng.


.. _inspect-signature-object:

Kiểm tra nội quan các đối tượng có thể gọi bằng đối tượng Signature
-------------------------------------------------------------------

.. versionadded:: 3.3

Đối tượng :class:`Signature` đại diện cho chữ ký lời gọi của một đối tượng có thể gọi và chú thích kiểu trả về của đối tượng đó. Để lấy một đối tượng :class:`!Signature`, hãy sử dụng hàm :func:`!signature`.

.. function:: signature(callable, *, follow_wrapped=True, globals=None, locals=None, eval_str=False, annotation_format=Format.VALUE)

   Trả về một đối tượng :class:`Signature` cho *đối tượng có thể gọi* đã cho:

   .. doctest::

      >>> from inspect import signature
      >>> def foo(a, *, b:int, **kwargs):
      ...     pass

      >>> sig = signature(foo)

      >>> str(sig)
      '(a, *, b: int, **kwargs)'

      >>> str(sig.parameters['b'])
      'b: int'

      >>> sig.parameters['b'].annotation
      <class 'int'>

   Chấp nhận nhiều loại đối tượng có thể gọi trong Python, từ các hàm thông thường và lớp cho đến
   các đối tượng :func:`functools.partial`.

   Nếu một số chú thích là chuỗi (ví dụ: do đã sử dụng ``from __future__ import annotations``), :func:`signature` sẽ thử tự động chuyển các chú thích từ chuỗi bằng cách sử dụng
   :func:`annotationlib.get_annotations`. Các tham số *globals*, *locals* và *eval_str* được truyền vào :func:`!annotationlib.get_annotations` khi phân giải các annotation; xem tài liệu về :func:`!annotationlib.get_annotations` để biết hướng dẫn sử dụng các tham số này. Một thành viên của
   enum :class:`annotationlib.Format` có thể được truyền vào tham số *annotation_format* để kiểm soát định dạng của các annotation được trả về. Ví dụ, sử dụng ``annotation_format=annotationlib.Format.STRING`` để trả về các annotation ở định dạng chuỗi.

   Phát sinh :exc:`ValueError` nếu không thể cung cấp signature, và
   :exc:`TypeError` nếu loại đối tượng đó không được hỗ trợ. Ngoài ra, nếu các annotation được chuyển thành chuỗi và *eval_str* không phải là false, các lần gọi ``eval()`` để chuyển các annotation trong :func:`annotationlib.get_annotations` từ chuỗi về lại có khả năng phát sinh bất kỳ loại exception nào.

   Dấu gạch chéo (/) trong signature của một hàm cho biết các tham số đứng trước nó chỉ được truyền theo vị trí. Để biết thêm thông tin, hãy xem
   :ref:`mục FAQ về các tham số chỉ nhận theo vị trí <faq-positional-only-arguments>`.

   .. versionchanged:: 3.5
      Đã thêm tham số *follow_wrapped*. Truyền ``False`` để lấy signature dành riêng cho *callable* (``callable.__wrapped__`` sẽ không được dùng để bỏ lớp bao quanh các callable đã được trang trí.)

   .. versionchanged:: 3.10
      Các tham số *globals*, *locals* và *eval_str* đã được thêm vào.

   .. versionchanged:: 3.14
      Tham số *annotation_format* đã được thêm vào.

   .. note::

      Một số callable có thể không thể được introspect trong một số triển khai Python nhất định. Ví dụ, trong CPython, một số hàm tích hợp được định nghĩa bằng C không cung cấp metadata về các đối số của chúng.

   .. impl-detail::

      Nếu đối tượng được truyền vào có thuộc tính :attr:`!__signature__`, chúng ta có thể sử dụng thuộc tính này để tạo signature. Ngữ nghĩa chính xác là một chi tiết triển khai và có thể thay đổi mà không được thông báo trước. Hãy tham khảo mã nguồn để biết ngữ nghĩa hiện tại.


.. class:: Signature(parameters=None, *, return_annotation=Signature.empty)

   Một đối tượng :class:`!Signature` biểu diễn signature gọi của một hàm và annotation giá trị trả về của hàm đó. Với mỗi tham số mà hàm chấp nhận, đối tượng này lưu trữ một
   đối tượng :class:`Parameter` trong collection :attr:`parameters` của nó.

   Đối số tùy chọn *parameters* là một chuỗi các đối tượng :class:`Parameter`, được xác thực để kiểm tra rằng không có tham số nào trùng tên và các tham số được sắp xếp đúng thứ tự, tức là trước hết là positional-only, tiếp theo là positional-or-keyword, đồng thời các tham số có giá trị mặc định phải đứng sau các tham số không có giá trị mặc định.

   Đối số *return_annotation* tùy chọn có thể là một đối tượng Python bất kỳ. Đối số này biểu thị chú thích "return" của callable.

   Các đối tượng :class:`!Signature` là *immutable*. Hãy sử dụng :meth:`Signature.replace` hoặc
   :func:`copy.replace` để tạo một bản sao đã sửa đổi.

   .. versionchanged:: 3.5
      :class:`!Signature` objects are now picklable and :term:`hashable`.

   .. attribute:: Signature.empty

      Một marker đặc biệt ở cấp lớp dùng để chỉ định rằng không có chú thích return.

   .. attribute:: Signature.parameters

      Một ánh xạ có thứ tự từ tên của các tham số đến các đối tượng tương ứng
      :class:`Parameter`. Các tham số xuất hiện đúng theo thứ tự định nghĩa, bao gồm cả các tham số chỉ nhận keyword.

      .. versionchanged:: 3.7
         Python chỉ đảm bảo rõ ràng rằng thứ tự khai báo của các tham số chỉ nhận keyword được giữ nguyên kể từ phiên bản 3.7, mặc dù trên thực tế thứ tự này vốn luôn được giữ nguyên trong Python 3.

   .. attribute:: Signature.return_annotation

      Chú thích "return" của callable. Nếu callable không có chú thích "return", thuộc tính này được đặt thành :attr:`Signature.empty`.

   .. method:: Signature.bind(*args, **kwargs)

      Tạo ánh xạ từ các đối số positional và keyword đến các tham số. Trả về :class:`BoundArguments` nếu ``*args`` và ``**kwargs`` khớp với signature, hoặc phát sinh :exc:`TypeError`.

   .. method:: Signature.bind_partial(*args, **kwargs)

      Hoạt động giống như :meth:`Signature.bind`, nhưng cho phép bỏ qua một số đối số bắt buộc (mô phỏng hành vi của :func:`functools.partial`). Trả về :class:`BoundArguments`, hoặc phát sinh :exc:`TypeError` nếu các đối số đã truyền không khớp với signature.

   .. method:: Signature.replace(*[, parameters][, return_annotation])

      Tạo một đối tượng :class:`Signature` mới dựa trên đối tượng
      mà :meth:`replace` được gọi trên đó. Có thể truyền các *tham số* khác nhau và/hoặc *return_annotation* để ghi đè các thuộc tính tương ứng của signature cơ sở. Để xóa ``return_annotation`` khỏi signature đã sao chép
      :class:`!Signature`, hãy truyền vào
      :attr:`Signature.empty`.

      .. doctest::

         >>> def test(a, b):
         ...     pass
         ...
         >>> sig = signature(test)
         >>> new_sig = sig.replace(return_annotation="new return anno")
         >>> str(new_sig)
         "(a, b) -> 'new return anno'"

      Các đối tượng :class:`Signature` cũng được hàm generic hỗ trợ
      :func:`copy.replace`.

   .. method:: format(*, max_width=None, quote_annotation_strings=True)

      Tạo biểu diễn chuỗi của đối tượng :class:`Signature`.

      Nếu truyền *max_width*, phương thức sẽ cố gắng đưa signature vào các dòng có tối đa *max_width* ký tự. Nếu signature dài hơn *max_width*, tất cả tham số sẽ nằm trên các dòng riêng biệt.

      Nếu *quote_annotation_strings* là False, :term:`annotations <annotation>` trong signature sẽ được hiển thị mà không có dấu ngoặc kép mở và đóng nếu chúng là chuỗi. Điều này hữu ích nếu signature được tạo bằng định dạng
      :attr:`~annotationlib.Format.STRING` hoặc nếu đã sử dụng ``from __future__ import annotations``.

      .. versionadded:: 3.13

      .. versionchanged:: 3.14
         Tham số *unquote_annotations* đã được thêm.

   .. classmethod:: Signature.from_callable(obj, *, follow_wrapped=True, globals=None, locals=None, eval_str=False)

       Trả về một đối tượng :class:`Signature` (hoặc lớp con của nó) cho một callable *obj* nhất định.

       Phương thức này giúp đơn giản hóa việc tạo lớp con của :class:`Signature`:

       .. testcode::

          class MySignature(Signature):
              pass
          sig = MySignature.from_callable(sum)
          assert isinstance(sig, MySignature)

       Hành vi của nó giống hệt :func:`signature` về mọi mặt khác.

       .. versionadded:: 3.5

       .. versionchanged:: 3.10
         Các tham số *globals*, *locals* và *eval_str* đã được thêm vào.


.. class:: Parameter(name, kind, *, default=Parameter.empty, annotation=Parameter.empty)

   Các đối tượng :class:`!Parameter` là *bất biến*. Thay vì sửa đổi một đối tượng :class:`!Parameter`, bạn có thể sử dụng :meth:`Parameter.replace` hoặc :func:`copy.replace` để tạo một bản sao đã sửa đổi.

   .. versionchanged:: 3.5
      Các đối tượng Parameter hiện có thể được pickle và :term:`hashable`.

   .. attribute:: Parameter.empty

      Một marker đặc biệt ở cấp lớp để chỉ định việc không có giá trị mặc định và chú thích.

   .. attribute:: Parameter.name

      Tên của parameter dưới dạng chuỗi. Tên này phải là một mã định danh Python hợp lệ.

      .. impl-detail::

         CPython tạo các tên parameter ngầm định có dạng ``.0`` trên các code object được dùng để triển khai các biểu thức comprehension và generator.

         .. versionchanged:: 3.6
            Các tên tham số này hiện được module này cung cấp dưới dạng những tên như ``implicit0``.

   .. attribute:: Parameter.default

      Giá trị mặc định của tham số. Nếu tham số không có giá trị mặc định, thuộc tính này được đặt thành :attr:`Parameter.empty`.

   .. attribute:: Parameter.annotation

      Chú thích của tham số. Nếu tham số không có chú thích, thuộc tính này được đặt thành :attr:`Parameter.empty`.

   .. attribute:: Parameter.kind

      Mô tả cách các giá trị đối số được liên kết với tham số. Các giá trị có thể có được truy cập thông qua :class:`Parameter` (chẳng hạn như ``Parameter.KEYWORD_ONLY``), đồng thời hỗ trợ phép so sánh và sắp xếp theo thứ tự sau:

      .. tabularcolumns:: |l|L|

      +-------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
      | Tên                     | Ý nghĩa                                                                                                                                                                  |
      +=========================+==========================================================================================================================================================================+
      | *POSITIONAL_ONLY*       | Giá trị phải được cung cấp dưới dạng đối số positional. Các tham số chỉ nhận positional là những tham số xuất hiện trước mục ``/`` (nếu có) trong định nghĩa hàm Python. |
      +-------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
      | *POSITIONAL_OR_KEYWORD* | Giá trị có thể được cung cấp dưới dạng đối số keyword hoặc positional (đây là hành vi binding tiêu chuẩn đối với các hàm được triển khai bằng Python.)                   |
      +-------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
      | *VAR_POSITIONAL*        | Một tuple gồm các đối số positional không được liên kết với bất kỳ tham số nào khác. Điều này tương ứng với tham số ``*args`` trong định nghĩa hàm Python.               |
      +-------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
      | *KEYWORD_ONLY*          | Giá trị phải được cung cấp dưới dạng đối số keyword. Các tham số chỉ nhận keyword là những tham số xuất hiện sau mục ``*`` hoặc ``*args`` trong định nghĩa hàm Python.   |
      +-------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
      | *VAR_KEYWORD*           | Một dict chứa các đối số từ khóa không được liên kết với bất kỳ tham số nào khác. Điều này tương ứng với một tham số ``**kwargs`` trong định nghĩa hàm Python.           |
      +-------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

      Ví dụ: in tất cả các đối số chỉ nhận từ khóa không có giá trị mặc định:

      .. doctest::

         >>> def foo(a, b, *, c, d=10):
         ...     pass

         >>> sig = signature(foo)
         >>> for param in sig.parameters.values():
         ...     if (param.kind == param.KEYWORD_ONLY and
         ...                        param.default is param.empty):
         ...         print('Parameter:', param)
         Parameter: c

   .. attribute:: Parameter.kind.description

      Mô tả một giá trị enum của :attr:`Parameter.kind`.

      .. versionadded:: 3.8

      Ví dụ: in tất cả mô tả của các đối số:

      .. doctest::

         >>> def foo(a, b, *, c, d=10):
         ...     pass

         >>> sig = signature(foo)
         >>> for param in sig.parameters.values():
         ...     print(param.kind.description)
         positional or keyword
         positional or keyword
         keyword-only
         keyword-only

   .. method:: Parameter.replace(*[, name][, kind][, default][, annotation])

      Tạo một instance :class:`Parameter` mới dựa trên instance mà phương thức được gọi trên đó. Để ghi đè một thuộc tính :class:`!Parameter`, hãy truyền đối số tương ứng. Để xóa một giá trị mặc định hoặc/và một chú thích khỏi một
      :class:`!Parameter`, hãy truyền :attr:`Parameter.empty`.

      .. doctest::

         >>> from inspect import Parameter
         >>> param = Parameter('foo', Parameter.KEYWORD_ONLY, default=42)
         >>> str(param)
         'foo=42'

         >>> str(param.replace()) # Sẽ tạo một bản sao nông của 'param'
         'foo=42'

         >>> str(param.replace(default=Parameter.empty, annotation='spam'))
         "foo: 'spam'"

      Các đối tượng :class:`Parameter` cũng được hàm generic hỗ trợ
      :func:`copy.replace`.

   .. versionchanged:: 3.4
      Trong Python 3.3, các đối tượng :class:`Parameter` được phép có ``name`` được đặt thành ``None`` nếu ``kind`` của chúng được đặt thành ``POSITIONAL_ONLY``. Điều này không còn được phép.

.. class:: BoundArguments

   Kết quả của lệnh gọi :meth:`Signature.bind` hoặc :meth:`Signature.bind_partial`. Chứa ánh xạ các đối số với các tham số của hàm.

   .. attribute:: BoundArguments.arguments

      Một ánh xạ có thể thay đổi từ tên của tham số đến giá trị của đối số. Chỉ chứa các đối số được liên kết một cách rõ ràng. Các thay đổi trong :attr:`arguments` sẽ được phản ánh trong :attr:`args` và :attr:`kwargs`.

      Nên được sử dụng cùng với :attr:`Signature.parameters` cho mọi mục đích xử lý đối số.

      .. note::

         Các đối số mà :meth:`Signature.bind` hoặc
         Các :meth:`Signature.bind_partial` dựa vào một giá trị mặc định sẽ bị bỏ qua. Tuy nhiên, nếu cần, hãy sử dụng :meth:`BoundArguments.apply_defaults` để thêm chúng.

      .. versionchanged:: 3.9
         :attr:`arguments` is now of type :class:`dict`. Formerly, it was of
         kiểu :class:`collections.OrderedDict`.

   .. attribute:: BoundArguments.args

      Một tuple chứa các giá trị đối số vị trí. Được tính động từ
      thuộc tính :attr:`arguments`.

   .. attribute:: BoundArguments.kwargs

      Một dict chứa các giá trị đối số từ khóa. Được tính động từ
      thuộc tính :attr:`arguments`. Các đối số có thể được truyền theo vị trí sẽ được đưa vào :attr:`args` thay vào đó.

   .. attribute:: BoundArguments.signature

      Một tham chiếu đến đối tượng :class:`Signature` cha.

   .. method:: BoundArguments.apply_defaults()

      Đặt các giá trị mặc định cho những đối số bị thiếu.

      Đối với các đối số biến-positional (``*args``), giá trị mặc định là một tuple rỗng.

      Đối với các đối số biến-keyword (``**kwargs``), giá trị mặc định là một dict rỗng.

      .. doctest::

         >>> def foo(a, b='ham', *args): pass
         >>> ba = inspect.signature(foo).bind('spam')
         >>> ba.apply_defaults()
         >>> ba.arguments
         {'a': 'spam', 'b': 'ham', 'args': ()}

      .. versionadded:: 3.5

   Có thể sử dụng các thuộc tính :attr:`args` và :attr:`kwargs` để gọi các hàm:

   .. testcode::

      def test(a, *, b):
          ...

      sig = signature(test)
      ba = sig.bind(10, b=20)
      test(*ba.args, **ba.kwargs)


.. seealso::

   :pep:`362` - Đối tượng Signature của hàm.
      Đặc tả chi tiết, thông tin chi tiết về cách triển khai và các ví dụ.


.. _inspect-classes-functions:

Các lớp và hàm
--------------

.. function:: getclasstree(classes, unique=False)

   Sắp xếp danh sách lớp đã cho thành một hệ phân cấp gồm các danh sách lồng nhau. Khi xuất hiện một danh sách lồng nhau, danh sách đó chứa các lớp dẫn xuất từ lớp có mục nhập ngay trước danh sách. Mỗi mục nhập là một bộ 2 phần tử gồm một lớp và một tuple chứa các lớp cơ sở của lớp đó. Nếu đối số *unique* là true, cấu trúc được trả về sẽ chứa chính xác một mục nhập cho mỗi lớp trong danh sách đã cho. Nếu không, các lớp sử dụng đa kế thừa và các lớp dẫn xuất của chúng sẽ xuất hiện nhiều lần.


.. function:: getfullargspec(func)

   Lấy tên và giá trị mặc định của các tham số trong một hàm Python. Một
   :term:`named tuple` được trả về:

   ``FullArgSpec(args, varargs, varkw, defaults, kwonlyargs, kwonlydefaults,
   annotations)``

   *args* là danh sách tên của các tham số vị trí. *varargs* là tên của tham số ``*`` hoặc ``None`` nếu không chấp nhận các đối số vị trí tùy ý. *varkw* là tên của tham số ``**`` hoặc ``None`` nếu không chấp nhận các đối số từ khóa tùy ý. *defaults* là một tuple gồm *n* giá trị mặc định của đối số, tương ứng với *n* tham số vị trí cuối cùng, hoặc ``None`` nếu không có giá trị mặc định nào như vậy được định nghĩa. *kwonlyargs* là danh sách tên các tham số chỉ từ khóa theo thứ tự khai báo. *kwonlydefaults* là một dictionary ánh xạ tên các tham số từ *kwonlyargs* tới các giá trị mặc định được sử dụng khi không cung cấp đối số. *annotations* là một dictionary ánh xạ tên tham số tới các chú thích. Khóa đặc biệt ``"return"`` được dùng để báo cáo chú thích cho giá trị trả về của hàm (nếu có).

   Lưu ý rằng :func:`signature` và
   :ref:`Signature Object <inspect-signature-object>` cung cấp API được khuyến nghị để introspection các đối tượng callable và hỗ trợ thêm các hành vi (chẳng hạn như đối số chỉ vị trí) đôi khi gặp trong API của các extension module. Hàm này chủ yếu được giữ lại để sử dụng trong mã cần duy trì khả năng tương thích với API của module ``inspect`` trong Python 2.

   .. versionchanged:: 3.4
      Hàm này hiện dựa trên :func:`signature`, nhưng vẫn bỏ qua các thuộc tính ``__wrapped__`` và bao gồm tham số đầu tiên đã được binding trong đầu ra chữ ký đối với các bound method.

   .. versionchanged:: 3.6
      Phương thức này trước đây được ghi nhận là không còn được khuyến nghị sử dụng để thay cho
      :func:`signature` trong Python 3.5, nhưng quyết định đó đã được đảo ngược nhằm khôi phục một giao diện chuẩn được hỗ trợ rõ ràng cho mã Python 2/3 dùng chung một nguồn đang chuyển khỏi API cũ
      :func:`!getargspec` API.

   .. versionchanged:: 3.7
      Python chỉ đảm bảo tường minh rằng thứ tự khai báo của các tham số chỉ dùng từ khóa được giữ nguyên kể từ phiên bản 3.7, mặc dù trên thực tế thứ tự này luôn được giữ nguyên trong Python 3.


.. function:: getargvalues(frame)

   Lấy thông tin về các đối số được truyền vào một frame cụ thể. Một
   :term:`named tuple` ``ArgInfo(args, varargs, keywords, locals)`` được trả về. *args* là danh sách tên các đối số. *varargs* và *keywords* là tên của các đối số ``*`` và ``**`` hoặc ``None``. *locals* là từ điển biến cục bộ của frame đã cho.

   .. note::
      Hàm này đã vô tình được đánh dấu là không còn được khuyến nghị sử dụng trong Python 3.5.


.. function:: formatargvalues(args[, varargs, varkw, locals, formatarg, formatvarargs, formatvarkw, formatvalue])

   Định dạng một đặc tả đối số dễ đọc từ bốn giá trị được trả về bởi
   :func:`getargvalues`.  Các đối số format\* là những hàm định dạng tùy chọn tương ứng, được gọi để chuyển tên và giá trị thành chuỗi.

   .. note::
      Hàm này đã vô tình được đánh dấu là không còn được khuyến nghị sử dụng trong Python 3.5.


.. function:: getmro(cls)

   Trả về một tuple gồm các lớp cơ sở của lớp cls, bao gồm cả cls, theo thứ tự phân giải phương thức. Không có lớp nào xuất hiện quá một lần trong tuple này. Lưu ý rằng thứ tự phân giải phương thức phụ thuộc vào kiểu của cls. Trừ khi đang sử dụng một metaclass do người dùng định nghĩa rất đặc biệt, cls sẽ là phần tử đầu tiên của tuple.


.. function:: getcallargs(func, /, *args, **kwds)

   Liên kết *args* và *kwds* với tên các đối số của hàm hoặc phương thức Python *func*, như thể hàm hoặc phương thức đó được gọi cùng các đối số này. Đối với các phương thức đã liên kết, đồng thời liên kết đối số đầu tiên (thường có tên là ``self``) với thực thể liên kết. Một dict được trả về, ánh xạ tên các đối số (bao gồm tên của các đối số ``*`` và ``**``, nếu có) với các giá trị tương ứng của chúng từ *args* và *kwds*. Nếu gọi *func* không đúng cách, tức là khi ``func(*args, **kwds)`` sẽ phát sinh một ngoại lệ do chữ ký không tương thích, một ngoại lệ cùng kiểu và có thông báo giống hoặc tương tự sẽ được phát sinh. Ví dụ:

   .. doctest::

      >>> from inspect import getcallargs
      >>> def f(a, b=1, *pos, **named):
      ...     pass
      ...
      >>> getcallargs(f, 1, 2, 3) == {'a': 1, 'named': {}, 'b': 2, 'pos': (3,)}
      True
      >>> getcallargs(f, a=2, x=4) == {'a': 2, 'named': {'x': 4}, 'b': 1, 'pos': ()}
      True
      >>> getcallargs(f)
      Traceback (most recent call last):
      ...
      TypeError: f() missing 1 required positional argument: 'a'

   .. versionadded:: 3.2

   .. deprecated:: 3.5
      Thay vào đó, hãy sử dụng :meth:`Signature.bind` và :meth:`Signature.bind_partial`.


.. function:: getclosurevars(func)

   Lấy ánh xạ các tham chiếu tên bên ngoài trong hàm hoặc phương thức Python *func* tới các giá trị hiện tại của chúng. Một
   :term:`named tuple` ``ClosureVars(nonlocals, globals, builtins, unbound)`` được trả về. *nonlocals* ánh xạ các tên được tham chiếu tới các biến closure theo phạm vi từ vựng, *globals* tới các biến toàn cục của module chứa hàm và *builtins* tới các builtins có thể truy cập từ phần thân hàm. *unbound* là tập hợp các tên được tham chiếu trong hàm nhưng hoàn toàn không thể phân giải dựa trên các biến toàn cục và builtins hiện tại của module.

   :exc:`TypeError` được phát sinh nếu *func* không phải là một hàm hoặc phương thức Python.

   .. versionadded:: 3.3


.. function:: unwrap(func, *, stop=None)

   Lấy đối tượng được *func* bọc. Hàm này lần theo chuỗi các thuộc tính :attr:`__wrapped__` và trả về đối tượng cuối cùng trong chuỗi.

   *stop* là một callback tùy chọn, nhận một đối tượng trong chuỗi wrapper làm đối số duy nhất và cho phép dừng quá trình tháo bọc sớm nếu callback trả về một giá trị true. Nếu callback không bao giờ trả về một giá trị true, đối tượng cuối cùng trong chuỗi sẽ được trả về như thường lệ. Ví dụ:
   :func:`signature` sử dụng điều này để dừng quá trình tháo bọc nếu bất kỳ đối tượng nào trong chuỗi có thuộc tính ``__signature__`` được định nghĩa.

   :exc:`ValueError` được phát sinh nếu phát hiện một chu kỳ.

   .. versionadded:: 3.4


.. function:: get_annotations(obj, *, globals=None, locals=None, eval_str=False, format=annotationlib.Format.VALUE)

   Tính toán dict annotations cho một đối tượng.

   Đây là bí danh của :func:`annotationlib.get_annotations`; xem tài liệu về hàm đó để biết thêm thông tin.

   .. caution::

      Hàm này có thể thực thi mã tùy ý có trong các annotation. Xem :ref:`annotationlib-security` để biết thêm thông tin.

   .. versionadded:: 3.10

   .. versionchanged:: 3.14
      Hàm này hiện là bí danh của :func:`annotationlib.get_annotations`. Gọi nó dưới dạng ``inspect.get_annotations`` vẫn sẽ tiếp tục hoạt động.


.. _inspect-stack:

Ngăn xếp của interpreter
------------------------

Một số hàm sau đây trả về
các đối tượng :class:`FrameInfo`. Để đảm bảo khả năng tương thích ngược, các đối tượng này cho phép thực hiện các thao tác kiểu tuple trên mọi thuộc tính, ngoại trừ ``positions``. Hành vi này được xem là đã lỗi thời và có thể bị loại bỏ trong tương lai.

.. class:: FrameInfo

   .. attribute:: frame

      :ref:`Đối tượng frame <frame-objects>` mà bản ghi tương ứng với.

   .. attribute:: filename

      Tên tệp liên kết với đoạn mã đang được thực thi bởi frame mà bản ghi này tương ứng.

   .. attribute:: lineno

      Số dòng của dòng hiện tại liên kết với đoạn mã đang được thực thi bởi frame mà bản ghi này tương ứng.

   .. attribute:: function

      Tên hàm đang được thực thi bởi frame mà bản ghi này tương ứng.

   .. attribute:: code_context

      Danh sách các dòng ngữ cảnh từ mã nguồn đang được thực thi bởi frame mà bản ghi này tương ứng.

   .. attribute:: index

      Chỉ mục của dòng hiện tại đang được thực thi trong danh sách :attr:`code_context`.

   .. attribute:: positions

      Một đối tượng :class:`dis.Positions` chứa số dòng bắt đầu, số dòng kết thúc, độ lệch cột bắt đầu và độ lệch cột kết thúc liên kết với lệnh đang được thực thi bởi frame mà bản ghi này tương ứng.

   .. versionchanged:: 3.5
      Trả về một :term:`named tuple` thay vì một :class:`tuple`.

   .. versionchanged:: 3.11
      :class:`!FrameInfo` is now a class instance
      (tương thích ngược với :term:`named tuple` trước đó).


.. class:: Traceback

   .. attribute:: filename

      Tên tệp liên kết với đoạn mã đang được thực thi bởi frame mà traceback này tương ứng.

   .. attribute:: lineno

      Số dòng của dòng hiện tại liên kết với đoạn mã đang được thực thi bởi frame mà traceback này tương ứng.

   .. attribute:: function

      Tên hàm đang được thực thi bởi frame mà traceback này tương ứng.

   .. attribute:: code_context

      Danh sách các dòng ngữ cảnh từ mã nguồn đang được thực thi bởi frame mà traceback này tương ứng.

   .. attribute:: index

      Chỉ mục của dòng hiện tại đang được thực thi trong danh sách :attr:`code_context`.

   .. attribute:: positions

      Một đối tượng :class:`dis.Positions` chứa số dòng bắt đầu, số dòng kết thúc, offset cột bắt đầu và offset cột kết thúc liên kết với instruction đang được thực thi bởi frame mà traceback này tương ứng.

   .. versionchanged:: 3.11
      :class:`!Traceback` is now a class instance
      (tương thích ngược với :term:`named tuple` trước đó).


.. note::

   Việc giữ các tham chiếu đến đối tượng frame, như tham chiếu nằm trong phần tử đầu tiên của các bản ghi frame mà những hàm này trả về, có thể khiến chương trình của bạn tạo ra các chu kỳ tham chiếu. Một khi chu kỳ tham chiếu được tạo, vòng đời của tất cả đối tượng có thể được truy cập từ các đối tượng tạo thành chu kỳ có thể kéo dài hơn nhiều, ngay cả khi trình phát hiện chu kỳ tùy chọn của Python được bật. Nếu bắt buộc phải tạo các chu kỳ như vậy, điều quan trọng là phải bảo đảm chúng được ngắt một cách rõ ràng để tránh việc hủy các đối tượng bị trì hoãn và mức tiêu thụ bộ nhớ tăng lên do đó gây ra.

   Mặc dù trình phát hiện chu kỳ sẽ phát hiện các chu kỳ này, việc hủy các frame (và biến cục bộ) có thể được thực hiện một cách xác định bằng cách loại bỏ chu kỳ trong một
   mệnh đề :keyword:`finally`. Điều này cũng quan trọng nếu trình phát hiện chu kỳ đã bị tắt khi biên dịch Python hoặc khi sử dụng :func:`gc.disable`. Ví dụ:::

      def handle_stackframe_without_leak():
          frame = inspect.currentframe()
          try:
              # thực hiện gì đó với frame
          finally:
              del frame

   Nếu muốn giữ frame lại (chẳng hạn để in traceback sau này), bạn cũng có thể ngắt các chu kỳ tham chiếu bằng cách sử dụng
   phương thức :meth:`frame.clear`.

Đối số *context* tùy chọn được hầu hết các hàm này hỗ trợ chỉ định số dòng ngữ cảnh cần trả về, được căn giữa quanh dòng hiện tại.


.. function:: getframeinfo(frame, context=1)

   Lấy thông tin về một frame hoặc đối tượng traceback. Một đối tượng :class:`Traceback` được trả về.

   .. versionchanged:: 3.11
      Một đối tượng :class:`Traceback` được trả về thay vì một named tuple.

.. function:: getouterframes(frame, context=1)

   Lấy danh sách các đối tượng :class:`FrameInfo` cho một frame và tất cả các frame bên ngoài. Các frame này biểu diễn những lời gọi dẫn đến việc tạo ra *frame*. Mục đầu tiên trong danh sách được trả về biểu diễn *frame*; mục cuối cùng biểu diễn lời gọi ngoài cùng trên ngăn xếp của *frame*.

   .. versionchanged:: 3.5
      Một danh sách các :term:`named tuples <named tuple>` ``FrameInfo(frame, filename, lineno, function, code_context, index)`` được trả về.

   .. versionchanged:: 3.11
      Một danh sách các đối tượng :class:`FrameInfo` được trả về.

.. function:: getinnerframes(traceback, context=1)

   Lấy danh sách các đối tượng :class:`FrameInfo` cho frame của traceback và tất cả các frame bên trong. Các frame này biểu diễn những lời gọi được thực hiện do *frame* gây ra. Mục đầu tiên trong danh sách biểu diễn *traceback*; mục cuối cùng biểu diễn nơi ngoại lệ được phát sinh.

   .. versionchanged:: 3.5
      Một danh sách các :term:`named tuples <named tuple>` ``FrameInfo(frame, filename, lineno, function, code_context, index)`` được trả về.

   .. versionchanged:: 3.11
      Một danh sách các đối tượng :class:`FrameInfo` được trả về.

.. function:: currentframe()

   Trả về đối tượng frame cho stack frame của bên gọi.

   .. impl-detail::

      Hàm này dựa vào khả năng hỗ trợ stack frame Python trong interpreter, nhưng khả năng này không được đảm bảo tồn tại trong mọi triển khai Python. Nếu chạy trong một triển khai không hỗ trợ stack frame Python, hàm này sẽ trả về ``None``.


.. function:: stack(context=1)

   Trả về danh sách các đối tượng :class:`FrameInfo` cho stack của bên gọi. Mục đầu tiên trong danh sách được trả về đại diện cho bên gọi; mục cuối cùng đại diện cho lời gọi ngoài cùng trên stack.

   .. versionchanged:: 3.5
      Một danh sách các :term:`named tuples <named tuple>` ``FrameInfo(frame, filename, lineno, function, code_context, index)`` được trả về.

   .. versionchanged:: 3.11
      Một danh sách các đối tượng :class:`FrameInfo` được trả về.

.. function:: trace(context=1)

   Trả về một danh sách các đối tượng :class:`FrameInfo` cho ngăn xếp giữa frame hiện tại và frame nơi ngoại lệ đang được xử lý được phát sinh. Phần tử đầu tiên trong danh sách đại diện cho caller; phần tử cuối cùng đại diện cho nơi ngoại lệ được phát sinh.

   .. versionchanged:: 3.5
      Một danh sách các :term:`named tuples <named tuple>` ``FrameInfo(frame, filename, lineno, function, code_context, index)`` được trả về.

   .. versionchanged:: 3.11
      Một danh sách các đối tượng :class:`FrameInfo` được trả về.

Lấy thuộc tính theo cách tĩnh
-----------------------------

Cả :func:`getattr` và :func:`hasattr` đều có thể kích hoạt việc thực thi mã khi lấy thuộc tính hoặc kiểm tra sự tồn tại của thuộc tính. Các descriptor, chẳng hạn như property, sẽ được gọi và :meth:`~object.__getattr__` và
:meth:`~object.__getattribute__` có thể được gọi.

Trong những trường hợp bạn muốn thực hiện việc introspection thụ động, chẳng hạn như với các công cụ tài liệu, điều này có thể gây bất tiện. :func:`getattr_static` có chữ ký tương tự :func:`getattr` nhưng tránh thực thi mã khi lấy thuộc tính.

.. function:: getattr_static(obj, attr)
              getattr_static(obj, attr, default)

   Truy xuất các thuộc tính mà không kích hoạt tra cứu động thông qua giao thức descriptor, :meth:`~object.__getattr__` hoặc :meth:`~object.__getattribute__`.

   Lưu ý: hàm này có thể không truy xuất được tất cả các thuộc tính mà getattr có thể lấy (chẳng hạn như các thuộc tính được tạo động), đồng thời có thể tìm thấy những thuộc tính mà getattr không thể tìm thấy (chẳng hạn như các descriptor gây ra AttributeError). Hàm này cũng có thể trả về các đối tượng descriptor thay vì các thành viên của instance.

   Nếu :attr:`~object.__dict__` của instance bị một thành viên khác che khuất (ví dụ như một property), hàm này sẽ không thể tìm thấy các thành viên của instance.

   .. versionadded:: 3.2

:func:`getattr_static` không phân giải các descriptor, chẳng hạn như các slot descriptor hoặc getset descriptor trên những đối tượng được triển khai bằng C. Đối tượng descriptor được trả về thay cho thuộc tính bên dưới.

Bạn có thể xử lý các trường hợp này bằng đoạn mã sau. Lưu ý rằng với các getset descriptor tùy ý, việc gọi chúng có thể kích hoạt thực thi mã::

   # mã ví dụ để phân giải các loại descriptor tích hợp sẵn
   class _foo:
       __slots__ = ['foo']

   slot_descriptor = type(_foo.foo)
   getset_descriptor = type(type(open(__file__)).name)
   wrapper_descriptor = type(str.__dict__['__add__'])
   descriptor_types = (slot_descriptor, getset_descriptor, wrapper_descriptor)

   result = getattr_static(some_object, 'foo')
   if type(result) in descriptor_types:
       try:
           result = result.__get__()
       except AttributeError:
           # descriptor có thể raise AttributeError để
           # cho biết không có giá trị nền tảng
           # trong trường hợp đó, descriptor sẽ tự
           # phải thực hiện việc này
           pass


Trạng thái hiện tại của Generator, Coroutine và Asynchronous Generator
----------------------------------------------------------------------

Khi triển khai các bộ lập lịch coroutine và cho những mục đích nâng cao khác của generator, việc xác định một generator hiện đang thực thi, đang chờ bắt đầu hoặc tiếp tục thực thi, hay đã kết thúc là rất hữu ích. :func:`getgeneratorstate` cho phép dễ dàng xác định trạng thái hiện tại của một generator.

.. function:: getgeneratorstate(generator)

   Lấy trạng thái hiện tại của generator-iterator.

   Các trạng thái có thể có là:

   * GEN_CREATED: Đang chờ bắt đầu thực thi.
   * GEN_RUNNING: Hiện đang được interpreter thực thi.
   * GEN_SUSPENDED: Hiện đang bị tạm dừng tại một biểu thức yield.
   * GEN_CLOSED: Đã hoàn tất thực thi.

   .. versionadded:: 3.2

.. function:: getcoroutinestate(coroutine)

   Lấy trạng thái hiện tại của một đối tượng coroutine. Hàm này được thiết kế để sử dụng với các đối tượng coroutine được tạo bởi các hàm :keyword:`async def`, nhưng sẽ chấp nhận mọi đối tượng tương tự coroutine có các thuộc tính ``cr_running`` và ``cr_frame``.

   Các trạng thái có thể có là:

   * CORO_CREATED: Đang chờ bắt đầu thực thi.
   * CORO_RUNNING: Hiện đang được trình thông dịch thực thi.
   * CORO_SUSPENDED: Hiện đang bị tạm dừng tại một biểu thức await.
   * CORO_CLOSED: Quá trình thực thi đã hoàn tất.

   .. versionadded:: 3.5

.. function:: getasyncgenstate(agen)

   Lấy trạng thái hiện tại của một đối tượng asynchronous generator. Hàm này được thiết kế để sử dụng với các đối tượng asynchronous iterator được tạo bởi
   các hàm :keyword:`async def` sử dụng câu lệnh :keyword:`yield`, nhưng sẽ chấp nhận mọi đối tượng giống asynchronous generator có các thuộc tính ``ag_running`` và ``ag_frame``.

   Các trạng thái có thể có là:

   * AGEN_CREATED: Đang chờ bắt đầu thực thi.
   * AGEN_RUNNING: Hiện đang được interpreter thực thi.
   * AGEN_SUSPENDED: Hiện đang tạm dừng tại một biểu thức yield.
   * AGEN_CLOSED: Đã hoàn tất thực thi.

   .. versionadded:: 3.12

Bạn cũng có thể truy vấn trạng thái nội bộ hiện tại của generator. Điều này chủ yếu hữu ích cho mục đích kiểm thử, nhằm đảm bảo trạng thái nội bộ được cập nhật như mong đợi:

.. function:: getgeneratorlocals(generator)

   Lấy ánh xạ các biến cục bộ đang hoạt động trong *generator* tới các giá trị hiện tại của chúng. Một dictionary được trả về, ánh xạ từ tên biến tới giá trị. Đây tương đương với việc gọi :func:`locals` trong phần thân của generator, và mọi lưu ý tương tự đều được áp dụng.

   Nếu *generator* là một :term:`generator` không có frame liên kết hiện tại, một dictionary rỗng sẽ được trả về. :exc:`TypeError` được đưa ra nếu *generator* không phải là một đối tượng generator Python.

   .. impl-detail::

      Hàm này dựa vào việc generator cung cấp một stack frame Python để introspection, điều này không được đảm bảo trong mọi triển khai Python. Trong những trường hợp như vậy, hàm này sẽ luôn trả về một dictionary rỗng.

   .. versionadded:: 3.3

.. function:: getcoroutinelocals(coroutine)

   Hàm này tương tự như :func:`~inspect.getgeneratorlocals`, nhưng hoạt động với các đối tượng coroutine được tạo bởi các hàm :keyword:`async def`.

   .. versionadded:: 3.5

.. function:: getasyncgenlocals(agen)

   Hàm này tương tự như :func:`~inspect.getgeneratorlocals`, nhưng hoạt động với các đối tượng asynchronous generator được tạo bởi các hàm :keyword:`async def` sử dụng câu lệnh :keyword:`yield`.

   .. versionadded:: 3.12


.. _inspect-module-co-flags:

Các cờ bit của đối tượng code
-----------------------------

Các đối tượng code Python có thuộc tính :attr:`~codeobject.co_flags`, là một bitmap gồm các cờ sau:

.. data:: CO_OPTIMIZED

   Đối tượng code được tối ưu hóa, sử dụng các local nhanh.

.. data:: CO_NEWLOCALS

   Nếu được thiết lập, một dict mới sẽ được tạo cho :attr:`~frame.f_locals` của frame khi đối tượng code được thực thi.

.. data:: CO_VARARGS

   Đối tượng mã có một tham số vị trí biến đổi (tương tự ``*args``).

.. data:: CO_VARKEYWORDS

   Đối tượng mã có một tham số từ khóa biến đổi (tương tự ``**kwargs``).

.. data:: CO_NESTED

   Cờ được thiết lập khi đối tượng mã là một hàm lồng nhau.

.. data:: CO_GENERATOR

   Cờ được thiết lập khi đối tượng mã là một hàm generator, tức là một đối tượng generator được trả về khi đối tượng mã được thực thi.

.. data:: CO_COROUTINE

   Cờ được thiết lập khi đối tượng mã là một hàm coroutine. Khi đối tượng mã được thực thi, nó trả về một đối tượng coroutine. Xem :pep:`492` để biết thêm chi tiết.

   .. versionadded:: 3.5

.. data:: CO_ITERABLE_COROUTINE

   Cờ này được dùng để chuyển đổi generator thành coroutine dựa trên generator. Các đối tượng generator có cờ này có thể được dùng trong biểu thức ``await`` và có thể ``yield from`` các đối tượng coroutine. Xem :pep:`492` để biết thêm chi tiết.

   .. versionadded:: 3.5

.. data:: CO_ASYNC_GENERATOR

   Cờ được thiết lập khi đối tượng mã là một hàm generator bất đồng bộ. Khi đối tượng mã được thực thi, nó trả về một đối tượng generator bất đồng bộ. Xem :pep:`525` để biết thêm chi tiết.

   .. versionadded:: 3.6

.. data:: CO_HAS_DOCSTRING

   Cờ được thiết lập khi mã nguồn có docstring cho đối tượng mã. Nếu được thiết lập, đây sẽ là mục đầu tiên trong
   :attr:`~codeobject.co_consts`.

   .. versionadded:: 3.14

.. data:: CO_METHOD

   Cờ được thiết lập khi đối tượng mã là một hàm được định nghĩa trong phạm vi lớp.

   .. versionadded:: 3.14

.. note::
   Các cờ này dành riêng cho CPython và có thể không được định nghĩa trong các triển khai Python khác. Hơn nữa, các cờ này là một chi tiết triển khai và có thể bị loại bỏ hoặc ngừng hỗ trợ trong các bản phát hành Python trong tương lai. Bạn nên sử dụng các API công khai từ mô-đun :mod:`!inspect` cho mọi nhu cầu introspection.


Cờ buffer
---------

.. class:: BufferFlags

   Đây là một :class:`enum.IntFlag` đại diện cho các cờ có thể được truyền vào phương thức :meth:`~object.__buffer__` của các đối tượng triển khai :ref:`giao thức buffer <bufferobjects>`.

   Ý nghĩa của các cờ được giải thích tại :ref:`buffer-request-types`.

   .. attribute:: BufferFlags.SIMPLE
   .. attribute:: BufferFlags.WRITABLE
   .. attribute:: BufferFlags.FORMAT
   .. attribute:: BufferFlags.ND
   .. attribute:: BufferFlags.STRIDES
   .. attribute:: BufferFlags.C_CONTIGUOUS
   .. attribute:: BufferFlags.F_CONTIGUOUS
   .. attribute:: BufferFlags.ANY_CONTIGUOUS
   .. attribute:: BufferFlags.INDIRECT
   .. attribute:: BufferFlags.CONTIG
   .. attribute:: BufferFlags.CONTIG_RO
   .. attribute:: BufferFlags.STRIDED
   .. attribute:: BufferFlags.STRIDED_RO
   .. attribute:: BufferFlags.RECORDS
   .. attribute:: BufferFlags.RECORDS_RO
   .. attribute:: BufferFlags.FULL
   .. attribute:: BufferFlags.FULL_RO
   .. attribute:: BufferFlags.READ
   .. attribute:: BufferFlags.WRITE

   .. versionadded:: 3.12

.. _inspect-module-cli:

Giao diện dòng lệnh
-------------------

Mô-đun :mod:`!inspect` cũng cung cấp khả năng introspection cơ bản từ dòng lệnh.

.. program:: inspect

Theo mặc định, lệnh này nhận tên của một mô-đun và in mã nguồn của mô-đun đó. Có thể in một lớp hoặc hàm bên trong mô-đun bằng cách thêm dấu hai chấm và tên đầy đủ của đối tượng đích.

.. option:: --details

   In thông tin về đối tượng được chỉ định thay vì mã nguồn
