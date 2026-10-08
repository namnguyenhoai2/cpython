:mod:`!timeit` --- Đo thời gian thực thi các đoạn mã nhỏ
========================================================

.. module:: timeit
   :synopsis: Đo thời gian thực thi các đoạn mã nhỏ.

**Mã nguồn:** :source:`Lib/timeit.py`

.. index::
   single: Benchmarking
   single: Performance

--------------

Mô-đun này cung cấp một cách đơn giản để đo thời gian thực thi các đoạn mã Python nhỏ. Mô-đun có cả :ref:`timeit-command-line-interface` và một :ref:`callable <python-interface>`. Mô-đun tránh được một số sai lầm phổ biến khi đo thời gian thực thi. Xem thêm phần giới thiệu của Tim Peters trong chương "Algorithms" của ấn bản thứ hai của *Python Cookbook*, do O'Reilly xuất bản.


Các ví dụ cơ bản
----------------

Ví dụ sau đây cho thấy cách sử dụng :ref:`timeit-command-line-interface` để so sánh ba biểu thức khác nhau:

.. code-block:: shell-session

   $ python -m timeit "'-'.join(str(n) for n in range(100))"
   10000 loops, best of 5: 30.2 usec per loop
   $ python -m timeit "'-'.join([str(n) for n in range(100)])"
   10000 loops, best of 5: 27.5 usec per loop
   $ python -m timeit "'-'.join(map(str, range(100)))"
   10000 loops, best of 5: 23.2 usec per loop

Bạn có thể thực hiện việc này từ :ref:`python-interface` bằng::

   >>> import timeit
   >>> timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
   0.3018611848820001
   >>> timeit.timeit('"-".join([str(n) for n in range(100)])', number=10000)
   0.2727368790656328
   >>> timeit.timeit('"-".join(map(str, range(100)))', number=10000)
   0.23702679807320237

Một callable cũng có thể được truyền từ :ref:`python-interface`::

   >>> timeit.timeit(lambda: "-".join(map(str, range(100))), number=10000)
   0.19665591977536678

Tuy nhiên, lưu ý rằng :func:`.timeit` sẽ tự động xác định số lần lặp chỉ khi sử dụng giao diện dòng lệnh.  Trong
:ref:`timeit-examples` bạn có thể tìm thấy các ví dụ nâng cao hơn.


.. _python-interface:

Giao diện Python
----------------

Mô-đun này định nghĩa ba hàm tiện ích và một lớp công khai:


.. function:: timeit(stmt='pass', setup='pass', timer=<default timer>, number=1000000, globals=None)

   Tạo một thực thể :class:`Timer` với câu lệnh, mã *setup* và hàm *timer* đã cho, rồi chạy phương thức :meth:`.timeit` của nó với *number* lần thực thi. Đối số tùy chọn *globals* chỉ định một namespace để thực thi mã.

   .. versionchanged:: 3.5
      Tham số tùy chọn *globals* đã được thêm vào.


.. function:: repeat(stmt='pass', setup='pass', timer=<default timer>, repeat=5, number=1000000, globals=None)

   Tạo một thực thể :class:`Timer` với câu lệnh đã cho, mã *setup* và hàm *timer*, rồi chạy phương thức :meth:`.repeat` của nó với số lần *repeat* và số lần thực thi *number* đã cho. Đối số tùy chọn *globals* chỉ định một namespace để thực thi mã.

   .. versionchanged:: 3.5
      Tham số tùy chọn *globals* đã được thêm vào.

   .. versionchanged:: 3.7
      Giá trị mặc định của *repeat* đã thay đổi từ 3 thành 5.


.. function:: default_timer()

   Timer mặc định, luôn là time.perf_counter(), trả về số giây kiểu float. Một lựa chọn khác, time.perf_counter_ns, trả về số nano giây kiểu integer.

   .. versionchanged:: 3.3
      :func:`time.perf_counter` is now the default timer.


