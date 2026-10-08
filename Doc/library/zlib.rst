:mod:`!zlib` --- Nén tương thích với :program:`gzip`
====================================================

.. module:: zlib
   :synopsis: Giao diện cấp thấp cho các routine nén và giải nén tương thích với gzip.

--------------

Đối với các ứng dụng yêu cầu nén dữ liệu, các hàm trong module này cho phép nén và giải nén bằng thư viện `zlib <https://www.zlib.net>`_.

.. include:: ../includes/optional-module.rst

Các hàm của zlib có nhiều tùy chọn và thường cần được sử dụng theo một thứ tự cụ thể. Tài liệu này không cố gắng trình bày tất cả các tổ hợp; hãy tham khảo `sổ tay zlib <https://www.zlib.net/manual.html>`_ để biết thông tin chính thức.

Để đọc và ghi các tệp ``.gz``, hãy xem module :mod:`gzip`.

Các exception và hàm có sẵn trong module này gồm:


.. exception:: error

   Exception được phát sinh khi xảy ra lỗi nén và giải nén.


.. function:: adler32(data, value=1, /)

   Tính checksum Adler-32 của *data*. (Checksum Adler-32 gần đáng tin cậy như CRC32 nhưng có thể được tính nhanh hơn nhiều.) Kết quả là một số nguyên 32-bit không dấu. Nếu *value* được cung cấp, giá trị này sẽ được dùng làm giá trị bắt đầu của checksum; nếu không, giá trị mặc định là 1 sẽ được sử dụng. Việc truyền *value* cho phép tính checksum liên tục trên phần nối của nhiều đầu vào. Thuật toán này không đủ mạnh về mặt mật mã và không nên được dùng cho xác thực hoặc chữ ký số. Vì thuật toán được thiết kế để dùng làm thuật toán checksum nên không phù hợp để sử dụng như một thuật toán hash nói chung.

   .. versionchanged:: 3.0
      Kết quả luôn là số không dấu.

.. function:: compress(data, /, level=Z_DEFAULT_COMPRESSION, wbits=MAX_WBITS)

   Nén các byte trong *data*, trả về một đối tượng bytes chứa dữ liệu đã nén. *level* là một số nguyên từ ``0`` đến ``9`` hoặc ``-1``, dùng để điều khiển mức độ nén; xem :const:`Z_BEST_SPEED` (``1``), :const:`Z_BEST_COMPRESSION` (``9``),
   :const:`Z_NO_COMPRESSION` (``0``), và giá trị mặc định,
   :const:`Z_DEFAULT_COMPRESSION` (``-1``) để biết thêm thông tin về các giá trị này.

   .. _compress-wbits:

   Đối số *wbits* điều khiển kích thước của bộ đệm lịch sử (hay "kích thước cửa sổ") được sử dụng khi nén dữ liệu, cũng như việc có đưa header và trailer vào đầu ra hay không. Đối số này có thể nhận một số khoảng giá trị, với giá trị mặc định là ``15`` (:const:`MAX_WBITS`):

   * +9 đến +15: Logarit cơ số hai của kích thước cửa sổ, do đó kích thước này nằm trong khoảng từ 512 đến 32768. Giá trị lớn hơn tạo ra mức nén tốt hơn nhưng phải đánh đổi bằng việc sử dụng nhiều bộ nhớ hơn. Đầu ra thu được sẽ bao gồm header và trailer dành riêng cho zlib.

   * −9 đến −15: Sử dụng giá trị tuyệt đối của *wbits* làm logarit kích thước cửa sổ, đồng thời tạo luồng đầu ra thô không có phần đầu hoặc checksum ở cuối.

   * +25 đến +31 = 16 + (9 đến 15): Sử dụng 4 bit thấp của giá trị làm logarit kích thước cửa sổ, đồng thời bao gồm phần đầu :program:`gzip` cơ bản và checksum ở cuối trong đầu ra.

   Tăng ngoại lệ :exc:`error` nếu xảy ra bất kỳ lỗi nào.

   .. versionchanged:: 3.6
      *level* hiện có thể được sử dụng làm tham số từ khóa.

   .. versionchanged:: 3.11
      Tham số *wbits* hiện có sẵn để thiết lập số bit của cửa sổ và kiểu nén.

