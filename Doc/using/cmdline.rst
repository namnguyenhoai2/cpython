.. highlight:: sh

.. ATTENTION: You probably should update Misc/python.man, too, if you modify
   this file.

.. _using-on-general:

Dòng lệnh và môi trường
=======================

Trình thông dịch CPython quét dòng lệnh và môi trường để tìm nhiều thiết lập khác nhau.

.. impl-detail::

   Other implementations' command line schemes may differ.  See
   :ref:`implementations` for further resources.


.. _using-on-cmdline:

Dòng lệnh
---------

Khi gọi Python, bạn có thể chỉ định bất kỳ tùy chọn nào sau đây::

    python [-bBdEhiIOPqRsSuvVWx?] [-c command | -m module-name | script | - ] [args]

Trường hợp sử dụng phổ biến nhất dĩ nhiên là gọi một script đơn giản::

    python myscript.py


.. _using-on-interface-options:

Các tùy chọn giao diện
~~~~~~~~~~~~~~~~~~~~~~

Giao diện của trình thông dịch tương tự giao diện của UNIX shell, nhưng cung cấp thêm một số phương thức gọi:

* Khi được gọi với đầu vào tiêu chuẩn được kết nối với thiết bị tty, chương trình sẽ nhắc nhập lệnh và thực thi chúng cho đến khi đọc được EOF (ký tự kết thúc tệp; bạn có thể tạo ký tự này bằng :kbd:`Ctrl-D` trên UNIX hoặc :kbd:`Ctrl-Z, Enter` trên Windows). Để biết thêm về chế độ tương tác, hãy xem :ref:`tut-interac`.
* Khi được gọi với đối số là tên tệp hoặc với một tệp làm đầu vào tiêu chuẩn, chương trình sẽ đọc và thực thi script từ tệp đó.
* Khi được gọi với đối số là tên thư mục, chương trình sẽ đọc và thực thi một script có tên phù hợp từ thư mục đó.
* Khi được gọi với ``-c command``, chương trình sẽ thực thi các câu lệnh Python được cung cấp dưới dạng *command*. Ở đây, *command* có thể chứa nhiều câu lệnh được phân tách bằng ký tự xuống dòng. Khoảng trắng ở đầu câu lệnh Python có ý nghĩa quan trọng!
* Khi được gọi với ``-m module-name``, module được cung cấp sẽ được định vị bằng cơ chế import tiêu chuẩn và được thực thi như một script.

Trong chế độ không tương tác, toàn bộ đầu vào sẽ được phân tích cú pháp trước khi thực thi.

Một tùy chọn giao diện sẽ kết thúc danh sách các tùy chọn được interpreter tiếp nhận; tất cả các đối số liên tiếp sẽ được đưa vào :data:`sys.argv` -- lưu ý rằng phần tử đầu tiên, chỉ mục không (``sys.argv[0]``), là một chuỗi phản ánh mã nguồn của chương trình.

.. option:: -c <command>

   Thực thi mã Python trong *command*. *command* có thể là một hoặc nhiều câu lệnh được phân tách bằng dòng mới, với khoảng trắng đầu dòng có ý nghĩa như trong mã module thông thường.

   Nếu cung cấp tùy chọn này, phần tử đầu tiên của :data:`sys.argv` sẽ là ``"-c"`` và thư mục hiện tại sẽ được thêm vào đầu
   :data:`sys.path` (cho phép import các module trong thư mục đó dưới dạng các top-level module).

   .. audit-event:: cpython.run_command command cmdoption-c

   .. versionchanged:: 3.14
      *command* sẽ được tự động loại bỏ thụt lề trước khi thực thi.

.. option:: -m <module-name>

   Định vị module bằng cơ chế import tiêu chuẩn và thực thi nội dung của module đó dưới dạng module :mod:`__main__`.

   Vì đối số là tên *module*, bạn không được cung cấp phần mở rộng tệp (``.py``). Tên module phải là một tên module Python tuyệt đối hợp lệ, nhưng implementation có thể không phải lúc nào cũng thực thi yêu cầu này (ví dụ: có thể cho phép bạn sử dụng tên chứa dấu gạch ngang).

   Tên package (bao gồm cả namespace package) cũng được phép. Khi cung cấp tên package thay vì một module thông thường, interpreter sẽ thực thi ``<pkg>.__main__`` dưới dạng module chính. Hành vi này cố ý tương tự như cách xử lý các thư mục và zipfile được truyền cho interpreter dưới dạng đối số script.

   .. note::

      Không thể sử dụng tùy chọn này với các module tích hợp sẵn và các module mở rộng được viết bằng C, vì chúng không có tệp module Python. Tuy nhiên, tùy chọn này vẫn có thể được sử dụng cho các module đã biên dịch trước, ngay cả khi không có tệp mã nguồn ban đầu.

   Nếu cung cấp tùy chọn này, phần tử đầu tiên của :data:`sys.argv` sẽ là đường dẫn đầy đủ đến tệp module (trong khi tệp module đang được định vị, phần tử đầu tiên sẽ được đặt thành ``"-m"``). Giống như tùy chọn :option:`-c`, thư mục hiện tại sẽ được thêm vào đầu :data:`sys.path`.

   Có thể sử dụng tùy chọn :option:`-I` để chạy script ở chế độ cô lập, trong đó
   :data:`sys.path` không chứa thư mục hiện tại cũng như thư mục site-packages của người dùng. Tất cả biến môi trường ``PYTHON*`` cũng bị bỏ qua.

   Nhiều module trong thư viện chuẩn chứa mã được gọi khi chúng được thực thi dưới dạng script. Một ví dụ là module :mod:`timeit`::

       python -m timeit -s "setup here" "benchmarked code here"
       python -m timeit -h # để biết chi tiết

   .. audit-event:: cpython.run_module module-name cmdoption-m

   .. seealso::
      :func:`runpy.run_module`
         Equivalent functionality directly available to Python code

      :pep:`338` -- Thực thi các module dưới dạng script

   .. versionchanged:: 3.1
      Cung cấp tên gói để chạy một submodule ``__main__``.

   .. versionchanged:: 3.4
      Các namespace package cũng được hỗ trợ

.. _cmdarg-dash:

.. describe:: -

   Read commands from standard input (:data:`sys.stdin`).  If standard input is
   a terminal, :option:`-i` is implied.

   If this option is given, the first element of :data:`sys.argv` will be
   ``"-"`` and the current directory will be added to the start of
   :data:`sys.path`.

   .. audit-event:: cpython.run_stdin "" ""

.. _cmdarg-script:

.. describe:: <script>

   Execute the Python code contained in *script*, which must be a filesystem
   path (absolute or relative) referring to either a Python file, a directory
   containing a ``__main__.py`` file, or a zipfile containing a
   ``__main__.py`` file.

   If this option is given, the first element of :data:`sys.argv` will be the
   script name as given on the command line.

   If the script name refers directly to a Python file, the directory
   containing that file is added to the start of :data:`sys.path`, and the
   file is executed as the :mod:`__main__` module.

   If the script name refers to a directory or zipfile, the script name is
   added to the start of :data:`sys.path` and the ``__main__.py`` file in
   that location is executed as the :mod:`__main__` module.

   :option:`-I` option can  be used to run the script in isolated mode where
   :data:`sys.path` contains neither the script's directory nor the user's
   site-packages directory. All ``PYTHON*`` environment variables are
   ignored, too.

   .. audit-event:: cpython.run_file filename

   .. seealso::
      :func:`runpy.run_path`
         Equivalent functionality directly available to Python code


Nếu không cung cấp tùy chọn giao diện, :option:`-i` được ngầm định, ``sys.argv[0]`` là một chuỗi rỗng (``""``) và thư mục hiện tại sẽ được thêm vào đầu :data:`sys.path`. Ngoài ra, tính năng tự động hoàn tất bằng phím Tab và chỉnh sửa lịch sử sẽ được bật tự động nếu nền tảng của bạn hỗ trợ (xem
:ref:`rlcompleter-config`).

.. seealso::  :ref:`tut-invoking`

.. versionchanged:: 3.4
   Tự động bật tính năng hoàn tất bằng phím Tab và chỉnh sửa lịch sử.


.. _using-on-generic-options:

