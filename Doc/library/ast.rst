:mod:`!ast` --- Cây cú pháp trừu tượng
======================================

.. module:: ast
   :synopsis: Các lớp và thao tác trên Cây cú pháp trừu tượng.

.. sectionauthor:: Martin v. Löwis <martin@v.loewis.de>
.. sectionauthor:: Georg Brandl <georg@python.org>

.. testsetup::

    import ast

**Mã nguồn:** :source:`Lib/ast.py`

--------------

Mô-đun :mod:`!ast` giúp các ứng dụng Python xử lý các cây của ngữ pháp cú pháp trừu tượng của Python. Bản thân cú pháp trừu tượng có thể thay đổi theo mỗi bản phát hành Python; mô-đun này giúp xác định bằng lập trình ngữ pháp hiện tại có dạng như thế nào.

Có thể tạo một cây cú pháp trừu tượng bằng cách truyền :data:`ast.PyCF_ONLY_AST` làm cờ cho hàm tích hợp :func:`compile`, hoặc sử dụng hàm trợ giúp :func:`parse` được cung cấp trong mô-đun này. Kết quả sẽ là một cây gồm các đối tượng mà lớp của chúng đều kế thừa từ :class:`ast.AST`. Có thể biên dịch một cây cú pháp trừu tượng thành đối tượng mã Python bằng hàm tích hợp :func:`compile`.


.. _abstract-grammar:

Ngữ pháp trừu tượng
-------------------

Ngữ pháp trừu tượng hiện được định nghĩa như sau:

.. literalinclude:: ../../Parser/Python.asdl
   :language: asdl


Các lớp node
------------

.. class:: AST

   Đây là lớp cơ sở của tất cả các lớp node AST. Các lớp node thực tế được dẫn xuất từ tệp :file:`Parser/Python.asdl`, tệp này được tái hiện
   :ref:`ở trên <abstract-grammar>`. Chúng được định nghĩa trong module C :mod:`!_ast` và được re-export trong :mod:`!ast`.

   Có một lớp được định nghĩa cho mỗi ký hiệu ở vế trái trong grammar trừu tượng (ví dụ: :class:`ast.stmt` hoặc :class:`ast.expr`). Ngoài ra, có một lớp được định nghĩa cho mỗi constructor ở vế phải; các lớp này kế thừa từ những lớp tương ứng với các cây ở vế trái. Ví dụ,
   :class:`ast.BinOp` kế thừa từ :class:`ast.expr`. Đối với các production rule có nhiều lựa chọn (còn gọi là "sums"), lớp ở vế trái là lớp trừu tượng: chỉ các instance của những node constructor cụ thể mới được tạo.

   .. index:: single: ? (question mark); in AST grammar
   .. index:: single: * (asterisk); in AST grammar

   .. attribute:: _fields

      Mỗi lớp cụ thể có một thuộc tính :attr:`!_fields` cho biết tên của tất cả node con.

      Mỗi instance của một lớp cụ thể có một thuộc tính cho mỗi node con, với kiểu được định nghĩa trong grammar. Ví dụ, các instance :class:`ast.BinOp` có một thuộc tính :attr:`left` thuộc kiểu :class:`ast.expr`.

      Nếu các thuộc tính này được đánh dấu là tùy chọn trong grammar (bằng dấu hỏi), giá trị có thể là ``None``. Nếu các thuộc tính có thể có từ không đến nhiều giá trị (được đánh dấu bằng dấu hoa thị), các giá trị sẽ được biểu diễn dưới dạng danh sách Python. Tất cả các thuộc tính có thể có phải hiện diện và có giá trị hợp lệ khi biên dịch AST bằng :func:`compile`.

   .. attribute:: _field_types

      Thuộc tính :attr:`!_field_types` trên mỗi lớp cụ thể là một dictionary ánh xạ tên trường (cũng được liệt kê trong :attr:`_fields`) với kiểu của chúng.

      .. doctest::

           >>> ast.TypeVar._field_types
           {'name': <class 'str'>, 'bound': ast.expr | None, 'default_value': ast.expr | None}

      .. versionadded:: 3.13

   .. attribute:: lineno
                  col_offset end_lineno end_col_offset

      Các instance của :class:`ast.expr` và các lớp con của :class:`ast.stmt` có
      các thuộc tính :attr:`lineno`, :attr:`col_offset`, :attr:`end_lineno`, và
      :attr:`end_col_offset`. :attr:`lineno` và :attr:`end_lineno` là số dòng đầu tiên và cuối cùng của phạm vi văn bản nguồn (được đánh số từ 1, nên dòng đầu tiên là dòng 1), còn :attr:`col_offset` và :attr:`end_col_offset` là các offset byte UTF-8 tương ứng của token đầu tiên và cuối cùng đã tạo ra node. Offset UTF-8 được ghi lại vì parser sử dụng UTF-8 internally.

      Lưu ý rằng vị trí kết thúc không bắt buộc đối với compiler và vì vậy là tùy chọn. Offset kết thúc nằm *sau* ký hiệu cuối cùng; chẳng hạn, bạn có thể lấy đoạn mã nguồn của một node biểu thức một dòng bằng ``source_line[node.col_offset : node.end_col_offset]``.

   Constructor của một lớp :class:`ast.T` phân tích các đối số như sau:

   * Nếu có các đối số vị trí, số lượng phải bằng số lượng mục trong :attr:`T._fields`; chúng sẽ được gán làm các thuộc tính với những tên này.
   * Nếu có các đối số từ khóa, chúng sẽ đặt các thuộc tính có cùng tên thành các giá trị được cung cấp.

   Ví dụ, để tạo và điền dữ liệu cho một node :class:`ast.UnaryOp`, bạn có thể dùng::

      node = ast.UnaryOp(ast.USub(), ast.Constant(5, lineno=0, col_offset=0),
                         lineno=0, col_offset=0)

   Nếu một trường tùy chọn trong grammar bị bỏ qua khi gọi constructor, nó mặc định là ``None``. Nếu một trường dạng danh sách bị bỏ qua, nó mặc định là danh sách rỗng. Nếu một trường có kiểu :class:`!ast.expr_context` bị bỏ qua, nó mặc định là
   :class:`Load() <ast.Load>`. Nếu bất kỳ trường nào khác bị bỏ qua, một :exc:`DeprecationWarning` sẽ được raised và node AST sẽ không có trường này. Trong Python 3.15, điều kiện này sẽ gây ra lỗi.

.. versionchanged:: 3.8

   Lớp :class:`ast.Constant` hiện được dùng cho tất cả các hằng số.

.. versionchanged:: 3.9

   Các chỉ số đơn được biểu diễn bằng giá trị của chúng, còn các lát cắt mở rộng được biểu diễn dưới dạng tuple.

.. versionchanged:: 3.13

    Các hàm khởi tạo node AST đã được thay đổi để cung cấp các giá trị mặc định hợp lý cho những trường bị bỏ qua: các trường tùy chọn giờ mặc định là ``None``, các trường dạng danh sách mặc định là một danh sách rỗng, còn các trường có kiểu :class:`!ast.expr_context` mặc định là
    :class:`Load() <ast.Load>`. Trước đây, các thuộc tính bị bỏ qua sẽ không tồn tại trên các node được khởi tạo (việc truy cập chúng sẽ gây ra :exc:`AttributeError`).

.. versionchanged:: 3.14

    Đầu ra :meth:`~object.__repr__` của các node :class:`~ast.AST` bao gồm các giá trị của các trường trong node.

.. deprecated-removed:: 3.8 3.14

   Các phiên bản Python trước đây cung cấp các lớp AST :class:`!ast.Num`,
   :class:`!ast.Str`, :class:`!ast.Bytes`, :class:`!ast.NameConstant` và
   :class:`!ast.Ellipsis`, vốn đã bị loại bỏ dần trong Python 3.8. Các lớp này đã bị xóa trong Python 3.14 và chức năng của chúng đã được thay thế bằng
   :class:`ast.Constant`.

.. deprecated:: 3.9

   Các class cũ :class:`!ast.Index` và :class:`!ast.ExtSlice` vẫn khả dụng, nhưng sẽ bị loại bỏ trong các bản phát hành Python sau này. Trong thời gian đó, việc khởi tạo chúng sẽ trả về một instance của class khác.

.. deprecated-removed:: 3.13 3.15

   Các phiên bản Python trước đây cho phép tạo các node AST bị thiếu những trường bắt buộc. Tương tự, các hàm khởi tạo node AST cho phép truyền các đối số từ khóa tùy ý, rồi đặt chúng làm thuộc tính của node AST, ngay cả khi chúng không khớp với bất kỳ trường nào của node AST. Hành vi này đã lỗi thời và sẽ bị loại bỏ trong Python 3.15.

.. note::
    Phần mô tả các class node cụ thể được hiển thị ở đây ban đầu được chuyển thể từ dự án `Green Tree Snakes <https://greentreesnakes.readthedocs.io/en/latest/>`__ tuyệt vời cùng tất cả những người đóng góp cho dự án.


.. _ast-root-nodes:

Các node gốc
^^^^^^^^^^^^

.. class:: Module(body, type_ignores)

   Một module Python, tương tự như :ref:`file input <file-input>`. Kiểu node được tạo bởi :func:`ast.parse` trong ``"exec"`` *mode* mặc định.

   ``body`` là một :class:`list` của :ref:`ast-statements` trong module.

   ``type_ignores`` là một :class:`list` của các chú thích bỏ qua kiểu trong module; xem :func:`ast.parse` để biết thêm chi tiết.

   .. doctest::

        >>> print(ast.dump(ast.parse('x = 1'), indent=4))
        Module(
            body=[
                Assign(
                    targets=[
                        Name(id='x', ctx=Store())],
                    value=Constant(value=1))])


.. class:: Expression(body)

   Một :ref:`đầu vào biểu thức <expression-input>` Python duy nhất. Loại nút được tạo bởi :func:`ast.parse` khi *chế độ* là ``"eval"``.

   ``body`` là một nút duy nhất, thuộc một trong các :ref:`kiểu biểu thức <ast-expressions>`.

   .. doctest::

        >>> print(ast.dump(ast.parse('123', mode='eval'), indent=4))
        Expression(
            body=Constant(value=123))


.. class:: Interactive(body)

   Một :ref:`đầu vào tương tác <interactive>` duy nhất, như trong :ref:`tut-interac`. Loại nút được tạo bởi :func:`ast.parse` khi *chế độ* là ``"single"``.

   ``body`` là một :class:`list` gồm :ref:`các nút câu lệnh <ast-statements>`.

   .. doctest::

        >>> print(ast.dump(ast.parse('x = 1; y = 2', mode='single'), indent=4))
        Interactive(
            body=[
                Assign(
                    targets=[
                        Name(id='x', ctx=Store())],
                    value=Constant(value=1)),
                Assign(
                    targets=[
                        Name(id='y', ctx=Store())],
                    value=Constant(value=2))])


.. class:: FunctionType(argtypes, returns)

   Biểu diễn các chú thích kiểu cũ cho hàm, vì các phiên bản Python trước 3.5 không hỗ trợ :pep:`484` annotation. Loại nút được tạo bởi :func:`ast.parse` khi *chế độ* là ``"func_type"``.

   Các chú thích kiểu như vậy sẽ có dạng sau::

       def sum_two_number(a, b):
           # type: (int, int) -> int
           return a + b

   ``argtypes`` là một :class:`list` của :ref:`các nút biểu thức <ast-expressions>`.

   ``returns`` là một :ref:`nút biểu thức <ast-expressions>` duy nhất.

   .. doctest::

        >>> print(ast.dump(ast.parse('(int, str) -> List[int]', mode='func_type'), indent=4))
        FunctionType(
            argtypes=[
                Name(id='int', ctx=Load()),
                Name(id='str', ctx=Load())],
            returns=Subscript(
                value=Name(id='List', ctx=Load()),
                slice=Name(id='int', ctx=Load()),
                ctx=Load()))

   .. versionadded:: 3.8


