.. highlight:: c

.. _new-types-topics:

********************************************
Định nghĩa các kiểu mở rộng: Các chủ đề khác
********************************************

.. _dnt-type-methods:

Phần này nhằm cung cấp cái nhìn tổng quan nhanh về các phương thức kiểu khác nhau mà bạn có thể triển khai và chức năng của chúng.

Đây là định nghĩa của :c:type:`PyTypeObject`, trong đó một số trường chỉ được sử dụng trong
:ref:`các bản build debug <debug-build>` được lược bỏ:

.. literalinclude:: ../includes/typestruct.h


Như bạn có thể thấy, có *rất nhiều* phương thức. Tuy vậy, đừng quá lo lắng -- nếu bạn có một kiểu muốn định nghĩa, rất có khả năng bạn sẽ chỉ triển khai một vài phương thức trong số này.

Như bạn có thể đã đoán, chúng ta sẽ xem xét phần này và cung cấp thêm thông tin về các handler khác nhau. Chúng ta sẽ không đi theo thứ tự chúng được định nghĩa trong cấu trúc, vì có rất nhiều yếu tố lịch sử ảnh hưởng đến thứ tự của các trường. Thường thì cách dễ nhất là tìm một ví dụ có các trường bạn cần, sau đó thay đổi các giá trị để phù hợp với kiểu mới của bạn.::

   const char *tp_name; /* Dùng để in */

Tên của kiểu -- như đã đề cập trong chương trước, tên này sẽ xuất hiện ở nhiều nơi, hầu như hoàn toàn nhằm mục đích chẩn đoán. Hãy cố gắng chọn một tên hữu ích trong những tình huống như vậy!::

   Py_ssize_t tp_basicsize, tp_itemsize; /* Dùng để cấp phát */

Các trường này cho runtime biết cần cấp phát bao nhiêu bộ nhớ khi các đối tượng thuộc kiểu này được tạo. Python có hỗ trợ tích hợp cho các cấu trúc có độ dài thay đổi (ví dụ: chuỗi, tuple), và đó là lý do trường :c:member:`~PyTypeObject.tp_itemsize` được sử dụng. Nội dung này sẽ được trình bày sau.::

   const char *tp_doc;

Tại đây, bạn có thể đặt một chuỗi (hoặc địa chỉ của chuỗi) mà bạn muốn trả về khi script Python tham chiếu đến ``obj.__doc__`` để lấy chuỗi tài liệu.

Bây giờ chúng ta chuyển sang các phương thức kiểu cơ bản -- những phương thức mà hầu hết các kiểu mở rộng sẽ triển khai.


Hoàn tất và giải phóng bộ nhớ
-----------------------------

.. index::
   single: object; deallocation
   single: deallocation, object
   single: object; finalization
   single: finalization, of objects

::

   destructor tp_dealloc;

Hàm này được gọi khi số lượng tham chiếu đến một instance của kiểu bạn giảm xuống bằng 0 và trình thông dịch Python muốn thu hồi nó. Nếu kiểu của bạn có bộ nhớ cần giải phóng hoặc cần thực hiện các thao tác dọn dẹp khác, bạn có thể đặt chúng tại đây. Bản thân đối tượng cũng cần được giải phóng tại đây. Sau đây là một ví dụ về hàm này::

   static void
   newdatatype_dealloc(PyObject *op)
   {
       newdatatypeobject *self = (newdatatypeobject *) op;
       free(self->obj_UnderlyingDatatypePtr);
       Py_TYPE(self)->tp_free(self);
   }

Nếu kiểu của bạn hỗ trợ garbage collection, hàm hủy nên gọi
:c:func:`PyObject_GC_UnTrack` trước khi xóa mọi trường thành viên::

   static void
   newdatatype_dealloc(PyObject *op)
   {
       newdatatypeobject *self = (newdatatypeobject *) op;
       PyObject_GC_UnTrack(op);
       Py_CLEAR(self->other_obj);
       ...
       Py_TYPE(self)->tp_free(self);
   }

.. index::
   single: PyErr_Fetch (C function)
   single: PyErr_Restore (C function)

