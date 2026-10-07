.. _bltin-exceptions:

Các ngoại lệ tích hợp sẵn
=========================

.. index::
   pair: statement; try
   pair: statement; except

Trong Python, tất cả ngoại lệ phải là các thể hiện của một lớp kế thừa từ
:class:`BaseException`. Trong một câu lệnh :keyword:`try` có mệnh đề :keyword:`except` đề cập đến một lớp cụ thể, mệnh đề đó cũng xử lý mọi lớp ngoại lệ kế thừa từ lớp đó (nhưng không xử lý các lớp ngoại lệ mà *it* được kế thừa từ đó). Hai lớp ngoại lệ không có quan hệ thông qua tính kế thừa thì không bao giờ tương đương, ngay cả khi chúng có cùng tên.

.. index:: pair: statement; raise

Các ngoại lệ tích hợp sẵn được liệt kê trong chương này có thể được trình thông dịch hoặc các hàm tích hợp sẵn tạo ra. Trừ khi được đề cập, chúng có một "giá trị đi kèm" cho biết nguyên nhân chi tiết của lỗi. Giá trị này có thể là một chuỗi hoặc một tuple gồm nhiều phần thông tin (ví dụ: mã lỗi và một chuỗi giải thích mã đó). Giá trị đi kèm thường được truyền dưới dạng đối số cho hàm khởi tạo của lớp ngoại lệ.

Mã do người dùng viết có thể raise các ngoại lệ tích hợp sẵn. Điều này có thể được dùng để kiểm thử một exception handler hoặc báo cáo một tình trạng lỗi "giống như" tình huống trình thông dịch raise cùng ngoại lệ đó; tuy nhiên, hãy lưu ý rằng không có gì ngăn mã do người dùng viết raise một lỗi không phù hợp.

Các lớp ngoại lệ tích hợp sẵn có thể được phân lớp để định nghĩa các ngoại lệ mới; lập trình viên được khuyến khích dẫn xuất các ngoại lệ mới từ lớp :exc:`Exception` hoặc một trong các lớp con của nó, thay vì từ :exc:`BaseException`. Có thêm thông tin về việc định nghĩa ngoại lệ trong Python Tutorial, dưới mục
:ref:`tut-userexceptions`.


Ngữ cảnh ngoại lệ
-----------------

.. index:: pair: exception; chaining
           __cause__ (exception attribute)
           __context__ (exception attribute)
           __suppress_context__ (exception attribute)

Ba thuộc tính trên các đối tượng ngoại lệ cung cấp thông tin về ngữ cảnh mà ngoại lệ được phát sinh:

.. attribute:: BaseException.__context__
               BaseException.__cause__
               BaseException.__suppress_context__

   Khi phát sinh một ngoại lệ mới trong lúc một ngoại lệ khác đang được xử lý, thuộc tính của ngoại lệ mới
   :attr:`!__context__` được tự động đặt thành ngoại lệ đang được xử lý. Một ngoại lệ có thể được xử lý khi một :keyword:`except` hoặc
   :keyword:`finally` clause, hoặc một :keyword:`with` statement, được sử dụng.

   Ngữ cảnh ngoại lệ ngầm định này có thể được bổ sung bằng nguyên nhân rõ ràng bằng cách sử dụng :keyword:`!from` với
   :keyword:`raise`::

      raise new_exc from original_exc

   Biểu thức theo sau :keyword:`from<raise>` phải là một ngoại lệ hoặc ``None``. Nó sẽ được đặt làm :attr:`!__cause__` trên ngoại lệ được phát sinh. Việc đặt
   :attr:`!__cause__` cũng ngầm định đặt thuộc tính :attr:`!__suppress_context__` thành ``True``, do đó việc sử dụng ``raise new_exc from None`` thực sự thay thế ngoại lệ cũ bằng ngoại lệ mới cho mục đích hiển thị (ví dụ: chuyển đổi :exc:`KeyError` thành :exc:`AttributeError`), đồng thời vẫn giữ ngoại lệ cũ trong :attr:`!__context__` để kiểm tra nội quan khi gỡ lỗi.

   Mã hiển thị traceback mặc định sẽ hiển thị các exception được liên kết này cùng với traceback của chính exception đó. Một exception được liên kết rõ ràng trong :attr:`!__cause__` luôn được hiển thị nếu có. Một exception được liên kết ngầm trong :attr:`!__context__` chỉ được hiển thị khi :attr:`!__cause__` là :const:`None` và :attr:`!__suppress_context__` là false.

   Trong cả hai trường hợp, chính exception đó luôn được hiển thị sau mọi exception được liên kết, để dòng cuối cùng của traceback luôn hiển thị exception cuối cùng đã được raise.


Kế thừa từ các exception tích hợp sẵn
-------------------------------------

Mã người dùng có thể tạo các lớp con kế thừa từ một kiểu exception. Bạn chỉ nên kế thừa một kiểu exception tại một thời điểm để tránh mọi xung đột có thể xảy ra giữa cách các lớp cơ sở xử lý thuộc tính ``args``, cũng như do khả năng không tương thích về bố cục bộ nhớ.

.. impl-detail::

   Hầu hết các exception tích hợp sẵn được triển khai bằng C để đạt hiệu suất cao, xem:
   :source:`Objects/exceptions.c`. Một số exception có bố cục bộ nhớ tùy chỉnh, khiến không thể tạo một lớp con kế thừa từ nhiều kiểu exception. Bố cục bộ nhớ của một kiểu là chi tiết triển khai và có thể thay đổi giữa các phiên bản Python, dẫn đến những xung đột mới trong tương lai. Vì vậy, bạn nên tránh hoàn toàn việc kế thừa nhiều kiểu exception.


Các lớp cơ sở
-------------

Các ngoại lệ sau đây chủ yếu được dùng làm lớp cơ sở cho các ngoại lệ khác.

