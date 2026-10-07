.. highlight:: c

.. _typehintobjects:

Đối tượng để gợi ý kiểu
-----------------------

Có nhiều kiểu dựng sẵn được cung cấp để gợi ý kiểu. Hiện tại, có hai kiểu là :ref:`GenericAlias <types-genericalias>` và
:ref:`Union <types-union>`. Chỉ ``GenericAlias`` được cung cấp cho C.

.. c:function:: PyObject* Py_GenericAlias(PyObject *origin, PyObject *args)

   Tạo một đối tượng :ref:`GenericAlias <types-genericalias>`. Tương đương với việc gọi class Python
   :class:`types.GenericAlias`. Các đối số *origin* và *args* lần lượt thiết lập các thuộc tính ``__origin__`` và ``__args__`` của ``GenericAlias``\ . *origin* phải là một :c:expr:`PyTypeObject*`, còn *args* có thể là
   một :c:expr:`PyTupleObject*` hoặc bất kỳ ``PyObject*`` nào. Nếu *args* được truyền vào không phải là một tuple, một tuple 1 phần tử sẽ được tự động tạo và ``__args__`` được đặt thành ``(args,)``. Chỉ thực hiện kiểm tra tối thiểu đối với các đối số, vì vậy hàm vẫn thành công ngay cả khi *origin* không phải là một kiểu. Đối tượng ``GenericAlias``\  có thuộc tính ``__parameters__`` được tạo một cách trì hoãn từ ``__args__``. Khi thất bại, một ngoại lệ được phát sinh và ``NULL`` được trả về.

   Sau đây là ví dụ về cách tạo một kiểu mở rộng generic::

      ...
      static PyMethodDef my_obj_methods[] = {
          // Other methods.
          ...
          {"__class_getitem__", Py_GenericAlias, METH_O|METH_CLASS, "my_obj is generic over its contained type"}
          ...
      }

   .. seealso:: Phương thức data model :meth:`~object.__class_getitem__`.

   .. versionadded:: 3.9

.. c:var:: PyTypeObject Py_GenericAliasType

   Kiểu C của đối tượng được trả về bởi :c:func:`Py_GenericAlias`. Tương đương với
   :class:`types.GenericAlias` trong Python.

   .. versionadded:: 3.9
