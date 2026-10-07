.. _gdb:

========================================================
Gỡ lỗi các phần mở rộng C API và nội bộ CPython bằng GDB
========================================================

.. highlight:: none

Tài liệu này giải thích cách sử dụng phần mở rộng GDB dành cho Python, ``python-gdb.py``, với trình gỡ lỗi GDB để gỡ lỗi các phần mở rộng CPython và chính trình thông dịch CPython.

Khi gỡ lỗi các sự cố cấp thấp như lỗi crash hoặc deadlock, một trình gỡ lỗi cấp thấp như GDB rất hữu ích để chẩn đoán và khắc phục sự cố. Theo mặc định, GDB (hoặc bất kỳ front-end nào của nó) không hỗ trợ thông tin cấp cao dành riêng cho trình thông dịch CPython.

Phần mở rộng ``python-gdb.py`` bổ sung thông tin về trình thông dịch CPython vào GDB. Phần mở rộng này giúp xem xét stack của các hàm Python đang thực thi. Với một đối tượng Python được biểu diễn bằng con trỏ :c:expr:`PyObject *`, phần mở rộng sẽ hiển thị kiểu và giá trị của đối tượng.

Các nhà phát triển đang làm việc trên các phần mở rộng CPython hoặc tìm hiểu các phần của CPython được viết bằng C có thể sử dụng tài liệu này để tìm hiểu cách dùng phần mở rộng ``python-gdb.py`` với GDB.

.. note::

   Tài liệu này giả định rằng bạn đã quen với những kiến thức cơ bản về GDB và C API của CPython. Tài liệu tổng hợp hướng dẫn từ `devguide <https://devguide.python.org>`_  và `Python wiki <https://wiki.python.org/moin/DebuggingWithGdb>`_.


Điều kiện tiên quyết
====================

Bạn cần có:

- GDB 7 trở lên. (Đối với các phiên bản GDB cũ hơn, hãy xem ``Misc/gdbinit`` trong mã nguồn của Python 3.11 hoặc các phiên bản cũ hơn.)
- Thông tin gỡ lỗi tương thích với GDB cho Python và mọi extension bạn đang gỡ lỗi.
- Extension ``python-gdb.py``.

Extension này được xây dựng cùng Python, nhưng có thể được phân phối riêng hoặc hoàn toàn không được phân phối. Dưới đây, chúng tôi đưa ra một số mẹo cho một vài hệ thống phổ biến để làm ví dụ. Lưu ý rằng ngay cả khi hướng dẫn phù hợp với hệ thống của bạn, chúng có thể đã lỗi thời.


Thiết lập với Python được xây dựng từ mã nguồn
----------------------------------------------

Khi bạn xây dựng CPython từ mã nguồn, thông tin gỡ lỗi sẽ có sẵn và quá trình build sẽ thêm một tệp ``python-gdb.py`` vào thư mục gốc của repository.

Để kích hoạt hỗ trợ, bạn phải thêm thư mục chứa ``python-gdb.py`` vào "auto-load-safe-path" của GDB. Nếu chưa thực hiện việc này, các phiên bản GDB gần đây sẽ in cảnh báo kèm hướng dẫn cách thực hiện.

.. note::

   Nếu bạn không thấy hướng dẫn dành cho phiên bản GDB của mình, hãy thêm nội dung này vào tệp cấu hình của bạn (``~/.gdbinit`` hoặc ``~/.config/gdb/gdbinit``)::

      add-auto-load-safe-path /path/to/cpython

   Bạn cũng có thể thêm nhiều đường dẫn, phân tách bằng ``:``.


Thiết lập cho Python từ bản phân phối Linux
-------------------------------------------

Hầu hết các hệ thống Linux đều cung cấp thông tin gỡ lỗi cho Python hệ thống trong một package có tên ``python-debuginfo``, ``python-dbg`` hoặc tên tương tự. Ví dụ:

- Fedora:

   .. code-block:: shell

      sudo dnf install gdb
      sudo dnf debuginfo-install python3

- Ubuntu:

   .. code-block:: shell

      sudo apt install gdb python3-dbg

Trên một số hệ thống Linux gần đây, GDB có thể tự động tải các ký hiệu debug bằng *debuginfod*. Tuy nhiên, thao tác này sẽ không cài đặt tiện ích mở rộng ``python-gdb.py``; nhìn chung, bạn vẫn cần cài riêng gói thông tin debug.


Sử dụng bản build Debug và development mode
===========================================

Để việc debug dễ dàng hơn, bạn có thể:

- Sử dụng một :ref:`debug build <debug-build>` của Python. (Khi build từ mã nguồn, hãy sử dụng ``configure --with-pydebug``. Trên các bản phân phối Linux, hãy cài đặt và chạy một gói như ``python-debug`` hoặc ``python-dbg``, nếu có.)
- Sử dụng :ref:`development mode <devmode>` của runtime (``-X dev``).

Cả hai đều bật các assertion bổ sung và tắt một số tối ưu hóa. Đôi khi, chúng che giấu lỗi mà bạn đang cố tìm, nhưng trong hầu hết trường hợp, chúng giúp quá trình này dễ dàng hơn.


Sử dụng tiện ích mở rộng ``python-gdb``
=======================================

Khi extension được tải, nó cung cấp hai tính năng chính: trình pretty-printer cho các giá trị Python và các command bổ sung.

Pretty-printer
--------------

Sau đây là hình dạng của một backtrace GDB (đã được rút gọn) khi extension này được bật::

   #0  0x000000000041a6b1 trong PyObject_Malloc (nbytes=Không thể truy cập bộ nhớ tại địa chỉ 0x7fffff7fefe8
   ) at Objects/obmalloc.c:748
   #1  0x000000000041b7c0 trong _PyObject_DebugMallocApi (id=111 'o', nbytes=24) tại Objects/obmalloc.c:1445
   #2  0x000000000041b717 trong _PyObject_DebugMalloc (nbytes=24) tại Objects/obmalloc.c:1412
   #3  0x000000000044060a trong _PyUnicode_New (length=11) tại Objects/unicodeobject.c:346
   #4  0x00000000004466aa in PyUnicodeUCS2_DecodeUTF8Stateful (s=0x5c2b8d "__lltrace__", size=11, errors=0x0, consumed=
       0x0) at Objects/unicodeobject.c:2531
   #5  0x0000000000446647 in PyUnicodeUCS2_DecodeUTF8 (s=0x5c2b8d "__lltrace__", size=11, errors=0x0)
       at Objects/unicodeobject.c:2495
   #6  0x0000000000440d1b in PyUnicodeUCS2_FromStringAndSize (u=0x5c2b8d "__lltrace__", size=11)
       at Objects/unicodeobject.c:551
   #7  0x0000000000440d94 in PyUnicodeUCS2_FromString (u=0x5c2b8d "__lltrace__") at Objects/unicodeobject.c:569
   #8  0x0000000000584abd in PyDict_GetItemString (v=
       {'Yuck': <type at remote 0xad4730>, '__builtins__': <module at remote 0x7ffff7fd5ee8>, '__file__': 'Lib/test/crashers/nasty_eq_vs_dict.py', '__package__': None, 'y': <Yuck(i=0) at remote 0xaacd80>, 'dict': {0: 0, 1: 1, 2: 2, 3: 3}, '__cached__': None, '__name__': '__main__', 'z': <Yuck(i=0) at remote 0xaace60>, '__doc__': None}, key=
       0x5c2b8d "__lltrace__") at Objects/dictobject.c:2171

Lưu ý rằng đối số dictionary truyền cho ``PyDict_GetItemString`` được hiển thị dưới dạng ``repr()`` của nó, thay vì một con trỏ ``PyObject *`` không rõ nội dung.

