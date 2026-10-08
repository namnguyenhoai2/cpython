:mod:`!xml.etree.ElementTree` --- API XML ElementTree
=====================================================

.. module:: xml.etree.ElementTree
   :synopsis: Triển khai API ElementTree.

.. moduleauthor:: Fredrik Lundh <fredrik@pythonware.com>

**Mã nguồn:** :source:`Lib/xml/etree/ElementTree.py`

--------------

Mô-đun :mod:`!xml.etree.ElementTree` triển khai một API đơn giản và hiệu quả để phân tích cú pháp và tạo dữ liệu XML.

.. versionchanged:: 3.3
   Mô-đun này sẽ sử dụng một triển khai nhanh bất cứ khi nào có sẵn.

.. deprecated:: 3.3
   Bí danh :mod:`!xml.etree.cElementTree` của mô-đun này đã lỗi thời.


.. note::

   Nếu bạn cần phân tích cú pháp dữ liệu không đáng tin cậy hoặc chưa được xác thực, hãy xem
   :ref:`xml-security`.

Hướng dẫn
---------

Đây là hướng dẫn ngắn về cách sử dụng :mod:`!xml.etree.ElementTree` (viết tắt là ``ET``). Mục tiêu là minh họa một số khối xây dựng và khái niệm cơ bản của module.

Cây XML và các phần tử
^^^^^^^^^^^^^^^^^^^^^^

XML vốn là một định dạng dữ liệu có cấu trúc phân cấp, và cách tự nhiên nhất để biểu diễn nó là bằng một cây. ``ET`` có hai lớp phục vụ mục đích này -
:class:`ElementTree` biểu diễn toàn bộ tài liệu XML dưới dạng một cây, và
:class:`Element` biểu diễn một node riêng lẻ trong cây này. Các thao tác với toàn bộ tài liệu (đọc và ghi từ/vào các tệp) thường được thực hiện ở cấp độ :class:`ElementTree`. Các thao tác với một phần tử XML riêng lẻ và các phần tử con của nó được thực hiện ở cấp độ :class:`Element`.

.. _elementtree-parsing-xml:

Phân tích cú pháp XML
^^^^^^^^^^^^^^^^^^^^^

Chúng ta sẽ sử dụng tài liệu XML hư cấu :file:`country_data.xml` làm dữ liệu mẫu cho phần này:

.. code-block:: xml

   <?xml version="1.0"?>
   <data>
       <country name="Liechtenstein">
           <rank>1</rank>
           <year>2008</year>
           <gdppc>141100</gdppc>
           <neighbor name="Austria" direction="E"/>
           <neighbor name="Switzerland" direction="W"/>
       </country>
       <country name="Singapore">
           <rank>4</rank>
           <year>2011</year>
           <gdppc>59900</gdppc>
           <neighbor name="Malaysia" direction="N"/>
       </country>
       <country name="Panama">
           <rank>68</rank>
           <year>2011</year>
           <gdppc>13600</gdppc>
           <neighbor name="Costa Rica" direction="W"/>
           <neighbor name="Colombia" direction="E"/>
       </country>
   </data>

Chúng ta có thể nhập dữ liệu này bằng cách đọc từ một tệp::

   import xml.etree.ElementTree as ET
   tree = ET.parse('country_data.xml')
   root = tree.getroot()

Hoặc trực tiếp từ một chuỗi::

   root = ET.fromstring(country_data_as_string)

:func:`fromstring` phân tích XML từ một chuỗi trực tiếp thành một :class:`Element`, là phần tử gốc của cây đã được phân tích. Một số hàm phân tích khác có thể tạo ra một :class:`ElementTree`. Hãy xem tài liệu để chắc chắn.

Là một :class:`Element`, ``root`` có một thẻ và một dictionary chứa các thuộc tính::

   >>> root.tag
   'data'
   >>> root.attrib
   {}

Nó cũng có các nút con mà chúng ta có thể lặp qua::

   >>> for child in root:
   ...     print(child.tag, child.attrib)
   ...
   country {'name': 'Liechtenstein'}
   country {'name': 'Singapore'}
   country {'name': 'Panama'}

Các nút con được lồng vào nhau và chúng ta có thể truy cập các nút con cụ thể theo chỉ mục::

   >>> root[0][1].text
   '2008'


.. note::

   Không phải tất cả các phần tử của đầu vào XML đều sẽ trở thành phần tử của cây đã phân tích cú pháp. Hiện tại, module này bỏ qua mọi chú thích XML, chỉ thị xử lý và khai báo kiểu tài liệu trong đầu vào. Tuy nhiên, các cây được xây dựng bằng API của module này thay vì được phân tích cú pháp từ văn bản XML vẫn có thể chứa chú thích và chỉ thị xử lý; chúng sẽ được đưa vào khi tạo đầu ra XML. Có thể truy cập một khai báo kiểu tài liệu bằng cách truyền một thực thể :class:`TreeBuilder` tùy chỉnh vào constructor :class:`XMLParser`.


.. _elementtree-pull-parsing:

API Pull để phân tích cú pháp không chặn
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Hầu hết các hàm phân tích cú pháp do module này cung cấp đều yêu cầu đọc toàn bộ tài liệu cùng lúc trước khi trả về bất kỳ kết quả nào. Có thể sử dụng một
:class:`XMLParser` và nạp dữ liệu vào đó từng phần, nhưng đây là một API push gọi các phương thức trên một đích callback, quá cấp thấp và bất tiện đối với hầu hết nhu cầu. Đôi khi điều người dùng thực sự muốn là có thể phân tích cú pháp XML từng phần mà không thực hiện các thao tác chặn, đồng thời vẫn tận dụng sự tiện lợi của các đối tượng :class:`Element` được tạo hoàn chỉnh.

Công cụ mạnh mẽ nhất để thực hiện việc này là :class:`XMLPullParser`. Công cụ này không yêu cầu thao tác đọc chặn để lấy dữ liệu XML, mà thay vào đó được nạp dữ liệu từng phần bằng các lệnh gọi :meth:`XMLPullParser.feed`. Để lấy các phần tử XML đã được phân tích cú pháp, hãy gọi :meth:`XMLPullParser.read_events`. Sau đây là một ví dụ::

   >>> parser = ET.XMLPullParser(['start', 'end'])
   >>> parser.feed('<mytag>sometext')
   >>> list(parser.read_events())
   [('start', <Element 'mytag' at 0x7fa66db2be58>)]
   >>> parser.feed(' more text</mytag>')
   >>> for event, elem in parser.read_events():
   ...     print(event)
   ...     print(elem.tag, 'text=', elem.text)
   ...
   end
   mytag text= sometext more text

Trường hợp sử dụng rõ ràng nhất là các ứng dụng hoạt động theo cách không chặn, trong đó dữ liệu XML được nhận từ một socket hoặc được đọc từng phần từ một thiết bị lưu trữ nào đó. Trong những trường hợp như vậy, các thao tác đọc chặn là không thể chấp nhận.

Vì rất linh hoạt, :class:`XMLPullParser` có thể bất tiện khi sử dụng cho các trường hợp đơn giản hơn. Nếu bạn không ngại ứng dụng của mình bị chặn khi đọc dữ liệu XML nhưng vẫn muốn có khả năng phân tích cú pháp từng phần, hãy xem :func:`iterparse`.

Lưu ý rằng cả hai parser đều xây dựng cây theo từng bước: cây không được giải phóng theo từng bước, vì vậy mọi phần tử đã phân tích đều được giữ lại cho đến khi đọc xong toàn bộ tài liệu. Để giảm mức sử dụng bộ nhớ, hãy loại bỏ dữ liệu không còn cần thiết.

Nếu các phần tử được xử lý có kích thước lớn, chỉ cần xóa nội dung của chúng. Cách này hoạt động bất kể chúng nằm ở đâu trong cây, nhưng các phần tử đã bị làm rỗng vẫn được giữ lại trong đó::

   for event, elem in ET.iterparse(source):
       if elem.tag == 'record':
           process(elem)
           elem.clear()

Nếu một phần tử có số lượng lớn phần tử con, hãy xóa các phần tử con đã được xử lý khỏi phần tử đó::

   for event, elem in ET.iterparse(source, events=('start', 'end')):
       if event == 'start' and elem.tag == 'parent':
           parent = elem
       elif event == 'end' and elem.tag == 'child':
           process(elem)
           parent.remove(elem)

Các ví dụ này không mang tính toàn diện mà chỉ minh họa cho hai trường hợp phổ biến. Nếu bạn hoàn toàn không cần cây, hãy phân tích bằng :class:`XMLParser` và một target tùy chỉnh; khi đó cây sẽ không được tạo và không cần xóa gì cả.

Khi cần phản hồi *immediate* thông qua các sự kiện, việc gọi phương thức
:meth:`XMLPullParser.flush` có thể giúp giảm độ trễ; hãy nhớ đọc kỹ các ghi chú bảo mật liên quan.


Tìm các phần tử đáng chú ý
^^^^^^^^^^^^^^^^^^^^^^^^^^

