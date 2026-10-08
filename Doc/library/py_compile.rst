:mod:`!py_compile` --- Biên dịch các tệp mã nguồn Python
========================================================

.. module:: py_compile
   :synopsis: Tạo các tệp byte-code từ các tệp mã nguồn Python.

.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>
.. documentation based on module docstrings

**Mã nguồn:** :source:`Lib/py_compile.py`

.. index:: pair: file; byte-code

--------------

Mô-đun :mod:`!py_compile` cung cấp một hàm để tạo tệp byte-code từ một tệp mã nguồn, cùng một hàm khác được sử dụng khi tệp mã nguồn của mô-đun được gọi như một script.

Mặc dù không thường xuyên cần đến, hàm này có thể hữu ích khi cài đặt các mô-đun để dùng chung, đặc biệt nếu một số người dùng có thể không có quyền ghi các tệp bộ nhớ đệm byte-code vào thư mục chứa mã nguồn.


.. exception:: PyCompileError

   Ngoại lệ được đưa ra khi xảy ra lỗi trong lúc cố gắng biên dịch tệp.


.. function:: compile(file, cfile=None, dfile=None, doraise=False, optimize=-1, invalidation_mode=PycInvalidationMode.TIMESTAMP, quiet=0)

   Biên dịch một tệp mã nguồn thành byte-code và ghi tệp bộ nhớ đệm byte-code. Mã nguồn được tải từ tệp có tên *file*. Byte-code được ghi vào *cfile*, mặc định là đường dẫn :pep:`3147`/:pep:`488`, kết thúc bằng ``.pyc``. Ví dụ, nếu *file* là ``/foo/bar/baz.py`` *cfile* sẽ mặc định là ``/foo/bar/__pycache__/baz.cpython-32.pyc`` đối với Python 3.2. Nếu *dfile* được chỉ định, nó sẽ được dùng thay cho *file* làm tên của tệp mã nguồn dùng để lấy các dòng mã nguồn nhằm hiển thị trong traceback của ngoại lệ. Nếu *doraise* là true, một :exc:`PyCompileError` sẽ được đưa ra khi gặp lỗi trong lúc biên dịch *file*. Nếu *doraise* là false (mặc định), một chuỗi lỗi sẽ được ghi vào ``sys.stderr``, nhưng không có ngoại lệ nào được đưa ra. Hàm này trả về đường dẫn đến tệp đã được biên dịch thành byte-code, tức là bất kỳ giá trị *cfile* nào đã được sử dụng.

   Các đối số *doraise* và *quiet* xác định cách xử lý lỗi khi biên dịch tệp. Nếu *quiet* là 0 hoặc 1, còn *doraise* là false, hành vi mặc định được bật: một chuỗi lỗi được ghi vào ``sys.stderr``, và hàm trả về ``None`` thay vì một đường dẫn. Nếu *doraise* là true, một :exc:`PyCompileError` sẽ được raise thay thế. Tuy nhiên, nếu *quiet* là 2, không có thông báo nào được ghi và *doraise* không có tác dụng.

   Nếu đường dẫn mà *cfile* trở thành (dù được chỉ định rõ ràng hay được tính toán) là một symlink hoặc tệp không thông thường, :exc:`FileExistsError` sẽ được raise. Điều này nhằm đưa ra cảnh báo rằng import sẽ chuyển các đường dẫn đó thành tệp thông thường nếu được phép ghi các tệp đã biên dịch thành byte-code vào những đường dẫn đó. Đây là tác dụng phụ của việc import sử dụng thao tác đổi tên tệp để đặt tệp byte-code cuối cùng vào đúng vị trí, nhằm ngăn các vấn đề do ghi tệp đồng thời.

   *optimize* kiểm soát mức optimization và được truyền cho hàm dựng sẵn
   :func:`compile` function. Giá trị mặc định là ``-1``, chọn mức optimization của interpreter hiện tại.

   *invalidation_mode* phải là một thành viên của enum :class:`PycInvalidationMode` và kiểm soát cách cache bytecode được tạo ra bị invalidated tại runtime. Giá trị mặc định là :attr:`PycInvalidationMode.CHECKED_HASH` nếu biến môi trường :envvar:`SOURCE_DATE_EPOCH` được đặt; nếu không, giá trị mặc định là :attr:`PycInvalidationMode.TIMESTAMP`.

   .. versionchanged:: 3.2
      Đã thay đổi giá trị mặc định của *cfile* để tuân thủ :PEP:`3147`. Giá trị mặc định trước đây là *file* + ``'c'`` (``'o'`` nếu optimization được bật). Đồng thời đã thêm tham số *optimize*.

   .. versionchanged:: 3.4
      Đã thay đổi mã để sử dụng :mod:`importlib` cho việc ghi tệp cache byte-code. Điều này có nghĩa là ngữ nghĩa tạo/ghi tệp hiện khớp với những gì :mod:`importlib` thực hiện, chẳng hạn như quyền, ngữ nghĩa ghi-rồi-di-chuyển, v.v. Đồng thời đã bổ sung lưu ý rằng :exc:`FileExistsError` sẽ được raise nếu *cfile* là một symlink hoặc tệp không thông thường.

   .. versionchanged:: 3.7
      Tham số *invalidation_mode* được thêm như được chỉ định trong :pep:`552`. Nếu biến môi trường :envvar:`SOURCE_DATE_EPOCH` được đặt, *invalidation_mode* sẽ bị buộc thành
      :attr:`PycInvalidationMode.CHECKED_HASH`.

   .. versionchanged:: 3.7.2
      Biến môi trường :envvar:`SOURCE_DATE_EPOCH` không còn ghi đè giá trị của đối số *invalidation_mode*, mà thay vào đó xác định giá trị mặc định của đối số này.

   .. versionchanged:: 3.8
      Đã thêm tham số *quiet*.


