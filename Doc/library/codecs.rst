:mod:`!codecs` --- Đăng ký codec và các lớp cơ sở
=================================================

.. module:: codecs
   :synopsis: Mã hóa và giải mã dữ liệu cũng như các stream.

.. moduleauthor:: Marc-André Lemburg <mal@lemburg.com>
.. sectionauthor:: Marc-André Lemburg <mal@lemburg.com>
.. sectionauthor:: Martin v. Löwis <martin@v.loewis.de>

**Mã nguồn:** :source:`Lib/codecs.py`

.. index::
   single: Unicode
   single: Codecs
   pair: Codecs; encode
   pair: Codecs; decode
   single: streams
   pair: stackable; streams

--------------

Mô-đun này định nghĩa các lớp cơ sở cho các codec Python tiêu chuẩn (encoder và decoder), đồng thời cung cấp quyền truy cập vào registry codec nội bộ của Python, nơi quản lý quá trình tra cứu codec và xử lý lỗi. Hầu hết codec tiêu chuẩn là :term:`mã hóa văn bản <text encoding>`, dùng để mã hóa văn bản thành bytes (và giải mã bytes thành văn bản), nhưng cũng có các codec mã hóa văn bản thành văn bản và bytes thành bytes. Codec tùy chỉnh có thể mã hóa và giải mã giữa các kiểu tùy ý, nhưng một số tính năng của mô-đun bị giới hạn và chỉ được sử dụng cụ thể với
:term:`mã hóa văn bản <text encoding>` hoặc với các codec mã hóa thành
:class:`bytes`.

Mô-đun định nghĩa các hàm sau để mã hóa và giải mã bằng bất kỳ codec nào:

.. function:: encode(obj, encoding='utf-8', errors='strict')

   Mã hóa *obj* bằng codec được đăng ký cho *encoding*.

   *Errors* có thể được cung cấp để thiết lập cơ chế xử lý lỗi mong muốn. Trình xử lý lỗi mặc định là ``'strict'``, nghĩa là các lỗi mã hóa sẽ phát sinh
   :exc:`ValueError` (hoặc một lớp con cụ thể hơn của codec, chẳng hạn như
   :exc:`UnicodeEncodeError`). Tham khảo :ref:`codec-base-classes` để biết thêm thông tin về việc xử lý lỗi của codec.

.. function:: decode(obj, encoding='utf-8', errors='strict')

   Giải mã *obj* bằng codec được đăng ký cho *encoding*.

   *Errors* có thể được cung cấp để thiết lập cơ chế xử lý lỗi mong muốn. Trình xử lý lỗi mặc định là ``'strict'``, nghĩa là các lỗi giải mã sẽ phát sinh
   :exc:`ValueError` (hoặc một lớp con cụ thể hơn của codec, chẳng hạn như
   :exc:`UnicodeDecodeError`). Tham khảo :ref:`codec-base-classes` để biết thêm thông tin về việc xử lý lỗi của codec.

.. function:: charmap_build(string)

   Trả về một ánh xạ phù hợp để mã hóa bằng một encoding một byte tùy chỉnh. Với một :class:`str` *chuỗi* có tối đa 256 ký tự, biểu diễn một bảng giải mã, hàm này trả về một đối tượng ánh xạ nội bộ gọn ``EncodingMap`` hoặc một ánh xạ :class:`dictionary <dict>` ánh xạ các ordinal của ký tự đến các giá trị byte. Phát sinh :exc:`TypeError` nếu đầu vào không hợp lệ.

Bạn cũng có thể tra cứu trực tiếp thông tin đầy đủ cho từng codec:

.. function:: lookup(encoding, /)

   Tra cứu thông tin codec trong registry codec của Python và trả về một
   :class:`CodecInfo` đối tượng như được định nghĩa dưới đây.

   Trước tiên, các encoding được tra cứu trong bộ nhớ đệm của registry. Nếu không tìm thấy, danh sách các hàm tìm kiếm đã đăng ký sẽ được quét. Nếu không tìm thấy đối tượng :class:`CodecInfo` nào, một :exc:`LookupError` sẽ được phát sinh. Nếu tìm thấy, đối tượng :class:`CodecInfo` sẽ được lưu vào bộ nhớ đệm và trả về cho bên gọi.

.. class:: CodecInfo(encode, decode, streamreader=None, streamwriter=None, incrementalencoder=None, incrementaldecoder=None, name=None)

   Thông tin chi tiết về codec khi tra cứu registry codec. Các đối số của hàm khởi tạo được lưu trong các thuộc tính có cùng tên:


   .. attribute:: name

      Tên của encoding.


   .. attribute:: encode
                  decode

      Các hàm encoding và decoding không lưu trạng thái. Đây phải là các hàm hoặc phương thức có cùng interface với các phương thức :meth:`~Codec.encode` và :meth:`~Codec.decode` của các instance Codec (xem :ref:`Giao diện Codec <codec-objects>`). Các hàm hoặc phương thức này được kỳ vọng hoạt động ở chế độ không lưu trạng thái.


   .. attribute:: incrementalencoder
                  incrementaldecoder

      Các lớp encoder và decoder tăng dần hoặc các hàm factory. Chúng phải cung cấp interface được định nghĩa bởi các lớp cơ sở
      :class:`IncrementalEncoder` và :class:`IncrementalDecoder`, tương ứng. Các codec tăng dần có thể duy trì trạng thái.


   .. attribute:: streamwriter
                  streamreader

      Các lớp stream writer và reader hoặc các hàm factory. Chúng phải cung cấp interface được định nghĩa bởi các lớp cơ sở
      :class:`StreamWriter` và :class:`StreamReader`, tương ứng. Stream codec có thể duy trì trạng thái.

Để đơn giản hóa việc truy cập vào các thành phần codec khác nhau, module cung cấp các hàm bổ sung sau đây, sử dụng :func:`lookup` để tra cứu codec:

.. function:: getencoder(encoding)

   Tra cứu codec cho encoding đã cho và trả về hàm encoder của codec đó.

   Phát sinh :exc:`LookupError` nếu không tìm thấy encoding.


.. function:: getdecoder(encoding)

   Tra cứu codec cho encoding đã cho và trả về hàm decoder của codec đó.

   Phát sinh :exc:`LookupError` nếu không tìm thấy encoding.


.. function:: getincrementalencoder(encoding)

   Tra cứu codec cho encoding đã cho và trả về class encoder tăng dần hoặc hàm factory của codec đó.

   Phát sinh :exc:`LookupError` trong trường hợp không tìm thấy encoding hoặc codec không hỗ trợ incremental encoder.


.. function:: getincrementaldecoder(encoding)

   Tra cứu codec cho encoding đã cho và trả về class incremental decoder hoặc hàm factory của codec đó.

   Phát sinh :exc:`LookupError` trong trường hợp không tìm thấy encoding hoặc codec không hỗ trợ incremental decoder.


.. function:: getreader(encoding)

   Tra cứu codec cho encoding đã cho và trả về class :class:`StreamReader` hoặc hàm factory của codec đó.

   Phát sinh :exc:`LookupError` nếu không tìm thấy encoding.


.. function:: getwriter(encoding)

   Tra cứu codec cho encoding đã cho và trả về class :class:`StreamWriter` hoặc hàm factory của codec đó.

   Phát sinh :exc:`LookupError` nếu không tìm thấy encoding.

Các codec tùy chỉnh được cung cấp bằng cách đăng ký một hàm tìm kiếm codec phù hợp:

.. function:: register(search_function, /)

   Đăng ký một hàm tìm kiếm codec. Các hàm tìm kiếm được yêu cầu nhận một đối số là tên encoding được viết bằng chữ thường, trong đó dấu gạch nối và dấu cách được chuyển thành dấu gạch dưới, và trả về một đối tượng :class:`CodecInfo`. Nếu một hàm tìm kiếm không thể tìm thấy encoding đã cho, hàm đó nên trả về ``None``.

   .. versionchanged:: 3.9
      Dấu gạch nối và dấu cách được chuyển thành dấu gạch dưới.


.. function:: unregister(search_function, /)

   Hủy đăng ký một hàm tìm kiếm codec và xóa bộ nhớ đệm của registry. Nếu hàm tìm kiếm chưa được đăng ký thì không làm gì cả.

   .. versionadded:: 3.10


Mặc dù :func:`open` tích hợp sẵn và module :mod:`io` đi kèm là cách tiếp cận được khuyến nghị để làm việc với các tệp văn bản được mã hóa, module này cung cấp thêm các hàm tiện ích và lớp cho phép sử dụng nhiều codec hơn khi làm việc với các tệp nhị phân:

.. function:: open(filename, mode='r', encoding=None, errors='strict', buffering=-1)

   Mở một tệp được mã hóa bằng *mode* đã cho và trả về một thể hiện của
   :class:`StreamReaderWriter`, cung cấp encoding/decoding trong suốt. Chế độ tệp mặc định là ``'r'``, nghĩa là mở tệp ở chế độ đọc.

   .. note::

      Nếu *encoding* không phải là ``None``, thì các tệp được mã hóa bên dưới luôn được mở ở chế độ nhị phân. Không tự động chuyển đổi ``'\n'`` khi đọc và ghi. Đối số *mode* có thể là bất kỳ chế độ nhị phân nào được hàm tích hợp sẵn chấp nhận
      hàm :func:`open`; ``'b'`` được tự động thêm vào.

   *encoding* chỉ định encoding sẽ được sử dụng cho tệp. Mọi encoding có thể mã hóa thành byte và giải mã từ byte đều được cho phép, còn các kiểu dữ liệu được các phương thức của tệp hỗ trợ phụ thuộc vào codec được sử dụng.

   Có thể cung cấp *errors* để xác định cách xử lý lỗi. Giá trị mặc định là ``'strict'``, khiến :exc:`ValueError` được phát sinh khi xảy ra lỗi encoding.

   *buffering* có cùng ý nghĩa như trong hàm :func:`open` tích hợp sẵn. Giá trị mặc định là -1, nghĩa là kích thước bộ đệm mặc định sẽ được sử dụng.

   .. versionchanged:: 3.11
      Chế độ ``'U'`` đã bị loại bỏ.

   .. deprecated:: 3.14

      :func:`codecs.open` đã được thay thế bằng :func:`open`.


