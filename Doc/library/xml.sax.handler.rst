:mod:`!xml.sax.handler` --- Các lớp cơ sở cho trình xử lý SAX
=============================================================

.. module:: xml.sax.handler
   :synopsis: Các lớp cơ sở cho trình xử lý sự kiện SAX.

.. moduleauthor:: Lars Marius Garshol <larsga@garshol.priv.no>
.. sectionauthor:: Martin v. Löwis <martin@v.loewis.de>

**Mã nguồn:** :source:`Lib/xml/sax/handler.py`

--------------

API SAX định nghĩa năm loại trình xử lý: trình xử lý nội dung, trình xử lý DTD, trình xử lý lỗi, bộ phân giải thực thể và trình xử lý lexical. Thông thường, ứng dụng chỉ cần triển khai những giao diện mà nó quan tâm đến sự kiện; các giao diện này có thể được triển khai trong một đối tượng duy nhất hoặc trong nhiều đối tượng. Các cài đặt trình xử lý nên kế thừa từ những lớp cơ sở được cung cấp trong mô-đun :mod:`!xml.sax.handler`, để tất cả các phương thức đều có cài đặt mặc định.


.. class:: ContentHandler

   Đây là giao diện callback chính trong SAX và là giao diện quan trọng nhất đối với ứng dụng. Thứ tự các sự kiện trong giao diện này phản ánh thứ tự của thông tin trong tài liệu.


.. class:: DTDHandler

   Xử lý các sự kiện DTD.

   Giao diện này chỉ chỉ định những sự kiện DTD cần thiết cho việc phân tích cú pháp cơ bản (thực thể chưa phân tích và thuộc tính).


.. class:: EntityResolver

   Giao diện cơ bản để phân giải các thực thể. Nếu bạn tạo một đối tượng triển khai giao diện này, sau đó đăng ký đối tượng với Parser của mình, parser sẽ gọi phương thức trong đối tượng để phân giải tất cả các thực thể bên ngoài.


.. class:: ErrorHandler

   Giao diện được parser sử dụng để trình bày các thông báo lỗi và cảnh báo cho ứng dụng. Các phương thức của đối tượng này kiểm soát việc lỗi được chuyển đổi ngay thành ngoại lệ hay được xử lý theo cách khác.


.. class:: LexicalHandler

   Giao diện được parser sử dụng để biểu diễn các sự kiện có tần suất thấp mà nhiều ứng dụng có thể không quan tâm.

Ngoài các lớp này, :mod:`!xml.sax.handler` cung cấp các hằng số tượng trưng cho tên tính năng và thuộc tính.


.. data:: feature_namespaces

   | giá trị: ``"http://xml.org/sax/features/namespaces"``
   | true: Thực hiện xử lý Namespace.
   | false: Tùy chọn không thực hiện xử lý Namespace (ngụ ý namespace-prefixes; mặc định).
   | quyền truy cập: (đang phân tích cú pháp) chỉ đọc; (không phân tích cú pháp) đọc/ghi


.. data:: feature_namespace_prefixes

   | giá trị: ``"http://xml.org/sax/features/namespace-prefixes"``
   | true: Báo cáo các tên có tiền tố và thuộc tính ban đầu được sử dụng cho các khai báo Namespace.
   | false: Không báo cáo các thuộc tính được sử dụng cho các khai báo Namespace và tùy chọn không báo cáo các tên có tiền tố ban đầu (mặc định).
   | quyền truy cập: (đang phân tích cú pháp) chỉ đọc; (không phân tích cú pháp) đọc/ghi

   Trình phân tích cú pháp dựa trên :mod:`xml.parsers.expat` không hỗ trợ tính năng này.


.. data:: feature_string_interning

   | giá trị: ``"http://xml.org/sax/features/string-interning"``
   | true: Tên của tất cả phần tử, tiền tố, tên thuộc tính, URI Namespace và tên cục bộ đều được intern trong một từ điển (xem :data:`property_interning_dict`).
   | false: Tên không nhất thiết được intern, mặc dù chúng có thể được intern (mặc định).
   | quyền truy cập: (đang phân tích cú pháp) chỉ đọc; (không phân tích cú pháp) đọc/ghi


.. data:: feature_validation

   | value: ``"http://xml.org/sax/features/validation"``
   | true: Báo cáo tất cả lỗi validation (bao gồm external-general-entities và external-parameter-entities).
   | false: Không báo cáo lỗi validation.
   | quyền truy cập: (đang phân tích cú pháp) chỉ đọc; (không phân tích cú pháp) đọc/ghi

   Bộ phân tích cú pháp dựa trên :mod:`xml.parsers.expat` không hỗ trợ tính năng này vì Expat là bộ phân tích cú pháp không kiểm tra tính hợp lệ.


