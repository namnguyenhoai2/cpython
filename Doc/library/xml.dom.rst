:mod:`!xml.dom` --- API Mô hình Đối tượng Tài liệu
==================================================

.. module:: xml.dom
   :synopsis: API Mô hình Đối tượng Tài liệu cho Python.

.. sectionauthor:: Paul Prescod <paul@prescod.net>
.. sectionauthor:: Martin v. Löwis <martin@v.loewis.de>

**Mã nguồn:** :source:`Lib/xml/dom/__init__.py`

--------------

Mô hình Đối tượng Tài liệu, hay "DOM", là một API đa ngôn ngữ do World Wide Web Consortium (W3C) cung cấp để truy cập và sửa đổi các tài liệu XML. Một triển khai DOM biểu diễn tài liệu XML dưới dạng cấu trúc cây, hoặc cho phép mã client xây dựng một cấu trúc như vậy từ đầu. Sau đó, nó cung cấp quyền truy cập vào cấu trúc thông qua một tập hợp các đối tượng có những giao diện được biết đến rộng rãi.

DOM cực kỳ hữu ích cho các ứng dụng cần truy cập ngẫu nhiên. SAX chỉ cho phép bạn xem từng phần của tài liệu tại một thời điểm. Nếu bạn đang xem một phần tử SAX, bạn không thể truy cập phần tử khác. Nếu bạn đang xem một nút văn bản, bạn không thể truy cập phần tử chứa nó. Khi viết một ứng dụng SAX, bạn cần tự theo dõi vị trí của chương trình trong tài liệu ở đâu đó trong mã của mình. SAX không làm việc đó thay bạn. Ngoài ra, nếu cần xem trước trong tài liệu XML, bạn hoàn toàn không thể thực hiện điều đó.

Một số ứng dụng đơn giản là không thể thực hiện trong mô hình hướng sự kiện nếu không có quyền truy cập vào một cây. Tất nhiên, bạn có thể tự xây dựng một dạng cây nào đó từ các sự kiện SAX, nhưng DOM cho phép bạn tránh phải viết mã đó. DOM là một biểu diễn cây tiêu chuẩn cho dữ liệu XML.

Mô hình Đối tượng Tài liệu đang được W3C định nghĩa theo từng giai đoạn, hay "level" theo thuật ngữ của họ. Phần ánh xạ API sang Python chủ yếu dựa trên khuyến nghị DOM Level 2.

Các ứng dụng DOM thường bắt đầu bằng cách phân tích một XML thành DOM. Cách thực hiện việc này hoàn toàn không được đề cập trong DOM Level 1, còn Level 2 chỉ cung cấp một số cải tiến hạn chế: Có một lớp đối tượng :class:`DOMImplementation` cung cấp quyền truy cập vào các phương thức tạo :class:`Document`, nhưng không có cách nào để truy cập XML reader/parser/Document builder theo cách độc lập với việc triển khai. Ngoài ra, cũng không có cách được định nghĩa rõ ràng để truy cập các phương thức này nếu không có sẵn một
đối tượng :class:`Document`. Trong Python, mỗi triển khai DOM sẽ cung cấp một hàm :func:`getDOMImplementation`. DOM Level 3 bổ sung đặc tả Load/Store, trong đó định nghĩa một giao diện cho reader, nhưng giao diện này hiện chưa có trong thư viện chuẩn Python.

Sau khi có đối tượng tài liệu DOM, bạn có thể truy cập các phần của tài liệu XML thông qua các thuộc tính và phương thức của đối tượng đó. Các thuộc tính này được định nghĩa trong đặc tả DOM; phần này của tài liệu tham khảo mô tả cách diễn giải đặc tả trong Python.

Đặc tả do W3C cung cấp định nghĩa API DOM cho Java, ECMAScript và OMG IDL. Phép ánh xạ sang Python được định nghĩa ở đây phần lớn dựa trên phiên bản IDL của đặc tả, nhưng không bắt buộc phải tuân thủ nghiêm ngặt (dù các triển khai được tự do hỗ trợ phép ánh xạ nghiêm ngặt từ IDL). Xem phần
:ref:`dom-conformance` để biết thảo luận chi tiết về các yêu cầu ánh xạ.


.. seealso::

   `Đặc tả Document Object Model (DOM) Level 2 <https://www.w3.org/TR/2000/REC-DOM-Level-2-Core-20001113/>`_
      Khuyến nghị của W3C làm nền tảng cho API DOM của Python.

   `Đặc tả Document Object Model (DOM) Cấp độ 1 <https://www.w3.org/TR/REC-DOM-Level-1/>`_
      Khuyến nghị của W3C về DOM được :mod:`xml.dom.minidom` hỗ trợ.

   `Đặc tả ánh xạ ngôn ngữ Python <https://www.omg.org/spec/PYTH/1.2/PDF>`_
      Tài liệu này quy định ánh xạ từ OMG IDL sang Python.


Nội dung mô-đun
---------------

:mod:`!xml.dom` chứa các hàm sau:


.. function:: registerDOMImplementation(name, factory)

   Đăng ký hàm *factory* với tên *name*. Hàm factory phải trả về một đối tượng triển khai giao diện :class:`DOMImplementation`. Hàm factory có thể trả về cùng một đối tượng trong mọi lần gọi hoặc một đối tượng mới cho mỗi lần gọi, tùy theo yêu cầu của triển khai cụ thể (ví dụ: nếu triển khai đó hỗ trợ một số tùy chỉnh).


.. function:: getDOMImplementation(name=None, features=())

   Trả về một triển khai DOM phù hợp. *name* có thể là tên đã biết, tên mô-đun của một triển khai DOM hoặc ``None``. Nếu không phải ``None``, hàm sẽ import mô-đun tương ứng và trả về một đối tượng :class:`DOMImplementation` nếu import thành công. Nếu không cung cấp tên và biến môi trường
   :envvar:`!PYTHON_DOM` được thiết lập, biến này sẽ được dùng để tìm triển khai. Tên duy nhất đã biết trong standard library là ``'minidom'``, dành cho :mod:`xml.dom.minidom`.

   Nếu không cung cấp name, hàm này sẽ kiểm tra các triển khai hiện có để tìm một triển khai có tập tính năng bắt buộc. Nếu không tìm thấy triển khai nào, hãy raise một
   :exc:`ImportError`. Danh sách tính năng phải là một dãy các cặp ``(feature, version)``, được truyền vào phương thức :meth:`~DOMImplementation.hasFeature` trên các đối tượng :class:`DOMImplementation` hiện có.

Một số hằng số tiện ích cũng được cung cấp:


.. data:: EMPTY_NAMESPACE

   Giá trị dùng để biểu thị rằng không có namespace nào được liên kết với một node trong DOM. Giá trị này thường được tìm thấy dưới dạng :attr:`~Node.namespaceURI` của một node hoặc được dùng làm tham số *namespaceURI* cho một phương thức dành riêng cho namespace.


.. data:: XML_NAMESPACE

   URI namespace được liên kết với tiền tố dành riêng ``xml``, như được định nghĩa trong `Namespaces in XML <https://www.w3.org/TR/REC-xml-names/>`_ (mục 4).


.. data:: XMLNS_NAMESPACE

   URI không gian tên dùng cho các khai báo không gian tên, như được định nghĩa trong `Đặc tả DOM (Document Object Model) Level 2 Core <https://www.w3.org/TR/DOM-Level-2-Core/core.html>`_ (mục 1.1.8).


