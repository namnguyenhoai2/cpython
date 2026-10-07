.. highlight:: c

.. _os:

Tiện ích hệ điều hành
=====================


.. c:function:: PyObject* PyOS_FSPath(PyObject *path)

   Trả về biểu diễn hệ thống tệp cho *path*. Nếu đối tượng là một
   :class:`str` hoặc đối tượng :class:`bytes`, thì một đối tượng mới
   :term:`strong reference` được trả về. Nếu đối tượng triển khai giao diện :class:`os.PathLike`, thì :meth:`~os.PathLike.__fspath__` được trả về miễn là nó là một
   :class:`str` hoặc đối tượng :class:`bytes`. Nếu không, :exc:`TypeError` được phát sinh và ``NULL`` được trả về.

   .. versionadded:: 3.6


.. c:function:: int Py_FdIsInteractive(FILE *fp, const char *filename)

   Trả về true (khác không) nếu tệp I/O chuẩn *fp* có tên *filename* được xem là tương tác. Đây là trường hợp đối với các tệp mà ``isatty(fileno(fp))`` là true. Nếu :c:member:`PyConfig.interactive` khác không, hàm này cũng trả về true nếu con trỏ *filename* là ``NULL`` hoặc nếu tên bằng một trong các chuỗi ``'<stdin>'`` hoặc ``'???'``.

   Không được gọi hàm này trước khi Python được khởi tạo.


.. c:function:: void PyOS_BeforeFork()

   Hàm chuẩn bị một số trạng thái nội bộ trước khi fork tiến trình. Hàm này nên được gọi trước khi gọi :c:func:`fork` hoặc bất kỳ hàm tương tự nào sao chép tiến trình hiện tại. Chỉ khả dụng trên các hệ thống nơi :c:func:`fork` được định nghĩa.

   .. warning::
      Lời gọi C :c:func:`fork` chỉ nên được thực hiện từ
      :ref:`luồng "main" <fork-and-threads>` (của
      :ref:`trình thông dịch "main" <sub-interpreter-support>`). Điều tương tự cũng đúng với ``PyOS_BeforeFork()``.

   .. versionadded:: 3.7


.. c:function:: void PyOS_AfterFork_Parent()

   Hàm cập nhật một số trạng thái nội bộ sau khi fork tiến trình. Hàm này nên được gọi từ tiến trình cha sau khi gọi :c:func:`fork` hoặc bất kỳ hàm tương tự nào sao chép tiến trình hiện tại, bất kể việc sao chép tiến trình có thành công hay không. Chỉ khả dụng trên các hệ thống nơi :c:func:`fork` được định nghĩa.

   .. warning::
      Lời gọi C :c:func:`fork` chỉ nên được thực hiện từ
      :ref:`luồng "main" <fork-and-threads>` (của
      :ref:`"main" trình thông dịch <sub-interpreter-support>`).  Điều tương tự cũng đúng với ``PyOS_AfterFork_Parent()``.

   .. versionadded:: 3.7


.. c:function:: void PyOS_AfterFork_Child()

   Hàm cập nhật trạng thái nội bộ của trình thông dịch sau khi fork tiến trình. Hàm này phải được gọi từ tiến trình con sau khi gọi :c:func:`fork`, hoặc bất kỳ hàm tương tự nào sao chép tiến trình hiện tại, nếu có khả năng tiến trình đó sẽ gọi lại vào trình thông dịch Python. Chỉ khả dụng trên các hệ thống nơi :c:func:`fork` được định nghĩa.

   .. warning::
      Lời gọi C :c:func:`fork` chỉ nên được thực hiện từ
      :ref:`luồng "main" <fork-and-threads>` (của
      :ref:`"main" trình thông dịch <sub-interpreter-support>`).  Điều tương tự cũng đúng với ``PyOS_AfterFork_Child()``.

   .. versionadded:: 3.7

   .. seealso::
      :func:`os.register_at_fork` allows registering custom Python functions
      được gọi bởi :c:func:`PyOS_BeforeFork()`,
      :c:func:`PyOS_AfterFork_Parent` và  :c:func:`PyOS_AfterFork_Child`.


