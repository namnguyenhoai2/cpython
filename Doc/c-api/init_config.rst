.. highlight:: c

.. _init-config:

************************
Cấu hình khởi tạo Python
************************


.. _pyinitconfig_api:

C API PyInitConfig
==================

.. versionadded:: 3.14

Python có thể được khởi tạo bằng :c:func:`Py_InitializeFromInitConfig`.

Hàm :c:func:`Py_RunMain` có thể được sử dụng để viết một chương trình Python tùy chỉnh.

Xem thêm :ref:`Initialization, Finalization, and Threads <initialization>`.

.. seealso::
   :pep:`741` "Python Configuration C API".


Ví dụ
-----

Ví dụ về Python tùy chỉnh luôn chạy với :ref:`Python Development Mode <devmode>` được bật; trả về ``-1`` khi có lỗi:

.. code-block:: c

    int init_python(void)
    {
        PyInitConfig *config = PyInitConfig_Create();
        if (config == NULL) {
            printf("PYTHON INIT ERROR: memory allocation failed\n");
            return -1;
        }

        // Bật Python Development Mode
        if (PyInitConfig_SetInt(config, "dev_mode", 1) < 0) {
            goto error;
        }

        // Khởi tạo Python với cấu hình
        if (Py_InitializeFromInitConfig(config) < 0) {
            goto error;
        }
        PyInitConfig_Free(config);
        return 0;

    error:
        {
            // Hiển thị thông báo lỗi.
            //
            // Kiểu dấu ngoặc nhọn không phổ biến này được sử dụng vì bạn không thể khiến
            // các đích goto trỏ đến khai báo biến.
            const char *err_msg;
            (void)PyInitConfig_GetError(config, &err_msg);
            printf("PYTHON INIT ERROR: %s\n", err_msg);
            PyInitConfig_Free(config);
            return -1;
        }
    }

Tạo Config
----------

.. c:struct:: PyInitConfig

   Cấu trúc opaque để cấu hình việc khởi tạo Python.


.. c:function:: PyInitConfig* PyInitConfig_Create(void)

   Tạo một cấu hình khởi tạo mới bằng các giá trị mặc định của :ref:`Cấu hình biệt lập <init-isolated-conf>`.

   Phải giải phóng cấu hình này bằng :c:func:`PyInitConfig_Free`.

   Trả về ``NULL`` nếu cấp phát bộ nhớ không thành công.


.. c:function:: void PyInitConfig_Free(PyInitConfig *config)

   Giải phóng bộ nhớ của cấu hình khởi tạo *config*.

   Nếu *config* là ``NULL``, không thực hiện thao tác nào.


Xử lý lỗi
---------

.. c:function:: int PyInitConfig_GetError(PyInitConfig* config, const char **err_msg)

   Lấy thông báo lỗi của *config*.

   * Đặt *\*err_msg* và trả về ``1`` nếu đã thiết lập lỗi.
   * Đặt *\*err_msg* thành ``NULL`` và trả về ``0`` nếu không.

   Thông báo lỗi là một chuỗi được mã hóa UTF-8.

   Nếu *config* có mã thoát, hãy định dạng mã thoát thành thông báo lỗi.

   Thông báo lỗi vẫn hợp lệ cho đến khi một ``PyInitConfig`` function khác được gọi với *config*. Bên gọi không cần giải phóng thông báo lỗi.


.. c:function:: int PyInitConfig_GetExitCode(PyInitConfig* config, int *exitcode)

   Lấy mã thoát của *config*.

   * Đặt *\*exitcode* và trả về ``1`` nếu *config* đã được thiết lập mã thoát.
   * Trả về ``0`` nếu *config* chưa được đặt mã thoát.

   Chỉ hàm ``Py_InitializeFromInitConfig()`` mới có thể đặt mã thoát nếu tùy chọn ``parse_argv`` khác không.

   Mã thoát có thể được đặt khi quá trình phân tích dòng lệnh không thành công (mã thoát ``2``) hoặc khi một tùy chọn dòng lệnh yêu cầu hiển thị trợ giúp dòng lệnh (mã thoát ``0``).


Lấy tùy chọn
------------

Tham số *name* của tùy chọn cấu hình phải là một chuỗi được mã hóa UTF-8, kết thúc bằng null và khác NULL. Xem :ref:`Configuration Options <pyinitconfig-opts>`.

.. c:function:: int PyInitConfig_HasOption(PyInitConfig *config, const char *name)

   Kiểm tra xem cấu hình có tùy chọn tên *name* hay không.

   Trả về ``1`` nếu tùy chọn tồn tại hoặc trả về ``0`` nếu không.


.. c:function:: int PyInitConfig_GetInt(PyInitConfig *config, const char *name, int64_t *value)

   Lấy một tùy chọn cấu hình kiểu số nguyên.

   * Đặt *\*value*, và trả về ``0`` khi thành công.
   * Đặt một lỗi trong *config* và trả về ``-1`` khi có lỗi.


.. c:function:: int PyInitConfig_GetStr(PyInitConfig *config, const char *name, char **value)

   Lấy một tùy chọn cấu hình chuỗi dưới dạng chuỗi được mã hóa UTF-8 kết thúc bằng null.

   * Đặt *\*value*, và trả về ``0`` khi thành công.
   * Đặt một lỗi trong *config* và trả về ``-1`` khi có lỗi.

   *\*value* có thể được đặt thành ``NULL`` nếu tùy chọn là một chuỗi không bắt buộc và chưa được thiết lập.

   Khi thành công, phải giải phóng chuỗi bằng ``free(value)`` nếu chuỗi không phải là ``NULL``.


.. c:function:: int PyInitConfig_GetStrList(PyInitConfig *config, const char *name, size_t *length, char ***items)

   Lấy tùy chọn cấu hình danh sách chuỗi dưới dạng một mảng các chuỗi được mã hóa UTF-8 và kết thúc bằng ký tự null.

   * Đặt *\*length* và *\*value*, rồi trả về ``0`` khi thành công.
   * Đặt một lỗi trong *config* và trả về ``-1`` khi có lỗi.

   Khi thành công, phải giải phóng danh sách chuỗi bằng ``PyInitConfig_FreeStrList(length, items)``.


.. c:function:: void PyInitConfig_FreeStrList(size_t length, char **items)

   Giải phóng bộ nhớ của danh sách chuỗi được tạo bởi ``PyInitConfig_GetStrList()``.


Đặt tùy chọn
------------

Tham số *name* của tùy chọn cấu hình phải là một chuỗi được mã hóa UTF-8, kết thúc bằng null và khác NULL. Xem :ref:`Configuration Options <pyinitconfig-opts>`.

Một số tùy chọn cấu hình có tác dụng phụ đối với các tùy chọn khác. Logic này chỉ được triển khai khi ``Py_InitializeFromInitConfig()`` được gọi, không phải bởi các hàm "Set" bên dưới. Ví dụ, việc đặt ``dev_mode`` thành ``1`` không đặt ``faulthandler`` thành ``1``.

.. c:function:: int PyInitConfig_SetInt(PyInitConfig *config, const char *name, int64_t value)

   Đặt một tùy chọn cấu hình dạng số nguyên.

   * Trả về ``0`` khi thành công.
   * Đặt lỗi trong *config* và trả về ``-1`` khi có lỗi.


.. c:function:: int PyInitConfig_SetStr(PyInitConfig *config, const char *name, const char *value)

   Đặt một tùy chọn cấu hình dạng chuỗi từ một chuỗi được mã hóa UTF-8, kết thúc bằng null. Chuỗi được sao chép.

   * Trả về ``0`` khi thành công.
   * Đặt lỗi trong *config* và trả về ``-1`` khi có lỗi.


.. c:function:: int PyInitConfig_SetStrList(PyInitConfig *config, const char *name, size_t length, char * const *items)

   Đặt một tùy chọn cấu hình danh sách chuỗi từ một mảng các chuỗi được mã hóa UTF-8 và kết thúc bằng null. Danh sách chuỗi được sao chép.

   * Trả về ``0`` khi thành công.
   * Đặt lỗi trong *config* và trả về ``-1`` khi có lỗi.


Mô-đun
------

.. c:function:: int PyInitConfig_AddModule(PyInitConfig *config, const char *name, PyObject* (*initfunc)(void))

   Thêm một mô-đun mở rộng tích hợp sẵn vào bảng các mô-đun tích hợp sẵn.

   Mô-đun mới có thể được nhập bằng tên *name*, và sử dụng hàm *initfunc* làm hàm khởi tạo được gọi khi lần đầu tiên thử nhập.

   * Trả về ``0`` khi thành công.
   * Đặt một lỗi trong *config* và trả về ``-1`` khi xảy ra lỗi.

   Nếu Python được khởi tạo nhiều lần, phải gọi ``PyInitConfig_AddModule()`` ở mỗi lần khởi tạo Python.

   Tương tự như hàm :c:func:`PyImport_AppendInittab`.


Khởi tạo Python
---------------

.. c:function:: int Py_InitializeFromInitConfig(PyInitConfig *config)

   Khởi tạo Python từ cấu hình khởi tạo.

   * Trả về ``0`` khi thành công.
   * Đặt một lỗi trong *config* và trả về ``-1`` khi xảy ra lỗi.
   * Đặt mã thoát trong *config* và trả về ``-1`` nếu Python muốn thoát.

   Xem ``PyInitConfig_GetExitcode()`` để biết trường hợp mã thoát.


.. _pyinitconfig-opts:

Tùy chọn cấu hình
=================

