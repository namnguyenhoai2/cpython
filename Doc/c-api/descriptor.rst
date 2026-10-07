.. highlight:: c

.. _descriptor-objects:

Các đối tượng Descriptor
------------------------

"Descriptor" là các đối tượng mô tả một thuộc tính nào đó của một đối tượng. Chúng nằm trong từ điển của các đối tượng kiểu.

.. c:var:: PyTypeObject PyProperty_Type

   Đối tượng kiểu cho các kiểu descriptor dựng sẵn.


.. c:function:: PyObject* PyDescr_NewGetSet(PyTypeObject *type, struct PyGetSetDef *getset)

   Tạo một descriptor get-set mới cho kiểu extension *type* từ
   cấu trúc :c:type:`PyGetSetDef` structure *getset*.

   Descriptor get-set cung cấp các thuộc tính được triển khai bằng các hàm getter và setter C thay vì được lưu trữ trực tiếp trong instance. Đây là cùng loại descriptor được tạo cho các mục trong :c:member:`~PyTypeObject.tp_getset`, và nó xuất hiện trong Python dưới dạng một đối tượng :class:`types.GetSetDescriptorType`.

   Nếu thành công, trả về một :term:`strong reference` trỏ đến descriptor. Trả về ``NULL`` với một ngoại lệ được thiết lập khi thất bại.

.. c:function:: PyObject* PyDescr_NewMember(PyTypeObject *type, struct PyMemberDef *member)

   Tạo một mô tả thành viên mới cho kiểu phần mở rộng *type* từ
   :c:type:`PyMemberDef` cấu trúc *member*.

   Các mô tả thành viên cung cấp quyền truy cập các trường trong C struct của kiểu dưới dạng các thuộc tính Python. Đây là cùng loại mô tả được tạo cho các mục trong
   :c:member:`~PyTypeObject.tp_members`, và nó xuất hiện trong Python dưới dạng một
   :class:`types.MemberDescriptorType` object.

   Nếu thành công, trả về một :term:`strong reference` trỏ đến descriptor. Trả về ``NULL`` với một ngoại lệ được thiết lập khi thất bại.

.. c:var:: PyTypeObject PyMemberDescr_Type

   Đối tượng kiểu dành cho các đối tượng mô tả thành viên được tạo từ
   các cấu trúc :c:type:`PyMemberDef`. Các descriptor này cung cấp các trường của một cấu trúc C dưới dạng thuộc tính trên một kiểu, và tương ứng với các đối tượng :class:`types.MemberDescriptorType` trong Python.



.. c:var:: PyTypeObject PyGetSetDescr_Type

   Đối tượng kiểu cho các đối tượng descriptor get/set được tạo từ
   các cấu trúc :c:type:`PyGetSetDef`. Các descriptor này triển khai các thuộc tính có giá trị được tính toán bởi các hàm getter và setter của C, và được dùng cho nhiều thuộc tính kiểu dựng sẵn. Chúng tương ứng với
   các đối tượng :class:`types.GetSetDescriptorType` trong Python.


.. c:function:: PyObject* PyDescr_NewMethod(PyTypeObject *type, struct PyMethodDef *meth)

   Tạo một method descriptor mới cho extension type *type* từ
   :c:type:`PyMethodDef` cấu trúc *meth*.

   Method descriptor cung cấp các hàm C dưới dạng phương thức trên một kiểu. Đây là cùng loại descriptor được tạo cho các mục trong
   :c:member:`~PyTypeObject.tp_methods`, và trong Python, nó xuất hiện dưới dạng một
   đối tượng :class:`types.MethodDescriptorType`.

   Nếu thành công, trả về một :term:`strong reference` trỏ đến descriptor. Trả về ``NULL`` với một ngoại lệ được thiết lập khi thất bại.

.. c:var:: PyTypeObject PyMethodDescr_Type

   Đối tượng kiểu cho các đối tượng mô tả phương thức được tạo từ
   các cấu trúc :c:type:`PyMethodDef`. Các descriptor này cung cấp các hàm C dưới dạng phương thức trên một kiểu và tương ứng với các đối tượng :class:`types.MethodDescriptorType` trong Python.


.. c:struct:: wrapperbase

   Mô tả một slot wrapper được sử dụng bởi :c:func:`PyDescr_NewWrapper`.

   Mỗi bản ghi ``wrapperbase`` lưu trữ tên hiển thị trong Python và siêu dữ liệu cho một special method được triển khai bởi một type slot, cùng với hàm wrapper dùng để điều chỉnh slot đó theo quy ước gọi của Python.

