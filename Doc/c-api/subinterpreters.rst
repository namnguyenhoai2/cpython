.. highlight:: c

.. _sub-interpreter-support:

Nhiều trình thông dịch trong một tiến trình Python
==================================================

Mặc dù trong hầu hết trường hợp sử dụng, bạn chỉ nhúng một trình thông dịch Python, vẫn có những trường hợp bạn cần tạo nhiều trình thông dịch độc lập trong cùng một tiến trình và thậm chí có thể trong cùng một thread. Các trình thông dịch con cho phép bạn thực hiện điều đó.

Trình thông dịch "chính" là trình thông dịch đầu tiên được tạo khi runtime khởi tạo. Thông thường, đây là trình thông dịch Python duy nhất trong một tiến trình. Không giống các trình thông dịch con, trình thông dịch chính có những trách nhiệm duy nhất ở cấp độ toàn tiến trình, chẳng hạn như xử lý tín hiệu. Trình thông dịch này cũng chịu trách nhiệm thực thi trong quá trình khởi tạo runtime và thường là trình thông dịch đang hoạt động trong quá trình hoàn tất runtime.
Hàm :c:func:`PyInterpreterState_Main` trả về một con trỏ đến trạng thái của nó.

Bạn có thể chuyển đổi giữa các trình thông dịch con bằng hàm :c:func:`PyThreadState_Swap`. Bạn có thể tạo và hủy chúng bằng các hàm sau:


.. c:type:: PyInterpreterConfig

   Cấu trúc chứa hầu hết các tham số để cấu hình một trình thông dịch con. Các giá trị của cấu trúc chỉ được sử dụng trong :c:func:`Py_NewInterpreterFromConfig` và không bao giờ bị runtime sửa đổi.

   .. versionadded:: 3.12

   Các trường của cấu trúc:

   .. c:member:: int use_main_obmalloc

      Nếu giá trị này là ``0`` thì sub-interpreter sẽ sử dụng trạng thái bộ cấp phát "object" riêng của nó. Nếu không, nó sẽ sử dụng (chia sẻ) trạng thái của interpreter chính.

      Nếu giá trị này là ``0`` thì
      :c:member:`~PyInterpreterConfig.check_multi_interp_extensions` phải là ``1`` (khác không). Nếu giá trị này là ``1`` thì :c:member:`~PyInterpreterConfig.gil` không được là :c:macro:`PyInterpreterConfig_OWN_GIL`.

   .. c:member:: int allow_fork

      Nếu giá trị này là ``0`` thì runtime sẽ không hỗ trợ fork process trong bất kỳ thread nào mà sub-interpreter hiện đang hoạt động. Nếu không, fork không bị hạn chế.

      Lưu ý rằng module :mod:`subprocess` vẫn hoạt động khi fork bị vô hiệu hóa.

   .. c:member:: int allow_exec

      Nếu giá trị này là ``0`` thì runtime sẽ không hỗ trợ thay thế process hiện tại bằng exec (ví dụ: :func:`os.execv`) trong bất kỳ thread nào mà sub-interpreter hiện đang hoạt động. Nếu không, exec không bị hạn chế.

      Lưu ý rằng module :mod:`subprocess` vẫn hoạt động khi exec bị vô hiệu hóa.

   .. c:member:: int allow_threads

      Nếu giá trị này là ``0`` thì mô-đun :mod:`threading` của trình thông dịch con sẽ không tạo thread. Nếu không, thread được phép tạo.

   .. c:member:: int allow_daemon_threads

      Nếu giá trị này là ``0`` thì mô-đun :mod:`threading` của trình thông dịch con sẽ không tạo daemon thread. Nếu không, daemon thread được phép tạo (miễn là
      :c:member:`~PyInterpreterConfig.allow_threads` khác không).

   .. c:member:: int check_multi_interp_extensions

      Nếu giá trị này là ``0`` thì mọi mô-đun mở rộng đều có thể được import, bao gồm các mô-đun legacy (khởi tạo single-phase), trong bất kỳ thread nào mà trình thông dịch con hiện đang hoạt động. Nếu không, chỉ các mô-đun mở rộng khởi tạo multi-phase (xem :pep:`489`) mới có thể được import. (Cũng xem :c:macro:`Py_mod_multiple_interpreters`.)

      Giá trị này phải là ``1`` (khác không) nếu
      :c:member:`~PyInterpreterConfig.use_main_obmalloc` là ``0``.

   .. c:member:: int gil

      Điều này xác định cách GIL hoạt động đối với trình thông dịch con. Giá trị có thể là một trong các giá trị sau:

      .. c:namespace:: NULL

      .. c:macro:: PyInterpreterConfig_DEFAULT_GIL

         Sử dụng lựa chọn mặc định (:c:macro:`PyInterpreterConfig_SHARED_GIL`).

      .. c:macro:: PyInterpreterConfig_SHARED_GIL

         Sử dụng GIL của interpreter chính (share).

      .. c:macro:: PyInterpreterConfig_OWN_GIL

         Sử dụng GIL riêng của sub-interpreter.

      Nếu đây là :c:macro:`PyInterpreterConfig_OWN_GIL` thì
      :c:member:`PyInterpreterConfig.use_main_obmalloc` phải là ``0``.