.. list-table::
   :header-rows: 1

   * - Tùy chọn
     - thành viên PyConfig/PyPreConfig
     - Kiểu
     - Khả năng hiển thị
   * - ``"allocator"``
     - :c:member:`allocator <PyPreConfig.allocator>`
     - ``int``
     - Chỉ đọc
   * - ``"argv"``
     - :c:member:`argv <PyConfig.argv>`
     - ``list[str]``
     - Công khai
   * - ``"base_exec_prefix"``
     - :c:member:`base_exec_prefix <PyConfig.base_exec_prefix>`
     - ``str``
     - Công khai
   * - ``"base_executable"``
     - :c:member:`base_executable <PyConfig.base_executable>`
     - ``str``
     - Công khai
   * - ``"base_prefix"``
     - :c:member:`base_prefix <PyConfig.base_prefix>`
     - ``str``
     - Công khai
   * - ``"buffered_stdio"``
     - :c:member:`buffered_stdio <PyConfig.buffered_stdio>`
     - ``bool``
     - Chỉ đọc
   * - ``"bytes_warning"``
     - :c:member:`bytes_warning <PyConfig.bytes_warning>`
     - ``int``
     - Công khai
   * - ``"check_hash_pycs_mode"``
     - :c:member:`check_hash_pycs_mode <PyConfig.check_hash_pycs_mode>`
     - ``str``
     - Chỉ đọc
   * - ``"code_debug_ranges"``
     - :c:member:`code_debug_ranges <PyConfig.code_debug_ranges>`
     - ``bool``
     - Chỉ đọc
   * - ``"coerce_c_locale"``
     - :c:member:`coerce_c_locale <PyPreConfig.coerce_c_locale>`
     - ``bool``
     - Chỉ đọc
   * - ``"coerce_c_locale_warn"``
     - :c:member:`coerce_c_locale_warn <PyPreConfig.coerce_c_locale_warn>`
     - ``bool``
     - Chỉ đọc
   * - ``"configure_c_stdio"``
     - :c:member:`configure_c_stdio <PyConfig.configure_c_stdio>`
     - ``bool``
     - Chỉ đọc
   * - ``"configure_locale"``
     - :c:member:`configure_locale <PyPreConfig.configure_locale>`
     - ``bool``
     - Chỉ đọc
   * - ``"cpu_count"``
     - :c:member:`cpu_count <PyConfig.cpu_count>`
     - ``int``
     - Công khai
   * - ``"dev_mode"``
     - :c:member:`dev_mode <PyConfig.dev_mode>`
     - ``bool``
     - Chỉ đọc
   * - ``"dump_refs"``
     - :c:member:`dump_refs <PyConfig.dump_refs>`
     - ``bool``
     - Chỉ đọc
   * - ``"dump_refs_file"``
     - :c:member:`dump_refs_file <PyConfig.dump_refs_file>`
     - ``str``
     - Chỉ đọc
   * - ``"exec_prefix"``
     - :c:member:`exec_prefix <PyConfig.exec_prefix>`
     - ``str``
     - Công khai
   * - ``"executable"``
     - :c:member:`executable <PyConfig.executable>`
     - ``str``
     - Công khai
   * - ``"faulthandler"``
     - :c:member:`faulthandler <PyConfig.faulthandler>`
     - ``bool``
     - Chỉ đọc
   * - ``"filesystem_encoding"``
     - :c:member:`filesystem_encoding <PyConfig.filesystem_encoding>`
     - ``str``
     - Chỉ đọc
   * - ``"filesystem_errors"``
     - :c:member:`filesystem_errors <PyConfig.filesystem_errors>`
     - ``str``
     - Chỉ đọc
   * - ``"hash_seed"``
     - :c:member:`hash_seed <PyConfig.hash_seed>`
     - ``int``
     - Chỉ đọc
   * - ``"home"``
     - :c:member:`home <PyConfig.home>`
     - ``str``
     - Chỉ đọc
   * - ``"import_time"``
     - :c:member:`import_time <PyConfig.import_time>`
     - ``int``
     - Chỉ đọc
   * - ``"inspect"``
     - :c:member:`inspect <PyConfig.inspect>`
     - ``bool``
     - Công khai
   * - ``"install_signal_handlers"``
     - :c:member:`install_signal_handlers <PyConfig.install_signal_handlers>`
     - ``bool``
     - Chỉ đọc
   * - ``"int_max_str_digits"``
     - :c:member:`int_max_str_digits <PyConfig.int_max_str_digits>`
     - ``int``
     - Công khai
   * - ``"interactive"``
     - :c:member:`interactive <PyConfig.interactive>`
     - ``bool``
     - Công khai
   * - ``"isolated"``
     - :c:member:`isolated <PyConfig.isolated>`
     - ``bool``
     - Chỉ đọc
   * - ``"legacy_windows_fs_encoding"``
     - :c:member:`legacy_windows_fs_encoding <PyPreConfig.legacy_windows_fs_encoding>`
     - ``bool``
     - Chỉ đọc
   * - ``"legacy_windows_stdio"``
     - :c:member:`legacy_windows_stdio <PyConfig.legacy_windows_stdio>`
     - ``bool``
     - Chỉ đọc
   * - ``"malloc_stats"``
     - :c:member:`malloc_stats <PyConfig.malloc_stats>`
     - ``bool``
     - Chỉ đọc
   * - ``"module_search_paths"``
     - :c:member:`module_search_paths <PyConfig.module_search_paths>`
     - ``list[str]``
     - Công khai
   * - ``"optimization_level"``
     - :c:member:`optimization_level <PyConfig.optimization_level>`
     - ``int``
     - Công khai
   * - ``"orig_argv"``
     - :c:member:`orig_argv <PyConfig.orig_argv>`
     - ``list[str]``
     - Chỉ đọc
   * - ``"parse_argv"``
     - :c:member:`parse_argv <PyConfig.parse_argv>`
     - ``bool``
     - Chỉ đọc
   * - ``"parser_debug"``
     - :c:member:`parser_debug <PyConfig.parser_debug>`
     - ``bool``
     - Công khai
   * - ``"pathconfig_warnings"``
     - :c:member:`pathconfig_warnings <PyConfig.pathconfig_warnings>`
     - ``bool``
     - Chỉ đọc
   * - ``"perf_profiling"``
     - :c:member:`perf_profiling <PyConfig.perf_profiling>`
     - ``bool``
     - Chỉ đọc
   * - ``"platlibdir"``
     - :c:member:`platlibdir <PyConfig.platlibdir>`
     - ``str``
     - Công khai
   * - ``"prefix"``
     - :c:member:`prefix <PyConfig.prefix>`
     - ``str``
     - Công khai
   * - ``"program_name"``
     - :c:member:`program_name <PyConfig.program_name>`
     - ``str``
     - Chỉ đọc
   * - ``"pycache_prefix"``
     - :c:member:`pycache_prefix <PyConfig.pycache_prefix>`
     - ``str``
     - Công khai
   * - ``"quiet"``
     - :c:member:`quiet <PyConfig.quiet>`
     - ``bool``
     - Công khai
   * - ``"run_command"``
     - :c:member:`run_command <PyConfig.run_command>`
     - ``str``
     - Chỉ đọc
   * - ``"run_filename"``
     - :c:member:`run_filename <PyConfig.run_filename>`
     - ``str``
     - Chỉ đọc
   * - ``"run_module"``
     - :c:member:`run_module <PyConfig.run_module>`
     - ``str``
     - Chỉ đọc
   * - ``"run_presite"``
     - :c:member:`run_presite <PyConfig.run_presite>`
     - ``str``
     - Chỉ đọc
   * - ``"safe_path"``
     - :c:member:`safe_path <PyConfig.safe_path>`
     - ``bool``
     - Chỉ đọc
   * - ``"show_ref_count"``
     - :c:member:`show_ref_count <PyConfig.show_ref_count>`
     - ``bool``
     - Chỉ đọc
   * - ``"site_import"``
     - :c:member:`site_import <PyConfig.site_import>`
     - ``bool``
     - Chỉ đọc
   * - ``"skip_source_first_line"``
     - :c:member:`skip_source_first_line <PyConfig.skip_source_first_line>`
     - ``bool``
     - Chỉ đọc
   * - ``"stdio_encoding"``
     - :c:member:`stdio_encoding <PyConfig.stdio_encoding>`
     - ``str``
     - Chỉ đọc
   * - ``"stdio_errors"``
     - :c:member:`stdio_errors <PyConfig.stdio_errors>`
     - ``str``
     - Chỉ đọc
   * - ``"stdlib_dir"``
     - :c:member:`stdlib_dir <PyConfig.stdlib_dir>`
     - ``str``
     - Công khai
   * - ``"tracemalloc"``
     - :c:member:`tracemalloc <PyConfig.tracemalloc>`
     - ``int``
     - Chỉ đọc
   * - ``"use_environment"``
     - :c:member:`use_environment <PyConfig.use_environment>`
     - ``bool``
     - Công khai
   * - ``"use_frozen_modules"``
     - :c:member:`use_frozen_modules <PyConfig.use_frozen_modules>`
     - ``bool``
     - Chỉ đọc
   * - ``"use_hash_seed"``
     - :c:member:`use_hash_seed <PyConfig.use_hash_seed>`
     - ``bool``
     - Chỉ đọc
   * - ``"use_system_logger"``
     - :c:member:`use_system_logger <PyConfig.use_system_logger>`
     - ``bool``
     - Chỉ đọc
   * - ``"user_site_directory"``
     - :c:member:`user_site_directory <PyConfig.user_site_directory>`
     - ``bool``
     - Chỉ đọc
   * - ``"utf8_mode"``
     - :c:member:`utf8_mode <PyPreConfig.utf8_mode>`
     - ``bool``
     - Chỉ đọc
   * - ``"verbose"``
     - :c:member:`verbose <PyConfig.verbose>`
     - ``int``
     - Công khai
   * - ``"warn_default_encoding"``
     - :c:member:`warn_default_encoding <PyConfig.warn_default_encoding>`
     - ``bool``
     - Chỉ đọc
   * - ``"warnoptions"``
     - :c:member:`warnoptions <PyConfig.warnoptions>`
     - ``list[str]``
     - Công khai
   * - ``"write_bytecode"``
     - :c:member:`write_bytecode <PyConfig.write_bytecode>`
     - ``bool``
     - Công khai
   * - ``"xoptions"``
     - :c:member:`xoptions <PyConfig.xoptions>`
     - ``dict[str, str]``
     - Công khai
   * - ``"_pystats"``
     - :c:member:`_pystats <PyConfig._pystats>`
     - ``bool``
     - Chỉ đọc

Khả năng hiển thị:

* Công khai: Có thể được truy xuất bằng :c:func:`PyConfig_Get` và thiết lập bằng
  :c:func:`PyConfig_Set`.
* Chỉ đọc: Có thể được truy xuất bằng :c:func:`PyConfig_Get`, nhưng không thể được thiết lập bằng
  :c:func:`PyConfig_Set`.


API cấu hình Python trong runtime
=================================

Trong runtime, có thể lấy và thiết lập các tùy chọn cấu hình bằng
:c:func:`PyConfig_Get` và  :c:func:`PyConfig_Set` functions.

Tham số *name* của tùy chọn cấu hình phải là một chuỗi được mã hóa UTF-8, kết thúc bằng null và không phải NULL. Xem :ref:`Configuration Options <pyinitconfig-opts>`.

Một số tùy chọn được đọc từ các thuộc tính :mod:`sys`. Ví dụ: tùy chọn ``"argv"`` được đọc từ :data:`sys.argv`.


.. c:function:: PyObject* PyConfig_Get(const char *name)

   Lấy giá trị runtime hiện tại của một tùy chọn cấu hình dưới dạng một đối tượng Python.

   * Trả về một reference mới nếu thành công.
   * Đặt một exception và trả về ``NULL`` nếu xảy ra lỗi.

   Kiểu đối tượng phụ thuộc vào tùy chọn cấu hình. Nó có thể là:

   * ``bool``
   * ``int``
   * ``str``
   * ``list[str]``
   * ``dict[str, str]``

   Caller phải có một :term:`attached thread state`. Không thể gọi hàm này trước khi khởi tạo Python hoặc sau khi Python hoàn tất việc kết thúc.

   .. versionadded:: 3.14


.. c:function:: int PyConfig_GetInt(const char *name, int *value)

   Tương tự như :c:func:`PyConfig_Get`, nhưng lấy giá trị dưới dạng một int C.

   * Trả về ``0`` nếu thành công.
   * Đặt một ngoại lệ và trả về ``-1`` khi xảy ra lỗi.

   .. versionadded:: 3.14


.. c:function:: PyObject* PyConfig_Names(void)

   Lấy tất cả tên tùy chọn cấu hình dưới dạng một ``frozenset``.

   * Trả về một reference mới nếu thành công.
   * Đặt một exception và trả về ``NULL`` nếu xảy ra lỗi.

   Caller phải có một :term:`attached thread state`. Không thể gọi hàm này trước khi khởi tạo Python hoặc sau khi Python hoàn tất việc kết thúc.

   .. versionadded:: 3.14


.. c:function:: int PyConfig_Set(const char *name, PyObject *value)

   Đặt giá trị runtime hiện tại của một tùy chọn cấu hình.

   * Nêu một :exc:`ValueError` nếu không có tùy chọn *name*.
   * Phát sinh :exc:`ValueError` nếu *value* là một giá trị không hợp lệ.
   * Phát sinh :exc:`ValueError` nếu tùy chọn này chỉ được đọc (không thể thiết lập).
   * Phát sinh :exc:`TypeError` nếu *value* không có kiểu phù hợp.

   Caller phải có một :term:`attached thread state`. Không thể gọi hàm này trước khi khởi tạo Python hoặc sau khi Python hoàn tất việc kết thúc.

   .. audit-event:: cpython.PyConfig_Set name,value c.PyConfig_Set

   .. versionadded:: 3.14

   .. versionchanged:: 3.14.7
      Hàm hiện thay thế :data:`sys.flags` (tạo một đối tượng mới), thay vì sửa đổi :data:`sys.flags` tại chỗ.


