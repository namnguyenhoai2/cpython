.. highlight:: c

.. _common-structs:

Các cấu trúc đối tượng phổ biến
===============================

Có rất nhiều cấu trúc được sử dụng trong định nghĩa các kiểu đối tượng cho Python. Phần này mô tả các cấu trúc đó và cách sử dụng chúng.


Các kiểu đối tượng cơ sở và macro
---------------------------------

Tất cả các đối tượng Python cuối cùng đều dùng chung một số ít trường ở phần đầu biểu diễn của đối tượng trong bộ nhớ. Các trường này được biểu diễn bởi
các kiểu :c:type:`PyObject` và :c:type:`PyVarObject`, lần lượt được định nghĩa bởi phần khai triển của một số macro cũng được sử dụng, trực tiếp hoặc gián tiếp, trong định nghĩa của tất cả các đối tượng Python khác. Có thể tìm thấy các macro bổ sung trong phần :ref:`reference counting <countingrefs>`.


.. c:type:: PyObject

   Tất cả các kiểu đối tượng đều là phần mở rộng của kiểu này. Đây là một kiểu chứa thông tin mà Python cần để xử lý một con trỏ tới đối tượng như một đối tượng. Trong bản build "release" thông thường, kiểu này chỉ chứa số lượng tham chiếu của đối tượng và một con trỏ tới đối tượng kiểu tương ứng. Không có gì được khai báo thực sự là một :c:type:`PyObject`, nhưng mọi con trỏ tới một đối tượng Python đều có thể được ép kiểu thành :c:expr:`PyObject*`.

   Không được truy cập trực tiếp vào các thành viên này; thay vào đó, hãy sử dụng các macro như
   :c:macro:`Py_REFCNT` và :c:macro:`Py_TYPE`.

   .. c:member:: Py_ssize_t ob_refcnt

      Số lượng tham chiếu của đối tượng, được trả về bởi :c:macro:`Py_REFCNT`. Không sử dụng trực tiếp trường này; thay vào đó, hãy sử dụng các hàm và macro như
      :c:macro:`!Py_REFCNT`, :c:func:`Py_INCREF` và :c:func:`Py_DecRef`.

      Kiểu của trường có thể khác với ``Py_ssize_t``, tùy thuộc vào cấu hình bản build và nền tảng.

   .. c:member:: PyTypeObject* ob_type

      Kiểu của đối tượng. Không sử dụng trực tiếp trường này; hãy sử dụng :c:macro:`Py_TYPE` và
      :c:func:`Py_SET_TYPE` thay vào đó.


.. c:type:: PyVarObject

   Phần mở rộng của :c:type:`PyObject` bổ sung
   trường :c:member:`~PyVarObject.ob_size`. Trường này dành cho các đối tượng có khái niệm về *length*.

   Cũng như :c:type:`!PyObject`, không được truy cập trực tiếp vào các thành viên; thay vào đó, hãy sử dụng các macro như :c:macro:`Py_SIZE`, :c:macro:`Py_REFCNT` và
   :c:macro:`Py_TYPE`.

   .. c:member:: Py_ssize_t ob_size

      Một trường kích thước, nội dung của trường này nên được xem là chi tiết triển khai nội bộ của một đối tượng.

      Không sử dụng trực tiếp trường này; thay vào đó, hãy sử dụng :c:macro:`Py_SIZE`.

      Các hàm tạo đối tượng như :c:func:`PyObject_NewVar` thường sẽ đặt trường này thành kích thước được yêu cầu (số lượng phần tử). Sau khi tạo, có thể lưu trữ các giá trị tùy ý trong :c:member:`!ob_size` bằng :c:macro:`Py_SET_SIZE`.

      Để lấy độ dài được công khai của một đối tượng, như được hàm Python :py:func:`len` trả về, hãy sử dụng :c:func:`PyObject_Length`.


.. c:macro:: PyObject_HEAD

   Đây là một macro được sử dụng khi khai báo các kiểu mới biểu diễn những đối tượng không có độ dài thay đổi. Macro PyObject_HEAD được mở rộng thành::

      PyObject ob_base;

   Xem tài liệu về :c:type:`PyObject` ở trên.


.. c:macro:: PyObject_VAR_HEAD

   Đây là một macro được sử dụng khi khai báo các kiểu mới biểu diễn những đối tượng có độ dài thay đổi tùy theo từng instance. Macro PyObject_VAR_HEAD mở rộng thành::

      PyVarObject ob_base;

   Xem tài liệu về :c:type:`PyVarObject` ở trên.


.. c:var:: PyTypeObject PyBaseObject_Type

   Lớp cơ sở của tất cả các đối tượng khác, tương đương với :class:`object` trong Python.


.. c:function:: int Py_Is(PyObject *x, PyObject *y)

   Kiểm tra xem đối tượng *x* có phải là đối tượng *y* hay không, tương đương với ``x is y`` trong Python.

   .. versionadded:: 3.10


