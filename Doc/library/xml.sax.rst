:mod:`!xml.sax` --- Hỗ trợ các bộ phân tích SAX2
================================================

.. module:: xml.sax
   :synopsis: Gói chứa các lớp cơ sở SAX2 và các hàm tiện ích.

.. moduleauthor:: Lars Marius Garshol <larsga@garshol.priv.no>
.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>
.. sectionauthor:: Martin v. Löwis <martin@v.loewis.de>

**Mã nguồn:** :source:`Lib/xml/sax/__init__.py`

--------------

Gói :mod:`!xml.sax` cung cấp một số mô-đun triển khai giao diện Simple API for XML (SAX) cho Python. Bản thân gói này cung cấp các ngoại lệ SAX và những hàm tiện ích được người dùng API SAX sử dụng nhiều nhất.


.. note::

   Nếu bạn cần phân tích dữ liệu không đáng tin cậy hoặc chưa được xác thực, hãy xem
   :ref:`xml-security`.

.. versionchanged:: 3.7.1

   Theo mặc định, bộ phân tích SAX không còn xử lý các thực thể bên ngoài tổng quát nhằm tăng cường bảo mật. Trước đây, bộ phân tích tạo kết nối mạng để tải các tệp từ xa hoặc tải các tệp cục bộ từ hệ thống tệp cho DTD và các thực thể. Có thể bật lại tính năng này bằng phương thức
   :meth:`~xml.sax.xmlreader.XMLReader.setFeature` trên đối tượng parser và đối số :data:`~xml.sax.handler.feature_external_ges`.

Các hàm tiện ích và dữ liệu là:


.. function:: make_parser(parser_list=())

   Tạo và trả về một đối tượng :class:`~xml.sax.xmlreader.XMLReader` SAX. Trình phân tích cú pháp đầu tiên được tìm thấy sẽ được sử dụng. Nếu cung cấp *parser_list*, đối số này phải là một iterable gồm các chuỗi chỉ tên những module có một hàm tên là :func:`create_parser`. Các module được liệt kê trong *parser_list* sẽ được sử dụng trước các module trong danh sách trình phân tích cú pháp mặc định.

   .. versionchanged:: 3.8
      Đối số *parser_list* có thể là bất kỳ iterable nào, không chỉ là một list.


.. function:: parse(filename_or_stream, handler, errorHandler=handler.ErrorHandler())

   Tạo một trình phân tích cú pháp SAX và sử dụng nó để phân tích một tài liệu. Tài liệu được truyền vào dưới dạng *filename_or_stream* có thể là một system identifier (một chuỗi xác định nguồn đầu vào -- thường là tên tệp hoặc URL), một đối tượng :term:`path-like <path-like object>`, hoặc một đối tượng tệp. System identifier không trỏ đến một tệp hiện có sẽ được mở bằng :func:`urllib.request.urlopen`. Tham số *handler* phải là một instance :class:`~handler.ContentHandler` SAX. Nếu cung cấp *errorHandler*, tham số này phải là một instance :class:`~handler.ErrorHandler` SAX; nếu bỏ qua, :exc:`SAXParseException` sẽ được nêu ra cho mọi lỗi. Hàm không trả về giá trị nào; mọi công việc phải được thực hiện bởi *handler* được truyền vào.


.. function:: parseString(string, handler, errorHandler=handler.ErrorHandler())

   Tương tự :func:`parse`, nhưng phân tích cú pháp từ một buffer *string* được nhận dưới dạng tham số. *string* phải là một instance :class:`str` hoặc một
   :term:`bytes-like object`.

   .. versionchanged:: 3.5
      Đã bổ sung hỗ trợ cho các instance :class:`str`.


.. data:: default_parser_list

   Danh sách tên các module được :func:`make_parser` thử sau các module được nêu trong đối số *parser_list*. Danh sách này chứa ``'xml.sax.expatreader'``, hoặc, nếu
   khi biến môi trường :envvar:`!PY_SAX_PARSER` được đặt và môi trường không bị bỏ qua, danh sách tên module được phân tách bằng dấu phẩy lấy từ biến đó.

Một ứng dụng SAX điển hình sử dụng ba loại đối tượng: reader, handler và input source. “Reader” trong ngữ cảnh này là một thuật ngữ khác chỉ parser, tức một đoạn mã đọc các byte hoặc ký tự từ input source và tạo ra một chuỗi sự kiện. Sau đó, các sự kiện được phân phối đến các đối tượng handler; cụ thể là reader gọi một phương thức trên handler. Vì vậy, một ứng dụng SAX phải lấy một đối tượng reader, tạo hoặc mở các input source, tạo các handler và kết nối tất cả những đối tượng này với nhau. Ở bước chuẩn bị cuối cùng, reader được gọi để phân tích cú pháp input. Trong quá trình phân tích cú pháp, các phương thức trên những đối tượng handler được gọi dựa trên các sự kiện về cấu trúc và cú pháp từ dữ liệu input.

