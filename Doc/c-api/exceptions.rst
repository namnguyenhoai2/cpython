.. highlight:: c


.. _exceptionhandling:

**************
Xử lý ngoại lệ
**************

Các hàm được mô tả trong chương này cho phép bạn xử lý và phát sinh các ngoại lệ Python. Điều quan trọng là phải hiểu một số kiến thức cơ bản về việc xử lý ngoại lệ trong Python. Cơ chế này phần nào giống biến POSIX :c:data:`errno`: có một chỉ báo toàn cục (theo từng thread) về lỗi gần nhất đã xảy ra. Hầu hết các hàm C API không xóa chỉ báo này khi thành công, nhưng sẽ đặt nó để cho biết nguyên nhân lỗi khi thất bại. Hầu hết các hàm C API cũng trả về một chỉ báo lỗi, thường là ``NULL`` nếu chúng được thiết kế để trả về một con trỏ, hoặc ``-1`` nếu chúng trả về một số nguyên (ngoại lệ: các hàm ``PyArg_*`` trả về ``1`` khi thành công và ``0`` khi thất bại).

Cụ thể, chỉ báo lỗi bao gồm ba con trỏ đối tượng: kiểu của ngoại lệ, giá trị của ngoại lệ và đối tượng traceback. Bất kỳ con trỏ nào trong số đó cũng có thể là ``NULL`` nếu chưa được thiết lập (mặc dù một số tổ hợp bị cấm; ví dụ: bạn không thể có traceback khác ``NULL`` nếu kiểu ngoại lệ là ``NULL``).

Khi một hàm phải thất bại vì một hàm mà nó gọi đã thất bại, nhìn chung nó không đặt chỉ báo lỗi; hàm được gọi đã đặt chỉ báo này. Hàm đó có trách nhiệm xử lý lỗi và xóa ngoại lệ, hoặc trả về sau khi dọn dẹp mọi tài nguyên mà nó đang nắm giữ (chẳng hạn như các tham chiếu đối tượng hoặc vùng nhớ được cấp phát); hàm *không* nên tiếp tục hoạt động bình thường nếu chưa sẵn sàng xử lý lỗi. Nếu trả về do lỗi, điều quan trọng là phải cho bên gọi biết rằng một lỗi đã được thiết lập. Nếu lỗi không được xử lý hoặc truyền tiếp một cách cẩn thận, các lần gọi bổ sung vào Python/C API có thể không hoạt động như dự kiến và có thể thất bại theo những cách khó hiểu.

.. note::
   Chỉ báo lỗi **không** phải là kết quả của :func:`sys.exc_info`. Chỉ báo đầu tiên tương ứng với một ngoại lệ chưa được bắt (và do đó vẫn đang được truyền đi), trong khi chỉ báo sau trả về một ngoại lệ sau khi ngoại lệ đó được bắt (và do đó đã ngừng được truyền đi).


In và xóa
=========


.. c:function:: void PyErr_Clear()

   Xóa chỉ báo lỗi. Nếu chỉ báo lỗi chưa được thiết lập thì không có tác động nào.


.. c:function:: void PyErr_PrintEx(int set_sys_last_vars)

   In traceback tiêu chuẩn đến ``sys.stderr`` và xóa chỉ báo lỗi. **Trừ khi** lỗi là một ``SystemExit``, trong trường hợp đó không có traceback nào được in và tiến trình Python sẽ thoát với mã lỗi được chỉ định bởi thực thể ``SystemExit``.

   Chỉ gọi hàm này **khi** chỉ báo lỗi được thiết lập. Nếu không, hàm sẽ gây ra lỗi nghiêm trọng!

   Nếu *set_sys_last_vars* khác 0, biến :data:`sys.last_exc` sẽ được đặt thành ngoại lệ đã in. Để tương thích ngược, các biến đã lỗi thời :data:`sys.last_type`, :data:`sys.last_value` và
   :data:`sys.last_traceback` cũng được đặt lần lượt thành kiểu, giá trị và traceback của ngoại lệ này.

   .. versionchanged:: 3.12
      Thiết lập :data:`sys.last_exc` đã được thêm.


.. c:function:: void PyErr_Print()

   Bí danh của ``PyErr_PrintEx(1)``.


.. c:function:: void PyErr_WriteUnraisable(PyObject *obj)

   Gọi :func:`sys.unraisablehook` bằng ngoại lệ hiện tại và đối số *obj*.

   Hàm tiện ích này in một thông báo cảnh báo vào ``sys.stderr`` khi một ngoại lệ đã được thiết lập nhưng trình thông dịch không thể thực sự phát sinh ngoại lệ đó. Ví dụ, hàm được sử dụng khi một ngoại lệ xảy ra trong một
   :meth:`~object.__del__` phương thức.

   Hàm được gọi với một đối số duy nhất là *obj*, đối số này xác định ngữ cảnh xảy ra ngoại lệ không thể phát sinh. Nếu có thể, repr của *obj* sẽ được in trong thông báo cảnh báo. Nếu *obj* là ``NULL``, chỉ traceback được in.

   Phải thiết lập một ngoại lệ khi gọi hàm này.

   .. versionchanged:: 3.4
      In traceback. Chỉ in traceback nếu *obj* là ``NULL``.

   .. versionchanged:: 3.8
      Sử dụng :func:`sys.unraisablehook`.


.. c:function:: void PyErr_FormatUnraisable(const char *format, ...)

   Tương tự :c:func:`PyErr_WriteUnraisable`, nhưng *format* và các tham số tiếp theo giúp định dạng thông báo cảnh báo; chúng có cùng ý nghĩa và giá trị như trong :c:func:`PyUnicode_FromFormat`. ``PyErr_WriteUnraisable(obj)`` tương đương gần đúng với ``PyErr_FormatUnraisable("Exception ignored in: %R", obj)``. Nếu *format* là ``NULL``, chỉ traceback được in.

   .. versionadded:: 3.13


.. c:function:: void PyErr_DisplayException(PyObject *exc)

   In bản hiển thị traceback tiêu chuẩn của ``exc`` vào ``sys.stderr``, bao gồm các ngoại lệ được nối chuỗi và ghi chú.

   .. versionadded:: 3.12


.. c:function:: void PyErr_Display(PyObject *unused, PyObject *value, PyObject *tb)

   Biến thể cũ của :c:func:`PyErr_DisplayException`.

   In ngoại lệ *value* cùng traceback của nó vào :data:`sys.stderr`. Nếu *value* chưa được thiết lập traceback, *tb* sẽ được dùng làm traceback của nó. Đối số đầu tiên bị bỏ qua.

   Nếu :data:`sys.stderr` là ``None``, không có gì được in. Nếu :data:`sys.stderr` chưa được thiết lập, ngoại lệ sẽ được đổ vào stream C ``stderr`` thay thế.

   .. deprecated:: 3.12
      Thay vào đó, hãy sử dụng :c:func:`PyErr_DisplayException`.

Phát sinh ngoại lệ
==================

Các hàm này giúp bạn thiết lập chỉ báo lỗi của thread hiện tại. Để thuận tiện, một số hàm trong đó sẽ luôn trả về con trỏ ``NULL`` để sử dụng trong câu lệnh ``return``.


.. c:function:: void PyErr_SetString(PyObject *type, const char *message)

   Đây là cách phổ biến nhất để thiết lập chỉ báo lỗi. Đối số đầu tiên chỉ định kiểu ngoại lệ; thông thường đó là một trong các ngoại lệ chuẩn, chẳng hạn như :c:data:`PyExc_RuntimeError`. Bạn không cần tạo mới
   :term:`strong reference` cho nó (ví dụ: bằng :c:func:`Py_INCREF`). Đối số thứ hai là thông báo lỗi; thông báo này được giải mã từ ``'utf-8'``.


.. c:function:: void PyErr_SetObject(PyObject *type, PyObject *value)

   Hàm này tương tự như :c:func:`PyErr_SetString` nhưng cho phép bạn chỉ định một đối tượng Python tùy ý làm "giá trị" của ngoại lệ.