Một yêu cầu quan trọng đối với hàm deallocator là không tác động đến bất kỳ exception nào đang chờ xử lý. Điều này rất quan trọng vì các deallocator thường được gọi khi interpreter unwinds ngăn xếp Python; khi ngăn xếp được unwind do một exception (thay vì các lệnh return thông thường), không có gì bảo vệ các deallocator khỏi việc thấy rằng một exception đã được thiết lập. Bất kỳ hành động nào mà deallocator thực hiện có thể khiến mã Python bổ sung được thực thi và phát hiện rằng một exception đã được thiết lập. Điều này có thể dẫn đến các lỗi gây hiểu nhầm từ interpreter. Cách đúng để bảo vệ là lưu exception đang chờ xử lý trước khi thực hiện hành động không an toàn, rồi khôi phục nó sau khi hoàn tất. Có thể thực hiện việc này bằng cách sử dụng :c:func:`PyErr_Fetch` và
:c:func:`PyErr_Restore` các hàm::

   static void
   my_dealloc(PyObject *obj)
   {
       MyObject *self = (MyObject *) obj;
       PyObject *cbresult;

       if (self->my_callback != NULL) {
           PyObject *err_type, *err_value, *err_traceback;

           /* Lưu trạng thái ngoại lệ hiện tại */
           PyErr_Fetch(&err_type, &err_value, &err_traceback);

           cbresult = PyObject_CallNoArgs(self->my_callback);
           if (cbresult == NULL) {
              PyErr_WriteUnraisable(self->my_callback);
           }
           else {
               Py_DECREF(cbresult);
           }

           /* Khôi phục trạng thái ngoại lệ đã lưu */
           PyErr_Restore(err_type, err_value, err_traceback);

           Py_DECREF(self->my_callback);
       }
       Py_TYPE(self)->tp_free(self);
   }

.. note::
   Có những giới hạn đối với những gì bạn có thể thực hiện một cách an toàn trong hàm deallocator. Trước hết, nếu kiểu của bạn hỗ trợ garbage collection (sử dụng :c:member:`~PyTypeObject.tp_traverse` và/hoặc :c:member:`~PyTypeObject.tp_clear`), một số thành viên của đối tượng có thể đã bị xóa hoặc finalized trước khi :c:member:`~PyTypeObject.tp_dealloc` được gọi. Thứ hai, trong
   :c:member:`~PyTypeObject.tp_dealloc`, đối tượng của bạn đang ở trạng thái không ổn định: reference count của nó bằng không. Bất kỳ lệnh gọi nào đến một đối tượng hoặc API không tầm thường (như trong ví dụ trên) cũng có thể lại gọi :c:member:`~PyTypeObject.tp_dealloc`, gây ra double free và crash.

   Bắt đầu từ Python 3.4, bạn được khuyến nghị không đặt bất kỳ mã finalization phức tạp nào trong :c:member:`~PyTypeObject.tp_dealloc`, mà thay vào đó hãy sử dụng kiểu method mới
   :c:member:`~PyTypeObject.tp_finalize`.

   .. seealso::
      :pep:`442` explains the new finalization scheme.

.. index::
   single: string; object representation
   pair: built-in function; repr

Trình bày đối tượng
-------------------

Trong Python, có hai cách để tạo biểu diễn dạng văn bản của một đối tượng: hàm :func:`repr` và hàm :func:`str`. (Hàm :func:`print` chỉ gọi :func:`str`.) Cả hai handler này đều là tùy chọn.

::

   reprfunc tp_repr;
   reprfunc tp_str;

Handler :c:member:`~PyTypeObject.tp_repr` sẽ trả về một đối tượng chuỗi chứa biểu diễn của instance mà nó được gọi cho. Đây là một ví dụ đơn giản::

   static PyObject *
   newdatatype_repr(PyObject *op)
   {
       newdatatypeobject *self = (newdatatypeobject *) op;
       return PyUnicode_FromFormat("Repr-ified_newdatatype{{size:%d}}",
                                   self->obj_UnderlyingDatatypePtr->size);
   }

Nếu không chỉ định handler :c:member:`~PyTypeObject.tp_repr`, interpreter sẽ cung cấp một biểu diễn sử dụng :c:member:`~PyTypeObject.tp_name` của kiểu và một giá trị nhận dạng duy nhất cho đối tượng.

Handler :c:member:`~PyTypeObject.tp_str` đối với :func:`str` cũng giống như handler :c:member:`~PyTypeObject.tp_repr` được mô tả ở trên đối với :func:`repr`; nghĩa là, nó được gọi khi mã Python gọi
:func:`str` trên một instance của đối tượng bạn. Cách triển khai của nó rất giống với hàm :c:member:`~PyTypeObject.tp_repr`, nhưng chuỗi kết quả được dành cho con người đọc. Nếu không chỉ định :c:member:`~PyTypeObject.tp_str`, handler :c:member:`~PyTypeObject.tp_repr` sẽ được sử dụng thay thế.

