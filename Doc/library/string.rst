:mod:`!string` --- Các thao tác chuỗi phổ biến
==============================================

.. module:: string
   :synopsis: Các thao tác chuỗi phổ biến.

**Mã nguồn:** :source:`Lib/string/__init__.py`

--------------


.. seealso::

   :ref:`textseq`

   :ref:`string-methods`

Các hằng chuỗi
--------------

Các hằng được định nghĩa trong mô-đun này là:


.. data:: ascii_letters

   Phép nối của các hằng :const:`ascii_lowercase` và :const:`ascii_uppercase` được mô tả dưới đây.  Giá trị này không phụ thuộc vào locale.


.. data:: ascii_lowercase

   Các chữ cái viết thường ``'abcdefghijklmnopqrstuvwxyz'``.  Giá trị này không phụ thuộc vào locale và sẽ không thay đổi.


.. data:: ascii_uppercase

   Các chữ cái viết hoa ``'ABCDEFGHIJKLMNOPQRSTUVWXYZ'``. Giá trị này không phụ thuộc vào locale và sẽ không thay đổi.


.. data:: digits

   Chuỗi ``'0123456789'``.


.. data:: hexdigits

   Chuỗi ``'0123456789abcdefABCDEF'``.


.. data:: octdigits

   Chuỗi ``'01234567'``.


.. data:: punctuation

   Chuỗi các ký tự ASCII được xem là ký tự dấu câu trong locale ``C``: ``!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~``.


.. data:: printable

   Chuỗi các ký tự ASCII được Python xem là có thể in được. Đây là sự kết hợp của :const:`digits`, :const:`ascii_letters`,
   :const:`punctuation`, và :const:`whitespace`.

   .. note::

      Theo thiết kế, :meth:`string.printable.isprintable() <str.isprintable>` trả về :const:`False`. Cụ thể, ``string.printable`` không thể in theo nghĩa POSIX (xem :manpage:`LC_CTYPE <locale(5)>`).


.. data:: whitespace

   Một chuỗi chứa tất cả các ký tự ASCII được xem là khoảng trắng. Chuỗi này bao gồm các ký tự khoảng trắng, tab, xuống dòng, về đầu dòng, xuống trang và tab dọc.


.. _string-formatting:

Định dạng chuỗi tùy chỉnh
-------------------------

Lớp chuỗi tích hợp cung cấp khả năng thực hiện việc thay thế biến và định dạng giá trị phức tạp thông qua phương thức :meth:`~str.format` được mô tả trong
:pep:`3101`. Lớp :class:`Formatter` trong module :mod:`!string` cho phép bạn tạo và tùy chỉnh hành vi định dạng chuỗi của riêng mình bằng cách sử dụng cùng cách triển khai như phương thức :meth:`~str.format` tích hợp.


.. class:: Formatter

   Lớp :class:`Formatter` có các phương thức public sau:

   .. method:: format(format_string, /, *args, **kwargs)

      Phương thức API chính. Phương thức này nhận một chuỗi định dạng cùng một tập hợp tùy ý các đối số vị trí và đối số từ khóa. Đây chỉ là một wrapper gọi :meth:`vformat`.

      .. versionchanged:: 3.7
         Đối số chuỗi định dạng giờ đây chỉ nhận theo vị trí (:ref:`positional-only <positional-only_parameter>`).

   .. method:: vformat(format_string, args, kwargs)

      Hàm này thực hiện công việc định dạng thực tế. Hàm được cung cấp riêng cho những trường hợp bạn muốn truyền vào một dictionary đối số đã được định nghĩa trước, thay vì giải nén rồi đóng gói lại dictionary thành các đối số riêng lẻ bằng cú pháp ``*args`` và ``**kwargs``. :meth:`vformat` thực hiện việc tách chuỗi định dạng thành dữ liệu ký tự và các trường thay thế. Hàm gọi các phương thức khác nhau được mô tả bên dưới.

   Ngoài ra, :class:`Formatter` định nghĩa một số phương thức được thiết kế để các subclass ghi đè:

   .. method:: parse(format_string)

      Lặp qua format_string và trả về một iterable gồm các tuple (*literal_text*, *field_name*, *format_spec*, *conversion*). :meth:`vformat` sử dụng giá trị này để tách chuỗi thành văn bản cố định hoặc các trường thay thế.

      Các giá trị trong tuple về mặt khái niệm biểu diễn một đoạn văn bản cố định, theo sau là một trường thay thế duy nhất. Nếu không có văn bản cố định (điều này có thể xảy ra khi hai trường thay thế xuất hiện liên tiếp), thì *literal_text* sẽ là một chuỗi có độ dài bằng không. Nếu không có trường thay thế, thì các giá trị của *field_name*, *format_spec* và *conversion* sẽ là ``None``. Giá trị của *field_name* không bị thay đổi và việc tự động đánh số các trường positional không đánh số được thực hiện bởi :meth:`vformat`.

   .. method:: get_field(field_name, args, kwargs)

      Với *field_name*, chuyển nó thành một object để định dạng. Việc tự động đánh số *field_name* được trả về từ :meth:`parse` được thực hiện bởi
      :meth:`vformat` trước khi gọi phương thức này. Trả về một tuple (obj, used_key). Phiên bản mặc định nhận các chuỗi có dạng được định nghĩa trong :pep:`3101`, chẳng hạn như "0[name]" hoặc "label.title". *args* và *kwargs* được truyền vào như đối với
      :meth:`vformat`. Giá trị trả về *used_key* có cùng ý nghĩa với tham số *key* của :meth:`get_value`.

   .. method:: get_value(key, args, kwargs)

      Truy xuất giá trị của một trường đã cho. Đối số *key* sẽ là một số nguyên hoặc một chuỗi. Nếu là số nguyên, nó biểu thị chỉ mục của đối số vị trí trong *args*; nếu là chuỗi, nó biểu thị một đối số có tên trong *kwargs*.

      Tham số *args* được đặt thành danh sách các đối số vị trí truyền vào
      :meth:`vformat`, còn tham số *kwargs* được đặt thành từ điển các đối số từ khóa.

      Đối với tên trường phức hợp, các hàm này chỉ được gọi cho thành phần đầu tiên của tên trường; các thành phần tiếp theo được xử lý thông qua các thao tác thuộc tính và lập chỉ mục thông thường.

      Ví dụ, biểu thức trường '0.name' sẽ khiến
      :meth:`get_value` được gọi với đối số *key* là 0. Thuộc tính ``name`` sẽ được tra cứu sau khi :meth:`get_value` trả về bằng cách gọi hàm tích hợp sẵn :func:`getattr`.

      Nếu chỉ mục hoặc từ khóa tham chiếu đến một mục không tồn tại, thì một
      :exc:`IndexError` hoặc :exc:`KeyError` nên được phát sinh.

   .. method:: check_unused_args(used_args, args, kwargs)

      Nếu muốn, hãy triển khai việc kiểm tra các đối số chưa được sử dụng.  Các đối số của hàm này là tập hợp tất cả các khóa đối số thực sự được tham chiếu trong chuỗi định dạng (số nguyên đối với các đối số vị trí và chuỗi đối với các đối số được đặt tên), cùng với một tham chiếu đến *args* và *kwargs* đã được truyền cho vformat.  Có thể tính tập hợp các đối số chưa được sử dụng từ những tham số này.  :meth:`check_unused_args` được giả định là sẽ phát sinh một ngoại lệ nếu việc kiểm tra không thành công.

   .. method:: format_field(value, format_spec)

      :meth:`format_field` chỉ gọi hàm dựng sẵn toàn cục :func:`format`.  Phương thức này được cung cấp để các lớp con có thể ghi đè.

   .. method:: convert_field(value, conversion)

      Chuyển đổi giá trị (do :meth:`get_field` trả về) theo một kiểu chuyển đổi (như trong tuple do phương thức :meth:`parse` trả về). Phiên bản mặc định hiểu các kiểu chuyển đổi 's' (str), 'r' (repr) và 'a' (ascii).


