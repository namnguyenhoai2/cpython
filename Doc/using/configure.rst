***************
Cấu hình Python
***************

.. highlight:: sh


.. _build-requirements:

Yêu cầu build
=============

Để build CPython, bạn sẽ cần:

* Một trình biên dịch `C11 <https://en.cppreference.com/w/c/11>`_. Không bắt buộc phải có `các tính năng C11 tùy chọn <https://en.wikipedia.org/wiki/C11_(C_standard_revision)#Optional_features>`_.

* Trên Windows, cần có Microsoft Visual Studio 2017 trở lên.

* Hỗ trợ số dấu phẩy động `IEEE 754 <https://en.wikipedia.org/wiki/IEEE_754>`_ và `giá trị Not-a-Number (NaN) dấu phẩy động <https://en.wikipedia.org/wiki/NaN#Floating_point>`_.

* Hỗ trợ threads.

.. versionchanged:: 3.5
   Trên Windows, hiện yêu cầu Visual Studio 2015 trở lên.

.. versionchanged:: 3.6
   Hiện yêu cầu một số tính năng C99 được chọn, chẳng hạn như các hàm ``<stdint.h>`` và ``static inline``.

.. versionchanged:: 3.7
   Hiện yêu cầu hỗ trợ thread.

.. versionchanged:: 3.11
   Hiện yêu cầu compiler C11, hỗ trợ IEEE 754 và NaN. Trên Windows, yêu cầu Visual Studio 2017 trở lên.

Xem thêm :pep:`7` "Style Guide for C Code" và :pep:`11` "CPython platform support".


.. _optional-module-requirements:

Yêu cầu đối với các module tùy chọn
-----------------------------------

Một số :term:`module tùy chọn <optional module>` của standard library yêu cầu cài đặt các thư viện bên thứ ba để phát triển (ví dụ: phải có sẵn các tệp header).

Các yêu cầu còn thiếu được báo cáo trong đầu ra ``configure``. Các mô-đun bị thiếu do thiếu dependency được liệt kê gần cuối đầu ra ``make``, đôi khi sử dụng tên nội bộ; ví dụ: ``_ctypes`` cho mô-đun :mod:`ctypes`.

Nếu bạn phân phối một trình thông dịch CPython không có các mô-đun tùy chọn, bạn nên thông báo cho người dùng, vì họ thường mong đợi các mô-đun trong thư viện chuẩn luôn khả dụng.

Các dependency để xây dựng các mô-đun tùy chọn là:

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
     - khuyến nghị 3.3.0
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

.. [1] Nếu *libmpdec* không khả dụng, mô-đun :mod:`decimal` sẽ sử dụng một triển khai thuần Python. Xem :option:`--with-system-libmpdec` để biết chi tiết.
.. [2] Xem :option:`--with-readline` để chọn backend cho
   :mod:`readline` mô-đun.
.. [3] Mô-đun :mod:`uuid` sử dụng ``_uuid`` để tạo các UUID “an toàn”. Xem tài liệu của mô-đun để biết chi tiết.
.. [4] Mô-đun :mod:`curses` yêu cầu thư viện ``libncurses`` hoặc ``libncursesw``. Mô-đun :mod:`curses.panel` cũng yêu cầu thư viện ``libpanel`` hoặc ``libpanelw``.
.. [5] Nếu OpenSSL không khả dụng, mô-đun :mod:`hashlib` sẽ sử dụng các triển khai đi kèm của một số hàm băm. Xem :option:`--with-builtin-hashlib-hashes` để *buộc* sử dụng OpenSSL.
.. [6] OpenSSL 1.1.1 là phiên bản tối thiểu có thể dùng để build, nhưng dòng phiên bản này đã hết vòng đời và không còn nhận được các bản sửa lỗi bảo mật công khai. Hãy sử dụng bản phát hành vá mới nhất của một dòng bản phát hành LTS hiện được hỗ trợ (xem `OpenSSL Roadmap <https://openssl-library.org/roadmap/index.html>`__), hoặc gói do hệ điều hành cung cấp nếu có. Các thư viện khác cung cấp API tương thích với OpenSSL 1.1.1 trở lên có thể hoạt động, nhưng không được hỗ trợ chính thức.

Lưu ý rằng bảng này không bao gồm tất cả các module tùy chọn; cụ thể là các module dành riêng cho từng nền tảng như :mod:`winreg` không được liệt kê ở đây.

.. seealso::

   * `devguide <https://devguide.python.org/getting-started/setup-building/#install-dependencies>`_ bao gồm danh sách đầy đủ các dependency cần thiết để build tất cả các module, cùng hướng dẫn cài đặt chúng trên các nền tảng phổ biến.
   * :option:`--with-system-expat` cho phép build với thư viện `libexpat <https://libexpat.github.io/>`_ bên ngoài.
   * :ref:`configure-options-for-dependencies`

.. versionchanged:: 3.1
   Hiện yêu cầu Tcl/Tk phiên bản 8.3.1 cho :mod:`tkinter`.

.. versionchanged:: 3.5
   Hiện yêu cầu Tcl/Tk phiên bản 8.4 cho :mod:`tkinter`.

.. versionchanged:: 3.7
   Hiện yêu cầu OpenSSL 1.0.2 cho :mod:`hashlib` và :mod:`ssl`.

.. versionchanged:: 3.10
   Hiện yêu cầu OpenSSL 1.1.1 cho :mod:`hashlib` và :mod:`ssl`. Hiện yêu cầu SQLite 3.7.15 cho :mod:`sqlite3`.

.. versionchanged:: 3.11
   Hiện yêu cầu Tcl/Tk phiên bản 8.5.12 cho :mod:`tkinter`.

.. versionchanged:: 3.13
   Hiện yêu cầu SQLite 3.15.2 cho :mod:`sqlite3`.


Các tệp được tạo
================

Để giảm các dependency khi build, mã nguồn Python chứa nhiều tệp được tạo. Các lệnh để tạo lại tất cả các tệp được tạo::

    make regen-all
    make regen-stdlib-module-names
    make regen-limited-abi
    make regen-configure

Tệp ``Makefile.pre.in`` mô tả các tệp được tạo, đầu vào của chúng và các công cụ được sử dụng để tạo lại chúng. Tìm các make target ``regen-*``.

Tập lệnh configure
------------------

Lệnh ``make regen-configure`` tạo lại tệp ``aclocal.m4`` và tập lệnh ``configure`` bằng tập lệnh shell ``Tools/build/regen-configure.sh``, sử dụng một container Ubuntu để có được cùng phiên bản công cụ và tạo ra đầu ra có thể tái lập.

Container là tùy chọn, bạn có thể chạy lệnh sau trên máy cục bộ::

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

Liệt kê tất cả các tùy chọn của script :file:`configure` bằng lệnh::

    ./configure --help

Xem thêm :file:`Misc/SpecialBuilds.txt` trong bản phân phối mã nguồn Python.

Tùy chọn chung
--------------

.. option:: --enable-loadable-sqlite-extensions

   Hỗ trợ các extension có thể tải trong mô-đun extension :mod:`!_sqlite` (mặc định là không) của mô-đun :mod:`sqlite3`.

   Xem phương thức :meth:`sqlite3.Connection.enable_load_extension` của
   mô-đun :mod:`sqlite3`.

   .. versionadded:: 3.6

.. option:: --disable-ipv6

   Tắt hỗ trợ IPv6 (được bật theo mặc định nếu được hỗ trợ), xem
   mô-đun :mod:`socket`.

.. option:: --enable-big-digits=[15|30]

   Xác định kích thước tính bằng bit của các chữ số :class:`int` trong Python: 15 hoặc 30 bit.

   Theo mặc định, kích thước chữ số là 30.

   Định nghĩa ``PYLONG_BITS_IN_DIGIT`` thành ``15`` hoặc ``30``.

   Xem :data:`sys.int_info.bits_per_digit <sys.int_info>`.

