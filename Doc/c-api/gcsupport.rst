.. highlight:: c

.. _supporting-cycle-detection:

Hỗ trợ thu gom rác tuần hoàn
============================

Việc Python hỗ trợ phát hiện và thu gom rác liên quan đến các tham chiếu vòng yêu cầu các kiểu đối tượng là "container" cho những đối tượng khác, vốn cũng có thể là container. Các kiểu không lưu tham chiếu đến đối tượng khác, hoặc chỉ lưu tham chiếu đến các kiểu nguyên tử (chẳng hạn như số hoặc chuỗi), không cần cung cấp bất kỳ hỗ trợ rõ ràng nào cho việc thu gom rác.

Để tạo một kiểu container, trường :c:member:`~PyTypeObject.tp_flags` của đối tượng kiểu phải bao gồm :c:macro:`Py_TPFLAGS_HAVE_GC` và cung cấp một triển khai cho
trình xử lý :c:member:`~PyTypeObject.tp_traverse`. Nếu các instance của kiểu này có thể thay đổi, một
triển khai :c:member:`~PyTypeObject.tp_clear` cũng phải được cung cấp.


:c:macro:`Py_TPFLAGS_HAVE_GC`
   Các đối tượng có kiểu với cờ này được thiết lập phải tuân theo các quy tắc được ghi lại tại đây. Để thuận tiện, các đối tượng này sẽ được gọi là đối tượng container.

Các constructor cho kiểu container phải tuân theo hai quy tắc:

#. Bộ nhớ cho đối tượng phải được cấp phát bằng :c:macro:`PyObject_GC_New` hoặc :c:macro:`PyObject_GC_NewVar`.

#. Sau khi tất cả các trường có thể chứa tham chiếu đến các container khác đã được khởi tạo, nó phải gọi :c:func:`PyObject_GC_Track`.

Tương tự, deallocator của đối tượng phải tuân theo một cặp quy tắc tương tự:

#. Trước khi các trường tham chiếu đến các container khác bị vô hiệu hóa,
   phải gọi :c:func:`PyObject_GC_UnTrack`.

#. Bộ nhớ của đối tượng phải được giải phóng bằng :c:func:`PyObject_GC_Del`.

   .. warning::
      Nếu một kiểu thêm Py_TPFLAGS_HAVE_GC, thì nó *phải* triển khai ít nhất một handler :c:member:`~PyTypeObject.tp_traverse` hoặc sử dụng rõ ràng một handler từ lớp con hoặc các lớp con của nó.

      Khi gọi :c:func:`PyType_Ready` hoặc một số API gián tiếp gọi nó như :c:func:`PyType_FromSpecWithBases` hoặc
      :c:func:`PyType_FromSpec`, interpreter sẽ tự động điền các trường
      :c:member:`~PyTypeObject.tp_flags`, :c:member:`~PyTypeObject.tp_traverse` và :c:member:`~PyTypeObject.tp_clear` nếu kiểu này kế thừa từ một class triển khai giao thức garbage collector và class con *không* bao gồm cờ :c:macro:`Py_TPFLAGS_HAVE_GC`.

.. c:macro:: PyObject_GC_New(TYPE, typeobj)

   Tương tự như :c:macro:`PyObject_New` nhưng dành cho các đối tượng container có
   cờ :c:macro:`Py_TPFLAGS_HAVE_GC` được thiết lập.

   Không gọi trực tiếp hàm này để cấp phát bộ nhớ cho một đối tượng; thay vào đó, hãy gọi
   slot :c:member:`~PyTypeObject.tp_alloc` của kiểu.

   Khi điền vào slot :c:member:`~PyTypeObject.tp_alloc` của một type,
   Nên ưu tiên :c:func:`PyType_GenericAlloc` hơn một hàm tùy chỉnh chỉ đơn giản gọi macro này.

   Bộ nhớ được cấp phát bởi macro này phải được giải phóng bằng
   :c:func:`PyObject_GC_Del` (thường được gọi thông qua slot
   :c:member:`~PyTypeObject.tp_free` của đối tượng).

   .. seealso::

      * :c:func:`PyObject_GC_Del`
      * :c:macro:`PyObject_New`
      * :c:func:`PyType_GenericAlloc`
      * :c:member:`~PyTypeObject.tp_alloc`


