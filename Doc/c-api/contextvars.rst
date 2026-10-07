.. highlight:: c

.. _contextvarsobjects:

Đối tượng biến ngữ cảnh
-----------------------

.. _contextvarsobjects_pointertype_change:
.. versionadded:: 3.7

.. versionchanged:: 3.7.1

   .. note::

      Trong Python 3.7.1, chữ ký của tất cả các API C cho biến ngữ cảnh đã được **thay đổi** để sử dụng :c:type:`PyObject` các con trỏ thay vì :c:type:`PyContext`, :c:type:`PyContextVar`, và
      :c:type:`PyContextToken`, ví dụ.::

         // in 3.7.0:
         PyContext *PyContext_New(void);

         // in 3.7.1+:
         PyObject *PyContext_New(void);

      Xem :issue:`34762` để biết thêm chi tiết.


Phần này trình bày chi tiết API C công khai cho module :mod:`contextvars`.

.. c:type:: PyContext

   Cấu trúc C được sử dụng để biểu diễn một đối tượng :class:`contextvars.Context`.

.. c:type:: PyContextVar

   Cấu trúc C được sử dụng để biểu diễn một đối tượng :class:`contextvars.ContextVar`.

.. c:type:: PyContextToken

   Cấu trúc C được dùng để biểu diễn một đối tượng :class:`contextvars.Token`.

.. c:var:: PyTypeObject PyContext_Type

   Đối tượng kiểu biểu diễn kiểu *context*.

.. c:var:: PyTypeObject PyContextVar_Type

   Đối tượng kiểu biểu diễn kiểu *context variable*.

.. c:var:: PyTypeObject PyContextToken_Type

   Đối tượng kiểu biểu diễn kiểu *context variable token*.


Các macro kiểm tra kiểu:

.. c:function:: int PyContext_CheckExact(PyObject *o)

   Trả về true nếu *o* thuộc kiểu :c:data:`PyContext_Type`. *o* không được là ``NULL``. Hàm này luôn thành công.

.. c:function:: int PyContextVar_CheckExact(PyObject *o)

   Trả về true nếu *o* thuộc kiểu :c:data:`PyContextVar_Type`. *o* không được là ``NULL``. Hàm này luôn thành công.

.. c:function:: int PyContextToken_CheckExact(PyObject *o)

   Trả về true nếu *o* thuộc kiểu :c:data:`PyContextToken_Type`. *o* không được là ``NULL``. Hàm này luôn thực hiện thành công.


Các hàm quản lý đối tượng context:

.. c:function:: PyObject *PyContext_New(void)

   Tạo một đối tượng context trống mới. Trả về ``NULL`` nếu đã xảy ra lỗi.

.. c:function:: PyObject *PyContext_Copy(PyObject *ctx)

   Tạo một bản sao nông của đối tượng context *ctx* được truyền vào. Trả về ``NULL`` nếu đã xảy ra lỗi.

.. c:function:: PyObject *PyContext_CopyCurrent(void)

   Tạo một bản sao nông của context của thread hiện tại. Trả về ``NULL`` nếu đã xảy ra lỗi.

.. c:function:: int PyContext_Enter(PyObject *ctx)

   Đặt *ctx* làm context hiện tại cho thread hiện tại. Trả về ``0`` khi thành công và ``-1`` khi xảy ra lỗi.

.. c:function:: int PyContext_Exit(PyObject *ctx)

   Vô hiệu hóa context *ctx* và khôi phục context trước đó làm context hiện tại cho thread hiện tại. Trả về ``0`` khi thành công và ``-1`` khi xảy ra lỗi.

.. c:function:: int PyContext_AddWatcher(PyContext_WatchCallback callback)

   Đăng ký *callback* làm trình theo dõi đối tượng context cho interpreter hiện tại. Trả về một ID có thể được truyền vào :c:func:`PyContext_ClearWatcher`. Nếu xảy ra lỗi (ví dụ: không còn ID trình theo dõi nào khả dụng), trả về ``-1`` và đặt một exception.

   .. versionadded:: 3.14

