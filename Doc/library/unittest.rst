:mod:`!unittest` --- Khung kiểm thử đơn vị
==========================================

.. module:: unittest
   :synopsis: Khung kiểm thử đơn vị cho Python.

.. moduleauthor:: Steve Purcell <stephen_purcell@yahoo.com>
.. sectionauthor:: Steve Purcell <stephen_purcell@yahoo.com>
.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>
.. sectionauthor:: Raymond Hettinger <python@rcn.com>

**Mã nguồn:** :source:`Lib/unittest/__init__.py`

--------------

(Nếu bạn đã quen với các khái niệm cơ bản về kiểm thử, bạn có thể chuyển đến :ref:`danh sách các phương thức assert <assert-methods>`.)

Khung kiểm thử đơn vị :mod:`!unittest` ban đầu lấy cảm hứng từ JUnit và có cách hoạt động tương tự các khung kiểm thử đơn vị phổ biến trong những ngôn ngữ khác. Khung này hỗ trợ tự động hóa kiểm thử, chia sẻ mã thiết lập và mã dọn dẹp cho các bài kiểm thử, tập hợp các bài kiểm thử thành các bộ sưu tập, đồng thời tách biệt các bài kiểm thử khỏi khung báo cáo.

Để đạt được điều này, :mod:`!unittest` hỗ trợ một số khái niệm quan trọng theo cách tiếp cận hướng đối tượng:

test fixture
   Một :dfn:`fixture kiểm thử` đại diện cho phần chuẩn bị cần thiết để thực hiện một hoặc nhiều bài kiểm thử, cùng với mọi tác vụ dọn dẹp liên quan. Việc này có thể bao gồm, chẳng hạn như, tạo cơ sở dữ liệu tạm thời hoặc proxy, tạo thư mục hoặc khởi động một tiến trình máy chủ.

trường hợp kiểm thử
   Một :dfn:`trường hợp kiểm thử` là đơn vị kiểm thử riêng lẻ. Nó kiểm tra một phản hồi cụ thể đối với một tập hợp đầu vào cụ thể. :mod:`!unittest` cung cấp một lớp cơ sở,
   :class:`TestCase`, có thể được sử dụng để tạo các trường hợp kiểm thử mới.

bộ kiểm thử
   Một :dfn:`bộ kiểm thử` là tập hợp các trường hợp kiểm thử, các bộ kiểm thử hoặc cả hai. Nó được dùng để tập hợp các bài kiểm thử cần được thực thi cùng nhau.

trình chạy kiểm thử
   :dfn:`Trình chạy kiểm thử` là một thành phần điều phối việc thực thi các bài kiểm thử và cung cấp kết quả cho người dùng. Trình chạy có thể sử dụng giao diện đồ họa, giao diện văn bản hoặc trả về một giá trị đặc biệt để cho biết kết quả thực thi các bài kiểm thử.

.. seealso::

   Mô-đun :mod:`doctest`
      Một mô-đun hỗ trợ kiểm thử khác với đặc điểm rất khác biệt.

   `Kiểm thử Smalltalk đơn giản: Với các mẫu <https://web.archive.org/web/20150315073817/http://www.xprogramming.com/testfram.htm>`_
      Bài viết gốc của Kent Beck về các framework kiểm thử sử dụng mẫu được chia sẻ bởi :mod:`!unittest`.

   `pytest <https://docs.pytest.org/>`_
      Framework unittest của bên thứ ba với cú pháp gọn nhẹ hơn để viết các bài kiểm thử. Ví dụ: ``assert func(10) == 42``.

   `Phân loại các công cụ kiểm thử Python <https://wiki.python.org/moin/PythonTestingToolsTaxonomy>`_
      Danh sách phong phú các công cụ kiểm thử Python, bao gồm các framework kiểm thử chức năng và thư viện mock object.

   `Danh sách gửi thư Testing in Python <http://lists.idyll.org/listinfo/testing-in-python>`_
      Một nhóm chuyên quan tâm để thảo luận về việc kiểm thử và các công cụ kiểm thử trong Python.

   Script :file:`Tools/unittestgui/unittestgui.py` trong bản phân phối mã nguồn Python là một công cụ GUI để phát hiện và thực thi kiểm thử. Công cụ này chủ yếu nhằm giúp những người mới làm quen với unit testing dễ sử dụng hơn. Trong môi trường production, bạn nên chạy các bài kiểm thử bằng một hệ thống tích hợp liên tục như `Buildbot <https://buildbot.net/>`_, `Jenkins <https://www.jenkins.io/>`_, `GitHub Actions <https://github.com/features/actions>`_ hoặc `AppVeyor <https://www.appveyor.com/>`_.


.. _unittest-minimal-example:

Ví dụ cơ bản
------------

Module :mod:`!unittest` cung cấp một bộ công cụ phong phú để xây dựng và chạy các bài kiểm thử. Phần này minh họa rằng một tập hợp nhỏ các công cụ cũng đủ đáp ứng nhu cầu của hầu hết người dùng.

Sau đây là một script ngắn để kiểm thử ba phương thức xử lý chuỗi::

  import unittest

  class TestStringMethods(unittest.TestCase):

      def test_upper(self):
          self.assertEqual('foo'.upper(), 'FOO')

      def test_isupper(self):
          self.assertTrue('FOO'.isupper())
          self.assertFalse('Foo'.isupper())

      def test_split(self):
          s = 'hello world'
          self.assertEqual(s.split(), ['hello', 'world'])
          # kiểm tra rằng s.split không thành công khi dấu phân tách không phải là một chuỗi
          with self.assertRaises(TypeError):
              s.split(2)

  if __name__ == '__main__':
      unittest.main()


Một trường hợp kiểm thử được tạo bằng cách phân lớp :class:`unittest.TestCase`. Ba bài kiểm thử riêng lẻ được định nghĩa bằng các phương thức có tên bắt đầu bằng các chữ cái ``test``. Quy ước đặt tên này cho test runner biết những phương thức nào đại diện cho các bài kiểm thử.

Cốt lõi của mỗi bài kiểm thử là một lệnh gọi đến :meth:`~TestCase.assertEqual` để kiểm tra kết quả mong đợi; :meth:`~TestCase.assertTrue` hoặc :meth:`~TestCase.assertFalse` để xác minh một điều kiện; hoặc :meth:`~TestCase.assertRaises` để xác minh rằng một exception cụ thể được phát sinh. Các phương thức này được sử dụng thay cho
câu lệnh :keyword:`assert` để test runner có thể tập hợp tất cả kết quả kiểm thử và tạo báo cáo.

Các phương thức :meth:`~TestCase.setUp` và :meth:`~TestCase.tearDown` cho phép bạn định nghĩa những chỉ dẫn sẽ được thực thi trước và sau mỗi phương thức kiểm thử. Chúng được trình bày chi tiết hơn trong phần :ref:`organizing-tests`.

Khối cuối cùng trình bày một cách đơn giản để chạy các bài kiểm thử. :func:`unittest.main` cung cấp giao diện dòng lệnh cho script kiểm thử. Khi được chạy từ dòng lệnh, script ở trên tạo ra kết quả có dạng như sau::

   ...
   ----------------------------------------------------------------------
   Ran 3 tests in 0.000s

   OK

Việc truyền tùy chọn ``-v`` vào test script sẽ hướng dẫn :func:`unittest.main` bật mức độ chi tiết cao hơn và tạo ra kết quả sau đây::

   test_isupper (__main__.TestStringMethods.test_isupper) ... ok
   test_split (__main__.TestStringMethods.test_split) ... ok
   test_upper (__main__.TestStringMethods.test_upper) ... ok

   ----------------------------------------------------------------------
   Ran 3 tests in 0.001s

   OK

Các ví dụ trên minh họa những tính năng :mod:`!unittest` được sử dụng phổ biến nhất, đủ để đáp ứng nhiều nhu cầu kiểm thử hằng ngày. Phần còn lại của tài liệu sẽ tìm hiểu toàn bộ tập tính năng từ những nguyên tắc cơ bản.

.. versionchanged:: 3.11
   Hành vi trả về một giá trị từ phương thức kiểm thử (khác với giá trị ``None`` mặc định) hiện đã không còn được khuyến nghị.


.. _unittest-command-line-interface:

Giao diện dòng lệnh
-------------------

Có thể sử dụng module unittest từ dòng lệnh để chạy các bài kiểm thử từ module, class hoặc thậm chí từng phương thức kiểm thử riêng lẻ::

   python -m unittest test_module1 test_module2
   python -m unittest test_module.TestClass
   python -m unittest test_module.TestClass.test_method

Bạn có thể truyền vào một danh sách chứa bất kỳ tổ hợp nào của tên module và tên class hoặc phương thức đầy đủ.

Các module kiểm thử cũng có thể được chỉ định bằng đường dẫn tệp::

   python -m unittest tests/test_something.py

Điều này cho phép bạn sử dụng tính năng hoàn thành tên tệp của shell để chỉ định test module. Tệp được chỉ định vẫn phải có thể được import dưới dạng module. Đường dẫn được chuyển đổi thành tên module bằng cách loại bỏ '.py' và chuyển các dấu phân cách trong đường dẫn thành '.'. Nếu muốn thực thi một tệp test không thể import dưới dạng module, bạn nên thực thi trực tiếp tệp đó.

Bạn có thể chạy các test với nhiều thông tin chi tiết hơn (độ chi tiết cao hơn) bằng cách truyền vào cờ -v::

   python -m unittest -v test_module

Khi được thực thi mà không có đối số, :ref:`unittest-test-discovery` sẽ được khởi động::

   python -m unittest

Để xem danh sách tất cả các tùy chọn dòng lệnh::

   python -m unittest -h

.. versionchanged:: 3.2
   Trong các phiên bản trước, bạn chỉ có thể chạy từng phương thức test riêng lẻ, không thể chạy module hoặc class.

.. versionadded:: 3.14
   Theo mặc định, đầu ra được tô màu và có thể được
   :ref:`điều khiển bằng các biến môi trường <using-on-controlling-color>`.

.. _`Command-line options`:

Các tùy chọn dòng lệnh
~~~~~~~~~~~~~~~~~~~~~~

:program:`unittest` hỗ trợ các tùy chọn dòng lệnh sau:

.. program:: unittest

.. option:: -b, --buffer

   Các stream đầu ra tiêu chuẩn và lỗi tiêu chuẩn được đệm trong quá trình chạy kiểm thử. Đầu ra trong một kiểm thử thành công sẽ bị loại bỏ. Đầu ra được hiển thị bình thường khi kiểm thử thất bại hoặc xảy ra lỗi, đồng thời được thêm vào các thông báo lỗi.

.. option:: -c, --catch

   :kbd:`Control-C` trong quá trình chạy kiểm thử sẽ chờ kiểm thử hiện tại kết thúc, sau đó báo cáo tất cả kết quả cho đến thời điểm đó. Nhấn :kbd:`Control-C` lần thứ hai sẽ đưa ra ngoại lệ thông thường
   :exc:`KeyboardInterrupt`.

   Xem `Signal Handling <Signal Handling_>`_ để biết các hàm cung cấp chức năng này.

.. option:: -f, --failfast

   Dừng quá trình chạy kiểm thử ngay khi gặp lỗi hoặc thất bại đầu tiên.

.. option:: -k

   Chỉ chạy các phương thức và lớp kiểm thử khớp với mẫu hoặc chuỗi con. Tùy chọn này có thể được sử dụng nhiều lần; khi đó, tất cả các trường hợp kiểm thử khớp với bất kỳ mẫu nào đã cho đều được đưa vào.

   Các mẫu chứa ký tự đại diện (``*``) được đối chiếu với tên kiểm thử bằng :meth:`fnmatch.fnmatchcase`; nếu không, phép đối chiếu chuỗi con phân biệt chữ hoa chữ thường đơn giản sẽ được sử dụng.

   Các mẫu được đối chiếu với tên phương thức kiểm thử đầy đủ (fully qualified) như được test loader nhập vào.

   Ví dụ, ``-k foo`` khớp với ``foo_tests.SomeTest.test_something``, ``bar_tests.SomeTest.test_foo``, nhưng không khớp với ``bar_tests.FooTest.test_something``.

.. option:: --locals

   Hiển thị các biến cục bộ trong traceback.

.. option:: --durations N

   Hiển thị N trường hợp kiểm thử chạy chậm nhất (N=0 để hiển thị tất cả).

.. versionadded:: 3.2
   Các tùy chọn dòng lệnh ``-b``, ``-c`` và ``-f`` đã được thêm vào.

.. versionadded:: 3.5
   Tùy chọn dòng lệnh ``--locals``.

.. versionadded:: 3.7
   Tùy chọn dòng lệnh ``-k``.

.. versionadded:: 3.12
   Tùy chọn dòng lệnh ``--durations``.

Dòng lệnh cũng có thể được dùng để discovery test, chạy tất cả các test trong một project hoặc chỉ một tập hợp con.

.. _unittest-test-discovery:

Discovery test
--------------

.. versionadded:: 3.2

Unittest hỗ trợ discovery test đơn giản. Để tương thích với discovery test, tất cả các tệp test phải là :ref:`modules <tut-modules>` hoặc
:ref:`packages <tut-packages>` có thể import từ thư mục cấp cao nhất của project (điều này có nghĩa là tên tệp của chúng phải là các :ref:`identifiers <identifiers>` hợp lệ).

Tính năng phát hiện test được triển khai trong :meth:`TestLoader.discover`, nhưng cũng có thể được sử dụng từ dòng lệnh. Cách sử dụng cơ bản trên dòng lệnh là::

   cd project_directory
   python -m unittest discover

.. note::

   Dưới dạng viết tắt, ``python -m unittest`` tương đương với ``python -m unittest discover``. Nếu muốn truyền đối số cho quá trình phát hiện test, phải sử dụng rõ ràng tiểu lệnh ``discover``.

Tiểu lệnh ``discover`` có các tùy chọn sau:

.. program:: unittest discover

.. option:: -v, --verbose

   Đầu ra chi tiết

.. option:: -s, --start-directory directory

   Thư mục bắt đầu quá trình phát hiện (``.`` theo mặc định)

.. option:: -p, --pattern pattern

   Mẫu khớp với các tệp test (``test*.py`` theo mặc định)

.. option:: -t, --top-level-directory directory

   Thư mục cấp cao nhất của dự án (mặc định là thư mục bắt đầu)

Các tùy chọn :option:`-s`, :option:`-p` và :option:`-t` có thể được truyền dưới dạng các đối số vị trí theo thứ tự đó. Hai dòng lệnh sau tương đương::

   python -m unittest discover -s project_directory -p "*_test.py"
   python -m unittest discover project_directory "*_test.py"

Ngoài đường dẫn, bạn cũng có thể truyền tên package, chẳng hạn như ``myproject.subpackage.test``, làm thư mục bắt đầu. Tên package bạn cung cấp sau đó sẽ được import và vị trí của nó trên hệ thống tệp sẽ được dùng làm thư mục bắt đầu.

