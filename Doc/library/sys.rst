:mod:`!sys` --- Các tham số và hàm dành riêng cho hệ thống
==========================================================

.. module:: sys
   :synopsis: Truy cập các tham số và hàm dành riêng cho hệ thống.

--------------

Module này cung cấp quyền truy cập vào một số biến được trình thông dịch sử dụng hoặc duy trì, cũng như các hàm tương tác chặt chẽ với trình thông dịch. Module này luôn khả dụng. Trừ khi có ghi chú rõ ràng khác, tất cả biến đều chỉ được đọc.


.. data:: abiflags

   Trên các hệ thống POSIX nơi Python được xây dựng bằng ``configure`` script tiêu chuẩn, giá trị này chứa các cờ ABI như được chỉ định bởi :pep:`3149`.

   .. versionadded:: 3.2

   .. versionchanged:: 3.8
      Các cờ mặc định trở thành một chuỗi rỗng (cờ ``m`` dành cho pymalloc đã bị loại bỏ).

   .. availability:: Unix.


.. function:: addaudithook(hook)

   Thêm callable *hook* vào danh sách các auditing hook đang hoạt động cho interpreter hiện tại (hoặc subinterpreter).

   Khi một auditing event được phát sinh thông qua hàm :func:`sys.audit`, mỗi hook sẽ được gọi theo thứ tự được thêm vào, cùng với tên event và tuple các đối số. Các native hook được thêm bằng :c:func:`PySys_AddAuditHook` sẽ được gọi trước, tiếp theo là các hook được thêm trong interpreter hiện tại (hoặc subinterpreter). Sau đó, các hook có thể ghi lại event, phát sinh exception để hủy thao tác hoặc chấm dứt hoàn toàn process.

   Lưu ý rằng audit hook chủ yếu dùng để thu thập thông tin về các hành động nội bộ hoặc không thể quan sát theo cách khác, dù do Python hay các thư viện được viết bằng Python thực hiện. Chúng không phù hợp để triển khai một "sandbox". Cụ thể, mã độc có thể dễ dàng vô hiệu hóa hoặc vượt qua các hook được thêm bằng hàm này. Tối thiểu, mọi hook liên quan đến bảo mật phải được thêm bằng C API :c:func:`PySys_AddAuditHook` trước khi khởi tạo runtime, và mọi module cho phép sửa đổi bộ nhớ tùy ý (chẳng hạn như :mod:`ctypes`) nên được loại bỏ hoàn toàn hoặc giám sát chặt chẽ.

   .. audit-event:: sys.addaudithook "" sys.addaudithook

      Việc gọi :func:`sys.addaudithook` tự nó sẽ phát sinh một auditing event có tên ``sys.addaudithook`` mà không có đối số. Nếu bất kỳ hook hiện có nào phát sinh một ngoại lệ dẫn xuất từ :class:`RuntimeError`, hook mới sẽ không được thêm vào và ngoại lệ sẽ bị loại bỏ. Do đó, bên gọi không thể giả định rằng hook của mình đã được thêm vào, trừ khi họ kiểm soát tất cả hook hiện có.

   Xem :ref:`bảng các audit event <audit-events>` để biết tất cả event do CPython phát sinh, và :pep:`578` để xem thảo luận thiết kế ban đầu.

   .. versionadded:: 3.8

   .. versionchanged:: 3.8.1

      Các ngoại lệ dẫn xuất từ :class:`Exception` nhưng không phải từ :class:`RuntimeError` sẽ không còn bị loại bỏ.

   .. impl-detail::

      Khi tracing được bật (xem :func:`settrace`), các hook Python chỉ được trace nếu callable có một thành viên ``__cantrace__`` được đặt thành giá trị true. Nếu không, các hàm trace sẽ bỏ qua hook.


.. data:: argv

   Danh sách các đối số dòng lệnh được truyền cho một Python script. ``argv[0]`` là tên script (việc đây có phải là tên đường dẫn đầy đủ hay không phụ thuộc vào hệ điều hành). Nếu lệnh được thực thi bằng tùy chọn dòng lệnh :option:`-c` của interpreter, ``argv[0]`` sẽ được đặt thành chuỗi ``'-c'``. Nếu không truyền tên script cho Python interpreter, ``argv[0]`` là chuỗi rỗng.

   Để lặp qua đầu vào chuẩn hoặc danh sách các tệp được cung cấp trên dòng lệnh, hãy xem module :mod:`fileinput`.

   Xem thêm :data:`sys.orig_argv`.

   .. note::
      Trên Unix, các đối số dòng lệnh được hệ điều hành truyền dưới dạng byte. Python giải mã chúng bằng encoding của hệ thống tệp và trình xử lý lỗi "surrogateescape". Khi cần các byte ban đầu, bạn có thể lấy chúng bằng ``[os.fsencode(arg) for arg in sys.argv]``.


.. _auditing:

.. function:: audit(event, *args)

   .. index:: single: auditing

   Phát sinh một sự kiện auditing và kích hoạt mọi hook auditing đang hoạt động. *event* là một chuỗi xác định sự kiện, còn *args* có thể chứa các đối số tùy chọn với thêm thông tin về sự kiện. Số lượng và kiểu của các đối số đối với một sự kiện nhất định được xem là một API công khai và ổn định, đồng thời không nên bị thay đổi giữa các bản phát hành.

   Ví dụ, một sự kiện auditing có tên là ``os.chdir``. Sự kiện này có một đối số tên là *path*, chứa thư mục làm việc mới được yêu cầu.

   :func:`sys.audit` sẽ gọi các hook auditing hiện có, truyền tên sự kiện và các đối số, đồng thời sẽ phát sinh lại ngoại lệ đầu tiên từ bất kỳ hook nào. Nhìn chung, nếu một ngoại lệ được phát sinh, không nên xử lý ngoại lệ đó và tiến trình nên được kết thúc nhanh nhất có thể. Điều này cho phép các triển khai hook quyết định cách phản hồi với từng sự kiện cụ thể: chúng chỉ có thể ghi nhật ký sự kiện hoặc hủy bỏ thao tác bằng cách phát sinh một ngoại lệ.

   Các hook được thêm bằng :func:`sys.addaudithook` hoặc
   các hàm :c:func:`PySys_AddAuditHook`.

   Tương đương bản địa của hàm này là :c:func:`PySys_Audit`. Khi có thể, nên sử dụng hàm bản địa.

   Xem :ref:`bảng các sự kiện audit <audit-events>` để biết tất cả các sự kiện do CPython phát sinh.

   .. versionadded:: 3.8


.. data:: base_exec_prefix

   Tương đương với :data:`exec_prefix`, nhưng tham chiếu đến bản cài đặt Python cơ sở.

   Khi chạy trong :ref:`sys-path-init-virtual-environments`,
   :data:`exec_prefix` bị ghi đè thành tiền tố của môi trường ảo.
   Ngược lại, :data:`base_exec_prefix` không thay đổi và luôn trỏ đến bản cài đặt Python cơ sở. Xem :ref:`sys-path-init-virtual-environments` để biết thêm thông tin.

   .. versionadded:: 3.3


.. data:: base_prefix

   Tương đương với :data:`prefix`, nhưng tham chiếu đến bản cài đặt Python cơ sở.

   Khi chạy trong :ref:`môi trường ảo <venv-def>`,
   :data:`prefix` sẽ bị ghi đè bằng tiền tố của môi trường ảo.
   Ngược lại, :data:`base_prefix` không thay đổi và luôn trỏ đến bản cài đặt Python cơ sở. Tham khảo :ref:`sys-path-init-virtual-environments` để biết thêm thông tin.

   .. versionadded:: 3.3


.. data:: byteorder

   Chỉ báo về thứ tự byte gốc. Giá trị này sẽ là ``'big'`` trên các nền tảng big-endian (byte có ý nghĩa lớn nhất đứng trước), và ``'little'`` trên các nền tảng little-endian (byte có ý nghĩa nhỏ nhất đứng trước).


.. data:: builtin_module_names

   Một tuple gồm các chuỗi chứa tên của tất cả module được biên dịch vào trình thông dịch Python này. (Thông tin này không thể lấy bằng cách nào khác --- ``modules.keys()`` chỉ liệt kê các module đã được import.)

   Xem thêm danh sách :data:`sys.stdlib_module_names`.


.. function:: call_tracing(func, args)

   Gọi ``func(*args)`` khi tracing đang được bật. Trạng thái tracing được lưu lại và khôi phục sau đó. Hàm này được gọi từ một debugger tại một checkpoint, nhằm debug hoặc profile đệ quy một số mã khác.

   Việc tracing bị tạm ngưng khi gọi một hàm tracing được thiết lập bởi
   :func:`settrace` hoặc :func:`setprofile` để tránh đệ quy vô hạn.
   :func:`!call_tracing` cho phép hàm tracing đệ quy một cách tường minh.


.. data:: copyright

   Một chuỗi chứa thông tin bản quyền liên quan đến trình thông dịch Python.


.. function:: _clear_type_cache()

   Xóa bộ nhớ đệm kiểu nội bộ. Bộ nhớ đệm kiểu được dùng để tăng tốc việc tra cứu thuộc tính và phương thức. Chỉ sử dụng hàm *only* để loại bỏ các tham chiếu không cần thiết trong quá trình gỡ lỗi rò rỉ tham chiếu.

   Chỉ nên sử dụng hàm này cho các mục đích nội bộ và chuyên biệt.

   .. deprecated:: 3.13
      Thay vào đó, hãy sử dụng hàm :func:`_clear_internal_caches` tổng quát hơn.


.. function:: _clear_internal_caches()

   Xóa tất cả bộ nhớ đệm nội bộ liên quan đến hiệu năng. Chỉ sử dụng hàm này *chỉ* để giải phóng các tham chiếu và khối bộ nhớ không cần thiết khi tìm kiếm rò rỉ.

   .. versionadded:: 3.13


.. function:: _current_frames()

   Trả về một dictionary ánh xạ mã định danh của mỗi thread tới stack frame trên cùng hiện đang hoạt động trong thread đó tại thời điểm hàm được gọi. Lưu ý rằng các hàm trong module :mod:`traceback` có thể dựng call stack dựa trên một frame như vậy.

   Điều này hữu ích nhất khi gỡ lỗi deadlock: hàm này không yêu cầu các thread bị deadlock phải phối hợp, và call stack của các thread đó sẽ bị đóng băng chừng nào chúng vẫn còn bị deadlock. Frame được trả về cho một thread không bị deadlock có thể không liên quan gì đến hoạt động hiện tại của thread đó vào thời điểm mã gọi kiểm tra frame.

   Chỉ nên sử dụng hàm này cho các mục đích nội bộ và chuyên biệt.

   .. audit-event:: sys._current_frames "" sys._current_frames

.. function:: _current_exceptions()

   Trả về một dictionary ánh xạ mã định danh của mỗi thread tới exception trên cùng hiện đang hoạt động trong thread đó tại thời điểm hàm được gọi. Nếu một thread hiện không đang xử lý exception, thread đó sẽ không được đưa vào dictionary kết quả.

   Điều này hữu ích nhất cho việc profiling thống kê.

   Chỉ nên sử dụng hàm này cho các mục đích nội bộ và chuyên biệt.

   .. audit-event:: sys._current_exceptions "" sys._current_exceptions

   .. versionchanged:: 3.12
      Mỗi giá trị trong từ điển giờ đây là một instance ngoại lệ duy nhất, thay vì một bộ 3 phần tử như được trả về từ ``sys.exc_info()``.

.. function:: breakpointhook()

   Hàm hook này được gọi bởi :func:`breakpoint` tích hợp sẵn. Theo mặc định, hàm đưa bạn vào trình gỡ lỗi :mod:`pdb`, nhưng có thể được đặt thành bất kỳ hàm nào khác để bạn chọn trình gỡ lỗi sẽ được sử dụng.

   Chữ ký của hàm này phụ thuộc vào hàm mà nó gọi. Ví dụ, binding mặc định (chẳng hạn như ``pdb.set_trace()``) không yêu cầu đối số, nhưng bạn có thể liên kết nó với một hàm yêu cầu thêm đối số (đối số vị trí và/hoặc từ khóa). Hàm ``breakpoint()`` tích hợp sẵn truyền thẳng ``*args`` và ``**kws`` của nó. Bất kỳ giá trị nào ``breakpointhooks()`` trả về cũng được trả về từ ``breakpoint()``.

   Triển khai mặc định trước tiên kiểm tra biến môi trường
   :envvar:`PYTHONBREAKPOINT`. Nếu biến này được đặt thành ``"0"`` thì hàm này trả về ngay lập tức; tức là không thực hiện thao tác nào. Nếu biến môi trường chưa được đặt hoặc được đặt thành chuỗi rỗng, ``pdb.set_trace()`` sẽ được gọi. Nếu không, biến này phải chỉ rõ một hàm cần chạy, sử dụng quy ước dotted-import của Python, chẳng hạn như ``package.subpackage.module.function``. Trong trường hợp này, ``package.subpackage.module`` sẽ được import và module thu được phải có một hàm có thể gọi được với tên ``function()``. Hàm này được chạy với ``*args`` và ``**kws`` làm đối số, đồng thời bất kỳ giá trị nào ``function()`` trả về cũng được ``sys.breakpointhook()`` trả về cho hàm :func:`breakpoint` tích hợp sẵn.

   Lưu ý rằng nếu xảy ra bất kỳ lỗi nào trong khi import hàm có tên
   :envvar:`PYTHONBREAKPOINT`, một :exc:`RuntimeWarning` sẽ được báo cáo và breakpoint sẽ bị bỏ qua.

   Cũng lưu ý rằng nếu ``sys.breakpointhook()`` bị ghi đè theo chương trình,
   :envvar:`PYTHONBREAKPOINT` được *không* tham vấn.

   .. versionadded:: 3.7

