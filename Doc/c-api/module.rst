.. highlight:: c

.. _moduleobjects:

Đối tượng module
----------------

.. index:: pair: object; module


.. c:var:: PyTypeObject PyModule_Type

   .. index:: single: ModuleType (in module types)

   Instance này của :c:type:`PyTypeObject` đại diện cho kiểu module Python. Kiểu này được cung cấp cho các chương trình Python dưới dạng :py:class:`types.ModuleType`.


.. c:function:: int PyModule_Check(PyObject *p)

   Trả về true nếu *p* là một đối tượng module hoặc một kiểu con của đối tượng module. Hàm này luôn thực thi thành công.


.. c:function:: int PyModule_CheckExact(PyObject *p)

   Trả về true nếu *p* là một đối tượng module nhưng không phải là một kiểu con của
   :c:data:`PyModule_Type`. Hàm này luôn thực thi thành công.


.. c:function:: PyObject* PyModule_NewObject(PyObject *name)

   .. index::
      single: __name__ (module attribute)
      single: __doc__ (module attribute)
      single: __file__ (module attribute)
      single: __package__ (module attribute)
      single: __loader__ (module attribute)

   Trả về một đối tượng module mới với :attr:`module.__name__` được đặt thành *name*. Các thuộc tính :attr:`!__name__`, :attr:`~module.__doc__` của module,
   :attr:`~module.__package__` và :attr:`~module.__loader__` được điền vào (tất cả trừ :attr:`!__name__` đều được đặt thành ``None``). Bên gọi chịu trách nhiệm thiết lập thuộc tính :attr:`~module.__file__`.

   Trả về ``NULL`` với một exception được đặt khi xảy ra lỗi.

   .. versionadded:: 3.3

   .. versionchanged:: 3.4
      :attr:`~module.__package__` and :attr:`~module.__loader__` are now set to
      ``None``.


.. c:function:: PyObject* PyModule_New(const char *name)

   Tương tự như :c:func:`PyModule_NewObject`, nhưng tên là một chuỗi được mã hóa UTF-8 thay vì một đối tượng Unicode.


.. c:function:: PyObject* PyModule_GetDict(PyObject *module)

   .. index:: single: __dict__ (module attribute)

   Trả về đối tượng dictionary triển khai namespace của *module*; đối tượng này giống với thuộc tính :attr:`~object.__dict__` của đối tượng module. Nếu *module* không phải là một đối tượng module (hoặc một kiểu con của đối tượng module),
   :exc:`SystemError` được phát sinh và ``NULL`` được trả về.

   Các extension được khuyến nghị sử dụng những hàm ``PyModule_*`` và ``PyObject_*`` khác thay vì thao tác trực tiếp với namespace của module
   :attr:`~object.__dict__`.

   Tham chiếu được trả về là tham chiếu mượn từ module; nó hợp lệ cho đến khi module bị hủy.


.. c:function:: PyObject* PyModule_GetNameObject(PyObject *module)

   .. index::
      single: __name__ (module attribute)
      single: SystemError (built-in exception)

   Trả về giá trị :attr:`~module.__name__` của *module*.  Nếu module không cung cấp giá trị này hoặc nếu giá trị đó không phải là một chuỗi, :exc:`SystemError` được phát sinh và ``NULL`` được trả về.

   .. versionadded:: 3.3


.. c:function:: const char* PyModule_GetName(PyObject *module)

   Tương tự như :c:func:`PyModule_GetNameObject` nhưng trả về tên được mã hóa thành ``'utf-8'``.

   Bộ đệm được trả về chỉ hợp lệ cho đến khi module được đổi tên hoặc hủy. Lưu ý rằng mã Python có thể đổi tên một module bằng cách thiết lập thuộc tính :py:attr:`~module.__name__` của module đó.

.. c:function:: void* PyModule_GetState(PyObject *module)

   Trả về "trạng thái" của module, tức là một con trỏ đến khối bộ nhớ được cấp phát tại thời điểm tạo module, hoặc ``NULL``.  Xem
   :c:member:`PyModuleDef.m_size`.


