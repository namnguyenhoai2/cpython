:mod:`!doctest` --- Kiểm thử các ví dụ Python tương tác
=======================================================

.. module:: doctest
   :synopsis: Kiểm thử các đoạn mã trong docstring.

.. moduleauthor:: Tim Peters <tim@python.org>
.. sectionauthor:: Tim Peters <tim@python.org>
.. sectionauthor:: Moshe Zadka <moshez@debian.org>
.. sectionauthor:: Edward Loper <edloper@users.sourceforge.net>

**Mã nguồn:** :source:`Lib/doctest.py`

--------------

Module :mod:`!doctest` tìm kiếm các đoạn văn bản trông giống như những phiên làm việc Python tương tác, sau đó thực thi các phiên đó để xác minh rằng chúng hoạt động chính xác như được hiển thị. Có một số cách phổ biến để sử dụng doctest:

* Kiểm tra xem docstring của một module có được cập nhật hay không bằng cách xác minh rằng tất cả các ví dụ tương tác vẫn hoạt động như được ghi lại.

* Thực hiện kiểm thử hồi quy bằng cách xác minh rằng các ví dụ tương tác từ một tệp kiểm thử hoặc một đối tượng kiểm thử hoạt động như mong đợi.

* Viết tài liệu hướng dẫn cho một package, minh họa phong phú bằng các ví dụ đầu vào–đầu ra. Tùy thuộc vào việc nhấn mạnh các ví dụ hay phần văn bản thuyết minh, cách này mang màu sắc của “kiểm thử bằng văn bản” hoặc “tài liệu có thể thực thi”.

Đây là một module hoàn chỉnh nhưng nhỏ::

   """
   This is the "example" module.

   The example module supplies one function, factorial().  For example,

   >>> factorial(5)
   120
   """

   def factorial(n):
       """Return the factorial of n, an exact integer >= 0.

       >>> [factorial(n) for n in range(6)]
       [1, 1, 2, 6, 24, 120]
       >>> factorial(30)
       265252859812191058636308480000000
       >>> factorial(-1)
       Traceback (most recent call last):
           ...
       ValueError: n must be >= 0

       Factorials of floats are OK, but the float must be an exact integer:
       >>> factorial(30.1)
       Traceback (most recent call last):
           ...
       ValueError: n must be exact integer
       >>> factorial(30.0)
       265252859812191058636308480000000

       It must also not be ridiculously large:
       >>> factorial(1e100)
       Traceback (most recent call last):
           ...
       OverflowError: n too large
       """

       import math
       if not n >= 0:
           raise ValueError("n must be >= 0")
       if math.floor(n) != n:
           raise ValueError("n must be exact integer")
       if n+1 == n:  # bắt một giá trị như 1e300
           raise OverflowError("n too large")
       result = 1
       factor = 2
       while factor <= n:
           result *= factor
           factor += 1
       return result


   if __name__ == "__main__":
       import doctest
       doctest.testmod()

Nếu bạn chạy :file:`example.py` trực tiếp từ dòng lệnh, :mod:`!doctest` sẽ phát huy tác dụng kỳ diệu của nó:

.. code-block:: shell-session

   $ python example.py
   $

Không có đầu ra! Điều đó là bình thường và có nghĩa là tất cả các ví dụ đều hoạt động. Truyền ``-v`` cho script, :mod:`!doctest` sẽ in nhật ký chi tiết về những gì nó đang thử, rồi in bản tóm tắt ở cuối:

.. code-block:: shell-session

   $ python example.py -v
   Trying:
       factorial(5)
   Expecting:
       120
   ok
   Trying:
       [factorial(n) for n in range(6)]
   Expecting:
       [1, 1, 2, 6, 24, 120]
   ok

Và cứ tiếp tục như vậy, cuối cùng kết thúc bằng:

.. code-block:: none

   Trying:
       factorial(1e100)
   Expecting:
       Traceback (most recent call last):
           ...
       OverflowError: n too large
   ok
   2 items passed all tests:
      1 test in __main__
      6 tests in __main__.factorial
   7 tests in 2 items.
   7 passed.
   Test passed.
   $

Đó là tất cả những gì bạn cần biết để bắt đầu sử dụng :mod:`!doctest` hiệu quả! Hãy bắt tay vào làm. Các phần sau cung cấp đầy đủ chi tiết. Lưu ý rằng có rất nhiều ví dụ về doctest trong bộ kiểm thử và các thư viện Python chuẩn. Bạn có thể tìm thấy những ví dụ đặc biệt hữu ích trong tệp kiểm thử chuẩn
:file:`Lib/test/test_doctest/test_doctest.py`.

.. versionadded:: 3.13
   Theo mặc định, đầu ra được tô màu và có thể
   :ref:`được điều khiển bằng các biến môi trường <using-on-controlling-color>`.


.. _doctest-simple-testmod:

Cách sử dụng đơn giản: Kiểm tra các ví dụ trong docstring
---------------------------------------------------------

Cách đơn giản nhất để bắt đầu sử dụng doctest (nhưng không nhất thiết là cách bạn sẽ tiếp tục sử dụng) là kết thúc mỗi module :mod:`!M` bằng::

   if __name__ == "__main__":
       import doctest
       doctest.testmod()

:mod:`!doctest` sau đó kiểm tra các docstring trong module :mod:`!M`.

Chạy module dưới dạng một script sẽ khiến các ví dụ trong docstring được thực thi và kiểm tra::

   python M.py

Lệnh này sẽ không hiển thị gì trừ khi một ví dụ thất bại; khi đó, (các) ví dụ bị lỗi và (các) nguyên nhân gây ra (các) lỗi sẽ được in ra stdout, và dòng cuối cùng của kết quả là ``***Test Failed*** N failures.``, trong đó *N* là số ví dụ đã thất bại.

Thay vào đó, hãy chạy lệnh này với tùy chọn ``-v``::

   python M.py -v

và một báo cáo chi tiết về tất cả các ví dụ đã thử được in ra đầu ra tiêu chuẩn, cùng với nhiều bản tóm tắt khác nhau ở cuối.

Bạn có thể buộc chế độ chi tiết bằng cách truyền ``verbose=True`` cho :func:`testmod`, hoặc tắt chế độ này bằng cách truyền ``verbose=False``.  Trong cả hai trường hợp đó,
:data:`sys.argv` không được :func:`testmod` kiểm tra (vì vậy việc truyền ``-v`` hay không cũng không có tác dụng).

Ngoài ra còn có một lối tắt trên dòng lệnh để chạy :func:`testmod`, xem phần
:ref:`doctest-cli`.

Để biết thêm thông tin về :func:`testmod`, hãy xem phần :ref:`doctest-basic-api`.


.. _doctest-simple-testfile:

Cách sử dụng đơn giản: Kiểm tra các ví dụ trong tệp văn bản
-----------------------------------------------------------

Một ứng dụng đơn giản khác của doctest là kiểm thử các ví dụ tương tác trong một tệp văn bản.  Việc này có thể được thực hiện bằng hàm :func:`testfile`::

   import doctest
   doctest.testfile("example.txt")

Script ngắn đó thực thi và xác minh mọi ví dụ Python tương tác có trong tệp :file:`example.txt`. Nội dung tệp được xử lý như thể đó là một docstring khổng lồ duy nhất; tệp không cần chứa một chương trình Python! Ví dụ: có thể :file:`example.txt` chứa nội dung sau:

.. code-block:: none

   The ``example`` module
   ======================

   Using ``factorial``
   -------------------

   This is an example text file in reStructuredText format.  First import
   ``factorial`` from the ``example`` module:

       >>> from example import factorial

   Now use it:

       >>> factorial(6)
       120

Chạy ``doctest.testfile("example.txt")`` sau đó sẽ phát hiện lỗi trong tài liệu này::

   File "./example.txt", line 14, in example.txt
   Failed example:
       factorial(6)
   Expected:
       120
   Got:
       720

Tương tự như :func:`testmod`, :func:`testfile` sẽ không hiển thị gì trừ khi một ví dụ bị lỗi. Nếu một ví dụ thực sự bị lỗi, thì (các) ví dụ bị lỗi và (các) nguyên nhân gây lỗi sẽ được in ra stdout, sử dụng cùng định dạng như
:func:`!testmod`.

Theo mặc định, :func:`testfile` tìm các tệp trong thư mục của module gọi nó. Xem phần :ref:`doctest-basic-api` để biết mô tả về các đối số tùy chọn có thể dùng để yêu cầu nó tìm tệp ở những vị trí khác.

Giống như :func:`testmod`, mức độ chi tiết của :func:`testfile` có thể được đặt bằng switch dòng lệnh ``-v`` hoặc bằng đối số từ khóa tùy chọn *verbose*.

Ngoài ra còn có một phím tắt dòng lệnh để chạy :func:`testfile`; xem phần
:ref:`doctest-cli`.

Để biết thêm thông tin về :func:`testfile`, hãy xem phần :ref:`doctest-basic-api`.


.. _doctest-cli:

Cách sử dụng trên dòng lệnh
---------------------------

Có thể gọi module :mod:`!doctest` dưới dạng một script từ dòng lệnh:

.. code-block:: bash

   python -m doctest [-v] [-o OPTION] [-f] file [file ...]

.. program:: doctest

.. option:: -v, --verbose

   Báo cáo chi tiết về tất cả các ví dụ đã thử được in ra đầu ra tiêu chuẩn, cùng với nhiều bản tóm tắt khác nhau ở cuối::

      python -m doctest -v example.py

   Thao tác này sẽ nhập :file:`example.py` dưới dạng một module độc lập và chạy
   :func:`testmod` trên đó. Lưu ý rằng thao tác này có thể không hoạt động chính xác nếu tệp là một phần của package và nhập các submodule khác từ package đó.

   Nếu tên tệp không kết thúc bằng :file:`.py`, :mod:`!doctest` sẽ suy ra rằng tệp phải được chạy bằng :func:`testfile` thay thế::

      python -m doctest -v example.txt

.. option:: -o, --option <option>

   Các cờ tùy chọn kiểm soát nhiều khía cạnh khác nhau trong hành vi của doctest; xem phần
   :ref:`doctest-options`.

   .. versionadded:: 3.4

.. option:: -f, --fail-fast

   Đây là cách viết tắt của ``-o FAIL_FAST``.

   .. versionadded:: 3.4


.. _doctest-how-it-works:

Cách thức hoạt động
-------------------

Phần này xem xét chi tiết cách doctest hoạt động: nó kiểm tra những docstring nào, tìm các ví dụ tương tác ra sao, sử dụng ngữ cảnh thực thi nào, xử lý ngoại lệ như thế nào và có thể dùng các cờ tùy chọn để kiểm soát hành vi của nó ra sao. Đây là những thông tin bạn cần biết để viết các ví dụ doctest; để biết thông tin về cách thực sự chạy doctest trên các ví dụ này, hãy xem các phần sau.


.. _doctest-which-docstrings:

Những Docstring Nào Được Kiểm Tra?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Docstring của module cùng với tất cả docstring của function, class và method đều được tìm kiếm. Các object được import vào module không được tìm kiếm.

.. currentmodule:: None

.. attribute:: module.__test__
   :no-typesetting:

.. currentmodule:: doctest

Ngoài ra, có những trường hợp bạn muốn các test thuộc về một module nhưng không xuất hiện trong phần văn bản trợ giúp, do đó các test không được bao gồm trong docstring. Doctest tìm một biến cấp module có tên ``__test__`` và dùng biến này để định vị các test khác. Nếu ``M.__test__`` tồn tại, nó phải là một dict và mỗi mục ánh xạ một tên (chuỗi) tới một function object, class object hoặc chuỗi. Các docstring của function object và class object được tìm thấy từ ``M.__test__`` sẽ được tìm kiếm, còn các chuỗi được xử lý như thể chúng là docstring. Trong đầu ra, một khóa ``K`` trong ``M.__test__`` sẽ xuất hiện với tên ``M.__test__.K``.

