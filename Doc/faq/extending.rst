===================================
Câu hỏi thường gặp về mở rộng/nhúng
===================================

.. only:: html

   .. contents::

.. highlight:: c


.. XXX need review for Python 3.


Tôi có thể tự tạo các hàm bằng C không?
---------------------------------------

Có, bạn có thể tạo các module dựng sẵn chứa hàm, biến, ngoại lệ và thậm chí cả kiểu mới bằng C. Điều này được giải thích trong tài liệu
:ref:`extending-index`.

Hầu hết các sách Python trình độ trung cấp hoặc nâng cao cũng đề cập đến chủ đề này.


Tôi có thể tự tạo các hàm bằng C++ không?
-----------------------------------------

Có, bằng cách sử dụng các tính năng tương thích với C có trong C++. Hãy đặt ``extern "C" { ... }`` bao quanh các tệp include của Python và đặt ``extern "C"`` trước mỗi hàm sẽ được trình thông dịch Python gọi. Các đối tượng C++ toàn cục hoặc static có hàm khởi tạo có lẽ không phải là một ý hay.


.. _c-wrapper-software:

Viết C thật khó; có lựa chọn nào khác không?
--------------------------------------------

Có một số lựa chọn thay thế cho việc tự viết các phần mở rộng C, tùy thuộc vào điều bạn đang muốn thực hiện. :ref:`Các công cụ bên thứ ba được đề xuất <c-api-tools>` cung cấp cả những cách tiếp cận đơn giản hơn và nâng cao hơn để tạo các phần mở rộng C và C++ cho Python.


Làm thế nào để thực thi các câu lệnh Python tùy ý từ C?
-------------------------------------------------------

Hàm ở cấp cao nhất để thực hiện việc này là :c:func:`PyRun_SimpleString`, nhận một đối số chuỗi duy nhất để thực thi trong ngữ cảnh của module ``__main__`` và trả về ``0`` nếu thành công, còn ``-1`` khi xảy ra ngoại lệ (bao gồm cả :exc:`SyntaxError`). Nếu muốn kiểm soát nhiều hơn, hãy sử dụng
:c:func:`PyRun_String`; xem mã nguồn của :c:func:`PyRun_SimpleString` trong ``Python/pythonrun.c``.


Làm thế nào để đánh giá một biểu thức Python tùy ý từ C?
--------------------------------------------------------

Gọi hàm :c:func:`PyRun_String` từ câu hỏi trước với ký hiệu bắt đầu :c:data:`Py_eval_input`; hàm này phân tích cú pháp một biểu thức, đánh giá biểu thức đó và trả về giá trị của nó.


Làm thế nào để trích xuất các giá trị C từ một đối tượng Python?
----------------------------------------------------------------

Điều đó phụ thuộc vào kiểu của đối tượng. Nếu đó là một tuple, :c:func:`PyTuple_Size` trả về độ dài của tuple và :c:func:`PyTuple_GetItem` trả về phần tử tại một chỉ mục được chỉ định. Lists có các hàm tương tự, :c:func:`PyList_Size` và
:c:func:`PyList_GetItem`.

Đối với bytes, :c:func:`PyBytes_Size` trả về độ dài của nó và
:c:func:`PyBytes_AsStringAndSize` cung cấp một con trỏ đến giá trị và độ dài của nó. Lưu ý rằng các đối tượng bytes của Python có thể chứa byte null, vì vậy của C
:c:func:`!strlen` không nên được sử dụng.

Để kiểm tra kiểu của một đối tượng, trước tiên hãy đảm bảo rằng nó không phải là ``NULL``, sau đó sử dụng
:c:func:`PyBytes_Check`, :c:func:`PyTuple_Check`, :c:func:`PyList_Check`, v.v.

Ngoài ra còn có một API cấp cao để làm việc với các đối tượng Python, được cung cấp bởi giao diện được gọi là "abstract" — hãy đọc ``Include/abstract.h`` để biết thêm chi tiết. Giao diện này cho phép tương tác với mọi loại sequence Python bằng các lệnh gọi như :c:func:`PySequence_Length`, :c:func:`PySequence_GetItem`, v.v., cũng như nhiều protocol hữu ích khác như numbers (:c:func:`PyNumber_Index` và các hàm khác) và mappings trong các API PyMapping.


Làm thế nào để sử dụng Py_BuildValue() nhằm tạo một tuple có độ dài tùy ý?
--------------------------------------------------------------------------

