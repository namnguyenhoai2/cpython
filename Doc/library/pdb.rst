.. _debugger:

:mod:`!pdb` --- Trình gỡ lỗi Python
===================================

.. module:: pdb
   :synopsis: Trình gỡ lỗi Python dành cho các trình thông dịch tương tác.

**Mã nguồn:** :source:`Lib/pdb.py`

.. index:: single: debugging

--------------

Mô-đun :mod:`!pdb` định nghĩa một trình gỡ lỗi mã nguồn tương tác cho các chương trình Python. Mô-đun này hỗ trợ đặt các breakpoint (có điều kiện) và thực hiện từng bước ở cấp dòng mã nguồn, kiểm tra các stack frame, liệt kê mã nguồn và đánh giá mã Python tùy ý trong ngữ cảnh của bất kỳ stack frame nào. Mô-đun cũng hỗ trợ gỡ lỗi sau sự cố (post-mortem) và có thể được gọi dưới sự điều khiển của chương trình.

.. index::
   single: Pdb (class in pdb)
   pair: module; bdb
   pair: module; cmd

Trình gỡ lỗi có thể mở rộng -- thực tế, nó được định nghĩa dưới dạng lớp :class:`Pdb`. Hiện tại, phần này chưa được tài liệu hóa nhưng có thể dễ dàng hiểu được bằng cách đọc mã nguồn. Giao diện mở rộng sử dụng các mô-đun :mod:`bdb` và :mod:`cmd`.

.. seealso::

   Mô-đun :mod:`faulthandler`
      Được dùng để kết xuất các Python traceback một cách rõ ràng khi xảy ra lỗi, sau một khoảng thời gian chờ hoặc khi nhận được tín hiệu từ người dùng.

   Mô-đun :mod:`traceback`
      Giao diện tiêu chuẩn để trích xuất, định dạng và in các stack trace của chương trình Python.

Cách sử dụng thông thường để vào trình gỡ lỗi là chèn::

   import pdb; pdb.set_trace()

Hoặc::

   breakpoint()

tại vị trí bạn muốn vào trình gỡ lỗi, sau đó chạy chương trình. Bạn có thể lần lượt thực thi mã theo sau câu lệnh này, rồi tiếp tục chạy mà không có trình gỡ lỗi bằng lệnh :pdbcmd:`continue`.

.. versionchanged:: 3.7
   :func:`breakpoint` tích hợp sẵn, khi được gọi với các giá trị mặc định, có thể được sử dụng thay cho ``import pdb; pdb.set_trace()``.

::

   def double(x):
      breakpoint()
      return x * 2
   val = 3
   print(f"{val} * 2 is {double(val)}")

Dấu nhắc của trình gỡ lỗi là ``(Pdb)``, cho biết bạn đang ở chế độ gỡ lỗi::

   > ...(2)double()
   -> breakpoint()
   (Pdb) p x
   3
   (Pdb) continue
   3 * 2 is 6

.. versionchanged:: 3.3
   Tính năng hoàn thành bằng phím Tab thông qua module :mod:`readline` khả dụng cho các lệnh và đối số lệnh; ví dụ, các tên global và local hiện tại được cung cấp làm đối số cho lệnh ``p``.


.. _pdb-cli:

Giao diện dòng lệnh
-------------------

.. program:: pdb

Bạn cũng có thể gọi :mod:`!pdb` từ dòng lệnh để debug các script khác. Ví dụ:::

   python -m pdb [-c command] (-m module | -p pid | pyfile) [args ...]

Khi được gọi dưới dạng module, pdb sẽ tự động chuyển sang chế độ post-mortem debugging nếu chương trình đang được debug thoát bất thường. Sau post-mortem debugging (hoặc sau khi chương trình thoát bình thường), pdb sẽ khởi động lại chương trình. Việc tự động khởi động lại giữ nguyên trạng thái của pdb (chẳng hạn như các breakpoint) và trong hầu hết trường hợp hữu ích hơn việc thoát khỏi debugger khi chương trình kết thúc.

.. option:: -c, --command <command>

   Để thực thi các lệnh như thể chúng được cung cấp trong tệp :file:`.pdbrc`; xem
   :ref:`debugger-commands`.

   .. versionchanged:: 3.2
      Đã thêm tùy chọn ``-c``.

.. option:: -m <module>

   Để thực thi các module tương tự như cách ``python -m`` thực hiện. Cũng như với một script, debugger sẽ tạm dừng việc thực thi ngay trước dòng đầu tiên của module.

   .. versionchanged:: 3.7
      Đã thêm tùy chọn ``-m``.

.. option:: -p, --pid <pid>

   Đính kèm vào tiến trình có PID được chỉ định.

   .. versionadded:: 3.14


Để đính kèm vào một tiến trình Python đang chạy nhằm debug từ xa, hãy sử dụng tùy chọn ``-p`` hoặc ``--pid`` cùng với PID của tiến trình đích::

   python -m pdb -p 1234

