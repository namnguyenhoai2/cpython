
.. _expressions:

*********
Biểu thức
*********

.. index:: expression, BNF

Chương này giải thích ý nghĩa của các thành phần trong biểu thức Python.

**Ghi chú cú pháp:** Trong chương này và các chương tiếp theo,
:ref:`ký hiệu ngữ pháp <notation>` sẽ được dùng để mô tả cú pháp, không phải phân tích từ vựng.

Khi (một lựa chọn của) quy tắc cú pháp có dạng:

.. productionlist:: python-grammar
   name: othername

và không có ngữ nghĩa nào được nêu, ngữ nghĩa của dạng ``name`` này giống với ngữ nghĩa của ``othername``.


.. _conversions:

Chuyển đổi số học
=================

.. index:: pair: arithmetic; conversion

Khi phần mô tả một toán tử số học dưới đây sử dụng cụm từ "các đối số số được chuyển đổi sang một kiểu thực chung", điều này có nghĩa là phần triển khai toán tử cho các kiểu số tích hợp sẵn hoạt động như được mô tả trong
:ref:`Các kiểu số <stdtypes-mixed-arithmetic>` của tài liệu thư viện chuẩn.

Một số quy tắc bổ sung áp dụng cho một số toán tử và toán hạng không phải số (ví dụ: một chuỗi làm đối số bên trái cho ``%`` toán tử). Các phần mở rộng phải tự định nghĩa cách chuyển đổi của mình.


.. _atoms:

Các atom
========

.. index:: atom

Atom là những phần tử cơ bản nhất của biểu thức. Các atom đơn giản nhất là :ref:`tên <identifiers>` hoặc literal. Các dạng được đặt trong dấu ngoặc đơn, ngoặc vuông hoặc ngoặc nhọn cũng được phân loại về mặt cú pháp là atom.

Về hình thức, cú pháp của atom là:

.. grammar-snippet::
   :group: python-grammar

   atom:
      | 'True'
      | 'False'
      | 'None'
      | '...'
      | `identifier`
      | `literal`
      | `enclosure`
   enclosure:
      | `parenth_form`
      | `list_display`
      | `dict_display`
      | `set_display`
      | `generator_expression`
      | `yield_atom`


.. _atom-singletons:

Hằng số tích hợp sẵn
--------------------

Các từ khóa ``True``, ``False`` và ``None`` đặt tên
:ref:`các hằng số dựng sẵn <built-in-consts>`. Token ``...`` đặt tên cho hằng số :py:data:`Ellipsis`.

Việc đánh giá các atom này cho ra giá trị tương ứng.

.. note::

   Một số hằng số dựng sẵn khác khả dụng dưới dạng biến toàn cục, nhưng chỉ những hằng số được đề cập ở đây mới là :ref:`từ khóa <keywords>`. Cụ thể, không thể gán lại hoặc sử dụng các tên này làm thuộc tính:

   .. code-block:: pycon

      >>> False = 123
        File "<input>", line 1
         False = 123
         ^^^^^
      SyntaxError: cannot assign to False

.. _atom-identifiers:

Định danh (Tên)
---------------

.. index:: name, identifier

Một định danh xuất hiện dưới dạng atom là một tên. Xem mục :ref:`identifiers` để biết định nghĩa từ vựng và mục :ref:`naming` để xem tài liệu về việc đặt tên và liên kết.

.. index:: pair: exception; NameError

Khi tên được liên kết với một đối tượng, việc đánh giá atom sẽ cho ra đối tượng đó. Khi một tên chưa được liên kết, nỗ lực đánh giá tên đó sẽ gây ra một ngoại lệ :exc:`NameError`.

.. _private-name-mangling:

.. index::
   pair: name; mangling
   pair: private; names

Biến đổi tên riêng tư
^^^^^^^^^^^^^^^^^^^^^

Khi một định danh xuất hiện dưới dạng văn bản trong định nghĩa lớp bắt đầu bằng từ hai ký tự gạch dưới trở lên và không kết thúc bằng từ hai ký tự gạch dưới trở lên, định danh đó được xem là :dfn:`tên riêng tư` của lớp đó.

.. seealso::

   :ref:`Các đặc tả lớp <class>`.

Cụ thể hơn, tên riêng tư được chuyển đổi thành dạng dài hơn trước khi mã được tạo cho chúng. Nếu tên sau khi chuyển đổi dài hơn 255 ký tự, việc cắt ngắn có thể xảy ra tùy theo triển khai.

Việc chuyển đổi không phụ thuộc vào ngữ cảnh cú pháp mà định danh được sử dụng, nhưng chỉ các định danh riêng tư sau đây mới được biến đổi:

- Mọi tên được sử dụng làm tên của một biến được gán hoặc đọc, hoặc mọi tên của một attribute đang được truy cập.

  Tuy nhiên, thuộc tính :attr:`~definition.__name__` của các hàm, lớp và bí danh kiểu lồng nhau không bị biến đổi tên.

- Tên của các mô-đun đã nhập, ví dụ ``__spam`` trong ``import __spam``. Nếu mô-đun là một phần của một package (tức là tên của nó chứa dấu chấm), tên đó *không* bị biến đổi, ví dụ, ``__foo`` trong ``import __foo.bar`` không bị biến đổi.

- Tên của một thành phần đã nhập, ví dụ ``__f`` trong ``from spam import __f``.

Quy tắc biến đổi được định nghĩa như sau:

- Tên lớp, sau khi loại bỏ các dấu gạch dưới ở đầu và thêm một dấu gạch dưới đơn ở đầu, được chèn vào trước định danh; ví dụ, định danh ``__spam`` xuất hiện trong một lớp có tên ``Foo``, ``_Foo`` hoặc ``__Foo`` sẽ được biến đổi thành ``_Foo__spam``.

- Nếu tên lớp chỉ gồm các dấu gạch dưới, phép biến đổi giữ nguyên định danh, ví dụ, định danh ``__spam`` xuất hiện trong một lớp có tên ``_`` hoặc ``__`` sẽ được giữ nguyên.

.. _atom-literals:

Các literal
-----------

.. index:: single: literal

Một :dfn:`literal` là biểu diễn dạng văn bản của một giá trị. Python hỗ trợ các literal số, chuỗi và byte.
:ref:`Format strings <f-strings>` và :ref:`template strings <t-strings>` được xem là các string literal.

Numeric literal bao gồm một :token:`NUMBER <python-grammar:NUMBER>` token duy nhất, dùng để chỉ một số nguyên, số dấu phẩy động hoặc số ảo. Xem phần :ref:`numbers` trong tài liệu Lexical analysis để biết thêm chi tiết.

String literal và bytes literal có thể bao gồm nhiều token. Xem phần :ref:`string-concatenation` để biết thêm chi tiết.

Lưu ý rằng các số âm và số phức, chẳng hạn như ``-3`` hoặc ``3+4.2j``, về mặt cú pháp không phải là literal, mà là :ref:`unary <unary>` hoặc
:ref:`binary <binary>` arithmetic operation liên quan đến toán tử ``-`` hoặc ``+``.

Việc đánh giá một literal tạo ra một object thuộc kiểu đã cho (:class:`int`, :class:`float`, :class:`complex`, :class:`str`,
:class:`bytes`, hoặc :class:`~string.templatelib.Template`) với giá trị đã cho. Giá trị có thể được xấp xỉ trong trường hợp floating-point literal và imaginary literal.

Ngữ pháp hình thức cho các literal là:

.. grammar-snippet::
   :group: python-grammar

   literal: `strings` | `NUMBER`


.. index::
   triple: immutable; data; type
   pair: immutable; object

Literal và danh tính đối tượng
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Tất cả literal đều tương ứng với các kiểu dữ liệu bất biến, vì vậy danh tính của đối tượng ít quan trọng hơn giá trị của nó. Nhiều lần đánh giá các literal có cùng giá trị (dù là cùng một lần xuất hiện trong văn bản chương trình hay các lần xuất hiện khác nhau) có thể nhận được cùng một đối tượng hoặc các đối tượng khác nhau có cùng giá trị.

.. admonition:: Chi tiết triển khai CPython

   Ví dụ, trong CPython, các số nguyên *nhỏ* có cùng giá trị sẽ được đánh giá thành cùng một đối tượng::

      >>> x = 7
      >>> y = 7
      >>> x is y
      True

   Tuy nhiên, các số nguyên lớn sẽ được đánh giá thành các đối tượng khác nhau::

      >>> x = 123456789
      >>> y = 123456789
      >>> x is y
      False

   Hành vi này có thể thay đổi trong các phiên bản CPython tương lai. Cụ thể, ranh giới giữa các số nguyên "nhỏ" và "lớn" trước đây đã từng thay đổi.

   CPython sẽ phát ra một :py:exc:`SyntaxWarning` khi bạn so sánh các literal bằng ``is``::

      >>> x = 7
      >>> x is 7
      <input>:1: SyntaxWarning: "is" with 'int' literal. Did you mean "=="?
      True

   Xem :ref:`faq-identity-with-is` để biết thêm thông tin.

:ref:`Template strings <t-strings>` là bất biến nhưng có thể tham chiếu đến các đối tượng khả biến dưới dạng giá trị :class:`~string.templatelib.Interpolation`. Trong phạm vi của phần này, hai t-string được coi là có "cùng giá trị" nếu cả cấu trúc của chúng và *identity* của các giá trị đều khớp nhau.

.. impl-detail::

   Hiện tại, mỗi lần đánh giá một template string đều tạo ra một đối tượng khác.


.. _string-concatenation:

Phép nối literal chuỗi
^^^^^^^^^^^^^^^^^^^^^^

Có thể sử dụng nhiều literal chuỗi hoặc bytes liền kề nhau, có thể theo các quy ước trích dẫn khác nhau, và ý nghĩa của chúng giống với phép nối các literal đó::

   >>> "hello" 'world'
   "helloworld"

Tính năng này được định nghĩa ở cấp độ cú pháp, vì vậy chỉ hoạt động với các literal. Để nối các biểu thức chuỗi trong thời gian chạy, có thể sử dụng toán tử '+'::

   >>> greeting = "Hello"
   >>> space = " "
   >>> name = "Blaise"
   >>> print(greeting + space + name)   # không phải: print(greeting space name)
   Hello Blaise

Có thể tự do kết hợp string literal thông thường, string literal được đặt trong ba dấu nháy và formatted string literal. Ví dụ::

   >>> "Hello" r', ' f"{name}!"
   "Hello, Blaise!"

Có thể sử dụng tính năng này để giảm số lượng dấu gạch chéo ngược cần dùng, thuận tiện chia các chuỗi dài thành nhiều dòng dài, hoặc thậm chí thêm chú thích vào các phần của chuỗi. Ví dụ::

   re.compile("[A-Za-z_]"       # chữ cái hoặc dấu gạch dưới
              "[A-Za-z0-9_]*"   # chữ cái, chữ số hoặc dấu gạch dưới
             )

Tuy nhiên, bytes literal chỉ có thể được kết hợp với các bytes literal khác, không thể kết hợp với string literal thuộc bất kỳ loại nào. Ngoài ra, template string literal chỉ có thể được kết hợp với các template string literal khác::

   >>> t"Hello" t"{name}!"
   Template(strings=('Hello', '!'), interpolations=(...))

Về mặt hình thức:

.. grammar-snippet::
   :group: python-grammar

   strings: (`STRING` | `fstring`)+ | `tstring`+


.. _parenthesized:

Dạng có dấu ngoặc
-----------------

.. index::
   single: parenthesized form
   single: () (parentheses); tuple display

Dạng có dấu ngoặc là một danh sách biểu thức tùy chọn được đặt trong dấu ngoặc đơn:

.. productionlist:: python-grammar
   parenth_form: "(" [`starred_expression`] ")"

Danh sách biểu thức có dấu ngoặc cho kết quả giống như danh sách biểu thức đó: nếu danh sách chứa ít nhất một dấu phẩy, nó cho kết quả là một tuple; nếu không, nó cho kết quả là biểu thức duy nhất tạo nên danh sách biểu thức đó.

.. index:: pair: empty; tuple

Một cặp dấu ngoặc đơn rỗng cho kết quả là một đối tượng tuple rỗng. Vì tuple là bất biến, các quy tắc tương tự như đối với literal được áp dụng (tức là hai lần xuất hiện của tuple rỗng có thể cho kết quả là cùng một đối tượng hoặc không).

.. index::
   single: comma
   single: , (comma)

Lưu ý rằng tuple không được tạo bởi dấu ngoặc, mà bởi việc sử dụng dấu phẩy. Ngoại lệ là tuple rỗng, đối với tuple này, dấu ngoặc *là* bắt buộc --- việc cho phép "không có gì" không đặt trong ngoặc trong các biểu thức sẽ gây ra sự mơ hồ và cho phép các lỗi gõ phổ biến không bị phát hiện.


.. _comprehensions:

Biểu diễn danh sách, tập hợp và từ điển
---------------------------------------

.. index:: single: comprehensions

Để tạo một danh sách, một tập hợp hoặc một từ điển, Python cung cấp cú pháp đặc biệt gọi là "biểu diễn", mỗi loại có hai dạng:

* hoặc nội dung của container được liệt kê một cách tường minh, hoặc

* được tính thông qua một tập hợp các chỉ dẫn lặp và lọc, gọi là
  :dfn:`comprehension`.

.. index::
   single: for; in comprehensions
   single: if; in comprehensions
   single: async for; in comprehensions

Các thành phần cú pháp phổ biến của comprehension là:

.. productionlist:: python-grammar
   comprehension: `assignment_expression` `comp_for`
   comp_for: ["async"] "for" `target_list` "in" `or_test` [`comp_iter`]
   comp_iter: `comp_for` | `comp_if`
   comp_if: "if" `or_test` [`comp_iter`]