.. c:function:: PyObject* PyDescr_NewWrapper(PyTypeObject *type, struct wrapperbase *base, void *wrapped)

   Tạo một wrapper descriptor mới cho extension type *type* từ
   :c:struct:`wrapperbase` cấu trúc *base* và con trỏ hàm slot được bọc *wrapped*.

   Wrapper descriptor cung cấp các phương thức đặc biệt được triển khai bởi các slot của kiểu. Đây là cùng loại descriptor mà CPython tạo cho các phương thức đặc biệt dựa trên slot như ``__repr__`` hoặc ``__add__``, và xuất hiện trong Python dưới dạng một
   :class:`types.WrapperDescriptorType` đối tượng.

   Nếu thành công, trả về một :term:`strong reference` trỏ đến descriptor. Trả về ``NULL`` với một ngoại lệ được thiết lập khi thất bại.

.. c:var:: PyTypeObject PyWrapperDescr_Type

   Đối tượng kiểu cho các wrapper descriptor được tạo bởi
   :c:func:`PyDescr_NewWrapper` và :c:func:`PyWrapper_New`. Wrapper descriptor được dùng nội bộ để cung cấp các phương thức đặc biệt được triển khai thông qua các cấu trúc wrapper, và xuất hiện trong Python dưới dạng
   Các đối tượng :class:`types.WrapperDescriptorType`.


.. c:function:: PyObject* PyDescr_NewClassMethod(PyTypeObject *type, PyMethodDef *method)

   Tạo một descriptor phương thức lớp mới cho kiểu mở rộng *type* từ
   :c:type:`PyMethodDef` cấu trúc *phương thức*.

   Descriptor phương thức lớp cung cấp các phương thức C nhận lớp thay vì một instance khi được truy cập. Đây là cùng loại descriptor được tạo cho các mục ``METH_CLASS`` trong :c:member:`~PyTypeObject.tp_methods`, và xuất hiện trong Python dưới dạng một đối tượng :class:`types.ClassMethodDescriptorType`.

   Nếu thành công, trả về một :term:`strong reference` trỏ đến descriptor. Trả về ``NULL`` với một ngoại lệ được thiết lập khi thất bại.

.. c:function:: int PyDescr_IsData(PyObject *descr)

   Trả về giá trị khác 0 nếu đối tượng descriptor *descr* mô tả một thuộc tính dữ liệu, hoặc ``0`` nếu nó mô tả một phương thức. *descr* phải là một đối tượng descriptor; không có kiểm tra lỗi.


.. c:function:: PyObject* PyWrapper_New(PyObject *d, PyObject *self)

   Tạo một đối tượng wrapper được liên kết mới từ descriptor wrapper *d* và instance *self*.

   Đây là dạng đã liên kết của một wrapper descriptor được tạo bởi
   :c:func:`PyDescr_NewWrapper`. CPython tạo các đối tượng này khi một slot wrapper được truy cập thông qua một instance, và chúng xuất hiện trong Python dưới dạng
   các đối tượng :class:`types.MethodWrapperType`.

   Khi thành công, trả về một :term:`strong reference` trỏ đến đối tượng wrapper. Khi thất bại, trả về ``NULL`` cùng với một exception đã được thiết lập.

Các descriptor tích hợp sẵn
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. c:var:: PyTypeObject PySuper_Type

   Đối tượng kiểu dành cho các đối tượng super. Đây cũng chính là đối tượng
   :class:`super` ở tầng Python.


.. c:var:: PyTypeObject PyClassMethod_Type

   Kiểu của các đối tượng phương thức lớp. Đây là cùng một đối tượng với
   :class:`classmethod` trong lớp Python.


.. c:var:: PyTypeObject PyClassMethodDescr_Type

   Đối tượng kiểu cho các đối tượng mô tả phương thức lớp ở cấp C. Đây là kiểu của các đối tượng mô tả được tạo cho :func:`classmethod` được định nghĩa trong các kiểu mở rộng C, và tương ứng với
   các đối tượng :class:`types.ClassMethodDescriptorType` trong Python.


.. c:function:: PyObject *PyClassMethod_New(PyObject *callable)

   Tạo một đối tượng :class:`classmethod` mới bao bọc *callable*. *callable* phải là một đối tượng có thể gọi và không được là ``NULL``.

   Khi thành công, hàm này trả về một :term:`strong reference` trỏ đến một bộ mô tả phương thức lớp mới. Khi thất bại, hàm này trả về ``NULL`` với một ngoại lệ đã được thiết lập.


.. c:var:: PyTypeObject PyStaticMethod_Type

   Kiểu của các đối tượng phương thức tĩnh. Đây là cùng một đối tượng với
   :class:`staticmethod` trong lớp Python.


.. c:function:: PyObject *PyStaticMethod_New(PyObject *callable)

   Tạo một đối tượng :class:`staticmethod` mới bao bọc *callable*. *callable* phải là một đối tượng có thể gọi được và không được là ``NULL``.

   Khi thành công, hàm này trả về một :term:`strong reference` trỏ đến một descriptor phương thức tĩnh mới. Khi thất bại, hàm này trả về ``NULL`` cùng với một exception đã được thiết lập.