Extension này hoạt động bằng cách cung cấp một routine in tùy chỉnh cho các giá trị thuộc kiểu ``PyObject *``. Nếu bạn cần truy cập các chi tiết cấp thấp hơn của một object, hãy ép giá trị này thành một con trỏ có kiểu phù hợp. Ví dụ::

    (gdb) p globals
    $1 = {'__builtins__': <module at remote 0x7ffff7fb1868>, '__name__':
    '__main__', 'ctypes': <module at remote 0x7ffff7f14360>, '__doc__': None,
    '__package__': None}

    (gdb) p *(PyDictObject*)globals
    $2 = {ob_refcnt = 3, ob_type = 0x3dbdf85820, ma_fill = 5, ma_used = 5,
    ma_mask = 7, ma_table = 0x63d0f8, ma_lookup = 0x3dbdc7ea70
    <lookdict_string>, ma_smalltable = {{me_hash = 7065186196740147912,
    me_key = '__builtins__', me_value = <module at remote 0x7ffff7fb1868>},
    {me_hash = -368181376027291943, me_key = '__name__',
    me_value ='__main__'}, {me_hash = 0, me_key = 0x0, me_value = 0x0},
    {me_hash = 0, me_key = 0x0, me_value = 0x0},
    {me_hash = -9177857982131165996, me_key = 'ctypes',
    me_value = <module at remote 0x7ffff7f14360>},
    {me_hash = -8518757509529533123, me_key = '__doc__', me_value = None},
    {me_hash = 0, me_key = 0x0, me_value = 0x0}, {
      me_hash = 6614918939584953775, me_key = '__package__', me_value = None}}}

Lưu ý rằng các pretty-printer không thực sự gọi ``repr()``. Đối với các kiểu cơ bản, chúng cố gắng khớp sát với kết quả của nó.

Một điểm có thể gây nhầm lẫn là trình in tùy chỉnh cho một số kiểu trông rất giống trình in tích hợp sẵn của GDB dành cho các kiểu chuẩn. Ví dụ, pretty-printer cho một ``int`` Python (:c:expr:`PyLongObject *`) tạo ra biểu diễn không thể phân biệt với biểu diễn của một số nguyên thông thường ở cấp máy::

    (gdb) p some_machine_integer
    $3 = 42

    (gdb) p some_python_integer
    $4 = 42

Có thể tiết lộ cấu trúc nội bộ bằng cách ép kiểu sang :c:expr:`PyLongObject *`::

    (gdb) p *(PyLongObject*)some_python_integer
    $5 = {ob_base = {ob_base = {ob_refcnt = 8, ob_type = 0x3dad39f5e0}, ob_size = 1},
    ob_digit = {42}}

Sự nhầm lẫn tương tự có thể xảy ra với kiểu ``str``, trong đó đầu ra trông rất giống trình in tích hợp sẵn của gdb dành cho ``char *``::

    (gdb) p ptr_to_python_str
    $6 = '__builtins__'

Pretty-printer cho các thực thể ``str`` mặc định sử dụng dấu nháy đơn (giống như ``repr`` của Python dành cho chuỗi), trong khi trình in chuẩn cho các giá trị ``char *`` sử dụng dấu nháy kép và chứa một địa chỉ hệ thập lục phân::

    (gdb) p ptr_to_char_star
    $7 = 0x6d72c0 "hello world"

Một lần nữa, có thể tiết lộ các chi tiết triển khai bằng cách ép kiểu sang
:c:expr:`PyUnicodeObject *`::

    (gdb) p *(PyUnicodeObject*)$6
    $8 = {ob_base = {ob_refcnt = 33, ob_type = 0x3dad3a95a0}, length = 12,
    str = 0x7ffff2128500, hash = 7065186196740147912, state = 1, defenc = 0x0}

