:mod:`!xmlrpc.client` --- Truy cập client XML-RPC
=================================================

.. module:: xmlrpc.client
   :synopsis: Truy cập client XML-RPC.

.. moduleauthor:: Fredrik Lundh <fredrik@pythonware.com>
.. sectionauthor:: Eric S. Raymond <esr@snark.thyrsus.com>

**Mã nguồn:** :source:`Lib/xmlrpc/client.py`

.. XXX Not everything is documented yet.  It might be good to describe
   Marshaller, Unmarshaller, getparser and Transport.

--------------

XML-RPC là một phương thức Remote Procedure Call sử dụng XML được truyền qua HTTP(S) làm phương tiện truyền tải. Với phương thức này, client có thể gọi các phương thức kèm tham số trên một máy chủ từ xa (máy chủ được xác định bằng một URI) và nhận lại dữ liệu có cấu trúc. Mô-đun này hỗ trợ viết mã client XML-RPC; mô-đun xử lý mọi chi tiết của việc chuyển đổi giữa các đối tượng Python tương thích và XML trên đường truyền.


.. warning::

   Mô-đun :mod:`!xmlrpc.client` không an toàn trước dữ liệu được tạo nhằm mục đích xấu. Nếu bạn cần phân tích dữ liệu không đáng tin cậy hoặc chưa được xác thực, hãy xem :ref:`xml-security`.

.. versionchanged:: 3.5

   Đối với các URI HTTPS, :mod:`!xmlrpc.client` hiện thực hiện tất cả các bước kiểm tra chứng chỉ và hostname cần thiết theo mặc định.

.. include:: ../includes/wasm-notavail.rst

