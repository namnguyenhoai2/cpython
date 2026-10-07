.. highlight:: c

.. _complexobjects:

Đối tượng số phức
-----------------

.. index:: pair: object; complex number

Các đối tượng số phức của Python được triển khai thành hai kiểu riêng biệt khi nhìn từ C API: một kiểu là đối tượng Python được cung cấp cho các chương trình Python, kiểu còn lại là một cấu trúc C biểu diễn giá trị số phức thực tế. API cung cấp các hàm để làm việc với cả hai kiểu này.


Số phức dưới dạng cấu trúc C
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Lưu ý rằng các hàm nhận những cấu trúc này làm tham số và trả về chúng dưới dạng kết quả thực hiện việc đó *theo giá trị* thay vì giải tham chiếu chúng thông qua con trỏ. Điều này nhất quán trong toàn bộ API.


.. c:type:: Py_complex

   Cấu trúc C tương ứng với phần giá trị của một đối tượng số phức Python. Hầu hết các hàm xử lý đối tượng số phức đều sử dụng các cấu trúc thuộc kiểu này làm giá trị đầu vào hoặc đầu ra, tùy trường hợp.

   .. c:member:: double real
                 double imag

   Cấu trúc được định nghĩa như sau::

      typedef struct {
          double real;
          double imag;
      } Py_complex;


.. c:function:: Py_complex _Py_c_sum(Py_complex left, Py_complex right)

   Trả về tổng của hai số phức, sử dụng biểu diễn :c:type:`Py_complex` của C.


.. c:function:: Py_complex _Py_c_diff(Py_complex left, Py_complex right)

   Trả về hiệu của hai số phức, sử dụng biểu diễn C
   :c:type:`Py_complex`.


.. c:function:: Py_complex _Py_c_neg(Py_complex num)

   Trả về số đối của số phức *num*, sử dụng biểu diễn C
   :c:type:`Py_complex`.


.. c:function:: Py_complex _Py_c_prod(Py_complex left, Py_complex right)

   Trả về tích của hai số phức, sử dụng biểu diễn :c:type:`Py_complex` của C.


.. c:function:: Py_complex _Py_c_quot(Py_complex dividend, Py_complex divisor)

   Trả về thương của hai số phức, sử dụng biểu diễn :c:type:`Py_complex` của C.

   Nếu *divisor* là null, phương thức này trả về 0 và đặt
   :c:data:`errno` thành :c:macro:`!EDOM`.


.. c:function:: Py_complex _Py_c_pow(Py_complex num, Py_complex exp)

   Trả về kết quả lũy thừa của *num* với số mũ *exp*, sử dụng biểu diễn C :c:type:`Py_complex`.

   Nếu *num* là null và *exp* không phải là một số thực dương, phương thức này trả về 0 và đặt :c:data:`errno` thành :c:macro:`!EDOM`.

   Đặt :c:data:`errno` thành :c:macro:`!ERANGE` khi xảy ra tràn số.


Số phức dưới dạng đối tượng Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. c:type:: PyComplexObject

   Subtype này của :c:type:`PyObject` đại diện cho một đối tượng số phức Python.


.. c:var:: PyTypeObject PyComplex_Type

   Đối tượng này của :c:type:`PyTypeObject` đại diện cho kiểu số phức Python. Nó là cùng một đối tượng với :class:`complex` ở tầng Python.


.. c:function:: int PyComplex_Check(PyObject *p)

   Trả về true nếu đối số của nó là một :c:type:`PyComplexObject` hoặc là kiểu con của
   :c:type:`PyComplexObject`. Hàm này luôn thành công.


.. c:function:: int PyComplex_CheckExact(PyObject *p)

   Trả về true nếu đối số của nó là một :c:type:`PyComplexObject`, nhưng không phải là kiểu con của
   :c:type:`PyComplexObject`. Hàm này luôn thành công.


.. c:function:: PyObject* PyComplex_FromCComplex(Py_complex v)

   Tạo một đối tượng số phức Python mới từ một giá trị :c:type:`Py_complex` của C. Trả về ``NULL`` và thiết lập ngoại lệ nếu xảy ra lỗi.


.. c:function:: PyObject* PyComplex_FromDoubles(double real, double imag)

   Trả về một đối tượng :c:type:`PyComplexObject` mới từ *real* và *imag*. Trả về ``NULL`` và thiết lập ngoại lệ nếu xảy ra lỗi.


.. c:function:: double PyComplex_RealAsDouble(PyObject *op)

   Trả về phần thực của *op* dưới dạng một :c:expr:`double` trong C.

   Nếu *op* không phải là một đối tượng số phức Python nhưng có một
   phương thức :meth:`~object.__complex__`, phương thức này sẽ được gọi trước tiên để chuyển đổi *op* thành một đối tượng số phức Python. Nếu :meth:`!__complex__` chưa được định nghĩa thì phương thức này sẽ gọi :c:func:`PyFloat_AsDouble` thay thế và trả về kết quả của nó.

   Khi thất bại, phương thức này trả về ``-1.0`` cùng với một ngoại lệ đã được thiết lập, vì vậy cần gọi :c:func:`PyErr_Occurred` để kiểm tra lỗi.

   .. versionchanged:: 3.13
      Sử dụng :meth:`~object.__complex__` nếu có.

.. c:function:: double PyComplex_ImagAsDouble(PyObject *op)

   Trả về phần ảo của *op* dưới dạng một :c:expr:`double` trong C.

   Nếu *op* không phải là một đối tượng số phức Python nhưng có một
   phương thức :meth:`~object.__complex__`, phương thức này trước tiên sẽ được gọi để chuyển *op* thành một đối tượng số phức Python. Nếu :meth:`!__complex__` chưa được định nghĩa thì phương thức này sẽ chuyển sang gọi :c:func:`PyFloat_AsDouble` và trả về ``0.0`` khi thành công.

   Khi thất bại, phương thức này trả về ``-1.0`` cùng với một ngoại lệ đã được thiết lập, vì vậy cần gọi :c:func:`PyErr_Occurred` để kiểm tra lỗi.

   .. versionchanged:: 3.13
      Sử dụng :meth:`~object.__complex__` nếu có.

.. c:function:: Py_complex PyComplex_AsCComplex(PyObject *op)

   Trả về giá trị :c:type:`Py_complex` của số phức *op*.

   Nếu *op* không phải là một đối tượng số phức Python nhưng có phương thức :meth:`~object.__complex__`, phương thức này trước tiên sẽ được gọi để chuyển *op* thành một đối tượng số phức Python. Nếu :meth:`!__complex__` chưa được định nghĩa thì phương thức này sẽ chuyển sang
   :meth:`~object.__float__`. Nếu :meth:`!__float__` chưa được định nghĩa thì phương thức này sẽ chuyển sang :meth:`~object.__index__`.

   Khi thất bại, phương thức này trả về :c:type:`Py_complex` với :c:member:`~Py_complex.real` được đặt thành ``-1.0`` và một exception được thiết lập, vì vậy cần gọi :c:func:`PyErr_Occurred` để kiểm tra lỗi.

   .. versionchanged:: 3.8
      Sử dụng :meth:`~object.__index__` nếu có sẵn.
