:mod:`!fileinput` --- Lặp qua các dòng từ nhiều luồng đầu vào
=============================================================

.. module:: fileinput
   :synopsis: Lặp qua đầu vào chuẩn hoặc một danh sách tệp.

.. moduleauthor:: Guido van Rossum <guido@python.org>
.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>

**Mã nguồn:** :source:`Lib/fileinput.py`

--------------

Mô-đun này triển khai một lớp trợ giúp và các hàm để nhanh chóng viết vòng lặp qua đầu vào chuẩn hoặc một danh sách tệp. Nếu bạn chỉ muốn đọc hoặc ghi một tệp, hãy xem :func:`open`.

Cách sử dụng điển hình là::

   import fileinput
   for line in fileinput.input(encoding="utf-8"):
       process(line)

Lệnh này lặp qua các dòng của tất cả các tệp được liệt kê trong ``sys.argv[1:]``, mặc định là ``sys.stdin`` nếu danh sách trống. Nếu tên tệp là ``'-'``, tên đó cũng được thay thế bằng ``sys.stdin`` và các đối số tùy chọn *mode* và *openhook* sẽ bị bỏ qua. Để chỉ định một danh sách tên tệp thay thế, hãy truyền danh sách đó làm đối số đầu tiên cho :func:`.input`. Cũng có thể sử dụng một tên tệp duy nhất.

Theo mặc định, tất cả các tệp được mở ở chế độ văn bản, nhưng bạn có thể ghi đè điều này bằng cách chỉ định tham số *mode* trong lệnh gọi đến :func:`.input` hoặc
:class:`FileInput`. Nếu xảy ra lỗi I/O trong khi mở hoặc đọc tệp,
:exc:`OSError` sẽ được phát sinh.

.. versionchanged:: 3.3
   :exc:`IOError` used to be raised; it is now an alias of :exc:`OSError`.

Nếu ``sys.stdin`` được sử dụng nhiều hơn một lần, lần sử dụng thứ hai và các lần tiếp theo sẽ không trả về dòng nào, ngoại trừ khi sử dụng tương tác hoặc khi nó đã được đặt lại một cách rõ ràng (ví dụ: bằng cách sử dụng ``sys.stdin.seek(0)``).

Các tệp rỗng được mở rồi đóng ngay lập tức; sự hiện diện của chúng trong danh sách tên tệp hầu như chỉ có thể nhận thấy khi tệp cuối cùng được mở là tệp rỗng.

Các dòng được trả về với mọi ký tự xuống dòng còn nguyên, nghĩa là dòng cuối cùng trong một tệp có thể không có ký tự xuống dòng.

Bạn có thể kiểm soát cách mở tệp bằng cách cung cấp một opening hook thông qua tham số *openhook* cho :func:`fileinput.input` hoặc :func:`FileInput`. Hook này phải là một hàm nhận hai đối số, *filename* và *mode*, đồng thời trả về một đối tượng tương tự tệp đã được mở tương ứng. Nếu *encoding* và/hoặc *errors* được chỉ định, chúng sẽ được truyền cho hook dưới dạng các đối số từ khóa bổ sung. Mô-đun này cung cấp một :func:`hook_compressed` để hỗ trợ các tệp nén.

Hàm sau đây là giao diện chính của mô-đun này:


.. function:: input(files=None, inplace=False, backup='', *, mode='r', openhook=None, encoding=None, errors=None)

   Tạo một instance của lớp :class:`FileInput`. Instance này sẽ được dùng làm trạng thái toàn cục cho các hàm của module này, đồng thời cũng được trả về để sử dụng trong quá trình lặp. Các tham số truyền vào hàm này sẽ được chuyển tiếp đến hàm khởi tạo của lớp :class:`FileInput`.

   Có thể sử dụng instance :class:`FileInput` làm context manager trong câu lệnh
   :keyword:`with`. Trong ví dụ này, *input* được đóng sau khi
   thoát khỏi câu lệnh :keyword:`!with`, ngay cả khi xảy ra ngoại lệ::

      with fileinput.input(files=('spam.txt', 'eggs.txt'), encoding="utf-8") as f:
          for line in f:
              process(line)

   .. versionchanged:: 3.2
      Có thể sử dụng làm context manager.

   .. versionchanged:: 3.8
      Các tham số từ khóa *mode* và *openhook* hiện chỉ có thể được truyền dưới dạng từ khóa.

   .. versionchanged:: 3.10
      Đã thêm các tham số chỉ dùng dưới dạng từ khóa *encoding* và *errors*.


