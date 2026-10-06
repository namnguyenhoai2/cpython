:mod:`!compression.zstd` --- Nén tương thích với định dạng Zstandard
====================================================================

.. module:: compression.zstd
   :synopsis: Giao diện cấp thấp cho các routine nén và giải nén trong thư viện zstd.

.. versionadded:: 3.14

**Mã nguồn:** :source:`Lib/compression/zstd/__init__.py`

--------------

Mô-đun này cung cấp các lớp và hàm để nén và giải nén dữ liệu bằng thuật toán nén Zstandard (hay *zstd*). `Sổ tay zstd <https://facebook.github.io/zstd/doc/api_manual_latest.html>`__ mô tả Zstandard là "một thuật toán nén không mất dữ liệu nhanh, hướng đến các kịch bản nén theo thời gian thực với tốc độ ở mức zlib và tỷ lệ nén tốt hơn." Ngoài ra còn có một giao diện tệp hỗ trợ đọc và ghi nội dung của các tệp ``.zst`` được tạo bởi tiện ích :program:`zstd`, cũng như các luồng nén zstd thô.

Mô-đun :mod:`!compression.zstd` chứa:

* Hàm :func:`.open` và lớp :class:`ZstdFile` để đọc và ghi các tệp đã nén.
* Các lớp :class:`ZstdCompressor` và :class:`ZstdDecompressor` để nén và giải nén tăng dần.
* Các hàm :func:`compress` và :func:`decompress` để nén/giải nén một lần.
* Các hàm :func:`train_dict` và :func:`finalize_dict` cùng
  lớp :class:`ZstdDict` để huấn luyện và quản lý các từ điển Zstandard.
* Các lớp :class:`CompressionParameter`, :class:`DecompressionParameter` và
  :class:`Strategy` để thiết lập các tham số nén/giải nén nâng cao.

.. include:: ../includes/optional-module.rst


Ngoại lệ
--------

.. exception:: ZstdError

   Ngoại lệ này được nâng lên khi xảy ra lỗi trong quá trình nén hoặc giải nén, hoặc khi khởi tạo trạng thái của bộ nén/giải nén.


Đọc và ghi tệp được nén
-----------------------

.. function:: open(file, /, mode='rb', *, level=None, options=None, \
                   zstd_dict=None, encoding=None, errors=None, newline=None)

   Mở tệp được nén bằng Zstandard ở chế độ nhị phân hoặc văn bản, trả về một
   :term:`file object`.

   Đối số *file* có thể là tên tệp (được cung cấp dưới dạng
   :class:`str`, :class:`bytes` hoặc :term:`path-like <path-like object>`), trong trường hợp đó tệp có tên tương ứng sẽ được mở; hoặc có thể là một đối tượng tệp hiện có để đọc từ đó hoặc ghi vào đó.

   Đối số mode có thể là ``'rb'`` để đọc (mặc định), ``'wb'`` để ghi đè, ``'ab'`` để nối thêm hoặc ``'xb'`` để tạo độc quyền. Tương ứng, bạn cũng có thể cung cấp các giá trị này dưới dạng ``'r'``, ``'w'``, ``'a'`` và ``'x'``. Bạn cũng có thể mở ở chế độ văn bản bằng lần lượt các giá trị ``'rt'``, ``'wt'``, ``'at'`` và ``'xt'``.

   Khi đọc, đối số *options* có thể là một dictionary cung cấp các tham số giải nén nâng cao; xem :class:`DecompressionParameter` để biết thông tin chi tiết về các tham số được hỗ trợ. Đối số *zstd_dict* là một thực thể :class:`ZstdDict` được sử dụng trong quá trình giải nén. Khi đọc, nếu đối số *level* không phải là None, một :exc:`!TypeError` sẽ được raised.

   Khi ghi dữ liệu, đối số *options* có thể là một dictionary cung cấp các tham số compression nâng cao; xem
   :class:`CompressionParameter` để biết thông tin chi tiết về các tham số được hỗ trợ. Đối số *level* là compression level được sử dụng khi ghi dữ liệu đã nén. Chỉ một trong hai đối số *level* hoặc *options* có thể khác None. Đối số *zstd_dict* là một instance :class:`ZstdDict` được sử dụng trong quá trình compression.

   Ở chế độ nhị phân, hàm này tương đương với constructor :class:`ZstdFile`: ``ZstdFile(file, mode, ...)``. Trong trường hợp này, không được cung cấp các tham số *encoding*, *errors* và *newline*.

   Ở chế độ văn bản, một đối tượng :class:`ZstdFile` được tạo và bọc trong một
   instance :class:`io.TextIOWrapper` với encoding, behavior xử lý lỗi và line ending được chỉ định.


