.. highlight:: c

.. _longobjects:

Đối tượng số nguyên
-------------------

.. index:: pair: object; long integer
           pair: object; integer

Tất cả số nguyên được triển khai dưới dạng các đối tượng số nguyên "long" có kích thước tùy ý.

Khi xảy ra lỗi, hầu hết các API ``PyLong_As*`` trả về ``(return type)-1``, giá trị này không thể phân biệt với một số. Hãy sử dụng :c:func:`PyErr_Occurred` để phân biệt.

.. c:type:: PyLongObject

   Kiểu con này của :c:type:`PyObject` đại diện cho một đối tượng số nguyên Python.


.. c:var:: PyTypeObject PyLong_Type

   Thể hiện này của :c:type:`PyTypeObject` đại diện cho kiểu số nguyên Python. Đây chính là đối tượng :class:`int` trong lớp Python.


.. c:function:: int PyLong_Check(PyObject *p)

   Trả về true nếu đối số của nó là :c:type:`PyLongObject` hoặc một kiểu con của
   :c:type:`PyLongObject`. Hàm này luôn thành công.


.. c:function:: int PyLong_CheckExact(PyObject *p)

   Trả về true nếu đối số của nó là một :c:type:`PyLongObject`, nhưng không phải là kiểu con của
   :c:type:`PyLongObject`. Hàm này luôn thành công.


.. c:function:: PyObject* PyLong_FromLong(long v)

   Trả về một đối tượng :c:type:`PyLongObject` mới từ *v*, hoặc ``NULL`` nếu thất bại.

   .. impl-detail::

      CPython duy trì một mảng các đối tượng số nguyên cho tất cả các số nguyên từ ``-5`` đến ``256``. Khi bạn tạo một int trong phạm vi đó, thực tế bạn chỉ nhận lại một tham chiếu đến đối tượng hiện có.


.. c:function:: PyObject* PyLong_FromUnsignedLong(unsigned long v)

   Trả về một đối tượng :c:type:`PyLongObject` mới từ một :c:expr:`unsigned long` C, hoặc ``NULL`` nếu thất bại.


.. c:function:: PyObject* PyLong_FromSsize_t(Py_ssize_t v)

   Trả về một đối tượng :c:type:`PyLongObject` mới từ một :c:type:`Py_ssize_t` C, hoặc ``NULL`` nếu thất bại.


.. c:function:: PyObject* PyLong_FromSize_t(size_t v)

   Trả về một đối tượng :c:type:`PyLongObject` mới từ một :c:type:`size_t` C, hoặc ``NULL`` nếu thất bại.


.. c:function:: PyObject* PyLong_FromLongLong(long long v)

   Trả về một đối tượng :c:type:`PyLongObject` mới từ một kiểu C :c:expr:`long long`, hoặc ``NULL`` nếu thất bại.


.. c:function:: PyObject* PyLong_FromUnsignedLongLong(unsigned long long v)

   Trả về một đối tượng :c:type:`PyLongObject` mới từ một kiểu C :c:expr:`unsigned long long`, hoặc ``NULL`` nếu thất bại.


.. c:function:: PyObject* PyLong_FromInt32(int32_t value)
                PyObject* PyLong_FromInt64(int64_t value)

   Trả về một đối tượng :c:type:`PyLongObject` mới từ một kiểu C có dấu
   :c:expr:`int32_t` hoặc :c:expr:`int64_t`, hoặc ``NULL`` với một ngoại lệ được thiết lập nếu thất bại.

   .. versionadded:: 3.14


.. c:function:: PyObject* PyLong_FromUInt32(uint32_t value)
                PyObject* PyLong_FromUInt64(uint64_t value)

   Trả về một đối tượng :c:type:`PyLongObject` mới từ một kiểu C không dấu
   :c:expr:`uint32_t` hoặc :c:expr:`uint64_t`, hoặc ``NULL`` với một exception được thiết lập khi thất bại.

   .. versionadded:: 3.14


.. c:function:: PyObject* PyLong_FromDouble(double v)

   Trả về một đối tượng :c:type:`PyLongObject` mới từ phần nguyên của *v*, hoặc ``NULL`` khi thất bại.


.. c:function:: PyObject* PyLong_FromString(const char *str, char **pend, int base)

   Trả về một :c:type:`PyLongObject` mới dựa trên giá trị chuỗi trong *str*, được diễn giải theo cơ số trong *base*, hoặc ``NULL`` khi thất bại. Nếu *pend* khác ``NULL``, *\*pend* sẽ trỏ đến cuối *str* khi thành công hoặc đến ký tự đầu tiên không thể xử lý khi xảy ra lỗi. Nếu *base* là ``0``, *str* được diễn giải theo định nghĩa :ref:`integers`; trong trường hợp này, các số 0 đứng đầu trong một số thập phân khác 0 sẽ gây ra :exc:`ValueError`. Nếu *base* không phải là ``0``, giá trị này phải nằm trong khoảng từ ``2`` đến ``36``, bao gồm cả hai. Khoảng trắng ở đầu và cuối, cùng với các dấu gạch dưới đơn sau chỉ báo cơ số và giữa các chữ số, sẽ bị bỏ qua. Nếu không có chữ số hoặc *str* không được kết thúc bằng NULL sau các chữ số và khoảng trắng ở cuối, :exc:`ValueError` sẽ được raised.

   .. seealso:: :c:func:`PyLong_AsNativeBytes()` và
      :c:func:`PyLong_FromNativeBytes()` functions can be used to convert
      một :c:type:`PyLongObject` đến/từ một mảng byte ở cơ số ``256``.


