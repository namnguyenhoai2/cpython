:mod:`!xmlrpc.server` --- Máy chủ XML-RPC cơ bản
================================================

.. module:: xmlrpc.server
   :synopsis: Các triển khai máy chủ XML-RPC cơ bản.

.. moduleauthor:: Brian Quinlan <brianq@activestate.com>
.. sectionauthor:: Fred L. Drake, Jr. <fdrake@acm.org>

**Mã nguồn:** :source:`Lib/xmlrpc/server.py`

--------------

Mô-đun :mod:`!xmlrpc.server` cung cấp một framework máy chủ cơ bản cho các máy chủ XML-RPC được viết bằng Python. Máy chủ có thể hoạt động độc lập, bằng cách sử dụng
:class:`SimpleXMLRPCServer`, hoặc được nhúng trong môi trường CGI, bằng cách sử dụng
:class:`CGIXMLRPCRequestHandler`.


.. warning::

   Mô-đun :mod:`!xmlrpc.server` không an toàn trước dữ liệu được tạo dựng với mục đích độc hại. Nếu bạn cần phân tích dữ liệu không đáng tin cậy hoặc chưa được xác thực, hãy xem :ref:`xml-security`.

.. include:: ../includes/wasm-notavail.rst

.. class:: SimpleXMLRPCServer(addr, requestHandler=SimpleXMLRPCRequestHandler,\
               logRequests=True, allow_none=False, encoding=None,\ bind_and_activate=True, use_builtin_types=False)

   Tạo một server instance mới. Lớp này cung cấp các phương thức để đăng ký các function có thể được gọi bằng giao thức XML-RPC. Tham số *requestHandler* phải là một factory tạo các request handler instance; mặc định là
   :class:`SimpleXMLRPCRequestHandler`. Các tham số *addr* và *requestHandler* được truyền cho constructor :class:`socketserver.TCPServer`. Nếu *logRequests* là true (mặc định), các request sẽ được ghi log; đặt tham số này thành false sẽ tắt việc ghi log. Các tham số *allow_none* và *encoding* được truyền tiếp cho :mod:`xmlrpc.client` và kiểm soát các phản hồi XML-RPC sẽ được server trả về. Tham số *bind_and_activate* kiểm soát việc liệu
   :meth:`server_bind` và :meth:`server_activate` có được constructor gọi ngay hay không; mặc định là true. Đặt thành false cho phép code thao tác với biến lớp *allow_reuse_address* trước khi địa chỉ được bind. Tham số *use_builtin_types* được truyền cho
   function :func:`~xmlrpc.client.loads` và kiểm soát các kiểu dữ liệu được xử lý khi nhận các giá trị date/time hoặc dữ liệu nhị phân; mặc định là false.

   .. versionchanged:: 3.3
      Cờ *use_builtin_types* đã được thêm vào.


.. class:: CGIXMLRPCRequestHandler(allow_none=False, encoding=None,\
               use_builtin_types=False)

   Tạo một instance mới để xử lý các request XML-RPC trong môi trường CGI. Các tham số *allow_none* và *encoding* được truyền tiếp cho :mod:`xmlrpc.client` và kiểm soát các phản hồi XML-RPC sẽ được server trả về. Tham số *use_builtin_types* được truyền cho
   function :func:`~xmlrpc.client.loads` và kiểm soát các kiểu dữ liệu được xử lý khi nhận các giá trị date/time hoặc dữ liệu nhị phân; mặc định là false.

   .. versionchanged:: 3.3
      Cờ *use_builtin_types* đã được thêm vào.


.. class:: SimpleXMLRPCRequestHandler()

   Tạo một instance request handler mới. Request handler này hỗ trợ các request ``POST`` và sửa đổi việc logging để tham số *logRequests* đối với
   tham số constructor :class:`SimpleXMLRPCServer` được áp dụng.


.. _simple-xmlrpc-servers:

Các đối tượng SimpleXMLRPCServer
--------------------------------

Lớp :class:`SimpleXMLRPCServer` được xây dựng dựa trên
:class:`socketserver.TCPServer` và cung cấp phương tiện để tạo các XML-RPC server đơn giản, độc lập.


.. method:: SimpleXMLRPCServer.register_function(function=None, name=None)

   Đăng ký một hàm có thể phản hồi các yêu cầu XML-RPC. Nếu *name* được cung cấp, đó sẽ là tên phương thức được liên kết với *function*, nếu không thì
   :attr:`function.__name__` sẽ được sử dụng. *name* là một chuỗi và có thể chứa các ký tự không hợp lệ trong định danh Python, bao gồm cả dấu chấm.

   Phương thức này cũng có thể được sử dụng như một decorator. Khi được sử dụng như một decorator, chỉ có thể cung cấp *name* dưới dạng đối số từ khóa để đăng ký *function* dưới *name*. Nếu không cung cấp *name*, :attr:`function.__name__` sẽ được sử dụng.

   .. versionchanged:: 3.7
      :meth:`register_function` can be used as a decorator.


.. method:: SimpleXMLRPCServer.register_instance(instance, allow_dotted_names=False)

   Đăng ký một đối tượng được dùng để cung cấp các tên phương thức chưa được đăng ký bằng :meth:`register_function`. Nếu *instance* chứa một
   :meth:`_dispatch` method, phương thức đó được gọi với tên phương thức được yêu cầu và các tham số từ yêu cầu. API của nó là ``def _dispatch(self, method, params)`` (lưu ý rằng *params* không biểu thị một danh sách đối số biến đổi). Nếu phương thức này gọi một hàm underlying để thực hiện tác vụ, hàm đó được gọi dưới dạng ``func(*params)``, với danh sách tham số được mở rộng. Giá trị trả về từ
   :meth:`_dispatch` được trả về cho client làm kết quả. Nếu *instance* không có phương thức :meth:`_dispatch`, một thuộc tính khớp với tên của phương thức được yêu cầu sẽ được tìm kiếm.

   Nếu đối số tùy chọn *allow_dotted_names* là true và instance không có phương thức :meth:`_dispatch`, thì nếu tên phương thức được yêu cầu chứa dấu chấm, từng thành phần của tên phương thức sẽ được tìm kiếm riêng lẻ, nhờ đó thực hiện một quy trình tìm kiếm phân cấp đơn giản. Giá trị tìm được từ quy trình tìm kiếm này sau đó được gọi với các tham số từ yêu cầu, và giá trị trả về được chuyển lại cho client.

   .. warning::

      Việc bật tùy chọn *allow_dotted_names* cho phép kẻ xâm nhập truy cập các biến toàn cục của module và có thể cho phép chúng thực thi mã tùy ý trên máy của bạn. Chỉ sử dụng tùy chọn này trên một mạng an toàn, khép kín.


.. method:: SimpleXMLRPCServer.register_introspection_functions()

   Đăng ký các hàm introspection XML-RPC ``system.listMethods``, ``system.methodHelp`` và ``system.methodSignature``.


.. method:: SimpleXMLRPCServer.register_multicall_functions()

   Đăng ký hàm multicall XML-RPC system.multicall.


.. attribute:: SimpleXMLRPCRequestHandler.rpc_paths

   Một giá trị thuộc tính phải là một tuple liệt kê các phần đường dẫn hợp lệ của URL dùng để nhận các yêu cầu XML-RPC. Các yêu cầu được gửi đến những đường dẫn khác sẽ dẫn đến lỗi HTTP 404 "không có trang như vậy". Nếu tuple này rỗng, mọi đường dẫn sẽ được coi là hợp lệ. Giá trị mặc định là ``('/', '/RPC2')``.


.. _simplexmlrpcserver-example:

Ví dụ về SimpleXMLRPCServer
^^^^^^^^^^^^^^^^^^^^^^^^^^^
Mã server::

   from xmlrpc.server import SimpleXMLRPCServer
   from xmlrpc.server import SimpleXMLRPCRequestHandler

   # Giới hạn ở một đường dẫn cụ thể.
   class RequestHandler(SimpleXMLRPCRequestHandler):
       rpc_paths = ('/RPC2',)

   # Tạo máy chủ
   with SimpleXMLRPCServer(('localhost', 8000),
                           requestHandler=RequestHandler) as server:
       server.register_introspection_functions()

       # Đăng ký hàm pow(); hàm này sẽ sử dụng giá trị của
       # pow.__name__ làm tên, tức là 'pow'.
       server.register_function(pow)

       # Đăng ký một hàm với tên khác
       def adder_function(x, y):
           return x + y
       server.register_function(adder_function, 'add')

       # Đăng ký một instance; tất cả các phương thức của instance đều được
       # công bố dưới dạng các phương thức XML-RPC (trong trường hợp này chỉ là 'mul').
       class MyFuncs:
           def mul(self, x, y):
               return x * y

       server.register_instance(MyFuncs())

       # Chạy vòng lặp chính của máy chủ
       server.serve_forever()

Đoạn mã client sau đây sẽ gọi các phương thức được server ở trên cung cấp::

   import xmlrpc.client

   s = xmlrpc.client.ServerProxy('http://localhost:8000')
   print(s.pow(2,3))  # Trả về 2**3 = 8
   print(s.add(2,3))  # Trả về 5
   print(s.mul(5,2))  # Trả về 5*2 = 10

   # In danh sách các phương thức hiện có
   print(s.system.listMethods())

:meth:`register_function` cũng có thể được sử dụng như một decorator. Ví dụ server trước đó có thể đăng ký các hàm theo cách sử dụng decorator::

   from xmlrpc.server import SimpleXMLRPCServer
   from xmlrpc.server import SimpleXMLRPCRequestHandler

   class RequestHandler(SimpleXMLRPCRequestHandler):
       rpc_paths = ('/RPC2',)

   with SimpleXMLRPCServer(('localhost', 8000),
                           requestHandler=RequestHandler) as server:
       server.register_introspection_functions()

       # Đăng ký hàm pow(); hàm này sẽ sử dụng giá trị của
       # pow.__name__ làm tên, tức là 'pow'.
       server.register_function(pow)

       # Đăng ký một hàm dưới tên khác bằng cách sử dụng
       # register_function dưới dạng decorator. Chỉ có thể cung cấp *name*
       # dưới dạng đối số từ khóa.
       @server.register_function(name='add')
       def adder_function(x, y):
           return x + y

       # Đăng ký một hàm dưới function.__name__.
       @server.register_function
       def mul(x, y):
           return x * y

       server.serve_forever()

Ví dụ sau đây trong module :file:`Lib/xmlrpc/server.py` cho thấy một server cho phép các tên có dấu chấm và đăng ký một hàm multicall.

.. warning::

  Bật tùy chọn *allow_dotted_names* cho phép kẻ xâm nhập truy cập các biến toàn cục của module và có thể cho phép chúng thực thi mã tùy ý trên máy của bạn. Chỉ sử dụng ví dụ này trong một mạng an toàn, khép kín.

::

    import datetime as dt

    class ExampleService:
        def getData(self):
            return '42'

        class currentTime:
            @staticmethod
            def getCurrentTime():
                return dt.datetime.now()

    with SimpleXMLRPCServer(("localhost", 8000)) as server:
        server.register_function(pow)
        server.register_function(lambda x,y: x+y, 'add')
        server.register_instance(ExampleService(), allow_dotted_names=True)
        server.register_multicall_functions()
        print('Serving XML-RPC on localhost port 8000')
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)

Có thể gọi bản demo ExampleService này từ dòng lệnh::

    python -m xmlrpc.server


