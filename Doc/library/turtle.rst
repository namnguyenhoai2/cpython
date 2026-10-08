================================
:mod:`!turtle` --- Đồ họa Turtle
================================

.. module:: turtle
   :synopsis: Một framework giáo dục dành cho các ứng dụng đồ họa đơn giản

.. sectionauthor:: Gregor Lingl <gregor.lingl@aon.at>

**Mã nguồn:** :source:`Lib/turtle.py`

.. testsetup:: default
   :skipif: _tkinter is None

   from turtle import *
   turtle = Turtle()

.. testcleanup::
   :skipif: _tkinter is None

   import os
   os.remove("my_drawing.ps")

--------------

.. sidebar:: Ngôi sao Turtle

   Turtle có thể vẽ các hình dạng phức tạp bằng những chương trình lặp lại các bước di chuyển đơn giản.

   .. image:: turtle-star.png
      :alt: Một ngôi sao bùng nổ màu vàng với các tia mảnh và đường viền màu đỏ, được vẽ bằng turtle.
      :align: center

Hãy tưởng tượng một chú turtle robot bắt đầu tại (0, 0) trên mặt phẳng x-y. Sau một ``import turtle``, hãy ra lệnh ``turtle.forward(15)`` cho nó, và nó sẽ di chuyển (trên màn hình!) 15 pixel theo hướng đang quay mặt tới, đồng thời vẽ một đường thẳng khi di chuyển. Ra lệnh ``turtle.right(25)`` cho nó, và nó sẽ xoay tại chỗ 25 độ theo chiều kim đồng hồ.

Đồ họa Turtle là một cách triển khai `các công cụ vẽ được giới thiệu trong Logo <https://en.wikipedia.org/wiki/Turtle_(robot)>`__ vào năm 1967. Nó được tạo ra như một công cụ giáo dục, và phản hồi tức thì, trực quan giúp nó trở thành một cách hiệu quả để người học tiếp cận các khái niệm lập trình. Đây cũng là một cách thuận tiện để tạo ra đầu ra đồ họa đơn giản mà không cần sử dụng các thư viện bên ngoài.

Tài liệu này gồm bốn phần chính:

* :ref:`turtle-tutorial` hướng dẫn những kiến thức cơ bản về vẽ bằng Turtle.
* :ref:`turtle-reference` mô tả các hàm, phương thức và lớp mà module này định nghĩa.
* :ref:`turtle-howtos` trình bày chi tiết cách xử lý các tác vụ cụ thể.
* :ref:`turtle-explanation` cung cấp thông tin nền tảng về giao diện hướng đối tượng.

.. note::

   Đồ họa Turtle yêu cầu :mod:`tkinter` :term:`optional module`. Các trình cài đặt python.org dành cho Windows và macOS có sẵn thành phần này, nhưng một số bản phân phối Linux và các nền tảng khác có thể đóng gói riêng. Nếu ``import turtle`` không thành công với lỗi đề cập đến ``_tkinter``, hãy tìm tài liệu từ nhà phân phối của bạn (tức là bên đã cung cấp Python cho bạn). Hãy kiểm tra điều này trước nếu bạn dự định sử dụng đồ họa Turtle với người học.


.. _turtle-tutorial:
.. _get-started:
.. _get-started-as-quickly-as-possible:

Hướng dẫn
=========

Người dùng mới nên bắt đầu từ đây. Trong hướng dẫn này, chúng ta sẽ tìm hiểu một số kiến thức cơ bản về vẽ bằng turtle.


Khởi động môi trường turtle
---------------------------

Trong Python shell, import tất cả các đối tượng của module ``turtle``::

    from turtle import *

Nếu gặp lỗi ``No module named '_tkinter'``, bạn sẽ phải cài đặt :mod:`Tk interface package <tkinter>` trên hệ thống của mình.


Vẽ cơ bản
---------

Điều khiển turtle tiến về phía trước 100 bước::

   forward(100)

Bạn sẽ thấy (rất có thể là trong một cửa sổ mới trên màn hình) một đường thẳng do turtle vẽ, hướng về phía Đông. Hãy thay đổi hướng của turtle để nó quay 120 độ sang trái (ngược chiều kim đồng hồ)::

   left(120)

Hãy tiếp tục bằng cách vẽ một hình tam giác::

   forward(100)
   left(120)
   forward(100)

Hãy chú ý cách turtle, được biểu diễn bằng một mũi tên, chỉ theo các hướng khác nhau khi bạn điều khiển nó.

Hãy thử nghiệm với những lệnh đó, cũng như ``backward()`` và ``right()``. Nhiều lệnh còn có các alias ngắn hơn, chẳng hạn như ``fd()`` cho
:func:`forward`.


Điều khiển bút
^^^^^^^^^^^^^^

Hãy thử thay đổi màu — chẳng hạn như ``color('blue')`` — và độ rộng của đường — chẳng hạn như ``width(3)`` — rồi vẽ lại.

Bạn cũng có thể di chuyển turtle mà không vẽ bằng cách nhấc bút lên: ``up()`` trước khi di chuyển. Để bắt đầu vẽ lại, hãy sử dụng ``down()``.


Vị trí của rùa
^^^^^^^^^^^^^^

Đưa rùa trở về điểm bắt đầu (hữu ích nếu rùa đã biến mất khỏi màn hình)::

   home()

Vị trí home nằm ở chính giữa màn hình của rùa. Nếu cần biết vị trí này, hãy lấy tọa độ x-y của rùa bằng::

    pos()

Home nằm tại ``(0, 0)``.

Và sau một lúc, có lẽ bạn sẽ muốn xóa cửa sổ để chúng ta có thể bắt đầu lại::

   clearscreen()


Tạo các mẫu hình thuật toán
---------------------------

Bằng cách sử dụng các vòng lặp, bạn có thể tạo nên các mẫu hình hình học::

    for steps in range(100):
        for c in ('blue', 'red', 'green'):
            color(c)
            forward(steps)
            right(30)


\  - tất nhiên, chỉ bị giới hạn bởi trí tưởng tượng!

Hãy vẽ hình ngôi sao ở đầu trang này. Chúng ta muốn các đường màu đỏ, được tô màu vàng::

    color('red')
    fillcolor('yellow')

Cũng như ``up()`` và ``down()`` xác định liệu các đường có được vẽ hay không, việc tô màu cũng có thể được bật và tắt::

    begin_fill()

Tiếp theo, chúng ta sẽ tạo một vòng lặp::

    start = pos()

    while True:
        forward(200)
        left(170)
        if distance(start) < 1:
            break

``distance(start) < 1`` là một cách hữu ích để biết khi nào turtle quay lại vị trí bắt đầu.

Cuối cùng, hãy hoàn tất việc tô màu::

    end_fill()

(Lưu ý rằng việc tô màu chỉ thực sự diễn ra khi bạn đưa ra lệnh ``end_fill()``.)


.. _turtle-reference:
.. _turtle-graphics-reference:

Tham khảo
=========

.. _turtle-methods:
.. _methods-of-rawturtle-turtle-and-corresponding-functions:

Các phương thức và hàm của Turtle
---------------------------------

Hầu hết các ví dụ trong phần này đều tham chiếu đến một thực thể Turtle có tên là ``turtle``.

.. _turtle-motion:

Di chuyển và vẽ
^^^^^^^^^^^^^^^

.. function:: forward(distance)
              fd(distance)

   :param distance: một số

   Di chuyển rùa về phía trước theo *khoảng cách* được chỉ định, theo hướng rùa đang hướng tới.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.position()
      (0.00,0.00)
      >>> turtle.forward(25)
      >>> turtle.position()
      (25.00,0.00)
      >>> turtle.forward(-75)
      >>> turtle.position()
      (-50.00,0.00)


.. function:: back(distance)
              bk(distance) backward(distance)

   :param distance: một số

   Di chuyển turtle lùi lại một khoảng *distance*, ngược với hướng turtle đang hướng tới. Hướng của turtle không thay đổi.

   .. doctest::
      :skipif: _tkinter is None
      :hide:

      >>> turtle.goto(0, 0)

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.position()
      (0.00,0.00)
      >>> turtle.backward(30)
      >>> turtle.position()
      (-30.00,0.00)


.. function:: right(angle)
              rt(angle)

   :param angle: một số

   Xoay turtle sang phải theo *angle* được chỉ định. Theo mặc định, góc được đo bằng độ; có thể thay đổi đơn vị bằng :func:`degrees` hoặc
   :func:`radians`. Cách đo hướng phụ thuộc vào chế độ của turtle, xem :func:`mode`.

   .. doctest::
      :skipif: _tkinter is None
      :hide:

      >>> turtle.setheading(22)

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.heading()
      22.0
      >>> turtle.right(45)
      >>> turtle.heading()
      337.0


.. function:: left(angle)
              lt(angle)

   :param angle: một số

   Xoay turtle sang trái theo *góc* được chỉ định. Theo mặc định, góc được đo bằng độ; đơn vị có thể được thay đổi bằng :func:`degrees` hoặc
   :func:`radians`. Cách đo hướng phụ thuộc vào chế độ của turtle, xem :func:`mode`.

   .. doctest::
      :skipif: _tkinter is None
      :hide:

      >>> turtle.setheading(22)

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.heading()
      22.0
      >>> turtle.left(45)
      >>> turtle.heading()
      67.0


.. function:: goto(x, y=None)
              setpos(x, y=None) setposition(x, y=None)

   :param x: một số hoặc một cặp/vector số
   :param y: một số hoặc ``None``

   Di chuyển turtle đến một vị trí tuyệt đối. Nếu *y* là ``None``, *x* phải là một cặp tọa độ hoặc một :class:`Vec2D`, chẳng hạn như giá trị được trả về bởi
   :func:`pos`. Nếu bút đang hạ, một đường thẳng sẽ được vẽ. Hướng của turtle không thay đổi.

   .. doctest::
      :skipif: _tkinter is None
      :hide:

      >>> turtle.goto(0, 0)

   .. doctest::
      :skipif: _tkinter is None

      >>> tp = turtle.pos()
      >>> tp
      (0.00,0.00)
      >>> turtle.goto(60,30)
      >>> turtle.pos()
      (60.00,30.00)
      >>> turtle.goto((20,80))
      >>> turtle.pos()
      (20.00,80.00)
      >>> turtle.goto(tp)
      >>> turtle.pos()
      (0.00,0.00)


.. function:: teleport(x, y=None, *, fill_gap=False)

   :param x: một số hoặc ``None``
   :param y: một số hoặc ``None``
   :param fill_gap: một giá trị boolean

   Di chuyển turtle đến một vị trí tuyệt đối. Không giống như goto(x, y), thao tác này sẽ không vẽ đường thẳng. Hướng của turtle không thay đổi. Nếu hiện đang tô, đa giác mà turtle được dịch chuyển khỏi đó sẽ được tô sau khi rời đi, và việc tô sẽ bắt đầu lại sau khi dịch chuyển. Có thể vô hiệu hóa hành vi này bằng fill_gap=True, khiến đường tưởng tượng mà turtle đi qua trong khi dịch chuyển hoạt động như một rào chắn đối với việc tô, giống như trong goto(x, y).

   .. doctest::
      :skipif: _tkinter is None
      :hide:

      >>> turtle.goto(0, 0)

   .. doctest::
      :skipif: _tkinter is None

      >>> tp = turtle.pos()
      >>> tp
      (0.00,0.00)
      >>> turtle.teleport(60)
      >>> turtle.pos()
      (60.00,0.00)
      >>> turtle.teleport(y=10)
      >>> turtle.pos()
      (60.00,10.00)
      >>> turtle.teleport(20, 30)
      >>> turtle.pos()
      (20.00,30.00)

   .. versionadded:: 3.12


