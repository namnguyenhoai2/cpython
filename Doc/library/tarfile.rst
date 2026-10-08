:mod:`!tarfile` --- Đọc và ghi các tệp lưu trữ tar
==================================================

.. module:: tarfile
   :synopsis: Đọc và ghi các tệp lưu trữ định dạng tar.

.. moduleauthor:: Lars Gustäbel <lars@gustaebel.de>
.. sectionauthor:: Lars Gustäbel <lars@gustaebel.de>

**Mã nguồn:** :source:`Lib/tarfile.py`

--------------

Mô-đun :mod:`!tarfile` cho phép đọc và ghi các kho lưu trữ tar, bao gồm cả những kho sử dụng tính năng nén gzip, bz2 và lzma. Sử dụng mô-đun :mod:`zipfile` để đọc hoặc ghi các tệp :file:`.zip`, hoặc sử dụng các hàm cấp cao hơn trong :ref:`shutil <archiving-operations>`.

Một số thông tin và số liệu:

* đọc và ghi :mod:`gzip`, :mod:`bz2`, :mod:`compression.zstd`, và
  :mod:`lzma` các kho lưu trữ được nén nếu có các mô-đun tương ứng.

  ..
     Đoạn văn sau đây phải tương tự như ../includes/optional-module.rst

  Nếu bất kỳ :term:`mô-đun tùy chọn <optional module>` nào trong số này bị thiếu trong bản CPython của bạn, hãy tìm tài liệu từ nhà phân phối của bạn (tức là bên đã cung cấp Python cho bạn). Nếu bạn là nhà phân phối, hãy xem :ref:`optional-module-requirements`.

* hỗ trợ đọc/ghi định dạng POSIX.1-1988 (ustar).

* hỗ trợ đọc/ghi định dạng GNU tar, bao gồm các phần mở rộng *longname* và *longlink*, hỗ trợ chỉ đọc cho mọi biến thể của phần mở rộng *sparse*, bao gồm cả việc khôi phục các tệp sparse.

* hỗ trợ đọc/ghi định dạng POSIX.1-2001 (pax).

* xử lý thư mục, tệp thông thường, hardlink, symbolic link, FIFO, thiết bị ký tự và thiết bị khối, đồng thời có thể lấy và khôi phục thông tin tệp như dấu thời gian, quyền truy cập và chủ sở hữu.

.. versionchanged:: 3.3
   Đã bổ sung hỗ trợ nén :mod:`lzma`.

.. versionchanged:: 3.12
   Các archive được giải nén bằng :ref:`filter <tarfile-extraction-filter>`, cho phép либо giới hạn các tính năng bất ngờ/nguy hiểm, либо xác nhận rằng chúng được mong đợi và archive hoàn toàn đáng tin cậy.

.. versionchanged:: 3.14
   Đặt extraction filter mặc định thành :func:`data <data_filter>`, bộ lọc này không cho phép một số tính năng nguy hiểm, chẳng hạn như liên kết đến đường dẫn tuyệt đối hoặc đường dẫn nằm ngoài đích. Trước đây, chiến lược lọc tương đương với :func:`fully_trusted <fully_trusted_filter>`.

.. versionchanged:: 3.14

   Đã thêm hỗ trợ nén Zstandard bằng :mod:`compression.zstd`.

.. function:: open(name=None, mode='r', fileobj=None, bufsize=10240, **kwargs)

   Trả về một đối tượng :class:`TarFile` cho pathname *name*. Để biết thông tin chi tiết về các đối tượng :class:`TarFile` và các đối số từ khóa được phép, hãy xem :ref:`tarfile-objects`.

   *mode* phải là một chuỗi có dạng ``'filemode[:compression]'``, mặc định là ``'r'``. Sau đây là danh sách đầy đủ các tổ hợp mode:

   +------------------------+--------------------------------------------------------------------------------------------------------------------+
   | mode                   | action                                                                                                             |
   +========================+====================================================================================================================+
   | ``'r'`` hoặc ``'r:*'`` | Mở để đọc với tính năng nén tự động (khuyến nghị).                                                                 |
   +------------------------+--------------------------------------------------------------------------------------------------------------------+
   | ``'r:'``               | Mở chỉ để đọc mà không nén.                                                                                        |
   +------------------------+--------------------------------------------------------------------------------------------------------------------+
   | ``'r:gz'``             | Mở để đọc với tính năng nén gzip.                                                                                  |
   +------------------------+--------------------------------------------------------------------------------------------------------------------+
   | ``'r:bz2'``            | Mở để đọc với tính năng nén bzip2.                                                                                 |
   +------------------------+--------------------------------------------------------------------------------------------------------------------+
   | ``'r:xz'``             | Mở để đọc với tính năng nén lzma.                                                                                  |
   +------------------------+--------------------------------------------------------------------------------------------------------------------+
   | ``'r:zst'``            | Mở để đọc với tính năng nén Zstandard.                                                                             |
   +------------------------+--------------------------------------------------------------------------------------------------------------------+
   | ``'x'`` hoặc ``'x:'``  | Tạo một tarfile chỉ sử dụng chế độ không nén. Phát sinh ngoại lệ :exc:`FileExistsError` nếu tarfile đó đã tồn tại. |
   +------------------------+--------------------------------------------------------------------------------------------------------------------+
   | ``'x:gz'``             | Tạo một tarfile với compression gzip. Phát sinh ngoại lệ :exc:`FileExistsError` nếu tarfile đó đã tồn tại.         |
   +------------------------+--------------------------------------------------------------------------------------------------------------------+
   | ``'x:bz2'``            | Tạo một tarfile với compression bzip2. Phát sinh ngoại lệ :exc:`FileExistsError` nếu tarfile đó đã tồn tại.        |
   +------------------------+--------------------------------------------------------------------------------------------------------------------+
   | ``'x:xz'``             | Tạo một tarfile với compression lzma. Phát sinh ngoại lệ :exc:`FileExistsError` nếu tarfile đó đã tồn tại.         |
   +------------------------+--------------------------------------------------------------------------------------------------------------------+
   | ``'x:zst'``            | Tạo một tarfile với compression Zstandard. Phát sinh ngoại lệ :exc:`FileExistsError` nếu tarfile đó đã tồn tại.    |
   +------------------------+--------------------------------------------------------------------------------------------------------------------+
   | ``'a'`` hoặc ``'a:'``  | Mở để ghi nối tiếp không nén. Tệp sẽ được tạo nếu chưa tồn tại.                                                    |
   +------------------------+--------------------------------------------------------------------------------------------------------------------+
   | ``'w'`` hoặc ``'w:'``  | Mở để ghi không nén.                                                                                               |
   +------------------------+--------------------------------------------------------------------------------------------------------------------+
   | ``'w:gz'``             | Mở để ghi bằng nén gzip.                                                                                           |
   +------------------------+--------------------------------------------------------------------------------------------------------------------+
   | ``'w:bz2'``            | Mở để ghi bằng nén bzip2.                                                                                          |
   +------------------------+--------------------------------------------------------------------------------------------------------------------+
   | ``'w:xz'``             | Mở để ghi bằng nén lzma.                                                                                           |
   +------------------------+--------------------------------------------------------------------------------------------------------------------+
   | ``'w:zst'``            | Mở để ghi bằng nén Zstandard.                                                                                      |
   +------------------------+--------------------------------------------------------------------------------------------------------------------+

   Lưu ý rằng không thể sử dụng ``'a:gz'``, ``'a:bz2'`` hoặc ``'a:xz'``. Nếu *mode* không phù hợp để mở một tệp (đã nén) nhất định ở chế độ đọc,
   :exc:`ReadError` sẽ được phát sinh. Hãy sử dụng *mode* ``'r'`` để tránh điều này. Nếu phương thức nén không được hỗ trợ, :exc:`CompressionError` sẽ được phát sinh.

   Nếu chỉ định *fileobj*, đối tượng này sẽ được sử dụng thay cho một :term:`file object` được mở ở chế độ nhị phân cho *name*. Đối tượng này được cho là đang ở vị trí 0.

   Đối với các mode ``'w:gz'``, ``'x:gz'``, ``'w|gz'``, ``'w:bz2'``, ``'x:bz2'``, ``'w|bz2'``, :func:`tarfile.open` chấp nhận keyword argument *compresslevel* (mặc định là ``9``) để chỉ định mức nén của tệp.

   Đối với các mode ``'w:xz'``, ``'x:xz'`` và ``'w|xz'``, :func:`tarfile.open` chấp nhận keyword argument *preset* để chỉ định mức nén của tệp.

   Đối với các mode ``'w:zst'``, ``'x:zst'`` và ``'w|zst'``, :func:`tarfile.open` chấp nhận keyword argument *level* để chỉ định mức nén của tệp. Cũng có thể truyền keyword argument *options*, cung cấp các tham số nén Zstandard nâng cao được mô tả bởi
   :class:`~compression.zstd.CompressionParameter`. Có thể truyền keyword argument *zstd_dict* để cung cấp một :class:`~compression.zstd.ZstdDict`, tức dictionary Zstandard được sử dụng nhằm cải thiện việc nén các lượng dữ liệu nhỏ hơn.

   Vì các mục đích đặc biệt, có định dạng thứ hai cho *mode*: ``'filemode|[compression]'``. :func:`tarfile.open` sẽ trả về một đối tượng :class:`TarFile` xử lý dữ liệu dưới dạng một stream các khối. Tệp sẽ không được truy cập ngẫu nhiên. Nếu được cung cấp, *fileobj* có thể là bất kỳ đối tượng nào có một
   :meth:`~io.RawIOBase.read` hoặc :meth:`~io.RawIOBase.write` method (tùy thuộc vào *mode*) hoạt động với bytes. *bufsize* chỉ định kích thước khối và mặc định là ``20 * 512`` byte. Sử dụng biến thể này kết hợp với, chẳng hạn như ``sys.stdin.buffer``, một socket
   :term:`file object` hoặc thiết bị băng. Tuy nhiên, một đối tượng :class:`TarFile` như vậy bị giới hạn vì không cho phép truy cập ngẫu nhiên; xem :ref:`tar-examples`. Các mode hiện có:

   +-------------+---------------------------------------------------------------------------+
   | Mode        | Action                                                                    |
   +=============+===========================================================================+
   | ``'r|*'``   | Mở một *stream* các khối tar để đọc với tính năng compression trong suốt. |
   +-------------+---------------------------------------------------------------------------+
   | ``'r|'``    | Mở một *stream* các khối tar không nén để đọc.                            |
   +-------------+---------------------------------------------------------------------------+
   | ``'r|gz'``  | Mở một *stream* được nén bằng gzip để đọc.                                |
   +-------------+---------------------------------------------------------------------------+
   | ``'r|bz2'`` | Mở một *stream* được nén bằng bzip2 để đọc.                               |
   +-------------+---------------------------------------------------------------------------+
   | ``'r|xz'``  | Mở một *stream* được nén bằng lzma để đọc.                                |
   +-------------+---------------------------------------------------------------------------+
   | ``'r|zst'`` | Mở một *stream* được nén bằng Zstandard để đọc.                           |
   +-------------+---------------------------------------------------------------------------+
   | ``'w|'``    | Mở một *stream* không nén để ghi.                                         |
   +-------------+---------------------------------------------------------------------------+
   | ``'w|gz'``  | Mở một *stream* được nén bằng gzip để ghi.                                |
   +-------------+---------------------------------------------------------------------------+
   | ``'w|bz2'`` | Mở một *stream* được nén bằng bzip2 để ghi.                               |
   +-------------+---------------------------------------------------------------------------+
   | ``'w|xz'``  | Mở một *luồng* nén lzma để ghi.                                           |
   +-------------+---------------------------------------------------------------------------+
   | ``'w|zst'`` | Mở một *luồng* nén Zstandard để ghi.                                      |
   +-------------+---------------------------------------------------------------------------+

   .. versionchanged:: 3.5
      Đã bổ sung chế độ ``'x'`` (tạo độc quyền).

   .. versionchanged:: 3.6
      Tham số *name* chấp nhận một :term:`path-like object`.

   .. versionchanged:: 3.12
      Đối số từ khóa *compresslevel* cũng hoạt động với các luồng.

   .. versionchanged:: 3.14
      Đối số từ khóa *preset* cũng hoạt động với các luồng.


