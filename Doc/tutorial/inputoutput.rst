.. _tut-io:

*****************
Đầu vào và đầu ra
*****************

Có một số cách để trình bày đầu ra của chương trình; dữ liệu có thể được in ở dạng dễ đọc đối với con người hoặc được ghi vào một tệp để sử dụng sau này. Chương này sẽ thảo luận về một số khả năng.


.. _tut-formatting:

Định dạng đầu ra nâng cao
=========================

Cho đến nay, chúng ta đã gặp hai cách ghi các giá trị: *các câu lệnh biểu thức* và :func:`print` function. (Cách thứ ba là sử dụng :meth:`~io.TextIOBase.write` method của các đối tượng tệp; tệp đầu ra tiêu chuẩn có thể được tham chiếu bằng ``sys.stdout``. Xem Library Reference để biết thêm thông tin về nội dung này.)

Thông thường, bạn sẽ muốn kiểm soát nhiều hơn đối với định dạng đầu ra thay vì chỉ in các giá trị được phân tách bằng khoảng trắng. Có một số cách để định dạng đầu ra.

* Để sử dụng :ref:`các literal chuỗi được định dạng <tut-f-strings>`, hãy bắt đầu một chuỗi bằng ``f`` hoặc ``F`` trước dấu ngoặc kép mở đầu hoặc dấu ngoặc kép ba. Bên trong chuỗi này, bạn có thể viết một biểu thức Python giữa các ký tự ``{`` và ``}``, biểu thức này có thể tham chiếu đến các biến hoặc giá trị literal.

  ::

     >>> year = 2016
     >>> event = 'Referendum'
     >>> f'Results of the {year} {event}'
     'Results of the 2016 Referendum'

* :meth:`str.format` method của chuỗi đòi hỏi nhiều thao tác thủ công hơn. Bạn vẫn sẽ sử dụng ``{`` và ``}`` để đánh dấu vị trí một biến sẽ được thay thế và có thể cung cấp các chỉ thị định dạng chi tiết, nhưng bạn cũng cần cung cấp thông tin cần được định dạng. Trong khối mã sau đây có hai ví dụ về cách định dạng các biến:


  ::

     >>> yes_votes = 42_572_654
     >>> total_votes = 85_705_149
     >>> percentage = yes_votes / total_votes
     >>> '{:-9} YES votes  {:2.2%}'.format(yes_votes, percentage)
     ' 42572654 YES votes  49.67%'

  Hãy chú ý rằng ``yes_votes`` được đệm bằng dấu cách và chỉ có dấu âm đối với các số âm. Ví dụ này cũng in ``percentage`` được nhân với 100, có 2 chữ số thập phân và theo sau là dấu phần trăm (xem :ref:`formatspec` để biết chi tiết).


* Cuối cùng, bạn có thể tự xử lý toàn bộ chuỗi bằng cách sử dụng các thao tác cắt và nối chuỗi để tạo ra bất kỳ bố cục nào bạn có thể hình dung. Kiểu chuỗi có một số phương thức thực hiện các thao tác hữu ích nhằm đệm chuỗi đến độ rộng cột cho trước.

Khi không cần đầu ra cầu kỳ mà chỉ muốn nhanh chóng hiển thị một số biến để debug, bạn có thể chuyển đổi bất kỳ giá trị nào thành chuỗi bằng các hàm :func:`repr` hoặc :func:`str`.

Hàm :func:`str` được dùng để trả về các biểu diễn của giá trị tương đối dễ đọc đối với con người, trong khi :func:`repr` được dùng để tạo ra các biểu diễn mà interpreter có thể đọc được (hoặc sẽ buộc phải có một :exc:`SyntaxError` nếu không có cú pháp tương đương). Đối với các đối tượng không có biểu diễn cụ thể dành cho con người, :func:`str` sẽ trả về cùng giá trị như
:func:`repr`. Nhiều giá trị, chẳng hạn như số hoặc các cấu trúc như list và dictionary, có cùng biểu diễn khi sử dụng một trong hai hàm. Đặc biệt, chuỗi có hai biểu diễn khác nhau.

