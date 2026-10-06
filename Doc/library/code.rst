:mod:`!code` --- Các lớp cơ sở của trình thông dịch
===================================================

.. module:: code
   :synopsis: Các tiện ích để triển khai các vòng lặp read-eval-print.

**Mã nguồn:** :source:`Lib/code.py`

--------------

Module ``code`` cung cấp các tiện ích để triển khai các vòng lặp read-eval-print trong Python. Module này bao gồm hai lớp và các hàm tiện ích, có thể được dùng để xây dựng các ứng dụng cung cấp lời nhắc của trình thông dịch tương tác.


.. class:: InteractiveInterpreter(locals=None)

   Lớp này xử lý việc phân tích cú pháp và trạng thái của trình thông dịch (namespace của người dùng); lớp này không xử lý việc đệm đầu vào, hiển thị lời nhắc hoặc đặt tên tệp đầu vào (tên tệp luôn được truyền vào một cách rõ ràng). Đối số *locals* tùy chọn chỉ định một mapping được dùng làm namespace nơi mã sẽ được thực thi; theo mặc định, đó là một dictionary mới được tạo, với khóa ``'__name__'`` được đặt thành ``'__console__'`` và khóa ``'__doc__'`` được đặt thành ``None``.

   Lưu ý rằng các đối tượng hàm và lớp được tạo trong một
   :class:`!InteractiveInterpreter` instance sẽ thuộc về namespace được chỉ định bởi *locals*. Chúng chỉ có thể được pickle nếu *locals* là namespace của một module hiện có.


.. class:: InteractiveConsole(locals=None, filename="<console>", local_exit=False)

   Mô phỏng sát hành vi của trình thông dịch Python tương tác. Lớp này xây dựng trên :class:`InteractiveInterpreter` và bổ sung lời nhắc bằng ``sys.ps1`` và ``sys.ps2`` quen thuộc, cùng với bộ đệm đầu vào. Nếu *local_exit* là true, ``exit()`` và ``quit()`` trong console sẽ không phát sinh :exc:`SystemExit`, mà thay vào đó quay lại mã gọi.

   .. versionchanged:: 3.13
      Đã thêm tham số *local_exit*.

.. function:: interact(banner=None, readfunc=None, local=None, exitmsg=None, local_exit=False)

   Hàm tiện ích để chạy vòng lặp read-eval-print. Hàm này tạo một thể hiện mới của :class:`InteractiveConsole` và đặt *readfunc* để dùng làm phương thức :meth:`InteractiveConsole.raw_input`, nếu được cung cấp. Nếu *local* được cung cấp, giá trị này sẽ được truyền cho hàm khởi tạo :class:`InteractiveConsole` để dùng làm namespace mặc định cho vòng lặp trình thông dịch. Nếu *local_exit* được cung cấp, giá trị này sẽ được truyền cho hàm khởi tạo :class:`InteractiveConsole`. Sau đó, phương thức :meth:`~InteractiveConsole.interact` của thể hiện sẽ được chạy với *banner* và *exitmsg* được truyền làm banner và thông báo thoát cần sử dụng, nếu được cung cấp. Đối tượng console sẽ bị loại bỏ sau khi sử dụng.

   .. versionchanged:: 3.6
      Đã thêm tham số *exitmsg*.

   .. versionchanged:: 3.13
      Đã thêm tham số *local_exit*.

.. function:: compile_command(source, filename="<input>", symbol="single")

   Hàm này hữu ích cho các chương trình muốn mô phỏng vòng lặp chính của trình thông dịch Python (còn gọi là vòng lặp read-eval-print). Phần khó là xác định khi nào người dùng đã nhập một lệnh chưa hoàn chỉnh có thể được hoàn tất bằng cách nhập thêm văn bản (thay vì một lệnh hoàn chỉnh hoặc lỗi cú pháp). Hàm này *almost* luôn đưa ra quyết định giống như vòng lặp chính của trình thông dịch thực.

   *source* là chuỗi nguồn; *filename* là tên tệp tùy chọn mà từ đó mã nguồn được đọc, mặc định là ``'<input>'``; còn *symbol* là ký hiệu bắt đầu ngữ pháp tùy chọn, phải là ``'single'`` (mặc định), ``'eval'`` hoặc ``'exec'``.

   Trả về một đối tượng code (giống như ``compile(source, filename, symbol)``) nếu lệnh hoàn chỉnh và hợp lệ; ``None`` nếu lệnh chưa hoàn chỉnh; raises
   :exc:`SyntaxError` nếu lệnh hoàn chỉnh nhưng chứa lỗi cú pháp, hoặc raises :exc:`OverflowError` hoặc :exc:`ValueError` nếu lệnh chứa một literal không hợp lệ.


.. _interpreter-objects:

Các đối tượng Interactive Interpreter
-------------------------------------


