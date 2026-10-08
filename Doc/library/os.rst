:mod:`!os` --- Các giao diện hệ điều hành khác
==============================================

.. module:: os
   :synopsis: Các giao diện hệ điều hành khác.

**Mã nguồn:** :source:`Lib/os.py`

--------------

Mô-đun này cung cấp một cách portable để sử dụng các chức năng phụ thuộc vào hệ điều hành. Nếu bạn chỉ muốn đọc hoặc ghi một tệp, hãy xem :func:`open`; nếu bạn muốn thao tác với các đường dẫn, hãy xem mô-đun :mod:`os.path`; và nếu bạn muốn đọc tất cả các dòng trong tất cả các tệp trên dòng lệnh, hãy xem mô-đun :mod:`fileinput`. Để tạo các tệp và thư mục tạm thời, hãy xem mô-đun :mod:`tempfile`; còn để xử lý tệp và thư mục ở cấp độ cao, hãy xem mô-đun :mod:`shutil`.

Lưu ý về khả năng sử dụng của các hàm này:

* Thiết kế của tất cả các mô-đun tích hợp phụ thuộc vào hệ điều hành trong Python tuân theo nguyên tắc: miễn là cùng một chức năng được cung cấp, mô-đun sẽ sử dụng cùng một giao diện; ví dụ, hàm ``os.stat(path)`` trả về thông tin stat về *path* theo cùng một định dạng (định dạng này bắt nguồn từ giao diện POSIX).

* Các phần mở rộng dành riêng cho một hệ điều hành cụ thể cũng có sẵn thông qua mô-đun :mod:`!os`, nhưng tất nhiên, việc sử dụng chúng sẽ đe dọa tính portable.

* Tất cả các hàm chấp nhận tên đường dẫn hoặc tên tệp đều chấp nhận cả đối tượng bytes và string, đồng thời trả về một đối tượng cùng kiểu nếu có trả về đường dẫn hoặc tên tệp.

* Trên VxWorks, os.popen, os.fork, os.execv và os.spawn*p* không được hỗ trợ.

* Trên các nền tảng WebAssembly, Android và iOS, phần lớn module :mod:`!os` không khả dụng hoặc hoạt động khác đi. Các API liên quan đến tiến trình (ví dụ:
  :func:`~os.fork`, :func:`~os.execve`) và tài nguyên (ví dụ: :func:`~os.nice`) không khả dụng. Những API khác như :func:`~os.getuid` và :func:`~os.getpid` được mô phỏng hoặc chỉ là stub. Các nền tảng WebAssembly cũng không hỗ trợ signal (ví dụ:
  :func:`~os.kill`, :func:`~os.wait`).


.. note::

   Tất cả các hàm trong module này đều phát sinh :exc:`OSError` (hoặc các lớp con của ngoại lệ này) khi tên tệp và đường dẫn không hợp lệ hoặc không thể truy cập, hoặc khi các đối số khác có kiểu chính xác nhưng không được hệ điều hành chấp nhận.

.. exception:: error

   Bí danh cho ngoại lệ tích hợp :exc:`OSError`.


.. data:: name

   Tên của module phụ thuộc vào hệ điều hành được import. Các tên sau hiện đã được đăng ký: ``'posix'``, ``'nt'``, ``'java'``.

   .. seealso::
      :data:`sys.platform` has a finer granularity.  :func:`os.uname` gives
      thông tin phiên bản phụ thuộc hệ thống.

      Mô-đun :mod:`platform` cung cấp các kiểm tra chi tiết về danh tính của hệ thống.


.. _os-filenames:
.. _filesystem-encoding:

Tên tệp, Đối số dòng lệnh và Biến môi trường
--------------------------------------------

Trong Python, tên tệp, đối số dòng lệnh và biến môi trường được biểu diễn bằng kiểu chuỗi. Trên một số hệ thống, cần giải mã các chuỗi này thành và từ các byte trước khi truyền chúng cho hệ điều hành. Python sử dụng :term:`filesystem encoding and error handler` để thực hiện việc chuyển đổi này (xem :func:`sys.getfilesystemencoding`).

:term:`filesystem encoding and error handler` được cấu hình khi Python khởi động bởi hàm :c:func:`PyConfig_Read`: xem
:c:member:`~PyConfig.filesystem_encoding` và
các thành viên :c:member:`~PyConfig.filesystem_errors` của :c:type:`PyConfig`.

.. versionchanged:: 3.1
   Trên một số hệ thống, việc chuyển đổi bằng mã hóa hệ thống tệp có thể không thành công. Trong trường hợp này, Python sử dụng bộ xử lý lỗi mã hóa :ref:`surrogateescape <surrogateescape>`, nghĩa là các byte không thể giải mã được sẽ được thay thế bằng một ký tự Unicode U+DC\ *xx* khi giải mã, và các ký tự này sẽ lại được chuyển thành byte ban đầu khi mã hóa.


:term:`Mã hóa hệ thống tệp <filesystem encoding and error handler>` phải đảm bảo giải mã thành công tất cả các byte nhỏ hơn 128. Nếu mã hóa hệ thống tệp không đáp ứng được đảm bảo này, các hàm API có thể đưa ra
:exc:`UnicodeError`.

Xem thêm :term:`locale encoding`.


.. _utf8-mode:

Chế độ UTF-8 của Python
-----------------------

.. versionadded:: 3.7
   Xem :pep:`540` để biết thêm chi tiết.

Chế độ UTF-8 của Python bỏ qua :term:`locale encoding` và buộc sử dụng mã hóa UTF-8:

* Sử dụng UTF-8 làm :term:`mã hóa hệ thống tệp <filesystem encoding and error handler>`.
* :func:`sys.getfilesystemencoding` trả về ``'utf-8'``.
* :func:`locale.getpreferredencoding` trả về ``'utf-8'`` (đối số *do_setlocale* không có tác dụng).
* :data:`sys.stdin`, :data:`sys.stdout` và :data:`sys.stderr` đều sử dụng UTF-8 làm mã hóa văn bản, với ``surrogateescape``
  :ref:`trình xử lý lỗi <error-handlers>` được bật cho :data:`sys.stdin` và :data:`sys.stdout` (:data:`sys.stderr` vẫn tiếp tục sử dụng ``backslashreplace`` như trong chế độ nhận biết locale mặc định)
* Trên Unix, :func:`os.device_encoding` trả về ``'utf-8'`` thay vì encoding của thiết bị.

Lưu ý rằng các thiết lập stream tiêu chuẩn trong chế độ UTF-8 có thể bị ghi đè bởi
:envvar:`PYTHONIOENCODING` (giống như trong chế độ nhận biết locale mặc định).

Do những thay đổi trong các API cấp thấp hơn đó, các API cấp cao khác cũng có hành vi mặc định khác:

* Các đối số dòng lệnh, biến môi trường và tên tệp được giải mã thành văn bản bằng bảng mã UTF-8.
* :func:`os.fsdecode` và :func:`os.fsencode` sử dụng bảng mã UTF-8.
* :func:`open`, :func:`io.open` và :func:`codecs.open` sử dụng bảng mã UTF-8 theo mặc định. Tuy nhiên, chúng vẫn sử dụng trình xử lý lỗi strict theo mặc định, vì vậy việc cố mở một tệp nhị phân ở chế độ văn bản có khả năng gây ra ngoại lệ thay vì tạo ra dữ liệu vô nghĩa.

:ref:`Python UTF-8 Mode <utf8-mode>` được bật nếu locale LC_CTYPE là ``C`` hoặc ``POSIX`` khi Python khởi động (xem hàm :c:func:`PyConfig_Read`).

Có thể bật hoặc tắt chế độ này bằng tùy chọn dòng lệnh :option:`-X utf8 <-X>` và biến môi trường :envvar:`PYTHONUTF8`.

Nếu biến môi trường :envvar:`PYTHONUTF8` hoàn toàn không được đặt, trình thông dịch sẽ mặc định sử dụng các thiết lập locale hiện tại, *trừ khi* locale hiện tại được xác định là locale dựa trên ASCII kiểu cũ (như được mô tả cho
:envvar:`PYTHONCOERCECLOCALE`), và việc ép locale bị vô hiệu hóa hoặc không thành công. Trong các locale cũ như vậy, interpreter sẽ mặc định bật chế độ UTF-8, trừ khi được chỉ dẫn rõ ràng là không làm vậy.

Chỉ có thể bật Python UTF-8 Mode khi Python khởi động. Có thể đọc giá trị của chế độ này từ :data:`sys.flags.utf8_mode <sys.flags>`.

Xem thêm :ref:`chế độ UTF-8 trên Windows <win-utf8-mode>` và :term:`filesystem encoding and error handler`.

.. seealso::

   :pep:`686`
      Python 3.15 sẽ đặt :ref:`utf8-mode` làm mặc định.


.. _os-procinfo:

Tham số tiến trình
------------------

Các hàm và mục dữ liệu này cung cấp thông tin và thực hiện thao tác trên tiến trình và người dùng hiện tại.


.. function:: ctermid()

   Trả về tên tệp tương ứng với terminal điều khiển tiến trình.

   .. availability:: Unix, not WASI.


.. data:: environ

   Một đối tượng :term:`mapping` trong đó các khóa và giá trị là những chuỗi biểu thị môi trường của tiến trình. Ví dụ: ``environ['HOME']`` là đường dẫn đến thư mục chính của bạn (trên một số nền tảng) và tương đương với ``getenv("HOME")`` trong C.

   Ánh xạ này được ghi nhận vào lần đầu tiên mô-đun :mod:`!os` được import, thường là trong quá trình Python khởi động khi xử lý :file:`site.py`. Những thay đổi đối với môi trường được thực hiện sau thời điểm này sẽ không được phản ánh trong :data:`os.environ`, ngoại trừ các thay đổi được thực hiện bằng cách sửa đổi trực tiếp :data:`os.environ`.

   Bạn có thể sử dụng ánh xạ này để sửa đổi cũng như truy vấn môi trường. :func:`putenv` sẽ được tự động gọi khi ánh xạ được sửa đổi.

   Trên Unix, các khóa và giá trị sử dụng :func:`sys.getfilesystemencoding` và trình xử lý lỗi ``'surrogateescape'``. Hãy sử dụng :data:`environb` nếu bạn muốn dùng một encoding khác.

   Trên Windows, các khóa được chuyển thành chữ hoa. Điều này cũng áp dụng khi lấy, đặt hoặc xóa một mục. Ví dụ: ``environ['monty'] = 'python'`` ánh xạ khóa ``'MONTY'`` với giá trị ``'python'``.

   .. note::

      Việc gọi trực tiếp :func:`putenv` không làm thay đổi :data:`os.environ`, vì vậy tốt hơn là bạn nên sửa đổi :data:`os.environ`.

   .. note::

      Trên một số nền tảng, bao gồm FreeBSD và macOS, việc đặt ``environ`` có thể gây rò rỉ bộ nhớ. Hãy tham khảo tài liệu hệ thống để
      :c:func:`!putenv`.

   Bạn có thể xóa các mục trong ánh xạ này để bỏ đặt các biến môi trường.
   :func:`unsetenv` sẽ được gọi tự động khi một mục bị xóa khỏi
   :data:`os.environ`, và khi một trong các phương thức :meth:`pop` hoặc :meth:`clear` được gọi.

   .. seealso::

      Hàm :func:`os.reload_environ`.

   .. versionchanged:: 3.9
      Đã được cập nhật để hỗ trợ các toán tử hợp nhất (``|``) và cập nhật (``|=``) của :pep:`584`.


.. data:: environb

   Phiên bản bytes của :data:`environ`: một đối tượng :term:`mapping` trong đó cả khóa và giá trị đều là các đối tượng :class:`bytes` đại diện cho môi trường của tiến trình.
   :data:`environ` và :data:`environb` được đồng bộ hóa (việc sửa đổi
   :data:`environb` cập nhật :data:`environ`, và ngược lại).

   :data:`environb` chỉ khả dụng nếu :const:`supports_bytes_environ` là ``True``.

   .. versionadded:: 3.2

   .. versionchanged:: 3.9
      Đã được cập nhật để hỗ trợ các toán tử hợp nhất (``|``) và cập nhật (``|=``) của :pep:`584`.


.. function:: reload_environ()

   Các ánh xạ :data:`os.environ` và :data:`os.environb` là bộ nhớ đệm của các biến môi trường tại thời điểm Python khởi động. Do đó, các thay đổi đối với môi trường của tiến trình hiện tại sẽ không được phản ánh nếu được thực hiện bên ngoài Python hoặc bởi :func:`os.putenv` hay :func:`os.unsetenv`. Sử dụng :func:`!os.reload_environ` để cập nhật :data:`os.environ` và :data:`os.environb` với mọi thay đổi như vậy đối với môi trường của tiến trình hiện tại.

   .. warning::
      Hàm này không an toàn khi sử dụng trong môi trường đa luồng. Việc gọi hàm này trong khi môi trường đang được sửa đổi ở một luồng khác sẽ tạo ra hành vi không xác định. Việc đọc từ
      :data:`os.environ` hoặc :data:`os.environb`, hay gọi :func:`os.getenv` trong khi đang tải lại, có thể trả về kết quả trống.

   .. versionadded:: 3.14


.. function:: chdir(path)
              fchdir(fd) getcwd()
   :noindex:

   Các hàm này được mô tả trong :ref:`os-file-dir`.


.. function:: fsencode(filename)

   Mã hóa :term:`giống đường dẫn <path-like object>` *tên tệp* thành
   :term:`filesystem encoding and error handler`; trả về :class:`bytes` không thay đổi.

   :func:`fsdecode` là hàm ngược.

   .. versionadded:: 3.2

   .. versionchanged:: 3.6
      Đã bổ sung hỗ trợ để chấp nhận các đối tượng triển khai giao diện :class:`os.PathLike`.


.. function:: fsdecode(filename)

   Giải mã :term:`giống đường dẫn <path-like object>` *tên tệp* từ
   :term:`filesystem encoding and error handler`; trả về :class:`str` không thay đổi.

   :func:`fsencode` là hàm đảo ngược.

   .. versionadded:: 3.2

   .. versionchanged:: 3.6
      Đã bổ sung hỗ trợ để chấp nhận các đối tượng triển khai giao diện :class:`os.PathLike`.


.. function:: fspath(path)

   Trả về biểu diễn hệ thống tệp của đường dẫn.

   Nếu :class:`str` hoặc :class:`bytes` được truyền vào, giá trị đó sẽ được trả về mà không thay đổi. Nếu không, :meth:`~os.PathLike.__fspath__` sẽ được gọi và giá trị của nó sẽ được trả về miễn là đó là một đối tượng :class:`str` hoặc :class:`bytes`. Trong mọi trường hợp khác, :exc:`TypeError` sẽ được phát sinh.

   .. versionadded:: 3.6


.. class:: PathLike

   Một :term:`abstract base class` dành cho các đối tượng biểu diễn một đường dẫn hệ thống tệp, ví dụ :class:`pathlib.PurePath`.

   .. versionadded:: 3.6

   .. method:: __fspath__()
      :abstractmethod:

      Trả về biểu diễn đường dẫn hệ thống tệp của đối tượng.

      Phương thức chỉ nên trả về một đối tượng :class:`str` hoặc :class:`bytes`, ưu tiên :class:`str`.


.. function:: getenv(key, default=None)

   Trả về giá trị của biến môi trường *key* dưới dạng chuỗi nếu biến này tồn tại, hoặc *default* nếu không tồn tại. *key* là một chuỗi. Lưu ý rằng vì :func:`getenv` sử dụng :data:`os.environ`, ánh xạ của :func:`getenv` cũng được ghi nhận tương tự tại thời điểm import, và hàm này có thể không phản ánh những thay đổi môi trường về sau.

   Trên Unix, các khóa và giá trị được giải mã bằng :func:`sys.getfilesystemencoding` và trình xử lý lỗi ``'surrogateescape'``. Sử dụng :func:`os.getenvb` nếu bạn muốn dùng một encoding khác.

   .. availability:: Unix, Windows.


.. function:: getenvb(key, default=None)

   Trả về giá trị của biến môi trường *key* dưới dạng bytes nếu biến này tồn tại, hoặc *default* nếu không tồn tại. *key* phải là bytes. Lưu ý rằng vì :func:`getenvb` sử dụng :data:`os.environb`, ánh xạ của :func:`getenvb` cũng được ghi nhận tương tự tại thời điểm import, và hàm này có thể không phản ánh những thay đổi môi trường về sau.


   :func:`getenvb` chỉ khả dụng nếu :const:`supports_bytes_environ` là ``True``.

   .. availability:: Unix.

   .. versionadded:: 3.2


.. function:: get_exec_path(env=None)

   Trả về danh sách các thư mục sẽ được tìm kiếm để tìm một executable có tên cụ thể, tương tự như shell, khi khởi chạy một process. *env*, khi được chỉ định, phải là một dictionary biến môi trường dùng để tra cứu PATH. Theo mặc định, khi *env* là ``None``, :data:`environ` được sử dụng.

   .. versionadded:: 3.2


.. function:: getegid()

   Trả về group id hiệu lực của process hiện tại. Giá trị này tương ứng với bit "set id" trên tệp đang được thực thi trong process hiện tại.

   .. availability:: Unix, not WASI.


.. function:: geteuid()

   .. index:: single: user; effective id

   Trả về user id hiệu lực của process hiện tại.

   .. availability:: Unix, not WASI.


.. function:: getgid()

   .. index:: single: process; group

   Trả về ID nhóm thực của tiến trình hiện tại.

   .. availability:: Unix.

      Hàm này là một stub trên WASI, xem :ref:`wasm-availability` để biết thêm thông tin.


.. function:: getgrouplist(user, group, /)

   Trả về danh sách các ID nhóm mà *người dùng* thuộc về. Nếu *nhóm* không có trong danh sách, nhóm này sẽ được thêm vào; thông thường, *nhóm* được chỉ định là trường ID nhóm từ bản ghi mật khẩu của *người dùng*, vì nếu không, ID nhóm đó có thể bị bỏ sót.

   .. availability:: Unix, not WASI.

   .. versionadded:: 3.3


.. function:: getgroups()

   Trả về danh sách các ID nhóm bổ sung được liên kết với tiến trình hiện tại.

   .. availability:: Unix, not WASI.

   .. note::

      Trên macOS, hành vi của :func:`getgroups` hơi khác so với các nền tảng Unix khác. Nếu trình thông dịch Python được xây dựng với deployment target là ``10.5`` hoặc cũ hơn, :func:`getgroups` trả về danh sách các ID nhóm hiệu lực được liên kết với tiến trình người dùng hiện tại; danh sách này bị giới hạn ở một số lượng mục do hệ thống xác định, thường là 16, và có thể được thay đổi bằng các lệnh gọi đến :func:`setgroups` nếu có đủ đặc quyền. Nếu được xây dựng với deployment target lớn hơn ``10.5``,
      :func:`getgroups` trả về danh sách quyền truy cập nhóm hiện tại của người dùng được liên kết với ID người dùng hiệu lực của tiến trình; danh sách quyền truy cập nhóm có thể thay đổi trong suốt vòng đời của tiến trình, không bị ảnh hưởng bởi các lệnh gọi đến :func:`setgroups`, và độ dài của danh sách không bị giới hạn ở 16. Có thể lấy giá trị deployment target, :const:`MACOSX_DEPLOYMENT_TARGET`, bằng :func:`sysconfig.get_config_var`.


.. function:: getlogin()

   Trả về tên người dùng đã đăng nhập trên terminal điều khiển của tiến trình. Trong hầu hết các trường hợp, việc sử dụng sẽ hữu ích hơn
   :func:`getpass.getuser` vì phần sau kiểm tra các biến môi trường
   :envvar:`LOGNAME` hoặc :envvar:`USERNAME` để xác định người dùng là ai, và chuyển sang ``pwd.getpwuid(os.getuid())[0]`` để lấy tên đăng nhập của người dùng thực hiện tại.

   .. availability:: Unix, Windows, not WASI.


.. function:: getpgid(pid)

   Trả về id nhóm tiến trình của tiến trình có id tiến trình là *pid*. Nếu *pid* bằng 0, id nhóm tiến trình của tiến trình hiện tại sẽ được trả về.

   .. availability:: Unix, not WASI.

.. function:: getpgrp()

   .. index:: single: process; group

   Trả về id của nhóm tiến trình hiện tại.

   .. availability:: Unix, not WASI.


.. function:: getpid()

   .. index:: single: process; id

   Trả về id tiến trình hiện tại.

   Hàm này là một stub trên WASI, xem :ref:`wasm-availability` để biết thêm thông tin.

.. function:: getppid()

   .. index:: single: process; id of parent

   Trả về id tiến trình của tiến trình cha. Khi tiến trình cha đã thoát, trên Unix, id được trả về là id của tiến trình init (1); trên Windows, id đó vẫn giữ nguyên và có thể đã được một tiến trình khác sử dụng lại.

   .. availability:: Unix, Windows, not WASI.

   .. versionchanged:: 3.2
      Đã bổ sung hỗ trợ cho Windows.


.. function:: getpriority(which, who)

   .. index:: single: process; scheduling priority

   Lấy mức độ ưu tiên lập lịch của chương trình. Giá trị *which* là một trong các giá trị
   :const:`PRIO_PROCESS`, :const:`PRIO_PGRP` hoặc :const:`PRIO_USER`, và *who* được diễn giải tương ứng với *which* (một mã định danh tiến trình cho
   :const:`PRIO_PROCESS`, mã định danh nhóm tiến trình cho :const:`PRIO_PGRP`, và mã định danh người dùng cho :const:`PRIO_USER`). Giá trị bằng 0 của *who* lần lượt biểu thị tiến trình đang gọi, nhóm tiến trình của tiến trình đang gọi hoặc mã định danh người dùng thực của tiến trình đang gọi.

   .. availability:: Unix, not WASI.

   .. versionadded:: 3.3


.. data:: PRIO_PROCESS
          PRIO_PGRP PRIO_USER

   Các tham số cho các hàm :func:`getpriority` và :func:`setpriority`.

   .. availability:: Unix, not WASI.

   .. versionadded:: 3.3


.. data:: PRIO_DARWIN_THREAD
          PRIO_DARWIN_PROCESS PRIO_DARWIN_BG PRIO_DARWIN_NONUI

   Các tham số cho các hàm :func:`getpriority` và :func:`setpriority`.

   .. availability:: macOS

   .. versionadded:: 3.12

.. function:: getresuid()

   Trả về một tuple (ruid, euid, suid) biểu thị các user id thực, hiệu lực và đã lưu của process hiện tại.

   .. availability:: Unix, not WASI, not macOS, not iOS.

   .. versionadded:: 3.2


.. function:: getresgid()

   Trả về một tuple (rgid, egid, sgid) biểu thị các group id thực, hiệu lực và đã lưu của process hiện tại.

   .. availability:: Unix, not WASI, not macOS, not iOS.

   .. versionadded:: 3.2


.. function:: getuid()

   .. index:: single: user; id

   Trả về real user id của process hiện tại.

   .. availability:: Unix.

      Hàm này là một stub trên WASI, xem :ref:`wasm-availability` để biết thêm thông tin.


.. function:: initgroups(username, gid, /)

   Gọi system ``initgroups()`` để khởi tạo danh sách group access bằng tất cả các group mà username được chỉ định là thành viên, cùng với group id được chỉ định.

   .. availability:: Unix, not WASI, not Android.

   .. versionadded:: 3.2


.. function:: putenv(key, value, /)

   .. index:: single: environment variables; setting

   Đặt biến môi trường có tên *key* thành chuỗi *value*. Những thay đổi như vậy đối với môi trường sẽ ảnh hưởng đến các subprocess được khởi chạy bằng :func:`os.system`,
   :func:`popen` hoặc :func:`fork` và :func:`execv`.

   Việc gán giá trị cho các mục trong :data:`os.environ` sẽ tự động được chuyển thành các lời gọi tương ứng đến :func:`putenv`; tuy nhiên, các lời gọi đến :func:`putenv` không cập nhật :data:`os.environ`, vì vậy thực tế nên gán giá trị cho các mục của :data:`os.environ`. Điều này cũng áp dụng cho :func:`getenv` và :func:`getenvb`, lần lượt sử dụng :data:`os.environ` và :data:`os.environb` trong phần triển khai của chúng.

   Xem thêm hàm :func:`os.reload_environ`.

   .. note::

      Trên một số nền tảng, bao gồm FreeBSD và macOS, việc thiết lập ``environ`` có thể gây rò rỉ bộ nhớ. Tham khảo tài liệu hệ thống về :c:func:`!putenv`.

   .. audit-event:: os.putenv key,value os.putenv

   .. versionchanged:: 3.9
      Hàm này hiện luôn khả dụng.


.. function:: setegid(egid, /)

   Đặt group id hiệu dụng của process hiện tại.

   .. availability:: Unix, not WASI, not Android.


.. function:: seteuid(euid, /)

   Đặt user id hiệu dụng của process hiện tại.

   .. availability:: Unix, not WASI, not Android.


.. function:: setgid(gid, /)

   Đặt group id của tiến trình hiện tại.

   .. availability:: Unix, not WASI, not Android.


.. function:: setgroups(groups, /)

   Đặt danh sách các group id bổ sung được liên kết với tiến trình hiện tại thành *groups*. *groups* phải là một sequence, và mỗi phần tử phải là một số nguyên xác định một group. Thao tác này thường chỉ khả dụng với superuser.

   .. availability:: Unix, not WASI.

   .. note:: Trên macOS, độ dài của *groups* có thể không vượt quá số lượng group id hiệu dụng tối đa do hệ thống xác định, thường là 16. Xem tài liệu về :func:`getgroups` để biết các trường hợp mà nó có thể không trả về cùng danh sách group được thiết lập bằng cách gọi setgroups().

.. function:: setns(fd, nstype=0)

   Liên kết lại thread hiện tại với một Linux namespace. Xem các trang man :manpage:`setns(2)` và :manpage:`namespaces(7)` để biết thêm chi tiết.

   Nếu *fd* tham chiếu đến một :file:`/proc/{pid}/ns/` link, ``setns()`` sẽ liên kết lại thread gọi với namespace được liên kết với link đó, và *nstype* có thể được đặt thành một trong các
   hằng số :ref:`CLONE_NEW* constants <os-unshare-clone-flags>` để áp đặt các ràng buộc lên thao tác (``0`` nghĩa là không có ràng buộc nào).

   Kể từ Linux 5.8, *fd* có thể tham chiếu đến một PID file descriptor nhận được từ
   :func:`~os.pidfd_open`. Trong trường hợp này, ``setns()`` liên kết lại thread đang gọi với một hoặc nhiều namespace giống với thread được tham chiếu bởi *fd*. Điều này phụ thuộc vào mọi ràng buộc do *nstype* áp đặt; đây là một bit mask kết hợp một hoặc nhiều
   :ref:`CLONE_NEW* constants <os-unshare-clone-flags>`, chẳng hạn như ``setns(fd, os.CLONE_NEWUTS | os.CLONE_NEWPID)``. Các membership của caller trong những namespace không được chỉ định sẽ không thay đổi.

   *fd* có thể là bất kỳ object nào có phương thức :meth:`~io.IOBase.fileno`, hoặc một raw file descriptor.

   Ví dụ này liên kết lại thread với network namespace của process ``init``::

      fd = os.open("/proc/1/ns/net", os.O_RDONLY)
      os.setns(fd, os.CLONE_NEWNET)
      os.close(fd)

   .. availability:: Linux >= 3.0 with glibc >= 2.14.

   .. versionadded:: 3.12

   .. seealso::

      Hàm :func:`~os.unshare`.

.. function:: setpgrp()

   Gọi system call :c:func:`!setpgrp` hoặc ``setpgrp(0, 0)`` tùy thuộc vào phiên bản nào được triển khai (nếu có). Xem hướng dẫn Unix để biết ngữ nghĩa.

   .. availability:: Unix, not WASI.


.. function:: setpgid(pid, pgrp, /)

   Gọi system call :c:func:`!setpgid` để đặt process group ID của process có ID *pid* thành process group có ID *pgrp*. Xem hướng dẫn Unix để biết ngữ nghĩa.

   .. availability:: Unix, not WASI.


.. function:: setpriority(which, who, priority)

   .. index:: single: process; scheduling priority

   Đặt mức độ ưu tiên lập lịch của chương trình. Giá trị *which* là một trong các giá trị sau
   :const:`PRIO_PROCESS`, :const:`PRIO_PGRP` hoặc :const:`PRIO_USER`, và *who* được diễn giải tương ứng với *which* (một mã định danh tiến trình cho
   :const:`PRIO_PROCESS`, mã định danh nhóm tiến trình cho :const:`PRIO_PGRP`, và mã định danh người dùng cho :const:`PRIO_USER`). Giá trị bằng không của *who* lần lượt biểu thị tiến trình đang gọi, nhóm tiến trình của tiến trình đang gọi hoặc mã định danh người dùng thực của tiến trình đang gọi. *priority* là một giá trị trong khoảng từ -20 đến 19. Mức độ ưu tiên mặc định là 0; mức độ ưu tiên thấp hơn khiến việc lập lịch được ưu tiên hơn.

   .. availability:: Unix, not WASI.

   .. versionadded:: 3.3


.. function:: setregid(rgid, egid, /)

   Đặt mã định danh nhóm thực và hiệu dụng của tiến trình hiện tại.

   .. availability:: Unix, not WASI, not Android.


.. function:: setresgid(rgid, egid, sgid, /)

   Đặt mã định danh nhóm thực, hiệu dụng và đã lưu của tiến trình hiện tại.

   .. availability:: Unix, not WASI, not Android, not macOS, not iOS.

   .. versionadded:: 3.2


.. function:: setresuid(ruid, euid, suid, /)

   Đặt mã định danh người dùng thực, hiệu dụng và đã lưu của tiến trình hiện tại.

   .. availability:: Unix, not WASI, not Android, not macOS, not iOS.

   .. versionadded:: 3.2


.. function:: setreuid(ruid, euid, /)

   Đặt mã định danh người dùng thực và hiệu dụng của tiến trình hiện tại.

   .. availability:: Unix, not WASI, not Android.


.. function:: getsid(pid, /)

   Gọi system call :c:func:`!getsid`. Xem hướng dẫn sử dụng Unix để biết ngữ nghĩa.

   .. availability:: Unix, not WASI.


.. function:: setsid()

   Gọi system call :c:func:`!setsid`. Xem hướng dẫn sử dụng Unix để biết ngữ nghĩa.

   .. availability:: Unix, not WASI.


.. function:: setuid(uid, /)

   .. index:: single: user; id, setting

   Đặt user id của process hiện tại.

   .. availability:: Unix, not WASI, not Android.


.. placed in this section since it relates to errno.... a little weak
.. function:: strerror(code, /)

   Trả về thông báo lỗi tương ứng với mã lỗi trong *code*. Trên các nền tảng mà :c:func:`!strerror` trả về ``NULL`` khi nhận một số lỗi không xác định, :exc:`ValueError` sẽ được raised.


.. data:: supports_bytes_environ

   ``True`` nếu kiểu OS gốc của environment là bytes (ví dụ: ``False`` trên Windows).

   .. versionadded:: 3.2


.. function:: umask(mask, /)

   Đặt umask dạng số hiện tại và trả về umask trước đó.

   Hàm này là một stub trên WASI, xem :ref:`wasm-availability` để biết thêm thông tin.


.. function:: uname()

   .. index::
      single: gethostname() (in module socket)
      single: gethostbyaddr() (in module socket)

   Trả về thông tin xác định hệ điều hành hiện tại. Giá trị trả về là một :class:`uname_result`.

   Trên macOS, iOS và Android, giá trị này trả về tên và bản phát hành của *kernel* (tức là ``'Darwin'`` trên macOS và iOS; ``'Linux'`` trên Android). Có thể sử dụng :func:`platform.uname` để lấy tên và bản phát hành hệ điều hành hiển thị cho người dùng trên iOS và Android.

   .. seealso::
      :data:`sys.platform` which has finer granularity.

      Mô-đun :mod:`platform` cung cấp các kiểm tra chi tiết về danh tính của hệ thống.

   .. availability:: Unix.

   .. versionchanged:: 3.3
      Kiểu trả về được thay đổi từ tuple thành một đối tượng tương tự tuple với các thuộc tính được đặt tên.