Một số ví dụ::

   >>> s = 'Hello, world.'
   >>> str(s)
   'Hello, world.'
   >>> repr(s)
   "'Hello, world.'"
   >>> str(1/7)
   '0.14285714285714285'
   >>> x = 10 * 3.25
   >>> y = 200 * 200
   >>> s = 'The value of x is ' + repr(x) + ', and y is ' + repr(y) + '...'
   >>> print(s)
   The value of x is 32.5, and y is 40000...
   >>> # repr() của một chuỗi bổ sung dấu ngoặc kép của chuỗi và dấu gạch chéo ngược:
   >>> hello = 'hello, world\n'
   >>> hellos = repr(hello)
   >>> print(hellos)
   'hello, world\n'
   >>> # Đối số của repr() có thể là bất kỳ đối tượng Python nào:
   >>> repr((x, y, ('spam', 'eggs')))
   "(32.5, 40000, ('spam', 'eggs'))"

Mô-đun :mod:`string` cung cấp hỗ trợ cho một phương pháp tạo mẫu đơn giản dựa trên regular expression, thông qua :class:`string.Template`. Đây là một cách khác để thay thế các giá trị trong chuỗi, bằng cách sử dụng các placeholder như ``$x`` và thay thế chúng bằng các giá trị từ một dictionary. Cú pháp này dễ sử dụng, mặc dù cung cấp ít quyền kiểm soát hơn nhiều đối với việc định dạng.

.. index::
   single: formatted string literal
   single: interpolated string literal
   single: string; formatted literal
   single: string; interpolated literal
   single: f-string
   single: fstring

.. _tut-f-strings:

Các literal chuỗi được định dạng
--------------------------------

:ref:`Các literal chuỗi được định dạng <f-strings>` (còn được gọi tắt là f-string) cho phép bạn đưa giá trị của các biểu thức Python vào trong chuỗi bằng cách thêm ``f`` hoặc ``F`` vào trước chuỗi và viết các biểu thức dưới dạng ``{expression}``.

Một format specifier tùy chọn có thể được đặt sau biểu thức. Điều này cho phép kiểm soát tốt hơn cách giá trị được định dạng. Ví dụ sau làm tròn pi đến ba chữ số sau dấu thập phân::

   >>> import math
   >>> print(f'The value of pi is approximately {math.pi:.3f}.')
   The value of pi is approximately 3.142.

Truyền một số nguyên sau ``':'`` sẽ khiến trường đó có độ rộng tối thiểu bằng số ký tự được chỉ định. Điều này hữu ích để căn thẳng các cột.::

   >>> table = {'Sjoerd': 4127, 'Jack': 4098, 'Dcab': 7678}
   >>> for name, phone in table.items():
   ...     print(f'{name:10} ==> {phone:10d}')
   ...
   Sjoerd     ==>       4127
   Jack       ==>       4098
   Dcab       ==>       7678

Có thể sử dụng các modifier khác để chuyển đổi giá trị trước khi định dạng. ``'!a'`` áp dụng :func:`ascii`, ``'!s'`` áp dụng :func:`str`, và ``'!r'`` áp dụng :func:`repr`::

   >>> animals = 'eels'
   >>> print(f'My hovercraft is full of {animals}.')
   My hovercraft is full of eels.
   >>> print(f'My hovercraft is full of {animals!r}.')
   My hovercraft is full of 'eels'.

Bộ chỉ định ``=`` có thể được dùng để mở rộng một biểu thức thành văn bản của biểu thức đó, một dấu bằng, rồi đến biểu diễn của biểu thức đã được đánh giá:

   >>> bugs = 'roaches'
   >>> count = 13
   >>> area = 'living room'
   >>> print(f'Debugging {bugs=} {count=} {area=}')
   Debugging bugs='roaches' count=13 area='living room'

