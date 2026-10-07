.. highlight:: c

.. _threads:

Trạng thái luồng và khóa trình thông dịch toàn cục
==================================================

.. index::
   single: global interpreter lock
   single: interpreter lock
   single: lock, interpreter

Trừ khi đang chạy trên một :term:`free-threaded build` của :term:`CPython`, trình thông dịch Python nhìn chung không an toàn với luồng. Để hỗ trợ các chương trình Python đa luồng, có một khóa toàn cục, được gọi là :term:`global interpreter lock` hoặc :term:`GIL`, mà một luồng phải nắm giữ trước khi truy cập các đối tượng Python. Nếu không có khóa này, ngay cả những thao tác đơn giản nhất cũng có thể gây ra sự cố trong một chương trình đa luồng: ví dụ, khi hai luồng đồng thời tăng số lượng tham chiếu của cùng một đối tượng, số lượng tham chiếu có thể cuối cùng chỉ được tăng một lần thay vì hai lần.

Do đó, chỉ luồng đang nắm giữ GIL mới có thể thao tác trên các đối tượng Python hoặc gọi Python's C API.

.. index:: single: setswitchinterval (in module sys)

Để mô phỏng tính đồng thời, trình thông dịch thường xuyên cố gắng chuyển đổi giữa các luồng ở ranh giới các chỉ thị bytecode (xem :func:`sys.setswitchinterval`). Đây là lý do các khóa cũng cần thiết để bảo đảm an toàn luồng trong mã Python thuần.

Ngoài ra, khóa trình thông dịch toàn cục được giải phóng trong khoảng thời gian thực hiện các thao tác I/O chặn, chẳng hạn như đọc hoặc ghi tệp. Trong C API, việc này được thực hiện bằng cách :ref:`tách trạng thái luồng <detaching-thread-state>`.


.. index::
   single: PyThreadState (C type)

Trình thông dịch Python lưu một số thông tin cục bộ theo luồng bên trong một cấu trúc dữ liệu có tên là :c:type:`PyThreadState`, được gọi là :term:`thread state`. Mỗi luồng có một con trỏ cục bộ theo luồng trỏ đến một :c:type:`PyThreadState`; trạng thái luồng được con trỏ này tham chiếu được xem là :term:`được gắn <attached thread state>`.

Mỗi lần một luồng chỉ có thể có một :term:`attached thread state`. Một trạng thái luồng được gắn thường tương đương với việc nắm giữ GIL, ngoại trừ trong các bản dựng free-threaded. Trên các bản dựng bật GIL, việc gắn trạng thái luồng sẽ chặn cho đến khi có thể giành được GIL. Tuy nhiên, ngay cả trên các bản dựng tắt GIL, vẫn cần có một trạng thái luồng được gắn, vì trình thông dịch cần theo dõi những luồng nào có thể truy cập các đối tượng Python.

.. note::

   Ngay cả trong bản build free-threaded, việc gắn trạng thái luồng cũng có thể bị chặn, vì GIL có thể được bật lại hoặc các luồng có thể tạm thời bị đình chỉ (chẳng hạn trong quá trình thu gom rác).

Nhìn chung, sẽ luôn có một trạng thái luồng được gắn khi sử dụng C API của Python, bao gồm cả trong quá trình nhúng và khi triển khai các phương thức, vì vậy hiếm khi bạn cần tự thiết lập trạng thái luồng. Chỉ trong một số trường hợp cụ thể, chẳng hạn như trong khối :c:macro:`Py_BEGIN_ALLOW_THREADS` hoặc trong một luồng mới, luồng mới không có trạng thái luồng được gắn. Nếu không chắc chắn, hãy kiểm tra xem :c:func:`PyThreadState_GetUnchecked` có trả về ``NULL`` hay không.

Nếu xác định rằng bạn cần tạo trạng thái luồng, hãy gọi :c:func:`PyThreadState_New` rồi gọi :c:func:`PyThreadState_Swap`, hoặc sử dụng hàm nguy hiểm
:c:func:`PyGILState_Ensure`.


.. _detaching-thread-state:

Tách trạng thái luồng khỏi mã extension
---------------------------------------

Hầu hết mã extension thao tác với :term:`thread state` đều có cấu trúc đơn giản sau đây::

   Save the thread state in a local variable.
   ... Do some blocking I/O operation ...
   Restore the thread state from the local variable.

Điều này phổ biến đến mức đã có một cặp macro để đơn giản hóa việc này::

   Py_BEGIN_ALLOW_THREADS
   ... Do some blocking I/O operation ...
   Py_END_ALLOW_THREADS

.. index::
   single: Py_BEGIN_ALLOW_THREADS (C macro)
   single: Py_END_ALLOW_THREADS (C macro)

Macro :c:macro:`Py_BEGIN_ALLOW_THREADS` mở một block mới và khai báo một biến cục bộ ẩn; macro :c:macro:`Py_END_ALLOW_THREADS` đóng block đó.

