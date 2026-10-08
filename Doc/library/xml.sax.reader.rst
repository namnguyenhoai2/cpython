:mod:`!xml.sax.xmlreader` --- Giao diện cho trình phân tích cú pháp XML
=======================================================================

.. module:: xml.sax.xmlreader
   :synopsis: Giao diện mà các trình phân tích cú pháp XML tuân thủ SAX phải triển khai.

.. moduleauthor:: Lars Marius Garshol <larsga@garshol.priv.no>
.. sectionauthor:: Martin v. Löwis <martin@v.loewis.de>

**Mã nguồn:** :source:`Lib/xml/sax/xmlreader.py`

--------------

Các trình phân tích cú pháp SAX triển khai giao diện :class:`XMLReader`. Chúng được triển khai trong một mô-đun Python, mô-đun này phải cung cấp một hàm :func:`create_parser`. Hàm này được :func:`xml.sax.make_parser` gọi không có đối số để tạo một đối tượng trình phân tích cú pháp mới.


.. class:: XMLReader()

   Lớp cơ sở mà các trình phân tích cú pháp SAX có thể kế thừa.


.. class:: IncrementalParser()

   Trong một số trường hợp, bạn không nên phân tích cú pháp toàn bộ nguồn đầu vào cùng một lúc, mà nên cung cấp từng phần của tài liệu khi chúng sẵn sàng. Lưu ý rằng reader thường cũng không đọc toàn bộ tệp mà đọc theo từng phần; tuy nhiên, :meth:`parse` sẽ không trả về cho đến khi toàn bộ tài liệu được xử lý. Vì vậy, nên sử dụng các giao diện này nếu hành vi blocking của :meth:`parse` không phù hợp.

   Khi được khởi tạo, parser đã sẵn sàng ngay lập tức để nhận dữ liệu từ phương thức feed. Sau khi hoàn tất việc phân tích cú pháp bằng một lệnh gọi đến close, phải gọi phương thức reset để đưa parser về trạng thái sẵn sàng nhận dữ liệu mới, είτε từ feed hoặc bằng phương thức parse.

   Lưu ý rằng các phương thức này *không* được gọi trong quá trình phân tích cú pháp, tức là sau khi parse được gọi và trước khi nó trả về.

   Theo mặc định, lớp này cũng triển khai phương thức parse của interface XMLReader bằng cách sử dụng các phương thức feed, close và reset của interface IncrementalParser, nhằm tạo thuận tiện cho các tác giả viết driver SAX 2.0.


.. class:: Locator()

   Interface dùng để liên kết một sự kiện SAX với vị trí trong tài liệu. Đối tượng locator chỉ trả về kết quả hợp lệ trong các lần gọi đến các phương thức của DocumentHandler; vào bất kỳ thời điểm nào khác, kết quả là không thể dự đoán. Nếu không có thông tin, các phương thức có thể trả về ``None``.


.. class:: InputSource(system_id=None)

   Đóng gói thông tin cần thiết cho :class:`XMLReader` để đọc các entity.

   Lớp này có thể chứa thông tin về public identifier, system identifier, byte stream (có thể kèm thông tin về encoding ký tự) và/hoặc character stream của một entity.

   Các ứng dụng sẽ tạo các đối tượng của lớp này để sử dụng trong
   :meth:`XMLReader.parse` method và để trả về từ EntityResolver.resolveEntity.

   Một :class:`InputSource` thuộc về ứng dụng; :class:`XMLReader` không được phép sửa đổi các đối tượng :class:`InputSource` được ứng dụng truyền cho nó, mặc dù nó có thể tạo bản sao và sửa đổi các bản sao đó.


.. class:: AttributesImpl(attrs)

   Đây là một cách triển khai giao diện :class:`Attributes` (xem phần
   :ref:`attributes-objects`). Đây là một đối tượng giống từ điển, biểu diễn các thuộc tính của phần tử trong một lệnh gọi :meth:`startElement`. Ngoài các thao tác từ điển hữu ích nhất, đối tượng này còn hỗ trợ một số phương thức khác như được mô tả trong giao diện. Các đối tượng thuộc lớp này nên được reader khởi tạo; *attrs* phải là một đối tượng giống từ điển chứa ánh xạ từ tên thuộc tính đến giá trị thuộc tính.


.. class:: AttributesNSImpl(attrs, qnames)

   Biến thể nhận biết namespace của :class:`AttributesImpl`, sẽ được truyền cho
   :meth:`startElementNS`. Nó được kế thừa từ :class:`AttributesImpl`, nhưng hiểu tên thuộc tính là các bộ đôi gồm *namespaceURI* và *localname*. Ngoài ra, nó cung cấp một số phương thức nhận tên đủ điều kiện như xuất hiện trong tài liệu gốc. Lớp này triển khai giao diện
   :class:`AttributesNS` (xem phần :ref:`attributes-ns-objects`).


.. _xmlreader-objects:

Đối tượng XMLReader
-------------------

Giao diện :class:`XMLReader` hỗ trợ các phương thức sau:


.. method:: XMLReader.parse(source)

   Xử lý một nguồn đầu vào và tạo ra các sự kiện SAX. Đối tượng *source* có thể là một system identifier (một chuỗi xác định nguồn đầu vào -- thường là tên tệp hoặc URL), một :class:`pathlib.Path` hoặc đối tượng :term:`path-like <path-like object>`, hoặc một đối tượng :class:`InputSource`. Khi
   :meth:`parse` trả về, dữ liệu đầu vào đã được xử lý hoàn toàn và có thể loại bỏ hoặc đặt lại đối tượng parser.

   .. versionchanged:: 3.5
      Đã bổ sung hỗ trợ cho các character stream.

   .. versionchanged:: 3.8
      Đã bổ sung hỗ trợ cho các đối tượng path-like.


.. method:: XMLReader.getContentHandler()

   Trả về :class:`~xml.sax.handler.ContentHandler` hiện tại.


.. method:: XMLReader.setContentHandler(handler)

   Đặt :class:`~xml.sax.handler.ContentHandler` hiện tại. Nếu không
   :class:`~xml.sax.handler.ContentHandler` được thiết lập, các sự kiện nội dung sẽ bị loại bỏ.


.. method:: XMLReader.getDTDHandler()

   Trả về :class:`~xml.sax.handler.DTDHandler` hiện tại.


.. method:: XMLReader.setDTDHandler(handler)

   Thiết lập :class:`~xml.sax.handler.DTDHandler` hiện tại.  Nếu không
   :class:`~xml.sax.handler.DTDHandler` được thiết lập, các sự kiện DTD sẽ bị loại bỏ.


.. method:: XMLReader.getEntityResolver()

   Trả về :class:`~xml.sax.handler.EntityResolver` hiện tại.


.. method:: XMLReader.setEntityResolver(handler)

   Thiết lập :class:`~xml.sax.handler.EntityResolver` hiện tại.  Nếu không
   :class:`~xml.sax.handler.EntityResolver` được thiết lập, việc cố gắng phân giải một thực thể bên ngoài sẽ dẫn đến việc mở system identifier của thực thể đó và thất bại nếu nó không khả dụng.


.. method:: XMLReader.getErrorHandler()

   Trả về :class:`~xml.sax.handler.ErrorHandler` hiện tại.


.. method:: XMLReader.setErrorHandler(handler)

   Thiết lập bộ xử lý lỗi hiện tại. Nếu chưa thiết lập :class:`~xml.sax.handler.ErrorHandler`, lỗi sẽ được phát sinh dưới dạng ngoại lệ và cảnh báo sẽ được in ra.


.. method:: XMLReader.setLocale(locale)

   Cho phép ứng dụng thiết lập locale cho lỗi và cảnh báo.

   Các bộ phân tích SAX không bắt buộc phải cung cấp bản địa hóa cho lỗi và cảnh báo; tuy nhiên, nếu không thể hỗ trợ locale được yêu cầu, chúng phải phát sinh một ngoại lệ SAX. Ứng dụng có thể yêu cầu thay đổi locale ở giữa quá trình phân tích.


.. method:: XMLReader.getFeature(featurename)

   Trả về thiết lập hiện tại cho feature *featurename*. Nếu không nhận dạng được feature, :exc:`SAXNotRecognizedException` sẽ được phát sinh. Các featurename được biết đến được liệt kê trong module :mod:`xml.sax.handler`.


.. method:: XMLReader.setFeature(featurename, value)

   Thiết lập *featurename* thành *value*. Nếu không nhận dạng được feature,
   :exc:`SAXNotRecognizedException` sẽ được phát sinh. Nếu parser không hỗ trợ feature hoặc thiết lập của feature, *SAXNotSupportedException* sẽ được phát sinh.


.. method:: XMLReader.getProperty(propertyname)

   Trả về thiết lập hiện tại cho thuộc tính *propertyname*. Nếu không nhận dạng được thuộc tính, một :exc:`SAXNotRecognizedException` sẽ được phát sinh. Các propertyname phổ biến được liệt kê trong module :mod:`xml.sax.handler`.


.. method:: XMLReader.setProperty(propertyname, value)

   Đặt *propertyname* thành *value*. Nếu không nhận dạng được thuộc tính,
   :exc:`SAXNotRecognizedException` sẽ được phát sinh. Nếu parser không hỗ trợ thuộc tính hoặc thiết lập của thuộc tính đó, *SAXNotSupportedException* sẽ được phát sinh.


.. _incremental-parser-objects:

Các đối tượng IncrementalParser
-------------------------------

Các instance của :class:`IncrementalParser` cung cấp các phương thức bổ sung sau:


.. method:: IncrementalParser.feed(data)

   Xử lý một phần *data*.


.. method:: IncrementalParser.close()

   Giả định rằng tài liệu đã kết thúc. Thao tác này sẽ kiểm tra các điều kiện well-formed chỉ có thể được kiểm tra khi kết thúc, gọi các handler và có thể dọn dẹp các tài nguyên được cấp phát trong quá trình phân tích cú pháp.