.. c:function:: PyObject* PyErr_Format(PyObject *exception, const char *format, ...)

   Hàm này thiết lập chỉ báo lỗi và trả về ``NULL``. *exception* phải là một lớp ngoại lệ Python. *format* và các tham số tiếp theo giúp định dạng thông báo lỗi; chúng có cùng ý nghĩa và giá trị như trong :c:func:`PyUnicode_FromFormat`. *format* là một chuỗi được mã hóa ASCII.


.. c:function:: PyObject* PyErr_FormatV(PyObject *exception, const char *format, va_list vargs)

   Giống như :c:func:`PyErr_Format`, nhưng nhận một đối số :c:type:`va_list` thay vì một số lượng đối số thay đổi.

   .. versionadded:: 3.5


.. c:function:: void PyErr_SetNone(PyObject *type)

   Đây là cách viết tắt của ``PyErr_SetObject(type, Py_None)``.


.. c:function:: int PyErr_BadArgument()

   Đây là cách viết tắt của ``PyErr_SetString(PyExc_TypeError, message)``, trong đó *message* cho biết một thao tác tích hợp sẵn đã được gọi với một đối số không hợp lệ. Chủ yếu dùng cho mục đích nội bộ.


.. c:function:: PyObject* PyErr_NoMemory()

   Đây là cách viết tắt của ``PyErr_SetNone(PyExc_MemoryError)``; hàm này trả về ``NULL`` để một hàm cấp phát đối tượng có thể ghi ``return PyErr_NoMemory();`` khi hết bộ nhớ.


.. c:function:: PyObject* PyErr_SetFromErrno(PyObject *type)

   .. index:: single: strerror (C function)

   Đây là một hàm tiện ích để phát sinh ngoại lệ khi một hàm thư viện C trả về lỗi và đặt biến C :c:data:`errno`. Hàm này xây dựng một đối tượng tuple, trong đó phần tử đầu tiên là giá trị số nguyên :c:data:`errno`, còn phần tử thứ hai là thông báo lỗi tương ứng (lấy từ :c:func:`!strerror`), rồi gọi ``PyErr_SetObject(type, object)``. Trên Unix, khi
   giá trị :c:data:`errno` là :c:macro:`!EINTR`, cho biết một lời gọi hệ thống bị gián đoạn, hàm này gọi :c:func:`PyErr_CheckSignals`, và nếu hàm đó đặt chỉ báo lỗi thì giữ nguyên chỉ báo đó. Hàm luôn trả về ``NULL``, vì vậy một hàm bao quanh lời gọi hệ thống có thể ghi ``return PyErr_SetFromErrno(type);`` khi lời gọi hệ thống trả về lỗi.


.. c:function:: PyObject* PyErr_SetFromErrnoWithFilenameObject(PyObject *type, PyObject *filenameObject)

   Tương tự :c:func:`PyErr_SetFromErrno`, nhưng có thêm hành vi là nếu *filenameObject* không phải là ``NULL``, đối tượng này được truyền cho hàm khởi tạo của *type* dưới dạng tham số thứ ba. Trong trường hợp ngoại lệ :exc:`OSError`, đối tượng này được dùng để xác định thuộc tính :attr:`!filename` của thể hiện ngoại lệ.


.. c:function:: PyObject* PyErr_SetFromErrnoWithFilenameObjects(PyObject *type, PyObject *filenameObject, PyObject *filenameObject2)

   Tương tự :c:func:`PyErr_SetFromErrnoWithFilenameObject`, nhưng nhận thêm một đối tượng filename thứ hai để phát sinh lỗi khi một hàm nhận hai filename bị lỗi.

   .. versionadded:: 3.4


.. c:function:: PyObject* PyErr_SetFromErrnoWithFilename(PyObject *type, const char *filename)

   Tương tự :c:func:`PyErr_SetFromErrnoWithFilenameObject`, nhưng filename được cung cấp dưới dạng chuỗi C. *filename* được giải mã từ :term:`filesystem encoding and error handler`.


.. c:function:: PyObject* PyErr_SetFromWindowsErr(int ierr)

   Đây là một hàm tiện ích để phát sinh :exc:`OSError`. Nếu được gọi với *ierr* bằng ``0``, mã lỗi được trả về bởi một lần gọi :c:func:`!GetLastError` sẽ được sử dụng thay thế. Hàm này gọi hàm Win32 :c:func:`!FormatMessage` để lấy mô tả lỗi Windows của mã lỗi được cung cấp bởi *ierr* hoặc :c:func:`!GetLastError`, sau đó xây dựng một đối tượng :exc:`OSError` với thuộc tính :attr:`~OSError.winerror` được đặt thành mã lỗi và thuộc tính :attr:`~OSError.strerror` được đặt thành thông báo lỗi tương ứng (lấy từ
   :c:func:`!FormatMessage`), sau đó gọi ``PyErr_SetObject(PyExc_OSError, object)``. Hàm này luôn trả về ``NULL``.

   .. availability:: Windows.


.. c:function:: PyObject* PyErr_SetExcFromWindowsErr(PyObject *type, int ierr)

   Tương tự :c:func:`PyErr_SetFromWindowsErr`, với một tham số bổ sung chỉ định kiểu exception sẽ được raise.

   .. availability:: Windows.


.. c:function:: PyObject* PyErr_SetFromWindowsErrWithFilename(int ierr, const char *filename)

   Tương tự :c:func:`PyErr_SetFromWindowsErr`, với hành vi bổ sung là nếu *filename* không phải là ``NULL``, nó sẽ được giải mã bằng encoding của filesystem (:func:`os.fsdecode`) và được truyền cho constructor của
   :exc:`OSError` làm tham số thứ ba để dùng cho việc xác định
   thuộc tính :attr:`!filename` của instance exception.

   .. availability:: Windows.


.. c:function:: PyObject* PyErr_SetExcFromWindowsErrWithFilenameObject(PyObject *type, int ierr, PyObject *filename)

   Tương tự :c:func:`PyErr_SetExcFromWindowsErr`, với hành vi bổ sung là nếu *filename* không phải là ``NULL``, nó sẽ được truyền cho constructor của
   :exc:`OSError` làm tham số thứ ba để dùng cho việc xác định
   thuộc tính :attr:`!filename` của instance exception.

   .. availability:: Windows.


.. c:function:: PyObject* PyErr_SetExcFromWindowsErrWithFilenameObjects(PyObject *type, int ierr, PyObject *filename, PyObject *filename2)

   Tương tự :c:func:`PyErr_SetExcFromWindowsErrWithFilenameObject`, nhưng chấp nhận thêm một đối tượng tên tệp thứ hai.

   .. availability:: Windows.

   .. versionadded:: 3.4


.. c:function:: PyObject* PyErr_SetExcFromWindowsErrWithFilename(PyObject *type, int ierr, const char *filename)

   Tương tự :c:func:`PyErr_SetFromWindowsErrWithFilename`, với một tham số bổ sung chỉ định kiểu ngoại lệ cần được đưa ra.

   .. availability:: Windows.


.. c:function:: PyObject* PyErr_SetImportError(PyObject *msg, PyObject *name, PyObject *path)

   Đây là một hàm tiện ích để đưa ra :exc:`ImportError`. *msg* sẽ được đặt làm chuỗi thông báo của ngoại lệ. *name* và *path*, cả hai đều có thể là ``NULL``, sẽ được đặt làm các thuộc tính ``name`` và ``path`` tương ứng của :exc:`ImportError`.

   .. versionadded:: 3.3


.. c:function:: PyObject* PyErr_SetImportErrorSubclass(PyObject *exception, PyObject *msg, PyObject *name, PyObject *path)

   Tương tự :c:func:`PyErr_SetImportError`, nhưng hàm này cho phép chỉ định một lớp con của :exc:`ImportError` để đưa ra.

   .. versionadded:: 3.6


.. c:function:: void PyErr_SyntaxLocationObject(PyObject *filename, int lineno, int col_offset)

   Đặt thông tin về tệp, dòng và vị trí offset cho ngoại lệ hiện tại. Nếu ngoại lệ hiện tại không phải là :exc:`SyntaxError`, hàm sẽ đặt các thuộc tính bổ sung, khiến hệ thống in ngoại lệ cho rằng ngoại lệ đó là :exc:`SyntaxError`.

   .. versionadded:: 3.4


