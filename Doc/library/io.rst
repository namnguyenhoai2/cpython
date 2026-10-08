:mod:`!io` --- Công cụ cốt lõi để làm việc với stream
=====================================================

.. module:: io
   :synopsis: Công cụ cốt lõi để làm việc với stream.

.. moduleauthor:: Guido van Rossum <guido@python.org>
.. moduleauthor:: Mike Verdone <mike.verdone@gmail.com>
.. moduleauthor:: Mark Russell <mark.russell@zen.co.uk>
.. moduleauthor:: Antoine Pitrou <solipsis@pitrou.net>
.. moduleauthor:: Amaury Forgeot d'Arc <amauryfa@gmail.com>
.. moduleauthor:: Benjamin Peterson <benjamin@python.org>
.. sectionauthor:: Benjamin Peterson <benjamin@python.org>

**Mã nguồn:** :source:`Lib/io.py`

--------------

.. _io-overview:

Tổng quan
---------

.. index::
   single: file object; io module

Mô-đun :mod:`!io` cung cấp các phương tiện chính của Python để xử lý nhiều loại I/O. Có ba loại I/O chính: *I/O văn bản*, *I/O nhị phân* và *I/O thô*. Đây là các danh mục tổng quát và mỗi danh mục có thể sử dụng nhiều loại kho lưu trữ phía sau khác nhau. Một đối tượng cụ thể thuộc bất kỳ danh mục nào trong số này được gọi là :term:`file object`. Các thuật ngữ phổ biến khác là *stream* và *đối tượng giống tệp*.

Bất kể thuộc danh mục nào, mỗi đối tượng stream cụ thể cũng sẽ có nhiều khả năng khác nhau: có thể chỉ đọc, chỉ ghi hoặc vừa đọc vừa ghi. Đối tượng cũng có thể cho phép truy cập ngẫu nhiên tùy ý (tìm kiếm tiến hoặc lùi đến bất kỳ vị trí nào), hoặc chỉ cho phép truy cập tuần tự (ví dụ trong trường hợp socket hoặc pipe).

Tất cả stream đều xử lý cẩn thận kiểu dữ liệu mà bạn cung cấp cho chúng. Ví dụ, truyền một đối tượng :class:`str` cho phương thức :meth:`!write` của một stream nhị phân sẽ gây ra :exc:`TypeError`. Việc truyền một đối tượng :class:`bytes` cho
Phương thức :meth:`!write` của một luồng văn bản.

.. versionchanged:: 3.3
   Các thao tác trước đây gây ra :exc:`IOError` giờ đây gây ra :exc:`OSError`, vì
   :exc:`IOError` hiện là bí danh của :exc:`OSError`.

.. _text-io:

I/O văn bản
^^^^^^^^^^^

I/O văn bản tiếp nhận và tạo ra các đối tượng :class:`str`. Điều này có nghĩa là khi bộ lưu trữ nền vốn được tạo thành từ các byte (chẳng hạn như trong trường hợp tệp), dữ liệu sẽ được mã hóa và giải mã một cách minh bạch, đồng thời việc chuyển đổi tùy chọn các ký tự dòng mới dành riêng cho từng nền tảng cũng được thực hiện.

Cách dễ nhất để tạo một luồng văn bản là sử dụng :meth:`open`, với việc chỉ định encoding nếu muốn::

   f = open("myfile.txt", "r", encoding="utf-8")

Các luồng văn bản trong bộ nhớ cũng có sẵn dưới dạng các đối tượng :class:`StringIO`::

   f = io.StringIO("some initial text data")

.. note::

   Khi làm việc với một stream không chặn, hãy lưu ý rằng các thao tác đọc trên các đối tượng I/O văn bản có thể phát sinh :exc:`BlockingIOError` nếu stream không thể thực hiện thao tác ngay lập tức.

API stream văn bản được mô tả chi tiết trong tài liệu của
:class:`TextIOBase`.

.. _binary-io:

I/O nhị phân
^^^^^^^^^^^^

I/O nhị phân (còn được gọi là *buffered I/O*) yêu cầu
:term:`bytes-like objects <bytes-like object>` và tạo ra các đối tượng :class:`bytes`. Không thực hiện mã hóa, giải mã hoặc chuyển đổi ký tự xuống dòng. Có thể sử dụng loại stream này cho mọi loại dữ liệu không phải văn bản, cũng như khi cần kiểm soát thủ công cách xử lý dữ liệu văn bản.

Cách dễ nhất để tạo một stream nhị phân là sử dụng :meth:`open` với ``'b'`` trong chuỗi mode::

   f = open("myfile.jpg", "rb")

Các stream nhị phân trong bộ nhớ cũng có sẵn dưới dạng các đối tượng :class:`BytesIO`::

   f = io.BytesIO(b"some initial binary data: \x00\x01")

API binary stream được mô tả chi tiết trong tài liệu về
:class:`BufferedIOBase`.

Các module thư viện khác có thể cung cấp thêm cách tạo text stream hoặc binary stream. Xem :meth:`socket.socket.makefile` để biết ví dụ.


Raw I/O
^^^^^^^

Raw I/O (còn gọi là *unbuffered I/O*) thường được dùng làm khối xây dựng cấp thấp cho binary stream và text stream; hiếm khi mã người dùng cần trực tiếp thao tác với raw stream. Tuy vậy, bạn có thể tạo raw stream bằng cách mở một tệp ở chế độ binary với buffering bị tắt::

   f = open("myfile.jpg", "rb", buffering=0)

API raw stream được mô tả chi tiết trong tài liệu về :class:`RawIOBase`.

.. warning::
   Raw I/O là một giao diện cấp thấp và các method thường phải được kiểm tra giá trị trả về cũng như retry một cách tường minh để đảm bảo thao tác hoàn tất. Ví dụ, :meth:`~RawIOBase.write` trả về số byte đã ghi, có thể ít hơn số byte được cung cấp (ghi một phần). Các đối tượng I/O cấp cao như :ref:`binary-io` và :ref:`text-io` triển khai hành vi retry.

.. _io-text-encoding:

Mã hóa văn bản
--------------

Mã hóa mặc định của :class:`TextIOWrapper` và :func:`open` phụ thuộc vào locale (:func:`locale.getencoding`).

Tuy nhiên, nhiều developer quên chỉ định encoding khi mở các tệp văn bản được mã hóa bằng UTF-8 (ví dụ: JSON, TOML, Markdown, v.v.) vì hầu hết nền tảng Unix mặc định sử dụng locale UTF-8. Điều này gây ra lỗi vì encoding của locale không phải là UTF-8 đối với hầu hết người dùng Windows. Ví dụ::

   # Có thể không hoạt động trên Windows khi tệp chứa các ký tự không phải ASCII.
   with open("README.md") as f:
       long_description = f.read()

Do đó, bạn nên chỉ định rõ encoding khi mở các tệp văn bản. Nếu muốn sử dụng UTF-8, hãy truyền ``encoding="utf-8"``. Để sử dụng encoding của locale hiện tại, ``encoding="locale"`` được hỗ trợ kể từ Python 3.10.

.. seealso::

   :ref:`utf8-mode`
      Python UTF-8 Mode có thể được sử dụng để thay đổi encoding mặc định từ encoding phụ thuộc vào locale thành UTF-8.

   :pep:`686`
      Python 3.15 sẽ đặt :ref:`utf8-mode` làm mặc định.

.. _io-encoding-warning:

Bật tùy chọn EncodingWarning
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. versionadded:: 3.10
   Xem :pep:`597` để biết thêm chi tiết.

Để tìm nơi encoding mặc định của locale được sử dụng, bạn có thể bật tùy chọn dòng lệnh :option:`-X warn_default_encoding <-X>` hoặc đặt
biến môi trường :envvar:`PYTHONWARNDEFAULTENCODING`, biến này sẽ phát ra một :exc:`EncodingWarning` khi encoding mặc định được sử dụng.

