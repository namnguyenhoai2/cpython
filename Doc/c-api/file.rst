.. highlight:: c

.. _fileobjects:

Đối tượng tệp
-------------

.. index:: pair: object; file

Các API này là bản mô phỏng tối thiểu của C API Python 2 dành cho các đối tượng tệp tích hợp, vốn từng dựa vào tính năng I/O có bộ đệm (:c:expr:`FILE*`) của thư viện chuẩn C. Trong Python 3, tệp và stream sử dụng
module :mod:`io`, module này định nghĩa một số tầng trên I/O không có bộ đệm cấp thấp của hệ điều hành. Các hàm được mô tả dưới đây là các wrapper C tiện ích cho những API mới này, chủ yếu предназначены cho việc báo cáo lỗi nội bộ trong trình thông dịch; mã của bên thứ ba nên truy cập các API :mod:`io` thay thế.


.. c:function:: PyObject* PyFile_FromFd(int fd, const char *name, const char *mode, int buffering, const char *encoding, const char *errors, const char *newline, int closefd)

   Tạo một đối tượng tệp Python từ file descriptor của một tệp đã được mở *fd*. Các đối số *name*, *encoding*, *errors* và *newline* có thể là ``NULL`` để sử dụng các giá trị mặc định; *buffering* có thể là *-1* để sử dụng giá trị mặc định. *name* bị bỏ qua và được giữ lại để tương thích ngược. Trả về ``NULL`` nếu thất bại. Để xem mô tả đầy đủ hơn về các đối số, hãy tham khảo tài liệu về hàm :func:`io.open`.

   .. warning::

     Vì các stream Python có lớp buffering riêng, việc trộn chúng với file descriptor cấp hệ điều hành có thể gây ra nhiều vấn đề (chẳng hạn như thứ tự dữ liệu không như mong đợi).

   .. versionchanged:: 3.2
      Bỏ qua thuộc tính *name*.


.. c:function:: int PyObject_AsFileDescriptor(PyObject *p)

   Trả về file descriptor liên kết với *p* dưới dạng một :c:expr:`int`. Nếu đối tượng là một số nguyên, giá trị của nó được trả về. Nếu không, phương thức :meth:`~io.IOBase.fileno` của đối tượng sẽ được gọi nếu tồn tại; phương thức này phải trả về một số nguyên, và số nguyên đó sẽ được trả về làm giá trị file descriptor. Thiết lập một ngoại lệ và trả về ``-1`` nếu thất bại.


.. c:function:: PyObject* PyFile_GetLine(PyObject *p, int n)

   .. index:: single: EOFError (built-in exception)

   Tương đương với ``p.readline([n])``, hàm này đọc một dòng từ đối tượng *p*. *p* có thể là một đối tượng tệp hoặc bất kỳ đối tượng nào có
   phương thức :meth:`~io.IOBase.readline`. Nếu *n* là ``0``, chính xác một dòng sẽ được đọc, bất kể độ dài của dòng. Nếu *n* lớn hơn ``0``, không quá *n* byte sẽ được đọc từ tệp; một dòng chưa đầy đủ có thể được trả về. Trong cả hai trường hợp, một chuỗi rỗng sẽ được trả về nếu gặp cuối tệp ngay lập tức. Tuy nhiên, nếu *n* nhỏ hơn ``0``, một dòng sẽ được đọc bất kể độ dài, nhưng :exc:`EOFError` sẽ được phát sinh nếu gặp cuối tệp ngay lập tức.


