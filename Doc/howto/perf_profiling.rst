.. highlight:: shell-session

.. _perf_profiling:

=============================================
Hỗ trợ Python cho profiler ``perf`` của Linux
=============================================

:author: Pablo Galindo

`Profiler perf của Linux <https://perf.wiki.kernel.org>`_ là một công cụ rất mạnh, cho phép bạn lập hồ sơ và thu thập thông tin về hiệu năng của ứng dụng. ``perf`` cũng có một hệ sinh thái công cụ rất sôi động hỗ trợ phân tích dữ liệu mà nó tạo ra.

Vấn đề chính khi sử dụng profiler ``perf`` với các ứng dụng Python là ``perf`` chỉ thu thập thông tin về các native symbol, tức là tên của các hàm và thủ tục được viết bằng C. Điều này có nghĩa là tên và tên tệp của các hàm Python trong mã của bạn sẽ không xuất hiện trong đầu ra của ``perf``.

Kể từ Python 3.12, trình thông dịch có thể chạy ở một chế độ đặc biệt, cho phép các hàm Python xuất hiện trong đầu ra của profiler ``perf``. Khi chế độ này được bật, trình thông dịch sẽ chèn một đoạn mã nhỏ được biên dịch ngay trong lúc chạy trước khi thực thi mỗi hàm Python, đồng thời cung cấp cho ``perf`` thông tin về mối quan hệ giữa đoạn mã này và hàm Python tương ứng bằng cách sử dụng
:doc:`tệp perf map <../c-api/perfmaps>`.

.. note::

    Hiện tại, hỗ trợ cho profiler ``perf`` chỉ khả dụng trên Linux với một số kiến trúc được chọn. Hãy kiểm tra đầu ra của bước build ``configure`` hoặc kiểm tra đầu ra của ``python -m sysconfig | grep HAVE_PERF_TRAMPOLINE`` để biết hệ thống của bạn có được hỗ trợ hay không.

Ví dụ: hãy xem xét script sau:

.. code-block:: python

    def foo(n):
        result = 0
        for _ in range(n):
            result += 1
        return result

    def bar(n):
        foo(n)

    def baz(n):
        bar(n)

    if __name__ == "__main__":
        baz(1000000)

Chúng ta có thể chạy ``perf`` để lấy mẫu các dấu vết ngăn xếp CPU ở tần số 9999 hertz::

    $ perf record -F 9999 -g -o perf.data python my_script.py

Sau đó, chúng ta có thể dùng ``perf report`` để phân tích dữ liệu:

.. code-block:: shell-session

    $ perf report --stdio -n -g

    # Children      Self       Samples  Command     Shared Object       Symbol
    # ........  ........  ............  ..........  ..................  ..........................................
    #
        91.08%     0.00%             0  python.exe  python.exe          [.] _start
                |
                ---_start
                |
                    --90.71%--__libc_start_main
                            Py_BytesMain
                            |
                            |--56.88%--pymain_run_python.constprop.0
                            |          |
                            |          |--56.13%--_PyRun_AnyFileObject
                            |          |          _PyRun_SimpleFileObject
                            |          |          |
                            |          |          |--55.02%--run_mod
                            |          |          |          |
                            |          |          |           --54.65%--PyEval_EvalCode
                            |          |          |                     _PyEval_EvalFrameDefault
                            |          |          |                     PyObject_Vectorcall
                            |          |          |                     _PyEval_Vector
                            |          |          |                     _PyEval_EvalFrameDefault
                            |          |          |                     PyObject_Vectorcall
                            |          |          |                     _PyEval_Vector
                            |          |          |                     _PyEval_EvalFrameDefault
                            |          |          |                     PyObject_Vectorcall
                            |          |          |                     _PyEval_Vector
                            |          |          |                     |
                            |          |          |                     |--51.67%--_PyEval_EvalFrameDefault
                            |          |          |                     |          |
                            |          |          |                     |          |--11.52%--_PyLong_Add
                            |          |          |                     |          |          |
                            |          |          |                     |          |          |--2.97%--_PyObject_Malloc
    ...

Như bạn có thể thấy, các hàm Python không xuất hiện trong đầu ra; chỉ ``_PyEval_EvalFrameDefault`` (hàm đánh giá bytecode Python) xuất hiện. Đáng tiếc là điều này không hữu ích lắm, vì tất cả các hàm Python đều sử dụng cùng một hàm C để đánh giá bytecode, nên chúng ta không thể biết hàm Python nào tương ứng với hàm đánh giá bytecode nào.