.. class:: TarFile
   :noindex:

   Lớp dùng để đọc và ghi các kho lưu trữ tar. Không sử dụng trực tiếp lớp này: thay vào đó, hãy sử dụng :func:`tarfile.open`. Xem :ref:`tarfile-objects`.


.. function:: is_tarfile(name)

   Trả về :const:`True` nếu *name* là một tệp tar archive mà module :mod:`!tarfile` có thể đọc. *name* có thể là một :class:`str`, tệp hoặc đối tượng giống tệp.

   .. versionchanged:: 3.9
      Hỗ trợ các đối tượng tệp và giống tệp.


Module :mod:`!tarfile` định nghĩa các ngoại lệ sau:


.. exception:: TarError

   Lớp cơ sở cho tất cả các ngoại lệ :mod:`!tarfile`.


.. exception:: ReadError

   Được phát sinh khi một tar archive được mở nhưng không thể được xử lý bởi
   module :mod:`!tarfile` hoặc không hợp lệ vì lý do nào đó.


.. exception:: CompressionError

   Được phát sinh khi một phương thức nén không được hỗ trợ hoặc khi dữ liệu không thể được giải mã đúng cách.


.. exception:: StreamError

   Được phát sinh đối với các giới hạn thường gặp ở các đối tượng :class:`TarFile` dạng stream.


.. exception:: ExtractError

   Được phát sinh đối với các lỗi *không nghiêm trọng* khi sử dụng :meth:`TarFile.extract`, nhưng chỉ khi
   :attr:`TarFile.errorlevel`\ ``== 2``.


.. exception:: HeaderError

   Được :meth:`TarInfo.frombuf` phát sinh nếu bộ đệm nhận được không hợp lệ.


.. exception:: FilterError

   Lớp cơ sở cho các mục :ref:`bị bộ lọc từ chối <tarfile-extraction-refuse>`.

   .. attribute:: tarinfo

      Thông tin về mục mà bộ lọc từ chối giải nén, dưới dạng :ref:`TarInfo <tarinfo-objects>`.

.. exception:: AbsolutePathError

   Được phát sinh để từ chối giải nén một mục có đường dẫn tuyệt đối.

.. exception:: OutsideDestinationError

   Được phát sinh để từ chối giải nén một mục nằm ngoài thư mục đích.

.. exception:: SpecialFileError

   Được phát sinh khi từ chối giải nén một tệp đặc biệt (ví dụ: thiết bị hoặc pipe).

.. exception:: AbsoluteLinkError

   Được phát sinh khi từ chối giải nén một symbolic link có đường dẫn tuyệt đối.

.. exception:: LinkOutsideDestinationError

   Được phát sinh khi từ chối giải nén một symbolic link trỏ ra ngoài thư mục đích.

.. exception:: LinkFallbackError

   Được phát sinh khi từ chối mô phỏng một liên kết (cứng hoặc symbolic) bằng cách giải nén một thành viên khác trong archive, khi thành viên đó bị bộ lọc tại vị trí đích từ chối. Ngoại lệ được phát sinh để từ chối thành viên thay thế có sẵn trong :attr:`!BaseException.__context__`.

   .. versionadded:: 3.14


Các hằng số sau có sẵn ở cấp module:

.. data:: ENCODING

   Encoding ký tự mặc định: ``'utf-8'`` trên Windows, giá trị do
   :func:`sys.getfilesystemencoding` trả về trong các trường hợp khác.

.. data:: REGTYPE
          AREGTYPE

   Một tệp thông thường :attr:`~TarInfo.type`.

.. data:: LNKTYPE

   Một liên kết (bên trong tarfile) :attr:`~TarInfo.type`.

.. data:: SYMTYPE

   Một symbolic link :attr:`~TarInfo.type`.

.. data:: CHRTYPE

   Một thiết bị đặc biệt dạng ký tự :attr:`~TarInfo.type`.

.. data:: BLKTYPE

   Một thiết bị đặc biệt dạng khối :attr:`~TarInfo.type`.

.. data:: DIRTYPE

   Một thư mục :attr:`~TarInfo.type`.

.. data:: FIFOTYPE

   Một thiết bị đặc biệt FIFO :attr:`~TarInfo.type`.

.. data:: CONTTYPE

   Một tệp liền mạch :attr:`~TarInfo.type`.

.. data:: GNUTYPE_LONGNAME

   Một longname của GNU tar :attr:`~TarInfo.type`.

.. data:: GNUTYPE_LONGLINK

   Một longlink của GNU tar :attr:`~TarInfo.type`.

.. data:: GNUTYPE_SPARSE

   Một tệp sparse của GNU tar :attr:`~TarInfo.type`.


Mỗi hằng số sau đây xác định một định dạng kho lưu trữ tar mà
mô-đun :mod:`!tarfile` có thể tạo. Xem phần :ref:`tar-formats` để biết chi tiết.


.. data:: USTAR_FORMAT

   Định dạng POSIX.1-1988 (ustar).


.. data:: GNU_FORMAT

   Định dạng GNU tar.


.. data:: PAX_FORMAT

   Định dạng POSIX.1-2001 (pax).


