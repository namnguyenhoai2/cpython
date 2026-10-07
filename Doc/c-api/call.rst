.. highlight:: c

.. _call:

Giao thức gọi
=============

CPython hỗ trợ hai giao thức gọi khác nhau: *tp_call* và vectorcall.

Giao thức *tp_call*
-------------------

Các instance của những class thiết lập :c:member:`~PyTypeObject.tp_call` có thể được gọi. Chữ ký của slot là::

    PyObject *tp_call(PyObject *callable, PyObject *args, PyObject *kwargs);

Một lệnh gọi được thực hiện bằng cách sử dụng một tuple cho các đối số vị trí và một dict cho các đối số từ khóa, tương tự như ``callable(*args, **kwargs)`` trong mã Python. *args* phải khác NULL (sử dụng một tuple rỗng nếu không có đối số nào), nhưng *kwargs* có thể là *NULL* nếu không có đối số từ khóa.

Quy ước này không chỉ được sử dụng bởi *tp_call*:
:c:member:`~PyTypeObject.tp_new` và :c:member:`~PyTypeObject.tp_init` cũng truyền các đối số theo cách này.

Để gọi một đối tượng, hãy sử dụng :c:func:`PyObject_Call` hoặc một
:ref:`API gọi <capi-call>`.


.. _vectorcall:

Giao thức Vectorcall
--------------------

.. versionadded:: 3.9

Giao thức vectorcall được giới thiệu trong :pep:`590` như một giao thức bổ sung để thực hiện các lệnh gọi hiệu quả hơn.

Theo nguyên tắc kinh nghiệm, CPython sẽ ưu tiên vectorcall cho các lệnh gọi nội bộ nếu đối tượng có thể gọi hỗ trợ nó. Tuy nhiên, đây không phải là quy tắc bắt buộc. Ngoài ra, một số extension bên thứ ba sử dụng *tp_call* trực tiếp (thay vì sử dụng :c:func:`PyObject_Call`). Vì vậy, một class hỗ trợ vectorcall cũng phải triển khai
:c:member:`~PyTypeObject.tp_call`. Hơn nữa, đối tượng có thể gọi phải hoạt động giống nhau bất kể sử dụng giao thức nào. Cách được khuyến nghị để đạt được điều này là đặt
:c:member:`~PyTypeObject.tp_call` thành :c:func:`PyVectorcall_Call`. Cần nhắc lại điều này:

.. warning::

   Một class hỗ trợ vectorcall **phải** đồng thời triển khai
   :c:member:`~PyTypeObject.tp_call` với cùng ngữ nghĩa.

.. versionchanged:: 3.12

   Cờ :c:macro:`Py_TPFLAGS_HAVE_VECTORCALL` hiện bị xóa khỏi một class khi phương thức :py:meth:`~object.__call__` của class được gán lại. (Về nội bộ, thao tác này chỉ đặt :c:member:`~PyTypeObject.tp_call`, vì vậy nó có thể hoạt động khác với hàm vectorcall.) Trong các phiên bản Python trước đây, chỉ nên sử dụng vectorcall với
   :c:macro:`bất biến <Py_TPFLAGS_IMMUTABLETYPE>` hoặc các kiểu static.

Một class không nên triển khai vectorcall nếu việc đó chậm hơn *tp_call*. Ví dụ: nếu callee dù sao cũng cần chuyển các đối số thành một args tuple và kwargs dict, thì việc triển khai vectorcall là không cần thiết.

Các class có thể triển khai giao thức vectorcall bằng cách bật
:c:macro:`Py_TPFLAGS_HAVE_VECTORCALL` cờ và thiết lập
:c:member:`~PyTypeObject.tp_vectorcall_offset` đến offset bên trong cấu trúc đối tượng, nơi *vectorcallfunc* xuất hiện. Đây là một con trỏ đến một hàm có chữ ký sau:

.. c:type:: PyObject *(*vectorcallfunc)(PyObject *callable, PyObject *const *args, size_t nargsf, PyObject *kwnames)

- *callable* là đối tượng đang được gọi.
- *args* là một mảng C gồm các đối số vị trí, theo sau là
   các giá trị của các đối số từ khóa. Giá trị này có thể là *NULL* nếu không có đối số nào.