.. class:: uname_result

   Tên và thông tin về hệ thống được :func:`os.uname` trả về. Các thuộc tính này tương ứng với những thành phần được mô tả trong :manpage:`uname(2)`.

   Để đảm bảo khả năng tương thích ngược, đối tượng này cũng có thể được lặp, hoạt động như một tuple gồm năm phần tử chứa :attr:`~uname_result.sysname`,
   :attr:`~uname_result.nodename`, :attr:`~uname_result.release`,
   :attr:`~uname_result.version` và :attr:`~uname_result.machine` theo thứ tự đó.

   .. attribute:: sysname

      Tên hệ điều hành.

   .. attribute:: nodename

      Tên của máy trên mạng. Một số hệ thống cắt ngắn
      :attr:`~uname_result.nodename` còn 8 ký tự hoặc thành phần đứng đầu; cách tốt hơn để lấy hostname là :func:`socket.gethostname` hoặc thậm chí ``socket.gethostbyaddr(socket.gethostname())``.

   .. attribute:: release

      Bản phát hành của hệ điều hành.

   .. attribute:: version

      Phiên bản hệ điều hành.

   .. attribute:: machine

      Mã định danh phần cứng.


.. function:: unsetenv(key, /)

   .. index:: single: environment variables; deleting

   Bỏ đặt (xóa) biến môi trường có tên *key*. Những thay đổi như vậy đối với môi trường sẽ ảnh hưởng đến các subprocess được khởi chạy bằng :func:`os.system`, :func:`popen` hoặc
   :func:`fork` và :func:`execv`.

   Việc xóa các mục trong :data:`os.environ` được tự động chuyển thành một lệnh gọi tương ứng đến :func:`unsetenv`; tuy nhiên, các lệnh gọi đến :func:`unsetenv` không cập nhật :data:`os.environ`, vì vậy thực tế tốt hơn là xóa các mục của
   :data:`os.environ`.

   Xem thêm hàm :func:`os.reload_environ`.

   .. audit-event:: os.unsetenv key os.unsetenv

   .. versionchanged:: 3.9
      Hàm này hiện luôn khả dụng và cũng khả dụng trên Windows.


.. function:: unshare(flags)

   Tách liên kết các phần của ngữ cảnh thực thi quy trình và chuyển chúng vào một namespace mới được tạo. Xem trang hướng dẫn :manpage:`unshare(2)` để biết thêm chi tiết. Đối số *flags* là một bit mask, kết hợp từ không hoặc một số giá trị sau
   :ref:`CLONE_* hằng số <os-unshare-clone-flags>`, chỉ định những phần nào của ngữ cảnh thực thi cần được hủy chia sẻ khỏi các liên kết hiện có và chuyển vào một namespace mới. Nếu đối số *flags* là ``0``, không có thay đổi nào được thực hiện đối với ngữ cảnh thực thi của quy trình gọi.

   .. availability:: Linux >= 2.6.16.

   .. versionadded:: 3.12

   .. seealso::

      Hàm :func:`~os.setns`.

.. _os-unshare-clone-flags:

Các cờ truyền cho hàm :func:`unshare`, nếu phần triển khai hỗ trợ chúng. Xem :manpage:`unshare(2)` trong sổ tay Linux để biết tác dụng và khả năng hỗ trợ chính xác của chúng.

.. data:: CLONE_FILES
          CLONE_FS CLONE_NEWCGROUP CLONE_NEWIPC CLONE_NEWNET CLONE_NEWNS CLONE_NEWPID CLONE_NEWTIME CLONE_NEWUSER CLONE_NEWUTS CLONE_SIGHAND CLONE_SYSVSEM CLONE_THREAD CLONE_VM


.. _os-newstreams:

Tạo đối tượng tệp
-----------------

Các hàm này tạo các :term:`đối tượng tệp mới <file object>`.  (Xem thêm
:func:`~os.open` để mở các bộ mô tả tệp.)


.. function:: fdopen(fd, *args, **kwargs)

   Trả về một đối tượng tệp đang mở được kết nối với bộ mô tả tệp *fd*.  Đây là bí danh của hàm dựng sẵn :func:`open` và chấp nhận các đối số tương tự. Điểm khác biệt duy nhất là đối số đầu tiên của :func:`fdopen` luôn phải là một số nguyên.


.. _os-fd-ops:

Các thao tác với bộ mô tả tệp
-----------------------------

Các hàm này hoạt động trên các luồng I/O được tham chiếu bằng bộ mô tả tệp.

Bộ mô tả tệp là các số nguyên nhỏ tương ứng với một tệp đã được tiến trình hiện tại mở. Ví dụ, đầu vào tiêu chuẩn thường là bộ mô tả tệp 0, đầu ra tiêu chuẩn là 1 và lỗi tiêu chuẩn là 2. Các tệp tiếp theo được tiến trình mở sẽ lần lượt được gán các số 3, 4, 5, v.v. Tên "bộ mô tả tệp" hơi gây hiểu nhầm; trên các nền tảng Unix, socket và pipe cũng được tham chiếu bằng bộ mô tả tệp.

Có thể sử dụng phương thức :meth:`~io.IOBase.fileno` để lấy bộ mô tả tệp liên kết với một :term:`file object` khi cần. Lưu ý rằng việc sử dụng trực tiếp bộ mô tả tệp sẽ bỏ qua các phương thức của đối tượng tệp, đồng thời bỏ qua những khía cạnh như việc đệm dữ liệu nội bộ.


.. function:: close(fd)

   Đóng bộ mô tả tệp *fd*.

   .. note::

      Hàm này dành cho I/O cấp thấp và phải được áp dụng cho một bộ mô tả tệp do :func:`os.open` hoặc :func:`pipe` trả về. Để đóng một "đối tượng tệp" được trả về bởi hàm tích hợp sẵn :func:`open` hoặc bởi :func:`popen` hoặc
      :func:`fdopen`, hãy sử dụng phương thức :meth:`~io.IOBase.close` của nó.


.. function:: closerange(fd_low, fd_high, /)

   Đóng tất cả các bộ mô tả tệp từ *fd_low* (bao gồm) đến *fd_high* (không bao gồm), bỏ qua lỗi. Tương đương với (nhưng nhanh hơn nhiều so với)::

      for fd in range(fd_low, fd_high):
          try:
              os.close(fd)
          except OSError:
              pass


.. function:: copy_file_range(src, dst, count, offset_src=None, offset_dst=None)

   Sao chép *count* byte từ file descriptor *src*, bắt đầu từ offset *offset_src*, sang file descriptor *dst*, bắt đầu từ offset *offset_dst*. Nếu *offset_src* là ``None``, thì *src* được đọc từ vị trí hiện tại; tương tự đối với *offset_dst*.

   Trong các phiên bản Linux cũ hơn 5.3, các tệp được *src* và *dst* trỏ tới phải nằm trên cùng một filesystem; nếu không, một :exc:`OSError` sẽ được phát sinh với :attr:`~OSError.errno` được đặt thành :const:`errno.EXDEV`.

   Quá trình sao chép này được thực hiện mà không phát sinh chi phí bổ sung do chuyển dữ liệu từ kernel sang user space rồi trở lại kernel. Ngoài ra, một số filesystem có thể triển khai các tối ưu hóa bổ sung, chẳng hạn như sử dụng reflink (tức là hai hoặc nhiều inode chia sẻ các con trỏ tới cùng một bản sao của các block trên đĩa theo cơ chế copy-on-write; các filesystem được hỗ trợ bao gồm btrfs và XFS) và sao chép phía máy chủ (trong trường hợp NFS).

   Hàm này sao chép các byte giữa hai file descriptor. Các tùy chọn văn bản, chẳng hạn như encoding và ký tự kết thúc dòng, sẽ bị bỏ qua.

   Giá trị trả về là số byte đã được sao chép. Giá trị này có thể nhỏ hơn số byte được yêu cầu.

   .. note::

      Trên Linux, không nên sử dụng :func:`os.copy_file_range` để sao chép một phạm vi của pseudo file từ filesystem đặc biệt như procfs và sysfs. Hàm này sẽ luôn sao chép 0 byte và trả về 0 như thể tệp trống, do một lỗi đã biết trong Linux kernel.

   .. availability:: Linux >= 4.5 with glibc >= 2.27.

   .. versionadded:: 3.8


.. function:: device_encoding(fd)

   Trả về một chuỗi mô tả encoding của thiết bị được liên kết với *fd* nếu thiết bị đó được kết nối với terminal; nếu không, trả về :const:`None`.

   Trên Unix, nếu :ref:`Python UTF-8 Mode <utf8-mode>` được bật, hãy trả về ``'UTF-8'`` thay vì encoding của thiết bị.

   .. versionchanged:: 3.10
      Trên Unix, hàm này hiện triển khai Python UTF-8 Mode.


.. function:: dup(fd, /)

   Trả về một bản sao của file descriptor *fd*. File descriptor mới là
   :ref:`không kế thừa <fd_inheritance>`.

   Trên Windows, khi sao chép một stream chuẩn (0: stdin, 1: stdout, 2: stderr), file descriptor mới là :ref:`có thể kế thừa <fd_inheritance>`.

   .. availability:: not WASI.

   .. versionchanged:: 3.4
      File descriptor mới hiện không thể kế thừa.


.. function:: dup2(fd, fd2, inheritable=True)

   Sao chép file descriptor *fd* vào *fd2*, trước tiên đóng file descriptor sau nếu cần. Trả về *fd2*. Theo mặc định, file descriptor mới :ref:`có thể kế thừa <fd_inheritance>` hoặc không thể kế thừa nếu *có thể kế thừa* là ``False``.

   .. availability:: not WASI.

   .. versionchanged:: 3.4
      Thêm tham số *inheritable* tùy chọn.

   .. versionchanged:: 3.7
      Trả về *fd2* khi thành công. Trước đây, ``None`` luôn được trả về.


.. function:: fchmod(fd, mode)

   Thay đổi mode của tệp được chỉ định bởi *fd* thành *mode* dạng số. Xem tài liệu về :func:`chmod` để biết các giá trị có thể có của *mode*. Kể từ Python 3.3, thao tác này tương đương với ``os.chmod(fd, mode)``.

   .. audit-event:: os.chmod path,mode,dir_fd os.fchmod

   .. availability:: Unix, Windows.

      Hàm này bị giới hạn trên WASI; xem :ref:`wasm-availability` để biết thêm thông tin.

   .. versionchanged:: 3.13
      Đã thêm hỗ trợ trên Windows.


.. function:: fchown(fd, uid, gid)

   Thay đổi ID chủ sở hữu và nhóm của tệp được chỉ định bởi *fd* thành *uid* và *gid* dạng số. Để giữ nguyên một trong các ID, hãy đặt ID đó thành -1. Xem
   :func:`chown`. Kể từ Python 3.3, thao tác này tương đương với ``os.chown(fd, uid, gid)``.

   .. audit-event:: os.chown path,uid,gid,dir_fd os.fchown

   .. availability:: Unix.

      Hàm này bị giới hạn trên WASI; xem :ref:`wasm-availability` để biết thêm thông tin.


.. function:: fdatasync(fd)

   Buộc ghi tệp có file descriptor *fd* xuống đĩa. Không buộc cập nhật siêu dữ liệu.

   .. availability:: Unix, not macOS, not iOS.


.. function:: fpathconf(fd, name, /)

   Trả về thông tin cấu hình hệ thống liên quan đến một tệp đang mở. *name* chỉ định giá trị cấu hình cần truy xuất; đây có thể là một chuỗi chứa tên của một giá trị hệ thống đã được định nghĩa; các tên này được quy định trong một số tiêu chuẩn (POSIX.1, Unix 95, Unix 98 và các tiêu chuẩn khác). Một số nền tảng cũng định nghĩa các tên bổ sung. Các tên mà hệ điều hành máy chủ nhận biết được cung cấp trong dictionary ``pathconf_names``. Đối với các biến cấu hình không có trong ánh xạ đó, cũng chấp nhận truyền một số nguyên cho *name*.

   Nếu *name* là một chuỗi nhưng không được nhận biết, :exc:`ValueError` sẽ được phát sinh. Nếu một giá trị cụ thể của *name* không được hệ thống máy chủ hỗ trợ, ngay cả khi giá trị đó có trong ``pathconf_names``, một :exc:`OSError` sẽ được phát sinh với
   :const:`errno.EINVAL` cho số hiệu lỗi.

   Kể từ Python 3.3, thao tác này tương đương với ``os.pathconf(fd, name)``.

   .. availability:: Unix.


.. function:: fstat(fd)

   Lấy trạng thái của file descriptor *fd*. Trả về một đối tượng :class:`stat_result`.

   Kể từ Python 3.3, điều này tương đương với ``os.stat(fd)``.

   .. seealso::

      Hàm :func:`.stat`.


.. function:: fstatvfs(fd, /)

   Trả về thông tin về hệ thống tệp chứa tệp được liên kết với file descriptor *fd* trong một :class:`statvfs_result`, chẳng hạn như :func:`statvfs`. Kể từ Python 3.3, điều này tương đương với ``os.statvfs(fd)``.

   .. availability:: Unix.


.. function:: fsync(fd)

   Buộc ghi tệp có file descriptor *fd* xuống đĩa. Trên Unix, thao tác này gọi hàm gốc :c:func:`!fsync`; trên Windows, gọi hàm MS :c:func:`!_commit`.

   Nếu bạn bắt đầu với một :term:`file object` *f* Python được đệm, trước tiên hãy thực hiện ``f.flush()``, sau đó thực hiện ``os.fsync(f.fileno())``, để đảm bảo tất cả các bộ đệm nội bộ liên kết với *f* đều được ghi xuống đĩa.

   .. availability:: Unix, Windows.


.. function:: ftruncate(fd, length, /)

   Cắt ngắn tệp tương ứng với file descriptor *fd*, sao cho kích thước của tệp không vượt quá *length* byte. Kể từ Python 3.3, thao tác này tương đương với ``os.truncate(fd, length)``.

   .. audit-event:: os.truncate fd,length os.ftruncate

   .. availability:: Unix, Windows.

   .. versionchanged:: 3.5
      Đã thêm hỗ trợ cho Windows


.. function:: get_blocking(fd, /)

   Lấy chế độ blocking của file descriptor: ``False`` nếu cờ này được thiết lập,
   :data:`O_NONBLOCK` cờ được thiết lập, ``True`` nếu cờ bị xóa.

   Xem thêm :func:`set_blocking` và :meth:`socket.socket.setblocking`.

   .. availability:: Unix, Windows.

      Hàm này bị giới hạn trên WASI; xem :ref:`wasm-availability` để biết thêm thông tin.

      Trên Windows, hàm này chỉ áp dụng cho pipes.

   .. versionadded:: 3.5

   .. versionchanged:: 3.12
      Đã thêm hỗ trợ pipes trên Windows.


.. function:: grantpt(fd, /)

   Cấp quyền truy cập vào thiết bị pseudo-terminal slave liên kết với thiết bị pseudo-terminal master mà file descriptor *fd* tham chiếu đến. File descriptor *fd* không bị đóng khi xảy ra lỗi.

   Gọi hàm của thư viện chuẩn C :c:func:`grantpt`.

   .. availability:: Unix, not WASI.

   .. versionadded:: 3.13


.. function:: isatty(fd, /)

   Trả về ``True`` nếu file descriptor *fd* đang mở và được kết nối với thiết bị tty (hoặc tương tự tty), nếu không thì trả về ``False``.


.. function:: lockf(fd, cmd, len, /)

   Áp dụng, kiểm tra hoặc gỡ bỏ khóa POSIX trên một file descriptor đang mở. *fd* là một file descriptor đang mở. *cmd* chỉ định lệnh cần sử dụng - một trong các lệnh :data:`F_LOCK`, :data:`F_TLOCK`,
   :data:`F_ULOCK` hoặc :data:`F_TEST`. *len* chỉ định phần của tệp cần khóa.

   .. audit-event:: os.lockf fd,cmd,len os.lockf

   .. availability:: Unix.

   .. versionadded:: 3.3


.. data:: F_LOCK
          F_TLOCK F_ULOCK F_TEST

   Các cờ chỉ định hành động mà :func:`lockf` sẽ thực hiện.

   .. availability:: Unix.

   .. versionadded:: 3.3


.. function:: login_tty(fd, /)

   Chuẩn bị tty mà fd là một file descriptor cho một phiên đăng nhập mới. Biến tiến trình gọi thành session leader; đặt tty làm controlling tty, stdin, stdout và stderr của tiến trình gọi; đóng fd.

   .. availability:: Unix, not WASI.

   .. versionadded:: 3.11


.. function:: lseek(fd, pos, whence, /)

   Đặt vị trí hiện tại của bộ mô tả tệp *fd* thành vị trí *pos*, được điều chỉnh bởi *whence*, và trả về vị trí mới tính bằng byte so với đầu tệp. Các giá trị hợp lệ cho *whence* là:

   * :const:`SEEK_SET` hoặc ``0`` -- đặt *pos* tương đối so với đầu tệp
   * :const:`SEEK_CUR` hoặc ``1`` -- đặt *pos* tương đối so với vị trí hiện tại trong tệp
   * :const:`SEEK_END` hoặc ``2`` -- đặt *pos* tương đối so với cuối tệp
   * :const:`SEEK_HOLE` -- đặt *pos* đến vị trí dữ liệu tiếp theo, tương đối so với *pos*
   * :const:`SEEK_DATA` -- đặt *pos* đến khoảng trống dữ liệu tiếp theo, tương đối so với *pos*

   .. versionchanged:: 3.3

      Bổ sung hỗ trợ cho :const:`!SEEK_HOLE` và :const:`!SEEK_DATA`.


.. data:: SEEK_SET
          SEEK_CUR SEEK_END

   Các tham số của hàm :func:`lseek` và phương thức :meth:`~io.IOBase.seek` trên :term:`các đối tượng dạng tệp <file object>`, dùng cho whence để điều chỉnh chỉ báo vị trí tệp.

   :const:`SEEK_SET`
      Điều chỉnh vị trí tệp tương đối so với đầu tệp.
   :const:`SEEK_CUR`
      Điều chỉnh vị trí tệp tương đối so với vị trí hiện tại trong tệp.
   :const:`SEEK_END`
      Điều chỉnh vị trí tệp tương đối so với cuối tệp.

   Giá trị của chúng lần lượt là 0, 1 và 2.


.. data:: SEEK_HOLE
          SEEK_DATA

   Các tham số của hàm :func:`lseek` và phương thức :meth:`~io.IOBase.seek` trên các đối tượng :term:`giống tệp <file object>`, dùng để tìm kiếm dữ liệu và các vùng trống trong tệp được cấp phát thưa.

   :data:`!SEEK_DATA`
      Điều chỉnh vị trí offset của tệp đến vị trí tiếp theo chứa dữ liệu, tính tương đối so với vị trí tìm kiếm.

   :data:`!SEEK_HOLE`
      Điều chỉnh vị trí offset của tệp đến vị trí tiếp theo chứa một vùng trống, tính tương đối so với vị trí tìm kiếm. Vùng trống được định nghĩa là một chuỗi các số 0.

   .. note::

      Các thao tác này chỉ có ý nghĩa đối với những filesystem hỗ trợ chúng.

   .. availability:: Linux >= 3.1, macOS, Unix

   .. versionadded:: 3.3


.. function:: open(path, flags, mode=0o777, *, dir_fd=None)

   Mở tệp *path* và thiết lập các cờ khác nhau theo *flags*, đồng thời có thể thiết lập mode của tệp theo *mode*. Khi tính *mode*, giá trị umask hiện tại trước tiên sẽ được loại ra bằng phép mặt nạ. Trả về file descriptor của tệp vừa mở. File descriptor mới là :ref:`không kế thừa <fd_inheritance>`.

   Để biết mô tả về các giá trị cờ và mode, hãy xem tài liệu C run-time; các hằng số cờ (chẳng hạn như :const:`O_RDONLY` và :const:`O_WRONLY`) được định nghĩa trong module :mod:`!os`. Cụ thể, trên Windows, cần thêm
   :const:`O_BINARY` để mở tệp ở binary mode.

   Hàm này có thể hỗ trợ :ref:`các đường dẫn tương đối với bộ mô tả thư mục <dir_fd>` bằng tham số *dir_fd*.

   .. audit-event:: open path,mode,flags os.open

   .. versionchanged:: 3.4
      File descriptor mới hiện không thể kế thừa.

   .. note::

      Hàm này предназначена cho I/O cấp thấp. Trong trường hợp sử dụng thông thường, hãy dùng hàm tích hợp sẵn :func:`open`, hàm này trả về một :term:`file object` với
      các phương thức :meth:`~io.BufferedIOBase.read` và :meth:`~io.BufferedIOBase.write`. Để bọc một bộ mô tả tệp trong một đối tượng tệp, hãy dùng :func:`fdopen`.

   .. versionchanged:: 3.3
      Đã thêm tham số *dir_fd*.

   .. versionchanged:: 3.5
      Nếu system call bị gián đoạn và signal handler không phát sinh ngoại lệ, hàm hiện sẽ thử lại system call thay vì phát sinh một
      ngoại lệ :exc:`InterruptedError` (xem :pep:`475` để biết lý do).

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.

Các hằng số sau đây là các tùy chọn cho tham số *flags* của
:func:`~os.open` function. Có thể kết hợp chúng bằng toán tử OR theo bit ``|``. Một số hằng số không khả dụng trên tất cả các nền tảng. Để biết mô tả về khả năng hỗ trợ và cách sử dụng, hãy tham khảo trang hướng dẫn :manpage:`open(2)` trên Unix hoặc `the MSDN <https://msdn.microsoft.com/en-us/library/z0kc8e3z.aspx>`_ trên Windows.


.. data:: O_RDONLY
          O_WRONLY O_RDWR O_APPEND O_CREAT O_EXCL O_TRUNC

   Các hằng số trên khả dụng trên Unix và Windows.


.. data:: O_DSYNC
          O_RSYNC O_SYNC O_NDELAY O_NONBLOCK O_NOCTTY O_CLOEXEC

   Các hằng số trên chỉ khả dụng trên Unix.

   .. versionchanged:: 3.3
      Thêm hằng số :data:`O_CLOEXEC`.

.. data:: O_BINARY
          O_NOINHERIT O_SHORT_LIVED O_TEMPORARY O_RANDOM O_SEQUENTIAL O_TEXT

   Các hằng số trên chỉ khả dụng trên Windows.

.. data:: O_EVTONLY
          O_FSYNC O_SYMLINK O_NOFOLLOW_ANY

   Các hằng số trên chỉ khả dụng trên macOS.

   .. versionchanged:: 3.10
      Thêm các hằng số :data:`O_EVTONLY`, :data:`O_FSYNC`, :data:`O_SYMLINK` và :data:`O_NOFOLLOW_ANY`.

.. data:: O_ASYNC
          O_DIRECT O_DIRECTORY O_NOFOLLOW O_NOATIME O_PATH O_TMPFILE O_SHLOCK O_EXLOCK

   Các hằng số nêu trên là phần mở rộng và không tồn tại nếu không được thư viện C định nghĩa.

   .. versionchanged:: 3.4
      Thêm :data:`O_PATH` trên các hệ thống hỗ trợ nó. Thêm :data:`O_TMPFILE`, chỉ có trên Linux Kernel 3.11
        hoặc mới hơn.


.. function:: openpty()

   .. index:: pair: module; pty

   Mở một cặp pseudo-terminal mới. Trả về một cặp bộ mô tả tệp ``(master, slave)`` lần lượt dành cho pty và tty. Các bộ mô tả tệp mới :ref:`không thể kế thừa <fd_inheritance>`. Để có một cách tiếp cận (hơi) portable hơn, hãy sử dụng module :mod:`pty`.

   .. availability:: Unix, not WASI.

   .. versionchanged:: 3.4
      Các bộ mô tả tệp mới hiện không thể kế thừa.


.. function:: pipe()

   Tạo một pipe.  Trả về một cặp bộ mô tả tệp ``(r, w)`` có thể dùng lần lượt để đọc và ghi. Bộ mô tả tệp mới là
   :ref:`không kế thừa <fd_inheritance>`.

   .. availability:: Unix, Windows.

   .. versionchanged:: 3.4
      Các bộ mô tả tệp mới hiện không thể kế thừa.


.. function:: pipe2(flags, /)

   Tạo một pipe với *flags* được thiết lập một cách nguyên tử. *flags* có thể được tạo bằng cách OR một hoặc nhiều giá trị sau:
   :data:`O_NONBLOCK`, :data:`O_CLOEXEC`. Trả về một cặp file descriptor ``(r, w)`` có thể lần lượt được sử dụng để đọc và ghi.

   .. availability:: Unix, not WASI, not macOS, not iOS.

   .. versionadded:: 3.3


.. function:: posix_fallocate(fd, offset, len, /)

   Đảm bảo có đủ dung lượng đĩa được cấp phát cho tệp được chỉ định bởi *fd*, bắt đầu từ *offset* và tiếp tục trong *len* byte.

   .. availability:: Unix, not macOS, not iOS.

   .. versionadded:: 3.3


.. function:: posix_fadvise(fd, offset, len, advice, /)

   Thông báo ý định truy cập dữ liệu theo một mẫu cụ thể, nhờ đó cho phép kernel thực hiện các tối ưu hóa. Gợi ý này áp dụng cho vùng của tệp được chỉ định bởi *fd*, bắt đầu tại *offset* và tiếp tục trong *len* byte. *advice* là một trong các giá trị :data:`POSIX_FADV_NORMAL`, :data:`POSIX_FADV_SEQUENTIAL`,
   :data:`POSIX_FADV_RANDOM`, :data:`POSIX_FADV_NOREUSE`,
   :data:`POSIX_FADV_WILLNEED` hoặc :data:`POSIX_FADV_DONTNEED`.

   .. availability:: Unix, not macOS, not iOS.

   .. versionadded:: 3.3


.. data:: POSIX_FADV_NORMAL
          POSIX_FADV_SEQUENTIAL POSIX_FADV_RANDOM POSIX_FADV_NOREUSE POSIX_FADV_WILLNEED POSIX_FADV_DONTNEED

   Các cờ có thể được sử dụng trong *advice* ở :func:`posix_fadvise`, chỉ rõ mẫu truy cập có khả năng sẽ được sử dụng.

   .. availability:: Unix.

   .. versionadded:: 3.3


.. function:: pread(fd, n, offset, /)

   Đọc nhiều nhất *n* byte từ file descriptor *fd* tại vị trí *offset*, giữ nguyên offset của tệp.

   Trả về một bytestring chứa các byte đã đọc. Nếu đã đến cuối tệp được *fd* tham chiếu, một đối tượng bytes rỗng sẽ được trả về.

   .. availability:: Unix.

   .. versionadded:: 3.3


.. function:: posix_openpt(oflag, /)

   Mở và trả về một file descriptor cho thiết bị pseudo-terminal chính.

   Gọi hàm thư viện chuẩn C :c:func:`posix_openpt`. Đối số *oflag* được dùng để thiết lập các cờ trạng thái tệp và chế độ truy cập tệp như được chỉ định trong trang hướng dẫn của :c:func:`posix_openpt` trên hệ thống của bạn.

   File descriptor được trả về là :ref:`non-inheritable <fd_inheritance>`. Nếu giá trị :data:`O_CLOEXEC` khả dụng trên hệ thống, giá trị đó sẽ được thêm vào *oflag*.

   .. availability:: Unix, not WASI.

   .. versionadded:: 3.13


.. function:: preadv(fd, buffers, offset, flags=0, /)

   Đọc từ file descriptor *fd* tại vị trí *offset* vào một đối tượng có thể thay đổi
   :term:`các đối tượng dạng byte <bytes-like object>` *các bộ đệm*, giữ nguyên offset của tệp. Truyền dữ liệu vào từng bộ đệm cho đến khi bộ đệm đầy, sau đó chuyển sang bộ đệm tiếp theo trong chuỗi để chứa phần dữ liệu còn lại.

   Đối số flags chứa phép OR theo bit của không hoặc một hay nhiều cờ sau:

   - :data:`RWF_HIPRI`
   - :data:`RWF_NOWAIT`

   Trả về tổng số byte thực sự đã đọc, giá trị này có thể nhỏ hơn tổng dung lượng của tất cả các đối tượng.

   Hệ điều hành có thể đặt giới hạn (:func:`sysconf` value ``'SC_IOV_MAX'``) đối với số lượng bộ đệm có thể sử dụng.

   Kết hợp chức năng của :func:`os.readv` và :func:`os.pread`.

   .. availability:: Linux >= 2.6.30, FreeBSD >= 6.0, OpenBSD >= 2.7, AIX >= 7.1.

      Việc sử dụng các cờ yêu cầu Linux >= 4.6.

   .. versionadded:: 3.7


.. data:: RWF_NOWAIT

   Không chờ dữ liệu chưa khả dụng ngay lập tức. Nếu chỉ định cờ này, system call sẽ trả về ngay lập tức nếu phải đọc dữ liệu từ bộ nhớ lưu trữ nền hoặc chờ một khóa.

   Nếu một số dữ liệu đã được đọc thành công, nó sẽ trả về số byte đã đọc. Nếu không có byte nào được đọc, nó sẽ trả về ``-1`` và đặt errno thành
   :const:`errno.EAGAIN`.

   .. availability:: Linux >= 4.14.

   .. versionadded:: 3.7


.. data:: RWF_HIPRI

   Đọc/ghi ưu tiên cao. Cho phép các filesystem dựa trên block sử dụng polling của thiết bị, giúp giảm độ trễ nhưng có thể sử dụng thêm tài nguyên.

   Hiện tại, trên Linux, tính năng này chỉ có thể được sử dụng trên một file descriptor được mở bằng flag :data:`O_DIRECT`.

   .. availability:: Linux >= 4.6.

   .. versionadded:: 3.7


.. function:: ptsname(fd, /)

   Trả về tên của thiết bị pseudo-terminal slave liên kết với thiết bị pseudo-terminal master mà file descriptor *fd* tham chiếu đến. File descriptor *fd* không bị đóng khi xảy ra lỗi.

   Gọi hàm thư viện chuẩn C reentrant :c:func:`ptsname_r` nếu hàm này khả dụng; nếu không, hàm thư viện chuẩn C
   :c:func:`ptsname`, vốn không được đảm bảo là thread-safe, sẽ được gọi.

   .. availability:: Unix, not WASI.

   .. versionadded:: 3.13


.. function:: pwrite(fd, str, offset, /)

   Ghi bytestring trong *str* vào file descriptor *fd* tại vị trí *offset*, giữ nguyên file offset.

   Trả về số byte thực sự đã được ghi.

   .. availability:: Unix.

   .. versionadded:: 3.3


.. function:: pwritev(fd, buffers, offset, flags=0, /)

   Ghi nội dung của *buffers* vào bộ mô tả tệp *fd* tại độ lệch *offset*, giữ nguyên độ lệch tệp.  *buffers* phải là một chuỗi gồm
   :term:`các đối tượng giống bytes <bytes-like object>`. Các buffer được xử lý theo thứ tự trong mảng. Toàn bộ nội dung của buffer đầu tiên được ghi trước khi chuyển sang buffer thứ hai, và tiếp tục như vậy.

   Đối số flags chứa phép OR theo bit của không hoặc một hay nhiều cờ sau:

   - :data:`RWF_DSYNC`
   - :data:`RWF_SYNC`
   - :data:`RWF_APPEND`

   Trả về tổng số byte thực sự đã được ghi.

   Hệ điều hành có thể đặt giới hạn (:func:`sysconf` value ``'SC_IOV_MAX'``) đối với số lượng bộ đệm có thể sử dụng.

   Kết hợp chức năng của :func:`os.writev` và :func:`os.pwrite`.

   .. availability:: Linux >= 2.6.30, FreeBSD >= 6.0, OpenBSD >= 2.7, AIX >= 7.1.

      Việc sử dụng các cờ yêu cầu Linux >= 4.6.

   .. versionadded:: 3.7


.. data:: RWF_DSYNC

   Cung cấp phiên bản tương đương theo từng lần ghi của cờ :data:`O_DSYNC` :func:`os.open`. Hiệu lực của cờ này chỉ áp dụng cho phạm vi dữ liệu được system call ghi.

   .. availability:: Linux >= 4.7.

   .. versionadded:: 3.7