.. function:: setx(x)

   :param x: một số

   Đặt tọa độ x của rùa thành *x*. Tọa độ y không thay đổi.

   .. doctest::
      :skipif: _tkinter is None
      :hide:

      >>> turtle.goto(0, 240)

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.position()
      (0.00,240.00)
      >>> turtle.setx(10)
      >>> turtle.position()
      (10.00,240.00)


.. function:: sety(y)

   :param y: một số

   Đặt tọa độ y của rùa thành *y*. Tọa độ x không thay đổi.

   .. doctest::
      :skipif: _tkinter is None
      :hide:

      >>> turtle.goto(0, 40)

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.position()
      (0.00,40.00)
      >>> turtle.sety(-10)
      >>> turtle.position()
      (0.00,-10.00)


.. function:: setheading(to_angle)
              seth(to_angle)

   :param to_angle: một số

   Đặt hướng của rùa thành *to_angle*. Dưới đây là một số hướng phổ biến tính theo độ:

   +---------------+-------------+
   | standard mode | chế độ logo |
   +===============+=============+
   | 0 - đông      | 0 - bắc     |
   +---------------+-------------+
   | 90 - bắc      | 90 - đông   |
   +---------------+-------------+
   | 180 - tây     | 180 - nam   |
   +---------------+-------------+
   | 270 - nam     | 270 - tây   |
   +---------------+-------------+

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.setheading(90)
      >>> turtle.heading()
      90.0


.. function:: home()

   Di chuyển rùa đến gốc tọa độ, tọa độ (0,0). Hướng của rùa được đặt thành hướng ban đầu, phụ thuộc vào chế độ của rùa, xem
   :func:`mode`.

   .. doctest::
      :skipif: _tkinter is None
      :hide:

      >>> turtle.setheading(90)
      >>> turtle.goto(0, -10)

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.heading()
      90.0
      >>> turtle.position()
      (0.00,-10.00)
      >>> turtle.home()
      >>> turtle.position()
      (0.00,0.00)
      >>> turtle.heading()
      0.0


.. function:: circle(radius, extent=None, steps=None)

   :param radius: một số
   :param extent: một số hoặc ``None``
   :param steps: một số nguyên hoặc ``None``

   Vẽ một đường tròn với *radius* đã cho. Tâm nằm cách rùa *radius* đơn vị về bên trái; *extent*, một góc, xác định phần nào của đường tròn được vẽ. Nếu không cung cấp *extent*, hãy vẽ toàn bộ đường tròn. Nếu *extent* không phải là một đường tròn đầy đủ, một đầu mút của cung là vị trí hiện tại của bút. Vẽ cung theo hướng ngược chiều kim đồng hồ nếu *radius* dương, nếu không thì theo chiều kim đồng hồ. Cuối cùng, hướng của rùa được thay đổi một lượng *extent*.

   Khi đường tròn được xấp xỉ bằng một đa giác đều nội tiếp, *steps* xác định số bước cần sử dụng. Nếu không được cung cấp, giá trị này sẽ được tự động tính. Có thể dùng để vẽ các đa giác đều.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.home()
      >>> turtle.position()
      (0.00,0.00)
      >>> turtle.heading()
      0.0
      >>> turtle.circle(50)
      >>> turtle.position()
      (-0.00,0.00)
      >>> turtle.heading()
      0.0
      >>> turtle.circle(120, 180)  # vẽ một nửa đường tròn
      >>> turtle.position()
      (0.00,240.00)
      >>> turtle.heading()
      180.0


.. function:: dot()
              dot(size) dot(color, /) dot(size, color, /) dot(size, r, g, b, /)

   :param size: một số nguyên >= 1 (nếu được cung cấp)
   :param color: một colorstring hoặc một tuple màu dạng số

   Vẽ một chấm hình tròn có đường kính *size*, sử dụng *color*. Nếu không cung cấp *size*, giá trị lớn hơn giữa ``pensize+4`` và ``2*pensize`` sẽ được sử dụng.


   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.home()
      >>> turtle.dot()
      >>> turtle.fd(50); turtle.dot(20, "blue"); turtle.fd(50)
      >>> turtle.position()
      (100.00,-0.00)
      >>> turtle.heading()
      0.0


.. function:: stamp()

   Đóng dấu một bản sao của hình dạng turtle lên canvas tại vị trí hiện tại của turtle. Trả về một stamp_id cho dấu đó, có thể dùng để xóa dấu bằng cách gọi ``clearstamp(stamp_id)``.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.color("blue")
      >>> stamp_id = turtle.stamp()
      >>> turtle.fd(50)


.. function:: clearstamp(stampid)

   :param stampid: một số nguyên, phải là giá trị trả về của thao tác trước đó
                   :func:`stamp` call

   Xóa con dấu có *stampid* đã cho.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.position()
      (150.00,-0.00)
      >>> turtle.color("blue")
      >>> astamp = turtle.stamp()
      >>> turtle.fd(50)
      >>> turtle.position()
      (200.00,-0.00)
      >>> turtle.clearstamp(astamp)
      >>> turtle.position()
      (200.00,-0.00)


.. function:: clearstamps(n=None)

   :param n: một số nguyên (hoặc ``None``)

   Xóa tất cả hoặc *n* con dấu đầu/cuối của rùa. Nếu *n* là ``None``, hãy xóa tất cả các con dấu; nếu *n* > 0, hãy xóa *n* con dấu đầu tiên; nếu không, nếu *n* < 0, hãy xóa *n* con dấu cuối cùng.

   .. doctest::
      :skipif: _tkinter is None

      >>> for i in range(8):
      ...     unused_stamp_id = turtle.stamp()
      ...     turtle.fd(30)
      >>> turtle.clearstamps(2)
      >>> turtle.clearstamps(-2)
      >>> turtle.clearstamps()


.. function:: undo()

   Hoàn tác (lặp lại) hành động cuối cùng của rùa. Số hành động có thể hoàn tác được xác định bởi kích thước của undobuffer.

   .. doctest::
      :skipif: _tkinter is None

      >>> for i in range(4):
      ...     turtle.fd(50); turtle.lt(80)
      ...
      >>> for i in range(8):
      ...     turtle.undo()


.. function:: speed(speed=None)

   :param speed: một số nguyên trong phạm vi 0..10 hoặc một speedstring (xem bên dưới)

   Đặt tốc độ của turtle thành một giá trị nguyên trong khoảng 0..10. Nếu không cung cấp đối số, trả về tốc độ hiện tại.

   Nếu đầu vào là một số lớn hơn 10 hoặc nhỏ hơn 0.5, tốc độ được đặt thành 0. Các chuỗi tốc độ được ánh xạ thành các giá trị tốc độ như sau:

   * "fastest":  0
   * "fast":  10
   * "normal":  6
   * "slow":  3
   * "slowest":  1

   Các giá trị từ 1 đến 10 buộc hoạt ảnh vẽ đường và xoay turtle diễn ra ngày càng nhanh.

   Lưu ý: *tốc độ* = 0 có nghĩa là *không* có animation nào diễn ra. forward/back khiến turtle nhảy, tương tự, left/right khiến turtle xoay ngay lập tức.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.speed()
      3
      >>> turtle.speed('normal')
      >>> turtle.speed()
      6
      >>> turtle.speed(9)
      >>> turtle.speed()
      9


Cho biết trạng thái của Turtle
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. function:: position()
              pos()

   Trả về vị trí hiện tại (x,y) của turtle dưới dạng :class:`Vec2D` vector.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.pos()
      (440.00,-0.00)


.. function:: towards(x, y=None)

   :param x: một số hoặc một cặp/vector các số hoặc một instance của turtle
   :param y: một số nếu *x* là một số, nếu không thì ``None``

   Trả về góc của đường thẳng từ vị trí của turtle đến (x,y). Nếu *y* là ``None``, *x* phải là một cặp tọa độ, một :class:`Vec2D`, ví dụ như được trả về bởi :func:`pos`, hoặc một turtle khác. Góc được đo từ hướng ban đầu của turtle, phụ thuộc vào chế độ turtle; xem
   :func:`mode`.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.goto(10, 10)
      >>> turtle.towards(0,0)
      225.0


.. function:: xcor()

   Trả về tọa độ x của turtle.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.home()
      >>> turtle.left(50)
      >>> turtle.forward(100)
      >>> turtle.pos()
      (64.28,76.60)
      >>> print(round(turtle.xcor(), 5))
      64.27876


.. function:: ycor()

   Trả về tọa độ y của turtle.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.home()
      >>> turtle.left(60)
      >>> turtle.forward(100)
      >>> print(turtle.pos())
      (50.00,86.60)
      >>> print(round(turtle.ycor(), 5))
      86.60254


.. function:: heading()

   Trả về hướng hiện tại của turtle. Giá trị này phụ thuộc vào chế độ turtle, xem :func:`mode`.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.home()
      >>> turtle.left(67)
      >>> turtle.heading()
      67.0


.. function:: distance(x, y=None)

   :param x: một số hoặc một cặp/vector các số hoặc một instance của turtle
   :param y: một số nếu *x* là một số, nếu không thì ``None``

   Trả về khoảng cách từ turtle đến (x,y) theo đơn vị bước của turtle. Nếu *y* là ``None``, *x* phải là một cặp tọa độ, một :class:`Vec2D`, ví dụ như được trả về bởi :func:`pos`, hoặc một turtle khác.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.home()
      >>> turtle.distance(30,40)
      50.0
      >>> turtle.distance((30,40))
      50.0
      >>> joe = Turtle()
      >>> joe.forward(77)
      >>> turtle.distance(joe)
      77.0


Cài đặt đo lường
^^^^^^^^^^^^^^^^

.. function:: degrees(fullcircle=360.0)

   :param fullcircle: một số

   Đặt đơn vị đo góc thành độ. Số độ trong một vòng tròn đầy đủ được đặt thành *fullcircle*, mặc định là 360.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.home()
      >>> turtle.left(90)
      >>> turtle.heading()
      90.0

      >>> # Thay đổi đơn vị đo góc thành grad (còn gọi là gon,
      >>> # grade hoặc gradian và bằng 1/100 góc vuông.)
      >>> turtle.degrees(400.0)
      >>> turtle.heading()
      100.0
      >>> turtle.degrees(360)
      >>> turtle.heading()
      90.0


.. function:: radians()

   Đặt đơn vị đo góc thành radian. Tương đương với ``degrees(2 * math.pi)``.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.home()
      >>> turtle.left(90)
      >>> turtle.heading()
      90.0
      >>> turtle.radians()
      >>> turtle.heading()
      1.5707963267948966

   .. doctest::
      :skipif: _tkinter is None
      :hide:

      >>> turtle.degrees(360)


Điều khiển bút
^^^^^^^^^^^^^^

Trạng thái vẽ
~~~~~~~~~~~~~

.. function:: pendown()
              pd() down()

   Hạ bút -- vẽ khi di chuyển.


.. function:: penup()
              pu() up()

   Nhấc bút -- không vẽ khi di chuyển.