.. class:: ZstdFile(file, /, mode='rb', *, level=None, options=None, \
                    zstd_dict=None)

   Mở tệp được nén bằng Zstandard ở chế độ nhị phân.

   Một :class:`ZstdFile` có thể bao bọc một :term:`file object` đã được mở sẵn hoặc hoạt động trực tiếp trên một tệp có tên. Đối số *file* chỉ định đối tượng tệp cần bao bọc hoặc tên tệp cần mở (dưới dạng :class:`str`,
   :class:`bytes` hoặc đối tượng :term:`path-like <path-like object>`). Nếu bao bọc một đối tượng tệp hiện có, tệp được bao bọc sẽ không bị đóng khi :class:`ZstdFile` được đóng.

   Đối số *mode* có thể là ``'rb'`` để đọc (mặc định), ``'wb'`` để ghi đè, ``'xb'`` để tạo độc quyền hoặc ``'ab'`` để nối thêm. Các giá trị này tương đương với ``'r'``, ``'w'``, ``'x'`` và ``'a'`` tương ứng.

   Nếu *file* là một đối tượng tệp (thay vì tên tệp thực tế), chế độ ``'w'`` sẽ không cắt ngắn tệp mà thay vào đó tương đương với ``'a'``.

   Khi đọc, đối số *options* có thể là một dictionary cung cấp các tham số giải nén nâng cao; xem
   :class:`DecompressionParameter` để biết thông tin chi tiết về các tham số được hỗ trợ. Đối số *zstd_dict* là một instance :class:`ZstdDict` được sử dụng trong quá trình giải nén. Khi đọc, nếu đối số *level* không phải là None, một :exc:`!TypeError` sẽ được đưa ra.

   Khi ghi dữ liệu, đối số *options* có thể là một dictionary cung cấp các tham số compression nâng cao; xem
   :class:`CompressionParameter` để biết thông tin chi tiết về các tham số được hỗ trợ. Đối số *level* là cấp độ nén được sử dụng khi ghi dữ liệu đã nén. Chỉ có thể truyền một trong *level* hoặc *options*. Đối số *zstd_dict* là một thể hiện :class:`ZstdDict` được sử dụng trong quá trình nén.

   :class:`!ZstdFile` hỗ trợ tất cả các thành viên được chỉ định bởi
   :class:`io.BufferedIOBase`, ngoại trừ :meth:`~io.BufferedIOBase.detach` và :meth:`~io.IOBase.truncate`. Việc lặp và câu lệnh :keyword:`with` được hỗ trợ.

   Các phương thức và thuộc tính sau đây cũng được cung cấp:

   .. method:: peek(size=-1)

      Trả về dữ liệu đã đệm mà không làm thay đổi vị trí tệp. Sẽ trả về ít nhất một byte dữ liệu, trừ khi đã đến EOF. Số byte chính xác được trả về không được xác định (đối số *size* bị bỏ qua).

      .. note:: Mặc dù việc gọi :meth:`peek` không làm thay đổi vị trí tệp của :class:`ZstdFile`, thao tác này có thể làm thay đổi vị trí của đối tượng tệp bên dưới (ví dụ: nếu :class:`ZstdFile` được tạo bằng cách truyền một đối tượng tệp cho *file*).

   .. attribute:: mode

      ``'rb'`` để đọc và ``'wb'`` để ghi.

   .. attribute:: name

      Tên của tệp Zstandard. Tương đương với thuộc tính :attr:`~io.FileIO.name` của :term:`file object` bên dưới.


Nén và giải nén dữ liệu trong bộ nhớ
------------------------------------

.. function:: compress(data, level=None, options=None, zstd_dict=None)

   Nén *data* (một :term:`bytes-like object`), trả về dữ liệu đã nén dưới dạng đối tượng :class:`bytes`.

   Đối số *level* là một số nguyên dùng để kiểm soát mức độ nén. *level* là một lựa chọn thay thế cho việc thiết lập
   :attr:`CompressionParameter.compression_level` trong *options*. Sử dụng
   :meth:`~CompressionParameter.bounds` trên
   :attr:`~CompressionParameter.compression_level` để nhận các giá trị có thể truyền cho *level*. Nếu cần các tùy chọn nén nâng cao, phải bỏ qua đối số *level* và trong từ điển *options*
   Tham số :attr:`!CompressionParameter.compression_level` cần được đặt.

   Đối số *options* là một dictionary Python chứa các tham số nén nâng cao. Các khóa và giá trị hợp lệ cho các tham số nén được ghi lại trong tài liệu :class:`CompressionParameter`.

   Đối số *zstd_dict* là một thực thể của :class:`ZstdDict` chứa dữ liệu đã được huấn luyện để cải thiện hiệu quả nén. Có thể sử dụng hàm :func:`train_dict` để tạo dictionary Zstandard.


.. function:: decompress(data, zstd_dict=None, options=None)

   Giải nén *data* (một :term:`bytes-like object`), trả về dữ liệu chưa nén dưới dạng đối tượng :class:`bytes`.

   Đối số *options* là một dictionary Python chứa các tham số giải nén nâng cao. Các khóa và giá trị hợp lệ cho các tham số nén được ghi lại trong tài liệu :class:`DecompressionParameter`.

   Đối số *zstd_dict* là một thực thể của :class:`ZstdDict` chứa dữ liệu đã được huấn luyện được sử dụng trong quá trình nén. Đây phải là dictionary Zstandard được sử dụng trong quá trình nén.

   Nếu *data* là phần nối của nhiều frame nén riêng biệt, hãy giải nén tất cả các frame này và trả về phần nối của các kết quả.


