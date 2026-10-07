.. highlight:: c

.. _setobjects:

Đối tượng set
-------------

.. sectionauthor:: Raymond D. Hettinger <python@rcn.com>


.. index::
   pair: object; set
   pair: object; frozenset

Phần này trình bày chi tiết public API cho các đối tượng :class:`set` và :class:`frozenset`. Bất kỳ chức năng nào không được liệt kê dưới đây tốt nhất nên được truy cập bằng giao thức đối tượng trừu tượng (bao gồm :c:func:`PyObject_CallMethod`,
:c:func:`PyObject_RichCompareBool`, :c:func:`PyObject_Hash`,
:c:func:`PyObject_Repr`, :c:func:`PyObject_IsTrue`, :c:func:`PyObject_Print`, và
:c:func:`PyObject_GetIter`) hoặc giao thức số trừu tượng (bao gồm
:c:func:`PyNumber_And`, :c:func:`PyNumber_Subtract`, :c:func:`PyNumber_Or`,
:c:func:`PyNumber_Xor`, :c:func:`PyNumber_InPlaceAnd`,
:c:func:`PyNumber_InPlaceSubtract`, :c:func:`PyNumber_InPlaceOr`, và
:c:func:`PyNumber_InPlaceXor`).


.. c:type:: PySetObject

   Kiểu con này của :c:type:`PyObject` được dùng để lưu trữ dữ liệu nội bộ cho cả hai
   Kiểu con này của :class:`set` được dùng để lưu trữ dữ liệu nội bộ cho cả hai loại đối tượng :class:`set` và :class:`frozenset`. Nó giống :c:type:`PyDictObject` ở chỗ có kích thước cố định đối với các set nhỏ (tương tự cách lưu trữ tuple) và sẽ trỏ đến một khối bộ nhớ riêng có kích thước thay đổi đối với các set vừa và lớn (tương tự cách lưu trữ list). Không trường nào trong cấu trúc này nên được xem là public và tất cả đều có thể thay đổi. Mọi thao tác truy cập phải được thực hiện thông qua API đã được tài liệu hóa thay vì thao tác trực tiếp trên các giá trị trong cấu trúc.


.. c:var:: PyTypeObject PySet_Type

   Đây là một thể hiện của :c:type:`PyTypeObject` đại diện cho kiểu Python
   :class:`set`.


.. c:var:: PyTypeObject PyFrozenSet_Type

   Đây là một thể hiện của :c:type:`PyTypeObject` đại diện cho kiểu Python
   :class:`frozenset`.

Các macro kiểm tra kiểu sau đây hoạt động trên con trỏ tới bất kỳ đối tượng Python nào. Tương tự, các hàm khởi tạo hoạt động với bất kỳ đối tượng Python nào có thể lặp.


.. c:function:: int PySet_Check(PyObject *p)

   Trả về true nếu *p* là một đối tượng :class:`set` hoặc một thể hiện của kiểu con. Hàm này luôn thành công.

.. c:function:: int PyFrozenSet_Check(PyObject *p)

   Trả về true nếu *p* là một đối tượng :class:`frozenset` hoặc một thể hiện của kiểu con. Hàm này luôn thành công.

.. c:function:: int PyAnySet_Check(PyObject *p)

   Trả về true nếu *p* là đối tượng :class:`set`, đối tượng :class:`frozenset` hoặc một instance của kiểu con. Hàm này luôn thực thi thành công.

.. c:function:: int PySet_CheckExact(PyObject *p)

   Trả về true nếu *p* là đối tượng :class:`set` nhưng không phải là instance của kiểu con. Hàm này luôn thực thi thành công.

   .. versionadded:: 3.10

.. c:function:: int PyAnySet_CheckExact(PyObject *p)

   Trả về true nếu *p* là đối tượng :class:`set` hoặc đối tượng :class:`frozenset` nhưng không phải là instance của kiểu con. Hàm này luôn thực thi thành công.


.. c:function:: int PyFrozenSet_CheckExact(PyObject *p)

   Trả về true nếu *p* là đối tượng :class:`frozenset` nhưng không phải là instance của kiểu con. Hàm này luôn thực thi thành công.


.. c:function:: PyObject* PySet_New(PyObject *iterable)

   Trả về một :class:`set` mới chứa các đối tượng do *iterable* trả về. *iterable* có thể là ``NULL`` để tạo một set rỗng mới. Trả về set mới nếu thành công hoặc ``NULL`` nếu thất bại. Gây ra :exc:`TypeError` nếu *iterable* thực tế không phải là iterable. Hàm khởi tạo cũng hữu ích để sao chép một set (``c=set(s)``).

   .. note::

      Thao tác này là nguyên tử trong :term:`free threading <free-threaded build>` khi *iterable* là một :class:`set`, :class:`frozenset` hoặc :class:`dict`.


.. c:function:: PyObject* PyFrozenSet_New(PyObject *iterable)

   Trả về một :class:`frozenset` mới chứa các đối tượng do *iterable* trả về. *iterable* có thể là ``NULL`` để tạo một frozenset rỗng mới. Trả về set mới nếu thành công hoặc ``NULL`` nếu thất bại. Gây ra :exc:`TypeError` nếu *iterable* thực tế không phải là iterable.

   .. note::

      Thao tác này là nguyên tử trong :term:`free threading <free-threaded build>` khi *iterable* là một :class:`set`, :class:`frozenset` hoặc :class:`dict`.