.. function:: compressobj(level=Z_DEFAULT_COMPRESSION, method=DEFLATED, wbits=MAX_WBITS, memLevel=DEF_MEM_LEVEL, strategy=Z_DEFAULT_STRATEGY[, zdict])

   Trả về một đối tượng nén, được dùng để nén các luồng dữ liệu không thể vừa vào bộ nhớ cùng một lúc.

   *level* là mức nén -- một số nguyên từ ``0`` đến ``9`` hoặc ``-1``. Xem :const:`Z_BEST_SPEED` (``1``), :const:`Z_BEST_COMPRESSION` (``9``),
   :const:`Z_NO_COMPRESSION` (``0``), và giá trị mặc định,
   :const:`Z_DEFAULT_COMPRESSION` (``-1``) để biết thêm thông tin về các giá trị này.

   *method* là thuật toán nén. Hiện tại, giá trị duy nhất được hỗ trợ là
   :const:`DEFLATED`.

   Tham số *wbits* kiểm soát kích thước của bộ đệm lịch sử (hay "kích thước cửa sổ"), cũng như định dạng header và trailer sẽ được sử dụng. Tham số này có cùng ý nghĩa với `described for compress() <#compress-wbits>`__.

   Đối số *memLevel* kiểm soát lượng bộ nhớ được sử dụng cho trạng thái nén nội bộ. Các giá trị hợp lệ nằm trong khoảng từ ``1`` đến ``9``. Giá trị cao hơn sử dụng nhiều bộ nhớ hơn, nhưng nhanh hơn và tạo ra đầu ra nhỏ hơn.

   *strategy* được dùng để tinh chỉnh thuật toán nén. Các giá trị có thể có là
   :const:`Z_DEFAULT_STRATEGY`, :const:`Z_FILTERED`, :const:`Z_HUFFMAN_ONLY`,
   :const:`Z_RLE` và :const:`Z_FIXED`.

   *zdict* là một từ điển nén được định nghĩa sẵn. Đây là một chuỗi byte (chẳng hạn như một đối tượng :class:`bytes`) chứa các chuỗi con được dự đoán là sẽ thường xuyên xuất hiện trong dữ liệu cần nén. Các chuỗi con được dự đoán là phổ biến nhất nên nằm ở cuối từ điển.

   .. versionchanged:: 3.3
      Đã bổ sung tham số *zdict* và hỗ trợ đối số keyword.


.. function:: crc32(data, value=0, /)

   .. index::
      single: Cyclic Redundancy Check
      single: checksum; Cyclic Redundancy Check

   Tính checksum CRC (Cyclic Redundancy Check) của *data*. Kết quả là một số nguyên 32 bit không dấu. Nếu có *value*, giá trị này được dùng làm giá trị khởi đầu của checksum; nếu không, giá trị mặc định 0 sẽ được sử dụng. Việc truyền *value* cho phép tính checksum liên tục trên phần nối của nhiều đầu vào. Thuật toán này không đủ mạnh về mặt mật mã và không nên được sử dụng cho xác thực hoặc chữ ký số. Vì thuật toán được thiết kế để dùng làm thuật toán checksum, nó không phù hợp để sử dụng như một thuật toán hash tổng quát.

   .. versionchanged:: 3.0
      Kết quả luôn là số không dấu.

.. function:: decompress(data, /, wbits=MAX_WBITS, bufsize=DEF_BUF_SIZE)

   Giải nén các byte trong *data*, trả về một đối tượng bytes chứa dữ liệu chưa nén. Tham số *wbits* phụ thuộc vào định dạng của *data* và sẽ được thảo luận thêm bên dưới. Nếu cung cấp *bufsize*, giá trị này được dùng làm kích thước ban đầu của bộ đệm đầu ra. Phát sinh ngoại lệ :exc:`error` nếu xảy ra bất kỳ lỗi nào.

   .. _decompress-wbits:

   Tham số *wbits* kiểm soát kích thước của bộ đệm lịch sử (hay "kích thước cửa sổ") và định dạng header và trailer được mong đợi. Tham số này tương tự tham số của :func:`compressobj`, nhưng chấp nhận nhiều khoảng giá trị hơn:

   * +8 đến +15: Logarit cơ số hai của kích thước cửa sổ. Đầu vào phải bao gồm header và trailer của zlib.

   * 0: Tự động xác định kích thước cửa sổ từ header của zlib. Chỉ được hỗ trợ kể từ zlib 1.2.3.5.

   * −8 đến −15: Sử dụng giá trị tuyệt đối của *wbits* làm logarit kích thước cửa sổ. Dữ liệu đầu vào phải là một raw stream không có header hoặc trailer.

   * +24 đến +31 = 16 + (8 đến 15): Sử dụng 4 bit thấp của giá trị làm logarit kích thước cửa sổ. Dữ liệu đầu vào phải bao gồm header và trailer của gzip.

   * +40 đến +47 = 32 + (8 đến 15): Sử dụng 4 bit thấp của giá trị làm logarit kích thước cửa sổ và tự động chấp nhận định dạng zlib hoặc gzip.

   Khi giải nén một stream, kích thước cửa sổ không được nhỏ hơn kích thước ban đầu được dùng để nén stream; sử dụng giá trị quá nhỏ có thể dẫn đến ngoại lệ :exc:`error` . Giá trị *wbits* mặc định tương ứng với kích thước cửa sổ lớn nhất và yêu cầu phải bao gồm header và trailer của zlib.

   *bufsize* là kích thước ban đầu của bộ đệm dùng để chứa dữ liệu đã giải nén. Nếu cần thêm không gian, kích thước bộ đệm sẽ được tăng lên khi cần, vì vậy bạn không cần phải xác định chính xác giá trị này; việc tinh chỉnh nó chỉ giúp giảm vài lần gọi đến :c:func:`malloc`.

   .. versionchanged:: 3.6
      *wbits* và *bufsize* có thể được sử dụng làm keyword arguments.