.. option:: --with-suffix=SUFFIX

   Đặt hậu tố của tệp thực thi Python thành *SUFFIX*.

   Hậu tố mặc định là ``.exe`` trên Windows và macOS (tệp thực thi ``python.exe``), ``.js`` trên nút Emscripten, ``.html`` trên trình duyệt Emscripten, ``.wasm`` trên WASI và chuỗi rỗng trên các nền tảng khác (tệp thực thi ``python``).

   .. versionchanged:: 3.11
      Hậu tố mặc định trên nền tảng WASM là một trong các giá trị ``.js``, ``.html`` hoặc ``.wasm``.

.. option:: --with-tzpath=<list of absolute paths separated by pathsep>

   Chọn đường dẫn tìm kiếm múi giờ mặc định cho :const:`zoneinfo.TZPATH`. Xem :ref:`Cấu hình tại thời điểm biên dịch <zoneinfo_data_compile_time_config>` của mô-đun :mod:`zoneinfo`.

   Mặc định: ``/usr/share/zoneinfo:/usr/lib/zoneinfo:/usr/share/lib/zoneinfo:/etc/zoneinfo``.

   Xem dấu phân cách đường dẫn :data:`os.pathsep`.

   .. versionadded:: 3.9

.. option:: --without-decimal-contextvar

   Xây dựng module extension ``_decimal`` bằng context cục bộ theo thread thay vì context cục bộ theo coroutine (mặc định), xem module :mod:`decimal`.

   Xem :const:`decimal.HAVE_CONTEXTVAR` và module :mod:`contextvars`.

   .. versionadded:: 3.9

.. option:: --with-dbmliborder=<list of backend names>

   Ghi đè thứ tự kiểm tra các backend cơ sở dữ liệu cho module :mod:`dbm`

   Giá trị hợp lệ là một chuỗi được phân tách bằng dấu hai chấm (``:``) chứa tên các backend:

   * ``ndbm``;
   * ``gdbm``;
   * ``bdb``.

.. option:: --without-c-locale-coercion

   Tắt cơ chế chuyển đổi locale C sang locale dựa trên UTF-8 (được bật theo mặc định).

   Không định nghĩa macro ``PY_COERCE_C_LOCALE``.

   Xem :envvar:`PYTHONCOERCECLOCALE` và :pep:`538`.

.. option:: --with-platlibdir=DIRNAME

   Tên thư mục thư viện Python (mặc định là ``lib``).

   Fedora và SuSE sử dụng ``lib64`` trên các nền tảng 64-bit.

   Xem :data:`sys.platlibdir`.

   .. versionadded:: 3.9

.. option:: --with-wheel-pkg-dir=PATH

   Thư mục chứa các gói wheel được module :mod:`ensurepip` sử dụng (mặc định không có).

   Một số chính sách đóng gói của bản phân phối Linux khuyến nghị không đóng gói kèm các dependency. Ví dụ, Fedora cài đặt các gói wheel vào thư mục ``/usr/share/python-wheels/`` và không cài đặt
   gói :mod:`!ensurepip._bundled`.

   .. versionadded:: 3.10

.. option:: --with-pkg-config=[check|yes|no]

   Liệu configure có nên sử dụng :program:`pkg-config` để phát hiện các dependency khi build hay không.

   * ``check`` (mặc định): :program:`pkg-config` là tùy chọn
   * ``yes``: :program:`pkg-config` là bắt buộc
   * ``no``: configure không sử dụng :program:`pkg-config` ngay cả khi có mặt

   .. versionadded:: 3.11

.. option:: --enable-pystats

   Bật tính năng thu thập thống kê hiệu năng Python nội bộ.

   Theo mặc định, tính năng thu thập thống kê bị tắt. Sử dụng lệnh ``python3 -X pystats`` hoặc đặt biến môi trường ``PYTHONSTATS=1`` để bật tính năng thu thập thống kê khi Python khởi động.

   Khi Python thoát, kết xuất số liệu thống kê nếu tính năng thu thập số liệu thống kê đang được bật và chưa bị xóa.

   Tác động:

   * Thêm tùy chọn dòng lệnh :option:`-X pystats <-X>`.
   * Thêm biến môi trường :envvar:`!PYTHONSTATS`.
   * Định nghĩa macro ``Py_STATS``.
   * Thêm các hàm vào module :mod:`sys`:

     * :func:`!sys._stats_on`: Bật tính năng thu thập số liệu thống kê.
     * :func:`!sys._stats_off`: Tắt việc thu thập thống kê.
     * :func:`!sys._stats_clear`: Xóa số liệu thống kê.
     * :func:`!sys._stats_dump`: Ghi số liệu thống kê vào tệp rồi xóa số liệu thống kê.

   Số liệu thống kê sẽ được ghi vào một tệp bất kỳ (có thể là duy nhất) trong ``/tmp/py_stats/`` (Unix) hoặc ``C:\temp\py_stats\`` (Windows). Nếu thư mục đó không tồn tại, kết quả sẽ được in ra stderr.

   Dùng ``Tools/scripts/summarize_stats.py`` để đọc số liệu thống kê.

   Thống kê:

   * Opcode:

     * Chuyên biệt hóa: thành công, thất bại, trúng, trì hoãn, trượt, deopt, các lỗi;
     * Số lần thực thi;
     * Số cặp.

   * Lời gọi:

     * Lời gọi Python được inline;
     * Lời gọi PyEval;
     * Các frame được push;
     * Đã tạo đối tượng Frame;
     * Các lệnh gọi Eval: vector, generator, legacy, hàm VECTORCALL, lớp build, slot, hàm "ex", API, phương thức.

   * Đối tượng:

     * incref và decref;
     * incref và decref của interpreter;
     * cấp phát: tất cả, 512 bytes, 4 kiB, lớn;
     * giải phóng;
     * đến/từ free list;
     * dictionary được materialize/dematerialize;
     * bộ nhớ đệm kiểu;
     * các lần thử tối ưu hóa;
     * các optimization trace được tạo/thực thi;
     * các uops được thực thi.

   * Bộ thu gom rác:

     * Số lần thu gom rác;
     * Số đối tượng đã duyệt qua;
     * Số đối tượng đã được thu gom.

   .. versionadded:: 3.11

.. _free-threading-build:

.. option:: --disable-gil

   Cho phép chạy Python mà không có :term:`global interpreter lock` (GIL): :term:`free-threaded build`.

   Định nghĩa macro ``Py_GIL_DISABLED`` và thêm ``"t"`` vào
   :data:`sys.abiflags`.

   Xem :ref:`whatsnew313-free-threaded-cpython` để biết thêm chi tiết.

   .. versionadded:: 3.13

.. option:: --enable-experimental-jit=[no|yes|yes-off|interpreter]

   Cho biết cách tích hợp :ref:`trình biên dịch just-in-time thử nghiệm <whatsnew314-jit-compiler>`.

   * ``no``: Không xây dựng JIT.
   * ``yes``: Bật JIT. Để tắt JIT trong runtime, hãy đặt biến môi trường :envvar:`PYTHON_JIT=0 <PYTHON_JIT>`.
   * ``yes-off``: Xây dựng JIT nhưng tắt theo mặc định. Để bật JIT trong runtime, hãy đặt biến môi trường :envvar:`PYTHON_JIT=1 <PYTHON_JIT>`.
   * ``interpreter``: Bật "trình thông dịch JIT" (chỉ hữu ích cho những người gỡ lỗi chính JIT). Để tắt nó trong runtime, hãy đặt biến môi trường :envvar:`PYTHON_JIT=0 <PYTHON_JIT>`.

   ``--enable-experimental-jit=no`` là hành vi mặc định nếu không cung cấp tùy chọn này, còn ``--enable-experimental-jit`` là dạng viết tắt của ``--enable-experimental-jit=yes``. Xem :file:`Tools/jit/README.md` để biết thêm thông tin, bao gồm cách cài đặt các phần phụ thuộc cần thiết tại thời điểm xây dựng.

   .. note::

      Khi xây dựng CPython với JIT được bật, hãy đảm bảo hệ thống của bạn đã cài đặt Python 3.11 trở lên.

   .. versionadded:: 3.13

.. option:: PKG_CONFIG

   Đường dẫn đến tiện ích ``pkg-config``.

.. option:: PKG_CONFIG_LIBDIR
.. option:: PKG_CONFIG_PATH

   ``pkg-config`` tùy chọn.