.. class:: ZstdCompressor(level=None, options=None, zstd_dict=None)

   Tạo một đối tượng compressor, có thể được dùng để nén dữ liệu theo từng phần.

   Để có cách thuận tiện hơn nhằm nén một khối dữ liệu đơn lẻ, hãy xem hàm cấp mô-đun :func:`compress`.

   Đối số *level* là một số nguyên dùng để kiểm soát mức độ nén. *level* là một lựa chọn thay thế cho việc thiết lập
   :attr:`CompressionParameter.compression_level` trong *options*. Sử dụng
   :meth:`~CompressionParameter.bounds` trên
   :attr:`~CompressionParameter.compression_level` để nhận các giá trị có thể truyền cho *level*. Nếu cần các tùy chọn nén nâng cao, phải bỏ qua đối số *level* và trong từ điển *options*
   Tham số :attr:`!CompressionParameter.compression_level` cần được đặt.

   Đối số *options* là một dictionary Python chứa các tham số nén nâng cao. Các khóa và giá trị hợp lệ cho các tham số nén được ghi lại trong tài liệu :class:`CompressionParameter`.

   Đối số *zstd_dict* là một thể hiện tùy chọn của :class:`ZstdDict` chứa dữ liệu đã được huấn luyện để cải thiện hiệu quả nén. Có thể sử dụng hàm :func:`train_dict` để tạo một từ điển Zstandard.


   .. method:: compress(data, mode=ZstdCompressor.CONTINUE)

      Nén *data* (một :term:`bytes-like object`), trả về một đối tượng :class:`bytes` chứa dữ liệu đã nén nếu có thể, hoặc nếu không thì trả về một đối tượng rỗng
      :class:`!bytes`. Một phần *data* có thể được lưu vào bộ đệm nội bộ để sử dụng trong các lần gọi sau đến :meth:`!compress` và :meth:`~.flush`. Dữ liệu trả về phải được nối với đầu ra của mọi lần gọi trước đó đến
      :meth:`~.compress`.

      Đối số *mode* là một thuộc tính :class:`ZstdCompressor`, có thể là
      :attr:`~.CONTINUE`, :attr:`~.FLUSH_BLOCK` hoặc :attr:`~.FLUSH_FRAME`.

      Khi đã cung cấp toàn bộ dữ liệu cho compressor, hãy gọi
      :meth:`~.flush` để hoàn tất quá trình nén. Nếu
      :meth:`~.compress` được gọi với *mode* được đặt thành :attr:`~.FLUSH_FRAME`,
      Không nên gọi :meth:`~.flush`, vì thao tác này sẽ ghi ra một frame trống mới.

   .. method:: flush(mode=ZstdCompressor.FLUSH_FRAME)

      Hoàn tất quá trình nén và trả về một đối tượng :class:`bytes` chứa mọi dữ liệu được lưu trong các bộ đệm nội bộ của compressor.

      Đối số *mode* là một thuộc tính :class:`ZstdCompressor`, có thể là
      :attr:`~.FLUSH_BLOCK`, hoặc :attr:`~.FLUSH_FRAME`.

   .. method:: set_pledged_input_size(size)

      Chỉ định lượng dữ liệu chưa nén *size* sẽ được cung cấp cho frame tiếp theo. *size* sẽ được ghi vào phần header của frame tiếp theo, trừ khi :attr:`CompressionParameter.content_size_flag` là ``False`` hoặc ``0``. Kích thước ``0`` nghĩa là frame trống. Nếu *size* là ``None``, phần header của frame sẽ không bao gồm kích thước frame. Các frame có chứa kích thước dữ liệu chưa nén sẽ cần ít bộ nhớ hơn để giải nén, đặc biệt ở các mức nén cao hơn.

      Nếu :attr:`last_mode` không phải là :attr:`FLUSH_FRAME`, một
      :exc:`ValueError` sẽ được phát sinh vì compressor không ở đầu frame. Nếu kích thước đã cam kết không khớp với kích thước thực tế của dữ liệu được cung cấp cho :meth:`.compress`, các lần gọi :meth:`!compress` tiếp theo hoặc
      :meth:`flush` có thể phát sinh :exc:`ZstdError` và phần dữ liệu cuối cùng có thể bị mất.

      Sau khi :meth:`flush` hoặc :meth:`.compress` được gọi với mode
      :attr:`FLUSH_FRAME`, frame tiếp theo sẽ không đưa kích thước frame vào header, trừ khi :meth:`!set_pledged_input_size` được gọi lại.

   .. attribute:: CONTINUE

      Thu thập thêm dữ liệu để nén; thao tác này có thể tạo hoặc không tạo output ngay lập tức. Mode này tối ưu hóa tỷ lệ nén bằng cách tối đa hóa lượng dữ liệu trong mỗi block và frame.

   .. attribute:: FLUSH_BLOCK

      Hoàn tất và ghi một block vào data stream. Dữ liệu được trả về cho đến thời điểm này có thể được giải nén ngay lập tức. Dữ liệu trước đó vẫn có thể được tham chiếu trong các block tiếp theo do các lệnh gọi đến :meth:`~.compress` tạo ra, giúp cải thiện khả năng nén.

   .. attribute:: FLUSH_FRAME

      Hoàn tất và ghi ra một frame. Dữ liệu trong tương lai được cung cấp cho
      :meth:`~.compress` sẽ được ghi vào một frame mới và *không thể* tham chiếu đến dữ liệu trước đó.

   .. attribute:: last_mode

      Chế độ gần đây nhất được truyền vào :meth:`~.compress` hoặc :meth:`~.flush`. Giá trị này có thể là một trong :attr:`~.CONTINUE`, :attr:`~.FLUSH_BLOCK` hoặc
      :attr:`~.FLUSH_FRAME`. Giá trị ban đầu là :attr:`~.FLUSH_FRAME`, cho biết compressor đang ở đầu một frame mới.


