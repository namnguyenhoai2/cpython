.. highlight:: c

.. _weakrefobjects:

Đối tượng tham chiếu yếu
------------------------

Python hỗ trợ *các tham chiếu yếu* dưới dạng các đối tượng hạng nhất. Có hai kiểu đối tượng cụ thể trực tiếp triển khai tham chiếu yếu. Kiểu đầu tiên là một đối tượng tham chiếu đơn giản, còn kiểu thứ hai hoạt động như một proxy cho đối tượng gốc trong phạm vi tối đa có thể.


.. c:function:: int PyWeakref_Check(PyObject *ob)

   Trả về giá trị khác không nếu *ob* là một đối tượng tham chiếu hoặc proxy. Hàm này luôn thành công.


.. c:function:: int PyWeakref_CheckRef(PyObject *ob)

   Trả về giá trị khác không nếu *ob* là một đối tượng tham chiếu hoặc một lớp con của kiểu tham chiếu. Hàm này luôn thành công.


.. c:function:: int PyWeakref_CheckRefExact(PyObject *ob)

   Trả về giá trị khác không nếu *ob* là một đối tượng tham chiếu nhưng không phải là một lớp con của kiểu tham chiếu. Hàm này luôn thành công.


.. c:function:: int PyWeakref_CheckProxy(PyObject *ob)

   Trả về giá trị khác không nếu *ob* là một đối tượng proxy. Hàm này luôn thành công.


.. c:function:: PyObject* PyWeakref_NewRef(PyObject *ob, PyObject *callback)

   Trả về một đối tượng tham chiếu yếu cho đối tượng *ob*. Hàm này luôn trả về một tham chiếu mới, nhưng không đảm bảo tạo ra một đối tượng mới; một đối tượng tham chiếu hiện có có thể được trả về. Tham số thứ hai, *callback*, có thể là một đối tượng callable nhận thông báo khi *ob* được garbage collect; đối tượng đó phải chấp nhận một tham số duy nhất, là chính đối tượng tham chiếu yếu. *callback* cũng có thể là ``None`` hoặc ``NULL``. Nếu *ob* không phải là một đối tượng có thể tham chiếu yếu, hàm này sẽ raise :exc:`TypeError` và trả về ``NULL``.

   .. seealso::
      :c:func:`PyType_SUPPORTS_WEAKREFS` for checking if *ob* is weakly
      có thể được tham chiếu.


.. c:function:: PyObject* PyWeakref_NewProxy(PyObject *ob, PyObject *callback)

   Trả về một đối tượng proxy tham chiếu yếu cho đối tượng *ob*. Lệnh này luôn trả về một tham chiếu mới, nhưng không đảm bảo tạo một đối tượng mới; một đối tượng proxy hiện có có thể được trả về. Tham số thứ hai, *callback*, có thể là một đối tượng callable nhận thông báo khi *ob* được garbage collect; đối tượng này phải chấp nhận một tham số duy nhất, là chính đối tượng tham chiếu yếu. *callback* cũng có thể là ``None`` hoặc ``NULL``. Nếu *ob* không phải là đối tượng có thể được tham chiếu yếu, thao tác này sẽ raise :exc:`TypeError` và trả về ``NULL``.

   .. seealso::
      :c:func:`PyType_SUPPORTS_WEAKREFS` for checking if *ob* is weakly
      có thể được tham chiếu.


.. c:function:: int PyWeakref_GetRef(PyObject *ref, PyObject **pobj)

   Lấy một :term:`strong reference` tới đối tượng được tham chiếu từ một weak reference, *ref*, vào *\*pobj*.

   * Khi thành công, gán *\*pobj* bằng một :term:`strong reference` mới tới đối tượng được tham chiếu và trả về 1.
   * Nếu tham chiếu đã bị hủy, gán *\*pobj* bằng ``NULL`` và trả về 0.
   * Khi xảy ra lỗi, raise một exception và trả về -1.

   .. versionadded:: 3.13


.. c:function:: PyObject* PyWeakref_GetObject(PyObject *ref)

   Trả về một :term:`borrowed reference` tới đối tượng được tham chiếu từ một tham chiếu yếu, *ref*. Nếu đối tượng được tham chiếu không còn tồn tại, trả về ``Py_None``.

   .. note::

      Hàm này trả về một :term:`borrowed reference` tới đối tượng được tham chiếu. Điều này có nghĩa là bạn luôn phải gọi :c:func:`Py_INCREF` trên đối tượng, trừ khi đối tượng đó không thể bị hủy trước lần sử dụng cuối cùng của tham chiếu mượn.

   .. deprecated-removed:: 3.13 3.15
      Thay vào đó, hãy sử dụng :c:func:`PyWeakref_GetRef`.


.. c:function:: PyObject* PyWeakref_GET_OBJECT(PyObject *ref)

   Tương tự như :c:func:`PyWeakref_GetObject`, nhưng không thực hiện kiểm tra lỗi.

   .. deprecated-removed:: 3.13 3.15
      Thay vào đó, hãy sử dụng :c:func:`PyWeakref_GetRef`.


.. c:function:: int PyWeakref_IsDead(PyObject *ref)

   Kiểm tra xem tham chiếu yếu *ref* đã bị hủy hay chưa. Trả về 1 nếu tham chiếu đã bị hủy, 0 nếu tham chiếu vẫn còn hiệu lực và -1 kèm theo một lỗi được thiết lập nếu *ref* không phải là đối tượng tham chiếu yếu.

   .. versionadded:: 3.14


.. c:function:: void PyObject_ClearWeakRefs(PyObject *object)

   Hàm này được trình xử lý :c:member:`~PyTypeObject.tp_dealloc` gọi để xóa các tham chiếu yếu.

   Hàm này lặp qua các weak reference của *object* và gọi callback cho những reference có callback. Hàm trả về sau khi đã thử gọi tất cả callback.


.. c:function:: void PyUnstable_Object_ClearWeakRefsNoCallbacks(PyObject *object)

   Xóa các weakref của *object* mà không gọi callback.

   Hàm này được :c:member:`~PyTypeObject.tp_dealloc` handler gọi cho các kiểu có finalizer (tức là :meth:`~object.__del__`). Handler cho các đối tượng đó trước tiên gọi :c:func:`PyObject_ClearWeakRefs` để xóa weakref và gọi callback của chúng, sau đó gọi finalizer, và cuối cùng gọi hàm này để xóa mọi weakref có thể đã được finalizer tạo ra.

   Trong hầu hết trường hợp, sử dụng sẽ phù hợp hơn
   :c:func:`PyObject_ClearWeakRefs` để xóa weakref thay vì hàm này.

   .. versionadded:: 3.13
