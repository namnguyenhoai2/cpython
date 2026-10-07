.. highlight:: c

.. _gen-objects:

Đối tượng Generator
-------------------

Đối tượng generator là những gì Python sử dụng để triển khai các generator iterator. Chúng thường được tạo bằng cách lặp qua một hàm trả về các giá trị, thay vì gọi tường minh :c:func:`PyGen_New` hoặc :c:func:`PyGen_NewWithQualName`.


.. c:type:: PyGenObject

   Cấu trúc C được sử dụng cho các đối tượng generator.


.. c:var:: PyTypeObject PyGen_Type

   Đối tượng kiểu tương ứng với các đối tượng generator.


.. c:function:: int PyGen_Check(PyObject *ob)

   Trả về true nếu *ob* là một đối tượng generator; *ob* không được là ``NULL``. Hàm này luôn thực hiện thành công.


.. c:function:: int PyGen_CheckExact(PyObject *ob)

   Trả về true nếu kiểu của *ob* là :c:type:`PyGen_Type`; *ob* không được là ``NULL``. Hàm này luôn thực hiện thành công.


.. c:function:: PyObject* PyGen_New(PyFrameObject *frame)

   Tạo và trả về một đối tượng generator mới dựa trên đối tượng *frame*. Một tham chiếu đến *frame* bị hàm này ":term:`stolen <steal>`" (ngay cả khi xảy ra lỗi). Đối số này không được là ``NULL``.

.. c:function:: PyObject* PyGen_NewWithQualName(PyFrameObject *frame, PyObject *name, PyObject *qualname)

   Tạo và trả về một đối tượng generator mới dựa trên đối tượng *frame*, với ``__name__`` và ``__qualname__`` được đặt thành *name* và *qualname*. Tham chiếu đến *frame* bị hàm này ":term:`stolen <steal>`" (ngay cả khi xảy ra lỗi). Đối số *frame* không được là ``NULL``.


.. c:function:: PyCodeObject* PyGen_GetCode(PyGenObject *gen)

   Trả về một :term:`strong reference` mới cho đối tượng mã được bao bọc bởi *gen*. Hàm này luôn thành công.


Đối tượng Generator bất đồng bộ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. seealso::
   :pep:`525`

.. c:var:: PyTypeObject PyAsyncGen_Type

   Đối tượng kiểu tương ứng với các đối tượng generator bất đồng bộ. Đối tượng này khả dụng dưới dạng :class:`types.AsyncGeneratorType` trong lớp Python.

   .. versionadded:: 3.6

.. c:function:: PyObject *PyAsyncGen_New(PyFrameObject *frame, PyObject *name, PyObject *qualname)

   Tạo một generator bất đồng bộ mới bao bọc *frame*, với ``__name__`` và ``__qualname__`` được đặt thành *name* và *qualname*. *frame* bị hàm này ":term:`stolen <steal>`" (kể cả khi xảy ra lỗi) và không được là ``NULL``.

   Khi thành công, hàm này trả về một :term:`strong reference` cho generator bất đồng bộ mới. Khi thất bại, hàm này trả về ``NULL`` với một ngoại lệ được thiết lập.

   .. versionadded:: 3.6

.. c:function:: int PyAsyncGen_CheckExact(PyObject *op)

   Trả về true nếu *op* là một đối tượng generator bất đồng bộ, nếu không thì trả về false. Hàm này luôn thành công.

   .. versionadded:: 3.6


API đã lỗi thời
^^^^^^^^^^^^^^^

.. c:macro:: PyAsyncGenASend_CheckExact(op)

   Đây là một API được đưa vào C API của Python do nhầm lẫn.

   API này chỉ được giữ lại để đầy đủ; không sử dụng API này.

   .. soft-deprecated:: 3.14
