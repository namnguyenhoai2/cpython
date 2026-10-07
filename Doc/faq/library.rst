:tocdepth: 2

===========================================
Câu hỏi thường gặp về Thư viện và Extension
===========================================

.. only:: html

   .. contents::

Câu hỏi chung về Thư viện
=========================

Làm thế nào để tìm một module hoặc ứng dụng thực hiện tác vụ X?
---------------------------------------------------------------

Hãy xem :ref:`Tài liệu tham khảo về Thư viện <library-index>` để kiểm tra xem có module standard library phù hợp hay không. (Cuối cùng, bạn sẽ biết standard library có những gì và có thể bỏ qua bước này.)

Đối với các package của bên thứ ba, hãy tìm kiếm trên `Python Package Index <https://pypi.org>`_ hoặc thử `Google <https://www.google.com>`_ hay một công cụ tìm kiếm web khác. Tìm kiếm "Python" cùng với một hoặc hai từ khóa về chủ đề bạn quan tâm thường sẽ giúp bạn tìm được thông tin hữu ích.


Tệp mã nguồn math.py (socket.py, regex.py, v.v.) nằm ở đâu?
-----------------------------------------------------------

Nếu không thể tìm thấy tệp mã nguồn của một module, có thể đó là module tích hợp sẵn hoặc module được tải động, được triển khai bằng C, C++ hoặc một ngôn ngữ biên dịch khác. Trong trường hợp này, bạn có thể không có tệp mã nguồn hoặc tệp đó có thể có dạng như
:file:`mathmodule.c`, ở đâu đó trong một thư mục mã nguồn C (không nằm trên Python Path).

Có (ít nhất) ba loại module trong Python:

1) module được viết bằng Python (.py);
2) module được viết bằng C và được tải động (.dll, .pyd, .so, .sl, v.v.);
3) module được viết bằng C và được liên kết với trình thông dịch; để lấy danh sách các module này, hãy nhập::

      import sys
      print(sys.builtin_module_names)


Làm thế nào để khiến một tập lệnh Python có thể thực thi trên Unix?
-------------------------------------------------------------------

Bạn cần làm hai việc: chế độ của tệp tập lệnh phải cho phép thực thi và dòng đầu tiên phải bắt đầu bằng ``#!`` theo sau là đường dẫn đến trình thông dịch Python.

Cách đầu tiên được thực hiện bằng cách chạy ``chmod +x scriptfile`` hoặc có thể là ``chmod 755 scriptfile``.

Cách thứ hai có thể được thực hiện theo nhiều cách. Cách đơn giản nhất là viết::

  #!/usr/local/bin/python

ở dòng đầu tiên của tệp, sử dụng pathname trỏ đến vị trí cài đặt Python interpreter trên nền tảng của bạn.

Nếu muốn script không phụ thuộc vào vị trí của Python interpreter, bạn có thể sử dụng chương trình :program:`env`. Hầu hết các biến thể Unix đều hỗ trợ cách sau, với điều kiện Python interpreter nằm trong một thư mục trên :program:`env` của người dùng
:envvar:`PATH`::

  #!/usr/bin/env python

*Đừng* làm vậy với các CGI script. Biến :envvar:`PATH` dành cho CGI script thường rất tối giản, vì vậy bạn cần sử dụng pathname tuyệt đối thực tế của interpreter.

Đôi khi, môi trường của người dùng quá đầy khiến chương trình :program:`/usr/bin/env` bị lỗi; hoặc hoàn toàn không có chương trình env. Trong trường hợp đó, bạn có thể thử thủ thuật sau (do Alex Rezinsky đề xuất):

.. code-block:: sh

   #! /bin/sh
   """:"
   exec python $0 ${1+"$@"}
   """

Một nhược điểm nhỏ là cách này định nghĩa chuỗi __doc__ của script. Tuy nhiên, bạn có thể khắc phục bằng cách thêm::

   __doc__ = """...Whatever..."""



Python có package curses/termcap không?
---------------------------------------

.. XXX curses *is* built by default, isn't it?

Đối với các biến thể Unix: Bản phân phối mã nguồn Python tiêu chuẩn đi kèm một module curses trong thư mục con :source:`Modules`, mặc dù module này không được biên dịch theo mặc định. (Lưu ý rằng module này không có trong bản phân phối Windows -- không có module curses cho Windows.)

