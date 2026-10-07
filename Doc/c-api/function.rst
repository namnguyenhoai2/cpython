.. highlight:: c

.. _function-objects:

Đối tượng hàm
-------------

.. index:: pair: object; function

Có một vài hàm dành riêng cho các hàm Python.


.. c:type:: PyFunctionObject

   Cấu trúc C được sử dụng cho các hàm.


.. c:var:: PyTypeObject PyFunction_Type

   .. index:: single: MethodType (in module types)

   Đây là một thực thể của :c:type:`PyTypeObject` và đại diện cho kiểu hàm Python. Nó được cung cấp cho lập trình viên Python dưới dạng ``types.FunctionType``.


.. c:function:: int PyFunction_Check(PyObject *o)

   Trả về true nếu *o* là một đối tượng hàm (có kiểu :c:data:`PyFunction_Type`). Tham số này không được là ``NULL``. Hàm này luôn thực hiện thành công.


.. c:function:: PyObject* PyFunction_New(PyObject *code, PyObject *globals)

   Trả về một đối tượng hàm mới được liên kết với đối tượng mã *code*. *globals* phải là một dictionary chứa các biến toàn cục mà hàm có thể truy cập.

   Docstring và tên của hàm được lấy từ đối tượng mã.
   :attr:`~function.__module__` được lấy từ *globals*. Các giá trị mặc định của đối số, chú thích và closure được đặt thành ``NULL``. :attr:`~function.__qualname__` được đặt thành cùng giá trị với trường :attr:`~codeobject.co_qualname` của code object.


.. c:function:: PyObject* PyFunction_NewWithQualName(PyObject *code, PyObject *globals, PyObject *qualname)

   Tương tự như :c:func:`PyFunction_New`, nhưng cũng cho phép thiết lập
   thuộc tính :attr:`~function.__qualname__`. *qualname* phải là một đối tượng unicode hoặc ``NULL``; nếu là ``NULL``, thuộc tính :attr:`!__qualname__` được đặt thành cùng giá trị với trường :attr:`~codeobject.co_qualname` của code object.

   .. versionadded:: 3.3


.. c:function:: PyObject* PyFunction_GetCode(PyObject *op)

   Trả về code object liên kết với function object *op*.


.. c:function:: PyObject* PyFunction_GetGlobals(PyObject *op)

   Trả về dictionary globals liên kết với function object *op*.


.. c:function:: PyObject* PyFunction_GetModule(PyObject *op)

   Trả về một :term:`borrowed reference` tới thuộc tính :attr:`~function.__module__` của :ref:`function object <user-defined-funcs>` *op*. Giá trị này có thể là *NULL*.

   Đây thường là một :class:`string <str>` chứa tên module, nhưng mã Python có thể đặt nó thành bất kỳ đối tượng nào khác.


.. c:function:: PyObject* PyFunction_GetDefaults(PyObject *op)

   Trả về các giá trị mặc định của đối số của đối tượng hàm *op*. Giá trị này có thể là một tuple các đối số hoặc ``NULL``.


.. c:function:: int PyFunction_SetDefaults(PyObject *op, PyObject *defaults)

   Đặt các giá trị mặc định của đối số cho đối tượng hàm *op*. *defaults* phải là ``Py_None`` hoặc một tuple.

   Phát sinh :exc:`SystemError` và trả về ``-1`` khi thất bại.


.. c:function:: void PyFunction_SetVectorcall(PyFunctionObject *func, vectorcallfunc vectorcall)

   Đặt trường vectorcall của đối tượng hàm đã cho *func*.

   Cảnh báo: các extension sử dụng API này phải duy trì hành vi của hàm vectorcall chưa được thay đổi (mặc định)!

   .. versionadded:: 3.12


.. c:function:: PyObject* PyFunction_GetKwDefaults(PyObject *op)

   Trả về các giá trị mặc định của đối số chỉ từ khóa của đối tượng hàm *op*. Giá trị này có thể là một dictionary các đối số hoặc ``NULL``.


.. c:function:: int PyFunction_SetKwDefaults(PyObject *op, PyObject *defaults)

   Đặt các giá trị mặc định của đối số chỉ từ khóa cho đối tượng hàm *op*. *defaults* phải là một dictionary của các đối số chỉ từ khóa hoặc ``Py_None``.

   Hàm này trả về ``0`` khi thành công và trả về ``-1`` khi thất bại, đồng thời đặt một exception.


.. c:function:: PyObject* PyFunction_GetClosure(PyObject *op)

   Trả về closure liên kết với function object *op*. Giá trị này có thể là ``NULL`` hoặc một tuple gồm các cell object.


.. c:function:: int PyFunction_SetClosure(PyObject *op, PyObject *closure)

   Đặt closure liên kết với function object *op*. *closure* phải là ``Py_None`` hoặc một tuple gồm các cell object.

   Phát sinh :exc:`SystemError` và trả về ``-1`` khi thất bại.


.. c:function:: PyObject *PyFunction_GetAnnotations(PyObject *op)

   Trả về các annotation của function object *op*. Giá trị này có thể là một dictionary có thể thay đổi hoặc ``NULL``.


