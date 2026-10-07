.. highlight:: c

.. _iterator-objects:

Đối tượng iterator
------------------

Python cung cấp hai đối tượng iterator đa dụng. Đối tượng đầu tiên, iterator của sequence, hoạt động với một sequence bất kỳ hỗ trợ phương thức :meth:`~object.__getitem__`. Đối tượng thứ hai hoạt động với một đối tượng callable và một giá trị sentinel, gọi callable cho từng mục trong sequence và kết thúc quá trình lặp khi giá trị sentinel được trả về.


.. c:var:: PyTypeObject PySeqIter_Type

   Đối tượng kiểu dành cho các đối tượng iterator được :c:func:`PySeqIter_New` trả về và dạng một đối số của hàm tích hợp :func:`iter` đối với các kiểu sequence tích hợp.


.. c:function:: int PySeqIter_Check(PyObject *op)

   Trả về true nếu kiểu của *op* là :c:data:`PySeqIter_Type`. Hàm này luôn thành công.


.. c:function:: PyObject* PySeqIter_New(PyObject *seq)

   Trả về một iterator hoạt động với một đối tượng sequence tổng quát, *seq*. Quá trình lặp kết thúc khi sequence phát sinh :exc:`IndexError` cho thao tác truy cập chỉ mục.


.. c:var:: PyTypeObject PyCallIter_Type

   Đối tượng kiểu dành cho các đối tượng iterator được :c:func:`PyCallIter_New` trả về và dạng hai đối số của hàm tích hợp :func:`iter`.


.. c:function:: int PyCallIter_Check(PyObject *op)

   Trả về true nếu kiểu của *op* là :c:data:`PyCallIter_Type`. Hàm này luôn thành công.


.. c:function:: PyObject* PyCallIter_New(PyObject *callable, PyObject *sentinel)

   Trả về một iterator mới. Tham số đầu tiên, *callable*, có thể là bất kỳ đối tượng callable nào của Python có thể được gọi mà không cần tham số; mỗi lần gọi đối tượng này sẽ trả về mục tiếp theo trong quá trình lặp. Khi *callable* trả về một giá trị bằng *sentinel*, quá trình lặp sẽ kết thúc.


Đối tượng range
^^^^^^^^^^^^^^^

.. c:var:: PyTypeObject PyRange_Type

   Đối tượng kiểu cho các đối tượng :class:`range`.


.. c:function:: int PyRange_Check(PyObject *o)

   Trả về true nếu đối tượng *o* là một thể hiện của đối tượng :class:`range`. Hàm này luôn thực thi thành công.


Các kiểu iterator tích hợp sẵn
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Đây là các kiểu iteration tích hợp sẵn được đưa vào C API của Python nhưng không cung cấp thêm hàm nào. Chúng được liệt kê ở đây để đầy đủ.


.. list-table::
   :widths: auto
   :header-rows: 1

   * * Kiểu C
     * kiểu Python
   * * .. c:var:: PyTypeObject PyEnum_Type
     * :py:class:`enumerate`
   * * .. c:var:: PyTypeObject PyFilter_Type
     * :py:class:`filter`
   * * .. c:var:: PyTypeObject PyMap_Type
     * :py:class:`map`
   * * .. c:var:: PyTypeObject PyReversed_Type
     * :py:class:`reversed`
   * * .. c:var:: PyTypeObject PyZip_Type
     * :py:class:`zip`


Các đối tượng iterator khác
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. c:var:: PyTypeObject PyByteArrayIter_Type
.. c:var:: PyTypeObject PyBytesIter_Type
.. c:var:: PyTypeObject PyListIter_Type
.. c:var:: PyTypeObject PyListRevIter_Type
.. c:var:: PyTypeObject PySetIter_Type
.. c:var:: PyTypeObject PyTupleIter_Type
.. c:var:: PyTypeObject PyRangeIter_Type
.. c:var:: PyTypeObject PyLongRangeIter_Type
.. c:var:: PyTypeObject PyDictIterKey_Type
.. c:var:: PyTypeObject PyDictRevIterKey_Type
.. c:var:: PyTypeObject PyDictIterValue_Type
.. c:var:: PyTypeObject PyDictRevIterValue_Type
.. c:var:: PyTypeObject PyDictIterItem_Type
.. c:var:: PyTypeObject PyDictRevIterItem_Type
.. c:var:: PyTypeObject PyODictIter_Type

   Các đối tượng kiểu dành cho iterator của nhiều đối tượng dựng sẵn khác nhau.

   Không tạo trực tiếp các thực thể của những kiểu này; nên gọi
   :c:func:`PyObject_GetIter` thay vào đó.

   Lưu ý rằng không có gì đảm bảo một kiểu dựng sẵn nhất định sẽ sử dụng một kiểu iterator nhất định. Ví dụ: việc lặp qua :class:`range` sẽ sử dụng một trong hai kiểu iterator, tùy thuộc vào kích thước của range. Trong tương lai, các kiểu khác có thể bắt đầu sử dụng cơ chế tương tự mà không có cảnh báo.
