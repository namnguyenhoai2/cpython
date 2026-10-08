.. _library-intro:

**********
Giới thiệu
**********

Thư viện chuẩn Python bao gồm một tập hợp các module. Có nhiều cách để phân tích tập hợp này. Hầu hết các module được viết bằng Python, nhưng một số được viết bằng C. Tất cả đều có thể được import vào chương trình của bạn để bổ sung chức năng. Một số module cung cấp các interface rất đặc thù của Python, chẳng hạn như in stack trace; một số cung cấp các interface dành riêng cho những hệ điều hành cụ thể, chẳng hạn như quyền truy cập vào phần cứng cụ thể; những module khác cung cấp các interface dành riêng cho một lĩnh vực ứng dụng cụ thể, chẳng hạn như phát triển web. Một số module có sẵn trong mọi phiên bản và bản port của Python; một số khác chỉ có sẵn khi hệ thống bên dưới hỗ trợ hoặc yêu cầu chúng; còn những module khác nữa chỉ có sẵn khi một tùy chọn cấu hình cụ thể được chọn lúc Python được biên dịch và cài đặt.

Nếu bạn bắt đầu đọc tài liệu hướng dẫn này từ đầu và chuyển sang chương tiếp theo khi thấy chán, bạn sẽ có được một cái nhìn tổng quan khá đầy đủ về các module có sẵn và những lĩnh vực ứng dụng được thư viện Python hỗ trợ. Tất nhiên, bạn không *phải* đọc nó như đọc một cuốn tiểu thuyết --- bạn cũng có thể xem mục lục (ở đầu tài liệu), hoặc tìm một hàm, module hay thuật ngữ cụ thể trong phần chỉ mục (ở cuối tài liệu). Cuối cùng, nếu thích tìm hiểu những chủ đề ngẫu nhiên, bạn có thể chọn một trang bất kỳ và đọc một hoặc hai phần. Bất kể bạn đọc các phần của tài liệu này theo thứ tự nào, trước tiên bạn nên đọc
:ref:`built-in-funcs`, vì phần còn lại của mục này giả định rằng bạn đã quen thuộc với nội dung đó.

.. seealso::

   Các hàm và lớp dựng sẵn (có thể sử dụng mà không cần một
   :keyword:`import` câu lệnh) được mô tả trong :ref:`builtins-index`.


.. _availability:

Lưu ý về tính khả dụng
======================

* Ghi chú "Availability: Unix" có nghĩa là hàm này thường được tìm thấy trên các hệ thống Unix. Ghi chú này không khẳng định rằng hàm tồn tại trên một hệ điều hành cụ thể.

* Nếu không có ghi chú riêng, tất cả các hàm có ghi chú "Availability: Unix" đều được hỗ trợ trên macOS, iOS và Android; tất cả các hệ điều hành này đều được xây dựng trên một lõi Unix.

* Nếu một ghi chú về tính khả dụng chứa cả phiên bản Kernel tối thiểu và phiên bản libc tối thiểu, thì cả hai điều kiện đều phải được đáp ứng. Ví dụ: một tính năng có ghi chú *Availability: Linux >= 3.17 with glibc >= 2.27* yêu cầu cả Linux 3.17 trở lên và glibc 2.27 trở lên.

.. _wasm-availability:

Các nền tảng WebAssembly
------------------------

Các nền tảng `WebAssembly`_ ``wasm32-emscripten`` (`Emscripten`_) và ``wasm32-wasi`` (`WASI`_) cung cấp một phần các API POSIX. Các runtime WebAssembly và trình duyệt được sandbox và chỉ có quyền truy cập hạn chế vào host cũng như các tài nguyên bên ngoài. Bất kỳ module nào trong thư viện chuẩn Python sử dụng process, threading, networking, signal hoặc các hình thức giao tiếp liên tiến trình (IPC) khác đều либо không khả dụng, либо có thể không hoạt động như trên các hệ thống tương tự Unix khác. Các hàm liên quan đến I/O tệp, hệ thống tệp và quyền Unix cũng bị hạn chế. Emscripten không cho phép I/O blocking. Các thao tác blocking khác như
:func:`~time.sleep` cũng chặn event loop của trình duyệt.

Các thuộc tính và hành vi của Python trên các nền tảng WebAssembly phụ thuộc vào phiên bản `Emscripten`_-SDK hoặc `WASI`_-SDK, các runtime WASM (trình duyệt, NodeJS, `wasmtime`_) và các cờ tại thời điểm build Python. WebAssembly, Emscripten và WASI là các tiêu chuẩn đang phát triển; một số tính năng như networking có thể được hỗ trợ trong tương lai.

Đối với Python trong trình duyệt, người dùng nên cân nhắc `Pyodide`_ hoặc `PyScript`_. PyScript được xây dựng trên Pyodide, còn Pyodide được xây dựng trên CPython và Emscripten. Pyodide cung cấp quyền truy cập vào JavaScript và các API DOM của trình duyệt, cũng như khả năng kết nối mạng hạn chế thông qua các API ``XMLHttpRequest`` và ``Fetch`` của JavaScript.

