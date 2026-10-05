.. _tut-modules:

******
Mô-đun
******

Nếu bạn thoát khỏi trình thông dịch Python rồi vào lại, các định nghĩa bạn đã tạo (hàm và biến) sẽ bị mất. Vì vậy, nếu muốn viết một chương trình dài hơn một chút, tốt hơn hết là bạn nên dùng trình soạn thảo văn bản để chuẩn bị đầu vào cho trình thông dịch và chạy trình thông dịch với tệp đó làm đầu vào. Đây được gọi là tạo một *script*. Khi chương trình dài hơn, bạn có thể muốn chia chương trình thành nhiều tệp để dễ bảo trì hơn. Bạn cũng có thể muốn sử dụng một hàm tiện dụng mà mình đã viết trong nhiều chương trình mà không cần sao chép định nghĩa của hàm đó vào từng chương trình.

Để hỗ trợ việc này, Python cung cấp cách đặt các định nghĩa trong một tệp và sử dụng chúng trong một script hoặc trong một phiên tương tác của trình thông dịch. Một tệp như vậy được gọi là *module*; các định nghĩa từ một module có thể được *imported* vào các module khác hoặc vào module *main* (tập hợp các biến mà bạn có quyền truy cập trong một script được thực thi ở cấp cao nhất và trong chế độ máy tính).

Một module là một tệp chứa các định nghĩa và câu lệnh Python. Tên tệp là tên module với hậu tố :file:`.py` được thêm vào. Bên trong một module, tên của module (dưới dạng một chuỗi) có sẵn dưới dạng giá trị của biến toàn cục ``__name__``. Ví dụ, hãy dùng trình soạn thảo văn bản yêu thích của bạn để tạo một tệp có tên :file:`fibo.py` trong thư mục hiện tại với nội dung sau::

   # Module các số Fibonacci

   def fib(n):
       """Write Fibonacci series up to n."""
       a, b = 0, 1
       while a < n:
           print(a, end=' ')
           a, b = b, a+b
       print()

   def fib2(n):
       """Return Fibonacci series up to n."""
       result = []
       a, b = 0, 1
       while a < n:
           result.append(a)
           a, b = b, a+b
       return result

Bây giờ hãy vào trình thông dịch Python và import module này bằng lệnh sau::

   >>> import fibo