.. _pyconfig_api:

C API PyConfig
==============

.. versionadded:: 3.8

Python có thể được khởi tạo bằng :c:func:`Py_InitializeFromConfig` và
:c:type:`PyConfig` cấu trúc. Cấu trúc này có thể được khởi tạo trước bằng
:c:func:`Py_PreInitialize` và cấu trúc :c:type:`PyPreConfig`.

Có hai loại cấu hình:

* :ref:`Cấu hình Python <init-python-config>` có thể được dùng để xây dựng một Python tùy chỉnh nhưng hoạt động như Python thông thường. Ví dụ, các biến môi trường và đối số dòng lệnh được dùng để cấu hình Python.

* :ref:`Cấu hình cô lập <init-isolated-conf>` có thể được dùng để nhúng Python vào một ứng dụng. Cấu hình này cô lập Python khỏi hệ thống. Ví dụ, các biến môi trường bị bỏ qua, locale LC_CTYPE không bị thay đổi và không có trình xử lý tín hiệu nào được đăng ký.

Có thể sử dụng hàm :c:func:`Py_RunMain` để viết một chương trình Python tùy chỉnh.

Xem thêm :ref:`Khởi tạo, Kết thúc và Luồng <initialization>`.

.. seealso::
   :pep:`587` "Python Initialization Configuration".


Ví dụ
-----

Ví dụ về Python được tùy chỉnh luôn chạy ở chế độ isolated::

    int main(int argc, char **argv)
    {
        PyStatus status;

        PyConfig config;
        PyConfig_InitPythonConfig(&config);
        config.isolated = 1;

        /* Decode command line arguments.
           Implicitly preinitialize Python (in isolated mode). */
        status = PyConfig_SetBytesArgv(&config, argc, argv);
        if (PyStatus_Exception(status)) {
            goto exception;
        }

        status = Py_InitializeFromConfig(&config);
        if (PyStatus_Exception(status)) {
            goto exception;
        }
        PyConfig_Clear(&config);

        return Py_RunMain();

    exception:
        PyConfig_Clear(&config);
        if (PyStatus_IsExit(status)) {
            return status.exitcode;
        }
        /* Display the error message and exit the process with
           non-zero exit code */
        Py_ExitStatusException(status);
    }


PyWideStringList
----------------

.. c:type:: PyWideStringList

   Danh sách các chuỗi ``wchar_t*``.

   Nếu *length* khác không, *items* phải khác ``NULL`` và tất cả các chuỗi phải khác ``NULL``.

   .. c:namespace:: NULL

   Các phương thức:

   .. c:function:: PyStatus PyWideStringList_Append(PyWideStringList *list, const wchar_t *item)

      Nối thêm *item* vào *list*.

      Python phải được khởi tạo trước để gọi hàm này.

   .. c:function:: PyStatus PyWideStringList_Insert(PyWideStringList *list, Py_ssize_t index, const wchar_t *item)

      Chèn *item* vào *list* tại *index*.

      Nếu *index* lớn hơn hoặc bằng độ dài của *list*, hãy nối thêm *item* vào *list*.

      *index* phải lớn hơn hoặc bằng ``0``.

      Python phải được khởi tạo trước để gọi hàm này.

   .. c:namespace:: PyWideStringList

   Các trường của cấu trúc:

   .. c:member:: Py_ssize_t length

      Độ dài danh sách.

   .. c:member:: wchar_t** items

      Các mục trong danh sách.

PyStatus
--------

.. c:type:: PyStatus

   Cấu trúc dùng để lưu trạng thái của một hàm khởi tạo: thành công, lỗi hoặc thoát.

   Đối với lỗi, cấu trúc này có thể lưu tên hàm C đã tạo ra lỗi.

   Các trường của cấu trúc:

   .. c:member:: int exitcode

      Mã thoát. Đối số được truyền cho ``exit()``.

   .. c:member:: const char *err_msg

      Thông báo lỗi.

   .. c:member:: const char *func

      Tên của hàm đã tạo ra lỗi, có thể là ``NULL``.

   .. c:namespace:: NULL

   Các hàm để tạo status:

   .. c:function:: PyStatus PyStatus_Ok(void)

      Thành công.

   .. c:function:: PyStatus PyStatus_Error(const char *err_msg)

      Lỗi khởi tạo kèm thông báo.

      *err_msg* không được là ``NULL``.

   .. c:function:: PyStatus PyStatus_NoMemory(void)

      Lỗi cấp phát bộ nhớ (hết bộ nhớ).

   .. c:function:: PyStatus PyStatus_Exit(int exitcode)

      Thoát Python với mã thoát được chỉ định.

   Các hàm xử lý một trạng thái:

   .. c:function:: int PyStatus_Exception(PyStatus status)

      Trạng thái là lỗi hay yêu cầu thoát? Nếu đúng, phải xử lý ngoại lệ; chẳng hạn bằng cách gọi :c:func:`Py_ExitStatusException`.

   .. c:function:: int PyStatus_IsError(PyStatus status)

      Kết quả có phải là lỗi không?

   .. c:function:: int PyStatus_IsExit(PyStatus status)

      Kết quả có phải là yêu cầu thoát không?

   .. c:function:: void Py_ExitStatusException(PyStatus status)

      Gọi ``exit(exitcode)`` nếu *status* là yêu cầu thoát. In thông báo lỗi và thoát với mã thoát khác 0 nếu *status* là lỗi. Chỉ được gọi khi ``PyStatus_Exception(status)`` khác 0.

.. note::
   Bên trong, Python sử dụng các macro để thiết lập ``PyStatus.func``, trong khi các hàm tạo trạng thái thiết lập ``func`` thành ``NULL``.

Ví dụ::

    PyStatus alloc(void **ptr, size_t size)
    {
        *ptr = PyMem_RawMalloc(size);
        if (*ptr == NULL) {
            return PyStatus_NoMemory();
        }
        return PyStatus_Ok();
    }

    int main(int argc, char **argv)
    {
        void *ptr;
        PyStatus status = alloc(&ptr, 16);
        if (PyStatus_Exception(status)) {
            Py_ExitStatusException(status);
        }
        PyMem_Free(ptr);
        return 0;
    }


PyPreConfig
-----------

.. c:type:: PyPreConfig

   Cấu trúc được dùng để tiền khởi tạo Python.

   .. c:namespace:: NULL

   Hàm để khởi tạo cấu hình tiền khởi tạo:

   .. c:function:: void PyPreConfig_InitPythonConfig(PyPreConfig *preconfig)

      Khởi tạo cấu hình tiền khởi tạo với :ref:`Python Configuration <init-python-config>`.

   .. c:function:: void PyPreConfig_InitIsolatedConfig(PyPreConfig *preconfig)

      Khởi tạo cấu hình tiền khởi tạo với :ref:`Isolated Configuration <init-isolated-conf>`.

   .. c:namespace:: PyPreConfig

   Các trường của cấu trúc:

   .. c:member:: int allocator

      Tên của các bộ cấp phát bộ nhớ Python:

      * ``PYMEM_ALLOCATOR_NOT_SET`` (``0``): không thay đổi các trình cấp phát bộ nhớ (sử dụng mặc định).
      * ``PYMEM_ALLOCATOR_DEFAULT`` (``1``): :ref:`các trình cấp phát bộ nhớ mặc định <default-memory-allocators>`.
      * ``PYMEM_ALLOCATOR_DEBUG`` (``2``): :ref:`các trình cấp phát bộ nhớ mặc định <default-memory-allocators>` cùng với :ref:`các hook gỡ lỗi <pymem-debug-hooks>`.
      * ``PYMEM_ALLOCATOR_MALLOC`` (``3``): sử dụng ``malloc()`` của thư viện C.
      * ``PYMEM_ALLOCATOR_MALLOC_DEBUG`` (``4``): buộc sử dụng ``malloc()`` cùng với :ref:`các hook gỡ lỗi <pymem-debug-hooks>`.
      * ``PYMEM_ALLOCATOR_PYMALLOC`` (``5``): :ref:`trình cấp phát bộ nhớ pymalloc của Python <pymalloc>`.
      * ``PYMEM_ALLOCATOR_PYMALLOC_DEBUG`` (``6``): :ref:`trình cấp phát bộ nhớ pymalloc của Python <pymalloc>` cùng với :ref:`các hook gỡ lỗi <pymem-debug-hooks>`.
      * ``PYMEM_ALLOCATOR_MIMALLOC`` (``6``): sử dụng ``mimalloc``, một phương án thay thế malloc nhanh.
      * ``PYMEM_ALLOCATOR_MIMALLOC_DEBUG`` (``7``): sử dụng ``mimalloc``, một phương án thay thế malloc nhanh với các hook :ref:`debug hooks <pymem-debug-hooks>`.


      ``PYMEM_ALLOCATOR_PYMALLOC`` và ``PYMEM_ALLOCATOR_PYMALLOC_DEBUG`` không được hỗ trợ nếu Python ở chế độ :option:`configured using --without-pymalloc <--without-pymalloc>`.

      ``PYMEM_ALLOCATOR_MIMALLOC`` và ``PYMEM_ALLOCATOR_MIMALLOC_DEBUG`` không được hỗ trợ nếu Python ở chế độ :option:`configured using --without-mimalloc <--without-mimalloc>` hoặc nếu hệ thống hỗ trợ atomic bên dưới không khả dụng.

      Xem :ref:`Memory Management <memory>`.

      Mặc định: ``PYMEM_ALLOCATOR_NOT_SET``.

   .. c:member:: int configure_locale

      Đặt locale LC_CTYPE thành locale ưu tiên của người dùng.

      Nếu bằng ``0``, đặt :c:member:`~PyPreConfig.coerce_c_locale` và
      các thành viên :c:member:`~PyPreConfig.coerce_c_locale_warn` thành ``0``.

      Xem :term:`locale encoding`.

      Mặc định: ``1`` trong cấu hình Python, ``0`` trong cấu hình isolated.

   .. c:member:: int coerce_c_locale

      Nếu bằng ``2``, ép locale C.

      Nếu bằng ``1``, đọc locale LC_CTYPE để quyết định có nên ép locale hay không.

      Xem :term:`locale encoding`.

      Mặc định: ``-1`` trong cấu hình Python, ``0`` trong cấu hình cô lập.

   .. c:member:: int coerce_c_locale_warn

      Nếu khác không, phát cảnh báo nếu locale C bị ép buộc.

      Mặc định: ``-1`` trong cấu hình Python, ``0`` trong cấu hình cô lập.

   .. c:member:: int dev_mode

      :ref:`Python Development Mode <devmode>`: xem
      :c:member:`PyConfig.dev_mode`.

      Mặc định: ``-1`` trong chế độ Python, ``0`` trong chế độ cô lập.

   .. c:member:: int isolated

      Chế độ cô lập: xem :c:member:`PyConfig.isolated`.

      Mặc định: ``0`` trong chế độ Python, ``1`` trong chế độ cô lập.

   .. c:member:: int legacy_windows_fs_encoding

      Nếu khác không:

      * Đặt :c:member:`PyPreConfig.utf8_mode` thành ``0``,
      * Đặt :c:member:`PyConfig.filesystem_encoding` thành ``"mbcs"``,
      * Đặt :c:member:`PyConfig.filesystem_errors` thành ``"replace"``.

      Được khởi tạo từ giá trị của biến môi trường :envvar:`PYTHONLEGACYWINDOWSFSENCODING`.

      Chỉ khả dụng trên Windows. Macro ``#ifdef MS_WINDOWS`` có thể được sử dụng cho mã dành riêng cho Windows.

      Mặc định: ``0``.

   .. c:member:: int parse_argv

      Nếu khác không, :c:func:`Py_PreInitializeFromArgs` và
      :c:func:`Py_PreInitializeFromBytesArgs` phân tích đối số ``argv`` của chúng theo cùng cách Python thông thường phân tích các đối số dòng lệnh: xem
      :ref:`Đối số dòng lệnh <using-on-cmdline>`.

      Mặc định: ``1`` trong cấu hình Python, ``0`` trong cấu hình isolated.

   .. c:member:: int use_environment

      Sử dụng :ref:`biến môi trường <using-on-envvars>`? Xem
      :c:member:`PyConfig.use_environment`.

      Mặc định: ``1`` trong cấu hình Python và ``0`` trong cấu hình biệt lập.

   .. c:member:: int utf8_mode

      Nếu khác không, bật :ref:`Python UTF-8 Mode <utf8-mode>`.

      Được đặt thành ``0`` hoặc ``1`` bằng tùy chọn dòng lệnh :option:`-X utf8 <-X>` và biến môi trường :envvar:`PYTHONUTF8`.

      Cũng được đặt thành ``1`` nếu locale ``LC_CTYPE`` là ``C`` hoặc ``POSIX``.

      Mặc định: ``-1`` trong cấu hình Python và ``0`` trong cấu hình cô lập.