``py-list``
-----------

   Phần mở rộng bổ sung lệnh ``py-list``, lệnh này liệt kê mã nguồn Python (nếu có) của frame hiện tại trong thread được chọn. Dòng hiện tại được đánh dấu bằng ">"::

        (gdb) py-list
         901        if options.profile:
         902            options.profile = False
         903            profile_me()
         904            return
         905
        >906        u = UI()
         907        if not u.quit:
         908            try:
         909                gtk.main()
         910            except KeyboardInterrupt:
         911                # thoát đúng cách khi bị ngắt bằng bàn phím...

   Dùng ``py-list START`` để liệt kê tại một số dòng khác trong mã nguồn Python, và ``py-list START,END`` để liệt kê một phạm vi dòng cụ thể trong mã nguồn Python.

``py-up`` và ``py-down``
------------------------

   Các lệnh ``py-up`` và ``py-down`` tương tự như các lệnh ``up`` và ``down`` thông thường của GDB, nhưng cố gắng di chuyển ở cấp độ frame của CPython thay vì frame C.

   GDB không phải lúc nào cũng có thể đọc thông tin frame liên quan, tùy thuộc vào mức tối ưu hóa được sử dụng khi biên dịch CPython. Về bên trong, các lệnh tìm những frame C đang thực thi hàm đánh giá frame mặc định (tức là vòng lặp thông dịch bytecode cốt lõi bên trong CPython) và tra cứu giá trị của ``PyFrameObject *`` liên quan.

   Chúng xuất ra số frame (ở cấp C) trong thread.

   Ví dụ::

        (gdb) py-up
        #37 Khung 0x9420b04, cho tệp /usr/lib/python2.6/site-packages/
        gnome_sudoku/main.py, line 906, in start_game ()
            u = UI()
        (gdb) py-up
        #40 Khung 0x948e82c, cho tệp /usr/lib/python2.6/site-packages/
        gnome_sudoku/gnome_sudoku.py, line 22, in start_game(main=<module at remote 0xb771b7f4>)
            main.start_game()
        (gdb) py-up
        Unable to find an older python frame

   vậy là chúng ta đang ở đầu ngăn xếp Python.

   Các số khung tương ứng với những số được hiển thị bởi lệnh ``backtrace`` tiêu chuẩn của GDB. Lệnh này bỏ qua các khung C không thực thi mã Python.

   Đi xuống lại::

        (gdb) py-down
        #37 Khung 0x9420b04, cho tệp /usr/lib/python2.6/site-packages/gnome_sudoku/main.py, dòng 906, trong start_game ()
            u = UI()
        (gdb) py-down
        #34 (không thể đọc thông tin khung Python)
        (gdb) py-down
        #23 (không thể đọc thông tin frame Python)
        (gdb) py-down
        #19 (không thể đọc thông tin frame Python)
        (gdb) py-down
        #14 Frame 0x99262ac, trong tệp /usr/lib/python2.6/site-packages/gnome_sudoku/game_selector.py, dòng 201, trong run_swallowed_dialog (self=<NewOrSavedGameSelector(new_game_model=<gtk.ListStore at remote 0x98fab44>, puzzle=None, saved_games=[{'gsd.auto_fills': 0, 'tracking': {}, 'trackers': {}, 'notes': [], 'saved_at': 1270084485, 'game': '7 8 0 0 0 0 0 5 6 0 0 9 0 8 0 1 0 0 0 4 6 0 0 0 0 7 0 6 5 0 0 0 4 7 9 2 0 0 0 9 0 1 0 0 0 3 9 7 6 0 0 0 1 8 0 6 0 0 0 0 2 8 0 0 0 5 0 4 0 6 0 0 2 1 0 0 0 0 0 4 5\n7 8 0 0 0 0 0 5 6 0 0 9 0 8 0 1 0 0 0 4 6 0 0 0 0 7 0 6 5 1 8 3 4 7 9 2 0 0 0 9 0 1 0 0 0 3 9 7 6 0 0 0 1 8 0 6 0 0 0 0 2 8 0 0 0 5 0 4 0 6 0 0 2 1 0 0 0 0 0 4 5', 'gsd.impossible_hints': 0, 'timer.__absolute_start_time__': <float at remote 0x984b474>, 'gsd.hints': 0, 'timer.active_time': <float at remote 0x984b494>, 'timer.total_time': <float at remote 0x984b464>}], dialog=<gtk.Dialog at remote 0x98faaa4>, saved_game_model=<gtk.ListStore at remote 0x98fad24>, sudoku_maker=<SudokuMaker(terminated=False, played=[], batch_siz...(truncated)
                    swallower.run_dialog(self.dialog)
        (gdb) py-down
        #11 Frame 0x9aead74, trong tệp /usr/lib/python2.6/site-packages/gnome_sudoku/dialog_swallower.py, dòng 48, trong run_dialog (self=<SwappableArea(running=<gtk.Dialog at remote 0x98faaa4>, main_page=0) at remote 0x98fa6e4>, d=<gtk.Dialog at remote 0x98faaa4>)
                    gtk.main()
        (gdb) py-down
        #8 (không thể đọc thông tin frame Python)
        (gdb) py-down
        Unable to find a newer python frame

   và chúng ta đang ở cuối ngăn xếp Python.

   Lưu ý rằng trong Python 3.12 trở lên, cùng một frame ngăn xếp C có thể được sử dụng cho nhiều frame ngăn xếp Python. Điều này có nghĩa là ``py-up`` và ``py-down`` có thể di chuyển nhiều frame Python cùng một lúc. Ví dụ::

      (gdb) py-up
      #6 Khung 0x7ffff7fb62b0, tệp /tmp/rec.py, dòng 5, trong recursive_function (n=0)
         time.sleep(5)
      #6 Khung 0x7ffff7fb6240, tệp /tmp/rec.py, dòng 7, trong recursive_function (n=1)
         recursive_function(n-1)
      #6 Khung 0x7ffff7fb61d0, tệp /tmp/rec.py, dòng 7, trong recursive_function (n=2)
         recursive_function(n-1)
      #6 Khung 0x7ffff7fb6160, tệp /tmp/rec.py, dòng 7, trong recursive_function (n=3)
         recursive_function(n-1)
      #6 Khung 0x7ffff7fb60f0, tệp /tmp/rec.py, dòng 7, trong recursive_function (n=4)
         recursive_function(n-1)
      #6 Khung 0x7ffff7fb6080, tệp /tmp/rec.py, dòng 7, trong recursive_function (n=5)
         recursive_function(n-1)
      #6 Khung 0x7ffff7fb6020, tệp /tmp/rec.py, dòng 9, trong <module> ()
         recursive_function(5)
      (gdb) py-up
      Unable to find an older python frame


