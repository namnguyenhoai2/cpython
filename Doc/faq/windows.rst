:tocdepth: 2

.. highlight:: none

.. _windows-faq:

=========================================
Câu hỏi thường gặp về Python trên Windows
=========================================

.. only:: html

   .. contents::

.. XXX need review for Python 3.
   XXX need review for Windows Vista/Seven?

.. _faq-run-program-under-windows:


Làm thế nào để chạy một chương trình Python trên Windows?
---------------------------------------------------------

Đây không nhất thiết là một câu hỏi đơn giản. Nếu bạn đã quen chạy các chương trình từ dòng lệnh Windows thì mọi thứ sẽ có vẻ hiển nhiên; nếu không, bạn có thể cần thêm một chút hướng dẫn.

Trừ khi sử dụng một dạng môi trường phát triển tích hợp nào đó, bạn sẽ phải *gõ* các lệnh Windows vào nơi thường được gọi là "Command prompt window". Thông thường, bạn có thể mở một cửa sổ như vậy từ thanh tìm kiếm bằng cách tìm ``cmd``. Bạn sẽ có thể nhận ra khi đã mở một cửa sổ như vậy vì bạn sẽ thấy "command prompt" của Windows, thường có dạng như sau:

.. code-block:: doscon

   C:\>

Chữ cái này có thể khác, và có thể có thêm những thứ khác sau đó, vì vậy bạn cũng có thể dễ dàng thấy dạng như sau:

.. code-block:: doscon

   D:\YourName\Projects\Python>

tùy thuộc vào cách máy tính của bạn được thiết lập và những việc khác bạn vừa thực hiện trên đó. Khi đã mở một cửa sổ như vậy, bạn đã tiến khá gần đến việc chạy các chương trình Python.

Bạn cần hiểu rằng các tập lệnh Python của mình phải được xử lý bởi một chương trình khác có tên là *interpreter* Python. Interpreter đọc tập lệnh của bạn, biên dịch nó thành bytecode, rồi thực thi bytecode để chạy chương trình. Vậy bạn cần làm gì để interpreter xử lý mã Python của mình?

Trước tiên, bạn cần đảm bảo rằng cửa sổ lệnh nhận biết từ "py" là chỉ dẫn để khởi động interpreter. Nếu bạn đã mở một cửa sổ lệnh, hãy thử nhập lệnh ``py`` rồi nhấn Enter:

.. code-block:: doscon

   C:\Users\YourName> py

Sau đó, bạn sẽ thấy nội dung tương tự như sau:

.. code-block:: pycon

   Python 3.6.4 (v3.6.4:d48eceb, Dec 19 2017, 06:04:45) [MSC v.1900 32 bit (Intel)] on win32
   Type "help", "copyright", "credits" or "license" for more information.
   >>>

Bạn đã khởi động interpreter ở "interactive mode". Điều đó có nghĩa là bạn có thể tương tác nhập các câu lệnh hoặc biểu thức Python, rồi chờ chúng được thực thi hoặc đánh giá. Đây là một trong những tính năng mạnh nhất của Python. Hãy kiểm tra bằng cách nhập một vài biểu thức tùy ý và xem kết quả:

.. code-block:: pycon

    >>> print("Hello")
    Hello
    >>> "Hello" * 3
    'HelloHelloHello'

Nhiều người sử dụng interactive mode như một máy tính vừa tiện lợi vừa có khả năng lập trình cao. Khi muốn kết thúc phiên Python tương tác, hãy gọi hàm :func:`exit` hoặc giữ phím :kbd:`Ctrl` trong khi nhập ký tự :kbd:`Z`, sau đó nhấn phím ":kbd:`Enter`" để quay lại dấu nhắc lệnh Windows.

Bạn cũng có thể thấy trong Start-menu một mục như :menuselection:`Start --> Programs --> Python 3.x --> Python (command line)`, mục này sẽ mở dấu nhắc ``>>>`` trong một cửa sổ mới. Nếu vậy, cửa sổ sẽ biến mất sau khi bạn gọi hàm :func:`exit` hoặc nhập ký tự :kbd:`Ctrl-Z`; Windows đang chạy một lệnh "python" duy nhất trong cửa sổ đó và sẽ đóng cửa sổ khi bạn kết thúc interpreter.

