***************
Cấu hình Python
***************

.. highlight:: sh


.. _build-requirements:

Yêu cầu để build
================

Để build CPython, bạn sẽ cần:

* Một trình biên dịch `C11 <https://en.cppreference.com/w/c/11>`_. Không yêu cầu `các tính năng C11 tùy chọn <https://en.wikipedia.org/wiki/C11_(C_standard_revision)#Optional_features>`_.

* Trên Windows, cần có Microsoft Visual Studio 2017 hoặc phiên bản mới hơn.

* Hỗ trợ số dấu phẩy động `IEEE 754 <https://en.wikipedia.org/wiki/IEEE_754>`_ và `giá trị Không-phải-số (NaN) dấu phẩy động <https://en.wikipedia.org/wiki/NaN#Floating_point>`_.

* Hỗ trợ luồng.

.. versionchanged:: 3.5
   Trên Windows, hiện yêu cầu Visual Studio 2015 trở lên.

.. versionchanged:: 3.6
   Hiện yêu cầu một số tính năng C99 được chọn, chẳng hạn như các hàm ``<stdint.h>`` và ``static inline``.

.. versionchanged:: 3.7
   Hiện yêu cầu hỗ trợ thread.

.. versionchanged:: 3.11
   Hiện yêu cầu trình biên dịch C11, IEEE 754 và hỗ trợ NaN. Trên Windows, yêu cầu Visual Studio 2017 trở lên.

Xem thêm :pep:`7` "Hướng dẫn phong cách viết mã C" và :pep:`11` "Hỗ trợ nền tảng CPython".


.. _optional-module-requirements:

Yêu cầu đối với các module tùy chọn
-----------------------------------

Một số :term:`module tùy chọn <optional module>` của thư viện chuẩn yêu cầu cài đặt các thư viện bên thứ ba để phát triển (ví dụ: phải có sẵn các tệp header).

Các yêu cầu còn thiếu được báo cáo trong đầu ra ``configure``. Các mô-đun bị thiếu do thiếu dependency được liệt kê gần cuối đầu ra ``make``, đôi khi sử dụng tên nội bộ; ví dụ: ``_ctypes`` cho mô-đun :mod:`ctypes`.

Nếu bạn phân phối một trình thông dịch CPython không có các mô-đun tùy chọn, cách làm tốt nhất là thông báo cho người dùng, vì họ thường kỳ vọng các mô-đun trong standard library luôn khả dụng.

Các dependency để build các mô-đun tùy chọn là:

.. list-table::
   :header-rows: 1
   :align: left

   * - Dependency
     - Phiên bản tối thiểu
     - Mô-đun Python
   * - `libbz2 <https://sourceware.org/bzip2/>`_
   ---------------------------------------------
     - :mod:`bz2`
   * - `libffi <https://sourceware.org/libffi/>`_
     - khuyến nghị dùng 3.3.0
     - :mod:`ctypes`
   * - `liblzma <https://tukaani.org/xz/>`_
   ----------------------------------------
     - :mod:`lzma`
   * - `libmpdec <https://www.bytereef.org/mpdecimal/doc/libmpdec/>`_
     - 2.5.0
     - :mod:`decimal` [1]_
   * - `libreadline <https://tiswww.case.edu/php/chet/readline/rltop.html>`_ hoặc
       `libedit <https://www.thrysoee.dk/editline/>`_ [2]_
       ---------------------------------------------------
     - :mod:`readline`
   * - `libuuid <https://linux.die.net/man/3/libuuid>`_
   ----------------------------------------------------
     - ``_uuid`` [3]_
   * - `ncurses <https://gnu.org/software/ncurses/ncurses.html>`_ [4]_
   -------------------------------------------------------------------
     - :mod:`curses`
   * - `OpenSSL <https://openssl-library.org/>`_
     - [6]_
     - :mod:`ssl`, :mod:`hashlib` [5]_
   * - `SQLite <https://sqlite.org/>`_
     - 3.15.2
     - :mod:`sqlite3`
   * - `Tcl/Tk <https://www.tcl-lang.org/>`_
     - 8.5.12
     - :mod:`tkinter`, :ref:`IDLE <idle>`, :mod:`turtle`
   * - `zlib <https://www.zlib.net>`_
     - 1.2.2.1
     - :mod:`zlib`, :mod:`gzip`, :mod:`ensurepip`
   * - `zstd <https://facebook.github.io/zstd/>`_
     - 1.4.5
     - :mod:`compression.zstd`

.. [1] Nếu *libmpdec* không khả dụng, module :mod:`decimal` sẽ sử dụng một implementation thuần Python. Xem :option:`--with-system-libmpdec` để biết chi tiết.
.. [2] Xem :option:`--with-readline` để biết cách chọn backend cho
   module :mod:`readline`.
.. [3] Module :mod:`uuid` sử dụng ``_uuid`` để tạo UUID “an toàn”. Xem tài liệu của module để biết chi tiết.
.. [4] Module :mod:`curses` yêu cầu thư viện ``libncurses`` hoặc ``libncursesw``. Module :mod:`curses.panel` cũng yêu cầu thư viện ``libpanel`` hoặc ``libpanelw``.
.. [5] Nếu OpenSSL không khả dụng, module :mod:`hashlib` sẽ sử dụng các implementation đi kèm của một số hàm băm. Xem :option:`--with-builtin-hashlib-hashes` để *buộc* sử dụng OpenSSL.
.. [6] OpenSSL 1.1.1 là phiên bản tối thiểu có thể dùng để build, nhưng dòng phiên bản này đã hết vòng đời và không còn nhận được các bản sửa lỗi bảo mật công khai. Hãy sử dụng bản phát hành vá mới nhất của một dòng bản phát hành LTS hiện đang được hỗ trợ (xem `OpenSSL Roadmap <https://openssl-library.org/roadmap/index.html>`__), hoặc gói do hệ điều hành cung cấp nếu có. Các thư viện khác cung cấp API tương thích với OpenSSL 1.1.1 trở lên có thể hoạt động, nhưng không được hỗ trợ chính thức.

Lưu ý rằng bảng này không bao gồm tất cả các module tùy chọn; đặc biệt là các module dành riêng cho từng nền tảng như :mod:`winreg` không được liệt kê ở đây.

.. seealso::

   * `devguide <https://devguide.python.org/getting-started/setup-building/#install-dependencies>`_ bao gồm danh sách đầy đủ các dependency cần thiết để xây dựng tất cả các module và hướng dẫn cách cài đặt chúng trên các nền tảng phổ biến.
   * :option:`--with-system-expat` cho phép xây dựng với thư viện bên ngoài `libexpat <https://libexpat.github.io/>`_.
   * :ref:`configure-options-for-dependencies`

.. versionchanged:: 3.1
   Tcl/Tk phiên bản 8.3.1 hiện được yêu cầu cho :mod:`tkinter`.

.. versionchanged:: 3.5
   Tcl/Tk phiên bản 8.4 hiện được yêu cầu cho :mod:`tkinter`.

.. versionchanged:: 3.7
   OpenSSL 1.0.2 hiện được yêu cầu cho :mod:`hashlib` và :mod:`ssl`.

.. versionchanged:: 3.10
   OpenSSL 1.1.1 hiện được yêu cầu cho :mod:`hashlib` và :mod:`ssl`. SQLite 3.7.15 hiện được yêu cầu cho :mod:`sqlite3`.

.. versionchanged:: 3.11
   Tcl/Tk phiên bản 8.5.12 hiện được yêu cầu cho :mod:`tkinter`.

