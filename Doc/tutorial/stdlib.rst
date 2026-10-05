.. _tut-brieftour:

********************************
Tham quan ngắn về thư viện chuẩn
********************************


.. _tut-os-interface:

Giao diện hệ điều hành
======================

Mô-đun :mod:`os` cung cấp hàng chục hàm để tương tác với hệ điều hành::

   >>> import os
   >>> os.getcwd()      # Trả về thư mục làm việc hiện tại
   'C:\\Python314'
   >>> os.chdir('/server/accesslogs')   # Thay đổi thư mục làm việc hiện tại
   >>> os.system('mkdir today')   # Chạy lệnh mkdir trong system shell
   0

Hãy chắc chắn sử dụng kiểu ``import os`` thay vì ``from os import *``. Điều này sẽ ngăn :func:`os.open` che khuất hàm :func:`open` tích hợp sẵn, vốn hoạt động rất khác.

.. index:: pair: built-in function; help

Các hàm tích hợp sẵn :func:`dir` và :func:`help` rất hữu ích như những công cụ hỗ trợ tương tác khi làm việc với các module lớn như :mod:`os`::

   >>> import os
   >>> dir(os)
   <returns a list of all module functions>
   >>> help(os)
   <returns an extensive manual page created from the module's docstrings>

Đối với các tác vụ quản lý tệp và thư mục hằng ngày, module :mod:`shutil` cung cấp một interface cấp cao hơn, dễ sử dụng hơn::

   >>> import shutil
   >>> shutil.copyfile('data.db', 'archive.db')
   'archive.db'
   >>> shutil.move('/build/executables', 'installdir')
   'installdir'


.. _tut-file-wildcards:

Ký tự đại diện cho tệp
======================

Module :mod:`glob` cung cấp một hàm để tạo danh sách tệp từ các tìm kiếm ký tự đại diện trong thư mục::

   >>> import glob
   >>> glob.glob('*.py')
   ['primes.py', 'random.py', 'quote.py']


.. _tut-command-line-arguments:

Đối số dòng lệnh
================

Các script tiện ích phổ biến thường cần xử lý các đối số dòng lệnh. Các đối số này được lưu trữ dưới dạng một danh sách trong thuộc tính *argv* của module :mod:`sys`. Chẳng hạn, hãy xem tệp :file:`demo.py` sau đây::

   # Tệp demo.py
   import sys
   print(sys.argv)

Đây là kết quả khi chạy ``python demo.py one two three`` trên dòng lệnh::

   ['demo.py', 'one', 'two', 'three']

Mô-đun :mod:`argparse` cung cấp một cơ chế tinh vi hơn để xử lý các đối số dòng lệnh. Tập lệnh sau trích xuất một hoặc nhiều tên tệp cùng với số dòng tùy chọn cần hiển thị::

    import argparse

    parser = argparse.ArgumentParser(
        prog='top',
        description='Show top lines from each file')
    parser.add_argument('filenames', nargs='+')
    parser.add_argument('-l', '--lines', type=int, default=10)
    args = parser.parse_args()
    print(args)

Khi được chạy trên dòng lệnh với ``python top.py --lines=5 alpha.txt beta.txt``, tập lệnh đặt ``args.lines`` thành ``5`` và ``args.filenames`` thành ``['alpha.txt', 'beta.txt']``.


.. _tut-stderr:

Chuyển hướng đầu ra lỗi và kết thúc chương trình
================================================

Mô-đun :mod:`sys` cũng có các thuộc tính cho *stdin*, *stdout* và *stderr*. Thuộc tính sau rất hữu ích để phát ra các cảnh báo và thông báo lỗi, giúp chúng vẫn hiển thị ngay cả khi *stdout* đã được chuyển hướng::

   >>> sys.stderr.write('Warning, log file not found starting a new one\n')
   Warning, log file not found starting a new one

Cách trực tiếp nhất để kết thúc một tập lệnh là sử dụng ``sys.exit()``.


.. _tut-string-pattern-matching:

Đối sánh mẫu chuỗi
==================

module :mod:`re` cung cấp các công cụ biểu thức chính quy để xử lý chuỗi nâng cao. Đối với việc so khớp và thao tác phức tạp, biểu thức chính quy cung cấp các giải pháp ngắn gọn, được tối ưu hóa::

   >>> import re
   >>> re.findall(r'\bf[a-z]*', 'which foot or hand fell fastest')
   ['foot', 'fell', 'fastest']
   >>> re.sub(r'(\b[a-z]+) \1', r'\1', 'cat in the the hat')
   'cat in the hat'

Khi chỉ cần các khả năng đơn giản, nên ưu tiên các phương thức chuỗi vì chúng dễ đọc và gỡ lỗi hơn::

   >>> 'tea for too'.replace('too', 'two')
   'tea for two'


