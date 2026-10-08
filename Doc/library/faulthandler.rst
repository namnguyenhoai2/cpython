:mod:`!faulthandler` --- Kết xuất traceback Python
==================================================

.. module:: faulthandler
   :synopsis: Kết xuất traceback Python.

.. versionadded:: 3.3

----------------

Mô-đun này chứa các hàm để kết xuất traceback Python một cách rõ ràng khi xảy ra lỗi, sau một khoảng thời gian chờ hoặc khi nhận được tín hiệu người dùng. Gọi :func:`faulthandler.enable` để cài đặt các trình xử lý lỗi cho :const:`~signal.SIGSEGV`,
:const:`~signal.SIGFPE`, :const:`~signal.SIGABRT`, :const:`~signal.SIGBUS` và
:const:`~signal.SIGILL`. Bạn cũng có thể bật chúng khi khởi động bằng cách đặt biến môi trường :envvar:`PYTHONFAULTHANDLER` hoặc sử dụng tùy chọn dòng lệnh :option:`-X` ``faulthandler``.

Trình xử lý lỗi tương thích với các trình xử lý lỗi hệ thống như Apport hoặc trình xử lý lỗi của Windows. Mô-đun này sử dụng một ngăn xếp thay thế cho các trình xử lý tín hiệu nếu hàm :c:func:`!sigaltstack` khả dụng. Nhờ đó, mô-đun vẫn có thể kết xuất traceback ngay cả khi bị tràn ngăn xếp.

Trình xử lý lỗi được gọi trong các trường hợp nghiêm trọng, do đó chỉ có thể sử dụng các hàm an toàn với tín hiệu (ví dụ: không thể cấp phát bộ nhớ trên heap). Vì hạn chế này, việc kết xuất traceback có mức độ chi tiết tối thiểu so với traceback Python thông thường:

* Chỉ ASCII được hỗ trợ. Trình xử lý lỗi ``backslashreplace`` được sử dụng khi mã hóa.
* Mỗi chuỗi được giới hạn ở 500 ký tự.
* Chỉ tên tệp, tên hàm và số dòng được hiển thị. (không có mã nguồn)
* Giới hạn là 100 frame và 100 thread.
* Thứ tự bị đảo ngược: lệnh gọi gần đây nhất được hiển thị trước.

Theo mặc định, traceback của Python được ghi vào :data:`sys.stderr`. Để xem traceback, ứng dụng phải được chạy trong terminal. Ngoài ra, có thể truyền tệp nhật ký cho :func:`faulthandler.enable`.

Mô-đun này được triển khai bằng C, vì vậy traceback có thể được kết xuất khi xảy ra sự cố hoặc khi Python bị deadlock.

:ref:`Python Development Mode <devmode>` gọi :func:`faulthandler.enable` khi Python khởi động.

.. seealso::

   Mô-đun :mod:`pdb`
      Trình gỡ lỗi mã nguồn tương tác cho các chương trình Python.

   Mô-đun :mod:`traceback`
      Giao diện tiêu chuẩn để trích xuất, định dạng và in stack trace của các chương trình Python.

Ghi traceback
-------------

.. function:: dump_traceback(file=sys.stderr, all_threads=True)

   Ghi traceback của tất cả các thread vào *file*. Nếu *all_threads* là ``False``, chỉ ghi thread hiện tại.

   .. seealso:: :func:`traceback.print_tb`, có thể được dùng để in một đối tượng traceback.

   .. versionchanged:: 3.5
      Đã bổ sung hỗ trợ truyền file descriptor cho hàm này.


Kết xuất stack C
----------------

.. versionadded:: 3.14

.. function:: dump_c_stack(file=sys.stderr)

   Kết xuất stack trace C của thread hiện tại vào *tệp*.

   Nếu bản dựng Python không hỗ trợ tính năng này hoặc hệ điều hành không cung cấp stack trace, thì một lỗi sẽ được in ra thay cho C stack được kết xuất.

.. _c-stack-compatibility:

Khả năng tương thích của C stack
********************************

Nếu hệ thống không hỗ trợ :manpage:`backtrace(3)` hoặc :manpage:`dladdr1(3)` ở cấp C, thì việc kết xuất C stack sẽ không hoạt động. Thay vào đó, một lỗi sẽ được in ra.

Ngoài ra, một số compiler không hỗ trợ việc triển khai kết xuất ngăn xếp C của :term:`CPython's <CPython>`. Do đó, một lỗi khác có thể được in ra thay vì ngăn xếp, ngay cả khi hệ điều hành hỗ trợ kết xuất ngăn xếp.

