.. highlight:: c

.. _defining-new-types:

****************************************
Định nghĩa các kiểu Extension: Hướng dẫn
****************************************

.. sectionauthor:: Michael Hudson <mwh@python.net>
.. sectionauthor:: Dave Kuhlman <dkuhlman@rexx.com>
.. sectionauthor:: Jim Fulton <jim@zope.com>


Python cho phép người viết module extension C định nghĩa các kiểu mới có thể được thao tác từ mã Python, tương tự như các kiểu :class:`str` và :class:`list` tích hợp sẵn. Mã cho tất cả các kiểu extension đều tuân theo một mẫu, nhưng có một số chi tiết bạn cần hiểu trước khi bắt đầu. Tài liệu này là phần giới thiệu nhẹ nhàng về chủ đề này.


.. _dnt-basics:

Kiến thức cơ bản
================

runtime :term:`CPython` xem tất cả các đối tượng Python là các biến thuộc kiểu
:c:expr:`PyObject*`, đóng vai trò là "kiểu cơ sở" cho tất cả các đối tượng Python. Bản thân cấu trúc :c:type:`PyObject` chỉ chứa
:term:`reference count` của đối tượng và một con trỏ đến "đối tượng kiểu" của đối tượng đó. Đây là nơi diễn ra phần xử lý chính; đối tượng kiểu quyết định những hàm (C) nào được trình thông dịch gọi khi, chẳng hạn, một thuộc tính được tra cứu trên một đối tượng, một phương thức được gọi hoặc đối tượng đó được nhân với một đối tượng khác. Các hàm C này được gọi là "phương thức kiểu".

Vì vậy, nếu muốn định nghĩa một kiểu extension mới, bạn cần tạo một đối tượng kiểu mới.

Loại nội dung này chỉ có thể được giải thích bằng ví dụ, vì vậy dưới đây là một module tối giản nhưng hoàn chỉnh, định nghĩa một kiểu mới có tên :class:`!Custom` bên trong module mở rộng C :mod:`!custom`:

.. note::
   Ở đây, chúng ta trình bày cách truyền thống để định nghĩa các kiểu mở rộng *static*. Cách này đáp ứng hầu hết các trường hợp sử dụng. C API cũng cho phép định nghĩa các kiểu mở rộng được cấp phát trên heap bằng
   hàm :c:func:`PyType_FromSpec`, nhưng nội dung này không được đề cập trong tutorial.

.. literalinclude:: ../includes/newtypes/custom.c

Có khá nhiều thông tin cần tiếp nhận cùng lúc, nhưng hy vọng một số phần sẽ quen thuộc từ chương trước. Tệp này định nghĩa ba thành phần:

#. Nội dung của một :class:`!Custom` **object**: đây là struct ``CustomObject``, được cấp phát một lần cho mỗi instance của :class:`!Custom`.
#. Cách một :class:`!Custom` **type** hoạt động: đây là struct ``CustomType``, định nghĩa một tập hợp các cờ và con trỏ hàm mà interpreter kiểm tra khi có yêu cầu thực hiện các thao tác cụ thể.
#. Cách định nghĩa và thực thi module :mod:`!custom`: đây là hàm ``PyInit_custom`` và struct ``custom_module`` tương ứng để định nghĩa module, cùng với hàm ``custom_module_exec`` để thiết lập một module object mới.

Phần đầu tiên là::

   typedef struct {
       PyObject_HEAD
   } CustomObject;

Đây là những gì một đối tượng Custom sẽ chứa. ``PyObject_HEAD`` là bắt buộc ở đầu mỗi struct đối tượng và định nghĩa một trường có tên ``ob_base`` thuộc kiểu :c:type:`PyObject`, chứa một con trỏ trỏ đến một đối tượng kiểu và một bộ đếm tham chiếu (có thể truy cập chúng lần lượt bằng các macro :c:macro:`Py_TYPE` và :c:macro:`Py_REFCNT`). Macro này được dùng để ẩn chi tiết bố cục và cho phép thêm các trường trong :ref:`debug builds <debug-build>`.

.. note::
   Ở trên không có dấu chấm phẩy sau macro :c:macro:`PyObject_HEAD`. Hãy cẩn thận để không vô tình thêm dấu này: một số compiler sẽ báo lỗi.

Dĩ nhiên, các đối tượng thường lưu trữ thêm dữ liệu bên cạnh phần boilerplate ``PyObject_HEAD`` tiêu chuẩn; ví dụ, sau đây là định nghĩa cho các số thực Python tiêu chuẩn::

   typedef struct {
       PyObject_HEAD
       double ob_fval;
   } PyFloatObject;

Phần thứ hai là định nghĩa của đối tượng kiểu.::

   static PyTypeObject CustomType = {
       .ob_base = PyVarObject_HEAD_INIT(NULL, 0)
       .tp_name = "custom.Custom",
       .tp_doc = PyDoc_STR("Custom objects"),
       .tp_basicsize = sizeof(CustomObject),
       .tp_itemsize = 0,
       .tp_flags = Py_TPFLAGS_DEFAULT,
       .tp_new = PyType_GenericNew,
   };

.. note::
   Chúng tôi khuyến nghị sử dụng designated initializer theo kiểu C99 như trên, để tránh phải liệt kê tất cả các trường :c:type:`PyTypeObject` mà bạn không quan tâm, đồng thời không phải quan tâm đến thứ tự khai báo các trường.