Giờ đây, khi đã biết lệnh ``py`` được nhận diện, bạn có thể đưa tập lệnh Python của mình cho nó. Bạn sẽ phải cung cấp đường dẫn tuyệt đối hoặc tương đối đến tập lệnh Python. Giả sử tập lệnh Python của bạn nằm trên màn hình nền và có tên là ``hello.py``, còn dấu nhắc lệnh đang được mở thuận tiện trong thư mục nhà của bạn nên bạn thấy nội dung tương tự như sau::

   C:\Users\YourName>

Vậy bây giờ bạn sẽ yêu cầu lệnh ``py`` đưa tập lệnh của mình cho Python bằng cách nhập ``py`` theo sau là đường dẫn đến tập lệnh::


   C:\Users\YourName> py Desktop\hello.py
   hello

Làm thế nào để các script Python có thể thực thi?
-------------------------------------------------

Trên Windows, trình cài đặt Python chuẩn đã liên kết phần mở rộng .py với một loại tệp (Python.File) và cung cấp cho loại tệp đó một lệnh mở để chạy trình thông dịch (``D:\Program Files\Python\python.exe "%1" %*``). Điều này đủ để làm cho các script có thể thực thi từ command prompt dưới dạng 'foo.py'. Nếu muốn có thể thực thi script chỉ bằng cách gõ 'foo' mà không có phần mở rộng, bạn cần thêm .py vào biến môi trường PATHEXT.

Tại sao đôi khi Python khởi động lâu đến vậy?
---------------------------------------------

Thông thường Python khởi động rất nhanh trên Windows, nhưng đôi khi có các báo cáo lỗi cho biết Python đột nhiên mất nhiều thời gian để khởi động. Điều này càng khó hiểu hơn vì Python vẫn hoạt động bình thường trên các hệ thống Windows khác có vẻ được cấu hình giống hệt nhau.

Vấn đề có thể do phần mềm kiểm tra virus trên máy gặp sự cố được cấu hình sai. Một số trình quét virus được biết là làm tăng thời gian khởi động lên hai bậc độ lớn khi được cấu hình để theo dõi mọi thao tác đọc từ filesystem. Hãy kiểm tra cấu hình của phần mềm quét virus trên các hệ thống của bạn để đảm bảo rằng chúng thực sự được cấu hình giống hệt nhau. McAfee là một trường hợp đặc biệt gây vấn đề khi được cấu hình để quét mọi hoạt động đọc filesystem.


Làm thế nào để tạo tệp thực thi từ một script Python?
-----------------------------------------------------

Xem :ref:`faq-create-standalone-binary` để biết danh sách các công cụ có thể dùng để tạo tệp thực thi.


Tệp ``*.pyd`` có giống DLL không?
---------------------------------

Có, các tệp .pyd là dll, nhưng có một vài điểm khác biệt. Nếu bạn có một DLL tên là ``foo.pyd``, thì nó phải có một hàm ``PyInit_foo()``. Sau đó, bạn có thể viết Python "import foo", và Python sẽ tìm foo.pyd (cũng như foo.py, foo.pyc); nếu tìm thấy, Python sẽ cố gọi ``PyInit_foo()`` để khởi tạo nó. Bạn không liên kết .exe của mình với foo.lib, vì điều đó sẽ khiến Windows yêu cầu DLL phải hiện diện.

Lưu ý rằng đường dẫn tìm kiếm cho foo.pyd là PYTHONPATH, không giống với đường dẫn mà Windows dùng để tìm foo.dll. Ngoài ra, foo.pyd không nhất thiết phải hiện diện để chạy chương trình của bạn, trong khi nếu bạn liên kết chương trình với một dll thì dll đó là bắt buộc. Tất nhiên, foo.pyd là bắt buộc nếu bạn muốn viết ``import foo``. Trong DLL, việc liên kết được khai báo trong mã nguồn bằng ``__declspec(dllexport)``. Trong .pyd, việc liên kết được xác định trong danh sách các hàm khả dụng.