.. note::

   Việc kết xuất ngăn xếp C có thể chậm tùy ý, tùy thuộc vào cấp độ DWARF của các binary trong call stack.

Trạng thái fault handler
------------------------

.. function:: enable(file=sys.stderr, all_threads=True, c_stack=True)

   Bật fault handler: cài đặt các handler cho :const:`~signal.SIGSEGV`,
   :const:`~signal.SIGFPE`, :const:`~signal.SIGABRT`, :const:`~signal.SIGBUS` và :const:`~signal.SIGILL` để kết xuất Python traceback. Nếu *all_threads* là ``True``, tạo traceback cho mọi thread đang chạy. Nếu không, chỉ kết xuất thread hiện tại.

   *file* phải được giữ mở cho đến khi fault handler bị tắt: xem
   :ref:`issue with file descriptors <faulthandler-fd>`.

   Nếu *c_stack* là ``True``, thì dấu vết ngăn xếp C sẽ được in sau traceback Python, trừ khi hệ thống không hỗ trợ tính năng này. Xem :func:`dump_c_stack` để biết thêm thông tin về khả năng tương thích.

   .. versionchanged:: 3.5
      Đã bổ sung hỗ trợ truyền file descriptor vào hàm này.

   .. versionchanged:: 3.6
      Trên Windows, một handler cho ngoại lệ Windows cũng được cài đặt.

   .. versionchanged:: 3.10
      Kết quả kết xuất hiện cho biết liệu một lần thu gom của garbage collector có đang chạy hay không nếu *all_threads* là true.

   .. versionchanged:: 3.14
      Chỉ thread hiện tại được kết xuất nếu :term:`GIL` bị tắt để ngăn ngừa nguy cơ xảy ra data race.

   .. versionchanged:: 3.14
      Kết quả kết xuất hiện hiển thị dấu vết ngăn xếp C nếu *c_stack* là true.

.. function:: disable()

   Tắt fault handler: gỡ cài đặt các signal handler được cài đặt bởi
   :func:`enable`.

.. function:: is_enabled()

   Kiểm tra xem fault handler đã được bật hay chưa.


Dump traceback sau khi hết thời gian chờ
----------------------------------------

.. function:: dump_traceback_later(timeout, repeat=False, file=sys.stderr, exit=False)

   Dump traceback của tất cả các thread sau *timeout* giây, hoặc cứ mỗi *timeout* giây nếu *repeat* là ``True``. Nếu *exit* là ``True``, hãy gọi
   :c:func:`!_exit` với status=1 sau khi dump traceback. (Lưu ý
   :c:func:`!_exit` thoát khỏi process ngay lập tức, nghĩa là nó không thực hiện bất kỳ thao tác cleanup nào, chẳng hạn như flush file buffer.) Nếu hàm được gọi hai lần, lần gọi mới sẽ thay thế các tham số trước đó và đặt lại thời gian chờ. Bộ hẹn giờ có độ phân giải dưới một giây.

   Phải giữ *file* mở cho đến khi traceback được dump hoặc
   :func:`cancel_dump_traceback_later` được gọi: xem :ref:`issue with file descriptors <faulthandler-fd>`.

   Hàm này được triển khai bằng một watchdog thread.

   .. versionchanged:: 3.5
      Đã bổ sung hỗ trợ truyền file descriptor cho hàm này.

   .. versionchanged:: 3.7
      Hàm này hiện luôn khả dụng.

.. function:: cancel_dump_traceback_later()

   Hủy lệnh gọi cuối cùng tới :func:`dump_traceback_later`.


Dump traceback khi nhận tín hiệu từ người dùng
----------------------------------------------

.. function:: register(signum, file=sys.stderr, all_threads=True, chain=False)

   Đăng ký một tín hiệu từ người dùng: cài đặt một handler cho tín hiệu *signum* để dump traceback của tất cả các thread, hoặc của thread hiện tại nếu *all_threads* là ``False``, vào *file*. Gọi handler trước đó nếu chain là ``True``.

   *file* phải được mở cho đến khi tín hiệu được hủy đăng ký bởi
   :func:`unregister`: xem :ref:`vấn đề với file descriptor <faulthandler-fd>`.

   Không khả dụng trên Windows.

   .. versionchanged:: 3.5
      Đã bổ sung hỗ trợ truyền file descriptor cho hàm này.

.. function:: unregister(signum)

   Hủy đăng ký một user signal: gỡ handler của signal *signum* do :func:`register` cài đặt. Trả về ``True`` nếu signal đã được đăng ký, ngược lại trả về ``False``.

   Không khả dụng trên Windows.


.. _faulthandler-fd:

Vấn đề với file descriptor
--------------------------

