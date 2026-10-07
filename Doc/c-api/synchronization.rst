.. highlight:: c

.. _synchronization:

Các primitive đồng bộ hóa
=========================

C-API cung cấp một mutex cơ bản.

.. c:type:: PyMutex

   Một mutex. :c:type:`!PyMutex` phải được khởi tạo bằng 0 để biểu thị trạng thái đã mở khóa. Ví dụ:::

      PyMutex mutex = {0};

   Các instance của :c:type:`!PyMutex` không nên được sao chép hoặc di chuyển. Cả nội dung và địa chỉ của một :c:type:`!PyMutex` đều có ý nghĩa, và nó phải được giữ cố định tại một vị trí có thể ghi trong bộ nhớ.

   .. note::

      Một :c:type:`!PyMutex` hiện chiếm một byte, nhưng kích thước này nên được xem là không ổn định. Kích thước có thể thay đổi trong các bản phát hành Python sau này mà không cần có thời gian deprecation.

   .. versionadded:: 3.13

.. c:function:: void PyMutex_Lock(PyMutex *m)

   Khóa mutex *m*. Nếu một thread khác đã khóa mutex này, thread gọi sẽ bị chặn cho đến khi mutex được mở khóa. Trong khi bị chặn, thread sẽ tạm thời tách :term:`trạng thái thread <attached thread state>` nếu có.

   .. versionadded:: 3.13

.. c:function:: void PyMutex_Unlock(PyMutex *m)

   Mở khóa mutex *m*. Mutex phải đang được khóa --- nếu không, hàm sẽ phát sinh lỗi nghiêm trọng.

   .. versionadded:: 3.13

.. c:function:: int PyMutex_IsLocked(PyMutex *m)

   Trả về giá trị khác không nếu mutex *m* hiện đang bị khóa, ngược lại trả về giá trị bằng không.

   .. note::

      Hàm này chỉ предназначен cho các phép assertion và việc debug, không nên được dùng để đưa ra quyết định kiểm soát đồng thời, vì trạng thái khóa có thể thay đổi ngay sau khi kiểm tra.

   .. versionadded:: 3.14

.. _python-critical-section-api:

API vùng tới hạn của Python
---------------------------

API vùng tới hạn cung cấp một lớp tránh deadlock trên các khóa riêng theo từng đối tượng cho CPython :term:`không có GIL <free threading>`. Chúng được thiết kế để thay thế việc phụ thuộc vào :term:`global interpreter lock`, và không thực hiện thao tác nào trong các phiên bản Python có global interpreter lock.

Các vùng tới hạn được thiết kế để sử dụng cho những kiểu tùy chỉnh được triển khai trong các phần mở rộng C-API. Nhìn chung, không nên sử dụng chúng với các kiểu dựng sẵn như
:class:`list` và :class:`dict` vì các C-API công khai của chúng đã sử dụng vùng tới hạn ở bên trong, ngoại trừ đáng chú ý là :c:func:`PyDict_Next`, vốn yêu cầu vùng tới hạn phải được lấy ở bên ngoài.

Các vùng tới hạn tránh deadlock bằng cách ngầm tạm dừng các vùng tới hạn đang hoạt động; do đó, chúng không cung cấp quyền truy cập độc quyền như các khóa truyền thống, chẳng hạn :c:type:`PyMutex`. Khi bắt đầu một vùng tới hạn, khóa riêng theo từng đối tượng của đối tượng đó sẽ được lấy. Nếu mã được thực thi bên trong vùng tới hạn gọi các hàm C-API, vùng tới hạn có thể bị tạm dừng, qua đó giải phóng khóa riêng theo từng đối tượng để các thread khác có thể lấy khóa riêng theo từng đối tượng của cùng đối tượng đó.

Các biến thể chấp nhận con trỏ :c:type:`PyMutex` thay vì các đối tượng Python cũng có sẵn. Hãy sử dụng các biến thể này để bắt đầu một critical section trong tình huống không có :c:type:`PyObject` -- chẳng hạn khi làm việc với một kiểu C không mở rộng hoặc bao bọc :c:type:`PyObject` nhưng vẫn cần gọi C API theo cách có thể dẫn đến deadlock.