.. versionchanged:: 3.13
   SQLite 3.15.2 hiện được yêu cầu cho :mod:`sqlite3`.


Các tệp được tạo
================

Để giảm các dependency khi build, mã nguồn Python chứa nhiều tệp được tạo. Các lệnh để tạo lại tất cả các tệp được tạo::

    make regen-all
    make regen-stdlib-module-names
    make regen-limited-abi
    make regen-configure

Tệp ``Makefile.pre.in`` ghi lại các tệp được tạo, đầu vào của chúng và các công cụ được sử dụng để tạo lại chúng. Tìm các target make ``regen-*``.

Tập lệnh configure
------------------

Lệnh ``make regen-configure`` tạo lại tệp ``aclocal.m4`` và tập lệnh ``configure`` bằng tập lệnh shell ``Tools/build/regen-configure.sh``, sử dụng một container Ubuntu để có cùng phiên bản công cụ và tạo ra đầu ra có thể tái lập.

Container là tùy chọn; bạn có thể chạy lệnh sau locally::

    autoreconf -ivf -Werror

Các tệp được tạo có thể thay đổi tùy thuộc vào phiên bản chính xác của các công cụ được sử dụng. Container mà CPython sử dụng có `Autoconf <https://gnu.org/software/autoconf>`_ 2.72, ``aclocal`` từ `Automake <https://www.gnu.org/software/automake>`_ 1.16.5 và `pkg-config <https://www.freedesktop.org/wiki/Software/pkg-config/>`_ 1.8.1.

.. versionchanged:: 3.13
   Autoconf 2.71 và aclocal 1.16.5 hiện được sử dụng để tạo lại
   :file:`configure`.

.. versionchanged:: 3.14
   Autoconf 2.72 hiện được sử dụng để tạo lại :file:`configure`.


.. _configure-options:

Các tùy chọn Configure
======================

Liệt kê tất cả các tùy chọn của script :file:`configure` bằng cách sử dụng::

    ./configure --help

Xem thêm :file:`Misc/SpecialBuilds.txt` trong bản phân phối mã nguồn Python.

Tùy chọn chung
--------------

.. option:: --enable-loadable-sqlite-extensions

   Support loadable extensions in the :mod:`!_sqlite` extension module (default
   is no) of the :mod:`sqlite3` module.

   See the :meth:`sqlite3.Connection.enable_load_extension` method of the
   :mod:`sqlite3` module.

   .. versionadded:: 3.6

.. option:: --disable-ipv6

   Disable IPv6 support (enabled by default if supported), see the
   :mod:`socket` module.

.. option:: --enable-big-digits=[15|30]

   Define the size in bits of Python :class:`int` digits: 15 or 30 bits.

   By default, the digit size is 30.

   Define the ``PYLONG_BITS_IN_DIGIT`` to ``15`` or ``30``.

   See :data:`sys.int_info.bits_per_digit <sys.int_info>`.

.. option:: --with-suffix=SUFFIX

   Set the Python executable suffix to *SUFFIX*.

   The default suffix is ``.exe`` on Windows and macOS (``python.exe``
   executable), ``.js`` on Emscripten node, ``.html`` on Emscripten browser,
   ``.wasm`` on WASI, and an empty string on other platforms (``python``
   executable).

   .. versionchanged:: 3.11
      The default suffix on WASM platform is one of ``.js``, ``.html``
      or ``.wasm``.

.. option:: --with-tzpath=<list of absolute paths separated by pathsep>

   Select the default time zone search path for :const:`zoneinfo.TZPATH`.
   See the :ref:`Compile-time configuration
   <zoneinfo_data_compile_time_config>` of the :mod:`zoneinfo` module.

   Default: ``/usr/share/zoneinfo:/usr/lib/zoneinfo:/usr/share/lib/zoneinfo:/etc/zoneinfo``.

   See :data:`os.pathsep` path separator.

   .. versionadded:: 3.9

.. option:: --without-decimal-contextvar

   Build the ``_decimal`` extension module using a thread-local context rather
   than a coroutine-local context (default), see the :mod:`decimal` module.

   See :const:`decimal.HAVE_CONTEXTVAR` and the :mod:`contextvars` module.

   .. versionadded:: 3.9

.. option:: --with-dbmliborder=<list of backend names>

   Override order to check db backends for the :mod:`dbm` module

   A valid value is a colon (``:``) separated string with the backend names:

   * ``ndbm``;
   * ``gdbm``;
   * ``bdb``.

.. option:: --without-c-locale-coercion

   Disable C locale coercion to a UTF-8 based locale (enabled by default).

   Don't define the ``PY_COERCE_C_LOCALE`` macro.

   See :envvar:`PYTHONCOERCECLOCALE` and the :pep:`538`.

.. option:: --with-platlibdir=DIRNAME

   Python library directory name (default is ``lib``).

   Fedora and SuSE use ``lib64`` on 64-bit platforms.

   See :data:`sys.platlibdir`.

   .. versionadded:: 3.9

.. option:: --with-wheel-pkg-dir=PATH

   Directory of wheel packages used by the :mod:`ensurepip` module
   (none by default).

   Some Linux distribution packaging policies recommend against bundling
   dependencies. For example, Fedora installs wheel packages in the
   ``/usr/share/python-wheels/`` directory and don't install the
   :mod:`!ensurepip._bundled` package.

   .. versionadded:: 3.10

.. option:: --with-pkg-config=[check|yes|no]

   Whether configure should use :program:`pkg-config` to detect build
   dependencies.

   * ``check`` (default): :program:`pkg-config` is optional
   * ``yes``: :program:`pkg-config` is mandatory
   * ``no``: configure does not use :program:`pkg-config` even when present

   .. versionadded:: 3.11

.. option:: --enable-pystats

   Turn on internal Python performance statistics gathering.

   By default, statistics gathering is off. Use ``python3 -X pystats`` command
   or set ``PYTHONSTATS=1`` environment variable to turn on statistics
   gathering at Python startup.

   At Python exit, dump statistics if statistics gathering was on and not
   cleared.

   Effects:

   * Add :option:`-X pystats <-X>` command line option.
   * Add :envvar:`!PYTHONSTATS` environment variable.
   * Define the ``Py_STATS`` macro.
   * Add functions to the :mod:`sys` module:

     * :func:`!sys._stats_on`: Turns on statistics gathering.
     * :func:`!sys._stats_off`: Turns off statistics gathering.
     * :func:`!sys._stats_clear`: Clears the statistics.
     * :func:`!sys._stats_dump`: Dump statistics to file, and clears the statistics.

   The statistics will be dumped to a arbitrary (probably unique) file in
   ``/tmp/py_stats/`` (Unix) or ``C:\temp\py_stats\`` (Windows). If that
   directory does not exist, results will be printed on stderr.

   Use ``Tools/scripts/summarize_stats.py`` to read the stats.

   Statistics:

   * Opcode:

     * Specialization: success, failure, hit, deferred, miss, deopt, failures;
     * Execution count;
     * Pair count.

   * Call:

     * Inlined Python calls;
     * PyEval calls;
     * Frames pushed;
     * Frame object created;
     * Eval calls: vector, generator, legacy, function VECTORCALL, build class,
       slot, function "ex", API, method.

   * Object:

     * incref and decref;
     * interpreter incref and decref;
     * allocations: all, 512 bytes, 4 kiB, big;
     * free;
     * to/from free lists;
     * dictionary materialized/dematerialized;
     * type cache;
     * optimization attempts;
     * optimization traces created/executed;
     * uops executed.

   * Garbage collector:

     * Garbage collections;
     * Objects visited;
     * Objects collected.

   .. versionadded:: 3.11

