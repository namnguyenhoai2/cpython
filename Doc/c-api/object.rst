.. highlight:: c

.. _object:

Giao thức đối tượng
===================


.. c:function:: PyObject* Py_GetConstant(unsigned int constant_id)

   Lấy một :term:`strong reference` tới một hằng số.

   Đặt một ngoại lệ và trả về ``NULL`` nếu *constant_id* không hợp lệ.

   *constant_id* phải là một trong các mã định danh hằng số sau:

   .. c:namespace:: NULL

   +------------------------------------------+---------+---------------------------+
   | Mã định danh hằng số                     | Giá trị | Đối tượng được trả về     |
   +==========================================+=========+===========================+
   | .. c:macro:: Py_CONSTANT_NONE            | ``0``   | :py:data:`None`           |
   +------------------------------------------+---------+---------------------------+
   | .. c:macro:: Py_CONSTANT_FALSE           | ``1``   | :py:data:`False`          |
   +------------------------------------------+---------+---------------------------+
   | .. c:macro:: Py_CONSTANT_TRUE            | ``2``   | :py:data:`True`           |
   +------------------------------------------+---------+---------------------------+
   | .. c:macro:: Py_CONSTANT_ELLIPSIS        | ``3``   | :py:data:`Ellipsis`       |
   +------------------------------------------+---------+---------------------------+
   | .. c:macro:: Py_CONSTANT_NOT_IMPLEMENTED | ``4``   | :py:data:`NotImplemented` |
   +------------------------------------------+---------+---------------------------+
   | .. c:macro:: Py_CONSTANT_ZERO            | ``5``   | ``0``                     |
   +------------------------------------------+---------+---------------------------+
   | .. c:macro:: Py_CONSTANT_ONE             | ``6``   | ``1``                     |
   +------------------------------------------+---------+---------------------------+
   | .. c:macro:: Py_CONSTANT_EMPTY_STR       | ``7``   | ``''``                    |
   +------------------------------------------+---------+---------------------------+
   | .. c:macro:: Py_CONSTANT_EMPTY_BYTES     | ``8``   | ``b''``                   |
   +------------------------------------------+---------+---------------------------+
   | .. c:macro:: Py_CONSTANT_EMPTY_TUPLE     | ``9``   | ``()``                    |
   +------------------------------------------+---------+---------------------------+

   Các giá trị số chỉ được cung cấp cho những dự án không thể sử dụng các mã định danh hằng số.


   .. versionadded:: 3.13

   .. impl-detail::

      Trong CPython, tất cả các hằng số này đều là :term:`immortal`.


.. c:function:: PyObject* Py_GetConstantBorrowed(unsigned int constant_id)

   Tương tự như :c:func:`Py_GetConstant`, nhưng trả về một :term:`borrowed reference`.

   Hàm này chủ yếu nhằm đảm bảo khả năng tương thích ngược: nên sử dụng :c:func:`Py_GetConstant` trong mã mới.

   Tham chiếu này được mượn từ interpreter và hợp lệ cho đến khi interpreter hoàn tất quá trình kết thúc.

   .. versionadded:: 3.13


.. c:var:: PyObject* Py_NotImplemented

   Singleton ``NotImplemented``, được dùng để báo hiệu rằng một thao tác không được triển khai cho tổ hợp kiểu đã cho.


.. c:macro:: Py_RETURN_NOTIMPLEMENTED

   Xử lý đúng việc trả về :c:data:`Py_NotImplemented` từ bên trong một hàm C (tức là tạo một :term:`strong reference` mới để :const:`NotImplemented` và trả về nó).


.. c:macro:: Py_PRINT_RAW

   Cờ được dùng với nhiều hàm in đối tượng (chẳng hạn như
   :c:func:`PyObject_Print` và :c:func:`PyFile_WriteObject`). Nếu được truyền vào, các hàm này sử dụng :func:`str` của đối tượng thay vì :func:`repr`.


.. c:function:: int PyObject_Print(PyObject *o, FILE *fp, int flags)

   In một đối tượng *o* vào tệp *fp*. Trả về ``-1`` nếu xảy ra lỗi. Đối số flags được dùng để bật một số tùy chọn in nhất định. Tùy chọn duy nhất hiện được hỗ trợ là :c:macro:`Py_PRINT_RAW`; nếu được chỉ định, :func:`str` của đối tượng sẽ được ghi thay vì :func:`repr`.


.. c:function:: int PyObject_HasAttrWithError(PyObject *o, PyObject *attr_name)

   Trả về ``1`` nếu *o* có thuộc tính *attr_name*, và ``0`` nếu không. Điều này tương đương với biểu thức Python ``hasattr(o, attr_name)``. Nếu thất bại, trả về ``-1``.

   .. versionadded:: 3.13