Đây là một ví dụ đơn giản::

   static PyObject *
   newdatatype_str(PyObject *op)
   {
       newdatatypeobject *self = (newdatatypeobject *) op;
       return PyUnicode_FromFormat("Stringified_newdatatype{{size:%d}}",
                                   self->obj_UnderlyingDatatypePtr->size);
   }



Quản lý thuộc tính
------------------

Đối với mọi đối tượng có thể hỗ trợ thuộc tính, kiểu tương ứng phải cung cấp các hàm kiểm soát cách các thuộc tính được phân giải. Cần có một hàm để truy xuất các thuộc tính (nếu có thuộc tính nào được định nghĩa) và một hàm khác để thiết lập thuộc tính (nếu cho phép thiết lập thuộc tính). Việc xóa một thuộc tính là trường hợp đặc biệt, trong đó giá trị mới được truyền cho handler là ``NULL``.

Python hỗ trợ hai cặp handler thuộc tính; một kiểu hỗ trợ thuộc tính chỉ cần triển khai các hàm cho một cặp. Điểm khác biệt là một cặp nhận tên thuộc tính dưới dạng :c:expr:`char\*`, còn cặp kia nhận một :c:expr:`PyObject*`. Mỗi kiểu có thể sử dụng cặp phù hợp hơn với sự thuận tiện khi triển khai.::

   getattrfunc  tp_getattr;        /* phiên bản dùng char * */
   setattrfunc  tp_setattr;
   /* ... */
   getattrofunc tp_getattro;       /* phiên bản dùng PyObject * */
   setattrofunc tp_setattro;

Nếu việc truy cập các thuộc tính của một đối tượng luôn là một thao tác đơn giản (điều này sẽ được giải thích ngay sau đây), có các triển khai tổng quát có thể được dùng để cung cấp phiên bản :c:expr:`PyObject*` của các hàm quản lý thuộc tính. Nhu cầu thực tế đối với các handler thuộc tính dành riêng cho từng kiểu gần như hoàn toàn biến mất kể từ Python 2.2, dù vẫn có nhiều ví dụ chưa được cập nhật để sử dụng một số cơ chế tổng quát mới hiện có.


.. _generic-attribute-management:

Quản lý thuộc tính tổng quát
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Hầu hết các kiểu mở rộng chỉ sử dụng các thuộc tính *đơn giản*. Vậy điều gì khiến các thuộc tính này đơn giản? Chỉ có một vài điều kiện cần đáp ứng:

#. Tên của các thuộc tính phải được biết khi :c:func:`PyType_Ready` được gọi.

#. Không cần xử lý đặc biệt để ghi nhận rằng một thuộc tính đã được tra cứu hoặc thiết lập, cũng không cần thực hiện hành động nào dựa trên giá trị đó.

Lưu ý rằng danh sách này không đặt ra bất kỳ hạn chế nào đối với giá trị của các thuộc tính, thời điểm tính toán các giá trị hoặc cách dữ liệu liên quan được lưu trữ.

Khi :c:func:`PyType_Ready` được gọi, nó sử dụng ba bảng được tham chiếu bởi đối tượng kiểu để tạo :term:`descriptor`\s, được đặt trong từ điển của đối tượng kiểu. Mỗi descriptor kiểm soát quyền truy cập vào một thuộc tính của đối tượng instance. Mỗi bảng đều là tùy chọn; nếu cả ba đều ``NULL``, các instance của kiểu này sẽ chỉ có những thuộc tính được kế thừa từ kiểu cơ sở và cũng nên để các trường :c:member:`~PyTypeObject.tp_getattro` và :c:member:`~PyTypeObject.tp_setattro` ở trạng thái ``NULL``, cho phép kiểu cơ sở xử lý các thuộc tính.

Các bảng được khai báo dưới dạng ba trường của đối tượng kiểu::

   struct PyMethodDef *tp_methods;
   struct PyMemberDef *tp_members;
   struct PyGetSetDef *tp_getset;