.. _tut-mathematics:

Toán học
========

module :mod:`math` cho phép truy cập các hàm thư viện C bên dưới để thực hiện các phép toán số thực dấu phẩy động::

   >>> import math
   >>> math.cos(math.pi / 4)
   0.70710678118654757
   >>> math.log(1024, 2)
   10.0

module :mod:`random` cung cấp các công cụ để thực hiện việc chọn ngẫu nhiên::

   >>> import random
   >>> random.choice(['apple', 'pear', 'banana'])
   'apple'
   >>> random.sample(range(100), 10)   # lấy mẫu không hoàn lại
   [30, 83, 16, 4, 8, 81, 41, 50, 18, 33]
   >>> random.random()    # số thực ngẫu nhiên trong khoảng [0.0, 1.0)
   0.17970987693706186
   >>> random.randrange(6)    # số nguyên ngẫu nhiên được chọn từ range(6)
   4

Mô-đun :mod:`statistics` tính toán các đặc tính thống kê cơ bản (trung bình, trung vị, phương sai, v.v.) của dữ liệu số::

    >>> import statistics
    >>> data = [2.75, 1.75, 1.25, 0.25, 0.5, 1.25, 3.5]
    >>> statistics.mean(data)
    1.6071428571428572
    >>> statistics.median(data)
    1.25
    >>> statistics.variance(data)
    1.3720238095238095

Dự án SciPy <https://scipy.org> có nhiều mô-đun khác để tính toán số.

.. _tut-internet-access:

Truy cập Internet
=================

Có một số mô-đun để truy cập Internet và xử lý các giao thức Internet. Hai mô-đun đơn giản nhất là :mod:`urllib.request` để truy xuất dữ liệu từ các URL và :mod:`smtplib` để gửi thư::

   >>> from urllib.request import urlopen
   >>> with urlopen('https://docs.python.org/3/') as response:
   ...     for line in response:
   ...         line = line.decode()             # Chuyển đổi bytes thành str
   ...         if 'updated' in line:
   ...             print(line.rstrip())         # Xóa ký tự xuống dòng ở cuối
   ...
         Last updated on Nov 11, 2025 (20:11 UTC).

   >>> import smtplib
   >>> server = smtplib.SMTP('localhost')
   >>> server.sendmail('soothsayer@example.org', 'jcaesar@example.org',
   ... """To: jcaesar@example.org
   ... From: soothsayer@example.org
   ...
   ... Beware the Ides of March.
   ... """)
   >>> server.quit()

(Lưu ý rằng ví dụ thứ hai cần có mailserver đang chạy trên localhost.)


.. _tut-dates-and-times:

Ngày tháng và thời gian
=======================

Mô-đun :mod:`datetime` cung cấp các lớp để thao tác với ngày tháng và thời gian theo cả cách đơn giản lẫn phức tạp. Mặc dù hỗ trợ các phép tính số học trên ngày tháng và thời gian, trọng tâm của việc triển khai là trích xuất thành viên hiệu quả để định dạng và thao tác đầu ra. Mô-đun này cũng hỗ trợ các đối tượng nhận biết múi giờ.::

   >>> # dễ dàng tạo và định dạng ngày tháng
   >>> import datetime as dt
   >>> now = dt.date.today()
   >>> now
   datetime.date(2003, 12, 2)
   >>> now.strftime("%m-%d-%y. %d %b %Y is a %A on the %d day of %B.")
   '12-02-03. 02 Dec 2003 is a Tuesday on the 02 day of December.'

   >>> # ngày tháng hỗ trợ các phép tính lịch
   >>> birthday = dt.date(1964, 7, 31)
   >>> age = now - birthday
   >>> age.days
   14368


.. _tut-data-compression:

Nén dữ liệu
===========

Các định dạng lưu trữ và nén dữ liệu phổ biến được hỗ trợ trực tiếp bởi các mô-đun bao gồm: :mod:`zlib`, :mod:`gzip`, :mod:`bz2`, :mod:`lzma`, :mod:`zipfile` và
:mod:`tarfile`. ::

   >>> import zlib
   >>> s = b'witch which has which witches wrist watch'
   >>> len(s)
   41
   >>> t = zlib.compress(s)
   >>> len(t)
   37
   >>> zlib.decompress(t)
   b'witch which has which witches wrist watch'
   >>> zlib.crc32(s)
   226805979


.. _tut-performance-measurement:

Đo lường hiệu năng
==================

Một số người dùng Python đặc biệt quan tâm đến việc biết hiệu năng tương đối của các phương pháp khác nhau cho cùng một vấn đề. Python cung cấp một công cụ đo lường giúp trả lời ngay những câu hỏi đó.