.. c:function:: int PyObject_HasAttrStringWithError(PyObject *o, const char *attr_name)

   Tương tự như :c:func:`PyObject_HasAttrWithError`, nhưng *attr_name* được chỉ định dưới dạng chuỗi byte được mã hóa UTF-8 :c:expr:`const char*`, thay vì :c:expr:`PyObject*`.

   .. versionadded:: 3.13


.. c:function:: int PyObject_HasAttr(PyObject *o, PyObject *attr_name)

   Trả về ``1`` nếu *o* có thuộc tính *attr_name*, và ``0`` nếu không. Hàm này luôn thành công.

   .. note::

      Các ngoại lệ xảy ra khi hàm này gọi :meth:`~object.__getattr__` và
      Các phương thức :meth:`~object.__getattribute__` không được truyền tiếp mà thay vào đó được chuyển cho :func:`sys.unraisablehook`. Để xử lý lỗi đúng cách, hãy sử dụng :c:func:`PyObject_HasAttrWithError`,
      :c:func:`PyObject_GetOptionalAttr` hoặc :c:func:`PyObject_GetAttr` thay vào đó.


.. c:function:: int PyObject_HasAttrString(PyObject *o, const char *attr_name)

   Điều này giống với :c:func:`PyObject_HasAttr`, nhưng *attr_name* được chỉ định dưới dạng một chuỗi byte được mã hóa UTF-8 :c:expr:`const char*`, thay vì một :c:expr:`PyObject*`.

   .. note::

      Các ngoại lệ xảy ra khi hàm này gọi :meth:`~object.__getattr__` và
      các phương thức :meth:`~object.__getattribute__` hoặc trong khi tạo đối tượng tạm thời
      Đối tượng :class:`str` bị bỏ qua mà không báo lỗi. Để xử lý lỗi đúng cách, hãy sử dụng :c:func:`PyObject_HasAttrStringWithError`,
      :c:func:`PyObject_GetOptionalAttrString` hoặc :c:func:`PyObject_GetAttrString` thay vào đó.


.. c:function:: PyObject* PyObject_GetAttr(PyObject *o, PyObject *attr_name)

   Lấy một thuộc tính có tên *attr_name* từ đối tượng *o*. Trả về giá trị thuộc tính nếu thành công hoặc ``NULL`` nếu thất bại. Đây là tương đương với biểu thức Python ``o.attr_name``.

   Nếu không nên xem việc thiếu thuộc tính là một lỗi, bạn có thể sử dụng
   :c:func:`PyObject_GetOptionalAttr` thay thế.


.. c:function:: PyObject* PyObject_GetAttrString(PyObject *o, const char *attr_name)

   Tương tự như :c:func:`PyObject_GetAttr`, nhưng *attr_name* được chỉ định dưới dạng chuỗi byte được mã hóa UTF-8 :c:expr:`const char*`, thay vì một :c:expr:`PyObject*`.

   Nếu không nên xem việc thiếu thuộc tính là một lỗi, bạn có thể sử dụng
   :c:func:`PyObject_GetOptionalAttrString` thay thế.


.. c:function:: int PyObject_GetOptionalAttr(PyObject *obj, PyObject *attr_name, PyObject **result);

   Biến thể của :c:func:`PyObject_GetAttr` không phát sinh lỗi
   :exc:`AttributeError` nếu không tìm thấy thuộc tính.

   Nếu tìm thấy thuộc tính, trả về ``1`` và đặt *\*result* thành một giá trị mới
   :term:`strong reference` cho thuộc tính. Nếu không tìm thấy thuộc tính, trả về ``0`` và đặt *\*result* thành ``NULL``; :exc:`AttributeError` sẽ bị bỏ qua. Nếu phát sinh lỗi khác với :exc:`AttributeError`, trả về ``-1`` và đặt *\*result* thành ``NULL``.

   .. versionadded:: 3.13


.. c:function:: int PyObject_GetOptionalAttrString(PyObject *obj, const char *attr_name, PyObject **result);

   Điều này tương tự như :c:func:`PyObject_GetOptionalAttr`, nhưng *attr_name* được chỉ định dưới dạng một chuỗi byte được mã hóa bằng UTF-8 :c:expr:`const char*`, thay vì một :c:expr:`PyObject*`.

   .. versionadded:: 3.13

.. c:function:: PyObject* PyObject_GenericGetAttr(PyObject *o, PyObject *name)

   Hàm getter thuộc tính generic, được dùng để đặt vào ``tp_getattro`` slot của một đối tượng kiểu. Hàm này tìm descriptor trong từ điển của các lớp thuộc MRO của đối tượng, cũng như một thuộc tính trong
   :attr:`~object.__dict__` của đối tượng (nếu có). Như đã nêu trong :ref:`descriptors`, data descriptor được ưu tiên hơn thuộc tính instance, còn non-data descriptor thì không. Nếu không, một :exc:`AttributeError` sẽ được phát sinh.