.. c:function:: int Py_IsNone(PyObject *x)

   Kiểm tra xem một đối tượng có phải là singleton ``None`` hay không, tương đương với ``x is None`` trong Python.

   .. versionadded:: 3.10


.. c:function:: int Py_IsTrue(PyObject *x)

   Kiểm tra xem một đối tượng có phải là singleton ``True`` hay không, tương đương với ``x is True`` trong Python.

   .. versionadded:: 3.10


.. c:function:: int Py_IsFalse(PyObject *x)

   Kiểm tra xem một đối tượng có phải là singleton ``False``, tương đương với ``x is False`` trong Python hay không.

   .. versionadded:: 3.10


.. c:function:: PyTypeObject* Py_TYPE(PyObject *o)

   Lấy kiểu của đối tượng Python *o*.

   Tham chiếu được trả về là :term:`borrowed <borrowed reference>` từ *o*. Không giải phóng tham chiếu này bằng :c:func:`Py_DECREF` hoặc cách tương tự.

   .. versionchanged:: 3.11
      :c:func:`Py_TYPE()` is changed to an inline static function.
      Kiểu của tham số không còn là :c:expr:`const PyObject*`.


.. c:function:: int Py_IS_TYPE(PyObject *o, PyTypeObject *type)

   Trả về giá trị khác 0 nếu kiểu của đối tượng *o* là *type*. Nếu không, trả về 0. Tương đương với: ``Py_TYPE(o) == type``.

   .. versionadded:: 3.9


.. c:function:: void Py_SET_TYPE(PyObject *o, PyTypeObject *type)

   Đặt kiểu của đối tượng *o* thành *type*, mà không thực hiện kiểm tra hay đếm tham chiếu.

   Đây là một thao tác ở mức rất thấp. Thay vào đó, hãy cân nhắc đặt thuộc tính Python :attr:`~object.__class__` bằng :c:func:`PyObject_SetAttrString` hoặc cách tương tự.

   Lưu ý rằng việc gán một kiểu không tương thích có thể dẫn đến hành vi không xác định.

   Nếu *kiểu* là một :ref:`kiểu heap <heap-types>`, bên gọi phải tạo một tham chiếu mới đến nó. Tương tự, nếu kiểu cũ của *o* là một kiểu heap, bên gọi phải giải phóng một tham chiếu đến kiểu đó.

   .. versionadded:: 3.9


.. c:function:: Py_ssize_t Py_SIZE(PyVarObject *o)

   Lấy trường :c:member:`~PyVarObject.ob_size` của *o*.

   .. versionchanged:: 3.11
      :c:func:`Py_SIZE()` is changed to an inline static function.
      Kiểu tham số không còn là :c:expr:`const PyVarObject*`.


.. c:function:: void Py_SET_SIZE(PyVarObject *o, Py_ssize_t size)

   Đặt trường :c:member:`~PyVarObject.ob_size` của *o* thành *size*.

   .. versionadded:: 3.9


.. c:macro:: PyObject_HEAD_INIT(type)

   Đây là một macro mở rộng thành các giá trị khởi tạo cho một
   :c:type:`PyObject` kiểu. Macro này mở rộng thành::

      _PyObject_EXTRA_INIT
      1, type,


.. c:macro:: PyVarObject_HEAD_INIT(type, size)

   Đây là một macro mở rộng thành các giá trị khởi tạo cho một
   kiểu :c:type:`PyVarObject`, bao gồm cả trường :c:member:`~PyVarObject.ob_size`. Macro này mở rộng thành::

      _PyObject_EXTRA_INIT
      1, type, size,


Triển khai các hàm và phương thức
---------------------------------

.. c:type:: PyCFunction

   Kiểu của các hàm được dùng để triển khai hầu hết các Python callable trong C. Các hàm thuộc kiểu này nhận hai tham số :c:expr:`PyObject*` và trả về một giá trị cùng kiểu. Nếu giá trị trả về là ``NULL``, một exception phải được thiết lập. Nếu không phải ``NULL``, giá trị trả về được hiểu là giá trị trả về của hàm khi được cung cấp trong Python. Hàm phải trả về một reference mới.

   Chữ ký hàm là::

      PyObject *PyCFunction(PyObject *self,
                            PyObject *args);

.. c:type:: PyCFunctionWithKeywords

   Kiểu của các hàm được dùng để triển khai Python callable trong C với chữ ký :ref:`METH_VARARGS | METH_KEYWORDS <METH_VARARGS-METH_KEYWORDS>`. Chữ ký hàm là::

      PyObject *PyCFunctionWithKeywords(PyObject *self,
                                        PyObject *args,
                                        PyObject *kwargs);


.. c:type:: PyCFunctionFast

   Kiểu của các hàm được dùng để triển khai Python callable trong C với chữ ký :c:macro:`METH_FASTCALL`. Chữ ký hàm là::

      PyObject *PyCFunctionFast(PyObject *self,
                                PyObject *const *args,
                                Py_ssize_t nargs);