.. c:function:: void PyOS_AfterFork()

   Hàm cập nhật một số trạng thái nội bộ sau khi fork tiến trình; hàm này nên được gọi trong tiến trình mới nếu trình thông dịch Python sẽ tiếp tục được sử dụng. Nếu một tệp thực thi mới được tải vào tiến trình mới, không cần gọi hàm này.

   .. deprecated:: 3.7
      Hàm này đã được thay thế bằng :c:func:`PyOS_AfterFork_Child()`.


.. c:function:: int PyOS_CheckStack()

   .. index:: single: USE_STACKCHECK (C macro)

   Trả về true khi trình thông dịch hết không gian ngăn xếp. Đây là một phép kiểm tra đáng tin cậy, nhưng chỉ khả dụng khi :c:macro:`!USE_STACKCHECK` được định nghĩa (hiện chỉ có trên một số phiên bản Windows sử dụng trình biên dịch Microsoft Visual C++).
   :c:macro:`!USE_STACKCHECK` sẽ được tự động định nghĩa; bạn không bao giờ nên thay đổi định nghĩa này trong mã của mình.


.. c:type::  void (*PyOS_sighandler_t)(int)


.. c:function:: PyOS_sighandler_t PyOS_getsig(int i)

   Trả về trình xử lý tín hiệu hiện tại cho tín hiệu *i*. Đây là một wrapper mỏng quanh :c:func:`!sigaction` hoặc :c:func:`!signal`. Không được gọi trực tiếp các hàm đó!


.. c:function:: PyOS_sighandler_t PyOS_setsig(int i, PyOS_sighandler_t h)

   Đặt trình xử lý tín hiệu cho tín hiệu *i* thành *h*; trả về trình xử lý tín hiệu cũ. Đây là một wrapper mỏng quanh :c:func:`!sigaction` hoặc :c:func:`!signal`. Không được gọi trực tiếp các hàm đó!


.. c:function:: int PyOS_InterruptOccurred(void)

   Kiểm tra xem tín hiệu :c:macro:`!SIGINT` có được nhận hay không.

   Trả về ``1`` nếu :c:macro:`!SIGINT` đã xảy ra và xóa cờ tín hiệu, hoặc ``0`` nếu không.

   Trong hầu hết các trường hợp, bạn nên ưu tiên :c:func:`PyErr_CheckSignals` hơn hàm này.
   :c:func:`!PyErr_CheckSignals` gọi các trình xử lý tín hiệu thích hợp cho tất cả tín hiệu đang chờ, cho phép mã Python xử lý tín hiệu đúng cách. Hàm này chỉ phát hiện :c:macro:`!SIGINT` và không gọi bất kỳ trình xử lý tín hiệu Python nào.

   Hàm này an toàn với tín hiệu bất đồng bộ và không thể thất bại. Bên gọi phải nắm giữ một :term:`attached thread state`.


