:mod:`!xml.dom.minidom` --- Triển khai DOM tối giản
===================================================

.. module:: xml.dom.minidom
   :synopsis: Triển khai Document Object Model (DOM) tối giản.

.. moduleauthor:: Paul Prescod <paul@prescod.net>
.. sectionauthor:: Paul Prescod <paul@prescod.net>
.. sectionauthor:: Martin v. Löwis <martin@v.loewis.de>

**Mã nguồn:** :source:`Lib/xml/dom/minidom.py`

--------------

:mod:`!xml.dom.minidom` là một triển khai tối giản của giao diện Document Object Model, với API tương tự các API trong những ngôn ngữ khác. Nó được thiết kế đơn giản hơn DOM đầy đủ và cũng nhỏ gọn hơn đáng kể. Những người chưa thành thạo DOM nên cân nhắc sử dụng
:mod:`xml.etree.ElementTree` mô-đun để xử lý XML thay vào đó.


.. note::

   Nếu bạn cần phân tích dữ liệu không đáng tin cậy hoặc chưa được xác thực, hãy xem
   :ref:`xml-security`.


Các ứng dụng DOM thường bắt đầu bằng cách phân tích một số XML thành DOM. Với
Đối với :mod:`!xml.dom.minidom`, việc này được thực hiện thông qua các hàm parse::

   from xml.dom.minidom import parse, parseString

   dom1 = parse('c:\\temp\\mydata.xml')  # phân tích một tệp XML theo tên

   datasource = open('c:\\temp\\mydata.xml')
   dom2 = parse(datasource)  # phân tích một tệp đang mở

   dom3 = parseString('<myxml>Some data<empty/> some more data</myxml>')

Hàm :func:`parse` có thể nhận tên tệp hoặc một đối tượng tệp đang mở.


.. function:: parse(filename_or_file, parser=None, bufsize=None)

   Trả về một :class:`Document` từ đầu vào đã cho. *filename_or_file* có thể là tên tệp hoặc một đối tượng giống tệp. *parser*, nếu được cung cấp, phải là một đối tượng trình phân tích SAX2. Hàm này sẽ thay đổi document handler của trình phân tích và kích hoạt hỗ trợ namespace; các cấu hình trình phân tích khác (chẳng hạn như thiết lập entity resolver) phải được thực hiện trước.

Nếu bạn có XML trong một chuỗi, thay vào đó bạn có thể sử dụng hàm :func:`parseString`:


.. function:: parseString(string, parser=None)

   Trả về một :class:`Document` biểu diễn *string*. Phương thức này tạo một
   đối tượng :class:`io.StringIO` cho chuỗi và truyền đối tượng đó cho :func:`parse`.

Cả hai hàm đều trả về một đối tượng :class:`Document` đại diện cho nội dung của tài liệu.

Hai hàm :func:`parse` và :func:`parseString` kết nối một trình phân tích XML với một "DOM builder" có thể tiếp nhận các sự kiện phân tích từ bất kỳ trình phân tích SAX nào và chuyển đổi chúng thành một cây DOM. Tên của các hàm này có thể gây hiểu nhầm, nhưng sẽ dễ nắm bắt khi tìm hiểu các interface. Việc phân tích tài liệu sẽ hoàn tất trước khi các hàm này trả về; chỉ là bản thân các hàm này không cung cấp một triển khai trình phân tích.

Bạn cũng có thể tạo một :class:`Document` bằng cách gọi một phương thức trên đối tượng "DOM Implementation". Bạn có thể lấy đối tượng này bằng cách gọi hàm
:func:`getDOMImplementation` trong package :mod:`xml.dom` hoặc
module :mod:`!xml.dom.minidom`. Khi đã có một :class:`Document`, bạn có thể thêm các nút con vào đó để tạo nội dung cho DOM::

   from xml.dom.minidom import getDOMImplementation

   impl = getDOMImplementation()

   newdoc = impl.createDocument(None, "some_tag", None)
   top_element = newdoc.documentElement
   text = newdoc.createTextNode('Some textual content.')
   top_element.appendChild(text)

Khi đã có một đối tượng tài liệu DOM, bạn có thể truy cập các phần của tài liệu XML thông qua các thuộc tính và phương thức của nó. Các thuộc tính này được định nghĩa trong đặc tả DOM. Thuộc tính chính của đối tượng tài liệu là
Thuộc tính :attr:`documentElement`. Nó cung cấp cho bạn phần tử chính trong tài liệu XML: phần tử chứa tất cả các phần tử khác. Đây là một chương trình ví dụ::

   dom3 = parseString("<myxml>Some data</myxml>")
   assert dom3.documentElement.tagName == "myxml"

Khi đã hoàn tất với một cây DOM, bạn có thể tùy ý gọi
phương thức :meth:`unlink` để khuyến khích dọn dẹp sớm các đối tượng hiện không còn cần thiết. :meth:`unlink` là một phần mở rộng của DOM API dành riêng cho :mod:`!xml.dom.minidom`\ , khiến nút và các nút con của nó về cơ bản không còn tác dụng. Nếu không, bộ thu gom rác của Python cuối cùng sẽ xử lý các đối tượng trong cây.