Nếu :c:member:`~PyTypeObject.tp_methods` không phải là ``NULL``, nó phải tham chiếu đến một mảng gồm
các cấu trúc :c:type:`PyMethodDef`. Mỗi mục trong bảng là một instance của cấu trúc này::

   typedef struct PyMethodDef {
       const char  *ml_name;       /* tên phương thức */
       PyCFunction  ml_meth;       /* hàm triển khai */
       int          ml_flags;      /* các cờ */
       const char  *ml_doc;        /* chuỗi tài liệu */
   } PyMethodDef;

Cần định nghĩa một mục cho mỗi phương thức do kiểu cung cấp; không cần mục nào cho các phương thức được kế thừa từ kiểu cơ sở. Cần thêm một mục ở cuối; đó là sentinel đánh dấu kết thúc mảng. Trường
:c:member:`~PyMethodDef.ml_name` của sentinel phải là ``NULL``.

Bảng thứ hai được dùng để định nghĩa các thuộc tính ánh xạ trực tiếp tới dữ liệu được lưu trong instance. Nhiều kiểu C nguyên thủy được hỗ trợ, và quyền truy cập có thể là chỉ đọc hoặc đọc-ghi. Các cấu trúc trong bảng được định nghĩa như sau::

   typedef struct PyMemberDef {
       const char *name;
       int         type;
       int         offset;
       int         flags;
       const char *doc;
   } PyMemberDef;

Đối với mỗi mục trong bảng, một :term:`descriptor` sẽ được tạo và thêm vào kiểu, cho phép trích xuất một giá trị từ cấu trúc instance. :term:`descriptor`
Trường :c:member:`~PyMemberDef.type` phải chứa một mã kiểu như :c:macro:`Py_T_INT` hoặc
:c:macro:`Py_T_DOUBLE`; giá trị này sẽ được dùng để xác định cách chuyển đổi các giá trị Python sang và từ các giá trị C. Trường :c:member:`~PyMemberDef.flags` được dùng để lưu các cờ kiểm soát cách truy cập thuộc tính: bạn có thể đặt trường này thành
:c:macro:`Py_READONLY` để ngăn mã Python thiết lập thuộc tính đó.

Một ưu điểm đáng chú ý của việc sử dụng bảng :c:member:`~PyTypeObject.tp_members` để xây dựng các descriptor được dùng trong runtime là bất kỳ thuộc tính nào được định nghĩa theo cách này cũng có thể có chuỗi tài liệu đi kèm, chỉ cần cung cấp văn bản trong bảng. Một ứng dụng có thể sử dụng API introspection để truy xuất descriptor từ đối tượng lớp và lấy chuỗi tài liệu bằng thuộc tính :attr:`~type.__doc__` của descriptor đó.

Cũng như với bảng :c:member:`~PyTypeObject.tp_methods`, cần có một mục sentinel với giá trị :c:member:`~PyMethodDef.ml_name` là ``NULL``.

.. XXX Descriptors need to be explained in more detail somewhere, but not here.

   Descriptor objects have two handler functions which correspond to the
   \member{tp_getattro} and \member{tp_setattro} handlers.  The
   \method{__get__()} handler is a function which is passed the descriptor,
   instance, and type objects, and returns the value of the attribute, or it
   returns \NULL{} and sets an exception.  The \method{__set__()} handler is
   passed the descriptor, instance, type, and new value;


Quản lý thuộc tính theo kiểu
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Để đơn giản, ở đây chỉ minh họa phiên bản :c:expr:`char\*`; kiểu của tham số name là điểm khác biệt duy nhất giữa hai biến thể :c:expr:`char\*` và :c:expr:`PyObject*` của giao diện. Ví dụ này thực hiện hiệu quả cùng một việc như ví dụ tổng quát ở trên, nhưng không sử dụng cơ chế hỗ trợ tổng quát được bổ sung trong Python 2.2. Ví dụ giải thích cách các hàm handler được gọi, để nếu cần mở rộng chức năng của chúng, bạn sẽ hiểu cần thực hiện những gì.

Handler :c:member:`~PyTypeObject.tp_getattr` được gọi khi đối tượng cần tra cứu thuộc tính. Nó được gọi trong cùng những tình huống mà phương thức :meth:`~object.__getattr__` của một class sẽ được gọi.

Sau đây là một ví dụ::

   static PyObject *
   newdatatype_getattr(PyObject *op, char *name)
   {
       newdatatypeobject *self = (newdatatypeobject *) op;
       if (strcmp(name, "data") == 0) {
           return PyLong_FromLong(self->data);
       }

       PyErr_Format(PyExc_AttributeError,
                    "'%.100s' object has no attribute '%.400s'",
                    Py_TYPE(self)->tp_name, name);
       return NULL;
   }

