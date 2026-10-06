:mod:`!argparse` --- Trình phân tích cú pháp cho các tùy chọn, đối số và lệnh con trên dòng lệnh
================================================================================================

.. module:: argparse
   :synopsis: Thư viện phân tích cú pháp tùy chọn và đối số trên dòng lệnh.

.. moduleauthor:: Steven Bethard <steven.bethard@gmail.com>
.. sectionauthor:: Steven Bethard <steven.bethard@gmail.com>

.. versionadded:: 3.2

**Mã nguồn:** :source:`Lib/argparse.py`

.. note::

   Mặc dù :mod:`!argparse` là module thư viện chuẩn được khuyến nghị mặc định để triển khai các ứng dụng dòng lệnh cơ bản, những tác giả có yêu cầu khắt khe hơn về chính xác cách hoạt động của ứng dụng dòng lệnh có thể nhận thấy module này không cung cấp mức độ kiểm soát cần thiết. Hãy tham khảo :ref:`choosing-an-argument-parser` để xem xét các giải pháp thay thế khi ``argparse`` không hỗ trợ những hành vi mà ứng dụng yêu cầu (chẳng hạn như vô hiệu hóa hoàn toàn hỗ trợ cho các tùy chọn và đối số vị trí xen kẽ, hoặc chấp nhận các giá trị tham số tùy chọn bắt đầu bằng ``-`` ngay cả khi chúng tương ứng với một tùy chọn khác đã được định nghĩa).

--------------

.. sidebar:: Hướng dẫn

   Trang này chứa thông tin tham khảo về API. Để làm quen nhẹ nhàng hơn với việc phân tích cú pháp dòng lệnh trong Python, hãy xem
   :ref:`hướng dẫn argparse <argparse-tutorial>`.

Mô-đun :mod:`!argparse` giúp dễ dàng viết các giao diện dòng lệnh thân thiện với người dùng. Chương trình xác định những đối số mà nó yêu cầu, còn :mod:`!argparse` sẽ tự phân tích cú pháp các đối số đó từ :data:`sys.argv`. Mô-đun :mod:`!argparse` cũng tự động tạo các thông báo trợ giúp và cách sử dụng. Mô-đun này cũng sẽ báo lỗi khi người dùng cung cấp cho chương trình các đối số không hợp lệ.

Khả năng hỗ trợ giao diện dòng lệnh của mô-đun :mod:`!argparse` được xây dựng xoay quanh một thực thể :class:`argparse.ArgumentParser`. Đây là một vùng chứa các đặc tả đối số và có các tùy chọn áp dụng cho toàn bộ parser::

   parser = argparse.ArgumentParser(
                       prog='ProgramName',
                       description='What the program does',
                       epilog='Text at the bottom of help')

Phương thức :meth:`ArgumentParser.add_argument` gắn từng đặc tả đối số vào parser. Phương thức này hỗ trợ các đối số vị trí, các tùy chọn nhận giá trị và các cờ bật/tắt::

   parser.add_argument('filename')           # đối số vị trí
   parser.add_argument('-c', '--count')      # tùy chọn nhận giá trị
   parser.add_argument('-v', '--verbose',
                       action='store_true')  # cờ bật/tắt

Phương thức :meth:`ArgumentParser.parse_args` chạy parser và đặt dữ liệu đã trích xuất vào một đối tượng :class:`argparse.Namespace`::

   args = parser.parse_args()
   print(args.filename, args.count, args.verbose)

.. note::
   Nếu bạn đang tìm hướng dẫn về cách nâng cấp mã :mod:`optparse` lên :mod:`!argparse`, hãy xem :ref:`Nâng cấp mã Optparse <upgrading-optparse-code>`.

Các đối tượng ArgumentParser
----------------------------

.. class:: ArgumentParser(prog=None, usage=None, description=None, \
                          epilog=None, parents=[], \ formatter_class=argparse.HelpFormatter, \ prefix_chars='-', fromfile_prefix_chars=None, \ argument_default=None, conflict_handler='error', \ add_help=True, allow_abbrev=True, exit_on_error=True, \ *, suggest_on_error=False, color=True)

   Tạo một đối tượng :class:`ArgumentParser` mới. Tất cả tham số phải được truyền dưới dạng đối số từ khóa. Mỗi tham số đều có phần mô tả chi tiết hơn bên dưới, nhưng tóm lại, chúng là:

   * prog_ - Tên của chương trình (mặc định: được tạo từ các thuộc tính của module ``__main__`` và ``sys.argv[0]``)

   * usage_ - Chuỗi mô tả cách sử dụng chương trình (mặc định: được tạo từ các đối số đã thêm vào parser)

   * description_ - Văn bản hiển thị trước phần trợ giúp về đối số (mặc định là không có văn bản)

   * epilog_ - Văn bản hiển thị sau phần trợ giúp về đối số (mặc định: không có văn bản)

   * parents_ - Danh sách các đối tượng :class:`ArgumentParser` có các đối số cũng sẽ được bao gồm

   * formatter_class_ - Một lớp dùng để tùy chỉnh nội dung trợ giúp

   * prefix_chars_ - Tập hợp các ký tự đứng trước các đối số tùy chọn (mặc định: '-')

   * fromfile_prefix_chars_ - Tập hợp các ký tự đứng trước các tệp mà từ đó sẽ đọc thêm các đối số (mặc định: ``None``)

   * argument_default_ - Giá trị mặc định chung cho các đối số (mặc định: ``None``)

   * conflict_handler_ - Chiến lược giải quyết các tùy chọn xung đột (thường không cần thiết)

   * add_help_ - Thêm tùy chọn ``-h/--help`` vào parser (mặc định: ``True``)

   * allow_abbrev_ - Cho phép viết tắt các tùy chọn dài nếu cách viết tắt đó không gây nhập nhằng (mặc định: ``True``)

   * exit_on_error_ - Xác định liệu :class:`!ArgumentParser` có thoát kèm thông tin lỗi khi xảy ra lỗi hay không (mặc định: ``True``)

   * suggest_on_error_ - Bật gợi ý cho các lựa chọn đối số và tên subparser bị nhập sai (mặc định: ``False``)

   * color_ - Cho phép đầu ra có màu (mặc định: ``True``)

   .. versionchanged:: 3.5
      Đã thêm tham số *allow_abbrev*.

   .. versionchanged:: 3.8
      Trong các phiên bản trước, *allow_abbrev* cũng vô hiệu hóa việc nhóm các cờ ngắn, chẳng hạn như ``-vv`` để biểu thị ``-v -v``.

   .. versionchanged:: 3.9
      Đã thêm tham số *exit_on_error*.

   .. versionchanged:: 3.14
      Đã thêm các tham số *suggest_on_error* và *color*.

Các phần sau đây mô tả cách sử dụng từng tham số này.


.. _prog:

prog
^^^^


Theo mặc định, :class:`ArgumentParser` tính tên của chương trình sẽ hiển thị trong các thông báo trợ giúp, tùy thuộc vào cách chạy trình thông dịch Python:

* :func:`base name <os.path.basename>` của ``sys.argv[0]`` nếu một tệp được truyền làm đối số.
* Tên trình thông dịch Python theo sau là ``sys.argv[0]`` nếu một thư mục hoặc tệp zip được truyền làm đối số.
* Tên của trình thông dịch Python, theo sau là ``-m``, rồi đến tên module hoặc package nếu đã sử dụng tùy chọn :option:`-m`.

Giá trị mặc định này hầu như luôn phù hợp vì nó sẽ khiến các thông báo trợ giúp khớp với chuỗi được dùng để gọi chương trình trên dòng lệnh. Tuy nhiên, để thay đổi hành vi mặc định này, có thể cung cấp một giá trị khác bằng cách sử dụng đối số ``prog=`` cho :class:`ArgumentParser`::

   >>> parser = argparse.ArgumentParser(prog='myprogram')
   >>> parser.print_help()
   usage: myprogram [-h]

   options:
    -h, --help  show this help message and exit

Lưu ý rằng tên chương trình, dù được xác định từ ``sys.argv[0]``, từ các thuộc tính module ``__main__`` hay từ đối số ``prog=``, đều có thể được sử dụng trong các thông báo trợ giúp thông qua định dạng ``%(prog)s``.

::

   >>> parser = argparse.ArgumentParser(prog='myprogram')
   >>> parser.add_argument('--foo', help='foo of the %(prog)s program')
   >>> parser.print_help()
   usage: myprogram [-h] [--foo FOO]

   options:
    -h, --help  show this help message and exit
    --foo FOO   foo of the myprogram program

.. versionchanged:: 3.14
   Giá trị ``prog`` mặc định hiện phản ánh cách ``__main__`` thực sự được thực thi, thay vì luôn là ``os.path.basename(sys.argv[0])``.

cách sử dụng
^^^^^^^^^^^^

Theo mặc định, :class:`ArgumentParser` tính toán thông báo cách sử dụng từ các đối số mà nó chứa. Có thể ghi đè thông báo mặc định bằng đối số từ khóa ``usage=``::

   >>> parser = argparse.ArgumentParser(prog='PROG', usage='%(prog)s [options]')
   >>> parser.add_argument('--foo', nargs='?', help='foo help')
   >>> parser.add_argument('bar', nargs='+', help='bar help')
   >>> parser.print_help()
   usage: PROG [options]

   positional arguments:
    bar          bar help

   options:
    -h, --help   show this help message and exit
    --foo [FOO]  foo help

Định dạng ``%(prog)s`` có thể được sử dụng để điền tên chương trình vào các thông báo cách sử dụng.

Khi chỉ định thông báo usage tùy chỉnh cho parser chính, bạn cũng có thể cân nhắc truyền đối số ``prog`` cho :meth:`~ArgumentParser.add_subparsers` hoặc các đối số ``prog`` và ``usage`` cho
:meth:`~_SubParsersAction.add_parser`, để đảm bảo các tiền tố lệnh và thông tin usage nhất quán giữa các subparser.


.. _description:

description
^^^^^^^^^^^

Hầu hết các lệnh gọi đến constructor :class:`ArgumentParser` sẽ sử dụng keyword argument ``description=``. Đối số này cung cấp mô tả ngắn gọn về chức năng và cách hoạt động của chương trình. Trong các thông báo trợ giúp, phần mô tả được hiển thị giữa chuỗi usage trên dòng lệnh và thông báo trợ giúp cho các đối số khác nhau.

Theo mặc định, phần mô tả sẽ được ngắt dòng để vừa với không gian được cung cấp. Để thay đổi hành vi này, hãy xem đối số formatter_class_.


epilog
^^^^^^

Một số chương trình muốn hiển thị thêm phần mô tả về chương trình sau phần mô tả các đối số. Bạn có thể chỉ định văn bản đó bằng đối số ``epilog=`` cho :class:`ArgumentParser`::

   >>> parser = argparse.ArgumentParser(
   ...     description='A foo that bars',
   ...     epilog="And that's how you'd foo a bar")
   >>> parser.print_help()
   usage: argparse.py [-h]

   A foo that bars

   options:
    -h, --help  show this help message and exit

   And that's how you'd foo a bar

Cũng như đối số description_, văn bản ``epilog=`` theo mặc định sẽ được ngắt dòng, nhưng bạn có thể điều chỉnh hành vi này bằng đối số formatter_class_ cho :class:`ArgumentParser`.


các parser cha
^^^^^^^^^^^^^^

Đôi khi, một số parser dùng chung một tập hợp đối số. Thay vì lặp lại định nghĩa của các đối số này, bạn có thể sử dụng một parser duy nhất chứa tất cả các đối số dùng chung và truyền parser đó vào đối số ``parents=`` của :class:`ArgumentParser`. Đối số ``parents=`` nhận một danh sách các đối tượng :class:`ArgumentParser`, thu thập tất cả action positional và optional từ các đối tượng đó, rồi thêm các action này vào đối tượng :class:`ArgumentParser` đang được xây dựng::

   >>> parent_parser = argparse.ArgumentParser(add_help=False)
   >>> parent_parser.add_argument('--parent', type=int)

   >>> foo_parser = argparse.ArgumentParser(parents=[parent_parser])
   >>> foo_parser.add_argument('foo')
   >>> foo_parser.parse_args(['--parent', '2', 'XXX'])
   Namespace(foo='XXX', parent=2)

   >>> bar_parser = argparse.ArgumentParser(parents=[parent_parser])
   >>> bar_parser.add_argument('--bar')
   >>> bar_parser.parse_args(['--bar', 'YYY'])
   Namespace(bar='YYY', parent=None)

Lưu ý rằng hầu hết các parser cha sẽ chỉ định ``add_help=False``. Nếu không thì
:class:`ArgumentParser` sẽ thấy hai tùy chọn ``-h/--help`` (một ở parser cha và một ở parser con) rồi phát sinh lỗi.

.. note::
   Bạn phải khởi tạo đầy đủ các parser trước khi truyền chúng qua ``parents=``. Nếu bạn thay đổi các parser cha sau khi tạo parser con, những thay đổi đó sẽ không được phản ánh trong parser con.


.. _formatter_class:

formatter_class
^^^^^^^^^^^^^^^

Các đối tượng :class:`ArgumentParser` cho phép tùy chỉnh định dạng trợ giúp bằng cách chỉ định một lớp định dạng thay thế. Hiện tại có bốn lớp như vậy:

.. class:: RawDescriptionHelpFormatter
           RawTextHelpFormatter ArgumentDefaultsHelpFormatter MetavarTypeHelpFormatter