.. function:: EncodedFile(file, data_encoding, file_encoding=None, errors='strict')

   Trả về một instance :class:`StreamRecoder`, là phiên bản bọc của *file* cung cấp khả năng chuyển mã trong suốt. Tệp gốc được đóng khi phiên bản bọc được đóng.

   Dữ liệu được ghi vào tệp bọc sẽ được giải mã theo *data_encoding*, sau đó được ghi vào tệp gốc dưới dạng byte bằng *file_encoding*. Các byte được đọc từ tệp gốc sẽ được giải mã theo *file_encoding*, rồi kết quả được mã hóa bằng *data_encoding*.

   Nếu không cung cấp *file_encoding*, giá trị mặc định sẽ là *data_encoding*.

   Có thể cung cấp *errors* để xác định cách xử lý lỗi. Giá trị mặc định là ``'strict'``, khiến :exc:`ValueError` được phát sinh khi xảy ra lỗi mã hóa.


.. function:: iterencode(iterator, encoding, errors='strict', **kwargs)

   Sử dụng incremental encoder để mã hóa lặp dữ liệu đầu vào do *iterator* cung cấp. *iterator* phải sinh ra các đối tượng :class:`str`. Hàm này là một :term:`generator`. Đối số *errors* (cũng như mọi đối số từ khóa khác) được truyền cho incremental encoder.

   Hàm này yêu cầu codec chấp nhận các đối tượng văn bản :class:`str` để mã hóa. Do đó, hàm không hỗ trợ các encoder chuyển đổi từ byte sang byte, chẳng hạn như ``base64_codec``.


.. function:: iterdecode(iterator, encoding, errors='strict', **kwargs)

   Sử dụng incremental decoder để giải mã lặp dữ liệu đầu vào do *iterator* cung cấp. *iterator* phải sinh ra các đối tượng :class:`bytes`. Hàm này là một :term:`generator`. Đối số *errors* (cũng như mọi đối số từ khóa khác) được truyền cho incremental decoder.

   Hàm này yêu cầu codec chấp nhận các đối tượng :class:`bytes` để giải mã. Do đó, hàm không hỗ trợ các encoder chuyển văn bản thành văn bản như ``rot_13``, mặc dù ``rot_13`` có thể được sử dụng tương đương với
   :func:`iterencode`.


.. function:: readbuffer_encode(buffer, errors=None, /)

   Trả về một :class:`tuple` chứa các byte thô của *buffer*, một
   :ref:`đối tượng tương thích với buffer <bufferobjects>` hoặc :class:`str` (được mã hóa thành UTF-8 trước khi xử lý), cùng với độ dài của chúng tính theo byte.

   Đối số *errors* bị bỏ qua.

   .. code-block:: pycon

      >>> codecs.readbuffer_encode(b"Zito")
      (b'Zito', 4)


Mô-đun này cũng cung cấp các hằng số sau đây, hữu ích khi đọc và ghi vào các tệp phụ thuộc vào nền tảng:


.. data:: BOM
          BOM_BE BOM_LE BOM_UTF8 BOM_UTF16 BOM_UTF16_BE BOM_UTF16_LE BOM_UTF32 BOM_UTF32_BE BOM_UTF32_LE

   Các hằng số này xác định nhiều chuỗi byte khác nhau, là các dấu thứ tự byte Unicode (BOM) cho một số encoding. Chúng được sử dụng trong các luồng dữ liệu UTF-16 và UTF-32 để cho biết thứ tự byte được sử dụng, và trong UTF-8 dưới dạng chữ ký Unicode. :const:`BOM_UTF16` là một trong hai
   :const:`BOM_UTF16_BE` hoặc :const:`BOM_UTF16_LE` tùy thuộc vào thứ tự byte gốc của nền tảng, :const:`BOM` là bí danh của :const:`BOM_UTF16`,
   :const:`BOM_LE` cho :const:`BOM_UTF16_LE` và :const:`BOM_BE` cho
   :const:`BOM_UTF16_BE`. Các giá trị còn lại đại diện cho BOM trong các encoding UTF-8 và UTF-32.


.. _codec-base-classes:

Các lớp cơ sở của Codec
-----------------------

Module :mod:`!codecs` định nghĩa một tập hợp các lớp cơ sở, trong đó xác định các interface để làm việc với các đối tượng codec, đồng thời có thể dùng làm nền tảng để triển khai codec tùy chỉnh.

Mỗi codec phải định nghĩa bốn interface để có thể được sử dụng như một codec trong Python: encoder không trạng thái, decoder không trạng thái, stream reader và stream writer. Stream reader và stream writer thường tái sử dụng encoder/decoder không trạng thái để triển khai các giao thức tệp. Tác giả codec cũng cần xác định cách codec xử lý các lỗi encoding và decoding.


.. _surrogateescape:
.. _error-handlers:

Trình xử lý lỗi
^^^^^^^^^^^^^^^

Để đơn giản hóa và chuẩn hóa việc xử lý lỗi, các codec có thể triển khai những cơ chế xử lý lỗi khác nhau bằng cách chấp nhận đối số chuỗi *errors*:

      >>> 'German ß, ♬'.encode(encoding='ascii', errors='backslashreplace')
      b'German \\xdf, \\u266c'
      >>> 'German ß, ♬'.encode(encoding='ascii', errors='xmlcharrefreplace')
      b'German &#223;, &#9836;'

.. index::
   pair: strict; error handler's name
   pair: ignore; error handler's name
   pair: replace; error handler's name
   pair: backslashreplace; error handler's name
   pair: surrogateescape; error handler's name
   single: ? (question mark); replacement character
   single: \ (backslash); escape sequence
   single: \x; escape sequence
   single: \u; escape sequence
   single: \U; escape sequence

Có thể sử dụng các trình xử lý lỗi sau đây với mọi Python
:ref:`standard-encodings` codec:

.. tabularcolumns:: |l|L|

+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Giá trị                | Ý nghĩa                                                                                                                                                                                                                                                           |
+========================+===================================================================================================================================================================================================================================================================+
| ``'strict'``           | Ném :exc:`UnicodeError` (hoặc một lớp con); đây là giá trị mặc định. Được triển khai trong                                                                                                                                                                        |
|                        | :func:`strict_errors`.                                                                                                                                                                                                                                            |
+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``'ignore'``           | Bỏ qua dữ liệu không đúng định dạng và tiếp tục mà không có thêm thông báo nào. Được triển khai trong                                                                                                                                                             |
|                        | :func:`ignore_errors`.                                                                                                                                                                                                                                            |
+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``'replace'``          | Thay thế bằng một marker thay thế. Khi mã hóa, sử dụng ``?`` (ký tự ASCII). Khi giải mã, sử dụng ``�`` (U+FFFD, ký tự REPLACEMENT CHARACTER chính thức). Được triển khai trong                                                                                    |
|                        | :func:`replace_errors`.                                                                                                                                                                                                                                           |
+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``'backslashreplace'`` | Thay thế bằng các chuỗi escape có dấu gạch chéo ngược. Khi mã hóa, sử dụng dạng thập lục phân của mã điểm Unicode với các định dạng :samp:`\\x{hh}`                                                                                                               |
|                        | :samp:`\\u{xxxx}` :samp:`\\U{xxxxxxxx}`. Khi giải mã, sử dụng dạng thập lục phân của giá trị byte với định dạng :samp:`\\x{hh}`. Được triển khai trong                                                                                                            |
|                        | :func:`backslashreplace_errors`.                                                                                                                                                                                                                                  |
+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``'surrogateescape'``  | Khi giải mã, thay thế byte bằng mã surrogate riêng lẻ trong khoảng từ ``U+DC80`` đến ``U+DCFF``. Mã này sau đó sẽ được chuyển đổi lại thành cùng byte đó khi sử dụng error handler ``'surrogateescape'`` trong lúc mã hóa dữ liệu. (Xem :pep:`383` để biết thêm.) |
+------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

.. index::
   pair: xmlcharrefreplace; error handler's name
   pair: namereplace; error handler's name
   single: \N; escape sequence

Các error handler sau chỉ áp dụng cho việc mã hóa (trong
:term:`text encodings <text encoding>`):

+-------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Giá trị                 | Ý nghĩa                                                                                                                                                                             |
+=========================+=====================================================================================================================================================================================+
| ``'xmlcharrefreplace'`` | Thay thế bằng tham chiếu ký tự số XML/HTML, là dạng thập phân của điểm mã Unicode với định dạng :samp:`&#{num};`. Được triển khai trong                                             |
|                         | :func:`xmlcharrefreplace_errors`.                                                                                                                                                   |
+-------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``'namereplace'``       | Thay thế bằng các chuỗi escape ``\N{...}``, phần xuất hiện trong dấu ngoặc nhọn là thuộc tính Name từ Unicode Character Database. Được triển khai trong :func:`namereplace_errors`. |
+-------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

.. index::
   pair: surrogatepass; error handler's name

Ngoài ra, trình xử lý lỗi sau đây dành riêng cho các codec tương ứng:

+---------------------+-------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Giá trị             | Codec                                                             | Ý nghĩa                                                                                                                                                                                |
+=====================+===================================================================+========================================================================================================================================================================================+
| ``'surrogatepass'`` | utf-8, utf-16, utf-32, utf-16-be, utf-16-le, utf-32-be, utf-32-le | Cho phép mã hóa và giải mã surrogate code point (``U+D800`` - ``U+DFFF``) như một code point thông thường. Nếu không, các codec này sẽ coi sự hiện diện của surrogate code point trong |
|                     |                                                                   | :class:`str` là một lỗi.                                                                                                                                                               |
+---------------------+-------------------------------------------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

.. versionadded:: 3.1
   Các error handler ``'surrogateescape'`` và ``'surrogatepass'``.

.. versionchanged:: 3.4
   Error handler ``'surrogatepass'`` hiện hoạt động với các codec utf-16\* và utf-32\* khi giải mã.

.. versionadded:: 3.5
   Error handler ``'namereplace'``.

.. versionchanged:: 3.5
   Error handler ``'backslashreplace'`` hiện hoạt động với việc giải mã và chuyển đổi.

Có thể mở rộng tập hợp các giá trị được phép bằng cách đăng ký một trình xử lý lỗi có tên mới:

.. function:: register_error(name, error_handler, /)

   Đăng ký hàm xử lý lỗi *error_handler* dưới tên *name*. Đối số *error_handler* sẽ được gọi trong quá trình mã hóa và giải mã khi xảy ra lỗi, nếu *name* được chỉ định làm tham số errors.

   Đối với quá trình mã hóa, *error_handler* sẽ được gọi với một thực thể :exc:`UnicodeEncodeError`, chứa thông tin về vị trí xảy ra lỗi. Trình xử lý lỗi phải либо raise ngoại lệ này hoặc một ngoại lệ khác, hoặc trả về một tuple chứa phần thay thế cho phần đầu vào không thể mã hóa và vị trí mà tại đó quá trình mã hóa sẽ tiếp tục. Phần thay thế có thể là :class:`str` hoặc
   :class:`bytes`. Nếu phần thay thế là bytes, encoder sẽ פשוט sao chép chúng vào bộ đệm đầu ra. Nếu phần thay thế là một chuỗi, encoder sẽ mã hóa phần thay thế đó. Quá trình mã hóa tiếp tục trên đầu vào ban đầu tại vị trí được chỉ định. Các giá trị vị trí âm sẽ được coi là tương đối so với cuối chuỗi đầu vào. Nếu vị trí kết quả nằm ngoài phạm vi, một :exc:`IndexError` sẽ được raise.

   Giải mã và chuyển đổi hoạt động tương tự, ngoại trừ :exc:`UnicodeDecodeError` hoặc
   :exc:`UnicodeTranslateError` sẽ được truyền cho trình xử lý và phần thay thế từ trình xử lý lỗi sẽ được đưa trực tiếp vào đầu ra.


Có thể tra cứu các trình xử lý lỗi đã đăng ký trước đó (bao gồm cả các trình xử lý lỗi tiêu chuẩn) theo tên:

.. function:: lookup_error(name, /)

   Trả về trình xử lý lỗi đã được đăng ký trước đó với tên *name*.

   Ném một :exc:`LookupError` nếu không tìm thấy trình xử lý.

Các trình xử lý lỗi tiêu chuẩn sau đây cũng được cung cấp dưới dạng các hàm cấp mô-đun:

.. function:: strict_errors(exception)

   Triển khai cơ chế xử lý lỗi ``'strict'``.

   Mỗi lỗi mã hóa hoặc giải mã đều ném một :exc:`UnicodeError`.


.. function:: ignore_errors(exception)

   Triển khai cơ chế xử lý lỗi ``'ignore'``.

   Dữ liệu không đúng định dạng sẽ bị bỏ qua; quá trình mã hóa hoặc giải mã vẫn tiếp tục mà không có thêm thông báo nào.


.. function:: replace_errors(exception)

   Triển khai cơ chế xử lý lỗi ``'replace'``.

   Thay thế ``?`` (ký tự ASCII) cho các lỗi mã hóa hoặc ``�`` (U+FFFD, KÝ TỰ THAY THẾ chính thức) cho các lỗi giải mã.


.. function:: backslashreplace_errors(exception)

   Triển khai cơ chế xử lý lỗi ``'backslashreplace'``.

   Dữ liệu không đúng định dạng được thay thế bằng một escape sequence có dấu gạch chéo ngược. Khi mã hóa, hãy sử dụng dạng thập lục phân của điểm mã Unicode với các định dạng
   :samp:`\\x{hh}` :samp:`\\u{xxxx}` :samp:`\\U{xxxxxxxx}`. Khi giải mã, hãy sử dụng dạng thập lục phân của giá trị byte với định dạng :samp:`\\x{hh}`.

   .. versionchanged:: 3.5
      Hoạt động với việc giải mã và chuyển đổi.


.. function:: xmlcharrefreplace_errors(exception)

   Triển khai cơ chế xử lý lỗi ``'xmlcharrefreplace'`` (để mã hóa trong
   :term:`text encoding` chỉ).

   Ký tự không thể mã hóa được thay thế bằng một tham chiếu ký tự số XML/HTML thích hợp, là dạng thập phân của điểm mã Unicode với định dạng :samp:`&#{num};` .


.. function:: namereplace_errors(exception)

   Triển khai cơ chế xử lý lỗi ``'namereplace'`` (để mã hóa trong
   :term:`text encoding` chỉ).

   Ký tự không thể mã hóa được thay thế bằng một chuỗi escape ``\N{...}``. Tập hợp các ký tự xuất hiện trong dấu ngoặc nhọn là thuộc tính Name từ Unicode Character Database. Ví dụ, chữ cái thường tiếng Đức ``'ß'`` sẽ được chuyển đổi thành chuỗi byte ``\N{LATIN SMALL LETTER SHARP S}`` .

   .. versionadded:: 3.5


.. _codec-objects:

Mã hóa và Giải mã Không trạng thái
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Lớp cơ sở :class:`Codec` định nghĩa các phương thức này, đồng thời cũng định nghĩa các giao diện hàm của encoder và decoder không trạng thái:


.. class:: Codec

   .. method:: encode(input, errors='strict')

      Mã hóa đối tượng *input* và trả về một tuple (đối tượng đầu ra, độ dài đã xử lý). Ví dụ, :term:`text encoding` chuyển đổi một đối tượng chuỗi thành một đối tượng bytes bằng cách sử dụng một encoding bộ ký tự cụ thể (ví dụ: ``cp1252`` hoặc ``iso-8859-1``).

      Đối số *errors* xác định cách xử lý lỗi cần áp dụng. Theo mặc định, đối số này sử dụng cách xử lý ``'strict'``.

      Phương thức này không được lưu trạng thái trong instance :class:`Codec`. Hãy sử dụng
      :class:`StreamWriter` cho các codec cần duy trì trạng thái để việc mã hóa đạt hiệu quả.

      Encoder phải có khả năng xử lý dữ liệu đầu vào có độ dài bằng 0 và trong trường hợp này trả về một đối tượng rỗng thuộc kiểu đối tượng đầu ra.


   .. method:: decode(input, errors='strict')

      Giải mã đối tượng *input* và trả về một tuple (đối tượng đầu ra, độ dài đã xử lý). Ví dụ, đối với :term:`text encoding`, quá trình giải mã chuyển đổi một đối tượng bytes được mã hóa bằng một encoding bộ ký tự cụ thể thành một đối tượng chuỗi.

      Đối với các encoding văn bản và codec bytes-to-bytes, *input* phải là một đối tượng bytes hoặc một đối tượng cung cấp read-only buffer interface -- ví dụ: các đối tượng buffer và các tệp được ánh xạ vào bộ nhớ.

      Đối số *errors* xác định cách xử lý lỗi cần áp dụng. Theo mặc định, đối số này sử dụng cách xử lý ``'strict'``.

      Phương thức này không được lưu trạng thái trong instance :class:`Codec`. Hãy sử dụng
      :class:`StreamReader` đối với các codec phải duy trì trạng thái để việc giải mã đạt hiệu quả.

      Bộ giải mã phải có khả năng xử lý đầu vào có độ dài bằng 0 và trong trường hợp này trả về một đối tượng rỗng thuộc kiểu đối tượng đầu ra.


Mã hóa và giải mã tăng dần
^^^^^^^^^^^^^^^^^^^^^^^^^^

Các lớp :class:`IncrementalEncoder` và :class:`IncrementalDecoder` cung cấp giao diện cơ bản cho việc mã hóa và giải mã tăng dần. Việc mã hóa/giải mã đầu vào không được thực hiện bằng một lần gọi đến hàm encoder/decoder stateless, mà bằng nhiều lần gọi đến
phương thức :meth:`~IncrementalEncoder.encode`/:meth:`~IncrementalDecoder.decode` của encoder/decoder tăng dần. Encoder/decoder tăng dần theo dõi tiến trình mã hóa/giải mã trong các lần gọi phương thức.

Đầu ra được nối lại từ các lần gọi đến
:meth:`~IncrementalEncoder.encode`/:meth:`~IncrementalDecoder.decode` phương thức giống với trường hợp tất cả các đầu vào đơn lẻ được nối lại thành một đầu vào duy nhất, rồi đầu vào này được mã hóa/giải mã bằng encoder/decoder không trạng thái.


.. _incremental-encoder-objects:

Đối tượng IncrementalEncoder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lớp :class:`IncrementalEncoder` được dùng để mã hóa một đầu vào qua nhiều bước. Lớp này định nghĩa các phương thức sau mà mọi incremental encoder phải định nghĩa để tương thích với Python codec registry.


.. class:: IncrementalEncoder(errors='strict')

   Hàm khởi tạo cho một thực thể :class:`IncrementalEncoder`.

   Mọi incremental encoder phải cung cấp giao diện hàm khởi tạo này. Chúng có thể tự do bổ sung các đối số keyword, nhưng Python codec registry chỉ sử dụng những đối số được định nghĩa ở đây.

   :class:`IncrementalEncoder` có thể triển khai các cơ chế xử lý lỗi khác nhau bằng cách cung cấp đối số keyword *errors*. Xem :ref:`error-handlers` để biết các giá trị có thể dùng.

   Đối số *errors* sẽ được gán cho một thuộc tính có cùng tên. Việc gán cho thuộc tính này cho phép chuyển đổi giữa các chiến lược xử lý lỗi khác nhau trong suốt vòng đời của đối tượng :class:`IncrementalEncoder`.


   .. method:: encode(object, final=False)

      Mã hóa *object* (có xét đến trạng thái hiện tại của encoder) và trả về đối tượng đã mã hóa tương ứng. Nếu đây là lần gọi cuối cùng đến
      :meth:`encode` *final* phải là true (mặc định là false).


   .. method:: reset()

      Đặt encoder về trạng thái ban đầu. Kết quả sẽ bị loại bỏ: gọi ``.encode(object, final=True)``, truyền vào một chuỗi byte hoặc chuỗi văn bản rỗng nếu cần, để đặt lại encoder và nhận kết quả.


   .. method:: getstate()

      Trả về trạng thái hiện tại của encoder; trạng thái này phải là một số nguyên. Phần triển khai nên đảm bảo rằng ``0`` là trạng thái phổ biến nhất. (Các trạng thái phức tạp hơn số nguyên có thể được chuyển đổi thành một số nguyên bằng cách marshal/pickle trạng thái rồi mã hóa các byte của chuỗi kết quả thành một số nguyên.)


   .. method:: setstate(state)

      Đặt trạng thái của encoder thành *state*. *state* phải là một trạng thái encoder được trả về bởi :meth:`getstate`.


.. _incremental-decoder-objects:

Đối tượng IncrementalDecoder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lớp :class:`IncrementalDecoder` được dùng để giải mã một đầu vào qua nhiều bước. Lớp này định nghĩa các phương thức sau đây mà mọi incremental decoder đều phải định nghĩa để tương thích với Python codec registry.