``py-bt``
---------

   Lệnh ``py-bt`` cố gắng hiển thị backtrace ở cấp Python của thread hiện tại.

   Ví dụ::

        (gdb) py-bt
        #8 (không thể đọc thông tin frame Python)
        #11 Khung 0x9aead74, trong tệp /usr/lib/python2.6/site-packages/gnome_sudoku/dialog_swallower.py, dòng 48, trong run_dialog (self=<SwappableArea(running=<gtk.Dialog at remote 0x98faaa4>, main_page=0) at remote 0x98fa6e4>, d=<gtk.Dialog at remote 0x98faaa4>)
                    gtk.main()
        #14 Khung 0x99262ac, trong tệp /usr/lib/python2.6/site-packages/gnome_sudoku/game_selector.py, dòng 201, trong run_swallowed_dialog (self=<NewOrSavedGameSelector(new_game_model=<gtk.ListStore at remote 0x98fab44>, puzzle=None, saved_games=[{'gsd.auto_fills': 0, 'tracking': {}, 'trackers': {}, 'notes': [], 'saved_at': 1270084485, 'game': '7 8 0 0 0 0 0 5 6 0 0 9 0 8 0 1 0 0 0 4 6 0 0 0 0 7 0 6 5 0 0 0 4 7 9 2 0 0 0 9 0 1 0 0 0 3 9 7 6 0 0 0 1 8 0 6 0 0 0 0 2 8 0 0 0 5 0 4 0 6 0 0 2 1 0 0 0 0 0 4 5\n7 8 0 0 0 0 0 5 6 0 0 9 0 8 0 1 0 0 0 4 6 0 0 0 0 7 0 6 5 1 8 3 4 7 9 2 0 0 0 9 0 1 0 0 0 3 9 7 6 0 0 0 1 8 0 6 0 0 0 0 2 8 0 0 0 5 0 4 0 6 0 0 2 1 0 0 0 0 0 4 5', 'gsd.impossible_hints': 0, 'timer.__absolute_start_time__': <float at remote 0x984b474>, 'gsd.hints': 0, 'timer.active_time': <float at remote 0x984b494>, 'timer.total_time': <float at remote 0x984b464>}], dialog=<gtk.Dialog at remote 0x98faaa4>, saved_game_model=<gtk.ListStore at remote 0x98fad24>, sudoku_maker=<SudokuMaker(terminated=False, played=[], batch_siz...(đã rút gọn)
                    swallower.run_dialog(self.dialog)
        #19 (không thể đọc thông tin frame Python)
        #23 (không thể đọc thông tin frame Python)
        #34 (không thể đọc thông tin frame Python)
        #37 Frame 0x9420b04, trong tệp /usr/lib/python2.6/site-packages/gnome_sudoku/main.py, dòng 906, trong start_game ()
            u = UI()
        #40 Frame 0x948e82c, trong tệp /usr/lib/python2.6/site-packages/gnome_sudoku/gnome_sudoku.py, dòng 22, trong start_game (main=<module at remote 0xb771b7f4>)
            main.start_game()

   Các số frame tương ứng với những số được hiển thị bởi lệnh ``backtrace`` tiêu chuẩn của GDB.