.. exception:: BaseException

   Lớp cơ sở cho tất cả các ngoại lệ tích hợp sẵn. Lớp này không предназначено để được kế thừa trực tiếp bởi các lớp do người dùng định nghĩa (để làm việc đó, hãy sử dụng :exc:`Exception`). Nếu
   :func:`str` được gọi trên một thực thể của lớp này, biểu diễn của (các) đối số của thực thể sẽ được trả về, hoặc chuỗi rỗng nếu không có đối số nào.

   .. attribute:: args

      Tuple chứa các đối số được truyền cho hàm khởi tạo ngoại lệ. Một số ngoại lệ tích hợp sẵn (chẳng hạn như :exc:`OSError`) yêu cầu một số lượng đối số nhất định và gán ý nghĩa đặc biệt cho các phần tử của tuple này, trong khi những ngoại lệ khác thường chỉ được gọi với một chuỗi duy nhất chứa thông báo lỗi.

   .. method:: with_traceback(tb)

      Phương thức này đặt *tb* làm traceback mới cho ngoại lệ và trả về đối tượng ngoại lệ. Phương thức này thường được sử dụng hơn trước khi các tính năng chaining ngoại lệ của :pep:`3134` khả dụng. Ví dụ sau cho thấy cách chuyển đổi một thực thể của ``SomeException`` thành một thực thể của ``OtherException`` trong khi vẫn giữ nguyên traceback. Khi được raise, frame hiện tại được thêm vào traceback của ``OtherException``, tương tự như cách traceback của ``SomeException`` ban đầu sẽ được xử lý nếu chúng ta để nó truyền đến caller.::

         try:
             ...
         except SomeException:
             tb = sys.exception().__traceback__
             raise OtherException(...).with_traceback(tb)

   .. attribute:: __traceback__

      Một trường có thể ghi, chứa
      :ref:`traceback object <traceback-objects>` được liên kết với ngoại lệ này. Xem thêm: :ref:`raise`.

   .. method:: add_note(note)

      Thêm chuỗi ``note`` vào phần ghi chú của ngoại lệ; các ghi chú này xuất hiện trong traceback tiêu chuẩn sau chuỗi ngoại lệ. Một :exc:`TypeError` sẽ được phát sinh nếu ``note`` không phải là chuỗi.

      .. versionadded:: 3.11

   .. attribute:: __notes__

      Danh sách các ghi chú của ngoại lệ này, được thêm bằng :meth:`add_note`. Thuộc tính này được tạo khi :meth:`add_note` được gọi.

      .. versionadded:: 3.11


.. exception:: Exception

   Tất cả các ngoại lệ tích hợp không thoát khỏi hệ thống đều kế thừa từ lớp này. Tất cả các ngoại lệ do người dùng định nghĩa cũng nên kế thừa từ lớp này.


.. exception:: ArithmeticError

   Lớp cơ sở cho các ngoại lệ tích hợp được phát sinh khi xảy ra nhiều lỗi số học khác nhau: :exc:`OverflowError`, :exc:`ZeroDivisionError`,
   :exc:`FloatingPointError`.


.. exception:: BufferError

   Được phát sinh khi không thể thực hiện thao tác liên quan đến :ref:`buffer <bufferobjects>`.


.. exception:: LookupError

   Lớp cơ sở cho các ngoại lệ được phát sinh khi khóa hoặc chỉ mục được sử dụng trên mapping hoặc sequence không hợp lệ: :exc:`IndexError`, :exc:`KeyError`. Ngoại lệ này có thể được phát sinh trực tiếp bởi :func:`codecs.lookup`.


Các ngoại lệ cụ thể
-------------------

Các ngoại lệ sau đây là những ngoại lệ thường được phát sinh.

.. exception:: AssertionError

   .. index:: pair: statement; assert

   Được phát sinh khi một câu lệnh :keyword:`assert` không thành công.


.. exception:: AttributeError

   Được phát sinh khi việc tham chiếu thuộc tính (xem :ref:`attribute-references`) hoặc phép gán không thành công.  (Khi một đối tượng hoàn toàn không hỗ trợ việc tham chiếu hoặc gán thuộc tính, :exc:`TypeError` sẽ được phát sinh.)

   Các đối số chỉ dành cho từ khóa tùy chọn *name* và *obj* thiết lập các thuộc tính tương ứng:

   .. attribute:: name

      Tên của thuộc tính đã được cố gắng truy cập.

   .. attribute:: obj

      Đối tượng được truy cập để lấy thuộc tính có tên đó.

   .. versionchanged:: 3.10
      Đã thêm các thuộc tính :attr:`name` và :attr:`obj`.

.. exception:: EOFError

   Được phát sinh khi hàm :func:`input` gặp điều kiện cuối tệp (EOF) mà chưa đọc dữ liệu nào. (Lưu ý: :meth:`io.TextIOBase.read` và
   các phương thức :meth:`io.IOBase.readline` trả về một chuỗi rỗng khi gặp EOF.)


.. exception:: FloatingPointError

   Hiện không được sử dụng.


.. exception:: GeneratorExit

   Được phát sinh khi một :term:`generator` hoặc :term:`coroutine` bị đóng; xem :meth:`generator.close` và :meth:`coroutine.close`. Nó kế thừa trực tiếp từ :exc:`BaseException` thay vì :exc:`Exception` vì về mặt kỹ thuật, đây không phải là lỗi.


.. exception:: ImportError

   Được phát sinh khi câu lệnh :keyword:`import` gặp sự cố trong quá trình tải một module. Cũng được phát sinh khi "danh sách from" trong ``from ... import`` chứa một tên không thể tìm thấy.

   Các đối số chỉ dùng theo từ khóa tùy chọn *name* và *path* thiết lập các thuộc tính tương ứng:

   .. attribute:: name

      Tên của module đã được cố gắng import.

   .. attribute:: path

      Đường dẫn đến bất kỳ tệp nào đã gây ra ngoại lệ.

   .. versionchanged:: 3.3
      Đã thêm các thuộc tính :attr:`name` và :attr:`path`.

.. exception:: ModuleNotFoundError

   Một lớp con của :exc:`ImportError` được :keyword:`import` phát sinh khi không thể định vị mô-đun. Ngoại lệ này cũng được phát sinh khi tìm thấy ``None`` trong :data:`sys.modules`.

   .. versionadded:: 3.6