Xem :ref:`biểu thức tự mô tả <bpo-36817-whatsnew>` để biết thêm thông tin về bộ chỉ định ``=``. Để tham khảo về các đặc tả định dạng này, hãy xem hướng dẫn tham khảo về :ref:`formatspec`.

.. _tut-string-format:

Phương thức format() của chuỗi
------------------------------

Cách sử dụng cơ bản của phương thức :meth:`str.format` trông như sau::

   >>> print('We are the {} who say "{}!"'.format('knights', 'Ni'))
   We are the knights who say "Ni!"

Các dấu ngoặc và ký tự bên trong chúng (được gọi là các trường định dạng) sẽ được thay thế bằng các đối tượng được truyền vào phương thức :meth:`str.format`. Có thể dùng một số trong dấu ngoặc để tham chiếu đến vị trí của đối tượng được truyền vào
phương thức :meth:`str.format`.::

   >>> print('{0} and {1}'.format('spam', 'eggs'))
   spam and eggs
   >>> print('{1} and {0}'.format('spam', 'eggs'))
   eggs and spam

Nếu sử dụng các đối số từ khóa trong phương thức :meth:`str.format`, các giá trị của chúng được tham chiếu bằng cách dùng tên của đối số.::

   >>> print('This {food} is {adjective}.'.format(
   ...       food='spam', adjective='absolutely horrible'))
   This spam is absolutely horrible.

Các đối số vị trí và đối số từ khóa có thể được kết hợp tùy ý::

   >>> print('The story of {0}, {1}, and {other}.'.format('Bill', 'Manfred',
   ...                                                    other='Georg'))
   The story of Bill, Manfred, and Georg.

Nếu bạn có một format string thực sự dài mà không muốn chia nhỏ, sẽ thật tiện nếu bạn có thể tham chiếu đến các biến cần định dạng bằng tên thay vì vị trí. Bạn có thể thực hiện việc này bằng cách chỉ cần truyền dict và sử dụng dấu ngoặc vuông ``'[]'`` để truy cập các khóa.::

   >>> table = {'Sjoerd': 4127, 'Jack': 4098, 'Dcab': 8637678}
   >>> print('Jack: {0[Jack]:d}; Sjoerd: {0[Sjoerd]:d}; '
   ...       'Dcab: {0[Dcab]:d}'.format(table))
   Jack: 4098; Sjoerd: 4127; Dcab: 8637678

Bạn cũng có thể thực hiện việc này bằng cách truyền dictionary ``table`` dưới dạng các đối số từ khóa với ký hiệu ``**``.::

   >>> table = {'Sjoerd': 4127, 'Jack': 4098, 'Dcab': 8637678}
   >>> print('Jack: {Jack:d}; Sjoerd: {Sjoerd:d}; Dcab: {Dcab:d}'.format(**table))
   Jack: 4098; Sjoerd: 4127; Dcab: 8637678

Điều này đặc biệt hữu ích khi kết hợp với hàm tích hợp sẵn
:func:`vars`, hàm này trả về một dictionary chứa tất cả các biến cục bộ::

   >>> table = {k: str(v) for k, v in vars().items()}
   >>> message = " ".join([f'{k}: ' + '{' + k +'};' for k in table.keys()])
   >>> print(message.format(**table))
   __name__: __main__; __doc__: None; __package__: None; __loader__: ...

Ví dụ, các dòng sau tạo ra một tập hợp cột được căn chỉnh gọn gàng, hiển thị các số nguyên cùng với bình phương và lập phương của chúng::

   >>> for x in range(1, 11):
   ...     print('{0:2d} {1:3d} {2:4d}'.format(x, x*x, x*x*x))
   ...
    1   1    1
    2   4    8
    3   9   27
    4  16   64
    5  25  125
    6  36  216
    7  49  343
    8  64  512
    9  81  729
   10 100 1000

Để xem tổng quan đầy đủ về việc định dạng chuỗi với :meth:`str.format`, hãy xem
:ref:`formatstrings`.


Định dạng chuỗi thủ công
------------------------

