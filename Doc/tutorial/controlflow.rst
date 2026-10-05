.. _tut-morecontrol:

*********************************
Các công cụ điều khiển luồng khác
*********************************

Ngoài câu lệnh :keyword:`while` vừa được giới thiệu, Python còn sử dụng một vài câu lệnh khác mà chúng ta sẽ gặp trong chương này.


.. _tut-if:

Các câu lệnh :keyword:`!if`
===========================

Có lẽ loại câu lệnh được biết đến nhiều nhất là câu lệnh :keyword:`if`. Ví dụ:::

   >>> x = int(input("Please enter an integer: "))
   Please enter an integer: 42
   >>> if x < 0:
   ...     x = 0
   ...     print('Negative changed to zero')
   ... elif x == 0:
   ...     print('Zero')
   ... elif x == 1:
   ...     print('Single')
   ... else:
   ...     print('More')
   ...
   More

Có thể có không hoặc nhiều phần :keyword:`elif`, còn phần :keyword:`else` là tùy chọn. Từ khóa ':keyword:`!elif`' là dạng viết tắt của 'else if' và hữu ích để tránh thụt lề quá sâu. Một :keyword:`!if` ... :keyword:`!elif` ...
Chuỗi :keyword:`!elif` ... là một cách thay thế cho các câu lệnh ``switch`` hoặc ``case`` trong các ngôn ngữ khác.

Nếu bạn đang so sánh cùng một giá trị với nhiều hằng số hoặc kiểm tra các kiểu hay thuộc tính cụ thể, bạn cũng có thể thấy câu lệnh :keyword:`!match` hữu ích. Để biết thêm chi tiết, hãy xem :ref:`tut-match`.

.. _tut-for:

Câu lệnh :keyword:`!for`
========================

.. index::
   pair: statement; for

Câu lệnh :keyword:`for` trong Python hơi khác so với những gì bạn có thể đã quen dùng trong C hoặc Pascal. Thay vì luôn lặp qua một cấp số cộng các số (như trong Pascal), hoặc cho phép người dùng xác định cả bước lặp và điều kiện dừng (như trong C), câu lệnh :keyword:`!for` của Python lặp qua các phần tử của bất kỳ sequence nào (danh sách hoặc chuỗi), theo đúng thứ tự xuất hiện trong sequence đó. Ví dụ (hoàn toàn không có ý chơi chữ):

.. One suggestion was to give a real C example here, but that may only serve to
   confuse non-C programmers.

::

   >>> # Measure some strings:
   >>> words = ['cat', 'window', 'defenestrate']
   >>> for w in words:
   ...     print(w, len(w))
   ...
   cat 3
   window 6
   defenestrate 12

Mã sửa đổi một collection trong khi đang lặp qua chính collection đó có thể khó triển khai chính xác. Thay vào đó, thường sẽ đơn giản hơn nếu lặp qua một bản sao của collection hoặc tạo một collection mới::

    # Tạo một collection mẫu
    users = {'Hans': 'active', 'Éléonore': 'inactive', '景太郎': 'active'}

    # Chiến lược: Lặp qua một bản sao
    for user, status in users.copy().items():
        if status == 'inactive':
            del users[user]

    # Chiến lược: Tạo một collection mới
    active_users = {}
    for user, status in users.items():
        if status == 'active':
            active_users[user] = status


.. _tut-range:

Hàm :func:`range`
=================

Nếu bạn thực sự cần lặp qua một dãy số, hàm tích hợp sẵn
:func:`range` sẽ rất hữu ích. Hàm này tạo ra các cấp số cộng::

    >>> for i in range(5):
    ...     print(i)
    ...
    0
    1
    2
    3
    4

Điểm cuối đã cho không bao giờ là một phần của dãy được tạo; ``range(10)`` tạo ra 10 giá trị, là các chỉ số hợp lệ cho các phần tử của một dãy có độ dài 10. Bạn có thể để phạm vi bắt đầu từ một số khác hoặc chỉ định một bước tăng khác (kể cả số âm; đôi khi được gọi là 'step')::

    >>> list(range(5, 10))
    [5, 6, 7, 8, 9]

    >>> list(range(0, 10, 3))
    [0, 3, 6, 9]

    >>> list(range(-10, -100, -30))
    [-10, -40, -70]

Để lặp qua các chỉ số của một dãy, bạn có thể kết hợp :func:`range` và
:func:`len` như sau::

   >>> a = ['Mary', 'had', 'a', 'little', 'lamb']
   >>> for i in range(len(a)):
   ...     print(i, a[i])
   ...
   0 Mary
   1 had
   2 a
   3 little
   4 lamb

Tuy nhiên, trong hầu hết các trường hợp như vậy, sẽ thuận tiện hơn khi sử dụng hàm :func:`enumerate`, xem :ref:`tut-loopidioms`.

Một điều kỳ lạ xảy ra nếu bạn chỉ in một range::

   >>> range(10)
   range(0, 10)

Theo nhiều cách, đối tượng được trả về bởi :func:`range` hoạt động như thể nó là một danh sách, nhưng thực tế không phải vậy. Đây là một đối tượng trả về các phần tử liên tiếp của chuỗi mong muốn khi bạn lặp qua nó, nhưng nó không thực sự tạo danh sách, nhờ đó tiết kiệm không gian.

Chúng ta gọi một đối tượng như vậy là :term:`iterable`, nghĩa là nó phù hợp làm đích cho các hàm và cấu trúc cần một đối tượng mà từ đó chúng có thể lấy các phần tử liên tiếp cho đến khi nguồn cung :term:`exhausted`. Chúng ta đã thấy câu lệnh :keyword:`for` là một cấu trúc như vậy, còn một ví dụ về hàm nhận một iterable là :func:`sum`::

    >>> sum(range(4))  # 0 + 1 + 2 + 3
    6

Sau này chúng ta sẽ thấy thêm nhiều hàm trả về iterable và nhận iterable làm đối số. Trong chương :ref:`tut-structures`, chúng ta sẽ thảo luận chi tiết hơn về :func:`list`.

.. _tut-break:

Các câu lệnh :keyword:`!break` và :keyword:`!continue`
======================================================