Module :mod:`curses` hỗ trợ các tính năng curses cơ bản cũng như nhiều hàm bổ sung từ ncurses và SYSV curses, chẳng hạn như màu sắc, hỗ trợ bộ ký tự thay thế, pads và hỗ trợ chuột. Điều này có nghĩa là module này không tương thích với các hệ điều hành chỉ có BSD curses, nhưng dường như hiện không có hệ điều hành nào còn được duy trì thuộc nhóm này.


Trong Python có thành phần tương đương với onexit() của C không?
----------------------------------------------------------------

Module :mod:`atexit` cung cấp một hàm register tương tự như của C
:c:func:`!onexit`.


Tại sao các signal handler của tôi không hoạt động?
---------------------------------------------------

Vấn đề thường gặp nhất là signal handler được khai báo với danh sách đối số không đúng. Nó được gọi như sau::

   handler(signum, frame)

vì vậy nó phải được khai báo với hai tham số::

   def handler(signum, frame):
       ...


Các tác vụ thường gặp
=====================

Làm thế nào để kiểm thử một chương trình hoặc thành phần Python?
----------------------------------------------------------------

Python đi kèm với hai framework kiểm thử. Mô-đun :mod:`doctest` tìm các ví dụ trong docstring của một mô-đun và chạy chúng, rồi so sánh đầu ra với đầu ra dự kiến được nêu trong docstring.

Mô-đun :mod:`unittest` là một framework kiểm thử nâng cao hơn, được xây dựng theo mô hình của các framework kiểm thử Java và Smalltalk.

Để việc kiểm thử dễ dàng hơn, bạn nên sử dụng thiết kế module tốt trong chương trình của mình. Chương trình của bạn nên đóng gói gần như toàn bộ chức năng trong các hàm hoặc phương thức của lớp -- và điều này đôi khi còn mang lại hiệu quả bất ngờ và thú vị là làm chương trình chạy nhanh hơn (vì việc truy cập biến cục bộ nhanh hơn truy cập biến toàn cục). Ngoài ra, chương trình nên tránh phụ thuộc vào việc thay đổi các biến toàn cục, vì điều này khiến việc kiểm thử khó hơn nhiều.

"logic chính toàn cục" của chương trình có thể đơn giản như sau::

   if __name__ == "__main__":
       main_logic()

ở cuối module chính của chương trình.

Khi chương trình của bạn được tổ chức thành một tập hợp có thể quản lý gồm các hành vi của hàm và lớp, bạn nên viết các hàm kiểm thử để thực thi những hành vi đó. Một test suite tự động hóa một chuỗi bài kiểm thử có thể được liên kết với từng module. Điều này nghe có vẻ tốn nhiều công sức, nhưng vì Python rất ngắn gọn và linh hoạt nên việc này dễ hơn đáng kể. Bạn có thể khiến việc lập trình trở nên thú vị và dễ chịu hơn nhiều bằng cách viết các hàm kiểm thử song song với "production code", vì điều này giúp bạn dễ dàng tìm ra lỗi và thậm chí cả những thiếu sót trong thiết kế sớm hơn.

Các "support module" không được dùng làm module chính của chương trình có thể bao gồm một bài tự kiểm thử cho module đó.::

   if __name__ == "__main__":
       self_test()

Ngay cả những chương trình tương tác với các giao diện bên ngoài phức tạp cũng có thể được kiểm thử khi các giao diện bên ngoài không khả dụng, bằng cách sử dụng các giao diện "giả" được triển khai bằng Python.


Làm cách nào để tạo tài liệu từ các chuỗi tài liệu?
---------------------------------------------------

Module :mod:`pydoc` có thể tạo HTML từ các chuỗi tài liệu trong mã nguồn Python của bạn. Một lựa chọn khác để tạo tài liệu API hoàn toàn từ các chuỗi tài liệu là `epydoc <https://epydoc.sourceforge.net/>`_. `Sphinx <https://www.sphinx-doc.org>`_ cũng có thể đưa nội dung chuỗi tài liệu vào.


Làm cách nào để nhận từng lần nhấn phím riêng lẻ?
-------------------------------------------------

Đối với các biến thể Unix, có một số giải pháp. Thực hiện việc này bằng curses khá đơn giản, nhưng curses là một module tương đối lớn cần tìm hiểu.