:class:`RawDescriptionHelpFormatter` và :class:`RawTextHelpFormatter` cho phép kiểm soát tốt hơn cách hiển thị các mô tả dạng văn bản. Theo mặc định, các đối tượng :class:`ArgumentParser` tự động xuống dòng các văn bản description_ và epilog_ trong thông báo trợ giúp dòng lệnh::

   >>> parser = argparse.ArgumentParser(
   ...     prog='PROG',
   ...     description='''this description
   ...         was indented weird
   ...             but that is okay''',
   ...     epilog='''
   ...             likewise for this epilog whose whitespace will
   ...         be cleaned up and whose words will be wrapped
   ...         across a couple lines''')
   >>> parser.print_help()
   usage: PROG [-h]

   this description was indented weird but that is okay

   options:
    -h, --help  show this help message and exit

   likewise for this epilog whose whitespace will be cleaned up and whose words
   will be wrapped across a couple lines

Truyền :class:`RawDescriptionHelpFormatter` dưới dạng ``formatter_class=`` cho biết rằng description_ và epilog_ đã được định dạng chính xác và không nên được tự động xuống dòng::

   >>> parser = argparse.ArgumentParser(
   ...     prog='PROG',
   ...     formatter_class=argparse.RawDescriptionHelpFormatter,
   ...     description=textwrap.dedent('''\
   ...         Please do not mess up this text!
   ...         --------------------------------
   ...             I have indented it
   ...             exactly the way
   ...             I want it
   ...         '''))
   >>> parser.print_help()
   usage: PROG [-h]

   Please do not mess up this text!
   --------------------------------
      I have indented it
      exactly the way
      I want it

   options:
    -h, --help  show this help message and exit

:class:`RawTextHelpFormatter` giữ nguyên khoảng trắng cho mọi loại văn bản trợ giúp, bao gồm cả mô tả đối số. Tuy nhiên, nhiều dòng mới sẽ được thay thế bằng một dòng mới. Nếu muốn giữ lại nhiều dòng trống, hãy thêm dấu cách giữa các dòng mới.