.. _c-preinit:

Tiền khởi tạo Python bằng PyPreConfig
-------------------------------------

Quá trình tiền khởi tạo Python:

* Đặt các memory allocator của Python (:c:member:`PyPreConfig.allocator`)
* Cấu hình locale LC_CTYPE (:term:`locale encoding`)
* Thiết lập :ref:`Python UTF-8 Mode <utf8-mode>` (:c:member:`PyPreConfig.utf8_mode`)

Cấu hình tiền khởi tạo hiện tại (``PyPreConfig`` type) được lưu trong ``_PyRuntime.preconfig``.

Các hàm để tiền khởi tạo Python:

.. c:function:: PyStatus Py_PreInitialize(const PyPreConfig *preconfig)

   Tiền khởi tạo Python từ cấu hình tiền khởi tạo *preconfig*.

   *preconfig* không được là ``NULL``.

.. c:function:: PyStatus Py_PreInitializeFromBytesArgs(const PyPreConfig *preconfig, int argc, char * const *argv)

   Tiền khởi tạo Python từ cấu hình tiền khởi tạo *preconfig*.

   Phân tích các đối số dòng lệnh *argv* (chuỗi byte) nếu
   :c:member:`~PyPreConfig.parse_argv` của *preconfig* khác không.

   *preconfig* không được là ``NULL``.

.. c:function:: PyStatus Py_PreInitializeFromArgs(const PyPreConfig *preconfig, int argc, wchar_t * const * argv)

   Tiền khởi tạo Python từ cấu hình tiền khởi tạo *preconfig*.

   Phân tích các đối số dòng lệnh *argv* (chuỗi ký tự rộng) nếu
   :c:member:`~PyPreConfig.parse_argv` của *preconfig* khác không.

   *preconfig* không được là ``NULL``.

Bên gọi có trách nhiệm xử lý các ngoại lệ (lỗi hoặc thoát) bằng cách sử dụng
:c:func:`PyStatus_Exception` và :c:func:`Py_ExitStatusException`.

Đối với :ref:`Python Configuration <init-python-config>` (:c:func:`PyPreConfig_InitPythonConfig`), nếu Python được khởi tạo với các đối số dòng lệnh, các đối số dòng lệnh đó cũng phải được truyền vào bước khởi tạo trước Python, vì chúng ảnh hưởng đến cấu hình trước, chẳng hạn như các encoding. Ví dụ, tùy chọn dòng lệnh :option:`-X utf8 <-X>` bật :ref:`Python UTF-8 Mode <utf8-mode>`.

Có thể gọi ``PyMem_SetAllocator()`` sau :c:func:`Py_PreInitialize` và trước :c:func:`Py_InitializeFromConfig` để cài đặt một memory allocator tùy chỉnh. Có thể gọi hàm này trước :c:func:`Py_PreInitialize` nếu
:c:member:`PyPreConfig.allocator` được đặt thành ``PYMEM_ALLOCATOR_NOT_SET``.

Không được sử dụng các hàm cấp phát bộ nhớ của Python như :c:func:`PyMem_RawMalloc` trước khi thực hiện bước khởi tạo trước Python, trong khi việc gọi trực tiếp ``malloc()`` và ``free()`` luôn an toàn. Không được gọi :c:func:`Py_DecodeLocale` trước khi thực hiện bước khởi tạo trước Python.

Ví dụ sử dụng bước khởi tạo trước để bật :ref:`Python UTF-8 Mode <utf8-mode>`::

    PyStatus status;
    PyPreConfig preconfig;
    PyPreConfig_InitPythonConfig(&preconfig);

    preconfig.utf8_mode = 1;

    status = Py_PreInitialize(&preconfig);
    if (PyStatus_Exception(status)) {
        Py_ExitStatusException(status);
    }

    /* at this point, Python speaks UTF-8 */

    Py_Initialize();
    /* ... use Python API here ... */
    Py_Finalize();


PyConfig
--------