Block ở trên được mở rộng thành đoạn mã sau::

   PyThreadState *_save;

   _save = PyEval_SaveThread();
   ... Do some blocking I/O operation ...
   PyEval_RestoreThread(_save);

.. index::
   single: PyEval_RestoreThread (C function)
   single: PyEval_SaveThread (C function)

Các hàm này hoạt động như sau:

Thread state được gắn vào cho biết GIL đang được giữ cho interpreter. Để tách thread state, gọi :c:func:`PyEval_SaveThread` và lưu kết quả vào một biến cục bộ.

Việc tách thread state sẽ giải phóng GIL, cho phép các thread khác gắn vào interpreter và thực thi trong khi thread hiện tại thực hiện I/O chặn. Khi thao tác I/O hoàn tất, thread state cũ được gắn lại bằng cách gọi :c:func:`PyEval_RestoreThread`, hàm này sẽ chờ cho đến khi có thể lấy được GIL.

.. note::
   Thực hiện I/O chặn là trường hợp sử dụng phổ biến nhất của việc tách thread state, nhưng việc gọi nó trong đoạn mã native chạy lâu và không cần truy cập vào các đối tượng Python hoặc C API của Python cũng rất hữu ích. Ví dụ, các module chuẩn :mod:`zlib` và :mod:`hashlib` sẽ tách
   :term:`thread state <attached thread state>` khi nén hoặc băm dữ liệu.

Trên một :term:`free-threaded build`, :term:`GIL` thường là điều không thể thực hiện, nhưng **việc tách trạng thái luồng vẫn là bắt buộc**, vì trình thông dịch định kỳ cần chặn tất cả các luồng để có được chế độ xem nhất quán về các đối tượng Python mà không có nguy cơ xảy ra race condition. Ví dụ: CPython hiện tạm dừng tất cả các luồng trong một khoảng thời gian ngắn khi chạy trình thu gom rác.

.. warning::

   Việc tách trạng thái luồng có thể dẫn đến hành vi không mong muốn trong quá trình hoàn tất trình thông dịch. Xem :ref:`cautions-regarding-runtime-finalization` để biết thêm chi tiết.


APIs
^^^^

Các macro sau đây thường được sử dụng mà không có dấu chấm phẩy ở cuối; hãy tìm cách sử dụng mẫu trong bản phân phối mã nguồn Python.

.. note::

    Các macro này vẫn cần thiết trên :term:`free-threaded build` để ngăn deadlock.

.. c:macro:: Py_BEGIN_ALLOW_THREADS

   Macro này được mở rộng thành ``{ PyThreadState *_save; _save = PyEval_SaveThread();``. Lưu ý rằng macro này chứa một dấu ngoặc nhọn mở; nó phải được ghép với một macro tiếp theo
   :c:macro:`Py_END_ALLOW_THREADS`. Xem phần trên để biết thêm thảo luận về macro này.


.. c:macro:: Py_END_ALLOW_THREADS

   Macro này mở rộng thành ``PyEval_RestoreThread(_save); }``. Lưu ý rằng nó chứa một dấu ngoặc nhọn đóng; nó phải được ghép với một
   macro :c:macro:`Py_BEGIN_ALLOW_THREADS` trước đó. Xem phần trên để biết thêm về macro này.


.. c:macro:: Py_BLOCK_THREADS

   Macro này mở rộng thành ``PyEval_RestoreThread(_save);``: nó tương đương với
   :c:macro:`Py_END_ALLOW_THREADS` không có dấu ngoặc nhọn đóng.


.. c:macro:: Py_UNBLOCK_THREADS

   Macro này mở rộng thành ``_save = PyEval_SaveThread();``: nó tương đương với
   :c:macro:`Py_BEGIN_ALLOW_THREADS` không có dấu ngoặc nhọn mở và phần khai báo biến.


Các thread được tạo không phải bằng Python
------------------------------------------

Khi các thread được tạo bằng các Python API chuyên dụng (chẳng hạn như
:mod:`threading` module), một trạng thái thread sẽ tự động được liên kết với chúng. Tuy nhiên, khi một thread được tạo từ mã native (ví dụ: bởi một thư viện bên thứ ba có cơ chế quản lý thread riêng), thread đó không có trạng thái thread được đính kèm.

Nếu cần gọi mã Python từ các thread này (thường đây sẽ là một phần của callback API do thư viện bên thứ ba nói trên cung cấp), trước tiên bạn phải đăng ký các thread này với interpreter bằng cách tạo một trạng thái thread mới và đính kèm trạng thái đó.

Cách đáng tin cậy nhất để thực hiện việc này là thông qua :c:func:`PyThreadState_New` rồi đến :c:func:`PyThreadState_Swap`.

.. note::
   ``PyThreadState_New`` yêu cầu một đối số trỏ đến interpreter mong muốn; bạn có thể lấy con trỏ này bằng cách gọi
   :c:func:`PyInterpreterState_Get` từ mã nơi thread được tạo.

