:mod:`!bdb` --- Framework trình gỡ lỗi
======================================

.. module:: bdb
   :synopsis: Framework trình gỡ lỗi.

**Mã nguồn:** :source:`Lib/bdb.py`

--------------

Mô-đun :mod:`!bdb` xử lý các chức năng gỡ lỗi cơ bản, chẳng hạn như đặt breakpoint hoặc quản lý việc thực thi thông qua trình gỡ lỗi.

Ngoại lệ sau được định nghĩa:

.. exception:: BdbQuit

   Ngoại lệ do lớp :class:`Bdb` đưa ra để thoát khỏi trình gỡ lỗi.


Mô-đun :mod:`!bdb` cũng định nghĩa hai lớp:

.. class:: Breakpoint(self, file, line, temporary=False, cond=None, funcname=None)

   Lớp này triển khai các điểm ngắt tạm thời, số lần bỏ qua, việc vô hiệu hóa và (tái) kích hoạt, cùng các điều kiện.

   Các điểm ngắt được lập chỉ mục theo số thông qua một danh sách có tên :attr:`bpbynumber` và theo các cặp ``(file, line)`` thông qua :attr:`bplist`. Cách đầu trỏ đến một thực thể duy nhất của lớp :class:`Breakpoint`. Cách sau trỏ đến một danh sách các thực thể như vậy vì mỗi dòng có thể có nhiều hơn một điểm ngắt.

   Khi tạo một điểm ngắt, :attr:`file name <file>` liên kết với nó phải ở dạng chuẩn. Nếu :attr:`funcname` được xác định, một điểm ngắt
   :attr:`hit <hits>` sẽ được tính khi dòng đầu tiên của hàm đó được thực thi. Một điểm ngắt :attr:`conditional <cond>` luôn tính một
   :attr:`hit <hits>`.

   Các thực thể :class:`Breakpoint` có những phương thức sau:

   .. method:: deleteMe()

      Xóa điểm ngắt khỏi danh sách liên kết với tệp/dòng. Nếu đó là điểm ngắt cuối cùng tại vị trí đó, phương thức này cũng xóa mục nhập của tệp/dòng.


   .. method:: enable()

      Đánh dấu điểm ngắt là đã bật.


   .. method:: disable()

      Đánh dấu breakpoint là đã tắt.


   .. method:: bpformat()

      Trả về một chuỗi chứa tất cả thông tin về breakpoint, được định dạng rõ ràng:

      * Số breakpoint.
      * Trạng thái tạm thời (del hoặc keep).
      * Vị trí tệp/dòng.
      * Điều kiện dừng.
      * Số lần cần bỏ qua.
      * Số lần được kích hoạt.

      .. versionadded:: 3.2

   .. method:: bpprint(out=None)

      In kết quả của :meth:`bpformat` vào tệp *out*, hoặc nếu là ``None``, thì in ra đầu ra chuẩn.

   Các thể hiện của :class:`Breakpoint` có các thuộc tính sau:

   .. attribute:: file

      Tên tệp của :class:`Breakpoint`.

   .. attribute:: line

      Số dòng của :class:`Breakpoint` trong :attr:`file`.

   .. attribute:: temporary

      ``True`` nếu một :class:`Breakpoint` tại (file, line) là tạm thời.

   .. attribute:: cond

      Điều kiện để đánh giá một :class:`Breakpoint` tại (file, line).

   .. attribute:: funcname

      Tên hàm xác định liệu có :class:`Breakpoint` khi đi vào hàm hay không.

   .. attribute:: enabled

      ``True`` nếu :class:`Breakpoint` được bật.

   .. attribute:: bpbynumber

      Chỉ mục dạng số cho một thực thể :class:`Breakpoint`.

   .. attribute:: bplist

      Từ điển các thực thể :class:`Breakpoint`, được lập chỉ mục theo các tuple (:attr:`file`, :attr:`line`).

   .. attribute:: ignore

      Số lần bỏ qua một :class:`Breakpoint`.

   .. attribute:: hits

      Số lần một :class:`Breakpoint` đã được kích hoạt.