.. data:: RWF_SYNC

   Cung cấp phiên bản tương đương theo từng lần ghi của cờ :data:`O_SYNC` :func:`os.open`. Hiệu lực của cờ này chỉ áp dụng cho phạm vi dữ liệu được system call ghi.

   .. availability:: Linux >= 4.7.

   .. versionadded:: 3.7


.. data:: RWF_APPEND

   Cung cấp phiên bản tương đương theo từng lần ghi của cờ :data:`O_APPEND` :func:`os.open`. Cờ này chỉ có ý nghĩa đối với :func:`os.pwritev`, và hiệu lực của nó chỉ áp dụng cho phạm vi dữ liệu được system call ghi. Đối số *offset* không ảnh hưởng đến thao tác ghi; dữ liệu luôn được nối vào cuối tệp. Tuy nhiên, nếu đối số *offset* là ``-1``, *offset* hiện tại của tệp sẽ được cập nhật.

   .. availability:: Linux >= 4.16.

   .. versionadded:: 3.10


.. function:: read(fd, n, /)

   Đọc nhiều nhất *n* byte từ file descriptor *fd*.

   Trả về một bytestring chứa các byte đã đọc. Nếu đã đến cuối tệp được *fd* tham chiếu, một đối tượng bytes rỗng sẽ được trả về.

   .. note::

      Hàm này dành cho I/O cấp thấp và phải được áp dụng cho file descriptor do :func:`os.open` hoặc :func:`pipe` trả về.  Để đọc một "file object" được trả về bởi hàm tích hợp sẵn :func:`open` hoặc bởi
      :func:`popen` hoặc :func:`fdopen`, hoặc :data:`sys.stdin`, hãy sử dụng các phương thức của nó
      :meth:`~io.TextIOBase.read` hoặc :meth:`~io.IOBase.readline`.

   .. versionchanged:: 3.5
      Nếu system call bị gián đoạn và signal handler không phát sinh ngoại lệ, hàm hiện sẽ thử lại system call thay vì phát sinh một
      ngoại lệ :exc:`InterruptedError` (xem :pep:`475` để biết lý do).


.. function:: readinto(fd, buffer, /)

   Đọc từ một file descriptor *fd* vào một
   đối tượng buffer có thể thay đổi :ref:`buffer object <bufferobjects>` *buffer*.

   *buffer* phải có thể thay đổi và có dạng :term:`bytes-like <bytes-like object>`. Khi thành công, hàm trả về số byte đã đọc. Số byte được đọc có thể ít hơn kích thước của buffer. Lệnh gọi hệ thống bên dưới sẽ được thử lại khi bị gián đoạn bởi một signal, trừ khi signal handler phát sinh một exception. Các lỗi khác sẽ không được thử lại và một lỗi sẽ được phát sinh.

   Trả về 0 nếu *fd* ở cuối tệp hoặc nếu *buffer* được cung cấp có độ dài bằng 0 (có thể dùng để kiểm tra lỗi mà không cần đọc dữ liệu). Không bao giờ trả về số âm.

   .. note::

      Hàm này dành cho I/O cấp thấp và phải được áp dụng cho một file descriptor do :func:`os.open` hoặc :func:`os.pipe` trả về. Để đọc một "file object" do hàm tích hợp sẵn :func:`open` trả về, hoặc
      :data:`sys.stdin`, hãy sử dụng các hàm thành viên của nó, ví dụ như
      :meth:`io.BufferedIOBase.readinto`, :meth:`io.BufferedIOBase.read`, hoặc
      :meth:`io.TextIOBase.read`

   .. versionadded:: 3.14


.. function:: sendfile(out_fd, in_fd, offset, count)
              sendfile(out_fd, in_fd, offset, count, headers=(), trailers=(), flags=0)

   Sao chép *count* byte từ file descriptor *in_fd* sang file descriptor *out_fd*, bắt đầu tại *offset*. Trả về số byte đã gửi. Khi đạt đến EOF, trả về ``0``.

   Ký hiệu hàm đầu tiên được hỗ trợ trên tất cả các nền tảng định nghĩa
   :func:`sendfile`.

   Trên Linux, nếu *offset* được cung cấp dưới dạng ``None``, các byte sẽ được đọc từ vị trí hiện tại của *in_fd* và vị trí của *in_fd* sẽ được cập nhật.

   Trường hợp thứ hai có thể được sử dụng trên macOS và FreeBSD, trong đó *headers* và *trailers* là các chuỗi buffer tùy ý được ghi trước và sau khi dữ liệu từ *in_fd* được ghi. Nó trả về kết quả giống như trường hợp thứ nhất.

   Trên macOS và FreeBSD, giá trị ``0`` của *count* chỉ định rằng việc gửi sẽ tiếp tục cho đến khi đạt đến cuối *in_fd*.

   Tất cả các nền tảng đều hỗ trợ socket làm file descriptor *out_fd*, và một số nền tảng cũng cho phép các loại khác (ví dụ: file thông thường, pipe).

   Các ứng dụng đa nền tảng không nên sử dụng các đối số *headers*, *trailers* và *flags*.

   .. availability:: Unix, not WASI.

   .. note::

      Để sử dụng wrapper cấp cao hơn cho :func:`sendfile`, hãy xem
      :meth:`socket.socket.sendfile`.

   .. versionadded:: 3.3

   .. versionchanged:: 3.9
      Các tham số *out* và *in* đã được đổi tên thành *out_fd* và *in_fd*.


.. data:: SF_NODISKIO
          SF_MNOWAIT SF_SYNC

   Các tham số của hàm :func:`sendfile`, nếu bản triển khai hỗ trợ chúng.

   .. availability:: Unix, not WASI.

   .. versionadded:: 3.3

.. data:: SF_NOCACHE

   Tham số của hàm :func:`sendfile`, nếu bản triển khai hỗ trợ tham số này. Dữ liệu sẽ không được lưu vào bộ nhớ ảo và sẽ được giải phóng sau đó.

   .. availability:: Unix, not WASI.

   .. versionadded:: 3.11


.. function:: set_blocking(fd, blocking, /)

   Đặt chế độ chặn của file descriptor được chỉ định. Đặt
   cờ :data:`O_NONBLOCK` nếu chế độ chặn là ``False``, nếu không thì xóa cờ.

   Xem thêm :func:`get_blocking` và :meth:`socket.socket.setblocking`.

   .. availability:: Unix, Windows.

      Hàm này bị giới hạn trên WASI; xem :ref:`wasm-availability` để biết thêm thông tin.

      Trên Windows, hàm này chỉ áp dụng cho pipes.

   .. versionadded:: 3.5

   .. versionchanged:: 3.12
      Đã thêm hỗ trợ pipes trên Windows.


.. function:: splice(src, dst, count, offset_src=None, offset_dst=None, flags=0)

   Chuyển *count* byte từ file descriptor *src*, bắt đầu từ offset *offset_src*, đến file descriptor *dst*, bắt đầu từ offset *offset_dst*.

   Hành vi splice có thể được thay đổi bằng cách chỉ định giá trị *flags*. Có thể sử dụng bất kỳ biến nào sau đây, kết hợp bằng phép OR theo bit (toán tử ``|``):

   * Nếu chỉ định :const:`SPLICE_F_MOVE`, kernel sẽ được yêu cầu di chuyển các trang thay vì sao chép, nhưng các trang vẫn có thể được sao chép nếu kernel không thể di chuyển các trang khỏi pipe.

   * Nếu chỉ định :const:`SPLICE_F_NONBLOCK`, kernel sẽ được yêu cầu không chặn khi thực hiện I/O. Điều này khiến các thao tác splice trên pipe trở thành nonblocking, nhưng splice vẫn có thể chặn vì các file descriptor được splice có thể chặn.

   * Nếu chỉ định :const:`SPLICE_F_MORE`, tùy chọn này gợi ý cho kernel rằng sẽ có thêm dữ liệu đến trong một thao tác splice tiếp theo.

   Ít nhất một trong các file descriptor phải tham chiếu đến một pipe. Nếu *offset_src* là ``None``, thì *src* được đọc từ vị trí hiện tại; tương tự đối với *offset_dst*. Offset liên kết với file descriptor tham chiếu đến một pipe phải là ``None``. Các tệp được *src* và *dst* trỏ tới phải nằm trên cùng một filesystem; nếu không, một :exc:`OSError` sẽ được phát sinh với
   :attr:`~OSError.errno` được đặt thành :const:`errno.EXDEV`.

   Thao tác sao chép này được thực hiện mà không phải chịu thêm chi phí truyền dữ liệu từ kernel vào user space rồi quay lại kernel. Ngoài ra, một số filesystem có thể triển khai thêm các tối ưu hóa. Thao tác sao chép được thực hiện như thể cả hai tệp đều được mở ở dạng binary.

   Khi hoàn tất thành công, trả về số byte được splice đến hoặc đi từ pipe. Giá trị trả về bằng 0 означает kết thúc đầu vào. Nếu *src* tham chiếu đến một pipe, điều này có nghĩa là không có dữ liệu nào để truyền và việc block sẽ không hợp lý vì không có writer nào được kết nối với đầu ghi của pipe.

   .. seealso:: Trang man :manpage:`splice(2)`.

   .. availability:: Linux >= 2.6.17 with glibc >= 2.5

   .. versionadded:: 3.10


.. data:: SPLICE_F_MOVE
          SPLICE_F_NONBLOCK SPLICE_F_MORE

   .. versionadded:: 3.10

.. function:: readv(fd, buffers, /)

   Đọc từ file descriptor *fd* vào một số :term:`đối tượng giống bytes có thể thay đổi <bytes-like object>` *bộ đệm*. Truyền dữ liệu vào từng bộ đệm cho đến khi bộ đệm đầy, sau đó chuyển sang bộ đệm tiếp theo trong chuỗi để chứa phần dữ liệu còn lại.

   Trả về tổng số byte thực sự đã đọc, giá trị này có thể nhỏ hơn tổng dung lượng của tất cả các đối tượng.

   Hệ điều hành có thể đặt giới hạn (:func:`sysconf` value ``'SC_IOV_MAX'``) đối với số lượng bộ đệm có thể sử dụng.

   .. availability:: Unix.

   .. versionadded:: 3.3


.. function:: tcgetpgrp(fd, /)

   Trả về nhóm tiến trình được liên kết với terminal được chỉ định bởi *fd* (một file descriptor đang mở được trả về bởi :func:`os.open`).

   .. availability:: Unix, not WASI.


.. function:: tcsetpgrp(fd, pg, /)

   Đặt nhóm tiến trình được liên kết với terminal được chỉ định bởi *fd* (một file descriptor đang mở được trả về bởi :func:`os.open`) thành *pg*.

   .. availability:: Unix, not WASI.


.. function:: ttyname(fd, /)

   Trả về một chuỗi chỉ định thiết bị terminal được liên kết với file descriptor *fd*. Nếu *fd* không được liên kết với thiết bị terminal, một ngoại lệ sẽ được phát sinh.

   .. availability:: Unix.


.. function:: unlockpt(fd, /)

   Mở khóa thiết bị pseudo-terminal phụ được liên kết với thiết bị pseudo-terminal chính mà file descriptor *fd* tham chiếu đến. File descriptor *fd* không bị đóng khi xảy ra lỗi.

   Gọi hàm thư viện chuẩn C :c:func:`unlockpt`.

   .. availability:: Unix, not WASI.

   .. versionadded:: 3.13


.. function:: write(fd, str, /)

   Ghi bytestring trong *str* vào file descriptor *fd*.

   Trả về số byte thực sự đã được ghi.

   .. note::

      Hàm này được thiết kế cho I/O cấp thấp và phải được áp dụng cho một file descriptor được trả về bởi :func:`os.open` hoặc :func:`pipe`. Để ghi một "file object" được trả về bởi hàm tích hợp sẵn :func:`open` hoặc bởi :func:`popen` hoặc
      :func:`fdopen`, hoặc :data:`sys.stdout` hay :data:`sys.stderr`, hãy sử dụng
      phương thức :meth:`~io.TextIOBase.write`.

   .. versionchanged:: 3.5
      Nếu system call bị gián đoạn và signal handler không phát sinh ngoại lệ, hàm hiện sẽ thử lại system call thay vì phát sinh một
      ngoại lệ :exc:`InterruptedError` (xem :pep:`475` để biết lý do).


.. function:: writev(fd, buffers, /)

   Ghi nội dung của *buffers* vào bộ mô tả tệp *fd*. *buffers* phải là một chuỗi các :term:`đối tượng dạng bytes <bytes-like object>`. Các buffer được xử lý theo thứ tự trong mảng. Toàn bộ nội dung của buffer đầu tiên được ghi trước khi chuyển sang buffer thứ hai, và tiếp tục như vậy.

   Trả về tổng số byte thực sự đã được ghi.

   Hệ điều hành có thể đặt giới hạn (:func:`sysconf` value ``'SC_IOV_MAX'``) đối với số lượng bộ đệm có thể sử dụng.

   .. availability:: Unix.

   .. versionadded:: 3.3


.. _terminal-size:

Truy vấn kích thước của terminal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 3.3

.. function:: get_terminal_size(fd=STDOUT_FILENO, /)

   Trả về kích thước cửa sổ terminal dưới dạng ``(columns, lines)``, một tuple thuộc kiểu :class:`terminal_size`.

   Đối số tùy chọn ``fd`` (mặc định là ``STDOUT_FILENO``, hoặc đầu ra tiêu chuẩn) chỉ định bộ mô tả tệp cần được truy vấn.

   Nếu bộ mô tả tệp không được kết nối với terminal, một :exc:`OSError` sẽ được phát sinh.

   :func:`shutil.get_terminal_size` là hàm cấp cao thường được sử dụng, còn ``os.get_terminal_size`` là phần triển khai cấp thấp.

   .. availability:: Unix, Windows.

.. class:: terminal_size

   Một lớp con của tuple, chứa ``(columns, lines)`` về kích thước cửa sổ terminal.

   .. attribute:: columns

      Chiều rộng của cửa sổ terminal tính bằng số ký tự.

   .. attribute:: lines

      Chiều cao của cửa sổ terminal tính bằng số ký tự.


.. _fd_inheritance:

Kế thừa File Descriptor
~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 3.4

File descriptor có cờ "inheritable" cho biết file descriptor đó có thể được các tiến trình con kế thừa hay không. Kể từ Python 3.4, các file descriptor do Python tạo ra mặc định không thể được kế thừa.

Trên UNIX, các file descriptor không thể được kế thừa sẽ bị đóng trong các tiến trình con khi thực thi một chương trình mới, còn các file descriptor khác sẽ được kế thừa. Lưu ý rằng các file descriptor không thể được kế thừa vẫn *được kế thừa* bởi các tiến trình con trên :func:`os.fork`.

Trên Windows, các handle và file descriptor không thể kế thừa sẽ được đóng trong các tiến trình con, ngoại trừ các stream chuẩn (file descriptor 0, 1 và 2: stdin, stdout và stderr), luôn được kế thừa. Khi sử dụng các hàm :func:`spawn\* <spawnl>`, tất cả handle có thể kế thừa và tất cả file descriptor có thể kế thừa đều được kế thừa. Khi sử dụng module :mod:`subprocess`, tất cả file descriptor ngoại trừ các stream chuẩn sẽ được đóng, và các handle có thể kế thừa chỉ được kế thừa nếu tham số *close_fds* là ``False``.

Trên các nền tảng WebAssembly, file descriptor không thể được sửa đổi.

.. function:: get_inheritable(fd, /)

   Lấy cờ "inheritable" của file descriptor được chỉ định (một giá trị boolean).

.. function:: set_inheritable(fd, inheritable, /)

   Đặt cờ "inheritable" của file descriptor được chỉ định.

.. function:: get_handle_inheritable(handle, /)

   Lấy cờ "inheritable" của handle được chỉ định (một giá trị boolean).

   .. availability:: Windows.

.. function:: set_handle_inheritable(handle, inheritable, /)

   Đặt cờ "inheritable" của handle được chỉ định.

   .. availability:: Windows.


.. _os-file-dir:

Tệp và Thư mục
--------------

Trên một số nền tảng Unix, nhiều hàm trong số này hỗ trợ một hoặc nhiều tính năng sau:

.. _path_fd:

* **chỉ định một file descriptor:** Thông thường, đối số *path* được truyền cho các hàm trong module :mod:`!os` phải là một chuỗi chỉ định đường dẫn tệp. Tuy nhiên, hiện nay một số hàm cũng chấp nhận một file descriptor đã mở cho đối số *path*. Khi đó, hàm sẽ thao tác trên tệp được descriptor tham chiếu. Đối với các hệ thống POSIX, Python sẽ gọi biến thể của hàm có tiền tố ``f`` (ví dụ: gọi ``fchdir`` thay vì ``chdir``).

  Bạn có thể kiểm tra trên nền tảng của mình xem *path* có thể được chỉ định dưới dạng file descriptor cho một hàm cụ thể hay không bằng cách sử dụng :data:`os.supports_fd`. Nếu chức năng này không khả dụng, việc sử dụng nó sẽ gây ra một
  :exc:`NotImplementedError`.

  Nếu hàm cũng hỗ trợ các đối số *dir_fd* hoặc *follow_symlinks*, thì việc chỉ định một trong hai đối số đó khi cung cấp *path* dưới dạng file descriptor là lỗi.

.. _dir_fd:

* **các đường dẫn tương đối với directory descriptor:** Nếu *dir_fd* không phải là ``None``, thì nó phải là một file descriptor tham chiếu đến một thư mục, và đường dẫn cần thao tác phải là đường dẫn tương đối; khi đó, path sẽ được tính tương đối với thư mục đó. Nếu đường dẫn là tuyệt đối, *dir_fd* sẽ bị bỏ qua. Đối với các hệ thống POSIX, Python sẽ gọi biến thể của hàm có hậu tố ``at`` và có thể có tiền tố ``f`` (ví dụ: gọi ``faccessat`` thay vì ``access``).

  Bạn có thể kiểm tra trên nền tảng của mình xem *dir_fd* có được hỗ trợ cho một hàm cụ thể hay không bằng cách sử dụng :data:`os.supports_dir_fd`. Nếu không khả dụng, việc sử dụng nó sẽ gây ra một :exc:`NotImplementedError`.

.. _follow_symlinks:

* **không theo symlink:** Nếu *follow_symlinks* là ``False`` và phần tử cuối cùng của đường dẫn cần thao tác là một symbolic link, hàm sẽ thao tác trên chính symbolic link đó thay vì tệp được link trỏ tới. Đối với các hệ thống POSIX, Python sẽ gọi biến thể ``l...`` của hàm.

  Bạn có thể kiểm tra xem *follow_symlinks* có được hỗ trợ cho một hàm cụ thể trên nền tảng của mình hay không bằng cách sử dụng :data:`os.supports_follow_symlinks`. Nếu không khả dụng, việc sử dụng nó sẽ gây ra :exc:`NotImplementedError`.



.. function:: access(path, mode, *, dir_fd=None, effective_ids=False, follow_symlinks=True)

   Sử dụng uid/gid thực để kiểm tra quyền truy cập vào *path*. Lưu ý rằng hầu hết các thao tác sẽ sử dụng uid/gid hiệu dụng, do đó, routine này có thể được dùng trong môi trường suid/sgid để kiểm tra xem người dùng gọi có quyền truy cập được chỉ định vào *path* hay không. *mode* phải là :const:`F_OK` để kiểm tra sự tồn tại của *path*, hoặc có thể là phép OR bao hàm của một hoặc nhiều giá trị trong :const:`R_OK`, :const:`W_OK`, và
   :const:`X_OK` để kiểm tra quyền. Trả về :const:`True` nếu quyền truy cập được cho phép,
   :const:`False` nếu không. Xem trang hướng dẫn Unix :manpage:`access(2)` để biết thêm thông tin.

   Hàm này có thể hỗ trợ việc chỉ định :ref:`paths tương đối với các bộ mô tả thư mục <dir_fd>` và :ref:`không đi theo symlink <follow_symlinks>`.

   Nếu *effective_ids* là ``True``, :func:`access` sẽ thực hiện các kiểm tra quyền truy cập bằng uid/gid hiệu dụng thay vì uid/gid thực. *effective_ids* có thể không được nền tảng của bạn hỗ trợ; bạn có thể kiểm tra xem tùy chọn này có khả dụng hay không bằng cách sử dụng :data:`os.supports_effective_ids`. Nếu không khả dụng, việc sử dụng nó sẽ gây ra :exc:`NotImplementedError`.

   .. note::

      Việc sử dụng :func:`access` để kiểm tra xem người dùng có được phép, chẳng hạn như mở một tệp, trước khi thực sự thực hiện thao tác đó bằng :func:`open` sẽ tạo ra một lỗ hổng bảo mật, vì người dùng có thể khai thác khoảng thời gian ngắn giữa lúc kiểm tra và lúc mở tệp để thao túng tệp. Tốt hơn nên sử dụng các kỹ thuật :term:`EAFP`. Ví dụ::

         if os.access("myfile", os.R_OK):
             with open("myfile") as fp:
                 return fp.read()
         return "some default data"

      được viết tốt hơn là::

         try:
             fp = open("myfile")
         except PermissionError:
             return "some default data"
         else:
             with fp:
                 return fp.read()

   .. note::

      Các thao tác I/O có thể không thành công ngay cả khi :func:`access` cho biết rằng chúng sẽ thành công, đặc biệt là đối với các thao tác trên hệ thống tệp mạng, nơi ngữ nghĩa về quyền có thể vượt ra ngoài mô hình bit quyền POSIX thông thường.

   .. versionchanged:: 3.3
      Đã thêm các tham số *dir_fd*, *effective_ids* và *follow_symlinks*.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. data:: F_OK
          R_OK W_OK X_OK

   Các giá trị truyền làm tham số *mode* của :func:`access` để lần lượt kiểm tra sự tồn tại, khả năng đọc, khả năng ghi và khả năng thực thi của *path*.


.. function:: chdir(path)

   .. index:: single: directory; changing

   Thay đổi thư mục làm việc hiện tại thành *path*.

   Hàm này hỗ trợ :ref:`chỉ định một bộ mô tả tệp <path_fd>`. Bộ mô tả phải tham chiếu đến một thư mục đã mở, không phải một tệp đang mở.

   Hàm này có thể phát sinh :exc:`OSError` và các lớp con như
   :exc:`FileNotFoundError`, :exc:`PermissionError` và :exc:`NotADirectoryError`.

   .. audit-event:: os.chdir path os.chdir

   .. seealso::

      Trình quản lý ngữ cảnh :func:`contextlib.chdir`, thay đổi thư mục làm việc hiện tại khi bắt đầu và khôi phục thư mục trước đó khi kết thúc.

   .. versionchanged:: 3.3
      Đã bổ sung hỗ trợ chỉ định *path* dưới dạng bộ mô tả tệp trên một số nền tảng.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: chflags(path, flags, *, follow_symlinks=True)

   Đặt các cờ của *path* thành *flags* dạng số. *flags* có thể nhận một tổ hợp (OR theo bit) của các giá trị sau (được định nghĩa trong mô-đun :mod:`stat`):

   * :const:`stat.UF_NODUMP`
   * :const:`stat.UF_IMMUTABLE`
   * :const:`stat.UF_APPEND`
   * :const:`stat.UF_OPAQUE`
   * :const:`stat.UF_NOUNLINK`
   * :const:`stat.UF_COMPRESSED`
   * :const:`stat.UF_HIDDEN`
   * :const:`stat.SF_ARCHIVED`
   * :const:`stat.SF_IMMUTABLE`
   * :const:`stat.SF_APPEND`
   * :const:`stat.SF_NOUNLINK`
   * :const:`stat.SF_SNAPSHOT`

   Hàm này có thể hỗ trợ :ref:`không theo các symlink <follow_symlinks>`.

   .. audit-event:: os.chflags path,flags os.chflags

   .. availability:: Unix, not WASI.

   .. versionchanged:: 3.3
      Đã thêm tham số *follow_symlinks*.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: chmod(path, mode, *, dir_fd=None, follow_symlinks=True)

   Thay đổi mode của *path* thành *mode* dạng số. *mode* có thể nhận một trong các giá trị sau (như được định nghĩa trong mô-đun :mod:`stat`) hoặc các tổ hợp được OR theo bit của chúng:

   * :const:`stat.S_ISUID`
   * :const:`stat.S_ISGID`
   * :const:`stat.S_ENFMT`
   * :const:`stat.S_ISVTX`
   * :const:`stat.S_IREAD`
   * :const:`stat.S_IWRITE`
   * :const:`stat.S_IEXEC`
   * :const:`stat.S_IRWXU`
   * :const:`stat.S_IRUSR`
   * :const:`stat.S_IWUSR`
   * :const:`stat.S_IXUSR`
   * :const:`stat.S_IRWXG`
   * :const:`stat.S_IRGRP`
   * :const:`stat.S_IWGRP`
   * :const:`stat.S_IXGRP`
   * :const:`stat.S_IRWXO`
   * :const:`stat.S_IROTH`
   * :const:`stat.S_IWOTH`
   * :const:`stat.S_IXOTH`

   Hàm này có thể hỗ trợ :ref:`chỉ định một file descriptor <path_fd>`,
   :ref:`các path tương đối so với các directory descriptor <dir_fd>` và :ref:`không theo các symlink <follow_symlinks>`.

   .. note::

      Mặc dù Windows hỗ trợ :func:`chmod`, bạn chỉ có thể dùng nó để đặt cờ chỉ đọc của tệp (thông qua các hằng số ``stat.S_IWRITE`` và ``stat.S_IREAD`` hoặc một giá trị số nguyên tương ứng). Mọi bit khác đều bị bỏ qua. Giá trị mặc định của *follow_symlinks* là ``False`` trên Windows.

      Hàm này bị giới hạn trên WASI, xem :ref:`wasm-availability` để biết thêm thông tin.

   .. audit-event:: os.chmod path,mode,dir_fd os.chmod

   .. versionchanged:: 3.3
      Đã bổ sung hỗ trợ chỉ định *path* dưới dạng một file descriptor đang mở, cùng các đối số *dir_fd* và *follow_symlinks*.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.

   .. versionchanged:: 3.13
      Đã bổ sung hỗ trợ file descriptor và đối số *follow_symlinks* trên Windows.


.. function:: chown(path, uid, gid, *, dir_fd=None, follow_symlinks=True)

   Thay đổi id chủ sở hữu và nhóm của *path* thành *uid* và *gid* dạng số. Để giữ nguyên một trong các id, hãy đặt giá trị của nó thành -1.

   Hàm này có thể hỗ trợ :ref:`chỉ định một file descriptor <path_fd>`,
   :ref:`các path tương đối so với các directory descriptor <dir_fd>` và :ref:`không theo các symlink <follow_symlinks>`.

   Xem :func:`shutil.chown` để biết hàm cấp cao hơn chấp nhận cả tên lẫn id số.

   .. audit-event:: os.chown path,uid,gid,dir_fd os.chown

   .. availability:: Unix.

      Hàm này bị giới hạn trên WASI, xem :ref:`wasm-availability` để biết thêm thông tin.

   .. versionchanged:: 3.3
      Đã bổ sung hỗ trợ chỉ định *path* dưới dạng một file descriptor đang mở, cùng các đối số *dir_fd* và *follow_symlinks*.

   .. versionchanged:: 3.6
      Hỗ trợ :term:`path-like object`.


.. function:: chroot(path)

   Thay đổi thư mục gốc của tiến trình hiện tại thành *path*.

   .. availability:: Unix, not WASI, not Android.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: fchdir(fd)

   Thay đổi thư mục làm việc hiện tại thành thư mục được biểu diễn bởi file descriptor *fd*. Descriptor phải tham chiếu đến một thư mục đã mở, không phải một tệp đang mở. Kể từ Python 3.3, thao tác này tương đương với ``os.chdir(fd)``.

   .. audit-event:: os.chdir path os.fchdir

   .. availability:: Unix.


.. function:: getcwd()

   Trả về một chuỗi biểu diễn thư mục làm việc hiện tại.


.. function:: getcwdb()

   Trả về một chuỗi byte biểu diễn thư mục làm việc hiện tại.

   .. versionchanged:: 3.8
      Hàm hiện sử dụng encoding UTF-8 trên Windows thay vì ANSI code page: xem :pep:`529` để biết lý do. Hàm không còn bị deprecated trên Windows.


.. function:: lchflags(path, flags)

   Đặt các cờ của *path* thành *flags* dạng số, giống như :func:`chflags`, nhưng không đi theo symbolic link. Kể từ Python 3.3, thao tác này tương đương với ``os.chflags(path, flags, follow_symlinks=False)``.

   .. audit-event:: os.chflags path,flags os.lchflags

   .. availability:: Unix, not WASI.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: lchmod(path, mode)

   Thay đổi mode của *path* thành *mode* dạng số. Nếu path là symbolic link, thao tác này ảnh hưởng đến symbolic link thay vì đích. Xem tài liệu về :func:`chmod` để biết các giá trị có thể có của *mode*. Kể từ Python 3.3, thao tác này tương đương với ``os.chmod(path, mode, follow_symlinks=False)``.

   ``lchmod()`` không thuộc POSIX, nhưng các triển khai Unix có thể có nó nếu hỗ trợ thay đổi mode của symbolic link.

   .. audit-event:: os.chmod path,mode,dir_fd os.lchmod

   .. availability:: Unix, Windows, not Linux, FreeBSD >= 1.3, NetBSD >= 1.3, not OpenBSD

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.

   .. versionchanged:: 3.13
      Đã bổ sung hỗ trợ trên Windows.