.. function:: pensize(width=None)
              width(width=None)

   :param width: một số dương

   Đặt độ dày đường kẻ thành *width* hoặc trả về độ dày đó. Nếu resizemode được đặt thành "auto" và turtleshape là một đa giác, đa giác đó sẽ được vẽ với cùng độ dày đường kẻ. Nếu không cung cấp đối số, pensize hiện tại sẽ được trả về.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.pensize()
      1
      >>> turtle.pensize(10)   # từ đây trở đi, các đường kẻ có độ rộng 10 sẽ được vẽ


.. function:: pen(pen=None, **pendict)

   :param pen: một dictionary có một số hoặc tất cả các khóa được liệt kê bên dưới
   :param pendict: một hoặc nhiều keyword-arguments với các khóa được liệt kê bên dưới làm keyword

   Trả về hoặc đặt các thuộc tính của pen trong một "pen-dictionary" với các cặp khóa/giá trị sau:

   * "shown": True/False
   * "pendown": True/False
   * "pencolor": chuỗi màu hoặc bộ màu
   * "fillcolor": chuỗi màu hoặc bộ màu
   * "pensize": số dương
   * "speed": số trong khoảng 0..10
   * "resizemode": "auto" hoặc "user" hoặc "noresize"
   * "stretchfactor": (số dương, số dương)
   * "outline": số dương
   * "tilt": number

   Từ điển này có thể được dùng làm đối số cho lần gọi :func:`pen` tiếp theo để khôi phục trạng thái bút trước đó. Ngoài ra, có thể cung cấp một hoặc nhiều thuộc tính này dưới dạng keyword argument. Cách này cho phép thiết lập nhiều thuộc tính bút trong một câu lệnh.

   .. doctest::
      :skipif: _tkinter is None
      :options: +NORMALIZE_WHITESPACE

      >>> turtle.pen(fillcolor="black", pencolor="red", pensize=10)
      >>> sorted(turtle.pen().items())
      [('fillcolor', 'black'), ('outline', 1), ('pencolor', 'red'),
       ('pendown', True), ('pensize', 10), ('resizemode', 'noresize'),
       ('shearfactor', 0.0), ('shown', True), ('speed', 9),
       ('stretchfactor', (1.0, 1.0)), ('tilt', 0.0)]
      >>> penstate=turtle.pen()
      >>> turtle.color("yellow", "")
      >>> turtle.penup()
      >>> sorted(turtle.pen().items())[:3]
      [('fillcolor', ''), ('outline', 1), ('pencolor', 'yellow')]
      >>> turtle.pen(penstate, fillcolor="green")
      >>> sorted(turtle.pen().items())[:3]
      [('fillcolor', 'green'), ('outline', 1), ('pencolor', 'red')]

.. function:: isdown()

   Trả về ``True`` nếu bút đang hạ, ``False`` nếu bút đang nhấc.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.penup()
      >>> turtle.isdown()
      False
      >>> turtle.pendown()
      >>> turtle.isdown()
      True


Điều khiển màu
~~~~~~~~~~~~~~

.. function:: pencolor()
              pencolor(color, /) pencolor(r, g, b, /)

   Trả về hoặc thiết lập pencolor.

   Có bốn định dạng đầu vào được cho phép:

   ``pencolor()``
      Trả về pencolor hiện tại dưới dạng chuỗi đặc tả màu hoặc tuple (xem ví dụ). Có thể dùng làm đầu vào cho một lệnh gọi color/pencolor/fillcolor/bgcolor khác.

   ``pencolor(colorstring)``
      Đặt pencolor thành *colorstring*, là một chuỗi đặc tả màu Tk, chẳng hạn như ``"red"``, ``"yellow"`` hoặc ``"#33cc8c"``.

   ``pencolor((r, g, b))``
      Đặt pencolor thành màu RGB được biểu diễn bởi tuple gồm *r*, *g* và *b*. Mỗi giá trị trong *r*, *g* và *b* phải nằm trong phạm vi 0..colormode, trong đó colormode là 1.0 hoặc 255 (xem :func:`colormode`).

   ``pencolor(r, g, b)``
      Đặt pencolor thành màu RGB được biểu diễn bởi *r*, *g* và *b*. Mỗi giá trị trong *r*, *g* và *b* phải nằm trong phạm vi 0..colormode.

   Nếu turtleshape là một đa giác, đường viền của đa giác đó sẽ được vẽ bằng pencolor mới được đặt.

   .. doctest::
      :skipif: _tkinter is None

      >>> colormode()
      1.0
      >>> turtle.pencolor()
      'red'
      >>> turtle.pencolor("brown")
      >>> turtle.pencolor()
      'brown'
      >>> tup = (0.2, 0.8, 0.55)
      >>> turtle.pencolor(tup)
      >>> turtle.pencolor()
      (0.2, 0.8, 0.5490196078431373)
      >>> colormode(255)
      >>> turtle.pencolor()
      (51.0, 204.0, 140.0)
      >>> turtle.pencolor('#32c18f')
      >>> turtle.pencolor()
      (50.0, 193.0, 143.0)


.. function:: fillcolor()
              fillcolor(color, /) fillcolor(r, g, b, /)

   Trả về hoặc đặt fillcolor.

   Có bốn định dạng đầu vào được cho phép:

   ``fillcolor()``
      Trả về fillcolor hiện tại dưới dạng chuỗi đặc tả màu, có thể ở định dạng tuple (xem ví dụ). Có thể dùng chuỗi này làm đầu vào cho một lệnh gọi color/pencolor/fillcolor/bgcolor khác.

   ``fillcolor(colorstring)``
      Đặt fillcolor thành *colorstring*, đây là một chuỗi đặc tả màu Tk, chẳng hạn như ``"red"``, ``"yellow"`` hoặc ``"#33cc8c"``.

   ``fillcolor((r, g, b))``
      Đặt fillcolor thành màu RGB được biểu diễn bởi tuple gồm *r*, *g* và *b*. Mỗi giá trị trong *r*, *g* và *b* phải nằm trong phạm vi 0..colormode, trong đó colormode là 1.0 hoặc 255 (xem :func:`colormode`).

   ``fillcolor(r, g, b)``
      Đặt fillcolor thành màu RGB được biểu diễn bởi *r*, *g* và *b*. Mỗi giá trị trong *r*, *g* và *b* phải nằm trong phạm vi 0..colormode.

   Nếu turtleshape là một đa giác, phần bên trong đa giác đó sẽ được vẽ bằng fillcolor mới được đặt.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.fillcolor("violet")
      >>> turtle.fillcolor()
      'violet'
      >>> turtle.pencolor()
      (50.0, 193.0, 143.0)
      >>> turtle.fillcolor((50, 193, 143))  # Số nguyên, không phải số thực
      >>> turtle.fillcolor()
      (50.0, 193.0, 143.0)
      >>> turtle.fillcolor('#ffffff')
      >>> turtle.fillcolor()
      (255.0, 255.0, 255.0)


.. function:: color()
              color(color, /) color(r, g, b, /) color(pencolor, fillcolor, /)

   Trả về hoặc thiết lập pencolor và fillcolor.

   Cho phép sử dụng một số định dạng đầu vào. Chúng sử dụng từ 0 đến 3 đối số như sau:

   ``color()``
      Trả về pencolor hiện tại và fillcolor hiện tại dưới dạng một cặp chuỗi hoặc tuple đặc tả màu như được trả về bởi :func:`pencolor` và
      :func:`fillcolor`.

   ``color(colorstring)``, ``color((r,g,b))``, ``color(r,g,b)``
      Đầu vào như trong :func:`pencolor`, thiết lập cả fillcolor và pencolor thành giá trị đã cho.

   ``color(colorstring1, colorstring2)``, ``color((r1,g1,b1), (r2,g2,b2))``
      Tương đương với ``pencolor(colorstring1)`` và ``fillcolor(colorstring2)``, và tương tự nếu sử dụng định dạng đầu vào khác.

   Nếu turtleshape là một đa giác, đường viền và phần bên trong của đa giác đó sẽ được vẽ bằng các màu mới được thiết lập.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.color("red", "green")
      >>> turtle.color()
      ('red', 'green')
      >>> color("#285078", "#a0c8f0")
      >>> color()
      ((40.0, 80.0, 120.0), (160.0, 200.0, 240.0))


Xem thêm: Screen method :func:`colormode`.


Tô màu
~~~~~~

.. doctest::
   :skipif: _tkinter is None
   :hide:

   >>> turtle.home()

.. function:: filling()

   Trả về fillstate (``True`` nếu đang tô màu, ``False`` nếu không).

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.begin_fill()
      >>> if turtle.filling():
      ...    turtle.pensize(5)
      ... else:
      ...    turtle.pensize(3)

.. function:: fill()

   Tô hình được vẽ trong khối ``with turtle.fill():``.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.color("black", "red")
      >>> with turtle.fill():
      ...     turtle.circle(80)

   Sử dụng :func:`!fill` tương đương với việc thêm :func:`begin_fill` trước khối tô và :func:`end_fill` sau khối tô:

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.color("black", "red")
      >>> turtle.begin_fill()
      >>> turtle.circle(80)
      >>> turtle.end_fill()

   .. versionadded:: 3.14


.. function:: begin_fill()

   Được gọi ngay trước khi vẽ một hình cần được tô.


.. function:: end_fill()

   Tô hình được vẽ sau lần gọi :func:`begin_fill` gần nhất.

   Việc các vùng chồng lấp của đa giác tự giao nhau hoặc nhiều hình có được tô màu hay không phụ thuộc vào hệ thống đồ họa của hệ điều hành, kiểu chồng lấp và số vùng chồng lấp. Ví dụ, ngôi sao Turtle ở trên có thể hoàn toàn màu vàng hoặc có một số vùng màu trắng.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.color("black", "red")
      >>> turtle.begin_fill()
      >>> turtle.circle(80)
      >>> turtle.end_fill()


Kiểm soát việc vẽ nâng cao hơn
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. function:: reset()

   Xóa các hình vẽ của turtle khỏi màn hình, đưa turtle về giữa màn hình và đặt các biến về giá trị mặc định.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.goto(0,-22)
      >>> turtle.left(100)
      >>> turtle.position()
      (0.00,-22.00)
      >>> turtle.heading()
      100.0
      >>> turtle.reset()
      >>> turtle.position()
      (0.00,0.00)
      >>> turtle.heading()
      0.0


.. function:: clear()

   Xóa các hình vẽ của turtle khỏi màn hình. Không di chuyển turtle. Trạng thái và vị trí của turtle cũng như hình vẽ của các turtle khác không bị ảnh hưởng.


.. function:: write(arg, move=False, align="left", font=("Arial", 8, "normal"))

   :param arg: đối tượng sẽ được ghi vào TurtleScreen
   :param move: True/False
   :param align: một trong các chuỗi "left", "center" hoặc right"
   :param font: một bộ ba (fontname, fontsize, fonttype)

   Viết văn bản - biểu diễn chuỗi của *arg* - tại vị trí hiện tại của turtle theo *align* ("left", "center" hoặc "right") và với font đã cho. Nếu *move* là true, bút sẽ được di chuyển đến góc dưới bên phải của văn bản. Theo mặc định, *move* là ``False``.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.write("Home = ", True, align="center")
      >>> turtle.write((0,0), True)


Trạng thái turtle
^^^^^^^^^^^^^^^^^

Khả năng hiển thị
~~~~~~~~~~~~~~~~~