Tùy chọn chung
~~~~~~~~~~~~~~

.. option:: -?
            -h --help

   In mô tả ngắn về tất cả tùy chọn dòng lệnh và các biến môi trường tương ứng rồi thoát.

.. option:: --help-env

   In mô tả ngắn về các biến môi trường dành riêng cho Python rồi thoát.

   .. versionadded:: 3.11

.. option:: --help-xoptions

   In mô tả về các tùy chọn dành riêng cho từng bản triển khai :option:`-X` rồi thoát.

   .. versionadded:: 3.11

.. option:: --help-all

   In thông tin sử dụng đầy đủ rồi thoát.

   .. versionadded:: 3.11

.. option:: -V
            --version

   In số phiên bản Python rồi thoát. Đầu ra mẫu có thể là:

   .. code-block:: none

       Python 3.8.0b2+

   Khi được chỉ định hai lần, in thêm thông tin về bản build, chẳng hạn như:

   .. code-block:: none

       Python 3.8.0b2+ (3.8:0c076caaa8, Apr 20 2019, 21:55:00)
       [GCC 6.2.0 20161005]

   .. versionadded:: 3.6
      Tùy chọn ``-VV``.


.. _using-on-misc-options:

Tùy chọn khác
~~~~~~~~~~~~~

.. option:: -b

   Phát cảnh báo khi chuyển đổi :class:`bytes` hoặc :class:`bytearray` thành
   :class:`str` mà không chỉ định encoding hoặc so sánh :class:`!bytes` hoặc
   :class:`!bytearray` với :class:`!str` hoặc :class:`!bytes` với :class:`int`. Phát lỗi khi tùy chọn được cung cấp hai lần (:option:`!-bb`).

   .. versionchanged:: 3.5
      Cũng ảnh hưởng đến việc so sánh :class:`bytes` với :class:`int`.

.. option:: -B

   Nếu được cung cấp, Python sẽ không cố ghi các tệp ``.pyc`` khi nhập các mô-đun nguồn. Xem thêm :envvar:`PYTHONDONTWRITEBYTECODE`.


.. option:: --check-hash-based-pycs default|always|never

   Kiểm soát hành vi xác thực của các tệp ``.pyc`` dựa trên hash. Xem
   :ref:`pyc-invalidation`. Khi được đặt thành ``default``, các tệp bộ nhớ đệm bytecode dựa trên hash đã kiểm tra và chưa kiểm tra được xác thực theo ngữ nghĩa mặc định của chúng. Khi được đặt thành ``always``, tất cả các tệp ``.pyc`` dựa trên hash, dù đã kiểm tra hay chưa kiểm tra, đều được xác thực dựa trên tệp nguồn tương ứng. Khi được đặt thành ``never``, các tệp ``.pyc`` dựa trên hash không được xác thực dựa trên các tệp nguồn tương ứng của chúng.

   Ngữ nghĩa của các tệp ``.pyc`` dựa trên dấu thời gian không bị ảnh hưởng bởi tùy chọn này.


.. option:: -d

   Bật đầu ra gỡ lỗi của parser (chỉ dành cho chuyên gia). Xem thêm biến môi trường :envvar:`PYTHONDEBUG`.

   Tùy chọn này yêu cầu bản :ref:`debug build của Python <debug-build>`, nếu không, tùy chọn này sẽ bị bỏ qua.


.. option:: -E

   Bỏ qua tất cả các biến môi trường ``PYTHON*``, chẳng hạn như
   :envvar:`PYTHONPATH` và :envvar:`PYTHONHOME`, có thể đã được đặt.

   Xem thêm các tùy chọn :option:`-P` và :option:`-I` (isolated).


.. option:: -i

   Chuyển sang chế độ tương tác sau khi thực thi.

   Sử dụng tùy chọn :option:`-i` sẽ chuyển sang chế độ tương tác trong bất kỳ trường hợp nào sau đây\:

   * Khi một script được truyền dưới dạng đối số đầu tiên
   * Khi sử dụng tùy chọn :option:`-c`
   * Khi sử dụng tùy chọn :option:`-m`

   Chế độ tương tác sẽ khởi động ngay cả khi :data:`sys.stdin` có vẻ không phải là một terminal. Tệp
   :envvar:`PYTHONSTARTUP` không được đọc.

   Điều này có thể hữu ích để kiểm tra các biến toàn cục hoặc stack trace khi một script phát sinh ngoại lệ. Xem thêm :envvar:`PYTHONINSPECT`.


.. option:: -I

   Chạy Python ở chế độ cô lập. Điều này cũng ngầm áp dụng các tùy chọn :option:`-E`, :option:`-P` và :option:`-s`.

   Ở chế độ cô lập, :data:`sys.path` không chứa thư mục của script cũng như thư mục site-packages của người dùng. Tất cả các biến môi trường ``PYTHON*`` cũng bị bỏ qua. Có thể áp dụng thêm các hạn chế để ngăn người dùng chèn mã độc hại.

   .. versionadded:: 3.4


.. option:: -O

   Xóa các câu lệnh assert và mọi mã phụ thuộc có điều kiện vào giá trị của
   :const:`__debug__`. Bổ sung tên tệp cho các tệp đã biên dịch (:term:`bytecode`) bằng cách thêm ``.opt-1`` trước phần mở rộng ``.pyc`` (xem :pep:`488`). Xem thêm :envvar:`PYTHONOPTIMIZE`.

   .. versionchanged:: 3.5
      Sửa đổi tên tệp ``.pyc`` theo :pep:`488`.


.. option:: -OO

   Thực hiện :option:`-O` và đồng thời loại bỏ docstring. Bổ sung tên tệp cho các tệp đã biên dịch (:term:`bytecode`) bằng cách thêm ``.opt-2`` trước phần mở rộng ``.pyc`` (xem :pep:`488`).

   .. versionchanged:: 3.5
      Sửa đổi tên tệp ``.pyc`` theo :pep:`488`.


.. option:: -P

   Không thêm một đường dẫn có thể không an toàn vào trước :data:`sys.path`:

   * Dòng lệnh ``python -m module``: Không thêm thư mục làm việc hiện tại vào trước.
   * Dòng lệnh ``python script.py``: Không thêm thư mục của script vào trước. Nếu đó là một liên kết tượng trưng, hãy phân giải các liên kết tượng trưng.
   * Dòng lệnh ``python -c code`` và ``python`` (REPL): Không thêm một chuỗi rỗng vào trước; chuỗi này có nghĩa là thư mục làm việc hiện tại.

   Xem thêm biến môi trường :envvar:`PYTHONSAFEPATH`, cùng các tùy chọn :option:`-E` và :option:`-I` (cô lập).

   .. versionadded:: 3.11


.. option:: -q

   Không hiển thị thông báo bản quyền và phiên bản, kể cả trong chế độ tương tác.

   .. versionadded:: 3.2


.. option:: -R

   Bật tính năng ngẫu nhiên hóa hash. Tùy chọn này chỉ có hiệu lực nếu biến môi trường
   :envvar:`PYTHONHASHSEED` được đặt thành bất kỳ giá trị nào khác ``random``, vì tính năng ngẫu nhiên hóa hash được bật theo mặc định.

   Trong các phiên bản Python trước đây, tùy chọn này bật tính năng ngẫu nhiên hóa hash, nhờ đó các giá trị :meth:`~object.__hash__` của đối tượng str và bytes được "salt" bằng một giá trị ngẫu nhiên không thể đoán trước. Mặc dù chúng không đổi trong một tiến trình Python riêng lẻ, nhưng không thể dự đoán được giữa các lần gọi Python lặp lại.

   Tính năng ngẫu nhiên hóa hash nhằm bảo vệ chống lại cuộc tấn công từ chối dịch vụ do các đầu vào được lựa chọn cẩn thận gây ra, khai thác hiệu năng trong trường hợp xấu nhất của việc xây dựng dict với độ phức tạp *O*\ (*n*\ :sup:`2`). Xem https://ocert.org/advisories/ocert-2011-003.html để biết chi tiết.

   :envvar:`PYTHONHASHSEED` cho phép bạn đặt một giá trị cố định cho secret của hash seed.

   .. versionadded:: 3.2.3

   .. versionchanged:: 3.7
      Tùy chọn này không còn bị bỏ qua.