.. class:: ServerProxy(uri, transport=None, encoding=None, verbose=False, \
                       allow_none=False, use_datetime=False, \ use_builtin_types=False, *, headers=(), context=None)

   Một instance :class:`ServerProxy` là một đối tượng quản lý việc giao tiếp với máy chủ XML-RPC từ xa. Đối số đầu tiên bắt buộc là một URI (Uniform Resource Indicator), và thông thường sẽ là URL của máy chủ. Đối số thứ hai tùy chọn là một instance của transport factory; theo mặc định, đó là một đối tượng nội bộ
   :class:`SafeTransport` cho các URL https: và một đối tượng HTTP nội bộ
   :class:`Transport` trong các trường hợp khác. Đối số thứ ba tùy chọn là encoding, mặc định là UTF-8. Đối số thứ tư tùy chọn là một cờ debugging.

   Các tham số sau đây chi phối việc sử dụng instance proxy được trả về. Nếu *allow_none* là true, hằng số Python ``None`` sẽ được chuyển thành XML; hành vi mặc định là ``None`` sẽ raise một :exc:`TypeError`. Đây là một phần mở rộng thường được sử dụng của đặc tả XML-RPC, nhưng không được tất cả client và server hỗ trợ; xem `http://ontosys.com/xml-rpc/extensions.php <https://web.archive.org/web/20130120074804/http://ontosys.com/xml-rpc/extensions.php>`_ để biết mô tả. Cờ *use_builtin_types* có thể được dùng để khiến các giá trị ngày/giờ được biểu diễn dưới dạng đối tượng :class:`datetime.datetime` và dữ liệu nhị phân được biểu diễn dưới dạng đối tượng :class:`bytes`; theo mặc định, cờ này là false.
   Các đối tượng :class:`datetime.datetime`, :class:`bytes` và :class:`bytearray` có thể được truyền vào các lệnh gọi. Tham số *headers* là một dãy tùy chọn các header HTTP sẽ được gửi cùng mỗi request, được biểu diễn dưới dạng một dãy các bộ 2-tuple đại diện cho tên và giá trị của header. (ví dụ: ``[('Header-Name', 'value')]``). Nếu cung cấp URL HTTPS, *context* có thể là :class:`ssl.SSLContext` và cấu hình các thiết lập SSL của kết nối HTTPS bên dưới. Cờ lỗi thời *use_datetime* tương tự như *use_builtin_types* nhưng chỉ áp dụng cho các giá trị ngày/giờ.

   .. versionchanged:: 3.3
      Cờ *use_builtin_types* đã được thêm.

   .. versionchanged:: 3.8
      Tham số *headers* đã được thêm.

   Cả transport HTTP và HTTPS đều hỗ trợ phần mở rộng cú pháp URL cho Basic Authentication của HTTP: ``http://user:pass@host:port/path``. Phần ``user:pass`` sẽ được mã hóa bằng base64 dưới dạng header HTTP 'Authorization' và được gửi đến máy chủ từ xa như một phần của quá trình kết nối khi gọi một phương thức XML-RPC. Bạn chỉ cần sử dụng tính năng này nếu máy chủ từ xa yêu cầu tên người dùng và mật khẩu để Basic Authentication.

   Instance được trả về là một proxy object có các phương thức có thể được dùng để gọi các RPC tương ứng trên máy chủ từ xa. Nếu máy chủ từ xa hỗ trợ introspection API, proxy cũng có thể được dùng để truy vấn máy chủ từ xa về các phương thức mà máy chủ hỗ trợ (service discovery) và lấy các metadata khác liên kết với máy chủ.

   Các kiểu dữ liệu tương thích (ví dụ: có thể được marshal qua XML) bao gồm những kiểu sau (trừ khi có ghi chú khác, chúng sẽ được unmarshal thành cùng kiểu Python):

   .. tabularcolumns:: |l|L|

   +-------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | Kiểu XML-RPC                                                | Kiểu Python                                                                                                                                                  |
   +=============================================================+==============================================================================================================================================================+
   | ``boolean``                                                 | :class:`bool`                                                                                                                                                |
   +-------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``int``, ``i1``, ``i2``, ``i4``, ``i8`` hoặc ``biginteger`` | :class:`int` trong phạm vi từ -2147483648 đến 2147483647. Các giá trị nhận thẻ ``<int>``.                                                                    |
   +-------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``double`` hoặc ``float``                                   | :class:`float`. Giá trị được gắn thẻ ``<double>``.                                                                                                           |
   +-------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``string``                                                  | :class:`str`                                                                                                                                                 |
   +-------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``array``                                                   | :class:`list` hoặc :class:`tuple` chứa các phần tử tương thích. Các mảng được trả về dưới dạng                                                               |
   |                                                             | :class:`lists <list>`.                                                                                                                                       |
   +-------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``struct``                                                  | :class:`dict`. Khóa phải là chuỗi, còn giá trị có thể thuộc bất kỳ kiểu tương thích nào. Có thể truyền các đối tượng thuộc lớp do người dùng định nghĩa; chỉ |
   |                                                             | :attr:`~object.__dict__` của chúng được truyền đi.                                                                                                           |
   +-------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``dateTime.iso8601``                                        | :class:`DateTime` hoặc :class:`datetime.datetime`. Kiểu được trả về phụ thuộc vào giá trị của các cờ *use_builtin_types* và *use_datetime*.                  |
   +-------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``base64``                                                  | :class:`Binary`, :class:`bytes` hoặc                                                                                                                         |
   |                                                             | :class:`bytearray`. Kiểu trả về phụ thuộc vào cờ *use_builtin_types*.                                                                                        |
   +-------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``nil``                                                     | Hằng số ``None``. Chỉ được phép truyền vào nếu *allow_none* là true.                                                                                         |
   +-------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+
   | ``bigdecimal``                                              | :class:`decimal.Decimal`. Chỉ có kiểu trả về.                                                                                                                |
   +-------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+

   Đây là toàn bộ các kiểu dữ liệu được XML-RPC hỗ trợ. Các lệnh gọi phương thức cũng có thể đưa ra một thể hiện :exc:`Fault` đặc biệt, được dùng để báo hiệu lỗi của máy chủ XML-RPC, hoặc
   :exc:`ProtocolError` được dùng để báo hiệu lỗi trong tầng truyền tải HTTP/HTTPS. Cả :exc:`Fault` và :exc:`ProtocolError` đều kế thừa từ một lớp cơ sở có tên là
   :exc:`Error`. Lưu ý rằng mô-đun xmlrpc client hiện không marshal các thể hiện của lớp con của các kiểu dựng sẵn.

   Khi truyền chuỗi, các ký tự đặc biệt đối với XML như ``<``, ``>`` và ``&`` sẽ tự động được escape. Tuy nhiên, người gọi có trách nhiệm đảm bảo chuỗi không chứa các ký tự không được XML cho phép, chẳng hạn như các ký tự điều khiển có giá trị ASCII từ 0 đến 31 (tất nhiên, ngoại trừ tab, dòng mới và ký tự xuống dòng); nếu không, kết quả sẽ là một yêu cầu XML-RPC không phải là XML đúng định dạng. Nếu cần truyền các byte tùy ý qua XML-RPC, hãy sử dụng các lớp :class:`bytes` hoặc :class:`bytearray` hoặc
   :class:`Binary` lớp wrapper được mô tả dưới đây.

   :class:`Server` được giữ lại làm bí danh cho :class:`ServerProxy` để tương thích ngược. Mã mới nên sử dụng :class:`ServerProxy`.

   .. versionchanged:: 3.5
      Đã bổ sung đối số *context*.

   .. versionchanged:: 3.6
      Đã bổ sung hỗ trợ các thẻ kiểu có tiền tố (ví dụ: ``ex:nil``). Đã bổ sung hỗ trợ giải mã các kiểu bổ sung được triển khai Apache XML-RPC sử dụng cho các giá trị số: ``i1``, ``i2``, ``i8``, ``biginteger``, ``float`` và ``bigdecimal``. Xem https://ws.apache.org/xmlrpc/types.html để biết mô tả.