.. function:: hideturtle()
              ht()

   Làm cho turtle trở nên vô hình. Bạn nên làm điều này khi đang thực hiện một số thao tác vẽ phức tạp, vì việc ẩn turtle giúp tăng tốc độ vẽ đáng kể.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.hideturtle()


.. function:: showturtle()
              st()

   Hiển thị rùa.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.showturtle()


.. function:: isvisible()

   Trả về ``True`` nếu Turtle đang được hiển thị, ``False`` nếu nó đang bị ẩn.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.hideturtle()
      >>> turtle.isvisible()
      False
      >>> turtle.showturtle()
      >>> turtle.isvisible()
      True


Diện mạo
~~~~~~~~

.. function:: shape(name=None)

   :param name: một chuỗi là shapename hợp lệ

   Đặt hình dạng của rùa thành hình dạng có *name* đã cho hoặc, nếu không cung cấp name, trả về name của hình dạng hiện tại. Hình dạng có *name* phải tồn tại trong từ điển hình dạng của TurtleScreen. Ban đầu có các hình đa giác sau: "arrow", "turtle", "circle", "square", "triangle", "classic". Để tìm hiểu cách xử lý hình dạng, hãy xem phương thức Screen :func:`register_shape`.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.shape()
      'classic'
      >>> turtle.shape("turtle")
      >>> turtle.shape()
      'turtle'


.. function:: resizemode(rmode=None)

   :param rmode: một trong các chuỗi "auto", "user", "noresize"

   Đặt resizemode thành một trong các giá trị: "auto", "user", "noresize". Nếu không cung cấp *rmode*, trả về resizemode hiện tại. Các resizemode khác nhau có những tác động sau:

   - "auto": điều chỉnh diện mạo của turtle tương ứng với giá trị của pensize.
   - "user": điều chỉnh diện mạo của turtle theo các giá trị của stretchfactor và outlinewidth (outline), được thiết lập bởi
     :func:`shapesize`.
   - "noresize": không thực hiện điều chỉnh diện mạo của turtle.

   ``resizemode("user")`` được :func:`shapesize` gọi khi được sử dụng với các đối số.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.resizemode()
      'noresize'
      >>> turtle.resizemode("auto")
      >>> turtle.resizemode()
      'auto'


.. function:: shapesize(stretch_wid=None, stretch_len=None, outline=None)
              turtlesize(stretch_wid=None, stretch_len=None, outline=None)

   :param stretch_wid: số dương
   :param stretch_len: số dương
   :param outline: số dương

   Trả về hoặc đặt các thuộc tính của pen là x/y-stretchfactors và/hoặc outline. Đặt resizemode thành "user". Khi và chỉ khi resizemode được đặt thành "user", turtle sẽ được hiển thị với độ kéo giãn theo các stretchfactor của nó: *stretch_wid* là stretchfactor vuông góc với hướng của nó, *stretch_len* là stretchfactor theo hướng của nó, *outline* xác định độ rộng outline của hình dạng.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.shapesize()
      (1.0, 1.0, 1)
      >>> turtle.resizemode("user")
      >>> turtle.shapesize(5, 5, 12)
      >>> turtle.shapesize()
      (5, 5, 12)
      >>> turtle.shapesize(outline=8)
      >>> turtle.shapesize()
      (5, 5, 8)


.. function:: shearfactor(shear=None)

   :param shear: number (tùy chọn)

   Đặt hoặc trả về shearfactor hiện tại. Làm nghiêng turtleshape theo shear đã cho, trong đó shear là tangent của góc nghiêng. *not* thay đổi heading (hướng di chuyển) của turtle. Nếu không cung cấp shear: trả về shearfactor hiện tại, tức là tangent của góc nghiêng, theo đó các đường thẳng song song với heading của turtle bị làm nghiêng.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.shape("circle")
      >>> turtle.shapesize(5,2)
      >>> turtle.shearfactor(0.5)
      >>> turtle.shearfactor()
      0.5


.. function:: tilt(angle)

   :param angle: a number

   Xoay turtleshape một góc *angle* tính từ góc nghiêng hiện tại, nhưng *not* thay đổi heading (hướng di chuyển) của turtle.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.reset()
      >>> turtle.shape("circle")
      >>> turtle.shapesize(5,2)
      >>> turtle.tilt(30)
      >>> turtle.fd(50)
      >>> turtle.tilt(30)
      >>> turtle.fd(50)


.. function:: tiltangle(angle=None)

   :param angle: a number (tùy chọn)

   Đặt hoặc trả về góc nghiêng hiện tại. Nếu angle được cung cấp, xoay turtleshape để hướng theo hướng được chỉ định bởi angle, bất kể góc nghiêng hiện tại của nó. Không *not* thay đổi heading của turtle (hướng di chuyển). Nếu không cung cấp angle: trả về góc nghiêng hiện tại, tức là góc giữa hướng của turtleshape và heading của turtle (hướng di chuyển của nó).

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.reset()
      >>> turtle.shape("circle")
      >>> turtle.shapesize(5,2)
      >>> turtle.tilt(45)
      >>> turtle.tiltangle()
      45.0


.. function:: shapetransform(t11=None, t12=None, t21=None, t22=None)

   :param t11: a number (tùy chọn)
   :param t12: a number (tùy chọn)
   :param t21: a number (tùy chọn)
   :param t12: a number (tùy chọn)

   Đặt hoặc trả về ma trận biến đổi hiện tại của turtleshape.

   Nếu không cung cấp phần tử ma trận nào, trả về ma trận biến đổi dưới dạng một tuple gồm 4 phần tử. Nếu không, đặt các phần tử đã cho và biến đổi turtleshape theo ma trận gồm hàng đầu tiên là t11, t12 và hàng thứ hai là t21, t22. Định thức t11 * t22 - t12 * t21 không được bằng 0; nếu không, sẽ phát sinh lỗi. Sửa đổi stretchfactor, shearfactor và tiltangle theo ma trận đã cho.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle = Turtle()
      >>> turtle.shape("square")
      >>> turtle.shapesize(4,2)
      >>> turtle.shearfactor(-0.5)
      >>> turtle.shapetransform()
      (4.0, -1.0, -0.0, 2.0)


.. function:: get_shapepoly()

   Trả về đa giác hình dạng hiện tại dưới dạng tuple gồm các cặp tọa độ. Có thể sử dụng nó để định nghĩa một hình dạng mới hoặc các thành phần của một hình dạng phức hợp.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.shape("square")
      >>> turtle.shapetransform(4, -1, 0, 2)
      >>> turtle.get_shapepoly()
      ((50, -20), (30, 20), (-50, 20), (-30, -20))


Sử dụng sự kiện
^^^^^^^^^^^^^^^

.. function:: onclick(fun, btn=1, add=None)
   :noindex:

   :param fun: một hàm có hai đối số, được gọi với tọa độ của điểm được nhấp trên canvas
   :param btn: số của nút chuột, mặc định là 1 (nút chuột trái)
   :param add: ``True`` hoặc ``False`` -- nếu ``True``, một binding mới sẽ được thêm vào, nếu không nó sẽ thay thế binding trước đó

   Liên kết *fun* với các sự kiện nhấp chuột trên turtle này. Nếu *fun* là ``None``, các binding hiện có sẽ bị xóa. Ví dụ cho turtle ẩn danh, tức là theo cách thủ tục:

   .. doctest::
      :skipif: _tkinter is None

      >>> def turn(x, y):
      ...     left(180)
      ...
      >>> onclick(turn)  # Bây giờ, khi nhấp vào turtle, nó sẽ xoay.
      >>> onclick(None)  # liên kết sự kiện sẽ bị xóa


.. function:: onrelease(fun, btn=1, add=None)

   :param fun: một hàm có hai đối số, được gọi với tọa độ của điểm được nhấp trên canvas
   :param btn: số của nút chuột, mặc định là 1 (nút chuột trái)
   :param add: ``True`` hoặc ``False`` -- nếu ``True``, một binding mới sẽ được thêm vào, nếu không nó sẽ thay thế binding trước đó

   Liên kết *fun* với các sự kiện nhả nút chuột trên turtle này. Nếu *fun* là ``None``, các liên kết hiện có sẽ bị xóa.

   .. doctest::
      :skipif: _tkinter is None

      >>> class MyTurtle(Turtle):
      ...     def glow(self,x,y):
      ...         self.fillcolor("red")
      ...     def unglow(self,x,y):
      ...         self.fillcolor("")
      ...
      >>> turtle = MyTurtle()
      >>> turtle.onclick(turtle.glow)     # nhấp vào turtle sẽ đổi fillcolor thành đỏ,
      >>> turtle.onrelease(turtle.unglow) # nhả nút chuột sẽ đổi nó thành trong suốt.


.. function:: ondrag(fun, btn=1, add=None)

   :param fun: một hàm có hai đối số, được gọi với tọa độ của điểm được nhấp trên canvas
   :param btn: số của nút chuột, mặc định là 1 (nút chuột trái)
   :param add: ``True`` hoặc ``False`` -- nếu ``True``, một binding mới sẽ được thêm vào, nếu không nó sẽ thay thế binding trước đó

   Gắn *fun* với các sự kiện di chuyển chuột trên turtle này. Nếu *fun* là ``None``, các liên kết hiện có sẽ bị xóa.

   Lưu ý: Mọi chuỗi sự kiện di chuyển chuột trên một turtle đều bắt đầu bằng một sự kiện nhấp chuột trên turtle đó.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.ondrag(turtle.goto)

   Sau đó, việc nhấp và kéo Turtle sẽ di chuyển nó trên màn hình, qua đó tạo ra các hình vẽ bằng tay (nếu bút đang hạ).


Các phương thức đặc biệt của Turtle
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. function:: poly()

   Ghi lại các đỉnh của một đa giác được vẽ trong khối ``with turtle.poly():``. Đỉnh đầu tiên và đỉnh cuối cùng sẽ được nối với nhau.

   .. doctest::
      :skipif: _tkinter is None

      >>> with turtle.poly():
      ...     turtle.forward(100)
      ...     turtle.right(60)
      ...     turtle.forward(100)

   .. versionadded:: 3.14


.. function:: begin_poly()

   Bắt đầu ghi lại các đỉnh của một đa giác. Vị trí hiện tại của turtle là đỉnh đầu tiên của đa giác.


.. function:: end_poly()

   Dừng ghi lại các đỉnh của một đa giác. Vị trí hiện tại của turtle là đỉnh cuối cùng của đa giác. Đỉnh này sẽ được nối với đỉnh đầu tiên.


.. function:: get_poly()

   Trả về đa giác được ghi lại gần nhất.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.home()
      >>> turtle.begin_poly()
      >>> turtle.fd(100)
      >>> turtle.left(20)
      >>> turtle.fd(30)
      >>> turtle.left(60)
      >>> turtle.fd(50)
      >>> turtle.end_poly()
      >>> p = turtle.get_poly()
      >>> register_shape("myFavouriteShape", p)


.. function:: clone()

   Tạo và trả về một bản sao của turtle với cùng vị trí, hướng và các thuộc tính của turtle.

   .. doctest::
      :skipif: _tkinter is None

      >>> mick = Turtle()
      >>> joe = mick.clone()


.. function:: getturtle()
              getpen()

   Trả về chính đối tượng Turtle. Cách sử dụng hợp lý duy nhất: dùng như một hàm để trả về "anonymous turtle":

   .. doctest::
      :skipif: _tkinter is None

      >>> pet = getturtle()
      >>> pet.fd(50)
      >>> pet
      <turtle.Turtle object at 0x...>