Nếu bạn cung cấp một API sử dụng :func:`open` hoặc
:class:`TextIOWrapper` và truyền ``encoding=None`` làm tham số, bạn có thể sử dụng :func:`text_encoding` để các bên gọi API phát ra một
:exc:`EncodingWarning` nếu họ không truyền một ``encoding``. Tuy nhiên, hãy cân nhắc sử dụng UTF-8 theo mặc định (tức là ``encoding="utf-8"``) cho các API mới.


Giao diện mô-đun cấp cao
------------------------

.. data:: DEFAULT_BUFFER_SIZE

   Một giá trị int chứa kích thước bộ đệm mặc định được các lớp I/O có bộ đệm của mô-đun sử dụng.  :func:`open` sử dụng blksize của tệp (lấy được bằng
   :func:`os.stat`) nếu có thể.


.. function:: open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)

   Đây là bí danh của hàm builtin :func:`open`.

   .. audit-event:: open path,mode,flags io.open

      Hàm này phát sinh một sự kiện :ref:`auditing event <auditing>` ``open`` với các đối số *path*, *mode* và *flags*. Các đối số *mode* và *flags* có thể đã được sửa đổi hoặc suy ra từ lệnh gọi ban đầu.


.. function:: open_code(path)

   Mở tệp được cung cấp với mode ``'rb'``. Nên sử dụng hàm này khi mục đích là coi nội dung như mã thực thi.

   *path* phải là một :class:`str` và là một đường dẫn tuyệt đối.

   Hành vi của hàm này có thể bị ghi đè bởi một lệnh gọi trước đó đến
   :c:func:`PyFile_SetOpenCodeHook`. Tuy nhiên, với giả định rằng *path* là một
   :class:`str` và là một đường dẫn tuyệt đối, ``open_code(path)`` phải luôn hoạt động giống như ``open(path, 'rb')``. Việc ghi đè hành vi này nhằm thực hiện thêm validation hoặc tiền xử lý tệp.

   .. versionadded:: 3.8


.. function:: text_encoding(encoding, stacklevel=2, /)

   Đây là một hàm trợ giúp dành cho các callable sử dụng :func:`open` hoặc
   :class:`TextIOWrapper` và có tham số ``encoding=None``.

   Hàm này trả về *encoding* nếu nó không phải là ``None``. Nếu không, hàm trả về ``"locale"`` hoặc ``"utf-8"`` tùy thuộc vào
   :ref:`UTF-8 Mode <utf8-mode>`.

   Hàm này phát ra một :class:`EncodingWarning` nếu
   :data:`sys.flags.warn_default_encoding <sys.flags>` là true và *encoding* là ``None``. *stacklevel* xác định nơi cảnh báo được phát ra. Ví dụ::

      def read_text(path, encoding=None):
          encoding = io.text_encoding(encoding)  # stacklevel=2
          with open(path, encoding) as f:
              return f.read()

   Trong ví dụ này, một :class:`EncodingWarning` được phát ra cho caller của ``read_text()``.

   Xem :ref:`io-text-encoding` để biết thêm thông tin.

   .. versionadded:: 3.10

   .. versionchanged:: 3.11
      :func:`text_encoding` returns "utf-8" when UTF-8 mode is enabled and
      *encoding* là ``None``.


.. exception:: BlockingIOError

   Đây là bí danh tương thích cho exception tích hợp sẵn :exc:`BlockingIOError`.


.. exception:: UnsupportedOperation

   Một exception kế thừa :exc:`OSError` và :exc:`ValueError`, được raise khi một thao tác không được hỗ trợ được gọi trên một stream.


.. seealso::

   :mod:`sys`
       chứa các luồng IO tiêu chuẩn: :data:`sys.stdin`, :data:`sys.stdout` và :data:`sys.stderr`.


Phân cấp lớp
------------

Việc triển khai các luồng I/O được tổ chức theo một hệ thống phân cấp các lớp. Trước hết
:term:`các lớp cơ sở trừu tượng <abstract base class>` (ABCs), được dùng để xác định nhiều danh mục luồng khác nhau, sau đó là các lớp cụ thể cung cấp các triển khai luồng tiêu chuẩn.

.. note::

   Các lớp cơ sở trừu tượng cũng cung cấp triển khai mặc định cho một số phương thức nhằm hỗ trợ việc triển khai các lớp luồng cụ thể. Ví dụ: :class:`BufferedIOBase` cung cấp các triển khai chưa được tối ưu hóa cho
   :meth:`!readinto` và :meth:`!readline`.

Ở đỉnh của hệ thống phân cấp I/O là lớp cơ sở trừu tượng :class:`IOBase`. Lớp này định nghĩa giao diện cơ bản cho một luồng. Tuy nhiên, cần lưu ý rằng không có sự phân tách giữa việc đọc và ghi vào luồng; các triển khai được phép phát sinh :exc:`UnsupportedOperation` nếu chúng không hỗ trợ một thao tác nhất định.

ABC :class:`RawIOBase` kế thừa :class:`IOBase`. Nó xử lý việc đọc và ghi byte vào một stream. :class:`FileIO` kế thừa :class:`RawIOBase` để cung cấp interface cho các tệp trong hệ thống tệp của máy.

ABC :class:`BufferedIOBase` kế thừa :class:`IOBase`. Nó xử lý việc buffering trên một raw binary stream (:class:`RawIOBase`). Các subclass của nó là:
:class:`BufferedWriter`, :class:`BufferedReader` và :class:`BufferedRWPair` lần lượt thực hiện buffering cho các raw binary stream có thể ghi, có thể đọc và vừa có thể đọc vừa có thể ghi. :class:`BufferedRandom` cung cấp interface đã buffer cho các stream có thể seek. Một subclass :class:`BufferedIOBase` khác là :class:`BytesIO`, một stream gồm các byte trong bộ nhớ.

ABC :class:`TextIOBase` kế thừa :class:`IOBase`. Nó xử lý các stream có byte biểu diễn văn bản, đồng thời thực hiện encoding và decoding từ và sang string. :class:`TextIOWrapper`, kế thừa :class:`TextIOBase`, là một text interface đã buffer cho một raw stream đã buffer (:class:`BufferedIOBase`). Cuối cùng,
:class:`StringIO` là một stream văn bản trong bộ nhớ.

Tên của các đối số không thuộc đặc tả, và chỉ các đối số của
:func:`open` được dùng làm keyword argument.

Bảng sau đây tóm tắt các ABC được cung cấp bởi module :mod:`!io`:

.. tabularcolumns:: |l|l|L|L|

+-------------------------+-----------------+-------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ABC                     | Kế thừa         | Các phương thức stub                            | Các phương thức và thuộc tính mixin                                                                                                                                                                      |
+=========================+=================+=================================================+==========================================================================================================================================================================================================+
| :class:`IOBase`         |                 | ``fileno``, ``seek`` và ``truncate``            | ``close``, ``closed``, ``__enter__``, ``__exit__``, ``flush``, ``isatty``, ``__iter__``, ``__next__``, ``readable``, ``readline``, ``readlines``, ``seekable``, ``tell``, ``writable`` và ``writelines`` |
+-------------------------+-----------------+-------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :class:`RawIOBase`      | :class:`IOBase` | ``readinto`` và ``write``                       | Các phương thức :class:`IOBase` được kế thừa, ``read`` và ``readall``                                                                                                                                    |
+-------------------------+-----------------+-------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :class:`BufferedIOBase` | :class:`IOBase` | ``detach``, ``read``, ``read1`` và ``write``    | Các phương thức :class:`IOBase` được kế thừa, ``readinto`` và ``readinto1``                                                                                                                              |
+-------------------------+-----------------+-------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| :class:`TextIOBase`     | :class:`IOBase` | ``detach``, ``read``, ``readline`` và ``write`` | Các phương thức :class:`IOBase` được kế thừa, ``encoding``, ``errors`` và ``newlines``                                                                                                                   |
+-------------------------+-----------------+-------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+


Các lớp cơ sở I/O
^^^^^^^^^^^^^^^^^