Đây là cùng một bảng bình phương và lập phương, được định dạng thủ công::

   >>> for x in range(1, 11):
   ...     print(repr(x).rjust(2), repr(x*x).rjust(3), end=' ')
   ...     # Lưu ý việc sử dụng 'end' ở dòng trước
   ...     print(repr(x*x*x).rjust(4))
   ...
    1   1    1
    2   4    8
    3   9   27
    4  16   64
    5  25  125
    6  36  216
    7  49  343
    8  64  512
    9  81  729
   10 100 1000

(Lưu ý rằng khoảng trắng duy nhất giữa mỗi cột được thêm vào bởi cách :func:`print` hoạt động: nó luôn thêm khoảng trắng giữa các đối số.)

Phương thức :meth:`str.rjust` của các đối tượng chuỗi căn phải một chuỗi trong một trường có độ rộng cho trước bằng cách đệm khoảng trắng ở bên trái. Có các phương thức tương tự là :meth:`str.ljust` và :meth:`str.center`. Các phương thức này không ghi bất cứ thứ gì, chúng chỉ trả về một chuỗi mới. Nếu chuỗi đầu vào quá dài, chúng không cắt bớt chuỗi mà trả về nguyên trạng; điều này sẽ làm rối bố cục các cột, nhưng thường vẫn tốt hơn phương án còn lại, vốn sẽ làm sai lệch một giá trị. (Nếu thực sự muốn cắt bớt, bạn luôn có thể thêm thao tác lấy lát cắt, như trong ``x.ljust(n)[:n]``.)

Có một phương thức khác, :meth:`str.zfill`, dùng để đệm một chuỗi số ở bên trái bằng các số 0. Nó hiểu các dấu cộng và dấu trừ::

   >>> '12'.zfill(5)
   '00012'
   >>> '-3.14'.zfill(7)
   '-003.14'
   >>> '3.14159265359'.zfill(5)
   '3.14159265359'


Định dạng chuỗi kiểu cũ
-----------------------

Toán tử % (modulo) cũng có thể được dùng để định dạng chuỗi. Với ``format % values`` (trong đó *format* là một chuỗi), ``%`` các đặc tả chuyển đổi trong *format* được thay thế bằng không hoặc nhiều phần tử của *values*. Thao tác này thường được gọi là nội suy chuỗi. Ví dụ::

   >>> import math
   >>> print('The value of pi is approximately %5.3f.' % math.pi)
   The value of pi is approximately 3.142.

Bạn có thể tìm thêm thông tin trong phần :ref:`old-string-formatting`.


.. _tut-files:

Đọc và Ghi Tệp
==============

.. index::
   pair: built-in function; open
   pair: object; file

:func:`open` trả về một :term:`file object`, và thường được sử dụng nhất với hai đối số vị trí và một đối số keyword: ``open(filename, mode, encoding=None)``

::

   >>> f = open('workfile', 'w', encoding="utf-8")

.. XXX str(f) is <io.TextIOWrapper object at 0x82e8dc4>

   >>> print(f)
   <open file 'workfile', mode 'w' at 80a0960>

Đối số đầu tiên là một chuỗi chứa tên tệp. Đối số thứ hai là một chuỗi khác chứa một vài ký tự mô tả cách tệp sẽ được sử dụng. *mode* có thể là ``'r'`` khi tệp chỉ được đọc, ``'w'`` khi chỉ ghi (một tệp hiện có cùng tên sẽ bị xóa), và ``'a'`` để mở tệp cho việc nối thêm; mọi dữ liệu được ghi vào tệp sẽ tự động được thêm vào cuối tệp. ``'r+'`` mở tệp để đọc và ghi. Đối số *mode* là tùy chọn; ``'r'`` sẽ được giả định nếu đối số này bị bỏ qua.