.. _formatstrings:

Cú pháp chuỗi định dạng
-----------------------

Phương thức :meth:`str.format` và lớp :class:`Formatter` sử dụng cùng một cú pháp cho các chuỗi định dạng (mặc dù trong trường hợp của :class:`Formatter`, các lớp con có thể định nghĩa cú pháp chuỗi định dạng riêng). Cú pháp này có liên quan đến :ref:`các literal chuỗi được định dạng <f-strings>` và
:ref:`các literal chuỗi template <t-strings>`, nhưng nó kém tinh vi hơn và đặc biệt là không hỗ trợ các biểu thức tùy ý trong phép nội suy.

.. index::
   single: {} (curly brackets); in string formatting
   single: . (dot); in string formatting
   single: [] (square brackets); in string formatting
   single: ! (exclamation); in string formatting
   single: : (colon); in string formatting

Chuỗi định dạng chứa các "trường thay thế" được bao quanh bởi dấu ngoặc nhọn ``{}``. Mọi nội dung không nằm trong dấu ngoặc nhọn được xem là văn bản literal và được sao chép nguyên trạng vào đầu ra. Nếu cần đưa ký tự ngoặc nhọn vào văn bản literal, bạn có thể escape bằng cách lặp đôi: ``{{`` và ``}}``.

Cú pháp cho một trường thay thế như sau:

.. productionlist:: format-string
   replacement_field: "{" [`field_name`] ["!" `conversion`] [":" `format_spec`] "}"
   field_name: `arg_name` ("." `attribute_name` | "[" `element_index` "]")*
   arg_name: [`~python-grammar:identifier` | `~python-grammar:digit`+]
   attribute_name: `~python-grammar:identifier`
   element_index: `~python-grammar:digit`+ | `index_string`
   index_string: <any source character except "]"> +
   conversion: "r" | "s" | "a"
   format_spec: `format-spec:format_spec`

Theo cách diễn đạt ít hình thức hơn, trường thay thế có thể bắt đầu bằng một *field_name* chỉ định đối tượng có giá trị sẽ được định dạng và chèn vào đầu ra thay cho trường thay thế. *field_name* có thể được theo sau bởi một trường *conversion* tùy chọn, đứng sau dấu chấm than ``'!'``, và một *format_spec*, đứng sau dấu hai chấm ``':'``. Các trường này chỉ định định dạng không mặc định cho giá trị thay thế.

Xem thêm :ref:`formatspec`.

Bản thân *field_name* bắt đầu bằng một *arg_name* có thể là một số hoặc một từ khóa. Nếu là số, nó tham chiếu đến một đối số vị trí; nếu là từ khóa, nó tham chiếu đến một đối số từ khóa có tên. Một *arg_name* được xem là một số nếu việc gọi :meth:`str.isdecimal` trên chuỗi trả về true. Nếu các arg_name dạng số trong một chuỗi định dạng là 0, 1, 2, ... theo thứ tự, bạn có thể bỏ qua tất cả chúng (không chỉ một số) và các số 0, 1, 2, ... sẽ được tự động chèn theo thứ tự đó. Vì *arg_name* không được phân cách bằng dấu nháy, bạn không thể chỉ định các khóa dictionary tùy ý (ví dụ: các chuỗi ``'10'`` hoặc ``':-]'``) trong một chuỗi định dạng. *arg_name* có thể được theo sau bởi bất kỳ số lượng biểu thức chỉ mục hoặc thuộc tính nào. Biểu thức có dạng ``'.name'`` chọn thuộc tính được đặt tên bằng :func:`getattr`, trong khi biểu thức có dạng ``'[index]'`` thực hiện tra cứu chỉ mục bằng :meth:`~object.__getitem__`.

.. versionchanged:: 3.1
   Có thể bỏ qua các bộ chỉ định đối số vị trí cho :meth:`str.format`, vì vậy ``'{} {}'.format(a, b)`` tương đương với ``'{0} {1}'.format(a, b)``.

.. versionchanged:: 3.4
   Có thể lược bỏ các chỉ định đối số vị trí cho :class:`Formatter`.

Một số ví dụ đơn giản về chuỗi định dạng::

   "First, thou shalt count to {0}"  # Tham chiếu đến đối số vị trí đầu tiên
   "Bring me a {}"                   # Ngầm tham chiếu đến đối số vị trí đầu tiên
   "From {} to {}"                   # Tương đương với "From {0} to {1}"
   "My quest is {name}"              # Tham chiếu đến đối số từ khóa 'name'
   "Weight in tons {0.weight}"       # Thuộc tính 'weight' của đối số vị trí đầu tiên
   "Units destroyed: {players[0]}"   # Phần tử đầu tiên của đối số từ khóa 'players'.

.. _formatstrings-conversion:

Trường *conversion* thực hiện việc ép kiểu trước khi định dạng. Thông thường, việc định dạng một giá trị do phương thức :meth:`~object.__format__` của chính giá trị đó thực hiện. Tuy nhiên, trong một số trường hợp, bạn nên buộc một kiểu được định dạng dưới dạng chuỗi, ghi đè định nghĩa định dạng riêng của kiểu đó. Bằng cách chuyển đổi giá trị thành chuỗi trước khi gọi :meth:`~object.__format__`, logic định dạng thông thường sẽ bị bỏ qua.

Hiện hỗ trợ ba cờ chuyển đổi: ``'!s'``, gọi :func:`str` trên giá trị; ``'!r'``, gọi :func:`repr`; và ``'!a'``, gọi
:func:`ascii`.

Một số ví dụ::

   "Harold's a clever {0!s}"        # Gọi str() trên đối số trước
   "Bring out the holy {name!r}"    # Gọi repr() trên đối số trước
   "More {!a}"                      # Gọi ascii() trên đối số trước

Trường *format_spec* chứa đặc tả về cách trình bày giá trị, bao gồm các chi tiết như độ rộng trường, căn chỉnh, phần đệm, độ chính xác thập phân, v.v. Mỗi kiểu giá trị có thể định nghĩa "ngôn ngữ mini về định dạng" hoặc cách diễn giải riêng cho *format_spec*.

Hầu hết các kiểu dựng sẵn đều hỗ trợ một ngôn ngữ mini về định dạng chung, được mô tả trong phần tiếp theo.

Trường *format_spec* cũng có thể chứa các trường thay thế lồng nhau bên trong. Những trường thay thế lồng nhau này có thể chứa tên trường, cờ chuyển đổi và đặc tả định dạng, nhưng không cho phép lồng sâu hơn. Các trường thay thế bên trong format_spec được thay thế trước khi chuỗi *format_spec* được diễn giải. Điều này cho phép chỉ định động cách định dạng một giá trị.

Xem :ref:`formatexamples` để biết một số ví dụ.


.. _formatspec:

Ngôn ngữ mini về đặc tả định dạng
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

"Đặc tả định dạng" được sử dụng bên trong các trường thay thế nằm trong một chuỗi định dạng để xác định cách trình bày từng giá trị (xem
:ref:`formatstrings`, :ref:`f-strings` và :ref:`t-strings`). Chúng cũng có thể được truyền trực tiếp cho kiểu dựng sẵn
:func:`format` function. Mỗi kiểu có thể định dạng có thể xác định cách diễn giải đặc tả định dạng.

Hầu hết các kiểu tích hợp sẵn đều triển khai các tùy chọn sau cho đặc tả định dạng, mặc dù một số tùy chọn định dạng chỉ được các kiểu số hỗ trợ.

Một quy ước chung là đặc tả định dạng rỗng tạo ra cùng kết quả như khi bạn gọi :func:`str` trên giá trị đó. Đặc tả định dạng không rỗng thường sửa đổi kết quả.

Dạng tổng quát của *standard format specifier* là:

.. productionlist:: format-spec
   format_spec: [`options`][`width_and_precision`][`type`]
   options: [[`fill`]`align`][`sign`]["z"]["#"]["0"]
   fill: <any character>
   align: "<" | ">" | "=" | "^"
   sign: "+" | "-" | " "
   width_and_precision: [`width_with_grouping`][`precision_with_grouping`]
   width_with_grouping: [`width`][`grouping`]
   precision_with_grouping: "." [`precision`][`grouping`] | "." `grouping`
   width: `~python-grammar:digit`+
   precision: `~python-grammar:digit`+
   grouping: "," | "_"
   type: "b" | "c" | "d" | "e" | "E" | "f" | "F" | "g"
       : | "G" | "n" | "o" | "s" | "x" | "X" | "%"

Nếu chỉ định một giá trị *align* hợp lệ, giá trị đó có thể được đặt trước bởi một ký tự *fill*, có thể là bất kỳ ký tự nào và mặc định là dấu cách nếu bị bỏ qua. Không thể sử dụng dấu ngoặc nhọn nguyên văn ("``{``" hoặc "``}``") làm ký tự *fill* trong :ref:`formatted string literal <f-strings>` hoặc khi sử dụng phương thức :meth:`str.format`. Tuy nhiên, có thể chèn dấu ngoặc nhọn bằng một trường thay thế lồng nhau. Hạn chế này không ảnh hưởng đến hàm :func:`format`.

Ý nghĩa của các tùy chọn căn chỉnh khác nhau như sau:

.. index::
   single: < (less); in string formatting
   single: > (greater); in string formatting
   single: = (equals); in string formatting
   single: ^ (caret); in string formatting

+----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Tùy chọn | Ý nghĩa                                                                                                                                                                                                                                                                                           |
+==========+===================================================================================================================================================================================================================================================================================================+
| ``'<'``  | Buộc trường được căn trái trong không gian khả dụng (đây là tùy chọn mặc định cho hầu hết các đối tượng).                                                                                                                                                                                         |
+----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``'>'``  | Buộc trường được căn phải trong không gian khả dụng (đây là tùy chọn mặc định cho các số).                                                                                                                                                                                                        |
+----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``'='``  | Buộc phần đệm được đặt sau dấu (nếu có) nhưng trước các chữ số. Tùy chọn này được dùng để in các trường theo dạng '+000000120'. Tùy chọn căn chỉnh này chỉ hợp lệ với các kiểu số, ngoại trừ :class:`complex`. Tùy chọn này trở thành mặc định cho các số khi '0' đứng ngay trước độ rộng trường. |
+----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``'^'``  | Buộc trường được căn giữa trong không gian khả dụng.                                                                                                                                                                                                                                              |
+----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

Lưu ý rằng trừ khi độ rộng tối thiểu của trường được xác định, độ rộng trường sẽ luôn bằng kích thước của dữ liệu dùng để điền vào trường, vì vậy tùy chọn căn chỉnh không có ý nghĩa trong trường hợp này.

Tùy chọn *sign* chỉ hợp lệ với các kiểu số và có thể là một trong những tùy chọn sau:

.. index::
   single: + (plus); in string formatting
   single: - (minus); in string formatting
   single: space; in string formatting

+----------+------------------------------------------------------------------------------------+
| Tùy chọn | Ý nghĩa                                                                            |
+==========+====================================================================================+
| ``'+'``  | Cho biết dấu sẽ được sử dụng cho cả số dương và số âm.                             |
+----------+------------------------------------------------------------------------------------+
| ``'-'``  | Cho biết dấu sẽ chỉ được sử dụng cho số âm (đây là hành vi mặc định).              |
+----------+------------------------------------------------------------------------------------+
| space    | Cho biết một khoảng trắng ở đầu sẽ được sử dụng cho số dương và dấu trừ cho số âm. |
+----------+------------------------------------------------------------------------------------+