.. data:: DEFAULT_FORMAT

   Định dạng mặc định để tạo các kho lưu trữ. Hiện tại, đây là :const:`PAX_FORMAT`.

   .. versionchanged:: 3.8
      Định dạng mặc định cho các kho lưu trữ mới đã được thay đổi thành
      :const:`PAX_FORMAT` từ :const:`GNU_FORMAT`.


.. seealso::

   Mô-đun :mod:`zipfile`
      Tài liệu về mô-đun tiêu chuẩn :mod:`zipfile`.

   :ref:`archiving-operations`
      Tài liệu về các tiện ích lưu trữ cấp cao hơn do mô-đun tiêu chuẩn :mod:`shutil` cung cấp.

   `Sổ tay GNU tar, Định dạng Tar cơ bản <https://www.gnu.org/software/tar/manual/html_node/Standard.html>`_
      Tài liệu về các tệp lưu trữ tar, bao gồm các phần mở rộng của GNU tar.


.. _tarfile-objects:

Đối tượng TarFile
-----------------

Đối tượng :class:`TarFile` cung cấp giao diện cho một kho lưu trữ tar. Một kho lưu trữ tar là một chuỗi các khối. Một thành viên của kho lưu trữ (một tệp được lưu trữ) gồm một khối tiêu đề theo sau là các khối dữ liệu. Có thể lưu một tệp trong kho lưu trữ tar nhiều lần. Mỗi thành viên của kho lưu trữ được biểu diễn bằng một đối tượng :class:`TarInfo`; xem :ref:`tarinfo-objects` để biết chi tiết.

Có thể sử dụng đối tượng :class:`TarFile` làm context manager trong câu lệnh :keyword:`with`. Đối tượng này sẽ tự động được đóng khi khối lệnh hoàn tất. Lưu ý rằng trong trường hợp xảy ra ngoại lệ, kho lưu trữ được mở để ghi sẽ không được hoàn tất; chỉ đối tượng tệp được sử dụng nội bộ mới được đóng. Xem
:ref:`tar-examples` phần dành cho một trường hợp sử dụng.

.. versionadded:: 3.2
   Đã bổ sung hỗ trợ cho context management protocol.

.. class:: TarFile(name=None, mode='r', fileobj=None, format=DEFAULT_FORMAT, tarinfo=TarInfo, dereference=False, ignore_zeros=False, encoding=ENCODING, errors='surrogateescape', pax_headers=None, debug=0, errorlevel=1, stream=False)

   Tất cả các đối số sau đây đều là tùy chọn và cũng có thể được truy cập dưới dạng thuộc tính của instance.

   *name* là đường dẫn của archive. *name* có thể là một :term:`path-like object`. Có thể bỏ qua đối số này nếu cung cấp *fileobj*. Trong trường hợp đó, thuộc tính :attr:`!name` của đối tượng tệp sẽ được sử dụng nếu thuộc tính này tồn tại.

   *mode* có thể là ``'r'`` để đọc từ một archive hiện có, ``'a'`` để nối dữ liệu vào một tệp hiện có, ``'w'`` để tạo một tệp mới và ghi đè tệp hiện có, hoặc ``'x'`` để chỉ tạo một tệp mới nếu tệp đó chưa tồn tại.

   Nếu cung cấp *fileobj*, đối tượng này sẽ được dùng để đọc hoặc ghi dữ liệu. Nếu xác định được, *mode* sẽ được ghi đè bằng chế độ của *fileobj*. *fileobj* sẽ được sử dụng từ vị trí 0.

   .. note::

      *fileobj* không bị đóng khi :class:`TarFile` được đóng.

   *format* kiểm soát định dạng lưu trữ khi ghi. Nó phải là một trong các hằng số
   :const:`USTAR_FORMAT`, :const:`GNU_FORMAT` hoặc :const:`PAX_FORMAT` được định nghĩa ở cấp mô-đun. Khi đọc, định dạng sẽ được tự động phát hiện, ngay cả khi có nhiều định dạng khác nhau trong cùng một kho lưu trữ.

   Đối số *tarinfo* có thể được dùng để thay thế lớp :class:`TarInfo` mặc định bằng một lớp khác.

   Nếu *dereference* là :const:`False`, hãy thêm các liên kết tượng trưng và liên kết cứng vào kho lưu trữ. Nếu là :const:`True`, hãy thêm nội dung của các tệp đích vào kho lưu trữ. Điều này không có tác dụng trên các hệ thống không hỗ trợ liên kết tượng trưng.

   Nếu *ignore_zeros* là :const:`False`, hãy xem một khối trống là phần kết thúc của kho lưu trữ. Nếu là :const:`True`, hãy bỏ qua các khối trống (và không hợp lệ) rồi cố lấy được nhiều thành viên nhất có thể. Điều này chỉ hữu ích khi đọc các kho lưu trữ được nối hoặc bị hỏng.

   *debug* có thể được đặt từ ``0`` (không có thông báo debug) đến ``3`` (tất cả thông báo debug). Các thông báo được ghi vào ``sys.stderr``.

   *errorlevel* kiểm soát cách xử lý các lỗi khi giải nén, xem :attr:`the corresponding attribute <TarFile.errorlevel>`.

   Các đối số *encoding* và *errors* xác định encoding ký tự được sử dụng để đọc hoặc ghi archive, cũng như cách xử lý các lỗi chuyển đổi. Các thiết lập mặc định sẽ phù hợp với hầu hết người dùng. Xem phần :ref:`tar-unicode` để biết thông tin chuyên sâu.

   Đối số *pax_headers* là một dictionary tùy chọn gồm các chuỗi, được thêm dưới dạng global header pax nếu *format* là :const:`PAX_FORMAT`.

   Nếu *stream* được đặt thành :const:`True`, thì trong khi đọc archive, thông tin về các tệp trong archive sẽ không được lưu vào bộ nhớ đệm, giúp tiết kiệm bộ nhớ.

   .. versionchanged:: 3.2
      Sử dụng ``'surrogateescape'`` làm giá trị mặc định cho đối số *errors*.

   .. versionchanged:: 3.5
      Chế độ ``'x'`` (tạo độc quyền) đã được thêm vào.

   .. versionchanged:: 3.6
      Tham số *name* chấp nhận một :term:`path-like object`.

   .. versionchanged:: 3.13
      Thêm tham số *stream*.

.. classmethod:: TarFile.open(...)

   Hàm khởi tạo thay thế. Hàm :func:`tarfile.open` thực chất là cách viết tắt cho classmethod này.


.. method:: TarFile.getmember(name)

   Trả về một đối tượng :class:`TarInfo` cho thành viên *name*. Nếu không tìm thấy *name* trong archive, :exc:`KeyError` sẽ được ném ra.

   .. note::

      Nếu một thành viên xuất hiện nhiều hơn một lần trong archive, lần xuất hiện cuối cùng được xem là phiên bản cập nhật mới nhất.


.. method:: TarFile.getmembers()

   Trả về các thành viên của archive dưới dạng danh sách các đối tượng :class:`TarInfo`. Danh sách có cùng thứ tự với các thành viên trong archive.


.. method:: TarFile.getnames()

   Trả về các thành viên dưới dạng danh sách tên của chúng. Danh sách này có cùng thứ tự với danh sách được trả về bởi :meth:`getmembers`.


.. method:: TarFile.list(verbose=True, *, members=None)

   In mục lục vào ``sys.stdout``. Nếu *verbose* là :const:`False`, chỉ tên của các thành viên được in. Nếu là :const:`True`, đầu ra tương tự :program:`ls -l` sẽ được tạo ra. Nếu cung cấp *members* tùy chọn, nó phải là tập con của danh sách được trả về bởi :meth:`getmembers`.

   .. versionchanged:: 3.5
      Đã thêm tham số *members*.


.. method:: TarFile.next()

   Trả về thành viên tiếp theo của kho lưu trữ dưới dạng đối tượng :class:`TarInfo`, khi
   :class:`TarFile` được mở để đọc. Trả về :const:`None` nếu không còn thành viên nào.