:class:`Element` có một số phương thức hữu ích giúp lặp đệ quy qua toàn bộ cây con bên dưới nó (các phần tử con, các phần tử con của chúng, v.v.). Ví dụ:
:meth:`Element.iter`::

   >>> for neighbor in root.iter('neighbor'):
   ...     print(neighbor.attrib)
   ...
   {'name': 'Austria', 'direction': 'E'}
   {'name': 'Switzerland', 'direction': 'W'}
   {'name': 'Malaysia', 'direction': 'N'}
   {'name': 'Costa Rica', 'direction': 'W'}
   {'name': 'Colombia', 'direction': 'E'}

:meth:`Element.findall` chỉ tìm các phần tử có thẻ là phần tử con trực tiếp của phần tử hiện tại. :meth:`Element.find` tìm *first* phần tử con đầu tiên có một thẻ cụ thể, còn :attr:`Element.text` truy cập nội dung văn bản của phần tử. :meth:`Element.get` truy cập các thuộc tính của phần tử::

   >>> for country in root.findall('country'):
   ...     rank = country.find('rank').text
   ...     name = country.get('name')
   ...     print(name, rank)
   ...
   Liechtenstein 1
   Singapore 4
   Panama 68

Có thể chỉ định phức tạp hơn các phần tử cần tìm bằng cách sử dụng :ref:`XPath <elementtree-xpath>`.

Sửa đổi tệp XML
^^^^^^^^^^^^^^^

:class:`ElementTree` cung cấp một cách đơn giản để xây dựng tài liệu XML và ghi chúng vào tệp. Phương thức :meth:`ElementTree.write` phục vụ mục đích này.

Sau khi được tạo, một đối tượng :class:`Element` có thể được thao tác bằng cách thay đổi trực tiếp các trường của nó (chẳng hạn như :attr:`Element.text`), thêm và sửa đổi các thuộc tính (phương thức :meth:`Element.set`), cũng như thêm các phần tử con mới (ví dụ bằng :meth:`Element.append`).

Giả sử chúng ta muốn tăng hạng của mỗi quốc gia lên một đơn vị và thêm thuộc tính ``updated`` vào phần tử rank::

   >>> for rank in root.iter('rank'):
   ...     new_rank = int(rank.text) + 1
   ...     rank.text = str(new_rank)
   ...     rank.set('updated', 'yes')
   ...
   >>> tree.write('output.xml')

XML của chúng ta hiện có dạng như sau:

.. code-block:: xml

   <?xml version="1.0"?>
   <data>
       <country name="Liechtenstein">
           <rank updated="yes">2</rank>
           <year>2008</year>
           <gdppc>141100</gdppc>
           <neighbor name="Austria" direction="E"/>
           <neighbor name="Switzerland" direction="W"/>
       </country>
       <country name="Singapore">
           <rank updated="yes">5</rank>
           <year>2011</year>
           <gdppc>59900</gdppc>
           <neighbor name="Malaysia" direction="N"/>
       </country>
       <country name="Panama">
           <rank updated="yes">69</rank>
           <year>2011</year>
           <gdppc>13600</gdppc>
           <neighbor name="Costa Rica" direction="W"/>
           <neighbor name="Colombia" direction="E"/>
       </country>
   </data>

Chúng ta có thể xóa các phần tử bằng :meth:`Element.remove`. Giả sử chúng ta muốn xóa tất cả các quốc gia có thứ hạng lớn hơn 50::

   >>> for country in root.findall('country'):
   ...     # sử dụng root.findall() để tránh xóa trong khi duyệt
   ...     rank = int(country.find('rank').text)
   ...     if rank > 50:
   ...         root.remove(country)
   ...
   >>> tree.write('output.xml')

Lưu ý rằng việc sửa đổi đồng thời trong khi lặp có thể gây ra sự cố, tương tự như khi lặp và sửa đổi các list hoặc dict trong Python. Vì vậy, ví dụ trước tiên thu thập tất cả các phần tử phù hợp bằng ``root.findall()``, rồi mới lặp qua danh sách các phần tử phù hợp.

XML của chúng ta hiện có dạng như sau:

.. code-block:: xml

   <?xml version="1.0"?>
   <data>
       <country name="Liechtenstein">
           <rank updated="yes">2</rank>
           <year>2008</year>
           <gdppc>141100</gdppc>
           <neighbor name="Austria" direction="E"/>
           <neighbor name="Switzerland" direction="W"/>
       </country>
       <country name="Singapore">
           <rank updated="yes">5</rank>
           <year>2011</year>
           <gdppc>59900</gdppc>
           <neighbor name="Malaysia" direction="N"/>
       </country>
   </data>

Xây dựng tài liệu XML
^^^^^^^^^^^^^^^^^^^^^

Hàm :func:`SubElement` cũng cung cấp một cách thuận tiện để tạo các phần tử con mới cho một phần tử đã cho::

   >>> a = ET.Element('a')
   >>> b = ET.SubElement(a, 'b')
   >>> c = ET.SubElement(a, 'c')
   >>> d = ET.SubElement(c, 'd')
   >>> ET.dump(a)
   <a><b /><c><d /></c></a>

Phân tích XML với Namespace
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Nếu đầu vào XML có `namespace <https://en.wikipedia.org/wiki/XML_namespace>`__, các thẻ và thuộc tính có tiền tố ở dạng ``prefix:sometag`` sẽ được mở rộng thành ``{uri}sometag``, trong đó *tiền tố* được thay thế bằng *URI* đầy đủ. Ngoài ra, nếu có `namespace mặc định <https://www.w3.org/TR/xml-names/#defaulting>`__, URI đầy đủ đó sẽ được thêm vào trước tất cả các thẻ không có tiền tố.

Dưới đây là một ví dụ XML sử dụng hai namespace, một namespace có tiền tố "fictional" và namespace còn lại đóng vai trò là namespace mặc định:

.. code-block:: xml

    <?xml version="1.0"?>
    <actors xmlns:fictional="http://characters.example.com"
            xmlns="http://people.example.com">
        <actor>
            <name>John Cleese</name>
            <fictional:character>Lancelot</fictional:character>
            <fictional:character>Archie Leach</fictional:character>
        </actor>
        <actor>
            <name>Eric Idle</name>
            <fictional:character>Sir Robin</fictional:character>
            <fictional:character>Gunther</fictional:character>
            <fictional:character>Commander Clement</fictional:character>
        </actor>
    </actors>

Một cách để tìm kiếm và khám phá ví dụ XML này là thêm URI theo cách thủ công vào mọi thẻ hoặc thuộc tính trong xpath của một
:meth:`~Element.find` hoặc :meth:`~Element.findall`::

    root = fromstring(xml_text)
    for actor in root.findall('{http://people.example.com}actor'):
        name = actor.find('{http://people.example.com}name')
        print(name.text)
        for char in actor.findall('{http://characters.example.com}character'):
            print(' |-->', char.text)

Một cách tốt hơn để tìm kiếm ví dụ XML có namespace là tạo một dictionary với các tiền tố riêng của bạn và sử dụng chúng trong các hàm tìm kiếm::

    ns = {'real_person': 'http://people.example.com',
          'role': 'http://characters.example.com'}

    for actor in root.findall('real_person:actor', ns):
        name = actor.find('real_person:name', ns)
        print(name.text)
        for char in actor.findall('role:character', ns):
            print(' |-->', char.text)

Cả hai cách tiếp cận này đều cho ra::

    John Cleese
     |--> Lancelot
     |--> Archie Leach
    Eric Idle
     |--> Sir Robin
     |--> Gunther
     |--> Commander Clement


.. _elementtree-xpath:

Hỗ trợ XPath
------------

Mô-đun này cung cấp khả năng hỗ trợ hạn chế cho các biểu thức `XPath <https://www.w3.org/TR/xpath>`_ để định vị các phần tử trong một cây. Mục tiêu là hỗ trợ một tập con nhỏ của cú pháp rút gọn; một công cụ XPath đầy đủ nằm ngoài phạm vi của mô-đun.

Ví dụ
^^^^^

Dưới đây là một ví dụ minh họa một số khả năng XPath của mô-đun. Chúng ta sẽ sử dụng tài liệu XML ``countrydata`` từ
:ref:`Phân tích XML <elementtree-parsing-xml>`::

   import xml.etree.ElementTree as ET

   root = ET.fromstring(countrydata)

   # Các phần tử cấp cao nhất
   root.findall(".")

   # Tất cả các phần tử cháu 'láng giềng' của các phần tử con 'country' ở cấp cao nhất
   # phần tử
   root.findall("./country/neighbor")

   # Các nút có name='Singapore' và có nút con 'year'
   root.findall(".//year/..[@name='Singapore']")

   # Các nút 'year' là nút con của các nút có name='Singapore'
   root.findall(".//*[@name='Singapore']/year")

   # Tất cả các nút 'neighbor' là nút con thứ hai của nút cha tương ứng
   root.findall(".//neighbor[2]")

Đối với XML có namespace, hãy sử dụng ký hiệu qualified ``{namespace}tag`` thông thường::

   # Tất cả các thẻ "title" của dublin-core trong tài liệu
   root.findall(".//{http://purl.org/dc/elements/1.1/}title")