.. seealso::

   `XML-RPC HOWTO <https://tldp.org/HOWTO/XML-RPC-HOWTO/index.html>`_
      Mô tả hữu ích về hoạt động của XML-RPC và phần mềm client bằng một số ngôn ngữ. Tài liệu này chứa gần như mọi thông tin mà nhà phát triển client XML-RPC cần biết.

   `XML-RPC Introspection <https://xmlrpc-c.sourceforge.io/introspection.html>`_
      Mô tả phần mở rộng giao thức XML-RPC để introspection.

   `Đặc tả XML-RPC <http://xmlrpc.scripting.com/spec.html>`_
      Đặc tả chính thức.

.. _serverproxy-objects:

Các đối tượng ServerProxy
-------------------------

Một instance :class:`ServerProxy` có một phương thức tương ứng với mỗi lệnh gọi thủ tục từ xa được máy chủ XML-RPC chấp nhận. Việc gọi phương thức sẽ thực hiện một RPC, được phân phối dựa trên cả tên và chữ ký tham số (ví dụ: cùng một tên phương thức có thể được nạp chồng với nhiều chữ ký tham số). RPC kết thúc bằng cách trả về một giá trị, có thể là dữ liệu được trả về thuộc một kiểu phù hợp hoặc một
đối tượng :class:`Fault` hoặc :class:`ProtocolError` cho biết đã xảy ra lỗi.

Các máy chủ hỗ trợ API introspection của XML sẽ hỗ trợ một số phương thức phổ biến được nhóm dưới thuộc tính dành riêng :attr:`~ServerProxy.system`:


.. method:: ServerProxy.system.listMethods()

   Phương thức này trả về một danh sách chuỗi, mỗi chuỗi tương ứng với một phương thức (không thuộc hệ thống) được máy chủ XML-RPC hỗ trợ.


.. method:: ServerProxy.system.methodSignature(name)

   Phương thức này nhận một tham số là tên của một phương thức được máy chủ XML-RPC triển khai. Phương thức trả về một mảng gồm các signature khả dĩ của phương thức này. Một signature là một mảng các kiểu. Kiểu đầu tiên là kiểu trả về của phương thức, các kiểu còn lại là các tham số.

   Vì cho phép có nhiều signature (tức là overloading), phương thức này trả về một danh sách các signature thay vì một giá trị đơn.

   Bản thân các signature chỉ giới hạn ở những tham số cấp cao nhất mà một phương thức yêu cầu. Ví dụ, nếu một phương thức yêu cầu một mảng các struct làm tham số và trả về một chuỗi, signature của nó đơn giản là "string, array". Nếu phương thức yêu cầu ba số nguyên và trả về một chuỗi, signature của nó là "string, int, int, int".

   Nếu không có signature nào được định nghĩa cho phương thức, một giá trị không phải mảng sẽ được trả về. Trong Python, điều này có nghĩa là kiểu của giá trị được trả về sẽ khác với list.


.. method:: ServerProxy.system.methodHelp(name)

   Phương thức này nhận một tham số là tên của một phương thức được máy chủ XML-RPC triển khai. Phương thức trả về một chuỗi tài liệu mô tả cách sử dụng phương thức đó. Nếu không có chuỗi như vậy, một chuỗi rỗng sẽ được trả về. Chuỗi tài liệu có thể chứa markup HTML.

.. versionchanged:: 3.5

   Các thể hiện của :class:`ServerProxy` hỗ trợ giao thức :term:`context manager` để đóng transport bên dưới.