Client tương tác với server ở trên được bao gồm trong ``Lib/xmlrpc/client.py``::

    server = ServerProxy("http://localhost:8000")

    try:
        print(server.currentTime.getCurrentTime())
    except Error as v:
        print("ERROR", v)

    multi = MultiCall(server)
    multi.getData()
    multi.pow(2,9)
    multi.add(1,2)
    try:
        for response in multi():
            print(response)
    except Error as v:
        print("ERROR", v)

Có thể gọi client tương tác với server XMLRPC demo này như sau::

    python -m xmlrpc.client


CGIXMLRPCRequestHandler
-----------------------

Có thể sử dụng lớp :class:`CGIXMLRPCRequestHandler` để xử lý các yêu cầu XML-RPC được gửi đến các tập lệnh CGI của Python.


.. method:: CGIXMLRPCRequestHandler.register_function(function=None, name=None)

   Đăng ký một hàm có thể phản hồi các yêu cầu XML-RPC. Nếu cung cấp *name*, đây sẽ là tên phương thức được liên kết với *function*, nếu không thì
   :attr:`function.__name__` sẽ được sử dụng. *name* là một chuỗi và có thể chứa các ký tự không hợp lệ trong các định danh Python, bao gồm cả ký tự dấu chấm.

   Phương thức này cũng có thể được dùng làm decorator. Khi được dùng làm decorator, *name* chỉ có thể được cung cấp dưới dạng đối số keyword để đăng ký *function* dưới *name*. Nếu không cung cấp *name*, :attr:`function.__name__` sẽ được dùng.

   .. versionchanged:: 3.7
      :meth:`register_function` can be used as a decorator.


.. method:: CGIXMLRPCRequestHandler.register_instance(instance)

   Đăng ký một đối tượng được dùng để cung cấp các tên phương thức chưa được đăng ký bằng :meth:`register_function`. Nếu instance chứa một
   :meth:`_dispatch` method, phương thức này được gọi với tên phương thức được yêu cầu và các tham số từ request; giá trị trả về được gửi cho client làm kết quả. Nếu instance không có phương thức :meth:`_dispatch`, một thuộc tính khớp với tên của phương thức được yêu cầu sẽ được tìm kiếm; nếu tên phương thức được yêu cầu chứa dấu chấm, từng thành phần của tên phương thức sẽ được tìm kiếm riêng, nhờ đó thực hiện một tìm kiếm phân cấp đơn giản. Giá trị tìm được từ quá trình tìm kiếm này sau đó được gọi với các tham số từ request, và giá trị trả về được gửi lại cho client.


.. method:: CGIXMLRPCRequestHandler.register_introspection_functions()

   Đăng ký các hàm introspection XML-RPC ``system.listMethods``, ``system.methodHelp`` và ``system.methodSignature``.


.. method:: CGIXMLRPCRequestHandler.register_multicall_functions()

   Đăng ký hàm multicall XML-RPC ``system.multicall``.


.. method:: CGIXMLRPCRequestHandler.handle_request(request_text=None)

   Xử lý một request XML-RPC. Nếu *request_text* được cung cấp, đó phải là dữ liệu POST do HTTP server cung cấp; nếu không, nội dung của stdin sẽ được sử dụng.

Ví dụ::

   class MyFuncs:
       def mul(self, x, y):
           return x * y


   handler = CGIXMLRPCRequestHandler()
   handler.register_function(pow)
   handler.register_function(lambda x,y: x+y, 'add')
   handler.register_introspection_functions()
   handler.register_instance(MyFuncs())
   handler.handle_request()


Tài liệu về máy chủ XMLRPC
--------------------------

Các lớp này mở rộng các lớp ở trên để cung cấp tài liệu HTML khi nhận được các yêu cầu HTTP GET. Máy chủ có thể hoạt động độc lập, sử dụng
:class:`DocXMLRPCServer`
:class:`DocCGIXMLRPCRequestHandler`.


