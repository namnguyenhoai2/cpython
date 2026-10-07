.. highlight:: shell-session

.. _instrumentation:

===========================================
Instrument CPython bằng DTrace và SystemTap
===========================================

:author: David Malcolm
:author: Łukasz Langa

DTrace và SystemTap là các công cụ giám sát, mỗi công cụ cung cấp một cách để kiểm tra những gì các tiến trình trên một hệ thống máy tính đang thực hiện. Cả hai đều sử dụng các ngôn ngữ chuyên biệt cho từng miền, cho phép người dùng viết các script để:

- lọc các tiến trình cần được quan sát
- thu thập dữ liệu từ các tiến trình cần quan tâm
- tạo báo cáo về dữ liệu

Kể từ Python 3.6, CPython có thể được xây dựng với các “marker” được nhúng, còn gọi là “probe”, mà một tập lệnh DTrace hoặc SystemTap có thể quan sát, giúp dễ dàng hơn trong việc theo dõi các tiến trình CPython trên hệ thống đang thực hiện những gì.

.. impl-detail::

   Các marker DTrace là chi tiết triển khai của trình thông dịch CPython. Không có bảo đảm nào về khả năng tương thích của probe giữa các phiên bản CPython. Các tập lệnh DTrace có thể ngừng hoạt động hoặc hoạt động không chính xác mà không có cảnh báo khi thay đổi phiên bản CPython.


Bật các marker tĩnh
-------------------

macOS được tích hợp sẵn hỗ trợ cho DTrace. Trên Linux, để xây dựng CPython với các marker được nhúng cho SystemTap, phải cài đặt các công cụ phát triển SystemTap.

Trên một máy Linux, bạn có thể thực hiện việc này bằng::

   $ yum install systemtap-sdt-devel

hoặc::

   $ sudo apt-get install systemtap-sdt-dev


Sau đó, CPython phải được cấu hình với :option:`configured with the --with-dtrace option <--with-dtrace>`:

.. code-block:: none

   checking for --with-dtrace... yes

Trên macOS, bạn có thể liệt kê các probe DTrace hiện có bằng cách chạy một tiến trình Python ở chế độ nền rồi liệt kê tất cả probe do Python provider cung cấp::

   $ python3.6 -q &
   $ sudo dtrace -l -P python$!  # hoặc: dtrace -l -m python3.6

      ID   PROVIDER            MODULE                          FUNCTION NAME
   29564 python18035        python3.6          _PyEval_EvalFrameDefault function-entry
   29565 python18035        python3.6             dtrace_function_entry function-entry
   29566 python18035        python3.6          _PyEval_EvalFrameDefault function-return
   29567 python18035        python3.6            dtrace_function_return function-return
   29568 python18035        python3.6                           collect gc-done
   29569 python18035        python3.6                           collect gc-start
   29570 python18035        python3.6          _PyEval_EvalFrameDefault line
   29571 python18035        python3.6                 maybe_dtrace_line line

Trên Linux, bạn có thể kiểm tra xem các static marker của SystemTap có hiện diện trong binary đã build hay không bằng cách xem nó có chứa section ".note.stapsdt" hay không.

::

   $ readelf -S ./python | grep .note.stapsdt
   [30] .note.stapsdt        NOTE         0000000000000000 00308d78

Nếu bạn đã build Python dưới dạng shared library (với tùy chọn configure :option:`--enable-shared`), thay vào đó bạn cần kiểm tra bên trong shared library. Ví dụ::

   $ readelf -S libpython3.3dm.so.1.0 | grep .note.stapsdt
   [29] .note.stapsdt        NOTE         0000000000000000 00365b68

