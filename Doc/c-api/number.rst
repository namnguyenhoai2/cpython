.. highlight:: c

.. _number:

Giao thức số
============


.. c:function:: int PyNumber_Check(PyObject *o)

   Trả về ``1`` nếu đối tượng *o* cung cấp các giao thức số, và trả về false trong các trường hợp khác. Hàm này luôn thành công.

   .. versionchanged:: 3.8
      Trả về ``1`` nếu *o* là một số nguyên chỉ mục.


.. c:function:: PyObject* PyNumber_Add(PyObject *o1, PyObject *o2)

   Trả về kết quả cộng *o1* và *o2*, hoặc ``NULL`` nếu thất bại. Đây là tương đương với biểu thức Python ``o1 + o2``.


.. c:function:: PyObject* PyNumber_Subtract(PyObject *o1, PyObject *o2)

   Trả về kết quả lấy *o2* trừ *o1*, hoặc ``NULL`` nếu thất bại. Đây là tương đương với biểu thức Python ``o1 - o2``.


.. c:function:: PyObject* PyNumber_Multiply(PyObject *o1, PyObject *o2)

   Trả về kết quả nhân *o1* với *o2*, hoặc ``NULL`` nếu thất bại. Đây là tương đương với biểu thức Python ``o1 * o2``.


.. c:function:: PyObject* PyNumber_MatrixMultiply(PyObject *o1, PyObject *o2)

   Trả về kết quả phép nhân ma trận trên *o1* và *o2*, hoặc ``NULL`` nếu thất bại. Đây là tương đương với biểu thức Python ``o1 @ o2``.

   .. versionadded:: 3.5


.. c:function:: PyObject* PyNumber_FloorDivide(PyObject *o1, PyObject *o2)

   Trả về giá trị sàn của *o1* chia cho *o2*, hoặc ``NULL`` nếu xảy ra lỗi. Đây là biểu thức Python tương đương với ``o1 // o2``.


.. c:function:: PyObject* PyNumber_TrueDivide(PyObject *o1, PyObject *o2)

   Trả về giá trị xấp xỉ hợp lý của *o1* chia cho *o2*, hoặc ``NULL`` nếu xảy ra lỗi. Giá trị trả về là "xấp xỉ" vì các số dấu phẩy động nhị phân là các giá trị xấp xỉ; không thể biểu diễn mọi số thực trong hệ cơ số hai. Hàm này có thể trả về một giá trị dấu phẩy động khi được truyền vào hai số nguyên. Đây là biểu thức Python tương đương với ``o1 / o2``.


.. c:function:: PyObject* PyNumber_Remainder(PyObject *o1, PyObject *o2)

   Trả về phần dư của phép chia *o1* cho *o2*, hoặc ``NULL`` nếu xảy ra lỗi. Đây là biểu thức Python tương đương với ``o1 % o2``.


.. c:function:: PyObject* PyNumber_Divmod(PyObject *o1, PyObject *o2)

   .. index:: pair: built-in function; divmod

   Xem hàm tích hợp :func:`divmod`. Trả về ``NULL`` nếu xảy ra lỗi. Đây là biểu thức Python tương đương với ``divmod(o1, o2)``.


.. c:function:: PyObject* PyNumber_Power(PyObject *o1, PyObject *o2, PyObject *o3)

   .. index:: pair: built-in function; pow

   Xem hàm tích hợp :func:`pow`. Trả về ``NULL`` nếu xảy ra lỗi. Đây là biểu thức Python tương đương với ``pow(o1, o2, o3)``, trong đó *o3* là tùy chọn. Nếu muốn bỏ qua *o3*, hãy truyền :c:data:`Py_None` thay cho nó (truyền ``NULL`` cho *o3* sẽ gây ra lỗi truy cập bộ nhớ trái phép).


.. c:function:: PyObject* PyNumber_Negative(PyObject *o)

   Trả về phép phủ định của *o* nếu thành công, hoặc ``NULL`` nếu xảy ra lỗi. Đây là biểu thức Python tương đương với ``-o``.


.. c:function:: PyObject* PyNumber_Positive(PyObject *o)

   Trả về *o* nếu thành công, hoặc ``NULL`` nếu xảy ra lỗi. Đây là biểu thức Python tương đương với ``+o``.


.. c:function:: PyObject* PyNumber_Absolute(PyObject *o)

   .. index:: pair: built-in function; abs

   Trả về giá trị tuyệt đối của *o*, hoặc ``NULL`` nếu thất bại. Đây là tương đương với biểu thức Python ``abs(o)``.


.. c:function:: PyObject* PyNumber_Invert(PyObject *o)

   Trả về phép phủ định bit của *o* nếu thành công, hoặc ``NULL`` nếu thất bại. Đây là tương đương với biểu thức Python ``~o``.


.. c:function:: PyObject* PyNumber_Lshift(PyObject *o1, PyObject *o2)

   Trả về kết quả dịch trái *o1* đi *o2* bit nếu thành công, hoặc ``NULL`` nếu thất bại. Đây là tương đương với biểu thức Python ``o1 << o2``.


