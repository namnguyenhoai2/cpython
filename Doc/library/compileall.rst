:mod:`!compileall` --- Biên dịch byte các thư viện Python
=========================================================

.. module:: compileall
   :synopsis: Các công cụ để biên dịch byte tất cả tệp nguồn Python trong một cây thư mục.

**Mã nguồn:** :source:`Lib/compileall.py`

--------------

Mô-đun này cung cấp một số hàm tiện ích để hỗ trợ cài đặt các thư viện Python. Các hàm này biên dịch các tệp nguồn Python trong một cây thư mục. Mô-đun này có thể được dùng để tạo các tệp bytecode được lưu vào bộ nhớ đệm tại thời điểm cài đặt thư viện, nhờ đó chúng vẫn có thể được sử dụng ngay cả bởi những người dùng không có quyền ghi vào các thư mục thư viện.

.. include:: ../includes/wasm-notavail.rst

.. _compileall-cli:

Sử dụng từ dòng lệnh
--------------------

Mô-đun này có thể hoạt động như một script (sử dụng :program:`python -m compileall`) để biên dịch mã nguồn Python.

.. program:: compileall

.. option:: directory ...
            file ...

   Các đối số vị trí là các tệp cần biên dịch hoặc các thư mục chứa tệp mã nguồn, được duyệt đệ quy. Nếu không cung cấp đối số nào, hoạt động như thể dòng lệnh là :samp:`-l {<directories from sys.path>}`.

.. option:: -l

   Không đệ quy vào các thư mục con, chỉ biên dịch các tệp mã nguồn nằm trực tiếp trong những thư mục được chỉ định hoặc được ngầm định.

.. option:: -f

   Buộc xây dựng lại ngay cả khi các dấu thời gian đã được cập nhật.

.. option:: -q

   Không in danh sách các tệp đã biên dịch. Nếu được truyền một lần, các thông báo lỗi vẫn được in. Nếu được truyền hai lần (``-qq``), mọi đầu ra sẽ bị loại bỏ.

.. option:: -d destdir

   Thư mục được thêm vào trước đường dẫn của mỗi tệp đang được biên dịch. Thư mục này sẽ xuất hiện trong các traceback tại thời điểm biên dịch, đồng thời cũng được biên dịch vào tệp bytecode, nơi nó sẽ được sử dụng trong traceback và các thông báo khác khi tệp mã nguồn không tồn tại tại thời điểm tệp bytecode được thực thi.

.. option:: -s strip_prefix

   Xóa tiền tố đã cho khỏi các đường dẫn được ghi trong các tệp ``.pyc``. Các đường dẫn được chuyển thành tương đối so với tiền tố.

   Tùy chọn này có thể được sử dụng với ``-p`` nhưng không thể sử dụng với ``-d``.

.. option:: -p prepend_prefix

   Thêm tiền tố đã cho vào trước các đường dẫn được ghi trong các tệp ``.pyc``. Sử dụng ``-p /`` để chuyển các đường dẫn thành đường dẫn tuyệt đối.

   Tùy chọn này có thể được sử dụng với ``-s`` nhưng không thể sử dụng với ``-d``.

.. option:: -x regex

   regex được dùng để tìm kiếm đường dẫn đầy đủ đến từng tệp được xem xét để biên dịch, và nếu regex tạo ra kết quả khớp, tệp đó sẽ bị bỏ qua.

.. option:: -i list

   Đọc tệp ``list`` và thêm từng dòng trong tệp đó vào danh sách các tệp và thư mục cần biên dịch. Nếu ``list`` là ``-``, hãy đọc các dòng từ ``stdin``.

.. option:: -b

   Ghi các tệp byte-code vào vị trí và tên cũ của chúng; thao tác này có thể ghi đè các tệp byte-code được tạo bởi một phiên bản Python khác. Mặc định là ghi các tệp vào vị trí và tên :pep:`3147` của chúng, cho phép các tệp byte-code từ nhiều phiên bản Python cùng tồn tại.

.. option:: -r

   Kiểm soát mức đệ quy tối đa cho các thư mục con. Nếu được chỉ định, tùy chọn ``-l`` sẽ không được tính đến.
   :program:`python -m compileall <directory> -r 0` tương đương với
   :program:`python -m compileall <directory> -l`.

.. option:: -j N

   Sử dụng *N* worker để biên dịch các tệp trong thư mục đã cho. Nếu sử dụng ``0``, kết quả của :func:`os.process_cpu_count` sẽ được sử dụng.