.. c:function:: void PyErr_RangedSyntaxLocationObject(PyObject *filename, int lineno, int col_offset, int end_lineno, int end_col_offset)

   Tương tự :c:func:`PyErr_SyntaxLocationObject`, nhưng cũng đặt thông tin *end_lineno* và *end_col_offset* cho ngoại lệ hiện tại.

   .. versionadded:: 3.10


.. c:function:: void PyErr_SyntaxLocationEx(const char *filename, int lineno, int col_offset)

   Giống :c:func:`PyErr_SyntaxLocationObject`, nhưng *filename* là một chuỗi byte được giải mã từ :term:`filesystem encoding and error handler`.

   .. versionadded:: 3.2


.. c:function:: void PyErr_SyntaxLocation(const char *filename, int lineno)

   Giống :c:func:`PyErr_SyntaxLocationEx`, nhưng tham số *col_offset* bị bỏ qua.


.. c:function:: void PyErr_BadInternalCall()

   Đây là cách viết tắt của ``PyErr_SetString(PyExc_SystemError, message)``, trong đó *message* cho biết một thao tác nội bộ (ví dụ: một hàm Python/C API) đã được gọi với một đối số không hợp lệ. Nó chủ yếu dùng cho mục đích nội bộ.


.. c:function:: PyObject *PyErr_ProgramTextObject(PyObject *filename, int lineno)

   Lấy dòng mã nguồn trong *filename* tại dòng *lineno*. *filename* phải là một đối tượng :class:`str` của Python.

   Khi thành công, hàm này trả về một đối tượng chuỗi Python chứa dòng được tìm thấy. Khi thất bại, hàm này trả về ``NULL`` mà không thiết lập ngoại lệ.


.. c:function:: PyObject *PyErr_ProgramText(const char *filename, int lineno)

   Tương tự :c:func:`PyErr_ProgramTextObject`, nhưng *filename* là một
   :c:expr:`const char *`, được giải mã bằng
   :term:`filesystem encoding and error handler`, thay vì một tham chiếu đến đối tượng Python.


Phát hành cảnh báo
==================

Sử dụng các hàm này để phát hành cảnh báo từ mã C. Chúng tương tự như các hàm tương ứng được Python :mod:`warnings` module xuất ra. Thông thường, chúng in thông báo cảnh báo vào *sys.stderr*; tuy nhiên, cũng có thể người dùng đã chỉ định rằng cảnh báo phải được chuyển thành lỗi, và trong trường hợp đó, chúng sẽ raise một exception. Cũng có thể các hàm raise một exception do có vấn đề với hệ thống cảnh báo. Giá trị trả về là ``0`` nếu không có exception nào được raise, hoặc ``-1`` nếu có exception được raise. (Không thể xác định liệu một thông báo cảnh báo có thực sự được in hay không, cũng như lý do của exception; đây là chủ ý.) Nếu có exception được raise, caller nên thực hiện việc xử lý exception thông thường (ví dụ: :c:func:`Py_DECREF` các reference do mình sở hữu và trả về một giá trị lỗi).

.. c:function:: int PyErr_WarnEx(PyObject *category, const char *message, Py_ssize_t stack_level)

   Phát hành một thông báo cảnh báo. Đối số *category* là một loại cảnh báo (xem bên dưới) hoặc ``NULL``; đối số *message* là một chuỗi được mã hóa UTF-8. *stack_level* là một số dương cho biết số lượng stack frame; cảnh báo sẽ được phát hành từ dòng mã hiện đang được thực thi trong stack frame đó. Giá trị *stack_level* là 1 tương ứng với hàm gọi :c:func:`PyErr_WarnEx`, 2 tương ứng với hàm bên trên hàm đó, v.v.

   Các loại cảnh báo phải là lớp con của :c:data:`PyExc_Warning`;
   :c:data:`PyExc_Warning` là một lớp con của :c:data:`PyExc_Exception`; loại cảnh báo mặc định là :c:data:`PyExc_RuntimeWarning`. Các loại cảnh báo Python tiêu chuẩn có sẵn dưới dạng các biến toàn cục với tên được liệt kê tại :ref:`standardwarningcategories`.

   Để biết thông tin về việc kiểm soát cảnh báo, hãy xem tài liệu về
   Mô-đun :mod:`warnings` và tùy chọn :option:`-W` trong tài liệu dòng lệnh. Không có C API để kiểm soát cảnh báo.


.. c:function:: int PyErr_WarnExplicitObject(PyObject *category, PyObject *message, PyObject *filename, int lineno, PyObject *module, PyObject *registry)

   Phát hành một thông báo cảnh báo với quyền kiểm soát rõ ràng đối với tất cả các thuộc tính cảnh báo. Đây là một wrapper đơn giản quanh hàm Python
   :func:`warnings.warn_explicit`; xem phần đó để biết thêm thông tin. Các đối số *module* và *registry* có thể được đặt thành ``NULL`` để có hiệu ứng mặc định được mô tả ở đó.

   .. versionadded:: 3.4


.. c:function:: int PyErr_WarnExplicit(PyObject *category, const char *message, const char *filename, int lineno, const char *module, PyObject *registry)

   Tương tự như :c:func:`PyErr_WarnExplicitObject`, ngoại trừ việc *message* và *module* là các chuỗi được mã hóa UTF-8, còn *filename* được giải mã từ
   :term:`filesystem encoding and error handler`.


.. c:function:: int PyErr_WarnFormat(PyObject *category, Py_ssize_t stack_level, const char *format, ...)

   Hàm tương tự như :c:func:`PyErr_WarnEx`, nhưng sử dụng
   :c:func:`PyUnicode_FromFormat` để định dạng thông báo cảnh báo. *format* là một chuỗi được mã hóa ASCII.

   .. versionadded:: 3.2


.. c:function:: int PyErr_WarnExplicitFormat(PyObject *category, const char *filename, int lineno, const char *module, PyObject *registry, const char *format, ...)

   Tương tự như :c:func:`PyErr_WarnExplicit`, nhưng sử dụng
   :c:func:`PyUnicode_FromFormat` để định dạng thông báo cảnh báo. *format* là một chuỗi được mã hóa ASCII.

   .. versionadded:: 3.2


.. c:function:: int PyErr_ResourceWarning(PyObject *source, Py_ssize_t stack_level, const char *format, ...)

   Hàm này tương tự :c:func:`PyErr_WarnFormat`, nhưng *category* là
   :exc:`ResourceWarning` và truyền *source* vào :class:`!warnings.WarningMessage`.

   .. versionadded:: 3.6


Truy vấn chỉ báo lỗi
====================

.. c:function:: PyObject* PyErr_Occurred()

   Kiểm tra xem chỉ báo lỗi đã được thiết lập hay chưa. Nếu đã thiết lập, trả về *type* của exception (đối số đầu tiên trong lần gọi gần nhất đến một trong các hàm ``PyErr_Set*`` hoặc đến :c:func:`PyErr_Restore`). Nếu chưa được thiết lập, trả về ``NULL``. Bạn không sở hữu một tham chiếu đến giá trị trả về, vì vậy không cần :c:func:`Py_DECREF` giá trị đó.

   Bên gọi phải có một :term:`attached thread state`.

   .. note::

      Không so sánh giá trị trả về với một exception cụ thể; hãy dùng
      :c:func:`PyErr_ExceptionMatches` thay vào đó, như dưới đây.  (Phép so sánh có thể dễ dàng thất bại vì ngoại lệ có thể là một instance thay vì một class, trong trường hợp ngoại lệ là một class, hoặc có thể là một subclass của ngoại lệ được mong đợi.)


.. c:function:: int PyErr_ExceptionMatches(PyObject *exc)

   Tương đương với ``PyErr_GivenExceptionMatches(PyErr_Occurred(), exc)``.  Chỉ nên gọi hàm này khi một ngoại lệ thực sự đã được thiết lập; sẽ xảy ra lỗi truy cập bộ nhớ nếu chưa có ngoại lệ nào được phát sinh.