.. c:function:: wchar_t* Py_DecodeLocale(const char* arg, size_t *size)

   .. warning::
      Không nên gọi trực tiếp hàm này: hãy sử dụng API :c:type:`PyConfig` cùng với hàm :c:func:`PyConfig_SetBytesString`, hàm này bảo đảm rằng :ref:`Python được khởi tạo trước <c-preinit>`.

      Không được gọi hàm này trước khi :ref:`Python được khởi tạo trước <c-preinit>` và để locale LC_CTYPE được cấu hình đúng cách: xem hàm :c:func:`Py_PreInitialize`.

   Giải mã một chuỗi byte từ :term:`filesystem encoding and error handler`. Nếu trình xử lý lỗi là :ref:`trình xử lý lỗi surrogateescape <surrogateescape>`, các byte không thể giải mã sẽ được giải mã thành các ký tự trong phạm vi U+DC80..U+DCFF; và nếu một chuỗi byte có thể được giải mã thành một ký tự surrogate, các byte sẽ được escape bằng trình xử lý lỗi surrogateescape thay vì được giải mã.

   Trả về một con trỏ tới chuỗi ký tự wide mới được cấp phát, sử dụng
   :c:func:`PyMem_RawFree` để giải phóng bộ nhớ. Nếu size không phải là ``NULL``, ghi số ký tự wide, không bao gồm ký tự null, vào ``*size``

   Trả về ``NULL`` nếu xảy ra lỗi giải mã hoặc lỗi cấp phát bộ nhớ. Nếu *size* không phải là ``NULL``, ``*size`` được đặt thành ``(size_t)-1`` khi có lỗi bộ nhớ hoặc thành ``(size_t)-2`` khi có lỗi giải mã.

   :term:`filesystem encoding and error handler` được chọn bởi
   :c:func:`PyConfig_Read`: xem :c:member:`~PyConfig.filesystem_encoding` và
   các thành viên :c:member:`~PyConfig.filesystem_errors` của :c:type:`PyConfig`.

   Lỗi giải mã không bao giờ xảy ra, trừ khi có lỗi trong thư viện C.

   Sử dụng hàm :c:func:`Py_EncodeLocale` để mã hóa chuỗi ký tự thành chuỗi byte.

   .. seealso::

      :c:func:`PyUnicode_DecodeFSDefaultAndSize` và
      các hàm :c:func:`PyUnicode_DecodeLocaleAndSize`.

   .. versionadded:: 3.5

   .. versionchanged:: 3.7
      Hàm này hiện sử dụng bảng mã UTF-8 trong :ref:`Chế độ UTF-8 của Python <utf8-mode>`.

   .. versionchanged:: 3.8
      Hàm này hiện sử dụng bảng mã UTF-8 trên Windows nếu
      :c:member:`PyPreConfig.legacy_windows_fs_encoding` bằng không;


.. c:function:: char* Py_EncodeLocale(const wchar_t *text, size_t *error_pos)

   Mã hóa một chuỗi ký tự wide thành :term:`filesystem encoding and error handler`. Nếu trình xử lý lỗi là :ref:`trình xử lý lỗi surrogateescape <surrogateescape>`, các ký tự surrogate trong phạm vi U+DC80..U+DCFF sẽ được chuyển đổi thành các byte 0x80..0xFF.

   Trả về một con trỏ đến chuỗi byte mới được cấp phát, sử dụng :c:func:`PyMem_Free` để giải phóng bộ nhớ. Trả về ``NULL`` khi xảy ra lỗi mã hóa hoặc lỗi cấp phát bộ nhớ.

   Nếu error_pos không phải là ``NULL``, ``*error_pos`` được đặt thành ``(size_t)-1`` khi thành công hoặc được đặt thành chỉ mục của ký tự không hợp lệ khi xảy ra lỗi mã hóa.

   :term:`filesystem encoding and error handler` được chọn bởi
   :c:func:`PyConfig_Read`: xem :c:member:`~PyConfig.filesystem_encoding` và
   các thành viên :c:member:`~PyConfig.filesystem_errors` của :c:type:`PyConfig`.

   Sử dụng hàm :c:func:`Py_DecodeLocale` để giải mã chuỗi byte trở lại thành chuỗi ký tự rộng.

   .. warning::
      Không được gọi hàm này trước khi :ref:`Python được khởi tạo trước <c-preinit>` và để locale LC_CTYPE được cấu hình đúng cách: xem hàm :c:func:`Py_PreInitialize`.

   .. seealso::

      :c:func:`PyUnicode_EncodeFSDefault` và
      các hàm :c:func:`PyUnicode_EncodeLocale`.

   .. versionadded:: 3.5

   .. versionchanged:: 3.7
      Hàm này hiện sử dụng bảng mã UTF-8 trong :ref:`Chế độ UTF-8 của Python <utf8-mode>`.

   .. versionchanged:: 3.8
      Hàm này hiện sử dụng bảng mã UTF-8 trên Windows nếu
      :c:member:`PyPreConfig.legacy_windows_fs_encoding` bằng không.

