.. _profile:

************************************
Các trình phân tích hiệu năng Python
************************************

**Mã nguồn:** :source:`Lib/profile.py` và :source:`Lib/pstats.py`

--------------

.. _profiler-introduction:

Giới thiệu về các trình phân tích hiệu năng
===========================================

.. index::
   single: deterministic profiling
   single: profiling, deterministic

:mod:`cProfile` và :mod:`profile` cung cấp khả năng :dfn:`phân tích hiệu năng xác định` cho các chương trình Python. Một :dfn:`bản phân tích hiệu năng` là một tập hợp các số liệu thống kê mô tả tần suất và khoảng thời gian thực thi của các phần khác nhau trong chương trình. Các số liệu thống kê này có thể được định dạng thành báo cáo thông qua mô-đun :mod:`pstats`.

Thư viện chuẩn Python cung cấp hai cách triển khai khác nhau của cùng một giao diện phân tích hiệu năng:

1. :mod:`cProfile` được khuyến nghị cho hầu hết người dùng; đây là một phần mở rộng C có mức overhead hợp lý, phù hợp để phân tích hiệu năng các chương trình chạy trong thời gian dài. Dựa trên :mod:`lsprof`, do Brett Rosen và Ted Czotter đóng góp.

2. :mod:`profile`, một mô-đun Python thuần túy có giao diện được mô phỏng bởi
   :mod:`cProfile`, nhưng module này làm tăng đáng kể overhead cho các chương trình được profile. Nếu bạn đang cố gắng mở rộng profiler theo một cách nào đó, công việc có thể dễ dàng hơn với module này. Ban đầu được Jim Roskind thiết kế và viết.

.. note::

   Các module profiler được thiết kế để cung cấp profile thực thi cho một chương trình cụ thể, không nhằm mục đích benchmark (với mục đích đó, có :mod:`timeit` để cho kết quả tương đối chính xác). Điều này đặc biệt áp dụng khi benchmark mã Python với mã C: profiler tạo overhead cho mã Python nhưng không tạo overhead cho các hàm ở cấp C, vì vậy mã C có vẻ nhanh hơn bất kỳ mã Python nào.


.. _profile-instant:

Hướng dẫn sử dụng nhanh
=======================

Phần này dành cho những người dùng "không muốn đọc hướng dẫn sử dụng". Phần này cung cấp cái nhìn tổng quan rất ngắn gọn và cho phép người dùng nhanh chóng thực hiện profiling trên một ứng dụng hiện có.

Để profile một hàm nhận một đối số, bạn có thể thực hiện như sau::

   import cProfile
   import re
   cProfile.run('re.compile("foo|bar")')

(Sử dụng :mod:`profile` thay cho :mod:`cProfile` nếu thành phần sau không khả dụng trên hệ thống của bạn.)

Thao tác trên sẽ chạy :func:`re.compile` và in ra kết quả profile như sau::

         214 function calls (207 primitive calls) in 0.002 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.002    0.002 {built-in method builtins.exec}
        1    0.000    0.000    0.001    0.001 <string>:1(<module>)
        1    0.000    0.000    0.001    0.001 __init__.py:250(compile)
        1    0.000    0.000    0.001    0.001 __init__.py:289(_compile)
        1    0.000    0.000    0.000    0.000 _compiler.py:759(compile)
        1    0.000    0.000    0.000    0.000 _parser.py:937(parse)
        1    0.000    0.000    0.000    0.000 _compiler.py:598(_code)
        1    0.000    0.000    0.000    0.000 _parser.py:435(_parse_sub)

Dòng đầu tiên cho biết 214 lần gọi đã được giám sát. Trong số đó, 207 lần gọi là :dfn:`nguyên thủy`, nghĩa là lần gọi đó không được tạo ra thông qua đệ quy. Dòng tiếp theo: ``Ordered by: cumulative time`` cho biết đầu ra được sắp xếp theo các giá trị ``cumtime``. Tiêu đề các cột bao gồm:

ncalls
   cho số lần gọi.

tottime
   cho tổng thời gian dành cho hàm đã cho (không tính thời gian thực hiện các lệnh gọi đến những hàm con)

percall
   là thương của ``tottime`` chia cho ``ncalls``

cumtime
   là tổng thời gian đã dành cho hàm này và tất cả các hàm con (từ khi được gọi cho đến khi thoát). Giá trị này chính xác *ngay cả* đối với các hàm đệ quy.

percall
   là thương của ``cumtime`` chia cho số lần gọi nguyên thủy

filename:lineno(function)
   cung cấp dữ liệu tương ứng của từng hàm