.. c:function:: PyObject* PyLong_FromUnicodeObject(PyObject *u, int base)

   Chuyển đổi một chuỗi các chữ số Unicode trong chuỗi *u* thành một giá trị số nguyên Python.

   .. versionadded:: 3.3


.. c:function:: PyObject* PyLong_FromVoidPtr(void *p)

   Tạo một số nguyên Python từ con trỏ *p*. Có thể truy xuất giá trị con trỏ từ giá trị thu được bằng :c:func:`PyLong_AsVoidPtr`.


.. c:function:: PyObject* PyLong_FromNativeBytes(const void* buffer, size_t n_bytes, int flags)

   Tạo một số nguyên Python từ giá trị nằm trong *n_bytes* đầu tiên của *buffer*, được diễn giải là một số có dấu bù hai.

   *flags* giống như đối với :c:func:`PyLong_AsNativeBytes`. Truyền ``-1`` sẽ chọn thứ tự byte native mà CPython được biên dịch cùng và giả định rằng bit quan trọng nhất là bit dấu. Truyền ``Py_ASNATIVEBYTES_UNSIGNED_BUFFER`` sẽ cho kết quả giống như gọi
   :c:func:`PyLong_FromUnsignedNativeBytes`. Các cờ khác bị bỏ qua.

   .. versionadded:: 3.13


.. c:function:: PyObject* PyLong_FromUnsignedNativeBytes(const void* buffer, size_t n_bytes, int flags)

   Tạo một số nguyên Python từ giá trị nằm trong *n_bytes* đầu tiên của *buffer*, được diễn giải là một số không dấu.

   *flags* giống như đối với :c:func:`PyLong_AsNativeBytes`. Truyền ``-1`` sẽ chọn thứ tự byte native mà CPython được biên dịch cùng và giả định rằng bit quan trọng nhất không phải là bit dấu. Các cờ khác ngoài thứ tự byte bị bỏ qua.

   .. versionadded:: 3.13


.. c:macro:: PyLong_FromPid(pid)

   Macro để tạo một số nguyên Python từ mã định danh tiến trình.

   Có thể định nghĩa macro này làm bí danh cho :c:func:`PyLong_FromLong` hoặc
   :c:func:`PyLong_FromLongLong`, tùy thuộc vào kích thước của kiểu PID của hệ thống.

   .. versionadded:: 3.2


.. c:function:: long PyLong_AsLong(PyObject *obj)

   .. index::
      single: LONG_MAX (C macro)
      single: OverflowError (built-in exception)

   Trả về biểu diễn C :c:expr:`long` của *obj*. Nếu *obj* không phải là một thể hiện của :c:type:`PyLongObject`, trước tiên hãy gọi phương thức :meth:`~object.__index__` của nó (nếu có) để chuyển đổi nó thành một :c:type:`PyLongObject`.

   Phát sinh :exc:`OverflowError` nếu giá trị của *obj* nằm ngoài phạm vi của một
   :c:expr:`long`.

   Trả về ``-1`` khi có lỗi. Sử dụng :c:func:`PyErr_Occurred` để phân biệt.

   .. versionchanged:: 3.8
      Sử dụng :meth:`~object.__index__` nếu có.

   .. versionchanged:: 3.10
      Hàm này sẽ không còn sử dụng :meth:`~object.__int__`.

   .. c:namespace:: NULL

   .. c:function:: long PyLong_AS_LONG(PyObject *obj)

      Hoàn toàn tương đương với ``PyLong_AsLong`` được ưu tiên. Cụ thể, nó có thể thất bại với :exc:`OverflowError` hoặc một ngoại lệ khác.

      .. soft-deprecated:: 3.14

.. c:function:: int PyLong_AsInt(PyObject *obj)

   Tương tự như :c:func:`PyLong_AsLong`, nhưng lưu kết quả vào một C
   :c:expr:`int` thay vì một C :c:expr:`long`.

   .. versionadded:: 3.13


.. c:function:: long PyLong_AsLongAndOverflow(PyObject *obj, int *overflow)

   Trả về biểu diễn C :c:expr:`long` của *obj*. Nếu *obj* không phải là một thể hiện của :c:type:`PyLongObject`, trước tiên hãy gọi phương thức :meth:`~object.__index__` của nó (nếu có) để chuyển đổi nó thành một :c:type:`PyLongObject`.

   Nếu giá trị của *obj* lớn hơn :c:macro:`LONG_MAX` hoặc nhỏ hơn
   :c:macro:`LONG_MIN`, hãy đặt *\*overflow* thành ``1`` hoặc ``-1``, tương ứng, rồi trả về ``-1``; nếu không, hãy đặt *\*overflow* thành ``0``. Nếu xảy ra bất kỳ ngoại lệ nào khác, hãy đặt *\*overflow* thành ``0`` và trả về ``-1`` như thường lệ.

   Trả về ``-1`` khi có lỗi. Sử dụng :c:func:`PyErr_Occurred` để phân biệt.

   .. versionchanged:: 3.8
      Sử dụng :meth:`~object.__index__` nếu có.

   .. versionchanged:: 3.10
      Hàm này sẽ không còn sử dụng :meth:`~object.__int__`.