.. data:: XHTML_NAMESPACE

   URI của không gian tên XHTML như được định nghĩa trong `XHTML 1.0: Ngôn ngữ đánh dấu siêu văn bản mở rộng <https://www.w3.org/TR/xhtml1/>`_ (mục 3.1.1).


Ngoài ra, :mod:`!xml.dom` còn chứa một lớp :class:`Node` cơ sở và các lớp ngoại lệ DOM. Lớp :class:`Node` do mô-đun này cung cấp không triển khai bất kỳ phương thức hoặc thuộc tính nào được định nghĩa bởi đặc tả DOM; các triển khai DOM cụ thể phải cung cấp những thành phần đó. Lớp :class:`Node` được cung cấp trong mô-đun này cũng cung cấp các hằng số được dùng cho
thuộc tính :attr:`~Node.nodeType` trên các đối tượng :class:`Node` cụ thể; chúng nằm trong lớp thay vì ở cấp mô-đun để phù hợp với các đặc tả DOM.

.. Should the Node documentation go here?


.. _dom-objects:

Các đối tượng trong DOM
-----------------------

Tài liệu chính thức và đầy đủ về DOM là đặc tả DOM của W3C.

Các tên được ghi lại trong phần này là các giao diện DOM. Ngoại trừ :class:`Node` và các lớp ngoại lệ, chúng không được cung cấp bởi chính mô-đun :mod:`!xml.dom`, mà bởi các triển khai DOM cụ thể, chẳng hạn như :mod:`xml.dom.minidom`.

Lưu ý rằng các thuộc tính DOM cũng có thể được thao tác dưới dạng các node thay vì các chuỗi đơn giản. Tuy nhiên, trường hợp này khá hiếm, vì vậy cách sử dụng này hiện chưa được ghi lại.

+--------------------------------+-----------------------------------+------------------------------------------------------------+
| Giao diện                      | Phần                              | Mục đích                                                   |
+================================+===================================+============================================================+
| :class:`DOMImplementation`     | :ref:`dom-implementation-objects` | Giao diện với phần triển khai bên dưới.                    |
+--------------------------------+-----------------------------------+------------------------------------------------------------+
| :class:`Node`                  | :ref:`dom-node-objects`           | Giao diện cơ sở cho hầu hết các đối tượng trong tài liệu.  |
+--------------------------------+-----------------------------------+------------------------------------------------------------+
| :class:`NodeList`              | :ref:`dom-nodelist-objects`       | Giao diện cho một chuỗi các node.                          |
+--------------------------------+-----------------------------------+------------------------------------------------------------+
| :class:`DocumentType`          | :ref:`dom-documenttype-objects`   | Thông tin về các khai báo cần thiết để xử lý một tài liệu. |
+--------------------------------+-----------------------------------+------------------------------------------------------------+
| :class:`Document`              | :ref:`dom-document-objects`       | Đối tượng đại diện cho toàn bộ tài liệu.                   |
+--------------------------------+-----------------------------------+------------------------------------------------------------+
| :class:`Element`               | :ref:`dom-element-objects`        | Các nút phần tử trong hệ thống phân cấp của tài liệu.      |
+--------------------------------+-----------------------------------+------------------------------------------------------------+
| :class:`Attr`                  | :ref:`dom-attr-objects`           | Các nút giá trị thuộc tính trên các nút phần tử.           |
+--------------------------------+-----------------------------------+------------------------------------------------------------+
| :class:`Comment`               | :ref:`dom-comment-objects`        | Biểu diễn các chú thích trong tài liệu nguồn.              |
+--------------------------------+-----------------------------------+------------------------------------------------------------+
| :class:`Text`                  | :ref:`dom-text-objects`           | Các nút chứa nội dung văn bản từ tài liệu.                 |
+--------------------------------+-----------------------------------+------------------------------------------------------------+
| :class:`ProcessingInstruction` | :ref:`dom-pi-objects`             | Biểu diễn chỉ thị xử lý.                                   |
+--------------------------------+-----------------------------------+------------------------------------------------------------+

Một phần bổ sung mô tả các ngoại lệ được định nghĩa khi làm việc với DOM trong Python.


.. _dom-implementation-objects:

Các đối tượng DOMImplementation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: DOMImplementation
   :no-typesetting:

Giao diện :class:`DOMImplementation` cung cấp một cách để các ứng dụng xác định tính khả dụng của các tính năng cụ thể trong DOM mà chúng đang sử dụng. DOM Level 2 bổ sung khả năng tạo :class:`Document` mới và
các đối tượng :class:`DocumentType` cũng sử dụng :class:`DOMImplementation`.


.. method:: DOMImplementation.hasFeature(feature, version)

   Trả về ``True`` nếu tính năng được xác định bởi cặp chuỗi *feature* và *version* đã được triển khai.


.. method:: DOMImplementation.createDocument(namespaceUri, qualifiedName, doctype)

   Trả về một đối tượng :class:`Document` mới (gốc của DOM), có một đối tượng con
   :class:`Element` với *namespaceUri* và *qualifiedName* đã cho. *doctype* phải là một đối tượng :class:`DocumentType` được tạo bởi
   :meth:`createDocumentType`, hoặc ``None``. Trong Python DOM API, hai đối số đầu tiên cũng có thể là ``None`` để cho biết rằng không tạo :class:`Element` nào.


.. method:: DOMImplementation.createDocumentType(qualifiedName, publicId, systemId)

   Trả về một đối tượng :class:`DocumentType` mới đóng gói các chuỗi *qualifiedName*, *publicId* và *systemId* đã cho, biểu thị thông tin có trong khai báo kiểu tài liệu XML.


.. _dom-node-objects:

Đối tượng Node
^^^^^^^^^^^^^^

.. class:: Node
   :no-typesetting:

Tất cả các thành phần của một tài liệu XML đều là các lớp con của :class:`Node`.

Chỉ các node thuộc những kiểu sau đây mới có thể có node con, và node con chỉ có thể thuộc những kiểu được liệt kê:

:class:`Document`
   nhiều nhất một :class:`Element`, nhiều nhất một :class:`DocumentType`,
   :class:`ProcessingInstruction` và :class:`Comment`

:class:`DocumentFragment` và :class:`Element`
   :class:`Element`, :class:`Text`, :class:`CDATASection`,
   :class:`ProcessingInstruction` và :class:`Comment`

:class:`Attr`
   :class:`Text`

Các node thuộc những kiểu khác không thể có node con. Việc chèn một node con thuộc kiểu không được phép sẽ gây ra :exc:`HierarchyRequestErr`.


.. attribute:: Node.nodeType

   Một số nguyên biểu thị kiểu của node. Các hằng số ký hiệu cho các kiểu nằm trên đối tượng :class:`Node`. Đây là thuộc tính chỉ đọc.


.. data:: Node.ELEMENT_NODE
          Node.ATTRIBUTE_NODE Node.TEXT_NODE Node.CDATA_SECTION_NODE Node.ENTITY_REFERENCE_NODE Node.ENTITY_NODE Node.PROCESSING_INSTRUCTION_NODE Node.COMMENT_NODE Node.DOCUMENT_NODE Node.DOCUMENT_TYPE_NODE Node.DOCUMENT_FRAGMENT_NODE Node.NOTATION_NODE

   Các hằng số nguyên cho những giá trị có thể có của thuộc tính :attr:`~Node.nodeType`.


