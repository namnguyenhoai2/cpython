.. highlight:: c


.. _veryhigh:

***************
Lớp cấp rất cao
***************

Các hàm trong chương này cho phép bạn thực thi mã nguồn Python được cung cấp trong một tệp hoặc bộ đệm, nhưng không cho phép bạn tương tác với trình thông dịch theo cách chi tiết hơn.

Một số hàm trong đó nhận một ký hiệu bắt đầu từ văn phạm làm tham số. Các ký hiệu bắt đầu có sẵn là :c:data:`Py_eval_input`,
:c:data:`Py_file_input`, :c:data:`Py_single_input`, và
:c:data:`Py_func_type_input`. Các ký hiệu này được mô tả sau những hàm nhận chúng làm tham số.

Cũng lưu ý rằng một số hàm trong đó nhận các tham số :c:expr:`FILE*`. Một vấn đề đặc biệt cần được xử lý cẩn thận là cấu trúc :c:type:`FILE` của các thư viện C khác nhau có thể khác nhau và không tương thích. Ít nhất là trên Windows, các phần mở rộng được liên kết động thực sự có thể sử dụng các thư viện khác nhau, vì vậy cần đảm bảo rằng các tham số :c:expr:`FILE*` chỉ được truyền cho những hàm này khi chắc chắn rằng chúng được tạo bởi cùng thư viện mà runtime Python đang sử dụng.


.. c:function:: int PyRun_AnyFile(FILE *fp, const char *filename)

   Đây là giao diện đơn giản hóa cho :c:func:`PyRun_AnyFileExFlags` bên dưới, trong đó *closeit* được đặt thành ``0`` và *flags* được đặt thành ``NULL``.


.. c:function:: int PyRun_AnyFileFlags(FILE *fp, const char *filename, PyCompilerFlags *flags)

   Đây là một giao diện đơn giản hóa cho :c:func:`PyRun_AnyFileExFlags` bên dưới, giữ đối số *closeit* ở giá trị ``0``.


.. c:function:: int PyRun_AnyFileEx(FILE *fp, const char *filename, int closeit)

   Đây là một giao diện đơn giản hóa cho :c:func:`PyRun_AnyFileExFlags` bên dưới, giữ đối số *flags* ở giá trị ``NULL``.


.. c:function:: int PyRun_AnyFileExFlags(FILE *fp, const char *filename, int closeit, PyCompilerFlags *flags)

   Nếu *fp* tham chiếu đến một tệp liên kết với thiết bị tương tác (bảng điều khiển hoặc đầu vào từ terminal, hay pseudo-terminal Unix), trả về giá trị của
   :c:func:`PyRun_InteractiveLoop`, nếu không thì trả về kết quả của
   :c:func:`PyRun_SimpleFile`. *filename* được giải mã từ encoding của filesystem (:func:`sys.getfilesystemencoding`). Nếu *filename* là ``NULL``, hàm này sử dụng ``"???"`` làm tên tệp. Nếu *closeit* là true, tệp sẽ được đóng trước khi ``PyRun_SimpleFileExFlags()`` trả về.


.. c:function:: int PyRun_SimpleString(const char *command)

   Đây là một giao diện đơn giản hóa cho :c:func:`PyRun_SimpleStringFlags` bên dưới, giữ đối số :c:struct:`PyCompilerFlags`\* ở giá trị ``NULL``.


.. c:function:: int PyRun_SimpleStringFlags(const char *command, PyCompilerFlags *flags)

   Thực thi mã nguồn Python từ *command* trong module :mod:`__main__` theo đối số *flags*. Nếu :mod:`__main__` chưa tồn tại, nó sẽ được tạo. Trả về ``0`` khi thành công hoặc ``-1`` nếu xảy ra ngoại lệ. Nếu có lỗi, không có cách nào lấy được thông tin về ngoại lệ. Để biết ý nghĩa của *flags*, hãy xem phần bên dưới.

   Lưu ý rằng nếu một :exc:`SystemExit` không được xử lý theo cách khác được phát sinh, hàm này sẽ không trả về ``-1`` mà sẽ thoát khỏi tiến trình, miễn là
   :c:member:`PyConfig.inspect` bằng không.


