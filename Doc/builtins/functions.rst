.. XXX document all delegations to __special__ methods
.. _built-in-funcs:

Các hàm tích hợp sẵn
====================

Trình thông dịch Python có một số hàm và kiểu dữ liệu được tích hợp sẵn, luôn khả dụng. Chúng được liệt kê theo thứ tự bảng chữ cái ở đây.

+---------------------------------------------------------------------------------------------------+
|                                        Built-in Functions                                         |
+=========================+=======================+=======================+=========================+
| |  **A**                | |  **E**              | |  **L**              | |  **R**                |
| |  :func:`abs`          | |  :func:`enumerate`  | |  :func:`len`        | |  |func-range|_        |
| |  :func:`aiter`        | |  :func:`eval`       | |  |func-list|_       | |  :func:`repr`         |
| |  :func:`all`          | |  :func:`exec`       | |  :func:`locals`     | |  :func:`reversed`     |
| |  :func:`anext`        | |                     | |                     | |  :func:`round`        |
| |  :func:`any`          | |  **F**              | |  **M**              | |                       |
| |  :func:`ascii`        | |  :func:`filter`     | |  :func:`map`        | |  **S**                |
| |                       | |  :func:`float`      | |  :func:`max`        | |  |func-set|_          |
| |  **B**                | |  :func:`format`     | |  |func-memoryview|_ | |  :func:`setattr`      |
| |  :func:`bin`          | |  |func-frozenset|_  | |  :func:`min`        | |  :func:`slice`        |
| |  :func:`bool`         | |                     | |                     | |  :func:`sorted`       |
| |  :func:`breakpoint`   | |  **G**              | |  **N**              | |  :func:`staticmethod` |
| |  |func-bytearray|_    | |  :func:`getattr`    | |  :func:`next`       | |  |func-str|_          |
| |  |func-bytes|_        | |  :func:`globals`    | |                     | |  :func:`sum`          |
| |                       | |                     | |  **O**              | |  :func:`super`        |
| |  **C**                | |  **H**              | |  :func:`object`     | |                       |
| |  :func:`callable`     | |  :func:`hasattr`    | |  :func:`oct`        | |  **T**                |
| |  :func:`chr`          | |  :func:`hash`       | |  :func:`open`       | |  |func-tuple|_        |
| |  :func:`classmethod`  | |  :func:`help`       | |  :func:`ord`        | |  :func:`type`         |
| |  :func:`compile`      | |  :func:`hex`        | |                     | |                       |
| |  :func:`complex`      | |                     | |  **P**              | |  **V**                |
| |                       | |  **I**              | |  :func:`pow`        | |  :func:`vars`         |
| |  **D**                | |  :func:`id`         | |  :func:`print`      | |                       |
| |  :func:`delattr`      | |  :func:`input`      | |  :func:`property`   | |  **Z**                |
| |  |func-dict|_         | |  :func:`int`        | |                     | |  :func:`zip`          |
| |  :func:`dir`          | |  :func:`isinstance` | |                     | |                       |
| |  :func:`divmod`       | |  :func:`issubclass` | |                     | |  **_**                |
| |                       | |  :func:`iter`       | |                     | |  :func:`__import__`   |
+-------------------------+-----------------------+-----------------------+-------------------------+

.. using :func:`dict` would create a link to another page, so local targets are
   used, with replacement texts to make the output in the table consistent

.. |func-dict| replace:: ``dict()``
.. |func-frozenset| replace:: ``frozenset()``
.. |func-memoryview| replace:: ``memoryview()``
.. |func-set| replace:: ``set()``
.. |func-list| replace:: ``list()``
.. |func-str| replace:: ``str()``
.. |func-tuple| replace:: ``tuple()``
.. |func-range| replace:: ``range()``
.. |func-bytearray| replace:: ``bytearray()``
.. |func-bytes| replace:: ``bytes()``

.. function:: abs(number, /)

   Trả về giá trị tuyệt đối của một số. Đối số có thể là một số nguyên, số dấu phẩy động hoặc một đối tượng triển khai
   :meth:`~object.__abs__`. Nếu đối số là một số phức, độ lớn của nó sẽ được trả về.


.. function:: aiter(async_iterable, /)

   Trả về một :term:`asynchronous iterator` cho một :term:`asynchronous iterable`. Tương đương với việc gọi ``x.__aiter__()``.

   Lưu ý: Không giống như :func:`iter`, :func:`aiter` không có biến thể nhận 2 đối số.

   .. versionadded:: 3.10

.. function:: all(iterable, /)

   Trả về ``True`` nếu tất cả các phần tử của *iterable* đều đúng (hoặc nếu iterable rỗng). Tương đương với::

      def all(iterable):
          for element in iterable:
              if not element:
                  return False
          return True


.. awaitablefunction:: anext(async_iterator, /)
                       anext(async_iterator, default, /)

   Khi được await, trả về mục tiếp theo từ :term:`asynchronous iterator` đã cho, hoặc *default* nếu được cung cấp và iterator đã :term:`exhausted`.

   Đây là biến thể async của hàm dựng sẵn :func:`next`, và hoạt động tương tự.

   Lệnh này gọi phương thức :meth:`~object.__anext__` của *async_iterator*, trả về một :term:`awaitable`. Việc await giá trị này sẽ trả về giá trị tiếp theo của iterator. Nếu *default* được cung cấp, giá trị đó sẽ được trả về khi iterator đã cạn; nếu không, :exc:`StopAsyncIteration` sẽ được phát sinh.

   .. versionadded:: 3.10

.. function:: any(iterable, /)

   Trả về ``True`` nếu bất kỳ phần tử nào của *iterable* là true. Nếu iterable rỗng, trả về ``False``. Tương đương với::

      def any(iterable):
          for element in iterable:
              if element:
                  return True
          return False


.. function:: ascii(object, /)

   Giống như :func:`repr`, trả về một chuỗi chứa biểu diễn có thể in được của một đối tượng, nhưng escape các ký tự không phải ASCII trong chuỗi được trả về bởi
   :func:`repr` bằng các escape ``\x``, ``\u`` hoặc ``\U``. Lệnh này tạo ra một chuỗi tương tự chuỗi được trả về bởi :func:`repr` trong Python 2.


.. function:: bin(integer, /)

   Chuyển đổi một số nguyên thành chuỗi nhị phân có tiền tố "0b". Kết quả là một biểu thức Python hợp lệ. Nếu *số nguyên* không phải là một :class:`int` đối tượng Python, đối tượng đó phải định nghĩa một :meth:`~object.__index__` phương thức trả về một số nguyên. Một số ví dụ:

      >>> bin(3)
      '0b11'
      >>> bin(-10)
      '-0b1010'

   Cho dù có muốn tiền tố "0b" hay không, bạn có thể sử dụng một trong các cách sau.

      >>> format(14, '#b'), format(14, 'b')
      ('0b1110', '1110')
      >>> f'{14:#b}', f'{14:b}'
      ('0b1110', '1110')

   Xem thêm :func:`enum.bin` để biểu diễn các giá trị âm dưới dạng bù hai.

   Xem thêm :func:`format` để biết thêm thông tin.


.. class:: bool(object=False, /)

   Trả về một giá trị Boolean, tức là một trong ``True`` hoặc ``False``. Đối số được chuyển đổi bằng cách sử dụng :ref:`truth testing procedure <truth>` tiêu chuẩn. Nếu đối số là false hoặc bị bỏ qua, hàm này trả về ``False``; nếu không, hàm trả về ``True``.  The
   Lớp :class:`bool` là lớp con của :class:`int` (xem :ref:`typesnumeric`). Không thể tạo lớp con của lớp này thêm nữa. Các thể hiện duy nhất của lớp là ``False`` và ``True`` (xem :ref:`typebool`).

   .. index:: pair: Boolean; type

   .. versionchanged:: 3.7
      Tham số này hiện chỉ có thể được truyền theo vị trí.

.. function:: breakpoint(*args, **kws)

   Hàm này đưa bạn vào trình debugger tại vị trí gọi. Cụ thể, hàm này gọi :func:`sys.breakpointhook`, truyền thẳng ``args`` và ``kws``. Theo mặc định, ``sys.breakpointhook()`` gọi
   :func:`pdb.set_trace` mà không yêu cầu đối số nào. Trong trường hợp này, đây chỉ là một hàm tiện ích để bạn không phải tự import :func:`pdb.set_trace` một cách rõ ràng
   :mod:`pdb` hoặc nhập đủ mã để vào trình gỡ lỗi. Tuy nhiên,
   :func:`sys.breakpointhook` có thể được đặt thành một hàm khác và
   :func:`breakpoint` sẽ tự động gọi hàm đó, cho phép bạn vào trình debugger mà mình muốn. Nếu :func:`sys.breakpointhook` không thể truy cập được, hàm này sẽ phát sinh :exc:`RuntimeError`.

   Theo mặc định, hành vi của :func:`breakpoint` có thể được thay đổi bằng biến môi trường :envvar:`PYTHONBREAKPOINT`. Xem :func:`sys.breakpointhook` để biết chi tiết sử dụng.

   Lưu ý rằng điều này không được đảm bảo nếu :func:`sys.breakpointhook` đã bị thay thế.

   .. audit-event:: builtins.breakpoint breakpointhook breakpoint

   .. versionadded:: 3.7

.. _func-bytearray:
.. class:: bytearray(source=b'')
           bytearray(source, encoding, errors='strict')
   :noindex:

   Trả về một mảng byte mới. Lớp :class:`bytearray` là một sequence có thể thay đổi gồm các số nguyên trong phạm vi 0 <= x < 256. Lớp này có hầu hết các phương thức thông thường của sequence có thể thay đổi, được mô tả trong :ref:`typesseq-mutable`, cũng như hầu hết các phương thức của kiểu :class:`bytes`; xem :ref:`bytes-methods`.

   Tham số *source* tùy chọn có thể được dùng để khởi tạo mảng theo một vài cách khác nhau:

   * Nếu đó là một *string*, bạn cũng phải cung cấp tham số *encoding* (và tùy chọn *errors*); :func:`bytearray` sau đó chuyển đổi string thành byte bằng cách sử dụng :meth:`str.encode`.

   * Nếu đó là một *integer*, mảng sẽ có kích thước đó và được khởi tạo bằng các byte null.

   * Nếu đó là một đối tượng tuân theo :ref:`buffer interface <bufferobjects>`, một buffer chỉ đọc của đối tượng sẽ được dùng để khởi tạo mảng byte.

   * Nếu đó là một *iterable*, nó phải là một iterable gồm các số nguyên trong phạm vi ``0 <= x < 256``, được dùng làm nội dung ban đầu của mảng.

   Nếu không có đối số, một mảng có kích thước 0 sẽ được tạo.

   Xem thêm :ref:`binaryseq` và :ref:`typebytearray`.


.. _func-bytes:
.. class:: bytes(source=b'')
           bytes(source, encoding, errors='strict')
   :noindex:

   Trả về một đối tượng "bytes" mới, là một chuỗi bất biến gồm các số nguyên trong phạm vi ``0 <= x < 256``.  :class:`bytes` là phiên bản bất biến của
   :class:`bytearray` -- nó có các phương thức không biến đổi giống nhau, cũng như cách lập chỉ mục và cắt lát giống nhau.

   Theo đó, các đối số của hàm khởi tạo được diễn giải như đối với :func:`bytearray`.

   Các đối tượng bytes cũng có thể được tạo bằng các literal, xem :ref:`strings`.

   Xem thêm :ref:`binaryseq`, :ref:`typebytes` và :ref:`bytes-methods`.


.. function:: callable(object, /)

   Trả về :const:`True` nếu đối số *object* có vẻ có thể gọi được,
   :const:`False` nếu không. Nếu kết quả này là ``True``, một lần gọi vẫn có thể thất bại, nhưng nếu là ``False``, việc gọi *object* sẽ không bao giờ thành công. Lưu ý rằng các class có thể gọi được (việc gọi một class sẽ trả về một instance mới); các instance có thể gọi được nếu class của chúng có method :meth:`~object.__call__`.

   .. versionadded:: 3.2
      Hàm này đầu tiên bị loại bỏ trong Python 3.0, sau đó được đưa trở lại trong Python 3.2.


.. function:: chr(codepoint, /)

   Trả về chuỗi biểu diễn một ký tự có code point Unicode được chỉ định. Ví dụ: ``chr(97)`` trả về chuỗi ``'a'``, trong khi ``chr(8364)`` trả về chuỗi ``'€'``. Đây là phép đảo ngược của :func:`ord`.

   Phạm vi hợp lệ của đối số là từ 0 đến 1.114.111 (0x10FFFF trong hệ cơ số 16). :exc:`ValueError` sẽ được phát sinh nếu đối số nằm ngoài phạm vi đó.


.. decorator:: classmethod

   Chuyển một method thành class method.

   Một class method nhận class làm đối số đầu tiên ngầm định, giống như một instance method nhận instance. Để khai báo một class method, hãy sử dụng thành ngữ này::

      class C:
          @classmethod
          def f(cls, arg1, arg2): ...

   Dạng ``@classmethod`` là một hàm :term:`decorator` -- xem
   :ref:`function` để biết chi tiết.

   Một class method có thể được gọi trên class (chẳng hạn như ``C.f()``) hoặc trên một instance (chẳng hạn như ``C().f()``). Instance bị bỏ qua, ngoại trừ class của nó. Nếu một class method được gọi cho một derived class, đối tượng derived class sẽ được truyền làm đối số đầu tiên ngầm định.

   Class method khác với static method trong C++ hoặc Java. Nếu bạn muốn các phương thức đó, hãy xem :func:`staticmethod` trong phần này. Để biết thêm thông tin về class method, hãy xem :ref:`types`.

   .. versionchanged:: 3.9
      Class method hiện có thể bao bọc các :term:`descriptor <descriptor>` khác, chẳng hạn như
      :func:`property`.

   .. versionchanged:: 3.10
      Class method hiện kế thừa các thuộc tính của method (:attr:`~function.__module__`, :attr:`~function.__name__`,
      :attr:`~function.__qualname__`, :attr:`~function.__doc__` và
      :attr:`~function.__annotations__`) và có một thuộc tính ``__wrapped__`` mới.

   .. deprecated-removed:: 3.11 3.13
      Các phương thức lớp không còn có thể bao bọc các :term:`descriptors <descriptor>` khác như
      :func:`property`.


