:mod:`!string.templatelib` --- Hỗ trợ các chuỗi ký tự mẫu
=========================================================

.. module:: string.templatelib
   :synopsis: Hỗ trợ các chuỗi ký tự mẫu.

**Mã nguồn:** :source:`Lib/string/templatelib.py`

--------------

.. seealso::

   * :ref:`Chuỗi định dạng <f-strings>`
   * :ref:`Cú pháp chuỗi ký tự mẫu (t-string) <t-strings>`
   * :pep:`750`

.. _template-strings:

Chuỗi mẫu
---------

.. versionadded:: 3.14

Chuỗi mẫu là một cơ chế để xử lý chuỗi tùy chỉnh. Chúng có đầy đủ tính linh hoạt của :ref:`f-strings` của Python, nhưng trả về một thực thể :class:`Template` cho phép truy cập vào các phần tĩnh và phần nội suy (trong ngoặc nhọn) của một chuỗi *trước* khi chúng được kết hợp.

Để viết một t-string, hãy sử dụng tiền tố ``'t'`` thay vì một ``'f'``, như sau:

.. code-block:: pycon

   >>> pi = 3.14
   >>> t't-strings are new in Python {pi!s}!'
   Template(
      strings=('t-strings are new in Python ', '!'),
      interpolations=(Interpolation(3.14, 'pi', 's', ''),)
   )

Các kiểu
--------