.. index:: single: z; in string formatting

Tùy chọn ``'z'`` chuyển các giá trị số thực âm bằng không thành số thực dương bằng không sau khi làm tròn theo độ chính xác của định dạng. Tùy chọn này chỉ hợp lệ với các kiểu biểu diễn số thực.

.. versionchanged:: 3.11
   Đã thêm tùy chọn ``'z'`` (xem thêm :pep:`682`).

.. index:: single: # (hash); in string formatting

Tùy chọn ``'#'`` khiến dạng "thay thế" được sử dụng cho phép chuyển đổi. Dạng thay thế được định nghĩa khác nhau đối với từng kiểu. Tùy chọn này chỉ hợp lệ với các kiểu số nguyên, số thực và số phức. Đối với số nguyên, khi sử dụng đầu ra nhị phân, bát phân hoặc thập lục phân, tùy chọn này thêm tiền tố tương ứng ``'0b'``, ``'0o'``, ``'0x'`` hoặc ``'0X'`` vào giá trị đầu ra. Đối với số thực và số phức, dạng thay thế khiến kết quả chuyển đổi luôn chứa ký tự dấu thập phân, ngay cả khi không có chữ số nào theo sau. Thông thường, ký tự dấu thập phân chỉ xuất hiện trong kết quả của các phép chuyển đổi này nếu có một chữ số theo sau. Ngoài ra, đối với các phép chuyển đổi ``'g'`` và ``'G'``, các số 0 ở cuối không bị loại bỏ khỏi kết quả.

*width* là một số nguyên thập phân xác định độ rộng tối thiểu của toàn bộ trường, bao gồm mọi tiền tố, dấu phân cách và ký tự định dạng khác. Nếu không được chỉ định, độ rộng trường sẽ được xác định dựa trên nội dung.

Khi không chỉ định căn chỉnh rõ ràng, đặt ký tự số 0 (``'0'``) trước trường *width* sẽ bật tính năng đệm bằng số 0 có xét đến dấu cho các kiểu số, ngoại trừ :class:`complex`. Điều này tương đương với ký tự *fill* có giá trị ``'0'`` và kiểu *alignment* là ``'='``.

.. versionchanged:: 3.10
   Việc đặt ``'0'`` trước trường *width* không còn ảnh hưởng đến căn chỉnh mặc định của chuỗi.

*precision* là một số nguyên thập phân cho biết cần hiển thị bao nhiêu chữ số sau dấu thập phân đối với các kiểu trình bày ``'f'`` và ``'F'``, hoặc trước và sau dấu thập phân đối với các kiểu trình bày ``'g'`` hoặc ``'G'``. Đối với các kiểu trình bày chuỗi, trường này cho biết kích thước trường tối đa — nói cách khác, có bao nhiêu ký tự sẽ được sử dụng từ nội dung trường. Không cho phép *precision* đối với các kiểu trình bày số nguyên.

Tùy chọn *grouping* sau các trường *width* và *precision* chỉ định dấu phân cách nhóm chữ số tương ứng cho phần nguyên và phần thập phân của một số. Dấu này có thể là một trong các giá trị sau:

.. index::
   single: , (comma); in string formatting
   single: _ (underscore); in string formatting

+----------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Tùy chọn | Ý nghĩa                                                                                                                                                                                                                                                                                                                       |
+==========+===============================================================================================================================================================================================================================================================================================================================+
| ``','``  | Chèn dấu phẩy sau mỗi 3 chữ số đối với kiểu trình bày số nguyên ``'d'`` và các kiểu trình bày số dấu phẩy động, ngoại trừ ``'n'``. Đối với các kiểu trình bày khác, tùy chọn này không được hỗ trợ.                                                                                                                           |
+----------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``'_'``  | Chèn dấu gạch dưới sau mỗi 3 chữ số đối với kiểu trình bày số nguyên ``'d'`` và các kiểu trình bày số dấu phẩy động, ngoại trừ ``'n'``. Đối với các kiểu trình bày số nguyên ``'b'``, ``'o'``, ``'x'`` và ``'X'``, dấu gạch dưới được chèn sau mỗi 4 chữ số. Đối với các kiểu trình bày khác, tùy chọn này không được hỗ trợ. |
+----------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

Để sử dụng dấu phân cách phụ thuộc vào locale, hãy dùng ``'n'``
:ref:`kiểu trình bày float <n-format-float>` hoặc
:ref:`kiểu trình bày số nguyên <n-format-integer>` thay thế.

.. versionchanged:: 3.1
   Đã thêm tùy chọn ``','`` (xem thêm :pep:`378`).

.. versionchanged:: 3.6
   Đã thêm tùy chọn ``'_'`` (xem thêm :pep:`515`).

.. versionchanged:: 3.14
   Hỗ trợ tùy chọn *grouping* cho phần phân số.

Cuối cùng, *type* xác định cách dữ liệu được trình bày.

Các kiểu trình bày chuỗi hiện có là:

   +---------+------------------------------------------------------------------------+
   | Kiểu    | Ý nghĩa                                                                |
   +=========+========================================================================+
   | ``'s'`` | Định dạng chuỗi. Đây là kiểu mặc định cho chuỗi và có thể được bỏ qua. |
   +---------+------------------------------------------------------------------------+
   | None    | Giống như ``'s'``.                                                     |
   +---------+------------------------------------------------------------------------+

