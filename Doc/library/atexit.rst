:mod:`!atexit` --- Trình xử lý khi thoát
========================================

.. module:: atexit
   :synopsis: Đăng ký và thực thi các hàm dọn dẹp.

.. moduleauthor:: Skip Montanaro <skip.montanaro@gmail.com>
.. sectionauthor:: Skip Montanaro <skip.montanaro@gmail.com>

--------------

Mô-đun :mod:`!atexit` định nghĩa các hàm để đăng ký và hủy đăng ký
:dfn:`trình xử lý khi thoát`: các hàm được tự động thực thi "khi thoát", tức là khi chương trình kết thúc bình thường (ví dụ: nếu :func:`sys.exit` được gọi hoặc quá trình thực thi của mô-đun chính hoàn tất) hoặc nói chung là khi :term:`interpreter shutdown`.

Khi thoát, tất cả trình xử lý khi thoát đã đăng ký được gọi theo thứ tự *ngược lại* với thứ tự chúng được đăng ký. Nếu bạn đăng ký ``A``, ``B`` và ``C``, khi interpreter tắt, chúng sẽ được chạy theo thứ tự ``C``, ``B``, ``A``. Giả định ở đây là các mô-đun cấp thấp thường được import trước các mô-đun cấp cao hơn và do đó phải được dọn dẹp sau.

Nếu một ngoại lệ được phát sinh trong quá trình thực thi trình xử lý khi thoát, một traceback sẽ được in (trừ khi :exc:`SystemExit` được phát sinh) và thông tin ngoại lệ sẽ được lưu lại. Sau khi tất cả trình xử lý khi thoát đã có cơ hội chạy, ngoại lệ cuối cùng được phát sinh sẽ được phát sinh lại.

Trong các chương trình sử dụng nhiều interpreter, mỗi interpreter có ngăn xếp trình xử lý khi thoát riêng, được thực thi khi interpreter tắt (ví dụ: với :meth:`concurrent.interpreters.Interpreter.close` hoặc C API :c:func:`Py_EndInterpreter`). Các hàm đăng ký trong mô-đun này chỉ ảnh hưởng đến interpreter mà chúng được gọi từ đó.

**Lưu ý:** Các trình xử lý khi thoát không được gọi khi chương trình bị kết thúc bởi một signal không được Python xử lý, khi phát hiện lỗi nghiêm trọng nội bộ của Python hoặc khi gọi :func:`os._exit`.

**Lưu ý:** Hành vi khi đăng ký hoặc hủy đăng ký các hàm từ bên trong một hàm dọn dẹp là không xác định.

.. warning::
   Khi viết các trình xử lý khi thoát, đặc biệt là trong các phần mở rộng C API, hãy lưu ý rằng những trình xử lý khi thoát khác vẫn có thể chạy mã Python tùy ý sau khi bạn dọn dẹp. Mã đó phải thành công hoặc thất bại với một exception, thay vì làm chương trình bị crash.

.. versionchanged:: 3.12
   Việc cố gắng khởi động một thread mới hoặc :func:`os.fork` một process mới trong trình xử lý khi thoát hiện sẽ dẫn đến :exc:`RuntimeError`. Trước đây, điều này có thể gây ra race condition giữa việc thread runtime Python chính giải phóng các thread state trong khi các routine :mod:`threading` nội bộ hoặc process mới cố gắng sử dụng state đó, dẫn đến crash thay vì tắt máy sạch sẽ.

.. versionchanged:: 3.7
   Khi được sử dụng với subinterpreter, các hàm đã đăng ký chỉ thuộc về interpreter nơi chúng được đăng ký.

.. function:: register(func, *args, **kwargs)

   Đăng ký *func* làm trình xử lý khi thoát. Mọi đối số tùy chọn cần được truyền cho *func* phải được truyền dưới dạng đối số cho :func:`register`. Có thể đăng ký cùng một hàm và các đối số nhiều lần.

   Hàm này trả về *func*, nhờ đó có thể sử dụng nó làm decorator.

.. function:: unregister(func)

   Xóa *func* khỏi danh sách các exit handler.
   :func:`unregister` không làm gì một cách im lặng nếu *func* chưa được đăng ký trước đó. Nếu *func* đã được đăng ký nhiều lần, mọi lần xuất hiện của hàm đó trong ngăn xếp lời gọi :mod:`!atexit` sẽ bị xóa. Các phép so sánh bằng (``==``) được sử dụng nội bộ trong quá trình hủy đăng ký, vì vậy các tham chiếu hàm không cần có cùng identity.


.. seealso::

   Mô-đun :mod:`readline`
      Ví dụ hữu ích về :mod:`!atexit` để đọc và ghi các tệp lịch sử :mod:`readline`.


.. _atexit-example:

Ví dụ :mod:`!atexit`
--------------------

Ví dụ đơn giản sau đây minh họa cách một mô-đun có thể khởi tạo bộ đếm từ một tệp khi được import và tự động lưu giá trị đã cập nhật của bộ đếm khi chương trình kết thúc mà không cần ứng dụng gọi tường minh vào mô-đun này lúc kết thúc.::

   try:
       with open('counterfile') as infile:
           _count = int(infile.read())
   except FileNotFoundError:
       _count = 0

   def incrcounter(n):
       global _count
       _count = _count + n

   def savecounter():
       with open('counterfile', 'w') as outfile:
           outfile.write('%d' % _count)

   import atexit

   atexit.register(savecounter)

Các đối số vị trí và đối số từ khóa cũng có thể được truyền cho :func:`register` để truyền tiếp cho hàm đã đăng ký khi hàm đó được gọi::

   def goodbye(name, adjective):
       print('Goodbye %s, it was %s to meet you.' % (name, adjective))

   import atexit

   atexit.register(goodbye, 'Donny', 'nice')
   # hoặc:
   atexit.register(goodbye, adjective='nice', name='Donny')

Sử dụng như một :term:`decorator`::

   import atexit

   @atexit.register
   def goodbye():
       print('You are now leaving the Python sector.')

Điều này chỉ hoạt động với các hàm có thể được gọi mà không cần đối số.