.. c:function:: int PyErr_GivenExceptionMatches(PyObject *given, PyObject *exc)

   Trả về true nếu ngoại lệ *given* khớp với kiểu ngoại lệ trong *exc*.  Nếu *exc* là một class object, hàm này cũng trả về true khi *given* là một instance của subclass.  Nếu *exc* là một tuple, tất cả các kiểu ngoại lệ trong tuple đó (và đệ quy trong các subtuple) sẽ được tìm kiếm để tìm kết quả khớp.


.. c:function:: PyObject *PyErr_GetRaisedException(void)

   Trả về ngoại lệ hiện đang được phát sinh, đồng thời xóa error indicator. Trả về ``NULL`` nếu error indicator chưa được thiết lập.

   Hàm này được sử dụng bởi code cần bắt ngoại lệ hoặc code cần tạm thời lưu và khôi phục error indicator.

   Ví dụ::

      {
         PyObject *exc = PyErr_GetRaisedException();

         /* ... code that might produce other errors ... */

         PyErr_SetRaisedException(exc);
      }

   .. seealso:: :c:func:`PyErr_GetHandledException`, để lưu ngoại lệ hiện đang được xử lý.

   .. versionadded:: 3.12


.. c:function:: void PyErr_SetRaisedException(PyObject *exc)

   Đặt *exc* làm ngoại lệ hiện đang được phát sinh, đồng thời xóa ngoại lệ hiện có nếu đã được thiết lập. Nếu *exc* là ``NULL``, chỉ cần xóa ngoại lệ hiện có.

   *exc* phải là một ngoại lệ hợp lệ hoặc ``NULL``.

   Lệnh gọi này ":term:`steals <steal>`" một tham chiếu đến *exc*.

   .. versionadded:: 3.12


.. c:function:: void PyErr_Fetch(PyObject **ptype, PyObject **pvalue, PyObject **ptraceback)

   .. deprecated:: 3.12

      Thay vào đó, hãy sử dụng :c:func:`PyErr_GetRaisedException`.

   Lấy error indicator vào ba biến có địa chỉ được truyền vào. Nếu error indicator chưa được thiết lập, đặt cả ba biến thành ``NULL``. Nếu đã được thiết lập, error indicator sẽ bị xóa và bạn sở hữu một tham chiếu đến mỗi đối tượng được lấy. Đối tượng value và traceback có thể là ``NULL`` ngay cả khi đối tượng type không phải là ``NULL``.

   .. note::

      Hàm này thường chỉ được mã legacy sử dụng khi cần bắt các ngoại lệ hoặc tạm thời lưu và khôi phục error indicator.

      Ví dụ::

         {
            PyObject *type, *value, *traceback;
            PyErr_Fetch(&type, &value, &traceback);

            /* ... code that might produce other errors ... */

            PyErr_Restore(type, value, traceback);
         }


.. c:function:: void PyErr_Restore(PyObject *type, PyObject *value, PyObject *traceback)

   .. deprecated:: 3.12

      Thay vào đó, hãy sử dụng :c:func:`PyErr_SetRaisedException`.

   Đặt chỉ báo lỗi từ ba đối tượng, *type*, *value* và *traceback*, đồng thời xóa ngoại lệ hiện có nếu đã được đặt. Nếu các đối tượng là ``NULL``, chỉ báo lỗi sẽ được xóa. Không truyền ``NULL`` type và value hoặc traceback không phải ``NULL``. Kiểu ngoại lệ phải là một class. Không truyền kiểu hoặc giá trị ngoại lệ không hợp lệ. (Vi phạm các quy tắc này sẽ gây ra những vấn đề khó nhận thấy về sau.) Lệnh gọi này lấy đi một tham chiếu đến mỗi đối tượng: bạn phải sở hữu một tham chiếu đến mỗi đối tượng trước khi gọi, và sau khi gọi bạn không còn sở hữu các tham chiếu đó nữa. (Nếu bạn không hiểu điều này, đừng sử dụng hàm này. Tôi đã cảnh báo bạn.)

   .. note::

      Hàm này thường chỉ được sử dụng bởi mã legacy cần lưu và khôi phục tạm thời chỉ báo lỗi. Hãy sử dụng :c:func:`PyErr_Fetch` để lưu chỉ báo lỗi hiện tại.


.. c:function:: void PyErr_NormalizeException(PyObject **exc, PyObject **val, PyObject **tb)

   .. deprecated:: 3.12

      Thay vào đó, hãy sử dụng :c:func:`PyErr_GetRaisedException` để tránh mọi khả năng de-normalization.

   Trong một số trường hợp, các giá trị được :c:func:`PyErr_Fetch` trả về bên dưới có thể là “chưa được chuẩn hóa”, nghĩa là ``*exc`` là một đối tượng class nhưng ``*val`` không phải là một instance của cùng class đó. Có thể sử dụng hàm này để khởi tạo class trong trường hợp đó. Nếu các giá trị đã được chuẩn hóa thì không có gì xảy ra. Cơ chế chuẩn hóa trì hoãn được triển khai để cải thiện hiệu năng.

   .. note::

      Hàm này *không* ngầm đặt
      thuộc tính :attr:`~BaseException.__traceback__` trên giá trị ngoại lệ. Nếu muốn đặt traceback một cách phù hợp, cần có thêm đoạn mã sau::

         if (tb != NULL) {
           PyException_SetTraceback(val, tb);
         }


.. c:function:: PyObject* PyErr_GetHandledException(void)

   Lấy instance của ngoại lệ đang hoạt động, như được trả về bởi :func:`sys.exception`. Đây là ngoại lệ đã được *bắt*, không phải ngoại lệ vừa được phát sinh. Trả về một tham chiếu mới đến ngoại lệ hoặc ``NULL``. Không sửa đổi trạng thái ngoại lệ của trình thông dịch.

   .. note::

      Hàm này thường không được mã muốn xử lý ngoại lệ sử dụng. Thay vào đó, hàm có thể được dùng khi mã cần tạm thời lưu và khôi phục trạng thái ngoại lệ. Sử dụng :c:func:`PyErr_SetHandledException` để khôi phục hoặc xóa trạng thái ngoại lệ.

   .. versionadded:: 3.11

.. c:function:: void PyErr_SetHandledException(PyObject *exc)

   Đặt ngoại lệ đang hoạt động, như được biết từ ``sys.exception()``. Đây là ngoại lệ đã được *bắt*, không phải ngoại lệ vừa được phát sinh. Để xóa trạng thái ngoại lệ, truyền ``NULL``.

   .. note::

      Hàm này thường không được mã muốn xử lý ngoại lệ sử dụng. Thay vào đó, hàm có thể được dùng khi mã cần tạm thời lưu và khôi phục trạng thái ngoại lệ. Sử dụng :c:func:`PyErr_GetHandledException` để lấy trạng thái ngoại lệ.

   .. versionadded:: 3.11

.. c:function:: void PyErr_GetExcInfo(PyObject **ptype, PyObject **pvalue, PyObject **ptraceback)

   Lấy biểu diễn kiểu cũ của thông tin ngoại lệ, như được biết từ
   :func:`sys.exc_info`. Đây là ngoại lệ đã được *bắt*, không phải ngoại lệ vừa được phát sinh. Trả về các tham chiếu mới đến ba đối tượng, bất kỳ đối tượng nào trong số đó cũng có thể là ``NULL``. Không sửa đổi trạng thái thông tin ngoại lệ. Hàm này được duy trì để tương thích ngược. Ưu tiên sử dụng
   :c:func:`PyErr_GetHandledException`.

   .. note::

      Hàm này thường không được mã muốn xử lý ngoại lệ sử dụng. Thay vào đó, hàm có thể được dùng khi mã cần tạm thời lưu và khôi phục trạng thái ngoại lệ. Sử dụng :c:func:`PyErr_SetExcInfo` để khôi phục hoặc xóa trạng thái ngoại lệ.

   .. versionadded:: 3.3