.. c:function:: long long PyLong_AsLongLong(PyObject *obj)

   .. index::
      single: OverflowError (built-in exception)

   Trả về biểu diễn C :c:expr:`long long` của *obj*. Nếu *obj* không phải là một thể hiện của :c:type:`PyLongObject`, trước tiên hãy gọi phương thức :meth:`~object.__index__` của nó (nếu có) để chuyển đổi nó thành một :c:type:`PyLongObject`.

   Phát sinh :exc:`OverflowError` nếu giá trị của *obj* nằm ngoài phạm vi của một
   :c:expr:`long long`.

   Trả về ``-1`` khi có lỗi. Sử dụng :c:func:`PyErr_Occurred` để phân biệt.

   .. versionchanged:: 3.8
      Sử dụng :meth:`~object.__index__` nếu có.

   .. versionchanged:: 3.10
      Hàm này sẽ không còn sử dụng :meth:`~object.__int__`.


.. c:function:: long long PyLong_AsLongLongAndOverflow(PyObject *obj, int *overflow)

   Trả về biểu diễn C :c:expr:`long long` của *obj*. Nếu *obj* không phải là một thể hiện của :c:type:`PyLongObject`, trước tiên hãy gọi phương thức :meth:`~object.__index__` của nó (nếu có) để chuyển đổi nó thành một :c:type:`PyLongObject`.

   Nếu giá trị của *obj* lớn hơn :c:macro:`LLONG_MAX` hoặc nhỏ hơn
   :c:macro:`LLONG_MIN`, lần lượt đặt *\*overflow* thành ``1`` hoặc ``-1``, rồi trả về ``-1``; nếu không, đặt *\*overflow* thành ``0``.  Nếu xảy ra bất kỳ ngoại lệ nào khác, đặt *\*overflow* thành ``0`` và trả về ``-1`` như thường lệ.

   Trả về ``-1`` khi có lỗi. Sử dụng :c:func:`PyErr_Occurred` để phân biệt.

   .. versionadded:: 3.2

   .. versionchanged:: 3.8
      Sử dụng :meth:`~object.__index__` nếu có.

   .. versionchanged:: 3.10
      Hàm này sẽ không còn sử dụng :meth:`~object.__int__`.


.. c:function:: Py_ssize_t PyLong_AsSsize_t(PyObject *pylong)

   .. index::
      single: PY_SSIZE_T_MAX (C macro)
      single: OverflowError (built-in exception)

   Trả về một biểu diễn C :c:type:`Py_ssize_t` của *pylong*. *pylong* phải là một thực thể của :c:type:`PyLongObject`.

   Phát sinh :exc:`OverflowError` nếu giá trị của *pylong* nằm ngoài phạm vi cho một
   :c:type:`Py_ssize_t`.

   Trả về ``-1`` khi có lỗi. Sử dụng :c:func:`PyErr_Occurred` để phân biệt.


.. c:function:: unsigned long PyLong_AsUnsignedLong(PyObject *pylong)

   .. index::
      single: ULONG_MAX (C macro)
      single: OverflowError (built-in exception)

   Trả về biểu diễn C :c:expr:`unsigned long` của *pylong*.  *pylong* phải là một thể hiện của :c:type:`PyLongObject`.

   Phát sinh :exc:`OverflowError` nếu giá trị của *pylong* nằm ngoài phạm vi cho một
   :c:expr:`unsigned long`.

   Trả về ``(unsigned long)-1`` khi xảy ra lỗi. Sử dụng :c:func:`PyErr_Occurred` để phân biệt rõ.


.. c:function:: size_t PyLong_AsSize_t(PyObject *pylong)

   .. index::
      single: SIZE_MAX (C macro)
      single: OverflowError (built-in exception)

   Trả về biểu diễn C :c:type:`size_t` của *pylong*.  *pylong* phải là một thể hiện của :c:type:`PyLongObject`.

   Phát sinh :exc:`OverflowError` nếu giá trị của *pylong* nằm ngoài phạm vi cho một
   :c:type:`size_t`.

   Trả về ``(size_t)-1`` khi xảy ra lỗi. Sử dụng :c:func:`PyErr_Occurred` để phân biệt rõ.


.. c:function:: unsigned long long PyLong_AsUnsignedLongLong(PyObject *pylong)

   .. index::
      single: OverflowError (built-in exception)

   Trả về biểu diễn :c:expr:`unsigned long long` bằng C của *pylong*. *pylong* phải là một thực thể của :c:type:`PyLongObject`.

   Phát sinh :exc:`OverflowError` nếu giá trị của *pylong* nằm ngoài phạm vi của một
   :c:expr:`unsigned long long`.

   Trả về ``(unsigned long long)-1`` khi xảy ra lỗi. Sử dụng :c:func:`PyErr_Occurred` để phân biệt.

   .. versionchanged:: 3.1
      Một *pylong* âm hiện sẽ phát sinh :exc:`OverflowError`, không phải :exc:`TypeError`.