.. function:: getscreen()

   Trả về đối tượng :class:`TurtleScreen` mà turtle đang vẽ lên. Sau đó có thể gọi các phương thức TurtleScreen cho đối tượng đó.

   .. doctest::
      :skipif: _tkinter is None

      >>> ts = turtle.getscreen()
      >>> ts
      <turtle._Screen object at 0x...>
      >>> ts.bgcolor("pink")


.. function:: setundobuffer(size)

   :param size: một số nguyên hoặc ``None``

   Thiết lập hoặc vô hiệu hóa undobuffer. Nếu *size* là một số nguyên, một undobuffer trống với kích thước đã cho sẽ được cài đặt. *size* cung cấp số thao tác turtle tối đa có thể được hoàn tác bằng phương thức/hàm :func:`undo`. Nếu *size* là ``None``, undobuffer sẽ bị vô hiệu hóa.

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.setundobuffer(42)


.. function:: undobufferentries()

   Trả về số mục trong undobuffer.

   .. doctest::
      :skipif: _tkinter is None

      >>> while undobufferentries():
      ...     undo()



.. _compoundshapes:

Các hình dạng compound
^^^^^^^^^^^^^^^^^^^^^^

Để sử dụng các hình dạng turtle compound, bao gồm nhiều đa giác có màu khác nhau, bạn phải sử dụng rõ ràng lớp trợ giúp :class:`Shape` như mô tả dưới đây:

1. Tạo một đối tượng Shape trống thuộc kiểu "compound".
2. Thêm bao nhiêu component tùy ý vào đối tượng này bằng cách sử dụng
   phương thức :meth:`~Shape.addcomponent`.

   Ví dụ:

   .. doctest::
      :skipif: _tkinter is None

      >>> s = Shape("compound")
      >>> poly1 = ((0,0),(10,-5),(0,10),(-10,-5))
      >>> s.addcomponent(poly1, "red", "blue")
      >>> poly2 = ((0,0),(10,-5),(-10,-5))
      >>> s.addcomponent(poly2, "blue", "red")

3. Bây giờ, thêm Shape vào shapelist của Screen và sử dụng nó:

   .. doctest::
      :skipif: _tkinter is None

      >>> register_shape("myshape", s)
      >>> shape("myshape")


.. note::

   Lớp :class:`Shape` được phương thức :func:`register_shape` sử dụng nội bộ theo nhiều cách khác nhau. Lập trình viên ứng dụng chỉ phải xử lý lớp Shape *chỉ* khi sử dụng các compound shape như minh họa ở trên!


.. _methods-of-turtlescreen-screen:
.. _methods-of-turtlescreen-screen-and-corresponding-functions:

Các phương thức và hàm của Screen
---------------------------------

Hầu hết các ví dụ trong phần này đều đề cập đến một instance TurtleScreen có tên là ``screen``.

.. doctest::
   :skipif: _tkinter is None
   :hide:

   >>> screen = Screen()

Điều khiển cửa sổ
^^^^^^^^^^^^^^^^^

.. function:: bgcolor()
              bgcolor(color, /) bgcolor(r, g, b, /)

   Trả về hoặc đặt màu nền của TurtleScreen.

   Có thể sử dụng bốn định dạng đầu vào:

   ``bgcolor()``
      Trả về màu nền hiện tại dưới dạng chuỗi đặc tả màu hoặc tuple (xem ví dụ). Có thể dùng làm đầu vào cho một lệnh gọi color/pencolor/fillcolor/bgcolor khác.

   ``bgcolor(colorstring)``
      Đặt màu nền thành *colorstring*, là một chuỗi đặc tả màu Tk, chẳng hạn như ``"red"``, ``"yellow"`` hoặc ``"#33cc8c"``.

   ``bgcolor((r, g, b))``
      Đặt màu nền thành màu RGB được biểu diễn bằng tuple gồm *r*, *g* và *b*. Mỗi giá trị *r*, *g* và *b* phải nằm trong phạm vi 0..colormode, trong đó colormode là 1.0 hoặc 255 (xem :func:`colormode`).

   ``bgcolor(r, g, b)``
      Đặt màu nền thành màu RGB được biểu diễn bởi *r*, *g* và *b*. Mỗi giá trị *r*, *g* và *b* phải nằm trong phạm vi 0..colormode.

   .. doctest::
      :skipif: _tkinter is None

      >>> screen.bgcolor("orange")
      >>> screen.bgcolor()
      'orange'
      >>> screen.bgcolor("#800080")
      >>> screen.bgcolor()
      (128.0, 0.0, 128.0)


.. function:: bgpic(picname=None)

   :param picname: một chuỗi, tên của tệp hình ảnh (PNG, GIF, PGM và PPM), hoặc ``"nopic"``, hoặc ``None``

   Đặt ảnh nền hoặc trả về tên của ảnh nền hiện tại. Nếu *picname* là tên tệp, đặt hình ảnh tương ứng làm nền. Nếu *picname* là ``"nopic"``, xóa ảnh nền nếu có. Nếu *picname* là ``None``, trả về tên tệp của ảnh nền hiện tại.::

      >>> screen.bgpic()
      'nopic'
      >>> screen.bgpic("landscape.gif")
      >>> screen.bgpic()
      "landscape.gif"


.. function:: clear()
   :noindex:

   .. note::
      Phương thức TurtleScreen này chỉ khả dụng dưới dạng hàm global với tên ``clearscreen``. Hàm global ``clear`` là một hàm khác được dẫn xuất từ phương thức Turtle ``clear``.


.. function:: clearscreen()

   Xóa tất cả bản vẽ và tất cả turtle khỏi TurtleScreen. Đặt lại TurtleScreen hiện đang trống về trạng thái ban đầu: nền trắng, không có ảnh nền, không có liên kết sự kiện và bật tracing.


.. function:: reset()
   :noindex:

   .. note::
      Phương thức TurtleScreen này chỉ khả dụng dưới dạng hàm global với tên ``resetscreen``. Hàm global ``reset`` là một hàm khác được dẫn xuất từ phương thức Turtle ``reset``.


.. function:: resetscreen()

   Đặt lại tất cả Turtle trên Screen về trạng thái ban đầu.


.. function:: screensize(canvwidth=None, canvheight=None, bg=None)

   :param canvwidth: số nguyên dương, chiều rộng mới của canvas tính bằng pixel
   :param canvheight: số nguyên dương, chiều cao mới của canvas tính bằng pixel
   :param bg: colorstring hoặc color-tuple, màu nền mới

   Nếu không cung cấp đối số nào, trả về (canvaswidth, canvasheight) hiện tại. Nếu không, thay đổi kích thước canvas mà các turtle đang vẽ lên. Không thay đổi cửa sổ vẽ. Để quan sát các phần bị ẩn của canvas, hãy sử dụng các thanh cuộn. Với phương thức này, ta có thể hiển thị những phần của hình vẽ trước đây nằm bên ngoài canvas.

   .. doctest::
      :skipif: _tkinter is None

      >>> screen.screensize()
      (400, 300)
      >>> screen.screensize(2000,1500)
      >>> screen.screensize()
      (2000, 1500)

   ví dụ: để tìm một turtle bị escape sai ;-)​


.. function:: setworldcoordinates(llx, lly, urx, ury)

   :param llx: một số, tọa độ x của góc dưới bên trái canvas
   :param lly: một số, tọa độ y của góc dưới bên trái canvas
   :param urx: một số, tọa độ x của góc trên bên phải của canvas
   :param ury: một số, tọa độ y của góc trên bên phải của canvas

   Thiết lập hệ tọa độ do người dùng định nghĩa và chuyển sang chế độ "world" nếu cần. Thao tác này thực hiện một ``screen.reset()``. Nếu chế độ "world" đã được kích hoạt, tất cả hình vẽ sẽ được vẽ lại theo các tọa độ mới.

   **CHÚ Ý**: trong các hệ tọa độ do người dùng định nghĩa, các góc có thể bị biến dạng.

   .. doctest::
      :skipif: _tkinter is None

      >>> screen.reset()
      >>> screen.setworldcoordinates(-50,-7.5,50,7.5)
      >>> for _ in range(72):
      ...     left(10)
      ...
      >>> for _ in range(8):
      ...     left(45); fd(2)   # một hình bát giác đều

   .. doctest::
      :skipif: _tkinter is None
      :hide:

      >>> screen.reset()
      >>> for t in turtles():
      ...      t.reset()


Điều khiển hoạt ảnh
^^^^^^^^^^^^^^^^^^^

.. function:: no_animation()

   Tạm thời vô hiệu hóa hoạt ảnh của turtle. Mã được viết bên trong khối ``no_animation`` sẽ không được tạo hoạt ảnh; khi thoát khỏi khối mã, hình vẽ sẽ xuất hiện.

   .. doctest::
      :skipif: _tkinter is None

      >>> with screen.no_animation():
      ...     for dist in range(2, 400, 2):
      ...         fd(dist)
      ...         rt(90)

   .. versionadded:: 3.14


.. function:: delay(delay=None)

   :param delay: số nguyên dương

   Đặt hoặc trả về *độ trễ* vẽ tính bằng mili giây.  (Đây xấp xỉ là khoảng thời gian giữa hai lần cập nhật canvas liên tiếp.)  Độ trễ vẽ càng dài thì animation càng chậm.

   Đối số tùy chọn:

   .. doctest::
      :skipif: _tkinter is None

      >>> screen.delay()
      10
      >>> screen.delay(5)
      >>> screen.delay()
      5


.. function:: tracer(n=None, delay=None)

   :param n: số nguyên không âm
   :param delay: số nguyên không âm

   Bật/tắt animation của turtle và đặt độ trễ cho các bản vẽ được cập nhật.  Nếu cung cấp *n*, chỉ mỗi lần cập nhật màn hình thứ n mới thực sự được thực hiện.  (Có thể dùng để tăng tốc quá trình vẽ đồ họa phức tạp.)  Khi được gọi mà không có đối số, hàm trả về giá trị n hiện được lưu. Đối số thứ hai đặt giá trị độ trễ (xem
   :func:`delay`).

   .. doctest::
      :skipif: _tkinter is None

      >>> screen.tracer(8, 25)
      >>> dist = 2
      >>> for i in range(200):
      ...     fd(dist)
      ...     rt(90)
      ...     dist += 2


.. function:: update()

   Thực hiện cập nhật TurtleScreen. Dùng khi tracer bị tắt.

Xem thêm phương thức RawTurtle/Turtle :func:`speed`.


Sử dụng sự kiện màn hình
^^^^^^^^^^^^^^^^^^^^^^^^

.. function:: listen(xdummy=None, ydummy=None)

   Đặt tiêu điểm cho TurtleScreen (để thu thập các sự kiện phím). Các đối số giả được cung cấp để có thể truyền :func:`listen` vào phương thức onclick.


.. function:: onkey(fun, key)
              onkeyrelease(fun, key)

   :param fun: một hàm không có đối số hoặc ``None``
   :param key: một chuỗi: phím (ví dụ: "a") hoặc ký hiệu phím (ví dụ: "space")

   Liên kết *fun* với sự kiện nhả phím của key. Nếu *fun* là ``None``, các liên kết sự kiện sẽ bị gỡ bỏ. Lưu ý: để có thể đăng ký các sự kiện phím, TurtleScreen phải được đặt tiêu điểm. (Xem phương thức :func:`listen`.)

   .. doctest::
      :skipif: _tkinter is None

      >>> def f():
      ...     fd(50)
      ...     lt(60)
      ...
      >>> screen.onkey(f, "Up")
      >>> screen.listen()