.. c:function:: PyStatus Py_NewInterpreterFromConfig(PyThreadState **tstate_p, const PyInterpreterConfig *config)

   .. index::
      pair: module; builtins
      pair: module; __main__
      pair: module; sys
      single: stdout (in module sys)
      single: stderr (in module sys)
      single: stdin (in module sys)

   Tạo một sub-interpreter mới. Đây là một môi trường (gần như) hoàn toàn tách biệt để thực thi mã Python. Cụ thể, interpreter mới có các phiên bản riêng biệt và độc lập của tất cả module đã import, bao gồm các module cơ bản :mod:`builtins`, :mod:`__main__` và :mod:`sys`. Bảng các module đã tải (``sys.modules``) và đường dẫn tìm kiếm module (``sys.path``) cũng riêng biệt. Môi trường mới không có biến ``sys.argv``. Nó có các đối tượng tệp luồng I/O chuẩn mới ``sys.stdin``, ``sys.stdout`` và ``sys.stderr`` (tuy nhiên, các đối tượng này trỏ đến cùng các file descriptor bên dưới).

   *config* được cung cấp sẽ kiểm soát các tùy chọn dùng để khởi tạo interpreter.

   Nếu thành công, *tstate_p* sẽ được đặt thành :term:`thread state` đầu tiên được tạo trong sub-interpreter mới. Trạng thái thread này là
   :term:`attached <attached thread state>`. Lưu ý rằng không có thread thực tế nào được tạo; xem phần thảo luận về các trạng thái thread bên dưới. Nếu không thể tạo interpreter mới, *tstate_p* được đặt thành ``NULL``; không có exception nào được thiết lập vì trạng thái exception được lưu trong
   :term:`attached thread state`, vốn có thể không tồn tại.

   Giống như mọi hàm Python/C API khác, phải có một :term:`attached thread state` trước khi gọi hàm này, nhưng nó có thể bị tách (detached) khi hàm trả về. Khi thành công, thread state được trả về sẽ ở trạng thái :term:`attached <attached thread state>`. Nếu sub-interpreter được tạo với :term:`GIL` riêng thì
   :term:`attached thread state` của interpreter đang gọi sẽ bị tách (detached). Khi hàm trả về, :term:`thread state` của interpreter mới sẽ được :term:`attached <attached thread state>` vào thread hiện tại, còn :term:`attached thread state` của interpreter trước đó vẫn sẽ bị tách.

   .. versionadded:: 3.12

   Sub-interpreter hoạt động hiệu quả nhất khi được cô lập với nhau, với một số chức năng bị hạn chế::

      PyInterpreterConfig config = {
          .use_main_obmalloc = 0,
          .allow_fork = 0,
          .allow_exec = 0,
          .allow_threads = 1,
          .allow_daemon_threads = 0,
          .check_multi_interp_extensions = 1,
          .gil = PyInterpreterConfig_OWN_GIL,
      };
      PyThreadState *tstate = NULL;
      PyStatus status = Py_NewInterpreterFromConfig(&tstate, &config);
      if (PyStatus_Exception(status)) {
          Py_ExitStatusException(status);
      }

   Lưu ý rằng config chỉ được sử dụng trong thời gian ngắn và không bị sửa đổi. Trong quá trình khởi tạo, các giá trị của config được chuyển đổi thành nhiều
   Các giá trị :c:type:`PyInterpreterState`. Một bản sao chỉ đọc của config có thể được lưu trữ nội bộ trên :c:type:`PyInterpreterState`.

   .. index::
      single: Py_FinalizeEx (C function)
      single: Py_Initialize (C function)

   Các module mở rộng được dùng chung giữa các interpreter (và sub-interpreter) như sau:

   *  Đối với các module sử dụng khởi tạo nhiều giai đoạn, ví dụ :c:func:`PyModule_FromDefAndSpec`, một đối tượng module riêng biệt được tạo và khởi tạo cho mỗi interpreter. Chỉ các biến static và biến toàn cục ở cấp C được dùng chung giữa các đối tượng module này.

   *  Đối với các module sử dụng khởi tạo kiểu legacy
      :ref:`khởi tạo một giai đoạn <single-phase-initialization>`, ví dụ :c:func:`PyModule_Create`, lần đầu một extension cụ thể được import, nó được khởi tạo bình thường và một bản sao (nông) của dictionary của module được lưu lại. Khi extension đó được import bởi một interpreter (hoặc sub-interpreter) khác, một module mới được khởi tạo và điền nội dung của bản sao này; hàm ``init`` của extension không được gọi. Do đó, các đối tượng trong dictionary của module cuối cùng được dùng chung giữa các interpreter (hoặc sub-interpreter), điều này có thể gây ra hành vi không mong muốn (xem `Lỗi và lưu ý <Bugs and caveats_>`_ bên dưới).

      Lưu ý rằng điều này khác với những gì xảy ra khi một extension được import sau khi interpreter đã được khởi tạo lại hoàn toàn bằng cách gọi :c:func:`Py_FinalizeEx` và :c:func:`Py_Initialize`; trong trường hợp đó, hàm ``initmodule`` của extension *được* gọi lại. Tương tự như khởi tạo nhiều giai đoạn, điều này có nghĩa là chỉ các biến static và biến toàn cục ở cấp C được dùng chung giữa các module này.

   .. index:: single: close (in module os)