.. class:: DocXMLRPCServer(addr, requestHandler=DocXMLRPCRequestHandler,\
               logRequests=True, allow_none=False, encoding=None,\ bind_and_activate=True, use_builtin_types=True)

   Tạo một phiên bản máy chủ mới. Tất cả tham số có cùng ý nghĩa như trong
   :class:`SimpleXMLRPCServer`; *requestHandler* mặc định là
   :class:`DocXMLRPCRequestHandler`.

   .. versionchanged:: 3.3
      Cờ *use_builtin_types* đã được thêm vào.


.. class:: DocCGIXMLRPCRequestHandler()

   Tạo một instance mới để xử lý các yêu cầu XML-RPC trong môi trường CGI.


.. class:: DocXMLRPCRequestHandler()

   Tạo một instance request handler mới. Request handler này hỗ trợ các yêu cầu XML-RPC POST, các yêu cầu GET để xem tài liệu và điều chỉnh việc ghi log để tham số *logRequests* truyền cho tham số constructor :class:`DocXMLRPCServer` được áp dụng.


.. _doc-xmlrpc-servers:

Các đối tượng DocXMLRPCServer
-----------------------------

Lớp :class:`DocXMLRPCServer` được kế thừa từ :class:`SimpleXMLRPCServer` và cung cấp cách tạo các XML-RPC server độc lập, có tài liệu tự mô tả. Các yêu cầu HTTP POST được xử lý dưới dạng các lệnh gọi phương thức XML-RPC. Các yêu cầu HTTP GET được xử lý bằng cách tạo tài liệu HTML theo kiểu pydoc. Điều này cho phép server cung cấp tài liệu dựa trên web của chính nó.


.. method:: DocXMLRPCServer.set_server_title(server_title)

   Đặt tiêu đề được sử dụng trong tài liệu HTML được tạo. Tiêu đề này sẽ được sử dụng bên trong phần tử HTML "title".


.. method:: DocXMLRPCServer.set_server_name(server_name)

   Đặt tên được sử dụng trong tài liệu HTML được tạo. Tên này sẽ xuất hiện ở đầu tài liệu được tạo, bên trong phần tử "h1".


.. method:: DocXMLRPCServer.set_server_documentation(server_documentation)

   Đặt mô tả được sử dụng trong tài liệu HTML được tạo. Mô tả này sẽ xuất hiện dưới dạng một đoạn văn, bên dưới tên server, trong tài liệu.


DocCGIXMLRPCRequestHandler
--------------------------

Lớp :class:`DocCGIXMLRPCRequestHandler` được dẫn xuất từ
:class:`CGIXMLRPCRequestHandler` và cung cấp một phương thức để tạo các tập lệnh CGI XML-RPC có tài liệu tự mô tả. Các yêu cầu HTTP POST được xử lý dưới dạng các lệnh gọi phương thức XML-RPC. Các yêu cầu HTTP GET được xử lý bằng cách tạo tài liệu HTML theo kiểu pydoc. Điều này cho phép máy chủ cung cấp tài liệu dựa trên web của riêng mình.


.. method:: DocCGIXMLRPCRequestHandler.set_server_title(server_title)

   Đặt tiêu đề được sử dụng trong tài liệu HTML được tạo. Tiêu đề này sẽ được sử dụng bên trong phần tử HTML "title".


.. method:: DocCGIXMLRPCRequestHandler.set_server_name(server_name)

   Đặt tên được sử dụng trong tài liệu HTML được tạo. Tên này sẽ xuất hiện ở đầu tài liệu được tạo, bên trong phần tử "h1".


.. method:: DocCGIXMLRPCRequestHandler.set_server_documentation(server_documentation)

   Đặt phần mô tả được sử dụng trong tài liệu HTML được tạo. Phần mô tả này sẽ xuất hiện dưới dạng một đoạn văn, bên dưới tên máy chủ, trong tài liệu.