.. function:: lchown(path, uid, gid)

   Thay đổi chủ sở hữu và group id của *path* thành *uid* và *gid* dạng số. Hàm này sẽ không đi theo symbolic link. Kể từ Python 3.3, hàm này tương đương với ``os.chown(path, uid, gid, follow_symlinks=False)``.

   .. audit-event:: os.chown path,uid,gid,dir_fd os.lchown

   .. availability:: Unix.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: link(src, dst, *, src_dir_fd=None, dst_dir_fd=None, follow_symlinks=True)

   Tạo một hard link trỏ đến *src* có tên là *dst*.

   Hàm này hỗ trợ chỉ định *src_dir_fd* và/hoặc *dst_dir_fd* để cung cấp :ref:`các đường dẫn tương đối với file descriptor của thư mục <dir_fd>`, cũng như :ref:`không đi theo symlink <follow_symlinks>`. Giá trị mặc định của *follow_symlinks* là ``False`` trên Windows.

   .. audit-event:: os.link src,dst,src_dir_fd,dst_dir_fd os.link

   .. availability:: Unix, Windows.

   .. versionchanged:: 3.2
      Đã bổ sung hỗ trợ cho Windows.

   .. versionchanged:: 3.3
      Đã thêm các tham số *src_dir_fd*, *dst_dir_fd* và *follow_symlinks*.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object` cho *src* và *dst*.


.. function:: listdir(path='.')

   Trả về danh sách chứa tên các mục trong thư mục được chỉ định bởi *path*. Danh sách có thứ tự tùy ý và không bao gồm các mục đặc biệt ``'.'`` và ``'..'`` ngay cả khi chúng có trong thư mục. Nếu một tệp bị xóa khỏi hoặc được thêm vào thư mục trong khi hàm này đang được gọi, việc có bao gồm tên của tệp đó hay không là không xác định.

   *path* có thể là một :term:`path-like object`. Nếu *path* có kiểu ``bytes`` (trực tiếp hoặc gián tiếp thông qua giao diện :class:`PathLike`), tên tệp được trả về cũng sẽ có kiểu ``bytes``; trong mọi trường hợp khác, chúng sẽ có kiểu ``str``.

   Hàm này cũng hỗ trợ :ref:`chỉ định một bộ mô tả tệp <path_fd>`; bộ mô tả tệp phải tham chiếu đến một thư mục.

   .. audit-event:: os.listdir path os.listdir

   .. note::
      Để mã hóa ``str`` tên tệp thành ``bytes``, hãy sử dụng :func:`~os.fsencode`.

   .. seealso::

      Hàm :func:`scandir` trả về các mục trong thư mục cùng với thông tin thuộc tính tệp, mang lại hiệu năng tốt hơn cho nhiều trường hợp sử dụng phổ biến.

   .. versionchanged:: 3.2
      Tham số *path* đã trở thành tùy chọn.

   .. versionchanged:: 3.3
      Đã thêm hỗ trợ chỉ định *path* dưới dạng một file descriptor đang mở.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: listdrives()

   Trả về danh sách chứa tên các ổ đĩa trên hệ thống Windows.

   Tên ổ đĩa thường có dạng ``'C:\\'``. Không phải mọi tên ổ đĩa đều được liên kết với một volume, và một số ổ có thể không truy cập được vì nhiều lý do, bao gồm quyền, kết nối mạng hoặc thiếu phương tiện lưu trữ. Hàm này không kiểm tra quyền truy cập.

   Có thể phát sinh :exc:`OSError` nếu xảy ra lỗi khi thu thập tên các ổ đĩa.

   .. audit-event:: os.listdrives "" os.listdrives

   .. availability:: Windows

   .. versionadded:: 3.12


.. function:: listmounts(volume)

   Trả về danh sách chứa các mount point của một volume trên hệ thống Windows.

   *volume* phải được biểu diễn dưới dạng đường dẫn GUID, chẳng hạn như những đường dẫn được trả về bởi
   :func:`os.listvolumes`. Các volume có thể được mount tại nhiều vị trí hoặc không được mount ở đâu cả. Trong trường hợp sau, danh sách sẽ trống. Các mount point không liên kết với volume sẽ không được hàm này trả về.

   Các mount point được hàm này trả về sẽ là các đường dẫn tuyệt đối và có thể dài hơn tên ổ đĩa.

   Phát sinh :exc:`OSError` nếu volume không được nhận diện hoặc nếu xảy ra lỗi khi thu thập các đường dẫn.

   .. audit-event:: os.listmounts volume os.listmounts

   .. availability:: Windows

   .. versionadded:: 3.12


.. function:: listvolumes()

   Trả về danh sách chứa các volume trong hệ thống.

   Các volume thường được biểu diễn dưới dạng đường dẫn GUID có dạng ``\\?\Volume{xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx}\``. Thông thường, các tệp có thể được truy cập thông qua đường dẫn GUID, tùy thuộc vào quyền. Tuy nhiên, người dùng thường không quen với chúng, vì vậy cách sử dụng được khuyến nghị cho hàm này là truy xuất các mount point bằng :func:`os.listmounts`.

   Có thể phát sinh :exc:`OSError` nếu xảy ra lỗi khi thu thập các volume.

   .. audit-event:: os.listvolumes "" os.listvolumes

   .. availability:: Windows

   .. versionadded:: 3.12


.. function:: lstat(path, *, dir_fd=None)

   Thực hiện tương đương một system call :c:func:`!lstat` trên đường dẫn đã cho. Tương tự :func:`~os.stat`, nhưng không đi theo các symbolic link. Trả về một
   đối tượng :class:`stat_result`.

   Trên các nền tảng không hỗ trợ symbolic link, đây là bí danh của
   :func:`~os.stat`.

   Kể từ Python 3.3, hàm này tương đương với ``os.stat(path, dir_fd=dir_fd, follow_symlinks=False)``.

   Hàm này cũng hỗ trợ các :ref:`đường dẫn tương đối với bộ mô tả thư mục <dir_fd>`.

   .. seealso::

      Hàm :func:`.stat`.

   .. versionchanged:: 3.2
      Đã bổ sung hỗ trợ symbolic link trên Windows 6.0 (Vista).

   .. versionchanged:: 3.3
      Đã thêm tham số *dir_fd*.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.

   .. versionchanged:: 3.8
      Trên Windows, giờ đây mở các reparse point đại diện cho một đường dẫn khác (name surrogate), bao gồm symbolic link và directory junction. Các loại reparse point khác được hệ điều hành phân giải như đối với :func:`~os.stat`.


.. function:: mkdir(path, mode=0o777, *, dir_fd=None)

   Tạo một thư mục có tên *path* với mode dạng số *mode*.

   Nếu thư mục đã tồn tại, :exc:`FileExistsError` sẽ được phát sinh. Nếu một thư mục cha trong đường dẫn không tồn tại, :exc:`FileNotFoundError` sẽ được phát sinh.

   .. _mkdir_modebits:

   Trên một số hệ thống, *mode* bị bỏ qua. Ở những nơi sử dụng giá trị này, giá trị umask hiện tại trước tiên sẽ được che đi. Nếu các bit khác 9 bit cuối (tức 3 chữ số cuối trong biểu diễn bát phân của *mode*) được đặt, ý nghĩa của chúng phụ thuộc vào nền tảng. Trên một số nền tảng, chúng bị bỏ qua và bạn nên gọi
   :func:`chmod` một cách rõ ràng để đặt chúng.

   Trên Windows, một *mode* có giá trị ``0o700`` được xử lý riêng để áp dụng kiểm soát quyền truy cập cho thư mục mới, sao cho chỉ người dùng hiện tại và quản trị viên mới có quyền truy cập. Các giá trị khác của *mode* sẽ bị bỏ qua.

   Hàm này cũng hỗ trợ các :ref:`đường dẫn tương đối với bộ mô tả thư mục <dir_fd>`.

   Bạn cũng có thể tạo các thư mục tạm thời; hãy xem
   :mod:`tempfile` module :func:`tempfile.mkdtemp` có hàm.

   .. audit-event:: os.mkdir path,mode,dir_fd os.mkdir

   .. versionchanged:: 3.3
      Đã thêm tham số *dir_fd*.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.

   .. versionchanged:: 3.13
      Windows hiện xử lý *mode* có giá trị ``0o700``.


.. function:: makedirs(name, mode=0o777, exist_ok=False)

   .. index::
      single: directory; creating
      single: UNC paths; and os.makedirs()

   Hàm tạo thư mục đệ quy. Giống như :func:`mkdir`, nhưng tạo tất cả các thư mục ở các cấp trung gian cần thiết để chứa thư mục lá.

   Tham số *mode* được truyền cho :func:`mkdir` để tạo thư mục lá; xem :ref:`mô tả về mkdir() <mkdir_modebits>` để biết cách diễn giải tham số này. Để đặt các bit quyền tệp của bất kỳ thư mục cha mới nào được tạo, bạn có thể đặt umask trước khi gọi :func:`makedirs`. Các bit quyền tệp của những thư mục cha hiện có sẽ không bị thay đổi.

   Nếu *exist_ok* là ``False`` (giá trị mặc định), một :exc:`FileExistsError` sẽ được phát sinh nếu thư mục đích đã tồn tại.

   .. note::

      :func:`makedirs` sẽ bị nhầm lẫn nếu các phần tử đường dẫn cần tạo bao gồm :data:`pardir` (ví dụ: ".." trên các hệ thống UNIX).

   Hàm này xử lý chính xác các đường dẫn UNC.

   .. audit-event:: os.mkdir path,mode,dir_fd os.makedirs

   .. versionchanged:: 3.2
      Đã thêm tham số *exist_ok*.

   .. versionchanged:: 3.4.1

      Trước Python 3.4.1, nếu *exist_ok* là ``True`` và thư mục đã tồn tại,
      :func:`makedirs` vẫn sẽ phát sinh lỗi nếu *mode* không khớp với mode của thư mục hiện có. Vì không thể triển khai hành vi này một cách an toàn, nó đã bị loại bỏ trong Python 3.4.1. Xem :issue:`21082`.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.

   .. versionchanged:: 3.7
      Đối số *mode* không còn ảnh hưởng đến các bit quyền truy cập tệp của những thư mục cấp trung gian mới được tạo.


.. function:: mkfifo(path, mode=0o666, *, dir_fd=None)

   Tạo một FIFO (named pipe) có tên *path* với mode dạng số là *mode*. Giá trị umask hiện tại trước tiên sẽ được loại bỏ khỏi mode.

   Hàm này cũng hỗ trợ các :ref:`đường dẫn tương đối với bộ mô tả thư mục <dir_fd>`.

   FIFO là các pipe có thể được truy cập như các tệp thông thường. FIFO tồn tại cho đến khi bị xóa (ví dụ bằng :func:`os.unlink`). Nhìn chung, FIFO được dùng làm điểm gặp gỡ giữa các tiến trình kiểu "client" và "server": server mở FIFO để đọc, còn client mở FIFO để ghi. Lưu ý rằng :func:`mkfifo` không mở FIFO --- nó chỉ tạo điểm gặp gỡ.

   .. availability:: Unix, not WASI.

   .. versionchanged:: 3.3
      Đã thêm tham số *dir_fd*.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: mknod(path, mode=0o600, device=0, *, dir_fd=None)

   Tạo một nút hệ thống tệp (tệp, tệp thiết bị đặc biệt hoặc named pipe) có tên là *path*. *mode* chỉ định cả quyền truy cập cần sử dụng và kiểu nút cần tạo, được kết hợp (theo phép OR bit) với một trong ``stat.S_IFREG``, ``stat.S_IFCHR``, ``stat.S_IFBLK`` và ``stat.S_IFIFO`` (các hằng số đó có trong :mod:`stat`). Đối với ``stat.S_IFCHR`` và ``stat.S_IFBLK``, *device* xác định tệp thiết bị đặc biệt mới được tạo (có thể sử dụng
   :func:`os.makedev`), nếu không thì sẽ bị bỏ qua.

   Hàm này cũng hỗ trợ các :ref:`đường dẫn tương đối với bộ mô tả thư mục <dir_fd>`.

   .. availability:: Unix, not WASI.

   .. versionchanged:: 3.3
      Đã thêm tham số *dir_fd*.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: major(device, /)

   Trích xuất số major của thiết bị từ một số thiết bị thô (thường là
   hoặc trường :attr:`st_dev` hoặc :attr:`st_rdev` từ :c:struct:`stat`).


.. function:: minor(device, /)

   Trích xuất số minor của thiết bị từ một số thiết bị thô (thường là
   trường :attr:`st_dev` hoặc :attr:`st_rdev` từ :c:struct:`stat`).


.. function:: makedev(major, minor, /)

   Tạo một số thiết bị thô từ số major và số minor của thiết bị.


.. function:: pathconf(path, name)

   Trả về thông tin cấu hình hệ thống liên quan đến một tệp có tên. *name* chỉ định giá trị cấu hình cần truy xuất; đó có thể là một chuỗi chứa tên của một giá trị hệ thống đã được định nghĩa; các tên này được quy định trong một số tiêu chuẩn (POSIX.1, Unix 95, Unix 98 và các tiêu chuẩn khác). Một số nền tảng cũng định nghĩa thêm các tên khác. Các tên được hệ điều hành máy chủ nhận biết được cung cấp trong từ điển ``pathconf_names``. Đối với các biến cấu hình không có trong ánh xạ đó, cũng có thể truyền một số nguyên cho *name*.

   Nếu *name* là một chuỗi nhưng không được nhận biết, :exc:`ValueError` sẽ được phát sinh. Nếu một giá trị cụ thể cho *name* không được hệ thống máy chủ hỗ trợ, ngay cả khi giá trị đó có trong ``pathconf_names``, một :exc:`OSError` sẽ được phát sinh cùng với
   :const:`errno.EINVAL` cho số lỗi.

   Hàm này có thể hỗ trợ :ref:`chỉ định một file descriptor <path_fd>`.

   .. availability:: Unix.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. data:: pathconf_names

   Từ điển ánh xạ các tên được :func:`pathconf` và :func:`fpathconf` chấp nhận sang các giá trị số nguyên được hệ điều hành máy chủ định nghĩa cho những tên đó. Có thể sử dụng từ điển này để xác định tập hợp các tên mà hệ thống nhận biết.

   .. availability:: Unix.


.. function:: readlink(path, *, dir_fd=None)

   Trả về một chuỗi biểu diễn đường dẫn mà liên kết tượng trưng trỏ tới. Kết quả có thể là tên đường dẫn tuyệt đối hoặc tương đối; nếu là tương đối, có thể chuyển đổi thành tên đường dẫn tuyệt đối bằng ``os.path.join(os.path.dirname(path), result)``.

   Nếu *đường dẫn* là một đối tượng chuỗi (trực tiếp hoặc gián tiếp thông qua một
   :class:`PathLike` interface), kết quả cũng sẽ là một đối tượng chuỗi và lệnh gọi có thể phát sinh UnicodeDecodeError. Nếu *đường dẫn* là một đối tượng bytes (trực tiếp hoặc gián tiếp), kết quả sẽ là một đối tượng bytes.

   Hàm này cũng hỗ trợ các :ref:`đường dẫn tương đối với bộ mô tả thư mục <dir_fd>`.

   Khi cố gắng phân giải một đường dẫn có thể chứa các liên kết, hãy sử dụng
   :func:`~os.path.realpath` để xử lý đúng việc đệ quy và sự khác biệt giữa các nền tảng.

   .. availability:: Unix, Windows.

   .. versionchanged:: 3.2
      Đã bổ sung hỗ trợ symbolic link trên Windows 6.0 (Vista).

   .. versionchanged:: 3.3
      Đã thêm tham số *dir_fd*.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object` trên Unix.

   .. versionchanged:: 3.8
      Chấp nhận một :term:`path-like object` và một đối tượng bytes trên Windows.

      Đã bổ sung hỗ trợ cho các junction của thư mục và thay đổi để trả về đường dẫn thay thế (thường bao gồm tiền tố ``\\?\``) thay vì trường "print name" tùy chọn được trả về trước đây.

.. function:: remove(path, *, dir_fd=None)

   Xóa (xóa bỏ) tệp *path*. Nếu *path* là một thư mục, một
   :exc:`OSError` sẽ được phát sinh. Sử dụng :func:`rmdir` để xóa các thư mục. Nếu tệp không tồn tại, một :exc:`FileNotFoundError` sẽ được phát sinh.

   Hàm này hỗ trợ :ref:`paths relative to directory descriptors <dir_fd>`.

   Trên Windows, việc cố gắng xóa một tệp đang được sử dụng sẽ khiến một exception được phát sinh; trên Unix, mục nhập thư mục sẽ bị xóa nhưng phần dung lượng lưu trữ được cấp phát cho tệp sẽ chưa được giải phóng cho đến khi tệp ban đầu không còn được sử dụng.

   Về mặt ngữ nghĩa, hàm này tương đương với :func:`unlink`.

   .. audit-event:: os.remove path,dir_fd os.remove

   .. versionchanged:: 3.3
      Đã thêm tham số *dir_fd*.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: removedirs(name)

   .. index:: single: directory; deleting

   Xóa đệ quy các thư mục. Hoạt động giống như :func:`rmdir`, ngoại trừ việc nếu thư mục lá được xóa thành công, :func:`removedirs` sẽ lần lượt cố gắng xóa mọi thư mục cha được đề cập trong *path* cho đến khi phát sinh lỗi (lỗi này bị bỏ qua vì nhìn chung có nghĩa là một thư mục cha không trống). Ví dụ, ``os.removedirs('foo/bar/baz')`` trước tiên sẽ xóa thư mục ``'foo/bar/baz'``, sau đó xóa ``'foo/bar'`` và ``'foo'`` nếu chúng trống. Phát sinh :exc:`OSError` nếu không thể xóa thành công thư mục lá.

   .. audit-event:: os.remove path,dir_fd os.removedirs

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: rename(src, dst, *, src_dir_fd=None, dst_dir_fd=None)

   Đổi tên tệp hoặc thư mục *src* thành *dst*. Nếu *dst* tồn tại, thao tác sẽ thất bại với một lớp con của :exc:`OSError` trong một số trường hợp:

   Trên Windows, nếu *dst* tồn tại, :exc:`FileExistsError` luôn được phát sinh. Thao tác có thể thất bại nếu *src* và *dst* nằm trên các filesystem khác nhau. Sử dụng
   :func:`shutil.move` để hỗ trợ việc di chuyển sang một filesystem khác.

   Trên Unix, nếu *src* là một tệp còn *dst* là một thư mục hoặc ngược lại, một
   :exc:`IsADirectoryError` hoặc :exc:`NotADirectoryError` sẽ lần lượt được phát sinh. Nếu cả hai đều là thư mục và *dst* trống, *dst* sẽ được thay thế mà không thông báo. Nếu *dst* là một thư mục không trống, một :exc:`OSError` sẽ được phát sinh. Nếu cả hai đều là tệp, *dst* sẽ được thay thế mà không thông báo nếu người dùng có quyền. Thao tác có thể thất bại trên một số biến thể Unix nếu *src* và *dst* nằm trên các filesystem khác nhau. Nếu thành công, việc đổi tên sẽ là một thao tác nguyên tử (đây là yêu cầu của POSIX).

   Hàm này hỗ trợ chỉ định *src_dir_fd* và/hoặc *dst_dir_fd* để cung cấp :ref:`các đường dẫn tương đối với bộ mô tả thư mục <dir_fd>`.

   Nếu bạn muốn ghi đè đích trên nhiều nền tảng, hãy sử dụng :func:`replace`.

   .. audit-event:: os.rename src,dst,src_dir_fd,dst_dir_fd os.rename

   .. versionchanged:: 3.3
      Đã thêm các tham số *src_dir_fd* và *dst_dir_fd*.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object` cho *src* và *dst*.


.. function:: renames(old, new)

   Hàm đổi tên đệ quy thư mục hoặc tệp. Hoạt động giống như :func:`rename`, ngoại trừ việc trước tiên hàm sẽ thử tạo mọi thư mục trung gian cần thiết để pathname mới hợp lệ. Sau khi đổi tên, các thư mục tương ứng với những phần đường dẫn ở bên phải cùng của tên cũ sẽ được loại bỏ bằng :func:`removedirs`.

   .. note::

      Hàm này có thể không thành công với cấu trúc thư mục mới đã được tạo nếu bạn không có quyền cần thiết để xóa thư mục lá hoặc tệp.

   .. audit-event:: os.rename src,dst,src_dir_fd,dst_dir_fd os.renames

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object` cho *old* và *new*.


.. function:: replace(src, dst, *, src_dir_fd=None, dst_dir_fd=None)

   Đổi tên tệp hoặc thư mục *src* thành *dst*.  Nếu *dst* là một thư mục không rỗng,
   :exc:`OSError` sẽ được phát sinh.  Nếu *dst* tồn tại và là một tệp, tệp đó sẽ được thay thế một cách im lặng nếu người dùng có quyền.  Thao tác có thể thất bại nếu *src* và *dst* nằm trên các hệ thống tệp khác nhau.  Nếu thành công, việc đổi tên sẽ là một thao tác nguyên tử (đây là yêu cầu của POSIX).

   Hàm này hỗ trợ chỉ định *src_dir_fd* và/hoặc *dst_dir_fd* để cung cấp :ref:`các đường dẫn tương đối với bộ mô tả thư mục <dir_fd>`.

   .. audit-event:: os.rename src,dst,src_dir_fd,dst_dir_fd os.replace

   .. versionadded:: 3.3

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object` cho *src* và *dst*.


.. function:: rmdir(path, *, dir_fd=None)

   Xóa (remove) thư mục *path*.  Nếu thư mục không tồn tại hoặc không rỗng, lần lượt một :exc:`FileNotFoundError` hoặc một :exc:`OSError` sẽ được phát sinh.  Để xóa toàn bộ cây thư mục,
   có thể sử dụng :func:`shutil.rmtree`.

   Hàm này hỗ trợ :ref:`paths relative to directory descriptors <dir_fd>`.

   .. audit-event:: os.rmdir path,dir_fd os.rmdir

   .. versionchanged:: 3.3
      Đã thêm tham số *dir_fd*.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: scandir(path='.')

   Trả về một iterator gồm các đối tượng :class:`os.DirEntry` tương ứng với các mục trong thư mục được chỉ định bởi *path*. Các mục được trả về theo thứ tự tùy ý và không bao gồm các mục đặc biệt ``'.'`` và ``'..'``. Nếu một tệp bị xóa khỏi hoặc được thêm vào thư mục sau khi tạo iterator, việc mục tương ứng với tệp đó có được bao gồm hay không là không xác định.

   Sử dụng :func:`scandir` thay vì :func:`listdir` có thể cải thiện đáng kể hiệu năng của mã cũng cần thông tin về loại tệp hoặc thuộc tính tệp, vì các đối tượng :class:`os.DirEntry` cung cấp thông tin này nếu hệ điều hành cung cấp thông tin đó khi quét thư mục. Tất cả các phương thức :class:`os.DirEntry` có thể thực hiện một system call, nhưng
   :func:`~os.DirEntry.is_dir` và :func:`~os.DirEntry.is_file` thường chỉ cần một system call đối với symbolic link; :func:`os.DirEntry.stat` luôn cần một system call trên Unix, nhưng trên Windows chỉ cần một system call đối với symbolic link.

   *path* có thể là một :term:`path-like object`. Nếu *path* có kiểu ``bytes`` (trực tiếp hoặc gián tiếp thông qua interface :class:`PathLike`), kiểu của các thuộc tính :attr:`~os.DirEntry.name` và :attr:`~os.DirEntry.path` của mỗi :class:`os.DirEntry` sẽ là ``bytes``; trong mọi trường hợp khác, chúng sẽ có kiểu ``str``.

   Hàm này cũng hỗ trợ :ref:`chỉ định một bộ mô tả tệp <path_fd>`; bộ mô tả tệp phải tham chiếu đến một thư mục.

   .. audit-event:: os.scandir path os.scandir

   iterator :func:`scandir` hỗ trợ protocol :term:`context manager` và có phương thức sau:

   .. method:: scandir.close()

      Đóng iterator và giải phóng các tài nguyên đã thu nhận.

      Phương thức này được gọi tự động khi iterator ở trạng thái :term:`exhausted` hoặc được garbage collection, hoặc khi xảy ra lỗi trong quá trình lặp. Tuy nhiên, bạn nên gọi phương thức này một cách rõ ràng hoặc sử dụng câu lệnh :keyword:`with`.

      .. versionadded:: 3.6

   Ví dụ sau cho thấy cách sử dụng đơn giản :func:`scandir` để hiển thị tất cả các tệp (không bao gồm thư mục) trong *path* đã cho mà không bắt đầu bằng ``'.'``. Lệnh gọi ``entry.is_file()`` nhìn chung sẽ không thực hiện thêm system call nào::

      with os.scandir(path) as it:
          for entry in it:
              if not entry.name.startswith('.') and entry.is_file():
                  print(entry.name)

   .. note::

      Trên các hệ thống dựa trên Unix, :func:`scandir` sử dụng các hàm `opendir() <https://pubs.opengroup.org/onlinepubs/009695399/functions/opendir.html>`_ và `readdir() <https://pubs.opengroup.org/onlinepubs/009695399/functions/readdir_r.html>`_ của hệ thống. Trên Windows, nó sử dụng các hàm Win32 `FindFirstFileW <https://msdn.microsoft.com/en-us/library/windows/desktop/aa364418(v=vs.85).aspx>`_ và `FindNextFileW <https://msdn.microsoft.com/en-us/library/windows/desktop/aa364428(v=vs.85).aspx>`_.

   .. versionadded:: 3.5

   .. versionchanged:: 3.6
      Đã bổ sung hỗ trợ cho protocol :term:`context manager` và
      phương thức :func:`~scandir.close`. Nếu một iterator :func:`scandir` chưa được duyệt hết cũng chưa được đóng một cách rõ ràng, một :exc:`ResourceWarning` sẽ được phát ra trong destructor của nó.

      Hàm này chấp nhận một :term:`path-like object`.

   .. versionchanged:: 3.7
      Đã bổ sung hỗ trợ cho :ref:`bộ mô tả tệp <path_fd>` trên Unix.


.. class:: DirEntry

   Đối tượng được :func:`scandir` trả về để cung cấp đường dẫn tệp và các thuộc tính tệp khác của một mục nhập thư mục.

   :func:`scandir` sẽ cung cấp nhiều thông tin nhất có thể mà không thực hiện thêm các lệnh gọi hệ thống. Khi thực hiện lệnh gọi hệ thống ``stat()`` hoặc ``lstat()``, đối tượng ``os.DirEntry`` sẽ lưu kết quả vào bộ nhớ đệm.

   Các thực thể ``os.DirEntry`` không được thiết kế để lưu trữ trong các cấu trúc dữ liệu tồn tại lâu dài; nếu biết siêu dữ liệu tệp đã thay đổi hoặc đã một khoảng thời gian dài kể từ khi gọi :func:`scandir`, hãy gọi ``os.stat(entry.path)`` để lấy thông tin mới nhất.

   Vì các phương thức ``os.DirEntry`` có thể thực hiện các lệnh gọi đến hệ điều hành, chúng cũng có thể phát sinh :exc:`OSError`. Nếu cần kiểm soát lỗi thật chi tiết, bạn có thể bắt :exc:`OSError` khi gọi một trong các phương thức ``os.DirEntry`` và xử lý cho phù hợp.

   Để có thể được sử dụng trực tiếp như một :term:`path-like object`, ``os.DirEntry`` triển khai giao diện :class:`PathLike`.

   Các đối tượng :class:`!DirEntry` là :ref:`generic <generics>` theo kiểu của path (:class:`str` hoặc :class:`bytes`).

   Các thuộc tính và phương thức trên một thực thể ``os.DirEntry`` như sau:

   .. attribute:: name

      Tên tệp cơ sở của mục nhập, tương đối so với đối số :func:`scandir` *path*.

      Thuộc tính :attr:`name` sẽ là ``bytes`` nếu đối số :func:`scandir` *path* thuộc kiểu ``bytes`` và ``str`` nếu không. Sử dụng
      :func:`~os.fsdecode` để giải mã tên tệp dạng byte.

   .. attribute:: path

      Tên đường dẫn của mục nhập: tương đương với ``os.path.join(scandir_path, entry.name)`` trong đó *scandir_path* là đối số :func:`scandir` *path* ban đầu. Ngoài tên tệp, đường dẫn giữ nguyên đối số :func:`scandir` ban đầu. Nếu đối số :func:`scandir` *path* là đường dẫn tương đối, thuộc tính :attr:`path` cũng là đường dẫn tương đối. Việc thay đổi thư mục làm việc hiện tại sau khi tạo
      bộ lặp :func:`scandir` có thể khiến các lần sử dụng sau này của :attr:`path` được phân giải khác đi. Trên một số nền tảng, đường dẫn được tạo có thể không hợp lệ nếu đối số :func:`scandir` ban đầu có thể dùng để liệt kê nhưng không thể dùng để ghép với tên mục nhập. Nếu đối số :func:`scandir` *path* là một :ref:`file descriptor <path_fd>`, thuộc tính :attr:`path` giống với thuộc tính :attr:`name`.

      Thuộc tính :attr:`path` sẽ là ``bytes`` nếu đối số :func:`scandir` *path* có kiểu ``bytes`` và ``str`` nếu không. Sử dụng
      :func:`~os.fsdecode` để giải mã tên tệp dạng byte.

   .. method:: inode()

      Trả về số inode của mục nhập.

      Kết quả được lưu vào bộ nhớ đệm trên đối tượng ``os.DirEntry``. Sử dụng ``os.stat(entry.path, follow_symlinks=False).st_ino`` để lấy thông tin mới nhất.

      Trong lần gọi đầu tiên, khi chưa có dữ liệu trong bộ nhớ đệm, cần thực hiện system call trên Windows nhưng không cần trên Unix.

   .. method:: is_dir(*, follow_symlinks=True)

      Trả về ``True`` nếu mục nhập này là một thư mục hoặc là một symbolic link trỏ đến một thư mục; trả về ``False`` nếu mục nhập là hoặc trỏ đến bất kỳ loại tệp nào khác, hoặc nếu mục nhập không còn tồn tại.

      Nếu *follow_symlinks* là ``False``, chỉ trả về ``True`` nếu mục nhập này là một thư mục (không đi theo symbolic link); trả về ``False`` nếu mục nhập là bất kỳ loại tệp nào khác hoặc nếu mục nhập không còn tồn tại.

      Kết quả được lưu vào bộ nhớ đệm trên đối tượng ``os.DirEntry``, với một bộ nhớ đệm riêng cho *follow_symlinks* ``True`` và ``False``. Gọi :func:`os.stat` cùng với :func:`stat.S_ISDIR` để lấy thông tin mới nhất.

      Trong lần gọi đầu tiên, khi chưa có dữ liệu trong bộ nhớ đệm, hầu hết trường hợp không cần thực hiện lời gọi hệ thống. Cụ thể, đối với các mục không phải liên kết tượng trưng, cả Windows và Unix đều không yêu cầu lời gọi hệ thống, ngoại trừ một số hệ thống tệp Unix, chẳng hạn như hệ thống tệp mạng, trả về ``dirent.d_type == DT_UNKNOWN``. Nếu mục là một liên kết tượng trưng, cần thực hiện lời gọi hệ thống để theo liên kết tượng trưng, trừ khi *follow_symlinks* là ``False``.

      Phương thức này có thể phát sinh :exc:`OSError`, chẳng hạn như :exc:`PermissionError`, nhưng :exc:`FileNotFoundError` được bắt và không được phát sinh lại.

   .. method:: is_file(*, follow_symlinks=True)

      Trả về ``True`` nếu mục này là một tệp hoặc là một liên kết tượng trưng trỏ đến một tệp; trả về ``False`` nếu mục này là hoặc trỏ đến một thư mục hay mục không phải tệp khác, hoặc nếu mục đó không còn tồn tại.

      Nếu *follow_symlinks* là ``False``, chỉ trả về ``True`` nếu mục này là một tệp (không theo liên kết tượng trưng); trả về ``False`` nếu mục này là một thư mục hoặc mục không phải tệp khác, hoặc nếu mục đó không còn tồn tại.

      Kết quả được lưu vào bộ nhớ đệm trên đối tượng ``os.DirEntry``. Việc lưu vào bộ nhớ đệm, các lời gọi hệ thống được thực hiện và các ngoại lệ phát sinh tuân theo :func:`~os.DirEntry.is_dir`.

   .. method:: is_symlink()

      Trả về ``True`` nếu mục này là một liên kết tượng trưng (kể cả khi liên kết bị hỏng); trả về ``False`` nếu mục này trỏ đến một thư mục hoặc bất kỳ loại tệp nào, hoặc nếu mục đó không còn tồn tại.

      Kết quả được lưu vào bộ nhớ đệm trên đối tượng ``os.DirEntry``. Gọi
      :func:`os.path.islink` để lấy thông tin mới nhất.

      Trong lần gọi đầu tiên, khi chưa có dữ liệu trong bộ nhớ đệm, hầu hết trường hợp không cần thực hiện lời gọi hệ thống. Cụ thể, cả Windows và Unix đều không cần lời gọi hệ thống, ngoại trừ một số hệ thống tệp Unix nhất định, chẳng hạn như hệ thống tệp mạng, trả về ``dirent.d_type == DT_UNKNOWN``.

      Phương thức này có thể phát sinh :exc:`OSError`, chẳng hạn như :exc:`PermissionError`, nhưng :exc:`FileNotFoundError` được bắt và không được phát sinh lại.

   .. method:: is_junction()

      Trả về ``True`` nếu mục này là junction (ngay cả khi junction bị hỏng); trả về ``False`` nếu mục trỏ đến một thư mục thông thường, bất kỳ loại tệp nào, một symlink hoặc nếu mục đó không còn tồn tại.

      Kết quả được lưu vào bộ nhớ đệm trên đối tượng ``os.DirEntry``. Gọi
      :func:`os.path.isjunction` để lấy thông tin mới nhất.

      .. versionadded:: 3.12

   .. method:: stat(*, follow_symlinks=True)

      Trả về một đối tượng :class:`stat_result` cho mục nhập này. Theo mặc định, phương thức này đi theo các liên kết tượng trưng; để lấy thông tin của một liên kết tượng trưng, hãy thêm đối số ``follow_symlinks=False``.

      Trên Unix, phương thức này luôn yêu cầu một system call. Trên Windows, phương thức này chỉ yêu cầu một system call nếu *follow_symlinks* là ``True`` và mục nhập là một reparse point (ví dụ: liên kết tượng trưng hoặc junction thư mục).

      Trên Windows, các thuộc tính ``st_ino``, ``st_dev`` và ``st_nlink`` của
      :class:`stat_result` luôn được đặt thành số không. Gọi :func:`os.stat` để lấy các thuộc tính này.

      Kết quả được lưu vào bộ nhớ đệm trên đối tượng ``os.DirEntry``, với một bộ đệm riêng cho *follow_symlinks* ``True`` và ``False``. Gọi :func:`os.stat` để lấy thông tin mới nhất.

   Lưu ý rằng có sự tương ứng khá rõ ràng giữa một số thuộc tính và phương thức của ``os.DirEntry`` với các thuộc tính và phương thức của :class:`pathlib.Path`. Cụ thể, thuộc tính ``name`` có cùng ý nghĩa, cũng như các phương thức ``is_dir()``, ``is_file()``, ``is_symlink()``, ``is_junction()`` và ``stat()``.

   .. versionadded:: 3.5

   .. versionchanged:: 3.6
      Đã bổ sung hỗ trợ cho interface :class:`~os.PathLike`. Đã bổ sung hỗ trợ cho các đường dẫn :class:`bytes` trên Windows.

   .. versionchanged:: 3.12
      Thuộc tính ``st_ctime`` của kết quả stat không được dùng nữa trên Windows. Thời gian tạo tệp được cung cấp đúng cách dưới dạng ``st_birthtime``, và trong tương lai ``st_ctime`` có thể được thay đổi để trả về giá trị bằng 0 hoặc thời gian thay đổi metadata, nếu có.