.. attribute:: Node.parentNode

   Node cha của node hiện tại hoặc ``None`` đối với node tài liệu. Giá trị luôn là đối tượng :class:`Node` hoặc ``None``. Đối với các node :class:`Element`, đây sẽ là phần tử cha, ngoại trừ phần tử gốc; trong trường hợp đó, đây sẽ là đối tượng :class:`Document`. Đối với các node :class:`Attr`, giá trị này luôn là ``None``. Đây là thuộc tính chỉ đọc.


.. attribute:: Node.attributes

   Một :class:`NamedNodeMap` các đối tượng thuộc tính. Chỉ các element mới có giá trị thực cho thuộc tính này; các đối tượng khác cung cấp ``None`` cho thuộc tính này. Đây là thuộc tính chỉ đọc.


.. attribute:: Node.previousSibling

   Node ngay trước node này và có cùng parent. Ví dụ: element có end-tag nằm ngay trước start-tag của element *self*. Dĩ nhiên, tài liệu XML không chỉ gồm các element, vì vậy sibling trước đó có thể là văn bản, comment hoặc một thành phần khác. Nếu node này là child đầu tiên của parent, thuộc tính này sẽ là ``None``. Đây là thuộc tính chỉ đọc.


.. attribute:: Node.nextSibling

   Node ngay sau node này và có cùng parent. Xem thêm
   :attr:`previousSibling`. Nếu đây là child cuối cùng của parent, thuộc tính này sẽ là ``None``. Đây là thuộc tính chỉ đọc.


.. attribute:: Node.childNodes

   Một :class:`NodeList` các child của node này. Nếu node không có child, danh sách sẽ trống. Đây là thuộc tính chỉ đọc.


.. attribute:: Node.firstChild

   Child đầu tiên của node, nếu có, hoặc ``None``. Đây là thuộc tính chỉ đọc.


.. attribute:: Node.lastChild

   Child cuối cùng của node, nếu có, hoặc ``None``. Đây là thuộc tính chỉ đọc.


.. attribute:: Node.localName

   Phần của :attr:`~Element.tagName` nằm sau dấu hai chấm nếu có, nếu không thì là toàn bộ :attr:`~Element.tagName`. Giá trị là một chuỗi.


.. attribute:: Node.prefix

   Phần của :attr:`~Element.tagName` nằm trước dấu hai chấm nếu có, nếu không thì là chuỗi rỗng. Giá trị là một chuỗi hoặc ``None``.


.. attribute:: Node.namespaceURI

   Không gian tên liên kết với tên phần tử. Đây sẽ là một chuỗi hoặc ``None``. Đây là thuộc tính chỉ đọc.


.. attribute:: Node.ownerDocument

   Đối tượng :class:`Document` mà node này thuộc về, hoặc ``None`` nếu bản thân nó là một tài liệu. Đây là thuộc tính chỉ đọc.


.. method:: Node.isSupported(feature, version)

   Trả về liệu cài đặt DOM có hỗ trợ *feature* cụ thể hay không, như :meth:`DOMImplementation.hasFeature` thực hiện.


.. method:: Node.setUserData(key, data, handler)

   Liên kết *data* với *key* trên node này và trả về dữ liệu trước đó được liên kết với *key*, hoặc ``None``. Nếu *data* là ``None``, liên kết sẽ bị xóa. *handler* được gọi khi node được sao chép, nhập, đổi tên hoặc xóa; truyền ``None`` nếu không cần thông báo.


.. method:: Node.getUserData(key)

   Trả về dữ liệu được liên kết với *key* trên node này bằng :meth:`~Node.setUserData`, hoặc ``None``.


.. attribute:: Node.nodeName

   Tên của node này, tùy thuộc vào kiểu của nó; xem bảng bên dưới. Bạn luôn có thể lấy thông tin mà bạn nhận được ở đây từ một thuộc tính khác, chẳng hạn như thuộc tính :attr:`~Element.tagName` dành cho các phần tử hoặc
   :attr:`~Attr.name` dành cho các thuộc tính. Đây là thuộc tính chỉ đọc.


.. attribute:: Node.nodeValue

   Giá trị của node này, tùy thuộc vào kiểu của nó; xem bảng bên dưới. Giá trị là một chuỗi hoặc ``None``.


Các giá trị của :attr:`~Node.nodeName` và :attr:`~Node.nodeValue` đối với từng kiểu node là:

+--------------------------------+---------------------------------------+-------------------------------------+
| Kiểu node                      | nodeName                              | nodeValue                           |
+================================+=======================================+=====================================+
| :class:`Attr`                  | :attr:`~Attr.name`                    | :attr:`~Attr.value`                 |
+--------------------------------+---------------------------------------+-------------------------------------+
| :class:`CDATASection`          | ``'#cdata-section'``                  | nội dung                            |
+--------------------------------+---------------------------------------+-------------------------------------+
| :class:`Comment`               | ``'#comment'``                        | nội dung                            |
+--------------------------------+---------------------------------------+-------------------------------------+
| :class:`Document`              | ``'#document'``                       | ``None``                            |
+--------------------------------+---------------------------------------+-------------------------------------+
| :class:`DocumentFragment`      | ``'#document-fragment'``              | ``None``                            |
+--------------------------------+---------------------------------------+-------------------------------------+
| :class:`DocumentType`          | :attr:`~DocumentType.name`            | ``None``                            |
+--------------------------------+---------------------------------------+-------------------------------------+
| :class:`Element`               | :attr:`~Element.tagName`              | ``None``                            |
+--------------------------------+---------------------------------------+-------------------------------------+
| :class:`Entity`                | tên của thực thể                      | ``None``                            |
+--------------------------------+---------------------------------------+-------------------------------------+
| :class:`Notation`              | tên của ký hiệu                       | ``None``                            |
+--------------------------------+---------------------------------------+-------------------------------------+
| :class:`ProcessingInstruction` | :attr:`~ProcessingInstruction.target` | :attr:`~ProcessingInstruction.data` |
+--------------------------------+---------------------------------------+-------------------------------------+
| :class:`Text`                  | ``'#text'``                           | nội dung                            |
+--------------------------------+---------------------------------------+-------------------------------------+

.. method:: Node.hasAttributes()

   Trả về ``True`` nếu nút có bất kỳ thuộc tính nào.


.. method:: Node.hasChildNodes()

   Trả về ``True`` nếu nút có bất kỳ nút con nào.


.. method:: Node.isSameNode(other)

   Trả về ``True`` nếu *other* tham chiếu đến cùng node với node này. Điều này đặc biệt hữu ích cho các triển khai DOM sử dụng bất kỳ dạng kiến trúc proxy nào (vì nhiều object có thể tham chiếu đến cùng một node).

   .. note::

      Điều này dựa trên một DOM Level 3 API được đề xuất, hiện vẫn đang ở giai đoạn "working draft", nhưng interface cụ thể này dường như không gây tranh cãi. Các thay đổi từ W3C không nhất thiết ảnh hưởng đến method này trong Python DOM interface (mặc dù mọi W3C API mới cho mục đích này cũng sẽ được hỗ trợ).


.. method:: Node.appendChild(newChild)

   Thêm một child node mới vào node này ở cuối danh sách các node con, trả về *newChild*. Nếu node này đã nằm trong cây, trước tiên nó sẽ được xóa khỏi cây.


.. method:: Node.insertBefore(newChild, refChild)

   Chèn một child node mới trước một child node hiện có. *refChild* phải là một child của node này; nếu không, :exc:`NotFoundErr` sẽ được raise. *newChild* được trả về. Nếu *refChild* là ``None``, *newChild* sẽ được chèn vào cuối danh sách các child.