* Các API liên quan đến process không khả dụng hoặc luôn thất bại với lỗi. Điều đó bao gồm các API tạo process mới (:func:`~os.fork`,
  :func:`~os.execve`), chờ process (:func:`~os.waitpid`), gửi signal (:func:`~os.kill`) hoặc tương tác với process theo cách khác. Các
  :mod:`subprocess` có thể được import nhưng không hoạt động.

* Module :mod:`socket` khả dụng, nhưng bị giới hạn và hoạt động khác với các nền tảng khác. Trên Emscripten, socket luôn ở chế độ non-blocking và cần thêm mã JavaScript cùng các helper trên máy chủ để proxy TCP thông qua WebSocket; xem `Emscripten Networking <Emscripten Networking_>`_ để biết thêm thông tin. WASI snapshot preview 1 chỉ cho phép sử dụng socket từ một file descriptor hiện có.

* Một số hàm chỉ là stub, không thực hiện thao tác nào và luôn trả về các giá trị được hardcode.

* Các hàm liên quan đến file descriptor, quyền tệp, chủ sở hữu tệp và liên kết bị giới hạn, đồng thời không hỗ trợ một số thao tác. Ví dụ: WASI không cho phép symlink có tên tệp tuyệt đối.

.. _WebAssembly: https://webassembly.org/
.. _Emscripten: https://emscripten.org/
.. _Emscripten Networking: https://emscripten.org/docs/porting/networking.html
.. _WASI: https://wasi.dev/
.. _wasmtime: https://wasmtime.dev/
.. _Pyodide: https://pyodide.org/
.. _PyScript: https://pyscript.net/

.. _mobile-availability:
.. _iOS-availability:

Nền tảng di động
----------------

Android và iOS, trên hầu hết phương diện, là các hệ điều hành POSIX. I/O tệp, xử lý socket và threading đều hoạt động như trên bất kỳ hệ điều hành POSIX nào. Tuy nhiên, có một số khác biệt lớn:

* Các nền tảng di động chỉ có thể sử dụng Python ở chế độ "embedded". Không có Python REPL và không thể sử dụng các tệp thực thi riêng biệt như :program:`python` hoặc
  :program:`pip`. Để thêm mã Python vào ứng dụng di động, bạn phải sử dụng :ref:`Python embedding API <embedding>`. Để biết thêm chi tiết, hãy xem
  :ref:`using-android` và :ref:`using-ios`.

* Subprocess:

  * Trên Android, có thể tạo subprocess nhưng `officially unsupported <https://issuetracker.google.com/issues/128554619#comment4>`__. Cụ thể, Android không hỗ trợ bất kỳ phần nào của System V IPC API, vì vậy :mod:`multiprocessing` không khả dụng.

  * Ứng dụng iOS không thể sử dụng bất kỳ hình thức xử lý tiến trình con, xử lý đa tiến trình hoặc giao tiếp liên tiến trình nào. Nếu ứng dụng iOS cố tạo một tiến trình con, tiến trình tạo tiến trình con đó sẽ bị treo hoặc gặp sự cố. Ứng dụng iOS không thể thấy các ứng dụng khác đang chạy, cũng không thể giao tiếp với các ứng dụng khác đang chạy, ngoài các API dành riêng cho iOS được cung cấp cho mục đích này.

* Ứng dụng di động bị hạn chế quyền sửa đổi tài nguyên hệ thống (chẳng hạn như đồng hồ hệ thống). Các tài nguyên này thường *có thể đọc*, nhưng những nỗ lực sửa đổi chúng thường sẽ thất bại.

* Đầu vào và đầu ra của console:

  * Trên Android, ``stdout`` và ``stderr`` gốc không được kết nối với bất kỳ thứ gì, vì vậy Python tự cài đặt các stream riêng để chuyển hướng thông báo vào system log. Bạn có thể xem các thông báo này lần lượt dưới các tag ``python.stdout`` và ``python.stderr``.

  * Ứng dụng iOS có khái niệm hạn chế về đầu ra của console. ``stdout`` và ``stderr`` *tồn tại*, và nội dung được ghi vào ``stdout`` và ``stderr`` sẽ hiển thị trong log khi chạy bằng Xcode, nhưng nội dung này *sẽ không* được ghi vào system log. Nếu người dùng đã cài đặt ứng dụng của bạn cung cấp log của ứng dụng để hỗ trợ chẩn đoán, log đó sẽ không bao gồm bất kỳ chi tiết nào được ghi vào ``stdout`` hoặc ``stderr``.

  * Ứng dụng di động hoàn toàn không có ``stdin`` có thể sử dụng được. Mặc dù ứng dụng có thể hiển thị bàn phím trên màn hình, đây là một tính năng phần mềm chứ không phải thứ được kết nối với ``stdin``.

    Do đó, các module Python liên quan đến việc thao tác console (chẳng hạn như
    :mod:`curses` và :mod:`readline`) không khả dụng trên các nền tảng di động.
