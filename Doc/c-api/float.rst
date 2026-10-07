.. highlight:: c

.. _floatobjects:

Đối tượng số dấu phẩy động
==========================

.. index:: pair: object; floating-point


.. c:type:: PyFloatObject

   Kiểu con này của :c:type:`PyObject` đại diện cho một đối tượng số dấu phẩy động trong Python.


.. c:var:: PyTypeObject PyFloat_Type

   Thể hiện này của :c:type:`PyTypeObject` đại diện cho kiểu số dấu phẩy động trong Python. Đây là cùng một đối tượng với :class:`float` ở lớp Python.


.. c:function:: int PyFloat_Check(PyObject *p)

   Trả về true nếu đối số của nó là một :c:type:`PyFloatObject` hoặc một kiểu con của
   :c:type:`PyFloatObject`. Hàm này luôn thành công.


.. c:function:: int PyFloat_CheckExact(PyObject *p)

   Trả về true nếu đối số của nó là một :c:type:`PyFloatObject`, nhưng không phải là một kiểu con của
   :c:type:`PyFloatObject`. Hàm này luôn thành công.


.. c:function:: PyObject* PyFloat_FromString(PyObject *str)

   Tạo một đối tượng :c:type:`PyFloatObject` dựa trên giá trị chuỗi trong *str*, hoặc ``NULL`` nếu thất bại.


.. c:function:: PyObject* PyFloat_FromDouble(double v)

   Tạo một đối tượng :c:type:`PyFloatObject` từ *v*, hoặc ``NULL`` nếu thất bại.


.. c:function:: double PyFloat_AsDouble(PyObject *pyfloat)

   Trả về biểu diễn C :c:expr:`double` của nội dung trong *pyfloat*. Nếu *pyfloat* không phải là một đối tượng số thực Python nhưng có phương thức :meth:`~object.__float__`, phương thức này sẽ được gọi trước tiên để chuyển *pyfloat* thành một số thực. Nếu :meth:`!__float__` không được định nghĩa thì hàm sẽ chuyển sang :meth:`~object.__index__`. Phương thức này trả về ``-1.0`` khi thất bại, vì vậy nên gọi
   :c:func:`PyErr_Occurred` để kiểm tra lỗi.

   .. versionchanged:: 3.8
      Sử dụng :meth:`~object.__index__` nếu có.


.. c:function:: double PyFloat_AS_DOUBLE(PyObject *pyfloat)

   Trả về biểu diễn C :c:expr:`double` của nội dung trong *pyfloat*, nhưng không kiểm tra lỗi.


.. c:function:: PyObject* PyFloat_GetInfo(void)

   Trả về một thực thể structseq chứa thông tin về độ chính xác, giá trị tối thiểu và tối đa của một số thực. Đây là một lớp bao bọc mỏng quanh tệp tiêu đề :file:`float.h`.


.. c:function:: double PyFloat_GetMax()

   Trả về số thực hữu hạn lớn nhất có thể biểu diễn *DBL_MAX* dưới dạng C :c:expr:`double`.


.. c:function:: double PyFloat_GetMin()

   Trả về số thực dương đã chuẩn hóa nhỏ nhất *DBL_MIN* dưới dạng C :c:expr:`double`.


.. c:macro:: Py_INFINITY

   Macro này mở rộng thành một biểu thức hằng có kiểu :c:expr:`double`, biểu diễn vô cực dương.

   Trên hầu hết các nền tảng, giá trị này tương đương với macro :c:macro:`!INFINITY` trong header tiêu chuẩn C11 ``<math.h>``.


.. c:macro:: Py_NAN

   Macro này mở rộng thành một biểu thức hằng có kiểu :c:expr:`double`, biểu diễn một giá trị không phải số yên lặng (qNaN).

   Trên hầu hết các nền tảng, giá trị này tương đương với macro :c:macro:`!NAN` trong header tiêu chuẩn C11 ``<math.h>``.