.. note::

   Việc đính kèm vào một tiến trình đang bị chặn trong system call hoặc đang chờ I/O sẽ chỉ hoạt động sau khi lệnh bytecode tiếp theo được thực thi hoặc khi tiến trình nhận được một signal.

Cách sử dụng điển hình để thực thi một câu lệnh dưới sự điều khiển của debugger là::

   >>> import pdb
   >>> def f(x):
   ...     print(1 / x)
   >>> pdb.run("f(2)")
   > <string>(1)<module>()
   (Pdb) continue
   0.5
   >>>

Cách sử dụng điển hình để kiểm tra một chương trình bị crash là::

   >>> import pdb
   >>> def f(x):
   ...     print(1 / x)
   ...
   >>> f(0)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
     File "<stdin>", line 2, in f
   ZeroDivisionError: division by zero
   >>> pdb.pm()
   > <stdin>(2)f()
   (Pdb) p x
   0
   (Pdb)

.. versionchanged:: 3.13
   Việc triển khai :pep:`667` có nghĩa là các phép gán tên được thực hiện qua ``pdb`` sẽ ngay lập tức ảnh hưởng đến phạm vi hoạt động hiện tại, ngay cả khi đang chạy bên trong một
   :term:`optimized scope`.


Mô-đun định nghĩa các hàm sau; mỗi hàm sẽ vào trình gỡ lỗi theo một cách hơi khác nhau:

.. function:: run(statement, globals=None, locals=None)

   Thực thi *statement* (được cung cấp dưới dạng chuỗi hoặc đối tượng mã) dưới sự điều khiển của trình gỡ lỗi. Lời nhắc của trình gỡ lỗi xuất hiện trước khi bất kỳ mã nào được thực thi; bạn có thể đặt các breakpoint và nhập :pdbcmd:`continue`, hoặc duyệt từng bước qua statement bằng :pdbcmd:`step` hoặc :pdbcmd:`next` (tất cả các lệnh này được giải thích bên dưới). Các đối số *globals* và *locals* tùy chọn chỉ định môi trường nơi mã được thực thi; theo mặc định, từ điển của mô-đun :mod:`__main__` được sử dụng. (Xem phần giải thích về hàm tích hợp sẵn
   :func:`exec` hoặc :func:`eval`.)


.. function:: runeval(expression, globals=None, locals=None)

   Đánh giá *expression* (được cung cấp dưới dạng chuỗi hoặc đối tượng mã) dưới sự điều khiển của trình gỡ lỗi. Khi :func:`runeval` trả về, nó trả về giá trị của *expression*. Ngoài ra, hàm này tương tự như :func:`run`.


.. function:: runcall(function, *args, **kwds)

   Gọi *function* (một đối tượng hàm hoặc phương thức, không phải chuỗi) với các đối số đã cho. Khi :func:`runcall` trả về, nó trả về bất kỳ giá trị nào mà lệnh gọi hàm trả về. Lời nhắc của trình gỡ lỗi xuất hiện ngay khi hàm được gọi.


.. function:: set_trace(*, header=None, commands=None)

   Vào trình gỡ lỗi tại stack frame của hàm gọi. Điều này hữu ích để hard-code một breakpoint tại một vị trí nhất định trong chương trình, ngay cả khi mã không được debug theo cách khác (ví dụ: khi một assertion không thành công). Nếu được cung cấp, *header* sẽ được in ra console ngay trước khi bắt đầu debug. Đối số *commands*, nếu được cung cấp, là danh sách các lệnh sẽ thực thi khi trình gỡ lỗi khởi động.


   .. versionchanged:: 3.7
      Đối số chỉ dùng theo từ khóa *header*.

   .. versionchanged:: 3.13
      :func:`set_trace` will enter the debugger immediately, rather than
      trên dòng mã tiếp theo sẽ được thực thi.

   .. versionadded:: 3.14
      Đối số *commands*.


.. awaitablefunction:: set_trace_async(*, header=None, commands=None)

   phiên bản async của :func:`set_trace`. Hàm này nên được sử dụng bên trong một hàm async với :keyword:`await`.

   .. code-block:: python

      async def f():
          await pdb.set_trace_async()

   Các câu lệnh :keyword:`await` được hỗ trợ nếu trình gỡ lỗi được gọi bằng hàm này.

   .. versionadded:: 3.14

.. function:: post_mortem(t=None)

   Bắt đầu gỡ lỗi post-mortem đối với ngoại lệ đã cho hoặc
   :ref:`traceback object <traceback-objects>`. Nếu không cung cấp giá trị, hàm sẽ sử dụng ngoại lệ hiện đang được xử lý hoặc phát sinh ``ValueError`` nếu không có ngoại lệ nào.

   .. versionchanged:: 3.13
      Đã bổ sung hỗ trợ cho các đối tượng ngoại lệ.