Tùy chọn trình biên dịch C
--------------------------

.. option:: CC

   Lệnh trình biên dịch C.

.. option:: CFLAGS

   Cờ trình biên dịch C.

.. option:: CPP

   Lệnh bộ tiền xử lý C.

.. option:: CPPFLAGS

   Cờ bộ tiền xử lý C, ví dụ: :samp:`-I{include_dir}`.


Tùy chọn trình liên kết
-----------------------

.. option:: LDFLAGS

   Các cờ của linker, ví dụ :samp:`-L{library_directory}`.

.. option:: LIBS

   Các thư viện sẽ truyền cho linker, ví dụ :samp:`-l{library}`.

.. option:: MACHDEP

   Tên cho các tệp thư viện phụ thuộc vào máy.


.. _configure-options-for-dependencies:

Các tùy chọn cho các dependency bên thứ ba
------------------------------------------

.. versionadded:: 3.11

.. option:: BZIP2_CFLAGS
.. option:: BZIP2_LIBS

   Các cờ của trình biên dịch C và linker để liên kết Python với ``libbz2``, được mô-đun :mod:`bz2` sử dụng, ghi đè lên ``pkg-config``.

.. option:: CURSES_CFLAGS
.. option:: CURSES_LIBS

   Các cờ của trình biên dịch C và linker cho ``libncurses`` hoặc ``libncursesw``, được sử dụng bởi
   mô-đun :mod:`curses`, ghi đè lên ``pkg-config``.

.. option:: GDBM_CFLAGS
.. option:: GDBM_LIBS

   Cờ trình biên dịch và liên kết C cho ``gdbm``.

.. option:: LIBEDIT_CFLAGS
.. option:: LIBEDIT_LIBS

   Cờ trình biên dịch và liên kết C cho ``libedit``, được module :mod:`readline` sử dụng, ghi đè ``pkg-config``.

.. option:: LIBFFI_CFLAGS
.. option:: LIBFFI_LIBS

   Cờ trình biên dịch và liên kết C cho ``libffi``, được module :mod:`ctypes` sử dụng, ghi đè ``pkg-config``.

.. option:: LIBMPDEC_CFLAGS
.. option:: LIBMPDEC_LIBS

   Cờ trình biên dịch và liên kết C cho ``libmpdec``, được module :mod:`decimal` sử dụng, ghi đè ``pkg-config``.

   .. note::

      Các biến môi trường này không có hiệu lực trừ khi
      :option:`--with-system-libmpdec` được chỉ định.

.. option:: LIBLZMA_CFLAGS
.. option:: LIBLZMA_LIBS

   Cờ trình biên dịch và liên kết C cho ``liblzma``, được module :mod:`lzma` sử dụng, ghi đè ``pkg-config``.

.. option:: LIBREADLINE_CFLAGS
.. option:: LIBREADLINE_LIBS

   Các cờ trình biên dịch và liên kết C cho ``libreadline``, được mô-đun :mod:`readline` sử dụng, ghi đè ``pkg-config``.

.. option:: LIBSQLITE3_CFLAGS
.. option:: LIBSQLITE3_LIBS

   Các cờ trình biên dịch và liên kết C cho ``libsqlite3``, được mô-đun :mod:`sqlite3` sử dụng, ghi đè ``pkg-config``.

.. option:: LIBUUID_CFLAGS
.. option:: LIBUUID_LIBS

   Các cờ trình biên dịch và liên kết C cho ``libuuid``, được mô-đun :mod:`uuid` sử dụng, ghi đè ``pkg-config``.

.. option:: LIBZSTD_CFLAGS
.. option:: LIBZSTD_LIBS

   Các cờ trình biên dịch và liên kết C cho ``libzstd``, được mô-đun :mod:`compression.zstd` sử dụng, ghi đè ``pkg-config``.

   .. versionadded:: 3.14

.. option:: PANEL_CFLAGS
.. option:: PANEL_LIBS

   Các cờ trình biên dịch và liên kết C cho PANEL, ghi đè ``pkg-config``.

   Các cờ trình biên dịch và liên kết C cho ``libpanel`` hoặc ``libpanelw``, được sử dụng bởi
   mô-đun :mod:`curses.panel`, ghi đè ``pkg-config``.

.. option:: TCLTK_CFLAGS
.. option:: TCLTK_LIBS

   Các cờ compiler và linker C cho TCLTK, ghi đè ``pkg-config``.

.. option:: ZLIB_CFLAGS
.. option:: ZLIB_LIBS

   Các cờ compiler và linker C cho ``libzlib``, được module :mod:`gzip` sử dụng, ghi đè ``pkg-config``.


Tùy chọn WebAssembly
--------------------

.. option:: --enable-wasm-dynamic-linking

   Bật hỗ trợ dynamic linking cho WASM.

   Dynamic linking cho phép ``dlopen``. Kích thước tệp thực thi tăng do khả năng loại bỏ dead code bị hạn chế và có thêm các tính năng.

   .. versionadded:: 3.11

.. option:: --enable-wasm-pthreads

   Bật hỗ trợ pthreads cho WASM.

   .. versionadded:: 3.11


Tùy chọn cài đặt
----------------

.. option:: --prefix=PREFIX

   Cài đặt các tệp không phụ thuộc kiến trúc vào PREFIX. Trên Unix, giá trị mặc định là :file:`/usr/local`.

   Có thể lấy giá trị này trong runtime bằng :data:`sys.prefix`.

   Ví dụ, có thể sử dụng ``--prefix="$HOME/.local/"`` để cài đặt Python vào thư mục chính của nó.

.. option:: --exec-prefix=EPREFIX

   Cài đặt các tệp phụ thuộc kiến trúc vào EPREFIX, với giá trị mặc định là :option:`--prefix`.

   Có thể lấy giá trị này trong runtime bằng :data:`sys.exec_prefix`.

.. option:: --disable-test-modules

   Không xây dựng hoặc cài đặt các mô-đun kiểm thử, chẳng hạn như package :mod:`test` hoặc
   mô-đun mở rộng :mod:`!_testcapi` (được xây dựng và cài đặt theo mặc định).

   .. versionadded:: 3.10

.. option:: --with-ensurepip=[upgrade|install|no]

   Chọn lệnh :mod:`ensurepip` chạy khi cài đặt Python:

   * ``upgrade`` (mặc định): chạy lệnh ``python -m ensurepip --altinstall --upgrade``.
   * ``install``: chạy lệnh ``python -m ensurepip --altinstall``;
   * ``no``: không chạy ensurepip;

   .. versionadded:: 3.6


Các tùy chọn hiệu năng
----------------------

Bạn nên cấu hình Python bằng ``--enable-optimizations --with-lto`` (PGO + LTO) để đạt hiệu năng tốt nhất. Cũng có thể sử dụng cờ thử nghiệm ``--enable-bolt`` để cải thiện hiệu năng.

.. option:: --enable-optimizations

   Bật Profile Guided Optimization (PGO) bằng :envvar:`PROFILE_TASK` (theo mặc định là tắt).

   Trình biên dịch C Clang yêu cầu chương trình ``llvm-profdata`` cho PGO. Trên macOS, GCC cũng yêu cầu điều này: GCC thực chất chỉ là bí danh của Clang trên macOS.

   Đồng thời vô hiệu hóa semantic interposition trong libpython nếu sử dụng ``--enable-shared`` và GCC: thêm ``-fno-semantic-interposition`` vào các cờ của trình biên dịch và trình liên kết.

   .. note::

      Trong quá trình build, bạn có thể gặp cảnh báo của trình biên dịch cho biết dữ liệu profile không khả dụng đối với một số tệp nguồn. Những cảnh báo này không gây ảnh hưởng, vì chỉ một phần code được thực thi trong quá trình thu thập dữ liệu profile. Để tắt các cảnh báo này trên Clang, hãy tự suppress chúng bằng cách thêm ``-Wno-profile-instr-unprofiled`` vào :envvar:`CFLAGS`.

   .. versionadded:: 3.6

   .. versionchanged:: 3.10
      Sử dụng ``-fno-semantic-interposition`` trên GCC.