.. c:function:: int PyObject_SetAttr(PyObject *o, PyObject *attr_name, PyObject *v)

   Đặt giá trị của thuộc tính có tên *attr_name* cho đối tượng *o* thành giá trị *v*. Phát sinh một ngoại lệ và trả về ``-1`` khi thất bại; trả về ``0`` khi thành công. Điều này tương đương với câu lệnh Python ``o.attr_name = v``.

   Nếu *v* là ``NULL``, thuộc tính sẽ bị xóa. Hành vi này không còn được khuyến nghị và nên dùng :c:func:`PyObject_DelAttr` thay thế, nhưng hiện chưa có kế hoạch loại bỏ nó.


.. c:function:: int PyObject_SetAttrString(PyObject *o, const char *attr_name, PyObject *v)

   Điều này tương tự :c:func:`PyObject_SetAttr`, nhưng *attr_name* được chỉ định dưới dạng chuỗi byte được mã hóa UTF-8 :c:expr:`const char*`, thay vì một :c:expr:`PyObject*`.

   Nếu *v* là ``NULL``, thuộc tính sẽ bị xóa, nhưng tính năng này không còn được khuyến nghị và nên dùng :c:func:`PyObject_DelAttrString` thay thế.

   Nên giữ số lượng tên thuộc tính khác nhau được truyền cho hàm này ở mức thấp, thường bằng cách sử dụng một chuỗi được cấp phát tĩnh làm *attr_name*. Đối với các tên thuộc tính chưa được biết tại thời điểm biên dịch, nên gọi
   :c:func:`PyUnicode_FromString` và :c:func:`PyObject_SetAttr` trực tiếp. Để biết thêm chi tiết, hãy xem :c:func:`PyUnicode_InternFromString`, đối tượng này có thể được dùng nội bộ để tạo một đối tượng khóa.

.. c:function:: int PyObject_GenericSetAttr(PyObject *o, PyObject *name, PyObject *value)

   Hàm setter và deleter thuộc tính tổng quát, được thiết kế để đặt vào slot :c:member:`~PyTypeObject.tp_setattro` của một đối tượng kiểu. Hàm tìm kiếm một data descriptor trong từ điển của các lớp thuộc MRO của đối tượng; nếu tìm thấy, descriptor đó được ưu tiên hơn việc đặt hoặc xóa thuộc tính trong từ điển của instance. Nếu không, thuộc tính sẽ được đặt hoặc xóa trong :attr:`~object.__dict__` của đối tượng (nếu có). Khi thành công, hàm trả về ``0``; nếu không, một :exc:`AttributeError` được phát sinh và ``-1`` được trả về.


.. c:function:: int PyObject_DelAttr(PyObject *o, PyObject *attr_name)

   Xóa thuộc tính có tên *attr_name* của đối tượng *o*. Trả về ``-1`` nếu thất bại. Đây là cách tương đương với câu lệnh Python ``del o.attr_name``.


.. c:function:: int PyObject_DelAttrString(PyObject *o, const char *attr_name)

   Điều này tương tự như :c:func:`PyObject_DelAttr`, nhưng *attr_name* được chỉ định dưới dạng chuỗi byte được mã hóa UTF-8 :c:expr:`const char*`, thay vì :c:expr:`PyObject*`.

   Nên giữ số lượng tên thuộc tính khác nhau được truyền cho hàm này ở mức thấp, thường bằng cách sử dụng một chuỗi được cấp phát tĩnh làm *attr_name*. Đối với các tên thuộc tính chưa được biết tại thời điểm biên dịch, nên gọi
   :c:func:`PyUnicode_FromString` và :c:func:`PyObject_DelAttr` trực tiếp. Để biết thêm chi tiết, hãy xem :c:func:`PyUnicode_InternFromString`, có thể được sử dụng nội bộ để tạo một đối tượng khóa dùng cho việc tra cứu.


.. c:function:: PyObject* PyObject_GenericGetDict(PyObject *o, void *context)

   Một triển khai tổng quát cho getter của descriptor ``__dict__``. Hàm này tạo dictionary nếu cần.

   Hàm này cũng có thể được gọi để lấy :py:attr:`~object.__dict__` của đối tượng *o*. Truyền ``NULL`` cho *context* khi gọi hàm. Vì hàm này có thể cần cấp phát bộ nhớ cho dictionary, việc gọi :c:func:`PyObject_GetAttr` khi truy cập một attribute trên đối tượng có thể hiệu quả hơn.

   Nếu xảy ra lỗi, trả về ``NULL`` và thiết lập exception.

   .. versionadded:: 3.3


.. c:function:: int PyObject_GenericSetDict(PyObject *o, PyObject *value, void *context)

   Một triển khai tổng quát cho setter của descriptor ``__dict__``. Triển khai này không cho phép xóa dictionary.

   .. versionadded:: 3.3