Thay vào đó, nếu chạy cùng một thử nghiệm với hỗ trợ ``perf`` được bật, chúng ta sẽ nhận được:

.. code-block:: shell-session

    $ perf report --stdio -n -g

    # Children      Self       Samples  Command     Shared Object       Symbol
    # ........  ........  ............  ..........  ..................  .....................................................................
    #
        90.58%     0.36%             1  python.exe  python.exe          [.] _start
                |
                ---_start
                |
                    --89.86%--__libc_start_main
                            Py_BytesMain
                            |
                            |--55.43%--pymain_run_python.constprop.0
                            |          |
                            |          |--54.71%--_PyRun_AnyFileObject
                            |          |          _PyRun_SimpleFileObject
                            |          |          |
                            |          |          |--53.62%--run_mod
                            |          |          |          |
                            |          |          |           --53.26%--PyEval_EvalCode
                            |          |          |                     py::<module>:/src/script.py
                            |          |          |                     _PyEval_EvalFrameDefault
                            |          |          |                     PyObject_Vectorcall
                            |          |          |                     _PyEval_Vector
                            |          |          |                     py::baz:/src/script.py
                            |          |          |                     _PyEval_EvalFrameDefault
                            |          |          |                     PyObject_Vectorcall
                            |          |          |                     _PyEval_Vector
                            |          |          |                     py::bar:/src/script.py
                            |          |          |                     _PyEval_EvalFrameDefault
                            |          |          |                     PyObject_Vectorcall
                            |          |          |                     _PyEval_Vector
                            |          |          |                     py::foo:/src/script.py
                            |          |          |                     |
                            |          |          |                     |--51.81%--_PyEval_EvalFrameDefault
                            |          |          |                     |          |
                            |          |          |                     |          |--13.77%--_PyLong_Add
                            |          |          |                     |          |          |
                            |          |          |                     |          |          |--3.26%--_PyObject_Malloc



Cách bật hỗ trợ profiling ``perf``
----------------------------------

Có thể bật hỗ trợ profiling ``perf`` ngay từ đầu bằng biến môi trường :envvar:`PYTHONPERFSUPPORT` hoặc
tùy chọn :option:`-X perf <-X>`, hoặc một cách động bằng cách sử dụng :func:`sys.activate_stack_trampoline` và
:func:`sys.deactivate_stack_trampoline`.

Các hàm :mod:`!sys` được ưu tiên hơn tùy chọn :option:`!-X`, còn tùy chọn :option:`!-X` được ưu tiên hơn biến môi trường.

Ví dụ, sử dụng biến môi trường::

   $ PYTHONPERFSUPPORT=1 perf record -F 9999 -g -o perf.data python my_script.py
   $ perf report -g -i perf.data

Ví dụ, sử dụng tùy chọn :option:`!-X`::

   $ perf record -F 9999 -g -o perf.data python -X perf my_script.py
   $ perf report -g -i perf.data

Ví dụ, sử dụng các API :mod:`sys` trong tệp :file:`example.py`:

.. code-block:: python

   import sys

   sys.activate_stack_trampoline("perf")
   do_profiled_stuff()
   sys.deactivate_stack_trampoline()

   non_profiled_stuff()

...sau đó::

   $ perf record -F 9999 -g -o perf.data python ./example.py
   $ perf report -g -i perf.data


Cách đạt được kết quả tốt nhất
------------------------------

Để đạt được kết quả tốt nhất, Python nên được biên dịch với ``CFLAGS="-fno-omit-frame-pointer -mno-omit-leaf-frame-pointer"``, vì điều này cho phép các profiler unwind chỉ bằng cách sử dụng frame pointer mà không cần thông tin debug DWARF. Lý do là đoạn mã được chèn vào để hỗ trợ ``perf`` được tạo động, nên không có thông tin debug DWARF.

Bạn có thể kiểm tra xem hệ thống của mình đã được biên dịch với cờ này hay chưa bằng cách chạy::

    $ python -m sysconfig | grep 'no-omit-frame-pointer'

Nếu không thấy kết quả nào, điều đó có nghĩa là interpreter của bạn chưa được biên dịch với frame pointer và do đó có thể không hiển thị được các hàm Python trong kết quả của ``perf``.


Cách làm việc mà không có frame pointer
---------------------------------------