.. class:: ZstdDecompressor(zstd_dict=None, options=None)

   Tạo một đối tượng decompressor, có thể được dùng để giải nén dữ liệu theo từng phần.

   Để có cách thuận tiện hơn khi giải nén toàn bộ compressed stream cùng lúc, hãy xem hàm cấp module :func:`decompress`.

   Đối số *options* là một dictionary Python chứa các tham số giải nén nâng cao. Các khóa và giá trị hợp lệ cho các tham số nén được ghi lại trong tài liệu :class:`DecompressionParameter`.

   Đối số *zstd_dict* là một thực thể của :class:`ZstdDict` chứa dữ liệu đã được huấn luyện được sử dụng trong quá trình nén. Đây phải là dictionary Zstandard được sử dụng trong quá trình nén.

   .. note::
      Lớp này không tự động xử lý các đầu vào chứa nhiều frame đã nén, khác với hàm :func:`decompress` và
      lớp :class:`ZstdFile`. Để giải nén đầu vào nhiều frame, bạn nên sử dụng :func:`decompress`, :class:`ZstdFile` nếu đang làm việc với một
      :term:`file object`, hoặc nhiều instance :class:`!ZstdDecompressor`.

   .. method:: decompress(data, max_length=-1)

      Giải nén *data* (một :term:`bytes-like object`), trả về dữ liệu chưa nén dưới dạng byte. Một phần *data* có thể được đệm nội bộ để sử dụng trong các lần gọi sau đến :meth:`!decompress`. Dữ liệu được trả về nên được nối với kết quả của mọi lần gọi trước đó đến :meth:`!decompress`.

      Nếu *max_length* không âm, phương thức sẽ trả về nhiều nhất *max_length* byte dữ liệu đã giải nén. Nếu đạt đến giới hạn này và vẫn có thể tạo thêm đầu ra, thuộc tính :attr:`~.needs_input` sẽ được đặt thành ``False``. Trong trường hợp này, lần gọi tiếp theo đến
      :meth:`~.decompress` có thể cung cấp *data* làm ``b''`` để lấy thêm phần đầu ra.

      Nếu toàn bộ dữ liệu đầu vào đã được giải nén và trả về (either vì dữ liệu có kích thước nhỏ hơn *max_length* byte, hoặc vì *max_length* là số âm), thuộc tính :attr:`~.needs_input` sẽ được đặt thành ``True``.

      Việc cố gắng giải nén dữ liệu sau phần cuối của một frame sẽ gây ra một
      :exc:`EOFError`. Mọi dữ liệu được tìm thấy sau phần cuối của frame sẽ bị bỏ qua và được lưu trong thuộc tính :attr:`~.unused_data`.

   .. attribute:: eof

      ``True`` nếu đã đạt đến marker kết thúc luồng.

   .. attribute:: unused_data

      Dữ liệu được tìm thấy sau phần cuối của luồng đã nén.

      Trước khi đạt đến phần cuối của luồng, giá trị này sẽ là ``b''``.

   .. attribute:: needs_input

      ``False`` nếu phương thức :meth:`.decompress` có thể cung cấp thêm dữ liệu đã giải nén trước khi cần dữ liệu đầu vào đã nén mới.


Các dictionary của Zstandard
----------------------------


.. function:: train_dict(samples, dict_size)

   Huấn luyện một dictionary của Zstandard và trả về một instance :class:`ZstdDict`. Các dictionary của Zstandard cho phép nén hiệu quả hơn các tập dữ liệu nhỏ, vốn thường khó nén do có ít sự lặp lại hơn. Nếu bạn đang nén nhiều nhóm dữ liệu tương tự nhau (chẳng hạn như các tệp tương tự nhau), các dictionary của Zstandard có thể cải thiện đáng kể tỷ lệ và tốc độ nén.

   Đối số *samples* (một iterable gồm các đối tượng :class:`bytes`) là tập hợp các mẫu được dùng để huấn luyện dictionary của Zstandard.

   Đối số *dict_size*, một số nguyên, là kích thước tối đa (tính bằng byte) mà dictionary của Zstandard nên có. Tài liệu Zstandard đề xuất giới hạn tuyệt đối không quá 100 KB, nhưng giới hạn tối đa thường có thể nhỏ hơn tùy thuộc vào dữ liệu. Dictionary lớn hơn thường làm chậm quá trình nén nhưng cải thiện tỷ lệ nén. Dictionary nhỏ hơn giúp nén nhanh hơn nhưng làm giảm tỷ lệ nén.


.. function:: finalize_dict(zstd_dict, /, samples, dict_size, level)

   Một hàm nâng cao để chuyển đổi dictionary của Zstandard "raw content" thành dictionary Zstandard thông thường. Các dictionary "raw content" là một chuỗi byte không cần tuân theo cấu trúc của dictionary Zstandard thông thường.

   Đối số *zstd_dict* là một instance :class:`ZstdDict` có :attr:`~ZstdDict.dict_content` chứa nội dung dictionary thô.

   Đối số *samples* (một iterable gồm các đối tượng :class:`bytes`) chứa dữ liệu mẫu để tạo dictionary của Zstandard.

   Đối số *dict_size*, là một số nguyên, là kích thước tối đa (tính bằng byte) mà từ điển Zstandard nên có. Xem :func:`train_dict` để biết các đề xuất về kích thước từ điển tối đa.

   Đối số *level* (một số nguyên) là mức nén dự kiến được truyền cho các compressor sử dụng từ điển này. Thông tin từ điển thay đổi theo từng mức nén, vì vậy việc tinh chỉnh để chọn đúng mức nén có thể giúp quá trình nén hiệu quả hơn.