Các kiểu biểu diễn số nguyên hiện có là:

   +----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | Kiểu     | Ý nghĩa                                                                                                                                                                                                                                                                   |
   +==========+===========================================================================================================================================================================================================================================================================+
   | ``'b'``  | Định dạng nhị phân. Xuất số ở cơ số 2.                                                                                                                                                                                                                                    |
   +----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``'c'``  | Ký tự. Chuyển đổi số nguyên thành ký tự Unicode tương ứng trước khi in.                                                                                                                                                                                                   |
   +----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``'d'``  | Số nguyên thập phân. Xuất số ở cơ số 10.                                                                                                                                                                                                                                  |
   +----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``'o'``  | Định dạng bát phân. Xuất số ở cơ số 8.                                                                                                                                                                                                                                    |
   +----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``'x'``  | Định dạng thập lục phân. Xuất số ở cơ số 16, sử dụng chữ cái viết thường cho các chữ số lớn hơn 9.                                                                                                                                                                        |
   +----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``'X'``  | Định dạng thập lục phân. Xuất số ở cơ số 16, sử dụng chữ cái viết hoa cho các chữ số lớn hơn 9. Trong trường hợp ``'#'`` được chỉ định, tiền tố ``'0x'`` cũng sẽ được viết hoa thành ``'0X'``.                                                                            |
   +----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``'n'``  | .. _n-format-integer:                                                                                                                                                                                                                                                     |
   |          |                                                                                                                                                                                                                                                                           |
   |          | Số. Tương tự như ``'d'``, ngoại trừ việc sử dụng cài đặt locale hiện tại để chèn các dấu phân cách nhóm chữ số thích hợp. Lưu ý rằng locale mặc định không phải là locale hệ thống. Tùy thuộc vào trường hợp sử dụng, bạn có thể muốn đặt :const:`~locale.LC_NUMERIC` với |
   |          | :func:`locale.setlocale` trước khi sử dụng ``'n'``.                                                                                                                                                                                                                       |
   +----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | Không có | Giống như ``'d'``.                                                                                                                                                                                                                                                        |
   +----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

Ngoài các kiểu trình bày trên, số nguyên có thể được định dạng bằng các kiểu trình bày số dấu phẩy động được liệt kê bên dưới (ngoại trừ ``'n'`` và ``None``). Khi thực hiện việc này, :func:`float` được dùng để chuyển đổi số nguyên thành số dấu phẩy động trước khi định dạng.

Các kiểu trình bày có sẵn cho :class:`float` và
các giá trị :class:`~decimal.Decimal` là:

   +---------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | Kiểu    | Ý nghĩa                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
   +=========+=============================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================+
   | ``'e'`` | Ký hiệu khoa học. Với độ chính xác đã cho ``p``, định dạng số theo ký hiệu khoa học, trong đó chữ 'e' phân cách hệ số với số mũ. Hệ số có một chữ số trước dấu thập phân và ``p`` chữ số sau dấu thập phân, tổng cộng ``p + 1`` chữ số có nghĩa. Nếu không cung cấp độ chính xác, sử dụng độ chính xác gồm ``6`` chữ số sau dấu thập phân cho                                                                                                                                                                                                                                                                                               |
   |         | :class:`float`, và hiển thị tất cả các chữ số của hệ số cho :class:`~decimal.Decimal`. Nếu ``p=0``, dấu thập phân sẽ được bỏ qua trừ khi sử dụng tùy chọn ``#``.                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
   |         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
   |         | Đối với :class:`float`, số mũ luôn có ít nhất hai chữ số và bằng không nếu giá trị bằng không.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
   +---------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``'E'`` | Ký hiệu khoa học. Tương tự ``'e'``, ngoại trừ việc sử dụng chữ 'E' viết hoa làm ký tự phân cách.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
   +---------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``'f'`` | Ký hiệu dấu phẩy động cố định. Với độ chính xác đã cho ``p``, định dạng số dưới dạng số thập phân với chính xác ``p`` chữ số sau dấu thập phân. Nếu không cung cấp độ chính xác, sử dụng độ chính xác gồm ``6`` chữ số sau dấu thập phân cho :class:`float`, và sử dụng độ chính xác đủ lớn để hiển thị tất cả các chữ số của hệ số cho :class:`~decimal.Decimal`. Nếu ``p=0``, dấu thập phân sẽ được bỏ qua trừ khi sử dụng tùy chọn ``#``.                                                                                                                                                                                                |
   +---------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``'F'`` | Ký hiệu dấu phẩy động cố định. Tương tự ``'f'``, nhưng chuyển đổi ``nan`` thành ``NAN`` và ``inf`` thành ``INF``.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
   +---------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``'g'`` | Định dạng tổng quát. Với độ chính xác đã cho ``p >= 1``, làm tròn số đến ``p`` chữ số có nghĩa, sau đó định dạng kết quả theo định dạng dấu phẩy động cố định hoặc ký hiệu khoa học, tùy thuộc vào độ lớn của số. Độ chính xác ``0`` được xem là tương đương với độ chính xác ``1``.                                                                                                                                                                                                                                                                                                                                                        |
   |         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
   |         | Các quy tắc chính xác như sau: giả sử kết quả được định dạng với kiểu trình bày ``'e'`` và độ chính xác ``p-1`` sẽ có số mũ ``exp``. Sau đó, nếu ``m <= exp < p``, trong đó ``m`` là -4 đối với số thực dấu phẩy động và -6 đối với :class:`Decimals <decimal.Decimal>`, số này được định dạng với kiểu trình bày ``'f'`` và độ chính xác ``p-1-exp``. Nếu không, số này được định dạng với kiểu trình bày ``'e'`` và độ chính xác ``p-1``. Trong cả hai trường hợp, các số 0 ở cuối phần có nghĩa không đáng kể đều bị loại bỏ, đồng thời dấu thập phân cũng bị loại bỏ nếu không còn chữ số nào sau nó, trừ khi sử dụng tùy chọn ``'#'``. |
   |         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
   |         | Nếu không chỉ định độ chính xác, sử dụng độ chính xác gồm ``6`` chữ số có nghĩa cho :class:`float`. Đối với                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
   |         | :class:`~decimal.Decimal`, phần hệ số của kết quả được tạo từ các chữ số hệ số của giá trị; ký hiệu khoa học được sử dụng cho các giá trị có giá trị tuyệt đối nhỏ hơn ``1e-6`` và các giá trị mà giá trị vị trí của chữ số ít quan trọng nhất lớn hơn 1, còn ký hiệu số cố định được sử dụng trong các trường hợp khác.                                                                                                                                                                                                                                                                                                                    |
   |         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
   |         | Vô cực dương và âm, số 0 dương và âm, cùng các giá trị NaN, lần lượt được định dạng thành ``inf``, ``-inf``, ``0``, ``-0`` và ``nan``, bất kể độ chính xác.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
   +---------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``'G'`` | Định dạng tổng quát. Giống ``'g'``, nhưng chuyển sang ``'E'`` nếu số trở nên quá lớn. Các biểu diễn của vô cực và NaN cũng được viết hoa.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
   +---------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``'n'`` | .. _n-format-float:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
   |         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
   |         | Số. Giống ``'g'``, nhưng sử dụng thiết lập locale hiện tại để chèn các dấu phân cách nhóm chữ số thích hợp cho phần nguyên của một số. Lưu ý rằng locale mặc định không phải là locale của hệ thống. Tùy vào trường hợp sử dụng, bạn có thể muốn thiết lập                                                                                                                                                                                                                                                                                                                                                                                  |
   |         | :const:`~locale.LC_NUMERIC` bằng                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
   |         | :func:`locale.setlocale` trước khi sử dụng ``'n'``.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
   +---------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``'%'`` | Phần trăm. Nhân số đó với 100 và hiển thị ở định dạng (``'f'``) cố định, theo sau là dấu phần trăm.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
   +---------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | None    | Đối với :class:`float`, kiểu này tương tự kiểu ``'g'``, ngoại trừ việc khi dùng ký hiệu dấu phẩy động cố định để định dạng kết quả, nó luôn bao gồm ít nhất một chữ số sau dấu thập phân và chuyển sang ký hiệu khoa học khi ``exp >= p - 1``. Khi không chỉ định độ chính xác, phần sau sẽ lớn đến mức cần thiết để biểu diễn chính xác giá trị đã cho.                                                                                                                                                                                                                                                                                    |
   |         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
   |         | Đối với :class:`~decimal.Decimal`, kiểu này giống ``'g'`` hoặc ``'G'``, tùy thuộc vào giá trị của ``context.capitals`` trong decimal context hiện tại.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
   |         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
   |         | Hiệu ứng tổng thể là khớp với đầu ra của :func:`str` sau khi được điều chỉnh bởi các bổ từ định dạng khác.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
   +---------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

