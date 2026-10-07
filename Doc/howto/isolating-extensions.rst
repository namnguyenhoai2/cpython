.. highlight:: c

.. _isolating-extensions-howto:

*************************
Cô lập các mô-đun mở rộng
*************************

.. topic:: Tóm tắt

    Theo truyền thống, trạng thái thuộc về các mô-đun mở rộng Python được lưu trong các biến ``static`` của C, vốn có phạm vi trên toàn bộ tiến trình. Tài liệu này mô tả các vấn đề của trạng thái theo từng tiến trình như vậy và trình bày một cách an toàn hơn: trạng thái theo từng mô-đun.

    Tài liệu cũng mô tả cách chuyển sang trạng thái theo từng mô-đun ở những nơi có thể. Quá trình chuyển đổi này bao gồm việc cấp phát không gian cho trạng thái đó, có thể chuyển từ các kiểu static sang các kiểu heap và—có lẽ quan trọng nhất—truy cập trạng thái theo từng mô-đun từ mã.


Ai nên đọc tài liệu này
=======================

Hướng dẫn này dành cho những người duy trì các phần mở rộng :ref:`C-API <c-api-index>` muốn làm cho phần mở rộng đó an toàn hơn khi sử dụng trong các ứng dụng mà bản thân Python được dùng như một thư viện.


Bối cảnh
========

Một *interpreter* là ngữ cảnh trong đó mã Python chạy. Nó chứa cấu hình (ví dụ: đường dẫn import) và trạng thái runtime (ví dụ: tập hợp các module đã import).

Python hỗ trợ chạy nhiều interpreter trong cùng một process. Có hai trường hợp cần xem xét—người dùng có thể chạy các interpreter:

-  theo tuần tự, với nhiều chu kỳ :c:func:`Py_InitializeEx`/:c:func:`Py_FinalizeEx`, và
-  song song, bằng cách quản lý các "sub-interpreter" sử dụng
   :c:func:`Py_NewInterpreter`/:c:func:`Py_EndInterpreter`.

Cả hai trường hợp (và sự kết hợp của chúng) sẽ hữu ích nhất khi nhúng Python vào một thư viện. Các thư viện thường không nên đưa ra giả định về ứng dụng sử dụng chúng, trong đó có giả định về một "main Python interpreter" trên toàn process.

Trong lịch sử, các module mở rộng Python không xử lý tốt trường hợp sử dụng này. Nhiều module mở rộng (và thậm chí một số module stdlib) sử dụng trạng thái global *per-process*, vì các biến C ``static`` cực kỳ dễ sử dụng. Do đó, dữ liệu lẽ ra phải dành riêng cho một interpreter lại trở thành dữ liệu được chia sẻ giữa các interpreter. Nếu nhà phát triển module mở rộng không cẩn thận, rất dễ phát sinh các trường hợp biên dẫn đến sự cố khi một module được tải trong nhiều interpreter thuộc cùng một process.

Đáng tiếc là không dễ đạt được trạng thái *per-interpreter*. Các tác giả module mở rộng thường không lưu ý đến việc có nhiều interpreter khi phát triển, và hiện tại việc kiểm thử hành vi này khá cồng kềnh.

Chuyển sang trạng thái theo mô-đun
----------------------------------

Thay vì tập trung vào trạng thái theo interpreter, Python's C API đang phát triển để hỗ trợ tốt hơn trạng thái *theo mô-đun* với mức độ chi tiết hơn. Điều này có nghĩa là dữ liệu ở cấp C nên được gắn vào một *đối tượng mô-đun*. Mỗi interpreter tạo đối tượng mô-đun riêng, giữ cho dữ liệu được tách biệt. Để kiểm thử khả năng cô lập, thậm chí có thể tải nhiều đối tượng mô-đun tương ứng với một extension duy nhất trong cùng một interpreter.

Trạng thái theo mô-đun cung cấp một cách dễ dàng để hình dung về vòng đời và quyền sở hữu tài nguyên: mô-đun extension sẽ được khởi tạo khi một đối tượng mô-đun được tạo và dọn dẹp khi đối tượng đó được giải phóng. Về khía cạnh này, một mô-đun cũng giống như bất kỳ :c:expr:`PyObject *` nào khác; không có hook "khi interpreter tắt" nào cần phải ghi nhớ—hoặc quên mất.