.. function:: _debugmallocstats()

   In thông tin cấp thấp vào stderr về trạng thái của bộ cấp phát bộ nhớ của CPython.

   Nếu Python được :ref:`biên dịch ở chế độ debug <debug-build>` (:option:`configure --with-pydebug option <--with-pydebug>`), Python cũng thực hiện một số kiểm tra tính nhất quán nội bộ tốn kém.

   .. versionadded:: 3.3

   .. impl-detail::

      Hàm này chỉ dành riêng cho CPython. Định dạng đầu ra chính xác không được định nghĩa ở đây và có thể thay đổi.


.. data:: dllhandle

   Số nguyên chỉ định handle của Python DLL.

   .. availability:: Windows.


.. function:: displayhook(value)

   Nếu *value* không phải là ``None``, hàm này in ``repr(value)`` vào ``sys.stdout`` và lưu *value* trong ``builtins._``. Nếu ``repr(value)`` không thể mã hóa thành ``sys.stdout.encoding`` bằng trình xử lý lỗi ``sys.stdout.errors`` (có lẽ là ``'strict'``), hãy mã hóa nó thành ``sys.stdout.encoding`` bằng trình xử lý lỗi ``'backslashreplace'``.

   ``sys.displayhook`` được gọi trên kết quả của việc đánh giá một :term:`expression` được nhập trong một phiên Python tương tác. Việc hiển thị các giá trị này có thể được tùy chỉnh bằng cách gán một hàm nhận một đối số khác cho ``sys.displayhook``.

   Mã giả::

       def displayhook(value):
           if value is None:
               return
           # Đặt '_' thành None để tránh đệ quy
           builtins._ = None
           text = repr(value)
           try:
               sys.stdout.write(text)
           except UnicodeEncodeError:
               bytes = text.encode(sys.stdout.encoding, 'backslashreplace')
               if hasattr(sys.stdout, 'buffer'):
                   sys.stdout.buffer.write(bytes)
               else:
                   text = bytes.decode(sys.stdout.encoding, 'strict')
                   sys.stdout.write(text)
           sys.stdout.write("\n")
           builtins._ = value

   .. versionchanged:: 3.2
      Sử dụng trình xử lý lỗi ``'backslashreplace'`` trên :exc:`UnicodeEncodeError`.


.. data:: dont_write_bytecode

   Nếu giá trị này là true, Python sẽ không cố ghi các tệp ``.pyc`` khi import các module mã nguồn. Ban đầu, giá trị này được đặt thành ``True`` hoặc ``False`` tùy thuộc vào tùy chọn dòng lệnh :option:`-B` và biến môi trường
   :envvar:`PYTHONDONTWRITEBYTECODE`, nhưng bạn có thể tự đặt giá trị này để kiểm soát việc tạo tệp bytecode.


.. data:: _emscripten_info

   Một :term:`named tuple` chứa thông tin về môi trường trên nền tảng *wasm32-emscripten*. Named tuple này chỉ mang tính tạm thời và có thể thay đổi trong tương lai.

   .. attribute:: _emscripten_info.emscripten_version

      Phiên bản Emscripten dưới dạng tuple gồm các số nguyên (major, minor, micro), ví dụ ``(3, 1, 8)``.

   .. attribute:: _emscripten_info.runtime

      Chuỗi runtime, ví dụ như user agent của trình duyệt, ``'Node.js v14.18.2'`` hoặc ``'UNKNOWN'``.

   .. attribute:: _emscripten_info.pthreads

      ``True`` nếu Python được biên dịch với hỗ trợ pthreads của Emscripten.

   .. attribute:: _emscripten_info.shared_memory

      ``True`` nếu Python được biên dịch với hỗ trợ shared memory.

   .. availability:: Emscripten.

   .. versionadded:: 3.11


.. data:: pycache_prefix

   Nếu được thiết lập (không phải ``None``), Python sẽ ghi các tệp ``.pyc`` bộ nhớ đệm bytecode vào (và đọc chúng từ) một cây thư mục song song có thư mục gốc là thư mục này, thay vì từ các thư mục ``__pycache__`` trong cây mã nguồn. Mọi thư mục ``__pycache__`` trong cây mã nguồn sẽ bị bỏ qua và các tệp ``.pyc`` mới sẽ được ghi trong tiền tố pycache. Do đó, nếu bạn sử dụng
   :mod:`compileall` như một bước trước khi build, bạn phải đảm bảo chạy nó với cùng tiền tố pycache (nếu có) mà bạn sẽ sử dụng khi runtime.

   Đường dẫn tương đối được diễn giải tương đối so với thư mục làm việc hiện tại.

   Giá trị này ban đầu được thiết lập dựa trên giá trị của tùy chọn dòng lệnh :option:`-X` ``pycache_prefix=PATH`` hoặc
   biến môi trường :envvar:`PYTHONPYCACHEPREFIX` (tùy chọn dòng lệnh được ưu tiên). Nếu cả hai đều chưa được thiết lập, giá trị là ``None``.

   .. versionadded:: 3.8


.. function:: excepthook(type, value, traceback)

   Hàm này in traceback và exception đã cho ra ``sys.stderr``.

   Khi một exception khác :exc:`SystemExit` được raise và không được bắt, interpreter sẽ gọi ``sys.excepthook`` với ba đối số: class của exception, instance của exception và một đối tượng traceback. Trong một phiên tương tác, việc này xảy ra ngay trước khi quyền điều khiển được trả về prompt; trong một chương trình Python, việc này xảy ra ngay trước khi chương trình kết thúc. Việc xử lý các top-level exception như vậy có thể được tùy chỉnh bằng cách gán một hàm khác nhận ba đối số cho ``sys.excepthook``.

   .. audit-event:: sys.excepthook hook,type,value,traceback sys.excepthook

      Phát sinh một auditing event ``sys.excepthook`` với các đối số ``hook``, ``type``, ``value``, ``traceback`` khi xảy ra một exception không được bắt. Nếu chưa có hook nào được thiết lập, ``hook`` có thể là ``None``. Nếu bất kỳ hook nào raise một exception kế thừa từ :class:`RuntimeError`, lệnh gọi hook sẽ bị bỏ qua. Nếu không, exception của audit hook sẽ được báo cáo là không thể raise và ``sys.excepthook`` sẽ được gọi.

   .. seealso::

      Hàm :func:`sys.unraisablehook` xử lý các exception không thể raise và hàm :func:`threading.excepthook` xử lý exception do :func:`threading.Thread.run` raise.


.. data:: __breakpointhook__
          __displayhook__ __excepthook__ __unraisablehook__

   Các đối tượng này chứa các giá trị ban đầu của ``breakpointhook``, ``displayhook``, ``excepthook`` và ``unraisablehook`` tại thời điểm chương trình bắt đầu. Chúng được lưu lại để ``breakpointhook``, ``displayhook`` và ``excepthook``, ``unraisablehook`` có thể được khôi phục trong trường hợp chúng bị thay thế bằng các đối tượng bị lỗi hoặc đối tượng thay thế.

   .. versionadded:: 3.7
      __breakpointhook__

   .. versionadded:: 3.8
      __unraisablehook__


.. function:: exception()

   Khi được gọi trong lúc một trình xử lý exception đang thực thi (chẳng hạn như mệnh đề ``except`` hoặc ``except*``), hàm này trả về instance exception đã được trình xử lý này bắt. Khi các trình xử lý exception được lồng trong nhau, chỉ exception được xử lý bởi trình xử lý bên trong cùng mới có thể truy cập được.

   Nếu không có trình xử lý exception nào đang thực thi, hàm này trả về ``None``.

   .. versionadded:: 3.11


.. function:: exc_info()

   Hàm này trả về biểu diễn kiểu cũ của exception đang được xử lý. Nếu một ``e`` exception hiện đang được xử lý (vì vậy
   :func:`exception` sẽ trả về ``e``), :func:`exc_info` trả về tuple ``(type(e), e, e.__traceback__)``. Nghĩa là, một tuple chứa kiểu của exception (một lớp con của
   :exc:`BaseException`), bản thân ngoại lệ và một :ref:`đối tượng traceback <traceback-objects>` thường đóng gói ngăn xếp lời gọi tại thời điểm ngoại lệ xảy ra lần cuối.

   .. index:: pair: object; traceback

   Nếu không có ngoại lệ nào đang được xử lý ở bất kỳ vị trí nào trên ngăn xếp, hàm này trả về một tuple chứa ba giá trị ``None``.

   .. versionchanged:: 3.11
      Các trường ``type`` và ``traceback`` hiện được lấy từ ``value`` (instance của ngoại lệ), vì vậy khi một ngoại lệ được sửa đổi trong lúc đang được xử lý, những thay đổi đó sẽ được phản ánh trong kết quả của các lần gọi :func:`exc_info` tiếp theo.

.. data:: exec_prefix

   Một chuỗi chỉ định tiền tố thư mục dành riêng cho từng hệ thống, nơi các tệp Python phụ thuộc vào nền tảng được cài đặt; theo mặc định, đây cũng là ``'/usr/local'``.  Có thể thiết lập giá trị này trong thời gian build bằng đối số ``--exec-prefix`` cho
   tập lệnh :program:`configure`.  Cụ thể, tất cả các tệp cấu hình (ví dụ: tệp
   header :file:`pyconfig.h`) được cài đặt trong thư mục
   :file:`{exec_prefix}/lib/python{X.Y}/config`, còn các module thư viện dùng chung được cài đặt trong :file:`{exec_prefix}/lib/python{X.Y}/lib-dynload`, trong đó *X.Y* là số phiên bản của Python, ví dụ ``3.2``.

   .. note::

      Nếu một :ref:`môi trường ảo <venv-def>` đang được áp dụng, :data:`exec_prefix` này sẽ trỏ đến môi trường ảo. Giá trị của bản cài đặt Python vẫn khả dụng thông qua :data:`base_exec_prefix`. Xem :ref:`sys-path-init-virtual-environments` để biết thêm thông tin.

   .. versionchanged:: 3.14

      Khi chạy trong :ref:`môi trường ảo <venv-def>`,
      :data:`prefix` và :data:`exec_prefix` hiện được :ref:`khởi tạo đường dẫn <sys-path-init>` đặt thành tiền tố của môi trường ảo, thay vì :mod:`site`. Điều này có nghĩa là :data:`prefix` và
      :data:`exec_prefix` luôn trỏ đến môi trường ảo, ngay cả khi
      :mod:`site` bị vô hiệu hóa (:option:`-S`).

.. data:: executable

   Một chuỗi cung cấp đường dẫn tuyệt đối đến tệp nhị phân thực thi của trình thông dịch Python, trên các hệ thống mà điều này có ý nghĩa. Nếu Python không thể lấy đường dẫn thực đến tệp thực thi của nó, :data:`sys.executable` sẽ là một chuỗi rỗng hoặc ``None``.


.. function:: exit([arg])

   Ném một ngoại lệ :exc:`SystemExit`, báo hiệu ý định thoát khỏi trình thông dịch.

   Đối số tùy chọn *arg* có thể là một số nguyên chỉ trạng thái thoát (mặc định là 0) hoặc một kiểu đối tượng khác. Nếu là số nguyên, shell và các chương trình tương tự coi 0 là “kết thúc thành công” và mọi giá trị khác 0 là “kết thúc bất thường”. Hầu hết các hệ thống yêu cầu giá trị này nằm trong phạm vi 0--127 và cho kết quả không xác định nếu không thuộc phạm vi đó. Một số hệ thống có quy ước gán ý nghĩa cụ thể cho từng mã thoát cụ thể, nhưng nhìn chung các quy ước này chưa được phát triển đầy đủ; các chương trình Unix thường dùng 2 cho lỗi cú pháp dòng lệnh và 1 cho mọi loại lỗi khác. Nếu truyền vào một kiểu đối tượng khác, ``None`` tương đương với việc truyền 0, còn mọi đối tượng khác sẽ được in ra :data:`stderr` và dẫn đến mã thoát là 1. Cụ thể, ``sys.exit("some error message")`` là cách nhanh để thoát khỏi chương trình khi xảy ra lỗi.

   Vì :func:`exit` rốt cuộc “chỉ” phát sinh một exception, nó chỉ thoát khỏi tiến trình khi được gọi từ main thread và exception đó không bị chặn. Các thao tác dọn dẹp được chỉ định trong mệnh đề finally của các câu lệnh :keyword:`try` vẫn được thực hiện, và có thể chặn nỗ lực thoát ở một cấp bên ngoài.

   .. versionchanged:: 3.6
      Nếu xảy ra lỗi trong quá trình dọn dẹp sau khi trình thông dịch Python đã bắt được :exc:`SystemExit` (chẳng hạn như lỗi khi flush dữ liệu đã đệm trong các stream tiêu chuẩn), trạng thái thoát sẽ được đổi thành 120.