.. XXX this doesn't work out of the box, some IO expert needs to check why

   Here's a solution without curses::

   import termios, fcntl, sys, os
   fd = sys.stdin.fileno()

   oldterm = termios.tcgetattr(fd)
   newattr = termios.tcgetattr(fd)
   newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
   termios.tcsetattr(fd, termios.TCSANOW, newattr)

   oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
   fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

   try:
       while True:
           try:
               c = sys.stdin.read(1)
               print("Got character", repr(c))
           except OSError:
               pass
   finally:
       termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
       fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

   You need the :mod:`termios` and the :mod:`fcntl` module for any of this to
   work, and I've only tried it on Linux, though it should work elsewhere.  In
   this code, characters are read and printed one at a time.

   :func:`termios.tcsetattr` turns off stdin's echoing and disables canonical
   mode.  :func:`fcntl.fnctl` is used to obtain stdin's file descriptor flags
   and modify them for non-blocking mode.  Since reading stdin when it is empty
   results in an :exc:`OSError`, this error is caught and ignored.

   .. versionchanged:: 3.3
      *sys.stdin.read* used to raise :exc:`IOError`. Starting from Python 3.3
      :exc:`IOError` is alias for :exc:`OSError`.


Threads
=======

Lập trình bằng threads như thế nào?
-----------------------------------

Hãy đảm bảo sử dụng module :mod:`threading` chứ không phải module :mod:`_thread`. Module :mod:`threading` xây dựng các abstraction thuận tiện dựa trên những primitive cấp thấp do module :mod:`_thread` cung cấp.


Tại sao dường như không có thread nào của tôi chạy?
---------------------------------------------------

Ngay khi main thread thoát, mọi thread đều bị dừng. Main thread của bạn đang chạy quá nhanh, không cho các thread có thời gian thực hiện bất kỳ công việc nào.

Một cách khắc phục đơn giản là thêm một lệnh sleep vào cuối chương trình với thời lượng đủ dài để tất cả các thread hoàn tất::

   import threading, time

   def thread_task(name, n):
       for i in range(n):
           print(name, i)

   for i in range(10):
       T = threading.Thread(target=thread_task, args=(str(i), i))
       T.start()

   time.sleep(10)  # <---------------------------!

Nhưng hiện nay (trên nhiều nền tảng), các thread không chạy song song mà dường như chạy tuần tự, từng thread một! Lý do là bộ lập lịch thread của OS không khởi động thread mới cho đến khi thread trước đó bị chặn.

Một cách khắc phục đơn giản là thêm một khoảng sleep rất ngắn vào đầu hàm run::

   def thread_task(name, n):
       time.sleep(0.001)  # <--------------------!
       for i in range(n):
           print(name, i)

   for i in range(10):
       T = threading.Thread(target=thread_task, args=(str(i), i))
       T.start()

   time.sleep(10)

Thay vì cố đoán một giá trị delay phù hợp cho :func:`time.sleep`, tốt hơn là sử dụng một dạng cơ chế semaphore. Một ý tưởng là sử dụng
module :mod:`queue` để tạo một đối tượng queue, cho mỗi thread thêm một token vào queue khi hoàn tất, rồi để main thread đọc số token từ queue tương ứng với số thread.


Làm thế nào để phân chia công việc cho một nhóm worker thread?
--------------------------------------------------------------

Cách dễ nhất là sử dụng module :mod:`concurrent.futures`, đặc biệt là class :mod:`~concurrent.futures.ThreadPoolExecutor`.

Hoặc nếu muốn kiểm soát chi tiết thuật toán dispatch, bạn có thể tự viết logic theo cách thủ công. Sử dụng module :mod:`queue` để tạo một queue chứa danh sách job. Class :class:`~queue.Queue` duy trì một danh sách các object và có method ``.put(obj)`` để thêm các item vào queue, cùng method ``.get()`` để lấy chúng ra. Class này sẽ xử lý việc locking cần thiết để bảo đảm mỗi job được phân phối chính xác một lần.