.. c:function:: PyModuleDef* PyModule_GetDef(PyObject *module)

   Trả về một con trỏ đến struct :c:type:`PyModuleDef` mà từ đó module được tạo, hoặc ``NULL`` nếu module không được tạo từ một định nghĩa.

   Khi xảy ra lỗi, trả về ``NULL`` cùng với một exception được thiết lập. Sử dụng :c:func:`PyErr_Occurred` để phân biệt trường hợp này với trường hợp bị thiếu
   :c:type:`!PyModuleDef`.


.. c:function:: PyObject* PyModule_GetFilenameObject(PyObject *module)

   .. index::
      single: __file__ (module attribute)
      single: SystemError (built-in exception)

   Trả về tên của tệp từ đó *module* được tải bằng cách sử dụng *module*'s
   :attr:`~module.__file__` attribute.  Nếu thuộc tính này chưa được định nghĩa hoặc không phải là một chuỗi, raise :exc:`SystemError` và trả về ``NULL``; nếu không, trả về một tham chiếu đến một đối tượng Unicode.

   .. versionadded:: 3.2


.. c:function:: const char* PyModule_GetFilename(PyObject *module)

   Tương tự như :c:func:`PyModule_GetFilenameObject` nhưng trả về tên tệp được mã hóa theo 'utf-8'.

   Bộ đệm được trả về chỉ hợp lệ cho đến khi thuộc tính :py:attr:`~module.__file__` của module được gán lại hoặc module bị hủy.

   .. deprecated:: 3.2
      :c:func:`PyModule_GetFilename` raises :exc:`UnicodeEncodeError` on
      các tên tệp không thể mã hóa, hãy sử dụng :c:func:`PyModule_GetFilenameObject` thay thế.


.. _pymoduledef:

Định nghĩa module
-----------------

Các hàm trong phần trước hoạt động trên mọi đối tượng module, bao gồm cả các module được nhập từ mã Python.

Các module được định nghĩa bằng C API thường sử dụng một *định nghĩa module*,
:c:type:`PyModuleDef` -- một “mô tả” hằng được cấp phát tĩnh về cách tạo một module.

Định nghĩa này thường được dùng để định nghĩa đối tượng module “chính” của một extension (xem :ref:`extension-modules` để biết chi tiết). Nó cũng được dùng để
:ref:`tạo các module extension một cách động <moduledef-dynamic>`.

Không giống :c:func:`PyModule_New`, định nghĩa này cho phép quản lý *trạng thái module* -- một vùng bộ nhớ được cấp phát và giải phóng cùng với đối tượng module. Không giống các thuộc tính Python của module, mã Python không thể thay thế hoặc xóa dữ liệu được lưu trong trạng thái module.