Các phiên bản readelf đủ mới có thể in metadata::

    $ readelf -n ./python

    Displaying notes found at file offset 0x00000254 with length 0x00000020:
        Owner                 Data size          Description
        GNU                  0x00000010          NT_GNU_ABI_TAG (ABI version tag)
            OS: Linux, ABI: 2.6.32

    Displaying notes found at file offset 0x00000274 with length 0x00000024:
        Owner                 Data size          Description
        GNU                  0x00000014          NT_GNU_BUILD_ID (unique build ID bitstring)
            Build ID: df924a2b08a7e89f6e11251d4602022977af2670

    Displaying notes found at file offset 0x002d6c30 with length 0x00000144:
        Owner                 Data size          Description
        stapsdt              0x00000031          NT_STAPSDT (SystemTap probe descriptors)
            Provider: python
            Name: gc__start
            Location: 0x00000000004371c3, Base: 0x0000000000630ce2, Semaphore: 0x00000000008d6bf6
            Arguments: -4@%ebx
        stapsdt              0x00000030          NT_STAPSDT (SystemTap probe descriptors)
            Provider: python
            Name: gc__done
            Location: 0x00000000004374e1, Base: 0x0000000000630ce2, Semaphore: 0x00000000008d6bf8
            Arguments: -8@%rax
        stapsdt              0x00000045          NT_STAPSDT (SystemTap probe descriptors)
            Provider: python
            Name: function__entry
            Location: 0x000000000053db6c, Base: 0x0000000000630ce2, Semaphore: 0x00000000008d6be8
            Arguments: 8@%rbp 8@%r12 -4@%eax
        stapsdt              0x00000046          NT_STAPSDT (SystemTap probe descriptors)
            Provider: python
            Name: function__return
            Location: 0x000000000053dba8, Base: 0x0000000000630ce2, Semaphore: 0x00000000008d6bea
            Arguments: 8@%rbp 8@%r12 -4@%eax

Metadata ở trên chứa thông tin dành cho SystemTap, mô tả cách nó có thể vá các lệnh machine code được đặt một cách có chủ đích để bật các tracing hook được một script SystemTap sử dụng.


Các probe DTrace tĩnh
---------------------

Bạn có thể sử dụng script DTrace sau để hiển thị hệ phân cấp call/return của một script Python, chỉ trace trong lần gọi một hàm có tên "start". Nói cách khác, các lần gọi hàm trong thời gian import sẽ không được liệt kê:

.. code-block:: none

    self int indent;

    python$target:::function-entry
    /copyinstr(arg1) == "start"/
    {
            self->trace = 1;
    }

    python$target:::function-entry
    /self->trace/
    {
            printf("%d\t%*s:", timestamp, 15, probename);
            printf("%*s", self->indent, "");
            printf("%s:%s:%d\n", basename(copyinstr(arg0)), copyinstr(arg1), arg2);
            self->indent++;
    }

    python$target:::function-return
    /self->trace/
    {
            self->indent--;
            printf("%d\t%*s:", timestamp, 15, probename);
            printf("%*s", self->indent, "");
            printf("%s:%s:%d\n", basename(copyinstr(arg0)), copyinstr(arg1), arg2);
    }

    python$target:::function-return
    /copyinstr(arg1) == "start"/
    {
            self->trace = 0;
    }

Có thể gọi nó như sau::

  $ sudo dtrace -q -s call_stack.d -c "python3.6 script.py"

Kết quả hiển thị như sau:

.. code-block:: none

    156641360502280  function-entry:call_stack.py:start:23
    156641360518804  function-entry: call_stack.py:function_1:1
    156641360532797  function-entry:  call_stack.py:function_3:9
    156641360546807 function-return:  call_stack.py:function_3:10
    156641360563367 function-return: call_stack.py:function_1:2
    156641360578365  function-entry: call_stack.py:function_2:5
    156641360591757  function-entry:  call_stack.py:function_1:1
    156641360605556  function-entry:   call_stack.py:function_3:9
    156641360617482 function-return:   call_stack.py:function_3:10
    156641360629814 function-return:  call_stack.py:function_1:2
    156641360642285 function-return: call_stack.py:function_2:6
    156641360656770  function-entry: call_stack.py:function_3:9
    156641360669707 function-return: call_stack.py:function_3:10
    156641360687853  function-entry: call_stack.py:function_4:13
    156641360700719 function-return: call_stack.py:function_4:14
    156641360719640  function-entry: call_stack.py:function_5:18
    156641360732567 function-return: call_stack.py:function_5:21
    156641360747370 function-return:call_stack.py:start:28