Khi có hai số trong cột đầu tiên (ví dụ ``3/1``), điều đó có nghĩa là hàm đã đệ quy. Giá trị thứ hai là số lần gọi nguyên thủy, còn giá trị thứ nhất là tổng số lần gọi. Lưu ý rằng khi hàm không đệ quy, hai giá trị này giống nhau và chỉ một giá trị duy nhất được in ra.

Thay vì in kết quả ở cuối lần chạy profiling, bạn có thể lưu kết quả vào một tệp bằng cách chỉ định tên tệp cho hàm :func:`run`::

   import cProfile
   import re
   cProfile.run('re.compile("foo|bar")', 'restats')

Lớp :class:`pstats.Stats` đọc kết quả profiling từ một tệp và định dạng chúng theo nhiều cách khác nhau.

.. _profile-cli:

.. program:: cProfile

Các tệp :mod:`cProfile` và :mod:`profile` cũng có thể được gọi như một script để thực hiện profiling cho một script khác. Ví dụ::

   python -m cProfile [-o output_file] [-s sort_order] (-m module | myscript.py)

.. option:: -o <output_file>

   Ghi kết quả profiling vào một tệp thay vì stdout.

.. option:: -s <sort_order>

   Chỉ định một trong các giá trị sắp xếp của :func:`~pstats.Stats.sort_stats` để sắp xếp đầu ra theo đó. Điều này chỉ áp dụng khi không cung cấp :option:`-o <cProfile -o>`.

.. option:: -m <module>

   Chỉ định rằng một module đang được profiling thay vì một script.

   .. versionadded:: 3.7
      Đã thêm tùy chọn ``-m`` vào :mod:`cProfile`.

   .. versionadded:: 3.8
      Đã thêm tùy chọn ``-m`` vào :mod:`profile`.

Lớp :class:`~pstats.Stats` của module :mod:`pstats` có nhiều phương thức để thao tác và in dữ liệu được lưu trong tệp kết quả profile::

   import pstats
   from pstats import SortKey
   p = pstats.Stats('restats')
   p.strip_dirs().sort_stats(-1).print_stats()

Phương thức :meth:`~pstats.Stats.strip_dirs` đã loại bỏ phần đường dẫn thừa khỏi tất cả tên module. Phương thức :meth:`~pstats.Stats.sort_stats` đã sắp xếp tất cả các mục theo chuỗi module/line/name tiêu chuẩn được in ra. Phương thức
:meth:`~pstats.Stats.print_stats` đã in ra tất cả thống kê. Bạn có thể thử các lệnh gọi sort sau đây::

   p.sort_stats(SortKey.NAME)
   p.print_stats()

Lệnh gọi đầu tiên sẽ thực sự sắp xếp danh sách theo tên hàm, còn lệnh gọi thứ hai sẽ in ra các thống kê. Sau đây là một số lệnh gọi thú vị để bạn thử nghiệm::

   p.sort_stats(SortKey.CUMULATIVE).print_stats(10)

Lệnh này sắp xếp profile theo thời gian tích lũy trong một hàm, sau đó chỉ in mười dòng quan trọng nhất. Nếu bạn muốn hiểu những thuật toán nào đang tốn thời gian, bạn sẽ sử dụng dòng trên.

Nếu bạn muốn xem những hàm nào đang lặp nhiều và tốn nhiều thời gian, bạn sẽ thực hiện::

   p.sort_stats(SortKey.TIME).print_stats(10)

để sắp xếp theo thời gian dành cho mỗi hàm, sau đó in thống kê của mười hàm đứng đầu.

Bạn cũng có thể thử::

   p.sort_stats(SortKey.FILENAME).print_stats('__init__')

Lệnh này sẽ sắp xếp tất cả thống kê theo tên tệp, sau đó chỉ in thống kê của các phương thức khởi tạo của lớp (vì tên của chúng có ``__init__``). Cuối cùng, bạn có thể thử::

   p.sort_stats(SortKey.TIME, SortKey.CUMULATIVE).print_stats(.5, 'init')

Dòng lệnh này sắp xếp thống kê với khóa chính là thời gian và khóa phụ là thời gian tích lũy, sau đó in ra một phần thống kê. Cụ thể, trước tiên danh sách được rút gọn xuống còn 50% (liên quan đến ``.5``) kích thước ban đầu, rồi chỉ giữ lại các dòng chứa ``init``, và in danh sách con đó.

Nếu bạn muốn biết những hàm nào đã gọi các hàm trên, giờ đây bạn có thể thực hiện (``p`` vẫn được sắp xếp theo tiêu chí trước đó)::

   p.print_callers(.5, 'init')