.. method:: Node.removeChild(oldChild)

   Xóa một child node. *oldChild* phải là một child của node này; nếu không,
   :exc:`NotFoundErr` sẽ được raise. Khi thành công, *oldChild* được trả về. Nếu *oldChild* không còn được sử dụng, nên gọi method :meth:`~xml.dom.minidom.Node.unlink` của nó.


.. method:: Node.replaceChild(newChild, oldChild)

   Thay thế một node hiện có bằng một node mới. *oldChild* phải là một child của node này; nếu không, :exc:`NotFoundErr` sẽ được raise.


.. method:: Node.normalize()

   Gộp các nút văn bản liền kề để mọi đoạn văn bản được lưu dưới dạng một
   :class:`Text` duy nhất. Điều này giúp đơn giản hóa việc xử lý văn bản từ cây DOM cho nhiều ứng dụng.


.. method:: Node.cloneNode(deep)

   Sao chép nút này. Đặt *deep* có nghĩa là cũng sao chép tất cả các nút con. Thao tác này trả về bản sao.


.. _dom-nodelist-objects:

Đối tượng NodeList
^^^^^^^^^^^^^^^^^^

.. class:: NodeList
   :no-typesetting:

Một :class:`NodeList` biểu diễn một chuỗi các nút. Các đối tượng này được sử dụng theo hai cách trong khuyến nghị DOM Core: một đối tượng :class:`Element` cung cấp một đối tượng như danh sách các nút con của nó, còn các phương thức :meth:`~Element.getElementsByTagName` và :meth:`~Element.getElementsByTagNameNS` của :class:`Node` trả về các đối tượng có giao diện này để biểu diễn kết quả truy vấn.

:class:`NodeList` *không* kế thừa từ :class:`Node`.

Khuyến nghị DOM Level 2 định nghĩa một phương thức và một thuộc tính cho các đối tượng này:


.. method:: NodeList.item(i)

   Trả về phần tử thứ *i* trong dãy, hoặc ``None`` nếu *i* nằm ngoài phạm vi. Không hỗ trợ chỉ mục âm.


.. attribute:: NodeList.length

   Số lượng node trong dãy.

Ngoài ra, giao diện DOM của Python yêu cầu cung cấp một số hỗ trợ bổ sung để cho phép các đối tượng :class:`NodeList` được sử dụng như các dãy Python. Tất cả
Các triển khai :class:`NodeList` phải hỗ trợ
:meth:`~object.__len__` và
:meth:`~object.__getitem__`; điều này cho phép lặp qua :class:`NodeList` trong
các câu lệnh :keyword:`for` và hỗ trợ chính xác cho hàm dựng sẵn :func:`len`.

Nếu một triển khai DOM hỗ trợ sửa đổi tài liệu thì triển khai
:class:`NodeList` cũng phải hỗ trợ
các phương thức :meth:`~object.__setitem__` và :meth:`~object.__delitem__`.


.. _dom-documenttype-objects:

Đối tượng DocumentType
^^^^^^^^^^^^^^^^^^^^^^

.. class:: DocumentType
   :no-typesetting:

Thông tin về các notation và entity được khai báo bởi một tài liệu (bao gồm cả external subset nếu parser sử dụng nó và có thể cung cấp thông tin này) có sẵn từ một đối tượng :class:`DocumentType`. :class:`DocumentType` của một tài liệu có sẵn từ thuộc tính :attr:`~Document.doctype` của đối tượng :class:`Document`; nếu tài liệu không có khai báo ``DOCTYPE``, thuộc tính :attr:`~Document.doctype` của tài liệu sẽ được đặt thành ``None`` thay vì một instance của interface này.

:class:`DocumentType` là một specialization của :class:`Node` và bổ sung các thuộc tính sau:


.. attribute:: DocumentType.publicId

   Định danh public cho external subset của định nghĩa kiểu tài liệu, hoặc ``None`` nếu khai báo ``DOCTYPE`` không chỉ định định danh đó.


.. attribute:: DocumentType.systemId

   Mã định danh hệ thống, một URI, cho tập con bên ngoài của định nghĩa kiểu tài liệu, hoặc ``None`` nếu khai báo ``DOCTYPE`` không chỉ định mã này.


.. attribute:: DocumentType.internalSubset

   Một chuỗi cung cấp đầy đủ tập con bên trong của tài liệu. Chuỗi này không bao gồm các dấu ngoặc bao quanh tập con. Nếu tài liệu không có tập con bên trong, giá trị này phải là ``None``.


.. attribute:: DocumentType.name

   Tên của phần tử gốc như được chỉ định trong khai báo ``DOCTYPE``, nếu có.


.. attribute:: DocumentType.entities

   Đây là một :class:`NamedNodeMap` gồm các nút :class:`Entity` cung cấp định nghĩa của các thực thể bên ngoài. Đối với những tên thực thể được định nghĩa nhiều lần, chỉ cung cấp định nghĩa đầu tiên (các định nghĩa khác bị bỏ qua theo yêu cầu của khuyến nghị XML). Giá trị này có thể là ``None`` nếu trình phân tích cú pháp không cung cấp thông tin hoặc nếu không có thực thể nào được định nghĩa.


.. attribute:: DocumentType.notations

   Đây là một :class:`NamedNodeMap` gồm các nút :class:`Notation` cung cấp định nghĩa của các ký hiệu. Đối với những tên ký hiệu được định nghĩa nhiều lần, chỉ cung cấp định nghĩa đầu tiên (các định nghĩa khác bị bỏ qua theo yêu cầu của khuyến nghị XML). Giá trị này có thể là ``None`` nếu trình phân tích cú pháp không cung cấp thông tin hoặc nếu không có ký hiệu nào được định nghĩa.


.. _dom-document-objects:

Đối tượng Document
^^^^^^^^^^^^^^^^^^

.. class:: Document
   :no-typesetting:

Một :class:`Document` đại diện cho toàn bộ tài liệu XML, bao gồm các phần tử, thuộc tính, chỉ thị xử lý, chú thích cấu thành tài liệu, v.v. Hãy nhớ rằng nó kế thừa các thuộc tính từ :class:`Node`.


.. attribute:: Document.documentElement

   Phần tử gốc duy nhất của tài liệu.


.. attribute:: Document.doctype

   Nút :class:`DocumentType` của tài liệu hoặc ``None``. Đây là thuộc tính chỉ đọc.


.. attribute:: Document.implementation

   Đối tượng :class:`DOMImplementation` đã tạo tài liệu này. Đây là thuộc tính chỉ đọc.


.. attribute:: Document.strictErrorChecking

   Có bắt buộc kiểm tra lỗi hay không.


.. attribute:: Document.documentURI

   Vị trí của tài liệu hoặc ``None`` nếu không xác định được.


.. method:: Document.createDocumentFragment()

   Tạo và trả về một nút :class:`DocumentFragment` trống.


.. method:: Document.createCDATASection(data)

   Tạo và trả về một nút :class:`CDATASection` chứa *data*.


.. method:: Document.importNode(importedNode, deep)

   Trả về một bản sao của *importedNode* thuộc về tài liệu này. Node ban đầu không bị xóa khỏi tài liệu của nó. Nếu *deep* là true, các node con của node đó cũng được sao chép.


.. method:: Document.createElement(tagName)

   Tạo và trả về một element node mới. Element này không được chèn vào tài liệu khi được tạo. Bạn cần chèn rõ ràng bằng một trong các phương thức khác, chẳng hạn như :meth:`~Node.insertBefore` hoặc :meth:`~Node.appendChild`.