.. class:: IncrementalDecoder(errors='strict')

   Hàm khởi tạo cho một instance :class:`IncrementalDecoder`.

   Mọi incremental decoder đều phải cung cấp interface hàm khởi tạo này. Chúng có thể tự do thêm các đối số keyword khác, nhưng Python codec registry chỉ sử dụng những đối số được định nghĩa ở đây.

   :class:`IncrementalDecoder` có thể triển khai các scheme xử lý lỗi khác nhau bằng cách cung cấp đối số keyword *errors*. Xem :ref:`error-handlers` để biết các giá trị có thể dùng.

   Đối số *errors* sẽ được gán cho một attribute có cùng tên. Việc gán cho attribute này cho phép chuyển đổi giữa các chiến lược xử lý lỗi khác nhau trong suốt vòng đời của đối tượng :class:`IncrementalDecoder`.


   .. method:: decode(object, final=False)

      Giải mã *object* (có tính đến trạng thái hiện tại của decoder) và trả về object đã giải mã tương ứng. Nếu đây là lần gọi cuối cùng đến
      :meth:`decode` *final* phải là true (mặc định là false). Nếu *final* là true, decoder phải giải mã hoàn toàn đầu vào và phải flush tất cả buffer. Nếu không thể thực hiện việc này (ví dụ: do các byte sequence chưa hoàn chỉnh ở cuối đầu vào), decoder phải bắt đầu xử lý lỗi giống như trong trường hợp stateless (có thể sẽ phát sinh exception).


   .. method:: reset()

      Đặt lại bộ giải mã về trạng thái ban đầu.


   .. method:: getstate()

      Trả về trạng thái hiện tại của bộ giải mã. Giá trị này phải là một tuple gồm hai phần tử; phần tử đầu tiên phải là bộ đệm chứa dữ liệu đầu vào chưa được giải mã. Phần tử thứ hai phải là một số nguyên và có thể chứa thông tin trạng thái bổ sung. (Việc triển khai phải đảm bảo rằng ``0`` là thông tin trạng thái bổ sung phổ biến nhất.) Nếu thông tin trạng thái bổ sung này là ``0``, phải có thể đặt bộ giải mã về trạng thái không có dữ liệu đầu vào nào trong bộ đệm và ``0`` làm thông tin trạng thái bổ sung, để việc cung cấp dữ liệu đầu vào đã được lưu trong bộ đệm trước đó cho bộ giải mã sẽ đưa nó trở lại trạng thái trước đó mà không tạo ra bất kỳ đầu ra nào. (Thông tin trạng thái bổ sung phức tạp hơn số nguyên có thể được chuyển đổi thành một số nguyên bằng cách marshal/pickle thông tin đó và mã hóa các byte của chuỗi kết quả thành một số nguyên.)


   .. method:: setstate(state)

      Đặt trạng thái của bộ giải mã thành *trạng thái*. *trạng thái* phải là trạng thái bộ giải mã được trả về bởi :meth:`getstate`.


Mã hóa và giải mã luồng
^^^^^^^^^^^^^^^^^^^^^^^


Các lớp :class:`StreamWriter` và :class:`StreamReader` cung cấp các giao diện hoạt động chung, có thể được dùng để triển khai các submodule mã hóa mới một cách rất dễ dàng. Xem :mod:`!encodings.utf_8` để biết ví dụ về cách thực hiện việc này.


.. _stream-writer-objects:

Đối tượng StreamWriter
~~~~~~~~~~~~~~~~~~~~~~

Lớp :class:`StreamWriter` là một lớp con của :class:`Codec` và định nghĩa các phương thức sau mà mọi stream writer phải định nghĩa để tương thích với Python codec registry.


.. class:: StreamWriter(stream, errors='strict')

   Hàm khởi tạo cho một thực thể :class:`StreamWriter`.

   Tất cả stream writer phải cung cấp giao diện hàm khởi tạo này. Chúng có thể tự do thêm các đối số từ khóa khác, nhưng Python codec registry chỉ sử dụng những đối số được định nghĩa ở đây.

   Đối số *stream* phải là một đối tượng tương tự tệp được mở để ghi dữ liệu văn bản hoặc dữ liệu nhị phân, tùy theo codec cụ thể.

   :class:`StreamWriter` có thể triển khai các cơ chế xử lý lỗi khác nhau bằng cách cung cấp đối số từ khóa *errors*. Xem :ref:`error-handlers` để biết các trình xử lý lỗi tiêu chuẩn mà codec của stream bên dưới có thể hỗ trợ.

   Đối số *errors* sẽ được gán cho một thuộc tính cùng tên. Việc gán cho thuộc tính này cho phép chuyển đổi giữa các chiến lược xử lý lỗi khác nhau trong suốt vòng đời của đối tượng :class:`StreamWriter`.

   .. method:: write(object)

      Ghi nội dung của đối tượng vào stream sau khi mã hóa.


   .. method:: writelines(list)

      Ghi iterable các chuỗi đã nối vào stream (có thể bằng cách sử dụng lại phương thức :meth:`write`). Không hỗ trợ iterable vô hạn hoặc rất lớn. Các codec bytes-to-bytes tiêu chuẩn không hỗ trợ phương thức này.


   .. method:: reset()

      Đặt lại các bộ đệm codec được dùng để duy trì trạng thái nội bộ.

      Việc gọi phương thức này phải bảo đảm dữ liệu trên đầu ra được đưa về trạng thái sạch, cho phép nối thêm dữ liệu mới mà không cần quét lại toàn bộ stream để khôi phục trạng thái.


Ngoài các phương thức nêu trên, :class:`StreamWriter` cũng phải kế thừa tất cả các phương thức và thuộc tính khác từ stream nền.


.. _stream-reader-objects:

Đối tượng StreamReader
~~~~~~~~~~~~~~~~~~~~~~

Lớp :class:`StreamReader` là lớp con của :class:`Codec` và định nghĩa các phương thức sau đây mà mọi stream reader phải định nghĩa để tương thích với Python codec registry.


.. class:: StreamReader(stream, errors='strict')

   Hàm khởi tạo cho một thực thể :class:`StreamReader`.

   Mọi stream reader phải cung cấp giao diện hàm khởi tạo này. Chúng được phép bổ sung các đối số từ khóa, nhưng Python codec registry chỉ sử dụng những đối số được định nghĩa ở đây.

   Đối số *stream* phải là một đối tượng giống tệp được mở để đọc dữ liệu văn bản hoặc nhị phân, tùy theo codec cụ thể.

   :class:`StreamReader` có thể triển khai các cơ chế xử lý lỗi khác nhau bằng cách cung cấp đối số từ khóa *errors*. Xem :ref:`error-handlers` để biết các trình xử lý lỗi tiêu chuẩn mà codec stream bên dưới có thể hỗ trợ.

   Đối số *errors* sẽ được gán cho một thuộc tính có cùng tên. Việc gán cho thuộc tính này cho phép chuyển đổi giữa các chiến lược xử lý lỗi khác nhau trong suốt vòng đời của đối tượng :class:`StreamReader`.

   Tập hợp các giá trị được phép cho đối số *errors* có thể được mở rộng bằng
   :func:`register_error`.


   .. method:: read(size=-1, chars=-1, firstline=False)

      Giải mã dữ liệu từ stream và trả về đối tượng kết quả.

      Đối số *chars* cho biết số lượng code point hoặc byte đã giải mã cần trả về. Phương thức :func:`read` sẽ không bao giờ trả về nhiều dữ liệu hơn mức được yêu cầu, nhưng có thể trả về ít hơn nếu không có đủ dữ liệu.

      Đối số *size* cho biết số byte hoặc code point đã mã hóa tối đa ước lượng cần đọc để giải mã. Decoder có thể điều chỉnh thiết lập này cho phù hợp. Giá trị mặc định -1 cho biết cần đọc và giải mã nhiều nhất có thể. Tham số này nhằm tránh phải giải mã các tệp rất lớn trong một bước.

      Cờ *firstline* cho biết rằng chỉ cần trả về dòng đầu tiên nếu xảy ra lỗi giải mã ở các dòng sau.

      Phương thức này nên sử dụng chiến lược đọc tham lam, nghĩa là đọc nhiều dữ liệu nhất có thể trong phạm vi cho phép của định nghĩa encoding và kích thước đã cho; ví dụ: nếu có các phần kết thúc encoding tùy chọn hoặc các dấu trạng thái trên stream, thì cũng nên đọc chúng.


   .. method:: readline(size=None, keepends=True)

      Đọc một dòng từ input stream và trả về dữ liệu đã được giải mã.

      *size*, nếu được cung cấp, sẽ được truyền làm đối số size cho
      phương thức :meth:`read`.

      Nếu *keepends* là false, các ký tự kết thúc dòng sẽ bị loại bỏ khỏi những dòng được trả về.


   .. method:: readlines(sizehint=None, keepends=True)

      Đọc tất cả các dòng hiện có trên input stream và trả về chúng dưới dạng danh sách các dòng.

      Các ký tự kết thúc dòng được triển khai bằng phương thức :meth:`decode` của codec và được đưa vào các mục danh sách nếu *keepends* là true.

      *sizehint*, nếu được cung cấp, sẽ được truyền dưới dạng đối số *size* cho stream
      phương thức :meth:`read`.


   .. method:: reset()

      Đặt lại các bộ đệm của codec được dùng để duy trì trạng thái nội bộ.

      Lưu ý rằng không được thực hiện việc định vị lại stream. Phương thức này chủ yếu nhằm khôi phục sau các lỗi giải mã.


Ngoài các phương thức nêu trên, :class:`StreamReader` cũng phải kế thừa tất cả các phương thức và thuộc tính khác từ stream bên dưới.

.. _stream-reader-writer:

Các đối tượng StreamReaderWriter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:class:`StreamReaderWriter` là một lớp tiện ích cho phép bọc các stream hoạt động ở cả chế độ đọc và ghi.

Thiết kế này cho phép sử dụng các hàm factory được trả về bởi
hàm :func:`lookup` để tạo instance.


.. class:: StreamReaderWriter(stream, Reader, Writer, errors='strict')

   Tạo một instance :class:`StreamReaderWriter`. *stream* phải là một đối tượng giống tệp. *Reader* và *Writer* phải là các hàm factory hoặc lớp cung cấp
   :class:`StreamReader` và interface :class:`StreamWriter` tương ứng. Việc xử lý lỗi được thực hiện theo cùng cách như đã định nghĩa cho các stream reader và writer.

Các instance :class:`StreamReaderWriter` định nghĩa các interface kết hợp của
các lớp :class:`StreamReader` và :class:`StreamWriter`. Chúng kế thừa tất cả các phương thức và thuộc tính khác từ stream bên dưới.


.. _stream-recoder-objects:

Đối tượng StreamRecoder
~~~~~~~~~~~~~~~~~~~~~~~