.. function:: pm()

   Bắt đầu gỡ lỗi post-mortem đối với ngoại lệ được tìm thấy trong
   :data:`sys.last_exc`.

.. function:: set_default_backend(backend)

   pdb hỗ trợ hai backend: ``'settrace'`` và ``'monitoring'``. Xem :class:`bdb.Bdb` để biết chi tiết. Người dùng có thể đặt backend mặc định sẽ được sử dụng nếu không chỉ định backend khi khởi tạo :class:`Pdb`. Nếu không chỉ định backend, mặc định là ``'settrace'``.

   .. note::

      :func:`breakpoint` và :func:`set_trace` sẽ không bị ảnh hưởng bởi hàm này. Chúng luôn sử dụng backend ``'monitoring'``.

   .. versionadded:: 3.14

.. function:: get_default_backend()

   Trả về backend mặc định cho pdb.

   .. versionadded:: 3.14

Các hàm ``run*`` và :func:`set_trace` là bí danh để khởi tạo
lớp :class:`Pdb` và gọi phương thức cùng tên. Nếu muốn truy cập các tính năng bổ sung, bạn phải tự thực hiện việc này:

.. class:: Pdb(completekey='tab', stdin=None, stdout=None, skip=None, \
               nosigint=False, readrc=True, mode=None, backend=None, colorize=False)

   :class:`Pdb` là lớp trình gỡ lỗi.

   Các đối số *completekey*, *stdin* và *stdout* được truyền cho lớp :class:`cmd.Cmd` bên dưới; xem phần mô tả của lớp đó.

   Đối số *skip*, nếu được cung cấp, phải là một iterable gồm các mẫu tên module kiểu glob. Trình gỡ lỗi sẽ không bước vào các frame bắt nguồn từ một module khớp với một trong các mẫu này. [1]_

   Theo mặc định, Pdb thiết lập handler cho tín hiệu SIGINT (được gửi khi người dùng nhấn :kbd:`Ctrl-C` trên console) khi bạn đưa ra lệnh :pdbcmd:`continue`. Điều này cho phép bạn quay lại trình gỡ lỗi bằng cách nhấn :kbd:`Ctrl-C`. Nếu bạn không muốn Pdb tác động đến handler SIGINT, hãy đặt *nosigint* thành true.

   Đối số *readrc* mặc định là true và kiểm soát việc Pdb có tải các tệp .pdbrc từ filesystem hay không.

   Đối số *mode* chỉ định cách trình gỡ lỗi được gọi. Đối số này ảnh hưởng đến hoạt động của một số lệnh trình gỡ lỗi. Các giá trị hợp lệ là ``'inline'`` (được sử dụng bởi hàm dựng sẵn breakpoint()), ``'cli'`` (được sử dụng khi gọi từ command line) hoặc ``None`` (để đảm bảo hành vi tương thích ngược, như trước khi thêm đối số *mode*).

   Đối số *backend* chỉ định backend sẽ được sử dụng cho trình gỡ lỗi. Nếu truyền ``None``, backend mặc định sẽ được sử dụng. Xem :func:`set_default_backend`. Nếu không, các backend được hỗ trợ là ``'settrace'`` và ``'monitoring'``.

   Đối số *colorize*, nếu được đặt thành ``True``, sẽ bật đầu ra có màu trong trình debugger, nếu màu được hỗ trợ. Đối số này sẽ làm nổi bật mã nguồn được hiển thị trong pdb.

   Lời gọi ví dụ để bật tracing với *skip*::

      import pdb; pdb.Pdb(skip=['django.*']).set_trace()

   .. audit-event:: pdb.Pdb "" pdb.Pdb

   .. versionchanged:: 3.1
      Đã thêm tham số *skip*.

   .. versionchanged:: 3.2
      Đã thêm tham số *nosigint*. Trước đây, Pdb không bao giờ thiết lập trình xử lý SIGINT.

   .. versionchanged:: 3.6
      Đối số *readrc*.

   .. versionadded:: 3.14
      Đã thêm đối số *mode*.

   .. versionadded:: 3.14
      Đã thêm đối số *backend*.

   .. versionadded:: 3.14
      Đã thêm đối số *colorize*.

   .. versionchanged:: 3.14
      Các breakpoint nội tuyến như :func:`breakpoint` hoặc :func:`pdb.set_trace` sẽ luôn dừng chương trình tại frame đang gọi, bỏ qua mẫu *skip* (nếu có).

   .. method:: run(statement, globals=None, locals=None)
               runeval(expression, globals=None, locals=None) runcall(function, *args, **kwds) set_trace()

      Xem tài liệu về các hàm được giải thích ở trên.


.. _debugger-commands:

Các lệnh của trình gỡ lỗi
-------------------------