Literal
^^^^^^^

.. class:: Constant(value, kind)

   Một giá trị hằng số. Thuộc tính ``value`` của literal ``Constant`` chứa đối tượng Python mà nó biểu diễn. Các giá trị được biểu diễn có thể là các thực thể của :class:`str`,
   :class:`bytes`, :class:`int`, :class:`float`, :class:`complex`, và :class:`bool`, cũng như các hằng số :data:`None` và :data:`Ellipsis`.

   Thuộc tính ``kind`` là một chuỗi tùy chọn. Đối với các literal chuỗi có tiền tố ``u``, ``kind`` được đặt thành ``'u'``. Đối với mọi hằng số khác, ``kind`` là ``None``.

   .. doctest::

        >>> print(ast.dump(ast.parse('123', mode='eval'), indent=4))
        Expression(
            body=Constant(value=123))
        >>> print(ast.dump(ast.parse("u'hello'", mode='eval'), indent=4))
        Expression(
            body=Constant(value='hello', kind='u'))


.. class:: FormattedValue(value, conversion, format_spec)

   Nút biểu diễn một trường định dạng duy nhất trong f-string. Nếu chuỗi chỉ chứa một trường định dạng duy nhất và không có gì khác, nút này có thể được tách riêng; nếu không, nó xuất hiện trong :class:`JoinedStr`.

   * ``value`` là bất kỳ nút biểu thức nào (chẳng hạn như literal, biến hoặc lệnh gọi hàm).
   * ``conversion`` là một số nguyên:

     * -1: không định dạng
     * 97 (``ord('a')``): định dạng ``!a`` :func:`ASCII <ascii>`
     * 114 (``ord('r')``): định dạng ``!r`` :func:`repr`
     * 115 (``ord('s')``): định dạng ``!s`` :func:`string <str>`

   * ``format_spec`` là một nút :class:`JoinedStr` biểu thị cách định dạng giá trị, hoặc ``None`` nếu không chỉ định định dạng. Cả ``conversion`` và ``format_spec`` đều có thể được đặt cùng lúc.


.. class:: JoinedStr(values)

   Một f-string, gồm một chuỗi các nút :class:`FormattedValue` và :class:`Constant`.

   .. doctest::

        >>> print(ast.dump(ast.parse('f"sin({a}) is {sin(a):.3}"', mode='eval'), indent=4))
        Expression(
            body=JoinedStr(
                values=[
                    Constant(value='sin('),
                    FormattedValue(
                        value=Name(id='a', ctx=Load()),
                        conversion=-1),
                    Constant(value=') is '),
                    FormattedValue(
                        value=Call(
                            func=Name(id='sin', ctx=Load()),
                            args=[
                                Name(id='a', ctx=Load())]),
                        conversion=-1,
                        format_spec=JoinedStr(
                            values=[
                                Constant(value='.3')]))]))


.. class:: TemplateStr(values, /)

   .. versionadded:: 3.14

   Nút đại diện cho một template string literal, gồm một chuỗi các
   nút :class:`Interpolation` và :class:`Constant`. Các nút này có thể xuất hiện theo bất kỳ thứ tự nào và không cần được xen kẽ.

   .. doctest::

        >>> expr = ast.parse('t"{name} finished {place:ordinal}"', mode='eval')
        >>> print(ast.dump(expr, indent=4))
        Expression(
            body=TemplateStr(
                values=[
                    Interpolation(
                        value=Name(id='name', ctx=Load()),
                        str='name',
                        conversion=-1),
                    Constant(value=' finished '),
                    Interpolation(
                        value=Name(id='place', ctx=Load()),
                        str='place',
                        conversion=-1,
                        format_spec=JoinedStr(
                            values=[
                                Constant(value='ordinal')]))]))

.. class:: Interpolation(value, str, conversion, format_spec=None)

   .. versionadded:: 3.14

   Nút đại diện cho một trường nội suy riêng lẻ trong một template string literal.

   * ``value`` là bất kỳ nút biểu thức nào (chẳng hạn như một literal, một biến hoặc một lệnh gọi hàm). Điều này có cùng ý nghĩa với ``FormattedValue.value``.
   * ``str`` là một hằng số chứa văn bản của biểu thức nội suy.

     Nếu ``str`` được đặt thành ``None``, thì ``value`` được dùng để tạo mã khi gọi :func:`ast.unparse`. Điều này không còn đảm bảo mã được tạo giống hệt mã ban đầu và được dùng cho việc tạo mã.
   * ``conversion`` là một số nguyên:

     * -1: không chuyển đổi
     * 97 (``ord('a')``): ``!a`` :func:`ASCII <ascii>` chuyển đổi
     * 114 (``ord('r')``): ``!r`` :func:`repr` chuyển đổi
     * 115 (``ord('s')``): ``!s`` :func:`string <str>` chuyển đổi

     Điều này có cùng ý nghĩa với ``FormattedValue.conversion``.
   * ``format_spec`` là một node :class:`JoinedStr` đại diện cho định dạng của giá trị, hoặc ``None`` nếu không chỉ định định dạng. Cả ``conversion`` và ``format_spec`` đều có thể được đặt cùng lúc. Điều này có cùng ý nghĩa với ``FormattedValue.format_spec``.


.. class:: List(elts, ctx)
           Tuple(elts, ctx)

   Một list hoặc tuple. ``elts`` chứa một danh sách các node biểu diễn các phần tử. ``ctx`` là :class:`Store` nếu container là đích gán (tức là ``(x,y)=something``), và là :class:`Load` trong các trường hợp còn lại.

   .. doctest::

        >>> print(ast.dump(ast.parse('[1, 2, 3]', mode='eval'), indent=4))
        Expression(
            body=List(
                elts=[
                    Constant(value=1),
                    Constant(value=2),
                    Constant(value=3)],
                ctx=Load()))
        >>> print(ast.dump(ast.parse('(1, 2, 3)', mode='eval'), indent=4))
        Expression(
            body=Tuple(
                elts=[
                    Constant(value=1),
                    Constant(value=2),
                    Constant(value=3)],
                ctx=Load()))


.. class:: Set(elts)

   Một set. ``elts`` chứa một danh sách các node biểu diễn các phần tử của set.

   .. doctest::

        >>> print(ast.dump(ast.parse('{1, 2, 3}', mode='eval'), indent=4))
        Expression(
            body=Set(
                elts=[
                    Constant(value=1),
                    Constant(value=2),
                    Constant(value=3)]))


.. class:: Dict(keys, values)

   Một dictionary. ``keys`` và ``values`` chứa các danh sách node biểu diễn các key và value tương ứng, theo đúng thứ tự (những gì sẽ được trả về khi gọi :code:`dictionary.keys()` và :code:`dictionary.values()`).

   Khi thực hiện dictionary unpacking bằng dictionary literal, biểu thức cần mở rộng được đặt trong danh sách ``values``, với một ``None`` ở vị trí tương ứng trong ``keys``.

   .. doctest::

        >>> print(ast.dump(ast.parse('{"a":1, **d}', mode='eval'), indent=4))
        Expression(
            body=Dict(
                keys=[
                    Constant(value='a'),
                    None],
                values=[
                    Constant(value=1),
                    Name(id='d', ctx=Load())]))


Biến
^^^^

.. class:: Name(id, ctx)

   Tên biến. ``id`` chứa tên dưới dạng một chuỗi, còn ``ctx`` là một trong các kiểu sau.


.. class:: Load()
           Store() Del()

   Tham chiếu biến có thể được dùng để tải giá trị của một biến, gán giá trị mới cho biến đó hoặc xóa biến đó. Tham chiếu biến được cung cấp một ngữ cảnh để phân biệt các trường hợp này.

   .. doctest::

        >>> print(ast.dump(ast.parse('a'), indent=4))
        Module(
            body=[
                Expr(
                    value=Name(id='a', ctx=Load()))])

        >>> print(ast.dump(ast.parse('a = 1'), indent=4))
        Module(
            body=[
                Assign(
                    targets=[
                        Name(id='a', ctx=Store())],
                    value=Constant(value=1))])

        >>> print(ast.dump(ast.parse('del a'), indent=4))
        Module(
            body=[
                Delete(
                    targets=[
                        Name(id='a', ctx=Del())])])


.. class:: Starred(value, ctx)

   Một tham chiếu biến ``*var``. ``value`` chứa biến, thường là một
   node :class:`Name`. Kiểu này phải được sử dụng khi xây dựng một node :class:`Call` bằng ``*args``.

   .. doctest::

        >>> print(ast.dump(ast.parse('a, *b = it'), indent=4))
        Module(
            body=[
                Assign(
                    targets=[
                        Tuple(
                            elts=[
                                Name(id='a', ctx=Store()),
                                Starred(
                                    value=Name(id='b', ctx=Store()),
                                    ctx=Store())],
                            ctx=Store())],
                    value=Name(id='it', ctx=Load()))])


.. _ast-expressions:

Biểu thức
^^^^^^^^^

.. class:: Expr(value)

   Khi một biểu thức, chẳng hạn như một lệnh gọi hàm, xuất hiện độc lập dưới dạng một câu lệnh nhưng giá trị trả về của nó không được sử dụng hoặc lưu trữ, biểu thức đó được bọc trong container này. ``value`` chứa một trong các node khác trong phần này, một :class:`Constant`, một
   :class:`Name`, một :class:`Lambda`, một :class:`Yield` hoặc node :class:`YieldFrom`.

   .. doctest::

        >>> print(ast.dump(ast.parse('-a'), indent=4))
        Module(
            body=[
                Expr(
                    value=UnaryOp(
                        op=USub(),
                        operand=Name(id='a', ctx=Load())))])


.. class:: UnaryOp(op, operand)

   Một phép toán một ngôi. ``op`` là toán tử, còn ``operand`` là một nút biểu thức bất kỳ.


.. class:: UAdd
           USub Not Invert

   Các token toán tử một ngôi. :class:`Not` là từ khóa ``not``, còn :class:`Invert` là toán tử ``~``.

   .. doctest::

        >>> print(ast.dump(ast.parse('not x', mode='eval'), indent=4))
        Expression(
            body=UnaryOp(
                op=Not(),
                operand=Name(id='x', ctx=Load())))


.. class:: BinOp(left, op, right)

   Một phép toán hai ngôi (chẳng hạn phép cộng hoặc phép chia). ``op`` là toán tử, còn ``left`` và ``right`` là các nút biểu thức bất kỳ.

   .. doctest::

        >>> print(ast.dump(ast.parse('x + y', mode='eval'), indent=4))
        Expression(
            body=BinOp(
                left=Name(id='x', ctx=Load()),
                op=Add(),
                right=Name(id='y', ctx=Load())))


.. class:: Add
           Sub Mult Div FloorDiv Mod Pow LShift RShift BitOr BitXor BitAnd MatMult

   Các token toán tử hai ngôi.


.. class:: BoolOp(op, values)

   Một phép toán Boolean, 'or' hoặc 'and'. ``op`` là :class:`Or` hoặc :class:`And`. ``values`` là các giá trị liên quan. Các phép toán liên tiếp có cùng toán tử, chẳng hạn như ``a or b or c``, được gộp thành một nút với nhiều giá trị.

   Điều này không bao gồm ``not``, vốn là một :class:`UnaryOp`.

   .. doctest::

        >>> print(ast.dump(ast.parse('x or y', mode='eval'), indent=4))
        Expression(
            body=BoolOp(
                op=Or(),
                values=[
                    Name(id='x', ctx=Load()),
                    Name(id='y', ctx=Load())]))


.. class:: And
           Hoặc

   Các token toán tử Boolean.


.. class:: Compare(left, ops, comparators)

   Phép so sánh hai hoặc nhiều giá trị. ``left`` là giá trị đầu tiên trong phép so sánh, ``ops`` là danh sách các toán tử, còn ``comparators`` là danh sách các giá trị sau phần tử đầu tiên trong phép so sánh.

   .. doctest::

        >>> print(ast.dump(ast.parse('1 <= a < 10', mode='eval'), indent=4))
        Expression(
            body=Compare(
                left=Constant(value=1),
                ops=[
                    LtE(),
                    Lt()],
                comparators=[
                    Name(id='a', ctx=Load()),
                    Constant(value=10)]))