.. c:function:: FILE* Py_fopen(PyObject *path, const char *mode)

   Tương tự :c:func:`!fopen`, nhưng *path* là một đối tượng Python và một exception được thiết lập khi xảy ra lỗi.

   *path* phải là một đối tượng :class:`str`, một đối tượng :class:`bytes` hoặc một :term:`path-like object`.

   Khi thành công, trả về con trỏ tệp mới. Khi xảy ra lỗi, đặt một ngoại lệ và trả về ``NULL``.

   Tệp phải được đóng bằng :c:func:`Py_fclose` thay vì gọi trực tiếp
   :c:func:`!fclose`.

   Bộ mô tả tệp được tạo ở trạng thái không kế thừa (:pep:`446`).

   Bên gọi phải có một :term:`attached thread state`.

   .. versionadded:: 3.14


.. c:function:: int Py_fclose(FILE *file)

   Đóng một tệp đã được mở bởi :c:func:`Py_fopen`.

   Khi thành công, trả về ``0``. Khi xảy ra lỗi, trả về ``EOF`` và ``errno`` được đặt để cho biết lỗi. Trong cả hai trường hợp, mọi lần truy cập tiếp theo (bao gồm cả một lần gọi khác tới
   :c:func:`Py_fclose`) vào luồng đều dẫn đến hành vi không xác định.

   .. versionadded:: 3.14


.. _systemfunctions:

Các hàm hệ thống
================

Đây là các hàm tiện ích giúp mã C truy cập chức năng từ module :mod:`sys`. Tất cả đều hoạt động với dict của luồng thông dịch hiện tại
của module :mod:`sys`, nằm trong cấu trúc trạng thái luồng nội bộ.

.. c:function:: PyObject *PySys_GetObject(const char *name)

   Trả về đối tượng *name* từ module :mod:`sys` hoặc ``NULL`` nếu đối tượng đó không tồn tại, mà không thiết lập ngoại lệ.

.. c:function:: int PySys_SetObject(const char *name, PyObject *v)

   Đặt *name* trong module :mod:`sys` thành *v* trừ khi *v* là ``NULL``; trong trường hợp đó, *name* sẽ bị xóa khỏi module sys. Trả về ``0`` khi thành công và ``-1`` khi có lỗi.

.. c:function:: void PySys_ResetWarnOptions()

   Đặt lại :data:`sys.warnoptions` thành một danh sách rỗng. Có thể gọi hàm này trước :c:func:`Py_Initialize`.

   .. deprecated-removed:: 3.13 3.15
      Thay vào đó, xóa :data:`sys.warnoptions` và :data:`!warnings.filters`.

.. c:function:: void PySys_WriteStdout(const char *format, ...)

   Ghi chuỗi đầu ra được mô tả bởi *format* vào :data:`sys.stdout`. Không có ngoại lệ nào được phát sinh, ngay cả khi xảy ra việc cắt ngắn (xem bên dưới).

   *format* nên giới hạn tổng kích thước của chuỗi đầu ra đã định dạng ở mức 1000 byte trở xuống -- sau 1000 byte, chuỗi đầu ra sẽ bị cắt ngắn. Cụ thể, điều này có nghĩa là không được sử dụng các định dạng "%s" không giới hạn; thay vào đó, cần giới hạn chúng bằng "%.<N>s", trong đó <N> là một số thập phân được tính sao cho <N> cộng với kích thước tối đa của phần văn bản đã định dạng khác không vượt quá 1000 byte. Ngoài ra, hãy chú ý đến "%f", vì nó có thể in ra hàng trăm chữ số đối với các số rất lớn.

   Nếu xảy ra sự cố hoặc :data:`sys.stdout` chưa được thiết lập, thông báo đã định dạng sẽ được ghi vào *stdout* thực (ở cấp độ C).

.. c:function:: void PySys_WriteStderr(const char *format, ...)

   Tương tự như :c:func:`PySys_WriteStdout`, nhưng thay vào đó ghi vào :data:`sys.stderr` hoặc *stderr*.