Các hàm và struct được macro sử dụng được cung cấp cho những trường hợp không có macro C. Chỉ nên sử dụng chúng giống như trong các macro expansion đã cho. Lưu ý rằng kích thước và nội dung của các cấu trúc có thể thay đổi trong các phiên bản Python tương lai.

.. note::

   Các thao tác cần khóa đồng thời hai đối tượng phải sử dụng
   :c:macro:`Py_BEGIN_CRITICAL_SECTION2`. Bạn *không thể* sử dụng các critical section lồng nhau để khóa đồng thời nhiều hơn một đối tượng, vì critical section bên trong có thể tạm dừng các critical section bên ngoài. API này không cung cấp cách khóa đồng thời nhiều hơn hai đối tượng.

Ví dụ sử dụng::

   static PyObject *
   set_field(MyObject *self, PyObject *value)
   {
      Py_BEGIN_CRITICAL_SECTION(self);
      Py_SETREF(self->field, Py_XNewRef(value));
      Py_END_CRITICAL_SECTION();
      Py_RETURN_NONE;
   }

Trong ví dụ trên, :c:macro:`Py_SETREF` gọi :c:macro:`Py_DECREF`, hàm này có thể gọi mã tùy ý thông qua hàm giải phóng của một đối tượng. API critical section tránh các deadlock tiềm ẩn do khả năng tái nhập và thứ tự khóa bằng cách cho phép runtime tạm thời tạm dừng critical section nếu mã được finalizer kích hoạt bị block và gọi :c:func:`PyEval_SaveThread`.

