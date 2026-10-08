:mod:`!html.parser` --- Trình phân tích cú pháp HTML và XHTML đơn giản
======================================================================

.. module:: html.parser
   :synopsis: Một trình phân tích cú pháp đơn giản có thể xử lý HTML và XHTML.

**Mã nguồn:** :source:`Lib/html/parser.py`

.. index::
   single: HTML
   single: XHTML

--------------

Mô-đun này định nghĩa một lớp :class:`HTMLParser`, làm nền tảng cho việc phân tích các tệp văn bản được định dạng bằng HTML (HyperText Mark-up Language) và XHTML.

.. class:: HTMLParser(*, convert_charrefs=True, scripting=False)

   Tạo một phiên bản trình phân tích cú pháp có khả năng phân tích mã đánh dấu không hợp lệ.

   Nếu *convert_charrefs* là true (mặc định), tất cả các tham chiếu ký tự (ngoại trừ những tham chiếu trong các phần tử như ``script`` và ``style``) sẽ tự động được chuyển đổi thành các ký tự Unicode tương ứng.

   Nếu *scripting* là false (mặc định), nội dung của phần tử ``noscript`` sẽ được phân tích bình thường; nếu là true, nội dung được trả về nguyên trạng mà không được phân tích.

   Một thực thể :class:`.HTMLParser` được cung cấp dữ liệu HTML và gọi các phương thức handler khi gặp thẻ bắt đầu, thẻ kết thúc, văn bản, chú thích và các phần tử markup khác. Người dùng nên tạo lớp con của :class:`.HTMLParser` và ghi đè các phương thức của lớp đó để triển khai hành vi mong muốn.

   Parser này không kiểm tra xem thẻ kết thúc có khớp với thẻ bắt đầu hay không, cũng không gọi handler của thẻ kết thúc đối với các phần tử được đóng ngầm khi một phần tử bên ngoài được đóng.

   .. versionchanged:: 3.4
      Đã thêm keyword argument *convert_charrefs*.

   .. versionchanged:: 3.5
      Giá trị mặc định của đối số *convert_charrefs* hiện là ``True``.

   .. versionchanged:: 3.14.1
      Đã thêm tham số *scripting*.


Ứng dụng parser HTML mẫu
------------------------

Dưới đây là một ví dụ cơ bản về một parser HTML đơn giản sử dụng
:class:`HTMLParser` lớp để in ra các thẻ mở, thẻ đóng và dữ liệu khi chúng được gặp:

.. testcode::

   from html.parser import HTMLParser

   class MyHTMLParser(HTMLParser):
       def handle_starttag(self, tag, attrs):
           print("Encountered a start tag:", tag)

       def handle_endtag(self, tag):
           print("Encountered an end tag :", tag)

       def handle_data(self, data):
           print("Encountered some data  :", data)

   parser = MyHTMLParser()
   parser.feed('<html><head><title>Test</title></head>'
               '<body><h1>Parse me!</h1></body></html>')

Kết quả sau đó sẽ là:

.. testoutput::

   Encountered a start tag: html
   Encountered a start tag: head
   Encountered a start tag: title
   Encountered some data  : Test
   Encountered an end tag : title
   Encountered an end tag : head
   Encountered a start tag: body
   Encountered a start tag: h1
   Encountered some data  : Parse me!
   Encountered an end tag : h1
   Encountered an end tag : body
   Encountered an end tag : html


:class:`.HTMLParser` Phương thức
--------------------------------

Các instance :class:`HTMLParser` có những phương thức sau:


.. method:: HTMLParser.feed(data)

   Cung cấp một phần văn bản cho parser. Văn bản được xử lý khi bao gồm các phần tử hoàn chỉnh; dữ liệu chưa hoàn chỉnh sẽ được lưu vào bộ đệm cho đến khi có thêm dữ liệu được cung cấp hoặc
   :meth:`close` được gọi. *data* phải là :class:`str`.


.. method:: HTMLParser.close()

   Buộc xử lý toàn bộ dữ liệu đang được lưu trong bộ đệm như thể dữ liệu đó được theo sau bởi một dấu hiệu cuối tệp. Phương thức này có thể được định nghĩa lại trong một lớp dẫn xuất để xác định quá trình xử lý bổ sung ở cuối dữ liệu đầu vào, nhưng phiên bản được định nghĩa lại luôn phải gọi :class:`HTMLParser` phương thức của lớp cơ sở :meth:`close`.


.. method:: HTMLParser.reset()

   Đặt lại instance. Làm mất toàn bộ dữ liệu chưa xử lý. Phương thức này được gọi ngầm tại thời điểm khởi tạo.


.. method:: HTMLParser.getpos()

   Trả về số dòng và offset hiện tại.


.. method:: HTMLParser.get_starttag_text()

   Trả về nội dung của thẻ bắt đầu được mở gần đây nhất. Thông thường, điều này không cần thiết khi xử lý có cấu trúc, nhưng có thể hữu ích khi xử lý HTML "được triển khai" hoặc tạo lại đầu vào với số thay đổi tối thiểu (chẳng hạn như có thể giữ nguyên khoảng trắng giữa các thuộc tính).