Thông thường, các tệp được mở ở :dfn:`text mode`, nghĩa là bạn đọc và ghi các chuỗi vào và từ tệp; các chuỗi này được mã hóa bằng một *encoding* cụ thể. Nếu không chỉ định *encoding*, mặc định sẽ phụ thuộc vào nền tảng (xem :func:`open`). Vì UTF-8 là tiêu chuẩn trên thực tế hiện đại, nên khuyến nghị sử dụng ``encoding="utf-8"`` trừ khi bạn biết mình cần một encoding khác. Thêm một ``'b'`` vào mode sẽ mở tệp ở :dfn:`binary mode`. Dữ liệu ở binary mode được đọc và ghi dưới dạng các đối tượng :class:`bytes`. Bạn không thể chỉ định *encoding* khi mở tệp ở binary mode.

Ở text mode, mặc định khi đọc là chuyển đổi các ký tự kết thúc dòng đặc thù theo nền tảng (``\n`` trên Unix, ``\r\n`` trên Windows) thành chỉ ``\n``. Khi ghi ở text mode, mặc định là chuyển đổi các lần xuất hiện của ``\n`` trở lại thành ký tự kết thúc dòng đặc thù theo nền tảng. Việc sửa đổi dữ liệu tệp ngầm phía sau này phù hợp với các tệp văn bản, nhưng sẽ làm hỏng dữ liệu nhị phân như dữ liệu trong
các tệp :file:`JPEG` hoặc :file:`EXE`. Hãy đặc biệt cẩn thận sử dụng chế độ nhị phân khi đọc và ghi các tệp như vậy.

Bạn nên sử dụng từ khóa :keyword:`with` khi làm việc với các đối tượng tệp. Ưu điểm là tệp được đóng đúng cách sau khi phần lệnh của nó kết thúc, ngay cả khi có ngoại lệ xảy ra tại một thời điểm nào đó. Sử dụng :keyword:`!with` cũng ngắn gọn hơn nhiều so với việc viết các khối :keyword:`try`\ -\ :keyword:`finally` tương đương.::

    >>> with open('workfile', encoding="utf-8") as f:
    ...     read_data = f.read()

    >>> # Chúng ta có thể kiểm tra xem tệp đã được tự động đóng hay chưa.
    >>> f.closed
    True

Nếu không sử dụng từ khóa :keyword:`with`, bạn nên gọi ``f.close()`` để đóng tệp và ngay lập tức giải phóng mọi tài nguyên hệ thống mà tệp đang sử dụng.

.. warning::
   Việc gọi ``f.write()`` mà không sử dụng từ khóa :keyword:`!with` hoặc gọi ``f.close()`` **might** khiến các đối số của ``f.write()`` có thể không được ghi hoàn toàn vào đĩa, ngay cả khi chương trình thoát thành công.

..
   Xem thêm https://bugs.python.org/issue17852

Sau khi một đối tượng tệp được đóng, είτε bằng câu lệnh :keyword:`with` hoặc bằng cách gọi ``f.close()``, mọi nỗ lực sử dụng đối tượng tệp sẽ tự động thất bại.::

   >>> f.close()
   >>> f.read()
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   ValueError: I/O operation on closed file.


.. _tut-filemethods:

Các phương thức của đối tượng tệp
---------------------------------

Các ví dụ còn lại trong phần này giả định rằng một đối tượng tệp có tên là ``f`` đã được tạo.

Để đọc nội dung của một tệp, hãy gọi ``f.read(size)``, phương thức này đọc một lượng dữ liệu nhất định và trả về dữ liệu đó dưới dạng chuỗi (ở chế độ văn bản) hoặc đối tượng bytes (ở chế độ nhị phân). *size* là một đối số số tùy chọn. Khi *size* bị bỏ qua hoặc là số âm, toàn bộ nội dung của tệp sẽ được đọc và trả về; nếu tệp lớn gấp đôi dung lượng bộ nhớ của máy thì đó là vấn đề của bạn. Nếu không, nhiều nhất *size* ký tự (ở chế độ văn bản) hoặc *size* byte (ở chế độ nhị phân) sẽ được đọc và trả về. Khi đã đến cuối tệp, ``f.read()`` sẽ trả về một chuỗi rỗng (``''``).::

   >>> f.read()
   'This is the entire file.\n'
   >>> f.read()
   ''