.. exception:: IndexError

   Được phát sinh khi chỉ mục của một sequence nằm ngoài phạm vi. (Các chỉ mục của slice sẽ được âm thầm cắt ngắn để nằm trong phạm vi cho phép; nếu một chỉ mục không phải là số nguyên, :exc:`TypeError` sẽ được phát sinh.)

   .. XXX xref to sequences


.. exception:: KeyError

   Được phát sinh khi không tìm thấy khóa của mapping (dictionary) trong tập hợp các khóa hiện có.

   .. XXX xref to mapping objects?


.. exception:: KeyboardInterrupt

   Được phát sinh khi người dùng nhấn phím ngắt (thông thường là :kbd:`Control-C` hoặc
   :kbd:`Delete`). Trong quá trình thực thi, việc kiểm tra ngắt được thực hiện thường xuyên. Ngoại lệ này kế thừa từ :exc:`BaseException` để không vô tình bị bắt bởi mã bắt :exc:`Exception`, từ đó ngăn trình thông dịch thoát.

   .. note::

      Việc bắt :exc:`KeyboardInterrupt` cần được cân nhắc đặc biệt. Vì nó có thể được phát sinh tại những thời điểm không thể dự đoán, trong một số trường hợp, nó có thể khiến chương trình đang chạy rơi vào trạng thái không nhất quán. Nhìn chung, tốt nhất là để :exc:`KeyboardInterrupt` kết thúc chương trình nhanh nhất có thể hoặc hoàn toàn tránh phát sinh nó. (Xem
      :ref:`handlers-and-exceptions`.)


.. exception:: MemoryError

   Được phát sinh khi một thao tác hết bộ nhớ nhưng tình huống này vẫn có thể được xử lý (bằng cách xóa một số đối tượng). Giá trị đi kèm là một chuỗi cho biết loại thao tác (nội bộ) nào đã hết bộ nhớ. Lưu ý rằng do kiến trúc quản lý bộ nhớ bên dưới (hàm :c:func:`malloc` của C), trình thông dịch có thể không phải lúc nào cũng khôi phục hoàn toàn được từ tình huống này; tuy vậy, nó vẫn phát sinh một ngoại lệ để có thể in stack traceback, phòng trường hợp nguyên nhân là một chương trình chạy mất kiểm soát.


.. exception:: NameError

   Được phát sinh khi không tìm thấy tên cục bộ hoặc tên toàn cục. Điều này chỉ áp dụng cho các tên không đủ điều kiện. Giá trị đi kèm là một thông báo lỗi có chứa tên không thể tìm thấy.

   Đối số chỉ có từ khóa *name* tùy chọn đặt thuộc tính:

   .. attribute:: name

      Tên của biến đã được cố gắng truy cập.

   .. versionchanged:: 3.10
      Đã thêm thuộc tính :attr:`name`.


.. exception:: NotImplementedError

   Ngoại lệ này kế thừa từ :exc:`RuntimeError`. Trong các lớp cơ sở do người dùng định nghĩa, các phương thức abstract nên phát sinh ngoại lệ này khi yêu cầu các lớp dẫn xuất ghi đè phương thức, hoặc trong quá trình phát triển lớp để cho biết rằng vẫn cần bổ sung phần triển khai thực sự.

   .. note::

      Không nên sử dụng nó để chỉ ra rằng một operator hoặc method hoàn toàn không được hỗ trợ -- trong trường hợp đó, hãy để operator / method chưa được định nghĩa hoặc, nếu là subclass, đặt nó thành :data:`None`.

   .. caution::

      :exc:`!NotImplementedError` và :data:`!NotImplemented` không thể thay thế cho nhau. Chỉ nên sử dụng exception này như mô tả ở trên; xem :data:`NotImplemented` để biết chi tiết về cách sử dụng đúng hằng số tích hợp sẵn.


.. exception:: OSError([arg])
               OSError(errno, strerror[, filename[, winerror[, filename2]]])

   .. index:: pair: module; errno

   Exception này được raised khi một hàm hệ thống trả về lỗi liên quan đến hệ thống, bao gồm các lỗi I/O như "không tìm thấy tệp" hoặc "đĩa đầy" (không áp dụng cho các kiểu đối số không hợp lệ hoặc những lỗi phát sinh ngẫu nhiên khác).

   Dạng thứ hai của constructor đặt các thuộc tính tương ứng, được mô tả bên dưới. Các thuộc tính mặc định là :const:`None` nếu không được chỉ định. Để tương thích ngược, nếu truyền ba đối số, thuộc tính :attr:`~BaseException.args` chỉ chứa một 2-tuple gồm hai đối số đầu tiên của constructor.

   Constructor thường thực sự trả về một subclass của :exc:`OSError`, như mô tả trong `ngoại lệ OS <OS exceptions_>`_ bên dưới. Subclass cụ thể phụ thuộc vào giá trị :attr:`.errno` cuối cùng. Hành vi này chỉ xảy ra khi khởi tạo trực tiếp :exc:`OSError` hoặc thông qua alias, và không được kế thừa khi tạo subclass.

   .. attribute:: errno

      Mã lỗi dạng số từ biến C :c:data:`errno`.

   .. attribute:: winerror

      Trên Windows, điều này cung cấp cho bạn mã lỗi Windows gốc. Sau đó, thuộc tính :attr:`.errno` là bản dịch gần đúng, theo các thuật ngữ POSIX, của mã lỗi gốc đó.

      Trên Windows, nếu đối số *winerror* của hàm khởi tạo là một số nguyên, thuộc tính :attr:`.errno` được xác định từ mã lỗi Windows và đối số *errno* bị bỏ qua. Trên các nền tảng khác, đối số *winerror* bị bỏ qua và thuộc tính :attr:`winerror` không tồn tại.

   .. attribute:: strerror

      Thông báo lỗi tương ứng do hệ điều hành cung cấp. Thông báo này được định dạng bởi các hàm C :c:func:`!perror` trên POSIX và :c:func:`!FormatMessage` trên Windows.

   .. attribute:: filename
                  filename2

      Đối với các ngoại lệ liên quan đến đường dẫn hệ thống tệp (chẳng hạn như :func:`open` hoặc
      :func:`os.unlink`), :attr:`filename` là tên tệp được truyền vào hàm. Đối với các hàm liên quan đến hai đường dẫn hệ thống tệp (chẳng hạn như
      :func:`os.rename`), :attr:`filename2` tương ứng với tên tệp thứ hai được truyền vào hàm.


   .. versionchanged:: 3.3
      :exc:`EnvironmentError`, :exc:`IOError`, :exc:`WindowsError`,
      :exc:`socket.error`, :exc:`select.error` and
      :exc:`!mmap.error` have been merged into :exc:`OSError`, and the
      hàm khởi tạo có thể trả về một lớp con.

   .. versionchanged:: 3.4
      Thuộc tính :attr:`filename` hiện là tên tệp gốc được truyền vào hàm, thay vì tên được mã hóa thành hoặc giải mã từ
      :term:`filesystem encoding and error handler`. Ngoài ra, đối số và thuộc tính *filename2* của hàm khởi tạo đã được thêm vào.


