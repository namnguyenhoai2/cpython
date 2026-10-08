:mod:`!zipfile` --- Làm việc với các tệp lưu trữ ZIP
====================================================

.. module:: zipfile
   :synopsis: Đọc và ghi các tệp lưu trữ định dạng ZIP.

.. moduleauthor:: James C. Ahlstrom <jim@interet.com>
.. sectionauthor:: James C. Ahlstrom <jim@interet.com>

**Mã nguồn:** :source:`Lib/zipfile/`

--------------

Định dạng tệp ZIP là một tiêu chuẩn lưu trữ và nén phổ biến. Mô-đun này cung cấp các công cụ để tạo, đọc, ghi, nối thêm và liệt kê một tệp ZIP. Mọi cách sử dụng nâng cao mô-đun này đều yêu cầu hiểu về định dạng, như được định nghĩa trong `PKZIP Application Note <PKZIP Application Note_>`_.

Mô-đun này không xử lý các tệp ZIP nhiều phần. Mô-đun có thể xử lý các tệp ZIP sử dụng phần mở rộng ZIP64 (tức là các tệp ZIP có kích thước lớn hơn 4 GiB). Mô-đun hỗ trợ giải mã các tệp được mã hóa trong kho lưu trữ ZIP, nhưng không thể tạo tệp được mã hóa. Việc giải mã cực kỳ chậm vì được triển khai bằng Python thuần thay vì C.

..
   Đoạn văn sau đây phải tương tự như ../includes/optional-module.rst

Việc xử lý các kho lưu trữ đã nén yêu cầu các :term:`mô-đun tùy chọn <optional module>` như :mod:`zlib`, :mod:`bz2`, :mod:`lzma` và :mod:`compression.zstd`. Nếu bất kỳ mô-đun nào trong số đó bị thiếu trong bản sao CPython của bạn, hãy tìm tài liệu từ nhà phân phối (tức là đơn vị đã cung cấp Python cho bạn). Nếu bạn là nhà phân phối, hãy xem :ref:`optional-module-requirements`.

Mô-đun định nghĩa các mục sau:

.. exception:: BadZipFile

   Lỗi được phát sinh đối với các tệp ZIP không hợp lệ.

   .. versionadded:: 3.2


.. exception:: BadZipfile

   Bí danh của :exc:`BadZipFile`, để tương thích với các phiên bản Python cũ hơn.

   .. deprecated:: 3.2


.. exception:: LargeZipFile

   Lỗi được phát sinh khi một tệp ZIP yêu cầu chức năng ZIP64 nhưng chức năng này chưa được bật.


.. class:: ZipFile
   :noindex:

   Lớp dùng để đọc và ghi các tệp ZIP. Xem phần
   :ref:`zipfile-objects` để biết chi tiết về hàm khởi tạo.


.. class:: Path
   :noindex:

   Lớp triển khai một tập con của giao diện do
   :class:`pathlib.Path`, bao gồm toàn bộ
   :class:`importlib.resources.abc.Traversable` interface.

   .. versionadded:: 3.8


.. class:: PyZipFile
   :noindex:

   Lớp dùng để tạo các kho lưu trữ ZIP chứa các thư viện Python.


.. class:: ZipInfo(filename='NoName', date_time=(1980,1,1,0,0,0))

   Lớp dùng để biểu diễn thông tin về một thành phần của kho lưu trữ. Các thực thể của lớp này được các phương thức :meth:`.getinfo` và :meth:`.infolist` của các đối tượng :class:`ZipFile` trả về. Hầu hết người dùng mô-đun :mod:`!zipfile` sẽ không cần tạo các thực thể này mà chỉ sử dụng những thực thể do mô-đun này tạo ra. *filename* phải là tên đầy đủ của thành phần trong kho lưu trữ, còn *date_time* phải là một tuple chứa sáu trường mô tả thời điểm tệp được sửa đổi lần cuối; các trường được mô tả trong phần
   :ref:`zipinfo-objects`.

   .. versionchanged:: 3.13
      Một thuộc tính :attr:`!compress_level` công khai đã được thêm để cung cấp :attr:`!_compresslevel` trước đây được bảo vệ. Tên được bảo vệ cũ tiếp tục hoạt động dưới dạng một property để đảm bảo khả năng tương thích ngược.


   .. method:: _for_archive(archive)

      Phân giải các thuộc tính date_time, compression và các thuộc tính bên ngoài thành các giá trị mặc định phù hợp như được :meth:`ZipFile.writestr` sử dụng.

      Trả về self để cho phép chaining.

      .. versionadded:: 3.14


.. function:: is_zipfile(filename)

   Trả về ``True`` nếu *filename* là tệp ZIP hợp lệ dựa trên magic number của nó, nếu không thì trả về ``False``. *filename* cũng có thể là tệp hoặc đối tượng giống tệp.

   .. versionchanged:: 3.1
      Hỗ trợ các đối tượng tệp và đối tượng giống tệp.


.. data:: ZIP_STORED

   Hằng số số cho một thành viên archive không nén.


.. data:: ZIP_DEFLATED

   Hằng số số cho phương thức nén ZIP thông thường. Điều này yêu cầu
   :mod:`zlib` mô-đun.


.. data:: ZIP_BZIP2

   Hằng số số cho phương thức nén BZIP2. Điều này yêu cầu
   :mod:`bz2` mô-đun.

   .. versionadded:: 3.3

.. data:: ZIP_LZMA

   Hằng số số học cho phương thức nén LZMA. Phương thức này yêu cầu
   :mod:`lzma` mô-đun.

   .. versionadded:: 3.3

.. data:: ZIP_ZSTANDARD

   Hằng số số học cho phương thức nén Zstandard. Phương thức này yêu cầu
   :mod:`compression.zstd` mô-đun.

   .. note::

      Trong APPNOTE 6.3.7, mã phương thức ``20`` được gán cho phương thức nén Zstandard. Mã này đã được thay đổi trong APPNOTE 6.3.8 thành mã phương thức ``93`` để tránh xung đột, còn mã phương thức ``20`` bị ngừng sử dụng. Để đảm bảo khả năng tương thích, mô-đun :mod:`!zipfile` đọc cả hai mã phương thức nhưng chỉ ghi dữ liệu bằng mã phương thức ``93``.

   .. versionadded:: 3.14