.. method:: IncrementalParser.prepareParser(source)

   Chuẩn bị parser để phân tích cú pháp *source*, một
   :class:`InputSource` instance. Phương thức này được gọi bởi :meth:`~XMLReader.parse` trước khi nạp dữ liệu. Phần triển khai parser phải ghi đè phương thức này; phần triển khai mặc định sẽ phát sinh :exc:`NotImplementedError`.


.. method:: IncrementalParser.reset()

   Phương thức này được gọi sau khi close được gọi để đặt lại parser, giúp parser sẵn sàng phân tích cú pháp các tài liệu mới. Kết quả của việc gọi parse hoặc feed sau close mà không gọi reset là không xác định.


.. _locator-objects:

Các đối tượng Locator
---------------------

Các instance của :class:`Locator` cung cấp những phương thức sau:


.. method:: Locator.getColumnNumber()

   Trả về số cột nơi sự kiện hiện tại bắt đầu.


.. method:: Locator.getLineNumber()

   Trả về số dòng nơi sự kiện hiện tại bắt đầu.


.. method:: Locator.getPublicId()

   Trả về mã định danh công khai cho sự kiện hiện tại.


.. method:: Locator.getSystemId()

   Trả về mã định danh hệ thống cho sự kiện hiện tại.


.. _input-source-objects:

Đối tượng InputSource
---------------------


.. method:: InputSource.setPublicId(id)

   Đặt mã định danh công khai của :class:`InputSource` này.


.. method:: InputSource.getPublicId()

   Trả về mã định danh công khai của :class:`InputSource` này.


.. method:: InputSource.setSystemId(id)

   Đặt mã định danh hệ thống của :class:`InputSource` này.


.. method:: InputSource.getSystemId()

   Trả về mã định danh hệ thống của :class:`InputSource` này.


.. method:: InputSource.setEncoding(encoding)

   Thiết lập encoding ký tự của :class:`InputSource` này.

   Encoding phải là một chuỗi được chấp nhận trong khai báo encoding của XML (xem mục 4.3.3 của khuyến nghị XML).

   Thuộc tính encoding của :class:`InputSource` sẽ bị bỏ qua nếu
   :class:`InputSource` cũng chứa một luồng ký tự.


.. method:: InputSource.getEncoding()

   Lấy encoding ký tự của InputSource này.


.. method:: InputSource.setByteStream(bytefile)

   Thiết lập luồng byte (một :term:`binary file`) cho input source này.

   SAX parser sẽ bỏ qua luồng này nếu đồng thời có một luồng ký tự được chỉ định, nhưng sẽ ưu tiên sử dụng luồng byte thay vì tự mở kết nối URI.

   Nếu ứng dụng biết encoding ký tự của byte stream, ứng dụng nên thiết lập encoding đó bằng method setEncoding.


.. method:: InputSource.getByteStream()

   Lấy byte stream cho input source này.

   Method getEncoding sẽ trả về encoding ký tự của byte stream này hoặc ``None`` nếu không xác định.


.. method:: InputSource.setCharacterStream(charfile)

   Thiết lập character stream (một :term:`text file`) cho input source này.

   Nếu có character stream được chỉ định, SAX parser sẽ bỏ qua mọi byte stream và không cố mở kết nối URI đến system identifier.


.. method:: InputSource.getCharacterStream()

   Lấy character stream cho input source này.


.. _attributes-objects:

Giao diện :class:`Attributes`
-----------------------------

Các đối tượng :class:`Attributes` triển khai một phần của giao thức :term:`mapping protocol <mapping>`, bao gồm các phương thức :meth:`~collections.abc.Mapping.copy`,
:meth:`~collections.abc.Mapping.get`, :meth:`~object.__contains__`,
:meth:`~collections.abc.Mapping.items`, :meth:`~collections.abc.Mapping.keys` và :meth:`~collections.abc.Mapping.values`. Các phương thức sau đây cũng được cung cấp:


.. method:: Attributes.getLength()

   Trả về số lượng thuộc tính.


.. method:: Attributes.getNames()

   Trả về tên của các thuộc tính.


.. method:: Attributes.getType(name)

   Trả về kiểu của thuộc tính *name*, thường là ``'CDATA'``.


.. method:: Attributes.getValue(name)

   Trả về giá trị của thuộc tính *name*.

.. getValueByQName, getNameByQName, getQNameByName, getQNames available
.. here already, but documented only for derived class.


.. _attributes-ns-objects:

Giao diện :class:`AttributesNS`
-------------------------------

Giao diện này là một kiểu con của giao diện :class:`Attributes` (xem phần
:ref:`attributes-objects`). Tất cả các phương thức được giao diện đó hỗ trợ cũng có sẵn trên các đối tượng :class:`AttributesNS`.

Các phương thức sau cũng có sẵn:


.. method:: AttributesNS.getValueByQName(name)

   Trả về giá trị của một tên đủ điều kiện.


.. method:: AttributesNS.getNameByQName(name)

   Trả về cặp ``(namespace, localname)`` cho một *tên* đủ điều kiện.


.. method:: AttributesNS.getQNameByName(name)

   Trả về tên đủ điều kiện cho một cặp ``(namespace, localname)``.


.. method:: AttributesNS.getQNames()

   Trả về tên đủ điều kiện của tất cả các thuộc tính.