.. caution::

    Test discovery tải các test bằng cách import chúng. Sau khi test discovery tìm thấy tất cả các tệp test từ thư mục bắt đầu mà bạn chỉ định, nó chuyển đổi các đường dẫn thành tên package để import. Ví dụ: :file:`foo/bar/baz.py` sẽ được import dưới tên ``foo.bar.baz``.

    Nếu bạn đã cài đặt một package trên toàn hệ thống và cố gắng thực hiện test discovery trên một bản sao khác của package đó, thao tác import *có thể* diễn ra từ sai vị trí. Nếu điều này xảy ra, test discovery sẽ cảnh báo bạn rồi thoát.

    Nếu bạn cung cấp thư mục bắt đầu dưới dạng tên package thay vì đường dẫn đến một thư mục, discover sẽ giả định rằng bất kỳ vị trí nào mà nó import từ đó đều là vị trí bạn mong muốn, vì vậy bạn sẽ không nhận được cảnh báo.

Các module và package test có thể tùy chỉnh việc tải và test discovery thông qua `load_tests protocol <load_tests protocol_>`_.

.. versionchanged:: 3.4
   Test discovery hỗ trợ :term:`namespace packages <namespace package>`.

.. versionchanged:: 3.11
   Tính năng phát hiện test đã loại bỏ hỗ trợ cho các :term:`namespace package <namespace package>`. Tính năng này đã bị hỏng kể từ Python 3.7. Thư mục bắt đầu và các thư mục con chứa test phải là package thông thường có tệp ``__init__.py``.

   Nếu thư mục bắt đầu là tên có dấu chấm của package, các package tổ tiên có thể là namespace package.

.. versionchanged:: 3.14
   Tính năng phát hiện test một lần nữa hỗ trợ :term:`namespace package` làm thư mục bắt đầu. Để tránh quét các thư mục không liên quan đến Python, test sẽ không được tìm kiếm trong các thư mục con không chứa ``__init__.py``.


.. _organizing-tests:

Tổ chức mã test
---------------

Các khối xây dựng cơ bản của unit testing là các :dfn:`test case` --- những kịch bản riêng lẻ cần được thiết lập và kiểm tra tính chính xác. Trong :mod:`!unittest`, test case được biểu diễn bằng các instance :class:`unittest.TestCase`. Để tự tạo test case, bạn phải viết các lớp con của
:class:`TestCase` hoặc sử dụng :class:`FunctionTestCase`.

Mã test của một instance :class:`TestCase` phải hoàn toàn độc lập, sao cho có thể chạy riêng lẻ hoặc kết hợp tùy ý với bất kỳ số lượng test case nào khác.

Lớp con :class:`TestCase` đơn giản nhất sẽ chỉ triển khai một phương thức kiểm thử (tức là phương thức có tên bắt đầu bằng ``test``) để thực hiện mã kiểm thử cụ thể::

   import unittest

   class DefaultWidgetSizeTestCase(unittest.TestCase):
       def test_default_widget_size(self):
           widget = Widget('The widget')
           self.assertEqual(widget.size(), (50, 50))

Lưu ý rằng để kiểm thử một điều gì đó, chúng ta sử dụng một trong các phương thức :ref:`assert\*methods <assert-methods>` do lớp cơ sở :class:`TestCase` cung cấp. Nếu kiểm thử thất bại, một ngoại lệ sẽ được phát sinh kèm theo thông báo giải thích, và :mod:`!unittest` sẽ xác định trường hợp kiểm thử là một :dfn:`failure`. Mọi ngoại lệ khác sẽ được xử lý như :dfn:`errors`.

Các bài kiểm thử có thể rất nhiều, và việc thiết lập chúng có thể lặp đi lặp lại. May mắn là chúng ta có thể tách riêng mã thiết lập bằng cách triển khai một phương thức có tên
:meth:`~TestCase.setUp`, mà framework kiểm thử sẽ tự động gọi cho từng bài kiểm thử mà chúng ta chạy::

   import unittest

   class WidgetTestCase(unittest.TestCase):
       def setUp(self):
           self.widget = Widget('The widget')

       def test_default_widget_size(self):
           self.assertEqual(self.widget.size(), (50,50),
                            'incorrect default size')

       def test_widget_resize(self):
           self.widget.resize(100,150)
           self.assertEqual(self.widget.size(), (100,150),
                            'wrong size after resize')

.. note::
   Thứ tự chạy các bài kiểm thử khác nhau được xác định bằng cách sắp xếp tên các phương thức kiểm thử theo thứ tự dựng sẵn dành cho chuỗi.

Nếu phương thức :meth:`~TestCase.setUp` phát sinh ngoại lệ trong khi bài kiểm thử đang chạy, framework sẽ coi bài kiểm thử đã gặp lỗi và phương thức kiểm thử sẽ không được thực thi.

Tương tự, chúng ta có thể cung cấp một phương thức :meth:`~TestCase.tearDown` để dọn dẹp sau khi phương thức kiểm thử đã được chạy::

   import unittest

   class WidgetTestCase(unittest.TestCase):
       def setUp(self):
           self.widget = Widget('The widget')

       def tearDown(self):
           self.widget.dispose()

Nếu :meth:`~TestCase.setUp` thành công, :meth:`~TestCase.tearDown` sẽ được chạy bất kể phương thức kiểm thử có thành công hay không.

Môi trường làm việc như vậy cho mã kiểm thử được gọi là
:dfn:`test fixture`. Một đối tượng TestCase mới được tạo dưới dạng một test fixture riêng biệt, dùng để thực thi từng phương thức kiểm thử. Do đó
:meth:`~TestCase.setUp`, :meth:`~TestCase.tearDown` và :meth:`!TestCase.__init__` sẽ được gọi một lần cho mỗi kiểm thử.

Bạn nên sử dụng các triển khai TestCase để nhóm các kiểm thử theo những tính năng mà chúng kiểm thử. :mod:`!unittest` cung cấp một cơ chế cho việc này: :dfn:`test suite`, được biểu diễn bởi :mod:`!unittest`'s
:class:`TestSuite` class. Trong hầu hết các trường hợp, gọi :func:`unittest.main` sẽ thực hiện đúng việc cần làm, tự động tập hợp tất cả test case của mô-đun và thực thi chúng.

Tuy nhiên, nếu muốn tùy chỉnh việc xây dựng test suite, bạn có thể tự thực hiện::

   def suite():
       suite = unittest.TestSuite()
       suite.addTest(WidgetTestCase('test_default_widget_size'))
       suite.addTest(WidgetTestCase('test_widget_resize'))
       return suite

   if __name__ == '__main__':
       runner = unittest.TextTestRunner()
       runner.run(suite())

Bạn có thể đặt định nghĩa của các test case và test suite trong cùng module với mã mà chúng sẽ kiểm thử (chẳng hạn như :file:`widget.py`), nhưng việc đặt mã kiểm thử trong một module riêng có một số ưu điểm, chẳng hạn như
:file:`test_widget.py`:

* Có thể chạy module kiểm thử độc lập từ dòng lệnh.

* Mã kiểm thử có thể được tách khỏi mã được phát hành dễ dàng hơn.

* Ít có khả năng bạn muốn thay đổi mã kiểm thử để phù hợp với mã mà nó kiểm thử nếu không có lý do chính đáng.

* Mã kiểm thử nên được sửa đổi ít thường xuyên hơn nhiều so với mã mà nó kiểm thử.

* Mã được kiểm thử có thể được refactor dễ dàng hơn.

* Các test dành cho module được viết bằng C ohnehin phải nằm trong các module riêng, vậy tại sao không nhất quán?

* Nếu chiến lược kiểm thử thay đổi, bạn không cần thay đổi mã nguồn.


.. _legacy-unit-tests:

Tái sử dụng mã kiểm thử cũ
--------------------------

Một số người dùng sẽ nhận thấy rằng họ có mã kiểm thử hiện có mà họ muốn chạy từ :mod:`!unittest`, mà không cần chuyển đổi mọi hàm kiểm thử cũ thành một
lớp con :class:`TestCase`.

Vì lý do này, :mod:`!unittest` cung cấp một lớp :class:`FunctionTestCase`. Lớp con này của :class:`TestCase` có thể được dùng để bọc một hàm kiểm thử hiện có. Bạn cũng có thể cung cấp các hàm set-up và tear-down.

Với hàm kiểm thử sau đây::

   def testSomething():
       something = makeSomething()
       assert something.name is not None
       # ...

ta có thể tạo một thực thể test case tương đương như sau, kèm theo các phương thức set-up và tear-down tùy chọn::

   testcase = unittest.FunctionTestCase(testSomething,
                                        setUp=makeSomethingDB,
                                        tearDown=deleteSomethingDB)

.. note::

   Mặc dù :class:`FunctionTestCase` có thể được dùng để nhanh chóng chuyển một bộ kiểm thử hiện có sang hệ thống dựa trên :mod:`!unittest`\ , cách tiếp cận này không được khuyến nghị. Dành thời gian thiết lập các lớp con :class:`TestCase` phù hợp sẽ giúp việc tái cấu trúc kiểm thử sau này dễ dàng hơn rất nhiều.

Trong một số trường hợp, các kiểm thử hiện có có thể được viết bằng module :mod:`doctest`. Nếu vậy, :mod:`doctest` cung cấp một lớp :class:`~doctest.DocTestSuite` có thể tự động xây dựng các thực thể :class:`unittest.TestSuite` từ các kiểm thử hiện có
dựa trên :mod:`doctest`\ .


.. _unittest-skipping:

Bỏ qua kiểm thử và các lỗi dự kiến
----------------------------------

.. versionadded:: 3.1

Unittest hỗ trợ bỏ qua từng phương thức kiểm thử riêng lẻ và thậm chí cả những lớp kiểm thử. Ngoài ra, nó còn hỗ trợ đánh dấu một kiểm thử là "lỗi dự kiến"—một kiểm thử bị hỏng và sẽ thất bại, nhưng không nên được tính là một lỗi trên một
:class:`TestResult`.

Việc bỏ qua một kiểm thử chỉ đơn giản là sử dụng :deco:`skip` :term:`decorator` hoặc một biến thể có điều kiện của nó, gọi :meth:`TestCase.skipTest` bên trong một
:meth:`~TestCase.setUp` hoặc phương thức kiểm thử, hoặc trực tiếp phát sinh :exc:`SkipTest`.

Bỏ qua cơ bản trông như sau::

   class MyTestCase(unittest.TestCase):

       @unittest.skip("demonstrating skipping")
       def test_nothing(self):
           self.fail("shouldn't happen")

       @unittest.skipIf(mylib.__version__ < (1, 3),
                        "not supported in this library version")
       def test_format(self):
           # Các test chỉ hoạt động với một phiên bản cụ thể của thư viện.
           pass

       @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
       def test_windows_support(self):
           # mã kiểm thử dành riêng cho Windows
           pass

       def test_maybe_skipped(self):
           if not external_resource_available():
               self.skipTest("external resource not available")
           # mã kiểm thử phụ thuộc vào tài nguyên bên ngoài
           pass

Đây là kết quả khi chạy ví dụ trên ở chế độ verbose::

   test_format (__main__.MyTestCase.test_format) ... skipped 'not supported in this library version'
   test_nothing (__main__.MyTestCase.test_nothing) ... skipped 'demonstrating skipping'
   test_maybe_skipped (__main__.MyTestCase.test_maybe_skipped) ... skipped 'external resource not available'
   test_windows_support (__main__.MyTestCase.test_windows_support) ... skipped 'requires Windows'

   ----------------------------------------------------------------------
   Ran 4 tests in 0.005s

   OK (skipped=4)

Có thể bỏ qua các class giống như các method::

   @unittest.skip("showing class skipping")
   class MySkippedTestCase(unittest.TestCase):
       def test_not_run(self):
           pass

:meth:`TestCase.setUp` cũng có thể bỏ qua test. Điều này hữu ích khi không có tài nguyên cần thiết lập.

Các lỗi dự kiến sử dụng decorator :deco:`expectedFailure`.::

   class ExpectedFailureTestCase(unittest.TestCase):
       @unittest.expectedFailure
       def test_fail(self):
           self.assertEqual(1, 0, "broken")

Bạn có thể dễ dàng tự tạo các decorator để bỏ qua bằng cách tạo một decorator gọi
:func:`skip` trên bài kiểm thử khi muốn bỏ qua bài kiểm thử đó. Decorator này bỏ qua bài kiểm thử trừ khi đối tượng được truyền vào có một thuộc tính nhất định::

   def skipUnlessHasattr(obj, attr):
       if hasattr(obj, attr):
           return lambda func: func
       return unittest.skip("{!r} doesn't have {!r}".format(obj, attr))

Các decorator và exception sau đây triển khai chức năng bỏ qua bài kiểm thử và các lỗi dự kiến:

.. decorator:: skip(reason)

   Luôn bỏ qua bài kiểm thử được áp dụng decorator. *reason* nên mô tả lý do bài kiểm thử bị bỏ qua.

.. decorator:: skipIf(condition, reason)

   Bỏ qua bài kiểm thử được áp dụng decorator nếu *condition* là true.

.. decorator:: skipUnless(condition, reason)

   Bỏ qua bài kiểm thử được áp dụng decorator trừ khi *condition* là true.

.. decorator:: expectedFailure

   Đánh dấu test là một lỗi hoặc thất bại được dự kiến. Nếu test thất bại hoặc xảy ra lỗi ngay trong hàm test (thay vì trong một trong các phương thức :dfn:`test fixture`) thì test sẽ được xem là thành công. Nếu test chạy thành công, test sẽ được xem là thất bại.

.. exception:: SkipTest(reason)

   Ngoại lệ này được đưa ra để bỏ qua một test.

   Thông thường, bạn có thể sử dụng :meth:`TestCase.skipTest` hoặc một trong các decorator bỏ qua thay vì trực tiếp đưa ra ngoại lệ này.

Các test bị bỏ qua sẽ không chạy :meth:`~TestCase.setUp` hoặc :meth:`~TestCase.tearDown` xung quanh chúng. Các lớp bị bỏ qua sẽ không chạy :meth:`~TestCase.setUpClass` hoặc :meth:`~TestCase.tearDownClass`. Các module bị bỏ qua sẽ không chạy :func:`setUpModule` hoặc :func:`tearDownModule`.


.. _subtests:

Phân biệt các lần lặp test bằng subtest
---------------------------------------

.. versionadded:: 3.4

Khi các test của bạn chỉ khác nhau ở một vài điểm rất nhỏ, chẳng hạn như một số tham số, unittest cho phép bạn phân biệt chúng bên trong phần thân của một phương thức test bằng context manager :meth:`~TestCase.subTest`.

Ví dụ, test sau đây::

   class NumbersTest(unittest.TestCase):

       def test_even(self):
           """
           Test that numbers between 0 and 5 are all even.
           """
           for i in range(0, 6):
               with self.subTest(i=i):
                   self.assertEqual(i % 2, 0)

sẽ tạo ra kết quả sau::

   ======================================================================
   FAIL: test_even (__main__.NumbersTest.test_even) (i=1)
   Test that numbers between 0 and 5 are all even.
   ----------------------------------------------------------------------
   Traceback (most recent call last):
     File "subtests.py", line 11, in test_even
       self.assertEqual(i % 2, 0)
       ^^^^^^^^^^^^^^^^^^^^^^^^^^
   AssertionError: 1 != 0

   ======================================================================
   FAIL: test_even (__main__.NumbersTest.test_even) (i=3)
   Test that numbers between 0 and 5 are all even.
   ----------------------------------------------------------------------
   Traceback (most recent call last):
     File "subtests.py", line 11, in test_even
       self.assertEqual(i % 2, 0)
       ^^^^^^^^^^^^^^^^^^^^^^^^^^
   AssertionError: 1 != 0

   ======================================================================
   FAIL: test_even (__main__.NumbersTest.test_even) (i=5)
   Test that numbers between 0 and 5 are all even.
   ----------------------------------------------------------------------
   Traceback (most recent call last):
     File "subtests.py", line 11, in test_even
       self.assertEqual(i % 2, 0)
       ^^^^^^^^^^^^^^^^^^^^^^^^^^
   AssertionError: 1 != 0

