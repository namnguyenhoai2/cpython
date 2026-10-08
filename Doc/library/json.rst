:mod:`!json` --- bộ mã hóa và giải mã JSON
==========================================

.. module:: json
   :synopsis: Mã hóa và giải mã định dạng JSON.

.. moduleauthor:: Bob Ippolito <bob@redivi.com>
.. sectionauthor:: Bob Ippolito <bob@redivi.com>

**Mã nguồn:** :source:`Lib/json/__init__.py`

--------------

`JSON (JavaScript Object Notation) <https://json.org>`_, được đặc tả bởi
:rfc:`7159` (thay thế :rfc:`4627`) và bởi `ECMA-404 <https://ecma-international.org/publications-and-standards/standards/ecma-404/>`_, là một định dạng trao đổi dữ liệu nhẹ lấy cảm hứng từ cú pháp literal đối tượng của `JavaScript <https://en.wikipedia.org/wiki/JavaScript>`_ (mặc dù không phải là một tập con thực sự của JavaScript [#rfc-errata]_ ).

.. note::
   Thuật ngữ "object" trong ngữ cảnh xử lý JSON bằng Python có thể gây nhầm lẫn. Mọi giá trị trong Python đều là object. Trong JSON, object chỉ bất kỳ dữ liệu nào được bao bọc trong dấu ngoặc nhọn, tương tự như một dictionary trong Python.

.. warning::
   Hãy thận trọng khi phân tích cú pháp dữ liệu JSON từ các nguồn không đáng tin cậy. Một chuỗi JSON độc hại có thể khiến decoder tiêu tốn đáng kể tài nguyên CPU và bộ nhớ. Bạn nên giới hạn kích thước dữ liệu cần phân tích cú pháp.

Mô-đun này cung cấp một API quen thuộc với người dùng thư viện chuẩn
:mod:`marshal` và :mod:`pickle` mô-đun.

Mã hóa các phân cấp đối tượng Python cơ bản::

    >>> import json
    >>> json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
    '["foo", {"bar": ["baz", null, 1.0, 2]}]'
    >>> print(json.dumps("\"foo\bar"))
    "\"foo\bar"
    >>> print(json.dumps('\u1234'))
    "\u1234"
    >>> print(json.dumps('\\'))
    "\\"
    >>> print(json.dumps({"c": 0, "b": 0, "a": 0}, sort_keys=True))
    {"a": 0, "b": 0, "c": 0}
    >>> from io import StringIO
    >>> io = StringIO()
    >>> json.dump(['streaming API'], io)
    >>> io.getvalue()
    '["streaming API"]'

Mã hóa gọn::

    >>> import json
    >>> json.dumps([1, 2, 3, {'4': 5, '6': 7}], separators=(',', ':'))
    '[1,2,3,{"4":5,"6":7}]'

In đẹp::

    >>> import json
    >>> print(json.dumps({'6': 7, '4': 5}, sort_keys=True, indent=4))
    {
        "4": 5,
        "6": 7
    }

Tùy chỉnh việc mã hóa đối tượng JSON::

   >>> import json
   >>> def custom_json(obj):
   ...     if isinstance(obj, complex):
   ...         return {'__complex__': True, 'real': obj.real, 'imag': obj.imag}
   ...     raise TypeError(f'Cannot serialize object of {type(obj)}')
   ...
   >>> json.dumps(1 + 2j, default=custom_json)
   '{"__complex__": true, "real": 1.0, "imag": 2.0}'

Giải mã JSON::

    >>> import json
    >>> json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]')
    ['foo', {'bar': ['baz', None, 1.0, 2]}]
    >>> json.loads('"\\"foo\\bar"')
    '"foo\x08ar'
    >>> from io import StringIO
    >>> io = StringIO('["streaming API"]')
    >>> json.load(io)
    ['streaming API']

Tùy chỉnh việc giải mã đối tượng JSON::

    >>> import json
    >>> def as_complex(dct):
    ...     if '__complex__' in dct:
    ...         return complex(dct['real'], dct['imag'])
    ...     return dct
    ...
    >>> json.loads('{"__complex__": true, "real": 1, "imag": 2}',
    ...     object_hook=as_complex)
    (1+2j)
    >>> import decimal
    >>> json.loads('1.1', parse_float=decimal.Decimal)
    Decimal('1.1')

Mở rộng :class:`JSONEncoder`::

    >>> import json
    >>> class ComplexEncoder(json.JSONEncoder):
    ...     def default(self, obj):
    ...         if isinstance(obj, complex):
    ...             return [obj.real, obj.imag]
    ...         # Để phương thức mặc định của lớp cơ sở phát sinh TypeError
    ...         return super().default(obj)
    ...
    >>> json.dumps(2 + 1j, cls=ComplexEncoder)
    '[2.0, 1.0]'
    >>> ComplexEncoder().encode(2 + 1j)
    '[2.0, 1.0]'
    >>> list(ComplexEncoder().iterencode(2 + 1j))
    ['[2.0', ', 1.0', ']']


Sử dụng :mod:`!json` từ shell để xác thực và in đẹp:

.. code-block:: shell-session

    $ echo '{"json":"obj"}' | python -m json
    {
        "json": "obj"
    }
    $ echo '{1.2:3.4}' | python -m json
    Expecting property name enclosed in double quotes: line 1 column 2 (char 1)

Xem :ref:`json-commandline` để biết tài liệu chi tiết.

.. note::

   JSON là một tập con của `YAML <https://yaml.org/>`_ 1.2. JSON được tạo bởi module này với các cài đặt mặc định (đặc biệt là giá trị *separators* mặc định) cũng là một tập con của YAML 1.0 và 1.1. Vì vậy, module này cũng có thể được dùng làm YAML serializer.

.. note::

   Theo mặc định, encoder và decoder của module này bảo toàn thứ tự đầu vào và đầu ra. Thứ tự chỉ bị mất nếu các container bên dưới không có thứ tự.


Cách sử dụng cơ bản
-------------------

.. function:: dump(obj, fp, *, skipkeys=False, ensure_ascii=True, \
                   check_circular=True, allow_nan=True, cls=None, \ indent=None, separators=None, default=None, \ sort_keys=False, ****kw)

   Tuần tự hóa *obj* thành một luồng có định dạng JSON tới *fp* (một đối tượng hỗ trợ ``.write()``
   :term:`file-like object`) bằng cách sử dụng :ref:`bảng chuyển đổi Python-sang-JSON <py-to-json-table>` này.

   .. note::

      Không giống như :mod:`pickle` và :mod:`marshal`, JSON không phải là một giao thức có khung, vì vậy việc cố gắng tuần tự hóa nhiều đối tượng bằng các lần gọi lặp lại tới
      :func:`dump` bằng cùng một *fp* sẽ dẫn đến một tệp JSON không hợp lệ.

   :param object obj:Đối tượng Python sẽ được tuần tự hóa.

   :param fp:Đối tượng giống tệp *obj* sẽ được tuần tự hóa vào. Mô-đun :mod:`!json` luôn tạo ra các đối tượng :class:`str`, không phải các đối tượng :class:`bytes`, do đó ``fp.write()`` phải hỗ trợ đầu vào :class:`str`.
   :type fp: :term:`file-like object`

   :param bool skipkeys:Nếu ``True``, các khóa không thuộc kiểu cơ bản (:class:`str`, :class:`int`, :class:`float`, :class:`bool`, ``None``) sẽ bị bỏ qua thay vì phát sinh :exc:`TypeError`. Mặc định là ``False``.

   :param bool ensure_ascii:Nếu ``True`` (mặc định), đầu ra được đảm bảo sẽ escape tất cả ký tự không phải ASCII và không in được trong dữ liệu đầu vào. Nếu ``False``, tất cả ký tự sẽ được xuất nguyên trạng, ngoại trừ các ký tự bắt buộc phải escape: dấu ngoặc kép, dấu gạch chéo ngược và các ký tự điều khiển từ U+0000 đến U+001F.

   :param bool check_circular:Nếu ``False``, việc kiểm tra tham chiếu vòng cho các kiểu container sẽ bị bỏ qua và một tham chiếu vòng sẽ dẫn đến :exc:`RecursionError` (hoặc tệ hơn). Mặc định là ``True``.

   :param bool allow_nan:Nếu ``False``, việc tuần tự hóa các giá trị :class:`float` nằm ngoài phạm vi (``nan``, ``inf``, ``-inf``) sẽ dẫn đến :exc:`ValueError`, tuân thủ nghiêm ngặt đặc tả JSON. Nếu ``True`` (mặc định), các giá trị tương đương trong JavaScript (``NaN``, ``Infinity``, ``-Infinity``) sẽ được sử dụng.

   :param cls:Nếu được đặt, một JSON encoder tùy chỉnh với
      phương thức :meth:`~JSONEncoder.default` được ghi đè, dùng để tuần tự hóa thành các kiểu dữ liệu tùy chỉnh. Nếu ``None`` (mặc định), :class:`!JSONEncoder` sẽ được sử dụng.
   :type cls: một lớp con :class:`JSONEncoder`

   :param indent:Nếu là một số nguyên dương hoặc chuỗi, các phần tử mảng JSON và thành viên đối tượng sẽ được định dạng đẹp với cấp độ thụt lề đó. Một số nguyên dương sẽ thụt lề theo số khoảng trắng tương ứng ở mỗi cấp; một chuỗi (chẳng hạn như ``"\t"``) được dùng để thụt lề cho mỗi cấp. Nếu bằng không, là số âm hoặc là ``""`` (chuỗi rỗng), chỉ chèn các dòng mới. Nếu là ``None`` (mặc định), không chèn dòng mới.
   :type indent: int | str | None

   :param separators:Một tuple gồm hai phần tử: ``(item_separator, key_separator)``. Nếu ``None`` (mặc định), *separators* mặc định là ``(', ', ': ')`` nếu *indent* là ``None``, và ``(',', ': ')`` nếu không. Để có JSON cô đọng nhất, chỉ định ``(',', ':')`` để loại bỏ khoảng trắng.
   :type separators: tuple | None

   :param default:Một hàm được gọi cho các đối tượng không thể được tuần tự hóa theo cách khác. Hàm này phải trả về một phiên bản của đối tượng có thể mã hóa thành JSON hoặc phát sinh một :exc:`TypeError`. Nếu là ``None`` (mặc định), :exc:`!TypeError` sẽ được phát sinh.
   :type default: :term:`callable` | None

   :param bool sort_keys:Nếu ``True``, các dictionary sẽ được xuất theo thứ tự sắp xếp của khóa. Mặc định là ``False``.

   .. note::

      Các khóa trong các cặp khóa/giá trị của JSON luôn có kiểu :class:`str`. Khi một dictionary được chuyển đổi thành JSON, tất cả các khóa của dictionary đều được chuyển đổi thành chuỗi. Do đó, nếu một dictionary được chuyển đổi thành JSON rồi обратно thành dictionary, dictionary đó có thể không bằng dictionary ban đầu. Nghĩa là, ``loads(dumps(x)) != x`` nếu x có các khóa không phải chuỗi. *sort_keys* sắp xếp các khóa trước khi chúng được chuyển đổi thành chuỗi, vì vậy các khóa dạng số được sắp xếp theo giá trị thay vì biểu diễn chuỗi của chúng.

   .. versionchanged:: 3.2
      Cho phép sử dụng chuỗi cho *indent* ngoài số nguyên.

   .. versionchanged:: 3.4
      Sử dụng ``(',', ': ')`` làm giá trị mặc định nếu *indent* không phải là ``None``.

   .. versionchanged:: 3.6
      Tất cả các tham số tùy chọn hiện là :ref:`keyword-only <keyword-only_parameter>`.


.. function:: dumps(obj, *, skipkeys=False, ensure_ascii=True, \
                    check_circular=True, allow_nan=True, cls=None, \ indent=None, separators=None, default=None, \ sort_keys=False, ****kw)

   Tuần tự hóa *obj* thành :class:`str` có định dạng JSON bằng cách sử dụng :ref:`conversion table <py-to-json-table>` này. Các đối số có cùng ý nghĩa như trong
   :func:`dump`.

.. function:: load(fp, *, cls=None, object_hook=None, parse_float=None, \
                   parse_int=None, parse_constant=None, \ object_pairs_hook=None, ****kw)

   Deserialize *fp* thành một đối tượng Python bằng cách sử dụng :ref:`bảng chuyển đổi JSON-sang-Python <json-to-py-table>`.

   :param fp:Một ``.read()``-hỗ trợ :term:`text file` hoặc :term:`binary file` chứa tài liệu JSON cần được giải tuần tự hóa.
   :type fp: :term:`file-like object`

   :param cls:Nếu được đặt, đây là một JSON decoder tùy chỉnh. Các đối số từ khóa bổ sung truyền cho :func:`!load` sẽ được chuyển đến hàm khởi tạo của *cls*. Nếu ``None`` (mặc định), :class:`!JSONDecoder` sẽ được sử dụng.
   :type cls: một lớp con của :class:`JSONDecoder`

   :param object_hook:Nếu được đặt, đây là một hàm được gọi với kết quả của mọi JSON object literal được giải mã (một :class:`dict`). Giá trị trả về của hàm này sẽ được sử dụng thay cho :class:`dict`. Tính năng này có thể được dùng để triển khai các decoder tùy chỉnh, chẳng hạn như gợi ý lớp `JSON-RPC <https://www.jsonrpc.org>`_. Mặc định là ``None``.
   :type object_hook: :term:`callable` | None

   :param object_pairs_hook:Nếu được đặt, đây là một hàm được gọi với kết quả của mọi literal đối tượng JSON được giải mã bằng một danh sách có thứ tự gồm các cặp. Giá trị trả về của hàm này sẽ được sử dụng thay cho :class:`dict`. Tính năng này có thể được dùng để triển khai các decoder tùy chỉnh. Nếu *object_hook* cũng được đặt, *object_pairs_hook* sẽ được ưu tiên. Mặc định là ``None``.
   :type object_pairs_hook: :term:`callable` | None

   :param parse_float:Nếu được đặt, đây là một hàm được gọi với chuỗi của mọi số thực JSON cần được giải mã. Nếu ``None`` (mặc định), nó tương đương với ``float(num_str)``. Có thể dùng cách này để phân tích số thực JSON thành các kiểu dữ liệu tùy chỉnh, chẳng hạn như :class:`decimal.Decimal`.
   :type parse_float: :term:`callable` | None

   :param parse_int:Nếu được đặt, đây là một hàm được gọi với chuỗi của mọi số nguyên JSON cần được giải mã. Nếu ``None`` (mặc định), nó tương đương với ``int(num_str)``. Có thể dùng cách này để phân tích số nguyên JSON thành các kiểu dữ liệu tùy chỉnh, chẳng hạn như :class:`float`.
   :type parse_int: :term:`callable` | None

   :param parse_constant:Nếu được đặt, đây là một hàm được gọi với một trong các chuỗi sau: ``'-Infinity'``, ``'Infinity'`` hoặc ``'NaN'``. Có thể dùng cách này để phát sinh ngoại lệ khi gặp các số JSON không hợp lệ. Mặc định là ``None``.
   :type parse_constant: :term:`callable` | None

   :raises JSONDecodeError:Khi dữ liệu đang được giải tuần tự không phải là một tài liệu JSON hợp lệ.

   :raises UnicodeDecodeError:Khi dữ liệu đang được giải tuần tự không chứa dữ liệu được mã hóa bằng UTF-8, UTF-16 hoặc UTF-32.

   .. versionchanged:: 3.1

      * Đã thêm tham số tùy chọn *object_pairs_hook*.
      * *parse_constant* không còn được gọi với 'null', 'true', 'false' nữa.

   .. versionchanged:: 3.6

      * Tất cả tham số tùy chọn hiện đều là :ref:`keyword-only <keyword-only_parameter>`.
      * *fp* giờ đây có thể là một :term:`binary file`. Mã hóa đầu vào phải là UTF-8, UTF-16 hoặc UTF-32.

   .. versionchanged:: 3.11
      Giá trị *parse_int* mặc định của :func:`int` hiện giới hạn độ dài tối đa của chuỗi số nguyên thông qua :ref:`giới hạn độ dài chuyển đổi chuỗi số nguyên <int_max_str_digits>` của trình thông dịch nhằm giúp ngăn chặn các cuộc tấn công từ chối dịch vụ.

.. function:: loads(s, *, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None, **kw)

   Giống hệt :func:`load`, nhưng thay vì một đối tượng giống tệp, giải tuần tự *s* (một thể hiện :class:`str`, :class:`bytes` hoặc :class:`bytearray` chứa tài liệu JSON) thành một đối tượng Python bằng cách sử dụng
   :ref:`bảng chuyển đổi <json-to-py-table>`.

   .. versionchanged:: 3.6
      *s* hiện có thể có kiểu :class:`bytes` hoặc :class:`bytearray`. Bảng mã đầu vào phải là UTF-8, UTF-16 hoặc UTF-32.

   .. versionchanged:: 3.9
      Đối số từ khóa *encoding* đã bị xóa.


Bộ mã hóa và bộ giải mã
-----------------------

.. class:: JSONDecoder(*, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, strict=True, object_pairs_hook=None)

   Bộ giải mã JSON đơn giản.

   Theo mặc định, thực hiện các phép chuyển đổi sau khi giải mã:

   .. _json-to-py-table:

   +-----------+--------+
   | JSON      | Python |
   +===========+========+
   | object    | dict   |
   +-----------+--------+
   | array     | list   |
   +-----------+--------+
   | chuỗi     | str    |
   +-----------+--------+
   | số (int)  | int    |
   +-----------+--------+
   | số (thực) | float  |
   +-----------+--------+
   | true      | True   |
   +-----------+--------+
   | false     | False  |
   +-----------+--------+
   | null      | None   |
   +-----------+--------+

   Nó cũng hiểu ``NaN``, ``Infinity`` và ``-Infinity`` là các giá trị ``float`` tương ứng của chúng, mặc dù điều này nằm ngoài đặc tả JSON.

   *object_hook* là một hàm tùy chọn được gọi với kết quả của mỗi đối tượng JSON đã được giải mã, và giá trị trả về của hàm sẽ được sử dụng thay cho :class:`dict` đã cho. Bạn có thể sử dụng hàm này để cung cấp các cơ chế deserialization tùy chỉnh (ví dụ: hỗ trợ gợi ý lớp `JSON-RPC <https://www.jsonrpc.org>`_).

   *object_pairs_hook* là một hàm tùy chọn được gọi với kết quả của mỗi đối tượng JSON được giải mã dưới dạng một danh sách có thứ tự các cặp. Giá trị trả về của *object_pairs_hook* sẽ được sử dụng thay cho
   :class:`dict`. Tính năng này có thể được dùng để triển khai các decoder tùy chỉnh. Nếu *object_hook* cũng được định nghĩa, *object_pairs_hook* sẽ được ưu tiên.

   .. versionchanged:: 3.1
      Đã bổ sung hỗ trợ cho *object_pairs_hook*.

   *parse_float* là một hàm tùy chọn được gọi với chuỗi biểu diễn của mỗi số thực JSON cần được giải mã. Theo mặc định, hàm này tương đương với ``float(num_str)``. Có thể dùng hàm này để sử dụng một kiểu dữ liệu hoặc parser khác cho các số thực JSON (ví dụ: :class:`decimal.Decimal`).

   *parse_int* là một hàm tùy chọn được gọi với chuỗi biểu diễn của mỗi số nguyên JSON cần được giải mã. Theo mặc định, hàm này tương đương với ``int(num_str)``. Có thể dùng hàm này để sử dụng một kiểu dữ liệu hoặc parser khác cho các số nguyên JSON (ví dụ: :class:`float`).

   *parse_constant* là một hàm tùy chọn được gọi với một trong các chuỗi sau: ``'-Infinity'``, ``'Infinity'``, ``'NaN'``. Có thể dùng hàm này để phát sinh một exception khi gặp các số JSON không hợp lệ.

   Nếu *strict* là false (``True`` là giá trị mặc định), các ký tự điều khiển sẽ được phép xuất hiện bên trong chuỗi. Trong ngữ cảnh này, ký tự điều khiển là các ký tự có mã ký tự trong phạm vi 0--31, bao gồm ``'\t'`` (tab), ``'\n'``, ``'\r'`` và ``'\0'``.

   Nếu dữ liệu được deserialize không phải là một tài liệu JSON hợp lệ, một
   :exc:`JSONDecodeError` sẽ được phát sinh.

   .. versionchanged:: 3.6
      Tất cả tham số hiện là :ref:`keyword-only <keyword-only_parameter>`.

   .. method:: decode(s)

      Trả về biểu diễn Python của *s* (một :class:`str` chứa một tài liệu JSON).

      :exc:`JSONDecodeError` sẽ được phát sinh nếu tài liệu JSON đã cho không hợp lệ.

   .. method:: raw_decode(s)

      Giải mã một tài liệu JSON từ *s* (một :class:`str` bắt đầu bằng một tài liệu JSON) và trả về một tuple 2 phần gồm biểu diễn Python và chỉ mục trong *s* tại đó tài liệu kết thúc.

      Có thể sử dụng cách này để giải mã một tài liệu JSON từ một chuỗi có thể có dữ liệu thừa ở cuối.


.. class:: JSONEncoder(*, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, sort_keys=False, indent=None, separators=None, default=None)

   Bộ mã hóa JSON có thể mở rộng cho các cấu trúc dữ liệu Python.

   Theo mặc định, hỗ trợ các đối tượng và kiểu sau:

   .. _py-to-json-table:

   +----------------------------------------+--------+
   | Python                                 | JSON   |
   +========================================+========+
   | dict                                   | object |
   +----------------------------------------+--------+
   | list, tuple                            | array  |
   +----------------------------------------+--------+
   | str                                    | string |
   +----------------------------------------+--------+
   | int, float, int- & float-derived Enums | number |
   +----------------------------------------+--------+
   | True                                   | true   |
   +----------------------------------------+--------+
   | False                                  | false  |
   +----------------------------------------+--------+
   | None                                   | null   |
   +----------------------------------------+--------+

   .. versionchanged:: 3.4
      Đã bổ sung hỗ trợ cho các lớp Enum kế thừa từ int và float.

   Để mở rộng khả năng này nhằm nhận diện các đối tượng khác, hãy tạo lớp con và triển khai
   phương thức :meth:`~JSONEncoder.default` cùng với một phương thức khác trả về một đối tượng có thể tuần tự hóa cho ``o`` nếu có thể; nếu không, phương thức đó nên gọi phần triển khai của lớp cha (để phát sinh :exc:`TypeError`).

   Nếu *skipkeys* là false (giá trị mặc định), một :exc:`TypeError` sẽ được raise khi cố gắng mã hóa các khóa không phải là :class:`str`, :class:`int`, :class:`float`,
   :class:`bool` hoặc ``None``. Nếu *skipkeys* là true, các mục như vậy sẽ đơn giản bị bỏ qua.

   Nếu *ensure_ascii* là true (giá trị mặc định), đầu ra được đảm bảo sẽ escape tất cả các ký tự đầu vào không phải ASCII và không in được. Nếu *ensure_ascii* là false, mọi ký tự sẽ được xuất nguyên trạng, ngoại trừ các ký tự bắt buộc phải escape: dấu ngoặc kép, dấu gạch chéo ngược và các ký tự điều khiển từ U+0000 đến U+001F.

   Nếu *check_circular* là true (giá trị mặc định), các list, dict và đối tượng được mã hóa tùy chỉnh sẽ được kiểm tra các tham chiếu vòng trong quá trình mã hóa để ngăn đệ quy vô hạn (sẽ gây ra một :exc:`RecursionError`). Nếu không, việc kiểm tra này sẽ không được thực hiện.

   Nếu *allow_nan* là true (giá trị mặc định), thì ``NaN``, ``Infinity`` và ``-Infinity`` sẽ được mã hóa như vậy. Hành vi này không tuân thủ đặc tả JSON, nhưng nhất quán với hầu hết các encoder và decoder dựa trên JavaScript. Nếu không, việc mã hóa các float như vậy sẽ gây ra :exc:`ValueError`.

   Nếu *sort_keys* là true (mặc định: ``False``), đầu ra của các dictionary sẽ được sắp xếp theo khóa; điều này hữu ích cho các regression test nhằm đảm bảo rằng các bản tuần tự hóa JSON có thể được so sánh hằng ngày.

   Nếu *indent* là một số nguyên không âm hoặc chuỗi, các phần tử mảng JSON và thành viên đối tượng sẽ được pretty-print với mức thụt lề đó. Mức thụt lề bằng 0, âm hoặc ``""`` chỉ chèn các dòng mới. ``None`` (giá trị mặc định) chọn biểu diễn gọn nhất. Sử dụng mức thụt lề là số nguyên dương sẽ thụt vào số khoảng trắng tương ứng ở mỗi cấp. Nếu *indent* là một chuỗi (chẳng hạn như ``"\t"``), chuỗi đó được dùng để thụt lề cho mỗi cấp.

   .. versionchanged:: 3.2
      Cho phép sử dụng chuỗi cho *indent* bên cạnh số nguyên.

   Nếu được chỉ định, *separators* phải là một tuple ``(item_separator, key_separator)``. Giá trị mặc định là ``(', ', ': ')`` nếu *indent* là ``None`` và ``(',', ': ')`` trong trường hợp ngược lại. Để có biểu diễn JSON gọn nhất, bạn nên chỉ định ``(',', ':')`` nhằm loại bỏ khoảng trắng.

   .. versionchanged:: 3.4
      Sử dụng ``(',', ': ')`` làm giá trị mặc định nếu *indent* không phải là ``None``.

   Nếu được chỉ định, *default* phải là một hàm được gọi cho các đối tượng không thể được serialize theo cách khác. Hàm này phải trả về một phiên bản của đối tượng có thể mã hóa thành JSON hoặc raise một :exc:`TypeError`. Nếu không được chỉ định, :exc:`TypeError` sẽ được raise.

   .. versionchanged:: 3.6
      Tất cả tham số hiện là :ref:`keyword-only <keyword-only_parameter>`.


   .. method:: default(o)

      Triển khai phương thức này trong một subclass để phương thức trả về một đối tượng có thể serialize cho *o*, hoặc gọi implementation của lớp cơ sở (để raise một
      :exc:`TypeError`).

      Ví dụ, để hỗ trợ các iterator tùy ý, bạn có thể triển khai
      :meth:`~JSONEncoder.default` như thế này::

         def default(self, o):
            try:
                iterable = iter(o)
            except TypeError:
                pass
            else:
                return list(iterable)
            # Để phương thức mặc định của lớp cơ sở ném TypeError
            return super().default(o)


   .. method:: encode(o)

      Trả về biểu diễn chuỗi JSON của một cấu trúc dữ liệu Python, *o*.  Ví dụ::

        >>> json.JSONEncoder().encode({"foo": ["bar", "baz"]})
        '{"foo": ["bar", "baz"]}'


   .. method:: iterencode(o)

      Mã hóa đối tượng đã cho, *o*, và tạo ra từng biểu diễn chuỗi khi có sẵn.  Ví dụ::

            for chunk in json.JSONEncoder().iterencode(bigobject):
                mysocket.write(chunk)


Ngoại lệ
--------

.. exception:: JSONDecodeError(msg, doc, pos)

   Lớp con của :exc:`ValueError` với các thuộc tính bổ sung sau:

   .. attribute:: msg

      Thông báo lỗi chưa được định dạng.

   .. attribute:: doc

      Tài liệu JSON đang được phân tích cú pháp.

   .. attribute:: pos

      Chỉ mục bắt đầu của *doc* tại đó quá trình phân tích cú pháp không thành công.

   .. attribute:: lineno

      Dòng tương ứng với *pos*.

   .. attribute:: colno

      Cột tương ứng với *pos*.

   .. versionadded:: 3.5


Tuân thủ tiêu chuẩn và khả năng tương tác
-----------------------------------------

Định dạng JSON được quy định bởi :rfc:`7159` và bởi `ECMA-404 <https://ecma-international.org/publications-and-standards/standards/ecma-404/>`_. Phần này trình bày mức độ tuân thủ RFC của module này. Để đơn giản, các lớp con :class:`JSONEncoder` và :class:`JSONDecoder`, cùng các tham số không được đề cập rõ ràng, không được xem xét.

Module này không tuân thủ RFC theo cách nghiêm ngặt, mà triển khai một số phần mở rộng hợp lệ trong JavaScript nhưng không hợp lệ trong JSON. Cụ thể:

- Các giá trị số vô hạn và NaN được chấp nhận và xuất ra;
- Các tên lặp lại trong một object được chấp nhận và chỉ giá trị của cặp tên-giá trị cuối cùng được sử dụng.

Vì RFC cho phép các parser tuân thủ RFC chấp nhận văn bản đầu vào không tuân thủ RFC, deserializer của module này về mặt kỹ thuật tuân thủ RFC với các thiết lập mặc định.

Mã hóa ký tự
^^^^^^^^^^^^

RFC yêu cầu JSON được biểu diễn bằng UTF-8, UTF-16 hoặc UTF-32, trong đó UTF-8 là mặc định được khuyến nghị để đạt khả năng tương tác tối đa.

Theo điều được RFC cho phép nhưng không bắt buộc, serializer của module này đặt *ensure_ascii=True* theo mặc định, nhờ đó escape đầu ra để các chuỗi kết quả chỉ chứa các ký tự ASCII có thể in được.

Ngoài tham số *ensure_ascii*, module này được định nghĩa hoàn toàn theo việc chuyển đổi giữa các object Python và
:class:`Unicode strings <str>`, và do đó không trực tiếp giải quyết vấn đề về mã hóa ký tự theo cách nào khác.

RFC cấm thêm dấu thứ tự byte (BOM) vào đầu văn bản JSON, và serializer của module này không thêm BOM vào đầu ra. RFC cho phép, nhưng không yêu cầu, deserializer JSON bỏ qua BOM ban đầu trong đầu vào. Deserializer của module này phát sinh :exc:`ValueError` khi có BOM ban đầu.

RFC không nghiêm cấm rõ ràng các chuỗi JSON chứa những chuỗi byte không tương ứng với các ký tự Unicode hợp lệ (ví dụ: các surrogate UTF-16 không ghép cặp), nhưng lưu ý rằng chúng có thể gây ra các vấn đề về khả năng tương tác. Theo mặc định, module này chấp nhận và xuất (khi có trong
:class:`str`) các điểm mã cho những chuỗi như vậy.


Các giá trị số vô hạn và NaN
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

RFC không cho phép biểu diễn các giá trị số vô hạn hoặc NaN. Mặc dù vậy, theo mặc định, module này chấp nhận và xuất ``Infinity``, ``-Infinity``, và ``NaN`` như thể chúng là các giá trị literal số JSON hợp lệ::

   >>> # Cả hai lệnh gọi này đều không phát sinh ngoại lệ, nhưng kết quả không phải là JSON hợp lệ
   >>> json.dumps(float('-inf'))
   '-Infinity'
   >>> json.dumps(float('nan'))
   'NaN'
   >>> # Tương tự khi giải tuần tự hóa
   >>> json.loads('-Infinity')
   -inf
   >>> json.loads('NaN')
   nan

Trong serializer, tham số *allow_nan* có thể được dùng để thay đổi hành vi này. Trong deserializer, tham số *parse_constant* có thể được dùng để thay đổi hành vi này.


Tên lặp lại trong một đối tượng
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

RFC quy định rằng các tên trong một đối tượng JSON phải là duy nhất, nhưng không bắt buộc cách xử lý các tên lặp lại trong đối tượng JSON. Theo mặc định, module này không phát sinh ngoại lệ; thay vào đó, nó bỏ qua tất cả cặp tên-giá trị ngoại trừ cặp cuối cùng đối với một tên nhất định::

   >>> weird_json = '{"x": 1, "x": 2, "x": 3}'
   >>> json.loads(weird_json)
   {'x': 3}

Tham số *object_pairs_hook* có thể được dùng để thay đổi hành vi này.


Giá trị cấp cao nhất không phải đối tượng và không phải mảng
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Phiên bản JSON cũ được quy định bởi :rfc:`4627` đã yêu cầu giá trị cấp cao nhất của một văn bản JSON phải là đối tượng hoặc mảng JSON (Python :class:`dict` hoặc :class:`list`), và không thể là giá trị null, boolean, số hoặc chuỗi JSON. :rfc:`7159` đã loại bỏ hạn chế đó, và module này không áp dụng, cũng chưa từng áp dụng, hạn chế đó trong serializer hoặc deserializer.

Dù vậy, để đạt khả năng tương tác tối đa, bạn có thể tự nguyện tuân thủ hạn chế này.


Hạn chế triển khai
^^^^^^^^^^^^^^^^^^

Một số triển khai bộ giải tuần tự JSON có thể đặt giới hạn đối với:

* kích thước của văn bản JSON được chấp nhận
* mức độ lồng nhau tối đa của các đối tượng và mảng JSON
* phạm vi và độ chính xác của các số JSON
* nội dung và độ dài tối đa của các chuỗi JSON

Mô-đun này không áp đặt bất kỳ giới hạn nào như vậy ngoài các giới hạn của chính những kiểu dữ liệu Python liên quan hoặc của chính trình thông dịch Python.

Khi tuần tự hóa sang JSON, hãy lưu ý mọi giới hạn như vậy trong các ứng dụng có thể sử dụng JSON của bạn. Cụ thể, các số JSON thường được giải tuần tự hóa thành số dấu phẩy động độ chính xác kép IEEE 754 và do đó chịu các giới hạn về phạm vi và độ chính xác của biểu diễn đó. Điều này đặc biệt liên quan khi tuần tự hóa các giá trị Python :class:`int` có độ lớn cực kỳ lớn hoặc khi tuần tự hóa các thực thể thuộc những kiểu số "exotic" như
:class:`decimal.Decimal`.


.. _json-commandline:
.. program:: json

Giao diện dòng lệnh
-------------------

.. module:: json.tool
    :synopsis: Giao diện dòng lệnh để xác thực và định dạng đẹp JSON.

**Mã nguồn:** :source:`Lib/json/tool.py`

--------------

Mô-đun :mod:`!json` có thể được gọi như một script thông qua ``python -m json`` để xác thực và định dạng đẹp các đối tượng JSON. Mô-đun con :mod:`!json.tool` triển khai giao diện này.

Nếu không chỉ định các đối số tùy chọn ``infile`` và ``outfile``, thì lần lượt sẽ sử dụng :data:`sys.stdin` và :data:`sys.stdout`:

.. code-block:: shell-session

    $ echo '{"json": "obj"}' | python -m json
    {
        "json": "obj"
    }
    $ echo '{1.2:3.4}' | python -m json
    Expecting property name enclosed in double quotes: line 1 column 2 (char 1)

.. versionchanged:: 3.5
   Kết quả hiện được sắp xếp theo cùng thứ tự với đầu vào. Sử dụng
   :option:`--sort-keys` tùy chọn để sắp xếp đầu ra của các từ điển theo thứ tự alphabet dựa trên khóa.

.. versionchanged:: 3.14
   Mô-đun :mod:`!json` giờ đây có thể được thực thi trực tiếp dưới dạng ``python -m json``. Để đảm bảo khả năng tương thích ngược, việc gọi CLI dưới dạng ``python -m json.tool`` vẫn được hỗ trợ.


Các tùy chọn dòng lệnh
^^^^^^^^^^^^^^^^^^^^^^

.. option:: infile

   Tệp JSON cần được xác thực hoặc định dạng đẹp:

   .. code-block:: shell-session

      $ python -m json mp_films.json
      [
          {
              "title": "And Now for Something Completely Different",
              "year": 1971
          },
          {
              "title": "Monty Python and the Holy Grail",
              "year": 1975
          }
      ]

   Nếu *infile* không được chỉ định, hãy đọc từ :data:`sys.stdin`.

.. option:: outfile

   Ghi đầu ra của *infile* vào *outfile* đã cho. Nếu không, ghi vào :data:`sys.stdout`.

.. option:: --sort-keys

   Sắp xếp đầu ra của các dictionary theo thứ tự bảng chữ cái dựa trên khóa.

   .. versionadded:: 3.5

.. option:: --no-ensure-ascii

   Tắt việc escape các ký tự không thuộc ASCII, xem :func:`json.dumps` để biết thêm thông tin.

   .. versionadded:: 3.9

.. option:: --json-lines

   Phân tích mỗi dòng đầu vào thành một đối tượng JSON riêng biệt.

   .. versionadded:: 3.8

.. option:: --indent, --tab, --no-indent, --compact

   Các tùy chọn loại trừ lẫn nhau để kiểm soát khoảng trắng.

   .. versionadded:: 3.9

.. option:: -h, --help

   Hiển thị thông báo trợ giúp.


.. rubric:: Chú thích cuối trang

.. [#rfc-errata] Như đã nêu trong `phần đính chính cho RFC 7159 <https://www.rfc-editor.org/errata_search.php?rfc=7159>`_, JSON cho phép các ký tự U+2028 (LINE SEPARATOR) và U+2029 (PARAGRAPH SEPARATOR) xuất hiện trực tiếp trong chuỗi, trong khi JavaScript (tính đến ECMAScript Edition 5.1) thì không.

.. _`JSON (JavaScript Object Notation)`: https://json.org
.. _`ECMA-404`: https://ecma-international.org/publications-and-standards/standards/ecma-404/
.. _`JavaScript`: https://en.wikipedia.org/wiki/JavaScript
.. _`YAML`: https://yaml.org/
.. _`JSON-RPC`: https://www.jsonrpc.org
.. _`the errata for RFC 7159`: https://www.rfc-editor.org/errata_search.php?rfc=7159