.. function:: onkeypress(fun, key=None)

   :param fun: một hàm không có đối số hoặc ``None``
   :param key: một chuỗi: phím (ví dụ: "a") hoặc ký hiệu phím (ví dụ: "space")

   Gắn *fun* với sự kiện nhấn phím của key nếu key được cung cấp, hoặc với mọi sự kiện nhấn phím nếu không cung cấp key. Lưu ý: để có thể đăng ký các sự kiện bàn phím, TurtleScreen phải được focus. (Xem phương thức :func:`listen`.)

   .. doctest::
      :skipif: _tkinter is None

      >>> def f():
      ...     fd(50)
      ...
      >>> screen.onkey(f, "Up")
      >>> screen.listen()


.. function:: onclick(fun, btn=1, add=None)
              onscreenclick(fun, btn=1, add=None)

   :param fun: một hàm có hai đối số, được gọi với tọa độ của điểm được nhấp trên canvas
   :param btn: số hiệu nút chuột, mặc định là 1 (nút chuột trái)
   :param add: ``True`` hoặc ``False`` -- nếu ``True``, một binding mới sẽ được thêm vào; nếu không, nó sẽ thay thế binding trước đó

   Gắn *fun* với các sự kiện nhấp chuột trên màn hình này. Nếu *fun* là ``None``, các liên kết hiện có sẽ bị xóa.

   Ví dụ với một thực thể TurtleScreen có tên là ``screen`` và một thực thể Turtle có tên là ``turtle``:

   .. doctest::
      :skipif: _tkinter is None

      >>> screen.onclick(turtle.goto) # Sau đó, khi nhấp vào TurtleScreen, sẽ
      >>>                             # khiến turtle di chuyển đến điểm được nhấp.
      >>> screen.onclick(None)        # xóa lại liên kết sự kiện

   .. note::
      Phương thức TurtleScreen này chỉ khả dụng dưới dạng hàm toàn cục với tên ``onscreenclick``. Hàm toàn cục ``onclick`` là một hàm khác được dẫn xuất từ phương thức Turtle ``onclick``.


.. function:: ontimer(fun, t=0)

   :param fun: một hàm không có đối số
   :param t: một số >= 0

   Cài đặt một timer gọi *fun* sau *t* mili giây.

   .. doctest::
      :skipif: _tkinter is None

      >>> running = True
      >>> def f():
      ...     if running:
      ...         fd(50)
      ...         lt(60)
      ...         screen.ontimer(f, 250)
      >>> f()   ### khiến rùa di chuyển vòng quanh
      >>> running = False


.. function:: mainloop()
              done()

   Bắt đầu vòng lặp sự kiện - gọi hàm mainloop của Tkinter. Phải là câu lệnh cuối cùng trong chương trình đồ họa turtle. Phải *không* được sử dụng nếu chạy một script từ bên trong IDLE ở chế độ -n (Không có subprocess) - để sử dụng turtle graphics theo cách tương tác.::

      >>> screen.mainloop()


Các phương thức nhập
^^^^^^^^^^^^^^^^^^^^

.. function:: textinput(title, prompt)

   :param title: chuỗi
   :param prompt: chuỗi

   Hiển thị một cửa sổ hộp thoại để nhập một chuỗi. Tham số title là tiêu đề của cửa sổ hộp thoại, còn prompt là văn bản chủ yếu mô tả thông tin cần nhập. Trả về chuỗi đã nhập. Nếu hộp thoại bị hủy, trả về ``None``.::

      >>> screen.textinput("NIM", "Name of first player:")


.. function:: numinput(title, prompt, default=None, minval=None, maxval=None)

   :param title: chuỗi
   :param prompt: chuỗi
   :param default: number (tùy chọn)
   :param minval: number (tùy chọn)
   :param maxval: number (tùy chọn)

   Mở hộp thoại để nhập một số. title là tiêu đề của hộp thoại, prompt là văn bản chủ yếu mô tả thông tin số cần nhập. default: giá trị mặc định, minval: giá trị nhỏ nhất cho đầu vào, maxval: giá trị lớn nhất cho đầu vào. Đầu vào số phải nằm trong phạm vi minval .. maxval nếu các giá trị này được cung cấp. Nếu không, một gợi ý sẽ được đưa ra và hộp thoại vẫn mở để sửa lại. Trả về số đã nhập. Nếu hộp thoại bị hủy, trả về ``None``.::

      >>> screen.numinput("Poker", "Your stakes:", 1000, minval=10, maxval=10000)


Cài đặt và các phương thức đặc biệt
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. function:: mode(mode=None)

   :param mode: một trong các chuỗi "standard", "logo" hoặc "world"

   Đặt chế độ turtle ("standard", "logo" hoặc "world") và thực hiện reset. Nếu không cung cấp mode, trả về mode hiện tại.

   Chế độ "standard" tương thích với :mod:`!turtle` cũ. Chế độ "logo" tương thích với hầu hết đồ họa turtle của Logo. Chế độ "world" sử dụng "tọa độ world" do người dùng định nghĩa. **Lưu ý**: trong chế độ này, các góc sẽ bị méo nếu ``x/y`` unit-ratio không bằng 1.

   +------------+-------------------------+-------------------------+
   | Mode       | Initial turtle heading  | các góc dương           |
   +============+=========================+=========================+
   | "standard" | sang phải (hướng đông)  | ngược chiều kim đồng hồ |
   +------------+-------------------------+-------------------------+
   | "logo"     | lên trên    (hướng bắc) | theo chiều kim đồng hồ  |
   +------------+-------------------------+-------------------------+

   .. doctest::
      :skipif: _tkinter is None

      >>> mode("logo")   # đặt lại hướng của turtle về phía bắc
      >>> mode()
      'logo'


.. function:: colormode(cmode=None)

   :param cmode: một trong hai giá trị 1.0 hoặc 255

   Trả về colormode hoặc đặt nó thành 1.0 hoặc 255. Sau đó, các giá trị *r*, *g*, *b* của các bộ ba màu phải nằm trong phạm vi 0..*cmode*.

   .. doctest::
      :skipif: _tkinter is None

      >>> screen.colormode(1)
      >>> turtle.pencolor(240, 160, 80)
      Traceback (most recent call last):
           ...
      TurtleGraphicsError: bad color sequence: (240, 160, 80)
      >>> screen.colormode()
      1.0
      >>> screen.colormode(255)
      >>> screen.colormode()
      255
      >>> turtle.pencolor(240,160,80)


.. function:: getcanvas()

   Trả về Canvas của TurtleScreen này. Hữu ích cho những người dùng chuyên sâu biết cách làm việc với Tkinter Canvas.

   .. doctest::
      :skipif: _tkinter is None

      >>> cv = screen.getcanvas()
      >>> cv
      <turtle.ScrolledCanvas object ...>


.. function:: getshapes()

   Trả về danh sách tên của tất cả các hình turtle hiện có.

   .. doctest::
      :skipif: _tkinter is None

      >>> screen.getshapes()
      ['arrow', 'blank', 'circle', ..., 'turtle']


.. function:: register_shape(name, shape=None)
              addshape(name, shape=None)

   Có bốn cách khác nhau để gọi hàm này:

   (1) *name* là tên của một tệp hình ảnh (PNG, GIF, PGM và PPM) còn *shape* là ``None``: Cài đặt shape tương ứng của hình ảnh.::

       >>> screen.register_shape("turtle.gif")

       .. note::
          Các shape hình ảnh *không* xoay khi xoay turtle, vì vậy chúng không hiển thị hướng của turtle!

   (2) *name* là một chuỗi tùy ý còn *shape* là tên của một tệp hình ảnh (PNG, GIF, PGM và PPM): Cài đặt shape tương ứng của hình ảnh.::

       >>> screen.register_shape("turtle", "turtle.gif")

       .. note::
          Các shape hình ảnh *không* xoay khi xoay turtle, vì vậy chúng không hiển thị hướng của turtle!

   (3) *name* là một chuỗi tùy ý còn *shape* là một tuple gồm các cặp tọa độ: Cài đặt polygon shape tương ứng.

       .. doctest::
          :skipif: _tkinter is None

          >>> screen.register_shape("triangle", ((5,-3), (0,5), (-5,-3)))

   (4) *name* là một chuỗi tùy ý còn *shape* là một đối tượng :class:`Shape` (compound): Cài đặt compound shape tương ứng.

   Thêm một shape của turtle vào shapelist của TurtleScreen. Chỉ những shape được đăng ký theo cách này mới có thể được sử dụng bằng cách chạy lệnh ``shape(shapename)``.

   .. versionchanged:: 3.14
      Đã thêm hỗ trợ cho các định dạng ảnh PNG, PGM và PPM. Có thể chỉ định cả tên shape và tên tệp ảnh.


.. function:: turtles()

   Trả về danh sách các turtle trên màn hình.

   .. doctest::
      :skipif: _tkinter is None

      >>> for turtle in screen.turtles():
      ...     turtle.color("red")


.. function:: window_height()

   Trả về chiều cao của cửa sổ turtle.::

      >>> screen.window_height()
      480


.. function:: window_width()

   Trả về chiều rộng của cửa sổ turtle.::

      >>> screen.window_width()
      640


.. _screenspecific:
.. _methods-specific-to-screen-not-inherited-from-turtlescreen:

Các phương thức chỉ dành cho Screen
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. function:: bye()

   Đóng cửa sổ turtlegraphics.


.. function:: exitonclick()

   Gắn phương thức ``bye()`` với các lần nhấp chuột trên Screen.


   Nếu giá trị "using_IDLE" trong từ điển cấu hình là ``False`` (giá trị mặc định), cũng đi vào mainloop. Lưu ý: Nếu sử dụng IDLE với switch ``-n`` (không có subprocess), giá trị này nên được đặt thành ``True`` trong
   :file:`turtle.cfg`. Trong trường hợp này, mainloop của chính IDLE cũng hoạt động cho client script.


.. function:: save(filename, overwrite=False)

   Lưu bản vẽ turtle hiện tại (và các turtle) dưới dạng tệp PostScript.

   :param filename: đường dẫn của tệp PostScript đã lưu
   :param overwrite: nếu ``False`` và đã tồn tại một tệp có tên tệp được chỉ định, hàm sẽ raise một ``FileExistsError``. Nếu là ``True``, tệp sẽ bị ghi đè.

   .. doctest::
      :skipif: _tkinter is None

      >>> screen.save("my_drawing.ps")
      >>> screen.save("my_drawing.ps", overwrite=True)

   .. versionadded:: 3.14