.. class:: Eq
           NotEq Lt LtE Gt GtE Is IsNot In NotIn

   Các token toán tử so sánh.


.. class:: Call(func, args, keywords)

   Một lời gọi hàm. ``func`` là hàm, thường sẽ là một
   đối tượng :class:`Name` hoặc :class:`Attribute`. Trong số các đối số:

   * ``args`` chứa một danh sách các đối số được truyền theo vị trí.
   * ``keywords`` chứa một danh sách các đối tượng :class:`.keyword` đại diện cho các đối số được truyền theo từ khóa.

   Các đối số ``args`` và ``keywords`` là tùy chọn và mặc định là các danh sách rỗng.

   .. doctest::

        >>> print(ast.dump(ast.parse('func(a, b=c, *d, **e)', mode='eval'), indent=4))
        Expression(
            body=Call(
                func=Name(id='func', ctx=Load()),
                args=[
                    Name(id='a', ctx=Load()),
                    Starred(
                        value=Name(id='d', ctx=Load()),
                        ctx=Load())],
                keywords=[
                    keyword(
                        arg='b',
                        value=Name(id='c', ctx=Load())),
                    keyword(
                        value=Name(id='e', ctx=Load()))]))


.. class:: keyword(arg, value)

   Một đối số từ khóa trong lệnh gọi hàm hoặc định nghĩa lớp. ``arg`` là một chuỗi thô chứa tên tham số, còn ``value`` là một node cần truyền vào.


.. class:: IfExp(test, body, orelse)

   Một biểu thức như ``a if b else c``. Mỗi trường chứa một node duy nhất, vì vậy trong ví dụ sau, cả ba đều là các node :class:`Name`.

   .. doctest::

        >>> print(ast.dump(ast.parse('a if b else c', mode='eval'), indent=4))
        Expression(
            body=IfExp(
                test=Name(id='b', ctx=Load()),
                body=Name(id='a', ctx=Load()),
                orelse=Name(id='c', ctx=Load())))


.. class:: Attribute(value, attr, ctx)

   Truy cập thuộc tính, ví dụ ``d.keys``. ``value`` là một node, thường là một
   :class:`Name`. ``attr`` là một chuỗi thuần chứa tên của thuộc tính, còn ``ctx`` là :class:`Load`, :class:`Store` hoặc :class:`Del` tùy theo cách thuộc tính được thao tác.

   .. doctest::

        >>> print(ast.dump(ast.parse('snake.colour', mode='eval'), indent=4))
        Expression(
            body=Attribute(
                value=Name(id='snake', ctx=Load()),
                attr='colour',
                ctx=Load()))


.. class:: NamedExpr(target, value)

   Một biểu thức có tên. Nút AST này được tạo bởi toán tử biểu thức gán (còn gọi là toán tử walrus). Khác với nút :class:`Assign`, trong đó đối số đầu tiên có thể gồm nhiều nút, trong trường hợp này cả ``target`` và ``value`` đều phải là các nút đơn.

   .. doctest::

        >>> print(ast.dump(ast.parse('(x := 4)', mode='eval'), indent=4))
        Expression(
            body=NamedExpr(
                target=Name(id='x', ctx=Store()),
                value=Constant(value=4)))

   .. versionadded:: 3.8

Lập chỉ mục
~~~~~~~~~~~

.. class:: Subscript(value, slice, ctx)

   Một chỉ mục con, chẳng hạn như ``l[1]``. ``value`` là đối tượng được lập chỉ mục con (thường là sequence hoặc mapping). ``slice`` là một chỉ mục, lát cắt hoặc khóa. Nó có thể là một :class:`Tuple` và chứa một :class:`Slice`. ``ctx`` là :class:`Load`, :class:`Store` hoặc :class:`Del` tùy theo thao tác được thực hiện với chỉ mục con.

   .. doctest::

        >>> print(ast.dump(ast.parse('l[1:2, 3]', mode='eval'), indent=4))
        Expression(
            body=Subscript(
                value=Name(id='l', ctx=Load()),
                slice=Tuple(
                    elts=[
                        Slice(
                            lower=Constant(value=1),
                            upper=Constant(value=2)),
                        Constant(value=3)],
                    ctx=Load()),
                ctx=Load()))


.. class:: Slice(lower, upper, step)

   Lát cắt thông thường (có dạng ``lower:upper`` hoặc ``lower:upper:step``). Chỉ có thể xuất hiện bên trong trường *slice* của :class:`Subscript`, trực tiếp hoặc dưới dạng một phần tử của :class:`Tuple`.

   .. doctest::

        >>> print(ast.dump(ast.parse('l[1:2]', mode='eval'), indent=4))
        Expression(
            body=Subscript(
                value=Name(id='l', ctx=Load()),
                slice=Slice(
                    lower=Constant(value=1),
                    upper=Constant(value=2)),
                ctx=Load()))


Biểu thức tạo
~~~~~~~~~~~~~

.. class:: ListComp(elt, generators)
           SetComp(elt, generators) GeneratorExp(elt, generators) DictComp(key, value, generators)

   Các phép comprehension của list và set, các biểu thức generator và các phép comprehension của dictionary. ``elt`` (hoặc ``key`` và ``value``) là một node duy nhất biểu diễn phần sẽ được đánh giá cho từng item.

   ``generators`` là một danh sách các node :class:`comprehension`.

   .. doctest::

        >>> print(ast.dump(
        ...     ast.parse('[x for x in numbers]', mode='eval'),
        ...     indent=4,
        ... ))
        Expression(
            body=ListComp(
                elt=Name(id='x', ctx=Load()),
                generators=[
                    comprehension(
                        target=Name(id='x', ctx=Store()),
                        iter=Name(id='numbers', ctx=Load()),
                        is_async=0)]))
        >>> print(ast.dump(
        ...     ast.parse('{x: x**2 for x in numbers}', mode='eval'),
        ...     indent=4,
        ... ))
        Expression(
            body=DictComp(
                key=Name(id='x', ctx=Load()),
                value=BinOp(
                    left=Name(id='x', ctx=Load()),
                    op=Pow(),
                    right=Constant(value=2)),
                generators=[
                    comprehension(
                        target=Name(id='x', ctx=Store()),
                        iter=Name(id='numbers', ctx=Load()),
                        is_async=0)]))
        >>> print(ast.dump(
        ...     ast.parse('{x for x in numbers}', mode='eval'),
        ...     indent=4,
        ... ))
        Expression(
            body=SetComp(
                elt=Name(id='x', ctx=Load()),
                generators=[
                    comprehension(
                        target=Name(id='x', ctx=Store()),
                        iter=Name(id='numbers', ctx=Load()),
                        is_async=0)]))


.. class:: comprehension(target, iter, ifs, is_async)

   Một mệnh đề ``for`` trong một phép comprehension. ``target`` là tham chiếu được sử dụng cho từng phần tử - thường là một node :class:`Name` hoặc :class:`Tuple`. ``iter`` là đối tượng cần lặp qua. ``ifs`` là danh sách các biểu thức kiểm tra: mỗi mệnh đề ``for`` có thể có nhiều ``ifs``.

   ``is_async`` cho biết một phép comprehension là bất đồng bộ (async), sử dụng một ``async for`` thay vì ``for``. Giá trị là một số nguyên (0 hoặc 1).

   .. doctest::

        >>> print(ast.dump(ast.parse('[ord(c) for line in file for c in line]', mode='eval'),
        ...                indent=4)) # Nhiều phép comprehension trong một phép.
        Expression(
            body=ListComp(
                elt=Call(
                    func=Name(id='ord', ctx=Load()),
                    args=[
                        Name(id='c', ctx=Load())]),
                generators=[
                    comprehension(
                        target=Name(id='line', ctx=Store()),
                        iter=Name(id='file', ctx=Load()),
                        is_async=0),
                    comprehension(
                        target=Name(id='c', ctx=Store()),
                        iter=Name(id='line', ctx=Load()),
                        is_async=0)]))

        >>> print(ast.dump(ast.parse('(n**2 for n in it if n>5 if n<10)', mode='eval'),
        ...                indent=4)) # phép comprehension của generator
        Expression(
            body=GeneratorExp(
                elt=BinOp(
                    left=Name(id='n', ctx=Load()),
                    op=Pow(),
                    right=Constant(value=2)),
                generators=[
                    comprehension(
                        target=Name(id='n', ctx=Store()),
                        iter=Name(id='it', ctx=Load()),
                        ifs=[
                            Compare(
                                left=Name(id='n', ctx=Load()),
                                ops=[
                                    Gt()],
                                comparators=[
                                    Constant(value=5)]),
                            Compare(
                                left=Name(id='n', ctx=Load()),
                                ops=[
                                    Lt()],
                                comparators=[
                                    Constant(value=10)])],
                        is_async=0)]))

        >>> print(ast.dump(ast.parse('[i async for i in soc]', mode='eval'),
        ...                indent=4)) # Phép comprehension bất đồng bộ
        Expression(
            body=ListComp(
                elt=Name(id='i', ctx=Load()),
                generators=[
                    comprehension(
                        target=Name(id='i', ctx=Store()),
                        iter=Name(id='soc', ctx=Load()),
                        is_async=1)]))


.. _ast-statements:

Câu lệnh
^^^^^^^^

.. class:: Assign(targets, value, type_comment)

   Một phép gán. ``targets`` là danh sách các node, còn ``value`` là một node duy nhất.

   Nhiều node trong ``targets`` biểu thị việc gán cùng một giá trị cho từng node. Việc giải nén được biểu thị bằng cách đặt một :class:`Tuple` hoặc :class:`List` bên trong ``targets``.

   .. attribute:: type_comment

       ``type_comment`` là một chuỗi tùy chọn chứa chú thích kiểu dưới dạng comment.

   .. doctest::

        >>> print(ast.dump(ast.parse('a = b = 1'), indent=4)) # Gán nhiều biến
        Module(
            body=[
                Assign(
                    targets=[
                        Name(id='a', ctx=Store()),
                        Name(id='b', ctx=Store())],
                    value=Constant(value=1))])

        >>> print(ast.dump(ast.parse('a,b = c'), indent=4)) # Giải nén
        Module(
            body=[
                Assign(
                    targets=[
                        Tuple(
                            elts=[
                                Name(id='a', ctx=Store()),
                                Name(id='b', ctx=Store())],
                            ctx=Store())],
                    value=Name(id='c', ctx=Load()))])


.. class:: AnnAssign(target, annotation, value, simple)

   Một phép gán có chú thích kiểu. ``target`` là một node duy nhất và có thể là :class:`Name`, :class:`Attribute` hoặc :class:`Subscript`. ``annotation`` là chú thích, chẳng hạn như node :class:`Constant` hoặc :class:`Name`. ``value`` là một node tùy chọn duy nhất.

   ``simple`` luôn là 0 (cho biết target “complex”) hoặc 1 (cho biết target “simple”). Target “simple” chỉ bao gồm một
   :class:`Name` node không xuất hiện giữa các dấu ngoặc đơn; mọi target khác đều được xem là complex. Chỉ các target simple mới xuất hiện trong từ điển :attr:`~object.__annotations__` của các module và class.

   .. doctest::

        >>> print(ast.dump(ast.parse('c: int'), indent=4))
        Module(
            body=[
                AnnAssign(
                    target=Name(id='c', ctx=Store()),
                    annotation=Name(id='int', ctx=Load()),
                    simple=1)])

        >>> print(ast.dump(ast.parse('(a): int = 1'), indent=4)) # Annotation có dấu ngoặc đơn
        Module(
            body=[
                AnnAssign(
                    target=Name(id='a', ctx=Store()),
                    annotation=Name(id='int', ctx=Load()),
                    value=Constant(value=1),
                    simple=0)])

        >>> print(ast.dump(ast.parse('a.b: int'), indent=4)) # Annotation thuộc tính
        Module(
            body=[
                AnnAssign(
                    target=Attribute(
                        value=Name(id='a', ctx=Load()),
                        attr='b',
                        ctx=Store()),
                    annotation=Name(id='int', ctx=Load()),
                    simple=0)])

        >>> print(ast.dump(ast.parse('a[1]: int'), indent=4)) # Annotation chỉ mục
        Module(
            body=[
                AnnAssign(
                    target=Subscript(
                        value=Name(id='a', ctx=Load()),
                        slice=Constant(value=1),
                        ctx=Store()),
                    annotation=Name(id='int', ctx=Load()),
                    simple=0)])