.. option:: --invalidation-mode [timestamp|checked-hash|unchecked-hash]

   Kiểm soát cách các tệp bytecode được tạo ra bị vô hiệu hóa trong runtime. Giá trị ``timestamp`` có nghĩa là sẽ tạo các tệp ``.pyc`` có nhúng dấu thời gian và kích thước của mã nguồn. Các giá trị ``checked-hash`` và ``unchecked-hash`` khiến các pyc dựa trên hash được tạo ra. Các pyc dựa trên hash nhúng hash của nội dung tệp mã nguồn thay vì dấu thời gian. Xem
   :ref:`pyc-invalidation` để biết thêm thông tin về cách Python xác thực các tệp bộ nhớ đệm bytecode trong runtime. Giá trị mặc định là ``timestamp`` nếu biến môi trường :envvar:`SOURCE_DATE_EPOCH` chưa được đặt, và là ``checked-hash`` nếu biến môi trường ``SOURCE_DATE_EPOCH`` đã được đặt.

.. option:: -o level

   Biên dịch với mức tối ưu hóa đã cho. Có thể sử dụng nhiều lần để biên dịch đồng thời cho nhiều mức (ví dụ: ``compileall -o 1 -o 2``).

.. option:: -e dir

   Bỏ qua các symlink trỏ ra ngoài thư mục đã cho.

.. option:: --hardlink-dupes

   Nếu hai tệp ``.pyc`` có mức tối ưu hóa khác nhau nhưng cùng nội dung, hãy sử dụng hard link để hợp nhất các tệp trùng lặp.

.. versionchanged:: 3.2
   Đã thêm các tùy chọn ``-i``, ``-b`` và ``-h``.

.. versionchanged:: 3.5
   Đã thêm các tùy chọn ``-j``, ``-r`` và ``-qq``. Tùy chọn ``-q`` đã được thay đổi thành một giá trị nhiều cấp. ``-b`` sẽ luôn tạo ra một tệp byte-code kết thúc bằng ``.pyc``, không bao giờ bằng ``.pyo``.

.. versionchanged:: 3.7
   Đã thêm tùy chọn ``--invalidation-mode``.

.. versionchanged:: 3.9
   Đã thêm các tùy chọn ``-s``, ``-p``, ``-e`` và ``--hardlink-dupes``. Đã tăng giới hạn đệ quy mặc định từ 10 lên
   :py:func:`sys.getrecursionlimit()`. Đã thêm khả năng chỉ định tùy chọn ``-o`` nhiều lần.


Không có tùy chọn dòng lệnh nào để kiểm soát cấp độ tối ưu hóa được sử dụng bởi
hàm :func:`compile`, vì bản thân trình thông dịch Python đã cung cấp tùy chọn này: :program:`python -O -m compileall`.

Tương tự, hàm :func:`compile` tuân theo thiết lập :data:`sys.pycache_prefix`. Bộ nhớ đệm bytecode được tạo ra sẽ chỉ hữu ích nếu :func:`compile` được chạy với cùng :data:`sys.pycache_prefix` (nếu có) sẽ được sử dụng khi chạy.

Các hàm công khai
-----------------

