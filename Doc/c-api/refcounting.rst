.. highlight:: c


.. _countingrefs:

**************
Đếm tham chiếu
**************

Các hàm và macro trong phần này được dùng để quản lý số lượng tham chiếu của các đối tượng Python.


.. c:function:: Py_ssize_t Py_REFCNT(PyObject *o)

   Lấy số lượng tham chiếu của đối tượng Python *o*.

   Lưu ý rằng giá trị được trả về có thể không thực sự phản ánh số lượng tham chiếu đang được giữ tới đối tượng. Ví dụ, một số đối tượng là :term:`immortal` và có refcount rất cao, không phản ánh số lượng tham chiếu thực tế. Do đó, không nên dựa vào giá trị được trả về để cho là chính xác, ngoại trừ khi giá trị là 0 hoặc 1.

   Sử dụng hàm :c:func:`Py_SET_REFCNT()` để đặt số lượng tham chiếu của một đối tượng.

   .. note::

      Trên các bản build :term:`free-threaded builds <free-threaded build>` của Python, việc trả về 1 là chưa đủ để xác định liệu có an toàn khi coi *o* là không bị các thread khác truy cập hay không. Thay vào đó, hãy sử dụng :c:func:`PyUnstable_Object_IsUniquelyReferenced`.

      Xem thêm hàm :c:func:`PyUnstable_Object_IsUniqueReferencedTemporary()`.

   .. versionchanged:: 3.10
      :c:func:`Py_REFCNT()` is changed to the inline static function.

   .. versionchanged:: 3.11
      Kiểu tham số không còn là :c:expr:`const PyObject*` nữa.


.. c:function:: void Py_SET_REFCNT(PyObject *o, Py_ssize_t refcnt)

   Đặt bộ đếm tham chiếu của đối tượng *o* thành *refcnt*.

   Trong :ref:`bản dựng Python với Free Threading <free-threading-build>`, nếu *refcnt* lớn hơn ``UINT32_MAX``, đối tượng sẽ được đặt thành :term:`immortal`.

   Hàm này không có tác dụng với các đối tượng :term:`immortal`.

   .. versionadded:: 3.9

   .. versionchanged:: 3.12
      Các đối tượng bất tử không bị sửa đổi.


.. c:function:: void Py_INCREF(PyObject *o)

   Cho biết đang lấy một :term:`strong reference` mới đến đối tượng *o*, cho biết đối tượng đang được sử dụng và không nên bị hủy.

   Hàm này không có tác dụng với các đối tượng :term:`immortal`.

   Hàm này thường được dùng để chuyển một :term:`borrowed reference` thành một
   :term:`strong reference` tại chỗ. Có thể dùng hàm :c:func:`Py_NewRef` để tạo một :term:`strong reference` mới.

   Khi dùng xong đối tượng, hãy giải phóng đối tượng bằng cách gọi :c:func:`Py_DECREF`.

   Đối tượng không được ``NULL``; nếu bạn không chắc rằng đối tượng không ``NULL``, hãy sử dụng :c:func:`Py_XINCREF`.

   Đừng mong hàm này thực sự sửa đổi *o* theo bất kỳ cách nào. Ít nhất đối với :pep:`some objects <0683>`, hàm này không có tác dụng.

   .. versionchanged:: 3.12
      Các đối tượng bất tử không bị sửa đổi.


.. c:function:: void Py_XINCREF(PyObject *o)

   Tương tự :c:func:`Py_INCREF`, nhưng đối tượng *o* có thể được ``NULL``, trong trường hợp đó hàm này không có tác dụng.

   Xem thêm :c:func:`Py_XNewRef`.


.. c:function:: PyObject* Py_NewRef(PyObject *o)

   Tạo một :term:`strong reference` mới cho một đối tượng: gọi :c:func:`Py_INCREF` trên *o* và trả về đối tượng *o*.

   Khi không còn cần đến :term:`strong reference`, cần gọi :c:func:`Py_DECREF` trên nó để giải phóng tham chiếu.

   Đối tượng *o* không được ``NULL``; hãy sử dụng :c:func:`Py_XNewRef` nếu *o* có thể được ``NULL``.

   Ví dụ::

       Py_INCREF(obj);
       self->attr = obj;

   có thể được viết như sau::

       self->attr = Py_NewRef(obj);

   Xem thêm :c:func:`Py_INCREF`.

   .. versionadded:: 3.10


.. c:function:: PyObject* Py_XNewRef(PyObject *o)

   Tương tự như :c:func:`Py_NewRef`, nhưng đối tượng *o* có thể là NULL.

   Nếu đối tượng *o* là ``NULL``, hàm chỉ trả về ``NULL``.

   .. versionadded:: 3.10


