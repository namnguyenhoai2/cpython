.. _argparse-tutorial:

*********************
Hướng dẫn về Argparse
*********************

:author: Tshepang Mbambo

.. currentmodule:: argparse

Hướng dẫn này nhằm giới thiệu một cách dễ tiếp cận về :mod:`argparse`, mô-đun phân tích dòng lệnh được khuyến nghị trong thư viện chuẩn Python.

.. note::

   Thư viện chuẩn bao gồm hai thư viện khác cũng liên quan trực tiếp đến việc xử lý tham số dòng lệnh: mô-đun :mod:`optparse` cấp thấp hơn (có thể cần nhiều mã hơn để cấu hình cho một ứng dụng cụ thể, nhưng cũng cho phép ứng dụng yêu cầu những hành vi mà ``argparse`` không hỗ trợ), và :mod:`getopt` cấp rất thấp (chủ yếu đóng vai trò tương đương với nhóm hàm :c:func:`!getopt` dành cho lập trình viên C). Mặc dù cả hai mô-đun này không được đề cập trực tiếp trong hướng dẫn, nhiều khái niệm cốt lõi trong ``argparse`` bắt nguồn từ ``optparse``, vì vậy một số phần của hướng dẫn này cũng sẽ hữu ích cho người dùng ``optparse``.


Các khái niệm
=============

Hãy minh họa loại chức năng mà chúng ta sẽ tìm hiểu trong hướng dẫn nhập môn này bằng cách sử dụng lệnh :command:`ls`:

.. code-block:: shell-session

   $ ls
   cpython  devguide  prog.py  pypy  rm-unused-function.patch
   $ ls pypy
   ctypes_configure  demo  dotviewer  include  lib_pypy  lib-python ...
   $ ls -l
   total 20
   drwxr-xr-x 19 wena wena 4096 Feb 18 18:51 cpython
   drwxr-xr-x  4 wena wena 4096 Feb  8 12:04 devguide
   -rwxr-xr-x  1 wena wena  535 Feb 19 00:05 prog.py
   drwxr-xr-x 14 wena wena 4096 Feb  7 00:59 pypy
   -rw-r--r--  1 wena wena  741 Feb 18 01:01 rm-unused-function.patch
   $ ls --help
   Usage: ls [OPTION]... [FILE]...
   List information about the FILEs (the current directory by default).
   Sort entries alphabetically if none of -cftuvSUX nor --sort is specified.
   ...

Bốn lệnh trên cho chúng ta biết một vài khái niệm:

* Lệnh :command:`ls` rất hữu ích khi được chạy hoàn toàn không có tùy chọn nào. Theo mặc định, lệnh này sẽ hiển thị nội dung của thư mục hiện tại.

* Nếu muốn làm nhiều hơn những gì lệnh cung cấp theo mặc định, chúng ta sẽ cung cấp thêm một chút thông tin cho lệnh. Trong trường hợp này, chúng ta muốn lệnh hiển thị một thư mục khác, ``pypy``. Việc chúng ta làm được gọi là chỉ định một positional argument. Nó được gọi như vậy vì chương trình phải biết cần làm gì với giá trị đó chỉ dựa vào vị trí của giá trị trên dòng lệnh. Khái niệm này phù hợp hơn với một lệnh như :command:`cp`, có cách sử dụng cơ bản nhất là ``cp SRC DEST``. Vị trí đầu tiên là *thứ bạn muốn sao chép,* còn vị trí thứ hai là *nơi bạn muốn sao chép đến*.

* Bây giờ, giả sử chúng ta muốn thay đổi hành vi của chương trình. Trong ví dụ này, chúng ta hiển thị nhiều thông tin hơn cho mỗi tệp thay vì chỉ hiển thị tên tệp. ``-l`` trong trường hợp đó được gọi là một optional argument.

* Đó là một đoạn văn bản trợ giúp. Nó rất hữu ích vì bạn có thể gặp một chương trình mà mình chưa từng sử dụng trước đây và tìm hiểu cách chương trình hoạt động chỉ bằng cách đọc văn bản trợ giúp của nó.


Những điều cơ bản
=================

Hãy bắt đầu với một ví dụ rất đơn giản, gần như không làm gì cả::

   import argparse
   parser = argparse.ArgumentParser()
   parser.parse_args()

