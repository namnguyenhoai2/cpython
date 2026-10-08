:mod:`!xml.dom.pulldom` --- Hỗ trợ xây dựng các cây DOM một phần
================================================================

.. module:: xml.dom.pulldom
   :synopsis: Hỗ trợ xây dựng các cây DOM một phần từ các sự kiện SAX.

.. moduleauthor:: Paul Prescod <paul@prescod.net>

**Mã nguồn:** :source:`Lib/xml/dom/pulldom.py`

.. The module was written by Paul Prescod and added in Python 2.0.
   It is not based on any specification: the implementation is the only
   reference.  The Java Streaming API for XML (StAX, JSR 173) is based on
   it, among other pull parsers.

--------------

Mô-đun :mod:`!xml.dom.pulldom` cung cấp một "pull parser", cũng có thể được yêu cầu tạo ra các phân mảnh của tài liệu có thể truy cập qua DOM khi cần. Khái niệm cơ bản là lấy các "sự kiện" từ một stream XML đến và xử lý chúng. Không giống SAX, vốn cũng sử dụng mô hình xử lý hướng sự kiện cùng với callback, người dùng pull parser chịu trách nhiệm chủ động lấy các sự kiện từ stream, lặp qua các sự kiện đó cho đến khi quá trình xử lý hoàn tất hoặc xảy ra lỗi.


.. note::

   Nếu bạn cần phân tích dữ liệu không đáng tin cậy hoặc chưa được xác thực, hãy xem
   :ref:`xml-security`.

.. versionchanged:: 3.7.1

   Trình phân tích SAX không còn xử lý các thực thể bên ngoài tổng quát theo mặc định, nhằm tăng cường bảo mật theo mặc định. Để bật tính năng xử lý các thực thể bên ngoài, hãy truyền một parser tùy chỉnh vào::

      from xml.dom.pulldom import parse
      from xml.sax import make_parser
      from xml.sax.handler import feature_external_ges

      parser = make_parser()
      parser.setFeature(feature_external_ges, True)
      parse(filename, parser=parser)


Ví dụ::

   from xml.dom import pulldom

   doc = pulldom.parse('sales_items.xml')
   for event, node in doc:
       if event == pulldom.START_ELEMENT and node.tagName == 'item':
           if int(node.getAttribute('price')) > 50:
               doc.expandNode(node)
               print(node.toxml())

``event`` là một trong các hằng số sau đây, còn ``node`` là node mà sự kiện liên quan đến. Các node triển khai các interface :mod:`xml.dom`; chúng được tạo bởi DOM implementation được cung cấp cho :class:`PullDOM`, mặc định là :mod:`xml.dom.minidom`.


.. data:: START_DOCUMENT
          END_DOCUMENT

   Phần bắt đầu và phần kết thúc của document. *node* là :class:`~xml.dom.Document`.


.. data:: START_ELEMENT
          END_ELEMENT

   Thẻ mở và thẻ đóng của một element. *node* là :class:`~xml.dom.Element`.


.. data:: CHARACTERS

   Dữ liệu ký tự. *node* là node :class:`~xml.dom.Text`.


.. data:: IGNORABLE_WHITESPACE

   Khoảng trắng trong nội dung element, như được khai báo trong DTD. *node* là node :class:`~xml.dom.Text`.


.. data:: COMMENT

   Một comment. *node* là nút :class:`~xml.dom.Comment` node.


.. data:: PROCESSING_INSTRUCTION

   Một processing instruction. *node* là nút :class:`~xml.dom.ProcessingInstruction` node.

Vì tài liệu được xử lý như một luồng sự kiện "phẳng", "cây" tài liệu được duyệt ngầm và các phần tử mong muốn được tìm thấy bất kể độ sâu của chúng trong cây. Nói cách khác, không cần xem xét các vấn đề phân cấp như tìm kiếm đệ quy các node của tài liệu, mặc dù nếu ngữ cảnh của các phần tử là quan trọng, ta sẽ cần duy trì một số trạng thái liên quan đến ngữ cảnh (tức là ghi nhớ vị trí hiện tại trong tài liệu tại bất kỳ thời điểm nào) hoặc sử dụng phương thức :func:`DOMEventStream.expandNode` và chuyển sang xử lý liên quan đến DOM.