.. function:: stat(path, *, dir_fd=None, follow_symlinks=True)

   Lấy trạng thái của một tệp hoặc file descriptor. Thực hiện tương đương một
   lời gọi hệ thống :c:func:`stat` trên đường dẫn đã cho. *path* có thể được chỉ định dưới dạng chuỗi hoặc bytes -- trực tiếp hoặc gián tiếp thông qua giao diện :class:`PathLike` -- hoặc dưới dạng file descriptor đang mở. Trả về một đối tượng :class:`stat_result`.

   Hàm này thường đi theo các symlink; để stat một symlink, hãy thêm đối số ``follow_symlinks=False``, hoặc sử dụng :func:`lstat`.

   Hàm này có thể hỗ trợ :ref:`việc chỉ định một file descriptor <path_fd>` và
   :ref:`không đi theo các symlink <follow_symlinks>`.

   Trên Windows, truyền ``follow_symlinks=False`` sẽ vô hiệu hóa việc đi theo tất cả name-surrogate reparse point, bao gồm symlink và directory junction. Các loại reparse point khác không giống liên kết hoặc không thể được hệ điều hành đi theo sẽ được mở trực tiếp. Khi đi theo một chuỗi gồm nhiều liên kết, điều này có thể khiến liên kết ban đầu được trả về thay vì đối tượng không phải liên kết đã ngăn việc duyệt hết chuỗi. Để lấy kết quả stat cho đường dẫn cuối cùng trong trường hợp này, hãy sử dụng
   Hàm :func:`os.path.realpath` để phân giải tên đường dẫn nhiều nhất có thể và gọi :func:`lstat` trên kết quả. Điều này không áp dụng cho các symbolic link hoặc junction point bị treo, vốn sẽ gây ra các ngoại lệ thông thường.

   .. index:: pair: module; stat

   Ví dụ::

      >>> import os
      >>> statinfo = os.stat('somefile.txt')
      >>> statinfo
      os.stat_result(st_mode=33188, st_ino=7876932, st_dev=234881026,
      st_nlink=1, st_uid=501, st_gid=501, st_size=264, st_atime=1297230295,
      st_mtime=1297230027, st_ctime=1297230027)
      >>> statinfo.st_size
      264

   .. seealso::

      Các hàm :func:`fstat` và :func:`lstat`.

   .. versionchanged:: 3.3
      Đã thêm các tham số *dir_fd* và *follow_symlinks*, dùng để chỉ định file descriptor thay vì đường dẫn.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.

   .. versionchanged:: 3.8
      Trên Windows, giờ đây tất cả reparse point có thể được hệ điều hành phân giải đều sẽ được theo sau, và việc truyền ``follow_symlinks=False`` sẽ vô hiệu hóa việc theo sau tất cả name surrogate reparse point. Nếu hệ điều hành gặp một reparse point mà nó không thể theo sau, *stat* giờ đây sẽ trả về thông tin của đường dẫn ban đầu, như thể ``follow_symlinks=False`` đã được chỉ định, thay vì gây ra lỗi.


.. class:: stat_result

   Đối tượng có các thuộc tính tương ứng gần đúng với các thành phần của
   :c:struct:`stat` cấu trúc. Nó được dùng cho kết quả của :func:`os.stat`,
   :func:`os.fstat` và :func:`os.lstat`.

   Các thuộc tính:

   .. attribute:: st_mode

      Chế độ tệp: loại tệp và các bit chế độ tệp (quyền).

   .. attribute:: st_ino

      Phụ thuộc vào nền tảng, nhưng nếu khác không thì sẽ xác định duy nhất tệp cho một giá trị ``st_dev``. Thông thường:

      * số inode trên Unix,
      * `chỉ mục tệp <https://msdn.microsoft.com/en-us/library/aa363788>`_ trên Windows

   .. attribute:: st_dev

      Mã định danh của thiết bị nơi tệp này nằm.

   .. attribute:: st_nlink

      Số lượng hard link.

   .. attribute:: st_uid

      Mã định danh người dùng của chủ sở hữu tệp.

   .. attribute:: st_gid

      Mã định danh nhóm của chủ sở hữu tệp.

   .. attribute:: st_size

      Kích thước của tệp tính bằng byte, nếu đó là tệp thông thường hoặc symbolic link. Kích thước của symbolic link là độ dài của pathname mà nó chứa, không bao gồm byte null kết thúc.

   Dấu thời gian:

   .. attribute:: st_atime

      Thời điểm truy cập gần đây nhất, được biểu thị bằng giây.

   .. attribute:: st_mtime

      Thời điểm sửa đổi nội dung gần đây nhất, được biểu thị bằng giây.

   .. attribute:: st_ctime

      Thời điểm thay đổi siêu dữ liệu gần đây nhất, được biểu thị bằng giây.

      .. versionchanged:: 3.12
         ``st_ctime`` không được khuyến nghị sử dụng trên Windows. Hãy dùng ``st_birthtime`` cho thời điểm tạo tệp. Trong tương lai, ``st_ctime`` sẽ chứa thời điểm thay đổi siêu dữ liệu gần đây nhất, như trên các nền tảng khác.

   .. attribute:: st_atime_ns

      Thời điểm truy cập gần đây nhất, được biểu thị dưới dạng số nguyên tính bằng nano giây.

      .. versionadded:: 3.3

   .. attribute:: st_mtime_ns

      Thời điểm sửa đổi nội dung gần đây nhất, được biểu thị dưới dạng số nguyên tính bằng nano giây.

      .. versionadded:: 3.3

   .. attribute:: st_ctime_ns

      Thời điểm thay đổi siêu dữ liệu gần đây nhất, được biểu thị dưới dạng số nguyên tính bằng nano giây.

      .. versionadded:: 3.3

      .. versionchanged:: 3.12
         ``st_ctime_ns`` không được khuyến nghị sử dụng trên Windows. Hãy dùng ``st_birthtime_ns`` cho thời điểm tạo tệp. Trong tương lai, ``st_ctime`` sẽ chứa thời điểm thay đổi siêu dữ liệu gần đây nhất, như trên các nền tảng khác.

   .. attribute:: st_birthtime

      Thời điểm tạo tệp được biểu thị bằng giây. Thuộc tính này không phải lúc nào cũng có sẵn và có thể gây ra :exc:`AttributeError`.

      .. versionchanged:: 3.12
         ``st_birthtime`` hiện đã có sẵn trên Windows.

   .. attribute:: st_birthtime_ns

      Thời điểm tạo tệp được biểu thị bằng nano giây dưới dạng số nguyên. Thuộc tính này không phải lúc nào cũng có sẵn và có thể gây ra
      :exc:`AttributeError`.

      .. versionadded:: 3.12

   .. note::

      Ý nghĩa chính xác và độ phân giải của :attr:`st_atime`,
      các thuộc tính :attr:`st_mtime`, :attr:`st_ctime` và :attr:`st_birthtime` phụ thuộc vào hệ điều hành và hệ thống tệp. Ví dụ, trên các hệ thống Windows sử dụng hệ thống tệp FAT32, :attr:`st_mtime` có độ phân giải 2 giây, còn :attr:`st_atime` chỉ có độ phân giải 1 ngày. Hãy xem tài liệu về hệ điều hành của bạn để biết chi tiết.

      Tương tự, mặc dù :attr:`st_atime_ns`, :attr:`st_mtime_ns`,
      :attr:`st_ctime_ns` và :attr:`st_birthtime_ns` luôn được biểu thị bằng nano giây, nhiều hệ thống không cung cấp độ chính xác đến nano giây. Trên các hệ thống có cung cấp độ chính xác đến nano giây, đối tượng dấu phẩy động được dùng để lưu trữ :attr:`st_atime`, :attr:`st_mtime`, :attr:`st_ctime` và
      :attr:`st_birthtime` không thể bảo toàn toàn bộ thông tin đó, vì vậy kết quả sẽ có sai lệch đôi chút. Nếu cần dấu thời gian chính xác, bạn luôn nên sử dụng
      :attr:`st_atime_ns`, :attr:`st_mtime_ns`, :attr:`st_ctime_ns` và
      :attr:`st_birthtime_ns`.

   Trên một số hệ thống Unix (chẳng hạn như Linux), các thuộc tính sau đây cũng có thể khả dụng:

   .. attribute:: st_blocks

      Số lượng block 512 byte được cấp phát cho tệp. Giá trị này có thể nhỏ hơn :attr:`st_size`/512 khi tệp có các lỗ trống.

   .. attribute:: st_blksize

      Kích thước block "ưu tiên" để hệ thống tệp thực hiện I/O hiệu quả. Việc ghi tệp theo các phần nhỏ hơn có thể gây ra thao tác đọc-sửa-ghi lại kém hiệu quả.

   .. attribute:: st_rdev

      Loại thiết bị nếu inode là một thiết bị.

   .. attribute:: st_flags

      Các cờ do người dùng định nghĩa cho tệp.

   Trên các hệ thống Unix khác (chẳng hạn như FreeBSD), các thuộc tính sau có thể khả dụng (nhưng có thể chỉ được điền nếu root cố gắng sử dụng chúng):

   .. attribute:: st_gen

      Số thế hệ của tệp.

   Trên Solaris và các hệ dẫn xuất, các thuộc tính sau cũng có thể khả dụng:

   .. attribute:: st_fstype

      Chuỗi nhận dạng duy nhất loại hệ thống tệp chứa tệp.

   Trên các hệ thống macOS, các thuộc tính sau cũng có thể khả dụng:

   .. attribute:: st_rsize

      Kích thước thực của tệp.

   .. attribute:: st_creator

      Tác giả tạo tệp.

   .. attribute:: st_type

      Loại tệp.

   Trên các hệ thống Windows, các thuộc tính sau cũng khả dụng:

   .. attribute:: st_file_attributes

      Các thuộc tính tệp Windows: ``dwFileAttributes`` là thành viên của cấu trúc ``BY_HANDLE_FILE_INFORMATION`` được trả về bởi
      :c:func:`!GetFileInformationByHandle`. Xem các hằng số :const:`!FILE_ATTRIBUTE_* <stat.FILE_ATTRIBUTE_ARCHIVE>` trong mô-đun :mod:`stat`.

      .. versionadded:: 3.5

   .. attribute:: st_reparse_tag

      Khi :attr:`st_file_attributes` được đặt :const:`~stat.FILE_ATTRIBUTE_REPARSE_POINT`, trường này chứa thẻ xác định loại reparse point. Xem các hằng số :const:`IO_REPARSE_TAG_* <stat.IO_REPARSE_TAG_SYMLINK>` trong mô-đun :mod:`stat`.

   Mô-đun chuẩn :mod:`stat` định nghĩa các hàm và hằng số hữu ích để trích xuất thông tin từ cấu trúc :c:struct:`stat`. (Trên Windows, một số mục được điền bằng các giá trị giả.)

   Để tương thích ngược, một thực thể :class:`stat_result` cũng có thể được truy cập dưới dạng một tuple gồm ít nhất 10 số nguyên, cung cấp các thành viên quan trọng nhất (và có tính khả chuyển) của cấu trúc :c:struct:`stat`, theo thứ tự
   :attr:`st_mode`, :attr:`st_ino`, :attr:`st_dev`, :attr:`st_nlink`,
   :attr:`st_uid`, :attr:`st_gid`, :attr:`st_size`, :attr:`st_atime`,
   :attr:`st_mtime`, :attr:`st_ctime`. Một số bản triển khai có thể thêm các mục khác vào cuối. Để tương thích với các phiên bản Python cũ hơn, việc truy cập :class:`stat_result` dưới dạng tuple luôn trả về các số nguyên.

   .. versionchanged:: 3.5
      Windows hiện trả về chỉ mục tệp dưới dạng :attr:`st_ino` khi có sẵn.

   .. versionchanged:: 3.7
      Đã thêm thành viên :attr:`st_fstype` vào Solaris/các hệ dẫn xuất.

   .. versionchanged:: 3.8
      Đã thêm thành viên :attr:`st_reparse_tag` trên Windows.

   .. versionchanged:: 3.8
      Trên Windows, thành viên :attr:`st_mode` hiện xác định các tệp đặc biệt là :const:`S_IFCHR`, :const:`S_IFIFO` hoặc :const:`S_IFBLK` tùy trường hợp.

   .. versionchanged:: 3.12
      Trên Windows, :attr:`st_ctime` hiện đã lỗi thời. Cuối cùng, nó sẽ chứa thời điểm thay đổi metadata gần nhất để nhất quán với các nền tảng khác, nhưng hiện tại vẫn chứa thời điểm tạo. Hãy sử dụng :attr:`st_birthtime` cho thời điểm tạo.

      Trên Windows, :attr:`st_ino` hiện có thể lên đến 128 bit, tùy thuộc vào hệ thống tệp. Trước đây, giá trị này không vượt quá 64 bit và các mã định danh tệp lớn hơn sẽ được đóng gói một cách tùy ý.

      Trên Windows, :attr:`st_rdev` không còn trả về giá trị. Trước đây, nó chứa giá trị giống với :attr:`st_dev`, điều này là không chính xác.

      Đã thêm member :attr:`st_birthtime` trên Windows.


.. function:: statvfs(path)

   Thực hiện system call :manpage:`statvfs(3)` trên path đã cho. Giá trị trả về là một :class:`statvfs_result` có các thuộc tính mô tả filesystem trên path đã cho và tương ứng với các member của cấu trúc :c:struct:`statvfs`.

   Hàm này có thể hỗ trợ :ref:`chỉ định một file descriptor <path_fd>`.

   .. availability:: Unix.

   .. versionchanged:: 3.3
      Đã thêm hỗ trợ chỉ định *path* dưới dạng một file descriptor đang mở.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. class:: statvfs_result

   Các thống kê filesystem được :func:`os.statvfs` và :func:`os.fstatvfs` trả về. Xem :manpage:`statvfs(3)` để biết thêm chi tiết.

   .. attribute:: f_bsize

      Kích thước block.

   .. attribute:: f_frsize

      Kích thước fragment.

   .. attribute:: f_blocks

      Số lượng block có kích thước :attr:`~statvfs_result.f_frsize` mà hệ thống tệp có thể chứa.

   .. attribute:: f_bfree

      Số lượng block trống.

   .. attribute:: f_bavail

      Số lượng block trống dành cho người dùng không có đặc quyền.

   .. attribute:: f_files

      Số lượng mục nhập tệp (inode) mà hệ thống tệp có thể chứa.

   .. attribute:: f_ffree

      Số lượng mục nhập tệp trống.

   .. attribute:: f_favail

      Số mục tệp miễn phí dành cho người dùng không có đặc quyền.

   .. attribute:: f_flag

      Bit-mask của các cờ mount. Các cờ sau được định nghĩa:
      :data:`ST_RDONLY`, :data:`ST_NOSUID`, :data:`ST_NODEV`,
      :data:`ST_NOEXEC`, :data:`ST_SYNCHRONOUS`, :data:`ST_MANDLOCK`,
      :data:`ST_WRITE`, :data:`ST_APPEND`, :data:`ST_IMMUTABLE`,
      :data:`ST_NOATIME`, :data:`ST_NODIRATIME`, và :data:`ST_RELATIME`.

   .. attribute:: f_namemax

      Độ dài tên tệp tối đa của filesystem. Các giới hạn riêng theo hệ điều hành như
      :ref:`Windows MAX_PATH <max-path>` và các giới hạn được mô tả trong Linux
      :manpage:`pathname(7)` có thể tồn tại.

   .. attribute:: f_fsid

      ID của filesystem.

      .. versionadded:: 3.7


Các cờ sau được sử dụng trong :attr:`statvfs_result.f_flag`.

.. data:: ST_RDONLY

   Hệ thống tệp chỉ đọc.

   .. versionadded:: 3.2

.. data:: ST_NOSUID

   Các bit setuid/setgid bị tắt hoặc không được hỗ trợ.

   .. versionadded:: 3.2

.. data:: ST_NODEV

   Không cho phép truy cập các tệp đặc biệt của thiết bị.

   .. availability:: Linux.

   .. versionadded:: 3.4

.. data:: ST_NOEXEC

   Không cho phép thực thi chương trình.

   .. availability:: Linux.

   .. versionadded:: 3.4

.. data:: ST_SYNCHRONOUS

   Các thao tác ghi được đồng bộ ngay lập tức.

   .. availability:: Linux.

   .. versionadded:: 3.4

.. data:: ST_MANDLOCK

   Cho phép khóa bắt buộc trên một FS.

   .. availability:: Linux.

   .. versionadded:: 3.4

.. data:: ST_WRITE

   Ghi vào tệp/thư mục/liên kết tượng trưng.

   .. availability:: Linux.

   .. versionadded:: 3.4

.. data:: ST_APPEND

   Tệp chỉ cho phép nối thêm.

   .. availability:: Linux.

   .. versionadded:: 3.4

.. data:: ST_IMMUTABLE

   Tệp bất biến.

   .. availability:: Linux.

   .. versionadded:: 3.4

.. data:: ST_NOATIME

   Không cập nhật thời gian truy cập.

   .. availability:: Linux.

   .. versionadded:: 3.4

.. data:: ST_NODIRATIME

   Không cập nhật thời gian truy cập của thư mục.

   .. availability:: Linux.

   .. versionadded:: 3.4

.. data:: ST_RELATIME

   Cập nhật atime tương đối với mtime/ctime.

   .. availability:: Linux.

   .. versionadded:: 3.4


.. data:: supports_dir_fd

   Một đối tượng :class:`set` cho biết những hàm nào trong mô-đun :mod:`!os` chấp nhận file descriptor đang mở cho tham số *dir_fd* của chúng. Các nền tảng khác nhau cung cấp những tính năng khác nhau, và chức năng nền tảng bên dưới mà Python sử dụng để triển khai tham số *dir_fd* không khả dụng trên tất cả các nền tảng mà Python hỗ trợ. Để đảm bảo tính nhất quán, các hàm có thể hỗ trợ *dir_fd* luôn cho phép chỉ định tham số này, nhưng sẽ ném ra một ngoại lệ nếu sử dụng chức năng đó khi chức năng này không khả dụng cục bộ. (Việc chỉ định ``None`` cho *dir_fd* luôn được hỗ trợ trên mọi nền tảng.)

   Để kiểm tra một hàm cụ thể có chấp nhận file descriptor đang mở cho tham số *dir_fd* hay không, hãy sử dụng toán tử ``in`` trên ``supports_dir_fd``. Ví dụ, biểu thức này cho kết quả ``True`` nếu :func:`os.stat` chấp nhận các file descriptor đang mở cho *dir_fd* trên nền tảng cục bộ::

       os.stat in os.supports_dir_fd

   Hiện tại, các tham số *dir_fd* chỉ hoạt động trên các nền tảng Unix; không tham số nào hoạt động trên Windows.

   .. versionadded:: 3.3


.. data:: supports_effective_ids

   Một đối tượng :class:`set` cho biết liệu :func:`os.access` có cho phép chỉ định ``True`` cho tham số *effective_ids* trên nền tảng cục bộ hay không. (Việc chỉ định ``False`` cho *effective_ids* luôn được hỗ trợ trên mọi nền tảng.) Nếu nền tảng cục bộ hỗ trợ, tập hợp này sẽ chứa
   :func:`os.access`; nếu không, tập hợp sẽ trống.

   Biểu thức này cho kết quả ``True`` nếu :func:`os.access` hỗ trợ ``effective_ids=True`` trên nền tảng cục bộ::

       os.access in os.supports_effective_ids

   Hiện tại, *effective_ids* chỉ được hỗ trợ trên các nền tảng Unix; nó không hoạt động trên Windows.

   .. versionadded:: 3.3


.. data:: supports_fd

   Một đối tượng :class:`set` cho biết những hàm nào trong
   Mô-đun :mod:`!os` cho phép chỉ định tham số *path* dưới dạng một file descriptor đang mở trên nền tảng cục bộ. Các nền tảng khác nhau cung cấp những tính năng khác nhau, và chức năng nền tảng mà Python sử dụng để chấp nhận các file descriptor đang mở làm đối số *path* không có trên tất cả các nền tảng được Python hỗ trợ.

   Để xác định một hàm cụ thể có cho phép chỉ định một file descriptor đang mở cho tham số *path* hay không, hãy sử dụng toán tử ``in`` trên ``supports_fd``. Ví dụ, biểu thức này cho kết quả là ``True`` nếu
   :func:`os.chdir` chấp nhận các file descriptor đang mở cho *path* trên nền tảng cục bộ của bạn::

       os.chdir in os.supports_fd

   .. versionadded:: 3.3


.. data:: supports_follow_symlinks

   Một đối tượng :class:`set` cho biết những hàm nào trong mô-đun :mod:`!os` chấp nhận ``False`` cho tham số *follow_symlinks* trên nền tảng cục bộ. Các nền tảng khác nhau cung cấp những tính năng khác nhau, và chức năng nền tảng mà Python sử dụng để triển khai *follow_symlinks* không có trên tất cả các nền tảng được Python hỗ trợ. Để nhất quán, các hàm có thể hỗ trợ *follow_symlinks* luôn cho phép chỉ định tham số này, nhưng sẽ ném ra một ngoại lệ nếu chức năng đó không khả dụng cục bộ mà vẫn được sử dụng. (Việc chỉ định ``True`` cho *follow_symlinks* luôn được hỗ trợ trên tất cả các nền tảng.)

   Để kiểm tra một hàm cụ thể có chấp nhận ``False`` cho tham số *follow_symlinks* hay không, hãy sử dụng toán tử ``in`` trên ``supports_follow_symlinks``. Ví dụ, biểu thức này cho kết quả là ``True`` nếu bạn có thể chỉ định ``follow_symlinks=False`` khi gọi
   :func:`os.stat` trên nền tảng cục bộ::

       os.stat in os.supports_follow_symlinks

   .. versionadded:: 3.3