và bạn sẽ nhận được danh sách các hàm gọi cho từng hàm được liệt kê.

Nếu muốn có thêm chức năng, bạn sẽ phải đọc hướng dẫn sử dụng hoặc đoán xem các hàm sau đây thực hiện điều gì::

   p.print_callees()
   p.add('restats')

Khi được gọi như một script, module :mod:`pstats` là một trình duyệt thống kê dùng để đọc và kiểm tra các bản dump profile. Module này có giao diện đơn giản theo từng dòng (được triển khai bằng :mod:`cmd`) và trợ giúp tương tác.

Tham chiếu module :mod:`profile` và :mod:`!cProfile`
====================================================

.. module:: cProfile
.. module:: profile
   :synopsis: Trình profiler mã nguồn Python.

Cả hai module :mod:`profile` và :mod:`!cProfile` đều cung cấp các hàm sau:

.. function:: run(command, filename=None, sort=-1)

   Hàm này nhận một đối số duy nhất có thể được truyền cho hàm :func:`exec`, cùng với một tên tệp tùy chọn. Trong mọi trường hợp, thủ tục này thực thi::

      exec(command, __main__.__dict__, __main__.__dict__)

   và thu thập các thống kê profiling từ quá trình thực thi. Nếu không có tên tệp, hàm này sẽ tự động tạo một instance :class:`~pstats.Stats` và in một báo cáo profiling đơn giản. Nếu giá trị sort được chỉ định, giá trị đó sẽ được truyền cho instance :class:`~pstats.Stats` này để kiểm soát cách sắp xếp kết quả.

.. function:: runctx(command, globals, locals, filename=None, sort=-1)

   Hàm này tương tự như :func:`run`, với các đối số bổ sung để cung cấp các ánh xạ globals và locals cho chuỗi *command*. Thủ tục này thực thi::

      exec(command, globals, locals)

   và thu thập các số liệu thống kê profiling như trong hàm :func:`run` ở trên.

.. class:: Profile(timer=None, timeunit=0.0, subcalls=True, builtins=True)

   Lớp này thường chỉ được sử dụng khi cần kiểm soát profiling chính xác hơn so với khả năng mà hàm :func:`cProfile.run` cung cấp.

   Có thể cung cấp một timer tùy chỉnh để đo thời gian chạy của mã thông qua đối số *timer*. Đây phải là một hàm trả về một số duy nhất biểu thị thời gian hiện tại. Nếu số đó là một số nguyên, *timeunit* chỉ định một hệ số nhân xác định thời lượng của mỗi đơn vị thời gian. Ví dụ, nếu timer trả về thời gian được đo bằng hàng nghìn giây, đơn vị thời gian sẽ là ``.001``.

   Việc sử dụng trực tiếp lớp :class:`Profile` cho phép định dạng kết quả profile mà không cần ghi dữ liệu profile vào tệp::

      import cProfile, pstats, io
      from pstats import SortKey
      pr = cProfile.Profile()
      pr.enable()
      # ... do something ...
      pr.disable()
      s = io.StringIO()
      sortby = SortKey.CUMULATIVE
      ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
      ps.print_stats()
      print(s.getvalue())

   Lớp :class:`Profile` cũng có thể được sử dụng như một context manager (chỉ được hỗ trợ trong module :mod:`!cProfile`. xem :ref:`typecontextmanager`)՝::

      import cProfile

      with cProfile.Profile() as pr:
          # ... do something ...

          pr.print_stats()

   .. versionchanged:: 3.8
      Đã bổ sung hỗ trợ context manager.

   .. method:: enable()

      Bắt đầu thu thập dữ liệu profiling. Chỉ có trong :mod:`!cProfile`.

   .. method:: disable()

      Dừng thu thập dữ liệu profiling. Chỉ có trong :mod:`!cProfile`.

   .. method:: create_stats()

      Dừng thu thập dữ liệu profiling và ghi lại kết quả nội bộ dưới dạng profile hiện tại.

   .. method:: print_stats(sort=-1)

      Tạo một đối tượng :class:`~pstats.Stats` dựa trên profile hiện tại và in kết quả ra stdout.

      Tham số *sort* chỉ định thứ tự sắp xếp của các thống kê được hiển thị. Tham số này chấp nhận một khóa duy nhất hoặc một tuple gồm các khóa để bật tính năng sắp xếp nhiều cấp, như trong :func:`Stats.sort_stats <pstats.Stats.sort_stats>`.

      .. versionadded:: 3.13
         :meth:`~Profile.print_stats` now accepts a tuple of keys.

   .. method:: dump_stats(filename)

      Ghi kết quả của profile hiện tại vào *filename*.

   .. method:: run(cmd)

      Lập hồ sơ cmd bằng :func:`exec`.

   .. method:: runctx(cmd, globals, locals)

      Lập hồ sơ cmd bằng :func:`exec` với môi trường toàn cục và cục bộ được chỉ định.

   .. method:: runcall(func, /, *args, **kwargs)

      Lập hồ sơ ``func(*args, **kwargs)``