.. function:: decompressobj(wbits=MAX_WBITS, zdict=b'')

   Trả về một đối tượng giải nén, được dùng để giải nén các luồng dữ liệu không thể vừa vào bộ nhớ cùng một lúc.

   Tham số *wbits* kiểm soát kích thước bộ đệm lịch sử (hay "kích thước cửa sổ") và định dạng header và trailer được mong đợi. Nó có cùng ý nghĩa như `described for decompress() <#decompress-wbits>`__.

   Tham số *zdict* chỉ định một từ điển nén được xác định trước. Nếu được cung cấp, đây phải là cùng một từ điển đã được bộ nén sử dụng để tạo ra dữ liệu cần giải nén.

   .. note::

      Nếu *zdict* là một đối tượng có thể thay đổi (chẳng hạn như :class:`bytearray`), bạn không được sửa đổi nội dung của nó giữa lần gọi :func:`decompressobj` và lần gọi đầu tiên đến phương thức ``decompress()`` của bộ giải nén.

   .. versionchanged:: 3.3
      Đã thêm tham số *zdict*.


Các đối tượng nén hỗ trợ các phương thức sau:


.. method:: Compress.compress(data, /)

   Nén *data*, trả về một đối tượng bytes chứa dữ liệu đã nén cho ít nhất một phần dữ liệu trong *data*. Dữ liệu này nên được nối vào đầu ra do mọi lần gọi trước đó đến phương thức :meth:`compress` tạo ra. Một phần dữ liệu đầu vào có thể được giữ trong các bộ đệm nội bộ để xử lý sau.


.. method:: Compress.flush(mode=Z_FINISH, /)

   Toàn bộ dữ liệu đầu vào đang chờ được xử lý và một đối tượng bytes chứa phần đầu ra đã nén còn lại được trả về. Có thể chọn *mode* từ các hằng số
   :const:`Z_NO_FLUSH`, :const:`Z_PARTIAL_FLUSH`, :const:`Z_SYNC_FLUSH`,
   :const:`Z_FULL_FLUSH`, :const:`Z_BLOCK` hoặc :const:`Z_FINISH`, mặc định là :const:`Z_FINISH`. Ngoại trừ :const:`Z_FINISH`, tất cả các hằng số đều cho phép tiếp tục nén các bytestring dữ liệu khác, trong khi :const:`Z_FINISH` hoàn tất luồng đã nén và ngăn không cho nén thêm dữ liệu. Sau khi gọi :meth:`flush` với *mode* được đặt thành :const:`Z_FINISH`, không thể gọi lại phương thức :meth:`compress`; hành động thực tế duy nhất là xóa đối tượng.


.. method:: Compress.copy()

   Trả về một bản sao của đối tượng nén. Có thể dùng bản sao này để nén hiệu quả một tập dữ liệu có cùng tiền tố ban đầu.


.. versionchanged:: 3.8
   Đã thêm hỗ trợ :func:`copy.copy` và :func:`copy.deepcopy` cho các đối tượng nén.


Các đối tượng giải nén hỗ trợ những phương thức và thuộc tính sau:


.. attribute:: Decompress.unused_data

   Một đối tượng bytes chứa mọi byte nằm sau phần cuối của dữ liệu đã nén. Nghĩa là, giá trị này vẫn là ``b""`` cho đến khi có sẵn byte cuối cùng chứa dữ liệu nén. Nếu toàn bộ bytestring hóa ra đều chứa dữ liệu đã nén thì giá trị này là ``b""``, một đối tượng bytes rỗng.


