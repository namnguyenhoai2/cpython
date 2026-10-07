.. highlight:: c

.. _mapping:

Giao thức ánh xạ
================

Xem thêm :c:func:`PyObject_GetItem`, :c:func:`PyObject_SetItem` và
:c:func:`PyObject_DelItem`.


.. c:function:: int PyMapping_Check(PyObject *o)

   Trả về ``1`` nếu đối tượng cung cấp mapping protocol hoặc hỗ trợ slicing, và ``0`` trong các trường hợp khác. Lưu ý rằng hàm trả về ``1`` đối với các lớp Python có phương thức :meth:`~object.__getitem__`, vì nhìn chung không thể xác định lớp đó hỗ trợ kiểu khóa nào. Hàm này luôn thành công.


.. c:function:: Py_ssize_t PyMapping_Size(PyObject *o)
               Py_ssize_t PyMapping_Length(PyObject *o)

   .. index:: pair: built-in function; len

   Trả về số lượng khóa trong đối tượng *o* khi thành công và ``-1`` khi thất bại. Điều này tương đương với biểu thức Python ``len(o)``.


.. c:function:: PyObject* PyMapping_GetItemString(PyObject *o, const char *key)

   Biến thể này giống :c:func:`PyObject_GetItem`, nhưng *key* được chỉ định dưới dạng chuỗi byte được mã hóa UTF-8 :c:expr:`const char*`, thay vì một :c:expr:`PyObject*`.


.. c:function:: int PyMapping_GetOptionalItem(PyObject *obj, PyObject *key, PyObject **result)

   Biến thể của :c:func:`PyObject_GetItem` không phát sinh ngoại lệ
   :exc:`KeyError` nếu không tìm thấy key.

   Nếu tìm thấy key, trả về ``1`` và đặt *\*result* thành một giá trị mới
   :term:`strong reference` thành giá trị tương ứng. Nếu không tìm thấy key, trả về ``0`` và đặt *\*result* thành ``NULL``; :exc:`KeyError` bị bỏ qua. Nếu xảy ra lỗi khác với :exc:`KeyError`, trả về ``-1`` và đặt *\*result* thành ``NULL``.

   .. versionadded:: 3.13


.. c:function:: int PyMapping_GetOptionalItemString(PyObject *obj, const char *key, PyObject **result)

   Điều này giống với :c:func:`PyMapping_GetOptionalItem`, nhưng *key* được chỉ định dưới dạng một :c:expr:`const char*` chuỗi byte được mã hóa UTF-8, thay vì một :c:expr:`PyObject*`.

   .. versionadded:: 3.13


.. c:function:: int PyMapping_SetItemString(PyObject *o, const char *key, PyObject *v)

   Điều này giống với :c:func:`PyObject_SetItem`, nhưng *key* được chỉ định dưới dạng một :c:expr:`const char*` chuỗi byte được mã hóa UTF-8, thay vì một :c:expr:`PyObject*`.


.. c:function:: int PyMapping_DelItem(PyObject *o, PyObject *key)

   Đây là bí danh của :c:func:`PyObject_DelItem`.


.. c:function:: int PyMapping_DelItemString(PyObject *o, const char *key)

   Điều này giống với :c:func:`PyObject_DelItem`, nhưng *key* được chỉ định dưới dạng một :c:expr:`const char*` chuỗi byte được mã hóa UTF-8, thay vì một :c:expr:`PyObject*`.


.. c:function:: int PyMapping_HasKeyWithError(PyObject *o, PyObject *key)

   Trả về ``1`` nếu đối tượng mapping có khóa *key* và ``0`` nếu không. Điều này tương đương với biểu thức Python ``key in o``. Khi xảy ra lỗi, trả về ``-1``.

   .. versionadded:: 3.13


.. c:function:: int PyMapping_HasKeyStringWithError(PyObject *o, const char *key)

   Điều này tương tự như :c:func:`PyMapping_HasKeyWithError`, nhưng *key* được chỉ định dưới dạng một chuỗi byte được mã hóa UTF-8 :c:expr:`const char*`, thay vì một :c:expr:`PyObject*`.

   .. versionadded:: 3.13


.. c:function:: int PyMapping_HasKey(PyObject *o, PyObject *key)

   Trả về ``1`` nếu đối tượng mapping có khóa *key* và ``0`` nếu không. Điều này tương đương với biểu thức Python ``key in o``. Hàm này luôn thành công.

   .. note::

      Các ngoại lệ xảy ra khi hàm này gọi phương thức :meth:`~object.__getitem__` sẽ bị bỏ qua một cách im lặng. Để xử lý lỗi đúng cách, hãy sử dụng :c:func:`PyMapping_HasKeyWithError`,
      thay vào đó sử dụng :c:func:`PyMapping_GetOptionalItem` hoặc :c:func:`PyObject_GetItem()`.


.. c:function:: int PyMapping_HasKeyString(PyObject *o, const char *key)

   Điều này tương tự như :c:func:`PyMapping_HasKey`, nhưng *key* được chỉ định dưới dạng một chuỗi byte được mã hóa UTF-8 :c:expr:`const char*`, thay vì một :c:expr:`PyObject*`.

   .. note::

      Các ngoại lệ xảy ra khi hàm này gọi phương thức :meth:`~object.__getitem__` hoặc trong quá trình tạo đối tượng tạm thời :class:`str` sẽ bị bỏ qua một cách im lặng. Để xử lý lỗi đúng cách, hãy sử dụng :c:func:`PyMapping_HasKeyStringWithError`,
      :c:func:`PyMapping_GetOptionalItemString` hoặc
      :c:func:`PyMapping_GetItemString` thay vào đó.


.. c:function:: PyObject* PyMapping_Keys(PyObject *o)

   Khi thành công, trả về danh sách các khóa trong đối tượng *o*. Khi thất bại, trả về ``NULL``.

   .. versionchanged:: 3.7
      Trước đây, hàm này trả về một danh sách hoặc một tuple.


.. c:function:: PyObject* PyMapping_Values(PyObject *o)

   Khi thành công, trả về danh sách các giá trị trong đối tượng *o*. Khi thất bại, trả về ``NULL``.

   .. versionchanged:: 3.7
      Trước đây, hàm này trả về một danh sách hoặc một tuple.


.. c:function:: PyObject* PyMapping_Items(PyObject *o)

   Khi thành công, trả về danh sách các mục trong đối tượng *o*, trong đó mỗi mục là một tuple chứa một cặp khóa-giá trị. Khi thất bại, trả về ``NULL``.

   .. versionchanged:: 3.7
      Trước đây, hàm này trả về một danh sách hoặc một tuple.