.. c:function:: int PyContext_ClearWatcher(int watcher_id)

   Xóa trình theo dõi được xác định bởi *watcher_id* trước đó được trả về từ
   :c:func:`PyContext_AddWatcher` cho interpreter hiện tại. Trả về ``0`` nếu thành công hoặc ``-1`` và đặt một exception nếu xảy ra lỗi (ví dụ: nếu *watcher_id* đã cho chưa từng được đăng ký).

   .. versionadded:: 3.14

.. c:type:: PyContextEvent

   Liệt kê các sự kiện có thể xảy ra đối với trình theo dõi đối tượng context:

   - ``Py_CONTEXT_SWITCHED``: :term:`current context` đã chuyển sang một context khác. Đối tượng được truyền vào watch callback là đối tượng :class:`contextvars.Context` hiện tại hoặc None nếu hiện không có context nào.

   .. versionadded:: 3.14

.. c:type:: int (*PyContext_WatchCallback)(PyContextEvent event, PyObject *obj)

   Hàm callback của trình theo dõi đối tượng context. Đối tượng được truyền vào callback phụ thuộc vào sự kiện; xem :c:type:`PyContextEvent` để biết chi tiết.

   Nếu callback kết thúc khi một exception đang được đặt, nó phải trả về ``-1``; exception này sẽ được in dưới dạng unraisable exception bằng cách sử dụng
   :c:func:`PyErr_FormatUnraisable`. Nếu không, nó sẽ trả về ``0``.

   Có thể đã có một exception đang chờ được thiết lập khi callback được gọi. Trong trường hợp này, callback phải trả về ``0`` và vẫn giữ nguyên exception đó. Điều này có nghĩa là callback không được gọi bất kỳ API nào khác có thể thiết lập exception, trừ khi trước tiên lưu và xóa trạng thái exception, rồi khôi phục trạng thái đó trước khi trả về.

   .. versionadded:: 3.14


Các hàm biến ngữ cảnh:

.. c:function:: PyObject *PyContextVar_New(const char *name, PyObject *def)

   Tạo một đối tượng ``ContextVar`` mới. Tham số *name* được dùng cho mục đích introspection và debug. Tham số *def* chỉ định giá trị mặc định cho biến ngữ cảnh, hoặc ``NULL`` nếu không có giá trị mặc định. Nếu đã xảy ra lỗi, hàm này trả về ``NULL``.

.. c:function:: int PyContextVar_Get(PyObject *var, PyObject *default_value, PyObject **value)

   Lấy giá trị của một biến ngữ cảnh. Trả về ``-1`` nếu xảy ra lỗi trong quá trình tra cứu và ``0`` nếu không xảy ra lỗi, bất kể có tìm thấy giá trị hay không.

   Nếu tìm thấy biến context, *giá trị* sẽ là một con trỏ trỏ đến biến đó. Nếu không tìm thấy biến context, *không* *giá trị* sẽ trỏ đến:

   - *default_value*, nếu không phải ``NULL``;
   - giá trị mặc định của *var*, nếu không ``NULL``;
   - ``NULL``

   Ngoại trừ ``NULL``, hàm trả về một tham chiếu mới.

.. c:function:: PyObject *PyContextVar_Set(PyObject *var, PyObject *value)

   Đặt giá trị của *var* thành *value* trong context hiện tại. Trả về một đối tượng token mới cho thay đổi này hoặc ``NULL`` nếu đã xảy ra lỗi.

.. c:function:: int PyContextVar_Reset(PyObject *var, PyObject *token)

   Đặt lại trạng thái của biến ngữ cảnh *var* về trạng thái trước đó
   :c:func:`PyContextVar_Set` đã trả về *token* được gọi. Hàm này trả về ``0`` khi thành công và ``-1`` khi xảy ra lỗi.