.. c:function:: PyObject** _PyObject_GetDictPtr(PyObject *obj)

   Trả về một con trỏ tới :py:attr:`~object.__dict__` của đối tượng *obj*. Nếu không có ``__dict__``, trả về ``NULL`` mà không đặt ngoại lệ.

   Hàm này có thể cần cấp phát bộ nhớ cho dictionary, vì vậy có thể hiệu quả hơn nếu gọi :c:func:`PyObject_GetAttr` khi truy cập một thuộc tính trên đối tượng.


.. c:function:: PyObject* PyObject_RichCompare(PyObject *o1, PyObject *o2, int opid)

   So sánh các giá trị của *o1* và *o2* bằng thao tác được chỉ định bởi *opid*, phải là một trong :c:macro:`Py_LT`, :c:macro:`Py_LE`, :c:macro:`Py_EQ`,
   :c:macro:`Py_NE`, :c:macro:`Py_GT` hoặc :c:macro:`Py_GE`, lần lượt tương ứng với ``<``, ``<=``, ``==``, ``!=``, ``>`` hoặc ``>=``. Đây là tương đương với biểu thức Python ``o1 op o2``, trong đó ``op`` là toán tử tương ứng với *opid*. Trả về giá trị của phép so sánh khi thành công hoặc ``NULL`` khi thất bại.


.. c:function:: int PyObject_RichCompareBool(PyObject *o1, PyObject *o2, int opid)

   So sánh các giá trị của *o1* và *o2* bằng thao tác được chỉ định bởi *opid*, tương tự như :c:func:`PyObject_RichCompare`, nhưng trả về ``-1`` khi xảy ra lỗi, ``0`` nếu kết quả là false và ``1`` trong các trường hợp còn lại.

.. note::
   Nếu *o1* và *o2* là cùng một đối tượng, :c:func:`PyObject_RichCompareBool` sẽ luôn trả về ``1`` cho :c:macro:`Py_EQ` và ``0`` cho :c:macro:`Py_NE`.

.. c:function:: PyObject* PyObject_Format(PyObject *obj, PyObject *format_spec)

   Định dạng *obj* bằng *format_spec*. Tương đương với biểu thức Python ``format(obj, format_spec)``.

   *format_spec* có thể là ``NULL``. Trong trường hợp này, lệnh gọi tương đương với ``format(obj)``. Trả về chuỗi đã định dạng nếu thành công, ``NULL`` nếu thất bại.

.. c:function:: PyObject* PyObject_Repr(PyObject *o)

   .. index:: pair: built-in function; repr

   Tính biểu diễn chuỗi của đối tượng *o*. Trả về biểu diễn chuỗi nếu thành công, ``NULL`` nếu thất bại. Đây là tương đương với biểu thức Python ``repr(o)``. Được gọi bởi hàm built-in :func:`repr`.

   Nếu đối số là ``NULL``, trả về chuỗi ``'<NULL>'``.

   .. versionchanged:: 3.4
      Hàm này hiện bao gồm một debug assertion để giúp bảo đảm rằng hàm không âm thầm loại bỏ một exception đang hoạt động.

.. c:function:: PyObject* PyObject_ASCII(PyObject *o)

   .. index:: pair: built-in function; ascii

   Tương tự như :c:func:`PyObject_Repr`, tính biểu diễn chuỗi của đối tượng *o*, nhưng escape các ký tự không phải ASCII trong chuỗi được trả về bởi
   :c:func:`PyObject_Repr` bằng các escape ``\x``, ``\u`` hoặc ``\U``. Điều này tạo ra một chuỗi tương tự chuỗi được trả về bởi :c:func:`PyObject_Repr` trong Python 2. Được gọi bởi hàm built-in :func:`ascii`.

   Nếu đối số là ``NULL``, trả về chuỗi ``'<NULL>'``.

   .. index:: string; PyObject_Str (C function)


.. c:function:: PyObject* PyObject_Str(PyObject *o)

   Tính biểu diễn chuỗi của đối tượng *o*. Trả về biểu diễn chuỗi khi thành công và ``NULL`` khi thất bại. Đây là tương đương với biểu thức Python ``str(o)``. Được gọi bởi hàm dựng sẵn :func:`str` và do đó bởi hàm :func:`print`.

   Nếu đối số là ``NULL``, trả về chuỗi ``'<NULL>'``.

   .. versionchanged:: 3.4
      Hàm này hiện bao gồm một debug assertion để giúp bảo đảm rằng hàm không âm thầm loại bỏ một exception đang hoạt động.


.. c:function:: PyObject* PyObject_Bytes(PyObject *o)

   .. index:: pair: built-in function; bytes

   Tính biểu diễn bytes của đối tượng *o*. Trả về ``NULL`` khi thất bại và một đối tượng bytes khi thành công. Tương đương với biểu thức Python ``bytes(o)`` khi *o* không phải là số nguyên. Không giống như ``bytes(o)``, một TypeError sẽ được phát sinh khi *o* là số nguyên thay vì một đối tượng bytes được khởi tạo bằng các giá trị 0.

   Nếu đối số là ``NULL``, trả về đối tượng :class:`bytes` ``b'<NULL>'``.