.. method:: TarFile.extractall(path=".", members=None, *, numeric_owner=False, filter=None)

   Giải nén tất cả thành viên từ kho lưu trữ vào thư mục làm việc hiện tại hoặc thư mục *path*. Nếu cung cấp *members* tùy chọn, nó phải là một tập con của danh sách do :meth:`getmembers` trả về. Thông tin thư mục như chủ sở hữu, thời gian sửa đổi và quyền được thiết lập sau khi tất cả thành viên đã được giải nén. Cách này nhằm khắc phục hai vấn đề: Thời gian sửa đổi của thư mục được đặt lại mỗi khi một tệp được tạo trong đó. Ngoài ra, nếu quyền của thư mục không cho phép ghi, việc giải nén tệp vào đó sẽ thất bại.

   Nếu *numeric_owner* là :const:`True`, các số uid và gid từ tarfile sẽ được dùng để thiết lập chủ sở hữu/nhóm cho các tệp được giải nén. Nếu không, các giá trị dạng tên từ tarfile sẽ được dùng.

   Đối số *filter* chỉ định cách các ``members`` được sửa đổi hoặc từ chối trước khi giải nén. Xem :ref:`tarfile-extraction-filter` để biết chi tiết. Bạn chỉ nên thiết lập rõ ràng đối số này nếu cần các tính năng cụ thể của *tar*, hoặc đặt thành ``filter='data'`` để hỗ trợ các phiên bản Python có giá trị mặc định kém an toàn hơn (3.13 trở xuống).

   .. warning::

      Không bao giờ giải nén kho lưu trữ từ các nguồn không đáng tin cậy mà chưa kiểm tra trước.

      Kể từ Python 3.14, giá trị mặc định (:func:`data <data_filter>`) sẽ ngăn chặn những vấn đề bảo mật nguy hiểm nhất. Tuy nhiên, nó sẽ không ngăn chặn *all* hành vi ngoài ý muốn hoặc không an toàn. Đọc phần :ref:`tarfile-extraction-filter` để biết chi tiết.

   .. versionchanged:: 3.5
      Đã thêm tham số *numeric_owner*.

   .. versionchanged:: 3.6
      Tham số *path* chấp nhận một :term:`path-like object`.

   .. versionchanged:: 3.12
      Đã thêm tham số *filter*.

   .. versionchanged:: 3.14
      Tham số *filter* hiện mặc định là ``'data'``.


.. method:: TarFile.extract(member, path="", set_attrs=True, *, numeric_owner=False, filter=None)

   Trích xuất một thành viên từ kho lưu trữ vào thư mục làm việc hiện tại bằng tên đầy đủ của thành viên đó. Thông tin tệp được trích xuất chính xác nhất có thể. *member* có thể là tên tệp hoặc một đối tượng :class:`TarInfo`. Bạn có thể chỉ định một thư mục khác bằng *path*. *path* có thể là một :term:`path-like object`. Các thuộc tính tệp (chủ sở hữu, mtime, mode) được thiết lập trừ khi *set_attrs* là false.

   Các đối số *numeric_owner* và *filter* giống như đối số của :meth:`extractall`.

   .. note::

      Phương thức :meth:`extract` không xử lý một số vấn đề khi trích xuất. Trong hầu hết các trường hợp, bạn nên cân nhắc sử dụng phương thức :meth:`extractall`.

   .. warning::

      Không bao giờ giải nén các archive từ nguồn không đáng tin cậy nếu chưa kiểm tra trước. Xem cảnh báo về :meth:`extractall` để biết chi tiết.

   .. versionchanged:: 3.2
      Đã thêm tham số *set_attrs*.

   .. versionchanged:: 3.5
      Đã thêm tham số *numeric_owner*.

   .. versionchanged:: 3.6
      Tham số *path* chấp nhận một :term:`path-like object`.

   .. versionchanged:: 3.12
      Đã thêm tham số *filter*.


.. method:: TarFile.extractfile(member)

   Trích xuất một thành viên từ archive dưới dạng file object. *member* có thể là tên tệp hoặc một đối tượng :class:`TarInfo`. Nếu *member* là tệp thông thường hoặc liên kết, một đối tượng :class:`io.BufferedReader` sẽ được trả về. Với tất cả các thành viên hiện có khác, :const:`None` được trả về. Nếu *member* không xuất hiện trong archive, :exc:`KeyError` sẽ được nêu.

   .. versionchanged:: 3.3
      Trả về một đối tượng :class:`io.BufferedReader`.

   .. versionchanged:: 3.13
      Đối tượng :class:`io.BufferedReader` được trả về có thuộc tính :attr:`!mode`, luôn bằng ``'rb'``.

.. attribute:: TarFile.errorlevel
   :type: int

   Nếu *errorlevel* là ``0``, các lỗi sẽ bị bỏ qua khi sử dụng :meth:`TarFile.extract` và :meth:`TarFile.extractall`. Tuy nhiên, chúng xuất hiện dưới dạng thông báo lỗi trong đầu ra gỡ lỗi khi *debug* lớn hơn 0. Nếu ``1`` (giá trị mặc định), tất cả các lỗi *fatal* đều được phát sinh dưới dạng :exc:`OSError` hoặc
   :exc:`FilterError` ngoại lệ. Nếu ``2``, tất cả các lỗi *non-fatal* cũng được phát sinh dưới dạng ngoại lệ :exc:`TarError`.

   Một số ngoại lệ, chẳng hạn như các ngoại lệ do kiểu đối số không đúng hoặc dữ liệu bị hỏng, luôn được phát sinh.

   Các :ref:`extraction filters <tarfile-extraction-filter>` tùy chỉnh nên phát sinh :exc:`FilterError` đối với các lỗi *fatal* và :exc:`ExtractError` đối với các lỗi *non-fatal*.

   Lưu ý rằng khi một ngoại lệ được phát sinh, kho lưu trữ có thể đã được giải nén một phần. Người dùng có trách nhiệm dọn dẹp.

.. attribute:: TarFile.extraction_filter

   .. versionadded:: 3.12

   :ref:`extraction filter <tarfile-extraction-filter>` được sử dụng làm giá trị mặc định cho đối số *filter* của :meth:`~TarFile.extract` và :meth:`~TarFile.extractall`.

   Thuộc tính này có thể là ``None`` hoặc một callable. Không cho phép tên chuỗi đối với thuộc tính này, không giống như đối số *filter* của :meth:`~TarFile.extract`.

   Nếu ``extraction_filter`` là ``None`` (giá trị mặc định), các phương thức extraction sẽ mặc định sử dụng bộ lọc :func:`data <data_filter>`.

   Có thể đặt thuộc tính này trên các instance hoặc ghi đè trong các subclass. Bạn cũng có thể đặt thuộc tính này trên chính lớp ``TarFile`` để thiết lập giá trị mặc định trên toàn cục. Tuy nhiên, vì nó ảnh hưởng đến mọi lần sử dụng *tarfile*, cách tốt nhất là chỉ thực hiện việc này trong các ứng dụng cấp cao nhất hoặc
   :mod:`site configuration <site>`. Để thiết lập giá trị mặc định trên toàn cục theo cách này, cần bọc một hàm filter trong
   :deco:`staticmethod` để ngăn việc chèn một đối số ``self``.

   .. versionchanged:: 3.14

      Bộ lọc mặc định được đặt thành :func:`data <data_filter>`, bộ lọc này không cho phép một số tính năng nguy hiểm, chẳng hạn như liên kết đến các đường dẫn tuyệt đối hoặc các đường dẫn nằm ngoài đích. Trước đây, giá trị mặc định tương đương với
      :func:`fully_trusted <fully_trusted_filter>`.

.. method:: TarFile.add(name, arcname=None, recursive=True, *, filter=None)

   Thêm tệp *name* vào archive. *name* có thể là bất kỳ loại tệp nào (thư mục, fifo, symbolic link, v.v.). Nếu được cung cấp, *arcname* chỉ định một tên thay thế cho tệp trong archive. Theo mặc định, các thư mục được thêm đệ quy. Có thể tránh điều này bằng cách đặt *recursive* thành
   :const:`False`. Việc đệ quy thêm các mục theo thứ tự đã sắp xếp. Nếu cung cấp *filter*, thì đó phải là một hàm nhận đối số là đối tượng :class:`TarInfo` và trả về đối tượng :class:`TarInfo` đã thay đổi. Nếu thay vào đó hàm trả về
   :const:`None` đối tượng :class:`TarInfo` sẽ bị loại khỏi archive. Xem :ref:`tar-examples` để biết ví dụ.

   .. versionchanged:: 3.2
      Đã thêm tham số *filter*.

   .. versionchanged:: 3.7
      Việc đệ quy thêm các mục theo thứ tự đã sắp xếp.


.. method:: TarFile.addfile(tarinfo, fileobj=None)

   Thêm đối tượng :class:`TarInfo` *tarinfo* vào archive. Nếu *tarinfo* đại diện cho một tệp thông thường có kích thước khác 0, đối số *fileobj* phải là một :term:`binary file`, và ``tarinfo.size`` byte sẽ được đọc từ đó rồi thêm vào archive. Bạn có thể tạo trực tiếp các đối tượng :class:`TarInfo`, hoặc sử dụng :meth:`gettarinfo`.

   .. versionchanged:: 3.13

      Phải cung cấp *fileobj* cho các tệp thông thường có kích thước khác 0.