Các lệnh được trình gỡ lỗi nhận diện được liệt kê dưới đây. Hầu hết các lệnh có thể được viết tắt bằng một hoặc hai chữ cái như đã chỉ ra; ví dụ: ``h(elp)`` có nghĩa là có thể sử dụng ``h`` hoặc ``help`` để nhập lệnh trợ giúp (nhưng không thể sử dụng ``he`` hoặc ``hel``, cũng như ``H`` hoặc ``Help`` hoặc ``HELP``). Các đối số của lệnh phải được phân tách bằng khoảng trắng (dấu cách hoặc tab). Các đối số tùy chọn được đặt trong dấu ngoặc vuông (``[]``) trong cú pháp lệnh; không được nhập các dấu ngoặc vuông này. Các lựa chọn trong cú pháp lệnh được phân tách bằng dấu gạch đứng (``|``).

Nhập một dòng trống sẽ lặp lại lệnh được nhập gần nhất. Ngoại lệ: nếu lệnh gần nhất là lệnh :pdbcmd:`list`, 11 dòng tiếp theo sẽ được liệt kê.

Các lệnh mà trình gỡ lỗi không nhận dạng được sẽ được xem là các câu lệnh Python và được thực thi trong ngữ cảnh của chương trình đang được gỡ lỗi. Các câu lệnh Python cũng có thể được thêm dấu chấm than (``!``) ở trước. Đây là một cách mạnh mẽ để kiểm tra chương trình đang được gỡ lỗi; thậm chí bạn còn có thể thay đổi một biến hoặc gọi một hàm. Khi một ngoại lệ xảy ra trong câu lệnh như vậy, tên ngoại lệ sẽ được in ra nhưng trạng thái của trình gỡ lỗi không bị thay đổi.

.. versionchanged:: 3.13
   Các biểu thức/câu lệnh có tiền tố là một lệnh pdb hiện được nhận dạng và thực thi chính xác.

Trình gỡ lỗi hỗ trợ :ref:`bí danh <debugger-aliases>`. Bí danh có thể có tham số, cho phép chúng thích ứng ở một mức độ nhất định với ngữ cảnh đang được kiểm tra.

Có thể nhập nhiều lệnh trên một dòng, phân tách bằng ``;;``. (Một ``;`` đơn lẻ không được sử dụng vì nó là dấu phân tách cho nhiều lệnh trên một dòng được chuyển đến trình phân tích cú pháp Python.) Không có cơ chế xử lý thông minh nào được áp dụng để phân tách các lệnh; dữ liệu nhập được tách tại cặp ``;;`` đầu tiên, ngay cả khi cặp này nằm giữa một chuỗi được đặt trong dấu ngoặc kép. Cách xử lý tạm thời cho các chuỗi có hai dấu chấm phẩy liên tiếp là sử dụng phép nối chuỗi ngầm định ``';'';'`` hoặc ``";"";"``.

Để đặt một biến toàn cục tạm thời, hãy sử dụng một *biến convenience*. Một *biến convenience* là biến có tên bắt đầu bằng ``$``. Ví dụ, ``$foo = 1`` đặt một biến toàn cục ``$foo`` mà bạn có thể sử dụng trong phiên làm việc của trình gỡ lỗi. *Các biến convenience* sẽ được xóa khi chương trình tiếp tục thực thi, vì vậy chúng ít có khả năng can thiệp vào chương trình của bạn hơn so với việc sử dụng các biến thông thường như ``foo = 1``.

Có bốn *biến convenience* được đặt sẵn:

* ``$_frame``: khung hiện tại mà bạn đang gỡ lỗi
* ``$_retval``: giá trị trả về nếu frame đang thực hiện lệnh return
* ``$_exception``: exception nếu frame đang phát sinh exception
* ``$_asynctask``: asyncio task nếu pdb dừng trong một hàm async

.. versionadded:: 3.12

   Đã bổ sung tính năng *biến tiện ích*.

.. versionadded:: 3.14
   Đã bổ sung biến tiện ích ``$_asynctask``.

.. index::
   pair: .pdbrc; file
   triple: debugger; configuration; file

Nếu tệp :file:`.pdbrc` tồn tại trong thư mục home của người dùng hoặc trong thư mục hiện tại, tệp này sẽ được đọc bằng encoding ``'utf-8'`` và thực thi như thể nội dung của nó được nhập tại dấu nhắc của debugger, ngoại trừ các dòng trống và các dòng bắt đầu bằng ``#`` sẽ bị bỏ qua. Điều này đặc biệt hữu ích cho các alias. Nếu cả hai tệp đều tồn tại, tệp trong thư mục home sẽ được đọc trước và các alias được định nghĩa ở đó có thể bị ghi đè bởi tệp cục bộ.

.. versionchanged:: 3.2
   :file:`.pdbrc` can now contain commands that continue debugging, such as
   :pdbcmd:`continue` or :pdbcmd:`next`.  Previously, these commands had no
   tác dụng.

