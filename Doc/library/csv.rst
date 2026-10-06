:mod:`!csv` --- Đọc và Ghi Tệp CSV
==================================

.. module:: csv
   :synopsis: Ghi và đọc dữ liệu dạng bảng vào và từ các tệp được phân tách.

.. sectionauthor:: Skip Montanaro <skip.montanaro@gmail.com>

**Mã nguồn:** :source:`Lib/csv.py`

.. index::
   single: csv
   pair: data; tabular

--------------

Định dạng CSV (Comma Separated Values, các giá trị được phân tách bằng dấu phẩy) được gọi là này là định dạng nhập và xuất phổ biến nhất cho bảng tính và cơ sở dữ liệu. Định dạng CSV đã được sử dụng trong nhiều năm trước khi có những nỗ lực mô tả định dạng này theo cách được chuẩn hóa trong
:rfc:`4180`. Việc thiếu một tiêu chuẩn được định nghĩa rõ ràng có nghĩa là thường tồn tại những khác biệt nhỏ trong dữ liệu do các ứng dụng khác nhau tạo ra và sử dụng. Những khác biệt này có thể khiến việc xử lý các tệp CSV từ nhiều nguồn trở nên phiền phức. Tuy nhiên, mặc dù các dấu phân cách và ký tự trích dẫn khác nhau, định dạng tổng thể vẫn đủ tương đồng để có thể viết một module duy nhất có khả năng thao tác hiệu quả với loại dữ liệu này, ẩn các chi tiết đọc và ghi dữ liệu khỏi lập trình viên.

Module :mod:`!csv` triển khai các lớp để đọc và ghi dữ liệu dạng bảng ở định dạng CSV. Module này cho phép lập trình viên nói rằng "hãy ghi dữ liệu này theo định dạng được Excel ưu tiên," hoặc "hãy đọc dữ liệu từ tệp được Excel tạo ra," mà không cần biết các chi tiết chính xác về định dạng CSV được Excel sử dụng. Lập trình viên cũng có thể mô tả các định dạng CSV mà những ứng dụng khác hiểu được hoặc tự định nghĩa các định dạng CSV chuyên dụng.

Các đối tượng :class:`reader` và :class:`writer` của module :mod:`!csv` đọc và ghi các sequence. Lập trình viên cũng có thể đọc và ghi dữ liệu ở dạng dictionary bằng cách sử dụng các lớp :class:`DictReader` và :class:`DictWriter`.

.. seealso::

   :pep:`305` - API tệp CSV
      Python Enhancement Proposal đã đề xuất bổ sung này vào Python.


.. _csv-contents:

Nội dung mô-đun
---------------

Mô-đun :mod:`!csv` định nghĩa các hàm sau:


.. index::
   single: universal newlines; csv.reader function

.. function:: reader(csvfile, /, dialect='excel', **fmtparams)

   Trả về một :ref:`đối tượng reader <reader-objects>` để xử lý các dòng từ *csvfile* đã cho. csvfile phải là một iterable gồm các chuỗi, mỗi chuỗi tuân theo định dạng csv do reader xác định. csvfile thường là một đối tượng giống tệp hoặc một danh sách. Nếu *csvfile* là một đối tượng tệp, đối tượng đó nên được mở bằng ``newline=''``. [1]_  Có thể cung cấp tham số tùy chọn *dialect*, được dùng để xác định một tập hợp các tham số dành riêng cho một dialect CSV cụ thể. Tham số này có thể là một thể hiện của lớp con của lớp :class:`Dialect` hoặc một trong các chuỗi được hàm
   :func:`list_dialects` trả về. Có thể cung cấp các đối số từ khóa *fmtparams* tùy chọn khác để ghi đè từng tham số định dạng trong dialect hiện tại. Để biết đầy đủ chi tiết về dialect và các tham số định dạng, hãy xem phần :ref:`csv-fmt-params`.

   Mỗi hàng được đọc từ tệp csv được trả về dưới dạng một danh sách các chuỗi. Không thực hiện chuyển đổi kiểu dữ liệu tự động, trừ khi chỉ định tùy chọn định dạng :data:`QUOTE_NONNUMERIC` (khi đó các trường không được đặt trong dấu ngoặc kép sẽ được chuyển thành số thực).

   Một ví dụ ngắn về cách sử dụng::

      >>> import csv
      >>> with open('eggs.csv', newline='') as csvfile:
      ...     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
      ...     for row in spamreader:
      ...         print(', '.join(row))
      Spam, Spam, Spam, Spam, Spam, Baked Beans
      Spam, Lovely Spam, Wonderful Spam

   trong đó :file:`eggs.csv` chứa:

   .. code-block:: text

      Spam Spam Spam Spam Spam |Baked Beans|
      Spam |Lovely Spam| |Wonderful Spam|