.. class:: IOBase

   Lớp cơ sở trừu tượng cho tất cả các lớp I/O.

   Lớp này cung cấp các triển khai trừu tượng rỗng cho nhiều phương thức mà các lớp dẫn xuất có thể chọn ghi đè; các triển khai mặc định biểu thị một tệp không thể đọc, ghi hoặc tìm vị trí.

   Mặc dù :class:`IOBase` không khai báo :meth:`!read` hoặc :meth:`!write` vì chữ ký của chúng sẽ khác nhau, các triển khai và client vẫn nên xem những phương thức đó là một phần của interface. Ngoài ra, các triển khai có thể phát sinh :exc:`ValueError` (hoặc :exc:`UnsupportedOperation`) khi các thao tác mà chúng không hỗ trợ được gọi.

   Kiểu cơ bản được dùng cho dữ liệu nhị phân được đọc từ hoặc ghi vào tệp là
   :class:`bytes`. Các :term:`đối tượng kiểu bytes <bytes-like object>` khác cũng được chấp nhận làm đối số phương thức. Các lớp I/O văn bản làm việc với dữ liệu :class:`str`.

   Lưu ý rằng việc gọi bất kỳ phương thức nào (kể cả các phương thức truy vấn) trên một stream đã đóng đều không được xác định. Trong trường hợp này, các triển khai có thể phát sinh :exc:`ValueError`.

   :class:`IOBase` (và các lớp con của nó) hỗ trợ iterator protocol, nghĩa là có thể lặp qua một đối tượng :class:`IOBase` để nhận từng dòng trong stream. Các dòng được định nghĩa hơi khác nhau tùy thuộc vào việc stream là binary stream (trả về bytes) hay text stream (trả về các chuỗi ký tự). Xem :meth:`~IOBase.readline` bên dưới.

   :class:`IOBase` cũng là một context manager và do đó hỗ trợ
   :keyword:`with` câu lệnh. Trong ví dụ này, *file* được đóng sau khi
   suite của câu lệnh :keyword:`!with` hoàn tất---ngay cả khi xảy ra ngoại lệ::

      with open('spam.txt', 'w') as file:
          file.write('Spam and eggs!')

   :class:`IOBase` cung cấp các thuộc tính dữ liệu và phương thức sau:

   .. method:: close()

      Xả và đóng stream này. Phương thức này không có tác dụng nếu tệp đã được đóng. Khi tệp đã đóng, mọi thao tác trên tệp (ví dụ: đọc hoặc ghi) sẽ phát sinh :exc:`ValueError`.

      Để thuận tiện, bạn có thể gọi phương thức này nhiều lần; tuy nhiên, chỉ lần gọi đầu tiên mới có tác dụng.

   .. attribute:: closed

      ``True`` nếu stream đã đóng.

   .. method:: fileno()

      Trả về file descriptor bên dưới (một số nguyên) của stream nếu nó tồn tại. Một :exc:`OSError` sẽ được phát sinh nếu đối tượng IO không sử dụng file descriptor.

   .. method:: flush()

      Flush các write buffer của stream nếu có thể. Thao tác này không làm gì với các stream chỉ đọc và không blocking.

   .. method:: isatty()

      Trả về ``True`` nếu stream là interactive (tức là được kết nối với terminal hoặc thiết bị tty).

   .. method:: readable()

      Trả về ``True`` nếu có thể đọc từ stream. Nếu ``False``, :meth:`!read` sẽ phát sinh :exc:`OSError`.

   .. method:: readline(size=-1, /)

      Đọc và trả về một dòng từ stream. Nếu chỉ định *size*, nhiều nhất *size* byte sẽ được đọc.

      Ký tự kết thúc dòng luôn là ``b'\n'`` đối với các tệp nhị phân; đối với các tệp văn bản, có thể sử dụng đối số *newline* của :func:`open` để chọn (các) ký tự kết thúc dòng được nhận diện.

   .. method:: readlines(hint=-1, /)

      Đọc và trả về một danh sách các dòng từ stream. Có thể chỉ định *hint* để kiểm soát số dòng được đọc: sẽ không đọc thêm dòng nào nếu tổng kích thước (tính bằng byte/ký tự) của tất cả các dòng đã đọc vượt quá *hint*.

      Các giá trị *hint* bằng ``0`` hoặc nhỏ hơn, cũng như ``None``, được xem là không có gợi ý.

      Lưu ý rằng bạn đã có thể lặp qua các đối tượng tệp bằng ``for line in file: ...`` mà không cần gọi :meth:`!file.readlines`.

   .. method:: seek(offset, whence=os.SEEK_SET, /)

      Thay đổi vị trí của stream đến *offset* byte đã cho, được diễn giải tương đối so với vị trí được chỉ báo bởi *whence*, rồi trả về vị trí tuyệt đối mới. Các giá trị của *whence* là:

      * :data:`os.SEEK_SET` hoặc ``0`` -- đầu stream (mặc định); *offset* phải bằng không hoặc là số dương
      * :data:`os.SEEK_CUR` hoặc ``1`` -- vị trí hiện tại của stream; *offset* có thể là số âm
      * :data:`os.SEEK_END` hoặc ``2`` -- cuối stream; *offset* thường là số âm

      .. versionadded:: 3.1
         Các hằng số :data:`!SEEK_*`.

      .. versionadded:: 3.3
         Một số hệ điều hành có thể hỗ trợ các giá trị bổ sung, chẳng hạn như
         :const:`os.SEEK_HOLE` hoặc :const:`os.SEEK_DATA`. Các giá trị hợp lệ cho một tệp có thể phụ thuộc vào việc tệp đó được mở ở chế độ văn bản hay nhị phân.

   .. method:: seekable()

      Trả về ``True`` nếu stream hỗ trợ truy cập ngẫu nhiên. Nếu ``False``,
      :meth:`seek`, :meth:`tell` và :meth:`truncate` sẽ phát sinh :exc:`OSError`.

   .. method:: tell()

      Trả về vị trí hiện tại của stream.

   .. method:: truncate(size=None, /)

      Thay đổi kích thước stream thành *size* đã cho, tính bằng byte (hoặc vị trí hiện tại nếu *size* không được chỉ định). Vị trí hiện tại của stream không thay đổi. Thao tác thay đổi kích thước này có thể mở rộng hoặc thu nhỏ kích thước tệp hiện tại. Khi mở rộng, nội dung của vùng tệp mới phụ thuộc vào nền tảng (trên hầu hết các hệ thống, các byte bổ sung được điền bằng số 0). Kích thước tệp mới được trả về.

      .. versionchanged:: 3.5
         Windows hiện sẽ điền bằng số 0 khi mở rộng tệp.

   .. method:: writable()

      Trả về ``True`` nếu stream hỗ trợ ghi. Nếu ``False``,
      :meth:`!write` và :meth:`truncate` sẽ phát sinh :exc:`OSError`.

   .. method:: writelines(lines, /)

      Ghi một danh sách các dòng vào stream. Không thêm dấu phân cách dòng, vì vậy thông thường mỗi dòng được cung cấp sẽ có dấu phân cách dòng ở cuối.

   .. method:: __del__()

      Chuẩn bị cho việc hủy đối tượng. :class:`IOBase` cung cấp triển khai mặc định cho phương thức này, gọi phương thức
      :meth:`~IOBase.close` của instance.


