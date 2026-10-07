.. highlight:: c

.. _capsules:

Capsule
-------

.. index:: pair: object; Capsule

Tham khảo :ref:`using-capsules` để biết thêm thông tin về cách sử dụng các đối tượng này.

.. versionadded:: 3.1


.. c:type:: PyCapsule

   Kiểu con này của :c:type:`PyObject` biểu diễn một giá trị opaque, hữu ích cho các module mở rộng C cần truyền một giá trị opaque (dưới dạng con trỏ :c:expr:`void*`) qua mã Python đến mã C khác. Nó thường được dùng để cung cấp một con trỏ hàm C được định nghĩa trong một module cho các module khác, nhờ đó có thể sử dụng cơ chế import thông thường để truy cập các C API được định nghĩa trong các module được tải động.


.. c:var:: PyTypeObject PyCapsule_Type

   Đối tượng kiểu tương ứng với các đối tượng capsule. Đây chính là đối tượng :class:`types.CapsuleType` trong lớp Python.


.. c:type:: PyCapsule_Destructor

   Kiểu của một callback hủy đối với capsule. Được định nghĩa như sau::

      typedef void (*PyCapsule_Destructor)(PyObject *);

   Xem :c:func:`PyCapsule_New` để biết ngữ nghĩa của các callback PyCapsule_Destructor.


.. c:function:: int PyCapsule_CheckExact(PyObject *p)

   Trả về true nếu đối số của nó là một :c:type:`PyCapsule`. Hàm này luôn thành công.


.. c:function:: PyObject* PyCapsule_New(void *pointer, const char *name, PyCapsule_Destructor destructor)

   Tạo một :c:type:`PyCapsule` đóng gói *con trỏ*. Đối số *con trỏ* không được là ``NULL``.

   Nếu thất bại, hãy đặt một exception và trả về ``NULL``.

   Chuỗi *tên* có thể là ``NULL`` hoặc một con trỏ trỏ đến một chuỗi C hợp lệ. Nếu không phải ``NULL``, chuỗi này phải tồn tại lâu hơn capsule. (Tuy nhiên, bạn được phép giải phóng nó bên trong *hàm hủy*.)

   Nếu đối số *hàm hủy* không phải là ``NULL``, hàm này sẽ được gọi với capsule làm đối số khi capsule bị hủy.

   Nếu capsule này sẽ được lưu làm thuộc tính của một module, *tên* nên được chỉ định là ``modulename.attributename``. Điều này cho phép các module khác import capsule bằng :c:func:`PyCapsule_Import`.


.. c:function:: void* PyCapsule_GetPointer(PyObject *capsule, const char *name)

   Truy xuất *con trỏ* được lưu trong capsule. Nếu thất bại, hãy đặt một exception và trả về ``NULL``.

   Tham số *tên* phải khớp chính xác với tên được lưu trong capsule. Nếu tên được lưu trong capsule là ``NULL``, *tên* được truyền vào cũng phải là ``NULL``. Python sử dụng hàm C :c:func:`!strcmp` để so sánh tên capsule.


.. c:function:: PyCapsule_Destructor PyCapsule_GetDestructor(PyObject *capsule)

   Trả về trình hủy hiện tại được lưu trong capsule. Nếu thất bại, thiết lập một exception và trả về ``NULL``.

   Một capsule có thể hợp lệ có trình hủy ``NULL``. Điều này khiến mã trả về ``NULL`` trở nên khá mơ hồ; hãy sử dụng :c:func:`PyCapsule_IsValid` hoặc
   :c:func:`PyErr_Occurred` để phân biệt.


.. c:function:: void* PyCapsule_GetContext(PyObject *capsule)

   Trả về context hiện tại được lưu trong capsule. Nếu thất bại, thiết lập một exception và trả về ``NULL``.

   Một capsule có thể hợp lệ có context ``NULL``. Điều này khiến mã trả về ``NULL`` trở nên khá mơ hồ; hãy sử dụng :c:func:`PyCapsule_IsValid` hoặc
   :c:func:`PyErr_Occurred` để phân biệt.