``py-print``
------------

   Lệnh ``py-print`` tra cứu một tên Python và cố gắng in tên đó. Lệnh tìm trong các biến cục bộ của thread hiện tại, sau đó là các biến toàn cục và cuối cùng là builtins::

        (gdb) py-print self
        local 'self' = <SwappableArea(running=<gtk.Dialog at remote 0x98faaa4>,
        main_page=0) at remote 0x98fa6e4>
        (gdb) py-print __name__
        global '__name__' = 'gnome_sudoku.dialog_swallower'
        (gdb) py-print len
        builtin 'len' = <built-in function len>
        (gdb) py-print scarlet_pimpernel
        'scarlet_pimpernel' not found

   Nếu frame C hiện tại tương ứng với nhiều frame Python, ``py-print`` chỉ xét frame đầu tiên.

``py-locals``
-------------

   Lệnh ``py-locals`` tra cứu tất cả biến cục bộ Python trong frame Python hiện tại của thread được chọn và in biểu diễn của chúng::

        (gdb) py-locals
        self = <SwappableArea(running=<gtk.Dialog at remote 0x98faaa4>,
        main_page=0) at remote 0x98fa6e4>
        d = <gtk.Dialog at remote 0x98faaa4>

   Nếu frame C hiện tại tương ứng với nhiều frame Python, các biến cục bộ từ tất cả chúng sẽ được hiển thị::

      (gdb) py-locals
      Locals for recursive_function
      n = 0
      Locals for recursive_function
      n = 1
      Locals for recursive_function
      n = 2
      Locals for recursive_function
      n = 3
      Locals for recursive_function
      n = 4
      Locals for recursive_function
      n = 5
      Locals for <module>