Đây là một ví dụ đơn giản::

   import threading, queue, time

   # Luồng worker lấy các công việc từ hàng đợi. Khi hàng đợi trống, nó
   # giả định rằng sẽ không còn công việc nào nữa và thoát.
   # (Trên thực tế, các worker sẽ chạy cho đến khi bị kết thúc.)
   def worker():
       print('Running worker')
       time.sleep(0.1)
       while True:
           try:
               arg = q.get(block=False)
           except queue.Empty:
               print('Worker', threading.current_thread(), end=' ')
               print('queue empty')
               break
           else:
               print('Worker', threading.current_thread(), end=' ')
               print('running with argument', arg)
               time.sleep(0.5)

   # Tạo hàng đợi
   q = queue.Queue()

   # Khởi động một pool gồm 5 worker
   for i in range(5):
       t = threading.Thread(target=worker, name='worker %i' % (i+1))
       t.start()

   # Bắt đầu thêm công việc vào hàng đợi
   for i in range(50):
       q.put(i)

   # Cho các thread thời gian để chạy
   print('Main thread sleeping')
   time.sleep(5)

Khi chạy, đoạn mã này sẽ tạo ra đầu ra sau:

.. code-block:: none

   Running worker
   Running worker
   Running worker
   Running worker
   Running worker
   Main thread sleeping
   Worker <Thread(worker 1, started 130283832797456)> running with argument 0
   Worker <Thread(worker 2, started 130283824404752)> running with argument 1
   Worker <Thread(worker 3, started 130283816012048)> running with argument 2
   Worker <Thread(worker 4, started 130283807619344)> running with argument 3
   Worker <Thread(worker 5, started 130283799226640)> running with argument 4
   Worker <Thread(worker 1, started 130283832797456)> running with argument 5
   ...

Tham khảo tài liệu của module để biết thêm chi tiết; lớp :class:`~queue.Queue` cung cấp một giao diện đầy đủ tính năng.


Những kiểu thay đổi giá trị toàn cục nào là an toàn cho thread?
---------------------------------------------------------------

Một :term:`global interpreter lock` (GIL) được sử dụng nội bộ để đảm bảo rằng tại một thời điểm chỉ có một thread chạy trong Python VM. Nhìn chung, Python chỉ chuyển đổi giữa các thread giữa các lệnh bytecode; tần suất chuyển đổi có thể được thiết lập thông qua :func:`sys.setswitchinterval`. Do đó, mỗi lệnh bytecode và toàn bộ mã triển khai C được gọi từ mỗi lệnh đều mang tính nguyên tử dưới góc nhìn của một chương trình Python.

Về lý thuyết, điều này có nghĩa là muốn tính toán chính xác thì cần hiểu chính xác cách triển khai bytecode của PVM. Trên thực tế, điều này có nghĩa là các thao tác trên những biến dùng chung thuộc các kiểu dữ liệu tích hợp sẵn (int, list, dict, v.v.) mà "trông có vẻ nguyên tử" thực sự là nguyên tử.

Ví dụ, tất cả các thao tác sau đều mang tính nguyên tử (L, L1, L2 là các list, D, D1, D2 là các dict, x, y là các object, i, j là các int)::

   L.append(x)
   L1.extend(L2)
   x = L[i]
   x = L.pop()
   L1[i:j] = L2
   L.sort()
   x = y
   x.field = y
   D[x] = y
   D1.update(D2)
   D.keys()

Những thao tác này không phải::

   i = i+1
   L.append(L[-1])
   L[i] = L[j]
   D[x] = D[x] + 1

Các thao tác thay thế những đối tượng khác có thể gọi phương thức
:meth:`~object.__del__` của các đối tượng đó khi số lượng tham chiếu của chúng giảm xuống 0, và điều đó có thể ảnh hưởng đến mọi thứ. Điều này đặc biệt đúng với các thao tác cập nhật hàng loạt đối với dictionary và list. Khi không chắc chắn, hãy dùng mutex!


Có thể loại bỏ Global Interpreter Lock không?
---------------------------------------------

:term:`global interpreter lock` (GIL) thường được xem là một trở ngại đối với việc triển khai Python trên các máy chủ đa bộ xử lý cao cấp, vì một chương trình Python đa luồng thực tế chỉ sử dụng một CPU, do yêu cầu gần như toàn bộ mã Python chỉ có thể chạy khi đang giữ GIL.