.. method:: Document.createElementNS(namespaceURI, tagName)

   Tạo và trả về một element mới có namespace. *tagName* có thể có một prefix. Element này không được chèn vào tài liệu khi được tạo. Bạn cần chèn rõ ràng bằng một trong các phương thức khác, chẳng hạn như
   :meth:`~Node.insertBefore` hoặc :meth:`~Node.appendChild`.


.. method:: Document.createTextNode(data)

   Tạo và trả về một text node chứa dữ liệu được truyền dưới dạng tham số. Cũng như các phương thức tạo khác, phương thức này không chèn node vào cây.


.. method:: Document.createComment(data)

   Tạo và trả về một comment node chứa dữ liệu được truyền dưới dạng tham số. Cũng như các phương thức tạo khác, phương thức này không chèn node vào cây.


.. method:: Document.createProcessingInstruction(target, data)

   Tạo và trả về một processing instruction node chứa *target* và *data* được truyền dưới dạng tham số. Cũng như các phương thức tạo khác, phương thức này không chèn node vào cây.


.. method:: Document.createAttribute(name)

   Tạo và trả về một nút thuộc tính. Phương thức này không liên kết nút thuộc tính với bất kỳ phần tử cụ thể nào. Bạn phải sử dụng
   :meth:`~Element.setAttributeNode` trên đối tượng :class:`Element` thích hợp để sử dụng thực thể thuộc tính vừa tạo.


.. method:: Document.createAttributeNS(namespaceURI, qualifiedName)

   Tạo và trả về một nút thuộc tính có namespace. *tagName* có thể có tiền tố. Phương thức này không liên kết nút thuộc tính với bất kỳ phần tử cụ thể nào. Bạn phải sử dụng :meth:`~Element.setAttributeNode` trên đối tượng thích hợp
   :class:`Element` để sử dụng thực thể thuộc tính vừa tạo.


.. method:: Document.getElementById(id)

   Trả về phần tử có ID đã cho hoặc ``None``. Chỉ các thuộc tính được khai báo có kiểu ID trong DTD hoặc bởi :meth:`Element.setIdAttribute` mới được tìm kiếm.


.. method:: Document.getElementsByTagName(tagName)

   Tìm kiếm tất cả các hậu duệ (con trực tiếp, con của các con, v.v.) có tên kiểu phần tử cụ thể.


.. method:: Document.getElementsByTagNameNS(namespaceURI, localName)

   Tìm kiếm tất cả các hậu duệ (con trực tiếp, con của các con, v.v.) có URI namespace và localname cụ thể. localname là phần namespace nằm sau tiền tố.


.. method:: Document.renameNode(n, namespaceURI, name)

   Đổi tên nút phần tử hoặc thuộc tính *n* rồi trả về nút đó. *namespaceURI* là URI không gian tên mới, hoặc
   :data:`~xml.dom.EMPTY_NAMESPACE` nếu nút không thuộc không gian tên nào. *name* là tên đủ điều kiện mới.

   Phát sinh :exc:`WrongDocumentErr` nếu *n* được tạo bởi một tài liệu khác, và :exc:`NotSupportedErr` nếu nó không phải là phần tử cũng không phải là thuộc tính.


.. _dom-element-objects:

Đối tượng phần tử
^^^^^^^^^^^^^^^^^

.. class:: Element
   :no-typesetting:

:class:`Element` là một lớp con của :class:`Node`, vì vậy kế thừa tất cả các thuộc tính của lớp đó.


.. attribute:: Element.tagName

   Tên kiểu của phần tử. Trong một tài liệu sử dụng không gian tên, tên này có thể chứa dấu hai chấm. Giá trị là một chuỗi.


.. method:: Element.setIdAttribute(name)

   Khai báo rằng thuộc tính *name* có kiểu ID, để phần tử được tìm thấy bằng :meth:`Document.getElementById`. Phát sinh :exc:`NotFoundErr` nếu phần tử không có thuộc tính như vậy.


.. method:: Element.setIdAttributeNS(namespaceURI, localName)

   Giống như :meth:`~Element.setIdAttribute`, nhưng áp dụng cho một thuộc tính được chỉ định bằng URI không gian tên và tên cục bộ của thuộc tính đó.


.. method:: Element.setIdAttributeNode(idAttr)

   Giống như :meth:`~Element.setIdAttribute`, nhưng áp dụng cho một nút thuộc tính đã được lấy.


.. method:: Element.getElementsByTagName(tagName)

   Giống như phương thức tương đương trong lớp :class:`Document`.


.. method:: Element.getElementsByTagNameNS(namespaceURI, localName)

   Giống như phương thức tương đương trong lớp :class:`Document`.


.. method:: Element.hasAttribute(name)

   Trả về ``True`` nếu phần tử có một thuộc tính được đặt tên bởi *name*.


.. method:: Element.hasAttributeNS(namespaceURI, localName)

   Trả về ``True`` nếu phần tử có một thuộc tính được đặt tên bởi *namespaceURI* và *localName*.


.. method:: Element.getAttribute(name)

   Trả về giá trị của thuộc tính được đặt tên bởi *name* dưới dạng chuỗi. Nếu không tồn tại thuộc tính như vậy, một chuỗi rỗng sẽ được trả về, như thể thuộc tính đó không có giá trị.


.. method:: Element.getAttributeNode(attrname)

   Trả về nút :class:`Attr` cho thuộc tính có tên được chỉ định bởi *attrname*.


.. method:: Element.getAttributeNS(namespaceURI, localName)

   Trả về giá trị của thuộc tính có tên được chỉ định bởi *namespaceURI* và *localName* dưới dạng chuỗi. Nếu không có thuộc tính như vậy, một chuỗi rỗng được trả về, như thể thuộc tính đó không có giá trị.


.. method:: Element.getAttributeNodeNS(namespaceURI, localName)

   Trả về giá trị thuộc tính dưới dạng nút, với *namespaceURI* và *localName*.


.. method:: Element.removeAttribute(name)

   Xóa một thuộc tính theo tên.


.. method:: Element.removeAttributeNode(oldAttr)

   Xóa và trả về *oldAttr* khỏi danh sách thuộc tính, nếu có. Nếu *oldAttr* không có, :exc:`NotFoundErr` sẽ được phát sinh.


.. method:: Element.removeAttributeNS(namespaceURI, localName)

   Xóa một thuộc tính theo tên. Lưu ý rằng thao tác này sử dụng localName, không phải qname.


.. method:: Element.setAttribute(name, value)

   Đặt giá trị thuộc tính từ một chuỗi.


.. method:: Element.setAttributeNode(newAttr)

   Thêm một nút thuộc tính mới vào element, thay thế một thuộc tính hiện có nếu cần nếu thuộc tính :attr:`~Attr.name` khớp. Nếu xảy ra việc thay thế, nút thuộc tính cũ sẽ được trả về. Nếu *newAttr* đã được sử dụng,
   :exc:`InuseAttributeErr` sẽ được ném ra.


.. method:: Element.setAttributeNodeNS(newAttr)

   Thêm một nút thuộc tính mới vào element, thay thế một thuộc tính hiện có nếu cần nếu các thuộc tính :attr:`~Node.namespaceURI` và :attr:`~Attr.localName` khớp. Nếu xảy ra việc thay thế, nút thuộc tính cũ sẽ được trả về. Nếu *newAttr* đã được sử dụng, :exc:`InuseAttributeErr` sẽ được ném ra.


