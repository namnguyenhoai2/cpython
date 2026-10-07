.. highlight:: c

.. _listobjects:

Đối tượng List
--------------

.. index:: pair: object; list


.. c:type:: PyListObject

   Subtype này của :c:type:`PyObject` biểu diễn một đối tượng list trong Python.


.. c:var:: PyTypeObject PyList_Type

   Instance này của :c:type:`PyTypeObject` biểu diễn kiểu list của Python. Đây là cùng một đối tượng với :class:`list` trong lớp Python.


.. c:function:: int PyList_Check(PyObject *p)

   Trả về true nếu *p* là một đối tượng list hoặc một instance của subtype thuộc kiểu list. Hàm này luôn thực thi thành công.


.. c:function:: int PyList_CheckExact(PyObject *p)

   Trả về true nếu *p* là một đối tượng list nhưng không phải là instance của subtype thuộc kiểu list. Hàm này luôn thực thi thành công.


.. c:function:: PyObject* PyList_New(Py_ssize_t len)

   Trả về một list mới có độ dài *len* nếu thành công hoặc ``NULL`` nếu thất bại.

   .. note::

      Nếu *len* lớn hơn zero, các item của đối tượng list được trả về sẽ được đặt thành ``NULL``. Do đó, bạn không thể sử dụng các hàm abstract API như
      :c:func:`PySequence_SetItem` hoặc cung cấp đối tượng cho mã Python trước khi đặt tất cả các mục thành một đối tượng thực bằng :c:func:`PyList_SetItem` hoặc
      :c:func:`PyList_SET_ITEM()`. Các API sau đây an toàn để sử dụng trước khi danh sách được khởi tạo hoàn chỉnh: :c:func:`PyList_SetItem()` và :c:func:`PyList_SET_ITEM()`.



.. c:function:: Py_ssize_t PyList_Size(PyObject *list)

   .. index:: pair: built-in function; len

   Trả về độ dài của đối tượng danh sách trong *list*; tương đương với ``len(list)`` trên một đối tượng danh sách.


.. c:function:: Py_ssize_t PyList_GET_SIZE(PyObject *list)

   Tương tự như :c:func:`PyList_Size`, nhưng không kiểm tra lỗi.


.. c:function:: PyObject* PyList_GetItemRef(PyObject *list, Py_ssize_t index)

   Trả về đối tượng tại vị trí *index* trong danh sách được *list* trỏ tới. Vị trí phải là số không âm; không hỗ trợ lập chỉ mục từ cuối danh sách. Nếu *index* nằm ngoài phạm vi (:code:`<0 or >=len(list)`), trả về ``NULL`` và đặt một ngoại lệ :exc:`IndexError`.

   .. versionadded:: 3.13


.. c:function:: PyObject* PyList_GetItem(PyObject *list, Py_ssize_t index)

   Giống như :c:func:`PyList_GetItemRef`, nhưng trả về một
   :term:`borrowed reference` thay vì một :term:`strong reference`.

   .. note::

      Trong :term:`free-threaded build`, giá trị được trả về
      :term:`borrowed reference` có thể trở nên không hợp lệ nếu một thread khác đồng thời sửa đổi danh sách. Nên dùng :c:func:`PyList_GetItemRef`, hàm này trả về một :term:`strong reference`.


.. c:function:: PyObject* PyList_GET_ITEM(PyObject *list, Py_ssize_t i)

   Tương tự :c:func:`PyList_GetItem`, nhưng không kiểm tra lỗi.

   .. note::

      Trong :term:`free-threaded build`, giá trị được trả về
      :term:`borrowed reference` có thể trở nên không hợp lệ nếu một thread khác đồng thời sửa đổi danh sách. Nên dùng :c:func:`PyList_GetItemRef`, hàm này trả về một :term:`strong reference`.


.. c:function:: int PyList_SetItem(PyObject *list, Py_ssize_t index, PyObject *item)

   Đặt phần tử tại chỉ mục *index* trong danh sách thành *item*. Trả về ``0`` nếu thành công. Nếu *index* nằm ngoài phạm vi, trả về ``-1`` và thiết lập một ngoại lệ :exc:`IndexError`.

   .. note::

      Hàm này ":term:`steals <steal>`" một tham chiếu đến *item*, ngay cả khi xảy ra lỗi. Khi thành công, hàm loại bỏ một tham chiếu đến phần tử đã có trong danh sách tại vị trí bị ảnh hưởng (trừ khi phần tử đó là ``NULL``).