Cú pháp XPath được hỗ trợ
^^^^^^^^^^^^^^^^^^^^^^^^^

.. tabularcolumns:: |l|L|

+------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Cú pháp                | Ý nghĩa                                                                                                                                                                                                                                                                                                                                                                                                                                |
+========================+========================================================================================================================================================================================================================================================================================================================================================================================================================================+
| ``tag``                | Chọn tất cả các phần tử con có thẻ đã cho. Ví dụ, ``spam`` chọn tất cả các phần tử con có tên ``spam``, còn ``spam/egg`` chọn tất cả các phần tử cháu có tên ``egg`` trong tất cả các phần tử con có tên ``spam``. ``{namespace}*`` chọn tất cả các thẻ trong namespace đã cho, ``{*}spam`` chọn các thẻ có tên ``spam`` trong bất kỳ namespace nào (hoặc không có namespace), còn ``{}*`` chỉ chọn các thẻ không thuộc namespace nào. |
|                        |                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|                        | .. versionchanged:: 3.8                                                                                                                                                                                                                                                                                                                                                                                                                |
|                        |    Đã bổ sung hỗ trợ cho ký tự đại diện dấu sao.                                                                                                                                                                                                                                                                                                                                                                                       |
+------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``*``                  | Chọn tất cả các phần tử con, bao gồm cả chú thích và chỉ thị xử lý. Ví dụ, ``*/egg`` chọn tất cả các phần tử cháu có tên ``egg``.                                                                                                                                                                                                                                                                                                      |
+------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``.``                  | Chọn node hiện tại. Tính năng này chủ yếu hữu ích ở đầu path để cho biết đó là một relative path.                                                                                                                                                                                                                                                                                                                                      |
+------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``//``                 | Chọn tất cả các phần tử con cháu ở mọi cấp bên dưới node hiện tại. Ví dụ, ``.//egg`` chọn tất cả các phần tử ``egg`` trong toàn bộ cây.                                                                                                                                                                                                                                                                                                |
+------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``..``                 | Chọn phần tử cha. Trả về ``None`` nếu đường dẫn cố gắng truy cập các phần tử tổ tiên của phần tử bắt đầu (phần tử mà ``find`` được gọi trên đó).                                                                                                                                                                                                                                                                                       |
+------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``[@attrib]``          | Chọn tất cả các phần tử có thuộc tính đã cho.                                                                                                                                                                                                                                                                                                                                                                                          |
+------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``[@attrib='value']``  | Chọn tất cả các phần tử mà thuộc tính đã cho có giá trị đã cho. Giá trị không được chứa dấu ngoặc kép.                                                                                                                                                                                                                                                                                                                                 |
+------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``[@attrib!='value']`` | Chọn tất cả các phần tử mà thuộc tính đã cho không có giá trị đã cho. Giá trị không được chứa dấu ngoặc kép.                                                                                                                                                                                                                                                                                                                           |
|                        |                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|                        | .. versionadded:: 3.10                                                                                                                                                                                                                                                                                                                                                                                                                 |
+------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``[tag]``              | Chọn tất cả các phần tử có phần tử con được đặt tên là ``tag``. Chỉ hỗ trợ các phần tử con trực tiếp.                                                                                                                                                                                                                                                                                                                                  |
+------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``[.='text']``         | Chọn tất cả các phần tử có toàn bộ nội dung văn bản, bao gồm cả các phần tử hậu duệ, bằng với ``text`` đã cho.                                                                                                                                                                                                                                                                                                                         |
|                        |                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|                        | .. versionadded:: 3.7                                                                                                                                                                                                                                                                                                                                                                                                                  |
+------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``[.!='text']``        | Chọn tất cả các phần tử có toàn bộ nội dung văn bản, bao gồm cả các phần tử hậu duệ, không bằng với ``text`` đã cho.                                                                                                                                                                                                                                                                                                                   |
|                        |                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|                        | .. versionadded:: 3.10                                                                                                                                                                                                                                                                                                                                                                                                                 |
+------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``[tag='text']``       | Chọn tất cả các phần tử có phần tử con tên là ``tag`` với toàn bộ nội dung văn bản, bao gồm cả các phần tử hậu duệ, bằng với ``text`` đã cho.                                                                                                                                                                                                                                                                                          |
+------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``[tag!='text']``      | Chọn tất cả các phần tử có phần tử con tên là ``tag`` với toàn bộ nội dung văn bản, bao gồm cả các phần tử hậu duệ, không bằng với ``text`` đã cho.                                                                                                                                                                                                                                                                                    |
|                        |                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|                        | .. versionadded:: 3.10                                                                                                                                                                                                                                                                                                                                                                                                                 |
+------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ``[position]``         | Chọn tất cả các phần tử nằm ở vị trí đã cho. Vị trí có thể là một số nguyên (1 là vị trí đầu tiên), biểu thức ``last()`` (cho vị trí cuối cùng) hoặc một vị trí tính tương đối so với vị trí cuối cùng (ví dụ: ``last()-1``).                                                                                                                                                                                                          |
+------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

Các predicate (biểu thức trong dấu ngoặc vuông) phải đứng trước một tên thẻ, dấu hoa thị hoặc predicate khác. Các predicate ``position`` phải đứng trước một tên thẻ.

Tham khảo
---------

.. _elementtree-functions:

Hàm
^^^

.. function:: canonicalize(xml_data=None, *, out=None, from_file=None, **options)

   Hàm chuyển đổi `C14N 2.0 <https://www.w3.org/TR/xml-c14n2/>`_.

   Canonicalization là cách chuẩn hóa đầu ra XML để cho phép so sánh từng byte và tạo chữ ký số. Cách này hạn chế mức độ tự do của các bộ tuần tự hóa XML, thay vào đó tạo ra một biểu diễn XML chặt chẽ hơn. Các hạn chế chính liên quan đến vị trí của khai báo namespace, thứ tự của các thuộc tính và khoảng trắng có thể bỏ qua.

   Hàm này nhận một chuỗi dữ liệu XML (*xml_data*) hoặc đường dẫn tệp hay đối tượng giống tệp (*from_file*) làm đầu vào, chuyển đổi dữ liệu sang dạng canonical và ghi dữ liệu bằng đối tượng tệp (hoặc giống tệp) *out*, nếu được cung cấp; nếu không, hàm trả về dữ liệu dưới dạng chuỗi văn bản. Tệp đầu ra nhận văn bản, không phải byte. Vì vậy, tệp cần được mở ở chế độ văn bản với mã hóa ``utf-8``.

   Các cách sử dụng điển hình::

      xml_data = "<root>...</root>"
      print(canonicalize(xml_data))

      with open("c14n_output.xml", mode='w', encoding='utf-8') as out_file:
          canonicalize(xml_data, out=out_file)

      with open("c14n_output.xml", mode='w', encoding='utf-8') as out_file:
          canonicalize(from_file="inputfile.xml", out=out_file)

   Các *options* cấu hình như sau:

   - *with_comments*: đặt thành true để bao gồm các chú thích (mặc định: false)
   - *strip_text*: đặt thành true để loại bỏ khoảng trắng trước và sau nội dung văn bản
                   (mặc định: false)
   - *rewrite_prefixes*: đặt thành true để thay thế các tiền tố namespace bằng "n{number}"
                         (mặc định: false)
   - *qname_aware_tags*: một tập hợp các tên thẻ nhận biết qname, trong đó các tiền tố
                         sẽ được thay thế trong nội dung văn bản (mặc định: rỗng)
   - *qname_aware_attrs*: một tập hợp các tên thuộc tính nhận biết qname, trong đó các tiền tố
                          sẽ được thay thế trong nội dung văn bản (mặc định: rỗng)
   - *exclude_attrs*: một tập hợp các tên thuộc tính không được tuần tự hóa
   - *exclude_tags*: một tập hợp các tên thẻ không nên được tuần tự hóa

   Trong danh sách tùy chọn ở trên, "một tập hợp" đề cập đến bất kỳ collection hoặc iterable nào của các chuỗi; không yêu cầu thứ tự.

   .. versionadded:: 3.8


.. function:: Comment(text=None)

   Factory phần tử comment. Hàm factory này tạo một phần tử đặc biệt, phần tử này sẽ được serializer tiêu chuẩn tuần tự hóa thành một comment XML. *text* là một chuỗi chứa nội dung comment. Trả về một instance phần tử đại diện cho một comment.

   Lưu ý rằng :class:`XMLParser` bỏ qua các comment trong đầu vào thay vì tạo các đối tượng comment cho chúng. Một :class:`ElementTree` sẽ chỉ chứa các node comment nếu chúng đã được chèn vào tree bằng một trong các phương thức :class:`Element`.

.. function:: dump(elem)

   Ghi một tree phần tử hoặc cấu trúc phần tử vào sys.stdout. Chỉ nên sử dụng hàm này để debug.

   Định dạng đầu ra chính xác phụ thuộc vào cách triển khai. Trong phiên bản này, đầu ra được ghi dưới dạng một tệp XML thông thường.

   *elem* là một tree phần tử hoặc một phần tử riêng lẻ.

   .. versionchanged:: 3.8
      Hàm :func:`dump` hiện giữ nguyên thứ tự thuộc tính do người dùng chỉ định.


