.. highlight:: c

.. _importing:

Nhập module
===========


.. c:function:: PyObject* PyImport_ImportModule(const char *name)

   .. index::
      single: package variable; __all__
      single: __all__ (package variable)
      single: modules (in module sys)

   Đây là một wrapper cho :c:func:`PyImport_Import()`, nhận một
   :c:expr:`const char *` làm đối số thay vì một :c:expr:`PyObject *`.

.. c:function:: PyObject* PyImport_ImportModuleNoBlock(const char *name)

   Hàm này là bí danh không còn được khuyến nghị dùng của :c:func:`PyImport_ImportModule`.

   .. versionchanged:: 3.3
      Trước đây, hàm này sẽ thất bại ngay lập tức khi một thread khác đang giữ import lock. Tuy nhiên, trong Python 3.3, cơ chế khóa đã chuyển sang dùng khóa theo từng module cho hầu hết các mục đích, vì vậy hành vi đặc biệt của hàm này không còn cần thiết nữa.

   .. deprecated-removed:: 3.13 3.15
      Thay vào đó, hãy dùng :c:func:`PyImport_ImportModule`.


.. c:function:: PyObject* PyImport_ImportModuleEx(const char *name, PyObject *globals, PyObject *locals, PyObject *fromlist)

   .. index:: pair: built-in function; __import__

   Nhập một module. Cách mô tả phù hợp nhất là tham chiếu đến hàm Python tích hợp sẵn :func:`__import__`.

   Giá trị trả về là một tham chiếu mới đến module đã nhập hoặc package cấp cao nhất, hoặc ``NULL`` khi việc nhập không thành công và một ngoại lệ được thiết lập. Tương tự như đối với
   :func:`__import__`, khi yêu cầu một submodule của package, giá trị trả về thường là package cấp cao nhất, trừ khi cung cấp *fromlist* không rỗng.

   Các lần nhập không thành công sẽ loại bỏ những đối tượng module chưa hoàn chỉnh, tương tự như với
   :c:func:`PyImport_ImportModule`.


.. c:function:: PyObject* PyImport_ImportModuleLevelObject(PyObject *name, PyObject *globals, PyObject *locals, PyObject *fromlist, int level)

   Nhập một module. Cách mô tả rõ nhất là tham chiếu đến hàm Python tích hợp sẵn :func:`__import__`, vì hàm :func:`__import__` chuẩn gọi trực tiếp hàm này.

   Giá trị trả về là một tham chiếu mới đến module đã nhập hoặc package cấp cao nhất, hoặc ``NULL`` khi việc nhập không thành công và một ngoại lệ được thiết lập. Tương tự như đối với :func:`__import__`, khi yêu cầu một submodule của package, giá trị trả về thường là package cấp cao nhất, trừ khi cung cấp *fromlist* không rỗng.

   .. versionadded:: 3.3


.. c:function:: PyObject* PyImport_ImportModuleLevel(const char *name, PyObject *globals, PyObject *locals, PyObject *fromlist, int level)

   Tương tự như :c:func:`PyImport_ImportModuleLevelObject`, nhưng tên là một chuỗi được mã hóa UTF-8 thay vì một đối tượng Unicode.

   .. versionchanged:: 3.3
         Các giá trị âm cho *level* không còn được chấp nhận.

.. c:function:: PyObject* PyImport_Import(PyObject *name)

   Đây là một giao diện cấp cao hơn, gọi "hàm import hook" hiện tại (với *level* rõ ràng là 0, nghĩa là import tuyệt đối). Hàm này gọi hàm :func:`__import__` từ ``__builtins__`` của các biến toàn cục hiện tại. Điều này có nghĩa là thao tác import được thực hiện bằng bất kỳ import hook nào đang được cài đặt trong môi trường hiện tại.

   Hàm này luôn sử dụng import tuyệt đối.


.. c:function:: PyObject* PyImport_ReloadModule(PyObject *m)

   Tải lại một module. Trả về một tham chiếu mới đến module đã được tải lại hoặc ``NULL`` kèm theo một exception được thiết lập nếu xảy ra lỗi (trong trường hợp này, module vẫn tồn tại).