.. class:: ZstdDict(dict_content, /, *, is_raw=False)

   Một wrapper cho các từ điển Zstandard. Có thể sử dụng từ điển để cải thiện khả năng nén nhiều đoạn dữ liệu nhỏ. Hãy sử dụng :func:`train_dict` nếu bạn cần huấn luyện một từ điển mới từ dữ liệu mẫu.

   Đối số *dict_content* (một :term:`bytes-like object`) là thông tin từ điển đã được huấn luyện.

   Đối số *is_raw*, một giá trị boolean, là tham số nâng cao dùng để kiểm soát ý nghĩa của *dict_content*. ``True`` có nghĩa là *dict_content* là một từ điển "raw content", không có bất kỳ hạn chế định dạng nào. ``False`` có nghĩa là *dict_content* là một từ điển Zstandard thông thường, được tạo từ các hàm Zstandard, chẳng hạn như :func:`train_dict` hoặc CLI :program:`zstd` bên ngoài.

   Khi truyền một :class:`!ZstdDict` cho một hàm,
   Các thuộc tính :attr:`!as_digested_dict` và :attr:`!as_undigested_dict` có thể kiểm soát cách từ điển được tải bằng cách truyền chúng dưới dạng đối số ``zstd_dict``, chẳng hạn như ``compress(data, zstd_dict=zd.as_digested_dict)``. Việc digest một từ điển là thao tác tốn kém, xảy ra khi tải một từ điển Zstandard. Khi thực hiện nhiều lần gọi đến compression hoặc decompression, việc truyền một từ điển đã được digest sẽ giảm chi phí tải từ điển.

    .. list-table:: Sự khác biệt khi nén
       :widths: 10 14 10
       :header-rows: 1

       * -
         - Dictionary đã được xử lý
         - Dictionary chưa được xử lý
       * - Các tham số nâng cao của compressor có thể được ghi đè bởi các tham số của dictionary
         - ``window_log``, ``hash_log``, ``chain_log``, ``search_log``, ``min_match``, ``target_length``, ``strategy``, ``enable_long_distance_matching``, ``ldm_hash_log``, ``ldm_min_match``, ``ldm_bucket_size_log``, ``ldm_hash_rate_log``, và một số tham số không công khai.
         - Không có
       * - :class:`!ZstdDict` nội bộ lưu dictionary vào bộ nhớ đệm
         - Đúng vậy. Việc tải lại một từ điển đã digest sẽ nhanh hơn khi sử dụng cùng một mức compression.
         - Không. Nếu muốn tải một từ điển chưa digest nhiều lần, hãy cân nhắc việc sử dụng lại một đối tượng compressor.

   Nếu truyền một :class:`!ZstdDict` mà không có thuộc tính nào, theo mặc định, một từ điển chưa digest sẽ được truyền khi nén, còn một từ điển đã digest sẽ được tạo nếu cần và được truyền theo mặc định khi giải nén.

    .. attribute:: dict_content

        Nội dung của từ điển Zstandard, một đối tượng ``bytes``. Nội dung này giống với đối số *dict_content* trong phương thức ``__init__``. Nó có thể được sử dụng với các chương trình khác, chẳng hạn như chương trình CLI ``zstd``.

    .. attribute:: dict_id

        Mã định danh của từ điển Zstandard, một giá trị int không âm.

        Giá trị khác không có nghĩa là từ điển thông thường, được tạo bởi các hàm Zstandard và tuân theo định dạng Zstandard.

        ``0`` có nghĩa là từ điển “raw content”, không bị giới hạn bởi bất kỳ định dạng nào và dành cho người dùng nâng cao.

        .. note::

            Ý nghĩa của ``0`` đối với :attr:`!ZstdDict.dict_id` khác với thuộc tính ``dictionary_id`` của hàm :func:`get_frame_info`.

    .. attribute:: as_digested_dict

        Tải dưới dạng dictionary đã được digest.

    .. attribute:: as_undigested_dict

        Tải dưới dạng dictionary chưa được digest.


Điều khiển tham số nâng cao
---------------------------