.. data:: feature_external_ges

   .. warning::

      Việc bật tính năng này sẽ tạo ra lỗ hổng trước `các cuộc tấn công thực thể bên ngoài <https://en.wikipedia.org/wiki/XML_external_entity_attack>`_ nếu bộ phân tích cú pháp được sử dụng với nội dung XML do người dùng cung cấp. Vui lòng xem xét `mô hình mối đe dọa <https://en.wikipedia.org/wiki/Threat_model>`_ của bạn trước khi bật tính năng này.

   | value: ``"http://xml.org/sax/features/external-general-entities"``
   | true: Bao gồm tất cả thực thể tổng quát (văn bản) bên ngoài.
   | false: Không bao gồm các thực thể tổng quát bên ngoài.
   | quyền truy cập: (đang phân tích cú pháp) chỉ đọc; (không phân tích cú pháp) đọc/ghi


.. data:: feature_external_pes

   | value: ``"http://xml.org/sax/features/external-parameter-entities"``
   | true: Bao gồm tất cả các thực thể tham số bên ngoài, bao gồm cả tập con DTD bên ngoài.
   | false: Không bao gồm bất kỳ thực thể tham số bên ngoài nào, kể cả tập con DTD bên ngoài.
   | quyền truy cập: (đang phân tích cú pháp) chỉ đọc; (không phân tích cú pháp) đọc/ghi

   Trình phân tích cú pháp dựa trên :mod:`xml.parsers.expat` không hỗ trợ tính năng này.


.. data:: all_features

   Danh sách tất cả các tính năng.


.. data:: property_lexical_handler

   | giá trị: ``"http://xml.org/sax/properties/lexical-handler"``
   | kiểu dữ liệu: :class:`~xml.sax.handler.LexicalHandler`
   | mô tả: Một trình xử lý mở rộng tùy chọn cho các sự kiện lexical như chú thích.
   | quyền truy cập: đọc/ghi


.. data:: property_declaration_handler

   | giá trị: ``"http://xml.org/sax/properties/declaration-handler"``
   | kiểu dữ liệu: một đối tượng triển khai giao diện ``DeclHandler`` của SAX2
   | mô tả: Một trình xử lý mở rộng tùy chọn cho các sự kiện liên quan đến DTD, ngoại trừ ký hiệu và thực thể chưa phân tích.
   | quyền truy cập: đọc/ghi

   Không có parser nào trong thư viện chuẩn hỗ trợ thuộc tính này và thư viện chuẩn cũng không cung cấp trình xử lý như vậy.


.. data:: property_dom_node

   | giá trị: ``"http://xml.org/sax/properties/dom-node"``
   | kiểu dữ liệu: :class:`xml.dom.Node`
   | mô tả: Khi đang phân tích cú pháp, node DOM hiện tại đang được duyệt nếu đây là một DOM iterator; khi không phân tích cú pháp, node DOM gốc để lặp.
   | quyền truy cập: (đang phân tích cú pháp) chỉ đọc; (không phân tích cú pháp) đọc/ghi

   Không có parser nào trong thư viện chuẩn hỗ trợ thuộc tính này.


.. data:: property_xml_string

   | giá trị: ``"http://xml.org/sax/properties/xml-string"``
   | kiểu dữ liệu: Bytes
   | mô tả: Chuỗi ký tự nguyên bản là nguồn của sự kiện hiện tại.
   | quyền truy cập: chỉ đọc và chỉ trong callback của handler


.. data:: property_encoding

   | giá trị: ``"http://www.python.org/sax/properties/encoding"``
   | kiểu dữ liệu: String
   | mô tả: Tên của encoding cần giả định cho dữ liệu đầu vào.
   | quyền truy cập: đọc/ghi

   Không có parser nào trong thư viện chuẩn hỗ trợ thuộc tính này.


.. data:: property_interning_dict

   | giá trị: ``"http://www.python.org/sax/properties/interning-dict"``
   | kiểu dữ liệu: Dictionary
   | mô tả: Từ điển dùng để intern tên, hoặc ``None`` nếu tên không được intern. Việc đặt giá trị này sẽ bật tính năng interning, cũng như
     tính năng :data:`feature_string_interning`.
   | quyền truy cập: đọc/ghi


.. data:: all_properties

   Danh sách tất cả tên thuộc tính đã biết.


.. _content-handler-objects:

Đối tượng ContentHandler
------------------------

