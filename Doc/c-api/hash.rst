.. highlight:: c

API PyHash
----------

Xem thêm thành viên :c:member:`PyTypeObject.tp_hash` và :ref:`numeric-hash`.

.. c:type:: Py_hash_t

   Kiểu giá trị hash: số nguyên có dấu.

   .. versionadded:: 3.2


.. c:type:: Py_uhash_t

   Kiểu giá trị hash: số nguyên không dấu.

   .. versionadded:: 3.2


.. c:macro:: Py_HASH_ALGORITHM

   Một giá trị số cho biết thuật toán dùng để băm :class:`str`,
   :class:`bytes` và :class:`memoryview`.

   Tên thuật toán được cung cấp thông qua :data:`sys.hash_info.algorithm`.

   .. versionadded:: 3.4


.. c:macro:: Py_HASH_FNV
             Py_HASH_SIPHASH24 Py_HASH_SIPHASH13

   Các giá trị số để so sánh với :c:macro:`Py_HASH_ALGORITHM` nhằm xác định thuật toán nào được sử dụng để băm. Có thể cấu hình thuật toán băm thông qua tùy chọn :option:`--with-hash-algorithm` configure.

   .. versionadded:: 3.4
      Thêm :c:macro:`!Py_HASH_FNV` và :c:macro:`!Py_HASH_SIPHASH24`.

   .. versionadded:: 3.11
      Thêm :c:macro:`!Py_HASH_SIPHASH13`.


.. c:macro:: Py_HASH_CUTOFF

   Các buffer có độ dài trong phạm vi ``[1, Py_HASH_CUTOFF)`` được băm bằng DJBX33A thay vì thuật toán được mô tả bởi :c:macro:`Py_HASH_ALGORITHM`.

   - Giá trị :c:macro:`!Py_HASH_CUTOFF` bằng 0 sẽ tắt tính năng tối ưu hóa.
   - :c:macro:`!Py_HASH_CUTOFF` phải không âm và nhỏ hơn hoặc bằng 7.

   Các nền tảng 32-bit nên sử dụng ngưỡng nhỏ hơn các nền tảng 64-bit vì việc tạo các chuỗi xung đột dễ hơn. Ngưỡng 7 trên các nền tảng 64-bit và 5 trên các nền tảng 32-bit sẽ cung cấp một biên độ an toàn khá tốt.

   Điều này tương ứng với hằng số :data:`sys.hash_info.cutoff`.

   .. versionadded:: 3.4


.. c:macro:: PyHASH_MODULUS

   `Số nguyên tố Mersenne <https://en.wikipedia.org/wiki/Mersenne_prime>`_ ``P = 2**n -1``, được dùng cho lược đồ băm số.

   Điều này tương ứng với hằng số :data:`sys.hash_info.modulus`.

   .. versionadded:: 3.13


.. c:macro:: PyHASH_BITS

   Số mũ ``n`` của ``P`` trong :c:macro:`PyHASH_MODULUS`.

   .. versionadded:: 3.13


.. c:macro:: PyHASH_MULTIPLIER

   Bộ nhân số nguyên tố được sử dụng trong hash chuỗi và nhiều loại hash khác.

   .. versionadded:: 3.13


.. c:macro:: PyHASH_INF

   Giá trị hash được trả về cho một giá trị dương vô cực.

   Điều này tương ứng với hằng số :data:`sys.hash_info.inf`.

   .. versionadded:: 3.13


.. c:macro:: PyHASH_IMAG

   Hệ số nhân được sử dụng cho phần ảo của một số phức.

   Điều này tương ứng với hằng số :data:`sys.hash_info.imag`.

   .. versionadded:: 3.13


.. c:type:: PyHash_FuncDef

   Định nghĩa hàm băm được :c:func:`PyHash_GetFuncDef` sử dụng.

   .. c:member:: Py_hash_t (*const hash)(const void *, Py_ssize_t)

      Hàm băm.

   .. c:member:: const char *name

      Tên hàm băm (chuỗi được mã hóa UTF-8).

      Điều này tương ứng với hằng số :data:`sys.hash_info.algorithm`.

   .. c:member:: const int hash_bits

      Kích thước nội bộ của giá trị băm tính theo bit.

      Điều này tương ứng với hằng số :data:`sys.hash_info.hash_bits`.

   .. c:member:: const int seed_bits

      Kích thước của đầu vào seed tính theo bit.

      Điều này tương ứng với hằng số :data:`sys.hash_info.seed_bits`.

   .. versionadded:: 3.4


.. c:function:: PyHash_FuncDef* PyHash_GetFuncDef(void)

   Lấy định nghĩa của hàm băm.

   .. seealso::
      :pep:`456` "Secure and interchangeable hash algorithm".

   .. versionadded:: 3.4


.. c:function:: Py_hash_t Py_HashPointer(const void *ptr)

   Băm một giá trị con trỏ: xử lý giá trị con trỏ như một số nguyên (ép kiểu nội bộ thành ``uintptr_t``). Con trỏ không được tham chiếu đến.

   Hàm này không thể thất bại: nó không thể trả về ``-1``.

   .. versionadded:: 3.13


.. c:function:: Py_hash_t Py_HashBuffer(const void *ptr, Py_ssize_t len)

   Tính và trả về giá trị hash của một buffer gồm *len* byte bắt đầu tại địa chỉ *ptr*. Hash này được đảm bảo khớp với hash của
   :class:`bytes`, :class:`memoryview`, và các đối tượng dựng sẵn khác triển khai :ref:`buffer protocol <bufferobjects>`.

   Sử dụng hàm này để triển khai việc hashing cho các đối tượng bất biến mà
   :c:member:`~PyTypeObject.tp_richcompare` so sánh với buffer của một đối tượng khác.

   *len* phải lớn hơn hoặc bằng ``0``.

   Hàm này luôn thành công.

   .. versionadded:: 3.14


.. c:function:: Py_hash_t PyObject_GenericHash(PyObject *obj)

   Hàm hashing tổng quát được dùng để đặt vào slot ``tp_hash`` của đối tượng kiểu. Kết quả của hàm chỉ phụ thuộc vào identity của đối tượng.

   .. impl-detail::
      Trong CPython, điều này tương đương với :c:func:`Py_HashPointer`.

   .. versionadded:: 3.13

.. _`Mersenne prime`: https://en.wikipedia.org/wiki/Mersenne_prime