:class:`StreamRecoder` chuyển đổi dữ liệu từ một encoding này sang encoding khác, đôi khi hữu ích khi làm việc với các môi trường encoding khác nhau.

Thiết kế này cho phép sử dụng các hàm factory được trả về bởi
hàm :func:`lookup` để tạo instance.


.. class:: StreamRecoder(stream, encode, decode, Reader, Writer, errors='strict')

   Tạo một instance :class:`StreamRecoder` thực hiện chuyển đổi hai chiều: *encode* và *decode* hoạt động ở frontend — dữ liệu mà code gọi :meth:`~StreamReader.read` và :meth:`~StreamWriter.write` có thể nhìn thấy, còn *Reader* và *Writer* hoạt động ở backend — dữ liệu trong *stream*.

   Bạn có thể sử dụng các đối tượng này để thực hiện chuyển mã (transcoding) trong suốt, chẳng hạn từ Latin-1 sang UTF-8 và ngược lại.

   Đối số *stream* phải là một đối tượng giống tệp.

   Các đối số *encode* và *decode* phải tuân theo giao diện :class:`Codec`. *Reader* và *Writer* phải là các hàm factory hoặc lớp cung cấp các đối tượng thuộc
   giao diện :class:`StreamReader` và :class:`StreamWriter` tương ứng.

   Việc xử lý lỗi được thực hiện theo cách tương tự như đã định nghĩa cho các stream reader và writer.


Các instance :class:`StreamRecoder` định nghĩa các giao diện kết hợp của
các lớp :class:`StreamReader` và :class:`StreamWriter`. Chúng kế thừa mọi phương thức và thuộc tính khác từ stream bên dưới.


.. _encodings-overview:

Encoding và Unicode
-------------------

Các chuỗi được lưu trữ nội bộ dưới dạng các dãy code point trong phạm vi ``U+0000``--``U+10FFFF``. (Xem :pep:`393` để biết thêm chi tiết về cách triển khai.) Khi một đối tượng chuỗi được sử dụng bên ngoài CPU và bộ nhớ, thứ tự byte và cách các mảng này được lưu trữ dưới dạng byte trở thành vấn đề. Cũng như với các codec khác, việc tuần tự hóa một chuỗi thành một dãy byte được gọi là *encoding*, còn việc tái tạo chuỗi từ dãy byte được gọi là *decoding*. Có nhiều codec tuần tự hóa văn bản khác nhau, được gọi chung là :term:`mã hóa văn bản <text encoding>`.

Kiểu mã hóa văn bản đơn giản nhất (được gọi là ``'latin-1'`` hoặc ``'iso-8859-1'``) ánh xạ các code point từ 0--255 tới các byte ``0x0``--``0xff``, nghĩa là một đối tượng chuỗi chứa các code point lớn hơn ``U+00FF`` không thể được mã hóa bằng codec này. Thực hiện việc đó sẽ gây ra :exc:`UnicodeEncodeError` có dạng như sau (mặc dù chi tiết của thông báo lỗi có thể khác): ``UnicodeEncodeError: 'latin-1' codec can't encode character '\u1234' in position 3: ordinal not in range(256)``.

Có một nhóm kiểu mã hóa khác (được gọi là các kiểu mã hóa charmap) chọn một tập con khác của toàn bộ các code point Unicode và cách ánh xạ các code point này tới các byte ``0x0``--``0xff``. Để xem cách thực hiện, chỉ cần mở chẳng hạn :file:`encodings/cp1252.py` (một kiểu mã hóa được sử dụng chủ yếu trên Windows). Có một hằng chuỗi gồm 256 ký tự cho biết ký tự nào được ánh xạ tới giá trị byte nào.

Tất cả các kiểu mã hóa này chỉ có thể mã hóa 256 trong số 1114112 code point được định nghĩa trong Unicode. Một cách đơn giản và trực tiếp có thể lưu trữ mỗi code point Unicode là lưu mỗi code point dưới dạng bốn byte liên tiếp. Có hai khả năng: lưu các byte theo thứ tự big endian hoặc little endian. Hai kiểu mã hóa này lần lượt được gọi là ``UTF-32-BE`` và ``UTF-32-LE``. Nhược điểm của chúng là, chẳng hạn, nếu bạn sử dụng ``UTF-32-BE`` trên một máy little endian, bạn sẽ luôn phải hoán đổi các byte khi mã hóa và giải mã. Các codec ``UTF-16`` và ``UTF-32`` của Python tránh được vấn đề này bằng cách sử dụng thứ tự byte gốc của nền tảng khi không có BOM. Python tuân theo cách thực hành phổ biến của nền tảng, vì vậy dữ liệu native-endian có thể round-trip mà không cần hoán đổi byte dư thừa, mặc dù Unicode Standard mặc định sử dụng big endian khi thứ tự byte không được chỉ định. Khi các byte này được CPU có endianness khác đọc, chúng phải được hoán đổi. Để phát hiện endianness của một chuỗi byte ``UTF-16`` hoặc ``UTF-32``, người ta sử dụng BOM ("Byte Order Mark"). Đây là ký tự Unicode ``U+FEFF``. Ký tự này có thể được thêm vào đầu mọi chuỗi byte ``UTF-16`` hoặc ``UTF-32``. Phiên bản đã hoán đổi byte của ký tự này (``0xFFFE``) là một ký tự không hợp lệ, không được xuất hiện trong văn bản Unicode. Khi ký tự đầu tiên của chuỗi byte ``UTF-16`` hoặc ``UTF-32`` là ``U+FFFE``, các byte phải được hoán đổi khi giải mã.

Đáng tiếc là ký tự ``U+FEFF`` còn có một mục đích thứ hai, đó là một ``ZERO WIDTH NO-BREAK SPACE``: một ký tự không có độ rộng và không cho phép tách một từ. Ví dụ, nó có thể được dùng để cung cấp gợi ý cho thuật toán ligature. Kể từ Unicode 4.0, việc sử dụng ``U+FEFF`` làm ``ZERO WIDTH NO-BREAK SPACE`` đã bị phản đối (với ``U+2060`` (``WORD JOINER``) đảm nhiệm vai trò này). Tuy vậy, phần mềm Unicode vẫn phải có khả năng xử lý ``U+FEFF`` trong cả hai vai trò: với tư cách BOM, nó là công cụ xác định bố cục lưu trữ của các byte đã mã hóa và biến mất sau khi chuỗi byte được giải mã thành một chuỗi; với tư cách ``ZERO WIDTH NO-BREAK SPACE``, nó là một ký tự bình thường được giải mã như mọi ký tự khác.

Có một kiểu mã hóa khác có thể mã hóa toàn bộ phạm vi ký tự Unicode: UTF-8. UTF-8 là kiểu mã hóa 8 bit, nghĩa là UTF-8 không gặp vấn đề về thứ tự byte. Mỗi byte trong một chuỗi byte UTF-8 gồm hai phần: các bit đánh dấu (các bit có ý nghĩa cao nhất) và các bit dữ liệu. Các bit đánh dấu là một chuỗi gồm từ không đến bốn bit ``1`` liên tiếp, theo sau là một bit ``0``. Các ký tự Unicode được mã hóa như sau (với x là các bit dữ liệu, khi nối lại sẽ tạo thành ký tự Unicode):

+-----------------------------------+-------------------------------------+
| Phạm vi                           | Mã hóa                              |
+===================================+=====================================+
| ``U-00000000`` ... ``U-0000007F`` | 0xxxxxxx                            |
+-----------------------------------+-------------------------------------+
| ``U-00000080`` ... ``U-000007FF`` | 110xxxxx 10xxxxxx                   |
+-----------------------------------+-------------------------------------+
| ``U-00000800`` ... ``U-0000FFFF`` | 1110xxxx 10xxxxxx 10xxxxxx          |
+-----------------------------------+-------------------------------------+
| ``U-00010000`` ... ``U-0010FFFF`` | 11110xxx 10xxxxxx 10xxxxxx 10xxxxxx |
+-----------------------------------+-------------------------------------+

Bit có trọng số thấp nhất của ký tự Unicode là bit x ngoài cùng bên phải.

Vì UTF-8 là một encoding 8 bit nên không cần BOM, và mọi ký tự ``U+FEFF`` trong chuỗi đã giải mã (ngay cả khi đó là ký tự đầu tiên) đều được coi là một ``ZERO WIDTH NO-BREAK SPACE``.

Nếu không có thông tin bên ngoài thì không thể xác định một cách đáng tin cậy encoding nào đã được dùng để encoding một chuỗi. Mỗi encoding charmap đều có thể giải mã bất kỳ chuỗi byte ngẫu nhiên nào. Tuy nhiên, điều đó không thể thực hiện với UTF-8, vì các chuỗi byte UTF-8 có một cấu trúc không cho phép các chuỗi byte tùy ý. Để tăng độ tin cậy khi phát hiện encoding UTF-8, Microsoft đã phát minh một biến thể của UTF-8 (mà Python gọi là ``"utf-8-sig"``) cho chương trình Notepad của mình: Trước khi bất kỳ ký tự Unicode nào được ghi vào tệp, một BOM được encoding theo UTF-8 (có dạng chuỗi byte như sau: ``0xef``, ``0xbb``, ``0xbf``) sẽ được ghi vào. Vì khá khó có khả năng một tệp được encoding bằng charmap bất kỳ lại bắt đầu bằng các giá trị byte này (những giá trị này, chẳng hạn, sẽ ánh xạ thành

   | CHỮ CÁI I THƯỜNG LATIN CÓ DẤU HAI CHẤM
   | DẤU NGOẶC KÉP GÓC ĐÔI HƯỚNG SANG PHẢI
   | DẤU CHẤM HỎI ĐẢO NGƯỢC

trong iso-8859-1), điều này làm tăng khả năng có thể đoán chính xác encoding ``utf-8-sig`` từ chuỗi byte. Vì vậy, ở đây BOM không được dùng để xác định thứ tự byte được sử dụng khi tạo chuỗi byte, mà được dùng như một chữ ký giúp đoán encoding. Khi encoding, codec utf-8-sig sẽ ghi ``0xef``, ``0xbb``, ``0xbf`` dưới dạng ba byte đầu tiên vào tệp. Khi giải mã, ``utf-8-sig`` sẽ bỏ qua ba byte đó nếu chúng xuất hiện ở vị trí ba byte đầu tiên trong tệp. Trong UTF-8, không khuyến khích sử dụng BOM và nhìn chung nên tránh sử dụng BOM.


.. _standard-encodings:

Các Encoding Tiêu Chuẩn
-----------------------

Python được tích hợp sẵn một số codec, được triển khai dưới dạng hàm C hoặc bằng các dictionary làm bảng ánh xạ. Bảng sau liệt kê các codec theo tên, cùng với một số bí danh phổ biến và những ngôn ngữ mà encoding có khả năng được sử dụng. Danh sách bí danh và danh sách ngôn ngữ đều không nhằm mục đích đầy đủ. Lưu ý rằng các cách viết chỉ khác nhau về chữ hoa chữ thường hoặc sử dụng dấu gạch ngang thay cho dấu gạch dưới cũng là bí danh hợp lệ, vì chúng tương đương khi được chuẩn hóa bởi
:func:`~encodings.normalize_encoding`. Ví dụ: ``'utf-8'`` là bí danh hợp lệ của codec ``'utf_8'``.

.. note::

   Bảng dưới đây liệt kê các bí danh phổ biến nhất; để xem danh sách đầy đủ, hãy tham khảo tệp :source:`aliases.py <Lib/encodings/aliases.py>` nguồn.

Trên Windows, các codec ``cpXXX`` có sẵn cho tất cả các code page. Tuy nhiên, chỉ những codec được liệt kê trong bảng sau mới được đảm bảo tồn tại trên các nền tảng khác.

.. impl-detail::

   Một số encoding phổ biến có thể bỏ qua cơ chế tra cứu codec để cải thiện hiệu năng. CPython chỉ nhận diện các cơ hội tối ưu hóa này đối với một tập hợp giới hạn các bí danh (không phân biệt chữ hoa chữ thường): utf-8, utf8, latin-1, latin1, iso-8859-1, iso8859-1, mbcs (chỉ trên Windows), ascii, us-ascii, utf-16, utf16, utf-32, utf32 và các bí danh tương tự sử dụng dấu gạch dưới thay cho dấu gạch ngang. Việc sử dụng bí danh thay thế cho các encoding này có thể khiến quá trình thực thi chậm hơn.

   .. versionchanged:: 3.6
      Đã nhận diện cơ hội tối ưu hóa cho us-ascii.

Nhiều bộ ký tự hỗ trợ cùng một ngôn ngữ. Chúng khác nhau ở từng ký tự (ví dụ: có hỗ trợ EURO SIGN hay không) và ở cách gán ký tự vào các vị trí mã. Đặc biệt đối với các ngôn ngữ châu Âu, thường tồn tại các biến thể sau:

* một codeset ISO 8859

* một code page Microsoft Windows, thường được phát triển từ một codeset 8859 nhưng thay thế các ký tự điều khiển bằng các ký tự đồ họa bổ sung

* một code page IBM EBCDIC

* một code page IBM PC, tương thích với ASCII

.. tabularcolumns:: |l|p{0.3\linewidth}|p{0.3\linewidth}|

+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| Codec           | Aliases                                                                                  | Languages                                                         |
+=================+==========================================================================================+===================================================================+
| ascii           | 646, us-ascii                                                                            | Tiếng Anh                                                         |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| big5            | big5-tw, csbig5                                                                          | Tiếng Trung phồn thể                                              |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| big5hkscs       | big5-hkscs, hkscs                                                                        | Tiếng Trung phồn thể                                              |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp037           | IBM037, IBM039                                                                           | Tiếng Anh                                                         |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp273           | 273, IBM273, csIBM273                                                                    | Tiếng Đức                                                         |
|                 |                                                                                          |                                                                   |
|                 |                                                                                          | .. versionadded:: 3.4                                             |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp424           | EBCDIC-CP-HE, IBM424                                                                     | Tiếng Hebrew                                                      |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp437           | 437, IBM437                                                                              | Tiếng Anh                                                         |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp500           | EBCDIC-CP-BE, EBCDIC-CP-CH, IBM500                                                       | Tây Âu                                                            |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp720           |                                                                                          | Tiếng Ả Rập                                                       |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp737           |                                                                                          | Tiếng Hy Lạp                                                      |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp775           | IBM775                                                                                   | Các ngôn ngữ Baltic                                               |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp850           | 850, IBM850                                                                              | Tây Âu                                                            |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp852           | 852, IBM852                                                                              | Trung và Đông Âu                                                  |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp855           | 855, IBM855                                                                              | Belarus, Bulgaria, Bắc Macedonia, Nga, Serbia                     |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp856           |                                                                                          | Hebrew                                                            |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp857           | 857, IBM857                                                                              | Tiếng Thổ Nhĩ Kỳ                                                  |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp858           | 858, IBM00858                                                                            | Tây Âu                                                            |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp860           | 860, IBM860                                                                              | Tiếng Bồ Đào Nha                                                  |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp861           | 861, CP-IS, IBM861                                                                       | Tiếng Iceland                                                     |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp862           | 862, IBM862                                                                              | Tiếng Hebrew                                                      |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp863           | 863, IBM863                                                                              | Canada                                                            |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp864           | IBM864                                                                                   | Ả Rập                                                             |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp865           | 865, IBM865                                                                              | Đan Mạch, Na Uy                                                   |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp866           | 866, IBM866                                                                              | Nga                                                               |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp869           | 869, CP-GR, IBM869                                                                       | Hy Lạp                                                            |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp874           |                                                                                          | Thái                                                              |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp875           |                                                                                          | Hy Lạp                                                            |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp932           | 932, ms932, mskanji, ms-kanji, windows-31j                                               | Tiếng Nhật                                                        |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp949           | 949, ms949, uhc                                                                          | Tiếng Hàn                                                         |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp950           | 950, ms950                                                                               | Tiếng Trung phồn thể                                              |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp1006          |                                                                                          | Urdu                                                              |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp1026          | ibm1026                                                                                  | Tiếng Thổ Nhĩ Kỳ                                                  |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp1125          | 1125, ibm1125, cp866u, ruscii                                                            | Tiếng Ukraina                                                     |
|                 |                                                                                          |                                                                   |
|                 |                                                                                          | .. versionadded:: 3.4                                             |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp1140          | IBM01140                                                                                 | Tây Âu                                                            |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp1250          | windows-1250                                                                             | Trung và Đông Âu                                                  |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp1251          | windows-1251                                                                             | Belarus, Bulgaria, Bắc Macedonia, Nga, Serbia                     |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp1252          | windows-1252                                                                             | Tây Âu                                                            |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp1253          | windows-1253                                                                             | Tiếng Hy Lạp                                                      |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp1254          | windows-1254                                                                             | Tiếng Thổ Nhĩ Kỳ                                                  |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp1255          | windows-1255                                                                             | Tiếng Hebrew                                                      |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp1256          | windows-1256                                                                             | Tiếng Ả Rập                                                       |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp1257          | windows-1257                                                                             | Các ngôn ngữ Baltic                                               |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| cp1258          | windows-1258                                                                             | Tiếng Việt                                                        |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| euc_jp          | eucjp, ujis, u-jis                                                                       | Tiếng Nhật                                                        |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| euc_jis_2004    | jisx0213, eucjis2004                                                                     | Tiếng Nhật                                                        |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| euc_jisx0213    | eucjisx0213                                                                              | Tiếng Nhật                                                        |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| euc_kr          | euckr, korean, ksc5601, ks_c-5601, ks_c-5601-1987, ksx1001, ks_x-1001                    | Tiếng Hàn                                                         |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| gb2312          | chinese, csiso58gb231280, euc-cn, euccn, eucgb2312-cn, gb2312-1980, gb2312-80, iso-ir-58 | Tiếng Trung giản thể                                              |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| gbk             | 936, cp936, ms936                                                                        | Tiếng Trung hợp nhất                                              |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| gb18030         | gb18030-2000                                                                             | Tiếng Trung hợp nhất                                              |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| hz              | hzgb, hz-gb, hz-gb-2312                                                                  | Tiếng Trung giản thể                                              |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| iso2022_jp      | csiso2022jp, iso2022jp, iso-2022-jp                                                      | Tiếng Nhật                                                        |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| iso2022_jp_1    | iso2022jp-1, iso-2022-jp-1                                                               | Tiếng Nhật                                                        |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| iso2022_jp_2    | iso2022jp-2, iso-2022-jp-2                                                               | Tiếng Nhật, Tiếng Hàn, Tiếng Trung giản thể, Tây Âu, Tiếng Hy Lạp |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| iso2022_jp_2004 | iso2022jp-2004, iso-2022-jp-2004                                                         | tiếng Nhật                                                        |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| iso2022_jp_3    | iso2022jp-3, iso-2022-jp-3                                                               | tiếng Nhật                                                        |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| iso2022_jp_ext  | iso2022jp-ext, iso-2022-jp-ext                                                           | Tiếng Nhật                                                        |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| iso2022_kr      | csiso2022kr, iso2022kr, iso-2022-kr                                                      | Tiếng Hàn                                                         |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| latin_1         | iso-8859-1, iso8859-1, 8859, cp819, latin, latin1, L1                                    | Tây Âu                                                            |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| iso8859_2       | iso-8859-2, latin2, L2                                                                   | Trung và Đông Âu                                                  |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| iso8859_3       | iso-8859-3, latin3, L3                                                                   | Esperanto, tiếng Malta                                            |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| iso8859_4       | iso-8859-4, latin4, L4                                                                   | Bắc Âu                                                            |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| iso8859_5       | iso-8859-5, cyrillic                                                                     | Belarus, Bulgaria, Bắc Macedonia, Nga, Serbia                     |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| iso8859_6       | iso-8859-6, arabic                                                                       | Tiếng Ả Rập                                                       |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| iso8859_7       | iso-8859-7, greek, greek8                                                                | Tiếng Hy Lạp                                                      |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| iso8859_8       | iso-8859-8, hebrew                                                                       | Tiếng Hebrew                                                      |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| iso8859_9       | iso-8859-9, latin5, L5                                                                   | Tiếng Thổ Nhĩ Kỳ                                                  |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| iso8859_10      | iso-8859-10, latin6, L6                                                                  | Các ngôn ngữ Bắc Âu                                               |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| iso8859_11      | iso-8859-11, thai                                                                        | Các ngôn ngữ Thái                                                 |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| iso8859_13      | iso-8859-13, latin7, L7                                                                  | Các ngôn ngữ Baltic                                               |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| iso8859_14      | iso-8859-14, latin8, L8                                                                  | Các ngôn ngữ Celt                                                 |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| iso8859_15      | iso-8859-15, latin9, L9                                                                  | Tây Âu                                                            |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| iso8859_16      | iso-8859-16, latin10, L10                                                                | Đông Nam Âu                                                       |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| johab           | cp1361, ms1361                                                                           | Tiếng Hàn                                                         |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| koi8_r          |                                                                                          | Tiếng Nga                                                         |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| koi8_t          |                                                                                          | Tiếng Tajik                                                       |
|                 |                                                                                          |                                                                   |
|                 |                                                                                          | .. versionadded:: 3.5                                             |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| koi8_u          |                                                                                          | Tiếng Ukraina                                                     |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| kz1048          | kz_1048, strk1048_2002, rk1048                                                           | Tiếng Kazakh                                                      |
|                 |                                                                                          |                                                                   |
|                 |                                                                                          | .. versionadded:: 3.5                                             |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| mac_cyrillic    | maccyrillic                                                                              | Belarus, Bulgaria, Bắc Macedonia, Nga, Serbia                     |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| mac_greek       | macgreek                                                                                 | Tiếng Hy Lạp                                                      |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| mac_iceland     | maciceland                                                                               | Tiếng Iceland                                                     |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| mac_latin2      | maclatin2, maccentraleurope, mac_centeuro                                                | Trung và Đông Âu                                                  |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| mac_roman       | macroman, macintosh                                                                      | Tây Âu                                                            |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| mac_turkish     | macturkish                                                                               | Tiếng Thổ Nhĩ Kỳ                                                  |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| ptcp154         | csptcp154, pt154, cp154, cyrillic-asian                                                  | Tiếng Kazakh                                                      |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| shift_jis       | csshiftjis, shiftjis, sjis, s_jis                                                        | Tiếng Nhật                                                        |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| shift_jis_2004  | shiftjis2004, sjis_2004, sjis2004                                                        | Tiếng Nhật                                                        |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| shift_jisx0213  | shiftjisx0213, sjisx0213, s_jisx0213                                                     | Tiếng Nhật                                                        |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| utf_32          | U32, utf32                                                                               | mọi ngôn ngữ                                                      |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| utf_32_be       | UTF-32BE                                                                                 | mọi ngôn ngữ                                                      |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| utf_32_le       | UTF-32LE                                                                                 | tất cả ngôn ngữ                                                   |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| utf_16          | U16, utf16                                                                               | tất cả ngôn ngữ                                                   |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| utf_16_be       | UTF-16BE                                                                                 | tất cả ngôn ngữ                                                   |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| utf_16_le       | UTF-16LE                                                                                 | tất cả ngôn ngữ                                                   |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| utf_7           | U7, unicode-1-1-utf-7                                                                    | tất cả ngôn ngữ                                                   |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| utf_8           | U8, UTF, utf8, cp65001                                                                   | tất cả ngôn ngữ                                                   |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+
| utf_8_sig       |                                                                                          | tất cả ngôn ngữ                                                   |
+-----------------+------------------------------------------------------------------------------------------+-------------------------------------------------------------------+

