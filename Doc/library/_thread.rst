:mod:`!_thread` --- API phân luồng cấp thấp
===========================================

.. module:: _thread
   :synopsis: API phân luồng cấp thấp.

.. index::
   single: light-weight processes
   single: processes, light-weight
   single: binary semaphores
   single: semaphores, binary

--------------

Mô-đun này cung cấp các primitive cấp thấp để làm việc với nhiều thread (còn gọi là :dfn:`tiến trình nhẹ` hoặc :dfn:`tác vụ`) --- nhiều luồng điều khiển cùng chia sẻ không gian dữ liệu toàn cục. Để đồng bộ hóa, mô-đun cung cấp các khóa đơn giản (còn gọi là :dfn:`mutex` hoặc :dfn:`semaphore nhị phân`). Mô-đun :mod:`threading` cung cấp API phân luồng cấp cao hơn và dễ sử dụng hơn, được xây dựng dựa trên mô-đun này.

.. index::
   single: pthreads
   pair: threads; POSIX

.. versionchanged:: 3.7
   Trước đây, mô-đun này là tùy chọn; hiện tại, mô-đun luôn khả dụng.

Mô-đun này định nghĩa các hằng số và hàm sau:

.. exception:: error

   Được phát sinh khi xảy ra lỗi liên quan đến thread.

   .. versionchanged:: 3.3
      Hiện đây là từ đồng nghĩa với :exc:`RuntimeError` có sẵn.


.. function:: start_new_thread(function, args[, kwargs])

   Khởi chạy một thread mới và trả về mã định danh của thread đó. Thread thực thi hàm *function* với danh sách đối số *args* (phải là một tuple). Đối số tùy chọn *kwargs* chỉ định một dictionary chứa các keyword argument.

   Khi hàm trả về, thread sẽ âm thầm thoát.

   Khi hàm kết thúc do một ngoại lệ chưa được xử lý,
   :func:`sys.unraisablehook` được gọi để xử lý ngoại lệ. Thuộc tính *object* của đối số hook là *function*. Theo mặc định, một stack trace được in ra rồi thread thoát (nhưng các thread khác vẫn tiếp tục chạy).

   Khi hàm phát sinh một ngoại lệ :exc:`SystemExit`, ngoại lệ đó sẽ bị bỏ qua một cách im lặng.

   .. audit-event:: _thread.start_new_thread function,args,kwargs start_new_thread

   .. versionchanged:: 3.8
      :func:`sys.unraisablehook` is now used to handle unhandled exceptions.


.. function:: interrupt_main(signum=signal.SIGINT, /)

   Mô phỏng hiệu ứng của một signal đến trong thread chính. Một thread có thể sử dụng hàm này để ngắt thread chính, mặc dù không có gì đảm bảo rằng việc ngắt sẽ xảy ra ngay lập tức.

   Nếu được cung cấp, *signum* là số của signal cần mô phỏng. Nếu không cung cấp *signum*, :const:`signal.SIGINT` sẽ được mô phỏng.

   Nếu tín hiệu đã cho không được Python xử lý (nó đã được đặt thành
   :const:`signal.SIG_DFL` hoặc :const:`signal.SIG_IGN`), hàm này không thực hiện thao tác nào.

   .. versionchanged:: 3.10
      Đối số *signum* được thêm vào để tùy chỉnh số hiệu tín hiệu.

   .. note::
      Thao tác này không phát ra tín hiệu tương ứng mà lên lịch gọi trình xử lý liên kết (nếu trình xử lý đó tồn tại). Nếu bạn muốn thực sự phát tín hiệu, hãy sử dụng :func:`signal.raise_signal`.


.. function:: exit()

   Ném ngoại lệ :exc:`SystemExit`. Nếu không được bắt, ngoại lệ này sẽ khiến thread kết thúc trong im lặng.

..
   function:: exit_prog(status)

      Thoát khỏi tất cả các thread và báo cáo giá trị của đối số số nguyên *status* làm trạng thái thoát của toàn bộ chương trình. **Lưu ý:** mã trong các mệnh đề :keyword:`finally` đang chờ xử lý, dù trong thread này hay các thread khác, đều không được thực thi.


.. function:: allocate_lock()

   Trả về một đối tượng lock mới. Các phương thức của lock được mô tả bên dưới. Lock ban đầu ở trạng thái mở khóa.


.. function:: get_ident()

   Trả về 'thread identifier' của thread hiện tại. Đây là một số nguyên khác không. Giá trị của nó không có ý nghĩa trực tiếp; nó được dùng như một magic cookie, chẳng hạn để lập chỉ mục cho một dictionary chứa dữ liệu dành riêng cho thread. Thread identifier có thể được tái sử dụng khi một thread kết thúc và một thread khác được tạo.


.. function:: get_native_id()

   Trả về Thread ID dạng số nguyên gốc của thread hiện tại, do kernel gán. Đây là một số nguyên không âm. Giá trị này có thể được dùng để định danh duy nhất thread cụ thể này trên toàn hệ thống (cho đến khi thread kết thúc; sau đó giá trị có thể được OS tái sử dụng).

   .. availability:: Windows, FreeBSD, Linux, macOS, OpenBSD, NetBSD, AIX, DragonFlyBSD, GNU/kFreeBSD.

   .. versionadded:: 3.8

   .. versionchanged:: 3.13
      Đã bổ sung hỗ trợ cho GNU/kFreeBSD.


