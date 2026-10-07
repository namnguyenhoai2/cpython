.. highlight:: c

.. _apiabiversion:

********************
Phiên bản API và ABI
********************


Hằng số phiên bản tại thời điểm build
-------------------------------------

CPython cung cấp số phiên bản trong các macro sau. Lưu ý rằng các macro này tương ứng với mã phiên bản được **build** cùng. Xem :c:var:`Py_Version` để biết phiên bản được sử dụng tại **run time**.

Xem :ref:`stable` để tìm hiểu về tính ổn định của API và ABI giữa các phiên bản.

.. c:macro:: PY_MAJOR_VERSION

   ``3`` trong ``3.4.1a2``.

.. c:macro:: PY_MINOR_VERSION

   ``4`` trong ``3.4.1a2``.

.. c:macro:: PY_MICRO_VERSION

   ``1`` trong ``3.4.1a2``.

.. c:macro:: PY_RELEASE_LEVEL

   ``3.4.1a2`` chứa ``a``. Giá trị này có thể là ``0xA`` cho alpha, ``0xB`` cho beta, ``0xC`` cho bản phát hành candidate hoặc ``0xF`` cho bản chính thức.

.. c:macro:: PY_RELEASE_SERIAL

   ``3.4.1a2`` chứa ``2``. Bằng 0 đối với các bản phát hành chính thức.

.. c:macro:: PY_VERSION_HEX

   Số phiên bản Python được mã hóa trong một số nguyên duy nhất. Xem :c:func:`Py_PACK_FULL_VERSION` để biết chi tiết về cách mã hóa.

   Sử dụng giá trị này để so sánh số, ví dụ: ``#if PY_VERSION_HEX >= ...``.

Các macro này được định nghĩa trong :source:`Include/patchlevel.h`.


Phiên bản runtime
-----------------

.. c:var:: const unsigned long Py_Version

   Số phiên bản runtime của Python được mã hóa trong một hằng số nguyên duy nhất. Xem :c:func:`Py_PACK_FULL_VERSION` để biết chi tiết về cách mã hóa. Giá trị này chứa phiên bản Python được sử dụng trong thời gian chạy.

   Dùng nội dung này để so sánh số, ví dụ: ``if (Py_Version >= ...)``.

   .. versionadded:: 3.11


Macro đóng gói bit
------------------

.. c:function:: uint32_t Py_PACK_FULL_VERSION(int major, int minor, int micro, int release_level, int release_serial)

   Trả về phiên bản đã cho, được mã hóa thành một số nguyên 32-bit duy nhất với cấu trúc sau:

   +------------------+-------+----------------+-----------+--------------------------+
   |                  | No.   |                |           | Example values           |
   |                  | of    |                |           +-------------+------------+
   | Argument         | bits  | Bit mask       | Bit shift | ``3.4.1a2`` | ``3.10.0`` |
   +==================+=======+================+===========+=============+============+
   | *major*          |   8   | ``0xFF000000`` | 24        | ``0x03``    | ``0x03``   |
   +------------------+-------+----------------+-----------+-------------+------------+
   | *minor*          |   8   | ``0x00FF0000`` | 16        | ``0x04``    | ``0x0A``   |
   +------------------+-------+----------------+-----------+-------------+------------+
   | *micro*          |   8   | ``0x0000FF00`` | 8         | ``0x01``    | ``0x00``   |
   +------------------+-------+----------------+-----------+-------------+------------+
   | *release_level*  |   4   | ``0x000000F0`` | 4         | ``0xA``     | ``0xF``    |
   +------------------+-------+----------------+-----------+-------------+------------+
   | *release_serial* |   4   | ``0x0000000F`` | 0         | ``0x2``     | ``0x0``    |
   +------------------+-------+----------------+-----------+-------------+------------+

   Ví dụ:

   +-------------+---------------------------------+-----------------------+
   | Phiên bản   | đối số ``Py_PACK_FULL_VERSION`` | Phiên bản được mã hóa |
   +=============+=================================+=======================+
   | ``3.4.1a2`` | ``(3, 4, 1, 0xA, 2)``           | ``0x030401a2``        |
   +-------------+---------------------------------+-----------------------+
   | ``3.10.0``  | ``(3, 10, 0, 0xF, 0)``          | ``0x030a00f0``        |
   +-------------+---------------------------------+-----------------------+

   Các bit nằm ngoài phạm vi trong các đối số sẽ bị bỏ qua. Nghĩa là, macro có thể được định nghĩa như sau:

   .. code-block:: c

      #ifndef Py_PACK_FULL_VERSION
      #define Py_PACK_FULL_VERSION(X, Y, Z, LEVEL, SERIAL) ( \
         (((X) & 0xff) << 24) |                              \
         (((Y) & 0xff) << 16) |                              \
         (((Z) & 0xff) << 8) |                               \
         (((LEVEL) & 0xf) << 4) |                            \
         (((SERIAL) & 0xf) << 0))
      #endif

   ``Py_PACK_FULL_VERSION`` chủ yếu là một macro, được dùng trong các chỉ thị ``#if``, nhưng cũng có sẵn dưới dạng một hàm được export.

   .. versionadded:: 3.14

.. c:function:: uint32_t Py_PACK_VERSION(int major, int minor)

   Tương đương với ``Py_PACK_FULL_VERSION(major, minor, 0, 0, 0)``. Kết quả không tương ứng với bất kỳ bản phát hành Python nào, nhưng hữu ích khi so sánh số.

   .. versionadded:: 3.14
