.. highlight:: c

.. _initialization:

Khởi tạo và hoàn tất trình thông dịch
=====================================

Xem :ref:`Cấu hình khởi tạo Python <init-config>` để biết chi tiết về cách cấu hình trình thông dịch trước khi khởi tạo.

.. _pre-init-safe:

Trước khi khởi tạo Python
-------------------------

Trong một ứng dụng nhúng Python, phải gọi hàm :c:func:`Py_Initialize` trước khi sử dụng bất kỳ hàm Python/C API nào khác; ngoại trừ một vài hàm và :ref:`các biến cấu hình toàn cục <global-conf-vars>`.

Có thể gọi an toàn các hàm sau trước khi Python được khởi tạo:

* Các hàm khởi tạo trình thông dịch:

  * :c:func:`Py_Initialize`
  * :c:func:`Py_InitializeEx`
  * :c:func:`Py_InitializeFromConfig`
  * :c:func:`Py_BytesMain`
  * :c:func:`Py_Main`
  * các hàm tiền khởi tạo runtime được đề cập trong :ref:`init-config`

* Các hàm cấu hình:

  * :c:func:`PyImport_AppendInittab`
  * :c:func:`PyImport_ExtendInittab`
  * :c:func:`!PyInitFrozenExtensions`
  * :c:func:`PyMem_SetAllocator`
  * :c:func:`PyMem_SetupDebugHooks`
  * :c:func:`PyObject_SetArenaAllocator`
  * :c:func:`Py_SetProgramName`
  * :c:func:`Py_SetPythonHome`
  * các hàm cấu hình được đề cập trong :ref:`init-config`

* Các hàm cung cấp thông tin:

  * :c:func:`Py_IsInitialized`
  * :c:func:`PyMem_GetAllocator`
  * :c:func:`PyObject_GetArenaAllocator`
  * :c:func:`Py_GetBuildInfo`
  * :c:func:`Py_GetCompiler`
  * :c:func:`Py_GetCopyright`
  * :c:func:`Py_GetPlatform`
  * :c:func:`Py_GetVersion`
  * :c:func:`Py_IsInitialized`

* Tiện ích:

  * :c:func:`Py_DecodeLocale`
  * các hàm báo cáo trạng thái và tiện ích được đề cập trong :ref:`init-config`

* Bộ cấp phát bộ nhớ:

  * :c:func:`PyMem_RawMalloc`
  * :c:func:`PyMem_RawRealloc`
  * :c:func:`PyMem_RawCalloc`
  * :c:func:`PyMem_RawFree`

* Đồng bộ hóa:

  * :c:func:`PyMutex_Lock`
  * :c:func:`PyMutex_Unlock`

.. note::

   Mặc dù có vẻ tương tự với một số hàm được liệt kê ở trên, các hàm sau **không nên được gọi** trước khi trình thông dịch được khởi tạo: :c:func:`Py_EncodeLocale`, :c:func:`PyEval_InitThreads`, và
   :c:func:`Py_RunMain`.


.. _global-conf-vars:

Các biến cấu hình toàn cục
--------------------------

Python có các biến dùng cho cấu hình toàn cục để kiểm soát nhiều tính năng và tùy chọn khác nhau. Theo mặc định, các cờ này được điều khiển bằng :ref:`tùy chọn dòng lệnh <using-on-interface-options>`.

Khi một cờ được thiết lập bằng một tùy chọn, giá trị của cờ là số lần tùy chọn đó được thiết lập. Ví dụ, ``-b`` sẽ thiết lập :c:data:`Py_BytesWarningFlag` thành 1 và ``-bb`` sẽ thiết lập :c:data:`Py_BytesWarningFlag` thành 2.


.. c:var:: int Py_BytesWarningFlag

   API này được duy trì để tương thích ngược: việc thiết lập
   :c:member:`PyConfig.bytes_warning` nên được sử dụng thay thế; xem :ref:`Cấu hình khởi tạo Python <init-config>`.

   Phát cảnh báo khi so sánh :class:`bytes` hoặc :class:`bytearray` với
   :class:`str` hoặc :class:`bytes` với :class:`int`. Phát sinh lỗi nếu lớn hơn hoặc bằng ``2``.

   Được thiết lập bằng tùy chọn :option:`-b`.

   .. deprecated-removed:: 3.12 3.15


.. c:var:: int Py_DebugFlag

   API này được duy trì để tương thích ngược: việc thiết lập
   Thay vào đó nên sử dụng :c:member:`PyConfig.parser_debug`, xem :ref:`Cấu hình khởi tạo Python <init-config>`.

   Bật đầu ra gỡ lỗi của parser (chỉ dành cho chuyên gia, tùy thuộc vào các tùy chọn biên dịch).

   Được thiết lập bằng tùy chọn :option:`-d` và biến môi trường :envvar:`PYTHONDEBUG`.

   .. deprecated-removed:: 3.12 3.15


.. c:var:: int Py_DontWriteBytecodeFlag

   API này được duy trì để tương thích ngược: việc thiết lập
   Thay vào đó, nên sử dụng :c:member:`PyConfig.write_bytecode`; xem :ref:`Cấu hình khởi tạo Python <init-config>`.

   Nếu được đặt thành giá trị khác 0, Python sẽ không cố ghi các tệp ``.pyc`` khi import các mô-đun nguồn.

   Được thiết lập bởi tùy chọn :option:`-B` và biến môi trường :envvar:`PYTHONDONTWRITEBYTECODE`.

   .. deprecated-removed:: 3.12 3.15


.. c:var:: int Py_FrozenFlag

   API này được duy trì để tương thích ngược: việc thiết lập
   Thay vào đó, nên sử dụng :c:member:`PyConfig.pathconfig_warnings`; xem
   :ref:`Cấu hình khởi tạo Python <init-config>`.

   Cờ nội bộ được các chương trình ``_freeze_module`` và ``frozenmain`` sử dụng.

   .. deprecated-removed:: 3.12 3.15