Sau đây là một ví dụ hoạt động. Mã server::

   from xmlrpc.server import SimpleXMLRPCServer

   def is_even(n):
       return n % 2 == 0

   server = SimpleXMLRPCServer(("localhost", 8000))
   print("Listening on port 8000...")
   server.register_function(is_even, "is_even")
   server.serve_forever()

Mã client cho server ở trên::

   import xmlrpc.client

   with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy:
       print("3 is even: %s" % str(proxy.is_even(3)))
       print("100 is even: %s" % str(proxy.is_even(100)))

.. _datetime-objects:

Đối tượng DateTime
------------------

.. class:: DateTime

   Có thể khởi tạo lớp này bằng số giây kể từ epoch, một time tuple, chuỗi thời gian/ngày tháng theo chuẩn ISO 8601 hoặc một đối tượng :class:`datetime.datetime`. Lớp này có các phương thức sau, chủ yếu được hỗ trợ để mã marshalling/unmarshalling sử dụng nội bộ:


   .. method:: decode(string)

      Chấp nhận một chuỗi làm giá trị thời gian mới của instance.


   .. method:: encode(out)

      Ghi phần mã hóa XML-RPC của mục :class:`DateTime` này vào đối tượng stream *out*.

   Lớp này cũng hỗ trợ một số toán tử dựng sẵn của Python thông qua
   các phương thức :meth:`rich comparison <object.__lt__>` và :meth:`~object.__repr__`.

Sau đây là một ví dụ hoạt động. Mã server::

   import datetime as dt
   from xmlrpc.server import SimpleXMLRPCServer
   import xmlrpc.client

   def today():
       today = dt.datetime.today()
       return xmlrpc.client.DateTime(today)

   server = SimpleXMLRPCServer(("localhost", 8000))
   print("Listening on port 8000...")
   server.register_function(today, "today")
   server.serve_forever()

Mã client cho server nêu trên::

   import xmlrpc.client
   import datetime as dt

   proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

   today = proxy.today()
   # chuyển chuỗi ISO 8601 thành đối tượng datetime
   converted = dt.datetime.strptime(today.value, "%Y%m%dT%H:%M:%S")
   print(f"Today: {converted.strftime('%d.%m.%Y, %H:%M')}")

.. _binary-objects:

Đối tượng nhị phân
------------------

.. class:: Binary

   Lớp này có thể được khởi tạo từ dữ liệu bytes (có thể bao gồm các byte NUL). Quyền truy cập chính vào nội dung của đối tượng :class:`Binary` được cung cấp thông qua một thuộc tính:


   .. attribute:: data

      Dữ liệu nhị phân được đóng gói bởi thể hiện :class:`Binary`. Dữ liệu được cung cấp dưới dạng đối tượng :class:`bytes`.

   Các đối tượng :class:`Binary` có các phương thức sau, chủ yếu được hỗ trợ để mã hóa và giải mã dữ liệu nội bộ:


   .. method:: decode(bytes)

      Nhận một đối tượng :class:`bytes` base64 và giải mã nó thành dữ liệu mới của instance.


   .. method:: encode(out)

      Ghi dữ liệu được mã hóa base64 theo chuẩn XML-RPC của mục nhị phân này vào đối tượng stream *out*.

      Dữ liệu được mã hóa sẽ có ký tự xuống dòng sau mỗi 76 ký tự, theo
      :rfc:`RFC 2045 section 6.8 <2045#section-6.8>`, vốn là đặc tả base64 trên thực tế khi đặc tả XML-RPC được viết.

   Nó cũng hỗ trợ một số toán tử tích hợp sẵn của Python thông qua
   các phương thức :meth:`~object.__eq__` và :meth:`~object.__ne__`.

Ví dụ sử dụng các đối tượng nhị phân. Chúng ta sẽ truyền một hình ảnh qua XMLRPC::

   from xmlrpc.server import SimpleXMLRPCServer
   import xmlrpc.client

   def python_logo():
       with open("python_logo.jpg", "rb") as handle:
           return xmlrpc.client.Binary(handle.read())

   server = SimpleXMLRPCServer(("localhost", 8000))
   print("Listening on port 8000...")
   server.register_function(python_logo, 'python_logo')

   server.serve_forever()

Client nhận hình ảnh và lưu vào một tệp::

   import xmlrpc.client

   proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
   with open("fetched_python_logo.jpg", "wb") as handle:
       handle.write(proxy.python_logo().data)

.. _fault-objects:

Đối tượng Fault
---------------