.. option:: -s

   Không thêm :data:`user site-packages directory <site.USER_SITE>` vào
   :data:`sys.path`.

   Xem thêm :envvar:`PYTHONNOUSERSITE`.

   .. seealso::

      :pep:`370` -- Thư mục site-packages theo người dùng


.. option:: -S

   Vô hiệu hóa việc import module :mod:`site` và các thao tác phụ thuộc vào site đối với :data:`sys.path` mà module này thực hiện. Đồng thời vô hiệu hóa các thao tác này nếu :mod:`site` được import một cách tường minh về sau (gọi
   :func:`site.main` nếu bạn muốn kích hoạt chúng).


.. option:: -u

   Buộc các stream stdout và stderr ở chế độ không đệm. Tùy chọn này không ảnh hưởng đến stream stdin.

   Xem thêm :envvar:`PYTHONUNBUFFERED`.

   .. versionchanged:: 3.7
      Lớp văn bản của các stream stdout và stderr hiện ở chế độ không đệm.


.. option:: -v

   In một thông báo mỗi khi một module được khởi tạo, hiển thị vị trí (tên tệp hoặc module tích hợp sẵn) nơi module đó được tải. Khi được cung cấp hai lần (:option:`!-vv`), in một thông báo cho mỗi tệp được kiểm tra khi tìm kiếm một module. Cũng cung cấp thông tin về việc dọn dẹp module khi thoát.

   .. versionchanged:: 3.10
      Module :mod:`site` báo cáo các đường dẫn dành riêng cho từng site và các tệp :file:`.pth` đang được xử lý.

   Xem thêm :envvar:`PYTHONVERBOSE`.


.. _using-on-warnings:
.. option:: -W arg

   Kiểm soát cảnh báo. Theo mặc định, cơ chế cảnh báo của Python in các thông báo cảnh báo vào :data:`sys.stderr`.

   Các thiết lập đơn giản nhất áp dụng một hành động cụ thể một cách vô điều kiện cho tất cả cảnh báo do một process phát ra (kể cả những cảnh báo vốn bị bỏ qua theo mặc định)::

       -Wdefault  # Cảnh báo một lần cho mỗi vị trí gọi
       -Werror    # Chuyển thành ngoại lệ
       -Walways   # Cảnh báo mỗi lần
       -Wall      # Giống như -Walways
       -Wmodule   # Cảnh báo một lần cho mỗi mô-đun gọi
       -Wonce     # Cảnh báo một lần cho mỗi tiến trình Python
       -Wignore   # Không bao giờ cảnh báo

   Tên hành động có thể được viết tắt tùy ý và trình thông dịch sẽ phân giải chúng thành tên hành động thích hợp. Ví dụ: ``-Wi`` tương đương với ``-Wignore``.

   Dạng đầy đủ của đối số là::

       action:message:category:module:lineno

   Các trường trống khớp với mọi giá trị; có thể bỏ qua các trường trống ở cuối. Ví dụ: ``-W ignore::DeprecationWarning`` bỏ qua tất cả các cảnh báo DeprecationWarning.

   Trường *action* được giải thích như trên nhưng chỉ áp dụng cho các cảnh báo khớp với những trường còn lại.

   Trường *message* phải khớp với toàn bộ thông báo cảnh báo; việc khớp này không phân biệt chữ hoa chữ thường.

   Trường *category* khớp với danh mục cảnh báo (ví dụ: ``DeprecationWarning``). Đây phải là tên lớp; phép kiểm tra khớp xác định xem danh mục cảnh báo thực tế của thông báo có phải là lớp con của danh mục cảnh báo được chỉ định hay không.

   Trường *module* khớp với tên module (đủ điều kiện); việc khớp này phân biệt chữ hoa chữ thường.

   Trường *lineno* khớp với số dòng, trong đó số 0 khớp với mọi số dòng và do đó tương đương với việc bỏ qua số dòng.

   Có thể cung cấp nhiều tùy chọn :option:`-W`; khi một cảnh báo khớp với nhiều tùy chọn, hành động của tùy chọn khớp cuối cùng sẽ được thực hiện. Không hợp lệ
   Các tùy chọn :option:`-W` bị bỏ qua (mặc dù một thông báo cảnh báo về các tùy chọn không hợp lệ sẽ được in khi cảnh báo đầu tiên được đưa ra).

   Cảnh báo cũng có thể được kiểm soát bằng biến môi trường :envvar:`PYTHONWARNINGS` và từ bên trong một chương trình Python bằng cách sử dụng
   mô-đun :mod:`warnings`. Ví dụ, có thể sử dụng hàm :func:`warnings.filterwarnings` để áp dụng biểu thức chính quy cho thông báo cảnh báo.

   Xem :ref:`warning-filter` và :ref:`describing-warning-filters` để biết thêm chi tiết.


.. option:: -x

   Bỏ qua dòng đầu tiên của mã nguồn, cho phép sử dụng các dạng ``#!cmd`` không phải Unix.

   Có thể dùng cách này để biến một tập lệnh Python thành tệp batch của Windows. Tương tự như việc thêm dòng shebang và đặt bit thực thi trên Unix, có thể đổi phần mở rộng của tập lệnh Python thành ``.bat`` và thêm dòng sau vào đầu tập lệnh:

   .. code-block:: batch

      @py -x "%~f0" %* & exit /b

   Hoặc, để chỉ định rõ đường dẫn đến trình thông dịch Python:

   .. code-block:: batch

      @"C:\Path\to\python.exe" -x "%~f0" %* & exit /b

   Không giống như dòng shebang vốn là một chú thích Python, dòng này không phải cú pháp Python hợp lệ và cần có tùy chọn :option:`-x` để bỏ qua dòng đó.


