.. highlight:: c

.. index:: object; code, code object

.. _codeobjects:

Đối tượng mã
------------

.. sectionauthor:: Jeffrey Yasskin <jyasskin@gmail.com>

Đối tượng mã là một chi tiết cấp thấp trong triển khai CPython. Mỗi đối tượng biểu diễn một đoạn mã có thể thực thi nhưng chưa được liên kết với một hàm.

.. c:type:: PyCodeObject

   Cấu trúc C của các đối tượng được dùng để mô tả đối tượng mã. Các trường của kiểu này có thể thay đổi bất kỳ lúc nào.


.. c:var:: PyTypeObject PyCode_Type

   Đây là một thực thể của :c:type:`PyTypeObject` đại diện cho Python
   :ref:`đối tượng mã <code-objects>`.


.. c:function:: int PyCode_Check(PyObject *co)

   Trả về true nếu *co* là một :ref:`đối tượng mã <code-objects>`. Hàm này luôn thực hiện thành công.

.. c:function:: Py_ssize_t PyCode_GetNumFree(PyCodeObject *co)

   Trả về số lượng :term:`biến tự do (closure) <closure variable>` trong một đối tượng mã.

.. c:function:: int PyUnstable_Code_GetFirstFree(PyCodeObject *co)

   Trả về vị trí của :term:`biến free (closure) đầu tiên <closure variable>` trong một code object.

   .. versionchanged:: 3.13

      Được đổi tên từ ``PyCode_GetFirstFree`` như một phần của :ref:`unstable-c-api`. Tên cũ đã lỗi thời nhưng vẫn sẽ được cung cấp cho đến khi signature lại thay đổi.

.. c:function:: PyCodeObject* PyUnstable_Code_New(int argcount, int kwonlyargcount, int nlocals, int stacksize, int flags, PyObject *code, PyObject *consts, PyObject *names, PyObject *varnames, PyObject *freevars, PyObject *cellvars, PyObject *filename, PyObject *name, PyObject *qualname, int firstlineno, PyObject *linetable, PyObject *exceptiontable)

   Trả về một code object mới. Nếu bạn cần một code object giả để tạo frame, hãy dùng :c:func:`PyCode_NewEmpty` thay thế.

   Vì định nghĩa của bytecode thường xuyên thay đổi, việc gọi
   :c:func:`PyUnstable_Code_New` trực tiếp có thể khiến bạn phụ thuộc vào một phiên bản Python cụ thể.

   Nhiều đối số của hàm này phụ thuộc lẫn nhau theo những cách phức tạp, nghĩa là những thay đổi nhỏ đối với các giá trị có thể dẫn đến việc thực thi không chính xác hoặc VM bị lỗi. Chỉ sử dụng hàm này khi hết sức thận trọng.

   .. versionchanged:: 3.11
      Đã thêm các tham số ``qualname`` và ``exceptiontable``.

   .. index:: single: PyCode_New (C function)

   .. versionchanged:: 3.12

      Được đổi tên từ ``PyCode_New`` trong :ref:`unstable-c-api`. Tên cũ không còn được khuyến nghị, nhưng vẫn sẽ khả dụng cho đến khi signature lại thay đổi.

.. c:function:: PyCodeObject* PyCode_NewWithPosOnlyArgs(...)
   :no-typesetting:

.. c:function:: PyCodeObject* PyUnstable_Code_NewWithPosOnlyArgs(int argcount, int posonlyargcount, int kwonlyargcount, int nlocals, int stacksize, int flags, PyObject *code, PyObject *consts, PyObject *names, PyObject *varnames, PyObject *freevars, PyObject *cellvars, PyObject *filename, PyObject *name, PyObject *qualname, int firstlineno, PyObject *linetable, PyObject *exceptiontable)

   Tương tự :c:func:`PyUnstable_Code_New`, nhưng có thêm "posonlyargcount" cho các đối số positional-only. Các lưu ý áp dụng cho ``PyUnstable_Code_New`` cũng áp dụng cho hàm này.

   .. versionadded:: 3.8 như ``PyCode_NewWithPosOnlyArgs``

   .. versionchanged:: 3.11
      Đã thêm các tham số ``qualname`` và ``exceptiontable``.

   .. versionchanged:: 3.12

      Được đổi tên thành ``PyUnstable_Code_NewWithPosOnlyArgs``. Tên cũ không còn được khuyến nghị, nhưng vẫn sẽ khả dụng cho đến khi signature lại thay đổi.

.. c:function:: PyCodeObject* PyCode_NewEmpty(const char *filename, const char *funcname, int firstlineno)

   Trả về một code object trống mới với filename, tên hàm và số dòng đầu tiên được chỉ định. Code object thu được sẽ phát sinh ``Exception`` nếu được thực thi.