.. class:: Fault

   Một đối tượng :class:`Fault` đóng gói nội dung của thẻ fault XML-RPC. Các đối tượng Fault có những thuộc tính sau:


   .. attribute:: faultCode

      Một số nguyên cho biết loại fault.


   .. attribute:: faultString

      Một chuỗi chứa thông báo chẩn đoán liên quan đến fault.

Trong ví dụ sau, chúng ta sẽ cố ý gây ra một :exc:`Fault` bằng cách trả về một đối tượng kiểu phức hợp. Mã máy chủ::

   from xmlrpc.server import SimpleXMLRPCServer

   # Lỗi marshalling sẽ xảy ra vì chúng ta đang trả về một
   # số phức
   def add(x, y):
       return x+y+0j

   server = SimpleXMLRPCServer(("localhost", 8000))
   print("Listening on port 8000...")
   server.register_function(add, 'add')

   server.serve_forever()

Mã client cho server trước đó::

   import xmlrpc.client

   proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
   try:
       proxy.add(2, 5)
   except xmlrpc.client.Fault as err:
       print("A fault occurred")
       print("Fault code: %d" % err.faultCode)
       print("Fault string: %s" % err.faultString)



.. _protocol-error-objects:

Đối tượng ProtocolError
-----------------------

.. class:: ProtocolError

   Một đối tượng :class:`ProtocolError` mô tả lỗi giao thức trong lớp truyền tải bên dưới (chẳng hạn như lỗi 404 'không tìm thấy' nếu server được URI chỉ định không tồn tại). Đối tượng này có các thuộc tính sau:


   .. attribute:: url

      URI hoặc URL đã gây ra lỗi.


   .. attribute:: errcode

      Mã lỗi.


   .. attribute:: errmsg

      Thông báo lỗi hoặc chuỗi chẩn đoán.


   .. attribute:: headers

      Một dict chứa các header của request HTTP/HTTPS gây ra lỗi.

Trong ví dụ sau, chúng ta sẽ cố ý gây ra một :exc:`ProtocolError` bằng cách cung cấp một URI không hợp lệ::

   import xmlrpc.client

   # tạo một ServerProxy với URI không phản hồi các request XMLRPC
   proxy = xmlrpc.client.ServerProxy("http://google.com/")

   try:
       proxy.some_method()
   except xmlrpc.client.ProtocolError as err:
       print("A protocol error occurred")
       print("URL: %s" % err.url)
       print("HTTP/HTTPS headers: %s" % err.headers)
       print("Error code: %d" % err.errcode)
       print("Error message: %s" % err.errmsg)

Các đối tượng MultiCall
-----------------------