.. versionchanged:: 3.11
   :file:`.pdbrc` is now read with ``'utf-8'`` encoding. Previously, it was read
   với encoding locale của hệ thống.


.. pdbcommand:: h(elp) [command]

   Nếu không có đối số, in danh sách các lệnh hiện có. Với *command* làm đối số, in thông tin trợ giúp về lệnh đó. ``help pdb`` hiển thị toàn bộ tài liệu (docstring của module :mod:`pdb`). Vì đối số *command* phải là một identifier, phải nhập ``help exec`` để nhận trợ giúp về lệnh ``!``.

.. pdbcommand:: w(here) [count]

   In stack trace, với frame mới nhất ở dưới cùng. Nếu *count* bằng 0, in mục frame hiện tại. Nếu *count* là số âm, in các frame ít mới nhất - *count*. Nếu *count* là số dương, in các frame mới nhất *count*. Mũi tên (``>``) cho biết frame hiện tại, frame này xác định ngữ cảnh của hầu hết các lệnh.

   .. versionchanged:: 3.14
      Đối số *count* được thêm vào.

.. pdbcommand:: d(own) [count]

   Di chuyển frame hiện tại xuống *count* cấp (mặc định là một cấp) trong stack trace (đến một frame mới hơn).

.. pdbcommand:: u(p) [count]

   Di chuyển frame hiện tại lên *count* cấp (mặc định là một cấp) trong stack trace (đến một frame cũ hơn).

.. pdbcommand:: b(reak) [([filename:]lineno | function) [, condition]]

   Với đối số *lineno*, đặt breakpoint tại dòng *lineno* trong tệp hiện tại. Số dòng có thể được thêm tiền tố *filename* và dấu hai chấm để chỉ định breakpoint trong một tệp khác (có thể là tệp chưa được tải). Tệp được tìm kiếm trên :data:`sys.path`. Các dạng hợp lệ của *filename* là ``/abspath/to/file.py``, ``relpath/file.py``, ``module`` và ``package.module``.

   Với đối số *function*, đặt một điểm dừng tại câu lệnh thực thi đầu tiên trong function đó. *function* có thể là bất kỳ biểu thức nào cho kết quả là một function trong namespace hiện tại.

   Nếu có đối số thứ hai, đó là một biểu thức phải cho kết quả là true trước khi điểm dừng được kích hoạt.

   Nếu không có đối số, liệt kê tất cả các điểm dừng, bao gồm số lần mỗi điểm dừng đã được chạm tới, số lần bỏ qua hiện tại và điều kiện liên quan nếu có.

   Mỗi điểm dừng được gán một số, và tất cả các lệnh khác về điểm dừng đều tham chiếu đến số này.

.. pdbcommand:: tbreak [([filename:]lineno | function) [, condition]]

   Điểm dừng tạm thời, được tự động xóa khi lần đầu tiên được chạm tới. Các đối số giống như đối số của :pdbcmd:`break`.

.. pdbcommand:: cl(ear) [filename:lineno | bpnumber ...]

   Với đối số *filename:lineno*, xóa tất cả các điểm dừng tại dòng này. Với danh sách các số điểm dừng được phân tách bằng dấu cách, xóa các điểm dừng đó. Nếu không có đối số, xóa tất cả các điểm dừng (nhưng trước tiên yêu cầu xác nhận).

.. pdbcommand:: disable bpnumber [bpnumber ...]

   Vô hiệu hóa các điểm dừng được cung cấp dưới dạng danh sách các số điểm dừng được phân tách bằng dấu cách. Vô hiệu hóa một điểm dừng nghĩa là điểm dừng đó không thể khiến chương trình dừng thực thi, nhưng không giống như khi xóa một điểm dừng, nó vẫn nằm trong danh sách các điểm dừng và có thể được bật lại.

.. pdbcommand:: enable bpnumber [bpnumber ...]

   Bật các breakpoint được chỉ định.

.. pdbcommand:: ignore bpnumber [count]

   Đặt số lần bỏ qua cho số breakpoint đã cho. Nếu bỏ qua *count*, số lần bỏ qua được đặt thành 0. Một breakpoint sẽ hoạt động khi số lần bỏ qua bằng 0. Khi khác 0, *count* sẽ giảm đi mỗi khi đạt đến breakpoint, miễn là breakpoint không bị vô hiệu hóa và mọi điều kiện liên kết đều cho kết quả đúng.

.. pdbcommand:: condition bpnumber [condition]

   Đặt *condition* mới cho breakpoint, tức một biểu thức phải cho kết quả đúng trước khi breakpoint được kích hoạt. Nếu không có *condition*, mọi điều kiện hiện có sẽ bị xóa; nói cách khác, breakpoint sẽ không có điều kiện.