.. class:: Template

   Lớp :class:`!Template` mô tả nội dung của một template string. Lớp này bất biến, nghĩa là không thể gán lại các thuộc tính của template.

   Cách phổ biến nhất để tạo một đối tượng :class:`!Template` là sử dụng
   :ref:`cú pháp literal template string <t-strings>`. Cú pháp này giống hệt cú pháp của :ref:`f-strings <f-strings>`, ngoại trừ việc sử dụng tiền tố ``t`` thay cho ``f``:

   >>> cheese = 'Red Leicester'
   >>> template = t"We're fresh out of {cheese}, sir."
   >>> type(template)
   <class 'string.templatelib.Template'>

   Các template được lưu trữ dưới dạng chuỗi gồm :attr:`~Template.strings` literal và :attr:`~Template.interpolations` động. Một thuộc tính :attr:`~Template.values` chứa các giá trị của những phép nội suy:

   >>> cheese = 'Camembert'
   >>> template = t'Ah! We do have {cheese}.'
   >>> template.strings
   ('Ah! We do have ', '.')
   >>> template.interpolations
   (Interpolation('Camembert', ...),)
   >>> template.values
   ('Camembert',)

   Tuple :attr:`!strings` có nhiều hơn một phần tử so với :attr:`!interpolations` và :attr:`!values`; các phép nội suy “thuộc về” phần nằm giữa các chuỗi. Điều này có thể dễ hiểu hơn khi các tuple được căn chỉnh

   .. code-block:: python

      template.strings:  ('Ah! We do have ',              '.')
      template.values:   (                   'Camembert',    )

   .. rubric:: Thuộc tính

   .. attribute:: strings
      :type: tuple[str, ...]

      Một :class:`tuple` gồm các chuỗi tĩnh trong template.

      >>> cheese = 'Camembert'
      >>> template = t'Ah! We do have {cheese}.'
      >>> template.strings
      ('Ah! We do have ', '.')

      Các chuỗi rỗng *được* đưa vào tuple:

      >>> response = 'We do have '
      >>> cheese = 'Camembert'
      >>> template = t'Ah! {response}{cheese}.'
      >>> template.strings
      ('Ah! ', '', '.')

      Tuple ``strings`` không bao giờ rỗng và luôn chứa nhiều hơn một chuỗi so với các tuple ``interpolations`` và ``values``:

      >>> t''.strings
      ('',)
      >>> t''.values
      ()
      >>> t'{'cheese'}'.strings
      ('', '')
      >>> t'{'cheese'}'.values
      ('cheese',)

   .. attribute:: interpolations
      :type: tuple[Interpolation, ...]

      Một :class:`tuple` gồm các phép nội suy trong template.

      >>> cheese = 'Camembert'
      >>> template = t'Ah! We do have {cheese}.'
      >>> template.interpolations
      (Interpolation('Camembert', 'cheese', None, ''),)

      Tuple ``interpolations`` có thể rỗng và luôn chứa ít hơn một giá trị so với tuple ``strings``:

      >>> t'Red Leicester'.interpolations
      ()

   .. attribute:: values
      :type: tuple[object, ...]

      Một tuple chứa tất cả các giá trị được nội suy trong template.

      >>> cheese = 'Camembert'
      >>> template = t'Ah! We do have {cheese}.'
      >>> template.values
      ('Camembert',)

      Tuple ``values`` luôn có cùng độ dài với tuple ``interpolations``. Nó luôn tương đương với ``tuple(i.value for i in template.interpolations)``.

   .. rubric:: Các phương thức

   .. method:: __new__(*args: str | Interpolation)

      Mặc dù cú pháp literal là cách phổ biến nhất để tạo :class:`!Template`, bạn cũng có thể tạo trực tiếp bằng constructor:

      >>> from string.templatelib import Interpolation, Template
      >>> cheese = 'Camembert'
      >>> template = Template(
      ...     'Ah! We do have ', Interpolation(cheese, 'cheese'), '.'
      ... )
      >>> list(template)
      ['Ah! We do have ', Interpolation('Camembert', 'cheese', None, ''), '.']

      Nếu nhiều chuỗi được truyền liên tiếp, chúng sẽ được nối thành một giá trị duy nhất trong thuộc tính :attr:`~Template.strings`. Ví dụ, đoạn mã sau tạo một :class:`Template` với một chuỗi cuối cùng duy nhất:

      >>> from string.templatelib import Template
      >>> template = Template('Ah! We do have ', 'Camembert', '.')
      >>> template.strings
      ('Ah! We do have Camembert.',)

      Nếu nhiều phép nội suy được truyền liên tiếp, chúng sẽ được xử lý như các phép nội suy riêng biệt và một chuỗi rỗng sẽ được chèn vào giữa chúng. Ví dụ, đoạn mã sau tạo một template với các placeholder rỗng trong thuộc tính :attr:`~Template.strings`:

      >>> from string.templatelib import Interpolation, Template
      >>> template = Template(
      ...     Interpolation('Camembert', 'cheese'),
      ...     Interpolation('.', 'punctuation'),
      ... )
      >>> template.strings
      ('', '', '')

   .. describe:: iter(template)

      Lặp qua template, trả về từng chuỗi không rỗng và
      :class:`Interpolation` theo đúng thứ tự:

      >>> cheese = 'Camembert'
      >>> list(t'Ah! We do have {cheese}.')
      ['Ah! We do have ', Interpolation('Camembert', 'cheese', None, ''), '.']

      .. caution::

         Chuỗi rỗng **không** được đưa vào phép lặp:

         >>> response = 'We do have '
         >>> cheese = 'Camembert'
         >>> list(t'Ah! {response}{cheese}.')  # doctest: +NORMALIZE_WHITESPACE
         ['Ah! ',
          Interpolation('We do have ', 'response', None, ''),
          Interpolation('Camembert', 'cheese', None, ''),
          '.']

   .. describe:: template + other
                 template += other

      Nối template này với một template khác và trả về một đối tượng mới
      đối tượng :class:`!Template`:

      >>> cheese = 'Camembert'
      >>> list(t'Ah! ' + t'We do have {cheese}.')
      ['Ah! We do have ', Interpolation('Camembert', 'cheese', None, ''), '.']

      Việc nối một :class:`!Template` và một ``str`` **không** được hỗ trợ. Nguyên nhân là không rõ chuỗi nên được xử lý như một chuỗi tĩnh hay một phép nội suy. Nếu muốn nối một :class:`!Template` với một chuỗi, bạn nên bọc trực tiếp chuỗi trong một :class:`!Template` (để xử lý chuỗi đó như một chuỗi tĩnh) hoặc sử dụng một :class:`!Interpolation` (để xử lý chuỗi đó như động):

      >>> from string.templatelib import Interpolation, Template
      >>> template = t'Ah! '
      >>> # Xử lý 'We do have ' như một chuỗi tĩnh
      >>> template += Template('We do have ')
      >>> # Xử lý cheese như một interpolation
      >>> cheese = 'Camembert'
      >>> template += Template(Interpolation(cheese, 'cheese'))
      >>> list(template)
      ['Ah! We do have ', Interpolation('Camembert', 'cheese', None, '')]