Handler :c:member:`~PyTypeObject.tp_setattr` được gọi khi phương thức :meth:`~object.__setattr__` hoặc
phương thức :meth:`~object.__delattr__` của một instance class được gọi. Khi một thuộc tính cần bị xóa, tham số thứ ba sẽ là ``NULL``. Sau đây là một ví dụ chỉ đơn giản là raise một exception; nếu đây thực sự là tất cả những gì bạn muốn, handler
:c:member:`~PyTypeObject.tp_setattr` nên được đặt thành ``NULL``.::

   static int
   newdatatype_setattr(PyObject *op, char *name, PyObject *v)
   {
       PyErr_Format(PyExc_RuntimeError, "Read-only attribute: %s", name);
       return -1;
   }

So sánh đối tượng
-----------------

::

   richcmpfunc tp_richcompare;

Bộ xử lý :c:member:`~PyTypeObject.tp_richcompare` được gọi khi cần thực hiện so sánh. Nó tương tự như các :ref:`phương thức so sánh mở rộng <richcmpfuncs>`, chẳng hạn như
:meth:`!__lt__`, và cũng được gọi bởi :c:func:`PyObject_RichCompare` và
:c:func:`PyObject_RichCompareBool`.

Hàm này được gọi với hai đối tượng Python và toán tử làm các đối số, trong đó toán tử là một trong các toán tử ``Py_EQ``, ``Py_NE``, ``Py_LE``, ``Py_GE``, ``Py_LT`` hoặc ``Py_GT``. Hàm này nên so sánh hai đối tượng theo toán tử được chỉ định và trả về ``Py_True`` hoặc ``Py_False`` nếu phép so sánh thành công, ``Py_NotImplemented`` để cho biết phép so sánh chưa được triển khai và nên thử phương thức so sánh của đối tượng còn lại, hoặc ``NULL`` nếu một ngoại lệ đã được thiết lập.

Sau đây là một cách triển khai mẫu cho một kiểu dữ liệu được xem là bằng nhau nếu kích thước của một con trỏ nội bộ bằng nhau::

   static PyObject *
   newdatatype_richcmp(PyObject *lhs, PyObject *rhs, int op)
   {
       newdatatypeobject *obj1 = (newdatatypeobject *) lhs;
       newdatatypeobject *obj2 = (newdatatypeobject *) rhs;
       PyObject *result;
       int c, size1, size2;

       /* lược bỏ mã bảo đảm cả hai đối số đều có kiểu
          newdatatype */

       size1 = obj1->obj_UnderlyingDatatypePtr->size;
       size2 = obj2->obj_UnderlyingDatatypePtr->size;

       switch (op) {
       case Py_LT: c = size1 <  size2; break;
       case Py_LE: c = size1 <= size2; break;
       case Py_EQ: c = size1 == size2; break;
       case Py_NE: c = size1 != size2; break;
       case Py_GT: c = size1 >  size2; break;
       case Py_GE: c = size1 >= size2; break;
       }
       result = c ? Py_True : Py_False;
       return Py_NewRef(result);
    }


Hỗ trợ giao thức trừu tượng
---------------------------

Python hỗ trợ nhiều *giao thức trừu tượng*; các giao diện cụ thể được cung cấp để sử dụng những giao diện này được ghi lại trong :ref:`abstract`.


Một số giao thức trừu tượng này đã được định nghĩa từ giai đoạn đầu phát triển bản triển khai Python. Cụ thể, các giao thức number, mapping và sequence đã là một phần của Python ngay từ đầu. Các giao thức khác được bổ sung theo thời gian. Đối với những giao thức phụ thuộc vào nhiều routine xử lý từ phần triển khai type, các giao thức cũ hơn được định nghĩa dưới dạng các khối handler tùy chọn được type object tham chiếu. Đối với các giao thức mới hơn, có thêm các slot trong type object chính, cùng với một bit cờ được đặt để cho biết rằng các slot này hiện diện và interpreter cần kiểm tra chúng. (Bit cờ không cho biết các giá trị slot có phải là ``NULL`` hay không. Cờ có thể được đặt để cho biết sự hiện diện của một slot, nhưng slot đó vẫn có thể chưa được điền.)::

   PyNumberMethods   *tp_as_number;
   PySequenceMethods *tp_as_sequence;
   PyMappingMethods  *tp_as_mapping;