.. seealso::

   `Đặc tả Mô hình Đối tượng Tài liệu (DOM) Cấp 1 <https://www.w3.org/TR/REC-DOM-Level-1/>`_
      Khuyến nghị của W3C về DOM được :mod:`!xml.dom.minidom` hỗ trợ.


.. _minidom-objects:

Các đối tượng DOM
-----------------

Định nghĩa DOM API cho Python được cung cấp trong tài liệu về module :mod:`xml.dom`. Phần này liệt kê những điểm khác biệt giữa API và
:mod:`!xml.dom.minidom`.


.. method:: Node.unlink()

   Ngắt các tham chiếu nội bộ trong DOM để DOM được bộ thu gom rác giải phóng trên các phiên bản Python không có cyclic GC. Ngay cả khi có cyclic GC, việc sử dụng phương thức này có thể giúp giải phóng một lượng lớn bộ nhớ sớm hơn, vì vậy gọi phương thức này trên các đối tượng DOM ngay khi không còn cần đến chúng là một thực hành tốt. Chỉ cần gọi phương thức này trên đối tượng :class:`Document`, nhưng cũng có thể gọi trên các nút con để loại bỏ các nút con của nút đó.

   Bạn có thể tránh gọi phương thức này một cách rõ ràng bằng cách sử dụng câu lệnh :keyword:`with`. Đoạn mã sau sẽ tự động ngắt liên kết của *dom* khi
   khối :keyword:`!with` kết thúc::

      with xml.dom.minidom.parse(datasource) as dom:
          ... # Làm việc với dom.


.. method:: Node.writexml(writer, indent="", addindent="", newl="", \
                          encoding=None, standalone=None)

   Ghi XML vào đối tượng writer. writer nhận đầu vào là văn bản chứ không phải byte; đối tượng này phải có phương thức :meth:`write` tương ứng với phương thức của giao diện đối tượng tệp. Tham số *indent* là mức thụt lề của nút hiện tại. Tham số *addindent* là mức thụt lề tăng thêm cho các nút con của nút hiện tại. Tham số *newl* chỉ định chuỗi dùng để kết thúc các dòng mới.

   Đối với nút :class:`Document`, có thể sử dụng thêm đối số từ khóa *encoding* để chỉ định trường encoding của phần tiêu đề XML.

   Tương tự, việc nêu rõ đối số *standalone* sẽ khiến các khai báo tài liệu standalone được thêm vào phần mở đầu của tài liệu XML. Nếu giá trị được đặt thành ``True``, ``standalone="yes"`` sẽ được thêm vào; nếu không, giá trị sẽ được đặt thành ``"no"``. Nếu không nêu đối số này, khai báo sẽ bị lược bỏ khỏi tài liệu.

   .. versionchanged:: 3.8
      Phương thức :meth:`writexml` hiện bảo toàn thứ tự thuộc tính do người dùng chỉ định.

   .. versionchanged:: 3.9
      Tham số *standalone* đã được thêm vào.

.. method:: Node.toxml(encoding=None, standalone=None)

   Trả về một chuỗi hoặc chuỗi byte chứa XML được biểu diễn bởi nút DOM.

   Với đối số *encoding* [1]_ được chỉ định rõ ràng, kết quả là một chuỗi byte sử dụng encoding đã chỉ định. Nếu không có đối số *encoding*, kết quả là một chuỗi Unicode và khai báo XML trong chuỗi kết quả không chỉ định encoding. Việc encoding chuỗi này bằng encoding khác UTF-8 nhiều khả năng là không chính xác, vì UTF-8 là encoding mặc định của XML.

   Đối số *standalone* hoạt động chính xác như trong :meth:`writexml`.

   .. versionchanged:: 3.8
      Phương thức :meth:`toxml` hiện bảo toàn thứ tự thuộc tính do người dùng chỉ định.

   .. versionchanged:: 3.9
      Tham số *standalone* đã được thêm vào.

.. method:: Node.toprettyxml(indent="\t", newl="\n", encoding=None, \
                             standalone=None)

   Trả về phiên bản được định dạng đẹp của tài liệu. *indent* chỉ định chuỗi thụt lề và mặc định là một ký tự tab; *newl* chỉ định chuỗi được xuất ở cuối mỗi dòng và mặc định là ``\n``.

   Đối số *encoding* hoạt động giống như đối số tương ứng của
   :meth:`toxml`.

   Đối số *standalone* hoạt động chính xác như trong :meth:`writexml`.

   .. versionchanged:: 3.8
      Phương thức :meth:`toprettyxml` hiện bảo toàn thứ tự thuộc tính do người dùng chỉ định.

   .. versionchanged:: 3.9
      Tham số *standalone* đã được thêm vào.

.. _dom-example:

Ví dụ về DOM
------------

Chương trình ví dụ này là một ví dụ khá thực tế về một chương trình đơn giản. Trong trường hợp cụ thể này, chúng ta không tận dụng nhiều tính linh hoạt của DOM.

.. literalinclude:: ../includes/minidom-example.py