.. class:: RawIOBase

   Lớp cơ sở cho các raw binary stream. Lớp này kế thừa từ :class:`IOBase`.

   Raw binary stream thường cung cấp quyền truy cập cấp thấp vào thiết bị hoặc API bên dưới của hệ điều hành và không cố gắng đóng gói chúng trong các primitive cấp cao (chức năng này được thực hiện ở cấp cao hơn trong buffered binary stream và text stream, được mô tả ở phần sau của trang này).

   :class:`RawIOBase` cung cấp các phương thức này ngoài các phương thức từ
   :class:`IOBase`:

   .. method:: read(size=-1, /)

      Đọc tối đa *size* byte từ đối tượng và trả về chúng. Để thuận tiện, nếu *size* không được chỉ định hoặc là -1, tất cả các byte cho đến EOF sẽ được trả về.

      Cố gắng chỉ thực hiện một lệnh gọi hệ thống nhưng sẽ thử lại nếu bị gián đoạn và trình xử lý tín hiệu không phát sinh ngoại lệ (xem :pep:`475` để biết lý do). Điều này có nghĩa là có thể trả về ít hơn *size* byte nếu lệnh gọi hệ điều hành trả về ít hơn *size* byte.

      Nếu trả về 0 byte và *size* không phải là 0, điều này cho biết đã đến cuối tệp. Nếu đối tượng ở chế độ non-blocking và không có byte nào khả dụng, ``None`` sẽ được trả về.

      Phần triển khai mặc định chuyển tiếp đến :meth:`readall` và
      :meth:`readinto`.

   .. method:: readall()

      Đọc và trả về tất cả các byte từ stream cho đến EOF, sử dụng nhiều lệnh gọi đến stream nếu cần.

      Nếu trả về ``0`` byte, điều này cho biết đã đến cuối tệp. Nếu đối tượng ở chế độ non-blocking và :meth:`read` bên dưới trả về ``None``, cho biết không có byte nào khả dụng, thì ``None`` sẽ được trả về.

   .. method:: readinto(b, /)

      Đọc các byte vào một vùng đệm có thể ghi được cấp phát trước
      :term:`bytes-like object` *b*, và trả về số byte đã đọc. Ví dụ, *b* có thể là một :class:`bytearray`.

      Nếu trả về ``0`` và ``len(b)`` không phải là ``0``, điều này cho biết đã đến cuối tệp. Nếu đối tượng ở chế độ non-blocking và không có byte nào khả dụng, ``None`` sẽ được trả về.

   .. method:: write(b, /)

      Ghi :term:`bytes-like object` đã cho, *b*, vào raw stream bên dưới và trả về số byte đã ghi. Giá trị này có thể nhỏ hơn độ dài tính theo byte của *b*, tùy thuộc vào đặc điểm của raw stream bên dưới, đặc biệt nếu stream đang ở chế độ non-blocking. ``None`` được trả về nếu raw stream được đặt ở chế độ không chặn và không thể ghi ngay cả một byte nào vào đó. Bên gọi có thể giải phóng hoặc thay đổi *b* sau khi phương thức này trả về, vì vậy phần triển khai chỉ nên truy cập *b* trong khi phương thức đang được gọi.

      .. warning::

         Hàm này không đảm bảo tất cả các byte đều được ghi hoặc một ngoại lệ được ném ra. Bên gọi có thể triển khai hành vi đó bằng cách kiểm tra giá trị trả về và, nếu giá trị này nhỏ hơn độ dài tính theo byte của *b*, lặp lại với các lần gọi write bổ sung cho đến khi tất cả các byte chưa ghi được ghi xong. Các đối tượng I/O cấp cao như :ref:`binary-io` và :ref:`text-io` triển khai hành vi retry.

.. class:: BufferedIOBase

   Lớp cơ sở cho các binary stream hỗ trợ một dạng buffering nào đó. Lớp này kế thừa từ :class:`IOBase`.

   Điểm khác biệt chính so với :class:`RawIOBase` là các phương thức :meth:`read`,
   :meth:`readinto` và :meth:`write` sẽ lần lượt cố gắng đọc lượng dữ liệu đầu vào được yêu cầu hoặc phát ra toàn bộ dữ liệu đã cung cấp.

   Ngoài ra, nếu raw stream bên dưới đang ở chế độ non-blocking, khi hệ thống trả về trạng thái would block, :meth:`write` sẽ raise :exc:`BlockingIOError` với :attr:`BlockingIOError.characters_written`, còn :meth:`read` sẽ trả về dữ liệu đã đọc được cho đến lúc đó hoặc ``None`` nếu không có dữ liệu.

   Ngoài ra, phương thức :meth:`read` không có triển khai mặc định ủy quyền cho :meth:`readinto`.

   Một triển khai :class:`BufferedIOBase` điển hình không nên kế thừa từ một
   triển khai :class:`RawIOBase`, mà nên bọc một triển khai, như
   :class:`BufferedWriter` và :class:`BufferedReader`.

   :class:`BufferedIOBase` cung cấp hoặc ghi đè các thuộc tính dữ liệu và phương thức sau, ngoài những thuộc tính và phương thức của :class:`IOBase`:

   .. attribute:: raw

      Luồng raw nền tảng (một thực thể :class:`RawIOBase`) mà
      :class:`BufferedIOBase` xử lý. Đây không phải là một phần của
      API :class:`BufferedIOBase` và có thể không tồn tại trên một số bản triển khai.

   .. method:: detach()

      Tách luồng raw nền tảng khỏi buffer và trả về luồng đó.

      Sau khi luồng raw được tách ra, buffer sẽ ở trạng thái không thể sử dụng.

      Một số buffer, chẳng hạn như :class:`BytesIO`, không có khái niệm về một luồng raw duy nhất để trả về từ phương thức này. Chúng sẽ đưa ra
      :exc:`UnsupportedOperation`.

      .. versionadded:: 3.1

   .. method:: read(size=-1, /)

      Đọc và trả về tối đa *size* byte. Nếu đối số bị bỏ qua, ``None``, hoặc là số âm, hãy đọc nhiều nhất có thể.

      Có thể trả về ít byte hơn số byte được yêu cầu. Một đối tượng :class:`bytes` rỗng được trả về nếu luồng đã ở EOF. Có thể thực hiện nhiều lần đọc và thử lại các lệnh gọi nếu gặp lỗi cụ thể, xem
      :meth:`os.read` và :pep:`475` để biết thêm chi tiết. Việc trả về ít hơn số byte size không có nghĩa là EOF sắp xảy ra.

      Khi đọc nhiều nhất có thể, phần triển khai mặc định sẽ sử dụng ``raw.readall`` nếu có (vốn phải triển khai
      :meth:`RawIOBase.readall`), nếu không thì sẽ đọc trong một vòng lặp cho đến khi read trả về ``None``, một :class:`bytes` rỗng hoặc một lỗi không thể thử lại. Với hầu hết các luồng, quá trình này sẽ tiếp tục đến EOF, nhưng đối với các luồng không blocking, có thể sẽ có thêm dữ liệu khả dụng.

      .. note::

         Khi raw stream bên dưới không blocking, các phần triển khai có thể raise :exc:`BlockingIOError` hoặc return ``None`` nếu không có dữ liệu. Các phần triển khai :mod:`!io` trả về ``None``.

   .. method:: read1(size=-1, /)

      Đọc và trả về tối đa *size* byte, gọi :meth:`~RawIOBase.readinto`, vốn có thể thử lại nếu gặp :py:const:`~errno.EINTR` theo
      :pep:`475`. Nếu *size* là ``-1`` hoặc không được cung cấp, phần triển khai sẽ chọn một giá trị tùy ý cho *size*.

      .. note::

         Khi raw stream bên dưới không blocking, các phần triển khai có thể raise :exc:`BlockingIOError` hoặc return ``None`` nếu không có dữ liệu. Các phần triển khai :mod:`!io` trả về ``None``.

   .. method:: readinto(b, /)

      Đọc các byte vào một vùng đệm có thể ghi được cấp phát trước
      Đọc các byte vào một đối tượng dạng byte có thể ghi, được cấp phát trước :term:`bytes-like object` *b* và trả về số byte đã đọc. Ví dụ, *b* có thể là một :class:`bytearray`.

      Tương tự như :meth:`read`, có thể thực hiện nhiều lần đọc trên raw stream bên dưới, trừ khi raw stream đó ở chế độ tương tác.

      Một :exc:`BlockingIOError` sẽ được phát sinh nếu raw stream bên dưới đang ở chế độ non-blocking và hiện không có dữ liệu.

   .. method:: readinto1(b, /)

      Đọc các byte vào một vùng đệm có thể ghi được cấp phát trước
      Đọc tối đa các byte vào :term:`bytes-like object` *b*, chỉ sử dụng nhiều nhất một lần gọi đến :meth:`~RawIOBase.read` của raw stream bên dưới (hoặc
      :meth:`~RawIOBase.readinto`) method. Trả về số byte đã đọc.

      Một :exc:`BlockingIOError` sẽ được phát sinh nếu raw stream bên dưới đang ở chế độ non-blocking và hiện không có dữ liệu.

      .. versionadded:: 3.5

   .. method:: write(b, /)

      Ghi :term:`bytes-like object` đã cho, *b*, và trả về số byte đã ghi (luôn bằng độ dài của *b* tính theo byte, vì nếu thao tác ghi thất bại, một :exc:`OSError` sẽ được phát sinh). Tùy thuộc vào cách triển khai thực tế, các byte này có thể được ghi ngay vào stream bên dưới hoặc được giữ trong bộ đệm vì lý do hiệu năng và độ trễ.

      Khi ở chế độ không chặn, một :exc:`BlockingIOError` sẽ được phát sinh nếu dữ liệu cần ghi vào raw stream nhưng raw stream không thể nhận toàn bộ dữ liệu mà không bị chặn.

      Caller có thể giải phóng hoặc thay đổi *b* sau khi phương thức này trả về, vì vậy phần triển khai chỉ nên truy cập *b* trong lúc gọi phương thức.