.. function:: fromstring(text, parser=None)

   Phân tích một phần XML từ một hằng chuỗi. Giống như :func:`XML`. *text* là một chuỗi chứa dữ liệu XML. *parser* là một parser instance tùy chọn. Nếu không được cung cấp, parser :class:`XMLParser` tiêu chuẩn sẽ được sử dụng. Trả về một instance :class:`Element`.


.. function:: fromstringlist(sequence, parser=None)

   Phân tích một tài liệu XML từ một chuỗi các mảnh chuỗi. *sequence* là một danh sách hoặc chuỗi khác chứa các mảnh dữ liệu XML. *parser* là một parser instance tùy chọn. Nếu không được cung cấp, parser :class:`XMLParser` tiêu chuẩn sẽ được sử dụng. Trả về một instance :class:`Element`.

   .. versionadded:: 3.2


.. function:: indent(tree, space="  ", level=0)

   Thêm khoảng trắng vào cây con để thụt lề cây một cách trực quan. Có thể dùng cách này để tạo đầu ra XML được định dạng đẹp. *tree* có thể là một Element hoặc ElementTree. *space* là chuỗi khoảng trắng sẽ được chèn vào mỗi cấp thụt lề, mặc định là hai ký tự khoảng trắng. Để thụt lề các cây con một phần bên trong một cây đã được thụt lề, hãy truyền cấp thụt lề ban đầu dưới dạng *level*.

   .. versionadded:: 3.9


.. function:: iselement(element)

   Kiểm tra xem một đối tượng có phải là một element object hợp lệ hay không. *element* là một element instance. Trả về ``True`` nếu đây là một element object.


.. function:: iterparse(source, events=None, parser=None)

   Phân tích một phần XML vào một element tree theo cách tăng dần và thông báo cho người dùng về tiến trình. *source* là tên tệp hoặc :term:`file object` chứa dữ liệu XML. *events* là một chuỗi các sự kiện cần báo cáo. Các sự kiện được hỗ trợ là các chuỗi ``"start"``, ``"end"``, ``"comment"``, ``"pi"``, ``"start-ns"`` và ``"end-ns"`` (các sự kiện "ns" được dùng để lấy thông tin namespace chi tiết). Nếu *events* bị bỏ qua, chỉ các sự kiện ``"end"`` được báo cáo. *parser* là một parser instance tùy chọn. Nếu không được cung cấp, parser :class:`XMLParser` tiêu chuẩn sẽ được sử dụng. *parser* phải là một instance của :class:`XMLParser` hoặc một lớp con của nó và chỉ có thể sử dụng :class:`TreeBuilder` mặc định làm target. Trả về một :term:`iterator` cung cấp các cặp ``(event, elem)``; đối tượng này có thuộc tính ``root`` tham chiếu đến phần tử gốc của cây XML kết quả sau khi *source* được đọc hoàn toàn. Iterator có phương thức :meth:`!close` để đóng đối tượng tệp nội bộ nếu *source* là tên tệp.

   Lưu ý rằng mặc dù :func:`iterparse` xây dựng cây theo cách tăng dần, hàm này thực hiện các thao tác đọc blocking trên *source* (hoặc tệp mà nó chỉ đến). Vì vậy, hàm này không phù hợp với các ứng dụng không thể thực hiện thao tác đọc blocking. Để phân tích hoàn toàn không blocking, hãy xem :class:`XMLPullParser`.

   Cây chỉ được xây dựng dần dần, chứ không được giải phóng dần dần: mọi phần tử đã phân tích đều được giữ lại cho đến khi đọc xong toàn bộ tài liệu. Xem :ref:`elementtree-pull-parsing` để biết cách giữ mức sử dụng bộ nhớ thấp.

   .. note::

      :func:`iterparse` chỉ đảm bảo rằng nó đã gặp ký tự ">" của thẻ bắt đầu khi phát ra sự kiện "start", vì vậy các thuộc tính đã được xác định, nhưng nội dung của các thuộc tính text và tail chưa được xác định tại thời điểm đó. Điều tương tự cũng áp dụng cho các phần tử con; chúng có thể đã có hoặc chưa có.

      Nếu cần một phần tử được điền đầy đủ, thay vào đó hãy tìm các sự kiện "end".

   .. deprecated:: 3.4
      Đối số *parser*.

   .. versionchanged:: 3.8
      Các sự kiện ``comment`` và ``pi`` đã được thêm vào.

   .. versionchanged:: 3.13
      Đã thêm phương thức :meth:`!close`.


.. function:: parse(source, parser=None)

   Phân tích một phần XML thành cây phần tử. *source* là tên tệp hoặc đối tượng tệp chứa dữ liệu XML. *parser* là một instance parser tùy chọn. Nếu không được cung cấp, parser :class:`XMLParser` tiêu chuẩn sẽ được sử dụng. Trả về một
   :class:`ElementTree` một instance.


.. function:: ProcessingInstruction(target, text=None)

   Bộ tạo phần tử PI. Hàm factory này tạo một phần tử đặc biệt sẽ được tuần tự hóa thành một processing instruction XML. *target* là một chuỗi chứa đích PI. *text* là một chuỗi chứa nội dung PI, nếu được cung cấp. Trả về một instance phần tử đại diện cho một processing instruction.

   Lưu ý rằng :class:`XMLParser` bỏ qua các processing instruction trong dữ liệu đầu vào thay vì tạo các đối tượng PI cho chúng. Một
   :class:`ElementTree` sẽ chỉ chứa các node processing instruction nếu chúng đã được chèn vào cây bằng một trong các
   phương thức :class:`Element`.

.. function:: register_namespace(prefix, uri)

   Đăng ký một tiền tố namespace. Registry là toàn cục và mọi ánh xạ hiện có cho tiền tố hoặc URI namespace đã cho sẽ bị xóa. *prefix* là một tiền tố namespace. *uri* là một URI namespace. Các thẻ và thuộc tính trong namespace này sẽ được tuần tự hóa bằng tiền tố đã cho, nếu có thể.

   .. versionadded:: 3.2


.. function:: SubElement(parent, tag, attrib={}, **extra)

   Bộ tạo phần tử con. Hàm này tạo một instance phần tử và nối phần tử đó vào một phần tử hiện có.

   *parent* là phần tử cha. *tag* là tên phần tử con. *attrib* là một từ điển tùy chọn, chứa các thuộc tính của phần tử. *extra* chứa các thuộc tính bổ sung, được truyền dưới dạng đối số từ khóa. Trả về một thực thể phần tử.


.. function:: tostring(element, encoding="us-ascii", method="xml", *, \
                       xml_declaration=None, default_namespace=None, \ short_empty_elements=True)

   Tạo biểu diễn chuỗi của một phần tử XML, bao gồm tất cả các phần tử con. *element* là một thực thể :class:`Element`. *encoding* [1]_ là encoding đầu ra (mặc định là US-ASCII). Sử dụng ``encoding="unicode"`` để tạo chuỗi Unicode (nếu không sẽ tạo một bytestring). *method* là ``"xml"``, ``"html"`` hoặc ``"text"`` (mặc định là ``"xml"``). *xml_declaration*, *default_namespace* và *short_empty_elements* có cùng ý nghĩa như trong :meth:`ElementTree.write`. Trả về một chuỗi chứa dữ liệu XML, được mã hóa tùy chọn.

   .. versionchanged:: 3.4
      Đã thêm tham số *short_empty_elements*.

   .. versionchanged:: 3.8
      Đã thêm các tham số *xml_declaration* và *default_namespace*.

   .. versionchanged:: 3.8
      Hàm :func:`tostring` hiện bảo toàn thứ tự thuộc tính do người dùng chỉ định.


.. function:: tostringlist(element, encoding="us-ascii", method="xml", *, \
                           xml_declaration=None, default_namespace=None, \ short_empty_elements=True)

   Tạo biểu diễn chuỗi của một phần tử XML, bao gồm tất cả các phần tử con. *element* là một instance của :class:`Element`. *encoding* [1]_ là encoding đầu ra (mặc định là US-ASCII). Sử dụng ``encoding="unicode"`` để tạo chuỗi Unicode (nếu không, một bytestring sẽ được tạo). *method* là ``"xml"``, ``"html"`` hoặc ``"text"`` (mặc định là ``"xml"``). *xml_declaration*, *default_namespace* và *short_empty_elements* có cùng ý nghĩa như trong :meth:`ElementTree.write`. Trả về một danh sách các chuỗi chứa dữ liệu XML, có thể được encoding. Không đảm bảo thứ tự cụ thể nào, ngoại trừ ``b"".join(tostringlist(element)) == tostring(element)``.

   .. versionadded:: 3.2

   .. versionchanged:: 3.4
      Đã thêm tham số *short_empty_elements*.

   .. versionchanged:: 3.8
      Đã thêm các tham số *xml_declaration* và *default_namespace*.

   .. versionchanged:: 3.8
      Hàm :func:`tostringlist` hiện bảo toàn thứ tự thuộc tính do người dùng chỉ định.