.. _minidom-and-dom:

minidom và tiêu chuẩn DOM
-------------------------

Module :mod:`!xml.dom.minidom` về cơ bản là một DOM tương thích với DOM 1.0, cùng một số tính năng của DOM 2 (chủ yếu là các tính năng về namespace).

Việc sử dụng giao diện DOM trong Python khá đơn giản. Các quy tắc ánh xạ sau được áp dụng:

* Các giao diện được truy cập thông qua các đối tượng instance. Ứng dụng không nên tự khởi tạo các class; thay vào đó, chúng nên sử dụng các hàm creator có sẵn trên đối tượng :class:`Document`. Các giao diện dẫn xuất hỗ trợ mọi thao tác (và thuộc tính) từ các giao diện cơ sở, cùng với mọi thao tác mới.

* Các thao tác được sử dụng dưới dạng các phương thức. Vì DOM chỉ sử dụng các tham số :keyword:`in`, các đối số được truyền theo thứ tự thông thường (từ trái sang phải). Không có đối số tùy chọn. Các thao tác ``void`` trả về ``None``.

* Các thuộc tính IDL ánh xạ tới các thuộc tính của instance. Để tương thích với ánh xạ ngôn ngữ OMG IDL cho Python, một thuộc tính ``foo`` cũng có thể được truy cập thông qua các phương thức accessor :meth:`_get_foo` và :meth:`_set_foo`. Các thuộc tính ``readonly`` không được thay đổi; điều này không được thực thi tại runtime.

* Các kiểu ``short int``, ``unsigned int``, ``unsigned long long`` và ``boolean`` đều ánh xạ tới các đối tượng số nguyên Python.

* Kiểu ``DOMString`` ánh xạ tới các chuỗi Python. :mod:`!xml.dom.minidom` hỗ trợ cả bytes và chuỗi, nhưng thông thường sẽ tạo ra các chuỗi. Các giá trị kiểu ``DOMString`` cũng có thể là ``None`` khi đặc tả DOM của W3C cho phép giá trị IDL ``null``.

* Các khai báo ``const`` ánh xạ tới các biến trong phạm vi tương ứng của chúng (ví dụ: ``xml.dom.minidom.Node.PROCESSING_INSTRUCTION_NODE``); chúng không được thay đổi.

* ``DOMException`` hiện chưa được hỗ trợ trong :mod:`!xml.dom.minidom`. Thay vào đó, :mod:`!xml.dom.minidom` sử dụng các exception chuẩn của Python như
  :exc:`TypeError` và :exc:`AttributeError`.

* Mỗi interface :class:`~xml.dom.NodeList` và :class:`~xml.dom.NamedNodeMap` đều có hai implementation, cung cấp các phương thức và thao tác bổ sung.

  :attr:`~xml.dom.Node.childNodes` là một lớp con của :class:`list`, hoặc, đối với các node không thể có node con, là một lớp con của :class:`tuple`. Nó hỗ trợ phép lặp, phép nối, lập chỉ mục và cắt lát.

  :attr:`~xml.dom.Node.attributes` hỗ trợ ``len()``, toán tử :keyword:`in`, phép truy cập phần tử theo tên hoặc theo một tuple ``(namespaceURI, localName)``, phép gán và xóa, cùng các phương thức :meth:`!get`, :meth:`!keys`,
  :meth:`!keysNS`, :meth:`!values`, :meth:`!items` và :meth:`!itemsNS`.
  :attr:`~xml.dom.DocumentType.entities` và
  :attr:`~xml.dom.DocumentType.notations` là chỉ đọc và chỉ hỗ trợ ``len()`` cùng phép truy cập phần tử theo tên.

* :attr:`~xml.dom.Document.strictErrorChecking` và
  :attr:`~xml.dom.Attr.specified` luôn là ``False``.

* :meth:`~xml.dom.Element.removeAttribute` và
  :meth:`~xml.dom.Element.removeAttributeNS` phát sinh
  :exc:`~xml.dom.NotFoundErr` nếu không có thuộc tính tương ứng, trong khi DOM quy định rằng thao tác này không có tác dụng.

Các interface sau đây chưa được triển khai trong :mod:`!xml.dom.minidom`:

* :class:`DOMTimeStamp`

* :class:`EntityReference`

Hầu hết những thông tin này phản ánh dữ liệu trong tài liệu XML nhưng không có nhiều giá trị sử dụng chung đối với phần lớn người dùng DOM.

.. rubric:: Chú thích cuối trang

.. [1] Tên encoding có trong đầu ra XML phải tuân thủ các tiêu chuẩn thích hợp. Ví dụ: "UTF-8" là hợp lệ, nhưng "UTF8" không hợp lệ trong phần khai báo của tài liệu XML, mặc dù Python chấp nhận nó làm tên encoding. Xem https://www.w3.org/TR/2006/REC-xml11-20060816/#NT-EncodingDecl và https://www.iana.org/assignments/character-sets/character-sets.xhtml.

.. _`Document Object Model (DOM) Level 1 Specification`: https://www.w3.org/TR/REC-DOM-Level-1/
