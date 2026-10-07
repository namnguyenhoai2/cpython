.. highlight:: c

Đối tượng frame
---------------

.. c:type:: PyFrameObject

   Cấu trúc C của các đối tượng được dùng để mô tả đối tượng frame.

   Cấu trúc này không có thành viên công khai.

   .. versionchanged:: 3.11
      Các thành viên của cấu trúc này đã bị xóa khỏi public C API. Hãy tham khảo mục :ref:`What's New entry <pyframeobject-3.11-hiding>` để biết chi tiết.

Có thể sử dụng các hàm :c:func:`PyEval_GetFrame` và :c:func:`PyThreadState_GetFrame` để lấy một đối tượng frame.

Xem thêm :ref:`Reflection <reflection>`.

.. c:var:: PyTypeObject PyFrame_Type

   Kiểu của các đối tượng frame. Đây là cùng một đối tượng với :py:class:`types.FrameType` trong lớp Python.

   .. versionchanged:: 3.11

      Trước đây, kiểu này chỉ khả dụng sau khi đưa vào ``<frameobject.h>``.

.. c:function:: PyFrameObject *PyFrame_New(PyThreadState *tstate, PyCodeObject *code, PyObject *globals, PyObject *locals)

   Tạo một đối tượng frame mới. Khi thành công, hàm này trả về một :term:`strong reference` trỏ tới đối tượng frame mới và khi thất bại, trả về ``NULL`` cùng với một ngoại lệ đã được thiết lập.

.. c:function:: int PyFrame_Check(PyObject *obj)

   Trả về giá trị khác 0 nếu *obj* là một đối tượng frame.

   .. versionchanged:: 3.11

      Trước đây, hàm này chỉ khả dụng sau khi đưa vào ``<frameobject.h>``.

.. c:function:: PyFrameObject* PyFrame_GetBack(PyFrameObject *frame)

   Lấy frame bên ngoài tiếp theo của *frame*.

   Trả về :term:`strong reference`, hoặc ``NULL`` nếu *frame* không có frame bên ngoài. Hàm này không phát sinh ngoại lệ.

   .. versionadded:: 3.9


.. c:function:: PyObject* PyFrame_GetBuiltins(PyFrameObject *frame)

   Lấy *khung* :attr:`~frame.f_builtins` thuộc tính.

   Trả về một :term:`strong reference`. Kết quả không thể là ``NULL``.

   .. versionadded:: 3.11


.. c:function:: PyCodeObject* PyFrame_GetCode(PyFrameObject *frame)

   Lấy mã *frame*.

   Trả về một :term:`strong reference`.

   Kết quả (mã frame) không thể là ``NULL``.

   .. versionadded:: 3.9


.. c:function:: PyObject* PyFrame_GetGenerator(PyFrameObject *frame)

   Lấy generator, coroutine hoặc async generator sở hữu frame này, hoặc ``NULL`` nếu frame này không thuộc về generator nào. Không phát sinh ngoại lệ, ngay cả khi giá trị trả về là ``NULL``.

   Trả về một :term:`strong reference`, hoặc ``NULL``.

   .. versionadded:: 3.11


.. c:function:: PyObject* PyFrame_GetGlobals(PyFrameObject *frame)

   Lấy thuộc tính :attr:`~frame.f_globals` của *frame*.

   Trả về một :term:`strong reference`. Kết quả không thể là ``NULL``.

   .. versionadded:: 3.11


.. c:function:: int PyFrame_GetLasti(PyFrameObject *frame)

   Lấy *khung* của :attr:`~frame.f_lasti` thuộc tính.

   Trả về -1 nếu ``frame.f_lasti`` là ``None``.

   .. versionadded:: 3.11


.. c:function:: PyObject* PyFrame_GetVar(PyFrameObject *frame, PyObject *name)

   Lấy biến *name* của *frame*.

   * Trả về một :term:`strong reference` đến giá trị biến khi thành công.
   * Phát sinh :exc:`NameError` và trả về ``NULL`` nếu biến không tồn tại.
   * Phát sinh một ngoại lệ và trả về ``NULL`` khi xảy ra lỗi.

   Kiểu *name* phải là một :class:`str`.

   .. versionadded:: 3.12


.. c:function:: PyObject* PyFrame_GetVarString(PyFrameObject *frame, const char *name)

   Tương tự như :c:func:`PyFrame_GetVar`, nhưng tên biến là một chuỗi C được mã hóa bằng UTF-8.

   .. versionadded:: 3.12


.. c:function:: PyObject* PyFrame_GetLocals(PyFrameObject *frame)

   Lấy thuộc tính :attr:`~frame.f_locals` của *frame*. Nếu frame tham chiếu đến một :term:`optimized scope`, thao tác này trả về một đối tượng proxy cho phép ghi xuyên để sửa đổi các biến cục bộ. Trong mọi trường hợp khác (class, module, :func:`exec`, :func:`eval`), thao tác này trả về trực tiếp mapping biểu diễn các biến cục bộ của frame (như được mô tả cho
   :func:`locals`).

   Trả về một :term:`strong reference`.

   .. versionadded:: 3.11

   .. versionchanged:: 3.13
      Là một phần của :pep:`667`, trả về một instance của :c:var:`PyFrameLocalsProxy_Type`.


.. c:function:: int PyFrame_GetLineNumber(PyFrameObject *frame)

   Trả về số dòng mà *frame* hiện đang thực thi.