.. c:type:: PyCFunctionFastWithKeywords

   Kiểu của các hàm được dùng để triển khai các callable Python trong C với chữ ký :ref:`METH_FASTCALL | METH_KEYWORDS <METH_FASTCALL-METH_KEYWORDS>`. Chữ ký hàm là::

      PyObject *PyCFunctionFastWithKeywords(PyObject *self,
                                            PyObject *const *args,
                                            Py_ssize_t nargs,
                                            PyObject *kwnames);

.. c:type:: PyCMethod

   Kiểu của các hàm được dùng để triển khai các callable Python trong C với chữ ký :ref:`METH_METHOD | METH_FASTCALL | METH_KEYWORDS <METH_METHOD-METH_FASTCALL-METH_KEYWORDS>`. Chữ ký hàm là::

      PyObject *PyCMethod(PyObject *self,
                          PyTypeObject *defining_class,
                          PyObject *const *args,
                          Py_ssize_t nargs,
                          PyObject *kwnames)

   .. versionadded:: 3.9


.. c:type:: PyMethodDef

   Cấu trúc được dùng để mô tả một phương thức của extension type. Cấu trúc này có bốn trường:

   .. c:member:: const char *ml_name

      Tên của phương thức.

   .. c:member:: PyCFunction ml_meth

      Con trỏ tới phần triển khai bằng C.

   .. c:member:: int ml_flags

      Các bit cờ cho biết cách tạo lời gọi.

   .. c:member:: const char *ml_doc

      Trỏ tới nội dung của docstring.

:c:member:`~PyMethodDef.ml_meth` là một con trỏ hàm C. Các hàm có thể thuộc những kiểu khác nhau, nhưng luôn trả về :c:expr:`PyObject*`. Nếu hàm không thuộc :c:type:`PyCFunction`, trình biên dịch sẽ yêu cầu một phép ép kiểu trong bảng phương thức. Mặc dù :c:type:`PyCFunction` định nghĩa tham số đầu tiên là
:c:expr:`PyObject*`, thông thường phần triển khai phương thức sẽ sử dụng kiểu C cụ thể của đối tượng *self*.

Trường :c:member:`~PyMethodDef.ml_flags` là một bitfield có thể bao gồm các cờ sau. Các cờ riêng lẻ cho biết quy ước gọi hoặc quy ước liên kết.

Có các quy ước gọi sau:

.. c:macro:: METH_VARARGS

   Đây là quy ước gọi thông thường, trong đó các phương thức có kiểu
   :c:type:`PyCFunction`. Hàm nhận hai giá trị :c:expr:`PyObject*`. Giá trị đầu tiên là đối tượng *self* đối với các phương thức; đối với các hàm module, đó là đối tượng module. Tham số thứ hai (thường được gọi là *args*) là một đối tượng tuple đại diện cho tất cả các đối số. Tham số này thường được xử lý bằng :c:func:`PyArg_ParseTuple` hoặc :c:func:`PyArg_UnpackTuple`.


.. c:macro:: METH_KEYWORDS

   Chỉ có thể được sử dụng trong một số kết hợp nhất định với các cờ khác:
   :ref:`METH_VARARGS | METH_KEYWORDS <METH_VARARGS-METH_KEYWORDS>`,
   :ref:`METH_FASTCALL | METH_KEYWORDS <METH_FASTCALL-METH_KEYWORDS>` và
   :ref:`METH_METHOD | METH_FASTCALL | METH_KEYWORDS <METH_METHOD-METH_FASTCALL-METH_KEYWORDS>`.


.. _METH_VARARGS-METH_KEYWORDS:

:c:expr:`METH_VARARGS | METH_KEYWORDS`
   Các phương thức có những cờ này phải có kiểu :c:type:`PyCFunctionWithKeywords`. Hàm này nhận ba tham số: *self*, *args*, *kwargs*, trong đó *kwargs* là một dictionary chứa tất cả các đối số từ khóa hoặc có thể là ``NULL`` nếu không có đối số từ khóa nào. Các tham số thường được xử lý bằng :c:func:`PyArg_ParseTupleAndKeywords`.


.. c:macro:: METH_FASTCALL

   Quy ước gọi nhanh chỉ hỗ trợ các đối số vị trí. Các phương thức có kiểu :c:type:`PyCFunctionFast`. Tham số đầu tiên là *self*, tham số thứ hai là một mảng C gồm các giá trị :c:expr:`PyObject*` cho biết các đối số, còn tham số thứ ba là số lượng đối số (độ dài của mảng).

   .. versionadded:: 3.7

   .. versionchanged:: 3.10

      ``METH_FASTCALL`` hiện đã là một phần của :ref:`stable ABI <stable-abi>`.


.. _METH_FASTCALL-METH_KEYWORDS:

:c:expr:`METH_FASTCALL | METH_KEYWORDS`
   Phần mở rộng của :c:macro:`METH_FASTCALL` cũng hỗ trợ các đối số từ khóa, với các phương thức có kiểu :c:type:`PyCFunctionFastWithKeywords`. Các đối số từ khóa được truyền theo cùng cách như trong
   :ref:`giao thức vectorcall <vectorcall>`: có thêm một :c:expr:`PyObject*` tham số thứ tư, là một tuple biểu diễn tên của các đối số từ khóa (được đảm bảo là các chuỗi) hoặc có thể là ``NULL`` nếu không có từ khóa. Các giá trị của các đối số từ khóa được lưu trong mảng *args*, sau các đối số vị trí.

   .. versionadded:: 3.7


.. c:macro:: METH_METHOD

   Chỉ có thể được sử dụng kết hợp với các flag khác:
   :ref:`METH_METHOD | METH_FASTCALL | METH_KEYWORDS <METH_METHOD-METH_FASTCALL-METH_KEYWORDS>`.


.. _METH_METHOD-METH_FASTCALL-METH_KEYWORDS:

:c:expr:`METH_METHOD | METH_FASTCALL | METH_KEYWORDS`
   Phần mở rộng của :ref:`METH_FASTCALL | METH_KEYWORDS <METH_FASTCALL-METH_KEYWORDS>`, hỗ trợ *lớp định nghĩa*, tức là lớp chứa phương thức đang xét. Lớp định nghĩa có thể là lớp cha của ``Py_TYPE(self)``.

   Phương thức phải có kiểu :c:type:`PyCMethod`, giống như đối với ``METH_FASTCALL | METH_KEYWORDS``, với một đối số ``defining_class`` được thêm vào sau ``self``.

   .. versionadded:: 3.9


.. c:macro:: METH_NOARGS

   Các phương thức không có tham số không cần kiểm tra xem có đối số được truyền vào hay không nếu chúng được liệt kê với flag :c:macro:`METH_NOARGS`. Chúng cần có kiểu
   :c:type:`PyCFunction`. Tham số đầu tiên thường được đặt tên là *self* và sẽ chứa tham chiếu đến module hoặc instance của đối tượng. Trong mọi trường hợp, tham số thứ hai sẽ là ``NULL``.

   Hàm phải có 2 tham số. Vì tham số thứ hai không được sử dụng,
   :c:macro:`Py_UNUSED` có thể được sử dụng để ngăn cảnh báo của compiler.


.. c:macro:: METH_O

   Các method có một đối số object có thể được liệt kê bằng flag :c:macro:`METH_O`, thay vì gọi :c:func:`PyArg_ParseTuple` với một đối số ``"O"``. Chúng có kiểu :c:type:`PyCFunction`, với tham số *self*, và một
   tham số :c:expr:`PyObject*` đại diện cho đối số duy nhất.


Hai hằng số này không được dùng để chỉ calling convention mà chỉ binding khi được sử dụng với các method của class. Không được dùng chúng cho các function được định nghĩa trong module. Với mỗi method cụ thể, nhiều nhất chỉ được đặt một trong các flag này.


.. c:macro:: METH_CLASS

   .. index:: pair: built-in function; classmethod

   Method sẽ nhận đối tượng kiểu làm tham số đầu tiên thay vì một instance của kiểu đó. Cách này được dùng để tạo *class methods*, tương tự như cách tạo ra khi sử dụng built-in decorator :deco:`classmethod`.


.. c:macro:: METH_STATIC

   .. index:: pair: built-in function; staticmethod

   Method sẽ nhận ``NULL`` làm tham số đầu tiên thay vì một instance của kiểu đó. Cách này được dùng để tạo *static methods*, tương tự như cách tạo ra khi sử dụng built-in decorator :deco:`staticmethod`.

Một hằng số khác kiểm soát việc một method có được nạp thay cho một định nghĩa khác có cùng tên method hay không.


.. c:macro:: METH_COEXIST

   Method này sẽ được nạp thay cho các định nghĩa hiện có. Nếu không có *METH_COEXIST*, mặc định là bỏ qua các định nghĩa lặp lại. Vì các slot wrapper được nạp trước method table, sự tồn tại của một slot *sq_contains*, chẳng hạn, sẽ tạo ra một method wrapper có tên
   :meth:`~object.__contains__` và ngăn việc nạp một PyCFunction tương ứng có cùng tên. Khi cờ này được định nghĩa, PyCFunction sẽ được nạp thay cho wrapper object và cùng tồn tại với slot. Điều này hữu ích vì các lệnh gọi đến PyCFunction được tối ưu hóa nhiều hơn so với các lệnh gọi đến wrapper object.


.. c:var:: PyTypeObject PyCMethod_Type

   Đối tượng type tương ứng với các đối tượng method C của Python. Đối tượng này có sẵn dưới dạng :class:`types.BuiltinMethodType` ở tầng Python.


.. c:function:: int PyCMethod_Check(PyObject *op)

   Trả về true nếu *op* là một instance của type :c:type:`PyCMethod_Type` hoặc một subtype của type đó. Hàm này luôn thành công.


.. c:function:: int PyCMethod_CheckExact(PyObject *op)

   Điều này tương tự :c:func:`PyCMethod_Check`, nhưng không tính đến các subtype.