.. c:function:: PyObject* PyNumber_Rshift(PyObject *o1, PyObject *o2)

   Trả về kết quả dịch phải *o1* đi *o2* bit nếu thành công, hoặc ``NULL`` nếu thất bại. Đây là tương đương với biểu thức Python ``o1 >> o2``.


.. c:function:: PyObject* PyNumber_And(PyObject *o1, PyObject *o2)

   Trả về phép "and theo bit" của *o1* và *o2* nếu thành công, và ``NULL`` nếu thất bại. Đây là tương đương với biểu thức Python ``o1 & o2``.


.. c:function:: PyObject* PyNumber_Xor(PyObject *o1, PyObject *o2)

   Trả về phép "exclusive or theo bit" của *o1* với *o2* nếu thành công, hoặc ``NULL`` nếu thất bại. Đây là tương đương với biểu thức Python ``o1 ^ o2``.


.. c:function:: PyObject* PyNumber_Or(PyObject *o1, PyObject *o2)

   Trả về phép "or theo bit" của *o1* và *o2* nếu thành công, hoặc ``NULL`` nếu thất bại. Đây là tương đương với biểu thức Python ``o1 | o2``.


.. c:function:: PyObject* PyNumber_InPlaceAdd(PyObject *o1, PyObject *o2)

   Trả về kết quả của phép cộng *o1* và *o2*, hoặc ``NULL`` nếu thất bại. Phép toán được thực hiện *in-place* khi *o1* hỗ trợ. Đây là tương đương với câu lệnh Python ``o1 += o2``.


.. c:function:: PyObject* PyNumber_InPlaceSubtract(PyObject *o1, PyObject *o2)

   Trả về kết quả của phép trừ *o2* khỏi *o1*, hoặc ``NULL`` nếu thất bại. Phép toán được thực hiện *in-place* khi *o1* hỗ trợ. Đây là tương đương với câu lệnh Python ``o1 -= o2``.


.. c:function:: PyObject* PyNumber_InPlaceMultiply(PyObject *o1, PyObject *o2)

   Trả về kết quả của phép nhân *o1* và *o2*, hoặc ``NULL`` nếu thất bại. Phép toán được thực hiện *in-place* khi *o1* hỗ trợ. Đây là tương đương với câu lệnh Python ``o1 *= o2``.


.. c:function:: PyObject* PyNumber_InPlaceMatrixMultiply(PyObject *o1, PyObject *o2)

   Trả về kết quả của phép nhân ma trận trên *o1* và *o2*, hoặc ``NULL`` nếu thất bại. Phép toán được thực hiện *in-place* khi *o1* hỗ trợ. Đây là tương đương với câu lệnh Python ``o1 @= o2``.

   .. versionadded:: 3.5


.. c:function:: PyObject* PyNumber_InPlaceFloorDivide(PyObject *o1, PyObject *o2)

   Trả về phần nguyên theo toán học của phép chia *o1* cho *o2*, hoặc ``NULL`` nếu thất bại. Phép toán được thực hiện *in-place* khi *o1* hỗ trợ. Đây là tương đương với câu lệnh Python ``o1 //= o2``.


.. c:function:: PyObject* PyNumber_InPlaceTrueDivide(PyObject *o1, PyObject *o2)

   Trả về giá trị xấp xỉ hợp lý theo toán học của *o1* chia cho *o2*, hoặc ``NULL`` nếu thất bại. Giá trị trả về là "xấp xỉ" vì các số dấu phẩy động nhị phân là các giá trị xấp xỉ; không thể biểu diễn mọi số thực trong hệ cơ số hai. Hàm này có thể trả về một giá trị dấu phẩy động khi được truyền vào hai số nguyên. Phép toán được thực hiện *in-place* khi *o1* hỗ trợ. Đây là tương đương với câu lệnh Python ``o1 /= o2``.


.. c:function:: PyObject* PyNumber_InPlaceRemainder(PyObject *o1, PyObject *o2)

   Trả về phần dư của phép chia *o1* cho *o2*, hoặc ``NULL`` nếu thất bại. Phép toán được thực hiện *in-place* khi *o1* hỗ trợ. Đây là tương đương với câu lệnh Python ``o1 %= o2``.


.. c:function:: PyObject* PyNumber_InPlacePower(PyObject *o1, PyObject *o2, PyObject *o3)

   .. index:: pair: built-in function; pow

   Xem hàm tích hợp :func:`pow`. Trả về ``NULL`` khi xảy ra lỗi. Thao tác được thực hiện *in-place* khi *o1* hỗ trợ. Đây là tương đương với câu lệnh Python ``o1 **= o2`` khi o3 là :c:data:`Py_None`, hoặc một biến thể in-place của ``pow(o1, o2, o3)`` trong các trường hợp khác. Nếu *o3* cần được bỏ qua, hãy truyền :c:data:`Py_None` thay cho nó (truyền ``NULL`` cho *o3* sẽ gây ra lỗi truy cập bộ nhớ).