Proxy biến cục bộ của frame
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. versionadded:: 3.13

Thuộc tính :attr:`~frame.f_locals` trên một :ref:`đối tượng frame <frame-objects>` là một instance của “frame-locals proxy”. Đối tượng proxy cung cấp chế độ xem cho phép ghi xuyên vào từ điển locals bên dưới của frame. Điều này đảm bảo các biến được ``f_locals`` cung cấp luôn được cập nhật theo các biến cục bộ đang hoạt động trong chính frame.

Xem :pep:`667` để biết thêm thông tin.

.. c:var:: PyTypeObject PyFrameLocalsProxy_Type

   Kiểu của các đối tượng proxy :func:`locals` thuộc frame.

.. c:function:: int PyFrameLocalsProxy_Check(PyObject *obj)

   Trả về giá trị khác 0 nếu *obj* là proxy :func:`locals` của frame.


API biến cục bộ kiểu cũ
^^^^^^^^^^^^^^^^^^^^^^^

Các API này đã :term:`soft deprecated`. Kể từ Python 3.13, chúng không thực hiện thao tác nào. Chúng chỉ tồn tại để đảm bảo khả năng tương thích ngược.


.. c:function:: void PyFrame_LocalsToFast(PyFrameObject *f, int clear)

   Trước Python 3.13, hàm này sẽ sao chép thuộc tính :attr:`~frame.f_locals` của *f* vào mảng “nhanh” nội bộ của các biến cục bộ, cho phép các thay đổi trong đối tượng frame được trình thông dịch nhìn thấy. Nếu *clear* có giá trị true, hàm này sẽ xử lý các biến chưa được thiết lập trong từ điển locals.

   .. soft-deprecated:: 3.13
      Hàm này hiện không làm gì cả.


.. c:function:: void PyFrame_FastToLocals(PyFrameObject *f)

   Trước Python 3.13, hàm này sẽ sao chép mảng biến cục bộ "fast" nội bộ (được interpreter sử dụng) vào
   thuộc tính :attr:`~frame.f_locals` của *f*, cho phép các thay đổi trong biến cục bộ hiển thị trong các đối tượng frame.

   .. soft-deprecated:: 3.13
      Hàm này hiện không làm gì cả.


.. c:function:: int PyFrame_FastToLocalsWithError(PyFrameObject *f)

   Trước Python 3.13, hàm này tương tự như
   :c:func:`PyFrame_FastToLocals`, nhưng sẽ trả về ``0`` khi thành công và ``-1`` khi thất bại với một exception đã được thiết lập.

   .. soft-deprecated:: 3.13
      Hàm này hiện không làm gì cả.


.. seealso::
   :pep:`667`


Các frame nội bộ
^^^^^^^^^^^^^^^^

Trừ khi sử dụng :pep:`523`, bạn sẽ không cần đến phần này.

.. c:struct:: _PyInterpreterFrame

   Biểu diễn frame nội bộ của interpreter.

   .. versionadded:: 3.11

.. c:function:: PyObject* PyUnstable_InterpreterFrame_GetCode(struct _PyInterpreterFrame *frame);

    Trả về một :term:`strong reference` tới code object của frame.

   .. versionadded:: 3.12


.. c:function:: int PyUnstable_InterpreterFrame_GetLasti(struct _PyInterpreterFrame *frame);

   Trả về độ lệch byte tới instruction được thực thi gần nhất.

   .. versionadded:: 3.12


.. c:function:: int PyUnstable_InterpreterFrame_GetLine(struct _PyInterpreterFrame *frame);

   Trả về số dòng hiện đang được thực thi hoặc -1 nếu không có số dòng.

   .. versionadded:: 3.12


.. c:var:: const PyTypeObject *PyUnstable_ExecutableKinds

   Một mảng các loại có thể thực thi (executor type) cho các frame, được dùng để debug và tracing nội bộ.

   Các công cụ như trình gỡ lỗi và trình phân tích hiệu năng có thể sử dụng thông tin này để xác định loại ngữ cảnh thực thi liên kết với một frame (chẳng hạn để lọc các frame nội bộ). Các mục được lập chỉ mục bằng các hằng số sau:

   .. list-table::
      :header-rows: 1
      :widths: auto

      * - Hằng số
        - Mô tả
      * - .. c:macro:: PyUnstable_EXECUTABLE_KIND_SKIP
        - Frame là frame nội bộ (ví dụ: được inline) và các công cụ nên bỏ qua frame này.
      * - .. c:macro:: PyUnstable_EXECUTABLE_KIND_PY_FUNCTION
        - Frame tương ứng với một hàm Python tiêu chuẩn.
      * - .. c:macro:: PyUnstable_EXECUTABLE_KIND_BUILTIN_FUNCTION
        - Frame tương ứng với một hàm được định nghĩa trong mã native.
      * - .. c:macro:: PyUnstable_EXECUTABLE_KIND_METHOD_DESCRIPTOR
        - Frame tương ứng với một phương thức trên một thực thể lớp.

   Lưu ý rằng hiện tại chỉ có thể đọc loại executable từ một frame bằng các API nội bộ chưa được công bố.

   .. versionadded:: 3.13


.. c:macro:: PyUnstable_EXECUTABLE_KINDS

   Số lượng mục trong :c:data:`PyUnstable_ExecutableKinds`.

   .. versionadded:: 3.13