Câu lệnh :keyword:`break` thoát khỏi vòng lặp bao ngoài gần nhất
vòng lặp :keyword:`for` hoặc :keyword:`while`::

    >>> for n in range(2, 10):
    ...     for x in range(2, n):
    ...         if n % x == 0:
    ...             print(f"{n} equals {x} * {n//x}")
    ...             break
    ...
    4 equals 2 * 2
    6 equals 2 * 3
    8 equals 2 * 4
    9 equals 3 * 3

Câu lệnh :keyword:`continue` tiếp tục với lần lặp tiếp theo của vòng lặp::

    >>> for num in range(2, 10):
    ...     if num % 2 == 0:
    ...         print(f"Found an even number {num}")
    ...         continue
    ...     print(f"Found an odd number {num}")
    ...
    Found an even number 2
    Found an odd number 3
    Found an even number 4
    Found an odd number 5
    Found an even number 6
    Found an odd number 7
    Found an even number 8
    Found an odd number 9

.. _tut-for-else:
.. _break-and-continue-statements-and-else-clauses-on-loops:

:keyword:`!else` Mệnh đề trên vòng lặp
======================================

Trong vòng lặp :keyword:`!for` hoặc :keyword:`!while`, câu lệnh :keyword:`!break` có thể được ghép với mệnh đề :keyword:`!else`. Nếu vòng lặp kết thúc mà không thực thi :keyword:`!break`, mệnh đề :keyword:`!else` sẽ được thực thi.

Trong vòng lặp :keyword:`for`, mệnh đề :keyword:`!else` được thực thi sau khi vòng lặp hoàn tất lần lặp cuối cùng, tức là nếu không xảy ra break.

Trong vòng lặp :keyword:`while`, mệnh đề này được thực thi sau khi điều kiện của vòng lặp trở thành false.

Trong cả hai loại vòng lặp, mệnh đề :keyword:`!else` **không** được thực thi nếu vòng lặp bị kết thúc bởi :keyword:`break`. Tất nhiên, những cách khác để kết thúc vòng lặp sớm, chẳng hạn như :keyword:`return` hoặc một exception được raise, cũng sẽ bỏ qua việc thực thi mệnh đề :keyword:`else`.