Nếu không sử dụng subtest, quá trình thực thi sẽ dừng sau lỗi đầu tiên, và lỗi sẽ khó chẩn đoán hơn vì giá trị của ``i`` sẽ không được hiển thị::

   ======================================================================
   FAIL: test_even (__main__.NumbersTest.test_even)
   ----------------------------------------------------------------------
   Traceback (most recent call last):
     File "subtests.py", line 32, in test_even
       self.assertEqual(i % 2, 0)
   AssertionError: 1 != 0


.. _unittest-contents:

Các lớp và hàm
--------------

Phần này mô tả chi tiết API của :mod:`!unittest`.


.. _testcase-objects:

Các test case
~~~~~~~~~~~~~

.. class:: TestCase(methodName='runTest')

   Các instance của lớp :class:`TestCase` đại diện cho các đơn vị kiểm thử logic trong hệ sinh thái :mod:`!unittest`. Lớp này được thiết kế để sử dụng làm lớp cơ sở, trong đó các kiểm thử cụ thể được triển khai bởi các lớp con cụ thể. Lớp này triển khai interface cần thiết để test runner điều khiển các kiểm thử, cùng với các phương thức mà mã kiểm thử có thể sử dụng để kiểm tra và báo cáo nhiều loại lỗi khác nhau.

   Mỗi instance của :class:`TestCase` sẽ chạy một phương thức cơ sở duy nhất: phương thức có tên *methodName*. Trong hầu hết trường hợp sử dụng :class:`TestCase`, bạn sẽ không thay đổi *methodName* cũng như triển khai lại phương thức mặc định ``runTest()``.

   .. versionchanged:: 3.2
      :class:`TestCase` can be instantiated successfully without providing a
      *methodName*. Điều này giúp việc thử nghiệm với :class:`TestCase` từ trình thông dịch tương tác trở nên dễ dàng hơn.

   Các instance :class:`TestCase` cung cấp ba nhóm phương thức: một nhóm dùng để chạy kiểm thử, một nhóm khác được phần triển khai kiểm thử sử dụng để kiểm tra các điều kiện và báo cáo lỗi, cùng một số phương thức truy vấn cho phép thu thập thông tin về chính bài kiểm thử.

   Các phương thức trong nhóm đầu tiên (chạy kiểm thử) là:

   .. method:: setUp()

      Phương thức được gọi để chuẩn bị test fixture. Phương thức này được gọi ngay trước khi gọi phương thức kiểm thử; ngoài :exc:`AssertionError` hoặc :exc:`SkipTest`, mọi ngoại lệ do phương thức này phát sinh sẽ được xem là lỗi thay vì một lần kiểm thử thất bại. Phần triển khai mặc định không thực hiện gì.


   .. method:: tearDown()

      Phương thức được gọi ngay sau khi phương thức kiểm thử được gọi và kết quả được ghi lại. Phương thức này vẫn được gọi ngay cả khi phương thức kiểm thử phát sinh ngoại lệ, vì vậy phần triển khai trong các lớp con có thể cần đặc biệt cẩn thận khi kiểm tra trạng thái nội bộ. Mọi ngoại lệ, ngoại trừ
      :exc:`AssertionError` hoặc :exc:`SkipTest`, do phương thức này phát sinh sẽ được xem là một lỗi bổ sung thay vì một lần kiểm thử thất bại (do đó làm tăng tổng số lỗi được báo cáo). Phương thức này chỉ được gọi nếu :meth:`setUp` thành công, bất kể kết quả của phương thức kiểm thử. Phần triển khai mặc định không thực hiện gì.


   .. method:: setUpClass()

      Một class method được gọi trước khi các bài kiểm thử trong một lớp riêng lẻ được chạy. ``setUpClass`` được gọi với lớp đó là đối số duy nhất và phải được đánh dấu là một :deco:`classmethod`::

        @classmethod
        def setUpClass(cls):
            ...

      Xem `Class and Module Fixtures <Class and Module Fixtures_>`_ để biết thêm chi tiết.

      .. versionadded:: 3.2


   .. method:: tearDownClass()

      Một class method được gọi sau khi các test trong một class riêng lẻ đã chạy xong. ``tearDownClass`` được gọi với class là đối số duy nhất và phải được trang trí bằng :deco:`classmethod`::

        @classmethod
        def tearDownClass(cls):
            ...

      Xem `Class and Module Fixtures <Class and Module Fixtures_>`_ để biết thêm chi tiết.

      .. versionadded:: 3.2


   .. method:: run(result=None)

      Chạy test, lưu kết quả vào đối tượng :class:`TestResult` được truyền dưới dạng *result*. Nếu *result* bị bỏ qua hoặc là ``None``, một đối tượng kết quả tạm thời sẽ được tạo (bằng cách gọi method :meth:`defaultTestResult`) và được sử dụng. Đối tượng kết quả được trả về cho bên gọi :meth:`run`.

      Có thể đạt được hiệu ứng tương tự bằng cách פשוט gọi instance :class:`TestCase`.

      .. versionchanged:: 3.3
         Các phiên bản trước của ``run`` không trả về kết quả. Việc gọi một instance cũng vậy.

   .. method:: skipTest(reason)

      Việc gọi hàm này trong một test method hoặc :meth:`setUp` sẽ bỏ qua test hiện tại. Xem :ref:`unittest-skipping` để biết thêm thông tin.

      .. versionadded:: 3.1


   .. method:: subTest(msg=None, **params)

      Trả về một context manager thực thi khối mã được bao quanh dưới dạng một subtest. *msg* và *params* là các giá trị tùy ý, không bắt buộc; chúng được hiển thị mỗi khi một subtest thất bại, giúp bạn xác định rõ subtest đó.

      Một test case có thể chứa bất kỳ số lượng khai báo subtest nào và chúng có thể được lồng nhau tùy ý.

      Xem :ref:`subtests` để biết thêm thông tin.

      .. versionadded:: 3.4


   .. method:: debug()

      Chạy test mà không thu thập kết quả. Điều này cho phép các ngoại lệ do test phát sinh được truyền đến caller và có thể được dùng để hỗ trợ chạy test dưới debugger.

   .. _assert-methods:

   Lớp :class:`TestCase` cung cấp một số phương thức assert để kiểm tra và báo cáo lỗi. Bảng sau liệt kê các phương thức thường được sử dụng nhất (xem các bảng bên dưới để biết thêm các phương thức assert):

   +-----------------------------------------+-----------------------------+---------------+
   | Method                                  | Checks that                 | New in        |
   +=========================================+=============================+===============+
   | :meth:`assertEqual(a, b)                | ``a == b``                  |               |
   | <TestCase.assertEqual>`                 |                             |               |
   +-----------------------------------------+-----------------------------+---------------+
   | :meth:`assertNotEqual(a, b)             | ``a != b``                  |               |
   | <TestCase.assertNotEqual>`              |                             |               |
   +-----------------------------------------+-----------------------------+---------------+
   | :meth:`assertTrue(x)                    | ``bool(x) is True``         |               |
   | <TestCase.assertTrue>`                  |                             |               |
   +-----------------------------------------+-----------------------------+---------------+
   | :meth:`assertFalse(x)                   | ``bool(x) is False``        |               |
   | <TestCase.assertFalse>`                 |                             |               |
   +-----------------------------------------+-----------------------------+---------------+
   | :meth:`assertIs(a, b)                   | ``a is b``                  | 3.1           |
   | <TestCase.assertIs>`                    |                             |               |
   +-----------------------------------------+-----------------------------+---------------+
   | :meth:`assertIsNot(a, b)                | ``a is not b``              | 3.1           |
   | <TestCase.assertIsNot>`                 |                             |               |
   +-----------------------------------------+-----------------------------+---------------+
   | :meth:`assertIsNone(x)                  | ``x is None``               | 3.1           |
   | <TestCase.assertIsNone>`                |                             |               |
   +-----------------------------------------+-----------------------------+---------------+
   | :meth:`assertIsNotNone(x)               | ``x is not None``           | 3.1           |
   | <TestCase.assertIsNotNone>`             |                             |               |
   +-----------------------------------------+-----------------------------+---------------+
   | :meth:`assertIn(a, b)                   | ``a in b``                  | 3.1           |
   | <TestCase.assertIn>`                    |                             |               |
   +-----------------------------------------+-----------------------------+---------------+
   | :meth:`assertNotIn(a, b)                | ``a not in b``              | 3.1           |
   | <TestCase.assertNotIn>`                 |                             |               |
   +-----------------------------------------+-----------------------------+---------------+
   | :meth:`assertIsInstance(a, b)           | ``isinstance(a, b)``        | 3.2           |
   | <TestCase.assertIsInstance>`            |                             |               |
   +-----------------------------------------+-----------------------------+---------------+
   | :meth:`assertNotIsInstance(a, b)        | ``not isinstance(a, b)``    | 3.2           |
   | <TestCase.assertNotIsInstance>`         |                             |               |
   +-----------------------------------------+-----------------------------+---------------+
   | :meth:`assertIsSubclass(a, b)           | ``issubclass(a, b)``        | 3.14          |
   | <TestCase.assertIsSubclass>`            |                             |               |
   +-----------------------------------------+-----------------------------+---------------+
   | :meth:`assertNotIsSubclass(a, b)        | ``not issubclass(a, b)``    | 3.14          |
   | <TestCase.assertNotIsSubclass>`         |                             |               |
   +-----------------------------------------+-----------------------------+---------------+

   Tất cả các phương thức assert đều chấp nhận đối số *msg*, đối số này nếu được chỉ định sẽ được dùng làm thông báo lỗi khi thất bại (xem thêm :data:`longMessage`). Lưu ý rằng đối số từ khóa *msg* có thể được truyền cho :meth:`assertRaises`,
   :meth:`assertRaisesRegex`, :meth:`assertWarns`, :meth:`assertWarnsRegex` chỉ khi chúng được sử dụng dưới dạng context manager.

   .. method:: assertEqual(first, second, msg=None)

      Kiểm tra xem *first* và *second* có bằng nhau không. Nếu các giá trị không bằng nhau, phép kiểm tra sẽ thất bại.

      Ngoài ra, nếu *first* và *second* có cùng chính xác một kiểu và kiểu đó là một trong các kiểu list, tuple, dict, set, frozenset hoặc str, hoặc bất kỳ kiểu nào mà một lớp con đăng ký với :meth:`addTypeEqualityFunc`, hàm so sánh bằng dành riêng cho kiểu sẽ được gọi để tạo thông báo lỗi mặc định hữu ích hơn (xem thêm :ref:`danh sách các phương thức dành riêng cho từng kiểu <type-specific-methods>`).

      .. versionchanged:: 3.1
         Đã bổ sung việc tự động gọi hàm so sánh bằng dành riêng cho kiểu.

      .. versionchanged:: 3.2
         :meth:`assertMultiLineEqual` added as the default type equality
         hàm dùng để so sánh các chuỗi.


   .. method:: assertNotEqual(first, second, msg=None)

      Kiểm tra xem *first* và *second* có khác nhau không. Nếu các giá trị bằng nhau, phép kiểm tra sẽ thất bại.

   .. method:: assertTrue(expr, msg=None)
               assertFalse(expr, msg=None)

      Kiểm tra xem *expr* là true (hoặc false).

      Lưu ý rằng điều này tương đương với ``bool(expr) is True`` chứ không phải ``expr is True`` (hãy dùng ``assertIs(expr, True)`` cho trường hợp sau). Cũng nên tránh phương thức này khi có các phương thức cụ thể hơn (ví dụ: ``assertEqual(a, b)`` thay vì ``assertTrue(a == b)``), vì chúng cung cấp thông báo lỗi tốt hơn trong trường hợp thất bại.


   .. method:: assertIs(first, second, msg=None)
               assertIsNot(first, second, msg=None)

      Kiểm thử rằng *first* và *second* là (hoặc không là) cùng một đối tượng.

      .. versionadded:: 3.1


   .. method:: assertIsNone(expr, msg=None)
               assertIsNotNone(expr, msg=None)

      Kiểm thử rằng *expr* là (hoặc không là) ``None``.

      .. versionadded:: 3.1


   .. method:: assertIn(member, container, msg=None)
               assertNotIn(member, container, msg=None)

      Kiểm thử rằng *member* nằm (hoặc không nằm) trong *container*.

      .. versionadded:: 3.1


   .. method:: assertIsInstance(obj, cls, msg=None)
               assertNotIsInstance(obj, cls, msg=None)

      Kiểm tra rằng *obj* là (hoặc không là) một instance của *cls* (có thể là một class hoặc một tuple các class, như được hỗ trợ bởi :func:`isinstance`). Để kiểm tra type chính xác, hãy sử dụng :func:`assertIs(type(obj), cls) <assertIs>`.

      .. versionadded:: 3.2


   .. method:: assertIsSubclass(cls, superclass, msg=None)
               assertNotIsSubclass(cls, superclass, msg=None)

      Kiểm tra rằng *cls* là (hoặc không là) một subclass của *superclass* (có thể là một class hoặc một tuple các class, như được hỗ trợ bởi :func:`issubclass`). Để kiểm tra type chính xác, hãy sử dụng :func:`assertIs(cls, superclass) <assertIs>`.

      .. versionadded:: 3.14


   Bạn cũng có thể kiểm tra việc tạo ra exception, warning và log message bằng các phương thức sau:

   +---------------------------------------------------------+--------------------------------------+------------+
   | Method                                                  | Checks that                          | New in     |
   +=========================================================+======================================+============+
   | :meth:`assertRaises(exc, fun, *args, **kwds)            | ``fun(*args, **kwds)`` raises *exc*  |            |
   | <TestCase.assertRaises>`                                |                                      |            |
   +---------------------------------------------------------+--------------------------------------+------------+
   | :meth:`assertRaisesRegex(exc, r, fun, *args, **kwds)    | ``fun(*args, **kwds)`` raises *exc*  | 3.1        |
   | <TestCase.assertRaisesRegex>`                           | and the message matches regex *r*    |            |
   +---------------------------------------------------------+--------------------------------------+------------+
   | :meth:`assertWarns(warn, fun, *args, **kwds)            | ``fun(*args, **kwds)`` raises *warn* | 3.2        |
   | <TestCase.assertWarns>`                                 |                                      |            |
   +---------------------------------------------------------+--------------------------------------+------------+
   | :meth:`assertWarnsRegex(warn, r, fun, *args, **kwds)    | ``fun(*args, **kwds)`` raises *warn* | 3.2        |
   | <TestCase.assertWarnsRegex>`                            | and the message matches regex *r*    |            |
   +---------------------------------------------------------+--------------------------------------+------------+
   | :meth:`assertLogs(logger, level)                        | The ``with`` block logs on *logger*  | 3.4        |
   | <TestCase.assertLogs>`                                  | with minimum *level*                 |            |
   +---------------------------------------------------------+--------------------------------------+------------+
   | :meth:`assertNoLogs(logger, level)                      | The ``with`` block does not log on   | 3.10       |
   | <TestCase.assertNoLogs>`                                |  *logger* with minimum *level*       |            |
   +---------------------------------------------------------+--------------------------------------+------------+

   .. method:: assertRaises(exception, callable, *args, **kwds)
               assertRaises(exception, *, msg=None)

      Kiểm tra rằng một exception được raise khi *callable* được gọi với bất kỳ đối số positional hoặc keyword nào cũng được truyền cho
      :meth:`assertRaises`.  Bài kiểm thử đạt nếu *exception* được phát sinh, là lỗi nếu một ngoại lệ khác được phát sinh hoặc thất bại nếu không có ngoại lệ nào được phát sinh. Để bắt bất kỳ ngoại lệ nào trong một nhóm ngoại lệ, có thể truyền một tuple chứa các lớp ngoại lệ làm *exception*.

      Nếu chỉ cung cấp các đối số *exception* và có thể cả *msg*, hãy trả về một context manager để mã đang được kiểm thử có thể được viết trực tiếp thay vì viết dưới dạng một hàm::

         with self.assertRaises(SomeException):
             do_something()

      Khi được sử dụng làm context manager, :meth:`assertRaises` chấp nhận thêm đối số từ khóa *msg*.

      Context manager sẽ lưu đối tượng ngoại lệ đã bắt được vào
      :attr:`!exception` attribute.  Điều này có thể hữu ích nếu mục đích là thực hiện các kiểm tra bổ sung đối với ngoại lệ được phát sinh::

         with self.assertRaises(SomeException) as cm:
             do_something()

         the_exception = cm.exception
         self.assertEqual(the_exception.error_code, 3)

      .. versionchanged:: 3.1
         Đã bổ sung khả năng sử dụng :meth:`assertRaises` làm context manager.

      .. versionchanged:: 3.2
         Đã bổ sung :attr:`!exception` attribute.

      .. versionchanged:: 3.3
         Đã thêm đối số từ khóa *msg* khi được sử dụng như một context manager.


   .. method:: assertRaisesRegex(exception, regex, callable, *args, **kwds)
               assertRaisesRegex(exception, regex, *, msg=None)

      Tương tự :meth:`assertRaises` nhưng cũng kiểm tra rằng *regex* khớp với biểu diễn chuỗi của exception được nêu ra. *regex* có thể là một đối tượng biểu thức chính quy hoặc một chuỗi chứa biểu thức chính quy phù hợp để sử dụng bởi :func:`re.search`. Ví dụ::

         self.assertRaisesRegex(ValueError, "invalid literal for.*XYZ'$",
                                int, 'XYZ')

      hoặc::

         with self.assertRaisesRegex(ValueError, 'literal'):
            int('XYZ')

      .. versionadded:: 3.1
         Được thêm với tên ``assertRaisesRegexp``.

      .. versionchanged:: 3.2
         Đổi tên thành :meth:`assertRaisesRegex`.

      .. versionchanged:: 3.3
         Đã thêm đối số từ khóa *msg* khi được sử dụng như một context manager.


   .. method:: assertWarns(warning, callable, *args, **kwds)
               assertWarns(warning, *, msg=None)

      Kiểm thử rằng một cảnh báo được kích hoạt khi *callable* được gọi với bất kỳ đối số vị trí hoặc từ khóa nào cũng được truyền vào
      :meth:`assertWarns`. Bài kiểm thử thành công nếu *warning* được kích hoạt và thất bại nếu không. Mọi ngoại lệ đều là lỗi. Để bắt bất kỳ cảnh báo nào trong một nhóm cảnh báo, có thể truyền một tuple chứa các lớp cảnh báo làm *warnings*.

      Nếu chỉ cung cấp các đối số *warning* và có thể cả *msg*, hãy trả về một context manager để mã đang được kiểm thử có thể được viết nội tuyến thay vì viết dưới dạng một hàm::

         with self.assertWarns(SomeWarning):
             do_something()

      Khi được sử dụng như một context manager, :meth:`assertWarns` chấp nhận thêm đối số từ khóa *msg*.

      Context manager sẽ lưu đối tượng cảnh báo đã bắt được vào
      :attr:`!warning` attribute, và dòng mã nguồn đã kích hoạt cảnh báo vào các attribute :attr:`!filename` và :attr:`!lineno`. Điều này có thể hữu ích nếu cần thực hiện thêm các kiểm tra trên cảnh báo đã bắt được::

         with self.assertWarns(SomeWarning) as cm:
             do_something()

         self.assertIn('myfile.py', cm.filename)
         self.assertEqual(320, cm.lineno)

      Phương thức này hoạt động bất kể các bộ lọc cảnh báo đang được áp dụng khi phương thức được gọi.

      .. versionadded:: 3.2

      .. versionchanged:: 3.3
         Đã thêm đối số từ khóa *msg* khi được sử dụng như một context manager.


   .. method:: assertWarnsRegex(warning, regex, callable, *args, **kwds)
               assertWarnsRegex(warning, regex, *, msg=None)

      Tương tự :meth:`assertWarns` nhưng cũng kiểm tra rằng *regex* khớp với thông báo của cảnh báo được kích hoạt. *regex* có thể là một đối tượng biểu thức chính quy hoặc một chuỗi chứa biểu thức chính quy phù hợp để :func:`re.search` sử dụng. Ví dụ::

         self.assertWarnsRegex(DeprecationWarning,
                               r'legacy_function\(\) is deprecated',
                               legacy_function, 'XYZ')

      hoặc::

         with self.assertWarnsRegex(RuntimeWarning, 'unsafe frobnicating'):
             frobnicate('/etc/passwd')

      .. versionadded:: 3.2

      .. versionchanged:: 3.3
         Đã thêm đối số từ khóa *msg* khi được sử dụng như một context manager.

   .. method:: assertLogs(logger=None, level=None)

      Một context manager dùng để kiểm tra rằng ít nhất một thông báo được ghi vào *logger* hoặc một trong các logger con của nó, với *level* tối thiểu như đã chỉ định.

      Nếu được chỉ định, *logger* phải là một đối tượng :class:`logging.Logger` hoặc một
      :class:`str` chỉ định tên của một logger. Mặc định là root logger, logger này sẽ nhận tất cả thông báo không bị chặn bởi một logger con không truyền tiếp.

      Nếu được chỉ định, *level* phải là một logging level dạng số hoặc giá trị chuỗi tương ứng (ví dụ là ``"ERROR"`` hoặc
      :const:`logging.ERROR`). Mặc định là :const:`logging.INFO`.

      Bài kiểm thử đạt nếu ít nhất một thông báo được phát ra bên trong khối ``with`` khớp với các điều kiện *logger* và *level*; nếu không, bài kiểm thử thất bại.

      Đối tượng được context manager trả về là một recording helper dùng để theo dõi các thông báo log khớp điều kiện. Đối tượng này có hai thuộc tính:

      .. attribute:: records

         Một danh sách các đối tượng :class:`logging.LogRecord` của những thông báo log khớp điều kiện.

      .. attribute:: output

         Một danh sách các đối tượng :class:`str` chứa đầu ra đã được định dạng của các message khớp.

      Ví dụ::

         with self.assertLogs('foo', level='INFO') as cm:
             logging.getLogger('foo').info('first message')
             logging.getLogger('foo.bar').error('second message')
         self.assertEqual(cm.output, ['INFO:foo:first message',
                                      'ERROR:foo.bar:second message'])

      .. versionadded:: 3.4

   .. method:: assertNoLogs(logger=None, level=None)

      Một context manager để kiểm tra rằng không có message nào được ghi vào *logger* hoặc một logger con của nó, với *level* tối thiểu đã cho.

      Nếu được chỉ định, *logger* phải là một đối tượng :class:`logging.Logger` hoặc một
      :class:`str` chỉ định tên của một logger. Mặc định là root logger, logger này sẽ bắt tất cả message.

      Nếu được chỉ định, *level* phải là một logging level dạng số hoặc giá trị chuỗi tương ứng (ví dụ là ``"ERROR"`` hoặc
      :const:`logging.ERROR`). Mặc định là :const:`logging.INFO`.

      Không giống :meth:`assertLogs`, trình quản lý ngữ cảnh sẽ không trả về gì.

      .. versionadded:: 3.10

   Ngoài ra còn có các phương thức khác được dùng để thực hiện những kiểm tra cụ thể hơn, chẳng hạn như:

   +---------------------------------------+--------------------------------+--------------+
   | Method                                | Checks that                    | New in       |
   +=======================================+================================+==============+
   | :meth:`assertAlmostEqual(a, b)        | ``round(a-b, 7) == 0``         |              |
   | <TestCase.assertAlmostEqual>`         |                                |              |
   +---------------------------------------+--------------------------------+--------------+
   | :meth:`assertNotAlmostEqual(a, b)     | ``round(a-b, 7) != 0``         |              |
   | <TestCase.assertNotAlmostEqual>`      |                                |              |
   +---------------------------------------+--------------------------------+--------------+
   | :meth:`assertGreater(a, b)            | ``a > b``                      | 3.1          |
   | <TestCase.assertGreater>`             |                                |              |
   +---------------------------------------+--------------------------------+--------------+
   | :meth:`assertGreaterEqual(a, b)       | ``a >= b``                     | 3.1          |
   | <TestCase.assertGreaterEqual>`        |                                |              |
   +---------------------------------------+--------------------------------+--------------+
   | :meth:`assertLess(a, b)               | ``a < b``                      | 3.1          |
   | <TestCase.assertLess>`                |                                |              |
   +---------------------------------------+--------------------------------+--------------+
   | :meth:`assertLessEqual(a, b)          | ``a <= b``                     | 3.1          |
   | <TestCase.assertLessEqual>`           |                                |              |
   +---------------------------------------+--------------------------------+--------------+
   | :meth:`assertRegex(s, r)              | ``r.search(s)``                | 3.1          |
   | <TestCase.assertRegex>`               |                                |              |
   +---------------------------------------+--------------------------------+--------------+
   | :meth:`assertNotRegex(s, r)           | ``not r.search(s)``            | 3.2          |
   | <TestCase.assertNotRegex>`            |                                |              |
   +---------------------------------------+--------------------------------+--------------+
   | :meth:`assertCountEqual(a, b)         | *a* contains the same elements | 3.2          |
   | <TestCase.assertCountEqual>`          | as *b*, regardless of their    |              |
   |                                       | order.                         |              |
   +---------------------------------------+--------------------------------+--------------+
   | :meth:`assertStartsWith(a, b)         | ``a.startswith(b)``            | 3.14         |
   | <TestCase.assertStartsWith>`          |                                |              |
   +---------------------------------------+--------------------------------+--------------+
   | :meth:`assertNotStartsWith(a, b)      | ``not a.startswith(b)``        | 3.14         |
   | <TestCase.assertNotStartsWith>`       |                                |              |
   +---------------------------------------+--------------------------------+--------------+
   | :meth:`assertEndsWith(a, b)           | ``a.endswith(b)``              | 3.14         |
   | <TestCase.assertEndsWith>`            |                                |              |
   +---------------------------------------+--------------------------------+--------------+
   | :meth:`assertNotEndsWith(a, b)        | ``not a.endswith(b)``          | 3.14         |
   | <TestCase.assertNotEndsWith>`         |                                |              |
   +---------------------------------------+--------------------------------+--------------+
   | :meth:`assertHasAttr(a, b)            | ``hasattr(a, b)``              | 3.14         |
   | <TestCase.assertHasAttr>`             |                                |              |
   +---------------------------------------+--------------------------------+--------------+
   | :meth:`assertNotHasAttr(a, b)         | ``not hasattr(a, b)``          | 3.14         |
   | <TestCase.assertNotHasAttr>`          |                                |              |
   +---------------------------------------+--------------------------------+--------------+


   .. method:: assertAlmostEqual(first, second, places=7, msg=None, delta=None)
               assertNotAlmostEqual(first, second, places=7, msg=None, delta=None)

      Kiểm tra rằng *first* và *second* bằng nhau một cách xấp xỉ (hoặc không bằng nhau một cách xấp xỉ) bằng cách tính hiệu, làm tròn đến số *places* thập phân đã cho (mặc định là 7), rồi so sánh với số 0. Lưu ý rằng các phương thức này làm tròn các giá trị đến số *decimal places* đã cho (tức là giống hàm :func:`round`) chứ không phải *significant digits*.

      Nếu cung cấp *delta* thay cho *places* thì hiệu giữa *first* và *second* phải nhỏ hơn hoặc bằng (hoặc lớn hơn) *delta*.

      Việc cung cấp cả *delta* và *places* sẽ gây ra một :exc:`TypeError`.

      .. versionchanged:: 3.2
         :meth:`assertAlmostEqual` automatically considers almost equal objects
         có giá trị so sánh bằng nhau. :meth:`assertNotAlmostEqual` sẽ tự động thất bại nếu các đối tượng có giá trị so sánh bằng nhau. Đã thêm đối số từ khóa *delta*.


   .. method:: assertGreater(first, second, msg=None)
               assertGreaterEqual(first, second, msg=None) assertLess(first, second, msg=None) assertLessEqual(first, second, msg=None)

      Kiểm tra rằng *first* lần lượt >, >=, < hoặc <= *second* tùy thuộc vào tên phương thức. Nếu không, bài kiểm tra sẽ thất bại::

         >>> self.assertGreaterEqual(3, 4)
         AssertionError: "3" unexpectedly not greater than or equal to "4"

      .. versionadded:: 3.1


   .. method:: assertRegex(text, regex, msg=None)
               assertNotRegex(text, regex, msg=None)

      Kiểm tra rằng một phép tìm kiếm bằng *regex* khớp (hoặc không khớp) với *text*. Nếu thất bại, thông báo lỗi sẽ bao gồm mẫu và *text* (hoặc mẫu và phần của *text* bất ngờ khớp). *regex* có thể là một đối tượng regular expression hoặc một chuỗi chứa regular expression phù hợp để sử dụng với :func:`re.search`.

      .. versionadded:: 3.1
         Được thêm với tên ``assertRegexpMatches``.
      .. versionchanged:: 3.2
         Phương thức ``assertRegexpMatches()`` đã được đổi tên thành
         :meth:`.assertRegex`.
      .. versionadded:: 3.2
         :meth:`.assertNotRegex`.


   .. method:: assertCountEqual(first, second, msg=None)

      Kiểm tra rằng sequence *first* chứa các phần tử giống như *second*, bất kể thứ tự của chúng. Nếu không giống nhau, một thông báo lỗi liệt kê những khác biệt giữa các sequence sẽ được tạo.

      Các phần tử trùng lặp *không* bị bỏ qua khi so sánh *first* và *second*. Phương thức này xác minh rằng mỗi phần tử xuất hiện cùng số lần trong cả hai sequence. Tương đương với: ``assertEqual(Counter(list(first)), Counter(list(second)))`` nhưng cũng hoạt động với các sequence chứa những object không thể băm.

      .. versionadded:: 3.2


   .. method:: assertStartsWith(s, prefix, msg=None)
   .. method:: assertNotStartsWith(s, prefix, msg=None)

      Kiểm tra xem chuỗi Unicode hoặc byte *s* có bắt đầu (hoặc không bắt đầu) bằng *prefix* hay không. *prefix* cũng có thể là một tuple gồm các chuỗi cần thử.

      .. versionadded:: 3.14


   .. method:: assertEndsWith(s, suffix, msg=None)
   .. method:: assertNotEndsWith(s, suffix, msg=None)

      Kiểm tra xem chuỗi Unicode hoặc byte *s* có kết thúc (hoặc không kết thúc) bằng *suffix* hay không. *suffix* cũng có thể là một tuple gồm các chuỗi cần thử.

      .. versionadded:: 3.14


   .. method:: assertHasAttr(obj, name, msg=None)
   .. method:: assertNotHasAttr(obj, name, msg=None)

      Kiểm tra xem object *obj* có (hoặc không có) thuộc tính *name* hay không.

      .. versionadded:: 3.14


   .. _type-specific-methods:

   Phương thức :meth:`assertEqual` chuyển việc kiểm tra tính bằng nhau của các object cùng kiểu sang những phương thức riêng cho từng kiểu. Các phương thức này đã được triển khai cho hầu hết các kiểu tích hợp sẵn, nhưng cũng có thể đăng ký các phương thức mới bằng :meth:`addTypeEqualityFunc`:

   .. method:: addTypeEqualityFunc(typeobj, function)

      Đăng ký một phương thức riêng cho kiểu, được :meth:`assertEqual` gọi để kiểm tra xem hai object có cùng *typeobj* chính xác (không phải subclass) có bằng nhau hay không. *function* phải nhận hai đối số vị trí và đối số từ khóa thứ ba msg=None, giống như :meth:`assertEqual`. Phương thức này phải raise
      :data:`self.failureException(msg) <failureException>` khi phát hiện sự không bằng nhau giữa hai tham số đầu tiên — có thể cung cấp thông tin hữu ích và giải thích chi tiết sự khác nhau trong thông báo lỗi.

      .. versionadded:: 3.1

   Danh sách các phương thức dành riêng cho từng kiểu được tự động sử dụng bởi
   :meth:`~TestCase.assertEqual` được tóm tắt trong bảng sau. Lưu ý rằng thường không cần gọi trực tiếp các phương thức này.

   +-----------------------------------------+-----------------------------+--------------+
   | Method                                  | Used to compare             | New in       |
   +=========================================+=============================+==============+
   | :meth:`assertMultiLineEqual(a, b)       | strings                     | 3.1          |
   | <TestCase.assertMultiLineEqual>`        |                             |              |
   +-----------------------------------------+-----------------------------+--------------+
   | :meth:`assertSequenceEqual(a, b)        | sequences                   | 3.1          |
   | <TestCase.assertSequenceEqual>`         |                             |              |
   +-----------------------------------------+-----------------------------+--------------+
   | :meth:`assertListEqual(a, b)            | lists                       | 3.1          |
   | <TestCase.assertListEqual>`             |                             |              |
   +-----------------------------------------+-----------------------------+--------------+
   | :meth:`assertTupleEqual(a, b)           | tuples                      | 3.1          |
   | <TestCase.assertTupleEqual>`            |                             |              |
   +-----------------------------------------+-----------------------------+--------------+
   | :meth:`assertSetEqual(a, b)             | sets or frozensets          | 3.1          |
   | <TestCase.assertSetEqual>`              |                             |              |
   +-----------------------------------------+-----------------------------+--------------+
   | :meth:`assertDictEqual(a, b)            | dicts                       | 3.1          |
   | <TestCase.assertDictEqual>`             |                             |              |
   +-----------------------------------------+-----------------------------+--------------+



   .. method:: assertMultiLineEqual(first, second, msg=None)

      Kiểm tra xem chuỗi nhiều dòng *first* có bằng chuỗi *second* hay không. Nếu không bằng nhau, thông báo lỗi sẽ bao gồm diff của hai chuỗi, làm nổi bật những điểm khác biệt. Phương thức này được sử dụng theo mặc định khi so sánh các chuỗi với :meth:`assertEqual`.

      .. versionadded:: 3.1


   .. method:: assertSequenceEqual(first, second, msg=None, seq_type=None)

      Kiểm tra xem hai sequence có bằng nhau hay không. Nếu cung cấp một *seq_type*, cả *first* và *second* phải là các instance của *seq_type*, nếu không sẽ phát sinh lỗi. Nếu các sequence khác nhau, một thông báo lỗi sẽ được tạo để hiển thị sự khác biệt giữa chúng.

      Phương thức này không được :meth:`assertEqual` gọi trực tiếp, nhưng được dùng để triển khai :meth:`assertListEqual` và
      :meth:`assertTupleEqual`.

      .. versionadded:: 3.1


   .. method:: assertListEqual(first, second, msg=None)
               assertTupleEqual(first, second, msg=None)

      Kiểm tra xem hai list hoặc tuple có bằng nhau hay không. Nếu không, một thông báo lỗi sẽ được tạo để chỉ hiển thị những điểm khác biệt giữa chúng. Lỗi cũng sẽ phát sinh nếu một trong hai tham số có kiểu không đúng. Các phương thức này được sử dụng theo mặc định khi so sánh list hoặc tuple với
      :meth:`assertEqual`.

      .. versionadded:: 3.1


   .. method:: assertSetEqual(first, second, msg=None)

      Kiểm tra xem hai tập hợp có bằng nhau hay không. Nếu không, một thông báo lỗi sẽ được tạo, liệt kê những khác biệt giữa các tập hợp. Theo mặc định, phương thức này được sử dụng khi so sánh các tập hợp hoặc frozenset với :meth:`assertEqual`.

      Sẽ thất bại nếu *first* hoặc *second* không có phương thức :meth:`~frozenset.difference`.

      .. versionadded:: 3.1


   .. method:: assertDictEqual(first, second, msg=None)

      Kiểm tra xem hai dictionary có bằng nhau hay không. Nếu không, một thông báo lỗi sẽ được tạo để hiển thị những khác biệt trong các dictionary. Theo mặc định, phương thức này sẽ được dùng để so sánh các dictionary trong những lệnh gọi đến :meth:`assertEqual`.

      .. versionadded:: 3.1



   .. _other-methods-and-attrs:

   Cuối cùng, :class:`TestCase` cung cấp các phương thức và thuộc tính sau:


   .. method:: fail(msg=None)

      Luôn báo hiệu một kiểm thử thất bại, với *msg* hoặc ``None`` làm thông báo lỗi.


   .. attribute:: failureException

      Thuộc tính lớp này cung cấp exception được phương thức kiểm thử đưa ra. Nếu một test framework cần sử dụng một exception chuyên biệt, có thể để chứa thêm thông tin, exception đó phải kế thừa exception này để "phối hợp đúng cách" với framework. Giá trị ban đầu của thuộc tính này là
      :exc:`AssertionError`.


   .. attribute:: longMessage

      Thuộc tính lớp này xác định điều gì sẽ xảy ra khi một thông báo lỗi tùy chỉnh được truyền dưới dạng đối số msg cho một lệnh gọi assertXYY bị thất bại. ``True`` là giá trị mặc định. Trong trường hợp này, thông báo tùy chỉnh được nối vào cuối thông báo lỗi tiêu chuẩn. Khi được đặt thành ``False``, thông báo tùy chỉnh sẽ thay thế thông báo tiêu chuẩn.

      Có thể ghi đè thiết lập của lớp trong từng phương thức kiểm thử bằng cách gán thuộc tính instance self.longMessage là ``True`` hoặc ``False`` trước khi gọi các phương thức assert.

      Thiết lập của lớp được đặt lại trước mỗi lần gọi kiểm thử.

      .. versionadded:: 3.1


   .. attribute:: maxDiff

      Thuộc tính này kiểm soát độ dài tối đa của các diff do những phương thức assert xuất ra khi báo cáo diff lúc kiểm thử thất bại. Giá trị mặc định là 80*8 ký tự. Các phương thức assert bị ảnh hưởng bởi thuộc tính này gồm
      :meth:`assertSequenceEqual` (bao gồm tất cả các phương thức so sánh sequence ủy quyền cho phương thức này), :meth:`assertDictEqual` và
      :meth:`assertMultiLineEqual`.

      Đặt ``maxDiff`` thành ``None`` có nghĩa là độ dài của các diff không bị giới hạn.

      .. versionadded:: 3.2


   Các framework kiểm thử có thể sử dụng những phương thức sau để thu thập thông tin về bài kiểm thử:


   .. method:: countTestCases()

      Trả về số lượng bài kiểm thử được biểu diễn bởi đối tượng kiểm thử này.  Với
      các thực thể :class:`TestCase`, điều này sẽ luôn là ``1``.


   .. method:: defaultTestResult()

      Trả về một thực thể của lớp kết quả kiểm thử sẽ được sử dụng cho lớp trường hợp kiểm thử này (nếu không có thực thể kết quả nào khác được cung cấp cho
      phương thức :meth:`run`).

      Đối với các thực thể :class:`TestCase`, đây sẽ luôn là một thực thể của
      :class:`TestResult`; các lớp con của :class:`TestCase` nên ghi đè phương thức này khi cần.


   .. method:: id()

      Trả về một chuỗi xác định trường hợp kiểm thử cụ thể. Chuỗi này thường là tên đầy đủ của phương thức kiểm thử, bao gồm tên module và tên lớp.


   .. method:: shortDescription()

      Trả về mô tả của kiểm thử hoặc ``None`` nếu chưa có mô tả nào được cung cấp. Cách triển khai mặc định của phương thức này trả về dòng đầu tiên trong docstring của phương thức kiểm thử, nếu có, hoặc ``None``.

      .. versionchanged:: 3.1
         Trong 3.1, điều này đã được thay đổi để thêm tên kiểm thử vào phần mô tả ngắn ngay cả khi có docstring. Điều này gây ra các vấn đề tương thích với các phần mở rộng của unittest, và việc thêm tên kiểm thử đã được chuyển sang
         :class:`TextTestResult` trong Python 3.2.


   .. method:: addCleanup(function, /, *args, **kwargs)

      Thêm một hàm được gọi sau :meth:`tearDown` để dọn dẹp các tài nguyên được sử dụng trong quá trình kiểm thử. Các hàm sẽ được gọi theo thứ tự ngược với thứ tự chúng được thêm vào (:abbr:`LIFO (vào sau, ra trước)`). Chúng được gọi với mọi đối số và đối số từ khóa được truyền vào
      :meth:`addCleanup` khi chúng được thêm vào.

      Nếu :meth:`setUp` không thành công, nghĩa là :meth:`tearDown` không được gọi, thì mọi hàm dọn dẹp đã được thêm vào vẫn sẽ được gọi.

      .. versionadded:: 3.1


   .. method:: enterContext(cm)

      Nhập trình quản lý ngữ cảnh được cung cấp. Nếu thành công, đồng thời thêm phương thức :meth:`~object.__exit__` của nó làm hàm dọn dẹp bằng cách sử dụng :term:`context manager` và trả về kết quả của
      :meth:`addCleanup` và trả về kết quả của
      Phương thức :meth:`~object.__enter__`.

      .. versionadded:: 3.11


   .. method:: doCleanups()

      Phương thức này luôn được gọi sau :meth:`tearDown`, hoặc sau :meth:`setUp` nếu :meth:`setUp` phát sinh ngoại lệ.

      Phương thức này chịu trách nhiệm gọi tất cả các hàm dọn dẹp được thêm bởi
      :meth:`addCleanup`. Nếu bạn cần các hàm dọn dẹp được gọi *trước* :meth:`tearDown` thì bạn có thể tự gọi :meth:`doCleanups`.

      :meth:`doCleanups` lần lượt lấy từng phương thức ra khỏi ngăn xếp các hàm dọn dẹp, vì vậy có thể gọi phương thức này bất kỳ lúc nào.

      .. versionadded:: 3.1


   .. classmethod:: addClassCleanup(function, /, *args, **kwargs)

      Thêm một hàm sẽ được gọi sau :meth:`tearDownClass` để dọn dẹp các tài nguyên được sử dụng trong lớp kiểm thử. Các hàm sẽ được gọi theo thứ tự ngược với thứ tự chúng được thêm vào (:abbr:`LIFO (vào sau, gọi trước)`). Chúng được gọi với mọi đối số và đối số từ khóa được truyền vào
      :meth:`addClassCleanup` khi chúng được thêm vào.

      Nếu :meth:`setUpClass` thất bại, nghĩa là :meth:`tearDownClass` không được gọi, thì mọi hàm dọn dẹp đã được thêm vào vẫn sẽ được gọi.

      .. versionadded:: 3.8


   .. classmethod:: enterClassContext(cm)

      Nhập trình quản lý ngữ cảnh được cung cấp. Nếu thành công, đồng thời thêm phương thức :meth:`~object.__exit__` của nó làm hàm dọn dẹp bằng cách sử dụng :term:`context manager` và trả về kết quả của
      :meth:`addClassCleanup` và trả về kết quả của
      Phương thức :meth:`~object.__enter__`.

      .. versionadded:: 3.11


   .. classmethod:: doClassCleanups()

      Phương thức này luôn được gọi sau :meth:`tearDownClass`, hoặc sau :meth:`setUpClass` nếu :meth:`setUpClass` phát sinh ngoại lệ.

      Phương thức này chịu trách nhiệm gọi tất cả các hàm dọn dẹp được thêm bởi
      :meth:`addClassCleanup`. Nếu bạn cần các hàm dọn dẹp được gọi *trước* :meth:`tearDownClass` thì bạn có thể gọi
      :meth:`doClassCleanups` chính bạn.

      :meth:`doClassCleanups` lần lượt lấy các phương thức ra khỏi ngăn xếp các hàm cleanup, vì vậy có thể được gọi bất cứ lúc nào.

      .. versionadded:: 3.8


