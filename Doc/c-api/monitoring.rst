.. highlight:: c

.. _c-api-monitoring:

API C về giám sát
=================

Được thêm trong phiên bản 3.13.

Một extension có thể cần tương tác với hệ thống giám sát sự kiện. Việc đăng ký sự kiện và đăng ký callback có thể được thực hiện thông qua Python API được cung cấp trong
:mod:`sys.monitoring`.

Tạo sự kiện thực thi
====================

Các hàm dưới đây cho phép một extension kích hoạt các sự kiện giám sát khi mô phỏng việc thực thi mã Python. Mỗi hàm này nhận một struct ``PyMonitoringState``, struct này chứa thông tin ngắn gọn về trạng thái kích hoạt của các sự kiện, cũng như các đối số sự kiện, bao gồm một ``PyObject*`` đại diện cho đối tượng mã, offset của chỉ thị và đôi khi có thêm các đối số dành riêng cho từng sự kiện (xem :mod:`sys.monitoring` để biết chi tiết về chữ ký của các callback sự kiện khác nhau). Đối số ``codelike`` phải là một thực thể của :class:`types.CodeType` hoặc của một kiểu mô phỏng nó.

VM vô hiệu hóa việc tracing khi kích hoạt một sự kiện, vì vậy mã người dùng không cần thực hiện việc đó.

Không nên gọi các hàm giám sát khi một exception đang được thiết lập, ngoại trừ những hàm được liệt kê bên dưới là hoạt động với exception hiện tại.

.. c:type:: PyMonitoringState

  Biểu diễn trạng thái của một loại sự kiện. Người dùng cấp phát đối tượng này, còn nội dung của nó được duy trì bởi các hàm monitoring API được mô tả dưới đây.


Tất cả các hàm dưới đây trả về 0 khi thành công và -1 (với một exception được thiết lập) khi xảy ra lỗi.

Xem :mod:`sys.monitoring` để biết mô tả về các sự kiện.

.. c:function:: int PyMonitoring_FirePyStartEvent(PyMonitoringState *state, PyObject *codelike, int32_t offset)

   Kích hoạt một sự kiện ``PY_START``.


.. c:function:: int PyMonitoring_FirePyResumeEvent(PyMonitoringState *state, PyObject *codelike, int32_t offset)

   Kích hoạt một sự kiện ``PY_RESUME``.


.. c:function:: int PyMonitoring_FirePyReturnEvent(PyMonitoringState *state, PyObject *codelike, int32_t offset, PyObject* retval)

   Kích hoạt một sự kiện ``PY_RETURN``.


.. c:function:: int PyMonitoring_FirePyYieldEvent(PyMonitoringState *state, PyObject *codelike, int32_t offset, PyObject* retval)

   Kích hoạt một sự kiện ``PY_YIELD``.


.. c:function:: int PyMonitoring_FireCallEvent(PyMonitoringState *state, PyObject *codelike, int32_t offset, PyObject* callable, PyObject *arg0)

   Phát một sự kiện ``CALL``.


.. c:function:: int PyMonitoring_FireLineEvent(PyMonitoringState *state, PyObject *codelike, int32_t offset, int lineno)

   Phát một sự kiện ``LINE``.


.. c:function:: int PyMonitoring_FireJumpEvent(PyMonitoringState *state, PyObject *codelike, int32_t offset, PyObject *target_offset)

   Phát một sự kiện ``JUMP``.


.. c:function:: int PyMonitoring_FireBranchLeftEvent(PyMonitoringState *state, PyObject *codelike, int32_t offset, PyObject *target_offset)

   Phát một sự kiện ``BRANCH_LEFT``.


.. c:function:: int PyMonitoring_FireBranchRightEvent(PyMonitoringState *state, PyObject *codelike, int32_t offset, PyObject *target_offset)

   Phát một sự kiện ``BRANCH_RIGHT``.


.. c:function:: int PyMonitoring_FireCReturnEvent(PyMonitoringState *state, PyObject *codelike, int32_t offset, PyObject *retval)

   Phát một sự kiện ``C_RETURN``.