.. c:function:: void PyErr_SetExcInfo(PyObject *type, PyObject *value, PyObject *traceback)

   Thiết lập thông tin ngoại lệ như được biết từ ``sys.exc_info()``. Điều này đề cập đến một ngoại lệ đã *được bắt*, chứ không phải một ngoại lệ vừa được phát sinh. Hàm này ":term:`lấy quyền sở hữu <steal>`" các tham chiếu đến những đối số. Để xóa trạng thái ngoại lệ, truyền ``NULL`` cho cả ba đối số. Hàm này được duy trì để tương thích ngược. Nên sử dụng
   :c:func:`PyErr_SetHandledException`.

   .. note::

      Mã muốn xử lý ngoại lệ thường không sử dụng hàm này. Thay vào đó, hàm có thể được dùng khi mã cần tạm thời lưu và khôi phục trạng thái ngoại lệ. Sử dụng :c:func:`PyErr_GetExcInfo` để đọc trạng thái ngoại lệ.

   .. versionadded:: 3.3

   .. versionchanged:: 3.11
      Các đối số ``type`` và ``traceback`` không còn được sử dụng và có thể là NULL. Hiện tại, trình thông dịch suy ra chúng từ đối tượng ngoại lệ (đối số ``value``). Hàm vẫn ":term:`lấy quyền sở hữu <steal>`" các tham chiếu đến cả ba đối số.


Xử lý tín hiệu
==============


.. c:function:: int PyErr_CheckSignals()

   .. index::
      pair: module; signal
      single: SIGINT (C macro)
      single: KeyboardInterrupt (built-in exception)

   Xử lý các ngắt từ bên ngoài, chẳng hạn như tín hiệu hoặc việc kích hoạt trình gỡ lỗi, vốn đã bị trì hoãn cho đến khi an toàn để chạy mã Python và/hoặc phát sinh ngoại lệ.

   Ví dụ, nhấn :kbd:`Ctrl-C` khiến terminal gửi
   tín hiệu :py:data:`signal.SIGINT`. Hàm này thực thi signal handler Python tương ứng, theo mặc định sẽ phát sinh ngoại lệ :exc:`KeyboardInterrupt`.

   :c:func:`!PyErr_CheckSignals` nên được gọi bởi mã C chạy trong thời gian dài đủ thường xuyên để phản hồi xuất hiện ngay lập tức đối với người dùng.

   Các trình xử lý được hàm này gọi hiện bao gồm:

   - Các trình xử lý tín hiệu, bao gồm các hàm Python được đăng ký thông qua mô-đun :mod:`signal`.

     Trình xử lý tín hiệu chỉ được chạy trong thread chính của interpreter chính.

     (Đây là nguồn gốc tên của hàm: ban đầu, tín hiệu là cách duy nhất để ngắt interpreter.)

   - Chạy bộ thu gom rác, nếu cần.

   - Thực thi một tập lệnh :ref:`trình gỡ lỗi từ xa <remote-debugging>` đang chờ xử lý.

   Nếu bất kỳ handler nào phát sinh ngoại lệ, ngay lập tức trả về ``-1`` cùng với ngoại lệ đó. Mọi gián đoạn còn lại sẽ được để xử lý ở lần tiếp theo
   gọi :c:func:`PyErr_CheckSignals()`, nếu thích hợp.

   Nếu tất cả handler hoàn tất thành công hoặc không có handler nào cần chạy, hãy trả về ``0``.

   .. versionchanged:: 3.12
      Hàm này lúc này có thể gọi trình thu gom rác.

   .. versionchanged:: 3.14
      Hàm này lúc này có thể thực thi một tập lệnh trình gỡ lỗi từ xa, nếu tính năng gỡ lỗi từ xa được bật.


.. c:function:: void PyErr_SetInterrupt()

   .. index::
      pair: module; signal
      single: SIGINT (C macro)
      single: KeyboardInterrupt (built-in exception)

   Mô phỏng tác động của việc một tín hiệu :c:macro:`!SIGINT` đến. Điều này tương đương với ``PyErr_SetInterruptEx(SIGINT)``.

   .. note::
      Hàm này an toàn đối với tín hiệu bất đồng bộ (async-signal-safe). Hàm có thể được gọi mà không cần :term:`attached thread state` và từ một signal handler C.


.. c:function:: int PyErr_SetInterruptEx(int signum)

   .. index::
      pair: module; signal
      single: KeyboardInterrupt (built-in exception)

   Mô phỏng hiệu ứng của một tín hiệu đến. Lần tiếp theo
   :c:func:`PyErr_CheckSignals` được gọi, trình xử lý tín hiệu Python cho số hiệu tín hiệu đã cho sẽ được gọi.

   Hàm này có thể được gọi bởi mã C thiết lập cơ chế xử lý tín hiệu riêng và muốn các trình xử lý tín hiệu Python được gọi như mong đợi khi có yêu cầu ngắt (ví dụ: khi người dùng nhấn Ctrl-C để ngắt một thao tác).

   Nếu tín hiệu đã cho không được Python xử lý (nó được đặt thành
   :py:const:`signal.SIG_DFL` hoặc :py:const:`signal.SIG_IGN`), tín hiệu đó sẽ bị bỏ qua.

   Nếu *signum* nằm ngoài phạm vi số hiệu tín hiệu được phép, ``-1`` sẽ được trả về. Nếu không, ``0`` sẽ được trả về. Chỉ báo lỗi không bao giờ bị thay đổi bởi hàm này.

   .. note::
      Hàm này an toàn đối với tín hiệu bất đồng bộ (async-signal-safe). Hàm có thể được gọi mà không cần :term:`attached thread state` và từ một signal handler C.

   .. versionadded:: 3.10


.. c:function:: int PySignal_SetWakeupFd(int fd)

   Hàm tiện ích này chỉ định một file descriptor mà vào đó số hiệu tín hiệu được ghi dưới dạng một byte mỗi khi nhận được tín hiệu. *fd* phải ở chế độ non-blocking. Hàm trả về file descriptor trước đó.

   Giá trị ``-1`` sẽ tắt tính năng này; đây là trạng thái ban đầu. Trong Python, giá trị này tương đương với :func:`signal.set_wakeup_fd`, nhưng không thực hiện kiểm tra lỗi. *fd* phải là một file descriptor hợp lệ. Chỉ nên gọi hàm này từ luồng chính.

   .. versionchanged:: 3.5
      Trên Windows, hàm này hiện cũng hỗ trợ các socket handle.


Các lớp ngoại lệ
================

.. c:function:: PyObject* PyErr_NewException(const char *name, PyObject *base, PyObject *dict)

   Hàm tiện ích này tạo và trả về một lớp ngoại lệ mới. Đối số *name* phải là tên của ngoại lệ mới, một chuỗi C có dạng ``module.classname``. Các đối số *base* và *dict* thường là ``NULL``. Thao tác này tạo một đối tượng lớp kế thừa từ :exc:`Exception` (có thể truy cập trong C dưới dạng
   :c:data:`PyExc_Exception`).

   Thuộc tính :attr:`~type.__module__` của lớp mới được đặt thành phần đầu tiên (tính đến dấu chấm cuối cùng) của đối số *name*, còn tên lớp được đặt thành phần cuối cùng (sau dấu chấm cuối cùng). Đối số *base* có thể được dùng để chỉ định các lớp cơ sở thay thế; đối số này có thể là một lớp duy nhất hoặc một tuple các lớp. Đối số *dict* có thể được dùng để chỉ định một dictionary gồm các biến và phương thức của lớp.


.. c:function:: PyObject* PyErr_NewExceptionWithDoc(const char *name, const char *doc, PyObject *base, PyObject *dict)

   Tương tự như :c:func:`PyErr_NewException`, ngoại trừ việc lớp ngoại lệ mới có thể dễ dàng được gán docstring: Nếu *doc* khác ``NULL``, giá trị này sẽ được dùng làm docstring cho lớp ngoại lệ.

   .. versionadded:: 3.2


.. c:function:: int PyExceptionClass_Check(PyObject *ob)

   Trả về giá trị khác 0 nếu *ob* là một lớp ngoại lệ, nếu không thì trả về 0. Hàm này luôn thành công.


.. c:function:: const char *PyExceptionClass_Name(PyObject *ob)

   Trả về :c:member:`~PyTypeObject.tp_name` của lớp ngoại lệ *ob*.


Đối tượng ngoại lệ
==================