.. c:function:: void PySys_FormatStdout(const char *format, ...)

   Hàm tương tự như PySys_WriteStdout() nhưng định dạng thông báo bằng
   :c:func:`PyUnicode_FromFormatV` và không cắt ngắn thông báo theo một độ dài tùy ý.

   .. versionadded:: 3.2

.. c:function:: void PySys_FormatStderr(const char *format, ...)

   Tương tự như :c:func:`PySys_FormatStdout`, nhưng thay vào đó ghi vào :data:`sys.stderr` hoặc *stderr*.

   .. versionadded:: 3.2

.. c:function:: PyObject *PySys_GetXOptions()

   Trả về từ điển hiện tại của các tùy chọn :option:`-X`, tương tự như
   :data:`sys._xoptions`. Khi xảy ra lỗi, ``NULL`` được trả về và một exception được đặt.

   .. versionadded:: 3.2


.. c:function:: int PySys_Audit(const char *event, const char *format, ...)

   Phát sinh một sự kiện auditing với mọi hook đang hoạt động. Trả về số không nếu thành công và giá trị khác không kèm theo một exception được đặt nếu thất bại.

   Đối số chuỗi *event* không được là *NULL*.

   Nếu đã thêm hook, *format* và các đối số khác sẽ được dùng để tạo một tuple truyền vào. Ngoài ``N``, có thể sử dụng các ký tự định dạng giống như trong :c:func:`Py_BuildValue`. Nếu giá trị được tạo không phải là một tuple, giá trị đó sẽ được thêm vào một tuple có một phần tử.

   Không được sử dụng tùy chọn định dạng ``N``. Tùy chọn này tiêu thụ một reference, nhưng vì không có cách nào biết được các đối số của hàm này có bị tiêu thụ hay không, việc sử dụng tùy chọn này có thể gây rò rỉ reference.

   Lưu ý rằng các ký tự định dạng ``#`` luôn phải được xử lý như
   :c:type:`Py_ssize_t`, bất kể ``PY_SSIZE_T_CLEAN`` đã được định nghĩa hay chưa.

   :func:`sys.audit` thực hiện chức năng tương tự từ mã Python.

   Xem thêm :c:func:`PySys_AuditTuple`.

   .. versionadded:: 3.8

   .. versionchanged:: 3.8.2

      Yêu cầu :c:type:`Py_ssize_t` đối với các ký tự định dạng ``#``. Trước đây, một cảnh báo ngừng sử dụng không thể tránh khỏi đã được đưa ra.


.. c:function:: int PySys_AuditTuple(const char *event, PyObject *args)

   Tương tự :c:func:`PySys_Audit`, nhưng truyền các đối số dưới dạng đối tượng Python. *args* phải là một :class:`tuple`. Để không truyền đối số nào, *args* có thể là *NULL*.

   .. versionadded:: 3.13