.. class:: Bdb(skip=None, backend='settrace')

   Lớp :class:`Bdb` đóng vai trò là lớp cơ sở generic cho trình gỡ lỗi Python.

   Lớp này xử lý các chi tiết của cơ chế trace; lớp dẫn xuất cần triển khai tương tác với người dùng. Lớp debugger tiêu chuẩn (:class:`pdb.Pdb`) là một ví dụ.

   Đối số *skip*, nếu được cung cấp, phải là một iterable gồm các mẫu tên module theo kiểu glob. Debugger sẽ không bước vào các frame bắt nguồn từ một module khớp với một trong các mẫu này. Việc một frame có được xem là bắt nguồn từ một module nhất định hay không được xác định bởi ``__name__`` trong các biến toàn cục của frame.

   Đối số *backend* chỉ định backend được sử dụng cho :class:`Bdb`. Giá trị này có thể là ``'settrace'`` hoặc ``'monitoring'``. ``'settrace'`` sử dụng
   :func:`sys.settrace` có khả năng tương thích ngược tốt nhất. Backend ``'monitoring'`` sử dụng :mod:`sys.monitoring` mới được giới thiệu trong Python 3.12, có thể hiệu quả hơn nhiều vì có thể vô hiệu hóa các sự kiện không được sử dụng. Chúng tôi cố gắng duy trì các interface chính xác giống nhau cho cả hai backend, nhưng vẫn có một số khác biệt. Các nhà phát triển debugger được khuyến khích sử dụng backend ``'monitoring'`` để đạt hiệu suất tốt hơn.

   .. versionchanged:: 3.1
      Đã thêm tham số *skip*.

   .. versionchanged:: 3.14
      Đã thêm tham số *backend*.

   Các phương thức sau của :class:`Bdb` thường không cần được ghi đè.

   .. method:: canonic(filename)

      Trả về dạng chuẩn của *filename*.

      Đối với tên tệp thực, dạng chuẩn phụ thuộc vào hệ điều hành,
      :func:`case-normalized <os.path.normcase>` :func:`absolute path <os.path.abspath>`. Một *filename* có dấu ngoặc nhọn, chẳng hạn như ``"<stdin>"`` được tạo ở chế độ tương tác, được trả về không thay đổi.

   .. method:: start_trace(self)

      Bắt đầu tracing. Đối với backend ``'settrace'``, phương thức này tương đương với ``sys.settrace(self.trace_dispatch)``

      .. versionadded:: 3.14

   .. method:: stop_trace(self)

      Dừng tracing. Đối với backend ``'settrace'``, phương thức này tương đương với ``sys.settrace(None)``

      .. versionadded:: 3.14

   .. method:: reset()

      Đặt các thuộc tính :attr:`!botframe`, :attr:`!stopframe`, :attr:`!returnframe` và
      :attr:`quitting <Bdb.set_quit>` với các giá trị sẵn sàng để bắt đầu debugging.

   .. method:: trace_dispatch(frame, event, arg)

      Hàm này được cài đặt làm hàm trace của các frame đang được debug. Giá trị trả về của hàm là hàm trace mới (trong hầu hết trường hợp, chính là hàm này).

      Cài đặt mặc định quyết định cách dispatch một frame, tùy thuộc vào loại sự kiện (được truyền dưới dạng chuỗi) sắp được thực thi. *event* có thể là một trong những giá trị sau:

      * ``"line"``: Một dòng mã mới sắp được thực thi.
      * ``"call"``: Một hàm sắp được gọi hoặc một khối mã khác sắp được truy cập.
      * ``"return"``: Một hàm hoặc khối mã khác sắp trả về.
      * ``"exception"``: Một ngoại lệ đã xảy ra.
      * ``"c_call"``: Một hàm C sắp được gọi.
      * ``"c_return"``: Một hàm C đã trả về.
      * ``"c_exception"``: Một hàm C đã phát sinh ngoại lệ.

      Đối với các sự kiện Python, các hàm chuyên biệt (xem bên dưới) sẽ được gọi. Đối với các sự kiện C, không có hành động nào được thực hiện.

      Tham số *arg* phụ thuộc vào sự kiện trước đó.

      Xem tài liệu về :func:`sys.settrace` để biết thêm thông tin về hàm trace. Để biết thêm thông tin về các đối tượng code và frame, hãy tham khảo
      :ref:`types`.

   .. method:: dispatch_line(frame)

      Nếu debugger nên dừng ở dòng hiện tại, hãy gọi
      phương thức :meth:`user_line` (phương thức này nên được ghi đè trong các lớp con). Hãy raise một ngoại lệ :exc:`BdbQuit` nếu cờ :attr:`quitting  <Bdb.set_quit>` được đặt (có thể đặt cờ này từ :meth:`user_line`). Trả về một tham chiếu đến
      phương thức :meth:`trace_dispatch` để tiếp tục tracing trong phạm vi đó.

   .. method:: dispatch_call(frame, arg)

      Nếu trình gỡ lỗi cần dừng tại lệnh gọi hàm này, hãy gọi
      phương thức :meth:`user_call` (cần được ghi đè trong các lớp con). Phát sinh ngoại lệ :exc:`BdbQuit` nếu cờ :attr:`quitting  <Bdb.set_quit>` được đặt (có thể được đặt từ :meth:`user_call`).  Trả về một tham chiếu đến
      phương thức :meth:`trace_dispatch` để tiếp tục tracing trong phạm vi đó.

   .. method:: dispatch_return(frame, arg)

      Nếu trình gỡ lỗi cần dừng khi hàm này trả về, hãy gọi
      phương thức :meth:`user_return` (cần được ghi đè trong các lớp con). Phát sinh ngoại lệ :exc:`BdbQuit` nếu cờ :attr:`quitting  <Bdb.set_quit>` được đặt (có thể được đặt từ :meth:`user_return`).  Trả về một tham chiếu đến
      phương thức :meth:`trace_dispatch` để tiếp tục tracing trong phạm vi đó.

   .. method:: dispatch_exception(frame, arg)

      Nếu trình debugger phải dừng tại ngoại lệ này, gọi
      phương thức :meth:`user_exception` (phương thức này nên được ghi đè trong các lớp con). Gây ra ngoại lệ :exc:`BdbQuit` nếu cờ :attr:`quitting  <Bdb.set_quit>` được thiết lập (cờ này có thể được thiết lập từ :meth:`user_exception`). Trả về một tham chiếu đến
      phương thức :meth:`trace_dispatch` để tiếp tục tracing trong phạm vi đó.

   Thông thường, các lớp dẫn xuất không ghi đè những phương thức sau, nhưng có thể làm vậy nếu muốn định nghĩa lại việc dừng và các breakpoint.

   .. method:: is_skipped_module(module_name)

      Trả về ``True`` nếu *module_name* khớp với bất kỳ mẫu bỏ qua nào.

   .. method:: stop_here(frame)

      Trả về ``True`` nếu *frame* nằm bên dưới frame bắt đầu trong ngăn xếp.

   .. method:: break_here(frame)

      Trả về ``True`` nếu có breakpoint hiệu lực cho dòng này.

      Kiểm tra xem breakpoint trên dòng hoặc trong hàm có tồn tại và đang có hiệu lực hay không. Xóa các breakpoint tạm thời dựa trên thông tin từ :func:`effective`.

   .. method:: break_anywhere(frame)

      Trả về ``True`` nếu tồn tại bất kỳ breakpoint nào cho tên tệp của *frame*.

   Các lớp dẫn xuất nên ghi đè các phương thức này để giành quyền kiểm soát hoạt động của debugger.

   .. method:: user_call(frame, argument_list)

      Được gọi từ :meth:`dispatch_call` nếu một breakpoint có thể dừng bên trong hàm được gọi.

      *argument_list* không còn được sử dụng và sẽ luôn là ``None``. Đối số này được giữ lại để đảm bảo khả năng tương thích ngược.

   .. method:: user_line(frame)

      Được gọi từ :meth:`dispatch_line` khi :meth:`stop_here` hoặc
      :meth:`break_here` trả về ``True``.

   .. method:: user_return(frame, return_value)

      Được gọi từ :meth:`dispatch_return` khi :meth:`stop_here` trả về ``True``.

   .. method:: user_exception(frame, exc_info)

      Được gọi từ :meth:`dispatch_exception` khi :meth:`stop_here` trả về ``True``.

   .. method:: do_clear(arg)

      Xử lý cách breakpoint phải được gỡ bỏ khi đó là breakpoint tạm thời.

      Phương thức này phải được triển khai bởi các lớp dẫn xuất.


   Các lớp dẫn xuất và client có thể gọi các phương thức sau để tác động đến trạng thái stepping.

   .. method:: set_step()

      Dừng sau một dòng mã.

   .. method:: set_next(frame)

      Dừng ở dòng tiếp theo trong hoặc bên dưới frame đã cho.

   .. method:: set_return(frame)

      Dừng khi quay về từ frame đã cho.

   .. method:: set_until(frame, lineno=None)

      Dừng khi đến dòng có *lineno* lớn hơn dòng hiện tại hoặc khi quay về từ frame hiện tại.

   .. method:: set_trace([frame])

      Bắt đầu debugging từ *frame*. Nếu *frame* không được chỉ định, debugging sẽ bắt đầu từ frame của caller.

      .. versionchanged:: 3.13
         :func:`set_trace` will enter the debugger immediately, rather than
         trên dòng mã tiếp theo sẽ được thực thi.

   .. method:: set_continue()

      Chỉ dừng tại các breakpoint hoặc khi hoàn tất. Nếu không có breakpoint, đặt hàm system trace thành ``None``.

   .. method:: set_quit()

      .. index:: single: quitting (bdb.Bdb attribute)

      Đặt thuộc tính :attr:`!quitting` thành ``True``. Việc này sẽ raise :exc:`BdbQuit` trong lần gọi tiếp theo đến một trong các phương thức :meth:`!dispatch_\*`.


   Các lớp dẫn xuất và client có thể gọi những phương thức sau để thao tác với breakpoint. Những phương thức này trả về một chuỗi chứa thông báo lỗi nếu xảy ra sự cố hoặc ``None`` nếu mọi việc đều ổn.

   .. method:: set_break(filename, lineno, temporary=False, cond=None, funcname=None)

      Đặt một breakpoint mới. Nếu dòng *lineno* không tồn tại trong *filename* được truyền dưới dạng đối số, hãy trả về thông báo lỗi. *filename* phải ở dạng canonical như được mô tả trong :meth:`canonic` phương thức.

   .. method:: clear_break(filename, lineno)

      Xóa các breakpoint trong *filename* và *lineno*. Nếu chưa đặt breakpoint nào, hãy trả về thông báo lỗi.

   .. method:: clear_bpbynumber(arg)

      Xóa breakpoint có chỉ mục *arg* trong
      :attr:`Breakpoint.bpbynumber`. Nếu *arg* không phải là số hoặc nằm ngoài phạm vi, hãy trả về thông báo lỗi.

   .. method:: clear_all_file_breaks(filename)

      Xóa tất cả breakpoint hiện có trong *filename*. Nếu chưa đặt breakpoint nào, hãy trả về thông báo lỗi.

   .. method:: clear_all_breaks()

      Xóa tất cả breakpoint hiện có. Nếu chưa đặt breakpoint nào, hãy trả về thông báo lỗi.

   .. method:: get_bpbynumber(arg)

      Trả về breakpoint được chỉ định bằng số đã cho. Nếu *arg* là một chuỗi, chuỗi đó sẽ được chuyển đổi thành số. Nếu *arg* là một chuỗi không phải số, nếu breakpoint đã cho chưa từng tồn tại hoặc đã bị xóa, hãy
      :exc:`ValueError` được phát sinh.

      .. versionadded:: 3.2

   .. method:: get_break(filename, lineno)

      Trả về ``True`` nếu có điểm dừng tại *lineno* trong *filename*.

   .. method:: get_breaks(filename, lineno)

      Trả về tất cả các điểm dừng cho *lineno* trong *filename*, hoặc một danh sách trống nếu không có điểm dừng nào được thiết lập.

   .. method:: get_file_breaks(filename)

      Trả về tất cả các điểm dừng trong *filename*, hoặc một danh sách trống nếu không có điểm dừng nào được thiết lập.

   .. method:: get_all_breaks()

      Trả về tất cả các điểm dừng đã được thiết lập.


   Các lớp dẫn xuất và client có thể gọi các phương thức sau để vô hiệu hóa và khởi động lại các sự kiện nhằm đạt hiệu suất tốt hơn. Các phương thức này chỉ hoạt động khi sử dụng backend ``'monitoring'``.

   .. method:: disable_current_event()

      Vô hiệu hóa sự kiện hiện tại cho đến lần tiếp theo :func:`restart_events` được gọi. Điều này hữu ích khi debugger không quan tâm đến dòng hiện tại.

      .. versionadded:: 3.14

   .. method:: restart_events()

      Khởi động lại tất cả các sự kiện bị vô hiệu hóa. Hàm này được tự động gọi trong các phương thức ``dispatch_*`` sau khi các phương thức ``user_*`` được gọi. Nếu các phương thức ``dispatch_*`` không được ghi đè, các sự kiện bị vô hiệu hóa sẽ được khởi động lại sau mỗi lần tương tác của người dùng.

      .. versionadded:: 3.14


   Các lớp dẫn xuất và client có thể gọi các phương thức sau để lấy một cấu trúc dữ liệu biểu diễn dấu vết ngăn xếp.

   .. method:: get_stack(f, t)

      Trả về một danh sách các tuple (frame, lineno) trong dấu vết ngăn xếp và một kích thước.

      frame được gọi gần đây nhất nằm ở cuối danh sách. Kích thước là số lượng frame bên dưới frame nơi debugger được gọi.

   .. method:: format_stack_entry(frame_lineno, lprefix=': ')

      Trả về một chuỗi chứa thông tin về một mục nhập ngăn xếp, là một tuple ``(frame, lineno)``. Chuỗi trả về chứa:

      * Tên tệp chuẩn chứa frame.
      * Tên hàm hoặc ``"<lambda>"``.
      * Các đối số đầu vào.
      * Giá trị trả về.
      * Dòng mã (nếu tồn tại).


   Hai phương thức sau có thể được client gọi để sử dụng debugger nhằm gỡ lỗi một :term:`statement`, được cung cấp dưới dạng chuỗi.

   .. method:: run(cmd, globals=None, locals=None)

      Gỡ lỗi một câu lệnh được thực thi thông qua hàm :func:`exec`. *globals* mặc định là :attr:`!__main__.__dict__`, còn *locals* mặc định là *globals*.

   .. method:: runeval(expr, globals=None, locals=None)

      Gỡ lỗi một biểu thức được thực thi thông qua hàm :func:`eval`. *globals* và *locals* có cùng ý nghĩa như trong :meth:`run`.

   .. method:: runctx(cmd, globals, locals)

      Để đảm bảo khả năng tương thích ngược. Gọi phương thức :meth:`run`.

   .. method:: runcall(func, /, *args, **kwds)

      Gỡ lỗi một lần gọi hàm đơn lẻ và trả về kết quả của lần gọi đó.