Các hàm và macro sau đây khả dụng cho các đối tượng là :class:`set` hoặc :class:`frozenset`, hoặc các đối tượng thuộc subtype của chúng.


.. c:function:: Py_ssize_t PySet_Size(PyObject *anyset)

   .. index:: pair: built-in function; len

   Trả về độ dài của đối tượng :class:`set` hoặc :class:`frozenset`. Tương đương với ``len(anyset)``. Phát sinh :exc:`SystemError` nếu *anyset* không phải là
   :class:`set`, :class:`frozenset` hoặc một đối tượng thuộc subtype.


.. c:function:: Py_ssize_t PySet_GET_SIZE(PyObject *anyset)

   Dạng macro của :c:func:`PySet_Size` mà không kiểm tra lỗi.


.. c:function:: int PySet_Contains(PyObject *anyset, PyObject *key)

   Trả về ``1`` nếu tìm thấy, ``0`` nếu không tìm thấy và ``-1`` nếu gặp lỗi. Không giống phương thức :meth:`~object.__contains__` của Python, hàm này không tự động chuyển các set không thể băm thành các frozenset tạm thời. Phát sinh :exc:`TypeError` nếu *key* không thể băm. Phát sinh :exc:`SystemError` nếu *anyset* không phải là
   :class:`set`, :class:`frozenset` hoặc một đối tượng thuộc subtype.

   .. note::

      Phép toán là nguyên tử trên :term:`free threading <free-threaded build>` khi *key* là :class:`str`, :class:`int`, :class:`float`, :class:`bool` hoặc :class:`bytes`.

.. c:function:: int PySet_Add(PyObject *set, PyObject *key)

   Thêm *key* vào một instance :class:`set`. Cũng hoạt động với các instance :class:`frozenset` (giống như :c:func:`PyTuple_SetItem`, nó có thể được dùng để điền các giá trị của những frozenset hoàn toàn mới trước khi chúng được cung cấp cho mã khác). Trả về ``0`` khi thành công hoặc ``-1`` khi thất bại. Phát sinh :exc:`TypeError` nếu *key* không thể băm. Phát sinh :exc:`MemoryError` nếu không còn chỗ để mở rộng. Phát sinh một
   :exc:`SystemError` nếu *set* không phải là một instance của :class:`set` hoặc kiểu con của nó.

   .. note::

      Phép toán là nguyên tử trên :term:`free threading <free-threaded build>` khi *key* là :class:`str`, :class:`int`, :class:`float`, :class:`bool` hoặc :class:`bytes`.



Các hàm sau đây khả dụng cho các instance của :class:`set` hoặc các kiểu con của nó, nhưng không khả dụng cho các instance của :class:`frozenset` hoặc các kiểu con của nó.


.. c:function:: int PySet_Discard(PyObject *set, PyObject *key)

   Trả về ``1`` nếu tìm thấy và xóa được, ``0`` nếu không tìm thấy (không thực hiện thao tác nào), và ``-1`` nếu gặp lỗi. Không phát sinh :exc:`KeyError` đối với các key bị thiếu. Phát sinh một
   :exc:`TypeError` nếu *key* không thể băm. Không giống như phương thức :meth:`~set.discard` của Python, hàm này không tự động chuyển các set không thể băm thành frozenset tạm thời. Phát sinh :exc:`SystemError` nếu *set* không phải là một instance của :class:`set` hoặc kiểu con của nó.

   .. note::

      Phép toán là nguyên tử trên :term:`free threading <free-threaded build>` khi *key* là :class:`str`, :class:`int`, :class:`float`, :class:`bool` hoặc :class:`bytes`.


.. c:function:: PyObject* PySet_Pop(PyObject *set)

   Trả về một tham chiếu mới đến một đối tượng bất kỳ trong *set*, đồng thời xóa đối tượng đó khỏi *set*. Trả về ``NULL`` nếu thao tác thất bại. Phát sinh :exc:`KeyError` nếu set trống. Phát sinh một :exc:`SystemError` nếu *set* không phải là một thể hiện của
   :class:`set` hoặc kiểu con của nó.


.. c:function:: int PySet_Clear(PyObject *set)

   Xóa tất cả phần tử khỏi một set hiện có. Trả về ``0`` khi thành công. Trả về ``-1`` và phát sinh :exc:`SystemError` nếu *set* không phải là một thể hiện của
   :class:`set` hoặc kiểu con của nó.

   .. note::

      Trong :term:`free-threaded build`, set được làm rỗng trước khi các mục của nó bị xóa, vì vậy các thread khác sẽ quan sát thấy một set rỗng thay vì các trạng thái trung gian.


API đã lỗi thời
^^^^^^^^^^^^^^^

.. c:macro:: PySet_MINSIZE

   Một hằng số biểu thị kích thước của một bảng được cấp phát trước bên trong các instance của :c:type:`PySetObject`.

   Mục này chỉ được ghi lại để đầy đủ thông tin, vì không có gì đảm bảo rằng một phiên bản CPython cụ thể sử dụng các bảng được cấp phát trước với kích thước cố định. Trong mã không xử lý các phần nội bộ không ổn định của set,
   có thể thay thế :c:macro:`!PySet_MINSIZE` bằng một hằng số nhỏ như ``8``.

   Nếu muốn biết kích thước của một set, hãy sử dụng :c:func:`PySet_Size` thay thế.

   .. soft-deprecated:: 3.14