Ví dụ::

   /* The return value of PyInterpreterState_Get() from the
      function that created this thread. */
   PyInterpreterState *interp = thread_data->interp;

   /* Create a new thread state for the interpreter. It does not start out
      attached. */
   PyThreadState *tstate = PyThreadState_New(interp);

   /* Attach the thread state, which will acquire the GIL. */
   PyThreadState_Swap(tstate);

   /* Perform Python actions here. */
   result = CallSomeFunction();
   /* evaluate result or handle exception */

   /* Destroy the thread state. No Python API allowed beyond this point. */
   PyThreadState_Clear(tstate);
   PyThreadState_DeleteCurrent();

.. warning::

   Nếu interpreter hoàn tất trước khi ``PyThreadState_Swap`` được gọi, thì ``interp`` sẽ là một dangling pointer!

.. _gilstate:

API cũ
------

Một mẫu phổ biến khác để gọi mã Python từ một thread không phải Python là sử dụng
:c:func:`PyGILState_Ensure` rồi gọi :c:func:`PyGILState_Release`.

Các hàm này không hoạt động tốt khi có nhiều interpreter trong tiến trình Python. Nếu chưa từng có interpreter Python nào được sử dụng trong thread hiện tại (điều thường xảy ra với các thread được tạo bên ngoài Python), ``PyGILState_Ensure`` sẽ tạo và gắn một thread state cho interpreter "main" (interpreter đầu tiên trong tiến trình Python).

Ngoài ra, các hàm này có vấn đề về thread-safety trong quá trình hoàn tất interpreter. Việc sử dụng ``PyGILState_Ensure`` trong quá trình hoàn tất có khả năng cao sẽ khiến tiến trình bị crash.

Cách sử dụng các hàm này như sau::

   PyGILState_STATE gstate;
   gstate = PyGILState_Ensure();

   /* Perform Python actions here. */
   result = CallSomeFunction();
   /* evaluate result or handle exception */

   /* Release the thread. No Python API allowed beyond this point. */
   PyGILState_Release(gstate);


.. _fork-and-threads:

Lưu ý về fork()
---------------

Một điều quan trọng khác cần lưu ý về các thread là hành vi của chúng khi gặp lời gọi :c:func:`fork` trong C. Trên hầu hết các hệ thống có :c:func:`fork`, sau khi một process fork, chỉ thread thực hiện fork còn tồn tại. Điều này ảnh hưởng cụ thể đến cả cách phải xử lý các lock và toàn bộ trạng thái được lưu trong runtime của CPython.

Việc chỉ còn lại thread "hiện tại" có nghĩa là mọi lock do các thread khác nắm giữ sẽ không bao giờ được giải phóng. Python xử lý việc này cho :func:`os.fork` bằng cách lấy các lock mà nó sử dụng nội bộ trước khi fork và giải phóng chúng sau đó. Ngoài ra, nó đặt lại mọi
:ref:`lock-objects` trong child. Khi mở rộng hoặc nhúng Python, không có cách nào thông báo cho Python về các lock bổ sung (không thuộc Python) cần được lấy trước fork hoặc đặt lại sau fork. Các cơ chế của hệ điều hành như
:c:func:`!pthread_atfork` cần được sử dụng để thực hiện điều tương tự. Ngoài ra, khi mở rộng hoặc nhúng Python, việc gọi trực tiếp :c:func:`fork` thay vì thông qua :func:`os.fork` (và quay lại Python hoặc gọi vào Python) có thể dẫn đến deadlock do một trong các lock nội bộ của Python đang bị một thread đã không còn tồn tại sau fork nắm giữ.
:c:func:`PyOS_AfterFork_Child` cố gắng đặt lại các lock cần thiết, nhưng không phải lúc nào cũng làm được.

Việc tất cả các thread khác biến mất cũng có nghĩa là trạng thái runtime của CPython tại đó phải được dọn dẹp đúng cách, và :func:`os.fork` thực hiện việc này. Điều đó có nghĩa là hoàn tất việc xử lý tất cả các đối tượng :c:type:`PyThreadState` khác thuộc về interpreter hiện tại và tất cả các
Các đối tượng :c:type:`PyInterpreterState`. Do đó và do tính chất đặc biệt của trình thông dịch :ref:`"main" trình thông dịch <sub-interpreter-support>`,
:c:func:`fork` chỉ nên được gọi trong luồng "main" của trình thông dịch đó, nơi runtime toàn cục của CPython được khởi tạo ban đầu. Ngoại lệ duy nhất là nếu :c:func:`exec` sẽ được gọi ngay sau đó.


API cấp cao
-----------

Đây là các kiểu và hàm được sử dụng phổ biến nhất khi viết các extension C đa luồng.


.. c:type:: PyThreadState

   Cấu trúc dữ liệu này biểu diễn trạng thái của một luồng đơn. Thành viên dữ liệu công khai duy nhất là:

   .. c:member:: PyInterpreterState *interp

      Trạng thái trình thông dịch của luồng này.


