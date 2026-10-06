:mod:`!ctypes` --- Thư viện hàm ngoại cho Python
================================================

.. module:: ctypes
   :synopsis: Thư viện hàm ngoại cho Python.

.. moduleauthor:: Thomas Heller <theller@python.net>

**Mã nguồn:** :source:`Lib/ctypes`

--------------

:mod:`!ctypes` là một thư viện hàm ngoại cho Python. Thư viện này cung cấp các kiểu dữ liệu tương thích với C và cho phép gọi các hàm trong DLL hoặc shared library. Bạn có thể dùng thư viện này để bọc các thư viện đó bằng Python thuần.

.. include:: ../includes/optional-module.rst

.. warning::

   :mod:`!ctypes` cung cấp quyền truy cập cấp thấp vào các thư viện native và bộ nhớ của tiến trình, bỏ qua các cơ chế an toàn của Python và cho phép thực thi mã native tùy ý. Việc sử dụng không đúng cách có thể làm hỏng dữ liệu và đối tượng, làm lộ thông tin nhạy cảm, gây sự cố hoặc bằng cách khác xâm phạm tiến trình đang chạy.


.. _ctypes-ctypes-tutorial:

Hướng dẫn ctypes
----------------

Lưu ý: Một số mẫu mã tham chiếu đến kiểu :class:`c_int` của ctypes. Trên các nền tảng mà ``sizeof(long) == sizeof(int)`` thì nó là bí danh của :class:`c_long`. Vì vậy, bạn không nên bối rối nếu :class:`c_long` được in ra khi bạn mong đợi
:class:`c_int` --- thực ra chúng là cùng một kiểu.

.. _ctypes-loading-dynamic-link-libraries:

Nạp thư viện liên kết động
^^^^^^^^^^^^^^^^^^^^^^^^^^

:mod:`!ctypes` xuất :py:data:`~ctypes.cdll`, và trên Windows
các đối tượng :py:data:`~ctypes.windll` và :py:data:`~ctypes.oledll`, dùng để nạp thư viện liên kết động.

Bạn nạp các thư viện bằng cách truy cập chúng dưới dạng thuộc tính của các đối tượng này.
:py:data:`!cdll` nạp các thư viện xuất các hàm sử dụng quy ước gọi ``cdecl`` tiêu chuẩn, trong khi các thư viện :py:data:`!windll` gọi các hàm bằng quy ước gọi ``stdcall``.
:py:data:`~oledll` cũng sử dụng quy ước gọi ``stdcall`` và giả định rằng các hàm trả về mã lỗi :c:type:`!HRESULT` của Windows. Mã lỗi này được dùng để tự động phát sinh ngoại lệ :class:`OSError` khi lệnh gọi hàm thất bại.

.. versionchanged:: 3.3
   Các lỗi của Windows trước đây thường phát sinh :exc:`WindowsError`, hiện là bí danh của :exc:`OSError`.


Dưới đây là một số ví dụ dành cho Windows. Lưu ý rằng ``msvcrt`` là thư viện C chuẩn của MS, chứa hầu hết các hàm C chuẩn và sử dụng quy ước gọi ``cdecl``.::

   >>> from ctypes import *
   >>> print(windll.kernel32)  # doctest: +WINDOWS
   <WinDLL 'kernel32', handle ... at ...>
   >>> print(cdll.msvcrt)      # doctest: +WINDOWS
   <CDLL 'msvcrt', handle ... at ...>
   >>> libc = cdll.msvcrt      # doctest: +WINDOWS
   >>>

Windows tự động thêm hậu tố tệp ``.dll`` thông thường.

.. note::
    Việc truy cập thư viện C chuẩn thông qua ``cdll.msvcrt`` sẽ sử dụng một phiên bản thư viện đã lỗi thời, có thể không tương thích với phiên bản mà Python đang sử dụng. Khi có thể, hãy dùng chức năng gốc của Python; nếu không, hãy import và sử dụng module ``msvcrt``.

Các hệ thống khác yêu cầu tên tệp *bao gồm* phần mở rộng để tải một thư viện, vì vậy không thể sử dụng truy cập thuộc tính để tải thư viện. Bạn có thể dùng
phương thức :meth:`~LibraryLoader.LoadLibrary` của các trình tải dll, hoặc tải thư viện bằng cách tạo một instance của :py:class:`CDLL` bằng cách gọi constructor.

Ví dụ, trên Linux::

   >>> cdll.LoadLibrary("libc.so.6")  # doctest: +LINUX
   <CDLL 'libc.so.6', handle ... at ...>
   >>> libc = CDLL("libc.so.6")       # doctest: +LINUX
   >>> libc                           # doctest: +LINUX
   <CDLL 'libc.so.6', handle ... at ...>
   >>>

Trên macOS::

   >>> cdll.LoadLibrary("libc.dylib")  # doctest: +MACOS
   <CDLL 'libc.dylib', handle ... at ...>
   >>> libc = CDLL("libc.dylib")       # doctest: +MACOS
   >>> libc                            # doctest: +MACOS
   <CDLL 'libc.dylib', handle ... at ...>



.. _ctypes-accessing-functions-from-loaded-dlls:

Truy cập các hàm từ các DLL đã tải
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Có thể truy cập các hàm dưới dạng thuộc tính của các đối tượng DLL::

   >>> libc.printf
   <_FuncPtr object at 0x...>
   >>> print(windll.kernel32.GetModuleHandleA)  # doctest: +WINDOWS
   <_FuncPtr object at 0x...>
   >>> print(windll.kernel32.MyOwnFunction)     # doctest: +WINDOWS
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "ctypes.py", line 239, in __getattr__
       func = _StdcallFuncPtr(name, self)
   AttributeError: function 'MyOwnFunction' not found
   >>>

Lưu ý rằng các system dll của win32 như ``kernel32`` và ``user32`` thường export cả phiên bản ANSI lẫn UNICODE của một hàm. Phiên bản UNICODE được export với ``W`` nối vào tên, còn phiên bản ANSI được export với ``A`` nối vào tên. Hàm win32 ``GetModuleHandle``, trả về *module handle* cho tên module đã cho, có prototype C sau đây, và một macro được dùng để expose một trong hai phiên bản dưới dạng ``GetModuleHandle``, tùy thuộc vào việc UNICODE có được định nghĩa hay không::

   /* ANSI version */
   HMODULE GetModuleHandleA(LPCSTR lpModuleName);
   /* UNICODE version */
   HMODULE GetModuleHandleW(LPCWSTR lpModuleName);

*windll* không cố gắng tự động chọn một trong hai phiên bản; bạn phải truy cập phiên bản cần dùng bằng cách chỉ định rõ ràng ``GetModuleHandleA`` hoặc ``GetModuleHandleW``, sau đó gọi phiên bản đó lần lượt bằng các đối tượng bytes hoặc string.

Đôi khi, dll export các hàm có tên không phải là các Python identifier hợp lệ, chẳng hạn như ``"??2@YAPAXI@Z"``. Trong trường hợp này, bạn phải sử dụng
:func:`getattr` để lấy hàm::

   >>> getattr(cdll.msvcrt, "??2@YAPAXI@Z")  # doctest: +WINDOWS
   <_FuncPtr object at 0x...>
   >>>

Trên Windows, một số dll export các hàm không theo tên mà theo ordinal. Có thể truy cập các hàm này bằng cách lập chỉ mục đối tượng dll với số ordinal::

   >>> cdll.kernel32[1]  # doctest: +WINDOWS
   <_FuncPtr object at 0x...>
   >>> cdll.kernel32[0]  # doctest: +WINDOWS
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "ctypes.py", line 310, in __getitem__
       func = _StdcallFuncPtr(name, self)
   AttributeError: function ordinal 0 not found
   >>>


.. _ctypes-calling-functions:

Gọi hàm
^^^^^^^

Bạn có thể gọi các hàm này như mọi đối tượng có thể gọi khác trong Python. Ví dụ này sử dụng hàm ``rand()``, hàm không nhận đối số nào và trả về một số nguyên giả ngẫu nhiên::

   >>> print(libc.rand())  # doctest: +SKIP
   1804289383

Trên Windows, bạn có thể gọi hàm ``GetModuleHandleA()``, hàm này trả về một handle của module win32 (truyền ``None`` làm đối số duy nhất để gọi hàm với một con trỏ ``NULL``)::

   >>> print(hex(windll.kernel32.GetModuleHandleA(None)))  # doctest: +WINDOWS
   0x1d000000
   >>>

:exc:`ValueError` được phát sinh khi bạn gọi một hàm ``stdcall`` với quy ước gọi ``cdecl``, hoặc ngược lại::

   >>> cdll.kernel32.GetModuleHandleA(None)  # doctest: +WINDOWS
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   ValueError: Procedure probably called with not enough arguments (4 bytes missing)
   >>>

   >>> windll.msvcrt.printf(b"spam")  # doctest: +WINDOWS
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   ValueError: Procedure probably called with too many arguments (4 bytes in excess)
   >>>

Để tìm ra quy ước gọi chính xác, bạn phải xem tệp header C hoặc tài liệu về hàm mà bạn muốn gọi.

Trên Windows, :mod:`!ctypes` sử dụng cơ chế xử lý ngoại lệ có cấu trúc của win32 để ngăn sự cố do lỗi bảo vệ chung khi các hàm được gọi với các giá trị đối số không hợp lệ::

   >>> windll.kernel32.GetModuleHandleA(32)  # doctest: +WINDOWS
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   OSError: exception: access violation reading 0x00000020
   >>>

Mô-đun :mod:`faulthandler` có thể giúp gỡ lỗi các sự cố, chẳng hạn như lỗi phân đoạn do các lệnh gọi thư viện C sai gây ra.

``None``, các số nguyên, đối tượng bytes và chuỗi (unicode) là những đối tượng Python native duy nhất có thể được sử dụng trực tiếp làm tham số trong các lệnh gọi hàm này. ``None`` được truyền dưới dạng con trỏ ``NULL`` C, các đối tượng bytes và chuỗi được truyền dưới dạng con trỏ đến khối bộ nhớ chứa dữ liệu của chúng (:c:expr:`char *` hoặc
:c:expr:`wchar_t *`).  Các số nguyên Python được truyền dưới dạng kiểu C mặc định của nền tảng
:c:expr:`int` kiểu, giá trị của chúng được che để vừa với kiểu C.

Trước khi chuyển sang việc gọi hàm với các kiểu tham số khác, chúng ta cần tìm hiểu thêm về :mod:`!ctypes` các kiểu dữ liệu.


.. _ctypes-fundamental-data-types:

Các kiểu dữ liệu cơ bản
^^^^^^^^^^^^^^^^^^^^^^^

:mod:`!ctypes` định nghĩa một số kiểu dữ liệu C nguyên thủy tương thích:

.. list-table::
   :header-rows: 1

   * - kiểu ctypes
     - kiểu C
     - Kiểu Python
     - :py:attr:`~_SimpleCData._type_`
   * - :class:`c_bool`
     - :c:expr:`_Bool`
     - :py:class:`bool`
     - ``'?'``
   * - :class:`c_char`
     - :c:expr:`char`
     - :py:class:`bytes` 1 ký tự
     - ``'c'``
   * - :class:`c_wchar`
     - :c:type:`wchar_t`
     - :py:class:`str` 1 ký tự
     - ``'u'``
   * - :class:`c_byte`
     - :c:expr:`char`
     - :py:class:`int`
     - ``'b'``
   * - :class:`c_ubyte`
     - :c:expr:`unsigned char`
     - :py:class:`int`
     - ``'B'``
   * - :class:`c_short`
     - :c:expr:`short`
     - :py:class:`int`
     - ``'h'``
   * - :class:`c_ushort`
     - :c:expr:`unsigned short`
     - :py:class:`int`
     - ``'H'``
   * - :class:`c_int`
     - :c:expr:`int`
     - :py:class:`int`
     - ``'i'`` \*
   * - :class:`c_int8`
     - :c:type:`int8_t`
     - :py:class:`int`
     - \*
   * - :class:`c_int16`
     - :c:type:`int16_t`
     - :py:class:`int`
     - \*
   * - :class:`c_int32`
     - :c:type:`int32_t`
     - :py:class:`int`
     - \*
   * - :class:`c_int64`
     - :c:type:`int64_t`
     - :py:class:`int`
     - \*
   * - :class:`c_uint`
     - :c:expr:`unsigned int`
     - :py:class:`int`
     - ``'I'`` \*
   * - :class:`c_uint8`
     - :c:type:`uint8_t`
     - :py:class:`int`
     - \*
   * - :class:`c_uint16`
     - :c:type:`uint16_t`
     - :py:class:`int`
     - \*
   * - :class:`c_uint32`
     - :c:type:`uint32_t`
     - :py:class:`int`
     - \*
   * - :class:`c_uint64`
     - :c:type:`uint64_t`
     - :py:class:`int`
     - \*
   * - :class:`c_long`
     - :c:expr:`long`
     - :py:class:`int`
     - ``'l'``
   * - :class:`c_ulong`
     - :c:expr:`unsigned long`
     - :py:class:`int`
     - ``'L'``
   * - :class:`c_longlong`
     - :c:expr:`long long`
     - :py:class:`int`
     - ``'q'`` \*
   * - :class:`c_ulonglong`
     - :c:expr:`unsigned long long`
     - :py:class:`int`
     - ``'Q'`` \*
   * - :class:`c_size_t`
     - :c:type:`size_t`
     - :py:class:`int`
     - \*
   * - :class:`c_ssize_t`
     - :c:type:`Py_ssize_t`
     - :py:class:`int`
     - \*
   * - :class:`c_time_t`
     - :c:type:`time_t`
     - :py:class:`int`
     - \*
   * - :class:`c_float`
     - :c:expr:`float`
     - :py:class:`float`
     - ``'f'``
   * - :class:`c_double`
     - :c:expr:`double`
     - :py:class:`float`
     - ``'d'``
   * - :class:`c_longdouble`
     - :c:expr:`long double`
     - :py:class:`float`
     - ``'g'`` \*
   * - :class:`c_char_p`
     - :c:expr:`char *` (kết thúc bằng NUL)
     - :py:class:`bytes` hoặc ``None``
     - ``'z'``
   * - :class:`c_wchar_p`
     - :c:expr:`wchar_t *` (kết thúc bằng NUL)
     - :py:class:`str` hoặc ``None``
     - ``'Z'``
   * - :class:`c_void_p`
     - :c:expr:`void *`
     - :py:class:`int` hoặc ``None``
     - ``'P'``
   * - :class:`py_object`
     - :c:expr:`PyObject *`
     - :py:class:`object`
     - ``'O'``
   * - :ref:`VARIANT_BOOL <ctypes-wintypes>`
     - :c:expr:`short int`
     - :py:class:`bool`
     - ``'v'``

Ngoài ra, nếu phép tính số phức tương thích với IEC 60559 (Phụ lục G) được hỗ trợ ở cả C và ``libffi``, thì các kiểu số phức sau đây sẽ khả dụng:

.. list-table::
   :header-rows: 1

   * - kiểu ctypes
     - kiểu C
     - Kiểu Python
     - :py:attr:`~_SimpleCData._type_`
   * - :class:`c_float_complex`
     - :c:expr:`float complex`
     - :py:class:`complex`
     - ``'F'``
   * - :class:`c_double_complex`
     - :c:expr:`double complex`
     - :py:class:`complex`
     - ``'D'``
   * - :class:`c_longdouble_complex`
     - :c:expr:`long double complex`
     - :py:class:`complex`
     - ``'G'``


Tất cả các kiểu này có thể được tạo bằng cách gọi chúng với một trình khởi tạo tùy chọn có đúng kiểu và giá trị::

   >>> c_int()
   c_long(0)
   >>> c_wchar_p("Hello, World")
   c_wchar_p(140018365411392)
   >>> c_ushort(-3)
   c_ushort(65533)
   >>>

Các hàm khởi tạo cho các kiểu số sẽ chuyển đổi dữ liệu đầu vào bằng
:py:meth:`~object.__bool__`,
:py:meth:`~object.__index__` (đối với ``int``),
:py:meth:`~object.__float__` hoặc :py:meth:`~object.__complex__`. Điều này có nghĩa là :py:class:`~ctypes.c_bool` chấp nhận bất kỳ đối tượng nào có giá trị logic::

   >>> empty_list = []
   >>> c_bool(empty_list)
   c_bool(False)

Vì các kiểu này có thể thay đổi, nên giá trị của chúng cũng có thể được thay đổi sau đó::

   >>> i = c_int(42)
   >>> print(i)
   c_long(42)
   >>> print(i.value)
   42
   >>> i.value = -99
   >>> print(i.value)
   -99
   >>>

Việc gán một giá trị mới cho các thể hiện của các kiểu con trỏ :class:`c_char_p`,
:class:`c_wchar_p`, và :class:`c_void_p` sẽ thay đổi *vị trí bộ nhớ* mà chúng trỏ tới, *chứ không phải nội dung* của khối bộ nhớ (dĩ nhiên là không, vì các đối tượng chuỗi Python là bất biến)::

   >>> s = "Hello, World"
   >>> c_s = c_wchar_p(s)
   >>> print(c_s)
   c_wchar_p(139966785747344)
   >>> print(c_s.value)
   Hello World
   >>> c_s.value = "Hi, there"
   >>> print(c_s)              # vị trí bộ nhớ đã thay đổi
   c_wchar_p(139966783348904)
   >>> print(c_s.value)
   Hi, there
   >>> print(s)                # đối tượng đầu tiên không thay đổi
   Hello, World
   >>>