.. c:macro:: Py_BEGIN_CRITICAL_SECTION(op)

   Lấy khóa cho từng đối tượng của đối tượng *op* và bắt đầu một critical section.

   Trong bản dựng free-threaded, macro này mở rộng thành::

      {
          PyCriticalSection _py_cs;
          PyCriticalSection_Begin(&_py_cs, (PyObject*)(op))

   Trong bản dựng mặc định, macro này mở rộng thành ``{``.

   .. versionadded:: 3.13

.. c:macro:: Py_BEGIN_CRITICAL_SECTION_MUTEX(m)

   Khóa mutex *m* và bắt đầu một critical section.

   Trong bản dựng free-threaded, macro này mở rộng thành::

     {
          PyCriticalSection _py_cs;
          PyCriticalSection_BeginMutex(&_py_cs, m)

   Lưu ý rằng, không giống như :c:macro:`Py_BEGIN_CRITICAL_SECTION`, không có phép ép kiểu cho đối số của macro — đối số phải là một con trỏ :c:type:`PyMutex`.

   Trong bản dựng mặc định, macro này mở rộng thành ``{``.

   .. versionadded:: 3.14

.. c:macro:: Py_END_CRITICAL_SECTION()

   Kết thúc critical section và giải phóng khóa trên mỗi đối tượng.

   Trong bản dựng free-threaded, macro này mở rộng thành::

          PyCriticalSection_End(&_py_cs);
      }

   Trong bản dựng mặc định, macro này được mở rộng thành ``}``.

   .. versionadded:: 3.13

.. c:macro:: Py_BEGIN_CRITICAL_SECTION2(a, b)

   Lấy các khóa theo từng đối tượng cho các đối tượng *a* và *b* rồi bắt đầu một vùng tới hạn. Các khóa được lấy theo một thứ tự nhất quán (địa chỉ thấp nhất trước) để tránh deadlock do thứ tự khóa.

   Trong bản dựng free-threaded, macro này mở rộng thành::

      {
          PyCriticalSection2 _py_cs2;
          PyCriticalSection2_Begin(&_py_cs2, (PyObject*)(a), (PyObject*)(b))

   Trong bản dựng mặc định, macro này mở rộng thành ``{``.

   .. versionadded:: 3.13

.. c:macro:: Py_BEGIN_CRITICAL_SECTION2_MUTEX(m1, m2)

   Khóa các mutex *m1* và *m2* rồi bắt đầu một vùng tới hạn.

   Trong bản dựng free-threaded, macro này mở rộng thành::

     {
          PyCriticalSection2 _py_cs2;
          PyCriticalSection2_BeginMutex(&_py_cs2, m1, m2)

   Lưu ý rằng không giống như :c:macro:`Py_BEGIN_CRITICAL_SECTION2`, các đối số của macro không được ép kiểu - chúng phải là các con trỏ :c:type:`PyMutex`.

   Trong bản dựng mặc định, macro này mở rộng thành ``{``.

   .. versionadded:: 3.14

.. c:macro:: Py_END_CRITICAL_SECTION2()

   Kết thúc critical section và giải phóng các khóa trên từng đối tượng.

   Trong bản dựng free-threaded, macro này mở rộng thành::

          PyCriticalSection2_End(&_py_cs2);
      }

   Trong bản dựng mặc định, macro này được mở rộng thành ``}``.

   .. versionadded:: 3.13


Các API khóa cũ
---------------

Các API này đã lỗi thời kể từ Python 3.13 với sự ra mắt của
:c:type:`PyMutex`.


.. c:type:: PyThread_type_lock

   Một con trỏ tới khóa loại trừ tương hỗ.


.. c:type:: PyLockStatus

   Kết quả của việc lấy khóa với thời gian chờ.

   .. c:namespace:: NULL

   .. c:enumerator:: PY_LOCK_FAILURE

      Không thể lấy khóa.

   .. c:enumerator:: PY_LOCK_ACQUIRED

      Đã lấy khóa thành công.

   .. c:enumerator:: PY_LOCK_INTR

      Việc lấy khóa đã bị gián đoạn bởi một signal.


.. c:function:: PyThread_type_lock PyThread_allocate_lock(void)

   Cấp phát một khóa mới.

   Khi thành công, hàm này trả về một khóa; khi thất bại, hàm này trả về ``0`` mà không thiết lập ngoại lệ.

   Caller không cần phải giữ :term:`attached thread state`.


.. c:function:: void PyThread_free_lock(PyThread_type_lock lock)

   Hủy *lock*. Không thread nào được giữ lock khi gọi hàm này.

   Caller không cần phải giữ :term:`attached thread state`.


.. c:function:: PyLockStatus PyThread_acquire_lock_timed(PyThread_type_lock lock, long long microseconds, int intr_flag)

   Acquire *lock* với thời gian chờ.

   Hàm này sẽ chờ *microseconds* microseconds để acquire lock. Nếu hết thời gian chờ, hàm này trả về :c:enumerator:`PY_LOCK_FAILURE`. Nếu *microseconds* là ``-1``, hàm sẽ chờ vô thời hạn cho đến khi lock được giải phóng.

   Nếu *intr_flag* là ``1``, việc acquire lock có thể bị gián đoạn bởi một signal; khi đó, hàm này trả về :c:enumerator:`PY_LOCK_INTR`. Khi bị gián đoạn, caller thường được kỳ vọng sẽ gọi
   :c:func:`Py_MakePendingCalls` để truyền một exception đến mã Python.

   Nếu khóa được lấy thành công, hàm này trả về
   :c:enumerator:`PY_LOCK_ACQUIRED`.

   Caller không cần phải giữ :term:`attached thread state`.


.. c:function:: int PyThread_acquire_lock(PyThread_type_lock lock, int waitflag)

   Lấy *khóa*.

   Nếu *waitflag* là ``1`` và một thread khác hiện đang giữ khóa, hàm này sẽ chờ cho đến khi có thể lấy khóa và luôn trả về ``1``.

   Nếu *waitflag* là ``0`` và một thread khác đang giữ khóa, hàm này sẽ không chờ mà thay vào đó trả về ``0``. Nếu không có thread nào khác giữ khóa, hàm này sẽ lấy khóa và trả về ``1``.

   Không giống như :c:func:`PyThread_acquire_lock_timed`, việc lấy khóa không thể bị gián đoạn bởi tín hiệu.

   Caller không cần phải giữ :term:`attached thread state`.


.. c:function:: int PyThread_release_lock(PyThread_type_lock lock)

   Giải phóng *lock*. Nếu *lock* không được giữ, hàm này sẽ phát sinh lỗi nghiêm trọng.

   Caller không cần phải giữ :term:`attached thread state`.
