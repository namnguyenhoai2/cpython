:mod:`!xml.sax.saxutils` --- Tiện ích SAX
=========================================

.. module:: xml.sax.saxutils
   :synopsis: Các hàm và lớp tiện lợi dùng với SAX.

.. moduleauthor:: Lars Marius Garshol <larsga@garshol.priv.no>
.. sectionauthor:: Martin v. Löwis <martin@v.loewis.de>

**Mã nguồn:** :source:`Lib/xml/sax/saxutils.py`

--------------

Mô-đun :mod:`!xml.sax.saxutils` chứa một số lớp và hàm thường hữu ích khi tạo các ứng dụng SAX, dùng trực tiếp hoặc làm lớp cơ sở.


.. function:: escape(data, entities={})

   Escape ``'&'``, ``'<'`` và ``'>'`` trong một chuỗi dữ liệu.

   Bạn có thể escape các chuỗi dữ liệu khác bằng cách truyền một dictionary làm tham số tùy chọn *entities*. Tất cả khóa và giá trị phải là chuỗi; mỗi khóa sẽ được thay thế bằng giá trị tương ứng. Các ký tự ``'&'``, ``'<'`` và ``'>'`` luôn được escape, ngay cả khi *entities* được cung cấp.

   .. note::

      Chỉ nên dùng hàm này để escape các ký tự không thể sử dụng trực tiếp trong XML. Không dùng hàm này như một hàm dịch chuỗi tổng quát.

.. function:: unescape(data, entities={})

   Hủy escape cho ``'&amp;'``, ``'&lt;'`` và ``'&gt;'`` trong một chuỗi dữ liệu.

   Bạn có thể hủy escape cho các chuỗi dữ liệu khác bằng cách truyền một dictionary làm tham số tùy chọn *entities*. Các khóa và giá trị đều phải là chuỗi; mỗi khóa sẽ được thay thế bằng giá trị tương ứng. ``'&amp;'``, ``'&lt;'`` và ``'&gt;'`` luôn được hủy escape, ngay cả khi *entities* được cung cấp.


.. function:: quoteattr(data, entities={})

   Tương tự :func:`escape`, nhưng cũng chuẩn bị *data* để dùng làm giá trị thuộc tính. Giá trị trả về là phiên bản được đặt trong dấu ngoặc kép của *data*, kèm theo mọi thay thế bổ sung cần thiết. :func:`quoteattr` sẽ chọn một ký tự dấu ngoặc dựa trên nội dung của *data*, cố gắng tránh mã hóa bất kỳ ký tự dấu ngoặc nào trong chuỗi. Nếu cả ký tự dấu ngoặc đơn và dấu ngoặc kép đều đã có trong *data*, các ký tự dấu ngoặc kép sẽ được mã hóa và *data* sẽ được bao quanh bằng dấu ngoặc kép. Chuỗi kết quả có thể được dùng trực tiếp làm giá trị thuộc tính::

      >>> print("<element attr=%s>" % quoteattr("ab ' cd \" ef"))
      <element attr="ab ' cd &quot; ef">

   Hàm này hữu ích khi tạo các giá trị thuộc tính cho HTML hoặc bất kỳ SGML nào sử dụng cú pháp tham chiếu cụ thể.


.. class:: XMLGenerator(out=None, encoding='iso-8859-1', short_empty_elements=False)

   Lớp này triển khai interface :class:`~xml.sax.handler.ContentHandler` bằng cách ghi các sự kiện SAX trở lại một tài liệu XML. Nói cách khác, việc sử dụng một :class:`XMLGenerator` làm content handler sẽ tái tạo tài liệu gốc đang được phân tích cú pháp. *out* phải là một đối tượng dạng tệp, mặc định là *sys.stdout*. *encoding* là encoding của output stream, mặc định là ``'iso-8859-1'``. *short_empty_elements* kiểm soát cách định dạng các phần tử không chứa nội dung: nếu là ``False`` (mặc định), chúng được xuất ra dưới dạng một cặp thẻ bắt đầu/kết thúc; nếu đặt thành ``True``, chúng được xuất ra dưới dạng một thẻ tự đóng duy nhất.

   .. versionchanged:: 3.2
      Đã thêm tham số *short_empty_elements*.


.. class:: XMLFilterBase(base)

   Lớp này được thiết kế để nằm giữa một
   :class:`~xml.sax.xmlreader.XMLReader` và các event handler của ứng dụng client. Theo mặc định, nó chỉ chuyển tiếp các request lên reader và các event đến handler mà không thay đổi, nhưng các subclass có thể override những method cụ thể để sửa đổi event stream hoặc các request cấu hình khi chúng đi qua.

   .. method:: getParent()

      Trả về reader cha hoặc ``None`` nếu chưa được thiết lập.


   .. method:: setParent(parent)

      Thiết lập reader cha, từ đó các event được đọc.


.. function:: prepare_input_source(source, base='')

   Hàm này nhận một input source và một base URL tùy chọn, rồi trả về một đối tượng :class:`~xml.sax.xmlreader.InputSource` đã được phân giải đầy đủ và sẵn sàng để đọc. Input source có thể được cung cấp dưới dạng chuỗi, đối tượng giống file hoặc đối tượng :class:`~xml.sax.xmlreader.InputSource`; các parser sẽ sử dụng hàm này để triển khai đối số *source* cho các
   method :meth:`~xml.sax.xmlreader.XMLReader.parse`.