.. c:var:: int Py_HashRandomizationFlag

   API này được duy trì để tương thích ngược: việc thiết lập
   Thay vào đó, nên sử dụng :c:member:`PyConfig.hash_seed` và :c:member:`PyConfig.use_hash_seed`; xem :ref:`Cấu hình khởi tạo Python <init-config>`.

   Được đặt thành ``1`` nếu biến môi trường :envvar:`PYTHONHASHSEED` được đặt thành một chuỗi không rỗng.

   Nếu cờ này khác không, hãy đọc biến môi trường :envvar:`PYTHONHASHSEED` để khởi tạo secret hash seed.

   .. deprecated-removed:: 3.12 3.15


.. c:var:: int Py_IgnoreEnvironmentFlag

   API này được duy trì để tương thích ngược: việc thiết lập
   Thay vào đó, nên sử dụng :c:member:`PyConfig.use_environment`; xem
   :ref:`Cấu hình khởi tạo Python <init-config>`.

   Bỏ qua mọi biến môi trường :envvar:`!PYTHON*`, chẳng hạn như
   :envvar:`PYTHONPATH` và :envvar:`PYTHONHOME`, có thể đã được thiết lập.

   Được thiết lập bởi các tùy chọn :option:`-E` và :option:`-I`.

   .. deprecated-removed:: 3.12 3.15


.. c:var:: int Py_InspectFlag

   API này được duy trì để tương thích ngược: việc thiết lập
   Thay vào đó, nên sử dụng :c:member:`PyConfig.inspect`, xem
   :ref:`Cấu hình khởi tạo Python <init-config>`.

   Khi một script được truyền làm đối số đầu tiên hoặc sử dụng tùy chọn :option:`-c`, hãy vào chế độ tương tác sau khi thực thi script hoặc lệnh, ngay cả khi
   :data:`sys.stdin` dường như không phải là một terminal.

   Được thiết lập bằng tùy chọn :option:`-i` và biến môi trường :envvar:`PYTHONINSPECT`.

   .. deprecated-removed:: 3.12 3.15


.. c:var:: int Py_InteractiveFlag

   API này được duy trì để tương thích ngược: việc thiết lập
   Thay vào đó, nên sử dụng :c:member:`PyConfig.interactive`, xem
   :ref:`Cấu hình khởi tạo Python <init-config>`.

   Được thiết lập bằng tùy chọn :option:`-i`.

   .. deprecated-removed:: 3.12 3.15


.. c:var:: int Py_IsolatedFlag

   API này được duy trì để tương thích ngược: việc thiết lập
   Thay vào đó, nên sử dụng :c:member:`PyConfig.isolated`, xem
   :ref:`Cấu hình khởi tạo Python <init-config>`.

   Chạy Python ở chế độ isolated. Ở chế độ isolated, :data:`sys.path` không chứa thư mục của script cũng như thư mục site-packages của người dùng.

   Được thiết lập bởi tùy chọn :option:`-I`.

   .. versionadded:: 3.4

   .. deprecated-removed:: 3.12 3.15


.. c:var:: int Py_LegacyWindowsFSEncodingFlag

   API này được duy trì để tương thích ngược: việc thiết lập
   Thay vào đó, nên sử dụng :c:member:`PyPreConfig.legacy_windows_fs_encoding`, xem
   :ref:`Cấu hình khởi tạo Python <init-config>`.

   Nếu cờ khác 0, hãy sử dụng encoding ``mbcs`` với error handler ``replace``, thay vì encoding UTF-8 với error handler ``surrogatepass``, cho :term:`filesystem encoding and error handler`.

   Đặt thành ``1`` nếu biến môi trường :envvar:`PYTHONLEGACYWINDOWSFSENCODING` được đặt thành một chuỗi không rỗng.

   Xem :pep:`529` để biết thêm chi tiết.

   .. availability:: Windows.

   .. deprecated-removed:: 3.12 3.15


.. c:var:: int Py_LegacyWindowsStdioFlag

   API này được duy trì để tương thích ngược: việc thiết lập
   Thay vào đó nên sử dụng :c:member:`PyConfig.legacy_windows_stdio`, xem
   :ref:`Cấu hình khởi tạo Python <init-config>`.

   Nếu cờ khác 0, hãy sử dụng :class:`io.FileIO` thay vì
   :class:`!io._WindowsConsoleIO` cho các luồng tiêu chuẩn :mod:`sys`.

   Đặt thành ``1`` nếu biến môi trường :envvar:`PYTHONLEGACYWINDOWSSTDIO` được đặt thành một chuỗi không rỗng.

   Xem :pep:`528` để biết thêm chi tiết.

   .. availability:: Windows.

   .. deprecated-removed:: 3.12 3.15


.. c:var:: int Py_NoSiteFlag

   API này được duy trì để tương thích ngược: việc thiết lập
   Thay vào đó nên sử dụng :c:member:`PyConfig.site_import`, xem
   :ref:`Cấu hình khởi tạo Python <init-config>`.

   Tắt việc import module :mod:`site` và các thao tác phụ thuộc vào site đối với :data:`sys.path` mà module này thực hiện. Đồng thời tắt các thao tác này nếu :mod:`site` được import rõ ràng sau đó (gọi
   :func:`site.main` nếu bạn muốn chúng được kích hoạt).

   Được thiết lập bằng tùy chọn :option:`-S`.

   .. deprecated-removed:: 3.12 3.15


.. c:var:: int Py_NoUserSiteDirectory

   API này được duy trì để tương thích ngược: việc thiết lập
   Thay vào đó nên sử dụng :c:member:`PyConfig.user_site_directory`, xem
   :ref:`Cấu hình khởi tạo Python <init-config>`.

   Không thêm :data:`user site-packages directory <site.USER_SITE>` vào
   :data:`sys.path`.

   Được thiết lập bằng các tùy chọn :option:`-s` và :option:`-I`, và
   Biến môi trường :envvar:`PYTHONNOUSERSITE`.

   .. deprecated-removed:: 3.12 3.15