Làm cách nào để nhúng Python vào một ứng dụng Windows?
------------------------------------------------------

Có thể tóm tắt việc nhúng trình thông dịch Python vào một ứng dụng Windows như sau:

1. Đừng **not** xây dựng Python trực tiếp vào tệp .exe của bạn. Trên Windows, Python phải là một DLL để xử lý việc import các module vốn cũng là DLL. (Đây là sự thật quan trọng đầu tiên nhưng không được tài liệu hóa.) Thay vào đó, hãy liên kết với :file:`python{NN}.dll`; tệp này thường được cài đặt tại ``C:\Windows\System``. *NN* là phiên bản Python, một số như "33" đối với Python 3.3.

   Bạn có thể liên kết với Python theo hai cách khác nhau. Liên kết lúc tải nghĩa là liên kết với :file:`python{NN}.lib`, còn liên kết lúc chạy nghĩa là liên kết với :file:`python{NN}.dll`. (Lưu ý chung: :file:`python{NN}.lib` là "import lib" tương ứng với :file:`python{NN}.dll`. Nó chỉ định nghĩa các symbol cho linker.)

   Liên kết khi chạy (run-time linking) đơn giản hóa đáng kể các tùy chọn liên kết; mọi thứ đều diễn ra trong lúc chạy. Mã của bạn phải tải :file:`python{NN}.dll` bằng routine ``LoadLibraryEx()`` của Windows. Mã cũng phải sử dụng các routine truy cập và dữ liệu trong :file:`python{NN}.dll` (tức là C API của Python) bằng các con trỏ nhận được từ routine ``GetProcAddress()`` của Windows. Macro có thể giúp mọi mã C gọi các routine trong C API của Python sử dụng những con trỏ này một cách trong suốt.

   .. XXX what about static linking?

2. Nếu sử dụng SWIG, bạn có thể dễ dàng tạo một "extension module" Python để cung cấp dữ liệu và các phương thức của ứng dụng cho Python. SWIG sẽ xử lý gần như mọi chi tiết rắc rối cho bạn. Kết quả là mã C mà bạn liên kết *into* tệp .exe của mình (!)  Bạn **not** phải tạo tệp DLL, và điều này cũng đơn giản hóa việc liên kết.

3. SWIG sẽ tạo một hàm init (một hàm C), với tên phụ thuộc vào tên của extension module. Ví dụ, nếu tên module là leo, hàm init sẽ được gọi là initleo(). Nếu sử dụng shadow class của SWIG, như bạn nên làm, hàm init sẽ được gọi là initleoc(). Hàm này khởi tạo một helper class gần như được ẩn, được shadow class sử dụng.

   Lý do bạn có thể liên kết mã C ở bước 2 vào tệp .exe là vì việc gọi hàm khởi tạo tương đương với việc import module vào Python! (Đây là sự thật quan trọng thứ hai chưa được ghi chép.)

4. Tóm lại, bạn có thể sử dụng đoạn mã sau để khởi tạo trình thông dịch Python cùng với extension module của mình.

   .. code-block:: c

      #include <Python.h>
      ...
      Py_Initialize();  // Khởi tạo Python.
      initmyAppc();  // Khởi tạo (import) helper class.
      PyRun_SimpleString("import myApp");  // Import lớp shadow.