.. data:: flags

   :term:`named tuple` *flags* cung cấp trạng thái của các cờ dòng lệnh. Chỉ được truy cập các cờ theo tên, không truy cập theo chỉ mục. Các thuộc tính này chỉ được đọc.

   .. list-table::

      * - .. attribute:: flags.debug
        - :option:`-d`

      * - .. attribute:: flags.inspect
        - :option:`-i`

      * - .. attribute:: flags.interactive
        - :option:`-i`

      * - .. attribute:: flags.isolated
        - :option:`-I`

      * - .. attribute:: flags.optimize
        - :option:`-O` hoặc :option:`-OO`

      * - .. attribute:: flags.dont_write_bytecode
        - :option:`-B`

      * - .. attribute:: flags.no_user_site
        - :option:`-s`

      * - .. attribute:: flags.no_site
        - :option:`-S`

      * - .. attribute:: flags.ignore_environment
        - :option:`-E`

      * - .. attribute:: flags.verbose
        - :option:`-v`

      * - .. attribute:: flags.bytes_warning
        - :option:`-b`

      * - .. attribute:: flags.quiet
        - :option:`-q`

      * - .. attribute:: flags.hash_randomization
        - :option:`-R`

      * - .. attribute:: flags.dev_mode
        - :option:`-X dev <-X>` (:ref:`Python Development Mode <devmode>`)

      * - .. attribute:: flags.utf8_mode
        - :option:`-X utf8 <-X>`

      * - .. attribute:: flags.safe_path
        - :option:`-P`

      * - .. attribute:: flags.int_max_str_digits
        - :option:`-X int_max_str_digits <-X>` (:ref:`integer string conversion length limitation <int_max_str_digits>`)

      * - .. attribute:: flags.warn_default_encoding
        - :option:`-X warn_default_encoding <-X>`

      * - .. attribute:: flags.gil
        - :option:`-X gil <-X>` và :envvar:`PYTHON_GIL`

      * - .. attribute:: flags.thread_inherit_context
        - :option:`-X thread_inherit_context <-X>` và
          :envvar:`PYTHON_THREAD_INHERIT_CONTEXT`

      * - .. attribute:: flags.context_aware_warnings
        - :option:`-X context_aware_warnings <-X>` và
          :envvar:`PYTHON_CONTEXT_AWARE_WARNINGS`


   .. versionchanged:: 3.2
      Đã thêm thuộc tính ``quiet`` cho cờ :option:`-q` mới.

   .. versionadded:: 3.2.3
      Thuộc tính ``hash_randomization``.

   .. versionchanged:: 3.3
      Đã xóa thuộc tính ``division_warning`` đã lỗi thời.

   .. versionchanged:: 3.4
      Đã thêm thuộc tính ``isolated`` cho cờ :option:`-I` ``isolated``.

   .. versionchanged:: 3.7
      Đã thêm thuộc tính ``dev_mode`` cho :ref:`Python Development Mode <devmode>` mới và thuộc tính ``utf8_mode`` cho cờ :option:`-X` ``utf8`` mới.

   .. versionchanged:: 3.10
      Đã thêm thuộc tính ``warn_default_encoding`` cho cờ :option:`-X` ``warn_default_encoding``.

   .. versionchanged:: 3.11
      Đã thêm thuộc tính ``safe_path`` cho tùy chọn :option:`-P`.

   .. versionchanged:: 3.11
      Đã thêm thuộc tính ``int_max_str_digits``.

   .. versionchanged:: 3.13
      Đã thêm thuộc tính ``gil``.

   .. versionchanged:: 3.14
      Đã thêm thuộc tính ``thread_inherit_context``.

   .. versionchanged:: 3.14
      Đã thêm thuộc tính ``context_aware_warnings``.


.. data:: float_info

   Một :term:`named tuple` chứa thông tin về kiểu float. Nó chứa thông tin cấp thấp về độ chính xác và biểu diễn nội bộ. Các giá trị tương ứng với những hằng số dấu phẩy động khác nhau được định nghĩa trong tệp tiêu đề chuẩn :file:`float.h` của ngôn ngữ lập trình 'C'; xem mục 5.2.4.2.2, 'Characteristics of floating types', trong tiêu chuẩn ISO/IEC C năm 1999 [C99]_ để biết chi tiết.

   .. list-table:: Các thuộc tính của :data:`!float_info` :term:`named tuple`
      :header-rows: 1

      * - thuộc tính
        - macro float.h
        - giải thích

      * - .. attribute:: float_info.epsilon
        - :c:macro:`!DBL_EPSILON`
        - chênh lệch giữa 1.0 và giá trị nhỏ nhất lớn hơn 1.0 có thể biểu diễn dưới dạng float.

          Xem thêm :func:`math.ulp`.

      * - .. attribute:: float_info.dig
        - :c:macro:`!DBL_DIG`
        - Số chữ số thập phân tối đa có thể được biểu diễn chính xác trong một float; xem bên dưới.

      * - .. attribute:: float_info.mant_dig
        - :c:macro:`!DBL_MANT_DIG`
        - Độ chính xác của float: số chữ số theo cơ số ``radix`` trong phần định trị của một float.

      * - .. attribute:: float_info.max
        - :c:macro:`!DBL_MAX`
        - Float hữu hạn dương lớn nhất có thể biểu diễn.

      * - .. attribute:: float_info.max_exp
        - :c:macro:`!DBL_MAX_EXP`
        - Số nguyên lớn nhất *e* sao cho ``radix**(e-1)`` là một float hữu hạn có thể biểu diễn.

      * - .. attribute:: float_info.max_10_exp
        - :c:macro:`!DBL_MAX_10_EXP`
        - Số nguyên lớn nhất *e* sao cho ``10**e`` nằm trong phạm vi các float hữu hạn có thể biểu diễn.

      * - .. attribute:: float_info.min
        - :c:macro:`!DBL_MIN`
        - Float dương *normalized* nhỏ nhất có thể biểu diễn.

          Sử dụng :func:`math.ulp(0.0) <math.ulp>` để lấy float dương *denormalized* nhỏ nhất có thể biểu diễn.

      * - .. attribute:: float_info.min_exp
        - :c:macro:`!DBL_MIN_EXP`
        - Số nguyên nhỏ nhất *e* sao cho ``radix**(e-1)`` là một số thực dấu phẩy động đã chuẩn hóa.

      * - .. attribute:: float_info.min_10_exp
        - :c:macro:`!DBL_MIN_10_EXP`
        - Số nguyên nhỏ nhất *e* sao cho ``10**e`` là một số thực dấu phẩy động đã chuẩn hóa.

      * - .. attribute:: float_info.radix
        - :c:macro:`!FLT_RADIX`
        - Cơ số của biểu diễn số mũ.

      * - .. attribute:: float_info.rounds
        - :c:macro:`!FLT_ROUNDS`
        - Một số nguyên biểu thị chế độ làm tròn cho phép tính số thực dấu phẩy động. Giá trị này phản ánh giá trị của macro hệ thống :c:macro:`!FLT_ROUNDS` tại thời điểm khởi động trình thông dịch:

          * ``-1``: về phía 0
          * ``0``: về 0
          * ``1``: đến số gần nhất
          * ``2``: hướng tới dương vô cùng
          * ``3``: hướng tới âm vô cùng

          Mọi giá trị khác của :c:macro:`!FLT_ROUNDS` đều mô tả hành vi làm tròn do việc triển khai xác định.

   Thuộc tính :attr:`sys.float_info.dig` cần được giải thích thêm. Nếu ``s`` là một chuỗi bất kỳ biểu diễn một số thập phân có nhiều nhất
   :attr:`!sys.float_info.dig` chữ số có nghĩa, thì việc chuyển ``s`` sang float rồi chuyển ngược lại sẽ khôi phục một chuỗi biểu diễn cùng giá trị thập phân::

      >>> import sys
      >>> sys.float_info.dig
      15
      >>> s = '3.14159265358979'    # chuỗi thập phân có 15 chữ số có nghĩa
      >>> format(float(s), '.15g')  # chuyển sang float rồi chuyển ngược lại -> cùng giá trị
      '3.14159265358979'

   Tuy nhiên, đối với các chuỗi có nhiều hơn :attr:`sys.float_info.dig` chữ số có nghĩa thì điều này không phải lúc nào cũng đúng::

      >>> s = '9876543211234567'    # 16 chữ số có nghĩa là quá nhiều!
      >>> format(float(s), '.16g')  # việc chuyển đổi làm thay đổi giá trị
      '9876543211234568'

.. data:: float_repr_style

   Một chuỗi cho biết cách hàm :func:`repr` hoạt động với các số thực. Nếu chuỗi có giá trị ``'short'`` thì đối với một số thực hữu hạn ``x``, ``repr(x)`` cố gắng tạo ra một chuỗi ngắn có tính chất ``float(repr(x)) == x``. Đây là hành vi thông thường trong Python 3.1 trở lên. Nếu không, ``float_repr_style`` có giá trị ``'legacy'`` và ``repr(x)`` hoạt động giống như trong các phiên bản Python trước 3.1.

   .. versionadded:: 3.1


.. function:: getallocatedblocks()

   Trả về số khối bộ nhớ hiện đang được interpreter cấp phát, bất kể kích thước của chúng. Hàm này chủ yếu hữu ích để theo dõi và gỡ lỗi rò rỉ bộ nhớ. Do các bộ nhớ đệm nội bộ của interpreter, kết quả có thể thay đổi sau mỗi lần gọi; bạn có thể phải gọi
   :func:`_clear_internal_caches` và :func:`gc.collect` để nhận được kết quả dễ dự đoán hơn.

   Nếu một bản dựng hoặc bản triển khai Python không thể tính toán hợp lý thông tin này, :func:`getallocatedblocks` được phép trả về 0 thay thế.

   .. versionadded:: 3.4


.. function:: getunicodeinternedsize()

   Trả về số lượng đối tượng unicode đã được intern.

   .. versionadded:: 3.12


.. function:: getandroidapilevel()

   Trả về cấp API của Android tại thời điểm build dưới dạng số nguyên. Giá trị này biểu thị phiên bản Android tối thiểu mà bản build Python này có thể chạy trên đó. Để biết thông tin phiên bản runtime, xem :func:`platform.android_ver`.

   .. availability:: Android.

   .. versionadded:: 3.7


.. function:: getdefaultencoding()

   Trả về ``'utf-8'``. Đây là tên của encoding chuỗi mặc định, được sử dụng trong các phương thức như :meth:`str.encode`.


.. function:: getdlopenflags()

   Trả về giá trị hiện tại của các cờ được sử dụng cho
   các lệnh gọi :c:func:`dlopen`. Có thể tìm thấy tên tượng trưng của các giá trị cờ trong module :mod:`os` (các hằng số :samp:`RTLD_{xxx}`, chẳng hạn như
   :const:`os.RTLD_LAZY`).

   .. availability:: Unix.


.. function:: getfilesystemencoding()

   Lấy :term:`filesystem encoding <filesystem encoding and error handler>`: encoding được sử dụng cùng với :term:`filesystem error handler <filesystem encoding and error handler>` để chuyển đổi giữa tên tệp Unicode và tên tệp dạng byte. Filesystem error handler được trả về từ
   :func:`getfilesystemencodeerrors`.

   Để có khả năng tương thích tốt nhất, nên sử dụng str cho tên tệp trong mọi trường hợp, mặc dù việc biểu diễn tên tệp dưới dạng byte cũng được hỗ trợ. Các hàm nhận hoặc trả về tên tệp phải hỗ trợ cả str lẫn bytes và chuyển đổi nội bộ sang dạng biểu diễn được hệ thống ưu tiên.

   :func:`os.fsencode` và :func:`os.fsdecode` nên được sử dụng để đảm bảo sử dụng đúng chế độ mã hóa và xử lý lỗi.

   :term:`filesystem encoding and error handler` được cấu hình khi Python khởi động bằng hàm :c:func:`PyConfig_Read`: xem
   :c:member:`~PyConfig.filesystem_encoding` và
   các thành viên :c:member:`~PyConfig.filesystem_errors` của :c:type:`PyConfig`.

   .. versionchanged:: 3.2
      :func:`getfilesystemencoding` result cannot be ``None`` anymore.

   .. versionchanged:: 3.6
      Windows không còn được đảm bảo sẽ trả về ``'mbcs'``. Xem :pep:`529` và :func:`_enablelegacywindowsfsencoding` để biết thêm thông tin.

   .. versionchanged:: 3.7
      Trả về ``'utf-8'`` nếu :ref:`Python UTF-8 Mode <utf8-mode>` được bật.