.. note::

   Định dạng tệp ZIP đã hỗ trợ phương thức nén bzip2 từ năm 2001, phương thức nén LZMA từ năm 2006 và phương thức nén Zstandard từ
   2020. Tuy nhiên, một số công cụ (bao gồm các bản phát hành Python cũ hơn) không hỗ trợ
   các phương thức nén này, và có thể từ chối xử lý toàn bộ tệp ZIP hoặc không thể giải nén các tệp riêng lẻ.

.. seealso::

   `Ghi chú ứng dụng PKZIP <PKZIP Application Note_>`_
      Tài liệu về định dạng tệp ZIP do Phil Katz, người tạo ra định dạng và các thuật toán được sử dụng, biên soạn.

   `Trang chủ Info-ZIP <https://infozip.sourceforge.net/>`_
      Thông tin về các chương trình lưu trữ ZIP và thư viện phát triển của dự án Info-ZIP.


.. _zipfile-objects:

Đối tượng ZipFile
-----------------


.. class:: ZipFile(file, mode='r', compression=ZIP_STORED, allowZip64=True, \
                   compresslevel=None, *, strict_timestamps=True, \ metadata_encoding=None)

   Mở một tệp ZIP, trong đó *file* có thể là đường dẫn đến một tệp (một chuỗi), một đối tượng giống tệp hoặc một :term:`path-like object`.

   Tham số *mode* phải là ``'r'`` để đọc một tệp hiện có, ``'w'`` để cắt ngắn và ghi một tệp mới, ``'a'`` để nối thêm vào một tệp hiện có hoặc ``'x'`` để chỉ tạo và ghi một tệp mới. Nếu *mode* là ``'x'`` và *file* trỏ đến một tệp hiện có, một :exc:`FileExistsError` sẽ được phát sinh. Nếu *mode* là ``'a'`` và *file* trỏ đến một tệp ZIP hiện có, các tệp bổ sung sẽ được thêm vào đó. Nếu *file* không trỏ đến một tệp ZIP, một kho lưu trữ ZIP mới sẽ được nối thêm vào tệp. Cách này được dùng để thêm một kho lưu trữ ZIP vào một tệp khác (chẳng hạn như :file:`python.exe`). Nếu *mode* là ``'a'`` và tệp hoàn toàn không tồn tại, tệp sẽ được tạo. Nếu *mode* là ``'r'`` hoặc ``'a'``, tệp phải hỗ trợ thao tác seek.

   *compression* là phương thức nén ZIP được sử dụng khi ghi kho lưu trữ và phải là :const:`ZIP_STORED`, :const:`ZIP_DEFLATED`,
   :const:`ZIP_BZIP2`, :const:`ZIP_LZMA` hoặc :const:`ZIP_ZSTANDARD`; các giá trị không được nhận dạng sẽ khiến :exc:`NotImplementedError` được phát sinh. Nếu
   :const:`ZIP_DEFLATED`, :const:`ZIP_BZIP2`, :const:`ZIP_LZMA` hoặc
   :const:`ZIP_ZSTANDARD` được chỉ định nhưng mô-đun tương ứng (:mod:`zlib`, :mod:`bz2`, :mod:`lzma` hoặc :mod:`compression.zstd`) không khả dụng, :exc:`RuntimeError` sẽ được phát sinh. Giá trị mặc định là :const:`ZIP_STORED`.

   Nếu *allowZip64* là ``True`` (mặc định), zipfile sẽ tạo các tệp ZIP sử dụng phần mở rộng ZIP64 khi tệp zip lớn hơn 4 GiB. Nếu là ``false``, :mod:`!zipfile` sẽ phát sinh ngoại lệ khi tệp ZIP cần các phần mở rộng ZIP64.

   Tham số *compresslevel* kiểm soát mức độ nén được sử dụng khi ghi tệp vào kho lưu trữ. Khi sử dụng :const:`ZIP_STORED` hoặc :const:`ZIP_LZMA`, tham số này không có tác dụng. Khi sử dụng :const:`ZIP_DEFLATED`, các số nguyên từ ``0`` đến ``9`` được chấp nhận (xem :class:`zlib <zlib.compressobj>` để biết thêm thông tin). Khi sử dụng :const:`ZIP_BZIP2`, các số nguyên từ ``1`` đến ``9`` được chấp nhận (xem :class:`bz2 <bz2.BZ2File>` để biết thêm thông tin). Khi sử dụng :const:`ZIP_ZSTANDARD`, các số nguyên từ ``-131072`` đến ``22`` thường được chấp nhận (xem
   :attr:`CompressionParameter.compression_level <compression.zstd.CompressionParameter.compression_level>` để biết thêm về cách lấy các giá trị hợp lệ và ý nghĩa của chúng).

   Đối số *strict_timestamps*, khi được đặt thành ``False``, cho phép nén các tệp cũ hơn ngày 1980-01-01, nhưng phải trả giá bằng việc đặt dấu thời gian thành 1980-01-01. Hành vi tương tự xảy ra với các tệp mới hơn ngày 2107-12-31; dấu thời gian cũng được đặt thành giới hạn này.

   Khi mode là ``'r'``, có thể đặt *metadata_encoding* thành tên của một codec, được dùng để giải mã metadata như tên của các thành viên và chú thích ZIP.

   Nếu tệp được tạo với mode ``'w'``, ``'x'`` hoặc ``'a'`` rồi
   :meth:`closed <close>` mà không thêm tệp nào vào kho lưu trữ, các cấu trúc ZIP thích hợp cho một kho lưu trữ trống sẽ được ghi vào tệp.

   ZipFile cũng là một context manager và do đó hỗ trợ
   :keyword:`with` câu lệnh. Trong ví dụ, *myzip* được đóng sau khi
   phần thân của câu lệnh :keyword:`!with` hoàn tất---ngay cả khi xảy ra ngoại lệ::

      with ZipFile('spam.zip', 'w') as myzip:
          myzip.write('eggs.txt')

   .. note::

      *metadata_encoding* là thiết lập áp dụng cho toàn bộ ZipFile. Không thể thiết lập thuộc tính này riêng cho từng thành viên.

      Thuộc tính này là một giải pháp thay thế cho các implementation cũ tạo archive với tên được mã hóa theo encoding hoặc code page của locale hiện tại (chủ yếu trên Windows). Theo tiêu chuẩn .ZIP, encoding của metadata có thể được chỉ định là IBM code page (mặc định) hoặc UTF-8 bằng một cờ trong header của archive. Cờ đó được ưu tiên hơn *metadata_encoding*, vốn là một phần mở rộng dành riêng cho Python.

   .. versionchanged:: 3.2
      Đã bổ sung khả năng sử dụng :class:`ZipFile` làm context manager.

   .. versionchanged:: 3.3
      Đã bổ sung hỗ trợ nén bằng :mod:`bzip2 <bz2>` và :mod:`lzma`.

   .. versionchanged:: 3.4
      Các phần mở rộng ZIP64 được bật theo mặc định.

   .. versionchanged:: 3.5
      Đã bổ sung hỗ trợ ghi vào các stream không thể seek. Đã bổ sung hỗ trợ cho chế độ ``'x'``.

   .. versionchanged:: 3.6
      Trước đây, một :exc:`RuntimeError` đơn thuần sẽ được raise khi gặp các giá trị compression không được nhận dạng.

   .. versionchanged:: 3.6.2
      Tham số *file* chấp nhận một :term:`path-like object`.

   .. versionchanged:: 3.7
      Thêm tham số *compresslevel*.

   .. versionchanged:: 3.8
      Tham số chỉ nhận keyword *strict_timestamps*.

   .. versionchanged:: 3.11
      Đã bổ sung hỗ trợ chỉ định encoding của tên member để đọc metadata trong thư mục và các header của file trong zipfile.


