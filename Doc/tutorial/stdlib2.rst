.. _tut-brieftourtwo:

*************************************
Sơ lược về thư viện chuẩn --- phần II
*************************************

Phần sơ lược thứ hai này đề cập đến các module nâng cao hơn, hỗ trợ những nhu cầu lập trình chuyên nghiệp. Các module này hiếm khi xuất hiện trong những script nhỏ.


.. _tut-output-formatting:

Định dạng đầu ra
================

Module :mod:`reprlib` cung cấp một phiên bản của :func:`repr` được tùy chỉnh để hiển thị rút gọn các container lớn hoặc lồng nhau sâu::

   >>> import reprlib
   >>> reprlib.repr(set('supercalifragilisticexpialidocious'))
   "{'a', 'c', 'd', 'e', 'f', 'g', ...}"

Module :mod:`pprint` cho phép kiểm soát tinh vi hơn việc in cả các object dựng sẵn và object do người dùng định nghĩa theo cách mà interpreter có thể đọc được. Khi kết quả dài hơn một dòng, “pretty printer” sẽ thêm ngắt dòng và thụt lề để làm lộ rõ hơn cấu trúc dữ liệu::

   >>> import pprint
   >>> t = [[[['black', 'cyan'], 'white', ['green', 'red']], [['magenta',
   ...     'yellow'], 'blue']]]
   ...
   >>> pprint.pprint(t, width=30)
   [[[['black', 'cyan'],
      'white',
      ['green', 'red']],
     [['magenta', 'yellow'],
      'blue']]]

Module :mod:`textwrap` định dạng các đoạn văn bản sao cho vừa với chiều rộng màn hình nhất định::

   >>> import textwrap
   >>> doc = """The wrap() method is just like fill() except that it returns
   ... a list of strings instead of one big string with newlines to separate
   ... the wrapped lines."""
   ...
   >>> print(textwrap.fill(doc, width=40))
   The wrap() method is just like fill()
   except that it returns a list of strings
   instead of one big string with newlines
   to separate the wrapped lines.

Module :mod:`locale` truy cập cơ sở dữ liệu về các định dạng dữ liệu đặc thù theo văn hóa. Thuộc tính grouping của hàm format trong locale cung cấp một cách trực tiếp để định dạng các số với dấu phân cách nhóm::

   >>> import locale
   >>> locale.setlocale(locale.LC_ALL, 'English_United States.1252')
   'English_United States.1252'
   >>> conv = locale.localeconv()          # lấy ánh xạ các quy ước
   >>> x = 1234567.8
   >>> locale.format_string("%d", x, grouping=True)
   '1,234,567'
   >>> locale.format_string("%s%.*f", (conv['currency_symbol'],
   ...                      conv['frac_digits'], x), grouping=True)
   '$1,234,567.80'


.. _tut-templating:

Tạo mẫu
=======

Mô-đun :mod:`string` bao gồm một lớp :class:`~string.Template` linh hoạt với cú pháp đơn giản, phù hợp để người dùng cuối chỉnh sửa. Điều này cho phép người dùng tùy chỉnh ứng dụng của họ mà không cần thay đổi ứng dụng.

Định dạng này sử dụng các tên placeholder được tạo bởi ``$`` với các định danh Python hợp lệ (các ký tự chữ-số và dấu gạch dưới). Việc bao quanh placeholder bằng dấu ngoặc nhọn cho phép theo sau nó là nhiều ký tự chữ-số hơn mà không cần khoảng trắng. Viết ``$$`` sẽ tạo ra một ``$`` được escape duy nhất::

   >>> from string import Template
   >>> t = Template('${village}folk send $$10 to $cause.')
   >>> t.substitute(village='Nottingham', cause='the ditch fund')
   'Nottinghamfolk send $10 to the ditch fund.'

Phương thức :meth:`~string.Template.substitute` sẽ phát sinh :exc:`KeyError` khi một placeholder không được cung cấp trong một dictionary hoặc đối số từ khóa. Đối với các ứng dụng kiểu trộn thư, dữ liệu do người dùng cung cấp có thể không đầy đủ và
phương thức :meth:`~string.Template.safe_substitute` có thể phù hợp hơn — phương thức này sẽ giữ nguyên các placeholder nếu thiếu dữ liệu::

   >>> t = Template('Return the $item to $owner.')
   >>> d = dict(item='unladen swallow')
   >>> t.substitute(d)
   Traceback (most recent call last):
     ...
   KeyError: 'owner'
   >>> t.safe_substitute(d)
   'Return the unladen swallow to $owner.'