Nếu đang làm việc với một Python interpreter được biên dịch mà không có frame pointer, bạn vẫn có thể sử dụng profiler ``perf``, nhưng overhead sẽ cao hơn một chút vì Python cần tạo thông tin unwind cho mỗi lần gọi hàm Python ngay trong lúc chạy. Ngoài ra, ``perf`` sẽ mất nhiều thời gian hơn để xử lý dữ liệu vì cần sử dụng thông tin debug DWARF để unwind stack, và đây là một quá trình chậm.

Để bật chế độ này, bạn có thể sử dụng biến môi trường
:envvar:`PYTHON_PERF_JIT_SUPPORT` hoặc tùy chọn :option:`-X perf_jit <-X>`, tùy chọn này sẽ bật chế độ JIT cho profiler ``perf``.

.. note::

    Do có một lỗi trong công cụ ``perf``, chỉ những phiên bản ``perf`` cao hơn v6.8 mới hoạt động với chế độ JIT. Bản sửa lỗi cũng đã được backport vào phiên bản v6.7.2 của công cụ.

    Lưu ý rằng khi kiểm tra phiên bản của công cụ ``perf`` (có thể thực hiện bằng cách chạy ``perf version``), bạn phải tính đến việc một số distro thêm các số phiên bản tùy chỉnh, bao gồm cả ký tự ``-``. Điều này có nghĩa là ``perf 6.7-3`` không nhất thiết là ``perf 6.7.3``.

Khi sử dụng chế độ JIT của perf, bạn cần thực hiện thêm một bước trước khi có thể chạy ``perf report``. Bạn cần gọi lệnh ``perf inject`` để chèn thông tin JIT vào tệp ``perf.data``.::

    $ perf record -F 9999 -g -k 1 --call-graph dwarf -o perf.data python -Xperf_jit my_script.py
    $ perf inject -i perf.data --jit --output perf.jit.data
    $ perf report -g -i perf.jit.data

hoặc sử dụng biến môi trường::

    $ PYTHON_PERF_JIT_SUPPORT=1 perf record -F 9999 -g --call-graph dwarf -o perf.data python my_script.py
    $ perf inject -i perf.data --jit --output perf.jit.data
    $ perf report -g -i perf.jit.data

Lệnh ``perf inject --jit`` sẽ đọc ``perf.data``, tự động tìm tệp kết xuất perf mà Python tạo (trong ``/tmp/perf-$PID.dump``), sau đó tạo ``perf.jit.data``, hợp nhất toàn bộ thông tin JIT. Lệnh này cũng sẽ tạo nhiều tệp ``jitted-XXXX-N.so`` trong thư mục hiện tại; đó là các ảnh ELF cho tất cả trampoline JIT được Python tạo ra.

.. warning::
    Khi sử dụng ``--call-graph dwarf``, công cụ ``perf`` sẽ chụp ảnh nhanh stack của tiến trình đang được profile và lưu thông tin vào tệp ``perf.data``. Theo mặc định, kích thước dữ liệu kết xuất stack là 8192 byte, nhưng bạn có thể thay đổi kích thước bằng cách truyền giá trị sau dấu phẩy, như trong ``--call-graph dwarf,16384``.

    Kích thước dữ liệu kết xuất stack rất quan trọng vì nếu quá nhỏ, ``perf`` sẽ không thể unwind stack và đầu ra sẽ không đầy đủ. Mặt khác, nếu quá lớn, ``perf`` sẽ không thể sample tiến trình thường xuyên như mong muốn vì overhead sẽ cao hơn.

    Kích thước stack đặc biệt quan trọng khi profiling mã Python được biên dịch với mức tối ưu hóa thấp (như ``-O0``), vì các bản build này thường có các stack frame lớn hơn. Nếu bạn biên dịch Python với ``-O0`` nhưng không thấy các hàm Python trong đầu ra profiling, hãy thử tăng kích thước stack dump lên 65528 byte (mức tối đa)::

        $ perf record -F 9999 -g -k 1 --call-graph dwarf,65528 -o perf.data python -Xperf_jit my_script.py

    Các cờ biên dịch khác nhau có thể ảnh hưởng đáng kể đến kích thước stack:

    - Các bản build với ``-O0`` thường có stack frame lớn hơn nhiều so với các bản build với ``-O1`` hoặc cao hơn
    - Việc thêm các tùy chọn tối ưu hóa (``-O1``, ``-O2``, v.v.) thường làm giảm kích thước stack
    - Frame pointer (``-fno-omit-frame-pointer``) nhìn chung giúp việc stack unwinding đáng tin cậy hơn

.. _`The Linux perf profiler`: https://perf.wiki.kernel.org