.. c:function:: PyObject* PyImport_AddModuleRef(const char *name)

   Trả về đối tượng module tương ứng với tên module.

   Đối số *name* có thể có dạng ``package.module``. Trước tiên, hãy kiểm tra từ điển modules nếu đã có module ở đó; nếu chưa có, hãy tạo một module mới và chèn nó vào từ điển modules.

   Trả về một :term:`strong reference` đến module nếu thành công. Trả về ``NULL`` kèm theo một exception được thiết lập nếu xảy ra lỗi.

   Tên module *name* được giải mã từ UTF-8.

   Hàm này không tải hoặc import module; nếu module chưa được tải trước đó, bạn sẽ nhận được một đối tượng module rỗng. Sử dụng
   :c:func:`PyImport_ImportModule` hoặc một trong các biến thể của nó để import module. Các cấu trúc package được ngụ ý bởi một tên có dấu chấm cho *name* sẽ không được tạo nếu chưa tồn tại.

   .. versionadded:: 3.13


.. c:function:: PyObject* PyImport_AddModuleObject(PyObject *name)

   Tương tự như :c:func:`PyImport_AddModuleRef`, nhưng trả về một :term:`borrowed reference` và *name* là một đối tượng :class:`str` của Python.

   .. versionadded:: 3.3


.. c:function:: PyObject* PyImport_AddModule(const char *name)

   Tương tự như :c:func:`PyImport_AddModuleRef`, nhưng trả về một :term:`borrowed reference`.


.. c:function:: PyObject* PyImport_ExecCodeModule(const char *name, PyObject *co)

   .. index:: pair: built-in function; compile

   Với một tên module (có thể có dạng ``package.module``) và một đối tượng mã được đọc từ tệp bytecode Python hoặc nhận được từ hàm dựng sẵn
   :func:`compile`, tải module. Trả về một tham chiếu mới đến đối tượng module hoặc ``NULL`` với một ngoại lệ đã được thiết lập nếu xảy ra lỗi. *name* sẽ bị xóa khỏi :data:`sys.modules` trong các trường hợp lỗi, ngay cả khi *name* đã có trong :data:`sys.modules` khi bắt đầu :c:func:`PyImport_ExecCodeModule`. Việc để lại các module được khởi tạo chưa hoàn chỉnh trong :data:`sys.modules` rất nguy hiểm, vì các lần import những module như vậy không có cách nào biết rằng đối tượng module đang ở trạng thái không xác định (và có thể đã bị hỏng so với ý định của tác giả module).

   :attr:`~module.__spec__` và :attr:`~module.__loader__` của module sẽ được thiết lập, nếu chưa được thiết lập, với các giá trị thích hợp. Loader của spec sẽ được đặt thành :attr:`!__loader__` của module (nếu đã được thiết lập) và thành một instance của :class:`~importlib.machinery.SourceFileLoader` trong trường hợp ngược lại.

   Thuộc tính :attr:`~module.__file__` của module sẽ được đặt thành :attr:`~codeobject.co_filename` của đối tượng mã. Nếu phù hợp,
   :attr:`~module.__cached__` cũng sẽ được đặt.

   Hàm này sẽ tải lại module nếu module đó đã được import. Xem
   :c:func:`PyImport_ReloadModule` để biết cách dự kiến dùng để tải lại module.

   Nếu *name* trỏ đến một tên có dấu chấm theo dạng ``package.module``, mọi cấu trúc package chưa được tạo sẽ vẫn không được tạo.

   Xem thêm :c:func:`PyImport_ExecCodeModuleEx` và
   :c:func:`PyImport_ExecCodeModuleWithPathnames`.

   .. versionchanged:: 3.12
      Việc thiết lập :attr:`~module.__cached__` và :attr:`~module.__loader__` không còn được khuyến nghị. Xem :class:`~importlib.machinery.ModuleSpec` để biết các phương án thay thế.


.. c:function:: PyObject* PyImport_ExecCodeModuleEx(const char *name, PyObject *co, const char *pathname)

   Giống như :c:func:`PyImport_ExecCodeModule`, nhưng thuộc tính :attr:`~module.__file__` của đối tượng module được đặt thành *pathname* nếu nó không phải là ``NULL``.

   Xem thêm :c:func:`PyImport_ExecCodeModuleWithPathnames`.