.. c:function:: int PyExceptionInstance_Check(PyObject *op)

   Trả về true nếu *op* là một thể hiện của :class:`BaseException`, nếu không thì trả về false. Hàm này luôn thành công.


.. c:macro:: PyExceptionInstance_Class(op)

   Tương đương với :c:func:`Py_TYPE(op) <Py_TYPE>`.


.. c:function:: PyObject* PyException_GetTraceback(PyObject *ex)

   Trả về traceback liên kết với ngoại lệ dưới dạng một tham chiếu mới, có thể truy cập từ Python thông qua thuộc tính :attr:`~BaseException.__traceback__`. Nếu không có traceback liên kết, hàm này trả về ``NULL``.


.. c:function:: int PyException_SetTraceback(PyObject *ex, PyObject *tb)

   Đặt traceback liên kết với ngoại lệ thành *tb*. Sử dụng ``Py_None`` để xóa traceback.


.. c:function:: PyObject* PyException_GetContext(PyObject *ex)

   Trả về context (một instance ngoại lệ khác trong quá trình xử lý instance đó, *ex* đã được phát sinh) được liên kết với ngoại lệ dưới dạng một tham chiếu mới, có thể truy cập từ Python thông qua thuộc tính :attr:`~BaseException.__context__`. Nếu không có context được liên kết, hàm này trả về ``NULL``.


.. c:function:: void PyException_SetContext(PyObject *ex, PyObject *ctx)

   Đặt context được liên kết với ngoại lệ thành *ctx*. Sử dụng ``NULL`` để xóa nó. Không có kiểm tra kiểu để đảm bảo rằng *ctx* là một instance ngoại lệ. Thao tác này ":term:`steals <steal>`" một tham chiếu đến *ctx*.


.. c:function:: PyObject* PyException_GetCause(PyObject *ex)

   Trả về cause (một instance ngoại lệ hoặc ``None``, được đặt bởi ``raise ... from ...``) được liên kết với ngoại lệ dưới dạng một tham chiếu mới, có thể truy cập từ Python thông qua
   thuộc tính :attr:`~BaseException.__cause__`.


.. c:function:: void PyException_SetCause(PyObject *ex, PyObject *cause)

   Đặt cause được liên kết với ngoại lệ thành *cause*. Sử dụng ``NULL`` để xóa nó. Không có kiểm tra kiểu để đảm bảo rằng *cause* là một instance ngoại lệ hoặc ``None``. Thao tác này ":term:`steals <steal>`" một tham chiếu đến *cause*.

   Thuộc tính :attr:`~BaseException.__suppress_context__` được hàm này ngầm định đặt thành ``True``.


.. c:function:: PyObject* PyException_GetArgs(PyObject *ex)

   Trả về :attr:`~BaseException.args` của ngoại lệ *ex*.


.. c:function:: void PyException_SetArgs(PyObject *ex, PyObject *args)

   Đặt :attr:`~BaseException.args` của ngoại lệ *ex* thành *args*.

.. c:function:: PyObject* PyUnstable_Exc_PrepReraiseStar(PyObject *orig, PyObject *excs)

   Triển khai một phần trong implementation của interpreter cho :keyword:`!except*`. *orig* là ngoại lệ gốc đã được bắt, còn *excs* là danh sách các ngoại lệ cần được raise. Danh sách này chứa phần chưa được xử lý của *orig*, nếu có, cũng như các ngoại lệ được raise từ
   các mệnh đề :keyword:`!except*` (vì vậy chúng có traceback khác với *orig*) và các ngoại lệ được raise lại (có cùng traceback với *orig*). Trả về :exc:`ExceptionGroup` cần được raise lại sau cùng, hoặc ``None`` nếu không có gì cần raise lại.

   .. versionadded:: 3.12

.. _unicodeexceptions:

Đối tượng ngoại lệ Unicode
==========================

Các hàm sau được dùng để tạo và sửa đổi các ngoại lệ Unicode từ C.

.. c:function:: PyObject* PyUnicodeDecodeError_Create(const char *encoding, const char *object, Py_ssize_t length, Py_ssize_t start, Py_ssize_t end, const char *reason)

   Tạo một đối tượng :class:`UnicodeDecodeError` với các thuộc tính *encoding*, *object*, *length*, *start*, *end* và *reason*. *encoding* và *reason* là các chuỗi được mã hóa UTF-8.

.. c:function:: PyObject* PyUnicodeDecodeError_GetEncoding(PyObject *exc)
                PyObject* PyUnicodeEncodeError_GetEncoding(PyObject *exc)

   Trả về thuộc tính *encoding* của đối tượng ngoại lệ đã cho.

.. c:function:: PyObject* PyUnicodeDecodeError_GetObject(PyObject *exc)
                PyObject* PyUnicodeEncodeError_GetObject(PyObject *exc) PyObject* PyUnicodeTranslateError_GetObject(PyObject *exc)

   Trả về thuộc tính *object* của đối tượng ngoại lệ đã cho.

.. c:function:: int PyUnicodeDecodeError_GetStart(PyObject *exc, Py_ssize_t *start)
                int PyUnicodeEncodeError_GetStart(PyObject *exc, Py_ssize_t *start) int PyUnicodeTranslateError_GetStart(PyObject *exc, Py_ssize_t *start)

   Lấy thuộc tính *start* của đối tượng ngoại lệ đã cho và đặt thuộc tính đó vào *\*start*. *start* không được là ``NULL``. Trả về ``0`` nếu thành công và ``-1`` nếu thất bại.

   Nếu :attr:`UnicodeError.object` là một sequence rỗng, *start* kết quả là ``0``. Nếu không, giá trị này được giới hạn ở ``[0, len(object) - 1]``.

   .. seealso:: :attr:`UnicodeError.start`

.. c:function:: int PyUnicodeDecodeError_SetStart(PyObject *exc, Py_ssize_t start)
                int PyUnicodeEncodeError_SetStart(PyObject *exc, Py_ssize_t start) int PyUnicodeTranslateError_SetStart(PyObject *exc, Py_ssize_t start)

   Đặt thuộc tính *start* của đối tượng ngoại lệ đã cho thành *start*. Trả về ``0`` nếu thành công, ``-1`` nếu thất bại.

   .. note::

      Mặc dù việc truyền *start* âm không gây ra ngoại lệ, các getter tương ứng sẽ không coi đó là một độ lệch tương đối.

.. c:function:: int PyUnicodeDecodeError_GetEnd(PyObject *exc, Py_ssize_t *end)
                int PyUnicodeEncodeError_GetEnd(PyObject *exc, Py_ssize_t *end) int PyUnicodeTranslateError_GetEnd(PyObject *exc, Py_ssize_t *end)

   Lấy thuộc tính *end* của đối tượng ngoại lệ đã cho và đặt nó vào *\*end*. *end* không được là ``NULL``. Trả về ``0`` nếu thành công, ``-1`` nếu thất bại.

   Nếu :attr:`UnicodeError.object` là một chuỗi rỗng, *end* kết quả là ``0``. Nếu không, nó được giới hạn ở ``[1, len(object)]``.

.. c:function:: int PyUnicodeDecodeError_SetEnd(PyObject *exc, Py_ssize_t end)
                int PyUnicodeEncodeError_SetEnd(PyObject *exc, Py_ssize_t end) int PyUnicodeTranslateError_SetEnd(PyObject *exc, Py_ssize_t end)

   Đặt thuộc tính *end* của đối tượng ngoại lệ đã cho thành *end*. Trả về ``0`` nếu thành công, ``-1`` nếu thất bại.

   .. seealso:: :attr:`UnicodeError.end`

.. c:function:: PyObject* PyUnicodeDecodeError_GetReason(PyObject *exc)
                PyObject* PyUnicodeEncodeError_GetReason(PyObject *exc) PyObject* PyUnicodeTranslateError_GetReason(PyObject *exc)

   Trả về thuộc tính *reason* của đối tượng exception đã cho.

.. c:function:: int PyUnicodeDecodeError_SetReason(PyObject *exc, const char *reason)
                int PyUnicodeEncodeError_SetReason(PyObject *exc, const char *reason) int PyUnicodeTranslateError_SetReason(PyObject *exc, const char *reason)

   Đặt thuộc tính *reason* của đối tượng exception đã cho thành *reason*. Trả về ``0`` khi thành công, ``-1`` khi thất bại.