.. envvar:: PROFILE_TASK

   Biến môi trường được sử dụng trong Makefile: các đối số dòng lệnh Python cho tác vụ tạo PGO.

   Mặc định: ``-m test --pgo --timeout=$(TESTTIMEOUT)``.

   .. versionadded:: 3.8

   .. versionchanged:: 3.13
      Lỗi của tác vụ không còn bị âm thầm bỏ qua.

.. option:: --with-lto=[full|thin|no|yes]

   Bật Link Time Optimization (LTO) trong mọi bản build (mặc định bị tắt).

   Trình biên dịch C Clang yêu cầu ``llvm-ar`` cho LTO (``ar`` trên macOS), cùng với một linker hỗ trợ LTO (``ld.gold`` hoặc ``lld``).

   .. versionadded:: 3.6

   .. versionadded:: 3.11
      Để sử dụng tính năng ThinLTO, hãy dùng ``--with-lto=thin`` trên Clang.

   .. versionchanged:: 3.12
      Sử dụng ThinLTO làm chính sách tối ưu hóa mặc định trên Clang nếu trình biên dịch chấp nhận flag này.

.. option:: --enable-bolt

   Bật việc sử dụng `BOLT post-link binary optimizer <https://github.com/llvm/llvm-project/tree/main/bolt>`_ (mặc định bị tắt).

   BOLT là một phần của dự án LLVM nhưng không phải lúc nào cũng được bao gồm trong các bản phân phối binary của họ. Flag này yêu cầu ``llvm-bolt`` và ``merge-fdata`` phải khả dụng.

   BOLT vẫn là một dự án tương đối mới, vì vậy hiện tại nên xem flag này là thử nghiệm. Vì công cụ này hoạt động trên machine code, khả năng thành công phụ thuộc vào sự kết hợp giữa môi trường build, các configure args tối ưu hóa khác và kiến trúc CPU; không phải mọi tổ hợp đều được hỗ trợ. Các phiên bản BOLT trước LLVM 16 được biết là có thể khiến BOLT gặp lỗi dưới một số tình huống. Khuyến nghị mạnh mẽ sử dụng LLVM 16 hoặc mới hơn cho việc tối ưu hóa bằng BOLT.

   :envvar:`!BOLT_INSTRUMENT_FLAGS` và :envvar:`!BOLT_APPLY_FLAGS`
   Các biến :program:`configure` có thể được định nghĩa để ghi đè tập đối số mặc định cho :program:`llvm-bolt`, lần lượt dùng để instrument và áp dụng dữ liệu BOLT cho các binary.

   .. versionadded:: 3.12

.. option:: BOLT_APPLY_FLAGS

   Các đối số truyền cho ``llvm-bolt`` khi tạo một binary được tối ưu hóa bằng `BOLT optimized binary <https://github.com/facebookarchive/BOLT>`_.

   .. versionadded:: 3.12

.. option:: BOLT_INSTRUMENT_FLAGS

   Các đối số truyền cho ``llvm-bolt`` khi instrument các binary.

   .. versionadded:: 3.12

.. option:: --with-computed-gotos

   Bật computed goto trong vòng lặp đánh giá (được bật theo mặc định trên các compiler được hỗ trợ).

.. option:: --with-tail-call-interp

   Bật các interpreter sử dụng tail call trong CPython. Nếu bật, rất nên bật PGO (:option:`--enable-optimizations`). Tùy chọn này yêu cầu cụ thể một C compiler có hỗ trợ tail call phù hợp và calling convention `preserve_none <https://clang.llvm.org/docs/AttributeReference.html#preserve-none>`_. Ví dụ: Clang 19 trở lên hỗ trợ tính năng này.

   .. versionadded:: 3.14

.. option:: --without-mimalloc

   Tắt bộ cấp phát nhanh :ref:`mimalloc <mimalloc>` (được bật theo mặc định).

   Không thể sử dụng tùy chọn này cùng với :option:`--disable-gil` vì bản dựng :term:`free-threaded <free threading>` yêu cầu mimalloc.

   Xem thêm biến môi trường :envvar:`PYTHONMALLOC`.

.. option:: --without-pymalloc

   Vô hiệu hóa trình cấp phát bộ nhớ Python chuyên biệt :ref:`pymalloc <pymalloc>` (được bật theo mặc định).

   Xem thêm biến môi trường :envvar:`PYTHONMALLOC`.

.. option:: --without-doc-strings

   Không định nghĩa các chuỗi tài liệu tĩnh để giảm mức sử dụng bộ nhớ (được bật theo mặc định). Các chuỗi tài liệu được định nghĩa trong Python không bị ảnh hưởng.

   Không định nghĩa macro ``WITH_DOC_STRINGS``.

   Xem macro ``PyDoc_STRVAR()``.

.. option:: --enable-profiling

   Bật profiling mã cấp C bằng ``gprof`` (mặc định bị tắt).

.. option:: --with-strict-overflow

   Thêm ``-fstrict-overflow`` vào các cờ của trình biên dịch C (theo mặc định, chúng tôi thay vào đó thêm ``-fno-strict-overflow``).

.. option:: --without-remote-debug

   Tắt hỗ trợ remote debugging được mô tả trong :pep:`768` (mặc định được bật). Khi cung cấp cờ này, mã cho phép trình thông dịch lên lịch thực thi một tệp Python trong một tiến trình riêng như mô tả trong :pep:`768` sẽ không được biên dịch. Điều này bao gồm cả chức năng lên lịch thực thi mã và chức năng nhận mã để thực thi.

   .. c:macro:: Py_REMOTE_DEBUG

      This macro is defined by default, unless Python is configured with
      :option:`--without-remote-debug`.

      Note that even if the macro is defined, remote debugging may not be
      available (for example, on an incompatible platform).

   .. versionadded:: 3.14


.. _debug-build:

Bản dựng Python gỡ lỗi
----------------------

Bản dựng debug là Python được xây dựng với tùy chọn configure :option:`--with-pydebug`.

Các tác động của bản dựng debug:

* Hiển thị tất cả cảnh báo theo mặc định: danh sách bộ lọc cảnh báo mặc định trong module :mod:`warnings` là rỗng.
* Thêm ``d`` vào :data:`sys.abiflags`.
* Thêm hàm :func:`!sys.gettotalrefcount`.
* Thêm tùy chọn dòng lệnh :option:`-X showrefcount <-X>`.
* Thêm tùy chọn dòng lệnh :option:`-d` và biến môi trường :envvar:`PYTHONDEBUG` để gỡ lỗi trình phân tích cú pháp.
* Thêm hỗ trợ cho biến ``__lltrace__``: bật tính năng tracing cấp thấp trong vòng lặp đánh giá bytecode nếu biến này được định nghĩa.
* Cài đặt :ref:`các hook debug trên bộ cấp phát bộ nhớ <default-memory-allocators>` để phát hiện lỗi tràn bộ đệm và các lỗi bộ nhớ khác.
* Định nghĩa các macro ``Py_DEBUG`` và ``Py_REF_DEBUG``.
* Thêm các kiểm tra runtime: mã được bao quanh bởi ``#ifdef Py_DEBUG`` và ``#endif``. Bật các assertion ``assert(...)`` và ``_PyObject_ASSERT(...)``: không đặt macro ``NDEBUG`` (xem thêm tùy chọn configure :option:`--with-assertions`). Các kiểm tra runtime chính:

  * Thêm các kiểm tra tính hợp lệ cho các đối số của hàm.
  * Các đối tượng Unicode và int được tạo với vùng nhớ được điền bằng một mẫu để phát hiện việc sử dụng các đối tượng chưa được khởi tạo.
  * Đảm bảo rằng các hàm có thể xóa hoặc thay thế exception hiện tại không được gọi khi một exception đang được raise.
  * Kiểm tra để đảm bảo các hàm deallocator không thay đổi exception hiện tại.
  * Garbage collector (hàm :func:`gc.collect`) thực hiện một số kiểm tra cơ bản về tính nhất quán của các đối tượng.
  * Macro :c:macro:`!Py_SAFE_DOWNCAST()` kiểm tra tình trạng underflow và overflow của số nguyên khi chuyển từ kiểu rộng sang kiểu hẹp.