.. method:: TarFile.gettarinfo(name=None, arcname=None, fileobj=None)

   Tạo một đối tượng :class:`TarInfo` từ kết quả của :func:`os.stat` hoặc tương đương trên một tệp hiện có. Tệp được đặt tên bằng *name*, hoặc được chỉ định dưới dạng :term:`file object` *fileobj* có file descriptor. *name* có thể là một :term:`path-like object`. Nếu được cung cấp, *arcname* chỉ định một tên thay thế cho tệp trong archive; nếu không, tên được lấy từ *fileobj*’s
   thuộc tính :attr:`~io.FileIO.name`, hoặc đối số *name*. Tên này phải là một chuỗi văn bản.

   Bạn có thể sửa đổi một số thuộc tính của :class:`TarInfo` trước khi thêm nó bằng :meth:`addfile`. Nếu đối tượng tệp không phải là một đối tượng tệp thông thường được định vị ở đầu tệp, bạn có thể cần sửa đổi các thuộc tính như :attr:`~TarInfo.size`. Điều này áp dụng cho các đối tượng như :class:`~gzip.GzipFile`. Bạn cũng có thể sửa đổi :attr:`~TarInfo.name`, trong trường hợp đó *arcname* có thể là một chuỗi giả.

   .. versionchanged:: 3.6
      Tham số *name* chấp nhận một :term:`path-like object`.


.. method:: TarFile.close()

   Đóng :class:`TarFile`. Ở chế độ ghi, hai khối số 0 kết thúc được nối vào archive.


.. attribute:: TarFile.pax_headers
   :type: dict

   Một dictionary chứa các cặp khóa-giá trị của các global header pax.



.. _tarinfo-objects:

Đối tượng TarInfo
-----------------

Một đối tượng :class:`TarInfo` đại diện cho một thành viên trong :class:`TarFile`. Ngoài việc lưu trữ tất cả các thuộc tính bắt buộc của một tệp (chẳng hạn như loại tệp, kích thước, thời gian, quyền, chủ sở hữu, v.v.), đối tượng này cung cấp một số phương thức hữu ích để xác định loại của nó. Đối tượng này *không* chứa dữ liệu của tệp.

Các đối tượng :class:`TarInfo` được trả về bởi các phương thức của :class:`TarFile`
:meth:`~TarFile.getmember`, :meth:`~TarFile.getmembers` và
:meth:`~TarFile.gettarinfo`.

Việc sửa đổi các đối tượng được :meth:`~TarFile.getmember` trả về hoặc
:meth:`~TarFile.getmembers` sẽ ảnh hưởng đến tất cả các thao tác tiếp theo trên archive. Trong những trường hợp không mong muốn điều này, bạn có thể sử dụng :mod:`copy.copy() <copy>` hoặc gọi phương thức :meth:`~TarInfo.replace` để tạo một bản sao đã sửa đổi chỉ trong một bước.

Có thể đặt một số thuộc tính thành ``None`` để cho biết một phần metadata không được sử dụng hoặc không xác định. Các phương thức :class:`TarInfo` khác nhau xử lý ``None`` theo những cách khác nhau:

- Các phương thức :meth:`~TarFile.extract` hoặc :meth:`~TarFile.extractall` sẽ bỏ qua metadata tương ứng, giữ nguyên giá trị mặc định cho metadata đó.
- :meth:`~TarFile.addfile` sẽ thất bại.
- :meth:`~TarFile.list` sẽ in một chuỗi giữ chỗ.

.. class:: TarInfo(name="")

   Tạo một đối tượng :class:`TarInfo`.


.. classmethod:: TarInfo.frombuf(buf, encoding, errors)

   Tạo và trả về một đối tượng :class:`TarInfo` từ bộ đệm chuỗi *buf*.

   Phát sinh :exc:`HeaderError` nếu bộ đệm không hợp lệ.


.. classmethod:: TarInfo.fromtarfile(tarfile)

   Đọc thành viên tiếp theo từ đối tượng :class:`TarFile` *tarfile* và trả về thành viên đó dưới dạng đối tượng :class:`TarInfo`.


.. method:: TarInfo.tobuf(format=DEFAULT_FORMAT, encoding=ENCODING, errors='surrogateescape')

   Tạo một bộ đệm chuỗi từ đối tượng :class:`TarInfo`. Để biết thông tin về các đối số, hãy xem hàm khởi tạo của lớp :class:`TarFile`.

   .. versionchanged:: 3.2
      Sử dụng ``'surrogateescape'`` làm giá trị mặc định cho đối số *errors*.


Một đối tượng ``TarInfo`` có các thuộc tính dữ liệu công khai sau:


.. attribute:: TarInfo.name
   :type: str

   Tên của thành viên trong kho lưu trữ.


.. attribute:: TarInfo.size
   :type: int

   Kích thước tính bằng byte.


.. attribute:: TarInfo.mtime
   :type: int | float

   Thời điểm sửa đổi lần cuối tính bằng giây kể từ :ref:`epoch <epoch>`, như trong :attr:`os.stat_result.st_mtime`.

   .. versionchanged:: 3.12

      Có thể được đặt thành ``None`` cho :meth:`~TarFile.extract` và
      :meth:`~TarFile.extractall`, khiến quá trình trích xuất bỏ qua việc áp dụng thuộc tính này.

.. attribute:: TarInfo.mode
   :type: int

   Các bit quyền, như đối với :func:`os.chmod`.

   .. versionchanged:: 3.12

      Có thể được đặt thành ``None`` cho :meth:`~TarFile.extract` và
      :meth:`~TarFile.extractall`, khiến quá trình trích xuất bỏ qua việc áp dụng thuộc tính này.

.. attribute:: TarInfo.type

   Loại tệp.  *type* thường là một trong các hằng số sau: :const:`REGTYPE`,
   :const:`AREGTYPE`, :const:`LNKTYPE`, :const:`SYMTYPE`, :const:`DIRTYPE`,
   :const:`FIFOTYPE`, :const:`CONTTYPE`, :const:`CHRTYPE`, :const:`BLKTYPE`,
   :const:`GNUTYPE_SPARSE`.  Để xác định loại đối tượng :class:`TarInfo` thuận tiện hơn, hãy sử dụng các phương thức ``is*()`` bên dưới.


.. attribute:: TarInfo.linkname
   :type: str

   Tên của tệp đích, chỉ xuất hiện trong các đối tượng :class:`TarInfo` thuộc loại :const:`LNKTYPE` và :const:`SYMTYPE`.

   Đối với các symbolic link (``SYMTYPE``), *linkname* là đường dẫn tương đối so với thư mục chứa liên kết. Đối với các hard link (``LNKTYPE``), *linkname* là đường dẫn tương đối so với thư mục gốc của archive.


.. attribute:: TarInfo.uid
   :type: int

   ID người dùng của người dùng đã lưu mục này ban đầu.

   .. versionchanged:: 3.12

      Có thể được đặt thành ``None`` cho :meth:`~TarFile.extract` và
      :meth:`~TarFile.extractall`, khiến quá trình trích xuất bỏ qua việc áp dụng thuộc tính này.

.. attribute:: TarInfo.gid
   :type: int

   ID nhóm của người dùng đã lưu thành viên này ban đầu.

   .. versionchanged:: 3.12

      Có thể được đặt thành ``None`` cho :meth:`~TarFile.extract` và
      :meth:`~TarFile.extractall`, khiến quá trình trích xuất bỏ qua việc áp dụng thuộc tính này.

.. attribute:: TarInfo.uname
   :type: str

   Tên người dùng.

   .. versionchanged:: 3.12

      Có thể được đặt thành ``None`` cho :meth:`~TarFile.extract` và
      :meth:`~TarFile.extractall`, khiến quá trình trích xuất bỏ qua việc áp dụng thuộc tính này.

.. attribute:: TarInfo.gname
   :type: str

   Tên nhóm.

   .. versionchanged:: 3.12

      Có thể được đặt thành ``None`` cho :meth:`~TarFile.extract` và
      :meth:`~TarFile.extractall`, khiến quá trình trích xuất bỏ qua việc áp dụng thuộc tính này.

.. attribute:: TarInfo.chksum
   :type: int

   Checksum của header.


.. attribute:: TarInfo.devmajor
   :type: int

   Số major của thiết bị.


.. attribute:: TarInfo.devminor
   :type: int

   Số minor của thiết bị.


.. attribute:: TarInfo.offset
   :type: int

   Phần header tar bắt đầu tại đây.


.. attribute:: TarInfo.offset_data
   :type: int

   Dữ liệu của tệp bắt đầu tại đây.


.. attribute:: TarInfo.sparse

   Thông tin về member thưa.


.. attribute:: TarInfo.pax_headers
   :type: dict

   Một dictionary chứa các cặp key-value của extended header pax liên kết.