Lưu ý rằng có những trường hợp sử dụng các loại "biến toàn cục" khác nhau: trạng thái theo process, theo interpreter, theo thread hoặc theo task. Với trạng thái theo mô-đun làm mặc định, các loại trạng thái này vẫn khả thi, nhưng bạn nên xem chúng là những trường hợp ngoại lệ: nếu cần sử dụng, bạn nên đặc biệt cẩn trọng và kiểm thử thêm. (Lưu ý rằng hướng dẫn này không đề cập đến chúng.)


Các đối tượng mô-đun biệt lập
-----------------------------

Điểm chính cần ghi nhớ khi phát triển một mô-đun extension là có thể tạo nhiều đối tượng mô-đun từ một shared library duy nhất. Ví dụ:

.. code-block:: pycon

   >>> import sys
   >>> import binascii
   >>> old_binascii = binascii
   >>> del sys.modules['binascii']
   >>> import binascii  # tạo một đối tượng mô-đun mới
   >>> old_binascii == binascii
   False

Theo nguyên tắc chung, hai module nên hoàn toàn độc lập. Tất cả đối tượng và trạng thái dành riêng cho module nên được đóng gói trong đối tượng module, không được dùng chung với các đối tượng module khác, và được dọn dẹp khi đối tượng module được giải phóng. Vì đây chỉ là nguyên tắc chung, vẫn có thể có ngoại lệ (xem `Quản lý trạng thái toàn cục <Managing Global State_>`_), nhưng chúng sẽ cần được cân nhắc kỹ hơn và chú ý đến các trường hợp biên.

Mặc dù một số module có thể hoạt động với các hạn chế bớt nghiêm ngặt hơn, các module độc lập giúp dễ dàng đặt ra những kỳ vọng và hướng dẫn rõ ràng, có thể áp dụng cho nhiều trường hợp sử dụng.


Các trường hợp biên bất ngờ
---------------------------

Lưu ý rằng các module độc lập cũng tạo ra một số trường hợp biên bất ngờ. Đáng chú ý nhất là mỗi đối tượng module thường không dùng chung các class và exception của nó với các module tương tự khác. Tiếp nối từ `ví dụ ở trên <Isolated Module Objects_>`__, lưu ý rằng ``old_binascii.Error`` và ``binascii.Error`` là các đối tượng riêng biệt. Trong đoạn mã sau, exception *không* được bắt:

.. code-block:: pycon

   >>> old_binascii.Error == binascii.Error
   False
   >>> try:
   ...     old_binascii.unhexlify(b'qwertyuiop')
   ... except binascii.Error:
   ...     print('boo')
   ...
   Traceback (most recent call last):
     File "<stdin>", line 2, in <module>
   binascii.Error: Non-hexadecimal digit found

Điều này là đúng như dự kiến. Hãy lưu ý rằng các module thuần Python cũng hoạt động theo cách tương tự: đó là một phần trong cách Python vận hành.

Mục tiêu là làm cho các extension module an toàn ở cấp độ C, chứ không phải làm cho các thủ thuật hoạt động theo cách trực quan. Việc thay đổi ``sys.modules`` "thủ công" được xem là một thủ thuật.


Làm cho Module An toàn với Nhiều Interpreter
============================================


.. _`Managing Global State`:

Quản lý trạng thái toàn cục
---------------------------

Đôi khi, trạng thái liên kết với một module Python không dành riêng cho module đó mà dành cho toàn bộ tiến trình (hoặc một phạm vi nào đó “toàn cục hơn” module). Ví dụ:

-  Module ``readline`` quản lý *thiết bị đầu cuối*.
-  Một module chạy trên bo mạch muốn điều khiển *đèn LED* trên bo mạch.

Trong những trường hợp này, module Python nên cung cấp *quyền truy cập* vào trạng thái toàn cục thay vì *sở hữu* trạng thái đó. Nếu có thể, hãy viết module sao cho nhiều bản sao của nó có thể truy cập trạng thái một cách độc lập (cùng với các thư viện khác, dù dành cho Python hay các ngôn ngữ khác). Nếu không thể, hãy cân nhắc sử dụng khóa rõ ràng.

Nếu cần sử dụng trạng thái toàn cục của tiến trình, cách đơn giản nhất để tránh các vấn đề với nhiều trình thông dịch là ngăn module được tải nhiều hơn một lần trong mỗi tiến trình—xem
:ref:`isolating-extensions-optout`.