.. c:function:: int PyRun_SimpleFile(FILE *fp, const char *filename)

   Đây là một giao diện đơn giản hóa đối với :c:func:`PyRun_SimpleFileExFlags` bên dưới, trong đó *closeit* được giữ ở ``0`` và *flags* được giữ ở ``NULL``.


.. c:function:: int PyRun_SimpleFileEx(FILE *fp, const char *filename, int closeit)

   Đây là một giao diện đơn giản hóa đối với :c:func:`PyRun_SimpleFileExFlags` bên dưới, trong đó *flags* được giữ ở ``NULL``.


.. c:function:: int PyRun_SimpleFileExFlags(FILE *fp, const char *filename, int closeit, PyCompilerFlags *flags)

   Tương tự như :c:func:`PyRun_SimpleStringFlags`, nhưng mã nguồn Python được đọc từ *fp* thay vì từ một chuỗi trong bộ nhớ. *filename* phải là tên của tệp; tệp được giải mã từ :term:`filesystem encoding and error handler`. Nếu *closeit* là true, tệp sẽ được đóng trước khi ``PyRun_SimpleFileExFlags()`` trả về.

   .. note::
      Trên Windows, *fp* nên được mở ở chế độ nhị phân (ví dụ: ``fopen(filename, "rb")``). Nếu không, Python có thể không xử lý đúng tệp script có phần kết dòng LF.


.. c:function:: int PyRun_InteractiveOneObject(FILE *fp, PyObject *filename, PyCompilerFlags *flags)

   Đọc và thực thi một câu lệnh duy nhất từ một tệp được liên kết với thiết bị tương tác theo đối số *flags*. Người dùng sẽ được nhắc nhập bằng ``sys.ps1`` và ``sys.ps2``. *filename* phải là một Python
   đối tượng :class:`str`.

   Trả về ``0`` khi đầu vào được thực thi thành công, ``-1`` nếu có ngoại lệ hoặc mã lỗi từ tệp include :file:`errcode.h` được phân phối cùng Python nếu xảy ra lỗi phân tích cú pháp. (Lưu ý rằng :file:`errcode.h` không được include bởi
   :file:`Python.h`, vì vậy phải được include riêng nếu cần.)


.. c:function:: int PyRun_InteractiveOne(FILE *fp, const char *filename)

   Đây là giao diện đơn giản hóa cho :c:func:`PyRun_InteractiveOneFlags` bên dưới, giữ *flags* ở mức ``NULL``.


.. c:function:: int PyRun_InteractiveOneFlags(FILE *fp, const char *filename, PyCompilerFlags *flags)

   Tương tự như :c:func:`PyRun_InteractiveOneObject`, nhưng *filename* là một
   :c:expr:`const char*`, được giải mã từ
   :term:`filesystem encoding and error handler`.


.. c:function:: int PyRun_InteractiveLoop(FILE *fp, const char *filename)

   Đây là giao diện đơn giản hóa cho :c:func:`PyRun_InteractiveLoopFlags` bên dưới, giữ *flags* ở mức ``NULL``.


.. c:function:: int PyRun_InteractiveLoopFlags(FILE *fp, const char *filename, PyCompilerFlags *flags)

   Đọc và thực thi các câu lệnh từ một tệp được liên kết với thiết bị tương tác cho đến khi đạt EOF. Người dùng sẽ được nhắc nhập bằng ``sys.ps1`` và ``sys.ps2``. *filename* được giải mã từ :term:`filesystem encoding and error handler`. Trả về ``0`` khi gặp EOF hoặc một số âm nếu xảy ra lỗi.