.. exception:: OverflowError

   Được phát sinh khi kết quả của một phép toán số học quá lớn để có thể biểu diễn. Điều này không thể xảy ra với số nguyên (vì trong trường hợp đó sẽ phát sinh
   :exc:`MemoryError` thay vì bỏ cuộc). Tuy nhiên, vì lý do lịch sử, OverflowError đôi khi được phát sinh đối với các số nguyên nằm ngoài phạm vi bắt buộc. Do C thiếu tiêu chuẩn hóa về cách xử lý ngoại lệ số thực, hầu hết các phép toán số thực không được kiểm tra.


.. exception:: PythonFinalizationError

   Ngoại lệ này kế thừa từ :exc:`RuntimeError`. Ngoại lệ này được phát sinh khi một thao tác bị chặn trong quá trình trình thông dịch tắt, còn được gọi là
   :term:`quá trình hoàn tất Python <interpreter shutdown>`.

   Các ví dụ về những thao tác có thể bị chặn bằng một
   :exc:`PythonFinalizationError` trong quá trình Python kết thúc:

   * Tạo một thread Python mới.
   * :meth:`Joining <threading.Thread.join>` một daemon thread đang chạy.
   * :func:`os.fork`.

   Xem thêm hàm :func:`sys.is_finalizing`.

   .. versionadded:: 3.13
      Trước đây, một :exc:`RuntimeError` thông thường sẽ được raised.

   .. versionchanged:: 3.14

      :meth:`threading.Thread.join` hiện có thể raise exception này.

.. exception:: RecursionError

   Ngoại lệ này được kế thừa từ :exc:`RuntimeError`. Ngoại lệ này được phát sinh khi trình thông dịch phát hiện độ sâu đệ quy tối đa (xem
   :func:`sys.getrecursionlimit`) bị vượt quá.

   .. versionadded:: 3.5
      Trước đây, một :exc:`RuntimeError` thông thường sẽ được raised.


.. exception:: ReferenceError

   Ngoại lệ này được phát sinh khi một proxy tham chiếu yếu, được tạo bởi hàm
   :func:`weakref.proxy`, được dùng để truy cập một thuộc tính của đối tượng được tham chiếu sau khi đối tượng đó đã được thu gom rác. Để biết thêm thông tin về các tham chiếu yếu, hãy xem module :mod:`weakref`.


.. exception:: RuntimeError

   Được phát sinh khi phát hiện một lỗi không thuộc bất kỳ danh mục nào khác. Giá trị đi kèm là một chuỗi cho biết chính xác điều gì đã xảy ra.


.. exception:: StopIteration

   Được phát sinh bởi hàm dựng sẵn :func:`next` và các :term:`iterator`\'s
   phương thức :meth:`~iterator.__next__` để báo hiệu rằng iterator không còn tạo ra phần tử nào nữa.

   .. attribute:: StopIteration.value

      Đối tượng exception có một thuộc tính duy nhất là :attr:`!value`, được cung cấp dưới dạng đối số khi khởi tạo exception và mặc định là :const:`None`.

   Khi một hàm :term:`generator` hoặc :term:`coroutine` kết thúc, một instance :exc:`StopIteration` mới được raise và giá trị mà hàm trả về được dùng làm
   tham số :attr:`value` cho hàm khởi tạo của exception.

   Nếu mã generator trực tiếp hoặc gián tiếp raise :exc:`StopIteration`, nó sẽ được chuyển đổi thành :exc:`RuntimeError` (giữ lại
   :exc:`StopIteration` làm nguyên nhân của exception mới).

   .. versionchanged:: 3.3
      Đã thêm thuộc tính ``value`` và khả năng để các hàm generator sử dụng thuộc tính này nhằm trả về một giá trị.

   .. versionchanged:: 3.5
      Giới thiệu việc chuyển đổi RuntimeError thông qua ``from __future__ import generator_stop``, xem :pep:`479`.

   .. versionchanged:: 3.7
      Mặc định bật :pep:`479` cho toàn bộ mã: lỗi :exc:`StopIteration` được phát sinh trong generator sẽ được chuyển đổi thành :exc:`RuntimeError`.

.. exception:: StopAsyncIteration

   Phải được phát sinh bởi phương thức :meth:`~object.__anext__` của một
   đối tượng :term:`asynchronous iterator` để dừng quá trình lặp.

   .. versionadded:: 3.5