.. function:: XML(text, parser=None)

   Phân tích một phần XML từ một hằng chuỗi. Hàm này có thể được dùng để nhúng "XML literals" vào mã Python. *text* là một chuỗi chứa dữ liệu XML. *parser* là một parser instance tùy chọn. Nếu không được cung cấp, parser tiêu chuẩn
   :class:`XMLParser` sẽ được sử dụng. Trả về một instance :class:`Element`.


.. function:: XMLID(text, parser=None)

   Phân tích một phần XML từ một hằng chuỗi, đồng thời trả về một dictionary ánh xạ từ id của phần tử đến các phần tử. *text* là một chuỗi chứa dữ liệu XML. *parser* là một parser instance tùy chọn. Nếu không được cung cấp, parser tiêu chuẩn
   :class:`XMLParser` parser được sử dụng. Trả về một tuple chứa một
   instance :class:`Element` và một dictionary.


.. _elementtree-xinclude:

Hỗ trợ XInclude
---------------

Mô-đun này cung cấp hỗ trợ hạn chế cho các chỉ thị `XInclude directives <https://www.w3.org/TR/xinclude/>`_, thông qua mô-đun trợ giúp :mod:`xml.etree.ElementInclude`. Mô-đun này có thể được sử dụng để chèn các cây con và chuỗi văn bản vào cây phần tử, dựa trên thông tin trong cây.

Ví dụ
^^^^^