Lưu ý rằng việc lập hồ sơ chỉ hoạt động nếu command/function được gọi thực sự trả về. Nếu trình thông dịch bị chấm dứt (ví dụ: thông qua một lệnh gọi :func:`sys.exit` trong quá trình thực thi command/function được gọi), sẽ không có kết quả lập hồ sơ nào được in ra.

.. _profile-stats:

Lớp :class:`Stats`
==================

Việc phân tích dữ liệu của profiler được thực hiện bằng lớp :class:`~pstats.Stats`.

.. module:: pstats
   :synopsis: Đối tượng thống kê để sử dụng với profiler.

.. class:: Stats(*filenames or profile, stream=sys.stdout)

   Constructor của lớp này tạo một instance của "đối tượng statistics" từ *filename* (hoặc danh sách tên tệp) hoặc từ một instance :class:`Profile`. Kết quả sẽ được in ra stream được chỉ định bởi *stream*.

   Tệp được chọn bởi constructor ở trên phải được tạo bởi phiên bản tương ứng của :mod:`profile` hoặc :mod:`cProfile`. Cụ thể, không có *no* khả năng tương thích tệp nào được đảm bảo với các phiên bản tương lai của profiler này, và cũng không có khả năng tương thích với các tệp do profiler khác tạo ra hoặc do cùng profiler chạy trên một hệ điều hành khác tạo ra. Nếu cung cấp nhiều tệp, tất cả statistics của các function giống nhau sẽ được gộp lại, để có thể xem xét tổng thể nhiều process trong một report. Nếu cần kết hợp các tệp bổ sung với dữ liệu trong một đối tượng :class:`~pstats.Stats` hiện có, có thể sử dụng method :meth:`~pstats.Stats.add`.

   Thay vì đọc dữ liệu profile từ một tệp, có thể sử dụng một đối tượng :class:`cProfile.Profile` hoặc :class:`profile.Profile` làm nguồn dữ liệu profile.

   Các đối tượng :class:`Stats` có những method sau:

   .. method:: strip_dirs()

      Method này của lớp :class:`Stats` loại bỏ toàn bộ thông tin đường dẫn ở đầu tên tệp. Method này rất hữu ích để giảm kích thước kết quả in ra sao cho vừa trong khoảng (gần) 80 cột. Method này sửa đổi đối tượng và thông tin đã loại bỏ sẽ bị mất. Sau khi thực hiện thao tác loại bỏ, đối tượng được xem là có các entry theo thứ tự "ngẫu nhiên", giống như ngay sau khi khởi tạo và tải đối tượng. Nếu :meth:`~pstats.Stats.strip_dirs` khiến hai tên function không thể phân biệt được (chúng nằm trên cùng một dòng của cùng một tên tệp và có cùng tên function), statistics của hai entry này sẽ được cộng dồn thành một entry duy nhất.


   .. method:: add(*filenames)

      Method này của lớp :class:`Stats` cộng dồn thêm thông tin profiling vào đối tượng profiling hiện tại. Các đối số của method phải tham chiếu đến những tên tệp được tạo bởi phiên bản tương ứng của :func:`profile.run` hoặc :func:`cProfile.run`. Statistics của các function có tên giống hệt nhau (xét theo tệp, dòng, tên) sẽ tự động được cộng dồn thành statistics của một function duy nhất.


   .. method:: dump_stats(filename)

      Lưu dữ liệu đã tải vào đối tượng :class:`Stats` vào tệp có tên *filename*. Tệp sẽ được tạo nếu chưa tồn tại và bị ghi đè nếu đã tồn tại. Điều này tương đương với method cùng tên trên các lớp :class:`profile.Profile` và :class:`cProfile.Profile`.


   .. method:: sort_stats(*keys)

      Phương thức này sửa đổi đối tượng :class:`Stats` bằng cách sắp xếp đối tượng đó theo các tiêu chí được cung cấp. Đối số có thể là một chuỗi hoặc một enum SortKey xác định cơ sở sắp xếp (ví dụ: ``'time'``, ``'name'``, ``SortKey.TIME`` hoặc ``SortKey.NAME``). Đối số enum SortKey có ưu điểm hơn đối số chuỗi vì mạnh mẽ hơn và ít dễ gây lỗi hơn.

      Khi có nhiều khóa được cung cấp, các khóa bổ sung sẽ được dùng làm tiêu chí phụ khi tất cả các khóa được chọn trước đó đều có giá trị bằng nhau. Ví dụ: ``sort_stats(SortKey.NAME, SortKey.FILE)`` sẽ sắp xếp tất cả các mục theo tên hàm, rồi phân giải các trường hợp hòa (tên hàm giống nhau) bằng cách sắp xếp theo tên tệp.

      Đối với đối số chuỗi, có thể sử dụng dạng viết tắt cho bất kỳ tên khóa nào, miễn là dạng viết tắt đó không gây mơ hồ.

      Sau đây là các chuỗi và SortKey hợp lệ:

      +---------------------+--------------------+----------------------+
      | Đối số chuỗi hợp lệ | Đối số enum hợp lệ | Ý nghĩa              |
      +=====================+====================+======================+
      | ``'calls'``         | SortKey.CALLS      | số lần gọi           |
      +---------------------+--------------------+----------------------+
      | ``'cumulative'``    | SortKey.CUMULATIVE | thời gian tích lũy   |
      +---------------------+--------------------+----------------------+
      | ``'cumtime'``       | N/A                | thời gian tích lũy   |
      +---------------------+--------------------+----------------------+
      | ``'file'``          | N/A                | tên tệp              |
      +---------------------+--------------------+----------------------+
      | ``'filename'``      | SortKey.FILENAME   | tên tệp              |
      +---------------------+--------------------+----------------------+
      | ``'module'``        | N/A                | tên tệp              |
      +---------------------+--------------------+----------------------+
      | ``'ncalls'``        | N/A                | số lần gọi           |
      +---------------------+--------------------+----------------------+
      | ``'pcalls'``        | SortKey.PCALLS     | số lần gọi primitive |
      +---------------------+--------------------+----------------------+
      | ``'line'``          | SortKey.LINE       | số dòng              |
      +---------------------+--------------------+----------------------+
      | ``'name'``          | SortKey.NAME       | tên hàm              |
      +---------------------+--------------------+----------------------+
      | ``'nfl'``           | SortKey.NFL        | name/file/line       |
      +---------------------+--------------------+----------------------+
      | ``'stdname'``       | SortKey.STDNAME    | tên chuẩn            |
      +---------------------+--------------------+----------------------+
      | ``'time'``          | SortKey.TIME       | thời gian nội bộ     |
      +---------------------+--------------------+----------------------+
      | ``'tottime'``       | N/A                | thời gian nội bộ     |
      +---------------------+--------------------+----------------------+

      Lưu ý rằng mọi phép sắp xếp theo thống kê đều theo thứ tự giảm dần (đặt các mục tốn nhiều thời gian nhất lên trước), trong khi các phép tìm kiếm theo tên, tệp và số dòng lại theo thứ tự tăng dần (theo bảng chữ cái). Điểm khác biệt tinh tế giữa ``SortKey.NFL`` và ``SortKey.STDNAME`` là tên chuẩn là phép sắp xếp tên theo cách được in ra, nghĩa là các số dòng nằm trong đó được so sánh theo một cách khá bất thường. Ví dụ, các dòng 3, 20 và 40 sẽ (nếu tên tệp giống nhau) xuất hiện theo thứ tự chuỗi là 20, 3 và 40. Ngược lại, ``SortKey.NFL`` thực hiện so sánh số đối với các số dòng. Thực tế, ``sort_stats(SortKey.NFL)`` giống với ``sort_stats(SortKey.NAME, SortKey.FILENAME, SortKey.LINE)``.

      Vì lý do tương thích ngược, các đối số số ``-1``, ``0``, ``1`` và ``2`` được cho phép. Chúng lần lượt được diễn giải thành ``'stdname'``, ``'calls'``, ``'time'`` và ``'cumulative'``. Nếu sử dụng định dạng kiểu cũ này (dạng số), chỉ một khóa sắp xếp (khóa dạng số) sẽ được sử dụng, còn các đối số bổ sung sẽ bị bỏ qua một cách im lặng.

      .. For compatibility with the old profiler.

      .. versionadded:: 3.7
         Đã thêm enum SortKey.

   .. method:: reverse_order()

      Phương thức này dành cho lớp :class:`Stats` sẽ đảo ngược thứ tự của danh sách cơ bản bên trong đối tượng. Lưu ý rằng theo mặc định, thứ tự tăng dần hay giảm dần được chọn chính xác dựa trên khóa sắp xếp được chọn.

      .. This method is provided primarily for compatibility with the old
         profiler.


   .. method:: print_stats(*restrictions)

      Phương thức này dành cho lớp :class:`Stats` sẽ in ra một báo cáo như được mô tả trong định nghĩa :func:`profile.run`.

      Thứ tự in ra dựa trên lần cuối
      thực hiện thao tác :meth:`~pstats.Stats.sort_stats` trên đối tượng (tuân theo các lưu ý trong :meth:`~pstats.Stats.add` và
      :meth:`~pstats.Stats.strip_dirs`).

      Các đối số được cung cấp (nếu có) có thể được dùng để giới hạn danh sách chỉ còn các mục đáng chú ý. Ban đầu, danh sách được xem là toàn bộ tập hợp các hàm đã được lập hồ sơ. Mỗi điều kiện giới hạn либо là một số nguyên (để chọn số dòng), либо là một phân số thập phân trong khoảng từ 0.0 đến 1.0 (bao gồm cả hai đầu mút) (để chọn phần trăm số dòng), либо là một chuỗi được diễn giải như một biểu thức chính quy (để khớp mẫu với tên chuẩn được in ra). Nếu cung cấp nhiều điều kiện giới hạn, chúng sẽ được áp dụng tuần tự. Ví dụ::

         print_stats(.1, 'foo:')

      sẽ trước tiên giới hạn việc in ra 10% đầu tiên của danh sách, sau đó chỉ in các hàm thuộc tệp :file:`.\*foo:`. Ngược lại, lệnh::

         print_stats('foo:', .1)

      sẽ giới hạn danh sách còn tất cả các hàm có tên tệp là :file:`.\*foo:`, sau đó chỉ in 10% đầu tiên trong số đó.


   .. method:: print_callers(*restrictions)

      Phương thức này của lớp :class:`Stats` in ra danh sách tất cả các hàm đã gọi từng hàm trong cơ sở dữ liệu được lập hồ sơ. Thứ tự giống hệt thứ tự do :meth:`~pstats.Stats.print_stats` cung cấp và định nghĩa của đối số giới hạn cũng giống hệt. Mỗi caller được báo cáo trên một dòng riêng. Định dạng hơi khác nhau tùy theo profiler đã tạo ra các thống kê:

      * Với :mod:`profile`, một số được hiển thị trong dấu ngoặc đơn sau mỗi caller để cho biết số lần thực hiện lệnh gọi cụ thể này. Để thuận tiện, một số thứ hai không nằm trong dấu ngoặc đơn lặp lại thời gian tích lũy đã dành cho hàm ở bên phải.

      * Với :mod:`cProfile`, trước mỗi caller là ba số: số lần thực hiện lệnh gọi cụ thể này, cùng với thời gian tổng và thời gian tích lũy đã dành cho hàm hiện tại trong khi hàm này được caller cụ thể đó gọi.


   .. method:: print_callees(*restrictions)

      Phương thức này của lớp :class:`Stats` in ra danh sách tất cả các hàm được gọi bởi hàm được chỉ định. Ngoài việc đảo ngược hướng của các lệnh gọi (về việc được gọi so với được hàm nào đó gọi), các đối số và thứ tự giống hệt phương thức :meth:`~pstats.Stats.print_callers`.


   .. method:: get_stats_profile()

      Phương thức này trả về một thực thể StatsProfile, chứa ánh xạ từ tên hàm đến các thực thể FunctionProfile. Mỗi thực thể FunctionProfile lưu giữ thông tin liên quan đến profile của hàm, chẳng hạn như thời gian hàm chạy, số lần hàm được gọi, v.v...

      .. versionadded:: 3.9
         Đã thêm các dataclass sau: StatsProfile, FunctionProfile. Đã thêm hàm sau: get_stats_profile.