Ví dụ, bạn có thể muốn sử dụng tính năng đóng gói và giải nén tuple thay cho cách truyền thống để hoán đổi các đối số. Module :mod:`timeit` nhanh chóng cho thấy một lợi thế hiệu năng khiêm tốn::

   >>> from timeit import Timer
   >>> Timer('t=a; a=b; b=t', 'a=1; b=2').timeit()
   0.57535828626024577
   >>> Timer('a,b = b,a', 'a=1; b=2').timeit()
   0.54962537085770791

So với mức độ chi tiết cao của :mod:`timeit`, :mod:`profile` và
các module :mod:`pstats` cung cấp công cụ để xác định những phần nhạy cảm về thời gian trong các khối mã lớn hơn.


.. _tut-quality-control:

Kiểm soát chất lượng
====================

Một cách để phát triển phần mềm chất lượng cao là viết các bài kiểm thử cho từng hàm ngay khi phát triển hàm đó và thường xuyên chạy các bài kiểm thử trong suốt quá trình phát triển.

Mô-đun :mod:`doctest` cung cấp một công cụ để quét một mô-đun và xác thực các bài kiểm thử được nhúng trong docstring của chương trình. Việc tạo bài kiểm thử đơn giản như cắt và dán một lệnh gọi điển hình cùng với kết quả của nó vào docstring. Điều này cải thiện tài liệu bằng cách cung cấp cho người dùng một ví dụ, đồng thời cho phép mô-đun doctest đảm bảo mã vẫn khớp với tài liệu.::

   def average(values):
       """Computes the arithmetic mean of a list of numbers.

       >>> print(average([20, 30, 70]))
       40.0
       """
       return sum(values) / len(values)

   import doctest
   doctest.testmod()   # tự động xác thực các bài kiểm thử được nhúng

Mô-đun :mod:`unittest` không dễ sử dụng như mô-đun :mod:`doctest`, nhưng cho phép duy trì một tập hợp bài kiểm thử đầy đủ hơn trong một tệp riêng.::

   import unittest

   class TestStatisticalFunctions(unittest.TestCase):

       def test_average(self):
           self.assertEqual(average([20, 30, 70]), 40.0)
           self.assertEqual(round(average([1, 5, 7]), 1), 4.3)
           with self.assertRaises(ZeroDivisionError):
               average([])
           with self.assertRaises(TypeError):
               average(20, 30, 70)

   unittest.main()  # Gọi từ command line sẽ chạy tất cả bài kiểm thử


.. _tut-batteries-included:

Tích hợp sẵn
============

Python có triết lý "tích hợp sẵn". Điều này thể hiện rõ nhất qua các khả năng tinh vi và mạnh mẽ của những package lớn hơn. Ví dụ:

* Các mô-đun :mod:`xmlrpc.client` và :mod:`xmlrpc.server` khiến việc triển khai remote procedure call gần như trở nên quá đơn giản. Bất chấp tên gọi của các mô-đun, không cần có hiểu biết trực tiếp về XML hay phải tự xử lý XML.

* Gói :mod:`email` là một thư viện dùng để quản lý các email, bao gồm MIME và những tài liệu thư dựa trên :rfc:`5322` khác. Không giống :mod:`smtplib` và
  :mod:`poplib`, vốn thực sự gửi và nhận email, gói email cung cấp một bộ công cụ hoàn chỉnh để xây dựng hoặc giải mã các cấu trúc thư phức tạp (bao gồm cả tệp đính kèm), cũng như triển khai các giao thức mã hóa trên Internet và giao thức header.

* Gói :mod:`json` cung cấp khả năng hỗ trợ mạnh mẽ cho việc phân tích cú pháp định dạng trao đổi dữ liệu phổ biến này. Mô-đun :mod:`csv` hỗ trợ đọc và ghi trực tiếp các tệp ở định dạng Comma-Separated Value, thường được các cơ sở dữ liệu và bảng tính hỗ trợ. Việc xử lý XML được hỗ trợ bởi :mod:`xml.etree.ElementTree`, :mod:`xml.dom` và
  các gói :mod:`xml.sax`. Kết hợp với nhau, các mô-đun và gói này giúp đơn giản hóa đáng kể việc trao đổi dữ liệu giữa các ứng dụng Python và những công cụ khác.

* Mô-đun :mod:`sqlite3` là một wrapper cho thư viện cơ sở dữ liệu SQLite, cung cấp một cơ sở dữ liệu persistent có thể được cập nhật và truy cập bằng cú pháp SQL hơi khác chuẩn.

* Quốc tế hóa được hỗ trợ bởi một số mô-đun, bao gồm
  :mod:`gettext`, :mod:`locale` và gói :mod:`codecs`.