.. pdbcommand:: commands [bpnumber]

   Chỉ định danh sách lệnh cho breakpoint số *bpnumber*. Các lệnh sẽ xuất hiện trên những dòng tiếp theo. Nhập một dòng chỉ chứa ``end`` để kết thúc các lệnh. Ví dụ::

      (Pdb) commands 1
      (com) p some_variable
      (com) end
      (Pdb)

   Để xóa tất cả lệnh khỏi một breakpoint, hãy nhập ``commands`` rồi ngay lập tức nhập ``end``; nghĩa là không cung cấp lệnh nào.

   Nếu không có đối số *bpnumber*, ``commands`` sẽ tham chiếu đến breakpoint được đặt gần nhất.

   Bạn có thể sử dụng các lệnh breakpoint để khởi động lại chương trình. Chỉ cần sử dụng lệnh :pdbcmd:`continue`, hoặc :pdbcmd:`step`, hoặc bất kỳ lệnh nào khác tiếp tục quá trình thực thi.

   Chỉ định bất kỳ lệnh nào tiếp tục quá trình thực thi (hiện tại là :pdbcmd:`continue`, :pdbcmd:`step`, :pdbcmd:`next`,
   :pdbcmd:`return`, :pdbcmd:`until`, :pdbcmd:`jump`, :pdbcmd:`quit` và các dạng viết tắt của chúng) sẽ kết thúc danh sách lệnh (như thể ngay sau lệnh đó là end). Điều này là do bất cứ khi nào bạn tiếp tục quá trình thực thi (ngay cả với một lệnh next hoặc step đơn giản), bạn có thể gặp một breakpoint khác—breakpoint đó có thể có danh sách lệnh riêng, dẫn đến sự không rõ ràng về việc nên thực thi danh sách nào.

   Nếu danh sách lệnh chứa lệnh ``silent`` hoặc một lệnh tiếp tục quá trình thực thi, thì thông báo breakpoint chứa thông tin về frame sẽ không được hiển thị.

   .. versionchanged:: 3.14
      Thông tin về frame sẽ không được hiển thị nếu danh sách lệnh có chứa một lệnh tiếp tục quá trình thực thi.

.. pdbcommand:: s(tep)

   Thực thi dòng hiện tại, dừng tại thời điểm có thể dừng đầu tiên (trong một hàm được gọi hoặc ở dòng tiếp theo trong hàm hiện tại).

.. pdbcommand:: n(ext)

   Tiếp tục thực thi cho đến khi đến dòng tiếp theo trong hàm hiện tại hoặc hàm đó trả về.  (Điểm khác biệt giữa :pdbcmd:`next` và :pdbcmd:`step` là :pdbcmd:`step` dừng bên trong một hàm được gọi, còn :pdbcmd:`next` thực thi các hàm được gọi với tốc độ gần như tối đa, chỉ dừng ở dòng tiếp theo trong hàm hiện tại.)

.. pdbcommand:: unt(il) [lineno]

   Nếu không có đối số, tiếp tục thực thi cho đến khi đến dòng có số lớn hơn số của dòng hiện tại.

   Với *lineno*, tiếp tục thực thi cho đến khi đạt đến một dòng có số lớn hơn hoặc bằng *lineno*. Trong cả hai trường hợp, cũng dừng khi frame hiện tại trả về.

   .. versionchanged:: 3.2
      Cho phép cung cấp số dòng cụ thể.

.. pdbcommand:: r(eturn)

   Tiếp tục thực thi cho đến khi hàm hiện tại trả về.

.. pdbcommand:: c(ont(inue))

   Tiếp tục thực thi và chỉ dừng khi gặp breakpoint.

.. pdbcommand:: j(ump) lineno

   Đặt dòng tiếp theo sẽ được thực thi. Chỉ khả dụng trong frame ở dưới cùng. Điều này cho phép bạn quay lại và thực thi lại mã, hoặc tiến lên phía trước để bỏ qua mã mà bạn không muốn chạy.

   Cần lưu ý rằng không phải mọi thao tác nhảy đều được cho phép -- chẳng hạn, không thể nhảy vào giữa một :keyword:`for` vòng lặp hoặc nhảy ra khỏi một
   :keyword:`finally` mệnh đề.

.. pdbcommand:: l(ist) [first[, last]]

   Liệt kê mã nguồn của tệp hiện tại. Không có đối số, liệt kê 11 dòng xung quanh dòng hiện tại hoặc tiếp tục danh sách trước đó. Với ``.`` làm đối số, liệt kê 11 dòng xung quanh dòng hiện tại. Với một đối số, liệt kê 11 dòng xung quanh dòng đó. Với hai đối số, liệt kê phạm vi đã cho; nếu đối số thứ hai nhỏ hơn đối số thứ nhất, nó được hiểu là số lượng dòng.

   Dòng hiện tại trong frame hiện tại được đánh dấu bằng ``->``. Nếu đang debug một exception, dòng nơi exception ban đầu được phát sinh hoặc lan truyền được đánh dấu bằng ``>>``, nếu dòng đó khác với dòng hiện tại.

   .. versionchanged:: 3.2
      Đã thêm marker ``>>``.