Tuy nhiên, bạn nên cẩn thận không truyền chúng cho các hàm mong đợi con trỏ đến vùng nhớ có thể thay đổi. Nếu cần các khối vùng nhớ có thể thay đổi, ctypes có một
:func:`create_string_buffer` tạo các khối này theo nhiều cách khác nhau. Có thể truy cập (hoặc thay đổi) nội dung của khối vùng nhớ hiện tại bằng thuộc tính ``raw``; nếu muốn truy cập khối này dưới dạng chuỗi kết thúc bằng NUL, hãy sử dụng thuộc tính ``value``::

   >>> from ctypes import *
   >>> p = create_string_buffer(3)            # tạo bộ đệm 3 byte, được khởi tạo bằng các byte NUL
   >>> print(sizeof(p), repr(p.raw))
   3 b'\x00\x00\x00'
   >>> p = create_string_buffer(b"Hello")     # tạo bộ đệm chứa chuỗi kết thúc bằng NUL
   >>> print(sizeof(p), repr(p.raw))
   6 b'Hello\x00'
   >>> print(repr(p.value))
   b'Hello'
   >>> p = create_string_buffer(b"Hello", 10) # tạo bộ đệm 10 byte
   >>> print(sizeof(p), repr(p.raw))
   10 b'Hello\x00\x00\x00\x00\x00'
   >>> p.value = b"Hi"
   >>> print(sizeof(p), repr(p.raw))
   10 b'Hi\x00lo\x00\x00\x00\x00\x00'
   >>>

Hàm :func:`create_string_buffer` thay thế cho hàm :func:`!c_buffer` cũ (hàm này vẫn khả dụng dưới dạng bí danh). Để tạo một khối vùng nhớ có thể thay đổi chứa các ký tự unicode thuộc kiểu C :c:type:`wchar_t`, hãy sử dụng
:func:`create_unicode_buffer` hàm.


.. _ctypes-calling-functions-continued:

Tiếp tục gọi hàm
^^^^^^^^^^^^^^^^

Lưu ý rằng printf in ra kênh đầu ra tiêu chuẩn thực, *không* đến
:data:`sys.stdout`, vì vậy các ví dụ này chỉ hoạt động tại lời nhắc của console, không phải bên trong *IDLE* hoặc *PythonWin*::

   >>> printf = libc.printf
   >>> printf(b"Hello, %s\n", b"World!")
   Hello, World!
   14
   >>> printf(b"Hello, %S\n", "World!")
   Hello, World!
   14
   >>> printf(b"%d bottles of beer\n", 42)
   42 bottles of beer
   19
   >>> printf(b"%f bottles of beer\n", 42.5)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   ctypes.ArgumentError: argument 2: TypeError: Don't know how to convert parameter 2
   >>>

Như đã đề cập trước đây, tất cả các kiểu Python ngoại trừ số nguyên, chuỗi và đối tượng bytes đều phải được bọc trong kiểu :mod:`!ctypes` tương ứng của chúng để có thể được chuyển đổi thành kiểu dữ liệu C cần thiết::

   >>> printf(b"An int %d, a double %f\n", 1234, c_double(3.14))
   An int 1234, a double 3.140000
   31
   >>>

.. _ctypes-calling-variadic-functions:

Gọi các hàm variadic
^^^^^^^^^^^^^^^^^^^^

Trên nhiều nền tảng, việc gọi các hàm variadic thông qua ctypes hoàn toàn giống với việc gọi các hàm có số lượng tham số cố định. Trên một số nền tảng, đặc biệt là ARM64 cho Apple Platforms, calling convention của các hàm variadic khác với các hàm thông thường.

Trên các nền tảng đó, bắt buộc phải chỉ định thuộc tính :attr:`~_CFuncPtr.argtypes` cho các đối số hàm thông thường, không biến thiên:

.. code-block:: python3

   libc.printf.argtypes = [ctypes.c_char_p]

Vì việc chỉ định thuộc tính này không cản trở tính khả chuyển, nên khuyến nghị luôn chỉ định :attr:`~_CFuncPtr.argtypes` cho mọi hàm variadic.


.. _ctypes-calling-functions-with-own-custom-data-types:

Gọi các hàm bằng kiểu dữ liệu tùy chỉnh của riêng bạn
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Bạn cũng có thể tùy chỉnh việc chuyển đổi đối số :mod:`!ctypes` để cho phép các instance của lớp riêng được sử dụng làm đối số hàm. :mod:`!ctypes` tìm kiếm một
thuộc tính :attr:`!_as_parameter_` và sử dụng thuộc tính này làm đối số hàm. Thuộc tính phải là số nguyên, chuỗi, bytes, một instance :mod:`!ctypes`, hoặc một đối tượng có thuộc tính :attr:`!_as_parameter_`::

   >>> class Bottles:
   ...     def __init__(self, number):
   ...         self._as_parameter_ = number
   ...
   >>> bottles = Bottles(42)
   >>> printf(b"%d bottles of beer\n", bottles)
   42 bottles of beer
   19
   >>>

Nếu không muốn lưu dữ liệu của instance trong biến instance :attr:`!_as_parameter_`, bạn có thể định nghĩa một :deco:`property` để cung cấp thuộc tính này khi được yêu cầu.


.. _ctypes-specifying-required-argument-types:

Chỉ định các kiểu đối số bắt buộc (prototype hàm)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Có thể chỉ định các kiểu đối số bắt buộc của những hàm được export từ DLL bằng cách thiết lập thuộc tính :attr:`~_CFuncPtr.argtypes`.

:attr:`~_CFuncPtr.argtypes` phải là một chuỗi các kiểu dữ liệu C (hàm :func:`!printf` có lẽ không phải là ví dụ phù hợp ở đây, vì nó nhận số lượng và kiểu tham số khác nhau tùy thuộc vào chuỗi định dạng; mặt khác, đây là cách khá tiện để thử nghiệm tính năng này)::

   >>> printf.argtypes = [c_char_p, c_char_p, c_int, c_double]
   >>> printf(b"String '%s', Int %d, Double %f\n", b"Hi", 10, 2.2)
   String 'Hi', Int 10, Double 2.200000
   37
   >>>

Việc chỉ định một format giúp bảo vệ khỏi các kiểu đối số không tương thích (giống như prototype của một hàm C) và cố gắng chuyển đổi các đối số sang những kiểu hợp lệ::

   >>> printf(b"%d %d %d", 1, 2, 3)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   ctypes.ArgumentError: argument 2: TypeError: 'int' object cannot be interpreted as ctypes.c_char_p
   >>> printf(b"%s %d %f\n", b"X", 2, 3)
   X 2 3.000000
   13
   >>>

Nếu bạn đã định nghĩa các class của riêng mình và truyền chúng vào các lệnh gọi hàm, bạn phải triển khai một class method :meth:`~_CData.from_param` để có thể sử dụng chúng trong chuỗi :attr:`~_CFuncPtr.argtypes`. Class method :meth:`~_CData.from_param` nhận object Python được truyền vào lệnh gọi hàm; method này phải thực hiện kiểm tra kiểu hoặc bất kỳ thao tác cần thiết nào để bảo đảm object này có thể chấp nhận được, sau đó trả về chính object đó, thuộc tính :attr:`!_as_parameter_` của nó hoặc bất kỳ giá trị nào bạn muốn truyền làm đối số cho hàm C trong trường hợp này. Một lần nữa, kết quả phải là một số nguyên, chuỗi, bytes, một instance :mod:`!ctypes` hoặc một object có
thuộc tính :attr:`!_as_parameter_`.


.. _ctypes-return-types:

Kiểu giá trị trả về
^^^^^^^^^^^^^^^^^^^

.. testsetup::

   from ctypes import CDLL, c_char, c_char_p
   from ctypes.util import find_library
   libc = CDLL(find_library('c'))
   strchr = libc.strchr


Theo mặc định, các hàm được giả định là trả về kiểu C :c:expr:`int`. Có thể chỉ định các kiểu giá trị trả về khác bằng cách thiết lập thuộc tính :attr:`~_CFuncPtr.restype` của function object.

Nguyên mẫu C của :c:func:`time` là ``time_t time(time_t *)``. Vì :c:type:`time_t` có thể có kiểu khác với kiểu trả về mặc định :c:expr:`int`, bạn nên chỉ định thuộc tính :attr:`!restype`::

   >>> libc.time.restype = c_time_t

Có thể chỉ định các kiểu đối số bằng :attr:`~_CFuncPtr.argtypes`::

   >>> libc.time.argtypes = (POINTER(c_time_t),)

Để gọi hàm với một con trỏ ``NULL`` làm đối số đầu tiên, hãy sử dụng ``None``::

   >>> print(libc.time(None))  # doctest: +SKIP
   1150640792

Đây là một ví dụ nâng cao hơn, sử dụng hàm :func:`!strchr`, hàm này nhận một con trỏ chuỗi và một char, đồng thời trả về một con trỏ tới chuỗi::

   >>> strchr = libc.strchr
   >>> strchr(b"abcdef", ord("d"))  # doctest: +SKIP
   8059983
   >>> strchr.restype = c_char_p    # c_char_p là một con trỏ tới chuỗi
   >>> strchr(b"abcdef", ord("d"))
   b'def'
   >>> print(strchr(b"abcdef", ord("x")))
   None
   >>>

Nếu bạn muốn tránh các lần gọi :func:`ord("x") <ord>` ở trên, bạn có thể đặt
thuộc tính :attr:`~_CFuncPtr.argtypes`, và đối số thứ hai sẽ được chuyển đổi từ một đối tượng bytes Python một ký tự thành một char C:

.. doctest::

   >>> strchr.restype = c_char_p
   >>> strchr.argtypes = [c_char_p, c_char]
   >>> strchr(b"abcdef", b"d")
   b'def'
   >>> strchr(b"abcdef", b"def")
   Traceback (most recent call last):
   ctypes.ArgumentError: argument 2: TypeError: one character bytes, bytearray or integer expected
   >>> print(strchr(b"abcdef", b"x"))
   None
   >>> strchr(b"abcdef", b"d")
   b'def'
   >>>

Bạn cũng có thể sử dụng một đối tượng Python có thể gọi (ví dụ như một hàm hoặc một lớp) làm thuộc tính :attr:`~_CFuncPtr.restype`, nếu hàm foreign trả về một số nguyên. Đối tượng có thể gọi sẽ được gọi với *số nguyên* mà hàm C trả về, và kết quả của lần gọi này sẽ được dùng làm kết quả của lần gọi hàm của bạn. Điều này hữu ích để kiểm tra các giá trị trả về biểu thị lỗi và tự động phát sinh một exception::

   >>> GetModuleHandle = windll.kernel32.GetModuleHandleA  # doctest: +WINDOWS
   >>> def ValidHandle(value):
   ...     if value == 0:
   ...         raise WinError()
   ...     return value
   ...
   >>>
   >>> GetModuleHandle.restype = ValidHandle  # doctest: +WINDOWS
   >>> GetModuleHandle(None)  # doctest: +WINDOWS
   486539264
   >>> GetModuleHandle("something silly")  # doctest: +WINDOWS
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "<stdin>", line 3, in ValidHandle
   OSError: [Errno 126] The specified module could not be found.
   >>>

``WinError`` là một hàm sẽ gọi API Windows ``FormatMessage()`` để lấy biểu diễn chuỗi của một mã lỗi, và *returns* một exception. ``WinError`` nhận một tham số mã lỗi tùy chọn; nếu không sử dụng tham số này, nó sẽ gọi
:func:`GetLastError` để truy xuất mã đó.

Xin lưu ý rằng một cơ chế kiểm tra lỗi mạnh hơn nhiều có sẵn thông qua thuộc tính :attr:`~_CFuncPtr.errcheck`; hãy xem tài liệu tham khảo để biết chi tiết.


.. _ctypes-passing-pointers:

Truyền con trỏ (hay: truyền tham số bằng tham chiếu)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Đôi khi một hàm API C yêu cầu một *pointer* đến một kiểu dữ liệu làm tham số, có thể để ghi vào vị trí tương ứng hoặc vì dữ liệu quá lớn để truyền theo giá trị. Cách này còn được gọi là *truyền tham số bằng tham chiếu*.

:mod:`!ctypes` xuất :func:`byref` function, được dùng để truyền tham số bằng tham chiếu. Có thể đạt được hiệu ứng tương tự với hàm :func:`pointer`, mặc dù :func:`pointer` thực hiện nhiều công việc hơn vì nó tạo một đối tượng con trỏ thực, do đó sử dụng :func:`byref` sẽ nhanh hơn nếu bản thân Python không cần đối tượng con trỏ::

   >>> i = c_int()
   >>> f = c_float()
   >>> s = create_string_buffer(b'\000' * 32)
   >>> print(i.value, f.value, repr(s.value))
   0 0.0 b''
   >>> libc.sscanf(b"1 3.14 Hello", b"%d %f %s",
   ...             byref(i), byref(f), s)
   3
   >>> print(i.value, f.value, repr(s.value))
   1 3.1400001049 b'Hello'
   >>>


.. _ctypes-structures-unions:

Structures và unions
^^^^^^^^^^^^^^^^^^^^

Structures và unions phải kế thừa từ các lớp cơ sở :class:`Structure` và :class:`Union`, được định nghĩa trong module :mod:`!ctypes`. Mỗi lớp con phải định nghĩa một thuộc tính :attr:`~Structure._fields_`. :attr:`!_fields_` phải là một danh sách gồm các *2-tuples*, chứa *tên trường* và *kiểu trường*.

Kiểu trường phải là một kiểu :mod:`!ctypes` như :class:`c_int`, hoặc bất kỳ kiểu :mod:`!ctypes` dẫn xuất nào khác: structure, union, array, pointer.

Sau đây là một ví dụ đơn giản về structure POINT, chứa hai số nguyên có tên *x* và *y*, đồng thời cho thấy cách khởi tạo một structure trong constructor::

   >>> from ctypes import *
   >>> class POINT(Structure):
   ...     _fields_ = [("x", c_int),
   ...                 ("y", c_int)]
   ...
   >>> point = POINT(10, 20)
   >>> print(point.x, point.y)
   10 20
   >>> point = POINT(y=5)
   >>> print(point.x, point.y)
   0 5
   >>> POINT(1, 2, 3)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: too many initializers
   >>>

Tuy nhiên, bạn có thể xây dựng các structure phức tạp hơn nhiều. Một structure có thể tự chứa các structure khác bằng cách sử dụng một structure làm kiểu trường.

Sau đây là một structure RECT chứa hai POINT có tên *upperleft* và *lowerright*::

   >>> class RECT(Structure):
   ...     _fields_ = [("upperleft", POINT),
   ...                 ("lowerright", POINT)]
   ...
   >>> rc = RECT(point)
   >>> print(rc.upperleft.x, rc.upperleft.y)
   0 5
   >>> print(rc.lowerright.x, rc.lowerright.y)
   0 0
   >>>

Các structure lồng nhau cũng có thể được khởi tạo trong constructor theo nhiều cách::

   >>> r = RECT(POINT(1, 2), POINT(3, 4))
   >>> r = RECT((1, 2), (3, 4))

Trường :term:`descriptor`\s có thể được lấy từ *class*, và chúng hữu ích cho việc gỡ lỗi vì có thể cung cấp thông tin hữu ích. Xem :class:`CField`::

   >>> POINT.x
   <ctypes.CField 'x' type=c_int, ofs=0, size=4>
   >>> POINT.y
   <ctypes.CField 'y' type=c_int, ofs=4, size=4>
   >>>


.. _ctypes-structureunion-alignment-byte-order:

.. warning::

   :mod:`!ctypes` không hỗ trợ truyền các union hoặc structure có bit-field cho hàm theo giá trị. Mặc dù cách này có thể hoạt động trên x86 32-bit, thư viện không đảm bảo nó hoạt động trong trường hợp tổng quát. Các union và structure có bit-field luôn phải được truyền cho hàm bằng con trỏ.

Bố cục, căn chỉnh và thứ tự byte của structure/union
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Theo mặc định, các trường của Structure và Union được bố trí theo cùng cách mà trình biên dịch C thực hiện. Có thể ghi đè hoàn toàn hành vi này bằng cách chỉ định một
thuộc tính lớp :attr:`~Structure._layout_` trong định nghĩa lớp con; xem tài liệu về thuộc tính để biết chi tiết.

Có thể chỉ định căn chỉnh tối đa cho các trường và/hoặc cho chính structure bằng cách lần lượt thiết lập các thuộc tính lớp :attr:`~Structure._pack_` và/hoặc :attr:`~Structure._align_`. Xem tài liệu về thuộc tính để biết chi tiết.

:mod:`!ctypes` sử dụng thứ tự byte gốc cho các Structure và Union. Để tạo các structure có thứ tự byte không phải gốc, bạn có thể sử dụng một trong các
:class:`BigEndianStructure`, :class:`LittleEndianStructure`,
lớp cơ sở :class:`BigEndianUnion` và :class:`LittleEndianUnion`. Các lớp này không thể chứa các trường con trỏ.


.. _ctypes-bit-fields-in-structures-unions:

Các trường bit trong structure và union
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Có thể tạo các structure và union chứa các trường bit. Các trường bit chỉ có thể áp dụng cho các trường số nguyên; độ rộng bit được chỉ định ở mục thứ ba trong các tuple :attr:`~Structure._fields_`::

   >>> class Int(Structure):
   ...     _fields_ = [("first_16", c_int, 16),
   ...                 ("second_16", c_int, 16)]
   ...
   >>> print(Int.first_16)
   <ctypes.CField 'first_16' type=c_int, ofs=0, bit_size=16, bit_offset=0>
   >>> print(Int.second_16)
   <ctypes.CField 'second_16' type=c_int, ofs=0, bit_size=16, bit_offset=16>

Điều quan trọng cần lưu ý là việc cấp phát và bố trí trường bit trong bộ nhớ không được quy định trong tiêu chuẩn C; cách triển khai phụ thuộc vào compiler. Theo mặc định, Python sẽ cố gắng khớp với hành vi của compiler "native" trên nền tảng hiện tại. Xem thuộc tính :attr:`~Structure._layout_` để biết chi tiết về hành vi mặc định và cách thay đổi hành vi đó.


.. _ctypes-arrays:

Mảng
^^^^

Mảng là các dãy chứa một số lượng cố định các instance cùng kiểu.

Cách được khuyến nghị để tạo các kiểu mảng là nhân một kiểu dữ liệu với một số nguyên dương::

   TenPointsArrayType = POINT * 10

Sau đây là một ví dụ về kiểu dữ liệu hơi mang tính nhân tạo: một structure chứa 4 POINT cùng với một số thành phần khác::

   >>> from ctypes import *
   >>> class POINT(Structure):
   ...     _fields_ = ("x", c_int), ("y", c_int)
   ...
   >>> class MyStruct(Structure):
   ...     _fields_ = [("a", c_int),
   ...                 ("b", c_float),
   ...                 ("point_array", POINT * 4)]
   >>>
   >>> print(len(MyStruct().point_array))
   4
   >>>

Các instance được tạo theo cách thông thường bằng cách gọi class::

   arr = TenPointsArrayType()
   for pt in arr:
       print(pt.x, pt.y)

Đoạn mã trên in ra một loạt dòng ``0 0``, vì nội dung của array được khởi tạo bằng các số 0.