.. c:function:: void PyEval_InitThreads()

   .. index::
      single: PyEval_AcquireThread()
      single: PyEval_ReleaseThread()
      single: PyEval_SaveThread()
      single: PyEval_RestoreThread()

   Hàm đã lỗi thời và không thực hiện tác vụ nào.

   Trong Python 3.6 trở về trước, hàm này đã tạo GIL nếu nó chưa tồn tại.

   .. versionchanged:: 3.9
      Hiện hàm này không thực hiện thao tác nào.

   .. versionchanged:: 3.7
      Hiện hàm này được :c:func:`Py_Initialize()` gọi, vì vậy bạn không còn phải tự gọi nó nữa.

   .. versionchanged:: 3.2
      Hiện không thể gọi hàm này trước :c:func:`Py_Initialize()` nữa.

   .. deprecated:: 3.9

   .. index:: pair: module; _thread


.. c:function:: PyThreadState* PyEval_SaveThread()

   Tách :term:`attached thread state` và trả về nó. Khi trả về, thread sẽ không có :term:`thread state`.


.. c:function:: void PyEval_RestoreThread(PyThreadState *tstate)

   Đặt :term:`attached thread state` thành *tstate*. :term:`thread state` được truyền vào **không được** :term:`gắn <attached thread state>`, nếu không sẽ xảy ra deadlock. *tstate* sẽ được gắn khi trả về.

   .. note::
      Gọi hàm này từ một thread khi runtime đang trong quá trình kết thúc sẽ khiến thread bị treo cho đến khi chương trình thoát, ngay cả khi thread đó không được Python tạo. Hãy tham khảo
      :ref:`cautions-regarding-runtime-finalization` để biết thêm chi tiết.

   .. versionchanged:: 3.14
      Tạm dừng thread hiện tại thay vì kết thúc thread đó nếu được gọi khi interpreter đang hoàn tất quá trình finalization.

.. c:function:: PyThreadState* PyThreadState_Get()

   Trả về :term:`attached thread state`. Nếu thread không có thread state được đính kèm (chẳng hạn như khi đang ở trong block :c:macro:`Py_BEGIN_ALLOW_THREADS`), thao tác này sẽ phát sinh lỗi nghiêm trọng (fatal error), do đó caller không cần kiểm tra ``NULL``.

   Xem thêm :c:func:`PyThreadState_GetUnchecked`.

.. c:function:: PyThreadState* PyThreadState_GetUnchecked()

   Tương tự :c:func:`PyThreadState_Get`, nhưng không kết thúc process bằng lỗi nghiêm trọng nếu giá trị đó là NULL. Caller có trách nhiệm kiểm tra xem kết quả có phải là NULL hay không.

   .. versionadded:: 3.13
      Trong Python 3.5 đến 3.12, hàm này là private và được biết đến với tên ``_PyThreadState_UncheckedGet()``.


.. c:function:: PyThreadState* PyThreadState_Swap(PyThreadState *tstate)

   Đặt :term:`attached thread state` thành *tstate*, rồi trả về
   :term:`thread state` đã được gắn trước khi gọi.

   Có thể gọi hàm này một cách an toàn mà không cần :term:`attached thread state`; hàm sẽ chỉ trả về ``NULL``, cho biết không có trạng thái thread trước đó.

   .. seealso::
      :c:func:`PyEval_ReleaseThread`

   .. note::
      Tương tự như :c:func:`PyGILState_Ensure`, hàm này sẽ khiến thread bị treo nếu runtime đang trong quá trình kết thúc.


API trạng thái GIL
------------------

Các hàm sau sử dụng bộ nhớ lưu trữ cục bộ của thread và không tương thích với sub-interpreter:

.. c:type:: PyGILState_STATE

   Kiểu của giá trị được :c:func:`PyGILState_Ensure` trả về và được truyền cho
   :c:func:`PyGILState_Release`.

   .. c:enumerator:: PyGILState_LOCKED

      GIL đã được giữ khi :c:func:`PyGILState_Ensure` được gọi.

   .. c:enumerator:: PyGILState_UNLOCKED

      GIL không được giữ khi :c:func:`PyGILState_Ensure` được gọi.