.. class:: CompressionParameter()

   Một :class:`~enum.IntEnum` chứa các khóa tham số nén nâng cao có thể được sử dụng khi nén dữ liệu.

   Có thể sử dụng phương thức :meth:`~.bounds` trên bất kỳ thuộc tính nào để lấy các giá trị hợp lệ cho tham số đó.

   Các tham số là tùy chọn; mọi tham số bị bỏ qua sẽ được tự động chọn giá trị.

   Ví dụ lấy giới hạn dưới và giới hạn trên của :attr:`~.compression_level`::

      lower, upper = CompressionParameter.compression_level.bounds()

   Ví dụ đặt :attr:`~.window_log` thành kích thước tối đa::

      _lower, upper = CompressionParameter.window_log.bounds()
      options = {CompressionParameter.window_log: upper}
      compress(b'venezuelan beaver cheese', options=options)

   .. method:: bounds()

      Trả về tuple gồm các giới hạn int, ``(lower, upper)``, của một tham số nén. Phương thức này nên được gọi trên thuộc tính mà bạn muốn lấy các giới hạn. Ví dụ: để lấy các giá trị hợp lệ cho
      :attr:`~.compression_level`, bạn có thể kiểm tra kết quả của ``CompressionParameter.compression_level.bounds()``.

      Cả giới hạn dưới và giới hạn trên đều được tính.

   .. attribute:: compression_level

      Một cách cấp cao để thiết lập các tham số nén khác ảnh hưởng đến tốc độ và tỷ lệ nén dữ liệu.

      Các cấp độ nén thông thường lớn hơn ``0``. Các giá trị lớn hơn ``20`` được xem là mức nén "ultra" và cần nhiều bộ nhớ hơn các cấp độ khác. Có thể sử dụng các giá trị âm để đánh đổi tốc độ nén nhanh hơn lấy tỷ lệ nén kém hơn.

      Đặt mức này bằng không sẽ sử dụng :attr:`COMPRESSION_LEVEL_DEFAULT`.

   .. attribute:: window_log

      Khoảng cách back-reference tối đa mà compressor có thể sử dụng khi nén dữ liệu, được biểu thị dưới dạng lũy thừa của 2, ``1 << window_log`` byte. Tham số này ảnh hưởng đáng kể đến mức sử dụng bộ nhớ khi nén. Giá trị cao hơn yêu cầu nhiều bộ nhớ hơn nhưng cho hiệu quả nén tốt hơn.

      Giá trị bằng không sẽ khiến giá trị được tự động chọn.

   .. attribute:: hash_log

      Kích thước của bảng thăm dò ban đầu, dưới dạng lũy thừa của 2. Mức sử dụng bộ nhớ tương ứng là ``1 << (hash_log+2)`` byte. Các bảng lớn hơn cải thiện tỷ lệ nén của các strategy <= :attr:`~Strategy.dfast`, đồng thời cải thiện tốc độ nén của các strategy > :attr:`~Strategy.dfast`.

      Giá trị bằng không sẽ khiến giá trị được tự động chọn.

   .. attribute:: chain_log

      Kích thước của bảng tìm kiếm multi-probe, dưới dạng lũy thừa của 2. Mức sử dụng bộ nhớ tương ứng là ``1 << (chain_log+2)`` byte. Các bảng lớn hơn cho khả năng nén tốt hơn nhưng chậm hơn. Tham số này không có tác dụng đối với
      :attr:`~Strategy.fast` strategy. Tham số này vẫn hữu ích khi sử dụng
      chiến lược :attr:`~Strategy.dfast`, trong trường hợp đó nó xác định một bảng probe phụ.

      Giá trị bằng không sẽ khiến giá trị được tự động chọn.

   .. attribute:: search_log

      Số lần thử tìm kiếm, dưới dạng lũy thừa của hai. Nhiều lần thử hơn cho khả năng nén tốt hơn nhưng chậm hơn. Tham số này vô dụng đối với
      các chiến lược :attr:`~Strategy.fast` và :attr:`~Strategy.dfast`.

      Giá trị bằng không sẽ khiến giá trị được tự động chọn.

   .. attribute:: min_match

      Kích thước tối thiểu của các đoạn khớp được tìm kiếm. Giá trị lớn hơn làm tăng tốc độ nén và giải nén, nhưng làm giảm tỷ lệ nén. Lưu ý rằng Zstandard vẫn có thể tìm thấy các đoạn khớp nhỏ hơn; nó chỉ điều chỉnh thuật toán tìm kiếm để tìm các đoạn có kích thước này trở lên. Đối với mọi chiến lược < :attr:`~Strategy.btopt`, giá trị tối thiểu thực tế là ``4``; đối với mọi chiến lược > :attr:`~Strategy.fast`, giá trị tối đa thực tế là ``6``.

      Giá trị bằng không sẽ khiến giá trị được tự động chọn.

   .. attribute:: target_length

      Tác động của trường này phụ thuộc vào :class:`Strategy` đã chọn.

      Đối với các strategy :attr:`~Strategy.btopt`, :attr:`~Strategy.btultra` và
      :attr:`~Strategy.btultra2`, giá trị là độ dài của một kết quả khớp được xem là "đủ tốt" để dừng tìm kiếm. Giá trị lớn hơn giúp cải thiện tỷ lệ nén, nhưng quá trình nén sẽ chậm hơn.

      Đối với strategy :attr:`~Strategy.fast`, đây là khoảng cách giữa các lần lấy mẫu kết quả khớp. Giá trị lớn hơn giúp quá trình nén nhanh hơn, nhưng tỷ lệ nén sẽ kém hơn.

      Giá trị bằng không sẽ khiến giá trị được tự động chọn.

   .. attribute:: strategy

      Giá trị của strategy được chọn càng cao thì kỹ thuật nén mà zstd sử dụng càng phức tạp, resulting in higher compression ratios but slower compression.

      .. seealso:: :class:`Strategy`

   .. attribute:: enable_long_distance_matching

      Tính năng tìm kết quả khớp ở khoảng cách xa có thể được sử dụng để cải thiện khả năng nén đối với dữ liệu đầu vào lớn bằng cách tìm các kết quả khớp lớn ở khoảng cách xa hơn. Tính năng này làm tăng mức sử dụng bộ nhớ và kích thước cửa sổ.

      ``True`` hoặc ``1`` bật tính năng ghép cặp khoảng cách xa, còn ``False`` hoặc ``0`` tắt tính năng này.

      Việc bật tham số này làm tăng giá trị mặc định
      :attr:`~CompressionParameter.window_log` lên 128 MiB, trừ khi được đặt rõ ràng thành một giá trị khác. Thiết lập này được bật theo mặc định nếu
      :attr:`!window_log` >= 128 MiB và chiến lược nén >= :attr:`~Strategy.btopt` (mức nén 16+).

   .. attribute:: ldm_hash_log

      Kích thước của bảng dùng cho việc ghép cặp khoảng cách xa, tính theo lũy thừa của hai. Giá trị lớn hơn làm tăng mức sử dụng bộ nhớ và tỷ lệ nén, nhưng làm giảm tốc độ nén.

      Giá trị bằng không sẽ khiến giá trị được tự động chọn.

   .. attribute:: ldm_min_match

      Kích thước khớp tối thiểu cho bộ ghép cặp khoảng cách xa. Các giá trị lớn hơn hoặc quá nhỏ thường có thể làm giảm tỷ lệ nén.

      Giá trị bằng không sẽ khiến giá trị được tự động chọn.

   .. attribute:: ldm_bucket_size_log

      Ghi lại kích thước của từng bucket trong bảng băm của long distance matcher để xử lý xung đột. Giá trị lớn hơn giúp xử lý xung đột tốt hơn nhưng làm giảm tốc độ nén.

      Giá trị bằng không sẽ khiến giá trị được tự động chọn.

   .. attribute:: ldm_hash_rate_log

      Tần suất chèn/tra cứu các mục trong bảng băm của long distance matcher. Giá trị lớn hơn giúp tăng tốc độ nén. Việc đặt giá trị lệch quá xa so với giá trị mặc định có thể làm giảm tỷ lệ nén.

      Giá trị bằng không sẽ khiến giá trị được tự động chọn.

   .. attribute:: content_size_flag

      Ghi kích thước dữ liệu cần nén vào phần header của frame Zstandard khi kích thước này đã được biết trước khi nén.

      Cờ này chỉ có hiệu lực trong các trường hợp sau:

      * Gọi :func:`compress` để nén một lần
      * Cung cấp toàn bộ dữ liệu cần nén trong frame bằng một lần
        gọi :meth:`ZstdCompressor.compress`, với
        chế độ :attr:`ZstdCompressor.FLUSH_FRAME`.
      * Gọi :meth:`ZstdCompressor.set_pledged_input_size` với chính xác lượng dữ liệu sẽ được cung cấp cho compressor trước mọi lần gọi :meth:`ZstdCompressor.compress` cho frame hiện tại.
        Phải gọi :meth:`!ZstdCompressor.set_pledged_input_size` cho mỗi frame mới.

      Tất cả các lần gọi compression khác có thể không ghi thông tin kích thước vào phần header của frame.

      ``True`` hoặc ``1`` bật cờ kích thước nội dung, còn ``False`` hoặc ``0`` tắt cờ này.

   .. attribute:: checksum_flag

      Một checksum bốn byte sử dụng XXHash64 của nội dung chưa nén được ghi ở cuối mỗi frame. Mã decompression của Zstandard sẽ xác minh checksum. Nếu có sự không khớp, một exception :class:`ZstdError` sẽ được phát sinh.

      ``True`` hoặc ``1`` bật tính năng tạo checksum, còn ``False`` hoặc ``0`` tắt tính năng này.

   .. attribute:: dict_id_flag

      Khi nén bằng :class:`ZstdDict`, ID của dictionary được ghi vào frame header.

      ``True`` hoặc ``1`` bật tính năng lưu ID của dictionary, còn ``False`` hoặc ``0`` tắt tính năng này.

   .. attribute:: nb_workers

      Chọn số lượng thread sẽ được tạo để thực hiện nén song song. Khi
      :attr:`!nb_workers` > 0, bật tính năng nén đa thread; giá trị ``1`` có nghĩa là "chế độ đa thread một thread". Nhiều worker hơn sẽ cải thiện tốc độ, nhưng cũng làm tăng mức sử dụng bộ nhớ và giảm nhẹ tỉ lệ nén.

      Giá trị bằng 0 sẽ vô hiệu hóa chế độ đa luồng.

   .. attribute:: job_size

      Kích thước của một tác vụ nén, tính bằng byte. Giá trị này chỉ được áp dụng khi
      :attr:`~CompressionParameter.nb_workers` >= 1. Mỗi tác vụ nén được hoàn tất song song, vì vậy giá trị này có thể gián tiếp ảnh hưởng đến số lượng thread đang hoạt động.

      Giá trị bằng không sẽ khiến giá trị được tự động chọn.

   .. attribute:: overlap_log

      Thiết lập lượng dữ liệu được tải lại từ các tác vụ trước đó (thread) để các tác vụ mới sử dụng trong cửa sổ look-behind khi nén. Giá trị này chỉ được sử dụng khi :attr:`~CompressionParameter.nb_workers` >= 1. Các giá trị hợp lệ nằm trong khoảng từ 0 đến 9.

         * 0 nghĩa là tự động thiết lập lượng dữ liệu chồng lấn
         * 1 nghĩa là không chồng lấn
         * 9 nghĩa là sử dụng kích thước cửa sổ đầy đủ từ job trước đó

      Mỗi lần tăng sẽ giảm một nửa hoặc tăng gấp đôi kích thước phần chồng lấp. "8" nghĩa là phần chồng lấp ``window_size/2``, "7" nghĩa là phần chồng lấp ``window_size/4``, v.v.