Sau đây là kết quả khi chạy đoạn mã:

.. code-block:: shell-session

   $ python prog.py
   $ python prog.py --help
   usage: prog.py [-h]

   options:
     -h, --help  show this help message and exit
   $ python prog.py --verbose
   usage: prog.py [-h]
   prog.py: error: unrecognized arguments: --verbose
   $ python prog.py foo
   usage: prog.py [-h]
   prog.py: error: unrecognized arguments: foo

Sau đây là những gì đang diễn ra:

* Chạy script mà không có tùy chọn nào sẽ không hiển thị gì trên stdout. Không hữu ích lắm.

* Mục thứ hai bắt đầu cho thấy tính hữu ích của module :mod:`argparse`. Chúng ta hầu như chưa làm gì, nhưng đã nhận được một thông báo trợ giúp khá rõ ràng.

* Tùy chọn ``--help``, cũng có thể được viết ngắn gọn thành ``-h``, là tùy chọn duy nhất chúng ta được cung cấp sẵn (tức là không cần chỉ định). Việc chỉ định bất kỳ thứ gì khác sẽ dẫn đến lỗi. Nhưng ngay cả khi đó, chúng ta vẫn nhận được một thông báo usage hữu ích, cũng được cung cấp sẵn.


Giới thiệu các đối số vị trí
============================

Một ví dụ::

   import argparse
   parser = argparse.ArgumentParser()
   parser.add_argument("echo")
   args = parser.parse_args()
   print(args.echo)

Và chạy đoạn code:

.. code-block:: shell-session

   $ python prog.py
   usage: prog.py [-h] echo
   prog.py: error: the following arguments are required: echo
   $ python prog.py --help
   usage: prog.py [-h] echo

   positional arguments:
     echo

   options:
     -h, --help  show this help message and exit
   $ python prog.py foo
   foo

Sau đây là những gì đang diễn ra:

* Chúng ta đã thêm phương thức :meth:`~ArgumentParser.add_argument`, được dùng để chỉ định các tùy chọn dòng lệnh mà chương trình chấp nhận. Trong trường hợp này, tôi đặt tên cho nó là ``echo`` để phù hợp với chức năng của nó.

* Giờ đây, để gọi chương trình, chúng ta cần chỉ định một tùy chọn.

* Phương thức :meth:`~ArgumentParser.parse_args` thực sự trả về một số dữ liệu từ các tùy chọn đã chỉ định, trong trường hợp này là ``echo``.

* Biến này là một dạng 'ma thuật' mà :mod:`argparse` tự động thực hiện (tức là bạn không cần chỉ định giá trị đó được lưu trữ trong biến nào). Bạn cũng sẽ nhận thấy rằng tên của biến khớp với đối số chuỗi được truyền cho phương thức, ``echo``.

Tuy nhiên, hãy lưu ý rằng mặc dù phần hiển thị trợ giúp trông khá đẹp, hiện tại nó vẫn chưa hữu ích nhiều như có thể. Ví dụ, chúng ta thấy rằng mình nhận được ``echo`` dưới dạng một đối số vị trí, nhưng không biết nó làm gì ngoài việc đoán hoặc đọc mã nguồn. Vì vậy, hãy làm cho nó hữu ích hơn một chút::

   import argparse
   parser = argparse.ArgumentParser()
   parser.add_argument("echo", help="echo the string you use here")
   args = parser.parse_args()
   print(args.echo)

Và chúng ta nhận được:

.. code-block:: shell-session

   $ python prog.py -h
   usage: prog.py [-h] echo

   positional arguments:
     echo        echo the string you use here

   options:
     -h, --help  show this help message and exit

Bây giờ, hãy thử làm một việc thậm chí còn hữu ích hơn::

   import argparse
   parser = argparse.ArgumentParser()
   parser.add_argument("square", help="display a square of a given number")
   args = parser.parse_args()
   print(args.square**2)

Sau đây là kết quả khi chạy đoạn mã:

.. code-block:: shell-session

   $ python prog.py 4
   Traceback (most recent call last):
     File "prog.py", line 5, in <module>
       print(args.square**2)
   TypeError: unsupported operand type(s) for ** or pow(): 'str' and 'int'