.. method:: Element.setAttributeNS(namespaceURI, qname, value)

   Đặt giá trị thuộc tính từ một chuỗi, với *namespaceURI* và *qname*. Lưu ý rằng qname là toàn bộ tên thuộc tính. Điều này khác với phần trên.


.. _dom-attr-objects:

Đối tượng Attr
^^^^^^^^^^^^^^

.. class:: Attr
   :no-typesetting:

:class:`Attr` kế thừa từ :class:`Node`, vì vậy kế thừa tất cả các thuộc tính của nó.

Các nút thuộc tính không thuộc cây tài liệu. Chúng được chứa trong map :attr:`~Node.attributes` của một element, không phải trong các children của nó, và :attr:`~Node.parentNode`, :attr:`~Node.previousSibling` và :attr:`~Node.nextSibling` của chúng luôn là ``None``.


.. attribute:: Attr.name

   Tên thuộc tính. Trong tài liệu sử dụng namespace, tên này có thể bao gồm dấu hai chấm.


.. attribute:: Attr.localName

   Phần tên nằm sau dấu hai chấm nếu có, nếu không thì là toàn bộ tên. Đây là thuộc tính chỉ đọc.


.. attribute:: Attr.prefix

   Phần tên nằm trước dấu hai chấm nếu có, nếu không thì là chuỗi rỗng.


.. attribute:: Attr.isId

   Cho biết thuộc tính này có kiểu ID hay không, do được khai báo như vậy trong DTD hoặc do :meth:`Element.setIdAttribute` được sử dụng. Đây là thuộc tính chỉ đọc.


.. attribute:: Attr.ownerElement

   Nút :class:`Element` mà thuộc tính này thuộc về, hoặc ``None`` nếu thuộc tính này không được sử dụng. Đây là thuộc tính chỉ đọc.


.. attribute:: Attr.specified

   Cho biết giá trị của thuộc tính có được thiết lập rõ ràng trong tài liệu hay không, thay vì được lấy giá trị mặc định từ DTD. Đây là thuộc tính chỉ đọc.


.. attribute:: Attr.value

   Giá trị văn bản của thuộc tính. Đây là từ đồng nghĩa với
   thuộc tính :attr:`~Node.nodeValue`.


.. _dom-attributelist-objects:

Đối tượng NamedNodeMap
^^^^^^^^^^^^^^^^^^^^^^

.. class:: NamedNodeMap
   :no-typesetting:

:class:`NamedNodeMap` *không* kế thừa từ :class:`Node`.


.. attribute:: NamedNodeMap.length

   Độ dài của danh sách thuộc tính.


.. method:: NamedNodeMap.item(index)

   Trả về một thuộc tính tại một chỉ mục cụ thể. Thứ tự nhận được các thuộc tính là tùy ý nhưng sẽ nhất quán trong suốt vòng đời của một DOM. Mỗi mục là một nút thuộc tính. Lấy giá trị của nó bằng thuộc tính :attr:`~Attr.value`.


.. method:: NamedNodeMap.getNamedItem(name)

   Trả về nút có :attr:`~Attr.name` đã cho hoặc ``None`` nếu không có nút như vậy.


.. method:: NamedNodeMap.getNamedItemNS(namespaceURI, localName)

   Trả về nút có URI namespace và tên cục bộ đã cho hoặc ``None`` nếu không có nút như vậy.


.. method:: NamedNodeMap.setNamedItem(node)

   Thêm *node* vào map, sử dụng :attr:`~Attr.name` của nó làm khóa. Trả về node mà nó thay thế, hoặc ``None`` nếu nó không thay thế node nào.


.. method:: NamedNodeMap.setNamedItemNS(node)

   Thêm *node* vào map, sử dụng URI namespace và tên cục bộ của nó làm khóa. Trả về node mà nó thay thế, hoặc ``None`` nếu nó không thay thế node nào.


.. method:: NamedNodeMap.removeNamedItem(name)

   Xóa và trả về node có :attr:`~Attr.name` đã cho. Phát sinh :exc:`NotFoundErr` nếu không có node như vậy.


.. method:: NamedNodeMap.removeNamedItemNS(namespaceURI, localName)

   Xóa và trả về node có URI namespace và tên cục bộ đã cho. Phát sinh :exc:`NotFoundErr` nếu không có node như vậy.

Bạn cũng có thể sử dụng nhóm phương thức :meth:`!getAttribute\*` được chuẩn hóa trên các đối tượng :class:`Element`.


.. _dom-documentfragment-objects:

Đối tượng DocumentFragment
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: DocumentFragment
   :no-typesetting:

:class:`DocumentFragment` là một vùng chứa node nhẹ. Đây là lớp con của :class:`Node`. Khi được chèn vào cây tài liệu, các node con của nó sẽ được chèn thay cho nó, và nó trở nên rỗng.


.. _dom-characterdata-objects:

Đối tượng CharacterData
^^^^^^^^^^^^^^^^^^^^^^^

.. class:: CharacterData
   :no-typesetting:

:class:`CharacterData` đại diện cho dữ liệu dạng văn bản trong tài liệu XML. Đây là một lớp con của :class:`Node`, đồng thời là lớp cơ sở của :class:`Text`, :class:`CDATASection` và :class:`Comment`. Các nút này không thể có nút con.


.. attribute:: CharacterData.data

   Nội dung của nút dưới dạng chuỗi.


.. attribute:: CharacterData.length

   Số ký tự trong :attr:`~CharacterData.data`. Đây là thuộc tính chỉ đọc.


.. method:: CharacterData.substringData(offset, count)

   Trả về chuỗi con của :attr:`~CharacterData.data` gồm *count* ký tự, bắt đầu tại *offset*.


.. method:: CharacterData.appendData(arg)

   Nối chuỗi *arg* vào :attr:`~CharacterData.data`.


.. method:: CharacterData.insertData(offset, arg)

   Chèn chuỗi *arg* vào :attr:`~CharacterData.data` tại *offset*.


.. method:: CharacterData.deleteData(offset, count)

   Xóa *count* ký tự khỏi :attr:`~CharacterData.data`, bắt đầu từ *offset*.


.. method:: CharacterData.replaceData(offset, count, arg)

   Thay thế *count* ký tự của :attr:`~CharacterData.data`, bắt đầu từ *offset*, bằng chuỗi *arg*.


.. _dom-comment-objects:

Đối tượng Comment
^^^^^^^^^^^^^^^^^

.. class:: Comment
   :no-typesetting:

:class:`Comment` biểu diễn một comment trong tài liệu XML. Đây là lớp con của :class:`CharacterData`.


.. attribute:: Comment.data

   Nội dung của comment dưới dạng chuỗi. Thuộc tính này chứa tất cả các ký tự nằm giữa ``<!-``\ ``-`` ở đầu và ``-``\ ``->`` ở cuối, nhưng không bao gồm các ký tự đó.


.. _dom-text-objects:

Đối tượng Text và CDATASection
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: Text
   :no-typesetting:

.. class:: CDATASection
   :no-typesetting:

Giao diện :class:`Text` biểu diễn văn bản trong tài liệu XML. Nếu parser và phần triển khai DOM hỗ trợ phần mở rộng XML của DOM, các phần văn bản được bao quanh bởi các vùng được đánh dấu là CDATA sẽ được lưu trong các đối tượng :class:`CDATASection`. Hai giao diện này giống hệt nhau, nhưng cung cấp các giá trị khác nhau cho
Thuộc tính :attr:`~Node.nodeType`.