.. option:: -X

   Dành riêng cho các tùy chọn phụ thuộc vào từng triển khai. Hiện tại, CPython định nghĩa các giá trị có thể có sau đây:

   * ``-X faulthandler`` để bật :mod:`faulthandler`. Xem thêm :envvar:`PYTHONFAULTHANDLER`.

     .. versionadded:: 3.3

   * ``-X showrefcount`` để xuất tổng số lượng tham chiếu và số khối bộ nhớ đang được sử dụng khi chương trình kết thúc hoặc sau mỗi câu lệnh trong trình thông dịch tương tác. Tùy chọn này chỉ hoạt động trên các bản dựng :ref:`debug builds <debug-build>`.

     .. versionadded:: 3.4

   * ``-X tracemalloc`` để bắt đầu theo dõi các phân bổ bộ nhớ Python bằng mô-đun
     :mod:`tracemalloc`. Theo mặc định, chỉ frame gần đây nhất được lưu trong traceback của một trace. Dùng ``-X tracemalloc=NFRAME`` để bắt đầu theo dõi với giới hạn traceback là *NFRAME* frame. Xem :func:`tracemalloc.start` và :envvar:`PYTHONTRACEMALLOC` để biết thêm thông tin.

     .. versionadded:: 3.4

   * ``-X int_max_str_digits`` cấu hình :ref:`integer string conversion length limitation <int_max_str_digits>`. Xem thêm
     :envvar:`PYTHONINTMAXSTRDIGITS`.

     .. versionadded:: 3.11

   * ``-X importtime`` để hiển thị thời gian nhập của từng module. Lệnh này hiển thị tên module, thời gian tích lũy (bao gồm cả các lần nhập lồng nhau) và thời gian riêng (không bao gồm các lần nhập lồng nhau). Lưu ý rằng đầu ra của lệnh có thể bị sai lệch trong ứng dụng đa luồng. Cách sử dụng điển hình là ``python -X importtime -c 'import asyncio'``.

     ``-X importtime=2`` bật đầu ra bổ sung cho biết khi một module được nhập đã được tải trước đó. Trong những trường hợp như vậy, chuỗi ``cached`` sẽ được in ở cả hai cột thời gian.

     Xem thêm :envvar:`PYTHONPROFILEIMPORTTIME`.

     .. versionadded:: 3.7

     .. versionchanged:: 3.14

         Đã bổ sung ``-X importtime=2`` để cũng theo dõi việc nhập các module đã tải, đồng thời dành các giá trị khác ngoài ``1`` và ``2`` cho mục đích sử dụng trong tương lai.

   * ``-X dev``: bật :ref:`Python Development Mode <devmode>`, bổ sung các kiểm tra runtime có chi phí quá cao nên không được bật theo mặc định. Xem thêm :envvar:`PYTHONDEVMODE`.

     .. versionadded:: 3.7

   * ``-X utf8`` bật :ref:`Python UTF-8 Mode <utf8-mode>`. ``-X utf8=0`` tắt rõ ràng :ref:`Python UTF-8 Mode <utf8-mode>` (ngay cả khi chế độ này lẽ ra sẽ tự động được kích hoạt). Xem thêm :envvar:`PYTHONUTF8`.

     .. versionadded:: 3.7

   * ``-X pycache_prefix=PATH`` cho phép ghi các tệp ``.pyc`` vào một cây thư mục song song có thư mục gốc là thư mục đã cho, thay vì ghi vào cây mã. Xem thêm
     :envvar:`PYTHONPYCACHEPREFIX`.

     .. versionadded:: 3.8

   * ``-X warn_default_encoding`` phát ra :class:`EncodingWarning` khi sử dụng encoding mặc định dành riêng cho locale để mở tệp. Xem thêm :envvar:`PYTHONWARNDEFAULTENCODING`.

     .. versionadded:: 3.10

   * ``-X no_debug_ranges`` vô hiệu hóa việc đưa vào các bảng ánh xạ thông tin vị trí bổ sung (dòng kết thúc, offset cột bắt đầu và offset cột kết thúc) cho mọi instruction trong các code object. Điều này hữu ích khi cần các code object và tệp pyc nhỏ hơn, đồng thời loại bỏ các chỉ báo vị trí trực quan bổ sung khi interpreter hiển thị traceback. Xem thêm
     :envvar:`PYTHONNODEBUGRANGES`.

     .. versionadded:: 3.11

   * ``-X frozen_modules`` xác định liệu các frozen module có bị import machinery bỏ qua hay không. Giá trị ``on`` nghĩa là chúng được import, còn ``off`` nghĩa là chúng bị bỏ qua. Giá trị mặc định là ``on`` nếu đây là Python đã được cài đặt (trường hợp thông thường). Nếu đang trong quá trình phát triển (chạy từ source tree) thì giá trị mặc định là ``off``. Lưu ý rằng :mod:`!importlib_bootstrap` và
     :mod:`!importlib_bootstrap_external` luôn được sử dụng, ngay cả khi flag này được đặt thành ``off``. Xem thêm :envvar:`PYTHON_FROZEN_MODULES`.

     .. versionadded:: 3.11

   * ``-X perf`` bật hỗ trợ cho profiler ``perf`` của Linux. Khi cung cấp tùy chọn này, profiler ``perf`` sẽ có thể báo cáo các lệnh gọi Python. Tùy chọn này chỉ khả dụng trên một số nền tảng và sẽ không thực hiện gì nếu hệ thống hiện tại không hỗ trợ. Giá trị mặc định là "off". Xem thêm :envvar:`PYTHONPERFSUPPORT` và :ref:`perf_profiling`.

     .. versionadded:: 3.12

   * ``-X perf_jit`` bật hỗ trợ cho profiler ``perf`` của Linux với hỗ trợ DWARF. Khi cung cấp tùy chọn này, profiler ``perf`` sẽ có thể báo cáo các lệnh gọi Python bằng thông tin DWARF. Tùy chọn này chỉ khả dụng trên một số nền tảng và sẽ không thực hiện gì nếu hệ thống hiện tại không hỗ trợ. Giá trị mặc định là "off". Xem thêm :envvar:`PYTHON_PERF_JIT_SUPPORT` và :ref:`perf_profiling`.

     .. versionadded:: 3.13

   * ``-X disable_remote_debug`` vô hiệu hóa hỗ trợ remote debugging như được mô tả trong :pep:`768`. Hỗ trợ này bao gồm cả chức năng lập lịch code để thực thi trong một process khác và chức năng nhận code để thực thi trong process hiện tại.

     Tùy chọn này chỉ khả dụng trên một số nền tảng và sẽ không có tác dụng nếu hệ thống hiện tại không hỗ trợ. Xem thêm
     :envvar:`PYTHON_DISABLE_REMOTE_DEBUG` và :pep:`768`.

     .. versionadded:: 3.14

   * :samp:`-X cpu_count={n}` ghi đè :func:`os.cpu_count`,
     :func:`os.process_cpu_count`, và :func:`multiprocessing.cpu_count`. *n* phải lớn hơn hoặc bằng 1. Tùy chọn này có thể hữu ích cho người dùng cần giới hạn tài nguyên CPU của hệ thống container. Xem thêm :envvar:`PYTHON_CPU_COUNT`. Nếu *n* là ``default``, thì không có gì bị ghi đè.

     .. versionadded:: 3.13

   * :samp:`-X presite={package.module}` chỉ định một module cần được import trước khi module :mod:`site` được thực thi và trước khi
     module :mod:`__main__` tồn tại. Do đó, module được import không
     :mod:`__main__`. Tùy chọn này có thể được dùng để thực thi mã sớm trong quá trình khởi tạo Python. Python cần được :ref:`biên dịch ở chế độ debug <debug-build>` để tùy chọn này tồn tại. Xem thêm :envvar:`PYTHON_PRESITE`.

     .. versionadded:: 3.13

   * :samp:`-X gil={0,1}` buộc GIL lần lượt bị vô hiệu hóa hoặc được bật. Việc đặt thành ``0`` chỉ khả dụng trong các bản build được cấu hình với
     :option:`--disable-gil`. Xem thêm :envvar:`PYTHON_GIL` và
     :ref:`whatsnew313-free-threaded-cpython`.

     .. versionadded:: 3.13

   * :samp:`-X thread_inherit_context={0,1}` khiến :class:`~threading.Thread` theo mặc định sử dụng một bản sao context của caller của ``Thread.start()`` khi khởi động. Nếu không được đặt, các thread sẽ khởi động với context trống. Nếu không được đặt, giá trị của tùy chọn này mặc định là ``1`` trên các bản build free-threaded và ``0`` trong các trường hợp khác. Xem thêm
     :envvar:`PYTHON_THREAD_INHERIT_CONTEXT`.

     .. versionadded:: 3.14

   * :samp:`-X context_aware_warnings={0,1}` khiến
     :class:`warnings.catch_warnings` trình quản lý ngữ cảnh sử dụng một
     :class:`~contextvars.ContextVar` để lưu trữ trạng thái bộ lọc cảnh báo. Nếu không được đặt, giá trị của tùy chọn này mặc định là ``1`` trên các bản build free-threaded và ``0`` trong các trường hợp khác. Xem thêm :envvar:`PYTHON_CONTEXT_AWARE_WARNINGS`.

     .. versionadded:: 3.14

   * :samp:`-X tlbc={0,1}` bật (1, mặc định) hoặc tắt (0) bytecode cục bộ theo thread trong các bản build được cấu hình với :option:`--disable-gil`. Khi bị tắt, tùy chọn này cũng tắt trình thông dịch specializing. Xem thêm
     :envvar:`PYTHON_TLBC`.

     .. versionadded:: 3.14

   Ngoài ra, tùy chọn này cho phép truyền các giá trị tùy ý và truy xuất chúng thông qua
   :data:`sys._xoptions` từ điển.

   .. versionadded:: 3.2

   .. versionchanged:: 3.9
      Đã xóa tùy chọn ``-X showalloccount``.

   .. versionchanged:: 3.10
      Đã xóa tùy chọn ``-X oldparser``.

.. versionremoved:: 3.14

   :option:`!-J` không còn được dành riêng để Jython_ sử dụng và hiện không có ý nghĩa đặc biệt.

   .. _Jython: https://www.jython.org/

.. _using-on-controlling-color:

Điều khiển màu sắc
~~~~~~~~~~~~~~~~~~

Trình thông dịch Python được cấu hình mặc định để sử dụng màu sắc nhằm làm nổi bật đầu ra trong một số tình huống nhất định, chẳng hạn như khi hiển thị traceback. Có thể kiểm soát hành vi này bằng cách đặt các biến môi trường khác nhau.