.. c:var:: int (*PyOS_InputHook)(void)

   Có thể được thiết lập để trỏ đến một hàm có prototype ``int func(void)``. Hàm này sẽ được gọi khi dấu nhắc của trình thông dịch Python sắp chuyển sang trạng thái nhàn rỗi và chờ người dùng nhập dữ liệu từ terminal. Giá trị trả về bị bỏ qua. Việc ghi đè hook này có thể được dùng để tích hợp dấu nhắc của trình thông dịch với các event loop khác, như được thực hiện trong :file:`Modules/_tkinter.c` trong mã nguồn Python.

   .. versionchanged:: 3.12
      Hàm này chỉ được gọi từ
      :ref:`trình thông dịch chính <sub-interpreter-support>`.


.. c:var:: char* (*PyOS_ReadlineFunctionPointer)(FILE *, FILE *, const char *)

   Có thể được thiết lập để trỏ đến một hàm có prototype ``char *func(FILE *stdin, FILE *stdout, char *prompt)``, ghi đè hàm mặc định được dùng để đọc một dòng đầu vào tại dấu nhắc của trình thông dịch. Hàm này phải xuất chuỗi *prompt* nếu chuỗi đó không phải là ``NULL``, sau đó đọc một dòng đầu vào từ tệp đầu vào tiêu chuẩn được cung cấp và trả về chuỗi nhận được. Ví dụ, module :mod:`readline` thiết lập hook này để cung cấp các tính năng chỉnh sửa dòng và tự động hoàn tất bằng phím Tab.

   Kết quả phải là một chuỗi được cấp phát bởi :c:func:`PyMem_RawMalloc` hoặc
   :c:func:`PyMem_RawRealloc`, hoặc ``NULL`` nếu xảy ra lỗi.

   .. versionchanged:: 3.4
      Kết quả phải được cấp phát bởi :c:func:`PyMem_RawMalloc` hoặc
      :c:func:`PyMem_RawRealloc`, thay vì được cấp phát bởi
      :c:func:`PyMem_Malloc` hoặc :c:func:`PyMem_Realloc`.

   .. versionchanged:: 3.12
      Hàm này chỉ được gọi từ
      :ref:`trình thông dịch chính <sub-interpreter-support>`.

.. c:function:: PyObject* PyRun_String(const char *str, int start, PyObject *globals, PyObject *locals)

   Đây là giao diện đơn giản hóa cho :c:func:`PyRun_StringFlags` bên dưới, để *flags* được đặt thành ``NULL``.


.. c:function:: PyObject* PyRun_StringFlags(const char *str, int start, PyObject *globals, PyObject *locals, PyCompilerFlags *flags)

   Thực thi mã nguồn Python từ *str* trong ngữ cảnh được chỉ định bởi các đối tượng *globals* và *locals*, với các cờ của trình biên dịch được chỉ định bởi *flags*.  *globals* phải là một từ điển; *locals* có thể là bất kỳ đối tượng nào triển khai mapping protocol. Tham số *start* chỉ định ký hiệu bắt đầu và phải là một trong các :ref:`ký hiệu bắt đầu khả dụng <start-symbols>`.

   Trả về kết quả thực thi mã dưới dạng một đối tượng Python hoặc ``NULL`` nếu xảy ra ngoại lệ.


.. c:function:: PyObject* PyRun_File(FILE *fp, const char *filename, int start, PyObject *globals, PyObject *locals)

   Đây là giao diện đơn giản hóa cho :c:func:`PyRun_FileExFlags` bên dưới, trong đó *closeit* được đặt thành ``0`` và *flags* được đặt thành ``NULL``.


.. c:function:: PyObject* PyRun_FileEx(FILE *fp, const char *filename, int start, PyObject *globals, PyObject *locals, int closeit)

   Đây là giao diện đơn giản hóa cho :c:func:`PyRun_FileExFlags` bên dưới, trong đó *flags* được đặt thành ``NULL``.


.. c:function:: PyObject* PyRun_FileFlags(FILE *fp, const char *filename, int start, PyObject *globals, PyObject *locals, PyCompilerFlags *flags)

   Đây là giao diện đơn giản hóa cho :c:func:`PyRun_FileExFlags` bên dưới, trong đó *closeit* được đặt thành ``0``.