.. c:function:: void Py_DECREF(PyObject *o)

   Giải phóng một :term:`strong reference` tới đối tượng *o*, cho biết rằng tham chiếu đó không còn được sử dụng.

   Hàm này không có tác dụng với các đối tượng :term:`immortal`.

   Khi :term:`strong reference` cuối cùng được giải phóng (tức là số lượng tham chiếu của đối tượng giảm xuống 0), hàm giải phóng của kiểu đối tượng (không được là ``NULL``) sẽ được gọi.

   Hàm này thường được dùng để xóa một :term:`strong reference` trước khi thoát khỏi phạm vi của nó.

   Đối tượng không được là ``NULL``; nếu bạn không chắc chắn rằng nó không phải là ``NULL``, hãy sử dụng :c:func:`Py_XDECREF`.

   Đừng mong hàm này thực sự sửa đổi *o* theo bất kỳ cách nào. Ít nhất đối với :pep:`some objects <683>`, hàm này không có tác dụng.

   .. warning::

      Hàm giải phóng có thể khiến mã Python tùy ý được gọi (ví dụ: khi một thực thể lớp có phương thức :meth:`~object.__del__` được giải phóng). Mặc dù các ngoại lệ trong mã đó không được truyền lên, mã được thực thi vẫn có toàn quyền truy cập vào tất cả các biến toàn cục của Python. Điều này có nghĩa là mọi đối tượng có thể truy cập từ một biến toàn cục phải ở trạng thái nhất quán trước khi gọi :c:func:`Py_DECREF`. Ví dụ, mã để xóa một đối tượng khỏi danh sách cần sao chép một tham chiếu đến đối tượng bị xóa vào một biến tạm thời, cập nhật cấu trúc dữ liệu danh sách, rồi gọi :c:func:`Py_DECREF` cho biến tạm thời.

   .. versionchanged:: 3.12
      Các đối tượng bất tử không bị sửa đổi.


.. c:function:: void Py_XDECREF(PyObject *o)

   Tương tự như :c:func:`Py_DECREF`, nhưng đối tượng *o* có thể là ``NULL``, trong trường hợp đó thao tác này không có tác dụng. Cảnh báo tương tự từ :c:func:`Py_DECREF` cũng áp dụng ở đây.


.. c:function:: void Py_CLEAR(PyObject *o)

   Giải phóng một :term:`strong reference` cho đối tượng *o*. Đối tượng có thể là ``NULL``, trong trường hợp đó macro không có tác dụng; nếu không, tác dụng cũng giống như
   :c:func:`Py_DECREF`, ngoại trừ việc đối số cũng được đặt thành ``NULL``. Cảnh báo đối với :c:func:`Py_DECREF` không áp dụng cho đối tượng được truyền vào, vì macro sử dụng cẩn thận một biến tạm thời và đặt đối số thành ``NULL`` trước khi giải phóng tham chiếu.

   Bạn nên sử dụng macro này mỗi khi giải phóng một tham chiếu đến đối tượng có thể được duyệt trong quá trình thu gom rác.

   .. versionchanged:: 3.12
      Đối số macro giờ đây chỉ được đánh giá một lần. Nếu đối số có side effect, các side effect này sẽ không còn bị nhân đôi.


.. c:function:: void Py_IncRef(PyObject *o)

   Cho biết việc lấy một :term:`strong reference` tham chiếu mới đến đối tượng *o*. Một phiên bản hàm của :c:func:`Py_XINCREF`. Có thể dùng để nhúng Python động trong runtime.


.. c:function:: void Py_DecRef(PyObject *o)

   Giải phóng một :term:`strong reference` tham chiếu đến đối tượng *o*. Một phiên bản hàm của :c:func:`Py_XDECREF`. Có thể dùng để nhúng Python động trong runtime.


.. c:macro:: Py_SETREF(dst, src)

   Macro giải phóng an toàn một :term:`strong reference` tham chiếu đến đối tượng *dst* và đặt *dst* thành *src*.

   Như trong trường hợp của :c:func:`Py_CLEAR`, đoạn mã "hiển nhiên" có thể gây hậu quả nghiêm trọng::

       Py_DECREF(dst);
       dst = src;

   Cách an toàn là::

        Py_SETREF(dst, src);

   Cách này đảm bảo đặt *dst* thành *src* *trước* khi giải phóng tham chiếu đến giá trị cũ của *dst*, để mọi mã được kích hoạt do *dst* bị hủy không còn tin rằng *dst* trỏ đến một đối tượng hợp lệ.

   .. versionadded:: 3.6

   .. versionchanged:: 3.12
      Các đối số macro giờ đây chỉ được đánh giá một lần. Nếu một đối số có side effect, side effect đó sẽ không còn bị nhân đôi.


.. c:macro:: Py_XSETREF(dst, src)

   Biến thể của macro :c:macro:`Py_SETREF` sử dụng :c:func:`Py_XDECREF` thay vì :c:func:`Py_DECREF`.

   .. versionadded:: 3.6

   .. versionchanged:: 3.12
      Các đối số macro giờ đây chỉ được đánh giá một lần. Nếu một đối số có side effect, side effect đó sẽ không còn bị nhân đôi.