``f.readline()`` đọc một dòng duy nhất từ tệp; một ký tự xuống dòng (``\n``) được giữ lại ở cuối chuỗi và chỉ bị bỏ qua ở dòng cuối cùng của tệp nếu tệp không kết thúc bằng ký tự xuống dòng. Điều này giúp giá trị trả về không gây nhầm lẫn; nếu ``f.readline()`` trả về một chuỗi rỗng thì đã đến cuối tệp, còn một dòng trống được biểu diễn bằng ``'\n'``, một chuỗi chỉ chứa duy nhất một ký tự xuống dòng.::

   >>> f.readline()
   'This is the first line of the file.\n'
   >>> f.readline()
   'Second line of the file\n'
   >>> f.readline()
   ''

Để đọc các dòng từ một tệp, bạn có thể lặp qua đối tượng tệp. Cách này tiết kiệm bộ nhớ, nhanh và giúp tạo ra mã đơn giản::

   >>> for line in f:
   ...     print(line, end='')
   ...
   This is the first line of the file.
   Second line of the file

Nếu muốn đọc tất cả các dòng của một tệp vào một list, bạn cũng có thể sử dụng ``list(f)`` hoặc ``f.readlines()``.

``f.write(string)`` ghi nội dung của *string* vào tệp và trả về số ký tự đã ghi.::

   >>> f.write('This is a test\n')
   15

Các kiểu đối tượng khác cần được chuyển đổi -- thành chuỗi (ở chế độ văn bản) hoặc đối tượng bytes (ở chế độ nhị phân) -- trước khi ghi chúng::

   >>> value = ('the answer', 42)
   >>> s = str(value)  # chuyển tuple thành chuỗi
   >>> f.write(s)
   18

``f.tell()`` trả về một số nguyên cho biết vị trí hiện tại của đối tượng tệp trong tệp, được biểu diễn dưới dạng số byte tính từ đầu tệp khi ở chế độ nhị phân và một số không trong suốt khi ở chế độ văn bản.

Để thay đổi vị trí của đối tượng tệp, hãy sử dụng ``f.seek(offset, whence)``. Vị trí được tính bằng cách cộng *offset* với một điểm tham chiếu; điểm tham chiếu được chọn bởi đối số *whence*. Giá trị *whence* bằng 0 tính từ đầu tệp, bằng 1 sử dụng vị trí hiện tại của tệp và bằng 2 sử dụng cuối tệp làm điểm tham chiếu. Có thể bỏ qua *whence* và giá trị mặc định là 0, sử dụng đầu tệp làm điểm tham chiếu.::

   >>> f = open('workfile', 'rb+')
   >>> f.write(b'0123456789abcdef')
   16
   >>> f.seek(5)      # Đi tới byte thứ 6 trong tệp
   5
   >>> f.read(1)
   b'5'
   >>> f.seek(-3, 2)  # Đi tới byte thứ 3 tính từ cuối tệp
   13
   >>> f.read(1)
   b'd'

Trong các tệp văn bản (những tệp được mở mà không có ``b`` trong chuỗi mode), chỉ cho phép seek tương đối so với đầu tệp (ngoại lệ là seek đến đúng cuối tệp bằng ``seek(0, 2)``) và các giá trị *offset* hợp lệ duy nhất là những giá trị được ``f.tell()`` trả về hoặc bằng không. Bất kỳ giá trị *offset* nào khác đều tạo ra hành vi không xác định.

Đối tượng tệp còn có một số phương thức bổ sung, chẳng hạn như :meth:`~io.IOBase.isatty` và
:meth:`~io.IOBase.truncate`, ít được sử dụng hơn; hãy tham khảo Tài liệu Tham khảo Thư viện để có hướng dẫn đầy đủ về các đối tượng tệp.


.. _tut-json:

Lưu dữ liệu có cấu trúc bằng :mod:`json`
----------------------------------------