Kết quả không được tốt lắm. Đó là vì :mod:`argparse` xử lý các tùy chọn chúng ta cung cấp dưới dạng chuỗi, trừ khi chúng ta yêu cầu nó làm khác đi. Vì vậy, hãy yêu cầu
:mod:`argparse` xử lý dữ liệu đầu vào đó dưới dạng số nguyên::

   import argparse
   parser = argparse.ArgumentParser()
   parser.add_argument("square", help="display a square of a given number",
                       type=int)
   args = parser.parse_args()
   print(args.square**2)

Sau đây là kết quả khi chạy đoạn mã:

.. code-block:: shell-session

   $ python prog.py 4
   16
   $ python prog.py four
   usage: prog.py [-h] square
   prog.py: error: argument square: invalid int value: 'four'

Lần này đã thành công. Giờ đây, chương trình thậm chí còn hữu ích ở chỗ tự động thoát khi gặp dữ liệu đầu vào không hợp lệ trước khi tiếp tục.


Giới thiệu các đối số tùy chọn
==============================

Cho đến nay, chúng ta đã làm việc với các đối số vị trí. Hãy cùng xem cách thêm các đối số tùy chọn::

   import argparse
   parser = argparse.ArgumentParser()
   parser.add_argument("--verbosity", help="increase output verbosity")
   args = parser.parse_args()
   if args.verbosity:
       print("verbosity turned on")

Và kết quả:

.. code-block:: shell-session

   $ python prog.py --verbosity 1
   verbosity turned on
   $ python prog.py
   $ python prog.py --help
   usage: prog.py [-h] [--verbosity VERBOSITY]

   options:
     -h, --help            show this help message and exit
     --verbosity VERBOSITY
                           increase output verbosity
   $ python prog.py --verbosity
   usage: prog.py [-h] [--verbosity VERBOSITY]
   prog.py: error: argument --verbosity: expected one argument

Sau đây là những gì đang diễn ra:

* Chương trình được viết để hiển thị nội dung nào đó khi ``--verbosity`` được chỉ định và không hiển thị gì khi không được chỉ định.

* Để cho thấy tùy chọn này thực sự là tùy chọn, chương trình không báo lỗi khi chạy mà không có tùy chọn đó. Lưu ý rằng theo mặc định, nếu một đối số tùy chọn không được sử dụng, biến tương ứng, trong trường hợp này là ``args.verbosity``, sẽ nhận ``None`` làm giá trị, đó là lý do nó không vượt qua phép kiểm tra điều kiện của câu lệnh :keyword:`if`.

* Thông báo trợ giúp có đôi chút khác biệt.

* Khi sử dụng tùy chọn ``--verbosity``, bạn cũng phải chỉ định một giá trị nào đó, bất kỳ giá trị nào.

Ví dụ trên chấp nhận các giá trị số nguyên tùy ý cho ``--verbosity``, nhưng đối với chương trình đơn giản của chúng ta, chỉ có hai giá trị thực sự hữu ích là ``True`` hoặc ``False``. Hãy sửa đổi mã cho phù hợp::

   import argparse
   parser = argparse.ArgumentParser()
   parser.add_argument("--verbose", help="increase output verbosity",
                       action="store_true")
   args = parser.parse_args()
   if args.verbose:
       print("verbosity turned on")

Và kết quả:

.. code-block:: shell-session

   $ python prog.py --verbose
   verbosity turned on
   $ python prog.py --verbose 1
   usage: prog.py [-h] [--verbose]
   prog.py: error: unrecognized arguments: 1
   $ python prog.py --help
   usage: prog.py [-h] [--verbose]

   options:
     -h, --help  show this help message and exit
     --verbose   increase output verbosity

Sau đây là những gì đang diễn ra:

* Tùy chọn này giờ giống một flag hơn là một tùy chọn yêu cầu giá trị. Chúng ta thậm chí đã đổi tên tùy chọn để phản ánh ý tưởng đó. Lưu ý rằng giờ đây chúng ta chỉ định một keyword mới là ``action`` và gán cho nó giá trị ``"store_true"``. Điều này có nghĩa là nếu tùy chọn được chỉ định, hãy gán giá trị ``True`` cho ``args.verbose``. Nếu không chỉ định tùy chọn này thì mặc định là ``False``.