I/O tệp thô
^^^^^^^^^^^

.. class:: FileIO(name, mode='r', closefd=True, opener=None)

   Một binary stream thô đại diện cho một tệp ở cấp hệ điều hành chứa dữ liệu dạng byte. Nó kế thừa từ :class:`RawIOBase` và triển khai thiết kế truy cập cấp thấp của lớp đó. Điều này có nghĩa là :meth:`~RawIOBase.write` không đảm bảo tất cả byte đều được ghi và :meth:`~RawIOBase.read` có thể đọc ít byte hơn số byte được yêu cầu ngay cả khi tệp bên dưới còn nhiều byte hơn. Để có hành vi "ghi tất cả" và "đọc ít nhất", hãy sử dụng :ref:`binary-io`.

   Đối số *name* có thể là một trong hai dạng:

   * một chuỗi ký tự hoặc một đối tượng :class:`bytes` đại diện cho đường dẫn đến tệp sẽ được mở. Trong trường hợp này, closefd phải là ``True`` (mặc định), nếu không sẽ phát sinh lỗi.
   * một số nguyên đại diện cho số hiệu của một file descriptor ở cấp hệ điều hành hiện có mà đối tượng :class:`FileIO` được tạo ra sẽ cung cấp quyền truy cập. Khi đối tượng FileIO được đóng, fd này cũng sẽ được đóng, trừ khi *closefd* được đặt thành ``False``.

   *mode* có thể là ``'r'``, ``'w'``, ``'x'`` hoặc ``'a'`` tương ứng với đọc (mặc định), ghi, tạo độc quyền hoặc nối thêm. Tệp sẽ được tạo nếu chưa tồn tại khi mở để ghi hoặc nối thêm; tệp sẽ bị cắt ngắn khi mở để ghi. :exc:`FileExistsError` sẽ được phát sinh nếu tệp đã tồn tại khi mở để tạo. Việc mở tệp để tạo ngụ ý thao tác ghi, vì vậy mode này hoạt động tương tự như ``'w'``. Thêm ``'+'`` vào mode để cho phép đọc và ghi đồng thời.

   Có thể sử dụng một opener tùy chỉnh bằng cách truyền một callable làm *opener*. Sau đó, file descriptor nền tảng của đối tượng tệp được lấy bằng cách gọi *opener* với (*name*, *flags*). *opener* phải trả về một file descriptor đang mở (truyền
   :mod:`os.open` làm *opener* cho chức năng tương tự như truyền ``None``).

   Tệp mới được tạo là :ref:`non-inheritable <fd_inheritance>`.

   Xem hàm dựng sẵn :func:`open` để biết các ví dụ về cách sử dụng tham số *opener*.

   .. warning::
      :class:`FileIO` is a low-level I/O object and members, such as
      :meth:`~RawIOBase.read` and :meth:`~RawIOBase.write`, need to have their
      các giá trị trả về được kiểm tra rõ ràng trong một vòng lặp thử lại để triển khai hành vi "ghi toàn bộ" và "đọc ít nhất". Các đối tượng I/O cấp cao :ref:`binary-io` và
      :ref:`text-io` triển khai cơ chế thử lại.

   .. versionchanged:: 3.3
      Tham số *opener* đã được bổ sung. Chế độ ``'x'`` đã được bổ sung.

   .. versionchanged:: 3.4
      Tệp hiện không thể kế thừa.

   :class:`FileIO` cung cấp các thuộc tính dữ liệu sau, ngoài những thuộc tính từ
   :class:`RawIOBase` và :class:`IOBase`:

   .. attribute:: mode

      Chế độ được cung cấp trong hàm khởi tạo.

   .. attribute:: name

      Tên tệp.  Đây là bộ mô tả tệp của tệp khi không cung cấp tên trong hàm khởi tạo.


Các luồng có bộ đệm
^^^^^^^^^^^^^^^^^^^

Các luồng I/O có bộ đệm cung cấp giao diện cấp cao hơn để tương tác với thiết bị I/O so với I/O thô.

.. class:: BytesIO(initial_bytes=b'')

   Một luồng nhị phân sử dụng bộ đệm bytes trong bộ nhớ.  Nó kế thừa từ
   :class:`BufferedIOBase`.  Bộ đệm sẽ bị loại bỏ khi
   :meth:`~IOBase.close` được gọi.

   Đối số tùy chọn *initial_bytes* là một :term:`bytes-like object` chứa dữ liệu ban đầu.

   :class:`BytesIO` cung cấp hoặc ghi đè các phương thức này, ngoài các phương thức từ :class:`BufferedIOBase` và :class:`IOBase`:

   .. method:: getbuffer()

      Trả về một view có thể đọc và ghi trên nội dung của buffer mà không sao chép nội dung. Ngoài ra, việc thay đổi view sẽ tự động cập nhật nội dung của buffer::

         >>> b = io.BytesIO(b"abcdef")
         >>> view = b.getbuffer()
         >>> view[2:4] = b"56"
         >>> b.getvalue()
         b'ab56ef'

      .. note::
         Chừng nào view còn tồn tại, đối tượng :class:`BytesIO` không thể được thay đổi kích thước hoặc đóng.

      .. versionadded:: 3.2

   .. method:: getvalue()

      Trả về :class:`bytes` chứa toàn bộ nội dung của buffer.


   .. method:: read1(size=-1, /)

      Trong :class:`BytesIO`, điều này giống với :meth:`~BufferedIOBase.read`.

      .. versionchanged:: 3.7
         Đối số *size* hiện là tùy chọn.

   .. method:: readinto1(b, /)

      Trong :class:`BytesIO`, điều này tương đương với :meth:`~BufferedIOBase.readinto`.

      .. versionadded:: 3.5