Kết quả phải được làm tròn chính xác đến độ chính xác ``p`` chữ số sau dấu thập phân. Chế độ làm tròn cho :class:`float` giống với chế độ của builtin :func:`round`. Đối với :class:`~decimal.Decimal`, chế độ làm tròn của :ref:`context <decimal-context>` hiện tại sẽ được sử dụng.

Các kiểu trình bày có sẵn cho :class:`complex` cũng giống như các kiểu dành cho
:class:`float` (``'%'`` không được phép). Cả phần thực và phần ảo của một số phức đều được định dạng dưới dạng số dấu phẩy động, theo kiểu trình bày được chỉ định. Chúng được phân tách bằng dấu bắt buộc của phần ảo; phần này kết thúc bằng hậu tố ``j``. Nếu thiếu kiểu trình bày, kết quả sẽ khớp với đầu ra của :func:`str` (các số phức có phần thực khác không cũng được đặt trong dấu ngoặc đơn), và có thể bị thay đổi bởi các bộ sửa định dạng khác.


.. _formatexamples:

Ví dụ về định dạng
^^^^^^^^^^^^^^^^^^

Phần này bao gồm các ví dụ về cú pháp :meth:`str.format` và so sánh với cách định dạng ``%`` cũ.

Trong hầu hết các trường hợp, cú pháp tương tự cách định dạng ``%`` cũ, với việc bổ sung ``{}`` và sử dụng ``:`` thay cho ``%``. Ví dụ: ``'%03.2f'`` có thể được chuyển thành ``'{:03.2f}'``.

Cú pháp định dạng mới cũng hỗ trợ các tùy chọn mới và khác biệt, như trong các ví dụ sau.

Truy cập các đối số theo vị trí::

   >>> '{0}, {1}, {2}'.format('a', 'b', 'c')
   'a, b, c'
   >>> '{}, {}, {}'.format('a', 'b', 'c')  # Chỉ dành cho 3.1+
   'a, b, c'
   >>> '{2}, {1}, {0}'.format('a', 'b', 'c')
   'c, b, a'
   >>> '{2}, {1}, {0}'.format(*'abc')      # giải nén chuỗi đối số
   'c, b, a'
   >>> '{0}{1}{0}'.format('abra', 'cad')   # có thể lặp lại chỉ số của các đối số
   'abracadabra'

Truy cập đối số theo tên::

   >>> 'Coordinates: {latitude}, {longitude}'.format(latitude='37.24N', longitude='-115.81W')
   'Coordinates: 37.24N, -115.81W'
   >>> coord = {'latitude': '37.24N', 'longitude': '-115.81W'}
   >>> 'Coordinates: {latitude}, {longitude}'.format(**coord)
   'Coordinates: 37.24N, -115.81W'

Truy cập thuộc tính của đối số::

   >>> c = 3-5j
   >>> ('The complex number {0} is formed from the real part {0.real} '
   ...  'and the imaginary part {0.imag}.').format(c)
   'The complex number (3-5j) is formed from the real part 3.0 and the imaginary part -5.0.'
   >>> class Point:
   ...     def __init__(self, x, y):
   ...         self.x, self.y = x, y
   ...     def __str__(self):
   ...         return 'Point({self.x}, {self.y})'.format(self=self)
   ...
   >>> str(Point(4, 2))
   'Point(4, 2)'

Truy cập phần tử của đối số::

   >>> coord = (3, 5)
   >>> 'X: {0[0]};  Y: {0[1]}'.format(coord)
   'X: 3;  Y: 5'

Thay thế ``%s`` và ``%r``::

   >>> "repr() shows quotes: {!r}; str() doesn't: {!s}".format('test1', 'test2')
   "repr() shows quotes: 'test1'; str() doesn't: test2"

Căn chỉnh văn bản và chỉ định độ rộng::

   >>> '{:<30}'.format('left aligned')
   'left aligned                  '
   >>> '{:>30}'.format('right aligned')
   '                 right aligned'
   >>> '{:^30}'.format('centered')
   '           centered           '
   >>> '{:*^30}'.format('centered')  # dùng '*' làm ký tự điền
   '***********centered***********'

Thay thế ``%+f``, ``%-f`` và ``% f``, đồng thời chỉ định dấu::

   >>> '{:+f}; {:+f}'.format(3.14, -3.14)  # luôn hiển thị dấu
   '+3.140000; -3.140000'
   >>> '{: f}; {: f}'.format(3.14, -3.14)  # hiển thị khoảng trắng cho các số dương
   ' 3.140000; -3.140000'
   >>> '{:-f}; {:-f}'.format(3.14, -3.14)  # chỉ hiển thị dấu trừ -- giống như '{:f}; {:f}'
   '3.140000; -3.140000'