.. c:function:: PyThreadState* Py_NewInterpreter(void)

   .. index::
      pair: module; builtins
      pair: module; __main__
      pair: module; sys
      single: stdout (in module sys)
      single: stderr (in module sys)
      single: stdin (in module sys)

   Tạo một sub-interpreter mới. Về cơ bản, đây chỉ là một wrapper quanh :c:func:`Py_NewInterpreterFromConfig` với config giữ nguyên hành vi hiện có. Kết quả là một sub-interpreter không được cô lập, dùng chung GIL của main interpreter, cho phép fork/exec, cho phép daemon thread và cho phép các module khởi tạo một giai đoạn.


.. c:function:: void Py_EndInterpreter(PyThreadState *tstate)

   .. index:: single: Py_FinalizeEx (C function)

   Hủy trình thông dịch (phụ) được biểu diễn bởi :term:`thread state` đã cho. Trạng thái luồng đã cho phải được :term:`gắn <attached thread state>`. Khi lệnh gọi trả về, sẽ không còn :term:`attached thread state`. Tất cả trạng thái luồng liên kết với trình thông dịch này đều bị hủy.

   :c:func:`Py_FinalizeEx` sẽ hủy tất cả các trình thông dịch phụ chưa được hủy một cách rõ ràng tại thời điểm đó.


.. _per-interpreter-gil:

GIL cho mỗi trình thông dịch
----------------------------

.. versionadded:: 3.12

Bằng cách sử dụng :c:func:`Py_NewInterpreterFromConfig`, bạn có thể tạo một trình thông dịch phụ hoàn toàn biệt lập với các trình thông dịch khác, bao gồm cả việc có GIL riêng. Lợi ích quan trọng nhất của sự cô lập này là trình thông dịch đó có thể thực thi mã Python mà không bị các trình thông dịch khác chặn, cũng như không chặn bất kỳ trình thông dịch nào khác. Nhờ vậy, một tiến trình Python duy nhất có thể thực sự tận dụng nhiều lõi CPU khi chạy mã Python. Sự cô lập này cũng khuyến khích một cách tiếp cận khác đối với concurrency thay vì chỉ sử dụng các thread. (Xem :pep:`554` và :pep:`684`.)

Việc sử dụng một trình thông dịch biệt lập đòi hỏi phải hết sức cẩn trọng để duy trì sự cô lập đó. Điều này đặc biệt có nghĩa là không chia sẻ bất kỳ đối tượng hoặc trạng thái có thể thay đổi nào nếu không có bảo đảm về thread-safety. Ngay cả những đối tượng vốn bất biến (ví dụ: ``None``, ``(1, 5)``) thông thường cũng không thể được chia sẻ vì refcount. Một cách đơn giản nhưng kém hiệu quả hơn để xử lý việc này là dùng một global lock quanh mọi lần sử dụng một số trạng thái (hoặc đối tượng). Ngoài ra, các đối tượng về hiệu quả là bất biến (như số nguyên hoặc chuỗi) có thể được làm an toàn dù có refcount bằng cách làm cho chúng :term:`immortal`. Trên thực tế, điều này đã được thực hiện đối với các singleton dựng sẵn, các số nguyên nhỏ và một số đối tượng dựng sẵn khác.