.. c:function:: unsigned long PyLong_AsUnsignedLongMask(PyObject *obj)

   Trả về biểu diễn :c:expr:`unsigned long` bằng C của *obj*. Nếu *obj* không phải là một thực thể của :c:type:`PyLongObject`, trước tiên hãy gọi phương thức :meth:`~object.__index__` của nó (nếu có) để chuyển đổi nó thành một :c:type:`PyLongObject`.

   Nếu giá trị của *obj* nằm ngoài phạm vi của một :c:expr:`unsigned long`, trả về phần rút gọn của giá trị đó theo modulo ``ULONG_MAX + 1``.

   Trả về ``(unsigned long)-1`` khi xảy ra lỗi. Sử dụng :c:func:`PyErr_Occurred` để phân biệt.

   .. versionchanged:: 3.8
      Sử dụng :meth:`~object.__index__` nếu có.

   .. versionchanged:: 3.10
      Hàm này sẽ không còn sử dụng :meth:`~object.__int__`.


.. c:function:: unsigned long long PyLong_AsUnsignedLongLongMask(PyObject *obj)

   Trả về biểu diễn C :c:expr:`unsigned long long` của *obj*. Nếu *obj* không phải là một thể hiện của :c:type:`PyLongObject`, trước tiên hãy gọi phương thức của nó
   :meth:`~object.__index__` (nếu có) để chuyển đổi nó thành một
   :c:type:`PyLongObject`.

   Nếu giá trị của *obj* nằm ngoài phạm vi của một :c:expr:`unsigned long long`, hãy trả về phần dư của giá trị đó khi chia cho ``ULLONG_MAX + 1``.

   Trả về ``(unsigned long long)-1`` khi xảy ra lỗi. Sử dụng :c:func:`PyErr_Occurred` để phân biệt.

   .. versionchanged:: 3.8
      Sử dụng :meth:`~object.__index__` nếu có.

   .. versionchanged:: 3.10
      Hàm này sẽ không còn sử dụng :meth:`~object.__int__`.


.. c:function:: int PyLong_AsInt32(PyObject *obj, int32_t *value)
                int PyLong_AsInt64(PyObject *obj, int64_t *value)

   Đặt *\*value* thành biểu diễn C có dấu :c:expr:`int32_t` hoặc :c:expr:`int64_t` của *obj*.

   Nếu *obj* không phải là một thể hiện của :c:type:`PyLongObject`, trước tiên hãy gọi hàm của nó
   :meth:`~object.__index__` (nếu có) để chuyển đổi nó thành một
   :c:type:`PyLongObject`.

   Nếu giá trị *obj* nằm ngoài phạm vi, hãy đưa ra một :exc:`OverflowError`.

   Đặt *\*value* và trả về ``0`` khi thành công. Đặt một exception và trả về ``-1`` khi có lỗi.

   *value* không được là ``NULL``.

   .. versionadded:: 3.14


.. c:function:: int PyLong_AsUInt32(PyObject *obj, uint32_t *value)
                int PyLong_AsUInt64(PyObject *obj, uint64_t *value)

   Đặt *\*value* thành một biểu diễn C unsigned :c:expr:`uint32_t` hoặc :c:expr:`uint64_t` của *obj*.

   Nếu *obj* không phải là một thể hiện của :c:type:`PyLongObject`, trước tiên hãy gọi hàm của nó
   :meth:`~object.__index__` (nếu có) để chuyển đổi nó thành một
   :c:type:`PyLongObject`.

   * Nếu *obj* là số âm, hãy phát sinh một :exc:`ValueError`.
   * Nếu giá trị *obj* nằm ngoài phạm vi, hãy phát sinh một :exc:`OverflowError`.

   Đặt *\*value* và trả về ``0`` khi thành công. Đặt một exception và trả về ``-1`` khi có lỗi.

   *value* không được là ``NULL``.

   .. versionadded:: 3.14


.. c:function:: double PyLong_AsDouble(PyObject *pylong)

   Trả về biểu diễn C :c:expr:`double` của *pylong*.  *pylong* phải là một thể hiện của :c:type:`PyLongObject`.

   Phát sinh :exc:`OverflowError` nếu giá trị của *pylong* nằm ngoài phạm vi cho một
   :c:expr:`double`.

   Trả về ``-1.0`` khi xảy ra lỗi. Dùng :c:func:`PyErr_Occurred` để phân biệt.


.. c:function:: void* PyLong_AsVoidPtr(PyObject *pylong)

   Chuyển một số nguyên Python *pylong* thành một con trỏ C :c:expr:`void`. Nếu không thể chuyển đổi *pylong*, một :exc:`OverflowError` sẽ được phát sinh. Điều này chỉ được đảm bảo tạo ra một con trỏ :c:expr:`void` có thể sử dụng cho các giá trị được tạo bằng :c:func:`PyLong_FromVoidPtr`.

   Trả về ``NULL`` khi xảy ra lỗi. Dùng :c:func:`PyErr_Occurred` để phân biệt.