Cuối cùng, module định nghĩa các hàm sau:

.. function:: checkfuncname(b, frame)

   Trả về ``True`` nếu chúng ta nên dừng tại đây, tùy thuộc vào cách
   :class:`Breakpoint` *b* được đặt.

   Nếu được đặt thông qua số dòng, hàm sẽ kiểm tra xem
   :attr:`b.line <bdb.Breakpoint.line>` có giống với giá trị trong *frame* hay không. Nếu breakpoint được đặt thông qua
   :attr:`function name <bdb.Breakpoint.funcname>`, chúng ta phải kiểm tra xem mình có đang ở đúng *frame* (đúng hàm) và có đang ở dòng thực thi đầu tiên của hàm đó hay không.

.. function:: effective(file, line, frame)

   Trả về ``(active breakpoint, delete temporary flag)`` hoặc ``(None, None)`` làm breakpoint cần tác động.

   *điểm ngắt đang hoạt động* là mục nhập đầu tiên trong
   :attr:`bplist <bdb.Breakpoint.bplist>` cho (:attr:`file <bdb.Breakpoint.file>`, :attr:`line <bdb.Breakpoint.line>`) (phải tồn tại), đang :attr:`enabled <bdb.Breakpoint.enabled>`, mà :func:`checkfuncname` là true, và không có giá trị false
   :attr:`condition <bdb.Breakpoint.cond>` hoặc số lượng dương
   :attr:`ignore <bdb.Breakpoint.ignore>` số lượng. *Cờ*, có nghĩa là một breakpoint tạm thời nên được xóa, là ``False`` chỉ khi
   :attr:`cond <bdb.Breakpoint.cond>` không thể được đánh giá (trong trường hợp đó,
   số lượng :attr:`ignore <bdb.Breakpoint.ignore>` bị bỏ qua).

   Nếu không tồn tại mục nhập như vậy, thì ``(None, None)`` được trả về.


.. function:: set_trace()

   Bắt đầu gỡ lỗi bằng một instance :class:`Bdb` trong frame của caller.