.. c:function:: PyGILState_STATE PyGILState_Ensure()

   Đảm bảo rằng luồng hiện tại đã sẵn sàng gọi Python C API bất kể trạng thái hiện tại của Python hoặc của :term:`attached thread state`. Một luồng có thể gọi hàm này bao nhiêu lần tùy ý, miễn là mỗi lần gọi đều đi kèm một lần gọi :c:func:`PyGILState_Release`. Nhìn chung, có thể sử dụng các API liên quan đến luồng khác giữa :c:func:`PyGILState_Ensure` và
   các lần gọi :c:func:`PyGILState_Release`, miễn là trạng thái luồng được khôi phục về trạng thái trước đó trước khi gọi Release().  Ví dụ, cách sử dụng thông thường của các macro
   :c:macro:`Py_BEGIN_ALLOW_THREADS` và :c:macro:`Py_END_ALLOW_THREADS` là hợp lệ.

   Giá trị trả về là một "handle" không trong suốt tới :term:`attached thread state` khi
   :c:func:`PyGILState_Ensure` được gọi và phải được truyền vào
   :c:func:`PyGILState_Release` để đảm bảo Python được giữ ở cùng trạng thái. Mặc dù cho phép các lần gọi đệ quy, các handle này *không thể* được chia sẻ - mỗi lần gọi riêng biệt tới :c:func:`PyGILState_Ensure` phải lưu handle cho lần gọi :c:func:`PyGILState_Release` tương ứng.

   Khi hàm trả về, sẽ có một :term:`attached thread state` và thread sẽ có thể gọi mã Python tùy ý. Lỗi này là lỗi nghiêm trọng.

   .. warning::
      Việc gọi hàm này khi runtime đang trong quá trình kết thúc là không an toàn. Làm như vậy sẽ khiến thread bị treo cho đến khi chương trình kết thúc hoặc, trong một số trường hợp hiếm, khiến interpreter bị crash hoàn toàn. Tham khảo
      :ref:`cautions-regarding-runtime-finalization` để biết thêm chi tiết.

   .. versionchanged:: 3.14
      Treo thread hiện tại thay vì kết thúc thread đó nếu được gọi trong khi interpreter đang trong quá trình kết thúc.

.. c:function:: void PyGILState_Release(PyGILState_STATE)

   Giải phóng mọi tài nguyên đã được thu nhận trước đó. Sau lời gọi này, trạng thái của Python sẽ giống như trước lời gọi :c:func:`PyGILState_Ensure` tương ứng (nhưng nhìn chung trạng thái này sẽ không được bên gọi biết, do đó cần sử dụng GILState API).

   Mỗi lời gọi đến :c:func:`PyGILState_Ensure` phải tương ứng với một lời gọi đến
   :c:func:`PyGILState_Release` trên cùng thread.

.. c:function:: PyThreadState* PyGILState_GetThisThreadState()

   Lấy :term:`attached thread state` cho thread này. Có thể trả về ``NULL`` nếu chưa sử dụng API GILState nào trên thread hiện tại. Lưu ý rằng thread chính luôn có thread-state như vậy, ngay cả khi chưa thực hiện lệnh gọi auto-thread-state nào trên thread chính. Đây chủ yếu là một hàm trợ giúp/chẩn đoán.

   .. note::
      Hàm này có thể trả về giá trị khác ``NULL`` ngay cả khi :term:`thread state` được tách rời. Trong hầu hết trường hợp, hãy ưu tiên :c:func:`PyThreadState_Get` hoặc :c:func:`PyThreadState_GetUnchecked`.

   .. seealso:: :c:func:`PyThreadState_Get`

.. c:function:: int PyGILState_Check()

   Trả về ``1`` nếu thread hiện tại đang giữ :term:`GIL` và ``0`` trong trường hợp ngược lại. Có thể gọi hàm này từ bất kỳ thread nào vào bất kỳ thời điểm nào. Chỉ khi :term:`trạng thái thread <attached thread state>` của thread đó đã được khởi tạo thông qua :c:func:`PyGILState_Ensure` thì hàm mới trả về ``1``. Đây chủ yếu là một hàm trợ giúp/chẩn đoán. Ví dụ, hàm này có thể hữu ích trong các ngữ cảnh callback hoặc các hàm cấp phát bộ nhớ, khi việc biết rằng :term:`GIL` đang bị khóa cho phép caller thực hiện các hành động nhạy cảm hoặc ứng xử khác đi.

   .. note::
      Nếu tiến trình Python hiện tại đã từng tạo một subinterpreter, hàm này *luôn* trả về ``1``. Trong hầu hết trường hợp, hãy ưu tiên :c:func:`PyThreadState_GetUnchecked`.

   .. versionadded:: 3.4


API cấp thấp
------------

.. c:function:: PyThreadState* PyThreadState_New(PyInterpreterState *interp)

   Tạo một đối tượng thread state mới thuộc về đối tượng interpreter đã cho. Không cần có :term:`attached thread state`.

.. c:function:: void PyThreadState_Clear(PyThreadState *tstate)

   Đặt lại toàn bộ thông tin trong một đối tượng :term:`thread state`. *tstate* phải :term:`được gắn <attached thread state>`

   .. versionchanged:: 3.9
      Hàm này hiện gọi callback :c:member:`!PyThreadState.on_delete`. Trước đây, việc đó xảy ra trong :c:func:`PyThreadState_Delete`.

   .. versionchanged:: 3.13
      Callback :c:member:`!PyThreadState.on_delete` đã bị loại bỏ.


.. c:function:: void PyThreadState_Delete(PyThreadState *tstate)

   Hủy đối tượng :term:`thread state`. *tstate* không được :term:`gắn <attached thread state>` vào bất kỳ thread nào. *tstate* phải đã được reset bằng một lệnh gọi trước đó tới
   :c:func:`PyThreadState_Clear`.


.. c:function:: void PyThreadState_DeleteCurrent(void)

   Tách :term:`attached thread state` (đối tượng này phải đã được reset bằng một lệnh gọi trước đó tới :c:func:`PyThreadState_Clear`) rồi hủy nó.

   Không có :term:`thread state` nào được :term:`gắn <attached thread state>` khi trả về.