Các phương thức sau được gọi khi gặp dữ liệu hoặc phần tử markup và được thiết kế để ghi đè trong một lớp con. Các triển khai của lớp cơ sở không thực hiện thao tác nào (ngoại trừ :meth:`~HTMLParser.handle_startendtag`):


.. method:: HTMLParser.handle_starttag(tag, attrs)

   Phương thức này được gọi để xử lý thẻ bắt đầu của một phần tử (ví dụ: ``<div id="main">``).

   Đối số *tag* là tên của thẻ được chuyển thành chữ thường. Đối số *attrs* là một danh sách các cặp ``(name, value)`` chứa những thuộc tính được tìm thấy bên trong dấu ngoặc ``<>`` của thẻ. *name* sẽ được chuyển thành chữ thường, các dấu ngoặc kép trong *value* đã được loại bỏ, đồng thời các tham chiếu ký tự và thực thể đã được thay thế. Đối với các thuộc tính rỗng, *value* là ``None``.

   Ví dụ, đối với thẻ ``<A HREF="https://www.cwi.nl/">``, phương thức này sẽ được gọi như sau: ``handle_starttag('a', [('href', 'https://www.cwi.nl/')])``.

   Tất cả các tham chiếu thực thể từ :mod:`html.entities` đều được thay thế trong các giá trị thuộc tính.


.. method:: HTMLParser.handle_endtag(tag)

   Phương thức này được gọi để xử lý thẻ kết thúc của một phần tử (ví dụ: ``</div>``).

   Đối số *tag* là tên của thẻ được chuyển thành chữ thường.


.. method:: HTMLParser.handle_startendtag(tag, attrs)

   Tương tự như :meth:`handle_starttag`, nhưng được gọi khi parser gặp một thẻ rỗng kiểu XHTML (``<img ... />``). Các lớp con có yêu cầu thông tin từ vựng cụ thể này có thể ghi đè phương thức này; phần triển khai mặc định chỉ đơn giản gọi :meth:`handle_starttag` và :meth:`handle_endtag`.


.. method:: HTMLParser.handle_data(data)

   Phương thức này được gọi để xử lý dữ liệu tùy ý (ví dụ: các nút văn bản và nội dung của những phần tử như ``script`` và ``style``).


.. method:: HTMLParser.handle_entityref(name)

   Phương thức này được gọi để xử lý một tham chiếu ký tự có tên theo dạng ``&name;`` (ví dụ: ``&gt;``), trong đó *name* là một tham chiếu thực thể tổng quát (ví dụ: ``'gt'``). Phương thức này chỉ được gọi nếu *convert_charrefs* là false.


.. method:: HTMLParser.handle_charref(name)

   Phương thức này được gọi để xử lý các tham chiếu ký tự số thập phân và thập lục phân theo dạng :samp:`&#{NNN};` và :samp:`&#x{NNN};`. Ví dụ, giá trị thập phân tương đương với ``&gt;`` là ``&#62;``, trong khi giá trị thập lục phân là ``&#x3E;``; trong trường hợp này, phương thức sẽ nhận ``'62'`` hoặc ``'x3E'``. Phương thức này chỉ được gọi nếu *convert_charrefs* là false.


.. method:: HTMLParser.handle_comment(data)

   Phương thức này được gọi khi gặp một chú thích (ví dụ ``<!--comment-->``).

   Ví dụ, chú thích ``<!-- comment -->`` sẽ khiến phương thức này được gọi với đối số ``' comment '``.

   Nội dung của các chú thích điều kiện (condcoms) của Internet Explorer cũng sẽ được gửi đến phương thức này, vì vậy, với ``<!--[if IE 9]>IE9-specific content<![endif]-->``, phương thức này sẽ nhận được ``'[if IE 9]>IE9-specific content<![endif]'``.


.. method:: HTMLParser.handle_decl(decl)

   Phương thức này được gọi để xử lý khai báo doctype HTML (ví dụ ``<!DOCTYPE html>``).

   Tham số *decl* sẽ là toàn bộ nội dung của khai báo bên trong phần đánh dấu ``<!...>`` (ví dụ ``'DOCTYPE html'``).


.. method:: HTMLParser.handle_pi(data)

   Phương thức được gọi khi gặp một processing instruction. Tham số *data* sẽ chứa toàn bộ processing instruction. Ví dụ, đối với processing instruction ``<?proc color='red'>``, phương thức này sẽ được gọi như sau ``handle_pi("proc color='red'")``. Phương thức này được thiết kế để được ghi đè bởi một lớp dẫn xuất; phần triển khai của lớp cơ sở không thực hiện gì.

   .. note::

      Lớp :class:`HTMLParser` sử dụng các quy tắc cú pháp SGML cho processing instruction. Một processing instruction XHTML sử dụng ``'?'`` ở cuối sẽ khiến ``'?'`` được đưa vào *data*.