.. class:: DecompressionParameter()

   Một :class:`~enum.IntEnum` chứa các khóa tham số giải nén nâng cao có thể được sử dụng khi giải nén dữ liệu. Các tham số là tùy chọn; mọi tham số bị bỏ qua sẽ được tự động chọn giá trị.

   Có thể sử dụng phương thức :meth:`~.bounds` trên bất kỳ thuộc tính nào để lấy các giá trị hợp lệ cho tham số đó.

   Ví dụ thiết lập :attr:`~.window_log_max` thành kích thước tối đa::

      data = compress(b'Some very long buffer of bytes...')

      _lower, upper = DecompressionParameter.window_log_max.bounds()

      options = {DecompressionParameter.window_log_max: upper}
      decompress(data, options=options)

   .. method:: bounds()

      Trả về tuple gồm các giới hạn kiểu int, ``(lower, upper)``, của một tham số giải nén. Nên gọi phương thức này trên thuộc tính mà bạn muốn lấy các giới hạn.

      Cả giới hạn dưới và giới hạn trên đều được tính.

   .. attribute:: window_log_max

      Logarit cơ số hai của kích thước tối đa của cửa sổ được sử dụng trong quá trình giải nén. Thông tin này có thể hữu ích để giới hạn lượng bộ nhớ được sử dụng khi giải nén dữ liệu. Kích thước cửa sổ tối đa càng lớn thì tốc độ giải nén càng nhanh.

      Giá trị bằng không sẽ khiến giá trị được tự động chọn.