Nếu duy trì sự cô lập, bạn sẽ có quyền truy cập vào khả năng tính toán đa lõi thực sự mà không phải đối mặt với những phức tạp đi kèm với free-threading. Việc không duy trì sự cô lập sẽ khiến bạn phải chịu toàn bộ hệ quả của free-threading, bao gồm race condition và các lỗi crash khó gỡ lỗi.

Ngoài ra, một trong những thách thức chính khi sử dụng nhiều trình thông dịch biệt lập là làm thế nào để giao tiếp giữa chúng một cách an toàn (không phá vỡ sự cô lập) và hiệu quả. Runtime và stdlib hiện vẫn chưa cung cấp cách tiếp cận tiêu chuẩn nào cho việc này. Một module stdlib trong tương lai sẽ giúp giảm bớt nỗ lực duy trì sự cô lập và cung cấp các công cụ hiệu quả để giao tiếp (và chia sẻ) dữ liệu giữa các trình thông dịch.


.. _`Bugs and caveats`:

Lỗi và lưu ý
------------

Vì các sub-interpreter (và interpreter chính) là một phần của cùng một process, mức độ cách ly giữa chúng không hoàn hảo --- chẳng hạn, khi sử dụng các thao tác tệp cấp thấp như :func:`os.close`, chúng có thể (vô tình hoặc có ác ý) ảnh hưởng đến các tệp đang mở của nhau. Do cách các extension được dùng chung giữa các (sub-)interpreter, một số extension có thể không hoạt động đúng; điều này đặc biệt dễ xảy ra khi sử dụng khởi tạo một pha hoặc các biến toàn cục (static). Có thể chèn các đối tượng được tạo trong một sub-interpreter vào namespace của một (sub-)interpreter khác; nếu có thể, nên tránh việc này.

Cần đặc biệt cẩn thận để tránh chia sẻ các hàm, phương thức, instance hoặc class do người dùng định nghĩa giữa các sub-interpreter, vì các thao tác import do những đối tượng này thực hiện có thể ảnh hưởng đến dictionary chứa các module đã tải của (sub-)interpreter không đúng. Việc tránh chia sẻ các đối tượng mà từ đó có thể truy cập đến những đối tượng nêu trên cũng quan trọng không kém.

Ngoài ra, hãy lưu ý rằng việc kết hợp chức năng này với các API ``PyGILState_*`` rất dễ phát sinh vấn đề, vì các API này giả định có ánh xạ song ánh giữa trạng thái thread của Python và các thread ở cấp hệ điều hành, trong khi sự hiện diện của các sub-interpreter phá vỡ giả định đó. Bạn nên tuyệt đối tránh chuyển đổi sub-interpreter giữa một cặp lệnh gọi :c:func:`PyGILState_Ensure` và :c:func:`PyGILState_Release` tương ứng. Hơn nữa, các extension (chẳng hạn như :mod:`ctypes`) sử dụng những API này để cho phép gọi mã Python từ các thread không được Python tạo ra có thể sẽ bị hỏng khi sử dụng sub-interpreter.


API cấp cao
-----------

.. c:type:: PyInterpreterState

   Cấu trúc dữ liệu này biểu diễn trạng thái được chia sẻ bởi một số thread phối hợp với nhau. Các thread thuộc cùng một interpreter chia sẻ hoạt động quản lý module và một vài mục nội bộ khác. Cấu trúc này không có member công khai nào.

   Các thread thuộc các interpreter khác nhau ban đầu không chia sẻ gì, ngoại trừ trạng thái của process như bộ nhớ khả dụng, các file descriptor đang mở và những thứ tương tự. Global interpreter lock cũng được tất cả các thread chia sẻ, bất kể chúng thuộc interpreter nào.

   .. versionchanged:: 3.12

      :pep:`684` đã mở ra khả năng sử dụng :ref:`GIL theo từng interpreter <per-interpreter-gil>`. Xem :c:func:`Py_NewInterpreterFromConfig`.


.. c:function:: PyInterpreterState* PyInterpreterState_Get(void)

   Lấy interpreter hiện tại.

   Phát sinh lỗi nghiêm trọng nếu không có :term:`attached thread state`. Hàm này không thể trả về NULL.

   .. versionadded:: 3.9


.. c:function:: int64_t PyInterpreterState_GetID(PyInterpreterState *interp)

   Trả về ID duy nhất của interpreter. Nếu xảy ra bất kỳ lỗi nào trong quá trình thực hiện, ``-1`` sẽ được trả về và một lỗi sẽ được thiết lập.

   Caller phải có :term:`attached thread state`.

   .. versionadded:: 3.7