Người dùng được kỳ vọng sẽ tạo lớp con của :class:`ContentHandler` để hỗ trợ ứng dụng của mình. Các phương thức sau được parser gọi khi xảy ra những sự kiện tương ứng trong tài liệu đầu vào:


.. method:: ContentHandler.setDocumentLocator(locator)

   Được parser gọi để cung cấp cho ứng dụng một locator nhằm xác định nguồn gốc của các sự kiện trong tài liệu.

   Các SAX parser được khuyến khích mạnh mẽ (mặc dù không bắt buộc tuyệt đối) cung cấp một locator: nếu cung cấp, parser phải cung cấp locator cho ứng dụng bằng cách gọi phương thức này trước khi gọi bất kỳ phương thức nào khác trong interface DocumentHandler.

   Locator cho phép ứng dụng xác định vị trí kết thúc của bất kỳ sự kiện nào liên quan đến tài liệu, ngay cả khi parser không báo lỗi. Thông thường, ứng dụng sẽ sử dụng thông tin này để báo cáo các lỗi của chính mình (chẳng hạn như nội dung ký tự không khớp với các quy tắc nghiệp vụ của ứng dụng). Thông tin do locator trả về có thể không đủ để sử dụng với công cụ tìm kiếm.

   Lưu ý rằng locator chỉ trả về thông tin chính xác trong khi các sự kiện thuộc interface này đang được gọi. Ứng dụng không nên cố gắng sử dụng locator vào bất kỳ thời điểm nào khác.


.. method:: ContentHandler.startDocument()

   Nhận thông báo về thời điểm bắt đầu một tài liệu.

   SAX parser sẽ chỉ gọi phương thức này một lần, trước bất kỳ phương thức nào khác trong interface này hoặc trong DTDHandler (ngoại trừ :meth:`setDocumentLocator`).


.. method:: ContentHandler.endDocument()

   Nhận thông báo khi tài liệu kết thúc.

   Trình phân tích SAX sẽ gọi phương thức này chỉ một lần và đây sẽ là phương thức cuối cùng được gọi trong quá trình phân tích. Trình phân tích sẽ không gọi phương thức này cho đến khi nó đã hủy bỏ việc phân tích (do gặp lỗi không thể khắc phục) hoặc đến cuối dữ liệu đầu vào.


.. method:: ContentHandler.startPrefixMapping(prefix, uri)

   Bắt đầu phạm vi của ánh xạ Namespace prefix-URI.

   Thông tin từ sự kiện này không cần thiết cho việc xử lý Namespace thông thường: trình đọc XML SAX sẽ tự động thay thế các prefix cho tên phần tử và thuộc tính khi tính năng ``feature_namespaces`` được bật (mặc định).

   Tuy nhiên, có những trường hợp ứng dụng cần sử dụng prefix trong dữ liệu ký tự hoặc trong giá trị thuộc tính, nơi chúng không thể được tự động mở rộng một cách an toàn; các sự kiện :meth:`startPrefixMapping` và :meth:`endPrefixMapping` cung cấp thông tin để ứng dụng tự mở rộng prefix trong những ngữ cảnh đó, nếu cần.

   .. XXX This is not really the default, is it? MvL

   Lưu ý rằng các sự kiện :meth:`startPrefixMapping` và :meth:`endPrefixMapping` không được đảm bảo là lồng đúng cách so với nhau: tất cả
   các sự kiện :meth:`startPrefixMapping` sẽ xảy ra trước sự kiện tương ứng
   sự kiện :meth:`startElement`, và tất cả các sự kiện :meth:`endPrefixMapping` sẽ xảy ra sau sự kiện :meth:`endElement` tương ứng, nhưng thứ tự của chúng không được đảm bảo.


.. method:: ContentHandler.endPrefixMapping(prefix)

   Kết thúc phạm vi của ánh xạ prefix-URI.

   Xem :meth:`startPrefixMapping` để biết chi tiết. Sự kiện này sẽ luôn xảy ra sau sự kiện :meth:`endElement` tương ứng, nhưng thứ tự của
   các sự kiện :meth:`endPrefixMapping` không được đảm bảo theo cách nào khác.


.. method:: ContentHandler.startElement(name, attrs)

   Báo hiệu bắt đầu một phần tử ở chế độ không có namespace.

   Tham số *name* chứa tên XML 1.0 thô của kiểu phần tử dưới dạng chuỗi, còn tham số *attrs* chứa một đối tượng của
   giao diện :ref:`Attributes <attributes-objects>` chứa các thuộc tính của phần tử. Đối tượng được truyền dưới dạng *attrs* có thể được parser tái sử dụng; việc giữ tham chiếu đến đối tượng này không phải là cách đáng tin cậy để lưu một bản sao của các thuộc tính. Để lưu một bản sao của các thuộc tính, hãy sử dụng phương thức :meth:`copy` của đối tượng *attrs*.


