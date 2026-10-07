.. highlight:: c

.. _profiling:

Lập hồ sơ hiệu năng và truy vết
===============================

Trình thông dịch Python cung cấp một số hỗ trợ cấp thấp cho việc gắn các công cụ lập hồ sơ hiệu năng và truy vết thực thi. Các công cụ này được dùng để lập hồ sơ hiệu năng, gỡ lỗi và phân tích độ bao phủ.

Giao diện C này cho phép mã lập hồ sơ hiệu năng hoặc truy vết tránh chi phí gọi thông qua các đối tượng callable ở cấp Python bằng cách thực hiện một lần gọi hàm C trực tiếp. Các thuộc tính cốt lõi của cơ chế này không thay đổi; giao diện cho phép cài đặt các hàm truy vết theo từng thread, và các sự kiện cơ bản được báo cáo cho hàm truy vết vẫn giống như những sự kiện đã được báo cáo cho các hàm truy vết ở cấp Python trong các phiên bản trước.


.. c:type:: int (*Py_tracefunc)(PyObject *obj, PyFrameObject *frame, int what, PyObject *arg)

   Kiểu của hàm truy vết được đăng ký bằng :c:func:`PyEval_SetProfile` và
   :c:func:`PyEval_SetTrace`. Tham số đầu tiên là đối tượng được truyền cho hàm đăng ký dưới dạng *obj*, *frame* là đối tượng frame liên quan đến sự kiện, *what* là một trong các hằng số :c:data:`PyTrace_CALL`,
   :c:data:`PyTrace_EXCEPTION`, :c:data:`PyTrace_LINE`, :c:data:`PyTrace_RETURN`,
   :c:data:`PyTrace_C_CALL`, :c:data:`PyTrace_C_EXCEPTION`, :c:data:`PyTrace_C_RETURN` hoặc :c:data:`PyTrace_OPCODE`, còn *arg* phụ thuộc vào giá trị của *what*:

   +-------------------------------+---------------------------------------------------------------------------+
   | Giá trị của *what*            | Ý nghĩa của *arg*                                                         |
   +===============================+===========================================================================+
   | :c:data:`PyTrace_CALL`        | Luôn là :c:data:`Py_None`.                                                |
   +-------------------------------+---------------------------------------------------------------------------+
   | :c:data:`PyTrace_EXCEPTION`   | Thông tin ngoại lệ như được trả về bởi                                    |
   |                               | :func:`sys.exc_info`.                                                     |
   +-------------------------------+---------------------------------------------------------------------------+
   | :c:data:`PyTrace_LINE`        | Luôn là :c:data:`Py_None`.                                                |
   +-------------------------------+---------------------------------------------------------------------------+
   | :c:data:`PyTrace_RETURN`      | Giá trị được trả về cho caller, hoặc ``NULL`` nếu do một ngoại lệ gây ra. |
   +-------------------------------+---------------------------------------------------------------------------+
   | :c:data:`PyTrace_C_CALL`      | Đối tượng hàm đang được gọi.                                              |
   +-------------------------------+---------------------------------------------------------------------------+
   | :c:data:`PyTrace_C_EXCEPTION` | Đối tượng hàm đang được gọi.                                              |
   +-------------------------------+---------------------------------------------------------------------------+
   | :c:data:`PyTrace_C_RETURN`    | Đối tượng hàm đang được gọi.                                              |
   +-------------------------------+---------------------------------------------------------------------------+
   | :c:data:`PyTrace_OPCODE`      | Luôn :c:data:`Py_None`.                                                   |
   +-------------------------------+---------------------------------------------------------------------------+

.. c:var:: int PyTrace_CALL

   Giá trị của tham số *what* đối với hàm :c:type:`Py_tracefunc` khi một lệnh gọi mới đến một hàm hoặc phương thức được báo cáo, hoặc khi bắt đầu một generator mới. Lưu ý rằng việc tạo iterator cho một hàm generator không được báo cáo vì không có sự chuyển quyền điều khiển đến mã bytecode Python trong frame tương ứng.