.. function:: setup(width=_CFG["width"], height=_CFG["height"], startx=_CFG["leftright"], starty=_CFG["topbottom"])

   Đặt kích thước và vị trí của cửa sổ chính. Giá trị mặc định của các đối số được lưu trong từ điển cấu hình và có thể thay đổi thông qua một
   tệp :file:`turtle.cfg`.

   :param width: nếu là số nguyên, kích thước tính bằng pixel; nếu là số thực, một phần của màn hình; mặc định là 50% màn hình
   :param height: nếu là số nguyên, chiều cao tính bằng pixel; nếu là số thực, một phần của màn hình; mặc định là 75% màn hình
   :param startx: nếu dương, vị trí bắt đầu tính bằng pixel từ mép trái màn hình; nếu âm, tính từ mép phải; nếu ``None``, căn giữa cửa sổ theo chiều ngang
   :param starty: nếu dương, vị trí bắt đầu tính bằng pixel từ mép trên màn hình; nếu âm, tính từ mép dưới; nếu ``None``, căn giữa cửa sổ theo chiều dọc

   .. doctest::
      :skipif: _tkinter is None

      >>> screen.setup (width=200, height=200, startx=0, starty=0)
      >>>              # đặt cửa sổ thành 200x200 pixel ở góc trên bên trái màn hình
      >>> screen.setup(width=.75, height=0.5, startx=None, starty=None)
      >>>              # đặt cửa sổ có kích thước bằng 75% màn hình theo chiều cao và 50% màn hình theo chiều rộng, rồi căn giữa


.. function:: title(titlestring)

   :param titlestring: một chuỗi được hiển thị trên thanh tiêu đề của cửa sổ đồ họa turtle

   Đặt tiêu đề cửa sổ turtle thành *titlestring*.

   .. doctest::
      :skipif: _tkinter is None

      >>> screen.title("Welcome to the turtle zoo!")


Các lớp công khai
-----------------


.. class:: RawTurtle(canvas)
           RawPen(canvas)

   :param canvas: một :class:`!tkinter.Canvas`, một :class:`ScrolledCanvas` hoặc một
                  :class:`TurtleScreen`

   Tạo một turtle. Turtle có tất cả các phương thức được mô tả ở trên dưới dạng "methods of Turtle/RawTurtle".


.. class:: Turtle()

   Lớp con của RawTurtle, có cùng interface nhưng vẽ trên một
   đối tượng :class:`Screen` được tạo tự động khi cần lần đầu tiên.


.. class:: TurtleScreen(cv)

   :param cv: một :class:`!tkinter.Canvas`

   Cung cấp các phương thức định hướng màn hình như :func:`bgcolor` cùng nhiều phương thức khác được mô tả ở trên.

.. class:: Screen()

   Lớp con của TurtleScreen, được bổ sung :ref:`bốn phương thức <screenspecific>`.


.. class:: ScrolledCanvas(master)

   :param master: một widget Tkinter nào đó để chứa ScrolledCanvas, tức là một canvas Tkinter có thêm các thanh cuộn

   Được lớp Screen sử dụng, vì vậy lớp này tự động cung cấp một ScrolledCanvas làm không gian thực hành cho các turtle.

.. class:: Shape(type_, data)

   :param type\_: một trong các chuỗi "polygon", "image", "compound"

   Cấu trúc dữ liệu mô hình hóa các hình dạng. Cặp ``(type_, data)`` phải tuân theo đặc tả sau:


   +------------+------------------------------------------------------------------+
   | *type_*    | *dữ liệu*                                                        |
   +============+==================================================================+
   | "polygon"  | một polygon-tuple, tức là một tuple gồm các cặp tọa độ           |
   +------------+------------------------------------------------------------------+
   | "image"    | một image (ở dạng này chỉ được sử dụng nội bộ!)                  |
   +------------+------------------------------------------------------------------+
   | "compound" | ``None`` (một hình dạng compound phải được tạo bằng cách sử dụng |
   |            | :meth:`addcomponent` phương thức)                                |
   +------------+------------------------------------------------------------------+

   .. method:: addcomponent(poly, fill, outline=None)

      :param poly: một đa giác, tức là một tuple gồm các cặp số
      :param fill: một màu mà *poly* sẽ được tô bằng
      :param outline: một màu cho đường viền của poly (nếu được cung cấp)

      Ví dụ:

      .. doctest::
         :skipif: _tkinter is None

         >>> poly = ((0,0),(10,-5),(0,10),(-10,-5))
         >>> s = Shape("compound")
         >>> s.addcomponent(poly, "red", "blue")
         >>> # ... thêm các component khác rồi sử dụng register_shape()

      Xem :ref:`compoundshapes`.


.. class:: Vec2D(x, y)

   Một lớp vector hai chiều, được dùng làm lớp trợ giúp để triển khai đồ họa turtle. Cũng có thể hữu ích cho các chương trình đồ họa turtle. Được kế thừa từ tuple, vì vậy một vector cũng là một tuple!

   Cung cấp (với các vector *a* và *b*, số *k*):

   * ``a + b`` phép cộng vector
   * ``a - b`` phép trừ vector
   * ``a * b`` tích vô hướng
   * ``k * a`` phép nhân với scalar của a và ``a * k``
   * ``abs(a)`` giá trị tuyệt đối của a
   * ``a.rotate(angle)`` phép xoay


Ngoại lệ
--------

Mô-đun :mod:`!turtle` định nghĩa ngoại lệ sau:

.. exception:: TurtleGraphicsError

   Được phát sinh khi đối số hoặc thao tác không hợp lệ. Ví dụ: một chuỗi màu không đúng định dạng:

   .. doctest::
      :skipif: _tkinter is None

      >>> turtle.color("blau")
      Traceback (most recent call last):
          ...
      turtle.TurtleGraphicsError: bad color string: blau


.. _turtle-howtos:
.. _turtle-how-to:
.. _how-to:

Hướng dẫn thực hiện
===================

Phần này trình bày một số trường hợp sử dụng và cách tiếp cận điển hình với turtle.


Tự động bắt đầu và kết thúc việc tô màu
---------------------------------------

Bắt đầu từ Python 3.14, bạn có thể sử dụng :func:`fill` :term:`context manager` thay cho :func:`begin_fill` và :func:`end_fill` để tự động bắt đầu và kết thúc việc tô. Dưới đây là một ví dụ::

   with fill():
       for i in range(4):
           forward(100)
           right(90)

   forward(200)

Đoạn mã trên tương đương với::

   begin_fill()
   for i in range(4):
       forward(100)
       right(90)
   end_fill()

   forward(200)


Sử dụng không gian tên mô-đun ``turtle``
----------------------------------------

Sử dụng ``from turtle import *`` rất tiện lợi - nhưng hãy lưu ý rằng cách này nhập một tập hợp khá lớn các đối tượng, và nếu bạn làm bất cứ việc gì ngoài đồ họa turtle, bạn có nguy cơ xảy ra xung đột tên (điều này càng đáng lưu ý hơn nếu bạn sử dụng đồ họa turtle trong một script có thể nhập các mô-đun khác).

Giải pháp là sử dụng ``import turtle`` - ``fd()`` trở thành ``turtle.fd()``, ``width()`` trở thành ``turtle.width()`` và cứ tiếp tục như vậy. (Nếu việc gõ "turtle" lặp đi lặp lại trở nên tẻ nhạt, bạn có thể sử dụng chẳng hạn như ``import turtle as t``.)


Sử dụng đồ họa turtle trong một script
--------------------------------------

Bạn nên sử dụng không gian tên mô-đun ``turtle`` như mô tả ngay ở trên, chẳng hạn như::

    import turtle as t
    from random import random

    for i in range(100):
        steps = int(random() * 100)
        angle = int(random() * 360)
        t.right(angle)
        t.fd(steps)

Tuy nhiên, cũng cần thực hiện thêm một bước - ngay khi script kết thúc, Python cũng sẽ đóng cửa sổ turtle. Hãy thêm::

    t.mainloop()

vào cuối script. Giờ đây, script sẽ chờ được đóng và sẽ không thoát cho đến khi bị kết thúc, chẳng hạn bằng cách đóng cửa sổ turtle graphics.


Sử dụng turtle graphics theo hướng đối tượng
--------------------------------------------

.. seealso:: :ref:`Giải thích về interface hướng đối tượng <turtle-explanation>`

Ngoài những mục đích nhập môn rất cơ bản hoặc để thử nghiệm nhanh nhất có thể, cách sử dụng turtle graphics theo hướng đối tượng phổ biến hơn và mạnh mẽ hơn nhiều. Ví dụ, cách này cho phép hiển thị nhiều turtle trên màn hình cùng lúc.

Trong cách tiếp cận này, các lệnh turtle khác nhau là các method của các object (chủ yếu là các object ``Turtle``). Bạn *có thể* sử dụng cách tiếp cận hướng đối tượng trong shell, nhưng cách này thường được dùng hơn trong một Python script.

Khi đó, ví dụ trên sẽ trở thành::

    from turtle import Turtle
    from random import random

    t = Turtle()
    for i in range(100):
        steps = int(random() * 100)
        angle = int(random() * 360)
        t.right(angle)
        t.fd(steps)

    t.screen.mainloop()

Lưu ý dòng cuối cùng. ``t.screen`` là một thể hiện của :class:`Screen` mà một thể hiện Turtle tồn tại trên đó; nó được tự động tạo cùng với turtle.

Màn hình của turtle có thể được tùy chỉnh, chẳng hạn như::

    t.screen.title('Object-oriented turtle demo')
    t.screen.bgcolor("orange")


.. _help-and-configuration:

Cách sử dụng trợ giúp
---------------------

Các phương thức public của các lớp Screen và Turtle được ghi chép đầy đủ qua docstring. Vì vậy, bạn có thể sử dụng chúng làm trợ giúp trực tuyến thông qua các tiện ích help của Python:

- Khi sử dụng IDLE, chú giải công cụ sẽ hiển thị signature và những dòng đầu tiên của docstring trong các lời gọi hàm/phương thức được nhập.

- Gọi :func:`help` trên các phương thức hoặc hàm sẽ hiển thị docstring::

     >>> help(Screen.bgcolor)
     Help on method bgcolor in module turtle:

     bgcolor(self, *args) unbound turtle.Screen method
         Set or return backgroundcolor of the TurtleScreen.

         Arguments (if given): a color string or three numbers
         in the range 0..colormode or a 3-tuple of such numbers.


         >>> screen.bgcolor("orange")
         >>> screen.bgcolor()
         "orange"
         >>> screen.bgcolor(0.5,0,0.5)
         >>> screen.bgcolor()
         "#800080"

     >>> help(Turtle.penup)
     Help on method penup in module turtle:

     penup(self) unbound turtle.Turtle method
         Pull the pen up -- no drawing when moving.

         Aliases: penup | pu | up

         No argument

         >>> turtle.penup()

- Docstring của các hàm được tạo từ các phương thức có dạng đã được sửa đổi::

     >>> help(bgcolor)
     Help on function bgcolor in module turtle:

     bgcolor(*args)
         Set or return backgroundcolor of the TurtleScreen.

         Arguments (if given): a color string or three numbers
         in the range 0..colormode or a 3-tuple of such numbers.

         Example::

           >>> bgcolor("orange")
           >>> bgcolor()
           "orange"
           >>> bgcolor(0.5,0,0.5)
           >>> bgcolor()
           "#800080"

     >>> help(penup)
     Help on function penup in module turtle:

     penup()
         Pull the pen up -- no drawing when moving.

         Aliases: penup | pu | up

         No argument

         Example:
         >>> penup()

Các docstring đã sửa đổi này được tự động tạo cùng với các định nghĩa hàm được suy ra từ các method tại thời điểm import.


Dịch docstring sang các ngôn ngữ khác nhau
------------------------------------------

Có một tiện ích để tạo một dictionary, trong đó các khóa là tên method còn các giá trị là docstring của các method public thuộc các class Screen và Turtle.