.. c:type:: PyConfig

   Cấu trúc chứa hầu hết các tham số để cấu hình Python.

   Sau khi hoàn tất, phải sử dụng hàm :c:func:`PyConfig_Clear` để giải phóng bộ nhớ cấu hình.

   .. c:namespace:: NULL

   Các phương thức của cấu trúc:

   .. c:function:: void PyConfig_InitPythonConfig(PyConfig *config)

      Khởi tạo cấu hình bằng :ref:`Cấu hình Python <init-python-config>`.

   .. c:function:: void PyConfig_InitIsolatedConfig(PyConfig *config)

      Khởi tạo cấu hình bằng :ref:`Cấu hình cô lập <init-isolated-conf>`.

   .. c:function:: PyStatus PyConfig_SetString(PyConfig *config, wchar_t * const *config_str, const wchar_t *str)

      Sao chép chuỗi ký tự rộng *str* vào ``*config_str``.

      :ref:`Tiền khởi tạo Python <c-preinit>` nếu cần.

   .. c:function:: PyStatus PyConfig_SetBytesString(PyConfig *config, wchar_t * const *config_str, const char *str)

      Giải mã *str* bằng :c:func:`Py_DecodeLocale` và đặt kết quả vào ``*config_str``.

      :ref:`Tiền khởi tạo Python <c-preinit>` nếu cần.

   .. c:function:: PyStatus PyConfig_SetArgv(PyConfig *config, int argc, wchar_t * const *argv)

      Đặt các đối số dòng lệnh (thành viên :c:member:`~PyConfig.argv` của *config*) từ danh sách chuỗi ký tự wide *argv*.

      :ref:`Tiền khởi tạo Python <c-preinit>` nếu cần.

   .. c:function:: PyStatus PyConfig_SetBytesArgv(PyConfig *config, int argc, char * const *argv)

      Đặt các đối số dòng lệnh (thành viên :c:member:`~PyConfig.argv` của *config*) từ danh sách chuỗi byte *argv*. Giải mã các byte bằng
      :c:func:`Py_DecodeLocale`.

      :ref:`Tiền khởi tạo Python <c-preinit>` nếu cần.

   .. c:function:: PyStatus PyConfig_SetWideStringList(PyConfig *config, PyWideStringList *list, Py_ssize_t length, wchar_t **items)

      Đặt danh sách chuỗi wide *list* thành *length* và *items*.

      :ref:`Tiền khởi tạo Python <c-preinit>` nếu cần.

   .. c:function:: PyStatus PyConfig_Read(PyConfig *config)

      Đọc toàn bộ cấu hình Python.

      Các trường đã được khởi tạo sẽ không bị thay đổi.

      Các trường dành cho cấu hình :ref:`path configuration <init-path-config>` không còn được tính toán hoặc sửa đổi khi gọi hàm này kể từ Python 3.11.

      Hàm :c:func:`PyConfig_Read` chỉ phân tích cú pháp
      Các :c:member:`PyConfig.argv` đối số chỉ được phân tích cú pháp một lần: :c:member:`PyConfig.parse_argv` được đặt thành ``2`` sau khi các đối số được phân tích cú pháp. Vì các đối số Python bị loại bỏ khỏi :c:member:`PyConfig.argv`, việc phân tích cú pháp các đối số hai lần sẽ phân tích các tùy chọn của ứng dụng như các tùy chọn Python.

      :ref:`Tiền khởi tạo Python <c-preinit>` nếu cần.

      .. versionchanged:: 3.10
         Các đối số :c:member:`PyConfig.argv` giờ đây chỉ được phân tích một lần,
         :c:member:`PyConfig.parse_argv` được đặt thành ``2`` sau khi các đối số được phân tích, và các đối số chỉ được phân tích nếu
         :c:member:`PyConfig.parse_argv` bằng ``1``.

      .. versionchanged:: 3.11
         :c:func:`PyConfig_Read` no longer calculates all paths, and so fields
         được liệt kê trong :ref:`Python Path Configuration <init-path-config>` có thể không được cập nhật cho đến khi gọi :c:func:`Py_InitializeFromConfig`.

   .. c:function:: void PyConfig_Clear(PyConfig *config)

      Giải phóng bộ nhớ cấu hình.

   Hầu hết các phương thức ``PyConfig`` :ref:`preinitialize Python <c-preinit>` nếu cần. Trong trường hợp đó, cấu hình tiền khởi tạo Python (:c:type:`PyPreConfig`) dựa trên :c:type:`PyConfig`. Nếu các trường cấu hình dùng chung với :c:type:`PyPreConfig` được điều chỉnh, chúng phải được thiết lập trước khi gọi phương thức :c:type:`PyConfig`:

   * :c:member:`PyConfig.dev_mode`
   * :c:member:`PyConfig.isolated`
   * :c:member:`PyConfig.parse_argv`
   * :c:member:`PyConfig.use_environment`

   Ngoài ra, nếu sử dụng :c:func:`PyConfig_SetArgv` hoặc :c:func:`PyConfig_SetBytesArgv`, phương thức này phải được gọi trước các phương thức khác, vì cấu hình tiền khởi tạo phụ thuộc vào các đối số dòng lệnh (nếu
   :c:member:`~PyConfig.parse_argv` khác không).

   Bên gọi các phương thức này chịu trách nhiệm xử lý các ngoại lệ (lỗi hoặc thoát) bằng ``PyStatus_Exception()`` và ``Py_ExitStatusException()``.

   .. c:namespace:: PyConfig

   Các trường của cấu trúc:

   .. c:member:: PyWideStringList argv

      .. index::
         single: main()
         single: argv (in module sys)

      Đặt các đối số dòng lệnh của :data:`sys.argv` dựa trên
      :c:member:`~PyConfig.argv`. Các tham số này tương tự như các tham số được truyền vào hàm :c:func:`main` của chương trình, với điểm khác biệt là mục đầu tiên phải tham chiếu đến tệp script sẽ được thực thi thay vì tệp thực thi lưu trữ trình thông dịch Python. Nếu không có script nào được chạy, mục đầu tiên trong :c:member:`~PyConfig.argv` có thể là một chuỗi rỗng.

      Đặt :c:member:`~PyConfig.parse_argv` thành ``1`` để phân tích cú pháp
      :c:member:`~PyConfig.argv` theo cùng cách Python thông thường phân tích các đối số dòng lệnh của Python, sau đó loại bỏ các đối số của Python khỏi
      :c:member:`~PyConfig.argv`.

      Nếu :c:member:`~PyConfig.argv` trống, một chuỗi rỗng sẽ được thêm vào để đảm bảo rằng :data:`sys.argv` luôn tồn tại và không bao giờ trống.

      Mặc định: ``NULL``.

      Xem thêm thành viên :c:member:`~PyConfig.orig_argv`.

   .. c:member:: int safe_path

      Nếu bằng 0, ``Py_RunMain()`` sẽ thêm tiền tố là một đường dẫn có thể không an toàn vào
      :data:`sys.path` khi khởi động:

      * Nếu :c:member:`argv[0] <PyConfig.argv>` bằng ``L"-m"`` (``python -m module``), thêm tiền tố là thư mục làm việc hiện tại.
      * Nếu đang chạy một script (``python script.py``), thêm tiền tố là thư mục của script. Nếu đó là một symbolic link, hãy phân giải các symbolic link.
      * Nếu không (``python -c code`` và ``python``), thêm một chuỗi rỗng vào đầu, nghĩa là thư mục làm việc hiện tại.

      Được đặt thành ``1`` bởi tùy chọn dòng lệnh :option:`-P` và
      biến môi trường :envvar:`PYTHONSAFEPATH`.

      Mặc định: ``0`` trong cấu hình Python, ``1`` trong cấu hình isolated.

      .. versionadded:: 3.11

   .. c:member:: wchar_t* base_exec_prefix

      :data:`sys.base_exec_prefix`.

      Mặc định: ``NULL``.

      Là một phần của đầu ra :ref:`Cấu hình đường dẫn Python <init-path-config>`.

      Xem thêm :c:member:`PyConfig.exec_prefix`.

   .. c:member:: wchar_t* base_executable

      Tệp thực thi cơ sở của Python: ``sys._base_executable``.

      Được thiết lập bởi biến môi trường ``__PYVENV_LAUNCHER__``.

      Được thiết lập từ :c:member:`PyConfig.executable` nếu ``NULL``.

      Mặc định: ``NULL``.

      Là một phần của đầu ra :ref:`Cấu hình đường dẫn Python <init-path-config>`.

      Xem thêm :c:member:`PyConfig.executable`.

   .. c:member:: wchar_t* base_prefix

      :data:`sys.base_prefix`.

      Mặc định: ``NULL``.

      Là một phần của đầu ra :ref:`Cấu hình đường dẫn Python <init-path-config>`.

      Xem thêm :c:member:`PyConfig.prefix`.

   .. c:member:: int buffered_stdio

      Nếu bằng ``0`` và :c:member:`~PyConfig.configure_c_stdio` khác 0, hãy tắt buffering trên các luồng C stdout và stderr.

      Được đặt thành ``0`` bởi tùy chọn dòng lệnh :option:`-u` và
      biến môi trường :envvar:`PYTHONUNBUFFERED`.

      stdin luôn được mở ở chế độ buffered.

      Mặc định: ``1``.

   .. c:member:: int bytes_warning

      Nếu bằng ``1``, phát cảnh báo khi so sánh :class:`bytes` hoặc
      :class:`bytearray` với :class:`str`, hoặc so sánh :class:`bytes` với
      :class:`int`.

      Nếu bằng hoặc lớn hơn ``2``, raise một exception :exc:`BytesWarning` trong các trường hợp này.

      Được tăng lên bởi tùy chọn dòng lệnh :option:`-b`.

      Mặc định: ``0``.

   .. c:member:: int warn_default_encoding

      Nếu khác không, phát cảnh báo :exc:`EncodingWarning` khi :class:`io.TextIOWrapper` sử dụng encoding mặc định. Xem :ref:`io-encoding-warning` để biết chi tiết.

      Mặc định: ``0``.

      .. versionadded:: 3.10

   .. c:member:: int code_debug_ranges

      Nếu bằng ``0``, tắt việc đưa ánh xạ dòng và cột kết thúc vào các code object. Đồng thời tắt việc in các dấu mũ trong traceback để chỉ đến những vị trí lỗi cụ thể.

      Được đặt thành ``0`` bởi biến môi trường :envvar:`PYTHONNODEBUGRANGES` và tùy chọn dòng lệnh :option:`-X no_debug_ranges <-X>`.

      Mặc định: ``1``.

      .. versionadded:: 3.11

   .. c:member:: wchar_t* check_hash_pycs_mode

      Kiểm soát hành vi xác thực của các tệp ``.pyc`` dựa trên hash: giá trị của tùy chọn dòng lệnh :option:`--check-hash-based-pycs`.

      Các giá trị hợp lệ:

      - ``L"always"``: Băm tệp nguồn để vô hiệu hóa bất kể giá trị của cờ 'check_source'.
      - ``L"never"``: Giả định rằng các pyc dựa trên hash luôn hợp lệ.
      - ``L"default"``: Cờ 'check_source' trong các pyc dựa trên hash xác định cơ chế vô hiệu hóa.

      Mặc định: ``L"default"``.

      Xem thêm :pep:`552` "Các pyc xác định".

   .. c:member:: int configure_c_stdio

      Nếu khác không, cấu hình các luồng chuẩn của C:

      * Trên Windows, đặt chế độ nhị phân (``O_BINARY``) cho stdin, stdout và stderr.
      * Nếu :c:member:`~PyConfig.buffered_stdio` bằng 0, tắt bộ đệm của các luồng stdin, stdout và stderr.
      * Nếu :c:member:`~PyConfig.interactive` khác không, bật bộ đệm luồng trên stdin và stdout (chỉ stdout trên Windows).

      Mặc định: ``1`` trong cấu hình Python, ``0`` trong cấu hình cô lập.

   .. c:member:: int dev_mode

      Nếu khác không, bật :ref:`Python Development Mode <devmode>`.

      Được đặt thành ``1`` bởi tùy chọn :option:`-X dev <-X>` và
      biến môi trường :envvar:`PYTHONDEVMODE`.

      Mặc định: ``-1`` trong chế độ Python, ``0`` trong chế độ cô lập.

   .. c:member:: int dump_refs

      Kết xuất các tham chiếu Python?

      Nếu khác không, kết xuất tất cả các đối tượng vẫn còn tồn tại khi thoát.

      Được đặt thành ``1`` bởi biến môi trường :envvar:`PYTHONDUMPREFS`.

      Cần một bản build đặc biệt của Python với macro ``Py_TRACE_REFS`` được định nghĩa: xem :option:`configure --with-trace-refs option <--with-trace-refs>`.

      Mặc định: ``0``.

   .. c:member:: wchar_t* dump_refs_file

      Tên tệp nơi ghi kết xuất các tham chiếu Python.

      Được đặt bởi biến môi trường :envvar:`PYTHONDUMPREFSFILE`.

      Mặc định: ``NULL``.

      .. versionadded:: 3.11

   .. c:member:: wchar_t* exec_prefix

      Tiền tố thư mục dành riêng cho site, nơi các tệp Python phụ thuộc nền tảng được cài đặt: :data:`sys.exec_prefix`.

      Mặc định: ``NULL``.

      Là một phần của đầu ra :ref:`Cấu hình đường dẫn Python <init-path-config>`.

      Xem thêm :c:member:`PyConfig.base_exec_prefix`.

   .. c:member:: wchar_t* executable

      Đường dẫn tuyệt đối của tệp nhị phân thực thi cho trình thông dịch Python:
      :data:`sys.executable`.

      Mặc định: ``NULL``.

      Là một phần của đầu ra :ref:`Cấu hình đường dẫn Python <init-path-config>`.

      Xem thêm :c:member:`PyConfig.base_executable`.

   .. c:member:: int faulthandler

      Bật faulthandler?

      Nếu khác không, gọi :func:`faulthandler.enable` khi khởi động.

      Được đặt thành ``1`` bởi :option:`-X faulthandler <-X>` và
      biến môi trường :envvar:`PYTHONFAULTHANDLER`.

      Mặc định: ``-1`` trong chế độ Python, ``0`` trong chế độ cô lập.

   .. c:member:: wchar_t* filesystem_encoding

      :term:`Mã hóa hệ thống tệp <filesystem encoding and error handler>`:
      :func:`sys.getfilesystemencoding`.

      Trên macOS, Android và VxWorks: mặc định sử dụng ``"utf-8"``.

      Trên Windows: theo mặc định, sử dụng ``"utf-8"``, hoặc ``"mbcs"`` nếu
      :c:member:`~PyPreConfig.legacy_windows_fs_encoding` của
      :c:type:`PyPreConfig` khác 0.

      Encoding mặc định trên các nền tảng khác:

      * ``"utf-8"`` nếu :c:member:`PyPreConfig.utf8_mode` khác 0.
      * ``"ascii"`` nếu Python phát hiện rằng ``nl_langinfo(CODESET)`` công bố encoding ASCII, trong khi hàm ``mbstowcs()`` giải mã từ một encoding khác (thường là Latin1).
      * ``"utf-8"`` nếu ``nl_langinfo(CODESET)`` trả về một chuỗi rỗng.
      * Nếu không, hãy sử dụng kết quả :term:`locale encoding`: ``nl_langinfo(CODESET)``.

      Khi Python khởi động, tên encoding được chuẩn hóa thành tên codec của Python. Ví dụ: ``"ANSI_X3.4-1968"`` được thay thế bằng ``"ascii"``.

      Xem thêm member :c:member:`~PyConfig.filesystem_errors`.

   .. c:member:: wchar_t* filesystem_errors

      :term:`Bộ xử lý lỗi hệ thống tệp <filesystem encoding and error handler>`:
      :func:`sys.getfilesystemencodeerrors`.

      Trên Windows: theo mặc định, sử dụng ``"surrogatepass"``, hoặc ``"replace"``  nếu
      :c:member:`~PyPreConfig.legacy_windows_fs_encoding` của
      :c:type:`PyPreConfig` khác 0.

      Trên các nền tảng khác: theo mặc định, sử dụng ``"surrogateescape"``.

      Các trình xử lý lỗi được hỗ trợ:

      * ``"strict"``
      * ``"surrogateescape"``
      * ``"surrogatepass"`` (chỉ được hỗ trợ với mã hóa UTF-8)

      Xem thêm thành viên :c:member:`~PyConfig.filesystem_encoding`.

   .. c:member:: int use_frozen_modules

      Nếu khác không, sử dụng các mô-đun frozen.

      Được thiết lập bởi biến môi trường :envvar:`PYTHON_FROZEN_MODULES`.

      Mặc định: ``1`` trong bản dựng phát hành hoặc ``0`` trong :ref:`bản dựng gỡ lỗi <debug-build>`.

   .. c:member:: unsigned long hash_seed
   .. c:member:: int use_hash_seed

      Seed của hàm băm ngẫu nhiên.

      Nếu :c:member:`~PyConfig.use_hash_seed` bằng 0, một seed được chọn ngẫu nhiên khi Python khởi động, và :c:member:`~PyConfig.hash_seed` bị bỏ qua.

      Được thiết lập bởi biến môi trường :envvar:`PYTHONHASHSEED`.

      Giá trị mặc định của *use_hash_seed*: ``-1`` trong chế độ Python, ``0`` trong chế độ cô lập.

   .. c:member:: wchar_t* home

      Thiết lập thư mục "home" mặc định của Python, tức là vị trí của các thư viện Python chuẩn (xem :envvar:`PYTHONHOME`).

      Được thiết lập bởi biến môi trường :envvar:`PYTHONHOME`.

      Mặc định: ``NULL``.

      Một phần của :ref:`Cấu hình Đường dẫn Python <init-path-config>` đầu vào.

   .. c:member:: int import_time

      Nếu ``1``, đo thời gian import. Nếu ``2``, bao gồm đầu ra bổ sung cho biết khi một module được import đã được tải.

      Được thiết lập bởi tùy chọn :option:`-X importtime <-X>` và
      biến môi trường :envvar:`PYTHONPROFILEIMPORTTIME`.

      Mặc định: ``0``.

     .. versionchanged:: 3.14

        Đã thêm hỗ trợ cho ``import_time = 2``

   .. c:member:: int inspect

      Chuyển sang chế độ tương tác sau khi thực thi script hoặc lệnh.

      Nếu lớn hơn ``0``, bật inspect: khi một script được truyền dưới dạng đối số đầu tiên hoặc tùy chọn -c được sử dụng, chuyển sang chế độ tương tác sau khi thực thi script hoặc lệnh, ngay cả khi :data:`sys.stdin` dường như không phải là một terminal.

      Được tăng lên bởi tùy chọn dòng lệnh :option:`-i`. Đặt thành ``1`` nếu
      biến môi trường :envvar:`PYTHONINSPECT` không rỗng.

      Mặc định: ``0``.

   .. c:member:: int install_signal_handlers

      Cài đặt các signal handler của Python?

      Mặc định: ``1`` trong chế độ Python, ``0`` trong chế độ isolated.

   .. c:member:: int interactive

      Nếu lớn hơn ``0``, bật chế độ tương tác (REPL).

      Được tăng lên bởi tùy chọn dòng lệnh :option:`-i`.

      Mặc định: ``0``.

   .. c:member:: int int_max_str_digits

      Cấu hình :ref:`giới hạn độ dài chuyển đổi chuỗi số nguyên <int_max_str_digits>`.  Giá trị ban đầu là ``-1``, nghĩa là giá trị sẽ được lấy từ dòng lệnh hoặc môi trường; nếu không, mặc định là 4300 (:data:`sys.int_info.default_max_str_digits`).  Giá trị ``0`` sẽ tắt giới hạn.  Các giá trị lớn hơn 0 nhưng nhỏ hơn 640 (:data:`sys.int_info.str_digits_check_threshold`) không được hỗ trợ và sẽ gây ra lỗi.

      Được cấu hình bằng cờ dòng lệnh :option:`-X int_max_str_digits <-X>` hoặc biến môi trường :envvar:`PYTHONINTMAXSTRDIGITS`.

      Mặc định: ``-1`` ở chế độ Python.  4300 (:data:`sys.int_info.default_max_str_digits`) ở chế độ cô lập.

      .. versionadded:: 3.12

   .. c:member:: int cpu_count

      Nếu giá trị của :c:member:`~PyConfig.cpu_count` không phải là ``-1`` thì giá trị đó sẽ ghi đè các giá trị trả về của :func:`os.cpu_count`,
      :func:`os.process_cpu_count` và :func:`multiprocessing.cpu_count`.

      Được cấu hình bằng cờ dòng lệnh :samp:`-X cpu_count={n|default}` hoặc biến môi trường :envvar:`PYTHON_CPU_COUNT`.

      Mặc định: ``-1``.

      .. versionadded:: 3.13

   .. c:member:: int isolated

      Nếu lớn hơn ``0``, bật isolated mode:

      * Đặt :c:member:`~PyConfig.safe_path` thành ``1``: không thêm tiền tố là một đường dẫn có khả năng không an toàn vào :data:`sys.path` khi Python khởi động, chẳng hạn như thư mục hiện tại, thư mục của script hoặc một chuỗi rỗng.
      * Đặt :c:member:`~PyConfig.use_environment` thành ``0``: bỏ qua các biến môi trường ``PYTHON``.
      * Đặt :c:member:`~PyConfig.user_site_directory` thành ``0``: không thêm thư mục site của người dùng vào :data:`sys.path`.
      * Python REPL không import :mod:`readline` cũng như không bật cấu hình readline mặc định trong các lời nhắc tương tác.

      Được đặt thành ``1`` bởi tùy chọn dòng lệnh :option:`-I`.

      Mặc định: ``0`` trong chế độ Python, ``1`` trong chế độ cô lập.

      Xem thêm :ref:`Cấu hình cô lập <init-isolated-conf>` và
      :c:member:`PyPreConfig.isolated`.

   .. c:member:: int legacy_windows_stdio

      Nếu khác không, sử dụng :class:`io.FileIO` thay vì
      :class:`!io._WindowsConsoleIO` cho :data:`sys.stdin`, :data:`sys.stdout` và :data:`sys.stderr`.

      Được đặt thành ``1`` nếu biến môi trường :envvar:`PYTHONLEGACYWINDOWSSTDIO` được đặt thành một chuỗi không rỗng.

      Chỉ khả dụng trên Windows. Có thể sử dụng macro ``#ifdef MS_WINDOWS`` cho mã dành riêng cho Windows.

      Mặc định: ``0``.

      Xem thêm :pep:`528` (Thay đổi mã hóa console của Windows thành UTF-8).

   .. c:member:: int malloc_stats

      Nếu khác 0, kết xuất thống kê về :ref:`bộ cấp phát bộ nhớ Python pymalloc <pymalloc>` khi thoát.

      Được đặt thành ``1`` bởi biến môi trường :envvar:`PYTHONMALLOCSTATS`.

      Tùy chọn này bị bỏ qua nếu Python là :option:`configured using the --without-pymalloc option <--without-pymalloc>`.

      Mặc định: ``0``.

   .. c:member:: wchar_t* platlibdir

      Tên thư mục thư viện nền tảng: :data:`sys.platlibdir`.

      Được thiết lập bởi biến môi trường :envvar:`PYTHONPLATLIBDIR`.

      Mặc định: giá trị của macro ``PLATLIBDIR``, được thiết lập bởi
      :option:`configure --with-platlibdir option <--with-platlibdir>` (mặc định: ``"lib"``, hoặc ``"DLLs"`` trên Windows).

      Một phần của :ref:`Cấu hình Đường dẫn Python <init-path-config>` đầu vào.

      .. versionadded:: 3.9

      .. versionchanged:: 3.11
         Macro này hiện được sử dụng trên Windows để xác định vị trí các module mở rộng của thư viện chuẩn, thường nằm trong ``DLLs``. Tuy nhiên, để đảm bảo khả năng tương thích, lưu ý rằng giá trị này bị bỏ qua đối với mọi bố cục không chuẩn, bao gồm các bản build trong cây mã nguồn và môi trường ảo.

   .. c:member:: wchar_t* pythonpath_env

      Các đường dẫn tìm kiếm module (:data:`sys.path`) dưới dạng chuỗi được phân tách bằng ``DELIM`` (:data:`os.pathsep`).

      Được thiết lập bởi biến môi trường :envvar:`PYTHONPATH`.

      Mặc định: ``NULL``.

      Một phần của :ref:`Cấu hình Đường dẫn Python <init-path-config>` đầu vào.

   .. c:member:: PyWideStringList module_search_paths
   .. c:member:: int module_search_paths_set

      Đường dẫn tìm kiếm module: :data:`sys.path`.

      Nếu :c:member:`~PyConfig.module_search_paths_set` bằng ``0``,
      :c:func:`Py_InitializeFromConfig` sẽ thay thế
      :c:member:`~PyConfig.module_search_paths` và đặt
      :c:member:`~PyConfig.module_search_paths_set` thành ``1``.

      Mặc định: danh sách trống (``module_search_paths``) và ``0`` (``module_search_paths_set``).

      Là một phần của đầu ra :ref:`Cấu hình đường dẫn Python <init-path-config>`.

   .. c:member:: int optimization_level

      Mức tối ưu hóa khi biên dịch:

      * ``0``: Trình tối ưu hóa Peephole, đặt ``__debug__`` thành ``True``.
      * ``1``: Mức 0, loại bỏ các câu lệnh assertion, đặt ``__debug__`` thành ``False``.
      * ``2``: Mức 1, loại bỏ docstring.

      Được tăng lên bởi tùy chọn dòng lệnh :option:`-O`. Đặt thành
      giá trị của biến môi trường :envvar:`PYTHONOPTIMIZE`.

      Mặc định: ``0``.

   .. c:member:: PyWideStringList orig_argv

      Danh sách các đối số dòng lệnh ban đầu được truyền cho tệp thực thi Python: :data:`sys.orig_argv`.

      Nếu danh sách :c:member:`~PyConfig.orig_argv` trống và
      :c:member:`~PyConfig.argv` không phải là một danh sách chỉ chứa một chuỗi rỗng, :c:func:`PyConfig_Read` sao chép :c:member:`~PyConfig.argv` vào
      :c:member:`~PyConfig.orig_argv` trước khi sửa đổi
      :c:member:`~PyConfig.argv` (nếu :c:member:`~PyConfig.parse_argv` khác không).

      Xem thêm thành viên :c:member:`~PyConfig.argv` và
      hàm :c:func:`Py_GetArgcArgv`.

      Mặc định: danh sách trống.

      .. versionadded:: 3.10

   .. c:member:: int parse_argv

      Phân tích cú pháp các đối số dòng lệnh?

      Nếu bằng ``1``, hãy phân tích cú pháp :c:member:`~PyConfig.argv` theo cùng cách Python thông thường phân tích cú pháp :ref:`command line arguments <using-on-cmdline>`, rồi loại bỏ các đối số Python khỏi :c:member:`~PyConfig.argv`.

      Hàm :c:func:`PyConfig_Read` chỉ phân tích cú pháp
      Các :c:member:`PyConfig.argv` đối số chỉ được phân tích cú pháp một lần: :c:member:`PyConfig.parse_argv` được đặt thành ``2`` sau khi các đối số được phân tích cú pháp. Vì các đối số Python bị loại bỏ khỏi :c:member:`PyConfig.argv`, việc phân tích cú pháp các đối số hai lần sẽ phân tích các tùy chọn của ứng dụng như các tùy chọn Python.

      Mặc định: ``1`` trong chế độ Python, ``0`` trong chế độ isolated.

      .. versionchanged:: 3.10
         Các đối số :c:member:`PyConfig.argv` hiện chỉ được phân tích cú pháp nếu
         :c:member:`PyConfig.parse_argv` bằng ``1``.

   .. c:member:: int parser_debug

      Chế độ debug của parser. Nếu lớn hơn ``0``, bật đầu ra debug của parser (chỉ dành cho chuyên gia, tùy thuộc vào các tùy chọn biên dịch).

      Được tăng lên bởi tùy chọn dòng lệnh :option:`-d`. Đặt thành
      giá trị của biến môi trường :envvar:`PYTHONDEBUG`.

      Cần một bản build :ref:`debug của Python <debug-build>` (macro ``Py_DEBUG`` phải được định nghĩa).

      Mặc định: ``0``.

   .. c:member:: int pathconfig_warnings

      Nếu khác không, việc tính toán cấu hình đường dẫn được phép ghi cảnh báo vào ``stderr``. Nếu bằng ``0``, các cảnh báo này sẽ bị bỏ qua.

      Mặc định: ``1`` trong chế độ Python, ``0`` trong chế độ isolated.

      Một phần của :ref:`Cấu hình Đường dẫn Python <init-path-config>` đầu vào.

      .. versionchanged:: 3.11
         Hiện cũng áp dụng trên Windows.

   .. c:member:: wchar_t* prefix

      Tiền tố thư mục dành riêng cho site nơi các tệp Python độc lập với nền tảng được cài đặt: :data:`sys.prefix`.

      Mặc định: ``NULL``.

      Là một phần của đầu ra :ref:`Cấu hình đường dẫn Python <init-path-config>`.

      Xem thêm :c:member:`PyConfig.base_prefix`.

   .. c:member:: wchar_t* program_name

      Tên chương trình được dùng để khởi tạo :c:member:`~PyConfig.executable` và trong các thông báo lỗi sớm trong quá trình khởi tạo Python.

      * Trên macOS, sử dụng biến môi trường :envvar:`PYTHONEXECUTABLE` nếu biến này được đặt.
      * Nếu macro ``WITH_NEXT_FRAMEWORK`` được định nghĩa, sử dụng biến môi trường ``__PYVENV_LAUNCHER__`` nếu biến này được đặt.
      * Sử dụng ``argv[0]`` của :c:member:`~PyConfig.argv` nếu có và không rỗng.
      * Nếu không, sử dụng ``L"python"`` trên Windows hoặc ``L"python3"`` trên các nền tảng khác.

      Mặc định: ``NULL``.

      Một phần của :ref:`Cấu hình Đường dẫn Python <init-path-config>` đầu vào.

   .. c:member:: wchar_t* pycache_prefix

      Thư mục nơi các tệp ``.pyc`` được lưu vào bộ nhớ đệm:
      :data:`sys.pycache_prefix`.

      Được thiết lập bởi tùy chọn dòng lệnh :option:`-X pycache_prefix=PATH <-X>` và biến môi trường :envvar:`PYTHONPYCACHEPREFIX`. Tùy chọn dòng lệnh được ưu tiên.

      Nếu ``NULL``, :data:`sys.pycache_prefix` được đặt thành ``None``.

      Mặc định: ``NULL``.

   .. c:member:: int quiet

      Chế độ im lặng. Nếu lớn hơn ``0``, không hiển thị thông tin bản quyền và phiên bản khi Python khởi động ở chế độ tương tác.

      Được tăng lên bởi tùy chọn dòng lệnh :option:`-q`.

      Mặc định: ``0``.

   .. c:member:: wchar_t* run_command

      Giá trị của tùy chọn dòng lệnh :option:`-c`.

      Được :c:func:`Py_RunMain` sử dụng.

      Mặc định: ``NULL``.

   .. c:member:: wchar_t* run_filename

      Tên tệp được truyền trên dòng lệnh: đối số dòng lệnh ở cuối, không có :option:`-c` hoặc :option:`-m`. Nó được sử dụng bởi
      hàm :c:func:`Py_RunMain`.

      Ví dụ, nó được đặt thành ``script.py`` bởi dòng lệnh ``python3 script.py arg``.

      Xem thêm tùy chọn :c:member:`PyConfig.skip_source_first_line`.

      Mặc định: ``NULL``.

   .. c:member:: wchar_t* run_module

      Giá trị của tùy chọn dòng lệnh :option:`-m`.

      Được :c:func:`Py_RunMain` sử dụng.

      Mặc định: ``NULL``.

   .. c:member:: wchar_t* run_presite

      ``package.module`` đường dẫn đến mô-đun cần được import trước khi chạy ``site.py``.

      Được thiết lập bằng tùy chọn dòng lệnh :option:`-X presite=package.module <-X>` và biến môi trường :envvar:`PYTHON_PRESITE`. Tùy chọn dòng lệnh được ưu tiên.

      Cần một bản build :ref:`debug của Python <debug-build>` (macro ``Py_DEBUG`` phải được định nghĩa).

      Mặc định: ``NULL``.

   .. c:member:: int show_ref_count

      Hiển thị tổng số lượt tham chiếu khi thoát (không bao gồm các đối tượng :term:`immortal` )?

      Được thiết lập thành ``1`` bởi tùy chọn dòng lệnh :option:`-X showrefcount <-X>`.

      Cần một bản dựng :ref:`debug của Python <debug-build>` (macro ``Py_REF_DEBUG`` phải được định nghĩa).

      Mặc định: ``0``.

   .. c:member:: int site_import

      Nhập module :mod:`site` khi khởi động?

      Nếu bằng không, vô hiệu hóa việc nhập module site và các thao tác phụ thuộc vào site đối với :data:`sys.path` mà việc đó kéo theo.

      Ngoài ra, hãy vô hiệu hóa các thao tác này nếu mô-đun :mod:`site` được import một cách rõ ràng sau đó (hãy gọi :func:`site.main` nếu bạn muốn kích hoạt chúng).

      Được đặt thành ``0`` bởi tùy chọn dòng lệnh :option:`-S`.

      :data:`sys.flags.no_site <sys.flags>` được đặt thành giá trị đảo của
      :c:member:`~PyConfig.site_import`.

      Mặc định: ``1``.

   .. c:member:: int skip_source_first_line

      Nếu khác không, bỏ qua dòng đầu tiên của mã nguồn :c:member:`PyConfig.run_filename`.

      Cho phép sử dụng các dạng ``#!cmd`` không phải Unix. Tùy chọn này chỉ dành cho một thủ thuật riêng của DOS.

      Được đặt thành ``1`` bởi tùy chọn dòng lệnh :option:`-x`.

      Mặc định: ``0``.

   .. c:member:: wchar_t* stdio_encoding
   .. c:member:: wchar_t* stdio_errors

      Encoding và lỗi encoding của :data:`sys.stdin`, :data:`sys.stdout` và
      :data:`sys.stderr` (nhưng :data:`sys.stderr` luôn sử dụng error handler ``"backslashreplace"``).

      Sử dụng biến môi trường :envvar:`PYTHONIOENCODING` nếu biến này không rỗng.

      Encoding mặc định:

      * ``"UTF-8"`` nếu :c:member:`PyPreConfig.utf8_mode` khác không.
      * Nếu không, hãy sử dụng :term:`locale encoding`.

      Trình xử lý lỗi mặc định:

      * Trên Windows: sử dụng ``"surrogateescape"``.
      * ``"surrogateescape"`` nếu :c:member:`PyPreConfig.utf8_mode` khác không hoặc nếu locale LC_CTYPE là "C" hoặc "POSIX".
      * ``"strict"`` nếu không.

      Xem thêm :c:member:`PyConfig.legacy_windows_stdio`.

   .. c:member:: int tracemalloc

      Bật tracemalloc?

      Nếu khác không, gọi :func:`tracemalloc.start` khi khởi động.

      Được thiết lập bởi tùy chọn dòng lệnh :option:`-X tracemalloc=N <-X>` và bởi
      biến môi trường :envvar:`PYTHONTRACEMALLOC`.

      Mặc định: ``-1`` trong chế độ Python, ``0`` trong chế độ cô lập.

   .. c:member:: int perf_profiling

      Bật hỗ trợ profiler ``perf`` của Linux?

      Nếu bằng ``1``, bật hỗ trợ cho profiler ``perf`` của Linux.

      Nếu bằng ``2``, bật hỗ trợ cho trình profiler ``perf`` của Linux với hỗ trợ DWARF JIT.

      Được đặt thành ``1`` bằng tùy chọn dòng lệnh :option:`-X perf <-X>` và
      biến môi trường :envvar:`PYTHONPERFSUPPORT`.

      Được đặt thành ``2`` bằng tùy chọn dòng lệnh :option:`-X perf_jit <-X>` và biến môi trường :envvar:`PYTHON_PERF_JIT_SUPPORT`.

      Mặc định: ``-1``.

      .. seealso::
         Xem :ref:`perf_profiling` để biết thêm thông tin.

      .. versionadded:: 3.12

   .. c:member:: wchar_t* stdlib_dir

      Thư mục của thư viện chuẩn Python.

      Mặc định: ``NULL``.

      .. versionadded:: 3.11

   .. c:member:: int use_environment

      Sử dụng :ref:`biến môi trường <using-on-envvars>`?

      Nếu bằng không, bỏ qua :ref:`biến môi trường <using-on-envvars>`.

      Được đặt thành ``0`` bởi biến môi trường :option:`-E`.

      Mặc định: ``1`` trong cấu hình Python và ``0`` trong cấu hình isolated.

   .. c:member:: int use_system_logger

      Nếu khác không, ``stdout`` và ``stderr`` sẽ được chuyển hướng đến system log.

      Chỉ khả dụng trên macOS 10.12 trở lên và trên iOS.

      Mặc định: ``0`` (không sử dụng nhật ký hệ thống) trên macOS; ``1`` trên iOS (sử dụng nhật ký hệ thống).

      .. versionadded:: 3.14

   .. c:member:: int user_site_directory

      Nếu khác không, thêm thư mục site của người dùng vào :data:`sys.path`.

      Được đặt thành ``0`` bởi các tùy chọn dòng lệnh :option:`-s` và :option:`-I`.

      Được đặt thành ``0`` bởi biến môi trường :envvar:`PYTHONNOUSERSITE`.

      Mặc định: ``1`` trong chế độ Python, ``0`` trong chế độ isolated.

   .. c:member:: int verbose

      Chế độ chi tiết. Nếu lớn hơn ``0``, in một thông báo mỗi khi một module được import, cho biết vị trí (tên tệp hoặc module tích hợp) mà từ đó module được tải.

      Nếu lớn hơn hoặc bằng ``2``, in một thông báo cho mỗi tệp được kiểm tra khi tìm kiếm một module. Đồng thời cung cấp thông tin về việc dọn dẹp module khi thoát.

      Được tăng lên bởi tùy chọn dòng lệnh :option:`-v`.

      Được đặt theo giá trị của biến môi trường :envvar:`PYTHONVERBOSE`.

      Mặc định: ``0``.

   .. c:member:: PyWideStringList warnoptions

      Các tùy chọn của mô-đun :mod:`warnings` để xây dựng bộ lọc cảnh báo, theo thứ tự từ ưu tiên thấp đến cao: :data:`sys.warnoptions`.

      Mô-đun :mod:`warnings` thêm :data:`sys.warnoptions` theo thứ tự ngược lại: mục :c:member:`PyConfig.warnoptions` cuối cùng trở thành mục đầu tiên của ``warnings.filters``, được kiểm tra trước (ưu tiên cao nhất).

      Các tùy chọn dòng lệnh :option:`-W` thêm giá trị của chúng vào
      :c:member:`~PyConfig.warnoptions`, có thể được sử dụng nhiều lần.

      Biến môi trường :envvar:`PYTHONWARNINGS` cũng có thể được dùng để thêm các tùy chọn cảnh báo. Có thể chỉ định nhiều tùy chọn, phân tách bằng dấu phẩy (``,``).

      Mặc định: danh sách trống.

   .. c:member:: int write_bytecode

      Nếu bằng ``0``, Python sẽ không cố gắng ghi các tệp ``.pyc`` khi import các mô-đun nguồn.

      Được đặt thành ``0`` bởi tùy chọn dòng lệnh :option:`-B` và
      biến môi trường :envvar:`PYTHONDONTWRITEBYTECODE`.

      :data:`sys.dont_write_bytecode` được khởi tạo bằng giá trị đảo của
      :c:member:`~PyConfig.write_bytecode`.

      Mặc định: ``1``.

   .. c:member:: PyWideStringList xoptions

      Các giá trị của các tùy chọn dòng lệnh :option:`-X`: :data:`sys._xoptions`.

      Mặc định: danh sách trống.

   .. c:member:: int _pystats

      Nếu khác 0, ghi thống kê hiệu năng khi Python thoát.

      Cần một bản build đặc biệt có macro ``Py_STATS``: xem :option:`--enable-pystats`.

      Mặc định: ``0``.

