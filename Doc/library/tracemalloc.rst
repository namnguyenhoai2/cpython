:mod:`!tracemalloc` --- tracemalloc --- Theo dõi các cấp phát bộ nhớ
====================================================================

.. module:: tracemalloc
   :synopsis: Theo dõi các cấp phát bộ nhớ.

.. versionadded:: 3.4

**Mã nguồn:** :source:`Lib/tracemalloc.py`

--------------

Module tracemalloc là một công cụ debug dùng để theo dõi các khối bộ nhớ được Python cấp phát. Module này cung cấp các thông tin sau:

* Traceback tại nơi một đối tượng được cấp phát
* Thống kê về các khối bộ nhớ đã cấp phát theo tên tệp và số dòng: tổng kích thước, số lượng và kích thước trung bình của các khối bộ nhớ đã cấp phát
* Tính toán sự khác biệt giữa hai snapshot để phát hiện memory leak

Để theo dõi hầu hết các khối bộ nhớ được Python cấp phát, mô-đun này nên được khởi động sớm nhất có thể bằng cách đặt biến môi trường :envvar:`PYTHONTRACEMALLOC` thành ``1``, hoặc sử dụng tùy chọn dòng lệnh :option:`-X` ``tracemalloc``. Có thể gọi hàm :func:`tracemalloc.start` trong runtime để bắt đầu theo dõi các lần cấp phát bộ nhớ của Python.

Theo mặc định, một bản theo dõi khối bộ nhớ đã cấp phát chỉ lưu frame gần nhất (1 frame). Để lưu 25 frame khi khởi động: đặt
biến môi trường :envvar:`PYTHONTRACEMALLOC` thành ``25``, hoặc sử dụng
tùy chọn dòng lệnh :option:`-X` ``tracemalloc=25``.


Ví dụ
-----

Hiển thị 10 mục đầu
^^^^^^^^^^^^^^^^^^^

Hiển thị 10 tệp cấp phát nhiều bộ nhớ nhất::

    import tracemalloc

    tracemalloc.start()

    # ... chạy ứng dụng của bạn ...

    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')

    print("[ Top 10 ]")
    for stat in top_stats[:10]:
        print(stat)


Ví dụ về đầu ra của bộ kiểm thử Python::

    [ Top 10 ]
    <frozen importlib._bootstrap>:716: size=4855 KiB, count=39328, average=126 B
    <frozen importlib._bootstrap>:284: size=521 KiB, count=3199, average=167 B
    /usr/lib/python3.4/collections/__init__.py:368: size=244 KiB, count=2315, average=108 B
    /usr/lib/python3.4/unittest/case.py:381: size=185 KiB, count=779, average=243 B
    /usr/lib/python3.4/unittest/case.py:402: size=154 KiB, count=378, average=416 B
    /usr/lib/python3.4/abc.py:133: size=88.7 KiB, count=347, average=262 B
    <frozen importlib._bootstrap>:1446: size=70.4 KiB, count=911, average=79 B
    <frozen importlib._bootstrap>:1454: size=52.0 KiB, count=25, average=2131 B
    <string>:5: size=49.7 KiB, count=148, average=344 B
    /usr/lib/python3.4/sysconfig.py:411: size=48.0 KiB, count=1, average=48.0 KiB

Ta có thể thấy Python đã tải dữ liệu ``4855 KiB`` (bytecode và các hằng số) từ các module, còn module :mod:`collections` đã cấp phát ``244 KiB`` để xây dựng
các kiểu :class:`~collections.namedtuple`.

Xem :meth:`Snapshot.statistics` để biết thêm tùy chọn.


Tính toán các khác biệt
^^^^^^^^^^^^^^^^^^^^^^^

Chụp hai snapshot và hiển thị các khác biệt::

    import tracemalloc
    tracemalloc.start()
    # ... khởi chạy ứng dụng của bạn ...

    snapshot1 = tracemalloc.take_snapshot()
    # ... gọi hàm gây rò rỉ bộ nhớ ...
    snapshot2 = tracemalloc.take_snapshot()

    top_stats = snapshot2.compare_to(snapshot1, 'lineno')

    print("[ Top 10 differences ]")
    for stat in top_stats[:10]:
        print(stat)