.. function:: compile_dir(dir, maxlevels=sys.getrecursionlimit(), ddir=None, force=False, rx=None, quiet=0, legacy=False, optimize=-1, workers=1, invalidation_mode=None, *, stripdir=None, prependdir=None, limit_sl_dest=None, hardlink_dupes=False)

   Đệ quy duyệt cây thư mục có tên là *dir*, biên dịch tất cả các tệp :file:`.py` trên đường duyệt. Trả về giá trị true nếu tất cả các tệp được biên dịch thành công, và giá trị false nếu không.

   Tham số *maxlevels* được dùng để giới hạn độ sâu của quá trình đệ quy; giá trị mặc định là ``sys.getrecursionlimit()``.

   Nếu được cung cấp *ddir*, giá trị này được thêm vào đầu đường dẫn đến từng tệp đang được biên dịch để dùng trong các traceback tại thời điểm biên dịch, đồng thời cũng được biên dịch vào tệp byte-code, nơi nó sẽ được dùng trong các traceback và thông báo khác khi tệp nguồn không tồn tại tại thời điểm tệp byte-code được thực thi.

   Nếu *force* là true, các module sẽ được biên dịch lại ngay cả khi dấu thời gian đã được cập nhật.

   Nếu được cung cấp *rx*, phương thức ``search`` của nó sẽ được gọi trên đường dẫn đầy đủ đến từng tệp được xem xét để biên dịch; nếu phương thức này trả về giá trị true, tệp sẽ bị bỏ qua. Có thể dùng tùy chọn này để loại trừ các tệp khớp với một biểu thức chính quy, được cung cấp dưới dạng đối tượng :ref:`re.Pattern <re-objects>`.

   Nếu *quiet* là ``False`` hoặc ``0`` (mặc định), tên tệp và các thông tin khác sẽ được in ra đầu ra chuẩn. Đặt thành ``1``, chỉ các lỗi được in ra. Đặt thành ``2``, mọi đầu ra đều bị ẩn.

   Nếu *legacy* là true, các tệp byte-code sẽ được ghi vào các vị trí và tên cũ, điều này có thể ghi đè các tệp byte-code được tạo bởi một phiên bản Python khác. Mặc định là ghi tệp vào các vị trí và tên :pep:`3147` của chúng, cho phép các tệp byte-code từ nhiều phiên bản Python cùng tồn tại.

   *optimize* chỉ định mức tối ưu hóa cho compiler. Giá trị này được truyền cho hàm tích hợp sẵn :func:`compile`. Cũng chấp nhận một chuỗi các mức tối ưu hóa, dẫn đến việc biên dịch một tệp :file:`.py` nhiều lần trong một lần gọi.

   Đối số *workers* chỉ định số worker được dùng để biên dịch các tệp song song. Mặc định là không dùng nhiều worker. Nếu nền tảng không thể sử dụng nhiều worker và đối số *workers* được cung cấp, việc biên dịch tuần tự sẽ được dùng làm phương án dự phòng. Nếu *workers* là 0, số lõi trong hệ thống sẽ được sử dụng. Nếu *workers* nhỏ hơn ``0``, một :exc:`ValueError` sẽ được raised.

   *invalidation_mode* nên là một thành viên của
   :class:`py_compile.PycInvalidationMode` enum và kiểm soát cách các pyc được tạo sẽ bị vô hiệu hóa tại runtime.

   Các đối số *stripdir*, *prependdir* và *limit_sl_dest* tương ứng với các tùy chọn ``-s``, ``-p`` và ``-e`` được mô tả ở trên. Chúng có thể được chỉ định dưới dạng ``str`` hoặc :py:class:`os.PathLike`.

   Nếu *hardlink_dupes* là true và hai tệp ``.pyc`` có các mức tối ưu hóa khác nhau nhưng cùng nội dung, hãy sử dụng hard link để hợp nhất các tệp trùng lặp.

   .. versionchanged:: 3.2
      Đã thêm tham số *legacy* và *optimize*.

   .. versionchanged:: 3.5
      Đã thêm tham số *workers*.

   .. versionchanged:: 3.5
      Tham số *quiet* đã được thay đổi thành giá trị nhiều cấp.

   .. versionchanged:: 3.5
      Tham số *legacy* chỉ ghi các tệp ``.pyc``, không ghi các tệp ``.pyo`` bất kể giá trị của *optimize* là gì.

   .. versionchanged:: 3.6
      Chấp nhận một :term:`path-like object`.

   .. versionchanged:: 3.7
      Đã thêm tham số *invalidation_mode*.

   .. versionchanged:: 3.7.2
      Giá trị mặc định của tham số *invalidation_mode* đã được cập nhật thành ``None``.

   .. versionchanged:: 3.8
      Việc đặt *workers* thành 0 sẽ chọn số lõi tối ưu.

   .. versionchanged:: 3.9
      Đã thêm các đối số *stripdir*, *prependdir*, *limit_sl_dest* và *hardlink_dupes*. Giá trị mặc định của *maxlevels* đã được thay đổi từ ``10`` thành ``sys.getrecursionlimit()``

