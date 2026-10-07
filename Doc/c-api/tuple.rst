.. highlight:: c

.. _tupleobjects:

Đối tượng Tuple
---------------

.. index:: pair: object; tuple


.. c:type:: PyTupleObject

   Kiểu con này của :c:type:`PyObject` đại diện cho một đối tượng tuple trong Python.


.. c:var:: PyTypeObject PyTuple_Type

   Instance này của :c:type:`PyTypeObject` đại diện cho kiểu tuple trong Python; trong lớp Python, nó chính là đối tượng :class:`tuple`.


.. c:function:: int PyTuple_Check(PyObject *p)

   Trả về true nếu *p* là một đối tượng tuple hoặc là một instance của kiểu con của kiểu tuple. Hàm này luôn thành công.


.. c:function:: int PyTuple_CheckExact(PyObject *p)

   Trả về true nếu *p* là một đối tượng tuple nhưng không phải là một instance của kiểu con của kiểu tuple. Hàm này luôn thành công.


.. c:function:: PyObject* PyTuple_New(Py_ssize_t len)

   Trả về một đối tượng tuple mới có kích thước *len*, hoặc ``NULL`` nếu xảy ra lỗi.


.. c:function:: PyObject* PyTuple_Pack(Py_ssize_t n, ...)

   Trả về một đối tượng tuple mới có kích thước *n*, hoặc ``NULL`` nếu xảy ra lỗi. Các giá trị trong tuple được khởi tạo bằng các đối số C *n* tiếp theo trỏ đến các đối tượng Python. ``PyTuple_Pack(2, a, b)`` tương đương với ``Py_BuildValue("(OO)", a, b)``.


.. c:function:: Py_ssize_t PyTuple_Size(PyObject *p)

   Nhận một con trỏ tới đối tượng tuple và trả về kích thước của tuple đó. Khi xảy ra lỗi, trả về ``-1`` cùng với một exception được thiết lập.


.. c:function:: Py_ssize_t PyTuple_GET_SIZE(PyObject *p)

   Tương tự :c:func:`PyTuple_Size`, nhưng không kiểm tra lỗi.


.. c:function:: PyObject* PyTuple_GetItem(PyObject *p, Py_ssize_t pos)

   Trả về đối tượng ở vị trí *pos* trong tuple được *p* trỏ tới. Nếu *pos* là số âm hoặc nằm ngoài giới hạn, trả về ``NULL`` và thiết lập một exception :exc:`IndexError`.

   Tham chiếu được trả về là tham chiếu mượn từ tuple *p* (nghĩa là: tham chiếu chỉ hợp lệ khi bạn vẫn còn giữ một tham chiếu tới *p*). Để lấy một :term:`strong reference`, hãy sử dụng
   :c:func:`Py_NewRef(PyTuple_GetItem(...)) <Py_NewRef>` hoặc :c:func:`PySequence_GetItem`.


.. c:function:: PyObject* PyTuple_GET_ITEM(PyObject *p, Py_ssize_t pos)

   Tương tự :c:func:`PyTuple_GetItem`, nhưng không kiểm tra các đối số của nó.


.. c:function:: PyObject* PyTuple_GetSlice(PyObject *p, Py_ssize_t low, Py_ssize_t high)

   Trả về phần lát cắt của tuple được *p* trỏ tới, nằm giữa *low* và *high*, hoặc ``NULL`` cùng với một exception được thiết lập nếu xảy ra lỗi.

   Điều này tương đương với biểu thức Python ``p[low:high]``. Không hỗ trợ lập chỉ mục từ cuối tuple.


.. c:function:: int PyTuple_SetItem(PyObject *p, Py_ssize_t pos, PyObject *o)

   Chèn một tham chiếu đến đối tượng *o* vào vị trí *pos* của tuple được *p* trỏ tới. Trả về ``0`` nếu thành công. Nếu *pos* nằm ngoài giới hạn, trả về ``-1`` và đặt một exception :exc:`IndexError`.

   .. note::

      Hàm này ":term:`steals <steal>`" một tham chiếu đến *o* và loại bỏ tham chiếu đến một mục đã có trong tuple tại vị trí bị ảnh hưởng (trừ khi tham chiếu đó là NULL).


.. c:function:: void PyTuple_SET_ITEM(PyObject *p, Py_ssize_t pos, PyObject *o)

   Tương tự :c:func:`PyTuple_SetItem`, nhưng không kiểm tra lỗi và *only* nên được dùng để điền vào các tuple hoàn toàn mới.

   Việc kiểm tra giới hạn được thực hiện dưới dạng một assertion nếu Python được xây dựng ở
   :ref:`debug mode <debug-build>` hoặc :option:`with assertions <--with-assertions>`.

   .. note::

      Hàm này ":term:`steals <steal>`" một tham chiếu đến *o*, và, không giống như
      :c:func:`PyTuple_SetItem`, không *not* loại bỏ tham chiếu đến bất kỳ mục nào đang được thay thế; bất kỳ tham chiếu nào trong tuple ở vị trí *pos* sẽ bị rò rỉ.

   .. warning::

      Macro này *only* chỉ nên được sử dụng trên các tuple mới được tạo. Việc sử dụng macro này trên một tuple đang được sử dụng (hay nói cách khác, có refcount > 1) có thể dẫn đến hành vi không xác định.