.. attribute:: Decompress.unconsumed_tail

   Một đối tượng bytes chứa mọi dữ liệu chưa được tiêu thụ bởi lần gọi trước đó
   lệnh gọi :meth:`decompress` vì nó đã vượt quá giới hạn của bộ đệm dữ liệu chưa nén. Dữ liệu này vẫn chưa được bộ máy zlib xử lý, vì vậy bạn phải truyền dữ liệu đó (có thể nối thêm dữ liệu khác vào) trở lại cho một lệnh gọi tiếp theo
   lệnh gọi phương thức :meth:`decompress` để nhận được kết quả chính xác.


.. attribute:: Decompress.eof

   Một giá trị boolean cho biết đã đến cuối luồng dữ liệu nén hay chưa.

   Điều này giúp phân biệt giữa một luồng dữ liệu nén được tạo đúng định dạng và một luồng chưa hoàn chỉnh hoặc bị cắt ngắn.

   .. versionadded:: 3.3


.. method:: Decompress.decompress(data, /, max_length=0)

   Giải nén *data*, trả về một đối tượng bytes chứa dữ liệu chưa nén tương ứng với ít nhất một phần dữ liệu trong *string*. Dữ liệu này phải được nối vào kết quả do bất kỳ lệnh gọi nào trước đó tới
   phương thức :meth:`decompress`. Một phần dữ liệu đầu vào có thể được giữ lại trong các bộ đệm nội bộ để xử lý sau.

   Nếu tham số tùy chọn *max_length* khác không thì giá trị trả về sẽ không dài hơn *max_length*. Điều này có thể có nghĩa là không phải toàn bộ dữ liệu đầu vào đã nén đều được xử lý; dữ liệu chưa được sử dụng sẽ được lưu trong thuộc tính
   :attr:`unconsumed_tail`. Chuỗi byte này phải được truyền vào một lần gọi tiếp theo tới
   :meth:`decompress` nếu muốn tiếp tục giải nén. Nếu *max_length* bằng không thì toàn bộ đầu vào sẽ được giải nén và :attr:`unconsumed_tail` là rỗng.

   .. versionchanged:: 3.6
      *max_length* có thể được sử dụng làm đối số từ khóa.


.. method:: Decompress.flush(length=DEF_BUF_SIZE, /)

   Tất cả dữ liệu đầu vào đang chờ được xử lý và một đối tượng bytes chứa phần đầu ra chưa nén còn lại được trả về. Sau khi gọi :meth:`flush`,
   không thể gọi lại phương thức :meth:`decompress`; hành động thực tế duy nhất là xóa đối tượng.

   Tham số tùy chọn *length* đặt kích thước ban đầu của bộ đệm đầu ra.


.. method:: Decompress.copy()

   Trả về một bản sao của đối tượng giải nén. Có thể sử dụng bản sao này để lưu trạng thái của bộ giải nén ở giữa luồng dữ liệu, nhằm tăng tốc việc tìm kiếm ngẫu nhiên trong luồng tại một thời điểm sau đó.


.. versionchanged:: 3.8
   Đã bổ sung hỗ trợ :func:`copy.copy` và :func:`copy.deepcopy` cho các đối tượng giải nén.


Có thể sử dụng các hằng số sau để cấu hình hoạt động nén và giải nén:

.. data:: DEFLATED

   Phương thức nén deflate.


.. data:: MAX_WBITS

   Kích thước cửa sổ tối đa, được biểu thị dưới dạng lũy thừa của 2. Ví dụ: nếu :const:`!MAX_WBITS` là ``15`` thì kích thước cửa sổ sẽ là ``32 KiB``.


.. data:: DEF_MEM_LEVEL

   Cấp bộ nhớ mặc định cho các đối tượng nén.


.. data:: DEF_BUF_SIZE

   Kích thước bộ đệm mặc định cho các thao tác giải nén.


.. data:: Z_NO_COMPRESSION

   Cấp độ nén ``0``; không nén.

   .. versionadded:: 3.6


.. data:: Z_BEST_SPEED

   Cấp độ nén ``1``; nhanh nhất và cho mức nén thấp nhất.


.. data:: Z_BEST_COMPRESSION

   Cấp độ nén ``9``; chậm nhất và cho mức nén cao nhất.