Ví dụ về kết quả trước và sau khi chạy một số kiểm thử của bộ kiểm thử Python::

    [ Top 10 differences ]
    <frozen importlib._bootstrap>:716: size=8173 KiB (+4428 KiB), count=71332 (+39369), average=117 B
    /usr/lib/python3.4/linecache.py:127: size=940 KiB (+940 KiB), count=8106 (+8106), average=119 B
    /usr/lib/python3.4/unittest/case.py:571: size=298 KiB (+298 KiB), count=589 (+589), average=519 B
    <frozen importlib._bootstrap>:284: size=1005 KiB (+166 KiB), count=7423 (+1526), average=139 B
    /usr/lib/python3.4/mimetypes.py:217: size=112 KiB (+112 KiB), count=1334 (+1334), average=86 B
    /usr/lib/python3.4/http/server.py:848: size=96.0 KiB (+96.0 KiB), count=1 (+1), average=96.0 KiB
    /usr/lib/python3.4/inspect.py:1465: size=83.5 KiB (+83.5 KiB), count=109 (+109), average=784 B
    /usr/lib/python3.4/unittest/mock.py:491: size=77.7 KiB (+77.7 KiB), count=143 (+143), average=557 B
    /usr/lib/python3.4/urllib/parse.py:476: size=71.8 KiB (+71.8 KiB), count=969 (+969), average=76 B
    /usr/lib/python3.4/contextlib.py:38: size=67.2 KiB (+67.2 KiB), count=126 (+126), average=546 B

Ta có thể thấy Python đã tải ``8173 KiB`` của mô-đun data (bytecode và các hằng số), và lượng này ``4428 KiB`` so với lượng đã được tải trước khi chạy các kiểm thử, khi snapshot trước đó được tạo. Tương tự, mô-đun :mod:`linecache` đã lưu vào bộ nhớ đệm ``940 KiB`` mã nguồn Python để định dạng traceback, tất cả đều xảy ra kể từ snapshot trước đó.

Nếu hệ thống có ít bộ nhớ trống, bạn có thể ghi snapshot vào đĩa bằng phương thức :meth:`Snapshot.dump` để phân tích snapshot ngoại tuyến. Sau đó, hãy sử dụng
phương thức :meth:`Snapshot.load` để tải lại snapshot.


Lấy traceback của một khối bộ nhớ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Mã để hiển thị traceback của khối bộ nhớ lớn nhất::

    import tracemalloc

    # Lưu 25 frame
    tracemalloc.start(25)

    # ... chạy ứng dụng của bạn ...

    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('traceback')

    # chọn khối bộ nhớ lớn nhất
    stat = top_stats[0]
    print("%s memory blocks: %.1f KiB" % (stat.count, stat.size / 1024))
    for line in stat.traceback.format():
        print(line)

Ví dụ về đầu ra của bộ kiểm thử Python (traceback được giới hạn ở 25 frame)::

    903 memory blocks: 870.1 KiB
      File "<frozen importlib._bootstrap>", line 716
      File "<frozen importlib._bootstrap>", line 1036
      File "<frozen importlib._bootstrap>", line 934
      File "<frozen importlib._bootstrap>", line 1068
      File "<frozen importlib._bootstrap>", line 619
      File "<frozen importlib._bootstrap>", line 1581
      File "<frozen importlib._bootstrap>", line 1614
      File "/usr/lib/python3.4/doctest.py", line 101
        import pdb
      File "<frozen importlib._bootstrap>", line 284
      File "<frozen importlib._bootstrap>", line 938
      File "<frozen importlib._bootstrap>", line 1068
      File "<frozen importlib._bootstrap>", line 619
      File "<frozen importlib._bootstrap>", line 1581
      File "<frozen importlib._bootstrap>", line 1614
      File "/usr/lib/python3.4/test/support/__init__.py", line 1728
        import doctest
      File "/usr/lib/python3.4/test/test_pickletools.py", line 21
        support.run_doctest(pickletools)
      File "/usr/lib/python3.4/test/regrtest.py", line 1276
        test_runner()
      File "/usr/lib/python3.4/test/regrtest.py", line 976
        display_failure=not verbose)
      File "/usr/lib/python3.4/test/regrtest.py", line 761
        match_tests=ns.match_tests)
      File "/usr/lib/python3.4/test/regrtest.py", line 1563
        main()
      File "/usr/lib/python3.4/test/__main__.py", line 3
        regrtest.main_in_temp_cwd()
      File "/usr/lib/python3.4/runpy.py", line 73
        exec(code, run_globals)
      File "/usr/lib/python3.4/runpy.py", line 160
        "__main__", fname, loader, pkg_name)