.. c:function:: PyFrameObject* PyThreadState_GetFrame(PyThreadState *tstate)

   Lấy frame hiện tại của trạng thái thread Python *tstate*.

   Trả về một :term:`strong reference`. Trả về ``NULL`` nếu hiện không có frame nào đang được thực thi.

   Xem thêm :c:func:`PyEval_GetFrame`.

   *tstate* không được ``NULL``, và phải được :term:`gắn <attached thread state>`.

   .. versionadded:: 3.9


.. c:function:: uint64_t PyThreadState_GetID(PyThreadState *tstate)

   Lấy mã định danh duy nhất :term:`thread state` của trạng thái luồng Python *tstate*.

   *tstate* không được ``NULL``, và phải được :term:`gắn <attached thread state>`.

   .. versionadded:: 3.9


.. c:function:: PyInterpreterState* PyThreadState_GetInterpreter(PyThreadState *tstate)

   Lấy interpreter của trạng thái luồng Python *tstate*.

   *tstate* không được ``NULL``, và phải được :term:`gắn <attached thread state>`.

   .. versionadded:: 3.9


.. c:function:: void PyThreadState_EnterTracing(PyThreadState *tstate)

   Tạm dừng tracing và profiling trong trạng thái luồng Python *tstate*.

   Tiếp tục chúng bằng hàm :c:func:`PyThreadState_LeaveTracing`.

   .. versionadded:: 3.11


.. c:function:: void PyThreadState_LeaveTracing(PyThreadState *tstate)

   Tiếp tục tracing và profiling trong trạng thái luồng Python *tstate* bị tạm dừng bởi hàm :c:func:`PyThreadState_EnterTracing`.

   Xem thêm các hàm :c:func:`PyEval_SetTrace` và :c:func:`PyEval_SetProfile`.

   .. versionadded:: 3.11


.. c:function:: int PyUnstable_ThreadState_SetStackProtection(PyThreadState *tstate, void *stack_start_addr, size_t stack_size)

   Thiết lập địa chỉ bắt đầu bảo vệ ngăn xếp và kích thước bảo vệ ngăn xếp của một trạng thái luồng Python.

   Khi thành công, trả về ``0``. Khi thất bại, đặt một exception và trả về ``-1``.

   CPython triển khai :ref:`recursion control <recursion>` cho mã C bằng cách phát sinh
   :py:exc:`RecursionError` khi nhận thấy ngăn xếp thực thi của máy sắp bị tràn. Xem ví dụ về hàm :c:func:`Py_EnterRecursiveCall`. Để thực hiện việc này, nó cần biết vị trí ngăn xếp của luồng hiện tại, thông tin mà nó thường lấy từ hệ điều hành. Khi ngăn xếp bị thay đổi, chẳng hạn bằng các kỹ thuật chuyển đổi ngữ cảnh như ``boost::context`` của thư viện Boost, bạn phải gọi
   :c:func:`~PyUnstable_ThreadState_SetStackProtection` để thông báo cho CPython về thay đổi.

   Gọi :c:func:`~PyUnstable_ThreadState_SetStackProtection` trước hoặc sau khi thay đổi stack. Không gọi bất kỳ Python C API nào khác giữa lúc gọi và lúc thay đổi stack.

   Xem :c:func:`PyUnstable_ThreadState_ResetStackProtection` để hoàn tác thao tác này.

   .. versionadded:: 3.15


.. c:function:: void PyUnstable_ThreadState_ResetStackProtection(PyThreadState *tstate)

   Đặt lại địa chỉ bắt đầu bảo vệ stack và kích thước bảo vệ stack của trạng thái thread Python về các giá trị mặc định của hệ điều hành.

   Xem :c:func:`PyUnstable_ThreadState_SetStackProtection` để biết thêm giải thích.

   .. versionadded:: 3.15


.. c:function:: PyObject* PyThreadState_GetDict()

   Trả về một từ điển để các extension lưu trữ thông tin trạng thái dành riêng cho thread. Mỗi extension nên sử dụng một khóa duy nhất để lưu trạng thái trong từ điển. Có thể gọi hàm này khi không có :term:`thread state` nào được :term:`đính kèm <attached thread state>`. Nếu hàm này trả về ``NULL``, không có ngoại lệ nào được phát sinh và bên gọi nên giả định rằng không có trạng thái thread nào được đính kèm.