* Nó sẽ báo lỗi khi bạn chỉ định một giá trị, đúng với bản chất thực sự của các flag.

* Hãy chú ý đến phần văn bản trợ giúp khác biệt.


Các tùy chọn ngắn
-----------------

Nếu bạn quen sử dụng command line, bạn sẽ nhận thấy rằng tôi vẫn chưa đề cập đến phiên bản viết tắt của các tùy chọn. Điều này khá đơn giản::

   import argparse
   parser = argparse.ArgumentParser()
   parser.add_argument("-v", "--verbose", help="increase output verbosity",
                       action="store_true")
   args = parser.parse_args()
   if args.verbose:
       print("verbosity turned on")

Và đây là cách thực hiện:

.. code-block:: shell-session

   $ python prog.py -v
   verbosity turned on
   $ python prog.py --help
   usage: prog.py [-h] [-v]

   options:
     -h, --help     show this help message and exit
     -v, --verbose  increase output verbosity

Lưu ý rằng khả năng mới này cũng được phản ánh trong phần văn bản trợ giúp.


Kết hợp các đối số positional và optional
=========================================

Chương trình của chúng ta tiếp tục trở nên phức tạp hơn::

   import argparse
   parser = argparse.ArgumentParser()
   parser.add_argument("square", type=int,
                       help="display a square of a given number")
   parser.add_argument("-v", "--verbose", action="store_true",
                       help="increase output verbosity")
   args = parser.parse_args()
   answer = args.square**2
   if args.verbose:
       print(f"the square of {args.square} equals {answer}")
   else:
       print(answer)

Và đây là kết quả đầu ra:

.. code-block:: shell-session

   $ python prog.py
   usage: prog.py [-h] [-v] square
   prog.py: error: the following arguments are required: square
   $ python prog.py 4
   16
   $ python prog.py 4 --verbose
   the square of 4 equals 16
   $ python prog.py --verbose 4
   the square of 4 equals 16

* Chúng ta đã đưa một đối số positional trở lại, vì vậy mới xuất hiện thông báo lỗi.

* Lưu ý rằng thứ tự không quan trọng.

Vậy hãy khôi phục cho chương trình của chúng ta khả năng nhận nhiều giá trị verbosity và thực sự sử dụng chúng::

   import argparse
   parser = argparse.ArgumentParser()
   parser.add_argument("square", type=int,
                       help="display a square of a given number")
   parser.add_argument("-v", "--verbosity", type=int,
                       help="increase output verbosity")
   args = parser.parse_args()
   answer = args.square**2
   if args.verbosity == 2:
       print(f"the square of {args.square} equals {answer}")
   elif args.verbosity == 1:
       print(f"{args.square}^2 == {answer}")
   else:
       print(answer)

Và kết quả:

.. code-block:: shell-session

   $ python prog.py 4
   16
   $ python prog.py 4 -v
   usage: prog.py [-h] [-v VERBOSITY] square
   prog.py: error: argument -v/--verbosity: expected one argument
   $ python prog.py 4 -v 1
   4^2 == 16
   $ python prog.py 4 -v 2
   the square of 4 equals 16
   $ python prog.py 4 -v 3
   16

Tất cả đều có vẻ ổn, ngoại trừ trường hợp cuối cùng làm lộ ra một lỗi trong chương trình. Hãy sửa lỗi này bằng cách giới hạn các giá trị mà tùy chọn ``--verbosity`` có thể chấp nhận::

   import argparse
   parser = argparse.ArgumentParser()
   parser.add_argument("square", type=int,
                       help="display a square of a given number")
   parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2],
                       help="increase output verbosity")
   args = parser.parse_args()
   answer = args.square**2
   if args.verbosity == 2:
       print(f"the square of {args.square} equals {answer}")
   elif args.verbosity == 1:
       print(f"{args.square}^2 == {answer}")
   else:
       print(answer)

Và kết quả:

.. code-block:: shell-session

   $ python prog.py 4 -v 3
   usage: prog.py [-h] [-v {0,1,2}] square
   prog.py: error: argument -v/--verbosity: invalid choice: 3 (choose from 0, 1, 2)
   $ python prog.py 4 -h
   usage: prog.py [-h] [-v {0,1,2}] square

   positional arguments:
     square                display a square of a given number

   options:
     -h, --help            show this help message and exit
     -v, --verbosity {0,1,2}
                           increase output verbosity

