:mod:`!test` --- Gói kiểm thử hồi quy cho Python
================================================

.. module:: test
   :synopsis: Gói kiểm thử hồi quy chứa bộ kiểm thử cho Python.

.. sectionauthor:: Brett Cannon <brett@python.org>

.. note::
   Gói :mod:`!test` chỉ dành cho Python sử dụng nội bộ. Gói này được lập tài liệu nhằm phục vụ các nhà phát triển cốt lõi của Python. Không khuyến khích sử dụng gói này bên ngoài thư viện chuẩn của Python, vì mã được đề cập ở đây có thể thay đổi hoặc bị xóa mà không thông báo giữa các bản phát hành Python.

--------------

Gói :mod:`!test` chứa tất cả các kiểm thử hồi quy cho Python, cũng như các module :mod:`test.support` và :mod:`test.regrtest`.
:mod:`test.support` được dùng để nâng cao các kiểm thử của bạn trong khi
:mod:`test.regrtest` điều khiển bộ kiểm thử.

Mỗi module trong gói :mod:`!test` có tên bắt đầu bằng ``test_`` là một bộ kiểm thử dành cho một module hoặc tính năng cụ thể. Tất cả kiểm thử mới nên được viết bằng module :mod:`unittest` hoặc :mod:`doctest`. Một số kiểm thử cũ được viết theo kiểu kiểm thử "truyền thống", trong đó so sánh đầu ra được in ra ``sys.stdout``; kiểu kiểm thử này được xem là đã lỗi thời.


.. seealso::

   Mô-đun :mod:`unittest`
      Viết các bài kiểm thử hồi quy PyUnit.

   Mô-đun :mod:`doctest`
      Các bài kiểm thử được nhúng trong chuỗi tài liệu.


.. _writing-tests:

Viết các bài kiểm thử đơn vị cho gói :mod:`!test`
-------------------------------------------------