:class:`Text` kế thừa giao diện :class:`CharacterData`, còn :class:`CDATASection` kế thừa :class:`Text`.


.. attribute:: Text.data

   Nội dung của nút văn bản dưới dạng chuỗi.


.. attribute:: Text.wholeText

   Văn bản của tất cả các nút :class:`Text` kề về mặt logic với nút này, được nối theo thứ tự tài liệu. Đây là thuộc tính chỉ đọc.


.. method:: Text.replaceWholeText(content)

   Thay thế văn bản của tất cả các nút :class:`Text` kề về mặt logic với nút này bằng *content*, đồng thời xóa các nút còn lại. Trả về nút này hoặc ``None`` nếu *content* trống.


.. method:: Text.splitText(offset)

   Tách nút này thành hai nút tại *offset*, giữ phần đầu trong nút này và trả về một nút anh em mới chứa phần còn lại.

.. note::

   Việc sử dụng một nút :class:`CDATASection` không cho biết nút đó đại diện cho một phần CDATA được đánh dấu hoàn chỉnh, mà chỉ cho biết nội dung của nút là một phần của một CDATA section. Một CDATA section đơn lẻ có thể được biểu diễn bởi nhiều hơn một nút trong cây tài liệu. Không có cách nào xác định liệu hai nút :class:`CDATASection` kề nhau có đại diện cho các CDATA section được đánh dấu khác nhau hay không.


.. _dom-pi-objects:

Đối tượng ProcessingInstruction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: ProcessingInstruction
   :no-typesetting:

Đại diện cho một processing instruction trong tài liệu XML; đối tượng này kế thừa từ
:class:`Node` interface và không thể có node con.


.. attribute:: ProcessingInstruction.target

   Nội dung của processing instruction cho đến ký tự khoảng trắng đầu tiên. Đây là thuộc tính chỉ đọc.


.. attribute:: ProcessingInstruction.data

   Nội dung của processing instruction sau ký tự khoảng trắng đầu tiên.


.. _dom-entity-objects:

Đối tượng Entity
^^^^^^^^^^^^^^^^

.. class:: Entity
   :no-typesetting:

:class:`Entity` đại diện cho một entity đã được phân tích cú pháp hoặc chưa được phân tích cú pháp được khai báo trong DTD. Đây là một lớp con của :class:`Node`. Các node Entity được chứa trong :attr:`DocumentType.entities` và không thể được chèn vào cây tài liệu. Tên của entity là :attr:`~Node.nodeName`.


.. attribute:: Entity.publicId

   Định danh công khai của entity, hoặc ``None`` nếu không được chỉ định. Đây là thuộc tính chỉ đọc.


.. attribute:: Entity.systemId

   Định danh hệ thống của entity, hoặc ``None`` nếu không được chỉ định. Đây là thuộc tính chỉ đọc.


.. attribute:: Entity.notationName

   Tên của notation dành cho entity chưa được phân tích, hoặc ``None`` đối với entity đã được phân tích. Đây là thuộc tính chỉ đọc.


.. _dom-notation-objects:

Đối tượng Notation
^^^^^^^^^^^^^^^^^^

.. class:: Notation
   :no-typesetting:

:class:`Notation` đại diện cho một notation được khai báo trong DTD. Đây là một lớp con của :class:`Node` và không thể có các nút con. Các nút notation được chứa trong :attr:`DocumentType.notations` và không thể được chèn vào cây tài liệu. Tên của notation là :attr:`~Node.nodeName`.


.. attribute:: Notation.publicId

   Định danh công khai của notation, hoặc ``None`` nếu không được chỉ định. Đây là thuộc tính chỉ đọc.


.. attribute:: Notation.systemId

   Định danh hệ thống của notation, hoặc ``None`` nếu không được chỉ định. Đây là thuộc tính chỉ đọc.


.. _dom-exceptions:

Ngoại lệ
^^^^^^^^

Khuyến nghị DOM Level 2 định nghĩa một ngoại lệ duy nhất, :exc:`DOMException`, cùng một số hằng số cho phép các ứng dụng xác định loại lỗi đã xảy ra. Các thực thể :exc:`DOMException` mang một thuộc tính :attr:`code` cung cấp giá trị thích hợp cho ngoại lệ cụ thể đó.

Giao diện DOM của Python cung cấp các hằng số, nhưng cũng mở rộng tập hợp ngoại lệ để tồn tại một ngoại lệ cụ thể cho mỗi mã ngoại lệ được DOM định nghĩa. Các implementation phải raise ngoại lệ cụ thể thích hợp, mỗi ngoại lệ đều mang giá trị thích hợp cho thuộc tính :attr:`code`.


.. exception:: DOMException

   Lớp ngoại lệ cơ sở được dùng cho tất cả các ngoại lệ DOM cụ thể. Không thể khởi tạo trực tiếp lớp ngoại lệ này.


.. exception:: DomstringSizeErr

   Được raise khi một phạm vi văn bản được chỉ định không thể chứa trong một chuỗi. Không được biết là ngoại lệ này có được dùng trong các implementation DOM của Python hay không, nhưng có thể nhận được từ các implementation DOM không được viết bằng Python.


.. exception:: HierarchyRequestErr

   Được raise khi cố gắng chèn một node vào vị trí không cho phép kiểu node đó.


.. exception:: IndexSizeErr

   Được raise khi tham số chỉ mục hoặc kích thước của một method là số âm hoặc vượt quá các giá trị được phép.


.. exception:: InuseAttributeErr

   Được phát sinh khi cố gắng chèn một nút :class:`Attr` đã tồn tại ở nơi khác trong tài liệu.


.. exception:: InvalidAccessErr

   Được phát sinh nếu một tham số hoặc một thao tác không được hỗ trợ trên đối tượng bên dưới.


.. exception:: InvalidCharacterErr

   Ngoại lệ này được phát sinh khi một tham số chuỗi chứa ký tự không được phép trong ngữ cảnh sử dụng theo khuyến nghị XML 1.0. Ví dụ, cố gắng tạo một nút :class:`Element` với dấu cách trong tên kiểu phần tử sẽ khiến lỗi này được phát sinh.


.. exception:: InvalidModificationErr

   Được phát sinh khi cố gắng sửa đổi kiểu của một nút.


.. exception:: InvalidStateErr

   Được phát sinh khi cố gắng sử dụng một đối tượng chưa được định nghĩa hoặc không còn có thể sử dụng.


.. exception:: NamespaceErr

   Nếu cố gắng thay đổi bất kỳ đối tượng nào theo cách không được phép liên quan đến khuyến nghị `Namespaces in XML <https://www.w3.org/TR/REC-xml-names/>`_, ngoại lệ này sẽ được phát sinh.


.. exception:: NotFoundErr

   Ngoại lệ khi một nút không tồn tại trong ngữ cảnh được tham chiếu.  Ví dụ,
   :meth:`NamedNodeMap.removeNamedItem` sẽ đưa ra ngoại lệ này nếu node được truyền vào không tồn tại trong map.


.. exception:: NotSupportedErr

   Được đưa ra khi implementation không hỗ trợ kiểu object hoặc operation được yêu cầu.


.. exception:: NoDataAllowedErr

   Ngoại lệ này được đưa ra nếu dữ liệu được chỉ định cho một node không hỗ trợ dữ liệu.

   .. XXX  a better explanation is needed!


.. exception:: NoModificationAllowedErr

   Được đưa ra khi cố gắng sửa đổi một object mà không cho phép sửa đổi (chẳng hạn như các node chỉ đọc).