.. _recursion:

Điều khiển đệ quy
=================

Hai hàm này cung cấp một cách để thực hiện các lời gọi đệ quy an toàn ở cấp C, cả trong phần lõi lẫn trong các module mở rộng. Chúng cần thiết nếu mã đệ quy không nhất thiết gọi mã Python (vốn tự động theo dõi độ sâu đệ quy). Chúng cũng không cần thiết cho các triển khai *tp_call* vì :ref:`call protocol <call>` đảm nhiệm việc xử lý đệ quy.

.. c:function:: int Py_EnterRecursiveCall(const char *where)

   Đánh dấu một điểm sắp thực hiện lời gọi đệ quy ở cấp C.

   Sau đó, hàm kiểm tra xem đã đạt đến giới hạn stack hay chưa. Nếu đã đạt, một :exc:`RecursionError` sẽ được thiết lập và hàm trả về giá trị khác không. Nếu không, hàm trả về số không.

   Việc kiểm tra dựa trên dung lượng stack C còn lại của thread hiện tại, không dựa trên số lần gọi, nên không bị ảnh hưởng bởi
   :c:func:`Py_SetRecursionLimit` và :func:`sys.setrecursionlimit`.

   *trong đó* phải là một chuỗi được mã hóa UTF-8, chẳng hạn như ``" in instance check"``, để nối vào thông báo :exc:`RecursionError` do giới hạn độ sâu đệ quy gây ra.

   .. seealso::
      Hàm :c:func:`PyUnstable_ThreadState_SetStackProtection`.

   .. versionchanged:: 3.9
      Hiện chức năng này cũng có trong :ref:`limited API <limited-c-api>`.

   .. versionchanged:: 3.14
      Việc kiểm tra dựa trên dung lượng stack C còn lại. Trước đây, một bộ đếm riêng cho các lần gọi ở cấp C được sử dụng.

.. c:function:: void Py_LeaveRecursiveCall(void)

   Kết thúc một :c:func:`Py_EnterRecursiveCall`. Phải được gọi một lần cho mỗi *lần gọi thành công* của :c:func:`Py_EnterRecursiveCall`.

   .. versionchanged:: 3.9
      Hiện chức năng này cũng có trong :ref:`limited API <limited-c-api>`.

Việc triển khai đúng :c:member:`~PyTypeObject.tp_repr` cho các kiểu container đòi hỏi phải xử lý đệ quy đặc biệt. Ngoài việc bảo vệ ngăn xếp,
:c:member:`~PyTypeObject.tp_repr` cũng cần theo dõi các đối tượng để ngăn chu kỳ. Hai hàm sau hỗ trợ chức năng này. Về bản chất, đây là tương đương trong C của :deco:`reprlib.recursive_repr`.

.. c:function:: int Py_ReprEnter(PyObject *object)

   Được gọi ở đầu phần triển khai :c:member:`~PyTypeObject.tp_repr` để phát hiện chu kỳ.

   Nếu đối tượng đã được xử lý, hàm sẽ trả về một số nguyên dương. Trong trường hợp đó, phần triển khai :c:member:`~PyTypeObject.tp_repr` nên trả về một đối tượng chuỗi cho biết đã phát hiện chu kỳ. Ví dụ,
   Các đối tượng :class:`dict` trả về ``{...}`` còn các đối tượng :class:`list` trả về ``[...]``.

   Hàm sẽ trả về một số nguyên âm nếu đạt đến giới hạn đệ quy. Trong trường hợp đó, implementation :c:member:`~PyTypeObject.tp_repr` thường phải trả về ``NULL``.

   Nếu không, hàm trả về số 0 và implementation :c:member:`~PyTypeObject.tp_repr` có thể tiếp tục hoạt động bình thường.

.. c:function:: void Py_ReprLeave(PyObject *object)

   Kết thúc một :c:func:`Py_ReprEnter`. Phải được gọi một lần cho mỗi lần gọi :c:func:`Py_ReprEnter` trả về số 0.

.. c:function:: int Py_GetRecursionLimit(void)

   Lấy giới hạn đệ quy của interpreter hiện tại. Có thể thiết lập giới hạn này bằng
   :c:func:`Py_SetRecursionLimit`. Giới hạn đệ quy ngăn không cho ngăn xếp của Python interpreter phát triển vô hạn.

   Hàm này không thể thất bại và caller phải nắm giữ một
   :term:`attached thread state`.

   .. seealso::
      :py:func:`sys.getrecursionlimit`

.. c:function:: void Py_SetRecursionLimit(int new_limit)

   Thiết lập giới hạn đệ quy cho interpreter hiện tại.

   Hàm này không thể thất bại và caller phải nắm giữ một
   :term:`attached thread state`.

   .. seealso::
      :py:func:`sys.setrecursionlimit`

.. _standardexceptions:

Các loại ngoại lệ và cảnh báo
=============================

Tất cả các ngoại lệ Python tiêu chuẩn và danh mục cảnh báo đều có sẵn dưới dạng các biến toàn cục có tên là ``PyExc_`` theo sau là tên ngoại lệ Python. Chúng có kiểu :c:expr:`PyObject*`; tất cả đều là các đối tượng lớp.

Để đầy đủ, dưới đây là tất cả các biến:

Các loại ngoại lệ
-----------------