5. Có hai vấn đề với C API của Python sẽ trở nên rõ ràng nếu bạn sử dụng trình biên dịch khác MSVC, là trình biên dịch được dùng để xây dựng pythonNN.dll.

   Vấn đề 1: Các hàm được gọi là "Very High Level" nhận các đối số ``FILE *`` sẽ không hoạt động trong môi trường đa trình biên dịch vì cách hiểu về ``struct FILE`` của mỗi trình biên dịch sẽ khác nhau. Xét từ góc độ triển khai, đây là các hàm cấp rất thấp.

   Vấn đề 2: SWIG tạo ra đoạn mã sau khi tạo wrapper cho các hàm void:

   .. code-block:: c

      Py_INCREF(Py_None);
      _resultobj = Py_None;
      return _resultobj;

   Đáng tiếc là Py_None là một macro được mở rộng thành tham chiếu đến một cấu trúc dữ liệu phức tạp có tên _Py_NoneStruct bên trong pythonNN.dll. Một lần nữa, đoạn mã này sẽ không hoạt động trong môi trường đa trình biên dịch. Hãy thay đoạn mã đó bằng:

   .. code-block:: c

      return Py_BuildValue("");

   Có thể sử dụng lệnh ``%typemap`` của SWIG để tự động thực hiện thay đổi này, mặc dù tôi chưa thể làm cho cách này hoạt động (tôi hoàn toàn là người mới dùng SWIG).

6. Sử dụng shell script Python để mở một cửa sổ trình thông dịch Python từ bên trong ứng dụng Windows của bạn không phải là ý hay; cửa sổ tạo ra sẽ độc lập với hệ thống cửa sổ của ứng dụng. Thay vào đó, bạn (hoặc lớp wxPythonWindow) nên tạo một cửa sổ trình thông dịch "native". Việc kết nối cửa sổ đó với trình thông dịch Python rất dễ dàng. Bạn có thể chuyển hướng i/o của Python đến _any_ đối tượng hỗ trợ read và write, vì vậy tất cả những gì bạn cần là một đối tượng Python (được định nghĩa trong extension module) chứa các phương thức read() và write().

Làm thế nào để ngăn các trình soạn thảo chèn tab vào mã nguồn Python của tôi?
-----------------------------------------------------------------------------

FAQ không khuyến nghị sử dụng tab, và hướng dẫn kiểu Python, :pep:`8`, khuyến nghị dùng 4 dấu cách cho mã Python được phân phối; đây cũng là mặc định của Emacs python-mode.

Trong bất kỳ trình soạn thảo nào, việc trộn tab và dấu cách đều là một ý tưởng tồi. MSVC cũng không ngoại lệ về điểm này và có thể dễ dàng được cấu hình để sử dụng dấu cách: Chọn :menuselection:`Tools --> Options --> Tabs`, rồi đối với loại tệp "Default", đặt "Tab size" và "Indent size" thành 4, sau đó chọn nút radio "Insert spaces".

Python sẽ phát sinh :exc:`IndentationError` hoặc :exc:`TabError` nếu tab và dấu cách bị trộn lẫn gây ra sự cố trong khoảng trắng ở đầu dòng. Bạn cũng có thể chạy module :mod:`tabnanny` để kiểm tra một cây thư mục ở chế độ xử lý hàng loạt.


Làm thế nào để kiểm tra thao tác nhấn phím mà không chặn?
---------------------------------------------------------

Sử dụng module :mod:`msvcrt`. Đây là một extension module tiêu chuẩn dành riêng cho Windows. Module này định nghĩa một hàm ``kbhit()`` để kiểm tra xem có thao tác nhấn phím nào hay không, và ``getch()`` để lấy một ký tự mà không hiển thị ký tự đó.

Làm thế nào để khắc phục lỗi thiếu api-ms-win-crt-runtime-l1-1-0.dll?
---------------------------------------------------------------------

Điều này có thể xảy ra trên Python 3.5 trở lên khi sử dụng Windows 8.1 hoặc phiên bản cũ hơn mà chưa cài đặt đầy đủ mọi bản cập nhật. Trước tiên, hãy đảm bảo hệ điều hành của bạn được hỗ trợ và đã cập nhật, và nếu cách này không giải quyết được sự cố, hãy truy cập `trang hỗ trợ của Microsoft <https://support.microsoft.com/en-us/help/3118401/>`_ để được hướng dẫn cài đặt thủ công bản cập nhật C Runtime.

.. _`Microsoft support page`: https://support.microsoft.com/en-us/help/3118401/