.. _free-threading-build:

.. option:: --disable-gil

   Enables support for running Python without the :term:`global interpreter
   lock` (GIL): :term:`free-threaded build`.

   Defines the ``Py_GIL_DISABLED`` macro and adds ``"t"`` to
   :data:`sys.abiflags`.

   See :ref:`whatsnew313-free-threaded-cpython` for more detail.

   .. versionadded:: 3.13

.. option:: --enable-experimental-jit=[no|yes|yes-off|interpreter]

   Indicate how to integrate the :ref:`experimental just-in-time compiler <whatsnew314-jit-compiler>`.

   * ``no``: Don't build the JIT.
   * ``yes``: Enable the JIT. To disable it at runtime, set the environment
     variable :envvar:`PYTHON_JIT=0 <PYTHON_JIT>`.
   * ``yes-off``: Build the JIT, but disable it by default. To enable it at
     runtime, set the environment variable :envvar:`PYTHON_JIT=1 <PYTHON_JIT>`.
   * ``interpreter``: Enable the "JIT interpreter" (only useful for those
     debugging the JIT itself). To disable it at runtime, set the environment
     variable :envvar:`PYTHON_JIT=0 <PYTHON_JIT>`.

   ``--enable-experimental-jit=no`` is the default behavior if the option is not
   provided, and ``--enable-experimental-jit`` is shorthand for
   ``--enable-experimental-jit=yes``.  See :file:`Tools/jit/README.md` for more
   information, including how to install the necessary build-time dependencies.

   .. note::

      When building CPython with JIT enabled, ensure that your system has Python 3.11 or later installed.

   .. versionadded:: 3.13

.. option:: PKG_CONFIG

   Path to ``pkg-config`` utility.

.. option:: PKG_CONFIG_LIBDIR
.. option:: PKG_CONFIG_PATH

   ``pkg-config`` options.


Tùy chọn trình biên dịch C
--------------------------

.. option:: CC

   C compiler command.

.. option:: CFLAGS

   C compiler flags.

.. option:: CPP

   C preprocessor command.

.. option:: CPPFLAGS

   C preprocessor flags, e.g. :samp:`-I{include_dir}`.


Tùy chọn linker
---------------

.. option:: LDFLAGS

   Linker flags, e.g. :samp:`-L{library_directory}`.

.. option:: LIBS

   Libraries to pass to the linker, e.g. :samp:`-l{library}`.

.. option:: MACHDEP

   Name for machine-dependent library files.


.. _configure-options-for-dependencies:

Tùy chọn cho các dependency bên thứ ba
--------------------------------------

.. versionadded:: 3.11

.. option:: BZIP2_CFLAGS
.. option:: BZIP2_LIBS

   C compiler and linker flags to link Python to ``libbz2``, used by :mod:`bz2`
   module, overriding ``pkg-config``.

.. option:: CURSES_CFLAGS
.. option:: CURSES_LIBS

   C compiler and linker flags for ``libncurses`` or ``libncursesw``, used by
   :mod:`curses` module, overriding ``pkg-config``.

.. option:: GDBM_CFLAGS
.. option:: GDBM_LIBS

   C compiler and linker flags for ``gdbm``.

.. option:: LIBEDIT_CFLAGS
.. option:: LIBEDIT_LIBS

   C compiler and linker flags for ``libedit``, used by :mod:`readline` module,
   overriding ``pkg-config``.

.. option:: LIBFFI_CFLAGS
.. option:: LIBFFI_LIBS

   C compiler and linker flags for ``libffi``, used by :mod:`ctypes` module,
   overriding ``pkg-config``.

.. option:: LIBMPDEC_CFLAGS
.. option:: LIBMPDEC_LIBS

   C compiler and linker flags for ``libmpdec``, used by :mod:`decimal` module,
   overriding ``pkg-config``.

   .. note::

      These environment variables have no effect unless
      :option:`--with-system-libmpdec` is specified.

.. option:: LIBLZMA_CFLAGS
.. option:: LIBLZMA_LIBS

   C compiler and linker flags for ``liblzma``, used by :mod:`lzma` module,
   overriding ``pkg-config``.

.. option:: LIBREADLINE_CFLAGS
.. option:: LIBREADLINE_LIBS

   C compiler and linker flags for ``libreadline``, used by :mod:`readline`
   module, overriding ``pkg-config``.

.. option:: LIBSQLITE3_CFLAGS
.. option:: LIBSQLITE3_LIBS

   C compiler and linker flags for ``libsqlite3``, used by :mod:`sqlite3`
   module, overriding ``pkg-config``.

.. option:: LIBUUID_CFLAGS
.. option:: LIBUUID_LIBS

   C compiler and linker flags for ``libuuid``, used by :mod:`uuid` module,
   overriding ``pkg-config``.

.. option:: LIBZSTD_CFLAGS
.. option:: LIBZSTD_LIBS

   C compiler and linker flags for ``libzstd``, used by :mod:`compression.zstd` module,
   overriding ``pkg-config``.

   .. versionadded:: 3.14

.. option:: PANEL_CFLAGS
.. option:: PANEL_LIBS

   C compiler and linker flags for PANEL, overriding ``pkg-config``.

   C compiler and linker flags for ``libpanel`` or ``libpanelw``, used by
   :mod:`curses.panel` module, overriding ``pkg-config``.

.. option:: TCLTK_CFLAGS
.. option:: TCLTK_LIBS

   C compiler and linker flags for TCLTK, overriding ``pkg-config``.

.. option:: ZLIB_CFLAGS
.. option:: ZLIB_LIBS

   C compiler and linker flags for ``libzlib``, used by :mod:`gzip` module,
   overriding ``pkg-config``.


Tùy chọn WebAssembly
--------------------

.. option:: --enable-wasm-dynamic-linking

   Turn on dynamic linking support for WASM.

   Dynamic linking enables ``dlopen``. File size of the executable
   increases due to limited dead code elimination and additional features.

   .. versionadded:: 3.11

.. option:: --enable-wasm-pthreads

   Turn on pthreads support for WASM.

   .. versionadded:: 3.11


Tùy chọn cài đặt
----------------

.. option:: --prefix=PREFIX

   Install architecture-independent files in PREFIX. On Unix, it
   defaults to :file:`/usr/local`.

   This value can be retrieved at runtime using :data:`sys.prefix`.

   As an example, one can use ``--prefix="$HOME/.local/"`` to install
   a Python in its home directory.

.. option:: --exec-prefix=EPREFIX

   Install architecture-dependent files in EPREFIX, defaults to :option:`--prefix`.

   This value can be retrieved at runtime using :data:`sys.exec_prefix`.

.. option:: --disable-test-modules

   Don't build nor install test modules, like the :mod:`test` package or the
   :mod:`!_testcapi` extension module (built and installed by default).

   .. versionadded:: 3.10

.. option:: --with-ensurepip=[upgrade|install|no]

   Select the :mod:`ensurepip` command run on Python installation:

   * ``upgrade`` (default): run ``python -m ensurepip --altinstall --upgrade``
     command.
   * ``install``: run ``python -m ensurepip --altinstall`` command;
   * ``no``: don't run ensurepip;

   .. versionadded:: 3.6


Tùy chọn hiệu năng
------------------