.. c:function:: int PyObject_IsSubclass(PyObject *derived, PyObject *cls)

   Trả về ``1`` nếu lớp *derived* giống hệt hoặc được dẫn xuất từ lớp *cls*, nếu không thì trả về ``0``. Nếu xảy ra lỗi, trả về ``-1``.

   Nếu *cls* là một tuple, phép kiểm tra sẽ được thực hiện với từng mục trong *cls*. Kết quả sẽ là ``1`` khi ít nhất một phép kiểm tra trả về ``1``, nếu không sẽ là ``0``.

   Nếu *cls* có phương thức :meth:`~type.__subclasscheck__`, phương thức này sẽ được gọi để xác định trạng thái lớp con như mô tả trong :pep:`3119`. Nếu không, *derived* là lớp con của *cls* nếu nó là lớp con trực tiếp hoặc gián tiếp, tức là được chứa trong :attr:`cls.__mro__ <type.__mro__>`.

   Thông thường, chỉ các đối tượng lớp, tức là các thực thể của :class:`type` hoặc của một lớp dẫn xuất, mới được xem là lớp. Tuy nhiên, các đối tượng có thể ghi đè điều này bằng cách có thuộc tính :attr:`~type.__bases__` (thuộc tính này phải là một tuple gồm các lớp cơ sở).


.. c:function:: int PyObject_IsInstance(PyObject *inst, PyObject *cls)

   Trả về ``1`` nếu *inst* là một thực thể của lớp *cls* hoặc của một lớp con của *cls*, hoặc trả về ``0`` nếu không phải. Khi xảy ra lỗi, trả về ``-1`` và thiết lập một exception.

   Nếu *cls* là một tuple, phép kiểm tra sẽ được thực hiện với từng mục trong *cls*. Kết quả sẽ là ``1`` khi ít nhất một phép kiểm tra trả về ``1``, nếu không sẽ là ``0``.

   Nếu *cls* có phương thức :meth:`~type.__instancecheck__`, phương thức này sẽ được gọi để xác định trạng thái lớp con như mô tả trong :pep:`3119`. Nếu không, *inst* là một thực thể của *cls* nếu lớp của nó là lớp con của *cls*.

   Một thực thể *inst* có thể ghi đè lớp được xem là lớp của nó bằng cách có một
   :attr:`~object.__class__` thuộc tính.

   Một đối tượng *cls* có thể ghi đè việc nó có được xem là một class hay không và các base class của nó là gì bằng cách có thuộc tính :attr:`~type.__bases__` (thuộc tính này phải là một tuple gồm các base class).


.. c:function:: Py_hash_t PyObject_Hash(PyObject *o)

   .. index:: pair: built-in function; hash

   Tính toán và trả về giá trị hash của một đối tượng *o*. Khi thất bại, trả về ``-1``. Đây là cách tương đương với biểu thức Python ``hash(o)``.

   .. versionchanged:: 3.2
      Kiểu trả về hiện là Py_hash_t. Đây là một số nguyên có dấu, có cùng kích thước với :c:type:`Py_ssize_t`.


.. c:function:: Py_hash_t PyObject_HashNotImplemented(PyObject *o)

   Thiết lập một :exc:`TypeError` cho biết rằng ``type(o)`` không phải là :term:`hashable` rồi trả về ``-1``. Hàm này được xử lý đặc biệt khi được lưu trong một slot ``tp_hash``, cho phép một type chỉ rõ với interpreter rằng nó không thể hash.


.. c:function:: int PyObject_IsTrue(PyObject *o)

   Trả về ``1`` nếu đối tượng *o* được xem là true, và ``0`` nếu ngược lại. Tương đương với biểu thức Python ``not not o``. Khi thất bại, trả về ``-1``.


.. c:function:: int PyObject_Not(PyObject *o)

   Trả về ``0`` nếu đối tượng *o* được xem là true, và ``1`` nếu ngược lại. Tương đương với biểu thức Python ``not o``. Khi thất bại, trả về ``-1``.


.. c:function:: PyObject* PyObject_Type(PyObject *o)

   .. index:: pair: built-in function; type

   Khi *o* không phải là ``NULL``, trả về một đối tượng type tương ứng với object type của đối tượng *o*. Khi thất bại, phát sinh :exc:`SystemError` và trả về ``NULL``. Tương đương với biểu thức Python ``type(o)``. Hàm này tạo một :term:`strong reference` mới tới giá trị trả về. Thực sự không có lý do gì để sử dụng hàm này thay cho hàm :c:func:`Py_TYPE()`, vốn trả về một con trỏ kiểu :c:expr:`PyTypeObject*`, ngoại trừ khi một
   :term:`strong reference` là cần thiết.