.. function:: writer(csvfile, /, dialect='excel', **fmtparams)

   Trả về một đối tượng writer chịu trách nhiệm chuyển đổi dữ liệu của người dùng thành các chuỗi được phân tách trên đối tượng giống tệp được cung cấp. *csvfile* có thể là bất kỳ đối tượng nào có một
   :meth:`~io.TextIOBase.write` method. Nếu *csvfile* là một đối tượng tệp, đối tượng đó nên được mở bằng ``newline=''`` [1]_. Có thể cung cấp tham số *dialect* tùy chọn để xác định một tập hợp các tham số dành riêng cho một dialect CSV cụ thể. Tham số này có thể là một thể hiện của một lớp con của
   :class:`Dialect` class hoặc một trong các chuỗi được trả về bởi
   :func:`list_dialects` function. Có thể cung cấp các đối số từ khóa *fmtparams* tùy chọn khác để ghi đè từng tham số định dạng trong dialect hiện tại. Để biết đầy đủ chi tiết về dialect và các tham số định dạng, hãy xem phần :ref:`csv-fmt-params`. Để việc tích hợp với các module triển khai DB API dễ dàng nhất có thể, giá trị :const:`None` được ghi dưới dạng chuỗi rỗng. Mặc dù đây không phải là phép chuyển đổi có thể đảo ngược, cách này giúp dễ dàng kết xuất các giá trị dữ liệu SQL NULL vào tệp CSV mà không cần tiền xử lý dữ liệu được trả về từ một lệnh gọi ``cursor.fetch*``. Mọi dữ liệu không phải chuỗi khác đều được chuyển thành chuỗi bằng :func:`str` trước khi được ghi.

   Một ví dụ ngắn về cách sử dụng::

      import csv
      with open('eggs.csv', 'w', newline='') as csvfile:
          spamwriter = csv.writer(csvfile, delimiter=' ',
                                  quotechar='|', quoting=csv.QUOTE_MINIMAL)
          spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
          spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

   ghi :file:`eggs.csv` chứa:

   .. code-block:: text

      Spam Spam Spam Spam Spam |Baked Beans|
      Spam |Lovely Spam| |Wonderful Spam|


.. function:: register_dialect(name, /, dialect='excel', **fmtparams)

   Liên kết *dialect* với *name*. *name* phải là một chuỗi. Dialect có thể được chỉ định bằng cách truyền một lớp con của :class:`Dialect`, hoặc bằng các đối số từ khóa *fmtparams*, hoặc bằng cả hai; các đối số từ khóa sẽ ghi đè các tham số của dialect. Để biết đầy đủ chi tiết về dialect và các tham số định dạng, hãy xem phần :ref:`csv-fmt-params`.


.. function:: unregister_dialect(name)

   Xóa dialect được liên kết với *name* khỏi registry của các dialect. Một
   :exc:`Error` được phát sinh nếu *name* không phải là tên dialect đã đăng ký.


.. function:: get_dialect(name)

   Trả về dialect được liên kết với *name*. Một :exc:`Error` được phát sinh nếu *name* không phải là tên dialect đã đăng ký. Hàm này trả về một
   :class:`Dialect`.