Sau khi :pep:`703` được phê duyệt, công việc loại bỏ GIL khỏi quá trình triển khai CPython của Python hiện đang được tiến hành. Ban đầu, tính năng này sẽ được triển khai dưới dạng một cờ compiler tùy chọn khi xây dựng interpreter, vì vậy sẽ có các bản build riêng có và không có GIL. Về lâu dài, hy vọng là sẽ thống nhất thành một bản build duy nhất, sau khi hiểu đầy đủ những ảnh hưởng về hiệu năng của việc loại bỏ GIL. Python 3.13 có khả năng là bản phát hành đầu tiên chứa công việc này, mặc dù trong bản phát hành đó tính năng này có thể chưa hoạt động hoàn chỉnh.

Công việc hiện tại nhằm loại bỏ GIL dựa trên một `fork của Python 3.9 đã loại bỏ GIL <https://github.com/colesbury/nogil>`_ do Sam Gross thực hiện. Trước đó, vào thời Python 1.5, Greg Stein thực sự đã triển khai một bộ bản vá toàn diện (các bản vá "free threading") loại bỏ GIL và thay thế nó bằng cơ chế khóa chi tiết. Adam Olsen cũng thực hiện một thử nghiệm tương tự trong dự án `python-safethread <https://code.google.com/archive/p/python-safethread>`_ của mình. Đáng tiếc là cả hai thử nghiệm trước đó đều cho thấy hiệu năng đơn luồng giảm mạnh (chậm hơn ít nhất 30%), do cần quá nhiều cơ chế khóa chi tiết để bù đắp cho việc loại bỏ GIL. Fork Python 3.9 là nỗ lực đầu tiên nhằm loại bỏ GIL với mức ảnh hưởng đến hiệu năng có thể chấp nhận được.

Việc GIL tồn tại trong các bản phát hành Python hiện tại không có nghĩa là bạn không thể tận dụng tốt Python trên các máy có nhiều CPU! Bạn chỉ cần sáng tạo trong việc chia công việc giữa nhiều *tiến trình* thay vì nhiều *luồng*.  The
:class:`~concurrent.futures.ProcessPoolExecutor` class trong phiên bản mới
:mod:`concurrent.futures` module cung cấp một cách dễ dàng để thực hiện việc này; còn
:mod:`multiprocessing` module cung cấp API cấp thấp hơn trong trường hợp bạn muốn kiểm soát nhiều hơn việc phân phối tác vụ.

Việc sử dụng hợp lý các phần mở rộng C cũng sẽ hữu ích; nếu bạn dùng một phần mở rộng C để thực hiện một tác vụ tốn nhiều thời gian, phần mở rộng đó có thể giải phóng GIL trong khi luồng thực thi đang chạy mã C, cho phép các luồng khác thực hiện một phần công việc. Một số module trong standard library như :mod:`zlib` và :mod:`hashlib` đã làm như vậy.

Một cách tiếp cận khác để giảm ảnh hưởng của GIL là biến GIL thành một khóa theo trạng thái interpreter thay vì thực sự mang tính toàn cục. Điều này :ref:`được triển khai lần đầu trong Python 3.12 <whatsnew312-pep684>` và có sẵn trong C API. Dự kiến sẽ có giao diện Python cho tính năng này trong Python 3.13. Hạn chế chính của tính năng này ở thời điểm hiện tại có thể là các module phần mở rộng của bên thứ ba, vì chúng phải được viết có tính đến nhiều interpreter thì mới có thể sử dụng được; do đó, nhiều module phần mở rộng cũ sẽ không thể sử dụng.


Đầu vào và Đầu ra
=================

Làm thế nào để xóa một tệp? (Và các câu hỏi khác về tệp...)
-----------------------------------------------------------

Sử dụng ``os.remove(filename)`` hoặc ``os.unlink(filename)``; để xem tài liệu, hãy tham khảo module :mod:`os`. Hai hàm này giống hệt nhau; :func:`~os.unlink` đơn giản là tên của lệnh gọi hệ thống Unix cho hàm này.

Để xóa một thư mục, hãy sử dụng :func:`os.rmdir`; sử dụng :func:`os.mkdir` để tạo thư mục. ``os.makedirs(path)`` sẽ tạo mọi thư mục trung gian trong ``path`` chưa tồn tại. ``os.removedirs(path)`` sẽ xóa các thư mục trung gian miễn là chúng rỗng; nếu bạn muốn xóa toàn bộ cây thư mục cùng nội dung của nó, hãy sử dụng :func:`shutil.rmtree`.

Để đổi tên một tệp, hãy sử dụng ``os.rename(old_path, new_path)``.