.. c:function:: int PyObject_TypeCheck(PyObject *o, PyTypeObject *type)

   Trả về giá trị khác 0 nếu đối tượng *o* có kiểu *type* hoặc là kiểu con của *type*, và ``0`` trong các trường hợp khác. Cả hai tham số phải khác ``NULL``.


.. c:function:: Py_ssize_t PyObject_Size(PyObject *o)
               Py_ssize_t PyObject_Length(PyObject *o)

   .. index:: pair: built-in function; len

   Trả về độ dài của đối tượng *o*. Nếu đối tượng *o* cung cấp một trong các protocol sequence và mapping, độ dài sequence sẽ được trả về. Khi xảy ra lỗi, ``-1`` được trả về. Tương đương với biểu thức Python ``len(o)``.


.. c:function:: Py_ssize_t PyObject_LengthHint(PyObject *o, Py_ssize_t defaultvalue)

   Trả về độ dài ước tính của đối tượng *o*. Trước tiên, cố gắng trả về độ dài thực tế của đối tượng, sau đó ước tính bằng :meth:`~object.__length_hint__`, và cuối cùng trả về giá trị mặc định. Khi xảy ra lỗi, trả về ``-1``. Tương đương với biểu thức Python ``operator.length_hint(o, defaultvalue)``.

   .. versionadded:: 3.4


.. c:function:: PyObject* PyObject_GetItem(PyObject *o, PyObject *key)

   Trả về phần tử của *o* tương ứng với đối tượng *key*, hoặc ``NULL`` khi thất bại. Tương đương với biểu thức Python ``o[key]``.


.. c:function:: int PyObject_SetItem(PyObject *o, PyObject *key, PyObject *v)

   Ánh xạ đối tượng *key* tới giá trị *v*. Khi thất bại, phát sinh một ngoại lệ và trả về ``-1``; khi thành công, trả về ``0``. Tương đương với câu lệnh Python ``o[key] = v``. Hàm này *does not* lấy quyền sở hữu tham chiếu của *v*.


.. c:function:: int PyObject_DelItem(PyObject *o, PyObject *key)

   Xóa ánh xạ cho đối tượng *key* khỏi đối tượng *o*. Trả về ``-1`` nếu thất bại. Điều này tương đương với câu lệnh Python ``del o[key]``.


.. c:function:: int PyObject_DelItemString(PyObject *o, const char *key)

   Điều này giống với :c:func:`PyObject_DelItem`, nhưng *key* được chỉ định dưới dạng chuỗi byte được mã hóa UTF-8 :c:expr:`const char*`, thay vì một :c:expr:`PyObject*`.


.. c:function:: PyObject* PyObject_Dir(PyObject *o)

   Điều này tương đương với biểu thức Python ``dir(o)``, trả về một danh sách (có thể rỗng) các chuỗi phù hợp với đối số đối tượng, hoặc ``NULL`` nếu xảy ra lỗi. Nếu đối số là ``NULL``, điều này tương tự Python ``dir()``, trả về tên của các biến cục bộ hiện tại; trong trường hợp này, nếu không có execution frame nào đang hoạt động thì ``NULL`` được trả về, nhưng :c:func:`PyErr_Occurred` sẽ trả về false.


.. c:function:: PyObject* PyObject_GetIter(PyObject *o)

   Điều này tương đương với biểu thức Python ``iter(o)``. Nó trả về một iterator mới cho đối số đối tượng, hoặc chính đối tượng đó nếu đối tượng đã là một iterator. Phát sinh :exc:`TypeError` và trả về ``NULL`` nếu không thể lặp qua đối tượng.


.. c:function:: PyObject* PyObject_SelfIter(PyObject *obj)

   Điều này tương đương với phương thức Python ``__iter__(self): return self``. Phương thức này dành cho các kiểu :term:`iterator`, được sử dụng trong slot :c:member:`PyTypeObject.tp_iter`.


.. c:function:: PyObject* PyObject_GetAIter(PyObject *o)

   Đây là tương đương với biểu thức Python ``aiter(o)``. Nhận một
   đối tượng :class:`AsyncIterable` và trả về một :class:`AsyncIterator` cho đối tượng đó. Thông thường đây là một iterator mới, nhưng nếu đối số là một
   :class:`AsyncIterator`, phương thức này trả về chính nó. Gây ra :exc:`TypeError` và trả về ``NULL`` nếu đối tượng không thể được lặp qua.

   .. versionadded:: 3.10

.. c:function:: void *PyObject_GetTypeData(PyObject *o, PyTypeObject *cls)

   Lấy một con trỏ tới dữ liệu dành riêng cho lớp con được dành cho *cls*.

   Đối tượng *o* phải là một thực thể của *cls*, và *cls* phải được tạo bằng :c:member:`PyType_Spec.basicsize` âm. Python không kiểm tra điều này.

   Khi xảy ra lỗi, đặt một exception và trả về ``NULL``.

   .. versionadded:: 3.12