.. function:: list_dialects()

   Trả về tên của tất cả các dialect đã đăng ký.


.. function:: field_size_limit()
              field_size_limit(new_limit)

   Trả về kích thước trường tối đa hiện tại được parser cho phép. Nếu cung cấp *new_limit*, giá trị này sẽ trở thành giới hạn mới.


Mô-đun :mod:`!csv` định nghĩa các lớp sau:

.. class:: DictReader(f, fieldnames=None, restkey=None, restval=None, \
                      dialect='excel', *args, **kwds)

   Tạo một đối tượng hoạt động như một reader thông thường nhưng ánh xạ thông tin trong mỗi hàng vào một :class:`dict` với các khóa được chỉ định bởi tham số *fieldnames* tùy chọn.

   Tham số *fieldnames* là một :term:`sequence`. Nếu bỏ qua *fieldnames*, các giá trị trong hàng đầu tiên của tệp *f* sẽ được sử dụng làm fieldnames và bị loại khỏi kết quả. Nếu cung cấp *fieldnames*, chúng sẽ được sử dụng và hàng đầu tiên sẽ được đưa vào kết quả. Bất kể fieldnames được xác định như thế nào, dictionary vẫn giữ nguyên thứ tự ban đầu của chúng.

   Nếu một hàng có nhiều trường hơn số fieldnames, dữ liệu còn lại sẽ được đưa vào một danh sách và lưu với fieldname được chỉ định bởi *restkey* (mặc định là ``None``). Nếu một hàng không trống có ít trường hơn số fieldnames, các giá trị còn thiếu sẽ được điền bằng giá trị của *restval* (mặc định là ``None``).

   Tất cả các đối số tùy chọn hoặc đối số từ khóa khác đều được truyền cho đối tượng nền tảng
   một thể hiện của :class:`reader`.

   Nếu đối số được truyền cho *fieldnames* là một iterator, nó sẽ được chuyển đổi thành một :class:`list`.

   .. versionchanged:: 3.6
      Các hàng được trả về hiện có kiểu :class:`OrderedDict`.

   .. versionchanged:: 3.8
      Các hàng được trả về hiện có kiểu :class:`dict`.

   Một ví dụ ngắn về cách sử dụng::

       >>> import csv
       >>> with open('names.csv', newline='') as csvfile:
       ...     reader = csv.DictReader(csvfile)
       ...     for row in reader:
       ...         print(row['first_name'], row['last_name'])
       ...
       Eric Idle
       John Cleese

       >>> print(row)
       {'first_name': 'John', 'last_name': 'Cleese'}

   trong đó :file:`names.csv` chứa:

   .. code-block:: text

      first_name,last_name
      Eric,Idle
      John,Cleese


.. class:: DictWriter(f, fieldnames, restval='', extrasaction='raise', \
                      dialect='excel', *args, **kwds)

   Tạo một đối tượng hoạt động như một writer thông thường nhưng ánh xạ các dictionary thành các hàng đầu ra. Tham số *fieldnames* là một :mod:`sequence <collections.abc>` gồm các khóa xác định thứ tự ghi các giá trị trong dictionary được truyền vào phương thức :meth:`~csvwriter.writerow` vào tệp *f*. Tham số tùy chọn *restval* chỉ định giá trị sẽ được ghi nếu dictionary thiếu một khóa trong *fieldnames*. Nếu dictionary được truyền vào phương thức :meth:`~csvwriter.writerow` chứa một khóa không có trong *fieldnames*, tham số tùy chọn *extrasaction* cho biết cần thực hiện hành động nào. Nếu được đặt thành ``'raise'``, giá trị mặc định, một :exc:`ValueError` sẽ được phát sinh. Nếu được đặt thành ``'ignore'``, các giá trị bổ sung trong dictionary sẽ bị bỏ qua. Mọi đối số tùy chọn hoặc đối số từ khóa khác được truyền cho
   đối tượng :class:`writer` bên dưới.

   Lưu ý rằng không giống như lớp :class:`DictReader`, tham số *fieldnames* của lớp :class:`DictWriter` không phải là tùy chọn.

   Nếu đối số được truyền cho *fieldnames* là một iterator, nó sẽ được chuyển đổi thành một :class:`list`.

   Một ví dụ ngắn về cách sử dụng::

       import csv

       with open('names.csv', 'w', newline='') as csvfile:
           fieldnames = ['first_name', 'last_name']
           writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

           writer.writeheader()
           writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
           writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
           writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})

   ghi :file:`names.csv` chứa:

   .. code-block:: text

      first_name,last_name
      Baked,Beans
      Lovely,Spam
      Wonderful,Spam


