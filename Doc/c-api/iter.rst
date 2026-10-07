.. highlight:: c

.. _iterator:

Giao thức Iterator
==================

Có hai hàm dành riêng để làm việc với iterator.

.. c:function:: int PyIter_Check(PyObject *o)

   Trả về giá trị khác 0 nếu đối tượng *o* có thể được truyền an toàn cho
   :c:func:`PyIter_NextItem` và ``0`` trong các trường hợp còn lại. Hàm này luôn thành công.

.. c:function:: int PyAIter_Check(PyObject *o)

   Trả về giá trị khác 0 nếu đối tượng *o* cung cấp giao thức :class:`AsyncIterator`, và ``0`` trong các trường hợp còn lại. Hàm này luôn thành công.

   .. versionadded:: 3.10

.. c:function:: int PyIter_NextItem(PyObject *iter, PyObject **item)

   Trả về ``1`` và đặt *item* thành :term:`strong reference` của giá trị tiếp theo của iterator *iter* khi thành công. Trả về ``0`` và đặt *item* thành ``NULL`` nếu không còn giá trị nào. Trả về ``-1``, đặt *item* thành ``NULL`` và đặt một exception khi xảy ra lỗi.

   .. versionadded:: 3.14

.. c:function:: PyObject* PyIter_Next(PyObject *o)

   Đây là phiên bản cũ hơn của :c:func:`!PyIter_NextItem`, được giữ lại để tương thích ngược. Ưu tiên sử dụng :c:func:`PyIter_NextItem`.

   Trả về giá trị tiếp theo từ iterator *o*. Đối tượng phải là một iterator theo :c:func:`PyIter_Check` (người gọi phải tự kiểm tra điều này). Nếu không còn giá trị nào, trả về ``NULL`` mà không đặt ngoại lệ. Nếu xảy ra lỗi khi truy xuất mục này, trả về ``NULL`` và truyền tiếp ngoại lệ.

.. c:type:: PySendResult

   Giá trị enum được dùng để biểu diễn các kết quả khác nhau của :c:func:`PyIter_Send`.

   .. versionadded:: 3.10


.. c:function:: PySendResult PyIter_Send(PyObject *iter, PyObject *arg, PyObject **presult)

   Gửi giá trị *arg* vào iterator *iter*. Trả về:

   - ``PYGEN_RETURN`` nếu iterator trả về. Giá trị trả về được trả qua *presult*.
   - ``PYGEN_NEXT`` nếu iterator yield. Giá trị được yield được trả qua *presult*.
   - ``PYGEN_ERROR`` nếu iterator đã phát sinh ngoại lệ. *presult* được đặt thành ``NULL``.

   .. versionadded:: 3.10