.. c:function:: Py_ssize_t PyLong_AsNativeBytes(PyObject *pylong, void* buffer, Py_ssize_t n_bytes, int flags)

   Sao chép giá trị số nguyên Python *pylong* vào *buffer* native có kích thước *n_bytes*. Có thể đặt *flags* thành ``-1`` để hoạt động tương tự như một phép ép kiểu C, hoặc thành các giá trị được nêu dưới đây để kiểm soát hành vi.

   Trả về ``-1`` và phát sinh ngoại lệ nếu có lỗi. Điều này có thể xảy ra nếu không thể diễn giải *pylong* thành một số nguyên, hoặc nếu *pylong* là số âm và ``Py_ASNATIVEBYTES_REJECT_NEGATIVE`` flag được đặt.

   Nếu không, trả về số byte cần thiết để lưu trữ giá trị. Nếu giá trị này nhỏ hơn hoặc bằng *n_bytes*, thì toàn bộ giá trị đã được sao chép. Tất cả *n_bytes* của buffer đều được ghi: các byte còn lại được điền bằng các bản sao của bit dấu.

   Nếu giá trị trả về lớn hơn *n_bytes*, giá trị đã bị cắt bớt: số bit thấp nhất của giá trị nhiều nhất có thể vừa với kích thước được ghi, còn các bit cao hơn bị bỏ qua. Điều này phù hợp với hành vi thông thường của phép downcast kiểu C.

   .. note::

      Tràn số không được xem là lỗi. Nếu giá trị trả về lớn hơn *n_bytes*, các bit có trọng số cao nhất đã bị loại bỏ.

   ``0`` sẽ không bao giờ được trả về.

   Các giá trị luôn được sao chép dưới dạng bù hai.

   Ví dụ sử dụng::

      int32_t value;
      Py_ssize_t bytes = PyLong_AsNativeBytes(pylong, &value, sizeof(value), -1);
      if (bytes < 0) {
          // Thất bại. Một ngoại lệ Python đã được thiết lập với lý do này.
          return NULL;
      }
      else if (bytes <= (Py_ssize_t)sizeof(value)) {
          // Thành công!
      }
      else {
          // Đã xảy ra tràn, nhưng 'value' chứa các bit thấp nhất đã bị cắt ngắn
          // của pylong.
      }

   Truyền giá trị bằng không cho *n_bytes* sẽ trả về kích thước của một buffer đủ lớn để chứa giá trị. Kích thước này có thể lớn hơn mức thực sự cần thiết về mặt kỹ thuật, nhưng không lớn một cách bất hợp lý. Nếu *n_bytes=0*, *buffer* có thể là ``NULL``.

   .. note::

      Truyền *n_bytes=0* cho hàm này không phải là cách chính xác để xác định độ dài bit của giá trị.

   Để lấy toàn bộ giá trị Python có kích thước chưa biết, có thể gọi hàm hai lần: lần đầu để xác định kích thước bộ đệm, sau đó để điền dữ liệu vào bộ đệm::

      // Hỏi xem chúng ta cần bao nhiêu không gian.
      Py_ssize_t expected = PyLong_AsNativeBytes(pylong, NULL, 0, -1);
      if (expected < 0) {
          // Thất bại. Một ngoại lệ Python đã được thiết lập với lý do này.
          return NULL;
      }
      assert(expected != 0);  // Không thể theo định nghĩa của API.
      uint8_t *bignum = malloc(expected);
      if (!bignum) {
          PyErr_SetString(PyExc_MemoryError, "bignum malloc failed.");
          return NULL;
      }
      // Lấy toàn bộ giá trị một cách an toàn.
      Py_ssize_t bytes = PyLong_AsNativeBytes(pylong, bignum, expected, -1);
      if (bytes < 0) {  // Ngoại lệ đã được thiết lập.
          free(bignum);
          return NULL;
      }
      else if (bytes > expected) {  // Điều này không thể xảy ra.
          PyErr_SetString(PyExc_RuntimeError,
              "Unexpected bignum truncation after a size check.");
          free(bignum);
          return NULL;
      }
      // Kết quả thành công dự kiến dựa trên bước kiểm tra trước ở trên.
      // ... sử dụng bignum ...
      free(bignum);

   *flags* có thể là ``-1`` (``Py_ASNATIVEBYTES_DEFAULTS``) để chọn các giá trị mặc định hoạt động giống một phép ép kiểu C nhất, hoặc là sự kết hợp của các cờ khác trong bảng dưới đây. Lưu ý rằng ``-1`` không thể kết hợp với các cờ khác.

   Hiện tại, ``-1`` tương ứng với ``Py_ASNATIVEBYTES_NATIVE_ENDIAN | Py_ASNATIVEBYTES_UNSIGNED_BUFFER``.

   .. c:namespace:: NULL

   +-----------------------------------------------+---------+
   | Cờ                                            | Giá trị |
   +===============================================+=========+
   | .. c:macro:: Py_ASNATIVEBYTES_DEFAULTS        | ``-1``  |
   +-----------------------------------------------+---------+
   | .. c:macro:: Py_ASNATIVEBYTES_BIG_ENDIAN      | ``0``   |
   +-----------------------------------------------+---------+
   | .. c:macro:: Py_ASNATIVEBYTES_LITTLE_ENDIAN   | ``1``   |
   +-----------------------------------------------+---------+
   | .. c:macro:: Py_ASNATIVEBYTES_NATIVE_ENDIAN   | ``3``   |
   +-----------------------------------------------+---------+
   | .. c:macro:: Py_ASNATIVEBYTES_UNSIGNED_BUFFER | ``4``   |
   +-----------------------------------------------+---------+
   | .. c:macro:: Py_ASNATIVEBYTES_REJECT_NEGATIVE | ``8``   |
   +-----------------------------------------------+---------+
   | .. c:macro:: Py_ASNATIVEBYTES_ALLOW_INDEX     | ``16``  |
   +-----------------------------------------------+---------+

   Việc chỉ định ``Py_ASNATIVEBYTES_NATIVE_ENDIAN`` sẽ ghi đè mọi cờ endian khác. Việc truyền ``2`` được dành riêng.

   Theo mặc định, sẽ yêu cầu đủ bộ đệm để bao gồm một bit dấu. Ví dụ, khi chuyển đổi 128 với *n_bytes=1*, hàm sẽ trả về 2 (hoặc nhiều hơn) để lưu trữ một bit dấu bằng không.

   Nếu chỉ định ``Py_ASNATIVEBYTES_UNSIGNED_BUFFER``, một bit dấu bằng không sẽ bị bỏ qua khi tính kích thước. Điều này cho phép, chẳng hạn, 128 vừa với bộ đệm một byte. Nếu bộ đệm đích sau đó được xử lý như một giá trị có dấu, một giá trị đầu vào dương có thể trở thành âm. Lưu ý rằng cờ này không ảnh hưởng đến việc xử lý các giá trị âm: đối với những giá trị đó, luôn yêu cầu khoảng trống cho một bit dấu.

   Việc chỉ định ``Py_ASNATIVEBYTES_REJECT_NEGATIVE`` khiến một ngoại lệ được thiết lập nếu *pylong* là số âm. Nếu không có cờ này, các giá trị âm sẽ được sao chép miễn là có đủ chỗ cho ít nhất một bit dấu, bất kể ``Py_ASNATIVEBYTES_UNSIGNED_BUFFER`` có được chỉ định hay không.

   Nếu chỉ định ``Py_ASNATIVEBYTES_ALLOW_INDEX`` và truyền vào một giá trị không phải số nguyên, phương thức :meth:`~object.__index__` của giá trị đó sẽ được gọi trước. Điều này có thể khiến mã Python được thực thi và cho phép các luồng khác chạy, từ đó có thể gây ra thay đổi đối với các đối tượng hoặc giá trị khác đang được sử dụng. Khi *flags* là ``-1``, tùy chọn này không được thiết lập và các giá trị không phải số nguyên sẽ gây ra lỗi
   :exc:`TypeError`.

   .. note::

      Với *flags* mặc định (``-1``, hoặc *UNSIGNED_BUFFER* mà không có *REJECT_NEGATIVE*), nhiều số nguyên Python có thể ánh xạ đến cùng một giá trị mà không bị tràn. Ví dụ, cả ``255`` và ``-1`` đều vừa với bộ đệm một byte và thiết lập tất cả các bit của bộ đệm. Điều này phù hợp với hành vi ép kiểu C thông thường.

   .. versionadded:: 3.13