.. method:: HTMLParser.unknown_decl(data)

   Phương thức này được gọi khi parser đọc một khai báo không được nhận dạng.

   Tham số *data* sẽ chứa toàn bộ nội dung của khai báo bên trong markup ``<![...]>``. Đôi khi, một lớp dẫn xuất cần ghi đè phương thức này. Phần triển khai của lớp cơ sở không thực hiện thao tác nào.


.. _htmlparser-examples:

Ví dụ
-----

Lớp sau đây triển khai một parser được dùng để minh họa thêm các ví dụ:

.. testcode::

   from html.parser import HTMLParser
   from html.entities import name2codepoint

   class MyHTMLParser(HTMLParser):
       def handle_starttag(self, tag, attrs):
           print("Start tag:", tag)
           for attr in attrs:
               print("     attr:", attr)

       def handle_endtag(self, tag):
           print("End tag  :", tag)

       def handle_data(self, data):
           print("Data     :", data)

       def handle_comment(self, data):
           print("Comment  :", data)

       def handle_entityref(self, name):
           c = chr(name2codepoint[name])
           print("Named ent:", c)

       def handle_charref(self, name):
           if name.startswith('x'):
               c = chr(int(name[1:], 16))
           else:
               c = chr(int(name))
           print("Num ent  :", c)

       def handle_decl(self, data):
           print("Decl     :", data)

   parser = MyHTMLParser()

Phân tích một doctype:

.. doctest::

   >>> parser.feed('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" '
   ...             '"http://www.w3.org/TR/html4/strict.dtd">')
   Decl     : DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"

Phân tích một element có một vài thuộc tính và tiêu đề:

.. doctest::

   >>> parser.feed('<img src="python-logo.png" alt="The Python logo">')
   Start tag: img
        attr: ('src', 'python-logo.png')
        attr: ('alt', 'The Python logo')
   >>>
   >>> parser.feed('<h1>Python</h1>')
   Start tag: h1
   Data     : Python
   End tag  : h1

Nội dung của các element như ``script`` và ``style`` được trả về nguyên trạng, không phân tích thêm:

.. doctest::

   >>> parser.feed('<style type="text/css">#python { color: green }</style>')
   Start tag: style
        attr: ('type', 'text/css')
   Data     : #python { color: green }
   End tag  : style

   >>> parser.feed('<script type="text/javascript">'
   ...             'alert("<strong>hello! &#9786;</strong>");</script>')
   Start tag: script
        attr: ('type', 'text/javascript')
   Data     : alert("<strong>hello! &#9786;</strong>");
   End tag  : script

Tên thuộc tính được chuyển thành chữ thường, dấu ngoặc kép trong giá trị thuộc tính được loại bỏ, và ``None`` được trả về dưới dạng *value* đối với các thuộc tính rỗng (chẳng hạn như ``checked``):

.. doctest::

   >>> parser.feed("<input TYPE='checkbox' checked required='' disabled=disabled>")
   Start tag: input
        attr: ('type', 'checkbox')
        attr: ('checked', None)
        attr: ('required', '')
        attr: ('disabled', 'disabled')

Phân tích cú pháp các chú thích:

.. doctest::

   >>> parser.feed('<!--a comment-->'
   ...             '<!--[if IE 9]>IE-specific content<![endif]-->')
   Comment  : a comment
   Comment  : [if IE 9]>IE-specific content<![endif]

Phân tích cú pháp các tham chiếu ký tự có tên và dạng số rồi chuyển chúng thành ký tự tương ứng (lưu ý: cả 3 tham chiếu này đều tương đương với ``'>'``):

.. doctest::

   >>> parser = MyHTMLParser()
   >>> parser.feed('&gt;&#62;&#x3E;')
   Data     : >>>

   >>> parser = MyHTMLParser(convert_charrefs=False)
   >>> parser.feed('&gt;&#62;&#x3E;')
   Named ent: >
   Num ent  : >
   Num ent  : >

Việc truyền các đoạn chưa hoàn chỉnh vào :meth:`~HTMLParser.feed` vẫn hoạt động, nhưng
:meth:`~HTMLParser.handle_data` có thể được gọi nhiều hơn một lần nếu *convert_charrefs* là false:

.. doctest::

   >>> for chunk in ['<sp', 'an>buff', 'ered', ' text</s', 'pan>']:
   ...     parser.feed(chunk)
   ...
   Start tag: span
   Data     : buff
   Data     : ered
   Data     :  text
   End tag  : span

Việc phân tích cú pháp HTML không hợp lệ (ví dụ: thuộc tính không được đặt trong dấu ngoặc kép) cũng hoạt động:

.. doctest::

   >>> parser.feed('<p><a class=link href=#main>tag soup</p ></a>')
   Start tag: p
   Start tag: a
        attr: ('class', 'link')
        attr: ('href', '#main')
   Data     : tag soup
   End tag  : p
   End tag  : a