:func:`enable`, :func:`dump_traceback_later` và :func:`register` giữ file descriptor của đối số *file*. Nếu tệp bị đóng và file descriptor của nó được một tệp mới sử dụng lại, hoặc nếu :func:`os.dup2` được dùng để thay thế file descriptor, traceback sẽ được ghi vào một tệp khác. Hãy gọi lại các hàm này mỗi khi tệp được thay thế.


Ví dụ
-----

Ví dụ về lỗi segmentation fault trên Linux khi bật và không bật trình xử lý lỗi:

.. code-block:: shell-session

    $ python -c "import ctypes; ctypes.string_at(0)"
    Segmentation fault

    $ python -q -X faulthandler
    >>> import ctypes
    >>> ctypes.string_at(0)
    Fatal Python error: Segmentation fault

    Current thread 0x00007fb899f39700 (most recent call first):
      File "/opt/python/Lib/ctypes/__init__.py", line 486 in string_at
      File "<stdin>", line 1 in <module>

    Current thread's C stack trace (most recent call first):
      Binary file "/opt/python/python", at _Py_DumpStack+0x42 [0x5b27f7d7147e]
      Binary file "/opt/python/python", at +0x32dcbd [0x5b27f7d85cbd]
      Binary file "/opt/python/python", at +0x32df8a [0x5b27f7d85f8a]
      Binary file "/usr/lib/libc.so.6", at +0x3def0 [0x77b73226bef0]
      Binary file "/usr/lib/libc.so.6", at +0x17ef9c [0x77b7323acf9c]
      Binary file "/opt/python/build/lib.linux-x86_64-3.14/_ctypes.cpython-314d-x86_64-linux-gnu.so", at +0xcdf6 [0x77b7315dddf6]
      Binary file "/usr/lib/libffi.so.8", at +0x7976 [0x77b73158f976]
      Binary file "/usr/lib/libffi.so.8", at +0x413c [0x77b73158c13c]
      Binary file "/usr/lib/libffi.so.8", at ffi_call+0x12e [0x77b73158ef0e]
      Binary file "/opt/python/build/lib.linux-x86_64-3.14/_ctypes.cpython-314d-x86_64-linux-gnu.so", at +0x15a33 [0x77b7315e6a33]
      Binary file "/opt/python/build/lib.linux-x86_64-3.14/_ctypes.cpython-314d-x86_64-linux-gnu.so", at +0x164fa [0x77b7315e74fa]
      Binary file "/opt/python/build/lib.linux-x86_64-3.14/_ctypes.cpython-314d-x86_64-linux-gnu.so", at +0xc624 [0x77b7315dd624]
      Binary file "/opt/python/python", at _PyObject_MakeTpCall+0xce [0x5b27f7b73883]
      Binary file "/opt/python/python", at +0x11bab6 [0x5b27f7b73ab6]
      Binary file "/opt/python/python", at PyObject_Vectorcall+0x23 [0x5b27f7b73b04]
      Binary file "/opt/python/python", at _PyEval_EvalFrameDefault+0x490c [0x5b27f7cbb302]
      Binary file "/opt/python/python", at +0x2818e6 [0x5b27f7cd98e6]
      Binary file "/opt/python/python", at +0x281aab [0x5b27f7cd9aab]
      Binary file "/opt/python/python", at PyEval_EvalCode+0xc5 [0x5b27f7cd9ba3]
      Binary file "/opt/python/python", at +0x255957 [0x5b27f7cad957]
      Binary file "/opt/python/python", at +0x255ab4 [0x5b27f7cadab4]
      Binary file "/opt/python/python", at _PyEval_EvalFrameDefault+0x6c3e [0x5b27f7cbd634]
      Binary file "/opt/python/python", at +0x2818e6 [0x5b27f7cd98e6]
      Binary file "/opt/python/python", at +0x281aab [0x5b27f7cd9aab]
      Binary file "/opt/python/python", at +0x11b6e1 [0x5b27f7b736e1]
      Binary file "/opt/python/python", at +0x11d348 [0x5b27f7b75348]
      Binary file "/opt/python/python", at +0x11d626 [0x5b27f7b75626]
      Binary file "/opt/python/python", at PyObject_Call+0x20 [0x5b27f7b7565e]
      Binary file "/opt/python/python", at +0x32a67a [0x5b27f7d8267a]
      Binary file "/opt/python/python", at +0x32a7f8 [0x5b27f7d827f8]
      Binary file "/opt/python/python", at +0x32ac1b [0x5b27f7d82c1b]
      Binary file "/opt/python/python", at Py_RunMain+0x31 [0x5b27f7d82ebe]
      <truncated rest of calls>
    Segmentation fault