Đối tượng :class:`MultiCall` cung cấp một cách đóng gói nhiều lần gọi đến máy chủ từ xa vào một request duy nhất [#]_.


.. class:: MultiCall(server)

   Tạo một đối tượng dùng để xếp hàng các lần gọi phương thức. *server* là đích cuối cùng của lần gọi. Có thể thực hiện các lần gọi trên đối tượng kết quả, nhưng chúng sẽ ngay lập tức trả về ``None``, và chỉ lưu tên lần gọi cùng các tham số vào
   đối tượng :class:`MultiCall`. Việc gọi chính đối tượng này sẽ khiến tất cả các lệnh gọi đã lưu được truyền đi dưới dạng một yêu cầu ``system.multicall`` duy nhất. Kết quả của lần gọi này là một :term:`generator`; việc lặp qua generator này sẽ trả về từng kết quả riêng lẻ.

Sau đây là một ví dụ sử dụng lớp này. Mã server::

   from xmlrpc.server import SimpleXMLRPCServer

   def add(x, y):
       return x + y

   def subtract(x, y):
       return x - y

   def multiply(x, y):
       return x * y

   def divide(x, y):
       return x // y

   # Một server đơn giản với các hàm số học đơn giản
   server = SimpleXMLRPCServer(("localhost", 8000))
   print("Listening on port 8000...")
   server.register_multicall_functions()
   server.register_function(add, 'add')
   server.register_function(subtract, 'subtract')
   server.register_function(multiply, 'multiply')
   server.register_function(divide, 'divide')
   server.serve_forever()

Mã client cho server ở trên::

   import xmlrpc.client

   proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")
   multicall = xmlrpc.client.MultiCall(proxy)
   multicall.add(7, 3)
   multicall.subtract(7, 3)
   multicall.multiply(7, 3)
   multicall.divide(7, 3)
   result = multicall()

   print("7+3=%d, 7-3=%d, 7*3=%d, 7//3=%d" % tuple(result))


Các hàm tiện ích
----------------

.. function:: dumps(params, methodname=None, methodresponse=None, encoding=None, allow_none=False)

   Chuyển *params* thành một yêu cầu XML-RPC hoặc thành một response nếu *methodresponse* là true. *params* có thể là một tuple các đối số hoặc một instance của
   :exc:`Fault` lớp ngoại lệ. Nếu *methodresponse* là true, chỉ có thể trả về một giá trị duy nhất, nghĩa là *params* phải có độ dài là 1. *encoding*, nếu được cung cấp, là encoding sẽ dùng trong XML được tạo; mặc định là UTF-8. Giá trị :const:`None` của Python không thể được sử dụng trong XML-RPC tiêu chuẩn; để cho phép sử dụng giá trị này thông qua một phần mở rộng, hãy cung cấp giá trị true cho *allow_none*.


.. function:: loads(data, use_datetime=False, use_builtin_types=False)

   Chuyển đổi một request hoặc response XML-RPC thành các đối tượng Python, một ``(params, methodname)``. *params* là một tuple các đối số; *methodname* là một chuỗi hoặc ``None`` nếu packet không có tên method. Nếu packet XML-RPC biểu thị một điều kiện lỗi, hàm này sẽ raise một exception :exc:`Fault`. Cờ *use_builtin_types* có thể được dùng để khiến các giá trị ngày/giờ được biểu diễn dưới dạng các đối tượng :class:`datetime.datetime` và dữ liệu nhị phân được biểu diễn dưới dạng các đối tượng :class:`bytes`; theo mặc định, cờ này là false.

   Cờ *use_datetime* đã lỗi thời tương tự như *use_builtin_types* nhưng chỉ áp dụng cho các giá trị ngày/giờ.

   .. versionchanged:: 3.3
      Cờ *use_builtin_types* đã được thêm vào.


.. _xmlrpc-client-example:

Ví dụ về cách sử dụng Client
----------------------------

::

   # chương trình kiểm thử đơn giản (từ đặc tả XML-RPC)
   from xmlrpc.client import ServerProxy, Error

   # server = ServerProxy("http://localhost:8000") # máy chủ cục bộ
   with ServerProxy("http://betty.userland.com") as proxy:

       print(proxy)

       try:
           print(proxy.examples.getStateName(41))
       except Error as v:
           print("ERROR", v)

Để truy cập máy chủ XML-RPC thông qua HTTP proxy, bạn cần định nghĩa một transport tùy chỉnh. Ví dụ sau đây cho biết cách thực hiện::

   import http.client
   import xmlrpc.client

   class ProxiedTransport(xmlrpc.client.Transport):

       def set_proxy(self, host, port=None, headers=None):
           self.proxy = host, port
           self.proxy_headers = headers

       def make_connection(self, host):
           connection = http.client.HTTPConnection(*self.proxy)
           connection.set_tunnel(host, headers=self.proxy_headers)
           self._connection = host, connection
           return connection

   transport = ProxiedTransport()
   transport.set_proxy('proxy-server', 8080)
   server = xmlrpc.client.ServerProxy('http://betty.userland.com', transport=transport)
   print(server.examples.getStateName(41))


Ví dụ về cách sử dụng Client và Server
--------------------------------------

Xem :ref:`simplexmlrpcserver-example`.


.. rubric:: Chú thích cuối trang

.. [#] Cách tiếp cận này lần đầu được trình bày trong `một cuộc thảo luận trên xmlrpc.com <https://web.archive.org/web/20060624230303/http://www.xmlrpc.com/discuss/msgReader$1208?mode=topic>`_.
.. the link now points to webarchive since the one at
.. http://www.xmlrpc.com/discuss/msgReader%241208 is broken (and webadmin
.. doesn't reply)

.. _`http://ontosys.com/xml-rpc/extensions.php`: https://web.archive.org/web/20130120074804/http://ontosys.com/xml-rpc/extensions.php
.. _`XML-RPC HOWTO`: https://tldp.org/HOWTO/XML-RPC-HOWTO/index.html
.. _`XML-RPC Introspection`: https://xmlrpc-c.sourceforge.io/introspection.html
.. _`XML-RPC Specification`: http://xmlrpc.scripting.com/spec.html
.. _`a discussion on xmlrpc.com`: https://web.archive.org/web/20060624230303/http://www.xmlrpc.com/discuss/msgReader$1208?mode=topic