.. c:var:: int PyTrace_EXCEPTION

   Giá trị của tham số *what* đối với hàm :c:type:`Py_tracefunc` khi một exception đã được phát sinh. Hàm callback được gọi với giá trị này cho *what* khi bất kỳ bytecode nào được xử lý sau đó khiến exception được thiết lập trong frame đang thực thi. Điều này có nghĩa là khi quá trình lan truyền exception khiến ngăn xếp Python unwinding, callback được gọi khi quay lại mỗi frame trong quá trình exception lan truyền. Chỉ các hàm trace mới nhận được những sự kiện này; profiler không cần chúng.


.. c:var:: int PyTrace_LINE

   Giá trị được truyền dưới dạng tham số *what* cho hàm :c:type:`Py_tracefunc` (nhưng không phải hàm profiling) khi một sự kiện số dòng được báo cáo. Có thể vô hiệu hóa sự kiện này cho một frame bằng cách đặt :attr:`~frame.f_trace_lines` thành *0* trên frame đó.


.. c:var:: int PyTrace_RETURN

   Giá trị của tham số *what* đối với các hàm :c:type:`Py_tracefunc` khi một lệnh gọi sắp trả về.


.. c:var:: int PyTrace_C_CALL

   Giá trị của tham số *what* đối với các hàm :c:type:`Py_tracefunc` khi một hàm C sắp được gọi.


.. c:var:: int PyTrace_C_EXCEPTION

   Giá trị của tham số *what* đối với các hàm :c:type:`Py_tracefunc` khi một hàm C đã phát sinh ngoại lệ.


.. c:var:: int PyTrace_C_RETURN

   Giá trị của tham số *what* đối với các hàm :c:type:`Py_tracefunc` khi một hàm C đã trả về.


.. c:var:: int PyTrace_OPCODE

   Giá trị của tham số *what* đối với các hàm :c:type:`Py_tracefunc` (nhưng không phải các hàm profiling) khi một opcode mới sắp được thực thi. Sự kiện này không được phát ra theo mặc định: phải yêu cầu rõ ràng bằng cách đặt
   :attr:`~frame.f_trace_opcodes` thành *1* trên frame.


.. c:function:: void PyEval_SetProfile(Py_tracefunc func, PyObject *obj)

   Đặt hàm profiler thành *func*. Tham số *obj* được truyền cho hàm dưới dạng tham số đầu tiên và có thể là bất kỳ đối tượng Python nào hoặc ``NULL``. Nếu hàm profile cần duy trì trạng thái, việc sử dụng một giá trị *obj* khác nhau cho mỗi thread sẽ cung cấp một nơi thuận tiện và an toàn cho thread để lưu trữ trạng thái đó. Hàm profile được gọi cho tất cả các sự kiện được giám sát, ngoại trừ :c:data:`PyTrace_LINE`
   :c:data:`PyTrace_OPCODE` và :c:data:`PyTrace_EXCEPTION`.

   Xem thêm hàm :func:`sys.setprofile`.

   Bên gọi phải có một :term:`attached thread state`.


.. c:function:: void PyEval_SetProfileAllThreads(Py_tracefunc func, PyObject *obj)

   Tương tự :c:func:`PyEval_SetProfile`, nhưng đặt hàm profiling trong tất cả các thread đang chạy thuộc interpreter hiện tại thay vì chỉ đặt hàm đó trên thread hiện tại.

   Bên gọi phải có một :term:`attached thread state`.

   Giống như :c:func:`PyEval_SetProfile`, hàm này bỏ qua mọi ngoại lệ phát sinh khi đặt các hàm profiling trong tất cả các thread.

.. versionadded:: 3.12


.. c:function:: void PyEval_SetTrace(Py_tracefunc func, PyObject *obj)

   Đặt hàm tracing thành *func*. Hàm này tương tự như
   :c:func:`PyEval_SetProfile`, ngoại trừ việc hàm tracing có nhận các sự kiện số dòng và sự kiện trên từng opcode, nhưng không nhận bất kỳ sự kiện nào liên quan đến các đối tượng hàm C được gọi. Bất kỳ hàm trace nào được đăng ký bằng :c:func:`PyEval_SetTrace` sẽ không nhận :c:data:`PyTrace_C_CALL`, :c:data:`PyTrace_C_EXCEPTION` hoặc
   :c:data:`PyTrace_C_RETURN` làm giá trị cho tham số *what*.

   Xem thêm hàm :func:`sys.settrace`.

   Bên gọi phải có một :term:`attached thread state`.