Không thể. Thay vào đó, hãy sử dụng :c:func:`PyTuple_Pack`.


Làm thế nào để gọi phương thức của một đối tượng từ C?
------------------------------------------------------

Có thể sử dụng hàm :c:func:`PyObject_CallMethod` để gọi một phương thức bất kỳ của một đối tượng. Các tham số gồm đối tượng, tên phương thức cần gọi, một chuỗi định dạng giống chuỗi được sử dụng với :c:func:`Py_BuildValue`, và các giá trị đối số::

   PyObject *
   PyObject_CallMethod(PyObject *object, const char *method_name,
                       const char *arg_format, ...);

Cách này hoạt động với mọi đối tượng có phương thức -- dù là phương thức dựng sẵn hay do người dùng định nghĩa. Bạn chịu trách nhiệm cuối cùng trong việc :c:func:`Py_DECREF`\ 'ing giá trị trả về.

Để gọi, chẳng hạn, phương thức "seek" của một đối tượng file với các đối số 10, 0 (giả sử con trỏ đối tượng file là "f")::

   res = PyObject_CallMethod(f, "seek", "(ii)", 10, 0);
   if (res == NULL) {
           ... an exception occurred ...
   }
   else {
           Py_DECREF(res);
   }

Lưu ý rằng vì :c:func:`PyObject_CallObject` *luôn* yêu cầu một tuple cho danh sách đối số, để gọi một hàm không có đối số, hãy truyền "()" làm định dạng; còn để gọi một hàm có một đối số, hãy đặt đối số trong dấu ngoặc đơn, chẳng hạn "(i)".


Làm thế nào để bắt đầu ra từ PyErr_Print() (hoặc bất kỳ thứ gì in ra stdout/stderr)?
------------------------------------------------------------------------------------

Trong mã Python, hãy định nghĩa một đối tượng hỗ trợ phương thức ``write()``. Gán đối tượng này cho :data:`sys.stdout` và :data:`sys.stderr`. Gọi print_error hoặc chỉ cần cho phép cơ chế traceback tiêu chuẩn hoạt động. Khi đó, đầu ra sẽ được chuyển đến nơi mà phương thức ``write()`` của bạn gửi đến.

Cách dễ nhất để thực hiện việc này là sử dụng lớp :class:`io.StringIO`:

.. code-block:: pycon

   >>> import io, sys
   >>> sys.stdout = io.StringIO()
   >>> print('foo')
   >>> print('hello world!')
   >>> sys.stderr.write(sys.stdout.getvalue())
   foo
   hello world!

Một đối tượng tùy chỉnh để thực hiện điều tương tự sẽ có dạng như sau:

.. code-block:: pycon

   >>> import io, sys
   >>> class StdoutCatcher(io.TextIOBase):
   ...     def __init__(self):
   ...         self.data = []
   ...     def write(self, stuff):
   ...         self.data.append(stuff)
   ...
   >>> import sys
   >>> sys.stdout = StdoutCatcher()
   >>> print('foo')
   >>> print('hello world!')
   >>> sys.stderr.write(''.join(sys.stdout.data))
   foo
   hello world!


Làm thế nào để truy cập một module được viết bằng Python từ C?
--------------------------------------------------------------

Bạn có thể lấy con trỏ đến đối tượng module như sau::

   module = PyImport_ImportModule("<modulename>");

Nếu module chưa được import (tức là nó vẫn chưa xuất hiện trong
:data:`sys.modules`), thao tác này khởi tạo module; nếu không thì nó chỉ trả về giá trị của ``sys.modules["<modulename>"]``. Lưu ý rằng thao tác này không đưa module vào bất kỳ namespace nào -- nó chỉ đảm bảo module đã được khởi tạo và được lưu trong :data:`sys.modules`.

Sau đó, bạn có thể truy cập các thuộc tính của module (tức là bất kỳ tên nào được định nghĩa trong module) như sau::

   attr = PyObject_GetAttrString(module, "<attrname>");

Việc gọi :c:func:`PyObject_SetAttrString` để gán giá trị cho các biến trong module cũng hoạt động.


Làm cách nào để giao tiếp với các đối tượng C++ từ Python?
----------------------------------------------------------