.. method:: ContentHandler.endElement(name)

   Báo hiệu kết thúc một phần tử ở chế độ không gian tên.

   Tham số *name* chứa tên của kiểu phần tử, giống như với
   :meth:`startElement` sự kiện.


.. method:: ContentHandler.startElementNS(name, qname, attrs)

   Báo hiệu bắt đầu một phần tử ở chế độ không gian tên.

   Tham số *name* chứa tên của kiểu phần tử dưới dạng một ``(uri, localname)`` tuple, tham số *qname* chứa tên XML 1.0 thô được sử dụng trong tài liệu nguồn, còn tham số *attrs* chứa một thể hiện của
   giao diện :ref:`AttributesNS <attributes-ns-objects>` chứa các thuộc tính của phần tử.  Nếu không gian tên nào được liên kết với phần tử, thành phần *uri* của *name* sẽ là ``None``. Đối tượng được truyền dưới dạng *attrs* có thể được parser tái sử dụng; việc giữ tham chiếu đến đối tượng này không phải là cách đáng tin cậy để giữ một bản sao của các thuộc tính.  Để giữ một bản sao của các thuộc tính, hãy sử dụng phương thức :meth:`copy` của đối tượng *attrs*.

   Các parser có thể đặt tham số *qname* thành ``None``, trừ khi ``feature_namespace_prefixes`` feature được kích hoạt.


.. method:: ContentHandler.endElementNS(name, qname)

   Báo hiệu kết thúc một phần tử trong chế độ namespace.

   Tham số *name* chứa tên của kiểu phần tử, giống như với
   phương thức :meth:`startElementNS`, tương tự như tham số *qname*.


.. method:: ContentHandler.characters(content)

   Nhận thông báo về dữ liệu ký tự.

   Parser sẽ gọi phương thức này để báo cáo từng phần dữ liệu ký tự. Các trình phân tích SAX có thể trả về toàn bộ dữ liệu ký tự liền kề trong một phần duy nhất hoặc chia dữ liệu thành nhiều phần; tuy nhiên, tất cả ký tự trong một sự kiện phải đến từ cùng một thực thể bên ngoài để Locator cung cấp thông tin hữu ích.

   *content* có thể là một string hoặc một instance bytes; mô-đun reader ``expat`` luôn tạo ra các string.

   .. note::

      Giao diện SAX 1 trước đây do Python XML Special Interest Group cung cấp sử dụng giao diện cho phương thức này gần với Java hơn. Vì hầu hết các parser được sử dụng từ Python không tận dụng giao diện cũ, chữ ký đơn giản hơn đã được chọn để thay thế nó. Để chuyển mã cũ sang giao diện mới, hãy sử dụng *content* thay vì cắt content bằng các tham số *offset* và *length* cũ.


.. method:: ContentHandler.ignorableWhitespace(whitespace)

   Nhận thông báo về khoảng trắng có thể bỏ qua trong nội dung phần tử.

   Các Parser có xác thực phải sử dụng phương thức này để báo cáo từng đoạn khoảng trắng có thể bỏ qua (xem khuyến nghị W3C XML 1.0, mục 2.10): các parser không xác thực cũng có thể sử dụng phương thức này nếu chúng có khả năng phân tích cú pháp và sử dụng các content model.

   Các parser SAX có thể trả về toàn bộ khoảng trắng liên tiếp trong một đoạn duy nhất hoặc chia thành nhiều đoạn; tuy nhiên, tất cả ký tự trong mỗi sự kiện phải xuất phát từ cùng một external entity để Locator cung cấp thông tin hữu ích.


.. method:: ContentHandler.processingInstruction(target, data)

   Nhận thông báo về một processing instruction.

   Parser sẽ gọi phương thức này một lần cho mỗi processing instruction được tìm thấy: lưu ý rằng processing instruction có thể xuất hiện trước hoặc sau phần tử tài liệu chính.

   Một parser SAX không bao giờ được báo cáo XML declaration (XML 1.0, mục 2.8) hoặc text declaration (XML 1.0, mục 4.3.1) bằng phương thức này.


.. method:: ContentHandler.skippedEntity(name)

   Nhận thông báo về một entity bị bỏ qua.

   Parser sẽ gọi phương thức này một lần cho mỗi entity bị bỏ qua. Các processor không kiểm tra tính hợp lệ có thể bỏ qua các entity nếu chưa thấy các khai báo (chẳng hạn vì entity được khai báo trong một external DTD subset). Tất cả processor đều có thể bỏ qua các external entity, tùy thuộc vào giá trị của thuộc tính ``feature_external_ges`` và ``feature_external_pes``.