.. function:: compile_file(fullname, ddir=None, force=False, rx=None, quiet=0, legacy=False, optimize=-1, invalidation_mode=None, *, stripdir=None, prependdir=None, limit_sl_dest=None, hardlink_dupes=False)

   Biên dịch tệp có đường dẫn *fullname*. Trả về giá trị true nếu tệp được biên dịch thành công và giá trị false nếu không.

   Nếu được cung cấp *ddir*, giá trị này được thêm vào đầu đường dẫn đến tệp đang được biên dịch để sử dụng trong các traceback tại thời điểm biên dịch, đồng thời cũng được biên dịch vào tệp byte-code, nơi nó sẽ được sử dụng trong traceback và các thông báo khác khi tệp nguồn không tồn tại tại thời điểm tệp byte-code được thực thi.

   Nếu được cung cấp *rx*, phương thức ``search`` của nó sẽ nhận đường dẫn đầy đủ đến tệp đang được biên dịch; nếu phương thức này trả về giá trị true, tệp sẽ không được biên dịch và ``True`` sẽ được trả về. Có thể dùng tùy chọn này để loại trừ các tệp khớp với một biểu thức chính quy, được cung cấp dưới dạng đối tượng :ref:`re.Pattern <re-objects>`.

   Nếu *quiet* là ``False`` hoặc ``0`` (mặc định), tên tệp và các thông tin khác sẽ được in ra đầu ra chuẩn. Đặt thành ``1``, chỉ các lỗi được in ra. Đặt thành ``2``, mọi đầu ra đều bị ẩn.

   Nếu *legacy* là true, các tệp byte-code sẽ được ghi vào các vị trí và tên cũ, điều này có thể ghi đè các tệp byte-code được tạo bởi một phiên bản Python khác. Mặc định là ghi tệp vào các vị trí và tên :pep:`3147` của chúng, cho phép các tệp byte-code từ nhiều phiên bản Python cùng tồn tại.

   *optimize* chỉ định mức tối ưu hóa cho compiler. Giá trị này được truyền cho hàm tích hợp sẵn :func:`compile`. Cũng chấp nhận một chuỗi các mức tối ưu hóa, dẫn đến việc biên dịch một tệp :file:`.py` nhiều lần trong một lần gọi.

   *invalidation_mode* nên là một thành viên của
   :class:`py_compile.PycInvalidationMode` enum và kiểm soát cách các pyc được tạo sẽ bị vô hiệu hóa tại runtime.

   Các đối số *stripdir*, *prependdir* và *limit_sl_dest* tương ứng với các tùy chọn ``-s``, ``-p`` và ``-e`` được mô tả ở trên. Chúng có thể được chỉ định dưới dạng ``str`` hoặc :py:class:`os.PathLike`.

   Nếu *hardlink_dupes* là true và hai tệp ``.pyc`` có các mức tối ưu hóa khác nhau nhưng cùng nội dung, hãy sử dụng hard link để hợp nhất các tệp trùng lặp.

   .. versionadded:: 3.2

   .. versionchanged:: 3.5
      Tham số *quiet* đã được thay đổi thành giá trị nhiều cấp.

   .. versionchanged:: 3.5
      Tham số *legacy* chỉ ghi các tệp ``.pyc``, không ghi các tệp ``.pyo`` bất kể giá trị của *optimize* là gì.

   .. versionchanged:: 3.7
      Đã thêm tham số *invalidation_mode*.

   .. versionchanged:: 3.7.2
      Giá trị mặc định của tham số *invalidation_mode* đã được cập nhật thành ``None``.

   .. versionchanged:: 3.9
      Đã thêm các đối số *stripdir*, *prependdir*, *limit_sl_dest* và *hardlink_dupes*.

.. function:: compile_path(skip_curdir=True, maxlevels=0, force=False, quiet=0, legacy=False, optimize=-1, invalidation_mode=None)

   Biên dịch bytecode tất cả các tệp :file:`.py` được tìm thấy dọc theo ``sys.path``. Trả về giá trị true nếu tất cả các tệp được biên dịch thành công, và giá trị false nếu không.

   Nếu *skip_curdir* là true (mặc định), thư mục hiện tại sẽ không được đưa vào quá trình tìm kiếm. Tất cả các tham số khác được truyền cho hàm :func:`compile_dir`. Lưu ý rằng không giống các hàm biên dịch khác, ``maxlevels`` mặc định là ``0``.

   .. versionchanged:: 3.2
      Đã thêm tham số *legacy* và *optimize*.

   .. versionchanged:: 3.5
      Tham số *quiet* đã được thay đổi thành giá trị nhiều cấp.

   .. versionchanged:: 3.5
      Tham số *legacy* chỉ ghi các tệp ``.pyc``, không ghi các tệp ``.pyo`` bất kể giá trị của *optimize* là gì.

   .. versionchanged:: 3.7
      Đã thêm tham số *invalidation_mode*.

   .. versionchanged:: 3.7.2
      Giá trị mặc định của tham số *invalidation_mode* đã được cập nhật thành ``None``.

Để buộc biên dịch lại tất cả các tệp :file:`.py` trong thư mục con :file:`Lib/` và mọi thư mục con của nó::

   import compileall

   compileall.compile_dir('Lib/', force=True)

   # Thực hiện cùng quá trình biên dịch, không bao gồm các tệp trong thư mục .svn.
   import re
   compileall.compile_dir('Lib/', rx=re.compile(r'[/\\][.]svn'), force=True)

   # Các đối tượng pathlib.Path cũng có thể được sử dụng.
   import pathlib
   compileall.compile_dir(pathlib.Path('Lib/'), force=True)

.. seealso::

   Mô-đun :mod:`py_compile`
      Biên dịch byte một tệp nguồn duy nhất.