.. exception:: SyntaxErr

   Được đưa ra khi một chuỗi không hợp lệ hoặc bị cấm được chỉ định.

   .. XXX  how is this different from InvalidCharacterErr?


.. exception:: ValidationErr

   Được đưa ra khi một operation khiến tài liệu không hợp lệ theo quy tắc về tính hợp lệ từng phần. Hiện chưa biết các implementation Python DOM có sử dụng ngoại lệ này hay không, nhưng có thể nhận được ngoại lệ này từ các implementation DOM không được viết bằng Python.


.. exception:: WrongDocumentErr

   Được đưa ra khi một node được chèn vào một tài liệu khác với tài liệu mà node hiện thuộc về, và implementation không hỗ trợ di chuyển node từ tài liệu này sang tài liệu kia.


Các mã ngoại lệ được định nghĩa trong khuyến nghị DOM ánh xạ tới các ngoại lệ được mô tả ở trên theo bảng này:

+---------------------------------------+---------------------------------+
| Hằng số                               | Ngoại lệ                        |
+=======================================+=================================+
| .. data:: DOMSTRING_SIZE_ERR          | :exc:`DomstringSizeErr`         |
+---------------------------------------+---------------------------------+
| .. data:: HIERARCHY_REQUEST_ERR       | :exc:`HierarchyRequestErr`      |
+---------------------------------------+---------------------------------+
| .. data:: INDEX_SIZE_ERR              | :exc:`IndexSizeErr`             |
+---------------------------------------+---------------------------------+
| .. data:: INUSE_ATTRIBUTE_ERR         | :exc:`InuseAttributeErr`        |
+---------------------------------------+---------------------------------+
| .. data:: INVALID_ACCESS_ERR          | :exc:`InvalidAccessErr`         |
+---------------------------------------+---------------------------------+
| .. data:: INVALID_CHARACTER_ERR       | :exc:`InvalidCharacterErr`      |
+---------------------------------------+---------------------------------+
| .. data:: INVALID_MODIFICATION_ERR    | :exc:`InvalidModificationErr`   |
+---------------------------------------+---------------------------------+
| .. data:: INVALID_STATE_ERR           | :exc:`InvalidStateErr`          |
+---------------------------------------+---------------------------------+
| .. data:: NAMESPACE_ERR               | :exc:`NamespaceErr`             |
+---------------------------------------+---------------------------------+
| .. data:: NOT_FOUND_ERR               | :exc:`NotFoundErr`              |
+---------------------------------------+---------------------------------+
| .. data:: NOT_SUPPORTED_ERR           | :exc:`NotSupportedErr`          |
+---------------------------------------+---------------------------------+
| .. data:: NO_DATA_ALLOWED_ERR         | :exc:`NoDataAllowedErr`         |
+---------------------------------------+---------------------------------+
| .. data:: NO_MODIFICATION_ALLOWED_ERR | :exc:`NoModificationAllowedErr` |
+---------------------------------------+---------------------------------+
| .. data:: SYNTAX_ERR                  | :exc:`SyntaxErr`                |
+---------------------------------------+---------------------------------+
| .. data:: VALIDATION_ERR              | :exc:`ValidationErr`            |
+---------------------------------------+---------------------------------+
| .. data:: WRONG_DOCUMENT_ERR          | :exc:`WrongDocumentErr`         |
+---------------------------------------+---------------------------------+


.. _dom-conformance:

Tính tuân thủ
-------------

Phần này mô tả các yêu cầu về tính tuân thủ và mối quan hệ giữa Python DOM API, các khuyến nghị W3C DOM và ánh xạ OMG IDL cho Python.


.. _dom-type-mapping:

Ánh xạ kiểu
^^^^^^^^^^^

Các kiểu IDL được sử dụng trong đặc tả DOM được ánh xạ tới các kiểu Python theo bảng sau.

+------------------+------------------------+
| Kiểu IDL         | Kiểu Python            |
+==================+========================+
| ``boolean``      | ``bool`` hoặc ``int``  |
+------------------+------------------------+
| ``int``          | ``int``                |
+------------------+------------------------+
| ``long int``     | ``int``                |
+------------------+------------------------+
| ``unsigned int`` | ``int``                |
+------------------+------------------------+
| ``DOMString``    | ``str`` hoặc ``bytes`` |
+------------------+------------------------+
| ``null``         | ``None``               |
+------------------+------------------------+

.. _dom-accessor-methods:

Các phương thức accessor
^^^^^^^^^^^^^^^^^^^^^^^^

Ánh xạ từ OMG IDL sang Python định nghĩa các hàm accessor cho các khai báo ``attribute`` của IDL, tương tự như ánh xạ Java. Việc ánh xạ các khai báo IDL::

   readonly attribute string someValue;
            attribute string anotherValue;

tạo ra ba hàm accessor: một phương thức "get" cho :attr:`!someValue` (:meth:`!_get_someValue`), và các phương thức "get" và "set" cho :attr:`!anotherValue` (:meth:`!_get_anotherValue` và :meth:`!_set_anotherValue`). Cụ thể, ánh xạ này không yêu cầu các thuộc tính IDL phải có thể truy cập như các thuộc tính Python thông thường: ``object.someValue`` *không* bắt buộc phải hoạt động và có thể gây ra một :exc:`AttributeError`.

Tuy nhiên, Python DOM API *có* yêu cầu việc truy cập thuộc tính thông thường phải hoạt động. Điều này có nghĩa là các surrogate điển hình được tạo bởi trình biên dịch Python IDL khó có khả năng hoạt động, và có thể cần các đối tượng wrapper ở phía client nếu các đối tượng DOM được truy cập qua CORBA. Mặc dù điều này đòi hỏi các client CORBA DOM phải cân nhắc thêm, những người triển khai có kinh nghiệm sử dụng DOM qua CORBA từ Python không xem đây là vấn đề. Các thuộc tính được khai báo ``readonly`` có thể không hạn chế quyền ghi trong mọi triển khai DOM.

Trong Python DOM API, không bắt buộc phải có các hàm accessor. Nếu được cung cấp, chúng phải có dạng được định nghĩa bởi ánh xạ Python IDL, nhưng các phương thức này được xem là không cần thiết vì có thể truy cập trực tiếp các thuộc tính từ Python. Không bao giờ được cung cấp các accessor "Set" cho các thuộc tính ``readonly``.

Các định nghĩa IDL không thể hiện đầy đủ những yêu cầu của W3C DOM API, chẳng hạn như khái niệm một số đối tượng nhất định, ví dụ như giá trị trả về của
:meth:`~Element.getElementsByTagName`, là "live". Python DOM API không yêu cầu các triển khai phải thực thi những yêu cầu như vậy.

.. _`Document Object Model (DOM) Level 2 Specification`: https://www.w3.org/TR/2000/REC-DOM-Level-2-Core-20001113/
.. _`Document Object Model (DOM) Level 1 Specification`: https://www.w3.org/TR/REC-DOM-Level-1/
.. _`Python Language Mapping Specification`: https://www.omg.org/spec/PYTH/1.2/PDF
.. _`Namespaces in XML`: https://www.w3.org/TR/REC-xml-names/
.. _`Document Object Model (DOM) Level 2 Core Specification`: https://www.w3.org/TR/DOM-Level-2-Core/core.html
.. _`XHTML 1.0: The Extensible HyperText Markup Language`: https://www.w3.org/TR/xhtml1/