Để cắt ngắn một tệp, hãy mở tệp bằng ``f = open(filename, "rb+")`` và sử dụng ``f.truncate(offset)``; offset mặc định là vị trí seek hiện tại. Ngoài ra còn có ``os.ftruncate(fd, offset)`` dành cho các tệp được mở bằng :func:`os.open`, trong đó *fd* là file descriptor (một số nguyên nhỏ).

Module :mod:`shutil` cũng chứa một số hàm để thao tác với tệp, bao gồm :func:`~shutil.copyfile`, :func:`~shutil.copytree`, và
:func:`~shutil.rmtree`.


Làm thế nào để sao chép một tệp?
--------------------------------

Mô-đun :mod:`shutil` chứa một hàm :func:`~shutil.copyfile`. Lưu ý rằng trên các volume NTFS của Windows, hàm này không sao chép `alternate data streams <https://en.wikipedia.org/wiki/NTFS#Alternate_data_stream_(ADS)>`_ và cũng không sao chép `resource forks <https://en.wikipedia.org/wiki/Resource_fork>`__ trên các volume HFS+ của macOS, mặc dù hiện nay cả hai đều hiếm khi được sử dụng. Hàm này cũng không sao chép quyền truy cập và siêu dữ liệu của tệp, mặc dù việc sử dụng
:func:`shutil.copy2` thay vào đó sẽ bảo toàn phần lớn (dù không phải tất cả) các thuộc tính này.


Làm thế nào để đọc (hoặc ghi) dữ liệu nhị phân?
-----------------------------------------------

Để đọc hoặc ghi các định dạng dữ liệu nhị phân phức tạp, tốt nhất nên sử dụng mô-đun :mod:`struct`. Mô-đun này cho phép bạn nhận một chuỗi chứa dữ liệu nhị phân (thường là các số) và chuyển đổi chuỗi đó thành các đối tượng Python, cũng như thực hiện chuyển đổi ngược lại.

Ví dụ, đoạn mã sau đọc hai số nguyên 2 byte và một số nguyên 4 byte từ một tệp ở định dạng big-endian::

   import struct

   with open(filename, "rb") as f:
       s = f.read(8)
       x, y, z = struct.unpack(">hhl", s)

Ký tự '>' trong chuỗi định dạng buộc dữ liệu sử dụng thứ tự big-endian; chữ 'h' đọc một "short integer" (2 byte), còn 'l' đọc một "long integer" (4 byte) từ chuỗi.

Đối với dữ liệu có cấu trúc đều đặn hơn (ví dụ: một danh sách đồng nhất các số nguyên hoặc số thực), bạn cũng có thể sử dụng mô-đun :mod:`array`.

.. note::

   Để đọc và ghi dữ liệu nhị phân, bắt buộc phải mở tệp ở chế độ nhị phân (ở đây là truyền ``"rb"`` cho :func:`open`). Nếu thay vào đó bạn sử dụng ``"r"`` (mặc định), tệp sẽ được mở ở chế độ văn bản và ``f.read()`` sẽ trả về các đối tượng :class:`str` thay vì
   các đối tượng :class:`bytes`.


Tại sao tôi không thể sử dụng os.read() trên một pipe được tạo bằng os.popen()?
-------------------------------------------------------------------------------

:func:`os.read` là một hàm cấp thấp nhận một file descriptor, tức một số nguyên nhỏ đại diện cho tệp đã mở. :func:`os.popen` tạo một đối tượng tệp cấp cao, cùng kiểu với đối tượng được trả về bởi hàm tích hợp sẵn :func:`open`. Vì vậy, để đọc *n* byte từ pipe *p* được tạo bằng :func:`os.popen`, bạn cần sử dụng ``p.read(n)``.


Làm thế nào để truy cập cổng nối tiếp (RS232)?
----------------------------------------------

Đối với Win32, OSX, Linux, BSD, Jython, IronPython:

   :pypi:`pyserial`

Đối với Unix, hãy xem bài đăng Usenet của Mitch Chapman:

   https://groups.google.com/groups?selm=34A04430.CF9@ohioee.com


Tại sao việc đóng sys.stdout (stdin, stderr) lại không thực sự đóng nó?
-----------------------------------------------------------------------

Các :term:`đối tượng file <file object>` của Python là một lớp trừu tượng cấp cao trên các file descriptor C cấp thấp.