.. function:: getfilesystemencodeerrors()

   Lấy :term:`filesystem error handler <filesystem encoding and error handler>`: trình xử lý lỗi được sử dụng cùng với :term:`filesystem encoding <filesystem encoding and error handler>` để chuyển đổi giữa tên tệp Unicode và tên tệp dạng byte. Mã hóa hệ thống tệp được trả về từ
   :func:`getfilesystemencoding`.

   :func:`os.fsencode` và :func:`os.fsdecode` nên được sử dụng để đảm bảo sử dụng đúng chế độ mã hóa và xử lý lỗi.

   :term:`filesystem encoding and error handler` được cấu hình khi Python khởi động bằng hàm :c:func:`PyConfig_Read`: xem
   :c:member:`~PyConfig.filesystem_encoding` và
   các thành viên :c:member:`~PyConfig.filesystem_errors` của :c:type:`PyConfig`.

   .. versionadded:: 3.6

.. function:: get_int_max_str_digits()

   Trả về giá trị hiện tại của :ref:`giới hạn độ dài chuyển đổi chuỗi số nguyên <int_max_str_digits>`. Xem thêm :func:`set_int_max_str_digits`.

   .. versionadded:: 3.11

.. function:: getrefcount(object)

   Trả về số lượng tham chiếu của *đối tượng*. Số lượng được trả về thường cao hơn một đơn vị so với bạn dự kiến, vì nó bao gồm tham chiếu (tạm thời) đến đối số của :func:`getrefcount`.

   Lưu ý rằng giá trị được trả về có thể không thực sự phản ánh có bao nhiêu tham chiếu đang được giữ tới đối tượng. Ví dụ, một số đối tượng là :term:`immortal` và có refcount rất cao, không phản ánh số lượng tham chiếu thực tế. Vì vậy, đừng dựa vào giá trị được trả về để cho là chính xác, ngoại trừ khi giá trị đó là 0 hoặc 1.

   .. impl-detail::

      Các đối tượng :term:`Immortal <immortal>` có số lượng tham chiếu lớn có thể được xác định thông qua :func:`_is_immortal`.

   .. versionchanged:: 3.12
      Các đối tượng Immortal có refcount rất lớn, không tương ứng với số lượng tham chiếu thực tế đến đối tượng.

.. function:: getrecursionlimit()

   Trả về giá trị hiện tại của giới hạn đệ quy, là độ sâu tối đa của ngăn xếp trình thông dịch Python. Giới hạn này ngăn việc đệ quy vô hạn gây tràn ngăn xếp C và làm Python bị crash. Giới hạn này có thể được thiết lập bằng
   :func:`setrecursionlimit`.


.. function:: getsizeof(object[, default])

   Trả về kích thước của một đối tượng tính bằng byte. Đối tượng có thể thuộc bất kỳ kiểu nào. Tất cả các đối tượng tích hợp sẵn sẽ trả về kết quả chính xác, nhưng điều này không nhất thiết đúng với các extension của bên thứ ba vì còn tùy thuộc vào cách triển khai.

   Chỉ mức tiêu thụ bộ nhớ được quy trực tiếp cho đối tượng mới được tính, không tính mức tiêu thụ bộ nhớ của các đối tượng mà nó tham chiếu.

   Nếu được cung cấp, *default* sẽ được trả về nếu đối tượng không cung cấp cách truy xuất kích thước. Nếu không, một :exc:`TypeError` sẽ được phát sinh.

   :func:`getsizeof` gọi phương thức ``__sizeof__`` của đối tượng và cộng thêm phần overhead của garbage collector nếu đối tượng được garbage collector quản lý.

   Xem `công thức sizeof đệ quy <https://code.activestate.com/recipes/577504-compute-memory-footprint-of-an-object-and-its-cont/>`_ để biết ví dụ về cách sử dụng :func:`getsizeof` một cách đệ quy nhằm tìm kích thước của các container và toàn bộ nội dung bên trong chúng.

.. function:: getswitchinterval()

   Trả về "khoảng thời gian chuyển luồng" của trình thông dịch, tính bằng giây; xem
   :func:`setswitchinterval`.

   .. versionadded:: 3.2


.. function:: _getframe([depth])

   Trả về một đối tượng frame từ ngăn xếp lời gọi. Nếu cung cấp số nguyên tùy chọn *depth*, trả về đối tượng frame nằm dưới cùng của ngăn xếp số lần gọi tương ứng. Nếu vị trí đó sâu hơn ngăn xếp lời gọi, :exc:`ValueError` sẽ được phát sinh. Giá trị mặc định của *depth* là 0, trả về frame ở đầu ngăn xếp lời gọi.

   .. audit-event:: sys._getframe frame sys._getframe

   .. impl-detail::

      Chỉ nên sử dụng hàm này cho các mục đích nội bộ và chuyên biệt. Không đảm bảo hàm này tồn tại trong mọi bản triển khai Python.


.. function:: _getframemodulename([depth])

   Trả về tên của một module từ ngăn xếp lời gọi. Nếu cung cấp số nguyên tùy chọn *depth*, trả về module nằm dưới cùng của ngăn xếp số lần gọi tương ứng. Nếu vị trí đó sâu hơn ngăn xếp lời gọi hoặc không thể xác định module, ``None`` sẽ được trả về. Giá trị mặc định của *depth* là 0, trả về module ở đầu ngăn xếp lời gọi.

   .. audit-event:: sys._getframemodulename depth sys._getframemodulename

   .. impl-detail::

      Chỉ nên sử dụng hàm này cho các mục đích nội bộ và chuyên biệt. Không đảm bảo hàm này tồn tại trong mọi bản triển khai Python.

   .. versionadded:: 3.12


.. function:: getobjects(limit[, type])

   Hàm này chỉ tồn tại nếu CPython được xây dựng bằng tùy chọn configure chuyên biệt :option:`--with-trace-refs`. Hàm chỉ предназначена cho việc gỡ lỗi các vấn đề về thu gom rác.

   Trả về danh sách tối đa *limit* đối tượng Python được cấp phát động. Nếu có *type*, chỉ các đối tượng thuộc chính xác kiểu đó (không bao gồm các kiểu con) mới được đưa vào.

   Các đối tượng trong danh sách không an toàn để sử dụng. Cụ thể, kết quả sẽ bao gồm các đối tượng từ tất cả các interpreter dùng chung trạng thái bộ cấp phát đối tượng của chúng (tức là những interpreter được tạo bằng
   :c:member:`PyInterpreterConfig.use_main_obmalloc` được đặt thành 1 hoặc sử dụng :c:func:`Py_NewInterpreter`, và
   :ref:`main interpreter <sub-interpreter-support>`). Việc trộn các đối tượng từ những interpreter khác nhau có thể dẫn đến sự cố hoặc hành vi không mong muốn khác.

   .. impl-detail::

      Chỉ nên sử dụng hàm này cho các mục đích chuyên biệt. Không đảm bảo hàm này tồn tại trong mọi implementation của Python.

   .. versionchanged:: 3.14

      Kết quả có thể bao gồm các đối tượng từ những interpreter khác.


.. function:: getprofile()

   .. index::
      single: profile function
      single: profiler

   Lấy hàm profiler được thiết lập bởi :func:`setprofile`.


.. function:: gettrace()

   .. index::
      single: trace function
      single: debugger

   Lấy hàm trace do :func:`settrace` thiết lập.

   .. impl-detail::

      Hàm :func:`gettrace` chỉ dành cho việc triển khai debugger, profiler, công cụ đo độ bao phủ (coverage) và các công cụ tương tự. Hành vi của hàm này là một phần của nền tảng triển khai, không phải một phần của định nghĩa ngôn ngữ, vì vậy có thể không khả dụng trong mọi bản triển khai Python.


.. function:: getwindowsversion()

   Trả về một named tuple mô tả phiên bản Windows hiện đang chạy. Các phần tử được đặt tên là *major*, *minor*, *build*, *platform*, *service_pack*, *service_pack_minor*, *service_pack_major*, *suite_mask*, *product_type* và *platform_version*. *service_pack* chứa một chuỗi, *platform_version* chứa một tuple 3 phần tử, còn tất cả các giá trị khác là số nguyên. Các thành phần cũng có thể được truy cập theo tên, vì vậy ``sys.getwindowsversion()[0]`` tương đương với ``sys.getwindowsversion().major``. Để tương thích với các phiên bản trước, chỉ có 5 phần tử đầu tiên có thể được truy xuất bằng indexing.

   *platform* sẽ là ``2`` (VER_PLATFORM_WIN32_NT).

   *product_type* có thể là một trong các giá trị sau:

   +----------------------------------+----------------------------------------------------------------+
   | Hằng số                          | Ý nghĩa                                                        |
   +==================================+================================================================+
   | ``1`` (VER_NT_WORKSTATION)       | Hệ thống là một workstation.                                   |
   +----------------------------------+----------------------------------------------------------------+
   | ``2`` (VER_NT_DOMAIN_CONTROLLER) | Hệ thống là một domain controller.                             |
   +----------------------------------+----------------------------------------------------------------+
   | ``3`` (VER_NT_SERVER)            | Hệ thống là một server, nhưng không phải là domain controller. |
   +----------------------------------+----------------------------------------------------------------+

   Hàm này bao bọc hàm Win32 :c:func:`!GetVersionEx`; hãy xem tài liệu Microsoft về :c:func:`!OSVERSIONINFOEX` để biết thêm thông tin về các trường này.

   *platform_version* trả về phiên bản chính, phiên bản phụ và số bản dựng của hệ điều hành hiện tại, thay vì phiên bản đang được giả lập cho tiến trình. Nó được dùng cho việc ghi nhật ký thay vì phát hiện tính năng.

   .. note::
      *platform_version* lấy phiên bản từ kernel32.dll, vốn có thể khác với phiên bản hệ điều hành. Vui lòng sử dụng module :mod:`platform` để lấy phiên bản hệ điều hành chính xác.

   .. availability:: Windows.

   .. versionchanged:: 3.2
      Đã chuyển thành named tuple và thêm *service_pack_minor*, *service_pack_major*, *suite_mask* và *product_type*.

   .. versionchanged:: 3.6
      Đã thêm *platform_version*


.. function:: get_asyncgen_hooks()

   Trả về một đối tượng *asyncgen_hooks*, tương tự như một
   :class:`~collections.namedtuple` có dạng ``(firstiter, finalizer)``, trong đó *firstiter* và *finalizer* được kỳ vọng là ``None`` hoặc các hàm nhận một :term:`asynchronous generator iterator` làm đối số, và được dùng để lập lịch việc hoàn tất một asynchronous generator bởi event loop.

   .. versionadded:: 3.6
      Xem :pep:`525` để biết thêm chi tiết.

   .. note::
      Hàm này được bổ sung trên cơ sở tạm thời (xem :pep:`411` để biết chi tiết.)


.. function:: get_coroutine_origin_tracking_depth()

   Lấy độ sâu theo dõi nguồn gốc coroutine hiện tại, được thiết lập bởi
   :func:`set_coroutine_origin_tracking_depth`.

   .. versionadded:: 3.7

   .. note::
      Hàm này được bổ sung trên cơ sở tạm thời (xem :pep:`411` để biết chi tiết.) Chỉ sử dụng hàm này cho mục đích gỡ lỗi.


.. data:: hash_info

   Một :term:`named tuple` cung cấp các tham số của cách triển khai numeric hash. Để biết thêm chi tiết về việc băm các kiểu số, hãy xem
   :ref:`numeric-hash`.

   .. attribute:: hash_info.width

      Độ rộng tính theo bit được sử dụng cho các giá trị hash

   .. attribute:: hash_info.modulus

      Mô-đun nguyên tố P được sử dụng cho lược đồ numeric hash

   .. attribute:: hash_info.inf

      Giá trị hash được trả về đối với dương vô cực

   .. attribute:: hash_info.nan

      (Thuộc tính này không còn được sử dụng)

   .. attribute:: hash_info.imag

      Hệ số nhân được sử dụng cho phần ảo của một số phức

   .. attribute:: hash_info.algorithm

      Tên của algorithm dùng để băm str, bytes và memoryview

   .. attribute:: hash_info.hash_bits

      Kích thước đầu ra nội bộ của thuật toán băm

   .. attribute:: hash_info.seed_bits

      Kích thước của khóa seed của thuật toán băm

   .. attribute:: hash_info.cutoff

      Giới hạn cho tối ưu hóa DJBX33A đối với chuỗi nhỏ trong phạm vi ``[1, cutoff)``.

   .. versionadded:: 3.2

   .. versionchanged:: 3.4
      Đã thêm *algorithm*, *hash_bits*, *seed_bits* và *cutoff*.


.. data:: hexversion

   Số phiên bản được mã hóa thành một số nguyên duy nhất. Số này được đảm bảo tăng theo mỗi phiên bản, bao gồm cả việc hỗ trợ thích hợp cho các bản phát hành không dành cho môi trường production. Ví dụ, để kiểm tra xem trình thông dịch Python có ít nhất là phiên bản 1.5.2 hay không, hãy sử dụng::

      if sys.hexversion >= 0x010502F0:
          # sử dụng một tính năng nâng cao
          ...
      else:
          # sử dụng một triển khai thay thế hoặc cảnh báo người dùng
          ...

   Giá trị này được gọi là ``hexversion`` vì nó chỉ thực sự có ý nghĩa khi được xem như kết quả của việc truyền nó vào hàm :func:`hex` tích hợp sẵn. ``hexversion``
   :term:`named tuple` :data:`sys.version_info` có thể được sử dụng để mã hóa cùng thông tin theo cách thân thiện hơn với con người.

   Bạn có thể tìm thấy thêm thông tin chi tiết về ``hexversion`` tại :ref:`apiabiversion`.