Ta có thể thấy rằng phần lớn bộ nhớ được cấp phát trong module :mod:`importlib` để tải dữ liệu (bytecode và hằng số) từ các module: ``870.1 KiB``. Traceback cho biết nơi :mod:`importlib` tải dữ liệu gần đây nhất: trên dòng ``import pdb`` của module :mod:`doctest`. Traceback có thể thay đổi nếu một module mới được tải.


Top dễ đọc
^^^^^^^^^^

Mã để hiển thị 10 dòng cấp phát nhiều bộ nhớ nhất với đầu ra đẹp mắt, bỏ qua các tệp ``<frozen importlib._bootstrap>`` và ``<unknown>``::

    import linecache
    import os
    import tracemalloc

    def display_top(snapshot, key_type='lineno', limit=10):
        snapshot = snapshot.filter_traces((
            tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
            tracemalloc.Filter(False, "<unknown>"),
        ))
        top_stats = snapshot.statistics(key_type)

        print("Top %s lines" % limit)
        for index, stat in enumerate(top_stats[:limit], 1):
            frame = stat.traceback[0]
            print("#%s: %s:%s: %.1f KiB"
                  % (index, frame.filename, frame.lineno, stat.size / 1024))
            line = linecache.getline(frame.filename, frame.lineno).strip()
            if line:
                print('    %s' % line)

        other = top_stats[limit:]
        if other:
            size = sum(stat.size for stat in other)
            print("%s other: %.1f KiB" % (len(other), size / 1024))
        total = sum(stat.size for stat in top_stats)
        print("Total allocated size: %.1f KiB" % (total / 1024))

    tracemalloc.start()

    # ... chạy ứng dụng của bạn ...

    snapshot = tracemalloc.take_snapshot()
    display_top(snapshot)

Ví dụ về đầu ra của bộ kiểm thử Python::

    Top 10 lines
    #1: Lib/base64.py:414: 419.8 KiB
        _b85chars2 = [(a + b) for a in _b85chars for b in _b85chars]
    #2: Lib/base64.py:306: 419.8 KiB
        _a85chars2 = [(a + b) for a in _a85chars for b in _a85chars]
    #3: collections/__init__.py:368: 293.6 KiB
        exec(class_definition, namespace)
    #4: Lib/abc.py:133: 115.2 KiB
        cls = super().__new__(mcls, name, bases, namespace)
    #5: unittest/case.py:574: 103.1 KiB
        testMethod()
    #6: Lib/linecache.py:127: 95.4 KiB
        lines = fp.readlines()
    #7: urllib/parse.py:476: 71.8 KiB
        for a in _hexdig for b in _hexdig}
    #8: <string>:5: 62.0 KiB
    #9: Lib/_weakrefset.py:37: 60.0 KiB
        self.data = set()
    #10: Lib/base64.py:142: 59.8 KiB
        _b32tab2 = [a + b for a in _b32tab for b in _b32tab]
    6220 other: 3602.8 KiB
    Total allocated size: 5303.1 KiB

Xem :meth:`Snapshot.statistics` để biết thêm tùy chọn.