Định nghĩa thực tế của :c:type:`PyTypeObject` trong :file:`object.h` có nhiều :ref:`fields <type-structs>` hơn đáng kể so với định nghĩa ở trên. Các trường còn lại sẽ được compiler C điền bằng số 0, và thông thường người ta không chỉ định chúng một cách rõ ràng trừ khi cần dùng đến.

Chúng ta sẽ mổ xẻ nó, từng trường một::

   .ob_base = PyVarObject_HEAD_INIT(NULL, 0)

Dòng này là mã mẫu bắt buộc để khởi tạo trường ``ob_base`` được đề cập ở trên.::

   .tp_name = "custom.Custom",

Tên của kiểu. Tên này sẽ xuất hiện trong biểu diễn văn bản mặc định của các đối tượng của chúng ta và trong một số thông báo lỗi, ví dụ:

.. code-block:: pycon

   >>> "" + custom.Custom()
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: can only concatenate str (not "custom.Custom") to str

Lưu ý rằng tên này là một tên có dấu chấm, bao gồm cả tên module và tên kiểu trong module. Trong trường hợp này, module là :mod:`!custom` và kiểu là :class:`!Custom`, vì vậy chúng ta đặt tên kiểu là :class:`!custom.Custom`. Việc sử dụng đường dẫn import có dấu chấm thực tế rất quan trọng để kiểu của bạn tương thích với các module :mod:`pydoc` và :mod:`pickle`.::

   .tp_basicsize = sizeof(CustomObject),
   .tp_itemsize = 0,

Điều này giúp Python biết cần cấp phát bao nhiêu bộ nhớ khi tạo các instance :class:`!Custom` mới. :c:member:`~PyTypeObject.tp_itemsize` chỉ được sử dụng cho các đối tượng có kích thước thay đổi và nếu không thì phải là số không.

.. note::

   Nếu bạn muốn kiểu của mình có thể được tạo lớp con từ Python, và kiểu của bạn có cùng
   :c:member:`~PyTypeObject.tp_basicsize` với kiểu cơ sở, bạn có thể gặp vấn đề với đa kế thừa. Một lớp con Python của kiểu của bạn sẽ phải liệt kê kiểu của bạn trước trong :attr:`~type.__bases__`, nếu không nó sẽ không thể gọi
   phương thức :meth:`~object.__new__` mà không gặp lỗi. Bạn có thể tránh vấn đề này bằng cách đảm bảo rằng kiểu của bạn có giá trị :c:member:`~PyTypeObject.tp_basicsize` lớn hơn kiểu cơ sở của nó. Phần lớn thời gian, điều này vốn sẽ đúng, vì kiểu cơ sở của bạn либо sẽ là :class:`object`, либо bạn sẽ thêm các thành viên dữ liệu vào kiểu cơ sở, và do đó làm tăng kích thước của nó.

Chúng ta đặt các cờ của lớp thành :c:macro:`Py_TPFLAGS_DEFAULT`.::

   .tp_flags = Py_TPFLAGS_DEFAULT,

Tất cả các kiểu nên bao gồm hằng số này trong các cờ của chúng. Hằng số này bật tất cả các thành viên được định nghĩa cho đến ít nhất Python 3.3. Nếu cần thêm thành viên, bạn sẽ phải OR các cờ tương ứng.

Chúng ta cung cấp chuỗi tài liệu cho kiểu trong :c:member:`~PyTypeObject.tp_doc`.::

   .tp_doc = PyDoc_STR("Custom objects"),

Để bật việc tạo đối tượng, chúng ta phải cung cấp một trình xử lý :c:member:`~PyTypeObject.tp_new`. Đây là phần tương đương với phương thức Python :meth:`~object.__new__`, nhưng phải được chỉ định rõ ràng. Trong trường hợp này, chúng ta có thể chỉ cần sử dụng phần triển khai mặc định do hàm API :c:func:`PyType_GenericNew` cung cấp.::

   .tp_new = PyType_GenericNew,

Mọi thứ khác trong tệp sẽ khá quen thuộc, ngoại trừ một phần mã trong
:c:func:`!custom_module_exec`::

   if (PyType_Ready(&CustomType) < 0) {
       return -1;
   }

Thao tác này khởi tạo kiểu :class:`!Custom`, điền một số thành viên bằng các giá trị mặc định phù hợp, bao gồm :c:member:`~PyObject.ob_type`, mà ban đầu chúng ta đặt thành ``NULL``.::

   if (PyModule_AddObjectRef(m, "Custom", (PyObject *) &CustomType) < 0) {
       return -1;
   }

Điều này thêm kiểu vào từ điển module. Điều này cho phép chúng ta tạo
các thực thể :class:`!Custom` bằng cách gọi lớp :class:`!Custom`:

.. code-block:: pycon

   >>> import custom
   >>> mycustom = custom.Custom()

Vậy là xong! Tất cả những gì còn lại là build nó; hãy đặt đoạn mã trên vào một tệp có tên
:file:`custom.c`,

.. literalinclude:: ../includes/newtypes/pyproject.toml

trong một tệp có tên :file:`pyproject.toml`, và

.. code-block:: python

   from setuptools import Extension, setup
   setup(ext_modules=[Extension("custom", ["custom.c"])])

trong một tệp có tên :file:`setup.py`; sau đó nhập

.. code-block:: shell-session

   $ python -m pip install .

trong shell sẽ tạo ra một tệp :file:`custom.so` trong một thư mục con và cài đặt nó; bây giờ hãy khởi động Python --- bạn sẽ có thể ``import custom`` và thử làm việc với các đối tượng ``Custom``.

Cũng không khó lắm, phải không?