.. function:: symlink(src, dst, target_is_directory=False, *, dir_fd=None)

   Tạo một symbolic link trỏ đến *src* có tên là *dst*.

   Tham số *src* chỉ đến đích của liên kết (tệp hoặc thư mục được liên kết đến), còn *dst* là tên của liên kết được tạo.

   Trên Windows, một symlink đại diện cho một tệp hoặc thư mục và không tự động thay đổi theo đích. Nếu đích tồn tại, loại symlink sẽ được tạo để khớp với đích. Nếu không, symlink sẽ được tạo dưới dạng thư mục nếu *target_is_directory* là ``True``, hoặc dưới dạng symlink tệp (mặc định) trong các trường hợp khác. Trên các nền tảng không phải Windows, *target_is_directory* sẽ bị bỏ qua.

   Hàm này hỗ trợ :ref:`paths relative to directory descriptors <dir_fd>`.

   .. note::

      Trên các phiên bản Windows 10 mới hơn, tài khoản không có đặc quyền có thể tạo symlink nếu Developer Mode được bật. Khi Developer Mode không khả dụng hoặc chưa được bật, cần có đặc quyền *SeCreateSymbolicLinkPrivilege*, hoặc phải chạy tiến trình với tư cách quản trị viên.


      :exc:`OSError` được phát sinh khi hàm được gọi bởi người dùng không có đặc quyền.

   .. audit-event:: os.symlink src,dst,dir_fd os.symlink

   .. availability:: Unix, Windows.

      Hàm này bị giới hạn trên WASI, xem :ref:`wasm-availability` để biết thêm thông tin.

   .. versionchanged:: 3.2
      Đã bổ sung hỗ trợ symbolic link trên Windows 6.0 (Vista).

   .. versionchanged:: 3.3
      Đã thêm tham số *dir_fd* và hiện cho phép *target_is_directory* trên các nền tảng không phải Windows.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object` cho *src* và *dst*.

   .. versionchanged:: 3.8
      Đã thêm hỗ trợ symlink không cần quyền nâng cao trên Windows khi bật Developer Mode.


.. function:: sync()

   Buộc ghi mọi thứ vào đĩa.

   .. availability:: Unix.

   .. versionadded:: 3.3


.. function:: truncate(path, length)

   Cắt ngắn tệp tương ứng với *path* để kích thước tệp không vượt quá *length* byte.

   Hàm này có thể hỗ trợ :ref:`chỉ định một file descriptor <path_fd>`.

   .. audit-event:: os.truncate path,length os.truncate

   .. availability:: Unix, Windows.

   .. versionadded:: 3.3

   .. versionchanged:: 3.5
      Đã thêm hỗ trợ cho Windows

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: unlink(path, *, dir_fd=None)

   Xóa (delete) tệp *path*. Hàm này có ngữ nghĩa giống hệt :func:`remove`; tên ``unlink`` là tên Unix truyền thống của hàm này. Vui lòng xem tài liệu về
   :func:`remove` để biết thêm thông tin.

   .. audit-event:: os.remove path,dir_fd os.unlink

   .. versionchanged:: 3.3
      Đã thêm tham số *dir_fd*.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: utime(path, times=None, *[, ns], dir_fd=None, follow_symlinks=True)

   Đặt thời gian truy cập và thời gian sửa đổi của tệp được chỉ định bởi *path*.

   :func:`utime` nhận hai tham số tùy chọn là *times* và *ns*. Các tham số này chỉ định thời gian được đặt cho *path* và được sử dụng như sau:

   - Nếu *ns* được chỉ định, nó phải là một tuple gồm 2 phần tử có dạng ``(atime_ns, mtime_ns)``, trong đó mỗi phần tử là một int biểu thị số nanosecond.
   - Nếu *times* không phải là ``None``, nó phải là một tuple gồm 2 phần tử có dạng ``(atime, mtime)``, trong đó mỗi phần tử là một int hoặc float biểu thị số giây.
   - Nếu *times* là ``None`` và *ns* không được chỉ định, điều này tương đương với việc chỉ định ``ns=(atime_ns, mtime_ns)``, trong đó cả hai thời điểm đều là thời điểm hiện tại.

   Việc chỉ định tuple cho cả *times* và *ns* sẽ gây ra lỗi.

   Lưu ý rằng các thời điểm chính xác bạn đặt ở đây có thể không được trả về bởi một lệnh gọi tiếp theo
   :func:`~os.stat` , tùy thuộc vào độ phân giải mà hệ điều hành của bạn sử dụng để ghi lại thời điểm truy cập và sửa đổi; xem :func:`~os.stat`. Cách tốt nhất để giữ nguyên các thời điểm chính xác là sử dụng các trường *st_atime_ns* và *st_mtime_ns* từ đối tượng kết quả :func:`os.stat` cùng với tham số *ns* để
   :func:`utime`.

   Hàm này có thể hỗ trợ :ref:`chỉ định một file descriptor <path_fd>`,
   :ref:`các path tương đối so với các directory descriptor <dir_fd>` và :ref:`không theo các symlink <follow_symlinks>`.

   .. audit-event:: os.utime path,times,ns,dir_fd os.utime

   .. versionchanged:: 3.3
      Đã bổ sung hỗ trợ chỉ định *path* dưới dạng một file descriptor đang mở, cùng với các tham số *dir_fd*, *follow_symlinks* và *ns*.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: walk(top, topdown=True, onerror=None, followlinks=False)

   .. index::
      single: directory; walking
      single: directory; traversal

   Tạo tên tệp trong một cây thư mục bằng cách duyệt cây theo thứ tự từ trên xuống hoặc từ dưới lên. Với mỗi thư mục trong cây có thư mục gốc là *top* (bao gồm cả chính *top*), hàm trả về một bộ 3 phần tử ``(dirpath, dirnames, filenames)``.

   *dirpath* là một chuỗi, biểu thị đường dẫn đến thư mục. *dirnames* là danh sách tên các thư mục con trong *dirpath* (bao gồm các liên kết tượng trưng đến thư mục, và không bao gồm ``'.'`` và ``'..'``). *filenames* là danh sách tên các tệp không phải thư mục trong *dirpath*. Lưu ý rằng các tên trong danh sách không chứa thành phần đường dẫn. Để lấy đường dẫn đầy đủ (bắt đầu bằng *top*) đến một tệp hoặc thư mục trong *dirpath*, hãy thực hiện ``os.path.join(dirpath, name)``. Việc các danh sách có được sắp xếp hay không tùy thuộc vào hệ thống tệp. Nếu một tệp bị xóa khỏi hoặc được thêm vào thư mục *dirpath* trong khi đang tạo các danh sách, việc tên của tệp đó có được đưa vào hay không là không xác định.

   Nếu đối số tùy chọn *topdown* là ``True`` hoặc không được chỉ định, bộ ba phần tử của một thư mục được tạo trước các bộ ba phần tử của mọi thư mục con của nó (các thư mục được tạo theo thứ tự từ trên xuống). Nếu *topdown* là ``False``, bộ ba phần tử của một thư mục được tạo sau các bộ ba phần tử của tất cả thư mục con của nó (các thư mục được tạo theo thứ tự từ dưới lên). Bất kể giá trị của *topdown* là gì, danh sách các thư mục con được truy xuất trước khi tạo các tuple cho thư mục và các thư mục con của nó.

   Khi *topdown* là ``True``, bên gọi có thể sửa đổi trực tiếp danh sách *dirnames* (có thể bằng cách sử dụng :keyword:`del` hoặc phép gán lát cắt), và :func:`walk` sẽ chỉ đệ quy vào các thư mục con có tên vẫn còn trong *dirnames*; điều này có thể được dùng để cắt tỉa phạm vi tìm kiếm, áp đặt một thứ tự duyệt cụ thể, hoặc thậm chí để thông báo
   :func:`walk` về các thư mục mà caller tạo hoặc đổi tên trước khi tiếp tục
   :func:`walk` lần nữa. Việc sửa đổi *dirnames* khi *topdown* là ``False`` không ảnh hưởng đến cách hoạt động của quá trình duyệt, vì ở chế độ từ dưới lên, các thư mục trong *dirnames* được tạo trước khi bản thân *dirpath* được tạo.

   Theo mặc định, các lỗi từ lệnh gọi :func:`scandir` sẽ bị bỏ qua. Nếu chỉ định đối số tùy chọn *onerror*, đối số này phải là một hàm; hàm sẽ được gọi với một đối số là một thực thể :exc:`OSError`. Hàm có thể báo cáo lỗi để tiếp tục quá trình duyệt, hoặc raise exception để hủy quá trình duyệt. Lưu ý rằng tên tệp có sẵn trong thuộc tính ``filename`` của đối tượng exception.

   Theo mặc định, :func:`walk` sẽ không duyệt vào các liên kết tượng trưng trỏ đến thư mục. Đặt *followlinks* thành ``True`` để truy cập các thư mục được symlink trỏ tới, trên những hệ thống hỗ trợ chúng.

   .. note::

      Lưu ý rằng việc đặt *followlinks* thành ``True`` có thể dẫn đến đệ quy vô hạn nếu một liên kết trỏ đến thư mục cha của chính nó. :func:`walk` không theo dõi các thư mục mà nó đã truy cập.

   .. note::

      Nếu truyền vào một pathname tương đối, đừng thay đổi thư mục làm việc hiện tại giữa các lần tiếp tục của :func:`walk`. :func:`walk` không bao giờ thay đổi thư mục hiện tại và giả định rằng caller của nó cũng không làm vậy.

   Ví dụ này hiển thị số byte được các tệp không phải thư mục chiếm dụng trong từng thư mục bên dưới thư mục bắt đầu, ngoại trừ việc không xem xét bên trong bất kỳ thư mục con ``__pycache__`` nào::

      import os
      from os.path import join, getsize
      for root, dirs, files in os.walk('python/Lib/xml'):
          print(root, "consumes", end=" ")
          print(sum(getsize(join(root, name)) for name in files), end=" ")
          print("bytes in", len(files), "non-directory files")
          if '__pycache__' in dirs:
              dirs.remove('__pycache__')  # không truy cập các thư mục __pycache__

   Trong ví dụ tiếp theo (triển khai đơn giản của :func:`shutil.rmtree`), việc duyệt cây từ dưới lên là rất cần thiết, :func:`rmdir` không cho phép xóa một thư mục trước khi thư mục đó rỗng::

      # Xóa mọi thứ có thể truy cập từ thư mục được chỉ định trong "top",
      # giả sử không có liên kết tượng trưng.
      # CẢNH BÁO: Việc này rất nguy hiểm! Ví dụ, nếu top == '/', nó
      # có thể xóa tất cả các tệp trên ổ đĩa của bạn.
      import os
      for root, dirs, files in os.walk(top, topdown=False):
          for name in files:
              os.remove(os.path.join(root, name))
          for name in dirs:
              os.rmdir(os.path.join(root, name))
      os.rmdir(top)

   .. audit-event:: os.walk top,topdown,onerror,followlinks os.walk

   .. versionchanged:: 3.5
      Hàm này giờ đây gọi :func:`os.scandir` thay vì :func:`os.listdir`, giúp hàm nhanh hơn bằng cách giảm số lần gọi đến :func:`os.stat`.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: fwalk(top='.', topdown=True, onerror=None, *, follow_symlinks=False, dir_fd=None)

   .. index::
      single: directory; walking
      single: directory; traversal

   Thao tác này hoạt động chính xác như :func:`walk`, ngoại trừ việc trả về một bộ 4 phần tử ``(dirpath, dirnames, filenames, dirfd)``, và hỗ trợ ``dir_fd``.

   *dirpath*, *dirnames* và *filenames* giống hệt đầu ra của :func:`walk`, còn *dirfd* là một file descriptor tham chiếu đến thư mục *dirpath*.

   Hàm này luôn hỗ trợ :ref:`các đường dẫn tương đối với bộ mô tả thư mục <dir_fd>` và :ref:`không theo các liên kết tượng trưng <follow_symlinks>`.  Tuy nhiên, lưu ý rằng, không giống các hàm khác, :func:`fwalk` giá trị mặc định của *follow_symlinks* là ``False``.

   .. note::

      Vì :func:`fwalk` trả về các file descriptor, chúng chỉ hợp lệ cho đến bước lặp tiếp theo, vì vậy bạn nên sao chép chúng (ví dụ: bằng
      :func:`dup`) nếu bạn muốn giữ chúng lâu hơn.

   Ví dụ này hiển thị số byte được các tệp không phải thư mục chiếm dụng trong từng thư mục bên dưới thư mục bắt đầu, ngoại trừ việc không xem xét bên trong bất kỳ thư mục con ``__pycache__`` nào::

      import os
      for root, dirs, files, rootfd in os.fwalk('python/Lib/xml'):
          print(root, "consumes", end=" ")
          print(sum([os.stat(name, dir_fd=rootfd).st_size for name in files]),
                end=" ")
          print("bytes in", len(files), "non-directory files")
          if '__pycache__' in dirs:
              dirs.remove('__pycache__')  # không truy cập các thư mục __pycache__

   Trong ví dụ tiếp theo, việc duyệt cây từ dưới lên là rất quan trọng:
   :func:`rmdir` không cho phép xóa một thư mục trước khi thư mục đó rỗng::

      # Xóa mọi thứ có thể truy cập từ thư mục được chỉ định trong "top",
      # giả sử không có liên kết tượng trưng.
      # CẢNH BÁO: Việc này rất nguy hiểm! Ví dụ, nếu top == '/', nó
      # có thể xóa tất cả các tệp trên ổ đĩa của bạn.
      import os
      for root, dirs, files, rootfd in os.fwalk(top, topdown=False):
          for name in files:
              os.unlink(name, dir_fd=rootfd)
          for name in dirs:
              os.rmdir(name, dir_fd=rootfd)

   .. audit-event:: os.fwalk top,topdown,onerror,follow_symlinks,dir_fd os.fwalk

   .. availability:: Unix.

   .. versionadded:: 3.3

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.

   .. versionchanged:: 3.7
      Đã bổ sung hỗ trợ cho các đường dẫn :class:`bytes`.


.. function:: memfd_create(name[, flags=os.MFD_CLOEXEC])

   Tạo một tệp ẩn danh và trả về một file descriptor tham chiếu đến tệp đó. *flags* phải là một trong các hằng số ``os.MFD_*`` có sẵn trên hệ thống (hoặc tổ hợp OR theo bit của chúng). Theo mặc định, file descriptor mới là :ref:`không thể kế thừa <fd_inheritance>`.

   Tên được cung cấp trong *name* được dùng làm tên tệp và sẽ được hiển thị dưới dạng đích của symbolic link tương ứng trong thư mục ``/proc/self/fd/``. Tên được hiển thị luôn có tiền tố ``memfd:`` và chỉ phục vụ mục đích gỡ lỗi. Tên không ảnh hưởng đến hành vi của file descriptor, vì vậy nhiều tệp có thể có cùng tên mà không gây ra bất kỳ tác động phụ nào.

   .. availability:: Linux >= 3.17 with glibc >= 2.27.

   .. versionadded:: 3.8


.. data:: MFD_CLOEXEC
          MFD_ALLOW_SEALING MFD_HUGETLB MFD_HUGE_SHIFT MFD_HUGE_MASK MFD_HUGE_64KB MFD_HUGE_512KB MFD_HUGE_1MB MFD_HUGE_2MB MFD_HUGE_8MB MFD_HUGE_16MB MFD_HUGE_32MB MFD_HUGE_256MB MFD_HUGE_512MB MFD_HUGE_1GB MFD_HUGE_2GB MFD_HUGE_16GB

   Các cờ này có thể được truyền cho :func:`memfd_create`.

   .. availability:: Linux >= 3.17 with glibc >= 2.27

      Các cờ ``MFD_HUGE*`` chỉ khả dụng kể từ Linux 4.14.

   .. versionadded:: 3.8


.. function:: eventfd(initval[, flags=os.EFD_CLOEXEC])

   Tạo và trả về một file descriptor sự kiện. File descriptor này hỗ trợ raw :func:`read` và :func:`write` với kích thước bộ đệm là 8,
   :func:`~select.select`, :func:`~select.poll` và các giá trị tương tự. Xem trang man
   :manpage:`eventfd(2)` để biết thêm thông tin. Theo mặc định, file descriptor mới là :ref:`không kế thừa <fd_inheritance>`.

   *initval* là giá trị ban đầu của bộ đếm sự kiện. Giá trị ban đầu phải là một số nguyên không dấu 32 bit. Lưu ý rằng giá trị ban đầu bị giới hạn ở một số nguyên không dấu 32 bit, mặc dù bộ đếm sự kiện là một số nguyên không dấu 64 bit với giá trị tối đa là 2\ :sup:`64`\ -\ 2.

   *flags* có thể được tạo từ :const:`EFD_CLOEXEC`,
   :const:`EFD_NONBLOCK`, và :const:`EFD_SEMAPHORE`.

   Nếu :const:`EFD_SEMAPHORE` được chỉ định và bộ đếm sự kiện khác 0,
   :func:`eventfd_read` trả về 1 và giảm bộ đếm đi một.

   Nếu :const:`EFD_SEMAPHORE` không được chỉ định và bộ đếm sự kiện khác không, :func:`eventfd_read` trả về giá trị hiện tại của bộ đếm sự kiện và đặt lại bộ đếm về 0.

   Nếu bộ đếm sự kiện bằng 0 và :const:`EFD_NONBLOCK` không được chỉ định, :func:`eventfd_read` sẽ chặn.

   :func:`eventfd_write` tăng bộ đếm sự kiện. Ghi sẽ bị chặn nếu thao tác ghi làm tăng bộ đếm lên giá trị lớn hơn 2\ :sup:`64`\ -\ 2.

   Ví dụ::

       import os

       # semaphore với giá trị bắt đầu là '1'
       fd = os.eventfd(1, os.EFD_SEMAPHORE | os.EFD_CLOEXEC)
       try:
           # lấy semaphore
           v = os.eventfd_read(fd)
           try:
               do_work()
           finally:
               # giải phóng semaphore
               os.eventfd_write(fd, v)
       finally:
           os.close(fd)

   .. availability:: Linux >= 2.6.27 with glibc >= 2.8

   .. versionadded:: 3.10

.. function:: eventfd_read(fd)

   Đọc giá trị từ một :func:`eventfd` file descriptor và trả về một số nguyên không dấu 64 bit. Hàm không kiểm tra xem *fd* có phải là một :func:`eventfd` hay không.

   .. availability:: Linux >= 2.6.27

   .. versionadded:: 3.10

.. function:: eventfd_write(fd, value)

   Thêm giá trị vào một :func:`eventfd` file descriptor. *value* phải là một số nguyên không dấu 64 bit. Hàm không kiểm tra xem *fd* có phải là một :func:`eventfd` hay không.

   .. availability:: Linux >= 2.6.27

   .. versionadded:: 3.10

.. data:: EFD_CLOEXEC

   Đặt cờ close-on-exec cho :func:`eventfd` file descriptor mới.

   .. availability:: Linux >= 2.6.27

   .. versionadded:: 3.10

.. data:: EFD_NONBLOCK

   Đặt cờ trạng thái :const:`O_NONBLOCK` cho :func:`eventfd` file descriptor mới.

   .. availability:: Linux >= 2.6.27

   .. versionadded:: 3.10

.. data:: EFD_SEMAPHORE

   Cung cấp ngữ nghĩa giống semaphore cho các thao tác đọc từ một :func:`eventfd` file descriptor. Khi đọc, bộ đếm nội bộ giảm đi một.

   .. availability:: Linux >= 2.6.30

   .. versionadded:: 3.10


.. _os-timerfd:

File descriptor của bộ hẹn giờ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 3.13

Các hàm này cung cấp hỗ trợ cho API *timer file descriptor* của Linux. Tất nhiên, tất cả chúng chỉ khả dụng trên Linux.

.. function:: timerfd_create(clockid, /, *, flags=0)

   Tạo và trả về một timer file descriptor (*timerfd*).

   File descriptor được trả về bởi :func:`timerfd_create` hỗ trợ:

   - :func:`read`
   - :func:`~select.select`
   - :func:`~select.poll`

   Có thể gọi :func:`read` method của file descriptor với kích thước bộ đệm là 8. Nếu timer đã hết hạn một hoặc nhiều lần, :func:`read` trả về số lần hết hạn theo thứ tự byte của máy chủ, giá trị này có thể được chuyển đổi thành :class:`int` bằng ``int.from_bytes(x, byteorder=sys.byteorder)``.

   Có thể sử dụng :func:`~select.select` và :func:`~select.poll` để chờ đến khi timer hết hạn và file descriptor có thể đọc được.

   *clockid* phải là một :ref:`clock ID <time-clock-id-constants>` hợp lệ, như được định nghĩa trong module :py:mod:`time`:

   - :const:`time.CLOCK_REALTIME`
   - :const:`time.CLOCK_MONOTONIC`
   - :const:`time.CLOCK_BOOTTIME` (Kể từ Linux 3.15 đối với timerfd_create)

   Nếu *clockid* là :const:`time.CLOCK_REALTIME`, một đồng hồ thời gian thực trên toàn hệ thống có thể thiết lập được sẽ được sử dụng. Nếu đồng hồ hệ thống bị thay đổi, cần cập nhật thiết lập bộ hẹn giờ. Để hủy bộ hẹn giờ khi đồng hồ hệ thống bị thay đổi, xem
   :const:`TFD_TIMER_CANCEL_ON_SET`.

   Nếu *clockid* là :const:`time.CLOCK_MONOTONIC`, một đồng hồ tăng đơn điệu không thể thiết lập được sẽ được sử dụng. Ngay cả khi đồng hồ hệ thống bị thay đổi, thiết lập bộ hẹn giờ cũng không bị ảnh hưởng.

   Nếu *clockid* là :const:`time.CLOCK_BOOTTIME`, nó tương tự như
   :const:`time.CLOCK_MONOTONIC`, ngoại trừ việc nó bao gồm cả khoảng thời gian hệ thống bị tạm ngưng.

   Có thể sửa đổi hành vi của file descriptor bằng cách chỉ định giá trị *flags*. Có thể sử dụng bất kỳ biến nào sau đây, kết hợp bằng phép OR theo bit (toán tử ``|``):

   - :const:`TFD_NONBLOCK`
   - :const:`TFD_CLOEXEC`

   Nếu :const:`TFD_NONBLOCK` không được đặt làm flag, :func:`read` sẽ chặn cho đến khi bộ hẹn giờ hết hạn. Nếu được đặt làm flag, :func:`read` sẽ không chặn, nhưng nếu chưa có lần hết hạn nào kể từ lần gọi read gần nhất,
   :func:`read` sẽ phát sinh :class:`OSError` với ``errno`` được đặt thành
   :const:`errno.EAGAIN`.

   :const:`TFD_CLOEXEC` luôn được Python tự động thiết lập.

   Phải đóng bộ mô tả tệp bằng :func:`os.close` khi không còn cần đến nó; nếu không, bộ mô tả tệp sẽ bị rò rỉ.

   .. seealso:: Trang hướng dẫn man của :manpage:`timerfd_create(2)`.

   .. availability:: Linux >= 2.6.27 with glibc >= 2.8

   .. versionadded:: 3.13


.. function:: timerfd_settime(fd, /, *, flags=0, initial=0.0, interval=0.0)

   Thay đổi bộ hẹn giờ nội bộ của một bộ mô tả tệp hẹn giờ. Hàm này sử dụng cùng một bộ hẹn giờ theo khoảng thời gian như :func:`timerfd_settime_ns`.

   *fd* phải là một bộ mô tả tệp hẹn giờ hợp lệ.

   Có thể sửa đổi hành vi của bộ hẹn giờ bằng cách chỉ định giá trị *flags*. Có thể sử dụng bất kỳ biến nào sau đây, kết hợp bằng phép OR theo bit (toán tử ``|``):

   - :const:`TFD_TIMER_ABSTIME`
   - :const:`TFD_TIMER_CANCEL_ON_SET`

   Vô hiệu hóa bộ hẹn giờ bằng cách đặt *initial* thành không (``0``). Nếu *initial* lớn hơn không, bộ hẹn giờ sẽ được bật. Nếu *initial* nhỏ hơn không, nó sẽ phát sinh ngoại lệ :class:`OSError` với ``errno`` được đặt thành :const:`errno.EINVAL`.

   Theo mặc định, timer sẽ kích hoạt khi đã trôi qua *initial* giây.

   Tuy nhiên, nếu đặt cờ :const:`TFD_TIMER_ABSTIME`, timer sẽ kích hoạt khi clock của timer (được thiết lập bởi *clockid* trong :func:`timerfd_create`) đạt đến *initial* giây.

   Khoảng thời gian của timer được thiết lập bởi *interval* :py:class:`float`. Nếu *interval* bằng 0, timer chỉ kích hoạt một lần, tại lần hết hạn ban đầu. Nếu *interval* lớn hơn 0, timer kích hoạt mỗi khi đã trôi qua *interval* giây kể từ lần hết hạn trước đó. Nếu *interval* nhỏ hơn 0, nó raise :class:`OSError` với ``errno`` được đặt thành :const:`errno.EINVAL`.

   Nếu cờ :const:`TFD_TIMER_CANCEL_ON_SET` được đặt cùng với
   :const:`TFD_TIMER_ABSTIME` và clock của timer này là
   :const:`time.CLOCK_REALTIME`, timer được đánh dấu là có thể hủy nếu real-time clock bị thay đổi không liên tục. Việc đọc descriptor bị hủy bỏ với lỗi :const:`errno.ECANCELED`.

   Linux quản lý system clock theo UTC. Việc chuyển đổi giờ mùa hè chỉ được thực hiện bằng cách thay đổi độ lệch thời gian và không gây ra thay đổi không liên tục của system clock.

   Việc thay đổi đồng hồ hệ thống không liên tục sẽ do các sự kiện sau gây ra:

   - ``settimeofday``
   - ``clock_settime``
   - đặt ngày và giờ hệ thống bằng lệnh ``date``

   Trả về một tuple gồm hai phần tử (``next_expiration``, ``interval``) từ trạng thái timer trước đó, trước khi hàm này được thực thi.

   .. seealso::

      :manpage:`timerfd_create(2)`, :manpage:`timerfd_settime(2)`,
      :manpage:`settimeofday(2)`, :manpage:`clock_settime(2)` và :manpage:`date(1)`.

   .. availability:: Linux >= 2.6.27 with glibc >= 2.8

   .. versionadded:: 3.13


.. function:: timerfd_settime_ns(fd, /, *, flags=0, initial=0, interval=0)

   Tương tự như :func:`timerfd_settime`, nhưng sử dụng thời gian tính bằng nanosecond. Hàm này vận hành cùng interval timer như :func:`timerfd_settime`.

   .. availability:: Linux >= 2.6.27 with glibc >= 2.8

   .. versionadded:: 3.13


.. function:: timerfd_gettime(fd, /)

   Trả về một tuple gồm hai số thực (``next_expiration``, ``interval``).

   ``next_expiration`` biểu thị khoảng thời gian tương đối cho đến lần timer tiếp theo kích hoạt, bất kể cờ :const:`TFD_TIMER_ABSTIME` có được thiết lập hay không.

   ``interval`` biểu thị khoảng thời gian của bộ hẹn giờ. Nếu bằng 0, bộ hẹn giờ sẽ chỉ kích hoạt một lần, sau khi đã trôi qua ``next_expiration`` giây.

   .. seealso:: :manpage:`timerfd_gettime(2)`

   .. availability:: Linux >= 2.6.27 with glibc >= 2.8

   .. versionadded:: 3.13


.. function:: timerfd_gettime_ns(fd, /)

   Tương tự như :func:`timerfd_gettime`, nhưng trả về thời gian theo đơn vị nano giây.

   .. availability:: Linux >= 2.6.27 with glibc >= 2.8

   .. versionadded:: 3.13

.. data:: TFD_NONBLOCK

   Một cờ cho hàm :func:`timerfd_create`, dùng để đặt cờ trạng thái :const:`O_NONBLOCK` cho bộ mô tả tệp hẹn giờ mới. Nếu :const:`TFD_NONBLOCK` không được đặt làm cờ, :func:`read` sẽ chặn.

   .. availability:: Linux >= 2.6.27 with glibc >= 2.8

   .. versionadded:: 3.13

.. data:: TFD_CLOEXEC

   Một cờ cho hàm :func:`timerfd_create`. Nếu :const:`TFD_CLOEXEC` được đặt làm cờ, hãy đặt cờ close-on-exec cho bộ mô tả tệp mới.

   .. availability:: Linux >= 2.6.27 with glibc >= 2.8

   .. versionadded:: 3.13

.. data:: TFD_TIMER_ABSTIME

   Một cờ cho các hàm :func:`timerfd_settime` và :func:`timerfd_settime_ns`. Nếu cờ này được đặt, *initial* được diễn giải là một giá trị tuyệt đối trên đồng hồ của bộ hẹn giờ (tính bằng giây hoặc nano giây UTC kể từ Unix Epoch).

   .. availability:: Linux >= 2.6.27 with glibc >= 2.8

   .. versionadded:: 3.13

.. data:: TFD_TIMER_CANCEL_ON_SET

   Một cờ cho các hàm :func:`timerfd_settime` và :func:`timerfd_settime_ns`, cùng với :const:`TFD_TIMER_ABSTIME`. Bộ hẹn giờ sẽ bị hủy khi thời gian của đồng hồ nền tảng thay đổi không liên tục.

   .. availability:: Linux >= 2.6.27 with glibc >= 2.8

   .. versionadded:: 3.13


Thuộc tính mở rộng của Linux
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 3.3

Tất cả các hàm này chỉ khả dụng trên Linux.

.. function:: getxattr(path, attribute, *, follow_symlinks=True)

   Trả về giá trị của thuộc tính mở rộng của hệ thống tệp *attribute* cho *path*. *attribute* có thể là bytes hoặc str (trực tiếp hoặc gián tiếp thông qua
   :class:`PathLike` interface). Nếu là str, nó được mã hóa bằng encoding của hệ thống tệp.

   Hàm này hỗ trợ :ref:`chỉ định một file descriptor <path_fd>` và
   :ref:`không đi theo các symlink <follow_symlinks>`.

   .. audit-event:: os.getxattr path,attribute os.getxattr

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object` cho *path* và *attribute*.


.. function:: listxattr(path=None, *, follow_symlinks=True)

   Trả về danh sách các thuộc tính mở rộng của hệ thống tệp trên *path*. Các thuộc tính trong danh sách được biểu diễn dưới dạng chuỗi, giải mã bằng encoding của hệ thống tệp. Nếu *path* là ``None``, :func:`listxattr` sẽ kiểm tra thư mục hiện tại.

   Hàm này hỗ trợ :ref:`chỉ định một file descriptor <path_fd>` và
   :ref:`không đi theo các symlink <follow_symlinks>`.

   .. audit-event:: os.listxattr path os.listxattr

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.


.. function:: removexattr(path, attribute, *, follow_symlinks=True)

   Xóa thuộc tính mở rộng của hệ thống tệp *attribute* khỏi *path*. *attribute* phải là bytes hoặc str (trực tiếp hoặc gián tiếp thông qua giao diện
   :class:`PathLike`). Nếu là chuỗi, chuỗi đó được mã hóa bằng :term:`filesystem encoding and error handler`.

   Hàm này hỗ trợ :ref:`chỉ định một file descriptor <path_fd>` và
   :ref:`không đi theo các symlink <follow_symlinks>`.

   .. audit-event:: os.removexattr path,attribute os.removexattr

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object` cho *path* và *attribute*.


.. function:: setxattr(path, attribute, value, flags=0, *, follow_symlinks=True)

   Đặt thuộc tính hệ thống tệp mở rộng *attribute* trên *path* thành *value*. *attribute* phải là bytes hoặc str không chứa ký tự NUL, dù trực tiếp hay gián tiếp thông qua giao diện :class:`PathLike`. Nếu là str, nó sẽ được mã hóa bằng :term:`filesystem encoding and error handler`.  *flags* có thể là
   :data:`XATTR_REPLACE` hoặc :data:`XATTR_CREATE`. Nếu cung cấp :data:`XATTR_REPLACE` mà thuộc tính không tồn tại, ``ENODATA`` sẽ được raise. Nếu cung cấp :data:`XATTR_CREATE` mà thuộc tính đã tồn tại, thuộc tính sẽ không được tạo và ``EEXISTS`` sẽ được raise.

   Hàm này hỗ trợ :ref:`chỉ định một file descriptor <path_fd>` và
   :ref:`không đi theo các symlink <follow_symlinks>`.

   .. note::

      Một lỗi trong các phiên bản Linux kernel thấp hơn 2.6.39 khiến đối số flags bị bỏ qua trên một số hệ thống tệp.

   .. audit-event:: os.setxattr path,attribute,value,flags os.setxattr

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object` cho *path* và *attribute*.


.. data:: XATTR_SIZE_MAX

   Kích thước tối đa của giá trị một extended attribute có thể là bao nhiêu. Hiện tại, kích thước này là 64 KiB trên Linux.


.. data:: XATTR_CREATE

   Đây là một giá trị có thể có của đối số flags trong :func:`setxattr`. Giá trị này cho biết thao tác phải tạo một attribute.


.. data:: XATTR_REPLACE

   Đây là một giá trị có thể có của đối số flags trong :func:`setxattr`. Giá trị này cho biết thao tác phải thay thế một attribute hiện có.


.. _os-process:

Quản lý tiến trình
------------------

Bạn có thể sử dụng các hàm này để tạo và quản lý tiến trình.

Các hàm :func:`exec\* <execl>` khác nhau nhận một danh sách đối số cho chương trình mới được nạp vào tiến trình. Trong mỗi trường hợp, đối số đầu tiên được truyền cho chương trình mới dưới dạng tên của chính chương trình đó, thay vì là một đối số mà người dùng có thể đã nhập trên dòng lệnh. Đối với lập trình viên C, đây là ``argv[0]`` được truyền vào :c:func:`main` của chương trình. Ví dụ, ``os.execv('/bin/echo', ['foo', 'bar'])`` sẽ chỉ in ``bar`` ra đầu ra chuẩn; ``foo`` dường như sẽ bị bỏ qua.


.. function:: abort()

   Tạo tín hiệu :const:`SIGABRT` cho tiến trình hiện tại. Trên Unix, hành vi mặc định là tạo một core dump; trên Windows, tiến trình ngay lập tức trả về mã thoát ``3``. Lưu ý rằng việc gọi hàm này sẽ không gọi trình xử lý tín hiệu Python đã đăng ký cho :const:`SIGABRT` với
   :func:`signal.signal`.


.. function:: add_dll_directory(path)

   Thêm một đường dẫn vào đường dẫn tìm kiếm DLL.

   Đường dẫn tìm kiếm này được sử dụng khi phân giải các dependency cho những extension module được import (bản thân module được phân giải thông qua
   :data:`sys.path`), và cũng bởi :mod:`ctypes`.

   Xóa thư mục bằng cách gọi **close()** trên đối tượng được trả về hoặc sử dụng đối tượng đó trong câu lệnh :keyword:`with`.

   Xem `tài liệu của Microsoft <https://msdn.microsoft.com/44228cf2-6306-466c-8f16-f513cd3ba8b5>`_ để biết thêm thông tin về cách các DLL được tải.

   .. audit-event:: os.add_dll_directory path os.add_dll_directory

   .. availability:: Windows.

   .. versionadded:: 3.8
      Các phiên bản CPython trước đây sẽ phân giải DLL bằng hành vi mặc định của process hiện tại. Điều này dẫn đến những điểm không nhất quán, chẳng hạn như chỉ đôi khi tìm kiếm :envvar:`PATH` hoặc thư mục làm việc hiện tại, và các hàm của OS như ``AddDllDirectory`` không có tác dụng.

      Trong 3.8, hai cách chính để tải DLL hiện đã ghi đè rõ ràng hành vi trên toàn process nhằm đảm bảo tính nhất quán. Xem
      :ref:`ghi chú chuyển đổi <bpo-36085-whatsnew>` để biết thông tin về việc cập nhật các thư viện.


.. function:: execl(path, arg0, arg1, ...)
              execle(path, arg0, arg1, ..., env) execlp(file, arg0, arg1, ...) execlpe(file, arg0, arg1, ..., env) execv(path, args) execve(path, args, env) execvp(file, args) execvpe(file, args, env)

   Tất cả các hàm này đều thực thi một chương trình mới, thay thế process hiện tại; chúng không trả về. Trên Unix, tệp thực thi mới được tải vào process hiện tại và sẽ có cùng mã process với bên gọi. Các lỗi sẽ được báo cáo dưới dạng
   :exc:`OSError` ngoại lệ.

   Process hiện tại được thay thế ngay lập tức. Các đối tượng tệp và descriptor đang mở không được flush, vì vậy nếu có thể có dữ liệu đang được đệm trong các tệp đang mở này, bạn nên flush chúng bằng
   :func:`~io.IOBase.flush` hoặc :func:`os.fsync` trước khi gọi một
   :func:`exec\* <execl>` hàm.

   Các biến thể "l" và "v" của các hàm :func:`exec\* <execl>` khác nhau ở cách truyền các đối số dòng lệnh. Các biến thể "l" có lẽ dễ sử dụng nhất nếu số lượng tham số được cố định khi viết mã; các tham số riêng lẻ chỉ đơn giản trở thành các tham số bổ sung cho các hàm :func:`!execl\*`. Các biến thể "v" phù hợp khi số lượng tham số thay đổi, với các đối số được truyền trong một danh sách hoặc tuple dưới dạng tham số *args*. Trong cả hai trường hợp, các đối số của tiến trình con nên bắt đầu bằng tên của lệnh đang chạy, nhưng điều này không được bắt buộc.

   Các biến thể có chữ "p" gần cuối (:func:`execlp`,
   :func:`execlpe`, :func:`execvp`, và :func:`execvpe`) sẽ sử dụng
   biến môi trường :envvar:`PATH` để định vị tệp *file* của chương trình. Khi môi trường được thay thế (bằng một trong các biến thể :func:`exec\*e <execl>`, được thảo luận trong đoạn tiếp theo), môi trường mới sẽ được dùng làm nguồn của biến :envvar:`PATH`. Các biến thể khác, :func:`execl`, :func:`execle`,
   :func:`execv`, và :func:`execve`, sẽ không sử dụng biến :envvar:`PATH` để định vị tệp thực thi; *path* phải chứa một đường dẫn tuyệt đối hoặc tương đối phù hợp. Đường dẫn tương đối phải chứa ít nhất một dấu gạch chéo, kể cả trên Windows, vì các tên đơn thuần sẽ không được phân giải.

   Đối với :func:`execle`, :func:`execlpe`, :func:`execve`, và :func:`execvpe` (lưu ý rằng tất cả các tên này đều kết thúc bằng "e"), tham số *env* phải là một mapping được dùng để xác định các biến môi trường cho tiến trình mới (các biến này được sử dụng thay cho môi trường của tiến trình hiện tại); các hàm :func:`execl`,
   :func:`execlp`, :func:`execv`, và :func:`execvp` đều khiến tiến trình mới kế thừa môi trường của tiến trình hiện tại.

   Đối với :func:`execve` trên một số nền tảng, *path* cũng có thể được chỉ định dưới dạng một file descriptor đang mở. Tính năng này có thể không được nền tảng của bạn hỗ trợ; bạn có thể kiểm tra tính khả dụng của tính năng này bằng :data:`os.supports_fd`. Nếu không khả dụng, việc sử dụng nó sẽ gây ra :exc:`NotImplementedError`.

   .. audit-event:: os.exec path,args,env os.execl

   .. availability:: Unix, Windows, not WASI, not Android, not iOS.

   .. versionchanged:: 3.3
      Đã bổ sung hỗ trợ chỉ định *path* dưới dạng một file descriptor đang mở cho :func:`execve`.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.

.. function:: _exit(n)

   Thoát tiến trình với trạng thái *n*, mà không gọi các trình xử lý dọn dẹp, xả các bộ đệm stdio, v.v.

   .. note::

      Cách thoát tiêu chuẩn là :func:`sys.exit(n) <sys.exit>`. Thông thường, chỉ nên sử dụng :func:`!_exit` trong tiến trình con sau một :func:`fork`.

Các mã thoát sau đây được định nghĩa và có thể được sử dụng với :func:`_exit`, mặc dù không bắt buộc phải dùng chúng. Chúng thường được sử dụng cho các chương trình hệ thống được viết bằng Python, chẳng hạn như chương trình phân phối lệnh bên ngoài của máy chủ thư.

.. note::

   Một số hằng số trong số này có thể không khả dụng trên mọi nền tảng Unix do có một số khác biệt. Các hằng số này được định nghĩa ở những nơi mà nền tảng bên dưới định nghĩa chúng.


.. data:: EX_OK

   Mã thoát cho biết không xảy ra lỗi. Trên một số nền tảng, mã này có thể được lấy từ giá trị được định nghĩa của ``EXIT_SUCCESS``. Nhìn chung, mã này có giá trị bằng không.

   .. availability:: Unix, Windows.


.. data:: EX_USAGE

   Mã thoát cho biết lệnh đã được sử dụng không đúng cách, chẳng hạn như khi cung cấp sai số lượng đối số.

   .. availability:: Unix, not WASI.