Ghi lại kích thước hiện tại và kích thước cực đại của tất cả các khối bộ nhớ được theo dõi
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Đoạn mã sau tính hai tổng như ``0 + 1 + 2 + ...`` một cách không hiệu quả bằng cách tạo một danh sách chứa các số đó. Danh sách này tạm thời chiếm rất nhiều bộ nhớ. Chúng ta có thể sử dụng :func:`get_traced_memory` và :func:`reset_peak` để quan sát mức sử dụng bộ nhớ nhỏ sau khi tính tổng, cũng như mức sử dụng bộ nhớ cực đại trong quá trình tính toán::

  import tracemalloc

  tracemalloc.start()

  # Mã ví dụ: tính một tổng bằng danh sách tạm thời lớn
  large_sum = sum(list(range(100000)))

  first_size, first_peak = tracemalloc.get_traced_memory()

  tracemalloc.reset_peak()

  # Mã ví dụ: tính một tổng bằng danh sách tạm thời nhỏ
  small_sum = sum(list(range(1000)))

  second_size, second_peak = tracemalloc.get_traced_memory()

  print(f"{first_size=}, {first_peak=}")
  print(f"{second_size=}, {second_peak=}")

Kết quả::

  first_size=664, first_peak=3592984
  second_size=804, second_peak=29704

Việc sử dụng :func:`reset_peak` đảm bảo chúng ta có thể ghi lại chính xác mức cực đại trong quá trình tính ``small_sum``, mặc dù mức này nhỏ hơn nhiều so với kích thước cực đại tổng thể của các khối bộ nhớ kể từ lần gọi :func:`start`. Nếu không gọi
:func:`reset_peak`, ``second_peak`` vẫn sẽ là mức cực đại từ phép tính ``large_sum`` (nghĩa là bằng ``first_peak``). Trong trường hợp này, cả hai mức cực đại đều cao hơn nhiều so với mức sử dụng bộ nhớ cuối cùng, cho thấy chúng ta có thể tối ưu hóa (bằng cách loại bỏ lệnh gọi không cần thiết đến :class:`list` và viết ``sum(range(...))``).

API
---

Các hàm
^^^^^^^

.. function:: clear_traces()

   Xóa dấu vết của các khối bộ nhớ được Python cấp phát.

   Xem thêm :func:`stop`.


.. function:: get_object_traceback(obj)

   Lấy traceback tại đó đối tượng Python *obj* được cấp phát. Trả về một thực thể :class:`Traceback`, hoặc ``None`` nếu module :mod:`!tracemalloc` không theo dõi việc cấp phát bộ nhớ hoặc không theo dõi việc cấp phát đối tượng.

   Xem thêm các hàm :func:`gc.get_referrers` và :func:`sys.getsizeof`.


.. function:: get_traceback_limit()

   Lấy số lượng frame tối đa được lưu trong traceback của một trace.

   Mô-đun :mod:`!tracemalloc` phải đang theo dõi việc cấp phát bộ nhớ để lấy giới hạn; nếu không, một ngoại lệ sẽ được đưa ra.

   Giới hạn được thiết lập bởi hàm :func:`start`.


.. function:: get_traced_memory()

   Lấy kích thước hiện tại và kích thước cực đại của các khối bộ nhớ được theo dõi bởi
   mô-đun :mod:`!tracemalloc` dưới dạng tuple: ``(current: int, peak: int)``.


.. function:: reset_peak()

   Đặt kích thước cực đại của các khối bộ nhớ được theo dõi bởi mô-đun :mod:`!tracemalloc` thành kích thước hiện tại.

   Không thực hiện thao tác nào nếu mô-đun :mod:`!tracemalloc` không theo dõi việc cấp phát bộ nhớ.

   Hàm này chỉ sửa đổi kích thước cực đại đã ghi nhận, không sửa đổi hoặc xóa bất kỳ dấu vết nào, không giống như :func:`clear_traces`. Các snapshot được tạo bằng
   :func:`take_snapshot` trước một lần gọi :func:`reset_peak` có thể được so sánh một cách có ý nghĩa với các snapshot được chụp sau lần gọi đó.

   Xem thêm :func:`get_traced_memory`.

   .. versionadded:: 3.9


