.. highlight:: c

.. _slice-objects:

Đối tượng slice
---------------


.. c:var:: PyTypeObject PySlice_Type

   Đối tượng kiểu dành cho các đối tượng slice. Đây chính là :class:`slice` trong lớp Python.


.. c:function:: int PySlice_Check(PyObject *ob)

   Trả về true nếu *ob* là một đối tượng slice; *ob* không được là ``NULL``. Hàm này luôn thực thi thành công.


.. c:function:: PyObject* PySlice_New(PyObject *start, PyObject *stop, PyObject *step)

   Trả về một đối tượng slice mới với các giá trị đã cho. Các tham số *start*, *stop* và *step* được dùng làm giá trị cho các thuộc tính của đối tượng slice có cùng tên. Bất kỳ giá trị nào cũng có thể là ``NULL``, trong trường hợp đó ``None`` sẽ được dùng cho thuộc tính tương ứng.

   Trả về ``NULL`` với một ngoại lệ được thiết lập nếu không thể cấp phát đối tượng mới.


.. c:function:: int PySlice_GetIndices(PyObject *slice, Py_ssize_t length, Py_ssize_t *start, Py_ssize_t *stop, Py_ssize_t *step)

   Lấy các chỉ số start, stop và step từ đối tượng slice *slice*, với giả định một sequence có độ dài *length*. Xem các chỉ số lớn hơn *length* là lỗi.

   Trả về ``0`` khi thành công và ``-1`` khi có lỗi nhưng chưa thiết lập ngoại lệ (trừ khi một trong các chỉ số không phải là ``None`` và không thể được chuyển đổi thành số nguyên; khi đó ``-1`` được trả về cùng với một ngoại lệ được thiết lập).

   Có lẽ bạn không muốn sử dụng hàm này.

   .. versionchanged:: 3.2
      Kiểu tham số của tham số *slice* trước đây là ``PySliceObject*``.


.. c:function:: int PySlice_GetIndicesEx(PyObject *slice, Py_ssize_t length, Py_ssize_t *start, Py_ssize_t *stop, Py_ssize_t *step, Py_ssize_t *slicelength)

   Thay thế có thể sử dụng cho :c:func:`PySlice_GetIndices`. Lấy các chỉ số bắt đầu, kết thúc và bước từ đối tượng lát cắt *slice* với giả định một sequence có độ dài *length*, rồi lưu độ dài của lát cắt vào *slicelength*. Các chỉ số nằm ngoài phạm vi sẽ được giới hạn theo cách nhất quán với việc xử lý các lát cắt thông thường. *length* không được là số âm.

   Trả về ``0`` nếu thành công và ``-1`` nếu xảy ra lỗi kèm theo một exception được thiết lập.

   .. note::
      Hàm này được xem là không an toàn đối với các sequence có thể thay đổi kích thước. Lời gọi hàm này nên được thay thế bằng sự kết hợp của
      :c:func:`PySlice_Unpack` và :c:func:`PySlice_AdjustIndices` trong đó::

         if (PySlice_GetIndicesEx(slice, length, &start, &stop, &step, &slicelength) < 0) {
             // return error
         }

      được thay thế bằng::

         if (PySlice_Unpack(slice, &start, &stop, &step) < 0) {
             // return error
         }
         slicelength = PySlice_AdjustIndices(length, &start, &stop, step);

   .. versionchanged:: 3.2
      Kiểu tham số của tham số *slice* trước đây là ``PySliceObject*``.

   .. versionchanged:: 3.6.1
      Nếu ``Py_LIMITED_API`` không được thiết lập hoặc được thiết lập thành giá trị nằm giữa ``0x03050400`` và ``0x03060000`` (không bao gồm hai giá trị này), hoặc ``0x03060100`` trở lên
      :c:func:`!PySlice_GetIndicesEx` được triển khai dưới dạng một macro sử dụng
      :c:func:`!PySlice_Unpack` và :c:func:`!PySlice_AdjustIndices`. Các đối số *start*, *stop* và *step* được đánh giá nhiều hơn một lần.

   .. deprecated:: 3.6.1
      Nếu ``Py_LIMITED_API`` được thiết lập thành giá trị nhỏ hơn ``0x03050400`` hoặc nằm giữa ``0x03060000`` và ``0x03060100`` (không bao gồm hai giá trị này)
      :c:func:`!PySlice_GetIndicesEx` là một hàm đã lỗi thời.


.. c:function:: int PySlice_Unpack(PyObject *slice, Py_ssize_t *start, Py_ssize_t *stop, Py_ssize_t *step)

   Trích xuất các thành viên dữ liệu start, stop và step từ một đối tượng slice dưới dạng các số nguyên C. Âm thầm giảm các giá trị lớn hơn ``PY_SSIZE_T_MAX`` xuống ``PY_SSIZE_T_MAX``, âm thầm tăng các giá trị start và stop nhỏ hơn ``PY_SSIZE_T_MIN`` lên ``PY_SSIZE_T_MIN``, và âm thầm tăng các giá trị step nhỏ hơn ``-PY_SSIZE_T_MAX`` lên ``-PY_SSIZE_T_MAX``.

   Trả về ``-1`` khi có lỗi với một ngoại lệ được thiết lập, và ``0`` khi thành công.

   .. versionadded:: 3.6.1


.. c:function:: Py_ssize_t PySlice_AdjustIndices(Py_ssize_t length, Py_ssize_t *start, Py_ssize_t *stop, Py_ssize_t step)

   Điều chỉnh các chỉ số lát cắt start/end với giả định rằng chuỗi có độ dài được chỉ định. Các chỉ số nằm ngoài phạm vi được giới hạn theo cách nhất quán với việc xử lý các lát cắt thông thường.

   *length* không được âm. *step* không được bằng 0 và không được nhỏ hơn ``-PY_SSIZE_T_MAX``, như được đảm bảo bởi :c:func:`PySlice_Unpack`.

   Trả về độ dài của lát cắt. Luôn thành công. Không gọi mã Python.

   .. versionadded:: 3.6.1


Đối tượng Ellipsis
^^^^^^^^^^^^^^^^^^


.. c:var:: PyTypeObject PyEllipsis_Type

   Kiểu của đối tượng Python :const:`Ellipsis`. Giống :class:`types.EllipsisType` ở tầng Python.


.. c:var:: PyObject *Py_Ellipsis

   Đối tượng Python ``Ellipsis``. Đối tượng này không có phương thức nào. Giống như
   :c:data:`Py_None`, đây là một đối tượng singleton :term:`immortal`.

   .. versionchanged:: 3.12
      :c:data:`Py_Ellipsis` is immortal.
