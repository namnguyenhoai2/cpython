.. highlight:: c

.. _instancemethod-objects:

Đối tượng phương thức instance
------------------------------

.. index:: pair: object; instancemethod

Một phương thức instance là một trình bao bọc cho một :c:type:`PyCFunction` và là cách mới để liên kết một :c:type:`PyCFunction` với một đối tượng lớp. Nó thay thế lệnh gọi trước đây ``PyMethod_New(func, NULL, class)``.


.. c:var:: PyTypeObject PyInstanceMethod_Type

   Instance này của :c:type:`PyTypeObject` đại diện cho kiểu phương thức instance của Python. Nó không được cung cấp cho các chương trình Python.


.. c:function:: int PyInstanceMethod_Check(PyObject *o)

   Trả về true nếu *o* là một đối tượng phương thức instance (có kiểu
   :c:data:`PyInstanceMethod_Type`). Tham số không được là ``NULL``. Hàm này luôn thực hiện thành công.


.. c:function:: PyObject* PyInstanceMethod_New(PyObject *func)

   Trả về một đối tượng phương thức instance mới, trong đó *func* là bất kỳ đối tượng callable nào. *func* là hàm sẽ được gọi khi phương thức instance được gọi.


.. c:function:: PyObject* PyInstanceMethod_Function(PyObject *im)

   Trả về đối tượng hàm được liên kết với phương thức instance *im*.


.. c:function:: PyObject* PyInstanceMethod_GET_FUNCTION(PyObject *im)

   Phiên bản macro của :c:func:`PyInstanceMethod_Function` không thực hiện kiểm tra lỗi.


.. _method-objects:

Đối tượng phương thức
---------------------

.. index:: pair: object; method

Phương thức là các đối tượng hàm được liên kết. Phương thức luôn được liên kết với một instance của lớp do người dùng định nghĩa. Các phương thức chưa liên kết (phương thức được liên kết với một đối tượng lớp) không còn khả dụng.


.. c:var:: PyTypeObject PyMethod_Type

   .. index:: single: MethodType (in module types)

   Instance này của :c:type:`PyTypeObject` đại diện cho kiểu phương thức Python. Kiểu này được cung cấp cho các chương trình Python dưới dạng ``types.MethodType``.


.. c:function:: int PyMethod_Check(PyObject *o)

   Trả về true nếu *o* là một đối tượng phương thức (có kiểu :c:data:`PyMethod_Type`). Tham số không được là ``NULL``. Hàm này luôn thành công.


.. c:function:: PyObject* PyMethod_New(PyObject *func, PyObject *self)

   Trả về một đối tượng phương thức mới, trong đó *func* là bất kỳ đối tượng có thể gọi nào và *self* là instance mà phương thức sẽ được liên kết. *func* là hàm sẽ được gọi khi phương thức được gọi. *self* không được là ``NULL``.


.. c:function:: PyObject* PyMethod_Function(PyObject *meth)

   Trả về đối tượng hàm liên kết với phương thức *meth*.


.. c:function:: PyObject* PyMethod_GET_FUNCTION(PyObject *meth)

   Phiên bản macro của :c:func:`PyMethod_Function`, không thực hiện kiểm tra lỗi.


.. c:function:: PyObject* PyMethod_Self(PyObject *meth)

   Trả về instance được liên kết với method *meth*.


.. c:function:: PyObject* PyMethod_GET_SELF(PyObject *meth)

   Phiên bản macro của :c:func:`PyMethod_Self`, không thực hiện kiểm tra lỗi.
