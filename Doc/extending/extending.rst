.. highlight:: c


.. _extending-intro:

******************************
Mở rộng Python bằng C hoặc C++
******************************

Việc thêm các mô-đun tích hợp mới vào Python khá dễ dàng nếu bạn biết lập trình bằng C. Những :dfn:`mô-đun mở rộng` như vậy có thể thực hiện hai việc không thể làm trực tiếp bằng Python: triển khai các kiểu đối tượng tích hợp mới và gọi các hàm thư viện C cũng như các lệnh gọi hệ thống.

Để hỗ trợ các phần mở rộng, Python API (Giao diện Lập trình Ứng dụng) định nghĩa một tập hợp các hàm, macro và biến cho phép truy cập vào hầu hết các khía cạnh của hệ thống run-time Python. Python API được đưa vào một tệp mã nguồn C bằng cách thêm header ``"Python.h"``.

Việc biên dịch một mô-đun mở rộng phụ thuộc vào mục đích sử dụng của mô-đun cũng như cấu hình hệ thống của bạn; thông tin chi tiết được trình bày trong các chương sau.

.. note::

   Giao diện phần mở rộng C dành riêng cho CPython và các mô-đun mở rộng không hoạt động trên những triển khai Python khác. Trong nhiều trường hợp, bạn có thể tránh viết phần mở rộng C mà vẫn duy trì khả năng portable sang các triển khai khác. Ví dụ: nếu trường hợp sử dụng của bạn là gọi các hàm thư viện C hoặc các lệnh gọi hệ thống, bạn nên cân nhắc sử dụng mô-đun :mod:`ctypes` hoặc thư viện `cffi <https://cffi.readthedocs.io/>`_ thay vì tự viết mã C. Các mô-đun này cho phép bạn viết mã Python để giao tiếp với mã C và có tính portable giữa các triển khai Python tốt hơn so với việc viết và biên dịch một mô-đun mở rộng C.


.. _extending-simpleexample:

Một ví dụ đơn giản
==================