Bạn nên cấu hình Python bằng ``--enable-optimizations --with-lto`` (PGO + LTO) để đạt hiệu năng tốt nhất. Cũng có thể sử dụng cờ thử nghiệm ``--enable-bolt`` để cải thiện hiệu năng.

.. option:: --enable-optimizations

   Enable Profile Guided Optimization (PGO) using :envvar:`PROFILE_TASK`
   (disabled by default).

   The C compiler Clang requires ``llvm-profdata`` program for PGO. On
   macOS, GCC also requires it: GCC is just an alias to Clang on macOS.

   Disable also semantic interposition in libpython if ``--enable-shared`` and
   GCC is used: add ``-fno-semantic-interposition`` to the compiler and linker
   flags.

   .. note::

      During the build, you may encounter compiler warnings about
      profile data not being available for some source files.
      These warnings are harmless, as only a subset of the code is exercised
      during profile data acquisition.
      To disable these warnings on Clang, manually suppress them by adding
      ``-Wno-profile-instr-unprofiled`` to :envvar:`CFLAGS`.

   .. versionadded:: 3.6

   .. versionchanged:: 3.10
      Use ``-fno-semantic-interposition`` on GCC.

.. envvar:: PROFILE_TASK

   Environment variable used in the Makefile: Python command line arguments for
   the PGO generation task.

   Default: ``-m test --pgo --timeout=$(TESTTIMEOUT)``.

   .. versionadded:: 3.8

   .. versionchanged:: 3.13
      Task failure is no longer ignored silently.

.. option:: --with-lto=[full|thin|no|yes]

   Enable Link Time Optimization (LTO) in any build (disabled by default).

   The C compiler Clang requires ``llvm-ar`` for LTO (``ar`` on macOS), as well
   as an LTO-aware linker (``ld.gold`` or ``lld``).

   .. versionadded:: 3.6

   .. versionadded:: 3.11
      To use ThinLTO feature, use ``--with-lto=thin`` on Clang.

   .. versionchanged:: 3.12
      Use ThinLTO as the default optimization policy on Clang if the compiler accepts the flag.

.. option:: --enable-bolt

   Enable usage of the `BOLT post-link binary optimizer
   <https://github.com/llvm/llvm-project/tree/main/bolt>`_ (disabled by
   default).

   BOLT is part of the LLVM project but is not always included in their binary
   distributions. This flag requires that ``llvm-bolt`` and ``merge-fdata``
   are available.

   BOLT is still a fairly new project so this flag should be considered
   experimental for now. Because this tool operates on machine code its success
   is dependent on a combination of the build environment + the other
   optimization configure args + the CPU architecture, and not all combinations
   are supported.
   BOLT versions before LLVM 16 are known to crash BOLT under some scenarios.
   Use of LLVM 16 or newer for BOLT optimization is strongly encouraged.

   The :envvar:`!BOLT_INSTRUMENT_FLAGS` and :envvar:`!BOLT_APPLY_FLAGS`
   :program:`configure` variables can be defined to override the default set of
   arguments for :program:`llvm-bolt` to instrument and apply BOLT data to
   binaries, respectively.

   .. versionadded:: 3.12

.. option:: BOLT_APPLY_FLAGS

   Arguments to ``llvm-bolt`` when creating a `BOLT optimized binary
   <https://github.com/facebookarchive/BOLT>`_.

   .. versionadded:: 3.12

.. option:: BOLT_INSTRUMENT_FLAGS

   Arguments to ``llvm-bolt`` when instrumenting binaries.

   .. versionadded:: 3.12

.. option:: --with-computed-gotos

   Enable computed gotos in evaluation loop (enabled by default on supported
   compilers).

.. option:: --with-tail-call-interp

   Enable interpreters using tail calls in CPython. If enabled, enabling PGO
   (:option:`--enable-optimizations`) is highly recommended. This option specifically
   requires a C compiler with proper tail call support, and the
   `preserve_none <https://clang.llvm.org/docs/AttributeReference.html#preserve-none>`_
   calling convention. For example, Clang 19 and newer supports this feature.

   .. versionadded:: 3.14

.. option:: --without-mimalloc

   Disable the fast :ref:`mimalloc <mimalloc>` allocator
   (enabled by default).

   This option cannot be used together with :option:`--disable-gil`
   because the :term:`free-threaded <free threading>` build requires mimalloc.

   See also :envvar:`PYTHONMALLOC` environment variable.

.. option:: --without-pymalloc

   Disable the specialized Python memory allocator :ref:`pymalloc <pymalloc>`
   (enabled by default).

   See also :envvar:`PYTHONMALLOC` environment variable.

.. option:: --without-doc-strings

   Disable static documentation strings to reduce the memory footprint (enabled
   by default). Documentation strings defined in Python are not affected.

   Don't define the ``WITH_DOC_STRINGS`` macro.

   See the ``PyDoc_STRVAR()`` macro.

.. option:: --enable-profiling

   Enable C-level code profiling with ``gprof`` (disabled by default).

.. option:: --with-strict-overflow

   Add ``-fstrict-overflow`` to the C compiler flags (by default we add
   ``-fno-strict-overflow`` instead).

.. option:: --without-remote-debug

   Deactivate remote debugging support described in :pep:`768` (enabled by default).
   When this flag is provided the code that allows the interpreter to schedule the
   execution of a Python file in a separate process as described in :pep:`768` is
   not compiled. This includes both the functionality to schedule code to be executed
   and the functionality to receive code to be executed.

   .. c:macro:: Py_REMOTE_DEBUG

      This macro is defined by default, unless Python is configured with
      :option:`--without-remote-debug`.

      Note that even if the macro is defined, remote debugging may not be
      available (for example, on an incompatible platform).

   .. versionadded:: 3.14


.. _debug-build:

Bản dựng gỡ lỗi Python
----------------------

Bản dựng gỡ lỗi là Python được xây dựng với tùy chọn cấu hình :option:`--with-pydebug`.

Các tác động của bản dựng gỡ lỗi:

* Hiển thị tất cả cảnh báo theo mặc định: danh sách các bộ lọc cảnh báo mặc định trong mô-đun :mod:`warnings` là rỗng.
* Thêm ``d`` vào :data:`sys.abiflags`.
* Thêm hàm :func:`!sys.gettotalrefcount`.
* Thêm tùy chọn dòng lệnh :option:`-X showrefcount <-X>`.
* Thêm tùy chọn dòng lệnh :option:`-d` và biến môi trường :envvar:`PYTHONDEBUG` để gỡ lỗi parser.
* Thêm hỗ trợ cho biến ``__lltrace__``: bật tracing cấp thấp trong vòng lặp đánh giá bytecode nếu biến này được định nghĩa.
* Cài đặt :ref:`hook debug trên các trình cấp phát bộ nhớ <default-memory-allocators>` để phát hiện lỗi tràn bộ đệm và các lỗi bộ nhớ khác.
* Định nghĩa các macro ``Py_DEBUG`` và ``Py_REF_DEBUG``.
* Thêm các kiểm tra runtime: mã được bao quanh bởi ``#ifdef Py_DEBUG`` và ``#endif``. Bật các assertion ``assert(...)`` và ``_PyObject_ASSERT(...)``: không đặt macro ``NDEBUG`` (xem thêm tùy chọn configure :option:`--with-assertions`). Các kiểm tra runtime chính:

  * Thêm các kiểm tra tính hợp lệ cho các đối số của hàm.
  * Các đối tượng Unicode và int được tạo với vùng nhớ được điền bằng một mẫu để phát hiện việc sử dụng các đối tượng chưa được khởi tạo.
  * Đảm bảo rằng các hàm có thể xóa hoặc thay thế exception hiện tại không được gọi khi đang có một exception được phát sinh.
  * Kiểm tra để đảm bảo các hàm deallocator không thay đổi exception hiện tại.
  * Bộ thu gom rác (hàm :func:`gc.collect`) thực hiện một số kiểm tra cơ bản về tính nhất quán của các đối tượng.
  * Macro :c:macro:`!Py_SAFE_DOWNCAST()` kiểm tra underflow và overflow của số nguyên khi downcast từ các kiểu có độ rộng lớn sang các kiểu có độ rộng nhỏ hơn.