- *nargsf* là số lượng đối số vị trí, cộng thêm có thể là
   cờ :c:macro:`PY_VECTORCALL_ARGUMENTS_OFFSET`. Để lấy số lượng đối số vị trí thực tế từ *nargsf*, hãy sử dụng :c:func:`PyVectorcall_NARGS`.
- *kwnames* là một tuple chứa tên của các đối số từ khóa;
   Nói cách khác, đó là các khóa của dict kwargs. Các tên này phải là chuỗi (các instance của ``str`` hoặc lớp con của nó) và phải là duy nhất. Nếu không có đối số từ khóa nào, thì *kwnames* có thể thay bằng *NULL*.

.. c:macro:: PY_VECTORCALL_ARGUMENTS_OFFSET

   Nếu cờ này được đặt trong đối số *nargsf* của một vectorcall, hàm được gọi có thể tạm thời thay đổi ``args[-1]``. Nói cách khác, *args* trỏ đến đối số 1 (không phải 0) trong vector đã cấp phát. Hàm được gọi phải khôi phục giá trị của ``args[-1]`` trước khi trả về.

   Đối với :c:func:`PyObject_VectorcallMethod`, cờ này thay vào đó có nghĩa là ``args[0]`` có thể được thay đổi.

   Bất cứ khi nào có thể thực hiện với chi phí thấp (không cần cấp phát bổ sung), các caller được khuyến khích sử dụng :c:macro:`PY_VECTORCALL_ARGUMENTS_OFFSET`. Làm như vậy cho phép các callable như bound method thực hiện các lời gọi tiếp theo của chúng (bao gồm một đối số *self* được thêm vào đầu) một cách rất hiệu quả.

   .. versionadded:: 3.8

Để gọi một đối tượng triển khai vectorcall, hãy sử dụng hàm :ref:`call API <capi-call>` như với bất kỳ callable nào khác.
:c:func:`PyObject_Vectorcall` thường sẽ có hiệu suất cao nhất.


Điều khiển đệ quy
.................

Khi sử dụng *tp_call*, các hàm được gọi không cần bận tâm về
:ref:`đệ quy <recursion>`: CPython sử dụng
:c:func:`Py_EnterRecursiveCall` và :c:func:`Py_LeaveRecursiveCall` cho các lời gọi được thực hiện bằng *tp_call*.

Để đạt hiệu quả, điều này không áp dụng cho các lời gọi được thực hiện bằng vectorcall: hàm được gọi nên sử dụng *Py_EnterRecursiveCall* và *Py_LeaveRecursiveCall* nếu cần.


API hỗ trợ Vectorcall
.....................

.. c:function:: Py_ssize_t PyVectorcall_NARGS(size_t nargsf)

   Với đối số *nargsf* của vectorcall, hãy trả về số lượng đối số thực tế. Hiện tại tương đương với::

      (Py_ssize_t)(nargsf & ~PY_VECTORCALL_ARGUMENTS_OFFSET)

   Tuy nhiên, nên sử dụng hàm ``PyVectorcall_NARGS`` để cho phép mở rộng trong tương lai.

   .. versionadded:: 3.8

.. c:function:: vectorcallfunc PyVectorcall_Function(PyObject *op)

   Nếu *op* không hỗ trợ giao thức vectorcall (do kiểu không hỗ trợ hoặc do chính instance cụ thể không hỗ trợ), hãy trả về *NULL*. Nếu không, hãy trả về con trỏ hàm vectorcall được lưu trong *op*. Hàm này không bao giờ phát sinh ngoại lệ.

   Điều này chủ yếu hữu ích để kiểm tra xem *op* có hỗ trợ vectorcall hay không; bạn có thể thực hiện việc này bằng cách kiểm tra ``PyVectorcall_Function(op) != NULL``.

   .. versionadded:: 3.9

.. c:function:: PyObject* PyVectorcall_Call(PyObject *callable, PyObject *tuple, PyObject *dict)

   Gọi *callable*'s :c:type:`vectorcallfunc` với các đối số vị trí và từ khóa lần lượt được cung cấp trong một tuple và một dict.

   Đây là một hàm chuyên dụng, được thiết kế để đặt vào
   slot :c:member:`~PyTypeObject.tp_call` hoặc được sử dụng trong một triển khai của ``tp_call``. Hàm này không kiểm tra cờ :c:macro:`Py_TPFLAGS_HAVE_VECTORCALL` và không chuyển sang ``tp_call``.

   .. versionadded:: 3.8