.. function:: write_docstringdict(filename="turtle_docstringdict")

   :param filename: một chuỗi, được dùng làm tên tệp

   Tạo và ghi dictionary docstring vào một script Python với tên tệp đã cho. Hàm này phải được gọi một cách tường minh (không được các class turtle graphics sử dụng). Dictionary docstring sẽ được ghi vào script Python :file:`{filename}.py`. Script này nhằm làm mẫu để dịch các docstring sang các ngôn ngữ khác nhau.

Nếu bạn (hoặc học sinh của bạn) muốn sử dụng :mod:`!turtle` với phần trợ giúp trực tuyến bằng ngôn ngữ bản địa của mình, bạn phải dịch các docstring và lưu tệp kết quả, chẳng hạn như :file:`turtle_docstringdict_german.py`.

Nếu có mục nhập phù hợp trong tệp :file:`turtle.cfg` của bạn, dictionary này sẽ được đọc tại thời điểm import và thay thế các docstring tiếng Anh gốc.

Tại thời điểm viết tài liệu này, đã có các từ điển docstring bằng tiếng Đức và tiếng Ý. (Vui lòng gửi yêu cầu đến glingl@aon.at.)



Cách cấu hình Screen và Turtles
-------------------------------

Cấu hình mặc định tích hợp sẵn mô phỏng diện mạo và hành vi của module turtle cũ nhằm duy trì khả năng tương thích tốt nhất có thể với module đó.

Nếu muốn sử dụng một cấu hình khác phản ánh tốt hơn các tính năng của module này hoặc phù hợp hơn với nhu cầu của bạn, chẳng hạn để sử dụng trong lớp học, bạn có thể chuẩn bị một tệp cấu hình ``turtle.cfg``, tệp này sẽ được đọc tại thời điểm import và cấu hình sẽ được điều chỉnh theo các thiết lập trong đó.

Cấu hình tích hợp sẵn tương ứng với ``turtle.cfg`` sau đây:

.. code-block:: ini

   width = 0.5
   height = 0.75
   leftright = None
   topbottom = None
   canvwidth = 400
   canvheight = 300
   mode = standard
   colormode = 1.0
   delay = 10
   undobuffersize = 1000
   shape = classic
   pencolor = black
   fillcolor = black
   resizemode = noresize
   visible = True
   language = english
   exampleturtle = turtle
   examplescreen = screen
   title = Python Turtle Graphics
   using_IDLE = False

Giải thích ngắn gọn về một số mục được chọn:

- Bốn dòng đầu tiên tương ứng với các đối số của phương thức :func:`Screen.setup <setup>`.
- Dòng 5 và 6 tương ứng với các đối số của method
  :func:`Screen.screensize <screensize>`.
- *shape* có thể là bất kỳ shape dựng sẵn nào, ví dụ: arrow, turtle, v.v. Để biết thêm thông tin, hãy thử ``help(shape)``.
- Nếu bạn muốn không sử dụng màu tô (tức là làm cho turtle trong suốt), bạn phải viết ``fillcolor = ""`` (nhưng mọi chuỗi không rỗng đều không được có dấu ngoặc kép trong tệp cfg).
- Nếu bạn muốn phản ánh trạng thái của turtle, bạn phải sử dụng ``resizemode = auto``.
- Nếu bạn đặt, chẳng hạn, ``language = italian`` cho docstringdict
  :file:`turtle_docstringdict_italian.py` sẽ được tải tại thời điểm import (nếu có trong import path, ví dụ: cùng thư mục với :mod:`!turtle`).
- Các mục *exampleturtle* và *examplescreen* xác định tên của các đối tượng này khi chúng xuất hiện trong docstring. Việc chuyển đổi method-docstring thành function-docstring sẽ xóa các tên này khỏi docstring.
- *using_IDLE*: Đặt giá trị này thành ``True`` nếu bạn thường xuyên làm việc với IDLE và switch ``-n`` của nó ("no subprocess"). Điều này sẽ ngăn :func:`exitonclick` đi vào mainloop.

Có thể có một tệp :file:`turtle.cfg` trong thư mục lưu trữ :mod:`!turtle` và một tệp bổ sung trong thư mục làm việc hiện tại. Tệp sau sẽ ghi đè các thiết lập của tệp đầu tiên.

Thư mục :file:`Lib/turtledemo` chứa một tệp :file:`turtle.cfg`. Bạn có thể xem tệp này như một ví dụ và quan sát tác động của nó khi chạy các bản demo (tốt nhất không chạy từ bên trong trình xem demo).


.. _turtle-explanation:

Giải thích
==========

Một đối tượng turtle vẽ trên một đối tượng screen, và có một số lớp then chốt trong interface hướng đối tượng của turtle có thể được dùng để tạo các đối tượng này và thiết lập mối quan hệ giữa chúng.

Một instance :class:`Turtle` sẽ tự động tạo một instance :class:`Screen` nếu chưa có instance nào.

``Turtle`` là một subclass của :class:`RawTurtle`, lớp này *không* tự động tạo drawing surface - cần cung cấp hoặc tạo một *canvas* cho nó. *canvas* có thể là một :class:`!tkinter.Canvas`, :class:`ScrolledCanvas` hoặc :class:`TurtleScreen`.


:class:`TurtleScreen` là bề mặt vẽ cơ bản dành cho turtle. :class:`Screen` là một lớp con của ``TurtleScreen``, đồng thời bao gồm :ref:`một số phương thức bổ sung <screenspecific>` để quản lý giao diện (bao gồm kích thước và tiêu đề) cũng như hành vi của nó. Hàm khởi tạo của ``TurtleScreen`` cần một :class:`!tkinter.Canvas` hoặc
:class:`ScrolledCanvas` làm đối số.

Giao diện hàm dành cho đồ họa turtle sử dụng nhiều phương thức khác nhau của ``Turtle`` và ``TurtleScreen``/``Screen``. Phía sau, một đối tượng screen được tự động tạo mỗi khi một hàm bắt nguồn từ phương thức ``Screen`` được gọi. Tương tự, một đối tượng turtle được tự động tạo mỗi khi bất kỳ hàm nào bắt nguồn từ một phương thức của Turtle được gọi.

Để sử dụng nhiều turtle trên một screen, phải sử dụng giao diện hướng đối tượng.


:mod:`!turtledemo` --- Các tập lệnh minh họa
============================================

.. module:: turtledemo
   :synopsis: Trình xem các tập lệnh turtle mẫu

Gói :mod:`!turtledemo` bao gồm một tập hợp các tập lệnh minh họa. Có thể chạy và xem các tập lệnh này bằng trình xem minh họa được cung cấp như sau::

   python -m turtledemo

Ngoài ra, bạn có thể chạy riêng từng tập lệnh demo. Ví dụ:::

   python -m turtledemo.bytedesign

Thư mục gói :mod:`!turtledemo` chứa:

- Một trình xem demo :file:`__main__.py`, có thể dùng để xem mã nguồn của các tập lệnh và chạy chúng đồng thời.
- Nhiều tập lệnh minh họa các tính năng khác nhau của mô-đun :mod:`!turtle`. Bạn có thể truy cập các ví dụ thông qua menu Examples. Bạn cũng có thể chạy chúng độc lập.
- Một tệp :file:`turtle.cfg`, dùng làm ví dụ về cách viết và sử dụng các tệp như vậy.

Các tập lệnh demo là:

.. currentmodule:: turtle

.. tabularcolumns:: |l|L|L|

+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------+
| Tên                 | Mô tả                                                                                                                                   | Tính năng                                                              |
+=====================+=========================================================================================================================================+========================================================================+
| ``bytedesign``      | mẫu đồ họa turtle cổ điển phức tạp                                                                                                      | :func:`tracer`, :func:`delay`,                                         |
|                     |                                                                                                                                         | :func:`update`                                                         |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------+
| ``chaos``           | mô phỏng động lực học Verhulst, cho thấy các phép tính của máy tính đôi khi có thể tạo ra những kết quả trái với dự đoán theo lẽ thường | tọa độ thế giới                                                        |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------+
| ``clock``           | đồng hồ analog hiển thị thời gian trên máy tính của bạn                                                                                 | các turtle làm kim đồng hồ, :func:`ontimer`                            |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------+
| ``colormixer``      | thử nghiệm với r, g, b                                                                                                                  | :func:`ondrag`                                                         |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------+
| ``forest``          | 3 cây duyệt theo chiều rộng                                                                                                             | ngẫu nhiên hóa                                                         |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------+
| ``fractalcurves``   | đường cong Hilbert & Koch                                                                                                               | đệ quy                                                                 |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------+
| ``lindenmayer``     | toán học dân tộc (kolam Ấn Độ)                                                                                                          | L-System                                                               |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------+
| ``minimal_hanoi``   | Tháp Hà Nội                                                                                                                             | Turtle hình chữ nhật làm đĩa Hà Nội (:func:`shape`, :func:`shapesize`) |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------+
| ``nim``             | chơi trò nim cổ điển với ba đống que đấu với máy tính.                                                                                  | turtle làm que nim, điều khiển theo sự kiện (chuột, bàn phím)          |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------+
| ``paint``           | chương trình vẽ tối giản                                                                                                                | :func:`onclick`                                                        |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------+
| ``peace``           | cơ bản                                                                                                                                  | turtle: diện mạo và hoạt ảnh                                           |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------+
| ``penrose``         | mặt lát tuần hoàn với các hình diều và phi tiêu                                                                                         | :func:`stamp`                                                          |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------+
| ``planet_and_moon`` | mô phỏng hệ hấp dẫn                                                                                                                     | các hình phức hợp,                                                     |
|                     |                                                                                                                                         | :class:`Vec2D`                                                         |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------+
| ``rosette``         | một mẫu từ bài viết Wikipedia về đồ họa turtle                                                                                          | :func:`clone`,                                                         |
|                     |                                                                                                                                         | :func:`undo`                                                           |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------+
| ``round_dance``     | các turtle nhảy múa, xoay theo từng cặp theo hướng ngược nhau                                                                           | các hình phức hợp, :func:`clone`                                       |
|                     |                                                                                                                                         | :func:`shapesize`, :func:`tilt`,                                       |
|                     |                                                                                                                                         | :func:`get_shapepoly`, :func:`update`                                  |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------+
| ``sorting_animate`` | minh họa trực quan các phương pháp sắp xếp khác nhau                                                                                    | căn chỉnh đơn giản, ngẫu nhiên hóa                                     |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------+
| ``tree``            | một cây duyệt theo chiều rộng (dạng đồ họa) (sử dụng generator)                                                                         | :func:`clone`                                                          |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------+
| ``two_canvases``    | thiết kế đơn giản                                                                                                                       | các turtle trên hai canvas                                             |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------+
| ``yinyang``         | một ví dụ cơ bản khác                                                                                                                   | :func:`circle`                                                         |
+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------+

Chúc bạn vui vẻ!


.. doctest::
   :skipif: _tkinter is None
   :hide:

   >>> for turtle in turtles():
   ...      turtle.reset()
   >>> turtle.penup()
   >>> turtle.goto(-200,25)
   >>> turtle.pendown()
   >>> turtle.write("No one expects the Spanish Inquisition!",
   ...      font=("Arial", 20, "normal"))
   >>> turtle.penup()
   >>> turtle.goto(-100,-50)
   >>> turtle.pendown()
   >>> turtle.write("Our two chief Turtles are...",
   ...      font=("Arial", 16, "normal"))
   >>> turtle.penup()
   >>> turtle.goto(-450,-75)
   >>> turtle.write(str(turtles()))