Ví dụ, đặt khối mã này ở đầu :file:`example.py`:

.. code-block:: python

   __test__ = {
       'numbers': """
   >>> factorial(6)
   720

   >>> [factorial(n) for n in range(6)]
   [1, 1, 2, 6, 24, 120]
   """
   }

Giá trị của ``example.__test__["numbers"]`` sẽ được xem là một docstring và tất cả các test bên trong đó sẽ được chạy. Điều quan trọng cần lưu ý là giá trị này có thể trỏ tới một function, class object hoặc module; nếu vậy, :mod:`!doctest` sẽ tìm đệ quy trong chúng để lấy các docstring, sau đó quét các docstring này để tìm test.

Mọi class được tìm thấy cũng sẽ được tìm kiếm đệ quy tương tự để kiểm thử các docstring trong những method và class lồng nhau bên trong chúng.

.. note::

   ``doctest`` chỉ có thể tự động phát hiện các class và function được định nghĩa ở cấp module hoặc bên trong các class khác.

   Vì các class và function lồng nhau chỉ tồn tại khi một function bên ngoài được gọi, nên không thể phát hiện chúng. Hãy định nghĩa chúng ở bên ngoài để chúng có thể được nhìn thấy.

.. _doctest-finding-examples:

Các ví dụ trong Docstring được nhận diện như thế nào?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Trong hầu hết trường hợp, việc sao chép và dán một phiên làm việc trên interactive console sẽ hoạt động tốt, nhưng doctest không cố gắng mô phỏng chính xác bất kỳ Python shell cụ thể nào.

::

   >>> # bỏ qua các comment
   >>> x = 12
   >>> x
   12
   >>> if x == 13:
   ...     print("yes")
   ... else:
   ...     print("no")
   ...     print("NO")
   ...     print("NO!!!")
   ...
   no
   NO
   NO!!!
   >>>

.. index::
   single: >>>; interpreter prompt
   single: ...; interpreter prompt

Mọi đầu ra dự kiến phải ngay lập tức theo sau dòng ``'>>> '`` hoặc ``'... '`` cuối cùng chứa mã, và đầu ra dự kiến (nếu có) kéo dài đến dòng ``'>>> '`` tiếp theo hoặc dòng chỉ chứa khoảng trắng.

Chi tiết cần lưu ý:

* Đầu ra dự kiến không được chứa dòng chỉ gồm khoảng trắng, vì dòng như vậy được hiểu là báo hiệu kết thúc đầu ra dự kiến. Nếu đầu ra dự kiến có chứa dòng trống, hãy đặt ``<BLANKLINE>`` vào doctest example của bạn tại mỗi vị trí cần có dòng trống.

* Mọi ký tự tab cứng đều được chuyển thành khoảng trắng, sử dụng các điểm dừng tab cách nhau 8 cột. Các tab trong đầu ra do mã được kiểm thử tạo ra không bị thay đổi. Vì mọi tab cứng trong đầu ra mẫu *đều được* mở rộng, điều này có nghĩa là nếu đầu ra của mã chứa các tab cứng thì cách duy nhất để doctest có thể vượt qua là
  :const:`NORMALIZE_WHITESPACE` tùy chọn hoặc :ref:`chỉ thị <doctest-directives>` đang có hiệu lực. Ngoài ra, có thể viết lại bài kiểm thử để thu thập đầu ra và so sánh đầu ra đó với một giá trị dự kiến như một phần của bài kiểm thử. Cách xử lý tab trong mã nguồn này được đưa ra sau quá trình thử và sai, và đã chứng minh là cách ít dễ gây lỗi nhất để xử lý chúng. Có thể sử dụng một thuật toán khác để xử lý tab bằng cách viết một lớp :class:`DocTestParser` tùy chỉnh.

* Đầu ra tới stdout được capture, nhưng đầu ra tới stderr thì không (traceback của exception được capture bằng một cơ chế khác).

* Nếu bạn tiếp tục một dòng bằng dấu gạch chéo ngược trong một interactive session, hoặc vì bất kỳ lý do nào khác sử dụng dấu gạch chéo ngược, bạn nên dùng raw docstring, vốn sẽ giữ nguyên chính xác các dấu gạch chéo ngược như bạn nhập::

     >>> def f(x):
     ...     r'''Backslashes in a raw docstring: m\n'''
     ...
     >>> print(f.__doc__)
     Backslashes in a raw docstring: m\n

  Nếu không, dấu gạch chéo ngược sẽ được diễn giải như một phần của chuỗi. Ví dụ: ``\n`` ở trên sẽ được diễn giải thành một ký tự xuống dòng. Ngoài ra, bạn có thể nhân đôi mỗi dấu gạch chéo ngược trong phiên bản doctest (và không sử dụng raw string)::

     >>> def f(x):
     ...     '''Backslashes in a raw docstring: m\\n'''
     ...
     >>> print(f.__doc__)
     Backslashes in a raw docstring: m\n

* Cột bắt đầu không quan trọng::

     >>> assert "Easy!"
           >>> import math
               >>> math.floor(1.9)
               1

  and as many leading whitespace characters are stripped from the expected output
  as appeared in the initial ``'>>> '`` line that started the example.


.. _doctest-execution-context:

Bối cảnh thực thi là gì?
^^^^^^^^^^^^^^^^^^^^^^^^

Theo mặc định, mỗi khi :mod:`!doctest` tìm thấy một docstring cần kiểm thử, nó sử dụng *bản sao nông* của các biến toàn cục trong :mod:`!M`, để việc chạy các bài kiểm thử không thay đổi các biến toàn cục thực của module, đồng thời một bài kiểm thử trong :mod:`!M` không thể để lại những dấu vết vô tình giúp một bài kiểm thử khác hoạt động. Điều này có nghĩa là các ví dụ có thể tự do sử dụng mọi tên được định nghĩa ở cấp cao nhất trong :mod:`!M` và các tên được định nghĩa trước đó trong docstring đang được chạy. Các ví dụ không thể thấy những tên được định nghĩa trong các docstring khác.

Bạn có thể buộc sử dụng dict của riêng mình làm bối cảnh thực thi bằng cách truyền ``globs=your_dict`` cho :func:`testmod` hoặc :func:`testfile` thay vào đó.


.. _doctest-exceptions:

Còn ngoại lệ thì sao?
^^^^^^^^^^^^^^^^^^^^^