.. c:macro:: PyLong_AsPid(pid)

   Macro để chuyển đổi một số nguyên Python thành mã định danh tiến trình.

   Có thể định nghĩa đây là bí danh cho :c:func:`PyLong_AsLong`,
   :c:func:`PyLong_FromLongLong`, hoặc :c:func:`PyLong_AsInt`, tùy thuộc vào kích thước của kiểu PID của hệ thống.

   .. versionadded:: 3.2


.. c:function:: int PyLong_GetSign(PyObject *obj, int *sign)

   Lấy dấu của đối tượng số nguyên *obj*.

   Khi thành công, đặt *\*sign* thành dấu của số nguyên (0, -1 hoặc +1 lần lượt cho số nguyên bằng không, âm hoặc dương) và trả về 0.

   Khi thất bại, trả về -1 và đặt một exception. Hàm này luôn thành công nếu *obj* là một :c:type:`PyLongObject` hoặc subtype của nó.

   .. versionadded:: 3.14


.. c:function:: int PyLong_IsPositive(PyObject *obj)

   Kiểm tra xem đối tượng số nguyên *obj* có dương (``obj > 0``) hay không.

   Nếu *obj* là một instance của :c:type:`PyLongObject` hoặc subtype của nó, trả về ``1`` khi nó dương và ``0`` trong trường hợp ngược lại. Nếu không, đặt một exception và trả về ``-1``.

   .. versionadded:: 3.14