.. class:: PullDOM(documentFactory=None)

   Lớp con của :class:`xml.sax.handler.ContentHandler`, chuyển các sự kiện SAX thành các sự kiện của pull parser. Các node được tạo nhưng không được thêm vào cây, trừ khi :meth:`~DOMEventStream.expandNode` được gọi. *documentFactory*, nếu được cung cấp, là một triển khai DOM được dùng để tạo tài liệu; theo mặc định, triển khai của :mod:`xml.dom.minidom` được sử dụng.


.. class:: SAX2DOM(documentFactory=None)

   Lớp con của :class:`PullDOM`, đồng thời thêm mọi node được tạo vào cây, nhờ đó xây dựng toàn bộ tài liệu.


.. function:: parse(stream_or_string, parser=None, bufsize=None)

   Trả về một :class:`DOMEventStream` từ đầu vào đã cho. *stream_or_string* có thể là tên tệp hoặc một đối tượng giống tệp. *parser*, nếu được cung cấp, phải là một
   đối tượng :class:`~xml.sax.xmlreader.XMLReader`. Hàm này sẽ thay đổi document handler của parser và kích hoạt hỗ trợ namespace; các cấu hình khác của parser (chẳng hạn như thiết lập entity resolver) phải được thực hiện trước đó.

Nếu bạn có XML trong một chuỗi, thay vào đó, bạn có thể sử dụng hàm :func:`parseString`:

.. function:: parseString(string, parser=None)

   Trả về một :class:`DOMEventStream` đại diện cho *chuỗi*. *Chuỗi* phải là một instance :class:`str`; để phân tích cú pháp byte, hãy truyền một đối tượng tệp nhị phân cho :func:`parse`.

.. data:: default_bufsize

   Giá trị mặc định cho tham số *bufsize* của :func:`parse`.

   Có thể thay đổi giá trị của biến này trước khi gọi :func:`parse`, và giá trị mới sẽ có hiệu lực.

.. _domeventstream-objects:

Đối tượng DOMEventStream
------------------------

.. class:: DOMEventStream(stream, parser, bufsize)

   Tạo các sự kiện cho dữ liệu được đọc từ đối tượng tệp *stream* bởi trình phân tích cú pháp :class:`~xml.sax.xmlreader.XMLReader` *parser*. Dữ liệu được đọc mỗi lần *bufsize* byte hoặc ký tự đối với luồng văn bản.

   .. versionchanged:: 3.11
      Đã xóa hỗ trợ cho phương thức :meth:`~object.__getitem__`.

   .. method:: getEvent()

      Trả về tuple ``(event, node)`` tiếp theo hoặc ``None`` khi đến cuối tài liệu. Xem phần trên để biết các sự kiện và node tương ứng. Node hiện tại không chứa thông tin về các node con của nó, trừ khi
      :meth:`expandNode` được gọi.

   .. method:: expandNode(node)

      Mở rộng tất cả các node con của *node* vào *node*. Ví dụ::

          from xml.dom import pulldom

          xml = '<html><title>Foo</title> <p>Some text <div>and more</div></p> </html>'
          doc = pulldom.parseString(xml)
          for event, node in doc:
              if event == pulldom.START_ELEMENT and node.tagName == 'p':
                  # Câu lệnh sau chỉ in '<p/>'
                  print(node.toxml())
                  doc.expandNode(node)
                  # Câu lệnh sau in node cùng tất cả các node con của nó '<p>Some text <div>and more</div></p>'
                  print(node.toxml())

   .. method:: reset()

      Loại bỏ các sự kiện chưa được đọc và chuẩn bị đối tượng để phân tích cú pháp một tài liệu mới.


   .. method:: clear()

      Giải phóng parser và tài liệu. Stream không bị đóng và đối tượng không thể được sử dụng nữa.