Các hàm sau đây sử dụng trạng thái toàn cục được tạo bởi :func:`fileinput.input`; nếu không có trạng thái nào đang hoạt động, :exc:`RuntimeError` sẽ được phát sinh.


.. function:: filename()

   Trả về tên của tệp hiện đang được đọc. Trước khi dòng đầu tiên được đọc, trả về ``None``.


.. function:: fileno()

   Trả về số nguyên "file descriptor" của tệp hiện tại. Khi không có tệp nào được mở (trước dòng đầu tiên và giữa các tệp), trả về ``-1``.


.. function:: lineno()

   Trả về số dòng tích lũy của dòng vừa được đọc. Trước khi dòng đầu tiên được đọc, trả về ``0``. Sau khi dòng cuối cùng của tệp cuối cùng được đọc, trả về số dòng của dòng đó.


.. function:: filelineno()

   Trả về số dòng trong tệp hiện tại. Trước khi dòng đầu tiên được đọc, trả về ``0``. Sau khi dòng cuối cùng của tệp cuối cùng được đọc, trả về số dòng của dòng đó trong tệp.


.. function:: isfirstline()

   Trả về ``True`` nếu dòng vừa đọc là dòng đầu tiên của tệp đó, nếu không thì trả về ``False``.


.. function:: isstdin()

   Trả về ``True`` nếu dòng cuối cùng được đọc từ ``sys.stdin``, nếu không thì trả về ``False``.


.. function:: nextfile()

   Đóng tệp hiện tại để lần lặp tiếp theo đọc dòng đầu tiên từ tệp tiếp theo (nếu có); các dòng chưa được đọc từ tệp sẽ không được tính vào tổng số dòng. Tên tệp chỉ được thay đổi sau khi dòng đầu tiên của tệp tiếp theo đã được đọc. Trước khi dòng đầu tiên được đọc, hàm này không có tác dụng; không thể dùng hàm này để bỏ qua tệp đầu tiên. Sau khi dòng cuối cùng của tệp cuối cùng đã được đọc, hàm này không có tác dụng.


.. function:: close()

   Đóng chuỗi.

Lớp triển khai hành vi chuỗi do module cung cấp cũng có thể được phân lớp:


.. class:: FileInput(files=None, inplace=False, backup='', *, mode='r', openhook=None, encoding=None, errors=None)

   Lớp :class:`FileInput` là phần triển khai; các phương thức của lớp là :meth:`filename`,
   :meth:`fileno`, :meth:`lineno`, :meth:`filelineno`, :meth:`isfirstline`,
   :meth:`isstdin`, :meth:`nextfile` và :meth:`close` tương ứng với các hàm cùng tên trong module. Ngoài ra, lớp này còn là :term:`iterable` và có một phương thức :meth:`~io.TextIOBase.readline` trả về dòng đầu vào tiếp theo. Chuỗi phải được truy cập theo đúng thứ tự tuần tự; không thể kết hợp truy cập ngẫu nhiên với :meth:`~io.TextIOBase.readline`.

   Với *mode*, bạn có thể chỉ định chế độ tệp sẽ được truyền cho :func:`open`. Giá trị này phải là một trong ``'r'`` và ``'rb'``.

   Khi được cung cấp, *openhook* phải là một hàm nhận hai đối số, *filename* và *mode*, rồi trả về một đối tượng tương tự tệp đã được mở tương ứng. Bạn không thể sử dụng *inplace* cùng với *openhook*.

   Bạn có thể chỉ định *encoding* và *errors*, được truyền vào :func:`open` hoặc *openhook*.

   Một thực thể :class:`FileInput` có thể được sử dụng như một context manager trong
   :keyword:`with`. Trong ví dụ này, *input* được đóng sau khi
   thoát khỏi câu lệnh :keyword:`!with`, ngay cả khi xảy ra ngoại lệ::

      with FileInput(files=('spam.txt', 'eggs.txt')) as input:
          process(input)

   .. versionchanged:: 3.2
      Có thể sử dụng làm context manager.

   .. versionchanged:: 3.8
      Các tham số từ khóa *mode* và *openhook* hiện chỉ có thể được truyền dưới dạng tham số từ khóa.

   .. versionchanged:: 3.10
      Đã thêm các tham số chỉ dùng dưới dạng từ khóa *encoding* và *errors*.

   .. versionchanged:: 3.11
      Các chế độ ``'rU'`` và ``'U'``, cùng với phương thức :meth:`!__getitem__`, đã bị loại bỏ.


**Bộ lọc tại chỗ tùy chọn:** nếu đối số từ khóa ``inplace=True`` được truyền cho :func:`fileinput.input` hoặc hàm khởi tạo :class:`FileInput`, tệp sẽ được chuyển thành tệp sao lưu và đầu ra tiêu chuẩn được chuyển hướng đến tệp đầu vào (nếu đã tồn tại tệp có cùng tên với tệp sao lưu, tệp đó sẽ bị thay thế một cách im lặng).  Điều này cho phép viết một bộ lọc để ghi lại tệp đầu vào ngay tại chỗ.  Nếu tham số *backup* được cung cấp (thường là ``backup='.<some extension>'``), tham số này chỉ định phần mở rộng cho tệp sao lưu và tệp sao lưu sẽ được giữ lại; theo mặc định, phần mở rộng là ``'.bak'`` và tệp sẽ bị xóa khi tệp đầu ra được đóng.  Bộ lọc tại chỗ bị vô hiệu hóa khi đọc đầu vào tiêu chuẩn.


Mô-đun này cung cấp hai hook mở sau đây:

.. function:: hook_compressed(filename, mode, *, encoding=None, errors=None)

   Tự động mở các tệp được nén bằng gzip và bzip2 (được nhận diện qua các phần mở rộng ``'.gz'`` và ``'.bz2'``) bằng các mô-đun :mod:`gzip` và :mod:`bz2`.  Nếu phần mở rộng tên tệp không phải là ``'.gz'`` hoặc ``'.bz2'``, tệp sẽ được mở bình thường (tức là sử dụng :func:`open` mà không giải nén).

   Các giá trị *encoding* và *errors* được truyền cho :class:`io.TextIOWrapper` đối với các tệp nén và cho open đối với các tệp thông thường.

   Ví dụ sử dụng:  ``fi = fileinput.FileInput(openhook=fileinput.hook_compressed, encoding="utf-8")``

   .. versionchanged:: 3.10
      Đã thêm các tham số chỉ dùng dưới dạng từ khóa *encoding* và *errors*.


.. function:: hook_encoded(encoding, errors=None)

   Trả về một hook mở từng tệp bằng :func:`open`, sử dụng *encoding* và *errors* đã cho để đọc tệp.

   Ví dụ sử dụng: ``fi = fileinput.FileInput(openhook=fileinput.hook_encoded("utf-8", "surrogateescape"))``

   .. versionchanged:: 3.6
      Đã bổ sung tham số *errors* tùy chọn.

   .. deprecated:: 3.10
      Hàm này đã lỗi thời kể từ :func:`fileinput.input` và :class:`FileInput` hiện đã có các tham số *mã hóa* và *lỗi*.