.. data:: implementation

   Một đối tượng chứa thông tin về việc triển khai của trình thông dịch Python hiện đang chạy. Các thuộc tính sau đây bắt buộc phải tồn tại trong mọi triển khai Python.

   *name* là mã định danh của bản triển khai, ví dụ ``'cpython'``. Chuỗi thực tế được xác định bởi bản triển khai Python, nhưng được đảm bảo là chữ thường.

   *version* là một named tuple, theo cùng định dạng như
   :data:`sys.version_info`. Nó biểu thị phiên bản của *bản triển khai* Python. Điều này có ý nghĩa khác với phiên bản cụ thể của *ngôn ngữ* Python mà interpreter đang chạy tuân theo, được biểu thị bằng ``sys.version_info``. Ví dụ, đối với PyPy 1.8, ``sys.implementation.version`` có thể là ``sys.version_info(1, 8, 0, 'final', 0)``, trong khi ``sys.version_info`` sẽ là ``sys.version_info(2, 7, 2, 'final', 0)``. Đối với CPython, chúng có cùng giá trị vì đây là bản triển khai tham chiếu.

   *hexversion* là phiên bản của bản triển khai ở định dạng thập lục phân, như
   :data:`sys.hexversion`.

   *cache_tag* là thẻ được import machinery sử dụng trong tên tệp của các module đã lưu vào bộ nhớ đệm. Theo quy ước, thẻ này là sự kết hợp giữa tên và phiên bản của bản triển khai, như ``'cpython-33'``. Tuy nhiên, một bản triển khai Python có thể sử dụng giá trị khác nếu phù hợp. Nếu ``cache_tag`` được đặt thành ``None``, điều đó cho biết rằng việc lưu module vào bộ nhớ đệm sẽ bị vô hiệu hóa.

   *supports_isolated_interpreters* là một giá trị boolean, cho biết bản triển khai này có hỗ trợ nhiều isolated interpreter hay không. Trên hầu hết các nền tảng, giá trị này là ``True`` đối với CPython. Các nền tảng có hỗ trợ này triển khai module cấp thấp :mod:`!_interpreters`.

   .. seealso::

      :pep:`684`, :pep:`734`, và :mod:`concurrent.interpreters`.

   :data:`sys.implementation` có thể chứa các thuộc tính bổ sung dành riêng cho việc triển khai Python. Các thuộc tính không chuẩn này phải bắt đầu bằng dấu gạch dưới và không được mô tả ở đây. Bất kể nội dung của nó là gì,
   :data:`sys.implementation` sẽ không thay đổi trong suốt quá trình chạy của trình thông dịch, cũng như giữa các phiên bản triển khai. (Tuy nhiên, nó có thể thay đổi giữa các phiên bản ngôn ngữ Python.) Xem :pep:`421` để biết thêm thông tin.

   .. versionadded:: 3.3

   .. versionchanged:: 3.14
      Đã thêm trường ``supports_isolated_interpreters``.

   .. note::

      Việc thêm các thuộc tính bắt buộc mới phải tuân theo quy trình PEP thông thường. Xem :pep:`421` để biết thêm thông tin.

.. data:: int_info

   Một :term:`named tuple` chứa thông tin về biểu diễn nội bộ của số nguyên trong Python. Các thuộc tính này chỉ được đọc.

   .. attribute:: int_info.bits_per_digit

      Số bit được lưu trữ trong mỗi chữ số. Các số nguyên Python được lưu trữ nội bộ theo cơ số ``2**int_info.bits_per_digit``.

   .. attribute:: int_info.sizeof_digit

      Kích thước tính bằng byte của kiểu C được dùng để biểu diễn một chữ số.

   .. attribute:: int_info.default_max_str_digits

      Giá trị mặc định của :func:`sys.get_int_max_str_digits` khi chưa được cấu hình rõ ràng theo cách khác.

   .. attribute:: int_info.str_digits_check_threshold

      Giá trị nhỏ nhất khác không của :func:`sys.set_int_max_str_digits`,
      :envvar:`PYTHONINTMAXSTRDIGITS`, hoặc :option:`-X int_max_str_digits <-X>`.

   .. versionadded:: 3.1

   .. versionchanged:: 3.11

      Đã thêm :attr:`~int_info.default_max_str_digits` và
      :attr:`~int_info.str_digits_check_threshold`.


.. data:: __interactivehook__

   Khi thuộc tính này tồn tại, giá trị của nó sẽ được tự động gọi (không có đối số) khi trình thông dịch được khởi chạy ở :ref:`chế độ tương tác <tut-interactive>`. Việc này được thực hiện sau khi đọc tệp :envvar:`PYTHONSTARTUP`, để bạn có thể thiết lập hook này trong đó. Mô-đun :mod:`site`
   :ref:`thiết lập giá trị này <rlcompleter-config>`.

   .. audit-event:: cpython.run_interactivehook hook sys.__interactivehook__

      Phát sinh một :ref:`sự kiện auditing <auditing>` ``cpython.run_interactivehook`` với đối tượng hook làm đối số khi hook được gọi lúc khởi động.

   .. versionadded:: 3.4


.. function:: intern(string)

   Nhập *chuỗi* vào bảng các chuỗi "interned" và trả về chuỗi interned -- chính là *chuỗi* đó hoặc một bản sao. Intern chuỗi hữu ích để cải thiện một chút hiệu suất tra cứu dictionary -- nếu các khóa trong dictionary được intern và khóa tra cứu cũng được intern, việc so sánh khóa (sau khi băm) có thể được thực hiện bằng cách so sánh con trỏ thay vì so sánh chuỗi. Thông thường, các tên được sử dụng trong chương trình Python sẽ tự động được intern, và các dictionary dùng để lưu trữ thuộc tính của module, class hoặc instance có các khóa được intern.

   Các chuỗi đã được intern không phải là :term:`immortal`; bạn phải giữ một tham chiếu đến giá trị trả về của :func:`intern` để hưởng lợi từ chúng.


.. function:: _is_gil_enabled()

   Trả về :const:`True` nếu :term:`GIL` được bật và :const:`False` nếu bị tắt.

   .. versionadded:: 3.13

   .. impl-detail::

      Không đảm bảo rằng nó tồn tại trong mọi triển khai Python.

.. function:: is_finalizing()

   Trả về :const:`True` nếu trình thông dịch Python chính đang
   :term:`tắt <interpreter shutdown>`. Nếu không, trả về :const:`False`.

   Xem thêm :exc:`PythonFinalizationError` exception.

   .. versionadded:: 3.5

.. data:: _jit

   Các tiện ích để quan sát quá trình biên dịch just-in-time.

   .. impl-detail::

      Biên dịch JIT là một *experimental implementation detail* của CPython. ``sys._jit`` không được đảm bảo tồn tại hoặc hoạt động giống nhau trong mọi triển khai, phiên bản hoặc cấu hình build của Python.

   .. versionadded:: 3.14

   .. function:: _jit.is_available()

      Trả về ``True`` nếu trình thực thi Python hiện tại hỗ trợ biên dịch JIT, và ``False`` nếu không. Bạn có thể kiểm soát điều này bằng cách build CPython với tùy chọn ``--experimental-jit`` trên Windows, và
      tùy chọn :option:`--enable-experimental-jit` trên tất cả các nền tảng khác.

   .. function:: _jit.is_enabled()

      Trả về ``True`` nếu biên dịch JIT được bật cho tiến trình Python hiện tại (ngụ ý :func:`sys._jit.is_available`), và ``False`` nếu không. Nếu biên dịch JIT khả dụng, bạn có thể kiểm soát điều này bằng cách đặt
      biến môi trường :envvar:`PYTHON_JIT` thành ``0`` (tắt) hoặc ``1`` (bật) khi khởi động interpreter.

   .. function:: _jit.is_active()

      Trả về ``True`` nếu frame Python trên cùng hiện đang thực thi mã JIT (ngụ ý :func:`sys._jit.is_enabled`), và ``False`` nếu không.

      .. note::

         Hàm này được dùng để kiểm thử và gỡ lỗi chính JIT. Không nên sử dụng hàm này cho bất kỳ mục đích nào khác.

      .. note::

         Do đặc điểm của các trình biên dịch JIT tracing, việc gọi hàm này lặp lại có thể cho kết quả bất ngờ. Ví dụ, việc rẽ nhánh dựa trên giá trị trả về của hàm có thể dẫn đến hành vi không mong muốn (nếu việc đó khiến mã JIT được vào hoặc thoát):

         .. code-block:: pycon

            >>> for warmup in range(BIG_NUMBER):
            ...     # Dòng này là "hot" và cuối cùng sẽ được biên dịch bằng JIT:
            ...     if sys._jit.is_active():
            ...         # Dòng này là "cold" và được chạy trong trình thông dịch:
            ...         assert sys._jit.is_active()
            ...
            Traceback (most recent call last):
              File "<stdin>", line 5, in <module>
                assert sys._jit.is_active()
                       ~~~~~~~~~~~~~~~~~~^^
            AssertionError

.. data:: last_exc

   Biến này không phải lúc nào cũng được định nghĩa; nó được đặt thành thể hiện ngoại lệ khi một ngoại lệ không được xử lý và trình thông dịch in thông báo lỗi cùng traceback ngăn xếp. Mục đích sử dụng của biến là cho phép người dùng tương tác nhập một mô-đun gỡ lỗi và thực hiện gỡ lỗi post-mortem mà không cần chạy lại lệnh gây ra lỗi. (Cách sử dụng điển hình là ``import pdb; pdb.pm()`` để vào trình gỡ lỗi post-mortem; xem mô-đun :mod:`pdb` để biết thêm thông tin.)

   .. versionadded:: 3.12

.. function:: _is_immortal(op)

   Trả về :const:`True` nếu đối tượng đã cho là :term:`immortal`, ngược lại trả về :const:`False`.

   .. note::

      Các đối tượng bất tử (và do đó trả về ``True`` khi được truyền cho hàm này) không được đảm bảo sẽ vẫn bất tử trong các phiên bản tương lai, và điều ngược lại cũng đúng với các đối tượng hữu tử.

   .. versionadded:: 3.14

   .. impl-detail::

      Chỉ nên sử dụng hàm này cho các mục đích chuyên biệt. Không đảm bảo hàm này tồn tại trong mọi implementation của Python.

.. function:: _is_interned(string)

   Trả về :const:`True` nếu chuỗi đã cho là "interned", ngược lại trả về :const:`False`.

   .. versionadded:: 3.13

   .. impl-detail::

      Không đảm bảo rằng nó tồn tại trong mọi triển khai Python.


.. data:: last_type
          last_value last_traceback

   Ba biến này đã lỗi thời; thay vào đó hãy sử dụng :data:`sys.last_exc`. Chúng chứa biểu diễn cũ của ``sys.last_exc``, được trả về từ :func:`exc_info` ở trên.

.. data:: maxsize

   Một số nguyên cho biết giá trị lớn nhất mà một biến thuộc kiểu :c:type:`Py_ssize_t` có thể nhận. Thông thường, giá trị này là ``2**31 - 1`` trên nền tảng 32-bit và ``2**63 - 1`` trên nền tảng 64-bit.


.. data:: maxunicode

   Một số nguyên cho biết giá trị của điểm mã Unicode lớn nhất, tức là ``1114111`` (``0x10FFFF`` ở hệ thập lục phân).

   .. versionchanged:: 3.3
      Trước :pep:`393`, ``sys.maxunicode`` từng là ``0xFFFF`` hoặc ``0x10FFFF``, tùy thuộc vào tùy chọn cấu hình chỉ định việc các ký tự Unicode được lưu dưới dạng UCS-2 hay UCS-4.


.. data:: meta_path

    Một danh sách các đối tượng :term:`meta path finder` có
    các phương thức :meth:`~importlib.abc.MetaPathFinder.find_spec` được gọi để kiểm tra xem một trong các đối tượng có thể tìm thấy module cần import hay không. Theo mặc định, danh sách này chứa các mục triển khai ngữ nghĩa import mặc định của Python.
    Phương thức :meth:`~importlib.abc.MetaPathFinder.find_spec` được gọi với ít nhất tên tuyệt đối của module đang được import. Nếu module cần import nằm trong một package, thì thuộc tính
    :attr:`~module.__path__` của package cha được truyền vào làm đối số thứ hai. Phương thức này trả về một
    :term:`module spec`, hoặc ``None`` nếu không tìm thấy module.

    .. seealso::

        :class:`importlib.abc.MetaPathFinder`
          Lớp cơ sở trừu tượng định nghĩa interface của các đối tượng finder trên
          :data:`meta_path`.
        :class:`importlib.machinery.ModuleSpec`
          Lớp cụ thể mà
          :meth:`~importlib.abc.MetaPathFinder.find_spec` sẽ trả về các thể hiện của.

    .. versionchanged:: 3.4

        :term:`Đặc tả module <module spec>` được giới thiệu trong Python 3.4, bởi
        :pep:`451`.

    .. versionchanged:: 3.12

        Đã loại bỏ cơ chế dự phòng tìm kiếm phương thức :meth:`!find_module` nếu mục :data:`meta_path` không có
        phương thức :meth:`~importlib.abc.MetaPathFinder.find_spec`.