.. c:function:: PyObject* PyImport_ExecCodeModuleObject(PyObject *name, PyObject *co, PyObject *pathname, PyObject *cpathname)

   Giống như :c:func:`PyImport_ExecCodeModuleEx`, nhưng thuộc tính :attr:`~module.__cached__` của đối tượng module được đặt thành *cpathname* nếu nó không phải là ``NULL``. Trong ba hàm này, đây là hàm được khuyến nghị sử dụng.

   .. versionadded:: 3.3

   .. versionchanged:: 3.12
      Việc đặt :attr:`~module.__cached__` không còn được khuyến nghị. Xem
      :class:`~importlib.machinery.ModuleSpec` để biết các lựa chọn thay thế.


.. c:function:: PyObject* PyImport_ExecCodeModuleWithPathnames(const char *name, PyObject *co, const char *pathname, const char *cpathname)

   Giống như :c:func:`PyImport_ExecCodeModuleObject`, nhưng *name*, *pathname* và *cpathname* là các chuỗi được mã hóa UTF-8. Đồng thời, hệ thống cũng cố gắng xác định giá trị của *pathname* từ *cpathname* nếu giá trị trước được đặt thành ``NULL``.

   .. versionadded:: 3.2
   .. versionchanged:: 3.3
      Sử dụng :func:`!imp.source_from_cache` khi tính đường dẫn nguồn nếu chỉ cung cấp đường dẫn bytecode.
   .. versionchanged:: 3.12
      Không còn sử dụng module :mod:`!imp` đã bị loại bỏ.


.. c:function:: long PyImport_GetMagicNumber()

   Trả về số magic cho các tệp bytecode Python (còn gọi là tệp :file:`.pyc`). Số magic phải có trong bốn byte đầu tiên của tệp bytecode, theo thứ tự byte little-endian. Trả về ``-1`` nếu có lỗi.

   .. versionchanged:: 3.3
      Giá trị trả về của ``-1`` khi thất bại.


.. c:function:: const char * PyImport_GetMagicTag()

   Trả về chuỗi thẻ magic cho tên tệp bytecode Python định dạng :pep:`3147`. Hãy lưu ý rằng giá trị tại ``sys.implementation.cache_tag`` là giá trị có thẩm quyền và nên được sử dụng thay cho hàm này.

   .. versionadded:: 3.2

.. c:function:: PyObject* PyImport_GetModuleDict()

   Trả về từ điển được sử dụng để quản lý module (còn gọi là ``sys.modules``). Lưu ý rằng đây là một biến riêng của từng interpreter.

.. c:function:: PyObject* PyImport_GetModule(PyObject *name)

   Trả về module đã được import với tên đã cho. Nếu module chưa được import thì trả về ``NULL`` nhưng không thiết lập lỗi. Trả về ``NULL`` và thiết lập lỗi nếu việc tra cứu thất bại.

   .. versionadded:: 3.7

.. c:function:: PyObject* PyImport_GetImporter(PyObject *path)

   Trả về một đối tượng finder cho mục :data:`sys.path`/:attr:`!pkg.__path__` *path*, có thể bằng cách lấy đối tượng đó từ dict :data:`sys.path_importer_cache`. Nếu mục này chưa được lưu vào bộ nhớ đệm, duyệt qua :data:`sys.path_hooks` cho đến khi tìm thấy một hook có thể xử lý mục đường dẫn. Trả về ``None`` nếu không tìm thấy hook nào; điều này cho caller biết rằng :term:`path based finder` không thể tìm thấy finder cho mục đường dẫn này. Lưu kết quả vào :data:`sys.path_importer_cache`. Trả về một tham chiếu mới đến đối tượng finder.


.. c:function:: int PyImport_ImportFrozenModuleObject(PyObject *name)

   Tải một frozen module có tên *name*. Trả về ``1`` nếu thành công, ``0`` nếu không tìm thấy module và ``-1`` cùng với một exception được thiết lập nếu quá trình khởi tạo thất bại. Để truy cập module đã import sau khi tải thành công, hãy sử dụng
   :c:func:`PyImport_ImportModule`. (Lưu ý tên gọi không chính xác --- hàm này sẽ tải lại module nếu module đó đã được import.)

   .. versionadded:: 3.3

   .. versionchanged:: 3.4
      Thuộc tính ``__file__`` không còn được thiết lập trên module.


.. c:function:: int PyImport_ImportFrozenModule(const char *name)

   Tương tự như :c:func:`PyImport_ImportFrozenModuleObject`, nhưng tên là một chuỗi được mã hóa UTF-8 thay vì một đối tượng Unicode.