Tùy theo yêu cầu, có nhiều cách tiếp cận. Để thực hiện thủ công, trước tiên hãy đọc :ref:`tài liệu "Mở rộng và nhúng" <extending-index>`. Hãy lưu ý rằng đối với hệ thống runtime của Python, C và C++ không khác nhau quá nhiều -- vì vậy, chiến lược xây dựng một kiểu Python mới dựa trên kiểu cấu trúc (con trỏ) C cũng sẽ hoạt động với các đối tượng C++.

Đối với các thư viện C++, hãy xem :ref:`c-wrapper-software`.


Tôi đã thêm một module bằng tệp Setup nhưng make không thành công; tại sao?
---------------------------------------------------------------------------

Setup phải kết thúc bằng một ký tự xuống dòng; nếu không có ký tự xuống dòng ở đó, quá trình build sẽ thất bại. (Việc sửa lỗi này đòi hỏi một số thủ thuật shell khá rắc rối, và lỗi này nhỏ đến mức có vẻ không đáng bỏ công sức.)


Làm thế nào để debug một extension?
-----------------------------------

Khi sử dụng GDB với các extension được tải động, bạn không thể đặt breakpoint trong extension của mình cho đến khi extension đó được tải.

Trong tệp ``.gdbinit`` của bạn (hoặc trong chế độ tương tác), hãy thêm lệnh:

.. code-block:: none

   br _PyImport_LoadDynamicModule

Sau đó, khi bạn chạy GDB:

.. code-block:: shell-session

   $ gdb /local/bin/python
   gdb) run myscript.py
   gdb) continue # repeat until your extension is loaded
   gdb) finish   # so that your extension is loaded
   gdb) br myfunction.c:50
   gdb) continue

Tôi muốn biên dịch một module Python trên hệ thống Linux của mình, nhưng một số tệp bị thiếu. Tại sao?
------------------------------------------------------------------------------------------------------

Hầu hết các phiên bản Python được đóng gói đều lược bỏ một số tệp cần thiết để biên dịch các extension Python.

Đối với Red Hat, hãy cài đặt RPM python3-devel để có các tệp cần thiết.

Đối với Debian, hãy chạy ``apt-get install python3-dev``.

Làm thế nào để phân biệt "incomplete input" với "invalid input"?
----------------------------------------------------------------

Đôi khi bạn muốn mô phỏng hành vi của trình thông dịch tương tác Python, trong đó trình thông dịch hiển thị lời nhắc tiếp tục khi dữ liệu đầu vào chưa hoàn chỉnh (ví dụ: bạn đã nhập phần đầu của câu lệnh "if" hoặc chưa đóng dấu ngoặc hay dấu ngoặc kép ba), nhưng ngay lập tức hiển thị thông báo lỗi cú pháp khi dữ liệu đầu vào không hợp lệ.

Trong Python, bạn có thể sử dụng mô-đun :mod:`codeop`, mô-đun này mô phỏng đủ chính xác hành vi của parser. Ví dụ, IDLE sử dụng mô-đun này.

Cách dễ nhất để thực hiện việc này trong C là gọi :c:func:`PyRun_InteractiveLoop` (có thể trong một thread riêng) và để trình thông dịch Python xử lý dữ liệu đầu vào cho bạn. Bạn cũng có thể đặt :c:func:`PyOS_ReadlineFunctionPointer` trỏ đến hàm input tùy chỉnh của mình. Hãy xem ``Modules/readline.c`` và ``Parser/myreadline.c`` để biết thêm gợi ý.

Làm thế nào để tìm các symbol g++ chưa được định nghĩa __builtin_new hoặc __pure_virtual?
-----------------------------------------------------------------------------------------

Để tải động các extension module g++ , bạn phải biên dịch lại Python, liên kết lại bằng g++ (thay đổi LINKCC trong Python Modules Makefile), rồi liên kết extension module của bạn bằng g++ (ví dụ: ``g++ -shared -o mymodule.so mymodule.o``).


Tôi có thể tạo một object class với một số phương thức được triển khai bằng C và các phương thức khác bằng Python (ví dụ: thông qua inheritance) không?
-------------------------------------------------------------------------------------------------------------------------------------------------------

Có, bạn có thể kế thừa từ các built-in class như :class:`int`, :class:`list`,
:class:`dict`, v.v.

Boost Python Library (BPL, https://www.boost.org/libs/python/doc/index.html) cung cấp một cách để thực hiện việc này từ C++ (tức là bạn có thể kế thừa từ một extension class được viết bằng C++ bằng BPL).