Sử dụng với các lệnh GDB
========================

Các lệnh mở rộng bổ sung cho các lệnh tích hợp sẵn của GDB. Ví dụ: bạn có thể sử dụng số frame được hiển thị bởi ``py-bt`` cùng với lệnh ``frame`` để chuyển đến một frame cụ thể trong thread đã chọn, như sau::

        (gdb) py-bt
        (output snipped)
        #68 Frame 0xaa4560, cho tệp Lib/test/regrtest.py, dòng 1548, trong <module> ()
                main()
        (gdb) frame 68
        #68 0x00000000004cd1e6 trong PyEval_EvalFrameEx (f=Frame 0xaa4560, cho tệp Lib/test/regrtest.py, dòng 1548, trong <module> (), throwflag=0) tại Python/ceval.c:2665
        2665                            x = call_function(&sp, oparg);
        (gdb) py-list
        1543        # Chạy các bài kiểm thử trong một context manager tạm thời thay đổi CWD thành một thư mục
        1544        # tạm thời và có thể ghi. Nếu không thể tạo hoặc
        1545        # thay đổi CWD, CWD ban đầu sẽ được sử dụng. CWD ban đầu là
        1546        # có sẵn trong test_support.SAVEDCWD.
        1547        with test_support.temp_cwd(TESTCWD, quiet=True):
        >1548            main()

Lệnh ``info threads`` sẽ cung cấp cho bạn danh sách các thread trong process, và bạn có thể sử dụng lệnh ``thread`` để chọn một thread khác::

        (gdb) info threads
          105 Thread 0x7fffefa18710 (LWP 10260)  sem_wait () at ../nptl/sysdeps/unix/sysv/linux/x86_64/sem_wait.S:86
          104 Thread 0x7fffdf5fe710 (LWP 10259)  sem_wait () at ../nptl/sysdeps/unix/sysv/linux/x86_64/sem_wait.S:86
        * 1 Thread 0x7ffff7fe2700 (LWP 10145)  0x00000038e46d73e3 in select () at ../sysdeps/unix/syscall-template.S:82