Quản lý trạng thái theo từng module
-----------------------------------

Để sử dụng trạng thái theo từng module, hãy sử dụng
:ref:`khởi tạo module mở rộng theo nhiều giai đoạn <multi-phase-initialization>`. Điều này báo hiệu rằng module của bạn hỗ trợ chính xác nhiều interpreter.

Đặt ``PyModuleDef.m_size`` thành một số dương để yêu cầu số byte lưu trữ cục bộ module tương ứng. Thông thường, giá trị này sẽ được đặt bằng kích thước của một ``struct`` dành riêng cho module, có thể lưu trữ toàn bộ trạng thái ở cấp C của module. Cụ thể, đây là nơi bạn nên đặt các con trỏ đến các class (bao gồm cả exception, nhưng không bao gồm static type) và các thiết lập (ví dụ: ``csv``'s :py:data:`~csv.field_size_limit`) mà mã C cần để hoạt động.

.. note::
   Một lựa chọn khác là lưu trữ trạng thái trong ``__dict__`` của module, nhưng bạn phải tránh gây crash khi người dùng sửa đổi ``__dict__`` từ mã Python. Điều này thường có nghĩa là phải kiểm tra lỗi và kiểu ở cấp C, việc này rất dễ làm sai và khó kiểm thử đầy đủ.

   Tuy nhiên, nếu mã C không cần trạng thái module, chỉ lưu trữ trạng thái trong ``__dict__`` là một ý hay.

Nếu trạng thái module bao gồm các con trỏ ``PyObject``, đối tượng module phải giữ các tham chiếu đến những đối tượng đó và triển khai các hook cấp module ``m_traverse``, ``m_clear`` và ``m_free``. Chúng hoạt động giống như ``tp_traverse``, ``tp_clear`` và ``tp_free`` của một class. Việc thêm chúng sẽ đòi hỏi một số công sức và làm mã dài hơn; đây là cái giá phải trả cho các module có thể được dỡ tải một cách sạch sẽ.

Một ví dụ về module có trạng thái theo từng module hiện có tại `xxlimited <https://github.com/python/cpython/blob/master/Modules/xxlimited.c>`__; phần khởi tạo module mẫu được hiển thị ở cuối tệp.


.. _isolating-extensions-optout:

Không tham gia: Giới hạn một đối tượng module cho mỗi process
-------------------------------------------------------------

Một ``PyModuleDef.m_size`` không âm cho biết module hỗ trợ đúng cách nhiều interpreter. Nếu module của bạn chưa hỗ trợ điều này, bạn có thể chỉ rõ rằng module chỉ được load một lần trong mỗi process. Ví dụ:::

   // A process-wide flag
   static int loaded = 0;

   // Mutex to provide thread safety (only needed for free-threaded Python)
   static PyMutex modinit_mutex = {0};

   static int
   exec_module(PyObject* module)
   {
       PyMutex_Lock(&modinit_mutex);
       if (loaded) {
           PyMutex_Unlock(&modinit_mutex);
           PyErr_SetString(PyExc_ImportError,
                           "cannot load module more than once per process");
           return -1;
       }
       loaded = 1;
       PyMutex_Unlock(&modinit_mutex);
       // ... rest of initialization
   }


Nếu hàm :c:member:`PyModuleDef.m_clear` của module có thể chuẩn bị cho việc khởi tạo lại trong tương lai, hàm đó nên xóa cờ ``loaded``. Trong trường hợp này, module của bạn sẽ không hỗ trợ nhiều instance tồn tại *đồng thời*, nhưng sẽ hỗ trợ, chẳng hạn, việc được load sau khi Python runtime tắt (:c:func:`Py_FinalizeEx`) và khởi tạo lại (:c:func:`Py_Initialize`).


Truy cập trạng thái module từ các hàm
-------------------------------------

Việc truy cập trạng thái từ các hàm cấp module rất đơn giản. Các hàm nhận đối tượng module làm đối số đầu tiên; để trích xuất trạng thái, bạn có thể sử dụng ``PyModule_GetState``::

   static PyObject *
   func(PyObject *module, PyObject *args)
   {
       my_struct *state = (my_struct*)PyModule_GetState(module);
       if (state == NULL) {
           return NULL;
       }
       // ... rest of logic
   }

.. note::
   ``PyModule_GetState`` có thể trả về ``NULL`` mà không thiết lập exception nếu không có trạng thái module, tức là ``PyModuleDef.m_size`` bằng không. Trong module của riêng bạn, bạn kiểm soát ``m_size``, vì vậy có thể dễ dàng ngăn điều này xảy ra.


Các kiểu heap
=============

Theo truyền thống, các kiểu được định nghĩa trong mã C là *static*; nghĩa là ``static PyTypeObject`` các cấu trúc được định nghĩa trực tiếp trong mã và được khởi tạo bằng ``PyType_Ready()``.

Các kiểu như vậy nhất thiết được dùng chung trong toàn bộ tiến trình. Việc dùng chung chúng giữa các đối tượng module đòi hỏi phải chú ý đến mọi trạng thái mà chúng sở hữu hoặc truy cập. Để hạn chế các vấn đề có thể xảy ra, các kiểu static là bất biến ở cấp Python: chẳng hạn, bạn không thể đặt ``str.myattribute = 123``.

.. impl-detail::
   Việc dùng chung các đối tượng thực sự bất biến giữa các interpreter là an toàn, miễn là chúng không cung cấp quyền truy cập vào các đối tượng khả biến. Tuy nhiên, trong CPython, mọi đối tượng Python đều có một chi tiết triển khai khả biến: reference count. Các thay đổi đối với refcount được bảo vệ bởi GIL. Vì vậy, mã dùng chung bất kỳ đối tượng Python nào giữa các interpreter đều ngầm phụ thuộc vào GIL hiện tại của CPython, vốn có phạm vi toàn tiến trình.

Vì bất biến và có phạm vi toàn tiến trình, các kiểu static không thể truy cập trạng thái module "của chúng". Nếu bất kỳ phương thức nào của một kiểu như vậy cần truy cập trạng thái module, kiểu đó phải được chuyển đổi thành *kiểu được cấp phát trên heap*, hay gọi ngắn gọn là *kiểu heap*. Các kiểu này tương ứng gần hơn với những lớp được tạo bởi câu lệnh ``class`` của Python.

Đối với các module mới, dùng kiểu heap theo mặc định là một nguyên tắc thực hành tốt.


Chuyển đổi Kiểu Static thành Kiểu Heap
--------------------------------------

Có thể chuyển đổi các kiểu static thành kiểu heap, nhưng lưu ý rằng API cho kiểu heap không được thiết kế để chuyển đổi "không mất mát" từ kiểu static—tức là tạo ra một kiểu hoạt động chính xác như một kiểu static nhất định. Vì vậy, khi viết lại định nghĩa lớp bằng API mới, bạn có thể vô tình thay đổi một vài chi tiết (ví dụ: khả năng pickle hoặc các slot được kế thừa). Luôn kiểm thử những chi tiết quan trọng đối với bạn.

Đặc biệt, hãy chú ý đến hai điểm sau (nhưng lưu ý rằng đây không phải là danh sách đầy đủ):

* Không giống các kiểu tĩnh, các đối tượng kiểu heap mặc định có thể thay đổi. Sử dụng cờ :c:macro:`Py_TPFLAGS_IMMUTABLETYPE` để ngăn việc thay đổi này.
* Theo mặc định, các kiểu heap kế thừa :c:member:`~PyTypeObject.tp_new`, vì vậy có thể khởi tạo chúng từ mã Python. Bạn có thể ngăn điều này bằng cờ :c:macro:`Py_TPFLAGS_DISALLOW_INSTANTIATION`.


Định nghĩa kiểu heap
--------------------

Có thể tạo kiểu heap bằng cách điền vào cấu trúc :c:struct:`PyType_Spec`, một mô tả hoặc "bản thiết kế" của một class, rồi gọi
:c:func:`PyType_FromModuleAndSpec` để xây dựng một đối tượng class mới.

.. note::
   Các hàm khác, chẳng hạn như :c:func:`PyType_FromSpec`, cũng có thể tạo kiểu heap, nhưng :c:func:`PyType_FromModuleAndSpec` liên kết module với class, cho phép truy cập trạng thái của module từ các method.

Lớp này thường nên được lưu trữ *cả trong* trạng thái của module (để truy cập an toàn từ C) và ``__dict__`` của module (để truy cập từ mã Python).


Giao thức thu gom rác
---------------------

Các instance của heap type giữ một tham chiếu đến type của chúng. Điều này đảm bảo type không bị hủy trước khi tất cả instance của nó bị hủy, nhưng có thể tạo ra các chu kỳ tham chiếu cần được garbage collector phá vỡ.

Để tránh rò rỉ bộ nhớ, các instance của heap type phải triển khai giao thức thu gom rác. Nghĩa là, heap type nên:

- Có flag :c:macro:`Py_TPFLAGS_HAVE_GC`.
- Định nghĩa một hàm traverse bằng :c:data:`Py_tp_traverse`, hàm này duyệt qua type (ví dụ: sử dụng ``Py_VISIT(Py_TYPE(self))``).

Vui lòng tham khảo tài liệu về
:c:macro:`Py_TPFLAGS_HAVE_GC` và :c:member:`~PyTypeObject.tp_traverse` để biết thêm các điểm cần cân nhắc.

API để định nghĩa các kiểu heap được phát triển một cách tự phát, khiến việc sử dụng API này ở trạng thái hiện tại khá bất tiện. Các phần sau sẽ hướng dẫn bạn xử lý những vấn đề thường gặp.


``tp_traverse`` trong Python 3.8 trở xuống
..........................................

Yêu cầu truy cập kiểu này từ ``tp_traverse`` được thêm vào trong Python 3.9. Nếu hỗ trợ Python 3.8 trở xuống, hàm traverse phải *không* truy cập kiểu này, vì vậy nó phải phức tạp hơn::

   static int my_traverse(PyObject *self, visitproc visit, void *arg)
   {
       if (Py_Version >= 0x03090000) {
           Py_VISIT(Py_TYPE(self));
       }
       return 0;
   }

Không may là :c:data:`Py_Version` chỉ được thêm vào trong Python 3.11. Để thay thế, hãy sử dụng:

* :c:macro:`PY_VERSION_HEX`, nếu không sử dụng stable ABI, hoặc
* :py:data:`sys.version_info` (thông qua :c:func:`PySys_GetObject` và
  :c:func:`PyArg_ParseTuple`).


Ủy quyền cho ``tp_traverse``
............................

Nếu hàm traverse của bạn ủy quyền cho :c:member:`~PyTypeObject.tp_traverse` của lớp cơ sở (hoặc một kiểu khác), hãy đảm bảo rằng ``Py_TYPE(self)`` chỉ được duyệt một lần. Lưu ý rằng chỉ các kiểu heap mới được dự kiến sẽ duyệt kiểu này trong ``tp_traverse``.

Ví dụ, nếu hàm traverse của bạn bao gồm::

   base->tp_traverse(self, visit, arg)

...và ``base`` có thể là một kiểu tĩnh, thì hàm đó cũng nên bao gồm::

    if (base->tp_flags & Py_TPFLAGS_HEAPTYPE) {
        // a heap type's tp_traverse already visited Py_TYPE(self)
    } else {
        if (Py_Version >= 0x03090000) {
            Py_VISIT(Py_TYPE(self));
        }
    }

Không cần xử lý số lượng tham chiếu của kiểu trong
:c:member:`~PyTypeObject.tp_new` và :c:member:`~PyTypeObject.tp_clear`.


Định nghĩa ``tp_dealloc``
.........................

Nếu kiểu của bạn có hàm :c:member:`~PyTypeObject.tp_dealloc` tùy chỉnh, hàm này cần:

- gọi :c:func:`PyObject_GC_UnTrack` trước khi bất kỳ trường nào bị vô hiệu hóa, và
- giảm số lượng tham chiếu của kiểu.

Để giữ cho kiểu vẫn hợp lệ trong khi gọi ``tp_free``, số lượng tham chiếu của kiểu cần được giảm *after* khi instance được giải phóng. Ví dụ::

   static void my_dealloc(PyObject *self)
   {
       PyObject_GC_UnTrack(self);
       ...
       PyTypeObject *type = Py_TYPE(self);
       type->tp_free(self);
       Py_DECREF(type);
   }

Hàm ``tp_dealloc`` mặc định thực hiện việc này, vì vậy nếu kiểu của bạn *not* ghi đè ``tp_dealloc`` thì bạn không cần thêm hàm này.


Không ghi đè ``tp_free``
........................

Slot :c:member:`~PyTypeObject.tp_free` của kiểu heap phải được đặt thành
:c:func:`PyObject_GC_Del`. Đây là giá trị mặc định; không ghi đè giá trị này.


Tránh ``PyObject_New``
......................

Các đối tượng được GC theo dõi cần được cấp phát bằng các hàm hỗ trợ GC.

Nếu bạn sử dụng :c:func:`PyObject_New` hoặc :c:func:`PyObject_NewVar`:

- Nếu có thể, hãy lấy và gọi slot :c:member:`~PyTypeObject.tp_alloc` của kiểu. Tức là, thay ``TYPE *o = PyObject_New(TYPE, typeobj)`` bằng::

      TYPE *o = typeobj->tp_alloc(typeobj, 0);

  Thay ``o = PyObject_NewVar(TYPE, typeobj, size)`` bằng đoạn tương tự, nhưng sử dụng size thay vì 0.

- Nếu không thể thực hiện điều trên (ví dụ: bên trong một ``tp_alloc`` tùy chỉnh), hãy gọi :c:func:`PyObject_GC_New` hoặc :c:func:`PyObject_GC_NewVar`::

      TYPE *o = PyObject_GC_New(TYPE, typeobj);

      TYPE *o = PyObject_GC_NewVar(TYPE, typeobj, size);


Truy cập trạng thái module từ các lớp
-------------------------------------

Nếu bạn có một đối tượng kiểu được định nghĩa bằng :c:func:`PyType_FromModuleAndSpec`, bạn có thể gọi :c:func:`PyType_GetModule` để lấy module liên kết, rồi
:c:func:`PyModule_GetState` để lấy trạng thái của module.

Để tránh phải viết một số mã boilerplate xử lý lỗi tẻ nhạt, bạn có thể kết hợp hai bước này bằng :c:func:`PyType_GetModuleState`, cho kết quả là::

   my_struct *state = (my_struct*)PyType_GetModuleState(type);
   if (state == NULL) {
       return NULL;
   }


Truy cập trạng thái module từ các phương thức thông thường
----------------------------------------------------------

Việc truy cập trạng thái cấp module từ các phương thức của một lớp phức tạp hơn đôi chút, nhưng có thể thực hiện được nhờ API được giới thiệu trong Python 3.9. Để lấy trạng thái, trước tiên bạn cần lấy *lớp định nghĩa*, sau đó lấy trạng thái module từ lớp đó.

Trở ngại lớn nhất là lấy *lớp mà một phương thức được định nghĩa trong đó*, hay gọi ngắn gọn là "lớp định nghĩa" của phương thức đó. Lớp định nghĩa có thể tham chiếu đến module mà nó thuộc về.

Không được nhầm lẫn lớp định nghĩa với ``Py_TYPE(self)``. Nếu phương thức được gọi trên một *lớp con* của kiểu của bạn, ``Py_TYPE(self)`` sẽ tham chiếu đến lớp con đó, lớp này có thể được định nghĩa trong một module khác với module của bạn.

.. note::
   Đoạn mã Python sau đây có thể minh họa khái niệm này. ``Base.get_defining_class`` trả về ``Base`` ngay cả khi ``type(self) == Sub``:

   .. code-block:: python

      class Base:
          def get_type_of_self(self):
              return type(self)

          def get_defining_class(self):
              return __class__

      class Sub(Base):
          pass

Để một phương thức lấy được "lớp định nghĩa" của nó, phương thức đó phải sử dụng
:ref:`METH_METHOD | METH_FASTCALL | METH_KEYWORDS <METH_METHOD-METH_FASTCALL-METH_KEYWORDS>`
:c:type:`quy ước gọi <PyMethodDef>` và :c:type:`PyCMethod` chữ ký tương ứng::

   PyObject *PyCMethod(
       PyObject *self,               // object the method was called on
       PyTypeObject *defining_class, // defining class
       PyObject *const *args,        // C array of arguments
       Py_ssize_t nargs,             // length of "args"
       PyObject *kwnames)            // NULL, or dict of keyword arguments

Khi đã có lớp định nghĩa, hãy gọi :c:func:`PyType_GetModuleState` để lấy trạng thái của module liên kết với nó.

Ví dụ::

   static PyObject *
   example_method(PyObject *self,
           PyTypeObject *defining_class,
           PyObject *const *args,
           Py_ssize_t nargs,
           PyObject *kwnames)
   {
       my_struct *state = (my_struct*)PyType_GetModuleState(defining_class);
       if (state == NULL) {
           return NULL;
       }
       ... // rest of logic
   }

   PyDoc_STRVAR(example_method_doc, "...");

   static PyMethodDef my_methods[] = {
       {"example_method",
         (PyCFunction)(void(*)(void))example_method,
         METH_METHOD|METH_FASTCALL|METH_KEYWORDS,
         example_method_doc}
       {NULL},
   }


Truy cập trạng thái module từ các phương thức slot, getter và setter
--------------------------------------------------------------------

.. note::

   Tính năng này mới có trong Python 3.11.

   .. After adding to limited API:

      If you use the :ref:`limited API <limited-c-api>`,
      you must update ``Py_LIMITED_API`` to ``0x030b0000``, losing ABI
      compatibility with earlier versions.

Các phương thức slot—các phiên bản C nhanh tương đương với những phương thức đặc biệt, chẳng hạn như
:c:member:`~PyNumberMethods.nb_add` cho :py:attr:`~object.__add__` hoặc
:c:member:`~PyTypeObject.tp_new` để khởi tạo—có API rất đơn giản, không cho phép truyền vào class định nghĩa, không giống như với :c:type:`PyCMethod`. Điều tương tự cũng áp dụng cho các getter và setter được định nghĩa bằng
:c:type:`PyGetSetDef`.

Để truy cập trạng thái module trong những trường hợp này, hãy sử dụng hàm
:c:func:`PyType_GetModuleByDef`, và truyền vào định nghĩa module. Sau khi có module, hãy gọi :c:func:`PyModule_GetState` để lấy trạng thái::

    PyObject *module = PyType_GetModuleByDef(Py_TYPE(self), &module_def);
    my_struct *state = (my_struct*)PyModule_GetState(module);
    if (state == NULL) {
        return NULL;
    }

:c:func:`!PyType_GetModuleByDef` hoạt động bằng cách tìm kiếm trong
:term:`method resolution order` (tức là tất cả các lớp cha) để tìm lớp cha đầu tiên có module tương ứng.

.. note::

   Trong những trường hợp rất đặc biệt (chuỗi kế thừa trải rộng qua nhiều module được tạo từ cùng một định nghĩa), :c:func:`!PyType_GetModuleByDef` có thể không trả về module của lớp thực sự định nghĩa. Tuy nhiên, nó sẽ luôn trả về một module có cùng định nghĩa, đảm bảo bố cục bộ nhớ C tương thích.


Vòng đời của trạng thái module
------------------------------

Khi một đối tượng module được thu gom rác, trạng thái module của nó sẽ được giải phóng. Với mỗi con trỏ trỏ đến (một phần của) trạng thái module, bạn phải giữ một tham chiếu đến đối tượng module.

Thông thường, đây không phải là vấn đề, vì các kiểu được tạo bằng
:c:func:`PyType_FromModuleAndSpec` và các thực thể của chúng giữ một tham chiếu đến module. Tuy nhiên, bạn phải cẩn thận trong việc đếm tham chiếu khi tham chiếu đến trạng thái module từ những nơi khác, chẳng hạn như các callback cho thư viện bên ngoài.


Các vấn đề còn tồn đọng
=======================

Một số vấn đề liên quan đến trạng thái theo từng mô-đun và heap type vẫn chưa được giải quyết.

Tốt nhất nên thảo luận về việc cải thiện tình hình trên `diễn đàn discuss với thẻ c-api <https://discuss.python.org/c/core-dev/c-api/30>`__.


Phạm vi theo từng lớp
---------------------

Hiện tại (tính đến Python 3.11), không thể gắn trạng thái vào từng *kiểu* riêng lẻ nếu không dựa vào các chi tiết triển khai của CPython (những chi tiết này có thể thay đổi trong tương lai—có lẽ, một cách trớ trêu, để cho phép một giải pháp phù hợp cho phạm vi theo từng lớp).


Chuyển đổi không mất dữ liệu sang Heap Type
-------------------------------------------

API heap type không được thiết kế để chuyển đổi "không mất dữ liệu" từ các kiểu tĩnh; tức là tạo ra một kiểu hoạt động chính xác như một kiểu tĩnh nhất định.