Đối với những đối tượng này, chỉ các interface là đáng quan tâm; thông thường, chính ứng dụng không khởi tạo chúng. Vì Python không có khái niệm rõ ràng về interface, chúng được giới thiệu chính thức dưới dạng các class, nhưng ứng dụng có thể sử dụng các triển khai không kế thừa từ những class được cung cấp. Các
:class:`~xml.sax.xmlreader.InputSource`, :class:`~xml.sax.xmlreader.Locator`,
interface :class:`~xml.sax.xmlreader.Attributes`, :class:`~xml.sax.xmlreader.AttributesNS` và :class:`~xml.sax.xmlreader.XMLReader` được định nghĩa trong module :mod:`xml.sax.xmlreader`. Các interface handler được định nghĩa trong
:mod:`xml.sax.handler`. Để thuận tiện,
:class:`~xml.sax.xmlreader.InputSource` (thường được khởi tạo trực tiếp) và các class handler cũng có sẵn từ
:mod:`!xml.sax`. Các interface này được mô tả dưới đây.

Ngoài các lớp này, :mod:`!xml.sax` cung cấp các lớp ngoại lệ sau.


.. exception:: SAXException(msg, exception=None)

   Đóng gói một lỗi hoặc cảnh báo XML. Lớp này có thể chứa thông tin lỗi hoặc cảnh báo cơ bản từ trình phân tích cú pháp XML hoặc ứng dụng; lớp này có thể được phân lớp để cung cấp thêm chức năng hoặc bổ sung khả năng bản địa hóa. Lưu ý rằng mặc dù các trình xử lý được định nghĩa trong
   giao diện :class:`~xml.sax.handler.ErrorHandler` nhận các thực thể của ngoại lệ này, nhưng không bắt buộc phải thực sự phát sinh ngoại lệ; ngoại lệ này cũng hữu ích như một vùng chứa thông tin.

   Khi được khởi tạo, *msg* phải là mô tả lỗi mà con người có thể đọc được. Tham số *exception* tùy chọn, nếu được cung cấp, phải là ``None`` hoặc một ngoại lệ đã được mã phân tích cú pháp bắt và đang được truyền tiếp dưới dạng thông tin.

   Đây là lớp cơ sở cho các lớp ngoại lệ SAX khác.


.. exception:: SAXParseException(msg, exception, locator)

   Lớp con của :exc:`SAXException`, được phát sinh khi xảy ra lỗi phân tích cú pháp. Các thực thể của lớp này được truyền đến các phương thức của SAX
   giao diện :class:`~xml.sax.handler.ErrorHandler` để cung cấp thông tin về lỗi phân tích cú pháp. Lớp này hỗ trợ SAX
   :class:`~xml.sax.xmlreader.Locator` giao diện cũng như
   :class:`SAXException` giao diện.


.. exception:: SAXNotRecognizedException(msg, exception=None)

   Lớp con của :exc:`SAXException` được phát sinh khi một SAX
   :class:`~xml.sax.xmlreader.XMLReader` gặp phải một tính năng hoặc thuộc tính không được nhận dạng. Các ứng dụng và phần mở rộng SAX có thể sử dụng lớp này cho các mục đích tương tự.


.. exception:: SAXNotSupportedException(msg, exception=None)

   Lớp con của :exc:`SAXException` được phát sinh khi một SAX
   :class:`~xml.sax.xmlreader.XMLReader` được yêu cầu bật một tính năng không được hỗ trợ hoặc đặt một thuộc tính thành giá trị mà phần triển khai không hỗ trợ. Các ứng dụng và phần mở rộng SAX có thể sử dụng lớp này cho các mục đích tương tự.


.. exception:: SAXReaderNotAvailable(msg, exception=None)

   Lớp con của :exc:`SAXNotSupportedException` được phát sinh khi không có parser nào khả dụng. Một module parser sẽ phát sinh ngoại lệ này khi được import hoặc trong quá trình parsing nếu parser mà nó cung cấp không thể được sử dụng, còn :func:`make_parser` sẽ phát sinh ngoại lệ này nếu không có module nào trong số các module đã thử cung cấp parser có thể sử dụng.


.. seealso::

   `SAX: API đơn giản cho XML <http://www.saxproject.org/>`_
      Trang web này là trung tâm định nghĩa SAX API. Trang cung cấp một bản triển khai bằng Java và tài liệu trực tuyến. Bạn cũng có thể tìm thấy các liên kết đến những bản triển khai và thông tin lịch sử.

   Mô-đun :mod:`xml.sax.handler`
      Định nghĩa các interface cho những đối tượng do ứng dụng cung cấp.

   Mô-đun :mod:`xml.sax.saxutils`
      Các hàm tiện ích để sử dụng trong các ứng dụng SAX.

   Mô-đun :mod:`xml.sax.xmlreader`
      Định nghĩa các interface cho những đối tượng do parser cung cấp.


.. _sax-exception-objects:

Đối tượng SAXException
----------------------

Lớp exception :class:`SAXException` hỗ trợ các phương thức sau:


.. method:: SAXException.getMessage()

   Trả về thông báo dễ đọc cho người dùng mô tả điều kiện lỗi.


.. method:: SAXException.getException()

   Trả về đối tượng exception được đóng gói hoặc ``None``.

.. _`SAX: The Simple API for XML`: http://www.saxproject.org/