.. class:: Timer(stmt='pass', setup='pass', timer=<timer function>, globals=None)

   Lớp dùng để đo tốc độ thực thi của các đoạn mã nhỏ.

   Hàm khởi tạo nhận một câu lệnh cần đo thời gian, một câu lệnh bổ sung dùng để thiết lập và một hàm timer. Cả hai câu lệnh đều mặc định là ``'pass'``; hàm timer phụ thuộc vào nền tảng (xem doc string của module). *stmt* và *setup* cũng có thể chứa nhiều câu lệnh được phân tách bằng ``;`` hoặc các dòng mới, miễn là chúng không chứa các string literal nhiều dòng. Theo mặc định, câu lệnh sẽ được thực thi trong namespace của timeit; có thể kiểm soát hành vi này bằng cách truyền một namespace cho *globals*.

   Để đo thời gian thực thi của câu lệnh đầu tiên, hãy sử dụng phương thức :meth:`.timeit`. Phương thức :meth:`.repeat` và :meth:`.autorange` là các phương thức tiện ích để gọi :meth:`.timeit` nhiều lần.

   Thời gian thực thi của *setup* không được tính vào toàn bộ lần chạy thực thi được đo thời gian.

   Các tham số *stmt* và *setup* cũng có thể nhận các đối tượng có thể được gọi mà không cần đối số. Khi đó, các lệnh gọi đến chúng sẽ được nhúng vào một hàm timer, rồi hàm này sẽ được thực thi bởi :meth:`.timeit`. Lưu ý rằng trong trường hợp này, overhead đo thời gian sẽ lớn hơn một chút do có thêm các lệnh gọi hàm.

   .. versionchanged:: 3.5
      Tham số tùy chọn *globals* đã được thêm vào.

   .. method:: Timer.timeit(number=1000000)

      Đo thời gian thực thi *number* lần của câu lệnh chính. Thao tác này thực thi câu lệnh setup một lần, sau đó trả về thời gian cần để thực thi câu lệnh chính một số lần. Timer mặc định trả về số giây dưới dạng số thực. Đối số là số lần lặp, mặc định là một triệu. Câu lệnh chính, câu lệnh setup và hàm timer cần sử dụng được truyền cho constructor.

      .. note::

         Theo mặc định, :meth:`.timeit` tạm thời tắt :term:`garbage collection` trong khi đo thời gian. Ưu điểm của cách tiếp cận này là giúp các phép đo thời gian độc lập có tính so sánh cao hơn. Nhược điểm là GC có thể là một thành phần quan trọng trong hiệu năng của hàm được đo. Nếu vậy, có thể bật lại GC làm câu lệnh đầu tiên trong chuỗi *setup*. Ví dụ::

            timeit.Timer('for i in range(10): oct(i)', 'gc.enable()').timeit()


   .. method:: Timer.autorange(callback=None)

      Tự động xác định số lần cần gọi :meth:`.timeit`.

      Tự động gọi :meth:`.timeit` nhiều lần để tổng thời gian >= 0.2 giây, rồi trả về (số vòng lặp, thời gian cần cho số vòng lặp đó) cuối cùng. Hàm này gọi
      :meth:`.timeit` với các số tăng dần theo dãy 1, 2, 5, 10, 20, 50, ... cho đến khi thời gian thực thi ít nhất là 0.2 giây.

      Nếu *callback* được cung cấp và không phải là ``None``, hàm này sẽ được gọi sau mỗi lần chạy thử với hai đối số: ``callback(number, time_taken)``.

      .. versionadded:: 3.6


   .. method:: Timer.repeat(repeat=5, number=1000000)

      Gọi :meth:`.timeit` vài lần.

      Đây là một hàm tiện ích gọi :meth:`.timeit` lặp đi lặp lại và trả về một danh sách kết quả. Đối số đầu tiên chỉ định số lần gọi :meth:`.timeit`. Đối số thứ hai chỉ định đối số *number* cho :meth:`.timeit`.

      .. note::

         Việc tính giá trị trung bình và độ lệch chuẩn từ vector kết quả rồi báo cáo các giá trị này có vẻ hấp dẫn. Tuy nhiên, cách này không hữu ích lắm. Trong trường hợp điển hình, giá trị thấp nhất cung cấp một cận dưới cho tốc độ mà máy của bạn có thể chạy đoạn mã đã cho; các giá trị cao hơn trong vector kết quả thường không phải do tốc độ của Python biến thiên, mà do các tiến trình khác can thiệp vào độ chính xác đo thời gian của bạn. Vì vậy, :func:`min` của kết quả có lẽ là con số duy nhất bạn cần quan tâm. Sau đó, bạn nên xem toàn bộ vector và vận dụng suy luận thông thường thay vì thống kê.

      .. versionchanged:: 3.7
         Giá trị mặc định của *repeat* đã thay đổi từ 3 thành 5.


   .. method:: Timer.print_exc(file=None)

      Hàm trợ giúp để in traceback từ đoạn mã được đo thời gian.

      Cách sử dụng điển hình::

         t = Timer(...)       # bên ngoài try/except
         try:
             t.timeit(...)    # hoặc t.repeat(...)
         except Exception:
             t.print_exc()

      Ưu điểm so với traceback tiêu chuẩn là các dòng mã nguồn trong template đã biên dịch sẽ được hiển thị. Đối số tùy chọn *file* xác định nơi gửi traceback; mặc định là :data:`sys.stderr`.