Nếu muốn object của mình có thể hoạt động như một number, sequence hoặc mapping object, bạn đặt địa chỉ của một cấu trúc triển khai C type :c:type:`PyNumberMethods`, :c:type:`PySequenceMethods` hoặc
:c:type:`PyMappingMethods`, tương ứng. Bạn cần tự điền các giá trị thích hợp vào cấu trúc này. Bạn có thể tìm thấy các ví dụ về cách sử dụng từng cấu trúc trong thư mục :file:`Objects` của bản phân phối mã nguồn Python.::

   hashfunc tp_hash;

Nếu chọn cung cấp hàm này, hàm sẽ trả về một số hash cho một instance của data type. Sau đây là một ví dụ đơn giản::

   static Py_hash_t
   newdatatype_hash(PyObject *op)
   {
       newdatatypeobject *self = (newdatatypeobject *) op;
       Py_hash_t result;
       result = self->some_size + 32767 * self->some_number;
       if (result == -1) {
           result = -2;
       }
       return result;
   }

:c:type:`Py_hash_t` là một kiểu số nguyên có dấu với độ rộng thay đổi tùy theo nền tảng. Việc trả về ``-1`` từ :c:member:`~PyTypeObject.tp_hash` cho biết đã xảy ra lỗi, đó là lý do bạn cần cẩn thận để tránh trả về giá trị này khi việc tính hash thành công, như trong ví dụ trên.

::

   ternaryfunc tp_call;

Hàm này được gọi khi một instance của data type được "gọi", ví dụ: nếu ``obj1`` là một instance của data type của bạn và script Python chứa ``obj1('hello')``, handler :c:member:`~PyTypeObject.tp_call` sẽ được gọi.

Hàm này nhận ba đối số:

#. *self* là instance của kiểu dữ liệu đóng vai trò chủ thể của lời gọi. Nếu lời gọi là ``obj1('hello')``, thì *self* là ``obj1``.

#. *args* là một tuple chứa các đối số của lời gọi. Bạn có thể sử dụng
   :c:func:`PyArg_ParseTuple` để trích xuất các đối số.

#. *kwds* là một dictionary chứa các đối số keyword được truyền vào. Nếu giá trị này khác ``NULL`` và bạn hỗ trợ các đối số keyword, hãy sử dụng
   :c:func:`PyArg_ParseTupleAndKeywords` để trích xuất các đối số. Nếu bạn không muốn hỗ trợ các đối số keyword và giá trị này khác ``NULL``, hãy raise một
   :exc:`TypeError` với thông báo cho biết các đối số keyword không được hỗ trợ.

Sau đây là một triển khai ``tp_call`` đơn giản::

   static PyObject *
   newdatatype_call(PyObject *op, PyObject *args, PyObject *kwds)
   {
       newdatatypeobject *self = (newdatatypeobject *) op;
       PyObject *result;
       const char *arg1;
       const char *arg2;
       const char *arg3;

       if (!PyArg_ParseTuple(args, "sss:call", &arg1, &arg2, &arg3)) {
           return NULL;
       }
       result = PyUnicode_FromFormat(
           "Returning -- value: [%d] arg1: [%s] arg2: [%s] arg3: [%s]\n",
           self->obj_UnderlyingDatatypePtr->size,
           arg1, arg2, arg3);
       return result;
   }

::

   /* Các iterator */
   getiterfunc tp_iter;
   iternextfunc tp_iternext;

Các hàm này cung cấp hỗ trợ cho iterator protocol. Cả hai handler đều nhận chính xác một tham số, là instance mà chúng được gọi cho, và trả về một tham chiếu mới. Trong trường hợp xảy ra lỗi, chúng phải thiết lập một exception và trả về ``NULL``. :c:member:`~PyTypeObject.tp_iter` tương ứng với phương thức :meth:`~object.__iter__` của Python, còn :c:member:`~PyTypeObject.tp_iternext` tương ứng với phương thức :meth:`~iterator.__next__` của Python.

Mọi đối tượng :term:`iterable` đều phải triển khai handler :c:member:`~PyTypeObject.tp_iter`, handler này phải trả về một đối tượng :term:`iterator`. Ở đây, các hướng dẫn tương tự như đối với các class Python được áp dụng:

* Đối với các collection (chẳng hạn như list và tuple) có thể hỗ trợ nhiều iterator độc lập, mỗi lần gọi :c:member:`~PyTypeObject.tp_iter` nên tạo và trả về một iterator mới.
* Các đối tượng chỉ có thể được lặp qua một lần (thường là do các side effect của quá trình lặp, chẳng hạn như các đối tượng file) có thể triển khai :c:member:`~PyTypeObject.tp_iter` bằng cách trả về một tham chiếu mới đến chính chúng -- và do đó cũng nên triển khai handler :c:member:`~PyTypeObject.tp_iternext`.

Mọi đối tượng :term:`iterator` nên triển khai cả :c:member:`~PyTypeObject.tp_iter` và :c:member:`~PyTypeObject.tp_iternext`. Một iterator
handler :c:member:`~PyTypeObject.tp_iter` phải trả về một tham chiếu mới đến iterator. Handler :c:member:`~PyTypeObject.tp_iternext` của nó phải trả về một tham chiếu mới đến đối tượng tiếp theo trong quá trình lặp, nếu có. Nếu quá trình lặp đã đến cuối, :c:member:`~PyTypeObject.tp_iternext` có thể trả về ``NULL`` mà không thiết lập exception, hoặc có thể thiết lập
:exc:`StopIteration` *ngoài việc* trả về ``NULL``; việc tránh exception có thể mang lại hiệu năng tốt hơn một chút. Nếu xảy ra lỗi thực sự, :c:member:`~PyTypeObject.tp_iternext` luôn phải thiết lập một exception và trả về ``NULL``.


.. _weakref-support:

Hỗ trợ tham chiếu yếu
---------------------

Một trong những mục tiêu của việc triển khai tham chiếu yếu trong Python là cho phép mọi kiểu tham gia vào cơ chế tham chiếu yếu mà không làm phát sinh chi phí hiệu năng đối với các đối tượng quan trọng về hiệu năng (chẳng hạn như số).

.. seealso::
   Tài liệu về mô-đun :mod:`weakref`.

Để một đối tượng có thể được tham chiếu yếu, kiểu mở rộng phải đặt bit ``Py_TPFLAGS_MANAGED_WEAKREF`` của trường :c:member:`~PyTypeObject.tp_flags`. Trường :c:member:`~PyTypeObject.tp_weaklistoffset` kiểu cũ nên được để ở giá trị zero.

Cụ thể, đối tượng kiểu được khai báo tĩnh sẽ có dạng như sau::

   static PyTypeObject TrivialType = {
       PyVarObject_HEAD_INIT(NULL, 0)
       /* ... lược bỏ các thành viên khác cho ngắn gọn ... */
       .tp_flags = Py_TPFLAGS_MANAGED_WEAKREF | ...,
   };


Bổ sung duy nhất cần thực hiện là ``tp_dealloc`` phải xóa mọi tham chiếu yếu (bằng cách gọi :c:func:`PyObject_ClearWeakRefs`)::

   static void
   Trivial_dealloc(PyObject *op)
   {
       /* Xóa weakref trước khi gọi bất kỳ destructor nào */
       PyObject_ClearWeakRefs(op);
       /* ... lược bỏ phần mã hủy còn lại cho ngắn gọn ... */
       Py_TYPE(op)->tp_free(op);
   }


Các đề xuất khác
----------------

Để tìm hiểu cách triển khai một phương thức cụ thể cho kiểu dữ liệu mới, hãy tải mã nguồn :term:`CPython`. Đi tới thư mục :file:`Objects`, sau đó tìm trong các tệp mã nguồn C ``tp_`` cùng với hàm bạn muốn (ví dụ: ``tp_richcompare``). Bạn sẽ tìm thấy các ví dụ về hàm mà mình muốn triển khai.

Khi cần xác minh rằng một đối tượng là một thể hiện cụ thể của kiểu bạn đang triển khai, hãy sử dụng hàm :c:func:`PyObject_TypeCheck`. Ví dụ về cách sử dụng hàm này có thể như sau::

   if (!PyObject_TypeCheck(some_object, &MyType)) {
       PyErr_SetString(PyExc_TypeError, "arg #1 not a mything");
       return NULL;
   }

.. seealso::
   Tải xuống các bản phát hành mã nguồn CPython.
      https://www.python.org/downloads/source/

   Dự án CPython trên GitHub, nơi phát triển mã nguồn CPython.
      https://github.com/python/cpython