Xem thêm :ref:`Chế độ phát triển Python <devmode>` và
:option:`--with-trace-refs` tùy chọn configure.

.. versionchanged:: 3.8
   Các bản build phát hành hiện tương thích ABI với các bản build debug: việc định nghĩa macro ``Py_DEBUG`` không còn ngụ ý macro ``Py_TRACE_REFS`` (xem
   tùy chọn :option:`--with-trace-refs`). Tuy nhiên, các bản build debug vẫn cung cấp nhiều symbol hơn các bản build phát hành, và mã được build dựa trên bản build debug không nhất thiết tương thích với bản build phát hành.


Tùy chọn debug
--------------

.. option:: --with-pydebug

   :ref:`Xây dựng Python ở chế độ debug <debug-build>`: định nghĩa macro ``Py_DEBUG`` (bị tắt theo mặc định).

.. option:: --with-trace-refs

   Bật theo dõi các tham chiếu để gỡ lỗi (bị tắt theo mặc định).

   Ảnh hưởng:

   * Định nghĩa macro ``Py_TRACE_REFS``.
   * Thêm hàm :func:`sys.getobjects`.
   * Thêm biến môi trường :envvar:`PYTHONDUMPREFS`.

   Có thể sử dụng biến môi trường :envvar:`PYTHONDUMPREFS` để kết xuất các đối tượng và số lượng tham chiếu vẫn còn tồn tại khi Python thoát.

   :ref:`Các đối tượng được cấp phát tĩnh <static-types>` không được theo dõi.

   .. versionadded:: 3.8

   .. versionchanged:: 3.13
      Bản build này hiện tương thích ABI với bản build release và :ref:`bản build debug <debug-build>`.

.. option:: --with-assertions

   Biên dịch với các assertion của C được bật (mặc định là không): ``assert(...);`` và ``_PyObject_ASSERT(...);``.

   Nếu được đặt, macro ``NDEBUG`` không được định nghĩa trong biến compiler :envvar:`OPT`.

   Xem thêm tùy chọn :option:`--with-pydebug` (:ref:`debug build <debug-build>`), tùy chọn này cũng bật các assertion.

   .. versionadded:: 3.6

.. option:: --with-valgrind

   Bật hỗ trợ Valgrind (mặc định là không).

.. option:: --with-dtrace

   Bật hỗ trợ DTrace (mặc định là không).

   Xem :ref:`Instrumenting CPython with DTrace and SystemTap <instrumentation>`.

   .. versionadded:: 3.6

.. option:: --with-address-sanitizer

   Bật trình phát hiện lỗi bộ nhớ AddressSanitizer, ``asan`` (mặc định là không). Để cải thiện khả năng phát hiện của ASan, bạn cũng có thể kết hợp tùy chọn này với :option:`--without-pymalloc` để tắt trình cấp phát đối tượng nhỏ chuyên dụng, vì các vùng cấp phát của trình này không được ASan theo dõi.

   .. versionadded:: 3.6

.. option:: --with-memory-sanitizer

   Bật trình phát hiện lỗi cấp phát của MemorySanitizer, ``msan`` (mặc định là no).

   MSan báo cáo các kết quả dương tính giả đối với bộ nhớ được khởi tạo bởi những thư viện không được xây dựng với MSan, vì vậy hãy xây dựng tất cả dependency với MSan hoặc vô hiệu hóa các extension module sử dụng chúng trong :file:`Modules/Setup.local`.

   .. versionadded:: 3.6

.. option:: --with-undefined-behavior-sanitizer

   Bật trình phát hiện undefined behavior của UndefinedBehaviorSanitizer, ``ubsan`` (mặc định là no).

   .. versionadded:: 3.6

.. option:: --with-thread-sanitizer

   Bật trình phát hiện data race của ThreadSanitizer, ``tsan`` (mặc định là no).

   .. versionadded:: 3.13


Tùy chọn trình liên kết
-----------------------

.. option:: --enable-shared

   Bật việc xây dựng shared Python library: ``libpython`` (mặc định là no).

.. option:: --without-static-libpython

   Không xây dựng ``libpythonMAJOR.MINOR.a`` và không cài đặt ``python.o`` (được xây dựng và bật theo mặc định).

   .. versionadded:: 3.10


Tùy chọn thư viện
-----------------

.. option:: --with-libs='lib1 ...'

   Liên kết với các thư viện bổ sung (mặc định là không).

.. option:: --with-system-expat

   Xây dựng module :mod:`!pyexpat` bằng thư viện ``expat`` đã cài đặt (mặc định là không).

.. option:: --with-system-libmpdec

   Xây dựng module mở rộng ``_decimal`` bằng thư viện ``mpdecimal`` đã cài đặt, xem module :mod:`decimal` (mặc định là có).

   .. versionadded:: 3.3

   .. versionchanged:: 3.13
      Mặc định sử dụng thư viện ``mpdecimal`` đã cài đặt.

   .. versionchanged:: 3.15

      Bản sao thư viện đi kèm sẽ không còn được tự động chọn nếu không tìm thấy thư viện ``mpdecimal`` đã cài đặt. Chỉ trong Python 3.15, thư viện này vẫn có thể được chọn một cách rõ ràng bằng ``--with-system-libmpdec=no`` hoặc ``--without-system-libmpdec``.

   .. deprecated-removed:: 3.13 3.16
      A copy of the ``mpdecimal`` library sources will no longer be distributed
      with Python 3.16.

   .. seealso:: :option:`LIBMPDEC_CFLAGS` và :option:`LIBMPDEC_LIBS`.

.. option:: --with-readline=readline|editline

   Chỉ định thư viện backend cho mô-đun :mod:`readline`.

   * readline: Sử dụng readline làm backend.
   * editline: Sử dụng editline làm backend.

   .. versionadded:: 3.10

.. option:: --without-readline

   Không build mô-đun :mod:`readline` (mặc định được build).

   Không định nghĩa macro ``HAVE_LIBREADLINE``.

   .. versionadded:: 3.10

.. option:: --with-libm=STRING

   Ghi đè thư viện toán học ``libm`` thành *STRING* (mặc định phụ thuộc vào hệ thống).

.. option:: --with-libc=STRING

   Ghi đè thư viện C ``libc`` thành *STRING* (mặc định phụ thuộc vào hệ thống).

.. option:: --with-openssl=DIR

   Thư mục gốc của OpenSSL.

   .. versionadded:: 3.7

.. option:: --with-openssl-rpath=[no|auto|DIR]

   Đặt thư mục thư viện runtime (rpath) cho các thư viện OpenSSL:

   * ``no`` (mặc định): không đặt rpath;
   * ``auto``: tự động phát hiện rpath từ :option:`--with-openssl` và ``pkg-config``;
   * *DIR*: đặt rpath rõ ràng.

   .. versionadded:: 3.10


Tùy chọn bảo mật
----------------

.. option:: --with-hash-algorithm=[fnv|siphash13|siphash24]

   Chọn thuật toán hash để sử dụng trong ``Python/pyhash.c``:

   * ``siphash13`` (mặc định);
   * ``siphash24``;
   * ``fnv``.

   .. versionadded:: 3.4

   .. versionadded:: 3.11
      ``siphash13`` được thêm vào và là mặc định mới.

.. option:: --with-builtin-hashlib-hashes=md5,sha1,sha256,sha512,sha3,blake2

   Các mô-đun hash tích hợp sẵn:

   * ``md5``;
   * ``sha1``;
   * ``sha256``;
   * ``sha512``;
   * ``sha3`` (với shake);
   * ``blake2``.

   .. versionadded:: 3.9

.. option:: --with-ssl-default-suites=[python|openssl|STRING]

   Ghi đè chuỗi cipher suites mặc định của OpenSSL:

   * ``python``: sử dụng lựa chọn ưu tiên của Python;
   * ``openssl``: giữ nguyên các giá trị mặc định của OpenSSL;
   * *STRING*: sử dụng một chuỗi tùy chỉnh

   Xem module :mod:`ssl`.

   .. versionadded:: 3.7

   .. versionchanged:: 3.10

      Các cài đặt ``python`` và *STRING* cũng đặt TLS 1.2 làm phiên bản giao thức tối thiểu.