.. c:function:: int PyMonitoring_FirePyThrowEvent(PyMonitoringState *state, PyObject *codelike, int32_t offset)

   Phát một sự kiện ``PY_THROW`` với ngoại lệ hiện tại (do
   :c:func:`PyErr_GetRaisedException`).


.. c:function:: int PyMonitoring_FireRaiseEvent(PyMonitoringState *state, PyObject *codelike, int32_t offset)

   Phát một sự kiện ``RAISE`` với ngoại lệ hiện tại (như được trả về bởi
   :c:func:`PyErr_GetRaisedException`).


.. c:function:: int PyMonitoring_FireCRaiseEvent(PyMonitoringState *state, PyObject *codelike, int32_t offset)

   Phát một sự kiện ``C_RAISE`` với ngoại lệ hiện tại (như được trả về bởi
   :c:func:`PyErr_GetRaisedException`).


.. c:function:: int PyMonitoring_FireReraiseEvent(PyMonitoringState *state, PyObject *codelike, int32_t offset)

   Phát một sự kiện ``RERAISE`` với ngoại lệ hiện tại (như được trả về bởi
   :c:func:`PyErr_GetRaisedException`).


.. c:function:: int PyMonitoring_FireExceptionHandledEvent(PyMonitoringState *state, PyObject *codelike, int32_t offset)

   Phát một sự kiện ``EXCEPTION_HANDLED`` với ngoại lệ hiện tại (như được trả về bởi
   :c:func:`PyErr_GetRaisedException`).


.. c:function:: int PyMonitoring_FirePyUnwindEvent(PyMonitoringState *state, PyObject *codelike, int32_t offset)

   Phát một sự kiện ``PY_UNWIND`` với ngoại lệ hiện tại (như được trả về bởi
   :c:func:`PyErr_GetRaisedException`).


.. c:function:: int PyMonitoring_FireStopIterationEvent(PyMonitoringState *state, PyObject *codelike, int32_t offset, PyObject *value)

   Phát một sự kiện ``STOP_ITERATION``. Nếu ``value`` là một instance của :exc:`StopIteration`, nó sẽ được sử dụng. Nếu không, một instance :exc:`StopIteration` mới sẽ được tạo với ``value`` làm đối số.


Quản lý trạng thái giám sát
---------------------------

Trạng thái monitoring có thể được quản lý với sự trợ giúp của các phạm vi monitoring. Một phạm vi thường tương ứng với một hàm Python.