.. c:struct:: _frozen

   .. index:: single: freeze utility

   Đây là định nghĩa kiểu cấu trúc cho các bộ mô tả frozen module, được tạo bởi tiện ích :program:`freeze` (xem :file:`Tools/freeze/` trong bản phân phối mã nguồn Python). Định nghĩa của nó, nằm trong :file:`Include/import.h`, là::

      struct _frozen {
          const char *name;
          const unsigned char *code;
          int size;
          bool is_package;
      };

   .. versionchanged:: 3.11
      Trường ``is_package`` mới cho biết module có phải là package hay không. Trường này thay thế cho việc đặt trường ``size`` thành một giá trị âm.

.. c:var:: const struct _frozen* PyImport_FrozenModules

   Con trỏ này được khởi tạo để trỏ đến một mảng gồm các bản ghi :c:struct:`_frozen`, kết thúc bằng một bản ghi có tất cả các thành viên là ``NULL`` hoặc bằng không. Khi một frozen module được import, module đó sẽ được tìm kiếm trong bảng này. Mã của bên thứ ba có thể tận dụng điều này để cung cấp một tập hợp frozen module được tạo động.


.. c:function:: int PyImport_AppendInittab(const char *name, PyObject* (*initfunc)(void))

   Thêm một module duy nhất vào bảng các module tích hợp sẵn hiện có. Đây là một wrapper tiện lợi quanh :c:func:`PyImport_ExtendInittab`, trả về ``-1`` nếu không thể mở rộng bảng. Module mới có thể được import bằng tên *name*, và sử dụng hàm *initfunc* làm hàm khởi tạo được gọi trong lần import đầu tiên. Việc này nên được gọi trước
   :c:func:`Py_Initialize`.


.. c:struct:: _inittab

   Cấu trúc mô tả một mục duy nhất trong danh sách các module tích hợp sẵn. Các chương trình nhúng Python có thể sử dụng một mảng gồm các cấu trúc này kết hợp với
   :c:func:`PyImport_ExtendInittab` để cung cấp thêm các module tích hợp sẵn. Cấu trúc gồm hai thành viên:

   .. c:member:: const char *name

      Tên module, dưới dạng chuỗi được mã hóa ASCII.

   .. c:member:: PyObject* (*initfunc)(void)

      Hàm khởi tạo cho một module được tích hợp vào trình thông dịch.


.. c:function:: int PyImport_ExtendInittab(struct _inittab *newtab)

   Thêm một tập hợp module vào bảng các module tích hợp sẵn. Mảng *newtab* phải kết thúc bằng một mục sentinel chứa ``NULL`` cho trường :c:member:`~_inittab.name`; nếu không cung cấp giá trị sentinel, có thể xảy ra lỗi bộ nhớ. Trả về ``0`` khi thành công hoặc ``-1`` nếu không thể cấp phát đủ bộ nhớ để mở rộng bảng nội bộ. Nếu xảy ra lỗi, không module nào được thêm vào bảng nội bộ. Việc này phải được gọi trước :c:func:`Py_Initialize`.

   Nếu Python được khởi tạo nhiều lần, :c:func:`PyImport_AppendInittab` hoặc
   :c:func:`PyImport_ExtendInittab` phải được gọi trước mỗi lần khởi tạo Python.


.. c:var:: struct _inittab *PyImport_Inittab

   Bảng các module tích hợp được Python sử dụng khi khởi tạo. Không sử dụng trực tiếp bảng này; thay vào đó, hãy sử dụng :c:func:`PyImport_AppendInittab` và :c:func:`PyImport_ExtendInittab`.


.. c:function:: PyObject* PyImport_ImportModuleAttr(PyObject *mod_name, PyObject *attr_name)

   Import module *mod_name* và lấy thuộc tính *attr_name* của module đó.

   Tên phải là các đối tượng :class:`str` của Python.

   Hàm trợ giúp kết hợp :c:func:`PyImport_Import` và
   :c:func:`PyObject_GetAttr`. Ví dụ: hàm này có thể phát sinh :exc:`ImportError` nếu không tìm thấy module và :exc:`AttributeError` nếu thuộc tính không tồn tại.

   .. versionadded:: 3.14

.. c:function:: PyObject* PyImport_ImportModuleAttrString(const char *mod_name, const char *attr_name)

   Tương tự :c:func:`PyImport_ImportModuleAttr`, nhưng tên là các chuỗi được mã hóa UTF-8 thay vì các đối tượng :class:`str` của Python.

   .. versionadded:: 3.14