.. _dtd-handler-objects:

Các đối tượng DTDHandler
------------------------

Các instance :class:`DTDHandler` cung cấp những phương thức sau:


.. method:: DTDHandler.notationDecl(name, publicId, systemId)

   Xử lý một sự kiện khai báo notation.


.. method:: DTDHandler.unparsedEntityDecl(name, publicId, systemId, ndata)

   Xử lý một sự kiện khai báo unparsed entity.


.. _entity-resolver-objects:

Các đối tượng EntityResolver
----------------------------


.. method:: EntityResolver.resolveEntity(publicId, systemId)

   Phân giải system identifier của một entity và trả về system identifier cần đọc dưới dạng chuỗi hoặc một InputSource để đọc. Cài đặt mặc định trả về *systemId*.


.. _sax-error-handler:

Đối tượng ErrorHandler
----------------------

Các đối tượng có interface này được dùng để tiếp nhận thông tin lỗi và cảnh báo từ :class:`~xml.sax.xmlreader.XMLReader`. Nếu bạn tạo một đối tượng triển khai interface này, sau đó đăng ký đối tượng với
:class:`~xml.sax.xmlreader.XMLReader`, parser sẽ gọi các phương thức trong đối tượng của bạn để báo cáo tất cả cảnh báo và lỗi. Có ba cấp độ lỗi: cảnh báo, lỗi (có thể) khôi phục được và lỗi không thể khôi phục. Tất cả các phương thức đều nhận một :exc:`~xml.sax.SAXParseException` làm tham số duy nhất. Lỗi và cảnh báo có thể được chuyển thành exception bằng cách raise đối tượng exception được truyền vào.


.. method:: ErrorHandler.error(exception)

   Được gọi khi parser gặp lỗi có thể khôi phục. Nếu phương thức này không raise exception, quá trình phân tích có thể tiếp tục, nhưng ứng dụng không nên kỳ vọng nhận thêm thông tin nào về tài liệu. Việc cho phép parser tiếp tục có thể giúp phát hiện thêm lỗi trong tài liệu đầu vào.


.. method:: ErrorHandler.fatalError(exception)

   Được gọi khi parser gặp một lỗi không thể khôi phục; quá trình phân tích dự kiến sẽ kết thúc khi phương thức này trả về.


.. method:: ErrorHandler.warning(exception)

   Được gọi khi parser cung cấp thông tin cảnh báo nhỏ cho ứng dụng. Quá trình phân tích dự kiến sẽ tiếp tục khi phương thức này trả về và thông tin về tài liệu sẽ tiếp tục được truyền đến ứng dụng. Việc raise exception trong phương thức này sẽ khiến quá trình phân tích kết thúc.


.. _lexical-handler-objects:

Đối tượng LexicalHandler
------------------------
Trình xử lý SAX2 tùy chọn cho các sự kiện lexical.

Trình xử lý này được dùng để nhận thông tin lexical về một tài liệu XML. Thông tin lexical bao gồm thông tin mô tả encoding của tài liệu và các chú thích XML được nhúng trong tài liệu, cũng như ranh giới phần của DTD và mọi phần CDATA. Các trình xử lý lexical được sử dụng theo cách tương tự như các trình xử lý nội dung.

Đặt LexicalHandler của XMLReader bằng cách sử dụng phương thức setProperty với mã định danh thuộc tính ``'http://xml.org/sax/properties/lexical-handler'``.


.. method:: LexicalHandler.comment(content)

   Báo cáo một chú thích ở bất kỳ vị trí nào trong tài liệu (bao gồm DTD và bên ngoài phần tử tài liệu).

.. method:: LexicalHandler.startDTD(name, public_id, system_id)

   Báo cáo phần bắt đầu của các khai báo DTD nếu tài liệu có DTD liên kết.

.. method:: LexicalHandler.endDTD()

   Báo cáo phần kết thúc của khai báo DTD.

.. method:: LexicalHandler.startCDATA()

   Báo cáo phần bắt đầu của một section được đánh dấu CDATA.

   Nội dung của phần được đánh dấu CDATA sẽ được truyền đến trình xử lý characters.

.. method:: LexicalHandler.endCDATA()

   Báo cáo phần kết thúc của một phần được đánh dấu CDATA.

.. _`external entity attacks`: https://en.wikipedia.org/wiki/XML_external_entity_attack
.. _`threat model`: https://en.wikipedia.org/wiki/Threat_model