.. versionchanged:: 3.4
   Các bộ mã hóa utf-16\* và utf-32\* không còn cho phép mã hóa các code point surrogate (``U+D800``--``U+DFFF``). Các bộ giải mã utf-32\* không còn giải mã các chuỗi byte tương ứng với code point surrogate.

.. versionchanged:: 3.8
   ``cp65001`` hiện là bí danh của ``utf_8``.

.. versionchanged:: 3.14
   Trên Windows, các codec ``cpXXX`` hiện có sẵn cho tất cả các code page.


Các Encodings riêng của Python
------------------------------

Một số codec được định nghĩa sẵn chỉ dành riêng cho Python, vì vậy tên codec của chúng không có ý nghĩa bên ngoài Python. Các codec này được liệt kê trong những bảng dưới đây dựa trên kiểu dữ liệu đầu vào và đầu ra dự kiến (lưu ý rằng mặc dù encoding văn bản là trường hợp sử dụng phổ biến nhất của codec, cơ sở hạ tầng codec bên dưới hỗ trợ các phép biến đổi dữ liệu tùy ý thay vì chỉ encoding văn bản). Đối với các codec bất đối xứng, ý nghĩa được nêu mô tả hướng encoding.

Encoding văn bản
^^^^^^^^^^^^^^^^

Các codec sau đây cung cấp khả năng encoding từ :class:`str` sang :class:`bytes` và
giải mã từ :term:`bytes-like object` sang :class:`str`, tương tự như các encoding văn bản Unicode.

.. tabularcolumns:: |l|p{0.3\linewidth}|p{0.3\linewidth}|

+--------------------+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Bộ mã              | Bí danh    | Ý nghĩa                                                                                                                                                                                                                                                |
+====================+============+========================================================================================================================================================================================================================================================+
| idna               |            | Triển khai :rfc:`3490`, xem thêm                                                                                                                                                                                                                       |
|                    |            | :mod:`encodings.idna`. Chỉ ``errors='strict'`` được hỗ trợ.                                                                                                                                                                                            |
|                    |            |                                                                                                                                                                                                                                                        |
|                    |            | .. warning::                                                                                                                                                                                                                                           |
|                    |            |                                                                                                                                                                                                                                                        |
|                    |            |    Bộ mã này dựa trên ``punycode``, các thuật toán của bộ mã này có khả năng mở rộng kém, vì vậy hãy giới hạn độ dài của dữ liệu đầu vào không đáng tin cậy.                                                                                           |
+--------------------+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| mbcs               | ansi, dbcs | Chỉ dành cho Windows: Mã hóa toán hạng theo trang mã ANSI (CP_ACP).                                                                                                                                                                                    |
+--------------------+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| oem                |            | Chỉ dành cho Windows: Mã hóa toán hạng theo trang mã OEM (CP_OEMCP).                                                                                                                                                                                   |
|                    |            |                                                                                                                                                                                                                                                        |
|                    |            | .. versionadded:: 3.6                                                                                                                                                                                                                                  |
+--------------------+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| palmos             |            | Mã hóa của PalmOS 3.5.                                                                                                                                                                                                                                 |
+--------------------+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| punycode           |            | Triển khai :rfc:`3492`. Không hỗ trợ các codec có trạng thái.                                                                                                                                                                                          |
|                    |            |                                                                                                                                                                                                                                                        |
|                    |            | .. warning::                                                                                                                                                                                                                                           |
|                    |            |                                                                                                                                                                                                                                                        |
|                    |            |    Các thuật toán giải mã và mã hóa có hiệu năng kém khi mở rộng, vì vậy hãy giới hạn độ dài của dữ liệu đầu vào không đáng tin cậy.                                                                                                                   |
+--------------------+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| raw_unicode_escape |            | Mã hóa Latin-1 với                                                                                                                                                                                                                                     |
|                    |            | :samp:`\\u{XXXX}` và                                                                                                                                                                                                                                   |
|                    |            | :samp:`\\U{XXXXXXXX}` cho các code point khác. Các dấu gạch chéo ngược hiện có không được escape theo bất kỳ cách nào. Nó được sử dụng trong giao thức Python pickle.                                                                                  |
+--------------------+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| undefined          |            | Codec này chỉ nên được sử dụng cho mục đích kiểm thử.                                                                                                                                                                                                  |
|                    |            |                                                                                                                                                                                                                                                        |
|                    |            | Phát sinh ngoại lệ cho mọi chuyển đổi, kể cả chuỗi rỗng. Trình xử lý lỗi sẽ bị bỏ qua.                                                                                                                                                                 |
+--------------------+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| unicode_escape     |            | Mã hóa phù hợp để dùng làm nội dung của một literal Unicode trong mã nguồn Python được mã hóa bằng ASCII, ngoại trừ việc dấu ngoặc kép không được escape. Giải mã từ mã nguồn Latin-1. Lưu ý rằng mã nguồn Python thực tế sử dụng UTF-8 theo mặc định. |
+--------------------+------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

.. versionchanged:: 3.8
   Codec "unicode_internal" đã bị loại bỏ.


.. _binary-transforms:

Biến đổi nhị phân
^^^^^^^^^^^^^^^^^

Các codec sau đây cung cấp phép biến đổi nhị phân: ánh xạ từ :term:`bytes-like object` đến :class:`bytes`. Chúng không được :meth:`bytes.decode` hỗ trợ (chỉ tạo đầu ra :class:`str`).


.. tabularcolumns:: |l|L|L|L|