Thay thế ``%x`` và ``%o``, đồng thời chuyển đổi giá trị sang các cơ số khác nhau::

   >>> # format cũng hỗ trợ các số nhị phân
   >>> "int: {0:d};  hex: {0:x};  oct: {0:o};  bin: {0:b}".format(42)
   'int: 42;  hex: 2a;  oct: 52;  bin: 101010'
   >>> # với 0x, 0o hoặc 0b làm tiền tố:
   >>> "int: {0:d};  hex: {0:#x};  oct: {0:#o};  bin: {0:#b}".format(42)
   'int: 42;  hex: 0x2a;  oct: 0o52;  bin: 0b101010'

Sử dụng dấu phẩy hoặc dấu gạch dưới làm dấu phân cách nhóm chữ số::

   >>> '{:,}'.format(1234567890)
   '1,234,567,890'
   >>> '{:_}'.format(1234567890)
   '1_234_567_890'
   >>> '{:_b}'.format(1234567890)
   '100_1001_1001_0110_0000_0010_1101_0010'
   >>> '{:_x}'.format(1234567890)
   '4996_02d2'
   >>> '{:_}'.format(123456789.123456789)
   '123_456_789.12345679'
   >>> '{:.,}'.format(123456789.123456789)
   '123456789.123,456,79'
   >>> '{:,._}'.format(123456789.123456789)
   '123,456,789.123_456_79'

Biểu diễn phần trăm::

   >>> points = 19
   >>> total = 22
   >>> 'Correct answers: {:.2%}'.format(points/total)
   'Correct answers: 86.36%'

Sử dụng định dạng dành riêng cho từng kiểu::

   >>> import datetime as dt
   >>> d = dt.datetime(2010, 7, 4, 12, 15, 58)
   >>> '{:%Y-%m-%d %H:%M:%S}'.format(d)
   '2010-07-04 12:15:58'

Lồng các đối số và các ví dụ phức tạp hơn::

   >>> for align, text in zip('<^>', ['left', 'center', 'right']):
   ...     '{0:{fill}{align}16}'.format(text, fill=align, align=align)
   ...
   'left<<<<<<<<<<<<'
   '^^^^^center^^^^^'
   '>>>>>>>>>>>right'
   >>>
   >>> octets = [192, 168, 0, 1]
   >>> '{:02X}{:02X}{:02X}{:02X}'.format(*octets)
   'C0A80001'
   >>> int(_, 16)
   3232235521
   >>>
   >>> width = 5
   >>> for num in range(5,12): #doctest: +NORMALIZE_WHITESPACE
   ...     for base in 'dXob':
   ...         print('{0:{width}{base}}'.format(num, base=base, width=width), end=' ')
   ...     print()
   ...
       5     5     5   101
       6     6     6   110
       7     7     7   111
       8     8    10  1000
       9     9    11  1001
      10     A    12  1010
      11     B    13  1011



.. _template-strings-pep292:

Chuỗi template ($-strings)
--------------------------

.. note::

   Tính năng được mô tả ở đây được giới thiệu trong Python 2.4; đây là một phương pháp tạo template đơn giản dựa trên regular expression. Nó có trước :meth:`str.format`, :ref:`formatted string literals <f-strings>`, và :ref:`template string literals <template-strings>`.

   Tính năng này không liên quan đến các literal chuỗi template (t-strings), được giới thiệu trong Python 3.14. Các literal này được đánh giá thành đối tượng :class:`string.templatelib.Template`, có trong module :mod:`string.templatelib`.

Chuỗi template cung cấp các phép thay thế chuỗi đơn giản hơn như được mô tả trong
:pep:`292`.  Một trường hợp sử dụng chính của chuỗi template là quốc tế hóa (i18n), vì trong ngữ cảnh đó, cú pháp và chức năng đơn giản hơn giúp việc dịch dễ dàng hơn so với các cơ chế format chuỗi tích hợp khác trong Python.  Để xem một package được xây dựng trên chuỗi template nhằm phục vụ i18n, hãy xem package `flufl.i18n <https://flufli18n.readthedocs.io/en/latest/>`_.

.. index:: single: $ (dollar); in template strings

Chuỗi template hỗ trợ các phép thay thế dựa trên ``$``, theo các quy tắc sau:

* ``$$`` là một escape; nó được thay thế bằng một ``$`` duy nhất.

* ``$identifier`` xác định một placeholder thay thế khớp với một khóa ánh xạ của ``"identifier"``. Theo mặc định, ``"identifier"`` bị giới hạn ở mọi chuỗi chữ và số ASCII không phân biệt chữ hoa chữ thường (bao gồm cả dấu gạch dưới), bắt đầu bằng dấu gạch dưới hoặc chữ cái ASCII. Ký tự đầu tiên không phải ký tự định danh xuất hiện sau ký tự ``$`` sẽ kết thúc đặc tả placeholder này.

* ``${identifier}`` tương đương với ``$identifier``. Nó là bắt buộc khi các ký tự định danh hợp lệ theo sau placeholder nhưng không thuộc về placeholder, chẳng hạn như ``"${noun}ification"``.

Mọi lần xuất hiện khác của ``$`` trong chuỗi sẽ khiến một :exc:`ValueError` được phát sinh.

Mô-đun :mod:`!string` cung cấp một lớp :class:`Template` triển khai các quy tắc này. Các phương thức của :class:`Template` là:


.. class:: Template(template)

   Hàm khởi tạo nhận một đối số duy nhất là chuỗi mẫu.


   .. method:: substitute(mapping={}, /, **kwds)

      Thực hiện phép thay thế mẫu và trả về một chuỗi mới. *mapping* là bất kỳ đối tượng nào giống dictionary có các khóa khớp với các placeholder trong mẫu. Ngoài ra, bạn có thể cung cấp các đối số từ khóa, trong đó tên từ khóa là các placeholder. Khi cả *mapping* và *kwds* đều được cung cấp và có các mục trùng lặp, các placeholder từ *kwds* sẽ được ưu tiên.


   .. method:: safe_substitute(mapping={}, /, **kwds)

      Tương tự như :meth:`substitute`, ngoại trừ việc nếu thiếu placeholder trong *mapping* và *kwds*, thay vì phát sinh một ngoại lệ :exc:`KeyError`, placeholder ban đầu sẽ xuất hiện nguyên vẹn trong chuỗi kết quả. Ngoài ra, không giống như :meth:`substitute`, mọi lần xuất hiện khác của ``$`` sẽ chỉ trả về ``$`` thay vì phát sinh :exc:`ValueError`.

      Mặc dù vẫn có thể xảy ra các ngoại lệ khác, phương thức này được gọi là "an toàn" vì luôn cố gắng trả về một chuỗi có thể sử dụng thay vì phát sinh ngoại lệ. Theo một nghĩa khác, :meth:`safe_substitute` có thể hoàn toàn không an toàn, vì nó sẽ âm thầm bỏ qua các template không đúng định dạng chứa các dấu phân cách còn sót lại, dấu ngoặc nhọn không khớp hoặc các placeholder không phải là định danh Python hợp lệ.


   .. method:: is_valid()

      Trả về ``False`` nếu template có các placeholder không hợp lệ sẽ khiến
      :meth:`substitute` phát sinh :exc:`ValueError`.

      .. versionadded:: 3.11


   .. method:: get_identifiers()

      Trả về danh sách các định danh hợp lệ trong template theo thứ tự chúng xuất hiện lần đầu, bỏ qua mọi định danh không hợp lệ.

      .. versionadded:: 3.11

   Các thực thể :class:`Template` cũng cung cấp một thuộc tính dữ liệu công khai:

   .. attribute:: template

      Đây là đối tượng được truyền vào đối số *template* của hàm khởi tạo. Nhìn chung, bạn không nên thay đổi nó, nhưng quyền truy cập chỉ đọc không được thực thi.

Dưới đây là ví dụ về cách sử dụng một Template::

   >>> from string import Template
   >>> s = Template('$who likes $what')
   >>> s.substitute(who='tim', what='kung pao')
   'tim likes kung pao'
   >>> d = dict(who='tim')
   >>> Template('Give $who $100').substitute(d)
   Traceback (most recent call last):
   ...
   ValueError: Invalid placeholder in string: line 1, col 11
   >>> Template('$who likes $what').substitute(d)
   Traceback (most recent call last):
   ...
   KeyError: 'what'
   >>> Template('$who likes $what').safe_substitute(d)
   'tim likes $what'

Cách sử dụng nâng cao: bạn có thể dẫn xuất các lớp con của :class:`Template` để tùy chỉnh cú pháp placeholder, ký tự phân cách hoặc toàn bộ regular expression được dùng để phân tích chuỗi template. Để thực hiện việc này, bạn có thể ghi đè các thuộc tính lớp sau:

* *delimiter* -- Đây là chuỗi literal mô tả delimiter mở đầu placeholder. Giá trị mặc định là ``$``. Lưu ý rằng giá trị này *không* nên là một regular expression, vì phần triển khai sẽ gọi
  :meth:`re.escape` trên chuỗi này khi cần. Cũng lưu ý rằng bạn không thể thay đổi delimiter sau khi lớp được tạo (tức là phải đặt một delimiter khác trong namespace lớp của lớp con).

* *idpattern* -- Đây là regular expression mô tả pattern cho các placeholder không có dấu ngoặc nhọn. Giá trị mặc định là regular expression ``(?a:[_a-z][_a-z0-9]*)``. Nếu giá trị này được cung cấp và *braceidpattern* là ``None``, pattern này cũng sẽ áp dụng cho các placeholder có dấu ngoặc nhọn.

  .. note::

     Vì *flags* mặc định là ``re.IGNORECASE``, pattern ``[a-z]`` có thể khớp với một số ký tự không phải ASCII. Đó là lý do chúng ta sử dụng flag ``a`` cục bộ ở đây.

  .. versionchanged:: 3.7
     *braceidpattern* có thể được dùng để định nghĩa các pattern riêng được sử dụng bên trong và bên ngoài dấu ngoặc nhọn.

* *braceidpattern* -- Tương tự như *idpattern* nhưng mô tả pattern cho các placeholder có dấu ngoặc nhọn. Mặc định là ``None``, nghĩa là quay về sử dụng *idpattern* (tức là cùng một pattern được sử dụng cả bên trong lẫn bên ngoài dấu ngoặc nhọn). Nếu được cung cấp, thuộc tính này cho phép bạn định nghĩa các pattern khác nhau cho placeholder có và không có dấu ngoặc nhọn.

  .. versionadded:: 3.7

* *flags* -- Các cờ của regular expression sẽ được áp dụng khi biên dịch regular expression dùng để nhận diện các phép thay thế. Giá trị mặc định là ``re.IGNORECASE``. Lưu ý rằng ``re.VERBOSE`` sẽ luôn được thêm vào các cờ, vì vậy các *idpattern*\ s tùy chỉnh phải tuân theo các quy ước dành cho regular expression ở chế độ verbose.

  .. versionadded:: 3.2

Ngoài ra, bạn có thể cung cấp toàn bộ mẫu regular expression bằng cách ghi đè thuộc tính lớp *pattern*. Nếu làm vậy, giá trị này phải là một chuỗi mẫu regular expression hoặc một đối tượng regular expression đã biên dịch, với bốn nhóm bắt có tên. Các nhóm bắt tương ứng với những quy tắc đã nêu ở trên, cùng với quy tắc placeholder không hợp lệ:

* *escaped* -- Nhóm này khớp với chuỗi escape, chẳng hạn như ``$$``, trong mẫu mặc định.

* *named* -- Nhóm này khớp với tên placeholder không có dấu ngoặc; tên này không được bao gồm delimiter trong nhóm bắt.

* *braced* -- Nhóm này khớp với tên placeholder được bao quanh bằng dấu ngoặc; tên này không được bao gồm delimiter hoặc các dấu ngoặc trong nhóm bắt.

* *invalid* -- Nhóm này khớp với mọi mẫu delimiter khác (thường là một delimiter đơn) và phải xuất hiện cuối cùng trong regular expression.

Các phương thức trên lớp này sẽ raise :exc:`ValueError` nếu mẫu khớp với template mà không có nhóm có tên nào trong số này khớp.


Các hàm hỗ trợ
--------------

.. function:: capwords(s, sep=None)

   Tách đối số thành các từ bằng :meth:`str.split`, viết hoa từng từ bằng :meth:`str.capitalize`, rồi nối các từ đã viết hoa bằng
   :meth:`str.join`.  Nếu đối số thứ hai tùy chọn *sep* không được cung cấp hoặc là ``None``, các chuỗi ký tự khoảng trắng được thay thế bằng một dấu cách duy nhất và khoảng trắng ở đầu và cuối được loại bỏ; nếu không, *sep* được dùng để tách và nối các từ.

.. _`flufl.i18n`: https://flufli18n.readthedocs.io/en/latest/