.. c:macro:: Py_HUGE_VAL

   Tương đương với :c:macro:`!INFINITY`.

   .. deprecated:: 3.14
      Macro là :term:`soft deprecated`.


.. c:macro:: Py_MATH_E

   Định nghĩa hằng số :data:`math.e` (chính xác đối với kiểu :c:expr:`double`).


.. c:macro:: Py_MATH_El

   Định nghĩa độ chính xác cao (long double) của hằng số :data:`~math.e`.


.. c:macro:: Py_MATH_PI

   Định nghĩa hằng số :data:`math.pi` (chính xác đối với kiểu :c:expr:`double`).


.. c:macro:: Py_MATH_PIl

   Định nghĩa độ chính xác cao (long double) của hằng số :data:`~math.pi`.


.. c:macro:: Py_MATH_TAU

   Định nghĩa hằng số :data:`math.tau` (chính xác đối với kiểu :c:expr:`double`).

   .. versionadded:: 3.6


.. c:macro:: Py_RETURN_NAN

   Trả về :data:`math.nan` từ một hàm.

   Trên hầu hết các nền tảng, điều này tương đương với ``return PyFloat_FromDouble(NAN)``.


.. c:macro:: Py_RETURN_INF(sign)

   Trả về :data:`math.inf` hoặc :data:`-math.inf <math.inf>` từ một hàm, tùy thuộc vào dấu của *sign*.

   Trên hầu hết các nền tảng, điều này tương đương với nội dung sau::

      return PyFloat_FromDouble(copysign(INFINITY, sign));


.. c:macro:: Py_IS_FINITE(X)

   Trả về ``1`` nếu số dấu phẩy động đã cho *X* là hữu hạn, nghĩa là số đó là số chuẩn, số dưới chuẩn hoặc bằng không, nhưng không phải là vô cực hoặc NaN. Nếu không, trả về ``0``.

   .. deprecated:: 3.14
      Macro này là :term:`soft deprecated`. Thay vào đó, hãy sử dụng :c:macro:`!isfinite`.


.. c:macro:: Py_IS_INFINITY(X)

   Trả về ``1`` nếu số dấu phẩy động đã cho *X* là vô cực dương hoặc vô cực âm. Nếu không, trả về ``0``.

   .. deprecated:: 3.14
      Macro này là :term:`soft deprecated`. Thay vào đó, hãy sử dụng :c:macro:`!isinf`.


.. c:macro:: Py_IS_NAN(X)

   Trả về ``1`` nếu số dấu phẩy động đã cho *X* là một giá trị không phải là số (NaN).  Nếu không, trả về ``0``.

   .. deprecated:: 3.14
      Macro là :term:`soft deprecated`.  Thay vào đó, hãy sử dụng :c:macro:`!isnan`.


Các hàm Pack và Unpack
----------------------

Các hàm pack và unpack cung cấp một cách hiệu quả, độc lập với nền tảng để lưu trữ các giá trị dấu phẩy động dưới dạng chuỗi byte. Các routine Pack tạo ra một chuỗi bytes từ một :c:expr:`double` C, còn các routine Unpack tạo ra một C
:c:expr:`double` từ chuỗi bytes đó. Hậu tố (2, 4 hoặc 8) chỉ định số byte trong chuỗi bytes.

Trên các nền tảng có vẻ sử dụng các định dạng IEEE 754, những hàm này hoạt động bằng cách sao chép các bit. Trên các nền tảng khác, định dạng 2 byte giống hệt định dạng binary16 half-precision của IEEE 754, định dạng 4 byte (32 bit) giống hệt định dạng binary32 single precision của IEEE 754, còn định dạng 8 byte giống định dạng binary64 double precision của IEEE 754, mặc dù việc đóng gói INF và NaN (nếu các giá trị như vậy tồn tại trên nền tảng) không được xử lý chính xác, và việc cố gắng unpack một chuỗi bytes chứa INF hoặc NaN IEEE sẽ raise một exception.