.. c:function:: int PyMonitoring_EnterScope(PyMonitoringState *state_array, uint64_t *version, const uint8_t *event_types, Py_ssize_t length)

   Đi vào một phạm vi được monitoring. ``event_types`` là một mảng chứa các ID sự kiện của những sự kiện có thể được kích hoạt từ phạm vi này. Ví dụ, ID của sự kiện ``PY_START`` là giá trị ``PY_MONITORING_EVENT_PY_START``, về mặt số học bằng logarit cơ số 2 của ``sys.monitoring.events.PY_START``. ``state_array`` là một mảng có một mục nhập trạng thái monitoring cho mỗi sự kiện trong ``event_types``, mảng này do người dùng cấp phát nhưng được điền bởi
   :c:func:`!PyMonitoring_EnterScope` cùng thông tin về trạng thái kích hoạt của sự kiện. Kích thước của ``event_types`` (và do đó cả ``state_array``) được cung cấp trong ``length``.

   Đối số ``version`` là một con trỏ đến một giá trị mà người dùng phải cấp phát cùng với ``state_array``, khởi tạo bằng 0, sau đó chỉ được chính :c:func:`!PyMonitoring_EnterScope` thiết lập. Đối số này cho phép hàm xác định xem trạng thái sự kiện có thay đổi kể từ lần gọi trước hay không, và nhanh chóng trả về nếu không thay đổi.

   Các phạm vi được đề cập ở đây là phạm vi từ vựng: một hàm, lớp hoặc phương thức.
   :c:func:`!PyMonitoring_EnterScope` nên được gọi bất cứ khi nào phạm vi từ vựng được đi vào. Có thể đi vào lại các phạm vi bằng cách sử dụng lại *state_array* và *version* tương tự, trong những tình huống như khi mô phỏng một hàm Python đệ quy. Khi quá trình thực thi một cấu trúc giống mã bị tạm dừng, chẳng hạn khi mô phỏng một generator, cần thoát khỏi phạm vi rồi đi vào lại.

   Các macro cho *event_types* là:

   .. c:namespace:: NULL

   .. The table is here to make the docs searchable, and to allow automatic
      links to the identifiers.

   +----------------------------------------------------+---------------------------------------+
   | Macro                                              | Event                                 |
   +====================================================+=======================================+
   | .. c:macro:: PY_MONITORING_EVENT_BRANCH_LEFT       | :monitoring-event:`BRANCH_LEFT`       |
   +----------------------------------------------------+---------------------------------------+
   | .. c:macro:: PY_MONITORING_EVENT_BRANCH_RIGHT      | :monitoring-event:`BRANCH_RIGHT`      |
   +----------------------------------------------------+---------------------------------------+
   | .. c:macro:: PY_MONITORING_EVENT_CALL              | :monitoring-event:`CALL`              |
   +----------------------------------------------------+---------------------------------------+
   | .. c:macro:: PY_MONITORING_EVENT_C_RAISE           | :monitoring-event:`C_RAISE`           |
   +----------------------------------------------------+---------------------------------------+
   | .. c:macro:: PY_MONITORING_EVENT_C_RETURN          | :monitoring-event:`C_RETURN`          |
   +----------------------------------------------------+---------------------------------------+
   | .. c:macro:: PY_MONITORING_EVENT_EXCEPTION_HANDLED | :monitoring-event:`EXCEPTION_HANDLED` |
   +----------------------------------------------------+---------------------------------------+
   | .. c:macro:: PY_MONITORING_EVENT_INSTRUCTION       | :monitoring-event:`INSTRUCTION`       |
   +----------------------------------------------------+---------------------------------------+
   | .. c:macro:: PY_MONITORING_EVENT_JUMP              | :monitoring-event:`JUMP`              |
   +----------------------------------------------------+---------------------------------------+
   | .. c:macro:: PY_MONITORING_EVENT_LINE              | :monitoring-event:`LINE`              |
   +----------------------------------------------------+---------------------------------------+
   | .. c:macro:: PY_MONITORING_EVENT_PY_RESUME         | :monitoring-event:`PY_RESUME`         |
   +----------------------------------------------------+---------------------------------------+
   | .. c:macro:: PY_MONITORING_EVENT_PY_RETURN         | :monitoring-event:`PY_RETURN`         |
   +----------------------------------------------------+---------------------------------------+
   | .. c:macro:: PY_MONITORING_EVENT_PY_START          | :monitoring-event:`PY_START`          |
   +----------------------------------------------------+---------------------------------------+
   | .. c:macro:: PY_MONITORING_EVENT_PY_THROW          | :monitoring-event:`PY_THROW`          |
   +----------------------------------------------------+---------------------------------------+
   | .. c:macro:: PY_MONITORING_EVENT_PY_UNWIND         | :monitoring-event:`PY_UNWIND`         |
   +----------------------------------------------------+---------------------------------------+
   | .. c:macro:: PY_MONITORING_EVENT_PY_YIELD          | :monitoring-event:`PY_YIELD`          |
   +----------------------------------------------------+---------------------------------------+
   | .. c:macro:: PY_MONITORING_EVENT_RAISE             | :monitoring-event:`RAISE`             |
   +----------------------------------------------------+---------------------------------------+
   | .. c:macro:: PY_MONITORING_EVENT_RERAISE           | :monitoring-event:`RERAISE`           |
   +----------------------------------------------------+---------------------------------------+
   | .. c:macro:: PY_MONITORING_EVENT_STOP_ITERATION    | :monitoring-event:`STOP_ITERATION`    |
   +----------------------------------------------------+---------------------------------------+

.. c:function:: int PyMonitoring_ExitScope(void)

   Thoát khỏi phạm vi cuối cùng đã được nhập bằng :c:func:`!PyMonitoring_EnterScope`.


.. c:function:: int PY_MONITORING_IS_INSTRUMENTED_EVENT(uint8_t ev)

   Trả về true nếu event tương ứng với event ID *ev* là một :ref:`sự kiện cục bộ <monitoring-event-local>`.

   .. versionadded:: 3.13

   .. soft-deprecated:: 3.14