Các lớp con của Template có thể chỉ định một dấu phân cách tùy chỉnh. Ví dụ, một tiện ích đổi tên hàng loạt cho trình duyệt ảnh có thể chọn sử dụng dấu phần trăm cho các placeholder như ngày hiện tại, số thứ tự ảnh hoặc định dạng tệp::

   >>> import time, os.path
   >>> photofiles = ['img_1074.jpg', 'img_1076.jpg', 'img_1077.jpg']
   >>> class BatchRename(Template):
   ...     delimiter = '%'
   ...
   >>> fmt = input('Enter rename style (%d-date %n-seqnum %f-format):  ')
   Enter rename style (%d-date %n-seqnum %f-format):  Ashley_%n%f

   >>> t = BatchRename(fmt)
   >>> date = time.strftime('%d%b%y')
   >>> for i, filename in enumerate(photofiles):
   ...     base, ext = os.path.splitext(filename)
   ...     newname = t.substitute(d=date, n=i, f=ext)
   ...     print('{0} --> {1}'.format(filename, newname))

   img_1074.jpg --> Ashley_0.jpg
   img_1076.jpg --> Ashley_1.jpg
   img_1077.jpg --> Ashley_2.jpg

Một ứng dụng khác của templating là tách logic chương trình khỏi các chi tiết của nhiều định dạng đầu ra. Điều này giúp có thể thay thế bằng các template tùy chỉnh cho tệp XML, báo cáo văn bản thuần túy và báo cáo web HTML.


.. _tut-binary-formats:

Làm việc với bố cục bản ghi dữ liệu nhị phân
============================================

Mô-đun :mod:`struct` cung cấp :func:`~struct.pack` và
các hàm :func:`~struct.unpack` để làm việc với các định dạng bản ghi nhị phân có độ dài thay đổi. Ví dụ sau đây cho thấy cách lặp qua thông tin header trong tệp ZIP mà không sử dụng mô-đun
:mod:`zipfile`. Các mã pack ``"H"`` và ``"I"`` lần lượt biểu diễn các số không dấu dài hai và bốn byte. ``"<"`` cho biết rằng chúng có kích thước tiêu chuẩn và theo thứ tự byte little-endian::

   import struct

   with open('myfile.zip', 'rb') as f:
       data = f.read()

   start = 0
   for i in range(3):                      # hiển thị 3 header tệp đầu tiên
       start += 14
       fields = struct.unpack('<IIIHH', data[start:start+16])
       crc32, comp_size, uncomp_size, filenamesize, extra_size = fields

       start += 16
       filename = data[start:start+filenamesize]
       start += filenamesize
       extra = data[start:start+extra_size]
       print(filename, hex(crc32), comp_size, uncomp_size)

       start += extra_size + comp_size     # chuyển đến header tiếp theo


.. _tut-multi-threading:

Đa luồng
========

Lập trình luồng là một kỹ thuật tách rời các tác vụ không phụ thuộc tuần tự vào nhau. Các thread có thể được sử dụng để cải thiện khả năng phản hồi của các ứng dụng tiếp nhận dữ liệu đầu vào từ người dùng trong khi các tác vụ khác chạy ở chế độ nền. Một trường hợp sử dụng liên quan là chạy các thao tác I/O song song với các phép tính trong một thread khác.

Đoạn mã sau đây cho thấy cách module cấp cao :mod:`threading` có thể chạy các tác vụ ở chế độ nền trong khi chương trình chính vẫn tiếp tục chạy::

   import threading, zipfile

   class AsyncZip(threading.Thread):
       def __init__(self, infile, outfile):
           super().__init__()
           self.infile = infile
           self.outfile = outfile

       def run(self):
           with zipfile.ZipFile(self.outfile, 'w', zipfile.ZIP_DEFLATED) as f:
               f.write(self.infile)
           print('Finished background zip of:', self.infile)

   background = AsyncZip('mydata.txt', 'myarchive.zip')
   background.start()
   print('The main program continues to run in foreground.')

   background.join()    # Chờ tác vụ nền hoàn tất
   print('Main program waited until background was done.')

Thách thức chính của các ứng dụng đa luồng là điều phối các thread chia sẻ dữ liệu hoặc các tài nguyên khác. Để đạt được mục đích đó, module threading cung cấp một số primitive đồng bộ hóa, bao gồm lock, event, biến điều kiện và semaphore.

Mặc dù các công cụ đó rất mạnh, những lỗi nhỏ trong thiết kế có thể dẫn đến các vấn đề khó tái hiện. Vì vậy, cách tiếp cận được ưu tiên để điều phối tác vụ là tập trung toàn bộ quyền truy cập vào một tài nguyên trong một thread duy nhất, sau đó sử dụng
module :mod:`queue` để cung cấp cho thread đó các yêu cầu từ những thread khác. Các ứng dụng sử dụng các object :class:`~queue.Queue` để giao tiếp và điều phối giữa các thread sẽ dễ thiết kế hơn, dễ đọc hơn và đáng tin cậy hơn.