Lưu ý rằng thay đổi này được phản ánh cả trong thông báo lỗi lẫn chuỗi trợ giúp.

Bây giờ, hãy thử một cách khác để điều khiển verbosity, cách này khá phổ biến. Nó cũng tương ứng với cách tệp thực thi CPython xử lý đối số verbosity của chính nó (hãy kiểm tra kết quả của ``python --help``)::

   import argparse
   parser = argparse.ArgumentParser()
   parser.add_argument("square", type=int,
                       help="display the square of a given number")
   parser.add_argument("-v", "--verbosity", action="count",
                       help="increase output verbosity")
   args = parser.parse_args()
   answer = args.square**2
   if args.verbosity == 2:
       print(f"the square of {args.square} equals {answer}")
   elif args.verbosity == 1:
       print(f"{args.square}^2 == {answer}")
   else:
       print(answer)

Chúng ta đã thêm một action khác, "count", để đếm số lần xuất hiện của các tùy chọn cụ thể.


.. code-block:: shell-session

   $ python prog.py 4
   16
   $ python prog.py 4 -v
   4^2 == 16
   $ python prog.py 4 -vv
   the square of 4 equals 16
   $ python prog.py 4 --verbosity --verbosity
   the square of 4 equals 16
   $ python prog.py 4 -v 1
   usage: prog.py [-h] [-v] square
   prog.py: error: unrecognized arguments: 1
   $ python prog.py 4 -h
   usage: prog.py [-h] [-v] square

   positional arguments:
     square           display a square of a given number

   options:
     -h, --help       show this help message and exit
     -v, --verbosity  increase output verbosity
   $ python prog.py 4 -vvv
   16

* Đúng vậy, giờ nó giống một flag hơn (tương tự như ``action="store_true"``) trong phiên bản trước của script. Điều đó sẽ giải thích lời phàn nàn này.

* Nó cũng hoạt động tương tự action "store_true".

* Sau đây là minh họa về những gì action "count" cung cấp. Có lẽ bạn đã từng thấy kiểu sử dụng này trước đây.

* Và nếu bạn không chỉ định flag ``-v``, flag đó được xem là có giá trị ``None``.

* Đúng như dự kiến, khi chỉ định dạng đầy đủ của flag, chúng ta sẽ nhận được cùng một kết quả.

* Đáng tiếc là phần output trợ giúp của chúng ta chưa cung cấp nhiều thông tin về khả năng mới mà script đã có, nhưng điều đó luôn có thể được khắc phục bằng cách cải thiện tài liệu cho script (ví dụ: thông qua keyword argument ``help``).

* Kết quả đầu ra cuối cùng đó cho thấy một lỗi trong chương trình của chúng ta.


Hãy sửa lỗi này::

   import argparse
   parser = argparse.ArgumentParser()
   parser.add_argument("square", type=int,
                       help="display a square of a given number")
   parser.add_argument("-v", "--verbosity", action="count",
                       help="increase output verbosity")
   args = parser.parse_args()
   answer = args.square**2

   # bugfix: replace == with >=
   if args.verbosity >= 2:
       print(f"the square of {args.square} equals {answer}")
   elif args.verbosity >= 1:
       print(f"{args.square}^2 == {answer}")
   else:
       print(answer)

Và đây là kết quả:

.. code-block:: shell-session

   $ python prog.py 4 -vvv
   the square of 4 equals 16
   $ python prog.py 4 -vvvv
   the square of 4 equals 16
   $ python prog.py 4
   Traceback (most recent call last):
     File "prog.py", line 11, in <module>
       if args.verbosity >= 2:
   TypeError: '>=' not supported between instances of 'NoneType' and 'int'


* Kết quả đầu tiên diễn ra tốt và đã sửa được lỗi trước đó. Nghĩa là, chúng ta muốn mọi giá trị >= 2 đều có mức độ chi tiết tối đa.

* Kết quả thứ ba không được tốt lắm.