.. c:type:: PyModuleDef

   Cấu trúc định nghĩa module chứa mọi thông tin cần thiết để tạo một đối tượng module. Cấu trúc này phải được cấp phát tĩnh (hoặc phải được bảo đảm vẫn hợp lệ trong thời gian bất kỳ module nào được tạo từ nó còn tồn tại). Thông thường, mỗi module extension chỉ có một biến thuộc kiểu này.

   .. c:member:: PyModuleDef_Base m_base

      Luôn khởi tạo thành viên này thành :c:macro:`PyModuleDef_HEAD_INIT`.

   .. c:member:: const char *m_name

      Tên của module mới.

   .. c:member:: const char *m_doc

      Docstring của module; thường là một biến docstring được tạo bằng
      :c:macro:`PyDoc_STRVAR` được sử dụng.

   .. c:member:: Py_ssize_t m_size

      Trạng thái module có thể được lưu trong một vùng nhớ riêng cho từng module, có thể truy xuất bằng :c:func:`PyModule_GetState`, thay vì trong các biến toàn cục static. Điều này giúp các module an toàn khi sử dụng trong nhiều sub-interpreter.

      Vùng nhớ này được cấp phát dựa trên *m_size* khi tạo module và được giải phóng khi đối tượng module được hủy, sau khi
      hàm :c:member:`~PyModuleDef.m_free` đã được gọi, nếu có.

      Đặt giá trị này thành một giá trị không âm có nghĩa là module có thể được khởi tạo lại và chỉ định lượng bộ nhớ bổ sung mà module cần cho trạng thái của nó.

      Đặt ``m_size`` thành ``-1`` có nghĩa là module không hỗ trợ sub-interpreter vì module có trạng thái toàn cục. ``m_size`` âm chỉ được phép khi sử dụng
      :ref:`khởi tạo một pha kiểu cũ <single-phase-initialization>` hoặc khi :ref:`tạo module một cách động <moduledef-dynamic>`.

      Xem :PEP:`3121` để biết thêm chi tiết.

   .. c:member:: PyMethodDef* m_methods

      Một con trỏ trỏ đến bảng các hàm cấp module, được mô tả bởi
      các giá trị :c:type:`PyMethodDef`. Có thể là ``NULL`` nếu không có hàm nào.

   .. c:member:: PyModuleDef_Slot* m_slots

      Một mảng các định nghĩa slot cho quá trình khởi tạo nhiều giai đoạn, kết thúc bằng một mục ``{0, NULL}``. Khi sử dụng quá trình khởi tạo một giai đoạn kiểu cũ, *m_slots* phải là ``NULL``.

      .. versionchanged:: 3.5

         Trước phiên bản 3.5, thành viên này luôn được đặt thành ``NULL`` và được định nghĩa như sau:

           .. c:member:: inquiry m_reload

   .. c:member:: traverseproc m_traverse

      Một hàm traversal được gọi trong quá trình traversal đối tượng module bởi GC, hoặc ``NULL`` nếu không cần.

      Hàm này không được gọi nếu trạng thái module đã được yêu cầu nhưng chưa được cấp phát. Điều này xảy ra ngay sau khi module được tạo và trước khi module được thực thi (hàm :c:data:`Py_mod_exec`). Cụ thể hơn, hàm này không được gọi nếu :c:member:`~PyModuleDef.m_size` lớn hơn 0 và trạng thái module (do :c:func:`PyModule_GetState` trả về) là ``NULL``.

      .. versionchanged:: 3.9
         Không còn được gọi trước khi trạng thái module được cấp phát.

   .. c:member:: inquiry m_clear

      Một hàm clear để gọi trong quá trình GC dọn dẹp đối tượng module, hoặc ``NULL`` nếu không cần.

      Hàm này không được gọi nếu trạng thái module đã được yêu cầu nhưng chưa được cấp phát. Điều này xảy ra ngay sau khi module được tạo và trước khi module được thực thi (hàm :c:data:`Py_mod_exec`). Cụ thể hơn, hàm này không được gọi nếu :c:member:`~PyModuleDef.m_size` lớn hơn 0 và trạng thái module (do :c:func:`PyModule_GetState` trả về) là ``NULL``.

      Tương tự như :c:member:`PyTypeObject.tp_clear`, hàm này *không phải lúc nào cũng* được gọi trước khi một module được giải phóng. Ví dụ: khi việc đếm tham chiếu đủ để xác định rằng một đối tượng không còn được sử dụng, trình thu gom rác tuần hoàn không tham gia và
      :c:member:`~PyModuleDef.m_free` được gọi trực tiếp.

      .. versionchanged:: 3.9
         Không còn được gọi trước khi trạng thái module được cấp phát.

   .. c:member:: freefunc m_free

      Một hàm để gọi trong quá trình giải phóng đối tượng module, hoặc ``NULL`` nếu không cần.

      Hàm này không được gọi nếu trạng thái module đã được yêu cầu nhưng chưa được cấp phát. Điều này xảy ra ngay sau khi module được tạo và trước khi module được thực thi (hàm :c:data:`Py_mod_exec`). Cụ thể hơn, hàm này không được gọi nếu :c:member:`~PyModuleDef.m_size` lớn hơn 0 và trạng thái module (do :c:func:`PyModule_GetState` trả về) là ``NULL``.

      .. versionchanged:: 3.9
         Không còn được gọi trước khi trạng thái module được cấp phát.


.. c:var:: PyTypeObject PyModuleDef_Type

   Kiểu của các đối tượng ``PyModuleDef``.


Các slot của module
...................

.. c:type:: PyModuleDef_Slot

   .. c:member:: int slot

      ID của slot, được chọn từ các giá trị có sẵn được giải thích bên dưới.

   .. c:member:: void* value

      Giá trị của slot, có ý nghĩa phụ thuộc vào ID của slot.

   .. versionadded:: 3.5

Các loại slot có sẵn là:

.. c:macro:: Py_mod_create

   Chỉ định một hàm được gọi để tự tạo đối tượng module. Con trỏ *value* của slot này phải trỏ đến một hàm có chữ ký:

   .. c:function:: PyObject* create_module(PyObject *spec, PyModuleDef *def)
      :no-index-entry:
      :no-contents-entry:

   Hàm nhận một instance :py:class:`~importlib.machinery.ModuleSpec`, như được định nghĩa trong :PEP:`451`, cùng với định nghĩa module. Hàm phải trả về một đối tượng module mới, hoặc đặt lỗi và trả về ``NULL``.

   Hàm này nên được giữ ở mức tối thiểu. Đặc biệt, hàm không nên gọi mã Python tùy ý, vì việc cố gắng import lại cùng module có thể dẫn đến vòng lặp vô hạn.

   Không được chỉ định nhiều slot ``Py_mod_create`` trong một định nghĩa module.

   Nếu không chỉ định ``Py_mod_create``, cơ chế import sẽ tạo một đối tượng module thông thường bằng :c:func:`PyModule_New`. Tên được lấy từ *spec*, không phải từ định nghĩa, để cho phép các extension module tự động điều chỉnh theo vị trí của chúng trong hệ thống phân cấp module và được import dưới các tên khác nhau thông qua symlink, đồng thời vẫn dùng chung một định nghĩa module duy nhất.

   Không có yêu cầu đối tượng được trả về phải là một instance của
   :c:type:`PyModule_Type`. Có thể sử dụng bất kỳ kiểu nào, miễn là kiểu đó hỗ trợ thiết lập và lấy các thuộc tính liên quan đến import. Tuy nhiên, chỉ được trả về các instance ``PyModule_Type`` nếu ``PyModuleDef`` có ``NULL`` ``m_traverse``, ``m_clear``, ``m_free`` không phải ``m_size``; hoặc có các slot khác ngoài ``Py_mod_create``.

   .. versionadded:: 3.5

.. c:macro:: Py_mod_exec

   Chỉ định một hàm được gọi để *thực thi* module. Điều này tương đương với việc thực thi mã của một module Python: thông thường, hàm này thêm các lớp và hằng số vào module. Chữ ký của hàm là:

   .. c:function:: int exec_module(PyObject* module)
      :no-index-entry:
      :no-contents-entry:

   Nếu chỉ định nhiều ``Py_mod_exec`` slot__, chúng sẽ được xử lý theo thứ tự xuất hiện trong mảng *m_slots*.

   .. versionadded:: 3.5

.. c:macro:: Py_mod_multiple_interpreters

   Chỉ định một trong các giá trị sau:

   .. c:namespace:: NULL

   .. c:macro:: Py_MOD_MULTIPLE_INTERPRETERS_NOT_SUPPORTED

      Module không hỗ trợ việc được import trong các subinterpreter.

   .. c:macro:: Py_MOD_MULTIPLE_INTERPRETERS_SUPPORTED

      Module hỗ trợ được import trong các subinterpreter, nhưng chỉ khi chúng dùng chung GIL của interpreter chính. (Xem :ref:`isolating-extensions-howto`.)

   .. c:macro:: Py_MOD_PER_INTERPRETER_GIL_SUPPORTED

      Module hỗ trợ được import trong các subinterpreter, ngay cả khi chúng có GIL riêng. (Xem :ref:`isolating-extensions-howto`.)

   Slot này xác định việc import module này trong một subinterpreter có thất bại hay không.

   Không được chỉ định nhiều khe ``Py_mod_multiple_interpreters`` trong một định nghĩa module.

   Nếu không chỉ định ``Py_mod_multiple_interpreters``, cơ chế import sẽ mặc định dùng ``Py_MOD_MULTIPLE_INTERPRETERS_SUPPORTED``.

   .. versionadded:: 3.12