Xem thêm :ref:`Chế độ Phát triển Python <devmode>` và
:option:`--with-trace-refs` là tùy chọn configure.

.. versionchanged:: 3.8
   Các bản build release hiện tương thích ABI với các bản build debug: việc định nghĩa macro ``Py_DEBUG`` không còn ngụ ý macro ``Py_TRACE_REFS`` (xem
   tùy chọn :option:`--with-trace-refs`). Tuy nhiên, các bản build debug vẫn cung cấp nhiều symbol hơn các bản build release, và mã được build dựa trên bản build debug không nhất thiết tương thích với bản build release.


Các tùy chọn debug
------------------

.. option:: --with-pydebug

   :ref:`Build Python in debug mode <debug-build>`: define the ``Py_DEBUG``
   macro (disabled by default).

.. option:: --with-trace-refs

   Enable tracing references for debugging purpose (disabled by default).

   Effects:

   * Define the ``Py_TRACE_REFS`` macro.
   * Add :func:`sys.getobjects` function.
   * Add :envvar:`PYTHONDUMPREFS` environment variable.

   The :envvar:`PYTHONDUMPREFS` environment variable can be used to dump
   objects and reference counts still alive at Python exit.

   :ref:`Statically allocated objects <static-types>` are not traced.

   .. versionadded:: 3.8

   .. versionchanged:: 3.13
      This build is now ABI compatible with release build and :ref:`debug build
      <debug-build>`.

.. option:: --with-assertions

   Build with C assertions enabled (default is no): ``assert(...);`` and
   ``_PyObject_ASSERT(...);``.

   If set, the ``NDEBUG`` macro is not defined in the :envvar:`OPT` compiler
   variable.

   See also the :option:`--with-pydebug` option (:ref:`debug build
   <debug-build>`) which also enables assertions.

   .. versionadded:: 3.6

.. option:: --with-valgrind

   Enable Valgrind support (default is no).

.. option:: --with-dtrace

   Enable DTrace support (default is no).

   See :ref:`Instrumenting CPython with DTrace and SystemTap
   <instrumentation>`.

   .. versionadded:: 3.6

.. option:: --with-address-sanitizer

   Enable AddressSanitizer memory error detector, ``asan`` (default is no).
   To improve ASan detection capabilities you may also want to combine this
   with :option:`--without-pymalloc` to disable the specialized small-object
   allocator whose allocations are not tracked by ASan.

   .. versionadded:: 3.6

.. option:: --with-memory-sanitizer

   Enable MemorySanitizer allocation error detector, ``msan`` (default is no).

   MSan reports false positives for memory initialized by libraries that are
   not built with MSan, so either build all dependencies with MSan or disable
   the extension modules that use them in :file:`Modules/Setup.local`.

   .. versionadded:: 3.6

.. option:: --with-undefined-behavior-sanitizer

   Enable UndefinedBehaviorSanitizer undefined behaviour detector, ``ubsan``
   (default is no).

   .. versionadded:: 3.6

.. option:: --with-thread-sanitizer

   Enable ThreadSanitizer data race detector, ``tsan``
   (default is no).

   .. versionadded:: 3.13


Tùy chọn linker
---------------

.. option:: --enable-shared

   Enable building a shared Python library: ``libpython`` (default is no).

.. option:: --without-static-libpython

   Do not build ``libpythonMAJOR.MINOR.a`` and do not install ``python.o``
   (built and enabled by default).

   .. versionadded:: 3.10


Các tùy chọn thư viện
---------------------

.. option:: --with-libs='lib1 ...'

   Link against additional libraries (default is no).

.. option:: --with-system-expat

   Build the :mod:`!pyexpat` module using an installed ``expat`` library
   (default is no).

.. option:: --with-system-libmpdec

   Build the ``_decimal`` extension module using an installed ``mpdecimal``
   library, see the :mod:`decimal` module (default is yes).

   .. versionadded:: 3.3

   .. versionchanged:: 3.13
      Default to using the installed ``mpdecimal`` library.

   .. versionchanged:: 3.15

      A bundled copy of the library will no longer be selected
      implicitly if an installed ``mpdecimal`` library is not found.
      In Python 3.15 only, it can still be selected explicitly using
      ``--with-system-libmpdec=no`` or ``--without-system-libmpdec``.

   .. deprecated-removed:: 3.13 3.16
      A copy of the ``mpdecimal`` library sources will no longer be distributed
      with Python 3.16.

   .. seealso:: :option:`LIBMPDEC_CFLAGS` and :option:`LIBMPDEC_LIBS`.

.. option:: --with-readline=readline|editline

   Designate a backend library for the :mod:`readline` module.

   * readline: Use readline as the backend.
   * editline: Use editline as the backend.

   .. versionadded:: 3.10

.. option:: --without-readline

   Don't build the :mod:`readline` module (built by default).

   Don't define the ``HAVE_LIBREADLINE`` macro.

   .. versionadded:: 3.10

.. option:: --with-libm=STRING

   Override ``libm`` math library to *STRING* (default is system-dependent).

.. option:: --with-libc=STRING

   Override ``libc`` C library to *STRING* (default is system-dependent).

.. option:: --with-openssl=DIR

   Root of the OpenSSL directory.

   .. versionadded:: 3.7

.. option:: --with-openssl-rpath=[no|auto|DIR]

   Set runtime library directory (rpath) for OpenSSL libraries:

   * ``no`` (default): don't set rpath;
   * ``auto``: auto-detect rpath from :option:`--with-openssl` and
     ``pkg-config``;
   * *DIR*: set an explicit rpath.

   .. versionadded:: 3.10


Các tùy chọn bảo mật
--------------------

.. option:: --with-hash-algorithm=[fnv|siphash13|siphash24]

   Select hash algorithm for use in ``Python/pyhash.c``:

   * ``siphash13`` (default);
   * ``siphash24``;
   * ``fnv``.

   .. versionadded:: 3.4

   .. versionadded:: 3.11
      ``siphash13`` is added and it is the new default.

.. option:: --with-builtin-hashlib-hashes=md5,sha1,sha256,sha512,sha3,blake2

   Built-in hash modules:

   * ``md5``;
   * ``sha1``;
   * ``sha256``;
   * ``sha512``;
   * ``sha3`` (with shake);
   * ``blake2``.

   .. versionadded:: 3.9

.. option:: --with-ssl-default-suites=[python|openssl|STRING]

   Override the OpenSSL default cipher suites string:

   * ``python`` (default): use Python's preferred selection;
   * ``openssl``: leave OpenSSL's defaults untouched;
   * *STRING*: use a custom string

   See the :mod:`ssl` module.

   .. versionadded:: 3.7

   .. versionchanged:: 3.10

      The settings ``python`` and *STRING* also set TLS 1.2 as minimum
      protocol version.