.. function:: get_tracemalloc_memory()

   Lấy mức sử dụng bộ nhớ tính bằng byte của module :mod:`!tracemalloc` được dùng để lưu trữ các dấu vết của các khối bộ nhớ. Trả về một :class:`int`.


.. function:: is_tracing()

    ``True`` nếu module :mod:`!tracemalloc` đang theo dõi việc cấp phát bộ nhớ Python, nếu không thì ``False``.

    Xem thêm các hàm :func:`start` và :func:`stop`.


.. function:: start(nframe: int=1)

   Bắt đầu theo dõi việc cấp phát bộ nhớ Python: cài đặt các hook trên các bộ cấp phát bộ nhớ Python. Các traceback được thu thập từ các dấu vết sẽ bị giới hạn ở *nframe* frame. Theo mặc định, một dấu vết của một khối bộ nhớ chỉ lưu frame gần nhất: giới hạn là ``1``. *nframe* phải lớn hơn hoặc bằng ``1``.

   Bạn vẫn có thể đọc số frame tổng ban đầu cấu thành traceback bằng cách xem thuộc tính :attr:`Traceback.total_nframe`.

   Việc lưu trữ nhiều hơn ``1`` frame chỉ hữu ích để tính các thống kê được nhóm theo ``'traceback'`` hoặc để tính các thống kê tích lũy: xem
   các phương thức :meth:`Snapshot.compare_to` và :meth:`Snapshot.statistics`.

   Lưu trữ nhiều frame hơn sẽ làm tăng chi phí bộ nhớ và CPU của
   module :mod:`!tracemalloc`. Sử dụng hàm :func:`get_tracemalloc_memory` để đo lượng bộ nhớ được module :mod:`!tracemalloc` sử dụng.

   Có thể sử dụng biến môi trường :envvar:`PYTHONTRACEMALLOC` (``PYTHONTRACEMALLOC=NFRAME``) và tùy chọn dòng lệnh :option:`-X` ``tracemalloc=NFRAME`` để bắt đầu tracing khi khởi động.

   Xem thêm các hàm :func:`stop`, :func:`is_tracing` và :func:`get_traceback_limit`.


.. function:: stop()

   Dừng tracing các cấp phát bộ nhớ Python: gỡ cài đặt các hook trên các bộ cấp phát bộ nhớ Python. Đồng thời xóa tất cả các trace đã thu thập trước đó của những block bộ nhớ được Python cấp phát.

   Gọi hàm :func:`take_snapshot` để chụp ảnh các dấu vết trước khi xóa chúng.

   Xem thêm các hàm :func:`start`, :func:`is_tracing` và :func:`clear_traces`.


.. function:: take_snapshot()

   Chụp ảnh các dấu vết của những khối bộ nhớ được Python cấp phát. Trả về một
   đối tượng :class:`Snapshot` mới.

   Ảnh chụp không bao gồm các khối bộ nhớ được cấp phát trước khi mô-đun
   :mod:`!tracemalloc` bắt đầu theo dõi việc cấp phát bộ nhớ.

   Traceback của các dấu vết được giới hạn ở :func:`get_traceback_limit` frame. Sử dụng tham số *nframe* của hàm :func:`start` để lưu thêm frame.

   Mô-đun :mod:`!tracemalloc` phải đang theo dõi các lần cấp phát bộ nhớ để chụp snapshot; xem hàm :func:`start`.

   Xem thêm hàm :func:`get_object_traceback`.


DomainFilter
^^^^^^^^^^^^

.. class:: DomainFilter(inclusive: bool, domain: int)

   Lọc các trace của khối bộ nhớ theo không gian địa chỉ (domain) của chúng.

   .. versionadded:: 3.6

   .. attribute:: inclusive

      Nếu *inclusive* là ``True`` (bao gồm), khớp với các khối bộ nhớ được cấp phát trong không gian địa chỉ :attr:`domain`.

      Nếu *inclusive* là ``False`` (loại trừ), khớp với các khối bộ nhớ không được cấp phát trong không gian địa chỉ :attr:`domain`.

   .. attribute:: domain

      Không gian địa chỉ của một khối bộ nhớ (``int``). Thuộc tính chỉ đọc.