:class:`ArgumentDefaultsHelpFormatter` tự động thêm thông tin về các giá trị mặc định vào từng thông báo trợ giúp đối số::

   >>> parser = argparse.ArgumentParser(
   ...     prog='PROG',
   ...     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
   >>> parser.add_argument('--foo', type=int, default=42, help='FOO!')
   >>> parser.add_argument('bar', nargs='*', default=[1, 2, 3], help='BAR!')
   >>> parser.print_help()
   usage: PROG [-h] [--foo FOO] [bar ...]

   positional arguments:
    bar         BAR! (default: [1, 2, 3])

   options:
    -h, --help  show this help message and exit
    --foo FOO   FOO! (default: 42)

:class:`MetavarTypeHelpFormatter` sử dụng tên của đối số type_ cho mỗi đối số làm tên hiển thị cho các giá trị của đối số đó (thay vì sử dụng dest_ như formatter thông thường)::

   >>> parser = argparse.ArgumentParser(
   ...     prog='PROG',
   ...     formatter_class=argparse.MetavarTypeHelpFormatter)
   >>> parser.add_argument('--foo', type=int)
   >>> parser.add_argument('bar', type=float)
   >>> parser.print_help()
   usage: PROG [-h] [--foo int] float

   positional arguments:
     float

   options:
     -h, --help  show this help message and exit
     --foo int


prefix_chars
^^^^^^^^^^^^

Hầu hết các tùy chọn dòng lệnh sẽ sử dụng ``-`` làm tiền tố, ví dụ ``-f/--foo``. Các parser cần hỗ trợ những ký tự tiền tố khác hoặc bổ sung, chẳng hạn cho các tùy chọn như ``+f`` hoặc ``/foo``, có thể chỉ định chúng bằng đối số ``prefix_chars=`` cho constructor :class:`ArgumentParser`::

   >>> parser = argparse.ArgumentParser(prog='PROG', prefix_chars='-+')
   >>> parser.add_argument('+f')
   >>> parser.add_argument('++bar')
   >>> parser.parse_args('+f X ++bar Y'.split())
   Namespace(bar='Y', f='X')

Đối số ``prefix_chars=`` mặc định là ``'-'``. Việc cung cấp một tập ký tự không bao gồm ``-`` sẽ khiến các tùy chọn ``-f/--foo`` không được phép sử dụng.


fromfile_prefix_chars
^^^^^^^^^^^^^^^^^^^^^

Đôi khi, khi làm việc với một danh sách đối số đặc biệt dài, việc lưu danh sách đối số trong một tệp thay vì nhập trực tiếp tại dòng lệnh có thể hợp lý. Nếu đối số ``fromfile_prefix_chars=`` được truyền cho constructor
:class:`ArgumentParser`, thì các đối số bắt đầu bằng bất kỳ ký tự nào được chỉ định sẽ được coi là các tệp và được thay thế bằng những đối số mà chúng chứa. Ví dụ::

   >>> with open('args.txt', 'w', encoding=sys.getfilesystemencoding()) as fp:
   ...     fp.write('-f\nbar')
   ...
   >>> parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
   >>> parser.add_argument('-f')
   >>> parser.parse_args(['-f', 'foo', '@args.txt'])
   Namespace(f='bar')

Theo mặc định, các đối số được đọc từ một tệp phải nằm trên từng dòng riêng biệt (nhưng cũng xem
:meth:`~ArgumentParser.convert_arg_line_to_args`) và được xử lý như thể chúng nằm cùng vị trí với đối số tham chiếu đến tệp ban đầu trên dòng lệnh. Vì vậy, trong ví dụ trên, biểu thức ``['-f', 'foo', '@args.txt']`` được xem là tương đương với biểu thức ``['-f', 'foo', '-f', 'bar']``.

.. note::

   Mỗi dòng được xử lý như một đối số duy nhất, vì vậy một dòng trống được đọc dưới dạng chuỗi rỗng (``''``).

:class:`ArgumentParser` sử dụng :term:`filesystem encoding and error handler` để đọc tệp chứa các đối số.

Đối số ``fromfile_prefix_chars=`` mặc định là ``None``, nghĩa là các đối số sẽ không bao giờ được xử lý như tham chiếu đến tệp.

.. versionchanged:: 3.12
   :class:`ArgumentParser` changed encoding and errors to read arguments files
   từ giá trị mặc định (ví dụ: :func:`locale.getpreferredencoding(False) <locale.getpreferredencoding>` và ``"strict"``) đến :term:`filesystem encoding and error handler`. Tệp đối số phải được mã hóa bằng UTF-8 thay vì ANSI Codepage trên Windows.


argument_default
^^^^^^^^^^^^^^^^

Thông thường, giá trị mặc định của đối số được chỉ định bằng cách truyền một giá trị mặc định cho
:meth:`~ArgumentParser.add_argument` hoặc bằng cách gọi
các phương thức :meth:`~ArgumentParser.set_defaults` với một tập hợp cặp tên-giá trị cụ thể. Tuy nhiên, đôi khi việc chỉ định một giá trị mặc định chung cho toàn bộ parser đối với các đối số có thể hữu ích. Có thể thực hiện điều này bằng cách truyền đối số từ khóa ``argument_default=`` cho :class:`ArgumentParser`. Ví dụ: để ngăn việc tạo thuộc tính trên toàn cục trong các lệnh gọi :meth:`~ArgumentParser.parse_args`, chúng ta cung cấp ``argument_default=SUPPRESS``::

   >>> parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
   >>> parser.add_argument('--foo')
   >>> parser.add_argument('bar', nargs='?')
   >>> parser.parse_args(['--foo', '1', 'BAR'])
   Namespace(bar='BAR', foo='1')
   >>> parser.parse_args([])
   Namespace()

.. _allow_abbrev:

allow_abbrev
^^^^^^^^^^^^

Thông thường, khi bạn truyền một danh sách đối số cho phương thức
phương thức :meth:`~ArgumentParser.parse_args` của :class:`ArgumentParser` sẽ :ref:`nhận dạng các dạng viết tắt <prefix-matching>` của các tùy chọn dài.

Bạn có thể vô hiệu hóa tính năng này bằng cách đặt ``allow_abbrev`` thành ``False``::

   >>> parser = argparse.ArgumentParser(prog='PROG', allow_abbrev=False)
   >>> parser.add_argument('--foobar', action='store_true')
   >>> parser.add_argument('--foonley', action='store_false')
   >>> parser.parse_args(['--foon'])
   usage: PROG [-h] [--foobar] [--foonley]
   PROG: error: unrecognized arguments: --foon

.. versionadded:: 3.5


conflict_handler
^^^^^^^^^^^^^^^^

Các đối tượng :class:`ArgumentParser` không cho phép hai action có cùng option string. Theo mặc định, các đối tượng :class:`ArgumentParser` sẽ phát sinh ngoại lệ nếu cố tạo một argument với option string đã được sử dụng::

   >>> parser = argparse.ArgumentParser(prog='PROG')
   >>> parser.add_argument('-f', '--foo', help='old foo help')
   >>> parser.add_argument('--foo', help='new foo help')
   Traceback (most recent call last):
    ..
   ArgumentError: argument --foo: conflicting option string(s): --foo

Đôi khi (ví dụ: khi sử dụng parents_), việc chỉ cần ghi đè mọi argument cũ có cùng option string có thể hữu ích. Để có hành vi này, có thể cung cấp giá trị ``'resolve'`` cho argument ``conflict_handler=`` của
:class:`ArgumentParser`::

   >>> parser = argparse.ArgumentParser(prog='PROG', conflict_handler='resolve')
   >>> parser.add_argument('-f', '--foo', help='old foo help')
   >>> parser.add_argument('--foo', help='new foo help')
   >>> parser.print_help()
   usage: PROG [-h] [-f FOO] [--foo FOO]

   options:
    -h, --help  show this help message and exit
    -f FOO      old foo help
    --foo FOO   new foo help

Lưu ý rằng các đối tượng :class:`ArgumentParser` chỉ xóa một action nếu tất cả option string của action đó đều bị ghi đè. Vì vậy, trong ví dụ trên, action ``-f/--foo`` cũ được giữ lại dưới dạng action ``-f``, vì chỉ option string ``--foo`` bị ghi đè.


add_help
^^^^^^^^

Theo mặc định, các đối tượng :class:`ArgumentParser` thêm một tùy chọn chỉ hiển thị thông báo trợ giúp của parser. Nếu ``-h`` hoặc ``--help`` được cung cấp trên command line, thông báo trợ giúp :class:`!ArgumentParser` sẽ được in ra.

Đôi khi, việc tắt tùy chọn trợ giúp này có thể hữu ích. Có thể thực hiện điều này bằng cách truyền ``False`` làm argument ``add_help=`` cho
:class:`ArgumentParser`::

   >>> parser = argparse.ArgumentParser(prog='PROG', add_help=False)
   >>> parser.add_argument('--foo', help='foo help')
   >>> parser.print_help()
   usage: PROG [--foo FOO]

   options:
    --foo FOO  foo help

Tùy chọn trợ giúp thường là ``-h/--help``. Ngoại lệ là khi ``prefix_chars=`` được chỉ định và không bao gồm ``-``, trong trường hợp đó ``-h`` và ``--help`` không phải là các tùy chọn hợp lệ. Trong trường hợp này, ký tự đầu tiên trong ``prefix_chars`` được dùng làm tiền tố cho các tùy chọn trợ giúp::

   >>> parser = argparse.ArgumentParser(prog='PROG', prefix_chars='+/')
   >>> parser.print_help()
   usage: PROG [+h]

   options:
     +h, ++help  show this help message and exit


exit_on_error
^^^^^^^^^^^^^

Thông thường, khi bạn truyền một danh sách đối số không hợp lệ cho phương thức :meth:`~ArgumentParser.parse_args` của một :class:`ArgumentParser`, phương thức này sẽ in *thông báo* vào :data:`sys.stderr` và thoát với mã trạng thái 2.

Nếu người dùng muốn tự bắt lỗi, có thể bật tính năng này bằng cách đặt ``exit_on_error`` thành ``False``::

   >>> parser = argparse.ArgumentParser(exit_on_error=False)
   >>> parser.add_argument('--integers', type=int)
   _StoreAction(option_strings=['--integers'], dest='integers', nargs=None, const=None, default=None, type=<class 'int'>, choices=None, help=None, metavar=None)
   >>> try:
   ...     parser.parse_args('--integers a'.split())
   ... except argparse.ArgumentError:
   ...     print('Catching an argumentError')
   ...
   Catching an argumentError

.. versionadded:: 3.9

suggest_on_error
^^^^^^^^^^^^^^^^

Theo mặc định, khi người dùng truyền một lựa chọn đối số hoặc tên subparser không hợp lệ,
:class:`ArgumentParser` sẽ thoát với thông tin lỗi và liệt kê các lựa chọn đối số được phép (nếu được chỉ định) hoặc tên subparser trong thông báo lỗi.

Nếu người dùng muốn bật gợi ý cho các lựa chọn đối số và tên subparser bị nhập sai, có thể bật tính năng này bằng cách đặt ``suggest_on_error`` thành ``True``. Lưu ý rằng tính năng này chỉ áp dụng cho các đối số khi các choices được chỉ định là chuỗi::

   >>> parser = argparse.ArgumentParser(suggest_on_error=True)
   >>> parser.add_argument('--action', choices=['debug', 'dryrun'])
   >>> parser.parse_args(['--action', 'debugg'])
   usage: tester.py [-h] [--action {debug,dryrun}]
   tester.py: error: argument --action: invalid choice: 'debugg', maybe you meant 'debug'? (choose from debug, dryrun)

Nếu bạn đang viết mã cần tương thích với các phiên bản Python cũ hơn và muốn tận dụng ``suggest_on_error`` khi có sẵn, bạn có thể đặt nó làm thuộc tính sau khi khởi tạo parser thay vì sử dụng đối số từ khóa::

   >>> parser = argparse.ArgumentParser(description='Process some integers.')
   >>> parser.suggest_on_error = True

.. versionadded:: 3.14


color
^^^^^

Theo mặc định, thông báo trợ giúp được in bằng màu thông qua `ANSI escape sequences <https://en.wikipedia.org/wiki/ANSI_escape_code>`__. Nếu muốn thông báo trợ giúp dạng văn bản thuần túy, bạn có thể tắt :ref:`in your local environment <using-on-controlling-color>`, hoặc tắt trong chính argument parser bằng cách đặt ``color`` thành ``False``::

   >>> parser = argparse.ArgumentParser(description='Process some integers.',
   ...                                  color=False)
   >>> parser.add_argument('--action', choices=['sum', 'max'])
   >>> parser.add_argument('integers', metavar='N', type=int, nargs='+',
   ...                     help='an integer for the accumulator')
   >>> parser.parse_args(['--help'])

Lưu ý rằng khi ``color=True``, đầu ra có màu phụ thuộc vào cả các biến môi trường và khả năng của terminal. Tuy nhiên, nếu ``color=False``, đầu ra có màu luôn bị tắt, ngay cả khi các biến môi trường như ``FORCE_COLOR`` được đặt.

.. note::

   Thông báo lỗi sẽ bao gồm các mã màu khi chuyển hướng stderr vào một tệp. Để tránh điều này, hãy đặt biến môi trường |NO_COLOR|_ hoặc :envvar:`PYTHON_COLORS` (ví dụ: ``NO_COLOR=1 python script.py 2> errors.txt``).

.. versionadded:: 3.14


Phương thức add_argument()
--------------------------

.. method:: ArgumentParser.add_argument(name or flags..., *, [action], [nargs], \
                           [const], [default], [type], [choices], [required], \ [help], [metavar], [dest], [deprecated])

   Xác định cách phân tích cú pháp cho một đối số dòng lệnh đơn. Mỗi tham số đều có phần mô tả chi tiết hơn bên dưới, nhưng tóm lại là:

   * `name or flags <name or flags_>`_ - Một tên hoặc danh sách các chuỗi tùy chọn, chẳng hạn như ``'foo'`` hoặc ``'-f', '--foo'``.

   * action_ - Loại hành động cơ bản sẽ được thực hiện khi gặp đối số này trên dòng lệnh.

   * nargs_ - Số lượng đối số dòng lệnh sẽ được sử dụng.

   * const_ - Một giá trị hằng số bắt buộc đối với một số lựa chọn action_ và nargs_.

   * default_ - Giá trị được tạo ra nếu đối số không có trên dòng lệnh và cũng không có trong đối tượng namespace.

   * type_ - Kiểu dữ liệu mà đối số dòng lệnh sẽ được chuyển đổi sang.

   * choices_ - Một chuỗi các giá trị được phép cho đối số.

   * required_ - Tùy chọn dòng lệnh có thể được bỏ qua hay không (chỉ áp dụng cho các tùy chọn).

   * help_ - Mô tả ngắn gọn về chức năng của đối số.

   * metavar_ - Tên của đối số trong các thông báo usage.

   * dest_ - Tên của thuộc tính sẽ được thêm vào đối tượng được trả về bởi
     :meth:`parse_args`.

   * deprecated_ - Việc sử dụng đối số có bị deprecated hay không.

   Phương thức này trả về một đối tượng :class:`Action` đại diện cho đối số.

Các phần sau đây mô tả cách sử dụng từng thành phần này.


.. _`name or flags`:

name hoặc flags
^^^^^^^^^^^^^^^

Phương thức :meth:`~ArgumentParser.add_argument` phải biết liệu cần một đối số tùy chọn, chẳng hạn như ``-f`` hoặc ``--foo``, hay một đối số vị trí, chẳng hạn như danh sách tên tệp. Các đối số đầu tiên được truyền vào
:meth:`~ArgumentParser.add_argument` vì vậy phải là một chuỗi flags hoặc một tên đối số đơn giản.

Ví dụ: có thể tạo một đối số tùy chọn như sau::

   >>> parser.add_argument('-f', '--foo')

trong khi có thể tạo một đối số vị trí như sau::

   >>> parser.add_argument('bar')

Khi gọi :meth:`~ArgumentParser.parse_args`, các đối số tùy chọn sẽ được nhận diện bằng tiền tố ``-``, còn các đối số còn lại sẽ được mặc định là đối số vị trí::

   >>> parser = argparse.ArgumentParser(prog='PROG')
   >>> parser.add_argument('-f', '--foo')
   >>> parser.add_argument('bar')
   >>> parser.parse_args(['BAR'])
   Namespace(bar='BAR', foo=None)
   >>> parser.parse_args(['BAR', '--foo', 'FOO'])
   Namespace(bar='BAR', foo='FOO')
   >>> parser.parse_args(['--foo', 'FOO'])
   usage: PROG [-h] [-f FOO] bar
   PROG: error: the following arguments are required: bar

Theo mặc định, :mod:`!argparse` tự động xử lý tên nội bộ và tên hiển thị của các argument, đơn giản hóa quy trình mà không cần cấu hình bổ sung. Do đó, bạn không cần chỉ định các tham số dest_ và metavar_. Đối với các argument tùy chọn, tham số dest_ mặc định là tên của argument, trong đó dấu gạch dưới ``_`` thay thế dấu gạch ngang ``-``. Tham số metavar_ mặc định là tên được viết hoa. Ví dụ::

   >>> parser = argparse.ArgumentParser(prog='PROG')
   >>> parser.add_argument('--foo-bar')
   >>> parser.parse_args(['--foo-bar', 'FOO-BAR'])
   Namespace(foo_bar='FOO-BAR')
   >>> parser.print_help()
   usage:  [-h] [--foo-bar FOO-BAR]

   optional arguments:
    -h, --help  show this help message and exit
    --foo-bar FOO-BAR


.. _action:

action
^^^^^^

Các đối tượng :class:`ArgumentParser` liên kết các tham số dòng lệnh với các action. Những action này có thể thực hiện gần như mọi thao tác với các tham số dòng lệnh được liên kết với chúng, mặc dù hầu hết action chỉ thêm một thuộc tính vào đối tượng được :class:`ArgumentParser` trả về
:meth:`~ArgumentParser.parse_args`. Từ khóa ``action`` chỉ định cách xử lý các tham số dòng lệnh. Các action được cung cấp gồm:

* ``'store'`` - Chỉ lưu giá trị của argument. Đây là action mặc định.

* ``'store_const'`` - Lưu giá trị được chỉ định bởi đối số từ khóa const_; lưu ý rằng đối số từ khóa const_ mặc định là ``None``. action ``'store_const'`` thường được sử dụng nhất với các argument tùy chọn chỉ định một loại flag nào đó. Ví dụ::

    >>> parser = argparse.ArgumentParser()
    >>> parser.add_argument('--foo', action='store_const', const=42)
    >>> parser.parse_args(['--foo'])
    Namespace(foo=42)

* ``'store_true'`` và ``'store_false'`` - Đây là các trường hợp đặc biệt của ``'store_const'``, lần lượt lưu các giá trị ``True`` và ``False`` với các giá trị mặc định là ``False`` và ``True``::

    >>> parser = argparse.ArgumentParser()
    >>> parser.add_argument('--foo', action='store_true')
    >>> parser.add_argument('--bar', action='store_false')
    >>> parser.add_argument('--baz', action='store_false')
    >>> parser.parse_args('--foo --bar'.split())
    Namespace(foo=True, bar=False, baz=True)

* ``'append'`` - Thao tác này thêm giá trị của từng đối số vào một danh sách. Thao tác này hữu ích khi cho phép chỉ định một tùy chọn nhiều lần. Nếu giá trị mặc định là một danh sách không rỗng, giá trị được phân tích sẽ bắt đầu bằng các phần tử của danh sách mặc định, rồi các giá trị từ dòng lệnh sẽ được thêm vào sau những giá trị mặc định đó. Ví dụ sử dụng::

    >>> parser = argparse.ArgumentParser()
    >>> parser.add_argument('--foo', action='append', default=['0'])
    >>> parser.parse_args('--foo 1 --foo 2'.split())
    Namespace(foo=['0', '1', '2'])

* ``'append_const'`` - Thao tác này thêm giá trị được chỉ định bởi đối số từ khóa const_ vào một danh sách; lưu ý rằng đối số từ khóa const_ mặc định là ``None``. Thao tác ``'append_const'`` thường hữu ích khi nhiều đối số cần lưu các hằng số vào cùng một danh sách. Ví dụ::

    >>> parser = argparse.ArgumentParser()
    >>> parser.add_argument('--str', dest='types', action='append_const', const=str)
    >>> parser.add_argument('--int', dest='types', action='append_const', const=int)
    >>> parser.parse_args('--str --int'.split())
    Namespace(types=[<class 'str'>, <class 'int'>])

* ``'extend'`` - Thao tác này thêm từng mục từ một đối số nhiều giá trị vào một danh sách. Thao tác ``'extend'`` thường được dùng với giá trị đối số từ khóa nargs_ là ``'+'`` hoặc ``'*'``. Lưu ý rằng khi nargs_ là ``None`` (mặc định) hoặc ``'?'``, từng ký tự của chuỗi đối số sẽ được thêm vào danh sách. Ví dụ sử dụng::

    >>> parser = argparse.ArgumentParser()
    >>> parser.add_argument("--foo", action="extend", nargs="+", type=str)
    >>> parser.parse_args(["--foo", "f1", "--foo", "f2", "f3", "f4"])
    Namespace(foo=['f1', 'f2', 'f3', 'f4'])

  .. versionadded:: 3.8

* ``'count'`` - Thao tác này đếm số lần một đối số xuất hiện. Ví dụ, thao tác này hữu ích để tăng các mức độ chi tiết của đầu ra::

    >>> parser = argparse.ArgumentParser()
    >>> parser.add_argument('--verbose', '-v', action='count', default=0)
    >>> parser.parse_args(['-vvv'])
    Namespace(verbose=3)

  Trừ khi được đặt rõ ràng, *giá trị mặc định* sẽ là ``None``. Nếu giá trị mặc định là một số khác không, bộ đếm sẽ bắt đầu từ số đó thay vì từ số không.

* ``'help'`` - Thao tác này in thông báo trợ giúp đầy đủ cho tất cả tùy chọn trong parser hiện tại rồi thoát. Theo mặc định, một thao tác trợ giúp sẽ tự động được thêm vào parser. Xem :class:`ArgumentParser` để biết chi tiết về cách tạo đầu ra.

* ``'version'`` - Thao tác này yêu cầu một đối số từ khóa ``version=`` trong
  gọi :meth:`~ArgumentParser.add_argument`, in thông tin phiên bản rồi thoát khi được gọi::

    >>> import argparse
    >>> parser = argparse.ArgumentParser(prog='PROG')
    >>> parser.add_argument('--version', action='version', version='%(prog)s 2.0')
    >>> parser.parse_args(['--version'])
    PROG 2.0

Bạn cũng có thể chỉ định một action tùy ý bằng cách truyền một lớp con của :class:`Action` (ví dụ: :class:`BooleanOptionalAction`) hoặc đối tượng khác triển khai cùng một interface. Chỉ những action nhận các đối số dòng lệnh (ví dụ: ``'store'``, ``'append'``, ``'extend'`` hoặc action tùy chỉnh có ``nargs`` khác không) mới có thể được sử dụng với các đối số positional.

Cách được khuyến nghị để tạo action tùy chỉnh là mở rộng :class:`Action`, ghi đè phương thức :meth:`!__call__` và tùy chọn ghi đè :meth:`!__init__` và
các phương thức :meth:`!format_usage`. Bạn cũng có thể đăng ký action tùy chỉnh bằng phương thức
:meth:`~ArgumentParser.register` và tham chiếu đến chúng bằng tên đã đăng ký.

Ví dụ về một action tùy chỉnh::

   >>> class FooAction(argparse.Action):
   ...     def __init__(self, option_strings, dest, nargs=None, **kwargs):
   ...         if nargs is not None:
   ...             raise ValueError("nargs not allowed")
   ...         super().__init__(option_strings, dest, **kwargs)
   ...     def __call__(self, parser, namespace, values, option_string=None):
   ...         print('%r %r %r' % (namespace, values, option_string))
   ...         setattr(namespace, self.dest, values)
   ...
   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('--foo', action=FooAction)
   >>> parser.add_argument('bar', action=FooAction)
   >>> args = parser.parse_args('1 --foo 2'.split())
   Namespace(bar=None, foo=None) '1' None
   Namespace(bar='1', foo=None) '2' '--foo'
   >>> args
   Namespace(bar='1', foo='2')

Để biết thêm chi tiết, hãy xem :class:`Action`.


.. _nargs:

nargs
^^^^^

Các đối tượng :class:`ArgumentParser` thường liên kết một đối số dòng lệnh duy nhất với một hành động duy nhất cần thực hiện. Đối số từ khóa ``nargs`` liên kết một số lượng đối số dòng lệnh khác với một hành động duy nhất. Xem thêm :ref:`specifying-ambiguous-arguments`. Các giá trị được hỗ trợ là:

* ``N`` (một số nguyên). Các đối số ``N`` từ dòng lệnh sẽ được tập hợp vào một danh sách. Ví dụ::

     >>> parser = argparse.ArgumentParser()
     >>> parser.add_argument('--foo', nargs=2)
     >>> parser.add_argument('bar', nargs=1)
     >>> parser.parse_args('c --foo a b'.split())
     Namespace(bar=['c'], foo=['a', 'b'])

  Lưu ý rằng ``nargs=1`` tạo ra một danh sách gồm một phần tử. Điều này khác với giá trị mặc định, trong đó phần tử được tạo riêng lẻ.

.. index:: single: ? (question mark); in argparse module

* ``'?'``. Nếu có thể, một đối số sẽ được lấy từ dòng lệnh và tạo ra dưới dạng một phần tử duy nhất. Nếu không có đối số dòng lệnh nào, giá trị từ default_ sẽ được tạo ra. Lưu ý rằng đối với các đối số tùy chọn, có thêm một trường hợp: chuỗi tùy chọn xuất hiện nhưng không theo sau bởi một đối số dòng lệnh. Trong trường hợp này, giá trị từ const_ sẽ được tạo ra. Một số ví dụ minh họa cho điều này::

     >>> parser = argparse.ArgumentParser()
     >>> parser.add_argument('--foo', nargs='?', const='c', default='d')
     >>> parser.add_argument('bar', nargs='?', default='d')
     >>> parser.parse_args(['XX', '--foo', 'YY'])
     Namespace(bar='XX', foo='YY')
     >>> parser.parse_args(['XX', '--foo'])
     Namespace(bar='XX', foo='c')
     >>> parser.parse_args([])
     Namespace(bar='d', foo='d')

  Một trong những cách sử dụng phổ biến hơn của ``nargs='?'`` là cho phép các tệp đầu vào và đầu ra là tùy chọn::

     >>> parser = argparse.ArgumentParser()
     >>> parser.add_argument('infile', nargs='?')
     >>> parser.add_argument('outfile', nargs='?')
     >>> parser.parse_args(['input.txt', 'output.txt'])
     Namespace(infile='input.txt', outfile='output.txt')
     >>> parser.parse_args(['input.txt'])
     Namespace(infile='input.txt', outfile=None)
     >>> parser.parse_args([])
     Namespace(infile=None, outfile=None)

.. index:: single: * (asterisk); in argparse module

* ``'*'``. Tất cả đối số dòng lệnh hiện có sẽ được tập hợp vào một danh sách. Lưu ý rằng nhìn chung, việc có nhiều hơn một đối số vị trí với ``nargs='*'`` không có nhiều ý nghĩa, nhưng có thể có nhiều đối số tùy chọn với ``nargs='*'``. Ví dụ::

     >>> parser = argparse.ArgumentParser()
     >>> parser.add_argument('--foo', nargs='*')
     >>> parser.add_argument('--bar', nargs='*')
     >>> parser.add_argument('baz', nargs='*')
     >>> parser.parse_args('a b --foo x y --bar 1 2'.split())
     Namespace(bar=['1', '2'], baz=['a', 'b'], foo=['x', 'y'])

.. index:: single: + (plus); in argparse module

* ``'+'``. Giống như ``'*'``, tất cả các đối số dòng lệnh hiện có đều được tập hợp vào một danh sách. Ngoài ra, một thông báo lỗi sẽ được tạo nếu không có ít nhất một đối số dòng lệnh. Ví dụ::

     >>> parser = argparse.ArgumentParser(prog='PROG')
     >>> parser.add_argument('foo', nargs='+')
     >>> parser.parse_args(['a', 'b'])
     Namespace(foo=['a', 'b'])
     >>> parser.parse_args([])
     usage: PROG [-h] foo [foo ...]
     PROG: error: the following arguments are required: foo

Nếu không cung cấp đối số từ khóa ``nargs``, số lượng đối số được tiếp nhận sẽ được xác định bởi action_. Nhìn chung, điều này có nghĩa là một đối số dòng lệnh sẽ được tiếp nhận và một mục đơn (không phải danh sách) sẽ được tạo. Các action không tiếp nhận đối số dòng lệnh (ví dụ: ``'store_const'``) sẽ đặt ``nargs=0``.


.. _const:

const
^^^^^

Đối số ``const`` của :meth:`~ArgumentParser.add_argument` được dùng để lưu giữ các giá trị hằng số không được đọc từ dòng lệnh nhưng cần thiết cho nhiều action :class:`ArgumentParser`. Hai cách sử dụng phổ biến nhất là:

* Khi :meth:`~ArgumentParser.add_argument` được gọi với ``action='store_const'`` hoặc ``action='append_const'``. Các action này thêm giá trị ``const`` vào một trong các thuộc tính của đối tượng được trả về bởi
  :meth:`~ArgumentParser.parse_args`. Xem phần mô tả action_ để biết ví dụ. Nếu không cung cấp ``const`` cho :meth:`~ArgumentParser.add_argument`, nó sẽ nhận giá trị mặc định là ``None``.


* Khi :meth:`~ArgumentParser.add_argument` được gọi với các chuỗi tùy chọn (chẳng hạn như ``-f`` hoặc ``--foo``) và ``nargs='?'``. Điều này tạo ra một đối số tùy chọn có thể được theo sau bởi không hoặc một đối số dòng lệnh. Khi phân tích cú pháp dòng lệnh, nếu gặp chuỗi tùy chọn mà không có đối số dòng lệnh nào theo sau, giá trị từ ``const`` sẽ được sử dụng. Xem phần mô tả nargs_ để biết ví dụ.

.. versionchanged:: 3.11
   ``const=None`` theo mặc định, kể cả khi ``action='append_const'`` hoặc ``action='store_const'``.

.. _default:

mặc định
^^^^^^^^

Tất cả đối số tùy chọn và một số đối số vị trí có thể được bỏ qua trên dòng lệnh. Đối số từ khóa ``default`` của
:meth:`~ArgumentParser.add_argument`, có giá trị mặc định là ``None``, chỉ định giá trị sẽ được sử dụng nếu đối số dòng lệnh không xuất hiện. Đối với các đối số tùy chọn, giá trị ``default`` được sử dụng khi chuỗi tùy chọn không xuất hiện trên dòng lệnh::

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('--foo', default=42)
   >>> parser.parse_args(['--foo', '2'])
   Namespace(foo='2')
   >>> parser.parse_args([])
   Namespace(foo=42)

Nếu namespace đích đã có một thuộc tính được thiết lập, action *default* sẽ không ghi đè thuộc tính đó::

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('--foo', default=42)
   >>> parser.parse_args([], namespace=argparse.Namespace(foo=101))
   Namespace(foo=101)

Nếu giá trị ``default`` là một chuỗi, parser sẽ phân tích giá trị đó như thể nó là một đối số dòng lệnh. Cụ thể, parser sẽ áp dụng đối số chuyển đổi type_, nếu được cung cấp, trước khi thiết lập thuộc tính trên
giá trị trả về của :class:`Namespace`. Nếu không, parser sẽ sử dụng nguyên trạng giá trị đó::

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('--length', default='10', type=int)
   >>> parser.add_argument('--width', default=10.5, type=int)
   >>> parser.parse_args()
   Namespace(length=10, width=10.5)

Đối với các positional argument có nargs_ bằng ``?`` hoặc ``*``, giá trị ``default`` sẽ được sử dụng khi không có đối số dòng lệnh nào được cung cấp::

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('foo', nargs='?', default=42)
   >>> parser.parse_args(['a'])
   Namespace(foo='a')
   >>> parser.parse_args([])
   Namespace(foo=42)

Vì ``nargs='*'`` tập hợp mọi giá trị được cung cấp vào một danh sách, positional argument bị bỏ qua sẽ tạo ra một danh sách rỗng (``[]``). Chỉ *default* không phải ``None`` mới ghi đè hành vi này (vì vậy ``default=None`` vẫn cho kết quả ``[]``).

Đối với các argument required_, giá trị ``default`` sẽ bị bỏ qua. Ví dụ, điều này áp dụng cho các positional argument có giá trị nargs_ khác ``?`` hoặc ``*``, hoặc các optional argument được đánh dấu là ``required=True``.

Việc cung cấp ``default=argparse.SUPPRESS`` sẽ không thêm thuộc tính nào nếu đối số dòng lệnh không được cung cấp::

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('--foo', default=argparse.SUPPRESS)
   >>> parser.parse_args([])
   Namespace()
   >>> parser.parse_args(['--foo', '1'])
   Namespace(foo='1')


.. _argparse-type:

type
^^^^

Theo mặc định, parser đọc các đối số dòng lệnh dưới dạng các chuỗi đơn giản. Tuy nhiên, khá thường xuyên chuỗi dòng lệnh cần được diễn giải thành một kiểu khác, chẳng hạn như :class:`float` hoặc :class:`int`. Từ khóa ``type`` dành cho :meth:`~ArgumentParser.add_argument` cho phép thực hiện mọi thao tác kiểm tra kiểu và chuyển đổi kiểu cần thiết.

Nếu sử dụng từ khóa type_ cùng với từ khóa default_, bộ chuyển đổi kiểu chỉ được áp dụng nếu giá trị mặc định là một chuỗi.

Đối số của ``type`` có thể là một callable nhận một chuỗi duy nhất hoặc tên của một kiểu đã đăng ký (xem :meth:`~ArgumentParser.register`) Nếu hàm phát sinh :exc:`ArgumentTypeError`, :exc:`TypeError`, hoặc
:exc:`ValueError`, exception đó sẽ được bắt và một thông báo lỗi được định dạng rõ ràng sẽ hiển thị. Các kiểu exception khác không được xử lý.

Có thể sử dụng các kiểu và hàm dựng sẵn phổ biến làm type converter:

.. testcode::

   import argparse
   import pathlib

   parser = argparse.ArgumentParser()
   parser.add_argument('count', type=int)
   parser.add_argument('distance', type=float)
   parser.add_argument('street', type=ascii)
   parser.add_argument('code_point', type=ord)
   parser.add_argument('datapath', type=pathlib.Path)

Bạn cũng có thể sử dụng các hàm do người dùng định nghĩa:

.. doctest::

   >>> def hyphenated(string):
   ...     return '-'.join([word[:4] for word in string.casefold().split()])
   ...
   >>> parser = argparse.ArgumentParser()
   >>> _ = parser.add_argument('short_title', type=hyphenated)
   >>> parser.parse_args(['"The Tale of Two Cities"'])
   Namespace(short_title='"the-tale-of-two-citi')

Không nên sử dụng hàm :func:`bool` làm type converter. Hàm này chỉ chuyển đổi chuỗi rỗng thành ``False`` và chuỗi không rỗng thành ``True``. Đây thường không phải là điều mong muốn::

   >>> parser = argparse.ArgumentParser()
   >>> _ = parser.add_argument('--verbose', type=bool)
   >>> parser.parse_args(['--verbose', 'False'])
   Namespace(verbose=True)

Xem :class:`BooleanOptionalAction` hoặc ``action='store_true'`` để biết các lựa chọn thay thế phổ biến.

Nhìn chung, từ khóa ``type`` là một tiện ích chỉ nên được dùng cho các chuyển đổi đơn giản, vốn chỉ có thể phát sinh một trong ba exception được hỗ trợ. Mọi thao tác có xử lý lỗi hoặc quản lý tài nguyên phức tạp hơn nên được thực hiện ở downstream sau khi các đối số đã được phân tích.

Ví dụ, các chuyển đổi JSON hoặc YAML có những trường hợp lỗi phức tạp, đòi hỏi cách báo cáo tốt hơn mức mà từ khóa ``type`` có thể cung cấp. Một
:exc:`~json.JSONDecodeError` sẽ không được định dạng tốt và một
ngoại lệ :exc:`FileNotFoundError` sẽ hoàn toàn không được xử lý.

Ngay cả :class:`~argparse.FileType` cũng có những hạn chế khi dùng với từ khóa ``type``. Nếu một đối số sử dụng :class:`~argparse.FileType` rồi một đối số tiếp theo bị lỗi, một lỗi được báo cáo nhưng tệp không tự động đóng. Trong trường hợp này, tốt hơn là đợi đến khi parser chạy xong rồi dùng câu lệnh :keyword:`with` để quản lý các tệp.

Đối với các trình kiểm tra kiểu chỉ kiểm tra dựa trên một tập giá trị cố định, hãy cân nhắc sử dụng từ khóa choices_ thay thế.


.. _choices:

choices
^^^^^^^

Một số đối số dòng lệnh phải được chọn từ một tập giá trị giới hạn. Có thể xử lý các đối số này bằng cách truyền một đối tượng sequence làm đối số từ khóa *choices* cho :meth:`~ArgumentParser.add_argument`. Khi dòng lệnh được phân tích cú pháp, các giá trị đối số sẽ được kiểm tra và một thông báo lỗi sẽ hiển thị nếu đối số không thuộc một trong các giá trị được chấp nhận::

   >>> parser = argparse.ArgumentParser(prog='game.py')
   >>> parser.add_argument('move', choices=['rock', 'paper', 'scissors'])
   >>> parser.parse_args(['rock'])
   Namespace(move='rock')
   >>> parser.parse_args(['fire'])
   usage: game.py [-h] {rock,paper,scissors}
   game.py: error: argument move: invalid choice: 'fire' (choose from 'rock',
   'paper', 'scissors')

Bất kỳ sequence nào cũng có thể được truyền làm giá trị *choices*, vì vậy các đối tượng :class:`list` cũng được hỗ trợ,
các đối tượng :class:`tuple` và sequence tùy chỉnh đều được hỗ trợ.

Không nên sử dụng :class:`enum.Enum` vì khó kiểm soát cách nó xuất hiện trong các thông báo về cách sử dụng, trợ giúp và lỗi.

Lưu ý rằng *choices* được kiểm tra sau khi mọi phép chuyển đổi type_ đã được thực hiện, vì vậy các đối tượng trong *choices* phải khớp với type_ được chỉ định. Điều này có thể khiến *choices* trông không quen thuộc trong các thông báo về cách sử dụng, trợ giúp hoặc lỗi.

Để *choices* thân thiện với người dùng, hãy cân nhắc một trình bao bọc kiểu tùy chỉnh để chuyển đổi và định dạng các giá trị, hoặc bỏ qua type_ và xử lý việc chuyển đổi trong mã ứng dụng của bạn.

Các choices được định dạng sẽ ghi đè *metavar* mặc định, vốn thường được suy ra từ *dest*. Đây thường là điều bạn muốn vì người dùng không bao giờ thấy tham số *dest*. Nếu cách hiển thị này không phù hợp (có thể vì có nhiều choices), chỉ cần chỉ định một metavar_ rõ ràng.


.. _required:

bắt buộc
^^^^^^^^

Nhìn chung, module :mod:`!argparse` giả định rằng các cờ như ``-f`` và ``--bar`` cho biết các đối số *tùy chọn*, luôn có thể được bỏ qua trên dòng lệnh. Để một tùy chọn trở thành *bắt buộc*, có thể chỉ định ``True`` cho đối số từ khóa ``required=`` của :meth:`~ArgumentParser.add_argument`::

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('--foo', required=True)
   >>> parser.parse_args(['--foo', 'BAR'])
   Namespace(foo='BAR')
   >>> parser.parse_args([])
   usage: [-h] --foo FOO
   : error: the following arguments are required: --foo

Như ví dụ cho thấy, nếu một tùy chọn được đánh dấu là ``required``,
:meth:`~ArgumentParser.parse_args` sẽ báo lỗi nếu tùy chọn đó không có trên dòng lệnh.

.. note::

    Các tùy chọn bắt buộc thường bị xem là không phù hợp vì người dùng mong đợi các *tùy chọn* là *tùy chọn*, do đó nên tránh chúng khi có thể.


.. _help:

trợ giúp
^^^^^^^^

Giá trị ``help`` là một chuỗi chứa mô tả ngắn gọn về đối số. Khi người dùng yêu cầu trợ giúp (thường bằng cách sử dụng ``-h`` hoặc ``--help`` trên dòng lệnh), các mô tả ``help`` này sẽ được hiển thị cùng với từng đối số.

Các chuỗi ``help`` có thể bao gồm nhiều bộ chỉ định định dạng khác nhau để tránh lặp lại những nội dung như tên chương trình hoặc default_ của đối số. Các bộ chỉ định khả dụng bao gồm tên chương trình, ``%(prog)s`` và hầu hết các đối số từ khóa của
:meth:`~ArgumentParser.add_argument`, ví dụ ``%(default)s``, ``%(type)s``, v.v.::

   >>> parser = argparse.ArgumentParser(prog='frobble')
   >>> parser.add_argument('bar', nargs='?', type=int, default=42,
   ...                     help='the bar to %(prog)s (default: %(default)s)')
   >>> parser.print_help()
   usage: frobble [-h] [bar]

   positional arguments:
    bar     the bar to frobble (default: 42)

   options:
    -h, --help  show this help message and exit

Vì chuỗi trợ giúp hỗ trợ %-formatting, nếu bạn muốn một ``%`` literal xuất hiện trong chuỗi trợ giúp, bạn phải escape nó thành ``%%``.

:mod:`!argparse` hỗ trợ ẩn mục trợ giúp đối với một số tùy chọn bằng cách đặt giá trị ``help`` thành ``argparse.SUPPRESS``::

   >>> parser = argparse.ArgumentParser(prog='frobble')
   >>> parser.add_argument('--foo', help=argparse.SUPPRESS)
   >>> parser.print_help()
   usage: frobble [-h]

   options:
     -h, --help  show this help message and exit


.. _metavar:

metavar
^^^^^^^

Khi :class:`ArgumentParser` tạo thông báo trợ giúp, nó cần một cách để tham chiếu đến từng đối số dự kiến. Theo mặc định, các đối tượng :class:`!ArgumentParser` sử dụng giá trị dest_ làm "tên" của mỗi đối tượng. Theo mặc định, đối với các action của đối số vị trí, giá trị dest_ được sử dụng trực tiếp, còn đối với các action của đối số tùy chọn, giá trị dest_ được viết hoa. Vì vậy, một đối số vị trí duy nhất với ``dest='bar'`` sẽ được tham chiếu là ``bar``. Một đối số tùy chọn duy nhất ``--foo`` cần được theo sau bởi một đối số dòng lệnh duy nhất sẽ được tham chiếu là ``FOO``. Ví dụ::

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('--foo')
   >>> parser.add_argument('bar')
   >>> parser.parse_args('X --foo Y'.split())
   Namespace(bar='X', foo='Y')
   >>> parser.print_help()
   usage:  [-h] [--foo FOO] bar

   positional arguments:
    bar

   options:
    -h, --help  show this help message and exit
    --foo FOO

Có thể chỉ định một tên thay thế bằng ``metavar``::

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('--foo', metavar='YYY')
   >>> parser.add_argument('bar', metavar='XXX')
   >>> parser.parse_args('X --foo Y'.split())
   Namespace(bar='X', foo='Y')
   >>> parser.print_help()
   usage:  [-h] [--foo YYY] XXX

   positional arguments:
    XXX

   options:
    -h, --help  show this help message and exit
    --foo YYY

Lưu ý rằng ``metavar`` chỉ thay đổi tên *được hiển thị* - tên của thuộc tính trên đối tượng :meth:`~ArgumentParser.parse_args` vẫn được xác định bởi giá trị dest_.

Các giá trị khác nhau của ``nargs`` có thể khiến metavar được sử dụng nhiều lần. Cung cấp một tuple cho ``metavar`` sẽ chỉ định cách hiển thị khác nhau cho từng đối số::

   >>> parser = argparse.ArgumentParser(prog='PROG')
   >>> parser.add_argument('-x', nargs=2)
   >>> parser.add_argument('--foo', nargs=2, metavar=('bar', 'baz'))
   >>> parser.print_help()
   usage: PROG [-h] [-x X X] [--foo bar baz]

   options:
    -h, --help     show this help message and exit
    -x X X
    --foo bar baz


.. _dest:

dest
^^^^

Hầu hết các action của :class:`ArgumentParser` đều thêm một giá trị làm thuộc tính của đối tượng được :meth:`~ArgumentParser.parse_args` trả về. Tên của thuộc tính này được xác định bởi đối số từ khóa ``dest`` của
:meth:`~ArgumentParser.add_argument`. Đối với các action của positional argument, ``dest`` thường được cung cấp làm đối số đầu tiên cho
:meth:`~ArgumentParser.add_argument`::

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('bar')
   >>> parser.parse_args(['XXX'])
   Namespace(bar='XXX')

Đối với các action của optional argument, giá trị của ``dest`` thường được suy ra từ các option string. :class:`ArgumentParser` tạo giá trị của ``dest`` bằng cách lấy option string dài đầu tiên và loại bỏ chuỗi ``--`` ở đầu. Nếu không cung cấp option string dài nào, ``dest`` sẽ được suy ra từ option string ngắn đầu tiên bằng cách loại bỏ ký tự ``-`` ở đầu. Mọi ký tự ``-`` bên trong sẽ được chuyển thành ký tự ``_`` để đảm bảo chuỗi này là một tên thuộc tính hợp lệ. Các ví dụ dưới đây minh họa hành vi này::

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('-f', '--foo-bar', '--foo')
   >>> parser.add_argument('-x', '-y')
   >>> parser.parse_args('-f 1 -x 2'.split())
   Namespace(foo_bar='1', x='2')
   >>> parser.parse_args('--foo 1 -y 2'.split())
   Namespace(foo_bar='1', x='2')

``dest`` cho phép cung cấp một tên thuộc tính tùy chỉnh::

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument('--foo', dest='bar')
   >>> parser.parse_args('--foo XXX'.split())
   Namespace(bar='XXX')

Nhiều đối số có thể dùng chung một ``dest``. Theo mặc định, giá trị từ đối số như vậy được cung cấp sau cùng trên dòng lệnh sẽ được sử dụng. Thay vào đó, hãy dùng ``action='append'`` để thu thập các giá trị từ tất cả chúng vào một danh sách. Đối với các *chuỗi tùy chọn* xung đột thay vì các tên ``dest``, hãy xem conflict_handler_.

.. _deprecated:

không còn được dùng
^^^^^^^^^^^^^^^^^^^

Trong vòng đời của một dự án, một số đối số có thể cần được xóa khỏi dòng lệnh. Trước khi xóa chúng, bạn nên thông báo cho người dùng rằng các đối số này không còn được dùng và sẽ bị xóa. Đối số từ khóa ``deprecated`` của
:meth:`~ArgumentParser.add_argument`, mặc định là ``False``, xác định liệu đối số có không còn được dùng và sẽ bị xóa trong tương lai hay không. Đối với các đối số, nếu ``deprecated`` là ``True``, một cảnh báo sẽ được in ra :data:`sys.stderr` khi đối số được sử dụng::

   >>> import argparse
   >>> parser = argparse.ArgumentParser(prog='snake.py')
   >>> parser.add_argument('--legs', default=0, type=int, deprecated=True)
   >>> parser.parse_args([])
   Namespace(legs=0)
   >>> parser.parse_args(['--legs', '4'])  # doctest: +SKIP
   snake.py: warning: option '--legs' is deprecated
   Namespace(legs=4)

.. versionadded:: 3.13


Các lớp Action
^^^^^^^^^^^^^^

Các lớp :class:`!Action` triển khai Action API, một callable trả về một callable xử lý các đối số từ dòng lệnh. Bất kỳ đối tượng nào tuân theo API này đều có thể được truyền làm tham số ``action`` cho
:meth:`~ArgumentParser.add_argument`.

.. class:: Action(option_strings, dest, nargs=None, const=None, default=None, \
                  type=None, choices=None, required=False, help=None, \ metavar=None)

   Các đối tượng :class:`!Action` được một :class:`ArgumentParser` sử dụng để biểu diễn thông tin cần thiết nhằm phân tích cú pháp một đối số từ một hoặc nhiều chuỗi trên dòng lệnh. Lớp :class:`!Action` phải chấp nhận hai đối số vị trí cùng mọi đối số từ khóa được truyền vào :meth:`ArgumentParser.add_argument`, ngoại trừ chính ``action``.

   Các instance của :class:`!Action` (hoặc giá trị trả về của bất kỳ callable nào được truyền cho tham số ``action``) phải có các thuộc tính :attr:`!dest`,
   :attr:`!option_strings`, :attr:`!default`, :attr:`!type`, :attr:`!required`,
   :attr:`!help`, v.v. được định nghĩa. Cách dễ nhất để đảm bảo các thuộc tính này được định nghĩa là gọi :meth:`!Action.__init__`.

   .. method:: __call__(parser, namespace, values, option_string=None)

      Các instance của :class:`!Action` phải là callable, vì vậy các lớp con phải ghi đè
      phương thức :meth:`!__call__`, phương thức này phải chấp nhận bốn tham số:

      * *parser* - Đối tượng :class:`ArgumentParser` chứa action này.

      * *namespace* - Đối tượng :class:`Namespace` sẽ được trả về bởi
        :meth:`~ArgumentParser.parse_args`. Hầu hết các action đều thêm một thuộc tính vào đối tượng này bằng cách sử dụng :func:`setattr`.

      * *values* - Các đối số dòng lệnh tương ứng, với mọi chuyển đổi kiểu đã được áp dụng. Chuyển đổi kiểu được chỉ định bằng đối số từ khóa type_ cho
        :meth:`~ArgumentParser.add_argument`.

      * *option_string* - Chuỗi tùy chọn đã được sử dụng để gọi action này. Đối số ``option_string`` là tùy chọn và sẽ không tồn tại nếu action được liên kết với một đối số vị trí.

      Phương thức :meth:`!__call__` có thể thực hiện các hành động tùy ý, nhưng thường sẽ thiết lập các thuộc tính trên ``namespace`` dựa trên ``dest`` và ``values``.

   .. method:: format_usage()

      Các lớp con của :class:`!Action` có thể định nghĩa một phương thức :meth:`!format_usage` không nhận đối số và trả về một chuỗi sẽ được sử dụng khi in phần hướng dẫn sử dụng của chương trình. Nếu không cung cấp phương thức này, một giá trị mặc định hợp lý sẽ được sử dụng.

.. class:: BooleanOptionalAction

   Một lớp con của :class:`Action` dùng để xử lý các cờ boolean với các tùy chọn khẳng định và phủ định. Việc thêm một đối số duy nhất như ``--foo`` sẽ tự động tạo cả hai tùy chọn ``--foo`` và ``--no-foo``, lần lượt lưu trữ ``True`` và ``False``::

       >>> import argparse
       >>> parser = argparse.ArgumentParser()
       >>> parser.add_argument('--foo', action=argparse.BooleanOptionalAction)
       >>> parser.parse_args(['--no-foo'])
       Namespace(foo=False)

   .. versionadded:: 3.9


Phương thức parse_args()
------------------------

.. method:: ArgumentParser.parse_args(args=None, namespace=None)

   Chuyển đổi các chuỗi đối số thành các đối tượng và gán chúng làm thuộc tính của namespace. Trả về namespace đã được điền dữ liệu.

   Các lần gọi trước đó đến :meth:`add_argument` xác định chính xác những đối tượng nào được tạo và cách chúng được gán. Xem tài liệu về
   :meth:`!add_argument` để biết chi tiết.

   * args_ - Danh sách các chuỗi cần phân tích cú pháp. Giá trị mặc định được lấy từ
     :data:`sys.argv`.

   * namespace_ - Một đối tượng để nhận các thuộc tính. Mặc định là một đối tượng mới, rỗng
     :class:`Namespace`.


Cú pháp giá trị tùy chọn
^^^^^^^^^^^^^^^^^^^^^^^^

Phương thức :meth:`~ArgumentParser.parse_args` hỗ trợ một số cách chỉ định giá trị của một tùy chọn (nếu tùy chọn đó nhận giá trị). Trong trường hợp đơn giản nhất, tùy chọn và giá trị của nó được truyền dưới dạng hai đối số riêng biệt::

   >>> parser = argparse.ArgumentParser(prog='PROG')
   >>> parser.add_argument('-x')
   >>> parser.add_argument('--foo')
   >>> parser.parse_args(['-x', 'X'])
   Namespace(foo=None, x='X')
   >>> parser.parse_args(['--foo', 'FOO'])
   Namespace(foo='FOO', x=None)

Đối với các tùy chọn dài (các tùy chọn có tên dài hơn một ký tự), tùy chọn và giá trị cũng có thể được truyền dưới dạng một đối số dòng lệnh duy nhất, sử dụng ``=`` để phân tách chúng::

   >>> parser.parse_args(['--foo=FOO'])
   Namespace(foo='FOO', x=None)

Đối với các tùy chọn ngắn (các tùy chọn chỉ dài một ký tự), tùy chọn và giá trị của nó có thể được nối lại với nhau::

   >>> parser.parse_args(['-xX'])
   Namespace(foo=None, x='X')

Có thể nối nhiều tùy chọn ngắn với nhau, chỉ sử dụng một tiền tố ``-``, miễn là chỉ tùy chọn cuối cùng (hoặc không có tùy chọn nào) yêu cầu giá trị::

   >>> parser = argparse.ArgumentParser(prog='PROG')
   >>> parser.add_argument('-x', action='store_true')
   >>> parser.add_argument('-y', action='store_true')
   >>> parser.add_argument('-z')
   >>> parser.parse_args(['-xyzZ'])
   Namespace(x=True, y=True, z='Z')


Đối số không hợp lệ
^^^^^^^^^^^^^^^^^^^

Trong khi phân tích cú pháp dòng lệnh, :meth:`~ArgumentParser.parse_args` kiểm tra nhiều loại lỗi, bao gồm các tùy chọn không rõ ràng, kiểu không hợp lệ, tùy chọn không hợp lệ, số lượng đối số vị trí không đúng, v.v. Khi gặp lỗi như vậy, nó sẽ thoát và in lỗi cùng với thông báo hướng dẫn sử dụng::

   >>> parser = argparse.ArgumentParser(prog='PROG')
   >>> parser.add_argument('--foo', type=int)
   >>> parser.add_argument('bar', nargs='?')

   >>> # kiểu không hợp lệ
   >>> parser.parse_args(['--foo', 'spam'])
   usage: PROG [-h] [--foo FOO] [bar]
   PROG: error: argument --foo: invalid int value: 'spam'

   >>> # tùy chọn không hợp lệ
   >>> parser.parse_args(['--bar'])
   usage: PROG [-h] [--foo FOO] [bar]
   PROG: error: unrecognized arguments: --bar

   >>> # số lượng đối số không đúng
   >>> parser.parse_args(['spam', 'badger'])
   usage: PROG [-h] [--foo FOO] [bar]
   PROG: error: unrecognized arguments: badger


Các đối số chứa ``-``
^^^^^^^^^^^^^^^^^^^^^

Phương thức :meth:`~ArgumentParser.parse_args` cố gắng đưa ra lỗi bất cứ khi nào người dùng rõ ràng đã mắc lỗi, nhưng một số tình huống vốn dĩ không rõ ràng. Ví dụ: đối số dòng lệnh ``-1`` có thể là nỗ lực chỉ định một tùy chọn hoặc nỗ lực cung cấp một đối số vị trí. Phương thức :meth:`~ArgumentParser.parse_args` thận trọng trong trường hợp này: các đối số vị trí chỉ có thể bắt đầu bằng ``-`` nếu chúng có dạng số âm và parser không có tùy chọn nào có dạng số âm::

   >>> parser = argparse.ArgumentParser(prog='PROG')
   >>> parser.add_argument('-x')
   >>> parser.add_argument('foo', nargs='?')

   >>> # không có tùy chọn số âm, vì vậy -1 là một đối số vị trí
   >>> parser.parse_args(['-x', '-1'])
   Namespace(foo=None, x='-1')

   >>> # không có tùy chọn số âm, vì vậy -1 và -5 là các đối số vị trí
   >>> parser.parse_args(['-x', '-1', '-5'])
   Namespace(foo='-5', x='-1')

   >>> parser = argparse.ArgumentParser(prog='PROG')
   >>> parser.add_argument('-1', dest='one')
   >>> parser.add_argument('foo', nargs='?')

   >>> # có tùy chọn số âm, vì vậy -1 là một tùy chọn
   >>> parser.parse_args(['-1', 'X'])
   Namespace(foo=None, one='X')

   >>> # có các tùy chọn là số âm, nên -2 là một tùy chọn
   >>> parser.parse_args(['-2'])
   usage: PROG [-h] [-1 ONE] [foo]
   PROG: error: unrecognized arguments: -2

   >>> # có các tùy chọn là số âm, nên cả hai -1 đều là tùy chọn
   >>> parser.parse_args(['-1', '-1'])
   usage: PROG [-h] [-1 ONE] [foo]
   PROG: error: argument -1: expected one argument

Nếu bạn có các đối số vị trí phải bắt đầu bằng ``-`` và không có dạng số âm, bạn có thể chèn đối số giả ``'--'`` để cho biết
:meth:`~ArgumentParser.parse_args` rằng mọi thứ sau đó đều là đối số vị trí::

   >>> parser.parse_args(['--', '-f'])
   Namespace(foo='-f', one=None)

Xem thêm :ref:`hướng dẫn argparse về các đối số không rõ ràng <specifying-ambiguous-arguments>` để biết thêm chi tiết.

.. versionchanged:: 3.14
   Việc nhận diện số âm đã được mở rộng để bao gồm các số ở dạng ký hiệu khoa học (``-2.5e-6``), các số có chứa dấu gạch dưới (``-1_234.5``) và các số phức (``-1.2e-3j``).

.. _prefix-matching:

Viết tắt đối số (so khớp tiền tố)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Phương thức :meth:`~ArgumentParser.parse_args` :ref:`theo mặc định <allow_abbrev>` cho phép viết tắt các tùy chọn dài thành một tiền tố, nếu cách viết tắt đó không gây mơ hồ (tiền tố khớp với một tùy chọn duy nhất)::

   >>> parser = argparse.ArgumentParser(prog='PROG')
   >>> parser.add_argument('-bacon')
   >>> parser.add_argument('-badger')
   >>> parser.parse_args('-bac MMM'.split())
   Namespace(bacon='MMM', badger=None)
   >>> parser.parse_args('-bad WOOD'.split())
   Namespace(bacon=None, badger='WOOD')
   >>> parser.parse_args('-ba BA'.split())
   usage: PROG [-h] [-bacon BACON] [-badger BADGER]
   PROG: error: ambiguous option: -ba could match -badger, -bacon

Một lỗi sẽ được tạo ra đối với các đối số có thể khớp với nhiều tùy chọn. Có thể vô hiệu hóa tính năng này bằng cách đặt :ref:`allow_abbrev` thành ``False``.

.. _args:

Ngoài ``sys.argv``
^^^^^^^^^^^^^^^^^^

Đôi khi, việc yêu cầu :class:`ArgumentParser` phân tích cú pháp các đối số khác với các đối số của :data:`sys.argv` có thể hữu ích. Có thể thực hiện việc này bằng cách truyền một danh sách chuỗi cho
:meth:`~ArgumentParser.parse_args`. Điều này hữu ích khi kiểm thử tại dấu nhắc tương tác::

   >>> parser = argparse.ArgumentParser()
   >>> parser.add_argument(
   ...     'integers', metavar='int', type=int, choices=range(10),
   ...     nargs='+', help='an integer in the range 0..9')
   >>> parser.add_argument(
   ...     '--sum', dest='accumulate', action='store_const', const=sum,
   ...     default=max, help='sum the integers (default: find the max)')
   >>> parser.parse_args(['1', '2', '3', '4'])
   Namespace(accumulate=<built-in function max>, integers=[1, 2, 3, 4])
   >>> parser.parse_args(['1', '2', '3', '4', '--sum'])
   Namespace(accumulate=<built-in function sum>, integers=[1, 2, 3, 4])

.. _namespace:

Đối tượng Namespace
^^^^^^^^^^^^^^^^^^^

.. class:: Namespace

   Lớp đơn giản được :meth:`~ArgumentParser.parse_args` sử dụng theo mặc định để tạo một đối tượng chứa các thuộc tính và trả về đối tượng đó.

   Lớp này được thiết kế đơn giản, chỉ là một lớp con :class:`object` với biểu diễn chuỗi dễ đọc. Nếu bạn muốn có dạng xem các thuộc tính giống dict, bạn có thể sử dụng thành ngữ Python tiêu chuẩn, :func:`vars`::

      >>> parser = argparse.ArgumentParser()
      >>> parser.add_argument('--foo')
      >>> args = parser.parse_args(['--foo', 'BAR'])
      >>> vars(args)
      {'foo': 'BAR'}

   Việc để :class:`ArgumentParser` gán các thuộc tính cho một đối tượng đã tồn tại, thay vì một đối tượng :class:`Namespace` mới, cũng có thể hữu ích. Bạn có thể thực hiện điều này bằng cách chỉ định đối số từ khóa ``namespace=``::

      >>> class C:
      ...     pass
      ...
      >>> c = C()
      >>> parser = argparse.ArgumentParser()
      >>> parser.add_argument('--foo')
      >>> parser.parse_args(args=['--foo', 'BAR'], namespace=c)
      >>> c.foo
      'BAR'


Các tiện ích khác
-----------------

Các lệnh con
^^^^^^^^^^^^

.. method:: ArgumentParser.add_subparsers(*, [title], [description], [prog], \
                                          [parser_class], [action], \ [dest], [required], \ [help], [metavar])

   Nhiều chương trình chia chức năng thành một số lệnh con; chẳng hạn, chương trình ``svn`` có thể gọi các lệnh con như ``svn checkout``, ``svn update`` và ``svn commit``. Việc chia chức năng theo cách này có thể đặc biệt hữu ích khi một chương trình thực hiện nhiều chức năng khác nhau, yêu cầu các loại đối số dòng lệnh khác nhau.
   :class:`ArgumentParser` hỗ trợ tạo các lệnh con như vậy với
   :meth:`!add_subparsers` phương thức. Phương thức :meth:`!add_subparsers` thường được gọi mà không có đối số và trả về một đối tượng action đặc biệt. Đối tượng này có một phương thức duy nhất là :meth:`~_SubParsersAction.add_parser`, nhận tên lệnh và bất kỳ đối số constructor :class:`!ArgumentParser` nào, rồi trả về một đối tượng :class:`!ArgumentParser` có thể được sửa đổi như bình thường.

   Mô tả các tham số:

   * *title* - tiêu đề cho nhóm sub-parser trong phần đầu ra trợ giúp; mặc định là "subcommands" nếu description được cung cấp, nếu không thì sử dụng title cho các đối số vị trí

   * *description* - mô tả cho nhóm sub-parser trong phần đầu ra trợ giúp, mặc định là ``None``

   * *prog* - thông tin sử dụng sẽ được hiển thị cùng với phần trợ giúp của subcommand, mặc định là tên chương trình và mọi đối số vị trí nằm trước đối số subparser

   * *parser_class* - class sẽ được sử dụng để tạo các instance sub-parser, mặc định là class của parser hiện tại (ví dụ: :class:`ArgumentParser`)

   * action_ - loại action cơ bản sẽ được thực hiện khi gặp đối số này trên dòng lệnh

   * dest_ - tên của thuộc tính dùng để lưu tên subcommand; theo mặc định là ``None`` và không có giá trị nào được lưu

   * required_ - subcommand có bắt buộc phải được cung cấp hay không, theo mặc định là ``False`` (được thêm trong 3.7)

   * help_ - phần trợ giúp cho nhóm sub-parser trong phần hiển thị trợ giúp, theo mặc định là ``None``

   * metavar_ - chuỗi hiển thị các subcommand hiện có trong phần trợ giúp; theo mặc định là ``None`` và hiển thị các subcommand dưới dạng {cmd1, cmd2, ..}

   Một số ví dụ sử dụng::

     >>> # tạo parser cấp cao nhất
     >>> parser = argparse.ArgumentParser(prog='PROG')
     >>> parser.add_argument('--foo', action='store_true', help='foo help')
     >>> subparsers = parser.add_subparsers(help='subcommand help')
     >>>
     >>> # tạo parser cho lệnh "a"
     >>> parser_a = subparsers.add_parser('a', help='a help')
     >>> parser_a.add_argument('bar', type=int, help='bar help')
     >>>
     >>> # tạo parser cho lệnh "b"
     >>> parser_b = subparsers.add_parser('b', help='b help')
     >>> parser_b.add_argument('--baz', choices=('X', 'Y', 'Z'), help='baz help')
     >>>
     >>> # phân tích một số danh sách đối số
     >>> parser.parse_args(['a', '12'])
     Namespace(bar=12, foo=False)
     >>> parser.parse_args(['--foo', 'b', '--baz', 'Z'])
     Namespace(baz='Z', foo=True)

   Lưu ý rằng đối tượng được trả về bởi :meth:`parse_args` sẽ chỉ chứa các thuộc tính của parser chính và subparser được chọn trên dòng lệnh (không chứa bất kỳ subparser nào khác). Vì vậy, trong ví dụ trên, khi chỉ định lệnh ``a``, chỉ các thuộc tính ``foo`` và ``bar`` hiện diện; còn khi chỉ định lệnh ``b``, chỉ các thuộc tính ``foo`` và ``baz`` hiện diện.

   Nếu một subparser định nghĩa một đối số có cùng ``dest`` với parser cha, cả hai sẽ dùng chung một thuộc tính namespace, nên giá trị của parser cha sẽ không được giữ lại. Người dùng nên cung cấp cho chúng các giá trị ``dest`` khác nhau để giữ lại cả hai.

   Tương tự, khi yêu cầu thông báo trợ giúp từ một subparser, chỉ thông báo trợ giúp của parser cụ thể đó được in ra. Thông báo trợ giúp sẽ không bao gồm thông báo của parser cha hoặc parser cùng cấp. (Tuy nhiên, có thể cung cấp thông báo trợ giúp cho từng lệnh subparser bằng cách truyền đối số ``help=`` cho :meth:`~_SubParsersAction.add_parser` như trên.)

   ::

     >>> parser.parse_args(['--help'])
     usage: PROG [-h] [--foo] {a,b} ...

     positional arguments:
       {a,b}   subcommand help
         a     a help
         b     b help

     options:
       -h, --help  show this help message and exit
       --foo   foo help

     >>> parser.parse_args(['a', '--help'])
     usage: PROG a [-h] bar

     positional arguments:
       bar     bar help

     options:
       -h, --help  show this help message and exit

     >>> parser.parse_args(['b', '--help'])
     usage: PROG b [-h] [--baz {X,Y,Z}]

     options:
       -h, --help     show this help message and exit
       --baz {X,Y,Z}  baz help

   Phương thức :meth:`add_subparsers` cũng hỗ trợ các đối số keyword ``title`` và ``description``. Khi có một trong hai đối số này, các lệnh của subparser sẽ xuất hiện trong nhóm riêng của chúng trong phần đầu ra trợ giúp. Ví dụ:::

     >>> parser = argparse.ArgumentParser()
     >>> subparsers = parser.add_subparsers(title='subcommands',
     ...                                    description='valid subcommands',
     ...                                    help='additional help')
     >>> subparsers.add_parser('foo')
     >>> subparsers.add_parser('bar')
     >>> parser.parse_args(['-h'])
     usage:  [-h] {foo,bar} ...

     options:
       -h, --help  show this help message and exit

     subcommands:
       valid subcommands

       {foo,bar}   additional help

   Ngoài ra, :meth:`~_SubParsersAction.add_parser` hỗ trợ một đối số *aliases* bổ sung, cho phép dùng nhiều chuỗi để tham chiếu đến cùng một subparser. Ví dụ này, giống như ``svn``, dùng ``co`` làm bí danh viết tắt cho ``checkout``::

     >>> parser = argparse.ArgumentParser()
     >>> subparsers = parser.add_subparsers()
     >>> checkout = subparsers.add_parser('checkout', aliases=['co'])
     >>> checkout.add_argument('foo')
     >>> parser.parse_args(['co', 'bar'])
     Namespace(foo='bar')

   :meth:`~_SubParsersAction.add_parser` cũng hỗ trợ một đối số *deprecated*, cho phép đánh dấu subparser là không còn được khuyến nghị.

      >>> import argparse
      >>> parser = argparse.ArgumentParser(prog='chicken.py')
      >>> subparsers = parser.add_subparsers()
      >>> run = subparsers.add_parser('run')
      >>> fly = subparsers.add_parser('fly', deprecated=True)
      >>> parser.parse_args(['fly'])  # doctest: +SKIP
      chicken.py: warning: command 'fly' is deprecated
      Namespace()

   .. versionadded:: 3.13

   Một cách đặc biệt hiệu quả để xử lý các subcommand là kết hợp việc sử dụng phương thức :meth:`add_subparsers` với các lệnh gọi đến :meth:`set_defaults`, để mỗi subparser biết mình nên thực thi hàm Python nào. Ví dụ::

     >>> # các hàm subcommand
     >>> def foo(args):
     ...     print(args.x * args.y)
     ...
     >>> def bar(args):
     ...     print('((%s))' % args.z)
     ...
     >>> # tạo parser cấp cao nhất
     >>> parser = argparse.ArgumentParser()
     >>> subparsers = parser.add_subparsers(required=True)
     >>>
     >>> # tạo parser cho lệnh "foo"
     >>> parser_foo = subparsers.add_parser('foo')
     >>> parser_foo.add_argument('-x', type=int, default=1)
     >>> parser_foo.add_argument('y', type=float)
     >>> parser_foo.set_defaults(func=foo)
     >>>
     >>> # tạo parser cho lệnh "bar"
     >>> parser_bar = subparsers.add_parser('bar')
     >>> parser_bar.add_argument('z')
     >>> parser_bar.set_defaults(func=bar)
     >>>
     >>> # phân tích các đối số và gọi hàm đã được chọn
     >>> args = parser.parse_args('foo 1 -x 2'.split())
     >>> args.func(args)
     2.0
     >>>
     >>> # phân tích các đối số và gọi hàm đã được chọn
     >>> args = parser.parse_args('bar XYZYX'.split())
     >>> args.func(args)
     ((XYZYX))

   Bằng cách này, bạn có thể để :meth:`parse_args` thực hiện việc gọi hàm thích hợp sau khi hoàn tất phân tích đối số. Việc liên kết các hàm với những action như thế này thường là cách dễ nhất để xử lý các action khác nhau cho từng subparser. Tuy nhiên, nếu cần kiểm tra tên của subparser đã được gọi, đối số từ khóa ``dest`` trong lệnh gọi :meth:`add_subparsers` sẽ hoạt động::

     >>> parser = argparse.ArgumentParser()
     >>> subparsers = parser.add_subparsers(dest='subparser_name')
     >>> subparser1 = subparsers.add_parser('1')
     >>> subparser1.add_argument('-x')
     >>> subparser2 = subparsers.add_parser('2')
     >>> subparser2.add_argument('y')
     >>> parser.parse_args(['2', 'frobble'])
     Namespace(subparser_name='2', y='frobble')

   .. versionchanged:: 3.7
      Tham số chỉ từ khóa *required* mới.

   .. versionchanged:: 3.14
      *prog* của subparser không còn bị ảnh hưởng bởi thông báo usage tùy chỉnh trong parser chính.


Đối tượng FileType
^^^^^^^^^^^^^^^^^^

.. class:: FileType(mode='r', bufsize=-1, encoding=None, errors=None)

   Factory :class:`FileType` tạo các đối tượng có thể được truyền vào đối số type của :meth:`ArgumentParser.add_argument`. Các đối số có
   kiểu là đối tượng :class:`FileType` sẽ mở các đối số dòng lệnh dưới dạng tệp với các chế độ, kích thước bộ đệm, encoding và cách xử lý lỗi được yêu cầu (xem hàm :func:`open` để biết thêm chi tiết)::

      >>> parser = argparse.ArgumentParser()
      >>> parser.add_argument('--raw', type=argparse.FileType('wb', 0))
      >>> parser.add_argument('out', type=argparse.FileType('w', encoding='UTF-8'))
      >>> parser.parse_args(['--raw', 'raw.dat', 'file.txt'])
      Namespace(out=<_io.TextIOWrapper name='file.txt' mode='w' encoding='UTF-8'>, raw=<_io.FileIO name='raw.dat' mode='wb'>)

   Các đối tượng FileType hiểu đối số giả ``'-'`` và tự động chuyển đổi đối số này thành :data:`sys.stdin` cho các đối tượng :class:`FileType` có thể đọc và
   :data:`sys.stdout` cho các đối tượng :class:`FileType` có thể ghi::

      >>> parser = argparse.ArgumentParser()
      >>> parser.add_argument('infile', type=argparse.FileType('r'))
      >>> parser.parse_args(['-'])
      Namespace(infile=<_io.TextIOWrapper name='<stdin>' encoding='UTF-8'>)

   .. note::

      Nếu một đối số sử dụng *FileType* rồi một đối số tiếp theo không thành công, lỗi sẽ được báo cáo nhưng tệp không được tự động đóng. Điều này cũng có thể ghi đè các tệp đầu ra. Trong trường hợp này, tốt hơn nên đợi cho đến khi parser chạy xong rồi sử dụng câu lệnh :keyword:`with` để quản lý các tệp.

   .. versionchanged:: 3.4
      Đã thêm các tham số *encoding* và *errors*.

   .. deprecated:: 3.14


Các nhóm đối số
^^^^^^^^^^^^^^^

.. method:: ArgumentParser.add_argument_group(title=None, description=None, *, \
                                              [argument_default], [conflict_handler])

   Theo mặc định, :class:`ArgumentParser` nhóm các đối số dòng lệnh thành "positional arguments" và "options" khi hiển thị thông báo trợ giúp. Khi có cách nhóm đối số phù hợp hơn về mặt khái niệm so với cách mặc định này, bạn có thể tạo các nhóm thích hợp bằng cách sử dụng
   phương thức :meth:`!add_argument_group`::

     >>> parser = argparse.ArgumentParser(prog='PROG', add_help=False)
     >>> group = parser.add_argument_group('group')
     >>> group.add_argument('--foo', help='foo help')
     >>> group.add_argument('bar', help='bar help')
     >>> parser.print_help()
     usage: PROG [--foo FOO] bar

     group:
       bar    bar help
       --foo FOO  foo help

   Phương thức :meth:`add_argument_group` trả về một đối tượng nhóm đối số có phương thức :meth:`~ArgumentParser.add_argument` giống như một
   :class:`ArgumentParser` thông thường. Khi một đối số được thêm vào nhóm, parser xử lý nó giống như một đối số thông thường, nhưng hiển thị đối số đó trong một nhóm riêng biệt trong các thông báo trợ giúp. Phương thức :meth:`!add_argument_group` chấp nhận các đối số *title* và *description*, có thể được dùng để tùy chỉnh nội dung hiển thị này::

     >>> parser = argparse.ArgumentParser(prog='PROG', add_help=False)
     >>> group1 = parser.add_argument_group('group1', 'group1 description')
     >>> group1.add_argument('foo', help='foo help')
     >>> group2 = parser.add_argument_group('group2', 'group2 description')
     >>> group2.add_argument('--bar', help='bar help')
     >>> parser.print_help()
     usage: PROG [--bar BAR] foo

     group1:
       group1 description

       foo    foo help

     group2:
       group2 description

       --bar BAR  bar help

   Các tham số chỉ dành cho từ khóa và không bắt buộc argument_default_ và conflict_handler_ cho phép kiểm soát chi tiết hơn hành vi của nhóm đối số. Các tham số này có cùng ý nghĩa như trong hàm khởi tạo :class:`ArgumentParser`, nhưng chỉ áp dụng cho nhóm đối số thay vì toàn bộ parser.

   Lưu ý rằng mọi đối số không nằm trong các nhóm do bạn định nghĩa sẽ được đưa trở lại các phần thông thường "positional arguments" và "optional arguments".

   Trong mỗi nhóm đối số, các đối số được hiển thị trong đầu ra trợ giúp theo thứ tự mà chúng được thêm vào.

   .. deprecated-removed:: 3.11 3.14
      Hiện tại, việc gọi :meth:`add_argument_group` trên một nhóm đối số sẽ phát sinh ngoại lệ. Việc lồng nhóm này chưa bao giờ được hỗ trợ, thường không hoạt động chính xác và đã vô tình được để lộ thông qua tính kế thừa.

   .. deprecated:: 3.14
      Việc truyền prefix_chars_ cho :meth:`add_argument_group` hiện không còn được khuyến nghị.


Loại trừ lẫn nhau
^^^^^^^^^^^^^^^^^

.. method:: ArgumentParser.add_mutually_exclusive_group(required=False)

   Tạo một nhóm loại trừ lẫn nhau. :mod:`!argparse` sẽ đảm bảo rằng chỉ một trong các đối số thuộc nhóm loại trừ lẫn nhau xuất hiện trên dòng lệnh::

     >>> parser = argparse.ArgumentParser(prog='PROG')
     >>> group = parser.add_mutually_exclusive_group()
     >>> group.add_argument('--foo', action='store_true')
     >>> group.add_argument('--bar', action='store_false')
     >>> parser.parse_args(['--foo'])
     Namespace(bar=True, foo=True)
     >>> parser.parse_args(['--bar'])
     Namespace(bar=False, foo=False)
     >>> parser.parse_args(['--foo', '--bar'])
     usage: PROG [-h] [--foo | --bar]
     PROG: error: argument --bar: not allowed with argument --foo

   Phương thức :meth:`add_mutually_exclusive_group` cũng chấp nhận đối số *required*, để cho biết rằng cần có ít nhất một trong các đối số loại trừ lẫn nhau::

     >>> parser = argparse.ArgumentParser(prog='PROG')
     >>> group = parser.add_mutually_exclusive_group(required=True)
     >>> group.add_argument('--foo', action='store_true')
     >>> group.add_argument('--bar', action='store_false')
     >>> parser.parse_args([])
     usage: PROG [-h] (--foo | --bar)
     PROG: error: one of the arguments --foo --bar is required

   Lưu ý rằng hiện tại, các nhóm đối số loại trừ lẫn nhau không hỗ trợ các đối số *title* và *description* của
   :meth:`~ArgumentParser.add_argument_group`. Tuy nhiên, một nhóm loại trừ lẫn nhau có thể được thêm vào một nhóm đối số có tiêu đề và mô tả. Ví dụ::

     >>> parser = argparse.ArgumentParser(prog='PROG')
     >>> group = parser.add_argument_group('Group title', 'Group description')
     >>> exclusive_group = group.add_mutually_exclusive_group(required=True)
     >>> exclusive_group.add_argument('--foo', help='foo help')
     >>> exclusive_group.add_argument('--bar', help='bar help')
     >>> parser.print_help()
     usage: PROG [-h] (--foo FOO | --bar BAR)

     options:
       -h, --help  show this help message and exit

     Group title:
       Group description

       --foo FOO   foo help
       --bar BAR   bar help

   .. deprecated-removed:: 3.11 3.14
      Việc gọi :meth:`add_argument_group` hoặc :meth:`add_mutually_exclusive_group` trên một nhóm loại trừ lẫn nhau hiện sẽ phát sinh ngoại lệ. Kiểu lồng ghép này chưa bao giờ được hỗ trợ, thường không hoạt động chính xác và đã vô tình được cung cấp thông qua tính kế thừa.


Giá trị mặc định của parser
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. method:: ArgumentParser.set_defaults(**kwargs)

   Trong hầu hết trường hợp, các thuộc tính của đối tượng được trả về bởi :meth:`parse_args` sẽ được xác định hoàn toàn bằng cách kiểm tra các đối số dòng lệnh và các argument action. :meth:`set_defaults` cho phép thêm một số thuộc tính bổ sung được xác định mà không cần kiểm tra dòng lệnh::

     >>> parser = argparse.ArgumentParser()
     >>> parser.add_argument('foo', type=int)
     >>> parser.set_defaults(bar=42, baz='badger')
     >>> parser.parse_args(['736'])
     Namespace(bar=42, baz='badger', foo=736)

   Lưu ý rằng có thể thiết lập giá trị mặc định ở cả cấp parser bằng :meth:`set_defaults` và cấp argument bằng :meth:`add_argument`. Nếu cả hai đều được gọi cho cùng một argument, giá trị mặc định được thiết lập sau cùng cho argument đó sẽ được sử dụng::

     >>> parser = argparse.ArgumentParser()
     >>> parser.add_argument('--foo', default='bar')
     >>> parser.set_defaults(foo='spam')
     >>> parser.parse_args([])
     Namespace(foo='spam')

   Giá trị mặc định ở cấp parser đặc biệt hữu ích khi làm việc với nhiều parser. Xem phương thức :meth:`~ArgumentParser.add_subparsers` để biết ví dụ về loại này.

.. method:: ArgumentParser.get_default(dest)

   Lấy giá trị mặc định cho một thuộc tính namespace, được thiết lập bởi một trong hai cách sau
   :meth:`~ArgumentParser.add_argument` hoặc bằng
   :meth:`~ArgumentParser.set_defaults`::

     >>> parser = argparse.ArgumentParser()
     >>> parser.add_argument('--foo', default='badger')
     >>> parser.get_default('foo')
     'badger'


In thông tin trợ giúp
^^^^^^^^^^^^^^^^^^^^^

Trong hầu hết các ứng dụng thông thường, :meth:`~ArgumentParser.parse_args` sẽ đảm nhiệm việc định dạng và in mọi thông báo về cách sử dụng hoặc lỗi. Tuy nhiên, có sẵn một số phương thức định dạng:

.. method:: ArgumentParser.print_usage(file=None)

   In mô tả ngắn gọn về cách :class:`ArgumentParser` nên được gọi trên dòng lệnh. Nếu *file* là ``None``, thì :data:`sys.stdout` được giả định.

.. method:: ArgumentParser.print_help(file=None)

   In thông báo trợ giúp, bao gồm cách sử dụng chương trình và thông tin về các đối số đã đăng ký với :class:`ArgumentParser`. Nếu *file* là ``None``, thì :data:`sys.stdout` được giả định.

Ngoài ra còn có các biến thể của những phương thức này, chỉ trả về một chuỗi thay vì in chuỗi đó:

.. method:: ArgumentParser.format_usage()

   Trả về một chuỗi chứa mô tả ngắn gọn về cách
   :class:`ArgumentParser` nên được gọi trên dòng lệnh.

.. method:: ArgumentParser.format_help()

   Trả về một chuỗi chứa thông báo trợ giúp, bao gồm cách sử dụng chương trình và thông tin về các đối số đã đăng ký với :class:`ArgumentParser`.


Phân tích cú pháp một phần
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. method:: ArgumentParser.parse_known_args(args=None, namespace=None)

   Đôi khi, một script chỉ cần xử lý một tập hợp đối số dòng lệnh cụ thể và để các đối số không được nhận dạng cho một script hoặc chương trình khác. Trong những trường hợp này, phương thức :meth:`~ArgumentParser.parse_known_args` có thể hữu ích.

   Phương thức này hoạt động tương tự như :meth:`~ArgumentParser.parse_args`, nhưng không báo lỗi đối với các đối số thừa, không được nhận dạng. Thay vào đó, phương thức phân tích các đối số đã biết và trả về một tuple gồm hai phần tử, chứa namespace đã được điền và danh sách mọi đối số không được nhận dạng.

   ::

      >>> parser = argparse.ArgumentParser()
      >>> parser.add_argument('--foo', action='store_true')
      >>> parser.add_argument('bar')
      >>> parser.parse_known_args(['--foo', '--badger', 'BAR', 'spam'])
      (Namespace(bar='BAR', foo=True), ['--badger', 'spam'])

.. warning::
   :ref:`Prefix matching <prefix-matching>` rules apply to
   :meth:`~ArgumentParser.parse_known_args`. The parser may consume an option even if it's just
   một tiền tố của một trong các tùy chọn đã biết, thay vì để nó trong danh sách các đối số còn lại.


Tùy chỉnh việc phân tích cú pháp tệp
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. method:: ArgumentParser.convert_arg_line_to_args(arg_line)

   Các đối số được đọc từ một tệp (xem đối số từ khóa *fromfile_prefix_chars* của hàm khởi tạo :class:`ArgumentParser`) được đọc, mỗi dòng một đối số. Có thể ghi đè :meth:`convert_arg_line_to_args` để thực hiện cách đọc nâng cao hơn.

   Phương thức này nhận một đối số duy nhất *arg_line*, là một chuỗi được đọc từ tệp đối số. Phương thức trả về một danh sách các đối số được phân tích từ chuỗi này. Phương thức được gọi tuần tự một lần cho mỗi dòng được đọc từ tệp đối số.

   Một cách override hữu ích cho phương thức này là coi mỗi từ được phân tách bằng dấu cách là một đối số. Ví dụ sau đây minh họa cách thực hiện điều này::

    class MyArgumentParser(argparse.ArgumentParser):
        def convert_arg_line_to_args(self, arg_line):
            return arg_line.split()

   Lưu ý rằng với cách override này, một đối số không còn có thể chứa dấu cách, vì mỗi từ được phân tách bằng dấu cách sẽ trở thành một đối số riêng biệt.


Các phương thức thoát
^^^^^^^^^^^^^^^^^^^^^

.. method:: ArgumentParser.exit(status=0, message=None)

   Phương thức này kết thúc chương trình với *trạng thái* được chỉ định và, nếu được cung cấp, sẽ in *thông báo* tới :data:`sys.stderr` trước đó. Người dùng có thể override phương thức này để xử lý các bước này theo cách khác::

    class ErrorCatchingArgumentParser(argparse.ArgumentParser):
        def exit(self, status=0, message=None):
            if status:
                raise Exception(f'Exiting because of an error: {message}')
            exit(status)

.. method:: ArgumentParser.error(message)

   Phương thức này in thông báo sử dụng, bao gồm *thông báo*, tới
   :data:`sys.stderr` và kết thúc chương trình với mã trạng thái là 2.


Phân tích xen kẽ
^^^^^^^^^^^^^^^^

.. method:: ArgumentParser.parse_intermixed_args(args=None, namespace=None)
.. method:: ArgumentParser.parse_known_intermixed_args(args=None, namespace=None)

   Một số lệnh Unix cho phép người dùng xen kẽ các đối số tùy chọn với các đối số vị trí. Các phương thức :meth:`~ArgumentParser.parse_intermixed_args` và :meth:`~ArgumentParser.parse_known_intermixed_args` hỗ trợ kiểu phân tích cú pháp này.

   Các parser này không hỗ trợ tất cả các tính năng của :mod:`!argparse` và sẽ phát sinh ngoại lệ nếu sử dụng các tính năng không được hỗ trợ. Cụ thể, subparser và các nhóm loại trừ lẫn nhau có cả đối số tùy chọn lẫn đối số vị trí đều không được hỗ trợ.

   Ví dụ sau đây cho thấy sự khác biệt giữa
   :meth:`~ArgumentParser.parse_known_args` và
   :meth:`~ArgumentParser.parse_intermixed_args`: cái trước trả về ``['2', '3']`` dưới dạng các đối số chưa được phân tích, còn cái sau tập hợp tất cả các đối số vị trí vào ``rest``.::

      >>> parser = argparse.ArgumentParser()
      >>> parser.add_argument('--foo')
      >>> parser.add_argument('cmd')
      >>> parser.add_argument('rest', nargs='*', type=int)
      >>> parser.parse_known_args('doit 1 --foo bar 2 3'.split())
      (Namespace(cmd='doit', foo='bar', rest=[1]), ['2', '3'])
      >>> parser.parse_intermixed_args('doit 1 --foo bar 2 3'.split())
      Namespace(cmd='doit', foo='bar', rest=[1, 2, 3])

   :meth:`~ArgumentParser.parse_known_intermixed_args` trả về một tuple gồm hai phần tử, chứa namespace đã được điền và danh sách các chuỗi đối số còn lại.
   :meth:`~ArgumentParser.parse_intermixed_args` sẽ báo lỗi nếu còn bất kỳ chuỗi đối số nào chưa được phân tích.

   .. versionadded:: 3.7


Đăng ký các kiểu hoặc action tùy chỉnh
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. method:: ArgumentParser.register(registry_name, value, object)

   Đôi khi, việc sử dụng một chuỗi tùy chỉnh trong thông báo lỗi là điều hữu ích để tạo ra nội dung thân thiện hơn với người dùng. Trong những trường hợp này, :meth:`!register` có thể được dùng để đăng ký các action hoặc kiểu tùy chỉnh với parser và cho phép bạn tham chiếu đến kiểu bằng tên đã đăng ký thay vì tên callable của kiểu đó.

   Phương thức :meth:`!register` nhận ba đối số - một *registry_name*, chỉ định registry nội bộ nơi đối tượng sẽ được lưu trữ (ví dụ: ``action``, ``type``), một *value*, là khóa dùng để đăng ký đối tượng, và object, callable cần đăng ký.

   Ví dụ sau đây cho biết cách đăng ký một kiểu tùy chỉnh với parser::

      >>> import argparse
      >>> parser = argparse.ArgumentParser()
      >>> parser.register('type', 'hexadecimal integer', lambda s: int(s, 16))
      >>> parser.add_argument('--foo', type='hexadecimal integer')
      _StoreAction(option_strings=['--foo'], dest='foo', nargs=None, const=None, default=None, type='hexadecimal integer', choices=None, required=False, help=None, metavar=None, deprecated=False)
      >>> parser.parse_args(['--foo', '0xFA'])
      Namespace(foo=250)
      >>> parser.parse_args(['--foo', '1.2'])
      usage: PROG [-h] [--foo FOO]
      PROG: error: argument --foo: invalid 'hexadecimal integer' value: '1.2'

Ngoại lệ
--------

.. exception:: ArgumentError

   Lỗi phát sinh khi tạo hoặc sử dụng một đối số (tùy chọn hoặc vị trí).

   Giá trị chuỗi của ngoại lệ này là thông báo, được bổ sung thông tin về đối số gây ra lỗi.

.. exception:: ArgumentTypeError

   Được phát sinh khi xảy ra lỗi trong quá trình chuyển đổi chuỗi dòng lệnh sang một kiểu dữ liệu.


.. rubric:: Hướng dẫn và Bài hướng dẫn

.. toctree::
   :maxdepth: 1

   ../howto/argparse.rst
   ../howto/argparse-optparse.rst