.. method:: ZipFile.close()

   Đóng file archive. Bạn phải gọi :meth:`close` trước khi thoát khỏi chương trình, nếu không các bản ghi thiết yếu sẽ không được ghi.


.. method:: ZipFile.getinfo(name)

   Trả về một đối tượng :class:`ZipInfo` chứa thông tin về thành viên lưu trữ *name*. Việc gọi :meth:`getinfo` với một tên hiện không có trong kho lưu trữ sẽ gây ra :exc:`KeyError`.


.. method:: ZipFile.infolist()

   Trả về một danh sách chứa một đối tượng :class:`ZipInfo` cho mỗi thành viên của kho lưu trữ. Các đối tượng có cùng thứ tự với các mục tương ứng trong tệp ZIP thực tế trên đĩa nếu một kho lưu trữ hiện có đã được mở.


.. method:: ZipFile.namelist()

   Trả về danh sách các thành viên của kho lưu trữ theo tên.


.. method:: ZipFile.open(name, mode='r', pwd=None, *, force_zip64=False)

   Truy cập một thành viên của kho lưu trữ dưới dạng đối tượng giống tệp nhị phân. *name* có thể là tên của một tệp trong kho lưu trữ hoặc một đối tượng :class:`ZipInfo`. Tham số *mode*, nếu được cung cấp, phải là ``'r'`` (mặc định) hoặc ``'w'``. *pwd* là mật khẩu được sử dụng để giải mã các tệp ZIP được mã hóa dưới dạng một
   đối tượng :class:`bytes`.

   :meth:`~ZipFile.open` cũng là một context manager và do đó hỗ trợ
   câu lệnh :keyword:`with`::

      with ZipFile('spam.zip') as myzip:
          with myzip.open('eggs.txt') as myfile:
              print(myfile.read())

   Với *mode* ``'r'``, đối tượng giống tệp (``ZipExtFile``) là chỉ đọc và cung cấp các phương thức sau:
   :meth:`~io.BufferedIOBase.read`, :meth:`~io.IOBase.readline`,
   :meth:`~io.IOBase.readlines`, :meth:`~io.IOBase.seek`,
   :meth:`~io.IOBase.tell`, :meth:`~container.__iter__`, :meth:`~iterator.__next__`. Các đối tượng này có thể hoạt động độc lập với ZipFile.

   Với ``mode='w'``, một file handle có thể ghi được trả về, hỗ trợ
   phương thức :meth:`~io.BufferedIOBase.write`. Trong khi một file handle có thể ghi đang mở, việc cố gắng đọc hoặc ghi các tệp khác trong tệp ZIP sẽ gây ra
   :exc:`ValueError`.

   Trong cả hai trường hợp, đối tượng giống tệp cũng có thuộc tính :attr:`!name`, tương đương với tên của một tệp trong archive, và
   :attr:`!mode`, là ``'rb'`` hoặc ``'wb'`` tùy thuộc vào input mode.

   Khi ghi một tệp, nếu trước đó chưa biết kích thước tệp nhưng kích thước này có thể vượt quá 2 GiB, hãy truyền ``force_zip64=True`` để đảm bảo định dạng header có khả năng hỗ trợ các tệp lớn. Nếu biết trước kích thước tệp, hãy tạo một đối tượng :class:`ZipInfo` với :attr:`~ZipInfo.file_size` được thiết lập, rồi dùng đối tượng đó làm tham số *name*.

   .. note::

      Các phương thức :meth:`.open`, :meth:`read` và :meth:`extract` có thể nhận tên tệp hoặc đối tượng :class:`ZipInfo`. Điều này sẽ rất hữu ích khi bạn cố đọc một tệp ZIP chứa các thành viên có tên trùng nhau.

   .. versionchanged:: 3.6
      Đã loại bỏ hỗ trợ cho ``mode='U'``. Sử dụng :class:`io.TextIOWrapper` để đọc các tệp văn bản đã nén ở chế độ :term:`universal newlines`.

   .. versionchanged:: 3.6
      :meth:`ZipFile.open` can now be used to write files into the archive with the
      Tùy chọn ``mode='w'``.

   .. versionchanged:: 3.6
      Việc gọi :meth:`.open` trên một ZipFile đã đóng sẽ gây ra :exc:`ValueError`. Trước đây, một :exc:`RuntimeError` sẽ được phát sinh.

   .. versionchanged:: 3.13
      Đã thêm các thuộc tính :attr:`!name` và :attr:`!mode` cho đối tượng giống tệp có thể ghi. Giá trị của thuộc tính :attr:`!mode` đối với đối tượng giống tệp có thể đọc đã được thay đổi từ ``'r'`` thành ``'rb'``.