.. pdbcommand:: ll | longlist

   Liệt kê toàn bộ mã nguồn của function hoặc frame hiện tại. Các dòng đáng chú ý được đánh dấu như với :pdbcmd:`list`.

   .. versionadded:: 3.2

.. pdbcommand:: a(rgs)

   In các đối số của function hiện tại và các giá trị hiện tại của chúng.

.. pdbcommand:: p expression

   Đánh giá *expression* trong context hiện tại và in giá trị của nó.

   .. note::

      ``print()`` cũng có thể được sử dụng, nhưng không phải là một debugger command --- lệnh này thực thi function :func:`print` của Python.


.. pdbcommand:: pp expression

   Giống lệnh :pdbcmd:`p`, ngoại trừ giá trị của *expression* được in đẹp bằng module :mod:`pprint`.

.. pdbcommand:: whatis expression

   In kiểu của *expression*.

.. pdbcommand:: source expression

   Cố gắng lấy mã nguồn của *expression* và hiển thị mã đó.

   .. versionadded:: 3.2

.. pdbcommand:: display [expression]

   Hiển thị giá trị của *expression* nếu giá trị đó thay đổi, mỗi khi quá trình thực thi dừng trong frame hiện tại.

   Nếu không có *expression*, liệt kê tất cả các biểu thức display cho frame hiện tại.

   .. note::

      Display đánh giá *expression* và so sánh với kết quả của lần đánh giá trước đó của *expression*, vì vậy khi kết quả có thể thay đổi, display có thể không nhận ra các thay đổi.

   Ví dụ::

      lst = []
      breakpoint()
      pass
      lst.append(1)
      print(lst)

   Display sẽ không nhận ra ``lst`` đã bị thay đổi vì kết quả đánh giá bị ``lst.append(1)`` sửa đổi tại chỗ trước khi được so sánh::

      > example.py(3)<module>()
      -> pass
      (Pdb) display lst
      display lst: []
      (Pdb) n
      > example.py(4)<module>()
      -> lst.append(1)
      (Pdb) n
      > example.py(5)<module>()
      -> print(lst)
      (Pdb)

   Bạn có thể dùng một vài thủ thuật với cơ chế sao chép để làm cho nó hoạt động::

      > example.py(3)<module>()
      -> pass
      (Pdb) display lst[:]
      display lst[:]: []
      (Pdb) n
      > example.py(4)<module>()
      -> lst.append(1)
      (Pdb) n
      > example.py(5)<module>()
      -> print(lst)
      display lst[:]: [1]  [old: []]
      (Pdb)

   .. versionadded:: 3.2

.. pdbcommand:: undisplay [expression]

   Không còn hiển thị *expression* trong frame hiện tại. Nếu không có *expression*, hãy xóa tất cả biểu thức display cho frame hiện tại.

   .. versionadded:: 3.2

.. pdbcommand:: interact

   Khởi động một trình thông dịch tương tác (sử dụng module :mod:`code`) trong một global namespace mới được khởi tạo từ các namespace cục bộ và toàn cục của scope hiện tại. Sử dụng ``exit()`` hoặc ``quit()`` để thoát khỏi trình thông dịch và quay lại debugger.

   .. note::

      Vì ``interact`` tạo một namespace riêng mới để thực thi mã, các phép gán cho biến sẽ không ảnh hưởng đến các namespace ban đầu. Tuy nhiên, các thay đổi đối với mọi đối tượng mutable được tham chiếu sẽ được phản ánh trong các namespace ban đầu như thường lệ.

   .. versionadded:: 3.2

   .. versionchanged:: 3.13
      ``exit()`` và ``quit()`` có thể được dùng để thoát khỏi lệnh :pdbcmd:`interact`.

   .. versionchanged:: 3.13
      :pdbcmd:`interact` directs its output to the debugger's
      kênh output thay vì :data:`sys.stderr`.

.. _debugger-aliases:

.. pdbcommand:: alias [name [command]]

   Tạo một alias có tên *tên* thực thi *lệnh*. *Lệnh* phải *không* được đặt trong dấu ngoặc kép. Các tham số có thể thay thế được chỉ định bằng ``%1``, ``%2``, ... và ``%9``, trong khi ``%*`` được thay thế bằng tất cả các tham số. Nếu bỏ qua *lệnh*, alias hiện tại cho *tên* sẽ được hiển thị. Nếu không cung cấp đối số nào, tất cả alias sẽ được liệt kê.

   Các alias có thể được lồng nhau và có thể chứa bất kỳ nội dung nào có thể nhập hợp lệ tại dấu nhắc pdb. Lưu ý rằng các lệnh pdb nội bộ *can* bị alias ghi đè. Khi đó, lệnh này sẽ bị ẩn cho đến khi alias bị xóa. Việc áp dụng alias được thực hiện đệ quy cho từ đầu tiên của dòng lệnh; tất cả các từ còn lại trong dòng được giữ nguyên.

   Ví dụ, dưới đây là hai alias hữu ích (đặc biệt khi được đặt trong tệp
   :file:`.pdbrc`)::

      # In các biến instance (cách dùng "pi classInst")
      alias pi for k in %1.__dict__.keys(): print(f"%1.{k} = {%1.__dict__[k]}")
      # In các biến instance trong self
      alias ps pi self

.. pdbcommand:: unalias name

   Xóa alias được chỉ định *name*.

.. pdbcommand:: ! statement

   Thực thi *câu lệnh* (trên một dòng) trong ngữ cảnh của stack frame hiện tại. Có thể bỏ dấu chấm than, trừ khi từ đầu tiên của câu lệnh trông giống một lệnh debugger, ví dụ:

   .. code-block:: none

      (Pdb) ! n=42
      (Pdb)

   Để đặt một biến toàn cục, bạn có thể thêm tiền tố vào lệnh gán bằng một
   :keyword:`global` câu lệnh trên cùng dòng, ví dụ:

   .. code-block:: none

      (Pdb) global list_options; list_options = ['-l']
      (Pdb)

.. pdbcommand:: run [args ...]
                restart [args ...]

   Khởi động lại chương trình Python đang được debug. Nếu cung cấp *args*, đối số này sẽ được tách bằng :mod:`shlex` và kết quả được dùng làm :data:`sys.argv` mới. Lịch sử, breakpoint, action và các tùy chọn của debugger được giữ nguyên.
   :pdbcmd:`restart` là bí danh của :pdbcmd:`run`.

   .. versionchanged:: 3.14
      :pdbcmd:`run` and :pdbcmd:`restart` commands are disabled when the
      debugger được gọi ở chế độ ``'inline'``.

.. pdbcommand:: q(uit)

   Thoát khỏi trình gỡ lỗi. Chương trình đang được thực thi sẽ bị hủy bỏ. Dữ liệu đầu vào cuối tệp tương đương với :pdbcmd:`quit`.

   Một lời nhắc xác nhận sẽ được hiển thị nếu trình gỡ lỗi được gọi ở chế độ ``'inline'``. ``y``, ``Y``, ``<Enter>`` hoặc ``EOF`` sẽ xác nhận việc thoát.

   .. versionchanged:: 3.14
      Một lời nhắc xác nhận sẽ được hiển thị nếu trình gỡ lỗi được gọi ở chế độ ``'inline'``. Sau khi xác nhận, trình gỡ lỗi sẽ gọi
      :func:`sys.exit` ngay lập tức, thay vì phát sinh :exc:`bdb.BdbQuit` trong sự kiện trace tiếp theo.

.. pdbcommand:: debug code

   Đi vào một trình gỡ lỗi đệ quy để thực hiện từng bước qua *code* (là một biểu thức hoặc câu lệnh tùy ý được thực thi trong môi trường hiện tại).

.. pdbcommand:: retval

   In giá trị trả về của lần return cuối cùng trong hàm hiện tại.

.. pdbcommand:: exceptions [excnumber]

   Liệt kê hoặc chuyển đổi giữa các ngoại lệ được liên kết.

   Khi sử dụng ``pdb.pm()`` hoặc ``Pdb.post_mortem(...)`` với một exception được liên kết thay vì traceback, người dùng có thể chuyển đổi giữa các exception được liên kết bằng lệnh ``exceptions`` để liệt kê các exception và ``exceptions <number>`` để chuyển sang exception đó.


   Ví dụ::

        def out():
            try:
                middle()
            except Exception as e:
                raise ValueError("reraise middle() error") from e

        def middle():
            try:
                return inner(0)
            except Exception as e:
                raise ValueError("Middle fail")

        def inner(x):
            1 / x

        out()

   gọi ``pdb.pm()`` sẽ cho phép chuyển đổi giữa các exception::

    > example.py(5)out()
    -> raise ValueError("reraise middle() error") from e

    (Pdb) exceptions
      0 ZeroDivisionError('division by zero')
      1 ValueError('Middle fail')
    > 2 ValueError('reraise middle() error')

    (Pdb) exceptions 0
    > example.py(16)inner()
    -> 1 / x

    (Pdb) up
    > example.py(10)middle()
    -> return inner(0)

   .. versionadded:: 3.13

.. rubric:: Chú thích cuối trang

.. [1] Một frame có được xem là bắt nguồn từ một module nhất định hay không được xác định bởi ``__name__`` trong các biến toàn cục của frame.