.. class:: IsolatedAsyncioTestCase(methodName='runTest')

   Lớp này cung cấp API tương tự :class:`TestCase` và cũng chấp nhận coroutine làm các hàm kiểm thử.

   .. versionadded:: 3.8

   .. attribute:: loop_factory

      *loop_factory* được truyền vào :class:`asyncio.Runner`. Ghi đè trong các lớp con bằng :class:`asyncio.EventLoop` để tránh sử dụng hệ thống chính sách asyncio.

      .. versionadded:: 3.13

   .. method:: asyncSetUp()
      :async:

      Phương thức được gọi để chuẩn bị test fixture. Phương thức này được gọi sau :meth:`TestCase.setUp`. Phương thức này được gọi ngay trước khi gọi phương thức kiểm thử; ngoài
      :exc:`AssertionError` hoặc :exc:`SkipTest`, mọi ngoại lệ do phương thức này phát sinh sẽ được xem là lỗi thay vì test failure. Cách triển khai mặc định không thực hiện gì.

   .. method:: asyncTearDown()
      :async:

      Phương thức được gọi ngay sau khi phương thức kiểm thử được gọi và kết quả được ghi nhận. Phương thức này được gọi trước :meth:`~TestCase.tearDown`. Phương thức này vẫn được gọi ngay cả khi phương thức kiểm thử phát sinh ngoại lệ, vì vậy cách triển khai trong các lớp con có thể cần đặc biệt cẩn thận khi kiểm tra trạng thái nội bộ. Mọi ngoại lệ, ngoại trừ
      :exc:`AssertionError` hoặc :exc:`SkipTest` do phương thức này phát sinh sẽ được xem là một lỗi bổ sung thay vì lỗi kiểm thử (do đó làm tăng tổng số lỗi được báo cáo). Phương thức này chỉ được gọi nếu :meth:`asyncSetUp` thành công, bất kể kết quả của phương thức kiểm thử. Bản triển khai mặc định không thực hiện gì.

   .. method:: addAsyncCleanup(function, /, *args, **kwargs)

      Phương thức này nhận một coroutine có thể được dùng làm hàm cleanup.

   .. method:: enterAsyncContext(cm)
      :async:

      Đi vào :term:`asynchronous context manager` được cung cấp. Nếu thành công, đồng thời thêm phương thức :meth:`~object.__aexit__` của nó làm hàm cleanup bằng cách
      :meth:`addAsyncCleanup` và trả về kết quả của
      phương thức :meth:`~object.__aenter__`.

      .. versionadded:: 3.11


   .. method:: run(result=None)

      Thiết lập một event loop mới để chạy kiểm thử, rồi thu thập kết quả vào đối tượng :class:`TestResult` được truyền dưới dạng *result*. Nếu *result* bị bỏ qua hoặc là ``None``, một đối tượng kết quả tạm thời sẽ được tạo (bằng cách gọi phương thức :meth:`~TestCase.defaultTestResult`) và được sử dụng. Đối tượng kết quả được trả về cho bên gọi của :meth:`run`. Khi kết thúc kiểm thử, tất cả tác vụ trong event loop sẽ bị hủy.


   Ví dụ minh họa thứ tự::

      from unittest import IsolatedAsyncioTestCase

      events = []


      class Test(IsolatedAsyncioTestCase):


          def setUp(self):
              events.append("setUp")

          async def asyncSetUp(self):
              self._async_connection = await AsyncConnection()
              events.append("asyncSetUp")

          async def test_response(self):
              events.append("test_response")
              response = await self._async_connection.get("https://example.com")
              self.assertEqual(response.status_code, 200)
              self.addAsyncCleanup(self.on_cleanup)

          def tearDown(self):
              events.append("tearDown")

          async def asyncTearDown(self):
              await self._async_connection.close()
              events.append("asyncTearDown")

          async def on_cleanup(self):
              events.append("cleanup")

      if __name__ == "__main__":
          unittest.main()

   Sau khi chạy kiểm thử, ``events`` sẽ chứa ``["setUp", "asyncSetUp", "test_response", "asyncTearDown", "tearDown", "cleanup"]``.