.. _deterministic-profiling:

Profiling xác định là gì?
=========================

:dfn:`Profiling xác định` nhằm phản ánh thực tế rằng mọi sự kiện *lời gọi hàm*, *hàm trả về* và *ngoại lệ* đều được giám sát, đồng thời thời gian chính xác được đo cho các khoảng giữa những sự kiện này (trong thời gian đó mã của người dùng đang được thực thi). Ngược lại, :dfn:`profiling thống kê` (không được thực hiện bởi module này) lấy mẫu ngẫu nhiên con trỏ lệnh hiệu dụng và suy ra thời gian đang được tiêu tốn ở đâu. Kỹ thuật sau thường có overhead thấp hơn (vì mã không cần được instrument), nhưng chỉ cung cấp các chỉ dấu tương đối về nơi thời gian đang được tiêu tốn.

Trong Python, vì có một interpreter đang hoạt động trong quá trình thực thi, không cần có mã được instrument để thực hiện profiling xác định. Python tự động cung cấp một :dfn:`hook` (callback tùy chọn) cho mỗi sự kiện. Ngoài ra, bản chất thông dịch của Python có xu hướng tạo thêm nhiều overhead cho quá trình thực thi, nên profiling xác định thường chỉ làm tăng một lượng nhỏ overhead xử lý trong các ứng dụng điển hình. Kết quả là profiling xác định không quá tốn kém, nhưng cung cấp số liệu thống kê thời gian chạy phong phú về quá trình thực thi của chương trình Python.