Lưu ý rằng kiểu NaN có thể không được bảo toàn trên các nền tảng IEEE (signaling NaN trở thành quiet NaN), chẳng hạn như trên các hệ thống x86 ở chế độ 32 bit.

Trên các nền tảng không tuân theo IEEE có độ chính xác cao hơn hoặc phạm vi động lớn hơn những gì IEEE 754 hỗ trợ, không phải mọi giá trị đều có thể được đóng gói; trên các nền tảng không tuân theo IEEE có độ chính xác thấp hơn hoặc phạm vi động nhỏ hơn, không phải mọi giá trị đều có thể được giải nén. Điều xảy ra trong những trường hợp như vậy phần nào là ngẫu nhiên (đáng tiếc là vậy).

.. versionadded:: 3.11

Các hàm pack
^^^^^^^^^^^^

Các routine pack ghi 2, 4 hoặc 8 byte, bắt đầu từ *p*. *le* là một
:c:expr:`int` argument, khác 0 nếu bạn muốn chuỗi byte ở định dạng little-endian (exponent ở cuối, tại ``p+1``, ``p+3``, hoặc ``p+6`` và ``p+7``), bằng 0 nếu bạn muốn định dạng big-endian (exponent ở đầu, tại *p*). Hằng số :c:macro:`PY_BIG_ENDIAN` có thể được dùng để sử dụng endian gốc: nó bằng ``1`` trên bộ xử lý big endian hoặc ``0`` trên bộ xử lý little endian.

Giá trị trả về: ``0`` nếu mọi thứ đều ổn, ``-1`` nếu có lỗi (và một exception được thiết lập, nhiều khả năng là :exc:`OverflowError`).

Có hai vấn đề trên các nền tảng không tuân theo IEEE:

* Điều này không được định nghĩa nếu *x* là NaN hoặc vô hạn.
* ``-0.0`` và ``+0.0`` tạo ra cùng một chuỗi byte.

.. c:function:: int PyFloat_Pack2(double x, char *p, int le)

   Đóng gói một C double theo định dạng half-precision nhị phân IEEE 754 binary16.

.. c:function:: int PyFloat_Pack4(double x, char *p, int le)

   Đóng gói một C double theo định dạng single precision nhị phân IEEE 754 binary32.

.. c:function:: int PyFloat_Pack8(double x, char *p, int le)

   Đóng gói một C double theo định dạng double precision nhị phân IEEE 754 binary64.


Các hàm unpack
^^^^^^^^^^^^^^

Các routine unpack đọc 2, 4 hoặc 8 byte, bắt đầu từ *p*.  *le* là một
:c:expr:`int` đối số, khác 0 nếu chuỗi byte ở định dạng little-endian (exponent ở cuối, tại ``p+1``, ``p+3`` hoặc ``p+6`` và ``p+7``), bằng 0 nếu ở định dạng big-endian (exponent ở đầu, tại *p*). Có thể dùng hằng số :c:macro:`PY_BIG_ENDIAN` để sử dụng endian gốc: hằng số này bằng ``1`` trên bộ xử lý big endian hoặc ``0`` trên bộ xử lý little endian.

Giá trị trả về: double đã được giải nén. Khi có lỗi, giá trị này là ``-1.0`` và
:c:func:`PyErr_Occurred` là true (và một exception được thiết lập, nhiều khả năng
:exc:`OverflowError`).

Lưu ý rằng trên nền tảng không phải IEEE, hàm này sẽ từ chối giải nén một chuỗi bytes biểu diễn NaN hoặc infinity.

.. c:function:: double PyFloat_Unpack2(const char *p, int le)

   Giải nén định dạng binary16 half-precision IEEE 754 thành một C double.

.. c:function:: double PyFloat_Unpack4(const char *p, int le)

   Giải nén định dạng binary32 single precision IEEE 754 thành một C double.

.. c:function:: double PyFloat_Unpack8(const char *p, int le)

   Giải nén định dạng binary64 double precision IEEE 754 thành một C double.