.. c:function:: void PyEval_AcquireThread(PyThreadState *tstate)

   :term:`Gắn <attached thread state>` *tstate* vào thread hiện tại, thread này không được là ``NULL`` hoặc đã được :term:`đính kèm <attached thread state>`.

   Luồng gọi không được có sẵn một :term:`attached thread state`.

   .. note::
      Việc gọi hàm này từ một luồng khi runtime đang hoàn tất sẽ khiến luồng bị treo cho đến khi chương trình thoát, ngay cả khi luồng đó không được Python tạo. Hãy tham khảo
      :ref:`cautions-regarding-runtime-finalization` để biết thêm chi tiết.

   .. versionchanged:: 3.8
      Đã được cập nhật để nhất quán với :c:func:`PyEval_RestoreThread`,
      :c:func:`Py_END_ALLOW_THREADS` và :c:func:`PyGILState_Ensure`, đồng thời chấm dứt luồng hiện tại nếu được gọi khi interpreter đang hoàn tất.

   .. versionchanged:: 3.14
      Khi được gọi trong lúc interpreter đang hoàn tất, hàm này sẽ làm luồng hiện tại bị treo thay vì chấm dứt luồng.

   :c:func:`PyEval_RestoreThread` là một hàm cấp cao hơn, luôn khả dụng (ngay cả khi các luồng chưa được khởi tạo).


.. c:function:: void PyEval_ReleaseThread(PyThreadState *tstate)

   Tách :term:`attached thread state`. Đối số *tstate*, không được là ``NULL``, chỉ được dùng để kiểm tra rằng nó đại diện cho :term:`attached thread state` --- nếu không phải, một lỗi nghiêm trọng sẽ được báo cáo.

   :c:func:`PyEval_SaveThread` là một hàm cấp cao hơn, luôn khả dụng (ngay cả khi các thread chưa được khởi tạo).


Thông báo bất đồng bộ
=====================

Một cơ chế được cung cấp để gửi thông báo bất đồng bộ đến thread trình thông dịch chính. Các thông báo này có dạng một con trỏ hàm và một đối số con trỏ void.


.. c:function:: int Py_AddPendingCall(int (*func)(void *), void *arg)

   Lên lịch một hàm để được gọi từ thread trình thông dịch chính. Khi thành công, ``0`` được trả về và *func* được xếp hàng để được gọi trong thread chính. Khi thất bại, ``-1`` được trả về mà không đặt bất kỳ exception nào.

   Khi được xếp hàng thành công, *func* sẽ *eventually* được gọi từ thread trình thông dịch chính với đối số *arg*. Hàm sẽ được gọi bất đồng bộ so với mã Python đang chạy bình thường, nhưng đồng thời phải đáp ứng cả hai điều kiện sau:

   * tại một ranh giới :term:`bytecode`;
   * với main thread đang giữ một :term:`attached thread state` (*func* do đó có thể sử dụng toàn bộ C API).

   *func* phải trả về ``0`` khi thành công hoặc ``-1`` khi thất bại và đã thiết lập một exception.  *func* sẽ không bị gián đoạn để thực hiện đệ quy một asynchronous notification khác, nhưng vẫn có thể bị gián đoạn để chuyển thread nếu trạng thái :term:`thread state <attached thread state>` đã được tách.

   Hàm này không cần một :term:`attached thread state`. Tuy nhiên, để gọi hàm này trong một subinterpreter, caller phải có một :term:`attached thread state`. Nếu không, hàm *func* có thể được lên lịch gọi từ interpreter không đúng.

   .. warning::
      Đây là một hàm cấp thấp, chỉ hữu ích trong những trường hợp rất đặc biệt. Không có gì đảm bảo rằng *func* sẽ được gọi nhanh nhất có thể.  Nếu main thread đang bận thực thi một system call, *func* sẽ không được gọi trước khi system call đó trả về.  Nhìn chung, hàm này **not** phù hợp để gọi mã Python từ các C thread tùy ý.  Thay vào đó, hãy sử dụng :ref:`PyGILState API <gilstate>`.

   .. versionadded:: 3.1

   .. versionchanged:: 3.9
      Nếu hàm này được gọi trong một subinterpreter, hàm *func* sẽ được lên lịch gọi từ subinterpreter đó thay vì từ main interpreter. Mỗi subinterpreter hiện có danh sách các lệnh gọi đã lên lịch riêng.

   .. versionchanged:: 3.12
      Hàm này hiện luôn lên lịch để *func* được chạy trong main interpreter.


.. c:function:: int Py_MakePendingCalls(void)

   Thực thi tất cả các lệnh gọi đang chờ. Thông thường, interpreter sẽ tự động thực hiện việc này.

   Hàm này trả về ``0`` khi thành công và trả về ``-1`` khi thất bại, đồng thời thiết lập một exception.

   Nếu hàm này không được gọi trong thread chính của interpreter chính, hàm sẽ không thực hiện gì và trả về ``0``. Caller phải giữ một :term:`attached thread state`.

   .. versionadded:: 3.1

   .. versionchanged:: 3.12
      Hàm này chỉ chạy các lời gọi đang chờ xử lý trong interpreter chính.