.. exception:: SyntaxError(message, details)

   Được phát sinh khi parser gặp lỗi cú pháp. Điều này có thể xảy ra trong một
   câu lệnh :keyword:`import`, trong lần gọi các hàm tích hợp sẵn
   :func:`compile`, :func:`exec` hoặc :func:`eval`, hoặc khi đọc script ban đầu hay đầu vào tiêu chuẩn (cũng trong chế độ tương tác).

   :func:`str` của đối tượng ngoại lệ chỉ trả về thông báo lỗi. Details là một tuple, các thành phần của tuple cũng có sẵn dưới dạng các thuộc tính riêng biệt.

   .. attribute:: filename

      Tên của tệp nơi xảy ra lỗi cú pháp.

   .. attribute:: lineno

      Số dòng trong tệp nơi xảy ra lỗi. Số này được đánh chỉ mục từ 1: dòng đầu tiên trong tệp có ``lineno`` là 1.

   .. attribute:: offset

      Cột trong dòng nơi xảy ra lỗi. Số này được đánh chỉ mục từ 1: ký tự đầu tiên trong dòng có ``offset`` là 1.

   .. attribute:: text

      Đoạn mã nguồn liên quan đến lỗi.

   .. attribute:: end_lineno

      Số dòng trong tệp nơi lỗi kết thúc. Số này được đánh chỉ mục từ 1: dòng đầu tiên trong tệp có ``lineno`` là 1.

   .. attribute:: end_offset

      Cột trong dòng kết thúc nơi lỗi kết thúc. Số này được đánh chỉ mục từ 1: ký tự đầu tiên trong dòng có ``offset`` là 1.

   Đối với các lỗi trong các trường f-string, thông báo được thêm tiền tố "f-string: " và các offset là offset trong văn bản được tạo từ biểu thức thay thế.  Ví dụ, việc biên dịch f'Bad {a b} field' tạo ra thuộc tính args sau: ('f-string: ...', ('', 1, 2, '(a b)\n', 1, 5)).

   .. versionchanged:: 3.10
      Đã thêm các thuộc tính :attr:`end_lineno` và :attr:`end_offset`.

.. exception:: IndentationError

   Lớp cơ sở cho các lỗi cú pháp liên quan đến việc thụt lề không chính xác. Đây là lớp con của :exc:`SyntaxError`.


.. exception:: TabError

   Được phát sinh khi phần thụt lề sử dụng tab và dấu cách không nhất quán. Đây là lớp con của :exc:`IndentationError`.


.. exception:: SystemError

   Được phát sinh khi interpreter phát hiện một lỗi nội bộ, nhưng tình huống chưa nghiêm trọng đến mức khiến nó phải từ bỏ mọi hy vọng. Giá trị đi kèm là một chuỗi cho biết đã xảy ra lỗi gì (theo các thuật ngữ cấp thấp). Trong :term:`CPython`, lỗi này có thể được phát sinh do sử dụng không đúng C API của Python, chẳng hạn như trả về giá trị ``NULL`` mà không thiết lập exception.

   Nếu bạn chắc chắn rằng exception này không phải do mình gây ra hoặc không phải lỗi của package bạn đang sử dụng, bạn nên báo cáo cho tác giả hoặc maintainer của Python interpreter. Hãy nhớ báo cáo phiên bản của Python interpreter (``sys.version``; phiên bản này cũng được in ở đầu một phiên Python tương tác), thông báo lỗi chính xác (giá trị đi kèm của exception) và nếu có thể, mã nguồn của chương trình đã kích hoạt lỗi.


.. exception:: SystemExit

   Exception này được phát sinh bởi hàm :func:`sys.exit`. Nó kế thừa từ
   :exc:`BaseException` thay vì :exc:`Exception` để không vô tình bị bắt bởi mã bắt :exc:`Exception`. Điều này cho phép ngoại lệ được lan truyền đúng cách lên trên và khiến trình thông dịch thoát. Khi không được xử lý, trình thông dịch Python sẽ thoát; không in ra traceback của ngăn xếp. Hàm khởi tạo chấp nhận cùng đối số tùy chọn được truyền cho :func:`sys.exit`. Nếu giá trị là một số nguyên, giá trị đó chỉ định trạng thái thoát của hệ thống (được truyền cho hàm :c:func:`!exit` của C); nếu là ``None``, trạng thái thoát là bằng không; nếu thuộc kiểu khác (chẳng hạn như một chuỗi), giá trị của đối tượng sẽ được in ra và trạng thái thoát là một.

   Lệnh gọi :func:`sys.exit` được chuyển thành một ngoại lệ để các trình xử lý dọn dẹp (các mệnh đề :keyword:`finally` của câu lệnh :keyword:`try`) có thể được thực thi, đồng thời để debugger có thể thực thi một script mà không có nguy cơ mất quyền kiểm soát. Có thể sử dụng hàm :func:`os._exit` nếu nhất thiết phải thoát ngay lập tức (ví dụ: trong tiến trình con sau khi gọi :func:`os.fork`).

   .. attribute:: code

      Trạng thái thoát hoặc thông báo lỗi được truyền cho hàm khởi tạo. (Mặc định là ``None``.)


.. exception:: TypeError

   Được phát sinh khi một thao tác hoặc hàm được áp dụng cho một đối tượng không phù hợp về kiểu. Giá trị đi kèm là một chuỗi mô tả chi tiết về sự không khớp kiểu.

   Ngoại lệ này có thể được mã người dùng phát sinh để cho biết một thao tác được thử trên một đối tượng không được hỗ trợ và không được dự định hỗ trợ. Nếu một đối tượng được dự định hỗ trợ một thao tác nhất định nhưng chưa cung cấp phần triển khai, :exc:`NotImplementedError` là ngoại lệ thích hợp để phát sinh.

   Việc truyền các đối số sai kiểu (ví dụ: truyền một :class:`list` khi một
   :class:`int` được mong đợi) phải dẫn đến :exc:`TypeError`, nhưng việc truyền các đối số có giá trị sai (ví dụ: một số nằm ngoài các giới hạn dự kiến) phải dẫn đến :exc:`ValueError`.

.. exception:: UnboundLocalError

   Được phát sinh khi một tham chiếu đến biến cục bộ trong một hàm hoặc phương thức được tạo ra, nhưng chưa có giá trị nào được liên kết với biến đó. Đây là lớp con của
   :exc:`NameError`.


.. exception:: UnicodeError

   Được phát sinh khi xảy ra lỗi mã hóa hoặc giải mã liên quan đến Unicode. Đây là lớp con của :exc:`ValueError`.

   :exc:`UnicodeError` có các thuộc tính mô tả lỗi mã hóa hoặc giải mã. Ví dụ: ``err.object[err.start:err.end]`` cung cấp đầu vào không hợp lệ cụ thể mà codec gặp lỗi khi xử lý.

   .. attribute:: encoding

       Tên của encoding đã gây ra lỗi.

   .. attribute:: reason

       Một chuỗi mô tả lỗi cụ thể của codec.

   .. attribute:: object

       Đối tượng mà codec đang cố gắng mã hóa hoặc giải mã.

   .. attribute:: start

       Chỉ mục đầu tiên của dữ liệu không hợp lệ trong :attr:`object`.

       Giá trị này không được âm vì được diễn giải là một độ lệch tuyệt đối, nhưng ràng buộc này không được thực thi trong runtime.

   .. attribute:: end

       Chỉ mục sau dữ liệu không hợp lệ cuối cùng trong :attr:`object`.

       Giá trị này không được âm vì được diễn giải là một độ lệch tuyệt đối, nhưng ràng buộc này không được thực thi trong runtime.