.. data:: modules

   Đây là một từ điển ánh xạ tên module tới các module đã được tải. Có thể thao tác với từ điển này để buộc tải lại module và thực hiện các thủ thuật khác. Tuy nhiên, việc thay thế từ điển sẽ không nhất thiết hoạt động như mong đợi, và việc xóa các mục thiết yếu khỏi từ điển có thể khiến Python không thể hoạt động. Nếu muốn lặp qua từ điển toàn cục này, luôn sử dụng ``sys.modules.copy()`` hoặc ``tuple(sys.modules)`` để tránh ngoại lệ, vì kích thước của từ điển có thể thay đổi trong quá trình lặp do tác động phụ của mã hoặc hoạt động trong các thread khác.


.. data:: orig_argv

   Danh sách các đối số dòng lệnh ban đầu được truyền cho trình thực thi Python.

   Các phần tử của :data:`sys.orig_argv` là các đối số dành cho trình thông dịch Python, còn các phần tử của :data:`sys.argv` là các đối số dành cho chương trình của người dùng. Các đối số được chính trình thông dịch sử dụng sẽ có trong :data:`sys.orig_argv` và không có trong :data:`sys.argv`.

   .. versionadded:: 3.10


.. data:: path

   .. index:: triple: module; search; path

   Một danh sách các chuỗi chỉ định đường dẫn tìm kiếm các module. Được khởi tạo từ biến môi trường :envvar:`PYTHONPATH`, cùng với một giá trị mặc định phụ thuộc vào quá trình cài đặt.

   Theo mặc định, khi được khởi tạo lúc chương trình khởi động, một đường dẫn có khả năng không an toàn được thêm vào đầu :data:`sys.path` (*trước* các mục được chèn do :envvar:`PYTHONPATH`):

   * Dòng lệnh ``python -m module``: thêm thư mục làm việc hiện tại vào đầu.
   * Dòng lệnh ``python script.py``: thêm thư mục của script vào đầu. Nếu đó là một symbolic link, hãy phân giải các symbolic link.
   * Các dòng lệnh ``python -c code`` và ``python`` (REPL): thêm một chuỗi rỗng vào đầu, nghĩa là thư mục làm việc hiện tại.

   Để không thêm đường dẫn có khả năng không an toàn này vào đầu, hãy sử dụng tùy chọn dòng lệnh :option:`-P` hoặc biến môi trường :envvar:`PYTHONSAFEPATH`.

   Một chương trình có thể tự do sửa đổi danh sách này cho mục đích riêng. Chỉ nên thêm các chuỗi vào :data:`sys.path`; mọi kiểu dữ liệu khác sẽ bị bỏ qua khi nhập.


   .. seealso::
      * Mô-đun :mod:`site` Mô tả cách sử dụng các tệp .pth để mở rộng :data:`sys.path`.

.. data:: path_hooks

    Một danh sách các callable nhận một đối số đường dẫn để thử tạo một
    :term:`finder` cho đường dẫn đó. Nếu có thể tạo một finder, callable phải trả về finder đó; nếu không, hãy nêu :exc:`ImportError`.

    Ban đầu được chỉ định trong :pep:`302`.


.. data:: path_importer_cache

    Một từ điển hoạt động như bộ nhớ đệm cho các đối tượng :term:`finder`. Các khóa là những đường dẫn đã được truyền vào :data:`sys.path_hooks` và các giá trị là những finder được tìm thấy. Nếu một đường dẫn là đường dẫn hệ thống tệp hợp lệ nhưng không tìm thấy finder nào trên :data:`sys.path_hooks` thì ``None`` sẽ được lưu trữ.

    Ban đầu được chỉ định trong :pep:`302`.


.. data:: platform

   Một chuỗi chứa mã định danh nền tảng. Các giá trị đã biết là:

   +----------------+----------------------+
   | Hệ thống       | giá trị ``platform`` |
   +================+======================+
   | AIX            | ``'aix'``            |
   +----------------+----------------------+
   | Android        | ``'android'``        |
   +----------------+----------------------+
   | Emscripten     | ``'emscripten'``     |
   +----------------+----------------------+
   | FreeBSD        | ``'freebsd'``        |
   +----------------+----------------------+
   | iOS            | ``'ios'``            |
   +----------------+----------------------+
   | Linux          | ``'linux'``          |
   +----------------+----------------------+
   | macOS          | ``'darwin'``         |
   +----------------+----------------------+
   | Windows        | ``'win32'``          |
   +----------------+----------------------+
   | Windows/Cygwin | ``'cygwin'``         |
   +----------------+----------------------+
   | WASI           | ``'wasi'``           |
   +----------------+----------------------+

   Trên các hệ thống Unix không được liệt kê trong bảng, giá trị này là tên HĐH được viết thường do ``uname -s`` trả về, nối thêm phần đầu của phiên bản do ``uname -r`` trả về, ví dụ ``'sunos5'``, *tại thời điểm Python được build*. Trừ khi bạn muốn kiểm tra một phiên bản hệ thống cụ thể, do đó, bạn nên sử dụng cách viết sau::

      if sys.platform.startswith('sunos'):
          # Mã dành riêng cho SunOS ở đây...

   .. versionchanged:: 3.3
      Trên Linux, :data:`sys.platform` không còn chứa phiên bản chính nữa. Nó luôn là ``'linux'``, thay vì ``'linux2'`` hoặc ``'linux3'``.

   .. versionchanged:: 3.8
      Trên AIX, :data:`sys.platform` không còn chứa phiên bản chính nữa. Nó luôn là ``'aix'``, thay vì ``'aix5'`` hoặc ``'aix7'``.

   .. versionchanged:: 3.13
      Trên Android, :data:`sys.platform` hiện trả về ``'android'`` thay vì ``'linux'``.

   .. versionchanged:: 3.14
      Trên FreeBSD, :data:`sys.platform` không còn chứa phiên bản chính nữa. Nó luôn là ``'freebsd'``, thay vì ``'freebsd13'`` hoặc ``'freebsd14'``.

   .. seealso::

      :data:`os.name` có độ phân giải thô hơn. :func:`os.uname` cung cấp thông tin phiên bản phụ thuộc vào hệ thống.

      Mô-đun :mod:`platform` cung cấp các kiểm tra chi tiết về danh tính của hệ thống.


.. data:: platlibdir

   Tên của thư mục thư viện dành riêng cho nền tảng. Thư mục này được dùng để xây dựng đường dẫn của thư viện chuẩn và các đường dẫn của những mô-đun mở rộng đã cài đặt.

   Trên hầu hết các nền tảng, nó bằng ``"lib"``. Trên Fedora và SuSE, nó bằng ``"lib64"`` trên các nền tảng 64-bit, tạo ra các đường dẫn ``sys.path`` sau đây (trong đó ``X.Y`` là phiên bản ``major.minor`` của Python):

   * ``/usr/lib64/pythonX.Y/``: Thư viện chuẩn (chẳng hạn như ``os.py`` của mô-đun :mod:`os`)
   * ``/usr/lib64/pythonX.Y/lib-dynload/``: Các mô-đun mở rộng C của thư viện chuẩn (chẳng hạn như mô-đun :mod:`errno`; tên tệp chính xác phụ thuộc vào nền tảng)
   * ``/usr/lib/pythonX.Y/site-packages/`` (luôn sử dụng ``lib``, không phải
     :data:`sys.platlibdir`): Các mô-đun bên thứ ba
   * ``/usr/lib64/pythonX.Y/site-packages/``: Các mô-đun mở rộng C của các gói bên thứ ba

   .. versionadded:: 3.9


.. data:: prefix

   Một chuỗi cung cấp tiền tố thư mục dành riêng cho từng hệ thống, nơi các tệp Python độc lập với nền tảng được cài đặt; trên Unix, giá trị mặc định là
   :file:`/usr/local`. Bạn có thể đặt giá trị này trong thời gian build bằng đối số :option:`--prefix` cho script :program:`configure`. Xem
   :ref:`installation_paths` để biết các đường dẫn được suy ra.

   .. note::

      Nếu :ref:`môi trường ảo <venv-def>` đang được sử dụng, :data:`prefix` này sẽ trỏ đến môi trường ảo. Giá trị dành cho bản cài đặt Python vẫn có sẵn thông qua :data:`base_prefix`. Tham khảo :ref:`sys-path-init-virtual-environments` để biết thêm thông tin.

   .. versionchanged:: 3.14

      Khi chạy trong :ref:`môi trường ảo <venv-def>`,
      :data:`prefix` và :data:`exec_prefix` hiện được :ref:`khởi tạo đường dẫn <sys-path-init>` đặt thành tiền tố của môi trường ảo, thay vì :mod:`site`. Điều này có nghĩa là :data:`prefix` và
      :data:`exec_prefix` luôn trỏ đến môi trường ảo, ngay cả khi
      :mod:`site` bị vô hiệu hóa (:option:`-S`).


.. data:: ps1
          ps2

   .. index::
      single: interpreter prompts
      single: prompts, interpreter
      single: >>>; interpreter prompt
      single: ...; interpreter prompt

   Các chuỗi xác định lời nhắc chính và phụ của trình thông dịch. Các chuỗi này chỉ được định nghĩa khi trình thông dịch ở chế độ tương tác. Trong trường hợp đó, giá trị ban đầu của chúng lần lượt là ``'>>> '`` và ``'... '``. Nếu một đối tượng không phải chuỗi được gán cho một trong hai biến, :func:`str` của đối tượng đó sẽ được đánh giá lại mỗi lần trình thông dịch chuẩn bị đọc một lệnh tương tác mới; bạn có thể dùng cách này để triển khai lời nhắc động.


.. function:: setdlopenflags(n)

   Đặt các cờ được trình thông dịch sử dụng cho các lệnh gọi :c:func:`dlopen`, chẳng hạn như khi trình thông dịch tải các module mở rộng. Trong số những tác dụng khác, thao tác này sẽ cho phép phân giải lazy các symbol khi import một module, nếu được gọi dưới dạng ``sys.setdlopenflags(0)``. Để chia sẻ symbol giữa các module mở rộng, hãy gọi dưới dạng ``sys.setdlopenflags(os.RTLD_GLOBAL)``. Có thể tìm thấy tên dạng symbol cho các giá trị cờ trong module :mod:`os` (các hằng số :samp:`RTLD_{xxx}`, ví dụ như
   :const:`os.RTLD_LAZY`).

   .. availability:: Unix.

.. function:: set_int_max_str_digits(maxdigits)

   Đặt :ref:`giới hạn độ dài chuyển đổi chuỗi số nguyên <int_max_str_digits>` được trình thông dịch này sử dụng. Xem thêm
   :func:`get_int_max_str_digits`.

   .. versionadded:: 3.11

.. function:: setprofile(profilefunc)

   .. index::
      single: profile function
      single: profiler

   Đặt hàm profile của hệ thống, cho phép bạn triển khai một profiler mã nguồn Python bằng Python. Xem chương :ref:`profile` để biết thêm thông tin về profiler Python. Hàm profile của hệ thống được gọi tương tự như hàm trace của hệ thống (xem :func:`settrace`), nhưng được gọi với các sự kiện khác; chẳng hạn, hàm này không được gọi cho mỗi dòng mã được thực thi (chỉ khi gọi và trả về, nhưng sự kiện trả về vẫn được báo cáo ngay cả khi một ngoại lệ đã được đặt). Hàm này dành riêng cho từng thread, nhưng profiler không có cách nào biết về việc chuyển đổi ngữ cảnh giữa các thread, vì vậy việc sử dụng hàm này khi có nhiều thread là không hợp lý. Ngoài ra, giá trị trả về của hàm không được sử dụng, nên hàm chỉ cần trả về ``None``. Lỗi trong hàm profile sẽ khiến chính hàm này bị hủy thiết lập.

   .. note::
      Cơ chế tracing tương tự được sử dụng cho :func:`!setprofile` và :func:`settrace`. Để trace các lệnh gọi có :func:`!setprofile` bên trong một hàm tracing (ví dụ: tại điểm dừng của debugger), hãy xem :func:`call_tracing`.

   Các hàm profile phải có ba đối số: *frame*, *event* và *arg*. *frame* là stack frame hiện tại. *event* là một chuỗi: ``'call'``, ``'return'``, ``'c_call'``, ``'c_return'`` hoặc ``'c_exception'``. *arg* phụ thuộc vào loại sự kiện.

   Các sự kiện có ý nghĩa như sau:

   ``'call'``
      Một hàm được gọi (hoặc một khối mã khác được thực thi). Hàm profile được gọi; *arg* là ``None``.

   ``'return'``
      Một hàm (hoặc khối mã khác) sắp trả về. Hàm profile được gọi; *arg* là giá trị sẽ được trả về, hoặc ``None`` nếu sự kiện xảy ra do một ngoại lệ được phát sinh.

   ``'c_call'``
      Một hàm C sắp được gọi. Đây có thể là một hàm mở rộng hoặc một hàm dựng sẵn. *arg* là đối tượng hàm C.

   ``'c_return'``
      Một hàm C đã trả về. *arg* là đối tượng hàm C.

   ``'c_exception'``
      Một hàm C đã phát sinh ngoại lệ. *arg* là đối tượng hàm C.

   .. audit-event:: sys.setprofile "" sys.setprofile