.. method:: InteractiveInterpreter.runsource(source, filename="<input>", symbol="single")

   Biên dịch và chạy một phần source trong interpreter. Các đối số giống như đối số của
   :func:`compile_command`; giá trị mặc định của *filename* là ``'<input>'``, còn của *symbol* là ``'single'``. Có thể xảy ra một trong các trường hợp sau:

   * Đầu vào không chính xác; :func:`compile_command` đã phát sinh một exception (thường là :exc:`SyntaxError`). Một syntax traceback sẽ được in bằng cách gọi phương thức :meth:`showsyntaxerror`. :meth:`runsource` trả về ``False``.

   * Đầu vào chưa hoàn chỉnh và cần thêm dữ liệu; :func:`compile_command` đã trả về ``None``. :meth:`runsource` trả về ``True``.

   * Đầu vào đã hoàn tất; :func:`compile_command` đã trả về một đối tượng mã. Mã được thực thi bằng cách gọi :meth:`runcode` (phương thức này cũng xử lý các ngoại lệ trong thời gian chạy, ngoại trừ :exc:`SystemExit`). :meth:`runsource` trả về ``False``.

   Giá trị trả về có thể được dùng để quyết định sử dụng ``sys.ps1`` hay ``sys.ps2`` để nhắc nhập dòng tiếp theo.


.. method:: InteractiveInterpreter.runcode(code)

   Thực thi một đối tượng mã. Khi xảy ra ngoại lệ, :meth:`showtraceback` được gọi để hiển thị traceback. Tất cả các ngoại lệ đều được bắt, ngoại trừ :exc:`SystemExit`, ngoại lệ này được phép lan truyền.

   Lưu ý về :exc:`KeyboardInterrupt`: ngoại lệ này có thể xảy ra ở nơi khác trong mã và không phải lúc nào cũng được bắt. Bên gọi phải sẵn sàng xử lý ngoại lệ này.


.. method:: InteractiveInterpreter.showsyntaxerror(filename=None)

   Hiển thị lỗi cú pháp vừa xảy ra. Thao tác này không hiển thị stack trace vì lỗi cú pháp không có stack trace. Nếu cung cấp *filename*, giá trị này sẽ được chèn vào ngoại lệ thay cho tên tệp mặc định do trình phân tích cú pháp của Python cung cấp, vì trình phân tích này luôn sử dụng ``'<string>'`` khi đọc từ một chuỗi. Đầu ra được ghi bởi phương thức :meth:`write`.


.. method:: InteractiveInterpreter.showtraceback()

   Hiển thị ngoại lệ vừa xảy ra. Chúng tôi loại bỏ mục đầu tiên trong stack vì mục đó nằm bên trong phần triển khai của đối tượng trình thông dịch. Đầu ra được ghi bởi phương thức :meth:`write`.

   .. versionchanged:: 3.5 Thay vào đó, toàn bộ traceback được liên kết sẽ được hiển thị
      chỉ của traceback chính.


.. method:: InteractiveInterpreter.write(data)

   Ghi một chuỗi vào luồng lỗi chuẩn (``sys.stderr``). Các lớp dẫn xuất nên ghi đè phương thức này để cung cấp cách xử lý đầu ra phù hợp khi cần.


.. _console-objects:

Đối tượng Console tương tác
---------------------------

Lớp :class:`InteractiveConsole` là lớp con của
:class:`InteractiveInterpreter`, do đó cung cấp tất cả các phương thức của các đối tượng trình thông dịch cũng như những bổ sung sau.


.. method:: InteractiveConsole.interact(banner=None, exitmsg=None)

   Mô phỏng rất sát console Python tương tác. Đối số tùy chọn *banner* chỉ định banner sẽ in trước lần tương tác đầu tiên; theo mặc định, đối số này in một banner tương tự banner do trình thông dịch Python chuẩn in, theo sau là tên lớp của đối tượng console trong dấu ngoặc đơn (để không nhầm với trình thông dịch thực -- vì nó gần như giống hệt!).

   Đối số tùy chọn *exitmsg* chỉ định thông báo thoát được in khi thoát. Truyền một chuỗi rỗng để bỏ qua thông báo thoát. Nếu *exitmsg* không được cung cấp hoặc ``None``, một thông báo mặc định sẽ được in.

   .. versionchanged:: 3.4
      Để không in bất kỳ banner nào, hãy truyền vào một chuỗi rỗng.

   .. versionchanged:: 3.6
      In thông báo thoát khi thoát.


.. method:: InteractiveConsole.push(line)

   Đẩy một dòng văn bản mã nguồn vào interpreter. Dòng này không được có ký tự xuống dòng ở cuối; nhưng có thể chứa các ký tự xuống dòng bên trong. Dòng này được nối vào bộ đệm, sau đó phương thức :meth:`~InteractiveInterpreter.runsource` của interpreter được gọi với toàn bộ nội dung đã nối của bộ đệm làm mã nguồn. Nếu điều này cho biết lệnh đã được thực thi hoặc không hợp lệ, bộ đệm sẽ được đặt lại; nếu không, lệnh chưa hoàn chỉnh và bộ đệm được giữ nguyên như sau khi dòng này được nối vào. Giá trị trả về là ``True`` nếu cần thêm dữ liệu đầu vào, ``False`` nếu dòng đã được xử lý theo một cách nào đó (điều này giống với :meth:`!runsource`).


.. method:: InteractiveConsole.resetbuffer()

   Xóa mọi văn bản mã nguồn chưa được xử lý khỏi bộ đệm đầu vào.


.. method:: InteractiveConsole.raw_input(prompt="")

   Viết lời nhắc và đọc một dòng. Dòng được trả về không bao gồm ký tự xuống dòng ở cuối. Khi người dùng nhập chuỗi phím EOF, :exc:`EOFError` được phát sinh. Phần triển khai cơ sở đọc từ ``sys.stdin``; lớp con có thể thay thế phần này bằng một cách triển khai khác.