Comprehension bao gồm một biểu thức duy nhất, theo sau là ít nhất một
:keyword:`!for` mệnh đề và không hoặc có thêm một hay nhiều mệnh đề :keyword:`!for` hoặc :keyword:`!if`. Trong trường hợp này, các phần tử của container mới là những phần tử sẽ được tạo ra bằng cách coi mỗi mệnh đề :keyword:`!for` hoặc :keyword:`!if` như một khối, lồng từ trái sang phải, rồi đánh giá biểu thức để tạo ra một phần tử mỗi khi đến khối trong cùng.

Tuy nhiên, ngoại trừ biểu thức iterable trong mệnh đề :keyword:`!for` ngoài cùng bên trái, comprehension được thực thi trong một phạm vi lồng nhau ngầm riêng biệt. Điều này đảm bảo rằng các tên được gán trong danh sách đích không “rò rỉ” vào phạm vi bao quanh.

Biểu thức iterable trong mệnh đề :keyword:`!for` ngoài cùng bên trái được đánh giá trực tiếp trong phạm vi bao quanh, sau đó được truyền dưới dạng đối số cho phạm vi lồng nhau ngầm định. Các mệnh đề :keyword:`!for` tiếp theo và mọi điều kiện lọc trong mệnh đề :keyword:`!for` ngoài cùng bên trái không thể được đánh giá trong phạm vi bao quanh vì chúng có thể phụ thuộc vào các giá trị nhận được từ iterable ngoài cùng bên trái. Ví dụ: ``[x*y for x in range(10) for y in range(x, x+10)]``.

Để đảm bảo phép hiểu luôn cho kết quả là một container thuộc kiểu thích hợp, các biểu thức ``yield`` và ``yield from`` bị cấm trong phạm vi lồng nhau ngầm định.

.. index::
   single: await; in comprehensions

Kể từ Python 3.6, trong một hàm :keyword:`async def`, có thể sử dụng mệnh đề :keyword:`!async for` để lặp qua một :term:`asynchronous iterator`. Phép hiểu trong một hàm :keyword:`!async def` có thể bao gồm một trong hai
mệnh đề :keyword:`!for` hoặc :keyword:`!async for` theo sau biểu thức mở đầu, có thể chứa thêm các mệnh đề :keyword:`!for` hoặc :keyword:`!async for`, và cũng có thể sử dụng các biểu thức :keyword:`await`.

Nếu một phép hiểu chứa các mệnh đề :keyword:`!async for`, hoặc nếu nó chứa
các biểu thức :keyword:`!await` hoặc các phép hiểu bất đồng bộ khác ở bất kỳ vị trí nào ngoại trừ biểu thức iterable trong mệnh đề :keyword:`!for` ngoài cùng bên trái, thì nó được gọi là một
:dfn:`phép hiểu bất đồng bộ`. Một phép hiểu bất đồng bộ có thể tạm dừng việc thực thi của hàm coroutine nơi nó xuất hiện. Xem thêm :pep:`530`.

.. versionadded:: 3.6
   Phép comprehension bất đồng bộ đã được giới thiệu.

.. versionchanged:: 3.8
   ``yield`` và ``yield from`` không được phép trong phạm vi lồng nhau ngầm định.

.. versionchanged:: 3.11
   Các phép comprehension bất đồng bộ hiện được phép sử dụng bên trong các phép comprehension trong những hàm bất đồng bộ. Các phép comprehension bên ngoài sẽ mặc định trở thành bất đồng bộ.


.. _lists:

Biểu thức hiển thị danh sách
----------------------------

.. index::
   pair: list; display
   pair: list; comprehensions
   pair: empty; list
   pair: object; list
   single: [] (square brackets); list expression
   single: , (comma); expression list

Biểu thức hiển thị danh sách là một chuỗi biểu thức có thể rỗng, được đặt trong dấu ngoặc vuông:

.. productionlist:: python-grammar
   list_display: "[" [`flexible_expression_list` | `comprehension`] "]"

Biểu thức hiển thị danh sách tạo ra một đối tượng danh sách mới; nội dung của danh sách được xác định bằng một danh sách biểu thức hoặc một phép comprehension. Khi cung cấp một danh sách biểu thức được phân tách bằng dấu phẩy, các phần tử của danh sách được đánh giá từ trái sang phải và được đặt vào đối tượng danh sách theo thứ tự đó. Khi cung cấp một phép comprehension, danh sách được tạo từ các phần tử tạo ra bởi phép comprehension.


.. _set:

Biểu thức hiển thị tập hợp
--------------------------

.. index::
   pair: set; display
   pair: set; comprehensions
   pair: object; set
   single: {} (curly brackets); set expression
   single: , (comma); expression list

Biểu thức hiển thị tập hợp được ký hiệu bằng dấu ngoặc nhọn và có thể phân biệt với biểu thức hiển thị từ điển nhờ không có dấu hai chấm ngăn cách khóa và giá trị:

.. productionlist:: python-grammar
   set_display: "{" (`flexible_expression_list` | `comprehension`) "}"

Biểu thức hiển thị tập hợp tạo ra một đối tượng tập hợp mới có thể thay đổi, với nội dung được xác định bằng một chuỗi biểu thức hoặc một phép dựng tập hợp (comprehension). Khi cung cấp một danh sách biểu thức được phân tách bằng dấu phẩy, các phần tử của danh sách được đánh giá từ trái sang phải và thêm vào đối tượng tập hợp. Khi cung cấp một phép dựng tập hợp, tập hợp được tạo từ các phần tử là kết quả của phép dựng tập hợp đó.

Không thể tạo một tập hợp rỗng bằng ``{}``; literal này tạo ra một từ điển rỗng.


.. _dict:

Biểu thức hiển thị từ điển
--------------------------

.. index::
   pair: dictionary; display
   pair: dictionary; comprehensions
   key, value, key/value pair
   pair: object; dictionary
   single: {} (curly brackets); dictionary expression
   single: : (colon); in dictionary expressions
   single: , (comma); in dictionary displays

Biểu thức hiển thị từ điển là một chuỗi có thể rỗng gồm các mục từ điển (cặp khóa/giá trị) được đặt trong dấu ngoặc nhọn:

.. productionlist:: python-grammar
   dict_display: "{" [`dict_item_list` | `dict_comprehension`] "}"
   dict_item_list: `dict_item` ("," `dict_item`)* [","]
   dict_item: `expression` ":" `expression` | "**" `or_expr`
   dict_comprehension: `expression` ":" `expression` `comp_for`

Biểu thức hiển thị từ điển tạo ra một đối tượng từ điển mới.

Nếu cung cấp một chuỗi các mục từ điển được phân tách bằng dấu phẩy, các mục này được đánh giá từ trái sang phải để xác định các mục nhập của từ điển: mỗi đối tượng khóa được dùng làm khóa trong từ điển để lưu trữ giá trị tương ứng. Điều này có nghĩa là bạn có thể chỉ định cùng một khóa nhiều lần trong danh sách mục từ điển và giá trị cuối cùng của từ điển cho khóa đó sẽ là giá trị được chỉ định sau cùng.

.. index::
   unpacking; dictionary
   single: **; in dictionary displays

Hai dấu sao ``**`` biểu thị :dfn:`giải nén dictionary`. Toán hạng của nó phải là một :term:`mapping`. Mỗi mục trong mapping được thêm vào dictionary mới. Các giá trị xuất hiện sau sẽ thay thế những giá trị đã được thiết lập bởi các mục dict và phép giải nén dictionary xuất hiện trước đó.

.. versionadded:: 3.5
   Phép giải nén vào các biểu diễn dictionary, ban đầu được đề xuất bởi :pep:`448`.

Khác với list comprehension và set comprehension, dict comprehension cần hai biểu thức được phân tách bằng dấu hai chấm, theo sau là các mệnh đề "for" và "if" thông thường. Khi comprehension được thực thi, các phần tử khóa và giá trị tạo ra sẽ được chèn vào dictionary mới theo thứ tự chúng được tạo ra.

.. index:: pair: immutable; object
           hashable

Các hạn chế về kiểu của các giá trị khóa được liệt kê trước đó trong phần
:ref:`types`. (Tóm lại, kiểu khóa phải là :term:`hashable`, tức là loại trừ mọi đối tượng có thể thay đổi.) Các xung đột giữa những khóa trùng lặp không được phát hiện; giá trị cuối cùng (ở vị trí ngoài cùng bên phải trong biểu diễn) được lưu cho một giá trị khóa nhất định sẽ được ưu tiên.

.. versionchanged:: 3.8
   Trước Python 3.8, trong dict comprehension, thứ tự đánh giá khóa và giá trị chưa được xác định rõ ràng. Trong CPython, giá trị được đánh giá trước khóa. Kể từ 3.8, khóa được đánh giá trước giá trị, theo đề xuất của :pep:`572`.


.. _genexpr:

Biểu thức generator
-------------------

.. index::
   pair: generator; expression
   pair: object; generator
   single: () (parentheses); generator expression

Cú pháp của :dfn:`biểu thức generator (generator expression)` giống với cú pháp của :ref:`list comprehension <comprehensions>`, ngoại trừ việc chúng được đặt trong ngoặc đơn thay vì ngoặc vuông. Ví dụ::

   >>> iterator = (x ** 2 for x in range(10))
   >>> iterator
   <generator object <genexpr> at ...>