Sau đây là một ví dụ minh họa cách sử dụng mô-đun XInclude. Để đưa một tài liệu XML vào tài liệu hiện tại, hãy sử dụng phần tử ``{http://www.w3.org/2001/XInclude}include`` và đặt thuộc tính **parse** thành ``"xml"``, đồng thời sử dụng thuộc tính **href** để chỉ định tài liệu cần đưa vào.

.. code-block:: xml

    <?xml version="1.0"?>
    <document xmlns:xi="http://www.w3.org/2001/XInclude">
      <xi:include href="source.xml" parse="xml" />
    </document>

Theo mặc định, thuộc tính **href** được xem là tên tệp. Bạn có thể sử dụng các loader tùy chỉnh để ghi đè hành vi này. Cũng lưu ý rằng trình trợ giúp tiêu chuẩn không hỗ trợ cú pháp XPointer.

Để xử lý tệp này, hãy tải tệp như bình thường rồi truyền phần tử gốc cho module :mod:`!xml.etree.ElementTree`:

.. code-block:: python

   from xml.etree import ElementTree, ElementInclude

   tree = ElementTree.parse("document.xml")
   root = tree.getroot()

   ElementInclude.include(root)

Module ElementInclude thay thế phần tử ``{http://www.w3.org/2001/XInclude}include`` bằng phần tử gốc từ tài liệu **source.xml**. Kết quả có thể trông như sau:

.. code-block:: xml

    <document xmlns:xi="http://www.w3.org/2001/XInclude">
      <para>This is a paragraph.</para>
    </document>

Nếu thuộc tính **parse** bị bỏ qua, giá trị mặc định sẽ là "xml". Thuộc tính href là bắt buộc.

Để đưa vào một tài liệu văn bản, hãy sử dụng phần tử ``{http://www.w3.org/2001/XInclude}include``, rồi đặt thuộc tính **parse** thành "text":

.. code-block:: xml

    <?xml version="1.0"?>
    <document xmlns:xi="http://www.w3.org/2001/XInclude">
      Copyright (c) <xi:include href="year.txt" parse="text" />.
    </document>

Kết quả có thể trông như sau:

.. code-block:: xml

    <document xmlns:xi="http://www.w3.org/2001/XInclude">
      Copyright (c) 2003.
    </document>

Tham khảo
---------

.. _elementinclude-functions:

Hàm
^^^

.. module:: xml.etree.ElementInclude

.. function:: default_loader(href, parse, encoding=None)

   Loader mặc định. Loader mặc định này đọc một resource được include từ đĩa. *href* là một URL. *parse* dùng cho chế độ phân tích cú pháp là "xml" hoặc "text". *encoding* là một encoding văn bản tùy chọn. Nếu không được cung cấp, encoding là ``utf-8``. Trả về resource đã được mở rộng. Nếu chế độ phân tích cú pháp là ``"xml"``, đây là một instance :class:`~xml.etree.ElementTree.Element`. Nếu chế độ phân tích cú pháp là ``"text"``, đây là một chuỗi. Nếu loader không thành công, nó có thể trả về ``None`` hoặc raise một exception.


.. function:: include(elem, loader=None, base_url=None, max_depth=6)

   Hàm này mở rộng các chỉ thị XInclude ngay tại chỗ trong cây được trỏ tới bởi *elem*. *elem* là root :class:`~xml.etree.ElementTree.Element` hoặc một
   instance :class:`~xml.etree.ElementTree.ElementTree` để tìm element như vậy. *loader* là một resource loader tùy chọn. Nếu bỏ qua, giá trị mặc định là :func:`default_loader`. Nếu được cung cấp, nó phải là một callable triển khai cùng interface như
   :func:`default_loader`. *base_url* là URL cơ sở của file gốc, dùng để phân giải các tham chiếu đến file include tương đối. *max_depth* là số lần include đệ quy tối đa. Giới hạn này giúp giảm rủi ro bùng nổ nội dung độc hại. Truyền ``None`` để tắt giới hạn.

   .. versionchanged:: 3.9
      Đã thêm các tham số *base_url* và *max_depth*.


.. _elementtree-element-objects:

Các đối tượng Element
^^^^^^^^^^^^^^^^^^^^^

.. module:: xml.etree.ElementTree
   :noindex:
   :no-index:

.. class:: Element(tag, attrib={}, **extra)

   Lớp Element. Lớp này định nghĩa interface Element và cung cấp một triển khai tham chiếu của interface này.

   *tag* là tên phần tử. *attrib* là một dictionary tùy chọn, chứa các thuộc tính của phần tử. *extra* chứa các thuộc tính bổ sung, được truyền dưới dạng đối số keyword.

   Tên phần tử cùng với tên và giá trị thuộc tính là các chuỗi hoặc
   các instance của :class:`QName`, còn text và tail là các chuỗi hoặc ``None``. Tên phần tử cũng có thể là :func:`Comment` hoặc
   :func:`ProcessingInstruction`, được dùng cho các phần tử đặc biệt. Nếu là ``None``, bản thân phần tử sẽ không được serialize: chỉ text và các phần tử con của nó được ghi, còn các thuộc tính bị bỏ qua. Có thể dùng cách này cho một fragment chứa nhiều phần tử. Với ``method="html"``, giá trị thuộc tính cũng có thể là ``None``, tạo ra một thuộc tính rỗng (chẳng hạn như ``checked``). Có thể lưu các đối tượng khác trong cây, nhưng không thể serialize chúng.

   .. attribute:: tag

      Một chuỗi xác định loại dữ liệu mà phần tử này biểu diễn (nói cách khác, là kiểu phần tử).


   .. attribute:: text
                  tail

      Các thuộc tính này có thể được dùng để lưu trữ dữ liệu bổ sung liên kết với phần tử. Giá trị của chúng thường là các chuỗi, nhưng cũng có thể là bất kỳ đối tượng nào dành riêng cho ứng dụng. Nếu phần tử được tạo từ một tệp XML, thuộc tính *text* chứa text nằm giữa thẻ mở của phần tử và phần tử con hoặc thẻ đóng đầu tiên của nó, hoặc ``None``; còn thuộc tính *tail* chứa text nằm giữa thẻ đóng của phần tử và thẻ tiếp theo, hoặc ``None``. Đối với dữ liệu XML

      .. code-block:: xml

         <a><b>1<c>2<d/>3</c></b>4</a>

      phần tử *a* có ``None`` cho cả thuộc tính *text* và *tail*, phần tử *b* có *text* ``"1"`` và *tail* ``"4"``, phần tử *c* có *text* ``"2"`` và *tail* ``None``, còn phần tử *d* có *text* ``None`` và *tail* ``"3"``.

      Để thu thập văn bản bên trong của một phần tử, hãy xem :meth:`itertext`, ví dụ: ``"".join(element.itertext())``.

      Các ứng dụng có thể lưu trữ các đối tượng tùy ý trong những thuộc tính này.


   .. attribute:: attrib

      Một dictionary chứa các thuộc tính của phần tử. Lưu ý rằng mặc dù giá trị *attrib* luôn là một dictionary Python có thể thay đổi thực sự, một cách triển khai ElementTree có thể chọn sử dụng một biểu diễn nội bộ khác và chỉ tạo dictionary khi có yêu cầu. Để tận dụng các cách triển khai như vậy, hãy sử dụng các phương thức dictionary bên dưới bất cứ khi nào có thể.

   Các phương thức giống dictionary sau đây hoạt động trên các thuộc tính của phần tử.


   .. method:: clear()

      Đặt lại một phần tử. Hàm này xóa tất cả các phần tử con, xóa tất cả các thuộc tính và đặt các thuộc tính text và tail thành ``None``.


   .. method:: get(key, default=None)

      Lấy thuộc tính của phần tử có tên là *key*.

      Trả về giá trị thuộc tính hoặc *default* nếu không tìm thấy thuộc tính.


   .. method:: items()

      Trả về các thuộc tính của element dưới dạng các cặp (name, value).


   .. method:: keys()

      Trả về tên các thuộc tính của element.


   .. method:: set(key, value)

      Đặt thuộc tính *key* của element thành *value*.

   Các phương thức sau đây hoạt động trên các phần tử con (subelements) của element.


   .. method:: append(subelement)

      Thêm element *subelement* vào cuối danh sách nội bộ các phần tử con của element này. Gây ra :exc:`TypeError` nếu *subelement* không phải là một
      :class:`Element`.


   .. method:: extend(subelements)

      Nối *subelements* từ một iterable gồm các element. Gây ra :exc:`TypeError` nếu một phần tử con không phải là một :class:`Element`.

      .. versionadded:: 3.2


   .. method:: find(match, namespaces=None)

      Tìm phần tử con đầu tiên khớp với *match*. *match* có thể là tên thẻ hoặc một :ref:`path <elementtree-xpath>`. Trả về một thực thể phần tử hoặc ``None``. *namespaces* là ánh xạ tùy chọn từ tiền tố namespace đến tên đầy đủ. Truyền ``''`` làm tiền tố để chuyển tất cả tên thẻ không có tiền tố trong biểu thức vào namespace đã cho.


   .. method:: findall(match, namespaces=None)

      Tìm tất cả phần tử con khớp theo tên thẻ hoặc
      :ref:`path <elementtree-xpath>`. Trả về một danh sách chứa tất cả phần tử khớp theo thứ tự trong tài liệu. *namespaces* là ánh xạ tùy chọn từ tiền tố namespace đến tên đầy đủ. Truyền ``''`` làm tiền tố để chuyển tất cả tên thẻ không có tiền tố trong biểu thức vào namespace đã cho.


   .. method:: findtext(match, default=None, namespaces=None)

      Tìm văn bản của phần tử con đầu tiên khớp với *match*. *match* có thể là tên thẻ hoặc một :ref:`path <elementtree-xpath>`. Trả về nội dung văn bản của phần tử khớp đầu tiên hoặc *default* nếu không tìm thấy phần tử nào. Lưu ý rằng nếu phần tử khớp không có nội dung văn bản thì một chuỗi rỗng sẽ được trả về. *namespaces* là ánh xạ tùy chọn từ tiền tố namespace đến tên đầy đủ. Truyền ``''`` làm tiền tố để chuyển tất cả tên thẻ không có tiền tố trong biểu thức vào namespace đã cho.


   .. method:: insert(index, subelement)

      Chèn *subelement* vào vị trí đã cho trong phần tử này. Phát sinh
      :exc:`TypeError` nếu *subelement* không phải là một :class:`Element`.


   .. method:: iter(tag=None)

      Tạo một cây :term:`iterator` với phần tử hiện tại làm gốc. Iterator duyệt qua phần tử này và tất cả phần tử bên dưới nó theo thứ tự trong tài liệu (depth-first). Nếu *tag* không phải là ``None`` hoặc ``'*'``, iterator chỉ trả về các phần tử có thẻ bằng với *tag*. Nếu cấu trúc cây bị sửa đổi trong quá trình lặp, kết quả không được xác định.

      .. versionadded:: 3.2


   .. method:: iterfind(match, namespaces=None)

      Tìm tất cả phần tử con khớp theo tên thẻ hoặc
      :ref:`path <elementtree-xpath>`.  Trả về một iterable lần lượt cung cấp tất cả các phần tử khớp theo thứ tự trong tài liệu. *namespaces* là một ánh xạ tùy chọn từ tiền tố namespace đến tên đầy đủ.


      .. versionadded:: 3.2


   .. method:: itertext()

      Tạo một trình lặp văn bản. Trình lặp duyệt qua phần tử này và tất cả các phần tử con theo thứ tự trong tài liệu, đồng thời trả về toàn bộ văn bản bên trong.

      .. versionadded:: 3.2


   .. method:: makeelement(tag, attrib)

      Tạo một đối tượng phần tử mới có cùng kiểu với phần tử này. Không gọi phương thức này; thay vào đó, hãy sử dụng hàm factory :func:`SubElement`.


   .. method:: remove(subelement)

      Xóa *subelement* khỏi phần tử. Không giống các phương thức find\*, phương thức này so sánh các phần tử dựa trên danh tính của instance, không dựa trên giá trị thẻ hoặc nội dung.

   Các đối tượng :class:`Element` cũng hỗ trợ các phương thức kiểu sequence sau đây để làm việc với các phần tử con: :meth:`~object.__delitem__`,
   :meth:`~object.__getitem__`, :meth:`~object.__setitem__`,
   :meth:`~object.__len__`.

   Cảnh báo: Các phần tử không có phần tử con sẽ được đánh giá là ``False``. Trong một bản phát hành tương lai của Python, tất cả các phần tử sẽ được đánh giá là ``True`` bất kể có phần tử con hay không. Thay vào đó, nên ưu tiên các phép kiểm tra ``len(elem)`` hoặc ``elem is not None`` tường minh.::

     element = root.find('foo')

     if not element:  # cẩn thận!
         print("element not found, or element has no subelements")

     if element is None:
         print("element not found")

   .. versionchanged:: 3.12
      Việc kiểm tra giá trị truth của một Element sẽ phát ra :exc:`DeprecationWarning`.

   Trước Python 3.8, thứ tự serialisation của các thuộc tính XML của các phần tử được sắp xếp theo tên thuộc tính để tạo ra thứ tự có thể dự đoán một cách nhân tạo. Dựa trên thứ tự hiện đã được đảm bảo của dict, việc sắp xếp lại tùy ý này đã bị loại bỏ trong Python 3.8 để giữ nguyên thứ tự mà các thuộc tính được phân tích cú pháp ban đầu hoặc được tạo bởi mã người dùng.

   Nhìn chung, mã người dùng không nên phụ thuộc vào một thứ tự thuộc tính cụ thể, vì `Bộ thông tin XML <https://www.w3.org/TR/xml-infoset/>`_ nêu rõ rằng thứ tự thuộc tính không truyền tải thông tin. Mã phải sẵn sàng xử lý mọi thứ tự khi đầu vào. Trong các trường hợp cần đầu ra XML xác định, chẳng hạn như để ký mật mã hoặc tạo các tập dữ liệu kiểm thử, có thể sử dụng canonical serialisation với hàm :func:`canonicalize`.

   Trong các trường hợp không thể áp dụng đầu ra canonical nhưng vẫn mong muốn có một thứ tự thuộc tính cụ thể ở đầu ra, mã nên cố gắng tạo các thuộc tính trực tiếp theo thứ tự mong muốn để tránh gây lệch nhận thức cho người đọc mã. Khi khó thực hiện điều này, có thể áp dụng một recipe như sau trước khi serialisation để áp đặt thứ tự độc lập với việc tạo Element::

     def reorder_attributes(root):
         for el in root.iter():
             attrib = el.attrib
             if len(attrib) > 1:
                 # điều chỉnh thứ tự thuộc tính, chẳng hạn bằng cách sắp xếp
                 attribs = sorted(attrib.items())
                 attrib.clear()
                 attrib.update(attribs)


.. _elementtree-elementtree-objects:

Đối tượng ElementTree
^^^^^^^^^^^^^^^^^^^^^


.. class:: ElementTree(element=None, file=None)

   Lớp wrapper ElementTree. Lớp này đại diện cho toàn bộ hệ phân cấp phần tử và bổ sung một số hỗ trợ cho việc tuần tự hóa từ và sang XML tiêu chuẩn.

   *element* là phần tử gốc. Cây được khởi tạo với nội dung của *file* XML nếu được cung cấp.


   .. method:: _setroot(element)

      Thay thế phần tử gốc của cây này. Thao tác này loại bỏ nội dung hiện tại của cây và thay thế bằng phần tử đã cho. Hãy sử dụng cẩn thận. *element* là một thực thể phần tử.


   .. method:: find(match, namespaces=None)

      Giống như :meth:`Element.find`, bắt đầu từ gốc của cây.


   .. method:: findall(match, namespaces=None)

      Giống như :meth:`Element.findall`, bắt đầu từ gốc của cây.


   .. method:: findtext(match, default=None, namespaces=None)

      Giống như :meth:`Element.findtext`, bắt đầu từ gốc của cây.


   .. method:: getroot()

      Trả về phần tử gốc của cây này.


   .. method:: iter(tag=None)

      Tạo và trả về một tree iterator cho phần tử gốc. Iterator lặp qua tất cả các phần tử trong cây này theo thứ tự section. *tag* là tag cần tìm (mặc định là trả về tất cả các phần tử).


   .. method:: iterfind(match, namespaces=None)

      Giống như :meth:`Element.iterfind`, bắt đầu từ gốc của cây.

      .. versionadded:: 3.2


   .. method:: parse(source, parser=None)

      Tải một section XML bên ngoài vào element tree này. *source* là tên tệp hoặc :term:`file object`. *parser* là một parser instance tùy chọn. Nếu không được cung cấp, parser :class:`XMLParser` tiêu chuẩn sẽ được sử dụng. Trả về phần tử gốc của section.


   .. method:: write(file, encoding="us-ascii", xml_declaration=None, \
                     default_namespace=None, method="xml", *, \ short_empty_elements=True)

      Ghi element tree vào một tệp dưới dạng XML. *file* là tên tệp hoặc một
      :term:`file object` được mở để ghi. *encoding* [1]_ là encoding đầu ra (mặc định là US-ASCII). *xml_declaration* kiểm soát việc có thêm khai báo XML vào tệp hay không. Sử dụng ``False`` để không bao giờ thêm, ``True`` để luôn thêm, ``None`` để chỉ thêm nếu không phải US-ASCII, UTF-8 hoặc Unicode (mặc định là ``None``). *default_namespace* đặt namespace XML mặc định (cho "xmlns"). *method* là ``"xml"``, ``"html"`` hoặc ``"text"`` (mặc định là ``"xml"``). Tham số chỉ có keyword *short_empty_elements* kiểm soát cách định dạng các phần tử không chứa nội dung. Nếu là ``True`` (mặc định), chúng được xuất ra dưới dạng một tag tự đóng duy nhất; nếu không, chúng được xuất ra dưới dạng một cặp tag bắt đầu/kết thúc.

      Đầu ra có thể là một chuỗi (:class:`str`) hoặc dạng nhị phân (:class:`bytes`). Điều này được kiểm soát bởi đối số *encoding*. Nếu *encoding* là ``"unicode"``, đầu ra là một chuỗi; nếu không, đầu ra là dạng nhị phân. Lưu ý rằng điều này có thể xung đột với kiểu của *file* nếu đó là một
      :term:`file object`; hãy đảm bảo bạn không cố ghi một chuỗi vào luồng nhị phân và ngược lại.

      .. versionchanged:: 3.4
         Đã thêm tham số *short_empty_elements*.

      .. versionchanged:: 3.8
         Phương thức :meth:`write` hiện bảo toàn thứ tự thuộc tính do người dùng chỉ định.


Đây là tệp XML sẽ được thao tác::

    <html>
        <head>
            <title>Example page</title>
        </head>
        <body>
            <p>Moved to <a href="http://example.org/">example.org</a>
            or <a href="http://example.com/">example.com</a>.</p>
        </body>
    </html>

Ví dụ về việc thay đổi thuộc tính "target" của mọi liên kết trong đoạn đầu tiên::

    >>> from xml.etree.ElementTree import ElementTree
    >>> tree = ElementTree()
    >>> tree.parse("index.xhtml")
    <Element 'html' at 0xb77e6fac>
    >>> p = tree.find("body/p")     # Tìm lần xuất hiện đầu tiên của thẻ p trong body
    >>> p
    <Element 'p' at 0xb77ec26c>
    >>> links = list(p.iter("a"))   # Trả về danh sách tất cả các liên kết
    >>> links
    [<Element 'a' at 0xb77ec2ac>, <Element 'a' at 0xb77ec1cc>]
    >>> for i in links:             # Lặp qua tất cả các liên kết được tìm thấy
    ...     i.attrib["target"] = "blank"
    ...
    >>> tree.write("output.xhtml")

.. _elementtree-qname-objects:

Đối tượng QName
^^^^^^^^^^^^^^^


.. class:: QName(text_or_uri, tag=None)

   Trình bao bọc QName. Có thể dùng trình bao bọc này để bao bọc một giá trị thuộc tính QName nhằm xử lý namespace chính xác khi xuất. *text_or_uri* là một chuỗi chứa giá trị QName ở dạng {uri}local hoặc, nếu cung cấp đối số tag, là phần URI của một QName. Nếu cung cấp *tag*, đối số đầu tiên được hiểu là URI và đối số này được hiểu là tên cục bộ.
   Các thực thể :class:`QName` là dạng không công khai.



.. _elementtree-treebuilder-objects:

Đối tượng TreeBuilder
^^^^^^^^^^^^^^^^^^^^^


.. class:: TreeBuilder(element_factory=None, *, comment_factory=None, \
                       pi_factory=None, insert_comments=False, insert_pis=False)

   Trình dựng cấu trúc phần tử tổng quát. Trình dựng này chuyển đổi một chuỗi các lệnh gọi phương thức start, data, end, comment và pi thành một cấu trúc phần tử hợp lệ. Bạn có thể dùng lớp này để dựng cấu trúc phần tử bằng trình phân tích XML tùy chỉnh hoặc trình phân tích cho một định dạng giống XML khác.

   *element_factory*, nếu được cung cấp, phải là một callable nhận hai đối số positional: một tag và một dict thuộc tính. Callable này được kỳ vọng sẽ trả về một instance phần tử mới.

   Các hàm *comment_factory* và *pi_factory*, nếu được cung cấp, phải hoạt động giống như các hàm :func:`Comment` và :func:`ProcessingInstruction` để tạo comment và processing instruction. Nếu không được cung cấp, các factory mặc định sẽ được sử dụng. Khi *insert_comments* và/hoặc *insert_pis* là true, comment/pis sẽ được chèn vào cây nếu chúng xuất hiện bên trong phần tử gốc (nhưng không ở bên ngoài phần tử đó).

   .. method:: close()

      Flush các bộ đệm của builder và trả về phần tử tài liệu toplevel. Trả về một instance :class:`Element`.


   .. method:: data(data)

      Thêm văn bản vào phần tử hiện tại. *data* là một chuỗi.


   .. method:: end(tag)

      Đóng phần tử hiện tại. *tag* là tên phần tử. Trả về phần tử đã đóng.


   .. method:: start(tag, attrs)

      Mở một phần tử mới. *tag* là tên phần tử. *attrs* là một dictionary chứa các thuộc tính của phần tử. Trả về phần tử đã mở.


   .. method:: comment(text)

      Tạo một comment với *text* đã cho. Nếu ``insert_comments`` là true, comment này cũng sẽ được thêm vào cây.

      .. versionadded:: 3.8


   .. method:: pi(target, text)

      Tạo một chỉ thị xử lý với tên *target* đã cho và *text*. Nếu ``insert_pis`` là true, chỉ thị này cũng sẽ được thêm vào cây.

      .. versionadded:: 3.8


   Ngoài ra, một đối tượng :class:`TreeBuilder` tùy chỉnh có thể cung cấp các phương thức sau:

   .. method:: doctype(name, pubid, system)

      Xử lý khai báo doctype. *name* là tên doctype. *pubid* là public identifier. *system* là system identifier. Phương thức này không tồn tại trên lớp :class:`TreeBuilder` mặc định.

      .. versionadded:: 3.2

   .. method:: start_ns(prefix, uri)

      Được gọi mỗi khi parser gặp một khai báo namespace mới, trước callback ``start()`` cho phần tử mở xác định namespace đó. *prefix* là ``''`` đối với namespace mặc định và là tên prefix của namespace được khai báo trong các trường hợp khác. *uri* là URI của namespace.

      .. versionadded:: 3.8

   .. method:: end_ns(prefix)

      Được gọi sau callback ``end()`` của một phần tử đã khai báo ánh xạ prefix của namespace, với tên *prefix* đã không còn trong phạm vi.

      .. versionadded:: 3.8


.. class:: C14NWriterTarget(write, *, \
             with_comments=False, strip_text=False, rewrite_prefixes=False, \ qname_aware_tags=None, qname_aware_attrs=None, \ exclude_attrs=None, exclude_tags=None)

   Một writer `C14N 2.0 <https://www.w3.org/TR/xml-c14n2/>`_. Các đối số giống như của hàm :func:`canonicalize`. Lớp này không xây dựng cây mà chuyển trực tiếp các sự kiện callback thành dạng được tuần tự hóa bằng hàm *write*.

   .. versionadded:: 3.8


.. _elementtree-xmlparser-objects:

Đối tượng XMLParser
^^^^^^^^^^^^^^^^^^^


.. class:: XMLParser(*, target=None, encoding=None)

   Lớp này là khối xây dựng cấp thấp của module. Lớp sử dụng
   :mod:`xml.parsers.expat` để phân tích XML theo sự kiện một cách hiệu quả. Bạn có thể cung cấp dần dữ liệu XML bằng phương thức :meth:`feed`, và các sự kiện phân tích được chuyển thành push API bằng cách gọi các callback trên đối tượng *target*. Nếu bỏ qua *target*, :class:`TreeBuilder` tiêu chuẩn sẽ được sử dụng. Nếu cung cấp *encoding* [1]_, giá trị này sẽ ghi đè encoding được chỉ định trong tệp XML.

   .. versionchanged:: 3.8
      Các tham số hiện chỉ có thể được truyền dưới dạng :ref:`keyword-only <keyword-only_parameter>`. Đối số *html* không còn được hỗ trợ.


   .. method:: close()

      Kết thúc việc cung cấp dữ liệu cho parser. Trả về kết quả của việc gọi phương thức ``close()`` của đối tượng *target* được truyền khi khởi tạo; theo mặc định, đây là phần tử tài liệu cấp cao nhất.


   .. method:: feed(data)

      Cung cấp dữ liệu cho parser. *data* là một chuỗi hoặc dữ liệu đã được mã hóa (:class:`bytes` hoặc một :term:`bytes-like object`).


   .. method:: flush()

      Kích hoạt việc phân tích mọi dữ liệu chưa được phân tích đã cung cấp trước đó, có thể dùng để đảm bảo nhận được phản hồi nhanh hơn, đặc biệt với Expat >=2.6.0. Việc triển khai :meth:`flush` tạm thời vô hiệu hóa cơ chế trì hoãn phân tích lại với Expat (nếu hiện đang được bật) và kích hoạt phân tích lại. Việc vô hiệu hóa cơ chế trì hoãn phân tích lại có các hệ quả về bảo mật; vui lòng xem
      :meth:`xml.parsers.expat.xmlparser.SetReparseDeferralEnabled` để biết thêm chi tiết.

      Lưu ý rằng :meth:`flush` đã được backport vào một số bản phát hành trước đây của CPython như một bản sửa lỗi bảo mật. Kiểm tra tính khả dụng của :meth:`flush` bằng :func:`hasattr` nếu được sử dụng trong code chạy trên nhiều phiên bản Python khác nhau.

      .. versionadded:: 3.13


   :meth:`XMLParser.feed` gọi *target*\'s ``start(tag, attrs_dict)`` method cho mỗi thẻ mở, method ``end(tag)`` cho mỗi thẻ đóng, còn dữ liệu được xử lý bởi method ``data(data)``. Để xem các callback method được hỗ trợ khác, hãy tham khảo class :class:`TreeBuilder`. :meth:`XMLParser.close` gọi method *target*\'s ``close()``. :class:`XMLParser` không chỉ được dùng để xây dựng cấu trúc cây. Đây là ví dụ về cách đếm độ sâu tối đa của một tệp XML::

    >>> from xml.etree.ElementTree import XMLParser
    >>> class MaxDepth:                     # Đối tượng target của parser
    ...     maxDepth = 0
    ...     depth = 0
    ...     def start(self, tag, attrib):   # Được gọi cho mỗi thẻ mở.
    ...         self.depth += 1
    ...         if self.depth > self.maxDepth:
    ...             self.maxDepth = self.depth
    ...     def end(self, tag):             # Được gọi cho mỗi thẻ đóng.
    ...         self.depth -= 1
    ...     def data(self, data):
    ...         pass            # Chúng ta không cần làm gì với dữ liệu.
    ...     def close(self):    # Được gọi khi tất cả dữ liệu đã được phân tích cú pháp.
    ...         return self.maxDepth
    ...
    >>> target = MaxDepth()
    >>> parser = XMLParser(target=target)
    >>> exampleXml = """
    ... <a>
    ...   <b>
    ...   </b>
    ...   <b>
    ...     <c>
    ...       <d>
    ...       </d>
    ...     </c>
    ...   </b>
    ... </a>"""
    >>> parser.feed(exampleXml)
    >>> parser.close()
    4


.. _elementtree-xmlpullparser-objects:

Đối tượng XMLPullParser
^^^^^^^^^^^^^^^^^^^^^^^

.. class:: XMLPullParser(events=None)

   Một pull parser phù hợp với các ứng dụng không chặn. API ở phía đầu vào của nó tương tự như :class:`XMLParser`, nhưng thay vì đẩy các lệnh gọi đến một callback target, :class:`XMLPullParser` thu thập một danh sách nội bộ các sự kiện phân tích cú pháp và cho phép người dùng đọc từ danh sách đó. *events* là một chuỗi các sự kiện cần báo cáo lại. Các sự kiện được hỗ trợ là các chuỗi ``"start"``, ``"end"``, ``"comment"``, ``"pi"``, ``"start-ns"`` và ``"end-ns"`` (các sự kiện "ns" được dùng để lấy thông tin namespace chi tiết). Nếu bỏ qua *events*, chỉ các sự kiện ``"end"`` được báo cáo.

   .. method:: feed(data)

      Cung cấp dữ liệu đã cho cho parser. *data* là một chuỗi hoặc dữ liệu đã mã hóa (:class:`bytes` hoặc một :term:`bytes-like object`).

   .. method:: flush()

      Kích hoạt việc phân tích cú pháp mọi dữ liệu chưa được phân tích cú pháp đã được cung cấp trước đó, có thể được dùng để đảm bảo phản hồi nhanh hơn, đặc biệt với Expat >=2.6.0. Việc triển khai :meth:`flush` tạm thời vô hiệu hóa việc trì hoãn phân tích lại với Expat (nếu hiện đang được bật) và kích hoạt phân tích lại. Việc vô hiệu hóa trì hoãn phân tích lại có những hệ quả về bảo mật; vui lòng xem
      :meth:`xml.parsers.expat.xmlparser.SetReparseDeferralEnabled` để biết chi tiết.

      Lưu ý rằng :meth:`flush` đã được backport vào một số bản phát hành trước đó của CPython dưới dạng bản sửa lỗi bảo mật. Hãy kiểm tra tính khả dụng của :meth:`flush` bằng :func:`hasattr` nếu mã được chạy trên nhiều phiên bản Python khác nhau.

      .. versionadded:: 3.13

   .. method:: close()

      Báo hiệu cho parser rằng luồng dữ liệu đã kết thúc. Không giống như
      :meth:`XMLParser.close`, phương thức này luôn trả về :const:`None`. Mọi sự kiện chưa được truy xuất khi parser bị đóng vẫn có thể được đọc bằng :meth:`read_events`.

   .. method:: read_events()

      Trả về một iterator trên các sự kiện đã xuất hiện trong dữ liệu được cung cấp cho parser. Iterator này trả về các cặp ``(event, elem)``, trong đó *event* là một chuỗi biểu thị loại sự kiện (ví dụ: ``"end"``) và *elem* là đối tượng :class:`Element` được gặp, hoặc giá trị ngữ cảnh khác như sau.

      * ``start``, ``end``: Element hiện tại.
      * ``comment``, ``pi``: chú thích / chỉ thị xử lý hiện tại
      * ``start-ns``: một tuple ``(prefix, uri)`` có tên là ánh xạ namespace đã khai báo.
      * ``end-ns``: :const:`None` (điều này có thể thay đổi trong phiên bản tương lai)

      Các sự kiện được cung cấp trong một lần gọi trước đó đến :meth:`read_events` sẽ không được cung cấp lại. Các sự kiện chỉ được lấy khỏi hàng đợi nội bộ khi chúng được truy xuất từ iterator, vì vậy việc nhiều trình đọc lặp song song trên các iterator nhận được từ :meth:`read_events` sẽ cho kết quả không thể dự đoán.

   .. note::

      :class:`XMLPullParser` chỉ đảm bảo rằng nó đã gặp ký tự ">" của thẻ bắt đầu khi phát ra sự kiện "start", vì vậy các thuộc tính đã được xác định, nhưng nội dung của các thuộc tính text và tail tại thời điểm đó là không xác định. Điều tương tự cũng áp dụng cho các phần tử con; chúng có thể đã hoặc chưa xuất hiện.

      Nếu bạn cần một phần tử được điền đầy đủ, hãy tìm các sự kiện "end" thay thế.

   .. versionadded:: 3.4

   .. versionchanged:: 3.8
      Các sự kiện ``comment`` và ``pi`` đã được thêm vào.


Ngoại lệ
^^^^^^^^

.. class:: ParseError

   Lỗi phân tích cú pháp XML, được phát sinh bởi nhiều phương thức phân tích cú pháp trong mô-đun này khi việc phân tích cú pháp không thành công. Biểu diễn chuỗi của một экземпляар ngoại lệ này sẽ chứa thông báo lỗi thân thiện với người dùng. Ngoài ra, nó sẽ có các thuộc tính sau:

   .. attribute:: code

      Mã lỗi dạng số từ trình phân tích cú pháp expat. Xem tài liệu của
      :mod:`xml.parsers.expat` để xem danh sách mã lỗi và ý nghĩa của chúng.

   .. attribute:: position

      Một tuple gồm các số *dòng*, *cột*, chỉ rõ nơi xảy ra lỗi.

.. rubric:: Chú thích

.. [1] Chuỗi encoding được đưa vào đầu ra XML phải tuân thủ các tiêu chuẩn thích hợp. Ví dụ: "UTF-8" là hợp lệ, nhưng "UTF8" thì không. Xem https://www.w3.org/TR/2006/REC-xml11-20060816/#NT-EncodingDecl và https://www.iana.org/assignments/character-sets/character-sets.xhtml.

.. _`XPath expressions`: https://www.w3.org/TR/xpath
.. _`C14N 2.0`: https://www.w3.org/TR/xml-c14n2/
.. _`XInclude directives`: https://www.w3.org/TR/xinclude/
.. _`XML Information Set`: https://www.w3.org/TR/xml-infoset/