.. _capi-call:

API gọi đối tượng
-----------------

Có nhiều hàm dùng để gọi một đối tượng Python. Mỗi hàm chuyển đổi các đối số của nó sang một quy ước được đối tượng được gọi hỗ trợ – entweder *tp_call* hoặc vectorcall. Để thực hiện ít chuyển đổi nhất có thể, hãy chọn hàm phù hợp nhất với định dạng dữ liệu hiện có.

Bảng sau đây tóm tắt các hàm hiện có; vui lòng xem tài liệu riêng của từng hàm để biết chi tiết.

+----------------------------------------+-----------------+----------------+---------------+
| Function                               | callable        | args           | kwargs        |
+========================================+=================+================+===============+
| :c:func:`PyObject_Call`                | ``PyObject *``  | tuple          | dict/``NULL`` |
+----------------------------------------+-----------------+----------------+---------------+
| :c:func:`PyObject_CallNoArgs`          | ``PyObject *``  | ---            | ---           |
+----------------------------------------+-----------------+----------------+---------------+
| :c:func:`PyObject_CallOneArg`          | ``PyObject *``  | 1 đối tượng    | ---           |
+----------------------------------------+-----------------+----------------+---------------+
| :c:func:`PyObject_CallObject`          | ``PyObject *``  | tuple/``NULL`` | ---           |
+----------------------------------------+-----------------+----------------+---------------+
| :c:func:`PyObject_CallFunction`        | ``PyObject *``  | định dạng      | ---           |
+----------------------------------------+-----------------+----------------+---------------+
| :c:func:`PyObject_CallMethod`          | obj + ``char*`` | định dạng      | ---           |
+----------------------------------------+-----------------+----------------+---------------+
| :c:func:`PyObject_CallFunctionObjArgs` | ``PyObject *``  | variadic       | ---           |
+----------------------------------------+-----------------+----------------+---------------+
| :c:func:`PyObject_CallMethodObjArgs`   | obj + name      | variadic       | ---           |
+----------------------------------------+-----------------+----------------+---------------+
| :c:func:`PyObject_CallMethodNoArgs`    | obj + name      | ---            | ---           |
+----------------------------------------+-----------------+----------------+---------------+
| :c:func:`PyObject_CallMethodOneArg`    | obj + name      | 1 đối tượng    | ---           |
+----------------------------------------+-----------------+----------------+---------------+
| :c:func:`PyObject_Vectorcall`          | ``PyObject *``  | vectorcall     | vectorcall    |
+----------------------------------------+-----------------+----------------+---------------+
| :c:func:`PyObject_VectorcallDict`      | ``PyObject *``  | vectorcall     | dict/``NULL`` |
+----------------------------------------+-----------------+----------------+---------------+
| :c:func:`PyObject_VectorcallMethod`    | đối số + tên    | vectorcall     | vectorcall    |
+----------------------------------------+-----------------+----------------+---------------+


.. c:function:: PyObject* PyObject_Call(PyObject *callable, PyObject *args, PyObject *kwargs)

   Gọi đối tượng Python có thể gọi được *callable*, với các đối số được cung cấp bởi tuple *args* và các đối số có tên được cung cấp bởi dictionary *kwargs*.

   *args* không được là *NULL*; hãy sử dụng tuple rỗng nếu không cần đối số nào. Nếu không cần đối số có tên, *kwargs* có thể là *NULL*.

   Trả về kết quả của lệnh gọi nếu thành công hoặc phát sinh một exception và trả về *NULL* nếu thất bại.

   Điều này tương đương với biểu thức Python: ``callable(*args, **kwargs)``.


.. c:function:: PyObject* PyObject_CallNoArgs(PyObject *callable)

   Gọi đối tượng Python callable *callable* mà không có đối số nào. Đây là cách hiệu quả nhất để gọi đối tượng Python callable mà không có đối số.

   Trả về kết quả của lệnh gọi nếu thành công hoặc phát sinh một exception và trả về *NULL* nếu thất bại.

   .. versionadded:: 3.9