.. method:: ZipFile.extract(member, path=None, pwd=None)

   Trích xuất một thành viên từ kho lưu trữ vào thư mục làm việc hiện tại; *member* phải là tên đầy đủ của thành viên hoặc một đối tượng :class:`ZipInfo`. Thông tin tệp của thành viên được trích xuất chính xác nhất có thể. *path* chỉ định một thư mục khác để trích xuất vào. *member* có thể là tên tệp hoặc một đối tượng :class:`ZipInfo`. *pwd* là mật khẩu dùng cho các tệp được mã hóa, dưới dạng một đối tượng :class:`bytes`.

   Trả về đường dẫn đã chuẩn hóa được tạo (một thư mục hoặc tệp mới).

   .. note::

      Nếu tên tệp thành viên là một đường dẫn tuyệt đối, điểm chia sẻ drive/UNC và các dấu gạch chéo (ngược) ở đầu sẽ bị loại bỏ, ví dụ: ``///foo/bar`` trở thành ``foo/bar`` trên Unix và ``C:\foo\bar`` trở thành ``foo\bar`` trên Windows. Ngoài ra, mọi thành phần ``".."`` trong tên tệp thành viên sẽ bị loại bỏ, ví dụ: ``../../foo../../ba..r`` trở thành ``foo../ba..r``. Trên Windows, các ký tự không hợp lệ (``:``, ``<``, ``>``, ``|``, ``"``, ``?`` và ``*``) được thay thế bằng dấu gạch dưới (``_``).

   .. versionchanged:: 3.6
      Gọi :meth:`extract` trên một ZipFile đã đóng sẽ phát sinh một
      :exc:`ValueError`. Trước đây, một :exc:`RuntimeError` được phát sinh.

   .. versionchanged:: 3.6.2
      Tham số *path* chấp nhận một :term:`path-like object`.


.. method:: ZipFile.extractall(path=None, members=None, pwd=None)

   Giải nén tất cả thành viên từ archive vào thư mục làm việc hiện tại. *path* chỉ định một thư mục khác để giải nén. *members* là tùy chọn và phải là tập con của danh sách do :meth:`namelist` trả về. *pwd* là mật khẩu được dùng cho các tệp đã mã hóa dưới dạng đối tượng :class:`bytes`.

   .. warning::

      Không bao giờ giải nén archive từ các nguồn không đáng tin cậy nếu chưa kiểm tra trước. Các tệp có thể được tạo bên ngoài *path*, chẳng hạn như các thành viên có tên tệp tuyệt đối hoặc tên tệp chứa các thành phần "..". Module này cố gắng ngăn chặn điều đó. Xem :meth:`extract` note.

   .. versionchanged:: 3.6
      Gọi :meth:`extractall` trên một ZipFile đã đóng sẽ phát sinh một
      :exc:`ValueError`. Trước đây, một :exc:`RuntimeError` được phát sinh.

   .. versionchanged:: 3.6.2
      Tham số *path* chấp nhận một :term:`path-like object`.


.. method:: ZipFile.printdir()

   In mục lục của archive ra ``sys.stdout``.


.. method:: ZipFile.setpassword(pwd)

   Đặt *pwd* (một đối tượng :class:`bytes`) làm mật khẩu mặc định để giải nén các tệp được mã hóa.


.. method:: ZipFile.read(name, pwd=None)

   Trả về các byte của tệp *name* trong archive. *name* là tên của tệp trong archive hoặc một đối tượng :class:`ZipInfo`. Archive phải được mở để đọc hoặc nối thêm. *pwd* là mật khẩu được sử dụng cho các tệp được mã hóa dưới dạng đối tượng :class:`bytes` và nếu được chỉ định thì sẽ ghi đè mật khẩu mặc định được đặt bằng :meth:`setpassword`. Việc gọi :meth:`read` trên một ZipFile sử dụng phương thức nén khác với
   :const:`ZIP_STORED`, :const:`ZIP_DEFLATED`, :const:`ZIP_BZIP2`,
   :const:`ZIP_LZMA` hoặc :const:`ZIP_ZSTANDARD` sẽ phát sinh một
   :exc:`NotImplementedError`. Lỗi cũng sẽ phát sinh nếu không có mô-đun nén tương ứng.

   .. versionchanged:: 3.6
      Gọi :meth:`read` trên một ZipFile đã đóng sẽ gây ra :exc:`ValueError`. Trước đây, một :exc:`RuntimeError` sẽ được gây ra.


.. method:: ZipFile.testzip()

   Đọc tất cả các tệp trong archive và kiểm tra CRC cũng như các header của tệp. Trả về tên của tệp đầu tiên bị lỗi, hoặc trả về ``None``.

   .. versionchanged:: 3.6
      Gọi :meth:`testzip` trên một ZipFile đã đóng sẽ gây ra một
      :exc:`ValueError`. Trước đây, một :exc:`RuntimeError` được phát sinh.