.. c:var:: int Py_OptimizeFlag

   API này được duy trì để tương thích ngược: việc thiết lập
   Nên sử dụng :c:member:`PyConfig.optimization_level` thay thế, xem
   :ref:`Cấu hình khởi tạo Python <init-config>`.

   Được thiết lập bởi tùy chọn :option:`-O` và biến môi trường :envvar:`PYTHONOPTIMIZE`.

   .. deprecated-removed:: 3.12 3.15


.. c:var:: int Py_QuietFlag

   API này được duy trì để tương thích ngược: việc thiết lập
   Nên sử dụng :c:member:`PyConfig.quiet` thay thế, xem :ref:`Cấu hình khởi tạo Python <init-config>`.

   Không hiển thị các thông báo bản quyền và phiên bản, ngay cả trong chế độ tương tác.

   Được thiết lập bởi tùy chọn :option:`-q`.

   .. versionadded:: 3.2

   .. deprecated-removed:: 3.12 3.15


.. c:var:: int Py_UnbufferedStdioFlag

   API này được duy trì để tương thích ngược: việc thiết lập
   Thay vào đó, nên sử dụng :c:member:`PyConfig.buffered_stdio`, xem :ref:`Cấu hình khởi tạo Python <init-config>`.

   Buộc các luồng stdout và stderr không được đệm.

   Được thiết lập bởi tùy chọn :option:`-u` và biến môi trường :envvar:`PYTHONUNBUFFERED`.

   .. deprecated-removed:: 3.12 3.15


.. c:var:: int Py_VerboseFlag

   API này được duy trì để tương thích ngược: việc thiết lập
   Thay vào đó, nên sử dụng :c:member:`PyConfig.verbose`; xem :ref:`Python Initialization Configuration <init-config>`.

   In một thông báo mỗi khi một module được khởi tạo, cho biết vị trí (tên tệp hoặc module tích hợp sẵn) từ đó module được tải. Nếu lớn hơn hoặc bằng ``2``, in một thông báo cho mỗi tệp được kiểm tra khi tìm kiếm một module. Đồng thời cung cấp thông tin về việc dọn dẹp module khi thoát.

   Được thiết lập bởi tùy chọn :option:`-v` và biến môi trường :envvar:`PYTHONVERBOSE`.

   .. deprecated-removed:: 3.12 3.15


Khởi tạo và hoàn tất interpreter
--------------------------------

.. c:function:: void Py_Initialize()

   .. index::
      single: PyEval_InitThreads()
      single: modules (in module sys)
      single: path (in module sys)
      pair: module; builtins
      pair: module; __main__
      pair: module; sys
      triple: module; search; path
      single: Py_FinalizeEx (C function)

   Khởi tạo Python interpreter. Trong một ứng dụng nhúng Python, hàm này nên được gọi trước khi sử dụng bất kỳ hàm Python/C API nào khác; xem
   :ref:`Before Python Initialization <pre-init-safe>` để biết một vài ngoại lệ.

   Thao tác này khởi tạo bảng các module đã tải (``sys.modules``), đồng thời tạo các module nền tảng :mod:`builtins`, :mod:`__main__` và :mod:`sys`. Thao tác này cũng khởi tạo đường dẫn tìm kiếm module (``sys.path``). Thao tác này không thiết lập ``sys.argv``; hãy sử dụng API :ref:`Python Initialization Configuration <init-config>` cho mục đích đó. Đây là thao tác không làm gì khi được gọi lần thứ hai (mà không gọi
   :c:func:`Py_FinalizeEx` đầu tiên). Không có giá trị trả về; đây là lỗi nghiêm trọng nếu quá trình khởi tạo không thành công.

   Sử dụng :c:func:`Py_InitializeFromConfig` để tùy chỉnh
   :ref:`Cấu hình khởi tạo Python <init-config>`.

   .. note::
      Trên Windows, thay đổi chế độ console từ ``O_TEXT`` thành ``O_BINARY``, điều này cũng sẽ ảnh hưởng đến việc sử dụng console không phải Python thông qua C Runtime.


.. c:function:: void Py_InitializeEx(int initsigs)

   Hàm này hoạt động giống :c:func:`Py_Initialize` nếu *initsigs* là ``1``. Nếu *initsigs* là ``0``, hàm sẽ bỏ qua việc đăng ký trình xử lý tín hiệu trong quá trình khởi tạo, điều này có thể hữu ích khi CPython được nhúng như một phần của ứng dụng lớn hơn.

   Sử dụng :c:func:`Py_InitializeFromConfig` để tùy chỉnh
   :ref:`Cấu hình khởi tạo Python <init-config>`.


.. c:function:: PyStatus Py_InitializeFromConfig(const PyConfig *config)

   Khởi tạo Python từ cấu hình *config*, như được mô tả trong
   :ref:`init-from-config`.

   Xem phần :ref:`init-config` để biết chi tiết về việc khởi tạo trước trình thông dịch, điền cấu trúc cấu hình runtime và truy vấn cấu trúc trạng thái được trả về.


.. c:function:: int Py_IsInitialized()

   Trả về true (khác không) khi trình thông dịch Python đã được khởi tạo, false (bằng không) nếu chưa. Sau khi gọi :c:func:`Py_FinalizeEx`, hàm này trả về false cho đến khi
   :c:func:`Py_Initialize` được gọi lại.


.. c:function:: int Py_IsFinalizing()

   Trả về true (khác không) nếu trình thông dịch Python chính đang
   :term:`shutting down <interpreter shutdown>`. Nếu không, trả về false (bằng không).

   .. versionadded:: 3.13