Bạn có thể sử dụng ``thread apply all COMMAND`` hoặc (``t a a COMMAND`` để viết ngắn) để chạy một lệnh trên tất cả thread. Với ``py-bt``, bạn có thể xem mỗi thread đang làm gì ở cấp độ Python::

        (gdb) t a a py-bt

        Thread 105 (Thread 0x7fffefa18710 (LWP 10260)):
        #5 Khung 0x7fffd00019d0, trong tệp /home/david/coding/python-svn/Lib/threading.py, dòng 155, trong _acquire_restore (self=<_RLock(_Verbose__verbose=False, _RLock__owner=140737354016512, _RLock__block=<thread.lock at remote 0x858770>, _RLock__count=1) at remote 0xd7ff40>, count_owner=(1, 140737213728528), count=1, owner=140737213728528)
                self.__block.acquire()
        #8 Khung 0x7fffac001640, trong tệp /home/david/coding/python-svn/Lib/threading.py, dòng 269, trong wait (self=<_Condition(_Condition__lock=<_RLock(_Verbose__verbose=False, _RLock__owner=140737354016512, _RLock__block=<thread.lock at remote 0x858770>, _RLock__count=1) at remote 0xd7ff40>, acquire=<instancemethod at remote 0xd80260>, _is_owned=<instancemethod at remote 0xd80160>, _release_save=<instancemethod at remote 0xd803e0>, release=<instancemethod at remote 0xd802e0>, _acquire_restore=<instancemethod at remote 0xd7ee60>, _Verbose__verbose=False, _Condition__waiters=[]) at remote 0xd7fd10>, timeout=None, waiter=<thread.lock at remote 0x858a90>, saved_state=(1, 140737213728528))
                    self._acquire_restore(saved_state)
        #12 Khung 0x7fffb8001a10, trong tệp /home/david/coding/python-svn/Lib/test/lock_tests.py, dòng 348, trong f ()
                    cond.wait()
        #16 Frame 0x7fffb8001c40, trong tệp /home/david/coding/python-svn/Lib/test/lock_tests.py, dòng 37, trong task (tid=140737213728528)
                        f()

        Thread 104 (Thread 0x7fffdf5fe710 (LWP 10259)):
        #5 Frame 0x7fffe4001580, trong tệp /home/david/coding/python-svn/Lib/threading.py, dòng 155, trong _acquire_restore (self=<_RLock(_Verbose__verbose=False, _RLock__owner=140737354016512, _RLock__block=<thread.lock at remote 0x858770>, _RLock__count=1) at remote 0xd7ff40>, count_owner=(1, 140736940992272), count=1, owner=140736940992272)
                self.__block.acquire()
        #8 Frame 0x7fffc8002090, trong tệp /home/david/coding/python-svn/Lib/threading.py, dòng 269, trong wait (self=<_Condition(_Condition__lock=<_RLock(_Verbose__verbose=False, _RLock__owner=140737354016512, _RLock__block=<thread.lock at remote 0x858770>, _RLock__count=1) at remote 0xd7ff40>, acquire=<instancemethod at remote 0xd80260>, _is_owned=<instancemethod at remote 0xd80160>, _release_save=<instancemethod at remote 0xd803e0>, release=<instancemethod at remote 0xd802e0>, _acquire_restore=<instancemethod at remote 0xd7ee60>, _Verbose__verbose=False, _Condition__waiters=[]) at remote 0xd7fd10>, timeout=None, waiter=<thread.lock at remote 0x858860>, saved_state=(1, 140736940992272))
                    self._acquire_restore(saved_state)
        #12 Frame 0x7fffac001c90, trong tệp /home/david/coding/python-svn/Lib/test/lock_tests.py, dòng 348, trong f ()
                    cond.wait()
        #16 Frame 0x7fffac0011c0, trong tệp /home/david/coding/python-svn/Lib/test/lock_tests.py, dòng 37, trong task (tid=140736940992272)
                        f()

        Thread 1 (Thread 0x7ffff7fe2700 (LWP 10145)):
        #5 Frame 0xcb5380, trong tệp /home/david/coding/python-svn/Lib/test/lock_tests.py, dòng 16, trong _wait ()
            time.sleep(0.01)
        #8 Frame 0x7fffd00024a0, trong tệp /home/david/coding/python-svn/Lib/test/lock_tests.py, dòng 378, trong _check_notify (self=<ConditionTests(_testMethodName='test_notify', _resultForDoCleanups=<TestResult(_original_stdout=<cStringIO.StringO at remote 0xc191e0>, skipped=[], _mirrorOutput=False, testsRun=39, buffer=False, _original_stderr=<file at remote 0x7ffff7fc6340>, _stdout_buffer=<cStringIO.StringO at remote 0xc9c7f8>, _stderr_buffer=<cStringIO.StringO at remote 0xc9c790>, _moduleSetUpFailed=False, expectedFailures=[], errors=[], _previousTestClass=<type at remote 0x928310>, unexpectedSuccesses=[], failures=[], shouldStop=False, failfast=False) at remote 0xc185a0>, _threads=(0,), _cleanups=[], _type_equality_funcs={<type at remote 0x7eba00>: <instancemethod at remote 0xd750e0>, <type at remote 0x7e7820>: <instancemethod at remote 0xd75160>, <type at remote 0x7e30e0>: <instancemethod at remote 0xd75060>, <type at remote 0x7e7d20>: <instancemethod at remote 0xd751e0>, <type at remote 0x7f19e0...(đã rút gọn)
                _wait()

.. _`devguide`: https://devguide.python.org
.. _`Python wiki`: https://wiki.python.org/moin/DebuggingWithGdb
