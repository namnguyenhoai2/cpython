:mod:`!trace` --- Theo dõi hoặc truy vết quá trình thực thi câu lệnh Python
===========================================================================

.. module:: trace
   :synopsis: Theo dõi hoặc truy vết quá trình thực thi câu lệnh Python.

**Mã nguồn:** :source:`Lib/trace.py`

--------------

Mô-đun :mod:`!trace` cho phép bạn truy vết quá trình thực thi chương trình, tạo các danh sách độ bao phủ câu lệnh có chú thích, in ra mối quan hệ giữa hàm gọi và hàm được gọi, cũng như liệt kê các hàm được thực thi trong một lần chạy chương trình. Bạn có thể sử dụng mô-đun này trong một chương trình khác hoặc từ dòng lệnh.

.. seealso::

   `Coverage.py <https://coverage.readthedocs.io/>`_
      Một công cụ đo độ bao phủ phổ biến của bên thứ ba, cung cấp đầu ra HTML cùng các tính năng nâng cao như độ bao phủ nhánh.

.. _trace-cli:

Sử dụng dòng lệnh
-----------------

Mô-đun :mod:`!trace` có thể được gọi từ dòng lệnh. Cách dùng có thể đơn giản như sau::

   python -m trace --count -C . somefile.py ...

Lệnh trên sẽ thực thi :file:`somefile.py` và tạo các danh sách có chú thích của tất cả mô-đun Python được import trong quá trình thực thi vào thư mục hiện tại.

.. program:: trace

.. option:: --help

   Hiển thị thông tin cách dùng rồi thoát.

.. option:: --version

   Hiển thị phiên bản của mô-đun rồi thoát.

.. versionadded:: 3.8
    Đã thêm tùy chọn ``--module`` cho phép chạy một mô-đun thực thi.

Các tùy chọn chính
^^^^^^^^^^^^^^^^^^

Phải chỉ định ít nhất một trong các tùy chọn sau khi gọi
:mod:`!trace`. Tùy chọn :option:`--listfuncs <-l>` loại trừ lẫn nhau với các tùy chọn :option:`--trace <-t>` và :option:`--count <-c>`. Khi
:option:`--listfuncs <-l>` được cung cấp, cả :option:`--count <-c>` lẫn
:option:`--trace <-t>` đều không được chấp nhận, và ngược lại.

.. program:: trace

.. option:: -c, --count

   Tạo một tập hợp các tệp listing có chú thích sau khi chương trình hoàn tất, cho biết mỗi câu lệnh được thực thi bao nhiêu lần. Xem thêm
   :option:`--coverdir <-C>`, :option:`--file <-f>` và
   :option:`--no-report <-R>` bên dưới.

.. option:: -t, --trace

   Hiển thị các dòng khi chúng được thực thi.

.. option:: -l, --listfuncs

   Hiển thị các hàm được thực thi khi chạy chương trình.

.. option:: -r, --report

   Tạo danh sách có chú thích từ một lần chạy chương trình trước đó có sử dụng tùy chọn
   :option:`--count <-c>` và :option:`--file <-f>`. Thao tác này không thực thi bất kỳ mã nào.

.. option:: -T, --trackcalls

   Hiển thị các mối quan hệ gọi được thể hiện khi chạy chương trình.

Tùy chọn bổ trợ
^^^^^^^^^^^^^^^

.. program:: trace

.. option:: -f, --file=<file>

   Tên tệp dùng để cộng dồn số liệu qua nhiều lần tracing. Nên sử dụng cùng với tùy chọn :option:`--count <-c>`.

.. option:: -C, --coverdir=<dir>

   Thư mục lưu các tệp báo cáo. Báo cáo coverage cho ``package.module`` được ghi vào tệp :file:`{dir}/{package}/{module}.cover`.

.. option:: -m, --missing

   Khi tạo các danh sách có chú thích, hãy đánh dấu những dòng chưa được thực thi bằng ``>>>>>>``.

.. option:: -s, --summary

   Khi sử dụng :option:`--count <-c>` hoặc :option:`--report <-r>`, hãy ghi một bản tóm tắt ngắn vào stdout cho mỗi tệp được xử lý.

.. option:: -R, --no-report

   Không tạo các danh sách có chú thích. Điều này hữu ích nếu bạn định chạy nhiều lần với :option:`--count <-c>`, rồi tạo một bộ danh sách có chú thích duy nhất ở cuối.

.. option:: -g, --timing

   Thêm thời gian kể từ khi chương trình khởi động vào đầu mỗi dòng. Chỉ được sử dụng khi tracing.

Bộ lọc
^^^^^^