.. function:: compile(source, filename, mode, flags=0, dont_inherit=False, optimize=-1)

   Biên dịch *source* thành một đối tượng code hoặc AST. Các đối tượng code có thể được thực thi bởi :func:`exec` hoặc :func:`eval`. *source* có thể là một chuỗi thông thường, một chuỗi byte hoặc một đối tượng AST. Hãy tham khảo tài liệu về module :mod:`ast` để biết cách làm việc với các đối tượng AST.

   Đối số *filename* phải chỉ ra tệp mà từ đó code được đọc; hãy truyền một giá trị dễ nhận biết nếu code không được đọc từ tệp (``'<string>'`` thường được sử dụng).

   Đối số *mode* chỉ định loại code cần được biên dịch; giá trị này có thể là ``'exec'`` nếu *source* gồm một chuỗi câu lệnh, ``'eval'`` nếu gồm một biểu thức duy nhất hoặc ``'single'`` nếu gồm một câu lệnh tương tác duy nhất (trong trường hợp sau, các câu lệnh biểu thức đánh giá thành giá trị khác ``None`` sẽ được in ra).

   Các đối số tùy chọn *flags* và *dont_inherit* kiểm soát những
   :ref:`các tùy chọn trình biên dịch <ast-compiler-flags>` nào sẽ được kích hoạt và :ref:`các tính năng tương lai <future>` nào sẽ được cho phép. Nếu không có tùy chọn nào (hoặc cả hai đều bằng 0), mã sẽ được biên dịch với cùng các cờ ảnh hưởng đến mã đang gọi :func:`compile`. Nếu đối số *flags* được cung cấp và *dont_inherit* không được cung cấp (hoặc bằng 0), các tùy chọn trình biên dịch và các câu lệnh future được chỉ định bởi đối số *flags* sẽ được sử dụng cùng với những tùy chọn vốn được sử dụng. Nếu *dont_inherit* là một số nguyên khác 0, thì đối số *flags* là toàn bộ các cờ đó -- các cờ (tính năng future và tùy chọn trình biên dịch) trong mã bao quanh sẽ bị bỏ qua.

   Các tùy chọn trình biên dịch và câu lệnh future được chỉ định bằng các bit có thể được OR theo từng bit để chỉ định nhiều tùy chọn. Bitfield cần thiết để chỉ định một tính năng future cụ thể có thể được tìm thấy dưới dạng
   :attr:`~__future__._Feature.compiler_flag` thuộc tính trên
   :class:`~__future__._Feature` instance trong module :mod:`__future__`.
   :ref:`Các cờ trình biên dịch <ast-compiler-flags>` có thể được tìm thấy trong module :mod:`ast`, với tiền tố ``PyCF_``.

   Đối số *optimize* chỉ định cấp độ tối ưu hóa của trình biên dịch; giá trị mặc định ``-1`` chọn cấp độ tối ưu hóa của trình thông dịch như được chỉ định bởi các tùy chọn :option:`-O`. Các cấp độ tường minh là ``0`` (không tối ưu hóa; ``__debug__`` là true), ``1`` (các câu lệnh assert bị loại bỏ, ``__debug__`` là false) hoặc ``2`` (docstring cũng bị loại bỏ).

   Hàm này phát sinh :exc:`SyntaxError` nếu mã nguồn đã biên dịch không hợp lệ, bao gồm *mã nguồn* chứa ký tự null hoặc không thể được giải mã;
   :exc:`ValueError` nếu *mode* hoặc *flags* không hợp lệ, hoặc nếu một chuỗi *source* chứa các ký tự surrogate;
   :exc:`MemoryError` hoặc :exc:`RecursionError` nếu *source* quá phức tạp để phân tích cú pháp hoặc biên dịch, chẳng hạn như một biểu thức có hàng nghìn toán tử lồng nhau; và :exc:`OverflowError` nếu *source* quá lớn.

   Nếu bạn muốn phân tích mã Python thành biểu diễn AST, hãy xem
   :func:`ast.parse`.

   .. audit-event:: compile source,filename compile

      Phát ra một :ref:`auditing event <auditing>` ``compile`` với các đối số ``source`` và ``filename``. Sự kiện này cũng có thể được phát ra bởi quá trình biên dịch ngầm.

   .. note::

      Khi biên dịch một chuỗi chứa mã nhiều dòng ở chế độ ``'single'`` hoặc ``'eval'``, dữ liệu đầu vào phải được kết thúc bằng ít nhất một ký tự xuống dòng. Điều này nhằm hỗ trợ việc phát hiện các câu lệnh chưa hoàn chỉnh và hoàn chỉnh trong mô-đun :mod:`code`.

   .. warning::

      Có thể làm trình thông dịch Python bị crash bằng một chuỗi đủ lớn/phức tạp khi biên dịch thành đối tượng AST, do các giới hạn về độ sâu ngăn xếp trong trình biên dịch AST của Python.

   .. versionchanged:: 3.2
      Cho phép sử dụng ký tự xuống dòng của Windows và Mac. Ngoài ra, dữ liệu đầu vào ở chế độ ``'exec'`` không còn phải kết thúc bằng ký tự xuống dòng. Đã thêm tham số *optimize*.

   .. versionchanged:: 3.5
      Trước đây, :exc:`TypeError` được phát sinh khi gặp các byte null trong *source*.

   .. versionchanged:: 3.8
      Giờ đây, có thể truyền ``ast.PyCF_ALLOW_TOP_LEVEL_AWAIT`` trong các cờ để bật hỗ trợ cho ``await``, ``async for`` và ``async with`` ở cấp cao nhất.

   .. versionchanged:: 3.12
      :exc:`SyntaxError` is raised instead of :exc:`ValueError` when null bytes
      được gặp trong *source*.


.. class:: complex(number=0, /)
           complex(string, /) complex(real=0, imag=0)

   Chuyển đổi một chuỗi hoặc số đơn lẻ thành số phức, hoặc tạo một số phức từ phần thực và phần ảo.

   Ví dụ:

   .. doctest::

      >>> complex('+1.23')
      (1.23+0j)
      >>> complex('-4.5j')
      -4.5j
      >>> complex('-1.23+4.5j')
      (-1.23+4.5j)
      >>> complex('\t( -1.23+4.5J )\n')
      (-1.23+4.5j)
      >>> complex('-Infinity+NaNj')
      (-inf+nanj)
      >>> complex(1.23)
      (1.23+0j)
      >>> complex(imag=-4.5)
      -4.5j
      >>> complex(-1.23, 4.5)
      (-1.23+4.5j)

   Nếu đối số là một chuỗi, chuỗi đó phải chứa либо một phần thực (theo cùng định dạng như :func:`float`) hoặc một phần ảo (theo cùng định dạng nhưng có hậu tố ``'j'`` hoặc ``'J'``), hoặc cả phần thực và phần ảo (trong trường hợp này, bắt buộc phải có dấu của phần ảo). Chuỗi có thể tùy chọn được bao quanh bởi khoảng trắng và cặp dấu ngoặc tròn ``'('`` và ``')'``, những ký tự này sẽ bị bỏ qua. Chuỗi không được chứa khoảng trắng giữa ``'+'``, ``'-'``, hậu tố ``'j'`` hoặc ``'J'`` và số thập phân. Ví dụ, ``complex('1+2j')`` là hợp lệ, nhưng ``complex('1 + 2j')`` sẽ phát sinh
   :exc:`ValueError`. Cụ thể hơn, đầu vào phải tuân theo quy tắc sản xuất :token:`~float:complexvalue` trong văn phạm sau, sau khi đã loại bỏ dấu ngoặc và các ký tự khoảng trắng ở đầu cũng như cuối:

   .. productionlist:: float
      complexvalue: `floatvalue` |
                  : `floatvalue` ("j" | "J") |
                  : `floatvalue` `sign` `absfloatvalue` ("j" | "J")

   Nếu đối số là một số, hàm khởi tạo đóng vai trò như một phép chuyển đổi số giống như :class:`int` và :class:`float`. Với một đối tượng Python bất kỳ ``x``, ``complex(x)`` ủy quyền cho ``x.__complex__()``. Nếu :meth:`~object.__complex__` chưa được định nghĩa thì hàm sẽ chuyển sang :meth:`~object.__float__`. Nếu :meth:`!__float__` chưa được định nghĩa thì hàm sẽ chuyển sang :meth:`~object.__index__`.

   Nếu cung cấp hai đối số hoặc sử dụng các đối số từ khóa, mỗi đối số có thể thuộc bất kỳ kiểu số nào (bao gồm cả số phức). Nếu cả hai đối số là số thực, trả về một số phức với phần thực là *real* và phần ảo là *imag*. Nếu cả hai đối số là số phức, trả về một số phức với phần thực là ``real.real-imag.imag`` và phần ảo là ``real.imag+imag.real``. Nếu một trong các đối số là số thực, chỉ phần thực của đối số đó được sử dụng trong các biểu thức trên.

   Xem thêm :meth:`complex.from_number`, hàm này chỉ chấp nhận một đối số số duy nhất.

   Nếu bỏ qua tất cả các đối số, hàm trả về ``0j``.

   Kiểu complex được mô tả trong :ref:`typesnumeric`.

   .. versionchanged:: 3.6
      Cho phép nhóm các chữ số bằng dấu gạch dưới như trong các literal mã.

   .. versionchanged:: 3.8
      Nếu :meth:`~object.__complex__` và :meth:`~object.__index__` không được định nghĩa thì sử dụng :meth:`~object.__index__` làm giá trị dự phòng.
      :meth:`~object.__float__` không được định nghĩa.

   .. deprecated:: 3.14
      Việc truyền một số phức làm đối số *real* hoặc *imag* hiện đã không còn được khuyến nghị; số phức chỉ nên được truyền dưới dạng một đối số vị trí duy nhất.


.. function:: delattr(object, name, /)

   Đây là một hàm tương tự :func:`setattr`. Các đối số là một object và một string. String phải là tên của một thuộc tính của object. Hàm này xóa thuộc tính có tên đó, miễn là object cho phép. Ví dụ, ``delattr(x, 'foobar')`` tương đương với ``del x.foobar``. *name* không nhất thiết phải là một Python identifier (xem :func:`setattr`).


.. _func-dict:
.. class:: dict(**kwargs)
           dict(mapping, /, ****kwargs) dict(iterable, /, ****kwargs)
   :noindex:

   Tạo một dictionary mới. Đối tượng :class:`dict` là class dictionary. Xem thêm :ref:`typesmapping` để biết tài liệu về class này.

   Để biết các container khác, hãy xem các built-in :class:`list`, :class:`set`, và
   các lớp :class:`tuple`, cũng như mô-đun :mod:`collections`.


.. function:: dir()
              dir(object, /)

   Nếu không có đối số, trả về danh sách các tên trong phạm vi cục bộ hiện tại. Với một đối số, cố gắng trả về danh sách các thuộc tính hợp lệ của đối tượng đó.

   Nếu đối tượng có một phương thức có tên :meth:`~object.__dir__`, phương thức này sẽ được gọi và phải trả về danh sách các thuộc tính. Điều này cho phép các đối tượng triển khai một
   hàm :func:`~object.__getattr__` hoặc :func:`~object.__getattribute__` tùy chỉnh cách
   :func:`dir` báo cáo các thuộc tính của chúng.

   Nếu đối tượng không cung cấp :meth:`~object.__dir__`, hàm sẽ cố gắng hết sức để thu thập thông tin từ
   thuộc tính :attr:`~object.__dict__`, nếu được định nghĩa, và từ đối tượng kiểu của nó. Danh sách kết quả không nhất thiết đầy đủ và có thể không chính xác khi đối tượng có :func:`~object.__getattr__` tùy chỉnh.

   Cơ chế :func:`dir` mặc định hoạt động khác nhau với từng loại đối tượng, vì nó cố gắng tạo ra thông tin phù hợp nhất thay vì đầy đủ:

   * Nếu đối tượng là một đối tượng module, danh sách chứa tên các thuộc tính của module.

   * Nếu đối tượng là một đối tượng kiểu hoặc lớp, danh sách chứa tên các thuộc tính của nó, cũng như đệ quy các thuộc tính của các lớp cơ sở của nó.

   * Nếu không, danh sách chứa tên các thuộc tính của đối tượng, tên các thuộc tính của lớp của đối tượng và đệ quy các thuộc tính của các lớp cơ sở của lớp đó.

   Danh sách kết quả được sắp xếp theo thứ tự bảng chữ cái. Ví dụ:

      >>> import struct
      >>> dir()   # hiển thị tên trong namespace của module  # doctest: +SKIP
      ['__builtins__', '__name__', 'struct']
      >>> dir(struct)   # hiển thị tên trong mô-đun struct # doctest: +SKIP
      ['Struct', '__all__', '__builtins__', '__cached__', '__doc__', '__file__',
       '__initializing__', '__loader__', '__name__', '__package__',
       '_clearcache', 'calcsize', 'error', 'pack', 'pack_into',
       'unpack', 'unpack_from']
      >>> class Shape:
      ...     def __dir__(self):
      ...         return ['area', 'perimeter', 'location']
      ...
      >>> s = Shape()
      >>> dir(s)
      ['area', 'location', 'perimeter']

   .. note::

      Vì :func:`dir` chủ yếu được cung cấp để thuận tiện khi sử dụng tại dấu nhắc tương tác, nó ưu tiên cung cấp một tập hợp tên thú vị hơn là một tập hợp tên được định nghĩa chặt chẽ hoặc nhất quán, và hành vi chi tiết của nó có thể thay đổi giữa các bản phát hành. Ví dụ: các thuộc tính của metaclass không có trong danh sách kết quả khi đối số là một lớp.