Hãy sửa lỗi đó::

   import argparse
   parser = argparse.ArgumentParser()
   parser.add_argument("square", type=int,
                       help="display a square of a given number")
   parser.add_argument("-v", "--verbosity", action="count", default=0,
                       help="increase output verbosity")
   args = parser.parse_args()
   answer = args.square**2
   if args.verbosity >= 2:
       print(f"the square of {args.square} equals {answer}")
   elif args.verbosity >= 1:
       print(f"{args.square}^2 == {answer}")
   else:
       print(answer)

Chúng ta vừa giới thiệu thêm một keyword, ``default``. Chúng ta đặt nó thành ``0`` để có thể so sánh với các giá trị int khác. Hãy nhớ rằng theo mặc định, nếu không chỉ định một đối số tùy chọn, nó sẽ nhận giá trị ``None``, và giá trị này không thể so sánh với một giá trị int (do đó mới có exception :exc:`TypeError`).

Và:

.. code-block:: shell-session

   $ python prog.py 4
   16

Chỉ với những gì đã học cho đến nay, bạn đã có thể làm được khá nhiều việc, trong khi chúng ta mới chỉ khám phá sơ qua. Module :mod:`argparse` rất mạnh mẽ, và chúng ta sẽ tìm hiểu thêm một chút về module này trước khi kết thúc tutorial.


Tìm hiểu nâng cao hơn một chút
==============================

Nếu muốn mở rộng chương trình nhỏ của mình để thực hiện các phép lũy thừa khác, không chỉ bình phương thì sao::

   import argparse
   parser = argparse.ArgumentParser()
   parser.add_argument("x", type=int, help="the base")
   parser.add_argument("y", type=int, help="the exponent")
   parser.add_argument("-v", "--verbosity", action="count", default=0)
   args = parser.parse_args()
   answer = args.x**args.y
   if args.verbosity >= 2:
       print(f"{args.x} to the power {args.y} equals {answer}")
   elif args.verbosity >= 1:
       print(f"{args.x}^{args.y} == {answer}")
   else:
       print(answer)

Kết quả:

.. code-block:: shell-session

   $ python prog.py
   usage: prog.py [-h] [-v] x y
   prog.py: error: the following arguments are required: x, y
   $ python prog.py -h
   usage: prog.py [-h] [-v] x y

   positional arguments:
     x                the base
     y                the exponent

   options:
     -h, --help       show this help message and exit
     -v, --verbosity
   $ python prog.py 4 2 -v
   4^2 == 16


Hãy chú ý rằng cho đến nay, chúng ta đã sử dụng mức độ verbosity để *thay đổi* văn bản được hiển thị. Thay vào đó, ví dụ sau sử dụng mức độ verbosity để hiển thị *nhiều hơn* văn bản::

   import argparse
   parser = argparse.ArgumentParser()
   parser.add_argument("x", type=int, help="the base")
   parser.add_argument("y", type=int, help="the exponent")
   parser.add_argument("-v", "--verbosity", action="count", default=0)
   args = parser.parse_args()
   answer = args.x**args.y
   if args.verbosity >= 2:
       print(f"Running '{__file__}'")
   if args.verbosity >= 1:
       print(f"{args.x}^{args.y} == ", end="")
   print(answer)

Kết quả:

.. code-block:: shell-session

   $ python prog.py 4 2
   16
   $ python prog.py 4 2 -v
   4^2 == 16
   $ python prog.py 4 2 -vv
   Running 'prog.py'
   4^2 == 16


.. _specifying-ambiguous-arguments:

Chỉ định các đối số không rõ ràng
---------------------------------

Khi có sự không rõ ràng trong việc quyết định một đối số là positional hay dành cho một argument, ``--`` có thể được dùng để cho :meth:`~ArgumentParser.parse_args` biết rằng mọi thứ sau đó là một positional argument::

   >>> parser = argparse.ArgumentParser(prog='PROG')
   >>> parser.add_argument('-n', nargs='+')
   >>> parser.add_argument('args', nargs='*')

   >>> # không rõ ràng, nên parse_args giả định đó là một option
   >>> parser.parse_args(['-f'])
   usage: PROG [-h] [-n N [N ...]] [args ...]
   PROG: error: unrecognized arguments: -f

   >>> parser.parse_args(['--', '-f'])
   Namespace(args=['-f'], n=None)

   >>> # không rõ ràng, nên tùy chọn -n chấp nhận các đối số một cách tham lam
   >>> parser.parse_args(['-n', '1', '2', '3'])
   Namespace(args=[], n=['1', '2', '3'])

   >>> parser.parse_args(['-n', '1', '--', '2', '3'])
   Namespace(args=['2', '3'], n=['1'])