.. option:: --disable-safety

   Disable compiler options that are `recommended by OpenSSF`_ for security reasons with no performance overhead.
   If this option is not enabled, CPython will be built based on safety compiler options with no slow down.
   When this option is enabled, CPython will not be built with the compiler options listed below.

   The following compiler options are disabled with :option:`!--disable-safety`:

   * `-fstack-protector-strong`_: Enable run-time checks for stack-based buffer overflows.
   * `-Wtrampolines`_: Enable warnings about trampolines that require executable stacks.

   .. _recommended by OpenSSF: https://github.com/ossf/wg-best-practices-os-developers/blob/main/docs/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++.md
   .. _-fstack-protector-strong: https://github.com/ossf/wg-best-practices-os-developers/blob/main/docs/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++.md#enable-run-time-checks-for-stack-based-buffer-overflows
   .. _-Wtrampolines: https://github.com/ossf/wg-best-practices-os-developers/blob/main/docs/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++.md#enable-warning-about-trampolines-that-require-executable-stacks

   .. versionadded:: 3.14

.. option:: --enable-slower-safety

   Enable compiler options that are `recommended by OpenSSF`_ for security reasons which require overhead.
   If this option is not enabled, CPython will not be built based on safety compiler options which performance impact.
   When this option is enabled, CPython will be built with the compiler options listed below.

   The following compiler options are enabled with :option:`!--enable-slower-safety`:

   * `-D_FORTIFY_SOURCE=3`_: Fortify sources with compile- and run-time checks for unsafe libc usage and buffer overflows.

   .. _-D_FORTIFY_SOURCE=3: https://github.com/ossf/wg-best-practices-os-developers/blob/main/docs/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++.md#fortify-sources-for-unsafe-libc-usage-and-buffer-overflows

   .. versionadded:: 3.14


Các tùy chọn macOS
------------------

Xem :source:`Mac/README.rst`.

.. option:: --enable-universalsdk
.. option:: --enable-universalsdk=SDKDIR

   Create a universal binary build. *SDKDIR* specifies which macOS SDK should
   be used to perform the build (default is no).

.. option:: --enable-framework
.. option:: --enable-framework=INSTALLDIR

   Create a Python.framework rather than a traditional Unix install. Optional
   *INSTALLDIR* specifies the installation path (default is no).

.. option:: --with-universal-archs=ARCH

   Specify the kind of universal binary that should be created. This option is
   only valid when :option:`--enable-universalsdk` is set.

   Options:

   * ``universal2`` (x86-64 and arm64);
   * ``32-bit`` (PPC and i386);
   * ``64-bit``  (PPC64 and x86-64);
   * ``3-way`` (i386, PPC and x86-64);
   * ``intel`` (i386 and x86-64);
   * ``intel-32`` (i386);
   * ``intel-64`` (x86-64);
   * ``all``  (PPC, i386, PPC64 and x86-64).

   Note that values for this configuration item are *not* the same as the
   identifiers used for universal binary wheels on macOS. See the Python
   Packaging User Guide for details on the `packaging platform compatibility
   tags used on macOS
   <https://packaging.python.org/en/latest/specifications/platform-compatibility-tags/#macos>`_

.. option:: --with-framework-name=FRAMEWORK

   Specify the name for the python framework on macOS only valid when
   :option:`--enable-framework` is set (default: ``Python``).

.. option:: --with-app-store-compliance
.. option:: --with-app-store-compliance=PATCH-FILE

   The Python standard library contains strings that are known to trigger
   automated inspection tool errors when submitted for distribution by
   the macOS and iOS App Stores. If enabled, this option will apply the list of
   patches that are known to correct app store compliance. A custom patch
   file can also be specified. This option is disabled by default.

   .. versionadded:: 3.13

Tùy chọn iOS
------------

Xem :source:`iOS/README.rst`.

.. option:: --enable-framework=INSTALLDIR

   Create a Python.framework. Unlike macOS, the *INSTALLDIR* argument
   specifying the installation path is mandatory.

.. option:: --with-framework-name=FRAMEWORK

   Specify the name for the framework (default: ``Python``).


Tùy chọn biên dịch chéo
-----------------------

Biên dịch chéo, còn được gọi là cross building, có thể được sử dụng để xây dựng Python cho một kiến trúc CPU hoặc nền tảng khác. Biên dịch chéo yêu cầu một trình thông dịch Python cho build platform. Phiên bản của Python dùng để build phải khớp với phiên bản của Python trên host được biên dịch chéo.

.. option:: --build=BUILD

   configure for building on BUILD, usually guessed by :program:`config.guess`.

.. option:: --host=HOST

   cross-compile to build programs to run on HOST (target platform)

.. option:: --with-build-python=path/to/python

   path to build ``python`` binary for cross compiling

   .. versionadded:: 3.11

.. option:: CONFIG_SITE=file

   An environment variable that points to a file with configure overrides.

   Example *config.site* file:

   .. code-block:: ini

      # config.site-aarch64
      ac_cv_buggy_getaddrinfo=no
      ac_cv_file__dev_ptmx=yes
      ac_cv_file__dev_ptc=no

.. option:: HOSTRUNNER

   Program to run CPython for the host platform for cross-compilation.

   .. versionadded:: 3.11


Ví dụ về biên dịch chéo::

   CONFIG_SITE=config.site-aarch64 ../configure \
       --build=x86_64-pc-linux-gnu \
       --host=aarch64-unknown-linux-gnu \
       --with-build-python=../x86_64/python


Hệ thống xây dựng Python
========================

Các tệp chính của hệ thống build
--------------------------------

* :file:`configure.ac` => :file:`configure`;
* :file:`Makefile.pre.in` => :file:`Makefile` (được tạo bởi :file:`configure`);
* :file:`pyconfig.h` (được tạo bởi :file:`configure`);
* :file:`Modules/Setup`: Các phần mở rộng C được build bởi Makefile bằng
  tập lệnh shell :file:`Module/makesetup`;

Các bước build chính
--------------------

* Các tệp C (``.c``) được build thành các tệp đối tượng (``.o``).
* Một thư viện ``libpython`` tĩnh (``.a``) được tạo từ các tệp đối tượng.
* ``python.o`` và thư viện ``libpython`` tĩnh được liên kết vào chương trình ``python`` cuối cùng.
* Các phần mở rộng C được Makefile xây dựng (xem :file:`Modules/Setup`).

Các target chính của Makefile
-----------------------------

make
^^^^

Trong phần lớn trường hợp, khi xây dựng lại sau khi chỉnh sửa mã hoặc cập nhật checkout của bạn từ upstream, tất cả những gì bạn cần làm là thực thi ``make``, lệnh này (theo semantics của Make) sẽ xây dựng target mặc định, tức target đầu tiên được định nghĩa trong Makefile. Theo thông lệ (bao gồm cả trong dự án CPython), đây thường là target ``all``. Script ``configure`` mở rộng một biến ``autoconf``, ``@DEF_MAKE_ALL_RULE@`` để mô tả chính xác những target nào ``make all`` sẽ xây dựng. Có ba lựa chọn:

* ``profile-opt`` (được cấu hình bằng ``--enable-optimizations``)
* ``build_wasm`` (được chọn nếu nền tảng máy chủ khớp với ``wasm32-wasi*`` hoặc ``wasm32-emscripten``)
* ``build_all`` (được cấu hình mà không sử dụng rõ ràng một trong hai tùy chọn còn lại)