.. method:: ZipFile.write(filename, arcname=None, compress_type=None, \
                          compresslevel=None)

   Ghi tệp có tên *filename* vào archive, đặt tên trong archive là *arcname* (theo mặc định, tên này sẽ giống *filename*, nhưng không có ký tự ổ đĩa và các dấu phân cách đường dẫn ở đầu sẽ bị loại bỏ). Nếu được cung cấp, *compress_type* sẽ ghi đè giá trị được truyền cho tham số *compression* của constructor đối với entry mới. Tương tự, *compresslevel* sẽ ghi đè giá trị của constructor nếu được cung cấp. Archive phải được mở với mode ``'w'``, ``'x'`` hoặc ``'a'``.

   .. note::

      Tiêu chuẩn tệp ZIP trước đây không quy định encoding cho metadata, nhưng khuyến nghị mạnh mẽ CP437 (encoding gốc của IBM PC) để bảo đảm khả năng tương tác. Các phiên bản gần đây cho phép chỉ sử dụng UTF-8. Trong module này, UTF-8 sẽ tự động được dùng để ghi tên member nếu chúng chứa bất kỳ ký tự nào không phải ASCII. Không thể ghi tên member bằng bất kỳ encoding nào khác ngoài ASCII hoặc UTF-8.

   .. note::

      Tên archive phải tương đối so với thư mục gốc của archive, nghĩa là không được bắt đầu bằng dấu phân cách đường dẫn.

   .. note::

      Nếu ``arcname`` (hoặc ``filename``, nếu ``arcname`` không được cung cấp) chứa byte null, tên tệp trong archive sẽ bị cắt tại byte null.

   .. note::

      Dấu gạch chéo ở đầu tên tệp có thể khiến không thể mở archive bằng một số chương trình zip trên hệ thống Windows.

   .. versionchanged:: 3.6
      Gọi :meth:`write` trên một ZipFile được tạo với mode ``'r'`` hoặc một ZipFile đã đóng sẽ phát sinh :exc:`ValueError`. Trước đây, một :exc:`RuntimeError` sẽ được phát sinh.


.. method:: ZipFile.writestr(zinfo_or_arcname, data, compress_type=None, \
                             compresslevel=None)

   Ghi một tệp vào archive. Nội dung là *data*, có thể là một instance của :class:`str` hoặc :class:`bytes`; nếu là một :class:`str`, trước tiên nó sẽ được mã hóa thành UTF-8. *zinfo_or_arcname* là tên tệp sẽ được đặt trong archive hoặc một instance của :class:`ZipInfo`. Nếu là một instance, ít nhất phải cung cấp tên tệp, ngày và giờ. Nếu là một tên, ngày và giờ sẽ được đặt thành ngày và giờ hiện tại. Archive phải được mở với mode ``'w'``, ``'x'`` hoặc ``'a'``.

   Nếu được cung cấp, *compress_type* sẽ ghi đè giá trị được cung cấp cho tham số *compression* của constructor cho entry mới hoặc trong *zinfo_or_arcname* (nếu đó là một instance của :class:`ZipInfo`). Tương tự, *compresslevel* sẽ ghi đè giá trị của constructor nếu được cung cấp.

   .. note::

      Khi truyền một instance :class:`ZipInfo` làm tham số *zinfo_or_arcname*, phương thức nén được sử dụng sẽ là phương thức được chỉ định trong member *compress_type* của instance :class:`ZipInfo` đã cho. Theo mặc định, the
      constructor :class:`ZipInfo` đặt member này thành :const:`ZIP_STORED`.

   .. versionchanged:: 3.2
      Đối số *compress_type*.

   .. versionchanged:: 3.6
      Việc gọi :meth:`writestr` trên một ZipFile được tạo với mode ``'r'`` hoặc trên một ZipFile đã đóng sẽ phát sinh :exc:`ValueError`. Trước đây, một :exc:`RuntimeError` được phát sinh.

   .. versionchanged:: 3.14
      Hiện tôn trọng biến môi trường :envvar:`SOURCE_DATE_EPOCH`. Nếu được đặt, giá trị này được dùng làm dấu thời gian sửa đổi cho tệp được ghi vào kho lưu trữ ZIP, thay vì dùng thời gian hiện tại.

.. method:: ZipFile.mkdir(zinfo_or_directory, mode=511)

   Tạo một thư mục bên trong kho lưu trữ. Nếu *zinfo_or_directory* là một chuỗi, một thư mục sẽ được tạo bên trong kho lưu trữ với mode được chỉ định trong đối số *mode*. Tuy nhiên, nếu *zinfo_or_directory* là một instance :class:`ZipInfo` thì đối số *mode* sẽ bị bỏ qua.

   Kho lưu trữ phải được mở với mode ``'w'``, ``'x'`` hoặc ``'a'``.

   .. versionadded:: 3.11


Các thuộc tính dữ liệu sau cũng khả dụng:

.. attribute:: ZipFile.filename

   Tên của tệp ZIP.

.. attribute:: ZipFile.debug

   Mức đầu ra debug cần sử dụng. Có thể đặt giá trị này từ ``0`` (mặc định, không có đầu ra) đến ``3`` (nhiều đầu ra nhất). Thông tin debug được ghi vào ``sys.stdout``.

.. attribute:: ZipFile.comment

   Comment liên kết với tệp ZIP dưới dạng đối tượng :class:`bytes`. Nếu gán comment cho một
   instance :class:`ZipFile` được tạo với mode ``'w'``, ``'x'`` hoặc ``'a'``, comment đó không được dài quá 65535 byte. Comment dài hơn sẽ bị cắt bớt.


.. _path-objects:

Các đối tượng Path
------------------