Các tùy chọn này có thể được lặp lại nhiều lần.

.. program:: trace

.. option:: --ignore-module=<mod>

   Bỏ qua từng tên module được cung cấp và các module con của nó (nếu đó là một package). Đối số có thể là danh sách các tên được phân tách bằng dấu phẩy.

.. option:: --ignore-dir=<dir>

   Bỏ qua tất cả các module và package trong thư mục được chỉ định và các thư mục con. Đối số này có thể là danh sách các thư mục được phân tách bằng :data:`os.pathsep`.

.. _trace-api:

Giao diện lập trình
-------------------

.. class:: Trace(count=1, trace=1, countfuncs=0, countcallers=0, ignoremods=(),\
                 ignoredirs=(), infile=None, outfile=None, timing=False)

   Tạo một đối tượng để trace việc thực thi một câu lệnh hoặc biểu thức. Tất cả tham số đều là tùy chọn. *count* bật chức năng đếm số dòng. *trace* bật chức năng trace việc thực thi từng dòng. *countfuncs* bật chức năng liệt kê các hàm được gọi trong quá trình chạy. *countcallers* bật chức năng theo dõi quan hệ gọi. *ignoremods* là danh sách các module hoặc package cần bỏ qua. *ignoredirs* là danh sách các thư mục có module hoặc package cần được bỏ qua. *infile* là tên tệp dùng để đọc thông tin đếm đã lưu. *outfile* là tên tệp dùng để ghi thông tin đếm đã cập nhật. *timing* bật hiển thị dấu thời gian tính từ khi bắt đầu trace.

   .. method:: run(cmd)

      Thực thi lệnh và thu thập số liệu thống kê từ quá trình thực thi bằng các tham số trace hiện tại. *cmd* phải là một chuỗi hoặc đối tượng mã, phù hợp để truyền vào :func:`exec`.

   .. method:: runctx(cmd, globals=None, locals=None)

      Thực thi lệnh và thu thập số liệu thống kê từ quá trình thực thi bằng các tham số trace hiện tại, trong các môi trường global và local đã xác định. Nếu chưa được xác định, *globals* và *locals* mặc định là các dictionary rỗng.

   .. method:: runfunc(func, /, *args, **kwds)

      Gọi *func* với các đối số đã cho dưới sự điều khiển của đối tượng :class:`Trace`, bằng các tham số trace hiện tại.

   .. method:: results()

      Trả về một đối tượng :class:`CoverageResults` chứa kết quả tích lũy của tất cả các lần gọi trước đó tới ``run``, ``runctx`` và ``runfunc`` cho instance :class:`Trace` đã cho. Không đặt lại các kết quả trace đã tích lũy.

.. class:: CoverageResults

   Một vùng chứa cho các kết quả coverage, được tạo bởi :meth:`Trace.results`. Người dùng không nên trực tiếp tạo đối tượng này.

   .. method:: update(other)

      Gộp dữ liệu từ một đối tượng :class:`CoverageResults` khác.

   .. method:: write_results(show_missing=True, summary=False, coverdir=None,\
                             *, ignore_missing_files=False)

      Ghi các kết quả coverage. Đặt *show_missing* để hiển thị các dòng không có lượt thực thi. Đặt *summary* để đưa bản tóm tắt coverage theo từng module vào đầu ra. *coverdir* chỉ định thư mục mà các tệp kết quả coverage sẽ được xuất vào. Nếu ``None``, kết quả của mỗi tệp nguồn sẽ được đặt trong thư mục của tệp đó.

      Nếu *ignore_missing_files* là ``True``, các số liệu coverage của những tệp không còn tồn tại sẽ được âm thầm bỏ qua. Nếu không, một tệp bị thiếu sẽ gây ra :exc:`FileNotFoundError`.

      .. versionchanged:: 3.13
         Đã thêm tham số *ignore_missing_files*.

Một ví dụ đơn giản minh họa cách sử dụng giao diện lập trình::

   import sys
   import trace

   # tạo một đối tượng Trace, cho biết những gì cần bỏ qua và có thực hiện
   # tracing hoặc đếm dòng, hay thực hiện cả hai hay không.
   tracer = trace.Trace(
       ignoredirs=[sys.prefix, sys.exec_prefix],
       trace=0,
       count=1)

   # chạy lệnh mới bằng tracer đã cho
   tracer.run('main()')

   # tạo báo cáo, đặt đầu ra trong thư mục hiện tại
   r = tracer.results()
   r.write_results(show_missing=True, coverdir=".")

.. _`Coverage.py`: https://coverage.readthedocs.io/
