.. highlight:: c

.. _sequence:

Giao thức Sequence
==================


.. c:function:: int PySequence_Check(PyObject *o)

   Trả về ``1`` nếu đối tượng cung cấp sequence protocol, và ``0`` nếu không. Lưu ý rằng hàm trả về ``1`` cho các lớp Python có phương thức :meth:`~object.__getitem__`, trừ khi chúng là các lớp con của :class:`dict`, vì nhìn chung không thể xác định lớp đó hỗ trợ loại khóa nào. Hàm này luôn thành công.


.. c:function:: Py_ssize_t PySequence_Size(PyObject *o)
               Py_ssize_t PySequence_Length(PyObject *o)

   .. index:: pair: built-in function; len

   Trả về số lượng đối tượng trong sequence *o* khi thành công, và ``-1`` khi thất bại. Tương đương với biểu thức Python ``len(o)``.


.. c:function:: PyObject* PySequence_Concat(PyObject *o1, PyObject *o2)

   Trả về phép nối của *o1* và *o2* khi thành công, và ``NULL`` khi thất bại. Tương đương với biểu thức Python ``o1 + o2``.


.. c:function:: PyObject* PySequence_Repeat(PyObject *o, Py_ssize_t count)

   Trả về kết quả của việc lặp lại đối tượng sequence *o* *count* lần, hoặc ``NULL`` khi thất bại. Tương đương với biểu thức Python ``o * count``.


.. c:function:: PyObject* PySequence_InPlaceConcat(PyObject *o1, PyObject *o2)

   Trả về phép nối của *o1* và *o2* khi thành công, và ``NULL`` khi thất bại. Thao tác được thực hiện *in-place* khi *o1* hỗ trợ thao tác này. Tương đương với biểu thức Python ``o1 += o2``.


.. c:function:: PyObject* PySequence_InPlaceRepeat(PyObject *o, Py_ssize_t count)

   Trả về kết quả của việc lặp đối tượng sequence *o* *count* lần, hoặc ``NULL`` nếu thất bại. Thao tác được thực hiện *tại chỗ* khi *o* hỗ trợ. Đây là tương đương với biểu thức Python ``o *= count``.


.. c:function:: PyObject* PySequence_GetItem(PyObject *o, Py_ssize_t i)

   Trả về phần tử thứ *i*\  của *o*, hoặc ``NULL`` nếu thất bại. Đây là tương đương với biểu thức Python ``o[i]``.


.. c:function:: PyObject* PySequence_GetSlice(PyObject *o, Py_ssize_t i1, Py_ssize_t i2)

   Trả về lát cắt của đối tượng sequence *o* nằm giữa *i1* và *i2*, hoặc ``NULL`` nếu thất bại. Đây là tương đương với biểu thức Python ``o[i1:i2]``.


.. c:function:: int PySequence_SetItem(PyObject *o, Py_ssize_t i, PyObject *v)

   Gán đối tượng *v* cho phần tử thứ *i*\  của *o*. Ném một ngoại lệ và trả về ``-1`` nếu thất bại; trả về ``0`` nếu thành công. Đây là tương đương với câu lệnh Python ``o[i] = v``. Hàm này *không* ":term:`steal`" một tham chiếu đến *v*.

   Nếu *v* là ``NULL``, phần tử sẽ bị xóa, nhưng tính năng này đã lỗi thời và nên dùng :c:func:`PySequence_DelItem` thay thế.


.. c:function:: int PySequence_DelItem(PyObject *o, Py_ssize_t i)

   Xóa phần tử thứ *i*\  của đối tượng *o*. Trả về ``-1`` nếu thất bại. Đây là tương đương với câu lệnh Python ``del o[i]``.


.. c:function:: int PySequence_SetSlice(PyObject *o, Py_ssize_t i1, Py_ssize_t i2, PyObject *v)

   Gán đối tượng sequence *v* cho lát cắt trong đối tượng sequence *o* từ *i1* đến *i2*. Đây là tương đương với câu lệnh Python ``o[i1:i2] = v``.


.. c:function:: int PySequence_DelSlice(PyObject *o, Py_ssize_t i1, Py_ssize_t i2)

   Xóa slice trong đối tượng sequence *o* từ *i1* đến *i2*. Trả về ``-1`` khi thất bại. Đây là tương đương với câu lệnh Python ``del o[i1:i2]``.


.. c:function:: Py_ssize_t PySequence_Count(PyObject *o, PyObject *value)

   Trả về số lần xuất hiện của *value* trong *o*, tức là trả về số khóa mà ``o[key] == value``. Khi thất bại, trả về ``-1``. Điều này tương đương với biểu thức Python ``o.count(value)``.