Số liệu thống kê về số lần gọi có thể được dùng để xác định lỗi trong mã (số lần gọi bất ngờ) và xác định các điểm có khả năng inline expansion (số lần gọi cao). Số liệu thống kê về thời gian nội tại có thể được dùng để xác định các "vòng lặp nóng" cần được tối ưu hóa cẩn thận. Nên dùng số liệu thống kê về thời gian tích lũy để xác định các lỗi ở cấp độ cao trong việc lựa chọn thuật toán. Lưu ý rằng cách profiler này xử lý khác thường thời gian tích lũy cho phép so sánh trực tiếp số liệu thống kê của các triển khai thuật toán đệ quy với các triển khai lặp.


.. _profile-limitations:

Các hạn chế
===========

Một hạn chế liên quan đến độ chính xác của thông tin định thời. Các deterministic profiler có một vấn đề cơ bản liên quan đến độ chính xác. Hạn chế rõ ràng nhất là "đồng hồ" nền chỉ (thông thường) chạy với tốc độ khoảng .001 giây. Vì vậy, không phép đo nào có thể chính xác hơn đồng hồ nền. Nếu thực hiện đủ nhiều phép đo, thì "sai số" sẽ có xu hướng được trung bình hóa. Đáng tiếc là việc loại bỏ sai số đầu tiên này lại tạo ra một nguồn sai số thứ hai.