.. _tut-logging:

Ghi nhật ký
===========

Mô-đun :mod:`logging` cung cấp một hệ thống ghi nhật ký đầy đủ tính năng và linh hoạt. Ở dạng đơn giản nhất, các thông báo nhật ký được gửi đến một tệp hoặc đến ``sys.stderr``::

   import logging
   logging.debug('Debugging information')
   logging.info('Informational message')
   logging.warning('Warning:config file %s not found', 'server.conf')
   logging.error('Error occurred')
   logging.critical('Critical error -- shutting down')

Kết quả này tạo ra đầu ra sau:

.. code-block:: none

   WARNING:root:Warning:config file server.conf not found
   ERROR:root:Error occurred
   CRITICAL:root:Critical error -- shutting down

Theo mặc định, các thông báo thông tin và gỡ lỗi bị ẩn, còn đầu ra được gửi đến lỗi chuẩn. Các tùy chọn đầu ra khác bao gồm định tuyến thông báo qua email, datagram, socket hoặc đến HTTP Server. Các bộ lọc mới có thể chọn cách định tuyến khác nhau dựa trên mức độ ưu tiên của thông báo: :const:`~logging.DEBUG`,
:const:`~logging.INFO`, :const:`~logging.WARNING`, :const:`~logging.ERROR` và :const:`~logging.CRITICAL`.

Hệ thống ghi nhật ký có thể được cấu hình trực tiếp từ Python hoặc được tải từ một tệp cấu hình do người dùng chỉnh sửa để tùy biến việc ghi nhật ký mà không cần thay đổi ứng dụng.


.. _tut-weak-references:

Tham chiếu yếu
==============

Python tự động quản lý bộ nhớ (đếm tham chiếu đối với hầu hết các đối tượng và
:term:`garbage collection` để loại bỏ các chu kỳ). Bộ nhớ được giải phóng ngay sau khi tham chiếu cuối cùng đến nó bị loại bỏ.

Cách tiếp cận này hoạt động tốt với hầu hết các ứng dụng, nhưng đôi khi cần theo dõi các đối tượng chỉ trong thời gian chúng đang được một thứ khác sử dụng. Đáng tiếc là việc chỉ theo dõi chúng đã tạo ra một tham chiếu khiến chúng tồn tại vĩnh viễn. Module :mod:`weakref` cung cấp các công cụ để theo dõi đối tượng mà không tạo tham chiếu. Khi đối tượng không còn cần thiết, nó sẽ tự động bị xóa khỏi bảng weakref và một callback được kích hoạt cho các đối tượng weakref. Các ứng dụng điển hình bao gồm lưu vào bộ nhớ đệm những đối tượng tốn kém khi tạo ra::

   >>> import weakref, gc
   >>> class A:
   ...     def __init__(self, value):
   ...         self.value = value
   ...     def __repr__(self):
   ...         return str(self.value)
   ...
   >>> a = A(10)                   # tạo một tham chiếu
   >>> d = weakref.WeakValueDictionary()
   >>> d['primary'] = a            # không tạo một tham chiếu
   >>> d['primary']                # lấy đối tượng nếu nó vẫn còn tồn tại
   10
   >>> del a                       # xóa tham chiếu đó
   >>> gc.collect()                # chạy bộ thu gom rác ngay lập tức
   0
   >>> d['primary']                # mục nhập đã được tự động xóa
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
       d['primary']                # mục nhập đã được tự động xóa
     File "C:/python314/lib/weakref.py", line 46, in __getitem__
       o = self.data[key]()
   KeyError: 'primary'


.. _tut-list-tools:

Các công cụ làm việc với list
=============================

Nhiều nhu cầu về cấu trúc dữ liệu có thể được đáp ứng bằng kiểu list tích hợp sẵn. Tuy nhiên, đôi khi cần có các cách triển khai thay thế với những đánh đổi về hiệu năng khác nhau.

Mô-đun :mod:`array` cung cấp một đối tượng :class:`~array.array` tương tự list nhưng chỉ lưu trữ dữ liệu đồng nhất và lưu trữ dữ liệu đó gọn hơn. Ví dụ sau đây cho thấy một mảng các số được lưu dưới dạng số nhị phân không dấu hai byte (typecode ``"H"``) thay vì 16 byte cho mỗi mục nhập như các list thông thường gồm các đối tượng int của Python::

   >>> from array import array
   >>> a = array('H', [4000, 10, 700, 22222])
   >>> sum(a)
   26932
   >>> a[1:3]
   array('H', [10, 700])

