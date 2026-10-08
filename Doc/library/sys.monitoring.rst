:mod:`!sys.monitoring` --- Giám sát sự kiện thực thi
====================================================

.. module:: sys.monitoring
   :synopsis: Truy cập và kiểm soát việc giám sát sự kiện

.. versionadded:: 3.12

-----------------

.. note::

    :mod:`!sys.monitoring` là một namespace trong module :mod:`sys`, không phải là một module độc lập, và ``import sys.monitoring`` sẽ gây ra :exc:`ModuleNotFoundError`. Thay vào đó, chỉ cần ``import sys``, rồi sử dụng ``sys.monitoring``.


Namespace này cung cấp quyền truy cập vào các hàm và hằng số cần thiết để kích hoạt và kiểm soát việc giám sát sự kiện.

Khi chương trình thực thi, các sự kiện xảy ra có thể được các công cụ giám sát quá trình thực thi quan tâm. Namespace :mod:`!sys.monitoring` cung cấp phương thức để nhận callback khi các sự kiện cần quan tâm xảy ra.

API giám sát gồm ba thành phần:

* `Mã định danh công cụ <Tool identifiers_>`_
* `Events`_
* :ref:`Callback <callbacks>`

.. _`Tool identifiers`:

Mã định danh công cụ
--------------------

Mã định danh công cụ là một số nguyên và tên tương ứng. Mã định danh công cụ được sử dụng để ngăn các công cụ can thiệp lẫn nhau và cho phép nhiều công cụ hoạt động đồng thời. Hiện tại, các công cụ hoàn toàn độc lập và không thể được dùng để giám sát lẫn nhau. Hạn chế này có thể được gỡ bỏ trong tương lai.

Trước khi đăng ký hoặc kích hoạt các sự kiện, một công cụ nên chọn một mã định danh. Mã định danh là các số nguyên trong phạm vi từ 0 đến 5, bao gồm cả hai giá trị này.

Đăng ký và sử dụng công cụ
''''''''''''''''''''''''''

.. function:: use_tool_id(tool_id: int, name: str, /) -> None

   Phải được gọi trước khi có thể sử dụng *tool_id*. *tool_id* phải nằm trong phạm vi từ 0 đến 5, bao gồm cả hai giá trị này. Phát sinh một :exc:`ValueError` nếu *tool_id* đang được sử dụng.

.. function:: clear_tool_id(tool_id: int, /) -> None

   Hủy đăng ký tất cả sự kiện và các hàm callback liên kết với *tool_id*.

   .. versionadded:: 3.14

.. function:: free_tool_id(tool_id: int, /) -> None

   Nên được gọi một lần khi một tool không còn yêu cầu *tool_id*. Sẽ gọi :func:`clear_tool_id` trước khi giải phóng *tool_id*.

   .. versionchanged:: 3.14
      Giờ đây sẽ gọi :func:`clear_tool_id` trước khi giải phóng *tool_id*. Trước đây, hàm này không vô hiệu hóa các event toàn cục hoặc cục bộ liên kết với *tool_id*, cũng không hủy đăng ký bất kỳ callback function nào.

.. function:: get_tool(tool_id: int, /) -> str | None

   Trả về tên của tool nếu *tool_id* đang được sử dụng; nếu không, trả về ``None``. *tool_id* phải nằm trong khoảng từ 0 đến 5, bao gồm cả hai đầu mút.

VM xử lý tất cả ID như nhau đối với các event, nhưng các ID sau đây được định nghĩa sẵn để giúp các tool phối hợp dễ dàng hơn::

  sys.monitoring.DEBUGGER_ID = 0
  sys.monitoring.COVERAGE_ID = 1
  sys.monitoring.PROFILER_ID = 2
  sys.monitoring.OPTIMIZER_ID = 5


Sự kiện
-------

Các event sau được hỗ trợ:

.. monitoring-event:: BRANCH_LEFT

   Một nhánh điều kiện rẽ sang trái.

   Công cụ sẽ quyết định cách trình bày các nhánh "left" và "right". Không có gì đảm bảo nhánh nào là "left" và nhánh nào là "right", ngoại trừ việc cách này sẽ nhất quán trong suốt thời gian chạy của chương trình.

.. monitoring-event:: BRANCH_RIGHT

   Một nhánh điều kiện đi sang phải.

.. monitoring-event:: CALL

   Một lệnh gọi trong mã Python (event xảy ra trước lệnh gọi).

.. monitoring-event:: C_RAISE

   Một exception được nêu ra từ bất kỳ callable nào, ngoại trừ các hàm Python (event xảy ra sau khi thoát).