.. c:function:: int PyFile_SetOpenCodeHook(Py_OpenCodeHookFunction handler)

   Ghi đè hành vi thông thường của :func:`io.open_code` để truyền tham số của nó qua handler được cung cấp.

   *handler* là một hàm có kiểu:

   .. c:namespace:: NULL
   .. c:type:: PyObject * (*Py_OpenCodeHookFunction)(PyObject *, void *)

      Tương đương với :c:expr:`PyObject *(\*)(PyObject *path, void *userData)`, trong đó *path* được đảm bảo là
      :c:type:`PyUnicodeObject`.

   Con trỏ *userData* được truyền vào hàm hook. Vì các hàm hook có thể được gọi từ các runtime khác nhau, con trỏ này không nên tham chiếu trực tiếp đến trạng thái Python.

   Vì hook này được sử dụng có chủ đích trong quá trình import, hãy tránh import các module mới trong khi thực thi hook, trừ khi chúng được biết là frozen hoặc có sẵn trong ``sys.modules``.

   Sau khi một hook được thiết lập, không thể gỡ bỏ hoặc thay thế nó, và các lệnh gọi sau này tới
   :c:func:`PyFile_SetOpenCodeHook` sẽ thất bại. Khi thất bại, hàm trả về -1 và thiết lập một ngoại lệ nếu trình thông dịch đã được khởi tạo.

   Hàm này có thể được gọi an toàn trước :c:func:`Py_Initialize`.

   .. audit-event:: setopencodehook "" c.PyFile_SetOpenCodeHook

   .. versionadded:: 3.8


.. c:function:: PyObject *PyFile_OpenCodeObject(PyObject *path)

   Mở *path* bằng chế độ ``'rb'``. *path* phải là một đối tượng :class:`str` của Python. Hành vi của hàm này có thể bị ghi đè bởi
   :c:func:`PyFile_SetOpenCodeHook` để cho phép tiền xử lý văn bản.

   Hàm này tương tự như :func:`io.open_code` trong Python.

   Khi thành công, hàm này trả về một :term:`strong reference` trỏ tới một đối tượng tệp Python. Khi thất bại, hàm này trả về ``NULL`` và thiết lập một ngoại lệ.

   .. versionadded:: 3.8


.. c:function:: PyObject *PyFile_OpenCode(const char *path)

   Tương tự :c:func:`PyFile_OpenCodeObject`, nhưng *path* là một :c:expr:`const char*` được mã hóa UTF-8.

   .. versionadded:: 3.8


.. c:function:: int PyFile_WriteObject(PyObject *obj, PyObject *p, int flags)

   .. index:: single: Py_PRINT_RAW (C macro)

   Ghi đối tượng *obj* vào đối tượng tệp *p*.  Cờ duy nhất được hỗ trợ cho *flags* là
   :c:macro:`Py_PRINT_RAW`; nếu được cung cấp, :func:`str` của đối tượng sẽ được ghi thay cho :func:`repr`.

   Nếu *obj* là ``NULL``, hãy ghi chuỗi ``"<NULL>"``.

   Trả về ``0`` khi thành công hoặc ``-1`` khi thất bại; ngoại lệ thích hợp sẽ được thiết lập.

.. c:function:: int PyFile_WriteString(const char *s, PyObject *p)

   Ghi chuỗi *s* vào đối tượng tệp *p*.  Trả về ``0`` khi thành công hoặc ``-1`` khi thất bại; ngoại lệ thích hợp sẽ được thiết lập.


API không còn được khuyến khích sử dụng
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. soft-deprecated:: 3.15

Đây là các API đã vô tình được đưa vào C API của Python. Chúng chỉ được ghi chép để đầy đủ; thay vào đó, hãy sử dụng các API ``PyFile*`` khác.

.. c:function:: PyObject *PyFile_NewStdPrinter(int fd)

   Thay vào đó, hãy sử dụng :c:func:`PyFile_FromFd` với các giá trị mặc định (``fd, NULL, "w", -1, NULL, NULL, NULL, 0``).

.. c:var:: PyTypeObject PyStdPrinter_Type

   Kiểu của các đối tượng giống tệp được sử dụng nội bộ khi Python khởi động, lúc :py:mod:`io` chưa khả dụng. Thay vào đó, hãy sử dụng Python :py:func:`open` hoặc :c:func:`PyFile_FromFd` để tạo các đối tượng tệp.