.. c:function:: PyObject* PyNumber_InPlaceLshift(PyObject *o1, PyObject *o2)

   Trả về kết quả dịch trái *o1* theo *o2* khi thành công, hoặc ``NULL`` khi xảy ra lỗi. Thao tác được thực hiện *in-place* khi *o1* hỗ trợ. Đây là tương đương với câu lệnh Python ``o1 <<= o2``.


.. c:function:: PyObject* PyNumber_InPlaceRshift(PyObject *o1, PyObject *o2)

   Trả về kết quả dịch phải *o1* theo *o2* khi thành công, hoặc ``NULL`` khi xảy ra lỗi. Thao tác được thực hiện *in-place* khi *o1* hỗ trợ. Đây là tương đương với câu lệnh Python ``o1 >>= o2``.


.. c:function:: PyObject* PyNumber_InPlaceAnd(PyObject *o1, PyObject *o2)

   Trả về phép "AND theo bit" của *o1* và *o2* khi thành công, hoặc ``NULL`` khi xảy ra lỗi. Thao tác được thực hiện *in-place* khi *o1* hỗ trợ. Đây là tương đương với câu lệnh Python ``o1 &= o2``.


.. c:function:: PyObject* PyNumber_InPlaceXor(PyObject *o1, PyObject *o2)

   Trả về phép "XOR theo bit" của *o1* với *o2* khi thành công, hoặc ``NULL`` khi xảy ra lỗi. Thao tác được thực hiện *in-place* khi *o1* hỗ trợ. Đây là tương đương với câu lệnh Python ``o1 ^= o2``.


.. c:function:: PyObject* PyNumber_InPlaceOr(PyObject *o1, PyObject *o2)

   Trả về phép "OR theo bit" của *o1* và *o2* khi thành công, hoặc ``NULL`` khi xảy ra lỗi. Thao tác được thực hiện *in-place* khi *o1* hỗ trợ. Đây là tương đương với câu lệnh Python ``o1 |= o2``.


.. c:function:: PyObject* PyNumber_Long(PyObject *o)

   .. index:: pair: built-in function; int

   Trả về *o* được chuyển đổi thành một đối tượng số nguyên khi thành công, hoặc ``NULL`` khi xảy ra lỗi. Đây là tương đương với biểu thức Python ``int(o)``.


.. c:function:: PyObject* PyNumber_Float(PyObject *o)

   .. index:: pair: built-in function; float

   Trả về *o* được chuyển đổi thành một đối tượng float khi thành công hoặc ``NULL`` khi thất bại. Đây là tương đương với biểu thức Python ``float(o)``.


.. c:function:: PyObject* PyNumber_Index(PyObject *o)

   Trả về *o* được chuyển đổi thành một Python int khi thành công hoặc ``NULL`` kèm theo một
   ngoại lệ :exc:`TypeError` được phát sinh khi thất bại.

   .. versionchanged:: 3.10
      Kết quả luôn có kiểu chính xác là :class:`int`. Trước đây, kết quả có thể là một thực thể của lớp con của ``int``.


.. c:function:: PyObject* PyNumber_ToBase(PyObject *n, int base)

   Trả về số nguyên *n* được chuyển đổi sang cơ số *base* dưới dạng chuỗi. Đối số *base* phải là một trong các giá trị 2, 8, 10 hoặc 16. Với cơ số 2, 8 hoặc 16, chuỗi trả về lần lượt được thêm tiền tố là ký hiệu cơ số ``'0b'``, ``'0o'`` hoặc ``'0x'``. Nếu *n* không phải là một Python int, nó sẽ được chuyển đổi bằng
   :c:func:`PyNumber_Index` trước tiên.


.. c:function:: Py_ssize_t PyNumber_AsSsize_t(PyObject *o, PyObject *exc)

   Trả về *o* được chuyển đổi thành một giá trị :c:type:`Py_ssize_t` nếu *o* có thể được diễn giải là một số nguyên. Nếu lệnh gọi thất bại, một ngoại lệ sẽ được phát sinh và ``-1`` được trả về.

   Nếu *o* có thể được chuyển đổi thành một số nguyên Python nhưng nỗ lực chuyển đổi thành giá trị :c:type:`Py_ssize_t` sẽ gây ra một :exc:`OverflowError`, thì đối số *exc* là kiểu ngoại lệ sẽ được phát sinh (thường là
   :exc:`IndexError` hoặc :exc:`OverflowError`). Nếu *exc* là ``NULL``, thì ngoại lệ được xóa và giá trị được giới hạn thành ``PY_SSIZE_T_MIN`` đối với số nguyên âm hoặc ``PY_SSIZE_T_MAX`` đối với số nguyên dương.


.. c:function:: int PyIndex_Check(PyObject *o)

   Trả về ``1`` nếu *o* là một số nguyên chỉ mục (có slot ``nb_index`` của cấu trúc ``tp_as_number`` được điền), và ``0`` nếu không. Hàm này luôn thành công.