.. c:function:: PyObject* PyRun_FileExFlags(FILE *fp, const char *filename, int start, PyObject *globals, PyObject *locals, int closeit, PyCompilerFlags *flags)

   Tương tự như :c:func:`PyRun_StringFlags`, nhưng mã nguồn Python được đọc từ *fp* thay vì từ một chuỗi trong bộ nhớ. *filename* phải là tên của tệp; tệp được giải mã từ :term:`filesystem encoding and error handler`. Nếu *closeit* là true, tệp sẽ được đóng trước khi :c:func:`PyRun_FileExFlags` trả về.


.. c:function:: PyObject* Py_CompileString(const char *str, const char *filename, int start)

   Đây là giao diện đơn giản hóa cho :c:func:`Py_CompileStringFlags` bên dưới, trong đó *flags* được đặt thành ``NULL``.


.. c:function:: PyObject* Py_CompileStringFlags(const char *str, const char *filename, int start, PyCompilerFlags *flags)

   Đây là giao diện đơn giản hóa cho :c:func:`Py_CompileStringExFlags` bên dưới, trong đó *optimize* được đặt thành ``-1``.


.. c:function:: PyObject* Py_CompileStringObject(const char *str, PyObject *filename, int start, PyCompilerFlags *flags, int optimize)

   Phân tích cú pháp và biên dịch mã nguồn Python trong *str*, trả về code object tương ứng. Ký hiệu bắt đầu được chỉ định bởi *start*; có thể dùng ký hiệu này để giới hạn mã có thể được biên dịch và ký hiệu đó phải thuộc :ref:`available start symbols <start-symbols>`. Tên tệp được chỉ định bởi *filename* được dùng để tạo code object và có thể xuất hiện trong traceback hoặc
   :exc:`SyntaxError` thông báo ngoại lệ. Hàm này trả về ``NULL`` nếu không thể phân tích cú pháp hoặc biên dịch mã.

   Số nguyên *optimize* chỉ định mức tối ưu hóa của compiler; giá trị ``-1`` sẽ chọn mức tối ưu hóa của interpreter như được nêu trong
   :option:`-O` options. Các mức tường minh là ``0`` (không tối ưu hóa; ``__debug__`` là true), ``1`` (các câu lệnh assert bị loại bỏ, ``__debug__`` là false) hoặc ``2`` (docstring cũng bị loại bỏ).

   .. versionadded:: 3.4


.. c:function:: PyObject* Py_CompileStringExFlags(const char *str, const char *filename, int start, PyCompilerFlags *flags, int optimize)

   Tương tự :c:func:`Py_CompileStringObject`, nhưng *filename* là một chuỗi byte được giải mã từ :term:`filesystem encoding and error handler`.

   .. versionadded:: 3.2

.. c:function:: PyObject* PyEval_EvalCode(PyObject *co, PyObject *globals, PyObject *locals)

   Đây là interface đơn giản hóa cho :c:func:`PyEval_EvalCodeEx`, chỉ gồm code object cùng các biến global và local. Các đối số còn lại được đặt thành ``NULL``.


.. c:function:: PyObject* PyEval_EvalCodeEx(PyObject *co, PyObject *globals, PyObject *locals, PyObject *const *args, int argcount, PyObject *const *kws, int kwcount, PyObject *const *defs, int defcount, PyObject *kwdefs, PyObject *closure)

   Đánh giá một code object đã được biên dịch trước, với một môi trường cụ thể cho việc đánh giá. Môi trường này gồm một dictionary các biến global, một mapping object các biến local, các mảng đối số, từ khóa và giá trị mặc định, một dictionary các giá trị mặc định cho đối số :ref:`keyword-only <keyword-only_parameter>` và một tuple closure gồm các cell.


.. c:function:: PyObject* PyEval_EvalFrame(PyFrameObject *f)

   Đánh giá một execution frame. Đây là giao diện đơn giản hóa cho
   :c:func:`PyEval_EvalFrameEx`, để tương thích ngược.