.. monitoring-event:: C_RETURN

   Trả về từ bất kỳ callable nào, ngoại trừ các hàm Python (event xảy ra sau khi trả về).

.. monitoring-event:: EXCEPTION_HANDLED

   Một exception được xử lý.

.. monitoring-event:: INSTRUCTION

   Một chỉ thị VM sắp được thực thi.

.. monitoring-event:: JUMP

   Một bước nhảy vô điều kiện trong đồ thị luồng điều khiển được thực hiện.

.. monitoring-event:: LINE

   Một instruction sắp được thực thi có số dòng khác với instruction ngay trước đó.

.. monitoring-event:: PY_RESUME

   Tiếp tục thực thi một hàm Python (đối với các hàm generator và coroutine), ngoại trừ các lệnh gọi ``throw()``.

.. monitoring-event:: PY_RETURN

   Trở về từ một hàm Python (xảy ra ngay trước khi return; frame của callee sẽ nằm trên stack).

.. monitoring-event:: PY_START

   Bắt đầu một hàm Python (xảy ra ngay sau lệnh gọi; frame của callee sẽ nằm trên stack).

.. monitoring-event:: PY_THROW

   Một hàm Python được tiếp tục thực thi bởi một lệnh gọi ``throw()``.

.. monitoring-event:: PY_UNWIND

   Thoát khỏi một hàm Python trong quá trình unwind ngoại lệ. Điều này bao gồm các ngoại lệ được phát sinh trực tiếp bên trong hàm và được phép tiếp tục lan truyền.

.. monitoring-event:: PY_YIELD

   Yield từ một hàm Python (xảy ra ngay trước yield, frame của callee sẽ nằm trên stack).

.. monitoring-event:: RAISE

   Một exception được raised, ngoại trừ những exception gây ra sự kiện :monitoring-event:`STOP_ITERATION`.

.. monitoring-event:: RERAISE

   Một exception được re-raised, chẳng hạn ở cuối khối :keyword:`finally`.

.. monitoring-event:: STOP_ITERATION

   Một :exc:`StopIteration` nhân tạo được raised; xem `sự kiện STOP_ITERATION <the STOP_ITERATION event_>`_.


Có thể sẽ bổ sung thêm các sự kiện trong tương lai.

Các sự kiện này là các thuộc tính của namespace :mod:`!sys.monitoring.events`. Mỗi sự kiện được biểu diễn bằng một hằng số nguyên có giá trị là lũy thừa của 2. Để định nghĩa một tập hợp sự kiện, chỉ cần thực hiện phép OR theo bitwise giữa các sự kiện riêng lẻ. Ví dụ, để chỉ định cả hai sự kiện :monitoring-event:`PY_RETURN` và :monitoring-event:`PY_START`, hãy sử dụng biểu thức ``PY_RETURN | PY_START``.

.. monitoring-event:: NO_EVENTS

    Một bí danh cho ``0`` để người dùng có thể thực hiện các phép so sánh tường minh như::

      if get_events(DEBUGGER_ID) == NO_EVENTS:
          ...

    Việc thiết lập sự kiện này sẽ vô hiệu hóa tất cả các sự kiện.

.. _monitoring-event-local:

Các sự kiện cục bộ
''''''''''''''''''

Các sự kiện cục bộ gắn liền với quá trình thực thi thông thường của chương trình và xảy ra tại những vị trí được xác định rõ ràng. Có thể vô hiệu hóa tất cả các sự kiện cục bộ. Các sự kiện cục bộ bao gồm:

* :monitoring-event:`PY_START`
* :monitoring-event:`PY_RESUME`
* :monitoring-event:`PY_RETURN`
* :monitoring-event:`PY_YIELD`
* :monitoring-event:`CALL`
* :monitoring-event:`LINE`
* :monitoring-event:`INSTRUCTION`
* :monitoring-event:`JUMP`
* :monitoring-event:`BRANCH_LEFT`
* :monitoring-event:`BRANCH_RIGHT`
* :monitoring-event:`STOP_ITERATION`