.. data:: EX_DATAERR

   Mã thoát cho biết dữ liệu đầu vào không chính xác.

   .. availability:: Unix, not WASI.


.. data:: EX_NOINPUT

   Mã thoát cho biết tệp đầu vào không tồn tại hoặc không thể đọc được.

   .. availability:: Unix, not WASI.


.. data:: EX_NOUSER

   Mã thoát cho biết người dùng được chỉ định không tồn tại.

   .. availability:: Unix, not WASI.


.. data:: EX_NOHOST

   Mã thoát cho biết máy chủ được chỉ định không tồn tại.

   .. availability:: Unix, not WASI.


.. data:: EX_UNAVAILABLE

   Mã thoát cho biết một dịch vụ bắt buộc không khả dụng.

   .. availability:: Unix, not WASI.


.. data:: EX_SOFTWARE

   Mã thoát cho biết đã phát hiện lỗi phần mềm nội bộ.

   .. availability:: Unix, not WASI.


.. data:: EX_OSERR

   Mã thoát cho biết đã phát hiện lỗi hệ điều hành, chẳng hạn như không thể fork hoặc tạo pipe.

   .. availability:: Unix, not WASI.


.. data:: EX_OSFILE

   Mã thoát cho biết một tệp hệ thống nào đó không tồn tại, không thể mở hoặc gặp một loại lỗi khác.

   .. availability:: Unix, not WASI.


.. data:: EX_CANTCREAT

   Mã thoát cho biết không thể tạo tệp đầu ra do người dùng chỉ định.

   .. availability:: Unix, not WASI.


.. data:: EX_IOERR

   Mã thoát cho biết đã xảy ra lỗi khi thực hiện I/O trên một tệp nào đó.

   .. availability:: Unix, not WASI.


.. data:: EX_TEMPFAIL

   Mã thoát cho biết đã xảy ra lỗi tạm thời.  Điều này cho biết một sự cố có thể thực sự không phải là lỗi, chẳng hạn như không thể thiết lập kết nối mạng trong một thao tác có thể thử lại.

   .. availability:: Unix, not WASI.


.. data:: EX_PROTOCOL

   Mã thoát cho biết một hoạt động trao đổi giao thức là bất hợp pháp, không hợp lệ hoặc không được hiểu.

   .. availability:: Unix, not WASI.


.. data:: EX_NOPERM

   Mã thoát cho biết không đủ quyền để thực hiện thao tác (nhưng không dành cho các sự cố về hệ thống tệp).

   .. availability:: Unix, not WASI.


.. data:: EX_CONFIG

   Mã thoát cho biết đã xảy ra một loại lỗi cấu hình nào đó.

   .. availability:: Unix, not WASI.


.. data:: EX_NOTFOUND

   Mã thoát cho biết điều gì đó tương tự như "không tìm thấy mục nhập".

   .. availability:: Unix, not WASI.


.. function:: fork()

   Tạo một tiến trình con bằng fork. Trả về ``0`` trong tiến trình con và mã tiến trình của tiến trình con trong tiến trình cha. Nếu xảy ra lỗi, :exc:`OSError` sẽ được phát sinh.

   Lưu ý rằng một số nền tảng, bao gồm FreeBSD <= 6.3 và Cygwin, có các sự cố đã biết khi sử dụng ``fork()`` từ một thread.

   .. audit-event:: os.fork "" os.fork

   .. warning::

      Nếu bạn sử dụng TLS sockets trong một ứng dụng gọi ``fork()``, hãy xem cảnh báo trong tài liệu về :mod:`ssl`.

   .. warning::

      Trên macOS, việc sử dụng hàm này không an toàn khi kết hợp với việc sử dụng các system API cấp cao hơn, trong đó có việc sử dụng :mod:`urllib.request`.

   .. versionchanged:: 3.8
      Việc gọi ``fork()`` trong subinterpreter không còn được hỗ trợ (:exc:`RuntimeError` được phát sinh).

   .. versionchanged:: 3.12
      Nếu Python có thể phát hiện rằng tiến trình của bạn có nhiều thread, :func:`os.fork` hiện sẽ phát sinh một :exc:`DeprecationWarning`.

      Khi có thể phát hiện, chúng tôi chọn hiển thị điều này dưới dạng cảnh báo để thông báo rõ hơn cho các developer về một vấn đề thiết kế mà nền tảng POSIX đặc biệt ghi rõ là không được hỗ trợ. Ngay cả trong code mà *có vẻ* hoạt động, việc kết hợp threading với
      :func:`os.fork` trên các nền tảng POSIX chưa bao giờ an toàn. Bản thân runtime CPython luôn thực hiện các lệnh gọi API không an toàn khi dùng trong tiến trình con nếu tiến trình cha có thread (chẳng hạn như ``malloc`` và ``free``).

      Người dùng macOS hoặc người dùng các bản triển khai libc hay malloc khác với những bản thường có trong glibc cho đến nay nằm trong số những đối tượng có nhiều khả năng gặp deadlock hơn khi chạy code như vậy.

      Xem `cuộc thảo luận này về việc fork không tương thích với thread <https://discuss.python.org/t/33555>`_ để biết các chi tiết kỹ thuật về lý do chúng tôi đưa vấn đề tương thích lâu nay của nền tảng này ra cho các developer.

   .. availability:: POSIX, not WASI, not Android, not iOS.


.. function:: forkpty()

   Fork một tiến trình con, sử dụng một pseudo-terminal mới làm terminal điều khiển của tiến trình con. Trả về một cặp ``(pid, fd)``, trong đó *pid* là ``0`` trong tiến trình con, là process id của tiến trình con mới trong tiến trình cha, còn *fd* là file descriptor của đầu master của pseudo-terminal. Để có cách tiếp cận khả chuyển hơn, hãy sử dụng
   mô-đun :mod:`pty`. Nếu xảy ra lỗi, :exc:`OSError` sẽ được đưa ra.

   .. audit-event:: os.forkpty "" os.forkpty

   .. warning::

      Trên macOS, việc sử dụng hàm này không an toàn khi kết hợp với việc sử dụng các system API cấp cao hơn, trong đó có việc sử dụng :mod:`urllib.request`.

   .. versionchanged:: 3.8
      Không còn hỗ trợ gọi ``forkpty()`` trong subinterpreter (:exc:`RuntimeError` sẽ được đưa ra).

   .. versionchanged:: 3.12
      Nếu Python có thể phát hiện rằng process của bạn có nhiều thread, thao tác này sẽ đưa ra :exc:`DeprecationWarning`. Xem phần giải thích chi tiết hơn về :func:`os.fork`.

   .. availability:: Unix, not WASI, not Android, not iOS.


.. function:: kill(pid, sig, /)

   .. index::
      single: process; killing
      single: process; signalling

   Gửi signal *sig* đến process *pid*. Các hằng số cho những signal cụ thể có trên platform máy chủ được định nghĩa trong mô-đun :mod:`signal`.

   Windows: :const:`signal.CTRL_C_EVENT` và
   :const:`signal.CTRL_BREAK_EVENT` signals là những signal đặc biệt chỉ có thể được gửi đến các console process dùng chung một cửa sổ console, chẳng hạn như một số subprocess. Bất kỳ giá trị nào khác của *sig* sẽ khiến process bị TerminateProcess API kết thúc vô điều kiện, và mã thoát sẽ được đặt thành *sig*.

   Xem thêm :func:`signal.pthread_kill`.

   .. audit-event:: os.kill pid,sig os.kill

   .. availability:: Unix, Windows, not WASI, not iOS.

   .. versionchanged:: 3.2
      Đã bổ sung hỗ trợ Windows.


.. function:: killpg(pgid, sig, /)

   .. index::
      single: process; killing
      single: process; signalling

   Gửi tín hiệu *sig* đến nhóm tiến trình *pgid*.

   .. audit-event:: os.killpg pgid,sig os.killpg

   .. availability:: Unix, not WASI, not iOS.


.. function:: nice(increment, /)

   Tăng "niceness" của tiến trình thêm *increment*. Trả về niceness mới.

   .. availability:: Unix, not WASI.


.. function:: pidfd_open(pid, flags=0)

   Trả về một file descriptor tham chiếu đến tiến trình *pid* với *flags* được thiết lập. Descriptor này có thể được sử dụng để thực hiện việc quản lý tiến trình mà không gặp race condition và tín hiệu.

   Xem trang man :manpage:`pidfd_open(2)` để biết thêm chi tiết.

   .. availability:: Linux >= 5.3, Android >= :func:`build-time <sys.getandroidapilevel>` API level 31
   .. versionadded:: 3.9

   .. data:: PIDFD_NONBLOCK

      Cờ này cho biết file descriptor sẽ ở chế độ non-blocking. Nếu tiến trình được file descriptor tham chiếu chưa kết thúc, thì việc thử chờ file descriptor bằng :manpage:`waitid(2)` sẽ ngay lập tức trả về lỗi :const:`~errno.EAGAIN` thay vì bị chặn.

   .. availability:: Linux >= 5.10
   .. versionadded:: 3.12


.. function:: plock(op, /)

   Khóa các đoạn chương trình vào bộ nhớ. Giá trị của *op* (được định nghĩa trong ``<sys/lock.h>``) xác định những đoạn nào được khóa.

   .. availability:: Unix, not WASI, not macOS, not iOS.


.. function:: popen(cmd, mode='r', buffering=-1)

   Mở một pipe đến hoặc từ lệnh *cmd*. Giá trị trả về là một đối tượng tệp đang mở được kết nối với pipe, có thể đọc hoặc ghi tùy thuộc vào việc *mode* là ``'r'`` (mặc định) hay ``'w'``. Đối số *buffering* có cùng ý nghĩa như đối số tương ứng của hàm dựng sẵn :func:`open`. Đối tượng tệp được trả về đọc hoặc ghi các chuỗi văn bản thay vì byte.

   Phương thức ``close`` trả về :const:`None` nếu subprocess đã thoát thành công, hoặc mã trả về của subprocess nếu xảy ra lỗi. Trên các hệ thống POSIX, nếu mã trả về là số dương, mã này biểu thị giá trị trả về của tiến trình được dịch trái một byte. Nếu mã trả về là số âm, tiến trình đã bị kết thúc bởi signal được xác định bằng giá trị đối của mã trả về. (Ví dụ: giá trị trả về có thể là ``- signal.SIGKILL`` nếu subprocess bị kill.) Trên các hệ thống Windows, giá trị trả về chứa mã trả về số nguyên có dấu từ tiến trình con.

   Trên Unix, có thể dùng :func:`waitstatus_to_exitcode` để chuyển kết quả của phương thức ``close`` (trạng thái thoát) thành mã thoát nếu kết quả đó không phải là ``None``. Trên Windows, kết quả của phương thức ``close`` chính là mã thoát (hoặc ``None``).

   Phần này được triển khai bằng :class:`subprocess.Popen`; hãy xem tài liệu của lớp đó để biết những cách mạnh mẽ hơn nhằm quản lý và giao tiếp với subprocess.

   .. availability:: not WASI, not Android, not iOS.

   .. note::
      :ref:`Python UTF-8 Mode <utf8-mode>` ảnh hưởng đến các encoding được dùng cho *cmd* và nội dung của pipe.

      :func:`popen` là một wrapper đơn giản quanh :class:`subprocess.Popen`. Sử dụng :class:`subprocess.Popen` hoặc :func:`subprocess.run` để kiểm soát các tùy chọn như encoding.

   .. soft-deprecated:: 3.14
      Thay vào đó, nên sử dụng module :mod:`subprocess`.


.. function:: posix_spawn(path, argv, env, *, file_actions=None, \
                          setpgroup=None, resetids=False, setsid=False, setsigmask=(), \ setsigdef=(), scheduler=None)

   Bọc API thư viện C :c:func:`!posix_spawn` để sử dụng từ Python.

   Hầu hết người dùng nên sử dụng :func:`subprocess.run` thay vì :func:`posix_spawn`.

   Các đối số chỉ dùng theo vị trí *path*, *args* và *env* tương tự như
   :func:`execve`. *env* có thể là ``None``, trong trường hợp đó môi trường của process hiện tại sẽ được sử dụng.

   Tham số *path* là đường dẫn đến tệp thực thi. *path* phải chứa một thư mục. Sử dụng :func:`posix_spawnp` để truyền một tệp thực thi không có thư mục.

   Đối số *file_actions* có thể là một chuỗi các tuple mô tả những hành động cần thực hiện trên các file descriptor cụ thể trong tiến trình con giữa các bước :c:func:`fork` và :c:func:`exec` của phần triển khai thư viện C. Phần tử đầu tiên trong mỗi tuple phải là một trong ba chỉ báo kiểu được liệt kê dưới đây, mô tả các phần tử còn lại của tuple:

   .. data:: POSIX_SPAWN_OPEN

      (``os.POSIX_SPAWN_OPEN``, *fd*, *path*, *flags*, *mode*)

      Thực hiện ``os.dup2(os.open(path, flags, mode), fd)``.

   .. data:: POSIX_SPAWN_CLOSE

      (``os.POSIX_SPAWN_CLOSE``, *fd*)

      Thực hiện ``os.close(fd)``.

   .. data:: POSIX_SPAWN_DUP2

      (``os.POSIX_SPAWN_DUP2``, *fd*, *new_fd*)

      Thực hiện ``os.dup2(fd, new_fd)``.

   .. data:: POSIX_SPAWN_CLOSEFROM

      (``os.POSIX_SPAWN_CLOSEFROM``, *fd*)

      Thực hiện ``os.closerange(fd, INF)``.

   Các tuple này tương ứng với thư viện C
   :c:func:`!posix_spawn_file_actions_addopen`,
   :c:func:`!posix_spawn_file_actions_addclose`,
   :c:func:`!posix_spawn_file_actions_adddup2`, và
   các lệnh gọi API :c:func:`!posix_spawn_file_actions_addclosefrom_np` được dùng để chuẩn bị cho chính lệnh gọi :c:func:`!posix_spawn`.

   Đối số *setpgroup* sẽ đặt process group của tiến trình con thành giá trị được chỉ định. Nếu giá trị được chỉ định là 0, ID process group của tiến trình con sẽ được đặt giống với ID tiến trình của nó. Nếu giá trị của *setpgroup* chưa được đặt, tiến trình con sẽ kế thừa ID process group của tiến trình cha. Đối số này tương ứng với cờ :c:macro:`!POSIX_SPAWN_SETPGROUP` của thư viện C.

   Nếu đối số *resetids* là ``True``, nó sẽ đặt lại UID và GID hiệu dụng của tiến trình con thành UID và GID thực của tiến trình cha. Nếu đối số là ``False``, tiến trình con sẽ giữ nguyên UID và GID hiệu dụng của tiến trình cha. Trong cả hai trường hợp, nếu các bit quyền set-user-ID và set-group-ID được bật trên tệp thực thi, tác động của chúng sẽ ghi đè thiết lập UID và GID hiệu dụng. Đối số này tương ứng với cờ :c:macro:`!POSIX_SPAWN_RESETIDS` của thư viện C.

   Nếu đối số *setsid* là ``True``, đối số này sẽ tạo một session ID mới cho ``posix_spawn``. *setsid* yêu cầu cờ :c:macro:`!POSIX_SPAWN_SETSID` hoặc :c:macro:`!POSIX_SPAWN_SETSID_NP`. Nếu không, sẽ phát sinh :exc:`NotImplementedError`.

   Đối số *setsigmask* sẽ đặt signal mask thành tập tín hiệu được chỉ định. Nếu không sử dụng tham số này, tiến trình con sẽ kế thừa signal mask của tiến trình cha. Đối số này tương ứng với thư viện C
   cờ :c:macro:`!POSIX_SPAWN_SETSIGMASK`.

   Đối số *sigdef* sẽ đặt lại disposition của tất cả tín hiệu trong tập được chỉ định. Đối số này tương ứng với thư viện C
   cờ :c:macro:`!POSIX_SPAWN_SETSIGDEF`.

   Đối số *scheduler* phải là một tuple chứa policy của scheduler (tùy chọn) và một thực thể của :class:`sched_param` với các tham số của scheduler. Giá trị ``None`` ở vị trí của policy của scheduler cho biết policy này không được cung cấp. Đối số này là sự kết hợp của các cờ
   :c:macro:`!POSIX_SPAWN_SETSCHEDPARAM` và :c:macro:`!POSIX_SPAWN_SETSCHEDULER` của thư viện C.

   .. audit-event:: os.posix_spawn path,argv,env os.posix_spawn

   .. versionadded:: 3.8

   .. versionchanged:: 3.13
      Tham số *env* chấp nhận ``None``. ``os.POSIX_SPAWN_CLOSEFROM`` khả dụng trên các nền tảng mà
      :c:func:`!posix_spawn_file_actions_addclosefrom_np` tồn tại.

   .. availability:: Unix, not WASI, not Android, not iOS.

.. function:: posix_spawnp(path, argv, env, *, file_actions=None, \
                          setpgroup=None, resetids=False, setsid=False, setsigmask=(), \ setsigdef=(), scheduler=None)

   Bọc API thư viện C :c:func:`!posix_spawnp` để sử dụng từ Python.

   Tương tự :func:`posix_spawn`, ngoại trừ việc hệ thống tìm tệp *executable* trong danh sách các thư mục được chỉ định bởi
   biến môi trường :envvar:`PATH` (giống như đối với ``execvp(3)``).

   .. audit-event:: os.posix_spawn path,argv,env os.posix_spawnp

   .. versionadded:: 3.8

   .. availability:: POSIX, not WASI, not Android, not iOS.

      Xem tài liệu :func:`posix_spawn`.


.. function:: register_at_fork(*, before=None, after_in_parent=None, \
                               after_in_child=None)

   Đăng ký các callable sẽ được thực thi khi một tiến trình con mới được fork bằng :func:`os.fork` hoặc các API nhân bản tiến trình tương tự. Các tham số là tùy chọn và chỉ có thể được truyền dưới dạng keyword. Mỗi tham số xác định một thời điểm gọi khác nhau.

   * *before* là một hàm được gọi trước khi fork một tiến trình con.
   * *after_in_parent* là một hàm được gọi từ tiến trình cha sau khi fork một tiến trình con.
   * *after_in_child* là một hàm được gọi từ tiến trình con.

   Các lệnh gọi này chỉ được thực hiện nếu dự kiến quyền điều khiển sẽ quay lại trình thông dịch Python. Một lần khởi chạy :mod:`subprocess` điển hình sẽ không kích hoạt chúng vì tiến trình con sẽ không quay lại trình thông dịch.

   Các hàm được đăng ký để thực thi trước khi fork sẽ được gọi theo thứ tự đăng ký ngược lại. Các hàm được đăng ký để thực thi sau khi fork (dù trong tiến trình cha hay tiến trình con) sẽ được gọi theo thứ tự đăng ký.

   Lưu ý rằng các lệnh gọi :c:func:`fork` được thực hiện bởi mã C của bên thứ ba có thể không gọi các hàm đó, trừ khi mã này gọi :c:func:`PyOS_BeforeFork` một cách tường minh,
   :c:func:`PyOS_AfterFork_Parent` và :c:func:`PyOS_AfterFork_Child`.

   Không có cách nào để hủy đăng ký một hàm.

   .. availability:: Unix, not WASI, not Android, not iOS.

   .. versionadded:: 3.7


.. function:: spawnl(mode, path, ...)
              spawnle(mode, path, ..., env) spawnlp(mode, file, ...) spawnlpe(mode, file, ..., env) spawnv(mode, path, args) spawnve(mode, path, args, env) spawnvp(mode, file, args) spawnvpe(mode, file, args, env)

   Thực thi chương trình *path* trong một process mới.

   (Lưu ý rằng module :mod:`subprocess` cung cấp các chức năng mạnh mẽ hơn để khởi chạy process mới và truy xuất kết quả của chúng; nên sử dụng module đó thay cho các hàm này. Đặc biệt, hãy xem phần
   :ref:`subprocess-replacements`.)

   Nếu *mode* là :const:`P_NOWAIT`, hàm này trả về mã tiến trình của tiến trình mới; nếu *mode* là :const:`P_WAIT`, hàm trả về mã thoát của tiến trình nếu tiến trình thoát bình thường, hoặc ``-signal``, trong đó *signal* là tín hiệu đã kết thúc tiến trình. Trên Windows, mã tiến trình thực tế sẽ là process handle, nên có thể được sử dụng với hàm :func:`waitpid`.

   Lưu ý rằng trên VxWorks, hàm này không trả về ``-signal`` khi tiến trình mới bị kết thúc. Thay vào đó, hàm sẽ raise OSError exception.

   Các biến thể "l" và "v" của các hàm :func:`spawn\* <spawnl>` khác nhau ở cách truyền các đối số dòng lệnh. Các biến thể "l" có lẽ dễ sử dụng nhất nếu số lượng tham số được cố định khi viết code; các tham số riêng lẻ đơn giản trở thành những tham số bổ sung cho
   các hàm :func:`!spawnl\*`. Các biến thể "v" phù hợp khi số lượng tham số thay đổi, trong đó các đối số được truyền trong một list hoặc tuple dưới dạng tham số *args*. Trong cả hai trường hợp, các đối số của tiến trình con phải bắt đầu bằng tên của command đang được chạy.

   Các biến thể có chứa chữ "p" thứ hai ở gần cuối (:func:`spawnlp`,
   :func:`spawnlpe`, :func:`spawnvp` và :func:`spawnvpe`) sẽ sử dụng
   biến môi trường :envvar:`PATH` để định vị chương trình *file*. Khi môi trường được thay thế (bằng một trong các biến thể :func:`spawn\*e <spawnl>`, được thảo luận trong đoạn tiếp theo), môi trường mới sẽ được sử dụng làm nguồn của biến :envvar:`PATH`. Các biến thể khác, :func:`spawnl`,
   :func:`spawnle`, :func:`spawnv` và :func:`spawnve` sẽ không sử dụng
   biến :envvar:`PATH` để định vị tệp thực thi; *path* phải chứa một đường dẫn tuyệt đối hoặc tương đối phù hợp.

   Đối với :func:`spawnle`, :func:`spawnlpe`, :func:`spawnve` và :func:`spawnvpe` (lưu ý rằng tất cả các hàm này đều kết thúc bằng "e"), tham số *env* phải là một mapping được dùng để xác định các biến môi trường cho process mới (chúng được sử dụng thay cho môi trường của process hiện tại); các hàm
   :func:`spawnl`, :func:`spawnlp`, :func:`spawnv` và :func:`spawnvp` đều khiến process mới kế thừa môi trường của process hiện tại. Lưu ý rằng các khóa và giá trị trong dictionary *env* phải là các chuỗi; các khóa hoặc giá trị không hợp lệ sẽ khiến hàm thất bại và trả về ``127``.

   Ví dụ, các lệnh gọi sau đây đến :func:`spawnlp` và :func:`spawnvpe` là tương đương::

      import os
      os.spawnlp(os.P_WAIT, 'cp', 'cp', 'index.html', '/dev/null')

      L = ['cp', 'index.html', '/dev/null']
      os.spawnvpe(os.P_WAIT, 'cp', L, os.environ)

   .. audit-event:: os.spawn mode,path,args,env os.spawnl

   .. availability:: Unix, Windows, not WASI, not Android, not iOS.

      :func:`spawnlp`, :func:`spawnlpe`, :func:`spawnvp` và :func:`spawnvpe` không khả dụng trên Windows. :func:`spawnle` và
      :func:`spawnve` không thread-safe trên Windows; chúng tôi khuyên bạn nên sử dụng
      module :mod:`subprocess` thay vào đó.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.

   .. soft-deprecated:: 3.14
      Thay vào đó, nên sử dụng module :mod:`subprocess`.


.. data:: P_NOWAIT
          P_NOWAITO

   Các giá trị có thể có của tham số *mode* thuộc nhóm hàm :func:`spawn\* <spawnl>`. Nếu cung cấp một trong hai giá trị này, các hàm :func:`spawn\* <spawnl>` sẽ trả về ngay sau khi tiến trình mới được tạo, với ID tiến trình là giá trị trả về.

   .. availability:: Unix, Windows.


.. data:: P_WAIT

   Giá trị có thể có của tham số *mode* thuộc nhóm hàm :func:`spawn\* <spawnl>`. Nếu được cung cấp dưới dạng *mode*, các hàm :func:`spawn\* <spawnl>` sẽ không trả về cho đến khi tiến trình mới chạy xong và sẽ trả về mã thoát của tiến trình nếu tiến trình chạy thành công, hoặc ``-signal`` nếu một signal kết thúc tiến trình.

   .. availability:: Unix, Windows.


.. data:: P_DETACH
          P_OVERLAY

   Các giá trị có thể có của tham số *mode* cho nhóm hàm :func:`spawn\* <spawnl>`. Các giá trị này kém khả chuyển hơn những giá trị được liệt kê ở trên. :const:`P_DETACH` tương tự như :const:`P_NOWAIT`, nhưng tiến trình mới được tách khỏi console của tiến trình gọi. Nếu sử dụng :const:`P_OVERLAY`, tiến trình hiện tại sẽ bị thay thế; hàm :func:`spawn\* <spawnl>` sẽ không trả về.

   .. availability:: Windows.


.. function:: startfile(path, [operation], [arguments], [cwd], [show_cmd])

   Khởi động một tệp bằng ứng dụng liên kết với tệp đó.

   Khi không chỉ định *operation*, thao tác này hoạt động giống như việc bấm đúp vào tệp trong Windows Explorer hoặc truyền tên tệp làm đối số cho
   lệnh :program:`start` trong command shell tương tác: tệp được mở bằng ứng dụng (nếu có) được liên kết với phần mở rộng của tệp.

   Khi cung cấp một *operation* khác, giá trị này phải là một "command verb" chỉ định thao tác cần thực hiện với tệp. Các verb phổ biến được Microsoft ghi lại gồm ``'open'``, ``'print'`` và ``'edit'`` (dùng cho tệp), cũng như ``'explore'`` và ``'find'`` (dùng cho thư mục).

   Khi khởi chạy một ứng dụng, hãy chỉ định *arguments* để truyền dưới dạng một chuỗi duy nhất. Đối số này có thể không có tác dụng khi sử dụng hàm này để khởi chạy một tài liệu.

   Thư mục làm việc mặc định được kế thừa, nhưng có thể được ghi đè bằng đối số *cwd*. Đây phải là một đường dẫn tuyệt đối. *path* tương đối sẽ được phân giải dựa trên đối số này.

   Sử dụng *show_cmd* để ghi đè kiểu cửa sổ mặc định. Việc này có hiệu lực hay không sẽ phụ thuộc vào ứng dụng được khởi chạy. Các giá trị là số nguyên được hàm Win32 :c:func:`!ShellExecute` hỗ trợ.

   :func:`startfile` trả về ngay sau khi ứng dụng liên kết được khởi chạy. Không có tùy chọn chờ ứng dụng đóng và cũng không có cách nào lấy trạng thái thoát của ứng dụng. Tham số *path* được tính tương đối so với thư mục hiện tại hoặc *cwd*. Nếu muốn sử dụng đường dẫn tuyệt đối, hãy đảm bảo ký tự đầu tiên không phải là dấu gạch chéo (``'/'``) Sử dụng :mod:`pathlib` hoặc
   hàm :func:`os.path.normpath` để đảm bảo các đường dẫn được mã hóa đúng cách cho Win32.

   Để giảm chi phí khởi động interpreter, hàm Win32 :c:func:`!ShellExecute` chỉ được phân giải khi hàm này được gọi lần đầu. Nếu không thể phân giải hàm, :exc:`NotImplementedError` sẽ được đưa ra.

   .. audit-event:: os.startfile path,operation os.startfile

   .. audit-event:: os.startfile/2 path,operation,arguments,cwd,show_cmd os.startfile

   .. availability:: Windows.

   .. versionchanged:: 3.10
      Đã thêm các đối số *arguments*, *cwd* và *show_cmd*, cùng với sự kiện audit ``os.startfile/2``.


.. function:: system(command)

   Thực thi lệnh (một chuỗi) trong một subshell. Việc này được triển khai bằng cách gọi hàm Standard C :c:func:`system` và có cùng các hạn chế. Các thay đổi đối với :data:`sys.stdin`, v.v. không được phản ánh trong môi trường của lệnh được thực thi. Nếu *command* tạo ra bất kỳ đầu ra nào, đầu ra đó sẽ được gửi đến luồng đầu ra chuẩn của interpreter. Tiêu chuẩn C không quy định ý nghĩa của giá trị trả về từ hàm C, vì vậy giá trị trả về của hàm Python phụ thuộc vào hệ thống.

   Trên Unix, giá trị trả về là trạng thái thoát của tiến trình, được mã hóa theo định dạng được chỉ định cho :func:`wait`.

   Trên Windows, giá trị trả về là giá trị do shell hệ thống trả về sau khi chạy *command*. Shell được chỉ định bởi biến môi trường Windows
   :envvar:`COMSPEC`: thông thường là :program:`cmd.exe`, trả về trạng thái thoát của command đã chạy; trên các hệ thống sử dụng shell không phải shell gốc, hãy tham khảo tài liệu về shell của bạn.

   Mô-đun :mod:`subprocess` cung cấp các khả năng mạnh mẽ hơn để tạo process mới và truy xuất kết quả của chúng; nên sử dụng mô-đun đó thay vì hàm này. Xem phần :ref:`subprocess-replacements` trong tài liệu :mod:`subprocess` để biết một số công thức hữu ích.

   Trên Unix, có thể sử dụng :func:`waitstatus_to_exitcode` để chuyển đổi kết quả (trạng thái thoát) thành mã thoát. Trên Windows, kết quả chính là mã thoát.

   .. audit-event:: os.system command os.system

   .. availability:: Unix, Windows, not WASI, not Android, not iOS.


.. function:: times()

   Trả về thời gian process toàn cục hiện tại. Giá trị trả về là một object có năm thuộc tính:

   * :attr:`!user` - thời gian người dùng
   * :attr:`!system` - thời gian hệ thống
   * :attr:`!children_user` - thời gian người dùng của tất cả tiến trình con
   * :attr:`!children_system` - thời gian hệ thống của tất cả tiến trình con
   * :attr:`!elapsed` - thời gian thực đã trôi qua kể từ một thời điểm cố định trong quá khứ

   Để tương thích ngược, đối tượng này cũng hoạt động như một bộ năm phần tử chứa :attr:`!user`, :attr:`!system`, :attr:`!children_user`,
   :attr:`!children_system`, và :attr:`!elapsed` theo thứ tự đó.

   Xem trang hướng dẫn Unix
   :manpage:`times(2)` và `times(3) <https://man.freebsd.org/cgi/man.cgi?time(3)>`_ trên Unix hoặc `GetProcessTimes MSDN <https://docs.microsoft.com/windows/win32/api/processthreadsapi/nf-processthreadsapi-getprocesstimes>`_ trên Windows. Trên Windows, chỉ biết được :attr:`!user` và :attr:`!system`; các thuộc tính khác đều bằng không.

   .. availability:: Unix, Windows.

   .. versionchanged:: 3.3
      Kiểu trả về đã được thay đổi từ một tuple thành một đối tượng tương tự tuple với các thuộc tính được đặt tên.


.. function:: wait()

   Chờ một tiến trình con hoàn tất và trả về một tuple chứa pid của tiến trình cùng thông tin chỉ báo trạng thái thoát: một số 16 bit, trong đó byte thấp là số hiệu tín hiệu đã kết thúc tiến trình, còn byte cao là trạng thái thoát (nếu số hiệu tín hiệu bằng không); bit cao nhất của byte thấp được đặt nếu một tệp core được tạo.

   Nếu không có tiến trình con nào có thể chờ, :exc:`ChildProcessError` sẽ được nâng lên.

   Có thể dùng :func:`waitstatus_to_exitcode` để chuyển đổi trạng thái thoát thành mã thoát.

   .. availability:: Unix, not WASI, not Android, not iOS.

   .. seealso::

      Các hàm :func:`!wait*` khác được mô tả bên dưới có thể được dùng để chờ một tiến trình con cụ thể hoàn tất và cung cấp nhiều tùy chọn hơn.
      :func:`waitpid` là hàm duy nhất cũng có trên Windows.