.. class:: FunctionTestCase(testFunc, setUp=None, tearDown=None, description=None)

   Lớp này triển khai phần của giao diện :class:`TestCase` cho phép test runner điều khiển kiểm thử, nhưng không cung cấp các phương thức mà mã kiểm thử có thể dùng để kiểm tra và báo cáo lỗi. Lớp này được dùng để tạo các test case bằng mã kiểm thử kiểu cũ, cho phép tích hợp mã đó vào một
   framework kiểm thử dựa trên :mod:`!unittest`.


.. _testsuite-objects:

Nhóm các kiểm thử
~~~~~~~~~~~~~~~~~

.. class:: TestSuite(tests=())

   Lớp này biểu diễn một tập hợp các test case và test suite riêng lẻ. Lớp này cung cấp giao diện cần thiết cho test runner, cho phép chạy nó như bất kỳ test case nào khác. Chạy một thể hiện :class:`TestSuite` cũng giống như lặp qua test suite, chạy từng kiểm thử riêng lẻ.

   Nếu *tests* được cung cấp, nó phải là một iterable gồm các test case riêng lẻ hoặc các test suite khác, được dùng để tạo test suite ban đầu. Các phương thức bổ sung cho phép thêm test case và test suite vào tập hợp này sau đó.

   Các đối tượng :class:`TestSuite` hoạt động gần giống các đối tượng :class:`TestCase`, ngoại trừ việc chúng không thực sự triển khai một kiểm thử. Thay vào đó, chúng được dùng để tập hợp các kiểm thử thành những nhóm kiểm thử sẽ được chạy cùng nhau. Có thêm một số phương thức để thêm kiểm thử vào các thể hiện :class:`TestSuite`:


   .. method:: TestSuite.addTest(test)

      Thêm một :class:`TestCase` hoặc :class:`TestSuite` vào bộ kiểm thử.


   .. method:: TestSuite.addTests(tests)

      Thêm tất cả các kiểm thử từ một iterable gồm các thực thể :class:`TestCase` và :class:`TestSuite` vào bộ kiểm thử này.

      Tương đương với việc lặp qua *tests* và gọi :meth:`addTest` cho mỗi phần tử.

   :class:`TestSuite` dùng chung các phương thức sau với :class:`TestCase`:


   .. method:: run(result)

      Chạy các kiểm thử được liên kết với bộ kiểm thử này, rồi tập hợp kết quả vào đối tượng kết quả kiểm thử được truyền dưới dạng *result*. Lưu ý rằng không giống như
      :meth:`TestCase.run`, :meth:`TestSuite.run` yêu cầu phải truyền đối tượng kết quả vào.


   .. method:: debug()

      Chạy các kiểm thử được liên kết với bộ kiểm thử này mà không tập hợp kết quả. Điều này cho phép các ngoại lệ do kiểm thử phát sinh được truyền đến caller và có thể được dùng để hỗ trợ chạy kiểm thử dưới debugger.


   .. method:: countTestCases()

      Trả về số lượng kiểm thử được biểu diễn bởi đối tượng kiểm thử này, bao gồm tất cả các kiểm thử riêng lẻ và các bộ kiểm thử con.


   .. method:: __iter__()

      Các kiểm thử được nhóm bởi một :class:`TestSuite` luôn được truy cập thông qua phép lặp. Các lớp con có thể cung cấp kiểm thử một cách trì hoãn bằng cách ghi đè :meth:`!__iter__`. Lưu ý rằng phương thức này có thể được gọi nhiều lần trên cùng một bộ kiểm thử (ví dụ: khi đếm kiểm thử hoặc so sánh tính bằng nhau), vì vậy các kiểm thử được trả về qua những lần lặp lại trước :meth:`TestSuite.run` phải giống nhau trong mỗi lần gọi. Sau :meth:`TestSuite.run`, bên gọi không nên dựa vào các kiểm thử được phương thức này trả về, trừ khi bên gọi sử dụng một lớp con ghi đè :meth:`!TestSuite._removeTestAtIndex` để bảo toàn các tham chiếu đến kiểm thử.

      .. versionchanged:: 3.2
         Trong các phiên bản trước, :class:`TestSuite` truy cập trực tiếp vào các kiểm thử thay vì thông qua phép lặp, vì vậy việc ghi đè :meth:`!__iter__` là chưa đủ để cung cấp các kiểm thử.

      .. versionchanged:: 3.4
         Trong các phiên bản trước, :class:`TestSuite` lưu các tham chiếu đến từng
         :class:`TestCase` sau :meth:`TestSuite.run`. Các lớp con có thể khôi phục hành vi đó bằng cách ghi đè :meth:`!TestSuite._removeTestAtIndex`.

   Trong cách sử dụng điển hình của một đối tượng :class:`TestSuite`, phương thức :meth:`run` được gọi bởi một :class:`!TestRunner` thay vì bởi bộ chạy kiểm thử của người dùng cuối.