Mô-đun :mod:`collections` cung cấp một đối tượng :class:`~collections.deque` tương tự list, với thao tác thêm và lấy phần tử ở phía bên trái nhanh hơn nhưng thao tác tra cứu ở giữa chậm hơn. Các đối tượng này rất phù hợp để triển khai queue và tìm kiếm cây theo chiều rộng::

   >>> from collections import deque
   >>> d = deque(["task1", "task2", "task3"])
   >>> d.append("task4")
   >>> print("Handling", d.popleft())
   Handling task1

::

   unsearched = deque([starting_node])
   def breadth_first_search(unsearched):
       node = unsearched.popleft()
       for m in gen_moves(node):
           if is_goal(m):
               return m
           unsearched.append(m)

Ngoài các cách triển khai list thay thế, thư viện còn cung cấp những công cụ khác như module :mod:`bisect` với các hàm thao tác trên các list đã sắp xếp::

   >>> import bisect
   >>> scores = [(100, 'perl'), (200, 'tcl'), (400, 'lua'), (500, 'python')]
   >>> bisect.insort(scores, (300, 'ruby'))
   >>> scores
   [(100, 'perl'), (200, 'tcl'), (300, 'ruby'), (400, 'lua'), (500, 'python')]

Module :mod:`heapq` cung cấp các hàm để triển khai heap dựa trên các list thông thường. Phần tử có giá trị nhỏ nhất luôn được giữ ở vị trí 0. Điều này hữu ích cho các ứng dụng thường xuyên truy cập phần tử nhỏ nhất nhưng không muốn thực hiện việc sắp xếp toàn bộ list::

   >>> from heapq import heapify, heappop, heappush
   >>> data = [1, 3, 5, 7, 9, 2, 4, 6, 8, 0]
   >>> heapify(data)                      # sắp xếp lại list theo thứ tự heap
   >>> heappush(data, -5)                 # thêm một phần tử mới
   >>> [heappop(data) for i in range(3)]  # lấy ba phần tử nhỏ nhất
   [-5, 0, 1]


.. _tut-decimal-fp:

Số học dấu phẩy động thập phân
==============================

Module :mod:`decimal` cung cấp một kiểu dữ liệu :class:`~decimal.Decimal` cho số học dấu phẩy động thập phân. So với cách triển khai dấu phẩy động nhị phân tích hợp sẵn :class:`float`, class này đặc biệt hữu ích cho

* các ứng dụng tài chính và những mục đích sử dụng khác yêu cầu biểu diễn số thập phân chính xác tuyệt đối,
* kiểm soát độ chính xác,
* kiểm soát việc làm tròn để đáp ứng các yêu cầu pháp lý hoặc quy định,
* theo dõi số chữ số thập phân có nghĩa, hoặc
* các ứng dụng mà người dùng mong đợi kết quả khớp với các phép tính thực hiện bằng tay.

Ví dụ: tính thuế 5% trên cước điện thoại 70 cent cho kết quả khác nhau khi dùng số dấu phẩy động thập phân và số dấu phẩy động nhị phân. Sự khác biệt trở nên đáng kể nếu kết quả được làm tròn đến cent gần nhất::

   >>> from decimal import *
   >>> round(Decimal('0.70') * Decimal('1.05'), 2)
   Decimal('0.74')
   >>> round(.70 * 1.05, 2)
   0.73

Kết quả :class:`~decimal.Decimal` giữ lại một số 0 ở cuối, tự động suy ra độ chính xác bốn chữ số thập phân từ các thừa số có độ chính xác hai chữ số thập phân. Decimal tái hiện phép toán như khi thực hiện bằng tay và tránh các vấn đề có thể phát sinh khi số dấu phẩy động nhị phân không thể biểu diễn chính xác các đại lượng thập phân.

Biểu diễn chính xác cho phép lớp :class:`~decimal.Decimal` thực hiện các phép tính modulo và kiểm tra tính bằng nhau, vốn không phù hợp với số dấu phẩy động nhị phân::

   >>> Decimal('1.00') % Decimal('.10')
   Decimal('0.00')
   >>> 1.00 % 0.10
   0.09999999999999995

   >>> sum([Decimal('0.1')]*10) == Decimal('1.0')
   True
   >>> 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 + 0.1 == 1.0
   False

Mô-đun :mod:`decimal` cung cấp các phép tính số học với độ chính xác cao tùy theo nhu cầu::

   >>> getcontext().prec = 36
   >>> Decimal(1) / Decimal(7)
   Decimal('0.142857142857142857142857142857142857')