.. c:macro:: Py_mod_gil

   Chỉ định một trong các giá trị sau:

   .. c:namespace:: NULL

   .. c:macro:: Py_MOD_GIL_USED

      Module này phụ thuộc vào sự hiện diện của global interpreter lock (GIL) và có thể truy cập trạng thái toàn cục mà không cần đồng bộ hóa.

   .. c:macro:: Py_MOD_GIL_NOT_USED

      Module này có thể chạy an toàn mà không cần GIL đang hoạt động.

   Khe này bị các bản build Python không được cấu hình với bỏ qua
   :option:`--disable-gil`. Nếu không, khe này xác định việc import module này có khiến GIL tự động được bật hay không. Xem
   :ref:`whatsnew313-free-threaded-cpython` để biết thêm chi tiết.

   Không được chỉ định nhiều ``Py_mod_gil`` trong một định nghĩa module.

   Nếu ``Py_mod_gil`` không được chỉ định, cơ chế import sẽ mặc định sử dụng ``Py_MOD_GIL_USED``.

   .. versionadded:: 3.13


.. _moduledef-dynamic:

Tạo module extension một cách động
----------------------------------

Có thể sử dụng các hàm sau để tạo một module bên ngoài :ref:`hàm khởi tạo <extension-export-hook>` của extension. Chúng cũng được sử dụng trong
:ref:`khởi tạo một pha <single-phase-initialization>`.

.. c:function:: PyObject* PyModule_Create(PyModuleDef *def)

   Tạo một đối tượng module mới dựa trên định nghĩa trong *def*. Đây là một macro gọi :c:func:`PyModule_Create2` với *module_api_version* được đặt thành :c:macro:`PYTHON_API_VERSION`, hoặc thành :c:macro:`PYTHON_ABI_VERSION` nếu sử dụng
   :ref:`limited API <limited-c-api>`.

.. c:function:: PyObject* PyModule_Create2(PyModuleDef *def, int module_api_version)

   Tạo một đối tượng module mới dựa trên định nghĩa trong *def*, với giả định phiên bản API là *module_api_version*. Nếu phiên bản đó không khớp với phiên bản của interpreter đang chạy, một :exc:`RuntimeWarning` sẽ được phát ra.

   Trả về ``NULL`` với một ngoại lệ được thiết lập khi xảy ra lỗi.

   Hàm này không hỗ trợ slots. Thành viên :c:member:`~PyModuleDef.m_slots` của *def* phải là ``NULL``.


   .. note::

      Hầu hết các trường hợp sử dụng hàm này nên sử dụng :c:func:`PyModule_Create` thay vào đó; chỉ sử dụng hàm này nếu bạn chắc chắn mình cần nó.

.. c:function:: PyObject * PyModule_FromDefAndSpec(PyModuleDef *def, PyObject *spec)

   Macro này gọi :c:func:`PyModule_FromDefAndSpec2` với *module_api_version* được đặt thành :c:macro:`PYTHON_API_VERSION`, hoặc thành :c:macro:`PYTHON_ABI_VERSION` nếu sử dụng
   :ref:`limited API <limited-c-api>`.

   .. versionadded:: 3.5

.. c:function:: PyObject * PyModule_FromDefAndSpec2(PyModuleDef *def, PyObject *spec, int module_api_version)

   Tạo một đối tượng module mới dựa trên định nghĩa trong *def* và ModuleSpec *spec*, với giả định phiên bản API là *module_api_version*. Nếu phiên bản đó không khớp với phiên bản của interpreter đang chạy, một :exc:`RuntimeWarning` sẽ được phát ra.

   Trả về ``NULL`` với một ngoại lệ được thiết lập khi xảy ra lỗi.

   Lưu ý rằng thao tác này không xử lý các execution slot (:c:data:`Py_mod_exec`). Phải gọi cả ``PyModule_FromDefAndSpec`` và ``PyModule_ExecDef`` để khởi tạo đầy đủ một module.

   .. note::

      Hầu hết trường hợp sử dụng hàm này nên dùng :c:func:`PyModule_FromDefAndSpec` thay thế; chỉ sử dụng hàm này nếu bạn chắc chắn mình cần đến nó.

   .. versionadded:: 3.5

.. c:function:: int PyModule_ExecDef(PyObject *module, PyModuleDef *def)

   Xử lý mọi execution slot (:c:data:`Py_mod_exec`) được cung cấp trong *def*.

   .. versionadded:: 3.5

.. c:macro:: PYTHON_API_VERSION

   Phiên bản C API. Được định nghĩa để duy trì khả năng tương thích ngược.

   Hiện tại, hằng số này không được cập nhật trong các phiên bản Python mới và không hữu ích cho việc quản lý phiên bản. Điều này có thể thay đổi trong tương lai.