.. list-table::
   :align: left
   :widths: auto
   :header-rows: 1

   * * Tên C
     * Tên Python
   * * .. c:var:: PyObject *PyExc_BaseException
     * :exc:`BaseException`
   * * .. c:var:: PyObject *PyExc_BaseExceptionGroup
     * :exc:`BaseExceptionGroup`
   * * .. c:var:: PyObject *PyExc_Exception
     * :exc:`Exception`
   * * .. c:var:: PyObject *PyExc_ArithmeticError
     * :exc:`ArithmeticError`
   * * .. c:var:: PyObject *PyExc_AssertionError
     * :exc:`AssertionError`
   * * .. c:var:: PyObject *PyExc_AttributeError
     * :exc:`AttributeError`
   * * .. c:var:: PyObject *PyExc_BlockingIOError
     * :exc:`BlockingIOError`
   * * .. c:var:: PyObject *PyExc_BrokenPipeError
     * :exc:`BrokenPipeError`
   * * .. c:var:: PyObject *PyExc_BufferError
     * :exc:`BufferError`
   * * .. c:var:: PyObject *PyExc_ChildProcessError
     * :exc:`ChildProcessError`
   * * .. c:var:: PyObject *PyExc_ConnectionAbortedError
     * :exc:`ConnectionAbortedError`
   * * .. c:var:: PyObject *PyExc_ConnectionError
     * :exc:`ConnectionError`
   * * .. c:var:: PyObject *PyExc_ConnectionRefusedError
     * :exc:`ConnectionRefusedError`
   * * .. c:var:: PyObject *PyExc_ConnectionResetError
     * :exc:`ConnectionResetError`
   * * .. c:var:: PyObject *PyExc_EOFError
     * :exc:`EOFError`
   * * .. c:var:: PyObject *PyExc_FileExistsError
     * :exc:`FileExistsError`
   * * .. c:var:: PyObject *PyExc_FileNotFoundError
     * :exc:`FileNotFoundError`
   * * .. c:var:: PyObject *PyExc_FloatingPointError
     * :exc:`FloatingPointError`
   * * .. c:var:: PyObject *PyExc_GeneratorExit
     * :exc:`GeneratorExit`
   * * .. c:var:: PyObject *PyExc_ImportError
     * :exc:`ImportError`
   * * .. c:var:: PyObject *PyExc_IndentationError
     * :exc:`IndentationError`
   * * .. c:var:: PyObject *PyExc_IndexError
     * :exc:`IndexError`
   * * .. c:var:: PyObject *PyExc_InterruptedError
     * :exc:`InterruptedError`
   * * .. c:var:: PyObject *PyExc_IsADirectoryError
     * :exc:`IsADirectoryError`
   * * .. c:var:: PyObject *PyExc_KeyError
     * :exc:`KeyError`
   * * .. c:var:: PyObject *PyExc_KeyboardInterrupt
     * :exc:`KeyboardInterrupt`
   * * .. c:var:: PyObject *PyExc_LookupError
     * :exc:`LookupError`
   * * .. c:var:: PyObject *PyExc_MemoryError
     * :exc:`MemoryError`
   * * .. c:var:: PyObject *PyExc_ModuleNotFoundError
     * :exc:`ModuleNotFoundError`
   * * .. c:var:: PyObject *PyExc_NameError
     * :exc:`NameError`
   * * .. c:var:: PyObject *PyExc_NotADirectoryError
     * :exc:`NotADirectoryError`
   * * .. c:var:: PyObject *PyExc_NotImplementedError
     * :exc:`NotImplementedError`
   * * .. c:var:: PyObject *PyExc_OSError
     * :exc:`OSError`
   * * .. c:var:: PyObject *PyExc_OverflowError
     * :exc:`OverflowError`
   * * .. c:var:: PyObject *PyExc_PermissionError
     * :exc:`PermissionError`
   * * .. c:var:: PyObject *PyExc_ProcessLookupError
     * :exc:`ProcessLookupError`
   * * .. c:var:: PyObject *PyExc_PythonFinalizationError
     * :exc:`PythonFinalizationError`
   * * .. c:var:: PyObject *PyExc_RecursionError
     * :exc:`RecursionError`
   * * .. c:var:: PyObject *PyExc_ReferenceError
     * :exc:`ReferenceError`
   * * .. c:var:: PyObject *PyExc_RuntimeError
     * :exc:`RuntimeError`
   * * .. c:var:: PyObject *PyExc_StopAsyncIteration
     * :exc:`StopAsyncIteration`
   * * .. c:var:: PyObject *PyExc_StopIteration
     * :exc:`StopIteration`
   * * .. c:var:: PyObject *PyExc_SyntaxError
     * :exc:`SyntaxError`
   * * .. c:var:: PyObject *PyExc_SystemError
     * :exc:`SystemError`
   * * .. c:var:: PyObject *PyExc_SystemExit
     * :exc:`SystemExit`
   * * .. c:var:: PyObject *PyExc_TabError
     * :exc:`TabError`
   * * .. c:var:: PyObject *PyExc_TimeoutError
     * :exc:`TimeoutError`
   * * .. c:var:: PyObject *PyExc_TypeError
     * :exc:`TypeError`
   * * .. c:var:: PyObject *PyExc_UnboundLocalError
     * :exc:`UnboundLocalError`
   * * .. c:var:: PyObject *PyExc_UnicodeDecodeError
     * :exc:`UnicodeDecodeError`
   * * .. c:var:: PyObject *PyExc_UnicodeEncodeError
     * :exc:`UnicodeEncodeError`
   * * .. c:var:: PyObject *PyExc_UnicodeError
     * :exc:`UnicodeError`
   * * .. c:var:: PyObject *PyExc_UnicodeTranslateError
     * :exc:`UnicodeTranslateError`
   * * .. c:var:: PyObject *PyExc_ValueError
     * :exc:`ValueError`
   * * .. c:var:: PyObject *PyExc_ZeroDivisionError
     * :exc:`ZeroDivisionError`

.. versionadded:: 3.3
   :c:data:`PyExc_BlockingIOError`, :c:data:`PyExc_BrokenPipeError`,
   :c:data:`PyExc_ChildProcessError`, :c:data:`PyExc_ConnectionError`,
   :c:data:`PyExc_ConnectionAbortedError`, :c:data:`PyExc_ConnectionRefusedError`,
   :c:data:`PyExc_ConnectionResetError`, :c:data:`PyExc_FileExistsError`,
   :c:data:`PyExc_FileNotFoundError`, :c:data:`PyExc_InterruptedError`,
   :c:data:`PyExc_IsADirectoryError`, :c:data:`PyExc_NotADirectoryError`,
   :c:data:`PyExc_PermissionError`, :c:data:`PyExc_ProcessLookupError`
   và :c:data:`PyExc_TimeoutError` được giới thiệu sau :pep:`3151`.

.. versionadded:: 3.5
   :c:data:`PyExc_StopAsyncIteration` and :c:data:`PyExc_RecursionError`.

.. versionadded:: 3.6
   :c:data:`PyExc_ModuleNotFoundError`.

.. versionadded:: 3.11
   :c:data:`PyExc_BaseExceptionGroup`.


Các bí danh OSError
-------------------

Sau đây là các bí danh tương thích với :c:data:`PyExc_OSError`.

.. versionchanged:: 3.3
   Các bí danh này trước đây là những kiểu ngoại lệ riêng biệt.

.. list-table::
   :align: left
   :widths: auto
   :header-rows: 1

   * * Tên C
     * Tên Python
     * Ghi chú
   * * .. c:var:: PyObject *PyExc_EnvironmentError
     * :exc:`OSError`
     *
   * * .. c:var:: PyObject *PyExc_IOError
     * :exc:`OSError`
     *
   * * .. c:var:: PyObject *PyExc_WindowsError
     * :exc:`OSError`
     * [win]_

Ghi chú:

.. [win]
   :c:var:`!PyExc_WindowsError` chỉ được định nghĩa trên Windows; hãy bảo vệ mã sử dụng nó bằng cách kiểm tra xem macro tiền xử lý ``MS_WINDOWS`` đã được định nghĩa hay chưa.


.. _standardwarningcategories:

Các loại cảnh báo
-----------------

.. list-table::
   :align: left
   :widths: auto
   :header-rows: 1

   * * Tên C
     * Tên Python
   * * .. c:var:: PyObject *PyExc_Warning
     * :exc:`Warning`
   * * .. c:var:: PyObject *PyExc_BytesWarning
     * :exc:`BytesWarning`
   * * .. c:var:: PyObject *PyExc_DeprecationWarning
     * :exc:`DeprecationWarning`
   * * .. c:var:: PyObject *PyExc_EncodingWarning
     * :exc:`EncodingWarning`
   * * .. c:var:: PyObject *PyExc_FutureWarning
     * :exc:`FutureWarning`
   * * .. c:var:: PyObject *PyExc_ImportWarning
     * :exc:`ImportWarning`
   * * .. c:var:: PyObject *PyExc_PendingDeprecationWarning
     * :exc:`PendingDeprecationWarning`
   * * .. c:var:: PyObject *PyExc_ResourceWarning
     * :exc:`ResourceWarning`
   * * .. c:var:: PyObject *PyExc_RuntimeWarning
     * :exc:`RuntimeWarning`
   * * .. c:var:: PyObject *PyExc_SyntaxWarning
     * :exc:`SyntaxWarning`
   * * .. c:var:: PyObject *PyExc_UnicodeWarning
     * :exc:`UnicodeWarning`
   * * .. c:var:: PyObject *PyExc_UserWarning
     * :exc:`UserWarning`

.. versionadded:: 3.2
   :c:data:`PyExc_ResourceWarning`.

.. versionadded:: 3.10
   :c:data:`PyExc_EncodingWarning`.


Traceback
=========

.. c:var:: PyTypeObject PyTraceBack_Type

   Đối tượng kiểu dành cho các đối tượng traceback. Đối tượng này có sẵn dưới dạng
   :class:`types.TracebackType` trong lớp Python.


.. c:function:: int PyTraceBack_Check(PyObject *op)

   Trả về true nếu *op* là một đối tượng traceback, ngược lại trả về false. Hàm này không tính đến các subtype.


.. c:function:: int PyTraceBack_Here(PyFrameObject *f)

   Thay thế thuộc tính :attr:`~BaseException.__traceback__` của exception hiện tại bằng một traceback mới, thêm *f* vào đầu chuỗi hiện có.

   Việc gọi hàm này khi chưa thiết lập exception sẽ dẫn đến hành vi không xác định.

   Hàm này trả về ``0`` khi thành công và trả về ``-1`` cùng với một exception được thiết lập khi thất bại.


.. c:function:: int PyTraceBack_Print(PyObject *tb, PyObject *f)

   Ghi traceback *tb* vào tệp *f*.

   Hàm này trả về ``0`` khi thành công và trả về ``-1`` cùng với một exception được thiết lập khi thất bại.