.. class:: AugAssign(target, op, value)

   Phép gán tăng cường, chẳng hạn như ``a += 1``. Trong ví dụ sau, ``target`` là một node :class:`Name` cho ``x`` (với ngữ cảnh :class:`Store`), ``op`` là :class:`Add`, còn ``value`` là một :class:`Constant` có giá trị là 1.

   Thuộc tính ``target`` không thể thuộc class :class:`Tuple` hoặc :class:`List`, khác với các target của :class:`Assign`.

   .. doctest::

        >>> print(ast.dump(ast.parse('x += 2'), indent=4))
        Module(
            body=[
                AugAssign(
                    target=Name(id='x', ctx=Store()),
                    op=Add(),
                    value=Constant(value=2))])


.. class:: Raise(exc, cause)

   Một câu lệnh ``raise``. ``exc`` là đối tượng ngoại lệ sẽ được raise, thường là một
   :class:`Call` hoặc :class:`Name`, hoặc ``None`` đối với một ``raise`` độc lập. ``cause`` là phần tùy chọn cho ``y`` trong ``raise x from y``.

   .. doctest::

        >>> print(ast.dump(ast.parse('raise x from y'), indent=4))
        Module(
            body=[
                Raise(
                    exc=Name(id='x', ctx=Load()),
                    cause=Name(id='y', ctx=Load()))])


.. class:: Assert(test, msg)

   Một phép assert. ``test`` chứa điều kiện, chẳng hạn như một nút :class:`Compare`. ``msg`` chứa thông báo lỗi.

   .. doctest::

        >>> print(ast.dump(ast.parse('assert x,y'), indent=4))
        Module(
            body=[
                Assert(
                    test=Name(id='x', ctx=Load()),
                    msg=Name(id='y', ctx=Load()))])


.. class:: Delete(targets)

   Biểu diễn một câu lệnh ``del``. ``targets`` là danh sách các nút, chẳng hạn như
   các nút :class:`Name`, :class:`Attribute` hoặc :class:`Subscript`.

   .. doctest::

        >>> print(ast.dump(ast.parse('del x,y,z'), indent=4))
        Module(
            body=[
                Delete(
                    targets=[
                        Name(id='x', ctx=Del()),
                        Name(id='y', ctx=Del()),
                        Name(id='z', ctx=Del())])])


.. class:: Pass()

   Một câu lệnh ``pass``.

   .. doctest::

        >>> print(ast.dump(ast.parse('pass'), indent=4))
        Module(
            body=[
                Pass()])


.. class:: TypeAlias(name, type_params, value)

   Một :ref:`bí danh kiểu <type-aliases>` được tạo thông qua câu lệnh :keyword:`type`. ``name`` là tên của bí danh, ``type_params`` là một danh sách các
   :ref:`tham số kiểu <ast-type-params>`, và ``value`` là giá trị của bí danh kiểu.

   .. doctest::

        >>> print(ast.dump(ast.parse('type Alias = int'), indent=4))
        Module(
            body=[
                TypeAlias(
                    name=Name(id='Alias', ctx=Store()),
                    value=Name(id='int', ctx=Load()))])

   .. versionadded:: 3.12

Các câu lệnh khác chỉ áp dụng bên trong hàm hoặc vòng lặp được mô tả trong các phần khác.

Các câu lệnh import
~~~~~~~~~~~~~~~~~~~

.. class:: Import(names)

   Một câu lệnh import. ``names`` là danh sách các nút :class:`alias`.

   .. doctest::

        >>> print(ast.dump(ast.parse('import x,y,z'), indent=4))
        Module(
            body=[
                Import(
                    names=[
                        alias(name='x'),
                        alias(name='y'),
                        alias(name='z')])])


.. class:: ImportFrom(module, names, level)

   Biểu diễn ``from x import y``. ``module`` là một chuỗi thô chứa tên 'from', không có dấu chấm ở đầu, hoặc ``None`` đối với các câu lệnh như ``from . import foo``. ``level`` là một số nguyên chứa cấp độ của import tương đối (0 nghĩa là import tuyệt đối).

   .. doctest::

        >>> print(ast.dump(ast.parse('from y import x,y,z'), indent=4))
        Module(
            body=[
                ImportFrom(
                    module='y',
                    names=[
                        alias(name='x'),
                        alias(name='y'),
                        alias(name='z')],
                    level=0)])


.. class:: alias(name, asname)

   Cả hai tham số đều là các chuỗi thô chứa tên. ``asname`` có thể là ``None`` nếu sử dụng tên thông thường.

   .. doctest::

        >>> print(ast.dump(ast.parse('from ..foo.bar import a as b, c'), indent=4))
        Module(
            body=[
                ImportFrom(
                    module='foo.bar',
                    names=[
                        alias(name='a', asname='b'),
                        alias(name='c')],
                    level=2)])

Luồng điều khiển
^^^^^^^^^^^^^^^^

.. note::
   Các mệnh đề tùy chọn như ``else`` được lưu dưới dạng danh sách rỗng nếu chúng không xuất hiện.

.. class:: If(test, body, orelse)

   Một câu lệnh ``if``. ``test`` chứa một nút duy nhất, chẳng hạn như nút :class:`Compare`. ``body`` và ``orelse`` mỗi phần đều chứa một danh sách các nút.

   Các mệnh đề ``elif`` không có biểu diễn riêng trong AST, mà xuất hiện dưới dạng các nút :class:`If` bổ sung bên trong phần ``orelse`` của mệnh đề trước đó.

   .. doctest::

        >>> print(ast.dump(ast.parse("""
        ... if x:
        ...    ...
        ... elif y:
        ...    ...
        ... else:
        ...    ...
        ... """), indent=4))
        Module(
            body=[
                If(
                    test=Name(id='x', ctx=Load()),
                    body=[
                        Expr(
                            value=Constant(value=Ellipsis))],
                    orelse=[
                        If(
                            test=Name(id='y', ctx=Load()),
                            body=[
                                Expr(
                                    value=Constant(value=Ellipsis))],
                            orelse=[
                                Expr(
                                    value=Constant(value=Ellipsis))])])])


.. class:: For(target, iter, body, orelse, type_comment)

   Một vòng lặp ``for``. ``target`` chứa (các) biến mà vòng lặp gán giá trị, dưới dạng một :class:`Name` duy nhất, :class:`Tuple`, :class:`List`, :class:`Attribute` hoặc
   nút :class:`Subscript`. ``iter`` chứa mục cần lặp qua, cũng dưới dạng một nút duy nhất. ``body`` và ``orelse`` chứa các danh sách nút cần thực thi. Các nút trong ``orelse`` được thực thi nếu vòng lặp kết thúc bình thường, thay vì thông qua câu lệnh ``break``.

   .. attribute:: type_comment

       ``type_comment`` là một chuỗi tùy chọn chứa chú thích với type annotation.

   .. doctest::

        >>> print(ast.dump(ast.parse("""
        ... for x in y:
        ...     ...
        ... else:
        ...     ...
        ... """), indent=4))
        Module(
            body=[
                For(
                    target=Name(id='x', ctx=Store()),
                    iter=Name(id='y', ctx=Load()),
                    body=[
                        Expr(
                            value=Constant(value=Ellipsis))],
                    orelse=[
                        Expr(
                            value=Constant(value=Ellipsis))])])


.. class:: While(test, body, orelse)

   Một vòng lặp ``while``. ``test`` chứa điều kiện, chẳng hạn như một nút :class:`Compare`.

   .. doctest::

        >>> print(ast.dump(ast.parse("""
        ... while x:
        ...    ...
        ... else:
        ...    ...
        ... """), indent=4))
        Module(
            body=[
                While(
                    test=Name(id='x', ctx=Load()),
                    body=[
                        Expr(
                            value=Constant(value=Ellipsis))],
                    orelse=[
                        Expr(
                            value=Constant(value=Ellipsis))])])


.. class:: Break
           Tiếp tục

   Các câu lệnh ``break`` và ``continue``.

   .. doctest::

        >>> print(ast.dump(ast.parse("""\
        ... for a in b:
        ...     if a > 5:
        ...         break
        ...     else:
        ...         continue
        ...
        ... """), indent=4))
        Module(
            body=[
                For(
                    target=Name(id='a', ctx=Store()),
                    iter=Name(id='b', ctx=Load()),
                    body=[
                        If(
                            test=Compare(
                                left=Name(id='a', ctx=Load()),
                                ops=[
                                    Gt()],
                                comparators=[
                                    Constant(value=5)]),
                            body=[
                                Break()],
                            orelse=[
                                Continue()])])])


.. class:: Try(body, handlers, orelse, finalbody)

   Các khối ``try``. Tất cả thuộc tính đều là danh sách các node cần thực thi, ngoại trừ ``handlers``, là danh sách các node :class:`ExceptHandler`.

   .. doctest::

        >>> print(ast.dump(ast.parse("""
        ... try:
        ...    ...
        ... except Exception:
        ...    ...
        ... except OtherException as e:
        ...    ...
        ... else:
        ...    ...
        ... finally:
        ...    ...
        ... """), indent=4))
        Module(
            body=[
                Try(
                    body=[
                        Expr(
                            value=Constant(value=Ellipsis))],
                    handlers=[
                        ExceptHandler(
                            type=Name(id='Exception', ctx=Load()),
                            body=[
                                Expr(
                                    value=Constant(value=Ellipsis))]),
                        ExceptHandler(
                            type=Name(id='OtherException', ctx=Load()),
                            name='e',
                            body=[
                                Expr(
                                    value=Constant(value=Ellipsis))])],
                    orelse=[
                        Expr(
                            value=Constant(value=Ellipsis))],
                    finalbody=[
                        Expr(
                            value=Constant(value=Ellipsis))])])


.. class:: TryStar(body, handlers, orelse, finalbody)

   Các khối ``try`` được theo sau bởi các mệnh đề ``except*``. Các thuộc tính giống như đối với :class:`Try`, nhưng các node :class:`ExceptHandler` trong ``handlers`` được diễn giải là các khối ``except*`` thay vì ``except``.

   .. doctest::

        >>> print(ast.dump(ast.parse("""
        ... try:
        ...    ...
        ... except* Exception:
        ...    ...
        ... """), indent=4))
        Module(
            body=[
                TryStar(
                    body=[
                        Expr(
                            value=Constant(value=Ellipsis))],
                    handlers=[
                        ExceptHandler(
                            type=Name(id='Exception', ctx=Load()),
                            body=[
                                Expr(
                                    value=Constant(value=Ellipsis))])])])

   .. versionadded:: 3.11

.. class:: ExceptHandler(type, name, body)

   Một mệnh đề ``except`` duy nhất. ``type`` là kiểu ngoại lệ mà nó sẽ khớp, thường là một node :class:`Name` (hoặc ``None`` đối với mệnh đề ``except:`` bắt tất cả). ``name`` là một chuỗi thô chứa tên dùng để lưu ngoại lệ, hoặc ``None`` nếu mệnh đề không có ``as foo``. ``body`` là một danh sách các node.

   .. doctest::

        >>> print(ast.dump(ast.parse("""\
        ... try:
        ...     a + 1
        ... except TypeError:
        ...     pass
        ... """), indent=4))
        Module(
            body=[
                Try(
                    body=[
                        Expr(
                            value=BinOp(
                                left=Name(id='a', ctx=Load()),
                                op=Add(),
                                right=Constant(value=1)))],
                    handlers=[
                        ExceptHandler(
                            type=Name(id='TypeError', ctx=Load()),
                            body=[
                                Pass()])])])