.. class:: PycInvalidationMode

   Một kiểu liệt kê các phương thức mà trình thông dịch có thể sử dụng để xác định xem tệp bytecode có còn cập nhật so với tệp mã nguồn hay không. Tệp ``.pyc`` cho biết chế độ vô hiệu hóa mong muốn trong phần header của tệp. Xem
   :ref:`pyc-invalidation` để biết thêm thông tin về cách Python vô hiệu hóa các tệp ``.pyc`` trong runtime.

   .. versionadded:: 3.7

   .. attribute:: TIMESTAMP

      Tệp ``.pyc`` chứa dấu thời gian và kích thước của tệp mã nguồn; Python sẽ so sánh các giá trị này với metadata của tệp mã nguồn trong runtime để xác định xem có cần tạo lại tệp ``.pyc`` hay không.

   .. attribute:: CHECKED_HASH

      Tệp ``.pyc`` chứa hash của nội dung tệp mã nguồn; Python sẽ so sánh hash này với mã nguồn trong runtime để xác định xem có cần tạo lại tệp ``.pyc`` hay không.

   .. attribute:: UNCHECKED_HASH

      Giống như :attr:`CHECKED_HASH`, tệp ``.pyc`` chứa một hash của nội dung tệp nguồn. Tuy nhiên, khi chạy, Python sẽ giả định rằng tệp ``.pyc`` đã được cập nhật và hoàn toàn không xác thực ``.pyc`` với tệp nguồn.

      Tùy chọn này hữu ích khi ``.pycs`` được một hệ thống bên ngoài Python, chẳng hạn như hệ thống build, cập nhật.

.. _py_compile-cli:

Giao diện dòng lệnh
-------------------

Có thể gọi module này dưới dạng một script để biên dịch nhiều tệp nguồn. Các tệp được chỉ định trong *filenames* sẽ được biên dịch và bytecode tạo ra sẽ được lưu vào bộ nhớ đệm theo cách thông thường. Chương trình này không tìm kiếm cấu trúc thư mục để xác định các tệp nguồn; chương trình chỉ biên dịch những tệp được chỉ định rõ ràng. Trạng thái thoát sẽ khác không nếu không thể biên dịch một trong các tệp.

.. program:: python -m py_compile

.. option:: <file> ... <fileN>
            -

   Các đối số vị trí là những tệp cần biên dịch. Nếu ``-`` là tham số duy nhất, danh sách tệp sẽ được đọc từ đầu vào chuẩn.

.. option:: -q, --quiet

   Không xuất lỗi.

.. versionchanged:: 3.2
   Đã bổ sung hỗ trợ cho ``-``.

.. versionchanged:: 3.10
   Đã bổ sung hỗ trợ cho :option:`-q`.


.. seealso::

   Mô-đun :mod:`compileall`
      Các tiện ích để biên dịch tất cả tệp mã nguồn Python trong một cây thư mục.