.. c:function:: int PySys_AddAuditHook(Py_AuditHookFunction hook, void *userData)

   Thêm callable *hook* vào danh sách các hook kiểm tra đang hoạt động. Trả về số 0 khi thành công và số khác 0 khi thất bại. Nếu runtime đã được khởi tạo, đồng thời đặt một lỗi khi thất bại. Các hook được thêm thông qua API này sẽ được gọi cho tất cả interpreter do runtime tạo.

   Con trỏ *userData* được truyền vào hàm hook. Vì các hàm hook có thể được gọi từ các runtime khác nhau, con trỏ này không nên tham chiếu trực tiếp đến trạng thái Python.

   Hàm này có thể được gọi an toàn trước :c:func:`Py_Initialize`. Khi được gọi sau khi runtime được khởi tạo, các audit hook hiện có sẽ được thông báo và có thể âm thầm hủy thao tác bằng cách raise một lớp lỗi kế thừa từ
   :class:`Exception` (các lỗi khác sẽ không bị bỏ qua).

   Trình thông dịch Python gây ra sự kiện luôn gọi hàm hook với một :term:`attached thread state`.

   Xem :pep:`578` để biết mô tả chi tiết về auditing. Các hàm trong runtime và standard library phát sinh sự kiện được liệt kê trong
   :ref:`bảng các sự kiện audit <audit-events>`. Thông tin chi tiết nằm trong tài liệu của từng hàm.

   .. audit-event:: sys.addaudithook "" c.PySys_AddAuditHook

      Nếu trình thông dịch đã được khởi tạo, hàm này sẽ phát sinh một sự kiện auditing ``sys.addaudithook`` không có đối số. Nếu bất kỳ hook hiện có nào raise một ngoại lệ dẫn xuất từ :class:`Exception`, hook mới sẽ không được thêm vào và ngoại lệ sẽ được xóa. Do đó, bên gọi không thể giả định rằng hook của mình đã được thêm vào, trừ khi kiểm soát tất cả các hook hiện có.

   .. c:namespace:: NULL
   .. c:type:: int (*Py_AuditHookFunction) (const char *event, PyObject *args, void *userData)

      Kiểu của hàm hook. *event* là đối số sự kiện dạng chuỗi C được truyền đến :c:func:`PySys_Audit` hoặc
      :c:func:`PySys_AuditTuple`. *args* được đảm bảo là một :c:type:`PyTupleObject`. *userData* là đối số được truyền vào PySys_AddAuditHook().

   .. versionadded:: 3.8


.. _processcontrol:

Điều khiển tiến trình
=====================


.. c:function:: void Py_FatalError(const char *message)

   .. index:: single: abort (C function)

   In thông báo lỗi nghiêm trọng rồi kết thúc tiến trình. Không thực hiện bất kỳ thao tác dọn dẹp nào. Chỉ nên gọi hàm này khi phát hiện một điều kiện khiến việc tiếp tục sử dụng trình thông dịch Python trở nên nguy hiểm; chẳng hạn như khi có vẻ như việc quản lý đối tượng đã bị hỏng. Trên Unix, hàm thư viện C chuẩn :c:func:`!abort` được gọi và sẽ cố gắng tạo tệp :file:`core`.

   Hàm ``Py_FatalError()`` được thay thế bằng một macro tự động ghi nhật ký tên của hàm hiện tại, trừ khi macro ``Py_LIMITED_API`` được định nghĩa.

   .. versionchanged:: 3.9
      Tự động ghi nhật ký tên hàm.


.. c:function:: void Py_Exit(int status)

   .. index::
      single: Py_FinalizeEx (C function)
      single: exit (C function)

   Thoát khỏi tiến trình hiện tại. Hàm này gọi :c:func:`Py_FinalizeEx`, sau đó gọi hàm thư viện C chuẩn ``exit(status)``. Nếu :c:func:`Py_FinalizeEx` cho biết có lỗi, trạng thái thoát được đặt thành 120.

   .. versionchanged:: 3.6
      Các lỗi trong quá trình hoàn tất không còn bị bỏ qua.


.. c:function:: int Py_AtExit(void (*func) ())

   .. index::
      single: Py_FinalizeEx (C function)
      single: cleanup functions

   Đăng ký một hàm dọn dẹp để :c:func:`Py_FinalizeEx` gọi. Hàm dọn dẹp sẽ được gọi mà không có đối số nào và không nên trả về giá trị nào. Có thể đăng ký nhiều nhất 32 hàm dọn dẹp. Khi đăng ký thành công,
   :c:func:`Py_AtExit` trả về ``0``; khi thất bại, hàm này trả về ``-1``. Hàm dọn dẹp được đăng ký sau cùng sẽ được gọi trước. Mỗi hàm dọn dẹp sẽ được gọi nhiều nhất một lần. Vì quá trình finalization nội bộ của Python đã hoàn tất trước khi hàm dọn dẹp được gọi, không nên gọi API Python nào từ *func*.

   .. seealso::

      :c:func:`PyUnstable_AtExit` để truyền một đối số ``void *data``.