Các tùy chọn xung đột
---------------------

Cho đến nay, chúng ta đã làm việc với hai phương thức của một
:class:`argparse.ArgumentParser` instance. Hãy giới thiệu thêm một tùy chọn thứ ba,
:meth:`~ArgumentParser.add_mutually_exclusive_group`. Nó cho phép chúng ta chỉ định các tùy chọn xung đột với nhau. Hãy thay đổi phần còn lại của chương trình để chức năng mới trở nên hợp lý hơn: chúng ta sẽ giới thiệu tùy chọn ``--quiet``, là tùy chọn đối lập với tùy chọn ``--verbose``::

   import argparse

   parser = argparse.ArgumentParser()
   group = parser.add_mutually_exclusive_group()
   group.add_argument("-v", "--verbose", action="store_true")
   group.add_argument("-q", "--quiet", action="store_true")
   parser.add_argument("x", type=int, help="the base")
   parser.add_argument("y", type=int, help="the exponent")
   args = parser.parse_args()
   answer = args.x**args.y

   if args.quiet:
       print(answer)
   elif args.verbose:
       print(f"{args.x} to the power {args.y} equals {answer}")
   else:
       print(f"{args.x}^{args.y} == {answer}")

Chương trình của chúng ta giờ đây đơn giản hơn và chúng ta đã loại bỏ một số chức năng để phục vụ mục đích minh họa. Dù sao thì đây là đầu ra:

.. code-block:: shell-session

   $ python prog.py 4 2
   4^2 == 16
   $ python prog.py 4 2 -q
   16
   $ python prog.py 4 2 -v
   4 to the power 2 equals 16
   $ python prog.py 4 2 -vq
   usage: prog.py [-h] [-v | -q] x y
   prog.py: error: argument -q/--quiet: not allowed with argument -v/--verbose
   $ python prog.py 4 2 -v --quiet
   usage: prog.py [-h] [-v | -q] x y
   prog.py: error: argument -q/--quiet: not allowed with argument -v/--verbose

Điều này hẳn khá dễ theo dõi. Tôi đã thêm phần đầu ra cuối cùng đó để bạn thấy được mức độ linh hoạt, tức là có thể kết hợp các tùy chọn dạng dài với các tùy chọn dạng ngắn.

Trước khi kết thúc, có lẽ bạn muốn cho người dùng biết mục đích chính của chương trình, phòng trường hợp họ không biết::

   import argparse

   parser = argparse.ArgumentParser(description="calculate X to the power of Y")
   group = parser.add_mutually_exclusive_group()
   group.add_argument("-v", "--verbose", action="store_true")
   group.add_argument("-q", "--quiet", action="store_true")
   parser.add_argument("x", type=int, help="the base")
   parser.add_argument("y", type=int, help="the exponent")
   args = parser.parse_args()
   answer = args.x**args.y

   if args.quiet:
       print(answer)
   elif args.verbose:
       print(f"{args.x} to the power {args.y} equals {answer}")
   else:
       print(f"{args.x}^{args.y} == {answer}")

Hãy lưu ý sự khác biệt nhỏ trong văn bản usage. Lưu ý ``[-v | -q]``, cho chúng ta biết rằng có thể sử dụng ``-v`` hoặc ``-q``, nhưng không thể sử dụng cả hai cùng lúc:

.. code-block:: shell-session

   $ python prog.py --help
   usage: prog.py [-h] [-v | -q] x y

   calculate X to the power of Y

   positional arguments:
     x              the base
     y              the exponent

   options:
     -h, --help     show this help message and exit
     -v, --verbose
     -q, --quiet


Cách dịch đầu ra của argparse
=============================

Đầu ra của mô-đun :mod:`argparse`, chẳng hạn như văn bản trợ giúp và thông báo lỗi, đều có thể được dịch bằng mô-đun :mod:`gettext`. Điều này cho phép các ứng dụng dễ dàng bản địa hóa những thông báo do
:mod:`argparse` tạo ra. Xem thêm :ref:`i18n-howto`.