.. index:: pair: module; json

Bạn có thể dễ dàng ghi và đọc chuỗi từ một tệp. Số cần nhiều thao tác hơn một chút, vì phương thức :meth:`~io.TextIOBase.read` chỉ trả về chuỗi, và chuỗi đó phải được truyền cho một hàm như :func:`int`, hàm này nhận một chuỗi như ``'123'`` và trả về giá trị số 123 tương ứng. Khi muốn lưu các kiểu dữ liệu phức tạp hơn như danh sách lồng nhau và từ điển, việc tự phân tích cú pháp và tuần tự hóa trở nên phức tạp.

Thay vì để người dùng liên tục viết và gỡ lỗi mã để lưu các kiểu dữ liệu phức tạp vào tệp, Python cho phép bạn sử dụng định dạng trao đổi dữ liệu phổ biến có tên là `JSON (JavaScript Object Notation) <https://json.org>`_. Mô-đun chuẩn có tên :mod:`json` có thể tiếp nhận các cấu trúc phân cấp dữ liệu Python và chuyển đổi chúng thành biểu diễn chuỗi; quá trình này được gọi là :dfn:`tuần tự hóa (serializing)`. Việc tái tạo dữ liệu từ biểu diễn chuỗi được gọi là :dfn:`giải tuần tự hóa (deserializing)`. Trong khoảng thời gian giữa việc tuần tự hóa và giải tuần tự hóa, chuỗi biểu diễn đối tượng có thể đã được lưu trong một tệp hoặc cơ sở dữ liệu, hoặc được gửi qua kết nối mạng đến một máy ở xa.

.. note::
   Định dạng JSON thường được các ứng dụng hiện đại sử dụng để cho phép trao đổi dữ liệu. Nhiều lập trình viên đã quen thuộc với định dạng này, khiến nó trở thành một lựa chọn phù hợp cho khả năng tương tác.

Nếu bạn có một đối tượng ``x``, bạn có thể xem biểu diễn chuỗi JSON của đối tượng đó bằng một dòng mã đơn giản::

   >>> import json
   >>> x = [1, 'simple', 'list']
   >>> json.dumps(x)
   '[1, "simple", "list"]'

Một biến thể khác của hàm :func:`~json.dumps`, có tên là :func:`~json.dump`, chỉ đơn giản là tuần tự hóa đối tượng thành :term:`text file`. Vì vậy, nếu ``f`` là một
đối tượng :term:`text file` được mở để ghi, chúng ta có thể làm như sau::

   json.dump(x, f)

Để giải mã đối tượng một lần nữa, nếu ``f`` là một :term:`binary file` hoặc
đối tượng :term:`text file` đã được mở để đọc::

   x = json.load(f)

.. note::
   Các tệp JSON phải được mã hóa bằng UTF-8. Sử dụng ``encoding="utf-8"`` khi mở tệp JSON dưới dạng :term:`text file` để đọc và ghi.

Kỹ thuật tuần tự hóa đơn giản này có thể xử lý các danh sách và từ điển, nhưng việc tuần tự hóa các thực thể lớp tùy ý trong JSON đòi hỏi thêm một chút công sức. Tài liệu tham khảo về mô-đun :mod:`json` có giải thích về vấn đề này.

.. seealso::

   :mod:`pickle` - mô-đun pickle

   Trái với :ref:`JSON <tut-json>`, *pickle* là một giao thức cho phép tuần tự hóa các đối tượng Python phức tạp tùy ý. Vì vậy, nó dành riêng cho Python và không thể được dùng để giao tiếp với các ứng dụng được viết bằng ngôn ngữ khác. Theo mặc định, nó cũng không an toàn: việc giải tuần tự hóa dữ liệu pickle đến từ một nguồn không đáng tin cậy có thể thực thi mã tùy ý nếu dữ liệu đó được tạo bởi một kẻ tấn công có kỹ năng.

.. _`JSON (JavaScript Object Notation)`: https://json.org