.. exception:: UnicodeEncodeError

   Được phát sinh khi xảy ra lỗi liên quan đến Unicode trong quá trình mã hóa. Đây là một lớp con của
   :exc:`UnicodeError`.


.. exception:: UnicodeDecodeError

   Được phát sinh khi xảy ra lỗi liên quan đến Unicode trong quá trình giải mã. Đây là một lớp con của
   :exc:`UnicodeError`.


.. exception:: UnicodeTranslateError

   Được phát sinh khi xảy ra lỗi liên quan đến Unicode trong quá trình chuyển đổi. Đây là một lớp con của :exc:`UnicodeError`.


.. exception:: ValueError

   Được phát sinh khi một thao tác hoặc hàm nhận được một đối số có đúng kiểu nhưng giá trị không phù hợp, và tình huống này không được mô tả bởi một exception cụ thể hơn như :exc:`IndexError`.


.. exception:: ZeroDivisionError

   Được phát sinh khi đối số thứ hai của phép chia hoặc phép modulo bằng không. Giá trị đi kèm là một chuỗi cho biết kiểu của các toán hạng và phép toán.


Các ngoại lệ sau được giữ lại để tương thích với các phiên bản trước; kể từ Python 3.3, chúng là bí danh của :exc:`OSError`.

.. exception:: EnvironmentError

.. exception:: IOError

.. exception:: WindowsError

   Chỉ khả dụng trên Windows.


.. _`OS exceptions`:

Các ngoại lệ của hệ điều hành
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Các ngoại lệ sau là lớp con của :exc:`OSError`, chúng được phát sinh tùy thuộc vào mã lỗi hệ thống.

.. exception:: BlockingIOError

   Được phát sinh khi một thao tác sẽ bị chặn trên một đối tượng (ví dụ: socket) được đặt ở chế độ không chặn. Tương ứng với :c:data:`errno` :py:const:`~errno.EAGAIN`, :py:const:`~errno.EALREADY`,
   :py:const:`~errno.EWOULDBLOCK` và :py:const:`~errno.EINPROGRESS`.

   Ngoài các thuộc tính của :exc:`OSError`, :exc:`BlockingIOError` có thể có thêm một thuộc tính:

   .. attribute:: characters_written

      Một số nguyên chứa số **byte** được ghi vào stream trước khi stream bị chặn. Thuộc tính này khả dụng khi sử dụng các lớp I/O có bộ đệm trong mô-đun :mod:`io`.

.. exception:: ChildProcessError

   Được phát sinh khi một thao tác trên tiến trình con không thành công. Tương ứng với :c:data:`errno` :py:const:`~errno.ECHILD`.

.. exception:: ConnectionError

   Lớp cơ sở cho các sự cố liên quan đến kết nối.

   Các lớp con là :exc:`BrokenPipeError`, :exc:`ConnectionAbortedError`,
   :exc:`ConnectionRefusedError` và :exc:`ConnectionResetError`.

.. exception:: BrokenPipeError

   Một lớp con của :exc:`ConnectionError`, được phát sinh khi cố gắng ghi vào một pipe trong khi đầu kia đã bị đóng, hoặc cố gắng ghi vào một socket đã bị shutdown để ghi. Tương ứng với :c:data:`errno` :py:const:`~errno.EPIPE` và :py:const:`~errno.ESHUTDOWN`.

.. exception:: ConnectionAbortedError

   Một lớp con của :exc:`ConnectionError`, được phát sinh khi bên kia hủy bỏ nỗ lực kết nối. Tương ứng với :c:data:`errno` :py:const:`~errno.ECONNABORTED`.

.. exception:: ConnectionRefusedError

   Một lớp con của :exc:`ConnectionError`, được phát sinh khi bên kia từ chối nỗ lực kết nối. Tương ứng với :c:data:`errno` :py:const:`~errno.ECONNREFUSED`.

.. exception:: ConnectionResetError

   Một lớp con của :exc:`ConnectionError`, được phát sinh khi kết nối bị bên kia đặt lại. Tương ứng với :c:data:`errno` :py:const:`~errno.ECONNRESET`.

.. exception:: FileExistsError

   Được phát sinh khi cố gắng tạo một tệp hoặc thư mục đã tồn tại. Tương ứng với :c:data:`errno` :py:const:`~errno.EEXIST`.

.. exception:: FileNotFoundError

   Được phát sinh khi yêu cầu một tệp hoặc thư mục nhưng tệp hoặc thư mục đó không tồn tại. Tương ứng với :c:data:`errno` :py:const:`~errno.ENOENT`.

.. exception:: InterruptedError

   Được phát sinh khi một system call bị gián đoạn bởi tín hiệu đến. Tương ứng với :c:data:`errno` :py:const:`~errno.EINTR`.

   .. versionchanged:: 3.5
      Python hiện tự động thử lại các system call khi một syscall bị gián đoạn bởi tín hiệu, trừ khi trình xử lý tín hiệu phát sinh một exception (xem :pep:`475` để biết lý do), thay vì phát sinh :exc:`InterruptedError`.

.. exception:: IsADirectoryError

   Được phát sinh khi yêu cầu thao tác tệp (chẳng hạn :func:`os.remove`) trên một thư mục. Tương ứng với :c:data:`errno` :py:const:`~errno.EISDIR`.

.. exception:: NotADirectoryError

   Được phát sinh khi yêu cầu thao tác thư mục (chẳng hạn :func:`os.listdir`) trên một đối tượng không phải là thư mục. Trên hầu hết các nền tảng POSIX, lỗi này cũng có thể được phát sinh nếu một thao tác cố mở hoặc duyệt qua một tệp không phải thư mục như thể đó là một thư mục. Tương ứng với :c:data:`errno` :py:const:`~errno.ENOTDIR`.