.. option:: --disable-safety

   Vô hiệu hóa các tùy chọn trình biên dịch được `OpenSSF khuyến nghị <recommended by OpenSSF_>`_ vì lý do bảo mật mà không làm giảm hiệu năng. Nếu tùy chọn này không được bật, CPython sẽ được build dựa trên các tùy chọn trình biên dịch an toàn mà không bị chậm lại. Khi tùy chọn này được bật, CPython sẽ không được build với các tùy chọn trình biên dịch được liệt kê bên dưới.

   Các tùy chọn trình biên dịch sau đây bị vô hiệu hóa với :option:`!--disable-safety`:

   * `-fstack-protector-strong`_: Bật các kiểm tra thời gian chạy để phát hiện tràn bộ đệm dựa trên stack.
   * `-Wtrampolines`_: Bật cảnh báo về các trampoline yêu cầu stack có quyền thực thi.

   .. _recommended by OpenSSF: https://github.com/ossf/wg-best-practices-os-developers/blob/main/docs/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++.md
   .. _-fstack-protector-strong: https://github.com/ossf/wg-best-practices-os-developers/blob/main/docs/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++.md#enable-run-time-checks-for-stack-based-buffer-overflows
   .. _-Wtrampolines: https://github.com/ossf/wg-best-practices-os-developers/blob/main/docs/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++.md#enable-warning-about-trampolines-that-require-executable-stacks

   .. versionadded:: 3.14

.. option:: --enable-slower-safety

   Bật các tùy chọn trình biên dịch được `OpenSSF khuyến nghị <recommended by OpenSSF_>`_ vì lý do bảo mật nhưng cần thêm chi phí xử lý. Nếu không bật tùy chọn này, CPython sẽ không được xây dựng bằng các tùy chọn trình biên dịch bảo mật gây ảnh hưởng đến hiệu năng. Khi bật tùy chọn này, CPython sẽ được xây dựng với các tùy chọn trình biên dịch được liệt kê bên dưới.

   Các tùy chọn trình biên dịch sau được bật cùng với :option:`!--enable-slower-safety`:

   * `-D_FORTIFY_SOURCE=3`_: Tăng cường bảo vệ mã nguồn bằng các bước kiểm tra trong thời gian biên dịch và thời gian chạy đối với việc sử dụng libc không an toàn và lỗi tràn bộ đệm.

   .. _-D_FORTIFY_SOURCE=3: https://github.com/ossf/wg-best-practices-os-developers/blob/main/docs/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++.md#fortify-sources-for-unsafe-libc-usage-and-buffer-overflows

   .. versionadded:: 3.14


Tùy chọn macOS
--------------

Xem :source:`Mac/README.rst`.

.. option:: --enable-universalsdk
.. option:: --enable-universalsdk=SDKDIR

   Tạo bản build universal binary. *SDKDIR* chỉ định SDK macOS nào sẽ được sử dụng để thực hiện quá trình build (mặc định là không).

.. option:: --enable-framework
.. option:: --enable-framework=INSTALLDIR

   Tạo Python.framework thay vì cài đặt Unix truyền thống. *INSTALLDIR* tùy chọn chỉ định đường dẫn cài đặt (mặc định là không).

.. option:: --with-universal-archs=ARCH

   Chỉ định loại universal binary cần tạo. Tùy chọn này chỉ hợp lệ khi :option:`--enable-universalsdk` được thiết lập.

   Các tùy chọn:

   * ``universal2`` (x86-64 và arm64);
   * ``32-bit`` (PPC và i386);
   * ``64-bit``  (PPC64 và x86-64);
   * ``3-way`` (i386, PPC và x86-64);
   * ``intel`` (i386 và x86-64);
   * ``intel-32`` (i386);
   * ``intel-64`` (x86-64);
   * ``all``  (PPC, i386, PPC64 và x86-64).

   Lưu ý rằng các giá trị cho mục cấu hình này *không* giống với các mã định danh được sử dụng cho universal binary wheels trên macOS. Xem Python Packaging User Guide để biết chi tiết về `các thẻ tương thích nền tảng packaging được sử dụng trên macOS <https://packaging.python.org/en/latest/specifications/platform-compatibility-tags/#macos>`_

.. option:: --with-framework-name=FRAMEWORK

   Chỉ định tên của Python framework trên macOS, chỉ hợp lệ khi
   :option:`--enable-framework` được thiết lập (mặc định: ``Python``).

.. option:: --with-app-store-compliance
.. option:: --with-app-store-compliance=PATCH-FILE

   Thư viện chuẩn Python chứa các chuỗi được biết là có thể kích hoạt lỗi của các công cụ kiểm tra tự động khi được gửi để phân phối qua Mac App Store và iOS App Store. Nếu được bật, tùy chọn này sẽ áp dụng danh sách các bản vá được biết là có thể khắc phục việc tuân thủ yêu cầu của app store. Cũng có thể chỉ định một tệp bản vá tùy chỉnh. Tùy chọn này bị tắt theo mặc định.

   .. versionadded:: 3.13

Các tùy chọn iOS
----------------

Xem :source:`iOS/README.rst`.

.. option:: --enable-framework=INSTALLDIR

   Tạo một Python.framework. Không giống macOS, đối số *INSTALLDIR* chỉ định đường dẫn cài đặt là bắt buộc.

.. option:: --with-framework-name=FRAMEWORK

   Chỉ định tên cho framework (mặc định: ``Python``).


Các tùy chọn biên dịch chéo
---------------------------

Biên dịch chéo, còn được gọi là cross building, có thể được sử dụng để xây dựng Python cho một kiến trúc CPU hoặc nền tảng khác. Biên dịch chéo yêu cầu một trình thông dịch Python cho nền tảng build. Phiên bản Python dùng để build phải khớp với phiên bản Python host được biên dịch chéo.

.. option:: --build=BUILD

   configure để build trên BUILD, thường được :program:`config.guess` đoán.

.. option:: --host=HOST

   cross-compile để xây dựng các chương trình chạy trên HOST (nền tảng đích)

.. option:: --with-build-python=path/to/python

   đường dẫn để xây dựng binary ``python`` cho cross compiling

   .. versionadded:: 3.11

.. option:: CONFIG_SITE=file

   Một biến môi trường trỏ đến một tệp chứa các tùy chọn ghi đè configure.

   Ví dụ về tệp *config.site*:

   .. code-block:: ini

      # config.site-aarch64
      ac_cv_buggy_getaddrinfo=no
      ac_cv_file__dev_ptmx=yes
      ac_cv_file__dev_ptc=no

.. option:: HOSTRUNNER

   Chương trình dùng để chạy CPython trên nền tảng host cho cross-compilation.

   .. versionadded:: 3.11


Ví dụ về cross compiling::

   CONFIG_SITE=config.site-aarch64 ../configure \
       --build=x86_64-pc-linux-gnu \
       --host=aarch64-unknown-linux-gnu \
       --with-build-python=../x86_64/python


Hệ thống build Python
=====================

Các tệp chính của hệ thống build
--------------------------------

* :file:`configure.ac` => :file:`configure`;
* :file:`Makefile.pre.in` => :file:`Makefile` (được tạo bởi :file:`configure`);
* :file:`pyconfig.h` (được tạo bởi :file:`configure`);
* :file:`Modules/Setup`: Các phần mở rộng C được build bởi Makefile bằng cách sử dụng
  :file:`Module/makesetup` shell script;

Các bước build chính
--------------------

* Các tệp C (``.c``) được build thành các tệp đối tượng (``.o``).
* Một thư viện ``libpython`` tĩnh (``.a``) được tạo từ các tệp đối tượng.
* ``python.o`` và thư viện ``libpython`` tĩnh được liên kết thành chương trình ``python`` cuối cùng.
* Các phần mở rộng C được build bởi Makefile (xem :file:`Modules/Setup`).

Các target chính của Makefile
-----------------------------

make
^^^^