Sự kiện không còn được dùng
'''''''''''''''''''''''''''

* ``BRANCH``

Sự kiện ``BRANCH`` không còn được dùng kể từ phiên bản 3.14. Việc sử dụng các sự kiện :monitoring-event:`BRANCH_LEFT` và :monitoring-event:`BRANCH_RIGHT` sẽ mang lại hiệu suất tốt hơn nhiều vì bạn có thể vô hiệu hóa chúng độc lập.

Các sự kiện phụ trợ
'''''''''''''''''''

Các sự kiện phụ trợ có thể được giám sát như những sự kiện khác, nhưng được điều khiển bởi một sự kiện khác:

* :monitoring-event:`C_RAISE`
* :monitoring-event:`C_RETURN`

Các sự kiện :monitoring-event:`C_RETURN` và :monitoring-event:`C_RAISE` được điều khiển bởi sự kiện :monitoring-event:`CALL`.
Các sự kiện :monitoring-event:`C_RETURN` và :monitoring-event:`C_RAISE` chỉ xuất hiện nếu sự kiện :monitoring-event:`CALL` tương ứng đang được giám sát.


.. _monitoring-event-global:

Các sự kiện khác
''''''''''''''''

Các sự kiện khác không nhất thiết gắn với một vị trí cụ thể trong chương trình và không thể bị vô hiệu hóa riêng lẻ thông qua :data:`DISABLE`.

Các sự kiện khác có thể được giám sát là:

* :monitoring-event:`PY_THROW`
* :monitoring-event:`PY_UNWIND`
* :monitoring-event:`RAISE`
* :monitoring-event:`EXCEPTION_HANDLED`


.. _`The STOP_ITERATION event`:

Sự kiện STOP_ITERATION
''''''''''''''''''''''

:pep:`PEP 380 <380#use-of-stopiteration-to-return-values>` chỉ định rằng một ngoại lệ :exc:`StopIteration` được raised khi trả về một giá trị từ generator hoặc coroutine. Tuy nhiên, đây là cách trả về giá trị rất kém hiệu quả, vì vậy một số triển khai Python, đáng chú ý là CPython 3.12+, không raised ngoại lệ trừ khi ngoại lệ đó có thể được mã khác quan sát.

Để cho phép các công cụ theo dõi các ngoại lệ thực sự mà không làm chậm generators và coroutines, sự kiện :monitoring-event:`STOP_ITERATION` được cung cấp.
:monitoring-event:`STOP_ITERATION` có thể được tắt cục bộ, không giống như
:monitoring-event:`RAISE`.

Lưu ý rằng sự kiện :monitoring-event:`STOP_ITERATION` và
sự kiện :monitoring-event:`RAISE` đối với một ngoại lệ :exc:`StopIteration` là tương đương và được xử lý như có thể thay thế cho nhau khi tạo sự kiện. Các triển khai sẽ ưu tiên :monitoring-event:`STOP_ITERATION` vì lý do hiệu năng, nhưng có thể tạo một sự kiện :monitoring-event:`RAISE` với một
:exc:`StopIteration`.

Bật và tắt các sự kiện
----------------------

Để theo dõi một sự kiện, cần bật sự kiện đó và đăng ký callback tương ứng. Có thể bật hoặc tắt các sự kiện bằng cách thiết lập chúng trên toàn cục và/hoặc cho một đối tượng mã cụ thể. Một sự kiện sẽ chỉ được kích hoạt một lần, ngay cả khi được bật cả trên toàn cục lẫn cục bộ.


Thiết lập sự kiện trên toàn cục
'''''''''''''''''''''''''''''''

Có thể kiểm soát các event trên toàn cục bằng cách sửa đổi tập hợp các event đang được giám sát.

.. function:: get_events(tool_id: int, /) -> int

   Trả về ``int`` đại diện cho tất cả các event đang hoạt động.

.. function:: set_events(tool_id: int, event_set: int, /) -> None

   Kích hoạt tất cả các event được thiết lập trong *event_set*. Phát sinh :exc:`ValueError` nếu *tool_id* không được sử dụng.

Theo mặc định, không có event nào đang hoạt động.

Event theo từng code object
'''''''''''''''''''''''''''

Các event cũng có thể được kiểm soát theo từng code object. Các hàm được định nghĩa bên dưới và nhận :class:`types.CodeType` cần sẵn sàng chấp nhận một đối tượng tương tự từ các hàm không được định nghĩa trong Python (xem :ref:`c-api-monitoring`).

.. function:: get_local_events(tool_id: int, code: CodeType, /) -> int

   Trả về tất cả :ref:`local events <monitoring-event-local>` cho *code*

.. function:: set_local_events(tool_id: int, code: CodeType, event_set: int, /) -> None

   Kích hoạt tất cả :ref:`event cục bộ <monitoring-event-local>` cho *code* được thiết lập trong *event_set*. Phát sinh :exc:`ValueError` nếu *tool_id* không được sử dụng.