Bộ lọc
^^^^^^

.. class:: Filter(inclusive: bool, filename_pattern: str, lineno: int=None, all_frames: bool=False, domain: int=None)

   Lọc các trace của các block bộ nhớ.

   Xem hàm :func:`fnmatch.fnmatch` để biết cú pháp của *filename_pattern*. Phần mở rộng tệp ``'.pyc'`` được thay thế bằng ``'.py'``.

   Ví dụ:

   * ``Filter(True, subprocess.__file__)`` chỉ bao gồm các trace của
     :mod:`subprocess` mô-đun
   * ``Filter(False, tracemalloc.__file__)`` loại trừ các trace của
     mô-đun :mod:`!tracemalloc`
   * ``Filter(False, "<unknown>")`` loại trừ các traceback rỗng


   .. versionchanged:: 3.5
      Phần mở rộng tệp ``'.pyo'`` không còn được thay thế bằng ``'.py'``.

   .. versionchanged:: 3.6
      Đã thêm thuộc tính :attr:`domain`.


   .. attribute:: domain

      Không gian địa chỉ của một khối bộ nhớ (``int`` hoặc ``None``).

      tracemalloc sử dụng domain ``0`` để theo dõi các lần cấp phát bộ nhớ do Python thực hiện. Các phần mở rộng C có thể sử dụng các domain khác để theo dõi những tài nguyên khác.

   .. attribute:: inclusive

      Nếu *inclusive* là ``True`` (include), chỉ khớp với các khối bộ nhớ được cấp phát trong một tệp có tên khớp với :attr:`filename_pattern` tại số dòng
      :attr:`lineno`.

      Nếu *inclusive* là ``False`` (loại trừ), bỏ qua các khối bộ nhớ được cấp phát trong tệp có tên khớp với :attr:`filename_pattern` tại số dòng
      :attr:`lineno`.

   .. attribute:: lineno

      Số dòng (``int``) của bộ lọc. Nếu *lineno* là ``None``, bộ lọc khớp với mọi số dòng.

   .. attribute:: filename_pattern

      Mẫu tên tệp của bộ lọc (``str``). Thuộc tính chỉ đọc.

   .. attribute:: all_frames

      Nếu *all_frames* là ``True``, tất cả frame trong traceback đều được kiểm tra. Nếu *all_frames* là ``False``, chỉ frame gần nhất được kiểm tra.

      Thuộc tính này không có tác dụng nếu giới hạn traceback là ``1``. Xem
      hàm :func:`get_traceback_limit` và thuộc tính :attr:`Snapshot.traceback_limit`.


Frame
^^^^^

.. class:: Frame

   Frame của một traceback.

   Lớp :class:`Traceback` là một chuỗi các instance :class:`Frame`.

   .. attribute:: filename

      Tên tệp (``str``).

   .. attribute:: lineno

      Số dòng (``int``).


Snapshot
^^^^^^^^