Không vấn đề gì, miễn là traceback là đầu ra duy nhất do ví dụ tạo ra: chỉ cần dán traceback vào. [#]_ Vì traceback chứa những chi tiết có khả năng thay đổi nhanh (chẳng hạn như đường dẫn tệp và số dòng chính xác), đây là một trường hợp mà doctest cố gắng linh hoạt trong những gì nó chấp nhận.

Ví dụ đơn giản::

   >>> [1, 2, 3].remove(42)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   ValueError: list.remove(x): x not in list

Doctest đó thành công nếu :exc:`ValueError` được phát sinh, với chi tiết ``list.remove(x): x not in list`` như được minh họa.

Đầu ra dự kiến cho một exception phải bắt đầu bằng tiêu đề traceback, có thể là một trong hai dòng sau, được thụt lề giống với dòng đầu tiên của ví dụ::

   Traceback (most recent call last):
   Traceback (innermost last):

Tiêu đề traceback được theo sau bởi một stack traceback tùy chọn, nội dung của stack này sẽ bị doctest bỏ qua. Stack traceback thường được lược bỏ hoặc sao chép nguyên văn từ một phiên tương tác.

Stack traceback được theo sau bởi phần đáng chú ý nhất: (các) dòng chứa kiểu exception và thông tin chi tiết. Đây thường là dòng cuối cùng của traceback, nhưng có thể trải dài trên nhiều dòng nếu exception có thông tin chi tiết trên nhiều dòng::

   >>> raise ValueError('multi\n    line\ndetail')
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   ValueError: multi
       line
   detail

Ba dòng cuối cùng (bắt đầu bằng :exc:`ValueError`) được so sánh với kiểu và thông tin chi tiết của exception, còn phần còn lại bị bỏ qua.

Cách làm tốt nhất là lược bỏ stack traceback, trừ khi nó bổ sung giá trị đáng kể về mặt tài liệu cho ví dụ. Vì vậy, ví dụ cuối có lẽ nên được viết như sau::

   >>> raise ValueError('multi\n    line\ndetail')
   Traceback (most recent call last):
       ...
   ValueError: multi
       line
   detail

Lưu ý rằng traceback được xử lý theo cách rất đặc biệt. Cụ thể, trong ví dụ đã viết lại, việc sử dụng ``...`` không phụ thuộc vào tùy chọn doctest's
:const:`ELLIPSIS`. Dấu ba chấm trong ví dụ đó có thể được bỏ đi, hoặc cũng có thể được thay bằng ba (hoặc ba trăm) dấu phẩy hay chữ số, hoặc một transcript được thụt lề của một tiểu phẩm Monty Python.

Có một số chi tiết bạn nên đọc qua một lần nhưng không cần ghi nhớ:

* Doctest không thể đoán liệu output mong đợi của bạn đến từ traceback của exception hay từ việc in thông thường. Vì vậy, chẳng hạn, một ví dụ mong đợi ``ValueError: 42 is prime`` sẽ đạt bất kể :exc:`ValueError` thực sự được raise hay ví dụ chỉ đơn thuần in ra phần văn bản traceback đó. Trên thực tế, output thông thường hiếm khi bắt đầu bằng một dòng tiêu đề traceback, nên điều này không gây ra vấn đề thực sự.

* Mỗi dòng của stack traceback (nếu có) phải được thụt lề sâu hơn dòng đầu tiên của ví dụ, *hoặc* bắt đầu bằng một ký tự không phải chữ và số. Dòng đầu tiên sau tiêu đề traceback được thụt lề ở cùng mức và bắt đầu bằng một chữ hoặc số được coi là phần bắt đầu của chi tiết exception. Tất nhiên, điều này hoạt động đúng với các traceback thực sự.

* Khi tùy chọn doctest :const:`IGNORE_EXCEPTION_DETAIL` được chỉ định, mọi thứ sau dấu hai chấm ngoài cùng bên trái và mọi thông tin module trong tên exception đều bị bỏ qua.

* Interactive shell bỏ qua dòng tiêu đề traceback đối với một số
  :exc:`SyntaxError`\ s.  Nhưng doctest sử dụng dòng tiêu đề traceback để phân biệt ngoại lệ với trường hợp không phải ngoại lệ.  Vì vậy, trong trường hợp hiếm khi bạn cần kiểm thử một :exc:`!SyntaxError` không có dòng tiêu đề traceback, bạn sẽ cần tự thêm dòng tiêu đề traceback vào ví dụ kiểm thử.

.. index:: single: ^ (caret); marker

* Đối với một số ngoại lệ, Python hiển thị vị trí xảy ra lỗi bằng các dấu ``^`` và dấu ngã::

     >>> 1 + None
       File "<stdin>", line 1
         1 + None
         ~~^~~~~~
     TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'

  Vì các dòng hiển thị vị trí xảy ra lỗi xuất hiện trước loại và thông tin chi tiết của ngoại lệ, doctest không kiểm tra chúng.  Ví dụ, bài kiểm thử sau vẫn sẽ thành công, mặc dù đặt dấu ``^`` sai vị trí::

     >>> 1 + None
       File "<stdin>", line 1
         1 + None
         ^~~~~~~~
     TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'


.. _option-flags-and-directives:
.. _doctest-options:

Cờ tùy chọn
^^^^^^^^^^^

Một số cờ tùy chọn kiểm soát các khía cạnh khác nhau trong cách doctest hoạt động. Tên biểu tượng của các cờ được cung cấp dưới dạng hằng số của module, có thể được
:ref:`kết hợp bằng phép OR theo bit <bitwise>` với nhau rồi truyền cho nhiều hàm khác nhau. Các tên này cũng có thể được sử dụng trong :ref:`chỉ thị doctest <doctest-directives>`, và có thể được truyền cho giao diện dòng lệnh doctest thông qua tùy chọn ``-o``.

Nhóm tùy chọn đầu tiên xác định ngữ nghĩa của bài kiểm thử, kiểm soát các khía cạnh về cách doctest quyết định liệu đầu ra thực tế có khớp với đầu ra mong đợi của một ví dụ hay không:


.. data:: DONT_ACCEPT_TRUE_FOR_1

   Theo mặc định, nếu một khối đầu ra mong đợi chỉ chứa ``1``, thì một khối đầu ra thực tế chỉ chứa ``1`` hoặc chỉ chứa ``True`` được xem là khớp, và tương tự đối với ``0`` so với ``False``. Khi :const:`DONT_ACCEPT_TRUE_FOR_1` được chỉ định, không phép thay thế nào được cho phép. Hành vi mặc định này đáp ứng việc Python đã thay đổi kiểu trả về của nhiều hàm từ số nguyên sang boolean; các doctest mong đợi đầu ra là "số nguyên nhỏ" vẫn hoạt động trong những trường hợp này. Tùy chọn này có lẽ sẽ bị loại bỏ, nhưng không phải trong vài năm tới.


.. index:: single: <BLANKLINE>
.. data:: DONT_ACCEPT_BLANKLINE

   Theo mặc định, nếu một khối đầu ra mong đợi chứa một dòng chỉ có chuỗi ``<BLANKLINE>``, thì dòng đó sẽ khớp với một dòng trống trong đầu ra thực tế. Vì một dòng thực sự trống dùng để phân cách đầu ra mong đợi, đây là cách duy nhất để biểu thị rằng cần có một dòng trống. Khi
   :const:`DONT_ACCEPT_BLANKLINE` được chỉ định, phép thay thế này không được cho phép.


.. data:: NORMALIZE_WHITESPACE

   Khi được chỉ định, mọi chuỗi khoảng trắng (dấu cách và ký tự xuống dòng) được xem là tương đương. Bất kỳ chuỗi khoảng trắng nào trong đầu ra mong đợi sẽ khớp với bất kỳ chuỗi khoảng trắng nào trong đầu ra thực tế. Theo mặc định, khoảng trắng phải khớp chính xác. :const:`NORMALIZE_WHITESPACE` đặc biệt hữu ích khi một dòng đầu ra mong đợi rất dài và bạn muốn ngắt dòng đó thành nhiều dòng trong mã nguồn.


.. index:: single: ...; in doctests
.. data:: ELLIPSIS

   Khi được chỉ định, một dấu đánh dấu ellipsis (``...``) trong đầu ra mong đợi có thể khớp với bất kỳ chuỗi con nào trong đầu ra thực tế. Điều này bao gồm cả các chuỗi con trải qua ranh giới dòng và các chuỗi con rỗng, vì vậy tốt nhất là nên sử dụng đơn giản. Những cách sử dụng phức tạp có thể dẫn đến cùng kiểu bất ngờ "ôi không, nó khớp quá nhiều!" mà ``.*`` thường gây ra trong regular expression.


.. data:: IGNORE_EXCEPTION_DETAIL

   Khi được chỉ định, các doctest mong đợi ngoại lệ sẽ đạt nếu một ngoại lệ thuộc kiểu mong đợi được phát sinh, ngay cả khi các chi tiết (thông báo và tên ngoại lệ đầy đủ) không khớp.

   Ví dụ, một ví dụ mong đợi ``ValueError: 42`` sẽ đạt nếu ngoại lệ thực tế được phát sinh là ``ValueError: 3*14``, nhưng sẽ thất bại nếu, chẳng hạn, một
   :exc:`TypeError` sẽ được phát sinh thay thế. Nó cũng sẽ bỏ qua mọi tên đầy đủ được ghi trước lớp ngoại lệ, vì tên này có thể khác nhau giữa các bản triển khai và phiên bản Python, cũng như giữa các mã nguồn/thư viện đang được sử dụng. Do đó, cả ba biến thể này đều sẽ hoạt động với flag được chỉ định:

   .. code-block:: pycon

      >>> raise Exception('message')
      Traceback (most recent call last):
      Exception: message

      >>> raise Exception('message')
      Traceback (most recent call last):
      builtins.Exception: message

      >>> raise Exception('message')
      Traceback (most recent call last):
      __main__.Exception: message

   Lưu ý rằng :const:`ELLIPSIS` cũng có thể được dùng để bỏ qua các chi tiết của thông báo ngoại lệ, nhưng một phép kiểm thử như vậy vẫn có thể thất bại tùy thuộc vào việc tên module có xuất hiện hay khớp chính xác hay không.

   .. versionchanged:: 3.2
      :const:`IGNORE_EXCEPTION_DETAIL` now also ignores any information relating
      đến module chứa ngoại lệ đang được kiểm thử.


.. data:: SKIP

   Khi được chỉ định, không chạy ví dụ này. Điều này hữu ích trong các ngữ cảnh mà các ví dụ doctest vừa là tài liệu vừa là trường hợp kiểm thử, và một ví dụ cần được đưa vào nhằm mục đích tài liệu nhưng không nên được kiểm tra. Ví dụ: đầu ra của ví dụ có thể là ngẫu nhiên; hoặc ví dụ có thể phụ thuộc vào những tài nguyên mà test driver không thể truy cập.

   Flag SKIP cũng có thể được dùng để tạm thời "comment out" các ví dụ.


.. data:: COMPARISON_FLAGS

   Một bitmask kết hợp bằng phép OR tất cả các flag so sánh ở trên.

Nhóm tùy chọn thứ hai kiểm soát cách báo cáo các lỗi kiểm thử:


.. data:: REPORT_UDIFF

   Khi được chỉ định, các lỗi liên quan đến đầu ra mong đợi và đầu ra thực tế nhiều dòng sẽ được hiển thị bằng unified diff.


.. data:: REPORT_CDIFF

   Khi được chỉ định, các lỗi liên quan đến đầu ra mong đợi và đầu ra thực tế nhiều dòng sẽ được hiển thị bằng context diff.


.. data:: REPORT_NDIFF

   Khi được chỉ định, các điểm khác biệt được tính toán bằng ``difflib.Differ``, sử dụng cùng thuật toán với tiện ích phổ biến :file:`ndiff.py`. Đây là phương pháp duy nhất đánh dấu các điểm khác biệt cả trong từng dòng lẫn giữa các dòng. Ví dụ: nếu một dòng đầu ra mong đợi chứa chữ số ``1`` trong khi đầu ra thực tế chứa chữ cái ``l``, một dòng sẽ được chèn vào với dấu mũ đánh dấu vị trí các cột không khớp.


.. data:: REPORT_ONLY_FIRST_FAILURE

   Khi được chỉ định, hiển thị ví dụ đầu tiên bị lỗi trong mỗi doctest, nhưng ẩn đầu ra của tất cả các ví dụ còn lại. Điều này sẽ ngăn doctest báo cáo các ví dụ đúng bị lỗi do các lỗi trước đó; nhưng cũng có thể ẩn các ví dụ không đúng bị lỗi độc lập với lỗi đầu tiên. Khi
   :const:`REPORT_ONLY_FIRST_FAILURE` được chỉ định, các ví dụ còn lại vẫn được chạy và vẫn được tính vào tổng số lỗi được báo cáo; chỉ có đầu ra bị ẩn.


.. data:: FAIL_FAST

   Khi được chỉ định, thoát sau ví dụ đầu tiên bị lỗi và không cố chạy các ví dụ còn lại. Vì vậy, số lỗi được báo cáo nhiều nhất sẽ là
   1.  Cờ này có thể hữu ích trong quá trình debugging, vì các ví dụ sau ví dụ đầu tiên
   lỗi thậm chí sẽ không tạo ra đầu ra gỡ lỗi.


.. data:: REPORTING_FLAGS

   Một bitmask kết hợp tất cả các cờ báo cáo ở trên bằng phép OR.


Ngoài ra còn có cách đăng ký tên cờ tùy chọn mới, mặc dù cách này không hữu ích trừ khi bạn định mở rộng phần nội bộ của :mod:`!doctest` thông qua việc phân lớp:


.. function:: register_optionflag(name)

   Tạo một cờ tùy chọn mới với tên đã cho và trả về giá trị số nguyên của cờ mới đó. Có thể sử dụng :func:`register_optionflag` khi phân lớp
   :class:`OutputChecker` hoặc :class:`DocTestRunner` để tạo các tùy chọn được các lớp con của bạn hỗ trợ. Luôn phải gọi :func:`register_optionflag` bằng thành ngữ sau đây::

      MY_FLAG = register_optionflag('MY_FLAG')


.. index::
   single: # (hash); in doctests
   single: + (plus); in doctests
   single: - (minus); in doctests
.. _doctest-directives:

Directives
^^^^^^^^^^

Có thể sử dụng các directive của doctest để sửa đổi :ref:`option flags <doctest-options>` cho từng ví dụ. Directive của doctest là các chú thích Python đặc biệt nằm sau mã nguồn của một ví dụ:

.. productionlist:: doctest
   directive: "#" "doctest:" `directive_options`
   directive_options: `directive_option` ("," `directive_option`)*
   directive_option: `on_or_off` `directive_option_name`
   on_or_off: "+" | "-"
   directive_option_name: "DONT_ACCEPT_BLANKLINE" | "NORMALIZE_WHITESPACE" | ...

Không được phép có khoảng trắng giữa ``+`` hoặc ``-`` và tên tùy chọn của directive. Tên tùy chọn của directive có thể là bất kỳ tên cờ tùy chọn nào được giải thích ở trên.

Các directive doctest của một ví dụ sẽ thay đổi hành vi của doctest cho riêng ví dụ đó. Sử dụng ``+`` để bật hành vi được đặt tên hoặc ``-`` để tắt hành vi đó.

Ví dụ, kiểm thử này thành công:

.. doctest::
   :no-trim-doctest-flags:

   >>> print(list(range(20)))  # doctest: +NORMALIZE_WHITESPACE
   [0,   1,  2,  3,  4,  5,  6,  7,  8,  9,
   10,  11, 12, 13, 14, 15, 16, 17, 18, 19]

Nếu không có directive này, kiểm thử sẽ thất bại vì cả hai lý do: đầu ra thực tế không có hai khoảng trắng trước các phần tử danh sách một chữ số, và đầu ra thực tế nằm trên một dòng duy nhất. Kiểm thử này cũng thành công và cũng cần một directive để làm được như vậy:

.. doctest::
   :no-trim-doctest-flags:

   >>> print(list(range(20)))  # doctest: +ELLIPSIS
   [0, 1, ..., 18, 19]

Có thể sử dụng nhiều directive trên cùng một dòng vật lý, được phân tách bằng dấu phẩy:

.. doctest::
   :no-trim-doctest-flags:

   >>> print(list(range(20)))  # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
   [0,    1, ...,   18,    19]

Nếu sử dụng nhiều chú thích chỉ thị cho cùng một ví dụ, chúng sẽ được kết hợp:

.. doctest::
   :no-trim-doctest-flags:

   >>> print(list(range(20)))  # doctest: +ELLIPSIS
   ...                         # doctest: +NORMALIZE_WHITESPACE
   [0,    1, ...,   18,    19]

Như ví dụ trước cho thấy, bạn có thể thêm các dòng ``...`` chỉ chứa các chỉ thị vào ví dụ của mình. Điều này hữu ích khi ví dụ quá dài để đặt một chỉ thị trên cùng dòng một cách thoải mái:

.. doctest::
   :no-trim-doctest-flags:

   >>> print(list(range(5)) + list(range(10, 20)) + list(range(30, 40)))
   ... # doctest: +ELLIPSIS
   [0, ..., 4, 10, ..., 19, 30, ..., 39]

Lưu ý rằng vì tất cả các tùy chọn đều bị tắt theo mặc định và các chỉ thị chỉ áp dụng cho ví dụ nơi chúng xuất hiện, việc bật tùy chọn (thông qua ``+`` trong một chỉ thị) thường là lựa chọn duy nhất có ý nghĩa. Tuy nhiên, các cờ tùy chọn cũng có thể được truyền vào những hàm chạy doctest, qua đó thiết lập các giá trị mặc định khác nhau. Trong những trường hợp như vậy, việc tắt một tùy chọn thông qua ``-`` trong một chỉ thị có thể hữu ích.


.. _doctest-warnings:

Cảnh báo
^^^^^^^^

:mod:`!doctest` rất nghiêm ngặt trong việc yêu cầu kết quả mong đợi phải khớp chính xác. Chỉ cần một ký tự không khớp là bài kiểm tra sẽ thất bại. Điều này có thể sẽ khiến bạn bất ngờ vài lần khi tìm hiểu chính xác Python đảm bảo và không đảm bảo điều gì về kết quả đầu ra. Ví dụ: khi in một set, Python không đảm bảo các phần tử được in theo thứ tự cụ thể nào, nên một bài kiểm tra như sau::

   >>> foo()
   {"spam", "eggs"}

sẽ dễ gặp lỗi! Một cách khắc phục là thực hiện::

   >>> foo() == {"spam", "eggs"}
   True

thay vào đó. Một cách khác là thực hiện::

   >>> d = sorted(foo())
   >>> d
   ['eggs', 'spam']

Còn những cách khác, nhưng bạn đã hiểu ý.

Một ý tưởng tồi khác là in những thứ có chứa địa chỉ của một đối tượng, chẳng hạn như

.. doctest::

   >>> id(1.0)  # chắc chắn đôi khi sẽ thất bại  # doctest: +SKIP
   7948648
   >>> class C: pass
   >>> C()  # repr() mặc định cho các instance chứa một địa chỉ   # doctest: +SKIP
   <C object at 0x00AC18F0>

Chỉ thị :const:`ELLIPSIS` cung cấp một cách tiếp cận hữu ích cho ví dụ cuối cùng:

.. doctest::
   :no-trim-doctest-flags:

   >>> C()  # doctest: +ELLIPSIS
   <C object at 0x...>

Các số dấu phẩy động cũng có thể có những khác biệt nhỏ trong đầu ra giữa các nền tảng, vì Python ủy quyền một số phép tính dấu phẩy động cho thư viện C của nền tảng, mà chất lượng của các thư viện C khác nhau đáng kể trong trường hợp này.::

   >>> 1000**0.1  # rủi ro
   1.9952623149688797
   >>> round(1000**0.1, 9) # an toàn hơn
   1.995262315
   >>> print(f'{1000**0.1:.4f}') # an toàn hơn nhiều
   1.9953

Các số có dạng ``I/2.**J`` an toàn trên mọi nền tảng, và tôi thường cố ý tạo các ví dụ doctest để cho ra những số có dạng đó::

   >>> 3./4  # hoàn toàn an toàn
   0.75

Các phân số đơn giản cũng dễ hiểu hơn đối với mọi người, nhờ đó tài liệu sẽ tốt hơn.


.. _doctest-basic-api:

API cơ bản
----------

Các hàm :func:`testmod` và :func:`testfile` cung cấp một giao diện đơn giản cho doctest, đáp ứng hầu hết các nhu cầu sử dụng cơ bản. Để có phần giới thiệu ít trang trọng hơn về hai hàm này, hãy xem các phần :ref:`doctest-simple-testmod` và :ref:`doctest-simple-testfile`.


.. function:: testfile(filename, module_relative=True, name=None, package=None, globs=None, verbose=None, report=True, optionflags=0, extraglobs=None, raise_on_error=False, parser=DocTestParser(), encoding=None)

   Tất cả đối số ngoại trừ *filename* đều là tùy chọn và nên được chỉ định theo dạng keyword.

   Kiểm thử các ví dụ trong tệp có tên *filename*. Trả về ``(failure_count, test_count)``.

   Đối số tùy chọn *module_relative* chỉ định cách diễn giải tên tệp:

   * Nếu *module_relative* là ``True`` (giá trị mặc định), thì *filename* chỉ định một đường dẫn tương đối với module và không phụ thuộc hệ điều hành. Theo mặc định, đường dẫn này tương đối với thư mục của module gọi; nhưng nếu đối số *package* được chỉ định, thì nó tương đối với package đó. Để đảm bảo tính độc lập với hệ điều hành, *filename* phải sử dụng ký tự ``/`` để phân tách các thành phần đường dẫn và không được là đường dẫn tuyệt đối (tức là không được bắt đầu bằng ``/``).

   * Nếu *module_relative* là ``False``, thì *filename* chỉ định một đường dẫn đặc thù theo hệ điều hành. Đường dẫn này có thể là tuyệt đối hoặc tương đối; các đường dẫn tương đối được phân giải dựa trên thư mục làm việc hiện tại.

   Đối số tùy chọn *name* cung cấp tên của phép kiểm thử; theo mặc định, hoặc nếu ``None``, ``os.path.basename(filename)`` được sử dụng.

   Đối số tùy chọn *package* là một Python package hoặc tên của một Python package có thư mục được dùng làm thư mục cơ sở cho tên tệp tương đối với module. Nếu không chỉ định package, thư mục của module gọi sẽ được dùng làm thư mục cơ sở cho các tên tệp tương đối với module. Sẽ xảy ra lỗi nếu chỉ định *package* khi *module_relative* là ``False``.

   Đối số tùy chọn *globs* cung cấp một dict được dùng làm globals khi thực thi các ví dụ. Một bản sao nông mới của dict này được tạo cho doctest, vì vậy các ví dụ của nó bắt đầu với trạng thái sạch. Theo mặc định, hoặc nếu ``None``, một dict trống mới được sử dụng.

   Đối số tùy chọn *extraglobs* cung cấp một dict được hợp nhất vào globals dùng để thực thi các ví dụ. Cách này hoạt động tương tự như :meth:`dict.update`: nếu *globs* và *extraglobs* có một khóa chung, giá trị tương ứng trong *extraglobs* sẽ xuất hiện trong dict kết hợp. Theo mặc định, hoặc nếu ``None``, không sử dụng globals bổ sung. Đây là một tính năng nâng cao cho phép tham số hóa các doctest. Ví dụ, có thể viết một doctest cho một lớp cơ sở bằng cách sử dụng một tên chung cho lớp đó, sau đó dùng lại để kiểm thử bất kỳ số lượng lớp con nào bằng cách truyền một dict *extraglobs* ánh xạ tên chung đến lớp con cần kiểm thử.

   Đối số tùy chọn *verbose* sẽ in ra rất nhiều thông tin nếu có giá trị true và chỉ in ra các lỗi nếu có giá trị false; theo mặc định, hoặc nếu ``None``, nó là true khi và chỉ khi ``'-v'`` nằm trong :data:`sys.argv`.

   Đối số tùy chọn *report* sẽ in bản tóm tắt ở cuối khi có giá trị true, nếu không thì không in gì ở cuối.  Ở chế độ verbose, bản tóm tắt sẽ chi tiết; nếu không, bản tóm tắt sẽ rất ngắn (thực tế là trống nếu tất cả các bài kiểm tra đều đạt).

   Đối số tùy chọn *optionflags* (giá trị mặc định là ``0``) nhận phép
   :ref:`OR theo bit <bitwise>` của các cờ tùy chọn. Xem phần :ref:`doctest-options`.

   Đối số tùy chọn *raise_on_error* mặc định là false.  Nếu là true, một exception sẽ được raised khi gặp failure đầu tiên hoặc exception không mong đợi trong một ví dụ.  Điều này cho phép debug các failure sau khi chúng xảy ra. Hành vi mặc định là tiếp tục chạy các ví dụ.

   Đối số tùy chọn *parser* chỉ định một :class:`DocTestParser` (hoặc lớp con) sẽ được dùng để trích xuất các bài kiểm tra từ các tệp.  Theo mặc định, đây là một parser thông thường (tức là ``DocTestParser()``).

   Đối số tùy chọn *encoding* chỉ định encoding được dùng để chuyển đổi tệp sang Unicode.


.. function:: testmod(m=None, name=None, globs=None, verbose=None, report=True, optionflags=0, extraglobs=None, raise_on_error=False, exclude_empty=False)

   Tất cả đối số đều là tùy chọn, và tất cả ngoại trừ *m* phải được chỉ định dưới dạng keyword.

   Kiểm thử các ví dụ trong docstring của các function và class có thể truy cập từ module *m* (hoặc module :mod:`__main__` nếu *m* không được cung cấp hoặc là ``None``), bắt đầu từ ``m.__doc__``.

   Ngoài ra, hãy kiểm thử các ví dụ có thể truy cập từ dict ``m.__test__``, nếu dict này tồn tại. ``m.__test__`` ánh xạ các tên (chuỗi) tới các function, class và chuỗi; docstring của function và class được tìm kiếm để tìm các ví dụ; các chuỗi được tìm kiếm trực tiếp, như thể chúng là docstring.

   Chỉ các docstring gắn với những đối tượng thuộc module *m* mới được tìm kiếm.

   Trả về ``(failure_count, test_count)``.

   Đối số tùy chọn *name* cung cấp tên của module; theo mặc định, hoặc nếu ``None``, thì ``m.__name__`` được sử dụng.

   Đối số tùy chọn *exclude_empty* mặc định là false. Nếu là true, các đối tượng không tìm thấy doctest nào sẽ bị loại khỏi việc xem xét. Giá trị mặc định là một thủ thuật tương thích ngược, để mã vẫn đang sử dụng
   :meth:`doctest.master.summarize <DocTestRunner.summarize>` kết hợp với :func:`testmod` vẫn tiếp tục tạo đầu ra cho các đối tượng không có kiểm thử. Đối số *exclude_empty* của hàm khởi tạo :class:`DocTestFinder` mới hơn mặc định là true.

   Các đối số tùy chọn *extraglobs*, *verbose*, *report*, *optionflags*, *raise_on_error* và *globs* giống như đối với hàm :func:`testfile` ở trên, ngoại trừ việc *globs* mặc định là ``m.__dict__``.


.. function:: run_docstring_examples(f, globs, verbose=False, name="NoName", compileflags=None, optionflags=0)

   Kiểm thử các ví dụ được liên kết với đối tượng *f*; chẳng hạn, *f* có thể là một chuỗi, mô-đun, hàm hoặc đối tượng lớp.

   Một bản sao nông của đối số từ điển *globs* được sử dụng cho ngữ cảnh thực thi.

   Đối số tùy chọn *name* được sử dụng trong các thông báo lỗi và mặc định là ``"NoName"``.

   Nếu đối số tùy chọn *verbose* là true, đầu ra sẽ được tạo ngay cả khi không có lỗi nào. Theo mặc định, đầu ra chỉ được tạo khi một ví dụ bị lỗi.

   Đối số tùy chọn *compileflags* cung cấp tập cờ sẽ được trình biên dịch Python sử dụng khi chạy các ví dụ. Theo mặc định hoặc nếu ``None``, các cờ sẽ được suy ra tương ứng với tập tính năng future được tìm thấy trong *globs*.

   Đối số tùy chọn *optionflags* hoạt động giống như đối với hàm :func:`testfile` ở trên.


.. _doctest-unittest-api:

Unittest API
------------

Khi tập hợp các mô-đun có doctest của bạn ngày càng lớn, bạn sẽ cần một cách để chạy tất cả doctest của chúng một cách có hệ thống. :mod:`!doctest` cung cấp hai hàm có thể được dùng để tạo các bộ kiểm thử :mod:`unittest` từ các mô-đun và tệp văn bản chứa doctest. Để tích hợp với tính năng phát hiện kiểm thử của :mod:`unittest`, hãy thêm một hàm :ref:`load_tests <load_tests-protocol>` vào mô-đun kiểm thử của bạn::

   import unittest
   import doctest
   import my_module_with_doctests

   def load_tests(loader, tests, ignore):
       tests.addTests(doctest.DocTestSuite(my_module_with_doctests))
       return tests

Có hai hàm chính để tạo các thực thể :class:`unittest.TestSuite` từ các tệp văn bản và mô-đun có doctest:


.. function:: DocFileSuite(*paths, module_relative=True, package=None, setUp=None, tearDown=None, globs=None, optionflags=0, parser=DocTestParser(), encoding=None)

   Chuyển đổi các kiểm thử doctest từ một hoặc nhiều tệp văn bản thành một
   :class:`unittest.TestSuite`.

   :class:`unittest.TestSuite` được trả về sẽ được chạy bởi framework unittest và chạy các ví dụ tương tác trong từng tệp. Nếu một ví dụ trong bất kỳ tệp nào không thành công, kiểm thử đơn vị được tổng hợp sẽ thất bại và một ngoại lệ :exc:`~unittest.TestCase.failureException` được đưa ra, cho biết tên của tệp chứa kiểm thử và số dòng (đôi khi chỉ gần đúng). Nếu tất cả ví dụ trong một tệp đều bị bỏ qua, kiểm thử đơn vị được tổng hợp cũng được đánh dấu là bị bỏ qua.

   Truyền một hoặc nhiều đường dẫn (dưới dạng chuỗi) đến các tệp văn bản cần kiểm tra.

   Các tùy chọn có thể được cung cấp dưới dạng đối số từ khóa:

   Đối số tùy chọn *module_relative* chỉ định cách diễn giải các tên tệp trong *paths*:

   * Nếu *module_relative* là ``True`` (mặc định), thì mỗi tên tệp trong *paths* chỉ định một đường dẫn độc lập với hệ điều hành, tương đối với module. Theo mặc định, đường dẫn này tương đối với thư mục của module gọi; nhưng nếu đối số *package* được chỉ định, thì nó tương đối với package đó. Để đảm bảo tính độc lập với hệ điều hành, mỗi tên tệp phải sử dụng ký tự ``/`` để phân tách các phần của đường dẫn và không được là đường dẫn tuyệt đối (tức là không được bắt đầu bằng ``/``).

   * Nếu *module_relative* là ``False``, thì mỗi tên tệp trong *paths* chỉ định một đường dẫn dành riêng cho hệ điều hành. Đường dẫn này có thể là đường dẫn tuyệt đối hoặc tương đối; các đường dẫn tương đối được phân giải dựa trên thư mục làm việc hiện tại.

   Đối số tùy chọn *package* là một Python package hoặc tên của một Python package, có thư mục được dùng làm thư mục cơ sở cho các tên tệp tương đối với module trong *paths*. Nếu không chỉ định package, thư mục của module gọi sẽ được dùng làm thư mục cơ sở cho các tên tệp tương đối với module. Sẽ xảy ra lỗi nếu chỉ định *package* khi *module_relative* là ``False``.

   Đối số tùy chọn *setUp* chỉ định một hàm thiết lập cho test suite. Hàm này được gọi trước khi chạy các bài kiểm thử trong từng tệp. Hàm *setUp* sẽ được truyền một đối tượng :class:`DocTest`. Hàm *setUp* có thể truy cập các biến toàn cục của bài kiểm thử thông qua thuộc tính :attr:`~DocTest.globs` của bài kiểm thử được truyền vào.

   Đối số tùy chọn *tearDown* chỉ định một hàm dọn dẹp cho test suite. Hàm này được gọi sau khi chạy các bài kiểm thử trong từng tệp. Hàm *tearDown* sẽ được truyền một đối tượng :class:`DocTest`. Hàm *tearDown* có thể truy cập các biến toàn cục của bài kiểm thử thông qua thuộc tính :attr:`~DocTest.globs` của bài kiểm thử được truyền vào.

   Đối số tùy chọn *globs* là một từ điển chứa các biến toàn cục ban đầu cho các kiểm thử. Một bản sao mới của từ điển này được tạo cho mỗi kiểm thử. Theo mặc định, *globs* là một từ điển mới, rỗng.

   Đối số tùy chọn *optionflags* chỉ định các tùy chọn doctest mặc định cho các kiểm thử, được tạo bằng cách thực hiện phép OR trên từng cờ tùy chọn. Xem phần
   :ref:`doctest-options`. Xem hàm :func:`set_unittest_reportflags` bên dưới để biết cách tốt hơn nhằm thiết lập các tùy chọn báo cáo.

   Đối số tùy chọn *parser* chỉ định một :class:`DocTestParser` (hoặc lớp con) được dùng để trích xuất các kiểm thử từ các tệp. Theo mặc định, đây là một parser thông thường (tức là ``DocTestParser()``).

   Đối số tùy chọn *encoding* chỉ định encoding được dùng để chuyển đổi tệp sang unicode.

   Biến toàn cục ``__file__`` được thêm vào các biến toàn cục được cung cấp cho các doctest được tải từ một tệp văn bản bằng :func:`DocFileSuite`.


.. function:: DocTestSuite(module=None, globs=None, extraglobs=None, test_finder=None, setUp=None, tearDown=None, optionflags=0, checker=None)

   Chuyển đổi các kiểm thử doctest của một module thành một :class:`unittest.TestSuite`.

   :class:`unittest.TestSuite` được trả về sẽ được framework unittest chạy và chạy từng doctest trong module. Mỗi docstring được chạy như một unit test riêng biệt. Nếu bất kỳ doctest nào không thành công, unit test được tổng hợp cũng không thành công và một ngoại lệ :exc:`unittest.TestCase.failureException` được đưa ra, hiển thị tên tệp chứa test cùng với số dòng (đôi khi chỉ là số dòng gần đúng). Nếu tất cả các ví dụ trong một docstring đều bị bỏ qua, thì

   Đối số tùy chọn *module* cung cấp module cần được kiểm thử. Đối số này có thể là một đối tượng module hoặc tên module (có thể chứa dấu chấm). Nếu không được chỉ định, module gọi hàm này sẽ được sử dụng.

   Đối số tùy chọn *globs* là một từ điển chứa các biến global ban đầu cho các test. Một bản sao mới của từ điển này được tạo cho mỗi test. Theo mặc định, *globs* là :attr:`~module.__dict__` của module.

   Đối số tùy chọn *extraglobs* chỉ định một tập hợp bổ sung các biến global, được hợp nhất vào *globs*. Theo mặc định, không sử dụng biến global bổ sung nào.

   Đối số tùy chọn *test_finder* là đối tượng :class:`DocTestFinder` (hoặc một đối tượng thay thế tương thích) được dùng để trích xuất doctest từ module.

   Các đối số tùy chọn *setUp*, *tearDown* và *optionflags* giống như đối với hàm :func:`DocFileSuite` ở trên, nhưng chúng được gọi cho mỗi docstring.

   Hàm này sử dụng cùng kỹ thuật tìm kiếm như :func:`testmod`.

   .. versionchanged:: 3.5
      :func:`DocTestSuite` returns an empty :class:`unittest.TestSuite` if *module*
      không chứa docstring thay vì phát sinh :exc:`ValueError`.

Bên dưới lớp trừu tượng, :func:`DocTestSuite` tạo một :class:`unittest.TestSuite` từ các thực thể :class:`!doctest.DocTestCase`, và :class:`!DocTestCase` là một lớp con của :class:`unittest.TestCase`. :class:`!DocTestCase` không được tài liệu hóa ở đây (đây là chi tiết nội bộ), nhưng việc nghiên cứu mã nguồn của nó có thể giúp trả lời các câu hỏi về những chi tiết chính xác của việc tích hợp :mod:`unittest`.

Tương tự, :func:`DocFileSuite` tạo một :class:`unittest.TestSuite` từ
các thực thể :class:`!doctest.DocFileCase`, và :class:`!DocFileCase` là một lớp con của :class:`!DocTestCase`.

Vì vậy, cả hai cách tạo một :class:`unittest.TestSuite` đều chạy các thực thể của
:class:`!DocTestCase`. Điều này quan trọng vì một lý do khá tinh tế: khi bạn tự chạy
các hàm :mod:`!doctest`, bạn có thể trực tiếp kiểm soát các tùy chọn :mod:`!doctest` được sử dụng bằng cách truyền các cờ tùy chọn cho các hàm :mod:`!doctest`. Tuy nhiên, nếu bạn đang viết một framework :mod:`unittest`, thì :mod:`!unittest` cuối cùng sẽ kiểm soát thời điểm và cách các bài kiểm thử được chạy. Tác giả framework thường muốn kiểm soát
các tùy chọn báo cáo của :mod:`!doctest` (chẳng hạn như được chỉ định bằng các tùy chọn dòng lệnh), nhưng không có cách nào truyền các tùy chọn qua :mod:`!unittest` đến
các trình chạy kiểm thử :mod:`!doctest`.

Vì lý do này, :mod:`!doctest` cũng hỗ trợ khái niệm về các cờ báo cáo :mod:`!doctest` dành riêng cho việc hỗ trợ :mod:`unittest`, thông qua hàm sau:


.. function:: set_unittest_reportflags(flags)

   Đặt các cờ báo cáo :mod:`!doctest` cần sử dụng.

   Đối số *flags* nhận :ref:`phép OR theo bit <bitwise>` của các cờ tùy chọn. Xem phần :ref:`doctest-options`. Chỉ có thể sử dụng "các cờ báo cáo".

   Đây là một thiết lập ở cấp module và ảnh hưởng đến tất cả các doctest trong tương lai được chạy bởi module
   :mod:`unittest`: phương thức :meth:`!runTest` của :class:`!DocTestCase` xem xét các cờ tùy chọn được chỉ định cho test case khi instance :class:`!DocTestCase` được khởi tạo. Nếu không có cờ báo cáo nào được chỉ định (đây là trường hợp thường gặp và được mong đợi), các cờ báo cáo của :mod:`!doctest`'s :mod:`!unittest` là
   :ref:`được OR theo bit <bitwise>` vào các cờ tùy chọn, và các cờ tùy chọn sau khi được bổ sung như vậy sẽ được truyền cho instance :class:`DocTestRunner` được tạo để chạy doctest. Nếu có cờ báo cáo nào được chỉ định khi
   instance :class:`!DocTestCase` được khởi tạo, các cờ báo cáo của :mod:`!doctest`
   :mod:`!unittest` Các cờ reporting bị bỏ qua.

   Hàm trả về giá trị của các cờ báo cáo :mod:`unittest` đang có hiệu lực trước khi hàm được gọi.


.. _doctest-advanced-api:

API nâng cao
------------

API cơ bản là một wrapper đơn giản, được thiết kế để giúp sử dụng doctest dễ dàng. API này khá linh hoạt và đáp ứng nhu cầu của hầu hết người dùng; tuy nhiên, nếu bạn cần kiểm soát việc kiểm thử chi tiết hơn hoặc muốn mở rộng khả năng của doctest, bạn nên sử dụng API nâng cao.

API nâng cao xoay quanh hai lớp container, được dùng để lưu trữ các ví dụ tương tác được trích xuất từ các trường hợp doctest:

* :class:`Example`: Một :term:`statement` Python duy nhất, đi kèm với kết quả dự kiến.

* :class:`DocTest`: Một tập hợp các :class:`Example`\ s, thường được trích xuất từ một docstring hoặc tệp văn bản duy nhất.

Các lớp xử lý bổ sung được định nghĩa để tìm, phân tích cú pháp, thực thi và kiểm tra các ví dụ doctest:

* :class:`DocTestFinder`: Tìm tất cả docstring trong một module cho trước và sử dụng một
  :class:`DocTestParser` để tạo một :class:`DocTest` từ mỗi docstring chứa các ví dụ tương tác.

* :class:`DocTestParser`: Tạo một đối tượng :class:`DocTest` từ một chuỗi (chẳng hạn như docstring của một đối tượng).

* :class:`DocTestRunner`: Thực thi các ví dụ trong một :class:`DocTest` và sử dụng một :class:`OutputChecker` để xác minh kết quả của chúng.

* :class:`OutputChecker`: So sánh đầu ra thực tế từ một ví dụ doctest với đầu ra mong đợi và quyết định xem chúng có khớp nhau hay không.

Mối quan hệ giữa các lớp xử lý này được tóm tắt trong sơ đồ sau::

                               list of:
   +------+                   +---------+
   |module| --DocTestFinder-> | DocTest | --DocTestRunner-> results
   +------+    |        ^     +---------+     |       ^    (printed)
               |        |     | Example |     |       |
               v        |     |   ...   |     v       |
              DocTestParser   | Example |   OutputChecker
                              +---------+


.. _doctest-doctest:

DocTest Objects
^^^^^^^^^^^^^^^


.. class:: DocTest(examples, globs, name, filename, lineno, docstring)

   Một tập hợp các ví dụ doctest cần được chạy trong cùng một namespace. Các đối số của hàm khởi tạo được dùng để khởi tạo các thuộc tính có cùng tên.


   :class:`DocTest` định nghĩa các thuộc tính sau. Chúng được khởi tạo bởi hàm khởi tạo và không nên được sửa đổi trực tiếp.


   .. attribute:: examples

      Một danh sách các đối tượng :class:`Example` mã hóa những ví dụ Python tương tác riêng lẻ cần được chạy bởi bài kiểm thử này.


   .. attribute:: globs

      Namespace (hay còn gọi là globals) nơi các ví dụ sẽ được chạy. Đây là một dictionary ánh xạ tên với giá trị. Mọi thay đổi đối với namespace do các ví dụ thực hiện (chẳng hạn như liên kết các biến mới) sẽ được phản ánh trong :attr:`globs` sau khi bài kiểm thử chạy xong.


   .. attribute:: name

      Tên chuỗi xác định :class:`DocTest`. Thông thường, đây là tên của đối tượng hoặc tệp mà từ đó bài kiểm thử được trích xuất.


   .. attribute:: filename

      Tên của tệp mà từ đó :class:`DocTest` được trích xuất; hoặc ``None`` nếu không xác định được tên tệp, hoặc nếu :class:`!DocTest` không được trích xuất từ một tệp.


   .. attribute:: lineno

      Số dòng trong :attr:`filename` nơi :class:`DocTest` này bắt đầu, hoặc ``None`` nếu không xác định được số dòng. Số dòng này được đánh số bắt đầu từ 0 tính từ đầu tệp.


   .. attribute:: docstring

      Chuỗi mà từ đó bài kiểm thử được trích xuất, hoặc ``None`` nếu không có chuỗi, hoặc nếu bài kiểm thử không được trích xuất từ một chuỗi.


.. _doctest-example:

Các đối tượng ví dụ
^^^^^^^^^^^^^^^^^^^


.. class:: Example(source, want, exc_msg=None, lineno=0, indent=0, options=None)

   Một ví dụ tương tác đơn, gồm một câu lệnh Python và đầu ra dự kiến của câu lệnh đó. Các đối số của hàm khởi tạo được dùng để khởi tạo các thuộc tính có cùng tên.


   :class:`Example` định nghĩa các thuộc tính sau. Các thuộc tính này được khởi tạo bởi hàm khởi tạo và không nên được sửa đổi trực tiếp.


   .. attribute:: source

      Một chuỗi chứa mã nguồn của ví dụ. Mã nguồn này gồm một câu lệnh Python duy nhất và luôn kết thúc bằng ký tự xuống dòng; constructor sẽ thêm ký tự xuống dòng khi cần.


   .. attribute:: want

      Đầu ra dự kiến khi chạy mã nguồn của ví dụ (từ stdout hoặc một traceback trong trường hợp có exception). :attr:`want` kết thúc bằng ký tự xuống dòng, trừ khi không dự kiến có đầu ra; khi đó, nó là một chuỗi rỗng. Constructor sẽ thêm ký tự xuống dòng khi cần.


   .. attribute:: exc_msg

      Thông báo exception do ví dụ tạo ra, nếu ví dụ được dự kiến sẽ tạo ra một exception; hoặc ``None`` nếu không dự kiến tạo ra một exception. Thông báo exception này được so sánh với giá trị trả về của
      :func:`traceback.format_exception_only`. :attr:`exc_msg` kết thúc bằng ký tự xuống dòng, trừ khi nó là ``None``. Constructor sẽ thêm ký tự xuống dòng nếu cần.


   .. attribute:: lineno

      Số dòng trong chuỗi chứa ví dụ, tại đó ví dụ bắt đầu. Số dòng này được đánh số từ 0 so với phần đầu của chuỗi chứa nó.


   .. attribute:: indent

      Mức thụt lề của ví dụ trong chuỗi chứa nó, tức là số ký tự dấu cách đứng trước prompt đầu tiên của ví dụ.


   .. attribute:: options

      Một dictionary ánh xạ các cờ tùy chọn tới ``True`` hoặc ``False``, được dùng để ghi đè các tùy chọn mặc định cho ví dụ này. Mọi cờ tùy chọn không có trong dictionary này sẽ giữ giá trị mặc định (như được chỉ định bởi
      của :class:`DocTestRunner` :ref:`optionflags <doctest-options>`). Theo mặc định, không có tùy chọn nào được thiết lập.


.. _doctest-doctestfinder:

Các đối tượng DocTestFinder
^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. class:: DocTestFinder(verbose=False, parser=DocTestParser(), recurse=True, exclude_empty=True)

   Một lớp xử lý được dùng để trích xuất các :class:`DocTest`\ s có liên quan đến một đối tượng nhất định, từ docstring của đối tượng đó và docstring của các đối tượng chứa trong đó.
   Có thể trích xuất :class:`DocTest`\ s từ các module, class, function, method, staticmethod, classmethod và property.

   Có thể sử dụng đối số tùy chọn *verbose* để hiển thị các đối tượng được finder tìm kiếm. Theo mặc định, đối số này là ``False`` (không xuất gì).

   Đối số tùy chọn *parser* chỉ định đối tượng :class:`DocTestParser` (hoặc một đối tượng thay thế tương thích) được dùng để trích xuất doctest từ các docstring.

   Nếu đối số tùy chọn *recurse* là false, thì :meth:`DocTestFinder.find` sẽ chỉ kiểm tra đối tượng được cung cấp, không kiểm tra bất kỳ đối tượng nào chứa trong đó.

   Nếu đối số tùy chọn *exclude_empty* là false thì
   :meth:`DocTestFinder.find` sẽ bao gồm các bài kiểm thử cho những đối tượng có docstring rỗng.


   :class:`DocTestFinder` định nghĩa phương thức sau:


   .. method:: find(obj[, name][, module][, globs][, extraglobs])

      Trả về danh sách các :class:`DocTest`\ s được định nghĩa bởi docstring của *obj*, hoặc bởi docstring của bất kỳ đối tượng nào chứa trong đó.

      Đối số tùy chọn *name* chỉ định tên của đối tượng; tên này sẽ được dùng để tạo tên cho các :class:`DocTest`\ s được trả về. Nếu *name* không được chỉ định thì ``obj.__name__`` sẽ được sử dụng.

      Tham số tùy chọn *module* là module chứa đối tượng đã cho. Nếu module không được chỉ định hoặc là ``None``, trình tìm kiếm kiểm thử sẽ cố gắng tự động xác định module chính xác. Module của đối tượng được sử dụng:

      * Làm namespace mặc định nếu *globs* không được chỉ định.

      * Để ngăn DocTestFinder trích xuất các DocTest từ những đối tượng được nhập từ các module khác. (Các đối tượng chứa có module khác với *module* sẽ bị bỏ qua.)

      * Để tìm tên tệp chứa đối tượng.

      * Để hỗ trợ tìm số dòng của đối tượng trong tệp.

      Nếu *module* là ``False``, sẽ không cố gắng tìm module. Điều này khá khó hiểu và chủ yếu hữu ích khi kiểm thử chính doctest: nếu *module* là ``False``, hoặc là ``None`` nhưng không thể tự động tìm thấy, thì tất cả đối tượng được xem là thuộc về module (không tồn tại) đó, vì vậy tất cả đối tượng chứa sẽ được tìm kiếm doctest (theo đệ quy).

      Các biến toàn cục cho mỗi :class:`DocTest` được tạo bằng cách kết hợp *globs* và *extraglobs* (các liên kết trong *extraglobs* sẽ ghi đè các liên kết trong *globs*). Một bản sao nông mới của từ điển biến toàn cục được tạo cho mỗi :class:`!DocTest`. Nếu *globs* không được chỉ định, giá trị mặc định là biến toàn cục của module
      :attr:`~module.__dict__`, nếu được chỉ định, hoặc ``{}`` nếu không. Nếu *extraglobs* không được chỉ định, giá trị mặc định là ``{}``.


.. _doctest-doctestparser:

Các đối tượng DocTestParser
^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. class:: DocTestParser()

   Một processing class được sử dụng để trích xuất các ví dụ tương tác từ một chuỗi và dùng chúng để tạo một đối tượng :class:`DocTest`.


   :class:`DocTestParser` định nghĩa các phương thức sau:


   .. method:: get_doctest(string, globs, name, filename, lineno)

      Trích xuất tất cả các ví dụ doctest từ chuỗi đã cho và tập hợp chúng thành một
      đối tượng :class:`DocTest`.

      *globs*, *name*, *filename* và *lineno* là các thuộc tính của đối tượng mới
      :class:`!DocTest`. Xem tài liệu về :class:`DocTest` để biết thêm thông tin.


   .. method:: get_examples(string, name='<string>')

      Trích xuất tất cả các ví dụ doctest từ chuỗi đã cho và trả về chúng dưới dạng một danh sách các đối tượng :class:`Example`. Số dòng được đánh chỉ mục từ 0. Đối số tùy chọn *name* là tên xác định chuỗi này và chỉ được sử dụng trong các thông báo lỗi.


   .. method:: parse(string, name='<string>')

      Chia chuỗi đã cho thành các ví dụ và phần văn bản xen giữa, rồi trả về chúng dưới dạng danh sách xen kẽ các :class:`Example`\ s và các chuỗi. Số dòng của
      :class:`!Example`\ s được đánh số từ 0. Đối số tùy chọn *name* là tên xác định chuỗi này và chỉ được sử dụng trong các thông báo lỗi.


Các đối tượng TestResults
^^^^^^^^^^^^^^^^^^^^^^^^^


.. class:: TestResults(failed, attempted)

   .. attribute:: failed

      Số lượng bài kiểm thử không thành công.

   .. attribute:: attempted

      Số lượng bài kiểm thử đã thực hiện.

   .. attribute:: skipped

      Số lượng bài kiểm thử bị bỏ qua.

      .. versionadded:: 3.13


.. _doctest-doctestrunner:

Các đối tượng DocTestRunner
^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. class:: DocTestRunner(checker=None, verbose=None, optionflags=0)

   Một lớp xử lý được dùng để thực thi và xác minh các ví dụ tương tác trong một
   :class:`DocTest`.

   Việc so sánh giữa output dự kiến và output thực tế được thực hiện bằng một
   :class:`OutputChecker`.  Có thể tùy chỉnh phép so sánh này bằng một số option flag; xem phần :ref:`doctest-options` để biết thêm thông tin.  Nếu các option flag không đủ, bạn cũng có thể tùy chỉnh phép so sánh bằng cách truyền một lớp con của :class:`!OutputChecker` vào constructor.

   Output hiển thị của test runner có thể được kiểm soát theo hai cách. Trước tiên, có thể truyền một hàm output vào :meth:`run`; hàm này sẽ được gọi với các chuỗi cần hiển thị.  Giá trị mặc định là ``sys.stdout.write``.  Nếu việc capture output không đủ, bạn cũng có thể tùy chỉnh output hiển thị bằng cách tạo lớp con của DocTestRunner và ghi đè các phương thức
   :meth:`report_start`, :meth:`report_success`,
   :meth:`report_unexpected_exception` và :meth:`report_failure`.

   Keyword argument tùy chọn *checker* chỉ định đối tượng :class:`OutputChecker` (hoặc đối tượng thay thế tương thích) sẽ được dùng để so sánh output dự kiến với output thực tế của các ví dụ doctest.

   Keyword argument tùy chọn *verbose* kiểm soát mức độ chi tiết của :class:`DocTestRunner`.  Nếu *verbose* là ``True``, thông tin về từng ví dụ sẽ được in ra khi ví dụ đó chạy.  Nếu *verbose* là ``False``, chỉ các trường hợp thất bại được in ra.  Nếu *verbose* không được chỉ định hoặc là ``None``, output chi tiết sẽ được sử dụng khi và chỉ khi switch dòng lệnh ``-v`` được dùng.

   Đối số từ khóa tùy chọn *optionflags* có thể được sử dụng để kiểm soát cách test runner so sánh đầu ra mong đợi với đầu ra thực tế và cách hiển thị các lỗi. Để biết thêm thông tin, hãy xem phần :ref:`doctest-options`.

   Test runner tích lũy các thống kê. Tổng số các ví dụ đã thử, thất bại và bị bỏ qua cũng có thể được truy cập thông qua :attr:`tries`,
   các thuộc tính :attr:`failures` và :attr:`skips`. Các phương thức :meth:`run` và
   :meth:`summarize` trả về một thực thể :class:`TestResults`.

   :class:`DocTestRunner` định nghĩa các phương thức sau:


   .. method:: report_start(out, test, example)

      Báo cáo rằng test runner sắp xử lý ví dụ đã cho. Phương thức này được cung cấp để cho phép các lớp con của :class:`DocTestRunner` tùy chỉnh đầu ra; không nên gọi phương thức này trực tiếp.

      *example* là ví dụ sắp được xử lý. *test* là test chứa *example*. *out* là hàm đầu ra được truyền cho
      :meth:`DocTestRunner.run`.


   .. method:: report_success(out, test, example, got)

      Báo cáo rằng ví dụ đã cho chạy thành công. Phương thức này được cung cấp để cho phép các lớp con của :class:`DocTestRunner` tùy chỉnh đầu ra; không nên gọi trực tiếp phương thức này.

      *example* là ví dụ sắp được xử lý. *got* là đầu ra thực tế từ ví dụ. *test* là bài kiểm thử chứa *example*. *out* là hàm đầu ra được truyền vào :meth:`DocTestRunner.run`.


   .. method:: report_failure(out, test, example, got)

      Báo cáo rằng ví dụ đã cho không thành công. Phương thức này được cung cấp để cho phép các lớp con của :class:`DocTestRunner` tùy chỉnh đầu ra; không nên gọi trực tiếp phương thức này.

      *example* là ví dụ sắp được xử lý. *got* là đầu ra thực tế từ ví dụ. *test* là bài kiểm thử chứa *example*. *out* là hàm đầu ra được truyền vào :meth:`DocTestRunner.run`.


   .. method:: report_unexpected_exception(out, test, example, exc_info)

      Báo cáo rằng ví dụ đã cho phát sinh một ngoại lệ không mong đợi. Phương thức này được cung cấp để cho phép các lớp con của :class:`DocTestRunner` tùy chỉnh đầu ra; không nên gọi trực tiếp phương thức này.

      *example* là ví dụ sắp được xử lý. *exc_info* là một tuple chứa thông tin về ngoại lệ không mong đợi (như được trả về bởi
      :func:`sys.exc_info`). *test* là bài kiểm thử chứa *example*. *out* là hàm đầu ra được truyền vào :meth:`DocTestRunner.run`.


   .. method:: run(test, compileflags=None, out=None, clear_globs=True)

      Chạy các ví dụ trong *test* (một đối tượng :class:`DocTest`) và hiển thị kết quả bằng hàm writer *out*. Trả về một thực thể :class:`TestResults`.

      Các ví dụ được chạy trong namespace ``test.globs``. Nếu *clear_globs* là true (mặc định), namespace này sẽ được xóa sau khi chạy kiểm thử để hỗ trợ việc thu gom rác. Nếu muốn kiểm tra namespace sau khi kiểm thử hoàn tất, hãy sử dụng *clear_globs=False*.

      *compileflags* cung cấp tập các cờ mà Python compiler sẽ sử dụng khi chạy các ví dụ. Nếu không được chỉ định, giá trị này mặc định là tập các cờ future-import áp dụng cho *globs*.

      Đầu ra của mỗi ví dụ được kiểm tra bằng output checker của :class:`DocTestRunner`, và kết quả được định dạng bởi
      các phương thức :meth:`!DocTestRunner.report_\*`.


   .. method:: summarize(verbose=None)

      In bản tóm tắt của tất cả test case đã được DocTestRunner này chạy, rồi trả về một thực thể :class:`TestResults`.

      Đối số tùy chọn *verbose* kiểm soát mức độ chi tiết của bản tóm tắt. Nếu không chỉ định verbosity, thì verbosity của :class:`DocTestRunner` sẽ được sử dụng.

   :class:`DocTestParser` có các thuộc tính sau:

   .. attribute:: tries

      Số lượng ví dụ đã thử.

   .. attribute:: failures

      Số lượng ví dụ không thành công.

   .. attribute:: skips

      Số lượng ví dụ bị bỏ qua.

      .. versionadded:: 3.13


.. _doctest-outputchecker:

Đối tượng OutputChecker
^^^^^^^^^^^^^^^^^^^^^^^


.. class:: OutputChecker()

   Một lớp được dùng để kiểm tra xem đầu ra thực tế từ một ví dụ doctest có khớp với đầu ra mong đợi hay không. :class:`OutputChecker` định nghĩa hai phương thức:
   :meth:`check_output`, dùng để so sánh một cặp đầu ra đã cho và trả về ``True`` nếu chúng khớp; và :meth:`output_difference`, trả về một chuỗi mô tả sự khác biệt giữa hai đầu ra.


   :class:`OutputChecker` định nghĩa các phương thức sau:

   .. method:: check_output(want, got, optionflags)

      Trả về ``True`` khi và chỉ khi đầu ra thực tế từ một ví dụ (*got*) khớp với đầu ra mong đợi (*want*). Các chuỗi này luôn được xem là khớp nếu chúng giống hệt nhau; tuy nhiên, tùy thuộc vào các cờ tùy chọn mà test runner đang sử dụng, cũng có thể có một số kiểu khớp không chính xác. Xem phần
      :ref:`doctest-options` để biết thêm thông tin về các cờ tùy chọn.


   .. method:: output_difference(example, got, optionflags)

      Trả về một chuỗi mô tả sự khác biệt giữa đầu ra mong đợi của một ví dụ cụ thể (*example*) và đầu ra thực tế (*got*). *optionflags* là tập hợp các cờ tùy chọn được sử dụng để so sánh *want* và *got*.


.. _doctest-debugging:

Gỡ lỗi
------

Doctest cung cấp một số cơ chế để gỡ lỗi các ví dụ doctest:

* Một số hàm chuyển đổi doctest thành các chương trình Python có thể thực thi, sau đó có thể chạy chúng dưới trình gỡ lỗi Python, :mod:`pdb`.

* Lớp :class:`DebugRunner` là lớp con của :class:`DocTestRunner`, lớp này sẽ phát sinh ngoại lệ đối với ví dụ đầu tiên không thành công và chứa thông tin về ví dụ đó. Thông tin này có thể được dùng để gỡ lỗi sau khi lỗi xảy ra (post-mortem debugging) cho ví dụ.

* Các trường hợp :mod:`unittest` được tạo bởi :func:`DocTestSuite` hỗ trợ
  phương thức :meth:`debug` được định nghĩa bởi :class:`unittest.TestCase`.

* Bạn có thể thêm lệnh gọi đến :func:`pdb.set_trace` trong một ví dụ doctest, và trình gỡ lỗi Python sẽ được mở khi dòng đó được thực thi. Sau đó, bạn có thể kiểm tra các giá trị hiện tại của biến, v.v. Ví dụ: giả sử :file:`a.py` chỉ chứa module docstring này::

     """
     >>> def f(x):
     ...     g(x*2)
     >>> def g(x):
     ...     print(x+3)
     ...     import pdb; pdb.set_trace()
     >>> f(3)
     9
     """

  Khi đó, một phiên Python tương tác có thể trông như sau::

     >>> import a, doctest
     >>> doctest.testmod(a)
     --Return--
     > <doctest a[1]>(3)g()->None
     -> import pdb; pdb.set_trace()
     (Pdb) list
       1     def g(x):
       2         print(x+3)
       3  ->     import pdb; pdb.set_trace()
     [EOF]
     (Pdb) p x
     6
     (Pdb) step
     --Return--
     > <doctest a[0]>(2)f()->None
     -> g(x*2)
     (Pdb) list
       1     def f(x):
       2  ->     g(x*2)
     [EOF]
     (Pdb) p x
     3
     (Pdb) step
     --Return--
     > <doctest a[2]>(1)?()->None
     -> f(3)
     (Pdb) cont
     (0, 3)
     >>>


Các hàm chuyển đổi doctest thành mã Python và có thể chạy mã được tạo dưới trình gỡ lỗi:


.. function:: script_from_examples(s)

   Chuyển đổi văn bản có các ví dụ thành một tập lệnh.

   Đối số *s* là một chuỗi chứa các ví dụ doctest. Chuỗi này được chuyển đổi thành một Python script, trong đó các ví dụ doctest trong *s* được chuyển thành mã thông thường, còn mọi phần khác được chuyển thành chú thích Python. Python script được tạo sẽ được trả về dưới dạng một chuỗi. Ví dụ:::

      import doctest
      print(doctest.script_from_examples(r"""
          Set x and y to 1 and 2.
          >>> x, y = 1, 2

          Print their sum:
          >>> print(x+y)
          3
      """))

   hiển thị::

      # Đặt x và y thành 1 và 2.
      x, y = 1, 2
      #
      # In tổng của chúng:
      print(x+y)
      # Dự kiến:
      ## 3

   Hàm này được các hàm khác sử dụng internally (xem bên dưới), nhưng cũng có thể hữu ích khi bạn muốn chuyển một phiên Python tương tác thành một Python script.


.. function:: testsource(module, name)

   Chuyển doctest của một đối tượng thành một script.

   Đối số *module* là một đối tượng module hoặc tên có dấu chấm của một module, chứa đối tượng có các doctest cần quan tâm. Đối số *name* là tên (bên trong module) của đối tượng có các doctest cần quan tâm. Kết quả là một chuỗi chứa docstring của đối tượng được chuyển đổi thành một tập lệnh Python, như mô tả cho
   :func:`script_from_examples` ở trên. Ví dụ: nếu module :file:`a.py` chứa một hàm cấp cao nhất :func:`!f`, thì::

      import a, doctest
      print(doctest.testsource(a, "a.f"))

   sẽ in ra phiên bản tập lệnh của docstring của hàm :func:`!f`, trong đó các doctest được chuyển đổi thành mã, còn phần còn lại được đặt trong các chú thích.


.. function:: debug(module, name, pm=False)

   Gỡ lỗi các doctest của một đối tượng.

   Các đối số *module* và *name* giống như đối với hàm
   :func:`testsource` ở trên. Tập lệnh Python được tạo từ docstring của đối tượng có tên sẽ được ghi vào một tệp tạm thời, sau đó tệp đó được chạy dưới sự điều khiển của trình gỡ lỗi Python, :mod:`pdb`.

   Một bản sao nông của ``module.__dict__`` được sử dụng làm ngữ cảnh thực thi cục bộ và toàn cục.

   Đối số tùy chọn *pm* kiểm soát việc có sử dụng gỡ lỗi sau sự cố (post-mortem) hay không. Nếu *pm* có giá trị true, tệp script được chạy trực tiếp và trình gỡ lỗi chỉ được kích hoạt nếu script kết thúc do phát sinh một ngoại lệ chưa được xử lý. Nếu xảy ra trường hợp đó, gỡ lỗi sau sự cố sẽ được gọi thông qua :func:`pdb.post_mortem`, với đối tượng traceback từ ngoại lệ chưa được xử lý. Nếu *pm* không được chỉ định hoặc có giá trị false, script sẽ được chạy dưới trình gỡ lỗi ngay từ đầu bằng cách truyền một lệnh gọi :func:`exec` thích hợp cho :func:`pdb.run`.


.. function:: debug_src(src, pm=False, globs=None)

   Gỡ lỗi các doctest trong một chuỗi.

   Tương tự như function :func:`debug` ở trên, ngoại trừ việc một chuỗi chứa các ví dụ doctest được chỉ định trực tiếp thông qua đối số *src*.

   Đối số tùy chọn *pm* có cùng ý nghĩa như trong function :func:`debug` ở trên.

   Đối số tùy chọn *globs* cung cấp một dictionary được dùng làm ngữ cảnh thực thi cục bộ và toàn cục. Nếu không được chỉ định hoặc là ``None``, một dictionary rỗng sẽ được sử dụng. Nếu được chỉ định, một bản sao nông của dictionary sẽ được sử dụng.


Class :class:`DebugRunner`, cùng các ngoại lệ đặc biệt mà nó có thể phát sinh, chủ yếu được các tác giả framework kiểm thử quan tâm và ở đây chỉ được phác thảo sơ lược. Xem mã nguồn, đặc biệt là docstring của :class:`DebugRunner` (vốn là một doctest!), để biết thêm chi tiết:


.. class:: DebugRunner(checker=None, verbose=None, optionflags=0)

   Một subclass của :class:`DocTestRunner` phát sinh ngoại lệ ngay khi phát hiện lỗi. Nếu xảy ra một ngoại lệ không mong đợi, một
   Một ngoại lệ :exc:`UnexpectedException` được đưa ra, chứa bài kiểm thử, ví dụ và ngoại lệ ban đầu. Nếu đầu ra không khớp, thì một
   ngoại lệ :exc:`DocTestFailure` được đưa ra, chứa bài kiểm thử, ví dụ và đầu ra thực tế.

   Để biết thông tin về các tham số của hàm khởi tạo và các phương thức, hãy xem tài liệu về :class:`DocTestRunner` trong phần :ref:`doctest-advanced-api`.

Có hai ngoại lệ mà các instance của :class:`DebugRunner` có thể đưa ra:


.. exception:: DocTestFailure(test, example, got)

   Một ngoại lệ được :class:`DocTestRunner` đưa ra để báo hiệu rằng đầu ra thực tế của một ví dụ doctest không khớp với đầu ra mong đợi. Các đối số của hàm khởi tạo được dùng để khởi tạo các thuộc tính có cùng tên.

:exc:`DocTestFailure` định nghĩa các thuộc tính sau:


.. attribute:: DocTestFailure.test

   Đối tượng :class:`DocTest` đang được chạy khi ví dụ không thành công.


.. attribute:: DocTestFailure.example

   :class:`Example` đã bị lỗi.


.. attribute:: DocTestFailure.got

   Kết quả thực tế của ví dụ.


.. exception:: UnexpectedException(test, example, exc_info)

   Một ngoại lệ do :class:`DocTestRunner` phát sinh để báo hiệu rằng một ví dụ doctest đã phát sinh một ngoại lệ không mong muốn. Các đối số của hàm khởi tạo được dùng để khởi tạo các thuộc tính cùng tên.

:exc:`UnexpectedException` định nghĩa các thuộc tính sau:


.. attribute:: UnexpectedException.test

   Đối tượng :class:`DocTest` đang được chạy khi ví dụ không thành công.


.. attribute:: UnexpectedException.example

   :class:`Example` đã bị lỗi.


.. attribute:: UnexpectedException.exc_info

   Một tuple chứa thông tin về ngoại lệ không mong muốn, như được trả về bởi
   :func:`sys.exc_info`.


.. _doctest-soapbox:

Chia sẻ quan điểm
-----------------

Như đã đề cập trong phần giới thiệu, :mod:`!doctest` đã phát triển để phục vụ ba mục đích chính:

#. Kiểm tra các ví dụ trong docstring.

#. Kiểm thử hồi quy.

#. Tài liệu có thể thực thi / kiểm thử kiểu literate.

Các mục đích này có những yêu cầu khác nhau, và điều quan trọng là phải phân biệt chúng. Đặc biệt, việc lấp đầy docstring bằng những trường hợp kiểm thử khó hiểu sẽ tạo ra tài liệu kém chất lượng.

Khi viết docstring, hãy cẩn thận lựa chọn các ví dụ cho docstring. Đây là một kỹ năng cần học---ban đầu có thể bạn sẽ không thấy tự nhiên. Các ví dụ phải thực sự làm tăng giá trị cho tài liệu. Một ví dụ hay thường có giá trị hơn rất nhiều câu chữ. Nếu được thực hiện cẩn thận, các ví dụ sẽ vô cùng hữu ích cho người dùng và sẽ đền đáp thời gian bạn bỏ ra để thu thập chúng nhiều lần trong những năm tiếp theo, khi mọi thứ thay đổi. Tôi vẫn ngạc nhiên trước việc một trong các ví dụ :mod:`!doctest` của mình thường xuyên ngừng hoạt động sau một thay đổi "vô hại".

Doctest cũng là một công cụ tuyệt vời để kiểm thử hồi quy, đặc biệt nếu bạn không cắt giảm phần văn bản giải thích. Bằng cách xen kẽ phần diễn giải và các ví dụ, việc theo dõi chính xác nội dung đang được kiểm thử và lý do kiểm thử trở nên dễ dàng hơn nhiều. Khi một kiểm thử thất bại, phần diễn giải tốt có thể giúp bạn dễ dàng hơn nhiều trong việc xác định vấn đề là gì và cần khắc phục như thế nào. Đúng là bạn có thể viết các chú thích chi tiết trong hoạt động kiểm thử dựa trên code, nhưng rất ít lập trình viên làm vậy. Nhiều người nhận thấy rằng sử dụng các phương pháp doctest thay vào đó sẽ tạo ra những kiểm thử rõ ràng hơn nhiều. Có lẽ đơn giản là vì doctest khiến việc viết phần diễn giải dễ hơn một chút so với viết code, trong khi việc viết chú thích trong code lại khó hơn một chút. Tôi nghĩ vấn đề còn sâu xa hơn thế: thái độ tự nhiên khi viết một kiểm thử dựa trên doctest là bạn muốn giải thích những điểm tinh tế trong phần mềm của mình và minh họa chúng bằng các ví dụ. Điều này đến lượt nó tự nhiên dẫn đến các tệp kiểm thử bắt đầu từ những tính năng đơn giản nhất, rồi tiến triển một cách logic đến các trường hợp phức tạp và các trường hợp biên. Kết quả là một mạch trình bày mạch lạc, thay vì một tập hợp các hàm biệt lập kiểm thử những phần chức năng biệt lập có vẻ như một cách ngẫu nhiên. Đó là một thái độ khác và tạo ra những kết quả khác, làm mờ ranh giới giữa kiểm thử và giải thích.

Tốt nhất nên giới hạn việc kiểm thử hồi quy trong các đối tượng hoặc tệp chuyên dụng. Có một số tùy chọn để tổ chức các kiểm thử:

* Viết các tệp văn bản chứa các trường hợp kiểm thử dưới dạng ví dụ tương tác, rồi kiểm thử các tệp bằng :func:`testfile` hoặc :func:`DocFileSuite`. Đây là cách được khuyến nghị, mặc dù dễ thực hiện nhất đối với các dự án mới được thiết kế ngay từ đầu để sử dụng doctest.

* Định nghĩa các hàm có tên ``_regrtest_topic`` chỉ gồm các docstring, chứa các trường hợp kiểm thử cho những chủ đề tương ứng. Các hàm này có thể được đưa vào cùng tệp với module hoặc tách riêng thành một tệp kiểm thử riêng.

* Định nghĩa một từ điển :attr:`~module.__test__` ánh xạ các chủ đề kiểm thử hồi quy với những docstring chứa các trường hợp kiểm thử.

Khi đã đặt các kiểm thử vào một module, chính module đó có thể làm test runner. Khi một kiểm thử thất bại, bạn có thể sắp xếp để test runner chỉ chạy lại doctest bị lỗi trong khi gỡ lỗi vấn đề. Sau đây là một ví dụ tối thiểu về một test runner như vậy::

    if __name__ == '__main__':
        import doctest
        flags = doctest.REPORT_NDIFF|doctest.FAIL_FAST
        if len(sys.argv) > 1:
            name = sys.argv[1]
            if name in globals():
                obj = globals()[name]
            else:
                obj = __test__[name]
            doctest.run_docstring_examples(obj, globals(), name=name,
                                           optionflags=flags)
        else:
            fail, total = doctest.testmod(optionflags=flags)
            print(f"{fail} failures out of {total} tests")


.. rubric:: Chú thích cuối trang

.. [#] Không hỗ trợ các ví dụ chứa cả đầu ra dự kiến và một ngoại lệ. Việc cố đoán xem phần này kết thúc ở đâu và phần kia bắt đầu từ đâu rất dễ dẫn đến lỗi, đồng thời cũng khiến bài kiểm thử trở nên khó hiểu.