.. c:function:: int _PyTuple_Resize(PyObject **p, Py_ssize_t newsize)

   Có thể sử dụng để thay đổi kích thước một tuple. *newsize* sẽ là độ dài mới của tuple. Vì tuple được *supposed* cho là bất biến, bạn chỉ nên sử dụng hàm này nếu đối tượng chỉ có một tham chiếu. *not* Không sử dụng hàm này nếu tuple có thể đã được một phần khác của mã biết đến. Tuple sẽ luôn được mở rộng hoặc thu nhỏ ở cuối. Hãy xem đây là việc hủy tuple cũ và tạo một tuple mới, chỉ là hiệu quả hơn. Trả về ``0`` khi thành công. Mã phía client không bao giờ nên giả định rằng giá trị kết quả của ``*p`` sẽ giống như trước khi gọi hàm này. Nếu đối tượng được tham chiếu bởi ``*p`` được thay thế, ``*p`` ban đầu sẽ bị hủy. Khi thất bại, trả về ``-1`` và đặt ``*p`` thành ``NULL``, đồng thời phát sinh :exc:`MemoryError` hoặc :exc:`SystemError`.


.. _struct-sequence-objects:

Đối tượng Struct Sequence
-------------------------

Các đối tượng struct sequence là phiên bản tương đương trong C của các đối tượng :func:`~collections.namedtuple`, tức là một sequence mà các phần tử cũng có thể được truy cập thông qua các thuộc tính. Để tạo một struct sequence, trước tiên bạn phải tạo một kiểu struct sequence cụ thể.

.. c:function:: PyTypeObject* PyStructSequence_NewType(PyStructSequence_Desc *desc)

   Tạo một kiểu struct sequence mới từ dữ liệu trong *desc*, được mô tả bên dưới. Có thể tạo các instance của kiểu kết quả bằng :c:func:`PyStructSequence_New`.

   Trả về ``NULL`` và thiết lập một exception khi thất bại.


.. c:function:: void PyStructSequence_InitType(PyTypeObject *type, PyStructSequence_Desc *desc)

   Khởi tạo một kiểu struct sequence *type* từ *desc* tại chỗ.


.. c:function:: int PyStructSequence_InitType2(PyTypeObject *type, PyStructSequence_Desc *desc)

   Tương tự như :c:func:`PyStructSequence_InitType`, nhưng trả về ``0`` khi thành công và ``-1`` kèm theo một exception được thiết lập khi thất bại.

   .. versionadded:: 3.4


.. c:type:: PyStructSequence_Desc

   Chứa thông tin meta của kiểu struct sequence cần tạo.

   .. c:member:: const char *name

      Tên đầy đủ của kiểu; được mã hóa UTF-8 và kết thúc bằng null. Tên phải chứa tên module.

   .. c:member:: const char *doc

      Con trỏ tới docstring của kiểu hoặc ``NULL`` để bỏ qua.

   .. c:member:: PyStructSequence_Field *fields

      Con trỏ tới mảng kết thúc bằng ``NULL`` chứa tên các trường của kiểu mới.

   .. c:member:: int n_in_sequence

      Số trường hiển thị ở phía Python (nếu được sử dụng như tuple).


.. c:type:: PyStructSequence_Field

   Mô tả một trường của struct sequence. Vì struct sequence được mô hình hóa dưới dạng tuple nên tất cả các trường đều được định kiểu là :c:expr:`PyObject*`. Chỉ mục trong
   mảng :c:member:`~PyStructSequence_Desc.fields` của :c:type:`PyStructSequence_Desc` xác định trường nào của struct sequence được mô tả.

   .. c:member:: const char *name

      Tên của trường hoặc ``NULL`` để kết thúc danh sách các trường có tên; đặt thành :c:data:`PyStructSequence_UnnamedField` để để trống tên.

   .. c:member:: const char *doc

      Docstring của trường hoặc ``NULL`` để bỏ qua.


.. c:var:: const char * const PyStructSequence_UnnamedField

   Giá trị đặc biệt cho tên trường để để trống tên trường đó.

   .. versionchanged:: 3.9
      Kiểu này đã được thay đổi từ ``char *``.


.. c:function:: PyObject* PyStructSequence_New(PyTypeObject *type)

   Tạo một thực thể của *type*, đối tượng này phải được tạo bằng
   :c:func:`PyStructSequence_NewType`.

   Trả về ``NULL`` và thiết lập một exception khi thất bại.


.. c:function:: PyObject* PyStructSequence_GetItem(PyObject *p, Py_ssize_t pos)

   Trả về đối tượng tại vị trí *pos* trong chuỗi struct được *p* trỏ tới.

   Việc kiểm tra giới hạn được thực hiện dưới dạng một assertion nếu Python được build ở chế độ
   :ref:`debug mode <debug-build>` hoặc :option:`with assertions <--with-assertions>`.


.. c:function:: PyObject* PyStructSequence_GET_ITEM(PyObject *p, Py_ssize_t pos)

   Bí danh của :c:func:`PyStructSequence_GetItem`.

   .. versionchanged:: 3.13
      Hiện được triển khai dưới dạng bí danh của :c:func:`PyStructSequence_GetItem`.


.. c:function:: void PyStructSequence_SetItem(PyObject *p, Py_ssize_t pos, PyObject *o)

   Đặt trường tại chỉ mục *pos* của chuỗi struct *p* thành giá trị *o*.  Giống như
   :c:func:`PyTuple_SET_ITEM`, chỉ nên được dùng để điền vào các instance mới hoàn toàn.

   Việc kiểm tra giới hạn được thực hiện dưới dạng một assertion nếu Python được build ở chế độ
   :ref:`debug mode <debug-build>` hoặc :option:`with assertions <--with-assertions>`.

   .. note::

      Hàm ":term:`chiếm quyền sở hữu <steal>`" một tham chiếu đến *o*.


.. c:function:: void PyStructSequence_SET_ITEM(PyObject *p, Py_ssize_t *pos, PyObject *o)

   Bí danh của :c:func:`PyStructSequence_SetItem`.

   .. versionchanged:: 3.13
      Hiện được triển khai dưới dạng bí danh của :c:func:`PyStructSequence_SetItem`.