.. class:: Dialect

   Lớp :class:`Dialect` là một lớp chứa các thuộc tính cung cấp thông tin về cách xử lý dấu ngoặc kép, khoảng trắng, dấu phân cách, v.v. Do thiếu một đặc tả CSV nghiêm ngặt, các ứng dụng khác nhau tạo ra dữ liệu CSV có những khác biệt nhỏ. Các đối tượng :class:`Dialect` xác định cách
   Các instance :class:`reader` và :class:`writer` hoạt động như nhau.

   Tất cả tên :class:`Dialect` hiện có được :func:`list_dialects` trả về và có thể được đăng ký với các lớp :class:`reader` và :class:`writer` cụ thể thông qua các hàm ``__init__`` khởi tạo của chúng như sau::

       import csv

       with open('students.csv', 'w', newline='') as csvfile:
           writer = csv.writer(csvfile, dialect='unix')


.. class:: excel()

   Lớp :class:`excel` định nghĩa các thuộc tính thông thường của tệp CSV được tạo bởi Excel. Lớp này được đăng ký với tên dialect ``'excel'``.


.. class:: excel_tab()

   Lớp :class:`excel_tab` định nghĩa các thuộc tính thông thường của tệp TAB-delimited được tạo bởi Excel. Lớp này được đăng ký với tên dialect ``'excel-tab'``.


.. class:: unix_dialect()

   Lớp :class:`unix_dialect` định nghĩa các thuộc tính thông thường của tệp CSV được tạo trên các hệ thống UNIX, tức là sử dụng ``'\n'`` làm dấu kết thúc dòng và đặt dấu ngoặc kép quanh tất cả các trường. Lớp này được đăng ký với tên dialect ``'unix'``.

   .. versionadded:: 3.2


.. class:: Sniffer()

   Lớp :class:`Sniffer` được dùng để suy ra định dạng của tệp CSV.

   Lớp :class:`Sniffer` cung cấp hai phương thức:

   .. method:: sniff(sample, delimiters=None)

      Phân tích *mẫu* đã cho và trả về một :class:`Dialect` subclass phản ánh các tham số được tìm thấy. Nếu cung cấp tham số *delimiters* tùy chọn, tham số này được hiểu là một chuỗi chứa các ký tự phân cách hợp lệ có thể có.

      Nếu có nhiều ký tự phân cách phù hợp với mẫu ở mức như nhau --- chẳng hạn nếu cả ``','`` và ``';'`` đều phân tách nhất quán mọi hàng --- thì các ký tự phân cách được liệt kê trong thuộc tính :attr:`~Sniffer.preferred` sẽ được ưu tiên theo thứ tự đó, bất kể mỗi ký tự xuất hiện bao nhiêu lần.

   .. method:: has_header(sample)

      Phân tích văn bản mẫu (được giả định ở định dạng CSV) và trả về
      :const:`True` nếu hàng đầu tiên có vẻ là một loạt tiêu đề cột. Khi kiểm tra từng cột, hai tiêu chí chính sau đây sẽ được xem xét để ước tính xem mẫu có chứa tiêu đề hay không:

      - các hàng từ hàng thứ hai đến hàng thứ n chứa các giá trị số
      - các hàng từ hàng thứ hai đến hàng thứ n chứa các chuỗi trong đó độ dài của ít nhất một giá trị khác với độ dài của tiêu đề giả định của cột đó.

      Hai mươi mốt hàng sau tiêu đề được lấy mẫu; nếu hơn một nửa số cột + hàng đáp ứng các tiêu chí, :const:`True` sẽ được trả về.

   .. note::

      Phương pháp này là một heuristic sơ bộ và có thể tạo ra cả kết quả dương tính giả lẫn âm tính giả.

   Lớp :class:`Sniffer` có thuộc tính sau:

   .. attribute:: preferred

      Danh sách các dấu phân cách được ưu tiên để phân xử khi hòa, theo thứ tự ưu tiên. Danh sách này có thể được sửa đổi. Giá trị ban đầu là ``[',', '\t', ';', ' ', ':']``.