Vấn đề thứ hai là từ khi một sự kiện được dispatch cho đến khi lời gọi get time của profiler thực sự *lấy* trạng thái của đồng hồ thì "mất một khoảng thời gian". Tương tự, có một độ trễ nhất định khi thoát khỏi event handler của profiler, tính từ lúc nhận được giá trị của đồng hồ (rồi lưu tạm giá trị đó) cho đến khi code của người dùng thực thi trở lại. Do đó, các hàm được gọi nhiều lần hoặc gọi nhiều hàm thường sẽ tích lũy sai số này. Sai số tích lũy theo cách này thường nhỏ hơn độ chính xác của đồng hồ (nhỏ hơn một nhịp đồng hồ), nhưng nó *có thể* tích lũy và trở nên rất đáng kể.

Vấn đề này quan trọng hơn với :mod:`profile` so với thành phần có overhead thấp hơn
:mod:`cProfile`. Vì lý do này, :mod:`profile` cung cấp một cách để tự hiệu chuẩn cho một nền tảng nhất định, nhờ đó sai số này có thể được loại bỏ theo xác suất (trung bình). Sau khi profiler được hiệu chuẩn, nó sẽ chính xác hơn (theo nghĩa bình phương tối thiểu), nhưng đôi khi sẽ tạo ra các số âm (khi số lần gọi đặc biệt thấp và các vị thần xác suất chống lại bạn :-). ) Đừng *lo* lắng trước các số âm trong profile. Chúng *chỉ* xuất hiện nếu bạn đã hiệu chuẩn profiler, và kết quả thực sự tốt hơn so với khi không hiệu chuẩn.


.. _profile-calibration:

Hiệu chuẩn
==========

Profiler của module :mod:`profile` trừ một hằng số khỏi thời gian xử lý mỗi sự kiện để bù cho overhead của việc gọi hàm lấy thời gian và lưu lại kết quả. Theo mặc định, hằng số này là 0. Có thể sử dụng quy trình sau để lấy một hằng số tốt hơn cho một nền tảng nhất định (xem
:ref:`profile-limitations`). ::

   import profile
   pr = profile.Profile()
   for i in range(5):
       print(pr.calibrate(10000))