.. function:: setrecursionlimit(limit)

   Đặt độ sâu tối đa của ngăn xếp trình thông dịch Python thành *limit*. Giới hạn này ngăn việc đệ quy vô hạn gây tràn ngăn xếp C và làm Python bị lỗi.

   Giới hạn cao nhất có thể có phụ thuộc vào nền tảng. Người dùng có thể cần đặt giới hạn cao hơn khi có một chương trình yêu cầu đệ quy sâu và nền tảng hỗ trợ giới hạn cao hơn. Việc này cần được thực hiện thận trọng, vì giới hạn quá cao có thể dẫn đến lỗi.

   Nếu giới hạn mới quá thấp so với độ sâu đệ quy hiện tại, một
   ngoại lệ :exc:`RecursionError` sẽ được đưa ra.

   .. versionchanged:: 3.5.1
      Một ngoại lệ :exc:`RecursionError` hiện sẽ được đưa ra nếu giới hạn mới quá thấp so với độ sâu đệ quy hiện tại.


.. function:: setswitchinterval(interval)

   Đặt khoảng thời gian chuyển đổi thread của trình thông dịch (tính bằng giây). Giá trị dấu phẩy động này xác định thời lượng lý tưởng của các "timeslice" được phân bổ cho các thread Python chạy đồng thời. Lưu ý rằng giá trị thực tế có thể cao hơn, đặc biệt khi sử dụng các hàm hoặc phương thức nội bộ chạy trong thời gian dài. Ngoài ra, thread nào được lập lịch vào cuối khoảng thời gian là quyết định của hệ điều hành. Trình thông dịch không có scheduler riêng.

   .. versionadded:: 3.2


.. function:: settrace(tracefunc)

   .. index::
      single: trace function
      single: debugger

   Đặt hàm trace của hệ thống, cho phép bạn triển khai trình gỡ lỗi mã nguồn Python bằng Python. Hàm này dành riêng cho từng thread; để trình gỡ lỗi hỗ trợ nhiều thread, nó phải đăng ký một hàm trace bằng
   :func:`settrace` cho mỗi thread đang được debug hoặc sử dụng :func:`threading.settrace`.

   Các hàm trace phải có ba đối số: *frame*, *event* và *arg*. *frame* là :ref:`khung ngăn xếp hiện tại <frame-objects>`. *event* là một chuỗi: ``'call'``, ``'line'``, ``'return'``, ``'exception'`` hoặc ``'opcode'``. *arg* phụ thuộc vào loại sự kiện.

   Hàm trace được gọi (với *event* được đặt thành ``'call'``) bất cứ khi nào một phạm vi cục bộ mới được truy cập; hàm này sẽ trả về một tham chiếu đến hàm trace cục bộ được sử dụng cho phạm vi mới, hoặc ``None`` nếu không nên trace phạm vi đó.

   Hàm trace cục bộ sẽ trả về một tham chiếu đến chính nó hoặc đến một hàm khác, sau đó hàm này sẽ được sử dụng làm hàm trace cục bộ cho phạm vi đó.

   Nếu xảy ra bất kỳ lỗi nào trong hàm trace, hàm này sẽ bị hủy thiết lập, giống như khi ``settrace(None)`` được gọi.

   .. note::
      Tính năng tracing bị vô hiệu hóa khi gọi hàm trace (ví dụ: một hàm được thiết lập bởi
      :func:`!settrace`). Để tracing đệ quy, hãy xem :func:`call_tracing`.

   Các sự kiện có ý nghĩa như sau:

   ``'call'``
      Một hàm được gọi (hoặc một khối mã khác được thực thi). Hàm trace toàn cục được gọi; *arg* là ``None``; giá trị trả về chỉ định hàm trace cục bộ.

   ``'line'``
      Trình thông dịch sắp thực thi một dòng mã mới hoặc thực thi lại điều kiện của một vòng lặp. Hàm trace cục bộ được gọi; *arg* là ``None``; giá trị trả về chỉ định hàm trace cục bộ mới. Xem
      :source:`InternalDocs/code_objects.md` để biết giải thích chi tiết về cách thức hoạt động này. Có thể vô hiệu hóa các sự kiện theo từng dòng cho một frame bằng cách đặt
      :attr:`~frame.f_trace_lines` thành :const:`False` trên
      :ref:`frame <frame-objects>`.

   ``'return'``
      Một hàm (hoặc khối mã khác) sắp trả về. Hàm trace cục bộ được gọi; *arg* là giá trị sẽ được trả về, hoặc ``None`` nếu sự kiện xảy ra do một ngoại lệ được phát sinh. Giá trị trả về của hàm trace bị bỏ qua.

   ``'exception'``
      Một ngoại lệ đã xảy ra. Hàm trace cục bộ được gọi; *arg* là một tuple ``(exception, value, traceback)``; giá trị trả về chỉ định hàm trace cục bộ mới.

   ``'opcode'``
      Trình thông dịch sắp thực thi một opcode mới (xem :mod:`dis` để biết chi tiết về opcode). Hàm trace cục bộ được gọi; *arg* là ``None``; giá trị trả về chỉ định hàm trace cục bộ mới. Các sự kiện theo từng opcode không được phát ra theo mặc định: phải yêu cầu rõ ràng bằng cách đặt :attr:`~frame.f_trace_opcodes` thành :const:`True` trên
      :ref:`frame <frame-objects>`.

   Lưu ý rằng khi một ngoại lệ được truyền xuống chuỗi các caller, một sự kiện ``'exception'`` được tạo ở mỗi cấp.

   Để sử dụng chi tiết hơn, có thể đặt một hàm trace bằng cách gán rõ ràng ``frame.f_trace = tracefunc``, thay vì dựa vào việc hàm này được đặt gián tiếp thông qua giá trị trả về từ một hàm trace đã được cài đặt. Điều này cũng cần thiết để kích hoạt hàm trace trên frame hiện tại, việc mà :func:`settrace` không thực hiện. Lưu ý rằng để cách này hoạt động, một hàm tracing toàn cục phải được cài đặt bằng :func:`settrace` nhằm bật cơ chế tracing của runtime, nhưng không cần phải là cùng một hàm tracing (ví dụ: đó có thể là một hàm tracing có overhead thấp, chỉ trả về ``None`` để tự vô hiệu hóa ngay lập tức trên mỗi frame).

   Để biết thêm thông tin về các đối tượng code và frame, hãy tham khảo :ref:`types`.

   .. audit-event:: sys.settrace "" sys.settrace

   .. impl-detail::

      Hàm :func:`settrace` chỉ nhằm triển khai debugger, profiler, công cụ đo độ bao phủ và các công cụ tương tự. Hành vi của hàm này thuộc về nền tảng triển khai thay vì định nghĩa ngôn ngữ, vì vậy có thể không khả dụng trong mọi triển khai Python.

   .. versionchanged:: 3.7

      Đã thêm loại sự kiện ``'opcode'``; đã thêm :attr:`~frame.f_trace_lines` và
      Đã thêm các thuộc tính :attr:`~frame.f_trace_opcodes` cho frame

.. function:: set_asyncgen_hooks([firstiter] [, finalizer])

   Chấp nhận hai đối số từ khóa tùy chọn, là các callable nhận một
   :term:`asynchronous generator iterator` làm đối số. Callable *firstiter* sẽ được gọi khi một asynchronous generator được lặp lần đầu tiên. *finalizer* sẽ được gọi khi một asynchronous generator sắp bị garbage collection.

   .. audit-event:: sys.set_asyncgen_hooks_firstiter "" sys.set_asyncgen_hooks

   .. audit-event:: sys.set_asyncgen_hooks_finalizer "" sys.set_asyncgen_hooks

   Hai sự kiện auditing được phát sinh vì API nền tảng gồm hai lời gọi, và mỗi lời gọi phải phát sinh sự kiện riêng.

   .. versionadded:: 3.6
      Xem :pep:`525` để biết thêm chi tiết; để xem ví dụ tham khảo về một phương thức *finalizer*, hãy xem phần triển khai ``asyncio.Loop.shutdown_asyncgens`` trong
      :source:`Lib/asyncio/base_events.py`

   .. note::
      Hàm này được bổ sung trên cơ sở tạm thời (xem :pep:`411` để biết chi tiết.)

.. function:: set_coroutine_origin_tracking_depth(depth)

   Cho phép bật hoặc tắt việc theo dõi nguồn gốc coroutine. Khi được bật, thuộc tính ``cr_origin`` trên các đối tượng coroutine sẽ chứa một tuple gồm các tuple (tên tệp, số dòng, tên hàm) mô tả traceback nơi đối tượng coroutine được tạo, với lời gọi gần nhất đứng trước. Khi bị tắt, ``cr_origin`` sẽ là ``None``.

   Để bật, truyền một giá trị *depth* lớn hơn 0; giá trị này đặt số frame mà thông tin của chúng sẽ được thu thập. Để tắt, đặt *depth* về 0.

   Thiết lập này dành riêng cho từng thread.

   .. versionadded:: 3.7

   .. note::
      Hàm này được bổ sung trên cơ sở tạm thời (xem :pep:`411` để biết chi tiết.) Chỉ sử dụng hàm này cho mục đích gỡ lỗi.

.. function:: activate_stack_trampoline(backend, /)

   Kích hoạt stack profiler trampoline *backend*. Backend duy nhất được hỗ trợ là ``"perf"``.

   Không thể kích hoạt stack trampoline nếu JIT đang hoạt động.

   .. availability:: Linux.

   .. versionadded:: 3.12

   .. seealso::

      * :ref:`perf_profiling`
      * https://perf.wiki.kernel.org

.. function:: deactivate_stack_trampoline()

   Vô hiệu hóa backend stack profiler trampoline hiện tại.

   Nếu không có stack profiler nào được kích hoạt, hàm này không có tác dụng.

   .. availability:: Linux.

   .. versionadded:: 3.12

.. function:: is_stack_trampoline_active()

   Trả về ``True`` nếu một stack profiler trampoline đang hoạt động.

   .. availability:: Linux.

   .. versionadded:: 3.12


.. function:: remote_exec(pid, script)

   Thực thi *script*, một tệp chứa mã Python trong tiến trình từ xa có *pid* đã cho.

   Hàm này trả về ngay lập tức, còn mã sẽ được thực thi bởi luồng chính của tiến trình đích vào thời điểm sớm nhất có thể, tương tự như cách các signal được xử lý. Không có giao diện nào để xác định thời điểm mã đã được thực thi. Bên gọi chịu trách nhiệm bảo đảm rằng tệp vẫn tồn tại bất cứ khi nào tiến trình từ xa cố đọc tệp đó và tệp chưa bị ghi đè.

   Tiến trình từ xa phải đang chạy một trình thông dịch CPython có cùng phiên bản major và minor với tiến trình cục bộ. Nếu trình thông dịch cục bộ hoặc từ xa là bản phát hành trước (alpha, beta hoặc release candidate), thì trình thông dịch cục bộ và từ xa phải có cùng chính xác một phiên bản.

   Xem :ref:`remote-debugging` để biết thêm thông tin về cơ chế gỡ lỗi từ xa.

   .. audit-event:: sys.remote_exec pid script_path

      Khi mã được thực thi trong tiến trình từ xa, một
      :ref:`sự kiện kiểm tra <auditing>` ``sys.remote_exec`` được phát sinh với *pid* và đường dẫn đến tệp tập lệnh. Sự kiện này được phát sinh trong tiến trình đã gọi :func:`sys.remote_exec`.

   .. audit-event:: cpython.remote_debugger_script script_path

      Khi tập lệnh được thực thi trong tiến trình từ xa, một
      :ref:`sự kiện kiểm tra <auditing>` ``cpython.remote_debugger_script`` được phát sinh với đường dẫn trong tiến trình từ xa. Sự kiện này được phát sinh trong tiến trình từ xa, không phải tiến trình đã gọi :func:`sys.remote_exec`.

   .. availability:: Unix, Windows.
   .. versionadded:: 3.14
      Xem :pep:`768` để biết thêm chi tiết.


.. function:: _enablelegacywindowsfsencoding()

   Thay đổi :term:`filesystem encoding and error handler` thành 'mbcs' và 'replace' tương ứng, để nhất quán với các phiên bản Python trước 3.6.

   Điều này tương đương với việc định nghĩa biến môi trường :envvar:`PYTHONLEGACYWINDOWSFSENCODING` trước khi khởi chạy Python.

   Cũng xem :func:`sys.getfilesystemencoding` và
   :func:`sys.getfilesystemencodeerrors`.

   .. availability:: Windows.

   .. note::
      Việc thay đổi mã hóa filesystem sau khi Python khởi động rất rủi ro vì fsencoding cũ hoặc các đường dẫn được mã hóa bằng fsencoding cũ có thể đã được lưu vào bộ nhớ đệm ở đâu đó. Thay vào đó, hãy sử dụng :envvar:`PYTHONLEGACYWINDOWSFSENCODING`.

   .. versionadded:: 3.6
      Xem :pep:`529` để biết thêm chi tiết.

   .. deprecated-removed:: 3.13 3.16
      Thay vào đó, hãy sử dụng :envvar:`PYTHONLEGACYWINDOWSFSENCODING`.