Trong hầu hết trường hợp, khi build lại sau khi chỉnh sửa một phần code hoặc cập nhật checkout từ upstream, bạn chỉ cần thực thi ``make``, lệnh này (theo ngữ nghĩa của Make) sẽ build target mặc định, tức target đầu tiên được định nghĩa trong Makefile. Theo thông lệ (bao gồm cả trong dự án CPython), đây thường là target ``all``. Script ``configure`` mở rộng một biến ``autoconf``, ``@DEF_MAKE_ALL_RULE@`` để mô tả chính xác các target mà ``make all`` sẽ build. Có ba lựa chọn:

* ``profile-opt`` (được cấu hình với ``--enable-optimizations``)
* ``build_wasm`` (được chọn nếu nền tảng máy chủ khớp với ``wasm32-wasi*`` hoặc ``wasm32-emscripten``)
* ``build_all`` (được cấu hình mà không sử dụng rõ ràng một trong hai tùy chọn còn lại)

Tùy thuộc vào những thay đổi gần đây nhất đối với các tệp nguồn, Make sẽ xây dựng lại mọi target (tệp đối tượng và tệp thực thi) được xác định là đã lỗi thời, bao gồm cả việc chạy lại ``configure`` nếu cần. Tuy nhiên, các dependency giữa nguồn và target rất nhiều và được duy trì thủ công, vì vậy đôi khi Make không có đủ thông tin cần thiết để xác định chính xác tất cả target cần được xây dựng lại. Tùy thuộc vào những target không được xây dựng lại, bạn có thể gặp một số vấn đề. Nếu bạn gặp vấn đề khi build hoặc test mà không thể giải thích bằng cách nào khác, ``make clean && make`` sẽ xử lý phần lớn các vấn đề về dependency, đổi lại thời gian build sẽ lâu hơn.


make platform
^^^^^^^^^^^^^

Xây dựng chương trình ``python``, nhưng không xây dựng các mô-đun mở rộng của standard library. Thao tác này tạo một tệp có tên ``platform``, chứa một dòng duy nhất mô tả thông tin chi tiết về build platform, ví dụ: ``macosx-14.3-arm64-3.12`` hoặc ``linux-x86_64-3.13``.


make profile-opt
^^^^^^^^^^^^^^^^

Xây dựng Python bằng tối ưu hóa dựa trên hồ sơ (PGO). Bạn có thể sử dụng tùy chọn configure :option:`--enable-optimizations` để đặt đây làm target mặc định của lệnh ``make`` (``make all`` hoặc chỉ ``make``).



make clean
^^^^^^^^^^

Xóa các tệp đã được xây dựng.


make distclean
^^^^^^^^^^^^^^