Phương thức này thực hiện số lần gọi Python được chỉ định bởi đối số, trực tiếp và một lần nữa dưới profiler, đồng thời đo thời gian cho cả hai trường hợp. Sau đó, phương thức tính toán overhead ẩn trên mỗi sự kiện của profiler và trả về giá trị đó dưới dạng float. Ví dụ, trên máy Intel Core i5 1.8Ghz chạy macOS và sử dụng time.process_time() của Python làm bộ định thời, con số kỳ diệu này vào khoảng 4.04e-6.

Mục tiêu của bài tập này là thu được một kết quả tương đối nhất quán. Nếu máy tính của bạn *rất* nhanh hoặc hàm timer của bạn có độ phân giải kém, bạn có thể phải truyền 100000 hoặc thậm chí 1000000 để thu được kết quả nhất quán.

Khi đã có một kết quả nhất quán, bạn có thể sử dụng kết quả đó theo ba cách::

   import profile

   # 1. Áp dụng độ lệch đã tính toán cho tất cả các instance Profile được tạo sau đó.
   profile.Profile.bias = your_computed_bias

   # 2. Áp dụng độ lệch đã tính toán cho một instance Profile cụ thể.
   pr = profile.Profile()
   pr.bias = your_computed_bias

   # 3. Chỉ định độ lệch đã tính toán trong constructor của instance.
   pr = profile.Profile(bias=your_computed_bias)

Nếu có thể lựa chọn, bạn nên chọn một hằng số nhỏ hơn, khi đó kết quả của bạn sẽ "ít thường xuyên hơn" xuất hiện dưới dạng số âm trong thống kê profile.

.. _profile-timers:

Sử dụng timer tùy chỉnh
=======================

Nếu bạn muốn thay đổi cách xác định thời gian hiện tại (chẳng hạn như buộc sử dụng thời gian theo đồng hồ thực hoặc thời gian đã trôi qua của tiến trình), hãy truyền hàm định thời gian bạn muốn vào hàm khởi tạo lớp :class:`Profile`::

    pr = profile.Profile(your_time_func)

Profiler kết quả sau đó sẽ gọi ``your_time_func``. Tùy thuộc vào việc bạn đang sử dụng :class:`profile.Profile` hay :class:`cProfile.Profile`, giá trị trả về của ``your_time_func`` sẽ được diễn giải khác nhau:

:class:`profile.Profile`
   ``your_time_func`` phải trả về một số duy nhất hoặc một danh sách các số có tổng bằng thời gian hiện tại (tương tự giá trị :func:`os.times` trả về). Nếu hàm trả về một số thời gian duy nhất hoặc danh sách các số trả về có độ dài là 2, bạn sẽ nhận được một phiên bản đặc biệt nhanh của routine dispatch.

   Lưu ý rằng bạn nên hiệu chỉnh lớp profiler cho hàm định thời gian mà bạn chọn (xem :ref:`profile-calibration`). Đối với hầu hết máy tính, bộ định thời trả về một giá trị số nguyên đơn sẽ cho kết quả tốt nhất về mức overhead thấp trong quá trình profiling. (:func:`os.times` *khá* tệ, vì nó trả về một tuple gồm các giá trị số thực). Nếu muốn thay thế bằng một bộ định thời tốt hơn theo cách gọn gàng nhất, hãy tạo một lớp dẫn xuất và cố định một phương thức dispatch thay thế xử lý tốt nhất lệnh gọi bộ định thời của bạn, cùng với hằng số hiệu chỉnh phù hợp.

:class:`cProfile.Profile`
   ``your_time_func`` phải trả về một số duy nhất. Nếu trả về các số nguyên, bạn cũng có thể gọi hàm khởi tạo lớp với đối số thứ hai chỉ định thời lượng thực của một đơn vị thời gian. Ví dụ: nếu ``your_integer_time_func`` trả về thời gian được đo bằng phần nghìn giây, bạn sẽ khởi tạo instance :class:`Profile` như sau::

      pr = cProfile.Profile(your_integer_time_func, 0.001)

   Vì lớp :class:`cProfile.Profile` không thể được hiệu chỉnh, các hàm định thời gian tùy chỉnh nên được sử dụng cẩn thận và phải nhanh nhất có thể. Để đạt kết quả tốt nhất với bộ định thời tùy chỉnh, có thể cần hard-code nó trong mã nguồn C của module nội bộ :mod:`!_lsprof`.

Python 3.3 bổ sung một số hàm mới trong :mod:`time`, có thể được dùng để thực hiện các phép đo chính xác về thời gian của tiến trình hoặc thời gian theo đồng hồ thực. Ví dụ, hãy xem
:func:`time.perf_counter`.