Đặt biến môi trường ``TERM`` thành ``dumb`` sẽ tắt màu.

Nếu biến môi trường |FORCE_COLOR|_ được đặt, màu sẽ được bật bất kể giá trị của TERM. Điều này hữu ích trên các hệ thống CI không phải là terminal nhưng vẫn có thể hiển thị các chuỗi thoát ANSI.

Nếu biến môi trường |NO_COLOR|_ được đặt, Python sẽ tắt toàn bộ màu trong đầu ra. Thiết lập này được ưu tiên hơn ``FORCE_COLOR``.

Tất cả các biến môi trường này cũng được các công cụ khác sử dụng để kiểm soát đầu ra màu. Để chỉ kiểm soát đầu ra màu trong trình thông dịch Python, có thể sử dụng
biến môi trường :envvar:`PYTHON_COLORS`. Biến này được ưu tiên hơn ``NO_COLOR``, và ``NO_COLOR`` lại được ưu tiên hơn ``FORCE_COLOR``.


.. _using-on-envvars:

Các biến môi trường
-------------------

Các biến môi trường này ảnh hưởng đến hành vi của Python và được xử lý trước các tùy chọn dòng lệnh, ngoại trừ -E hoặc -I. Theo thông lệ, các tùy chọn dòng lệnh sẽ ghi đè các biến môi trường khi có xung đột.

.. envvar:: PYTHONHOME

   Thay đổi vị trí của các thư viện Python chuẩn. Theo mặc định, các thư viện được tìm kiếm trong :file:`{prefix}/lib/python{version}` và
   :file:`{exec_prefix}/lib/python{version}`, trong đó :file:`{prefix}` và
   :file:`{exec_prefix}` là các thư mục phụ thuộc vào quá trình cài đặt, cả hai đều mặc định là :file:`/usr/local`.

   Khi :envvar:`PYTHONHOME` được đặt thành một thư mục duy nhất, giá trị của nó sẽ thay thế cả :file:`{prefix}` và :file:`{exec_prefix}`. Để chỉ định các giá trị khác nhau cho những biến này, hãy đặt :envvar:`PYTHONHOME` thành :file:`{prefix}:{exec_prefix}`.


.. envvar:: PYTHONPATH

   Bổ sung vào đường dẫn tìm kiếm mặc định cho các tệp module. Định dạng giống với :envvar:`PATH` của shell: một hoặc nhiều tên đường dẫn thư mục được phân tách bằng
   :data:`os.pathsep` (ví dụ: dấu hai chấm trên Unix hoặc dấu chấm phẩy trên Windows). Các thư mục không tồn tại sẽ bị bỏ qua một cách âm thầm.

   Ngoài các thư mục thông thường, từng mục :envvar:`PYTHONPATH` có thể trỏ đến các tệp zip chứa các module Python thuần (ở dạng mã nguồn hoặc mã đã biên dịch). Không thể import các module mở rộng từ tệp zip.

   Đường dẫn tìm kiếm mặc định phụ thuộc vào bản cài đặt, nhưng nhìn chung bắt đầu bằng
   :file:`{prefix}/lib/python{version}` (xem :envvar:`PYTHONHOME` ở trên). Nó *luôn* được nối thêm vào :envvar:`PYTHONPATH`.

   Một thư mục bổ sung sẽ được chèn vào đường dẫn tìm kiếm, phía trước
   :envvar:`PYTHONPATH` như mô tả ở trên trong mục
   :ref:`using-on-interface-options`. Có thể thao tác với đường dẫn tìm kiếm từ bên trong chương trình Python thông qua biến :data:`sys.path`.


.. envvar:: PYTHONSAFEPATH

   Nếu được đặt thành một chuỗi không rỗng, tùy chọn này sẽ không thêm một đường dẫn có khả năng không an toàn vào trước :data:`sys.path`: xem tùy chọn :option:`-P` để biết chi tiết.

   .. versionadded:: 3.11


.. envvar:: PYTHONPLATLIBDIR

   Nếu được đặt thành một chuỗi không rỗng, tùy chọn này sẽ ghi đè giá trị :data:`sys.platlibdir`.

   .. versionadded:: 3.9


.. envvar:: PYTHONSTARTUP

   Nếu đây là tên của một tệp có thể đọc được, các lệnh Python trong tệp đó sẽ được thực thi trước khi dấu nhắc đầu tiên hiển thị ở chế độ tương tác. Tệp được thực thi trong cùng một không gian tên nơi các lệnh tương tác được thực thi, để các đối tượng được định nghĩa hoặc nhập trong tệp có thể được sử dụng mà không cần chỉ định đầy đủ trong phiên tương tác. Bạn cũng có thể thay đổi các dấu nhắc :data:`sys.ps1` và
   :data:`sys.ps2` và hook :data:`sys.__interactivehook__` trong tệp này.

   .. audit-event:: cpython.run_startup filename envvar-PYTHONSTARTUP

      Raises an :ref:`auditing event <auditing>` ``cpython.run_startup`` with
      the filename as the argument when called on startup.


.. envvar:: PYTHONOPTIMIZE

   Nếu được đặt thành một chuỗi không rỗng, giá trị này tương đương với việc chỉ định tùy chọn
   :option:`-O`. Nếu được đặt thành một số nguyên, giá trị này tương đương với việc chỉ định
   :option:`-O` nhiều lần.


.. envvar:: PYTHONBREAKPOINT

   Nếu được đặt, giá trị này chỉ định một hàm có thể gọi bằng ký hiệu đường dẫn phân tách bằng dấu chấm. Mô-đun chứa hàm có thể gọi sẽ được nhập, sau đó hàm này sẽ được chạy bởi implementation mặc định của :func:`sys.breakpointhook`, vốn được gọi bởi :func:`breakpoint` tích hợp sẵn. Nếu không được đặt hoặc được đặt thành chuỗi rỗng, giá trị này tương đương với "pdb.set_trace". Đặt giá trị này thành chuỗi "0" khiến implementation mặc định của :func:`sys.breakpointhook` không làm gì ngoài việc trả về ngay lập tức.

   .. versionadded:: 3.7

.. envvar:: PYTHONDEBUG

   Nếu được đặt thành một chuỗi không rỗng, giá trị này tương đương với việc chỉ định
   :option:`-d` tùy chọn. Nếu được đặt thành một số nguyên, nó tương đương với việc chỉ định
   :option:`-d` nhiều lần.

   Biến môi trường này yêu cầu :ref:`bản build debug của Python <debug-build>`, nếu không nó sẽ bị bỏ qua.


.. envvar:: PYTHONINSPECT

   Nếu được đặt thành một chuỗi không rỗng, giá trị này tương đương với việc chỉ định
   :option:`-i` tùy chọn.

   Biến này cũng có thể được sửa đổi bằng mã Python sử dụng :data:`os.environ` để buộc bật inspect mode khi chương trình kết thúc.

   .. audit-event:: cpython.run_stdin "" ""

   .. versionchanged:: 3.12.5 (cũng có trong 3.11.10, 3.10.15, 3.9.20 và 3.8.20)
      Phát ra các sự kiện kiểm toán.

   .. versionchanged:: 3.13
      Sử dụng PyREPL nếu có thể; trong trường hợp đó, :envvar:`PYTHONSTARTUP` cũng được thực thi. Phát ra các sự kiện kiểm toán.


.. envvar:: PYTHONUNBUFFERED

   Nếu được đặt thành một chuỗi không rỗng, giá trị này tương đương với việc chỉ định
   Tùy chọn :option:`-u`.


.. envvar:: PYTHONVERBOSE

   Nếu được đặt thành một chuỗi không rỗng, giá trị này tương đương với việc chỉ định
   Tùy chọn :option:`-v`. Nếu được đặt thành một số nguyên, tùy chọn này tương đương với việc chỉ định
   :option:`-v` nhiều lần.


.. envvar:: PYTHONCASEOK

   Nếu được thiết lập, Python sẽ bỏ qua chữ hoa chữ thường trong các câu lệnh :keyword:`import`. Tùy chọn này chỉ hoạt động trên Windows và macOS.