.. c:function:: int Py_FinalizeEx()

   Hủy mọi lần khởi tạo được thực hiện bởi :c:func:`Py_Initialize` và việc sử dụng tiếp theo các hàm Python/C API, đồng thời hủy tất cả các trình thông dịch con (xem
   :c:func:`Py_NewInterpreter` bên dưới) đã được tạo và chưa bị hủy kể từ lần gọi :c:func:`Py_Initialize` gần nhất. Đây là thao tác không làm gì khi được gọi lần thứ hai (mà trước đó không gọi lại :c:func:`Py_Initialize`).

   Vì đây là thao tác ngược với :c:func:`Py_Initialize`, nó phải được gọi trong cùng một thread với cùng interpreter đang hoạt động. Điều đó có nghĩa là main thread và main interpreter. Không được gọi thao tác này khi :c:func:`Py_RunMain` đang chạy.

   Thông thường, giá trị trả về là ``0``. Nếu xảy ra lỗi trong quá trình finalization (xả dữ liệu được đệm), ``-1`` sẽ được trả về.

   Lưu ý rằng Python sẽ cố gắng hết sức để giải phóng toàn bộ bộ nhớ do Python interpreter cấp phát. Vì vậy, mọi C-Extension cần đảm bảo dọn dẹp đúng cách tất cả PyObjects đã được cấp phát trước đó trước khi sử dụng chúng trong các lần gọi tiếp theo tới
   :c:func:`Py_Initialize`. Nếu không, điều này có thể gây ra lỗ hổng và hành vi không chính xác.

   Hàm này được cung cấp vì một số lý do. Một ứng dụng nhúng có thể muốn khởi động lại Python mà không phải khởi động lại chính ứng dụng đó. Một ứng dụng đã nạp Python interpreter từ một thư viện có thể nạp động (hoặc DLL) có thể muốn giải phóng toàn bộ bộ nhớ do Python cấp phát trước khi dỡ DLL. Trong quá trình tìm kiếm memory leak trong một ứng dụng, nhà phát triển có thể muốn giải phóng toàn bộ bộ nhớ do Python cấp phát trước khi thoát ứng dụng.

   **Lỗi và lưu ý:** Việc hủy các module và các object trong module được thực hiện theo thứ tự ngẫu nhiên; điều này có thể khiến các destructor (:meth:`~object.__del__` method) không hoạt động khi chúng phụ thuộc vào các object khác (kể cả function) hoặc module. Các extension module được nạp động bởi Python không bị dỡ. Một lượng nhỏ bộ nhớ do Python interpreter cấp phát có thể không được giải phóng (nếu phát hiện memory leak, vui lòng báo cáo). Bộ nhớ bị giữ lại trong các tham chiếu vòng giữa các object không được giải phóng. Các chuỗi interned sẽ đều được giải cấp phát bất kể reference count của chúng. Một phần bộ nhớ do extension module cấp phát có thể không được giải phóng. Một số extension có thể không hoạt động đúng nếu routine khởi tạo của chúng được gọi nhiều hơn một lần; điều này có thể xảy ra nếu một ứng dụng gọi :c:func:`Py_Initialize` và :c:func:`Py_FinalizeEx` nhiều hơn một lần. Không được gọi :c:func:`Py_FinalizeEx` đệ quy từ bên trong chính nó. Vì vậy, không được gọi hàm này từ bất kỳ code nào có thể được chạy trong quá trình interpreter shutdown, chẳng hạn như các handler của :py:mod:`atexit`, finalizer của object hoặc bất kỳ code nào có thể được chạy trong khi xả các file stdout và stderr.

   .. audit-event:: cpython._PySys_ClearAuditHooks "" c.Py_FinalizeEx

   .. versionadded:: 3.6


.. c:function:: void Py_Finalize()

   Đây là phiên bản tương thích ngược của :c:func:`Py_FinalizeEx`, bỏ qua giá trị trả về.


.. c:function:: int Py_BytesMain(int argc, char **argv)

   Tương tự :c:func:`Py_Main`, nhưng *argv* là một mảng các chuỗi byte, cho phép ứng dụng gọi ủy quyền bước giải mã văn bản cho runtime CPython.

   .. versionadded:: 3.8


.. c:function:: int Py_Main(int argc, wchar_t **argv)

   Chương trình chính cho interpreter tiêu chuẩn, bao hàm một chu kỳ khởi tạo/kết thúc hoàn chỉnh, cũng như hành vi bổ sung để thực hiện việc đọc các thiết lập cấu hình từ môi trường và dòng lệnh, sau đó thực thi ``__main__`` theo
   :ref:`using-on-cmdline`.

   Tính năng này được cung cấp cho các chương trình muốn hỗ trợ đầy đủ giao diện dòng lệnh CPython, thay vì chỉ nhúng một runtime Python vào một ứng dụng lớn hơn.

   Các tham số *argc* và *argv* tương tự các tham số được truyền cho hàm :c:func:`main` của một chương trình C, ngoại trừ việc các mục *argv* trước tiên được chuyển đổi thành ``wchar_t`` bằng :c:func:`Py_DecodeLocale`. Cũng cần lưu ý rằng các mục trong danh sách đối số có thể được sửa đổi để trỏ đến các chuỗi khác với những chuỗi đã truyền vào (tuy nhiên, nội dung của các chuỗi được danh sách đối số trỏ đến không bị sửa đổi).

   Giá trị trả về là ``2`` nếu danh sách đối số không biểu diễn một dòng lệnh Python hợp lệ; nếu không, giá trị này giống với :c:func:`Py_RunMain`.

   Xét theo các API cấu hình runtime CPython được ghi lại trong
   mục :ref:`cấu hình runtime <init-config>` (và không tính đến việc xử lý lỗi), ``Py_Main`` gần tương đương với::

      PyConfig config;
      PyConfig_InitPythonConfig(&config);
      PyConfig_SetArgv(&config, argc, argv);
      Py_InitializeFromConfig(&config);
      PyConfig_Clear(&config);

      Py_RunMain();

   Trong cách sử dụng thông thường, một ứng dụng nhúng sẽ gọi hàm này *thay vì* gọi :c:func:`Py_Initialize`, :c:func:`Py_InitializeEx` hoặc
   :c:func:`Py_InitializeFromConfig` trực tiếp, và tất cả các thiết lập sẽ được áp dụng như mô tả ở phần khác trong tài liệu này. Nếu thay vào đó hàm này được gọi *sau* một lệnh gọi API khởi tạo runtime trước đó, thì chính xác những thiết lập cấu hình môi trường và dòng lệnh nào được cập nhật sẽ phụ thuộc vào phiên bản (vì điều này phụ thuộc vào việc những thiết lập nào hỗ trợ đúng cách việc sửa đổi sau khi chúng đã được thiết lập một lần trong lần đầu runtime được khởi tạo).