.. c:function:: Py_ssize_t PyType_GetTypeDataSize(PyTypeObject *cls)

   Trả về kích thước vùng bộ nhớ của thực thể được dành riêng cho *cls*, tức là kích thước bộ nhớ mà :c:func:`PyObject_GetTypeData` trả về.

   Kích thước này có thể lớn hơn kích thước được yêu cầu bằng :c:member:`-PyType_Spec.basicsize <PyType_Spec.basicsize>`; việc sử dụng kích thước lớn hơn này là an toàn (ví dụ: với :c:func:`!memset`).

   Kiểu *cls* **phải** được tạo bằng :c:member:`PyType_Spec.basicsize` âm. Python không kiểm tra điều này.

   Khi xảy ra lỗi, hãy đặt một exception và trả về một giá trị âm.

   .. versionadded:: 3.12

.. c:function:: void *PyObject_GetItemData(PyObject *o)

   Lấy con trỏ tới dữ liệu trên từng mục cho một lớp có
   :c:macro:`Py_TPFLAGS_ITEMS_AT_END`.

   Khi xảy ra lỗi, đặt một exception và trả về ``NULL``.
   :py:exc:`TypeError` được phát sinh nếu *o* không có
   :c:macro:`Py_TPFLAGS_ITEMS_AT_END` được đặt.

   .. versionadded:: 3.12

.. c:function:: int PyObject_VisitManagedDict(PyObject *obj, visitproc visit, void *arg)

   Truy cập dictionary được quản lý của *obj*.

   Hàm này chỉ được gọi trong một hàm traverse của kiểu có cờ :c:macro:`Py_TPFLAGS_MANAGED_DICT` được đặt.

   .. versionadded:: 3.13

.. c:function:: void PyObject_ClearManagedDict(PyObject *obj)

   Xóa dictionary được quản lý của *obj*.

   Chỉ được gọi hàm này trong hàm clear của kiểu có đặt cờ :c:macro:`Py_TPFLAGS_MANAGED_DICT`.

   .. versionadded:: 3.13

.. c:function:: int PyUnstable_Object_EnableDeferredRefcount(PyObject *obj)

   Bật `deferred reference counting <https://peps.python.org/pep-0703/#deferred-reference-counting>`_ trên *obj*, nếu runtime hỗ trợ. Trong bản build :term:`free-threaded <free threading>`, việc này cho phép interpreter tránh điều chỉnh reference count cho *obj*, nhờ đó có thể cải thiện hiệu năng đa luồng. Đổi lại, *obj* sẽ chỉ được giải phóng bởi tracing garbage collector, thay vì khi interpreter không còn bất kỳ reference nào đến đối tượng.

   Hàm này trả về ``1`` nếu deferred reference counting được bật trên *obj*, và ``0`` nếu deferred reference counting không được hỗ trợ hoặc nếu interpreter bỏ qua gợi ý này, chẳng hạn khi deferred reference counting đã được bật trên *obj*. Hàm này an toàn khi chạy trong môi trường đa luồng và không thể thất bại.

   Hàm này không thực hiện thao tác nào trên các bản build bật :term:`GIL`, vốn không hỗ trợ deferred reference counting. Hàm cũng không thực hiện thao tác nào nếu *obj* không phải là đối tượng được garbage collector theo dõi (xem :func:`gc.is_tracked` và
   :c:func:`PyObject_GC_IsTracked`).

   Hàm này được dùng ngay sau khi *obj* được tạo, bởi đoạn code tạo đối tượng đó, chẳng hạn trong slot :c:member:`~PyTypeObject.tp_new` của đối tượng.

   .. versionadded:: 3.14

.. c:function:: int PyUnstable_Object_IsUniqueReferencedTemporary(PyObject *obj)

   Kiểm tra xem *obj* có phải là một temporary object duy nhất hay không. Trả về ``1`` nếu *obj* được xác định là một temporary object duy nhất, và ``0`` trong các trường hợp còn lại. Hàm này không thể thất bại, nhưng phép kiểm tra mang tính thận trọng và trong một số trường hợp có thể trả về ``0`` ngay cả khi *obj* là một temporary object duy nhất.

   Nếu một đối tượng là temporary duy nhất, thì chắc chắn rằng mã hiện tại là nơi duy nhất tham chiếu đến đối tượng đó. Đối với các đối số của hàm C, nên sử dụng điều này thay vì kiểm tra xem số lượng tham chiếu có phải là ``1`` hay không. Bắt đầu từ Python 3.14, trình thông dịch nội bộ tránh một số thao tác sửa đổi số lượng tham chiếu khi tải các đối tượng lên ngăn xếp toán hạng bằng cách
   :term:`borrowing <borrowed reference>` các tham chiếu khi có thể, nghĩa là chỉ riêng số lượng tham chiếu bằng ``1`` không đảm bảo rằng một đối số của hàm được tham chiếu duy nhất.

   Trong ví dụ dưới đây, ``my_func`` được gọi với một đối tượng temporary duy nhất làm đối số::

      my_func([1, 2, 3])

   Trong ví dụ dưới đây, ``my_func`` **not** được gọi với một đối tượng temporary duy nhất làm đối số, ngay cả khi refcount của đối tượng là ``1``::

      my_list = [1, 2, 3]
      my_func(my_list)

   Xem thêm hàm :c:func:`Py_REFCNT`.

   .. versionadded:: 3.14