.. c:function:: PyObject* PyObject_CallOneArg(PyObject *callable, PyObject *arg)

   Gọi đối tượng Python callable *callable* với chính xác 1 đối số vị trí *arg* và không có đối số từ khóa nào.

   Trả về kết quả của lệnh gọi nếu thành công hoặc phát sinh một exception và trả về *NULL* nếu thất bại.

   .. versionadded:: 3.9


.. c:function:: PyObject* PyObject_CallObject(PyObject *callable, PyObject *args)

   Gọi đối tượng Python callable *callable* với các đối số được cung cấp bởi tuple *args*. Nếu không cần đối số nào, thì *args* có thể là *NULL*.

   Trả về kết quả của lệnh gọi nếu thành công hoặc phát sinh một exception và trả về *NULL* nếu thất bại.

   Đây là tương đương của biểu thức Python: ``callable(*args)``.


.. c:function:: PyObject* PyObject_CallFunction(PyObject *callable, const char *format, ...)

   Gọi một đối tượng Python có thể gọi được *callable*, với số lượng đối số C thay đổi. Các đối số C được mô tả bằng chuỗi định dạng kiểu :c:func:`Py_BuildValue`. Định dạng này có thể là *NULL*, cho biết không có đối số nào được cung cấp.

   Trả về kết quả của lệnh gọi nếu thành công hoặc phát sinh một exception và trả về *NULL* nếu thất bại.

   Đây là tương đương của biểu thức Python: ``callable(*args)``.

   Lưu ý rằng nếu bạn chỉ truyền các đối số :c:expr:`PyObject *`,
   :c:func:`PyObject_CallFunctionObjArgs` là một lựa chọn nhanh hơn.

   .. versionchanged:: 3.4
      Kiểu của *format* đã được thay đổi từ ``char *``.


.. c:function:: PyObject* PyObject_CallMethod(PyObject *obj, const char *name, const char *format, ...)

   Gọi phương thức có tên *name* của đối tượng *obj* với số lượng đối số C tùy ý. Các đối số C được mô tả bằng một chuỗi :c:func:`Py_BuildValue` format tạo ra một tuple.

   format có thể là *NULL*, cho biết không có đối số nào được cung cấp.

   Trả về kết quả của lệnh gọi nếu thành công hoặc phát sinh một exception và trả về *NULL* nếu thất bại.

   Điều này tương đương với biểu thức Python: ``obj.name(arg1, arg2, ...)``.

   Lưu ý rằng nếu bạn chỉ truyền các đối số :c:expr:`PyObject *`,
   :c:func:`PyObject_CallMethodObjArgs` là một lựa chọn thay thế nhanh hơn.

   .. versionchanged:: 3.4
      Kiểu của *name* và *format* đã được thay đổi từ ``char *``.


.. c:function:: PyObject* PyObject_CallFunctionObjArgs(PyObject *callable, ...)

   Gọi một đối tượng Python có thể gọi được *callable*, với số lượng đối số thay đổi
   :c:expr:`PyObject *` đối số. Các đối số được cung cấp dưới dạng một số lượng tham số thay đổi, theo sau là *NULL*.

   Trả về kết quả của lệnh gọi nếu thành công hoặc phát sinh một exception và trả về *NULL* nếu thất bại.

   Điều này tương đương với biểu thức Python: ``callable(arg1, arg2, ...)``.


.. c:function:: PyObject* PyObject_CallMethodObjArgs(PyObject *obj, PyObject *name, ...)

   Gọi một phương thức của đối tượng Python *obj*, trong đó tên của phương thức được cung cấp dưới dạng một đối tượng chuỗi Python trong *name*. Phương thức được gọi với số lượng đối số thay đổi
   :c:expr:`PyObject *` đối số. Các đối số được cung cấp dưới dạng một số lượng tham số thay đổi, theo sau là *NULL*.

   Trả về kết quả của lệnh gọi nếu thành công hoặc phát sinh một exception và trả về *NULL* nếu thất bại.