Ví dụ sử dụng :class:`Sniffer`::

   with open('example.csv', newline='') as csvfile:
       dialect = csv.Sniffer().sniff(csvfile.read(1024))
       csvfile.seek(0)
       reader = csv.reader(csvfile, dialect)
       # ... xử lý nội dung tệp CSV tại đây ...


.. _csv-constants:

Module :mod:`!csv` định nghĩa các hằng số sau:

.. data:: QUOTE_ALL

   Yêu cầu các đối tượng :class:`writer` đặt tất cả các trường trong dấu ngoặc kép.


.. data:: QUOTE_MINIMAL

   Hướng dẫn các đối tượng :class:`writer` chỉ đặt trong dấu ngoặc kép những trường chứa các ký tự đặc biệt như *delimiter*, *quotechar*, ``'\r'``, ``'\n'`` hoặc bất kỳ ký tự nào trong *lineterminator*. Nếu *doublequote* là :const:`False` và *escapechar* được thiết lập, *quotechar* sẽ được escape thay vì khiến trường được đặt trong dấu ngoặc kép.


.. data:: QUOTE_NONNUMERIC

   Hướng dẫn các đối tượng :class:`writer` đặt tất cả các trường không phải số trong dấu ngoặc kép.

   Hướng dẫn các đối tượng :class:`reader` chuyển đổi tất cả các trường không được đặt trong dấu ngoặc kép sang kiểu :class:`float`.

   .. note::
      Một số kiểu số, chẳng hạn như :class:`bool`, :class:`~fractions.Fraction` hoặc :class:`~enum.IntEnum`, có biểu diễn chuỗi không thể chuyển đổi sang :class:`float`. Chúng không thể được đọc ở chế độ :data:`QUOTE_NONNUMERIC` và
      :data:`QUOTE_STRINGS`.

.. data:: QUOTE_NONE

   Hướng dẫn các đối tượng :class:`writer` không bao giờ đặt các trường trong dấu ngoặc kép. Khi *delimiter*, *quotechar*, *escapechar*, ``'\r'``, ``'\n'`` hiện tại hoặc bất kỳ ký tự nào trong *lineterminator* xuất hiện trong dữ liệu đầu ra, ký tự đó sẽ được đặt trước bằng ký tự *escapechar* hiện tại. Nếu *escapechar* chưa được thiết lập, writer sẽ raise :exc:`Error` nếu gặp bất kỳ ký tự nào cần escape. Đặt *quotechar* thành ``None`` để ngăn việc escape ký tự này.

   Hướng dẫn các đối tượng :class:`reader` không thực hiện xử lý đặc biệt nào đối với các ký tự đặt trong dấu ngoặc kép.

.. data:: QUOTE_NOTNULL

   Chỉ thị cho các đối tượng :class:`writer` đặt dấu ngoặc kép quanh mọi trường không phải là ``None``. Điều này tương tự :data:`QUOTE_ALL`, ngoại trừ việc nếu giá trị trường là ``None`` thì một chuỗi rỗng (không đặt trong dấu ngoặc kép) sẽ được ghi.

   Chỉ thị cho các đối tượng :class:`reader` diễn giải một trường rỗng (không đặt trong dấu ngoặc kép) là ``None`` và trong các trường hợp khác sẽ hoạt động như :data:`QUOTE_ALL`.

   .. versionadded:: 3.12