.. c:function:: int PySequence_Contains(PyObject *o, PyObject *value)

   Xác định xem *o* có chứa *value* hay không. Nếu một mục trong *o* bằng *value*, trả về ``1``, nếu không thì trả về ``0``. Khi xảy ra lỗi, trả về ``-1``. Điều này tương đương với biểu thức Python ``value in o``.


.. c:function:: int PySequence_In(PyObject *o, PyObject *value)

   Bí danh của :c:func:`PySequence_Contains`.

   .. soft-deprecated:: 3.14
      Không nên sử dụng hàm này để viết mã mới.


.. c:function:: Py_ssize_t PySequence_Index(PyObject *o, PyObject *value)

   Trả về chỉ mục đầu tiên *i* mà ``o[i] == value``. Khi xảy ra lỗi, trả về ``-1``. Điều này tương đương với biểu thức Python ``o.index(value)``.


.. c:function:: PyObject* PySequence_List(PyObject *o)

   Trả về một đối tượng list có cùng nội dung với sequence hoặc iterable *o*, hoặc ``NULL`` khi thất bại. List được trả về luôn là một list mới. Điều này tương đương với biểu thức Python ``list(o)``.


.. c:function:: PyObject* PySequence_Tuple(PyObject *o)

   .. index:: pair: built-in function; tuple

   Trả về một đối tượng tuple có cùng nội dung với sequence hoặc iterable *o*, hoặc ``NULL`` khi thất bại. Nếu *o* là một tuple, một tham chiếu mới sẽ được trả về; nếu không, một tuple sẽ được tạo với nội dung phù hợp. Điều này tương đương với biểu thức Python ``tuple(o)``.


.. c:function:: PyObject* PySequence_Fast(PyObject *o, const char *m)

   Trả về sequence hoặc iterable *o* dưới dạng một đối tượng có thể được sử dụng bởi các hàm khác thuộc họ ``PySequence_Fast*``. Nếu đối tượng này không phải là sequence hoặc iterable, sẽ phát sinh :exc:`TypeError` với *m* làm nội dung thông báo. Trả về ``NULL`` khi thất bại.

   Các hàm ``PySequence_Fast*`` được đặt tên như vậy vì chúng giả định *o* là một :c:type:`PyTupleObject` hoặc một :c:type:`PyListObject`, đồng thời truy cập trực tiếp các trường dữ liệu của *o*.

   Xét trên phương diện chi tiết triển khai của CPython, nếu *o* đã là một sequence hoặc list thì nó sẽ được trả về.


.. c:function:: Py_ssize_t PySequence_Fast_GET_SIZE(PyObject *o)

   Trả về độ dài của *o*, với giả định rằng *o* đã được trả về bởi
   :c:func:`PySequence_Fast` và *o* không phải là ``NULL``. Kích thước cũng có thể được lấy bằng cách gọi :c:func:`PySequence_Size` trên *o*, nhưng
   :c:func:`PySequence_Fast_GET_SIZE` nhanh hơn vì nó có thể giả định *o* là một list hoặc tuple.


.. c:function:: PyObject* PySequence_Fast_GET_ITEM(PyObject *o, Py_ssize_t i)

   Trả về phần tử thứ *i*\ th của *o*, với điều kiện *o* được trả về bởi
   :c:func:`PySequence_Fast`, *o* không phải là ``NULL``, và *i* nằm trong phạm vi hợp lệ.


.. c:function:: PyObject** PySequence_Fast_ITEMS(PyObject *o)

   Trả về mảng bên dưới chứa các con trỏ PyObject. Giả định rằng *o* được trả về bởi :c:func:`PySequence_Fast` và *o* không phải là ``NULL``.

   Lưu ý rằng nếu một list được thay đổi kích thước, thao tác cấp phát lại có thể di chuyển mảng items. Vì vậy, chỉ sử dụng con trỏ tới mảng bên dưới trong những ngữ cảnh mà sequence không thể thay đổi.


.. c:function:: PyObject* PySequence_ITEM(PyObject *o, Py_ssize_t i)

   Trả về phần tử thứ *i*\ th của *o* hoặc ``NULL`` nếu xảy ra lỗi. Dạng nhanh hơn của
   :c:func:`PySequence_GetItem` nhưng không kiểm tra rằng
   :c:func:`PySequence_Check` trên *o* là true và không điều chỉnh cho các chỉ mục âm.