Nếu :c:member:`~PyConfig.parse_argv` khác 0, :c:member:`~PyConfig.argv` các đối số được phân tích cú pháp theo cùng cách Python thông thường phân tích cú pháp :ref:`các đối số dòng lệnh <using-on-cmdline>`, và các đối số Python bị loại bỏ khỏi
:c:member:`~PyConfig.argv`.

Các tùy chọn :c:member:`~PyConfig.xoptions` được phân tích cú pháp để thiết lập các tùy chọn khác: xem tùy chọn dòng lệnh :option:`-X`.

.. versionchanged:: 3.9

   Trường ``show_alloc_count`` đã bị xóa.


.. _init-from-config:

Khởi tạo với PyConfig
---------------------

Việc khởi tạo interpreter từ một struct cấu hình đã được điền đầy đủ được thực hiện bằng cách gọi :c:func:`Py_InitializeFromConfig`.

Bên gọi có trách nhiệm xử lý các exception (lỗi hoặc thoát) bằng cách sử dụng
:c:func:`PyStatus_Exception` và :c:func:`Py_ExitStatusException`.

Nếu :c:func:`PyImport_FrozenModules`, :c:func:`PyImport_AppendInittab` hoặc
:c:func:`PyImport_ExtendInittab` được sử dụng, chúng phải được thiết lập hoặc gọi sau khi Python được tiền khởi tạo và trước khi Python được khởi tạo. Nếu Python được khởi tạo nhiều lần, :c:func:`PyImport_AppendInittab` hoặc
:c:func:`PyImport_ExtendInittab` phải được gọi trước mỗi lần khởi tạo Python.