.. class:: With(items, body, type_comment)

   Một khối ``with``. ``items`` là danh sách các node :class:`withitem` biểu diễn các context manager, còn ``body`` là khối được thụt lề bên trong context.

   .. attribute:: type_comment

       ``type_comment`` là một chuỗi tùy chọn chứa chú thích với type annotation.


.. class:: withitem(context_expr, optional_vars)

   Một context manager duy nhất trong khối ``with``. ``context_expr`` là context manager, thường là một node :class:`Call`. ``optional_vars`` là một :class:`Name`,
   :class:`Tuple` hoặc :class:`List` cho phần ``as foo``, hoặc ``None`` nếu phần đó không được sử dụng.

   .. doctest::

        >>> print(ast.dump(ast.parse("""\
        ... with a as b, c as d:
        ...    something(b, d)
        ... """), indent=4))
        Module(
            body=[
                With(
                    items=[
                        withitem(
                            context_expr=Name(id='a', ctx=Load()),
                            optional_vars=Name(id='b', ctx=Store())),
                        withitem(
                            context_expr=Name(id='c', ctx=Load()),
                            optional_vars=Name(id='d', ctx=Store()))],
                    body=[
                        Expr(
                            value=Call(
                                func=Name(id='something', ctx=Load()),
                                args=[
                                    Name(id='b', ctx=Load()),
                                    Name(id='d', ctx=Load())]))])])


Đối sánh mẫu
^^^^^^^^^^^^


.. class:: Match(subject, cases)

   Một câu lệnh ``match``. ``subject`` chứa subject của phép đối sánh (đối tượng được đối sánh với các case), còn ``cases`` chứa một iterable gồm
   các node :class:`match_case` tương ứng với những case khác nhau.

   .. versionadded:: 3.10

.. class:: match_case(pattern, guard, body)

   Một mẫu case duy nhất trong câu lệnh ``match``. ``pattern`` chứa mẫu đối sánh mà subject sẽ được đối sánh với. Lưu ý rằng các
   node :class:`AST` được tạo cho các mẫu khác với các node được tạo cho các biểu thức, ngay cả khi chúng có cùng cú pháp.

   Thuộc tính ``guard`` chứa một biểu thức sẽ được đánh giá nếu pattern khớp với đối tượng cần so khớp.

   ``body`` chứa danh sách các node cần thực thi nếu pattern khớp và kết quả đánh giá biểu thức điều kiện là true.

   .. doctest::

        >>> print(ast.dump(ast.parse("""
        ... match x:
        ...     case [x] if x>0:
        ...         ...
        ...     case tuple():
        ...         ...
        ... """), indent=4))
        Module(
            body=[
                Match(
                    subject=Name(id='x', ctx=Load()),
                    cases=[
                        match_case(
                            pattern=MatchSequence(
                                patterns=[
                                    MatchAs(name='x')]),
                            guard=Compare(
                                left=Name(id='x', ctx=Load()),
                                ops=[
                                    Gt()],
                                comparators=[
                                    Constant(value=0)]),
                            body=[
                                Expr(
                                    value=Constant(value=Ellipsis))]),
                        match_case(
                            pattern=MatchClass(
                                cls=Name(id='tuple', ctx=Load())),
                            body=[
                                Expr(
                                    value=Constant(value=Ellipsis))])])])

   .. versionadded:: 3.10

.. class:: MatchValue(value)

   Một literal hoặc value pattern dùng phép so sánh bằng. ``value`` là một expression node. Các value node được phép bị giới hạn như mô tả trong tài liệu về câu lệnh match. Pattern này thành công nếu đối tượng cần so khớp bằng với giá trị đã được đánh giá.

   .. doctest::

        >>> print(ast.dump(ast.parse("""
        ... match x:
        ...     case "Relevant":
        ...         ...
        ... """), indent=4))
        Module(
            body=[
                Match(
                    subject=Name(id='x', ctx=Load()),
                    cases=[
                        match_case(
                            pattern=MatchValue(
                                value=Constant(value='Relevant')),
                            body=[
                                Expr(
                                    value=Constant(value=Ellipsis))])])])

   .. versionadded:: 3.10

.. class:: MatchSingleton(value)

   Một literal pattern dùng phép so sánh đồng nhất. ``value`` là singleton được dùng để so sánh: ``None``, ``True`` hoặc ``False``. Pattern này thành công nếu đối tượng cần so khớp là hằng số đã cho.

   .. doctest::

        >>> print(ast.dump(ast.parse("""
        ... match x:
        ...     case None:
        ...         ...
        ... """), indent=4))
        Module(
            body=[
                Match(
                    subject=Name(id='x', ctx=Load()),
                    cases=[
                        match_case(
                            pattern=MatchSingleton(value=None),
                            body=[
                                Expr(
                                    value=Constant(value=Ellipsis))])])])

   .. versionadded:: 3.10

.. class:: MatchSequence(patterns)

   Một sequence pattern dùng để so khớp. ``patterns`` chứa các pattern cần được so khớp với các phần tử của đối tượng cần so khớp nếu đối tượng đó là một sequence. Pattern này khớp với sequence có độ dài thay đổi nếu một trong các subpattern là node ``MatchStar``; nếu không, nó khớp với sequence có độ dài cố định.

   .. doctest::

        >>> print(ast.dump(ast.parse("""
        ... match x:
        ...     case [1, 2]:
        ...         ...
        ... """), indent=4))
        Module(
            body=[
                Match(
                    subject=Name(id='x', ctx=Load()),
                    cases=[
                        match_case(
                            pattern=MatchSequence(
                                patterns=[
                                    MatchValue(
                                        value=Constant(value=1)),
                                    MatchValue(
                                        value=Constant(value=2))]),
                            body=[
                                Expr(
                                    value=Constant(value=Ellipsis))])])])

   .. versionadded:: 3.10

.. class:: MatchStar(name)

   Khớp với phần còn lại của sequence trong một variable-length match sequence pattern. Nếu ``name`` không phải là ``None``, một danh sách chứa các phần tử còn lại của sequence sẽ được liên kết với tên đó nếu toàn bộ sequence pattern khớp thành công.

   .. doctest::

        >>> print(ast.dump(ast.parse("""
        ... match x:
        ...     case [1, 2, *rest]:
        ...         ...
        ...     case [*_]:
        ...         ...
        ... """), indent=4))
        Module(
            body=[
                Match(
                    subject=Name(id='x', ctx=Load()),
                    cases=[
                        match_case(
                            pattern=MatchSequence(
                                patterns=[
                                    MatchValue(
                                        value=Constant(value=1)),
                                    MatchValue(
                                        value=Constant(value=2)),
                                    MatchStar(name='rest')]),
                            body=[
                                Expr(
                                    value=Constant(value=Ellipsis))]),
                        match_case(
                            pattern=MatchSequence(
                                patterns=[
                                    MatchStar()]),
                            body=[
                                Expr(
                                    value=Constant(value=Ellipsis))])])])

   .. versionadded:: 3.10

.. class:: MatchMapping(keys, patterns, rest)

   Một mapping pattern dùng để so khớp. ``keys`` là một sequence gồm các expression node. ``patterns`` là sequence tương ứng gồm các pattern node. ``rest`` là một tên tùy chọn có thể được chỉ định để thu thập các phần tử còn lại của mapping. Các key expression được phép bị giới hạn như mô tả trong tài liệu về câu lệnh match.

   Mẫu này thành công nếu đối tượng subject là một mapping, tất cả biểu thức key được đánh giá đều có trong mapping và giá trị tương ứng với mỗi key khớp với subpattern tương ứng. Nếu ``rest`` không phải là ``None``, một dict chứa các phần tử mapping còn lại sẽ được liên kết với tên đó nếu mẫu mapping tổng thể thành công.

   .. doctest::

        >>> print(ast.dump(ast.parse("""
        ... match x:
        ...     case {1: _, 2: _}:
        ...         ...
        ...     case {**rest}:
        ...         ...
        ... """), indent=4))
        Module(
            body=[
                Match(
                    subject=Name(id='x', ctx=Load()),
                    cases=[
                        match_case(
                            pattern=MatchMapping(
                                keys=[
                                    Constant(value=1),
                                    Constant(value=2)],
                                patterns=[
                                    MatchAs(),
                                    MatchAs()]),
                            body=[
                                Expr(
                                    value=Constant(value=Ellipsis))]),
                        match_case(
                            pattern=MatchMapping(rest='rest'),
                            body=[
                                Expr(
                                    value=Constant(value=Ellipsis))])])])

   .. versionadded:: 3.10

.. class:: MatchClass(cls, patterns, kwd_attrs, kwd_patterns)

   Một class pattern dùng để match. ``cls`` là một biểu thức cung cấp class danh nghĩa cần match. ``patterns`` là một chuỗi các pattern node được match với chuỗi thuộc tính được class định nghĩa cho việc pattern matching. ``kwd_attrs`` là một chuỗi các thuộc tính bổ sung cần match (được chỉ định dưới dạng keyword arguments trong class pattern), còn ``kwd_patterns`` là các pattern tương ứng (được chỉ định dưới dạng keyword values trong class pattern).

   Mẫu này thành công nếu subject là một instance của class được chỉ định, tất cả positional pattern đều khớp với các thuộc tính tương ứng do class định nghĩa và mọi thuộc tính keyword được chỉ định đều khớp với pattern tương ứng của chúng.

   Lưu ý: các class có thể định nghĩa một property trả về self để match một pattern node với instance đang được match. Một số kiểu builtin cũng được match theo cách đó, như được mô tả trong tài liệu về câu lệnh match.

   .. doctest::

        >>> print(ast.dump(ast.parse("""
        ... match x:
        ...     case Point2D(0, 0):
        ...         ...
        ...     case Point3D(x=0, y=0, z=0):
        ...         ...
        ... """), indent=4))
        Module(
            body=[
                Match(
                    subject=Name(id='x', ctx=Load()),
                    cases=[
                        match_case(
                            pattern=MatchClass(
                                cls=Name(id='Point2D', ctx=Load()),
                                patterns=[
                                    MatchValue(
                                        value=Constant(value=0)),
                                    MatchValue(
                                        value=Constant(value=0))]),
                            body=[
                                Expr(
                                    value=Constant(value=Ellipsis))]),
                        match_case(
                            pattern=MatchClass(
                                cls=Name(id='Point3D', ctx=Load()),
                                kwd_attrs=[
                                    'x',
                                    'y',
                                    'z'],
                                kwd_patterns=[
                                    MatchValue(
                                        value=Constant(value=0)),
                                    MatchValue(
                                        value=Constant(value=0)),
                                    MatchValue(
                                        value=Constant(value=0))]),
                            body=[
                                Expr(
                                    value=Constant(value=Ellipsis))])])])

   .. versionadded:: 3.10

.. class:: MatchAs(pattern, name)

   Một match "as-pattern", capture pattern hoặc wildcard pattern. ``pattern`` chứa match pattern mà subject sẽ được match với. Nếu pattern là ``None``, node biểu diễn một capture pattern (tức là một tên đứng riêng) và sẽ luôn thành công.

   Thuộc tính ``name`` chứa tên sẽ được liên kết nếu pattern thành công. Nếu ``name`` là ``None``, ``pattern`` cũng phải là ``None`` và node biểu diễn wildcard pattern.

   .. doctest::

        >>> print(ast.dump(ast.parse("""
        ... match x:
        ...     case [x] as y:
        ...         ...
        ...     case _:
        ...         ...
        ... """), indent=4))
        Module(
            body=[
                Match(
                    subject=Name(id='x', ctx=Load()),
                    cases=[
                        match_case(
                            pattern=MatchAs(
                                pattern=MatchSequence(
                                    patterns=[
                                        MatchAs(name='x')]),
                                name='y'),
                            body=[
                                Expr(
                                    value=Constant(value=Ellipsis))]),
                        match_case(
                            pattern=MatchAs(),
                            body=[
                                Expr(
                                    value=Constant(value=Ellipsis))])])])

   .. versionadded:: 3.10