.. class:: Snapshot

   Snapshot của các dấu vết bộ nhớ do Python cấp phát.

   Hàm :func:`take_snapshot` tạo một instance snapshot.

   .. method:: compare_to(old_snapshot: Snapshot, key_type: str, cumulative: bool=False)

      Tính toán các khác biệt với một snapshot cũ. Nhận thống kê dưới dạng danh sách các đối tượng :class:`StatisticDiff` được sắp xếp và nhóm theo *key_type*.

      Xem phương thức :meth:`Snapshot.statistics` để biết về các tham số *key_type* và *cumulative*.

      Kết quả được sắp xếp từ lớn nhất đến nhỏ nhất theo: giá trị tuyệt đối của :attr:`StatisticDiff.size_diff`, :attr:`StatisticDiff.size`, giá trị tuyệt đối của :attr:`StatisticDiff.count_diff`, :attr:`Statistic.count` và sau đó theo :attr:`StatisticDiff.traceback`.


   .. method:: dump(filename)

      Ghi snapshot vào một tệp.

      Sử dụng :meth:`load` để tải lại snapshot.


   .. method:: filter_traces(filters)

      Tạo một đối tượng :class:`Snapshot` mới với một chuỗi :attr:`traces` đã được lọc, trong đó *filters* là danh sách các :class:`DomainFilter` và
      các đối tượng :class:`Filter`. Nếu *filters* là một danh sách rỗng, trả về một đối tượng mới
      :class:`Snapshot` instance chứa một bản sao của các trace.

      Tất cả các bộ lọc bao gồm được áp dụng cùng lúc; một trace sẽ bị bỏ qua nếu không có bộ lọc bao gồm nào khớp với trace đó. Một trace sẽ bị bỏ qua nếu có ít nhất một bộ lọc loại trừ khớp với trace đó.

      .. versionchanged:: 3.6
         :class:`DomainFilter` instances are now also accepted in *filters*.


   .. classmethod:: load(filename)

      Tải snapshot từ một tệp.

      Xem thêm :meth:`dump`.


   .. method:: statistics(key_type: str, cumulative: bool=False)

      Lấy thống kê dưới dạng danh sách :class:`Statistic` instance được sắp xếp, nhóm theo *key_type*:

      +-----------------+--------------------+
      | key_type        | description        |
      +=================+====================+
      | ``'filename'``  | tên tệp            |
      +-----------------+--------------------+
      | ``'lineno'``    | tên tệp và số dòng |
      +-----------------+--------------------+
      | ``'traceback'`` | traceback          |
      +-----------------+--------------------+

      Nếu *cumulative* là ``True``, hãy cộng dồn kích thước và số lượng các khối bộ nhớ của tất cả các frame trong traceback của một trace, không chỉ frame gần nhất. Chế độ cộng dồn chỉ có thể được sử dụng với *key_type* bằng ``'filename'`` và ``'lineno'``.

      Kết quả được sắp xếp từ lớn nhất đến nhỏ nhất theo:
      :attr:`Statistic.size`, :attr:`Statistic.count` rồi đến
      :attr:`Statistic.traceback`.


   .. attribute:: traceback_limit

      Số frame tối đa được lưu trong traceback của :attr:`traces`: kết quả của :func:`get_traceback_limit` tại thời điểm snapshot được chụp.

   .. attribute:: traces

      Dấu vết của tất cả các khối bộ nhớ được Python cấp phát: một chuỗi các
      :class:`Trace` thực thể.

      Chuỗi này có thứ tự không xác định. Sử dụng phương thức :meth:`Snapshot.statistics` để nhận danh sách thống kê đã được sắp xếp.


Thống kê
^^^^^^^^

.. class:: Statistic

   Thống kê về việc cấp phát bộ nhớ.

   :func:`Snapshot.statistics` trả về một danh sách các thực thể :class:`Statistic`.

   Xem thêm lớp :class:`StatisticDiff`.

   .. attribute:: count

      Số lượng khối bộ nhớ (``int``).

   .. attribute:: size

      Tổng kích thước của các khối bộ nhớ tính bằng byte (``int``).

   .. attribute:: traceback

      Traceback tại vị trí khối bộ nhớ được cấp phát, instance :class:`Traceback`.


StatisticDiff
^^^^^^^^^^^^^