.. method:: TarInfo.replace(name=..., mtime=..., mode=..., linkname=..., \
                            uid=..., gid=..., uname=..., gname=..., \ deep=True)

   .. versionadded:: 3.12

   Trả về một bản sao *new* của đối tượng :class:`!TarInfo` với các thuộc tính đã cho được thay đổi. Ví dụ, để trả về một ``TarInfo`` với tên group được đặt thành ``'staff'``, hãy dùng::

       new_tarinfo = old_tarinfo.replace(gname='staff')

   Theo mặc định, một bản sao sâu được tạo. Nếu *deep* là false, bản sao sẽ là bản sao nông, tức là ``pax_headers`` và mọi thuộc tính tùy chỉnh được dùng chung với đối tượng ``TarInfo`` ban đầu.

Một đối tượng :class:`TarInfo` cũng cung cấp một số phương thức truy vấn tiện lợi:


.. method:: TarInfo.isfile()

   Trả về :const:`True` nếu đối tượng :class:`TarInfo` là một tệp thông thường.


.. method:: TarInfo.isreg()

   Giống như :meth:`isfile`.


.. method:: TarInfo.isdir()

   Trả về :const:`True` nếu đó là một thư mục.


.. method:: TarInfo.issym()

   Trả về :const:`True` nếu đó là một symbolic link.


.. method:: TarInfo.islnk()

   Trả về :const:`True` nếu đó là một hard link.


.. method:: TarInfo.ischr()

   Trả về :const:`True` nếu đó là một character device.


.. method:: TarInfo.isblk()

   Trả về :const:`True` nếu đó là thiết bị khối.


.. method:: TarInfo.isfifo()

   Trả về :const:`True` nếu đó là FIFO.


.. method:: TarInfo.isdev()

   Trả về :const:`True` nếu đó là thiết bị ký tự, thiết bị khối hoặc FIFO.


.. _tarfile-extraction-filter:

Bộ lọc giải nén
---------------

.. versionadded:: 3.12

Định dạng *tar* được thiết kế để nắm bắt mọi chi tiết của một hệ thống tệp tương tự UNIX, khiến nó rất mạnh mẽ. Đáng tiếc là các tính năng này khiến việc tạo các tệp tar có những tác động ngoài ý muốn -- và có thể là độc hại -- khi được giải nén trở nên dễ dàng. Ví dụ: việc giải nén một tệp tar có thể ghi đè các tệp tùy ý theo nhiều cách (chẳng hạn như sử dụng đường dẫn tuyệt đối, các thành phần đường dẫn ``..``, hoặc các symlink ảnh hưởng đến những thành viên tiếp theo).

Trong hầu hết trường hợp, không cần đến đầy đủ chức năng. Vì vậy, *tarfile* hỗ trợ các bộ lọc giải nén: một cơ chế để giới hạn chức năng và qua đó giảm thiểu một số vấn đề bảo mật.

.. warning::

   Không có bộ lọc nào hiện có thể chặn *tất cả* các tính năng nguy hiểm của kho lưu trữ. Không bao giờ giải nén các kho lưu trữ từ những nguồn không đáng tin cậy mà chưa kiểm tra trước. Xem thêm :ref:`tarfile-further-verification`.

.. seealso::

   :pep:`706`
      Chứa thêm động cơ và lý do đằng sau thiết kế.

Đối số *filter* của :meth:`TarFile.extract` hoặc :meth:`~TarFile.extractall` có thể là:

* chuỗi ``'fully_trusted'``: Tôn trọng toàn bộ siêu dữ liệu như được chỉ định trong archive. Nên sử dụng nếu người dùng hoàn toàn tin tưởng archive hoặc tự triển khai quy trình xác minh phức tạp.

* chuỗi ``'tar'``: Tôn trọng hầu hết các tính năng dành riêng cho *tar* (tức là các tính năng của hệ thống tệp tương tự UNIX), nhưng chặn những tính năng rất có khả năng gây bất ngờ hoặc độc hại. Xem :func:`tar_filter` để biết chi tiết.

* chuỗi ``'data'``: Bỏ qua hoặc chặn hầu hết các tính năng dành riêng cho hệ thống tệp tương tự UNIX. Dành cho việc giải nén các archive dữ liệu đa nền tảng. Xem :func:`data_filter` để biết chi tiết.

* ``None`` (mặc định): Sử dụng :attr:`TarFile.extraction_filter`.

  Nếu giá trị đó cũng là ``None`` (mặc định), filter ``'data'`` sẽ được sử dụng.

   .. versionchanged:: 3.14

      Bộ lọc mặc định được đặt thành :func:`data <data_filter>`. Trước đây, giá trị mặc định tương đương với
      :func:`fully_trusted <fully_trusted_filter>`.

* Một callable sẽ được gọi cho từng member được trích xuất với một
  :ref:`TarInfo <tarinfo-objects>` mô tả member và đường dẫn đích nơi archive được trích xuất (tức là cùng một đường dẫn được sử dụng cho tất cả member)::

      filter(member: TarInfo, path: str, /) -> TarInfo | None

  Callable được gọi ngay trước khi từng member được trích xuất, vì vậy nó có thể xem xét trạng thái hiện tại của disk. Callable có thể:

  - trả về một object :class:`TarInfo` sẽ được sử dụng thay cho metadata trong archive, hoặc
  - trả về ``None``, trong trường hợp đó member sẽ bị bỏ qua, hoặc
  - phát sinh một exception để hủy operation hoặc bỏ qua member, tùy thuộc vào :attr:`~TarFile.errorlevel`. Lưu ý rằng khi việc trích xuất bị hủy, :meth:`~TarFile.extractall` có thể khiến archive chỉ được trích xuất một phần. Nó không cố gắng dọn dẹp.

Các bộ lọc có tên mặc định
~~~~~~~~~~~~~~~~~~~~~~~~~~

Các bộ lọc có tên được định nghĩa sẵn khả dụng dưới dạng các hàm, vì vậy chúng có thể được sử dụng lại trong các bộ lọc tùy chỉnh:

.. function:: fully_trusted_filter(member, path)

   Trả về *member* không thay đổi.

   Điều này triển khai bộ lọc ``'fully_trusted'``.

.. function:: tar_filter(member, path)

  Triển khai bộ lọc ``'tar'``.

  - Loại bỏ các dấu gạch chéo ở đầu (``/`` và :data:`os.sep`) khỏi tên tệp.
  - :ref:`Từ chối <tarfile-extraction-refuse>` trích xuất các tệp có đường dẫn tuyệt đối (trong trường hợp tên vẫn là tuyệt đối ngay cả sau khi loại bỏ dấu gạch chéo, chẳng hạn như ``C:/foo`` trên Windows). Điều này phát sinh :class:`~tarfile.AbsolutePathError`.
  - Chuẩn hóa tên tệp (:attr:`TarInfo.name`) chứa các thành phần ``..`` bằng :func:`os.path.normpath`. Lưu ý rằng thao tác này loại bỏ các thành phần ``..`` bên trong, điều này có thể làm thay đổi ý nghĩa của tên nếu tên đó đi qua các liên kết tượng trưng.
  - :ref:`Từ chối <tarfile-extraction-refuse>` trích xuất các tệp có đường dẫn tuyệt đối (sau khi đi theo các liên kết tượng trưng) sẽ kết thúc bên ngoài đích. Thao tác này gây ra :class:`~tarfile.OutsideDestinationError`.
  - Xóa các bit mode cấp cao (setuid, setgid, sticky) và các bit ghi của group/other (:const:`~stat.S_IWGRP` | :const:`~stat.S_IWOTH`).

  Trả về thành viên ``TarInfo`` đã sửa đổi.

  .. versionchanged:: 3.14.8

     Các tên tệp chứa các thành phần ``..`` hiện đã được chuẩn hóa.