Hãy tạo một mô-đun mở rộng có tên ``spam`` (món ăn yêu thích của những người hâm mộ Monty Python...) và giả sử chúng ta muốn tạo một giao diện Python cho hàm thư viện C :c:func:`system` [#]_. Hàm này nhận một chuỗi ký tự kết thúc bằng null làm đối số và trả về một số nguyên. Chúng ta muốn hàm này có thể được gọi từ Python như sau:

.. code-block:: pycon

   >>> import spam
   >>> status = spam.system("ls -l")

Bắt đầu bằng cách tạo một tệp :file:`spammodule.c`.  (Theo thông lệ trước đây, nếu một module có tên ``spam``, tệp C chứa phần triển khai của module đó được gọi là
:file:`spammodule.c`; nếu tên module rất dài, chẳng hạn như ``spammify``, thì tên module có thể chỉ là :file:`spammify.c`.)

Hai dòng đầu tiên của tệp có thể là::

   #define PY_SSIZE_T_CLEAN
   #include <Python.h>

dòng này đưa Python API vào (nếu muốn, bạn có thể thêm một comment mô tả mục đích của module và thông báo bản quyền).

.. note::

   Vì Python có thể định nghĩa một số macro tiền xử lý ảnh hưởng đến các header chuẩn trên một số hệ thống, bạn *phải* include :file:`Python.h` trước khi include bất kỳ header chuẩn nào.

   ``#define PY_SSIZE_T_CLEAN`` được dùng để chỉ rằng trong một số API, nên sử dụng ``Py_ssize_t`` thay vì ``int``. Điều này không còn cần thiết kể từ Python 3.13, nhưng chúng tôi vẫn giữ lại để tương thích ngược. Xem :ref:`arg-parsing-string-and-buffers` để biết mô tả về macro này.

Tất cả các symbol hiển thị với người dùng được định nghĩa bởi :file:`Python.h` đều có tiền tố ``Py`` hoặc ``PY``, ngoại trừ những symbol được định nghĩa trong các tệp header tiêu chuẩn.

.. tip::

   Để tương thích ngược, :file:`Python.h` bao gồm một số tệp header tiêu chuẩn. Các phần mở rộng C nên include những header tiêu chuẩn mà chúng sử dụng và không nên phụ thuộc vào các include ngầm định này. Nếu sử dụng limited C API phiên bản 3.13 trở lên, các include ngầm định là:

   * ``<assert.h>``
   * ``<intrin.h>`` (trên Windows)
   * ``<inttypes.h>``
   * ``<limits.h>``
   * ``<math.h>``
   * ``<stdarg.h>``
   * ``<wchar.h>``
   * ``<sys/types.h>`` (nếu có)

   Nếu :c:macro:`Py_LIMITED_API` chưa được định nghĩa hoặc được đặt ở phiên bản 3.12 trở xuống, các header bên dưới cũng được include:

   * ``<ctype.h>``
   * ``<unistd.h>`` (trên POSIX)

   Nếu :c:macro:`Py_LIMITED_API` chưa được định nghĩa hoặc được đặt thành phiên bản 3.10 hoặc cũ hơn, các header dưới đây cũng được включ vào:

   * ``<errno.h>``
   * ``<stdio.h>``
   * ``<stdlib.h>``
   * ``<string.h>``

Tiếp theo, chúng ta thêm vào tệp module hàm C sẽ được gọi khi biểu thức Python ``spam.system(string)`` được đánh giá (chúng ta sẽ sớm xem cách hàm này được gọi)::

   static PyObject *
   spam_system(PyObject *self, PyObject *args)
   {
       const char *command;
       int sts;

       if (!PyArg_ParseTuple(args, "s", &command))
           return NULL;
       sts = system(command);
       return PyLong_FromLong(sts);
   }

Có một cách chuyển đổi trực tiếp từ danh sách đối số trong Python (ví dụ: biểu thức duy nhất ``"ls -l"``) sang các đối số được truyền cho hàm C. Hàm C luôn có hai đối số, theo quy ước được đặt tên là *self* và *args*.

Đối số *self* trỏ đến đối tượng module đối với các hàm cấp module; đối với một method, nó sẽ trỏ đến instance của đối tượng.

Đối số *args* sẽ là một con trỏ đến đối tượng tuple Python chứa các đối số. Mỗi phần tử của tuple tương ứng với một đối số trong danh sách đối số của lời gọi. Các đối số là các đối tượng Python --- để làm bất kỳ điều gì với chúng trong hàm C, chúng ta phải chuyển đổi chúng thành các giá trị C. Hàm
:c:func:`PyArg_ParseTuple` trong Python API kiểm tra kiểu của các đối số và chuyển đổi chúng thành các giá trị C. Hàm này sử dụng một chuỗi mẫu để xác định các kiểu cần thiết của đối số cũng như kiểu của các biến C dùng để lưu trữ các giá trị đã chuyển đổi. Chúng ta sẽ tìm hiểu thêm về điều này sau.

:c:func:`PyArg_ParseTuple` trả về true (khác 0) nếu tất cả các đối số đều có kiểu phù hợp và các thành phần của chúng đã được lưu vào những biến có địa chỉ được truyền vào. Hàm trả về false (0) nếu một danh sách đối số không hợp lệ được truyền vào. Trong trường hợp sau, hàm cũng đưa ra một exception phù hợp để hàm gọi có thể trả về ``NULL`` ngay lập tức (như chúng ta đã thấy trong ví dụ).


.. _extending-errors:

Xen kẽ: Lỗi và Ngoại lệ
=======================

Một quy ước quan trọng trong toàn bộ trình thông dịch Python là: khi một hàm không thành công, hàm đó phải thiết lập điều kiện ngoại lệ và trả về một giá trị lỗi (thường là ``-1`` hoặc một con trỏ ``NULL``). Thông tin ngoại lệ được lưu trong ba thành viên của trạng thái luồng của trình thông dịch. Khi không có ngoại lệ, các thành viên này là ``NULL``. Nếu không, chúng là các thành phần tương ứng trong C của bộ ba Python được :meth:`sys.exc_info` trả về. Đó là kiểu ngoại lệ, thực thể ngoại lệ và một đối tượng traceback. Biết về chúng là điều quan trọng để hiểu cách các lỗi được truyền đi.

Python API định nghĩa một số hàm để thiết lập nhiều loại ngoại lệ khác nhau.

Hàm phổ biến nhất là :c:func:`PyErr_SetString`. Các đối số của hàm là một đối tượng ngoại lệ và một chuỗi C. Đối tượng ngoại lệ thường là một đối tượng được định nghĩa sẵn như
:c:data:`PyExc_ZeroDivisionError`. Chuỗi C cho biết nguyên nhân của lỗi, được chuyển đổi thành một đối tượng chuỗi Python và lưu dưới dạng "giá trị liên kết" của ngoại lệ.

Một hàm hữu ích khác là :c:func:`PyErr_SetFromErrno`, chỉ nhận một đối số ngoại lệ và tạo giá trị liên kết bằng cách kiểm tra biến toàn cục :c:data:`errno`. Hàm tổng quát nhất là
:c:func:`PyErr_SetObject`, nhận hai đối số đối tượng, gồm ngoại lệ và giá trị liên kết của nó. Bạn không cần :c:func:`Py_INCREF` các đối tượng được truyền cho bất kỳ hàm nào trong số này.

Bạn có thể kiểm tra một cách không gây thay đổi xem một exception đã được thiết lập hay chưa bằng
:c:func:`PyErr_Occurred`.  Lệnh này trả về đối tượng exception hiện tại hoặc ``NULL`` nếu chưa xảy ra exception nào.  Thông thường, bạn không cần gọi
:c:func:`PyErr_Occurred` để kiểm tra xem đã xảy ra lỗi trong một lần gọi hàm hay chưa, vì bạn có thể nhận biết điều đó từ giá trị trả về.

Khi một hàm *f* gọi một hàm khác *g* và phát hiện hàm sau bị lỗi, *f* cũng phải tự trả về một giá trị lỗi (thường là ``NULL`` hoặc ``-1``). Nó *không* được gọi một trong các hàm ``PyErr_*`` --- một hàm như vậy đã được *g* gọi. Sau đó, caller của *f* cũng phải trả về một chỉ báo lỗi cho caller *its*, một lần nữa *không* gọi ``PyErr_*``, v.v. --- nguyên nhân chi tiết nhất của lỗi đã được báo cáo bởi hàm đầu tiên phát hiện ra lỗi. Khi lỗi đến vòng lặp chính của trình thông dịch Python, vòng lặp này sẽ hủy đoạn mã Python hiện đang thực thi và cố gắng tìm một exception handler do lập trình viên Python chỉ định.

(Có những tình huống trong đó một module thực sự có thể cung cấp thông báo lỗi chi tiết hơn bằng cách gọi một hàm ``PyErr_*`` khác, và trong những trường hợp như vậy thì làm vậy là phù hợp. Tuy nhiên, theo nguyên tắc chung, điều này không cần thiết và có thể khiến thông tin về nguyên nhân của lỗi bị mất: hầu hết các thao tác đều có thể thất bại vì nhiều lý do khác nhau.)

Để bỏ qua một exception được thiết lập bởi một lần gọi hàm bị lỗi, điều kiện exception phải được xóa rõ ràng bằng cách gọi :c:func:`PyErr_Clear`. Mã C chỉ nên gọi :c:func:`PyErr_Clear` khi không muốn chuyển lỗi lên trình thông dịch mà muốn tự mình xử lý hoàn toàn (có thể bằng cách thử một phương án khác hoặc giả vờ như không có gì sai).

Mọi lần gọi :c:func:`malloc` bị lỗi đều phải được chuyển thành một exception --- caller trực tiếp của :c:func:`malloc` (hoặc :c:func:`realloc`) phải gọi
:c:func:`PyErr_NoMemory` và tự nó trả về một chỉ báo thất bại. Tất cả các hàm tạo đối tượng (ví dụ: :c:func:`PyLong_FromLong`) đều đã làm điều này, vì vậy lưu ý này chỉ liên quan đến những ai trực tiếp gọi :c:func:`malloc`.

Cũng lưu ý rằng, ngoại trừ trường hợp quan trọng là :c:func:`PyArg_ParseTuple` và các hàm tương tự, những hàm trả về trạng thái dạng số nguyên thường trả về một giá trị dương hoặc bằng không khi thành công và ``-1`` khi thất bại, giống như các system call của Unix.

Cuối cùng, hãy nhớ dọn dẹp các đối tượng rác (bằng cách gọi :c:func:`Py_XDECREF` hoặc
:c:func:`Py_DECREF` cho những đối tượng bạn đã tạo) khi trả về một chỉ báo lỗi!

Bạn hoàn toàn có thể tự chọn exception cần raise. Có các đối tượng C được khai báo sẵn tương ứng với tất cả các exception dựng sẵn của Python, chẳng hạn như
:c:data:`PyExc_ZeroDivisionError`, mà bạn có thể sử dụng trực tiếp. Tất nhiên, bạn nên lựa chọn exception một cách hợp lý --- đừng dùng :c:data:`PyExc_TypeError` để biểu thị rằng không thể mở một tệp (trường hợp đó có lẽ nên dùng :c:data:`PyExc_OSError`). Nếu danh sách đối số có vấn đề, hàm :c:func:`PyArg_ParseTuple` thường raise :c:data:`PyExc_TypeError`. Nếu bạn có một đối số mà giá trị của nó phải nằm trong một phạm vi cụ thể hoặc phải thỏa mãn các điều kiện khác,
:c:data:`PyExc_ValueError` là phù hợp.

Bạn cũng có thể định nghĩa một exception mới dành riêng cho module của mình. Cách đơn giản nhất để thực hiện việc này là khai báo một biến đối tượng toàn cục static ở đầu tệp::

   static PyObject *SpamError = NULL;

và khởi tạo biến đó bằng cách gọi :c:func:`PyErr_NewException` trong hàm
:c:data:`Py_mod_exec` của module (:c:func:`!spam_module_exec`)::

   SpamError = PyErr_NewException("spam.error", NULL, NULL);

Vì :c:data:`!SpamError` là một biến toàn cục, nó sẽ bị ghi đè mỗi khi module được khởi tạo lại, khi hàm :c:data:`Py_mod_exec` được gọi.

Hiện tại, hãy tránh vấn đề này: chúng ta sẽ ngăn việc khởi tạo lặp lại bằng cách raise một
:py:exc:`ImportError`::

   static PyObject *SpamError = NULL;

   static int
   spam_module_exec(PyObject *m)
   {
       if (SpamError != NULL) {
           PyErr_SetString(PyExc_ImportError,
                           "cannot initialize spam module more than once");
           return -1;
       }
       SpamError = PyErr_NewException("spam.error", NULL, NULL);
       if (PyModule_AddObjectRef(m, "SpamError", SpamError) < 0) {
           return -1;
       }

       return 0;
   }

   static PyModuleDef_Slot spam_module_slots[] = {
       {Py_mod_exec, spam_module_exec},
       {0, NULL}
   };

   static struct PyModuleDef spam_module = {
       .m_base = PyModuleDef_HEAD_INIT,
       .m_name = "spam",
       .m_size = 0,  // không âm
       .m_slots = spam_module_slots,
   };

   PyMODINIT_FUNC
   PyInit_spam(void)
   {
       return PyModuleDef_Init(&spam_module);
   }

Lưu ý rằng tên Python của đối tượng exception là :exc:`!spam.error`.  Hàm
:c:func:`PyErr_NewException` có thể tạo một class với base class là :exc:`Exception` (trừ khi một class khác được truyền vào thay cho ``NULL``), được mô tả trong :ref:`bltin-exceptions`.

Cũng lưu ý rằng biến :c:data:`!SpamError` giữ một tham chiếu đến lớp ngoại lệ mới được tạo; đây là chủ ý! Vì ngoại lệ có thể bị mã bên ngoài xóa khỏi module, cần có một tham chiếu sở hữu đến lớp để bảo đảm lớp đó không bị loại bỏ, khiến :c:data:`!SpamError` trở thành con trỏ treo. Nếu trở thành con trỏ treo, mã C thực hiện việc phát sinh ngoại lệ có thể gây ra core dump hoặc các tác dụng phụ ngoài ý muốn khác.

Hiện tại, lệnh gọi :c:func:`Py_DECREF` để xóa tham chiếu này vẫn còn thiếu. Ngay cả khi trình thông dịch Python tắt, biến toàn cục :c:data:`!SpamError` cũng sẽ không được garbage collection. Nó sẽ bị "rò rỉ". Tuy nhiên, chúng ta đã bảo đảm rằng điều này xảy ra nhiều nhất một lần trong mỗi tiến trình.

Phần sau của ví dụ này sẽ thảo luận về việc sử dụng :c:macro:`PyMODINIT_FUNC` làm kiểu trả về của hàm.

Có thể phát sinh ngoại lệ :exc:`!spam.error` trong extension module của bạn bằng cách gọi :c:func:`PyErr_SetString` như minh họa bên dưới::

   static PyObject *
   spam_system(PyObject *self, PyObject *args)
   {
       const char *command;
       int sts;

       if (!PyArg_ParseTuple(args, "s", &command))
           return NULL;
       sts = system(command);
       if (sts < 0) {
           PyErr_SetString(SpamError, "System command failed");
           return NULL;
       }
       return PyLong_FromLong(sts);
   }


.. _backtoexample:

Quay lại ví dụ
==============

Quay lại hàm ví dụ, giờ đây bạn có thể hiểu câu lệnh này::

   if (!PyArg_ParseTuple(args, "s", &command))
       return NULL;

Hàm trả về ``NULL`` (ký hiệu lỗi dành cho các hàm trả về con trỏ đối tượng) nếu phát hiện lỗi trong danh sách đối số, dựa vào ngoại lệ được thiết lập bởi
:c:func:`PyArg_ParseTuple`. Nếu không, giá trị chuỗi của đối số đã được sao chép vào biến cục bộ :c:data:`!command`. Đây là phép gán con trỏ và bạn không được sửa đổi chuỗi mà nó trỏ tới (vì vậy trong Standard C, biến :c:data:`!command` cần được khai báo đúng là ``const char *command``).

Câu lệnh tiếp theo là một lệnh gọi đến hàm Unix :c:func:`system`, truyền cho nó chuỗi mà chúng ta vừa nhận được từ :c:func:`PyArg_ParseTuple`::

   sts = system(command);

Hàm :func:`!spam.system` của chúng ta phải trả về giá trị của :c:data:`!sts` dưới dạng một đối tượng Python. Việc này được thực hiện bằng hàm :c:func:`PyLong_FromLong`.::

   return PyLong_FromLong(sts);

Trong trường hợp này, nó sẽ trả về một đối tượng số nguyên. (Đúng vậy, ngay cả số nguyên cũng là các đối tượng trên heap trong Python!)

Nếu bạn có một hàm C không trả về đối số hữu ích nào (một hàm trả về
:c:expr:`void`), thì hàm Python tương ứng phải trả về ``None``. Bạn cần dùng thành ngữ sau để thực hiện việc đó (được triển khai bằng macro :c:macro:`Py_RETURN_NONE`)::

   Py_INCREF(Py_None);
   return Py_None;

:c:data:`Py_None` là tên C của đối tượng Python đặc biệt ``None``. Đây là một đối tượng Python thực sự chứ không phải một con trỏ ``NULL``, vốn có nghĩa là "lỗi" trong hầu hết các ngữ cảnh, như chúng ta đã thấy.


.. _methodtable:

Bảng phương thức và Hàm khởi tạo của Module
===========================================

Tôi đã hứa sẽ chỉ cho bạn cách :c:func:`!spam_system` được gọi từ các chương trình Python. Trước tiên, chúng ta cần liệt kê tên và địa chỉ của nó trong một "bảng phương thức"::

   static PyMethodDef spam_methods[] = {
       ...
       {"system",  spam_system, METH_VARARGS,
        "Execute a shell command."},
       ...
       {NULL, NULL, 0, NULL}        /* Phần tử đánh dấu kết thúc */
   };

Hãy lưu ý mục thứ ba (``METH_VARARGS``). Đây là một cờ cho trình thông dịch biết quy ước gọi nào sẽ được sử dụng cho hàm C. Thông thường, giá trị này luôn phải là ``METH_VARARGS`` hoặc ``METH_VARARGS | METH_KEYWORDS``; giá trị ``0`` có nghĩa là một biến thể lỗi thời của :c:func:`PyArg_ParseTuple` được sử dụng.

Khi chỉ sử dụng ``METH_VARARGS``, hàm phải chờ các tham số ở cấp Python được truyền vào dưới dạng một tuple có thể được phân tích cú pháp thông qua
:c:func:`PyArg_ParseTuple`; bên dưới có cung cấp thêm thông tin về hàm này.

Có thể đặt bit :c:macro:`METH_KEYWORDS` trong trường thứ ba nếu cần truyền các đối số từ khóa cho hàm. Trong trường hợp này, hàm C phải chấp nhận tham số ``PyObject *`` thứ ba, là một dictionary chứa các từ khóa. Sử dụng :c:func:`PyArg_ParseTupleAndKeywords` để phân tích cú pháp các đối số cho một hàm như vậy.

Bảng phương thức phải được tham chiếu trong cấu trúc định nghĩa module::

   static struct PyModuleDef spam_module = {
       ...
       .m_methods = spam_methods,
       ...
   };

Cấu trúc này, đến lượt nó, phải được truyền cho interpreter trong hàm khởi tạo của module. Hàm khởi tạo phải có tên là
:c:func:`!PyInit_name`, trong đó *name* là tên của module và phải là mục duy nhất không phải \ ``static`` được định nghĩa trong tệp module::

   PyMODINIT_FUNC
   PyInit_spam(void)
   {
       return PyModuleDef_Init(&spam_module);
   }

Lưu ý rằng :c:macro:`PyMODINIT_FUNC` khai báo hàm với kiểu trả về là ``PyObject *``, khai báo mọi liên kết đặc biệt cần thiết cho nền tảng, và đối với C++ thì khai báo hàm là ``extern "C"``.

:c:func:`!PyInit_spam` được gọi khi mỗi interpreter lần đầu import module của nó
:mod:`!spam`. (Xem bên dưới để biết các nhận xét về việc nhúng Python.) Một con trỏ đến định nghĩa module phải được trả về thông qua :c:func:`PyModuleDef_Init`, để cơ chế import có thể tạo module và lưu trữ module đó trong ``sys.modules``.

Khi nhúng Python, hàm :c:func:`!PyInit_spam` không được tự động gọi trừ khi có một mục nhập trong bảng :c:data:`PyImport_Inittab`. Để thêm module vào bảng khởi tạo, hãy sử dụng :c:func:`PyImport_AppendInittab`, tùy chọn theo sau là thao tác import module::

   #define PY_SSIZE_T_CLEAN
   #include <Python.h>

   int
   main(int argc, char *argv[])
   {
       PyStatus status;
       PyConfig config;
       PyConfig_InitPythonConfig(&config);

       /* Thêm một mô-đun tích hợp trước Py_Initialize */
       if (PyImport_AppendInittab("spam", PyInit_spam) == -1) {
           fprintf(stderr, "Error: could not extend in-built modules table\n");
           exit(1);
       }

       /* Truyền argv[0] cho trình thông dịch Python */
       status = PyConfig_SetBytesString(&config, &config.program_name, argv[0]);
       if (PyStatus_Exception(status)) {
           goto exception;
       }

       /* Khởi tạo trình thông dịch Python. Bắt buộc.
          Nếu bước này thất bại, đó sẽ là lỗi nghiêm trọng. */
       status = Py_InitializeFromConfig(&config);
       if (PyStatus_Exception(status)) {
           goto exception;
       }
       PyConfig_Clear(&config);

       /* Tùy chọn import mô-đun; hoặc,
          có thể hoãn việc import cho đến khi tập lệnh nhúng
          để mã Python import mô-đun. */
       PyObject *pmodule = PyImport_ImportModule("spam");
       if (!pmodule) {
           PyErr_Print();
           fprintf(stderr, "Error: could not import module 'spam'\n");
       }

       // ... sử dụng Python C API ở đây ...

       return 0;

     exception:
        PyConfig_Clear(&config);
        Py_ExitStatusException(status);
   }

.. note::

   Nếu bạn khai báo một biến toàn cục hoặc một biến static cục bộ, module có thể gặp các tác dụng phụ ngoài ý muốn khi khởi tạo lại, chẳng hạn như khi xóa các mục khỏi ``sys.modules`` hoặc nhập các module đã biên dịch vào nhiều interpreter trong cùng một tiến trình (hoặc sau một :c:func:`fork` mà không có một :c:func:`exec` xen giữa). Nếu trạng thái module chưa được :ref:`cô lập <isolating-extensions-howto>` hoàn toàn, tác giả nên cân nhắc đánh dấu module là không hỗ trợ subinterpreter (thông qua :c:macro:`Py_MOD_MULTIPLE_INTERPRETERS_NOT_SUPPORTED`).

Một module mẫu đầy đủ hơn được cung cấp trong bản phân phối mã nguồn Python dưới dạng :file:`Modules/xxlimited.c`. Bạn có thể dùng tệp này làm mẫu hoặc chỉ đọc để tham khảo.


.. _compilation:

Biên dịch và liên kết
=====================

Còn hai việc cần thực hiện trước khi bạn có thể sử dụng extension mới: biên dịch và liên kết nó với hệ thống Python. Nếu bạn sử dụng dynamic loading, chi tiết có thể phụ thuộc vào kiểu dynamic loading mà hệ thống của bạn sử dụng; hãy xem các chương về xây dựng extension module (chương :ref:`building`) và thông tin bổ sung chỉ áp dụng cho việc xây dựng trên Windows (chương
:ref:`building-on-windows`) để biết thêm thông tin về vấn đề này.

Nếu bạn không thể sử dụng dynamic loading, hoặc muốn biến module của mình thành một phần cố định của Python interpreter, bạn sẽ phải thay đổi cấu hình thiết lập và xây dựng lại interpreter. May mắn là việc này rất đơn giản trên Unix: chỉ cần đặt tệp của bạn (ví dụ :file:`spammodule.c`) vào thư mục :file:`Modules/` của bản phân phối mã nguồn đã giải nén, rồi thêm một dòng vào tệp
:file:`Modules/Setup.local` mô tả tệp của bạn:

.. code-block:: sh

   spam spammodule.o

và xây dựng lại interpreter bằng cách chạy :program:`make` trong thư mục cấp cao nhất. Bạn cũng có thể chạy :program:`make` trong thư mục con :file:`Modules/`, nhưng trước tiên bạn phải xây dựng lại :file:`Makefile` ở đó bằng cách chạy ':program:`make` Makefile'. (Việc này là cần thiết mỗi khi bạn thay đổi
tệp :file:`Setup`.)

Nếu module của bạn yêu cầu liên kết với các thư viện bổ sung, bạn cũng có thể liệt kê chúng trên dòng tương ứng trong tệp cấu hình, chẳng hạn như:

.. code-block:: sh

   spam spammodule.o -lX11


.. _callingpython:

Gọi các hàm Python từ C
=======================

Cho đến nay, chúng ta đã tập trung vào việc cho phép gọi các hàm C từ Python. Chiều ngược lại cũng hữu ích: gọi các hàm Python từ C. Điều này đặc biệt đúng với các thư viện hỗ trợ cái gọi là hàm "callback". Nếu một giao diện C sử dụng callback, phần tương đương trong Python thường cần cung cấp một cơ chế callback cho lập trình viên Python; phần triển khai sẽ yêu cầu gọi các hàm callback Python từ một callback C. Cũng có thể hình dung những trường hợp sử dụng khác.

May mắn là interpreter Python có thể dễ dàng được gọi đệ quy, và có một giao diện tiêu chuẩn để gọi một hàm Python. (Nếu bạn quan tâm đến cách gọi trình phân tích cú pháp Python với một chuỗi cụ thể làm đầu vào, hãy xem :ref:`veryhigh`.)

Việc gọi một hàm Python rất đơn giản. Trước tiên, chương trình Python phải bằng cách nào đó truyền cho bạn đối tượng hàm Python. Bạn nên cung cấp một hàm (hoặc một giao diện khác) để thực hiện việc này. Khi hàm này được gọi, hãy lưu một con trỏ đến đối tượng hàm Python (hãy cẩn thận :c:func:`Py_INCREF` nó!) vào một biến toàn cục — hoặc bất cứ nơi nào bạn thấy phù hợp. Ví dụ, hàm sau đây có thể là một phần của định nghĩa module::

   static PyObject *my_callback = NULL;

   static PyObject *
   my_set_callback(PyObject *dummy, PyObject *args)
   {
       PyObject *result = NULL;
       PyObject *temp;

       if (PyArg_ParseTuple(args, "O:set_callback", &temp)) {
           if (!PyCallable_Check(temp)) {
               PyErr_SetString(PyExc_TypeError, "parameter must be callable");
               return NULL;
           }
           Py_XINCREF(temp);         /* Thêm tham chiếu đến callback mới */
           Py_XDECREF(my_callback);  /* Hủy callback trước đó */
           my_callback = temp;       /* Lưu callback mới */
           /* Mã khuôn mẫu để trả về "None" */
           Py_INCREF(Py_None);
           result = Py_None;
       }
       return result;
   }

Hàm này phải được đăng ký với interpreter bằng cách sử dụng
cờ :c:macro:`METH_VARARGS`; nội dung này được mô tả trong phần :ref:`methodtable`.
Hàm :c:func:`PyArg_ParseTuple` và các đối số của nó được ghi chép trong phần
:ref:`parsetuple`.

Các macro :c:func:`Py_XINCREF` và :c:func:`Py_XDECREF` tăng/giảm reference count của một đối tượng và an toàn khi có các con trỏ ``NULL`` (nhưng lưu ý rằng *temp* sẽ không được ``NULL`` trong ngữ cảnh này). Xem thêm thông tin về chúng trong phần :ref:`refcounts`.

.. index:: single: PyObject_CallObject (C function)

Sau đó, khi đến lúc gọi hàm, bạn gọi hàm C
:c:func:`PyObject_CallObject`. Hàm này có hai đối số, cả hai đều là con trỏ đến các đối tượng Python bất kỳ: hàm Python và danh sách đối số. Danh sách đối số luôn phải là một đối tượng tuple, với độ dài bằng số lượng đối số. Để gọi hàm Python mà không có đối số, hãy truyền ``NULL``, hoặc một tuple rỗng; để gọi hàm với một đối số, hãy truyền một tuple singleton.
:c:func:`Py_BuildValue` trả về một tuple khi chuỗi format của nó bao gồm từ không đến nhiều format code đặt trong dấu ngoặc đơn. Ví dụ::

   int arg;
   PyObject *arglist;
   PyObject *result;
   ...
   arg = 123;
   ...
   /* Đến lúc gọi callback */
   arglist = Py_BuildValue("(i)", arg);
   result = PyObject_CallObject(my_callback, arglist);
   Py_DECREF(arglist);

:c:func:`PyObject_CallObject` trả về một con trỏ đến đối tượng Python: đây là giá trị trả về của hàm Python. :c:func:`PyObject_CallObject` không làm thay đổi số lượng tham chiếu đối với các đối số của nó. Trong ví dụ, một tuple mới đã được tạo để làm danh sách đối số, và tuple này sẽ được
:c:func:`Py_DECREF`\ -ed ngay sau lệnh gọi :c:func:`PyObject_CallObject`.

Giá trị trả về của :c:func:`PyObject_CallObject` là "mới": hoặc đó là một đối tượng hoàn toàn mới, hoặc đó là một đối tượng hiện có nhưng số lượng tham chiếu của nó đã được tăng lên. Vì vậy, trừ khi bạn muốn lưu nó vào một biến toàn cục, bằng cách nào đó bạn nên :c:func:`Py_DECREF` kết quả, ngay cả (đặc biệt là!) khi bạn không quan tâm đến giá trị của nó.

Tuy nhiên, trước khi thực hiện việc này, điều quan trọng là phải kiểm tra xem giá trị trả về có phải là ``NULL`` hay không. Nếu đúng như vậy, hàm Python đã kết thúc bằng cách phát sinh một ngoại lệ. Nếu mã C gọi :c:func:`PyObject_CallObject` được gọi từ Python, lúc này nó nên trả về một chỉ báo lỗi cho bên gọi Python, để interpreter có thể in stack trace hoặc mã Python gọi nó có thể xử lý ngoại lệ. Nếu điều này không thể thực hiện hoặc không nên thực hiện, ngoại lệ cần được xóa bằng cách gọi
:c:func:`PyErr_Clear`. Ví dụ::

   if (result == NULL)
       return NULL; /* Truyền lỗi trở lại */
   ...use result...
   Py_DECREF(result);

Tùy thuộc vào interface mong muốn cho hàm callback Python, bạn cũng có thể phải cung cấp một danh sách đối số cho :c:func:`PyObject_CallObject`. Trong một số trường hợp, danh sách đối số cũng được chương trình Python cung cấp thông qua cùng interface đã chỉ định hàm callback. Khi đó, danh sách này có thể được lưu lại và sử dụng giống như đối tượng hàm. Trong các trường hợp khác, bạn có thể phải tạo một tuple mới để truyền làm danh sách đối số. Cách đơn giản nhất để thực hiện việc này là gọi :c:func:`Py_BuildValue`. Ví dụ: nếu muốn truyền một mã sự kiện dạng số nguyên, bạn có thể sử dụng đoạn mã sau::

   PyObject *arglist;
   ...
   arglist = Py_BuildValue("(l)", eventcode);
   result = PyObject_CallObject(my_callback, arglist);
   Py_DECREF(arglist);
   if (result == NULL)
       return NULL; /* Truyền lỗi trở lại */
   /* Có thể sử dụng kết quả tại đây */
   Py_DECREF(result);

Hãy lưu ý vị trí của ``Py_DECREF(arglist)`` ngay sau lời gọi, trước khi kiểm tra lỗi! Đồng thời, cần lưu ý rằng nói một cách nghiêm ngặt, đoạn mã này chưa hoàn chỉnh:
:c:func:`Py_BuildValue` có thể hết bộ nhớ, và cần kiểm tra trường hợp này.

Bạn cũng có thể gọi một hàm với các đối số từ khóa bằng cách sử dụng
:c:func:`PyObject_Call`, hỗ trợ cả đối số và đối số từ khóa. Như trong ví dụ trên, chúng ta sử dụng :c:func:`Py_BuildValue` để tạo dictionary.::

   PyObject *dict;
   ...
   dict = Py_BuildValue("{s:i}", "name", val);
   result = PyObject_Call(my_callback, NULL, dict);
   Py_DECREF(dict);
   if (result == NULL)
       return NULL; /* Truyền lỗi trở lại */
   /* Có thể sử dụng kết quả tại đây */
   Py_DECREF(result);


.. _parsetuple:

Trích xuất tham số trong các hàm mở rộng
========================================

.. index:: single: PyArg_ParseTuple (C function)

Hàm :c:func:`PyArg_ParseTuple` được khai báo như sau::

   int PyArg_ParseTuple(PyObject *arg, const char *format, ...);

Đối số *arg* phải là một đối tượng tuple chứa danh sách đối số được truyền từ Python đến một hàm C. Đối số *format* phải là một chuỗi định dạng, với cú pháp được giải thích trong :ref:`arg-parsing` của Sổ tay tham khảo Python/C API. Các đối số còn lại phải là địa chỉ của các biến có kiểu được xác định bởi chuỗi định dạng.

Lưu ý rằng mặc dù :c:func:`PyArg_ParseTuple` kiểm tra các kiểu bắt buộc của đối số Python, nó không thể kiểm tra tính hợp lệ của địa chỉ các biến C được truyền vào lời gọi: nếu mắc lỗi ở đó, mã của bạn có thể sẽ bị crash hoặc ít nhất ghi đè các bit ngẫu nhiên trong bộ nhớ. Vì vậy, hãy cẩn thận!

Lưu ý rằng mọi tham chiếu đến đối tượng Python được cung cấp cho caller đều là tham chiếu *borrowed*; không được giảm reference count của chúng!

Một số lời gọi mẫu::

   #define PY_SSIZE_T_CLEAN
   #include <Python.h>

::

   int ok;
   int i, j;
   long k, l;
   const char *s;
   Py_ssize_t size;

   ok = PyArg_ParseTuple(args, ""); /* Không có đối số */
       /* Lời gọi Python: f() */

::

   ok = PyArg_ParseTuple(args, "s", &s); /* Một chuỗi */
       /* Lời gọi Python có thể có: f('whoops!') */

::

   ok = PyArg_ParseTuple(args, "lls", &k, &l, &s); /* Hai long và một chuỗi */
       /* Lời gọi Python có thể có: f(1, 2, 'three') */

::

   ok = PyArg_ParseTuple(args, "(ii)s#", &i, &j, &s, &size);
       /* Một cặp int và một chuỗi, đồng thời trả về kích thước chuỗi */
       /* Lời gọi Python có thể có: f((1, 2), 'three') */

::

   {
       const char *file;
       const char *mode = "r";
       int bufsize = 0;
       ok = PyArg_ParseTuple(args, "s|si", &file, &mode, &bufsize);
       /* Một chuỗi, cùng với tùy chọn một chuỗi khác và một số nguyên */
       /* Các lời gọi Python có thể có:
          f('spam')
          f('spam', 'w')
          f('spam', 'wb', 100000) */
   }

::

   {
       int left, top, right, bottom, h, v;
       ok = PyArg_ParseTuple(args, "((ii)(ii))(ii)",
                &left, &top, &right, &bottom, &h, &v);
       /* Một hình chữ nhật và một điểm */
       /* Lời gọi Python có thể có:
          f(((0, 0), (400, 300)), (10, 10)) */
   }

::

   {
       Py_complex c;
       ok = PyArg_ParseTuple(args, "D:myfunction", &c);
       /* một số phức, đồng thời cung cấp tên hàm cho lỗi */
       /* Lời gọi Python có thể có: myfunction(1+2j) */
   }


.. _parsetupleandkeywords:

Tham số từ khóa cho các hàm mở rộng
===================================

.. index:: single: PyArg_ParseTupleAndKeywords (C function)

Hàm :c:func:`PyArg_ParseTupleAndKeywords` được khai báo như sau::

   int PyArg_ParseTupleAndKeywords(PyObject *arg, PyObject *kwdict,
                                   const char *format, char * const *kwlist, ...);

Các tham số *arg* và *format* giống hệt các tham số của
:c:func:`PyArg_ParseTuple` hàm. Tham số *kwdict* là từ điển các keyword nhận được dưới dạng tham số thứ ba từ Python runtime. Tham số *kwlist* là danh sách chuỗi kết thúc bằng ``NULL``, dùng để xác định các tham số; tên được đối chiếu với thông tin kiểu từ *format* theo thứ tự từ trái sang phải. Khi thành công, :c:func:`PyArg_ParseTupleAndKeywords` trả về true; nếu không, nó trả về false và phát sinh ngoại lệ phù hợp.

.. note::

   Không thể phân tích các tuple lồng nhau khi sử dụng keyword arguments! Các keyword parameter được truyền vào nhưng không có trong *kwlist* sẽ khiến :exc:`TypeError` được phát sinh.

.. index:: single: Philbrick, Geoff

Sau đây là một module mẫu sử dụng keyword, dựa trên một ví dụ của Geoff Philbrick (philbrick@hks.com)::

   #define PY_SSIZE_T_CLEAN
   #include <Python.h>

   static PyObject *
   keywdarg_parrot(PyObject *self, PyObject *args, PyObject *keywds)
   {
       int voltage;
       const char *state = "a stiff";
       const char *action = "voom";
       const char *type = "Norwegian Blue";

       static char *kwlist[] = {"voltage", "state", "action", "type", NULL};

       if (!PyArg_ParseTupleAndKeywords(args, keywds, "i|sss", kwlist,
                                        &voltage, &state, &action, &type))
           return NULL;

       printf("-- This parrot wouldn't %s if you put %i Volts through it.\n",
              action, voltage);
       printf("-- Lovely plumage, the %s -- It's %s!\n", type, state);

       Py_RETURN_NONE;
   }

   static PyMethodDef keywdarg_methods[] = {
       /* Ép kiểu hàm là cần thiết vì các giá trị PyCFunction
        * chỉ nhận hai tham số PyObject*, còn keywdarg_parrot() nhận
        * ba tham số.
        */
       {"parrot", (PyCFunction)(void(*)(void))keywdarg_parrot, METH_VARARGS | METH_KEYWORDS,
        "Print a lovely skit to standard output."},
       {NULL, NULL, 0, NULL}   /* phần tử đánh dấu kết thúc */
   };

   static struct PyModuleDef keywdarg_module = {
       .m_base = PyModuleDef_HEAD_INIT,
       .m_name = "keywdarg",
       .m_size = 0,
       .m_methods = keywdarg_methods,
   };

   PyMODINIT_FUNC
   PyInit_keywdarg(void)
   {
       return PyModuleDef_Init(&keywdarg_module);
   }


.. _buildvalue:

Xây dựng các giá trị tùy ý
==========================

Hàm này là hàm tương ứng với :c:func:`PyArg_ParseTuple`. Hàm được khai báo như sau::

   PyObject *Py_BuildValue(const char *format, ...);

Hàm này nhận diện một tập hợp các đơn vị định dạng tương tự như các đơn vị được nhận diện bởi
:c:func:`PyArg_ParseTuple`, nhưng các đối số (là đầu vào của hàm, không phải đầu ra) không được là con trỏ mà phải là các giá trị. Hàm trả về một đối tượng Python mới, thích hợp để trả về từ một hàm C được gọi từ Python.

Một điểm khác biệt so với :c:func:`PyArg_ParseTuple` là: trong khi hàm sau yêu cầu đối số đầu tiên của nó phải là một tuple (vì các danh sách đối số Python luôn được biểu diễn dưới dạng tuple ở bên trong), :c:func:`Py_BuildValue` không phải lúc nào cũng tạo một tuple. Hàm chỉ tạo một tuple nếu chuỗi định dạng chứa từ hai đơn vị định dạng trở lên. Nếu chuỗi định dạng rỗng, hàm trả về ``None``; nếu chuỗi chứa chính xác một đơn vị định dạng, hàm trả về đối tượng được mô tả bởi đơn vị định dạng đó. Để buộc hàm trả về một tuple có kích thước 0 hoặc 1, hãy đặt chuỗi định dạng trong dấu ngoặc đơn.

Ví dụ (lệnh gọi ở bên trái, giá trị Python nhận được ở bên phải):

.. code-block:: none

   Py_BuildValue("")                        None
   Py_BuildValue("i", 123)                  123
   Py_BuildValue("iii", 123, 456, 789)      (123, 456, 789)
   Py_BuildValue("s", "hello")              'hello'
   Py_BuildValue("y", "hello")              b'hello'
   Py_BuildValue("ss", "hello", "world")    ('hello', 'world')
   Py_BuildValue("s#", "hello", 4)          'hell'
   Py_BuildValue("y#", "hello", 4)          b'hell'
   Py_BuildValue("()")                      ()
   Py_BuildValue("(i)", 123)                (123,)
   Py_BuildValue("(ii)", 123, 456)          (123, 456)
   Py_BuildValue("(i,i)", 123, 456)         (123, 456)
   Py_BuildValue("[i,i]", 123, 456)         [123, 456]
   Py_BuildValue("{s:i,s:i}",
                 "abc", 123, "def", 456)    {'abc': 123, 'def': 456}
   Py_BuildValue("((ii)(ii)) (ii)",
                 1, 2, 3, 4, 5, 6)          (((1, 2), (3, 4)), (5, 6))


.. _refcounts:

Bộ đếm tham chiếu
=================

Trong các ngôn ngữ như C hoặc C++, lập trình viên chịu trách nhiệm cấp phát và giải phóng động bộ nhớ trên heap. Trong C, việc này được thực hiện bằng các hàm
:c:func:`malloc` và :c:func:`free`. Trong C++, các toán tử ``new`` và ``delete`` được dùng với ý nghĩa về cơ bản giống nhau, và chúng ta sẽ giới hạn phần thảo luận sau đây trong trường hợp C.

Mỗi khối bộ nhớ được cấp phát bằng :c:func:`malloc` cuối cùng phải được trả lại vùng bộ nhớ khả dụng bằng đúng một lần gọi :c:func:`free`. Việc gọi :c:func:`free` đúng thời điểm là rất quan trọng. Nếu địa chỉ của một khối bị quên nhưng :c:func:`free` không được gọi cho khối đó, vùng bộ nhớ mà nó chiếm giữ không thể được sử dụng lại cho đến khi chương trình kết thúc. Đây được gọi là :dfn:`rò rỉ bộ nhớ`. Mặt khác, nếu một chương trình gọi :c:func:`free` cho một khối rồi tiếp tục sử dụng khối đó, nó sẽ tạo ra xung đột với việc tái sử dụng khối thông qua một lần gọi :c:func:`malloc` khác. Đây được gọi là :dfn:`sử dụng bộ nhớ đã được giải phóng`. Điều này gây ra những hậu quả tồi tệ giống như việc tham chiếu dữ liệu chưa được khởi tạo --- kết xuất core, kết quả sai và các sự cố khó hiểu.

Những nguyên nhân phổ biến của rò rỉ bộ nhớ là các đường đi bất thường trong mã. Chẳng hạn, một hàm có thể cấp phát một khối bộ nhớ, thực hiện một số phép tính rồi lại giải phóng khối đó. Sau đó, một thay đổi trong yêu cầu đối với hàm có thể bổ sung một phép kiểm tra vào quá trình tính toán để phát hiện điều kiện lỗi và trả về sớm khỏi hàm. Khi thực hiện việc thoát sớm này, rất dễ quên giải phóng khối bộ nhớ đã cấp phát, đặc biệt khi đoạn mã đó được bổ sung sau. Một khi đã xuất hiện, những rò rỉ như vậy thường không bị phát hiện trong thời gian dài: nhánh thoát do lỗi chỉ được thực hiện trong một phần rất nhỏ của tổng số lần gọi, và hầu hết các máy hiện đại đều có nhiều bộ nhớ ảo, vì vậy rò rỉ chỉ trở nên rõ ràng trong một tiến trình chạy lâu và thường xuyên sử dụng hàm gây rò rỉ. Do đó, điều quan trọng là ngăn rò rỉ xảy ra bằng cách áp dụng một quy ước hoặc chiến lược lập trình giúp giảm thiểu loại lỗi này.

Vì Python sử dụng nhiều :c:func:`malloc` và :c:func:`free`, nó cũng cần một chiến lược để tránh rò rỉ bộ nhớ cũng như việc sử dụng bộ nhớ đã được giải phóng. Phương pháp được chọn có tên là :dfn:`đếm tham chiếu`. Nguyên tắc rất đơn giản: mỗi đối tượng chứa một bộ đếm, bộ đếm này được tăng lên khi một tham chiếu đến đối tượng được lưu ở đâu đó và được giảm xuống khi một tham chiếu đến đối tượng bị xóa. Khi bộ đếm đạt đến số 0, tham chiếu cuối cùng đến đối tượng đã bị xóa và đối tượng được giải phóng.

Một chiến lược thay thế có tên là :dfn:`thu gom rác tự động`. (Đôi khi, đếm tham chiếu cũng được xem là một chiến lược thu gom rác, do đó từ "tự động" được dùng để phân biệt hai phương pháp.) Ưu điểm lớn của thu gom rác tự động là người dùng không cần gọi
:c:func:`free` một cách tường minh. (Một ưu điểm khác được cho là cải thiện tốc độ hoặc mức sử dụng bộ nhớ --- tuy nhiên đây không phải là sự thật chắc chắn.) Nhược điểm là đối với C, không có trình thu gom rác tự động nào thực sự portable, trong khi việc đếm tham chiếu có thể được triển khai theo cách portable (miễn là các hàm :c:func:`malloc` và :c:func:`free` khả dụng --- điều mà C Standard đảm bảo). Có lẽ một ngày nào đó sẽ có một trình thu gom rác tự động đủ portable cho C. Cho đến lúc đó, chúng ta sẽ phải sử dụng đếm tham chiếu.

Mặc dù Python sử dụng cách triển khai đếm tham chiếu truyền thống, nó cũng cung cấp một bộ phát hiện chu kỳ để phát hiện các chu kỳ tham chiếu. Điều này cho phép các ứng dụng không phải lo lắng về việc tạo ra các tham chiếu vòng trực tiếp hoặc gián tiếp; đây là điểm yếu của cơ chế thu gom rác chỉ được triển khai bằng cách đếm tham chiếu. Các chu kỳ tham chiếu bao gồm những đối tượng chứa các tham chiếu (có thể là gián tiếp) đến chính chúng, khiến mỗi đối tượng trong chu kỳ có số lượng tham chiếu khác không. Các cách triển khai đếm tham chiếu điển hình không thể thu hồi bộ nhớ thuộc về bất kỳ đối tượng nào trong một chu kỳ tham chiếu hoặc được các đối tượng trong chu kỳ tham chiếu đến, mặc dù không còn tham chiếu nào khác đến chính chu kỳ đó.

Bộ phát hiện chu kỳ có thể phát hiện các chu kỳ rác và thu hồi chúng. Module :mod:`gc` cung cấp một cách để chạy bộ phát hiện (the
hàm :func:`~gc.collect`), cũng như các giao diện cấu hình và khả năng vô hiệu hóa bộ phát hiện trong runtime.


.. _refcountsinpython:

Đếm tham chiếu trong Python
---------------------------

Có hai macro, ``Py_INCREF(x)`` và ``Py_DECREF(x)``, xử lý việc tăng và giảm số đếm tham chiếu. :c:func:`Py_DECREF` cũng giải phóng đối tượng khi số đếm đạt đến 0. Để linh hoạt, nó không gọi
:c:func:`free` trực tiếp --- thay vào đó, nó gọi thông qua một con trỏ hàm trong :dfn:`đối tượng kiểu` của đối tượng. Vì mục đích này (và các mục đích khác), mọi đối tượng cũng chứa một con trỏ đến đối tượng kiểu của nó.

Câu hỏi lớn còn lại là: khi nào nên sử dụng ``Py_INCREF(x)`` và ``Py_DECREF(x)``? Trước tiên, hãy giới thiệu một số thuật ngữ. Không ai "sở hữu" một đối tượng; tuy nhiên, bạn có thể
:dfn:`sở hữu một tham chiếu` đến một đối tượng. Khi đó, số đếm tham chiếu của một đối tượng được định nghĩa là số lượng tham chiếu được sở hữu đến đối tượng đó. Chủ sở hữu của một tham chiếu có trách nhiệm gọi :c:func:`Py_DECREF` khi tham chiếu đó không còn cần thiết. Quyền sở hữu một tham chiếu có thể được chuyển giao. Có ba cách để xử lý một tham chiếu được sở hữu: chuyển nó đi, lưu trữ nó hoặc gọi :c:func:`Py_DECREF`. Quên xử lý một tham chiếu được sở hữu sẽ tạo ra rò rỉ bộ nhớ.

Cũng có thể :dfn:`mượn` [#]_ một tham chiếu đến một đối tượng. Bên mượn tham chiếu không được gọi :c:func:`Py_DECREF`. Bên mượn không được giữ đối tượng lâu hơn chủ sở hữu mà từ đó nó được mượn. Việc sử dụng một tham chiếu đã mượn sau khi chủ sở hữu đã hủy đối tượng có nguy cơ sử dụng bộ nhớ đã được giải phóng và nên hoàn toàn tránh [#]_.

Ưu điểm của việc mượn thay vì sở hữu một tham chiếu là bạn không cần lo việc hủy tham chiếu trên mọi đường đi có thể qua mã --- nói cách khác, với một tham chiếu đã mượn, bạn không có nguy cơ gây rò rỉ khi thoát sớm. Nhược điểm của việc mượn thay vì sở hữu là có một số tình huống tinh vi mà trong mã có vẻ đúng, một tham chiếu đã mượn lại có thể được sử dụng sau khi chủ sở hữu mà từ đó nó được mượn thực tế đã hủy nó.

Có thể chuyển một tham chiếu đã mượn thành một tham chiếu sở hữu bằng cách gọi
:c:func:`Py_INCREF`. Việc này không ảnh hưởng đến trạng thái của chủ sở hữu mà từ đó tham chiếu được mượn --- nó tạo ra một tham chiếu sở hữu mới và trao đầy đủ trách nhiệm của chủ sở hữu (chủ sở hữu mới phải hủy tham chiếu đúng cách, cũng như chủ sở hữu trước đó).


.. _ownershiprules:

Quy tắc sở hữu
--------------

Bất cứ khi nào một tham chiếu đối tượng được truyền vào hoặc truyền ra khỏi một hàm, việc quyền sở hữu có được chuyển cùng với tham chiếu hay không là một phần trong đặc tả giao diện của hàm.

Hầu hết các hàm trả về một tham chiếu đến đối tượng đều chuyển quyền sở hữu cùng với tham chiếu đó. Cụ thể, tất cả các hàm có nhiệm vụ tạo một đối tượng mới, chẳng hạn như :c:func:`PyLong_FromLong` và :c:func:`Py_BuildValue`, đều chuyển quyền sở hữu cho bên nhận. Ngay cả khi đối tượng thực tế không mới, bạn vẫn nhận quyền sở hữu một tham chiếu mới đến đối tượng đó. Ví dụ,
:c:func:`PyLong_FromLong` duy trì bộ nhớ đệm các giá trị phổ biến và có thể trả về một tham chiếu đến mục được lưu trong bộ nhớ đệm.

Nhiều hàm trích xuất các đối tượng từ những đối tượng khác cũng chuyển quyền sở hữu cùng với tham chiếu, chẳng hạn như :c:func:`PyObject_GetAttrString`. Tuy nhiên, ở đây vấn đề không hoàn toàn rõ ràng, vì một vài routine phổ biến là ngoại lệ:
:c:func:`PyTuple_GetItem`, :c:func:`PyList_GetItem`, :c:func:`PyDict_GetItem`, và
:c:func:`PyDict_GetItemString` đều trả về các tham chiếu được mượn từ tuple, list hoặc dictionary.

Hàm :c:func:`PyImport_AddModule` cũng trả về một tham chiếu được mượn, mặc dù thực tế nó có thể tạo ra đối tượng được trả về: điều này có thể thực hiện được vì một tham chiếu sở hữu đối tượng được lưu trong ``sys.modules``.

Khi bạn truyền một tham chiếu đối tượng vào một hàm khác, nhìn chung, hàm đó mượn tham chiếu từ bạn --- nếu cần lưu trữ tham chiếu, hàm sẽ sử dụng
:c:func:`Py_INCREF` để trở thành chủ sở hữu độc lập. Có đúng hai ngoại lệ quan trọng cho quy tắc này: :c:func:`PyTuple_SetItem` và
:c:func:`PyList_SetItem`. Các hàm này tiếp nhận quyền sở hữu đối với đối tượng được truyền cho chúng --- ngay cả khi chúng thất bại! (Lưu ý rằng :c:func:`PyDict_SetItem` và các hàm tương tự không tiếp nhận quyền sở hữu --- chúng là các hàm "bình thường." )

Khi một hàm C được gọi từ Python, hàm đó mượn các tham chiếu đến những đối số của mình từ bên gọi. Bên gọi sở hữu một tham chiếu đến đối tượng, vì vậy thời gian tồn tại của tham chiếu mượn được bảo đảm cho đến khi hàm trả về. Chỉ khi cần lưu trữ hoặc truyền tiếp một tham chiếu mượn như vậy, tham chiếu đó mới phải được chuyển thành tham chiếu sở hữu bằng cách gọi :c:func:`Py_INCREF`.

Tham chiếu đối tượng được trả về từ một hàm C được gọi từ Python phải là một tham chiếu sở hữu --- quyền sở hữu được chuyển từ hàm sang bên gọi.


.. _thinice:

Băng mỏng
---------

Có một vài tình huống mà việc sử dụng tưởng như vô hại một tham chiếu mượn có thể dẫn đến sự cố. Tất cả đều liên quan đến những lần gọi ngầm trình thông dịch, có thể khiến bên sở hữu một tham chiếu giải phóng tham chiếu đó.

Trường hợp đầu tiên và quan trọng nhất cần biết là sử dụng :c:func:`Py_DECREF` trên một đối tượng không liên quan trong khi đang mượn tham chiếu đến một phần tử danh sách. Ví dụ:::

   void
   bug(PyObject *list)
   {
       PyObject *item = PyList_GetItem(list, 0);

       PyList_SetItem(list, 1, PyLong_FromLong(0L));
       PyObject_Print(item, stdout, 0); /* LỖI! */
   }

Hàm này trước tiên mượn một tham chiếu đến ``list[0]``, sau đó thay thế ``list[1]`` bằng giá trị ``0``, và cuối cùng in tham chiếu đã mượn. Có vẻ vô hại, đúng không? Nhưng không phải vậy!

Hãy lần theo luồng điều khiển đến :c:func:`PyList_SetItem`. Danh sách sở hữu các tham chiếu đến tất cả phần tử của nó, vì vậy khi phần tử 1 được thay thế, danh sách phải giải phóng phần tử 1 ban đầu. Bây giờ, hãy giả sử phần tử 1 ban đầu là một instance của lớp do người dùng định nghĩa, và giả sử thêm rằng lớp đó định nghĩa một
phương thức :meth:`!__del__`. Nếu instance của lớp này có số lượng tham chiếu là 1, việc giải phóng nó sẽ gọi phương thức :meth:`!__del__` của nó. Về mặt nội bộ,
:c:func:`PyList_SetItem` gọi :c:func:`Py_DECREF` trên phần tử được thay thế, và thao tác này gọi hàm tương ứng của phần tử được thay thế là
hàm :c:member:`~PyTypeObject.tp_dealloc`. Trong quá trình giải phóng, :c:member:`~PyTypeObject.tp_dealloc` gọi
:c:member:`~PyTypeObject.tp_finalize`, được ánh xạ tới
phương thức :meth:`!__del__` đối với các instance của lớp (xem :pep:`442`). Toàn bộ chuỗi này diễn ra đồng bộ trong lời gọi :c:func:`PyList_SetItem`.

Vì được viết bằng Python, phương thức :meth:`!__del__` có thể thực thi mã Python tùy ý. Liệu nó có thể làm gì đó để làm mất hiệu lực tham chiếu đến ``item`` trong :c:func:`!bug` không? Chắc chắn là có! Giả sử danh sách được truyền vào
:c:func:`!bug` có thể truy cập được đối với phương thức :meth:`!__del__`, phương thức này có thể thực thi một câu lệnh tương tự như ``del list[0]``, và nếu giả sử đây là tham chiếu cuối cùng đến đối tượng đó, nó sẽ giải phóng bộ nhớ được liên kết với đối tượng, từ đó làm ``item`` không còn hợp lệ.

Khi đã biết nguồn gốc của vấn đề, cách giải quyết rất đơn giản: tạm thời tăng số lượng tham chiếu. Phiên bản đúng của hàm là::

   void
   no_bug(PyObject *list)
   {
       PyObject *item = PyList_GetItem(list, 0);

       Py_INCREF(item);
       PyList_SetItem(list, 1, PyLong_FromLong(0L));
       PyObject_Print(item, stdout, 0);
       Py_DECREF(item);
   }

Đây là một câu chuyện có thật. Một phiên bản cũ của Python từng chứa các biến thể của lỗi này, và có người đã mất khá nhiều thời gian trong trình gỡ lỗi C để tìm ra lý do các phương thức :meth:`!__del__` của mình bị lỗi...

Trường hợp thứ hai của các vấn đề với tham chiếu mượn là một biến thể liên quan đến thread. Thông thường, nhiều thread trong trình thông dịch Python không thể cản trở lẫn nhau, vì có một :term:`khóa toàn cục <global interpreter lock>` bảo vệ toàn bộ không gian đối tượng của Python. Tuy nhiên, có thể tạm thời giải phóng khóa này bằng macro
:c:macro:`Py_BEGIN_ALLOW_THREADS`, và lấy lại khóa bằng
:c:macro:`Py_END_ALLOW_THREADS`. Điều này thường được thực hiện quanh các lệnh gọi I/O chặn, để các thread khác có thể sử dụng bộ xử lý trong khi chờ I/O hoàn tất. Rõ ràng, hàm sau đây gặp vấn đề giống như hàm trước đó::

   void
   bug(PyObject *list)
   {
       PyObject *item = PyList_GetItem(list, 0);
       Py_BEGIN_ALLOW_THREADS
       ...some blocking I/O call...
       Py_END_ALLOW_THREADS
       PyObject_Print(item, stdout, 0); /* LỖI! */
   }


.. _nullpointers:

Con trỏ NULL
------------

Nhìn chung, các hàm nhận tham chiếu đối tượng làm đối số không mong bạn truyền cho chúng các con trỏ ``NULL``, và sẽ gây kết xuất core (hoặc gây ra các lần kết xuất core sau đó) nếu bạn làm vậy. Các hàm trả về tham chiếu đối tượng thường chỉ trả về ``NULL`` để cho biết đã xảy ra một ngoại lệ. Lý do không kiểm tra các đối số ``NULL`` là vì các hàm thường chuyển tiếp những đối tượng mà chúng nhận được cho các hàm khác --- nếu mỗi hàm đều kiểm tra ``NULL``, sẽ có rất nhiều phép kiểm tra dư thừa và mã sẽ chạy chậm hơn.

Tốt hơn là chỉ kiểm tra ``NULL`` tại "nguồn:" khi nhận được một con trỏ có thể là ``NULL``, chẳng hạn như từ :c:func:`malloc` hoặc từ một hàm có thể phát sinh ngoại lệ.

Các macro :c:func:`Py_INCREF` và :c:func:`Py_DECREF` không kiểm tra các con trỏ ``NULL`` --- tuy nhiên, các biến thể :c:func:`Py_XINCREF` và :c:func:`Py_XDECREF` của chúng thì có.

Các macro dùng để kiểm tra một kiểu đối tượng cụ thể (``Pytype_Check()``) không kiểm tra các con trỏ ``NULL`` --- một lần nữa, có rất nhiều mã gọi liên tiếp một số macro này để kiểm tra một đối tượng với nhiều kiểu dự kiến khác nhau, và điều này sẽ tạo ra các phép kiểm tra dư thừa. Không có biến thể nào thực hiện kiểm tra ``NULL``.

Cơ chế gọi hàm C đảm bảo rằng danh sách đối số được truyền cho các hàm C (``args`` trong các ví dụ) không bao giờ là ``NULL`` --- thực tế, cơ chế này đảm bảo rằng nó luôn là một tuple [#]_.

Để một con trỏ ``NULL`` "thoát" đến người dùng Python là một lỗi nghiêm trọng.

.. Frank Stajano:
   A pedagogically buggy example, along the lines of the previous listing, would
   be helpful here -- showing in more concrete terms what sort of actions could
   cause the problem. I can't very well imagine it from the description.


.. _cplusplus:

Viết phần mở rộng bằng C++
==========================

Có thể viết các module mở rộng bằng C++. Có một số hạn chế. Nếu chương trình chính (trình thông dịch Python) được biên dịch và liên kết bằng trình biên dịch C, thì không thể sử dụng các đối tượng toàn cục hoặc tĩnh có hàm khởi tạo. Đây không phải là vấn đề nếu chương trình chính được liên kết bằng trình biên dịch C++. Các hàm sẽ được trình thông dịch Python gọi (đặc biệt là các hàm khởi tạo module) phải được khai báo bằng ``extern "C"``. Không cần đặt các tệp header của Python trong ``extern "C" {...}`` --- chúng đã sử dụng dạng này nếu ký hiệu ``__cplusplus`` được định nghĩa (tất cả các trình biên dịch C++ gần đây đều định nghĩa ký hiệu này).


.. _using-capsules:

Cung cấp API C cho một module mở rộng
=====================================

.. sectionauthor:: Konrad Hinsen <hinsen@cnrs-orleans.fr>


Nhiều module mở rộng chỉ cung cấp các hàm và kiểu mới để sử dụng từ Python, nhưng đôi khi mã trong một module mở rộng có thể hữu ích cho các module mở rộng khác. Ví dụ, một module mở rộng có thể triển khai một kiểu "collection" hoạt động giống như các list nhưng không có thứ tự. Cũng như kiểu list Python tiêu chuẩn có một API C cho phép các module mở rộng tạo và thao tác với các list, kiểu collection mới này cũng nên có một tập hợp các hàm C để các module mở rộng khác thao tác trực tiếp.

Thoạt nhìn, việc này có vẻ dễ: chỉ cần viết các hàm (tất nhiên là không khai báo chúng bằng ``static``), cung cấp một tệp header phù hợp và ghi lại tài liệu về API C. Và thực tế, cách này sẽ hoạt động nếu tất cả các module mở rộng luôn được liên kết tĩnh với trình thông dịch Python. Tuy nhiên, khi các module được sử dụng dưới dạng shared library, các symbol được định nghĩa trong một module có thể không hiển thị với module khác. Chi tiết về khả năng hiển thị phụ thuộc vào hệ điều hành; một số hệ thống sử dụng một namespace toàn cục cho trình thông dịch Python và tất cả các module mở rộng (ví dụ như Windows), trong khi các hệ thống khác yêu cầu một danh sách tường minh các symbol được import tại thời điểm liên kết module (AIX là một ví dụ), hoặc cung cấp lựa chọn giữa nhiều chiến lược khác nhau (phần lớn các hệ thống Unix). Và ngay cả khi các symbol hiển thị trên toàn cục, module chứa các hàm mà ta muốn gọi có thể vẫn chưa được tải!

Do đó, để đảm bảo tính portable, không được đưa ra bất kỳ giả định nào về khả năng hiển thị của symbol. Điều này có nghĩa là tất cả các symbol trong module mở rộng phải được khai báo bằng ``static``, ngoại trừ hàm khởi tạo module, nhằm tránh xung đột tên với các module mở rộng khác (như đã thảo luận trong phần
:ref:`methodtable`). Đồng thời, các symbol mà *should* có thể được các module mở rộng khác truy cập phải được export theo một cách khác.

Python cung cấp một cơ chế đặc biệt để truyền thông tin ở cấp C (các con trỏ) từ module mở rộng này sang module mở rộng khác: Capsules. Capsule là một kiểu dữ liệu Python lưu trữ một con trỏ (:c:expr:`void \*`). Các Capsule chỉ có thể được tạo và truy cập thông qua API C của chúng, nhưng có thể được truyền đi như bất kỳ đối tượng Python nào khác. Cụ thể, chúng có thể được gán cho một tên trong namespace của module mở rộng. Sau đó, các module mở rộng khác có thể import module này, lấy giá trị của tên đó, rồi lấy con trỏ từ Capsule.

Có nhiều cách sử dụng Capsules để export C API của một extension module. Mỗi hàm có thể có Capsule riêng, hoặc tất cả con trỏ C API có thể được lưu trong một mảng mà địa chỉ của mảng được công bố trong một Capsule. Ngoài ra, các tác vụ lưu trữ và truy xuất những con trỏ này có thể được phân chia theo nhiều cách khác nhau giữa module cung cấp mã và các client module.

Dù chọn phương pháp nào, việc đặt tên đúng cho các Capsule là rất quan trọng. Hàm :c:func:`PyCapsule_New` nhận một tham số name (:c:expr:`const char \*`); bạn được phép truyền vào một tên ``NULL``, nhưng chúng tôi đặc biệt khuyến khích bạn chỉ định một tên. Các Capsule được đặt tên đúng cung cấp một mức độ type-safety tại runtime; không có cách khả thi nào để phân biệt Capsule không có tên này với Capsule không có tên khác.

Cụ thể, các Capsule được dùng để expose C API nên được đặt tên theo quy ước sau::

    modulename.attributename

Hàm tiện ích :c:func:`PyCapsule_Import` giúp dễ dàng load một C API được cung cấp thông qua Capsule, nhưng chỉ khi tên của Capsule khớp với quy ước này. Hành vi này giúp người dùng C API có mức độ chắc chắn cao rằng Capsule họ load chứa đúng C API.

Ví dụ sau minh họa một phương pháp đặt phần lớn công việc lên người viết module export, phù hợp với các module thư viện được sử dụng phổ biến. Phương pháp này lưu tất cả con trỏ C API (chỉ có một con trỏ trong ví dụ!) trong một mảng các con trỏ :c:expr:`void`, rồi dùng mảng đó làm giá trị của một Capsule. Tệp header tương ứng với module cung cấp một macro đảm nhiệm việc import module và truy xuất các con trỏ C API; các client module chỉ cần gọi macro này trước khi truy cập C API.

Module export là một phiên bản sửa đổi của module :mod:`!spam` trong phần
:ref:`extending-simpleexample`. Hàm :func:`!spam.system` không gọi trực tiếp hàm thư viện C :c:func:`system`, mà gọi một hàm
:c:func:`!PySpam_System`, tất nhiên trong thực tế sẽ thực hiện điều gì đó phức tạp hơn (chẳng hạn như thêm "spam" vào mọi lệnh). Hàm này
:c:func:`!PySpam_System` cũng được export sang các extension module khác.

Hàm :c:func:`!PySpam_System` là một hàm C thuần túy, được khai báo ``static`` như mọi thứ khác::

   static int
   PySpam_System(const char *command)
   {
       return system(command);
   }

Hàm :c:func:`!spam_system` được sửa đổi theo một cách đơn giản::

   static PyObject *
   spam_system(PyObject *self, PyObject *args)
   {
       const char *command;
       int sts;

       if (!PyArg_ParseTuple(args, "s", &command))
           return NULL;
       sts = PySpam_System(command);
       return PyLong_FromLong(sts);
   }

Ở phần đầu của module, ngay sau dòng::

   #include <Python.h>

cần thêm hai dòng nữa::

   #định nghĩa SPAM_MODULE
   #include "spammodule.h"

``#define`` được dùng để cho tệp header biết rằng nó đang được include trong exporting module, không phải client module. Cuối cùng, hàm :c:data:`mod_exec <Py_mod_exec>` của module phải đảm nhiệm việc khởi tạo mảng con trỏ C API::

   static int
   spam_module_exec(PyObject *m)
   {
       static void *PySpam_API[PySpam_API_pointers];
       PyObject *c_api_object;

       /* Khởi tạo mảng con trỏ C API */
       PySpam_API[PySpam_System_NUM] = (void *)PySpam_System;

       /* Tạo Capsule chứa địa chỉ của mảng con trỏ API */
       c_api_object = PyCapsule_New((void *)PySpam_API, "spam._C_API", NULL);

       if (PyModule_Add(m, "_C_API", c_api_object) < 0) {
           return -1;
       }

       return 0;
   }

Lưu ý rằng ``PySpam_API`` được khai báo ``static``; nếu không, mảng con trỏ sẽ biến mất khi :c:func:`!PyInit_spam` kết thúc!

Phần lớn công việc nằm trong tệp header :file:`spammodule.h`, có dạng như sau::

   #ifndef Py_SPAMMODULE_H
   #define Py_SPAMMODULE_H
   #ifdef __cplusplus
   extern "C" {
   #endif

   /* Tệp header cho spammodule */

   /* Các hàm C API */
   #define PySpam_System_NUM 0
   #define PySpam_System_RETURN int
   #define PySpam_System_PROTO (const char *command)

   /* Tổng số con trỏ C API */
   #define PySpam_API_pointers 1


   #ifdef SPAM_MODULE
   /* Phần này được dùng khi biên dịch spammodule.c */

   static PySpam_System_RETURN PySpam_System PySpam_System_PROTO;

   #else
   /* Phần này được dùng trong các mô-đun dùng API của spammodule */

   static void **PySpam_API;

   #define PySpam_System \
    (*(PySpam_System_RETURN (*)PySpam_System_PROTO) PySpam_API[PySpam_System_NUM])

   /* Trả về -1 khi có lỗi, 0 khi thành công.
    * PyCapsule_Import sẽ thiết lập một ngoại lệ nếu có lỗi.
    */
   static int
   import_spam(void)
   {
       PySpam_API = (void **)PyCapsule_Import("spam._C_API", 0);
       return (PySpam_API != NULL) ? 0 : -1;
   }

   #endif

   #ifdef __cplusplus
   }
   #endif

   #endif /* !defined(Py_SPAMMODULE_H) */

Tất cả những gì một module client cần làm để có quyền truy cập vào hàm
:c:func:`!PySpam_System` là cách gọi hàm (hay đúng hơn là macro)
:c:func:`!import_spam` trong hàm :c:data:`mod_exec <Py_mod_exec>` của nó::

   static int
   client_module_exec(PyObject *m)
   {
       if (import_spam() < 0) {
           return -1;
       }
       /* có thể thực hiện khởi tạo bổ sung tại đây */
       return 0;
   }

Nhược điểm chính của cách tiếp cận này là tệp :file:`spammodule.h` khá phức tạp. Tuy nhiên, cấu trúc cơ bản giống nhau đối với mỗi hàm được export, vì vậy chỉ cần học một lần.

Cuối cùng, cần đề cập rằng Capsules cung cấp thêm chức năng, đặc biệt hữu ích cho việc cấp phát và giải phóng bộ nhớ của con trỏ được lưu trong một Capsule. Các chi tiết được mô tả trong Python/C API Reference Manual, tại phần :ref:`capsules` và trong phần triển khai Capsules (các tệp
:file:`Include/pycapsule.h` và :file:`Objects/capsule.c` trong bản phân phối mã nguồn Python).

.. rubric:: Chú thích cuối trang

.. [#] Một interface cho hàm này đã tồn tại trong module chuẩn :mod:`os` --- nó được chọn làm ví dụ đơn giản và dễ hiểu.

.. [#] Ẩn dụ về việc “mượn” một tham chiếu không hoàn toàn chính xác: chủ sở hữu vẫn giữ một bản sao của tham chiếu đó.

.. [#] Việc kiểm tra xem số lượng tham chiếu có ít nhất là 1 **không hoạt động** --- bản thân số lượng tham chiếu có thể nằm trong vùng nhớ đã được giải phóng và do đó có thể được tái sử dụng cho một đối tượng khác!

.. [#] Những bảo đảm này không áp dụng khi bạn sử dụng quy ước gọi "cũ" --- quy ước này vẫn xuất hiện trong nhiều đoạn mã hiện có.

.. _`cffi`: https://cffi.readthedocs.io/