.. exception:: PermissionError

   Được phát sinh khi cố gắng thực hiện một thao tác mà không có quyền truy cập cần thiết - chẳng hạn như quyền trên hệ thống tệp. Tương ứng với :c:data:`errno` :py:const:`~errno.EACCES`,
   :py:const:`~errno.EPERM`, và :py:const:`~errno.ENOTCAPABLE`.

   .. versionchanged:: 3.11.1
      :py:const:`~errno.ENOTCAPABLE` của WASI hiện được ánh xạ tới
      :exc:`PermissionError`.

.. exception:: ProcessLookupError

   Được phát sinh khi một tiến trình nhất định không tồn tại. Tương ứng với :c:data:`errno` :py:const:`~errno.ESRCH`.

.. exception:: TimeoutError

   Được phát sinh khi một hàm hệ thống hết thời gian chờ ở cấp hệ thống. Tương ứng với :c:data:`errno` :py:const:`~errno.ETIMEDOUT`.

.. versionadded:: 3.3
   Tất cả các lớp con :exc:`OSError` nêu trên đã được thêm vào.


.. seealso::

   :pep:`3151` - Tái cấu trúc hệ thống phân cấp ngoại lệ OS và IO


.. _warning-categories-as-exceptions:

Cảnh báo
--------

Các ngoại lệ sau đây được dùng làm danh mục cảnh báo; xem tài liệu
:ref:`warning-categories` để biết thêm chi tiết.

.. exception:: Warning

   Lớp cơ sở cho các danh mục cảnh báo.


.. exception:: UserWarning

   Lớp cơ sở cho các cảnh báo do mã người dùng tạo ra.


.. exception:: DeprecationWarning

   Lớp cơ sở cho các cảnh báo về những tính năng đã lỗi thời khi các cảnh báo đó hướng đến những nhà phát triển Python khác.

   Bị các bộ lọc cảnh báo mặc định bỏ qua, ngoại trừ trong mô-đun ``__main__`` (:pep:`565`). Bật :ref:`Python Development Mode <devmode>` sẽ hiển thị cảnh báo này.

   Chính sách ngừng sử dụng được mô tả trong :pep:`387`.


.. exception:: PendingDeprecationWarning

   Lớp cơ sở cho các cảnh báo về những tính năng đã lỗi thời và được dự kiến sẽ bị ngừng sử dụng trong tương lai, nhưng hiện tại chưa bị ngừng sử dụng.

   Lớp này hiếm khi được sử dụng vì việc phát ra cảnh báo về khả năng một tính năng sắp bị ngừng sử dụng là không phổ biến, và :exc:`DeprecationWarning` được ưu tiên cho những tính năng đã chính thức bị ngừng sử dụng.

   Bị các bộ lọc cảnh báo mặc định bỏ qua. Bật :ref:`Python Development Mode <devmode>` sẽ hiển thị cảnh báo này.

   Chính sách ngừng sử dụng được mô tả trong :pep:`387`.


.. exception:: SyntaxWarning

   Lớp cơ sở cho các cảnh báo về cú pháp đáng ngờ.

   Cảnh báo này thường được phát ra khi biên dịch mã nguồn Python và thường sẽ không được báo cáo khi chạy mã đã biên dịch.


.. exception:: RuntimeWarning

   Lớp cơ sở cho các cảnh báo về hành vi đáng ngờ trong runtime.


.. exception:: FutureWarning

   Lớp cơ sở cho các cảnh báo về các tính năng đã lỗi thời khi những cảnh báo đó dành cho người dùng cuối của các ứng dụng được viết bằng Python.


.. exception:: ImportWarning

   Lớp cơ sở cho các cảnh báo về những lỗi có thể xảy ra khi import module.

   Bị các bộ lọc cảnh báo mặc định bỏ qua. Bật :ref:`Python Development Mode <devmode>` sẽ hiển thị cảnh báo này.


.. exception:: UnicodeWarning

   Lớp cơ sở cho các cảnh báo liên quan đến Unicode.


.. exception:: EncodingWarning

   Lớp cơ sở cho các cảnh báo liên quan đến encoding.

   Xem :ref:`io-encoding-warning` để biết chi tiết.

   .. versionadded:: 3.10


.. exception:: BytesWarning

   Lớp cơ sở cho các cảnh báo liên quan đến :class:`bytes` và :class:`bytearray`.


.. exception:: ResourceWarning

   Lớp cơ sở cho các cảnh báo liên quan đến việc sử dụng tài nguyên.

   Bị các bộ lọc cảnh báo mặc định bỏ qua. Bật :ref:`Python Development Mode <devmode>` sẽ hiển thị cảnh báo này.

   .. versionadded:: 3.2


.. _lib-exception-groups:

Các nhóm ngoại lệ
-----------------

Các thành phần sau được sử dụng khi cần phát sinh nhiều ngoại lệ không liên quan. Chúng thuộc hệ thống phân cấp ngoại lệ nên có thể được xử lý bằng :keyword:`except` như mọi ngoại lệ khác. Ngoài ra, chúng được :keyword:`except*<except_star>` nhận diện; từ khóa này đối sánh các nhóm con của chúng dựa trên kiểu của những ngoại lệ được chứa bên trong.