.. c:macro:: PyObject_GC_NewVar(TYPE, typeobj, size)

   Tương tự như :c:macro:`PyObject_NewVar` nhưng dành cho các đối tượng container có
   cờ :c:macro:`Py_TPFLAGS_HAVE_GC` được thiết lập.

   Không gọi trực tiếp hàm này để cấp phát bộ nhớ cho một đối tượng; thay vào đó, hãy gọi
   slot :c:member:`~PyTypeObject.tp_alloc` của kiểu.

   Khi điền vào slot :c:member:`~PyTypeObject.tp_alloc` của một type,
   Nên ưu tiên :c:func:`PyType_GenericAlloc` hơn một hàm tùy chỉnh chỉ đơn giản gọi macro này.

   Bộ nhớ được cấp phát bởi macro này phải được giải phóng bằng
   :c:func:`PyObject_GC_Del` (thường được gọi thông qua slot
   :c:member:`~PyTypeObject.tp_free` của đối tượng).

   .. seealso::

      * :c:func:`PyObject_GC_Del`
      * :c:macro:`PyObject_NewVar`
      * :c:func:`PyType_GenericAlloc`
      * :c:member:`~PyTypeObject.tp_alloc`


.. c:function:: PyObject* PyUnstable_Object_GC_NewWithExtraData(PyTypeObject *type, size_t extra_size)

   Tương tự như :c:macro:`PyObject_GC_New` nhưng cấp phát thêm *extra_size* byte ở cuối đối tượng (tại offset
   :c:member:`~PyTypeObject.tp_basicsize`). Bộ nhớ được cấp phát được khởi tạo bằng các số 0, ngoại trừ :c:type:`header đối tượng Python <PyObject>`.

   Dữ liệu bổ sung sẽ được giải phóng cùng với đối tượng, nhưng ngoài ra Python không quản lý dữ liệu này.

   Bộ nhớ được cấp phát bởi hàm này phải được giải phóng bằng
   :c:func:`PyObject_GC_Del` (thường được gọi thông qua slot
   :c:member:`~PyTypeObject.tp_free` của đối tượng).

   .. warning::
      Hàm này được đánh dấu là không ổn định vì cơ chế cuối cùng để dành chỗ cho dữ liệu bổ sung sau một instance vẫn chưa được quyết định. Để cấp phát một số lượng trường thay đổi, nên sử dụng
      :c:type:`PyVarObject` và :c:member:`~PyTypeObject.tp_itemsize` thay vào đó.

   .. versionadded:: 3.12


.. c:macro:: PyObject_GC_Resize(TYPE, op, newsize)

   Thay đổi kích thước một đối tượng được cấp phát bởi :c:macro:`PyObject_NewVar`. Trả về đối tượng đã được thay đổi kích thước thuộc kiểu ``TYPE*`` (tham chiếu đến bất kỳ kiểu C nào) hoặc ``NULL`` nếu thất bại.

   *op* phải thuộc kiểu :c:expr:`PyVarObject *` và chưa được collector theo dõi. *newsize* phải thuộc kiểu :c:type:`Py_ssize_t`.


.. c:function:: void PyObject_GC_Track(PyObject *op)

   Thêm đối tượng *op* vào tập hợp các đối tượng container được collector theo dõi. Collector có thể chạy vào những thời điểm không thể dự đoán, vì vậy các đối tượng phải hợp lệ trong khi được theo dõi. Hàm này nên được gọi sau khi tất cả các trường được handler :c:member:`~PyTypeObject.tp_traverse` truy cập đã trở nên hợp lệ, thường là gần cuối constructor.


.. c:function:: int PyObject_IS_GC(PyObject *obj)

   Trả về giá trị khác 0 nếu đối tượng triển khai giao thức garbage collector, ngược lại trả về 0.

   Đối tượng không thể được garbage collector theo dõi nếu hàm này trả về 0.


.. c:function:: int PyObject_GC_IsTracked(PyObject *op)

   Trả về 1 nếu kiểu đối tượng của *op* triển khai giao thức GC và *op* hiện đang được garbage collector theo dõi, ngược lại trả về 0.

   Điều này tương tự như hàm Python :func:`gc.is_tracked`.

   .. versionadded:: 3.9