Trong runtime, một biểu thức generator sẽ đánh giá thành một :term:`generator iterator` cho ra các giá trị giống với list comprehension tương ứng::

   >>> list(iterator)
   [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

Do đó, ví dụ trên gần tương đương với việc định nghĩa và gọi hàm generator sau đây::

   def make_generator_of_squares(iterator):
       for x in iterator:
           yield x ** 2

   make_generator_of_squares(iter(range(10)))

Có thể bỏ qua cặp ngoặc đơn bao quanh trong các lệnh gọi khi biểu thức generator là đối số positional duy nhất và không có keyword arguments. Xem :ref:`mục Calls <calls>` để biết chi tiết. Ví dụ::

   # Các dấu ngoặc đơn sau `sum` là một phần của cú pháp gọi:
   >>> sum(x ** 2 for x in range(10))
   285

   # Biểu thức generator cần có cặp ngoặc đơn riêng nếu nó không phải là đối số duy nhất:
   >>> sum((x ** 2 for x in range(10)), start=1000)
   1285

Biểu thức iterable trong mệnh đề :keyword:`!for` ngoài cùng bên trái được đánh giá ngay lập tức, vì vậy lỗi do biểu thức này gây ra sẽ được phát ra tại thời điểm định nghĩa biểu thức generator, thay vì tại thời điểm truy xuất giá trị đầu tiên::

   >>> (x ** 2 for x in nonexistent_iterable)
   Traceback (most recent call last):
     ...
   NameError: name 'nonexistent_iterable' is not defined

Sau khi biểu thức được đánh giá, một iterator được tạo từ kết quả, như thể :py:func:`iter` được gọi trên kết quả đó. Mọi lỗi phát sinh khi tạo iterator cũng được phát ra ngay lập tức::

   >>> (x ** 2 for x in None)
   Traceback (most recent call last):
     ...
   TypeError: 'NoneType' object is not iterable

Tất cả các biểu thức khác đều được đánh giá một cách lazy, theo cùng cách với generator thông thường (tức là khi iterator được yêu cầu trả về một giá trị)::

   >>> iterator = (nonexistent_value for x in range(10))
   >>> iterator
   <generator object <genexpr> at ...>
   >>> list(iterator)
   Traceback (most recent call last):
     ...
   NameError: name 'nonexistent_value' is not defined

::

   >>> iterator = (x * y for x in range(10) for y in nonexistent_iterable)
   >>> iterator
   <generator object <genexpr> at ...>
   >>> list(iterator)
   Traceback (most recent call last):
     ...
   NameError: name 'nonexistent_iterable' is not defined

Để không ảnh hưởng đến hoạt động dự kiến của chính generator expression, các biểu thức ``yield`` và ``yield from`` bị cấm trong scope lồng nhau ngầm định.

Nếu một generator expression chứa các mệnh đề :keyword:`!async for` hoặc biểu thức :keyword:`await`, nó được gọi là một
:dfn:`asynchronous generator expression`. Một asynchronous generator expression trả về một đối tượng asynchronous generator mới, đây là một asynchronous iterator (xem :ref:`async-iterators`).

Cú pháp chính thức của generator expression là:

.. grammar-snippet::
   :group: python-grammar

   generator_expression: "(" `expression` `comp_for` ")"

.. versionadded:: 3.6
   Asynchronous generator expression đã được giới thiệu.

.. versionchanged:: 3.7
   Trước Python 3.7, các biểu thức trình tạo bất đồng bộ chỉ có thể xuất hiện trong các coroutine :keyword:`async def`. Kể từ 3.7, mọi hàm đều có thể sử dụng các biểu thức trình tạo bất đồng bộ.

.. versionchanged:: 3.8
   ``yield`` và ``yield from`` bị cấm trong phạm vi lồng ghép ngầm định.


.. _yieldexpr:

Biểu thức yield
---------------

.. index::
   pair: keyword; yield
   pair: keyword; from
   pair: yield; expression
   pair: generator; function

.. productionlist:: python-grammar
   yield_atom: "(" `yield_expression` ")"
   yield_from: "yield" "from" `expression`
   yield_expression: "yield" `yield_list` | `yield_from`

Biểu thức yield được sử dụng khi định nghĩa một hàm :term:`generator` hoặc một hàm :term:`asynchronous generator`, vì vậy chỉ có thể được sử dụng trong phần thân của một định nghĩa hàm. Việc sử dụng biểu thức yield trong phần thân của một hàm khiến hàm đó trở thành hàm trình tạo, còn việc sử dụng nó trong phần thân của một hàm :keyword:`async def` khiến hàm coroutine đó trở thành một hàm trình tạo bất đồng bộ. Ví dụ::

    def gen():  # định nghĩa một hàm trình tạo
        yield 123

    async def agen(): # định nghĩa một hàm trình tạo bất đồng bộ
        yield 123

Do có tác động phụ lên phạm vi chứa, các biểu thức ``yield`` không được phép xuất hiện trong các phạm vi được định nghĩa ngầm để triển khai các comprehension và biểu thức trình tạo.

.. versionchanged:: 3.8
   Các biểu thức yield bị cấm trong các phạm vi lồng nhau ngầm được dùng để triển khai comprehension và biểu thức generator.

Các hàm generator được mô tả bên dưới, còn các hàm generator bất đồng bộ được mô tả riêng trong phần
:ref:`asynchronous-generator-functions`.

Khi một hàm generator được gọi, nó trả về một iterator được gọi là generator. Generator đó sau đó điều khiển việc thực thi hàm generator. Việc thực thi bắt đầu khi một trong các phương thức của generator được gọi. Khi đó, việc thực thi tiếp tục đến biểu thức yield đầu tiên, tại đó lại bị tạm dừng và trả về giá trị của :token:`~python-grammar:yield_list` cho bên gọi generator, hoặc ``None`` nếu :token:`~python-grammar:yield_list` bị bỏ qua. “Bị tạm dừng” nghĩa là toàn bộ trạng thái cục bộ được giữ lại, bao gồm các binding hiện tại của biến cục bộ, con trỏ lệnh, ngăn xếp đánh giá nội bộ và trạng thái của mọi cơ chế xử lý ngoại lệ. Khi việc thực thi được tiếp tục bằng cách gọi một trong các phương thức của generator, hàm có thể tiếp tục chính xác như thể biểu thức yield chỉ là một lời gọi bên ngoài khác. Giá trị của biểu thức yield sau khi tiếp tục phụ thuộc vào phương thức đã tiếp tục việc thực thi. Nếu :meth:`~generator.__next__` được sử dụng (thường thông qua :keyword:`for` hoặc builtin :func:`next`) thì kết quả là :const:`None`. Ngược lại, nếu :meth:`~generator.send` được sử dụng thì kết quả sẽ là giá trị được truyền vào phương thức đó.

.. index:: single: coroutine

Tất cả những điều này khiến các hàm generator khá giống với coroutine; chúng yield nhiều lần, có nhiều hơn một điểm vào và việc thực thi có thể bị tạm dừng. Điểm khác biệt duy nhất là hàm generator không thể kiểm soát việc thực thi sẽ tiếp tục ở đâu sau khi yield; quyền điều khiển luôn được chuyển cho bên gọi generator.

Các biểu thức yield được phép xuất hiện ở bất kỳ đâu trong cấu trúc :keyword:`try`. Nếu generator không được tiếp tục trước khi hoàn tất (do đạt đến số lượng tham chiếu bằng không hoặc do được garbage collector thu gom), phương thức :meth:`~generator.close` của generator-iterator sẽ được gọi, cho phép mọi mệnh đề :keyword:`finally` đang chờ được thực thi.

.. index::
   single: from; yield from expression

Khi ``yield from <expr>`` được sử dụng, biểu thức được cung cấp phải là một iterable. Các giá trị được tạo ra khi lặp qua iterable đó được truyền trực tiếp cho bên gọi các phương thức của generator hiện tại. Mọi giá trị được truyền vào cùng với
:meth:`~generator.send` và mọi ngoại lệ được truyền vào cùng với
:meth:`~generator.throw` được truyền đến iterator cơ sở nếu iterator đó có các phương thức tương ứng. Nếu không, :meth:`~generator.send` sẽ phát sinh :exc:`AttributeError` hoặc :exc:`TypeError`, trong khi
:meth:`~generator.throw` chỉ phát sinh ngoại lệ được truyền vào ngay lập tức.

Khi iterator cơ sở hoàn tất, thuộc tính :attr:`~StopIteration.value` của thực thể :exc:`StopIteration` được phát sinh sẽ trở thành giá trị của biểu thức yield. Giá trị này có thể được đặt rõ ràng khi phát sinh
:exc:`StopIteration`, hoặc được đặt tự động khi subiterator là một generator (bằng cách trả về một giá trị từ subgenerator).

.. versionchanged:: 3.3
   Đã thêm ``yield from <expr>`` để ủy quyền luồng điều khiển cho một subiterator.

Có thể bỏ qua dấu ngoặc đơn khi biểu thức yield là biểu thức duy nhất ở vế phải của một câu lệnh gán.

.. seealso::

   :pep:`255` - Generator đơn giản
      Đề xuất bổ sung generator và câu lệnh :keyword:`yield` cho Python.

   :pep:`342` - Coroutine thông qua generator nâng cao
      Đề xuất nâng cao API và cú pháp của generator, giúp chúng có thể được sử dụng như các coroutine đơn giản.

   :pep:`380` - Cú pháp ủy quyền cho subgenerator
      Đề xuất giới thiệu cú pháp :token:`~python-grammar:yield_from`, giúp việc ủy quyền cho subgenerator trở nên dễ dàng.

   :pep:`525` - Generator bất đồng bộ
      Đề xuất mở rộng :pep:`492` bằng cách bổ sung khả năng generator cho các hàm coroutine.

.. index:: pair: object; generator
.. _generator-methods:

Các phương thức của generator-iterator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Phần này mô tả các phương thức của một generator iterator. Có thể sử dụng chúng để điều khiển việc thực thi một hàm generator.

Lưu ý rằng việc gọi bất kỳ phương thức generator nào dưới đây khi generator đang thực thi sẽ phát sinh một ngoại lệ :exc:`ValueError`.

.. index:: pair: exception; StopIteration


.. method:: generator.__next__()

   Bắt đầu thực thi một hàm generator hoặc tiếp tục thực thi tại biểu thức yield được thực thi gần nhất. Khi một hàm generator được tiếp tục bằng phương thức
   :meth:`~generator.__next__`, biểu thức yield hiện tại luôn được đánh giá thành :const:`None`. Sau đó, quá trình thực thi tiếp tục đến biểu thức yield tiếp theo, tại đó generator lại bị tạm dừng, và giá trị của
   :token:`~python-grammar:yield_list` được trả về cho bên gọi của :meth:`__next__`. Nếu generator kết thúc mà không yield thêm giá trị nào, một ngoại lệ
   :exc:`StopIteration` sẽ được phát sinh.

   Phương thức này thường được gọi một cách ngầm định, chẳng hạn bởi vòng lặp :keyword:`for`, hoặc bởi hàm dựng sẵn :func:`next`.


.. method:: generator.send(value)

   Tiếp tục quá trình thực thi và "gửi" một giá trị vào hàm generator. Đối số *value* trở thành kết quả của biểu thức yield hiện tại. Phương thức
   :meth:`send` trả về giá trị tiếp theo được generator yield, hoặc phát sinh :exc:`StopIteration` nếu generator kết thúc mà không yield thêm giá trị nào. Khi :meth:`send` được gọi để khởi động generator, nó phải được gọi với :const:`None` làm đối số, vì không có biểu thức yield nào có thể nhận giá trị này.


.. method:: generator.throw(value)
            generator.throw(type[, value[, traceback]])

   Phát sinh một ngoại lệ tại điểm generator bị tạm dừng và trả về giá trị tiếp theo được hàm generator yield. Nếu generator kết thúc mà không yield thêm giá trị nào, một ngoại lệ :exc:`StopIteration` sẽ được phát sinh. Nếu hàm generator không bắt ngoại lệ được truyền vào hoặc phát sinh một ngoại lệ khác, ngoại lệ đó sẽ lan truyền đến bên gọi.

   Trong cách sử dụng thông thường, phương thức này được gọi với một instance ngoại lệ duy nhất, tương tự cách sử dụng từ khóa :keyword:`raise`.

   Tuy nhiên, để tương thích ngược, chữ ký thứ hai vẫn được hỗ trợ, theo một quy ước từ các phiên bản Python cũ hơn. Đối số *type* phải là một class ngoại lệ, còn *value* phải là một instance ngoại lệ. Nếu không cung cấp *value*, hàm dựng *type* sẽ được gọi để lấy một instance. Nếu cung cấp *traceback*, nó sẽ được gán cho ngoại lệ; nếu không, mọi
   Thuộc tính :attr:`~BaseException.__traceback__` được lưu trong *value* có thể bị xóa.

   .. versionchanged:: 3.12

      Chữ ký thứ hai \(type\[, value\[, traceback\]\]\) không được dùng nữa và có thể bị loại bỏ trong phiên bản Python tương lai.

.. index:: pair: exception; GeneratorExit


.. method:: generator.close()

   Tạo ra một ngoại lệ :exc:`GeneratorExit` tại vị trí mà hàm generator bị tạm dừng (tương đương với việc gọi ``throw(GeneratorExit)``). Ngoại lệ được tạo ra bởi biểu thức yield tại nơi generator bị tạm dừng. Nếu hàm generator bắt ngoại lệ và trả về một giá trị, giá trị này được trả về từ :meth:`close`. Nếu hàm generator đã đóng hoặc tạo ra :exc:`GeneratorExit` (do không bắt ngoại lệ), :meth:`close` trả về :const:`None`. Nếu generator tạo ra một giá trị, một :exc:`RuntimeError` sẽ được tạo ra. Nếu generator tạo ra bất kỳ ngoại lệ nào khác, ngoại lệ đó được truyền đến caller. Nếu generator đã thoát do một ngoại lệ hoặc thoát bình thường, :meth:`close` trả về
   :const:`None` và không có tác dụng nào khác.

   .. versionchanged:: 3.13

      Nếu generator trả về một giá trị khi bị đóng, giá trị đó được :meth:`close` trả về.

.. index:: single: yield; examples

Ví dụ
^^^^^

Sau đây là một ví dụ đơn giản minh họa hoạt động của các generator và hàm generator::

   >>> def echo(value=None):
   ...     print("Execution starts when 'next()' is called for the first time.")
   ...     try:
   ...         while True:
   ...             try:
   ...                 value = (yield value)
   ...             except Exception as e:
   ...                 value = e
   ...     finally:
   ...         print("Don't forget to clean up when 'close()' is called.")
   ...
   >>> generator = echo(1)
   >>> print(next(generator))
   Execution starts when 'next()' is called for the first time.
   1
   >>> print(next(generator))
   None
   >>> print(generator.send(2))
   2
   >>> generator.throw(TypeError, "spam")
   TypeError('spam',)
   >>> generator.close()
   Don't forget to clean up when 'close()' is called.

Để xem các ví dụ sử dụng ``yield from``, hãy xem :ref:`pep-380` trong "What's New in Python."

.. _asynchronous-generator-functions:

Các hàm asynchronous generator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sự xuất hiện của biểu thức yield trong một hàm hoặc phương thức được định nghĩa bằng
:keyword:`async def` tiếp tục xác định hàm đó là một
:term:`asynchronous generator` hàm.

Khi một hàm asynchronous generator được gọi, nó trả về một iterator bất đồng bộ được gọi là đối tượng asynchronous generator. Sau đó, đối tượng này điều khiển việc thực thi hàm generator. Một đối tượng asynchronous generator thường được sử dụng trong một
câu lệnh :keyword:`async for` trong một hàm coroutine, tương tự như cách một đối tượng generator được sử dụng trong câu lệnh :keyword:`for`.

Việc gọi một trong các phương thức của asynchronous generator sẽ trả về một đối tượng :term:`awaitable`, và quá trình thực thi bắt đầu khi đối tượng này được await. Khi đó, quá trình thực thi tiếp tục đến biểu thức yield đầu tiên, tại đó lại bị tạm dừng và trả về giá trị của :token:`~python-grammar:yield_list` cho coroutine đang await. Tương tự generator, việc tạm dừng có nghĩa là toàn bộ trạng thái cục bộ được giữ lại, bao gồm các binding hiện tại của biến cục bộ, con trỏ lệnh, ngăn xếp đánh giá nội bộ và trạng thái của mọi cơ chế xử lý ngoại lệ. Khi quá trình thực thi được tiếp tục bằng cách await đối tượng tiếp theo do các phương thức của asynchronous generator trả về, hàm có thể tiếp tục chính xác như thể biểu thức yield chỉ là một lời gọi bên ngoài khác. Giá trị của biểu thức yield sau khi tiếp tục phụ thuộc vào phương thức đã tiếp tục quá trình thực thi. Nếu
sử dụng :meth:`~agen.__anext__` thì kết quả là :const:`None`. Ngược lại, nếu
sử dụng :meth:`~agen.asend`, thì kết quả sẽ là giá trị được truyền vào phương thức đó.

Nếu một asynchronous generator thoát sớm do :keyword:`break`, task của caller bị hủy hoặc do các ngoại lệ khác, mã dọn dẹp bất đồng bộ của generator sẽ chạy và có thể phát sinh ngoại lệ hoặc truy cập các biến context trong một context không mong muốn--chẳng hạn sau khi các task mà nó phụ thuộc vào đã hết vòng đời hoặc trong khi event loop đang tắt, khi hook thu gom rác của async generator được gọi. Để ngăn điều này, caller phải đóng rõ ràng asynchronous generator bằng cách gọi
phương thức :meth:`~agen.aclose` để hoàn tất generator và cuối cùng tách nó khỏi event loop.

Trong một hàm asynchronous generator, các biểu thức yield được phép xuất hiện ở bất kỳ đâu trong một cấu trúc :keyword:`try`. Tuy nhiên, nếu một asynchronous generator không được tiếp tục trước khi hoàn tất (do số lượng tham chiếu giảm về 0 hoặc do bị thu gom rác), thì một biểu thức yield bên trong cấu trúc :keyword:`!try` có thể khiến các mệnh đề :keyword:`finally` đang chờ không được thực thi. Trong trường hợp này, event loop hoặc scheduler đang chạy asynchronous generator có trách nhiệm gọi phương thức :meth:`~agen.aclose` của asynchronous generator-iterator và chạy đối tượng coroutine được tạo ra, nhờ đó cho phép mọi mệnh đề :keyword:`!finally` đang chờ được thực thi.

Để xử lý việc hoàn tất khi event loop kết thúc, một event loop nên định nghĩa một hàm *finalizer*, hàm này nhận một asynchronous generator-iterator và được cho là sẽ gọi :meth:`~agen.aclose` rồi thực thi coroutine. *finalizer* này có thể được đăng ký bằng cách gọi :func:`sys.set_asyncgen_hooks`. Khi được lặp qua lần đầu, một asynchronous generator-iterator sẽ lưu *finalizer* đã đăng ký để gọi khi hoàn tất. Để xem ví dụ tham khảo về phương thức *finalizer*, hãy xem phần triển khai của ``asyncio.Loop.shutdown_asyncgens`` trong :source:`Lib/asyncio/base_events.py`.

Biểu thức ``yield from <expr>`` là một lỗi cú pháp khi được sử dụng trong một hàm generator không đồng bộ.

.. index:: pair: object; asynchronous-generator
.. _asynchronous-generator-methods:

Các phương thức iterator-generator không đồng bộ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Phần phụ này mô tả các phương thức của một iterator generator không đồng bộ, được sử dụng để điều khiển việc thực thi một hàm generator.


.. index:: pair: exception; StopAsyncIteration

.. method:: agen.__anext__()
   :async:

   Trả về một awaitable mà khi được chạy sẽ bắt đầu thực thi generator không đồng bộ hoặc tiếp tục thực thi tại biểu thức yield được thực thi gần nhất. Khi một hàm generator không đồng bộ được tiếp tục bằng phương thức :meth:`~agen.__anext__`, biểu thức yield hiện tại luôn đánh giá thành :const:`None` trong awaitable được trả về; khi được chạy, awaitable này sẽ tiếp tục đến biểu thức yield tiếp theo. Giá trị của :token:`~python-grammar:yield_list` trong biểu thức yield là giá trị của ngoại lệ :exc:`StopIteration` do coroutine hoàn tất đưa ra. Nếu generator không đồng bộ kết thúc mà không yield thêm giá trị nào, awaitable thay vào đó sẽ đưa ra một
   ngoại lệ :exc:`StopAsyncIteration`, báo hiệu rằng quá trình lặp không đồng bộ đã hoàn tất.

   Phương thức này thường được gọi ngầm bởi một vòng lặp :keyword:`async for`.


.. method:: agen.asend(value)
   :async:

   Trả về một awaitable mà khi được chạy sẽ tiếp tục thực thi generator không đồng bộ. Tương tự phương thức :meth:`~generator.send` đối với generator, phương thức này “gửi” một giá trị vào hàm generator không đồng bộ, và đối số *value* trở thành kết quả của biểu thức yield hiện tại. Awaitable được phương thức :meth:`asend` trả về sẽ trả về giá trị tiếp theo được generator yield, làm giá trị của ngoại lệ được đưa ra
   :exc:`StopIteration`, hoặc phát sinh :exc:`StopAsyncIteration` nếu trình sinh bất đồng bộ kết thúc mà không tạo ra giá trị nào khác. Khi
   :meth:`asend` được gọi để bắt đầu trình sinh bất đồng bộ, nó phải được gọi với :const:`None` làm đối số, vì không có biểu thức yield nào có thể nhận giá trị này.


.. method:: agen.athrow(value)
            agen.athrow(type[, value[, traceback]])
   :async:

   Trả về một awaitable; khi được thực thi, awaitable này sẽ phát sinh một ngoại lệ có kiểu ``type`` tại điểm trình sinh bất đồng bộ bị tạm dừng, đồng thời trả về giá trị tiếp theo do hàm trình sinh tạo ra làm giá trị của ngoại lệ
   :exc:`StopIteration`. Nếu trình sinh bất đồng bộ kết thúc mà không tạo ra giá trị nào khác, awaitable sẽ phát sinh ngoại lệ :exc:`StopAsyncIteration`. Nếu hàm trình sinh không bắt ngoại lệ được truyền vào hoặc phát sinh một ngoại lệ khác, thì khi awaitable được thực thi, ngoại lệ đó sẽ lan truyền đến bên gọi awaitable.

   .. versionchanged:: 3.12

      Cú pháp thứ hai \(type\[, value\[, traceback\]\]\) không được khuyến nghị sử dụng và có thể bị loại bỏ trong một phiên bản Python trong tương lai.

.. index:: pair: exception; GeneratorExit


.. method:: agen.aclose()
   :async:

   Trả về một awaitable; khi được thực thi, awaitable này sẽ ném một :exc:`GeneratorExit` vào hàm trình sinh bất đồng bộ tại điểm hàm bị tạm dừng. Nếu sau đó hàm trình sinh bất đồng bộ kết thúc bình thường, đã được đóng hoặc phát sinh :exc:`GeneratorExit` (do không bắt ngoại lệ), thì awaitable được trả về sẽ phát sinh ngoại lệ :exc:`StopIteration`. Mọi awaitable tiếp theo được trả về bởi các lần gọi sau đến trình sinh bất đồng bộ sẽ phát sinh ngoại lệ :exc:`StopAsyncIteration`. Nếu trình sinh bất đồng bộ tạo ra một giá trị, awaitable sẽ phát sinh :exc:`RuntimeError`. Nếu trình sinh bất đồng bộ phát sinh bất kỳ ngoại lệ nào khác, ngoại lệ đó sẽ lan truyền đến bên gọi awaitable. Nếu trình sinh bất đồng bộ đã kết thúc do một ngoại lệ hoặc kết thúc bình thường, thì các lần gọi tiếp theo đến :meth:`aclose` sẽ trả về một awaitable không thực hiện thao tác nào.

.. _primaries:

Biểu thức chính
===============

.. index:: single: primary

Biểu thức chính đại diện cho các phép toán liên kết chặt chẽ nhất trong ngôn ngữ. Cú pháp của chúng là:

.. productionlist:: python-grammar
   primary: `atom` | `attributeref` | `subscription` | `call`


.. _attribute-references:

Tham chiếu thuộc tính
---------------------

.. index::
   pair: attribute; reference
   single: . (dot); attribute reference

Một tham chiếu thuộc tính là một biểu thức chính theo sau bởi dấu chấm và một tên:

.. productionlist:: python-grammar
   attributeref: `primary` "." `identifier`

.. index::
   pair: exception; AttributeError
   pair: object; module
   pair: object; list

Biểu thức chính phải được đánh giá thành một đối tượng thuộc kiểu hỗ trợ tham chiếu thuộc tính, mà hầu hết các đối tượng đều hỗ trợ. Sau đó, đối tượng này được yêu cầu cung cấp thuộc tính có tên là mã định danh. Kiểu và giá trị được tạo ra do đối tượng quyết định. Việc đánh giá nhiều lần cùng một tham chiếu thuộc tính có thể cho ra các đối tượng khác nhau.

Việc tạo này có thể được tùy chỉnh bằng cách ghi đè phương thức
:meth:`~object.__getattribute__` hoặc phương thức :meth:`~object.__getattr__`. Phương thức :meth:`!__getattribute__` được gọi trước tiên và trả về một giá trị hoặc phát sinh :exc:`AttributeError` nếu thuộc tính không khả dụng.

Nếu một :exc:`AttributeError` được raise và đối tượng có phương thức :meth:`!__getattr__`, phương thức đó sẽ được gọi như một phương án dự phòng.

.. _subscriptions:

Phép truy cập phần tử và phép cắt
---------------------------------

.. index::
   single: subscription
   single: [] (square brackets); subscription

.. index::
   pair: object; sequence
   pair: object; mapping
   pair: object; string
   pair: object; tuple
   pair: object; list
   pair: object; dictionary
   pair: sequence; item

Cú pháp :dfn:`subscription` thường được dùng để chọn một phần tử từ một
:ref:`container <sequence-types>` -- ví dụ, để lấy một giá trị từ một :class:`dict`::

   >>> digits_by_name = {'one': 1, 'two': 2}
   >>> digits_by_name['two']  # Truy cập dictionary bằng khóa 'two'
   2

Trong cú pháp subscription, đối tượng được truy cập -- một
:ref:`primary <primaries>` -- được theo sau bởi một :dfn:`subscript` trong cặp dấu ngoặc vuông. Trong trường hợp đơn giản nhất, subscript là một biểu thức duy nhất.

Tùy thuộc vào loại đối tượng được áp dụng phép subscription, chỉ mục đôi khi được gọi là :term:`key` (đối với mapping), :term:`index` (đối với sequence) hoặc *type argument* (đối với :term:`generic types <generic type>`). Về mặt cú pháp, tất cả đều tương đương::

   >>> colors = ['red', 'blue', 'green', 'black']
   >>> colors[3]  # Truy cập list bằng chỉ mục 3
   'black'

   >>> list[str]  # Tham số hóa kiểu list bằng đối số kiểu str
   list[str]

Trong runtime, interpreter sẽ đánh giá primary và subscript, rồi gọi :meth:`~object.__getitem__` của primary hoặc
:meth:`~object.__class_getitem__` :term:`special method` với subscript làm đối số. Để biết thêm chi tiết về phương thức nào được gọi, hãy xem
:ref:`classgetitem-versus-getitem`.

Để minh họa cách subscription hoạt động, chúng ta có thể định nghĩa một đối tượng tùy chỉnh triển khai :meth:`~object.__getitem__` và in ra giá trị của subscript::

   >>> class SubscriptionDemo:
   ...     def __getitem__(self, key):
   ...         print(f'subscripted with: {key!r}')
   ...
   >>> demo = SubscriptionDemo()
   >>> demo[1]
   subscripted with: 1
   >>> demo['a' * 3]
   subscripted with: 'aaa'

Xem tài liệu :meth:`~object.__getitem__` để biết cách các kiểu dựng sẵn xử lý subscription.

Subscriptions cũng có thể được dùng làm đích trong các câu lệnh :ref:`gán <assignment>` hoặc
các câu lệnh :ref:`xóa <del>`. Trong những trường hợp này, trình thông dịch sẽ gọi đối tượng được lập chỉ mục của nó
:meth:`~object.__setitem__` hoặc :meth:`~object.__delitem__`
:term:`special method`, tương ứng, thay vì :meth:`~object.__getitem__`.

.. code-block::

   >>> colors = ['red', 'blue', 'green', 'black']
   >>> colors[3] = 'white'  # Đặt mục tại chỉ mục
   >>> colors
   ['red', 'blue', 'green', 'white']
   >>> del colors[3]  # Xóa mục tại chỉ mục 3
   >>> colors
   ['red', 'blue', 'green']

Tất cả các dạng nâng cao của *truy cập bằng chỉ số* được mô tả trong các phần sau cũng có thể được sử dụng cho phép gán và xóa.


.. index::
   single: slicing
   single: slice
   single: : (colon); slicing
   single: , (comma); slicing

.. index::
   pair: object; sequence
   pair: object; string
   pair: object; tuple
   pair: object; list

.. _slicings:

Phép cắt
^^^^^^^^

Một dạng nâng cao hơn của phép subscription, :dfn:`slicing`, thường được dùng để trích xuất một phần của :ref:`sequence <datamodel-sequences>`. Ở dạng này, subscript là một :term:`slice`: tối đa ba biểu thức được phân tách bằng dấu hai chấm. Bất kỳ biểu thức nào cũng có thể được bỏ qua, nhưng một phép cắt phải chứa ít nhất một dấu hai chấm::

   >>> number_names = ['zero', 'one', 'two', 'three', 'four', 'five']
   >>> number_names[1:3]
   ['one', 'two']
   >>> number_names[1:]
   ['one', 'two', 'three', 'four', 'five']
   >>> number_names[:3]
   ['zero', 'one', 'two']
   >>> number_names[:]
   ['zero', 'one', 'two', 'three', 'four', 'five']
   >>> number_names[::2]
   ['zero', 'two', 'four']
   >>> number_names[:-3]
   ['zero', 'one', 'two']
   >>> del number_names[4:]
   >>> number_names
   ['zero', 'one', 'two', 'three']

Khi một phép cắt được đánh giá, interpreter tạo một đối tượng :class:`slice` có :attr:`~slice.start`, :attr:`~slice.stop` và
:attr:`~slice.step` các thuộc tính, lần lượt là kết quả của các biểu thức nằm giữa các dấu hai chấm. Mọi biểu thức bị thiếu đều được đánh giá thành :const:`None`. Đối tượng :class:`!slice` này sau đó được truyền cho :meth:`~object.__getitem__` hoặc :meth:`~object.__class_getitem__` :term:`special method`, như trên.::

   # tiếp tục với instance SubscriptionDemo được định nghĩa ở trên:
   >>> demo[2:3]
   subscripted with: slice(2, 3, None)
   >>> demo[::'spam']
   subscripted with: slice(None, None, 'spam')


Các subscript được phân tách bằng dấu phẩy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Subscript cũng có thể được cung cấp dưới dạng từ hai biểu thức hoặc phép cắt trở lên, được phân tách bằng dấu phẩy::

   # tiếp tục với thể hiện SubscriptionDemo được định nghĩa ở trên:
   >>> demo[1, 2, 3]
   subscripted with: (1, 2, 3)
   >>> demo[1:2, 3]
   subscripted with: (slice(1, 2, None), 3)

Dạng này thường được dùng với các thư viện số để cắt dữ liệu đa chiều. Trong trường hợp này, trình thông dịch tạo một :class:`tuple` từ kết quả của các biểu thức hoặc lát cắt, rồi truyền tuple này cho :meth:`~object.__getitem__` hoặc :meth:`~object.__class_getitem__` :term:`special method`, như trên.

Phần chỉ số cũng có thể được cung cấp dưới dạng một biểu thức hoặc lát cắt duy nhất theo sau là dấu phẩy, để chỉ định một tuple gồm một phần tử::

   >>> demo['spam',]
   subscripted with: ('spam',)


Subscription có dấu sao
^^^^^^^^^^^^^^^^^^^^^^^

.. versionadded:: 3.11
   Các biểu thức trong *tuple_slices* có thể có dấu sao. Xem :pep:`646`.

Phần chỉ số cũng có thể chứa một biểu thức có dấu sao. Trong trường hợp này, trình thông dịch giải nén kết quả thành một tuple rồi truyền tuple này cho :meth:`~object.__getitem__` hoặc :meth:`~object.__class_getitem__`::

   # tiếp tục với thể hiện SubscriptionDemo được định nghĩa ở trên:
   >>> demo[*range(10)]
   subscripted with: (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

Các biểu thức có dấu sao có thể được kết hợp với các biểu thức được phân tách bằng dấu phẩy và các lát cắt::

   >>> demo['a', 'b', *range(3), 'c']
   subscripted with: ('a', 'b', 0, 1, 2, 'c')


Ngữ pháp đăng ký hình thức
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. grammar-snippet::
   :group: python-grammar

   subscription:     `primary` '[' `subscript` ']'
   subscript:        `single_subscript` | `tuple_subscript`
   single_subscript: `proper_slice` | `assignment_expression`
   proper_slice:     [`expression`] ":" [`expression`] [ ":" [`expression`] ]
   tuple_subscript:  ','.(`single_subscript` | `starred_expression`)+ [',']

Hãy nhớ rằng toán tử ``|`` :ref:`biểu thị lựa chọn có thứ tự <notation>`. Cụ thể, trong :token:`!subscript`, nếu cả hai phương án đều khớp, phương án đầu tiên (:token:`!single_subscript`) được ưu tiên.

.. index::
   pair: object; callable
   single: call
   single: argument; call semantics
   single: () (parentheses); call
   single: , (comma); argument list
   single: = (equals); in function calls

.. _calls:

Lời gọi
-------

Một lời gọi gọi một đối tượng có thể gọi (ví dụ: một :term:`function`) với một chuỗi :term:`đối số <argument>` có thể rỗng:

.. productionlist:: python-grammar
   call: `primary` "(" [`argument_list` [","] | `comprehension`] ")"
   argument_list: `positional_arguments` ["," `starred_and_keywords`]
                :   ["," `keywords_arguments`]
                : | `starred_and_keywords` ["," `keywords_arguments`]
                : | `keywords_arguments`
   positional_arguments: `positional_item` ("," `positional_item`)*
   positional_item: `assignment_expression` | "*" `expression`
   starred_and_keywords: ("*" `expression` | `keyword_item`)
                : ("," "*" `expression` | "," `keyword_item`)*
   keywords_arguments: (`keyword_item` | "**" `expression`)
                : ("," `keyword_item` | "," "**" `expression`)*
   keyword_item: `identifier` "=" `expression`

Có thể có một dấu phẩy tùy chọn ở cuối sau các đối số vị trí và đối số từ khóa, nhưng điều này không ảnh hưởng đến ngữ nghĩa.

.. index::
   single: parameter; call semantics

Biểu thức chính phải được đánh giá thành một đối tượng có thể gọi (các hàm do người dùng định nghĩa, hàm dựng sẵn, phương thức của các đối tượng dựng sẵn, đối tượng lớp, phương thức của các thể hiện lớp và mọi đối tượng có phương thức :meth:`~object.__call__` đều có thể gọi được). Tất cả các biểu thức đối số được đánh giá trước khi thực hiện lời gọi. Vui lòng tham khảo mục :ref:`function` để biết cú pháp của các danh sách :term:`parameter` hình thức.

.. XXX update with kwonly args PEP

Nếu có các đối số từ khóa, trước tiên chúng được chuyển đổi thành các đối số vị trí như sau. Trước hết, một danh sách các vị trí chưa được điền được tạo cho các tham số hình thức. Nếu có N đối số vị trí, chúng được đặt vào N vị trí đầu tiên. Tiếp theo, với mỗi đối số từ khóa, mã định danh được dùng để xác định vị trí tương ứng (nếu mã định danh giống với tên tham số hình thức đầu tiên thì sử dụng vị trí đầu tiên, và tiếp tục như vậy). Nếu vị trí đó đã được điền, một ngoại lệ :exc:`TypeError` sẽ được phát sinh. Nếu không, đối số được đặt vào vị trí đó và điền vào vị trí (ngay cả khi biểu thức là ``None``, nó vẫn điền vào vị trí). Khi tất cả các đối số đã được xử lý, những vị trí vẫn chưa được điền sẽ được điền bằng giá trị mặc định tương ứng từ định nghĩa hàm. (Các giá trị mặc định được tính một lần, khi hàm được định nghĩa; vì vậy, một đối tượng có thể thay đổi như danh sách hoặc từ điển được dùng làm giá trị mặc định sẽ được dùng chung bởi mọi lần gọi không chỉ định giá trị đối số cho vị trí tương ứng; thông thường nên tránh điều này.) Nếu còn bất kỳ vị trí chưa được điền nào mà không có giá trị mặc định, một ngoại lệ :exc:`TypeError` sẽ được phát sinh. Nếu không, danh sách các vị trí đã được điền sẽ được dùng làm danh sách đối số cho lần gọi.

.. impl-detail::

   Một implementation có thể cung cấp các hàm tích hợp sẵn mà các tham số vị trí không có tên, ngay cả khi chúng được “đặt tên” nhằm phục vụ mục đích tài liệu, và do đó không thể được cung cấp bằng từ khóa. Trong CPython, điều này xảy ra với các hàm được triển khai bằng C sử dụng :c:func:`PyArg_ParseTuple` để phân tích cú pháp các đối số.

Nếu có nhiều đối số vị trí hơn số vị trí tham số hình thức, một
ngoại lệ :exc:`TypeError` sẽ được phát sinh, trừ khi có một tham số hình thức sử dụng cú pháp ``*identifier``; trong trường hợp này, tham số hình thức đó nhận một tuple chứa các đối số vị trí dư thừa (hoặc một tuple rỗng nếu không có đối số vị trí dư thừa).

Nếu bất kỳ đối số từ khóa nào không tương ứng với tên tham số hình thức, một
ngoại lệ :exc:`TypeError` sẽ được phát sinh, trừ khi có một tham số hình thức sử dụng cú pháp ``**identifier``; trong trường hợp này, tham số hình thức đó nhận một từ điển chứa các đối số từ khóa dư thừa (sử dụng từ khóa làm khóa và giá trị đối số tương ứng làm giá trị), hoặc một từ điển rỗng (mới) nếu không có đối số từ khóa dư thừa.

.. index::
   single: * (asterisk); in function calls
   single: unpacking; in function calls

Nếu cú pháp ``*expression`` xuất hiện trong lần gọi hàm, ``expression`` phải được đánh giá thành một :term:`iterable`. Các phần tử từ những đối tượng iterable này được xử lý như các đối số vị trí bổ sung. Đối với lần gọi ``f(x1, x2, *y, x3, x4)``, nếu *y* được đánh giá thành một dãy *y1*, ..., *yM*, thì điều này tương đương với một lần gọi có M+4 đối số vị trí *x1*, *x2*, *y1*, ..., *yM*, *x3*, *x4*.

Hệ quả là mặc dù cú pháp ``*expression`` có thể xuất hiện *sau* các đối số từ khóa tường minh, nó lại được xử lý *trước* các đối số từ khóa (và mọi đối số ``**expression`` -- xem bên dưới). Vì vậy::

   >>> def f(a, b):
   ...     print(a, b)
   ...
   >>> f(b=1, *(2,))
   2 1
   >>> f(a=1, *(2,))
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: f() got multiple values for keyword argument 'a'
   >>> f(1, *(2,))
   1 2

Việc sử dụng cả các đối số từ khóa và cú pháp ``*expression`` trong cùng một lần gọi là không phổ biến, nên trên thực tế sự nhầm lẫn này hiếm khi xảy ra.

.. index::
   single: **; in function calls

Nếu cú pháp ``**expression`` xuất hiện trong lời gọi hàm, ``expression`` phải đánh giá thành một :term:`mapping`, nội dung của nó được coi là các đối số từ khóa bổ sung. Nếu một tham số tương ứng với một khóa đã được gán giá trị (bằng một đối số từ khóa tường minh hoặc từ một phép unpacking khác), một ngoại lệ :exc:`TypeError` sẽ được phát sinh.

Khi sử dụng ``**expression``, mỗi khóa trong mapping này phải là một chuỗi. Mỗi giá trị trong mapping được gán cho tham số hình thức đầu tiên đủ điều kiện nhận phép gán theo từ khóa và có tên trùng với khóa. Khóa không nhất thiết phải là một định danh Python (ví dụ: ``"max-temp °F"`` là hợp lệ, mặc dù nó sẽ không khớp với bất kỳ tham số hình thức nào có thể được khai báo). Nếu không có tham số hình thức nào khớp, cặp khóa-giá trị sẽ được thu thập bởi tham số ``**``, nếu có; nếu không, một ngoại lệ :exc:`TypeError` sẽ được phát sinh.

Các tham số hình thức sử dụng cú pháp ``*identifier`` hoặc ``**identifier`` không thể được dùng làm vị trí cho đối số vị trí hoặc làm tên đối số từ khóa.

.. versionchanged:: 3.5
   Lời gọi hàm chấp nhận mọi số lượng phép unpacking ``*`` và ``**``; các đối số vị trí có thể đứng sau các phép unpacking iterable (``*``), và các đối số từ khóa có thể đứng sau các phép unpacking dictionary (``**``). Được đề xuất ban đầu bởi :pep:`448`.

Một lời gọi luôn trả về một giá trị nào đó, có thể là ``None``, trừ khi nó phát sinh một ngoại lệ. Cách tính giá trị này phụ thuộc vào loại đối tượng có thể gọi.

Nếu đó là---

một hàm do người dùng định nghĩa:
   .. index::
      pair: function; call
      triple: user-defined; function; call
      pair: object; user-defined function
      pair: object; function

   Khối mã của hàm được thực thi và nhận danh sách đối số. Việc đầu tiên khối mã thực hiện là liên kết các tham số hình thức với các đối số; nội dung này được mô tả trong phần :ref:`function`. Khi khối mã thực thi câu lệnh :keyword:`return`, câu lệnh này xác định giá trị trả về của lời gọi hàm. Nếu quá trình thực thi đi đến cuối khối mã mà không thực thi câu lệnh :keyword:`return`, giá trị trả về sẽ là ``None``.

một hàm hoặc phương thức dựng sẵn:
   .. index::
      pair: function; call
      pair: built-in function; call
      pair: method; call
      pair: built-in method; call
      pair: object; built-in method
      pair: object; built-in function
      pair: object; method
      pair: object; function

   Kết quả do trình thông dịch quyết định; xem :ref:`built-in-funcs` để biết mô tả về các hàm và phương thức dựng sẵn.

một đối tượng lớp:
   .. index::
      pair: object; class
      pair: class object; call

   Một thực thể mới của lớp đó được trả về.

một phương thức instance của class:
   .. index::
      pair: object; class instance
      pair: object; instance
      pair: class instance; call

   Hàm do người dùng định nghĩa tương ứng được gọi, với danh sách đối số dài hơn danh sách đối số của lệnh gọi một đối số: instance trở thành đối số đầu tiên.

một instance của class:
   .. index::
      pair: instance; call
      single: __call__() (object method)

   Class phải định nghĩa một phương thức :meth:`~object.__call__`; khi đó, hiệu ứng sẽ giống như khi phương thức đó được gọi.


.. index:: pair: keyword; await
.. _await:

Biểu thức await
===============

Tạm dừng việc thực thi :term:`coroutine` trên một đối tượng :term:`awaitable`. Chỉ có thể sử dụng bên trong một :term:`coroutine function`.

.. productionlist:: python-grammar
   await_expr: "await" `primary`

.. versionadded:: 3.5


.. _power:

Toán tử lũy thừa
================

.. index::
   pair: power; operation
   pair: operator; **

Toán tử lũy thừa liên kết chặt hơn các toán tử một ngôi ở bên trái; nó liên kết kém chặt hơn các toán tử một ngôi ở bên phải. Cú pháp là:

.. productionlist:: python-grammar
   power: (`await_expr` | `primary`) ["**" `u_expr`]

Do đó, trong một chuỗi không có dấu ngoặc của các toán tử lũy thừa và một ngôi, các toán tử được đánh giá từ phải sang trái (điều này không ràng buộc thứ tự đánh giá các toán hạng): ``-1**2`` cho kết quả là ``-1``.

Toán tử lũy thừa có ngữ nghĩa giống với hàm tích hợp sẵn :func:`pow` khi được gọi với hai đối số: nó cho kết quả là đối số bên trái được nâng lên lũy thừa của đối số bên phải. Các đối số dạng số trước tiên được :ref:`chuyển đổi sang một kiểu chung <stdtypes-mixed-arithmetic>`, và kết quả có kiểu đó.

Đối với các toán hạng int, kết quả có cùng kiểu với các toán hạng, trừ khi đối số thứ hai là số âm; trong trường hợp đó, tất cả các đối số được chuyển đổi thành float và kết quả float được trả về. Ví dụ, ``10**2`` trả về ``100``, nhưng ``10**-2`` trả về ``0.01``.

Nâng ``0.0`` lên một lũy thừa âm sẽ cho kết quả là :exc:`ZeroDivisionError`. Nâng một số âm lên một lũy thừa phân số sẽ cho kết quả là một số :class:`complex`. (Trong các phiên bản trước, thao tác này sẽ phát sinh một :exc:`ValueError`.)

Có thể tùy chỉnh thao tác này bằng cách sử dụng các phương thức đặc biệt :meth:`~object.__pow__` và
:meth:`~object.__rpow__`.

.. _unary:

Các phép toán số học một ngôi và phép toán trên bit
===================================================

.. index::
   triple: unary; arithmetic; operation
   triple: unary; bitwise; operation

Tất cả các phép toán số học một ngôi và phép toán trên bit đều có cùng độ ưu tiên:

.. productionlist:: python-grammar
   u_expr: `power` | "-" `u_expr` | "+" `u_expr` | "~" `u_expr`

.. index::
   single: negation
   single: minus
   single: operator; - (minus)
   single: - (minus); unary operator

Toán tử ``-`` (phép trừ) một ngôi cho kết quả là số đối của đối số dạng số; phép toán này có thể được ghi đè bằng phương thức đặc biệt :meth:`~object.__neg__`.

.. index::
   single: plus
   single: operator; + (plus)
   single: + (plus); unary operator

Toán tử ``+`` (phép cộng) một ngôi cho kết quả là đối số dạng số không thay đổi; phép toán này có thể được ghi đè bằng phương thức đặc biệt :meth:`~object.__pos__`.

.. index::
   single: inversion
   pair: operator; ~ (tilde)

Toán tử ``~`` (phép đảo) một ngôi cho kết quả là phép đảo bit của đối số số nguyên. Phép đảo bit của ``x`` được định nghĩa là ``-(x+1)``. Phép toán này chỉ áp dụng cho các số nguyên hoặc các đối tượng tùy chỉnh ghi đè
phương thức đặc biệt :meth:`~object.__invert__`.



.. index:: pair: exception; TypeError

Trong cả ba trường hợp, nếu đối số không có kiểu thích hợp, một
Ngoại lệ :exc:`TypeError` được ném ra.


.. _binary:

Các phép toán số học nhị phân
=============================

.. index:: triple: binary; arithmetic; operation

Các phép toán số học nhị phân có các mức độ ưu tiên thông thường. Lưu ý rằng một số phép toán trong đó cũng áp dụng cho một số kiểu không phải số. Ngoài toán tử lũy thừa, chỉ có hai mức: một mức dành cho các toán tử nhân và một mức dành cho các toán tử cộng:

.. productionlist:: python-grammar
   m_expr: `u_expr` | `m_expr` "*" `u_expr` | `m_expr` "@" `m_expr` |
         : `m_expr` "//" `u_expr` | `m_expr` "/" `u_expr` |
         : `m_expr` "%" `u_expr`
   a_expr: `m_expr` | `a_expr` "+" `m_expr` | `a_expr` "-" `m_expr`

.. index::
   single: multiplication
   pair: operator; * (asterisk)

Toán tử ``*`` (phép nhân) cho ra tích của các đối số. Các đối số phải либо đều là số, hoặc một đối số phải là số nguyên và đối số còn lại phải là một sequence. Trong trường hợp đầu tiên, các số được
:ref:`chuyển đổi sang một kiểu số thực chung <stdtypes-mixed-arithmetic>` rồi được nhân với nhau. Trong trường hợp thứ hai, phép lặp sequence được thực hiện; hệ số lặp âm tạo ra một sequence rỗng.

Có thể tùy chỉnh phép toán này bằng cách sử dụng các :meth:`~object.__mul__` đặc biệt và
các phương thức :meth:`~object.__rmul__`.

.. versionchanged:: 3.14
   Nếu chỉ một toán hạng là số phức, toán hạng còn lại sẽ được chuyển đổi thành số dấu phẩy động.

.. index::
   single: matrix multiplication
   pair: operator; @ (at)

Toán tử ``@`` (at) được dùng cho phép nhân ma trận. Không có kiểu dựng sẵn nào của Python triển khai toán tử này.

Có thể tùy chỉnh phép toán này bằng cách sử dụng các phương thức đặc biệt :meth:`~object.__matmul__` và
:meth:`~object.__rmatmul__`.

.. versionadded:: 3.5

.. index::
   pair: exception; ZeroDivisionError
   single: division
   pair: operator; / (slash)
   pair: operator; //

Các toán tử ``/`` (phép chia) và ``//`` (phép chia lấy phần nguyên) cho thương của các đối số. Trước tiên, các đối số số học được
:ref:`chuyển đổi sang một kiểu chung <stdtypes-mixed-arithmetic>`. Phép chia các số nguyên cho kết quả là một số thực, trong khi phép chia lấy phần nguyên các số nguyên cho kết quả là một số nguyên; kết quả là phép chia theo toán học với hàm 'floor' được áp dụng cho kết quả. Chia cho số 0 sẽ phát sinh ngoại lệ :exc:`ZeroDivisionError`.

Có thể tùy chỉnh phép chia bằng cách sử dụng các phương thức đặc biệt :meth:`~object.__truediv__` và :meth:`~object.__rtruediv__`. Có thể tùy chỉnh phép chia lấy phần nguyên bằng cách sử dụng phương thức đặc biệt
Các phương thức :meth:`~object.__floordiv__` và :meth:`~object.__rfloordiv__`.

.. index::
   single: modulo
   pair: operator; % (percent)

Toán tử ``%`` (modulo) trả về phần dư của phép chia đối số thứ nhất cho đối số thứ hai. Trước tiên, các đối số số học được
:ref:`chuyển đổi sang một kiểu chung <stdtypes-mixed-arithmetic>`. Đối số bên phải bằng không sẽ phát sinh ngoại lệ :exc:`ZeroDivisionError`. Các đối số có thể là số dấu phẩy động, ví dụ ``3.14%0.7`` bằng ``0.34`` (vì ``3.14`` bằng ``4*0.7 + 0.34``.) Toán tử modulo luôn cho kết quả có cùng dấu với toán hạng thứ hai (hoặc bằng không); giá trị tuyệt đối của kết quả luôn nhỏ hơn giá trị tuyệt đối của toán hạng thứ hai [#]_.

Toán tử chia lấy phần nguyên và modulo được liên kết bởi đẳng thức sau: ``x == (x//y)*y + (x%y)``. Phép chia lấy phần nguyên và modulo cũng liên kết với hàm dựng sẵn :func:`divmod`: ``divmod(x, y) == (x//y, x%y)``. [#]_.

Ngoài việc thực hiện phép toán modulo trên các số, toán tử ``%`` còn được các đối tượng chuỗi nạp chồng để thực hiện định dạng chuỗi kiểu cũ (còn gọi là interpolation). Cú pháp định dạng chuỗi được mô tả trong Python Library Reference, phần :ref:`old-string-formatting`.

Có thể tùy chỉnh phép toán *modulo* bằng các phương thức đặc biệt :meth:`~object.__mod__` và :meth:`~object.__rmod__`.

Toán tử chia lấy phần nguyên, toán tử modulo và hàm :func:`divmod` không được định nghĩa cho số phức. Thay vào đó, hãy chuyển đổi sang số dấu phẩy động bằng hàm :func:`abs` nếu phù hợp.

.. index::
   single: addition
   single: operator; + (plus)
   single: + (plus); binary operator

Toán tử ``+`` (phép cộng) cho kết quả là tổng của các đối số. Các đối số phải hoặc đều là số, hoặc đều là dãy cùng kiểu. Trong trường hợp đầu tiên, các số sẽ
:ref:`được chuyển đổi sang một kiểu thực chung <stdtypes-mixed-arithmetic>` rồi được cộng với nhau. Trong trường hợp thứ hai, các dãy được nối với nhau.

Bạn có thể tùy chỉnh phép toán này bằng cách sử dụng các :meth:`~object.__add__` đặc biệt và
các phương thức :meth:`~object.__radd__`.

.. versionchanged:: 3.14
   Nếu chỉ một toán hạng là số phức, toán hạng còn lại sẽ được chuyển đổi thành số dấu phẩy động.

.. index::
   single: subtraction
   single: operator; - (minus)
   single: - (minus); binary operator

Toán tử ``-`` (phép trừ) cho kết quả là hiệu của các đối số. Các đối số số trước tiên được
:ref:`chuyển đổi sang một kiểu thực chung <stdtypes-mixed-arithmetic>`.

Bạn có thể tùy chỉnh thao tác này bằng các phương thức đặc biệt :meth:`~object.__sub__` và
:meth:`~object.__rsub__`.

.. versionchanged:: 3.14
   Nếu chỉ một toán hạng là số phức, toán hạng còn lại sẽ được chuyển đổi thành số dấu phẩy động.


.. _shifting:

Các thao tác dịch bit
=====================

.. index::
   pair: shifting; operation
   pair: operator; <<
   pair: operator; >>

Các thao tác dịch bit có độ ưu tiên thấp hơn các thao tác số học:

.. productionlist:: python-grammar
   shift_expr: `a_expr` | `shift_expr` ("<<" | ">>") `a_expr`

Các toán tử này nhận số nguyên làm đối số. Chúng dịch đối số thứ nhất sang trái hoặc sang phải theo số bit được chỉ định bởi đối số thứ hai.

Bạn có thể tùy chỉnh thao tác dịch trái bằng các phương thức đặc biệt :meth:`~object.__lshift__` và :meth:`~object.__rlshift__`. Bạn có thể tùy chỉnh thao tác dịch phải bằng các phương thức đặc biệt :meth:`~object.__rshift__` và :meth:`~object.__rrshift__`.

.. index:: pair: exception; ValueError

Phép dịch phải *n* bit được định nghĩa là phép chia lấy phần nguyên cho ``pow(2,n)``. Phép dịch trái *n* bit được định nghĩa là phép nhân với ``pow(2,n)``.


.. _bitwise:

Các phép toán bitwise nhị phân
==============================

.. index:: triple: binary; bitwise; operation

Mỗi trong ba phép toán bitwise có một mức độ ưu tiên khác nhau:

.. productionlist:: python-grammar
   and_expr: `shift_expr` | `and_expr` "&" `shift_expr`
   xor_expr: `and_expr` | `xor_expr` "^" `and_expr`
   or_expr: `xor_expr` | `or_expr` "|" `xor_expr`

.. index::
   pair: bitwise; and
   pair: operator; & (ampersand)

Toán tử ``&`` cho kết quả là phép AND bitwise của các đối số; các đối số này phải là số nguyên hoặc một trong số đó phải là đối tượng tùy chỉnh ghi đè :meth:`~object.__and__` hoặc
các phương thức đặc biệt :meth:`~object.__rand__`.

.. index::
   pair: bitwise; xor
   pair: exclusive; or
   pair: operator; ^ (caret)

Toán tử ``^`` cho kết quả là phép XOR bitwise (OR loại trừ) của các đối số; các đối số này phải là số nguyên hoặc một trong số đó phải là đối tượng tùy chỉnh ghi đè :meth:`~object.__xor__` hoặc
các phương thức đặc biệt :meth:`~object.__rxor__`.

.. index::
   pair: bitwise; or
   pair: inclusive; or
   pair: operator; | (vertical bar)

Toán tử ``|`` cho kết quả là phép OR theo bit (bao gồm) của các đối số, các đối số này phải là số nguyên hoặc một trong số chúng phải là đối tượng tùy chỉnh ghi đè :meth:`~object.__or__` hoặc
các phương thức đặc biệt :meth:`~object.__ror__`.


.. _comparisons:

So sánh
=======

.. index::
   single: comparison
   pair: C; language
   pair: operator; < (less)
   pair: operator; > (greater)
   pair: operator; <=
   pair: operator; >=
   pair: operator; ==
   pair: operator; !=

Không giống C, tất cả các phép toán so sánh trong Python có cùng mức độ ưu tiên, thấp hơn mọi phép toán số học, dịch bit hoặc theo bit. Cũng không giống C, các biểu thức như ``a < b < c`` được hiểu theo cách thông thường trong toán học:

.. productionlist:: python-grammar
   comparison: `or_expr` (`comp_operator` `or_expr`)*
   comp_operator: "<" | ">" | "==" | ">=" | "<=" | "!="
                : | "is" ["not"] | ["not"] "in"

Các phép so sánh cho kết quả là các giá trị boolean: ``True`` hoặc ``False``. Các đối tượng tùy chỉnh
:dfn:`các phương thức so sánh mở rộng` có thể trả về các giá trị không phải boolean. Trong trường hợp này, Python sẽ gọi :func:`bool` trên giá trị đó trong các ngữ cảnh boolean.

.. index:: pair: chaining; comparisons

Các phép so sánh có thể được nối tùy ý, chẳng hạn như ``x < y <= z`` tương đương với ``x < y and y <= z``, ngoại trừ việc ``y`` chỉ được đánh giá một lần (nhưng trong cả hai trường hợp, ``z`` hoàn toàn không được đánh giá khi ``x < y`` được xác định là false).

Về mặt hình thức, nếu *a*, *b*, *c*, ..., *y*, *z* là các biểu thức và *op1*, *op2*, ..., *opN* là các toán tử so sánh, thì ``a op1 b op2 c ... y opN z`` tương đương với ``a op1 b and b op2 c and ... y opN z``, ngoại trừ việc mỗi biểu thức được đánh giá nhiều nhất một lần.

Lưu ý rằng ``a op1 b op2 c`` không ngụ ý bất kỳ kiểu so sánh nào giữa *a* và *c*, vì vậy, chẳng hạn, ``x < y > z`` hoàn toàn hợp lệ (dù có thể không đẹp mắt).

.. _expressions-value-comparisons:

So sánh giá trị
---------------

Các toán tử ``<``, ``>``, ``==``, ``>=``, ``<=`` và ``!=`` so sánh giá trị của hai đối tượng. Hai đối tượng không cần phải có cùng kiểu.

Chương :ref:`objects` nêu rằng các đối tượng có một giá trị (ngoài kiểu và danh tính). Trong Python, giá trị của một đối tượng là một khái niệm khá trừu tượng: Ví dụ, không có phương thức truy cập chuẩn tắc nào cho giá trị của một đối tượng. Ngoài ra, không có yêu cầu nào rằng giá trị của một đối tượng phải được tạo dựng theo một cách cụ thể, chẳng hạn như bao gồm tất cả các thuộc tính dữ liệu của đối tượng. Các toán tử so sánh triển khai một cách hiểu cụ thể về giá trị của một đối tượng. Có thể coi chúng là cách định nghĩa gián tiếp giá trị của một đối tượng thông qua phần triển khai phép so sánh của chúng.

Vì mọi kiểu đều là kiểu con (trực tiếp hoặc gián tiếp) của :class:`object`, chúng kế thừa hành vi so sánh mặc định từ :class:`object`. Các kiểu có thể tùy chỉnh hành vi so sánh của mình bằng cách triển khai
:dfn:`các phương thức so sánh mở rộng` như :meth:`~object.__lt__`, được mô tả trong
:ref:`customization`.

Hành vi mặc định của phép so sánh bằng (``==`` và ``!=``) dựa trên định danh của các đối tượng. Do đó, phép so sánh bằng giữa các instance có cùng định danh cho kết quả bằng nhau, còn phép so sánh bằng giữa các instance có định danh khác nhau cho kết quả không bằng nhau. Một lý do cho hành vi mặc định này là mong muốn tất cả đối tượng đều có tính phản xạ (tức là ``x is y`` kéo theo ``x == y``).

Không có phép so sánh thứ tự mặc định (``<``, ``>``, ``<=`` và ``>=``); một nỗ lực thực hiện phép so sánh này sẽ raise :exc:`TypeError`. Một lý do cho hành vi mặc định này là không có bất biến tương tự như đối với phép so sánh bằng.

Hành vi của phép so sánh bằng mặc định, theo đó các instance có định danh khác nhau luôn không bằng nhau, có thể trái với nhu cầu của những kiểu có định nghĩa hợp lý về giá trị đối tượng và phép so sánh bằng dựa trên giá trị. Những kiểu như vậy cần tùy chỉnh hành vi so sánh, và thực tế là một số kiểu dựng sẵn đã làm điều đó.

Danh sách sau đây mô tả hành vi so sánh của những kiểu dựng sẵn quan trọng nhất.

* Các số thuộc những kiểu số dựng sẵn (:ref:`typesnumeric`) và các kiểu thuộc standard library :class:`fractions.Fraction` và :class:`decimal.Decimal` có thể được so sánh trong cùng kiểu cũng như giữa các kiểu, với hạn chế là số phức không hỗ trợ phép so sánh thứ tự. Trong giới hạn của các kiểu liên quan, chúng được so sánh một cách đúng đắn về mặt toán học (thuật toán) mà không mất độ chính xác.

  Các giá trị not-a-number ``float('NaN')`` và ``decimal.Decimal('NaN')`` là những giá trị đặc biệt. Mọi phép so sánh có thứ tự giữa một số và giá trị not-a-number đều cho kết quả false. Một hệ quả trái với trực giác là các giá trị not-a-number không bằng chính chúng. Ví dụ, nếu ``x = float('NaN')``, ``3 < x``, ``x < 3`` và ``x == x`` đều false, còn ``x != x`` là true. Hành vi này tuân thủ IEEE 754.

* ``None`` và :data:`NotImplemented` là các singleton. :PEP:`8` khuyến nghị rằng việc so sánh các singleton luôn phải được thực hiện bằng ``is`` hoặc ``is not``, không bao giờ dùng các toán tử so sánh bằng.

* Các chuỗi nhị phân (các thể hiện của :class:`bytes` hoặc :class:`bytearray`) có thể được so sánh trong cùng một kiểu và giữa các kiểu. Chúng được so sánh theo thứ tự từ điển bằng cách sử dụng các giá trị số của phần tử.

* Các chuỗi (các thể hiện của :class:`str`) được so sánh theo thứ tự từ điển bằng cách sử dụng các điểm mã Unicode dạng số (kết quả của hàm tích hợp sẵn
  :func:`ord`) của các ký tự. [#]_

  Không thể so sánh trực tiếp chuỗi và chuỗi nhị phân.

* Các sequence (các thể hiện của :class:`tuple`, :class:`list` hoặc :class:`range`) chỉ có thể được so sánh trong từng kiểu tương ứng, với hạn chế là các range không hỗ trợ so sánh thứ tự. So sánh bằng giữa các kiểu này cho kết quả không bằng nhau, còn so sánh thứ tự giữa các kiểu này sẽ phát sinh
  :exc:`TypeError`.

  Các sequence được so sánh theo thứ tự từ điển bằng cách so sánh các phần tử tương ứng. Các container tích hợp sẵn thường giả định rằng các đối tượng giống hệt nhau thì bằng nhau với chính chúng. Điều này cho phép chúng bỏ qua các phép kiểm tra bằng nhau đối với các đối tượng giống hệt để cải thiện hiệu suất và duy trì các bất biến nội bộ.

  So sánh theo thứ tự từ điển giữa các collection tích hợp sẵn hoạt động như sau:

  - Để hai collection được xem là bằng nhau, chúng phải cùng kiểu, có cùng độ dài và mỗi cặp phần tử tương ứng phải bằng nhau (ví dụ: ``[1,2] == (1,2)`` là false vì kiểu không giống nhau).

  - Các collection hỗ trợ so sánh thứ tự được sắp xếp theo phần tử đầu tiên không bằng nhau của chúng (ví dụ: ``[1,2,x] <= [1,2,y]`` có cùng giá trị với ``x <= y``). Nếu không tồn tại phần tử tương ứng, collection ngắn hơn được sắp xếp trước (ví dụ: ``[1,2] < [1,2,3]`` là true).

* Mappings (các instance của :class:`dict`) được xem là bằng nhau khi và chỉ khi chúng có các cặp ``(key, value)`` bằng nhau. Việc so sánh bằng của các khóa và giá trị đảm bảo tính phản xạ.

  Các phép so sánh thứ tự (``<``, ``>``, ``<=`` và ``>=``) sẽ phát sinh :exc:`TypeError`.

* Các set (các instance của :class:`set` hoặc :class:`frozenset`) có thể được so sánh trong cùng kiểu và giữa các kiểu.

  Chúng định nghĩa các toán tử so sánh thứ tự là các phép kiểm tra tập con và tập cha. Những quan hệ này không xác định thứ tự toàn phần (ví dụ: hai set ``{1,2}`` và ``{2,3}`` không bằng nhau, cũng không là tập con hoặc tập cha của nhau). Vì vậy, set không phù hợp làm đối số cho các hàm phụ thuộc vào thứ tự toàn phần (ví dụ: :func:`min`, :func:`max` và
  :func:`sorted` cho kết quả không xác định khi đầu vào là một danh sách các set).

  Việc so sánh các tập hợp đảm bảo tính phản xạ của các phần tử trong chúng.

* Hầu hết các kiểu tích hợp khác không triển khai các phương thức so sánh, vì vậy chúng kế thừa hành vi so sánh mặc định.

Các lớp do người dùng định nghĩa tùy chỉnh hành vi so sánh nên tuân theo một số quy tắc nhất quán, nếu có thể:

* Phép so sánh bằng nên có tính phản xạ. Nói cách khác, các đối tượng giống hệt nhau nên được so sánh là bằng nhau:

    ``x is y`` ngụ ý ``x == y``

* Phép so sánh nên có tính đối xứng. Nói cách khác, các biểu thức sau nên cho cùng một kết quả:

    ``x == y`` và ``y == x``

    ``x != y`` và ``y != x``

    ``x < y`` và ``y > x``

    ``x <= y`` và ``y >= x``

* Phép so sánh phải có tính bắc cầu. Các ví dụ sau đây (không đầy đủ) minh họa điều đó:

    ``x > y and y > z`` suy ra ``x > z``

    ``x < y and y <= z`` suy ra ``x < z``

* Phép so sánh nghịch đảo phải cho kết quả là phủ định Boolean. Nói cách khác, các biểu thức sau phải cho cùng một kết quả:

    ``x == y`` và ``not x != y``

    ``x < y`` và ``not x >= y`` (để sắp thứ tự toàn phần)

    ``x > y`` và ``not x <= y`` (để sắp thứ tự toàn phần)

  Hai biểu thức cuối áp dụng cho các tập hợp có thứ tự toàn phần (ví dụ: các dãy, nhưng không áp dụng cho các tập hợp hoặc ánh xạ). Xem thêm
  decorator :deco:`~functools.total_ordering`.

* Kết quả :func:`hash` phải nhất quán với phép so sánh bằng. Các đối tượng bằng nhau phải có cùng giá trị băm hoặc được đánh dấu là không thể băm.

Python không thực thi các quy tắc nhất quán này. Trên thực tế, các giá trị không phải là số (not-a-number) là một ví dụ về việc không tuân theo các quy tắc này.


.. _in:
.. _not in:
.. _membership-test-details:

Các phép toán kiểm tra thành viên
---------------------------------

Các toán tử :keyword:`in` và :keyword:`not in` dùng để kiểm tra thành viên. ``x in s`` cho kết quả ``True`` nếu *x* là thành viên của *s*, và ``False`` trong trường hợp ngược lại. ``x not in s`` trả về phủ định của ``x in s``. Tất cả các sequence và kiểu set dựng sẵn đều hỗ trợ phép toán này, cũng như dictionary; với dictionary, :keyword:`!in` kiểm tra xem dictionary có một key nhất định hay không. Đối với các kiểu container như list, tuple, set, frozenset, dict hoặc collections.deque, biểu thức ``x in y`` tương đương với ``any(x is e or x == e for e in y)``.

Đối với kiểu string và bytes, ``x in y`` là ``True`` khi và chỉ khi *x* là một substring của *y*. Một phép kiểm tra tương đương là ``y.find(x) != -1``. String rỗng luôn được xem là substring của mọi string khác, vì vậy ``"" in "abc"`` sẽ trả về ``True``.

Đối với các class do người dùng định nghĩa có phương thức :meth:`~object.__contains__`, ``x in y`` trả về ``True`` nếu ``y.__contains__(x)`` trả về một giá trị đúng, và ``False`` trong trường hợp ngược lại.

Đối với các class do người dùng định nghĩa không có :meth:`~object.__contains__` nhưng có định nghĩa
:meth:`~object.__iter__`, ``x in y`` là ``True`` nếu một giá trị ``z``, mà biểu thức ``x is z or x == z`` cho kết quả đúng, được tạo ra trong khi lặp qua ``y``. Nếu một exception được phát sinh trong quá trình lặp, thì kết quả giống như :keyword:`in` đã phát sinh exception đó.

Cuối cùng, giao thức lặp kiểu cũ được thử: nếu một class định nghĩa
:meth:`~object.__getitem__`, ``x in y`` là ``True`` khi và chỉ khi tồn tại một chỉ số nguyên không âm *i* sao cho ``x is y[i] or x == y[i]``, và không có chỉ số nguyên nhỏ hơn nào làm phát sinh ngoại lệ :exc:`IndexError`. (Nếu phát sinh bất kỳ ngoại lệ nào khác thì coi như :keyword:`in` đã phát sinh ngoại lệ đó).

.. index::
   pair: operator; in
   pair: operator; not in
   pair: membership; test
   pair: object; sequence

Toán tử :keyword:`not in` được định nghĩa là có giá trị logic ngược với
:keyword:`in`.

.. index::
   pair: operator; is
   pair: operator; is not
   pair: identity; test


.. _is:
.. _is not:

So sánh định danh
-----------------

Các toán tử :keyword:`is` và :keyword:`is not` kiểm tra định danh của một đối tượng: ``x is y`` là đúng khi và chỉ khi *x* và *y* là cùng một đối tượng. Định danh của một Object được xác định bằng hàm :meth:`id`. ``x is not y`` cho giá trị logic ngược lại. [#]_


.. _booleans:
.. _and:
.. _or:
.. _not:

Các phép toán Boolean
=====================

.. index::
   pair: Conditional; expression
   pair: Boolean; operation

.. productionlist:: python-grammar
   or_test: `and_test` | `or_test` "or" `and_test`
   and_test: `not_test` | `and_test` "and" `not_test`
   not_test: `comparison` | "not" `not_test`

Trong ngữ cảnh của các phép toán Boolean, cũng như khi các biểu thức được sử dụng bởi các câu lệnh điều khiển luồng, các giá trị sau được diễn giải là false: ``False``, ``None``, số 0 thuộc mọi kiểu, cùng các chuỗi và vùng chứa rỗng (bao gồm chuỗi, tuple, danh sách, dictionary, set và frozenset). Tất cả các giá trị khác được diễn giải là true. Các đối tượng do người dùng định nghĩa có thể tùy chỉnh giá trị truth của chúng bằng cách cung cấp phương thức :meth:`~object.__bool__`.

.. index:: pair: operator; not

Toán tử :keyword:`not` cho kết quả ``True`` nếu đối số của nó là false, và ``False`` nếu không.

.. index:: pair: operator; and

Biểu thức ``x and y`` trước tiên đánh giá *x*; nếu *x* là false, giá trị của nó được trả về; nếu không, *y* được đánh giá và giá trị thu được được trả về.

.. index:: pair: operator; or

Biểu thức ``x or y`` trước tiên đánh giá *x*; nếu *x* là true, giá trị của nó được trả về; nếu không, *y* được đánh giá và giá trị thu được được trả về.

Lưu ý rằng cả :keyword:`and` lẫn :keyword:`or` đều không giới hạn giá trị và kiểu mà chúng trả về ở ``False`` và ``True``, mà thay vào đó trả về đối số được đánh giá cuối cùng. Điều này đôi khi hữu ích; ví dụ, nếu ``s`` là một chuỗi cần được thay bằng giá trị mặc định khi rỗng, biểu thức ``s or 'foo'`` sẽ cho ra giá trị mong muốn. Vì :keyword:`not` phải tạo một giá trị mới, nó luôn trả về một giá trị boolean bất kể kiểu của đối số là gì (ví dụ: ``not 'foo'`` tạo ra ``False`` thay vì ``''``.)


.. index::
   single: := (colon equals)
   single: assignment expression
   single: walrus operator
   single: named expression
   pair: assignment; expression

.. _assignment-expressions:

Biểu thức gán
=============

.. productionlist:: python-grammar
   assignment_expression: [`identifier` ":="] `expression`

Biểu thức gán (đôi khi còn được gọi là "named expression" hoặc "walrus") gán một :token:`~python-grammar:expression` cho một
:token:`~python-grammar:identifier`, đồng thời trả về giá trị của
:token:`~python-grammar:expression`.

Một trường hợp sử dụng phổ biến là khi xử lý các regular expression khớp:

.. code-block:: python

   if matching := pattern.search(data):
       do_something(matching)

Hoặc khi xử lý một luồng tệp theo từng khối:

.. code-block:: python

   while chunk := file.read(9000):
       process(chunk)

Các biểu thức gán phải được đặt trong dấu ngoặc đơn khi được sử dụng làm câu lệnh biểu thức và khi được sử dụng làm biểu thức con trong các biểu thức cắt, điều kiện, lambda, đối số từ khóa và if của comprehension, cũng như trong các câu lệnh ``assert``, ``with`` và ``assignment``. Trong mọi trường hợp khác mà chúng có thể được sử dụng, dấu ngoặc đơn không bắt buộc, bao gồm trong các câu lệnh ``if`` và ``while``.

.. versionadded:: 3.8
   Xem :pep:`572` để biết thêm chi tiết về các biểu thức gán.


.. _if_expr:

Biểu thức điều kiện
===================

.. index::
   pair: conditional; expression
   pair: ternary; operator
   single: if; conditional expression
   single: else; conditional expression

.. productionlist:: python-grammar
   conditional_expression: `or_test` ["if" `or_test` "else" `expression`]
   expression: `conditional_expression` | `lambda_expr`

Biểu thức điều kiện (đôi khi được gọi là "toán tử ba ngôi") là một lựa chọn thay thế cho câu lệnh if-else. Vì là một biểu thức, nó trả về một giá trị và có thể xuất hiện dưới dạng biểu thức con.

Biểu thức ``x if C else y`` trước tiên đánh giá điều kiện, *C* thay vì *x*. Nếu *C* là đúng, *x* sẽ được đánh giá và giá trị của nó được trả về; nếu không, *y* sẽ được đánh giá và giá trị của nó được trả về.

Xem :pep:`308` để biết thêm chi tiết về các biểu thức điều kiện.


.. _lambdas:
.. _lambda:

Lambda
======

.. index::
   pair: lambda; expression
   pair: lambda; form
   pair: anonymous; function
   single: : (colon); lambda expression

.. productionlist:: python-grammar
   lambda_expr: "lambda" [`parameter_list`] ":" `expression`

Biểu thức lambda (đôi khi được gọi là dạng lambda) được dùng để tạo các hàm ẩn danh. Biểu thức ``lambda parameters: expression`` trả về một đối tượng hàm. Đối tượng không có tên này hoạt động như một đối tượng hàm được định nghĩa bằng:

.. code-block:: none

   def <lambda>(parameters):
       return expression

Xem phần :ref:`function` để biết cú pháp của danh sách tham số. Lưu ý rằng các hàm được tạo bằng biểu thức lambda không thể chứa câu lệnh hoặc chú thích kiểu.


.. _exprlists:

Danh sách biểu thức
===================

.. index::
   pair: expression; list
   single: , (comma); expression list

.. productionlist:: python-grammar
   starred_expression: "*" `or_expr` | `expression`
   flexible_expression: `assignment_expression` | `starred_expression`
   flexible_expression_list: `flexible_expression` ("," `flexible_expression`)* [","]
   starred_expression_list: `starred_expression` ("," `starred_expression`)* [","]
   expression_list: `expression` ("," `expression`)* [","]
   yield_list: `expression_list` | `starred_expression` "," [`starred_expression_list`]

.. index:: pair: object; tuple

Ngoại trừ khi là một phần của phép hiển thị danh sách hoặc tập hợp, một danh sách biểu thức chứa ít nhất một dấu phẩy sẽ tạo ra một tuple. Độ dài của tuple là số lượng biểu thức trong danh sách. Các biểu thức được đánh giá từ trái sang phải.

.. index::
   pair: iterable; unpacking
   single: * (asterisk); in expression lists

Dấu hoa thị ``*`` biểu thị :dfn:`việc unpack iterable`. Toán hạng của nó phải là một :term:`iterable`. Iterable được mở rộng thành một chuỗi các mục, rồi được đưa vào tuple, list hoặc set mới tại vị trí unpack.

.. versionadded:: 3.5
   Việc unpack iterable trong các danh sách biểu thức, được đề xuất lần đầu bởi :pep:`448`.

.. versionadded:: 3.11
   Mọi mục trong danh sách biểu thức đều có thể được đánh dấu sao. Xem :pep:`646`.

.. index:: pair: trailing; comma

Dấu phẩy ở cuối chỉ bắt buộc để tạo một tuple một phần tử, chẳng hạn như ``1,``; trong mọi trường hợp khác, dấu phẩy này là tùy chọn. Một biểu thức đơn lẻ không có dấu phẩy ở cuối không tạo tuple mà trả về giá trị của biểu thức đó. (Để tạo một tuple rỗng, hãy dùng một cặp dấu ngoặc đơn rỗng: ``()``.)


.. _evalorder:

Thứ tự đánh giá
===============

.. index:: pair: evaluation; order

Python đánh giá các biểu thức từ trái sang phải. Lưu ý rằng khi đánh giá một phép gán, vế phải được đánh giá trước vế trái.

Trong các dòng sau, các biểu thức sẽ được đánh giá theo thứ tự số học của các hậu tố::

   expr1, expr2, expr3, expr4
   (expr1, expr2, expr3, expr4)
   {expr1: expr2, expr3: expr4}
   expr1 + expr2 * (expr3 - expr4)
   expr1(expr2, expr3, *expr4, **expr5)
   expr3, expr4 = expr1, expr2


.. _operator-summary:

Độ ưu tiên của toán tử
======================

.. index::
   pair: operator; precedence

Bảng sau đây tóm tắt độ ưu tiên của các toán tử trong Python, từ độ ưu tiên cao nhất (liên kết chặt nhất) đến thấp nhất (liên kết lỏng nhất). Các toán tử trong cùng một ô có cùng độ ưu tiên. Trừ khi cú pháp được nêu rõ, các toán tử là toán tử nhị phân. Các toán tử trong cùng một ô được nhóm từ trái sang phải (ngoại trừ phép lũy thừa và các biểu thức điều kiện, được nhóm từ phải sang trái).

Lưu ý rằng các phép so sánh, phép kiểm tra thành viên và phép kiểm tra định danh đều có cùng độ ưu tiên và có tính năng nối từ trái sang phải như được mô tả trong
:ref:`comparisons`.


+---------------------------------------------+------------------------------------------------------------------------------------------------------------------+
| Toán tử                                     | Mô tả                                                                                                            |
+=============================================+==================================================================================================================+
| ``(expressions...)``,                       | Biểu thức liên kết hoặc biểu thức đặt trong dấu ngoặc, biểu diễn danh sách, biểu diễn từ điển, biểu diễn tập hợp |
|                                             |                                                                                                                  |
| ``[expressions...]``,                       |                                                                                                                  |
| ``{key: value...}``,                        |                                                                                                                  |
| ``{expressions...}``                        |                                                                                                                  |
+---------------------------------------------+------------------------------------------------------------------------------------------------------------------+
| ``x[index]``, ``x[index:index]``            | Phép truy xuất (bao gồm cả việc cắt lát), lời gọi, tham chiếu thuộc tính                                         |
| ``x(arguments...)``, ``x.attribute``        |                                                                                                                  |
+---------------------------------------------+------------------------------------------------------------------------------------------------------------------+
| :keyword:`await x <await>`                  | Biểu thức await                                                                                                  |
+---------------------------------------------+------------------------------------------------------------------------------------------------------------------+
| ``**``                                      | Lũy thừa [#]_                                                                                                    |
+---------------------------------------------+------------------------------------------------------------------------------------------------------------------+
| ``+x``, ``-x``, ``~x``                      | Số dương, số âm, NOT bitwise                                                                                     |
+---------------------------------------------+------------------------------------------------------------------------------------------------------------------+
| ``*``, ``@``, ``/``, ``//``, ``%``          | Phép nhân, phép nhân ma trận, phép chia, phép chia lấy phần nguyên, phần dư [#]_                                 |
+---------------------------------------------+------------------------------------------------------------------------------------------------------------------+
| ``+``, ``-``                                | Phép cộng và phép trừ                                                                                            |
+---------------------------------------------+------------------------------------------------------------------------------------------------------------------+
| ``<<``, ``>>``                              | Phép dịch                                                                                                        |
+---------------------------------------------+------------------------------------------------------------------------------------------------------------------+
| ``&``                                       | AND bitwise                                                                                                      |
+---------------------------------------------+------------------------------------------------------------------------------------------------------------------+
| ``^``                                       | XOR bitwise                                                                                                      |
+---------------------------------------------+------------------------------------------------------------------------------------------------------------------+
| ``|``                                       | Phép OR theo bit                                                                                                 |
+---------------------------------------------+------------------------------------------------------------------------------------------------------------------+
| :keyword:`in`, :keyword:`not in`,           | Các phép so sánh, bao gồm kiểm tra thành viên và kiểm tra đồng nhất                                              |
| :keyword:`is`, :keyword:`is not`, ``<``,    |                                                                                                                  |
| ``<=``, ``>``, ``>=``, ``!=``, ``==``       |                                                                                                                  |
+---------------------------------------------+------------------------------------------------------------------------------------------------------------------+
| :keyword:`not x <not>`                      | Phép NOT logic                                                                                                   |
+---------------------------------------------+------------------------------------------------------------------------------------------------------------------+
| :keyword:`and`                              | Phép AND logic                                                                                                   |
+---------------------------------------------+------------------------------------------------------------------------------------------------------------------+
| :keyword:`or`                               | Phép OR logic                                                                                                    |
+---------------------------------------------+------------------------------------------------------------------------------------------------------------------+
| :keyword:`if <if_expr>` -- :keyword:`!else` | Biểu thức điều kiện                                                                                              |
+---------------------------------------------+------------------------------------------------------------------------------------------------------------------+
| :keyword:`lambda`                           | Biểu thức lambda                                                                                                 |
+---------------------------------------------+------------------------------------------------------------------------------------------------------------------+
| ``:=``                                      | Biểu thức gán                                                                                                    |
+---------------------------------------------+------------------------------------------------------------------------------------------------------------------+


.. rubric:: Chú thích cuối trang

.. [#] Mặc dù ``abs(x%y) < abs(y)`` đúng về mặt toán học, nhưng đối với số thực, điều này có thể không đúng về mặt số học do sai số làm tròn. Ví dụ, giả sử nền tảng sử dụng số thực Python là số dấu phẩy động double-precision theo IEEE 754, để ``-1e-100 % 1e100`` có cùng dấu với ``1e100``, kết quả tính được là ``-1e-100 + 1e100``, về mặt số học chính xác bằng ``1e100``. Hàm
   :func:`math.fmod` thay vào đó trả về kết quả có dấu trùng với dấu của đối số đầu tiên, vì vậy trong trường hợp này trả về ``-1e-100``. Cách tiếp cận nào phù hợp hơn còn tùy thuộc vào ứng dụng.

.. [#] Nếu x rất gần với một bội số nguyên chính xác của y, ``x//y`` có thể lớn hơn ``(x-x%y)//y`` một đơn vị do làm tròn. Trong những trường hợp như vậy, Python trả về kết quả sau, nhằm đảm bảo rằng ``divmod(x,y)[0] * y + x % y`` vẫn rất gần với ``x``.

.. [#] Tiêu chuẩn Unicode phân biệt giữa :dfn:`các điểm mã` (ví dụ U+0041) và :dfn:`các ký tự trừu tượng` (ví dụ "LATIN CAPITAL LETTER A"). Mặc dù hầu hết các ký tự trừu tượng trong Unicode chỉ được biểu diễn bằng một điểm mã, vẫn có một số ký tự trừu tượng có thể được biểu diễn bổ sung bằng một chuỗi gồm nhiều hơn một điểm mã. Ví dụ, ký tự trừu tượng "LATIN CAPITAL LETTER C WITH CEDILLA" có thể được biểu diễn dưới dạng một :dfn:`ký tự dựng sẵn` duy nhất tại vị trí mã U+00C7, hoặc dưới dạng một chuỗi gồm :dfn:`ký tự cơ sở` tại vị trí mã U+0043 (LATIN CAPITAL LETTER C), theo sau là :dfn:`ký tự kết hợp` tại vị trí mã U+0327 (COMBINING CEDILLA).

   Các toán tử so sánh trên chuỗi thực hiện so sánh ở cấp độ các điểm mã Unicode. Điều này có thể phản trực giác đối với con người. Ví dụ, ``"\u00C7" == "\u0043\u0327"`` là ``False``, mặc dù cả hai chuỗi đều biểu diễn cùng một ký tự trừu tượng "LATIN CAPITAL LETTER C WITH CEDILLA".

   Để so sánh các chuỗi ở cấp độ ký tự trừu tượng (tức là theo cách trực quan đối với con người), hãy sử dụng :func:`unicodedata.normalize`.

.. [#] Do cơ chế thu gom rác tự động, các free list và bản chất động của các descriptor, bạn có thể nhận thấy hành vi có vẻ bất thường trong một số trường hợp sử dụng toán tử :keyword:`is`, chẳng hạn như khi so sánh các method của instance hoặc các hằng số. Hãy xem tài liệu của chúng để biết thêm thông tin.

.. [#] Toán tử lũy thừa ``**`` có độ ưu tiên thấp hơn một toán tử một ngôi số học hoặc bit ở bên phải nó, tức là ``2**-1`` tương đương với ``0.5``.

.. [#] Toán tử ``%`` cũng được dùng để định dạng chuỗi; quy tắc ưu tiên tương tự được áp dụng.