.. function:: stack_size([size])

   Trả về kích thước stack của thread được sử dụng khi tạo các thread mới. Đối số *size* tùy chọn chỉ định kích thước stack sẽ được sử dụng cho các thread được tạo sau đó, và phải là 0 (sử dụng giá trị mặc định của platform hoặc giá trị đã cấu hình) hoặc một giá trị số nguyên dương ít nhất là 32.768 (32 KiB). Nếu không chỉ định *size*, giá trị 0 sẽ được sử dụng. Nếu không hỗ trợ thay đổi kích thước stack của thread, một :exc:`RuntimeError` sẽ được raise. Nếu kích thước stack được chỉ định không hợp lệ, một :exc:`ValueError` sẽ được raise và kích thước stack không thay đổi. Hiện tại, 32 KiB là giá trị kích thước stack tối thiểu được hỗ trợ để bảo đảm đủ không gian stack cho chính interpreter. Lưu ý rằng một số platform có thể áp đặt các hạn chế cụ thể đối với giá trị kích thước stack, chẳng hạn yêu cầu kích thước stack tối thiểu > 32 KiB hoặc yêu cầu cấp phát theo bội số của kích thước trang bộ nhớ hệ thống — cần tham khảo tài liệu của platform để biết thêm thông tin (trang 4 KiB là phổ biến; khi không có thông tin cụ thể hơn, nên sử dụng các bội số của 4096 cho kích thước stack).

   .. availability:: Windows, pthreads.

      Các platform Unix hỗ trợ POSIX threads.


.. data:: TIMEOUT_MAX

   Giá trị tối đa được phép cho tham số *timeout* của
   :meth:`Lock.acquire <threading.Lock.acquire>`. Việc chỉ định thời gian chờ lớn hơn giá trị này sẽ phát sinh một :exc:`OverflowError`.

   .. versionadded:: 3.2


.. raw:: html

   <!-- Keep the old URL fragments working (see gh-89554) -->
   <span id='thread.lock.acquire'></span>
   <span id='thread.lock.release'></span>
   <span id='thread.lock.locked'></span>

.. class:: LockType

   Đây là kiểu của các đối tượng khóa.

   Các đối tượng khóa có những phương thức sau:

   .. method:: acquire(blocking=True, timeout=-1)

      Nếu không có đối số tùy chọn, phương thức này sẽ luôn lấy khóa, nếu cần thì chờ cho đến khi khóa được một thread khác giải phóng (mỗi lần chỉ một thread có thể lấy khóa — đó là lý do các khóa tồn tại).

      Nếu có đối số *blocking*, hành động sẽ phụ thuộc vào giá trị của nó: nếu giá trị là false, khóa chỉ được lấy nếu có thể lấy ngay mà không cần chờ; còn nếu giá trị là true, khóa sẽ luôn được lấy như trên.

      Nếu có đối số *timeout* dạng số thực và có giá trị dương, đối số này chỉ định thời gian chờ tối đa tính bằng giây trước khi trả về. Đối số *timeout* âm chỉ định thời gian chờ không giới hạn. Bạn không thể chỉ định *timeout* nếu *blocking* là false.

      Giá trị trả về là ``True`` nếu lấy khóa thành công, và là ``False`` nếu không thành công.

      .. versionchanged:: 3.2
         Tham số *timeout* là tham số mới.

      .. versionchanged:: 3.2
         Việc acquire lock hiện có thể bị gián đoạn bởi các signal trên POSIX.

      .. versionchanged:: 3.14
         Việc acquire lock hiện có thể bị gián đoạn bởi các signal trên Windows.

   .. method:: release()

      Giải phóng lock. Lock phải được acquire trước đó, nhưng không nhất thiết phải bởi cùng một thread.

   .. method:: locked()

      Trả về trạng thái của lock: ``True`` nếu lock đã được một thread nào đó acquire, ``False`` nếu chưa.

   Ngoài các phương thức này, các đối tượng lock cũng có thể được sử dụng thông qua
   :keyword:`with` câu lệnh, ví dụ::

      import _thread

      a_lock = _thread.allocate_lock()

      with a_lock:
          print("a_lock is locked while this executes")

**Lưu ý:**

.. index:: pair: module; signal

* Các ngắt luôn được gửi đến main thread (thread đó sẽ nhận được exception :exc:`KeyboardInterrupt`.)

* Việc gọi :func:`sys.exit` hoặc raise exception :exc:`SystemExit` tương đương với việc gọi :func:`_thread.exit`.

* Khi main thread thoát, việc các thread khác có tiếp tục hoạt động hay không là do hệ thống quyết định. Trên hầu hết các hệ thống, chúng bị kết thúc mà không thực thi
  :keyword:`try` ... :keyword:`finally` hoặc thực thi các object destructor.