.. envvar:: PYTHONDONTWRITEBYTECODE

   Nếu được thiết lập thành một chuỗi không rỗng, Python sẽ không cố gắng ghi các tệp ``.pyc`` khi import các mô-đun mã nguồn. Điều này tương đương với việc chỉ định tùy chọn :option:`-B`.


.. envvar:: PYTHONPYCACHEPREFIX

   Nếu được thiết lập, Python sẽ ghi các tệp ``.pyc`` vào một cây thư mục phản chiếu tại đường dẫn này, thay vì vào các thư mục ``__pycache__`` bên trong cây mã nguồn. Điều này tương đương với việc chỉ định tùy chọn :option:`-X` ``pycache_prefix=PATH``.

   .. versionadded:: 3.8


.. envvar:: PYTHONHASHSEED

   Nếu biến này không được thiết lập hoặc được thiết lập thành ``random``, một giá trị ngẫu nhiên sẽ được dùng để khởi tạo seed cho các hash của các đối tượng str và bytes.

   Nếu :envvar:`PYTHONHASHSEED` được thiết lập thành một giá trị số nguyên, giá trị đó sẽ được dùng làm seed cố định để tạo hash() cho các kiểu được cơ chế ngẫu nhiên hóa hash áp dụng.

   Mục đích của nó là cho phép tạo hash có thể lặp lại, chẳng hạn như để thực hiện selftest cho chính interpreter hoặc cho phép một cụm các tiến trình Python chia sẻ các giá trị hash.

   Số nguyên phải là một số thập phân trong phạm vi [0,4294967295]. Chỉ định giá trị 0 sẽ vô hiệu hóa cơ chế ngẫu nhiên hóa hash.

   .. versionadded:: 3.2.3

.. envvar:: PYTHONINTMAXSTRDIGITS

   Nếu biến này được đặt thành một số nguyên, biến sẽ được dùng để cấu hình :ref:`giới hạn độ dài chuyển đổi chuỗi số nguyên toàn cục <int_max_str_digits>` của trình thông dịch.

   .. versionadded:: 3.11

.. envvar:: PYTHONIOENCODING

   Nếu được đặt trước khi chạy trình thông dịch, biến này sẽ ghi đè encoding được dùng cho stdin/stdout/stderr, theo cú pháp ``encodingname:errorhandler``. Cả phần ``encodingname`` và ``:errorhandler`` đều là tùy chọn và có cùng ý nghĩa như trong :func:`str.encode`.

   Đối với stderr, phần ``:errorhandler`` sẽ bị bỏ qua; handler luôn là ``'backslashreplace'``.

   .. versionchanged:: 3.4
      Phần ``encodingname`` hiện là tùy chọn.

   .. versionchanged:: 3.6
      Trên Windows, encoding được chỉ định bởi biến này sẽ bị bỏ qua đối với các bộ đệm console tương tác, trừ khi :envvar:`PYTHONLEGACYWINDOWSSTDIO` cũng được chỉ định. Các tệp và pipe được chuyển hướng qua những stream chuẩn không bị ảnh hưởng.

.. envvar:: PYTHONNOUSERSITE

   Nếu được đặt, Python sẽ không thêm :data:`user site-packages directory <site.USER_SITE>` vào :data:`sys.path`.

   .. seealso::

      :pep:`370` -- Thư mục site-packages của từng người dùng


.. envvar:: PYTHONUSERBASE

   Xác định :data:`user base directory <site.USER_BASE>`, được dùng để tính đường dẫn của :data:`user site-packages directory <site.USER_SITE>` và :ref:`các đường dẫn cài đặt <sysconfig-user-scheme>` cho ``python -m pip install --user``.

   .. seealso::

      :pep:`370` -- Thư mục site-packages của từng người dùng


.. envvar:: PYTHONEXECUTABLE

   Nếu biến môi trường này được đặt, ``sys.argv[0]`` sẽ được đặt thành giá trị của nó thay vì giá trị nhận được thông qua C runtime. Chỉ hoạt động trên macOS.

.. envvar:: PYTHONWARNINGS

   Tương đương với tùy chọn :option:`-W`. Nếu được đặt thành một chuỗi phân tách bằng dấu phẩy, tùy chọn này tương đương với việc chỉ định :option:`-W` nhiều lần, trong đó các filter ở vị trí sau trong danh sách được ưu tiên hơn các filter ở vị trí trước.

   Các thiết lập đơn giản nhất sẽ áp dụng một hành động cụ thể một cách vô điều kiện cho tất cả cảnh báo do một process phát ra (kể cả những cảnh báo vốn bị bỏ qua theo mặc định)::

       PYTHONWARNINGS=default  # Cảnh báo một lần cho mỗi vị trí gọi
       PYTHONWARNINGS=error    # Chuyển thành exception
       PYTHONWARNINGS=always   # Cảnh báo mỗi lần
       PYTHONWARNINGS=all      # Tương tự như PYTHONWARNINGS=always
       PYTHONWARNINGS=module   # Cảnh báo một lần cho mỗi mô-đun gọi
       PYTHONWARNINGS=once     # Cảnh báo một lần cho mỗi tiến trình Python
       PYTHONWARNINGS=ignore   # Không bao giờ cảnh báo

   Xem :ref:`warning-filter` và :ref:`describing-warning-filters` để biết thêm chi tiết.


.. envvar:: PYTHONFAULTHANDLER

   Nếu biến môi trường này được đặt thành một chuỗi không rỗng,
   :func:`faulthandler.enable` được gọi khi khởi động: cài đặt trình xử lý cho
   :const:`~signal.SIGSEGV`, :const:`~signal.SIGFPE`,
   :const:`~signal.SIGABRT`, :const:`~signal.SIGBUS` và
   :const:`~signal.SIGILL` báo hiệu để kết xuất traceback Python. Tương đương với tùy chọn :option:`-X` ``faulthandler``.

   .. versionadded:: 3.3


.. envvar:: PYTHONTRACEMALLOC

   Nếu biến môi trường này được đặt thành một chuỗi không rỗng, hãy bắt đầu theo dõi các cấp phát bộ nhớ Python bằng module :mod:`tracemalloc`. Giá trị của biến là số frame tối đa được lưu trong traceback của một trace. Ví dụ, ``PYTHONTRACEMALLOC=1`` chỉ lưu frame gần đây nhất. Xem hàm :func:`tracemalloc.start` để biết thêm thông tin. Tương đương với việc đặt tùy chọn :option:`-X` ``tracemalloc``.

   .. versionadded:: 3.4


.. envvar:: PYTHONPROFILEIMPORTTIME

   Nếu biến môi trường này được đặt thành ``1``, Python sẽ hiển thị thời gian cần thiết cho mỗi lần import. Nếu được đặt thành ``2``, Python sẽ bao gồm cả đầu ra của các module đã import và được tải từ trước. Tương đương với việc đặt tùy chọn :option:`-X` ``importtime``.

   .. versionadded:: 3.7

   .. versionchanged:: 3.14

      Đã thêm ``PYTHONPROFILEIMPORTTIME=2`` để cũng theo dõi các lần import những module đã được tải.


.. envvar:: PYTHONASYNCIODEBUG

   Nếu biến môi trường này được đặt thành một chuỗi không rỗng, hãy bật
   :ref:`chế độ debug <asyncio-debug-mode>` của module :mod:`asyncio`.

   .. versionadded:: 3.4


