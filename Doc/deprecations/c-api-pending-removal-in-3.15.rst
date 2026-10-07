Đang chờ loại bỏ trong Python 3.15
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* :c:func:`PyImport_ImportModuleNoBlock`: Thay vào đó, hãy sử dụng :c:func:`PyImport_ImportModule`.
* :c:func:`PyWeakref_GetObject` và :c:func:`PyWeakref_GET_OBJECT`: Thay vào đó, hãy sử dụng :c:func:`PyWeakref_GetRef`. Có thể sử dụng `pythoncapi-compat project <https://github.com/python/pythoncapi-compat/>`__ để lấy
  :c:func:`PyWeakref_GetRef` trên Python 3.12 trở về trước.
* kiểu :c:type:`Py_UNICODE` và macro :c:macro:`!Py_UNICODE_WIDE`: Thay vào đó, hãy sử dụng :c:type:`wchar_t`.
* :c:func:`!PyUnicode_AsDecodedObject`: Thay vào đó, hãy sử dụng :c:func:`PyCodec_Decode`.
* :c:func:`!PyUnicode_AsDecodedUnicode`: Thay vào đó, hãy sử dụng :c:func:`PyCodec_Decode`; lưu ý rằng một số codec (ví dụ: "base64") có thể trả về một kiểu khác với :class:`str`, chẳng hạn như :class:`bytes`.
* :c:func:`!PyUnicode_AsEncodedObject`: Thay vào đó, hãy sử dụng :c:func:`PyCodec_Encode`.
* :c:func:`!PyUnicode_AsEncodedUnicode`: Thay vào đó, hãy sử dụng :c:func:`PyCodec_Encode`; lưu ý rằng một số codec (ví dụ: "base64") có thể trả về kiểu khác với :class:`bytes`, chẳng hạn như :class:`str`.
* Các hàm khởi tạo Python, đã không còn được khuyến nghị sử dụng trong Python 3.13:

  * :c:func:`Py_GetPath`: Thay vào đó, hãy sử dụng :c:func:`PyConfig_Get("module_search_paths") <PyConfig_Get>` (:data:`sys.path`).
  * :c:func:`Py_GetPrefix`: Thay vào đó, hãy sử dụng :c:func:`PyConfig_Get("base_prefix") <PyConfig_Get>` (:data:`sys.base_prefix`). Sử dụng :c:func:`PyConfig_Get("prefix") <PyConfig_Get>` (:data:`sys.prefix`) nếu cần xử lý :ref:`virtual environments <venv-def>`.
  * :c:func:`Py_GetExecPrefix`: Thay vào đó, hãy sử dụng :c:func:`PyConfig_Get("base_exec_prefix") <PyConfig_Get>` (:data:`sys.base_exec_prefix`). Sử dụng
    :c:func:`PyConfig_Get("exec_prefix") <PyConfig_Get>` (:data:`sys.exec_prefix`) nếu cần xử lý :ref:`virtual environments <venv-def>`.
  * :c:func:`Py_GetProgramFullPath`: Thay vào đó, hãy sử dụng :c:func:`PyConfig_Get("executable") <PyConfig_Get>` (:data:`sys.executable`).
  * :c:func:`Py_GetProgramName`: Thay vào đó, hãy sử dụng :c:func:`PyConfig_Get("executable") <PyConfig_Get>` (:data:`sys.executable`).
  * :c:func:`Py_GetPythonHome`: Thay vào đó, hãy sử dụng :c:func:`PyConfig_Get("home") <PyConfig_Get>` hoặc
    thay vào đó sử dụng biến môi trường :envvar:`PYTHONHOME`.

  Có thể sử dụng `dự án pythoncapi-compat <https://github.com/python/pythoncapi-compat/>`__ để lấy
  :c:func:`PyConfig_Get` trên Python 3.13 và các phiên bản cũ hơn.

* Các hàm dùng để cấu hình quá trình khởi tạo Python, đã bị deprecated trong Python 3.11:

  * :c:func:`!PySys_SetArgvEx()`: Thay vào đó, hãy đặt :c:member:`PyConfig.argv`.
  * :c:func:`!PySys_SetArgv()`: Thay vào đó, hãy đặt :c:member:`PyConfig.argv`.
  * :c:func:`!Py_SetProgramName()`: Thay vào đó, hãy đặt :c:member:`PyConfig.program_name`.
  * :c:func:`!Py_SetPythonHome()`: Thay vào đó, hãy đặt :c:member:`PyConfig.home`.
  * :c:func:`PySys_ResetWarnOptions`: Thay vào đó, hãy xóa :data:`sys.warnoptions` và :data:`!warnings.filters`.

  API :c:func:`Py_InitializeFromConfig` nên được sử dụng cùng với
  :c:type:`PyConfig` thay vào đó.