.. class:: BufferedReader(raw, buffer_size=DEFAULT_BUFFER_SIZE)

   Một binary stream có bộ đệm, cung cấp quyền truy cập ở cấp cao hơn vào :class:`RawIOBase` raw binary stream có thể đọc nhưng không thể seek. Nó kế thừa từ
   :class:`BufferedIOBase`.

   Khi đọc dữ liệu từ đối tượng này, có thể yêu cầu một lượng dữ liệu lớn hơn từ raw stream bên dưới và giữ dữ liệu đó trong một bộ đệm nội bộ. Sau đó, dữ liệu trong bộ đệm có thể được trả về trực tiếp trong các lần đọc tiếp theo.

   Hàm khởi tạo tạo một :class:`BufferedReader` cho *raw* stream có thể đọc đã cho và *buffer_size*. Nếu *buffer_size* bị bỏ qua,
   :data:`DEFAULT_BUFFER_SIZE` được sử dụng.

   :class:`BufferedReader` cung cấp hoặc ghi đè các phương thức sau, ngoài những phương thức từ :class:`BufferedIOBase` và :class:`IOBase`:

   .. method:: peek(size=0, /)

      Trả về các byte từ stream mà không làm thay đổi vị trí. Số byte được trả về có thể ít hơn hoặc nhiều hơn số byte được yêu cầu. Nếu raw stream bên dưới hoạt động ở chế độ non-blocking và thao tác sẽ bị block, trả về các byte rỗng.

   .. method:: read(size=-1, /)

      Trong :class:`BufferedReader`, điều này tương đương với :meth:`io.BufferedIOBase.read`

   .. method:: read1(size=-1, /)

      Trong :class:`BufferedReader`, điều này tương đương với :meth:`io.BufferedIOBase.read1`

      .. versionchanged:: 3.7
         Đối số *size* hiện là tùy chọn.

.. class:: BufferedWriter(raw, buffer_size=DEFAULT_BUFFER_SIZE)

   Một buffered binary stream cung cấp quyền truy cập ở mức cao hơn vào :class:`RawIOBase`, một raw binary stream có thể ghi nhưng không thể seek. Nó kế thừa từ
   :class:`BufferedIOBase`.

   Khi ghi vào đối tượng này, dữ liệu thường được đặt vào một buffer nội bộ. Buffer sẽ được ghi ra đối tượng :class:`RawIOBase` bên dưới trong nhiều trường hợp khác nhau, bao gồm:

   * khi buffer trở nên quá nhỏ để chứa toàn bộ dữ liệu đang chờ;
   * khi gọi :meth:`flush`;
   * khi yêu cầu :meth:`~IOBase.seek` (đối với các đối tượng :class:`BufferedRandom`);
   * khi đối tượng :class:`BufferedWriter` được đóng hoặc hủy.

   Hàm khởi tạo tạo một :class:`BufferedWriter` cho stream *raw* có thể ghi đã cho. Nếu *buffer_size* không được cung cấp, giá trị mặc định là
   :data:`DEFAULT_BUFFER_SIZE`.

   :class:`BufferedWriter` cung cấp hoặc ghi đè các phương thức này, ngoài các phương thức từ :class:`BufferedIOBase` và :class:`IOBase`:

   .. method:: flush()

      Buộc các byte được lưu trong bộ đệm vào raw stream. Một
      :exc:`BlockingIOError` nên được phát sinh nếu raw stream bị chặn.

   .. method:: write(b, /)

      Ghi :term:`bytes-like object`, *b*, và trả về số byte đã ghi. Khi ở chế độ non-blocking, một
      Ngoại lệ :exc:`BlockingIOError` với :attr:`BlockingIOError.characters_written` được đặt sẽ được phát sinh nếu bộ đệm cần được ghi ra nhưng raw stream bị chặn.


.. class:: BufferedRandom(raw, buffer_size=DEFAULT_BUFFER_SIZE)

   Một buffered binary stream triển khai các interface :class:`BufferedIOBase`, cung cấp quyền truy cập cấp cao hơn vào một raw binary stream :class:`RawIOBase` có thể seek.

   Constructor tạo một reader và writer cho raw stream có thể seek, được truyền trong đối số đầu tiên. Nếu *buffer_size* bị bỏ qua, giá trị mặc định là
   :data:`DEFAULT_BUFFER_SIZE`.

   :class:`BufferedRandom` có thể thực hiện mọi việc mà :class:`BufferedReader` hoặc
   :class:`BufferedWriter` có thể thực hiện. Ngoài ra, :meth:`~IOBase.seek` và
   :meth:`~IOBase.tell` được đảm bảo là đã được triển khai.


.. class:: BufferedRWPair(reader, writer, buffer_size=DEFAULT_BUFFER_SIZE, /)

   Một buffered binary stream cung cấp quyền truy cập cấp cao hơn vào hai stream không hỗ trợ seek
   :class:`RawIOBase` là các luồng nhị phân thô—một luồng có thể đọc, luồng kia có thể ghi. Nó kế thừa từ :class:`BufferedIOBase`.

   *reader* và *writer* lần lượt là các đối tượng :class:`RawIOBase` có thể đọc và ghi. Nếu *buffer_size* bị bỏ qua, giá trị mặc định là
   :data:`DEFAULT_BUFFER_SIZE`.

   :class:`BufferedRWPair` triển khai tất cả các phương thức của :class:`BufferedIOBase`\'s, ngoại trừ :meth:`~BufferedIOBase.detach`, phương thức này sẽ phát sinh
   :exc:`UnsupportedOperation`.

   .. warning::

      :class:`BufferedRWPair` không cố gắng đồng bộ hóa việc truy cập vào các raw stream bên dưới. Bạn không nên truyền cùng một đối tượng cho reader và writer; thay vào đó, hãy sử dụng :class:`BufferedRandom`.


I/O văn bản
^^^^^^^^^^^

.. class:: TextIOBase

   Lớp cơ sở cho các luồng văn bản. Lớp này cung cấp giao diện I/O dựa trên ký tự và dòng. Nó kế thừa từ :class:`IOBase`.

   :class:`TextIOBase` cung cấp hoặc ghi đè các thuộc tính dữ liệu và phương thức sau, ngoài những thuộc tính và phương thức từ :class:`IOBase`:

   .. attribute:: encoding

      Tên của encoding được dùng để giải mã các byte của stream thành các chuỗi và mã hóa các chuỗi thành byte.

   .. attribute:: errors

      Thiết lập lỗi của decoder hoặc encoder.

   .. attribute:: newlines

      Một chuỗi, một tuple gồm các chuỗi hoặc ``None``, cho biết các ký tự xuống dòng đã được chuyển đổi cho đến thời điểm hiện tại. Tùy thuộc vào cách triển khai và các cờ constructor ban đầu, thông tin này có thể không khả dụng.

   .. attribute:: buffer

      Bộ đệm nhị phân bên dưới (một instance của :class:`BufferedIOBase` hoặc :class:`RawIOBase`) mà :class:`TextIOBase` xử lý. Đây không phải là một phần của API :class:`TextIOBase` và có thể không tồn tại trong một số cách triển khai.

   .. method:: detach()

      Tách bộ đệm nhị phân bên dưới khỏi :class:`TextIOBase` và trả về bộ đệm đó.

      Sau khi bộ đệm bên dưới được tách ra, :class:`TextIOBase` sẽ ở trạng thái không thể sử dụng.

      Một số cách triển khai :class:`TextIOBase`, chẳng hạn như :class:`StringIO`, có thể không có khái niệm về bộ đệm bên dưới; việc gọi phương thức này sẽ phát sinh :exc:`UnsupportedOperation`.

      .. versionadded:: 3.1

   .. method:: read(size=-1, /)

      Đọc và trả về nhiều nhất *size* ký tự từ stream dưới dạng một
      :class:`str`.  Nếu *size* là số âm hoặc ``None``, đọc cho đến EOF.

   .. method:: readline(size=-1, /)

      Đọc cho đến dòng mới hoặc EOF và trả về một :class:`str`.  Nếu stream đã ở EOF, một chuỗi rỗng sẽ được trả về.

      Nếu *size* được chỉ định, nhiều nhất *size* ký tự sẽ được đọc.

   .. method:: seek(offset, whence=SEEK_SET, /)

      Thay đổi vị trí của stream thành *offset* đã cho.  Hành vi phụ thuộc vào tham số *whence*.  Giá trị mặc định của *whence* là
      :data:`!SEEK_SET`.

      * :data:`!SEEK_SET` hoặc ``0``: tìm vị trí từ đầu stream (mặc định); *offset* phải là một số được trả về bởi
        :meth:`TextIOBase.tell`, hoặc bằng không.  Bất kỳ giá trị *offset* nào khác đều tạo ra hành vi không xác định.
      * :data:`!SEEK_CUR` hoặc ``1``: "seek" đến vị trí hiện tại; *offset* phải bằng không, đây là thao tác không làm gì (no-op) (mọi giá trị khác đều không được hỗ trợ).
      * :data:`!SEEK_END` hoặc ``2``: seek đến cuối stream; *offset* phải bằng không (mọi giá trị khác đều không được hỗ trợ).

      Trả về vị trí tuyệt đối mới dưới dạng một số opaque.

      .. versionadded:: 3.1
         Các hằng số :data:`!SEEK_*`.

   .. method:: tell()

      Trả về vị trí hiện tại của stream dưới dạng một số opaque. Số này thường không biểu thị số byte trong bộ lưu trữ nhị phân bên dưới.

   .. method:: write(s, /)

      Ghi chuỗi *s* vào stream và trả về số ký tự đã ghi.