.. class:: Interpolation

   Kiểu :class:`!Interpolation` biểu diễn một biểu thức bên trong chuỗi template. Đây là kiểu bất biến, nghĩa là không thể gán lại các thuộc tính của một interpolation.

   Interpolations hỗ trợ pattern matching, cho phép bạn so khớp với các thuộc tính của chúng bằng câu lệnh :ref:`match statement <match>`:

   >>> from string.templatelib import Interpolation
   >>> interpolation = t'{1. + 2.:.2f}'.interpolations[0]
   >>> interpolation
   Interpolation(3.0, '1. + 2.', None, '.2f')
   >>> match interpolation:
   ...     case Interpolation(value, expression, conversion, format_spec):
   ...         print(value, expression, conversion, format_spec, sep=' | ')
   ...
   3.0 | 1. + 2. | None | .2f

   Interpolations là :ref:`generic <generics>` theo kiểu của các giá trị tương ứng.

   .. rubric:: Thuộc tính

   .. attribute:: value
      :type: object

      Giá trị đã được đánh giá của interpolation.

      >>> t'{1 + 2}'.interpolations[0].value
      3

   .. attribute:: expression
      :type: str

      Đối với các interpolation được tạo bởi các t-string literal, :attr:`!expression` là văn bản biểu thức nằm bên trong dấu ngoặc nhọn (``{`` & ``}``), bao gồm mọi khoảng trắng, không bao gồm bản thân các dấu ngoặc nhọn và kết thúc trước ``!``, ``:`` hoặc ``=`` đầu tiên nếu có. Đối với các interpolation được tạo thủ công, :attr:`!expression` là chuỗi tùy ý được cung cấp khi tạo thực thể interpolation.

      Chúng tôi khuyến nghị sử dụng các biểu thức Python hợp lệ hoặc chuỗi rỗng cho trường ``expression`` của các instance :class:`!Interpolation` được tạo thủ công, mặc dù điều này không được thực thi trong runtime.

      >>> t'{1 + 2}'.interpolations[0].expression
      '1 + 2'

   .. attribute:: conversion
      :type: typing.Literal['a', 'r', 's'] | None

      Phép chuyển đổi cần áp dụng cho giá trị hoặc ``None``.

      :attr:`!conversion` là phép chuyển đổi tùy chọn cần áp dụng cho giá trị:

      >>> t'{1 + 2!a}'.interpolations[0].conversion
      'a'

      .. note::

         Không giống f-string, trong đó các phép chuyển đổi được áp dụng tự động, hành vi được mong đợi với t-string là mã *xử lý*
         :class:`!Template` sẽ quyết định cách diễn giải và có áp dụng :attr:`!conversion` hay không. Để thuận tiện, có thể sử dụng hàm :func:`convert` để mô phỏng ngữ nghĩa chuyển đổi của f-string.

   .. attribute:: format_spec
      :type: str

      Đặc tả định dạng cần áp dụng cho giá trị.

      :attr:`!format_spec` là một chuỗi tùy chọn, tùy ý được sử dụng làm đặc tả định dạng để trình bày giá trị:

      >>> t'{1 + 2:.2f}'.interpolations[0].format_spec
      '.2f'

      .. note::

         Không giống f-string, trong đó các đặc tả định dạng được tự động áp dụng thông qua giao thức :func:`format`, với t-string, hành vi được mong đợi là mã *processes* nội suy sẽ quyết định cách diễn giải và có áp dụng đặc tả định dạng hay không. Do đó, các giá trị :attr:`!format_spec` trong phép nội suy có thể là các chuỗi tùy ý, bao gồm cả những chuỗi không tuân theo giao thức :func:`format`.

   .. rubric:: Các phương thức

   .. method:: __new__(value: object, \
                       expression: str, \ conversion: typing.Literal['a', 'r', 's'] | None = None, \ format_spec: str = ''

      Tạo một đối tượng :class:`!Interpolation` mới từ các thành phần cấu thành.

      :param value: Kết quả đã được đánh giá, nằm trong phạm vi của phép nội suy.
      :param expression: Văn bản của một biểu thức Python hợp lệ hoặc một chuỗi rỗng.
      :param conversion: :ref:`conversion <formatstrings>` sẽ được sử dụng, có thể là một trong các giá trị ``None``, ``'a'``, ``'r'`` hoặc ``'s'``.
      :param format_spec: Một chuỗi tùy ý không bắt buộc được dùng làm
           :ref:`đặc tả định dạng <formatspec>` để trình bày giá trị.


Các hàm trợ giúp
----------------

.. function:: convert(obj, /, conversion)

   Áp dụng ngữ nghĩa :ref:`conversion <formatstrings-conversion>` của formatted string literal cho đối tượng đã cho *obj*. Điều này thường hữu ích cho logic xử lý template string tùy chỉnh.

   Hiện hỗ trợ ba cờ conversion:

   * ``'s'`` gọi :func:`str` trên giá trị (giống như ``!s``),
   * ``'r'`` gọi :func:`repr` (giống như ``!r``), và
   * ``'a'`` gọi :func:`ascii` (như ``!a``).

   Nếu cờ chuyển đổi là ``None``, *obj* được trả về không thay đổi.