* Các biến cấu hình toàn cục:

  * :c:var:`Py_DebugFlag`: Sử dụng :c:member:`PyConfig.parser_debug` hoặc
    :c:func:`PyConfig_Get("parser_debug") <PyConfig_Get>` thay vào đó.
  * :c:var:`Py_VerboseFlag`: Sử dụng :c:member:`PyConfig.verbose` hoặc
    :c:func:`PyConfig_Get("verbose") <PyConfig_Get>` thay vào đó.
  * :c:var:`Py_QuietFlag`: Sử dụng :c:member:`PyConfig.quiet` hoặc
    :c:func:`PyConfig_Get("quiet") <PyConfig_Get>` thay vào đó.
  * :c:var:`Py_InteractiveFlag`: Sử dụng :c:member:`PyConfig.interactive` hoặc
    :c:func:`PyConfig_Get("interactive") <PyConfig_Get>` thay vào đó.
  * :c:var:`Py_InspectFlag`: Sử dụng :c:member:`PyConfig.inspect` hoặc
    :c:func:`PyConfig_Get("inspect") <PyConfig_Get>` thay vào đó.
  * :c:var:`Py_OptimizeFlag`: Sử dụng :c:member:`PyConfig.optimization_level` hoặc
    :c:func:`PyConfig_Get("optimization_level") <PyConfig_Get>` thay vào đó.
  * :c:var:`Py_NoSiteFlag`: Sử dụng :c:member:`PyConfig.site_import` hoặc
    :c:func:`PyConfig_Get("site_import") <PyConfig_Get>` thay vào đó.
  * :c:var:`Py_BytesWarningFlag`: Sử dụng :c:member:`PyConfig.bytes_warning` hoặc
    :c:func:`PyConfig_Get("bytes_warning") <PyConfig_Get>` thay vào đó.
  * :c:var:`Py_FrozenFlag`: Sử dụng :c:member:`PyConfig.pathconfig_warnings` hoặc
    :c:func:`PyConfig_Get("pathconfig_warnings") <PyConfig_Get>` thay vào đó.
  * :c:var:`Py_IgnoreEnvironmentFlag`: Sử dụng :c:member:`PyConfig.use_environment` hoặc
    :c:func:`PyConfig_Get("use_environment") <PyConfig_Get>` thay vào đó.
  * :c:var:`Py_DontWriteBytecodeFlag`: Sử dụng :c:member:`PyConfig.write_bytecode` hoặc
    :c:func:`PyConfig_Get("write_bytecode") <PyConfig_Get>` thay vào đó.
  * :c:var:`Py_NoUserSiteDirectory`: Sử dụng :c:member:`PyConfig.user_site_directory` hoặc
    :c:func:`PyConfig_Get("user_site_directory") <PyConfig_Get>` thay vào đó.
  * :c:var:`Py_UnbufferedStdioFlag`: Sử dụng :c:member:`PyConfig.buffered_stdio` hoặc
    :c:func:`PyConfig_Get("buffered_stdio") <PyConfig_Get>` thay vào đó.
  * :c:var:`Py_HashRandomizationFlag`: Sử dụng :c:member:`PyConfig.use_hash_seed` và :c:member:`PyConfig.hash_seed` hoặc
    :c:func:`PyConfig_Get("hash_seed") <PyConfig_Get>` thay vào đó.
  * :c:var:`Py_IsolatedFlag`: Sử dụng :c:member:`PyConfig.isolated` hoặc
    :c:func:`PyConfig_Get("isolated") <PyConfig_Get>` thay vào đó.
  * :c:var:`Py_LegacyWindowsFSEncodingFlag`: Sử dụng :c:member:`PyPreConfig.legacy_windows_fs_encoding` hoặc
    :c:func:`PyConfig_Get("legacy_windows_fs_encoding") <PyConfig_Get>` thay vào đó.
  * :c:var:`Py_LegacyWindowsStdioFlag`: Sử dụng :c:member:`PyConfig.legacy_windows_stdio` hoặc
    :c:func:`PyConfig_Get("legacy_windows_stdio") <PyConfig_Get>` thay vào đó.
  * :c:var:`!Py_FileSystemDefaultEncoding`, :c:var:`!Py_HasFileSystemDefaultEncoding`: Sử dụng :c:member:`PyConfig.filesystem_encoding` hoặc
    :c:func:`PyConfig_Get("filesystem_encoding") <PyConfig_Get>` thay vào đó.
  * :c:var:`!Py_FileSystemDefaultEncodeErrors`: Sử dụng :c:member:`PyConfig.filesystem_errors` hoặc
    :c:func:`PyConfig_Get("filesystem_errors") <PyConfig_Get>` thay vào đó.
  * :c:var:`!Py_UTF8Mode`: Sử dụng :c:member:`PyPreConfig.utf8_mode` hoặc
    :c:func:`PyConfig_Get("utf8_mode") <PyConfig_Get>` thay vào đó. (xem :c:func:`Py_PreInitialize`)

  API :c:func:`Py_InitializeFromConfig` nên được sử dụng cùng với
  :c:type:`PyConfig` để thiết lập các tùy chọn này. Hoặc có thể sử dụng :c:func:`PyConfig_Get` để lấy các tùy chọn này trong runtime.