.. c:function:: void PyList_SET_ITEM(PyObject *list, Py_ssize_t i, PyObject *o)

   Dạng macro của :c:func:`PyList_SetItem` mà không kiểm tra lỗi. Thông thường, macro này chỉ được dùng để điền vào các list mới khi chưa có nội dung trước đó.

   Việc kiểm tra giới hạn được thực hiện dưới dạng assertion nếu Python được build ở chế độ
   :ref:`chế độ debug <debug-build>` hoặc :option:`with assertions <--with-assertions>`.

   .. note::

      Macro này ":term:`chiếm quyền sở hữu <steal>`" một tham chiếu đến *item*, và, không giống như
      :c:func:`PyList_SetItem`, không *loại bỏ* tham chiếu đến bất kỳ item nào đang được thay thế; mọi tham chiếu trong *list* tại vị trí *i* sẽ bị rò rỉ.

   .. note::

      Trong :term:`free-threaded build`, macro này không có cơ chế đồng bộ nội bộ. Thông thường, macro này chỉ được dùng để điền vào các list mới khi không có thread nào khác tham chiếu đến list. Nếu list có thể được chia sẻ, hãy dùng :c:func:`PyList_SetItem` thay thế, vì macro này sử dụng một :term:`per-object lock`.


.. c:function:: int PyList_Insert(PyObject *list, Py_ssize_t index, PyObject *item)

   Chèn item *item* vào list *list* ngay trước index *index*. Trả về ``0`` nếu thành công; trả về ``-1`` và thiết lập một exception nếu không thành công. Tương tự như ``list.insert(index, item)``.


.. c:function:: int PyList_Append(PyObject *list, PyObject *item)

   Thêm đối tượng *item* vào cuối list *list*. Trả về ``0`` nếu thành công; trả về ``-1`` và đặt một exception nếu không thành công. Tương tự như ``list.append(item)``.


.. c:function:: PyObject* PyList_GetSlice(PyObject *list, Py_ssize_t low, Py_ssize_t high)

   Trả về một list các đối tượng trong *list* chứa các đối tượng *between* *low* và *high*. Trả về ``NULL`` và đặt một exception nếu không thành công. Tương tự như ``list[low:high]``. Việc lập chỉ mục từ cuối list không được hỗ trợ.


.. c:function:: int PyList_SetSlice(PyObject *list, Py_ssize_t low, Py_ssize_t high, PyObject *itemlist)

   Đặt slice của *list* giữa *low* và *high* thành nội dung của *itemlist*. Tương tự như ``list[low:high] = itemlist``. *itemlist* có thể là ``NULL``, biểu thị việc gán một list rỗng (xóa slice). Trả về ``0`` khi thành công, ``-1`` khi thất bại. Việc lập chỉ mục từ cuối list không được hỗ trợ.

   .. note::

      Trong :term:`free-threaded build`, khi *itemlist* là một :class:`list`, cả *list* và *itemlist* đều bị khóa trong suốt thời gian thực hiện thao tác. Đối với các iterable khác (hoặc ``NULL``), chỉ *list* bị khóa.


.. c:function:: int PyList_Extend(PyObject *list, PyObject *iterable)

   Mở rộng *list* bằng nội dung của *iterable*. Điều này giống như ``PyList_SetSlice(list, PY_SSIZE_T_MAX, PY_SSIZE_T_MAX, iterable)`` và tương tự như ``list.extend(iterable)`` hoặc ``list += iterable``.

   Phát sinh một exception và trả về ``-1`` nếu *list* không phải là một đối tượng :class:`list`. Trả về 0 khi thành công.

   .. versionadded:: 3.13

   .. note::

      Trong :term:`free-threaded build`, khi *iterable* là một :class:`list`,
      :class:`set`, :class:`dict` hoặc dict view, cả *list* và *iterable* (hoặc dict nền tảng của nó) đều bị khóa trong suốt thời gian thực hiện thao tác. Đối với các iterable khác, chỉ *list* bị khóa; *iterable* có thể bị một thread khác sửa đổi đồng thời.


.. c:function:: int PyList_Clear(PyObject *list)

   Xóa tất cả các mục khỏi *list*. Điều này tương đương với ``PyList_SetSlice(list, 0, PY_SSIZE_T_MAX, NULL)`` và tương tự như ``list.clear()`` hoặc ``del list[:]``.

   Phát sinh một exception và trả về ``-1`` nếu *list* không phải là đối tượng :class:`list`. Trả về 0 nếu thành công.

   .. versionadded:: 3.13


.. c:function:: int PyList_Sort(PyObject *list)

   Sắp xếp các mục của *list* ngay tại chỗ. Trả về ``0`` nếu thành công, ``-1`` nếu thất bại. Điều này tương đương với ``list.sort()``.

   .. note::

      Trong :term:`free-threaded build`, việc so sánh phần tử thông qua
      :meth:`~object.__lt__` có thể thực thi mã Python tùy ý, trong thời gian đó :term:`per-object lock` có thể được tạm thời giải phóng. Đối với các kiểu dựng sẵn (:class:`str`, :class:`int`, :class:`float`), khóa không được giải phóng trong quá trình so sánh.


.. c:function:: int PyList_Reverse(PyObject *list)

   Đảo ngược các mục của *list* ngay tại chỗ. Trả về ``0`` nếu thành công, ``-1`` nếu thất bại. Điều này tương đương với ``list.reverse()``.


.. c:function:: PyObject* PyList_AsTuple(PyObject *list)

   .. index:: pair: built-in function; tuple

   Trả về một đối tượng tuple mới chứa nội dung của *list*; tương đương với ``tuple(list)``.