Ngoài các tác vụ do ``make clean`` thực hiện, hãy xóa các tệp được tạo bởi configure script. Bạn sẽ phải chạy ``configure`` trước khi xây dựng lại. [#]_


make install
^^^^^^^^^^^^

Xây dựng target ``all`` và cài đặt Python.


make test
^^^^^^^^^

Xây dựng target ``all`` và chạy bộ kiểm thử Python với tùy chọn ``--fast-ci``, không chạy các bài kiểm thử GUI. Các biến:

* ``TESTOPTS``: các tùy chọn dòng lệnh bổ sung cho regrtest.
* ``TESTPYTHONOPTS``: các tùy chọn dòng lệnh bổ sung cho Python.
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

Tạo lại (gần như) tất cả các tệp được tạo. Các tệp này bao gồm (nhưng không chỉ giới hạn ở) các trường hợp bytecode và tệp trình tạo parser. ``make regen-stdlib-module-names`` và ``autoconf`` phải được chạy riêng cho các `tệp được tạo còn lại <#generated-files>`_.


Các phần mở rộng C
------------------

Một số phần mở rộng C được xây dựng dưới dạng các module tích hợp sẵn, chẳng hạn như module ``sys``. Chúng được xây dựng với macro ``Py_BUILD_CORE_BUILTIN`` được định nghĩa. Các module tích hợp sẵn không có thuộc tính ``__file__``:

.. code-block:: pycon

    >>> import sys
    >>> sys
    <module 'sys' (built-in)>
    >>> sys.__file__
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: module 'sys' has no attribute '__file__'

Các phần mở rộng C khác được xây dựng dưới dạng thư viện động, chẳng hạn như module ``_asyncio``. Chúng được xây dựng với macro ``Py_BUILD_CORE_MODULE`` được định nghĩa. Ví dụ trên Linux x86-64:

.. code-block:: pycon

    >>> import _asyncio
    >>> _asyncio
    <module '_asyncio' from '/usr/lib64/python3.9/lib-dynload/_asyncio.cpython-39-x86_64-linux-gnu.so'>
    >>> _asyncio.__file__
    '/usr/lib64/python3.9/lib-dynload/_asyncio.cpython-39-x86_64-linux-gnu.so'

:file:`Modules/Setup` được dùng để tạo các target Makefile nhằm build các extension C. Ở phần đầu của các tệp, các extension C được build dưới dạng module tích hợp sẵn. Các extension được định nghĩa sau marker ``*shared*`` được build dưới dạng thư viện động.

Các :c:macro:`!PyAPI_FUNC()`, :c:macro:`!PyAPI_DATA()` và
Các macro :c:macro:`PyMODINIT_FUNC` của :file:`Include/exports.h` được định nghĩa khác nhau tùy thuộc vào việc macro ``Py_BUILD_CORE_MODULE`` có được định nghĩa hay không:

* Sử dụng ``Py_EXPORTED_SYMBOL`` nếu ``Py_BUILD_CORE_MODULE`` được định nghĩa
* Nếu không, hãy sử dụng ``Py_IMPORTED_SYMBOL``.

Nếu macro ``Py_BUILD_CORE_BUILTIN`` bị dùng nhầm trong một extension C được build dưới dạng shared library, hàm :samp:`PyInit_{xxx}()` của nó sẽ không được export, gây ra lỗi :exc:`ImportError` khi import.


Cờ compiler và linker
=====================

Các tùy chọn được đặt bởi script ``./configure`` và các biến môi trường, rồi được ``Makefile`` sử dụng.

Các cờ preprocessor
-------------------

.. envvar:: CONFIGURE_CPPFLAGS

   Giá trị của biến :envvar:`CPPFLAGS` được truyền cho script ``./configure``.

   .. versionadded:: 3.6

.. envvar:: CPPFLAGS

   Các cờ preprocessor của (Objective) C/C++, ví dụ :samp:`-I{include_dir}` nếu bạn có các header trong thư mục không theo chuẩn *include_dir*.

   Cả :envvar:`CPPFLAGS` và :envvar:`LDFLAGS` đều cần chứa giá trị của shell để có thể build các extension module bằng cách sử dụng những thư mục được chỉ định trong các biến môi trường.

.. envvar:: BASECPPFLAGS

   .. versionadded:: 3.4

.. envvar:: PY_CPPFLAGS

   Các cờ preprocessor bổ sung được thêm vào khi build các tệp đối tượng của interpreter.

   Mặc định: ``$(BASECPPFLAGS) -I. -I$(srcdir)/Include $(CONFIGURE_CPPFLAGS) $(CPPFLAGS)``.

   .. versionadded:: 3.2

Các cờ compiler
---------------

.. envvar:: CC

   Lệnh compiler C.

   Ví dụ: ``gcc -pthread``.

.. envvar:: CXX

   Lệnh compiler C++.

   Ví dụ: ``g++ -pthread``.

.. envvar:: CFLAGS

   Các cờ compiler C.

.. envvar:: CFLAGS_NODIST

   :envvar:`CFLAGS_NODIST` được sử dụng để xây dựng trình thông dịch và các phần mở rộng C của stdlib. Sử dụng nó khi một cờ compiler *không nên* là một phần của
   :envvar:`CFLAGS` sau khi Python được cài đặt (:gh:`65320`).

   Cụ thể, :envvar:`CFLAGS` không được chứa:

   * cờ compiler ``-I`` (để thiết lập đường dẫn tìm kiếm cho các tệp include). Các cờ ``-I`` được xử lý từ trái sang phải, và mọi cờ trong
     :envvar:`CFLAGS` sẽ được ưu tiên hơn các cờ ``-I`` do người dùng và gói cung cấp.

   * các cờ hardening như ``-Werror`` vì các bản phân phối không thể kiểm soát liệu các gói do người dùng cài đặt có tuân thủ những tiêu chuẩn cao hơn như vậy hay không.

   .. versionadded:: 3.5

.. envvar:: COMPILEALL_OPTS

   Các tùy chọn được truyền vào dòng lệnh :mod:`compileall` khi xây dựng tệp PYC trong ``make install``. Mặc định: ``-j0``.

   .. versionadded:: 3.12

.. envvar:: EXTRA_CFLAGS

   Các cờ compiler C bổ sung.

.. envvar:: CONFIGURE_CFLAGS

   Giá trị của biến :envvar:`CFLAGS` được truyền cho script ``./configure``.

   .. versionadded:: 3.2

.. envvar:: CONFIGURE_CFLAGS_NODIST

   Giá trị của biến :envvar:`CFLAGS_NODIST` được truyền cho script ``./configure``.

   .. versionadded:: 3.5

.. envvar:: BASECFLAGS

   Cờ biên dịch cơ sở.

.. envvar:: OPT

   Cờ tối ưu hóa.

.. envvar:: CFLAGS_ALIASING

   Các cờ aliasing nghiêm ngặt hoặc không nghiêm ngặt được sử dụng để biên dịch ``Python/dtoa.c``.

   .. versionadded:: 3.7

.. envvar:: CFLAGS_CEVAL

   Các cờ được sử dụng để biên dịch ``Python/ceval.c``.

   .. versionadded:: 3.14.5

.. envvar:: CCSHARED

   Các cờ biên dịch được sử dụng để xây dựng thư viện dùng chung.

   Ví dụ: ``-fPIC`` được sử dụng trên Linux và BSD.

.. envvar:: CFLAGSFORSHARED

   Các cờ C bổ sung được thêm vào để xây dựng các tệp đối tượng của trình thông dịch.

   Mặc định: ``$(CCSHARED)`` khi sử dụng :option:`--enable-shared`, hoặc chuỗi rỗng trong các trường hợp khác.

.. envvar:: PY_CFLAGS

   Mặc định: ``$(BASECFLAGS) $(OPT) $(CONFIGURE_CFLAGS) $(CFLAGS) $(EXTRA_CFLAGS)``.

.. envvar:: PY_CFLAGS_NODIST

   Mặc định: ``$(CONFIGURE_CFLAGS_NODIST) $(CFLAGS_NODIST) -I$(srcdir)/Include/internal``.

   .. versionadded:: 3.5

.. envvar:: PY_STDMODULE_CFLAGS

   Các cờ C được sử dụng để xây dựng các tệp đối tượng của trình thông dịch.

   Mặc định: ``$(PY_CFLAGS) $(PY_CFLAGS_NODIST) $(PY_CPPFLAGS) $(CFLAGSFORSHARED)``.

   .. versionadded:: 3.7

.. envvar:: PY_CORE_CFLAGS

   Mặc định: ``$(PY_STDMODULE_CFLAGS) -DPy_BUILD_CORE``.

   .. versionadded:: 3.2

.. envvar:: PY_BUILTIN_MODULE_CFLAGS

   Các cờ trình biên dịch để xây dựng một mô-đun mở rộng thư viện chuẩn dưới dạng mô-đun tích hợp sẵn, như mô-đun :mod:`posix`.

   Mặc định: ``$(PY_STDMODULE_CFLAGS) -DPy_BUILD_CORE_BUILTIN``.

   .. versionadded:: 3.8

.. envvar:: PURIFY

   Lệnh Purify. Purify là một chương trình gỡ lỗi bộ nhớ.

   Mặc định: chuỗi rỗng (không được sử dụng).


Các cờ trình liên kết
---------------------

.. envvar:: LINKCC

   Lệnh trình liên kết được sử dụng để xây dựng các chương trình như ``python`` và ``_testembed``.

   Mặc định: ``$(PURIFY) $(CC)``.

.. envvar:: CONFIGURE_LDFLAGS

   Giá trị của biến :envvar:`LDFLAGS` được truyền cho script ``./configure``.

   Tránh gán :envvar:`CFLAGS`, :envvar:`LDFLAGS`, v.v. để người dùng có thể sử dụng chúng trên dòng lệnh nhằm nối thêm vào các giá trị này mà không ghi đè các giá trị được thiết lập sẵn.

   .. versionadded:: 3.2

.. envvar:: LDFLAGS_NODIST

   :envvar:`LDFLAGS_NODIST` được dùng theo cùng cách như
   :envvar:`CFLAGS_NODIST`. Sử dụng nó khi một linker flag *không* nên là một phần của
   :envvar:`LDFLAGS` sau khi Python được cài đặt (:gh:`65320`).

   Đặc biệt, :envvar:`LDFLAGS` không nên chứa:

   * cờ trình biên dịch ``-L`` (dùng để thiết lập đường dẫn tìm kiếm cho các thư viện). Các cờ ``-L`` được xử lý từ trái sang phải, và mọi cờ trong
     :envvar:`LDFLAGS` sẽ được ưu tiên hơn các cờ ``-L`` do người dùng và package cung cấp.

.. envvar:: CONFIGURE_LDFLAGS_NODIST

   Giá trị của biến :envvar:`LDFLAGS_NODIST` được truyền cho script ``./configure``.

   .. versionadded:: 3.8

.. envvar:: LDFLAGS

   Các cờ linker, ví dụ :samp:`-L{lib_dir}` nếu bạn có các thư viện trong thư mục không chuẩn *lib_dir*.

   Cả :envvar:`CPPFLAGS` và :envvar:`LDFLAGS` đều cần chứa giá trị của shell để có thể build các extension module bằng cách sử dụng những thư mục được chỉ định trong các biến môi trường.

.. envvar:: LIBS

   Các cờ linker dùng để truyền các thư viện cho linker khi liên kết executable Python.

   Ví dụ: ``-lrt``.

.. envvar:: LDSHARED

   Lệnh để xây dựng một thư viện dùng chung.

   Mặc định: ``@LDSHARED@ $(PY_LDFLAGS)``.

.. envvar:: BLDSHARED

   Lệnh để xây dựng thư viện dùng chung ``libpython``.

   Mặc định: ``@BLDSHARED@ $(PY_CORE_LDFLAGS)``.

.. envvar:: PY_LDFLAGS

   Mặc định: ``$(CONFIGURE_LDFLAGS) $(LDFLAGS)``.

.. envvar:: PY_LDFLAGS_NODIST

   Mặc định: ``$(CONFIGURE_LDFLAGS_NODIST) $(LDFLAGS_NODIST)``.

   .. versionadded:: 3.8

.. envvar:: PY_CORE_LDFLAGS

   Các linker flags được sử dụng để xây dựng các tệp object của interpreter.

   .. versionadded:: 3.8


.. rubric:: Chú thích cuối trang

.. [#] ``git clean -fdx`` là một cách thậm chí cực đoan hơn để "dọn sạch" checkout của bạn. Nó xóa tất cả các tệp mà Git không biết đến. Khi tìm lỗi bằng ``git bisect``, `được khuyến nghị giữa các lần thăm dò <https://github.com/python/cpython/issues/114505#issuecomment-1907021718>`_ để đảm bảo một bản build hoàn toàn sạch. **Hãy sử dụng cẩn thận**, vì thao tác này sẽ xóa tất cả các tệp chưa được commit vào Git, bao gồm cả công việc mới chưa commit của bạn.

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
.. _`BOLT post-link binary optimizer`: https://github.com/llvm/llvm-project/tree/main/bolt
.. _`BOLT optimized binary`: https://github.com/facebookarchive/BOLT
.. _`preserve_none`: https://clang.llvm.org/docs/AttributeReference.html#preserve-none
.. _`packaging platform compatibility tags used on macOS`: https://packaging.python.org/en/latest/specifications/platform-compatibility-tags/#macos
.. _`generated files`: #generated-files
.. _`recommended between probes`: https://github.com/python/cpython/issues/114505#issuecomment-1907021718