Đối với hầu hết các đối tượng file bạn tạo trong Python thông qua hàm dựng sẵn :func:`open`, ``f.close()`` đánh dấu đối tượng file Python là đã đóng theo quan điểm của Python, đồng thời sắp xếp để đóng file descriptor C bên dưới. Điều này cũng tự động xảy ra trong destructor của ``f``, khi ``f`` trở thành rác.

Nhưng stdin, stdout và stderr được Python xử lý đặc biệt, vì C cũng dành cho chúng một trạng thái đặc biệt. Việc chạy ``sys.stdout.close()`` đánh dấu đối tượng file ở cấp Python là đã đóng, nhưng *không* đóng file descriptor C liên kết.

Để đóng file descriptor C bên dưới của một trong ba đối tượng này, trước tiên bạn nên chắc chắn rằng đó thực sự là điều mình muốn làm (ví dụ: bạn có thể gây nhầm lẫn cho các extension module đang cố gắng thực hiện I/O). Nếu đúng là vậy, hãy sử dụng :func:`os.close`::

   os.close(stdin.fileno())
   os.close(stdout.fileno())
   os.close(stderr.fileno())

Hoặc bạn có thể sử dụng các hằng số số 0, 1 và 2, lần lượt tương ứng.


Lập trình mạng/Internet
=======================

Có những công cụ WWW nào dành cho Python?
-----------------------------------------

Xem các chương có tiêu đề :ref:`internet` và :ref:`netdata` trong Sổ tay Tham khảo Thư viện. Python có nhiều mô-đun giúp bạn xây dựng các hệ thống web phía máy chủ và phía máy khách.

.. XXX check if wiki page is still up to date

Paul Boddie duy trì bản tóm tắt các framework hiện có tại https://wiki.python.org/moin/WebProgramming\ .


Tôi nên sử dụng mô-đun nào để hỗ trợ việc tạo HTML?
---------------------------------------------------

.. XXX add modern template languages

Bạn có thể tìm thấy một tập hợp các liên kết hữu ích trên `trang wiki Lập trình Web <https://wiki.python.org/moin/WebProgramming>`_.


Làm thế nào để gửi thư từ một tập lệnh Python?
----------------------------------------------

Hãy sử dụng mô-đun thư viện chuẩn :mod:`smtplib`.

Đây là một trình gửi thư tương tác rất đơn giản sử dụng nó. Phương thức này sẽ hoạt động trên mọi máy chủ hỗ trợ trình lắng nghe SMTP.::

   import sys, smtplib

   fromaddr = input("From: ")
   toaddrs  = input("To: ").split(',')
   print("Enter message, end with ^D:")
   msg = ''
   while True:
       line = sys.stdin.readline()
       if not line:
           break
       msg += line

   # Gửi thư thực tế
   server = smtplib.SMTP('localhost')
   server.sendmail(fromaddr, toaddrs, msg)
   server.quit()

Một lựa chọn thay thế chỉ dành cho Unix là sử dụng sendmail. Vị trí của chương trình sendmail thay đổi tùy hệ thống; đôi khi là ``/usr/lib/sendmail``, đôi khi là ``/usr/sbin/sendmail``. Trang hướng dẫn sử dụng sendmail sẽ giúp bạn. Dưới đây là một đoạn mã mẫu::

   import os

   SENDMAIL = "/usr/sbin/sendmail"  # vị trí sendmail
   p = os.popen("%s -t -i" % SENDMAIL, "w")
   p.write("To: receiver@example.com\n")
   p.write("Subject: test\n")
   p.write("\n")  # dòng trống phân tách phần header khỏi phần nội dung
   p.write("Some text\n")
   p.write("some more text\n")
   sts = p.close()
   if sts != 0:
       print("Sendmail exit status", sts)


Làm thế nào để tránh bị chặn trong phương thức connect() của socket?
--------------------------------------------------------------------

Mô-đun :mod:`select` thường được dùng để hỗ trợ I/O bất đồng bộ trên các socket.

Để tránh việc kết nối TCP bị blocking, bạn có thể đặt socket ở chế độ non-blocking. Sau đó, khi thực hiện :meth:`~socket.socket.connect`, bạn sẽ либо kết nối ngay lập tức (không có khả năng cao) hoặc nhận được một exception chứa số lỗi dưới dạng ``.errno``. ``errno.EINPROGRESS`` cho biết kết nối đang được tiến hành nhưng chưa hoàn tất. Các hệ điều hành khác nhau sẽ trả về các giá trị khác nhau, vì vậy bạn sẽ phải kiểm tra giá trị được trả về trên hệ thống của mình.