Điều này được minh họa trong vòng lặp :keyword:`!for` sau đây, dùng để tìm các số nguyên tố::

   >>> for n in range(2, 10):
   ...     for x in range(2, n):
   ...         if n % x == 0:
   ...             print(n, 'equals', x, '*', n//x)
   ...             break
   ...     else:
   ...         # vòng lặp kết thúc mà không tìm thấy thừa số
   ...         print(n, 'is a prime number')
   ...
   2 is a prime number
   3 is a prime number
   4 equals 2 * 2
   5 is a prime number
   6 equals 2 * 3
   7 is a prime number
   8 equals 2 * 4
   9 equals 3 * 3

(Đúng, đây là đoạn mã chính xác. Hãy nhìn kỹ: mệnh đề ``else`` thuộc về vòng lặp ``for``, **not** câu lệnh ``if``.)

Một cách để hình dung mệnh đề else là tưởng tượng nó được ghép cặp với ``if`` bên trong vòng lặp. Khi vòng lặp thực thi, nó sẽ chạy theo một chuỗi như if/if/if/else. ``if`` nằm bên trong vòng lặp và được gặp nhiều lần. Nếu điều kiện từng đúng, một ``break`` sẽ xảy ra. Nếu điều kiện chưa bao giờ đúng, mệnh đề ``else`` bên ngoài vòng lặp sẽ được thực thi.

Khi được dùng với vòng lặp, mệnh đề ``else`` có nhiều điểm chung hơn với mệnh đề ``else`` của câu lệnh :keyword:`try` so với mệnh đề đó của các câu lệnh ``if``: mệnh đề ``else`` của câu lệnh ``try`` được thực thi khi không xảy ra ngoại lệ, còn mệnh đề ``else`` của vòng lặp được thực thi khi không xảy ra ``break``. Để biết thêm về câu lệnh ``try`` và ngoại lệ, xem :ref:`tut-handling`.

.. index:: single: ...; ellipsis literal
.. _tut-pass:

Câu lệnh :keyword:`!pass`
=========================

Câu lệnh :keyword:`pass` không thực hiện thao tác nào. Câu lệnh này có thể được dùng khi cú pháp yêu cầu một câu lệnh nhưng chương trình không cần thực hiện hành động nào. Ví dụ::

   >>> while True:
   ...     pass  # Chờ bận để bắt ngắt bàn phím (Ctrl+C)
   ...

Cách này thường được dùng để tạo các class tối giản::

   >>> class MyEmptyClass:
   ...     pass
   ...

Một nơi khác có thể sử dụng :keyword:`pass` là làm chỗ giữ chỗ cho phần thân của một hàm hoặc điều kiện khi bạn đang viết mã mới, cho phép bạn tiếp tục suy nghĩ ở mức trừu tượng hơn. :keyword:`!pass` sẽ bị bỏ qua một cách im lặng::

   >>> def initlog(*args):
   ...     pass   # Nhớ triển khai phần này!
   ...

Trong trường hợp cuối cùng này, nhiều người sử dụng literal dấu ba chấm :code:`...` thay vì
:code:`pass`. Cách sử dụng này không có ý nghĩa đặc biệt đối với Python và không thuộc định nghĩa của ngôn ngữ (bạn có thể sử dụng bất kỳ biểu thức hằng nào ở đây), nhưng
:code:`...` cũng thường được sử dụng theo quy ước làm phần thân giữ chỗ. Xem :ref:`bltin-ellipsis-object`.


.. _tut-match:

Các câu lệnh :keyword:`!match`
==============================

Một câu lệnh :keyword:`match` nhận một biểu thức và so sánh giá trị của biểu thức đó với các mẫu liên tiếp được cung cấp trong một hoặc nhiều khối case. Cách này bề ngoài tương tự như câu lệnh switch trong C, Java hoặc JavaScript (và nhiều ngôn ngữ khác), nhưng gần với pattern matching trong các ngôn ngữ như Rust hoặc Haskell hơn. Chỉ mẫu đầu tiên khớp mới được thực thi, và câu lệnh cũng có thể trích xuất các thành phần (phần tử chuỗi hoặc thuộc tính đối tượng) từ giá trị vào các biến. Nếu không có case nào khớp, không nhánh nào được thực thi.

Dạng đơn giản nhất so sánh một giá trị subject với một hoặc nhiều literal::

    def http_error(status):
        match status:
            case 400:
                return "Bad request"
            case 404:
                return "Not found"
            case 418:
                return "I'm a teapot"
            case _:
                return "Something's wrong with the internet"

Lưu ý khối cuối cùng: "tên biến" ``_`` hoạt động như một *wildcard* và không bao giờ không khớp.

Bạn có thể kết hợp một số literal trong cùng một pattern bằng ``|`` ("hoặc")::

            case 401 | 403 | 404:
                return "Not allowed"

Các pattern có thể trông giống như các phép gán unpacking và có thể được dùng để liên kết các biến::

    # điểm là một tuple (x, y)
    match point:
        case (0, 0):
            print("Origin")
        case (0, y):
            print(f"Y={y}")
        case (x, 0):
            print(f"X={x}")
        case (x, y):
            print(f"X={x}, Y={y}")
        case _:
            raise ValueError("Not a point")

Hãy xem xét kỹ phần này! Pattern đầu tiên có hai literal và có thể được xem như phần mở rộng của literal pattern được trình bày ở trên. Nhưng hai pattern tiếp theo kết hợp một literal và một biến, trong đó biến *liên kết* một giá trị từ subject (``point``). Pattern thứ tư nắm bắt hai giá trị, khiến về mặt khái niệm nó tương tự phép gán unpacking ``(x, y) = point``.

Nếu bạn sử dụng các class để cấu trúc dữ liệu, bạn có thể dùng tên class theo sau là danh sách đối số giống với constructor, nhưng có khả năng nắm bắt các thuộc tính vào các biến::

    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    def where_is(point):
        match point:
            case Point(x=0, y=0):
                print("Origin")
            case Point(x=0, y=y):
                print(f"Y={y}")
            case Point(x=x, y=0):
                print(f"X={x}")
            case Point():
                print("Somewhere else")
            case _:
                print("Not a point")

Bạn có thể sử dụng các tham số vị trí với một số lớp dựng sẵn cung cấp thứ tự cho các thuộc tính của chúng (ví dụ: dataclasses). Bạn cũng có thể xác định vị trí cụ thể cho các thuộc tính trong pattern bằng cách đặt thuộc tính đặc biệt ``__match_args__`` trong các lớp của mình. Nếu đặt nó thành ("x", "y"), các pattern sau đều tương đương (và đều liên kết thuộc tính ``y`` với biến ``var``)::

    Point(1, var)
    Point(1, y=var)
    Point(x=1, y=var)
    Point(y=var, x=1)

Một cách được khuyến nghị để đọc các pattern là xem chúng như một dạng mở rộng của nội dung bạn sẽ đặt ở bên trái phép gán, nhằm hiểu biến nào sẽ được gán giá trị nào. Chỉ các tên đứng độc lập (như ``var`` ở trên) mới được câu lệnh match gán giá trị. Tên có dấu chấm (như ``foo.bar``), tên thuộc tính (các ``x=`` và ``y=`` ở trên) hoặc tên lớp (được nhận biết qua "(...)" bên cạnh chúng, như ``Point`` ở trên) không bao giờ được gán giá trị.

Các pattern có thể được lồng nhau tùy ý. Ví dụ, nếu chúng ta có một danh sách ngắn các Point, với ``__match_args__`` được thêm vào, chúng ta có thể so khớp danh sách đó như sau::

    class Point:
        __match_args__ = ('x', 'y')
        def __init__(self, x, y):
            self.x = x
            self.y = y

    match points:
        case []:
            print("No points")
        case [Point(0, 0)]:
            print("The origin")
        case [Point(x, y)]:
            print(f"Single point {x}, {y}")
        case [Point(0, y1), Point(0, y2)]:
            print(f"Two on the Y axis at {y1}, {y2}")
        case _:
            print("Something else")

Chúng ta có thể thêm mệnh đề ``if`` vào một pattern, được gọi là "guard". Nếu guard có giá trị false, ``match`` sẽ tiếp tục thử khối case tiếp theo. Lưu ý rằng việc capture giá trị diễn ra trước khi guard được đánh giá::

    match point:
        case Point(x, y) if x == y:
            print(f"Y=X at {x}")
        case Point(x, y):
            print(f"Not on the diagonal")

Một số tính năng quan trọng khác của câu lệnh này:

- Giống như phép gán unpacking, các pattern tuple và list có chính xác cùng ý nghĩa và thực tế sẽ khớp với các sequence tùy ý. Một ngoại lệ quan trọng là chúng không khớp với iterator hoặc string.

- Các pattern sequence hỗ trợ extended unpacking: ``[x, y, *rest]`` và ``(x, y, *rest)`` hoạt động tương tự như trong phép gán unpacking. Tên sau ``*`` cũng có thể là ``_``, vì vậy ``(x, y, *_)`` sẽ khớp với một sequence có ít nhất hai phần tử mà không liên kết các phần tử còn lại.

- Các mẫu ánh xạ (mapping pattern): ``{"bandwidth": b, "latency": l}`` lấy các giá trị ``"bandwidth"`` và ``"latency"`` từ một dictionary. Khác với các mẫu chuỗi (sequence pattern), những khóa thừa sẽ bị bỏ qua. Cú pháp unpacking như ``**rest`` cũng được hỗ trợ. (Tuy nhiên, ``**_`` sẽ là dư thừa nên không được phép.)

- Có thể capture các subpattern bằng từ khóa ``as``::

      case (Point(x1, y1), Point(x2, y2) as p2): ...

  will capture the second element of the input as ``p2`` (as long as the input is
  a sequence of two points)

- Hầu hết các literal được so sánh bằng phép so sánh bằng, tuy nhiên các singleton ``True``, ``False`` và ``None`` được so sánh bằng identity.

- Các pattern có thể sử dụng các hằng số có tên. Những hằng số này phải là các tên có dấu chấm để tránh bị diễn giải thành các biến capture::

      from enum import Enum
      class Color(Enum):
          RED = 'red'
          GREEN = 'green'
          BLUE = 'blue'

      color = Color(input("Enter your choice of 'red', 'blue' or 'green': "))

      match color:
          case Color.RED:
              print("I see red!")
          case Color.GREEN:
              print("Grass is green")
          case Color.BLUE:
              print("I'm feeling the blues :(")

Để xem phần giải thích chi tiết hơn và các ví dụ bổ sung, bạn có thể xem
:pep:`636` được viết theo dạng hướng dẫn.

.. _tut-functions:

Định nghĩa các hàm
==================

Chúng ta có thể tạo một hàm ghi dãy Fibonacci đến một giới hạn tùy ý::

   >>> def fib(n):    # ghi dãy Fibonacci nhỏ hơn n
   ...     """Print a Fibonacci series less than n."""
   ...     a, b = 0, 1
   ...     while a < n:
   ...         print(a, end=' ')
   ...         a, b = b, a+b
   ...     print()
   ...
   >>> # Bây giờ hãy gọi hàm chúng ta vừa định nghĩa:
   >>> fib(2000)
   0 1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597

.. index::
   single: documentation strings
   single: docstrings
   single: strings, documentation

Từ khóa :keyword:`def` giới thiệu *định nghĩa* một hàm. Từ khóa này phải được theo sau bởi tên hàm và danh sách các tham số hình thức đặt trong dấu ngoặc đơn. Các câu lệnh tạo thành thân hàm bắt đầu từ dòng tiếp theo và phải được thụt lề.

Câu lệnh đầu tiên trong phần thân hàm có thể tùy chọn là một chuỗi ký tự; chuỗi ký tự này là chuỗi tài liệu của hàm, hay còn gọi là :dfn:`docstring`. (Bạn có thể tìm thêm thông tin về docstring trong phần :ref:`tut-docstrings`.) Có những công cụ sử dụng docstring để tự động tạo tài liệu trực tuyến hoặc tài liệu in, hoặc cho phép người dùng duyệt mã tương tác; việc đưa docstring vào mã bạn viết là một thực hành tốt, vì vậy hãy tạo thói quen này.

Việc *thực thi* một hàm tạo ra một bảng ký hiệu mới được dùng cho các biến cục bộ của hàm. Cụ thể hơn, mọi phép gán biến trong một hàm đều lưu giá trị vào bảng ký hiệu cục bộ; trong khi đó, các tham chiếu biến trước tiên tìm trong bảng ký hiệu cục bộ, sau đó trong các bảng ký hiệu cục bộ của những hàm bao quanh, tiếp theo trong bảng ký hiệu toàn cục và cuối cùng trong bảng các tên dựng sẵn. Vì vậy, các biến toàn cục và biến của những hàm bao quanh không thể được gán giá trị trực tiếp bên trong một hàm (trừ khi các biến toàn cục được nêu trong câu lệnh :keyword:`global`, hoặc các biến của những hàm bao quanh được nêu trong câu lệnh :keyword:`nonlocal`), mặc dù chúng có thể được tham chiếu.

Các tham số thực tế (đối số) của một lần gọi hàm được đưa vào bảng ký hiệu cục bộ của hàm được gọi khi hàm đó được gọi; do đó, các đối số được truyền bằng *tham trị* (trong đó *giá trị* luôn là một *tham chiếu* đến đối tượng, chứ không phải giá trị của đối tượng). [#]_ Khi một hàm gọi một hàm khác hoặc tự gọi đệ quy, một bảng ký hiệu cục bộ mới sẽ được tạo cho lần gọi đó.

Một định nghĩa hàm liên kết tên hàm với đối tượng hàm trong bảng ký hiệu hiện tại. Trình thông dịch nhận diện đối tượng được tên đó trỏ tới là một hàm do người dùng định nghĩa. Các tên khác cũng có thể trỏ tới cùng đối tượng hàm đó và cũng có thể được dùng để truy cập hàm::

   >>> fib
   <function fib at 10042ed0>
   >>> f = fib
   >>> f(100)
   0 1 1 2 3 5 8 13 21 34 55 89

Nếu đến từ các ngôn ngữ khác, bạn có thể phản đối rằng ``fib`` không phải là một hàm mà là một thủ tục vì nó không trả về giá trị. Thực tế, ngay cả các hàm không có một
câu lệnh :keyword:`return` cũng trả về một giá trị, dù khá đơn điệu. Giá trị này được gọi là ``None`` (đây là một tên dựng sẵn). Thông thường, trình thông dịch sẽ không hiển thị giá trị ``None`` nếu đó là giá trị duy nhất được hiển thị. Bạn có thể xem giá trị này nếu thực sự muốn bằng cách sử dụng :func:`print`::

   >>> fib(0)
   >>> print(fib(0))
   None

Việc viết một hàm trả về một danh sách các số trong dãy Fibonacci thay vì in dãy đó ra rất đơn giản::

   >>> def fib2(n):  # trả về dãy Fibonacci đến n
   ...     """Return a list containing the Fibonacci series up to n."""
   ...     result = []
   ...     a, b = 0, 1
   ...     while a < n:
   ...         result.append(a)    # xem bên dưới
   ...         a, b = b, a+b
   ...     return result
   ...
   >>> f100 = fib2(100)    # gọi nó
   >>> f100                # ghi kết quả
   [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

Ví dụ này, như thường lệ, minh họa một số tính năng mới của Python:

* Câu lệnh :keyword:`return` trả về một giá trị từ một hàm.
  :keyword:`!return` không có đối số biểu thức sẽ trả về ``None``. Khi chạy đến cuối hàm cũng sẽ trả về ``None``.

* Câu lệnh ``result.append(a)`` gọi *method* của đối tượng danh sách ``result``. Một method là một hàm “thuộc về” một đối tượng và được đặt tên là ``obj.methodname``, trong đó ``obj`` là một đối tượng nào đó (có thể là một biểu thức), còn ``methodname`` là tên của một method được định nghĩa bởi kiểu của đối tượng. Các kiểu khác nhau định nghĩa các method khác nhau. Các method thuộc những kiểu khác nhau có thể có cùng tên mà không gây ra sự mơ hồ. (Bạn có thể định nghĩa các kiểu đối tượng và method của riêng mình bằng cách sử dụng *classes*, xem :ref:`tut-classes`) Method :meth:`~list.append` được minh họa trong ví dụ được định nghĩa cho các đối tượng danh sách; nó thêm một phần tử mới vào cuối danh sách. Trong ví dụ này, nó tương đương với ``result = result + [a]``, nhưng hiệu quả hơn.


.. _tut-defining:

Tìm hiểu thêm về Defining Functions
===================================

Bạn cũng có thể định nghĩa các hàm với số lượng đối số thay đổi. Có ba dạng và chúng có thể được kết hợp với nhau.


.. _tut-defaultargs:

Giá trị mặc định của đối số
---------------------------

Cách hữu ích nhất là chỉ định một giá trị mặc định cho một hoặc nhiều đối số. Điều này tạo ra một hàm có thể được gọi với ít đối số hơn số đối số mà hàm được định nghĩa để chấp nhận. Ví dụ:::

   def ask_ok(prompt, retries=4, reminder='Please try again!'):
       while True:
           reply = input(prompt)
           if reply in {'y', 'ye', 'yes'}:
               return True
           if reply in {'n', 'no', 'nop', 'nope'}:
               return False
           retries = retries - 1
           if retries < 0:
               raise ValueError('invalid user response')
           print(reminder)

Hàm này có thể được gọi theo một số cách:

* chỉ cung cấp đối số bắt buộc: ``ask_ok('Do you really want to quit?')``
* cung cấp một trong các đối số tùy chọn: ``ask_ok('OK to overwrite the file?', 2)``
* hoặc thậm chí cung cấp tất cả các đối số: ``ask_ok('OK to overwrite the file?', 2, 'Come on, only yes or no!')``

Ví dụ này cũng giới thiệu từ khóa :keyword:`in`. Từ khóa này kiểm tra xem một sequence có chứa một giá trị nhất định hay không.

Các giá trị mặc định được đánh giá tại thời điểm định nghĩa hàm trong phạm vi *định nghĩa*, vì vậy::

   i = 5

   def f(arg=i):
       print(arg)

   i = 6
   f()

sẽ in ra ``5``.

**Cảnh báo quan trọng:** Giá trị mặc định chỉ được đánh giá một lần. Điều này tạo ra khác biệt khi giá trị mặc định là một đối tượng có thể thay đổi, chẳng hạn như list, dictionary hoặc các thể hiện của hầu hết các lớp. Ví dụ, hàm sau đây sẽ tích lũy các đối số được truyền vào trong những lần gọi tiếp theo::

   def f(a, L=[]):
       L.append(a)
       return L

   print(f(1))
   print(f(2))
   print(f(3))

Lệnh này sẽ in ra::

   [1]
   [1, 2]
   [1, 2, 3]

Nếu bạn không muốn giá trị mặc định được dùng chung giữa các lần gọi tiếp theo, bạn có thể viết hàm như sau::

   def f(a, L=None):
       if L is None:
           L = []
       L.append(a)
       return L


.. _tut-keywordargs:

Đối số từ khóa
--------------

Các hàm cũng có thể được gọi bằng :term:`đối số từ khóa <keyword argument>` có dạng ``kwarg=value``. Ví dụ, hàm sau đây::

   def parrot(voltage, state='a stiff', action='voom', type='Norwegian Blue'):
       print("-- This parrot wouldn't", action, end=' ')
       print("if you put", voltage, "volts through it.")
       print("-- Lovely plumage, the", type)
       print("-- It's", state, "!")

chấp nhận một đối số bắt buộc (``voltage``) và ba đối số tùy chọn (``state``, ``action`` và ``type``). Hàm này có thể được gọi theo bất kỳ cách nào sau đây::

   parrot(1000)                                          # 1 đối số vị trí
   parrot(voltage=1000)                                  # 1 đối số từ khóa
   parrot(voltage=1000000, action='VOOOOOM')             # 2 đối số từ khóa
   parrot(action='VOOOOOM', voltage=1000000)             # 2 đối số từ khóa
   parrot('a million', 'bereft of life', 'jump')         # 3 đối số vị trí
   parrot('a thousand', state='pushing up the daisies')  # 1 đối số vị trí, 1 đối số từ khóa

nhưng tất cả các lệnh gọi sau đây đều không hợp lệ::

   parrot()                     # thiếu đối số bắt buộc
   parrot(voltage=5.0, 'dead')  # đối số không phải keyword đứng sau đối số keyword
   parrot(110, voltage=220)     # giá trị trùng lặp cho cùng một đối số
   parrot(actor='John Cleese')  # đối số keyword không xác định

Trong một lệnh gọi hàm, các đối số keyword phải đứng sau các đối số vị trí. Tất cả đối số keyword được truyền vào phải khớp với một trong các đối số mà hàm chấp nhận (ví dụ: ``actor`` không phải là đối số hợp lệ cho hàm ``parrot``), và thứ tự của chúng không quan trọng. Điều này cũng bao gồm các đối số không tùy chọn (ví dụ: ``parrot(voltage=1000)`` cũng hợp lệ). Không đối số nào được nhận giá trị nhiều hơn một lần. Dưới đây là một ví dụ không thành công do quy tắc hạn chế này::

   >>> def function(a):
   ...     pass
   ...
   >>> function(0, a=0)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: function() got multiple values for argument 'a'

Khi có một tham số hình thức cuối cùng có dạng ``**name``, tham số này sẽ nhận một dictionary (xem :ref:`typesmapping`) chứa tất cả đối số keyword, ngoại trừ những đối số tương ứng với một tham số hình thức. Tham số này có thể được kết hợp với một tham số hình thức có dạng ``*name`` (được mô tả trong tiểu mục tiếp theo), tham số này nhận một :ref:`tuple <tut-tuples>` chứa các đối số vị trí nằm ngoài danh sách tham số hình thức. (``*name`` phải xuất hiện trước ``**name``.) Ví dụ: nếu chúng ta định nghĩa một hàm như sau::

   def cheeseshop(kind, *arguments, **keywords):
       print("-- Do you have any", kind, "?")
       print("-- I'm sorry, we're all out of", kind)
       for arg in arguments:
           print(arg)
       print("-" * 40)
       for kw in keywords:
           print(kw, ":", keywords[kw])

Có thể gọi hàm như sau::

   cheeseshop("Limburger", "It's very runny, sir.",
              "It's really very, VERY runny, sir.",
              shopkeeper="Michael Palin",
              client="John Cleese",
              sketch="Cheese Shop Sketch")

và tất nhiên, kết quả in ra sẽ là:

.. code-block:: none

   -- Do you have any Limburger ?
   -- I'm sorry, we're all out of Limburger
   It's very runny, sir.
   It's really very, VERY runny, sir.
   ----------------------------------------
   shopkeeper : Michael Palin
   client : John Cleese
   sketch : Cheese Shop Sketch

Lưu ý rằng thứ tự in các đối số từ khóa được đảm bảo khớp với thứ tự chúng được cung cấp trong lệnh gọi hàm.

Các tham số đặc biệt
--------------------

Theo mặc định, các đối số có thể được truyền vào một hàm Python theo vị trí hoặc chỉ rõ bằng từ khóa. Để dễ đọc và đạt hiệu năng tốt hơn, việc giới hạn cách truyền đối số là hợp lý, để nhà phát triển chỉ cần xem định nghĩa hàm là có thể xác định các mục được truyền theo vị trí, theo vị trí hoặc từ khóa, hay theo từ khóa.

Một định nghĩa hàm có thể có dạng:

.. code-block:: none

   def f(pos1, pos2, /, pos_or_kwd, *, kwd1, kwd2):
         -----------    ----------     ----------
           |             |                  |
           |        Positional or keyword   |
           |                                - Keyword only
            -- Positional only

trong đó ``/`` và ``*`` là tùy chọn. Nếu được sử dụng, các ký hiệu này cho biết loại tham số dựa trên cách các đối số có thể được truyền vào hàm: chỉ theo vị trí, theo vị trí hoặc từ khóa, và chỉ theo từ khóa. Các tham số từ khóa còn được gọi là tham số có tên.

------------------------------------
Đối số theo vị trí hoặc theo từ khóa
------------------------------------

Nếu ``/`` và ``*`` không xuất hiện trong định nghĩa hàm, đối số có thể được truyền vào hàm theo vị trí hoặc theo từ khóa.

-----------------------
Tham số chỉ theo vị trí
-----------------------

Xem xét chi tiết hơn, bạn có thể đánh dấu một số tham số là *chỉ theo vị trí*. Nếu *chỉ theo vị trí*, thứ tự của các tham số rất quan trọng và không thể truyền các tham số bằng từ khóa. Các tham số chỉ theo vị trí được đặt trước ``/`` (dấu gạch chéo). ``/`` được dùng để phân tách về mặt logic các tham số chỉ theo vị trí với các tham số còn lại. Nếu không có ``/`` trong định nghĩa hàm, sẽ không có tham số chỉ theo vị trí.

Các tham số đứng sau ``/`` có thể là *theo vị trí hoặc theo từ khóa* hoặc *chỉ theo từ khóa*.

-----------------------
Đối số chỉ theo từ khóa
-----------------------

Để đánh dấu các tham số là *chỉ theo từ khóa*, cho biết rằng các tham số phải được truyền bằng đối số từ khóa, hãy đặt một ``*`` trong danh sách đối số, ngay trước tham số *chỉ theo từ khóa* đầu tiên.

------------
Ví dụ về hàm
------------

Hãy xem xét các định nghĩa hàm sau đây, đặc biệt chú ý đến các dấu đánh dấu ``/`` và ``*``::

   >>> def standard_arg(arg):
   ...     print(arg)
   ...
   >>> def pos_only_arg(arg, /):
   ...     print(arg)
   ...
   >>> def kwd_only_arg(*, arg):
   ...     print(arg)
   ...
   >>> def combined_example(pos_only, /, standard, *, kwd_only):
   ...     print(pos_only, standard, kwd_only)


Định nghĩa hàm đầu tiên, ``standard_arg``, là dạng quen thuộc nhất, không áp đặt hạn chế nào đối với quy ước gọi hàm, và các đối số có thể được truyền theo vị trí hoặc theo từ khóa::

   >>> standard_arg(2)
   2

   >>> standard_arg(arg=2)
   2

Hàm thứ hai ``pos_only_arg`` chỉ bị giới hạn ở việc sử dụng các tham số theo vị trí, vì có một ``/`` trong định nghĩa hàm::

   >>> pos_only_arg(1)
   1

   >>> pos_only_arg(arg=1)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: pos_only_arg() got some positional-only arguments passed as keyword arguments: 'arg'

Hàm thứ ba ``kwd_only_arg`` chỉ cho phép các đối số theo từ khóa, như được chỉ ra bởi một ``*`` trong định nghĩa hàm::

   >>> kwd_only_arg(3)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: kwd_only_arg() takes 0 positional arguments but 1 was given

   >>> kwd_only_arg(arg=3)
   3

Và hàm cuối cùng sử dụng cả ba quy ước gọi hàm trong cùng một định nghĩa hàm::

   >>> combined_example(1, 2, 3)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: combined_example() takes 2 positional arguments but 3 were given

   >>> combined_example(1, 2, kwd_only=3)
   1 2 3

   >>> combined_example(1, standard=2, kwd_only=3)
   1 2 3

   >>> combined_example(pos_only=1, standard=2, kwd_only=3)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: combined_example() got some positional-only arguments passed as keyword arguments: 'pos_only'


Cuối cùng, hãy xem xét định nghĩa hàm này, trong đó có khả năng xảy ra xung đột giữa đối số theo vị trí ``name`` và ``**kwds``, vốn có ``name`` làm khóa::

    def foo(name, **kwds):
        return 'name' in kwds

Không có cách gọi nào có thể khiến nó trả về ``True``, vì từ khóa ``'name'`` sẽ luôn liên kết với tham số đầu tiên. Ví dụ::

    >>> foo(1, **{'name': 2})
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: foo() got multiple values for argument 'name'
    >>>

Nhưng khi sử dụng ``/`` (các đối số chỉ theo vị trí), điều này là khả thi vì nó cho phép ``name`` làm đối số theo vị trí và ``'name'`` làm khóa trong các đối số từ khóa::

    >>> def foo(name, /, **kwds):
    ...     return 'name' in kwds
    ...
    >>> foo(1, **{'name': 2})
    True

Nói cách khác, tên của các tham số chỉ theo vị trí có thể được sử dụng trong ``**kwds`` mà không gây mơ hồ.

-------
Tóm tắt
-------

Trường hợp sử dụng sẽ quyết định nên dùng tham số nào trong định nghĩa hàm::

   def f(pos1, pos2, /, pos_or_kwd, *, kwd1, kwd2):

Hướng dẫn:

* Sử dụng các tham số chỉ theo vị trí nếu bạn không muốn tên của các tham số được cung cấp cho người dùng. Điều này hữu ích khi tên tham số không có ý nghĩa thực sự, khi bạn muốn bắt buộc thứ tự của các đối số lúc gọi hàm hoặc khi bạn cần nhận một số tham số theo vị trí và các từ khóa tùy ý.
* Dùng keyword-only khi tên có ý nghĩa và việc khai báo hàm sẽ dễ hiểu hơn nếu nêu rõ tên, hoặc khi bạn muốn ngăn người dùng dựa vào vị trí của đối số được truyền vào.
* Đối với một API, hãy dùng positional-only để ngăn các thay đổi API gây lỗi nếu tên tham số được sửa đổi trong tương lai.

.. _tut-arbitraryargs:

Danh sách đối số tùy ý
----------------------

.. index::
   single: * (asterisk); in function calls

Cuối cùng, tùy chọn ít được sử dụng nhất là chỉ định rằng một hàm có thể được gọi với một số lượng đối số tùy ý. Các đối số này sẽ được gói vào một tuple (xem :ref:`tut-tuples`). Trước số lượng đối số thay đổi, có thể có không hoặc một vài đối số thông thường.::

   def write_multiple_items(file, separator, *args):
       file.write(separator.join(args))


Thông thường, các đối số *variadic* này sẽ ở cuối danh sách tham số hình thức, vì chúng thu nhận tất cả các đối số đầu vào còn lại được truyền vào hàm. Bất kỳ tham số hình thức nào xuất hiện sau tham số ``*args`` đều là đối số 'keyword-only', nghĩa là chúng chỉ có thể được sử dụng dưới dạng keyword thay vì đối số vị trí.::

   >>> def concat(*args, sep="/"):
   ...     return sep.join(args)
   ...
   >>> concat("earth", "mars", "venus")
   'earth/mars/venus'
   >>> concat("earth", "mars", "venus", sep=".")
   'earth.mars.venus'

.. _tut-unpacking-arguments:

Giải nén danh sách đối số
-------------------------

Tình huống ngược lại xảy ra khi các đối số đã nằm trong một list hoặc tuple nhưng cần được giải nén để gọi một hàm yêu cầu các đối số vị trí riêng biệt. Ví dụ, hàm tích hợp sẵn :func:`range` yêu cầu các đối số *start* và *stop* riêng biệt. Nếu chúng không có sẵn một cách riêng biệt, hãy viết lệnh gọi hàm với ``*``\ -operator để giải nén các đối số từ một list hoặc tuple::

   >>> list(range(3, 6))            # lời gọi thông thường với các đối số riêng biệt
   [3, 4, 5]
   >>> args = [3, 6]
   >>> list(range(*args))            # lời gọi với các đối số được giải nén từ một danh sách
   [3, 4, 5]

.. index::
   single: **; in function calls

Tương tự, các dictionary có thể cung cấp các đối số từ khóa bằng toán tử ``**``\ ::

   >>> def parrot(voltage, state='a stiff', action='voom'):
   ...     print("-- This parrot wouldn't", action, end=' ')
   ...     print("if you put", voltage, "volts through it.", end=' ')
   ...     print("E's", state, "!")
   ...
   >>> d = {"voltage": "four million", "state": "bleedin' demised", "action": "VOOM"}
   >>> parrot(**d)
   -- This parrot wouldn't VOOM if you put four million volts through it. E's bleedin' demised !


.. _tut-lambda:

Biểu thức Lambda
----------------

Có thể tạo các hàm ẩn danh nhỏ bằng từ khóa :keyword:`lambda`. Hàm này trả về tổng của hai đối số: ``lambda a, b: a+b``. Các hàm lambda có thể được sử dụng ở bất cứ nơi nào cần các đối tượng hàm. Chúng bị giới hạn về mặt cú pháp ở một biểu thức duy nhất. Về ngữ nghĩa, chúng chỉ là cú pháp rút gọn cho một định nghĩa hàm thông thường. Giống như các định nghĩa hàm lồng nhau, các hàm lambda có thể tham chiếu đến các biến từ phạm vi chứa chúng::

   >>> def make_incrementor(n):
   ...     return lambda x: x + n
   ...
   >>> f = make_incrementor(42)
   >>> f(0)
   42
   >>> f(1)
   43

Ví dụ trên sử dụng một biểu thức lambda để trả về một hàm. Một cách sử dụng khác là truyền một hàm nhỏ làm đối số. Chẳng hạn, :meth:`list.sort` nhận một hàm khóa sắp xếp *key*, có thể là một hàm lambda::

   >>> pairs = [(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]
   >>> pairs.sort(key=lambda pair: pair[1])
   >>> pairs
   [(4, 'four'), (1, 'one'), (3, 'three'), (2, 'two')]


.. _tut-docstrings:

Chuỗi tài liệu
--------------

.. index::
   single: docstrings
   single: documentation strings
   single: strings, documentation

Sau đây là một số quy ước về nội dung và định dạng của chuỗi tài liệu.

Dòng đầu tiên luôn phải là bản tóm tắt ngắn gọn về mục đích của đối tượng. Để ngắn gọn, dòng này không nên nêu rõ tên hoặc kiểu của đối tượng, vì các thông tin đó có thể được biết bằng những cách khác (trừ khi tên tình cờ là một động từ mô tả thao tác của một hàm). Dòng này phải bắt đầu bằng chữ in hoa và kết thúc bằng dấu chấm.

Nếu chuỗi tài liệu có nhiều dòng hơn, dòng thứ hai phải để trống nhằm tách biệt về mặt hiển thị phần tóm tắt với phần mô tả còn lại. Các dòng tiếp theo phải gồm một hoặc nhiều đoạn mô tả quy ước gọi đối tượng, các tác dụng phụ của đối tượng, v.v.

Trình phân tích cú pháp Python loại bỏ thụt lề khỏi các string literal nhiều dòng khi chúng được dùng làm docstring của module, class hoặc function.

Sau đây là một ví dụ về docstring nhiều dòng::

   >>> def my_function():
   ...     """Do nothing, but document it.
   ...
   ...     No, really, it doesn't do anything:
   ...
   ...         >>> my_function()
   ...         >>>
   ...     """
   ...     pass
   ...
   >>> print(my_function.__doc__)
   Do nothing, but document it.

   No, really, it doesn't do anything:

       >>> my_function()
       >>>


.. _tut-annotations:

Chú thích hàm
-------------

.. sectionauthor:: Zachary Ware <zachary.ware@gmail.com>
.. index::
   pair: function; annotations
   single: ->; function annotations
   single: : (colon); function annotations

:ref:`Chú thích hàm <function>` là thông tin metadata hoàn toàn tùy chọn về các kiểu được sử dụng bởi các hàm do người dùng định nghĩa (xem :pep:`3107` và
:pep:`484` để biết thêm thông tin).

:term:`Các annotation <function annotation>` được lưu trong thuộc tính :attr:`~object.__annotations__` của hàm dưới dạng một dictionary và không ảnh hưởng đến bất kỳ phần nào khác của hàm. Annotation của tham số được định nghĩa bằng dấu hai chấm sau tên tham số, tiếp theo là một biểu thức đánh giá thành giá trị của annotation. Annotation giá trị trả về được định nghĩa bằng một ``->`` literal, tiếp theo là một biểu thức, nằm giữa danh sách tham số và dấu hai chấm đánh dấu phần kết thúc của câu lệnh :keyword:`def`. Ví dụ sau có một đối số bắt buộc, một đối số tùy chọn và giá trị trả về được chú thích::

   >>> def f(ham: str, eggs: str = 'eggs') -> str:
   ...     print("Annotations:", f.__annotations__)
   ...     print("Arguments:", ham, eggs)
   ...     return ham + ' and ' + eggs
   ...
   >>> f('spam')
   Annotations: {'ham': <class 'str'>, 'return': <class 'str'>, 'eggs': <class 'str'>}
   Arguments: spam eggs
   'spam and eggs'

.. _tut-codingstyle:

Xen kẽ: Phong cách viết mã
==========================

.. sectionauthor:: Georg Brandl <georg@python.org>
.. index:: pair: coding; style

Giờ đây, khi bạn sắp viết những phần Python dài hơn và phức tạp hơn, đây là lúc thích hợp để nói về *phong cách viết mã*. Hầu hết các ngôn ngữ đều có thể được viết (hay nói ngắn gọn hơn là *định dạng*) theo nhiều phong cách khác nhau; một số phong cách dễ đọc hơn những phong cách khác. Việc giúp người khác dễ đọc mã của bạn luôn là một ý hay, và áp dụng một phong cách viết mã tốt sẽ hỗ trợ rất nhiều cho điều đó.

Đối với Python, :pep:`8` đã trở thành hướng dẫn về phong cách mà hầu hết các dự án đều tuân theo; hướng dẫn này khuyến khích một phong cách viết mã rất dễ đọc và đẹp mắt. Mọi Python developer nên đọc tài liệu này vào một thời điểm nào đó; dưới đây là những điểm quan trọng nhất được trích ra cho bạn:

* Sử dụng thụt lề 4 dấu cách, không sử dụng tab.

  4 dấu cách là sự cân bằng hợp lý giữa thụt lề ít (cho phép lồng nhau ở độ sâu lớn hơn) và thụt lề nhiều (dễ đọc hơn). Tab gây nhầm lẫn và tốt nhất nên tránh sử dụng.

* Ngắt dòng sao cho mỗi dòng không vượt quá 79 ký tự.

  Điều này giúp người dùng có màn hình nhỏ dễ đọc hơn và cho phép hiển thị nhiều tệp mã cạnh nhau trên các màn hình lớn.

* Dùng các dòng trống để phân tách các hàm và lớp, cũng như các khối mã lớn hơn bên trong hàm.

* Khi có thể, hãy đặt chú thích trên một dòng riêng.

* Sử dụng docstring.

* Dùng khoảng trắng xung quanh các toán tử và sau dấu phẩy, nhưng không đặt khoảng trắng ngay bên trong các cấu trúc dấu ngoặc: ``a = f(1, 2) + g(3, 4)``.

* Đặt tên cho các lớp và hàm một cách nhất quán; quy ước là dùng ``UpperCamelCase`` cho các lớp và ``lowercase_with_underscores`` cho các hàm và phương thức. Luôn dùng ``self`` làm tên cho đối số phương thức đầu tiên (xem :ref:`tut-firstclasses` để biết thêm về các lớp và phương thức).

* Đừng sử dụng các encoding cầu kỳ nếu code của bạn được dùng trong môi trường quốc tế. Encoding mặc định của Python, UTF-8 hoặc thậm chí ASCII thuần túy đều hoạt động tốt trong mọi trường hợp.

* Tương tự, đừng sử dụng các ký tự không thuộc ASCII trong identifier nếu chỉ có một chút khả năng những người nói ngôn ngữ khác sẽ đọc hoặc bảo trì code.


.. rubric:: Chú thích cuối trang

.. [#] Thực ra, *truyền đối tượng theo tham chiếu* sẽ là cách mô tả chính xác hơn, vì nếu một đối tượng có thể thay đổi được được truyền vào, bên gọi sẽ thấy mọi thay đổi mà bên được gọi thực hiện đối với nó (các phần tử được chèn vào một danh sách).