Dĩ nhiên, kiểu Custom hiện tại khá tẻ nhạt. Nó không có dữ liệu và cũng không thực hiện bất kỳ điều gì. Thậm chí nó còn không thể được phân lớp.


Thêm dữ liệu và phương thức vào ví dụ Basic
===========================================

Hãy mở rộng ví dụ cơ bản để thêm một số dữ liệu và phương thức. Đồng thời, hãy làm cho kiểu này có thể được sử dụng làm lớp cơ sở. Chúng ta sẽ tạo một module mới, :mod:`!custom2` bổ sung các khả năng này:

.. literalinclude:: ../includes/newtypes/custom2.c


Phiên bản module này có một số thay đổi.

Kiểu :class:`!Custom` hiện có ba thuộc tính dữ liệu trong struct C của nó, *first*, *last* và *number*. Các biến *first* và *last* là các chuỗi Python chứa tên và họ. Thuộc tính *number* là một số nguyên C.

Cấu trúc đối tượng được cập nhật tương ứng::

   typedef struct {
       PyObject_HEAD
       PyObject *first; /* tên */
       PyObject *last;  /* họ */
       int number;
   } CustomObject;

Vì hiện có dữ liệu cần quản lý, chúng ta phải cẩn thận hơn khi cấp phát và giải phóng đối tượng. Tối thiểu, chúng ta cần một phương thức giải phóng::

   static void
   Custom_dealloc(PyObject *op)
   {
       CustomObject *self = (CustomObject *) op;
       Py_XDECREF(self->first);
       Py_XDECREF(self->last);
       Py_TYPE(self)->tp_free(self);
   }

được gán cho thành viên :c:member:`~PyTypeObject.tp_dealloc`::

   .tp_dealloc = Custom_dealloc,

Phương thức này trước tiên xóa số lượng tham chiếu của hai thuộc tính Python.
:c:func:`Py_XDECREF` xử lý chính xác trường hợp đối số của nó là ``NULL`` (điều này có thể xảy ra ở đây nếu ``tp_new`` bị lỗi giữa chừng). Sau đó, nó gọi thành viên :c:member:`~PyTypeObject.tp_free` của kiểu đối tượng (được tính bằng ``Py_TYPE(self)``) để giải phóng bộ nhớ của đối tượng. Lưu ý rằng kiểu của đối tượng có thể không phải là :class:`!CustomType`, vì đối tượng có thể là một instance của lớp con.

.. note::

   Phép ép kiểu tường minh sang ``CustomObject *`` ở trên là cần thiết vì chúng ta đã định nghĩa ``Custom_dealloc`` nhận đối số ``PyObject *``, do con trỏ hàm ``tp_dealloc`` yêu cầu nhận đối số ``PyObject *``. Bằng cách gán vào slot ``tp_dealloc`` của một kiểu, chúng ta khai báo rằng nó chỉ có thể được gọi với các instance của lớp ``CustomObject`` của chúng ta, vì vậy phép ép kiểu sang ``(CustomObject *)`` là an toàn. Đây chính là tính đa hình hướng đối tượng trong C!

   Trong mã hiện có hoặc các phiên bản trước của hướng dẫn này, bạn có thể thấy những hàm tương tự nhận trực tiếp một con trỏ đến cấu trúc đối tượng của kiểu con (``CustomObject*``), như sau::

      Custom_dealloc(CustomObject *self)
      {
          Py_XDECREF(self->first);
          Py_XDECREF(self->last);
          Py_TYPE(self)->tp_free((PyObject *) self);
      }
      ...
      .tp_dealloc = (destructor) Custom_dealloc,

   Cách này thực hiện cùng một việc trên mọi kiến trúc mà CPython hỗ trợ, nhưng theo tiêu chuẩn C, nó gọi đến hành vi không xác định.

Chúng ta muốn đảm bảo rằng tên và họ được khởi tạo thành các chuỗi rỗng, vì vậy chúng ta cung cấp một triển khai ``tp_new``::

   static PyObject *
   Custom_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
   {
       CustomObject *self;
       self = (CustomObject *) type->tp_alloc(type, 0);
       if (self != NULL) {
           self->first = PyUnicode_FromString("");
           if (self->first == NULL) {
               Py_DECREF(self);
               return NULL;
           }
           self->last = PyUnicode_FromString("");
           if (self->last == NULL) {
               Py_DECREF(self);
               return NULL;
           }
           self->number = 0;
       }
       return (PyObject *) self;
   }

và cài đặt nó vào thành viên :c:member:`~PyTypeObject.tp_new`::

   .tp_new = Custom_new,

Handler ``tp_new`` chịu trách nhiệm tạo (trái với khởi tạo) các đối tượng thuộc kiểu này. Trong Python, nó được cung cấp dưới dạng phương thức :meth:`~object.__new__`. Không bắt buộc phải định nghĩa thành viên ``tp_new``, và trên thực tế, nhiều extension type sẽ đơn giản tái sử dụng :c:func:`PyType_GenericNew` như trong phiên bản đầu tiên của kiểu :class:`!Custom` ở trên. Trong trường hợp này, chúng ta sử dụng handler ``tp_new`` để khởi tạo các thuộc tính ``first`` và ``last`` bằng các giá trị mặc định khác ``NULL``.

``tp_new`` được truyền kiểu đang được khởi tạo (không nhất thiết là ``CustomType`` nếu một subclass được khởi tạo) cùng với mọi đối số được truyền khi kiểu này được gọi, và được kỳ vọng trả về instance đã tạo. Các handler ``tp_new`` luôn chấp nhận cả đối số positional và keyword, nhưng thường bỏ qua các đối số này, để việc xử lý đối số cho các phương thức initializer (còn gọi là ``tp_init`` trong C hoặc ``__init__`` trong Python) thực hiện.