Bạn có thể sử dụng phương thức :meth:`~socket.socket.connect_ex` để tránh tạo exception. Phương thức này chỉ trả về giá trị errno. Để polling, bạn có thể gọi lại :meth:`~socket.socket.connect_ex` sau đó -- ``0`` hoặc ``errno.EISCONN`` cho biết bạn đã kết nối -- hoặc truyền socket này cho :meth:`select.select` để kiểm tra xem nó có thể ghi hay không.

.. note::
   Module :mod:`asyncio` cung cấp một thư viện asynchronous tổng quát, đơn luồng và concurrent, có thể được dùng để viết mã mạng non-blocking. Thư viện bên thứ ba `Twisted <https://twisted.org/>`_ là một lựa chọn thay thế phổ biến và giàu tính năng.


Cơ sở dữ liệu
=============

Có interface nào cho các package cơ sở dữ liệu trong Python không?
------------------------------------------------------------------

Có.

Các interface cho những hash dựa trên đĩa như :mod:`DBM <dbm.ndbm>` và :mod:`GDBM <dbm.gnu>` cũng được tích hợp trong Python tiêu chuẩn. Ngoài ra còn có
mô-đun :mod:`sqlite3`, cung cấp một cơ sở dữ liệu quan hệ nhẹ dựa trên đĩa.

Có hỗ trợ cho hầu hết các cơ sở dữ liệu quan hệ. Xem trang wiki `DatabaseProgramming <https://wiki.python.org/moin/DatabaseProgramming>`_ để biết chi tiết.


Làm thế nào để triển khai các đối tượng persistent trong Python?
----------------------------------------------------------------

Mô-đun thư viện :mod:`pickle` giải quyết vấn đề này theo một cách rất tổng quát (mặc dù bạn vẫn không thể lưu trữ những thứ như tệp đang mở, socket hoặc cửa sổ), và
Mô-đun thư viện :mod:`shelve` sử dụng pickle và (g)dbm để tạo các ánh xạ persistent chứa các đối tượng Python tùy ý.


Toán học và Tính toán số
========================

Làm thế nào để tạo các số ngẫu nhiên trong Python?
--------------------------------------------------

Mô-đun chuẩn :mod:`random` triển khai một bộ sinh số ngẫu nhiên. Cách sử dụng rất đơn giản::

   import random
   random.random()

Lệnh này trả về một số dấu phẩy động ngẫu nhiên trong khoảng [0, 1).

Mô-đun này cũng có nhiều bộ sinh chuyên biệt khác, chẳng hạn như:

* ``randrange(a, b)`` chọn một số nguyên trong khoảng [a, b).
* ``uniform(a, b)`` chọn một số dấu phẩy động trong khoảng [a, b).
* ``normalvariate(mean, sdev)`` lấy mẫu phân phối chuẩn (Gaussian).

Một số hàm cấp cao hơn hoạt động trực tiếp trên các sequence, chẳng hạn như:

* ``choice(S)`` chọn một phần tử ngẫu nhiên từ một dãy cho trước.
* ``shuffle(L)`` xáo trộn một danh sách ngay tại chỗ, tức là hoán vị danh sách đó một cách ngẫu nhiên.

Ngoài ra, còn có một class ``Random`` mà bạn có thể khởi tạo để tạo nhiều bộ tạo số ngẫu nhiên độc lập.

.. _`Python Package Index`: https://pypi.org
.. _`Google`: https://www.google.com
.. _`epydoc`: https://epydoc.sourceforge.net/
.. _`Sphinx`: https://www.sphinx-doc.org
.. _`fork of Python 3.9 with the GIL removed`: https://github.com/colesbury/nogil
.. _`python-safethread`: https://code.google.com/archive/p/python-safethread
.. _`alternate data streams`: https://en.wikipedia.org/wiki/NTFS#Alternate_data_stream_(ADS)
.. _`Web Programming wiki page`: https://wiki.python.org/moin/WebProgramming
.. _`Twisted`: https://twisted.org/
.. _`DatabaseProgramming wiki page`: https://wiki.python.org/moin/DatabaseProgramming