Tùy thuộc vào những thay đổi gần đây nhất đối với các tệp nguồn, Make sẽ xây dựng lại mọi target (tệp đối tượng và tệp thực thi) được xác định là đã lỗi thời, bao gồm cả việc chạy lại ``configure`` nếu cần. Tuy nhiên, các dependency giữa nguồn và target rất nhiều và được duy trì thủ công, nên đôi khi Make không có đủ thông tin cần thiết để phát hiện chính xác tất cả target cần được xây dựng lại. Tùy thuộc vào những target không được xây dựng lại, bạn có thể gặp một số vấn đề. Nếu bạn gặp vấn đề khi build hoặc test mà không thể giải thích theo cách nào khác, ``make clean && make`` sẽ xử lý phần lớn vấn đề về dependency, đổi lại thời gian build sẽ lâu hơn.


make platform
^^^^^^^^^^^^^

Xây dựng chương trình ``python``, nhưng không xây dựng các module mở rộng của standard library. Thao tác này tạo một tệp có tên ``platform``, chứa một dòng duy nhất mô tả chi tiết về nền tảng build, chẳng hạn như ``macosx-14.3-arm64-3.12`` hoặc ``linux-x86_64-3.13``.


make profile-opt
^^^^^^^^^^^^^^^^

Xây dựng Python bằng profile-guided optimization (PGO). Bạn có thể sử dụng tùy chọn configure :option:`--enable-optimizations` để đặt đây làm target mặc định của lệnh ``make`` (``make all`` hoặc chỉ ``make``).



make clean
^^^^^^^^^^

Xóa các tệp đã được build.


make distclean
^^^^^^^^^^^^^^