.. exception:: ExceptionGroup(msg, excs)
.. exception:: BaseExceptionGroup(msg, excs)

   Cả hai kiểu ngoại lệ này đều bao bọc các ngoại lệ trong sequence ``excs``. Tham số ``msg`` phải là một chuỗi. Điểm khác biệt giữa hai lớp là :exc:`BaseExceptionGroup` kế thừa :exc:`BaseException` và có thể bao bọc bất kỳ ngoại lệ nào, trong khi :exc:`ExceptionGroup` kế thừa :exc:`Exception` và chỉ có thể bao bọc các lớp con của :exc:`Exception`. Thiết kế này nhằm để ``except Exception`` bắt được một :exc:`ExceptionGroup` nhưng không bắt được
   :exc:`BaseExceptionGroup`.

   Hàm khởi tạo :exc:`BaseExceptionGroup` trả về một :exc:`ExceptionGroup` thay vì một :exc:`BaseExceptionGroup` nếu tất cả các ngoại lệ chứa trong đó đều là
   các instance :exc:`Exception`, nhờ đó có thể tự động thực hiện việc lựa chọn. Ngược lại, hàm khởi tạo :exc:`ExceptionGroup` sẽ phát sinh một :exc:`TypeError` nếu bất kỳ ngoại lệ nào chứa trong đó không phải là một
   lớp con của :exc:`Exception`.

   Các nhóm ngoại lệ là :ref:`generic <generics>` theo kiểu của các ngoại lệ chứa trong chúng.

   .. impl-detail::

      Tham số ``excs`` có thể là bất kỳ sequence nào, nhưng list và tuple được xử lý hiệu quả hơn trong trường hợp này. Để đạt hiệu suất tối ưu, hãy truyền một tuple làm ``excs``.

   .. attribute:: message

       Đối số ``msg`` của hàm khởi tạo. Đây là một thuộc tính chỉ đọc.

   .. attribute:: exceptions

       Một tuple chứa các exception trong chuỗi ``excs`` được truyền cho hàm khởi tạo. Đây là thuộc tính chỉ đọc.

   .. method:: subgroup(condition)

      Trả về một exception group chỉ chứa các exception từ group hiện tại khớp với *condition*, hoặc ``None`` nếu kết quả rỗng.

      Điều kiện có thể là một kiểu exception hoặc tuple các kiểu exception; trong trường hợp đó, mỗi exception được kiểm tra xem có khớp hay không bằng cùng một phép kiểm tra được sử dụng trong mệnh đề ``except``. Điều kiện cũng có thể là một callable (không phải là đối tượng kiểu) nhận một exception làm đối số duy nhất và trả về true cho những exception nên nằm trong subgroup.

      Cấu trúc lồng nhau của exception hiện tại được giữ nguyên trong kết quả, cũng như các giá trị của :attr:`message`,
      :attr:`~BaseException.__traceback__`, :attr:`~BaseException.__cause__`,
      :attr:`~BaseException.__context__` và
      :attr:`~BaseException.__notes__` fields. Các group lồng nhau rỗng sẽ bị loại khỏi kết quả.

      Điều kiện được kiểm tra đối với mọi exception trong exception group lồng nhau, bao gồm group cấp cao nhất và mọi exception group lồng nhau. Nếu điều kiện đúng đối với một exception group như vậy, toàn bộ group đó sẽ được đưa vào kết quả.

      .. versionadded:: 3.13
         ``condition`` có thể là bất kỳ callable nào không phải là một đối tượng kiểu.

   .. method:: split(condition)

      Tương tự như :meth:`subgroup`, nhưng trả về cặp ``(match, rest)``, trong đó ``match`` là ``subgroup(condition)`` còn ``rest`` là phần còn lại không khớp.

   .. method:: derive(excs)

      Trả về một exception group có cùng :attr:`message`, nhưng bọc các exception trong ``excs``.

      Phương thức này được :meth:`subgroup` và :meth:`split` sử dụng; chúng được dùng trong nhiều ngữ cảnh để chia nhỏ một exception group. Một lớp con cần ghi đè phương thức này để :meth:`subgroup` và :meth:`split` trả về các instance của lớp con thay vì :exc:`ExceptionGroup`.

      :meth:`subgroup` và :meth:`split` sao chép phần
      :attr:`~BaseException.__traceback__`,
      :attr:`~BaseException.__cause__`, :attr:`~BaseException.__context__` và
      các trường :attr:`~BaseException.__notes__` từ exception group ban đầu sang exception group do :meth:`derive` trả về, vì vậy các trường này không cần được :meth:`derive` cập nhật.

      .. doctest::

         >>> class MyGroup(ExceptionGroup):
         ...     def derive(self, excs):
         ...         return MyGroup(self.message, excs)
         ...
         >>> e = MyGroup("eg", [ValueError(1), TypeError(2)])
         >>> e.add_note("a note")
         >>> e.__context__ = Exception("context")
         >>> e.__cause__ = Exception("cause")
         >>> try:
         ...    raise e
         ... except Exception as e:
         ...    exc = e
         ...
         >>> match, rest = exc.split(ValueError)
         >>> exc, exc.__context__, exc.__cause__, exc.__notes__
         (MyGroup('eg', [ValueError(1), TypeError(2)]), Exception('context'), Exception('cause'), ['a note'])
         >>> match, match.__context__, match.__cause__, match.__notes__
         (MyGroup('eg', [ValueError(1)]), Exception('context'), Exception('cause'), ['a note'])
         >>> rest, rest.__context__, rest.__cause__, rest.__notes__
         (MyGroup('eg', [TypeError(2)]), Exception('context'), Exception('cause'), ['a note'])
         >>> exc.__traceback__ is match.__traceback__ is rest.__traceback__
         True


   Lưu ý rằng :exc:`BaseExceptionGroup` định nghĩa :meth:`~object.__new__`, vì vậy các lớp con cần chữ ký hàm khởi tạo khác phải ghi đè phương thức đó thay vì :meth:`~object.__init__`. Ví dụ sau định nghĩa một lớp con của nhóm ngoại lệ, lớp này chấp nhận một exit_code và tạo thông báo của nhóm từ giá trị đó.::

      class Errors(ExceptionGroup):
         def __new__(cls, errors, exit_code):
            self = super().__new__(Errors, f"exit code: {exit_code}", errors)
            self.exit_code = exit_code
            return self

         def derive(self, excs):
            return Errors(excs, self.exit_code)

   Giống như :exc:`ExceptionGroup`, mọi lớp con của :exc:`BaseExceptionGroup` đồng thời cũng là lớp con của :exc:`Exception` chỉ có thể bao bọc các thực thể của
   :exc:`Exception`.

   .. versionadded:: 3.11


Cây phân cấp ngoại lệ
---------------------

Cây phân cấp lớp cho các ngoại lệ tích hợp là:

.. literalinclude:: ../../Lib/test/exception_hierarchy.txt
  :language: text