Ví dụ, trong đầu ra của :mod:`argparse` này:

.. code-block:: shell-session

   $ python prog.py --help
   usage: prog.py [-h] [-v | -q] x y

   calculate X to the power of Y

   positional arguments:
     x              the base
     y              the exponent

   options:
     -h, --help     show this help message and exit
     -v, --verbose
     -q, --quiet

Các chuỗi ``usage:``, ``positional arguments:``, ``options:`` và ``show this help message and exit`` đều có thể được dịch.

Để dịch các chuỗi này, trước tiên chúng phải được trích xuất vào một tệp ``.po``. Ví dụ, sử dụng `Babel <https://babel.pocoo.org/>`__, hãy chạy lệnh sau:

.. code-block:: shell-session

  $ pybabel extract -o messages.po /usr/lib/python3.12/argparse.py

Lệnh này sẽ trích xuất tất cả các chuỗi có thể dịch từ mô-đun :mod:`argparse` và xuất chúng vào một tệp có tên ``messages.po``. Lệnh này giả định rằng bản cài đặt Python của bạn nằm trong ``/usr/lib``.

Bạn có thể tìm vị trí của mô-đun :mod:`argparse` trên hệ thống bằng tập lệnh này::

   import argparse
   print(argparse.__file__)

Sau khi các thông báo trong tệp ``.po`` được dịch và các bản dịch được cài đặt bằng :mod:`gettext`, :mod:`argparse` sẽ có thể hiển thị các thông báo đã dịch.

Để dịch các chuỗi của riêng bạn trong đầu ra :mod:`argparse`, hãy sử dụng :mod:`gettext`.

Bộ chuyển đổi kiểu tùy chỉnh
============================

Mô-đun :mod:`argparse` cho phép bạn chỉ định các bộ chuyển đổi kiểu tùy chỉnh cho các đối số dòng lệnh. Điều này cho phép bạn sửa đổi dữ liệu đầu vào của người dùng trước khi lưu vào :class:`argparse.Namespace`. Tính năng này hữu ích khi bạn cần tiền xử lý dữ liệu đầu vào trước khi sử dụng trong chương trình.

Khi sử dụng bộ chuyển đổi kiểu tùy chỉnh, bạn có thể dùng bất kỳ callable nào nhận một đối số chuỗi duy nhất (giá trị đối số) và trả về giá trị đã chuyển đổi. Tuy nhiên, nếu cần xử lý các tình huống phức tạp hơn, bạn có thể sử dụng một lớp action tùy chỉnh với tham số **action** thay thế.

Ví dụ: giả sử bạn muốn xử lý các đối số có các tiền tố khác nhau và xử lý chúng tương ứng::

   import argparse

   parser = argparse.ArgumentParser(prefix_chars='-+')

   parser.add_argument('-a', metavar='<value>', action='append',
                       type=lambda x: ('-', x))
   parser.add_argument('+a', metavar='<value>', action='append',
                       type=lambda x: ('+', x))

   args = parser.parse_args()
   print(args)

Đầu ra:

.. code-block:: shell-session

   $ python prog.py -a value1 +a value2
   Namespace(a=[('-', 'value1'), ('+', 'value2')])

Trong ví dụ này, chúng ta:

* Đã tạo một parser với các ký tự tiền tố tùy chỉnh bằng tham số ``prefix_chars``.

* Đã định nghĩa hai đối số, ``-a`` và ``+a``, sử dụng tham số ``type`` để tạo các bộ chuyển đổi kiểu tùy chỉnh nhằm lưu trữ giá trị trong một tuple cùng với tiền tố.

Nếu không có các bộ chuyển đổi kiểu tùy chỉnh, các đối số sẽ coi ``-a`` và ``+a`` là cùng một đối số, điều này sẽ không phù hợp. Bằng cách sử dụng các bộ chuyển đổi kiểu tùy chỉnh, chúng ta đã có thể phân biệt hai đối số này.

Kết luận
========

Module :mod:`argparse` cung cấp nhiều tính năng hơn những gì được trình bày ở đây. Tài liệu của module này khá chi tiết, đầy đủ và có rất nhiều ví dụ. Sau khi hoàn thành hướng dẫn này, bạn sẽ dễ dàng tiếp thu tài liệu đó mà không cảm thấy quá tải.