.. data:: Z_DEFAULT_COMPRESSION

   Cấp độ nén mặc định (``-1``); là sự cân bằng giữa tốc độ và mức nén. Hiện tương đương với cấp độ nén ``6``.


.. data:: Z_DEFAULT_STRATEGY

   Chiến lược nén mặc định dành cho dữ liệu thông thường.


.. data:: Z_FILTERED

   Chiến lược nén dành cho dữ liệu do một bộ lọc (hoặc bộ dự đoán) tạo ra.


.. data:: Z_HUFFMAN_ONLY

   Chiến lược nén chỉ sử dụng mã hóa Huffman.


.. data:: Z_RLE

   Chiến lược nén giới hạn khoảng cách khớp ở mức một (mã hóa độ dài chạy).

   Hằng số này chỉ khả dụng nếu Python được biên dịch với zlib 1.2.0.1 hoặc mới hơn.

   .. versionadded:: 3.6


.. data:: Z_FIXED

   Chiến lược nén ngăn việc sử dụng các mã Huffman động.

   Hằng số này chỉ khả dụng nếu Python được biên dịch với zlib 1.2.2.2 hoặc mới hơn.

   .. versionadded:: 3.6


.. data:: Z_NO_FLUSH

   Chế độ flush ``0``. Không có hành vi flush đặc biệt.

   .. versionadded:: 3.6


.. data:: Z_PARTIAL_FLUSH

   Chế độ flush ``1``. Flush nhiều dữ liệu đầu ra nhất có thể.


.. data:: Z_SYNC_FLUSH

   Chế độ flush ``2``. Toàn bộ dữ liệu đầu ra được flush và được căn chỉnh theo ranh giới byte.


.. data:: Z_FULL_FLUSH

   Chế độ flush ``3``. Toàn bộ dữ liệu đầu ra được flush và trạng thái nén được đặt lại.


.. data:: Z_FINISH

   Chế độ flush ``4``. Tất cả dữ liệu đầu vào đang chờ được xử lý và không có thêm dữ liệu đầu vào nào được mong đợi.


.. data:: Z_BLOCK

   Chế độ flush ``5``. Một khối deflate được hoàn tất và phát ra.

   Hằng số này chỉ khả dụng nếu Python được biên dịch với zlib 1.2.2.2 hoặc mới hơn.

   .. versionadded:: 3.6


.. data:: Z_TREES

   Chế độ flush ``6`` dành cho các thao tác inflate. Hướng dẫn inflate trả về khi đạt đến ranh giới khối deflate tiếp theo.

   Hằng số này chỉ khả dụng nếu Python được biên dịch với zlib 1.2.3.4 hoặc mới hơn.

   .. versionadded:: 3.6


Thông tin về phiên bản của thư viện zlib đang được sử dụng có sẵn thông qua các hằng số sau:


.. data:: ZLIB_VERSION

   Chuỗi phiên bản của thư viện zlib được sử dụng để xây dựng module. Chuỗi này có thể khác với thư viện zlib thực sự được sử dụng trong runtime, có sẵn dưới dạng :const:`ZLIB_RUNTIME_VERSION`.


.. data:: ZLIB_RUNTIME_VERSION

   Chuỗi phiên bản của thư viện zlib thực sự được interpreter tải.

   .. versionadded:: 3.3


.. data:: ZLIBNG_VERSION

   Chuỗi phiên bản của thư viện zlib-ng được sử dụng để xây dựng mô-đun nếu zlib-ng được sử dụng. Khi có mặt, :data:`ZLIB_VERSION` và
   các hằng số :data:`ZLIB_RUNTIME_VERSION` phản ánh phiên bản của API zlib do zlib-ng cung cấp.

   Nếu zlib-ng không được sử dụng để xây dựng mô-đun, hằng số này sẽ không tồn tại.

   .. versionadded:: 3.14


.. seealso::

   Mô-đun :mod:`gzip`
      Đọc và ghi các tệp định dạng :program:`gzip`\ -.

   https://www.zlib.net
      Trang chủ của thư viện zlib.

   https://www.zlib.net/manual.html
      Tài liệu hướng dẫn zlib giải thích ngữ nghĩa và cách sử dụng nhiều hàm của thư viện.

   Trong trường hợp quá trình nén và giải nén bằng gzip là nút thắt cổ chai, package `python-isal`_ sẽ tăng tốc quá trình nén và giải nén với API hầu như tương thích.

   .. _python-isal: https://github.com/pycompression/python-isal

.. _`zlib library`: https://www.zlib.net
.. _`zlib manual`: https://www.zlib.net/manual.html