.. c:function:: int PyLong_IsNegative(PyObject *obj)

   Kiểm tra xem đối tượng số nguyên *obj* có âm (``obj < 0``) hay không.

   Nếu *obj* là một instance của :c:type:`PyLongObject` hoặc subtype của nó, trả về ``1`` khi nó âm và ``0`` trong các trường hợp khác. Nếu không, đặt một exception và trả về ``-1``.

   .. versionadded:: 3.14


.. c:function:: int PyLong_IsZero(PyObject *obj)

   Kiểm tra xem integer object *obj* có bằng 0 hay không.

   Nếu *obj* là một instance của :c:type:`PyLongObject` hoặc subtype của nó, trả về ``1`` khi nó bằng 0 và ``0`` trong các trường hợp khác. Nếu không, đặt một exception và trả về ``-1``.

   .. versionadded:: 3.14


.. c:function:: PyObject* PyLong_GetInfo(void)

   Khi thành công, trả về một :term:`named tuple` chỉ đọc, chứa thông tin về biểu diễn nội bộ của các số nguyên trong Python. Xem :data:`sys.int_info` để biết mô tả về từng trường.

   Khi thất bại, trả về ``NULL`` cùng với một exception đã được đặt.

   .. versionadded:: 3.1


.. c:function:: int PyUnstable_Long_IsCompact(const PyLongObject* op)

   Trả về 1 nếu *op* là compact, nếu không thì trả về 0.

   Hàm này cho phép mã yêu cầu hiệu năng cao triển khai “fast path” cho các số nguyên nhỏ. Đối với các giá trị compact, hãy sử dụng
   :c:func:`PyUnstable_Long_CompactValue`; đối với các trường hợp khác, chuyển sang một
   :c:func:`PyLong_As* <PyLong_AsSize_t>` hàm hoặc
   :c:func:`PyLong_AsNativeBytes`.

   Đối với hầu hết người dùng, mức tăng tốc dự kiến là không đáng kể.

   Chính xác những giá trị nào được xem là compact là một chi tiết triển khai và có thể thay đổi.

   .. versionadded:: 3.12


.. c:function:: Py_ssize_t PyUnstable_Long_CompactValue(const PyLongObject* op)

   Nếu *op* là compact, như được xác định bởi :c:func:`PyUnstable_Long_IsCompact`, hãy trả về giá trị của nó.

   Nếu không, giá trị trả về không được xác định.

   .. versionadded:: 3.12


API xuất
^^^^^^^^

.. versionadded:: 3.14

.. c:struct:: PyLongLayout

   Bố cục của một mảng gồm các "digit" ("limb" theo thuật ngữ của GMP), được dùng để biểu diễn giá trị tuyệt đối của các số nguyên có độ chính xác tùy ý.

   Sử dụng :c:func:`PyLong_GetNativeLayout` để lấy bố cục gốc của Python
   Các đối tượng :class:`int`, được sử dụng nội bộ cho các số nguyên có giá trị tuyệt đối "đủ lớn".

   Xem thêm :data:`sys.int_info`, cung cấp thông tin tương tự trong Python.

   .. c:member:: uint8_t bits_per_digit

      Số bit trên mỗi digit. Ví dụ, digit 15 bit có nghĩa là các bit 0-14 chứa thông tin có ý nghĩa.

   .. c:member:: uint8_t digit_size

      Kích thước của digit tính bằng byte. Ví dụ, digit 15 bit sẽ cần ít nhất 2 byte.

   .. c:member:: int8_t digits_order

      Thứ tự các digit:

      - ``1`` cho thứ tự chữ số quan trọng nhất trước
      - ``-1`` cho thứ tự chữ số ít quan trọng nhất trước

   .. c:member:: int8_t digit_endianness

      Thứ tự byte của chữ số:

      - ``1`` cho thứ tự byte quan trọng nhất trước (big endian)
      - ``-1`` cho thứ tự byte ít quan trọng nhất trước (little endian)


.. c:function:: const PyLongLayout* PyLong_GetNativeLayout(void)

   Lấy bố cục gốc của các đối tượng Python :class:`int`.

   Xem cấu trúc :c:struct:`PyLongLayout`.

   Không được gọi hàm này trước khi Python được khởi tạo hoặc sau khi Python được hoàn tất. Bố cục được trả về hợp lệ cho đến khi Python được hoàn tất. Bố cục này giống nhau đối với tất cả các Python sub-interpreter trong một tiến trình, vì vậy có thể được lưu vào bộ nhớ đệm.


.. c:struct:: PyLongExport

   Xuất một đối tượng :class:`int` của Python.

   Có hai trường hợp:

   * Nếu :c:member:`digits` là ``NULL``, chỉ sử dụng thành viên :c:member:`value`.
   * Nếu :c:member:`digits` không phải là ``NULL``, sử dụng :c:member:`negative`,
     các thành viên :c:member:`ndigits` và :c:member:`digits`.

   .. c:member:: int64_t value

      Giá trị số nguyên gốc của đối tượng :class:`int` đã xuất. Chỉ hợp lệ nếu :c:member:`digits` là ``NULL``.

   .. c:member:: uint8_t negative

      ``1`` nếu số đó là số âm, ``0`` nếu không. Chỉ hợp lệ khi :c:member:`digits` không phải là ``NULL``.

   .. c:member:: Py_ssize_t ndigits

      Số chữ số trong mảng :c:member:`digits`. Chỉ hợp lệ khi :c:member:`digits` không phải là ``NULL``.

   .. c:member:: const void *digits

      Mảng chỉ đọc gồm các chữ số không dấu. Có thể là ``NULL``.