.. class:: MatchOr(patterns)

   Một match "or-pattern". Or-pattern lần lượt match từng subpattern của nó với subject cho đến khi một subpattern thành công. Khi đó, or-pattern được xem là thành công. Nếu không có subpattern nào thành công, or-pattern sẽ thất bại. Thuộc tính ``patterns`` chứa một danh sách các match pattern node sẽ được match với subject.

   .. doctest::

        >>> print(ast.dump(ast.parse("""
        ... match x:
        ...     case [x] | (y):
        ...         ...
        ... """), indent=4))
        Module(
            body=[
                Match(
                    subject=Name(id='x', ctx=Load()),
                    cases=[
                        match_case(
                            pattern=MatchOr(
                                patterns=[
                                    MatchSequence(
                                        patterns=[
                                            MatchAs(name='x')]),
                                    MatchAs(name='y')]),
                            body=[
                                Expr(
                                    value=Constant(value=Ellipsis))])])])

   .. versionadded:: 3.10


Chú thích kiểu
^^^^^^^^^^^^^^

.. class:: TypeIgnore(lineno, tag)

   Một chú thích ``# type: ignore`` nằm tại *lineno*. *tag* là thẻ tùy chọn được chỉ định theo dạng ``# type: ignore <tag>``.

   .. doctest::

      >>> print(ast.dump(ast.parse('x = 1 # type: ignore', type_comments=True), indent=4))
      Module(
          body=[
              Assign(
                  targets=[
                      Name(id='x', ctx=Store())],
                  value=Constant(value=1))],
          type_ignores=[
              TypeIgnore(lineno=1, tag='')])
      >>> print(ast.dump(ast.parse('x: bool = 1 # type: ignore[assignment]', type_comments=True), indent=4))
      Module(
          body=[
              AnnAssign(
                  target=Name(id='x', ctx=Store()),
                  annotation=Name(id='bool', ctx=Load()),
                  value=Constant(value=1),
                  simple=1)],
          type_ignores=[
              TypeIgnore(lineno=1, tag='[assignment]')])

   .. note::
      :class:`!TypeIgnore` nodes are not generated when the *type_comments* parameter
      được đặt thành ``False`` (mặc định). Xem :func:`ast.parse` để biết thêm chi tiết.

   .. versionadded:: 3.8

.. _ast-type-params:

Tham số kiểu
^^^^^^^^^^^^

:ref:`Tham số kiểu <type-params>` có thể tồn tại trên các lớp, hàm và bí danh kiểu.

.. class:: TypeVar(name, bound, default_value)

   Một :class:`typing.TypeVar`. ``name`` là tên của biến kiểu. ``bound`` là giới hạn hoặc các ràng buộc, nếu có. Nếu ``bound`` là một :class:`Tuple`, nó biểu diễn các ràng buộc; nếu không, nó biểu diễn giới hạn. ``default_value`` là giá trị mặc định; nếu :class:`!TypeVar` không có giá trị mặc định, thuộc tính này sẽ được đặt thành ``None``.

   .. doctest::

        >>> print(ast.dump(ast.parse("type Alias[T: int = bool] = list[T]"), indent=4))
        Module(
            body=[
                TypeAlias(
                    name=Name(id='Alias', ctx=Store()),
                    type_params=[
                        TypeVar(
                            name='T',
                            bound=Name(id='int', ctx=Load()),
                            default_value=Name(id='bool', ctx=Load()))],
                    value=Subscript(
                        value=Name(id='list', ctx=Load()),
                        slice=Name(id='T', ctx=Load()),
                        ctx=Load()))])

   .. versionadded:: 3.12

   .. versionchanged:: 3.13
      Đã thêm tham số *default_value*.

.. class:: ParamSpec(name, default_value)

   Một :class:`typing.ParamSpec`. ``name`` là tên của đặc tả tham số. ``default_value`` là giá trị mặc định; nếu :class:`!ParamSpec` không có giá trị mặc định, thuộc tính này sẽ được đặt thành ``None``.

   .. doctest::

        >>> print(ast.dump(ast.parse("type Alias[**P = [int, str]] = Callable[P, int]"), indent=4))
        Module(
            body=[
                TypeAlias(
                    name=Name(id='Alias', ctx=Store()),
                    type_params=[
                        ParamSpec(
                            name='P',
                            default_value=List(
                                elts=[
                                    Name(id='int', ctx=Load()),
                                    Name(id='str', ctx=Load())],
                                ctx=Load()))],
                    value=Subscript(
                        value=Name(id='Callable', ctx=Load()),
                        slice=Tuple(
                            elts=[
                                Name(id='P', ctx=Load()),
                                Name(id='int', ctx=Load())],
                            ctx=Load()),
                        ctx=Load()))])

   .. versionadded:: 3.12

   .. versionchanged:: 3.13
      Đã thêm tham số *default_value*.

.. class:: TypeVarTuple(name, default_value)

   Một :class:`typing.TypeVarTuple`. ``name`` là tên của tuple biến kiểu. ``default_value`` là giá trị mặc định; nếu :class:`!TypeVarTuple` không có giá trị mặc định, thuộc tính này sẽ được đặt thành ``None``.

   .. doctest::

        >>> print(ast.dump(ast.parse("type Alias[*Ts = ()] = tuple[*Ts]"), indent=4))
        Module(
            body=[
                TypeAlias(
                    name=Name(id='Alias', ctx=Store()),
                    type_params=[
                        TypeVarTuple(
                            name='Ts',
                            default_value=Tuple(ctx=Load()))],
                    value=Subscript(
                        value=Name(id='tuple', ctx=Load()),
                        slice=Tuple(
                            elts=[
                                Starred(
                                    value=Name(id='Ts', ctx=Load()),
                                    ctx=Load())],
                            ctx=Load()),
                        ctx=Load()))])

   .. versionadded:: 3.12

   .. versionchanged:: 3.13
      Đã thêm tham số *default_value*.

Định nghĩa hàm và lớp
^^^^^^^^^^^^^^^^^^^^^

.. class:: FunctionDef(name, args, body, decorator_list, returns, type_comment, type_params)

   Một định nghĩa hàm.

   * ``name`` là một chuỗi thô chứa tên hàm.
   * ``args`` là một nút :class:`arguments`.
   * ``body`` là danh sách các nút bên trong hàm.
   * ``decorator_list`` là danh sách các decorator cần áp dụng, được lưu theo thứ tự từ ngoài vào trong (tức là phần tử đầu tiên trong danh sách sẽ được áp dụng sau cùng).
   * ``returns`` là chú thích kiểu trả về.
   * ``type_params`` là danh sách các tham số :ref:`type parameters <ast-type-params>`.

   .. attribute:: type_comment

       ``type_comment`` là một chuỗi tùy chọn chứa chú thích kiểu dưới dạng comment.

   .. versionchanged:: 3.12
        Đã thêm ``type_params``.


.. class:: Lambda(args, body)

   ``lambda`` là định nghĩa hàm tối giản có thể được sử dụng bên trong một biểu thức. Không giống :class:`FunctionDef`, ``body`` chứa một node duy nhất.

   .. doctest::

        >>> print(ast.dump(ast.parse('lambda x,y: ...'), indent=4))
        Module(
            body=[
                Expr(
                    value=Lambda(
                        args=arguments(
                            args=[
                                arg(arg='x'),
                                arg(arg='y')]),
                        body=Constant(value=Ellipsis)))])


.. class:: arguments(posonlyargs, args, vararg, kwonlyargs, kw_defaults, kwarg, defaults)

   Các đối số của một hàm.

   * ``posonlyargs``, ``args`` và ``kwonlyargs`` là các danh sách node :class:`arg`.
   * ``vararg`` và ``kwarg`` là các node :class:`arg` đơn, tham chiếu đến các tham số ``*args, **kwargs``.
   * ``kw_defaults`` là danh sách các giá trị mặc định cho những đối số chỉ nhận từ khóa. Nếu một giá trị là ``None``, đối số tương ứng là bắt buộc.
   * ``defaults`` là danh sách các giá trị mặc định cho những đối số có thể được truyền theo vị trí. Nếu có ít giá trị mặc định hơn, chúng tương ứng với n đối số cuối cùng.


.. class:: arg(arg, annotation, type_comment)

   Một đối số đơn trong danh sách. ``arg`` là chuỗi thô chứa tên đối số; ``annotation`` là chú thích của đối số đó, chẳng hạn như một node :class:`Name`.

   .. attribute:: type_comment

       ``type_comment`` là một chuỗi tùy chọn chứa chú thích kiểu dưới dạng comment

   .. doctest::

        >>> print(ast.dump(ast.parse("""\
        ... @decorator1
        ... @decorator2
        ... def f(a: 'annotation', b=1, c=2, *d, e, f=3, **g) -> 'return annotation':
        ...     pass
        ... """), indent=4))
        Module(
            body=[
                FunctionDef(
                    name='f',
                    args=arguments(
                        args=[
                            arg(
                                arg='a',
                                annotation=Constant(value='annotation')),
                            arg(arg='b'),
                            arg(arg='c')],
                        vararg=arg(arg='d'),
                        kwonlyargs=[
                            arg(arg='e'),
                            arg(arg='f')],
                        kw_defaults=[
                            None,
                            Constant(value=3)],
                        kwarg=arg(arg='g'),
                        defaults=[
                            Constant(value=1),
                            Constant(value=2)]),
                    body=[
                        Pass()],
                    decorator_list=[
                        Name(id='decorator1', ctx=Load()),
                        Name(id='decorator2', ctx=Load())],
                    returns=Constant(value='return annotation'))])


.. class:: Return(value)

   Một câu lệnh ``return``.

   .. doctest::

        >>> print(ast.dump(ast.parse('return 4'), indent=4))
        Module(
            body=[
                Return(
                    value=Constant(value=4))])


.. class:: Yield(value)
           YieldFrom(value)

   Một biểu thức ``yield`` hoặc ``yield from``. Vì đây là các biểu thức, chúng phải được bao bọc trong một node :class:`Expr` nếu giá trị được gửi trả về không được sử dụng.

   .. doctest::

        >>> print(ast.dump(ast.parse('yield x'), indent=4))
        Module(
            body=[
                Expr(
                    value=Yield(
                        value=Name(id='x', ctx=Load())))])

        >>> print(ast.dump(ast.parse('yield from x'), indent=4))
        Module(
            body=[
                Expr(
                    value=YieldFrom(
                        value=Name(id='x', ctx=Load())))])


.. class:: Global(names)
           Nonlocal(names)

   Các câu lệnh ``global`` và ``nonlocal``. ``names`` là một danh sách các chuỗi thô.

   .. doctest::

        >>> print(ast.dump(ast.parse('global x,y,z'), indent=4))
        Module(
            body=[
                Global(
                    names=[
                        'x',
                        'y',
                        'z'])])

        >>> print(ast.dump(ast.parse('nonlocal x,y,z'), indent=4))
        Module(
            body=[
                Nonlocal(
                    names=[
                        'x',
                        'y',
                        'z'])])