Các bài kiểm thử sử dụng mô-đun :mod:`unittest` nên tuân theo một số hướng dẫn. Một trong số đó là đặt tên mô-đun kiểm thử bằng cách bắt đầu tên với ``test_`` và kết thúc bằng tên của mô-đun đang được kiểm thử. Các phương thức kiểm thử trong mô-đun kiểm thử nên bắt đầu với ``test_`` và kết thúc bằng phần mô tả nội dung mà phương thức đang kiểm thử. Điều này cần thiết để trình điều khiển kiểm thử nhận diện các phương thức đó là phương thức kiểm thử. Ngoài ra, không nên đưa chuỗi tài liệu vào phương thức. Nên sử dụng một chú thích (chẳng hạn như ``# Tests function returns only True or False``) để cung cấp tài liệu cho các phương thức kiểm thử. Lý do là nếu tồn tại, các chuỗi tài liệu sẽ được in ra, và do đó không cho biết bài kiểm thử nào đang được chạy.

Thường sử dụng một phần khung mã cơ bản::

   import unittest
   from test import support

   class MyTestCase1(unittest.TestCase):

       # Chỉ sử dụng setUp() và tearDown() khi cần thiết

       def setUp(self):
           ... code to execute in preparation for tests ...

       def tearDown(self):
           ... code to execute to clean up after tests ...

       def test_feature_one(self):
           # Kiểm thử tính năng một.
           ... testing code ...

       def test_feature_two(self):
           # Kiểm thử tính năng hai.
           ... testing code ...

       ... more test methods ...

   class MyTestCase2(unittest.TestCase):
       ... same structure as MyTestCase1 ...

   ... more test classes ...

   if __name__ == '__main__':
       unittest.main()

Mẫu mã này cho phép chạy bộ kiểm thử bằng :mod:`test.regrtest`, độc lập dưới dạng một script hỗ trợ CLI :mod:`unittest`, hoặc thông qua CLI ``python -m unittest``.

Mục tiêu của kiểm thử hồi quy là cố gắng làm hỏng mã. Điều này dẫn đến một số hướng dẫn cần tuân theo:

* Bộ kiểm thử cần kiểm tra tất cả các class, function và constant. Điều này không chỉ bao gồm API bên ngoài được cung cấp cho thế giới bên ngoài mà còn cả mã "private".

* Nên ưu tiên kiểm thử hộp trắng (kiểm tra mã đang được kiểm thử khi viết các bài kiểm thử). Kiểm thử hộp đen (chỉ kiểm thử giao diện người dùng đã công bố) chưa đủ để đảm bảo tất cả các trường hợp biên và trường hợp đặc biệt đều được kiểm thử.

* Đảm bảo kiểm thử tất cả các giá trị có thể có, bao gồm cả các giá trị không hợp lệ. Điều này đảm bảo không chỉ mọi giá trị hợp lệ đều được chấp nhận mà các giá trị không phù hợp cũng được xử lý đúng cách.

* Bao phủ càng nhiều đường dẫn mã càng tốt. Hãy kiểm thử tại những nơi xảy ra rẽ nhánh và điều chỉnh dữ liệu đầu vào để đảm bảo mã đi qua càng nhiều đường dẫn khác nhau càng tốt.

* Thêm một kiểm thử rõ ràng cho mọi lỗi được phát hiện trong mã đang kiểm thử. Điều này đảm bảo lỗi đó không xuất hiện trở lại nếu mã được thay đổi trong tương lai.

* Đảm bảo dọn dẹp sau khi kiểm thử (chẳng hạn như đóng và xóa tất cả các tệp tạm thời).

* Nếu một kiểm thử phụ thuộc vào một điều kiện cụ thể của hệ điều hành, hãy xác minh rằng điều kiện đó đã tồn tại trước khi thực hiện kiểm thử.

* Nhập càng ít module càng tốt và thực hiện việc đó càng sớm càng tốt. Điều này giảm thiểu các dependency bên ngoài của kiểm thử, đồng thời giảm thiểu hành vi bất thường có thể xảy ra do các tác dụng phụ khi nhập một module.

* Cố gắng tối đa hóa việc tái sử dụng mã. Đôi khi, các kiểm thử chỉ khác nhau ở một yếu tố nhỏ, chẳng hạn như kiểu dữ liệu đầu vào được sử dụng. Giảm thiểu việc trùng lặp mã bằng cách tạo lớp con từ một lớp kiểm thử cơ bản, trong đó lớp mới chỉ định dữ liệu đầu vào::

     class TestFuncAcceptsSequencesMixin:

         func = mySuperWhammyFunction

         def test_func(self):
             self.func(self.arg)

     class AcceptLists(TestFuncAcceptsSequencesMixin, unittest.TestCase):
         arg = [1, 2, 3]

     class AcceptStrings(TestFuncAcceptsSequencesMixin, unittest.TestCase):
         arg = 'abc'

     class AcceptTuples(TestFuncAcceptsSequencesMixin, unittest.TestCase):
         arg = (1, 2, 3)

  Khi sử dụng mẫu này, hãy nhớ rằng mọi lớp kế thừa từ
  :class:`unittest.TestCase` đều được chạy dưới dạng các bài kiểm thử. Lớp :class:`!TestFuncAcceptsSequencesMixin` trong ví dụ trên không có dữ liệu nên không thể tự chạy, do đó lớp này không kế thừa từ :class:`unittest.TestCase`.


.. seealso::

   Phát triển hướng kiểm thử
      Một cuốn sách của Kent Beck về việc viết test trước code.


.. _regrtest:

Chạy test bằng giao diện dòng lệnh
----------------------------------

.. module:: test.regrtest
   :synopsis: Điều khiển bộ kiểm thử hồi quy.

Gói :mod:`!test` có thể được chạy dưới dạng script để điều khiển bộ kiểm thử hồi quy của Python, nhờ tùy chọn :option:`-m`: :program:`python -m test`. Bên dưới, gói này sử dụng :mod:`!test.regrtest`; lời gọi :program:`python -m test.regrtest` được dùng trong các phiên bản Python trước đây vẫn hoạt động. Khi tự chạy script, tất cả các bài kiểm thử hồi quy trong
gói :mod:`!test`. Gói này thực hiện việc đó bằng cách tìm tất cả các module trong gói có tên bắt đầu bằng ``test_``, import chúng và thực thi hàm
:func:`test_main` nếu có, hoặc tải các bài kiểm thử bằng unittest.TestLoader.loadTestsFromModule nếu ``test_main`` không tồn tại. Tên của các bài kiểm thử cần thực thi cũng có thể được truyền vào script. Việc chỉ định một bài kiểm thử hồi quy duy nhất (:program:`python -m test test_spam`) sẽ giảm lượng đầu ra và chỉ in cho biết bài kiểm thử đã đạt hay thất bại.

Việc chạy :mod:`!test` trực tiếp cho phép thiết lập những tài nguyên nào có thể được các bài kiểm thử sử dụng. Bạn thực hiện việc này bằng tùy chọn dòng lệnh ``-u``. Chỉ định ``all`` làm giá trị cho tùy chọn ``-u`` sẽ bật tất cả tài nguyên có thể có: :program:`python -m test -uall`. Nếu muốn sử dụng tất cả trừ một tài nguyên (trường hợp phổ biến hơn), bạn có thể liệt kê các tài nguyên không mong muốn sau ``all``, phân tách bằng dấu phẩy. Lệnh :program:`python -m test -uall,-audio,-largefile` sẽ chạy :mod:`!test` với tất cả tài nguyên ngoại trừ tài nguyên ``audio`` và ``largefile``. Để xem danh sách tất cả tài nguyên và các tùy chọn dòng lệnh khác, hãy chạy :program:`python -m test -h`.

Một số cách khác để thực thi các bài kiểm thử hồi quy phụ thuộc vào nền tảng mà các bài kiểm thử được thực thi. Trên Unix, bạn có thể chạy :program:`make test` trong thư mục cấp cao nhất nơi Python được build. Trên Windows, việc thực thi :program:`rt.bat` từ thư mục :file:`PCbuild` của bạn sẽ chạy tất cả các bài kiểm thử hồi quy.

.. versionadded:: 3.14
   Theo mặc định, đầu ra được tô màu và có thể
   :ref:`được kiểm soát bằng các biến môi trường <using-on-controlling-color>`.


:mod:`!test.support` --- Các tiện ích cho bộ kiểm thử Python
============================================================

.. module:: test.support
   :synopsis: Hỗ trợ cho bộ kiểm thử hồi quy của Python.


Mô-đun :mod:`!test.support` cung cấp hỗ trợ cho bộ kiểm thử hồi quy của Python.

.. note::

   :mod:`!test.support` không phải là mô-đun công khai. Mô-đun này được ghi lại ở đây để giúp các nhà phát triển Python viết các bài kiểm thử. API của mô-đun này có thể thay đổi giữa các bản phát hành mà không đảm bảo khả năng tương thích ngược.


Mô-đun này định nghĩa các ngoại lệ sau:

.. exception:: TestFailed

   Ngoại lệ được phát sinh khi một bài kiểm thử thất bại. Ngoại lệ này không còn được khuyến nghị sử dụng, thay vào đó hãy dùng
   Các bài kiểm thử dựa trên :mod:`unittest`\  và các phương thức assertion của :class:`unittest.TestCase`.


.. exception:: ResourceDenied

   Lớp con của :exc:`unittest.SkipTest`. Được phát sinh khi một tài nguyên (chẳng hạn như kết nối mạng) không khả dụng. Được phát sinh bởi hàm :func:`requires`.


Mô-đun :mod:`!test.support` định nghĩa các hằng số sau:

.. data:: verbose

   ``True`` khi đầu ra chi tiết được bật. Nên kiểm tra giá trị này khi cần thông tin chi tiết hơn về một kiểm thử đang chạy. *verbose* được thiết lập bởi
   :mod:`test.regrtest`.


.. data:: is_jython

   ``True`` nếu trình thông dịch đang chạy là Jython.


.. data:: is_android

   ``True`` nếu ``sys.platform`` là ``android``.


.. data:: is_emscripten

   ``True`` nếu ``sys.platform`` là ``emscripten``.


.. data:: is_wasi

   ``True`` nếu ``sys.platform`` là ``wasi``.


.. data:: is_apple_mobile

   ``True`` nếu ``sys.platform`` là ``ios``, ``tvos`` hoặc ``watchos``.


.. data:: is_apple

   ``True`` nếu ``sys.platform`` là ``darwin`` hoặc ``is_apple_mobile`` là ``True``.


.. data:: unix_shell

   Đường dẫn cho shell nếu không chạy trên Windows; nếu không thì ``None``.


.. data:: LOOPBACK_TIMEOUT

   Thời gian chờ tính bằng giây cho các bài kiểm thử sử dụng máy chủ mạng lắng nghe trên giao diện loopback cục bộ của mạng, chẳng hạn như ``127.0.0.1``.

   Thời gian chờ đủ dài để ngăn bài kiểm thử thất bại: thời gian này tính đến khả năng client và máy chủ chạy trong các thread khác nhau hoặc thậm chí trong các process khác nhau.

   Thời gian chờ phải đủ dài cho :meth:`~socket.socket.connect`,
   các phương thức :meth:`~socket.socket.recv` và :meth:`~socket.socket.send` của
   :class:`socket.socket`.

   Giá trị mặc định của nó là 10 giây.

   Xem thêm :data:`INTERNET_TIMEOUT`.


.. data:: INTERNET_TIMEOUT

   Thời gian chờ tính bằng giây cho các yêu cầu mạng đi đến internet.

   Thời gian chờ đủ ngắn để ngăn một kiểm thử phải chờ quá lâu nếu yêu cầu internet bị chặn vì bất kỳ lý do nào.

   Thông thường, thời gian chờ sử dụng :data:`INTERNET_TIMEOUT` không nên đánh dấu kiểm thử là thất bại mà nên bỏ qua kiểm thử đó: xem
   :func:`~test.support.socket_helper.transient_internet`.

   Giá trị mặc định của nó là 1 phút.

   Xem thêm :data:`LOOPBACK_TIMEOUT`.


.. data:: SHORT_TIMEOUT

   Thời gian chờ tính bằng giây để đánh dấu kiểm thử là thất bại nếu kiểm thử chạy "quá lâu".

   Giá trị timeout phụ thuộc vào tùy chọn dòng lệnh ``--timeout`` của regrtest.

   Nếu một test sử dụng :data:`SHORT_TIMEOUT` bắt đầu bị lỗi ngẫu nhiên trên các buildbot chậm, hãy sử dụng :data:`LONG_TIMEOUT` thay thế.

   Giá trị mặc định là 30 giây.


.. data:: LONG_TIMEOUT

   Thời gian timeout tính bằng giây để phát hiện khi một test bị treo.

   Giá trị này đủ dài để giảm nguy cơ test bị lỗi trên các buildbot Python chậm nhất. Không nên sử dụng nó để đánh dấu test là bị lỗi nếu test mất "quá nhiều thời gian". Giá trị timeout phụ thuộc vào tùy chọn dòng lệnh ``--timeout`` của regrtest.

   Giá trị mặc định là 5 phút.

   Xem thêm :data:`LOOPBACK_TIMEOUT`, :data:`INTERNET_TIMEOUT` và
   :data:`SHORT_TIMEOUT`.


.. data:: PGO

   Được thiết lập khi có thể bỏ qua các bài kiểm thử vì chúng không hữu ích cho PGO.


.. data:: PIPE_MAX_SIZE

   Một hằng số có khả năng lớn hơn kích thước bộ đệm pipe của hệ điều hành bên dưới, nhằm khiến việc ghi bị chặn.


.. data:: Py_DEBUG

   ``True`` nếu Python được xây dựng với macro :c:macro:`Py_DEBUG` được định nghĩa, tức là nếu Python được :ref:`xây dựng ở chế độ debug <debug-build>`.

   .. versionadded:: 3.12


.. data:: SOCK_MAX_SIZE

   Một hằng số có khả năng lớn hơn kích thước bộ đệm socket của hệ điều hành bên dưới, nhằm khiến việc ghi bị chặn.


.. data:: TEST_SUPPORT_DIR

   Được thiết lập thành thư mục cấp cao nhất chứa :mod:`!test.support`.


.. data:: TEST_HOME_DIR

   Được thiết lập thành thư mục cấp cao nhất của gói kiểm thử.


.. data:: TEST_DATA_DIR

   Được thiết lập thành thư mục ``data`` bên trong gói kiểm thử.


.. data:: MAX_Py_ssize_t

   Đặt thành :data:`sys.maxsize` cho các bài kiểm tra bộ nhớ lớn.


.. data:: max_memuse

   Được :func:`set_memlimit` đặt làm giới hạn bộ nhớ cho các bài kiểm tra bộ nhớ lớn. Bị giới hạn bởi :data:`MAX_Py_ssize_t`.


.. data:: real_max_memuse

   Được :func:`set_memlimit` đặt làm giới hạn bộ nhớ cho các bài kiểm tra bộ nhớ lớn. Không bị giới hạn bởi :data:`MAX_Py_ssize_t`.


.. data:: MISSING_C_DOCSTRINGS

   Đặt thành ``True`` nếu Python được build mà không có docstring (macro
   :c:macro:`WITH_DOC_STRINGS` không được định nghĩa). Xem tùy chọn :option:`configure --without-doc-strings <--without-doc-strings>`.

   Xem thêm biến :data:`HAVE_DOCSTRINGS`.


.. data:: HAVE_DOCSTRINGS

   Đặt thành ``True`` nếu docstring của hàm khả dụng. Xem tùy chọn :option:`python -OO <-O>`, tùy chọn này loại bỏ docstring của các hàm được triển khai bằng Python.

   Xem thêm biến :data:`MISSING_C_DOCSTRINGS`.


.. data:: TEST_HTTP_URL

   Xác định URL của một HTTP server chuyên dụng cho các bài kiểm thử mạng.


.. data:: ALWAYS_EQ

   Đối tượng bằng với mọi thứ. Được dùng để kiểm thử phép so sánh giữa các kiểu khác nhau.


.. data:: NEVER_EQ

   Đối tượng không bằng bất kỳ thứ gì (kể cả :data:`ALWAYS_EQ`). Được dùng để kiểm thử phép so sánh giữa các kiểu khác nhau.


.. data:: LARGEST

   Đối tượng lớn hơn mọi thứ (ngoại trừ chính nó). Được dùng để kiểm thử phép so sánh giữa các kiểu khác nhau.


.. data:: SMALLEST

   Đối tượng nhỏ hơn mọi thứ (ngoại trừ chính nó). Được dùng để kiểm thử phép so sánh giữa các kiểu khác nhau.


Mô-đun :mod:`!test.support` định nghĩa các hàm sau:

.. function:: busy_retry(timeout, err_msg=None, /, *, error=True)

   Chạy phần thân vòng lặp cho đến khi ``break`` dừng vòng lặp.

   Sau *timeout* giây, phát sinh một :exc:`AssertionError` nếu *error* là true, hoặc chỉ dừng vòng lặp nếu *error* là false.

   Ví dụ::

       for _ in support.busy_retry(support.SHORT_TIMEOUT):
           if check():
               break

   Ví dụ sử dụng error=False::

       for _ in support.busy_retry(support.SHORT_TIMEOUT, error=False):
           if check():
               break
       else:
           raise RuntimeError('my custom error')

.. function:: sleeping_retry(timeout, err_msg=None, /, *, init_delay=0.010, max_delay=1.0, error=True)

   Chiến lược chờ áp dụng exponential backoff.

   Chạy phần thân vòng lặp cho đến khi ``break`` dừng vòng lặp. Chờ ở mỗi lần lặp, nhưng không chờ ở lần lặp đầu tiên. Thời gian chờ được tăng gấp đôi sau mỗi lần lặp (tối đa *max_delay* giây).

   Xem tài liệu :func:`busy_retry` để biết cách sử dụng các tham số.

   Ví dụ phát sinh một exception sau SHORT_TIMEOUT giây::

       for _ in support.sleeping_retry(support.SHORT_TIMEOUT):
           if check():
               break

   Ví dụ sử dụng error=False::

       for _ in support.sleeping_retry(support.SHORT_TIMEOUT, error=False):
           if check():
               break
       else:
           raise RuntimeError('my custom error')

.. function:: is_resource_enabled(resource)

   Trả về ``True`` nếu tài nguyên *resource* được bật và khả dụng. Danh sách các tài nguyên khả dụng chỉ được thiết lập khi :mod:`test.regrtest` đang thực thi các bài kiểm thử.


.. function:: get_resource_value(resource)

   Trả về giá trị được chỉ định cho tài nguyên *resource* (dưới dạng :samp:`-u {resource}={value}`). Trả về ``None`` nếu tài nguyên *resource* bị tắt hoặc không được chỉ định giá trị.


.. function:: python_is_optimized()

   Trả về ``True`` nếu Python không được build với ``-O0`` hoặc ``-Og``.


.. function:: with_pymalloc()

   Trả về :const:`_testcapi.WITH_PYMALLOC`.


.. function:: requires(resource, msg=None)

   Phát sinh :exc:`ResourceDenied` nếu tài nguyên *resource* không khả dụng. *msg* là đối số của :exc:`ResourceDenied` nếu exception này được phát sinh. Luôn trả về ``True`` nếu được gọi bởi một hàm có ``__name__`` là ``'__main__'``. Được sử dụng khi các bài kiểm thử được thực thi bởi :mod:`test.regrtest`.


.. function:: sortdict(dict)

   Trả về repr của *dict* với các khóa được sắp xếp.


.. function:: findfile(filename, subdir=None)

   Trả về đường dẫn đến tệp có tên *filename*. Nếu không tìm thấy kết quả khớp, *filename* sẽ được trả về. Điều này không tương đương với việc xảy ra lỗi, vì đó có thể là đường dẫn đến tệp.

   Thiết lập *subdir* cho biết đường dẫn tương đối cần dùng để tìm tệp thay vì tìm trực tiếp trong các thư mục đường dẫn.


.. function:: get_pagesize()

   Lấy kích thước của một trang theo byte.

   .. versionadded:: 3.12


.. function:: setswitchinterval(interval)

   Đặt :func:`sys.setswitchinterval` thành *interval* đã cho. Xác định khoảng thời gian tối thiểu cho các hệ thống Android để ngăn hệ thống bị treo.


.. function:: check_impl_detail(**guards)

   Sử dụng bước kiểm tra này để bảo vệ các bài kiểm thử dành riêng cho việc triển khai CPython hoặc chỉ chạy chúng trên các bản triển khai được bảo vệ bởi các đối số. Hàm này trả về ``True`` hoặc ``False`` tùy thuộc vào nền tảng máy chủ. Ví dụ sử dụng::

      check_impl_detail()               # Chỉ trên CPython (mặc định).
      check_impl_detail(jython=True)    # Chỉ trên Jython.
      check_impl_detail(cpython=False)  # Ở mọi nơi ngoại trừ CPython.


.. function:: set_memlimit(limit)

   Đặt các giá trị cho :data:`max_memuse` và :data:`real_max_memuse` cho các bài kiểm tra bộ nhớ lớn.


.. function:: record_original_stdout(stdout)

   Lưu giá trị từ *stdout*. Giá trị này dùng để lưu stdout tại thời điểm regrtest bắt đầu.


.. function:: get_original_stdout()

   Trả về stdout ban đầu được thiết lập bởi :func:`record_original_stdout` hoặc ``sys.stdout`` nếu nó chưa được thiết lập.


.. function:: args_from_interpreter_flags()

   Trả về danh sách các đối số dòng lệnh tái tạo các thiết lập hiện tại trong ``sys.flags`` và ``sys.warnoptions``.


.. function:: optim_args_from_interpreter_flags()

   Trả về danh sách các đối số dòng lệnh tái tạo các thiết lập tối ưu hóa hiện tại trong ``sys.flags``.


.. function:: captured_stdin()
              captured_stdout() captured_stderr()

   Một context manager tạm thời thay thế stream được chỉ định bằng
   đối tượng :class:`io.StringIO`.

   Ví dụ sử dụng với các output stream::

      with captured_stdout() as stdout, captured_stderr() as stderr:
          print("hello")
          print("error", file=sys.stderr)
      assert stdout.getvalue() == "hello\n"
      assert stderr.getvalue() == "error\n"

   Ví dụ sử dụng với input stream::

      with captured_stdin() as stdin:
          stdin.write('hello\n')
          stdin.seek(0)
          # gọi mã kiểm thử sử dụng dữ liệu từ sys.stdin
          captured = input()
      self.assertEqual(captured, "hello")


.. function:: disable_faulthandler()

   Một context manager tạm thời vô hiệu hóa :mod:`faulthandler`.


.. function:: gc_collect()

   Buộc thu gom càng nhiều đối tượng càng tốt. Điều này cần thiết vì trình garbage collector không đảm bảo giải phóng kịp thời. Điều đó có nghĩa là các phương thức ``__del__`` có thể được gọi muộn hơn dự kiến và weakref có thể vẫn tồn tại lâu hơn dự kiến.


.. function:: disable_gc()

   Một context manager vô hiệu hóa garbage collector khi bắt đầu. Khi kết thúc, garbage collector được khôi phục về trạng thái trước đó.


.. function:: swap_attr(obj, attr, new_val)

   Context manager để thay thế một thuộc tính bằng một đối tượng mới.

   Cách sử dụng::

      with swap_attr(obj, "attr", 5):
          ...

   Thao tác này sẽ đặt ``obj.attr`` thành 5 trong khoảng thời gian của khối ``with``, rồi khôi phục giá trị cũ khi kết thúc khối. Nếu ``attr`` không tồn tại trên ``obj``, nó sẽ được tạo rồi bị xóa khi kết thúc khối.

   Giá trị cũ (hoặc ``None`` nếu giá trị đó không tồn tại) sẽ được gán cho đối tượng đích của mệnh đề "as", nếu có.


.. function:: swap_item(obj, attr, new_val)

   Context manager để thay thế một phần tử bằng một đối tượng mới.

   Cách sử dụng::

      with swap_item(obj, "item", 5):
          ...

   Thao tác này sẽ đặt ``obj["item"]`` thành 5 trong suốt thời gian của khối ``with``, rồi khôi phục giá trị cũ khi kết thúc khối. Nếu ``item`` không tồn tại trên ``obj``, nó sẽ được tạo rồi bị xóa khi kết thúc khối.

   Giá trị cũ (hoặc ``None`` nếu giá trị đó không tồn tại) sẽ được gán cho đối tượng đích của mệnh đề "as", nếu có.


.. function:: flush_std_streams()

   Gọi phương thức ``flush()`` trên :data:`sys.stdout` rồi trên
   :data:`sys.stderr`. Có thể dùng nó để đảm bảo thứ tự của các log nhất quán trước khi ghi vào stderr.

   .. versionadded:: 3.11


.. function:: print_warning(msg)

   In một cảnh báo vào :data:`sys.__stderr__`. Định dạng thông báo như sau: ``f"Warning -- {msg}"``. Nếu *msg* gồm nhiều dòng, hãy thêm tiền tố ``"Warning -- "`` vào mỗi dòng.

   .. versionadded:: 3.9


.. function:: wait_process(pid, *, exitcode, timeout=None)

   Chờ tiến trình *pid* hoàn tất và kiểm tra xem mã thoát của tiến trình có phải là *exitcode* hay không.

   Ném một :exc:`AssertionError` nếu mã thoát của tiến trình không bằng *exitcode*.

   Nếu tiến trình chạy lâu hơn *timeout* giây (:data:`SHORT_TIMEOUT` theo mặc định), hãy kết thúc tiến trình và ném một :exc:`AssertionError`. Tính năng timeout không khả dụng trên Windows.

   .. versionadded:: 3.9


.. function:: calcobjsize(fmt)

   Trả về kích thước của :c:type:`PyObject` có các thành viên cấu trúc được định nghĩa bởi *fmt*. Giá trị trả về bao gồm kích thước phần header của đối tượng Python và phần căn chỉnh.


.. function:: calcvobjsize(fmt)

   Trả về kích thước của :c:type:`PyVarObject` có các thành viên cấu trúc được định nghĩa bởi *fmt*. Giá trị trả về bao gồm kích thước phần header của đối tượng Python và phần căn chỉnh.


.. function:: checksizeof(test, o, size)

   Đối với testcase *test*, hãy khẳng định rằng ``sys.getsizeof`` của *o* cộng với kích thước header GC bằng *size*.


.. decorator:: anticipate_failure(condition)

   Một decorator dùng để đánh dấu có điều kiện các kiểm thử bằng
   :deco:`unittest.expectedFailure`. Mọi cách sử dụng decorator này cần có chú thích đi kèm xác định issue tương ứng trên tracker.


.. function:: system_must_validate_cert(f)

   Một decorator bỏ qua bài kiểm thử được trang trí khi xảy ra lỗi xác thực chứng chỉ TLS.


.. decorator:: run_with_locale(catstr, *locales)

   Một decorator chạy một hàm trong locale khác và đặt lại locale đúng cách sau khi hàm hoàn tất. *catstr* là danh mục locale dưới dạng chuỗi (ví dụ ``"LC_ALL"``). Các *locales* được truyền vào sẽ lần lượt được thử, và locale hợp lệ đầu tiên sẽ được sử dụng.


.. decorator:: run_with_tz(tz)

   Một decorator chạy một hàm trong một múi giờ cụ thể và đặt lại múi giờ đúng cách sau khi hàm hoàn tất.


.. decorator:: requires_freebsd_version(*min_version)

   Decorator chỉ định phiên bản tối thiểu khi chạy bài kiểm thử trên FreeBSD. Nếu phiên bản FreeBSD thấp hơn mức tối thiểu, bài kiểm thử sẽ bị bỏ qua.


.. decorator:: requires_linux_version(*min_version)

   Decorator chỉ định phiên bản tối thiểu khi chạy bài kiểm thử trên Linux. Nếu phiên bản Linux thấp hơn mức tối thiểu, bài kiểm thử sẽ bị bỏ qua.


.. decorator:: requires_mac_version(*min_version)

   Decorator chỉ định phiên bản tối thiểu khi chạy bài kiểm thử trên macOS. Nếu phiên bản macOS thấp hơn mức tối thiểu, bài kiểm thử sẽ bị bỏ qua.


.. decorator:: requires_gil_enabled

   Decorator bỏ qua các bài kiểm thử trên bản build free-threaded. Nếu
   :term:`GIL` bị tắt, bài kiểm thử được bỏ qua.


.. decorator:: requires_IEEE_754

   Trình trang trí để bỏ qua các bài kiểm thử trên những nền tảng không tuân theo IEEE 754.


.. decorator:: requires_zlib

   Trình trang trí để bỏ qua các bài kiểm thử nếu :mod:`zlib` không tồn tại.


.. decorator:: requires_gzip

   Trình trang trí để bỏ qua các bài kiểm thử nếu :mod:`gzip` không tồn tại.


.. decorator:: requires_bz2

   Trình trang trí để bỏ qua các bài kiểm thử nếu :mod:`bz2` không tồn tại.


.. decorator:: requires_lzma

   Trình trang trí để bỏ qua các bài kiểm thử nếu :mod:`lzma` không tồn tại.


.. decorator:: requires_resource(resource)

   Trình trang trí để bỏ qua các bài kiểm thử nếu *resource* không khả dụng.


.. decorator:: requires_docstrings

   Decorator chỉ chạy bài kiểm thử nếu :data:`HAVE_DOCSTRINGS`.


.. decorator:: requires_limited_api

   Decorator chỉ chạy bài kiểm thử nếu :ref:`Limited C API <limited-c-api>` khả dụng.


.. decorator:: cpython_only

   Decorator dành cho các bài kiểm thử chỉ áp dụng cho CPython.


.. decorator:: impl_detail(msg=None, **guards)

   Decorator gọi :func:`check_impl_detail` trên *các guard*. Nếu kết quả là ``False``, thì sử dụng *msg* làm lý do bỏ qua bài kiểm thử.

.. decorator:: thread_unsafe(reason=None)

   Decorator đánh dấu các bài kiểm thử là không an toàn khi chạy trong thread. Bài kiểm thử này luôn chạy trong một thread ngay cả khi được gọi bằng ``--parallel-threads``.


.. decorator:: no_tracing

   Decorator tạm thời tắt tracing trong thời gian chạy bài kiểm thử.


.. decorator:: refcount_test

   Decorator dành cho các bài kiểm thử liên quan đến việc đếm reference. Decorator không chạy bài kiểm thử nếu nó không được chạy bởi CPython. Mọi hàm trace đều bị bỏ thiết lập trong thời gian chạy bài kiểm thử để ngăn refcount không mong muốn do hàm trace gây ra.


.. decorator:: bigmemtest(size, memuse, dry_run=True)

   Decorator dành cho các kiểm thử bigmem.

   *size* là kích thước được yêu cầu cho kiểm thử (theo các đơn vị tùy ý do kiểm thử diễn giải). *memuse* là số byte trên mỗi đơn vị cho kiểm thử hoặc một ước tính phù hợp. Ví dụ: một kiểm thử cần hai bộ đệm byte, mỗi bộ đệm có kích thước 4 GiB, có thể được áp dụng ``@bigmemtest(size=_4G, memuse=2)``.

   Đối số *size* thường được truyền cho phương thức kiểm thử đã được áp dụng decorator dưới dạng một đối số bổ sung. Nếu *dry_run* là ``True``, giá trị được truyền cho phương thức kiểm thử có thể nhỏ hơn giá trị được yêu cầu. Nếu *dry_run* là ``False``, điều đó có nghĩa là kiểm thử không hỗ trợ các lần chạy giả khi ``-M`` không được chỉ định.


.. decorator:: bigaddrspacetest

   Decorator dành cho các kiểm thử lấp đầy không gian địa chỉ.


.. function:: linked_to_musl()

   Trả về ``False`` nếu không có bằng chứng cho thấy interpreter được biên dịch với ``musl``; nếu không, trả về một bộ ba phiên bản, trong đó ``(0, 0, 0)`` nếu không xác định được phiên bản hoặc phiên bản thực tế nếu xác định được. Dùng cho các decorator ``skip``. Giả định ``emscripten`` và ``wasi`` được biên dịch với ``musl``; nếu không, ``platform.libc_ver`` sẽ được kiểm tra.


.. function:: check_syntax_error(testcase, statement, errtext='', *, lineno=None, offset=None)

   Kiểm tra lỗi cú pháp trong *statement* bằng cách cố gắng biên dịch *statement*. *testcase* là thực thể :mod:`unittest` cho kiểm thử. *errtext* là biểu thức chính quy phải khớp với biểu diễn chuỗi của :exc:`SyntaxError` được phát sinh. Nếu *lineno* không phải là ``None``, so sánh với dòng xảy ra ngoại lệ. Nếu *offset* không phải là ``None``, so sánh với vị trí lệch của ngoại lệ.


.. function:: open_urlresource(url, *args, **kw)

   Mở *url*. Nếu mở không thành công, phát sinh :exc:`TestFailed`.


.. function:: reap_children()

   Sử dụng điều này ở cuối ``test_main`` mỗi khi các quy trình con được khởi chạy. Điều này giúp đảm bảo không có tiến trình con dư thừa nào (zombie) tiếp tục tồn tại, chiếm dụng tài nguyên và gây ra sự cố khi tìm refleak.


.. function:: get_attribute(obj, name)

   Lấy một thuộc tính, đồng thời phát sinh :exc:`unittest.SkipTest` nếu :exc:`AttributeError` được phát sinh.


.. function:: catch_unraisable_exception()

   Trình quản lý ngữ cảnh bắt ngoại lệ không thể xử lý bằng cách sử dụng
   :func:`sys.unraisablehook`.

   Việc lưu giá trị ngoại lệ (``cm.unraisable.exc_value``) tạo ra một chu kỳ tham chiếu (reference cycle). Chu kỳ tham chiếu này được phá vỡ một cách rõ ràng khi trình quản lý ngữ cảnh kết thúc.

   Việc lưu đối tượng (``cm.unraisable.object``) có thể làm đối tượng hồi sinh nếu đối tượng đó được gán cho một đối tượng đang được hoàn tất. Khi trình quản lý ngữ cảnh kết thúc, đối tượng được lưu sẽ được xóa.

   Cách sử dụng::

       with support.catch_unraisable_exception() as cm:
           # đoạn mã tạo ra một "unraisable exception"
           ...

           # kiểm tra ngoại lệ không thể phát sinh: sử dụng cm.unraisable
           ...

       # thuộc tính cm.unraisable không còn tồn tại tại thời điểm này
       # (để phá vỡ một chu kỳ tham chiếu)

   .. versionadded:: 3.8


.. function:: load_package_tests(pkg_dir, loader, standard_tests, pattern)

   Triển khai :mod:`unittest` ``load_tests`` protocol tổng quát để sử dụng trong các gói kiểm thử. *pkg_dir* là thư mục gốc của gói; *loader*, *standard_tests* và *pattern* là các đối số mà ``load_tests`` mong đợi. Trong những trường hợp đơn giản, ``__init__.py`` của gói kiểm thử có thể là đoạn sau::

      import os
      from test.support import load_package_tests

      def load_tests(*args):
          return load_package_tests(os.path.dirname(__file__), *args)


.. function:: detect_api_mismatch(ref_api, other_api, *, ignore=())

   Trả về tập hợp các thuộc tính, hàm hoặc phương thức của *ref_api* không có trên *other_api*, ngoại trừ danh sách các mục được xác định để bỏ qua trong lần kiểm tra này, được chỉ định trong *ignore*.

   Theo mặc định, hàm này bỏ qua các thuộc tính private bắt đầu bằng '_' nhưng bao gồm tất cả các phương thức magic, tức là những phương thức bắt đầu và kết thúc bằng '__'.

   .. versionadded:: 3.5


.. function:: patch(test_instance, object_to_patch, attr_name, new_value)

   Ghi đè *object_to_patch.attr_name* bằng *new_value*. Đồng thời thêm thủ tục dọn dẹp vào *test_instance* để khôi phục *object_to_patch* cho *attr_name*. *attr_name* phải là một thuộc tính hợp lệ của *object_to_patch*.


.. function:: run_in_subinterp(code)

   Chạy *code* trong subinterpreter. Tăng :exc:`unittest.SkipTest` nếu
   :mod:`tracemalloc` được bật.


.. currentmodule:: test.support.isolation

.. decorator:: runInSubprocess(*, options=(), env=None, timeout=None)

   Decorator này chạy bài kiểm thử được trang trí trong một subprocess interpreter mới, độc lập, để không chia sẻ trạng thái toàn cục hoặc trạng thái interpreter với phần còn lại của lượt chạy kiểm thử. Decorator này có thể được áp dụng cho một phương thức kiểm thử hoặc toàn bộ
   :class:`~unittest.TestCase` subclass. Các phương thức được trang trí không được nhận thêm đối số. Một lỗi, ngoại lệ hoặc lần bỏ qua trong subprocess sẽ được báo cáo cho bài kiểm thử tương ứng, còn từng :meth:`subtests <unittest.TestCase.subTest>` bị lỗi hoặc bị bỏ qua sẽ được báo cáo riêng. Một lỗi hoặc ngoại lệ được báo cáo sẽ hiển thị traceback gốc của subprocess làm nguyên nhân của exception.

   Khi một **method** được trang trí, chỉ phương thức đó chạy trong subprocess; tất cả fixture (:meth:`~unittest.TestCase.setUp` / :meth:`~unittest.TestCase.tearDown`,
   :meth:`~unittest.TestCase.setUpClass` / :meth:`~unittest.TestCase.tearDownClass` và ``setUpModule()`` / ``tearDownModule()``) đều chạy trong process cha (như thường lệ) và trong subprocess quanh phương thức đó.

   Khi một **class** được trang trí, toàn bộ lớp chạy trong một subprocess duy nhất, còn :meth:`~unittest.TestCase.setUpClass`,
   :meth:`~unittest.TestCase.tearDownClass`, :meth:`~unittest.TestCase.setUp` và :meth:`~unittest.TestCase.tearDown` mỗi cái chạy một lần trong subprocess và bị bỏ qua trong parent process. Việc :meth:`~unittest.TestCase.tearDownClass` bị lỗi hoặc bị bỏ qua
   :meth:`~unittest.TestCase.setUpClass` trong subprocess được báo cáo cho toàn bộ lớp.  ``setUpModule()`` không thể được kiểm soát bằng class decorator, vì vậy nó vẫn chạy trong tiến trình cha; hãy kiểm thử bằng
   :data:`runningInSubprocess` nếu cần.

   Subprocess kế thừa các resource được bật (``-u``), giới hạn bộ nhớ (``-M``) và verbosity (``-v``) của lần chạy kiểm thử trong parent, để
   :func:`~test.support.requires_resource`, :func:`~test.support.requires`,
   :func:`~test.support.bigmemtest` và các tùy chọn tương tự hoạt động nhất quán trong cả hai process.

   *options* là một chuỗi các tùy chọn dòng lệnh của interpreter để chạy subprocess, còn *env* là một mapping các biến môi trường cần đặt trong đó, ngoài môi trường được kế thừa. Giá trị ``None`` trong *env* sẽ hủy đặt biến đó. Lưu ý rằng :option:`-E` và :option:`-I` khiến subprocess bỏ qua các biến môi trường ``PYTHON*``, bao gồm cả :envvar:`PYTHONPATH`.

   *timeout* là số giây cần chờ subprocess; bài kiểm thử được báo cáo là lỗi nếu không hoàn tất trong thời gian đó. Theo mặc định, không có thời gian chờ và một bài kiểm thử bị treo sẽ chờ đến thời hạn của test runner.

   Bài kiểm thử được bỏ qua trên các nền tảng không hỗ trợ subprocess.


.. data:: runningInSubprocess

   ``True`` trong khi mã chạy trong subprocess cô lập được tạo bởi
   :func:`runInSubprocess`, và ``False`` trong các trường hợp khác (bao gồm trong tiến trình cha và trong một lần chạy kiểm thử thông thường, không cô lập). Các fixture như
   :meth:`~unittest.TestCase.setUp`, :meth:`~unittest.TestCase.tearDown`,
   :meth:`~unittest.TestCase.setUpClass`, :meth:`~unittest.TestCase.tearDownClass`, ``setUpModule()`` và ``tearDownModule()`` có thể kiểm tra điều này để chọn mã cần chạy trong subprocess.


.. currentmodule:: test.support


.. function:: check_free_after_iterating(test, iter, cls, args=())

   Xác nhận rằng các thực thể của *cls* được giải phóng sau khi lặp.


.. function:: missing_compiler_executable(cmd_names=[])

   Kiểm tra sự tồn tại của các tệp thực thi của compiler có tên được liệt kê trong *cmd_names* hoặc tất cả các tệp thực thi của compiler khi *cmd_names* trống, rồi trả về tệp thực thi đầu tiên bị thiếu hoặc ``None`` nếu không tìm thấy tệp nào bị thiếu.


.. function:: check__all__(test_case, module, name_of_module=None, extra=(), not_exported=())

   Xác nhận rằng biến ``__all__`` của *module* chứa tất cả các tên công khai.

   Các tên public của module (API của module) được tự động phát hiện dựa trên việc chúng có khớp với quy ước tên public và được định nghĩa trong *module* hay không.

   Đối số *name_of_module* có thể chỉ định (dưới dạng một chuỗi hoặc tuple các chuỗi) module nào có thể định nghĩa API để API đó được phát hiện là public API. Một trường hợp sử dụng là khi *module* import một phần public API của nó từ các module khác, có thể là một C backend (như ``csv`` và ``_csv`` của nó).

   Đối số *extra* có thể là một tập hợp các tên mà nếu không thì sẽ không được tự động phát hiện là "public", chẳng hạn như các đối tượng không có thuộc tính :attr:`~definition.__module__` phù hợp. Nếu được cung cấp, tập hợp này sẽ được thêm vào các tên được tự động phát hiện.

   Đối số *not_exported* có thể là một tập hợp các tên không được xem là một phần của public API, ngay cả khi tên của chúng cho thấy điều ngược lại.

   Ví dụ sử dụng::

      import bar
      import foo
      import unittest
      from test import support

      class MiscTestCase(unittest.TestCase):
          def test__all__(self):
              support.check__all__(self, foo)

      class OtherTestCase(unittest.TestCase):
          def test__all__(self):
              extra = {'BAR_CONST', 'FOO_CONST'}
              not_exported = {'baz'}  # Tên không được ghi tài liệu.
              # bar import một phần API của nó từ _bar.
              support.check__all__(self, bar, ('bar', '_bar'),
                                   extra=extra, not_exported=not_exported)

   .. versionadded:: 3.6

.. function:: skip_if_broken_multiprocessing_synchronize()

   Bỏ qua các kiểm thử nếu thiếu module :mod:`multiprocessing.synchronize`, nếu không có implementation semaphore khả dụng hoặc nếu việc tạo lock phát sinh :exc:`OSError`.

   .. versionadded:: 3.10


.. function:: check_disallow_instantiation(test_case, tp, *args, **kwds)

   Khẳng định rằng không thể khởi tạo type *tp* bằng *args* và *kwds*.

   .. versionadded:: 3.10


.. function:: adjust_int_max_str_digits(max_digits)

   Hàm này trả về một context manager sẽ thay đổi giá trị global
   :func:`sys.set_int_max_str_digits` trong thời gian context tồn tại, cho phép thực thi mã kiểm thử cần một giới hạn khác về số chữ số khi chuyển đổi giữa integer và string.

   .. versionadded:: 3.11


Module :mod:`!test.support` định nghĩa các class sau:


.. class:: SuppressCrashReport()

   Một context manager được dùng để cố gắng ngăn các hộp thoại crash bật lên trong những kiểm thử dự kiến làm crash một subprocess.

   Trên Windows, nó vô hiệu hóa các hộp thoại Windows Error Reporting bằng `SetErrorMode <https://msdn.microsoft.com/en-us/library/windows/desktop/ms680621.aspx>`_.

   Trên UNIX, :func:`resource.setrlimit` được dùng để đặt
   giới hạn mềm của :const:`resource.RLIMIT_CORE` về 0 nhằm ngăn việc tạo tệp coredump.

   Trên cả hai nền tảng, giá trị cũ được khôi phục bằng :meth:`~object.__exit__`.


.. class:: SaveSignals()

   Lớp dùng để lưu và khôi phục các trình xử lý tín hiệu được đăng ký bởi trình xử lý tín hiệu Python.

   .. method:: save(self)

      Lưu các trình xử lý tín hiệu vào một từ điển ánh xạ số hiệu tín hiệu với trình xử lý tín hiệu hiện tại.

   .. method:: restore(self)

      Đặt các số hiệu tín hiệu từ từ điển :meth:`save` thành trình xử lý đã lưu.


.. class:: Matcher()

   .. method:: matches(self, d, **kwargs)

      Thử khớp một dict duy nhất với các đối số được cung cấp.


   .. method:: match_value(self, k, dv, v)

      Cố gắng khớp một giá trị được lưu trữ duy nhất (*dv*) với một giá trị được cung cấp (*v*).


:mod:`!test.support.socket_helper` --- Tiện ích cho các bài kiểm thử socket
===========================================================================

.. module:: test.support.socket_helper
   :synopsis: Hỗ trợ cho các bài kiểm thử socket.


Mô-đun :mod:`!test.support.socket_helper` cung cấp hỗ trợ cho các bài kiểm thử socket.

.. versionadded:: 3.9


.. data:: IPV6_ENABLED

    Được đặt thành ``True`` nếu IPv6 được bật trên máy chủ này, nếu không thì là ``False``.


.. function:: find_unused_port(family=socket.AF_INET, socktype=socket.SOCK_STREAM)

   Trả về một cổng chưa được sử dụng, phù hợp để liên kết. Việc này được thực hiện bằng cách tạo một socket tạm thời có cùng family và type với tham số ``sock`` (mặc định là :const:`~socket.AF_INET`,
   :const:`~socket.SOCK_STREAM`), rồi liên kết socket đó với địa chỉ host được chỉ định (mặc định là ``0.0.0.0``) và đặt cổng thành 0, yêu cầu hệ điều hành cấp một cổng tạm thời chưa được sử dụng. Sau đó, socket tạm thời được đóng và xóa, rồi cổng tạm thời được trả về.

   Nên sử dụng phương thức này hoặc :func:`bind_port` cho mọi kiểm thử cần liên kết một server socket với một cổng cụ thể trong suốt thời gian kiểm thử. Việc chọn phương thức nào phụ thuộc vào việc code gọi đang tạo một Python socket hay cần cung cấp một cổng chưa được sử dụng trong constructor hoặc truyền cổng đó cho một chương trình bên ngoài (ví dụ: đối số ``-accept`` trong chế độ s_server của openssl). Luôn ưu tiên :func:`bind_port` hơn
   :func:`find_unused_port` khi có thể. Không khuyến khích sử dụng cổng được ghi cố định vì điều này có thể khiến nhiều instance của kiểm thử không thể chạy đồng thời, gây ra vấn đề cho buildbot.


.. function:: bind_port(sock, host=HOST)

   Liên kết socket với một cổng trống và trả về số cổng. Phương thức này dựa vào các cổng ephemeral để đảm bảo chúng ta đang sử dụng một cổng chưa được liên kết. Điều này rất quan trọng vì nhiều kiểm thử có thể chạy đồng thời, đặc biệt trong môi trường buildbot. Phương thức này sẽ raise một exception nếu ``sock.family`` là :const:`~socket.AF_INET` và ``sock.type`` là
   :const:`~socket.SOCK_STREAM`, và socket đã có
   :const:`~socket.SO_REUSEADDR` hoặc :const:`~socket.SO_REUSEPORT` được thiết lập trên đó. Kiểm thử không bao giờ được thiết lập các socket option này cho socket TCP/IP. Trường hợp duy nhất cần thiết lập các option này là kiểm thử multicast thông qua nhiều UDP socket.

   Ngoài ra, nếu socket option :const:`~socket.SO_EXCLUSIVEADDRUSE` khả dụng (tức là trên Windows), option này sẽ được thiết lập trên socket. Điều này sẽ ngăn bất kỳ tiến trình nào khác liên kết với host/port của chúng ta trong suốt thời gian kiểm thử.


.. function:: bind_unix_socket(sock, addr)

   Liên kết một Unix socket, và raise :exc:`unittest.SkipTest` nếu
   :exc:`PermissionError` được phát sinh.


.. decorator:: skip_unless_bind_unix_socket

   Một decorator để chạy các bài kiểm thử yêu cầu ``bind()`` hoạt động bình thường cho các socket Unix.


.. function:: transient_internet(resource_name, *, timeout=30.0, errnos=())

   Một context manager sẽ phát sinh :exc:`~test.support.ResourceDenied` khi nhiều vấn đề khác nhau với kết nối internet biểu hiện dưới dạng các exception.


:mod:`!test.support.script_helper` --- Các tiện ích cho các bài kiểm thử thực thi Python
========================================================================================

.. module:: test.support.script_helper
   :synopsis: Hỗ trợ cho các bài kiểm thử thực thi script của Python.


Module :mod:`!test.support.script_helper` cung cấp hỗ trợ cho các bài kiểm thử thực thi script của Python.

.. function:: interpreter_requires_environment()

   Trả về ``True`` nếu ``sys.executable interpreter`` yêu cầu các biến môi trường để có thể chạy được.

   Điều này được thiết kế để dùng với ``@unittest.skipIf()`` nhằm chú thích các bài kiểm thử cần sử dụng hàm ``assert_python*()`` để khởi chạy một quy trình con ở chế độ cô lập (``-I``) hoặc chế độ không có môi trường (``-E``).

   Một lần build và test thông thường không gặp tình huống này, nhưng tình huống này có thể xảy ra khi cố chạy bộ kiểm thử thư viện chuẩn từ một interpreter không có thư mục home rõ ràng theo logic tìm home hiện tại của Python.

   Thiết lập :envvar:`PYTHONHOME` là một cách để chạy hầu hết testsuite trong tình huống đó. :envvar:`PYTHONPATH` hoặc :envvar:`PYTHONUSERSITE` là những biến môi trường phổ biến khác có thể ảnh hưởng đến việc interpreter có thể khởi động hay không.


.. function:: run_python_until_end(*args, **env_vars)

   Thiết lập môi trường dựa trên *env_vars* để chạy interpreter trong một subprocess. Các giá trị có thể bao gồm ``__isolated``, ``__cleanenv``, ``__cwd`` và ``TERM``.

   .. versionchanged:: 3.9
      Hàm này không còn loại bỏ khoảng trắng khỏi *stderr*.


.. function:: assert_python_ok(*args, **env_vars)

   Xác nhận rằng việc chạy interpreter với *args* và các biến môi trường tùy chọn *env_vars* thành công (``rc == 0``) và trả về một tuple ``(return code, stdout, stderr)``.

   Nếu tham số chỉ dùng theo keyword *__cleanenv* được thiết lập, *env_vars* sẽ được sử dụng làm môi trường mới.

   Python được khởi chạy ở chế độ isolated (tùy chọn dòng lệnh ``-I``), trừ khi tham số chỉ nhận đối số từ khóa *__isolated* được đặt thành ``False``.

   .. versionchanged:: 3.9
      Hàm này không còn loại bỏ khoảng trắng khỏi *stderr*.


.. function:: assert_python_failure(*args, **env_vars)

   Khẳng định rằng việc chạy trình thông dịch với *args* và các biến môi trường tùy chọn *env_vars* sẽ không thành công (``rc != 0``) và trả về một tuple ``(return code, stdout, stderr)``.

   Xem :func:`assert_python_ok` để biết thêm tùy chọn.

   .. versionchanged:: 3.9
      Hàm này không còn loại bỏ khoảng trắng khỏi *stderr*.


.. function:: spawn_python(*args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kw)

   Chạy một Python subprocess với các đối số đã cho.

   *kw* là các đối số từ khóa bổ sung cần truyền cho :func:`subprocess.Popen`. Trả về một
   đối tượng :class:`subprocess.Popen`.


.. function:: kill_python(p)

   Chạy quy trình :class:`subprocess.Popen` đã cho đến khi hoàn tất và trả về stdout.


.. function:: make_script(script_dir, script_basename, source, omit_suffix=False)

   Tạo tập lệnh chứa *source* tại đường dẫn *script_dir* và *script_basename*. Nếu *omit_suffix* là ``False``, hãy nối thêm ``.py`` vào tên. Trả về đường dẫn đầy đủ của tập lệnh.


.. function:: make_zip_script(zip_dir, zip_basename, script_name, name_in_zip=None)

   Tạo tệp zip tại *zip_dir* và *zip_basename* với phần mở rộng ``zip``, trong đó chứa các tệp trong *script_name*. *name_in_zip* là tên của kho lưu trữ. Trả về một tuple chứa ``(full path, full path of archive name)``.


.. function:: make_pkg(pkg_dir, init_source='')

   Tạo một thư mục có tên *pkg_dir*, chứa một tệp ``__init__`` với nội dung là *init_source*.


.. function:: make_zip_pkg(zip_dir, zip_basename, pkg_name, script_basename, \
                           source, depth=1, compiled=False)

   Tạo một thư mục gói zip với đường dẫn *zip_dir* và *zip_basename*, chứa một tệp ``__init__`` rỗng và một tệp *script_basename* chứa *source*. Nếu *compiled* là ``True``, cả hai tệp nguồn sẽ được biên dịch và thêm vào gói zip. Trả về một tuple gồm đường dẫn zip đầy đủ và tên kho lưu trữ của tệp zip.


:mod:`!test.support.bytecode_helper` --- Công cụ hỗ trợ kiểm thử việc tạo bytecode chính xác
============================================================================================

.. module:: test.support.bytecode_helper
   :synopsis: Công cụ hỗ trợ kiểm thử việc tạo bytecode chính xác.

Mô-đun :mod:`!test.support.bytecode_helper` cung cấp các tính năng hỗ trợ cho việc kiểm thử và kiểm tra quá trình tạo bytecode.

.. versionadded:: 3.9

Mô-đun này định nghĩa lớp sau:

.. class:: BytecodeTestCase(unittest.TestCase)

   Lớp này có các phương thức assertion tùy chỉnh để kiểm tra bytecode.

.. method:: BytecodeTestCase.get_disassembly_as_string(co)

   Trả về mã disassembly của *co* dưới dạng chuỗi.


.. method:: BytecodeTestCase.assertInBytecode(x, opname, argval=_UNSPECIFIED)

   Trả về instr nếu tìm thấy *opname*, nếu không sẽ ném :exc:`AssertionError`.


.. method:: BytecodeTestCase.assertNotInBytecode(x, opname, argval=_UNSPECIFIED)

   Phát sinh :exc:`AssertionError` nếu tìm thấy *opname*.


:mod:`!test.support.threading_helper` --- Tiện ích cho việc kiểm thử threading
==============================================================================

.. module:: test.support.threading_helper
   :synopsis: Hỗ trợ cho việc kiểm thử threading.

Mô-đun :mod:`!test.support.threading_helper` cung cấp các công cụ hỗ trợ cho việc kiểm thử threading.

.. versionadded:: 3.10


.. function:: join_thread(thread, timeout=None)

   Thực hiện join một *thread* trong *timeout*. Phát sinh một :exc:`AssertionError` nếu thread vẫn đang hoạt động sau *timeout* giây.


.. decorator:: reap_threads

   Decorator bảo đảm các thread được dọn dẹp ngay cả khi bài kiểm thử thất bại.


.. function:: start_threads(threads, unlock=None)

   Context manager để khởi động *threads*, tức là một chuỗi các thread. *unlock* là một hàm được gọi sau khi các thread được khởi động, ngay cả khi đã xảy ra ngoại lệ; một ví dụ có thể là :meth:`threading.Event.set`. ``start_threads`` sẽ cố gắng join các thread đã khởi động khi thoát.


.. function:: threading_cleanup(*original_values)

   Dọn dẹp các thread không được chỉ định trong *original_values*. Được thiết kế để phát cảnh báo nếu một test để lại các thread đang chạy trong nền.


.. function:: threading_setup()

   Trả về số lượng thread hiện tại và bản sao của các thread còn tồn tại.


.. function:: wait_threads_exit(timeout=None)

   Context manager chờ cho đến khi tất cả các thread được tạo trong câu lệnh ``with`` thoát.


.. function:: catch_threading_exception()

   Context manager bắt ngoại lệ :class:`threading.Thread` bằng cách sử dụng
   :func:`threading.excepthook`.

   Các thuộc tính được thiết lập khi bắt được một ngoại lệ:

   * ``exc_type``
   * ``exc_value``
   * ``exc_traceback``
   * ``thread``

   Xem tài liệu :func:`threading.excepthook`.

   Các thuộc tính này sẽ bị xóa khi context manager thoát.

   Cách sử dụng::

       with threading_helper.catch_threading_exception() as cm:
           # mã tạo một thread phát sinh exception
           ...

           # kiểm tra exception của thread, sử dụng các thuộc tính của cm:
           # các thuộc tính exc_type, exc_value, exc_traceback, thread
           ...

       # các thuộc tính exc_type, exc_value, exc_traceback, thread của cm không còn
       # tồn tại tại thời điểm này
       # (để tránh vòng lặp tham chiếu)

   .. versionadded:: 3.8


.. function:: run_concurrently(worker_func, nthreads, args=(), kwargs={})

    Chạy đồng thời hàm worker trong nhiều thread. Ném lại một exception nếu bất kỳ thread nào phát sinh exception, sau khi tất cả thread đã hoàn tất.


:mod:`!test.support.os_helper` --- Các tiện ích cho việc kiểm thử os
====================================================================

.. module:: test.support.os_helper
   :synopsis: Hỗ trợ cho việc kiểm thử os.

Module :mod:`!test.support.os_helper` cung cấp hỗ trợ cho việc kiểm thử os.

.. versionadded:: 3.10


.. data:: FS_NONASCII

   Một ký tự không phải ASCII có thể được mã hóa bằng :func:`os.fsencode`.


.. data:: SAVEDCWD

   Được đặt thành :func:`os.getcwd`.


.. data:: TESTFN

   Được đặt thành một tên an toàn để sử dụng làm tên tệp tạm thời. Mọi tệp tạm thời được tạo ra cần được đóng và unlink (xóa).


.. data:: TESTFN_NONASCII

   Đặt thành một tên tệp chứa ký tự :data:`FS_NONASCII`, nếu có thể. Điều này đảm bảo rằng nếu tên tệp tồn tại, nó có thể được mã hóa và giải mã bằng encoding mặc định của hệ thống tệp. Nhờ đó, các kiểm thử yêu cầu tên tệp không phải ASCII có thể dễ dàng được bỏ qua trên những nền tảng không hỗ trợ chúng.


.. data:: TESTFN_UNENCODABLE

   Đặt thành một tên tệp (kiểu str) không thể được mã hóa bằng encoding của hệ thống tệp ở chế độ strict. Nó có thể là ``None`` nếu không thể tạo tên tệp như vậy.


.. data:: TESTFN_UNDECODABLE

   Đặt thành một tên tệp (kiểu bytes) không thể được giải mã bằng encoding của hệ thống tệp ở chế độ strict. Nó có thể là ``None`` nếu không thể tạo tên tệp như vậy.


.. data:: TESTFN_UNICODE

    Đặt thành một tên không phải ASCII cho một tệp tạm thời.


.. class:: EnvironmentVarGuard()

   Lớp dùng để tạm thời đặt hoặc hủy đặt các biến môi trường. Các instance có thể được dùng như một context manager và có đầy đủ giao diện từ điển để truy vấn/sửa đổi ``os.environ`` bên dưới. Sau khi thoát khỏi context manager, mọi thay đổi đối với các biến môi trường được thực hiện thông qua instance này sẽ được hoàn tác.

   .. versionchanged:: 3.1
      Đã thêm giao diện từ điển.


.. class:: FakePath(path)

   :term:`path-like object` đơn giản. Nó triển khai
   Phương thức :meth:`~os.PathLike.__fspath__` chỉ trả về đối số *path*. Nếu *path* là một exception, nó sẽ được raise trong :meth:`!__fspath__`.


.. method:: EnvironmentVarGuard.set(envvar, value)

   Tạm thời đặt biến môi trường ``envvar`` thành giá trị ``value``.


.. method:: EnvironmentVarGuard.unset(envvar, *others)

   Tạm thời bỏ đặt một hoặc nhiều biến môi trường.

   .. versionchanged:: 3.14
      Có thể bỏ đặt nhiều biến môi trường.


.. function:: can_symlink()

   Trả về ``True`` nếu hệ điều hành hỗ trợ symbolic links, nếu không thì trả về ``False``.


.. function:: can_xattr()

   Trả về ``True`` nếu hệ điều hành hỗ trợ xattr, nếu không thì trả về ``False``.


.. function:: change_cwd(path, quiet=False)

   Một context manager tạm thời thay đổi thư mục làm việc hiện tại thành *path* và yield thư mục đó.

   Nếu *quiet* là ``False``, context manager sẽ phát sinh ngoại lệ khi có lỗi. Nếu không, nó chỉ đưa ra cảnh báo và giữ nguyên thư mục làm việc hiện tại.


.. function:: create_empty_file(filename)

   Tạo một tệp trống với *filename*. Nếu tệp đã tồn tại, cắt ngắn tệp đó.


.. function:: fd_count()

   Đếm số lượng file descriptor đang mở.


.. function:: fs_is_case_insensitive(directory)

   Trả về ``True`` nếu hệ thống tệp cho *directory* không phân biệt chữ hoa chữ thường.


.. function:: make_bad_fd()

   Tạo một file descriptor không hợp lệ bằng cách mở rồi đóng một tệp tạm thời, sau đó trả về descriptor của tệp đó.


.. function:: rmdir(filename)

   Gọi :func:`os.rmdir` trên *filename*. Trên các nền tảng Windows, thao tác này được bọc trong một vòng lặp chờ để kiểm tra sự tồn tại của tệp; điều này cần thiết vì các chương trình chống virus có thể giữ tệp ở trạng thái mở và ngăn việc xóa tệp.


.. function:: rmtree(path)

   Gọi :func:`shutil.rmtree` trên *path* hoặc gọi :func:`os.lstat` và
   :func:`os.rmdir` để xóa một đường dẫn và nội dung của đường dẫn đó. Cũng như :func:`rmdir`, trên các nền tảng Windows, thao tác này được bao bọc bằng một vòng lặp chờ để kiểm tra sự tồn tại của các tệp.


.. decorator:: skip_unless_symlink

   Một decorator dùng để chạy các bài kiểm thử yêu cầu hỗ trợ symbolic link.


.. decorator:: skip_unless_xattr

   Một decorator dùng để chạy các bài kiểm thử yêu cầu hỗ trợ xattr.


.. function:: temp_cwd(name='tempcwd', quiet=False)

   Một context manager tạm thời tạo một thư mục mới và thay đổi thư mục làm việc hiện tại (CWD).

   Context manager này tạo một thư mục tạm thời trong thư mục hiện tại với tên *name* trước khi tạm thời thay đổi thư mục làm việc hiện tại. Nếu *name* là ``None``, thư mục tạm thời được tạo bằng :func:`tempfile.mkdtemp`.

   Nếu *quiet* là ``False`` và không thể tạo hoặc thay đổi CWD, một lỗi sẽ được phát sinh. Nếu không, chỉ một cảnh báo được phát ra và CWD ban đầu được sử dụng.


.. function:: temp_dir(path=None, quiet=False)

   Một context manager tạo một thư mục tạm thời tại *path* và trả về thư mục đó.

   Nếu *path* là ``None``, thư mục tạm thời được tạo bằng
   :func:`tempfile.mkdtemp`.  Nếu *quiet* là ``False``, context manager sẽ phát sinh ngoại lệ khi có lỗi.  Nếu không, khi *path* được chỉ định nhưng không thể tạo, chỉ một cảnh báo được đưa ra.


.. function:: temp_umask(umask)

   Một context manager tạm thời đặt umask của process.


.. function:: unlink(filename)

   Gọi :func:`os.unlink` trên *filename*.  Tương tự như :func:`rmdir`, trên các nền tảng Windows, thao tác này được bọc trong một vòng lặp chờ để kiểm tra sự tồn tại của tệp.


:mod:`!test.support.import_helper` --- Tiện ích cho các bài kiểm thử import
===========================================================================

.. module:: test.support.import_helper
   :synopsis: Hỗ trợ cho các bài kiểm thử import.

Module :mod:`!test.support.import_helper` cung cấp hỗ trợ cho các bài kiểm thử import.

.. versionadded:: 3.10


.. function:: forget(module_name)

   Xóa module có tên *module_name* khỏi ``sys.modules`` và xóa mọi tệp đã biên dịch thành byte của module đó.


.. function:: import_fresh_module(name, fresh=(), blocked=(), deprecated=False)

   Hàm này nhập và trả về một bản sao mới của module Python có tên bằng cách xóa module đó khỏi ``sys.modules`` trước khi thực hiện thao tác nhập. Lưu ý rằng, không giống như :func:`reload`, module gốc không bị ảnh hưởng bởi thao tác này.

   *fresh* là một iterable chứa các tên module bổ sung cũng được xóa khỏi bộ nhớ đệm ``sys.modules`` trước khi thực hiện thao tác nhập.

   *blocked* là một iterable chứa các tên module được thay thế bằng ``None`` trong bộ nhớ đệm module trong quá trình nhập, nhằm đảm bảo rằng các nỗ lực nhập chúng sẽ gây ra :exc:`ImportError`.

   Module được chỉ định cùng mọi module có tên trong các tham số *fresh* và *blocked* sẽ được lưu lại trước khi bắt đầu thao tác nhập, sau đó được chèn trở lại vào ``sys.modules`` khi quá trình nhập mới hoàn tất.

   Các thông báo không còn được khuyến nghị của module và package sẽ bị bỏ qua trong quá trình nhập này nếu *deprecated* là ``True``.

   Hàm này sẽ phát sinh :exc:`ImportError` nếu không thể nhập module được chỉ định.

   Ví dụ sử dụng::

      # Lấy các bản sao của module warnings để kiểm thử mà không ảnh hưởng đến
      # phiên bản đang được phần còn lại của bộ kiểm thử sử dụng. Một bản sao sử dụng
      # implementation C, bản còn lại bị buộc sử dụng implementation Python thuần túy dự phòng
      # implementation
      py_warnings = import_fresh_module('warnings', blocked=['_warnings'])
      c_warnings = import_fresh_module('warnings', fresh=['_warnings'])

   .. versionadded:: 3.1


.. function:: import_module(name, deprecated=False, *, required_on=())

   Hàm này import và trả về module có tên được chỉ định. Không giống như import thông thường, hàm này phát sinh :exc:`unittest.SkipTest` nếu không thể import module.

   Các thông báo deprecated của module và package sẽ bị ẩn trong quá trình import này nếu *deprecated* là ``True``. Nếu một module bắt buộc phải có trên một nền tảng nhưng là tùy chọn trên các nền tảng khác, hãy đặt *required_on* thành một iterable gồm các tiền tố nền tảng để so sánh với :data:`sys.platform`.

   .. versionadded:: 3.1


.. function:: modules_setup()

   Trả về một bản sao của :data:`sys.modules`.


.. function:: modules_cleanup(oldmodules)

   Xóa các module ngoại trừ *oldmodules* và ``encodings`` để bảo toàn bộ nhớ đệm nội bộ.


.. function:: unload(name)

   Xóa *name* khỏi ``sys.modules``.


.. function:: make_legacy_pyc(source)

   Di chuyển một tệp pyc :pep:`3147`/:pep:`488` đến vị trí pyc cũ của nó và trả về đường dẫn hệ thống tệp đến tệp pyc cũ. Giá trị *source* là đường dẫn hệ thống tệp đến tệp nguồn. Tệp này không cần phải tồn tại, tuy nhiên tệp pyc PEP 3147/488 phải tồn tại.


.. class:: CleanImport(*module_names)

   Một context manager dùng để buộc import trả về một tham chiếu module mới. Điều này hữu ích khi kiểm thử các hành vi cấp module, chẳng hạn như việc phát ra một
   :exc:`DeprecationWarning` khi import. Ví dụ sử dụng::

      with CleanImport('foo'):
          importlib.import_module('foo')  # Tham chiếu mới.


.. class:: DirsOnSysPath(*paths)

   Một context manager để tạm thời thêm các thư mục vào :data:`sys.path`.

   Context manager này tạo một bản sao của :data:`sys.path`, nối thêm mọi thư mục được cung cấp dưới dạng đối số vị trí, rồi khôi phục :data:`sys.path` về các thiết lập đã sao chép khi context kết thúc.

   Lưu ý rằng *all* :data:`sys.path` sửa đổi nào trong phần thân của context manager, kể cả việc thay thế đối tượng, cũng sẽ được khôi phục khi kết thúc khối.


:mod:`!test.support.warnings_helper` --- Tiện ích cho các kiểm thử cảnh báo
===========================================================================

.. module:: test.support.warnings_helper
   :synopsis: Hỗ trợ cho các kiểm thử cảnh báo.

Mô-đun :mod:`!test.support.warnings_helper` cung cấp tính năng hỗ trợ cho các kiểm thử cảnh báo.

.. versionadded:: 3.10


.. function:: ignore_warnings(*, category)

   Bỏ qua các cảnh báo là các thể hiện của *category*, đối tượng này phải là :exc:`Warning` hoặc một lớp con. Về cơ bản tương đương với :func:`warnings.catch_warnings` cùng với :meth:`warnings.simplefilter('ignore', category=category) <warnings.simplefilter>`. Ví dụ::

      @warning_helper.ignore_warnings(category=DeprecationWarning)
      def test_suppress_warning():
          # thực hiện một thao tác

   .. versionadded:: 3.8


.. function:: check_no_resource_warning(testcase)

   Context manager để kiểm tra rằng không có :exc:`ResourceWarning` nào được phát ra. Bạn phải xóa đối tượng có thể phát ra :exc:`ResourceWarning` trước khi kết thúc context manager.


.. function:: check_syntax_warning(testcase, statement, errtext='', *, lineno=1, offset=None)

   Kiểm tra syntax warning trong *statement* bằng cách cố gắng biên dịch *statement*. Đồng thời kiểm tra rằng :exc:`SyntaxWarning` chỉ được phát ra một lần và sẽ được chuyển đổi thành :exc:`SyntaxError` khi được chuyển thành lỗi. *testcase* là instance :mod:`unittest` dùng cho bài kiểm tra. *errtext* là regular expression phải khớp với biểu diễn chuỗi của :exc:`SyntaxWarning` được phát ra và :exc:`SyntaxError` được phát sinh. Nếu *lineno* không phải là ``None``, so sánh với dòng của warning và exception. Nếu *offset* không phải là ``None``, so sánh với offset của exception.

   .. versionadded:: 3.8


.. function:: check_warnings(*filters, quiet=True)

   Một wrapper tiện lợi cho :func:`warnings.catch_warnings`, giúp dễ dàng kiểm tra rằng một warning đã được phát sinh đúng cách. Nó gần tương đương với việc gọi ``warnings.catch_warnings(record=True)`` với
   :meth:`warnings.simplefilter` được đặt thành ``always`` và có tùy chọn tự động xác thực các kết quả được ghi lại.

   ``check_warnings`` chấp nhận các tuple 2 phần tử có dạng ``("message regexp", WarningCategory)`` làm đối số vị trí. Nếu cung cấp một hoặc nhiều *filters*, hoặc nếu đối số keyword tùy chọn *quiet* là ``False``, hàm sẽ kiểm tra để đảm bảo các warning đúng như mong đợi: mỗi filter được chỉ định phải khớp với ít nhất một warning do đoạn mã bao quanh phát sinh, nếu không bài kiểm tra sẽ thất bại; và nếu có warning nào được phát sinh nhưng không khớp với bất kỳ filter nào đã chỉ định, bài kiểm tra cũng sẽ thất bại. Để tắt lần kiểm tra đầu tiên, đặt *quiet* thành ``True``.

   Nếu không chỉ định đối số nào, giá trị mặc định là::

      check_warnings(("", Warning), quiet=True)

   Trong trường hợp này, tất cả cảnh báo đều được bắt và không có lỗi nào được phát sinh.

   Khi đi vào context manager, một thực thể :class:`WarningRecorder` được trả về. Danh sách cảnh báo bên dưới từ
   :func:`~warnings.catch_warnings` có thể được truy cập thông qua thuộc tính
   :attr:`warnings` của đối tượng recorder. Để thuận tiện, các thuộc tính của đối tượng biểu diễn cảnh báo gần đây nhất cũng có thể được truy cập trực tiếp thông qua đối tượng recorder (xem ví dụ bên dưới). Nếu chưa có cảnh báo nào được phát sinh, mọi thuộc tính vốn được mong đợi trên một đối tượng biểu diễn cảnh báo sẽ trả về ``None``.

   Đối tượng recorder cũng có một phương thức :meth:`reset`, dùng để xóa danh sách cảnh báo.

   Context manager được thiết kế để sử dụng như sau::

      with check_warnings(("assertion is always true", SyntaxWarning),
                          ("", UserWarning)):
          exec('assert(False, "Hey!")')
          warnings.warn(UserWarning("Hide me!"))

   Trong trường hợp này, nếu một trong hai cảnh báo không được phát sinh hoặc có một cảnh báo khác được phát sinh, :func:`check_warnings` sẽ phát sinh lỗi.

   Khi một bài kiểm thử cần xem xét sâu hơn các cảnh báo, thay vì chỉ kiểm tra xem chúng có xảy ra hay không, có thể sử dụng đoạn mã như sau::

      with check_warnings(quiet=True) as w:
          warnings.warn("foo")
          assert str(w.args[0]) == "foo"
          warnings.warn("bar")
          assert str(w.args[0]) == "bar"
          assert str(w.warnings[0].args[0]) == "foo"
          assert str(w.warnings[1].args[0]) == "bar"
          w.reset()
          assert len(w.warnings) == 0


   Tại đây, tất cả cảnh báo sẽ được bắt lại và mã kiểm thử sẽ kiểm tra trực tiếp các cảnh báo đã thu thập.

   .. versionchanged:: 3.2
      Các đối số tùy chọn mới *filters* và *quiet*.


.. class:: WarningsRecorder()

   Lớp được sử dụng để ghi lại các cảnh báo cho unit test. Xem tài liệu của
   :func:`check_warnings` ở trên để biết thêm chi tiết.

.. _`SetErrorMode`: https://msdn.microsoft.com/en-us/library/windows/desktop/ms680621.aspx