.. c:function:: int PyCode_Addr2Line(PyCodeObject *co, int byte_offset)

    Trả về số dòng của instruction xảy ra tại hoặc trước ``byte_offset`` và kết thúc sau đó. Nếu bạn chỉ cần số dòng của một frame, hãy dùng :c:func:`PyFrame_GetLineNumber` thay thế.

    Để lặp hiệu quả qua các số dòng trong một đối tượng code, hãy sử dụng :pep:`the API described in PEP 626 <0626#out-of-process-debuggers-and-profilers>`.

.. c:function:: int PyCode_Addr2Location(PyObject *co, int byte_offset, int *start_line, int *start_column, int *end_line, int *end_column)

   Đặt các con trỏ ``int`` được truyền vào thành số dòng và số cột trong mã nguồn tương ứng với instruction tại ``byte_offset``. Đặt giá trị thành ``0`` khi không có thông tin cho một phần tử cụ thể nào.

   Trả về ``1`` nếu hàm thành công và trả về 0 trong các trường hợp khác.

   .. versionadded:: 3.11

.. c:function:: PyObject* PyCode_GetCode(PyCodeObject *co)

   Tương đương với mã Python ``getattr(co, 'co_code')``. Trả về một strong reference đến :c:type:`PyBytesObject` đại diện cho bytecode trong một đối tượng code. Khi xảy ra lỗi, trả về ``NULL`` và phát sinh một exception.

   ``PyBytesObject`` này có thể được interpreter tạo theo yêu cầu và không nhất thiết đại diện cho bytecode thực sự được CPython thực thi. Trường hợp sử dụng chính của hàm này là cho debugger và profiler.

   .. versionadded:: 3.11

.. c:function:: PyObject* PyCode_GetVarnames(PyCodeObject *co)

   Tương đương với mã Python ``getattr(co, 'co_varnames')``. Trả về một reference mới đến :c:type:`PyTupleObject` chứa tên của các biến cục bộ. Khi xảy ra lỗi, trả về ``NULL`` và phát sinh một exception.

   .. versionadded:: 3.11

.. c:function:: PyObject* PyCode_GetCellvars(PyCodeObject *co)

   Tương đương với mã Python ``getattr(co, 'co_cellvars')``. Trả về một reference mới đến :c:type:`PyTupleObject` chứa tên của các biến cục bộ được các hàm lồng nhau tham chiếu. Khi xảy ra lỗi, trả về ``NULL`` và phát sinh một exception.

   .. versionadded:: 3.11

.. c:function:: PyObject* PyCode_GetFreevars(PyCodeObject *co)

   Tương đương với mã Python ``getattr(co, 'co_freevars')``. Trả về một tham chiếu mới đến một :c:type:`PyTupleObject` chứa tên của các biến :term:`free (closure) variables <closure variable>`. Khi có lỗi, ``NULL`` được trả về và một ngoại lệ được phát sinh.

   .. versionadded:: 3.11

.. c:function:: int PyCode_AddWatcher(PyCode_WatchCallback callback)

   Đăng ký *callback* làm watcher đối tượng mã cho interpreter hiện tại. Trả về một ID có thể được truyền vào :c:func:`PyCode_ClearWatcher`. Nếu xảy ra lỗi (ví dụ: không còn ID watcher nào khả dụng), trả về ``-1`` và đặt một ngoại lệ.

   .. versionadded:: 3.12

.. c:function:: int PyCode_ClearWatcher(int watcher_id)

   Xóa watcher được xác định bởi *watcher_id* đã được trả về trước đó từ
   :c:func:`PyCode_AddWatcher` cho interpreter hiện tại. Trả về ``0`` nếu thành công, hoặc ``-1`` và đặt một ngoại lệ nếu xảy ra lỗi (ví dụ: nếu *watcher_id* đã cho chưa từng được đăng ký.)

   .. versionadded:: 3.12

.. c:type:: PyCodeEvent

   Liệt kê các sự kiện watcher đối tượng mã có thể xảy ra:
   - ``PY_CODE_EVENT_CREATE``
   - ``PY_CODE_EVENT_DESTROY``

   .. versionadded:: 3.12