.. class:: ClassDef(name, bases, keywords, body, decorator_list, type_params)

   Một định nghĩa lớp.

   * ``name`` là một chuỗi thô dùng cho tên lớp
   * ``bases`` là danh sách các node cho những lớp cơ sở được chỉ định rõ ràng.
   * ``keywords`` là danh sách các node :class:`.keyword`, chủ yếu dành cho 'metaclass'. Các keyword khác sẽ được truyền đến metaclass, theo :pep:`3115`.
   * ``body`` là danh sách các node biểu diễn mã bên trong định nghĩa lớp.
   * ``decorator_list`` là danh sách các node, như trong :class:`FunctionDef`.
   * ``type_params`` là danh sách các tham số :ref:`type parameters <ast-type-params>`.

   .. doctest::

        >>> print(ast.dump(ast.parse("""\
        ... @decorator1
        ... @decorator2
        ... class Foo(base1, base2, metaclass=meta):
        ...     pass
        ... """), indent=4))
        Module(
            body=[
                ClassDef(
                    name='Foo',
                    bases=[
                        Name(id='base1', ctx=Load()),
                        Name(id='base2', ctx=Load())],
                    keywords=[
                        keyword(
                            arg='metaclass',
                            value=Name(id='meta', ctx=Load()))],
                    body=[
                        Pass()],
                    decorator_list=[
                        Name(id='decorator1', ctx=Load()),
                        Name(id='decorator2', ctx=Load())])])

   .. versionchanged:: 3.12
        Đã thêm ``type_params``.

Async và await
^^^^^^^^^^^^^^

.. class:: AsyncFunctionDef(name, args, body, decorator_list, returns, type_comment, type_params)

   Một định nghĩa hàm ``async def``. Có các trường giống như
   :class:`FunctionDef`.

   .. versionchanged:: 3.12
        Được thêm trong ``type_params``.


.. class:: Await(value)

   Một biểu thức ``await``. ``value`` là giá trị mà nó chờ. Chỉ hợp lệ trong phần thân của :class:`AsyncFunctionDef`.

.. doctest::

    >>> print(ast.dump(ast.parse("""\
    ... async def f():
    ...     await other_func()
    ... """), indent=4))
    Module(
        body=[
            AsyncFunctionDef(
                name='f',
                args=arguments(),
                body=[
                    Expr(
                        value=Await(
                            value=Call(
                                func=Name(id='other_func', ctx=Load()))))])])


.. class:: AsyncFor(target, iter, body, orelse, type_comment)
           AsyncWith(items, body, type_comment)

   Các vòng lặp ``async for`` và trình quản lý ngữ cảnh ``async with``. Chúng lần lượt có các trường giống như :class:`For` và :class:`With`. Chỉ hợp lệ trong phần thân của :class:`AsyncFunctionDef`.

.. note::
   Khi một chuỗi được phân tích cú pháp bởi :func:`ast.parse`, các node toán tử (là các lớp con của :class:`ast.operator`, :class:`ast.unaryop`, :class:`ast.cmpop`,
   :class:`ast.boolop` và :class:`ast.expr_context`) trên cây được trả về sẽ là các singleton. Mọi thay đổi đối với một giá trị sẽ được phản ánh trong tất cả các lần xuất hiện khác của cùng giá trị đó (ví dụ: :class:`ast.Add`).


Các helper của :mod:`!ast`
--------------------------

Ngoài các lớp node, module :mod:`!ast` định nghĩa các hàm và lớp tiện ích sau đây để duyệt cây cú pháp trừu tượng:

.. function:: parse(source, filename='<unknown>', mode='exec', *, type_comments=False, feature_version=None, optimize=-1)

   Phân tích mã nguồn thành một node AST. Tương đương với ``compile(source, filename, mode, flags=FLAGS_VALUE, optimize=optimize)``, trong đó ``FLAGS_VALUE`` là ``ast.PyCF_ONLY_AST`` nếu ``optimize <= 0`` và ``ast.PyCF_OPTIMIZED_AST`` trong các trường hợp còn lại.

   Nếu cung cấp ``type_comments=True``, parser sẽ được sửa đổi để kiểm tra và trả về các chú thích kiểu theo quy định của :pep:`484` và :pep:`526`. Điều này tương đương với việc thêm :data:`ast.PyCF_TYPE_COMMENTS` vào các cờ được truyền cho :func:`compile`. Thao tác này sẽ báo lỗi cú pháp đối với các chú thích kiểu đặt sai vị trí. Nếu không có cờ này, các chú thích kiểu sẽ bị bỏ qua, và trường ``type_comment`` trên các node AST được chọn sẽ luôn là ``None``. Ngoài ra, vị trí của các chú thích ``# type: ignore`` sẽ được trả về dưới dạng thuộc tính ``type_ignores`` của :class:`Module` (nếu không thì đây luôn là một danh sách rỗng).

   Ngoài ra, nếu ``mode`` là ``'func_type'``, cú pháp đầu vào sẽ được sửa đổi để tương ứng với các "signature type comments" của :pep:`484`, chẳng hạn như ``(str, int) -> List[str]``.

   Đặt ``feature_version`` thành một tuple ``(major, minor)`` sẽ khiến parser cố gắng phân tích cú pháp ở mức "best-effort" bằng grammar của phiên bản Python đó. Ví dụ, đặt ``feature_version=(3, 9)`` sẽ cố gắng không cho phép phân tích các câu lệnh :keyword:`match`. Hiện tại, ``major`` phải bằng ``3``. Phiên bản thấp nhất được hỗ trợ là ``(3, 7)`` (và phiên bản này có thể tăng trong các phiên bản Python tương lai); phiên bản cao nhất là ``sys.version_info[0:2]``. Cố gắng "best-effort" nghĩa là không có gì bảo đảm rằng kết quả phân tích cú pháp (hoặc việc phân tích cú pháp có thành công hay không) sẽ giống với khi chạy trên phiên bản Python tương ứng với ``feature_version``.

   Nếu mã nguồn chứa ký tự null (``\0``), :exc:`ValueError` sẽ được phát sinh.

   .. warning::
      Lưu ý rằng việc phân tích cú pháp thành công mã nguồn thành một đối tượng AST không đảm bảo mã nguồn được cung cấp là mã Python hợp lệ có thể thực thi, vì bước biên dịch có thể phát sinh thêm các ngoại lệ :exc:`SyntaxError`. Ví dụ, mã nguồn ``return 42`` tạo ra một node AST hợp lệ cho câu lệnh return, nhưng không thể được biên dịch riêng lẻ (nó cần nằm bên trong một node hàm).

      Cụ thể, :func:`ast.parse` sẽ không thực hiện bất kỳ kiểm tra phạm vi nào, trong khi bước biên dịch có thực hiện kiểm tra đó.

   .. warning::
      Có thể làm trình thông dịch Python bị crash bằng một chuỗi đủ lớn/phức tạp do các giới hạn về độ sâu ngăn xếp trong trình biên dịch AST của Python.

   .. versionchanged:: 3.8
      Đã bổ sung ``type_comments``, ``mode='func_type'`` và ``feature_version``.

   .. versionchanged:: 3.13
      Phiên bản tối thiểu được hỗ trợ cho ``feature_version`` hiện là ``(3, 7)``. Đối số ``optimize`` đã được bổ sung.


.. function:: unparse(ast_obj)

   Unparse một đối tượng :class:`ast.AST` và tạo ra một chuỗi chứa mã sẽ tạo ra một đối tượng :class:`ast.AST` tương đương nếu được phân tích cú pháp lại bằng :func:`ast.parse`.

   .. warning::
      Chuỗi mã được tạo ra không nhất thiết sẽ bằng với mã ban đầu đã tạo đối tượng :class:`ast.AST` (khi không có bất kỳ tối ưu hóa trình biên dịch nào, chẳng hạn như tuple/frozenset hằng).

   .. warning::
      Việc unparse một biểu thức cực kỳ phức tạp sẽ cho kết quả là
      :exc:`RecursionError`.

   .. versionadded:: 3.9


.. function:: literal_eval(node_or_string)

   Đánh giá một node biểu thức hoặc một chuỗi chỉ chứa một literal Python hoặc biểu diễn container. Chuỗi hoặc node được cung cấp chỉ được phép bao gồm các cấu trúc literal Python sau: chuỗi, bytes, số, tuple, list, dict, set, boolean, ``None`` và ``Ellipsis``.

   Có thể dùng hàm này để đánh giá các chuỗi chứa giá trị Python mà không cần tự mình phân tích cú pháp các giá trị đó. Hàm này không thể đánh giá các biểu thức phức tạp tùy ý, chẳng hạn như các biểu thức có toán tử hoặc phép lập chỉ mục.

   Trước đây, hàm này được mô tả là "an toàn" mà không định nghĩa ý nghĩa của từ đó. Điều này gây hiểu lầm. Hàm này được thiết kế cụ thể để không thực thi mã Python, không giống :func:`eval` tổng quát hơn. Hàm không có namespace, không tra cứu tên và không có khả năng gọi ra bên ngoài. Tuy nhiên, hàm không hoàn toàn miễn nhiễm với tấn công: Một đầu vào tương đối nhỏ có thể dẫn đến cạn kiệt bộ nhớ hoặc cạn kiệt ngăn xếp C, khiến tiến trình bị lỗi. Một số đầu vào cũng có thể gây ra tình trạng từ chối dịch vụ do sử dụng CPU quá mức. Vì vậy, không nên gọi hàm này với dữ liệu không đáng tin cậy.

   .. warning::
      Có thể làm trình thông dịch Python bị lỗi do các giới hạn về độ sâu ngăn xếp trong trình biên dịch AST của Python.

      Hàm này có thể phát sinh :exc:`ValueError`, :exc:`TypeError`, :exc:`SyntaxError`,
      :exc:`MemoryError` và :exc:`RecursionError` tùy thuộc vào đầu vào không hợp lệ.

   .. versionchanged:: 3.2
      Hiện hỗ trợ bytes và các literal set.

   .. versionchanged:: 3.9
      Hiện hỗ trợ tạo các set rỗng bằng ``'set()'``.

   .. versionchanged:: 3.10
      Đối với đầu vào chuỗi, các khoảng trắng và tab ở đầu hiện đã được loại bỏ.


.. function:: get_docstring(node, clean=True)

   Trả về docstring của *node* đã cho (phải là một
   :class:`FunctionDef`, :class:`AsyncFunctionDef`, :class:`ClassDef`, hoặc :class:`Module` node), hoặc ``None`` nếu không có docstring. Nếu *clean* là true, dọn dẹp thụt lề của docstring bằng
   :func:`inspect.cleandoc`.

   .. versionchanged:: 3.5
      :class:`AsyncFunctionDef` is now supported.


.. function:: get_source_segment(source, node, *, padded=False)

   Lấy đoạn mã nguồn của *source* đã tạo ra *node*. Nếu thiếu một số thông tin vị trí (:attr:`~ast.AST.lineno`, :attr:`~ast.AST.end_lineno`,
   Nếu :attr:`~ast.AST.col_offset`, hoặc :attr:`~ast.AST.end_col_offset`) bị thiếu, trả về ``None``.

   Nếu *padded* là ``True``, dòng đầu tiên của một câu lệnh nhiều dòng sẽ được đệm bằng khoảng trắng để khớp với vị trí ban đầu.

   .. versionadded:: 3.8


.. function:: fix_missing_locations(node)

   Khi bạn biên dịch một cây nút bằng :func:`compile`, trình biên dịch yêu cầu
   các thuộc tính :attr:`~ast.AST.lineno` và :attr:`~ast.AST.col_offset` cho mọi nút hỗ trợ chúng. Việc điền các thuộc tính này cho những nút được tạo tự động khá tẻ nhạt, vì vậy helper này sẽ đệ quy thêm các thuộc tính ở những nơi chưa được thiết lập, bằng cách đặt chúng thành giá trị của nút cha. Helper này hoạt động đệ quy, bắt đầu từ *node*.


.. function:: increment_lineno(node, n=1)

   Tăng số dòng và số dòng kết thúc của mỗi nút trong cây, bắt đầu từ *node*, thêm *n*. Điều này hữu ích để "di chuyển mã" đến một vị trí khác trong tệp.


.. function:: copy_location(new_node, old_node)

   Sao chép vị trí nguồn (:attr:`~ast.AST.lineno`, :attr:`~ast.AST.col_offset`, :attr:`~ast.AST.end_lineno` và :attr:`~ast.AST.end_col_offset`) từ *old_node* sang *new_node* nếu có thể, rồi trả về *new_node*.