.. c:function:: PyObject* PyInterpreterState_GetDict(PyInterpreterState *interp)

   Trả về một dictionary dùng để lưu trữ dữ liệu dành riêng cho interpreter. Nếu hàm này trả về ``NULL`` thì không có exception nào được phát sinh và caller nên giả định rằng không có dict dành riêng cho interpreter.

   Đây không phải là phương án thay thế cho :c:func:`PyModule_GetState()`, vốn nên được các extension sử dụng để lưu trữ thông tin trạng thái dành riêng cho interpreter.

   Từ điển được trả về là đối tượng mượn từ trình thông dịch và hợp lệ cho đến khi trình thông dịch tắt.

   .. versionadded:: 3.8


.. c:type:: PyObject* (*_PyFrameEvalFunction)(PyThreadState *tstate, _PyInterpreterFrame *frame, int throwflag)

   Kiểu của hàm đánh giá frame.

   Tham số *throwflag* được phương thức ``throw()`` của generator sử dụng: nếu khác không, hãy xử lý ngoại lệ hiện tại.

   .. versionchanged:: 3.9
      Hàm hiện nhận tham số *tstate*.

   .. versionchanged:: 3.11
      Tham số *frame* đã thay đổi từ ``PyFrameObject*`` thành ``_PyInterpreterFrame*``.


.. c:function:: _PyFrameEvalFunction _PyInterpreterState_GetEvalFrameFunc(PyInterpreterState *interp)

   Lấy hàm đánh giá frame.

   Xem :pep:`523` "Thêm API đánh giá frame vào CPython".

   .. versionadded:: 3.9


.. c:function:: void _PyInterpreterState_SetEvalFrameFunc(PyInterpreterState *interp, _PyFrameEvalFunction eval_frame)

   Thiết lập hàm đánh giá frame.

   Xem :pep:`523` "Thêm API đánh giá frame vào CPython".

   .. versionadded:: 3.9


API cấp thấp
------------

Tất cả các hàm sau đây phải được gọi sau :c:func:`Py_Initialize`.

.. versionchanged:: 3.7
   :c:func:`Py_Initialize()` now initializes the :term:`GIL`
   và thiết lập một :term:`attached thread state`.


.. c:function:: PyInterpreterState* PyInterpreterState_New()

   Tạo một đối tượng trạng thái interpreter mới. Không cần :term:`attached thread state`, nhưng có thể tồn tại tùy chọn nếu cần tuần tự hóa các lệnh gọi đến hàm này.

   .. audit-event:: cpython.PyInterpreterState_New "" c.PyInterpreterState_New


.. c:function:: void PyInterpreterState_Clear(PyInterpreterState *interp)

   Đặt lại tất cả thông tin trong một đối tượng trạng thái interpreter. Phải có một :term:`attached thread state` cho interpreter.

   .. audit-event:: cpython.PyInterpreterState_Clear "" c.PyInterpreterState_Clear


.. c:function:: void PyInterpreterState_Delete(PyInterpreterState *interp)

   Hủy đối tượng trạng thái interpreter. **không nên** có một
   :term:`attached thread state` cho interpreter đích. Trạng thái interpreter phải đã được đặt lại bằng một lần gọi trước đó đến :c:func:`PyInterpreterState_Clear`.


.. _advanced-debugging:

Hỗ trợ trình gỡ lỗi nâng cao
----------------------------

Các hàm này chỉ dành cho các công cụ gỡ lỗi nâng cao.


.. c:function:: PyInterpreterState* PyInterpreterState_Head()

   Trả về đối tượng trạng thái interpreter ở đầu danh sách gồm tất cả các đối tượng như vậy.


.. c:function:: PyInterpreterState* PyInterpreterState_Main()

   Trả về đối tượng trạng thái interpreter chính.


.. c:function:: PyInterpreterState* PyInterpreterState_Next(PyInterpreterState *interp)

   Trả về đối tượng trạng thái interpreter tiếp theo sau *interp* trong danh sách gồm tất cả các đối tượng như vậy.


.. c:function:: PyThreadState * PyInterpreterState_ThreadHead(PyInterpreterState *interp)

   Trả về con trỏ đến đối tượng :c:type:`PyThreadState` đầu tiên trong danh sách các thread liên kết với interpreter *interp*.


.. c:function:: PyThreadState* PyThreadState_Next(PyThreadState *tstate)

   Trả về đối tượng trạng thái thread tiếp theo sau *tstate* từ danh sách tất cả các đối tượng như vậy thuộc cùng một đối tượng :c:type:`PyInterpreterState`.