Bạn cũng có thể chỉ định các initializer thuộc đúng type::

   >>> from ctypes import *
   >>> TenIntegers = c_int * 10
   >>> ii = TenIntegers(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
   >>> print(ii)
   <c_long_Array_10 object at 0x...>
   >>> for i in ii: print(i, end=" ")
   ...
   1 2 3 4 5 6 7 8 9 10
   >>>


.. _ctypes-pointers:

Con trỏ
^^^^^^^

Các instance của con trỏ được tạo bằng cách gọi hàm :func:`pointer` trên một
type :mod:`!ctypes`::

   >>> from ctypes import *
   >>> i = c_int(42)
   >>> pi = pointer(i)
   >>>

Các instance của con trỏ có thuộc tính :attr:`~_Pointer.contents`, thuộc tính này trả về object mà con trỏ trỏ tới, tức object ``i`` ở trên::

   >>> pi.contents
   c_long(42)
   >>>

Lưu ý rằng :mod:`!ctypes` không có OOR (original object return); mỗi lần bạn truy xuất một attribute, nó sẽ tạo một đối tượng tương đương mới::

   >>> pi.contents is i
   False
   >>> pi.contents is pi.contents
   False
   >>>

Việc gán một thể hiện :class:`c_int` khác vào attribute contents của con trỏ sẽ khiến con trỏ trỏ đến vị trí bộ nhớ nơi đối tượng này được lưu trữ::

   >>> i = c_int(99)
   >>> pi.contents = i
   >>> pi.contents
   c_long(99)
   >>>

.. XXX Document dereferencing pointers, and that it is preferred over the
   .contents attribute.

Các thể hiện con trỏ cũng có thể được lập chỉ mục bằng các số nguyên::

   >>> pi[0]
   99
   >>>

Việc gán cho một chỉ mục số nguyên sẽ thay đổi giá trị được trỏ đến::

   >>> print(i)
   c_long(99)
   >>> pi[0] = 22
   >>> print(i)
   c_long(22)
   >>>

Bạn cũng có thể sử dụng các chỉ mục khác 0, nhưng phải biết mình đang làm gì, giống như trong C: Bạn có thể truy cập hoặc thay đổi các vị trí bộ nhớ tùy ý. Nhìn chung, bạn chỉ sử dụng tính năng này khi nhận được một con trỏ từ một hàm C và *biết* rằng con trỏ thực sự trỏ đến một mảng thay vì một mục đơn lẻ.

.. warning::

   Vì các đối tượng con trỏ hỗ trợ phép truy cập theo chỉ mục, chúng cũng ngầm hỗ trợ
   :term:`phép lặp <iterator>`. Trừ khi thực hiện việc này theo cách có kiểm soát, chẳng hạn như gọi thủ công :func:`next` trên một iterator :func:`pointer`, thao tác này thường sẽ dẫn đến vòng lặp vô hạn hoặc sự cố, vì ctypes không có cách nào biết khi nào cần dừng phép lặp. Nói cách khác, một iterator ``pointer`` sẽ liên tục trả về các vùng nhớ tùy ý.

Đằng sau hậu trường, hàm :func:`pointer` không chỉ đơn giản là tạo các thực thể con trỏ; trước tiên, hàm này phải tạo các *kiểu* con trỏ. Việc này được thực hiện bằng
hàm :func:`POINTER`, chấp nhận bất kỳ :mod:`!ctypes` kiểu nào và trả về một kiểu mới::

   >>> PI = POINTER(c_int)
   >>> PI
   <class 'ctypes.LP_c_long'>
   >>> PI(42)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: expected c_long instead of int
   >>> PI(c_int(42))
   <ctypes.LP_c_long object at 0x...>
   >>>

Gọi kiểu con trỏ mà không có đối số sẽ tạo một con trỏ ``NULL``. Các con trỏ ``NULL`` có giá trị boolean là ``False``::

   >>> null_ptr = POINTER(c_int)()
   >>> print(bool(null_ptr))
   False
   >>>

:mod:`!ctypes` kiểm tra ``NULL`` khi hủy tham chiếu các con trỏ (nhưng việc hủy tham chiếu các con trỏ không hợp lệ, không phải \ ``NULL``, sẽ làm Python bị crash)::

   >>> null_ptr[0]
   Traceback (most recent call last):
       ....
   ValueError: NULL pointer access
   >>>

   >>> null_ptr[0] = 1234
   Traceback (most recent call last):
       ....
   ValueError: NULL pointer access
   >>>

.. _ctypes-thread-safety:

Đảm bảo an toàn luồng khi không có GIL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Kể từ Python 3.13, có thể vô hiệu hóa :term:`GIL` trên :term:`free-threaded build`. Trong ctypes, việc đồng thời đọc và ghi vào một đối tượng duy nhất là an toàn, nhưng không an toàn khi thực hiện trên nhiều đối tượng:

   .. code-block:: pycon

      >>> number = c_int(42)
      >>> pointer_a = pointer(number)
      >>> pointer_b = pointer(number)

Trong ví dụ trên, nếu GIL bị vô hiệu hóa thì chỉ an toàn khi một đối tượng đọc và ghi vào địa chỉ tại một thời điểm. Vì vậy, ``pointer_a`` có thể được chia sẻ và ghi từ nhiều thread, nhưng chỉ khi ``pointer_b`` không đồng thời cố gắng thực hiện việc tương tự. Nếu đây là vấn đề, hãy cân nhắc sử dụng :class:`threading.Lock` để đồng bộ hóa quyền truy cập vào bộ nhớ:

   .. code-block:: pycon

      >>> import threading
      >>> lock = threading.Lock()
      >>> # Luồng 1
      >>> with lock:
      ...    pointer_a.contents = 24
      >>> # Luồng 2
      >>> with lock:
      ...    pointer_b.contents = 42


.. _ctypes-type-conversions:

Chuyển đổi kiểu
^^^^^^^^^^^^^^^

Thông thường, ctypes kiểm tra kiểu nghiêm ngặt. Điều này có nghĩa là nếu bạn có ``POINTER(c_int)`` trong danh sách :attr:`~_CFuncPtr.argtypes` của một hàm hoặc làm kiểu của một trường thành viên trong định nghĩa cấu trúc, thì chỉ các instance có chính xác cùng kiểu mới được chấp nhận. Có một số ngoại lệ đối với quy tắc này, trong đó ctypes chấp nhận các đối tượng khác. Ví dụ: bạn có thể truyền các instance mảng tương thích thay cho các kiểu con trỏ. Vì vậy, đối với ``POINTER(c_int)``, ctypes chấp nhận một mảng c_int::

   >>> class Bar(Structure):
   ...     _fields_ = [("count", c_int), ("values", POINTER(c_int))]
   ...
   >>> bar = Bar()
   >>> bar.values = (c_int * 3)(1, 2, 3)
   >>> bar.count = 3
   >>> for i in range(bar.count):
   ...     print(bar.values[i])
   ...
   1
   2
   3
   >>>

Ngoài ra, nếu một đối số của hàm được khai báo rõ ràng là kiểu con trỏ (chẳng hạn như ``POINTER(c_int)``) trong :attr:`~_CFuncPtr.argtypes`, thì có thể truyền một đối tượng thuộc kiểu được con trỏ trỏ tới (``c_int`` trong trường hợp này) vào hàm. Trong trường hợp này, ctypes sẽ tự động áp dụng chuyển đổi :func:`byref` cần thiết.

Để đặt một trường kiểu POINTER thành ``NULL``, bạn có thể gán ``None``::

   >>> bar.values = None
   >>>

.. XXX list other conversions...

Đôi khi bạn có các instance thuộc những kiểu không tương thích. Trong C, bạn có thể ép một kiểu sang kiểu khác. :mod:`!ctypes` cung cấp một hàm :func:`cast` có thể được sử dụng theo cách tương tự. Cấu trúc ``Bar`` được định nghĩa ở trên chấp nhận các con trỏ ``POINTER(c_int)`` hoặc các mảng :class:`c_int` cho trường ``values``, nhưng không chấp nhận các instance thuộc kiểu khác::

   >>> bar.values = (c_byte * 4)()
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: incompatible types, c_byte_Array_4 instance instead of LP_c_long instance
   >>>

Trong những trường hợp này, hàm :func:`cast` rất hữu ích.

Có thể dùng hàm :func:`cast` để ép một thực thể ctypes thành con trỏ tới một kiểu dữ liệu ctypes khác. :func:`cast` nhận hai tham số: một đối tượng ctypes vốn là, hoặc có thể được chuyển đổi thành, một con trỏ thuộc một kiểu nào đó; và một kiểu con trỏ ctypes. Hàm trả về một thực thể thuộc đối số thứ hai, tham chiếu đến cùng khối bộ nhớ với đối số thứ nhất::

   >>> a = (c_byte * 4)()
   >>> cast(a, POINTER(c_int))
   <ctypes.LP_c_long object at ...>
   >>>

Vì vậy, có thể dùng :func:`cast` để gán vào trường ``values`` của cấu trúc ``Bar``::

   >>> bar = Bar()
   >>> bar.values = cast((c_byte * 4)(), POINTER(c_int))
   >>> print(bar.values[0])
   0
   >>>


.. _ctypes-incomplete-types:

Các kiểu chưa hoàn thiện
^^^^^^^^^^^^^^^^^^^^^^^^

*Các kiểu chưa hoàn thiện* là các cấu trúc, union hoặc mảng mà các thành phần của chúng chưa được chỉ định. Trong C, chúng được chỉ định bằng các khai báo chuyển tiếp, được định nghĩa sau đó::

   struct cell; /* forward declaration */

   struct cell {
       char *name;
       struct cell *next;
   };

Cách chuyển trực tiếp sang mã ctypes sẽ như sau, nhưng cách này không hoạt động::

   >>> class cell(Structure):
   ...     _fields_ = [("name", c_char_p),
   ...                 ("next", POINTER(cell))]
   ...
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "<stdin>", line 2, in cell
   NameError: name 'cell' is not defined
   >>>

vì ``class cell`` mới không khả dụng ngay trong câu lệnh khai báo lớp. Trong :mod:`!ctypes`, chúng ta có thể định nghĩa lớp ``cell`` và đặt
thuộc tính :attr:`~Structure._fields_` sau đó, sau câu lệnh khai báo lớp::

   >>> from ctypes import *
   >>> class cell(Structure):
   ...     pass
   ...
   >>> cell._fields_ = [("name", c_char_p),
   ...                  ("next", POINTER(cell))]
   >>>

Hãy thử xem. Chúng ta tạo hai thực thể của ``cell``, cho chúng trỏ đến nhau, rồi cuối cùng lần theo chuỗi con trỏ vài lần::

   >>> c1 = cell()
   >>> c1.name = b"foo"
   >>> c2 = cell()
   >>> c2.name = b"bar"
   >>> c1.next = pointer(c2)
   >>> c2.next = pointer(c1)
   >>> p = c1
   >>> for i in range(8):
   ...     print(p.name, end=" ")
   ...     p = p.next[0]
   ...
   foo bar foo bar foo bar foo bar
   >>>


.. _ctypes-callback-functions:

Các hàm callback
^^^^^^^^^^^^^^^^

:mod:`!ctypes` cho phép tạo các con trỏ hàm có thể được gọi từ C từ các callable của Python. Đôi khi chúng được gọi là *các hàm callback*.

Trước tiên, bạn phải tạo một lớp cho hàm callback. Lớp này xác định calling convention, kiểu giá trị trả về, cũng như số lượng và kiểu của các đối số mà hàm này sẽ nhận.

Hàm factory :func:`CFUNCTYPE` tạo các kiểu cho hàm callback bằng calling convention ``cdecl``. Trên Windows, hàm factory :func:`WINFUNCTYPE` tạo các kiểu cho hàm callback bằng calling convention ``stdcall``.

Cả hai hàm factory này đều được gọi với kiểu kết quả là đối số đầu tiên, còn các kiểu đối số mà hàm callback dự kiến nhận là những đối số còn lại.

Ở đây, tôi sẽ trình bày một ví dụ sử dụng thư viện C chuẩn
:c:func:`!qsort` function, được dùng để sắp xếp các phần tử nhờ một hàm callback. :c:func:`!qsort` sẽ được dùng để sắp xếp một mảng số nguyên::

   >>> IntArray5 = c_int * 5
   >>> ia = IntArray5(5, 1, 7, 33, 99)
   >>> qsort = libc.qsort
   >>> qsort.restype = None
   >>>

:func:`!qsort` phải được gọi với một con trỏ đến dữ liệu cần sắp xếp, số lượng phần tử trong mảng dữ liệu, kích thước của một phần tử và một con trỏ đến hàm so sánh, tức callback. Sau đó, callback sẽ được gọi với hai con trỏ đến các phần tử và phải trả về một số nguyên âm nếu phần tử thứ nhất nhỏ hơn phần tử thứ hai, 0 nếu chúng bằng nhau và một số nguyên dương trong các trường hợp còn lại.

Vì vậy, hàm callback của chúng ta nhận các con trỏ đến số nguyên và phải trả về một số nguyên. Trước tiên, chúng ta tạo ``type`` cho hàm callback::

   >>> CMPFUNC = CFUNCTYPE(c_int, POINTER(c_int), POINTER(c_int))
   >>>

Để bắt đầu, dưới đây là một callback đơn giản hiển thị các giá trị mà nó nhận được::

   >>> def py_cmp_func(a, b):
   ...     print("py_cmp_func", a[0], b[0])
   ...     return 0
   ...
   >>> cmp_func = CMPFUNC(py_cmp_func)
   >>>

Kết quả::

   >>> qsort(ia, len(ia), sizeof(c_int), cmp_func)  # doctest: +LINUX
   py_cmp_func 5 1
   py_cmp_func 33 99
   py_cmp_func 7 33
   py_cmp_func 5 7
   py_cmp_func 1 7
   >>>

Giờ đây, chúng ta thực sự có thể so sánh hai mục này và trả về một kết quả hữu ích::

   >>> def py_cmp_func(a, b):
   ...     print("py_cmp_func", a[0], b[0])
   ...     return a[0] - b[0]
   ...
   >>>
   >>> qsort(ia, len(ia), sizeof(c_int), CMPFUNC(py_cmp_func)) # doctest: +LINUX
   py_cmp_func 5 1
   py_cmp_func 33 99
   py_cmp_func 7 33
   py_cmp_func 1 7
   py_cmp_func 5 7
   >>>

Như có thể dễ dàng kiểm tra, mảng của chúng ta giờ đã được sắp xếp::

   >>> for i in ia: print(i, end=" ")
   ...
   1 5 7 33 99
   >>>

Các function factory có thể được dùng làm decorator factory, vì vậy chúng ta có thể viết luôn::

   >>> @CFUNCTYPE(c_int, POINTER(c_int), POINTER(c_int))
   ... def py_cmp_func(a, b):
   ...     print("py_cmp_func", a[0], b[0])
   ...     return a[0] - b[0]
   ...
   >>> qsort(ia, len(ia), sizeof(c_int), py_cmp_func)
   py_cmp_func 5 1
   py_cmp_func 33 99
   py_cmp_func 7 33
   py_cmp_func 1 7
   py_cmp_func 5 7
   >>>

.. note::

   Hãy đảm bảo bạn giữ tham chiếu đến các đối tượng :func:`CFUNCTYPE` chừng nào chúng còn được sử dụng từ mã C. :mod:`!ctypes` thì không làm vậy, và nếu bạn không giữ tham chiếu, chúng có thể bị garbage collection thu hồi, khiến chương trình của bạn bị crash khi một callback được tạo.

   Ngoài ra, lưu ý rằng nếu callback function được gọi trong một thread được tạo bên ngoài quyền kiểm soát của Python (ví dụ: bởi mã bên ngoài gọi callback), ctypes sẽ tạo một dummy Python thread mới trong mỗi lần gọi. Hành vi này đúng trong hầu hết trường hợp, nhưng có nghĩa là các giá trị được lưu cùng
   :class:`threading.local` sẽ *không* tồn tại qua các callback khác nhau, ngay cả khi những lần gọi đó được thực hiện từ cùng một C thread.

.. _ctypes-accessing-values-exported-from-dlls:

Truy cập các giá trị được xuất từ dll
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Một số thư viện dùng chung không chỉ xuất các hàm mà còn xuất cả các biến. Một ví dụ trong chính thư viện Python là :c:data:`Py_Version`, số phiên bản runtime của Python được mã hóa trong một hằng số nguyên duy nhất.

:mod:`!ctypes` có thể truy cập các giá trị như thế này bằng các phương thức của lớp :meth:`~_CData.in_dll` thuộc kiểu đó. *pythonapi* là một ký hiệu được định nghĩa sẵn, cho phép truy cập Python C api::

   >>> version = ctypes.c_int.in_dll(ctypes.pythonapi, "Py_Version")
   >>> print(hex(version.value))
   0x30c00a0

Ví dụ mở rộng sau đây cũng minh họa cách sử dụng con trỏ để truy cập
con trỏ :c:data:`PyImport_FrozenModules` được Python xuất.

Trích dẫn tài liệu về giá trị đó:

   Con trỏ này được khởi tạo để trỏ đến một mảng gồm các bản ghi :c:struct:`_frozen`, kết thúc bằng một bản ghi có tất cả các thành viên đều là ``NULL`` hoặc bằng không. Khi một frozen module được import, bảng này sẽ được tìm kiếm. Mã của bên thứ ba có thể lợi dụng điều này để cung cấp một tập hợp frozen module được tạo động.

Vì vậy, việc thao tác với con trỏ này thậm chí có thể hữu ích. Để giới hạn kích thước ví dụ, chúng tôi chỉ trình bày cách đọc bảng này bằng :mod:`!ctypes`::

   >>> from ctypes import *
   >>>
   >>> class struct_frozen(Structure):
   ...     _fields_ = [("name", c_char_p),
   ...                 ("code", POINTER(c_ubyte)),
   ...                 ("size", c_int),
   ...                 ("get_code", POINTER(c_ubyte)),  # Con trỏ hàm
   ...                ]
   ...
   >>>

Chúng ta đã định nghĩa kiểu dữ liệu :c:struct:`_frozen`, vì vậy có thể lấy con trỏ đến bảng::

   >>> FrozenTable = POINTER(struct_frozen)
   >>> table = FrozenTable.in_dll(pythonapi, "_PyImport_FrozenBootstrap")
   >>>

Vì ``table`` là ``pointer`` đến một mảng gồm các bản ghi ``struct_frozen``, chúng ta có thể lặp qua mảng này, nhưng phải đảm bảo vòng lặp kết thúc, vì con trỏ không có kích thước. Không sớm thì muộn, chương trình có thể sẽ gặp lỗi truy cập hoặc lỗi tương tự, vì vậy tốt hơn hết là thoát khỏi vòng lặp khi gặp mục ``NULL``::

   >>> for item in table:
   ...     if item.name is None:
   ...         break
   ...     print(item.name.decode("ascii"), item.size)
   ...
   _frozen_importlib 31764
   _frozen_importlib_external 41499
   zipimport 12345
   >>>

Việc Python chuẩn có một frozen module và một frozen package (được biểu thị bằng thành viên ``size`` âm) không được nhiều người biết đến; chúng chỉ được dùng để kiểm thử. Hãy thử với ``import __hello__`` chẳng hạn.


.. _ctypes-surprises:

Những điều bất ngờ
^^^^^^^^^^^^^^^^^^

Có một số trường hợp đặc biệt trong :mod:`!ctypes` mà bạn có thể dự đoán kết quả khác với những gì thực sự xảy ra.

Hãy xem ví dụ sau::

   >>> from ctypes import *
   >>> class POINT(Structure):
   ...     _fields_ = ("x", c_int), ("y", c_int)
   ...
   >>> class RECT(Structure):
   ...     _fields_ = ("a", POINT), ("b", POINT)
   ...
   >>> p1 = POINT(1, 2)
   >>> p2 = POINT(3, 4)
   >>> rc = RECT(p1, p2)
   >>> print(rc.a.x, rc.a.y, rc.b.x, rc.b.y)
   1 2 3 4
   >>> # bây giờ hoán đổi hai điểm
   >>> rc.a, rc.b = rc.b, rc.a
   >>> print(rc.a.x, rc.a.y, rc.b.x, rc.b.y)
   3 4 3 4
   >>>

Ừm. Chắc chắn chúng ta đã mong đợi câu lệnh cuối cùng in ra ``3 4 1 2``. Chuyện gì đã xảy ra? Sau đây là các bước của dòng ``rc.a, rc.b = rc.b, rc.a`` ở trên::

   >>> temp0, temp1 = rc.b, rc.a
   >>> rc.a = temp0
   >>> rc.b = temp1
   >>>

Lưu ý rằng ``temp0`` và ``temp1`` là các đối tượng vẫn sử dụng bộ đệm nội bộ của đối tượng ``rc`` ở trên. Vì vậy, việc thực thi ``rc.a = temp0`` sẽ sao chép nội dung bộ đệm của ``temp0`` vào bộ đệm của ``rc``. Điều này wiederum thay đổi nội dung của ``temp1``. Do đó, phép gán cuối cùng ``rc.b = temp1`` không mang lại hiệu quả như mong đợi.

Hãy nhớ rằng việc lấy các đối tượng con từ Structure, Unions và Arrays không *sao chép* đối tượng con; thay vào đó, nó lấy một đối tượng wrapper truy cập vào bộ đệm bên dưới của đối tượng gốc.

Một ví dụ khác có thể hoạt động khác với dự đoán là ví dụ sau::

   >>> s = c_char_p()
   >>> s.value = b"abc def ghi"
   >>> s.value
   b'abc def ghi'
   >>> s.value is s.value
   False
   >>>

.. note::

   Các đối tượng được khởi tạo từ :class:`c_char_p` chỉ có thể được đặt giá trị là byte hoặc số nguyên.

Tại sao nó lại in ra ``False``? Các instance của ctypes là những đối tượng chứa một khối bộ nhớ cùng một số :term:`descriptor`\s để truy cập nội dung của khối bộ nhớ đó. Việc lưu một đối tượng Python vào khối bộ nhớ không lưu chính đối tượng đó; thay vào đó, ``contents`` của đối tượng được lưu lại. Mỗi lần truy cập lại nội dung, một đối tượng Python mới sẽ được tạo ra!


.. _ctypes-variable-sized-data-types:

Kiểu dữ liệu có kích thước biến đổi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:mod:`!ctypes` cung cấp một số hỗ trợ cho các mảng và cấu trúc có kích thước biến đổi.

Có thể sử dụng hàm :func:`resize` để thay đổi kích thước bộ đệm bộ nhớ của một đối tượng ctypes hiện có. Hàm này nhận đối tượng làm đối số đầu tiên và kích thước yêu cầu tính bằng byte làm đối số thứ hai. Không thể làm cho khối bộ nhớ nhỏ hơn khối bộ nhớ tự nhiên được chỉ định bởi kiểu của đối tượng, a
:exc:`ValueError` được phát sinh nếu thử làm vậy::

   >>> short_array = (c_short * 4)()
   >>> print(sizeof(short_array))
   8
   >>> resize(short_array, 4)
   Traceback (most recent call last):
       ...
   ValueError: minimum size is 8
   >>> resize(short_array, 32)
   >>> sizeof(short_array)
   32
   >>> sizeof(type(short_array))
   8
   >>>

Điều này rất tốt, nhưng làm thế nào để truy cập các phần tử bổ sung có trong mảng này? Vì kiểu này vẫn chỉ biết về 4 phần tử, nên chúng ta sẽ gặp lỗi khi truy cập các phần tử khác::

   >>> short_array[:]
   [0, 0, 0, 0]
   >>> short_array[7]
   Traceback (most recent call last):
       ...
   IndexError: invalid index
   >>>

Một cách khác để sử dụng các kiểu dữ liệu có kích thước biến đổi với :mod:`!ctypes` là tận dụng tính linh động của Python và định nghĩa lại kiểu dữ liệu sau khi đã biết kích thước cần thiết, tùy theo từng trường hợp.


.. _ctypes-ctypes-reference:

tài liệu tham khảo ctypes
-------------------------


.. _ctypes-finding-shared-libraries:

Tìm thư viện dùng chung
^^^^^^^^^^^^^^^^^^^^^^^

Khi lập trình bằng một ngôn ngữ biên dịch, các thư viện dùng chung được truy cập trong quá trình biên dịch/liên kết chương trình và khi chương trình chạy.

Mục đích của hàm :func:`~ctypes.util.find_library` là định vị một thư viện theo cách tương tự như trình biên dịch hoặc trình nạp runtime thực hiện (trên các nền tảng có nhiều phiên bản của một thư viện dùng chung, phiên bản mới nhất sẽ được nạp), trong khi các trình nạp thư viện ctypes hoạt động giống như khi một chương trình chạy và gọi trực tiếp trình nạp runtime.

Mô-đun :mod:`!ctypes.util` cung cấp một hàm có thể giúp xác định thư viện cần nạp.


.. data:: find_library(name)
   :module: ctypes.util
   :noindex:

   Thử tìm một thư viện và trả về một pathname. *name* là tên thư viện không có tiền tố như *lib*, hậu tố như ``.so``, ``.dylib`` hoặc số phiên bản (đây là dạng được dùng cho tùy chọn linker posix :option:`!-l`). Nếu không tìm thấy thư viện, trả về ``None``.

Chức năng chính xác phụ thuộc vào hệ thống.

Trên Linux, :func:`~ctypes.util.find_library` cố gắng chạy các chương trình bên ngoài (``/sbin/ldconfig``, ``gcc``, ``objdump`` và ``ld``) để tìm tệp thư viện. Nó trả về tên tệp của thư viện.

Lưu ý rằng nếu đầu ra của các chương trình này không tương ứng với dynamic linker được Python sử dụng, kết quả của hàm này có thể gây hiểu lầm.

.. versionchanged:: 3.6
   Trên Linux, giá trị của biến môi trường ``LD_LIBRARY_PATH`` được sử dụng khi tìm kiếm thư viện nếu không thể tìm thấy thư viện bằng bất kỳ cách nào khác.

Dưới đây là một số ví dụ::

   >>> from ctypes.util import find_library
   >>> find_library("m")
   'libm.so.6'
   >>> find_library("c")
   'libc.so.6'
   >>> find_library("bz2")
   'libbz2.so.1.0'
   >>>

Trên macOS và Android, :func:`~ctypes.util.find_library` sử dụng các quy ước đặt tên và đường dẫn tiêu chuẩn của hệ thống để định vị thư viện, đồng thời trả về tên đường dẫn đầy đủ nếu thành công::

   >>> from ctypes.util import find_library
   >>> find_library("c")
   '/usr/lib/libc.dylib'
   >>> find_library("m")
   '/usr/lib/libm.dylib'
   >>> find_library("bz2")
   '/usr/lib/libbz2.dylib'
   >>> find_library("AGL")
   '/System/Library/Frameworks/AGL.framework/AGL'
   >>>

Trên Windows, :func:`~ctypes.util.find_library` tìm kiếm trong system search path và trả về tên đường dẫn đầy đủ, nhưng vì không có quy ước đặt tên được định nghĩa sẵn nên một lệnh gọi như ``find_library("c")`` sẽ thất bại và trả về ``None``.

Nếu bọc một shared library bằng :mod:`!ctypes`, *có thể* sẽ tốt hơn nếu xác định tên shared library trong thời gian phát triển và hardcode tên đó vào wrapper module, thay vì sử dụng :func:`~ctypes.util.find_library` để định vị thư viện trong runtime.


.. _ctypes-listing-loaded-shared-libraries:

Liệt kê các thư viện dùng chung đã được tải
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Khi viết mã dựa vào mã được tải từ các thư viện dùng chung, việc biết những thư viện dùng chung nào đã được tải vào tiến trình hiện tại có thể rất hữu ích.

Mô-đun :mod:`!ctypes.util` cung cấp hàm :func:`~ctypes.util.dllist`, hàm này gọi các API khác nhau do từng nền tảng cung cấp để giúp xác định những thư viện dùng chung nào đã được tải vào tiến trình hiện tại.

Đầu ra chính xác của hàm này sẽ phụ thuộc vào hệ thống. Trên hầu hết các nền tảng, mục đầu tiên trong danh sách này đại diện cho chính tiến trình hiện tại và có thể là một chuỗi rỗng. Ví dụ: trên Linux dựa trên glibc, giá trị trả về có thể có dạng::

   >>> from ctypes.util import dllist
   >>> dllist()
   ['', 'linux-vdso.so.1', '/lib/x86_64-linux-gnu/libm.so.6', '/lib/x86_64-linux-gnu/libc.so.6', ... ]

.. _ctypes-loading-shared-libraries:

Tải thư viện dùng chung
^^^^^^^^^^^^^^^^^^^^^^^

Có một số cách để tải thư viện dùng chung vào tiến trình Python. Một cách là khởi tạo :py:class:`CDLL` hoặc một trong các lớp con của nó:


.. class:: CDLL(name, mode=DEFAULT_MODE, handle=None, use_errno=False, use_last_error=False, winmode=None)

   Đại diện cho một thư viện dùng chung đã được tải.

   Các hàm trong thư viện này sử dụng quy ước gọi hàm C tiêu chuẩn và được giả định là trả về :c:expr:`int`. Python :term:`global interpreter lock` được giải phóng trước khi gọi bất kỳ hàm nào được xuất bởi các thư viện này, rồi được lấy lại sau đó. Để có hành vi hàm khác, hãy sử dụng một lớp con: :py:class:`~ctypes.OleDLL`,
   :py:class:`~ctypes.WinDLL`, hoặc :py:class:`~ctypes.PyDLL`.

   Nếu bạn đã có một :py:attr:`handle <ctypes.CDLL._handle>` trỏ đến một shared library đã được tải, bạn có thể truyền nó dưới dạng đối số *handle* để bọc thư viện đã mở trong một đối tượng :py:class:`!CDLL` mới. Trong trường hợp này, *name* chỉ được dùng để thiết lập thuộc tính :py:attr:`~ctypes.CDLL._name`, nhưng thuộc tính này có thể được điều chỉnh và/hoặc xác thực.

   Nếu *handle* là ``None``, :manpage:`dlopen(3)` của nền tảng bên dưới hoặc
   hàm :c:func:`!LoadLibrary` được dùng để tải thư viện vào process và lấy handle của thư viện đó.

   *name* là pathname của shared library cần mở. Nếu *name* không chứa dấu phân cách đường dẫn, thư viện sẽ được tìm theo cách dành riêng cho từng nền tảng.

   Trên các hệ thống không phải Windows, *name* có thể là ``None``. Trong trường hợp này,
   :c:func:`!dlopen` được gọi với ``NULL``, thao tác này mở chương trình chính dưới dạng một "library". (Một số hệ thống cũng làm tương tự khi *name* trống; ``None``/``NULL`` có tính khả chuyển cao hơn.)

   .. admonition:: Chi tiết triển khai CPython

      Vì CPython được liên kết với ``libc``, một ``None`` *name* thường được dùng để truy cập thư viện chuẩn C::

         >>> printf = ctypes.CDLL(None).printf
         >>> printf.argtypes = [ctypes.c_char_p]
         >>> printf(b"hello\n")
         hello
         6

      Để truy cập Python C API, hãy ưu tiên :py:data:`ctypes.pythonapi`, vốn hoạt động trên nhiều nền tảng.

   Có thể sử dụng tham số *mode* để chỉ định cách thư viện được tải. Để biết chi tiết, hãy tham khảo manpage :manpage:`dlopen(3)`. Trên Windows, *mode* bị bỏ qua. Trên các hệ thống posix, RTLD_NOW luôn được thêm vào và không thể cấu hình.

   Khi được đặt thành true, tham số *use_errno* bật một cơ chế của ctypes cho phép truy cập số hiệu lỗi :data:`errno` của hệ thống theo cách an toàn.
   :mod:`!ctypes` duy trì một bản sao của biến :data:`errno` của hệ thống cho từng thread; nếu bạn gọi các hàm foreign được tạo bằng ``use_errno=True`` thì
   Giá trị :data:`errno` trước khi gọi hàm được hoán đổi với bản sao riêng của ctypes; điều tương tự cũng xảy ra ngay sau khi gọi hàm.

   Hàm :func:`ctypes.get_errno` trả về giá trị của bản sao riêng của ctypes, còn hàm :func:`ctypes.set_errno` thay đổi bản sao riêng của ctypes thành một giá trị mới và trả về giá trị trước đó.

   Tham số *use_last_error*, khi được đặt thành true, bật cùng cơ chế cho mã lỗi Windows, vốn được quản lý bởi :func:`GetLastError` và
   :func:`!SetLastError` các hàm Windows API; :func:`ctypes.get_last_error` và
   :func:`ctypes.set_last_error` được dùng để yêu cầu và thay đổi bản sao riêng của ctypes về mã lỗi Windows.

   Tham số *winmode* được dùng trên Windows để chỉ định cách thư viện được tải (vì *mode* bị bỏ qua). Tham số này nhận mọi giá trị hợp lệ đối với tham số cờ ``LoadLibraryEx`` của Win32 API. Khi bị bỏ qua, mặc định là sử dụng các cờ tạo ra cách tải DLL an toàn nhất, giúp tránh những vấn đề như DLL hijacking. Truyền đường dẫn đầy đủ đến DLL là cách an toàn nhất để đảm bảo thư viện và các phần phụ thuộc chính xác được tải.

   Trên Windows, việc tạo một thực thể :class:`CDLL` có thể thất bại ngay cả khi tên DLL tồn tại. Khi không tìm thấy một DLL phụ thuộc của DLL đã tải, một
   :exc:`OSError` lỗi được phát sinh với thông báo *"[WinError 126] The specified module could not be found".* Thông báo lỗi này không chứa tên của DLL bị thiếu vì Windows API không trả về thông tin đó, khiến việc chẩn đoán lỗi trở nên khó khăn. Để khắc phục lỗi này và xác định DLL nào không được tìm thấy, bạn cần tìm danh sách các DLL phụ thuộc và xác định DLL nào không được tìm thấy bằng các công cụ gỡ lỗi và tracing của Windows.

   .. seealso::

      `Microsoft DUMPBIN tool <https://learn.microsoft.com/en-us/cpp/build/reference/dumpbin-reference?view=msvc-170>`_ -- Công cụ tìm các DLL phụ thuộc.

   .. versionchanged:: 3.8
      Đã thêm tham số *winmode*.

   .. versionchanged:: 3.12

      Tham số *name* giờ đây có thể là một :term:`path-like object`.

   Các instance của lớp này không có phương thức public. Có thể truy cập các hàm được shared library export dưới dạng thuộc tính hoặc theo chỉ mục. Lưu ý rằng việc truy cập hàm thông qua thuộc tính sẽ lưu kết quả vào cache, do đó mỗi lần truy cập lặp lại đều trả về cùng một đối tượng. Ngược lại, việc truy cập thông qua chỉ mục sẽ trả về một đối tượng mới mỗi lần.::

      >>> from ctypes import CDLL
      >>> libc = CDLL("libc.so.6")  # Trên Linux
      >>> libc.time == libc.time
      True
      >>> libc['time'] == libc['time']
      False

   Có các thuộc tính public sau đây. Tên của chúng bắt đầu bằng dấu gạch dưới để không xung đột với tên các hàm được export:

   .. attribute:: _handle

      Handle hệ thống được dùng để truy cập thư viện.

   .. attribute:: _name

      Tên của thư viện được truyền vào hàm khởi tạo.

.. class:: OleDLL

   Xem :py:class:`~ctypes.CDLL`, lớp cha, để biết thông tin chung.

   Các hàm trong thư viện này sử dụng quy ước gọi ``stdcall`` và được giả định là trả về mã :class:`HRESULT` dành riêng cho Windows. Các giá trị :class:`HRESULT` chứa thông tin cho biết lệnh gọi hàm đã thất bại hay thành công, cùng với mã lỗi bổ sung. Nếu giá trị trả về báo hiệu lỗi, một :class:`OSError` sẽ được tự động phát sinh.

   .. availability:: Windows

   .. versionchanged:: 3.3
      :exc:`WindowsError` used to be raised,
      hiện là bí danh của :exc:`OSError`.


.. class:: WinDLL

   Xem :py:class:`~ctypes.CDLL`, lớp cha, để biết thông tin chung.

   Các hàm trong những thư viện này sử dụng quy ước gọi ``stdcall`` và theo mặc định được giả định là trả về :c:expr:`int`.

   .. availability:: Windows

.. class:: PyDLL

   Xem :py:class:`~ctypes.CDLL`, lớp cha, để biết thông tin chung.

   Khi các hàm trong thư viện này được gọi, Python GIL *không* được giải phóng trong suốt lần gọi hàm, và sau khi hàm thực thi xong, cờ lỗi Python sẽ được kiểm tra. Nếu cờ lỗi được thiết lập, một ngoại lệ Python sẽ được phát sinh.

   Do đó, điều này chỉ hữu ích khi gọi trực tiếp các hàm Python C API.


.. data:: RTLD_GLOBAL

   Cờ được sử dụng làm tham số *mode*. Trên các nền tảng không có cờ này, cờ được định nghĩa là số nguyên bằng không.


.. data:: RTLD_LOCAL

   Cờ được sử dụng làm tham số *mode*. Trên các nền tảng không có cờ này, cờ này giống *RTLD_GLOBAL*.


.. data:: DEFAULT_MODE

   Chế độ mặc định được sử dụng để tải các thư viện dùng chung. Trên OSX 10.3, đây là *RTLD_GLOBAL*, còn trong các trường hợp khác thì giống *RTLD_LOCAL*.


Các thư viện dùng chung cũng có thể được tải bằng cách sử dụng một trong các đối tượng được tạo sẵn, là các instance của :class:`LibraryLoader` lớp, bằng cách gọi
phương thức :meth:`~LibraryLoader.LoadLibrary`, hoặc bằng cách truy xuất thư viện dưới dạng thuộc tính của thực thể loader.

.. class:: LibraryLoader(dlltype)

   Lớp dùng để tải các thư viện dùng chung. *dlltype* phải là một trong các
   kiểu :class:`CDLL`, :class:`PyDLL`, :class:`WinDLL` hoặc :class:`OleDLL`.

   :meth:`!__getattr__` có hành vi đặc biệt: Cho phép tải một thư viện dùng chung bằng cách truy xuất thư viện đó dưới dạng thuộc tính của một thực thể library loader. Kết quả được lưu vào bộ nhớ đệm, vì vậy các lần truy xuất thuộc tính lặp lại sẽ trả về cùng một thư viện.

   .. method:: LoadLibrary(name)

      Tải một thư viện dùng chung vào process và trả về thư viện đó. Phương thức này luôn trả về một thực thể mới của thư viện.


Các library loader dựng sẵn sau đây khả dụng:

.. data:: cdll

   Tạo các thực thể :class:`CDLL`.


.. data:: windll

   Tạo các instance :class:`WinDLL`.

   .. availability:: Windows


.. data:: oledll

   Tạo các instance :class:`OleDLL`.

   .. availability:: Windows


.. data:: pydll

   Tạo các instance :class:`PyDLL`.


Để truy cập trực tiếp vào Python C API, có sẵn một đối tượng shared library Python sẵn sàng sử dụng:

.. data:: pythonapi

   Một instance của :class:`PyDLL` cung cấp các hàm Python C API dưới dạng thuộc tính. Lưu ý rằng tất cả các hàm này được giả định là trả về C
   :c:expr:`int`, điều này dĩ nhiên không phải lúc nào cũng đúng, vì vậy bạn phải gán thuộc tính :attr:`!restype` chính xác để sử dụng các hàm này.

      .. note::

         Nếu trình thông dịch Python được liên kết tĩnh, giá trị này có thể là ``None``.

.. audit-event:: ctypes.dlopen name ctypes.LibraryLoader

   Việc tải một thư viện thông qua bất kỳ đối tượng nào trong số này sẽ phát sinh một
   :ref:`sự kiện auditing <auditing>` ``ctypes.dlopen`` với đối số chuỗi ``name``, là tên được dùng để tải thư viện.

.. audit-event:: ctypes.dlsym library,name ctypes.LibraryLoader

   Việc truy cập một hàm trong thư viện đã tải sẽ phát sinh một sự kiện auditing ``ctypes.dlsym`` với các đối số ``library`` (đối tượng thư viện) và ``name`` (tên của symbol dưới dạng chuỗi hoặc số nguyên).

.. audit-event:: ctypes.dlsym/handle handle,name ctypes.LibraryLoader

   Trong trường hợp chỉ có library handle thay vì đối tượng, việc truy cập một hàm sẽ phát sinh một sự kiện auditing ``ctypes.dlsym/handle`` với các đối số ``handle`` (library handle thô) và ``name``.

.. _ctypes-foreign-functions:

Các hàm ngoại lai
^^^^^^^^^^^^^^^^^

Như đã giải thích trong phần trước, có thể truy cập các hàm ngoại lai dưới dạng thuộc tính của các thư viện dùng chung đã tải. Các đối tượng hàm được tạo theo cách này mặc định chấp nhận số lượng đối số bất kỳ, chấp nhận mọi thực thể dữ liệu ctypes làm đối số và trả về kiểu kết quả mặc định do trình tải thư viện chỉ định.

Chúng là các thực thể của một lớp cục bộ riêng tư :class:`!_FuncPtr` (không được cung cấp trong :mod:`!ctypes`) kế thừa từ lớp riêng tư :class:`_CFuncPtr`:

.. doctest::

   >>> import ctypes
   >>> lib = ctypes.CDLL(None)
   >>> issubclass(lib._FuncPtr, ctypes._CFuncPtr)
   True
   >>> lib._FuncPtr is ctypes._CFuncPtr
   False

.. class:: _CFuncPtr

   Lớp cơ sở cho các hàm foreign có thể gọi được bằng C.

   Các thể hiện của hàm foreign cũng là các kiểu dữ liệu tương thích với C; chúng đại diện cho các con trỏ hàm C.

   Có thể tùy chỉnh hành vi này bằng cách gán giá trị cho các thuộc tính đặc biệt của đối tượng hàm foreign.

   .. attribute:: restype

      Gán một kiểu ctypes để chỉ định kiểu kết quả của hàm foreign. Sử dụng ``None`` cho :c:expr:`void`, một hàm không trả về gì.

      Có thể gán một đối tượng Python có thể gọi nhưng không phải là kiểu ctypes; trong trường hợp này, hàm được giả định là trả về một :c:expr:`int` C, và đối tượng có thể gọi sẽ được gọi với số nguyên này, cho phép xử lý thêm hoặc kiểm tra lỗi. Cách sử dụng này đã lỗi thời; để xử lý sau hoặc kiểm tra lỗi linh hoạt hơn, hãy sử dụng một kiểu dữ liệu ctypes làm
      :attr:`!restype` và gán một đối tượng có thể gọi cho thuộc tính :attr:`errcheck`.

   .. attribute:: argtypes

      Gán một tuple gồm các kiểu ctypes để chỉ định những kiểu đối số mà hàm chấp nhận. Các hàm sử dụng quy ước gọi ``stdcall`` chỉ có thể được gọi với số lượng đối số bằng độ dài của tuple này; các hàm sử dụng quy ước gọi C cũng chấp nhận các đối số bổ sung chưa được chỉ định.

      Khi một foreign function được gọi, mỗi đối số thực tế được truyền đến
      :meth:`~_CData.from_param` phương thức lớp của các item trong tuple :attr:`argtypes`, phương thức này cho phép chuyển đổi đối số thực tế thành một đối tượng mà foreign function chấp nhận. Ví dụ, một item :class:`c_char_p` trong tuple :attr:`argtypes` sẽ chuyển đổi chuỗi được truyền làm đối số thành một đối tượng bytes bằng các quy tắc chuyển đổi của ctypes.

      Mới: Giờ đây có thể đặt các item không phải là kiểu ctypes vào argtypes, nhưng mỗi item phải có phương thức :meth:`~_CData.from_param` trả về một giá trị có thể dùng làm đối số (số nguyên, chuỗi, thực thể ctypes). Điều này cho phép định nghĩa các adapter có thể chuyển đổi các đối tượng tùy chỉnh thành tham số hàm.

   .. attribute:: errcheck

      Gán một hàm Python hoặc một callable khác cho thuộc tính này. Callable sẽ được gọi với ba hoặc nhiều đối số:

      .. function:: callable(result, func, arguments)
         :noindex:
         :module:

         *result* là giá trị mà foreign function trả về, như được chỉ định bởi
         :attr:`!restype` thuộc tính.

         *func* là chính đối tượng foreign function; điều này cho phép sử dụng lại cùng một callable để kiểm tra hoặc hậu xử lý kết quả của nhiều hàm.

         *arguments* là một tuple chứa các tham số ban đầu được truyền vào lời gọi hàm; điều này cho phép chuyên biệt hóa hành vi dựa trên các đối số được sử dụng.

      Đối tượng mà hàm này trả về sẽ được trả về từ lời gọi hàm ngoại, nhưng hàm này cũng có thể kiểm tra giá trị kết quả và phát sinh một exception nếu lời gọi hàm ngoại thất bại.


.. audit-event:: ctypes.set_exception code foreign-functions

   Trên Windows, khi một lời gọi hàm ngoại phát sinh một system exception (ví dụ do lỗi vi phạm quyền truy cập), exception đó sẽ được bắt và thay thế bằng một Python exception phù hợp. Ngoài ra, một sự kiện audit ``ctypes.set_exception`` với đối số ``code`` sẽ được phát sinh, cho phép một audit hook thay thế exception đó bằng exception riêng của nó.

.. audit-event:: ctypes.call_function func_pointer,arguments foreign-functions

   Một số cách gọi hàm ngoại, cũng như một số hàm trong module này, có thể phát sinh một sự kiện audit ``ctypes.call_function`` với các đối số ``function pointer`` và ``arguments``.

.. _ctypes-function-prototypes:

Các prototype của hàm
^^^^^^^^^^^^^^^^^^^^^

Hàm ngoại cũng có thể được tạo bằng cách khởi tạo các prototype của hàm. Các prototype của hàm tương tự như prototype của hàm trong C; chúng mô tả một hàm (kiểu trả về, kiểu đối số, calling convention) mà không định nghĩa phần triển khai. Các hàm factory phải được gọi với kiểu kết quả mong muốn và các kiểu đối số của hàm, đồng thời có thể được dùng làm factory của decorator và do đó được áp dụng cho các hàm thông qua cú pháp ``@wrapper``. Xem :ref:`ctypes-callback-functions` để biết các ví dụ.


.. function:: CFUNCTYPE(restype, *argtypes, use_errno=False, use_last_error=False)

   Prototype của hàm được trả về sẽ tạo ra các hàm sử dụng calling convention C tiêu chuẩn. Hàm này sẽ giải phóng GIL trong khi gọi. Nếu *use_errno* được đặt thành true, bản sao riêng của ctypes về hệ thống
   Biến :data:`errno` được thay thế bằng giá trị :data:`errno` thực trước và sau khi gọi; *use_last_error* thực hiện điều tương tự với mã lỗi Windows.


.. function:: WINFUNCTYPE(restype, *argtypes, use_errno=False, use_last_error=False)

   Function prototype được trả về tạo ra các hàm sử dụng quy ước gọi hàm ``stdcall``. Hàm sẽ giải phóng GIL trong khi gọi. *use_errno* và *use_last_error* có cùng ý nghĩa như trên.

   .. availability:: Windows


.. function:: PYFUNCTYPE(restype, *argtypes)

   Function prototype được trả về tạo ra các hàm sử dụng quy ước gọi hàm Python. Hàm sẽ *not* giải phóng GIL trong khi gọi.

Các function prototype được tạo bởi những factory function này có thể được khởi tạo theo nhiều cách khác nhau, tùy thuộc vào kiểu và số lượng tham số trong lệnh gọi:

.. function:: prototype(address)
   :noindex:
   :module:

   Trả về một hàm ngoại tại địa chỉ đã chỉ định, địa chỉ này phải là một số nguyên.


.. function:: prototype(callable)
   :noindex:
   :module:

   Tạo một hàm có thể được C gọi (hàm callback) từ một *callable* Python.


.. function:: prototype(func_spec[, paramflags])
   :noindex:
   :module:

   Trả về một hàm ngoại được export bởi một shared library. *func_spec* phải là một bộ 2 phần tử ``(name_or_ordinal, library)``. Phần tử đầu tiên là tên của hàm được export dưới dạng chuỗi hoặc ordinal của hàm được export dưới dạng số nguyên nhỏ. Phần tử thứ hai là instance của shared library.


.. function:: prototype(vtbl_index, name[, paramflags[, iid]])
   :noindex:
   :module:

   Trả về một foreign function sẽ gọi một phương thức COM. *vtbl_index* là chỉ mục trong bảng hàm ảo, một số nguyên không âm nhỏ. *name* là tên của phương thức COM. *iid* là một con trỏ tùy chọn đến mã định danh giao diện, được dùng trong việc báo cáo lỗi mở rộng.

   Nếu không chỉ định *iid*, một :exc:`OSError` sẽ được phát sinh nếu lệnh gọi phương thức COM thất bại. Nếu chỉ định *iid*, một :exc:`~ctypes.COMError` sẽ được phát sinh thay thế.

   Các phương thức COM sử dụng một calling convention đặc biệt: Chúng yêu cầu một con trỏ đến giao diện COM làm đối số đầu tiên, ngoài các tham số được chỉ định trong tuple :attr:`!argtypes`.

   .. availability:: Windows


Tham số *paramflags* tùy chọn tạo các wrapper foreign function có nhiều chức năng hơn đáng kể so với các tính năng được mô tả ở trên.

*paramflags* phải là một tuple có cùng độ dài với :attr:`~_CFuncPtr.argtypes`.

Mỗi mục trong tuple này chứa thêm thông tin về một tham số; mục đó phải là một tuple chứa một, hai hoặc ba mục.

Mục đầu tiên là một số nguyên chứa tổ hợp các cờ hướng cho tham số:

   1
      Chỉ định một tham số đầu vào cho hàm.

   2
      Tham số đầu ra. Hàm ngoại điền một giá trị vào đó.

   4
      Tham số đầu vào có giá trị mặc định là số nguyên không.

Mục thứ hai tùy chọn là tên tham số dưới dạng chuỗi. Nếu được chỉ định, hàm ngoại có thể được gọi bằng các tham số có tên.

Mục thứ ba tùy chọn là giá trị mặc định cho tham số này.


Ví dụ sau minh họa cách bao bọc hàm Windows ``MessageBoxW`` để hàm hỗ trợ các tham số mặc định và đối số có tên. Khai báo C từ tệp header Windows là::

   WINUSERAPI int WINAPI
   MessageBoxW(
       HWND hWnd,
       LPCWSTR lpText,
       LPCWSTR lpCaption,
       UINT uType);

Sau đây là phần bao bọc với :mod:`!ctypes`::

   >>> from ctypes import c_int, WINFUNCTYPE, windll
   >>> from ctypes.wintypes import HWND, LPCWSTR, UINT
   >>> prototype = WINFUNCTYPE(c_int, HWND, LPCWSTR, LPCWSTR, UINT)
   >>> paramflags = (1, "hwnd", 0), (1, "text", "Hi"), (1, "caption", "Hello from ctypes"), (1, "flags", 0)
   >>> MessageBox = prototype(("MessageBoxW", windll.user32), paramflags)

Hàm foreign function ``MessageBox`` giờ đây có thể được gọi theo những cách sau::

   >>> MessageBox()
   >>> MessageBox(text="Spam, spam, spam")
   >>> MessageBox(flags=2, text="foo bar")

Ví dụ thứ hai minh họa các tham số đầu ra. Hàm win32 ``GetWindowRect`` lấy kích thước của một cửa sổ được chỉ định bằng cách sao chép chúng vào cấu trúc ``RECT`` mà bên gọi phải cung cấp. Dưới đây là khai báo C của hàm này::

   WINUSERAPI BOOL WINAPI
   GetWindowRect(
        HWND hWnd,
        LPRECT lpRect);

Sau đây là phần bao bọc với :mod:`!ctypes`::

   >>> from ctypes import POINTER, WINFUNCTYPE, windll, WinError
   >>> from ctypes.wintypes import BOOL, HWND, RECT
   >>> prototype = WINFUNCTYPE(BOOL, HWND, POINTER(RECT))
   >>> paramflags = (1, "hwnd"), (2, "lprect")
   >>> GetWindowRect = prototype(("GetWindowRect", windll.user32), paramflags)
   >>>

Các hàm có tham số đầu ra sẽ tự động trả về giá trị của tham số đầu ra nếu chỉ có một tham số, hoặc một tuple chứa các giá trị tham số đầu ra nếu có nhiều hơn một tham số, vì vậy hàm GetWindowRect giờ đây trả về một instance RECT khi được gọi.

Các tham số đầu ra có thể được kết hợp với protocol :attr:`~_CFuncPtr.errcheck` để thực hiện thêm việc xử lý đầu ra và kiểm tra lỗi. Hàm api win32 ``GetWindowRect`` trả về một ``BOOL`` để báo hiệu thành công hoặc thất bại, vì vậy hàm này có thể thực hiện việc kiểm tra lỗi và phát sinh một exception khi lệnh gọi api thất bại::

   >>> def errcheck(result, func, args):
   ...     if not result:
   ...         raise WinError()
   ...     return args
   ...
   >>> GetWindowRect.errcheck = errcheck
   >>>

Nếu hàm :attr:`~_CFuncPtr.errcheck` trả về tuple đối số mà nó nhận được mà không thay đổi, :mod:`!ctypes` sẽ tiếp tục quá trình xử lý thông thường đối với các tham số đầu ra. Nếu muốn trả về một tuple gồm các tọa độ cửa sổ thay vì một instance ``RECT``, bạn có thể lấy các trường trong hàm và trả về chúng; khi đó quá trình xử lý thông thường sẽ không còn diễn ra::

   >>> def errcheck(result, func, args):
   ...     if not result:
   ...         raise WinError()
   ...     rc = args[1]
   ...     return rc.left, rc.top, rc.bottom, rc.right
   ...
   >>> GetWindowRect.errcheck = errcheck
   >>>


.. _ctypes-utility-functions:

Các hàm tiện ích
^^^^^^^^^^^^^^^^

.. function:: addressof(obj)

   Trả về địa chỉ của bộ đệm bộ nhớ dưới dạng số nguyên. *obj* phải là một instance của kiểu ctypes.

   .. audit-event:: ctypes.addressof obj ctypes.addressof


.. function:: alignment(obj_or_type)

   Trả về các yêu cầu căn chỉnh của một kiểu ctypes. *obj_or_type* phải là một kiểu ctypes hoặc một instance.


.. function:: byref(obj[, offset])

   Trả về một con trỏ nhẹ đến *obj*, đối tượng này phải là một instance của kiểu ctypes. *offset* mặc định là 0 và phải là một số nguyên được cộng vào giá trị con trỏ nội bộ.

   ``byref(obj, offset)`` tương ứng với mã C này::

      (((char *)&obj) + offset)

   Đối tượng được trả về chỉ có thể được sử dụng làm tham số cho lời gọi hàm ngoại. Nó hoạt động tương tự ``pointer(obj)``, nhưng việc khởi tạo nhanh hơn nhiều.


.. function:: CopyComPointer(src, dst)

   Sao chép một con trỏ COM từ *src* sang *dst* và trả về giá trị dành riêng cho Windows
   :c:type:`!HRESULT`.

   Nếu *src* không phải là ``NULL``, phương thức ``AddRef`` của nó sẽ được gọi, làm tăng số lượng tham chiếu.

   Ngược lại, số lượng tham chiếu của *dst* sẽ không bị giảm trước khi gán giá trị mới. Trừ khi *dst* là ``NULL``, caller chịu trách nhiệm giảm số lượng tham chiếu bằng cách gọi phương thức ``Release`` của nó khi cần.

   .. availability:: Windows

   .. versionadded:: 3.14


.. function:: cast(obj, type)

   Hàm này tương tự như toán tử cast trong C. Hàm trả về một instance mới của *type*, trỏ đến cùng khối bộ nhớ với *obj*. *type* phải là một kiểu con trỏ, còn *obj* phải là một đối tượng có thể được diễn giải như một con trỏ.


.. function:: create_string_buffer(init, size=None)
              create_string_buffer(size)

   Hàm này tạo một buffer ký tự có thể thay đổi. Đối tượng được trả về là một mảng ctypes gồm :class:`c_char`.

   Nếu *size* được cung cấp (và không phải ``None``), nó phải là một :class:`int`. Giá trị này chỉ định kích thước của mảng được trả về.

   Nếu đối số *init* được cung cấp, nó phải là :class:`bytes`. Đối số này được dùng để khởi tạo các phần tử của mảng. Các byte không được khởi tạo theo cách này sẽ được đặt thành 0 (NUL).

   Nếu không cung cấp *size* (hoặc nếu nó là ``None``), buffer sẽ được tạo lớn hơn *init* một phần tử, về cơ bản là thêm một bộ kết thúc NUL.

   Nếu cung cấp cả hai đối số, *size* không được nhỏ hơn ``len(init)``.

   .. warning::

      Nếu *size* bằng ``len(init)``, bộ kết thúc NUL sẽ không được thêm vào. Không được coi buffer như vậy là một chuỗi C.

   Ví dụ::

      >>> bytes(create_string_buffer(2))
      b'\x00\x00'
      >>> bytes(create_string_buffer(b'ab'))
      b'ab\x00'
      >>> bytes(create_string_buffer(b'ab', 2))
      b'ab'
      >>> bytes(create_string_buffer(b'ab', 4))
      b'ab\x00\x00'
      >>> bytes(create_string_buffer(b'abcdef', 2))
      Traceback (most recent call last):
         ...
      ValueError: byte string too long

   .. audit-event:: ctypes.create_string_buffer init,size ctypes.create_string_buffer


.. function:: create_unicode_buffer(init, size=None)
              create_unicode_buffer(size)

   Hàm này tạo một buffer ký tự unicode có thể thay đổi. Đối tượng được trả về là một mảng ctypes của :class:`c_wchar`.

   Hàm này nhận các đối số giống như :func:`~create_string_buffer`, ngoại trừ *init* phải là một chuỗi và *size* tính theo :class:`c_wchar`.

   .. audit-event:: ctypes.create_unicode_buffer init,size ctypes.create_unicode_buffer


.. function:: DllCanUnloadNow()

   Hàm này là một hook cho phép triển khai các COM server trong tiến trình bằng ctypes. Hàm này được gọi từ hàm DllCanUnloadNow mà extension dll _ctypes xuất ra.

   .. availability:: Windows


.. function:: DllGetClassObject()

   Hàm này là một hook cho phép triển khai các COM server trong tiến trình bằng ctypes. Hàm này được gọi từ hàm DllGetClassObject mà extension dll ``_ctypes`` xuất ra.

   .. availability:: Windows


.. function:: find_library(name)
   :module: ctypes.util

   Cố gắng tìm một thư viện và trả về một pathname. *name* là tên thư viện không có tiền tố như ``lib``, hậu tố như ``.so``, ``.dylib`` hoặc số phiên bản (đây là dạng được dùng cho tùy chọn linker posix :option:`!-l`). Nếu không tìm thấy thư viện, trả về ``None``.

   Chức năng chính xác phụ thuộc vào hệ thống.

   Xem :ref:`ctypes-finding-shared-libraries` để biết tài liệu đầy đủ.


.. function:: find_msvcrt()
   :module: ctypes.util

   Trả về tên tệp của thư viện runtime VC được Python và các extension module sử dụng. Nếu không thể xác định tên thư viện, ``None`` sẽ được trả về.

   Nếu cần giải phóng bộ nhớ, chẳng hạn bộ nhớ được cấp phát bởi một extension module bằng lệnh gọi tới ``free(void *)``, điều quan trọng là bạn phải sử dụng hàm trong chính thư viện đã cấp phát bộ nhớ đó.

   .. availability:: Windows


.. function:: dllist()
   :module: ctypes.util

   Cố gắng cung cấp danh sách các đường dẫn của những shared library được tải vào process hiện tại. Các đường dẫn này không được chuẩn hóa hoặc xử lý theo bất kỳ cách nào. Hàm có thể phát sinh :exc:`OSError` nếu các API của nền tảng bên dưới bị lỗi. Chức năng chính xác phụ thuộc vào hệ thống.

   Trên hầu hết các nền tảng, phần tử đầu tiên của danh sách biểu thị tệp thực thi hiện tại. Phần tử này có thể là một chuỗi rỗng.

   .. availability:: Windows, macOS, iOS, glibc, BSD libc, musl
   .. versionadded:: 3.14

.. function:: FormatError([code])

   Trả về mô tả dạng văn bản của mã lỗi *code*. Nếu không chỉ định mã lỗi, mã lỗi cuối cùng sẽ được sử dụng bằng cách gọi hàm API Windows
   :func:`GetLastError`.

   .. availability:: Windows


.. function:: GetLastError()

   Trả về mã lỗi cuối cùng được Windows thiết lập trong thread đang gọi. Hàm này gọi trực tiếp hàm Windows ``GetLastError()``, không trả về bản sao riêng của ctypes về mã lỗi.

   .. availability:: Windows


.. function:: get_errno()

   Trả về giá trị hiện tại của bản sao riêng của ctypes về hệ thống
   biến :data:`errno` trong thread đang gọi.

   .. audit-event:: ctypes.get_errno "" ctypes.get_errno

.. function:: get_last_error()

   Trả về giá trị hiện tại của bản sao riêng của ctypes về hệ thống
   biến :data:`!LastError` trong luồng gọi.

   .. availability:: Windows

   .. audit-event:: ctypes.get_last_error "" ctypes.get_last_error


.. function:: memmove(dst, src, count)

   Tương tự hàm thư viện C chuẩn memmove: sao chép *count* byte từ *src* đến *dst*. *dst* và *src* phải là số nguyên hoặc các thực thể ctypes có thể được chuyển đổi thành con trỏ.


.. function:: memset(dst, c, count)

   Tương tự hàm thư viện C chuẩn memset: điền khối bộ nhớ tại địa chỉ *dst* bằng *count* byte có giá trị *c*. *dst* phải là một số nguyên chỉ định một địa chỉ hoặc một thực thể ctypes.


.. function:: POINTER(type, /)

   Tạo hoặc trả về một kiểu con trỏ ctypes. Các kiểu con trỏ được lưu vào bộ nhớ đệm và tái sử dụng nội bộ, vì vậy việc gọi hàm này nhiều lần không tốn nhiều chi phí. *type* phải là một kiểu ctypes.

   .. impl-detail::

      Kiểu con trỏ kết quả được lưu vào bộ nhớ đệm trong thuộc tính ``__pointer_type__`` của *type*. Có thể thiết lập thuộc tính này trước lần gọi đầu tiên đến ``POINTER`` để đặt một kiểu con trỏ tùy chỉnh. Tuy nhiên, không nên làm vậy: việc tự tạo một kiểu con trỏ phù hợp rất khó nếu không dựa vào các chi tiết triển khai có thể thay đổi trong những phiên bản Python sau này.


.. function:: pointer(obj, /)

   Tạo một thực thể con trỏ mới, trỏ đến *obj*. Đối tượng được trả về thuộc kiểu ``POINTER(type(obj))``.

   Lưu ý: Nếu bạn chỉ muốn truyền một con trỏ đến một đối tượng trong lời gọi hàm foreign, bạn nên sử dụng ``byref(obj)``, cách này nhanh hơn nhiều.


.. function:: resize(obj, size)

   Hàm này thay đổi kích thước bộ đệm bộ nhớ nội bộ của *obj*, vốn phải là một instance của kiểu ctypes. Không thể làm bộ đệm nhỏ hơn kích thước gốc của kiểu đối tượng, như được xác định bởi ``sizeof(type(obj))``, nhưng có thể mở rộng bộ đệm.


.. function:: set_errno(value)

   Đặt giá trị hiện tại của bản sao riêng của ctypes đối với biến hệ thống :data:`errno` trong thread đang gọi thành *value* và trả về giá trị trước đó.

   .. audit-event:: ctypes.set_errno errno ctypes.set_errno


.. function:: set_last_error(value)

   Đặt giá trị hiện tại của bản sao riêng của ctypes đối với biến hệ thống
   :data:`!LastError` trong thread đang gọi thành *value* và trả về giá trị trước đó.

   .. availability:: Windows

   .. audit-event:: ctypes.set_last_error error ctypes.set_last_error


.. function:: sizeof(obj_or_type)

   Trả về kích thước tính bằng byte của bộ đệm bộ nhớ của một kiểu hoặc instance ctypes. Thực hiện tương tự toán tử C ``sizeof``.


.. function:: string_at(ptr, size=-1)

   Trả về chuỗi byte tại *void \*ptr*. Nếu *size* được chỉ định, giá trị đó được dùng làm kích thước; nếu không, chuỗi được coi là kết thúc bằng số 0.

   .. audit-event:: ctypes.string_at ptr,size ctypes.string_at


.. function:: WinError(code=None, descr=None)

   Tạo một instance của :exc:`OSError`. Nếu *code* không được chỉ định,
   :func:`GetLastError` được gọi để xác định mã lỗi. Nếu *descr* không được chỉ định, :func:`FormatError` được gọi để lấy phần mô tả lỗi dạng văn bản.

   .. availability:: Windows

   .. versionchanged:: 3.3
      Trước đây, một thực thể của :exc:`WindowsError` được tạo, hiện là bí danh của :exc:`OSError`.


.. function:: wstring_at(ptr, size=-1)

   Trả về chuỗi ký tự rộng tại *void \*ptr*. Nếu *size* được chỉ định, giá trị này được dùng làm số ký tự của chuỗi; nếu không, chuỗi được giả định là kết thúc bằng ký tự null.

   .. audit-event:: ctypes.wstring_at ptr,size ctypes.wstring_at


.. function:: memoryview_at(ptr, size, readonly=False)

   Trả về một đối tượng :class:`memoryview` có độ dài *size*, tham chiếu đến vùng nhớ bắt đầu tại *void \*ptr*.

   Nếu *readonly* là true, không thể dùng đối tượng :class:`!memoryview` được trả về để sửa đổi vùng nhớ bên dưới. (Các thay đổi được thực hiện bằng cách khác vẫn sẽ được phản ánh trong đối tượng được trả về.)

   Hàm này tương tự :func:`string_at`, với điểm khác biệt chính là không tạo bản sao của vùng nhớ được chỉ định. Đây là một phương án tương đương về ngữ nghĩa (nhưng hiệu quả hơn) so với ``memoryview((c_byte * size).from_address(ptr))``. (Trong khi :meth:`~_CData.from_address` chỉ nhận các số nguyên, *ptr* cũng có thể được cung cấp dưới dạng :class:`ctypes.POINTER` hoặc đối tượng :func:`~ctypes.byref`.)

   .. audit-event:: ctypes.memoryview_at address,size,readonly

   .. versionadded:: 3.14


.. _ctypes-data-types:

Các kiểu dữ liệu
^^^^^^^^^^^^^^^^


.. class:: _CData

   Lớp không công khai này là lớp cơ sở chung của tất cả các kiểu dữ liệu ctypes. Ngoài những điều khác, mọi thực thể kiểu ctypes đều chứa một khối bộ nhớ lưu trữ dữ liệu tương thích với C; địa chỉ của khối bộ nhớ được hàm trả về
   :func:`addressof` helper function. Another instance variable is exposed as
   :attr:`_objects`; biến này chứa các đối tượng Python khác cần được giữ tồn tại trong trường hợp khối bộ nhớ chứa các con trỏ.

   Các phương thức phổ biến của kiểu dữ liệu ctypes đều là các phương thức lớp (chính xác hơn, chúng là các phương thức của :term:`metaclass`):

   .. method:: _CData.from_buffer(source[, offset])

      Phương thức này trả về một thực thể ctypes dùng chung bộ đệm của đối tượng *source*. Đối tượng *source* phải hỗ trợ giao diện bộ đệm có thể ghi. Tham số *offset* tùy chọn chỉ định độ lệch tính bằng byte trong bộ đệm nguồn; giá trị mặc định là 0. Nếu bộ đệm nguồn không đủ lớn, một :exc:`ValueError` sẽ được phát sinh.

      .. audit-event:: ctypes.cdata/buffer pointer,size,offset ctypes._CData.from_buffer

   .. method:: _CData.from_buffer_copy(source[, offset])

      Phương thức này tạo một thực thể ctypes bằng cách sao chép bộ đệm từ bộ đệm của đối tượng *source*, đối tượng này phải có thể đọc được. Tham số *offset* tùy chọn chỉ định độ lệch tính bằng byte trong bộ đệm nguồn; giá trị mặc định là 0. Nếu bộ đệm nguồn không đủ lớn, một :exc:`ValueError` sẽ được phát sinh.

      .. audit-event:: ctypes.cdata/buffer pointer,size,offset ctypes._CData.from_buffer_copy

   .. method:: from_address(address)

      Phương thức này trả về một thực thể kiểu ctypes sử dụng vùng bộ nhớ được chỉ định bởi *address*, giá trị này phải là một số nguyên.

      .. audit-event:: ctypes.cdata address ctypes._CData.from_address

         Phương thức này và các phương thức khác gián tiếp gọi phương thức này sẽ phát sinh một
         :ref:`auditing event <auditing>` ``ctypes.cdata`` với đối số ``address``.

   .. method:: from_param(obj)

      Phương thức này chuyển đổi *obj* thành một kiểu ctypes. Phương thức được gọi với đối tượng thực tế được sử dụng trong một lời gọi hàm ngoại khi kiểu này có trong tuple :attr:`~_CFuncPtr.argtypes` của hàm ngoại; phương thức phải trả về một đối tượng có thể được sử dụng làm tham số lời gọi hàm.

      Tất cả các kiểu dữ liệu ctypes đều có một triển khai classmethod mặc định của lớp này, thường trả về *obj* nếu đó là một instance của kiểu. Một số kiểu cũng chấp nhận các đối tượng khác.

   .. method:: in_dll(library, name)

      Phương thức này trả về một instance kiểu ctypes được xuất bởi một shared library. *name* là tên của symbol xuất dữ liệu, còn *library* là shared library đã được tải.

   Các biến lớp phổ biến của các kiểu dữ liệu ctypes:

   .. attribute:: __pointer_type__

      Kiểu con trỏ được tạo bằng cách gọi
      :func:`POINTER` cho kiểu dữ liệu ctypes tương ứng. Nếu một kiểu con trỏ chưa được tạo, thuộc tính này sẽ bị thiếu.

      .. versionadded:: 3.14

   Các biến instance phổ biến của kiểu dữ liệu ctypes:

   .. attribute:: _b_base_

      Đôi khi các thực thể dữ liệu ctypes không sở hữu khối bộ nhớ mà chúng chứa; thay vào đó, chúng chia sẻ một phần khối bộ nhớ của đối tượng cơ sở. Thành viên
      :attr:`_b_base_` chỉ đọc là đối tượng ctypes gốc sở hữu khối bộ nhớ.

   .. attribute:: _b_needsfree_

      Biến chỉ đọc này có giá trị true khi instance dữ liệu ctypes tự cấp phát khối bộ nhớ, và có giá trị false trong các trường hợp khác.

   .. attribute:: _objects

      Thành viên này có thể là ``None`` hoặc một dictionary chứa các đối tượng Python cần được giữ cho đến khi còn tồn tại, ताकि nội dung khối bộ nhớ vẫn hợp lệ. Đối tượng này chỉ được cung cấp để debug; không bao giờ được sửa đổi nội dung của dictionary này.


.. _ctypes-fundamental-data-types-2:

Các kiểu dữ liệu cơ bản
^^^^^^^^^^^^^^^^^^^^^^^

.. class:: _SimpleCData

   Lớp không công khai này là lớp cơ sở của tất cả các kiểu dữ liệu ctypes cơ bản. Lớp này được đề cập ở đây vì chứa các thuộc tính chung của những kiểu dữ liệu ctypes cơ bản. :class:`_SimpleCData` là một lớp con của
   :class:`_CData`, vì vậy nó kế thừa các phương thức và thuộc tính của chúng. Các kiểu dữ liệu ctypes không phải là con trỏ và không chứa con trỏ giờ đây có thể được pickle.

   Các instance có một thuộc tính duy nhất:

   .. attribute:: value

      Thuộc tính này chứa giá trị thực của instance. Đối với các kiểu số nguyên và con trỏ, đó là một số nguyên; đối với các kiểu ký tự, đó là một đối tượng bytes chứa một ký tự hoặc một chuỗi; đối với các kiểu con trỏ ký tự, đó là một đối tượng bytes hoặc một chuỗi Python.

      Khi thuộc tính ``value`` được lấy từ một instance ctypes, thường thì mỗi lần sẽ trả về một object mới. :mod:`!ctypes` không *not* triển khai việc trả về object ban đầu; luôn có một object mới được tạo. Điều tương tự cũng đúng với tất cả các instance object ctypes khác.

   Mỗi lớp con có một thuộc tính lớp:

   .. attribute:: _type_

      Thuộc tính lớp chứa một mã kiểu nội bộ dưới dạng chuỗi một ký tự. Xem :ref:`ctypes-fundamental-data-types` để biết phần tóm tắt.

      Các kiểu được đánh dấu \* trong phần tóm tắt có thể là (hoặc luôn là) bí danh của một lớp con :class:`_SimpleCData` khác và không nhất thiết sử dụng mã kiểu được liệt kê. Ví dụ: nếu các kiểu C :c:expr:`long`, :c:expr:`long long` và :c:expr:`time_t` của nền tảng là như nhau, thì :class:`c_long`,
      :class:`c_longlong` và :class:`c_time_t` đều tham chiếu đến cùng một lớp duy nhất,
      :class:`c_long`, có mã :attr:`_type_` là ``'l'``. Mã ``'L'`` sẽ không được sử dụng.

      .. seealso::

         Các mô-đun :mod:`array` và :ref:`struct <format-characters>`, cũng như các mô-đun bên thứ ba như `numpy <https://numpy.org/doc/stable/reference/arrays.interface.html#object.__array_interface__>`__, sử dụng các mã kiểu tương tự -- nhưng hơi khác nhau --.


Các kiểu dữ liệu cơ bản, khi được trả về dưới dạng kết quả của lệnh gọi hàm ngoại hoặc, chẳng hạn, khi truy xuất các thành viên trường của cấu trúc hay các phần tử mảng, sẽ được chuyển đổi trong suốt thành các kiểu Python gốc. Nói cách khác, nếu một hàm ngoại có
:attr:`~_CFuncPtr.restype` kiểu :class:`c_char_p`, bạn sẽ luôn nhận được một đối tượng bytes của Python, *không* một thực thể :class:`c_char_p`.

.. XXX above is false, it actually returns a Unicode string

Các lớp con của kiểu dữ liệu cơ bản *không* kế thừa hành vi này. Vì vậy, nếu :attr:`!restype` của một hàm ngoại là một lớp con của :class:`c_void_p`, bạn sẽ nhận được một thực thể của lớp con này từ lệnh gọi hàm. Tất nhiên, bạn có thể lấy giá trị của con trỏ bằng cách truy cập thuộc tính ``value``.

Đây là các kiểu dữ liệu ctypes cơ bản:

.. class:: c_byte

   Đại diện cho kiểu dữ liệu C :c:expr:`signed char` và diễn giải giá trị dưới dạng số nguyên nhỏ. Hàm khởi tạo chấp nhận một giá trị khởi tạo số nguyên tùy chọn; không thực hiện kiểm tra tràn số.


.. class:: c_char

   Đại diện cho kiểu dữ liệu C :c:expr:`char` và diễn giải giá trị dưới dạng một ký tự đơn. Hàm khởi tạo chấp nhận một giá trị khởi tạo chuỗi tùy chọn; độ dài của chuỗi phải chính xác là một ký tự.


.. class:: c_char_p

   Đại diện cho kiểu dữ liệu C :c:expr:`char *` khi nó trỏ đến một chuỗi kết thúc bằng ký tự null. Đối với một con trỏ ký tự tổng quát cũng có thể trỏ đến dữ liệu nhị phân, phải sử dụng ``POINTER(c_char)``. Hàm khởi tạo chấp nhận một địa chỉ số nguyên hoặc một đối tượng bytes.


.. class:: c_double

   Đại diện cho kiểu dữ liệu C :c:expr:`double`. Hàm khởi tạo chấp nhận một giá trị khởi tạo số thực tùy chọn.


.. class:: c_longdouble

   Đại diện cho kiểu dữ liệu C :c:expr:`long double`. Hàm khởi tạo chấp nhận một giá trị khởi tạo số thực tùy chọn. Trên các nền tảng mà ``sizeof(long double) == sizeof(double)``, nó là bí danh của :class:`c_double`.

.. class:: c_float

   Đại diện cho kiểu dữ liệu C :c:expr:`float`. Hàm khởi tạo chấp nhận một giá trị khởi tạo số thực tùy chọn.


.. class:: c_double_complex

   Biểu diễn kiểu dữ liệu C :c:expr:`double complex`, nếu có. Hàm khởi tạo chấp nhận một bộ khởi tạo :class:`complex` tùy chọn.

   .. versionadded:: 3.14


.. class:: c_float_complex

   Biểu diễn kiểu dữ liệu C :c:expr:`float complex`, nếu có. Hàm khởi tạo chấp nhận một bộ khởi tạo :class:`complex` tùy chọn.

   .. versionadded:: 3.14


.. class:: c_longdouble_complex

   Biểu diễn kiểu dữ liệu C :c:expr:`long double complex`, nếu có. Hàm khởi tạo chấp nhận một bộ khởi tạo :class:`complex` tùy chọn.

   .. versionadded:: 3.14


.. class:: c_int

   Biểu diễn kiểu dữ liệu C :c:expr:`signed int`. Hàm khởi tạo chấp nhận một bộ khởi tạo số nguyên tùy chọn; không thực hiện kiểm tra tràn số. Trên các nền tảng mà ``sizeof(int) == sizeof(long)``, nó là bí danh của :class:`c_long`.


.. class:: c_int8

   Biểu diễn kiểu dữ liệu C :c:expr:`signed int` 8 bit. Đây là bí danh của
   :class:`c_byte`.


.. class:: c_int16

   Biểu diễn kiểu dữ liệu C :c:expr:`signed int` 16 bit. Thường là bí danh của
   :class:`c_short`.


.. class:: c_int32

   Biểu diễn kiểu dữ liệu C :c:expr:`signed int` 32 bit. Thường là bí danh của
   :class:`c_int`.


.. class:: c_int64

   Đại diện cho kiểu dữ liệu C 64-bit :c:expr:`signed int`. Thường là bí danh của
   :class:`c_longlong`.


.. class:: c_long

   Đại diện cho kiểu dữ liệu C :c:expr:`signed long`. Hàm khởi tạo chấp nhận một giá trị khởi tạo số nguyên tùy chọn; không thực hiện kiểm tra tràn số.


.. class:: c_longlong

   Đại diện cho kiểu dữ liệu C :c:expr:`signed long long`. Hàm khởi tạo chấp nhận một giá trị khởi tạo số nguyên tùy chọn; không thực hiện kiểm tra tràn số. Trên các nền tảng mà ``sizeof(long long) == sizeof(long)``, nó là bí danh của :class:`c_long`.


.. class:: c_short

   Đại diện cho kiểu dữ liệu C :c:expr:`signed short`. Hàm khởi tạo chấp nhận một giá trị khởi tạo số nguyên tùy chọn; không thực hiện kiểm tra tràn số.


.. class:: c_size_t

   Đại diện cho kiểu dữ liệu C :c:type:`size_t`. Thường là bí danh của một kiểu số nguyên không dấu khác.


.. class:: c_ssize_t

   Đại diện cho kiểu dữ liệu :c:type:`Py_ssize_t`. Đây là phiên bản có dấu của :c:type:`size_t`; tức là kiểu POSIX :c:type:`ssize_t`. Thường là bí danh của một kiểu số nguyên khác.

   .. versionadded:: 3.2


.. class:: c_time_t

   Đại diện cho kiểu dữ liệu C :c:type:`time_t`. Thường là bí danh của một kiểu số nguyên khác.

   .. versionadded:: 3.12


.. class:: c_ubyte

   Biểu thị kiểu dữ liệu C :c:expr:`unsigned char`, diễn giải giá trị dưới dạng số nguyên nhỏ. Hàm khởi tạo chấp nhận một giá trị khởi tạo số nguyên tùy chọn; không thực hiện kiểm tra tràn.


.. class:: c_uint

   Biểu thị kiểu dữ liệu C :c:expr:`unsigned int`. Hàm khởi tạo chấp nhận một giá trị khởi tạo số nguyên tùy chọn; không thực hiện kiểm tra tràn. Trên các nền tảng mà ``sizeof(int) == sizeof(long)``, nó là bí danh của :class:`c_ulong`.


.. class:: c_uint8

   Biểu thị kiểu dữ liệu C :c:expr:`unsigned int` 8 bit. Đây là bí danh của
   :class:`c_ubyte`.


.. class:: c_uint16

   Biểu thị kiểu dữ liệu C :c:expr:`unsigned int` 16 bit. Thường là bí danh của
   :class:`c_ushort`.


.. class:: c_uint32

   Biểu thị kiểu dữ liệu C :c:expr:`unsigned int` 32 bit. Thường là bí danh của
   :class:`c_uint`.


.. class:: c_uint64

   Biểu thị kiểu dữ liệu C :c:expr:`unsigned int` 64 bit. Thường là bí danh của
   :class:`c_ulonglong`.


.. class:: c_ulong

   Biểu thị kiểu dữ liệu C :c:expr:`unsigned long`. Hàm khởi tạo chấp nhận một giá trị khởi tạo số nguyên tùy chọn; không thực hiện kiểm tra tràn.


.. class:: c_ulonglong

   Đại diện cho kiểu dữ liệu C :c:expr:`unsigned long long`. Hàm khởi tạo chấp nhận một giá trị khởi tạo số nguyên tùy chọn; không thực hiện kiểm tra tràn số. Trên các nền tảng mà ``sizeof(long long) == sizeof(long)``, nó là bí danh của :class:`c_long`.


.. class:: c_ushort

   Đại diện cho kiểu dữ liệu C :c:expr:`unsigned short`. Hàm khởi tạo chấp nhận một giá trị khởi tạo số nguyên tùy chọn; không thực hiện kiểm tra tràn số.


.. class:: c_void_p

   Đại diện cho kiểu C :c:expr:`void *`. Giá trị được biểu diễn dưới dạng số nguyên. Hàm khởi tạo chấp nhận một giá trị khởi tạo số nguyên tùy chọn.


.. class:: c_wchar

   Đại diện cho kiểu dữ liệu C :c:type:`wchar_t` và diễn giải giá trị dưới dạng chuỗi unicode một ký tự. Hàm khởi tạo chấp nhận một giá trị khởi tạo chuỗi tùy chọn; độ dài của chuỗi phải chính xác là một ký tự.


.. class:: c_wchar_p

   Đại diện cho kiểu dữ liệu C :c:expr:`wchar_t *`, kiểu này phải là một con trỏ tới chuỗi ký tự rộng kết thúc bằng số 0. Hàm khởi tạo chấp nhận một địa chỉ số nguyên hoặc một chuỗi.


.. class:: c_bool

   Đại diện cho kiểu dữ liệu C :c:expr:`bool` (chính xác hơn là :c:expr:`_Bool` từ C99). Giá trị của nó có thể là ``True`` hoặc ``False``, và hàm khởi tạo chấp nhận bất kỳ đối tượng nào có giá trị logic.


.. class:: HRESULT

   Đại diện cho một giá trị :c:type:`!HRESULT`, chứa thông tin thành công hoặc lỗi đối với một lệnh gọi hàm hoặc phương thức.

   .. availability:: Windows


.. class:: py_object

   Đại diện cho kiểu dữ liệu C :c:expr:`PyObject *`. Gọi hàm này mà không cung cấp đối số sẽ tạo một con trỏ ``NULL`` :c:expr:`PyObject *`.

   .. versionchanged:: 3.14
      :class:`!py_object` is now a :term:`generic type`.

.. _ctypes-wintypes:

Mô-đun :mod:`!ctypes.wintypes` cung cấp khá nhiều kiểu dữ liệu dành riêng cho Windows khác, chẳng hạn như :c:type:`!HWND`, :c:type:`!WPARAM`,
:c:type:`!VARIANT_BOOL` hoặc :c:type:`!DWORD`. Một số cấu trúc hữu ích như :c:type:`!MSG` hoặc :c:type:`!RECT` cũng được định nghĩa.


.. _ctypes-structured-data-types:

Kiểu dữ liệu có cấu trúc
^^^^^^^^^^^^^^^^^^^^^^^^


.. class:: Union(*args, **kw)

   Lớp cơ sở trừu tượng cho các union theo thứ tự byte gốc.

   Các union dùng chung những thuộc tính và hành vi với các cấu trúc; xem tài liệu :class:`Structure` để biết chi tiết.

.. class:: BigEndianUnion(*args, **kw)

   Lớp cơ sở trừu tượng cho các union theo thứ tự byte *big endian*.

   .. versionadded:: 3.11

.. class:: LittleEndianUnion(*args, **kw)

   Lớp cơ sở trừu tượng cho các union có thứ tự byte *little endian*.

   .. versionadded:: 3.11

.. class:: BigEndianStructure(*args, **kw)

   Lớp cơ sở trừu tượng cho các structure có thứ tự byte *big endian*.


.. class:: LittleEndianStructure(*args, **kw)

   Lớp cơ sở trừu tượng cho các structure có thứ tự byte *little endian*.

Các structure và union có thứ tự byte không phải native không thể chứa các trường thuộc kiểu con trỏ hoặc bất kỳ kiểu dữ liệu nào khác chứa các trường thuộc kiểu con trỏ.


.. class:: Structure(*args, **kw)

   Lớp cơ sở trừu tượng cho các structure có thứ tự byte *native*.

   Các kiểu structure và union cụ thể phải được tạo bằng cách kế thừa một trong các kiểu này và ít nhất phải định nghĩa một biến lớp :attr:`_fields_`. :mod:`!ctypes` sẽ tạo :term:`descriptor`\s cho phép đọc và ghi các trường bằng cách truy cập thuộc tính trực tiếp. Đây là


   .. attribute:: _fields_

      Một sequence định nghĩa các trường của structure. Các phần tử phải là tuple 2 phần tử hoặc 3 phần tử. Phần tử đầu tiên là tên của trường, phần tử thứ hai chỉ định kiểu của trường; kiểu này có thể là bất kỳ kiểu dữ liệu ctypes nào.

      Đối với các trường kiểu số nguyên như :class:`c_int`, có thể cung cấp một mục tùy chọn thứ ba. Mục này phải là một số nguyên dương nhỏ xác định độ rộng bit của trường.

      Tên trường phải là duy nhất trong một cấu trúc hoặc union. Điều này không được kiểm tra; nếu tên bị lặp, chỉ một trường có thể được truy cập.

      Có thể định nghĩa biến lớp :attr:`_fields_` *sau* câu lệnh lớp định nghĩa lớp con Structure, cho phép tạo các kiểu dữ liệu tham chiếu trực tiếp hoặc gián tiếp đến chính chúng.::

         class List(Structure):
             pass
         List._fields_ = [("pnext", POINTER(List)),
                          ...
                         ]

      Biến lớp :attr:`!_fields_` chỉ có thể được thiết lập một lần. Các phép gán sau đó sẽ gây ra :exc:`AttributeError`.

      Ngoài ra, biến lớp :attr:`!_fields_` phải được định nghĩa trước khi kiểu cấu trúc hoặc union được sử dụng lần đầu: một instance hoặc lớp con được tạo, :func:`sizeof` được gọi trên đó, v.v. Các phép gán sau đó cho :attr:`!_fields_` sẽ gây ra :exc:`AttributeError`. Nếu :attr:`!_fields_` chưa được thiết lập trước lần sử dụng đó, cấu trúc hoặc union sẽ không có trường riêng nào, như thể :attr:`!_fields_` trống.

      Các lớp con của lớp con của kiểu cấu trúc kế thừa các trường của lớp cơ sở cùng với :attr:`_fields_` được định nghĩa trong lớp con của lớp con, nếu có.


   .. attribute:: _pack_

      Một số nguyên nhỏ tùy chọn cho phép ghi đè alignment của các trường cấu trúc trong instance.

      Điều này chỉ được triển khai cho bố cục bộ nhớ tương thích với MSVC (xem :attr:`_layout_`).

      Đặt :attr:`!_pack_` thành 0 cũng giống như hoàn toàn không đặt nó. Nếu không, giá trị phải là lũy thừa dương của hai. Hiệu ứng này tương đương với ``#pragma pack(N)`` trong C, ngoại trừ
      :mod:`!ctypes` có thể cho phép các giá trị *n* lớn hơn mức trình biên dịch chấp nhận.

      :attr:`!_pack_` phải được định nghĩa trước khi :attr:`_fields_` được gán; nếu không, nó sẽ không có tác dụng.

      .. deprecated-removed:: 3.14 3.19

         Vì lý do lịch sử, nếu :attr:`!_pack_` khác 0, bố cục tương thích với MSVC sẽ được sử dụng theo mặc định. Trên các nền tảng không phải Windows, mặc định này đã không còn được khuyến nghị và dự kiến sẽ trở thành lỗi trong Python 3.19. Nếu đây là chủ đích, hãy đặt :attr:`~Structure._layout_` thành ``'ms'`` một cách rõ ràng.

   .. attribute:: _align_

      Một số nguyên nhỏ tùy chọn cho phép tăng alignment của cấu trúc khi đóng gói hoặc giải nén từ bộ nhớ.

      Giá trị không được âm. Hiệu ứng này tương đương với ``__attribute__((aligned(N)))`` trên GCC hoặc ``#pragma align(N)`` trên MSVC, ngoại trừ việc :mod:`!ctypes` có thể cho phép các giá trị mà trình biên dịch sẽ từ chối.

      :attr:`!_align_` chỉ có thể *tăng* các yêu cầu căn chỉnh của một cấu trúc. Đặt giá trị này thành 0 hoặc 1 sẽ không có tác dụng.

      Không khuyến khích sử dụng các giá trị không phải là lũy thừa của hai vì điều này có thể dẫn đến hành vi bất ngờ.

      :attr:`!_align_` phải được định nghĩa trước khi :attr:`_fields_` được gán, nếu không thao tác này sẽ không có tác dụng.

      .. versionadded:: 3.13

   .. attribute:: _layout_

      Một chuỗi tùy chọn đặt tên cho bố cục struct/union. Hiện tại, chuỗi này có thể được đặt thành:

      - ``"ms"``: bố cục được trình biên dịch Microsoft (MSVC) sử dụng. Trên GCC và Clang, có thể chọn bố cục này bằng ``__attribute__((ms_struct))``.
      - ``"gcc-sysv"``: bố cục được GCC sử dụng với mô hình dữ liệu System V hoặc “tương tự SysV”, như trên Linux và macOS. Với bố cục này, :attr:`~Structure._pack_` phải không được đặt hoặc phải bằng 0.

      Nếu không được đặt rõ ràng, ``ctypes`` sẽ sử dụng giá trị mặc định phù hợp với quy ước của nền tảng. Giá trị mặc định này có thể thay đổi trong các bản phát hành Python tương lai (ví dụ: khi một nền tảng mới được hỗ trợ chính thức hoặc khi phát hiện sự khác biệt giữa các nền tảng tương tự). Hiện tại, giá trị mặc định sẽ là:

      - Trên Windows: ``"ms"``
      - Khi :attr:`~Structure._pack_` được chỉ định: ``"ms"``. (Tùy chọn này đã lỗi thời; xem tài liệu :attr:`~Structure._pack_`.)
      - Nếu không: ``"gcc-sysv"``

      :attr:`!_layout_` phải được định nghĩa trước khi
      :attr:`~Structure._fields_` được gán, nếu không thao tác này sẽ không có hiệu lực.

      .. versionadded:: 3.14

   .. attribute:: _anonymous_

      Một chuỗi tùy chọn liệt kê tên của các trường không có tên (ẩn danh).
      :attr:`_anonymous_` phải được định nghĩa trước khi :attr:`_fields_` được gán, nếu không thao tác này sẽ không có hiệu lực.

      Các trường được liệt kê trong biến này phải là các trường thuộc kiểu structure hoặc union.
      :mod:`!ctypes` sẽ tạo các descriptor trong kiểu structure, cho phép truy cập trực tiếp vào các trường lồng nhau mà không cần tạo trường structure hoặc union.

      Sau đây là một kiểu ví dụ (Windows)::

         class _U(Union):
             _fields_ = [("lptdesc", POINTER(TYPEDESC)),
                         ("lpadesc", POINTER(ARRAYDESC)),
                         ("hreftype", HREFTYPE)]

         class TYPEDESC(Structure):
             _anonymous_ = ("u",)
             _fields_ = [("u", _U),
                         ("vt", VARTYPE)]


      Structure ``TYPEDESC`` mô tả một kiểu dữ liệu COM, trường ``vt`` chỉ định trường union nào hợp lệ. Vì trường ``u`` được định nghĩa là trường anonymous, giờ đây có thể truy cập trực tiếp vào các member từ instance TYPEDESC. ``td.lptdesc`` và ``td.u.lptdesc`` là tương đương, nhưng cách đầu tiên nhanh hơn vì không cần tạo một instance union tạm thời.::

         td = TYPEDESC()
         td.vt = VT_PTR
         td.lptdesc = POINTER(some_type)
         td.u.lptdesc = POINTER(some_type)

   Có thể định nghĩa các subclass con của structure; chúng kế thừa các trường của base class. Nếu định nghĩa subclass có một
   biến :attr:`_fields_` riêng, các trường được chỉ định trong biến này sẽ được nối thêm vào các trường của base class.

   Constructor của structure và union chấp nhận cả đối số positional và keyword. Các đối số positional được dùng để khởi tạo các trường member theo cùng thứ tự xuất hiện trong :attr:`_fields_`. Các đối số keyword trong constructor được diễn giải là các phép gán thuộc tính, vì vậy chúng sẽ khởi tạo
   :attr:`_fields_` với cùng tên hoặc tạo các thuộc tính mới cho những tên không có trong :attr:`_fields_`.


.. class:: CField(*args, **kw)

   Mô tả các trường của một :class:`Structure` và :class:`Union`. Ví dụ::

      >>> class Color(Structure):
      ...     _fields_ = (
      ...         ('red', c_uint8),
      ...         ('green', c_uint8),
      ...         ('blue', c_uint8),
      ...         ('intense', c_bool, 1),
      ...         ('blinking', c_bool, 1),
      ...    )
      ...
      >>> Color.red
      <ctypes.CField 'red' type=c_ubyte, ofs=0, size=1>
      >>> Color.green.type
      <class 'ctypes.c_ubyte'>
      >>> Color.blue.byte_offset
      2
      >>> Color.intense
      <ctypes.CField 'intense' type=c_bool, ofs=3, bit_size=1, bit_offset=0>
      >>> Color.blinking.bit_offset
      1

   Tất cả các thuộc tính đều chỉ có thể đọc.

   Các đối tượng :class:`!CField` được tạo thông qua :attr:`~Structure._fields_`; không khởi tạo lớp này trực tiếp.

   .. versionadded:: 3.14

      Trước đây, các descriptor chỉ có các thuộc tính ``offset`` và ``size`` cùng biểu diễn chuỗi có thể đọc; lớp :class:`!CField` không thể được sử dụng trực tiếp.

   .. attribute:: name

      Tên của trường, dưới dạng một chuỗi.

   .. attribute:: type

      Kiểu của trường, dưới dạng một :ref:`ctypes class <ctypes-data-types>`.

   .. attribute:: offset
                  byte_offset

      Độ lệch của trường, tính bằng byte.

      Đối với các bitfield, đây là độ lệch của *storage unit* được căn chỉnh theo byte bên dưới; xem :attr:`~CField.bit_offset`.

   .. attribute:: byte_size

      Kích thước của trường, tính bằng byte.

      Đối với các bitfield, đây là kích thước của *storage unit* bên dưới. Thông thường, nó có cùng kích thước với kiểu của bitfield.

   .. attribute:: size

      Đối với các trường không phải bitfield, tương đương với :attr:`~CField.byte_size`.

      Đối với các bitfield, trường này chứa một giá trị đóng gói theo bit tương thích ngược, kết hợp :attr:`~CField.bit_size` và
      :attr:`~CField.bit_offset`. Nên sử dụng các thuộc tính tường minh thay thế.

   .. attribute:: is_bitfield

      True nếu đây là một bitfield.

   .. attribute:: bit_offset
                  bit_size

      Vị trí của một bitfield trong *đơn vị lưu trữ* của nó, tức là trong
      :attr:`~CField.byte_size` byte bộ nhớ bắt đầu tại
      :attr:`~CField.byte_offset`.

      Để lấy giá trị của trường, hãy đọc đơn vị lưu trữ dưới dạng một số nguyên,
      :ref:`dịch trái <shifting>` đi :attr:`!bit_offset` và lấy :attr:`!bit_size` bit có trọng số thấp nhất.

      Đối với các trường không phải bitfield, :attr:`!bit_offset` bằng không và :attr:`!bit_size` bằng ``byte_size * 8``.

   .. attribute:: is_anonymous

      Bằng true nếu trường này là ẩn danh, nghĩa là trường chứa các trường con lồng nhau cần được hợp nhất vào một cấu trúc hoặc union bao quanh.


.. _ctypes-arrays-pointers:

Mảng và con trỏ
^^^^^^^^^^^^^^^

.. class:: Array(*args)

   Lớp cơ sở trừu tượng cho mảng.

   Cách được khuyến nghị để tạo các kiểu mảng cụ thể là nhân bất kỳ
   kiểu dữ liệu :mod:`!ctypes` nào với một số nguyên không âm. Ngoài ra, bạn có thể phân lớp kiểu này và định nghĩa các biến lớp :attr:`_length_` và :attr:`_type_`. Có thể đọc và ghi các phần tử mảng bằng cách sử dụng quyền truy cập chỉ mục và lát cắt tiêu chuẩn; đối với thao tác đọc lát cắt, đối tượng kết quả *không* phải là chính một :class:`Array`.

   Mảng là :ref:`tổng quát <generics>` theo kiểu của các phần tử trong đó.


   .. attribute:: _length_

        Một số nguyên dương chỉ định số phần tử trong array. Các chỉ số nằm ngoài phạm vi sẽ dẫn đến :exc:`IndexError`. Sẽ được trả về bởi :func:`len`.


   .. attribute:: _type_

        Chỉ định kiểu của từng phần tử trong array.


   Các constructor của lớp con array chấp nhận các đối số vị trí, được dùng để khởi tạo các phần tử theo thứ tự.

.. function:: ARRAY(type, length)

   Tạo một array. Tương đương với ``type * length``, trong đó *type* là một
   :mod:`!ctypes` kiểu dữ liệu và *length* là một số nguyên.

   .. soft-deprecated:: 3.14
      Ưu tiên phép nhân.


.. class:: _Pointer

   Lớp cơ sở trừu tượng private dành cho pointer.

   Các kiểu con trỏ cụ thể được tạo bằng cách gọi :func:`POINTER` với kiểu mà con trỏ sẽ trỏ tới; việc này được tự động thực hiện bởi
   :func:`pointer`.

   Nếu một con trỏ trỏ tới một mảng, bạn có thể đọc và ghi các phần tử của mảng bằng cách sử dụng các phép truy cập chỉ số và lát cắt tiêu chuẩn. Các đối tượng con trỏ không có kích thước, vì vậy :func:`len` sẽ phát sinh :exc:`TypeError`. Các chỉ số âm sẽ đọc từ vùng bộ nhớ *trước* con trỏ (như trong C), còn các chỉ số nằm ngoài phạm vi có thể sẽ khiến chương trình bị lỗi với vi phạm quyền truy cập (nếu bạn may mắn).


   .. attribute:: _type_

        Chỉ định kiểu mà con trỏ trỏ tới.

   .. attribute:: contents

        Trả về đối tượng mà con trỏ trỏ tới. Việc gán cho thuộc tính này sẽ thay đổi con trỏ để trỏ tới đối tượng được gán.


.. _ctypes-exceptions:

Ngoại lệ
^^^^^^^^

.. exception:: ArgumentError

   Ngoại lệ này được phát sinh khi một lời gọi hàm foreign không thể chuyển đổi một trong các đối số được truyền vào.


.. exception:: COMError(hresult, text, details)

   Ngoại lệ này được phát sinh khi một lời gọi phương thức COM không thành công.

   .. attribute:: hresult

      Giá trị số nguyên biểu thị mã lỗi.

   .. attribute:: text

      Thông báo lỗi.

   .. attribute:: details

      Bộ 5 phần tử ``(descr, source, helpfile, helpcontext, progid)``.

      *descr* là phần mô tả dạng văn bản.  *source* là ``ProgID`` phụ thuộc vào ngôn ngữ của lớp hoặc ứng dụng đã phát sinh lỗi.  *helpfile* là đường dẫn đến tệp trợ giúp.  *helpcontext* là mã định danh ngữ cảnh trợ giúp.  *progid* là ``ProgID`` của giao diện đã định nghĩa lỗi.

   .. availability:: Windows

   .. versionadded:: 3.14

.. _`Microsoft DUMPBIN tool`: https://learn.microsoft.com/en-us/cpp/build/reference/dumpbin-reference?view=msvc-170