.. c:function:: int Py_RunMain(void)

   Thực thi module chính trong một runtime CPython đã được cấu hình đầy đủ.

   Thực thi lệnh (:c:member:`PyConfig.run_command`), script (:c:member:`PyConfig.run_filename`) hoặc module (:c:member:`PyConfig.run_module`) được chỉ định trên dòng lệnh hoặc trong cấu hình. Nếu không có giá trị nào được thiết lập, chạy lời nhắc Python tương tác (REPL) bằng namespace toàn cục của module ``__main__``.

   Nếu :c:member:`PyConfig.inspect` chưa được thiết lập (mặc định), giá trị trả về sẽ là ``0`` nếu interpreter thoát bình thường (nghĩa là không phát sinh ngoại lệ), trạng thái thoát của một :exc:`SystemExit` chưa được xử lý, hoặc ``1`` đối với mọi ngoại lệ chưa được xử lý khác.

   Nếu :c:member:`PyConfig.inspect` được thiết lập (chẳng hạn khi sử dụng tùy chọn :option:`-i`), thay vì trả về khi interpreter thoát, quá trình thực thi sẽ tiếp tục trong một lời nhắc Python tương tác (REPL) bằng namespace toàn cục của module ``__main__``. Nếu interpreter thoát do một ngoại lệ, ngoại lệ đó sẽ được phát sinh ngay lập tức trong phiên REPL. Giá trị trả về của hàm sau đó được xác định bởi cách *phiên REPL* kết thúc: ``0``, ``1`` hoặc trạng thái của một :exc:`SystemExit`, như đã nêu ở trên.

   Hàm này luôn hoàn tất việc kết thúc trình thông dịch Python trước khi trả về.

   Xem :ref:`Python Configuration <init-python-config>` để biết ví dụ về một Python đã tùy chỉnh luôn chạy ở chế độ cô lập bằng cách sử dụng
   :c:func:`Py_RunMain`.

.. c:function:: int PyUnstable_AtExit(PyInterpreterState *interp, void (*func)(void *), void *data)

   Đăng ký một :mod:`atexit` callback cho trình thông dịch đích *interp*. Điều này tương tự như :c:func:`Py_AtExit`, nhưng nhận một trình thông dịch và con trỏ dữ liệu tường minh cho callback.

   Phải có một :term:`attached thread state` cho *interp*.

   .. versionadded:: 3.13


.. _cautions-regarding-runtime-finalization:

Các lưu ý về việc kết thúc runtime
----------------------------------

Trong giai đoạn cuối của :term:`interpreter shutdown`, sau khi cố gắng chờ các thread không phải daemon thoát (mặc dù việc này có thể bị gián đoạn bởi
:class:`KeyboardInterrupt`) và chạy các hàm :mod:`atexit`, runtime được đánh dấu là *finalizing*: :c:func:`Py_IsFinalizing` và
:func:`sys.is_finalizing` trả về true.  Tại thời điểm này, chỉ *thread finalization* đã khởi tạo quá trình finalization (thường là thread chính) mới được phép acquire :term:`GIL`.

Nếu bất kỳ thread nào, ngoài thread finalization, cố gắng attach một :term:`thread state` trong quá trình finalization, dù rõ ràng hay ngầm định, thread đó sẽ chuyển sang **trạng thái bị chặn vĩnh viễn** và ở đó cho đến khi chương trình kết thúc.  Trong hầu hết trường hợp, điều này không gây hại, nhưng có thể dẫn đến deadlock nếu một giai đoạn finalization sau đó cố gắng acquire một lock do thread bị chặn sở hữu, hoặc chờ thread bị chặn theo cách khác.

Khó chịu? Đúng vậy. Điều này ngăn các sự cố ngẫu nhiên và/hoặc việc bỏ qua ngoài dự kiến các quá trình finalization C++ ở phía trên call stack khi những thread như vậy bị buộc thoát tại đây trong CPython 3.13 và các phiên bản cũ hơn. Các API C :term:`thread state` runtime của CPython chưa bao giờ có yêu cầu về việc báo cáo hoặc xử lý lỗi tại :term:`thread state` thời điểm attach, cho phép thoát khỏi tình huống này một cách an toàn. Việc thay đổi điều đó sẽ đòi hỏi các API C ổn định mới và viết lại phần lớn mã C trong hệ sinh thái CPython để sử dụng chúng cùng với việc xử lý lỗi.


Các tham số áp dụng trên toàn process
-------------------------------------

.. c:function:: void Py_SetProgramName(const wchar_t *name)

   .. index::
      single: Py_Initialize()
      single: main()
      single: Py_GetPath()

   API này được duy trì để tương thích ngược: việc thiết lập
   :c:member:`PyConfig.program_name` nên được sử dụng thay vào đó, xem :ref:`Python Initialization Configuration <init-config>`.

   Hàm này nên được gọi trước khi :c:func:`Py_Initialize` được gọi lần đầu tiên, nếu hàm đó được gọi.  Hàm này cho interpreter biết giá trị của đối số ``argv[0]`` cho hàm :c:func:`main` của chương trình (được chuyển đổi thành các ký tự wide). Giá trị này được :c:func:`Py_GetPath` và một số hàm khác bên dưới sử dụng để tìm các thư viện run-time của Python tương đối với tệp thực thi của interpreter.  Giá trị mặc định là ``'python'``.  Đối số phải trỏ đến một chuỗi ký tự wide kết thúc bằng zero trong vùng lưu trữ tĩnh, với nội dung không thay đổi trong suốt thời gian thực thi của chương trình.  Không có mã nào trong interpreter Python thay đổi nội dung của vùng lưu trữ này.

   Sử dụng :c:func:`Py_DecodeLocale` để giải mã một chuỗi bytes thành một
   chuỗi :c:expr:`wchar_t*`.

   .. deprecated-removed:: 3.11 3.15