.. class:: TextIOWrapper(buffer, encoding=None, errors=None, newline=None, \
                         line_buffering=False, write_through=False)

   Một luồng văn bản có bộ đệm cung cấp quyền truy cập cấp cao hơn vào một
   :class:`BufferedIOBase` luồng nhị phân có bộ đệm. Nó kế thừa từ
   :class:`TextIOBase`.

   *encoding* chỉ định tên của encoding mà luồng sẽ được giải mã hoặc mã hóa bằng encoding đó. Trong :ref:`UTF-8 Mode <utf8-mode>`, giá trị mặc định là UTF-8. Nếu không, giá trị mặc định là :func:`locale.getencoding`. Có thể sử dụng ``encoding="locale"`` để chỉ định rõ ràng encoding của locale hiện tại. Xem :ref:`io-text-encoding` để biết thêm thông tin.

   *errors* là một chuỗi tùy chọn chỉ định cách xử lý các lỗi mã hóa và giải mã. Truyền ``'strict'`` để raise một ngoại lệ :exc:`ValueError` nếu xảy ra lỗi mã hóa (giá trị mặc định ``None`` cũng có tác dụng tương tự), hoặc truyền ``'ignore'`` để bỏ qua lỗi. (Lưu ý rằng việc bỏ qua lỗi mã hóa có thể dẫn đến mất dữ liệu.) ``'replace'`` khiến một dấu đánh dấu thay thế (chẳng hạn như ``'?'``) được chèn vào vị trí có dữ liệu không đúng định dạng. ``'backslashreplace'`` khiến dữ liệu không đúng định dạng được thay thế bằng một chuỗi escape có dấu gạch chéo ngược. Khi ghi, có thể sử dụng ``'xmlcharrefreplace'`` (thay thế bằng tham chiếu ký tự XML thích hợp) hoặc ``'namereplace'`` (thay thế bằng các chuỗi escape ``\N{...}``). Bất kỳ tên xử lý lỗi nào khác đã được đăng ký với
   :func:`codecs.register_error` cũng hợp lệ.

   .. index::
      single: universal newlines; io.TextIOWrapper class

   *newline* kiểm soát cách xử lý các ký tự kết thúc dòng. Nó có thể là ``None``, ``''``, ``'\n'``, ``'\r'`` hoặc ``'\r\n'``. Cách hoạt động như sau:

   * Khi đọc dữ liệu đầu vào từ luồng, nếu *newline* là ``None``,
     Chế độ :term:`universal newlines` đã được bật. Các dòng trong đầu vào có thể kết thúc bằng ``'\n'``, ``'\r'`` hoặc ``'\r\n'``, và các giá trị này được chuyển thành ``'\n'`` trước khi trả về cho caller. Nếu *newline* là ``''``, chế độ universal newlines được bật, nhưng các ký tự kết thúc dòng được trả về cho caller mà không được dịch. Nếu *newline* có bất kỳ giá trị hợp lệ nào khác, các dòng đầu vào chỉ được kết thúc bằng chuỗi đã cho, và ký tự kết thúc dòng được trả về cho caller mà không được dịch.

   * Khi ghi đầu ra vào stream, nếu *newline* là ``None``, mọi ký tự ``'\n'`` được ghi sẽ được chuyển thành dấu phân cách dòng mặc định của hệ thống,
     :data:`os.linesep`. Nếu *newline* là ``''`` hoặc ``'\n'``, sẽ không có quá trình dịch nào diễn ra. Nếu *newline* có bất kỳ giá trị hợp lệ nào khác, mọi ký tự ``'\n'`` được ghi sẽ được chuyển thành chuỗi đã cho.

   Nếu *line_buffering* là ``True``, :meth:`~IOBase.flush` được ngầm định khi một lần gọi write chứa ký tự newline hoặc carriage return.

   Nếu *write_through* là ``True``, các lần gọi :meth:`~BufferedIOBase.write` được đảm bảo không bị buffered: mọi dữ liệu được ghi vào đối tượng :class:`TextIOWrapper` sẽ ngay lập tức được xử lý bởi *buffer* nhị phân bên dưới.

   .. versionchanged:: 3.3
      Đối số *write_through* đã được thêm vào.

   .. versionchanged:: 3.3
      *encoding* mặc định hiện là ``locale.getpreferredencoding(False)`` thay vì ``locale.getpreferredencoding()``. Không tạm thời thay đổi encoding của locale bằng :func:`locale.setlocale`; thay vào đó, hãy sử dụng encoding của locale hiện tại thay vì encoding được người dùng ưu tiên.

   .. versionchanged:: 3.10
      Đối số *encoding* giờ đây hỗ trợ tên encoding dummy ``"locale"``.

   .. note::

      Khi raw stream bên dưới không chặn, một :exc:`BlockingIOError` có thể được phát sinh nếu thao tác đọc không thể hoàn tất ngay lập tức.

   :class:`TextIOWrapper` cung cấp các thuộc tính dữ liệu và phương thức sau, ngoài những thuộc tính và phương thức từ :class:`TextIOBase` và :class:`IOBase`:

   .. attribute:: line_buffering

      Cho biết line buffering có được bật hay không.

   .. attribute:: write_through

      Cho biết các thao tác ghi có được chuyển ngay đến binary buffer bên dưới hay không.

      .. versionadded:: 3.7

   .. method:: reconfigure(*, encoding=None, errors=None, newline=None, \
                           line_buffering=None, write_through=None)

      Cấu hình lại text stream này bằng các thiết lập mới cho *encoding*, *errors*, *newline*, *line_buffering* và *write_through*.

      Các tham số không được chỉ định sẽ giữ nguyên cài đặt hiện tại, ngoại trừ ``errors='strict'`` được sử dụng khi *encoding* được chỉ định nhưng *errors* không được chỉ định.

      Không thể thay đổi encoding hoặc ký tự dòng mới nếu một phần dữ liệu đã được đọc từ stream. Mặt khác, có thể thay đổi encoding sau khi ghi.

      Phương thức này sẽ ngầm flush stream trước khi thiết lập các tham số mới.

      .. versionadded:: 3.7

      .. versionchanged:: 3.11
         Phương thức này hỗ trợ tùy chọn ``encoding="locale"``.

   .. method:: seek(cookie, whence=os.SEEK_SET, /)

      Đặt vị trí của stream. Trả về vị trí mới của stream dưới dạng :class:`int`.

      Bốn thao tác được hỗ trợ, tương ứng với các tổ hợp đối số sau:

      * ``seek(0, SEEK_SET)``: Tua lại về đầu stream.
      * ``seek(cookie, SEEK_SET)``: Khôi phục một vị trí trước đó; *cookie* **phải là** một số được trả về bởi :meth:`tell`.
      * ``seek(0, SEEK_END)``: Tua nhanh đến cuối stream.
      * ``seek(0, SEEK_CUR)``: Giữ nguyên vị trí hiện tại của stream.

      Mọi tổ hợp đối số khác đều không hợp lệ và có thể gây ra ngoại lệ.

      .. seealso::

         :data:`os.SEEK_SET`, :data:`os.SEEK_CUR` và :data:`os.SEEK_END`.

   .. method:: tell()

      Trả về vị trí của stream dưới dạng một số không trong suốt. Giá trị trả về của :meth:`!tell` có thể được cung cấp làm đầu vào cho :meth:`seek` để khôi phục một vị trí trước đó của stream.