Ngoài những gì ``make clean`` thực hiện, hãy xóa các tệp do configure script tạo ra. Cần chạy ``configure`` trước khi build lại. [#]_


make install
^^^^^^^^^^^^

Build target ``all`` và cài đặt Python.


make test
^^^^^^^^^

Xây dựng target ``all`` và chạy bộ kiểm thử Python với tùy chọn ``--fast-ci`` mà không chạy các bài kiểm thử GUI. Các biến:

* ``TESTOPTS``: các tùy chọn dòng lệnh regrtest bổ sung.
* ``TESTPYTHONOPTS``: các tùy chọn dòng lệnh Python bổ sung.
* ``TESTTIMEOUT``: thời gian chờ tính bằng giây (mặc định: 10 phút).


make ci
^^^^^^^

Tương tự như ``make test``, nhưng sử dụng ``-ugui`` để chạy thêm các bài kiểm thử GUI.

.. versionadded:: 3.14


make buildbottest
^^^^^^^^^^^^^^^^^

Tương tự như ``make test``, nhưng sử dụng tùy chọn ``--slow-ci`` và thời gian chờ mặc định là 20 phút, thay vì tùy chọn ``--fast-ci``.


make regen-all
^^^^^^^^^^^^^^

Tạo lại (gần như) tất cả các tệp được tạo tự động. Các tệp này bao gồm (nhưng không chỉ giới hạn ở) các trường hợp bytecode và tệp trình tạo parser. Phải chạy riêng ``make regen-stdlib-module-names`` và ``autoconf`` cho các `tệp được tạo còn lại <#generated-files>`_.


C extension
-----------

Một số C extension được build dưới dạng built-in module, chẳng hạn như module ``sys``. Chúng được build với macro ``Py_BUILD_CORE_BUILTIN`` được định nghĩa. Built-in module không có thuộc tính ``__file__``:

.. code-block:: pycon

    >>> import sys
    >>> sys
    <module 'sys' (built-in)>
    >>> sys.__file__
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: module 'sys' has no attribute '__file__'

Các C extension khác được build dưới dạng dynamic library, chẳng hạn như module ``_asyncio``. Chúng được build với macro ``Py_BUILD_CORE_MODULE`` được định nghĩa. Ví dụ trên Linux x86-64:

.. code-block:: pycon

    >>> import _asyncio
    >>> _asyncio
    <module '_asyncio' from '/usr/lib64/python3.9/lib-dynload/_asyncio.cpython-39-x86_64-linux-gnu.so'>
    >>> _asyncio.__file__
    '/usr/lib64/python3.9/lib-dynload/_asyncio.cpython-39-x86_64-linux-gnu.so'

:file:`Modules/Setup` được dùng để tạo các target Makefile nhằm build C extension. Ở phần đầu của các tệp, C extension được build dưới dạng built-in module. Các extension được định nghĩa sau marker ``*shared*`` sẽ được build dưới dạng dynamic library.

Các :c:macro:`!PyAPI_FUNC()`, :c:macro:`!PyAPI_DATA()` và
macro :c:macro:`PyMODINIT_FUNC` của :file:`Include/exports.h` được định nghĩa khác nhau tùy thuộc vào việc macro ``Py_BUILD_CORE_MODULE`` có được định nghĩa hay không:

* Sử dụng ``Py_EXPORTED_SYMBOL`` nếu ``Py_BUILD_CORE_MODULE`` được định nghĩa
* Nếu không, sử dụng ``Py_IMPORTED_SYMBOL``.

Nếu vô tình sử dụng macro ``Py_BUILD_CORE_BUILTIN`` cho một C extension được xây dựng dưới dạng shared library, hàm :samp:`PyInit_{xxx}()` của nó sẽ không được export, gây ra :exc:`ImportError` khi import.


Cờ compiler và linker
=====================

Các tùy chọn được thiết lập bởi script ``./configure`` và các biến môi trường, đồng thời được ``Makefile`` sử dụng.

Cờ preprocessor
---------------

.. envvar:: CONFIGURE_CPPFLAGS

   Value of :envvar:`CPPFLAGS` variable passed to the ``./configure`` script.

   .. versionadded:: 3.6

.. envvar:: CPPFLAGS

   (Objective) C/C++ preprocessor flags, e.g. :samp:`-I{include_dir}` if you have
   headers in a nonstandard directory *include_dir*.

   Both :envvar:`CPPFLAGS` and :envvar:`LDFLAGS` need to contain the shell's
   value to be able to build extension modules using the
   directories specified in the environment variables.

.. envvar:: BASECPPFLAGS

   .. versionadded:: 3.4

.. envvar:: PY_CPPFLAGS

   Extra preprocessor flags added for building the interpreter object files.

   Default: ``$(BASECPPFLAGS) -I. -I$(srcdir)/Include $(CONFIGURE_CPPFLAGS) $(CPPFLAGS)``.

   .. versionadded:: 3.2

Cờ compiler
-----------

.. envvar:: CC

   C compiler command.

   Example: ``gcc -pthread``.

.. envvar:: CXX

   C++ compiler command.

   Example: ``g++ -pthread``.

.. envvar:: CFLAGS

   C compiler flags.

.. envvar:: CFLAGS_NODIST

   :envvar:`CFLAGS_NODIST` is used for building the interpreter and stdlib C
   extensions.  Use it when a compiler flag should *not* be part of
   :envvar:`CFLAGS` once Python is installed (:gh:`65320`).

   In particular, :envvar:`CFLAGS` should not contain:

   * the compiler flag ``-I`` (for setting the search path for include files).
     The ``-I`` flags are processed from left to right, and any flags in
     :envvar:`CFLAGS` would take precedence over user- and package-supplied ``-I``
     flags.

   * hardening flags such as ``-Werror`` because distributions cannot control
     whether packages installed by users conform to such heightened
     standards.

   .. versionadded:: 3.5

.. envvar:: COMPILEALL_OPTS

   Options passed to the :mod:`compileall` command line when building PYC files
   in ``make install``. Default: ``-j0``.

   .. versionadded:: 3.12

.. envvar:: EXTRA_CFLAGS

   Extra C compiler flags.

.. envvar:: CONFIGURE_CFLAGS

   Value of :envvar:`CFLAGS` variable passed to the ``./configure``
   script.

   .. versionadded:: 3.2

.. envvar:: CONFIGURE_CFLAGS_NODIST

   Value of :envvar:`CFLAGS_NODIST` variable passed to the ``./configure``
   script.

   .. versionadded:: 3.5

.. envvar:: BASECFLAGS

   Base compiler flags.

.. envvar:: OPT

   Optimization flags.

.. envvar:: CFLAGS_ALIASING

   Strict or non-strict aliasing flags used to compile ``Python/dtoa.c``.

   .. versionadded:: 3.7

.. envvar:: CFLAGS_CEVAL

   Flags used to compile ``Python/ceval.c``.

   .. versionadded:: 3.14.5

.. envvar:: CCSHARED

   Compiler flags used to build a shared library.

   For example, ``-fPIC`` is used on Linux and on BSD.

.. envvar:: CFLAGSFORSHARED

   Extra C flags added for building the interpreter object files.

   Default: ``$(CCSHARED)`` when :option:`--enable-shared` is used, or an empty
   string otherwise.

.. envvar:: PY_CFLAGS

   Default: ``$(BASECFLAGS) $(OPT) $(CONFIGURE_CFLAGS) $(CFLAGS) $(EXTRA_CFLAGS)``.

.. envvar:: PY_CFLAGS_NODIST

   Default: ``$(CONFIGURE_CFLAGS_NODIST) $(CFLAGS_NODIST) -I$(srcdir)/Include/internal``.

   .. versionadded:: 3.5

.. envvar:: PY_STDMODULE_CFLAGS

   C flags used for building the interpreter object files.

   Default: ``$(PY_CFLAGS) $(PY_CFLAGS_NODIST) $(PY_CPPFLAGS) $(CFLAGSFORSHARED)``.

   .. versionadded:: 3.7

.. envvar:: PY_CORE_CFLAGS

   Default: ``$(PY_STDMODULE_CFLAGS) -DPy_BUILD_CORE``.

   .. versionadded:: 3.2

.. envvar:: PY_BUILTIN_MODULE_CFLAGS

   Compiler flags to build a standard library extension module as a built-in
   module, like the :mod:`posix` module.

   Default: ``$(PY_STDMODULE_CFLAGS) -DPy_BUILD_CORE_BUILTIN``.

   .. versionadded:: 3.8

.. envvar:: PURIFY

   Purify command. Purify is a memory debugger program.

   Default: empty string (not used).


Cờ linker
---------

.. envvar:: LINKCC

   Linker command used to build programs like ``python`` and ``_testembed``.

   Default: ``$(PURIFY) $(CC)``.

.. envvar:: CONFIGURE_LDFLAGS

   Value of :envvar:`LDFLAGS` variable passed to the ``./configure`` script.

   Avoid assigning :envvar:`CFLAGS`, :envvar:`LDFLAGS`, etc. so users can use
   them on the command line to append to these values without stomping the
   pre-set values.

   .. versionadded:: 3.2

.. envvar:: LDFLAGS_NODIST

   :envvar:`LDFLAGS_NODIST` is used in the same manner as
   :envvar:`CFLAGS_NODIST`.  Use it when a linker flag should *not* be part of
   :envvar:`LDFLAGS` once Python is installed (:gh:`65320`).

   In particular, :envvar:`LDFLAGS` should not contain:

   * the compiler flag ``-L`` (for setting the search path for libraries).
     The ``-L`` flags are processed from left to right, and any flags in
     :envvar:`LDFLAGS` would take precedence over user- and package-supplied ``-L``
     flags.

.. envvar:: CONFIGURE_LDFLAGS_NODIST

   Value of :envvar:`LDFLAGS_NODIST` variable passed to the ``./configure``
   script.

   .. versionadded:: 3.8

.. envvar:: LDFLAGS

   Linker flags, e.g. :samp:`-L{lib_dir}` if you have libraries in a nonstandard
   directory *lib_dir*.

   Both :envvar:`CPPFLAGS` and :envvar:`LDFLAGS` need to contain the shell's
   value to be able to build extension modules using the
   directories specified in the environment variables.

.. envvar:: LIBS

   Linker flags to pass libraries to the linker when linking the Python
   executable.

   Example: ``-lrt``.

.. envvar:: LDSHARED

   Command to build a shared library.

   Default: ``@LDSHARED@ $(PY_LDFLAGS)``.

.. envvar:: BLDSHARED

   Command to build ``libpython`` shared library.

   Default: ``@BLDSHARED@ $(PY_CORE_LDFLAGS)``.

.. envvar:: PY_LDFLAGS

   Default: ``$(CONFIGURE_LDFLAGS) $(LDFLAGS)``.

.. envvar:: PY_LDFLAGS_NODIST

   Default: ``$(CONFIGURE_LDFLAGS_NODIST) $(LDFLAGS_NODIST)``.

   .. versionadded:: 3.8

.. envvar:: PY_CORE_LDFLAGS

   Linker flags used for building the interpreter object files.

   .. versionadded:: 3.8


.. rubric:: Chú thích cuối trang

.. [#] ``git clean -fdx`` là một cách thậm chí cực đoan hơn để "dọn dẹp" checkout của bạn. Nó xóa mọi tệp mà Git không nhận diện. Khi tìm lỗi bằng ``git bisect``, bạn `được khuyến nghị thực hiện việc này giữa các lần thăm dò <https://github.com/python/cpython/issues/114505#issuecomment-1907021718>`_ để đảm bảo một bản build hoàn toàn sạch. **Hãy sử dụng cẩn thận**, vì thao tác này sẽ xóa mọi tệp chưa được đưa vào Git, bao gồm cả phần công việc mới chưa commit của bạn.

.. _`C11`: https://en.cppreference.com/w/c/11
.. _`Optional C11 features`: https://en.wikipedia.org/wiki/C11_(C_standard_revision)#Optional_features
.. _`IEEE 754`: https://en.wikipedia.org/wiki/IEEE_754
.. _`floating-point Not-a-Number (NaN)`: https://en.wikipedia.org/wiki/NaN#Floating_point
.. _`libffi`: https://sourceware.org/libffi/
.. _`libmpdec`: https://www.bytereef.org/mpdecimal/doc/libmpdec/
.. _`libreadline`: https://tiswww.case.edu/php/chet/readline/rltop.html
.. _`OpenSSL`: https://openssl-library.org/
.. _`SQLite`: https://sqlite.org/
.. _`Tcl/Tk`: https://www.tcl-lang.org/
.. _`zlib`: https://www.zlib.net
.. _`zstd`: https://facebook.github.io/zstd/
.. _`devguide`: https://devguide.python.org/getting-started/setup-building/#install-dependencies
.. _`libexpat`: https://libexpat.github.io/
.. _`Autoconf`: https://gnu.org/software/autoconf
.. _`Automake`: https://www.gnu.org/software/automake
.. _`pkg-config`: https://www.freedesktop.org/wiki/Software/pkg-config/
.. _`generated files`: #generated-files
.. _`recommended between probes`: https://github.com/python/cpython/issues/114505#issuecomment-1907021718