.. function:: data_filter(member, path)

  Triển khai bộ lọc ``'data'``. Ngoài những gì ``tar_filter`` thực hiện:

  - Chuẩn hóa các đích liên kết (:attr:`TarInfo.linkname`) bằng
    :func:`os.path.normpath`. Lưu ý rằng thao tác này loại bỏ các thành phần ``..`` nội bộ, điều này có thể làm thay đổi ý nghĩa của liên kết nếu đường dẫn trong :attr:`!TarInfo.linkname` đi qua các liên kết tượng trưng.

  - :ref:`Refuse <tarfile-extraction-refuse>` để từ chối trích xuất các liên kết (cứng hoặc mềm) liên kết đến các đường dẫn tuyệt đối hoặc liên kết ra ngoài đích.

    Điều này gây ra :class:`~tarfile.AbsoluteLinkError` hoặc
    :class:`~tarfile.LinkOutsideDestinationError`.

    Lưu ý rằng các tệp như vậy sẽ bị từ chối ngay cả trên những nền tảng không hỗ trợ liên kết tượng trưng.

  - :ref:`Refuse <tarfile-extraction-refuse>` để từ chối trích xuất các tệp thiết bị (bao gồm cả pipe). Điều này gây ra :class:`~tarfile.SpecialFileError`.

  - Đối với các tệp thông thường, bao gồm cả liên kết cứng:

    - Đặt quyền đọc và ghi cho chủ sở hữu (:const:`~stat.S_IRUSR` | :const:`~stat.S_IWUSR`).
    - Xóa quyền thực thi của nhóm và các đối tượng khác (:const:`~stat.S_IXGRP` | :const:`~stat.S_IXOTH`) nếu chủ sở hữu không có quyền đó (:const:`~stat.S_IXUSR`).

  - Đối với các tệp khác (thư mục), đặt ``mode`` thành ``None``, để các phương thức trích xuất bỏ qua việc áp dụng các bit quyền.
  - Đặt thông tin người dùng và nhóm (``uid``, ``gid``, ``uname``, ``gname``) thành ``None``, để các phương thức trích xuất bỏ qua việc thiết lập thông tin này.

  Trả về thành viên ``TarInfo`` đã sửa đổi.

  Lưu ý rằng bộ lọc này không chặn *tất cả* các tính năng lưu trữ nguy hiểm. Xem :ref:`tarfile-further-verification` để biết chi tiết.

  .. versionchanged:: 3.14

     Các đích liên kết hiện đã được chuẩn hóa.


.. _tarfile-extraction-refuse:

Lỗi bộ lọc
~~~~~~~~~~

Khi một filter từ chối giải nén một tệp, nó sẽ đưa ra một exception thích hợp, là lớp con của :class:`~tarfile.FilterError`. Thao tác này sẽ hủy quá trình giải nén nếu :attr:`TarFile.errorlevel` là 1 trở lên. Với ``errorlevel=0``, lỗi sẽ được ghi vào log và member sẽ bị bỏ qua, nhưng quá trình giải nén vẫn tiếp tục.


.. _tarfile-further-verification:

Gợi ý để kiểm tra thêm
~~~~~~~~~~~~~~~~~~~~~~

Ngay cả khi có ``filter='data'``, *tarfile* vẫn không phù hợp để giải nén các tệp không đáng tin cậy mà chưa kiểm tra trước. Trong số các vấn đề khác, những filter được định nghĩa sẵn không ngăn chặn các cuộc tấn công từ chối dịch vụ. Người dùng nên thực hiện thêm các bước kiểm tra.

Dưới đây là danh sách chưa đầy đủ những điều cần cân nhắc:

* Giải nén vào một :func:`new temporary directory <tempfile.mkdtemp>` để ngăn việc khai thác, chẳng hạn như thông qua các liên kết có sẵn, đồng thời giúp dễ dàng dọn dẹp hơn sau khi quá trình giải nén thất bại.
* Không cho phép symbolic link nếu bạn không cần chức năng này.
* Khi làm việc với dữ liệu không đáng tin cậy, hãy sử dụng các giới hạn bên ngoài (chẳng hạn như ở cấp độ hệ điều hành) đối với việc sử dụng ổ đĩa, bộ nhớ và CPU.
* Kiểm tra tên tệp dựa trên danh sách ký tự được cho phép (để lọc các ký tự điều khiển, ký tự dễ gây nhầm lẫn, dấu phân cách đường dẫn ngoại lai, v.v.).
* Kiểm tra để bảo đảm tên tệp có phần mở rộng như dự kiến (không khuyến khích các tệp được thực thi khi bạn “bấm vào chúng”, hoặc các tệp không có phần mở rộng như tên thiết bị đặc biệt của Windows).
* Giới hạn số lượng tệp được giải nén, tổng kích thước dữ liệu được giải nén, độ dài tên tệp (bao gồm cả độ dài symlink) và kích thước của từng tệp.
* Kiểm tra các tệp có thể bị che khuất trên các filesystem không phân biệt chữ hoa chữ thường.

Cũng lưu ý rằng:

* Các tệp Tar có thể chứa nhiều phiên bản của cùng một tệp. Những phiên bản xuất hiện sau được cho là sẽ ghi đè lên các phiên bản trước đó. Tính năng này rất quan trọng để cho phép cập nhật các tape archive, nhưng có thể bị lạm dụng với mục đích xấu.
* *tarfile* không bảo vệ trước các vấn đề với dữ liệu “trực tiếp”, chẳng hạn như kẻ tấn công can thiệp vào thư mục đích (hoặc thư mục nguồn) trong khi quá trình giải nén (hoặc lưu trữ) đang diễn ra.


Hỗ trợ các phiên bản Python cũ hơn
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Các bộ lọc trích xuất được thêm vào Python 3.12, nhưng có thể được backport sang các phiên bản cũ hơn dưới dạng bản cập nhật bảo mật. Để kiểm tra xem tính năng này có khả dụng hay không, hãy sử dụng ví dụ như ``hasattr(tarfile, 'data_filter')`` thay vì kiểm tra phiên bản Python.

Các ví dụ sau đây cho thấy cách hỗ trợ các phiên bản Python có và không có tính năng này. Lưu ý rằng việc đặt ``extraction_filter`` sẽ ảnh hưởng đến mọi thao tác tiếp theo.

* Kho lưu trữ hoàn toàn đáng tin cậy::

    my_tarfile.extraction_filter = (lambda member, path: member)
    my_tarfile.extractall()

* Sử dụng bộ lọc ``'data'`` nếu khả dụng, nhưng quay lại hành vi của Python 3.11 (``'fully_trusted'``) nếu tính năng này không khả dụng::

    my_tarfile.extraction_filter = getattr(tarfile, 'data_filter',
                                           (lambda member, path: member))
    my_tarfile.extractall()

* Sử dụng bộ lọc ``'data'``; *fail* nếu bộ lọc không khả dụng::

    my_tarfile.extractall(filter=tarfile.data_filter)

  or::

    my_tarfile.extraction_filter = tarfile.data_filter
    my_tarfile.extractall()

* Sử dụng bộ lọc ``'data'``; *warn* nếu bộ lọc không khả dụng::

   if hasattr(tarfile, 'data_filter'):
       my_tarfile.extractall(filter='data')
   else:
       # xóa mục này khi không còn cần thiết
       warn_the_user('Extracting may be unsafe; consider updating Python')
       my_tarfile.extractall()


Ví dụ về bộ lọc trích xuất có trạng thái
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Mặc dù các phương thức trích xuất của *tarfile*'s nhận một callable *filter* đơn giản, các bộ lọc tùy chỉnh có thể là những đối tượng phức tạp hơn với trạng thái nội bộ. Có thể sẽ hữu ích nếu viết chúng dưới dạng context manager để sử dụng như sau::

    with StatefulFilter() as filter_func:
        tar.extractall(path, filter=filter_func)

Ví dụ, có thể viết một bộ lọc như vậy như sau::

    class StatefulFilter:
        def __init__(self):
            self.file_count = 0

        def __enter__(self):
            return self

        def __call__(self, member, path):
            self.file_count += 1
            return member

        def __exit__(self, *exc_info):
            print(f'{self.file_count} files extracted')


.. _tarfile-commandline:
.. program:: tarfile


Giao diện dòng lệnh
-------------------

.. versionadded:: 3.4

Mô-đun :mod:`!tarfile` cung cấp một giao diện dòng lệnh đơn giản để tương tác với các tar archive.

Nếu muốn tạo một tar archive mới, hãy chỉ định tên của nó sau tùy chọn :option:`-c` rồi liệt kê (các) tên tệp cần đưa vào:

.. code-block:: shell-session

    $ python -m tarfile -c monty.tar  spam.txt eggs.txt

Truyền một thư mục cũng được chấp nhận:

.. code-block:: shell-session

    $ python -m tarfile -c monty.tar life-of-brian_1979/

Nếu muốn giải nén một tar archive vào thư mục hiện tại, hãy sử dụng tùy chọn :option:`-e`:

.. code-block:: shell-session

    $ python -m tarfile -e monty.tar

Bạn cũng có thể giải nén một tar archive vào một thư mục khác bằng cách truyền tên thư mục đó:

.. code-block:: shell-session

    $ python -m tarfile -e monty.tar  other-dir/

Để liệt kê các tệp trong một tar archive, hãy sử dụng tùy chọn :option:`-l`:

.. code-block:: shell-session

    $ python -m tarfile -l monty.tar


Tùy chọn dòng lệnh
~~~~~~~~~~~~~~~~~~

.. option:: -l <tarfile>
            --list <tarfile>

   Liệt kê các tệp trong tarfile.

.. option:: -c <tarfile> <source1> ... <sourceN>
            --create <tarfile> <source1> ... <sourceN>

   Tạo tarfile từ các tệp nguồn.

.. option:: -e <tarfile> [<output_dir>]
            --extract <tarfile> [<output_dir>]

   Giải nén tarfile vào thư mục hiện tại nếu không chỉ định *output_dir*.