.. class:: StatisticDiff

   Chênh lệch thống kê về việc cấp phát bộ nhớ giữa một
   instance :class:`Snapshot` cũ và mới.

   :func:`Snapshot.compare_to` trả về một danh sách các instance :class:`StatisticDiff`. Xem thêm lớp :class:`Statistic`.

   .. attribute:: count

      Số lượng khối bộ nhớ trong snapshot mới (``int``): ``0`` nếu các khối bộ nhớ đã được giải phóng trong snapshot mới.

   .. attribute:: count_diff

      Chênh lệch số lượng khối bộ nhớ giữa snapshot cũ và snapshot mới (``int``): ``0`` nếu các khối bộ nhớ đã được cấp phát trong snapshot mới.

   .. attribute:: size

      Tổng kích thước tính bằng byte của các khối bộ nhớ trong snapshot mới (``int``): ``0`` nếu các khối bộ nhớ đã được giải phóng trong snapshot mới.

   .. attribute:: size_diff

      Chênh lệch tổng kích thước tính bằng byte của các khối bộ nhớ giữa snapshot cũ và snapshot mới (``int``): ``0`` nếu các khối bộ nhớ đã được cấp phát trong snapshot mới.

   .. attribute:: traceback

      Traceback nơi các khối bộ nhớ được cấp phát, instance :class:`Traceback`.


Trace
^^^^^

.. class:: Trace

   Trace của một khối bộ nhớ.

   Thuộc tính :attr:`Snapshot.traces` là một chuỗi các thực thể :class:`Trace`.

   .. versionchanged:: 3.6
      Đã thêm thuộc tính :attr:`domain`.

   .. attribute:: domain

      Không gian địa chỉ của một khối bộ nhớ (``int``). Thuộc tính chỉ đọc.

      tracemalloc sử dụng domain ``0`` để theo dõi các cấp phát bộ nhớ do Python thực hiện. Các phần mở rộng C có thể sử dụng những domain khác để theo dõi các tài nguyên khác.

   .. attribute:: size

      Kích thước của khối bộ nhớ tính bằng byte (``int``).

   .. attribute:: traceback

      Traceback tại đó khối bộ nhớ được cấp phát, thực thể :class:`Traceback`.


Traceback
^^^^^^^^^

.. class:: Traceback

   Chuỗi các thực thể :class:`Frame` được sắp xếp từ frame cũ nhất đến frame gần đây nhất.

   Một traceback chứa ít nhất ``1`` frame. Nếu module ``tracemalloc`` không lấy được frame, tên tệp ``"<unknown>"`` tại số dòng ``0`` sẽ được sử dụng.

   Khi snapshot được tạo, traceback của các trace bị giới hạn ở
   :func:`get_traceback_limit` frame. Xem hàm :func:`take_snapshot`. Số frame ban đầu của traceback được lưu trong
   thuộc tính :attr:`Traceback.total_nframe`. Điều này cho phép biết traceback có bị cắt ngắn bởi giới hạn traceback hay không.

   Thuộc tính :attr:`Trace.traceback` là một thực thể :class:`Traceback`.

   .. versionchanged:: 3.7
      Các frame hiện được sắp xếp từ frame cũ nhất đến frame gần đây nhất, thay vì từ frame gần đây nhất đến frame cũ nhất.

   .. attribute:: total_nframe

      Tổng số frame tạo nên traceback trước khi cắt ngắn. Thuộc tính này có thể được đặt thành ``None`` nếu không có thông tin.

   .. versionchanged:: 3.9
      Thuộc tính :attr:`Traceback.total_nframe` đã được thêm.

   .. method:: format(limit=None, most_recent_first=False)

      Định dạng traceback thành một danh sách các dòng. Sử dụng module :mod:`linecache` để lấy các dòng từ mã nguồn. Nếu *limit* được đặt, hãy định dạng *limit* frame gần đây nhất nếu *limit* là số dương. Nếu không, hãy định dạng ``abs(limit)`` frame cũ nhất. Nếu *most_recent_first* là ``True``, thứ tự của các frame được định dạng sẽ bị đảo ngược, trả về frame gần đây nhất trước thay vì sau cùng.

      Tương tự hàm :func:`traceback.format_tb`, ngoại trừ việc
      :meth:`.format` không bao gồm các dòng mới.

      Ví dụ::

          print("Traceback (most recent call first):")
          for line in traceback:
              print(line)

      Kết quả::

          Traceback (most recent call first):
            File "test.py", line 9
              obj = Object()
            File "test.py", line 12
              tb = tracemalloc.get_object_traceback(f())