Các marker SystemTap tĩnh
-------------------------

Cách sử dụng tích hợp SystemTap ở mức thấp là sử dụng trực tiếp các marker tĩnh. Cách này yêu cầu bạn chỉ rõ tệp nhị phân chứa chúng.

Ví dụ: bạn có thể sử dụng script SystemTap này để hiển thị hệ phân cấp call/return của một script Python:

.. code-block:: none

   probe process("python").mark("function__entry") {
        filename = user_string($arg1);
        funcname = user_string($arg2);
        lineno = $arg3;

        printf("%s => %s in %s:%d\\n",
               thread_indent(1), funcname, filename, lineno);
   }

   probe process("python").mark("function__return") {
       filename = user_string($arg1);
       funcname = user_string($arg2);
       lineno = $arg3;

       printf("%s <= %s in %s:%d\\n",
              thread_indent(-1), funcname, filename, lineno);
   }

Có thể gọi nó như sau::

   $ stap \
     show-call-hierarchy.stp \
     -c "./python test.py"

Kết quả sẽ có dạng như sau:

.. code-block:: none

   11408 python(8274):        => __contains__ in Lib/_abcoll.py:362
   11414 python(8274):         => __getitem__ in Lib/os.py:425
   11418 python(8274):          => encode in Lib/os.py:490
   11424 python(8274):          <= encode in Lib/os.py:493
   11428 python(8274):         <= __getitem__ in Lib/os.py:426
   11433 python(8274):        <= __contains__ in Lib/_abcoll.py:366

trong đó các cột là:

- thời gian tính bằng microgiây kể từ khi script bắt đầu
- tên của tệp thực thi
- PID của tiến trình

và phần còn lại cho biết thứ bậc gọi/trả về khi script thực thi.

Đối với bản build :option:`--enable-shared` của CPython, các marker nằm trong shared library libpython, và đường dẫn dạng dấu chấm của probe cần phản ánh điều này. Ví dụ, dòng sau trong ví dụ trên:

.. code-block:: none

   probe process("python").mark("function__entry") {

thay vào đó phải là:

.. code-block:: none

   probe process("python").library("libpython3.6dm.so.1.0").mark("function__entry") {

(giả sử là bản dựng :ref:`debug build <debug-build>` của CPython 3.6)


.. _static-markers:

Các static marker hiện có
-------------------------

.. object:: function__entry(str filename, str funcname, int lineno)

   Marker này cho biết quá trình thực thi một hàm Python đã bắt đầu. Nó chỉ được kích hoạt đối với các hàm Python thuần túy (hàm bytecode).

   Tên tệp, tên hàm và số dòng được cung cấp cho tracing script dưới dạng các đối số vị trí, phải được truy cập bằng ``$arg1``, ``$arg2``, ``$arg3``:

       * ``$arg1`` : ``(const char *)`` tên tệp, có thể truy cập bằng ``user_string($arg1)``

       * ``$arg2`` : ``(const char *)`` tên hàm, có thể truy cập bằng ``user_string($arg2)``

       * ``$arg3`` : ``int`` số dòng

.. object:: function__return(str filename, str funcname, int lineno)

   Marker này là điều ngược lại của :c:func:`!function__entry`, cho biết quá trình thực thi một hàm Python đã kết thúc (hoặc thông qua ``return``, hoặc do một exception). Marker này chỉ được kích hoạt đối với các hàm Python thuần (bytecode).

   Các đối số giống như đối với :c:func:`!function__entry`

.. object:: line(str filename, str funcname, int lineno)

   Marker này cho biết một dòng Python sắp được thực thi. Đây là cách tương đương với việc tracing từng dòng bằng một Python profiler. Marker này không được kích hoạt bên trong các hàm C.

   Các đối số giống như đối với :c:func:`!function__entry`.

.. object:: gc__start(int generation)

   Được kích hoạt khi Python interpreter bắt đầu một chu kỳ garbage collection. ``arg0`` là generation cần quét, chẳng hạn như :func:`gc.collect`.

.. object:: gc__done(long collected)

   Được kích hoạt khi Python interpreter hoàn tất một chu kỳ garbage collection. ``arg0`` là số lượng object đã được thu thập.

.. object:: import__find__load__start(str modulename)

   Được kích hoạt trước khi :mod:`importlib` thực hiện các lần thử tìm và tải module. ``arg0`` là tên module.

   .. versionadded:: 3.7

.. object:: import__find__load__done(str modulename, int found)

   Được kích hoạt sau khi hàm find_and_load của :mod:`importlib` được gọi. ``arg0`` là tên module, ``arg1`` cho biết module có được tải thành công hay không.

   .. versionadded:: 3.7


.. object:: audit(str event, void *tuple)

   Được kích hoạt khi :func:`sys.audit` hoặc :c:func:`PySys_Audit` được gọi. ``arg0`` là tên sự kiện dưới dạng chuỗi C, ``arg1`` là con trỏ :c:type:`PyObject` đến một đối tượng tuple.

   .. versionadded:: 3.8


Điểm vào C
^^^^^^^^^^

Để đơn giản hóa việc kích hoạt các marker DTrace, C API của Python cung cấp một số hàm trợ giúp tương ứng với từng marker tĩnh. Trên các bản build Python không bật DTrace, các hàm này không thực hiện thao tác nào.

Nhìn chung, bạn không cần tự gọi các hàm này, vì Python sẽ thực hiện việc đó thay bạn.

.. list-table::
   :widths: 50 25 25
   :header-rows: 1

   * * Hàm C API
     * Nhãn Static
     * Ghi chú
   * * .. c:function:: void PyDTrace_LINE(const char *arg0, const char *arg1, int arg2)
     * :c:func:`!line`
     *
   * * .. c:function:: void PyDTrace_FUNCTION_ENTRY(const char *arg0, const char *arg1, int arg2)
     * :c:func:`!function__entry`
     *
   * * .. c:function:: void PyDTrace_FUNCTION_RETURN(const char *arg0, const char *arg1, int arg2)
     * :c:func:`!function__return`
     *
   * * .. c:function:: void PyDTrace_GC_START(int arg0)
     * :c:func:`!gc__start`
     *
   * * .. c:function:: void PyDTrace_GC_DONE(Py_ssize_t arg0)
     * :c:func:`!gc__done`
     *
   * * .. c:function:: void PyDTrace_INSTANCE_NEW_START(int arg0)
     * :c:func:`!instance__new__start`
     * Không được Python sử dụng
   * * .. c:function:: void PyDTrace_INSTANCE_NEW_DONE(int arg0)
     * :c:func:`!instance__new__done`
     * Không được Python sử dụng
   * * .. c:function:: void PyDTrace_INSTANCE_DELETE_START(int arg0)
     * :c:func:`!instance__delete__start`
     * Không được Python sử dụng
   * * .. c:function:: void PyDTrace_INSTANCE_DELETE_DONE(int arg0)
     * :c:func:`!instance__delete__done`
     * Không được Python sử dụng
   * * .. c:function:: void PyDTrace_IMPORT_FIND_LOAD_START(const char *arg0)
     * :c:func:`!import__find__load__start`
     *
   * * .. c:function:: void PyDTrace_IMPORT_FIND_LOAD_DONE(const char *arg0, int arg1)
     * :c:func:`!import__find__load__done`
     *
   * * .. c:function:: void PyDTrace_AUDIT(const char *arg0, void *arg1)
     * :c:func:`!audit`
     *


Các kiểm tra thăm dò trong C
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. c:function:: int PyDTrace_LINE_ENABLED(void)
.. c:function:: int PyDTrace_FUNCTION_ENTRY_ENABLED(void)
.. c:function:: int PyDTrace_FUNCTION_RETURN_ENABLED(void)
.. c:function:: int PyDTrace_GC_START_ENABLED(void)
.. c:function:: int PyDTrace_GC_DONE_ENABLED(void)
.. c:function:: int PyDTrace_INSTANCE_NEW_START_ENABLED(void)
.. c:function:: int PyDTrace_INSTANCE_NEW_DONE_ENABLED(void)
.. c:function:: int PyDTrace_INSTANCE_DELETE_START_ENABLED(void)
.. c:function:: int PyDTrace_INSTANCE_DELETE_DONE_ENABLED(void)
.. c:function:: int PyDTrace_IMPORT_FIND_LOAD_START_ENABLED(void)
.. c:function:: int PyDTrace_IMPORT_FIND_LOAD_DONE_ENABLED(void)
.. c:function:: int PyDTrace_AUDIT_ENABLED(void)

   Mọi lệnh gọi đến các hàm ``PyDTrace`` phải được bảo vệ bằng một lệnh gọi đến một trong các hàm này. Điều này cho phép Python giảm thiểu ảnh hưởng đến hiệu năng khi tính năng probing bị tắt.

   Trên các bản build không bật DTrace, những hàm này không thực hiện thao tác nào và trả về ``0``.

Tapset của SystemTap
--------------------

Cách sử dụng tích hợp SystemTap ở mức cao hơn là dùng một "tapset": tương đương với một thư viện trong SystemTap, giúp ẩn một số chi tiết cấp thấp hơn của các static marker.

Sau đây là một tệp tapset, dựa trên bản build không dùng shared của CPython:

.. code-block:: none

    /*
       Provide a higher-level wrapping around the function__entry and
       function__return markers:
     \*/
    probe python.function.entry = process("python").mark("function__entry")
    {
        filename = user_string($arg1);
        funcname = user_string($arg2);
        lineno = $arg3;
        frameptr = $arg4
    }
    probe python.function.return = process("python").mark("function__return")
    {
        filename = user_string($arg1);
        funcname = user_string($arg2);
        lineno = $arg3;
        frameptr = $arg4
    }

Nếu tệp này được cài đặt trong thư mục tapset của SystemTap (ví dụ: ``/usr/share/systemtap/tapset``), thì các probepoint bổ sung sau sẽ khả dụng:

.. object:: python.function.entry(str filename, str funcname, int lineno, frameptr)

   Probepoint này cho biết quá trình thực thi một hàm Python đã bắt đầu. Nó chỉ được kích hoạt đối với các hàm thuần Python (bytecode).

.. object:: python.function.return(str filename, str funcname, int lineno, frameptr)

   Điểm probe này là đối ngược của ``python.function.return``, và cho biết quá trình thực thi một hàm Python đã kết thúc (do ``return`` hoặc do một ngoại lệ). Điểm này chỉ được kích hoạt đối với các hàm Python thuần túy (bytecode).


Ví dụ
-----
Script SystemTap này sử dụng tapset ở trên để triển khai rõ ràng hơn ví dụ đã nêu ở trên về việc theo dõi hệ thống phân cấp các lần gọi hàm Python, mà không cần nêu trực tiếp tên các static marker:

.. code-block:: none

    probe python.function.entry
    {
      printf("%s => %s in %s:%d\n",
             thread_indent(1), funcname, filename, lineno);
    }

    probe python.function.return
    {
      printf("%s <= %s in %s:%d\n",
             thread_indent(-1), funcname, filename, lineno);
    }


Script sau đây sử dụng tapset ở trên để cung cấp chế độ xem dạng top về toàn bộ mã CPython đang chạy, hiển thị 20 frame bytecode được vào thường xuyên nhất mỗi giây trên toàn hệ thống:

.. code-block:: none

    global fn_calls;

    probe python.function.entry
    {
        fn_calls[pid(), filename, funcname, lineno] += 1;
    }

    probe timer.ms(1000) {
        printf("\033[2J\033[1;1H") /* clear screen \*/
        printf("%6s %80s %6s %30s %6s\n",
               "PID", "FILENAME", "LINE", "FUNCTION", "CALLS")
        foreach ([pid, filename, funcname, lineno] in fn_calls- limit 20) {
            printf("%6d %80s %6d %30s %6d\n",
                pid, filename, lineno, funcname,
                fn_calls[pid, filename, funcname, lineno]);
        }
        delete fn_calls;
    }