.. c:macro:: PYTHON_ABI_VERSION

   Được định nghĩa là ``3`` để đảm bảo khả năng tương thích ngược.

   Hiện tại, hằng số này không được cập nhật trong các phiên bản Python mới và không hữu ích cho việc quản lý phiên bản. Điều này có thể thay đổi trong tương lai.


Các hàm hỗ trợ
--------------

Các hàm sau đây được cung cấp để giúp khởi tạo trạng thái module. Chúng предназначены cho các execution slot của module (:c:data:`Py_mod_exec`), hàm khởi tạo cho :ref:`single-phase initialization <single-phase-initialization>` cũ hoặc mã tạo module một cách động.

.. c:function:: int PyModule_AddObjectRef(PyObject *module, const char *name, PyObject *value)

   Thêm một đối tượng vào *module* với tên *name*. Đây là một hàm tiện ích có thể được sử dụng từ hàm khởi tạo của module.

   Khi thành công, trả về ``0``. Khi có lỗi, phát sinh một ngoại lệ và trả về ``-1``.

   Ví dụ sử dụng::

       static int
       add_spam(PyObject *module, int value)
       {
           PyObject *obj = PyLong_FromLong(value);
           if (obj == NULL) {
               return -1;
           }
           int res = PyModule_AddObjectRef(module, "spam", obj);
           Py_DECREF(obj);
           return res;
        }

   Để thuận tiện, hàm chấp nhận ``NULL`` *value* cùng với một exception set. Trong trường hợp này, hãy trả về ``-1`` và chỉ giữ nguyên exception đã được raise.

   Ví dụ này cũng có thể được viết mà không cần kiểm tra một cách tường minh xem *obj* có phải là ``NULL`` hay không.::

       static int
       add_spam(PyObject *module, int value)
       {
           PyObject *obj = PyLong_FromLong(value);
           int res = PyModule_AddObjectRef(module, "spam", obj);
           Py_XDECREF(obj);
           return res;
        }

   Lưu ý rằng nên sử dụng ``Py_XDECREF()`` thay vì ``Py_DECREF()`` trong trường hợp này, vì *obj* có thể là ``NULL``.

   Nên giữ số lượng các chuỗi *name* khác nhau được truyền cho hàm này ở mức nhỏ, thường bằng cách chỉ sử dụng các chuỗi được cấp phát tĩnh làm *name*. Đối với những tên không được biết tại thời điểm biên dịch, nên gọi
   :c:func:`PyUnicode_FromString` và :c:func:`PyObject_SetAttr` trực tiếp. Để biết thêm chi tiết, hãy xem :c:func:`PyUnicode_InternFromString`, có thể được sử dụng nội bộ để tạo một key object.

   .. versionadded:: 3.10


.. c:function:: int PyModule_Add(PyObject *module, const char *name, PyObject *value)

   Tương tự như :c:func:`PyModule_AddObjectRef`, nhưng ":term:`steals <steal>`" một reference đến *value* (kể cả khi xảy ra lỗi). Có thể gọi hàm này với kết quả của một hàm trả về một new reference mà không cần kiểm tra kết quả hoặc thậm chí lưu kết quả đó vào một biến.

   Ví dụ sử dụng::

        if (PyModule_Add(module, "spam", PyBytes_FromString(value)) < 0) {
            goto error;
        }

   .. versionadded:: 3.13


.. c:function:: int PyModule_AddObject(PyObject *module, const char *name, PyObject *value)

   Tương tự như :c:func:`PyModule_AddObjectRef`, nhưng :term:`chiếm <steal>` một tham chiếu đến *giá trị* khi thành công (nếu nó trả về ``0``).

   Các hàm mới :c:func:`PyModule_Add` hoặc :c:func:`PyModule_AddObjectRef` được khuyến nghị, vì rất dễ gây rò rỉ tham chiếu do sử dụng sai
   hàm :c:func:`PyModule_AddObject`.

   .. note::

      Không giống các hàm khác chiếm tham chiếu, ``PyModule_AddObject()`` chỉ giải phóng tham chiếu đến *giá trị* **khi thành công**.

      Điều này có nghĩa là phải kiểm tra giá trị trả về của nó, và mã gọi phải
      :c:func:`Py_XDECREF` *value* theo cách thủ công khi có lỗi.

   Ví dụ sử dụng::

        PyObject *obj = PyBytes_FromString(value);
        if (PyModule_AddObject(module, "spam", obj) < 0) {
            // If 'obj' is not NULL and PyModule_AddObject() failed,
            // 'obj' strong reference must be deleted with Py_XDECREF().
            // If 'obj' is NULL, Py_XDECREF() does nothing.
            Py_XDECREF(obj);
            goto error;
        }
        // PyModule_AddObject() stole a reference to obj:
        // Py_XDECREF(obj) is not needed here.

   .. soft-deprecated:: 3.13