.. c:type:: int (*PyCode_WatchCallback)(PyCodeEvent event, PyCodeObject* co)

   Kiểu của hàm callback watcher đối tượng mã.

   Nếu *event* là ``PY_CODE_EVENT_CREATE``, callback được gọi sau khi *co* đã được khởi tạo hoàn chỉnh. Nếu không, callback được gọi trước khi quá trình hủy *co* diễn ra, để có thể kiểm tra trạng thái trước đó của *co*.

   Nếu *event* là ``PY_CODE_EVENT_DESTROY``, việc giữ một tham chiếu trong callback đến đối tượng mã sắp bị hủy sẽ làm đối tượng đó được phục hồi và ngăn không cho nó được giải phóng vào thời điểm này. Khi đối tượng được phục hồi bị hủy sau đó, mọi callback của watcher đang hoạt động tại thời điểm đó sẽ được gọi lại.

   Người dùng API này không nên phụ thuộc vào các chi tiết triển khai runtime nội bộ. Những chi tiết đó có thể bao gồm, nhưng không chỉ giới hạn ở, thứ tự và thời điểm chính xác tạo cũng như hủy các đối tượng mã. Mặc dù những thay đổi trong các chi tiết này có thể dẫn đến các khác biệt mà watcher quan sát được (bao gồm cả việc callback có được gọi hay không), chúng không làm thay đổi ngữ nghĩa của mã Python đang được thực thi.

   Nếu callback đặt một ngoại lệ, nó phải trả về ``-1``; ngoại lệ này sẽ được in dưới dạng ngoại lệ không thể phát (unraisable exception) bằng :c:func:`PyErr_WriteUnraisable`. Nếu không, callback nên trả về ``0``.

   Có thể đã có một ngoại lệ đang chờ được đặt khi bắt đầu callback. Trong trường hợp này, callback nên trả về ``0`` trong khi vẫn giữ nguyên ngoại lệ đó. Điều này có nghĩa là callback không được gọi bất kỳ API nào khác có thể đặt một ngoại lệ, trừ khi trước tiên nó lưu và xóa trạng thái ngoại lệ, rồi khôi phục trạng thái đó trước khi trả về.

   .. versionadded:: 3.12


.. c:function:: PyObject *PyCode_Optimize(PyObject *code, PyObject *consts, PyObject *names, PyObject *lnotab_obj)

   Đây là một hàm không thực hiện thao tác nào.

   Trước Python 3.10, hàm này sẽ thực hiện các tối ưu hóa cơ bản cho một đối tượng mã.

   .. versionchanged:: 3.10
      Hàm này hiện không thực hiện thao tác nào.

   .. soft-deprecated:: 3.13


.. _c_codeobject_flags:

Các cờ của đối tượng mã
-----------------------

Các đối tượng mã chứa một trường bit gồm các cờ, có thể được truy xuất dưới dạng
:attr:`~codeobject.co_flags` thuộc tính Python (ví dụ bằng cách sử dụng
:c:func:`PyObject_GetAttrString`), và được thiết lập bằng đối số *flags* cho
:c:func:`PyUnstable_Code_New` và các hàm tương tự.

Các cờ có tên bắt đầu bằng ``CO_FUTURE_`` tương ứng với những tính năng thường có thể chọn bằng các câu lệnh :ref:`future statements <future>`. Có thể sử dụng các cờ này trong
:c:member:`PyCompilerFlags.cf_flags`. Lưu ý rằng nhiều cờ ``CO_FUTURE_`` là bắt buộc trong các phiên bản Python hiện tại, nên việc thiết lập chúng không có tác dụng.

Các flag sau đây hiện có. Để biết ý nghĩa của chúng, hãy xem tài liệu được liên kết về các phiên bản tương đương trong Python.