.. envvar:: PYTHONMALLOC

   Thiết lập các bộ cấp phát bộ nhớ của Python và/hoặc cài đặt các hook debug.

   Thiết lập nhóm bộ cấp phát bộ nhớ được Python sử dụng:

   * ``default``: sử dụng :ref:`các bộ cấp phát bộ nhớ mặc định <default-memory-allocators>`.
   * ``malloc``: sử dụng hàm :c:func:`malloc` của thư viện C cho tất cả các miền (:c:macro:`PYMEM_DOMAIN_RAW`, :c:macro:`PYMEM_DOMAIN_MEM`,
     :c:macro:`PYMEM_DOMAIN_OBJ`).
   * ``pymalloc``: sử dụng :ref:`bộ cấp phát pymalloc <pymalloc>` cho
     :c:macro:`PYMEM_DOMAIN_MEM` và các miền :c:macro:`PYMEM_DOMAIN_OBJ`, đồng thời sử dụng hàm :c:func:`malloc` cho miền :c:macro:`PYMEM_DOMAIN_RAW`.
   * ``mimalloc``: sử dụng :ref:`bộ cấp phát mimalloc <mimalloc>` cho
     :c:macro:`PYMEM_DOMAIN_MEM` và các miền :c:macro:`PYMEM_DOMAIN_OBJ`, đồng thời sử dụng hàm :c:func:`malloc` cho miền :c:macro:`PYMEM_DOMAIN_RAW`.

   Cài đặt :ref:`debug hooks <pymem-debug-hooks>`:

   * ``debug``: cài đặt các debug hooks trên các bộ cấp phát bộ nhớ :ref:`mặc định <default-memory-allocators>`.
   * ``malloc_debug``: giống như ``malloc`` nhưng cũng cài đặt các debug hooks.
   * ``pymalloc_debug``: giống như ``pymalloc`` nhưng cũng cài đặt các debug hooks.
   * ``mimalloc_debug``: giống như ``mimalloc`` nhưng cũng cài đặt các debug hooks.

   .. note::

      Trong bản build :term:`free-threaded <free threading>`, các giá trị ``malloc``, ``malloc_debug``, ``pymalloc`` và ``pymalloc_debug`` không được hỗ trợ. Chỉ chấp nhận ``default``, ``debug``, ``mimalloc`` và ``mimalloc_debug``.

   .. versionadded:: 3.6

   .. versionchanged:: 3.7
      Đã thêm allocator ``"default"``.


.. envvar:: PYTHONMALLOCSTATS

   Nếu được đặt thành một chuỗi không rỗng, Python sẽ in thống kê của
   :ref:`pymalloc memory allocator <pymalloc>` hoặc
   :ref:`mimalloc memory allocator <mimalloc>` (tùy allocator nào đang được sử dụng) mỗi khi một object arena mới được tạo và khi tắt.

   Biến này bị bỏ qua nếu biến môi trường :envvar:`PYTHONMALLOC` được sử dụng để buộc dùng :c:func:`malloc` allocator của thư viện C, hoặc nếu Python được cấu hình mà không có hỗ trợ ``pymalloc`` và ``mimalloc``.

   .. versionchanged:: 3.6
      Biến này hiện cũng có thể được sử dụng trên Python được biên dịch ở chế độ release. Hiện biến này không có tác dụng nếu được đặt thành một chuỗi rỗng.


.. envvar:: PYTHONLEGACYWINDOWSFSENCODING

   Nếu được đặt thành một chuỗi không rỗng, chế độ :term:`filesystem encoding and error handler` mặc định sẽ trở về các giá trị trước phiên bản 3.6 là 'mbcs' và 'replace', tương ứng. Nếu không, các giá trị mặc định mới 'utf-8' và 'surrogatepass' sẽ được sử dụng.

   Tùy chọn này cũng có thể được bật trong runtime bằng
   :func:`sys._enablelegacywindowsfsencoding`.

   .. availability:: Windows.

   .. versionadded:: 3.6
      Xem :pep:`529` để biết thêm chi tiết.

.. envvar:: PYTHONLEGACYWINDOWSSTDIO

   Nếu được đặt thành một chuỗi không rỗng, tùy chọn này sẽ không sử dụng reader và writer mới cho console. Điều này có nghĩa là các ký tự Unicode sẽ được mã hóa theo code page của console đang hoạt động, thay vì sử dụng utf-8.

   Biến này bị bỏ qua nếu các stream chuẩn được chuyển hướng (tới tệp hoặc pipe) thay vì tham chiếu đến các console buffer.

   .. availability:: Windows.

   .. versionadded:: 3.6


.. envvar:: PYTHONCOERCECLOCALE

   Nếu được đặt thành giá trị ``0``, biến này khiến ứng dụng dòng lệnh Python chính bỏ qua việc chuyển đổi các locale C và POSIX dựa trên ASCII cũ sang một locale thay thế mạnh hơn dựa trên UTF-8.

   Nếu biến này *không* được đặt (hoặc được đặt thành một giá trị khác ``0``), biến môi trường ghi đè locale ``LC_ALL`` cũng không được đặt, và locale hiện tại được báo cáo cho danh mục ``LC_CTYPE`` là locale ``C`` mặc định hoặc locale ``POSIX`` dựa trên ASCII được chỉ định rõ ràng, thì Python CLI sẽ cố gắng cấu hình các locale sau cho danh mục ``LC_CTYPE`` theo thứ tự được liệt kê trước khi tải interpreter runtime:

   * ``C.UTF-8``
   * ``C.utf8``
   * ``UTF-8``

   Nếu việc thiết lập một trong các nhóm locale này thành công, thì biến môi trường ``LC_CTYPE`` cũng sẽ được thiết lập tương ứng trong môi trường của tiến trình hiện tại trước khi runtime Python được khởi tạo. Điều này đảm bảo rằng ngoài việc được chính interpreter và các thành phần nhận biết locale khác đang chạy trong cùng tiến trình nhìn thấy (chẳng hạn như thư viện GNU ``readline``), thiết lập đã cập nhật cũng được nhìn thấy trong các subprocess (bất kể các tiến trình đó có chạy interpreter Python hay không), cũng như trong các thao tác truy vấn môi trường thay vì locale C hiện tại (chẳng hạn như :func:`locale.getdefaultlocale` của Python).

   Việc cấu hình một trong các locale này (dù là một cách rõ ràng hay thông qua cơ chế cưỡng chế locale ngầm định nêu trên) sẽ tự động bật ``surrogateescape``
   :ref:`trình xử lý lỗi <error-handlers>` cho :data:`sys.stdin` và
   :data:`sys.stdout` (:data:`sys.stderr` vẫn tiếp tục sử dụng ``backslashreplace`` như trong mọi locale khác). Hành vi xử lý stream này có thể được ghi đè bằng :envvar:`PYTHONIOENCODING` như thường lệ.

   Để phục vụ việc gỡ lỗi, việc thiết lập ``PYTHONCOERCECLOCALE=warn`` sẽ khiến Python phát ra các thông báo cảnh báo trên ``stderr`` nếu cơ chế cưỡng chế locale được kích hoạt, hoặc nếu một locale mà *sẽ* kích hoạt cơ chế cưỡng chế vẫn đang hoạt động khi runtime Python được khởi tạo.

   Cũng lưu ý rằng ngay cả khi cơ chế cưỡng chế locale bị tắt, hoặc khi cơ chế này không tìm được locale đích phù hợp, :envvar:`PYTHONUTF8` vẫn sẽ được bật theo mặc định trong các locale ASCII cũ. Cả hai tính năng đều phải được tắt để buộc interpreter sử dụng ``ASCII`` thay vì ``UTF-8`` cho các giao diện hệ thống.

   .. availability:: Unix.

   .. versionadded:: 3.7
      Xem :pep:`538` để biết thêm chi tiết.


.. envvar:: PYTHONDEVMODE

   Nếu biến môi trường này được đặt thành một chuỗi không rỗng, hãy bật
   :ref:`Python Development Mode <devmode>`, bổ sung các bước kiểm tra runtime có chi phí quá cao nên không được bật theo mặc định. Điều này tương đương với việc đặt tùy chọn :option:`-X` ``dev``.

   .. versionadded:: 3.7

.. envvar:: PYTHONUTF8

   Nếu được đặt thành ``1``, hãy bật :ref:`Python UTF-8 Mode <utf8-mode>`.

   Nếu được đặt thành ``0``, hãy tắt :ref:`Python UTF-8 Mode <utf8-mode>`.

   Việc đặt thành bất kỳ chuỗi không rỗng nào khác sẽ gây ra lỗi trong quá trình khởi tạo interpreter.

   .. versionadded:: 3.7

.. envvar:: PYTHONWARNDEFAULTENCODING

   Nếu biến môi trường này được đặt thành một chuỗi không rỗng, hãy phát ra một
   :class:`EncodingWarning` khi sử dụng encoding mặc định dành riêng cho locale.

   Xem :ref:`io-encoding-warning` để biết chi tiết.

   .. versionadded:: 3.10