.. function:: waitid(idtype, id, options, /)

   Chờ một tiến trình con hoàn tất.

   *idtype* có thể là :data:`P_PID`, :data:`P_PGID`, :data:`P_ALL` hoặc (trên Linux) :data:`P_PIDFD`. Cách diễn giải *id* phụ thuộc vào giá trị này; hãy xem phần mô tả riêng của từng loại.

   *options* là sự kết hợp OR của các flag. Ít nhất một trong các flag :data:`WEXITED`,
   :data:`WSTOPPED` hoặc :data:`WCONTINUED` là bắt buộc;
   :data:`WNOHANG` và :data:`WNOWAIT` là các flag tùy chọn bổ sung.

   Giá trị trả về là một đối tượng biểu diễn dữ liệu chứa trong
   cấu trúc :c:type:`siginfo_t` với các thuộc tính sau:

   * :attr:`!si_pid` (process ID)
   * :attr:`!si_uid` (ID người dùng thực của tiến trình con)
   * :attr:`!si_signo` (luôn là :const:`~signal.SIGCHLD`)
   * :attr:`!si_status` (trạng thái thoát hoặc số hiệu tín hiệu, tùy thuộc vào :attr:`!si_code`)
   * :attr:`!si_code` (xem :data:`CLD_EXITED` để biết các giá trị có thể có)

   Nếu :data:`WNOHANG` được chỉ định và không có tiến trình con nào khớp với trạng thái được yêu cầu, ``None`` sẽ được trả về. Ngược lại, nếu không có tiến trình con nào khớp mà có thể chờ, :exc:`ChildProcessError` sẽ được phát sinh.

   .. availability:: Unix, not WASI, not Android, not iOS.

   .. versionadded:: 3.3

   .. versionchanged:: 3.13
      Hàm này hiện cũng có trên macOS.


.. function:: waitpid(pid, options, /)

   Chi tiết của hàm này khác nhau trên Unix và Windows.

   Trên Unix: Chờ hoàn tất tiến trình con được chỉ định bằng mã tiến trình *pid*, và trả về một tuple chứa mã tiến trình cùng chỉ báo trạng thái thoát của tiến trình đó (được mã hóa như đối với :func:`wait`). Ngữ nghĩa của lệnh gọi bị ảnh hưởng bởi giá trị của số nguyên *options*, giá trị này phải là ``0`` để hoạt động bình thường.

   Nếu *pid* lớn hơn ``0``, :func:`waitpid` yêu cầu thông tin trạng thái của tiến trình cụ thể đó. Nếu *pid* là ``0``, yêu cầu dành cho trạng thái của bất kỳ tiến trình con nào trong process group của tiến trình hiện tại. Nếu *pid* là ``-1``, yêu cầu liên quan đến bất kỳ tiến trình con nào của tiến trình hiện tại. Nếu *pid* nhỏ hơn ``-1``, trạng thái được yêu cầu cho bất kỳ tiến trình nào trong process group ``-pid`` (giá trị tuyệt đối của *pid*).

   *options* là sự kết hợp OR của các flag. Nếu nó chứa :data:`WNOHANG` và không có tiến trình con phù hợp nào ở trạng thái được yêu cầu, ``(0, 0)`` được trả về. Nếu không, khi không có tiến trình con phù hợp nào có thể được chờ, :exc:`ChildProcessError` được phát sinh. Các tùy chọn khác có thể sử dụng là
   :data:`WUNTRACED` và :data:`WCONTINUED`.

   Trên Windows: Chờ hoàn tất tiến trình được chỉ định bằng process handle *pid*, và trả về một tuple chứa *pid* cùng trạng thái thoát của tiến trình đó, được dịch trái 8 bit (việc dịch này giúp hàm dễ sử dụng đa nền tảng hơn). *pid* nhỏ hơn hoặc bằng ``0`` không có ý nghĩa đặc biệt trên Windows và làm phát sinh một ngoại lệ. Giá trị của số nguyên *options* không có tác dụng. *pid* có thể tham chiếu đến bất kỳ tiến trình nào có mã tiến trình đã biết, không nhất thiết là tiến trình con. Các hàm :func:`spawn\* <spawnl>` được gọi với :const:`P_NOWAIT` sẽ trả về các process handle phù hợp.

   Có thể dùng :func:`waitstatus_to_exitcode` để chuyển đổi trạng thái thoát thành mã thoát.

   .. availability:: Unix, Windows, not WASI, not Android, not iOS.

   .. versionchanged:: 3.5
      Nếu system call bị gián đoạn và signal handler không phát sinh ngoại lệ, hàm hiện sẽ thử lại system call thay vì phát sinh một ngoại lệ
      ngoại lệ :exc:`InterruptedError` (xem :pep:`475` để biết lý do).


.. function:: wait3(options)

   Tương tự :func:`waitpid`, nhưng không cung cấp đối số process id và trả về một tuple gồm 3 phần tử chứa process id của tiến trình con, thông tin chỉ báo trạng thái thoát và thông tin sử dụng tài nguyên. Tham khảo
   :func:`resource.getrusage` để biết chi tiết về thông tin sử dụng tài nguyên. Đối số *options* giống với đối số được cung cấp cho :func:`waitpid` và
   :func:`wait4`.

   :func:`waitstatus_to_exitcode` có thể được dùng để chuyển đổi trạng thái thoát thành exitcode.

   .. availability:: Unix, not WASI, not Android, not iOS.


.. function:: wait4(pid, options)

   Tương tự :func:`waitpid`, nhưng trả về một tuple gồm 3 phần tử chứa process id của tiến trình con, thông tin chỉ báo trạng thái thoát và thông tin sử dụng tài nguyên. Tham khảo :func:`resource.getrusage` để biết chi tiết về thông tin sử dụng tài nguyên. Các đối số của :func:`wait4` giống với các đối số được cung cấp cho :func:`waitpid`.

   :func:`waitstatus_to_exitcode` có thể được dùng để chuyển đổi trạng thái thoát thành exitcode.

   .. availability:: Unix, not WASI, not Android, not iOS.


.. data:: P_PID
          P_PGID P_ALL P_PIDFD

   Sau đây là các giá trị có thể có cho *idtype* trong :func:`waitid`. Chúng ảnh hưởng đến cách diễn giải *id*:

   * :data:`!P_PID` - chờ tiến trình con có PID là *id*.
   * :data:`!P_PGID` - chờ bất kỳ tiến trình con nào có ID nhóm tiến trình là *id*.
   * :data:`!P_ALL` - chờ bất kỳ tiến trình con nào; bỏ qua *id*.
   * :data:`!P_PIDFD` - chờ tiến trình con được xác định bởi bộ mô tả tệp *id* (một bộ mô tả tệp tiến trình được tạo bằng :func:`pidfd_open`).

   .. availability:: Unix, not WASI, not Android, not iOS.

   .. note:: :data:`!P_PIDFD` chỉ khả dụng trên Linux >= 5.4.

   .. versionadded:: 3.3
   .. versionadded:: 3.9
      Hằng số :data:`!P_PIDFD`.


.. data:: WCONTINUED

   Cờ *options* này dành cho :func:`waitpid`, :func:`wait3`, :func:`wait4`, và
   :func:`waitid` khiến các tiến trình con được báo cáo nếu chúng đã được tiếp tục từ trạng thái dừng do job control kể từ lần cuối được báo cáo.

   .. availability:: Unix, not WASI, not Android, not iOS.


.. data:: WEXITED

   Cờ *options* này dành cho :func:`waitid` khiến các tiến trình con đã kết thúc được báo cáo.

   Các hàm ``wait*`` còn lại luôn báo cáo các tiến trình con đã kết thúc, vì vậy tùy chọn này không khả dụng cho chúng.

   .. availability:: Unix, not WASI, not Android, not iOS.

   .. versionadded:: 3.3


.. data:: WSTOPPED

   Cờ *options* này dành cho :func:`waitid` khiến các tiến trình con đã bị dừng do nhận một signal được báo cáo.

   Tùy chọn này không khả dụng cho các hàm ``wait*`` còn lại.

   .. availability:: Unix, not WASI, not Android, not iOS.

   .. versionadded:: 3.3


.. data:: WUNTRACED

   Cờ *options* này dành cho :func:`waitpid`, :func:`wait3`, và :func:`wait4` cũng khiến các tiến trình con được báo cáo nếu chúng đã bị dừng nhưng trạng thái hiện tại của chúng chưa được báo cáo kể từ khi bị dừng.

   Tùy chọn này không khả dụng cho :func:`waitid`.

   .. availability:: Unix, not WASI, not Android, not iOS.


.. data:: WNOHANG

   Cờ *options* này khiến :func:`waitpid`, :func:`wait3`, :func:`wait4`, và
   :func:`waitid` trả về ngay nếu không có trạng thái tiến trình con nào khả dụng ngay lập tức.

   .. availability:: Unix, not WASI, not Android, not iOS.


.. data:: WNOWAIT

   Cờ *options* này khiến :func:`waitid` để tiến trình con ở trạng thái có thể chờ, nhờ đó một lệnh gọi :func:`!wait*` sau đó có thể được dùng để truy xuất lại thông tin trạng thái của tiến trình con.

   Tùy chọn này không khả dụng cho các hàm ``wait*`` còn lại.

   .. availability:: Unix, not WASI, not Android, not iOS.


.. data:: CLD_EXITED
          CLD_KILLED CLD_DUMPED CLD_TRAPPED CLD_STOPPED CLD_CONTINUED

   Đây là các giá trị có thể có của :attr:`!si_code` trong kết quả được trả về bởi
   :func:`waitid`.

   .. availability:: Unix, not WASI, not Android, not iOS.

   .. versionadded:: 3.3

   .. versionchanged:: 3.9
      Đã thêm các giá trị :data:`CLD_KILLED` và :data:`CLD_STOPPED`.


.. function:: waitstatus_to_exitcode(status)

   Chuyển đổi trạng thái chờ thành mã thoát.

   Trên Unix:

   * Nếu tiến trình thoát bình thường (nếu ``WIFEXITED(status)`` là true), trả về trạng thái thoát của tiến trình (trả về ``WEXITSTATUS(status)``): kết quả lớn hơn hoặc bằng 0.
   * Nếu tiến trình bị kết thúc bởi một tín hiệu (nếu ``WIFSIGNALED(status)`` là true), trả về ``-signum``, trong đó *signum* là số hiệu của tín hiệu khiến tiến trình kết thúc (trả về ``-WTERMSIG(status)``): kết quả nhỏ hơn 0.
   * Nếu không, phát sinh một :exc:`ValueError`.

   Trên Windows, trả về *status* được dịch phải 8 bit.

   Trên Unix, nếu tiến trình đang được trace hoặc nếu :func:`waitpid` được gọi với tùy chọn :data:`WUNTRACED`, trước tiên caller phải kiểm tra xem ``WIFSTOPPED(status)`` có phải là true hay không. Không được gọi hàm này nếu ``WIFSTOPPED(status)`` là true.

   .. seealso::

      :func:`WIFEXITED`, :func:`WEXITSTATUS`, :func:`WIFSIGNALED`,
      Các hàm :func:`WTERMSIG`, :func:`WIFSTOPPED`, :func:`WSTOPSIG`.

   .. availability:: Unix, Windows, not WASI, not Android, not iOS.

   .. versionadded:: 3.9


Các hàm sau đây nhận mã trạng thái tiến trình do hàm trả về
:func:`system`, :func:`wait` hoặc :func:`waitpid` làm tham số. Có thể dùng chúng để xác định trạng thái của một tiến trình.

.. function:: WCOREDUMP(status, /)

   Trả về ``True`` nếu một core dump được tạo cho tiến trình, nếu không thì trả về ``False``.

   Chỉ nên sử dụng hàm này nếu :func:`WIFSIGNALED` là true.

   .. availability:: Unix, not WASI, not Android, not iOS.


.. function:: WIFCONTINUED(status)

   Trả về ``True`` nếu một tiến trình con bị dừng đã được tiếp tục nhờ việc phân phối
   :const:`~signal.SIGCONT` (nếu tiến trình được tiếp tục sau khi bị dừng bởi điều khiển công việc), nếu không thì trả về ``False``.

   Xem tùy chọn :data:`WCONTINUED`.

   .. availability:: Unix, not WASI, not Android, not iOS.


.. function:: WIFSTOPPED(status)

   Trả về ``True`` nếu tiến trình bị dừng do nhận một signal, nếu không thì trả về ``False``.

   :func:`WIFSTOPPED` chỉ trả về ``True`` nếu lệnh gọi :func:`waitpid` được thực hiện bằng tùy chọn :data:`WUNTRACED` hoặc khi tiến trình đang được trace (xem
   :manpage:`ptrace(2)`).

   .. availability:: Unix, not WASI, not Android, not iOS.

.. function:: WIFSIGNALED(status)

   Trả về ``True`` nếu tiến trình bị kết thúc bởi một signal, nếu không thì trả về ``False``.

   .. availability:: Unix, not WASI, not Android, not iOS.


.. function:: WIFEXITED(status)

   Trả về ``True`` nếu tiến trình kết thúc bình thường, tức là bằng cách gọi ``exit()`` hoặc ``_exit()``, hoặc bằng cách trả về từ ``main()``; nếu không thì trả về ``False``.

   .. availability:: Unix, not WASI, not Android, not iOS.


.. function:: WEXITSTATUS(status)

   Trả về trạng thái thoát của tiến trình.

   Chỉ nên sử dụng hàm này nếu :func:`WIFEXITED` là true.

   .. availability:: Unix, not WASI, not Android, not iOS.


.. function:: WSTOPSIG(status)

   Trả về signal khiến tiến trình dừng lại.

   Chỉ nên sử dụng hàm này nếu :func:`WIFSTOPPED` là true.

   .. availability:: Unix, not WASI, not Android, not iOS.


.. function:: WTERMSIG(status)

   Trả về số hiệu của signal khiến tiến trình kết thúc.

   Chỉ nên sử dụng hàm này nếu :func:`WIFSIGNALED` là true.

   .. availability:: Unix, not WASI, not Android, not iOS.


Giao diện với bộ lập lịch
-------------------------

Các hàm này kiểm soát cách hệ điều hành phân bổ thời gian CPU cho một tiến trình. Chúng chỉ khả dụng trên một số nền tảng Unix. Để biết thông tin chi tiết hơn, hãy tham khảo các trang man của Unix.

.. versionadded:: 3.3

Các chính sách lập lịch sau đây được cung cấp nếu hệ điều hành hỗ trợ chúng.

.. _os-scheduling-policy:

.. data:: SCHED_OTHER

   Chính sách lập lịch mặc định.

.. data:: SCHED_BATCH

   Chính sách lập lịch cho các tiến trình sử dụng nhiều CPU, cố gắng duy trì tính tương tác của các phần còn lại trên máy tính.

.. data:: SCHED_DEADLINE

   Chính sách lập lịch cho các tác vụ có ràng buộc về thời hạn.

   .. versionadded:: 3.14

.. data:: SCHED_IDLE

   Chính sách lập lịch cho các tác vụ nền có độ ưu tiên cực thấp.

.. data:: SCHED_NORMAL

   Bí danh của :data:`SCHED_OTHER`.

   .. versionadded:: 3.14

.. data:: SCHED_SPORADIC

   Chính sách lập lịch cho các chương trình sporadic server.

.. data:: SCHED_FIFO

   Một chính sách lập lịch First In First Out.

.. data:: SCHED_RR

   Một chính sách lập lịch round-robin.

.. data:: SCHED_RESET_ON_FORK

   Cờ này có thể được OR với bất kỳ chính sách lập lịch nào khác. Khi một process có cờ này được thiết lập thực hiện fork, chính sách lập lịch và độ ưu tiên của process con sẽ được đặt lại về mặc định.


.. class:: sched_param(sched_priority)

   Lớp này biểu diễn các tham số lập lịch có thể điều chỉnh được sử dụng trong
   :func:`sched_setparam`, :func:`sched_setscheduler`, và
   :func:`sched_getparam`. Lớp này là bất biến.

   Hiện tại, chỉ có một tham số khả dụng:

   .. attribute:: sched_priority

      Mức ưu tiên lập lịch cho một chính sách lập lịch.


.. function:: sched_get_priority_min(policy)

   Lấy giá trị ưu tiên tối thiểu cho *policy*. *policy* là một trong các hằng số chính sách lập lịch ở trên.


.. function:: sched_get_priority_max(policy)

   Lấy giá trị ưu tiên tối đa cho *policy*. *policy* là một trong các hằng số chính sách lập lịch ở trên.


.. function:: sched_setscheduler(pid, policy, param, /)

   Đặt chính sách lập lịch cho tiến trình có PID *pid*. Giá trị *pid* bằng 0 có nghĩa là tiến trình đang gọi. *policy* là một trong các hằng số chính sách lập lịch ở trên. *param* là một thực thể :class:`sched_param`.


.. function:: sched_getscheduler(pid, /)

   Trả về chính sách lập lịch cho tiến trình có PID *pid*. Giá trị *pid* bằng 0 có nghĩa là tiến trình đang gọi. Kết quả là một trong các hằng số chính sách lập lịch ở trên.


.. function:: sched_setparam(pid, param, /)

   Đặt các tham số lập lịch cho tiến trình có PID *pid*. Giá trị *pid* bằng 0 có nghĩa là tiến trình đang gọi. *param* là một thực thể :class:`sched_param`.


.. function:: sched_getparam(pid, /)

   Trả về các tham số lập lịch dưới dạng một thực thể :class:`sched_param` cho tiến trình có PID *pid*. Giá trị *pid* bằng 0 có nghĩa là tiến trình đang gọi.


.. function:: sched_rr_get_interval(pid, /)

   Trả về quantum round-robin tính bằng giây cho tiến trình có PID *pid*. *pid* bằng 0 nghĩa là tiến trình đang gọi.


.. function:: sched_yield()

   Tự nguyện nhường CPU. Xem :manpage:`sched_yield(2)` để biết chi tiết.


.. function:: sched_setaffinity(pid, mask, /)

   Giới hạn tiến trình có PID *pid* (hoặc tiến trình hiện tại nếu bằng 0) vào một tập CPU. *mask* là một iterable gồm các số nguyên biểu thị tập CPU mà tiến trình bị giới hạn sử dụng.


.. function:: sched_getaffinity(pid, /)

   Trả về tập CPU mà tiến trình có PID *pid* bị giới hạn sử dụng.

   Nếu *pid* bằng 0, trả về tập CPU mà thread đang gọi của tiến trình hiện tại bị giới hạn sử dụng.

   Xem thêm hàm :func:`process_cpu_count`.


.. _os-path:

Thông tin hệ thống khác
-----------------------


.. function:: confstr(name, /)

   Trả về các giá trị cấu hình hệ thống dạng chuỗi. *name* chỉ định giá trị cấu hình cần truy xuất; đây có thể là một chuỗi chứa tên của một giá trị hệ thống đã được định nghĩa; các tên này được quy định trong một số tiêu chuẩn (POSIX, Unix 95, Unix 98 và các tiêu chuẩn khác). Một số nền tảng cũng định nghĩa thêm các tên khác. Các tên được hệ điều hành máy chủ nhận biết được cung cấp dưới dạng các khóa của dictionary ``confstr_names``. Đối với các biến cấu hình không có trong ánh xạ đó, cũng có thể truyền một số nguyên cho *name*.

   Nếu giá trị cấu hình được chỉ định bởi *name* chưa được định nghĩa, ``None`` sẽ được trả về.

   Nếu *name* là một chuỗi và không được nhận biết, :exc:`ValueError` sẽ được phát sinh. Nếu một giá trị cụ thể của *name* không được hệ thống máy chủ hỗ trợ, ngay cả khi giá trị đó có trong ``confstr_names``, một :exc:`OSError` sẽ được phát sinh với
   :const:`errno.EINVAL` cho số hiệu lỗi.

   .. availability:: Unix.


.. data:: confstr_names

   Dictionary ánh xạ các tên được :func:`confstr` chấp nhận với các giá trị số nguyên mà hệ điều hành máy chủ định nghĩa cho những tên đó. Có thể sử dụng dictionary này để xác định tập hợp các tên mà hệ thống nhận biết.

   .. availability:: Unix.


.. function:: cpu_count()

   Trả về số lượng CPU logic trong **hệ thống**. Trả về ``None`` nếu không xác định được.

   Có thể sử dụng hàm :func:`process_cpu_count` để lấy số lượng CPU logic mà luồng gọi của **quy trình hiện tại** có thể sử dụng.

   .. versionadded:: 3.4

   .. versionchanged:: 3.13
      Nếu :option:`-X cpu_count <-X>` được cung cấp hoặc :envvar:`PYTHON_CPU_COUNT` được đặt,
      :func:`cpu_count` trả về giá trị ghi đè *n*.


.. function:: getloadavg()

   Trả về số lượng tiến trình trong hàng đợi chạy của hệ thống, được tính trung bình trong 1, 5 và 15 phút gần nhất, hoặc phát sinh :exc:`OSError` nếu không thể lấy được giá trị trung bình tải.

   .. availability:: Unix.


.. function:: process_cpu_count()

   Lấy số lượng CPU logic mà thread gọi của **tiến trình hiện tại** có thể sử dụng. Trả về ``None`` nếu không xác định được. Giá trị này có thể nhỏ hơn
   :func:`cpu_count` tùy thuộc vào CPU affinity.

   Có thể sử dụng hàm :func:`cpu_count` để lấy số lượng CPU logic trong **hệ thống**.

   Nếu :option:`-X cpu_count <-X>` được cung cấp hoặc :envvar:`PYTHON_CPU_COUNT` được đặt,
   :func:`process_cpu_count` trả về giá trị ghi đè *n*.

   Xem thêm hàm :func:`sched_getaffinity`.

   .. versionadded:: 3.13


.. function:: sysconf(name, /)

   Trả về các giá trị cấu hình hệ thống dạng số nguyên. Nếu giá trị cấu hình được chỉ định bởi *name* chưa được định nghĩa, ``-1`` sẽ được trả về. Các nhận xét về tham số *name* của :func:`confstr` cũng áp dụng ở đây; từ điển cung cấp thông tin về các tên đã biết được xác định bởi ``sysconf_names``.

   .. availability:: Unix.


.. data:: sysconf_names

   Từ điển ánh xạ các tên được :func:`sysconf` chấp nhận tới các giá trị số nguyên được hệ điều hành máy chủ xác định cho những tên đó. Có thể sử dụng từ điển này để xác định tập hợp các tên mà hệ thống biết.

   .. availability:: Unix.

   .. versionchanged:: 3.11
      Thêm tên ``'SC_MINSIGSTKSZ'``.

Các giá trị dữ liệu sau được dùng để hỗ trợ các thao tác xử lý đường dẫn. Chúng được xác định trên mọi nền tảng.

Các thao tác cấp cao hơn trên tên đường dẫn được định nghĩa trong mô-đun :mod:`os.path`.


.. index:: single: . (dot); in pathnames
.. data:: curdir

   Chuỗi hằng được hệ điều hành sử dụng để tham chiếu đến thư mục hiện tại. Đây là ``'.'`` trên Windows và POSIX. Cũng có thể truy cập qua
   :mod:`os.path`.


.. index:: single: ..; in pathnames
.. data:: pardir

   Chuỗi hằng được hệ điều hành sử dụng để tham chiếu đến thư mục cha. Đây là ``'..'`` trên Windows và POSIX. Cũng có thể truy cập qua
   :mod:`os.path`.


.. index:: single: / (slash); in pathnames
.. index:: single: \ (backslash); in pathnames (Windows)
.. data:: sep

   Ký tự được hệ điều hành sử dụng để phân tách các thành phần của tên đường dẫn. Đây là ``'/'`` trên POSIX và ``'\\'`` trên Windows. Lưu ý rằng chỉ biết ký tự này là chưa đủ để phân tích cú pháp hoặc nối các tên đường dẫn --- hãy sử dụng
   :func:`os.path.split` và :func:`os.path.join` --- tuy nhiên, đôi khi nó vẫn hữu ích. Cũng có thể truy cập qua :mod:`os.path`.


.. index:: single: / (slash); in pathnames
.. data:: altsep

   Ký tự thay thế được hệ điều hành sử dụng để phân tách các thành phần của tên đường dẫn, hoặc ``None`` nếu chỉ có một ký tự phân tách. Giá trị này là ``'/'`` trên các hệ thống Windows, nơi ``sep`` là dấu gạch chéo ngược. Cũng có thể truy cập qua
   :mod:`os.path`.


.. index:: single: . (dot); in pathnames
.. data:: extsep

   Ký tự phân tách tên tệp cơ sở khỏi phần mở rộng; ví dụ: ``'.'`` trong :file:`os.py`. Cũng có thể truy cập qua :mod:`os.path`.


.. index:: single: : (colon); path separator (POSIX)
   single: ; (semicolon)
.. data:: pathsep

   Ký tự thường được hệ điều hành sử dụng để phân tách các thành phần của đường dẫn tìm kiếm (như trong :envvar:`PATH`), chẳng hạn ``':'`` trên POSIX hoặc ``';'`` trên Windows. Cũng có thể truy cập qua :mod:`os.path`.


.. data:: defpath

   Đường dẫn tìm kiếm mặc định được :func:`exec\*p\* <execl>` và
   :func:`spawn\*p\* <spawnl>` sử dụng nếu môi trường không có khóa ``'PATH'``. Cũng có sẵn thông qua :mod:`os.path`.


.. data:: linesep

   Chuỗi được dùng để phân tách (hay đúng hơn là kết thúc) các dòng trên nền tảng hiện tại. Chuỗi này có thể là một ký tự đơn, chẳng hạn như ``'\n'`` trên POSIX, hoặc nhiều ký tự, ví dụ ``'\r\n'`` trên Windows. Không sử dụng *os.linesep* làm ký tự kết thúc dòng khi ghi các tệp được mở ở chế độ văn bản (mặc định); hãy sử dụng một ``'\n'`` duy nhất trên mọi nền tảng.


.. data:: devnull

   Đường dẫn tệp của thiết bị null. Ví dụ: ``'/dev/null'`` trên POSIX, ``'nul'`` trên Windows. Cũng có sẵn thông qua :mod:`os.path`.

.. data:: RTLD_LAZY
          RTLD_NOW RTLD_GLOBAL RTLD_LOCAL RTLD_NODELETE RTLD_NOLOAD RTLD_DEEPBIND

   Các cờ dùng với các hàm :func:`~sys.setdlopenflags` và
   :func:`~sys.getdlopenflags`. Xem trang hướng dẫn Unix
   :manpage:`dlopen(3)` để biết ý nghĩa của các cờ khác nhau.

   .. versionadded:: 3.3


Số ngẫu nhiên
-------------


.. function:: getrandom(size, flags=0)

   Nhận tối đa *size* byte ngẫu nhiên. Hàm có thể trả về ít byte hơn số lượng được yêu cầu.

   Các byte này có thể được dùng để khởi tạo các bộ tạo số ngẫu nhiên trong user space hoặc cho mục đích mật mã.

   ``getrandom()`` dựa vào entropy thu thập từ các driver thiết bị và những nguồn nhiễu môi trường khác. Việc đọc một lượng dữ liệu lớn không cần thiết sẽ gây ảnh hưởng tiêu cực đến những người dùng khác của các thiết bị ``/dev/random`` và ``/dev/urandom``.

   Đối số flags là một bit mask có thể chứa không hoặc nhiều giá trị sau, được kết hợp bằng phép OR: :py:const:`os.GRND_RANDOM` và
   :py:data:`GRND_NONBLOCK`.

   Xem thêm `trang hướng dẫn Linux về getrandom() <https://man7.org/linux/man-pages/man2/getrandom.2.html>`_.

   .. availability:: Linux >= 3.17.

   .. versionadded:: 3.6

.. function:: urandom(size, /)

   Trả về một chuỗi byte gồm *size* byte ngẫu nhiên phù hợp để sử dụng cho mục đích mật mã.

   Hàm này trả về các byte ngẫu nhiên từ một nguồn ngẫu nhiên cụ thể cho hệ điều hành. Dữ liệu được trả về phải đủ khó đoán cho các ứng dụng mật mã, mặc dù chất lượng chính xác phụ thuộc vào cách triển khai của hệ điều hành.

   Trên Linux, nếu có ``getrandom()`` syscall, syscall này sẽ được sử dụng ở chế độ blocking: chờ cho đến khi pool entropy urandom của hệ thống được khởi tạo (kernel đã thu thập 128 bit entropy). Xem :pep:`524` để biết lý do. Trên Linux, có thể sử dụng hàm :func:`getrandom` để lấy các byte ngẫu nhiên ở chế độ non-blocking (bằng cờ :data:`GRND_NONBLOCK`) hoặc thăm dò cho đến khi pool entropy urandom của hệ thống được khởi tạo.

   Trên hệ thống tương tự Unix, các byte ngẫu nhiên được đọc từ thiết bị ``/dev/urandom``. Nếu thiết bị ``/dev/urandom`` không khả dụng hoặc không thể đọc,
   sẽ phát sinh ngoại lệ :exc:`NotImplementedError`.

   Trên Windows, hàm này sẽ sử dụng ``BCryptGenRandom()``.

   .. seealso::
      Module :mod:`secrets` cung cấp các hàm cấp cao hơn. Để sử dụng giao diện dễ dùng cho bộ tạo số ngẫu nhiên do nền tảng của bạn cung cấp, hãy xem :class:`random.SystemRandom`.

   .. versionchanged:: 3.5
      Trên Linux 3.17 trở lên, syscall ``getrandom()`` hiện được sử dụng khi có sẵn. Trên OpenBSD 5.6 trở lên, hàm C ``getentropy()`` hiện được sử dụng. Các hàm này tránh việc sử dụng một file descriptor nội bộ.

   .. versionchanged:: 3.5.2
      Trên Linux, nếu syscall ``getrandom()`` bị chặn (pool entropy của urandom chưa được khởi tạo), sẽ chuyển sang đọc ``/dev/urandom``.

   .. versionchanged:: 3.6
      Trên Linux, ``getrandom()`` hiện được sử dụng ở chế độ blocking để tăng tính bảo mật.

   .. versionchanged:: 3.11
      Trên Windows, ``BCryptGenRandom()`` được sử dụng thay cho ``CryptGenRandom()``, vốn đã deprecated.

.. data:: GRND_NONBLOCK

   Theo mặc định, khi đọc từ ``/dev/random``, :func:`getrandom` sẽ chặn nếu không có byte ngẫu nhiên nào khả dụng; khi đọc từ ``/dev/urandom``, nó sẽ chặn nếu pool entropy chưa được khởi tạo.

   Nếu cờ :py:data:`GRND_NONBLOCK` được thiết lập, :func:`getrandom` sẽ không chặn trong những trường hợp này mà thay vào đó ngay lập tức raise :exc:`BlockingIOError`.

   .. versionadded:: 3.6

.. data:: GRND_RANDOM

   Nếu bit này được thiết lập, các byte ngẫu nhiên sẽ được lấy từ pool ``/dev/random`` thay vì pool ``/dev/urandom``.

   .. versionadded:: 3.6

.. _`the MSDN`: https://msdn.microsoft.com/en-us/library/z0kc8e3z.aspx
.. _`opendir()`: https://pubs.opengroup.org/onlinepubs/009695399/functions/opendir.html
.. _`readdir()`: https://pubs.opengroup.org/onlinepubs/009695399/functions/readdir_r.html
.. _`FindFirstFileW`: https://msdn.microsoft.com/en-us/library/windows/desktop/aa364418(v=vs.85).aspx
.. _`FindNextFileW`: https://msdn.microsoft.com/en-us/library/windows/desktop/aa364428(v=vs.85).aspx
.. _`file index`: https://msdn.microsoft.com/en-us/library/aa363788
.. _`Microsoft documentation`: https://msdn.microsoft.com/44228cf2-6306-466c-8f16-f513cd3ba8b5
.. _`this discussion on fork being incompatible with threads`: https://discuss.python.org/t/33555
.. _`times(3)`: https://man.freebsd.org/cgi/man.cgi?time(3)
.. _`the GetProcessTimes MSDN`: https://docs.microsoft.com/windows/win32/api/processthreadsapi/nf-processthreadsapi-getprocesstimes
.. _`Linux getrandom() manual page`: https://man7.org/linux/man-pages/man2/getrandom.2.html