.. note::
   ``tp_new`` không nên gọi ``tp_init`` một cách rõ ràng, vì interpreter sẽ tự thực hiện việc đó.

Việc triển khai ``tp_new`` gọi slot :c:member:`~PyTypeObject.tp_alloc` để cấp phát bộ nhớ::

   self = (CustomObject *) type->tp_alloc(type, 0);

Vì việc cấp phát bộ nhớ có thể thất bại, chúng ta phải kiểm tra kết quả :c:member:`~PyTypeObject.tp_alloc` với ``NULL`` trước khi tiếp tục.

.. note::
   Chúng ta không tự điền slot :c:member:`~PyTypeObject.tp_alloc`. Thay vào đó
   :c:func:`PyType_Ready` điền giá trị đó cho chúng ta bằng cách kế thừa nó từ lớp cơ sở, mặc định là :class:`object`. Hầu hết các kiểu sử dụng chiến lược cấp phát mặc định.

.. note::
   Nếu bạn đang tạo một :c:member:`~PyTypeObject.tp_new` hợp tác (một :c:member:`~PyTypeObject.tp_new` gọi :c:member:`~PyTypeObject.tp_new` hoặc :meth:`~object.__new__` của kiểu cơ sở), bạn *không* được cố gắng xác định phương thức cần gọi bằng thứ tự phân giải phương thức (method resolution order) tại runtime. Luôn xác định tĩnh kiểu mà bạn sẽ gọi, rồi gọi trực tiếp :c:member:`~PyTypeObject.tp_new` của kiểu đó hoặc thông qua ``type->tp_base->tp_new``. Nếu không làm vậy, các lớp con Python của kiểu bạn, vốn cũng kế thừa từ những lớp khác được định nghĩa bằng Python, có thể không hoạt động chính xác. (Cụ thể, bạn có thể không tạo được các thực thể của những lớp con như vậy mà không gặp :exc:`TypeError`.)

Chúng ta cũng định nghĩa một hàm khởi tạo nhận các đối số để cung cấp các giá trị ban đầu cho đối tượng của mình::

   static int
   Custom_init(PyObject *op, PyObject *args, PyObject *kwds)
   {
       CustomObject *self = (CustomObject *) op;
       static char *kwlist[] = {"first", "last", "number", NULL};
       PyObject *first = NULL, *last = NULL, *tmp;

       if (!PyArg_ParseTupleAndKeywords(args, kwds, "|OOi", kwlist,
                                        &first, &last,
                                        &self->number))
           return -1;

       if (first) {
           tmp = self->first;
           Py_INCREF(first);
           self->first = first;
           Py_XDECREF(tmp);
       }
       if (last) {
           tmp = self->last;
           Py_INCREF(last);
           self->last = last;
           Py_XDECREF(tmp);
       }
       return 0;
   }

bằng cách điền vào slot :c:member:`~PyTypeObject.tp_init`.::

   .tp_init = Custom_init,

Slot :c:member:`~PyTypeObject.tp_init` được cung cấp trong Python dưới dạng
phương thức :meth:`~object.__init__`. Phương thức này được dùng để khởi tạo một đối tượng sau khi đối tượng được tạo. Các hàm khởi tạo luôn nhận các đối số vị trí và đối số từ khóa, đồng thời phải trả về ``0`` khi thành công hoặc ``-1`` khi xảy ra lỗi.

Không giống trình xử lý ``tp_new``, không có gì đảm bảo rằng ``tp_init`` được gọi (ví dụ: theo mặc định, mô-đun :mod:`pickle` không gọi :meth:`~object.__init__` trên các thực thể đã được unpickle). Phương thức này cũng có thể được gọi nhiều lần. Bất kỳ ai cũng có thể gọi phương thức :meth:`!__init__` trên các đối tượng của chúng ta. Vì lý do này, chúng ta phải đặc biệt cẩn thận khi gán các giá trị thuộc tính mới. Chẳng hạn, chúng ta có thể bị hấp dẫn bởi cách gán thành viên ``first`` như sau::

   if (first) {
       Py_XDECREF(self->first);
       Py_INCREF(first);
       self->first = first;
   }

Tuy nhiên, việc này sẽ tiềm ẩn rủi ro. Kiểu của chúng ta không giới hạn kiểu của thành viên ``first``, vì vậy thành viên đó có thể là bất kỳ loại đối tượng nào. Đối tượng đó có thể có một hàm hủy khiến đoạn mã được thực thi và cố truy cập thành viên ``first``; hoặc hàm hủy đó có thể tách trạng thái
:term:`trạng thái luồng <attached thread state>` và cho phép mã tùy ý chạy trong các luồng khác, truy cập và sửa đổi đối tượng của chúng ta.

Để thận trọng và tự bảo vệ trước khả năng này, chúng ta gần như luôn gán lại các thành viên trước khi giảm số lượng tham chiếu của chúng. Khi nào chúng ta không cần làm vậy?

* khi chúng ta hoàn toàn biết chắc rằng số lượng tham chiếu lớn hơn 1;