.. c:function:: wchar_t* Py_GetProgramName()

   Trả về tên chương trình được đặt bằng :c:member:`PyConfig.program_name`, hoặc giá trị mặc định. Chuỗi được trả về trỏ đến vùng lưu trữ tĩnh; bên gọi không nên sửa đổi giá trị của nó.

   Không nên gọi hàm này trước :c:func:`Py_Initialize`, nếu không hàm sẽ trả về ``NULL``.

   .. versionchanged:: 3.10
      Hiện tại, hàm trả về ``NULL`` nếu được gọi trước :c:func:`Py_Initialize`.

   .. deprecated-removed:: 3.13 3.15
      Thay vào đó, hãy sử dụng :c:func:`PyConfig_Get("executable") <PyConfig_Get>` (:data:`sys.executable`).


.. c:function:: wchar_t* Py_GetPrefix()

   Trả về *prefix* của các tệp độc lập với nền tảng đã được cài đặt. Giá trị này được suy ra thông qua một số quy tắc phức tạp từ tên chương trình được đặt bằng
   :c:member:`PyConfig.program_name` và một số biến môi trường; ví dụ, nếu tên chương trình là ``'/usr/local/bin/python'``, tiền tố là ``'/usr/local'``. Chuỗi được trả về trỏ vào vùng lưu trữ tĩnh; bên gọi không nên sửa đổi giá trị của chuỗi. Điều này tương ứng với biến :makevar:`prefix` trong cấp cao nhất
   :file:`Makefile` và đối số :option:`--prefix` của script :program:`configure` tại thời điểm build. Giá trị này có sẵn trong mã Python dưới dạng ``sys.base_prefix``. Nó chỉ hữu ích trên Unix. Xem thêm hàm tiếp theo.

   Không nên gọi hàm này trước :c:func:`Py_Initialize`, nếu không hàm sẽ trả về ``NULL``.

   .. versionchanged:: 3.10
      Hiện tại, hàm trả về ``NULL`` nếu được gọi trước :c:func:`Py_Initialize`.

   .. deprecated-removed:: 3.13 3.15
      Thay vào đó, hãy dùng :c:func:`PyConfig_Get("base_prefix") <PyConfig_Get>` (:data:`sys.base_prefix`). Hãy dùng :c:func:`PyConfig_Get("prefix") <PyConfig_Get>` (:data:`sys.prefix`) nếu cần xử lý :ref:`môi trường ảo <venv-def>`.


.. c:function:: wchar_t* Py_GetExecPrefix()

   Trả về *exec-prefix* cho các tệp đã cài đặt *phụ thuộc* nền tảng. Giá trị này được suy ra thông qua một số quy tắc phức tạp từ tên chương trình được thiết lập bằng
   :c:member:`PyConfig.program_name` và một số biến môi trường; ví dụ, nếu tên chương trình là ``'/usr/local/bin/python'``, exec-prefix là ``'/usr/local'``. Chuỗi được trả về trỏ vào vùng lưu trữ tĩnh; bên gọi không nên sửa đổi giá trị của chuỗi. Điều này tương ứng với biến :makevar:`exec_prefix` trong :file:`Makefile` cấp cao nhất và đối số ``--exec-prefix`` của script :program:`configure` tại thời điểm build. Giá trị này có sẵn trong mã Python dưới dạng ``sys.base_exec_prefix``. Nó chỉ hữu ích trên Unix.

   Bối cảnh: exec-prefix khác với prefix khi các tệp phụ thuộc nền tảng (chẳng hạn như tệp thực thi và thư viện dùng chung) được cài đặt trong một cây thư mục khác. Trong một bản cài đặt điển hình, các tệp phụ thuộc nền tảng có thể được cài đặt trong cây con :file:`/usr/local/plat`, còn các tệp độc lập với nền tảng có thể được cài đặt trong :file:`/usr/local`.

   Nói chung, một nền tảng là sự kết hợp của các dòng phần cứng và phần mềm, ví dụ: các máy Sparc chạy hệ điều hành Solaris 2.x được xem là cùng một nền tảng, nhưng các máy Intel chạy Solaris 2.x là một nền tảng khác, còn các máy Intel chạy Linux lại là một nền tảng khác nữa. Các bản sửa đổi chính khác nhau của cùng một hệ điều hành nhìn chung cũng tạo thành các nền tảng khác nhau. Các hệ điều hành không phải Unix lại là một trường hợp khác; chiến lược cài đặt trên các hệ thống đó khác biệt đến mức prefix và exec-prefix trở nên vô nghĩa và được đặt thành chuỗi rỗng. Lưu ý rằng các tệp bytecode Python đã biên dịch là độc lập với nền tảng (nhưng không độc lập với phiên bản Python dùng để biên dịch chúng!).

   Các quản trị viên hệ thống sẽ biết cách cấu hình các chương trình :program:`mount` hoặc
   các chương trình :program:`automount` để chia sẻ :file:`/usr/local` giữa các nền tảng, đồng thời để :file:`/usr/local/plat` là một hệ thống tệp khác nhau cho mỗi nền tảng.

   Không nên gọi hàm này trước :c:func:`Py_Initialize`, nếu không hàm sẽ trả về ``NULL``.

   .. versionchanged:: 3.10
      Hiện tại, hàm trả về ``NULL`` nếu được gọi trước :c:func:`Py_Initialize`.

   .. deprecated-removed:: 3.13 3.15
      Thay vào đó, hãy sử dụng :c:func:`PyConfig_Get("base_exec_prefix") <PyConfig_Get>` (:data:`sys.base_exec_prefix`). Hãy sử dụng
      :c:func:`PyConfig_Get("exec_prefix") <PyConfig_Get>` (:data:`sys.exec_prefix`) nếu cần xử lý :ref:`virtual environments <venv-def>`.