.. c:function:: int PyFunction_SetAnnotations(PyObject *op, PyObject *annotations)

   Đặt các annotation cho function object *op*. *annotations* phải là một dictionary hoặc ``Py_None``.

   Phát sinh :exc:`SystemError` và trả về ``-1`` khi thất bại.


.. c:function:: PyObject *PyFunction_GET_CODE(PyObject *op)
                PyObject *PyFunction_GET_GLOBALS(PyObject *op) PyObject *PyFunction_GET_MODULE(PyObject *op) PyObject *PyFunction_GET_DEFAULTS(PyObject *op) PyObject *PyFunction_GET_KW_DEFAULTS(PyObject *op) PyObject *PyFunction_GET_CLOSURE(PyObject *op) PyObject *PyFunction_GET_ANNOTATIONS(PyObject *op)

   Các hàm này tương tự như các hàm tương ứng ``PyFunction_Get*``, nhưng không thực hiện kiểm tra kiểu. Việc truyền bất kỳ đối tượng nào khác ngoài một thể hiện của
   :c:data:`PyFunction_Type` là hành vi không được xác định.


.. c:function:: int PyFunction_AddWatcher(PyFunction_WatchCallback callback)

   Đăng ký *callback* làm function watcher cho interpreter hiện tại. Trả về một ID có thể được truyền cho :c:func:`PyFunction_ClearWatcher`. Trong trường hợp xảy ra lỗi (ví dụ: không còn ID watcher), trả về ``-1`` và đặt một exception.

   .. versionadded:: 3.12


.. c:function:: int PyFunction_ClearWatcher(int watcher_id)

   Xóa watcher được xác định bởi *watcher_id* đã được trả về từ
   :c:func:`PyFunction_AddWatcher` cho interpreter hiện tại. Trả về ``0`` nếu thành công, hoặc ``-1`` và đặt một exception nếu xảy ra lỗi (ví dụ: nếu *watcher_id* đã cho chưa từng được đăng ký.)

   .. versionadded:: 3.12


.. c:type:: PyFunction_WatchEvent

    Các sự kiện function watcher có thể xảy ra:

    - ``PyFunction_EVENT_CREATE``
    - ``PyFunction_EVENT_DESTROY``
    - ``PyFunction_EVENT_MODIFY_CODE``
    - ``PyFunction_EVENT_MODIFY_DEFAULTS``
    - ``PyFunction_EVENT_MODIFY_KWDEFAULTS``

   .. versionadded:: 3.12


.. c:type:: int (*PyFunction_WatchCallback)(PyFunction_WatchEvent event, PyFunctionObject *func, PyObject *new_value)

   Kiểu của hàm callback theo dõi hàm.

   Nếu *event* là ``PyFunction_EVENT_CREATE`` hoặc ``PyFunction_EVENT_DESTROY`` thì *new_value* sẽ là ``NULL``. Nếu không, *new_value* sẽ chứa một
   :term:`borrowed reference` đến giá trị mới sắp được lưu vào *func* cho thuộc tính đang được sửa đổi.

   Callback có thể kiểm tra nhưng không được sửa đổi *func*; việc đó có thể gây ra các hiệu ứng không thể dự đoán, bao gồm cả đệ quy vô hạn.

   Nếu *event* là ``PyFunction_EVENT_CREATE``, callback được gọi sau khi *func* đã được khởi tạo hoàn toàn. Nếu không, callback được gọi trước khi việc sửa đổi *func* diễn ra, nên có thể kiểm tra trạng thái trước đó của *func*. Runtime được phép tối ưu hóa để loại bỏ việc tạo các đối tượng hàm khi có thể. Trong những trường hợp đó, không có event nào được phát ra. Mặc dù điều này tạo ra khả năng hành vi runtime có thể quan sát được sẽ khác nhau tùy thuộc vào các quyết định tối ưu hóa, nó không làm thay đổi ngữ nghĩa của mã Python đang được thực thi.

   Nếu *event* là ``PyFunction_EVENT_DESTROY``, việc lấy một tham chiếu trong callback đến hàm sắp bị hủy sẽ hồi sinh hàm đó, ngăn không cho nó được giải phóng vào thời điểm này. Khi đối tượng đã được hồi sinh bị hủy sau đó, mọi callback theo dõi đang hoạt động tại thời điểm đó sẽ được gọi lại.

   Nếu callback đặt một exception, nó phải trả về ``-1``; exception này sẽ được in dưới dạng exception không thể báo cáo bằng :c:func:`PyErr_WriteUnraisable`. Nếu không, nó nên trả về ``0``.

   Có thể đã có một ngoại lệ đang chờ được đặt trước khi callback được gọi. Trong trường hợp này, callback phải trả về ``0`` với cùng ngoại lệ đó vẫn được đặt. Điều này có nghĩa là callback không được gọi bất kỳ API nào khác có thể đặt ngoại lệ, trừ khi trước tiên lưu và xóa trạng thái ngoại lệ, rồi khôi phục trạng thái đó trước khi trả về.

   .. versionadded:: 3.12