* khi chúng ta biết rằng việc giải phóng đối tượng [#]_ sẽ không tách :term:`trạng thái luồng <attached thread state>` và cũng không gây ra bất kỳ lời gọi nào quay lại mã của kiểu chúng ta;

* khi giảm số lượng tham chiếu trong một trình xử lý :c:member:`~PyTypeObject.tp_dealloc` trên một kiểu không hỗ trợ thu gom rác theo chu kỳ [#]_.

Chúng ta muốn đưa các biến thực thể ra dưới dạng thuộc tính. Có một số cách để thực hiện việc đó. Cách đơn giản nhất là định nghĩa các thành viên::

   static PyMemberDef Custom_members[] = {
       {"first", Py_T_OBJECT_EX, offsetof(CustomObject, first), 0,
        "first name"},
       {"last", Py_T_OBJECT_EX, offsetof(CustomObject, last), 0,
        "last name"},
       {"number", Py_T_INT, offsetof(CustomObject, number), 0,
        "custom number"},
       {NULL}  /* Phần tử đánh dấu kết thúc */
   };

và đặt các định nghĩa vào vị trí :c:member:`~PyTypeObject.tp_members`::

   .tp_members = Custom_members,

Mỗi định nghĩa thành viên gồm có tên thành viên, kiểu, độ lệch, cờ truy cập và chuỗi tài liệu. Xem phần :ref:`Generic-Attribute-Management` bên dưới để biết chi tiết.

Một nhược điểm của cách tiếp cận này là nó không cung cấp cách hạn chế các kiểu đối tượng có thể được gán cho các thuộc tính Python. Chúng ta mong đợi tên và họ là các chuỗi, nhưng có thể gán bất kỳ đối tượng Python nào. Ngoài ra, các thuộc tính có thể bị xóa, khiến các con trỏ C được đặt thành ``NULL``. Mặc dù chúng ta có thể đảm bảo các thành viên được khởi tạo bằng các giá trị không phải ``NULL``, các thành viên có thể được đặt thành ``NULL`` nếu các thuộc tính bị xóa.

Chúng ta định nghĩa một phương thức duy nhất, :meth:`!Custom.name`, để xuất tên của đối tượng bằng cách nối tên và họ.::

   static PyObject *
   Custom_name(PyObject *op, PyObject *Py_UNUSED(dummy))
   {
       CustomObject *self = (CustomObject *) op;
       if (self->first == NULL) {
           PyErr_SetString(PyExc_AttributeError, "first");
           return NULL;
       }
       if (self->last == NULL) {
           PyErr_SetString(PyExc_AttributeError, "last");
           return NULL;
       }
       return PyUnicode_FromFormat("%S %S", self->first, self->last);
   }

Phương thức này được triển khai dưới dạng một hàm C nhận một :class:`!Custom` (hoặc
một thể hiện lớp con :class:`!Custom`) làm đối số đầu tiên. Các phương thức luôn nhận một thể hiện làm đối số đầu tiên. Các phương thức thường cũng nhận các đối số vị trí và từ khóa, nhưng trong trường hợp này chúng ta không nhận đối số nào và không cần chấp nhận một tuple đối số vị trí hoặc một dictionary đối số từ khóa. Phương thức này tương đương với phương thức Python:

.. code-block:: python

   def name(self):
       return "%s %s" % (self.first, self.last)

Lưu ý rằng chúng ta phải kiểm tra khả năng :attr:`!first` và
Các member :attr:`!last` là ``NULL``. Điều này là vì chúng có thể bị xóa, khi đó chúng được đặt thành ``NULL``. Tốt hơn là ngăn việc xóa các thuộc tính này và giới hạn giá trị thuộc tính ở dạng chuỗi. Chúng ta sẽ xem cách thực hiện điều đó trong phần tiếp theo.

Bây giờ, sau khi đã định nghĩa phương thức, chúng ta cần tạo một mảng các định nghĩa phương thức::

   static PyMethodDef Custom_methods[] = {
       {"name", Custom_name, METH_NOARGS,
        "Return the name, combining the first and last name"
       },
       {NULL}  /* Phần tử đánh dấu kết thúc */
   };

(lưu ý rằng chúng ta đã sử dụng cờ :c:macro:`METH_NOARGS` để cho biết phương thức không nhận đối số nào ngoài *self*)

và gán mảng đó cho slot :c:member:`~PyTypeObject.tp_methods`::

   .tp_methods = Custom_methods,

Cuối cùng, chúng ta sẽ làm cho kiểu của mình có thể được sử dụng làm lớp cơ sở để tạo lớp con. Cho đến nay, chúng ta đã cẩn thận viết các phương thức sao cho chúng không giả định bất kỳ điều gì về kiểu của đối tượng được tạo hoặc sử dụng, vì vậy tất cả những gì cần làm là thêm :c:macro:`Py_TPFLAGS_BASETYPE` vào định nghĩa cờ lớp của chúng ta::

   .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,

Chúng ta đổi tên :c:func:`!PyInit_custom` thành :c:func:`!PyInit_custom2`, cập nhật tên module trong struct :c:type:`PyModuleDef`, và cập nhật tên lớp đầy đủ trong struct :c:type:`PyTypeObject`.

Cuối cùng, chúng ta cập nhật tệp :file:`setup.py` để đưa module mới vào,

.. code-block:: python

   from setuptools import Extension, setup
   setup(ext_modules=[
       Extension("custom", ["custom.c"]),
       Extension("custom2", ["custom2.c"]),
   ])

và sau đó chúng ta cài đặt lại để có thể ``import custom2``:

.. code-block:: shell-session

   $ python -m pip install .

Kiểm soát chi tiết hơn các thuộc tính dữ liệu
=============================================

Trong phần này, chúng ta sẽ kiểm soát chi tiết hơn cách các thuộc tính :attr:`!first` và
:attr:`!last` được thiết lập trong ví dụ :class:`!Custom`. Ở phiên bản trước của module, các biến thể hiện :attr:`!first` và :attr:`!last` có thể được đặt thành các giá trị không phải chuỗi hoặc thậm chí bị xóa. Chúng ta muốn đảm bảo rằng các thuộc tính này luôn chứa chuỗi.

.. literalinclude:: ../includes/newtypes/custom3.c


Để kiểm soát tốt hơn các thuộc tính :attr:`!first` và :attr:`!last`, chúng ta sẽ sử dụng các hàm getter và setter tùy chỉnh.  Dưới đây là các hàm lấy và thiết lập thuộc tính :attr:`!first`::

   static PyObject *
   Custom_getfirst(PyObject *op, void *closure)
   {
       CustomObject *self = (CustomObject *) op;
       Py_INCREF(self->first);
       return self->first;
   }

   static int
   Custom_setfirst(PyObject *op, PyObject *value, void *closure)
   {
       CustomObject *self = (CustomObject *) op;
       PyObject *tmp;
       if (value == NULL) {
           PyErr_SetString(PyExc_TypeError, "Cannot delete the first attribute");
           return -1;
       }
       if (!PyUnicode_Check(value)) {
           PyErr_SetString(PyExc_TypeError,
                           "The first attribute value must be a string");
           return -1;
       }
       tmp = self->first;
       Py_INCREF(value);
       self->first = value;
       Py_DECREF(tmp);
       return 0;
   }

Hàm getter nhận một đối tượng :class:`!Custom` và một "closure", tức là một con trỏ void.  Trong trường hợp này, closure bị bỏ qua.  (Closure hỗ trợ một cách sử dụng nâng cao, trong đó dữ liệu định nghĩa được truyền cho getter và setter. Ví dụ, cách này có thể được dùng để cho phép một cặp hàm getter và setter duy nhất quyết định thuộc tính cần lấy hoặc thiết lập dựa trên dữ liệu trong closure.)

Hàm setter nhận đối tượng :class:`!Custom`, giá trị mới và closure.  Giá trị mới có thể là ``NULL``, trong trường hợp đó thuộc tính đang bị xóa.  Trong setter của chúng ta, chúng ta phát sinh lỗi nếu thuộc tính bị xóa hoặc nếu giá trị mới của thuộc tính không phải là một chuỗi.

Chúng ta tạo một mảng các cấu trúc :c:type:`PyGetSetDef`::

   static PyGetSetDef Custom_getsetters[] = {
       {"first", Custom_getfirst, Custom_setfirst,
        "first name", NULL},
       {"last", Custom_getlast, Custom_setlast,
        "last name", NULL},
       {NULL}  /* Phần tử đánh dấu kết thúc */
   };

và đăng ký mảng đó trong slot :c:member:`~PyTypeObject.tp_getset`::

   .tp_getset = Custom_getsetters,

Phần tử cuối cùng trong một cấu trúc :c:type:`PyGetSetDef` là "closure" được đề cập ở trên. Trong trường hợp này, chúng ta không sử dụng closure, nên chỉ truyền ``NULL``.

Chúng ta cũng xóa các định nghĩa thành viên cho những thuộc tính này::

   static PyMemberDef Custom_members[] = {
       {"number", Py_T_INT, offsetof(CustomObject, number), 0,
        "custom number"},
       {NULL}  /* Phần tử đánh dấu kết thúc */
   };

Chúng ta cũng cần cập nhật handler :c:member:`~PyTypeObject.tp_init` để chỉ cho phép truyền các chuỗi [#]_::

   static int
   Custom_init(PyObject *op, PyObject *args, PyObject *kwds)
   {
       CustomObject *self = (CustomObject *) op;
       static char *kwlist[] = {"first", "last", "number", NULL};
       PyObject *first = NULL, *last = NULL, *tmp;

       if (!PyArg_ParseTupleAndKeywords(args, kwds, "|UUi", kwlist,
                                        &first, &last,
                                        &self->number))
           return -1;

       if (first) {
           tmp = self->first;
           Py_INCREF(first);
           self->first = first;
           Py_DECREF(tmp);
       }
       if (last) {
           tmp = self->last;
           Py_INCREF(last);
           self->last = last;
           Py_DECREF(tmp);
       }
       return 0;
   }

Với những thay đổi này, chúng ta có thể đảm bảo rằng các thành viên ``first`` và ``last`` không bao giờ ``NULL``, nên có thể xóa các kiểm tra giá trị ``NULL`` trong hầu hết các trường hợp. Điều này có nghĩa là hầu hết các lệnh gọi :c:func:`Py_XDECREF` có thể được chuyển đổi thành
các lệnh gọi :c:func:`Py_DECREF`. Vị trí duy nhất chúng ta không thể thay đổi các lệnh gọi này là trong phần triển khai ``tp_dealloc``, nơi có khả năng việc khởi tạo các thành viên này đã thất bại trong ``tp_new``.

Chúng ta cũng đổi tên hàm khởi tạo module và tên module trong hàm khởi tạo, như đã làm trước đây, đồng thời thêm một định nghĩa bổ sung vào
:file:`setup.py` tệp.


Hỗ trợ thu gom rác theo chu kỳ
==============================

Python có một :term:`bộ thu gom rác theo chu kỳ (GC) <garbage collection>` có thể xác định các đối tượng không cần thiết ngay cả khi số lượng tham chiếu của chúng không bằng không. Điều này có thể xảy ra khi các đối tượng tham gia vào các chu kỳ. Ví dụ: hãy xét:

.. code-block:: pycon

   >>> l = []
   >>> l.append(l)
   >>> del l

Trong ví dụ này, chúng ta tạo một danh sách chứa chính nó. Khi xóa danh sách, nó vẫn có một tham chiếu từ chính nó. Số lượng tham chiếu của nó không giảm xuống bằng không. May mắn là bộ thu gom rác theo chu kỳ của Python cuối cùng sẽ xác định danh sách đó là rác và giải phóng nó.

Trong phiên bản thứ hai của ví dụ :class:`!Custom` , chúng ta cho phép lưu trữ mọi loại đối tượng trong các thuộc tính :attr:`!first` hoặc :attr:`!last` [#]_. Ngoài ra, trong phiên bản thứ hai và thứ ba, chúng ta cho phép tạo lớp con
:class:`!Custom`, và các lớp con có thể thêm các thuộc tính tùy ý. Vì một trong hai lý do đó, các đối tượng :class:`!Custom` có thể tham gia vào các chu kỳ:

.. code-block:: pycon

   >>> import custom3
   >>> class Derived(custom3.Custom): pass
   ...
   >>> n = Derived()
   >>> n.some_attribute = n

Để cho phép một thể hiện :class:`!Custom` tham gia vào một chu trình tham chiếu được cyclic GC phát hiện và thu gom đúng cách, kiểu :class:`!Custom` của chúng ta cần điền vào hai slot bổ sung và bật một cờ cho phép sử dụng các slot này:

.. literalinclude:: ../includes/newtypes/custom4.c


Trước tiên, phương thức traversal cho cyclic GC biết về các subobject có thể tham gia vào chu trình::

   static int
   Custom_traverse(PyObject *op, visitproc visit, void *arg)
   {
       CustomObject *self = (CustomObject *) op;
       int vret;
       if (self->first) {
           vret = visit(self->first, arg);
           if (vret != 0)
               return vret;
       }
       if (self->last) {
           vret = visit(self->last, arg);
           if (vret != 0)
               return vret;
       }
       return 0;
   }

Đối với mỗi subobject có thể tham gia vào chu trình, chúng ta cần gọi
hàm :c:func:`!visit`, được truyền vào phương thức traversal. Hàm
:c:func:`!visit` nhận subobject và đối số bổ sung *arg* được truyền vào phương thức traversal làm các đối số. Hàm này trả về một giá trị số nguyên phải được trả về nếu giá trị đó khác không.

Python cung cấp macro :c:func:`Py_VISIT` để tự động gọi các hàm visit. Với :c:func:`Py_VISIT`, chúng ta có thể giảm lượng mã lặp trong ``Custom_traverse``::

   static int
   Custom_traverse(PyObject *op, visitproc visit, void *arg)
   {
       CustomObject *self = (CustomObject *) op;
       Py_VISIT(self->first);
       Py_VISIT(self->last);
       return 0;
   }

.. note::
   Phần triển khai :c:member:`~PyTypeObject.tp_traverse` phải đặt tên các đối số chính xác là *visit* và *arg* để có thể sử dụng :c:func:`Py_VISIT`.

Thứ hai, chúng ta cần cung cấp một phương thức để dọn mọi đối tượng con có thể tham gia vào các chu trình::

   static int
   Custom_clear(PyObject *op)
   {
       CustomObject *self = (CustomObject *) op;
       Py_CLEAR(self->first);
       Py_CLEAR(self->last);
       return 0;
   }

Hãy chú ý đến việc sử dụng macro :c:func:`Py_CLEAR`. Đây là cách được khuyến nghị và an toàn để xóa các thuộc tính dữ liệu thuộc kiểu bất kỳ đồng thời giảm số lượng tham chiếu của chúng. Nếu thay vào đó, bạn gọi :c:func:`Py_XDECREF` trên thuộc tính trước khi đặt thuộc tính thành ``NULL``, có khả năng hàm hủy của thuộc tính sẽ gọi ngược vào mã đọc lại thuộc tính (*đặc biệt* nếu có một chu trình tham chiếu).

.. note::
   Bạn có thể mô phỏng :c:func:`Py_CLEAR` bằng cách viết::

      PyObject *tmp;
      tmp = self->first;
      self->first = NULL;
      Py_XDECREF(tmp);

   Tuy nhiên, việc luôn sử dụng :c:func:`Py_CLEAR` khi xóa một thuộc tính sẽ dễ dàng hơn nhiều và ít có nguy cơ gây lỗi hơn. Đừng cố tối ưu vi mô (micro-optimize) mà đánh đổi tính vững chắc!

Bộ giải phóng ``Custom_dealloc`` có thể gọi mã bất kỳ khi dọn các thuộc tính. Điều đó có nghĩa là circular GC có thể được kích hoạt bên trong hàm. Vì GC giả định rằng số lượng tham chiếu không bằng 0, chúng ta cần bỏ theo dõi đối tượng khỏi GC bằng cách gọi :c:func:`PyObject_GC_UnTrack` trước khi dọn các thành phần. Đây là bộ giải phóng được cài đặt lại của chúng ta, sử dụng :c:func:`PyObject_GC_UnTrack` và ``Custom_clear``::

   static void
   Custom_dealloc(PyObject *op)
   {
       PyObject_GC_UnTrack(op);
       (void)Custom_clear(op);
       Py_TYPE(op)->tp_free(op);
   }

Cuối cùng, chúng ta thêm cờ :c:macro:`Py_TPFLAGS_HAVE_GC` vào các cờ của lớp::

   .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC,

Về cơ bản là xong. Nếu chúng ta đã viết :c:member:`~PyTypeObject.tp_alloc` tùy chỉnh hoặc
:c:member:`~PyTypeObject.tp_free` handlers, chúng ta sẽ cần sửa đổi chúng để hỗ trợ thu gom rác theo chu kỳ. Hầu hết các extension sẽ tự động sử dụng những phiên bản được cung cấp sẵn.


Kế thừa các kiểu khác
=====================

Có thể tạo các kiểu extension mới được dẫn xuất từ các kiểu hiện có. Việc kế thừa từ các kiểu dựng sẵn là dễ nhất, vì extension có thể dễ dàng sử dụng :c:type:`PyTypeObject` mà nó cần. Việc chia sẻ các cấu trúc :c:type:`PyTypeObject` này giữa các mô-đun extension có thể khó khăn.

Trong ví dụ này, chúng ta sẽ tạo một kiểu :class:`!SubList` kế thừa từ kiểu :class:`list` dựng sẵn. Kiểu mới sẽ hoàn toàn tương thích với các list thông thường, nhưng sẽ có thêm phương thức :meth:`!increment` để tăng một bộ đếm nội bộ:

.. code-block:: pycon

   >>> import sublist
   >>> s = sublist.SubList(range(3))
   >>> s.extend(s)
   >>> print(len(s))
   6
   >>> print(s.increment())
   1
   >>> print(s.increment())
   2

.. literalinclude:: ../includes/newtypes/sublist.c


Như bạn có thể thấy, mã nguồn rất giống với các ví dụ :class:`!Custom` trong những phần trước. Chúng ta sẽ phân tích những điểm khác biệt chính giữa chúng.::

   typedef struct {
       PyListObject list;
       int state;
   } SubListObject;

Điểm khác biệt chính đối với các đối tượng kiểu dẫn xuất là cấu trúc đối tượng của kiểu cơ sở phải là giá trị đầu tiên. Kiểu cơ sở đã bao gồm :c:func:`PyObject_HEAD` ở đầu cấu trúc của nó.

Khi một đối tượng Python là một thể hiện :class:`!SubList`, con trỏ ``PyObject *`` của nó có thể được ép kiểu an toàn thành cả ``PyListObject *`` và ``SubListObject *``::

   static int
   SubList_init(PyObject *op, PyObject *args, PyObject *kwds)
   {
       SubListObject *self = (SubListObject *) op;
       if (PyList_Type.tp_init(op, args, kwds) < 0)
           return -1;
       self->state = 0;
       return 0;
   }

Như đã thấy ở trên, chúng ta có thể gọi đến phương thức :meth:`~object.__init__` của kiểu cơ sở.

Mẫu này rất quan trọng khi viết một kiểu tùy chỉnh
:c:member:`~PyTypeObject.tp_new` và :c:member:`~PyTypeObject.tp_dealloc` thành viên. Trình xử lý :c:member:`~PyTypeObject.tp_new` không nên thực sự tạo vùng nhớ cho đối tượng bằng :c:member:`~PyTypeObject.tp_alloc` của nó, mà để lớp cơ sở xử lý việc đó bằng cách gọi :c:member:`~PyTypeObject.tp_new` của chính lớp đó.

Cấu trúc :c:type:`PyTypeObject` hỗ trợ một :c:member:`~PyTypeObject.tp_base` chỉ định lớp cơ sở cụ thể của kiểu. Do các vấn đề về trình biên dịch đa nền tảng, bạn không thể điền trực tiếp trường đó bằng một tham chiếu đến
:c:type:`PyList_Type`; việc này nên được thực hiện trong hàm :c:data:`Py_mod_exec`::

   static int
   sublist_module_exec(PyObject *m)
   {
       SubListType.tp_base = &PyList_Type;
       if (PyType_Ready(&SubListType) < 0) {
           return -1;
       }

       if (PyModule_AddObjectRef(m, "SubList", (PyObject *) &SubListType) < 0) {
           return -1;
       }

       return 0;
   }

Trước khi gọi :c:func:`PyType_Ready`, cấu trúc kiểu phải có slot
:c:member:`~PyTypeObject.tp_base` được điền. Khi dẫn xuất một kiểu hiện có, không cần điền slot :c:member:`~PyTypeObject.tp_alloc` bằng :c:func:`PyType_GenericNew` -- hàm cấp phát từ kiểu cơ sở sẽ được kế thừa.

Sau đó, việc gọi :c:func:`PyType_Ready` và thêm đối tượng type vào module cũng giống như trong các ví dụ :class:`!Custom` cơ bản.


.. rubric:: Chú thích

.. [#] Điều này đúng khi chúng ta biết đối tượng là một kiểu cơ bản, chẳng hạn như string hoặc float.

.. [#] Chúng ta đã dựa vào điều này trong handler :c:member:`~PyTypeObject.tp_dealloc` ở ví dụ này, vì type của chúng ta không hỗ trợ garbage collection.

.. [#] Bây giờ chúng ta biết rằng member đầu tiên và cuối cùng là string, nên có lẽ chúng ta có thể bớt thận trọng hơn khi giảm reference count của chúng. Tuy nhiên, chúng ta chấp nhận các instance của subclass string. Mặc dù việc giải phóng các string thông thường sẽ không gọi ngược vào các object của chúng ta, chúng ta không thể đảm bảo rằng việc giải phóng một instance của subclass string sẽ không gọi ngược vào các object của chúng ta.

.. [#] Ngoài ra, ngay cả khi các attribute của chúng ta chỉ giới hạn ở các instance string, người dùng vẫn có thể truyền các subclass :class:`str` tùy ý và do đó vẫn tạo ra các reference cycle.