.. data:: QUOTE_STRINGS

   Chỉ thị cho các đối tượng :class:`writer` luôn đặt dấu ngoặc kép quanh các trường là chuỗi. Điều này tương tự :data:`QUOTE_NONNUMERIC`, ngoại trừ việc nếu giá trị trường là ``None`` thì một chuỗi rỗng (không đặt trong dấu ngoặc kép) sẽ được ghi.

   Chỉ thị cho các đối tượng :class:`reader` diễn giải một chuỗi rỗng (không đặt trong dấu ngoặc kép) là ``None`` và trong các trường hợp khác sẽ hoạt động như :data:`QUOTE_NONNUMERIC`.

   .. versionadded:: 3.12

Mô-đun :mod:`!csv` định nghĩa ngoại lệ sau:


.. exception:: Error

   Được phát sinh bởi bất kỳ hàm nào khi phát hiện lỗi.

.. _csv-fmt-params:

Dialect và tham số định dạng
----------------------------

Để việc chỉ định định dạng của các bản ghi đầu vào và đầu ra trở nên dễ dàng hơn, các tham số định dạng cụ thể được nhóm lại thành các dialect. Một dialect là lớp con của lớp :class:`Dialect`, chứa nhiều thuộc tính mô tả định dạng của tệp CSV. Khi tạo :class:`reader` hoặc
các đối tượng :class:`writer`, lập trình viên có thể chỉ định một chuỗi hoặc một lớp con của lớp :class:`Dialect` làm tham số dialect. Ngoài hoặc thay cho tham số *dialect*, lập trình viên cũng có thể chỉ định từng tham số định dạng riêng lẻ, với tên giống tên các thuộc tính được định nghĩa dưới đây cho lớp :class:`Dialect`.

Dialects hỗ trợ các thuộc tính sau:


.. attribute:: Dialect.delimiter

   Một chuỗi gồm một ký tự dùng để phân tách các trường. Giá trị mặc định là ``','``.


.. attribute:: Dialect.doublequote

   Kiểm soát cách các thể hiện của *quotechar* xuất hiện bên trong một trường được đặt trong dấu ngoặc kép. Khi :const:`True`, ký tự này được nhân đôi. Khi
   :const:`False`, *escapechar* được dùng làm tiền tố cho *quotechar*. Giá trị mặc định là :const:`True`.

   Khi xuất, nếu *doublequote* là :const:`False` và không đặt *escapechar*,
   :exc:`Error` được phát sinh nếu tìm thấy *quotechar* trong một trường.


.. attribute:: Dialect.escapechar

   Một chuỗi gồm một ký tự được writer sử dụng để escape các ký tự cần được escape:

      * *delimiter*, *quotechar*, ``'\r'``, ``'\n'`` và mọi ký tự trong *lineterminator* đều được escape nếu *quoting* được đặt thành
        :const:`QUOTE_NONE`;
      * *quotechar* được escape nếu *doublequote* là :const:`False`;
      * chính *escapechar*.

   Khi đọc, *escapechar* loại bỏ ý nghĩa đặc biệt của ký tự tiếp theo. Giá trị mặc định là :const:`None`, tức là tắt việc escape.

   .. versionchanged:: 3.10
      Trước đây, chính *escapechar* không được escape, khiến nó bị mất khi đọc.

   .. versionchanged:: 3.11
      Không được phép sử dụng *escapechar* rỗng.

.. attribute:: Dialect.lineterminator

   Chuỗi được dùng để kết thúc các dòng do :class:`writer` tạo ra. Giá trị mặc định là ``'\r\n'``.

   .. note::

      :class:`reader` được lập trình cố định để nhận dạng ``'\r'`` hoặc ``'\n'`` là ký hiệu cuối dòng, đồng thời bỏ qua *lineterminator*. Hành vi này có thể thay đổi trong tương lai.