.. c:function:: int PyModule_AddIntConstant(PyObject *module, const char *name, long value)

   Thêm một hằng số nguyên vào *module* với tên *name*. Hàm tiện ích này có thể được sử dụng từ hàm khởi tạo của module. Trả về ``-1`` khi có ngoại lệ được thiết lập do lỗi, và ``0`` khi thành công.

   Đây là một hàm tiện ích gọi :c:func:`PyLong_FromLong` và
   :c:func:`PyModule_AddObjectRef`; xem tài liệu của chúng để biết chi tiết.


.. c:function:: int PyModule_AddStringConstant(PyObject *module, const char *name, const char *value)

   Thêm một hằng số chuỗi vào *module* với tên *name*. Hàm tiện ích này có thể được sử dụng từ hàm khởi tạo của module. Chuỗi *value* phải được kết thúc bằng ``NULL``. Trả về ``-1`` khi có ngoại lệ được thiết lập do lỗi, và ``0`` khi thành công.

   Đây là một hàm tiện ích gọi
   :c:func:`PyUnicode_InternFromString` và :c:func:`PyModule_AddObjectRef`; xem tài liệu của chúng để biết chi tiết.


.. c:macro:: PyModule_AddIntMacro(module, macro)

   Thêm một hằng số int vào *module*. Tên và giá trị được lấy từ *macro*. Ví dụ, ``PyModule_AddIntMacro(module, AF_INET)`` thêm hằng số int *AF_INET* với giá trị *AF_INET* vào *module*. Trả về ``-1`` khi có ngoại lệ được thiết lập do lỗi, và ``0`` khi thành công.


.. c:macro:: PyModule_AddStringMacro(module, macro)

   Thêm một hằng số chuỗi vào *mô-đun*.

.. c:function:: int PyModule_AddType(PyObject *module, PyTypeObject *type)

   Thêm một đối tượng kiểu vào *mô-đun*. Đối tượng kiểu được hoàn tất bằng cách gọi nội bộ :c:func:`PyType_Ready`. Tên của đối tượng kiểu được lấy từ thành phần cuối cùng của
   :c:member:`~PyTypeObject.tp_name` sau dấu chấm. Trả về ``-1`` với một exception được thiết lập khi xảy ra lỗi, và ``0`` khi thành công.

   .. versionadded:: 3.9

.. c:function:: int PyModule_AddFunctions(PyObject *module, PyMethodDef *functions)

   Thêm các hàm từ mảng ``NULL`` được kết thúc bằng *hàm* vào *mô-đun*. Hãy tham khảo tài liệu :c:type:`PyMethodDef` để biết chi tiết về từng mục (do không có namespace mô-đun dùng chung, các "hàm" cấp mô-đun được triển khai bằng C thường nhận mô-đun làm tham số đầu tiên, khiến chúng tương tự các phương thức instance trên các lớp Python).

   Hàm này được tự động gọi khi tạo một mô-đun từ ``PyModuleDef`` (chẳng hạn khi sử dụng :ref:`multi-phase-initialization`, ``PyModule_Create`` hoặc ``PyModule_FromDefAndSpec``). Một số tác giả mô-đun có thể muốn định nghĩa các hàm trong nhiều
   mảng :c:type:`PyMethodDef`; trong trường hợp đó, họ nên gọi trực tiếp hàm này.

   Mảng *hàm* phải được cấp phát tĩnh (hoặc được đảm bảo bằng cách khác là tồn tại lâu hơn đối tượng mô-đun).

   .. versionadded:: 3.5