.. c:function:: wchar_t* Py_GetProgramFullPath()

   .. index::
      single: executable (in module sys)

   Trả về tên đầy đủ của chương trình thực thi Python; giá trị này được tính như một tác dụng phụ của việc suy ra đường dẫn tìm kiếm module mặc định từ tên chương trình (được đặt bởi :c:member:`PyConfig.program_name`). Chuỗi được trả về trỏ vào vùng lưu trữ tĩnh; bên gọi không nên sửa đổi giá trị của nó. Giá trị này có sẵn trong mã Python dưới dạng ``sys.executable``.

   Không nên gọi hàm này trước :c:func:`Py_Initialize`, nếu không hàm sẽ trả về ``NULL``.

   .. versionchanged:: 3.10
      Hiện tại, hàm trả về ``NULL`` nếu được gọi trước :c:func:`Py_Initialize`.

   .. deprecated-removed:: 3.13 3.15
      Thay vào đó, hãy sử dụng :c:func:`PyConfig_Get("executable") <PyConfig_Get>` (:data:`sys.executable`).


.. c:function:: wchar_t* Py_GetPath()

   .. index::
      triple: module; search; path
      single: path (in module sys)

   Trả về đường dẫn tìm kiếm module mặc định; giá trị này được tính từ tên chương trình (được đặt bởi :c:member:`PyConfig.program_name`) và một số biến môi trường. Chuỗi được trả về bao gồm một loạt tên thư mục, được phân tách bằng một ký tự dấu phân cách phụ thuộc vào nền tảng. Ký tự dấu phân cách là ``':'`` trên Unix và macOS, ``';'`` trên Windows. Chuỗi được trả về trỏ vào vùng lưu trữ tĩnh; bên gọi không nên sửa đổi giá trị của nó. Danh sách
   :data:`sys.path` được khởi tạo bằng giá trị này khi trình thông dịch khởi động; về sau, giá trị này có thể được (và thường được) sửa đổi để thay đổi đường dẫn tìm kiếm dùng cho việc tải module.

   Không nên gọi hàm này trước :c:func:`Py_Initialize`, nếu không hàm sẽ trả về ``NULL``.

   .. XXX should give the exact rules

   .. versionchanged:: 3.10
      Hiện tại, hàm trả về ``NULL`` nếu được gọi trước :c:func:`Py_Initialize`.

   .. deprecated-removed:: 3.13 3.15
      Thay vào đó, hãy sử dụng :c:func:`PyConfig_Get("module_search_paths") <PyConfig_Get>` (:data:`sys.path`).

.. c:function:: const char* Py_GetVersion()

   Trả về phiên bản của trình thông dịch Python này. Đây là một chuỗi có dạng gần giống như sau::

      "3.0a5+ (py3k:63103M, May 12 2008, 00:53:55) \n[GCC 4.2.3]"

   .. index:: single: version (in module sys)

   Từ đầu tiên (cho đến ký tự khoảng trắng đầu tiên) là phiên bản Python hiện tại; các ký tự đầu tiên là phiên bản chính và phiên bản phụ được phân tách bằng dấu chấm. Chuỗi được trả về trỏ đến vùng lưu trữ tĩnh; bên gọi không nên sửa đổi giá trị của chuỗi. Giá trị này có sẵn trong mã Python với tên :data:`sys.version`.

   Xem thêm hằng số :c:var:`Py_Version`.


.. c:function:: const char* Py_GetPlatform()

   .. index:: single: platform (in module sys)

   Trả về mã định danh nền tảng của nền tảng hiện tại. Trên Unix, mã này được tạo từ tên "chính thức" của hệ điều hành, được chuyển thành chữ thường, theo sau là số hiệu chỉnh chính; ví dụ: với Solaris 2.x, cũng được gọi là SunOS 5.x, giá trị là ``'sunos5'``. Trên macOS, giá trị là ``'darwin'``. Trên Windows, giá trị là ``'win'``. Chuỗi được trả về trỏ đến vùng lưu trữ tĩnh; bên gọi không nên sửa đổi giá trị của chuỗi. Giá trị này có sẵn trong mã Python với tên ``sys.platform``.


.. c:function:: const char* Py_GetCopyright()

   Trả về chuỗi bản quyền chính thức cho phiên bản Python hiện tại, ví dụ

   ``'Copyright 1991-1995 Stichting Mathematisch Centrum, Amsterdam'``

   .. index:: single: copyright (in module sys)

   Chuỗi được trả về trỏ đến vùng lưu trữ tĩnh; bên gọi không nên sửa đổi giá trị của chuỗi. Giá trị này có sẵn trong mã Python dưới dạng ``sys.copyright``.


.. c:function:: const char* Py_GetCompiler()

   Trả về thông tin cho biết compiler được sử dụng để xây dựng phiên bản Python hiện tại, nằm trong dấu ngoặc vuông, ví dụ::

      "[GCC 2.7.2.2]"

   .. index:: single: version (in module sys)

   Chuỗi được trả về trỏ đến vùng lưu trữ tĩnh; bên gọi không nên sửa đổi giá trị của chuỗi. Giá trị này có sẵn trong mã Python dưới dạng một phần của biến ``sys.version``.


.. c:function:: const char* Py_GetBuildInfo()

   Trả về thông tin về số thứ tự, ngày và thời gian build của phiên bản Python hiện tại, ví dụ::

      "#67, Aug  1 1997, 22:34:28"

   .. index:: single: version (in module sys)

   Chuỗi được trả về trỏ đến vùng lưu trữ tĩnh; bên gọi không nên sửa đổi giá trị của chuỗi. Giá trị này có sẵn trong mã Python dưới dạng một phần của biến ``sys.version``.