.. c:function:: void PyEval_SetTraceAllThreads(Py_tracefunc func, PyObject *obj)

   Tương tự :c:func:`PyEval_SetTrace`, nhưng đặt hàm tracing trong tất cả các thread đang chạy thuộc interpreter hiện tại thay vì chỉ đặt hàm đó trên thread hiện tại.

   Bên gọi phải có một :term:`attached thread state`.

   Giống như :c:func:`PyEval_SetTrace`, hàm này bỏ qua mọi ngoại lệ phát sinh khi đặt các hàm trace trong tất cả các thread.

.. versionadded:: 3.12


Theo dõi tham chiếu
===================

.. versionadded:: 3.13


.. c:type:: int (*PyRefTracer)(PyObject *, int event, void* data)

   Kiểu của hàm trace được đăng ký bằng :c:func:`PyRefTracer_SetTracer`. Tham số đầu tiên là một đối tượng Python vừa được tạo (khi **event** được đặt thành :c:data:`PyRefTracer_CREATE`) hoặc sắp bị hủy (khi **event** được đặt thành :c:data:`PyRefTracer_DESTROY`). Đối số **data** là con trỏ opaque được cung cấp khi gọi :c:func:`PyRefTracer_SetTracer`.

   Nếu một hàm tracing mới được đăng ký để thay thế hàm hiện tại, một lệnh gọi đến hàm trace sẽ được thực hiện với object được đặt thành **NULL** và **event** được đặt thành
   :c:data:`PyRefTracer_TRACKER_REMOVED`. Điều này sẽ xảy ra ngay trước khi hàm mới được đăng ký.

.. versionadded:: 3.13


.. c:var:: int PyRefTracer_CREATE

   Giá trị của tham số *event* đối với các hàm :c:type:`PyRefTracer` khi một object Python được tạo.


.. c:var:: int PyRefTracer_DESTROY

   Giá trị của tham số *event* đối với các hàm :c:type:`PyRefTracer` khi một object Python bị hủy.


.. c:var:: int PyRefTracer_TRACKER_REMOVED

   Giá trị của tham số *event* đối với các hàm :c:type:`PyRefTracer` khi tracer hiện tại sắp được thay thế bằng một tracer mới.

   .. versionadded:: 3.14


.. c:function:: int PyRefTracer_SetTracer(PyRefTracer tracer, void *data)

   Đăng ký một hàm reference tracer. Hàm này sẽ được gọi khi một object Python mới được tạo hoặc khi một object sắp bị hủy. Nếu cung cấp **data**, giá trị này phải là một con trỏ opaque sẽ được cung cấp khi hàm tracer được gọi. Trả về ``0`` khi thành công. Đặt một exception và trả về ``-1`` khi có lỗi.

   Lưu ý rằng các hàm tracer **must not** tạo các object Python bên trong hàm; nếu không, lệnh gọi sẽ có tính re-entrant. Tracer cũng **must not** xóa bất kỳ exception hiện có nào hoặc đặt một exception. Một :term:`thread state` sẽ hoạt động mỗi khi hàm tracer được gọi.

   Phải có một :term:`attached thread state` khi gọi hàm này.

   Nếu một hàm tracer khác đã được đăng ký, hàm cũ sẽ được gọi với **event** được đặt thành :c:data:`PyRefTracer_TRACKER_REMOVED` ngay trước khi hàm mới được đăng ký.

.. versionadded:: 3.13


.. c:function:: PyRefTracer PyRefTracer_GetTracer(void** data)

   Lấy hàm reference tracer đã đăng ký và giá trị của con trỏ dữ liệu opaque đã được đăng ký khi :c:func:`PyRefTracer_SetTracer` được gọi. Nếu chưa đăng ký tracer nào, hàm này sẽ trả về NULL và đặt con trỏ **data** thành NULL.

   Phải có một :term:`attached thread state` khi gọi hàm này.

.. versionadded:: 3.13