.. c:function:: PyObject * PyCMethod_New(PyMethodDef *ml, PyObject *self, PyObject *module, PyTypeObject *cls)

   Chuyển *ml* thành một đối tượng :term:`callable` của Python. Bên gọi phải đảm bảo rằng *ml* tồn tại lâu hơn :term:`callable`. Thông thường, *ml* được định nghĩa dưới dạng một biến static.

   Tham số *self* sẽ được truyền dưới dạng đối số *self* cho hàm C trong ``ml->ml_meth`` khi được gọi. *self* có thể là ``NULL``.

   Thuộc tính ``__module__`` của đối tượng :term:`callable` có thể được thiết lập từ đối số *module* đã cho. *module* phải là một chuỗi Python, được dùng làm tên của module nơi hàm được định nghĩa. Nếu không khả dụng, có thể đặt thuộc tính này thành :const:`None` hoặc ``NULL``.

   .. seealso:: :attr:`function.__module__`

   Tham số *cls* sẽ được truyền dưới dạng đối số *defining_class* cho hàm C. Phải được đặt nếu :c:macro:`METH_METHOD` được đặt trên ``ml->ml_flags``.

   .. versionadded:: 3.9


.. c:var:: PyTypeObject PyCFunction_Type

   Đối tượng kiểu tương ứng với các đối tượng hàm C của Python. Đối tượng này khả dụng dưới dạng :class:`types.BuiltinFunctionType` trong lớp Python.


.. c:function:: int PyCFunction_Check(PyObject *op)

   Trả về true nếu *op* là một thể hiện của kiểu :c:type:`PyCFunction_Type` hoặc một kiểu con của nó. Hàm này luôn thành công.


.. c:function:: int PyCFunction_CheckExact(PyObject *op)

   Tương tự như :c:func:`PyCFunction_Check`, nhưng không tính đến các kiểu con.


.. c:function:: PyObject * PyCFunction_NewEx(PyMethodDef *ml, PyObject *self, PyObject *module)

   Tương đương với ``PyCMethod_New(ml, self, module, NULL)``.


.. c:function:: PyObject * PyCFunction_New(PyMethodDef *ml, PyObject *self)

   Tương đương với ``PyCMethod_New(ml, self, NULL, NULL)``.


.. c:function:: int PyCFunction_GetFlags(PyObject *func)

   Lấy các cờ của hàm trên *func* như đã được truyền vào
   :c:member:`~PyMethodDef.ml_flags`.

   Nếu *func* không phải là một đối tượng hàm C, thao tác này sẽ thất bại với một ngoại lệ. *func* không được là ``NULL``.

   Hàm này trả về các cờ của hàm khi thành công và ``-1`` cùng với một ngoại lệ được thiết lập khi thất bại.


.. c:function:: int PyCFunction_GET_FLAGS(PyObject *func)

   Điều này tương tự :c:func:`PyCFunction_GetFlags`, nhưng không kiểm tra lỗi hoặc kiểu.


.. c:function:: PyCFunction PyCFunction_GetFunction(PyObject *func)

   Lấy con trỏ hàm trên *func* như đã được truyền vào
   :c:member:`~PyMethodDef.ml_meth`.

   Nếu *func* không phải là một đối tượng hàm C, thao tác này sẽ thất bại với một ngoại lệ. *func* không được là ``NULL``.

   Hàm này trả về con trỏ hàm khi thành công và ``NULL`` cùng với một ngoại lệ được thiết lập khi thất bại.


.. c:function:: int PyCFunction_GET_FUNCTION(PyObject *func)

   Điều này giống với :c:func:`PyCFunction_GetFunction`, nhưng không thực hiện kiểm tra lỗi hoặc kiểu.


.. c:function:: PyObject *PyCFunction_GetSelf(PyObject *func)

   Lấy đối tượng "self" trên *func*. Đây là đối tượng sẽ được truyền vào đối số đầu tiên của một :c:type:`PyCFunction`. Đối với các đối tượng hàm C được tạo thông qua một :c:type:`PyMethodDef` trên một :c:type:`PyModuleDef`, đây là đối tượng module thu được.

   Nếu *func* không phải là một đối tượng hàm C, thao tác này sẽ thất bại với một ngoại lệ. *func* không được là ``NULL``.

   Hàm này trả về một :term:`borrowed reference` tới đối tượng "self" khi thành công và ``NULL`` cùng với một ngoại lệ được thiết lập khi thất bại.


.. c:function:: PyObject *PyCFunction_GET_SELF(PyObject *func)

   Điều này giống với :c:func:`PyCFunction_GetSelf`, nhưng không thực hiện kiểm tra lỗi hoặc kiểu.


Truy cập các thuộc tính của kiểu mở rộng
----------------------------------------