.. class:: Path(root, at='')

   Tạo một đối tượng Path từ một zipfile ``root`` (có thể là một
   một instance của :class:`ZipFile` hoặc ``file`` phù hợp để truyền vào constructor :class:`ZipFile`.

   ``at`` chỉ định vị trí của Path này trong zipfile, ví dụ: 'dir/file.txt', 'dir/' hoặc ''. Mặc định là chuỗi rỗng, biểu thị thư mục gốc.

   .. note::
      Lớp :class:`Path` không làm sạch tên tệp trong kho lưu trữ ZIP. Không giống các phương thức :meth:`ZipFile.extract` và :meth:`ZipFile.extractall`, trách nhiệm xác thực hoặc làm sạch tên tệp để ngăn lỗ hổng path traversal (ví dụ: đường dẫn tuyệt đối hoặc đường dẫn có các thành phần "..") thuộc về bên gọi. Khi xử lý các kho lưu trữ không đáng tin cậy, hãy cân nhắc phân giải tên tệp bằng :func:`os.path.abspath` và kiểm tra tên đó với thư mục đích bằng :func:`os.path.commonpath`.

Các đối tượng Path cung cấp những tính năng sau của các đối tượng :mod:`pathlib.Path`:

Có thể duyệt qua các đối tượng Path bằng toán tử ``/`` hoặc ``joinpath``.

.. attribute:: Path.name

   Thành phần cuối cùng của đường dẫn.

.. method:: Path.open(mode='r', *, pwd, **)

   Gọi :meth:`ZipFile.open` trên path hiện tại. Cho phép mở để đọc hoặc ghi, ở dạng văn bản hoặc nhị phân, thông qua các mode được hỗ trợ: 'r', 'w', 'rb', 'wb'. Các đối số vị trí và từ khóa được truyền tiếp đến
   :class:`io.TextIOWrapper` khi được mở dưới dạng văn bản và bị bỏ qua nếu không. ``pwd`` là tham số ``pwd`` cho
   :meth:`ZipFile.open`.

   .. versionchanged:: 3.9
      Đã bổ sung hỗ trợ cho các chế độ văn bản và nhị phân của open. Chế độ mặc định hiện là văn bản.

   .. versionchanged:: 3.11.2
      Có thể cung cấp tham số ``encoding`` dưới dạng đối số vị trí mà không gây ra :exc:`TypeError`. Như đã có thể xảy ra trong 3.9. Mã cần tương thích với các phiên bản 3.10 và 3.11 chưa được vá phải truyền tất cả
      các đối số :class:`io.TextIOWrapper`, bao gồm cả ``encoding``, dưới dạng keyword.

.. method:: Path.iterdir()

   Liệt kê các mục con của thư mục hiện tại.

.. method:: Path.is_dir()

   Trả về ``True`` nếu context hiện tại tham chiếu đến một thư mục.

.. method:: Path.is_file()

   Trả về ``True`` nếu context hiện tại tham chiếu đến một tệp.

.. method:: Path.is_symlink()

   Trả về ``True`` nếu ngữ cảnh hiện tại tham chiếu đến một symbolic link.

   .. versionadded:: 3.12

   .. versionchanged:: 3.13
      Trước đây, ``is_symlink`` luôn trả về ``False``.

.. method:: Path.exists()

   Trả về ``True`` nếu ngữ cảnh hiện tại tham chiếu đến một tệp hoặc thư mục trong tệp zip.

.. data:: Path.suffix

   Phần cuối được phân tách bằng dấu chấm của thành phần cuối cùng, nếu có. Phần này thường được gọi là phần mở rộng tệp.

   .. versionadded:: 3.11
      Đã thêm thuộc tính :data:`Path.suffix`.

.. data:: Path.stem

   Thành phần đường dẫn cuối cùng, không có hậu tố.

   .. versionadded:: 3.11
      Đã thêm thuộc tính :data:`Path.stem`.

.. data:: Path.suffixes

   Danh sách các hậu tố của đường dẫn, thường được gọi là phần mở rộng tệp.

   .. versionadded:: 3.11
      Đã thêm thuộc tính :data:`Path.suffixes`.

.. method:: Path.read_text(*, **)

   Đọc tệp hiện tại dưới dạng văn bản Unicode. Các đối số vị trí và đối số từ khóa được truyền tiếp đến
   :class:`io.TextIOWrapper` (ngoại trừ ``buffer``, vốn được ngầm định theo ngữ cảnh).

   .. versionchanged:: 3.11.2
      Có thể cung cấp tham số ``encoding`` dưới dạng đối số vị trí mà không gây ra :exc:`TypeError`. Như đã có thể xảy ra trong 3.9. Mã cần tương thích với các phiên bản 3.10 và 3.11 chưa được vá phải truyền tất cả
      các đối số :class:`io.TextIOWrapper`, bao gồm cả ``encoding``, dưới dạng keyword.

.. method:: Path.read_bytes()

   Đọc tệp hiện tại dưới dạng byte.

.. method:: Path.joinpath(*other)

   Trả về một đối tượng Path mới với từng đối số *other* được nối lại. Các cách sau là tương đương::

   >>> Path(...).joinpath('child').joinpath('grandchild')
   >>> Path(...).joinpath('child', 'grandchild')
   >>> Path(...) / 'child' / 'grandchild'

   .. versionchanged:: 3.10
      Trước phiên bản 3.10, ``joinpath`` chưa được ghi chép và chỉ chấp nhận đúng một tham số.

Dự án :pypi:`zipp` cung cấp các bản backport của chức năng đối tượng path mới nhất cho các phiên bản Python cũ hơn. Sử dụng ``zipp.Path`` thay cho ``zipfile.Path`` để sớm sử dụng các thay đổi.

.. _pyzipfile-objects:

Đối tượng PyZipFile
-------------------

Hàm khởi tạo :class:`PyZipFile` nhận các tham số giống như hàm khởi tạo
:class:`ZipFile`, cùng với một tham số bổ sung là *optimize*.

.. class:: PyZipFile(file, mode='r', compression=ZIP_STORED, allowZip64=True, \
                     optimize=-1)

   .. versionchanged:: 3.2
      Đã thêm tham số *optimize*.

   .. versionchanged:: 3.4
      Các phần mở rộng ZIP64 được bật theo mặc định.

   Các instance có thêm một phương thức ngoài những phương thức của các đối tượng :class:`ZipFile`:

   .. method:: PyZipFile.writepy(pathname, basename='', filterfunc=None)

      Tìm kiếm các tệp :file:`\*.py` và thêm tệp tương ứng vào archive.

      Nếu tham số *optimize* của :class:`PyZipFile` không được cung cấp hoặc là ``-1``, tệp tương ứng là tệp :file:`\*.pyc`, được biên dịch nếu cần.

      Nếu tham số *optimize* của :class:`PyZipFile` là ``0``, ``1`` hoặc ``2``, chỉ các tệp có mức tối ưu hóa đó (xem :func:`compile`) mới được thêm vào archive, được biên dịch nếu cần.

      Nếu *pathname* là một tệp, tên tệp phải kết thúc bằng :file:`.py`, và chỉ tệp (tương ứng với :file:`\*.pyc`) được thêm ở cấp cao nhất (không có thông tin đường dẫn). Nếu *pathname* là một tệp không kết thúc bằng
      :file:`.py`, một :exc:`RuntimeError` sẽ được raise. Nếu đó là một thư mục và thư mục đó không phải là thư mục package, thì tất cả các tệp
      :file:`\*.pyc` sẽ được thêm ở cấp cao nhất. Nếu thư mục đó là một thư mục package, thì tất cả :file:`\*.pyc` sẽ được thêm dưới tên package dưới dạng đường dẫn tệp; nếu có thư mục con nào là thư mục package, tất cả chúng sẽ được thêm đệ quy theo thứ tự sắp xếp.

      *basename* chỉ предназнач cho việc sử dụng nội bộ.

      *filterfunc*, nếu được cung cấp, phải là một hàm nhận một đối số chuỗi duy nhất. Hàm này sẽ được truyền từng đường dẫn (bao gồm từng đường dẫn tệp đầy đủ) trước khi đường dẫn đó được thêm vào archive. Nếu *filterfunc* trả về giá trị false, đường dẫn đó sẽ không được thêm vào; nếu đó là một thư mục, nội dung của nó sẽ bị bỏ qua. Ví dụ, nếu tất cả các tệp kiểm thử của chúng ta либо nằm trong các thư mục ``test`` hoặc bắt đầu bằng chuỗi ``test_``, chúng ta có thể sử dụng một *filterfunc* để loại trừ chúng::

          >>> zf = PyZipFile('myprog.zip')
          >>> def notests(s):
          ...     fn = os.path.basename(s)
          ...     return (not (fn == 'test' or fn.startswith('test_')))
          ...
          >>> zf.writepy('myprog', filterfunc=notests)

      Phương thức :meth:`writepy` tạo các archive có tên tệp như sau::

         string.pyc                   # Tên cấp cao nhất
         test/__init__.pyc            # Thư mục package
         test/testall.pyc             # Mô-đun test.testall
         test/bogus/__init__.pyc      # Thư mục subpackage
         test/bogus/myfile.pyc        # Submodule test.bogus.myfile

      .. versionchanged:: 3.4
         Đã thêm tham số *filterfunc*.

      .. versionchanged:: 3.6.2
         Tham số *pathname* chấp nhận một :term:`path-like object`.

      .. versionchanged:: 3.7
         Đệ quy sắp xếp các mục nhập thư mục.


.. _zipinfo-objects:

Các đối tượng ZipInfo
---------------------

Các instance của lớp :class:`ZipInfo` được trả về bởi :meth:`.getinfo` và
các phương thức :meth:`.infolist` của các đối tượng :class:`ZipFile`. Mỗi đối tượng lưu trữ thông tin về một thành phần riêng lẻ của kho lưu trữ ZIP.

Có một classmethod để tạo một instance :class:`ZipInfo` cho một tệp trong hệ thống tệp:

.. classmethod:: ZipInfo.from_file(filename, arcname=None, *, \
                                   strict_timestamps=True)

   Tạo một instance :class:`ZipInfo` cho một tệp trong hệ thống tệp, để chuẩn bị thêm tệp đó vào tệp zip.

   *filename* phải là đường dẫn đến một tệp hoặc thư mục trong hệ thống tệp.

   Nếu chỉ định *arcname*, giá trị này sẽ được dùng làm tên bên trong kho lưu trữ. Nếu không chỉ định *arcname*, tên sẽ giống với *filename*, nhưng mọi ký tự ổ đĩa và dấu phân cách đường dẫn ở đầu sẽ bị loại bỏ.

   Đối số *strict_timestamps*, khi được đặt thành ``False``, cho phép nén các tệp cũ hơn 1980-01-01, nhưng phải đặt dấu thời gian thành 1980-01-01. Hành vi tương tự xảy ra với các tệp mới hơn 2107-12-31; dấu thời gian cũng được đặt thành giới hạn này.

   .. versionadded:: 3.6

   .. versionchanged:: 3.6.2
      Tham số *filename* chấp nhận một :term:`path-like object`.

   .. versionchanged:: 3.8
      Đã thêm tham số chỉ nhận bằng từ khóa *strict_timestamps*.


Các instance có những phương thức và thuộc tính sau:

.. method:: ZipInfo.is_dir()

   Trả về ``True`` nếu thành viên này của archive là một thư mục.

   Điều này sử dụng tên của entry: các thư mục luôn phải kết thúc bằng ``/``.

   .. versionadded:: 3.6


.. attribute:: ZipInfo.filename

   Tên của tệp trong archive.


.. attribute:: ZipInfo.date_time

   Thời gian và ngày sửa đổi lần cuối của thành viên lưu trữ. Đây là một tuple gồm sáu giá trị, biểu thị các trường "thời gian tệp [được sửa đổi] lần cuối" và "ngày tệp [được sửa đổi] lần cuối" trong thư mục trung tâm của tệp ZIP.

   Tuple này chứa:

   +---------+-----------------------------------+
   | Chỉ mục | Giá trị                           |
   +=========+===================================+
   | ``0``   | Năm (>= 1980)                     |
   +---------+-----------------------------------+
   | ``1``   | Tháng (đánh số từ một)            |
   +---------+-----------------------------------+
   | ``2``   | Ngày trong tháng (đánh số từ một) |
   +---------+-----------------------------------+
   | ``3``   | Giờ (đánh số từ 0)                |
   +---------+-----------------------------------+
   | ``4``   | Phút (đánh số từ 0)               |
   +---------+-----------------------------------+
   | ``5``   | Giây (đánh số từ 0)               |
   +---------+-----------------------------------+

   .. note::

      Định dạng ZIP hỗ trợ nhiều trường dấu thời gian ở các vị trí khác nhau (thư mục trung tâm, các trường bổ sung cho hệ thống NTFS/UNIX, v.v.). Thuộc tính này cụ thể trả về dấu thời gian từ thư mục trung tâm. Định dạng dấu thời gian của thư mục trung tâm trong các tệp ZIP không hỗ trợ dấu thời gian trước
      1980. Mặc dù một số định dạng trường bổ sung (chẳng hạn như dấu thời gian UNIX) có thể biểu diễn
      các ngày sớm hơn, thuộc tính này chỉ trả về dấu thời gian của thư mục trung tâm.

      Dấu thời gian của thư mục trung tâm được hiểu là giờ địa phương, thay vì giờ UTC, để phù hợp với hành vi của các công cụ zip khác.


.. attribute:: ZipInfo.compress_type

   Loại nén của thành viên archive.


.. attribute:: ZipInfo.comment

   Chú thích cho thành viên archive riêng lẻ dưới dạng đối tượng :class:`bytes`.


.. attribute:: ZipInfo.extra

   Dữ liệu trường mở rộng. `Ghi chú ứng dụng PKZIP <PKZIP Application Note_>`_ có chứa một số nhận xét về cấu trúc nội bộ của dữ liệu có trong
   đối tượng :class:`bytes`.


.. attribute:: ZipInfo.create_system

   Hệ thống đã tạo archive ZIP.


.. attribute:: ZipInfo.create_version

   Phiên bản PKZIP đã tạo archive ZIP.


.. attribute:: ZipInfo.extract_version

   Phiên bản PKZIP cần thiết để giải nén archive.


.. attribute:: ZipInfo.reserved

   Phải bằng không.


.. attribute:: ZipInfo.flag_bits

   Các bit cờ ZIP.


.. attribute:: ZipInfo.volume

   Số volume của header tệp.


.. attribute:: ZipInfo.internal_attr

   Các thuộc tính nội bộ.


.. attribute:: ZipInfo.external_attr

   Các thuộc tính tệp bên ngoài.


.. attribute:: ZipInfo.header_offset

   Độ lệch byte đến header tệp.


.. attribute:: ZipInfo.CRC

   CRC-32 của tệp chưa giải nén.


.. attribute:: ZipInfo.compress_size

   Kích thước của dữ liệu đã nén.


.. attribute:: ZipInfo.file_size

   Kích thước của tệp chưa nén.


.. _zipfile-commandline:
.. program:: zipfile

Giao diện dòng lệnh
-------------------

Mô-đun :mod:`!zipfile` cung cấp một giao diện dòng lệnh đơn giản để tương tác với các kho lưu trữ ZIP.

Nếu muốn tạo một kho lưu trữ ZIP mới, hãy chỉ định tên của kho lưu trữ sau tùy chọn :option:`-c`, sau đó liệt kê (các) tên tệp cần đưa vào:

.. code-block:: shell-session

    $ python -m zipfile -c monty.zip spam.txt eggs.txt

Bạn cũng có thể truyền vào một thư mục:

.. code-block:: shell-session

    $ python -m zipfile -c monty.zip life-of-brian_1979/

Nếu muốn giải nén một kho lưu trữ ZIP vào thư mục được chỉ định, hãy sử dụng tùy chọn :option:`-e`:

.. code-block:: shell-session

    $ python -m zipfile -e monty.zip target-dir/

Để liệt kê các tệp trong một kho lưu trữ ZIP, hãy sử dụng tùy chọn :option:`-l`:

.. code-block:: shell-session

    $ python -m zipfile -l monty.zip


Các tùy chọn dòng lệnh
~~~~~~~~~~~~~~~~~~~~~~

.. option:: -l <zipfile>
            --list <zipfile>

   Liệt kê các tệp trong tệp ZIP.

.. option:: -c <zipfile> <source1> ... <sourceN>
            --create <zipfile> <source1> ... <sourceN>

   Tạo tệp ZIP từ các tệp nguồn.

.. option:: -e <zipfile> <output_dir>
            --extract <zipfile> <output_dir>

   Giải nén zipfile vào thư mục đích.

.. option:: -t <zipfile>
            --test <zipfile>

   Kiểm tra xem zipfile có hợp lệ hay không.

.. option:: --metadata-encoding <encoding>

   Chỉ định encoding của tên thành viên cho :option:`-l`, :option:`-e` và
   :option:`-t`.

   .. versionadded:: 3.11


Các cạm bẫy khi giải nén
------------------------

Việc giải nén trong module zipfile có thể thất bại do một số cạm bẫy được liệt kê dưới đây.

Từ chính tệp
~~~~~~~~~~~~

Việc giải nén có thể không thành công do mật khẩu không đúng, lỗi checksum CRC, định dạng ZIP hoặc phương thức nén/giải mã không được hỗ trợ.

Các giới hạn của hệ thống tệp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Việc vượt quá các giới hạn trên những hệ thống tệp khác nhau có thể khiến quá trình giải nén thất bại. Ví dụ: các ký tự được phép trong các mục thư mục, độ dài tên tệp, độ dài đường dẫn, kích thước của một tệp đơn lẻ và số lượng tệp, v.v.

.. _zipfile-resources-limitations:

Các giới hạn về tài nguyên
~~~~~~~~~~~~~~~~~~~~~~~~~~

Thiếu bộ nhớ hoặc dung lượng đĩa có thể khiến quá trình giải nén thất bại. Ví dụ, các bom giải nén (còn gọi là `bom ZIP <ZIP bomb_>`_) áp dụng cho thư viện zipfile có thể khiến dung lượng đĩa bị cạn kiệt.

Gián đoạn
~~~~~~~~~

Việc bị gián đoạn trong quá trình giải nén, chẳng hạn như nhấn control-C hoặc dừng tiến trình giải nén, có thể khiến quá trình giải nén kho lưu trữ không hoàn tất.

Hành vi mặc định khi giải nén
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Không nắm được các hành vi mặc định khi giải nén có thể dẫn đến kết quả giải nén không mong muốn. Ví dụ: khi giải nén cùng một archive hai lần, chương trình sẽ ghi đè các tệp mà không hỏi.


.. _ZIP bomb: https://en.wikipedia.org/wiki/Zip_bomb
.. _PKZIP Application Note: https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT

.. _`Info-ZIP Home Page`: https://infozip.sourceforge.net/