Tải và chạy kiểm thử
~~~~~~~~~~~~~~~~~~~~

.. class:: TestLoader()

   Lớp :class:`TestLoader` được dùng để tạo các test suite từ các lớp và module. Thông thường, không cần tạo một instance của lớp này;
   module :mod:`!unittest` cung cấp một instance có thể được dùng chung dưới dạng
   :data:`unittest.defaultTestLoader`. Tuy nhiên, việc sử dụng một lớp con hoặc instance cho phép tùy chỉnh một số thuộc tính có thể cấu hình.

   Các object :class:`TestLoader` có các thuộc tính sau:


   .. attribute:: errors

      Danh sách các lỗi không nghiêm trọng gặp phải trong khi tải test. Loader không reset danh sách này tại bất kỳ thời điểm nào. Các lỗi nghiêm trọng được báo hiệu bằng cách phương thức liên quan ném exception cho caller. Các lỗi không nghiêm trọng cũng được biểu thị bằng một test tổng hợp, test này sẽ ném lỗi ban đầu khi được chạy.

      .. versionadded:: 3.5


   Các object :class:`TestLoader` có các phương thức sau:


   .. method:: loadTestsFromTestCase(testCaseClass)

      Trả về một suite gồm tất cả các test case có trong các lớp :class:`TestCase`\ -derived
      :class:`!testCaseClass`.

      Một đối tượng test case được tạo cho mỗi phương thức có tên được chỉ định bởi
      :meth:`getTestCaseNames`. Theo mặc định, đây là các tên phương thức bắt đầu bằng ``test``. Nếu :meth:`getTestCaseNames` không trả về phương thức nào, nhưng phương thức :meth:`!runTest` được triển khai, thì thay vào đó, một test case duy nhất sẽ được tạo cho phương thức đó.


   .. method:: loadTestsFromModule(module, *, pattern=None)

      Trả về một suite chứa tất cả test case trong module đã cho. Phương thức này tìm kiếm *module* để tìm các lớp kế thừa từ :class:`TestCase` và tạo một đối tượng của lớp cho mỗi phương thức test được định nghĩa trong lớp.

      .. note::

         Mặc dù việc sử dụng một hệ phân cấp các lớp kế thừa từ :class:`TestCase`\  có thể thuận tiện cho việc chia sẻ fixture và hàm trợ giúp, việc định nghĩa các phương thức test trên các lớp cơ sở không được dự định khởi tạo trực tiếp sẽ không hoạt động tốt với phương thức này. Tuy nhiên, cách làm đó có thể hữu ích khi các fixture khác nhau và được định nghĩa trong các lớp con.

      Nếu một module cung cấp hàm ``load_tests`` thì hàm đó sẽ được gọi để tải các test. Điều này cho phép các module tùy chỉnh việc tải test. Đây là giao thức `load_tests protocol <load_tests protocol_>`_. Đối số *pattern* được truyền dưới dạng đối số thứ ba cho ``load_tests``.

      .. versionchanged:: 3.2
         Đã bổ sung hỗ trợ cho ``load_tests``.

      .. versionchanged:: 3.5
         Đã bổ sung hỗ trợ cho đối số chỉ nhận theo từ khóa *pattern*.

      .. versionchanged:: 3.12
         Tham số *use_load_tests* chưa được ghi nhận và không chính thức đã bị loại bỏ.


   .. method:: loadTestsFromName(name, module=None)

      Trả về một suite gồm tất cả các test case được chỉ định bằng một chuỗi đặc tả.

      Bộ chỉ định *name* là một "tên dạng chấm" (dotted name), có thể phân giải thành một module, một lớp test case, một phương thức test trong một lớp test case, hoặc một
      :class:`TestSuite` instance hoặc một đối tượng callable trả về một
      :class:`TestCase` hoặc instance :class:`TestSuite`. Các kiểm tra này được áp dụng theo thứ tự được liệt kê ở đây; nghĩa là, một phương thức trên một lớp test case có thể được chọn làm "một phương thức test trong một lớp test case", thay vì "một đối tượng callable".

      Ví dụ: nếu bạn có một module :mod:`!SampleTests` chứa một
      :class:`TestCase`\ -derived class :class:`!SampleTestCase` với ba phương thức test (:meth:`!test_one`, :meth:`!test_two` và :meth:`!test_three`), bộ chỉ định ``'SampleTests.SampleTestCase'`` sẽ khiến phương thức này trả về một suite chạy cả ba phương thức test. Sử dụng bộ chỉ định ``'SampleTests.SampleTestCase.test_two'`` sẽ khiến nó trả về một test suite chỉ chạy phương thức test :meth:`!test_two`. Bộ chỉ định có thể tham chiếu đến các module và package chưa được import; chúng sẽ được import như một tác dụng phụ.

      Phương thức này tùy chọn phân giải *name* tương đối so với *module* đã cho.

      .. versionchanged:: 3.5
         Nếu xảy ra :exc:`ImportError` hoặc :exc:`AttributeError` trong khi duyệt qua *name*, một bài kiểm thử tổng hợp sẽ được trả về; bài kiểm thử này sẽ phát sinh lỗi đó khi chạy. Các lỗi này được đưa vào những lỗi được tích lũy trong self.errors.


   .. method:: loadTestsFromNames(names, module=None)

      Tương tự như :meth:`loadTestsFromName`, nhưng nhận một chuỗi tên thay vì một tên duy nhất. Giá trị trả về là một test suite hỗ trợ tất cả các bài kiểm thử được định nghĩa cho từng tên.


   .. method:: getTestCaseNames(testCaseClass)

      Trả về một chuỗi tên phương thức đã được sắp xếp, được tìm thấy trong *testCaseClass*; đây phải là một lớp con của :class:`TestCase`.


   .. method:: discover(start_dir, pattern='test*.py', top_level_dir=None)

      Tìm tất cả các module kiểm thử bằng cách đệ quy vào các thư mục con từ thư mục bắt đầu được chỉ định, rồi trả về một đối tượng TestSuite chứa chúng. Chỉ những tệp kiểm thử khớp với *pattern* mới được tải. (Sử dụng khớp mẫu theo kiểu shell.) Chỉ những tên module có thể import (tức là các mã định danh Python hợp lệ) mới được tải.

      Tất cả các module kiểm thử phải có thể được import từ cấp cao nhất của dự án. Nếu thư mục bắt đầu không phải là thư mục cấp cao nhất thì phải chỉ định riêng *top_level_dir*.

      Nếu việc import một module không thành công, chẳng hạn do lỗi cú pháp, thì lỗi này sẽ được ghi nhận là một lỗi duy nhất và quá trình phát hiện sẽ tiếp tục. Nếu việc import không thành công là do :exc:`SkipTest` được phát sinh, thì lỗi này sẽ được ghi nhận là một lần bỏ qua thay vì một lỗi.

      Nếu tìm thấy một package (thư mục chứa tệp có tên :file:`__init__.py`), package đó sẽ được kiểm tra để tìm hàm ``load_tests``. Nếu hàm này tồn tại thì nó sẽ được gọi với ``package.load_tests(loader, tests, pattern)``. Việc phát hiện test đảm bảo rằng một package chỉ được kiểm tra test một lần trong mỗi lần gọi, ngay cả khi bản thân hàm load_tests gọi ``loader.discover``.

      Nếu ``load_tests`` tồn tại thì quá trình phát hiện *không* đệ quy vào package; ``load_tests`` chịu trách nhiệm tải tất cả test trong package.

      Mẫu này được cố ý không lưu dưới dạng thuộc tính của loader để các package có thể tiếp tục tự thực hiện việc phát hiện.

      *top_level_dir* được lưu trữ nội bộ và được dùng làm giá trị mặc định cho mọi lời gọi lồng nhau tới ``discover()``. Nghĩa là, nếu ``load_tests`` của một package gọi ``loader.discover()``, thì không cần truyền đối số này.

      *start_dir* cũng có thể là tên module dạng dotted, không chỉ là một thư mục.

      .. versionadded:: 3.2

      .. versionchanged:: 3.4
         Các module phát sinh :exc:`SkipTest` khi import sẽ được ghi nhận là bị bỏ qua, không phải lỗi.

         *start_dir* có thể là một :term:`namespace packages <namespace package>`.

         Các đường dẫn được sắp xếp trước khi import để thứ tự thực thi giống nhau ngay cả khi thứ tự của hệ thống tệp bên dưới không phụ thuộc vào tên tệp.

      .. versionchanged:: 3.5
         Các package được tìm thấy hiện được kiểm tra để tìm ``load_tests`` bất kể đường dẫn của chúng có khớp với *pattern* hay không, vì tên package không thể khớp với pattern mặc định.

      .. versionchanged:: 3.11
         *start_dir* không thể là một :term:`namespace packages <namespace package>`. Tính năng này đã bị hỏng kể từ Python 3.7 và Python 3.11 chính thức loại bỏ nó.

      .. versionchanged:: 3.13
         *top_level_dir* chỉ được lưu trong thời gian thực hiện lệnh gọi *discover*.

      .. versionchanged:: 3.14
         *start_dir* một lần nữa có thể là một :term:`namespace package`.

   Các thuộc tính sau của một :class:`TestLoader` có thể được cấu hình bằng cách tạo subclass hoặc gán giá trị cho một instance:


   .. attribute:: testMethodPrefix

      Chuỗi cho biết tiền tố của các tên phương thức sẽ được hiểu là phương thức kiểm thử. Giá trị mặc định là ``'test'``.

      Điều này ảnh hưởng đến :meth:`getTestCaseNames` và tất cả các phương thức ``loadTestsFrom*``.


   .. attribute:: sortTestMethodsUsing

      Hàm được dùng để so sánh tên phương thức khi sắp xếp chúng trong
      :meth:`getTestCaseNames` và tất cả các phương thức ``loadTestsFrom*``.


   .. attribute:: suiteClass

      Đối tượng có thể gọi được dùng để tạo một test suite từ danh sách các test. Không cần dùng phương thức nào trên đối tượng kết quả. Giá trị mặc định là
      lớp :class:`TestSuite`.

      Điều này ảnh hưởng đến tất cả các phương thức ``loadTestsFrom*``.

   .. attribute:: testNamePatterns

      Danh sách các mẫu tên test dùng ký tự đại diện theo kiểu Unix shell mà các phương thức test phải khớp để được đưa vào các test suite (xem tùy chọn ``-k``).

      Nếu thuộc tính này không phải là ``None`` (giá trị mặc định), tất cả các phương thức kiểm thử được đưa vào các test suite phải khớp với một trong các mẫu trong danh sách này. Lưu ý rằng việc khớp luôn được thực hiện bằng :meth:`fnmatch.fnmatchcase`, vì vậy không giống như các mẫu được truyền cho tùy chọn ``-k``, các mẫu chuỗi con đơn giản sẽ phải được chuyển đổi bằng các ký tự đại diện ``*``.

      Điều này ảnh hưởng đến tất cả các phương thức ``loadTestsFrom*``.

      .. versionadded:: 3.7