.. option:: -t <tarfile>
            --test <tarfile>

   Kiểm tra tarfile có hợp lệ hay không.

.. option:: -v, --verbose

   Đầu ra chi tiết.

.. option:: --filter <filtername>

   Chỉ định *filter* cho ``--extract``. Xem :ref:`tarfile-extraction-filter` để biết chi tiết. Chỉ chấp nhận tên chuỗi (tức là ``fully_trusted``, ``tar`` và ``data``).

.. _tar-examples:

Ví dụ
-----

Ví dụ về cách đọc
~~~~~~~~~~~~~~~~~

Cách giải nén toàn bộ kho lưu trữ tar vào thư mục làm việc hiện tại::

   import tarfile
   tar = tarfile.open("sample.tar.gz")
   tar.extractall(filter='data')
   tar.close()

Cách giải nén một phần kho lưu trữ tar bằng :meth:`TarFile.extractall` sử dụng hàm generator thay vì một danh sách::

   import os
   import tarfile

   def py_files(members):
       for tarinfo in members:
           if os.path.splitext(tarinfo.name)[1] == ".py":
               yield tarinfo

   tar = tarfile.open("sample.tar.gz")
   tar.extractall(members=py_files(tar))
   tar.close()

Cách đọc kho lưu trữ tar được nén bằng gzip và hiển thị thông tin về một số thành viên::

   import tarfile
   tar = tarfile.open("sample.tar.gz", "r:gz")
   for tarinfo in tar:
       print(tarinfo.name, "is", tarinfo.size, "bytes in size and is ", end="")
       if tarinfo.isreg():
           print("a regular file.")
       elif tarinfo.isdir():
           print("a directory.")
       else:
           print("something else.")
   tar.close()

Ví dụ về cách ghi
~~~~~~~~~~~~~~~~~

Cách tạo một tar archive không nén từ danh sách tên tệp::

   import tarfile
   tar = tarfile.open("sample.tar", "w")
   for name in ["foo", "bar", "quux"]:
       tar.add(name)
   tar.close()

Ví dụ tương tự sử dụng câu lệnh :keyword:`with`::

    import tarfile
    with tarfile.open("sample.tar", "w") as tar:
        for name in ["foo", "bar", "quux"]:
            tar.add(name)

Cách tạo và ghi một archive vào stdout bằng cách sử dụng
:data:`sys.stdout.buffer <sys.stdout>` trong tham số *fileobj* của :meth:`TarFile.add`::

    import sys
    import tarfile
    with tarfile.open("sample.tar.gz", "w|gz", fileobj=sys.stdout.buffer) as tar:
        for name in ["foo", "bar", "quux"]:
            tar.add(name)

Cách tạo một archive và đặt lại thông tin người dùng bằng tham số *filter* trong :meth:`TarFile.add`::

    import tarfile
    def reset(tarinfo):
        tarinfo.uid = tarinfo.gid = 0
        tarinfo.uname = tarinfo.gname = "root"
        return tarinfo
    tar = tarfile.open("sample.tar.gz", "w:gz")
    tar.add("foo", filter=reset)
    tar.close()


.. _tar-formats:

Các định dạng tar được hỗ trợ
-----------------------------

Có ba định dạng tar có thể được tạo bằng module :mod:`!tarfile`:

* Định dạng POSIX.1-1988 ustar (:const:`USTAR_FORMAT`). Định dạng này hỗ trợ tên tệp dài tối đa 256 ký tự và tên liên kết dài tối đa 100 ký tự. Kích thước tệp tối đa là 8 GiB. Đây là một định dạng cũ và hạn chế, nhưng được hỗ trợ rộng rãi.

* Định dạng GNU tar (:const:`GNU_FORMAT`). Định dạng này hỗ trợ tên tệp và tên liên kết dài, các tệp lớn hơn 8 GiB và các tệp thưa. Đây là tiêu chuẩn trên thực tế trên các hệ thống GNU/Linux. :mod:`!tarfile` hỗ trợ đầy đủ các phần mở rộng của GNU tar cho tên dài; tính năng hỗ trợ tệp thưa chỉ có thể đọc.

* Định dạng POSIX.1-2001 pax (:const:`PAX_FORMAT`). Đây là định dạng linh hoạt nhất, hầu như không có giới hạn. Định dạng này hỗ trợ tên tệp và tên liên kết dài, các tệp lớn, đồng thời lưu tên đường dẫn theo cách di động. Các triển khai tar hiện đại, bao gồm GNU tar, bsdtar/libarchive và star, hỗ trợ đầy đủ các tính năng *pax* mở rộng; một số thư viện cũ hoặc không còn được duy trì có thể không hỗ trợ, nhưng vẫn nên xử lý các kho lưu trữ *pax* như thể chúng ở định dạng *ustar* được hỗ trợ phổ biến. Đây là định dạng mặc định hiện tại cho các kho lưu trữ mới.

  Định dạng này mở rộng định dạng *ustar* hiện có bằng các header bổ sung để lưu trữ thông tin không thể được lưu theo cách khác. Có hai loại header pax: header mở rộng chỉ ảnh hưởng đến header của tệp ngay sau đó, còn header toàn cục có hiệu lực trên toàn bộ kho lưu trữ và ảnh hưởng đến tất cả các tệp tiếp theo. Vì lý do khả chuyển, toàn bộ dữ liệu trong header pax được mã hóa bằng *UTF-8*.

Có thêm một số biến thể của định dạng tar có thể được đọc nhưng không thể tạo:

* Định dạng V7 cổ. Đây là định dạng tar đầu tiên của Unix Seventh Edition, chỉ lưu trữ các tệp thông thường và thư mục. Tên không được dài quá 100 ký tự và không có thông tin về tên người dùng/nhóm. Một số kho lưu trữ có checksum header bị tính sai khi các trường chứa ký tự không phải ASCII.

* Định dạng tar mở rộng của SunOS. Định dạng này là một biến thể của định dạng POSIX.1-2001 pax nhưng không tương thích với định dạng đó.

.. _tar-unicode:

Các vấn đề về Unicode
---------------------

Định dạng tar ban đầu được thiết kế để tạo bản sao lưu trên ổ băng từ, tập trung chủ yếu vào việc bảo toàn thông tin hệ thống tệp. Ngày nay, các kho lưu trữ tar thường được dùng để phân phối tệp và trao đổi kho lưu trữ qua mạng. Một vấn đề của định dạng ban đầu (là nền tảng cho tất cả các định dạng khác) là không có khái niệm hỗ trợ các encoding ký tự khác nhau. Ví dụ, một kho lưu trữ tar thông thường được tạo trên hệ thống *UTF-8* không thể được đọc chính xác trên hệ thống *Latin-1* nếu chứa các ký tự không thuộc *ASCII*. Siêu dữ liệu dạng văn bản (chẳng hạn như tên tệp, linkname, tên người dùng/nhóm) sẽ bị hiển thị sai lệch. Đáng tiếc là không có cách nào tự động phát hiện encoding của một kho lưu trữ. Định dạng pax được thiết kế để giải quyết vấn đề này. Định dạng này lưu siêu dữ liệu không phải ASCII bằng encoding ký tự phổ quát *UTF-8*.

Chi tiết về việc chuyển đổi ký tự trong :mod:`!tarfile` được điều khiển bởi các đối số từ khóa *encoding* và *errors* của lớp :class:`TarFile`.

*encoding* xác định encoding ký tự sẽ dùng cho siêu dữ liệu trong kho lưu trữ. Giá trị mặc định là :func:`sys.getfilesystemencoding` hoặc ``'ascii'`` làm phương án dự phòng. Tùy thuộc vào việc kho lưu trữ được đọc hay ghi, siêu dữ liệu phải được giải mã hoặc mã hóa. Nếu *encoding* không được đặt phù hợp, quá trình chuyển đổi này có thể thất bại.

Đối số *errors* xác định cách xử lý các ký tự không thể chuyển đổi. Các giá trị có thể có được liệt kê trong phần :ref:`error-handlers`. Cơ chế mặc định là ``'surrogateescape'``, cơ chế mà Python cũng sử dụng cho các lệnh gọi hệ thống tệp của mình; xem :ref:`os-filenames`.

Đối với các kho lưu trữ :const:`PAX_FORMAT` (mặc định), *encoding* nhìn chung không cần thiết vì toàn bộ siêu dữ liệu được lưu bằng *UTF-8*. *encoding* chỉ được sử dụng trong những trường hợp hiếm gặp khi các header pax nhị phân được giải mã hoặc khi các chuỗi chứa ký tự surrogate được lưu trữ.

.. _`GNU tar manual, Basic Tar Format`: https://www.gnu.org/software/tar/manual/html_node/Standard.html