.. envvar:: PYTHONNODEBUGRANGES

   Nếu biến này được thiết lập, biến sẽ tắt việc đưa vào các bảng ánh xạ thông tin vị trí bổ sung (dòng kết thúc, độ lệch cột bắt đầu và độ lệch cột kết thúc) cho mọi lệnh trong các code object. Điều này hữu ích khi cần các code object và tệp pyc nhỏ hơn, đồng thời ẩn các chỉ báo vị trí trực quan bổ sung khi interpreter hiển thị traceback.

   .. versionadded:: 3.11

.. envvar:: PYTHONPERFSUPPORT

   Nếu biến này được thiết lập thành một giá trị khác không, biến sẽ bật hỗ trợ cho profiler ``perf`` của Linux để profiler này có thể phát hiện các lệnh gọi Python.

   Nếu được thiết lập thành ``0``, tắt hỗ trợ profiler ``perf`` của Linux.

   Xem thêm tùy chọn dòng lệnh :option:`-X perf <-X>` và :ref:`perf_profiling`.

   .. versionadded:: 3.12

.. envvar:: PYTHON_PERF_JIT_SUPPORT

   Nếu biến này được thiết lập thành một giá trị khác không, biến sẽ bật hỗ trợ cho profiler ``perf`` của Linux để profiler này có thể phát hiện các lệnh gọi Python bằng thông tin DWARF.

   Nếu được thiết lập thành ``0``, tắt hỗ trợ profiler ``perf`` của Linux.

   Xem thêm tùy chọn dòng lệnh :option:`-X perf_jit <-X>` và :ref:`perf_profiling`.

   .. versionadded:: 3.13

.. envvar:: PYTHON_DISABLE_REMOTE_DEBUG

   Nếu biến này được đặt thành một chuỗi không rỗng, biến sẽ vô hiệu hóa tính năng gỡ lỗi từ xa được mô tả trong :pep:`768`. Tính năng này bao gồm cả chức năng lập lịch mã để thực thi trong một tiến trình khác và chức năng nhận mã để thực thi trong tiến trình hiện tại.

   Xem thêm tùy chọn dòng lệnh :option:`-X disable_remote_debug`.

   .. versionadded:: 3.14

.. envvar:: PYTHON_CPU_COUNT

   Nếu biến này được đặt thành một số nguyên dương, biến sẽ ghi đè các giá trị trả về của :func:`os.cpu_count` và :func:`os.process_cpu_count`.

   Xem thêm tùy chọn dòng lệnh :option:`-X cpu_count <-X>`.

   .. versionadded:: 3.13

.. envvar:: PYTHON_FROZEN_MODULES

   Nếu biến này được đặt thành ``on`` hoặc ``off``, biến sẽ xác định các mô-đun đóng băng có bị cơ chế import bỏ qua hay không. Giá trị ``on`` có nghĩa là chúng được import, còn ``off`` có nghĩa là chúng bị bỏ qua. Giá trị mặc định là ``on`` đối với các bản build không gỡ lỗi (trường hợp thông thường) và ``off`` đối với các bản build gỡ lỗi. Lưu ý rằng :mod:`!importlib_bootstrap` và
   các mô-đun đóng băng :mod:`!importlib_bootstrap_external` luôn được sử dụng, ngay cả khi cờ này được đặt thành ``off``.

   Xem thêm tùy chọn dòng lệnh :option:`-X frozen_modules <-X>`.

   .. versionadded:: 3.13

.. envvar:: PYTHON_COLORS

   Nếu biến này được đặt thành ``1``, interpreter sẽ tô màu nhiều loại đầu ra khác nhau. Đặt biến này thành ``0`` sẽ tắt hành vi này. Xem thêm :ref:`using-on-controlling-color`.

   .. versionadded:: 3.13

.. envvar:: PYTHON_BASIC_REPL

   Nếu biến này được đặt thành bất kỳ giá trị nào, interpreter sẽ không cố tải :term:`REPL` dựa trên Python, vốn yêu cầu :mod:`readline`, mà thay vào đó sẽ sử dụng :term:`REPL` dựa trên parser truyền thống.

   .. versionadded:: 3.13

.. envvar:: PYTHON_HISTORY

   Có thể sử dụng biến môi trường này để đặt vị trí của tệp ``.python_history`` (theo mặc định, tệp nằm tại ``.python_history`` trong thư mục chính của người dùng).

   .. versionadded:: 3.13

.. envvar:: PYTHON_GIL

   Nếu biến này được đặt thành ``1``, global interpreter lock (GIL) sẽ bị buộc bật. Đặt biến này thành ``0`` sẽ buộc GIL tắt (cần Python được cấu hình với tùy chọn build :option:`--disable-gil`).

   Xem thêm tùy chọn dòng lệnh :option:`-X gil <-X>`, tùy chọn này được ưu tiên hơn biến này, và :ref:`whatsnew313-free-threaded-cpython`.

   .. versionadded:: 3.13

.. envvar:: PYTHON_THREAD_INHERIT_CONTEXT

   Nếu biến này được đặt thành ``1`` thì theo mặc định, :class:`~threading.Thread` sẽ sử dụng một bản sao context của caller gọi ``Thread.start()`` khi khởi động. Nếu không, các thread mới sẽ bắt đầu với context rỗng. Nếu không được đặt, biến này mặc định là ``1`` trên các bản build free-threaded và ``0`` trong các trường hợp khác. Xem thêm :option:`-X thread_inherit_context<-X>`.

   .. versionadded:: 3.14

.. envvar:: PYTHON_CONTEXT_AWARE_WARNINGS

   Nếu được đặt thành ``1`` thì context manager :class:`warnings.catch_warnings` sẽ sử dụng :class:`~contextvars.ContextVar` để lưu trạng thái bộ lọc cảnh báo. Nếu không được đặt, biến này mặc định là ``1`` trên các bản build free-threaded và là ``0`` trong các trường hợp khác. Xem :option:`-X context_aware_warnings<-X>`.

   .. versionadded:: 3.14

.. envvar:: PYTHON_JIT

   Trên các bản build có hỗ trợ biên dịch just-in-time thử nghiệm, biến này có thể buộc JIT bị tắt (``0``) hoặc được bật (``1``) khi interpreter khởi động.

   .. versionadded:: 3.13

.. envvar:: PYTHON_TLBC

   Nếu được đặt thành ``1``, tính năng bytecode cục bộ theo thread sẽ được bật. Nếu được đặt thành ``0``, bytecode cục bộ theo thread và specializing interpreter sẽ bị tắt. Chỉ áp dụng cho các bản build được cấu hình với :option:`--disable-gil`.

   Xem thêm tùy chọn dòng lệnh :option:`-X tlbc <-X>`.

   .. versionadded:: 3.14

Các biến trong chế độ debug
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. envvar:: PYTHONDUMPREFS

   Nếu được đặt, Python sẽ kết xuất các object và số lượng tham chiếu vẫn còn tồn tại sau khi interpreter tắt.

   Yêu cầu Python được cấu hình với tùy chọn build :option:`--with-trace-refs`.

.. envvar:: PYTHONDUMPREFSFILE

   Nếu được thiết lập, Python sẽ ghi các đối tượng và số lượng tham chiếu vẫn còn tồn tại sau khi tắt trình thông dịch vào một tệp trong đường dẫn được cung cấp làm giá trị cho biến môi trường này.

   Yêu cầu Python được cấu hình với tùy chọn build :option:`--with-trace-refs`.

   .. versionadded:: 3.11

.. envvar:: PYTHON_PRESITE

   Nếu biến này được thiết lập thành một module, module đó sẽ được import sớm trong vòng đời của trình thông dịch, trước khi module :mod:`site` được thực thi và trước khi module :mod:`__main__` được tạo. Do đó, module được import không được coi là :mod:`__main__`.

   Có thể sử dụng biến này để thực thi mã sớm trong quá trình khởi tạo Python.

   Để import một submodule, hãy sử dụng ``package.module`` làm giá trị, giống như trong một câu lệnh import.

   Xem thêm tùy chọn dòng lệnh :option:`-X presite <-X>`, tùy chọn này được ưu tiên hơn biến này.

   Cần có Python được cấu hình với tùy chọn build :option:`--with-pydebug`.

   .. versionadded:: 3.13