.. c:function:: void PySys_SetArgvEx(int argc, wchar_t **argv, int updatepath)

   .. index::
      single: main()
      single: Py_FatalError()
      single: argv (in module sys)

   API này được duy trì để tương thích ngược: việc thiết lập
   :c:member:`PyConfig.argv`, :c:member:`PyConfig.parse_argv` và
   thay vào đó nên sử dụng :c:member:`PyConfig.safe_path`, xem :ref:`Python Initialization Configuration <init-config>`.

   Đặt :data:`sys.argv` dựa trên *argc* và *argv*. Các tham số này tương tự như các tham số được truyền cho hàm :c:func:`main` của chương trình, với điểm khác biệt là mục nhập đầu tiên phải trỏ đến tệp script sẽ được thực thi thay vì tệp thực thi lưu trữ trình thông dịch Python. Nếu không có script nào được chạy, mục nhập đầu tiên trong *argv* có thể là một chuỗi rỗng. Nếu hàm này không khởi tạo được :data:`sys.argv`, một điều kiện nghiêm trọng sẽ được báo hiệu bằng :c:func:`Py_FatalError`.

   Nếu *updatepath* bằng không, đó là tất cả những gì hàm thực hiện. Nếu *updatepath* khác không, hàm cũng sửa đổi :data:`sys.path` theo thuật toán sau:

   - Nếu tên của một script hiện có được truyền trong ``argv[0]``, đường dẫn tuyệt đối của thư mục chứa script đó được thêm vào đầu
     :data:`sys.path`.
   - Ngược lại (nghĩa là nếu *argc* là ``0`` hoặc ``argv[0]`` không trỏ đến một tên tệp hiện có), một chuỗi rỗng được thêm vào đầu
     :data:`sys.path`, tương đương với việc thêm thư mục làm việc hiện tại (``"."``) vào đầu.

   Sử dụng :c:func:`Py_DecodeLocale` để giải mã một chuỗi bytes thành một
   chuỗi :c:expr:`wchar_t*`.

   Xem thêm các thành viên :c:member:`PyConfig.orig_argv` và :c:member:`PyConfig.argv` của :ref:`Python Initialization Configuration <init-config>`.

   .. note::
      Khuyến nghị rằng các ứng dụng nhúng trình thông dịch Python cho mục đích khác ngoài việc thực thi một tập lệnh duy nhất hãy truyền ``0`` dưới dạng *updatepath*, rồi tự cập nhật :data:`sys.path` nếu muốn. Xem :cve:`2008-5983`.

      Trên các phiên bản trước 3.1.3, bạn có thể đạt được hiệu ứng tương tự bằng cách tự xóa phần tử :data:`sys.path` đầu tiên sau khi đã gọi
      :c:func:`PySys_SetArgv`, chẳng hạn bằng cách sử dụng::

         PyRun_SimpleString("import sys; sys.path.pop(0)\n");

   .. versionadded:: 3.1.3

   .. deprecated-removed:: 3.11 3.15


.. c:function:: void PySys_SetArgv(int argc, wchar_t **argv)

   API này được duy trì để tương thích ngược: việc thiết lập
   :c:member:`PyConfig.argv` và :c:member:`PyConfig.parse_argv` nên được sử dụng thay thế, xem :ref:`Python Initialization Configuration <init-config>`.

   Hàm này hoạt động như :c:func:`PySys_SetArgvEx` với *updatepath* được đặt thành ``1`` trừ khi trình thông dịch :program:`python` được khởi động với
   :option:`-I`.

   Sử dụng :c:func:`Py_DecodeLocale` để giải mã một chuỗi bytes thành một
   chuỗi :c:expr:`wchar_t*`.

   Xem thêm các thành viên :c:member:`PyConfig.orig_argv` và :c:member:`PyConfig.argv` của :ref:`Python Initialization Configuration <init-config>`.

   .. versionchanged:: 3.4 Giá trị *updatepath* phụ thuộc vào :option:`-I`.

   .. deprecated-removed:: 3.11 3.15


.. c:function:: void Py_SetPythonHome(const wchar_t *home)

   API này được duy trì để tương thích ngược: việc thiết lập
   Thay vào đó nên sử dụng :c:member:`PyConfig.home`, xem :ref:`Python Initialization Configuration <init-config>`.

   Đặt thư mục "home" mặc định, tức là vị trí của các thư viện Python chuẩn. Xem :envvar:`PYTHONHOME` để biết ý nghĩa của chuỗi đối số.

   Đối số này phải trỏ đến một chuỗi ký tự kết thúc bằng số 0 trong vùng lưu trữ tĩnh, với nội dung không thay đổi trong suốt thời gian chương trình thực thi. Không có mã nào trong trình thông dịch Python thay đổi nội dung của vùng lưu trữ này.

   Sử dụng :c:func:`Py_DecodeLocale` để giải mã một chuỗi bytes thành một
   chuỗi :c:expr:`wchar_t*`.

   .. deprecated-removed:: 3.11 3.15


.. c:function:: wchar_t* Py_GetPythonHome()

   Trả về giá trị "home" mặc định, tức là giá trị được đặt bởi
   :c:member:`PyConfig.home`, hoặc giá trị của biến môi trường :envvar:`PYTHONHOME` nếu biến này được đặt.

   Không nên gọi hàm này trước :c:func:`Py_Initialize`, nếu không hàm sẽ trả về ``NULL``.

   .. versionchanged:: 3.10
      Hiện tại, hàm trả về ``NULL`` nếu được gọi trước :c:func:`Py_Initialize`.

   .. deprecated-removed:: 3.13 3.15
      Sử dụng :c:func:`PyConfig_Get("home") <PyConfig_Get>` hoặc
      biến môi trường :envvar:`PYTHONHOME` thay vào đó.