.. c:function:: const char* PyCapsule_GetName(PyObject *capsule)

   Trả về name hiện tại được lưu trong capsule. Nếu thất bại, thiết lập một exception và trả về ``NULL``.

   Một capsule có thể có tên ``NULL``. Điều này khiến mã trả về ``NULL`` trở nên khá mơ hồ; hãy sử dụng :c:func:`PyCapsule_IsValid` hoặc
   :c:func:`PyErr_Occurred` để phân biệt.


.. c:function:: void* PyCapsule_Import(const char *name, int no_block)

   Nhập một con trỏ đến đối tượng C từ thuộc tính capsule trong một module. Tham số *name* phải chỉ định tên đầy đủ của thuộc tính, như trong ``module.attribute``. *name* được lưu trong capsule phải khớp chính xác với chuỗi này.

   Hàm này tách *name* tại ký tự ``.`` và nhập phần tử đầu tiên. Sau đó, hàm xử lý các phần tử tiếp theo bằng cách tra cứu thuộc tính.

   Trả về *pointer* nội bộ của capsule nếu thành công. Khi thất bại, hãy đặt một exception và trả về ``NULL``.

   .. note::

      Nếu *name* trỏ đến một thuộc tính của submodule hoặc subpackage nào đó, submodule hoặc subpackage này phải được import trước bằng cách khác (ví dụ: sử dụng :c:func:`PyImport_ImportModule`) để việc tra cứu thuộc tính thành công.

   .. versionchanged:: 3.3
      *no_block* không còn có tác dụng.


.. c:function:: int PyCapsule_IsValid(PyObject *capsule, const char *name)

   Xác định liệu *capsule* có phải là một capsule hợp lệ hay không. Một capsule hợp lệ là không-``NULL``, vượt qua :c:func:`PyCapsule_CheckExact`, có một con trỏ ``NULL`` khác không được lưu trong đó, và tên nội bộ của nó khớp với tham số *name*. (Xem
   :c:func:`PyCapsule_GetPointer` để biết thông tin về cách so sánh tên capsule.)

   Nói cách khác, nếu :c:func:`PyCapsule_IsValid` trả về giá trị true, các lệnh gọi đến bất kỳ accessor nào (bất kỳ hàm nào bắt đầu bằng ``PyCapsule_Get``) đều được đảm bảo thành công.

   Trả về một giá trị khác không nếu đối tượng hợp lệ và khớp với tên được truyền vào. Trả về ``0`` nếu không. Hàm này sẽ không thất bại.


.. c:function:: int PyCapsule_SetContext(PyObject *capsule, void *context)

   Đặt con trỏ context bên trong *capsule* thành *context*.

   Trả về ``0`` khi thành công. Trả về giá trị khác không và đặt một exception khi thất bại.


.. c:function:: int PyCapsule_SetDestructor(PyObject *capsule, PyCapsule_Destructor destructor)

   Đặt destructor bên trong *capsule* thành *destructor*.

   Trả về ``0`` khi thành công. Trả về giá trị khác không và đặt một exception khi thất bại.


.. c:function:: int PyCapsule_SetName(PyObject *capsule, const char *name)

   Đặt name bên trong *capsule* thành *name*. Nếu không phải ``NULL``, name phải tồn tại lâu hơn capsule. Nếu *name* trước đó được lưu trong capsule không phải là ``NULL``, sẽ không cố gắng giải phóng nó.

   Trả về ``0`` khi thành công. Trả về giá trị khác không và đặt một exception khi thất bại.


.. c:function:: int PyCapsule_SetPointer(PyObject *capsule, void *pointer)

   Đặt con trỏ void bên trong *capsule* thành *pointer*. Con trỏ không được là ``NULL``.

   Trả về ``0`` khi thành công. Trả về giá trị khác không và đặt một exception khi thất bại.