.. c:function:: PyObject* PyEval_EvalFrameEx(PyFrameObject *f, int throwflag)

   Đây là hàm nguyên bản chính của quá trình diễn giải Python. Đối tượng mã liên kết với execution frame *f* được thực thi, diễn giải bytecode và thực hiện các lệnh gọi khi cần. Tham số bổ sung *throwflag* phần lớn có thể được bỏ qua - nếu là true, tham số này sẽ khiến một exception được ném ngay lập tức; nó được dùng cho các phương thức :meth:`~generator.throw` của các đối tượng generator.

   .. versionchanged:: 3.4
      Hàm này hiện bao gồm một debug assertion để giúp đảm bảo rằng nó không âm thầm loại bỏ một exception đang hoạt động.


.. c:function:: int PyEval_MergeCompilerFlags(PyCompilerFlags *cf)

   Hàm này thay đổi các flag của evaluation frame hiện tại và trả về true nếu thành công, false nếu thất bại.


.. c:struct:: PyCompilerFlags

   Đây là cấu trúc dùng để lưu các compiler flag. Trong trường hợp mã chỉ được biên dịch, cấu trúc này được truyền dưới dạng ``int flags``, còn trong trường hợp mã được thực thi, nó được truyền dưới dạng ``PyCompilerFlags *flags``. Trong trường hợp này, ``from __future__ import`` có thể sửa đổi *flags*.

   Bất cứ khi nào ``PyCompilerFlags *flags`` là ``NULL``, :c:member:`~PyCompilerFlags.cf_flags` được xem là bằng ``0``, và mọi sửa đổi do ``from __future__ import`` đều bị loại bỏ.

   .. c:member:: int cf_flags

      Các cờ trình biên dịch.

   .. c:member:: int cf_feature_version

      *cf_feature_version* là phiên bản minor của Python. Nó phải được khởi tạo thành ``PY_MINOR_VERSION``.

      Theo mặc định, trường này bị bỏ qua; nó được sử dụng khi và chỉ khi cờ ``PyCF_ONLY_AST`` được đặt trong :c:member:`~PyCompilerFlags.cf_flags`.

   .. versionchanged:: 3.8
      Đã thêm trường *cf_feature_version*.

   Các cờ trình biên dịch hiện có có thể được truy cập dưới dạng macro:

   .. c:namespace:: NULL

   .. c:macro:: PyCF_ALLOW_TOP_LEVEL_AWAIT
                PyCF_ONLY_AST PyCF_OPTIMIZED_AST PyCF_TYPE_COMMENTS

      Xem :ref:`compiler flags <ast-compiler-flags>` trong tài liệu của
      Mô-đun Python :py:mod:`!ast`, xuất các hằng số này với cùng tên.

   .. rubric:: Cờ cấp thấp

   Các cờ và mặt nạ sau đây phục vụ những nhu cầu chuyên biệt của thư viện chuẩn và các trình thông dịch tương tác. Mã bên ngoài thư viện chuẩn hiếm khi có lý do để sử dụng chúng. Chúng được xem là chi tiết triển khai và có thể thay đổi bất cứ lúc nào.

   .. c:macro:: PyCF_ALLOW_INCOMPLETE_INPUT

      Cờ này là một giao diện riêng tư giữa trình biên dịch và
      mô-đun :mod:`codeop`. Không được sử dụng nó; hành vi của nó không được hỗ trợ và có thể thay đổi mà không có cảnh báo.

      Khi cờ này được thiết lập, nếu quá trình biên dịch thất bại vì văn bản nguồn kết thúc tại nơi cần thêm dữ liệu đầu vào, chẳng hạn ở giữa một khối thụt lề hoặc một literal chuỗi chưa được kết thúc, lỗi được phát sinh là ``_IncompleteInputError`` không được tài liệu hóa, một lớp con của
      :exc:`SyntaxError`. Mô-đun :mod:`codeop` thiết lập cờ này cùng với :c:macro:`PyCF_DONT_IMPLY_DEDENT` để phân biệt dữ liệu đầu vào chưa hoàn chỉnh với dữ liệu đầu vào có lỗi cú pháp thực sự, nhờ đó các trình thông dịch tương tác biết khi nào cần nhắc nhập thêm một dòng thay vì báo lỗi.

      .. versionadded:: 3.11

   .. c:macro:: PyCF_DONT_IMPLY_DEDENT

      Theo mặc định, khi biên dịch với ký hiệu bắt đầu :c:var:`Py_single_input`, việc chạm đến cuối văn bản nguồn sẽ ngầm đóng mọi khối thụt lề đang mở. Khi đặt cờ này, các khối đang mở chỉ được đóng nếu dòng cuối cùng của nguồn kết thúc bằng ký tự xuống dòng; nếu không, quá trình biên dịch sẽ thất bại với :exc:`SyntaxError`:

      .. code-block:: c

         PyCompilerFlags flags = {
             .cf_flags = 0,
             .cf_feature_version = PY_MINOR_VERSION,
         };
         const char *source = "if a:\n    pass";

         /* Khối "if" được đóng ngầm;
            điều này trả về một đối tượng mã: */
         Py_CompileStringFlags(source, "<input>", Py_single_input, &flags);

         /* Có cờ này, thao tác sẽ thất bại với SyntaxError,
            vì dòng cuối cùng không kết thúc bằng ký tự xuống dòng: */
         flags.cf_flags = PyCF_DONT_IMPLY_DEDENT;
         Py_CompileStringFlags(source, "<input>", Py_single_input, &flags);

      Mô-đun :mod:`codeop` sử dụng cờ này để phát hiện dữ liệu nhập tương tác chưa hoàn chỉnh. Trong khi người dùng vẫn đang nhập bên trong một khối thụt lề, nguồn chưa kết thúc bằng ký tự xuống dòng, nên không biên dịch được và người dùng được nhắc nhập thêm một dòng.

   .. c:macro:: PyCF_IGNORE_COOKIE

      Đọc văn bản nguồn dưới dạng UTF-8, bỏ qua khai báo encoding :pep:`263` ("coding cookie") của nó, nếu có:

      .. code-block:: c

         PyCompilerFlags flags = {
             .cf_flags = 0,
             .cf_feature_version = PY_MINOR_VERSION,
         };
         const char *source = "# coding: latin-1\ns = '\xe9'\n";

         /* Cookie mã hóa được áp dụng: byte 0xE9 được giải mã thành
            Latin-1, và điều này trả về một code object đặt s thành "é": */
         Py_CompileStringFlags(source, "<input>", Py_file_input, &flags);

         /* Với cờ này, cookie bị bỏ qua và quá trình biên dịch thất bại
            với SyntaxError, vì 0xE9 không hợp lệ trong UTF-8: */
         flags.cf_flags = PyCF_IGNORE_COOKIE;
         Py_CompileStringFlags(source, "<input>", Py_file_input, &flags);

      Các hàm dựng sẵn :func:`compile`, :func:`eval` và :func:`exec` đặt cờ này khi mã nguồn là một đối tượng :class:`str`, vì chúng truyền văn bản tới parser được mã hóa dưới dạng UTF-8.

   .. c:macro:: PyCF_SOURCE_IS_UTF8

      Đánh dấu văn bản mã nguồn là đã biết được mã hóa UTF-8. Các hàm dựng sẵn :func:`compile`, :func:`eval` và :func:`exec` đặt cờ này, nhưng hiện tại cờ này không có tác dụng.

   Các cờ "``PyCF``" ở trên có thể kết hợp với các cờ "``CO_FUTURE``" như :c:macro:`CO_FUTURE_ANNOTATIONS` để bật các tính năng thường có thể chọn bằng các câu lệnh :ref:`future statements <future>`. Xem :ref:`c_codeobject_flags` để biết danh sách đầy đủ.

   Các mask sau đây kết hợp nhiều cờ:

   .. c:macro:: PyCF_MASK

      Bitmask của tất cả các cờ ``CO_FUTURE`` (xem :ref:`c_codeobject_flags`), dùng để chọn các tính năng thường được bật bởi
      :ref:`future statements <future>`. Khi mã được biên dịch với đối số ``PyCompilerFlags *flags`` chứa câu lệnh ``from __future__ import``, cờ tương ứng với tính năng được import sẽ được thêm vào *flags*, để mã được thực thi sau đó trong cùng context kế thừa cờ này.

   .. c:macro:: PyCF_MASK_OBSOLETE

      Không sử dụng mask này trong mã mới. Nó chỉ được giữ lại để mã cũ truyền các cờ của nó cho :func:`compile` vẫn tiếp tục hoạt động.

      Bitmask của các cờ dành cho những tính năng future đã lỗi thời và không còn có tác dụng.

   .. c:macro:: PyCF_COMPILE_MASK

      Bitmask của tất cả các cờ ``PyCF`` làm thay đổi cách mã nguồn được biên dịch, chẳng hạn như :c:macro:`PyCF_ONLY_AST`. Hàm built-in :func:`compile` sử dụng mask này để xác thực đối số *flags* của nó.