.. data:: stdin
          stdout stderr

   :term:`Đối tượng tệp <file object>` được trình thông dịch sử dụng cho đầu vào, đầu ra và lỗi tiêu chuẩn:

   * ``stdin`` được sử dụng cho mọi đầu vào tương tác (bao gồm cả các lệnh gọi đến
     :func:`input`);
   * ``stdout`` được sử dụng cho đầu ra của các câu lệnh :func:`print` và :term:`expression` cũng như lời nhắc của :func:`input`;
   * Các lời nhắc của chính trình thông dịch và thông báo lỗi của nó được gửi đến ``stderr``.

   Các luồng này là những :term:`tệp văn bản <text file>` thông thường giống như các luồng được hàm :func:`open` trả về. Các tham số của chúng được chọn như sau:

   * Mã hóa và việc xử lý lỗi được khởi tạo từ
     :c:member:`PyConfig.stdio_encoding` và :c:member:`PyConfig.stdio_errors`.

     Trên Windows, UTF-8 được sử dụng cho thiết bị console. Các thiết bị không phải ký tự như tệp đĩa và pipe sử dụng mã hóa locale của hệ thống (tức là ANSI codepage). Các thiết bị ký tự không phải console như NUL (tức là nơi ``isatty()`` trả về ``True``) sử dụng giá trị của codepage đầu vào và đầu ra của console tại thời điểm khởi động, lần lượt cho stdin và stdout/stderr. Giá trị mặc định là :term:`locale encoding` của hệ thống nếu tiến trình ban đầu không được gắn vào console.

     Có thể ghi đè hành vi đặc biệt của console bằng cách đặt biến môi trường PYTHONLEGACYWINDOWSSTDIO trước khi khởi động Python. Trong trường hợp đó, các codepage của console được sử dụng như đối với mọi thiết bị ký tự khác.

     Trên mọi nền tảng, bạn có thể ghi đè mã hóa ký tự bằng cách đặt biến môi trường :envvar:`PYTHONIOENCODING` trước khi khởi động Python hoặc sử dụng tùy chọn dòng lệnh :option:`-X` ``utf8`` mới và biến môi trường :envvar:`PYTHONUTF8`. Tuy nhiên, đối với console Windows, tùy chọn này chỉ áp dụng khi
     :envvar:`PYTHONLEGACYWINDOWSSTDIO` cũng được thiết lập.

   * Khi chạy tương tác, luồng ``stdout`` được đệm theo dòng. Nếu không, luồng này được đệm theo khối như các tệp văn bản thông thường. Luồng ``stderr`` được đệm theo dòng trong cả hai trường hợp. Bạn có thể tắt bộ đệm cho cả hai luồng bằng cách truyền tùy chọn dòng lệnh :option:`-u` hoặc thiết lập
     biến môi trường :envvar:`PYTHONUNBUFFERED`.

   .. versionchanged:: 3.9
      ``stderr`` trong chế độ không tương tác hiện được đệm theo dòng thay vì được đệm hoàn toàn.

   .. note::

      Để ghi hoặc đọc dữ liệu nhị phân từ hoặc vào các luồng tiêu chuẩn, hãy sử dụng đối tượng :data:`~io.TextIOBase.buffer` nhị phân bên dưới. Ví dụ, để ghi các byte vào :data:`stdout`, hãy sử dụng ``sys.stdout.buffer.write(b'abc')``.

      Tuy nhiên, nếu bạn đang viết một thư viện (và không kiểm soát được ngữ cảnh mà mã của thư viện sẽ được thực thi), hãy lưu ý rằng các luồng tiêu chuẩn có thể được thay thế bằng những đối tượng giống tệp như :class:`io.StringIO`, vốn không hỗ trợ thuộc tính :attr:`!buffer`.


.. data:: __stdin__
          __stdout__ __stderr__

   Các đối tượng này chứa các giá trị ban đầu của ``stdin``, ``stderr`` và ``stdout`` tại thời điểm chương trình bắt đầu. Chúng được sử dụng trong quá trình hoàn tất và có thể hữu ích khi in ra standard stream thực tế, bất kể đối tượng ``sys.std*`` đã được chuyển hướng hay chưa.

   Nó cũng có thể được dùng để khôi phục các tệp thực tế về những đối tượng tệp đang hoạt động đã biết trong trường hợp chúng bị ghi đè bằng một đối tượng bị lỗi. Tuy nhiên, cách được khuyến nghị là lưu rõ ràng stream trước khi thay thế nó, rồi khôi phục đối tượng đã lưu.

   .. note::
       Trong một số điều kiện, ``stdin``, ``stdout`` và ``stderr``, cũng như các giá trị ban đầu ``__stdin__``, ``__stdout__`` và ``__stderr__``, có thể là ``None``. Trường hợp này thường xảy ra với các ứng dụng GUI trên Windows không kết nối với console và các ứng dụng Python được khởi chạy bằng :program:`pythonw`.


.. data:: stdlib_module_names

   Một frozenset gồm các chuỗi chứa tên của các module trong standard library.

   Nó giống nhau trên mọi nền tảng. Các module không khả dụng trên một số nền tảng và các module bị vô hiệu hóa khi build Python cũng được liệt kê. Mọi loại module đều được liệt kê: Python thuần, built-in, frozen và extension. Các module kiểm thử bị loại trừ.

   Đối với các package, chỉ package chính được liệt kê: các sub-package và sub-module không được liệt kê. Ví dụ, package ``email`` được liệt kê, nhưng sub-package ``email.mime`` và sub-module ``email.message`` thì không.

   Xem thêm danh sách :data:`sys.builtin_module_names`.

   .. versionadded:: 3.10


.. data:: thread_info

   Một :term:`named tuple` chứa thông tin về quá trình triển khai luồng.

   .. attribute:: thread_info.name

      Tên của quá trình triển khai luồng:

      * ``"nt"``: luồng Windows
      * ``"pthread"``: luồng POSIX
      * ``"pthread-stubs"``: luồng POSIX giả (trên các nền tảng WebAssembly không hỗ trợ phân luồng)
      * ``"solaris"``: luồng Solaris

   .. attribute:: thread_info.lock

      Tên của quá trình triển khai khóa:

      * ``"semaphore"``: một lock sử dụng semaphore
      * ``"mutex+cond"``: một lock sử dụng mutex và biến điều kiện
      * ``None`` nếu không biết thông tin này

   .. attribute:: thread_info.version

      Tên và phiên bản của thư viện thread. Đây là một chuỗi hoặc ``None`` nếu không biết thông tin này.

   .. versionadded:: 3.3


.. data:: tracebacklimit

   Khi biến này được đặt thành một giá trị số nguyên, nó xác định số mức thông tin traceback tối đa được in ra khi xảy ra một ngoại lệ không được xử lý. Giá trị mặc định là ``1000``. Khi được đặt thành ``0`` hoặc nhỏ hơn, mọi thông tin traceback sẽ bị loại bỏ và chỉ kiểu cùng giá trị của ngoại lệ được in ra.


.. function:: unraisablehook(unraisable, /)

   Xử lý một ngoại lệ không thể báo cáo.

   Được gọi khi một ngoại lệ xảy ra nhưng Python không có cách nào xử lý ngoại lệ đó. Ví dụ: khi một destructor gây ra ngoại lệ hoặc trong quá trình thu gom rác (:func:`gc.collect`).

   Đối số *unraisable* có các thuộc tính sau:

   * :attr:`!exc_type`: Kiểu ngoại lệ.
   * :attr:`!exc_value`: Giá trị ngoại lệ, có thể là ``None``.
   * :attr:`!exc_traceback`: Traceback của ngoại lệ, có thể là ``None``.
   * :attr:`!err_msg`: Thông báo lỗi, có thể là ``None``.
   * :attr:`!object`: Đối tượng gây ra ngoại lệ, có thể là ``None``.

   Hook mặc định định dạng :attr:`!err_msg` và :attr:`!object` như sau: ``f'{err_msg}: {object!r}'``; sử dụng thông báo lỗi "Exception ignored in" nếu :attr:`!err_msg` là ``None``.

   :func:`sys.unraisablehook` có thể được ghi đè để kiểm soát cách xử lý các ngoại lệ không thể phát sinh.

   .. seealso::

      :func:`excepthook` xử lý các ngoại lệ chưa được bắt.

   .. warning::

      Việc lưu trữ :attr:`!exc_value` bằng một hook tùy chỉnh có thể tạo ra một chu trình tham chiếu. Cần xóa nó một cách rõ ràng để phá vỡ chu trình tham chiếu khi không còn cần ngoại lệ này.

      Việc lưu trữ :attr:`!object` bằng một hook tùy chỉnh có thể làm cho nó sống lại nếu nó được gán cho một đối tượng đang được hoàn tất. Tránh lưu trữ :attr:`!object` sau khi hook tùy chỉnh hoàn tất để tránh làm các đối tượng sống lại.

   .. audit-event:: sys.unraisablehook hook,unraisable sys.unraisablehook

      Phát sinh sự kiện kiểm tra ``sys.unraisablehook`` với các đối số *hook* và *unraisable* khi xảy ra một ngoại lệ không thể xử lý. Đối tượng *unraisable* giống với đối tượng sẽ được truyền cho hook. Nếu chưa đặt hook nào, *hook* có thể là ``None``.

   .. versionadded:: 3.8

.. data:: version

   Một chuỗi chứa số phiên bản của trình thông dịch Python cùng với thông tin bổ sung về số bản build và trình biên dịch được sử dụng. Chuỗi này được hiển thị khi trình thông dịch tương tác khởi động. Không trích xuất thông tin phiên bản từ chuỗi này; thay vào đó, hãy sử dụng :data:`version_info` và các hàm do
   mô-đun :mod:`platform` cung cấp.


.. data:: api_version

   Phiên bản C API, tương đương với macro C :c:macro:`PYTHON_API_VERSION`. Được định nghĩa để đảm bảo khả năng tương thích ngược.

   Hiện tại, hằng số này không được cập nhật trong các phiên bản Python mới và không hữu ích cho việc quản lý phiên bản. Điều này có thể thay đổi trong tương lai.


.. data:: version_info

   Một tuple chứa năm thành phần của số phiên bản: *major*, *minor*, *micro*, *releaselevel* và *serial*. Tất cả các giá trị ngoại trừ *releaselevel* đều là số nguyên; release level là ``'alpha'``, ``'beta'``, ``'candidate'`` hoặc ``'final'``. Giá trị ``version_info`` tương ứng với phiên bản Python 2.0 là ``(2, 0, 0, 'final', 0)``. Các thành phần cũng có thể được truy cập theo tên, vì vậy ``sys.version_info[0]`` tương đương với ``sys.version_info.major`` và tương tự.

   .. versionchanged:: 3.1
      Đã bổ sung các thuộc tính thành phần có tên.

.. data:: warnoptions

   Đây là chi tiết triển khai của framework warnings; không sửa đổi giá trị này. Tham khảo module :mod:`warnings` để biết thêm thông tin về framework warnings.


.. data:: winver

   Số phiên bản được sử dụng để tạo các khóa registry trên các nền tảng Windows. Giá trị này được lưu dưới dạng tài nguyên chuỗi 1000 trong Python DLL. Giá trị này thường là phiên bản chính và phiên bản phụ của trình thông dịch Python đang chạy. Giá trị được cung cấp trong module :mod:`!sys` nhằm mục đích cung cấp thông tin; việc sửa đổi giá trị này không ảnh hưởng đến các khóa registry được Python sử dụng.

   .. availability:: Windows.


.. data:: monitoring
   :noindex:

   Namespace chứa các hàm và hằng số để đăng ký callback và kiểm soát các sự kiện monitoring. Xem :mod:`sys.monitoring` để biết chi tiết.

.. data:: _xoptions

   Một dictionary chứa các flag tùy theo từng implementation khác nhau được truyền qua tùy chọn dòng lệnh :option:`-X`. Tên tùy chọn được ánh xạ tới giá trị tương ứng nếu được cung cấp rõ ràng, hoặc tới :const:`True`. Ví dụ:

   .. code-block:: shell-session

      $ ./python -Xa=b -Xc
      Python 3.2a3+ (py3k, Oct 16 2010, 20:14:50)
      [GCC 4.4.3] on linux2
      Type "help", "copyright", "credits" or "license" for more information.
      >>> import sys
      >>> sys._xoptions
      {'a': 'b', 'c': True}

   .. impl-detail::

      Đây là cách dành riêng cho CPython để truy cập các tùy chọn được truyền qua
      :option:`-X`. Các implementation khác có thể cung cấp chúng bằng những phương thức khác, hoặc hoàn toàn không cung cấp.

   .. versionadded:: 3.2


.. rubric:: Tài liệu tham khảo

.. [C99] ISO/IEC 9899:1999. "Ngôn ngữ lập trình -- C." Bản dự thảo công khai của tiêu chuẩn này có tại https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1256.pdf\ .

.. _`recursive sizeof recipe`: https://code.activestate.com/recipes/577504-compute-memory-footprint-of-an-object-and-its-cont/