.. c:function:: int PyLong_Export(PyObject *obj, PyLongExport *export_long)

   Xuất một đối tượng :class:`int` của Python.

   *export_long* phải trỏ đến một cấu trúc :c:struct:`PyLongExport` do bên gọi cấp phát. Giá trị này không được là ``NULL``.

   Khi thành công, điền *\*export_long* và trả về ``0``. Khi xảy ra lỗi, đặt một exception và trả về ``-1``.

   Phải gọi :c:func:`PyLong_FreeExport` khi không còn cần đến export nữa.

    .. impl-detail::
        Hàm này luôn thành công nếu *obj* là một Python :class:`int` object hoặc một lớp con.


.. c:function:: void PyLong_FreeExport(PyLongExport *export_long)

   Giải phóng *export_long* export được tạo bởi :c:func:`PyLong_Export`.

   .. impl-detail::
      Việc gọi :c:func:`PyLong_FreeExport` là tùy chọn nếu *export_long->digits* là ``NULL``.


API PyLongWriter
^^^^^^^^^^^^^^^^

Có thể sử dụng API :c:type:`PyLongWriter` để import một số nguyên.

.. versionadded:: 3.14

.. c:struct:: PyLongWriter

   Một instance writer Python :class:`int`.

   Instance phải được hủy bởi :c:func:`PyLongWriter_Finish` hoặc
   :c:func:`PyLongWriter_Discard`.


.. c:function:: PyLongWriter* PyLongWriter_Create(int negative, Py_ssize_t ndigits, void **digits)

   Tạo một :c:type:`PyLongWriter`.

   Khi thành công, cấp phát *\*digits* rồi trả về một writer. Khi có lỗi, đặt một exception và trả về ``NULL``.

   *negative* là ``1`` nếu số đó âm, hoặc ``0`` nếu không.

   *ndigits* là số lượng chữ số trong mảng *digits*. Giá trị này phải lớn hơn 0.

   *digits* không được là NULL.

   Sau khi gọi hàm này thành công, bên gọi nên điền vào mảng chữ số *digits*, sau đó gọi :c:func:`PyLongWriter_Finish` để nhận một :class:`int` Python. Bố cục của *digits* được mô tả bởi :c:func:`PyLong_GetNativeLayout`.

   Các chữ số phải nằm trong phạm vi [``0``; ``(1 << bits_per_digit) - 1``] (trong đó :c:struct:`~PyLongLayout.bits_per_digit` là số bit trên mỗi chữ số). Mọi chữ số có trọng số cao nhất không được sử dụng phải được đặt thành ``0``.

   Ngoài ra, gọi :c:func:`PyLongWriter_Discard` để hủy instance writer mà không tạo đối tượng :class:`~int`.


.. c:function:: PyObject* PyLongWriter_Finish(PyLongWriter *writer)

   Hoàn tất một :c:type:`PyLongWriter` được tạo bởi :c:func:`PyLongWriter_Create`.

   Khi thành công, trả về một đối tượng Python :class:`int`. Khi xảy ra lỗi, thiết lập một exception và trả về ``NULL``.

   Hàm này đảm nhiệm việc chuẩn hóa các chữ số và chuyển đối tượng thành số nguyên compact nếu cần.

   Instance writer và mảng *digits* không còn hợp lệ sau lời gọi này.


.. c:function:: void PyLongWriter_Discard(PyLongWriter *writer)

   Hủy một :c:type:`PyLongWriter` được tạo bởi :c:func:`PyLongWriter_Create`.

   Nếu *writer* là ``NULL``, không thực hiện thao tác nào.

   Instance writer và mảng *digits* không còn hợp lệ sau lời gọi này.


API không còn được khuyến nghị
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Các macro này là :term:`soft deprecated`. Chúng mô tả các tham số của biểu diễn nội bộ của các thể hiện :c:type:`PyLongObject`.

Thay vào đó, hãy sử dụng :c:func:`PyLong_GetNativeLayout`, cùng với :c:func:`PyLong_Export` để đọc dữ liệu số nguyên hoặc :c:type:`PyLongWriter` để ghi dữ liệu đó. Hiện tại, các API này sử dụng cùng một bố cục, nhưng được thiết kế để tiếp tục hoạt động chính xác ngay cả khi biểu diễn số nguyên nội bộ của CPython thay đổi.


.. c:macro:: PyLong_SHIFT

   Điều này tương đương với :c:member:`~PyLongLayout.bits_per_digit` trong đầu ra của :c:func:`PyLong_GetNativeLayout`.


.. c:macro:: PyLong_BASE

   Hiện tại, điều này tương đương với :c:expr:`1 << PyLong_SHIFT`.


.. c:macro:: PyLong_MASK

   Hiện tại, điều này tương đương với :c:expr:`(1 << PyLong_SHIFT) - 1`