.. _timeit-command-line-interface:

Giao diện dòng lệnh
-------------------

Khi được gọi dưới dạng một chương trình từ dòng lệnh, sử dụng dạng sau::

   python -m timeit [-n N] [-r N] [-u U] [-s S] [-p] [-v] [-h] [statement ...]

Các tùy chọn sau được hỗ trợ:

.. program:: timeit

.. option:: -n N, --number=N

   số lần thực thi 'statement'

.. option:: -r N, --repeat=N

   số lần lặp lại timer (mặc định là 5)

.. option:: -s S, --setup=S

   statement sẽ được thực thi một lần ban đầu (mặc định là ``pass``)

.. option:: -p, --process

   đo thời gian process, không phải thời gian thực, bằng :func:`time.process_time` thay vì :func:`time.perf_counter`, là giá trị mặc định

   .. versionadded:: 3.3

.. option:: -u, --unit=U

   chỉ định đơn vị thời gian cho đầu ra của timer; có thể chọn ``nsec``, ``usec``, ``msec`` hoặc ``sec``

   .. versionadded:: 3.5

.. option:: -v, --verbose

   in kết quả đo thời gian thô; lặp lại để có độ chính xác cao hơn

.. option:: -h, --help

   in thông báo hướng dẫn sử dụng ngắn gọn rồi thoát

Có thể cung cấp một câu lệnh nhiều dòng bằng cách chỉ định mỗi dòng như một đối số câu lệnh riêng; có thể thụt lề các dòng bằng cách đặt một đối số trong dấu ngoặc kép và sử dụng các khoảng trắng ở đầu. Nhiều tùy chọn :option:`-s` được xử lý tương tự.

Nếu không cung cấp :option:`-n`, chương trình sẽ tính số vòng lặp phù hợp bằng cách thử các số tăng dần trong dãy 1, 2, 5, 10, 20, 50, ... cho đến khi tổng thời gian đạt ít nhất 0,2 giây.

Các phép đo :func:`default_timer` có thể bị ảnh hưởng bởi những chương trình khác đang chạy trên cùng máy, vì vậy khi cần đo thời gian chính xác, cách tốt nhất là lặp lại phép đo vài lần và sử dụng thời gian tốt nhất. Tùy chọn :option:`-r` phù hợp cho việc này; mặc định 5 lần lặp có lẽ là đủ trong hầu hết trường hợp. Bạn có thể sử dụng :func:`time.process_time` để đo thời gian CPU.

.. note::

   Việc thực thi một câu lệnh pass có một phần overhead cơ sở nhất định. Đoạn mã này không cố che giấu phần overhead đó, nhưng bạn nên lưu ý đến nó. Có thể đo overhead cơ sở bằng cách gọi chương trình mà không có đối số; giá trị này có thể khác nhau giữa các phiên bản Python.


.. _timeit-examples:

Ví dụ
-----

Bạn có thể cung cấp một câu lệnh setup chỉ được thực thi một lần ở đầu:

.. code-block:: shell-session

   $ python -m timeit -s "text = 'sample string'; char = 'g'" "char in text"
   5000000 loops, best of 5: 0.0877 usec per loop
   $ python -m timeit -s "text = 'sample string'; char = 'g'" "text.find(char)"
   1000000 loops, best of 5: 0.342 usec per loop

Trong kết quả đầu ra có ba trường. Trường thứ nhất là số vòng lặp, cho biết phần thân câu lệnh được chạy bao nhiêu lần trong mỗi lần lặp đo thời gian. Trường thứ hai là số lần lặp ("tốt nhất trong 5 lần"), cho biết vòng lặp đo thời gian được lặp lại bao nhiêu lần. Cuối cùng là thời gian trung bình mà phần thân câu lệnh mất trong lần lặp tốt nhất của vòng lặp đo thời gian. Nói cách khác, đó là thời gian của lần lặp nhanh nhất chia cho số vòng lặp.

::

   >>> import timeit
   >>> timeit.timeit('char in text', setup='text = "sample string"; char = "g"')
   0.41440500499993504
   >>> timeit.timeit('text.find(char)', setup='text = "sample string"; char = "g"')
   1.7246671520006203

Bạn cũng có thể thực hiện tương tự bằng cách sử dụng lớp :class:`Timer` và các phương thức của lớp đó::

   >>> import timeit
   >>> t = timeit.Timer('char in text', setup='text = "sample string"; char = "g"')
   >>> t.timeit()
   0.3955516149999312
   >>> t.repeat()
   [0.40183617287970225, 0.37027556854118704, 0.38344867356679524, 0.3712595970846668, 0.37866875250654886]


Các ví dụ sau đây cho thấy cách đo thời gian của những biểu thức chứa nhiều dòng. Ở đây, chúng ta so sánh chi phí của việc sử dụng :func:`hasattr` với :keyword:`try`/:keyword:`except` để kiểm tra các thuộc tính đối tượng bị thiếu và hiện có:

.. code-block:: shell-session

   $ python -m timeit "try:" "  str.__bool__" "except AttributeError:" "  pass"
   20000 loops, best of 5: 15.7 usec per loop
   $ python -m timeit "if hasattr(str, '__bool__'): pass"
   50000 loops, best of 5: 4.26 usec per loop

   $ python -m timeit "try:" "  int.__bool__" "except AttributeError:" "  pass"
   200000 loops, best of 5: 1.43 usec per loop
   $ python -m timeit "if hasattr(int, '__bool__'): pass"
   100000 loops, best of 5: 2.23 usec per loop

::

   >>> import timeit
   >>> # thuộc tính bị thiếu
   >>> s = """\
   ... try:
   ...     str.__bool__
   ... except AttributeError:
   ...     pass
   ... """
   >>> timeit.timeit(stmt=s, number=100000)
   0.9138244460009446
   >>> s = "if hasattr(str, '__bool__'): pass"
   >>> timeit.timeit(stmt=s, number=100000)
   0.5829014980008651
   >>>
   >>> # thuộc tính hiện có
   >>> s = """\
   ... try:
   ...     int.__bool__
   ... except AttributeError:
   ...     pass
   ... """
   >>> timeit.timeit(stmt=s, number=100000)
   0.04215312199994514
   >>> s = "if hasattr(int, '__bool__'): pass"
   >>> timeit.timeit(stmt=s, number=100000)
   0.08588060699912603


Để cấp cho module :mod:`!timeit` quyền truy cập vào các hàm bạn định nghĩa, bạn có thể truyền một tham số *setup* chứa một câu lệnh import::

   def test():
       """Stupid test function"""
       L = [i for i in range(100)]

   if __name__ == '__main__':
       import timeit
       print(timeit.timeit("test()", setup="from __main__ import test"))

Một tùy chọn khác là truyền :func:`globals` vào tham số *globals*, khiến mã được thực thi trong namespace toàn cục hiện tại của bạn. Cách này có thể thuận tiện hơn so với việc chỉ định từng import riêng lẻ::

   def f(x):
       return x**2
   def g(x):
       return x**4
   def h(x):
       return x**8

   import timeit
   print(timeit.timeit('[func(42) for func in (f,g,h)]', globals=globals()))