Cấu hình hiện tại (kiểu ``PyConfig``) được lưu trong ``PyInterpreterState.config``.

Ví dụ thiết lập tên chương trình::

    void init_python(void)
    {
        PyStatus status;

        PyConfig config;
        PyConfig_InitPythonConfig(&config);

        /* Set the program name. Implicitly preinitialize Python. */
        status = PyConfig_SetString(&config, &config.program_name,
                                    L"/path/to/my_program");
        if (PyStatus_Exception(status)) {
            goto exception;
        }

        status = Py_InitializeFromConfig(&config);
        if (PyStatus_Exception(status)) {
            goto exception;
        }
        PyConfig_Clear(&config);
        return;

    exception:
        PyConfig_Clear(&config);
        Py_ExitStatusException(status);
    }

Ví dụ đầy đủ hơn về việc sửa đổi cấu hình mặc định, đọc cấu hình rồi ghi đè một số tham số. Lưu ý rằng kể từ phiên bản 3.11, nhiều tham số không được tính cho đến khi khởi tạo, vì vậy không thể đọc các giá trị từ cấu trúc cấu hình. Mọi giá trị được thiết lập trước khi gọi initialize sẽ không bị thay đổi bởi quá trình khởi tạo::

    PyStatus init_python(const char *program_name)
    {
        PyStatus status;

        PyConfig config;
        PyConfig_InitPythonConfig(&config);

        /* Set the program name before reading the configuration
           (decode byte string from the locale encoding).

           Implicitly preinitialize Python. */
        status = PyConfig_SetBytesString(&config, &config.program_name,
                                         program_name);
        if (PyStatus_Exception(status)) {
            goto done;
        }

        /* Read all configuration at once */
        status = PyConfig_Read(&config);
        if (PyStatus_Exception(status)) {
            goto done;
        }

        /* Specify sys.path explicitly */
        /* If you want to modify the default set of paths, finish
           initialization first and then use PySys_GetObject("path") */
        config.module_search_paths_set = 1;
        status = PyWideStringList_Append(&config.module_search_paths,
                                         L"/path/to/stdlib");
        if (PyStatus_Exception(status)) {
            goto done;
        }
        status = PyWideStringList_Append(&config.module_search_paths,
                                         L"/path/to/more/modules");
        if (PyStatus_Exception(status)) {
            goto done;
        }

        /* Override executable computed by PyConfig_Read() */
        status = PyConfig_SetString(&config, &config.executable,
                                    L"/path/to/my_executable");
        if (PyStatus_Exception(status)) {
            goto done;
        }

        status = Py_InitializeFromConfig(&config);

    done:
        PyConfig_Clear(&config);
        return status;
    }