.. class:: Strategy()

   Một :class:`~enum.IntEnum` chứa các chiến lược nén. Các chiến lược có số thứ tự cao hơn tương ứng với việc nén phức tạp hơn và chậm hơn.

   .. note::

      Các giá trị của các thuộc tính của :class:`!Strategy` không nhất thiết ổn định giữa các phiên bản zstd. Chỉ có thể dựa vào thứ tự của các thuộc tính. Các thuộc tính được liệt kê bên dưới theo thứ tự.

   Các chiến lược sau đây khả dụng:

   .. attribute:: fast

   .. attribute:: dfast

   .. attribute:: greedy

   .. attribute:: lazy

   .. attribute:: lazy2

   .. attribute:: btlazy2

   .. attribute:: btopt

   .. attribute:: btultra

   .. attribute:: btultra2


Thông tin khác
--------------

.. function:: get_frame_info(frame_buffer)

   Truy xuất một đối tượng :class:`FrameInfo` chứa siêu dữ liệu về một khung Zstandard. Các khung chứa siêu dữ liệu liên quan đến dữ liệu đã nén mà chúng lưu giữ.


.. class:: FrameInfo

   Siêu dữ liệu liên quan đến một frame Zstandard.

   .. attribute:: decompressed_size

      Kích thước nội dung đã được giải nén của frame.

   .. attribute:: dictionary_id

      Một số nguyên biểu thị ID từ điển Zstandard cần thiết để giải nén frame. ``0`` có nghĩa là ID từ điển không được ghi trong header của frame. Điều này có thể có nghĩa là không cần từ điển Zstandard hoặc ID của từ điển bắt buộc không được ghi lại.


.. attribute:: COMPRESSION_LEVEL_DEFAULT

   Mức nén mặc định cho Zstandard: ``3``.


.. attribute:: zstd_version_info

   Số phiên bản của thư viện zstd runtime dưới dạng một tuple số nguyên (major, minor, release).


Ví dụ
-----

Đọc một tệp đã nén:

.. code-block:: python

   from compression import zstd

   with zstd.open("file.zst") as f:
       file_content = f.read()

Tạo tệp nén:

.. code-block:: python

   from compression import zstd

   data = b"Insert Data Here"
   with zstd.open("file.zst", "w") as f:
       f.write(data)

Nén dữ liệu trong bộ nhớ:

.. code-block:: python

   from compression import zstd

   data_in = b"Insert Data Here"
   data_out = zstd.compress(data_in)

Nén tăng dần:

.. code-block:: python

   from compression import zstd

   comp = zstd.ZstdCompressor()
   out1 = comp.compress(b"Some data\n")
   out2 = comp.compress(b"Another piece of data\n")
   out3 = comp.compress(b"Even more data\n")
   out4 = comp.flush()
   # Nối tất cả các kết quả từng phần:
   result = b"".join([out1, out2, out3, out4])

Ghi dữ liệu nén vào tệp đã được mở:

.. code-block:: python

   from compression import zstd

   with open("myfile", "wb") as f:
       f.write(b"This data will not be compressed\n")
       with zstd.open(f, "w") as zstf:
           zstf.write(b"This *will* be compressed\n")
       f.write(b"Not compressed\n")

Tạo tệp nén bằng các tham số nén:

.. code-block:: python

   from compression import zstd

   options = {
      zstd.CompressionParameter.checksum_flag: 1
   }
   with zstd.open("file.zst", "w", options=options) as f:
       f.write(b"Mind if I squeeze in?")