Điều này không thêm trực tiếp tên của các hàm được định nghĩa trong ``fibo`` vào :term:`namespace` hiện tại (xem :ref:`tut-scopes` để biết thêm chi tiết); nó chỉ thêm tên module ``fibo`` vào đó. Bạn có thể truy cập các hàm bằng tên module::

   >>> fibo.fib(1000)
   0 1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987
   >>> fibo.fib2(100)
   [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
   >>> fibo.__name__
   'fibo'

Nếu dự định sử dụng một hàm thường xuyên, bạn có thể gán hàm đó cho một tên cục bộ::

   >>> fib = fibo.fib
   >>> fib(500)
   0 1 1 2 3 5 8 13 21 34 55 89 144 233 377


.. _tut-moremodules:

Tìm hiểu thêm về module
=======================

Một module có thể chứa các câu lệnh thực thi cũng như các định nghĩa hàm. Những câu lệnh này được dùng để khởi tạo module. Chúng chỉ được thực thi vào *lần đầu tiên* tên module xuất hiện trong một câu lệnh import. [#]_ (Chúng cũng được thực thi nếu tệp được chạy như một script.)

Mỗi module có namespace riêng tư của mình, được tất cả các hàm được định nghĩa trong module sử dụng làm namespace toàn cục. Vì vậy, tác giả của một module có thể sử dụng các biến toàn cục trong module mà không phải lo lắng về việc vô tình xung đột với các biến toàn cục của người dùng. Mặt khác, nếu biết mình đang làm gì, bạn có thể truy cập các biến toàn cục của module bằng cùng ký hiệu được dùng để tham chiếu đến các hàm của module, ``modname.itemname``.

Các module có thể import các module khác. Thông thường, nhưng không bắt buộc, người ta đặt tất cả
các câu lệnh :keyword:`import` ở đầu module (hoặc script cũng vậy). Tên của các module được import, nếu được đặt ở cấp cao nhất của một module (bên ngoài mọi hàm hoặc lớp), sẽ được thêm vào namespace toàn cục của module.

Có một biến thể của câu lệnh :keyword:`import` để import trực tiếp các tên từ một module vào namespace của module thực hiện việc import. Ví dụ::

   >>> from fibo import fib, fib2
   >>> fib(500)
   0 1 1 2 3 5 8 13 21 34 55 89 144 233 377

Điều này không đưa tên của module nơi các import được lấy vào namespace cục bộ (vì vậy trong ví dụ, ``fibo`` không được định nghĩa).

Thậm chí còn có một biến thể để import tất cả các tên mà một module định nghĩa::

   >>> from fibo import *
   >>> fib(500)
   0 1 1 2 3 5 8 13 21 34 55 89 144 233 377

Cách này import tất cả các tên ngoại trừ những tên bắt đầu bằng dấu gạch dưới (``_``). Trong hầu hết trường hợp, các lập trình viên Python không sử dụng tính năng này vì nó đưa một tập hợp tên không xác định vào interpreter, có thể che khuất một số thành phần bạn đã định nghĩa.

Lưu ý rằng nhìn chung, việc import ``*`` từ một module hoặc package không được khuyến khích vì thường khiến code khó đọc. Tuy nhiên, bạn có thể sử dụng cách này để giảm thao tác gõ trong các phiên tương tác.

Nếu tên module được theo sau bởi :keyword:`!as`, thì tên đứng sau :keyword:`!as` sẽ được liên kết trực tiếp với module đã import.

::

   >>> import fibo as fib
   >>> fib.fib(500)
   0 1 1 2 3 5 8 13 21 34 55 89 144 233 377

Về cơ bản, cách này import module theo cùng cách mà ``import fibo`` thực hiện, chỉ khác là module đó có thể được sử dụng với tên ``fib``.

Cách này cũng có thể được sử dụng khi dùng :keyword:`from` với các hiệu ứng tương tự::

   >>> from fibo import fib as fibonacci
   >>> fibonacci(500)
   0 1 1 2 3 5 8 13 21 34 55 89 144 233 377


.. note::

   Vì lý do hiệu suất, mỗi module chỉ được import một lần trong mỗi phiên interpreter. Do đó, nếu bạn thay đổi các module của mình, bạn phải khởi động lại interpreter -- hoặc nếu chỉ muốn kiểm thử tương tác một module, hãy sử dụng :func:`importlib.reload`, ví dụ ``import importlib; importlib.reload(modulename)``.


.. _tut-modulesasscripts:

Thực thi module dưới dạng script
--------------------------------

Khi bạn chạy một module Python bằng::

   python fibo.py <arguments>

mã trong module sẽ được thực thi, giống như khi bạn import module đó, nhưng với ``__name__`` được đặt thành ``"__main__"``. Điều đó có nghĩa là bằng cách thêm đoạn mã này vào cuối module::

   if __name__ == "__main__":
       import sys
       fib(int(sys.argv[1]))

bạn có thể sử dụng tệp này vừa như một script vừa như một module có thể import, vì mã phân tích command line chỉ chạy khi module được thực thi dưới dạng tệp "main":

.. code-block:: shell-session

   $ python fibo.py 50
   0 1 1 2 3 5 8 13 21 34

Nếu module được import, mã này sẽ không được chạy::

   >>> import fibo
   >>>

Cách này thường được dùng để cung cấp giao diện người dùng thuận tiện cho một module hoặc cho mục đích kiểm thử (chạy module dưới dạng script sẽ thực thi một test suite).


.. _tut-searchpath:

Đường dẫn tìm kiếm module
-------------------------

.. index:: triple: module; search; path

Khi một module có tên :mod:`!spam` được import, interpreter trước tiên sẽ tìm một built-in module có tên đó. Tên của các module này được liệt kê trong
:data:`sys.builtin_module_names`. Nếu không tìm thấy, interpreter sẽ tiếp tục tìm một tệp có tên :file:`spam.py` trong danh sách các thư mục được chỉ định bởi biến
:data:`sys.path`. :data:`sys.path` được khởi tạo từ các vị trí sau:

* Thư mục chứa input script (hoặc thư mục hiện tại khi không chỉ định tệp).
* :envvar:`PYTHONPATH` (danh sách tên thư mục, sử dụng cùng cú pháp với biến shell :envvar:`PATH`).
* Giá trị mặc định phụ thuộc vào cài đặt (theo quy ước bao gồm một thư mục ``site-packages``, được xử lý bởi module :mod:`site`).

Xem thêm chi tiết tại :ref:`sys-path-init`.

.. note::
   Trên các hệ thống tệp hỗ trợ symlink, thư mục chứa script đầu vào được tính sau khi symlink được resolve. Nói cách khác, thư mục chứa symlink **không** được thêm vào đường dẫn tìm kiếm module.

Sau khi khởi tạo, các chương trình Python có thể sửa đổi :data:`sys.path`. Thư mục chứa script đang được chạy được đặt ở đầu đường dẫn tìm kiếm, trước đường dẫn thư viện chuẩn. Điều này có nghĩa là các script trong thư mục đó sẽ được tải thay cho các module cùng tên trong thư mục thư viện. Đây là một lỗi trừ khi việc thay thế này là có chủ đích. Xem phần
:ref:`tut-standardmodules` để biết thêm thông tin.

.. %
    Do we need stuff on zip files etc. ? DUBOIS

.. _tut-pycache:

Các tệp Python "đã biên dịch"
-----------------------------

Để tăng tốc độ tải module, Python lưu phiên bản đã biên dịch của mỗi module vào bộ nhớ đệm trong thư mục ``__pycache__`` với tên :file:`module.{version}.pyc`, trong đó phiên bản mã hóa định dạng của tệp đã biên dịch; nhìn chung, nó chứa số phiên bản Python. Ví dụ, trong bản phát hành CPython 3.3, phiên bản đã biên dịch của spam.py sẽ được lưu vào bộ nhớ đệm dưới dạng ``__pycache__/spam.cpython-33.pyc``. Quy ước đặt tên này cho phép các module đã biên dịch từ những bản phát hành và phiên bản Python khác nhau cùng tồn tại.

Python kiểm tra ngày sửa đổi của mã nguồn với phiên bản đã biên dịch để xác định xem phiên bản đó đã lỗi thời và cần được biên dịch lại hay chưa. Đây là một quy trình hoàn toàn tự động. Ngoài ra, các module đã biên dịch không phụ thuộc vào nền tảng, vì vậy cùng một thư viện có thể được chia sẻ giữa các hệ thống có kiến trúc khác nhau.

Python không kiểm tra cache trong hai trường hợp. Thứ nhất, Python luôn biên dịch lại và không lưu kết quả đối với module được tải trực tiếp từ dòng lệnh. Thứ hai, Python không kiểm tra cache nếu không có module nguồn. Để hỗ trợ bản phân phối không có mã nguồn (chỉ có mã đã biên dịch), module đã biên dịch phải nằm trong thư mục mã nguồn và không được có module nguồn.

Một số mẹo dành cho chuyên gia:

* Bạn có thể sử dụng các switch :option:`-O` hoặc :option:`-OO` trong lệnh Python để giảm kích thước của module đã biên dịch. Switch ``-O`` loại bỏ các câu lệnh assert, còn switch ``-OO`` loại bỏ cả câu lệnh assert và chuỗi __doc__. Vì một số chương trình có thể phụ thuộc vào việc các thành phần này khả dụng, bạn chỉ nên sử dụng tùy chọn này nếu hiểu rõ mình đang làm gì. Các module "được tối ưu hóa" có thẻ ``opt-`` và thường nhỏ hơn. Các bản phát hành trong tương lai có thể thay đổi tác động của việc tối ưu hóa.

* Một chương trình không chạy nhanh hơn khi được đọc từ tệp ``.pyc`` so với khi được đọc từ tệp ``.py``; điều duy nhất nhanh hơn ở các tệp ``.pyc`` là tốc độ chúng được tải.

* Module :mod:`compileall` có thể tạo các tệp .pyc cho tất cả module trong một thư mục.

* Có thêm thông tin chi tiết về quy trình này, bao gồm lưu đồ về các quyết định, trong :pep:`3147`.


.. _tut-standardmodules:

Các mô-đun chuẩn
================

.. index:: pair: module; sys

Python đi kèm một thư viện gồm các module chuẩn, được mô tả trong một tài liệu riêng, Python Library Reference (sau đây gọi là "Library Reference"). Một số module được tích hợp sẵn trong trình thông dịch; chúng cung cấp quyền truy cập vào những thao tác không thuộc phần cốt lõi của ngôn ngữ nhưng vẫn được tích hợp sẵn, nhằm tăng hiệu quả hoặc cung cấp quyền truy cập vào các primitive của hệ điều hành, chẳng hạn như các system call. Tập hợp các module như vậy là một tùy chọn cấu hình và cũng phụ thuộc vào nền tảng bên dưới. Ví dụ, module :mod:`winreg` chỉ được cung cấp trên các hệ thống Windows. Có một module đặc biệt đáng được chú ý:
:mod:`sys`, được tích hợp sẵn trong mọi trình thông dịch Python. Các biến ``sys.ps1`` và ``sys.ps2`` xác định các chuỗi được dùng làm prompt chính và prompt phụ::

   >>> import sys
   >>> sys.ps1
   '>>> '
   >>> sys.ps2
   '... '
   >>> sys.ps1 = 'C> '
   C> print('Yuck!')
   Yuck!
   C>


Hai biến này chỉ được định nghĩa khi trình thông dịch ở chế độ interactive.

Biến ``sys.path`` là một danh sách các chuỗi xác định đường dẫn tìm kiếm module của trình thông dịch. Biến này được khởi tạo bằng đường dẫn mặc định lấy từ biến môi trường :envvar:`PYTHONPATH`, hoặc bằng giá trị mặc định tích hợp sẵn nếu
:envvar:`PYTHONPATH` không được thiết lập. Bạn có thể sửa đổi biến này bằng các thao tác danh sách chuẩn::

   >>> import sys
   >>> sys.path.append('/ufs/guido/lib/python')


.. _tut-dir:

Hàm :func:`dir`
===============

Hàm tích hợp sẵn :func:`dir` được dùng để tìm hiểu những tên nào được một module định nghĩa. Hàm này trả về một danh sách chuỗi đã được sắp xếp::

   >>> import fibo, sys
   >>> dir(fibo)
   ['__name__', 'fib', 'fib2']
   >>> dir(sys)  # doctest: +NORMALIZE_WHITESPACE
   ['__breakpointhook__', '__displayhook__', '__doc__', '__excepthook__',
    '__interactivehook__', '__loader__', '__name__', '__package__', '__spec__',
    '__stderr__', '__stdin__', '__stdout__', '__unraisablehook__',
    '_clear_type_cache', '_current_frames', '_debugmallocstats', '_framework',
    '_getframe', '_git', '_home', '_xoptions', 'abiflags', 'addaudithook',
    'api_version', 'argv', 'audit', 'base_exec_prefix', 'base_prefix',
    'breakpointhook', 'builtin_module_names', 'byteorder', 'call_tracing',
    'callstats', 'copyright', 'displayhook', 'dont_write_bytecode', 'exc_info',
    'excepthook', 'exec_prefix', 'executable', 'exit', 'flags', 'float_info',
    'float_repr_style', 'get_asyncgen_hooks', 'get_coroutine_origin_tracking_depth',
    'getallocatedblocks', 'getdefaultencoding', 'getdlopenflags',
    'getfilesystemencodeerrors', 'getfilesystemencoding', 'getprofile',
    'getrecursionlimit', 'getrefcount', 'getsizeof', 'getswitchinterval',
    'gettrace', 'hash_info', 'hexversion', 'implementation', 'int_info',
    'intern', 'is_finalizing', 'last_traceback', 'last_type', 'last_value',
    'maxsize', 'maxunicode', 'meta_path', 'modules', 'path', 'path_hooks',
    'path_importer_cache', 'platform', 'prefix', 'ps1', 'ps2', 'pycache_prefix',
    'set_asyncgen_hooks', 'set_coroutine_origin_tracking_depth', 'setdlopenflags',
    'setprofile', 'setrecursionlimit', 'setswitchinterval', 'settrace', 'stderr',
    'stdin', 'stdout', 'thread_info', 'unraisablehook', 'version', 'version_info',
    'warnoptions']

Không có đối số, :func:`dir` liệt kê các tên mà bạn hiện đã định nghĩa::

   >>> a = [1, 2, 3, 4, 5]
   >>> import fibo
   >>> fib = fibo.fib
   >>> dir()
   ['__builtins__', '__name__', 'a', 'fib', 'fibo', 'sys']

Lưu ý rằng nó liệt kê mọi loại tên: biến, module, hàm, v.v.

.. index:: pair: module; builtins

:func:`dir` không liệt kê tên của các hàm và biến dựng sẵn. Nếu muốn xem danh sách đó, chúng được định nghĩa trong mô-đun chuẩn
:mod:`builtins`::

   >>> import builtins
   >>> dir(builtins)  # doctest: +NORMALIZE_WHITESPACE
   ['ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException',
    'BlockingIOError', 'BrokenPipeError', 'BufferError', 'BytesWarning',
    'ChildProcessError', 'ConnectionAbortedError', 'ConnectionError',
    'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning',
    'EOFError', 'Ellipsis', 'EnvironmentError', 'Exception', 'False',
    'FileExistsError', 'FileNotFoundError', 'FloatingPointError',
    'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError',
    'ImportWarning', 'IndentationError', 'IndexError', 'InterruptedError',
    'IsADirectoryError', 'KeyError', 'KeyboardInterrupt', 'LookupError',
    'MemoryError', 'NameError', 'None', 'NotADirectoryError', 'NotImplemented',
    'NotImplementedError', 'OSError', 'OverflowError',
    'PendingDeprecationWarning', 'PermissionError', 'ProcessLookupError',
    'ReferenceError', 'ResourceWarning', 'RuntimeError', 'RuntimeWarning',
    'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError',
    'SystemExit', 'TabError', 'TimeoutError', 'True', 'TypeError',
    'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError',
    'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning',
    'ValueError', 'Warning', 'ZeroDivisionError', '_', '__build_class__',
    '__debug__', '__doc__', '__import__', '__name__', '__package__', 'abs',
    'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes', 'callable',
    'chr', 'classmethod', 'compile', 'complex', 'copyright', 'credits',
    'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'exit',
    'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr',
    'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass',
    'iter', 'len', 'license', 'list', 'locals', 'map', 'max', 'memoryview',
    'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property',
    'quit', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice',
    'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars',
    'zip']

.. _tut-packages:

Package
=======

Package là một cách tổ chức namespace của module Python bằng cách sử dụng "tên module dạng dấu chấm". Ví dụ, tên module :mod:`!A.B` chỉ một submodule có tên ``B`` trong một package có tên ``A``. Cũng như việc sử dụng module giúp tác giả của các module khác nhau không phải lo lắng về tên biến toàn cục của nhau, việc sử dụng tên module dạng dấu chấm giúp tác giả của các package nhiều module như NumPy hoặc Pillow không phải lo lắng về tên module của nhau.

Giả sử bạn muốn thiết kế một tập hợp các module (một "package") để xử lý thống nhất các tệp âm thanh và dữ liệu âm thanh. Có nhiều định dạng tệp âm thanh khác nhau (thường được nhận biết qua phần mở rộng, ví dụ: :file:`.wav`,
:file:`.aiff`, :file:`.au`), vì vậy bạn có thể cần tạo và duy trì một tập hợp module ngày càng mở rộng để chuyển đổi giữa các định dạng tệp khác nhau. Ngoài ra, có nhiều thao tác khác nhau mà bạn có thể muốn thực hiện trên dữ liệu âm thanh (chẳng hạn như trộn, thêm tiếng vang, áp dụng hàm equalizer, tạo hiệu ứng stereo nhân tạo), nên bạn cũng sẽ liên tục viết thêm các module để thực hiện những thao tác này. Sau đây là một cấu trúc khả dĩ cho package của bạn (được biểu diễn dưới dạng một hệ thống tệp phân cấp):

.. code-block:: text

   sound/                          Top-level package
         __init__.py               Initialize the sound package
         formats/                  Subpackage for file format conversions
                 __init__.py
                 wavread.py
                 wavwrite.py
                 aiffread.py
                 aiffwrite.py
                 auread.py
                 auwrite.py
                 ...
         effects/                  Subpackage for sound effects
                 __init__.py
                 echo.py
                 surround.py
                 reverse.py
                 ...
         filters/                  Subpackage for filters
                 __init__.py
                 equalizer.py
                 vocoder.py
                 karaoke.py
                 ...

Khi import package, Python sẽ tìm trong các thư mục trên ``sys.path`` để tìm thư mục con của package.

Các tệp :file:`__init__.py` là bắt buộc để Python coi những thư mục chứa tệp đó là package (trừ khi sử dụng :term:`namespace package`, một tính năng tương đối nâng cao). Điều này ngăn các thư mục có tên phổ biến, chẳng hạn như ``string``, vô tình che khuất các module hợp lệ xuất hiện sau đó trên đường dẫn tìm kiếm module. Trong trường hợp đơn giản nhất, :file:`__init__.py` chỉ cần là một tệp rỗng, nhưng nó cũng có thể thực thi mã khởi tạo cho package hoặc thiết lập biến ``__all__``, được mô tả ở phần sau.

Người dùng package có thể import từng module riêng lẻ từ package, ví dụ:::

   import sound.effects.echo

Thao tác này tải submodule :mod:`!sound.effects.echo`. Bạn phải tham chiếu đến nó bằng tên đầy đủ.::

   sound.effects.echo.echofilter(input, output, delay=0.7, atten=4)

Một cách khác để import submodule là::

   from sound.effects import echo

Điều này cũng tải submodule :mod:`!echo`, đồng thời cung cấp nó mà không cần tiền tố package, vì vậy có thể sử dụng như sau::

   echo.echofilter(input, output, delay=0.7, atten=4)

Một biến thể khác nữa là import trực tiếp hàm hoặc biến mong muốn::

   from sound.effects.echo import echofilter

Một lần nữa, thao tác này tải submodule :mod:`!echo`, nhưng khiến hàm của nó
:func:`!echofilter` được cung cấp trực tiếp::

   echofilter(input, output, delay=0.7, atten=4)

Lưu ý rằng khi sử dụng ``from package import item``, item có thể là một submodule (hoặc subpackage) của package, hoặc một tên khác được định nghĩa trong package, chẳng hạn như hàm, class hoặc biến. Câu lệnh ``import`` trước tiên kiểm tra xem item có được định nghĩa trong package hay không; nếu không, nó giả định item là một module và cố gắng tải module đó. Nếu không tìm thấy, một ngoại lệ :exc:`ImportError` sẽ được raise.

Ngược lại, khi sử dụng cú pháp như ``import item.subitem.subsubitem``, mọi item ngoại trừ item cuối cùng phải là một package; item cuối cùng có thể là một module hoặc package nhưng không thể là class, hàm hoặc biến được định nghĩa trong item trước đó.


.. _tut-pkg-import-star:

Import \* từ một Package
------------------------

.. index:: single: __all__

Vậy điều gì xảy ra khi người dùng viết ``from sound.effects import *``?  Lý tưởng nhất là ta hy vọng câu lệnh này bằng cách nào đó sẽ truy cập vào filesystem, tìm xem những submodule nào hiện diện trong package, rồi import tất cả chúng.  Quá trình này có thể mất nhiều thời gian, và việc import các submodule có thể gây ra những side effect không mong muốn, vốn chỉ nên xảy ra khi submodule được import một cách rõ ràng.

Giải pháp duy nhất là tác giả package cung cấp một chỉ mục rõ ràng cho package.  Câu lệnh :keyword:`import` sử dụng quy ước sau: nếu một package có
:file:`__init__.py` định nghĩa một danh sách có tên ``__all__``, danh sách đó được xem là danh sách tên các module cần được import khi gặp ``from package import *``.  Tác giả package có trách nhiệm cập nhật danh sách này khi phát hành phiên bản mới của package.  Tác giả package cũng có thể quyết định không hỗ trợ cơ chế này nếu họ không thấy có ích khi import \* từ package của mình.  Ví dụ, tệp :file:`sound/effects/__init__.py` có thể chứa đoạn code sau::

   __all__ = ["echo", "surround", "reverse"]

Điều này có nghĩa là ``from sound.effects import *`` sẽ import ba submodule đã nêu tên của package :mod:`!sound.effects`.

Hãy lưu ý rằng các submodule có thể bị che khuất bởi những tên được định nghĩa cục bộ. Ví dụ, nếu bạn thêm một hàm ``reverse`` vào tệp
:file:`sound/effects/__init__.py`, thì ``from sound.effects import *`` sẽ chỉ import hai submodule ``echo`` và ``surround``, nhưng *không* submodule ``reverse``, vì nó bị che khuất bởi hàm ``reverse`` được định nghĩa cục bộ::

    __all__ = [
        "echo",      # tham chiếu đến tệp 'echo.py'
        "surround",  # tham chiếu đến tệp 'surround.py'
        "reverse",   # !!! giờ đây tham chiếu đến hàm 'reverse' !!!
    ]

    def reverse(msg: str):  # <-- tên này che khuất submodule 'reverse.py'
        return msg[::-1]    #     trong trường hợp sử dụng 'from sound.effects import *'

Nếu ``__all__`` chưa được định nghĩa, câu lệnh ``from sound.effects import *`` sẽ *không* import tất cả các submodule từ package :mod:`!sound.effects` vào namespace hiện tại; nó chỉ đảm bảo rằng package :mod:`!sound.effects` đã được import (có thể chạy mọi mã khởi tạo trong :file:`__init__.py`) rồi import mọi tên được định nghĩa trong package. Điều này bao gồm mọi tên được định nghĩa (và các submodule được nạp rõ ràng) bởi :file:`__init__.py`. Nó cũng bao gồm mọi submodule của package đã được nạp rõ ràng bởi các câu lệnh :keyword:`import` trước đó. Hãy xem đoạn mã sau::

   import sound.effects.echo
   import sound.effects.surround
   from sound.effects import *

Trong ví dụ này, các module :mod:`!echo` và :mod:`!surround` được import vào namespace hiện tại vì chúng được định nghĩa trong package :mod:`!sound.effects` khi câu lệnh ``from...import`` được thực thi. (Điều này cũng hoạt động khi ``__all__`` được định nghĩa.)

Mặc dù một số module được thiết kế để chỉ export các tên tuân theo những mẫu nhất định khi bạn sử dụng ``import *``, cách này vẫn được xem là không nên dùng trong mã production.

Hãy nhớ rằng việc sử dụng ``from package import specific_submodule`` hoàn toàn không có gì sai! Trên thực tế, đây là ký hiệu được khuyến nghị, trừ khi module nhập cần sử dụng các submodule cùng tên từ những package khác nhau.


.. _intra-package-references:

Tham chiếu giữa các package
---------------------------

Khi các package được tổ chức thành những subpackage (như package :mod:`!sound` trong ví dụ), bạn có thể sử dụng absolute import để tham chiếu đến các submodule của những package ngang hàng. Ví dụ, nếu module :mod:`!sound.filters.vocoder` cần sử dụng module :mod:`!echo` trong package :mod:`!sound.effects`, nó có thể dùng ``from sound.effects import echo``.

Bạn cũng có thể viết relative import bằng dạng ``from module import name`` của câu lệnh import. Các import này sử dụng những dấu chấm ở đầu để biểu thị package hiện tại và các package cha liên quan trong relative import. Ví dụ, từ module :mod:`!surround`, bạn có thể dùng::

   from . import echo
   from .. import formats
   from ..filters import equalizer

Lưu ý rằng relative import dựa trên tên package của module hiện tại. Vì module chính không thuộc package nào, các module được dùng làm module chính của một ứng dụng Python luôn phải sử dụng absolute import.


.. rubric:: Chú thích cuối trang

.. [#] Thực tế, các định nghĩa hàm cũng là những 'câu lệnh' được 'thực thi'; việc thực thi một định nghĩa hàm ở cấp module sẽ thêm tên hàm vào namespace toàn cục của module.