.. c:function:: int PyModule_SetDocString(PyObject *module, const char *docstring)

   Đặt docstring cho *mô-đun* thành *docstring*. Hàm này được tự động gọi khi tạo một mô-đun từ ``PyModuleDef`` (chẳng hạn như khi sử dụng :ref:`multi-phase-initialization`, ``PyModule_Create`` hoặc ``PyModule_FromDefAndSpec``).

   Trả về ``0`` khi thành công. Trả về ``-1`` với một ngoại lệ được thiết lập khi xảy ra lỗi.

   .. versionadded:: 3.5

.. c:function:: int PyUnstable_Module_SetGIL(PyObject *module, void *gil)

   Cho biết *mô-đun* có hoặc không hỗ trợ chạy mà không cần khóa trình thông dịch toàn cục (GIL), bằng một trong các giá trị từ
   :c:macro:`Py_mod_gil`. Phải gọi hàm này trong hàm khởi tạo của *mô-đun* khi sử dụng :ref:`single-phase-initialization`. Nếu không gọi hàm này trong quá trình khởi tạo mô-đun, cơ chế nhập mô-đun sẽ giả định rằng mô-đun không hỗ trợ chạy mà không cần GIL. Hàm này chỉ khả dụng trong các bản dựng Python được cấu hình với
   :option:`--disable-gil`. Trả về ``-1`` với một ngoại lệ được thiết lập khi xảy ra lỗi, ``0`` khi thành công.

   .. versionadded:: 3.13


Tra cứu mô-đun (khởi tạo một giai đoạn)
.......................................

Sơ đồ khởi tạo :ref:`khởi tạo một giai đoạn <single-phase-initialization>` kế thừa tạo ra các mô-đun singleton có thể được tra cứu trong ngữ cảnh của trình thông dịch hiện tại. Điều này cho phép truy xuất đối tượng mô-đun về sau chỉ bằng một tham chiếu đến định nghĩa mô-đun.

Các hàm này sẽ không hoạt động trên những module được tạo bằng cơ chế khởi tạo nhiều pha, vì có thể tạo nhiều module như vậy từ cùng một định nghĩa.

.. c:function:: PyObject* PyState_FindModule(PyModuleDef *def)

   Trả về đối tượng module được tạo từ *def* cho trình thông dịch hiện tại. Phương thức này yêu cầu đối tượng module đã được gắn vào trạng thái của trình thông dịch bằng
   :c:func:`PyState_AddModule` trước đó. Nếu không tìm thấy đối tượng module tương ứng hoặc đối tượng này chưa được gắn vào trạng thái của trình thông dịch, hàm sẽ trả về ``NULL``.

.. c:function:: int PyState_AddModule(PyObject *module, PyModuleDef *def)

   Gắn đối tượng module được truyền vào hàm vào trạng thái của trình thông dịch. Điều này cho phép truy cập đối tượng module thông qua :c:func:`PyState_FindModule`.

   Chỉ có hiệu lực trên các module được tạo bằng cơ chế khởi tạo một pha.

   Python tự động gọi ``PyState_AddModule`` sau khi import một module sử dụng cơ chế :ref:`khởi tạo một pha <single-phase-initialization>`, vì vậy không cần (nhưng cũng không gây hại) gọi hàm này từ mã khởi tạo module. Chỉ cần gọi tường minh nếu mã khởi tạo của chính module đó tiếp tục gọi ``PyState_FindModule``. Hàm này chủ yếu được dùng để triển khai các cơ chế import thay thế (bằng cách gọi trực tiếp hàm này hoặc tham khảo phần triển khai của nó để biết chi tiết về các cập nhật trạng thái cần thiết).

   Nếu một module trước đó đã được gắn bằng cùng *def*, module đó sẽ được thay thế bằng *module* mới.

   Caller phải có một :term:`attached thread state`.

   Trả về ``-1`` với một exception được thiết lập khi xảy ra lỗi, và ``0`` khi thành công.

   .. versionadded:: 3.3

.. c:function:: int PyState_RemoveModule(PyModuleDef *def)

   Xóa đối tượng module được tạo từ *def* khỏi trạng thái của interpreter. Trả về ``-1`` với một exception được thiết lập khi xảy ra lỗi, và ``0`` khi thành công.

   Caller phải có một :term:`attached thread state`.

   .. versionadded:: 3.3