.. class:: TestResult

   Lớp này được dùng để tổng hợp thông tin về những kiểm thử đã thành công và những kiểm thử đã thất bại.

   Một đối tượng :class:`TestResult` lưu trữ kết quả của một tập hợp kiểm thử.  :class:`TestResult`
   Các lớp :class:`TestCase` và :class:`TestSuite` đảm bảo rằng kết quả được ghi lại đúng cách; tác giả kiểm thử không cần lo lắng về việc ghi lại kết quả của các kiểm thử.

   Các framework kiểm thử được xây dựng trên :mod:`!unittest` có thể muốn truy cập đối tượng
   :class:`TestResult` được tạo ra khi chạy một tập hợp kiểm thử cho mục đích báo cáo; một thực thể :class:`TestResult` được trả về bởi
   phương thức :meth:`!TestRunner.run` cho mục đích này.

   Các instance :class:`TestResult` có những thuộc tính sau đây, hữu ích khi kiểm tra kết quả chạy một tập hợp các bài kiểm thử:


   .. attribute:: errors

      Danh sách chứa các tuple 2 phần tử gồm các instance :class:`TestCase` và các chuỗi chứa traceback đã được định dạng. Mỗi tuple đại diện cho một bài kiểm thử phát sinh ngoại lệ không mong đợi.

   .. attribute:: failures

      Danh sách chứa các tuple 2 phần tử gồm các instance :class:`TestCase` và các chuỗi chứa traceback đã được định dạng. Mỗi tuple đại diện cho một bài kiểm thử trong đó lỗi được báo hiệu rõ ràng bằng các phương thức :ref:`assert\*methods <assert-methods>`.

   .. attribute:: skipped

      Danh sách chứa các tuple 2 phần tử gồm các instance :class:`TestCase` và các chuỗi chứa lý do bỏ qua bài kiểm thử.

      .. versionadded:: 3.1

   .. attribute:: expectedFailures

      Danh sách chứa các tuple 2 phần tử gồm các instance :class:`TestCase` và các chuỗi chứa traceback đã được định dạng. Mỗi tuple đại diện cho một lỗi hoặc ngoại lệ được dự kiến của test case.

   .. attribute:: unexpectedSuccesses

      Danh sách chứa các instance :class:`TestCase` được đánh dấu là lỗi dự kiến nhưng đã chạy thành công.

   .. attribute:: collectedDurations

      Một danh sách chứa các bộ 2 phần tử gồm tên các trường hợp kiểm thử và các số thực biểu thị thời gian đã trôi qua của mỗi kiểm thử được chạy.

      .. versionadded:: 3.12

   .. attribute:: shouldStop

      Đặt thành ``True`` khi việc thực thi các kiểm thử cần được dừng bởi :meth:`stop`.

   .. attribute:: testsRun

      Tổng số kiểm thử đã chạy cho đến thời điểm hiện tại.

   .. attribute:: buffer

      Nếu đặt thành true, ``sys.stdout`` và ``sys.stderr`` sẽ được đệm trong khoảng giữa
      việc gọi :meth:`startTest` và :meth:`stopTest`. Kết quả đầu ra được thu thập sẽ chỉ được ghi ra ``sys.stdout`` và ``sys.stderr`` thực tế nếu kiểm thử thất bại hoặc xảy ra lỗi. Mọi kết quả đầu ra cũng được đính kèm vào thông báo thất bại / lỗi.

      .. versionadded:: 3.2

   .. attribute:: failfast

      Nếu đặt thành true, :meth:`stop` sẽ được gọi khi xảy ra lỗi hoặc thất bại đầu tiên, dừng lượt chạy kiểm thử.

      .. versionadded:: 3.2

   .. attribute:: tb_locals

      Nếu đặt thành true, các biến cục bộ sẽ được hiển thị trong traceback.

      .. versionadded:: 3.5

   .. method:: wasSuccessful()

      Trả về ``True`` nếu tất cả các kiểm thử đã chạy cho đến nay đều đạt, nếu không thì trả về ``False``.

      .. versionchanged:: 3.4
         Trả về ``False`` nếu có bất kỳ :attr:`unexpectedSuccesses` nào từ các kiểm thử được đánh dấu bằng decorator :deco:`expectedFailure`.

   .. method:: stop()

      Có thể gọi phương thức này để báo hiệu rằng tập hợp các kiểm thử đang chạy nên bị hủy bằng cách đặt thuộc tính :attr:`shouldStop` thành ``True``.
      Các đối tượng :class:`!TestRunner` nên tuân theo cờ này và trả về mà không chạy thêm bất kỳ kiểm thử nào.

      Ví dụ: tính năng này được lớp :class:`TextTestRunner` sử dụng để dừng test framework khi người dùng phát tín hiệu ngắt từ bàn phím. Các công cụ tương tác cung cấp các triển khai :class:`!TestRunner` có thể sử dụng tính năng này theo cách tương tự.

   Các phương thức sau đây của lớp :class:`TestResult` được dùng để duy trì các cấu trúc dữ liệu nội bộ và có thể được mở rộng trong các lớp con để hỗ trợ thêm các yêu cầu báo cáo. Điều này đặc biệt hữu ích khi xây dựng các công cụ hỗ trợ báo cáo tương tác trong lúc các kiểm thử đang được chạy.


   .. method:: startTest(test)

      Được gọi khi test case *test* sắp được chạy.

   .. method:: stopTest(test)

      Được gọi sau khi test case *test* đã được thực thi, bất kể kết quả ra sao.

   .. method:: startTestRun()

      Được gọi một lần trước khi bất kỳ test nào được thực thi.

      .. versionadded:: 3.1


   .. method:: stopTestRun()

      Được gọi một lần sau khi tất cả test đã được thực thi.

      .. versionadded:: 3.1


   .. method:: addError(test, err)

      Được gọi khi test case *test* phát sinh một ngoại lệ không mong muốn. *err* là một tuple có dạng do :func:`sys.exc_info`: ``(type, value, traceback)`` trả về.

      Triển khai mặc định nối thêm một tuple ``(test, formatted_err)`` vào thuộc tính :attr:`errors` của instance, trong đó *formatted_err* là traceback đã được định dạng, bắt nguồn từ *err*.


   .. method:: addFailure(test, err)

      Được gọi khi test case *test* báo hiệu một lỗi thất bại. *err* là một tuple có dạng do :func:`sys.exc_info`: ``(type, value, traceback)`` trả về.

      Triển khai mặc định nối thêm một tuple ``(test, formatted_err)`` vào thuộc tính :attr:`failures` của instance, trong đó *formatted_err* là traceback đã được định dạng, bắt nguồn từ *err*.


   .. method:: addSuccess(test)

      Được gọi khi test case *test* thành công.

      Phần triển khai mặc định không thực hiện thao tác nào.


   .. method:: addSkip(test, reason)

      Được gọi khi test case *test* bị bỏ qua. *reason* là lý do mà test đưa ra để bỏ qua.

      Phần triển khai mặc định thêm một tuple ``(test, reason)`` vào thuộc tính :attr:`skipped` của instance.


   .. method:: addExpectedFailure(test, err)

      Được gọi khi test case *test* thất bại hoặc xảy ra lỗi, nhưng được đánh dấu bằng decorator :deco:`expectedFailure`.

      Phần triển khai mặc định thêm một tuple ``(test, formatted_err)`` vào thuộc tính :attr:`expectedFailures` của instance, trong đó *formatted_err* là traceback đã được định dạng, lấy từ *err*.


   .. method:: addUnexpectedSuccess(test)

      Được gọi khi test case *test* được đánh dấu bằng
      :deco:`expectedFailure` decorator nhưng đã thành công.

      Cách triển khai mặc định thêm test vào
      :attr:`unexpectedSuccesses` của instance.


   .. method:: addSubTest(test, subtest, outcome)

      Được gọi khi một subtest kết thúc. *test* là test case tương ứng với test method. *subtest* là một
      :class:`TestCase` instance tùy chỉnh mô tả subtest.

      Nếu *outcome* là :const:`None`, subtest đã thành công. Nếu không, subtest đã thất bại với một exception, trong đó *outcome* là một tuple có dạng được trả về bởi :func:`sys.exc_info`: ``(type, value, traceback)``.

      Cách triển khai mặc định không làm gì khi outcome là thành công và ghi nhận các lỗi của subtest như những lỗi thông thường.

      .. versionadded:: 3.4

   .. method:: addDuration(test, elapsed)

      Được gọi khi trường hợp kiểm thử kết thúc. *elapsed* là thời gian được biểu thị bằng giây và bao gồm cả thời gian thực thi các hàm cleanup.

      .. versionadded:: 3.12

.. class:: TextTestResult(stream, descriptions, verbosity, *, durations=None)

   Một triển khai cụ thể của :class:`TestResult` được sử dụng bởi
   :class:`TextTestRunner`. Các lớp con nên chấp nhận ``**kwargs`` để đảm bảo khả năng tương thích khi interface thay đổi.

   .. versionadded:: 3.2

   .. versionchanged:: 3.12
      Đã thêm tham số từ khóa *durations*.

.. data:: defaultTestLoader

   Instance của lớp :class:`TestLoader` предназначено để dùng chung. Nếu không cần tùy chỉnh :class:`TestLoader`, có thể sử dụng instance này thay vì liên tục tạo các instance mới.


.. class:: TextTestRunner(stream=None, descriptions=True, verbosity=1, failfast=False, \
                          buffer=False, resultclass=None, warnings=None, *, \ tb_locals=False, durations=None)

   Một triển khai test runner cơ bản xuất kết quả ra một stream. Nếu *stream* là ``None``, giá trị mặc định, thì :data:`sys.stderr` được sử dụng làm output stream. Lớp này có một vài tham số có thể cấu hình, nhưng về cơ bản rất đơn giản. Các ứng dụng đồ họa chạy các test suite nên cung cấp những triển khai thay thế. Các triển khai như vậy nên chấp nhận ``**kwargs`` vì interface để xây dựng các runner thay đổi khi các tính năng được thêm vào unittest.

   Theo mặc định, runner này hiển thị :exc:`DeprecationWarning`,
   :exc:`PendingDeprecationWarning`, :exc:`ResourceWarning` và
   :exc:`ImportWarning` ngay cả khi chúng :ref:`bị bỏ qua theo mặc định <warning-ignored>`. Có thể ghi đè hành vi này bằng các tùy chọn :option:`!-Wd` hoặc :option:`!-Wa` của Python (xem :ref:`Kiểm soát cảnh báo <using-on-warnings>`) và đặt *cảnh báo* thành ``None``.

   .. versionchanged:: 3.2
      Đã thêm tham số *cảnh báo*.

   .. versionchanged:: 3.2
      Luồng mặc định được đặt thành :data:`sys.stderr` tại thời điểm khởi tạo thay vì thời điểm import.

   .. versionchanged:: 3.5
      Đã thêm tham số *tb_locals*.

   .. versionchanged:: 3.12
      Đã thêm tham số *durations*.

   .. method:: _makeResult()

      Phương thức này trả về thực thể của ``TestResult`` được :meth:`run` sử dụng. Phương thức này không предназначен để được gọi trực tiếp, nhưng có thể được ghi đè trong các lớp con để cung cấp ``TestResult`` tùy chỉnh.

      ``_makeResult()`` khởi tạo lớp hoặc callable được truyền vào hàm khởi tạo ``TextTestRunner`` dưới dạng đối số ``resultclass``. Theo mặc định, giá trị này là :class:`TextTestResult` nếu không cung cấp ``resultclass``. Lớp kết quả được khởi tạo với các đối số sau đây::

        stream, descriptions, verbosity

   .. method:: run(test)

      Phương thức này là giao diện công khai chính của ``TextTestRunner``. Phương thức này nhận một thực thể :class:`TestSuite` hoặc :class:`TestCase`. Một
      :class:`TestResult` được tạo bằng cách gọi
      :func:`_makeResult` và các bài kiểm thử được chạy, sau đó kết quả được in ra stdout.