.. list-table::
   :widths: auto
   :header-rows: 1

   * * Flag
     * Ý nghĩa
   * * .. c:macro:: CO_OPTIMIZED
     * :py:data:`inspect.CO_OPTIMIZED`
   * * .. c:macro:: CO_NEWLOCALS
     * :py:data:`inspect.CO_NEWLOCALS`
   * * .. c:macro:: CO_VARARGS
     * :py:data:`inspect.CO_VARARGS`
   * * .. c:macro:: CO_VARKEYWORDS
     * :py:data:`inspect.CO_VARKEYWORDS`
   * * .. c:macro:: CO_NESTED
     * :py:data:`inspect.CO_NESTED`
   * * .. c:macro:: CO_GENERATOR
     * :py:data:`inspect.CO_GENERATOR`
   * * .. c:macro:: CO_COROUTINE
     * :py:data:`inspect.CO_COROUTINE`
   * * .. c:macro:: CO_ITERABLE_COROUTINE
     * :py:data:`inspect.CO_ITERABLE_COROUTINE`
   * * .. c:macro:: CO_ASYNC_GENERATOR
     * :py:data:`inspect.CO_ASYNC_GENERATOR`
   * * .. c:macro:: CO_HAS_DOCSTRING
     * :py:data:`inspect.CO_HAS_DOCSTRING`
   * * .. c:macro:: CO_METHOD
     * :py:data:`inspect.CO_METHOD`

   * * .. c:macro:: CO_FUTURE_DIVISION
     * không có tác dụng (:py:data:`__future__.division`)
   * * .. c:macro:: CO_FUTURE_ABSOLUTE_IMPORT
     * không có tác dụng (:py:data:`__future__.absolute_import`)
   * * .. c:macro:: CO_FUTURE_WITH_STATEMENT
     * không có tác dụng (:py:data:`__future__.with_statement`)
   * * .. c:macro:: CO_FUTURE_PRINT_FUNCTION
     * không có tác dụng (:py:data:`__future__.print_function`)
   * * .. c:macro:: CO_FUTURE_UNICODE_LITERALS
     * không có tác dụng (:py:data:`__future__.unicode_literals`)
   * * .. c:macro:: CO_FUTURE_GENERATOR_STOP
     * không có tác dụng (:py:data:`__future__.generator_stop`)
   * * .. c:macro:: CO_FUTURE_ANNOTATIONS
     * :py:data:`__future__.annotations`


Thông tin bổ sung
-----------------

Để hỗ trợ các phần mở rộng cấp thấp cho việc đánh giá frame, chẳng hạn như các trình biên dịch just-in-time bên ngoài, bạn có thể đính kèm dữ liệu tùy ý vào các code object.

Các hàm này thuộc tầng C API không ổn định: chức năng này là một chi tiết triển khai của CPython và API có thể thay đổi mà không có cảnh báo ngừng hỗ trợ.

.. c:function:: Py_ssize_t _PyEval_RequestCodeExtraIndex(freefunc free)
   :no-typesetting:

.. c:function:: Py_ssize_t PyUnstable_Eval_RequestCodeExtraIndex(freefunc free)

   Trả về một giá trị chỉ mục opaque mới được dùng để thêm dữ liệu vào các code object.

   Thông thường, bạn gọi hàm này một lần (cho mỗi interpreter) rồi sử dụng kết quả cùng với ``PyCode_GetExtra`` và ``PyCode_SetExtra`` để thao tác với dữ liệu trên từng code object.

   Nếu *free* không phải là ``NULL``: khi một đối tượng mã được giải phóng, *free* sẽ được gọi trên dữ liệu không phải ``NULL`` được lưu dưới chỉ mục mới. Sử dụng :c:func:`Py_DecRef` khi lưu trữ :c:type:`PyObject`.

   .. versionadded:: 3.6 kể từ ``_PyEval_RequestCodeExtraIndex``

   .. versionchanged:: 3.12

     Được đổi tên thành ``PyUnstable_Eval_RequestCodeExtraIndex``. Tên riêng tư cũ đã lỗi thời nhưng sẽ vẫn khả dụng cho đến khi API thay đổi.

.. c:function:: int _PyCode_GetExtra(PyObject *code, Py_ssize_t index, void **extra)
   :no-typesetting:

.. c:function:: int PyUnstable_Code_GetExtra(PyObject *code, Py_ssize_t index, void **extra)

   Đặt *extra* thành dữ liệu bổ sung được lưu dưới chỉ mục đã cho. Trả về 0 nếu thành công. Đặt một ngoại lệ và trả về -1 nếu thất bại.

   Nếu không có dữ liệu nào được đặt dưới chỉ mục, đặt *extra* thành ``NULL`` và trả về 0 mà không đặt ngoại lệ.

   .. versionadded:: 3.6 kể từ ``_PyCode_GetExtra``

   .. versionchanged:: 3.12

     Được đổi tên thành ``PyUnstable_Code_GetExtra``. Tên riêng tư cũ đã lỗi thời nhưng sẽ vẫn khả dụng cho đến khi API thay đổi.

.. c:function:: int _PyCode_SetExtra(PyObject *code, Py_ssize_t index, void *extra)
   :no-typesetting:

.. c:function:: int PyUnstable_Code_SetExtra(PyObject *code, Py_ssize_t index, void *extra)

   Đặt dữ liệu bổ sung được lưu dưới chỉ mục đã cho thành *extra*. Trả về 0 nếu thành công. Đặt một exception và trả về -1 nếu thất bại.

   .. versionadded:: 3.6 thành ``_PyCode_SetExtra``

   .. versionchanged:: 3.12

     Được đổi tên thành ``PyUnstable_Code_SetExtra``. Tên private cũ đã deprecated nhưng sẽ vẫn khả dụng cho đến khi API thay đổi.