.. class:: StringIO(initial_value='', newline='\n')

   Một text stream sử dụng bộ đệm văn bản trong bộ nhớ. Nó kế thừa từ
   :class:`TextIOBase`.

   Bộ đệm văn bản bị loại bỏ khi phương thức :meth:`~IOBase.close` được gọi.

   Có thể đặt giá trị ban đầu của bộ đệm bằng cách cung cấp *initial_value*. Nếu bật tính năng chuyển đổi dòng mới, các dòng mới sẽ được mã hóa như thể bằng
   :meth:`~TextIOBase.write`. Luồng được đặt ở đầu bộ đệm, mô phỏng việc mở một tệp hiện có ở chế độ ``w+``, sẵn sàng để ghi ngay từ đầu hoặc ghi đè lên giá trị ban đầu. Để mô phỏng việc mở tệp ở chế độ ``a+`` sẵn sàng để ghi nối tiếp, hãy dùng ``f.seek(0, io.SEEK_END)`` để định vị lại luồng ở cuối bộ đệm.

   Đối số *newline* hoạt động giống như đối số của :class:`TextIOWrapper`, ngoại trừ khi ghi đầu ra vào luồng, nếu *newline* là ``None``, các dòng mới sẽ được ghi dưới dạng ``\n`` trên mọi nền tảng.

   :class:`StringIO` cung cấp phương thức này ngoài các phương thức từ
   :class:`TextIOBase` và :class:`IOBase`:

   .. method:: getvalue()

      Trả về một :class:`str` chứa toàn bộ nội dung của bộ đệm. Các dòng mới được giải mã như thể bằng :meth:`~TextIOBase.read`, mặc dù vị trí luồng không thay đổi.

   Ví dụ sử dụng::

      import io

      output = io.StringIO()
      output.write('First line.\n')
      print('Second line.', file=output)

      # Lấy nội dung tệp -- nội dung này sẽ là
      # 'First line.\nSecond line.\n'
      contents = output.getvalue()

      # Đóng đối tượng và loại bỏ bộ đệm trong bộ nhớ --
      # .getvalue() giờ đây sẽ phát sinh một ngoại lệ.
      output.close()


.. index::
   single: universal newlines; io.IncrementalNewlineDecoder class

.. class:: IncrementalNewlineDecoder

   Một codec hỗ trợ giải mã ký tự xuống dòng cho chế độ :term:`universal newlines`. Nó kế thừa từ :class:`codecs.IncrementalDecoder`.


Kiểu tĩnh
---------

Các protocol sau đây có thể được sử dụng để chú thích các đối số của hàm và method cho các thao tác đọc hoặc ghi stream đơn giản. Chúng được trang trí bằng :deco:`typing.runtime_checkable`.

.. class:: Reader[T]

   Protocol tổng quát để đọc từ tệp hoặc stream đầu vào khác. ``T`` thường sẽ là :class:`str` hoặc :class:`bytes`, nhưng có thể là bất kỳ kiểu nào được đọc từ stream.

   .. versionadded:: 3.14

   .. method:: read()
               read(size, /)

      Đọc dữ liệu từ stream đầu vào và trả về dữ liệu đó. Nếu chỉ định *size*, giá trị này phải là một số nguyên và tối đa *size* mục (byte/ký tự) sẽ được đọc.

   Ví dụ::

     def read_it(reader: Reader[str]):
         data = reader.read(11)
         assert isinstance(data, str)

.. class:: Writer[T]

   Protocol tổng quát để ghi vào tệp hoặc stream đầu ra khác. ``T`` thường sẽ là :class:`str` hoặc :class:`bytes`, nhưng có thể là bất kỳ kiểu nào có thể được ghi vào stream.

   .. versionadded:: 3.14

   .. method:: write(data, /)

      Ghi *data* vào stream đầu ra và trả về số mục (byte/ký tự) đã được ghi.

   Ví dụ::

     def write_binary(writer: Writer[bytes]):
         writer.write(b"Hello world!\n")

Xem :ref:`typing-io` để biết các giao thức và lớp liên quan đến I/O khác có thể được sử dụng cho static type checking.

Hiệu năng
---------

Phần này thảo luận về hiệu năng của các triển khai I/O cụ thể được cung cấp.

I/O nhị phân
^^^^^^^^^^^^

Bằng cách chỉ đọc và ghi các khối dữ liệu lớn ngay cả khi người dùng yêu cầu một byte duy nhất, buffered I/O che giấu mọi sự kém hiệu quả trong việc gọi và thực thi các routine I/O không có bộ đệm của hệ điều hành. Mức cải thiện phụ thuộc vào hệ điều hành và loại I/O được thực hiện. Ví dụ, trên một số hệ điều hành hiện đại như Linux, disk I/O không có bộ đệm có thể nhanh bằng buffered I/O. Tuy nhiên, điểm mấu chốt là buffered I/O mang lại hiệu năng ổn định, bất kể nền tảng và thiết bị lưu trữ. Do đó, gần như luôn nên sử dụng buffered I/O thay vì I/O không có bộ đệm cho dữ liệu nhị phân.

I/O văn bản
^^^^^^^^^^^

I/O văn bản trên bộ lưu trữ nhị phân (chẳng hạn như một tệp) chậm hơn đáng kể so với I/O nhị phân trên cùng bộ lưu trữ, vì nó yêu cầu chuyển đổi giữa dữ liệu unicode và dữ liệu nhị phân bằng codec ký tự. Điều này có thể trở nên rõ rệt khi xử lý lượng dữ liệu văn bản khổng lồ, chẳng hạn như các tệp nhật ký lớn. Ngoài ra,
:meth:`~TextIOBase.tell` và :meth:`~TextIOBase.seek` đều khá chậm do thuật toán tái tạo được sử dụng.

Tuy nhiên, :class:`StringIO` là một vùng chứa unicode gốc trong bộ nhớ và sẽ có tốc độ tương tự như :class:`BytesIO`.

Đa luồng
^^^^^^^^

Các đối tượng :class:`FileIO` an toàn với luồng (thread-safe) trong phạm vi các lệnh gọi hệ điều hành (chẳng hạn như :manpage:`read(2)` trên Unix) mà chúng bao bọc cũng an toàn với luồng.

Các đối tượng đệm nhị phân (các thể hiện của :class:`BufferedReader`,
:class:`BufferedWriter`, :class:`BufferedRandom` và :class:`BufferedRWPair`) bảo vệ các cấu trúc bên trong bằng một khóa; do đó, việc gọi chúng từ nhiều luồng cùng lúc là an toàn.

Các đối tượng :class:`TextIOWrapper` không an toàn khi sử dụng trong môi trường đa luồng.

Tính tái nhập
^^^^^^^^^^^^^

Các đối tượng đệm nhị phân (các thực thể của :class:`BufferedReader`,
:class:`BufferedWriter`, :class:`BufferedRandom` và :class:`BufferedRWPair`) không có tính tái nhập. Mặc dù các lời gọi tái nhập sẽ không xảy ra trong những tình huống thông thường, chúng có thể phát sinh khi thực hiện I/O trong một trình xử lý :mod:`signal`. Nếu một thread cố gắng tái nhập vào một đối tượng đệm mà nó đang truy cập, một :exc:`RuntimeError` sẽ được phát sinh. Lưu ý rằng điều này không ngăn một thread khác truy cập vào đối tượng đệm.

Điều trên mặc nhiên cũng áp dụng cho các tệp văn bản, vì hàm :func:`open` sẽ bọc một đối tượng đệm bên trong một :class:`TextIOWrapper`. Điều này bao gồm cả các luồng tiêu chuẩn và do đó cũng ảnh hưởng đến hàm dựng sẵn :func:`print`.