.. c:type:: PyMemberDef

   Cấu trúc mô tả một thuộc tính của một kiểu tương ứng với một thành viên struct C. Khi định nghĩa một class, hãy đặt một mảng các cấu trúc này kết thúc bằng NULL vào vị trí :c:member:`~PyTypeObject.tp_members`.

   Các trường của nó, theo thứ tự, là:

   .. c:member:: const char* name

         Tên của thành viên. Giá trị NULL đánh dấu phần kết thúc của một mảng ``PyMemberDef[]``.

         Chuỗi này phải là static; chuỗi sẽ không được sao chép.

   .. c:member:: int type

      Kiểu của thành viên trong struct C. Xem :ref:`PyMemberDef-types` để biết các giá trị có thể có.

   .. c:member:: Py_ssize_t offset

      Độ lệch tính bằng byte tại đó thành viên nằm trong struct đối tượng của kiểu.

   .. c:member:: int flags

      Không hoặc nhiều giá trị trong số :ref:`PyMemberDef-flags`, được kết hợp bằng phép OR theo bit.

   .. c:member:: const char* doc

      Docstring hoặc NULL. Chuỗi này phải là tĩnh và không được sao chép. Thông thường, nó được định nghĩa bằng :c:macro:`PyDoc_STR`.

   Theo mặc định (khi :c:member:`~PyMemberDef.flags` là ``0``), các thành viên cho phép cả quyền truy cập đọc và ghi. Sử dụng cờ :c:macro:`Py_READONLY` để chỉ cho phép truy cập đọc. Một số kiểu nhất định, chẳng hạn như :c:macro:`Py_T_STRING`, ngầm bao gồm :c:macro:`Py_READONLY`. Chỉ các thành viên :c:macro:`Py_T_OBJECT_EX` (và :c:macro:`T_OBJECT` cũ) mới có thể bị xóa.

   .. _pymemberdef-offsets:

   Đối với các kiểu được cấp phát trên heap (được tạo bằng :c:func:`PyType_FromSpec` hoặc tương tự), ``PyMemberDef`` có thể chứa định nghĩa cho thành viên đặc biệt ``"__vectorcalloffset__"``, tương ứng với
   :c:member:`~PyTypeObject.tp_vectorcall_offset` trong các đối tượng kiểu. Thành viên này phải được định nghĩa bằng ``Py_T_PYSSIZET``, và ``Py_READONLY`` hoặc ``Py_READONLY | Py_RELATIVE_OFFSET``. Ví dụ::

      static PyMemberDef spam_type_members[] = {
          {"__vectorcalloffset__", Py_T_PYSSIZET,
           offsetof(Spam_object, vectorcall), Py_READONLY},
          {NULL}  /* Sentinel */
      };

   (Bạn có thể cần ``#include <stddef.h>`` cho :c:func:`!offsetof`.)

   Các offset cũ :c:member:`~PyTypeObject.tp_dictoffset` và
   :c:member:`~PyTypeObject.tp_weaklistoffset` có thể được định nghĩa tương tự bằng các thành viên ``"__dictoffset__"`` và ``"__weaklistoffset__"``, nhưng các extension được khuyến khích mạnh mẽ sử dụng :c:macro:`Py_TPFLAGS_MANAGED_DICT` và
   :c:macro:`Py_TPFLAGS_MANAGED_WEAKREF` thay vào đó.

   .. versionchanged:: 3.12

      ``PyMemberDef`` luôn khả dụng. Trước đây, cần phải include ``"structmember.h"``.

   .. versionchanged:: 3.14

      :c:macro:`Py_RELATIVE_OFFSET` hiện được cho phép đối với ``"__vectorcalloffset__"``, ``"__dictoffset__"`` và ``"__weaklistoffset__"``.

.. c:function:: PyObject* PyMember_GetOne(const char *obj_addr, struct PyMemberDef *m)

   Lấy một thuộc tính thuộc về đối tượng tại địa chỉ *obj_addr*. Thuộc tính này được mô tả bởi ``PyMemberDef`` *m*. Trả về ``NULL`` khi xảy ra lỗi.

   .. versionchanged:: 3.12

      ``PyMember_GetOne`` luôn khả dụng. Trước đây, cần phải include ``"structmember.h"``.

.. c:function:: int PyMember_SetOne(char *obj_addr, struct PyMemberDef *m, PyObject *o)

   Đặt thuộc tính thuộc về đối tượng tại địa chỉ *obj_addr* thành đối tượng *o*. Thuộc tính cần đặt được mô tả bởi ``PyMemberDef`` *m*. Trả về ``0`` nếu thành công và một giá trị âm nếu thất bại.

   .. versionchanged:: 3.12

      ``PyMember_SetOne`` luôn khả dụng. Trước đây, cần phải include ``"structmember.h"``.

.. _PyMemberDef-flags:

Cờ thành viên
^^^^^^^^^^^^^

Có thể sử dụng các cờ sau với :c:member:`PyMemberDef.flags`:

.. c:macro:: Py_READONLY

   Không thể ghi.

.. c:macro:: Py_AUDIT_READ

   Phát ra một ``object.__getattr__`` :ref:`sự kiện audit <audit-events>` trước khi đọc.

.. c:macro:: Py_RELATIVE_OFFSET

   Cho biết rằng :c:member:`~PyMemberDef.offset` của mục ``PyMemberDef`` này chỉ một offset tính từ dữ liệu dành riêng cho lớp con, thay vì từ ``PyObject``.

   Chỉ có thể được sử dụng như một phần của :c:data:`Py_tp_members`
   :c:type:`slot <PyType_Slot>` khi tạo một lớp bằng cách sử dụng giá trị âm
   :c:member:`~PyType_Spec.basicsize`. Trong trường hợp đó, đây là yêu cầu bắt buộc. Khi đặt :c:member:`~PyTypeObject.tp_members` từ slot trong quá trình tạo lớp, Python sẽ xóa cờ và đặt
   :c:member:`PyMemberDef.offset` thành độ lệch so với cấu trúc ``PyObject``.

.. index::
   single: READ_RESTRICTED (C macro)
   single: WRITE_RESTRICTED (C macro)
   single: RESTRICTED (C macro)

.. versionchanged:: 3.10

   Các macro :c:macro:`!RESTRICTED`, :c:macro:`!READ_RESTRICTED` và
   macro :c:macro:`!WRITE_RESTRICTED` có sẵn cùng với ``#include "structmember.h"`` đã không còn được khuyến nghị sử dụng.
   :c:macro:`!READ_RESTRICTED` và :c:macro:`!RESTRICTED` tương đương với
   :c:macro:`Py_AUDIT_READ`; :c:macro:`!WRITE_RESTRICTED` không thực hiện thao tác nào.

.. index::
   single: READONLY (C macro)

.. versionchanged:: 3.12

   Macro :c:macro:`!READONLY` đã được đổi tên thành :c:macro:`Py_READONLY`. Macro :c:macro:`!PY_AUDIT_READ` đã được đổi tên với tiền tố ``Py_``. Các tên mới hiện luôn khả dụng. Trước đây, các tên này yêu cầu ``#include "structmember.h"``. Tệp tiêu đề vẫn khả dụng và cung cấp các tên cũ.

.. _PyMemberDef-types:

Các kiểu thành viên
^^^^^^^^^^^^^^^^^^^

:c:member:`PyMemberDef.type` có thể là một trong các macro sau đây, tương ứng với nhiều kiểu C khác nhau. Khi thành viên được truy cập trong Python, nó sẽ được chuyển đổi thành kiểu Python tương ứng. Khi được thiết lập từ Python, nó sẽ được chuyển đổi обратно thành kiểu C. Nếu không thể thực hiện việc đó, một ngoại lệ như :exc:`TypeError` hoặc
:exc:`ValueError` sẽ được phát sinh.

Trừ khi được đánh dấu (D), không thể xóa các thuộc tính được định nghĩa theo cách này bằng, chẳng hạn như, :keyword:`del` hoặc :py:func:`delattr`.

+----------------------------------+---------------------------------------+------------------------+
| Tên macro                        | Kiểu C                                | Kiểu Python            |
+==================================+=======================================+========================+
| .. c:macro:: Py_T_BYTE           | :c:expr:`char`                        | :py:class:`int`        |
+----------------------------------+---------------------------------------+------------------------+
| .. c:macro:: Py_T_SHORT          | :c:expr:`short`                       | :py:class:`int`        |
+----------------------------------+---------------------------------------+------------------------+
| .. c:macro:: Py_T_INT            | :c:expr:`int`                         | :py:class:`int`        |
+----------------------------------+---------------------------------------+------------------------+
| .. c:macro:: Py_T_LONG           | :c:expr:`long`                        | :py:class:`int`        |
+----------------------------------+---------------------------------------+------------------------+
| .. c:macro:: Py_T_LONGLONG       | :c:expr:`long long`                   | :py:class:`int`        |
+----------------------------------+---------------------------------------+------------------------+
| .. c:macro:: Py_T_UBYTE          | :c:expr:`unsigned char`               | :py:class:`int`        |
+----------------------------------+---------------------------------------+------------------------+
| .. c:macro:: Py_T_UINT           | :c:expr:`unsigned int`                | :py:class:`int`        |
+----------------------------------+---------------------------------------+------------------------+
| .. c:macro:: Py_T_USHORT         | :c:expr:`unsigned short`              | :py:class:`int`        |
+----------------------------------+---------------------------------------+------------------------+
| .. c:macro:: Py_T_ULONG          | :c:expr:`unsigned long`               | :py:class:`int`        |
+----------------------------------+---------------------------------------+------------------------+
| .. c:macro:: Py_T_ULONGLONG      | :c:expr:`unsigned long long`          | :py:class:`int`        |
+----------------------------------+---------------------------------------+------------------------+
| .. c:macro:: Py_T_PYSSIZET       | :c:expr:`Py_ssize_t`                  | :py:class:`int`        |
+----------------------------------+---------------------------------------+------------------------+
| .. c:macro:: Py_T_FLOAT          | :c:expr:`float`                       | :py:class:`float`      |
+----------------------------------+---------------------------------------+------------------------+
| .. c:macro:: Py_T_DOUBLE         | :c:expr:`double`                      | :py:class:`float`      |
+----------------------------------+---------------------------------------+------------------------+
| .. c:macro:: Py_T_BOOL           | :c:expr:`char` (được ghi là 0 hoặc 1) | :py:class:`bool`       |
+----------------------------------+---------------------------------------+------------------------+
| .. c:macro:: Py_T_STRING         | :c:expr:`const char *` (*)            | :py:class:`str` (RO)   |
+----------------------------------+---------------------------------------+------------------------+
| .. c:macro:: Py_T_STRING_INPLACE | :c:expr:`const char[]` (*)            | :py:class:`str` (RO)   |
+----------------------------------+---------------------------------------+------------------------+
| .. c:macro:: Py_T_CHAR           | :c:expr:`char` (0-127)                | :py:class:`str` (**)   |
+----------------------------------+---------------------------------------+------------------------+
| .. c:macro:: Py_T_OBJECT_EX      | :c:expr:`PyObject *`                  | :py:class:`object` (D) |
+----------------------------------+---------------------------------------+------------------------+

   (*): Chuỗi C kết thúc bằng số 0 và được mã hóa UTF8. Với :c:macro:`!Py_T_STRING`, biểu diễn C là một con trỏ; với :c:macro:`!Py_T_STRING_INPLACE`, chuỗi được lưu trực tiếp trong cấu trúc.

   (****): Chuỗi có độ dài 1. Chỉ chấp nhận ASCII.

   (RO): Ngụ ý :c:macro:`Py_READONLY`.

   (D): Có thể bị xóa, trong trường hợp đó con trỏ được đặt thành ``NULL``. Việc đọc một con trỏ ``NULL`` sẽ phát sinh :py:exc:`AttributeError`.

.. index::
   single: T_BYTE (C macro)
   single: T_SHORT (C macro)
   single: T_INT (C macro)
   single: T_LONG (C macro)
   single: T_LONGLONG (C macro)
   single: T_UBYTE (C macro)
   single: T_USHORT (C macro)
   single: T_UINT (C macro)
   single: T_ULONG (C macro)
   single: T_ULONGULONG (C macro)
   single: T_PYSSIZET (C macro)
   single: T_FLOAT (C macro)
   single: T_DOUBLE (C macro)
   single: T_BOOL (C macro)
   single: T_CHAR (C macro)
   single: T_STRING (C macro)
   single: T_STRING_INPLACE (C macro)
   single: T_OBJECT_EX (C macro)
   single: structmember.h

.. versionadded:: 3.12

   Trong các phiên bản trước, các macro chỉ khả dụng với ``#include "structmember.h"`` và được đặt tên không có tiền tố ``Py_`` (ví dụ như ``T_INT``). Header này vẫn khả dụng và chứa các tên cũ, cùng với các kiểu không còn được khuyến nghị sau đây:

   .. c:macro:: T_OBJECT

      Giống như ``Py_T_OBJECT_EX``, nhưng ``NULL`` được chuyển đổi thành ``None``. Điều này dẫn đến hành vi bất ngờ trong Python: việc xóa thuộc tính thực chất sẽ đặt nó thành ``None``.

   .. c:macro:: T_NONE

      Luôn là ``None``. Phải được sử dụng với :c:macro:`Py_READONLY`.

Định nghĩa Getter và Setter
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. c:type:: PyGetSetDef

   Cấu trúc dùng để định nghĩa quyền truy cập giống thuộc tính cho một kiểu. Xem thêm mô tả về slot :c:member:`PyTypeObject.tp_getset`.

   .. c:member:: const char* name

      tên thuộc tính

   .. c:member:: getter get

      Hàm C để lấy thuộc tính.

   .. c:member:: setter set

      Hàm C tùy chọn để thiết lập hoặc xóa thuộc tính. Nếu ``NULL``, thuộc tính là chỉ đọc.

   .. c:member:: const char* doc

      docstring tùy chọn

   .. c:member:: void* closure

      Con trỏ dữ liệu người dùng tùy chọn, cung cấp dữ liệu bổ sung cho getter và setter.

.. c:type:: PyObject *(*getter)(PyObject *, void *)

   Hàm ``get`` nhận một tham số :c:expr:`PyObject*` (đối tượng thực thể) và một con trỏ dữ liệu người dùng (đối tượng ``closure`` liên kết):

   Hàm này sẽ trả về một tham chiếu mới khi thành công hoặc ``NULL`` với một exception đã được thiết lập khi thất bại.

.. c:type:: int (*setter)(PyObject *, PyObject *, void *)

   Các hàm ``set`` nhận hai tham số :c:expr:`PyObject*` (đối tượng thực thể và giá trị cần thiết lập) cùng một con trỏ dữ liệu người dùng (đối tượng ``closure`` liên kết):

   Nếu thuộc tính cần được xóa, tham số thứ hai là ``NULL``. Khi thành công, cần trả về ``0``; khi thất bại, trả về ``-1`` cùng với một ngoại lệ đã được thiết lập.