.. c:function:: int PyUnstable_IsImmortal(PyObject *obj)

   Hàm này trả về giá trị khác 0 nếu *obj* là :term:`immortal`, và trả về 0 trong các trường hợp khác. Hàm này không thể thất bại.

   .. note::

      Các đối tượng là immortal trong một phiên bản CPython không được đảm bảo là immortal trong phiên bản khác.

   .. versionadded:: 3.14

.. c:function:: int PyUnstable_TryIncRef(PyObject *obj)

   Tăng số lượng tham chiếu của *obj* nếu giá trị này khác không. Trả về ``1`` nếu số lượng tham chiếu của đối tượng được tăng thành công. Nếu không, hàm này trả về ``0``.

   :c:func:`PyUnstable_EnableTryIncRef` phải được gọi trước đó trên *obj*, nếu không hàm này có thể trả về ``0`` một cách không chính xác trong
   :term:`free-threaded build`.

   Về mặt logic, hàm này tương đương với đoạn mã C sau đây, ngoại trừ việc nó hoạt động nguyên tử trong :term:`free-threaded build`::

      if (Py_REFCNT(op) > 0) {
         Py_INCREF(op);
         return 1;
      }
      return 0;

   Hàm này được thiết kế như một khối xây dựng để quản lý weak reference mà không phải chịu chi phí của một :ref:`weak reference object <weakrefobjects>` Python.

   Thông thường, để sử dụng đúng hàm này, cần có sự hỗ trợ từ trình giải phóng của *obj* (:c:member:`~PyTypeObject.tp_dealloc`). Ví dụ, bản phác thảo sau đây có thể được điều chỉnh để triển khai một "weakmap" hoạt động như một :py:class:`~weakref.WeakValueDictionary` cho một kiểu cụ thể:

   .. code-block:: c

      PyMutex mutex;

      PyObject *
      add_entry(weakmap_key_type *key, PyObject *value)
      {
          PyUnstable_EnableTryIncRef(value);
          weakmap_type weakmap = ...;
          PyMutex_Lock(&mutex);
          weakmap_add_entry(weakmap, key, value);
          PyMutex_Unlock(&mutex);
          Py_RETURN_NONE;
      }

      PyObject *
      get_value(weakmap_key_type *key)
      {
          weakmap_type weakmap = ...;
          PyMutex_Lock(&mutex);
          PyObject *result = weakmap_find(weakmap, key);
          if (PyUnstable_TryIncRef(result)) {
              // `result` an toàn để sử dụng
              PyMutex_Unlock(&mutex);
              return result;
          }
          // nếu đến đây, `result` bắt đầu được thu gom rác,
          // nhưng vẫn chưa bị xóa khỏi weakmap
          PyMutex_Unlock(&mutex);
          return NULL;
      }

      // hàm tp_dealloc cho các giá trị của weakmap
      void
      value_dealloc(PyObject *value)
      {
          weakmap_type weakmap = ...;
          PyMutex_Lock(&mutex);
          weakmap_remove_value(weakmap, value);

          ...
          PyMutex_Unlock(&mutex);
      }

   .. versionadded:: 3.14

.. c:function:: void PyUnstable_EnableTryIncRef(PyObject *obj)

   Cho phép các lần sử dụng tiếp theo của :c:func:`PyUnstable_TryIncRef` trên *obj*. Bên gọi phải giữ một :term:`strong reference` để *obj* khi gọi hàm này.

   .. versionadded:: 3.14

.. c:function:: int PyUnstable_Object_IsUniquelyReferenced(PyObject *op)

   Xác định xem *op* chỉ có một tham chiếu hay không.

   Trên các bản build có GIL, hàm này tương đương với
   :c:expr:`Py_REFCNT(op) == 1`.

   Trên một :term:`free-threaded build`, hàm này kiểm tra *op*'s
   :term:`reference count` bằng một và đồng thời kiểm tra xem *op* chỉ được thread này sử dụng. :c:expr:`Py_REFCNT(op) == 1` là **not** thread-safe trên các bản build không có GIL; hãy ưu tiên dùng hàm này.

   Bên gọi phải giữ :term:`attached thread state`, mặc dù hàm này không gọi vào trình thông dịch Python. Hàm này không thể thất bại.

   .. versionadded:: 3.14

.. _`deferred reference counting`: https://peps.python.org/pep-0703/#deferred-reference-counting