.. _init-isolated-conf:

Cấu hình cô lập
---------------

:c:func:`PyPreConfig_InitIsolatedConfig` và
Các hàm :c:func:`PyConfig_InitIsolatedConfig` tạo một cấu hình để cô lập Python khỏi hệ thống. Ví dụ: để nhúng Python vào một ứng dụng.

Cấu hình này bỏ qua các biến cấu hình toàn cục, biến môi trường, đối số dòng lệnh (:c:member:`PyConfig.argv` không được phân tích) và thư mục site của người dùng. Các luồng chuẩn của C (ví dụ: ``stdout``) và locale LC_CTYPE được giữ nguyên. Các trình xử lý tín hiệu không được cài đặt.

Các tệp cấu hình vẫn được sử dụng với cấu hình này để xác định những đường dẫn chưa được chỉ định. Hãy bảo đảm :c:member:`PyConfig.home` được chỉ định để tránh việc tính toán cấu hình đường dẫn mặc định.


.. _init-python-config:

Cấu hình Python
---------------

Các hàm :c:func:`PyPreConfig_InitPythonConfig` và :c:func:`PyConfig_InitPythonConfig` tạo một cấu hình để xây dựng Python tùy chỉnh hoạt động như Python thông thường.

Các biến môi trường và đối số dòng lệnh được sử dụng để cấu hình Python, trong khi các biến cấu hình toàn cục bị bỏ qua.

Hàm này bật tính cưỡng chế locale C (:pep:`538`) và :ref:`Chế độ UTF-8 của Python <utf8-mode>` (:pep:`540`) tùy thuộc vào locale LC_CTYPE, :envvar:`PYTHONUTF8` và
:envvar:`PYTHONCOERCECLOCALE` các biến môi trường.


.. _init-path-config:

Cấu hình đường dẫn Python
-------------------------

:c:type:`PyConfig` chứa nhiều trường cho cấu hình đường dẫn:

* Các đầu vào cấu hình đường dẫn:

  * :c:member:`PyConfig.home`
  * :c:member:`PyConfig.platlibdir`
  * :c:member:`PyConfig.pathconfig_warnings`
  * :c:member:`PyConfig.program_name`
  * :c:member:`PyConfig.pythonpath_env`
  * thư mục làm việc hiện tại: để lấy các đường dẫn tuyệt đối
  * biến môi trường ``PATH`` để lấy đường dẫn đầy đủ của chương trình (từ :c:member:`PyConfig.program_name`)
  * biến môi trường ``__PYVENV_LAUNCHER__``
  * (Chỉ dành cho Windows) Các đường dẫn ứng dụng trong registry tại "Software\Python\PythonCore\X.Y\PythonPath" của HKEY_CURRENT_USER và HKEY_LOCAL_MACHINE (trong đó X.Y là phiên bản Python).

* Các trường đầu ra của cấu hình đường dẫn:

  * :c:member:`PyConfig.base_exec_prefix`
  * :c:member:`PyConfig.base_executable`
  * :c:member:`PyConfig.base_prefix`
  * :c:member:`PyConfig.exec_prefix`
  * :c:member:`PyConfig.executable`
  * :c:member:`PyConfig.module_search_paths_set`,
    :c:member:`PyConfig.module_search_paths`
  * :c:member:`PyConfig.prefix`

Nếu ít nhất một "trường đầu ra" chưa được thiết lập, Python sẽ tính toán cấu hình đường dẫn để điền các trường chưa được thiết lập. Nếu
:c:member:`~PyConfig.module_search_paths_set` bằng ``0``,
:c:member:`~PyConfig.module_search_paths` bị ghi đè và
:c:member:`~PyConfig.module_search_paths_set` được đặt thành ``1``.

Có thể hoàn toàn bỏ qua hàm tính toán cấu hình đường dẫn mặc định bằng cách thiết lập rõ ràng tất cả các trường đầu ra của cấu hình đường dẫn được liệt kê ở trên. Một chuỗi được xem là đã thiết lập ngay cả khi chuỗi đó không rỗng. ``module_search_paths`` được xem là đã thiết lập nếu ``module_search_paths_set`` được đặt thành ``1``. Trong trường hợp này, ``module_search_paths`` sẽ được sử dụng mà không sửa đổi.

Đặt :c:member:`~PyConfig.pathconfig_warnings` thành ``0`` để ngăn các cảnh báo khi tính toán cấu hình đường dẫn (chỉ Unix; Windows không ghi bất kỳ cảnh báo nào).

Nếu các trường :c:member:`~PyConfig.base_prefix` hoặc :c:member:`~PyConfig.base_exec_prefix` chưa được thiết lập, chúng lần lượt kế thừa giá trị từ :c:member:`~PyConfig.prefix` và :c:member:`~PyConfig.exec_prefix`.

:c:func:`Py_RunMain` và :c:func:`Py_Main` sửa đổi :data:`sys.path`:

* Nếu :c:member:`~PyConfig.run_filename` được thiết lập và là một thư mục chứa một script ``__main__.py``, thêm :c:member:`~PyConfig.run_filename` vào đầu
  :data:`sys.path`.
* Nếu :c:member:`~PyConfig.isolated` bằng không:

  * Nếu :c:member:`~PyConfig.run_module` được thiết lập, thêm thư mục hiện tại vào đầu :data:`sys.path`. Không làm gì nếu không thể đọc thư mục hiện tại.
  * Nếu :c:member:`~PyConfig.run_filename` được thiết lập, thêm thư mục chứa tên tệp vào đầu :data:`sys.path`.
  * Nếu không, thêm một chuỗi rỗng vào đầu :data:`sys.path`.

Nếu :c:member:`~PyConfig.site_import` khác không, :data:`sys.path` có thể được sửa đổi bởi module :mod:`site`. Nếu
:c:member:`~PyConfig.user_site_directory` khác không và thư mục site-package của người dùng tồn tại, module :mod:`site` sẽ nối thư mục site-package của người dùng vào :data:`sys.path`.

Các tệp cấu hình sau được sử dụng cho cấu hình đường dẫn:

* ``pyvenv.cfg``
* tệp ``._pth`` (ví dụ: ``python._pth``)
* ``pybuilddir.txt`` (chỉ dành cho Unix)

Nếu có tệp ``._pth``:

* Đặt :c:member:`~PyConfig.isolated` thành ``1``.
* Đặt :c:member:`~PyConfig.use_environment` thành ``0``.
* Đặt :c:member:`~PyConfig.site_import` thành ``0``.
* Đặt :c:member:`~PyConfig.safe_path` thành ``1``.

Nếu :c:member:`~PyConfig.home` chưa được đặt và có tệp ``pyvenv.cfg`` trong cùng thư mục với :c:member:`~PyConfig.executable` hoặc trong thư mục cha của nó,
:c:member:`~PyConfig.prefix` và :c:member:`~PyConfig.exec_prefix` được đặt thành vị trí đó. Khi điều này xảy ra, :c:member:`~PyConfig.base_prefix` và
:c:member:`~PyConfig.base_exec_prefix` vẫn giữ nguyên giá trị, trỏ đến bản cài đặt cơ sở. Xem :ref:`sys-path-init-virtual-environments` để biết thêm thông tin.

Biến môi trường ``__PYVENV_LAUNCHER__`` được dùng để đặt
:c:member:`PyConfig.base_executable`.

.. versionchanged:: 3.14

   :c:member:`~PyConfig.prefix` và :c:member:`~PyConfig.exec_prefix` hiện được đặt thành thư mục ``pyvenv.cfg``. Trước đây, việc này được thực hiện bởi :mod:`site`, nên bị ảnh hưởng bởi :option:`-S`.


Py_GetArgcArgv()
================

.. c:function:: void Py_GetArgcArgv(int *argc, wchar_t ***argv)

   Lấy các đối số dòng lệnh ban đầu, trước khi Python sửa đổi chúng.

   Xem thêm member :c:member:`PyConfig.orig_argv`.

Trì hoãn việc thực thi module chính
===================================

Trong một số trường hợp nhúng, bạn có thể muốn tách việc khởi tạo interpreter khỏi việc thực thi module chính.

Có thể thực hiện việc tách này bằng cách đặt ``PyConfig.run_command`` thành chuỗi rỗng trong quá trình khởi tạo (để ngăn interpreter chuyển sang dấu nhắc tương tác), sau đó thực thi mã của module chính mong muốn bằng cách sử dụng ``__main__.__dict__`` làm global namespace.