.. function:: divmod(a, b, /)

   Nhận hai số (không phải số phức) làm đối số và trả về một cặp số gồm thương và phần dư của chúng khi thực hiện phép chia số nguyên. Với các kiểu toán hạng hỗn hợp, các quy tắc dành cho toán tử số học nhị phân được áp dụng. Đối với số nguyên, kết quả giống với ``(a // b, a % b)``. Đối với số dấu phẩy động, kết quả là ``(q, a % b)``, trong đó *q* thường là ``math.floor(a / b)`` nhưng có thể nhỏ hơn giá trị đó 1 đơn vị. Trong mọi trường hợp, ``q * b + a % b`` rất gần với *a*, nếu ``a % b`` khác không thì nó có cùng dấu với *b*, và ``0 <= abs(a % b) < abs(b)``.


.. function:: enumerate(iterable, start=0)

   Trả về một đối tượng enumerate. *iterable* phải là một chuỗi, một
   :term:`iterator`, hoặc một đối tượng khác hỗ trợ phép lặp. Phương thức :meth:`~iterator.__next__` của iterator được trả về bởi
   :func:`enumerate` trả về một tuple chứa một bộ đếm (bắt đầu từ *start*, mặc định là 0) và các giá trị nhận được khi lặp qua *iterable*.

      >>> seasons = ['Spring', 'Summer', 'Fall', 'Winter']
      >>> list(enumerate(seasons))
      [(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]
      >>> list(enumerate(seasons, start=1))
      [(1, 'Spring'), (2, 'Summer'), (3, 'Fall'), (4, 'Winter')]

   Tương đương với::

      def enumerate(iterable, start=0):
          n = start
          for elem in iterable:
              yield n, elem
              n += 1

.. _func-eval:

.. function:: eval(source, /, globals=None, locals=None)

   :param source:Một biểu thức Python.
   :type source: :class:`str` | :ref:`code object <code-objects>`

   :param globals:Namespace toàn cục (mặc định: ``None``).
   :type globals: :class:`dict` | ``None``

   :param locals:Namespace cục bộ (mặc định: ``None``).
   :type locals: :term:`mapping` | ``None``

   :returns: Kết quả của biểu thức đã được đánh giá.
   :raises: Các lỗi cú pháp được báo cáo dưới dạng ngoại lệ.

   .. warning::

      Hàm này thực thi mã tùy ý. Việc gọi hàm với dữ liệu đầu vào do người dùng không đáng tin cậy cung cấp sẽ dẫn đến các lỗ hổng bảo mật.

   Đối số *source* được phân tích cú pháp và đánh giá như một biểu thức Python (nói chính xác hơn là một :ref:`expression list <exprlists>`) bằng cách sử dụng các ánh xạ *globals* và *locals* làm không gian tên toàn cục và cục bộ. Nếu từ điển *globals* hiện diện và không chứa giá trị cho khóa ``__builtins__``, một tham chiếu đến từ điển của mô-đun tích hợp sẵn :mod:`builtins` sẽ được chèn vào khóa đó trước khi *source* được phân tích cú pháp. Có thể ghi đè ``__builtins__`` để giới hạn hoặc thay đổi các tên khả dụng, nhưng đây **not** phải là cơ chế bảo mật: mã được thực thi vẫn có thể truy cập tất cả các đối tượng tích hợp sẵn. Nếu bỏ qua ánh xạ *locals*, ánh xạ này mặc định là từ điển *globals*. Nếu bỏ qua cả hai ánh xạ, mã nguồn sẽ được thực thi với *globals* và *locals* trong môi trường nơi
   :func:`eval` được gọi. Lưu ý, *eval()* sẽ chỉ có quyền truy cập vào
   :term:`nested scopes <nested scope>` (không phải biến cục bộ) trong môi trường bao quanh nếu chúng đã được tham chiếu trong phạm vi đang gọi
   :func:`eval` (ví dụ: thông qua một :keyword:`nonlocal` statement).

   Ví dụ:

      >>> x = 1
      >>> eval('x+1')
      2

      >>> eval("1, 2")
      (1, 2)

   Hàm này cũng có thể được dùng để thực thi các đối tượng mã tùy ý (chẳng hạn như những đối tượng được tạo bởi :func:`compile`). Trong trường hợp này, hãy truyền một đối tượng mã thay vì một chuỗi. Nếu đối tượng mã đã được biên dịch với ``'exec'`` làm đối số *mode*, giá trị trả về của :func:`eval`\'s sẽ là ``None``.

   Gợi ý: việc thực thi động các câu lệnh được hỗ trợ bởi hàm :func:`exec`. Các hàm :func:`globals` và :func:`locals` lần lượt trả về từ điển toàn cục và cục bộ hiện tại, có thể hữu ích khi truyền chúng để :func:`eval` hoặc :func:`exec` sử dụng.

   Nếu mã nguồn đã cho là một chuỗi, các dấu cách và tab ở đầu và cuối sẽ bị loại bỏ.

   Xem :func:`ast.literal_eval` để biết hàm đánh giá các chuỗi có biểu thức chỉ chứa các literal.

   .. audit-event:: exec code_object eval

      Phát sinh một :ref:`auditing event <auditing>` ``exec`` với đối tượng mã làm đối số. Các sự kiện biên dịch mã cũng có thể được phát sinh.

   .. versionchanged:: 3.13

      Các đối số *globals* và *locals* hiện có thể được truyền dưới dạng từ khóa.

   .. versionchanged:: 3.13

      Ngữ nghĩa của namespace *locals* mặc định đã được điều chỉnh như mô tả đối với builtin :func:`locals`.

.. index:: pair: built-in function; exec

.. function:: exec(source, /, globals=None, locals=None, *, closure=None)

   .. warning::

      Hàm này thực thi mã tùy ý. Việc gọi hàm với dữ liệu đầu vào do người dùng không đáng tin cậy cung cấp sẽ dẫn đến các lỗ hổng bảo mật.

   Hàm này hỗ trợ thực thi động mã Python. *source* phải là một chuỗi hoặc một đối tượng mã. Nếu là một chuỗi, chuỗi đó sẽ được phân tích cú pháp thành một suite gồm các câu lệnh Python rồi được thực thi (trừ khi xảy ra lỗi cú pháp). [#]_ Nếu là một đối tượng mã, đối tượng đó פשוט được thực thi. Trong mọi trường hợp, mã được thực thi được kỳ vọng là hợp lệ khi làm đầu vào tệp (xem phần :ref:`file-input` trong Reference Manual). Lưu ý rằng
   Các câu lệnh :keyword:`nonlocal`, :keyword:`yield` và :keyword:`return` không được sử dụng bên ngoài phần định nghĩa hàm, ngay cả trong ngữ cảnh của mã được truyền cho
   hàm :func:`exec`. Giá trị trả về là ``None``.

   Trong mọi trường hợp, nếu các phần tùy chọn bị bỏ qua, mã sẽ được thực thi trong scope hiện tại. Nếu chỉ cung cấp *globals*, nó phải là một dictionary (không phải lớp con của dictionary) và sẽ được dùng cho cả biến toàn cục lẫn biến cục bộ. Nếu cung cấp *globals* và *locals*, chúng lần lượt được dùng cho biến toàn cục và biến cục bộ. Nếu được cung cấp, *locals* có thể là bất kỳ đối tượng mapping nào. Hãy nhớ rằng ở cấp module, globals và locals là cùng một dictionary.

   .. note::

      Khi ``exec`` nhận hai đối tượng riêng biệt làm *globals* và *locals*, mã sẽ được thực thi như thể được nhúng trong phần định nghĩa lớp. Điều này có nghĩa là các hàm và lớp được định nghĩa trong mã đã thực thi sẽ không thể truy cập các biến được gán ở cấp cao nhất (vì các biến "cấp cao nhất" được xem là biến lớp trong phần định nghĩa lớp).

   Nếu dictionary *globals* không chứa giá trị cho khóa ``__builtins__``, một tham chiếu đến dictionary của module built-in
   :mod:`builtins` sẽ được chèn vào khóa đó. Việc ghi đè ``__builtins__`` có thể được dùng để hạn chế hoặc thay đổi các tên khả dụng, nhưng điều này **not** phải là một cơ chế bảo mật: mã được thực thi vẫn có thể truy cập tất cả builtins.

   Đối số *closure* chỉ định một closure—một tuple gồm các cellvar. Đối số này chỉ hợp lệ khi *object* là một code object chứa
   :term:`các biến tự do (closure) <closure variable>`. Độ dài của tuple phải khớp chính xác với độ dài của đối tượng mã
   :attr:`~codeobject.co_freevars` thuộc tính.

   .. audit-event:: exec code_object exec

      Phát sinh một :ref:`auditing event <auditing>` ``exec`` với đối tượng mã làm đối số. Các sự kiện biên dịch mã cũng có thể được phát sinh.

   .. note::

      Các hàm tích hợp :func:`globals` và :func:`locals` lần lượt trả về namespace global và local hiện tại, có thể hữu ích khi truyền chúng để sử dụng làm đối số thứ hai và thứ ba cho :func:`exec`.

   .. note::

      *locals* mặc định hoạt động như được mô tả cho hàm :func:`locals` bên dưới. Hãy truyền một từ điển *locals* tường minh nếu bạn cần thấy tác động của mã lên *locals* sau khi hàm :func:`exec` trả về.

   .. versionchanged:: 3.11
      Đã thêm tham số *closure*.

   .. versionchanged:: 3.13

      Các đối số *globals* và *locals* hiện có thể được truyền dưới dạng từ khóa.

   .. versionchanged:: 3.13

      Ngữ nghĩa của namespace *locals* mặc định đã được điều chỉnh như mô tả đối với builtin :func:`locals`.


.. function:: filter(function, iterable, /)

   Tạo một iterator từ những phần tử của *iterable* mà *function* trả về true. *iterable* có thể là một sequence, một container hỗ trợ iteration hoặc một iterator. Nếu *function* là ``None``, hàm identity sẽ được giả định, nghĩa là tất cả phần tử của *iterable* có giá trị false sẽ bị loại bỏ.

   Lưu ý rằng ``filter(function, iterable)`` tương đương với biểu thức generator ``(item for item in iterable if function(item))`` nếu function không phải là ``None``, và ``(item for item in iterable if item)`` nếu function là ``None``.

   Xem :func:`itertools.filterfalse` để biết hàm bổ sung trả về những phần tử của *iterable* mà *function* trả về false.


.. class:: float(number=0.0, /)
           float(string, /)

   .. index::
      single: NaN
      single: Infinity

   Trả về một số dấu phẩy động được tạo từ một số hoặc một chuỗi.

   Ví dụ:

   .. doctest::

      >>> float('+1.23')
      1.23
      >>> float('   -12345\n')
      -12345.0
      >>> float('1e-003')
      0.001
      >>> float('+1E6')
      1000000.0
      >>> float('-Infinity')
      -inf

   Nếu đối số là một chuỗi, chuỗi đó phải chứa một số thập phân, có thể có dấu ở trước và có thể được đặt giữa các khoảng trắng. Dấu tùy chọn có thể là ``'+'`` hoặc ``'-'``; dấu ``'+'`` không ảnh hưởng đến giá trị được tạo ra. Đối số cũng có thể là một chuỗi biểu diễn NaN (không phải là số), hoặc vô cực dương hay âm. Cụ thể hơn, sau khi loại bỏ các ký tự khoảng trắng ở đầu và cuối, đầu vào phải tuân theo quy tắc sản xuất :token:`~float:floatvalue` trong ngữ pháp sau:

   .. productionlist:: float
      sign: "+" | "-"
      infinity: "Infinity" | "inf"
      nan: "nan"
      digit: <a Unicode decimal digit, i.e. characters in Unicode general category Nd>
      digitpart: `digit` (["_"] `digit`)*
      number: [`digitpart`] "." `digitpart` | `digitpart` ["."]
      exponent: ("e" | "E") [`sign`] `digitpart`
      floatnumber: `number` [`exponent`]
      absfloatvalue: `floatnumber` | `infinity` | `nan`
      floatvalue: [`sign`] `absfloatvalue`

   Phân biệt chữ hoa chữ thường không quan trọng, vì vậy chẳng hạn như "inf", "Inf", "INFINITY" và "iNfINity" đều là các cách viết hợp lệ của vô cực dương.

   Nếu không, nếu đối số là một số nguyên hoặc số dấu phẩy động, một số dấu phẩy động có cùng giá trị (trong phạm vi độ chính xác số dấu phẩy động của Python) sẽ được trả về. Nếu đối số nằm ngoài phạm vi của một số float trong Python, :exc:`OverflowError` sẽ được phát sinh.

   Đối với một đối tượng Python tổng quát ``x``, ``float(x)`` ủy quyền cho ``x.__float__()``. Nếu :meth:`~object.__float__` không được định nghĩa, nó sẽ chuyển sang :meth:`~object.__index__`.

   Xem thêm :meth:`float.from_number`, vốn chỉ chấp nhận một đối số số.

   Nếu không cung cấp đối số nào, ``0.0`` sẽ được trả về.

   Kiểu float được mô tả trong :ref:`typesnumeric`.

   .. versionchanged:: 3.6
      Cho phép nhóm các chữ số bằng dấu gạch dưới như trong các literal mã.

   .. versionchanged:: 3.7
      Tham số này hiện chỉ có thể được truyền theo vị trí.

   .. versionchanged:: 3.8
      Sử dụng :meth:`~object.__index__` nếu :meth:`~object.__float__` chưa được định nghĩa.


.. index::
   single: __format__
   single: string; format() (built-in function)

.. function:: format(value, format_spec="", /)

   Chuyển đổi một *value* thành dạng biểu diễn "được định dạng", theo quy định của *format_spec*. Cách diễn giải *format_spec* sẽ phụ thuộc vào kiểu của đối số *value*; tuy nhiên, hầu hết các kiểu dựng sẵn đều sử dụng một cú pháp định dạng tiêu chuẩn: :ref:`formatspec`.

   *format_spec* mặc định là một chuỗi rỗng, thường cho kết quả giống như khi gọi :func:`str(value) <str>`.

   Lệnh gọi ``format(value, format_spec)`` được chuyển thành ``type(value).__format__(value, format_spec)``, bỏ qua dictionary của instance khi tìm phương thức :meth:`~object.__format__` của giá trị. Một ngoại lệ :exc:`TypeError` sẽ được phát sinh nếu quá trình tìm kiếm phương thức đi đến
   :mod:`object` và *format_spec* không rỗng, hoặc nếu *format_spec* hay giá trị trả về không phải là các chuỗi.

   .. versionchanged:: 3.4
      ``object().__format__(format_spec)`` phát sinh :exc:`TypeError` nếu *format_spec* không phải là một chuỗi rỗng.


.. _func-frozenset:
.. class:: frozenset(iterable=(), /)
   :noindex:

   Trả về một đối tượng :class:`frozenset` mới, tùy chọn với các phần tử lấy từ *iterable*. :class:`frozenset` là một lớp tích hợp sẵn. Xem thêm
   :ref:`types-set` để biết tài liệu về lớp này.

   Đối với các container khác, hãy xem :class:`set` tích hợp sẵn, :class:`list`,
   :class:`tuple` và các lớp :class:`dict`, cũng như mô-đun :mod:`collections`.


.. function:: getattr(object, name, /)
              getattr(object, name, default, /)

   Trả về giá trị của thuộc tính có tên của *object*. *name* phải là một chuỗi. Nếu chuỗi này là tên của một trong các thuộc tính của object, kết quả là giá trị của thuộc tính đó. Ví dụ: ``getattr(x, 'foobar')`` tương đương với ``x.foobar``. Nếu thuộc tính có tên không tồn tại, *default* sẽ được trả về nếu được cung cấp; nếu không, :exc:`AttributeError` sẽ phát sinh. *name* không nhất thiết phải là một định danh Python (xem :func:`setattr`).

   .. note::

      Vì :ref:`private name mangling <private-name-mangling>` diễn ra tại thời điểm biên dịch, cần tự mangle tên của một thuộc tính private (các thuộc tính có hai dấu gạch dưới ở đầu) để truy xuất thuộc tính đó bằng
      :func:`getattr`.


.. function:: globals()

   Trả về từ điển triển khai namespace của module hiện tại. Đối với mã bên trong các hàm, từ điển này được thiết lập khi hàm được định nghĩa và không thay đổi bất kể hàm được gọi ở đâu.


.. function:: hasattr(object, name, /)

   Các đối số là một object và một string. Kết quả là ``True`` nếu string là tên của một thuộc tính của object, và là ``False`` nếu không phải. (Điều này được triển khai bằng cách gọi ``getattr(object, name)`` và kiểm tra xem nó có phát sinh :exc:`AttributeError` hay không.)


.. function:: hash(object, /)

   Trả về giá trị hash của object (nếu object có giá trị hash). Giá trị hash là các số nguyên. Chúng được dùng để nhanh chóng so sánh các khóa dictionary trong quá trình tra cứu dictionary. Các giá trị số bằng nhau khi so sánh sẽ có cùng giá trị hash (ngay cả khi chúng thuộc các kiểu khác nhau, như trường hợp của 1 và 1.0).

   .. note::

      Đối với các object có phương thức :meth:`~object.__hash__` tùy chỉnh, lưu ý rằng :func:`hash` sẽ cắt ngắn giá trị trả về dựa trên độ rộng bit của máy chủ.

.. function:: help()
              help(request)

   Gọi hệ thống trợ giúp tích hợp sẵn. (Hàm này предназнач cho việc sử dụng tương tác.) Nếu không cung cấp đối số, hệ thống trợ giúp tương tác sẽ khởi động trên bảng điều khiển của interpreter. Nếu đối số là một string, string đó sẽ được tra cứu dưới dạng tên của module, function, class, method, keyword hoặc chủ đề tài liệu, rồi một trang trợ giúp sẽ được in trên bảng điều khiển. Nếu đối số là bất kỳ loại object nào khác, một trang trợ giúp về object đó sẽ được tạo.

   Lưu ý rằng nếu dấu gạch chéo(/) xuất hiện trong danh sách tham số của một hàm khi gọi :func:`help`, điều đó có nghĩa là các tham số trước dấu gạch chéo chỉ có thể được truyền theo vị trí. Để biết thêm thông tin, hãy xem
   :ref:`mục FAQ về tham số chỉ có thể truyền theo vị trí <faq-positional-only-arguments>`.

   Hàm này được mô-đun :mod:`site` thêm vào không gian tên dựng sẵn.

   .. versionchanged:: 3.4
      Các thay đổi đối với :mod:`pydoc` và :mod:`inspect` có nghĩa là các chữ ký được báo cáo cho các callable hiện đầy đủ và nhất quán hơn.


.. function:: hex(integer, /)

   Chuyển đổi một số nguyên thành chuỗi thập lục phân viết thường có tiền tố "0x". Nếu *integer* không phải là một đối tượng :class:`int` Python, đối tượng đó phải định nghĩa một
   :meth:`~object.__index__` method trả về một số nguyên. Một số ví dụ:

      >>> hex(255)
      '0xff'
      >>> hex(-42)
      '-0x2a'

   Nếu bạn muốn chuyển đổi một số nguyên thành chuỗi thập lục phân viết hoa hoặc viết thường, có hoặc không có tiền tố, bạn có thể sử dụng một trong các cách sau:

     >>> '%#x' % 255, '%x' % 255, '%X' % 255
     ('0xff', 'ff', 'FF')
     >>> format(255, '#x'), format(255, 'x'), format(255, 'X')
     ('0xff', 'ff', 'FF')
     >>> f'{255:#x}', f'{255:x}', f'{255:X}'
     ('0xff', 'ff', 'FF')

   Xem thêm :func:`format` để biết thêm thông tin.

   Xem thêm :func:`int` để chuyển một chuỗi thập lục phân thành số nguyên bằng cách sử dụng cơ số 16.

   .. note::

      Để nhận biểu diễn chuỗi thập lục phân của một số float, hãy sử dụng
      phương thức :meth:`float.hex`.


.. function:: id(object, /)

   Trả về "identity" của một đối tượng. Đây là một số nguyên được đảm bảo là duy nhất và không đổi đối với đối tượng này trong suốt vòng đời của nó. Hai đối tượng có vòng đời không giao nhau có thể có cùng giá trị :func:`id`.

   .. impl-detail:: This is the address of the object in memory.

   .. audit-event:: builtins.id id id


.. function:: input()
              input(prompt, /)

   Nếu có đối số *prompt*, đối số này sẽ được ghi vào đầu ra tiêu chuẩn mà không có ký tự dòng mới ở cuối. Sau đó, hàm đọc một dòng từ đầu vào, chuyển dòng đó thành chuỗi (loại bỏ ký tự dòng mới ở cuối) và trả về chuỗi đó. Khi đọc đến EOF, :exc:`EOFError` được phát sinh. Ví dụ::

      >>> s = input('--> ')  # doctest: +SKIP
      --> Monty Python's Flying Circus
      >>> s  # doctest: +SKIP
      "Monty Python's Flying Circus"

   Nếu mô-đun :mod:`readline` đã được tải, :func:`input` sẽ sử dụng mô-đun đó để cung cấp các tính năng chỉnh sửa dòng lệnh và lịch sử nâng cao.

   .. audit-event:: builtins.input prompt input

      Phát sinh :ref:`sự kiện kiểm tra <auditing>` ``builtins.input`` với đối số ``prompt`` trước khi đọc dữ liệu nhập

   .. audit-event:: builtins.input/result result input

      Phát sinh :ref:`sự kiện kiểm tra <auditing>` ``builtins.input/result`` với kết quả sau khi đọc dữ liệu nhập thành công.


.. class:: int(number=0, /)
           int(string, /, base=10)

   Trả về một đối tượng số nguyên được tạo từ một số hoặc một chuỗi, hoặc trả về ``0`` nếu không có đối số nào.

   Ví dụ:

   .. doctest::

      >>> int(123.45)
      123
      >>> int('123')
      123
      >>> int('   -12_345\n')
      -12345
      >>> int('FACE', 16)
      64206
      >>> int('0xface', 0)
      64206
      >>> int('01110011', base=2)
      115

   Nếu đối số định nghĩa :meth:`~object.__int__`, ``int(x)`` trả về ``x.__int__()``. Nếu đối số định nghĩa
   :meth:`~object.__index__`, nó trả về ``x.__index__()``. Đối với số dấu phẩy động, thao tác này cắt về 0.

   Nếu đối số không phải là một số hoặc nếu *cơ số* được cung cấp, thì đối số phải là một chuỗi,
   :class:`bytes`, hoặc một instance :class:`bytearray` đại diện cho một số nguyên theo cơ số *cơ số*. Chuỗi này có thể tùy chọn được đặt trước bởi ``+`` hoặc ``-`` (không có khoảng trắng ở giữa), có các số 0 ở đầu, được bao quanh bởi khoảng trắng và có các dấu gạch dưới đơn xen kẽ giữa các chữ số.

   Một chuỗi số nguyên cơ số n chứa các chữ số, mỗi chữ số biểu diễn một giá trị từ 0 đến n-1. Các giá trị 0--9 có thể được biểu diễn bằng bất kỳ chữ số thập phân Unicode nào. Các giá trị 10--35 có thể được biểu diễn bằng ``a`` đến ``z`` (hoặc ``A`` đến ``Z``). *Cơ số* mặc định là 10. Các cơ số được phép là 0 và 2--36. Các chuỗi cơ số 2, 8 và 16 có thể tùy chọn được đặt tiền tố bằng ``0b``/``0B``, ``0o``/``0O`` hoặc ``0x``/``0X``, giống như các literal số nguyên trong code. Với cơ số 0, chuỗi được diễn giải tương tự như một :ref:`literal số nguyên trong code <integers>`, trong đó cơ số thực tế là 2, 8, 10 hoặc 16, được xác định bởi tiền tố. Cơ số 0 cũng không cho phép các số 0 ở đầu: ``int('010', 0)`` không hợp lệ, còn ``int('010')`` và ``int('010', 8)`` thì hợp lệ.

   Kiểu số nguyên được mô tả trong :ref:`typesnumeric`.

   .. versionchanged:: 3.4
      Nếu *base* không phải là một thể hiện của :class:`int` và đối tượng *base* có một
      :meth:`base.__index__ <object.__index__>` method, phương thức đó được gọi để lấy một số nguyên cho base. Các phiên bản trước đây sử dụng
      :meth:`base.__int__ <object.__int__>` thay cho :meth:`base.__index__ <object.__index__>`.

   .. versionchanged:: 3.6
      Cho phép nhóm các chữ số bằng dấu gạch dưới như trong các literal mã.

   .. versionchanged:: 3.7
      Tham số đầu tiên hiện chỉ có thể được truyền theo vị trí.

   .. versionchanged:: 3.8
      Chuyển sang :meth:`~object.__index__` nếu :meth:`~object.__int__` chưa được định nghĩa.

   .. versionchanged:: 3.11
      :class:`int` string inputs and string representations can be limited to
      giúp tránh các cuộc tấn công từ chối dịch vụ. Một :exc:`ValueError` được phát sinh khi vượt quá giới hạn trong quá trình chuyển đổi một chuỗi thành :class:`int`, hoặc khi việc chuyển đổi một :class:`int` thành chuỗi sẽ vượt quá giới hạn. Xem tài liệu về :ref:`giới hạn độ dài chuyển đổi chuỗi số nguyên <int_max_str_digits>`.

   .. versionchanged:: 3.14
      :func:`int` no longer delegates to the :meth:`~object.__trunc__` method.

.. function:: isinstance(object, classinfo, /)

   Trả về ``True`` nếu đối số *object* là một thể hiện của đối số *classinfo*, hoặc của một lớp con (trực tiếp, gián tiếp hoặc :term:`virtual <abstract base class>`) của đối số đó. Nếu *object* không phải là một đối tượng thuộc kiểu đã cho, hàm luôn trả về ``False``. Nếu *classinfo* là một tuple gồm các đối tượng kiểu (hoặc đệ quy, các tuple tương tự khác) hoặc một :ref:`types-union` gồm nhiều kiểu, trả về ``True`` nếu *object* là một thể hiện của bất kỳ kiểu nào trong số đó. Nếu *classinfo* không phải là một kiểu hoặc tuple của các kiểu và các tuple tương tự, một ngoại lệ :exc:`TypeError` sẽ được phát sinh. :exc:`TypeError` có thể không được phát sinh đối với một kiểu không hợp lệ nếu một phép kiểm tra trước đó thành công.

   .. versionchanged:: 3.10
      *classinfo* có thể là một :ref:`types-union`.


.. function:: issubclass(class, classinfo, /)

   Trả về ``True`` nếu *class* là một lớp con (trực tiếp, gián tiếp hoặc :term:`virtual <abstract base class>`) của *classinfo*. Một lớp được xem là lớp con của chính nó. *classinfo* có thể là một tuple gồm các đối tượng lớp (hoặc đệ quy, các tuple tương tự khác) hoặc một :ref:`types-union`; trong trường hợp đó, trả về ``True`` nếu *class* là lớp con của bất kỳ phần tử nào trong *classinfo*. Trong mọi trường hợp khác, một ngoại lệ :exc:`TypeError` sẽ được phát sinh.

   .. versionchanged:: 3.10
      *classinfo* có thể là một :ref:`types-union`.


.. function:: iter(iterable, /)
              iter(callable, sentinel, /)

   Trả về một đối tượng :term:`iterator`. Đối số đầu tiên được diễn giải rất khác nhau tùy thuộc vào việc có đối số thứ hai hay không. Nếu không có đối số thứ hai, đối số duy nhất phải là một đối tượng collection hỗ trợ
   giao thức :term:`iterable` (phương thức :meth:`~object.__iter__`) hoặc phải hỗ trợ giao thức sequence (phương thức :meth:`~object.__getitem__` với các đối số số nguyên bắt đầu từ ``0``). Nếu không hỗ trợ giao thức nào trong hai giao thức đó,
   :exc:`TypeError` được phát sinh. Nếu cung cấp đối số thứ hai, *sentinel*, thì đối số thứ nhất phải là một đối tượng callable. Iterator được tạo trong trường hợp này sẽ gọi *callable* mà không có đối số trong mỗi lần gọi phương thức của nó
   :meth:`~iterator.__next__`; nếu giá trị được trả về bằng *sentinel*, :exc:`StopIteration` sẽ được phát sinh; nếu không, giá trị đó sẽ được trả về.

   Xem thêm :ref:`typeiter`.

   Một ứng dụng hữu ích của dạng thứ hai của :func:`iter` là xây dựng một block-reader. Ví dụ: đọc các block có kích thước cố định từ một tệp cơ sở dữ liệu nhị phân cho đến khi đạt đến cuối tệp::

      from functools import partial
      with open('mydata.db', 'rb') as f:
          for block in iter(partial(f.read, 64), b''):
              process_block(block)


.. function:: len(object, /)

   Trả về độ dài (số lượng phần tử) của một đối tượng. Đối số có thể là một sequence (chẳng hạn như chuỗi, bytes, tuple, list hoặc range) hoặc một collection (chẳng hạn như dictionary, set hoặc frozen set).

   .. impl-detail::

      ``len`` phát sinh :exc:`OverflowError` với các độ dài lớn hơn
      :data:`sys.maxsize`, chẳng hạn như :class:`range(2 ** 100) <range>`.


.. _func-list:
.. class:: list(iterable=(), /)
   :noindex:

   Thay vì là một hàm, :class:`list` thực chất là một kiểu sequence có thể thay đổi, như được mô tả trong :ref:`typesseq-list` và :ref:`typesseq`.


.. function:: locals()

   Trả về một đối tượng mapping biểu thị symbol table cục bộ hiện tại, với tên biến làm khóa và các tham chiếu hiện đang được liên kết với chúng làm giá trị.

   Ở phạm vi module, cũng như khi sử dụng :func:`exec` hoặc :func:`eval` với một namespace duy nhất, hàm này trả về cùng namespace với
   :func:`globals`.

   Ở phạm vi lớp, hàm này trả về namespace sẽ được truyền cho hàm khởi tạo metaclass.

   Khi sử dụng ``exec()`` hoặc ``eval()`` với các đối số local và global riêng biệt, hàm này trả về local namespace được truyền vào lời gọi hàm.

   Trong tất cả các trường hợp trên, mỗi lần gọi ``locals()`` trong một frame thực thi nhất định sẽ trả về cùng một đối tượng mapping *same*. Các thay đổi được thực hiện thông qua đối tượng mapping do ``locals()`` trả về sẽ hiển thị dưới dạng các biến cục bộ được gán, gán lại hoặc xóa, đồng thời việc gán, gán lại hoặc xóa các biến cục bộ sẽ ngay lập tức ảnh hưởng đến nội dung của đối tượng mapping được trả về.

   Trong một :term:`optimized scope` (bao gồm các hàm, generator và coroutine), mỗi lần gọi ``locals()`` thay vào đó sẽ trả về một dictionary mới chứa các binding hiện tại của biến cục bộ trong hàm và mọi tham chiếu cell nonlocal. Trong trường hợp này, các thay đổi binding tên được thực hiện thông qua dict được trả về *not* được ghi ngược vào các biến cục bộ hoặc tham chiếu cell nonlocal tương ứng, và việc gán, gán lại hoặc xóa các biến cục bộ cũng như tham chiếu cell nonlocal *not* không ảnh hưởng đến nội dung của các dictionary đã được trả về trước đó.

   Việc gọi ``locals()`` trong một comprehension thuộc một function, generator hoặc coroutine tương đương với việc gọi nó trong scope chứa, ngoại trừ việc các biến lặp được khởi tạo của comprehension cũng sẽ được đưa vào. Trong các scope khác, nó hoạt động như thể comprehension đang chạy dưới dạng một function lồng nhau.

   Việc gọi ``locals()`` trong một generator expression tương đương với việc gọi nó trong một generator function lồng nhau.

   .. versionchanged:: 3.12
      Hành vi của ``locals()`` trong một comprehension đã được cập nhật như mô tả trong :pep:`709`.

   .. versionchanged:: 3.13
      Trong khuôn khổ :pep:`667`, ngữ nghĩa của việc thay đổi các đối tượng mapping được function này trả về hiện đã được định nghĩa. Hành vi trong
      :term:`các scope được tối ưu hóa <optimized scope>` hiện được mô tả như trên. Ngoài việc đã được định nghĩa, hành vi trong các scope khác vẫn không thay đổi so với các phiên bản trước.


.. function:: map(function, iterable, /, *iterables, strict=False)

   Trả về một iterator áp dụng *function* cho từng mục của *iterable*, rồi trả về các kết quả. Nếu truyền thêm các đối số *iterables*, *function* phải nhận số lượng đối số tương ứng và được áp dụng song song cho các mục từ tất cả các iterable. Với nhiều iterable, iterator sẽ dừng khi iterable ngắn nhất đã :term:`exhausted`. Nếu *strict* là ``True`` và một trong các iterable cạn kiệt trước những iterable khác, một :exc:`ValueError` sẽ được sinh ra. Trong trường hợp các đầu vào của function đã được sắp xếp thành các tuple đối số, hãy xem :func:`itertools.starmap`.

   .. versionchanged:: 3.14
      Đã thêm tham số *strict*.


.. function:: max(iterable, /, *, key=None)
              max(iterable, /, *, default, key=None) max(arg1, arg2, /, *args, key=None)

   Trả về mục lớn nhất trong một iterable hoặc giá trị lớn nhất trong hai hay nhiều đối số.

   Nếu cung cấp một đối số vị trí, đối số đó phải là một :term:`iterable`. Mục lớn nhất trong iterable sẽ được trả về. Nếu cung cấp từ hai đối số vị trí trở lên, đối số vị trí lớn nhất sẽ được trả về.

   Có hai đối số chỉ dành cho từ khóa tùy chọn. Đối số *key* chỉ định một hàm sắp xếp nhận một đối số, tương tự hàm được dùng cho :meth:`list.sort`. Đối số *default* chỉ định một đối tượng sẽ được trả về nếu iterable được cung cấp là rỗng. Nếu iterable rỗng và không cung cấp *default*, một
   :exc:`ValueError` sẽ được phát sinh.

   Nếu nhiều mục có cùng giá trị lớn nhất, hàm sẽ trả về mục đầu tiên được gặp. Điều này nhất quán với các công cụ khác có khả năng duy trì tính ổn định khi sắp xếp, chẳng hạn như ``sorted(iterable, key=keyfunc, reverse=True)[0]`` và ``heapq.nlargest(1, iterable, key=keyfunc)``.

   .. versionchanged:: 3.4
      Đã thêm tham số chỉ dành cho từ khóa *default*.

   .. versionchanged:: 3.8
      *key* có thể ``None``.


.. _func-memoryview:
.. class:: memoryview(object)
   :noindex:

   Trả về một đối tượng "memory view" được tạo từ đối số đã cho. Xem
   :ref:`typememoryview` để biết thêm thông tin.


.. function:: min(iterable, /, *, key=None)
              min(iterable, /, *, default, key=None) min(arg1, arg2, /, *args, key=None)

   Trả về phần tử nhỏ nhất trong một iterable hoặc giá trị nhỏ nhất trong hai hay nhiều đối số.

   Nếu cung cấp một đối số vị trí, đối số đó phải là một :term:`iterable`. Phần tử nhỏ nhất trong iterable sẽ được trả về. Nếu cung cấp từ hai đối số vị trí trở lên, đối số vị trí nhỏ nhất sẽ được trả về.

   Có hai đối số chỉ dành cho từ khóa tùy chọn. Đối số *key* chỉ định một hàm sắp xếp nhận một đối số, tương tự hàm được dùng cho :meth:`list.sort`. Đối số *default* chỉ định một đối tượng sẽ được trả về nếu iterable được cung cấp là rỗng. Nếu iterable rỗng và không cung cấp *default*, một
   :exc:`ValueError` sẽ được phát sinh.

   Nếu có nhiều mục cùng đạt giá trị nhỏ nhất, hàm sẽ trả về mục đầu tiên được gặp. Điều này nhất quán với các công cụ khác cũng duy trì tính ổn định của việc sắp xếp, chẳng hạn như ``sorted(iterable, key=keyfunc)[0]`` và ``heapq.nsmallest(1, iterable, key=keyfunc)``.

   .. versionchanged:: 3.4
      Đã thêm tham số chỉ dành cho từ khóa *default*.

   .. versionchanged:: 3.8
      *key* có thể ``None``.


.. function:: next(iterator, /)
              next(iterator, default, /)

   Lấy mục tiếp theo từ :term:`iterator` bằng cách gọi phương thức
   :meth:`~iterator.__next__` của nó. Nếu *default* được cung cấp, giá trị này sẽ được trả về nếu iterator là :term:`exhausted`; nếu không, :exc:`StopIteration` sẽ được phát sinh.


.. class:: object()

   Đây là lớp cơ sở tối cao của tất cả các lớp khác. Lớp này có các phương thức dùng chung cho mọi instance của các lớp Python. Khi được gọi, hàm khởi tạo trả về một đối tượng mới không có tính năng. Hàm khởi tạo không nhận bất kỳ đối số nào.

   .. note::

      Các instance :class:`object` không *not* có :attr:`~object.__dict__` thuộc tính, vì vậy bạn không thể gán các thuộc tính tùy ý cho một instance của
      :class:`object`.


.. function:: oct(integer, /)

  Chuyển đổi một số nguyên thành chuỗi bát phân có tiền tố "0o". Kết quả là một biểu thức Python hợp lệ. Nếu *integer* không phải là một đối tượng :class:`int` Python, đối tượng đó phải định nghĩa một phương thức :meth:`~object.__index__` trả về một số nguyên. Ví dụ:

      >>> oct(8)
      '0o10'
      >>> oct(-56)
      '-0o70'

  Nếu muốn chuyển đổi một số nguyên thành chuỗi bát phân có hoặc không có tiền tố "0o", bạn có thể sử dụng một trong các cách sau.

      >>> '%#o' % 10, '%o' % 10
      ('0o12', '12')
      >>> format(10, '#o'), format(10, 'o')
      ('0o12', '12')
      >>> f'{10:#o}', f'{10:o}'
      ('0o12', '12')

  Xem thêm :func:`format` để biết thêm thông tin.

.. index::
   single: file object; open() built-in function

.. function:: open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)

   Mở *file* và trả về một :term:`file object` tương ứng. Nếu không thể mở tệp, một :exc:`OSError` sẽ được raise. Xem
   :ref:`tut-files` để biết thêm ví dụ về cách sử dụng hàm này.

   *file* là một :term:`path-like object` cung cấp tên đường dẫn (tuyệt đối hoặc tương đối với thư mục làm việc hiện tại) của tệp cần mở hoặc một bộ mô tả tệp dạng số của tệp cần bọc. (Nếu cung cấp bộ mô tả tệp, bộ mô tả này sẽ được đóng khi đối tượng I/O được trả về đóng, trừ khi *closefd* được đặt thành ``False``.)

   *mode* là một chuỗi tùy chọn chỉ định chế độ mở tệp. Mặc định là ``'r'``, nghĩa là mở để đọc ở chế độ văn bản. Các giá trị phổ biến khác là ``'w'`` để ghi (cắt ngắn tệp nếu tệp đã tồn tại), ``'x'`` để tạo tệp độc quyền và ``'a'`` để nối thêm (trên *some* hệ thống Unix, điều này có nghĩa là *all* thao tác ghi đều nối vào cuối tệp bất kể vị trí seek hiện tại). Ở chế độ văn bản, nếu không chỉ định *encoding*, encoding được sử dụng phụ thuộc vào nền tảng:
   :func:`locale.getencoding` được gọi để lấy encoding của locale hiện tại. (Để đọc và ghi các byte thô, hãy sử dụng chế độ nhị phân và không chỉ định *encoding*.) Các chế độ khả dụng là:

   .. _filemodes:

   .. index::
      pair: file; modes

   +---------+--------------------------------------------------------+
   | Ký tự   | Ý nghĩa                                                |
   +=========+========================================================+
   | ``'r'`` | mở để đọc (mặc định)                                   |
   +---------+--------------------------------------------------------+
   | ``'w'`` | mở để ghi, trước tiên cắt ngắn tệp                     |
   +---------+--------------------------------------------------------+
   | ``'x'`` | mở để tạo tệp độc quyền, và báo lỗi nếu tệp đã tồn tại |
   +---------+--------------------------------------------------------+
   | ``'a'`` | mở để ghi, nối thêm vào cuối tệp nếu tệp đã tồn tại    |
   +---------+--------------------------------------------------------+
   | ``'b'`` | chế độ nhị phân                                        |
   +---------+--------------------------------------------------------+
   | ``'t'`` | chế độ văn bản (mặc định)                              |
   +---------+--------------------------------------------------------+
   | ``'+'`` | mở để cập nhật (đọc và ghi)                            |
   +---------+--------------------------------------------------------+

   Chế độ mặc định là ``'r'`` (mở để đọc văn bản, đồng nghĩa với ``'rt'``). Các chế độ ``'w+'`` và ``'w+b'`` mở và cắt ngắn tệp. Các chế độ ``'r+'`` và ``'r+b'`` mở tệp mà không cắt ngắn.

   Như đã đề cập trong :ref:`io-overview`, Python phân biệt I/O nhị phân và I/O văn bản. Các tệp được mở ở chế độ nhị phân (bao gồm ``'b'`` trong đối số *mode*) trả về nội dung dưới dạng đối tượng :class:`bytes` mà không giải mã. Ở chế độ văn bản (mặc định hoặc khi ``'t'`` được đưa vào đối số *mode*), nội dung của tệp được trả về dưới dạng :class:`str`; các byte trước đó đã được giải mã bằng bảng mã phụ thuộc vào nền tảng hoặc bằng *encoding* được chỉ định nếu có.

   .. note::

      Python không phụ thuộc vào cách hệ điều hành nền tảng định nghĩa tệp văn bản; mọi quá trình xử lý đều do Python tự thực hiện và vì vậy không phụ thuộc nền tảng.

   *buffering* là một số nguyên tùy chọn dùng để thiết lập chính sách buffering. Truyền 0 để tắt buffering (chỉ được phép ở chế độ nhị phân), 1 để chọn line buffering (chỉ có thể sử dụng khi ghi ở chế độ văn bản), và một số nguyên > 1 để chỉ kích thước tính theo byte của bộ đệm khối có kích thước cố định. Lưu ý rằng việc chỉ định kích thước bộ đệm theo cách này áp dụng cho I/O nhị phân có buffering, nhưng ``TextIOWrapper`` (tức là các tệp được mở bằng ``mode='r+'``) sẽ có cơ chế buffering khác. Để tắt buffering trong ``TextIOWrapper``, hãy cân nhắc sử dụng cờ ``write_through`` cho
   :func:`io.TextIOWrapper.reconfigure`. Khi không cung cấp đối số *buffering*, chính sách buffering mặc định hoạt động như sau:

   * Các tệp nhị phân được buffering theo các khối có kích thước cố định; kích thước của bộ đệm là ``max(min(blocksize, 8 MiB), DEFAULT_BUFFER_SIZE)`` khi có sẵn kích thước khối của thiết bị. Trên hầu hết các hệ thống, bộ đệm thường có kích thước 128 kilobyte.

   * Các tệp văn bản “tương tác” (những tệp mà :meth:`~io.IOBase.isatty` trả về ``True``) sử dụng line buffering. Các tệp văn bản khác sử dụng chính sách được mô tả ở trên dành cho tệp nhị phân.

   *encoding* là tên của encoding được sử dụng để giải mã hoặc mã hóa tệp. Chỉ nên sử dụng tùy chọn này ở chế độ văn bản. Encoding mặc định phụ thuộc vào nền tảng (bất kỳ giá trị nào :func:`locale.getencoding` trả về), nhưng bất kỳ
   :term:`text encoding` được Python hỗ trợ đều có thể được sử dụng. Xem module :mod:`codecs` để biết danh sách các encoding được hỗ trợ.

   *errors* là một chuỗi tùy chọn chỉ định cách xử lý lỗi mã hóa và giải mã—không thể sử dụng tùy chọn này ở chế độ nhị phân. Có nhiều error handler tiêu chuẩn (được liệt kê trong :ref:`error-handlers`), mặc dù mọi tên xử lý lỗi đã được đăng ký với
   :func:`codecs.register_error` cũng hợp lệ. Các tên tiêu chuẩn gồm:

   * ``'strict'`` sẽ raise một ngoại lệ :exc:`ValueError` nếu xảy ra lỗi mã hóa. Giá trị mặc định của ``None`` cũng có tác dụng tương tự.

   * ``'ignore'`` bỏ qua các lỗi. Lưu ý rằng việc bỏ qua lỗi mã hóa có thể dẫn đến mất dữ liệu.

   * ``'replace'`` khiến một dấu đánh dấu thay thế (chẳng hạn như ``'?'``) được chèn vào vị trí có dữ liệu không đúng định dạng.

   * ``'surrogateescape'`` sẽ biểu diễn mọi byte không hợp lệ dưới dạng các code unit surrogate thấp trong khoảng từ U+DC80 đến U+DCFF. Sau đó, các code unit surrogate này sẽ được chuyển lại thành chính những byte đó khi error handler ``surrogateescape`` được sử dụng lúc ghi dữ liệu. Điều này hữu ích khi xử lý các tệp có encoding không xác định.

   * ``'xmlcharrefreplace'`` chỉ được hỗ trợ khi ghi vào tệp. Các ký tự không được encoding hỗ trợ sẽ được thay thế bằng tham chiếu ký tự XML thích hợp :samp:`&#{nnn};`.

   * ``'backslashreplace'`` thay thế dữ liệu không đúng định dạng bằng các chuỗi escape có dấu gạch chéo ngược của Python.

   * ``'namereplace'`` (cũng chỉ được hỗ trợ khi ghi) thay thế các ký tự không được hỗ trợ bằng các chuỗi escape ``\N{...}``.

   .. index::
      single: universal newlines; open() built-in function

   .. _open-newline-parameter:

   *newline* xác định cách phân tích các ký tự dòng mới từ stream. Giá trị này có thể là ``None``, ``''``, ``'\n'``, ``'\r'`` hoặc ``'\r\n'``. Cách hoạt động như sau:

   * Khi đọc dữ liệu đầu vào từ stream, nếu *newline* là ``None``, chế độ dòng mới phổ quát được bật. Các dòng trong dữ liệu đầu vào có thể kết thúc bằng ``'\n'``, ``'\r'`` hoặc ``'\r\n'``, và chúng được chuyển thành ``'\n'`` trước khi trả về cho caller. Nếu giá trị là ``''``, chế độ dòng mới phổ quát vẫn được bật, nhưng các ký tự kết thúc dòng được trả về cho caller mà không được dịch. Nếu có một trong các giá trị hợp lệ khác, các dòng đầu vào chỉ được kết thúc bằng chuỗi đã cho, và ký tự kết thúc dòng được trả về cho caller mà không được dịch.

   * Khi ghi dữ liệu đầu ra vào stream, nếu *newline* là ``None``, mọi ký tự ``'\n'`` được ghi sẽ được chuyển thành dấu phân cách dòng mặc định của hệ thống,
     :data:`os.linesep`. Nếu *newline* là ``''`` hoặc ``'\n'``, không có phép chuyển đổi nào được thực hiện. Nếu *newline* là một trong các giá trị hợp lệ khác, mọi ký tự ``'\n'`` được ghi sẽ được chuyển thành chuỗi đã cho.

   Nếu *closefd* là ``False`` và một file descriptor thay vì tên tệp được cung cấp, file descriptor bên dưới sẽ vẫn mở khi tệp được đóng. Nếu cung cấp tên tệp, *closefd* phải là ``True`` (giá trị mặc định); nếu không, một lỗi sẽ được phát sinh.

   Có thể sử dụng một opener tùy chỉnh bằng cách truyền một callable dưới dạng *opener*. Sau đó, bộ mô tả tệp bên dưới của đối tượng tệp được lấy bằng cách gọi *opener* với (*file*, *flags*). *opener* phải trả về một bộ mô tả tệp đang mở (truyền
   :mod:`os.open` dưới dạng *opener* sẽ cho kết quả tương tự như truyền ``None``).

   Tệp mới được tạo là :ref:`non-inheritable <fd_inheritance>`.

   Ví dụ sau sử dụng tham số :ref:`dir_fd <dir_fd>` của
   hàm :func:`os.open` để mở một tệp tương đối với một thư mục đã cho::

      >>> import os
      >>> dir_fd = os.open('somedir', os.O_RDONLY)
      >>> def opener(path, flags):
      ...     return os.open(path, flags, dir_fd=dir_fd)
      ...
      >>> with open('spamspam.txt', 'w', opener=opener) as f:
      ...     print('This will be written to somedir/spamspam.txt', file=f)
      ...
      >>> os.close(dir_fd)  # không làm rò rỉ bộ mô tả tệp

   Kiểu của :term:`file object` được hàm :func:`open` trả về phụ thuộc vào mode. Khi sử dụng :func:`open` để mở một tệp ở chế độ văn bản (``'w'``, ``'r'``, ``'wt'``, ``'rt'``, v.v.), hàm này trả về một lớp con của
   :class:`io.TextIOBase` (cụ thể là :class:`io.TextIOWrapper`). Khi được dùng để mở một tệp ở chế độ nhị phân có buffering, lớp được trả về là lớp con của :class:`io.BufferedIOBase`. Lớp cụ thể sẽ khác nhau: ở chế độ đọc nhị phân, hàm trả về một :class:`io.BufferedReader`; ở chế độ ghi nhị phân và nối thêm nhị phân, hàm trả về một :class:`io.BufferedWriter`; còn ở chế độ đọc/ghi, hàm trả về một :class:`io.BufferedRandom`. Khi buffering bị tắt, luồng thô, là lớp con của :class:`io.RawIOBase`,
   :class:`io.FileIO`, sẽ được trả về.

   .. index::
      single: line-buffered I/O
      single: unbuffered I/O
      single: buffer size, I/O
      single: I/O control; buffering
      single: binary mode
      single: text mode
      pair: module; sys

   Xem thêm các module xử lý tệp, chẳng hạn như :mod:`fileinput`, :mod:`io` (nơi :func:`open` được khai báo), :mod:`os`, :mod:`os.path`, :mod:`tempfile` và :mod:`shutil`.

   .. audit-event:: open path,mode,flags open

   Các đối số ``mode`` và ``flags`` có thể đã được sửa đổi hoặc suy ra từ lời gọi ban đầu.

   .. versionchanged:: 3.3

      * Tham số *opener* đã được thêm vào.
      * Chế độ ``'x'`` đã được thêm vào.
      * Trước đây :exc:`IOError` được đưa ra; hiện tại nó là bí danh của :exc:`OSError`.
      * :exc:`FileExistsError` giờ đây được phát sinh nếu tệp được mở ở chế độ tạo độc quyền (``'x'``) đã tồn tại.

   .. versionchanged:: 3.4

      * Tệp giờ đây không thể được kế thừa.

   .. versionchanged:: 3.5

      * Nếu system call bị gián đoạn và signal handler không phát sinh ngoại lệ, hàm giờ đây sẽ thử lại system call thay vì phát sinh một
        ngoại lệ :exc:`InterruptedError` (xem :pep:`475` để biết lý do).
      * Đã bổ sung error handler ``'namereplace'``.

   .. versionchanged:: 3.6

      * Đã bổ sung hỗ trợ để chấp nhận các đối tượng triển khai :class:`os.PathLike`.
      * Trên Windows, việc mở bộ đệm console có thể trả về một lớp con của
        :class:`io.RawIOBase` khác với :class:`io.FileIO`.

   .. versionchanged:: 3.11
      Chế độ ``'U'`` đã bị loại bỏ.

.. function:: ord(character, /)

   Trả về giá trị ordinal của một ký tự.

   Nếu đối số là một chuỗi gồm một ký tự, trả về code point Unicode của ký tự đó. Ví dụ, ``ord('a')`` trả về số nguyên ``97`` và ``ord('€')`` (ký hiệu Euro) trả về ``8364``. Đây là phép nghịch đảo của :func:`chr`.

   Nếu đối số là một đối tượng :class:`bytes` hoặc :class:`bytearray` có độ dài bằng 1, trả về giá trị byte duy nhất của đối tượng đó. Ví dụ, ``ord(b'a')`` trả về số nguyên ``97``.


.. function:: pow(base, exp, mod=None)

   Trả về *base* lũy thừa *exp*; nếu có *mod*, trả về *base* lũy thừa *exp*, theo modulo *mod* (được tính hiệu quả hơn ``pow(base, exp) % mod``). Dạng hai đối số ``pow(base, exp)`` tương đương với việc sử dụng toán tử lũy thừa: ``base**exp``.

   Khi các đối số là các kiểu số dựng sẵn với các kiểu toán hạng khác nhau, các quy tắc ép kiểu dành cho các toán tử số học nhị phân sẽ được áp dụng. Đối với các toán hạng :class:`int`, kết quả có cùng kiểu với các toán hạng (sau khi ép kiểu), trừ khi đối số thứ hai là số âm; trong trường hợp đó, tất cả các đối số được chuyển đổi thành float và kết quả float được trả về. Ví dụ, ``pow(10, 2)`` trả về ``100``, nhưng ``pow(10, -2)`` trả về ``0.01``. Đối với một cơ số âm có kiểu :class:`int` hoặc :class:`float` và số mũ không nguyên, kết quả complex sẽ được trả về. Ví dụ, ``pow(-9, 0.5)`` trả về một giá trị gần với ``3j``. Ngược lại, đối với một cơ số âm có kiểu :class:`int` hoặc :class:`float` với số mũ nguyên, kết quả float sẽ được trả về. Ví dụ, ``pow(-9, 2.0)`` trả về ``81.0``.

   Đối với :class:`int` các toán hạng *base* và *exp*, nếu có *mod*, thì *mod* cũng phải thuộc kiểu số nguyên và *mod* phải khác không. Nếu có *mod* và *exp* là số âm, thì *base* phải nguyên tố cùng nhau với *mod*. Trong trường hợp đó, ``pow(inv_base, -exp, mod)`` được trả về, trong đó *inv_base* là nghịch đảo của *base* theo modulo *mod*.

   Sau đây là một ví dụ về cách tính nghịch đảo của ``38`` theo modulo ``97``::

      >>> pow(38, -1, mod=97)
      23
      >>> 23 * 38 % 97 == 1
      True

   .. versionchanged:: 3.8
      Với các toán hạng :class:`int`, dạng ba đối số của ``pow`` hiện cho phép đối số thứ hai là số âm, từ đó cho phép tính nghịch đảo modulo.

   .. versionchanged:: 3.8
      Cho phép các đối số keyword. Trước đây, chỉ các đối số positional được hỗ trợ.


.. function:: print(*objects, sep=' ', end='\n', file=None, flush=False)

   In *objects* vào luồng văn bản *file*, được phân tách bằng *sep* và kết thúc bằng *end*. *sep*, *end*, *file* và *flush*, nếu có, phải được truyền dưới dạng các đối số keyword.

   Tất cả các đối số không phải keyword được chuyển đổi thành chuỗi giống như :func:`str` và được ghi vào luồng, phân tách bằng *sep* và kết thúc bằng *end*. Cả *sep* và *end* đều phải là chuỗi; chúng cũng có thể là ``None``, nghĩa là sử dụng các giá trị mặc định. Nếu không cung cấp *objects*, :func:`print` sẽ chỉ ghi *end*.

   Đối số *file* phải là một đối tượng có phương thức ``write(string)``; nếu phương thức này không tồn tại hoặc ``None``, :data:`sys.stdout` sẽ được sử dụng. Vì các đối số được in được chuyển đổi thành chuỗi văn bản, không thể sử dụng :func:`print` với các đối tượng tệp ở chế độ nhị phân. Với các đối tượng này, hãy sử dụng ``file.write(...)`` thay thế.

   Việc đệm đầu ra thường được xác định bởi *file*. Tuy nhiên, nếu *flush* là true, stream sẽ bị flush cưỡng bức.


   .. versionchanged:: 3.3
      Đã thêm đối số từ khóa *flush*.


.. class:: property(fget=None, fset=None, fdel=None, doc=None)

   Trả về một thuộc tính property.

   *fget* là một hàm dùng để lấy giá trị thuộc tính. *fset* là một hàm dùng để đặt giá trị thuộc tính. *fdel* là một hàm dùng để xóa giá trị thuộc tính. Còn *doc* tạo docstring cho thuộc tính.

   Một cách sử dụng điển hình là định nghĩa một thuộc tính được quản lý ``x``::

      class C:
          def __init__(self):
              self._x = None

          def getx(self):
              return self._x

          def setx(self, value):
              self._x = value

          def delx(self):
              del self._x

          x = property(getx, setx, delx, "I'm the 'x' property.")

   Nếu *c* là một thể hiện của *C*, ``c.x`` sẽ gọi getter, ``c.x = value`` sẽ gọi setter và ``del c.x`` sẽ gọi deleter.

   Nếu được cung cấp, *doc* sẽ là docstring của thuộc tính property. Nếu không, property sẽ sao chép docstring của *fget* (nếu có). Điều này giúp dễ dàng tạo các property chỉ đọc bằng cách sử dụng :deco:`property` làm một :term:`decorator`::

      class Parrot:
          def __init__(self):
              self._voltage = 100000

          @property
          def voltage(self):
              """Get the current voltage."""
              return self._voltage

   Decorator ``@property`` biến phương thức :meth:`!voltage` thành một "getter" cho thuộc tính chỉ đọc có cùng tên, đồng thời đặt chuỗi tài liệu cho *voltage* thành "Get the current voltage."

   .. decorator:: property.getter
   .. decorator:: property.setter
   .. decorator:: property.deleter

      Một đối tượng property có các phương thức ``getter``, ``setter`` và ``deleter`` có thể dùng làm decorator để tạo một bản sao của property với hàm accessor tương ứng được gán cho hàm đã áp dụng decorator. Ví dụ sau sẽ giải thích rõ hơn:

      .. testcode::

         class C:
             def __init__(self):
                 self._x = None

             @property
             def x(self):
                 """I'm the 'x' property."""
                 return self._x

             @x.setter
             def x(self, value):
                 self._x = value

             @x.deleter
             def x(self):
                 del self._x

      Đoạn mã này hoàn toàn tương đương với ví dụ đầu tiên. Hãy nhớ đặt cho các hàm bổ sung cùng tên với property ban đầu (trong trường hợp này là ``x``).

      Đối tượng property được trả về cũng có các thuộc tính ``fget``, ``fset`` và ``fdel`` tương ứng với các đối số của hàm khởi tạo.

   .. versionchanged:: 3.5
      Giờ đây, chuỗi tài liệu của các đối tượng property có thể được ghi.

   .. attribute:: __name__

      Thuộc tính chứa tên của property. Có thể thay đổi tên của property trong runtime.

      .. versionadded:: 3.13


.. _func-range:
.. class:: range(stop, /)
           range(start, stop, step=1, /)
   :noindex:

   Thay vì là một hàm, :class:`range` thực ra là một kiểu sequence bất biến, như được mô tả trong :ref:`typesseq-range` và :ref:`typesseq`.


.. function:: repr(object, /)

   Trả về một chuỗi chứa biểu diễn có thể in được của một đối tượng. Với nhiều kiểu, hàm này cố gắng trả về một chuỗi có thể tạo ra một đối tượng có cùng giá trị khi được truyền cho :func:`eval`; nếu không, biểu diễn sẽ là một chuỗi được đặt trong dấu ngoặc nhọn, chứa tên kiểu của đối tượng cùng với thông tin bổ sung, thường bao gồm tên và địa chỉ của đối tượng. Một class có thể kiểm soát giá trị mà hàm này trả về cho các instance của nó bằng cách định nghĩa phương thức :meth:`~object.__repr__`. Nếu :func:`sys.displayhook` không thể truy cập, hàm này sẽ phát sinh
   :exc:`RuntimeError`.

   Class này có một biểu diễn tùy chỉnh có thể được đánh giá::

      class Person:
         def __init__(self, name, age):
            self.name = name
            self.age = age

         def __repr__(self):
            return f"Person('{self.name}', {self.age})"


.. function:: reversed(object, /)

   Trả về một :term:`iterator` ngược. Đối số phải là một đối tượng có phương thức :meth:`~object.__reversed__` hoặc hỗ trợ sequence protocol (giao thức sequence) (phương thức
   :meth:`~object.__len__` và phương thức :meth:`~object.__getitem__` với các đối số số nguyên bắt đầu từ ``0``).


.. function:: round(number, ndigits=None)

   Trả về *number* được làm tròn đến độ chính xác *ndigits* chữ số sau dấu thập phân. Nếu *ndigits* bị bỏ qua hoặc là ``None``, hàm sẽ trả về số nguyên gần nhất với giá trị đầu vào.

   Đối với các kiểu dựng sẵn hỗ trợ :func:`round`, các giá trị được làm tròn đến bội số gần nhất của 10 lũy thừa âm *ndigits*; nếu hai bội số cách đều nhau, việc làm tròn sẽ hướng đến lựa chọn chẵn (vì vậy, chẳng hạn, cả ``round(0.5)`` và ``round(-0.5)`` đều là ``0``, còn ``round(1.5)`` là ``2``). Mọi giá trị số nguyên đều hợp lệ cho *ndigits* (dương, bằng không hoặc âm). Giá trị trả về là một số nguyên nếu *ndigits* bị bỏ qua hoặc là ``None``. Nếu không, giá trị trả về có cùng kiểu với *number*.

   Đối với một đối tượng Python tổng quát ``number``, ``round`` ủy quyền cho ``number.__round__``.

   .. note::

      Hành vi của :func:`round` đối với số thực có thể gây bất ngờ: chẳng hạn, ``round(2.675, 2)`` cho kết quả ``2.67`` thay vì ``2.68`` như mong đợi. Đây không phải là lỗi: nguyên nhân là hầu hết các phân số thập phân không thể được biểu diễn chính xác dưới dạng số thực. Xem :ref:`tut-fp-issues` để biết thêm thông tin.


.. _func-set:
.. class:: set(iterable=(), /)
   :noindex:

   Trả về một đối tượng :class:`set` mới, tùy chọn với các phần tử được lấy từ *iterable*. :class:`set` là một lớp tích hợp sẵn. Xem thêm
   :ref:`types-set` để biết tài liệu về lớp này.

   Đối với các container khác, hãy xem :class:`frozenset` tích hợp sẵn, :class:`list`,
   :class:`tuple` và các lớp :class:`dict`, cũng như mô-đun :mod:`collections`.


.. function:: setattr(object, name, value, /)

   Đây là thành phần tương ứng của :func:`getattr`. Các đối số là một đối tượng, một chuỗi và một giá trị tùy ý. Chuỗi này có thể chỉ định một thuộc tính hiện có hoặc một thuộc tính mới. Hàm gán giá trị cho thuộc tính, với điều kiện đối tượng cho phép. Ví dụ, ``setattr(x, 'foobar', 123)`` tương đương với ``x.foobar = 123``.

   *name* không nhất thiết phải là một định danh Python như được định nghĩa trong :ref:`identifiers`, trừ khi đối tượng chọn thực thi yêu cầu đó, chẳng hạn trong một
   :meth:`~object.__getattribute__` hoặc thông qua :attr:`~object.__slots__`. Một thuộc tính có tên không phải là định danh sẽ không thể được truy cập bằng ký hiệu dấu chấm, nhưng có thể được truy cập thông qua :func:`getattr` và các cách tương tự.

   .. note::

      Vì :ref:`private name mangling <private-name-mangling>` diễn ra tại thời điểm biên dịch, ta phải tự biến đổi tên của một thuộc tính private (các thuộc tính có hai dấu gạch dưới ở đầu) để đặt nó bằng
      :func:`setattr`.


.. class:: slice(stop, /)
           slice(start, stop, step=None, /)

   Trả về một đối tượng :term:`slice` đại diện cho tập hợp các chỉ mục được chỉ định bởi ``range(start, stop, step)``. Các đối số *start* và *step* mặc định là ``None``.

   Các đối tượng Slice cũng được tạo khi sử dụng :ref:`cú pháp slicing <slicings>`. Ví dụ: ``a[start:stop:step]`` hoặc ``a[start:stop, i]``.

   Xem :func:`itertools.islice` để biết một phiên bản thay thế trả về một
   :term:`iterator`.

   .. attribute:: slice.start
                  slice.stop slice.step

      Các thuộc tính chỉ đọc này được đặt thành các giá trị đối số (hoặc giá trị mặc định tương ứng). Chúng không có chức năng rõ ràng nào khác; tuy nhiên, NumPy và các package bên thứ ba khác sử dụng chúng.

   .. versionchanged:: 3.12
      Các đối tượng Slice hiện đã :term:`hashable` (với điều kiện :attr:`~slice.start`,
      :attr:`~slice.stop`, và :attr:`~slice.step` đều có thể băm).

.. function:: sorted(iterable, /, *, key=None, reverse=False)

   Trả về một danh sách mới đã được sắp xếp từ các phần tử trong *iterable*.

   Có hai đối số tùy chọn, phải được chỉ định dưới dạng đối số từ khóa.

   *key* chỉ định một hàm nhận một đối số, được dùng để trích xuất khóa so sánh từ mỗi phần tử trong *iterable* (ví dụ: ``key=str.lower``). Giá trị mặc định là ``None`` (so sánh trực tiếp các phần tử).

   *reverse* là một giá trị boolean. Nếu được đặt thành ``True``, các phần tử trong danh sách sẽ được sắp xếp như thể mỗi phép so sánh đều bị đảo ngược.

   Sử dụng :func:`functools.cmp_to_key` để chuyển một hàm *cmp* kiểu cũ thành một hàm *key*.

   Hàm dựng sẵn :func:`sorted` được đảm bảo là stable. Một phép sắp xếp là stable nếu đảm bảo không thay đổi thứ tự tương đối của các phần tử được so sánh là bằng nhau --- điều này hữu ích khi sắp xếp qua nhiều lượt (ví dụ: sắp xếp theo phòng ban, sau đó theo bậc lương).

   Thuật toán sắp xếp chỉ sử dụng các phép so sánh ``<`` giữa các mục. Mặc dù chỉ cần định nghĩa phương thức :meth:`~object.__lt__` để sắp xếp,
   :PEP:`8` khuyến nghị triển khai cả sáu phép :ref:`rich comparisons <comparisons>`. Điều này giúp tránh lỗi khi sử dụng cùng một dữ liệu với các công cụ sắp xếp khác, chẳng hạn như :func:`max`, vốn dựa vào một phương thức nền tảng khác. Việc triển khai cả sáu phép so sánh cũng giúp tránh nhầm lẫn khi so sánh các kiểu hỗn hợp, vì chúng có thể gọi phương thức :meth:`~object.__gt__` phản chiếu.

   Để xem các ví dụ về sắp xếp và hướng dẫn ngắn về sắp xếp, hãy xem :ref:`sortinghowto`.

.. decorator:: staticmethod

   Chuyển một phương thức thành một static method.

   Một phương thức static không nhận đối số đầu tiên ngầm định. Để khai báo một phương thức static, hãy sử dụng thành ngữ này::

      class C:
          @staticmethod
          def f(arg1, arg2, argN): ...

   Dạng ``@staticmethod`` là một hàm :term:`decorator` -- xem
   :ref:`function` để biết chi tiết.

   Một phương thức static có thể được gọi trên lớp (chẳng hạn như ``C.f()``) hoặc trên một thể hiện (chẳng hạn như ``C().f()``). Ngoài ra, phương thức static :term:`descriptor` cũng có thể được gọi, vì vậy nó có thể được sử dụng trong định nghĩa lớp (chẳng hạn như ``f()``).

   Các phương thức static trong Python tương tự như các phương thức trong Java hoặc C++. Ngoài ra, hãy xem
   :deco:`classmethod` để biết một biến thể hữu ích trong việc tạo các hàm khởi tạo lớp thay thế.

   Giống như mọi decorator, bạn cũng có thể gọi ``staticmethod`` như một hàm thông thường và thực hiện điều gì đó với kết quả của nó. Điều này cần thiết trong một số trường hợp khi bạn cần tham chiếu đến một hàm từ phần thân lớp và muốn tránh việc tự động chuyển đổi hàm đó thành phương thức instance. Trong những trường hợp này, hãy sử dụng thành ngữ này::

      def regular_function():
          ...

      class C:
          method = staticmethod(regular_function)

   Để biết thêm thông tin về các phương thức static, xem :ref:`types`.

   .. versionchanged:: 3.10
      Các phương thức static hiện kế thừa các thuộc tính của phương thức (:attr:`~function.__module__`, :attr:`~function.__name__`,
      :attr:`~function.__qualname__`, :attr:`~function.__doc__` và
      :attr:`~function.__annotations__`), có thuộc tính ``__wrapped__`` mới và hiện có thể được gọi như các hàm thông thường.


.. index::
   single: string; str() (built-in function)

.. _func-str:
.. class:: str(*, encoding='utf-8', errors='strict')
           str(object) str(object, encoding, errors='strict') str(object, *, errors)
   :noindex:

   Trả về phiên bản :class:`str` của *object*. Xem :func:`str` để biết chi tiết.

   ``str`` là :term:`class` chuỗi dựng sẵn. Để biết thông tin chung về chuỗi, xem :ref:`textseq`.


.. function:: sum(iterable, /, start=0)

   Tính tổng *start* và các phần tử của một *iterable* từ trái sang phải rồi trả về tổng. Các phần tử của *iterable* thường là các số và giá trị start không được là một chuỗi.

   Trong một số trường hợp sử dụng, có những lựa chọn thay thế phù hợp cho :func:`sum`. Cách nhanh được ưu tiên để nối một chuỗi các chuỗi là gọi ``''.join(sequence)``. Để cộng các giá trị dấu phẩy động với độ chính xác mở rộng, hãy xem :func:`math.fsum`\. Để nối một chuỗi các iterable, hãy cân nhắc sử dụng
   :func:`itertools.chain`.

   .. versionchanged:: 3.8
      Tham số *start* có thể được chỉ định dưới dạng đối số từ khóa.

   .. versionchanged:: 3.12 Việc tính tổng các số thực đã chuyển sang một thuật toán
      mang lại độ chính xác cao hơn và tính giao hoán tốt hơn trên hầu hết các bản build.

   .. versionchanged:: 3.14
      Đã thêm cơ chế chuyên biệt hóa cho việc tính tổng các số phức, sử dụng cùng thuật toán như khi tính tổng các số thực.


.. class:: super()
           super(type, object_or_type=None, /)

   Trả về một proxy object ủy quyền các lệnh gọi phương thức cho một lớp cha hoặc lớp anh em của *type*. Điều này hữu ích để truy cập các phương thức kế thừa đã bị ghi đè trong một lớp.

   *object_or_type* xác định :term:`method resolution order` cần được tìm kiếm. Việc tìm kiếm bắt đầu từ lớp ngay sau *type*.

   Ví dụ, nếu :attr:`~type.__mro__` của *object_or_type* là ``D -> B -> C -> A -> object`` và giá trị của *type* là ``B``, thì :func:`super` sẽ tìm kiếm ``C -> A -> object``.

   Thuộc tính :attr:`~type.__mro__` của lớp tương ứng với *object_or_type* liệt kê thứ tự tìm kiếm để phân giải phương thức được cả
   :func:`getattr` và :func:`super` sử dụng. Thuộc tính này là động và có thể thay đổi bất cứ khi nào hệ thống phân cấp kế thừa được cập nhật.

   Nếu bỏ qua đối số thứ hai, đối tượng super được trả về sẽ không bị ràng buộc. Nếu đối số thứ hai là một object, ``isinstance(obj, type)`` phải là true. Nếu đối số thứ hai là một type, ``issubclass(type2, type)`` phải là true (điều này hữu ích cho classmethod).

   Khi được gọi trực tiếp bên trong một phương thức thông thường của một lớp, có thể bỏ qua cả hai đối số (":func:`!super` không có đối số"). Trong trường hợp này, *type* sẽ là lớp bao quanh, còn *obj* sẽ là đối số đầu tiên của hàm bao quanh ngay lập tức (thường là ``self``). (Điều này có nghĩa là :func:`!super` không có đối số
   :func:`!super` sẽ không hoạt động như mong đợi trong các hàm lồng nhau, bao gồm cả biểu thức generator, vốn ngầm tạo ra các hàm lồng nhau.)

   Có hai trường hợp sử dụng điển hình cho *super*. Trong hệ thống phân cấp lớp với kế thừa đơn, *super* có thể được dùng để tham chiếu đến các lớp cha mà không cần nêu tên chúng một cách rõ ràng, nhờ đó giúp mã dễ bảo trì hơn. Cách sử dụng này tương tự với cách dùng *super* trong các ngôn ngữ lập trình khác.

   Trường hợp sử dụng thứ hai là hỗ trợ multiple inheritance mang tính hợp tác trong môi trường thực thi động. Trường hợp sử dụng này là đặc trưng của Python và không có trong các ngôn ngữ được biên dịch tĩnh hoặc các ngôn ngữ chỉ hỗ trợ kế thừa đơn. Nhờ đó, có thể triển khai "sơ đồ hình thoi", trong đó nhiều lớp cơ sở triển khai cùng một phương thức. Thiết kế tốt yêu cầu các triển khai như vậy có cùng calling signature trong mọi trường hợp (vì thứ tự gọi được xác định tại runtime, vì thứ tự đó thích ứng với các thay đổi trong hệ thống phân cấp lớp, và vì thứ tự đó có thể bao gồm các lớp anh em chưa được biết trước khi runtime).

   Đối với cả hai trường hợp sử dụng, một lời gọi lớp cha điển hình có dạng như sau::

      class C(B):
          def method(self, arg):
              super().method(arg)    # Điều này thực hiện cùng một việc như:
                                     # super(C, self).method(arg)

   Ngoài việc tra cứu phương thức, :func:`super` cũng hoạt động với việc tra cứu thuộc tính. Một trường hợp sử dụng có thể là gọi :term:`descriptors <descriptor>` trong một lớp cha hoặc lớp anh em.

   Lưu ý rằng :func:`super` được triển khai như một phần của quá trình binding cho các tra cứu thuộc tính dạng dấu chấm tường minh như ``super().__getitem__(name)``. Nó thực hiện điều này bằng cách triển khai phương thức :meth:`~object.__getattribute__` riêng để tìm kiếm các lớp theo một thứ tự xác định, hỗ trợ kế thừa đa lớp mang tính phối hợp. Do đó, :func:`super` không được định nghĩa cho các tra cứu ngầm định sử dụng các câu lệnh hoặc toán tử như ``super()[name]``.

   Cũng lưu ý rằng, ngoài dạng không có đối số, :func:`super` không bị giới hạn trong việc sử dụng bên trong các phương thức. Dạng có hai đối số chỉ rõ chính xác các đối số và tạo ra các tham chiếu thích hợp. Dạng không có đối số chỉ hoạt động bên trong định nghĩa lớp, vì compiler điền các chi tiết cần thiết để truy xuất chính xác lớp đang được định nghĩa, đồng thời truy cập instance hiện tại đối với các phương thức thông thường.

   Để biết các gợi ý thực tế về cách thiết kế các lớp mang tính phối hợp bằng cách sử dụng
   :func:`super`, xem `hướng dẫn sử dụng super() <https://rhettinger.wordpress.com/2011/05/26/super-considered-super/>`_.

   .. versionchanged:: 3.14
     :class:`super` objects are now :mod:`pickleable <pickle>` and
      :mod:`copyable <copy>`.


.. _func-tuple:
.. class:: tuple(iterable=(), /)
   :noindex:

   Thay vì là một hàm, :class:`tuple` thực chất là một kiểu sequence bất biến, như được ghi chép trong :ref:`typesseq-tuple` và :ref:`typesseq`.


.. class:: type(object, /)
           type(name, bases, dict, /, ****kwargs)

   .. index:: pair: object; type

   Với một đối số, trả về kiểu của một *đối tượng*. Giá trị trả về là một đối tượng kiểu và thường là cùng đối tượng được trả về bởi
   :attr:`object.__class__`.

   Hàm dựng sẵn :func:`isinstance` được khuyến nghị để kiểm tra kiểu của một đối tượng, vì hàm này có tính đến các lớp con.

   Với ba đối số, trả về một đối tượng kiểu mới. Đây thực chất là dạng động của câu lệnh :keyword:`class`. Chuỗi *name* là tên lớp và trở thành thuộc tính :attr:`~type.__name__`. Tuple *bases* chứa các lớp cơ sở và trở thành
   thuộc tính :attr:`~type.__bases__`; nếu rỗng, :class:`object`, lớp cơ sở tối thượng của mọi lớp, sẽ được thêm vào. Từ điển *dict* chứa các định nghĩa thuộc tính và phương thức cho phần thân lớp; từ điển này có thể được sao chép hoặc bọc trước khi trở thành thuộc tính :attr:`~type.__dict__`. Hai câu lệnh sau tạo ra các đối tượng :class:`!type` giống hệt nhau:

      >>> class X:
      ...     a = 1
      ...
      >>> X = type('X', (), dict(a=1))

   Xem thêm:

   * :ref:`Documentation on attributes and methods on classes <class-attrs-and-methods>`.
   * :ref:`bltin-type-objects`

   Các đối số từ khóa được cung cấp cho dạng ba đối số sẽ được truyền đến cơ chế metaclass thích hợp (thường là :meth:`~object.__init_subclass__`) theo cùng cách như các từ khóa trong định nghĩa lớp (ngoại trừ *metaclass*).

   Không giống câu lệnh :keyword:`class`, dạng ba đối số không gọi phương thức ``__prepare__`` của metaclass (xem :ref:`prepare`). Hãy dùng
   :func:`types.new_class` để tạo động một lớp bằng cách sử dụng metaclass thích hợp.

   Xem thêm :ref:`class-customization`.

   .. versionchanged:: 3.6
      Các lớp con của :class:`!type` không ghi đè ``type.__new__`` có thể không còn sử dụng dạng một đối số để lấy kiểu của một đối tượng.

.. function:: vars()
              vars(object, /)

   Trả về thuộc tính :attr:`~object.__dict__` của một module, lớp, instance hoặc bất kỳ đối tượng nào khác có thuộc tính :attr:`!__dict__`.

   Các đối tượng như module và instance có thuộc tính :attr:`~object.__dict__` có thể cập nhật; tuy nhiên, các đối tượng khác có thể hạn chế việc ghi vào
   các thuộc tính :attr:`!__dict__` (ví dụ: các lớp sử dụng một
   :class:`types.MappingProxyType` để ngăn việc cập nhật trực tiếp từ điển).

   Nếu không có đối số, :func:`vars` hoạt động giống như :func:`locals`.

   Một ngoại lệ :exc:`TypeError` sẽ được phát sinh nếu một đối tượng được chỉ định nhưng không có thuộc tính :attr:`~object.__dict__` (ví dụ: nếu lớp của đối tượng đó định nghĩa thuộc tính :attr:`~object.__slots__`).

   .. versionchanged:: 3.13

      Kết quả của việc gọi hàm này không có đối số đã được cập nhật như mô tả đối với builtin :func:`locals`.


.. function:: zip(*iterables, strict=False)

   Lặp qua nhiều iterable song song, tạo ra các tuple với một phần tử từ mỗi iterable.

   Ví dụ::

      >>> for item in zip([1, 2, 3], ['sugar', 'spice', 'everything nice']):
      ...     print(item)
      ...
      (1, 'sugar')
      (2, 'spice')
      (3, 'everything nice')

   Cụ thể hơn: :func:`zip` trả về một iterator gồm các tuple, trong đó tuple thứ *i* chứa phần tử thứ *i* từ mỗi iterable đối số.

   Một cách khác để hiểu :func:`zip` là nó biến các hàng thành các cột và các cột thành các hàng. Điều này tương tự như `chuyển vị một ma trận <https://en.wikipedia.org/wiki/Transpose>`_.

   :func:`zip` hoạt động theo cơ chế lazy: Các phần tử sẽ không được xử lý cho đến khi iterable được lặp qua, chẳng hạn bằng vòng :keyword:`!for` hoặc bằng cách bọc trong một
   :class:`list`.

   Một điều cần cân nhắc là các iterable được truyền vào :func:`zip` có thể có độ dài khác nhau; đôi khi là có chủ ý, đôi khi là do lỗi trong mã chuẩn bị các iterable này. Python cung cấp ba cách tiếp cận khác nhau để xử lý vấn đề này:

   * Theo mặc định, :func:`zip` dừng khi iterable ngắn nhất đã :term:`exhausted`. Nó sẽ bỏ qua các phần tử còn lại trong những iterable dài hơn, cắt kết quả để có độ dài bằng iterable ngắn nhất::

        >>> list(zip(range(3), ['fee', 'fi', 'fo', 'fum']))
        [(0, 'fee'), (1, 'fi'), (2, 'fo')]

   * :func:`zip` thường được sử dụng khi giả định rằng các iterable có cùng độ dài. Trong những trường hợp như vậy, bạn nên sử dụng tùy chọn ``strict=True``. Kết quả của nó giống với :func:`zip` thông thường::

        >>> list(zip(('a', 'b', 'c'), (1, 2, 3), strict=True))
        [('a', 1), ('b', 2), ('c', 3)]

     Không giống hành vi mặc định, nó sẽ raise một :exc:`ValueError` nếu một iterable :term:`exhausted` trước các iterable khác:

        >>> for item in zip(range(3), ['fee', 'fi', 'fo', 'fum'], strict=True):  # doctest: +SKIP
        ...     print(item)
        ...
        (0, 'fee')
        (1, 'fi')
        (2, 'fo')
        Traceback (most recent call last):
          ...
        ValueError: zip() argument 2 is longer than argument 1

     ..
        Doctest này bị vô hiệu hóa vì doctest không hỗ trợ việc thu thập đầu ra và ngoại lệ trong cùng một đơn vị mã. https://github.com/python/cpython/issues/65382

     Nếu không có đối số ``strict=True``, mọi lỗi dẫn đến các iterable có độ dài khác nhau sẽ bị bỏ qua, và có thể biểu hiện thành một lỗi khó phát hiện ở một phần khác của chương trình.

   * Các iterable ngắn hơn có thể được bổ sung bằng một giá trị hằng để tất cả các iterable có cùng độ dài. Việc này được thực hiện bằng cách
     :func:`itertools.zip_longest`.

   Các trường hợp biên: Với một đối số iterable duy nhất, :func:`zip` trả về một iterator gồm các tuple 1 phần tử. Không có đối số, hàm trả về một iterator rỗng.

   Mẹo và thủ thuật:

   * Thứ tự đánh giá các iterable từ trái sang phải được đảm bảo. Điều này cho phép sử dụng một cách viết để gom một chuỗi dữ liệu thành các nhóm có độ dài n bằng ``zip(*[iter(s)]*n, strict=True)``. Cách này lặp lại iterator *same* ``n`` lần để mỗi tuple đầu ra chứa kết quả của ``n`` lần gọi iterator. Nhờ đó, đầu vào được chia thành các đoạn có độ dài n.

   * Có thể sử dụng :func:`zip` kết hợp với toán tử ``*`` để giải nén một danh sách::

        >>> x = [1, 2, 3]
        >>> y = [4, 5, 6]
        >>> list(zip(x, y))
        [(1, 4), (2, 5), (3, 6)]
        >>> x2, y2 = zip(*zip(x, y))
        >>> x == list(x2) and y == list(y2)
        True

   .. versionchanged:: 3.10
      Đã thêm đối số ``strict``.


.. function:: __import__(name, globals=None, locals=None, fromlist=(), level=0)

   .. index::
      pair: statement; import
      pair: module; builtins

   .. note::

      Đây là một hàm nâng cao không cần thiết trong lập trình Python hằng ngày, không giống như :func:`importlib.import_module`.

   Hàm này được gọi bởi câu lệnh :keyword:`import`. Có thể thay thế hàm này (bằng cách import module :mod:`builtins` và gán cho ``builtins.__import__``) để thay đổi ngữ nghĩa của
   câu lệnh :keyword:`!import`, nhưng việc này **rất** không được khuyến khích vì thường sử dụng import hooks (xem :pep:`302`) sẽ đơn giản hơn để đạt được các mục tiêu tương tự và không gây ra vấn đề với mã giả định rằng implementation mặc định của import đang được sử dụng. Việc sử dụng trực tiếp :func:`__import__` cũng không được khuyến khích; thay vào đó nên dùng :func:`importlib.import_module`.

   Hàm này import module *name*, có thể sử dụng *globals* và *locals* được cung cấp để xác định cách diễn giải tên trong ngữ cảnh package. *fromlist* cung cấp tên của các đối tượng hoặc submodule cần được import từ module được chỉ định bởi *name*. Implementation tiêu chuẩn hoàn toàn không sử dụng đối số *locals* và chỉ sử dụng *globals* để xác định ngữ cảnh package của câu lệnh :keyword:`import`.

   *level* chỉ định việc sử dụng import tuyệt đối hay tương đối. ``0`` (mặc định) có nghĩa là chỉ thực hiện import tuyệt đối. Các giá trị dương của *level* cho biết số lượng thư mục cha cần tìm kiếm, tính tương đối với thư mục của module gọi :func:`__import__` (xem :pep:`328` để biết chi tiết).

   Khi biến *name* có dạng ``package.module``, thông thường, package cấp cao nhất (tên tính đến dấu chấm đầu tiên) được trả về, *không* phải module có tên *name*. Tuy nhiên, khi cung cấp đối số *fromlist* không rỗng, module có tên *name* sẽ được trả về.

   Ví dụ, câu lệnh ``import spam`` cho ra bytecode tương tự như đoạn mã sau::

      spam = __import__('spam', globals(), locals(), [], 0)

   Câu lệnh ``import spam.ham`` cho ra lời gọi này::

      spam = __import__('spam.ham', globals(), locals(), [], 0)

   Lưu ý rằng :func:`__import__` trả về module toplevel ở đây vì đây là đối tượng được liên kết với một tên bằng câu lệnh :keyword:`import`.

   Mặt khác, câu lệnh ``from spam.ham import eggs, sausage as saus`` cho ra::

      _temp = __import__('spam.ham', globals(), locals(), ['eggs', 'sausage'], 0)
      eggs = _temp.eggs
      saus = _temp.sausage

   Ở đây, module ``spam.ham`` được trả về từ :func:`__import__`. Từ đối tượng này, các tên cần import được truy xuất và gán cho các tên tương ứng.

   Nếu chỉ muốn import một module (có thể nằm trong một package) theo tên, hãy sử dụng :func:`importlib.import_module`.

   .. versionchanged:: 3.3
      Các giá trị âm cho *level* không còn được hỗ trợ (điều này cũng thay đổi giá trị mặc định thành 0).

   .. versionchanged:: 3.9
      Khi đang sử dụng các tùy chọn dòng lệnh :option:`-E` hoặc :option:`-I`, biến môi trường :envvar:`PYTHONCASEOK` hiện sẽ bị bỏ qua.

.. rubric:: Chú thích cuối trang

.. [#] Lưu ý rằng trình phân tích cú pháp chỉ chấp nhận quy ước kết thúc dòng kiểu Unix. Nếu bạn đang đọc mã từ một tệp, hãy nhớ sử dụng chế độ chuyển đổi dòng mới để chuyển đổi các dòng mới kiểu Windows hoặc Mac.

.. _`guide to using super()`: https://rhettinger.wordpress.com/2011/05/26/super-considered-super/
.. _`transposing a matrix`: https://en.wikipedia.org/wiki/Transpose