.. c:function:: int PyObject_GC_IsFinalized(PyObject *op)

   Trả về 1 nếu kiểu đối tượng của *op* triển khai giao thức GC và *op* đã được garbage collector hoàn tất, ngược lại trả về 0.

   Điều này tương tự như hàm Python :func:`gc.is_finalized`.

   .. versionadded:: 3.9


.. c:function:: void PyObject_GC_Del(void *op)

   Giải phóng bộ nhớ được cấp phát cho một đối tượng bằng :c:macro:`PyObject_GC_New` hoặc
   :c:macro:`PyObject_GC_NewVar`.

   Không gọi trực tiếp hàm này để giải phóng bộ nhớ của một đối tượng; thay vào đó, hãy gọi
   :c:member:`~PyTypeObject.tp_free` slot của kiểu.

   Không sử dụng hàm này cho bộ nhớ được cấp phát bởi :c:macro:`PyObject_New`,
   :c:macro:`PyObject_NewVar`, hoặc các hàm cấp phát liên quan; hãy sử dụng
   :c:func:`PyObject_Free` thay vào đó.

   .. seealso::

      * :c:func:`PyObject_Free` là phiên bản tương đương không dùng GC của hàm này.
      * :c:macro:`PyObject_GC_New`
      * :c:macro:`PyObject_GC_NewVar`
      * :c:func:`PyType_GenericAlloc`
      * :c:member:`~PyTypeObject.tp_free`


.. c:function:: void PyObject_GC_UnTrack(void *op)

   Xóa đối tượng *op* khỏi tập hợp các đối tượng chứa được bộ thu gom theo dõi. Lưu ý rằng có thể gọi lại :c:func:`PyObject_GC_Track` trên đối tượng này để thêm đối tượng trở lại tập hợp các đối tượng được theo dõi. Bộ giải phóng (:c:member:`~PyTypeObject.tp_dealloc` handler) nên gọi hàm này cho đối tượng trước khi bất kỳ trường nào được :c:member:`~PyTypeObject.tp_traverse` handler sử dụng trở nên không hợp lệ.


.. versionchanged:: 3.8

   Các macro :c:func:`!_PyObject_GC_TRACK` và :c:func:`!_PyObject_GC_UNTRACK` đã bị xóa khỏi public C API.

:c:member:`~PyTypeObject.tp_traverse` handler nhận một tham số hàm thuộc kiểu này:


.. c:type:: int (*visitproc)(PyObject *object, void *arg)

   Kiểu của hàm visitor được truyền cho :c:member:`~PyTypeObject.tp_traverse` handler. Hàm này phải được gọi với đối tượng cần duyệt làm *object* và tham số thứ ba của :c:member:`~PyTypeObject.tp_traverse` handler làm *arg*. Python core sử dụng một số hàm visitor để triển khai việc phát hiện garbage tuần hoàn; người dùng thường không cần tự viết các hàm visitor này.

Handler :c:member:`~PyTypeObject.tp_traverse` phải có kiểu sau:


.. c:type:: int (*traverseproc)(PyObject *self, visitproc visit, void *arg)

   Hàm duyệt dành cho một đối tượng container. Các triển khai phải gọi hàm *visit* cho từng đối tượng được chứa trực tiếp bởi *self*, trong đó các tham số truyền cho *visit* là đối tượng được chứa và giá trị *arg* được truyền cho handler. Không được gọi hàm *visit* với đối số là một đối tượng ``NULL``. Nếu *visit* trả về một giá trị khác không, phải trả về ngay giá trị đó.

   Hàm duyệt không được có bất kỳ side effect nào. Các triển khai không được sửa đổi reference count của bất kỳ đối tượng Python nào, cũng như không được tạo hoặc hủy bất kỳ đối tượng Python nào.

Để đơn giản hóa việc viết các handler :c:member:`~PyTypeObject.tp_traverse`, một macro :c:func:`Py_VISIT` được cung cấp. Để sử dụng macro này, triển khai :c:member:`~PyTypeObject.tp_traverse` phải đặt tên chính xác cho các đối số của nó là *visit* và *arg*:


.. c:macro:: Py_VISIT(o)

   Nếu :c:expr:`PyObject *` *o* không phải là ``NULL``, hãy gọi callback *visit*, với các đối số *o* và *arg*. Nếu *visit* trả về một giá trị khác không, hãy trả về giá trị đó. Khi sử dụng macro này, các handler :c:member:`~PyTypeObject.tp_traverse` có dạng như sau::

      static int
      my_traverse(Noddy *self, visitproc visit, void *arg)
      {
          Py_VISIT(self->foo);
          Py_VISIT(self->bar);
          return 0;
      }

Handler :c:member:`~PyTypeObject.tp_clear` phải thuộc kiểu :c:type:`inquiry`, hoặc ``NULL`` nếu đối tượng là immutable.


.. c:type:: int (*inquiry)(PyObject *self)

   Loại bỏ các tham chiếu có thể đã tạo ra reference cycle. Các đối tượng immutable không cần định nghĩa phương thức này vì chúng không thể trực tiếp tạo reference cycle. Lưu ý rằng đối tượng vẫn phải hợp lệ sau khi gọi phương thức này (không chỉ gọi :c:func:`Py_DECREF` trên một tham chiếu). Collector sẽ gọi phương thức này nếu phát hiện đối tượng đang tham gia vào một reference cycle.


Điều khiển trạng thái Garbage Collector
---------------------------------------

C-API cung cấp các hàm sau để điều khiển các lần chạy garbage collection.

.. c:function:: Py_ssize_t PyGC_Collect(void)

   Thực hiện garbage collection toàn phần nếu garbage collector được bật. (Lưu ý rằng :func:`gc.collect` luôn thực hiện việc này.)

   Trả về số đối tượng đã được thu gom cộng với số đối tượng không thể truy cập mà không thể thu gom. Nếu garbage collector bị tắt hoặc đang thu gom, trả về ``0`` ngay lập tức. Các lỗi trong quá trình garbage collection được truyền đến :data:`sys.unraisablehook`. Hàm này không phát sinh ngoại lệ.


.. c:function:: int PyGC_Enable(void)

   Bật garbage collector: tương tự như :func:`gc.enable`. Trả về trạng thái trước đó, 0 nếu bị tắt và 1 nếu được bật.

   .. versionadded:: 3.10


.. c:function:: int PyGC_Disable(void)

   Tắt garbage collector: tương tự như :func:`gc.disable`. Trả về trạng thái trước đó, 0 nếu bị tắt và 1 nếu được bật.

   .. versionadded:: 3.10


.. c:function:: int PyGC_IsEnabled(void)

   Truy vấn trạng thái của garbage collector: tương tự như :func:`gc.isenabled`. Trả về trạng thái hiện tại, 0 nếu bị tắt và 1 nếu được bật.

   .. versionadded:: 3.10


Truy vấn trạng thái Bộ thu gom rác
----------------------------------

C-API cung cấp giao diện sau để truy vấn thông tin về bộ thu gom rác.

.. c:function:: void PyUnstable_GC_VisitObjects(gcvisitobjects_t callback, void *arg)

   Chạy *callback* được cung cấp trên tất cả các đối tượng còn tồn tại có khả năng được GC. *arg* được truyền qua cho tất cả các lần gọi *callback*.

   .. warning::
      Nếu các đối tượng mới được cấp phát hoặc giải phóng bởi callback, việc chúng có được truy cập hay không là không xác định.

      Bộ thu gom rác bị vô hiệu hóa trong quá trình hoạt động. Việc chạy tường minh một lần thu gom trong callback có thể dẫn đến hành vi không xác định, chẳng hạn như truy cập cùng một đối tượng nhiều lần hoặc hoàn toàn không truy cập đối tượng đó.

   .. versionadded:: 3.12

.. c:type:: int (*gcvisitobjects_t)(PyObject *object, void *arg)

   Kiểu của hàm visitor được truyền vào :c:func:`PyUnstable_GC_VisitObjects`. *arg* giống với *arg* được truyền vào ``PyUnstable_GC_VisitObjects``. Trả về ``1`` để tiếp tục lặp, trả về ``0`` để dừng lặp. Hiện tại, các giá trị trả về khác được dành riêng, vì vậy hành vi khi trả về bất kỳ giá trị nào khác là không xác định.

   .. versionadded:: 3.12