.. c:function:: int PyThreadState_SetAsyncExc(unsigned long id, PyObject *exc)

   Nâng một ngoại lệ trong một thread theo cách bất đồng bộ. Đối số *id* là ID của thread đích; *exc* là đối tượng ngoại lệ cần được nâng lên. Hàm này không :term:`steal` giữ lại bất kỳ tham chiếu nào đến *exc*. Để ngăn việc sử dụng sai một cách ngây thơ, bạn phải tự viết một C extension để gọi hàm này. Phải được gọi với một :term:`attached thread state`. Trả về số lượng thread state đã được sửa đổi; thông thường là một, nhưng sẽ là không nếu không tìm thấy thread ID. Nếu *exc* là ``NULL``, ngoại lệ đang chờ xử lý (nếu có) của thread sẽ được xóa. Hàm này không phát sinh ngoại lệ nào.

   .. versionchanged:: 3.7
      Kiểu của tham số *id* đã thay đổi từ :c:expr:`long` thành
      :c:expr:`unsigned long`.


API thread của hệ điều hành
===========================

.. c:macro:: PYTHREAD_INVALID_THREAD_ID

   Giá trị sentinel cho thread ID không hợp lệ.

   Hiện tại, điều này tương đương với ``(unsigned long)-1``.


.. c:function:: unsigned long PyThread_start_new_thread(void (*func)(void *), void *arg)

   Bắt đầu hàm *func* trong một thread mới với đối số *arg*. Thread được tạo ra không предназначен để được join.

   *func* không được là ``NULL``, nhưng *arg* có thể là ``NULL``.

   Khi thành công, hàm này trả về mã định danh của thread mới; khi thất bại, hàm trả về :c:macro:`PYTHREAD_INVALID_THREAD_ID`.

   Bên gọi không cần phải nắm giữ một :term:`attached thread state`.


.. c:function:: unsigned long PyThread_get_thread_ident(void)

   Trả về mã định danh của thread hiện tại, mã này sẽ không bao giờ bằng 0.

   Hàm này không thể thất bại và bên gọi không cần phải nắm giữ một
   :term:`attached thread state`.

   .. seealso::
      :py:func:`threading.get_ident`


.. c:function:: PyObject *PyThread_GetInfo(void)

   Nhận thông tin chung về thread hiện tại dưới dạng một
   :ref:`struct sequence <struct-sequence-objects>` object. Có thể truy cập thông tin này dưới dạng :py:attr:`sys.thread_info` trong Python.

   Khi thành công, hàm này trả về một :term:`strong reference` tới thông tin thread; khi thất bại, hàm trả về ``NULL`` với một exception đã được thiết lập.

   Caller phải nắm giữ một :term:`attached thread state`.


.. c:macro:: PY_HAVE_THREAD_NATIVE_ID

   Macro này được định nghĩa khi hệ thống hỗ trợ native thread ID.


.. c:function:: unsigned long PyThread_get_thread_native_id(void)

   Lấy native identifier của thread hiện tại theo giá trị do kernel của hệ điều hành gán, giá trị này sẽ không bao giờ nhỏ hơn 0.

   Hàm này chỉ khả dụng khi :c:macro:`PY_HAVE_THREAD_NATIVE_ID` được định nghĩa.

   Hàm này không thể thất bại và bên gọi không cần phải nắm giữ một
   :term:`attached thread state`.

   .. seealso::
      :py:func:`threading.get_native_id`


.. c:function:: void PyThread_exit_thread(void)

   Chấm dứt luồng hiện tại. Hàm này thường được xem là không an toàn và nên tránh sử dụng. Hàm này chỉ được giữ lại để đảm bảo khả năng tương thích ngược.

   Hàm này chỉ an toàn khi gọi nếu tất cả các hàm trong toàn bộ call stack được viết để cho phép việc đó một cách an toàn.

   .. warning::

      Nếu hệ thống hiện tại sử dụng các luồng POSIX (còn được gọi là "pthreads"), hàm này gọi :manpage:`pthread_exit(3)`, hàm này cố gắng unwind stack và gọi các destructor C++ trên một số implementation của libc. Tuy nhiên, nếu gặp một hàm ``noexcept``, hàm đó có thể chấm dứt process. Các hệ thống khác, chẳng hạn như macOS, thực hiện unwinding.

      Trên Windows, hàm này gọi ``_endthreadex()``, hàm này kết thúc luồng mà không gọi các destructor C++.

      Trong mọi trường hợp, stack của luồng có nguy cơ bị hỏng.

   .. deprecated:: 3.14


.. c:function:: void PyThread_init_thread(void)

   Khởi tạo các API ``PyThread*``. Python tự động thực thi hàm này, vì vậy extension module hầu như không cần gọi hàm này.


.. c:function:: int PyThread_set_stacksize(size_t size)

   Đặt kích thước ngăn xếp của thread hiện tại thành *size* byte.

   Hàm này trả về ``0`` khi thành công, ``-1`` nếu *size* không hợp lệ hoặc ``-2`` nếu hệ thống không hỗ trợ thay đổi kích thước ngăn xếp. Hàm này không thiết lập exception.

   Bên gọi không cần phải nắm giữ một :term:`attached thread state`.


.. c:function:: size_t PyThread_get_stacksize(void)

   Trả về kích thước ngăn xếp của thread hiện tại tính bằng byte hoặc ``0`` nếu đang sử dụng kích thước ngăn xếp mặc định của hệ thống.

   Bên gọi không cần phải nắm giữ một :term:`attached thread state`.