.. _start-symbols:

Các start symbol khả dụng
^^^^^^^^^^^^^^^^^^^^^^^^^


.. c:var:: int Py_eval_input

   .. index:: single: Py_CompileString (C function)

   Ký hiệu bắt đầu trong grammar Python dành cho các biểu thức độc lập; dùng với
   :c:func:`Py_CompileString`.


.. c:var:: int Py_file_input

   .. index:: single: Py_CompileString (C function)

   Ký hiệu bắt đầu trong grammar Python dành cho các chuỗi câu lệnh được đọc từ một tệp hoặc nguồn khác; dùng với :c:func:`Py_CompileString`. Đây là ký hiệu cần dùng khi biên dịch mã nguồn Python có độ dài tùy ý.


.. c:var:: int Py_single_input

   .. index:: single: Py_CompileString (C function)

   Ký hiệu bắt đầu trong grammar Python dành cho một câu lệnh đơn; dùng với
   :c:func:`Py_CompileString`. Đây là ký hiệu được sử dụng cho vòng lặp trình thông dịch tương tác.


.. c:var:: int Py_func_type_input

   .. index:: single: Py_CompileString (C function)

   Ký hiệu bắt đầu trong grammar Python dành cho một kiểu hàm; dùng với
   :c:func:`Py_CompileString`. Ký hiệu này được dùng để phân tích cú pháp "signature type comments" từ :pep:`484`.

   Điều này yêu cầu phải đặt cờ :c:macro:`PyCF_ONLY_AST` .

   .. seealso::
      * :py:class:`ast.FunctionType`
      * :pep:`484`

   .. versionadded:: 3.8