Vô hiệu hóa event
'''''''''''''''''

.. data:: DISABLE

   Một giá trị đặc biệt có thể được trả về từ hàm callback để vô hiệu hóa event tại vị trí code hiện tại.

Có thể vô hiệu hóa :ref:`event cục bộ <monitoring-event-local>` cho một vị trí code cụ thể bằng cách trả về :data:`sys.monitoring.DISABLE` từ một hàm callback. Việc này không thay đổi các event được thiết lập hoặc bất kỳ vị trí code nào khác đối với cùng event.

Việc vô hiệu hóa event tại các vị trí cụ thể rất quan trọng đối với hoạt động giám sát hiệu năng cao. Ví dụ, một chương trình có thể được chạy dưới debugger mà không phát sinh overhead nếu debugger vô hiệu hóa toàn bộ hoạt động giám sát, ngoại trừ một vài breakpoint.

Nếu :data:`DISABLE` được callback trả về cho một
:ref:`event toàn cục <monitoring-event-global>`, :exc:`ValueError` sẽ được interpreter phát sinh tại một vị trí không cụ thể (nghĩa là sẽ không cung cấp traceback).

.. function:: restart_events() -> None

   Bật tất cả các sự kiện đã bị :data:`sys.monitoring.DISABLE` vô hiệu hóa cho mọi công cụ.


.. _callbacks:

Đăng ký các hàm callback
------------------------

.. function:: register_callback(tool_id: int, event: int, func: Callable | None, /) -> Callable | None

   Đăng ký callable *func* cho *event* với *tool_id* đã cho

   Nếu một callback khác đã được đăng ký cho *tool_id* và *event*, callback đó sẽ bị hủy đăng ký và được trả về. Nếu không, :func:`register_callback` trả về ``None``.

   .. audit-event:: sys.monitoring.register_callback func sys.monitoring.register_callback

Có thể hủy đăng ký các hàm bằng cách gọi ``sys.monitoring.register_callback(tool_id, event, None)``.

Có thể đăng ký và hủy đăng ký các hàm callback bất kỳ lúc nào.

Các callback chỉ được gọi một lần, bất kể sự kiện được bật cả trên phạm vi toàn cục và cục bộ. Vì vậy, nếu mã của bạn có thể bật một sự kiện cho cả sự kiện toàn cục và cục bộ thì callback cần được viết để xử lý cả hai cách kích hoạt.


Đối số của hàm callback
'''''''''''''''''''''''

.. data:: MISSING

   Một giá trị đặc biệt được truyền cho hàm callback để cho biết rằng lệnh gọi không có đối số nào.

Khi một sự kiện đang hoạt động xảy ra, hàm callback đã đăng ký sẽ được gọi. Các hàm callback trả về một đối tượng khác :data:`DISABLE` sẽ không có tác dụng. Các sự kiện khác nhau sẽ cung cấp cho hàm callback những đối số khác nhau, như sau:

* :monitoring-event:`PY_START` và :monitoring-event:`PY_RESUME`::

    func(code: CodeType, instruction_offset: int) -> object

* :monitoring-event:`PY_RETURN` và :monitoring-event:`PY_YIELD`::

    func(code: CodeType, instruction_offset: int, retval: object) -> object

* :monitoring-event:`CALL`, :monitoring-event:`C_RAISE` và :monitoring-event:`C_RETURN` (*arg0* cụ thể có thể là :data:`MISSING`)::

    func(code: CodeType, instruction_offset: int, callable: object, arg0: object) -> object

  *code* đại diện cho đối tượng code nơi lệnh gọi được thực hiện, còn *callable* là đối tượng sắp được gọi (và do đó đã kích hoạt sự kiện). Nếu không có đối số nào, *arg0* được đặt thành :data:`sys.monitoring.MISSING`.

  Đối với các phương thức của instance, *callable* sẽ là đối tượng hàm được tìm thấy trên class, với *arg0* được đặt thành instance (tức là đối số ``self`` của phương thức).

* :monitoring-event:`RAISE`, :monitoring-event:`RERAISE`, :monitoring-event:`EXCEPTION_HANDLED`,
  :monitoring-event:`PY_UNWIND`, :monitoring-event:`PY_THROW` và :monitoring-event:`STOP_ITERATION`::

    func(code: CodeType, instruction_offset: int, exception: BaseException) -> object

* :monitoring-event:`LINE`::

    func(code: CodeType, line_number: int) -> object

* :monitoring-event:`BRANCH_LEFT`, :monitoring-event:`BRANCH_RIGHT` và :monitoring-event:`JUMP`::

    func(code: CodeType, instruction_offset: int, destination_offset: int) -> object

  Note that the *destination_offset* is where the code will next execute.

* :monitoring-event:`INSTRUCTION`::

    func(code: CodeType, instruction_offset: int) -> object