.. function:: main(module='__main__', defaultTest=None, argv=None, testRunner=None, \
                   testLoader=unittest.defaultTestLoader, exit=True, verbosity=1, \ failfast=None, catchbreak=None, buffer=None, warnings=None)

   Một chương trình dòng lệnh tải một tập hợp bài kiểm thử từ *module* và chạy chúng; chương trình này chủ yếu dùng để giúp các module kiểm thử có thể được thực thi một cách thuận tiện. Cách sử dụng đơn giản nhất của hàm này là thêm dòng sau vào cuối tập lệnh kiểm thử::

      if __name__ == '__main__':
          unittest.main()

   Bạn có thể chạy các bài kiểm thử với thông tin chi tiết hơn bằng cách truyền đối số verbosity::

      if __name__ == '__main__':
          unittest.main(verbosity=2)

   Đối số *defaultTest* có thể là tên của một bài kiểm thử đơn lẻ hoặc một iterable chứa các tên bài kiểm thử cần chạy nếu không có tên bài kiểm thử nào được chỉ định qua *argv*. Nếu không được chỉ định hoặc là ``None`` và không có tên bài kiểm thử nào được cung cấp qua *argv*, tất cả các bài kiểm thử được tìm thấy trong *module* sẽ được chạy.

   Đối số *argv* có thể là một danh sách các tùy chọn được truyền cho chương trình, trong đó phần tử đầu tiên là tên chương trình. Nếu không được chỉ định hoặc là ``None``, các giá trị của :data:`sys.argv` sẽ được sử dụng.

   Đối số *testRunner* có thể là một lớp test runner hoặc một instance đã được tạo của lớp đó. Theo mặc định, ``main`` gọi :func:`sys.exit` với mã thoát cho biết các bài kiểm thử đã chạy thành công (0) hay thất bại (1). Mã thoát 5 cho biết không có bài kiểm thử nào được chạy hoặc bị bỏ qua.

   Đối số *testLoader* phải là một instance :class:`TestLoader`, và mặc định là :data:`defaultTestLoader`.

   ``main`` hỗ trợ việc được sử dụng từ trình thông dịch tương tác bằng cách truyền đối số ``exit=False``. Thao tác này hiển thị kết quả trên đầu ra tiêu chuẩn mà không gọi :func:`sys.exit`::

      >>> from unittest import main
      >>> main(module='test_module', exit=False)

   Các tham số *failfast*, *catchbreak* và *buffer* có tác dụng giống như các `tùy chọn dòng lệnh <command-line options_>`_ cùng tên.

   Đối số *warnings* chỉ định :ref:`bộ lọc cảnh báo <warning-filter>` sẽ được sử dụng trong khi chạy các bài kiểm thử. Nếu không được chỉ định, nó sẽ vẫn là ``None`` nếu một :option:`!-W` tùy chọn được truyền cho :program:`python` (xem :ref:`Kiểm soát cảnh báo <using-on-warnings>`), nếu không thì sẽ được đặt thành ``'default'``.

   Việc gọi ``main`` trả về một đối tượng có thuộc tính ``result`` chứa kết quả của các bài kiểm thử được chạy dưới dạng :class:`unittest.TestResult`.

   .. versionchanged:: 3.1
      Đã thêm tham số *exit*.

   .. versionchanged:: 3.2
      Đã thêm các tham số *verbosity*, *failfast*, *catchbreak*, *buffer* và *warnings*.

   .. versionchanged:: 3.4
      Tham số *defaultTest* được thay đổi để cũng chấp nhận một iterable chứa các tên bài kiểm thử.


.. _load_tests-protocol:

.. _`load_tests Protocol`:

Giao thức load_tests
####################

.. versionadded:: 3.2

Các module hoặc package có thể tùy chỉnh cách tải các bài kiểm thử từ chúng trong các lần chạy kiểm thử thông thường hoặc quá trình phát hiện bài kiểm thử bằng cách triển khai một hàm có tên ``load_tests``.

Nếu một module kiểm thử định nghĩa ``load_tests`` thì module đó sẽ được gọi bởi
:meth:`TestLoader.loadTestsFromModule` với các đối số sau::

    load_tests(loader, standard_tests, pattern)

trong đó *pattern* được truyền thẳng từ ``loadTestsFromModule``. Giá trị mặc định là ``None``.

Hàm này phải trả về một :class:`TestSuite`.

*loader* là instance của :class:`TestLoader` thực hiện việc tải. *standard_tests* là các kiểm thử được tải theo mặc định từ module. Các module kiểm thử thường chỉ muốn thêm hoặc xóa kiểm thử khỏi tập kiểm thử tiêu chuẩn. Đối số thứ ba được sử dụng khi tải các package trong quá trình phát hiện kiểm thử.

Một hàm ``load_tests`` điển hình tải các kiểm thử từ một tập hợp cụ thể gồm
:class:`TestCase` các lớp có thể trông như::

    test_cases = (TestCase1, TestCase2, TestCase3)

    def load_tests(loader, tests, pattern):
        suite = TestSuite()
        for test_class in test_cases:
            tests = loader.loadTestsFromTestCase(test_class)
            suite.addTests(tests)
        return suite

Nếu quá trình discovery được bắt đầu trong một thư mục chứa package, từ dòng lệnh hoặc bằng cách gọi :meth:`TestLoader.discover`, thì package
:file:`__init__.py` sẽ được kiểm tra để tìm ``load_tests``. Nếu hàm đó không tồn tại, discovery sẽ đệ quy vào package như với bất kỳ thư mục nào khác. Nếu không, việc discovery các test của package sẽ do ``load_tests`` đảm nhiệm; hàm này được gọi với các đối số sau đây::

    load_tests(loader, standard_tests, pattern)

Hàm này phải trả về một :class:`TestSuite` đại diện cho tất cả các test trong package. (``standard_tests`` sẽ chỉ chứa các test được thu thập từ :file:`__init__.py`.)

Vì pattern được truyền vào ``load_tests``, package có thể tiếp tục (và có khả năng sửa đổi) quá trình discovery test. Một hàm ``load_tests`` 'không làm gì' cho test package sẽ có dạng như sau::

    def load_tests(loader, standard_tests, pattern):
        # thư mục cấp cao nhất được lưu trong instance của loader
        this_dir = os.path.dirname(__file__)
        package_tests = loader.discover(start_dir=this_dir, pattern=pattern)
        standard_tests.addTests(package_tests)
        return standard_tests

.. versionchanged:: 3.5
   Discovery không còn kiểm tra tên package để khớp với *pattern* vì tên package không thể khớp với pattern mặc định.



.. _`Class and Module Fixtures`:

Fixture của lớp và mô-đun
-------------------------

Các fixture cấp class và module được triển khai trong :class:`TestSuite`. Khi test suite gặp một test từ một class mới thì
:meth:`~TestCase.tearDownClass` của class trước đó (nếu có) sẽ được gọi, tiếp theo là :meth:`~TestCase.setUpClass` của class mới.

Tương tự, nếu một test thuộc module khác với test trước đó thì ``tearDownModule`` của module trước đó sẽ được chạy, tiếp theo là ``setUpModule`` của module mới.

Sau khi tất cả các test đã chạy, ``tearDownClass`` và ``tearDownModule`` cuối cùng sẽ được chạy.

Lưu ý rằng các fixture dùng chung không hoạt động tốt với các tính năng [tiềm năng] như chạy test song song và chúng phá vỡ tính độc lập giữa các test. Hãy sử dụng chúng một cách thận trọng.

Thứ tự mặc định của các test được tạo bởi unittest test loader là nhóm tất cả các test từ cùng module và class lại với nhau. Điều này sẽ khiến ``setUpClass`` / ``setUpModule`` (v.v.) được gọi chính xác một lần cho mỗi class và module. Nếu bạn xáo trộn thứ tự để các test từ các module và class khác nhau nằm cạnh nhau, thì các hàm fixture dùng chung này có thể được gọi nhiều lần trong một lần chạy test.

Fixture dùng chung không được thiết kế để hoạt động với các suite có thứ tự không chuẩn. Một ``BaseTestSuite`` vẫn tồn tại dành cho các framework không muốn hỗ trợ fixture dùng chung.

Nếu có bất kỳ ngoại lệ nào được phát sinh trong một trong các hàm fixture dùng chung, bài kiểm thử sẽ được báo cáo là lỗi. Vì không có phiên bản kiểm thử tương ứng, một đối tượng ``_ErrorHolder`` (có cùng giao diện với một
:class:`TestCase`) được tạo để biểu diễn lỗi. Nếu bạn chỉ sử dụng test runner unittest tiêu chuẩn thì chi tiết này không quan trọng, nhưng nếu bạn là tác giả framework thì nó có thể liên quan.


setUpClass và tearDownClass
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Các phương thức này phải được triển khai dưới dạng class method::

    import unittest

    class Test(unittest.TestCase):
        @classmethod
        def setUpClass(cls):
            cls._connection = createExpensiveConnectionObject()

        @classmethod
        def tearDownClass(cls):
            cls._connection.destroy()

Nếu muốn ``setUpClass`` và ``tearDownClass`` trên các lớp cơ sở được gọi, bạn phải tự gọi chúng. Các triển khai trong
:class:`TestCase` là các triển khai rỗng.

Nếu một ngoại lệ được phát sinh trong ``setUpClass``, các bài kiểm thử trong lớp sẽ không được chạy và ``tearDownClass`` sẽ không được chạy. Các lớp bị bỏ qua sẽ không chạy ``setUpClass`` hoặc ``tearDownClass``. Nếu ngoại lệ là một
Nếu xảy ra ngoại lệ :exc:`SkipTest` thì lớp sẽ được báo cáo là đã bị bỏ qua thay vì là lỗi.


setUpModule và tearDownModule
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. function:: setUpModule
              tearDownModule
   :no-typesetting:

Các hàm này nên được triển khai dưới dạng các hàm::

    def setUpModule():
        createConnection()

    def tearDownModule():
        closeConnection()

Nếu xảy ra ngoại lệ trong ``setUpModule`` thì không có kiểm thử nào trong mô-đun được chạy và ``tearDownModule`` sẽ không được chạy. Nếu ngoại lệ là
ngoại lệ :exc:`SkipTest` thì mô-đun sẽ được báo cáo là đã bị bỏ qua thay vì là lỗi.

Để thêm mã dọn dẹp phải được chạy ngay cả khi xảy ra ngoại lệ, hãy sử dụng ``addModuleCleanup``:


.. function:: addModuleCleanup(function, /, *args, **kwargs)

   Thêm một hàm sẽ được gọi sau :func:`tearDownModule` để dọn dẹp các tài nguyên được sử dụng trong test class. Các hàm sẽ được gọi theo thứ tự ngược với thứ tự chúng được thêm vào (:abbr:`LIFO (last-in, first-out)`). Chúng được gọi với mọi đối số và đối số từ khóa được truyền vào
   :meth:`addModuleCleanup` khi chúng được thêm vào.

   Nếu :meth:`setUpModule` không thành công, nghĩa là :func:`tearDownModule` không được gọi, thì mọi hàm dọn dẹp đã được thêm vào vẫn sẽ được gọi.

   .. versionadded:: 3.8


.. function:: enterModuleContext(cm)

   Đi vào :term:`context manager` được cung cấp. Nếu thành công, đồng thời thêm phương thức :meth:`~object.__exit__` của nó làm hàm dọn dẹp bằng cách
   :func:`addModuleCleanup` và trả về kết quả của
   phương thức :meth:`~object.__enter__`.

   .. versionadded:: 3.11


.. function:: doModuleCleanups()

   Hàm này luôn được gọi sau :func:`tearDownModule`, hoặc sau :func:`setUpModule` nếu :func:`setUpModule` phát sinh ngoại lệ.

   Nó chịu trách nhiệm gọi tất cả các hàm cleanup được thêm bởi
   :func:`addModuleCleanup`. Nếu bạn cần các hàm cleanup được gọi *trước* :func:`tearDownModule` thì bạn có thể gọi
   :func:`doModuleCleanups` chính bạn.

   :func:`doModuleCleanups` lấy từng phương thức ra khỏi ngăn xếp các hàm cleanup, vì vậy nó có thể được gọi bất kỳ lúc nào.

   .. versionadded:: 3.8


.. _`Signal Handling`:

Xử lý tín hiệu
--------------

.. versionadded:: 3.2

Tùy chọn dòng lệnh :option:`-c/--catch <unittest -c>` của unittest, cùng với tham số ``catchbreak`` của :func:`unittest.main`, cung cấp cách xử lý thân thiện hơn đối với control-C trong khi chạy test. Khi bật behavior catch break, control-C sẽ cho phép test hiện đang chạy hoàn tất, sau đó quá trình chạy test sẽ kết thúc và báo cáo tất cả kết quả tính đến thời điểm đó. Control-C lần thứ hai sẽ raise một :exc:`KeyboardInterrupt` theo cách thông thường.

Trình xử lý tín hiệu control-c cố gắng duy trì khả năng tương thích với mã hoặc các bài kiểm thử cài đặt trình xử lý :const:`signal.SIGINT` riêng. Nếu trình xử lý ``unittest`` được gọi nhưng *isn't* trình xử lý :const:`signal.SIGINT` đã cài đặt, tức là nó đã bị hệ thống đang được kiểm thử thay thế và ủy quyền xử lý, thì nó sẽ gọi trình xử lý mặc định. Đây thường là hành vi được mã thay thế một trình xử lý đã cài đặt và ủy quyền xử lý cho trình xử lý đó mong đợi. Đối với các bài kiểm thử riêng lẻ cần tắt ``unittest`` việc xử lý control-c, có thể sử dụng decorator :func:`removeHandler`.

Có một số hàm tiện ích dành cho tác giả framework để bật chức năng xử lý control-c trong các test framework.

.. function:: installHandler()

   Cài đặt trình xử lý control-c. Khi nhận được một :const:`signal.SIGINT` (thường là do người dùng nhấn control-c), tất cả các kết quả đã đăng ký sẽ được gọi :meth:`~TestResult.stop`.


.. function:: registerResult(result)

   Đăng ký một đối tượng :class:`TestResult` để xử lý control-c. Việc đăng ký một kết quả sẽ lưu một weak reference đến kết quả đó, vì vậy không ngăn kết quả được garbage collection.

   Việc đăng ký một đối tượng :class:`TestResult` không gây ra tác dụng phụ nếu tính năng xử lý control-c chưa được bật, vì vậy các test framework có thể vô điều kiện đăng ký tất cả kết quả mà chúng tạo ra, bất kể tính năng xử lý có được bật hay không.


.. function:: removeResult(result)

   Xóa một kết quả đã đăng ký. Sau khi một kết quả đã bị xóa thì
   :meth:`~TestResult.stop` sẽ không còn được gọi trên đối tượng kết quả đó để phản hồi control-c.


.. function:: removeHandler(function=None)

   Khi được gọi mà không có đối số, hàm này sẽ xóa trình xử lý control-c nếu trình xử lý này đã được cài đặt. Hàm này cũng có thể được dùng làm test decorator để tạm thời xóa trình xử lý trong khi test đang được thực thi::

      @unittest.removeHandler
      def test_signal_handling(self):
          ...

.. _`Simple Smalltalk Testing: With Patterns`: https://web.archive.org/web/20150315073817/http://www.xprogramming.com/testfram.htm
.. _`pytest`: https://docs.pytest.org/
.. _`The Python Testing Tools Taxonomy`: https://wiki.python.org/moin/PythonTestingToolsTaxonomy
.. _`Testing in Python Mailing List`: http://lists.idyll.org/listinfo/testing-in-python
.. _`Buildbot`: https://buildbot.net/
.. _`Jenkins`: https://www.jenkins.io/
.. _`GitHub Actions`: https://github.com/features/actions
.. _`AppVeyor`: https://www.appveyor.com/