+----------------------+-------------------------------------------+---------------------------------------------------------------------------------------+------------------------------------------------+
| Codec                | Bí danh                                   | Ý nghĩa                                                                               | Bộ mã hóa / bộ giải mã                         |
+======================+===========================================+=======================================================================================+================================================+
| base64_codec [#b64]_ | base64, base_64                           | Chuyển toán hạng thành MIME base64 nhiều dòng (kết quả luôn bao gồm ``'\n'`` ở cuối). | :meth:`base64.encodebytes` /                   |
|                      |                                           |                                                                                       | :meth:`base64.decodebytes`                     |
|                      |                                           | .. versionchanged:: 3.4                                                               |                                                |
|                      |                                           |    chấp nhận mọi                                                                      |                                                |
|                      |                                           |    :term:`bytes-like object` làm đầu vào để mã hóa và giải mã                         |                                                |
+----------------------+-------------------------------------------+---------------------------------------------------------------------------------------+------------------------------------------------+
| bz2_codec            | bz2                                       | Nén toán hạng bằng bz2.                                                               | :meth:`bz2.compress` /                         |
|                      |                                           |                                                                                       | :meth:`bz2.decompress`                         |
+----------------------+-------------------------------------------+---------------------------------------------------------------------------------------+------------------------------------------------+
| hex_codec            | hex                                       | Chuyển toán hạng sang dạng biểu diễn thập lục phân, với hai chữ số cho mỗi byte.      | :meth:`binascii.b2a_hex` /                     |
|                      |                                           |                                                                                       | :meth:`binascii.a2b_hex`                       |
+----------------------+-------------------------------------------+---------------------------------------------------------------------------------------+------------------------------------------------+
| quopri_codec         | quopri, quotedprintable, quoted_printable | Chuyển toán hạng sang dạng quoted-printable của MIME.                                 | :meth:`quopri.encode` với ``quotetabs=True`` / |
|                      |                                           |                                                                                       | :meth:`quopri.decode`                          |
+----------------------+-------------------------------------------+---------------------------------------------------------------------------------------+------------------------------------------------+
| uu_codec             | uu                                        | Chuyển đổi toán hạng bằng uuencode.                                                   |                                                |
+----------------------+-------------------------------------------+---------------------------------------------------------------------------------------+------------------------------------------------+
| zlib_codec           | zip, zlib                                 | Nén toán hạng bằng gzip.                                                              | :meth:`zlib.compress` /                        |
|                      |                                           |                                                                                       | :meth:`zlib.decompress`                        |
+----------------------+-------------------------------------------+---------------------------------------------------------------------------------------+------------------------------------------------+

.. [#b64] Ngoài :term:`các đối tượng dạng bytes <bytes-like object>`, ``'base64_codec'`` cũng chấp nhận các instance chỉ chứa ASCII của :class:`str` để giải mã

.. versionadded:: 3.2
   Khôi phục các phép biến đổi nhị phân.

.. versionchanged:: 3.4
   Khôi phục các bí danh cho các phép biến đổi nhị phân.


.. _standalone-codec-functions:

Các hàm Codec độc lập
^^^^^^^^^^^^^^^^^^^^^

Các hàm sau đây cung cấp chức năng mã hóa và giải mã tương tự như codec, nhưng không khả dụng dưới dạng codec có tên thông qua :func:`codecs.encode` hoặc :func:`codecs.decode`. Chúng được sử dụng nội bộ (ví dụ: bởi :mod:`pickle`) và hoạt động tương tự codec ``string_escape`` đã bị loại bỏ trong Python 3.

.. function:: codecs.escape_encode(input, errors=None)

   Mã hóa *input* bằng các escape sequence. Tương tự như cách :func:`repr` trên bytes tạo ra các giá trị byte đã escape.

   *input* phải là một đối tượng :class:`bytes`.

   Trả về một tuple ``(output, length)``, trong đó *output* là một đối tượng :class:`bytes` và *length* là số byte đã được sử dụng.

.. function:: codecs.escape_decode(input, errors=None)

   Giải mã *input* từ các escape sequence trở lại thành các byte ban đầu.

   *input* phải là một :term:`bytes-like object`.

   Trả về một tuple ``(output, length)``, trong đó *output* là một đối tượng :class:`bytes` và *length* là số byte đã được sử dụng.


.. _text-transforms:

Biến đổi văn bản
^^^^^^^^^^^^^^^^

Codec sau đây cung cấp một phép biến đổi văn bản: ánh xạ từ :class:`str` sang :class:`str`. Codec này không được :meth:`str.encode` hỗ trợ (chỉ tạo ra
đầu ra :class:`bytes`).

.. tabularcolumns:: |l|l|L|

+--------+---------+-----------------------------------------+
| Codec  | Aliases | Ý nghĩa                                 |
+========+=========+=========================================+
| rot_13 | rot13   | Trả về bản mã hóa Caesar của toán hạng. |
+--------+---------+-----------------------------------------+

.. versionadded:: 3.2
   Giải mã phép biến đổi văn bản ``rot_13``.

.. versionchanged:: 3.4
   Giải mã bí danh ``rot13``.


:mod:`!encodings` --- Gói mã hóa
--------------------------------

.. module:: encodings
   :synopsis: Gói Encodings

Mô-đun này triển khai các hàm sau:

.. function:: normalize_encoding(encoding)

   Chuẩn hóa tên encoding *encoding*.

   Việc chuẩn hóa được thực hiện như sau: tất cả các ký tự không phải chữ và số, ngoại trừ dấu chấm được dùng cho tên package Python, sẽ được gộp lại và thay thế bằng một dấu gạch dưới duy nhất; các dấu gạch dưới ở đầu và cuối sẽ bị loại bỏ. Ví dụ, ``'  -;#'`` trở thành ``'_'``.

   Lưu ý rằng *encoding* chỉ nên chứa ASCII.


.. note::
   Không nên sử dụng trực tiếp các hàm sau đây, ngoại trừ cho mục đích kiểm thử; thay vào đó, nên sử dụng :func:`codecs.lookup`.


.. function:: search_function(encoding)

   Tìm mô-đun codec tương ứng với tên encoding đã cho *encoding*.

   Hàm này trước tiên chuẩn hóa *encoding* bằng
   :func:`normalize_encoding`, sau đó tìm alias tương ứng. Hàm cố gắng import một codec module từ package encodings bằng alias hoặc tên đã được chuẩn hóa. Nếu tìm thấy module và module định nghĩa một hàm ``getregentry()`` hợp lệ trả về một đối tượng :class:`codecs.CodecInfo`, codec sẽ được lưu vào bộ nhớ đệm và trả về.

   Nếu codec module định nghĩa một hàm ``getaliases()``, mọi alias được trả về sẽ được đăng ký để sử dụng về sau.


.. function:: win32_code_page_search_function(encoding)

   Tìm encoding trang mã Windows *encoding* có dạng ``cpXXXX``.

   Nếu trang mã hợp lệ và được hỗ trợ, trả về một đối tượng :class:`codecs.CodecInfo` cho trang mã đó.

   .. availability:: Windows.

   .. versionadded:: 3.14


Module này triển khai ngoại lệ sau:

.. exception:: CodecRegistryError

   Được phát sinh khi codec không hợp lệ hoặc không tương thích.


:mod:`!encodings.idna` --- Tên miền quốc tế hóa trong ứng dụng
--------------------------------------------------------------

.. module:: encodings.idna
   :synopsis: Triển khai Tên miền quốc tế hóa
.. moduleauthor:: Martin v. Löwis

Mô-đun này triển khai :rfc:`3490` (Tên miền quốc tế hóa trong ứng dụng) và :rfc:`3492` (Nameprep: Hồ sơ Stringprep cho Tên miền quốc tế hóa (IDN)). Mô-đun này dựa trên mã hóa ``punycode`` và :mod:`stringprep`.

.. warning::

   Mô-đun này dựa trên ``punycode``, trong đó các thuật toán có hiệu năng kém khi mở rộng, vì vậy hãy giới hạn độ dài của dữ liệu đầu vào không đáng tin cậy.

Nếu cần tiêu chuẩn IDNA 2008 từ :rfc:`5891` và :rfc:`5895`, hãy sử dụng mô-đun bên thứ ba :pypi:`idna`.

Các RFC này cùng định nghĩa một giao thức hỗ trợ các ký tự không phải ASCII trong tên miền. Tên miền chứa các ký tự không phải ASCII (chẳng hạn như ``www.Alliancefrançaise.nu``) được chuyển đổi thành dạng mã hóa tương thích ASCII (ACE, chẳng hạn như ``www.xn--alliancefranaise-npb.nu``). Sau đó, dạng ACE của tên miền được sử dụng ở mọi nơi mà giao thức không cho phép các ký tự tùy ý, chẳng hạn như trong các truy vấn DNS, các trường HTTP :mailheader:`Host`, v.v. Việc chuyển đổi này được thực hiện trong ứng dụng; nếu có thể thì người dùng không nhận thấy: Ứng dụng phải tự động chuyển đổi các nhãn miền Unicode thành IDNA khi truyền qua mạng, rồi chuyển các nhãn ACE trở lại Unicode trước khi hiển thị cho người dùng.

Python hỗ trợ việc chuyển đổi này theo nhiều cách: codec ``idna`` thực hiện chuyển đổi giữa Unicode và ACE, tách một chuỗi đầu vào thành các nhãn dựa trên các ký tự phân tách được định nghĩa trong :rfc:`section 3.1 of RFC 3490 <3490#section-3.1>` và chuyển đổi từng nhãn thành ACE khi cần, đồng thời tách một chuỗi byte đầu vào thành các nhãn dựa trên dấu phân tách ``.`` và chuyển mọi nhãn ACE tìm thấy thành unicode. Ngoài ra, mô-đun :mod:`socket` tự động chuyển đổi tên máy chủ Unicode thành ACE, để ứng dụng không cần tự xử lý việc chuyển đổi tên máy chủ khi truyền chúng cho mô-đun socket. Hơn nữa, các mô-đun có tên máy chủ làm tham số hàm, chẳng hạn như :mod:`http.client` và :mod:`ftplib`, chấp nhận tên máy chủ Unicode (:mod:`http.client` khi đó cũng tự động gửi một tên máy chủ IDNA trong
:mailheader:`Host` trường nếu nó gửi trường đó).

Khi nhận tên máy chủ từ wire (chẳng hạn như trong quá trình tra cứu tên ngược), không có việc tự động chuyển đổi sang Unicode: các ứng dụng muốn hiển thị những tên máy chủ đó cho người dùng nên giải mã chúng thành Unicode.

Mô-đun :mod:`!encodings.idna` cũng triển khai quy trình nameprep, thực hiện một số bước chuẩn hóa trên tên máy chủ để đạt được tính không phân biệt chữ hoa chữ thường của các tên miền quốc tế hóa và hợp nhất các ký tự tương tự. Nếu muốn, bạn có thể sử dụng trực tiếp các hàm nameprep.


.. function:: nameprep(label)

   Trả về phiên bản đã qua nameprep của *label*. Hiện tại, phần triển khai giả định các chuỗi truy vấn, vì vậy ``AllowUnassigned`` là true.


.. function:: ToASCII(label)

   Chuyển đổi một label sang ASCII, như được quy định trong :rfc:`3490`. Giả định rằng ``UseSTD3ASCIIRules`` là false.


.. function:: ToUnicode(label)

   Chuyển đổi một label sang Unicode, như được quy định trong :rfc:`3490`.


:mod:`!encodings.mbcs` --- Bảng mã ANSI của Windows
---------------------------------------------------

.. module:: encodings.mbcs
   :synopsis: bảng mã ANSI của Windows

Mô-đun này triển khai bảng mã ANSI (CP_ACP).

.. availability:: Windows.

.. versionchanged:: 3.2
   Trước phiên bản 3.2, đối số *errors* bị bỏ qua; ``'replace'`` luôn được dùng để mã hóa, còn ``'ignore'`` được dùng để giải mã.

.. versionchanged:: 3.3
   Hỗ trợ mọi error handler.


:mod:`!encodings.utf_8_sig` --- codec UTF-8 có chữ ký BOM
---------------------------------------------------------

.. module:: encodings.utf_8_sig
   :synopsis: codec UTF-8 có chữ ký BOM
.. moduleauthor:: Walter Dörwald

Mô-đun này triển khai một biến thể của codec UTF-8. Khi mã hóa, một BOM được mã hóa theo UTF-8 sẽ được thêm vào trước các byte đã mã hóa theo UTF-8. Đối với encoder có trạng thái, thao tác này chỉ được thực hiện một lần (khi ghi lần đầu tiên vào byte stream). Khi giải mã, BOM được mã hóa theo UTF-8 ở đầu dữ liệu, nếu có, sẽ bị bỏ qua.