.. function:: iter_fields(node)

   Tạo một tuple gồm ``(fieldname, value)`` cho mỗi trường trong ``node._fields`` hiện có trên *node*.


.. function:: iter_child_nodes(node)

   Yield tất cả các node con trực tiếp của *node*, tức là tất cả các field là node và tất cả các item của những field là danh sách node.


.. function:: walk(node)

   Đệ quy yield tất cả các node hậu duệ trong cây bắt đầu từ *node* (bao gồm cả *node*), theo thứ tự không xác định. Điều này hữu ích nếu bạn chỉ muốn sửa đổi các node tại chỗ và không quan tâm đến context.


.. class:: NodeVisitor()

   Một lớp cơ sở dành cho node visitor, dùng để duyệt abstract syntax tree và gọi một hàm visitor cho mỗi node được tìm thấy. Hàm này có thể trả về một giá trị, và giá trị đó được chuyển tiếp bởi phương thức :meth:`visit`.

   Lớp này được thiết kế để tạo lớp con, trong đó lớp con bổ sung các phương thức visitor.

   .. method:: visit(node)

      Truy cập một node. Cách triển khai mặc định gọi phương thức có tên
      :samp:`self.visit_{classname}`, trong đó *classname* là tên của lớp node, hoặc :meth:`generic_visit` nếu phương thức đó không tồn tại.

   .. method:: generic_visit(node)

      Visitor này gọi :meth:`visit` trên tất cả các node con của node.

      Lưu ý rằng các nút con của những nút có phương thức visitor tùy chỉnh sẽ không được duyệt, trừ khi visitor gọi :meth:`generic_visit` hoặc tự duyệt chúng.

   .. method:: visit_Constant(node)

      Xử lý tất cả các nút hằng số.

   Không sử dụng :class:`NodeVisitor` nếu bạn muốn áp dụng các thay đổi cho các nút trong quá trình duyệt. Để làm việc này, có một visitor đặc biệt (:class:`NodeTransformer`) cho phép sửa đổi các nút.

   .. deprecated-removed:: 3.8 3.14

      Các phương thức :meth:`!visit_Num`, :meth:`!visit_Str`, :meth:`!visit_Bytes`,
      :meth:`!visit_NameConstant` và :meth:`!visit_Ellipsis` sẽ không được gọi trong Python 3.14+. Thay vào đó, hãy thêm phương thức :meth:`visit_Constant` để xử lý tất cả các nút hằng số.


.. class:: NodeTransformer()

   Một lớp con :class:`NodeVisitor` duyệt cây cú pháp trừu tượng và cho phép sửa đổi các nút.

   :class:`NodeTransformer` sẽ duyệt AST và sử dụng giá trị trả về của các phương thức visitor để thay thế hoặc xóa nút cũ. Nếu giá trị trả về của phương thức visitor là ``None``, nút sẽ bị xóa khỏi vị trí của nó; nếu không, nút sẽ được thay thế bằng giá trị trả về. Giá trị trả về có thể là nút ban đầu, trong trường hợp đó sẽ không có thao tác thay thế nào diễn ra.

   Sau đây là một transformer viết lại tất cả các lần tra cứu tên (``foo``) thành ``data['foo']``::

      class RewriteName(NodeTransformer):

          def visit_Name(self, node):
              return Subscript(
                  value=Name(id='data', ctx=Load()),
                  slice=Constant(value=node.id),
                  ctx=node.ctx
              )

   Hãy lưu ý rằng nếu node bạn đang thao tác có các node con, bạn phải tự mình biến đổi các node con đó hoặc gọi phương thức :meth:`~ast.NodeVisitor.generic_visit` cho node trước.

   Đối với các node thuộc một tập hợp các câu lệnh (điều này áp dụng cho tất cả các node câu lệnh), visitor cũng có thể trả về một danh sách các node thay vì chỉ một node.

   Nếu :class:`NodeTransformer` giới thiệu các node mới (không thuộc cây ban đầu) mà không cung cấp thông tin vị trí cho chúng (chẳng hạn như
   :attr:`~ast.AST.lineno`), cần gọi :func:`fix_missing_locations` với cây con mới để tính toán lại thông tin vị trí::

      tree = ast.parse('foo', mode='eval')
      new_tree = fix_missing_locations(RewriteName().visit(tree))

   Thông thường, bạn sử dụng transformer như sau::

      node = YourTransformer().visit(node)


.. function:: dump(node, annotate_fields=True, include_attributes=False, *, indent=None, show_empty=False)

   Trả về bản dump đã được định dạng của cây trong *node*.  Tính năng này chủ yếu hữu ích cho mục đích debugging.  Nếu *annotate_fields* là true (theo mặc định), chuỗi trả về sẽ hiển thị tên và giá trị của các field. Nếu *annotate_fields* là false, chuỗi kết quả sẽ ngắn gọn hơn vì lược bỏ các tên field không gây mơ hồ.  Các thuộc tính như số dòng và độ lệch cột không được dump theo mặc định.  Nếu muốn bao gồm các thuộc tính này, có thể đặt *include_attributes* thành true.

   Nếu *indent* là một số nguyên không âm hoặc một chuỗi, cây sẽ được in đẹp với mức thụt lề đó. Mức thụt lề bằng 0, số âm hoặc ``""`` chỉ chèn các dòng mới. ``None`` (mặc định) chọn biểu diễn trên một dòng. Sử dụng số nguyên dương để thụt lề với số khoảng trắng tương ứng ở mỗi cấp. Nếu *indent* là một chuỗi (chẳng hạn như ``"\t"``), chuỗi đó sẽ được dùng để thụt lề cho mỗi cấp.

   Nếu *show_empty* là false (mặc định), các danh sách rỗng tùy chọn sẽ bị bỏ qua khỏi đầu ra. Các giá trị ``None`` tùy chọn luôn bị bỏ qua.

   .. versionchanged:: 3.9
      Đã thêm tùy chọn *indent*.

   .. versionchanged:: 3.13
      Đã thêm tùy chọn *show_empty*.

      .. doctest::

         >>> print(ast.dump(ast.parse("""\
         ... async def f():
         ...     await other_func()
         ... """), indent=4, show_empty=True))
         Module(
             body=[
                 AsyncFunctionDef(
                     name='f',
                     args=arguments(
                         posonlyargs=[],
                         args=[],
                         kwonlyargs=[],
                         kw_defaults=[],
                         defaults=[]),
                     body=[
                         Expr(
                             value=Await(
                                 value=Call(
                                     func=Name(id='other_func', ctx=Load()),
                                     args=[],
                                     keywords=[])))],
                     decorator_list=[],
                     type_params=[])],
             type_ignores=[])


.. function:: compare(a, b, /, *, compare_attributes=False)

   So sánh đệ quy hai AST.

   *compare_attributes* xác định việc các thuộc tính AST có được xem xét khi so sánh hay không. Nếu *compare_attributes* là ``False`` (mặc định), các thuộc tính sẽ bị bỏ qua. Nếu không, tất cả chúng phải bằng nhau. Tùy chọn này hữu ích để kiểm tra xem các AST có bằng nhau về cấu trúc nhưng khác nhau về khoảng trắng hoặc các chi tiết tương tự hay không. Các thuộc tính bao gồm số dòng và độ lệch cột.

   .. versionadded:: 3.14


.. _ast-compiler-flags:

Các cờ của trình biên dịch
--------------------------

Có thể truyền các cờ sau vào :func:`compile` để thay đổi tác động đến quá trình biên dịch một chương trình:

.. data:: PyCF_ALLOW_TOP_LEVEL_AWAIT

   Bật hỗ trợ cho ``await``, ``async for``, ``async with`` cấp cao nhất và các phép dựng async.

   .. versionadded:: 3.8

.. data:: PyCF_ONLY_AST

   Tạo và trả về một cây cú pháp trừu tượng thay vì trả về một đối tượng mã đã biên dịch.

.. data:: PyCF_OPTIMIZED_AST

   AST được trả về sẽ được tối ưu hóa theo đối số *optimize* trong :func:`compile` hoặc :func:`ast.parse`.

   .. versionadded:: 3.13

.. data:: PyCF_TYPE_COMMENTS

   Bật hỗ trợ cho các chú thích kiểu (type comment) theo kiểu :pep:`484` và :pep:`526` (``# type: <type>``, ``# type: ignore <stuff>``).

   .. versionadded:: 3.8


.. _ast-cli:

Cách sử dụng trên dòng lệnh
---------------------------

.. versionadded:: 3.9

Mô-đun :mod:`!ast` có thể được thực thi dưới dạng tập lệnh từ dòng lệnh. Cách thực hiện rất đơn giản:

.. code-block:: sh

   python -m ast [-m <mode>] [-a] [infile]

Các tùy chọn sau được chấp nhận:

.. program:: ast

.. option:: -h, --help

   Hiển thị thông báo trợ giúp rồi thoát.

.. option:: -m <mode>
            --mode <mode>

   Chỉ định loại mã cần được biên dịch, chẳng hạn như đối số *mode* trong :func:`parse`.

.. option:: --no-type-comments

   Không phân tích cú pháp các chú thích kiểu.

.. option:: -a, --include-attributes

   Bao gồm các thuộc tính như số dòng và độ lệch cột.

.. option:: -i <indent>
            --indent <indent>

   Mức thụt lề của các node trong AST (số khoảng trắng).

.. option:: --feature-version <version>

   Phiên bản Python ở định dạng 3.x (ví dụ: 3.10). Mặc định là phiên bản hiện tại của trình thông dịch.

   .. versionadded:: 3.14

.. option:: -O <level>
            --optimize <level>

   Mức tối ưu hóa cho parser. Mặc định không tối ưu hóa.

   .. versionadded:: 3.14

.. option:: --show-empty

   Hiển thị các danh sách rỗng và các trường có giá trị là ``None``. Mặc định không hiển thị các đối tượng rỗng.

   .. versionadded:: 3.14


Nếu chỉ định :file:`infile`, nội dung của nó sẽ được phân tích thành AST và xuất ra stdout. Nếu không, nội dung sẽ được đọc từ stdin.


.. seealso::

    `Green Tree Snakes <https://greentreesnakes.readthedocs.io/>`_, một tài nguyên tài liệu bên ngoài, cung cấp thông tin chi tiết hữu ích về cách làm việc với AST của Python.

    `ASTTokens <https://asttokens.readthedocs.io/en/latest/user-guide.html>`_ chú thích các AST của Python bằng vị trí của các token và văn bản trong mã nguồn đã tạo ra chúng. Điều này hữu ích cho các công cụ thực hiện chuyển đổi mã nguồn.

    `leoAst.py <https://leo-editor.github.io/leo-editor/appendices.html#leoast-py>`_ hợp nhất cách nhìn dựa trên token và cách nhìn dựa trên cây phân tích cú pháp của các chương trình Python bằng cách chèn các liên kết hai chiều giữa token và các nút ast.

    `LibCST <https://libcst.readthedocs.io/>`_ phân tích mã dưới dạng Concrete Syntax Tree, có cấu trúc giống cây ast và giữ lại mọi chi tiết định dạng. Thư viện này hữu ích để xây dựng các ứng dụng tự động tái cấu trúc mã (codemod) và linter.

    `Parso <https://parso.readthedocs.io>`_ là một trình phân tích cú pháp Python hỗ trợ khôi phục lỗi và phân tích cú pháp round-trip cho nhiều phiên bản Python (trên nhiều phiên bản Python). Parso cũng có thể liệt kê nhiều lỗi cú pháp trong tệp Python của bạn.

.. _`Green Tree Snakes`: https://greentreesnakes.readthedocs.io/
.. _`ASTTokens`: https://asttokens.readthedocs.io/en/latest/user-guide.html
.. _`leoAst.py`: https://leo-editor.github.io/leo-editor/appendices.html#leoast-py
.. _`LibCST`: https://libcst.readthedocs.io/
.. _`Parso`: https://parso.readthedocs.io