.. attribute:: Dialect.quotechar

   Chuỗi gồm một ký tự được dùng để đặt trong dấu trích dẫn các trường chứa ký tự đặc biệt, chẳng hạn như *delimiter* hoặc *quotechar*, hay chứa ký tự xuống dòng (``'\r'``, ``'\n'`` hoặc bất kỳ ký tự nào trong *lineterminator*). Giá trị mặc định là ``'"'``. Có thể đặt thành ``None`` để ngăn việc escape ``'"'`` nếu *quoting* được đặt thành :const:`QUOTE_NONE`.

   .. versionchanged:: 3.11
      Không được phép sử dụng *quotechar* rỗng.

.. attribute:: Dialect.quoting

   Kiểm soát thời điểm writer tạo dấu trích dẫn và reader nhận dạng chúng. Có thể nhận bất kỳ hằng số nào trong :ref:`QUOTE_\* constants <csv-constants>` và mặc định là :const:`QUOTE_MINIMAL` nếu *quotechar* không phải là ``None``, còn nếu không thì là :const:`QUOTE_NONE`.


.. attribute:: Dialect.skipinitialspace

   Khi là :const:`True`, các khoảng trắng ngay sau *delimiter* sẽ bị bỏ qua. Giá trị mặc định là :const:`False`. Khi kết hợp ``delimiter=' '`` với ``skipinitialspace=True``, không cho phép các trường rỗng không đặt trong dấu trích dẫn.


.. attribute:: Dialect.strict

   Khi ``True``, hãy raise exception :exc:`Error` nếu dữ liệu đầu vào CSV không hợp lệ. Giá trị mặc định là ``False``.

.. _reader-objects:

Đối tượng Reader
----------------

Các đối tượng Reader (các instance của :class:`DictReader` và các đối tượng được hàm
:func:`reader` trả về) có các phương thức public sau:

.. method:: csvreader.__next__()

   Trả về hàng tiếp theo của đối tượng iterable của reader dưới dạng list (nếu đối tượng được trả về từ :func:`reader`) hoặc dict (nếu đó là một instance của :class:`DictReader`), được phân tích theo :class:`Dialect` hiện tại. Thông thường, bạn nên gọi phương thức này như sau: ``next(reader)``.


Các đối tượng Reader có những thuộc tính public sau:

.. attribute:: csvreader.dialect

   Mô tả chỉ đọc về dialect mà parser đang sử dụng.


.. attribute:: csvreader.line_num

   Số dòng được đọc từ source iterator. Con số này không giống với số bản ghi được trả về, vì bản ghi có thể trải dài trên nhiều dòng.


Các đối tượng DictReader có thuộc tính công khai sau:

.. attribute:: DictReader.fieldnames

   Nếu không được truyền dưới dạng tham số khi tạo đối tượng, thuộc tính này sẽ được khởi tạo trong lần truy cập đầu tiên hoặc khi bản ghi đầu tiên được đọc từ tệp.



Các đối tượng Writer
--------------------

Các đối tượng :class:`writer` (:class:`DictWriter` instance và các đối tượng được hàm :func:`writer` trả về) có các phương thức công khai sau. *row* phải là một iterable gồm các chuỗi hoặc số đối với các đối tượng :class:`writer`, và một dictionary ánh xạ fieldname với chuỗi hoặc số (bằng cách truyền chúng qua :func:`str` trước) đối với các đối tượng :class:`DictWriter`. Lưu ý rằng các số phức được ghi ra với dấu ngoặc đơn bao quanh. Điều này có thể gây ra một số vấn đề cho các chương trình khác đọc tệp CSV (nếu chúng hỗ trợ số phức).