.. c:function:: PyObject* PyObject_CallMethodNoArgs(PyObject *obj, PyObject *name)

   Gọi một method của đối tượng Python *obj* mà không có đối số, trong đó tên của method được cung cấp dưới dạng một đối tượng chuỗi Python trong *name*.

   Trả về kết quả của lệnh gọi nếu thành công hoặc phát sinh một exception và trả về *NULL* nếu thất bại.

   .. versionadded:: 3.9


.. c:function:: PyObject* PyObject_CallMethodOneArg(PyObject *obj, PyObject *name, PyObject *arg)

   Gọi một method của đối tượng Python *obj* với một đối số vị trí duy nhất *arg*, trong đó tên của method được cung cấp dưới dạng một đối tượng chuỗi Python trong *name*.

   Trả về kết quả của lệnh gọi nếu thành công hoặc phát sinh một exception và trả về *NULL* nếu thất bại.

   .. versionadded:: 3.9

.. c:function:: PyObject* _PyObject_Vectorcall(PyObject *callable, PyObject *const *args, size_t nargsf, PyObject *kwnames)
   :no-typesetting:

.. c:function:: PyObject* PyObject_Vectorcall(PyObject *callable, PyObject *const *args, size_t nargsf, PyObject *kwnames)

   Gọi một đối tượng Python có thể gọi *callable*. Các đối số giống như đối số của :c:type:`vectorcallfunc`. Nếu *callable* hỗ trợ vectorcall_, thao tác này sẽ gọi trực tiếp hàm vectorcall được lưu trong *callable*.

   Trả về kết quả của lệnh gọi nếu thành công hoặc phát sinh một exception và trả về *NULL* nếu thất bại.

   .. versionadded:: 3.8 kể từ ``_PyObject_Vectorcall``

   .. versionchanged:: 3.9

      Được đổi tên thành tên hiện tại, không có dấu gạch dưới ở đầu. Tên tạm thời cũ là :term:`soft deprecated`.

.. c:function:: PyObject* PyObject_VectorcallDict(PyObject *callable, PyObject *const *args, size_t nargsf, PyObject *kwdict)

   Gọi *callable* với các đối số vị trí được truyền chính xác như trong giao thức vectorcall_, nhưng các đối số từ khóa được truyền dưới dạng từ điển *kwdict*. Mảng *args* chỉ chứa các đối số vị trí.

   Bất kể giao thức nào được sử dụng nội bộ, vẫn cần chuyển đổi các đối số. Do đó, chỉ nên sử dụng hàm này nếu bên gọi đã có sẵn một từ điển để dùng cho các đối số từ khóa, nhưng chưa có tuple cho các đối số vị trí.

   .. versionadded:: 3.9

.. c:function:: PyObject* PyObject_VectorcallMethod(PyObject *name, PyObject *const *args, size_t nargsf, PyObject *kwnames)

   Gọi một phương thức bằng quy ước gọi vectorcall. Tên của phương thức được cung cấp dưới dạng chuỗi Python *name*. Đối tượng có phương thức được gọi là *args[0]*, còn mảng *args* bắt đầu tại *args[1]* biểu thị các đối số của lệnh gọi. Phải có ít nhất một đối số vị trí. *nargsf* là số lượng đối số vị trí, bao gồm *args[0]*, cộng thêm :c:macro:`PY_VECTORCALL_ARGUMENTS_OFFSET` nếu giá trị của ``args[0]`` có thể được thay đổi tạm thời. Các đối số từ khóa có thể được truyền giống như trong
   :c:func:`PyObject_Vectorcall`.

   Nếu đối tượng có tính năng :c:macro:`Py_TPFLAGS_METHOD_DESCRIPTOR`, thao tác này sẽ gọi đối tượng phương thức chưa liên kết với toàn bộ vector *args* làm các đối số.

   Trả về kết quả của lệnh gọi nếu thành công hoặc phát sinh một exception và trả về *NULL* nếu thất bại.

   .. versionadded:: 3.9


API Hỗ trợ Gọi
--------------

.. c:function:: int PyCallable_Check(PyObject *o)

   Xác định xem đối tượng *o* có thể gọi được hay không. Trả về ``1`` nếu đối tượng có thể gọi được và ``0`` nếu không. Hàm này luôn thực hiện thành công.