Hiệu ứng ngăn xếp
^^^^^^^^^^^^^^^^^

.. seealso::
   :py:func:`dis.stack_effect`


.. c:macro:: PY_INVALID_STACK_EFFECT

   Giá trị sentinel biểu thị một hiệu ứng ngăn xếp không hợp lệ.

   Hiện tại, giá trị này tương đương với ``INT_MAX``.

   .. versionadded:: 3.8


.. c:function:: int PyCompile_OpcodeStackEffect(int opcode, int oparg)

   Tính hiệu ứng ngăn xếp của *opcode* với đối số *oparg*.

   Nếu thành công, hàm này trả về hiệu ứng ngăn xếp; nếu thất bại, hàm trả về :c:macro:`PY_INVALID_STACK_EFFECT`.

   .. versionadded:: 3.4


.. c:function:: int PyCompile_OpcodeStackEffectWithJump(int opcode, int oparg, int jump)

   Tương tự như :c:func:`PyCompile_OpcodeStackEffect`, nhưng không bao gồm hiệu ứng ngăn xếp của việc nhảy nếu *jump* bằng không.

   Nếu *jump* là ``0``, hàm này sẽ không bao gồm hiệu ứng ngăn xếp của việc nhảy, nhưng nếu *jump* là ``1`` hoặc ``-1``, hàm sẽ bao gồm hiệu ứng đó.

   Nếu thành công, hàm này trả về hiệu ứng ngăn xếp; nếu thất bại, hàm trả về :c:macro:`PY_INVALID_STACK_EFFECT`.

   .. versionadded:: 3.8