.. method:: csvwriter.writerow(row, /)

   Ghi tham số *row* vào file object của writer, được định dạng theo :class:`Dialect` hiện tại. Trả về giá trị trả về của lệnh gọi đến phương thức *write* của file object bên dưới.

   .. versionchanged:: 3.5
      Đã bổ sung hỗ trợ cho các iterable tùy ý.

.. method:: csvwriter.writerows(rows, /)

   Ghi tất cả phần tử trong *rows* (một iterable gồm các đối tượng *row* như đã mô tả ở trên) vào đối tượng tệp của writer, được định dạng theo dialect hiện tại.

Các đối tượng writer có thuộc tính public sau:


.. attribute:: csvwriter.dialect

   Mô tả chỉ đọc về dialect mà writer đang sử dụng.


Các đối tượng DictWriter có phương thức public sau:


.. method:: DictWriter.writeheader()

   Ghi một hàng chứa các tên trường (như được chỉ định trong constructor) vào đối tượng tệp của writer, được định dạng theo dialect hiện tại. Trả về giá trị trả về của lệnh gọi :meth:`csvwriter.writerow` được sử dụng nội bộ.

   .. versionadded:: 3.2
   .. versionchanged:: 3.8
      :meth:`writeheader` now also returns the value returned by
      phương thức :meth:`csvwriter.writerow` mà nó sử dụng nội bộ.


.. _csv-examples:

Ví dụ
-----

Ví dụ đơn giản nhất về cách đọc tệp CSV::

   import csv
   with open('some.csv', newline='') as f:
       reader = csv.reader(f)
       for row in reader:
           print(row)

Đọc một tệp có định dạng thay thế::

   import csv
   with open('passwd', newline='') as f:
       reader = csv.reader(f, delimiter=':', quoting=csv.QUOTE_NONE)
       for row in reader:
           print(row)

Ví dụ ghi tương ứng đơn giản nhất có thể là::

   import csv
   with open('some.csv', 'w', newline='') as f:
       writer = csv.writer(f)
       writer.writerows(someiterable)

Vì :func:`open` được dùng để mở tệp CSV để đọc, theo mặc định, tệp sẽ được giải mã thành unicode bằng encoding mặc định của hệ thống (xem :func:`locale.getencoding`).  Để giải mã tệp bằng encoding khác, hãy sử dụng đối số ``encoding`` của open::

   import csv
   with open('some.csv', newline='', encoding='utf-8') as f:
       reader = csv.reader(f)
       for row in reader:
           print(row)

Điều tương tự cũng áp dụng khi ghi bằng encoding khác với encoding mặc định của hệ thống: hãy chỉ định đối số encoding khi mở tệp đầu ra.

Đăng ký một dialect mới::

   import csv
   csv.register_dialect('unixpwd', delimiter=':', quoting=csv.QUOTE_NONE)
   with open('passwd', newline='') as f:
       reader = csv.reader(f, 'unixpwd')

Cách sử dụng reader nâng cao hơn một chút --- bắt và báo cáo lỗi::

   import csv, sys
   filename = 'some.csv'
   with open(filename, newline='') as f:
       reader = csv.reader(f)
       try:
           for row in reader:
               print(row)
       except csv.Error as e:
           sys.exit(f'file {filename}, line {reader.line_num}: {e}')

Và mặc dù module này không hỗ trợ trực tiếp việc phân tích cú pháp chuỗi, bạn vẫn có thể dễ dàng thực hiện việc đó::

   import csv
   for row in csv.reader(['one,two,three']):
       print(row)


.. rubric:: Chú thích cuối trang

.. [1] Nếu không chỉ định ``newline=''``, các ký tự xuống dòng nằm trong các trường được đặt trong dấu ngoặc kép sẽ không được diễn giải chính xác, và trên các nền tảng sử dụng ``\r\n`` làm ký tự kết thúc dòng khi ghi, một ``\r`` bổ sung sẽ được thêm vào. Luôn an toàn khi chỉ định ``newline=''``, vì module csv tự xử lý việc xuống dòng (:term:`universal <universal newlines>`).
